#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Format Reward配置化测试脚本

验证config/grpo_config.yaml中的format_reward配置可以被正确读取和使用
"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from grpo.config import GRPOTrainingConfig
from grpo.reward import format_reward_fn


def test_format_reward_configurable():
    """测试Format Reward配置化"""
    print("=" * 60)
    print("Format Reward配置化测试")
    print("=" * 60)

    # 配置文件路径
    config_path = "config/grpo_config.yaml"

    # 加载配置
    print(f"\n1. 加载配置文件: {config_path}")
    config = GRPOTrainingConfig.from_yaml(config_path)

    # 检查format_reward配置
    print("\n2. 读取format_reward配置:")
    print(f"   strict:   {config.format_reward.strict}")
    print(f"   partial:  {config.format_reward.partial}")
    print(f"   invalid:  {config.format_reward.invalid}")
    print(f"   regex:    {config.format_reward.extract_regex}")

    # 验证配置值是否合理
    print("\n3. 验证配置值:")
    success = True

    if config.format_reward.strict > 0:
        print(f"   ✅ strict ({config.format_reward.strict}) 为正值")
    else:
        print(f"   ❌ strict ({config.format_reward.strict}) 应为正值")
        success = False

    if config.format_reward.partial < 0:
        print(f"   ✅ partial ({config.format_reward.partial}) 为负值")
    else:
        print(f"   ❌ partial ({config.format_reward.partial}) 应为负值")
        success = False

    if config.format_reward.invalid < config.format_reward.partial:
        print(f"   ✅ invalid ({config.format_reward.invalid}) < partial ({config.format_reward.partial})")
    else:
        print(f"   ❌ invalid ({config.format_reward.invalid}) 应小于 partial")
        success = False

    if config.format_reward.extract_regex:
        print(f"   ✅ extract_regex 已配置")
    else:
        print(f"   ❌ extract_regex 未配置")
        success = False

    # 使用配置值测试format_reward_fn
    print("\n4. 使用配置值测试format_reward_fn:")

    test_output = '{"extend": "yes"}'
    result = format_reward_fn(
        test_output,
        regex=config.format_reward.extract_regex,
        strict_reward=config.format_reward.strict,
        partial_reward=config.format_reward.partial,
        invalid_reward=config.format_reward.invalid
    )

    print(f"   输入: {test_output}")
    print(f"   返回reward: {result.reward}")
    print(f"   期望reward: {config.format_reward.strict} (strict)")

    if result.reward == config.format_reward.strict:
        print(f"   ✅ reward值与配置一致")
    else:
        print(f"   ❌ reward值与配置不一致")
        success = False

    # 测试部分格式
    print("\n5. 测试部分格式:")
    test_partial = 'Decision: {"extend": "no"}'
    result_partial = format_reward_fn(
        test_partial,
        regex=config.format_reward.extract_regex,
        strict_reward=config.format_reward.strict,
        partial_reward=config.format_reward.partial,
        invalid_reward=config.format_reward.invalid
    )

    print(f"   输入: {test_partial}")
    print(f"   返回reward: {result_partial.reward}")
    print(f"   期望reward: {config.format_reward.partial} (partial)")

    if result_partial.reward == config.format_reward.partial:
        print(f"   ✅ reward值与配置一致")
    else:
        print(f"   ❌ reward值与配置不一致")
        success = False

    print("\n" + "=" * 60)
    if success:
        print("✅ Format Reward配置化验证通过")
        print("=" * 60)
        return True
    else:
        print("❌ Format Reward配置化验证失败")
        print("=" * 60)
        return False


if __name__ == "__main__":
    success = test_format_reward_configurable()
    sys.exit(0 if success else 1)
