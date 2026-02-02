#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小规模测试数据生成脚本

为集成测试生成小规模测试数据：
- 生成50条GRPO测试数据
- 从GRPO数据生成20条SFT测试数据
- 保存到tests/fixtures/testdata/目录

用法:
    python scripts/prepare_test_data.py
    python scripts/prepare_test_data.py --num-grpo 100 --num-sft 50
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


def generate_mock_sumo_state() -> Dict[str, Any]:
    """
    生成模拟的SUMO状态数据

    Returns:
        模拟的SUMO状态字典
    """
    return {
        "time": 10.0,
        "junction_id": f"cluster_{random.randint(10000000, 99999999)}",
        "phase_metrics_by_id": {
            str(phase_id): {
                "avg_queue_veh": random.uniform(0, 20),
                "avg_queue_length": random.uniform(0, 50),
                "avg_speed": random.uniform(0, 15),
            }
            for phase_id in range(4)
        },
        "current_phase_id": random.randint(0, 3),
        "green_elapsed": random.uniform(5, 30),
        "phase_order": [0, 1, 2, 3]
    }


def create_grpo_entry(entry_id: int, scenario: str) -> Dict[str, Any]:
    """
    创建一条GRPO测试数据

    Args:
        entry_id: 数据条目ID
        scenario: 场景名称

    Returns:
        GRPO格式的数据条目
    """
    # 生成SUMO状态
    sumo_state = generate_mock_sumo_state()

    # 构建prompt
    prompt_data = {
        "crossing_id": sumo_state["junction_id"],
        "state": {
            "current_phase_id": sumo_state["current_phase_id"],
            "green_elapsed": sumo_state["green_elapsed"],
            "phase_metrics_by_id": sumo_state["phase_metrics_by_id"]
        },
        "phase_order": sumo_state["phase_order"]
    }
    prompt = json.dumps(prompt_data, ensure_ascii=False)

    return {
        "id": f"test_{scenario}_{entry_id:06d}",
        "scenario": scenario,
        "junction_id": sumo_state["junction_id"],
        "prompt": prompt,
        "sumo_state": sumo_state,
        # 模拟state_file路径（实际不存在，但测试需要）
        "state_file": f"data/sumo_states/{scenario}/state_{entry_id:06d}.json"
    }


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


def generate_test_data(
    num_grpo: int = 50,
    num_sft: int = 20,
    output_dir: str = "tests/fixtures/testdata",
    scenarios: Optional[List[str]] = None
) -> Dict[str, str]:
    """
    生成测试数据

    Args:
        num_grpo: GRPO数据条数
        num_sft: SFT数据条数
        output_dir: 输出目录
        scenarios: 场景列表，None则使用默认场景

    Returns:
        生成的文件路径字典
    """
    if scenarios is None:
        scenarios = ["test_scenario"]

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 60)
    print("小规模测试数据生成器")
    print("=" * 60)
    print(f"GRPO数据条数: {num_grpo}")
    print(f"SFT数据条数: {num_sft}")
    print(f"输出目录: {output_dir}")
    print(f"场景: {scenarios}")
    print("=" * 60)

    # 生成GRPO数据
    print("\n[Step 1/3] 生成GRPO测试数据...")
    grpo_entries = []
    for scenario in scenarios:
        # 为每个场景均匀分配数据
        num_per_scenario = num_grpo // len(scenarios)
        for i in range(num_per_scenario):
            entry = create_grpo_entry(i, scenario)
            grpo_entries.append(entry)

    print(f"生成了 {len(grpo_entries)} 条GRPO数据")

    # 保存GRPO数据
    grpo_file = os.path.join(output_dir, "small_grpo_dataset.json")
    with open(grpo_file, 'w', encoding='utf-8') as f:
        json.dump(grpo_entries, f, ensure_ascii=False, indent=2)
    print(f"GRPO数据已保存: {grpo_file}")

    # 验证GRPO数据格式
    print("\n[Step 2/3] 验证GRPO数据格式...")
    try:
        with open(grpo_file, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
            assert len(loaded) == num_grpo
            assert all("id" in e for e in loaded)
            assert all("prompt" in e for e in loaded)
        print("GRPO数据格式验证通过 ✓")
    except Exception as e:
        print(f"GRPO数据格式验证失败: {e}")
        raise

    # 生成SFT数据
    print(f"\n[Step 3/3] 生成SFT测试数据...")
    # 从GRPO数据中采样
    if len(grpo_entries) >= num_sft:
        sft_grpo_entries = random.sample(grpo_entries, num_sft)
    else:
        sft_grpo_entries = grpo_entries

    sft_entries = []
    for entry in sft_grpo_entries:
        sft_entry = create_sft_entry(entry, SYSTEM_PROMPT)
        sft_entries.append(sft_entry)

    print(f"生成了 {len(sft_entries)} 条SFT数据")

    # 保存SFT数据
    sft_file = os.path.join(output_dir, "small_sft_dataset.json")
    with open(sft_file, 'w', encoding='utf-8') as f:
        json.dump(sft_entries, f, ensure_ascii=False, indent=2)
    print(f"SFT数据已保存: {sft_file}")

    # 保存JSONL格式（兼容datasets库）
    sft_jsonl_file = os.path.join(output_dir, "small_sft_dataset.jsonl")
    with open(sft_jsonl_file, 'w', encoding='utf-8') as f:
        for entry in sft_entries:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    print(f"SFT数据(JSONL)已保存: {sft_jsonl_file}")

    # 验证SFT数据格式
    print("\n验证SFT数据格式...")
    try:
        with open(sft_file, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
            assert len(loaded) == len(sft_entries)
            assert all("id" in e for e in loaded)
            assert all("messages" in e for e in loaded)
            assert all(len(e["messages"]) == 3 for e in loaded)
        print("SFT数据格式验证通过 ✓")
    except Exception as e:
        print(f"SFT数据格式验证失败: {e}")
        raise

    # 打印统计信息
    print("\n" + "=" * 60)
    print("数据生成完成!")
    print("=" * 60)
    print(f"GRPO数据: {len(grpo_entries)} 条 -> {grpo_file}")
    print(f"SFT数据: {len(sft_entries)} 条 -> {sft_file}")
    print(f"SFT数据(JSONL): {len(sft_entries)} 条 -> {sft_jsonl_file}")

    # 打印示例
    if grpo_entries:
        print("\nGRPO数据示例:")
        print(json.dumps(grpo_entries[0], ensure_ascii=False, indent=2)[:500] + "...")

    if sft_entries:
        print("\nSFT数据示例:")
        print(json.dumps(sft_entries[0], ensure_ascii=False, indent=2)[:500] + "...")

    return {
        "grpo_json": grpo_file,
        "sft_json": sft_file,
        "sft_jsonl": sft_jsonl_file
    }


def parse_args():
    parser = argparse.ArgumentParser(
        description="小规模测试数据生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--num-grpo",
        type=int,
        default=50,
        help="GRPO数据条数 (默认: 50)"
    )
    parser.add_argument(
        "--num-sft",
        type=int,
        default=20,
        help="SFT数据条数 (默认: 20)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="tests/fixtures/testdata",
        help="输出目录 (默认: tests/fixtures/testdata)"
    )
    parser.add_argument(
        "--scenarios",
        type=str,
        nargs="+",
        default=["test_scenario"],
        help="场景列表 (默认: test_scenario)"
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

    # 设置随机种子
    random.seed(args.seed)

    print(f"随机种子: {args.seed}")

    # 生成测试数据
    files = generate_test_data(
        num_grpo=args.num_grpo,
        num_sft=args.num_sft,
        output_dir=args.output_dir,
        scenarios=args.scenarios
    )

    print("\n完成!")


if __name__ == "__main__":
    main()
