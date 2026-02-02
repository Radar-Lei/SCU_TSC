#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TSC Reward归一化测试脚本

验证normalize_reward函数使用tanh(-delta/scale)将排队数变化归一化到[-1,1]范围
"""

import sys
import math
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from grpo.sumo_reward import normalize_reward


def test_normalize_reward():
    """测试TSC Reward归一化"""
    print("=" * 60)
    print("TSC Reward归一化测试")
    print("=" * 60)

    scale = 10.0  # 默认scale值

    # 测试用例
    test_cases = [
        {
            "name": "排队数减少10辆（改善）",
            "queue_before": 20,
            "queue_after": 10,
            "expected_delta": -10,
            "expected_sign": "positive",  # 改善应该返回正reward
        },
        {
            "name": "排队数增加10辆（恶化）",
            "queue_before": 10,
            "queue_after": 20,
            "expected_delta": 10,
            "expected_sign": "negative",  # 恶化应该返回负reward
        },
        {
            "name": "排队数不变",
            "queue_before": 15,
            "queue_after": 15,
            "expected_delta": 0,
            "expected_sign": "zero",
        },
        {
            "name": "排队数大幅减少30辆",
            "queue_before": 50,
            "queue_after": 20,
            "expected_delta": -30,
            "expected_sign": "positive",
        },
        {
            "name": "排队数大幅增加30辆",
            "queue_before": 20,
            "queue_after": 50,
            "expected_delta": 30,
            "expected_sign": "negative",
        },
    ]

    print(f"\n归一化公式: tanh(-delta / {scale})")
    print(f"输出范围: [-1, 1]")
    print()

    all_passed = True
    for i, test in enumerate(test_cases, 1):
        print(f"测试 {i}: {test['name']}")
        print(f"  queue_before: {test['queue_before']}")
        print(f"  queue_after:  {test['queue_after']}")

        # 计算delta
        delta = test['queue_after'] - test['queue_before']
        print(f"  delta: {delta}")

        # 验证delta
        if delta == test['expected_delta']:
            print(f"  ✅ delta计算正确")
        else:
            print(f"  ❌ delta计算错误: 期望 {test['expected_delta']}, 实际 {delta}")
            all_passed = False

        # 计算归一化reward
        reward = normalize_reward(delta, scale=scale)
        print(f"  normalized_reward: {reward:.4f}")

        # 验证reward范围
        if -1.0 <= reward <= 1.0:
            print(f"  ✅ reward在[-1, 1]范围内")
        else:
            print(f"  ❌ reward超出范围: {reward}")
            all_passed = False

        # 验证reward符号
        expected_sign = test['expected_sign']
        if expected_sign == "positive":
            if reward > 0:
                print(f"  ✅ reward为正（改善）")
            else:
                print(f"  ❌ reward应为正（改善），实际: {reward}")
                all_passed = False
        elif expected_sign == "negative":
            if reward < 0:
                print(f"  ✅ reward为负（恶化）")
            else:
                print(f"  ❌ reward应为负（恶化），实际: {reward}")
                all_passed = False
        elif expected_sign == "zero":
            if abs(reward) < 0.001:
                print(f"  ✅ reward接近零（不变）")
            else:
                print(f"  ❌ reward应接近零（不变），实际: {reward}")
                all_passed = False

        # 验证公式
        expected_reward = math.tanh(-delta / scale)
        if abs(reward - expected_reward) < 0.0001:
            print(f"  ✅ 公式正确: tanh(-{delta}/{scale}) = {expected_reward:.4f}")
        else:
            print(f"  ❌ 公式错误")
            all_passed = False

        print()

    # 额外测试：边界情况
    print("边界测试:")
    print("  极大的delta (100):", normalize_reward(100, scale))
    print("  极小的delta (-100):", normalize_reward(-100, scale))
    print()

    print("=" * 60)
    if all_passed:
        print("✅ TSC Reward归一化验证通过")
        print("=" * 60)
        return True
    else:
        print("❌ TSC Reward归一化验证失败")
        print("=" * 60)
        return False


if __name__ == "__main__":
    success = test_normalize_reward()
    sys.exit(0 if success else 1)
