# -*- coding: utf-8 -*-
"""GRPO模块初始化"""

from .config import (
    GRPOConfig,
    DEFAULT_CONFIG,
    SYSTEM_PROMPT,
    GRPOTrainingConfig,
    load_config,
)
from .training import train_grpo, load_grpo_dataset
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
