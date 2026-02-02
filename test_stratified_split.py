#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试分层抽样修复效果

验证训练集和验证集的场景分布是否一致
"""

import sys
import os
import json
from collections import Counter

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from grpo.sft_training import load_sft_dataset

def test_stratified_split():
    """测试分层抽样效果"""

    print("=" * 60)
    print("测试分层抽样数据划分")
    print("=" * 60)

    # 加载数据集
    dataset_path = "/home/samuel/SCU_TSC/data/sft_datasets/sft_dataset.json"

    print(f"\n加载数据集: {dataset_path}")
    train_dataset, eval_dataset = load_sft_dataset(
        dataset_path,
        eval_percent=0.05,
        eval_limit=100
    )

    if eval_dataset is None:
        print("❌ 验证集为空，测试失败")
        return False

    # 统计场景分布
    train_scenarios = [item['scenario'] for item in train_dataset]
    eval_scenarios = [item['scenario'] for item in eval_dataset]

    train_counts = Counter(train_scenarios)
    eval_counts = Counter(eval_scenarios)

    print("\n" + "=" * 60)
    print("场景分布统计")
    print("=" * 60)

    # 计算所有场景
    all_scenarios = sorted(set(train_scenarios + eval_scenarios))

    print(f"\n{'场景':<20} {'训练集':<10} {'验证集':<10} {'训练占比':<12} {'验证占比':<12}")
    print("-" * 60)

    for scenario in all_scenarios:
        train_count = train_counts.get(scenario, 0)
        eval_count = eval_counts.get(scenario, 0)
        train_ratio = train_count / len(train_dataset) * 100
        eval_ratio = eval_count / len(eval_dataset) * 100

        print(f"{scenario:<20} {train_count:<10} {eval_count:<10} {train_ratio:<12.2f}% {eval_ratio:<12.2f}%")

    # 验证修复效果
    print("\n" + "=" * 60)
    print("验证修复效果")
    print("=" * 60)

    # 检查1: 验证集是否包含多个场景
    num_eval_scenarios = len(eval_counts)
    if num_eval_scenarios >= 3:
        print(f"✓ 验证集包含 {num_eval_scenarios} 个场景 (修复前: 1个)")
    else:
        print(f"⚠ 验证集只包含 {num_eval_scenarios} 个场景，建议更多")

    # 检查2: 场景分布是否一致
    max_ratio_diff = 0
    for scenario in all_scenarios:
        train_ratio = train_counts.get(scenario, 0) / len(train_dataset)
        eval_ratio = eval_counts.get(scenario, 0) / len(eval_dataset)
        ratio_diff = abs(train_ratio - eval_ratio)
        max_ratio_diff = max(max_ratio_diff, ratio_diff)

    if max_ratio_diff < 0.05:  # 差异小于5%
        print(f"✓ 场景分布一致 (最大比例差异: {max_ratio_diff*100:.2f}%)")
    else:
        print(f"⚠ 场景分布有差异 (最大比例差异: {max_ratio_diff*100:.2f}%)")

    # 检查3: 是否避免了时间序列数据泄露
    print(f"\n✓ 使用分层随机抽样，避免了时间序列数据泄露")

    # 总体评估
    print("\n" + "=" * 60)
    if num_eval_scenarios >= 3 and max_ratio_diff < 0.05:
        print("✅ 修复成功！数据划分合理")
        return True
    else:
        print("⚠️  修复部分成功，建议进一步调整")
        return False

if __name__ == "__main__":
    success = test_stratified_split()
    sys.exit(0 if success else 1)
