# -*- coding: utf-8 -*-
"""
GRPO数据集生成器核心模块

运行SUMO仿真，在决策点收集数据并保存状态。
"""

import os
import json
import random
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime

from .config import GRPOConfig, SYSTEM_PROMPT
from .sumo_interface import SUMOInterface, PhaseInfo
from .prompt_builder import build_extend_decision_prompt, generate_timestamp


@dataclass
class GRPODataEntry:
    """GRPO数据集条目"""
    id: str                         # 唯一ID
    scenario: str                   # 场景名称
    junction_id: str                # 路口ID
    simulation_time: float          # 仿真时刻（秒）
    current_phase_id: int           # 当前绿灯相位ID（SUMO内部索引）
    current_phase_order_idx: int    # 当前相位在phase_order中的索引
    current_green_elapsed: float    # 当前绿灯已持续时间
    min_green: float                # 该相位最小绿（含随机偏移后）
    max_green: float                # 该相位最大绿（含随机偏移后）
    extend_seconds: int             # 决策延长秒数
    can_extend: bool                # 是否还可以延长（未达最大绿）
    phase_order: List[int]          # 相位执行顺序
    phase_metrics: Dict[str, float] # 各相位平均排队数 {str(phase_id): avg_queue}
    prompt: str                     # 输入JSON（不含系统提示）
    state_file: str                 # 仿真状态文件路径（相对路径）
    expert_decision: Optional[str] = None  # 专家决策 "yes" / "no"，用于SFT


class GRPODatasetGenerator:
    """GRPO数据集生成器"""
    
    def __init__(self, config: Optional[GRPOConfig] = None):
        """
        初始化生成器
        
        Args:
            config: 配置对象，None则使用默认配置
        """
        self.config = config or GRPOConfig()
        self.sumo: Optional[SUMOInterface] = None
        
        # 相位的随机min/max green缓存 {(scenario, tl_id, phase_id): (min_green, max_green)}
        self._green_time_cache: Dict[tuple, tuple] = {}
    
    def _get_randomized_green_times(
        self, 
        scenario: str, 
        tl_id: str, 
        phase: PhaseInfo
    ) -> tuple:
        """
        获取随机偏移后的min/max green
        
        每个(scenario, tl, phase)组合只随机一次，后续使用缓存值
        """
        cache_key = (scenario, tl_id, phase.phase_id)
        
        if cache_key not in self._green_time_cache:
            # 随机偏移
            min_offset = random.uniform(
                -self.config.min_green_offset_range,
                self.config.min_green_offset_range
            )
            max_offset = random.uniform(
                -self.config.max_green_offset_range,
                self.config.max_green_offset_range
            )
            
            randomized_min = round(max(5.0, phase.min_dur + min_offset))  # 至少5秒
            randomized_max = round(max(randomized_min + 10, phase.max_dur + max_offset))
            
            self._green_time_cache[cache_key] = (randomized_min, randomized_max)
        
        return self._green_time_cache[cache_key]
    
    def _is_decision_point(
        self,
        green_elapsed: float,
        min_green: float,
        extend_seconds: int
    ) -> bool:
        """
        判断是否为决策点
        
        决策点：
        1. 到达最小绿时刻（首次决策）
        2. 超过最小绿后，每隔extend_seconds秒的时刻
        
        Args:
            green_elapsed: 当前绿灯已持续时间
            min_green: 最小绿灯时间
            extend_seconds: 决策间隔秒数
            
        Returns:
            是否为决策点
        """
        # 使用容差处理浮点数比较
        tolerance = 0.5
        
        # 首次决策：到达最小绿时刻
        if abs(green_elapsed - min_green) < tolerance:
            return True
        
        # 后续决策：超过最小绿后，每隔extend_seconds秒
        if green_elapsed > min_green:
            time_since_min_green = green_elapsed - min_green
            # 检查是否刚好到达决策间隔点
            remainder = time_since_min_green % extend_seconds
            if remainder < tolerance or (extend_seconds - remainder) < tolerance:
                return True
        
        return False
    
    def _create_data_entry(
        self,
        scenario: str,
        tl_id: str,
        sim_time: float,
        phase: PhaseInfo,
        phase_order: List[int],
        phase_order_idx: int,
        green_elapsed: float,
        min_green: float,
        max_green: float,
        phase_metrics: Dict[int, float],
        state_file: str,
        decision_count: int
    ) -> GRPODataEntry:
        """创建数据条目"""
        # 生成唯一ID
        entry_id = f"{scenario}_{tl_id}_{int(sim_time)}_{decision_count}"
        
        # 判断是否还能延长
        can_extend = (green_elapsed + self.config.extend_seconds) <= max_green
        
        # 生成时间戳
        timestamp = generate_timestamp(sim_time)
        
        # 构建prompt (仅输入JSON部分)
        prompt = build_extend_decision_prompt(
            crossing_id=hash(tl_id) % 10000,  # 将tl_id转为数字
            as_of=timestamp,
            phase_order=phase_order,
            current_phase_id=phase.phase_id,
            phase_metrics=phase_metrics
        )
        
        # 转换phase_metrics的key为字符串
        phase_metrics_str = {str(k): v for k, v in phase_metrics.items()}
        
        return GRPODataEntry(
            id=entry_id,
            scenario=scenario,
            junction_id=tl_id,
            simulation_time=sim_time,
            current_phase_id=phase.phase_id,
            current_phase_order_idx=phase_order_idx,
            current_green_elapsed=green_elapsed,
            min_green=min_green,
            max_green=max_green,
            extend_seconds=self.config.extend_seconds,
            can_extend=can_extend,
            phase_order=phase_order,
            phase_metrics=phase_metrics_str,
            prompt=prompt,
            state_file=state_file
        )
    
    def generate_for_scenario(
        self, 
        scenario_name: str,
        output_dir: Optional[str] = None,
        port: Optional[int] = None
    ) -> List[GRPODataEntry]:
        """
        为单个场景生成GRPO数据集
        
        Args:
            scenario_name: 场景名称（环境目录下的子目录名）
            output_dir: 输出目录，None则使用默认
            port: SUMO端口，None则随机
            
        Returns:
            生成的数据条目列表
        """
        # 构建路径
        scenario_dir = os.path.join(self.config.scenarios_dir, scenario_name)
        sumocfg = self._find_sumocfg(scenario_dir)
        
        if not sumocfg:
            print(f"[{scenario_name}] 未找到.sumocfg文件")
            return []
        
        output_dir = output_dir or os.path.join(self.config.output_dir, scenario_name)
        states_dir = os.path.join(output_dir, "states")
        os.makedirs(states_dir, exist_ok=True)
        
        print(f"[{scenario_name}] 开始生成GRPO数据集...")
        print(f"[{scenario_name}] 配置文件: {sumocfg}")
        print(f"[{scenario_name}] 输出目录: {output_dir}")
        
        # 初始化SUMO接口
        self.sumo = SUMOInterface(
            config_file=sumocfg,
            port=port,
            gui=self.config.use_gui,
            verbose=False
        )
        
        # 启动仿真
        if not self.sumo.start(warmup_steps=self.config.warmup_steps):
            print(f"[{scenario_name}] SUMO启动失败")
            return []
        
        try:
            data_entries = self._run_collection_loop(scenario_name, states_dir)
            
            # 保存数据集
            self._save_dataset(data_entries, output_dir)
            
            print(f"[{scenario_name}] 生成完成，共 {len(data_entries)} 条数据")
            return data_entries
            
        finally:
            self.sumo.close()
    
    def _run_collection_loop(
        self, 
        scenario_name: str, 
        states_dir: str
    ) -> List[GRPODataEntry]:
        """运行数据收集循环"""
        data_entries = []
        decision_counts = {}  # {tl_id: count}
        
        # 获取所有信号灯
        tl_ids = self.sumo.get_traffic_lights()
        if not tl_ids:
            print(f"[{scenario_name}] 未找到信号灯")
            return []
        
        print(f"[{scenario_name}] 信号灯: {tl_ids}")
        
        # 获取各信号灯的有效相位信息
        tl_phases: Dict[str, List[PhaseInfo]] = {}
        tl_phase_orders: Dict[str, List[int]] = {}
        
        for tl_id in tl_ids:
            valid_phases = self.sumo.get_valid_phases(tl_id, self.config)
            if valid_phases:
                tl_phases[tl_id] = valid_phases
                # 相位顺序：有效相位的ID列表
                tl_phase_orders[tl_id] = [p.phase_id for p in valid_phases]
                decision_counts[tl_id] = 0
                print(f"[{scenario_name}] {tl_id} 有效相位: {tl_phase_orders[tl_id]}")
        
        # 跟踪每个信号灯当前相位的起始时间
        phase_start_times: Dict[str, float] = {tl_id: 0 for tl_id in tl_phases}
        last_phase_indices: Dict[str, int] = {}
        
        step_count = 0
        max_steps = 1000000  # 安全上限
        
        while step_count < max_steps:
            # 执行一步仿真
            if not self.sumo.step():
                print(f"[{scenario_name}] 仿真结束")
                break
            
            step_count += 1
            sim_time = self.sumo.get_simulation_time()
            
            # 每1000步打印进度
            if step_count % 1000 == 0:
                print(f"[{scenario_name}] 步数: {step_count}, 时间: {sim_time:.0f}s, 数据: {len(data_entries)}条")
            
            # 检查每个信号灯
            for tl_id, phases in tl_phases.items():
                current_sumo_phase = self.sumo.get_current_phase_index(tl_id)
                
                # 检测相位是否切换
                if tl_id in last_phase_indices:
                    if current_sumo_phase != last_phase_indices[tl_id]:
                        phase_start_times[tl_id] = sim_time
                
                last_phase_indices[tl_id] = current_sumo_phase
                
                # 检查当前相位是否为有效相位
                current_phase = None
                phase_order_idx = -1
                for idx, phase in enumerate(phases):
                    if phase.phase_id == current_sumo_phase:
                        current_phase = phase
                        phase_order_idx = idx
                        break
                
                if current_phase is None:
                    continue  # 当前相位不是有效相位（如黄灯）
                
                # 计算绿灯已持续时间
                green_elapsed = sim_time - phase_start_times[tl_id]
                
                # 获取随机偏移后的min/max green
                min_green, max_green = self._get_randomized_green_times(
                    scenario_name, tl_id, current_phase
                )
                
                # 检查是否为决策点
                if self._is_decision_point(green_elapsed, min_green, self.config.extend_seconds):
                    # 获取各相位排队数
                    phase_metrics = self.sumo.get_all_phases_queue(tl_id)
                    
                    # === 基于有效相位比例的过滤逻辑 ===
                    # 计算有值（非零）的相位占比，以此作为保留该条数据的概率
                    total_phases = len(phase_metrics)
                    if total_phases > 0:
                        non_zero_phases = sum(1 for v in phase_metrics.values() if v > 0)
                        keep_probability = non_zero_phases / total_phases
                        
                        # 根据概率决定是否保留
                        if keep_probability == 0:
                            # 所有相位都为0，不保留
                            continue
                        elif keep_probability < 1.0:
                            # 部分相位有值，按概率保留
                            if random.random() > keep_probability:
                                continue
                        # keep_probability == 1.0 时，100%保留
                    
                    # 保存仿真状态
                    decision_counts[tl_id] += 1
                    state_filename = f"state_{tl_id}_{int(sim_time)}_{decision_counts[tl_id]}.xml"
                    state_filepath = os.path.join(states_dir, state_filename)
                    
                    if decision_counts[tl_id] % self.config.state_save_interval == 0:
                        self.sumo.save_state(state_filepath)
                        relative_state_path = os.path.join("states", state_filename)
                    else:
                        relative_state_path = ""  # 不保存状态
                    
                    # 创建数据条目
                    entry = self._create_data_entry(
                        scenario=scenario_name,
                        tl_id=tl_id,
                        sim_time=sim_time,
                        phase=current_phase,
                        phase_order=tl_phase_orders[tl_id],
                        phase_order_idx=phase_order_idx,
                        green_elapsed=green_elapsed,
                        min_green=min_green,
                        max_green=max_green,
                        phase_metrics=phase_metrics,
                        state_file=relative_state_path,
                        decision_count=decision_counts[tl_id]
                    )
                    data_entries.append(entry)
        
        return data_entries
    
    def _find_sumocfg(self, scenario_dir: str) -> Optional[str]:
        """查找场景目录下的.sumocfg文件"""
        if not os.path.isdir(scenario_dir):
            return None
        
        for f in os.listdir(scenario_dir):
            if f.endswith('.sumocfg'):
                return os.path.join(scenario_dir, f)
        return None
    
    def _save_dataset(self, entries: List[GRPODataEntry], output_dir: str):
        """保存数据集到JSON文件"""
        output_file = os.path.join(output_dir, "grpo_dataset.json")
        
        # 转换为字典列表
        data = [asdict(entry) for entry in entries]
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"数据集已保存: {output_file}")


def run_single_scenario(args: tuple) -> List[dict]:
    """
    运行单个场景的数据生成（用于并行执行）
    
    Args:
        args: (scenario_name, config_dict, output_dir, port)
        
    Returns:
        数据条目字典列表
    """
    scenario_name, config_dict, output_dir, port = args
    
    config = GRPOConfig(**config_dict) if config_dict else GRPOConfig()
    generator = GRPODatasetGenerator(config)
    
    entries = generator.generate_for_scenario(
        scenario_name=scenario_name,
        output_dir=output_dir,
        port=port
    )
    
    return [asdict(entry) for entry in entries]
