#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Format Reward三级评分测试脚本

验证format_reward_fn的三种评分机制：
1. 严格格式 → +1.0
2. 部分格式 → -0.5
3. 无效格式 → -10.0
"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from grpo.reward import format_reward_fn


def test_format_reward_three_levels():
    """测试Format Reward三级评分"""
    print("=" * 60)
    print("Format Reward三级评分测试")
    print("=" * 60)

    # 默认评分值
    strict_reward = 1.0
    partial_reward = -0.5
    invalid_reward = -10.0

    # 测试用例
    test_cases = [
        {
            "name": "严格格式 - yes",
            "output": '{"extend": "yes"}',
            "expected_reward": strict_reward,
            "expected_is_strict": True,
            "expected_is_partial": False,
        },
        {
            "name": "严格格式 - no",
            "output": '{"extend": "no"}',
            "expected_reward": strict_reward,
            "expected_is_strict": True,
            "expected_is_partial": False,
        },
        {
            "name": "部分格式 - 带前缀",
            "output": 'Decision: {"extend": "yes"}',
            "expected_reward": partial_reward,
            "expected_is_strict": False,
            "expected_is_partial": True,
        },
        {
            "name": "部分格式 - 带额外字段",
            "output": '{"extend": "no", "confidence": 0.9}',
            "expected_reward": partial_reward,
            "expected_is_strict": False,
            "expected_is_partial": True,
        },
        {
            "name": "部分格式 - 带额外文本和JSON",
            "output": '我的决策是: {"extend": "yes"}，因为排队很长',
            "expected_reward": partial_reward,
            "expected_is_strict": False,
            "expected_is_partial": True,
        },
        {
            "name": "无效格式 - 纯文本",
            "output": "invalid text",
            "expected_reward": invalid_reward,
            "expected_is_strict": False,
            "expected_is_partial": False,
        },
        {
            "name": "无效格式 - 错误的JSON",
            "output": '{"wrong": "format"}',
            "expected_reward": invalid_reward,
            "expected_is_strict": False,
            "expected_is_partial": False,
        },
        {
            "name": "无效格式 - 空字符串",
            "output": "",
            "expected_reward": invalid_reward,
            "expected_is_strict": False,
            "expected_is_partial": False,
        },
    ]

    print(f"\n默认评分配置:")
    print(f"  严格格式 (strict):  +{strict_reward}")
    print(f"  部分格式 (partial): {partial_reward}")
    print(f"  无效格式 (invalid): {invalid_reward}")
    print()

    all_passed = True
    for i, test in enumerate(test_cases, 1):
        print(f"测试 {i}: {test['name']}")
        print(f"  输入: {repr(test['output'])}")

        result = format_reward_fn(
            test['output'],
            strict_reward=strict_reward,
            partial_reward=partial_reward,
            invalid_reward=invalid_reward
        )

        # 验证reward值
        if result.reward == test['expected_reward']:
            print(f"  ✅ reward: {result.reward} (符合预期)")
        else:
            print(f"  ❌ reward: {result.reward} (预期: {test['expected_reward']})")
            all_passed = False

        # 验证is_strict
        if result.is_strict == test['expected_is_strict']:
            print(f"  ✅ is_strict: {result.is_strict} (符合预期)")
        else:
            print(f"  ❌ is_strict: {result.is_strict} (预期: {test['expected_is_strict']})")
            all_passed = False

        # 验证is_partial
        if result.is_partial == test['expected_is_partial']:
            print(f"  ✅ is_partial: {result.is_partial} (符合预期)")
        else:
            print(f"  ❌ is_partial: {result.is_partial} (预期: {test['expected_is_partial']})")
            all_passed = False

        # 显示提取的决策
        if result.extracted_decision:
            print(f"  📋 extracted_decision: {result.extracted_decision}")
        print()

    print("=" * 60)
    if all_passed:
        print("✅ Format Reward三级评分验证通过")
        print("=" * 60)
        return True
    else:
        print("❌ Format Reward三级评分验证失败")
        print("=" * 60)
        return False


if __name__ == "__main__":
    success = test_format_reward_three_levels()
    sys.exit(0 if success else 1)
