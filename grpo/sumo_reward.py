# -*- coding: utf-8 -*-
"""
SUMO Reward计算模块

提供基于SUMO仿真的TSC reward计算功能，包括：
- 单样本reward计算
- 批量reward计算
- 并行reward计算
"""

import os
import json
import math
import random
import re
from typing import List, Optional, Any, Dict, Tuple
from dataclasses import dataclass
from types import SimpleNamespace

from .sumo_interface import SUMOInterface, find_available_port


@dataclass
class TSCResult:
    """TSC reward计算结果"""
    reward: float
    queue_before: int
    queue_after: int
    delta: int
    success: bool
    error: Optional[str] = None


def parse_prompt_for_decision_info(prompt: str) -> dict:
    """
    从prompt中提取决策所需信息

    Args:
        prompt: 输入JSON字符串

    Returns:
        包含tl_id_hash, current_phase_id, phase_order的字典
    """
    data = json.loads(prompt)
    return {
        "tl_id_hash": data.get("crossing_id"),
        "current_phase_id": data["state"]["current_phase_id"],
        "phase_order": data["phase_order"],
    }


def extract_decision_from_output(output: str) -> Optional[str]:
    """
    从模型输出中提取决策

    Args:
        output: 模型输出字符串

    Returns:
        "yes", "no", or None
    """
    pattern = r'\{["\s]*extend["\s]*:\s*["\s]*(yes|no)["\s]*\}'
    match = re.search(pattern, output.lower())
    return match.group(1) if match else None


def normalize_reward(delta: int, scale: float = 10.0) -> float:
    """
    将排队数变化归一化到[-1, 1]

    使用tanh函数: tanh(-delta / scale)

    Args:
        delta: 排队数变化量（queue_after - queue_before）
        scale: 归一化scale参数

    Returns:
        归一化后的reward值，范围[-1, 1]
    """
    return math.tanh(-delta / scale)


def calculate_tsc_reward_single(
    state_file: str,
    prompt: str,
    decision: str,
    config: Any
) -> TSCResult:
    """
    计算单个样本的TSC reward

    Args:
        state_file: SUMO状态文件路径
        prompt: 输入prompt（JSON格式）
        decision: 模型决策 ("yes" 或 "no")
        config: 配置对象（需包含sumocfg_path, extend_seconds等）

    Returns:
        TSCResult对象
    """
    try:
        # 解析prompt获取决策所需信息
        info = parse_prompt_for_decision_info(prompt)
        tl_id_hash = info["tl_id_hash"]
        current_phase_id = info["current_phase_id"]
        phase_order = info["phase_order"]

        # 获取配置参数
        extend_seconds = getattr(config, 'extend_seconds', 5)
        sumocfg_path = getattr(config, 'sumocfg_path', None)

        if not sumocfg_path:
            # 尝试从state_file路径推断sumocfg
            state_dir = os.path.dirname(state_file)
            # state文件在states/子目录中，sumocfg在上一级
            scenario_dir = os.path.dirname(state_dir)
            sumocfg_path = find_sumocfg(scenario_dir)

            if not sumocfg_path:
                return TSCResult(
                    reward=0.0,
                    queue_before=0,
                    queue_after=0,
                    delta=0,
                    success=False,
                    error="Cannot find sumocfg file"
                )

        # 创建SUMO接口实例
        sumo = SUMOInterface(
            config_file=sumocfg_path,
            port=None,  # 使用随机端口
            gui=False,
            verbose=False
        )

        # 从状态文件恢复仿真
        if not sumo.start_from_state(state_file):
            return TSCResult(
                reward=0.0,
                queue_before=0,
                queue_after=0,
                delta=0,
                success=False,
                error="Failed to start SUMO from state file"
            )

        # 记录初始排队数
        # 需要找到实际的tl_id（从hash反查或使用默认）
        tl_ids = sumo.get_traffic_lights()
        if not tl_ids:
            sumo.close()
            return TSCResult(
                reward=0.0,
                queue_before=0,
                queue_after=0,
                delta=0,
                success=False,
                error="No traffic lights found"
            )

        # 使用第一个信号灯（简化处理）
        tl_id = tl_ids[0]
        queue_before = sumo.get_total_queue_count(tl_id)

        # 根据决策执行操作
        if decision.lower() == "yes":
            # 延长当前绿灯相位
            sumo.extend_phase(tl_id, extend_seconds)
        else:
            # 切换到下一个相位
            current_idx = phase_order.index(current_phase_id)
            next_idx = (current_idx + 1) % len(phase_order)
            next_phase_id = phase_order[next_idx]
            sumo.set_phase(tl_id, next_phase_id)

        # 推进仿真
        for _ in range(extend_seconds):
            if not sumo.step():
                break

        # 记录结束排队数
        queue_after = sumo.get_total_queue_count(tl_id)

        # 关闭SUMO
        sumo.close()

        # 计算变化和reward
        delta = queue_after - queue_before
        # 从配置中读取reward_scale，而不是硬编码
        reward_scale = getattr(config, 'reward_scale', 10.0)
        reward = normalize_reward(delta, scale=reward_scale)

        return TSCResult(
            reward=reward,
            queue_before=queue_before,
            queue_after=queue_after,
            delta=delta,
            success=True
        )

    except Exception as e:
        return TSCResult(
            reward=0.0,
            queue_before=0,
            queue_after=0,
            delta=0,
            success=False,
            error=str(e)
        )


def find_sumocfg(scenario_dir: str) -> Optional[str]:
    """
    查找场景目录下的.sumocfg文件

    Args:
        scenario_dir: 场景目录路径

    Returns:
        sumocfg文件路径，未找到返回None
    """
    if not os.path.isdir(scenario_dir):
        return None

    for f in os.listdir(scenario_dir):
        if f.endswith('.sumocfg'):
            return os.path.join(scenario_dir, f)
    return None


def calculate_tsc_reward_worker(
    prompt: str,
    output: str,
    state_file: str,
    config_dict: dict
) -> TSCResult:
    """
    Worker函数，在单独进程中执行

    Args:
        prompt: 输入prompt
        output: 模型输出
        state_file: 状态文件路径
        config_dict: 配置字典

    Returns:
        TSCResult对象
    """
    # 重建配置对象
    config = SimpleNamespace(**config_dict)
    decision = extract_decision_from_output(output)
    if decision is None:
        return TSCResult(
            reward=0.0,
            queue_before=0,
            queue_after=0,
            delta=0,
            success=False,
            error="Cannot extract decision from output"
        )
    return calculate_tsc_reward_single(state_file, prompt, decision, config)


def tsc_reward_fn(
    prompts: List[str],
    outputs: List[str],
    state_files: List[str],
    config: Any
) -> List[float]:
    """
    批量计算TSC reward（单样本版本）

    Args:
        prompts: 输入prompt列表
        outputs: 模型输出列表
        state_files: 状态文件路径列表
        config: 配置对象

    Returns:
        reward列表
    """
    rewards = []

    for prompt, output, state_file in zip(prompts, outputs, state_files):
        # 提取决策
        decision = extract_decision_from_output(output)
        if decision is None:
            # 无法提取决策，返回0
            rewards.append(0.0)
            continue

        # 计算reward
        result = calculate_tsc_reward_single(state_file, prompt, decision, config)
        if result.success:
            rewards.append(result.reward)
        else:
            # SUMO计算失败，返回0并记录错误
            print(f"TSC reward计算失败: {result.error}")
            rewards.append(0.0)

    return rewards


def calculate_relative_baseline_reward(
    state_file: str,
    prompt: str,
    model_decision: str,
    config: Any,
    mp_config: Any = None
) -> Tuple[float, Dict[str, Any]]:
    """
    计算相对baseline的reward

    同时运行模型决策和baseline决策的SUMO仿真，
    返回相对优势作为reward

    Args:
        state_file: SUMO状态文件路径
        prompt: 输入prompt（JSON格式）
        model_decision: 模型决策 ("yes" 或 "no")
        config: 配置对象（需包含sumocfg_path, extend_seconds等）
        mp_config: Max Pressure配置对象（可选）

    Returns:
        (relative_reward, info_dict)
    """
    from .max_pressure import MaxPressureConfig, max_pressure_decision_from_prompt

    if mp_config is None:
        mp_config = MaxPressureConfig()

    # 1. 计算baseline决策
    prompt_data = json.loads(prompt)
    green_elapsed = prompt_data.get("current_green_elapsed", 0)
    min_green = prompt_data.get("min_green", 10.0)
    max_green = prompt_data.get("max_green", 60.0)

    baseline_decision = max_pressure_decision_from_prompt(
        prompt=prompt,
        green_elapsed=green_elapsed,
        min_green=min_green,
        max_green=max_green,
        config=mp_config
    )

    # 2. 运行模型决策的SUMO仿真
    model_result = calculate_tsc_reward_single(
        state_file=state_file,
        prompt=prompt,
        decision=model_decision,
        config=config
    )

    if not model_result.success:
        return 0.0, {"error": "model_simulation_failed"}

    # 3. 运行baseline决策的SUMO仿真
    baseline_result = calculate_tsc_reward_single(
        state_file=state_file,
        prompt=prompt,
        decision=baseline_decision,
        config=config
    )

    if not baseline_result.success:
        # baseline仿真失败，返回模型绝对reward
        return model_result.reward, {
            "model_reward": model_result.reward,
            "baseline_reward": None,
            "relative_reward": None,
            "baseline_simulation_failed": True
        }

    # 4. 计算相对优势
    # relative_delta = baseline_delta - model_delta
    # 如果模型让队列减少更多（model_delta更负），relative_delta为正
    # 此时应该给予正reward
    relative_delta = baseline_result.delta - model_result.delta
    reward_scale = getattr(config, 'reward_scale', 10.0)
    # 注意：这里直接用 tanh(relative_delta/scale)，不加负号
    # 因为 relative_delta 正 = 模型比baseline好 = 应获得正reward
    import math
    relative_reward = math.tanh(relative_delta / reward_scale)

    # 调试输出
    print(f"[RELATIVE DEBUG] model={model_decision}, baseline={baseline_decision}")
    print(f"[RELATIVE DEBUG] model_delta={model_result.delta}, baseline_delta={baseline_result.delta}")
    print(f"[RELATIVE DEBUG] relative_delta={relative_delta}, relative_reward={relative_reward}")

    return relative_reward, {
        "model_reward": model_result.reward,
        "baseline_reward": baseline_result.reward,
        "relative_reward": relative_reward,
        "model_decision": model_decision,
        "baseline_decision": baseline_decision,
        "model_delta": model_result.delta,
        "baseline_delta": baseline_result.delta,
        "relative_delta": relative_delta
    }


def _relative_baseline_worker(
    prompt: str,
    output: str,
    state_file: str,
    config_dict: dict,
    mp_config_dict: dict
) -> Tuple[float, Dict[str, Any]]:
    """
    模块级别的worker函数，用于多进程池

    这个函数必须在模块级别定义才能被pickle序列化。

    Args:
        prompt: 输入prompt
        output: 模型输出
        state_file: 状态文件路径
        config_dict: 配置字典
        mp_config_dict: Max Pressure配置字典

    Returns:
        (relative_reward, info_dict)
    """
    from .max_pressure import MaxPressureConfig

    decision = extract_decision_from_output(output)
    if decision is None:
        return 0.0, {"error": "cannot_extract_decision"}

    return calculate_relative_baseline_reward(
        state_file=state_file,
        prompt=prompt,
        model_decision=decision,
        config=SimpleNamespace(**config_dict),
        mp_config=MaxPressureConfig(**mp_config_dict)
    )


class ParallelSUMORewardCalculator:
    """
    并行SUMO reward计算器

    使用多进程并行计算多个样本的TSC reward
    """

    def __init__(self, max_workers: int = 4):
        """
        初始化并行计算器

        Args:
            max_workers: 最大并行进程数
        """
        self.max_workers = max_workers

    def calculate_batch(
        self,
        prompts: List[str],
        outputs: List[str],
        state_files: List[str],
        config: Any
    ) -> List[float]:
        """
        批量计算TSC reward

        Args:
            prompts: 输入prompt列表
            outputs: 模型输出列表
            state_files: 状态文件路径列表
            config: 配置对象

        Returns:
            reward列表

        Raises:
            RuntimeError: 任何SUMO进程失败时抛出
        """
        from multiprocessing import Pool

        # 准备参数
        tasks = list(zip(prompts, outputs, state_files))
        config_dict = self._config_to_dict(config)

        # 使用进程池并行计算
        with Pool(processes=self.max_workers) as pool:
            results = pool.starmap(
                calculate_tsc_reward_worker,
                [(p, o, s, config_dict) for p, o, s in tasks]
            )

        # 检查结果
        rewards = []
        for result in results:
            if not result.success:
                raise RuntimeError(
                    f"SUMO reward calculation failed: {result.error}"
                )
            rewards.append(result.reward)

        return rewards

    def calculate_batch_relative_baseline(
        self,
        prompts: List[str],
        outputs: List[str],
        state_files: List[str],
        config: Any,
        mp_config: Any = None
    ) -> Tuple[List[float], List[Dict]]:
        """
        批量计算相对baseline的reward

        Args:
            prompts: 输入prompt列表
            outputs: 模型输出列表
            state_files: 状态文件路径列表
            config: 配置对象
            mp_config: Max Pressure配置对象（可选）

        Returns:
            (rewards列表, 详细信息列表)
        """
        from multiprocessing import Pool

        if mp_config is None:
            from .max_pressure import MaxPressureConfig
            mp_config = MaxPressureConfig()

        config_dict = self._config_to_dict(config)
        mp_config_dict = mp_config.__dict__

        # 构建任务列表：(prompt, output, state_file, config_dict, mp_config_dict)
        tasks = [
            (prompt, output, state_file, config_dict, mp_config_dict)
            for prompt, output, state_file in zip(prompts, outputs, state_files)
        ]

        # 使用模块级别的worker函数（可以被pickle）
        with Pool(processes=self.max_workers) as pool:
            results = pool.starmap(_relative_baseline_worker, tasks)

        rewards = [r[0] for r in results]
        infos = [r[1] for r in results]

        return rewards, infos

    @staticmethod
    def _config_to_dict(config: Any) -> dict:
        """
        将配置对象转换为字典

        Args:
            config: 配置对象

        Returns:
            配置字典
        """
        if hasattr(config, '__dict__'):
            return config.__dict__
        return config
