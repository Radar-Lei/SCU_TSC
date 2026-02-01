#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SFT数据集生成器

从GRPO数据集生成SFT格式的数据，用于训练模型输出正确的JSON格式。
SFT只教会模型输出格式 {"extend": "yes/no"}，不关心决策正确性。

用法:
    python -m grpo.generate_sft_dataset
    python -m grpo.generate_sft_dataset --sample-size 500
"""

import os
import sys
import json
import random
import argparse
from typing import List, Dict, Any, Optional
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from grpo.config import SYSTEM_PROMPT


def load_grpo_datasets(grpo_datasets_dir: str) -> List[Dict[str, Any]]:
    """
    加载所有场景的GRPO数据集
    
    Args:
        grpo_datasets_dir: GRPO数据集根目录
        
    Returns:
        合并后的数据条目列表
    """
    all_entries = []
    
    if not os.path.isdir(grpo_datasets_dir):
        print(f"错误：GRPO数据集目录不存在: {grpo_datasets_dir}")
        return []
    
    for scenario_name in os.listdir(grpo_datasets_dir):
        scenario_dir = os.path.join(grpo_datasets_dir, scenario_name)
        if not os.path.isdir(scenario_dir):
            continue
        
        dataset_file = os.path.join(scenario_dir, "grpo_dataset.json")
        if not os.path.isfile(dataset_file):
            continue
        
        try:
            with open(dataset_file, 'r', encoding='utf-8') as f:
                entries = json.load(f)
                all_entries.extend(entries)
                print(f"加载 {scenario_name}: {len(entries)} 条数据")
        except Exception as e:
            print(f"加载 {scenario_name} 失败: {e}")
    
    print(f"共加载 {len(all_entries)} 条GRPO数据")
    return all_entries


def create_sft_entry(grpo_entry: Dict[str, Any], system_prompt: str) -> Dict[str, Any]:
    """
    从GRPO数据条目创建SFT格式的数据条目
    
    Args:
        grpo_entry: GRPO数据条目
        system_prompt: 系统提示模板
        
    Returns:
        SFT格式的数据条目
    """
    # 随机生成yes/no决策（SFT只关心格式）
    decision = random.choice(["yes", "no"])
    response = json.dumps({"extend": decision}, ensure_ascii=False)
    
    # 构建完整的系统提示（使用replace而非format，避免花括号冲突）
    full_system_prompt = system_prompt.replace(
        "{extend_decision_input_json}",
        grpo_entry["prompt"]
    )
    
    # 构建对话格式
    messages = [
        {"role": "system", "content": full_system_prompt},
        {"role": "user", "content": grpo_entry["prompt"]},
        {"role": "assistant", "content": response}
    ]
    
    return {
        "id": grpo_entry["id"],
        "scenario": grpo_entry["scenario"],
        "messages": messages
    }


def generate_sft_dataset(
    grpo_datasets_dir: str,
    output_dir: str,
    sample_size: Optional[int] = None,
    seed: int = 42
) -> List[Dict[str, Any]]:
    """
    生成SFT数据集
    
    Args:
        grpo_datasets_dir: GRPO数据集目录
        output_dir: 输出目录
        sample_size: 采样数量，None表示使用全部
        seed: 随机种子
        
    Returns:
        SFT数据条目列表
    """
    random.seed(seed)
    
    # 加载GRPO数据
    grpo_entries = load_grpo_datasets(grpo_datasets_dir)
    if not grpo_entries:
        print("错误：没有找到GRPO数据")
        return []
    
    # 采样
    if sample_size and sample_size < len(grpo_entries):
        grpo_entries = random.sample(grpo_entries, sample_size)
        print(f"采样 {sample_size} 条数据")
    
    # 转换为SFT格式
    sft_entries = []
    for entry in grpo_entries:
        sft_entry = create_sft_entry(entry, SYSTEM_PROMPT)
        sft_entries.append(sft_entry)
    
    # 保存
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "sft_dataset.json")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sft_entries, f, ensure_ascii=False, indent=2)
    
    print(f"SFT数据集已保存: {output_file}")
    print(f"共 {len(sft_entries)} 条数据")
    
    # 同时保存为JSONL格式（兼容datasets库）
    jsonl_file = os.path.join(output_dir, "sft_dataset.jsonl")
    with open(jsonl_file, 'w', encoding='utf-8') as f:
        for entry in sft_entries:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    print(f"JSONL格式已保存: {jsonl_file}")
    
    return sft_entries


def parse_args():
    parser = argparse.ArgumentParser(
        description="SFT数据集生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--grpo-dir",
        type=str,
        default="/home/samuel/SCU_TSC/data/grpo_datasets",
        help="GRPO数据集目录 (默认: data/grpo_datasets)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="/home/samuel/SCU_TSC/data/sft_datasets",
        help="输出目录 (默认: data/sft_datasets)"
    )
    parser.add_argument(
        "--sample-size",
        type=int,
        default=None,
        help="采样数量，不指定则使用全部数据"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="随机种子 (默认: 42)"
    )
    
    return parser.parse_args()


def main():
    args = parse_args()
    
    print("=" * 60)
    print("SFT数据集生成器")
    print("=" * 60)
    print(f"GRPO数据目录: {args.grpo_dir}")
    print(f"输出目录: {args.output_dir}")
    print(f"采样数量: {args.sample_size or '全部'}")
    print(f"随机种子: {args.seed}")
    print("=" * 60)
    
    generate_sft_dataset(
        grpo_datasets_dir=args.grpo_dir,
        output_dir=args.output_dir,
        sample_size=args.sample_size,
        seed=args.seed
    )
    
    print("完成！")


if __name__ == "__main__":
    main()
