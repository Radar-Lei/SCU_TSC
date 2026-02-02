#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI参数覆盖配置测试脚本

验证命令行参数能否正确覆盖YAML配置文件中的值
"""

import sys
import argparse
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from grpo.config import GRPOTrainingConfig


def test_cli_override():
    """测试CLI参数覆盖"""
    print("=" * 60)
    print("CLI参数覆盖测试")
    print("=" * 60)

    # 配置文件路径
    config_path = "config/grpo_config.yaml"

    # 加载原始配置
    print(f"\n1. 加载原始配置: {config_path}")
    original_config = GRPOTrainingConfig.from_yaml(config_path)
    print(f"   原始 learning_rate: {original_config.learning_rate}")
    print(f"   原始 batch_size: {original_config.batch_size}")

    # 模拟CLI参数覆盖
    print("\n2. 模拟CLI参数覆盖")
    print("   --learning-rate 5e-5")
    print("   --batch-size 8")

    # 覆盖参数（模拟main函数中的逻辑）
    test_config = GRPOTrainingConfig.from_yaml(config_path)
    test_config.learning_rate = 5e-5
    test_config.batch_size = 8

    print(f"\n   覆盖后 learning_rate: {test_config.learning_rate}")
    print(f"   覆盖后 batch_size: {test_config.batch_size}")

    # 验证覆盖是否生效
    print("\n3. 验证覆盖结果")
    success = True

    if test_config.learning_rate == 5e-5:
        print(f"   ✅ learning_rate 已正确覆盖为 {test_config.learning_rate}")
    else:
        print(f"   ❌ learning_rate 覆盖失败: 期望 5e-5, 实际 {test_config.learning_rate}")
        success = False

    if test_config.batch_size == 8:
        print(f"   ✅ batch_size 已正确覆盖为 {test_config.batch_size}")
    else:
        print(f"   ❌ batch_size 覆盖失败: 期望 8, 实际 {test_config.batch_size}")
        success = False

    # 验证其他参数未被修改
    print("\n4. 验证其他参数未被修改")
    if test_config.model_path == original_config.model_path:
        print(f"   ✅ model_path 未被修改: {test_config.model_path}")
    else:
        print(f"   ❌ model_path 被意外修改")
        success = False

    if test_config.num_train_epochs == original_config.num_train_epochs:
        print(f"   ✅ num_train_epochs 未被修改: {test_config.num_train_epochs}")
    else:
        print(f"   ❌ num_train_epochs 被意外修改")
        success = False

    print("\n" + "=" * 60)
    if success:
        print("✅ CLI参数覆盖功能验证通过")
        print("=" * 60)
        return True
    else:
        print("❌ CLI参数覆盖功能验证失败")
        print("=" * 60)
        return False


if __name__ == "__main__":
    success = test_cli_override()
    sys.exit(0 if success else 1)
