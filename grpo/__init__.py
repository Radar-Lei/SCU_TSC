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
]
