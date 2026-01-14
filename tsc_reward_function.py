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
    
    if not state_paths:
        raise ValueError("reward_fn 需要 state_path 字段")
    
    # 将 completions 转为文本（如果是 messages 格式）
    completion_texts = []
    for c in completions:
        if isinstance(c, list) and len(c) > 0 and isinstance(c[0], dict):
            # messages 格式：[{"role": "assistant", "content": "..."}]
            completion_texts.append(c[0].get('content', ''))
        else:
            completion_texts.append(str(c))
    
    rewards = []
    
    # 按样本逐个评估（每个样本对应一个 state_path）
    for i in range(len(completion_texts)):
        state_path = state_paths[i]
        scenario = scenarios[i]
        tl_id = tl_ids[i]
        phase_order = phase_orders[i]
        phase_limits = phase_limits_list[i]
        completion_text = completion_texts[i]
        
        # 查找对应的 sumocfg（从 state_path 推断）
        # state_path 格式: grpo_states/<scenario>/<tl_id>_step<i>_t<time>.xml
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
                rewards.append(-2.0)
                continue
            
            simulator.restore_simulation_state(state_path)
            
            # 解析 completion 并检查约束
            constraint_score, info, plan = score_constraints_and_format(
                completion_text=completion_text,
                phase_order=phase_order,
                phase_limits=phase_limits,
                D0=REWARD_CONFIG['D0'],
            )
            
            # 如果解析失败或硬约束违反，返回强负分
            if plan is None:
                reward = compute_total_reward(
                    constraint_score=constraint_score,
                    sim_reward=0.0,
                    w_sim=REWARD_CONFIG['w_sim'],
                    w_constraint=REWARD_CONFIG['w_constraint'],
                )
                rewards.append(float(reward))
                continue
            
            # 仿真评估
            sim_result = evaluate_plan_once_reward_fn(simulator, tl_id, plan)
            
            # 更新 scaler
            scaler.add_observation(
                passed=sim_result['passed_vehicles'],
                queue=sim_result['queue_vehicles'],
                proxy=sim_result['total_queue_proxy'],
            )
            
            # 计算仿真 reward
            sim_reward, _sim_info = compute_sim_reward_adaptive(
                result=sim_result,
                scaler=scaler,
                baseline_result=None,
                w_passed=REWARD_CONFIG['w_passed'],
                w_queue=REWARD_CONFIG['w_queue'],
                w_proxy=REWARD_CONFIG['w_proxy'],
            )
            
            # 总 reward
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
            rewards.append(-2.0)
    
    return rewards


def cleanup_global_pool():
    """清理全局 simulator 池（训练结束时调用）"""
    _GLOBAL_POOL.close_all()


# ==================== 测试代码 ====================
if __name__ == '__main__':
    # 简单测试
    print("Reward function 模块加载成功")
    print(f"配置: {REWARD_CONFIG}")
