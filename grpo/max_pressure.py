# -*- coding: utf-8 -*-
"""
Max Pressure算法模块

提供Max Pressure baseline算法实现，用于交通信号控制。
Max Pressure是交通信号控制领域的经典算法，根据各相位的排队车辆数
判断是否延长当前绿灯相位。

该算法将作为GRPO训练中reward计算的baseline参考。
"""

from dataclasses import dataclass
from typing import Dict, List

from .sumo_reward import parse_prompt_for_decision_info


@dataclass
class MaxPressureConfig:
    """Max Pressure算法配置"""

    # 最小绿时间偏移（秒），用于安全边界
    min_green_offset: float = 0.0

    # 是否允许覆盖最大绿时间（默认False，严格遵守最大绿时间）
    max_green_override: bool = False

    # 压力差阈值（默认0，当前相位>=其他相位时延长）
    # 设置为正值时，只有当前相位明显大于其他相位时才延长
    pressure_threshold: float = 0.0


def compute_phase_pressure(phase_queues: Dict[int, float]) -> Dict[int, float]:
    """
    计算各相位的压力值

    使用标准Max Pressure公式的简化版：
    pressure = queue_count（只考虑上游排队）

    注：完整的Max Pressure公式是 upstream - downstream，
    但当前数据结构中只有 avg_queue_veh（上游排队），所以简化为压力=排队数

    Args:
        phase_queues: 相位ID到排队长度的映射

    Returns:
        相位ID到压力值的映射

    Examples:
        >>> queues = {0: 10.0, 1: 5.0, 2: 3.0}
        >>> pressures = compute_phase_pressure(queues)
        >>> assert pressures[0] == 10.0
    """
    # 简化版：压力值等于排队数
    # 如果将来有下游数据，可以改为: pressure = upstream - downstream
    return {phase_id: queue_count for phase_id, queue_count in phase_queues.items()}


def max_pressure_decision(
    current_phase_id: int,
    phase_queues: Dict[int, float],
    green_elapsed: float,
    min_green: float,
    max_green: float,
    config: MaxPressureConfig
) -> str:
    """
    Max Pressure核心决策函数

    根据当前相位和其他相位的排队情况，判断是否延长当前绿灯相位。

    决策逻辑：
    1. 时间约束检查：
       - 如果 green_elapsed < min_green: 必须返回 'yes'（不能提前切换）
       - 如果 green_elapsed >= max_green: 必须返回 'no'（不能超时延长）

    2. Max Pressure决策：
       - 计算当前相位的压力：current_pressure = phase_queues[current_phase_id]
       - 找出其他相位的最大压力：max_other_pressure
       - 如果 current_pressure >= max_other_pressure + pressure_threshold: 返回 'yes'
       - 否则返回 'no'

    Args:
        current_phase_id: 当前相位ID
        phase_queues: 各相位排队数（键为phase_id）
        green_elapsed: 当前绿灯已持续时间（秒）
        min_green: 最小绿灯时间（秒）
        max_green: 最大绿灯时间（秒）
        config: MaxPressureConfig配置对象

    Returns:
        'yes' 或 'no'（小写字符串）

    Raises:
        ValueError: 当前相位不存在于phase_queues中时

    Examples:
        >>> config = MaxPressureConfig()
        >>> queues = {0: 10.0, 1: 5.0, 2: 3.0}
        >>>
        >>> # 测试时间约束（小于最小绿必须延长）
        >>> decision = max_pressure_decision(0, queues, 5, 10, 60, config)
        >>> assert decision == 'yes'
        >>>
        >>> # 测试时间约束（超过最大绿必须切换）
        >>> decision = max_pressure_decision(0, queues, 60, 10, 60, config)
        >>> assert decision == 'no'
        >>>
        >>> # 测试Max Pressure决策（当前相位排队最大）
        >>> decision = max_pressure_decision(0, queues, 15, 10, 60, config)
        >>> assert decision == 'yes'
        >>>
        >>> # 测试Max Pressure决策（其他相位排队更大）
        >>> queues = {0: 5.0, 1: 10.0, 2: 3.0}
        >>> decision = max_pressure_decision(0, queues, 15, 10, 60, config)
        >>> assert decision == 'no'
    """
    # 验证当前相位存在
    if current_phase_id not in phase_queues:
        raise ValueError(
            f"当前相位ID {current_phase_id} 不存在于 phase_queues 中。"
            f"可用的相位: {list(phase_queues.keys())}"
        )

    # 调整最小绿时间（应用偏移）
    effective_min_green = min_green + config.min_green_offset

    # 时间约束检查：小于最小绿时间，必须延长
    if green_elapsed < effective_min_green:
        return 'yes'

    # 时间约束检查：超过最大绿时间，必须切换
    if green_elapsed >= max_green:
        # 除非配置允许覆盖最大绿时间
        if not config.max_green_override:
            return 'no'

    # 计算当前相位的压力
    current_pressure = phase_queues[current_phase_id]

    # 找出其他相位的最大压力
    other_phases = {
        pid: queue for pid, queue in phase_queues.items()
        if pid != current_phase_id
    }

    if not other_phases:
        # 只有一个相位，延长它
        return 'yes'

    max_other_pressure = max(other_phases.values())

    # Max Pressure决策：当前相位压力 >= 其他相位最大压力 + 阈值
    if current_pressure >= max_other_pressure + config.pressure_threshold:
        return 'yes'
    else:
        return 'no'


def max_pressure_decision_from_prompt(
    prompt: str,
    green_elapsed: float,
    min_green: float,
    max_green: float,
    config: MaxPressureConfig
) -> str:
    """
    从prompt JSON中提取信息并进行Max Pressure决策

    便捷函数，用于直接在reward计算中获取baseline决策。

    Args:
        prompt: 输入prompt JSON字符串
        green_elapsed: 当前绿灯已持续时间（秒）
        min_green: 最小绿灯时间（秒）
        max_green: 最大绿灯时间（秒）
        config: MaxPressureConfig配置对象

    Returns:
        'yes' 或 'no'（小写字符串）

    Raises:
        ValueError: prompt格式错误或缺少必要字段时
        KeyError: prompt中缺少必要字段时

    Examples:
        >>> import json
        >>> config = MaxPressureConfig()
        >>> prompt_data = {
        ...     "state": {
        ...         "current_phase_id": 0,
        ...         "phase_metrics_by_id": {
        ...             0: {"avg_queue_veh": 10.0},
        ...             1: {"avg_queue_veh": 5.0},
        ...             2: {"avg_queue_veh": 3.0}
        ...         }
        ...     }
        ... }
        >>> prompt = json.dumps(prompt_data)
        >>> decision = max_pressure_decision_from_prompt(
        ...     prompt, 15, 10, 60, config
        ... )
        >>> assert decision == 'yes'
    """
    import json

    # 解析prompt
    data = json.loads(prompt)

    # 提取当前相位ID
    current_phase_id = data["state"]["current_phase_id"]

    # 提取各相位排队数
    phase_metrics = data["state"]["phase_metrics_by_id"]
    phase_queues = {
        phase_id: metrics["avg_queue_veh"]
        for phase_id, metrics in phase_metrics.items()
    }

    # 调用核心决策函数
    return max_pressure_decision(
        current_phase_id=current_phase_id,
        phase_queues=phase_queues,
        green_elapsed=green_elapsed,
        min_green=min_green,
        max_green=max_green,
        config=config
    )


def batch_max_pressure_decision(
    prompts: List[str],
    green_elapsed_list: List[float],
    min_green_list: List[float],
    max_green_list: List[float],
    config: MaxPressureConfig
) -> List[str]:
    """
    批量Max Pressure决策

    对多个prompt进行批量决策，用于reward计算中获取baseline决策。

    Args:
        prompts: 输入prompt JSON字符串列表
        green_elapsed_list: 各样本的绿灯已持续时间列表
        min_green_list: 各样本的最小绿灯时间列表
        max_green_list: 各样本的最大绿灯时间列表
        config: MaxPressureConfig配置对象

    Returns:
        决策列表，每个元素为 'yes' 或 'no'

    Examples:
        >>> config = MaxPressureConfig()
        >>> prompts = ["{...}", "{...}"]  # 简化示例
        >>> green_elapsed_list = [15, 20]
        >>> min_green_list = [10, 10]
        >>> max_green_list = [60, 60]
        >>> decisions = batch_max_pressure_decision(
        ...     prompts, green_elapsed_list,
        ...     min_green_list, max_green_list, config
        ... )
        >>> assert len(decisions) == 2
        >>> assert all(d in ['yes', 'no'] for d in decisions)
    """
    decisions = []

    for prompt, green_elapsed, min_green, max_green in zip(
        prompts, green_elapsed_list, min_green_list, max_green_list
    ):
        try:
            decision = max_pressure_decision_from_prompt(
                prompt=prompt,
                green_elapsed=green_elapsed,
                min_green=min_green,
                max_green=max_green,
                config=config
            )
            decisions.append(decision)
        except (ValueError, KeyError, json.JSONDecodeError) as e:
            # 解析失败时返回'no'（保守策略：切换相位）
            decisions.append('no')

    return decisions


def compare_with_baseline(
    model_decisions: List[str],
    baseline_decisions: List[str]
) -> List[bool]:
    """
    比较模型决策与baseline决策

    评估模型与Max Pressure baseline的一致性。

    Args:
        model_decisions: 模型输出决策列表（'yes'/'no'）
        baseline_decisions: Max Pressure决策列表（'yes'/'no'）

    Returns:
        匹配结果列表，True表示一致，False表示不一致

    Raises:
        ValueError: 两个列表长度不一致时

    Examples:
        >>> model = ['yes', 'no', 'yes']
        >>> baseline = ['yes', 'yes', 'yes']
        >>> matches = compare_with_baseline(model, baseline)
        >>> assert sum(matches) == 2  # 2个匹配
        >>> assert matches == [True, False, True]
    """
    if len(model_decisions) != len(baseline_decisions):
        raise ValueError(
            f"决策列表长度不一致: "
            f"model={len(model_decisions)}, baseline={len(baseline_decisions)}"
        )

    # 标准化为小写后比较
    matches = [
        m.lower() == b.lower()
        for m, b in zip(model_decisions, baseline_decisions)
    ]

    return matches


def compute_baseline_accuracy(
    model_decisions: List[str],
    baseline_decisions: List[str]
) -> float:
    """
    计算模型与baseline的一致性准确率

    Args:
        model_decisions: 模型输出决策列表
        baseline_decisions: Max Pressure决策列表

    Returns:
        准确率（0-1之间的浮点数）

    Examples:
        >>> model = ['yes', 'no', 'yes', 'yes']
        >>> baseline = ['yes', 'yes', 'yes', 'no']
        >>> accuracy = compute_baseline_accuracy(model, baseline)
        >>> assert accuracy == 0.5  # 4个中2个匹配
    """
    matches = compare_with_baseline(model_decisions, baseline_decisions)
    if not matches:
        return 0.0
    return sum(matches) / len(matches)
