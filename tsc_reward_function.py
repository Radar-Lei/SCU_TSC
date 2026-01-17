"""
TSC GRPO Reward Function

用于标准 Unsloth GRPOTrainer 的 reward 计算函数。
在 reward 计算时：
1. 从 dataset 字段恢复 SUMO state
2. 解析 completion（JSON 格式的信号配时方案）
3. 使用 rollback 评估交通指标
4. 返回每个 completion 的 reward

关键：同一 prompt 的多个 completion 共享同一个 SUMO state checkpoint。
"""

import os
import sys
import torch
from typing import List, Dict, Any, Union
from collections import defaultdict
import json
import re
from multiprocessing import Pool, cpu_count
from functools import partial

# 添加项目路径
sumo_sim_path = os.path.join(os.getcwd(), 'sumo_simulation')
if sumo_sim_path not in sys.path:
    sys.path.insert(0, sumo_sim_path)

from sumo_simulator import SUMOSimulator

sys.path.insert(0, os.getcwd())
from scu_tsc_newprompt.rewards import (
    score_constraints_and_format,
    AdaptiveScaler,
    compute_sim_reward_adaptive,
    compute_total_reward,
)


# ==================== 全局配置 ====================
REWARD_CONFIG = {
    'gui': False,
    'w_passed': 1.0,
    'w_queue': 1.0,
    'w_proxy': 0.2,
    'w_sim': 1.5,
    'w_constraint': 1.5,
    'D0': 25.0,  # 软约束归一化尺度
    'alpha_passed': 1.0,
    'beta_queue': 0.5,
    'invalid_output_reward': -2.0,
    'parallel_workers': 0,  # 默认单进程+复用SimulatorPool（更稳定）
    'green_sec_min': 1,     # signal_step 的 green_sec 下限
    'green_sec_max': 120,   # signal_step 的 green_sec 上限
}


# ==================== Simulator 池管理 ====================
class SimulatorPool:
    """
    管理 SUMO simulator 实例的对象池。
    为每个 (scenario, sumocfg) 维护一个 simulator 实例，避免频繁创建/销毁。
    """
    
    def __init__(self):
        self._pool: Dict[str, SUMOSimulator] = {}
        self._scalers: Dict[str, AdaptiveScaler] = {}  # 每个 tl_id 一个 scaler
    
    def get_simulator(self, scenario: str, sumocfg: str) -> SUMOSimulator:
        """获取或创建 simulator"""
        key = f"{scenario}:{sumocfg}"
        
        if key not in self._pool:
            print(f"[SimulatorPool] 创建新 simulator: {scenario}")
            sim = SUMOSimulator(
                config_file=sumocfg,
                junctions_file=None,
                gui=REWARD_CONFIG['gui'],
                additional_options=['--device.rerouting.probability', '0'],  # 禁用动态重路由
            )
            if not sim.start_simulation():
                raise RuntimeError(f"无法启动 SUMO simulator: {scenario}")
            self._pool[key] = sim
        
        return self._pool[key]
    
    def get_scaler(self, tl_id: str) -> AdaptiveScaler:
        """获取或创建 scaler"""
        if tl_id not in self._scalers:
            self._scalers[tl_id] = AdaptiveScaler()
        return self._scalers[tl_id]
    
    def close_all(self):
        """关闭所有 simulator"""
        for sim in self._pool.values():
            try:
                sim.close()
            except Exception as e:
                print(f"关闭 simulator 失败: {e}")
        self._pool.clear()
        self._scalers.clear()


# 全局 simulator 池
_GLOBAL_POOL = SimulatorPool()


# ==================== 评估辅助函数 ====================
def evaluate_plan_once_reward_fn(
    simulator: SUMOSimulator,
    tl_id: str,
    plan: List[dict]
) -> dict:
    """
    在当前 SUMO state 下执行一个信号配时方案并返回交通指标。
    
    Args:
        simulator: SUMO 仿真器实例
        tl_id: 信号灯 ID
        plan: 配时方案 [{"phase_id": int, "final": int}, ...]
    
    Returns:
        dict: {"passed_vehicles": float, "queue_vehicles": float, "total_queue_proxy": float, "sim_time": float}
    """
    import traci
    
    # 收集所有相位控制的 lanes
    phase_info = simulator.get_phase_info(tl_id)
    n = int(phase_info.get('num_phases', 0))
    all_lanes = set()
    for idx in range(n):
        all_lanes.update(simulator.get_phase_controlled_lanes(tl_id, idx).get('incoming_lanes', []))
    all_lanes = list(all_lanes)
    
    # 记录执行前的车辆
    vehicles_before = set()
    for ln in all_lanes:
        try:
            vehicles_before.update(traci.lane.getLastStepVehicleIDs(ln))
        except Exception:
            pass
    
    # 执行配时方案
    total_queue_proxy = 0.0
    for step in plan:
        pid = int(step['phase_id'])
        dur = int(step['final'])
        traci.trafficlight.setPhase(tl_id, pid - 1)
        for _ in range(max(0, dur)):
            traci.simulationStep()
            q = 0.0
            for ln in all_lanes:
                try:
                    q += traci.lane.getLastStepHaltingNumber(ln)
                except Exception:
                    pass
            total_queue_proxy += q
    
    # 记录执行后的车辆和排队
    vehicles_after = set()
    queue_end = 0.0
    for ln in all_lanes:
        try:
            vehicles_after.update(traci.lane.getLastStepVehicleIDs(ln))
            queue_end += traci.lane.getLastStepHaltingNumber(ln)
        except Exception:
            pass
    
    passed = len(vehicles_before - vehicles_after)
    
    return {
        'passed_vehicles': float(passed),
        'queue_vehicles': float(queue_end),
        'total_queue_proxy': float(total_queue_proxy),
        'sim_time': float(traci.simulation.getTime()),
    }


def _extract_json_object(text: str) -> Union[Dict[str, Any], None]:
    """
    提取JSON对象，使用最后一个匹配的 {...}（更容错）。
    """
    if not text:
        return None
    s = text.strip()
    
    # 快速路径：纯JSON
    if s.startswith("{") and s.endswith("}"):
        try:
            return json.loads(s)
        except Exception:
            pass
    
    # 查找所有 {...} 匹配，取最后一个（通常是真正的JSON输出）
    matches = list(re.finditer(r"\{[^{}]*\}", s))
    if not matches:
        # 尝试更复杂的嵌套匹配
        matches = list(re.finditer(r"\{[\s\S]*?\}", s))
    
    # 从后往前尝试解析
    for m in reversed(matches):
        try:
            obj = json.loads(m.group(0))
            if isinstance(obj, dict):
                return obj
        except Exception:
            continue
    
    return None


def _parse_signal_step_output(text: str, debug: bool = False) -> Union[Dict[str, int], None]:
    """
    解析 signal_step 输出，容忍多余字段和数值字符串。
    """
    obj = _extract_json_object(text)
    if not isinstance(obj, dict):
        if debug: print(f"  - 提取的不是dict: {type(obj)}")
        return None
    
    # 容忍多余字段，只检查必需字段是否存在
    if "next_phase_id" not in obj or "green_sec" not in obj:
        if debug: print(f"  - 缺少必需字段: {set(obj.keys())} 需要 {{next_phase_id, green_sec}}")
        return None
    
    # 容忍数值字符串，尝试转换
    try:
        next_phase_id = obj.get("next_phase_id")
        if isinstance(next_phase_id, str):
            next_phase_id = int(next_phase_id)
        elif not isinstance(next_phase_id, int):
            if debug: print(f"  - next_phase_id 无法转为 int: {next_phase_id}")
            return None
        
        green_sec = obj.get("green_sec")
        if isinstance(green_sec, str):
            green_sec = int(green_sec)
        elif not isinstance(green_sec, int):
            if debug: print(f"  - green_sec 无法转为 int: {green_sec}")
            return None
        
        if green_sec <= 0:
            if debug: print(f"  - green_sec <= 0: {green_sec}")
            return None
        
        return {"next_phase_id": int(next_phase_id), "green_sec": int(green_sec)}
    
    except (ValueError, TypeError) as e:
        if debug: print(f"  - 转换错误: {e}")
        return None


def _parse_extend_decision_output(text: str, debug: bool = False) -> Union[Dict[str, Any], None]:
    """
    解析 extend_decision 输出，容忍多余字段、数值字符串和extend同义值。
    """
    obj = _extract_json_object(text)
    if not isinstance(obj, dict):
        if debug: print(f"  - 提取的不是dict: {type(obj)}")
        return None
    
    # 容忍多余字段，只检查必需字段
    if "extend" not in obj or "extend_sec" not in obj:
        if debug: print(f"  - 缺少必需字段: {set(obj.keys())} 需要 {{extend, extend_sec}}")
        return None
    
    try:
        # 容忍 extend 的同义值
        extend = obj.get("extend")
        if isinstance(extend, str):
            extend_lower = extend.lower().strip()
            # 映射同义值
            if extend_lower in ("是", "yes", "true", "1", "延长"):
                extend = "是"
            elif extend_lower in ("否", "no", "false", "0", "不延长"):
                extend = "否"
            else:
                if debug: print(f"  - extend值无法识别: {extend}")
                return None
        elif isinstance(extend, bool):
            extend = "是" if extend else "否"
        else:
            if debug: print(f"  - extend类型错误: {type(extend)}")
            return None
        
        # 容忍数值字符串
        extend_sec = obj.get("extend_sec")
        if isinstance(extend_sec, str):
            extend_sec = int(extend_sec)
        elif not isinstance(extend_sec, int):
            if debug: print(f"  - extend_sec 无法转为 int: {extend_sec}")
            return None
        
        if extend_sec < 0:
            if debug: print(f"  - extend_sec < 0: {extend_sec}")
            return None
        
        return {"extend": extend, "extend_sec": int(extend_sec)}
    
    except (ValueError, TypeError) as e:
        if debug: print(f"  - 转换错误: {e}")
        return None


def _apply_tls_phase_durations(tl_id: str, durations: List[int]):
    """
    应用保存的 TLS 程序相位时长（用于回放时复现随机配时）。
    
    Args:
        tl_id: 信号灯ID
        durations: 各相位的duration列表
    """
    import traci
    
    if not durations:
        return
    
    try:
        logics = traci.trafficlight.getAllProgramLogics(tl_id)
        if not logics:
            return
        logic = logics[0]
        
        # 确保durations数量与phases数量匹配
        if len(durations) != len(logic.phases):
            return
        
        phases = []
        for i, ph in enumerate(logic.phases):
            new_dur = durations[i]
            phases.append(traci.trafficlight.Phase(new_dur, ph.state, ph.minDur, ph.maxDur, ph.next))
        
        new_logic = traci.trafficlight.Logic(
            logic.programID,
            logic.type,
            logic.currentPhaseIndex,
            phases,
            logic.subParameter,
        )
        traci.trafficlight.setProgramLogic(tl_id, new_logic)
    except Exception as e:
        print(f"应用 tls_phase_durations 失败: {e}")


def _get_phase_incoming_lanes(simulator: SUMOSimulator, tl_id: str, phase_id: int) -> List[str]:
    phase_idx = max(0, int(phase_id) - 1)
    info = simulator.get_phase_controlled_lanes(tl_id, phase_idx)
    return list(info.get("incoming_lanes", []))


def _simulate_phase_window(
    simulator: SUMOSimulator,
    tl_id: str,
    phase_id: int,
    duration_sec: int,
) -> Dict[str, float]:
    import traci

    duration = max(0, int(duration_sec))
    lanes = _get_phase_incoming_lanes(simulator, tl_id, phase_id)
    vehicles_before = set()
    for ln in lanes:
        try:
            vehicles_before.update(traci.lane.getLastStepVehicleIDs(ln))
        except Exception:
            pass

    if duration <= 0:
        return {"passed_total": 0.0, "avg_passed_veh": 0.0, "avg_queue_veh": 0.0}

    # 防御性检查：确保目标相位是绿灯相位
    phase_info = simulator.get_phase_info(tl_id)
    phase_states = phase_info.get('phase_states', [])
    target_idx = max(0, int(phase_id) - 1)
    if target_idx < len(phase_states):
        target_state = phase_states[target_idx]
        if not (("G" in target_state) or ("g" in target_state)):
            # 非绿灯相位，返回零 reward
            return {"passed_total": 0.0, "avg_passed_veh": 0.0, "avg_queue_veh": 0.0}

    traci.trafficlight.setPhase(tl_id, target_idx)
    traci.trafficlight.setPhaseDuration(tl_id, duration)

    total_queue = 0.0
    for _ in range(duration):
        traci.simulationStep()
        q = 0.0
        for ln in lanes:
            try:
                q += traci.lane.getLastStepHaltingNumber(ln)
            except Exception:
                pass
        total_queue += q

    vehicles_after = set()
    for ln in lanes:
        try:
            vehicles_after.update(traci.lane.getLastStepVehicleIDs(ln))
        except Exception:
            pass

    passed_total = float(len(vehicles_before - vehicles_after))
    avg_passed_veh = passed_total / max(1, duration)  # 平均通过车辆数
    avg_queue = float(total_queue / max(1, duration))
    return {"passed_total": passed_total, "avg_passed_veh": avg_passed_veh, "avg_queue_veh": avg_queue}


# ==================== 并行 Worker 函数 ====================
def _evaluate_single_completion(args: tuple) -> float:
    """
    并行worker函数：评估单个completion的reward
    
    Args:
        args: (completion_text, state_path, scenario, tl_id, sumocfg, task_type, ...)
    
    Returns:
        float: 该completion的reward
    """
    (completion_text, state_path, scenario, tl_id, sumocfg,
     task_type, phase_ids, decision_lead_sec, decision_remaining_sec,
     wait_time, phase_order, phase_limits, current_elapsed,
     tls_phase_durations) = args
    
    try:
        # 创建独立的simulator实例
        simulator = SUMOSimulator(
            config_file=sumocfg,
            junctions_file=None,
            gui=False,  # 并行worker强制关闭GUI
            additional_options=['--device.rerouting.probability', '0'],
        )
        
        if not simulator.start_simulation():
            return float(REWARD_CONFIG['invalid_output_reward'])
        
        # 恢复SUMO state
        if not os.path.exists(state_path):
            simulator.close()
            return float(REWARD_CONFIG['invalid_output_reward'])
        
        simulator.restore_simulation_state(state_path)
        
        # 根据task_type计算reward
        import traci
        
        if task_type == "signal_step":
            parsed = _parse_signal_step_output(completion_text, debug=True)
            if not parsed:
                print(f"[DEBUG] signal_step 解析失败，原始输出: {completion_text[:300]}")
                simulator.close()
                return float(REWARD_CONFIG['invalid_output_reward'])
            
            next_phase_id = parsed["next_phase_id"]
            green_sec = parsed["green_sec"]
            
            if phase_ids and next_phase_id not in phase_ids:
                print(f"[DEBUG] next_phase_id={next_phase_id} 不在 phase_ids={phase_ids}")
                simulator.close()
                return float(REWARD_CONFIG['invalid_output_reward'])
            
            # 检查 green_sec 范围
            min_green = REWARD_CONFIG['green_sec_min']
            max_green = REWARD_CONFIG['green_sec_max']
            if not (min_green <= green_sec <= max_green):
                print(f"[DEBUG] green_sec={green_sec} 超出范围 [{min_green}, {max_green}]")
                simulator.close()
                return float(REWARD_CONFIG['invalid_output_reward'])
            
            # 应用 tls_phase_durations
            _apply_tls_phase_durations(tl_id, tls_phase_durations)
            
            # 使用 decision_remaining_sec 推进
            decision_rem = decision_remaining_sec if decision_remaining_sec is not None else int(decision_lead_sec)
            for _ in range(int(max(0, decision_rem))):
                traci.simulationStep()
            
            # 模拟phase window
            sim_metrics = _simulate_phase_window(simulator, tl_id, next_phase_id, green_sec)
            
            avg_passed = sim_metrics["avg_passed_veh"]
            avg_queue = sim_metrics["avg_queue_veh"]
            reward = (
                REWARD_CONFIG["alpha_passed"] * avg_passed
                - REWARD_CONFIG["beta_queue"] * avg_queue
            )
            
            simulator.close()
            return float(reward)
        
        elif task_type == "extend_decision":
            parsed = _parse_extend_decision_output(completion_text, debug=True)
            if not parsed:
                print(f"[DEBUG] extend_decision 解析失败，原始输出: {completion_text[:300]}")
                simulator.close()
                return float(REWARD_CONFIG['invalid_output_reward'])
            
            extend = parsed["extend"]
            extend_sec = int(parsed["extend_sec"])
            
            # 应用 tls_phase_durations
            _apply_tls_phase_durations(tl_id, tls_phase_durations)
            
            # 使用传入的 current_elapsed（更稳定）
            if current_elapsed is None:
                # 兜底
                current_phase_idx = traci.trafficlight.getPhase(tl_id)
                planned_green = int(round(traci.trafficlight.getPhaseDuration(tl_id)))
                remaining = traci.trafficlight.getNextSwitch(tl_id) - traci.simulation.getTime()
                current_elapsed = int(max(0, round(planned_green - remaining)))
            else:
                current_elapsed = int(current_elapsed)
            
            current_phase_idx = traci.trafficlight.getPhase(tl_id)
            current_phase_id = current_phase_idx + 1
            
            if not phase_limits:
                simulator.close()
                return float(REWARD_CONFIG['invalid_output_reward'])
            
            limits = phase_limits.get(str(current_phase_id), None) if isinstance(phase_limits, dict) else None
            if not limits:
                simulator.close()
                return float(REWARD_CONFIG['invalid_output_reward'])
            
            min_green = int(limits["min_green"])
            max_green = int(limits["max_green"])
            
            if current_elapsed + int(wait_time) >= max_green:
                if extend_sec != 0:
                    simulator.close()
                    return float(REWARD_CONFIG['invalid_output_reward'])
                extend = "否"
            
            if extend == "否" and extend_sec != 0:
                simulator.close()
                return float(REWARD_CONFIG['invalid_output_reward'])
            
            final_green = current_elapsed + extend_sec
            if not (min_green <= final_green + int(wait_time) <= max_green):
                simulator.close()
                return float(REWARD_CONFIG['invalid_output_reward'])
            
            duration = extend_sec + int(wait_time) if extend == "是" else int(wait_time)
            sim_metrics = _simulate_phase_window(simulator, tl_id, current_phase_id, duration)
            
            avg_passed = sim_metrics["avg_passed_veh"]
            avg_queue = sim_metrics["avg_queue_veh"]
            reward = (
                REWARD_CONFIG["alpha_passed"] * avg_passed
                - REWARD_CONFIG["beta_queue"] * avg_queue
            )
            
            simulator.close()
            return float(reward)
        
        else:
            # 旧任务类型（cycle_predict等）
            simulator.close()
            return float(REWARD_CONFIG['invalid_output_reward'])
    
    except Exception as e:
        print(f"评估失败 [{scenario}/{tl_id}]: {e}")
        try:
            simulator.close()
        except:
            pass
        return float(REWARD_CONFIG['invalid_output_reward'])


# ==================== 主 Reward 函数 ====================
def tsc_reward_fn(
    prompts: Union[List[str], List[List[dict]]],
    completions: Union[List[str], List[List[dict]]],
    completion_ids: List[List[int]],
    **kwargs
) -> List[float]:
    """
    TSC GRPO Reward Function
    
    Args:
        prompts: 批次内的 prompt 列表（字符串或 messages）
        completions: 对应的 completion 列表（字符串）
        completion_ids: completion 的 token id 列表
        **kwargs: Dataset 中的额外字段，必须包含：
            - state_path: List[str] - SUMO state 文件路径
            - scenario: List[str] - 场景名
            - tl_id: List[str] - 信号灯 ID
            - phase_order: List[List[int]] - 相位顺序
            - phase_limits: List[Dict] - 相位约束
    
    Returns:
        List[float]: 每个 completion 的 reward（长度 = len(completions)）
    
    注意：
        - prompts/completions 长度 = batch_size × num_generations
        - 同一 prompt 的 G 个 completion 使用同一个 state_path（连续排列）
    """
    
    # 提取 dataset 字段
    state_paths = kwargs.get('state_path', [])
    scenarios = kwargs.get('scenario', [])
    tl_ids = kwargs.get('tl_id', [])
    phase_orders = kwargs.get('phase_order', [])
    phase_limits_list = kwargs.get('phase_limits', [])
    task_types = kwargs.get('task_type', [])
    phase_ids_list = kwargs.get('phase_ids', [])
    phase_lane_maps = kwargs.get('phase_lane_map', [])
    decision_lead_secs = kwargs.get('decision_lead_sec', [])
    wait_times = kwargs.get('wait_time_for_phase_change', [])
    
    if not state_paths:
        raise ValueError("reward_fn 需要 state_path 字段")
    
    # 将 completions 转为文本（如果是 messages 格式）
    completion_texts = []
    for c in completions:
        if isinstance(c, list) and len(c) > 0 and isinstance(c[-1], dict):
            # messages 格式：取最后一条消息（通常是 assistant 输出）
            completion_texts.append(c[-1].get('content', ''))
        else:
            completion_texts.append(str(c))
    
    # 计算每个 prompt 生成的 completions 数量
    num_generations = len(completion_texts) // len(state_paths) if len(state_paths) > 0 else 1
    
    # ========== 调试输出（前3条completion） ==========
    if not hasattr(tsc_reward_fn, '_debug_printed'):
        tsc_reward_fn._debug_printed = 0
    
    if tsc_reward_fn._debug_printed < 3:
        print(f"\n{'='*70}")
        print(f"[DEBUG] Completion #{tsc_reward_fn._debug_printed + 1}")
        print(f"{'='*70}")
        if completion_texts:
            print(f"原始输出:\n{completion_texts[0][:500]}")
            print(f"{'='*70}\n")
        tsc_reward_fn._debug_printed += 1
    
    # ========== 并行模式 ==========
    if REWARD_CONFIG['parallel_workers'] > 0 and len(completion_texts) > 1:
        # 准备并行任务参数
        tasks = []
        for i in range(len(completion_texts)):
            sample_idx = i // num_generations
            
            state_path = state_paths[sample_idx]
            scenario = scenarios[sample_idx]
            tl_id = tl_ids[sample_idx]
            completion_text = completion_texts[i]
            
            task_type = task_types[sample_idx] if task_types else None
            phase_ids = phase_ids_list[sample_idx] if phase_ids_list else None
            decision_lead_sec = decision_lead_secs[sample_idx] if decision_lead_secs else 10
            wait_time = wait_times[sample_idx] if wait_times else 0
            
            # 提取新增字段
            sumocfg_paths = kwargs.get('sumocfg_path', [])
            decision_remaining_secs = kwargs.get('decision_remaining_sec', [])
            elapsed_list = kwargs.get('current_phase_elapsed_sec', [])
            tls_durs_list = kwargs.get('tls_phase_durations', [])
            
            # 优先使用 dataset 的 sumocfg_path，否则兜底查找
            if sumocfg_paths and sample_idx < len(sumocfg_paths):
                sumocfg = sumocfg_paths[sample_idx]
            else:
                scenario_dir = os.path.join('sumo_simulation/environments', scenario)
                sumocfg = None
                for f in os.listdir(scenario_dir):
                    if f.endswith('.sumocfg'):
                        sumocfg = os.path.join(scenario_dir, f)
                        break
            
            if not sumocfg:
                tasks.append(None)  # 标记为无效任务
                continue
            
            # phase_order和phase_limits只在某些任务类型中需要
            phase_order = None
            phase_limits = None
            current_elapsed = None
            decision_remaining_sec = None
            tls_phase_durations = []
            
            if task_type == "signal_step":
                if decision_remaining_secs and sample_idx < len(decision_remaining_secs):
                    decision_remaining_sec = decision_remaining_secs[sample_idx]
                if tls_durs_list and sample_idx < len(tls_durs_list):
                    tls_phase_durations = tls_durs_list[sample_idx]
            elif task_type == "extend_decision":
                if phase_orders and sample_idx < len(phase_orders):
                    phase_order = phase_orders[sample_idx]
                if phase_limits_list and sample_idx < len(phase_limits_list):
                    phase_limits = phase_limits_list[sample_idx]
                if elapsed_list and sample_idx < len(elapsed_list):
                    current_elapsed = elapsed_list[sample_idx]
                if tls_durs_list and sample_idx < len(tls_durs_list):
                    tls_phase_durations = tls_durs_list[sample_idx]
            
            tasks.append((
                completion_text, state_path, scenario, tl_id, sumocfg,
                task_type, phase_ids, decision_lead_sec, decision_remaining_sec,
                wait_time, phase_order, phase_limits, current_elapsed,
                tls_phase_durations
            ))
        
        # 使用进程池并行计算
        num_workers = min(REWARD_CONFIG['parallel_workers'], len(completion_texts))
        with Pool(processes=num_workers) as pool:
            rewards = []
            for i, task in enumerate(tasks):
                if task is None:
                    rewards.append(float(REWARD_CONFIG['invalid_output_reward']))
                else:
                    # 并行执行
                    result = pool.apply_async(_evaluate_single_completion, (task,))
                    rewards.append(result)
            
            # 等待所有任务完成并获取结果
            final_rewards = []
            for r in rewards:
                if isinstance(r, float):
                    final_rewards.append(r)
                else:
                    try:
                        final_rewards.append(r.get(timeout=120))  # 最多等待2分钟
                    except Exception as e:
                        print(f"并行任务超时或失败: {e}")
                        final_rewards.append(float(REWARD_CONFIG['invalid_output_reward']))
        
        return final_rewards
    
    # ========== 顺序模式（原有逻辑） ==========
    rewards: List[float] = []
    
    # 按样本逐个评估（每个样本对应一个 state_path）
    for i in range(len(completion_texts)):
        # 计算原始样本索引（同一 prompt 的多个 completions 共享相同的 dataset 字段）
        sample_idx = i // num_generations
        
        state_path = state_paths[sample_idx]
        scenario = scenarios[sample_idx]
        tl_id = tl_ids[sample_idx]
        completion_text = completion_texts[i]

        task_type = task_types[sample_idx] if task_types else None
        phase_ids = phase_ids_list[sample_idx] if phase_ids_list else None
        decision_lead_sec = decision_lead_secs[sample_idx] if decision_lead_secs else 10
        wait_time = wait_times[sample_idx] if wait_times else 0
        
        # phase_order 和 phase_limits 只在某些任务类型中存在，延迟访问
        phase_order = None
        phase_limits = None
        
        # 优先使用 dataset 的 sumocfg_path，否则兜底查找
        sumocfg_paths = kwargs.get('sumocfg_path', [])
        if sumocfg_paths and sample_idx < len(sumocfg_paths):
            sumocfg = sumocfg_paths[sample_idx]
        else:
            # 兜底：从 state_path 推断
            scenario_dir = os.path.join('sumo_simulation/environments', scenario)
            sumocfg = None
            for f in os.listdir(scenario_dir):
                if f.endswith('.sumocfg'):
                    sumocfg = os.path.join(scenario_dir, f)
                    break
        
        if not sumocfg:
            print(f"警告: 找不到 sumocfg for {scenario}, 返回负奖励")
            rewards.append(-2.0)
            continue
        
        try:
            # 获取 simulator（复用或创建）
            simulator = _GLOBAL_POOL.get_simulator(scenario, sumocfg)
            scaler = _GLOBAL_POOL.get_scaler(tl_id)
            
            # 恢复 SUMO state
            if not os.path.exists(state_path):
                print(f"警告: state 文件不存在: {state_path}")
                rewards.append(float(REWARD_CONFIG['invalid_output_reward']))
                continue
            
            simulator.restore_simulation_state(state_path)

            if task_type in ("signal_step", "extend_decision"):
                import traci

                if task_type == "signal_step":
                    parsed = _parse_signal_step_output(completion_text, debug=True)
                    if not parsed:
                        print(f"[DEBUG 顺序] signal_step 解析失败，原始输出: {completion_text[:300]}")
                        rewards.append(float(REWARD_CONFIG['invalid_output_reward']))
                        continue
                    next_phase_id = parsed["next_phase_id"]
                    green_sec = parsed["green_sec"]
                    
                    # 检查 phase_id 有效性
                    if phase_ids and next_phase_id not in phase_ids:
                        print(f"[DEBUG 顺序] next_phase_id={next_phase_id} 不在 phase_ids={phase_ids}")
                        rewards.append(float(REWARD_CONFIG['invalid_output_reward']))
                        continue
                    
                    # 检查 green_sec 范围
                    min_green = REWARD_CONFIG['green_sec_min']
                    max_green = REWARD_CONFIG['green_sec_max']
                    if not (min_green <= green_sec <= max_green):
                        print(f"[DEBUG 顺序] green_sec={green_sec} 超出范围 [{min_green}, {max_green}]")
                        rewards.append(float(REWARD_CONFIG['invalid_output_reward']))
                        continue
                    
                    # 应用保存的 tls_phase_durations（复现随机配时）
                    tls_phase_durations_list = kwargs.get('tls_phase_durations', [])
                    if tls_phase_durations_list and sample_idx < len(tls_phase_durations_list):
                        tls_durs = tls_phase_durations_list[sample_idx]
                        _apply_tls_phase_durations(tl_id, tls_durs)
                    
                    # 使用 dataset 的 decision_remaining_sec 推进到相位切换点
                    decision_remaining_secs = kwargs.get('decision_remaining_sec', [])
                    decision_rem = decision_remaining_secs[sample_idx] if decision_remaining_secs and sample_idx < len(decision_remaining_secs) else int(decision_lead_sec)
                    for _ in range(int(max(0, decision_rem))):
                        traci.simulationStep()

                    sim_metrics = _simulate_phase_window(
                        simulator,
                        tl_id,
                        next_phase_id,
                        green_sec,
                    )

                    avg_passed = sim_metrics["avg_passed_veh"]
                    avg_queue = sim_metrics["avg_queue_veh"]
                    reward = (
                        REWARD_CONFIG["alpha_passed"] * avg_passed
                        - REWARD_CONFIG["beta_queue"] * avg_queue
                    )
                    rewards.append(float(reward))
                    continue

                if task_type == "extend_decision":
                    parsed = _parse_extend_decision_output(completion_text, debug=True)
                    if not parsed:
                        print(f"[DEBUG 顺序] extend_decision 解析失败，原始输出: {completion_text[:300]}")
                        rewards.append(float(REWARD_CONFIG['invalid_output_reward']))
                        continue
                    extend = parsed["extend"]
                    extend_sec = int(parsed["extend_sec"])
                    
                    # 应用保存的 tls_phase_durations（复现随机配时）
                    tls_phase_durations_list = kwargs.get('tls_phase_durations', [])
                    if tls_phase_durations_list and sample_idx < len(tls_phase_durations_list):
                        tls_durs = tls_phase_durations_list[sample_idx]
                        _apply_tls_phase_durations(tl_id, tls_durs)

                    # 使用 dataset 的 current_phase_elapsed_sec（更稳定）
                    elapsed_list = kwargs.get('current_phase_elapsed_sec', [])
                    if elapsed_list and sample_idx < len(elapsed_list):
                        current_elapsed = int(elapsed_list[sample_idx])
                    else:
                        # 兜底：从traci推导（不推荐）
                        current_phase_idx = traci.trafficlight.getPhase(tl_id)
                        planned_green = int(round(traci.trafficlight.getPhaseDuration(tl_id)))
                        remaining = traci.trafficlight.getNextSwitch(tl_id) - traci.simulation.getTime()
                        current_elapsed = int(max(0, round(planned_green - remaining)))
                    
                    current_phase_idx = traci.trafficlight.getPhase(tl_id)
                    current_phase_id = current_phase_idx + 1

                    # extend_decision 任务需要 phase_limits
                    if phase_limits_list and sample_idx < len(phase_limits_list):
                        phase_limits = phase_limits_list[sample_idx]
                    else:
                        rewards.append(float(REWARD_CONFIG['invalid_output_reward']))
                        continue
                    
                    limits = phase_limits.get(str(current_phase_id), None) if isinstance(phase_limits, dict) else None
                    if not limits:
                        rewards.append(float(REWARD_CONFIG['invalid_output_reward']))
                        continue
                    min_green = int(limits["min_green"])
                    max_green = int(limits["max_green"])

                    if current_elapsed + int(wait_time) >= max_green:
                        if extend_sec != 0:
                            rewards.append(float(REWARD_CONFIG['invalid_output_reward']))
                            continue
                        extend = "否"

                    if extend == "否" and extend_sec != 0:
                        rewards.append(float(REWARD_CONFIG['invalid_output_reward']))
                        continue

                    final_green = current_elapsed + extend_sec
                    if not (min_green <= final_green + int(wait_time) <= max_green):
                        rewards.append(float(REWARD_CONFIG['invalid_output_reward']))
                        continue

                    duration = extend_sec + int(wait_time) if extend == "是" else int(wait_time)
                    sim_metrics = _simulate_phase_window(
                        simulator,
                        tl_id,
                        current_phase_id,
                        duration,
                    )
                    avg_passed = sim_metrics["avg_passed_veh"]
                    avg_queue = sim_metrics["avg_queue_veh"]
                    reward = (
                        REWARD_CONFIG["alpha_passed"] * avg_passed
                        - REWARD_CONFIG["beta_queue"] * avg_queue
                    )
                    rewards.append(float(reward))
                    continue

            # ===== 旧任务: cycle_predict =====
            # cycle_predict 任务需要 phase_order 和 phase_limits
            if phase_orders and sample_idx < len(phase_orders):
                phase_order = phase_orders[sample_idx]
            else:
                rewards.append(float(REWARD_CONFIG['invalid_output_reward']))
                continue
            
            if phase_limits_list and sample_idx < len(phase_limits_list):
                phase_limits = phase_limits_list[sample_idx]
            else:
                rewards.append(float(REWARD_CONFIG['invalid_output_reward']))
                continue
            
            constraint_score, info, plan = score_constraints_and_format(
                completion_text=completion_text,
                phase_order=phase_order,
                phase_limits=phase_limits,
                D0=REWARD_CONFIG['D0'],
            )

            if plan is None:
                reward = compute_total_reward(
                    constraint_score=constraint_score,
                    sim_reward=0.0,
                    w_sim=REWARD_CONFIG['w_sim'],
                    w_constraint=REWARD_CONFIG['w_constraint'],
                )
                rewards.append(float(reward))
                continue

            sim_result = evaluate_plan_once_reward_fn(simulator, tl_id, plan)

            scaler.add_observation(
                passed=sim_result['passed_vehicles'],
                queue=sim_result['queue_vehicles'],
                proxy=sim_result['total_queue_proxy'],
            )

            sim_reward, _sim_info = compute_sim_reward_adaptive(
                result=sim_result,
                scaler=scaler,
                baseline_result=None,
                w_passed=REWARD_CONFIG['w_passed'],
                w_queue=REWARD_CONFIG['w_queue'],
                w_proxy=REWARD_CONFIG['w_proxy'],
            )

            total_reward = compute_total_reward(
                constraint_score=constraint_score,
                sim_reward=sim_reward,
                w_sim=REWARD_CONFIG['w_sim'],
                w_constraint=REWARD_CONFIG['w_constraint'],
            )

            rewards.append(float(total_reward))
            
        except Exception as e:
            print(f"评估失败 [{scenario}/{tl_id}]: {e}")
            import traceback
            traceback.print_exc()
            rewards.append(float(REWARD_CONFIG['invalid_output_reward']))
    
    return rewards


def cleanup_global_pool():
    """清理全局 simulator 池（训练结束时调用）"""
    _GLOBAL_POOL.close_all()


# ==================== 测试代码 ====================
if __name__ == '__main__':
    # 简单测试
    print("Reward function 模块加载成功")
    print(f"配置: {REWARD_CONFIG}")
