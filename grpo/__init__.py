# -*- coding: utf-8 -*-
"""GRPO模块初始化

注意：training 模块不在此处自动导入，以避免使用 `python -m grpo.training` 时
产生 RuntimeWarning（模块在包导入后但执行前已存在于 sys.modules 中）。

如需使用 training 模块的功能，请显式导入：
    from grpo.training import train_grpo, load_grpo_dataset
或直接运行：
    python -m grpo.training
"""

from .config import (
    GRPOConfig,
    DEFAULT_CONFIG,
    SYSTEM_PROMPT,
    GRPOTrainingConfig,
    load_config,
)
from .reward import format_reward_fn, extract_decision, FormatResult
from .sumo_reward import tsc_reward_fn, calculate_tsc_reward_single, ParallelSUMORewardCalculator, TSCResult
from .max_pressure import (
    MaxPressureConfig,
    compute_phase_pressure,
    max_pressure_decision,
    max_pressure_decision_from_prompt,
    batch_max_pressure_decision,
    compare_with_baseline,
    compute_baseline_accuracy,
)

__all__ = [
    # 数据集生成相关
    'GRPOConfig',
    'DEFAULT_CONFIG',
    'SYSTEM_PROMPT',
    # 训练相关
    'GRPOTrainingConfig',
    'load_config',
    # Reward函数
    'format_reward_fn',
    'extract_decision',
    'FormatResult',
    # SUMO Reward函数
    'tsc_reward_fn',
    'calculate_tsc_reward_single',
    'ParallelSUMORewardCalculator',
    'TSCResult',
    # Max Pressure算法
    'MaxPressureConfig',
    'compute_phase_pressure',
    'max_pressure_decision',
    'max_pressure_decision_from_prompt',
    'batch_max_pressure_decision',
    'compare_with_baseline',
    'compute_baseline_accuracy',
]


def __getattr__(name):
    """延迟导入 training 模块的函数，避免循环导入和 -m 运行时的警告"""
    if name in ('train_grpo', 'load_grpo_dataset'):
        from .training import train_grpo, load_grpo_dataset
        globals()['train_grpo'] = train_grpo
        globals()['load_grpo_dataset'] = load_grpo_dataset
        return globals()[name]
    raise AttributeError(f"module 'grpo' has no attribute {name!r}")
