#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置类加载测试脚本

验证 GRPOTrainingConfig.from_yaml 能否正确加载配置文件
"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from grpo.config import GRPOTrainingConfig


def test_config_loading():
    """测试配置文件加载"""
    print("=" * 60)
    print("配置类加载测试")
    print("=" * 60)

    # 配置文件路径
    config_path = "config/grpo_config.yaml"

    # 检查配置文件是否存在
    if not Path(config_path).exists():
        print(f"❌ 配置文件不存在: {config_path}")
        return False

    print(f"✅ 配置文件存在: {config_path}")
    print()

    # 加载配置
    try:
        config = GRPOTrainingConfig.from_yaml(config_path)
        print("✅ 配置加载成功")
        print()
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        return False

    # 转换为 dict
    try:
        config_dict = config.to_dict()
        print("✅ 配置转换为 dict 成功")
        print()
    except Exception as e:
        print(f"❌ 配置转换失败: {e}")
        return False

    # 验证必需字段
    required_fields = {
        "模型配置": ["model_path", "max_seq_length"],
        "GRPO核心参数": ["learning_rate", "batch_size", "num_generations", "temperature", "kl_coeff"],
        "生成控制参数": ["max_new_tokens", "top_p", "repetition_penalty"],
        "训练参数": ["num_train_epochs", "warmup_steps", "logging_steps", "optim"],
        "数据路径": ["dataset_path", "output_dir"],
    }

    print("验证必需字段:")
    all_fields_present = True
    for category, fields in required_fields.items():
        print(f"  {category}:")
        for field in fields:
            if field in config_dict:
                value = config_dict[field]
                print(f"    ✅ {field}: {value}")
            else:
                print(f"    ❌ {field}: 缺失")
                all_fields_present = False

    # 验证嵌套配置
    print()
    print("验证嵌套配置:")
    nested_configs = {
        "reward": ["format_weight", "tsc_weight"],
        "format_reward": ["strict", "partial", "invalid", "extract_regex"],
        "sumo": ["max_workers", "port_range", "reward_scale"],
    }

    for config_name, fields in nested_configs.items():
        print(f"  {config_name}:")
        if config_name not in config_dict:
            print(f"    ❌ 整个配置缺失")
            all_fields_present = False
            continue

        config_value = config_dict[config_name]
        for field in fields:
            if field in config_value:
                value = config_value[field]
                print(f"    ✅ {field}: {value}")
            else:
                print(f"    ❌ {field}: 缺失")
                all_fields_present = False

    print()
    print("=" * 60)
    if all_fields_present:
        print("✅ 所有配置字段验证通过")
        print("=" * 60)
        return True
    else:
        print("❌ 部分配置字段缺失")
        print("=" * 60)
        return False


if __name__ == "__main__":
    success = test_config_loading()
    sys.exit(0 if success else 1)
