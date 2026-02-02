# -*- coding: utf-8 -*-
"""GRPO模块初始化"""

from .config import (
    GRPOConfig,
    DEFAULT_CONFIG,
    SYSTEM_PROMPT,
    GRPOTrainingConfig,
    load_config,
)
# 注意：training 模块的导入放在最后或使用延迟导入，
# 避免 `python -m grpo.training` 时出现 RuntimeWarning
# 只有在非 -m 方式运行时才导入
import sys
if 'grpo.training' not in sys.modules:
    from .training import train_grpo, load_grpo_dataset
else:
    # 如果已经在 sys.modules 中，直接引用
    from grpo import training as _training
    train_grpo = _training.train_grpo
    load_grpo_dataset = _training.load_grpo_dataset
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
    'train_grpo',
    'load_grpo_dataset',
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
