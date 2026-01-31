#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GRPO数据生成器测试脚本

运行方式:
    # 单场景测试
    python -m grpo.test_generator --single arterial4x4_1

    # 并行处理所有场景
    python -m grpo.test_generator --parallel 8
"""

import os
import sys
import json
import argparse

# 添加项目根目录
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from grpo.config import GRPOConfig, SYSTEM_PROMPT
from grpo.dataset_generator import GRPODatasetGenerator
from grpo.parallel_runner import ParallelRunner
from grpo.prompt_builder import build_extend_decision_prompt, generate_timestamp


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="GRPO数据生成器测试脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--single", "-s",
        type=str,
        help="只运行单个场景测试"
    )
    parser.add_argument(
        "--parallel", "-p",
        type=int,
        default=0,
        help="并行进程数 (0=使用默认配置，默认: 0)"
    )
    parser.add_argument(
        "--warmup-steps",
        type=int,
        default=100,
        help="预热步数 (默认: 100)"
    )
    return parser.parse_args()


def test_prompt_builder():
    """测试Prompt构建器"""
    print("\n=== 测试Prompt构建器 ===")
    
    prompt = build_extend_decision_prompt(
        crossing_id=1234,
        as_of="2025-01-01 08:30:00",
        phase_order=[0, 2, 4, 6],
        current_phase_id=2,
        phase_metrics={0: 3.5, 2: 1.2, 4: 5.8, 6: 0.0}
    )
    
    print("生成的Prompt:")
    print(prompt)
    
    # 验证JSON格式
    data = json.loads(prompt)
    assert data["crossing_id"] == 1234
    assert data["state"]["current_phase_id"] == 2
    print("✓ Prompt格式正确")


def test_timestamp_generator():
    """测试时间戳生成"""
    print("\n=== 测试时间戳生成 ===")
    
    ts1 = generate_timestamp(0)
    print(f"仿真时间 0s: {ts1}")
    assert ts1 == "2025-01-01 00:00:00"
    
    ts2 = generate_timestamp(3661)  # 1小时1分1秒
    print(f"仿真时间 3661s: {ts2}")
    assert ts2 == "2025-01-01 01:01:01"
    
    print("✓ 时间戳生成正确")


def test_config():
    """测试配置"""
    print("\n=== 测试配置 ===")
    
    config = GRPOConfig()
    print(f"默认决策秒数: {config.extend_seconds}")
    print(f"默认并行数: {config.num_workers}")
    print(f"场景目录: {config.scenarios_dir}")
    print(f"输出目录: {config.output_dir}")
    
    assert config.extend_seconds == 5
    print("✓ 配置加载正确")


def test_single_scenario(scenario_name: str, warmup_steps: int = 100):
    """测试单场景数据生成（实际运行SUMO）"""
    print(f"\n=== 测试单场景数据生成: {scenario_name} ===")
    
    config = GRPOConfig(
        warmup_steps=warmup_steps,
        use_gui=False,
        num_workers=1,
    )
    
    generator = GRPODatasetGenerator(config)
    
    # 检查场景是否存在
    scenario_dir = os.path.join(config.scenarios_dir, scenario_name)
    
    if not os.path.exists(scenario_dir):
        print(f"跳过：场景 {scenario_name} 不存在")
        return None
    
    print(f"正在生成场景 {scenario_name} 的数据...")
    print("（这可能需要几分钟，取决于场景长度）")
    
    # 使用配置的实际输出目录
    output_dir = os.path.join(config.output_dir, scenario_name)
    os.makedirs(output_dir, exist_ok=True)
    
    entries = generator.generate_for_scenario(
        scenario_name=scenario_name,
        output_dir=output_dir
    )
    
    if entries:
        print(f"✓ 生成了 {len(entries)} 条数据")
        
        # 显示第一条数据
        first = entries[0]
        print(f"\n第一条数据示例:")
        print(f"  ID: {first.id}")
        print(f"  仿真时间: {first.simulation_time}s")
        print(f"  当前相位: {first.current_phase_id}")
        print(f"  绿灯已持续: {first.current_green_elapsed}s")
        print(f"  可以延长: {first.can_extend}")
        print(f"  状态文件: {first.state_file}")
        
        # 检查输出文件
        dataset_file = os.path.join(output_dir, "grpo_dataset.json")
        if os.path.exists(dataset_file):
            print(f"✓ 数据集文件已保存: {dataset_file}")
    else:
        print("✗ 未生成任何数据")
    
    return entries


def test_parallel_all_scenarios(num_workers: int = 0, warmup_steps: int = 100):
    """并行处理所有场景的数据生成"""
    print("\n=== 并行处理所有场景 ===")
    
    config = GRPOConfig(
        warmup_steps=warmup_steps,
        use_gui=False,
        num_workers=num_workers if num_workers > 0 else None,  # None=使用默认配置
    )
    
    print(f"配置信息:")
    print(f"  场景目录: {config.scenarios_dir}")
    print(f"  输出目录: {config.output_dir}")
    print(f"  并行进程数: {config.num_workers}")
    print(f"  预热步数: {config.warmup_steps}")
    
    runner = ParallelRunner(config)
    results = runner.run(None)  # None=处理所有场景
    
    return results


def main():
    args = parse_args()
    
    print("=" * 60)
    print("GRPO数据生成器测试")
    print("=" * 60)
    
    # 基础测试（不需要SUMO）
    test_config()
    test_timestamp_generator()
    test_prompt_builder()
    
    # 完整测试（需要SUMO）
    try:
        if args.single:
            # 单场景测试
            test_single_scenario(args.single, args.warmup_steps)
        else:
            # 并行处理所有场景
            test_parallel_all_scenarios(args.parallel, args.warmup_steps)
    except Exception as e:
        print(f"\n仿真测试失败: {e}")
        print("请确保SUMO已正确安装")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
