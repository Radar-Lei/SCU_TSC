#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GRPO数据集生成 - 主入口脚本

用法:
    # 生成单个场景
    python -m grpo.generate_grpo_dataset --scenario arterial4x4_1
    
    # 生成多个场景（并行）
    python -m grpo.generate_grpo_dataset --scenarios arterial4x4_1,arterial4x4_2 --parallel 4
    
    # 生成所有场景
    python -m grpo.generate_grpo_dataset --all --parallel 8
"""

import argparse
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from grpo.config import GRPOConfig
from grpo.dataset_generator import GRPODatasetGenerator
from grpo.parallel_runner import ParallelRunner


def parse_args():
    parser = argparse.ArgumentParser(
        description="GRPO数据集生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # 场景选择
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--scenario", "-s",
        type=str,
        help="单个场景名称"
    )
    group.add_argument(
        "--scenarios",
        type=str,
        help="多个场景名称，逗号分隔"
    )
    group.add_argument(
        "--all", "-a",
        action="store_true",
        help="处理所有场景"
    )
    
    # 配置参数
    parser.add_argument(
        "--parallel", "-p",
        type=int,
        default=1,
        help="并行进程数 (默认: 1)"
    )
    parser.add_argument(
        "--extend-seconds",
        type=int,
        default=5,
        help="决策延长秒数 (默认: 5)"
    )
    parser.add_argument(
        "--output-dir", "-o",
        type=str,
        default=None,
        help="输出目录 (默认: data/grpo_datasets)"
    )
    parser.add_argument(
        "--scenarios-dir",
        type=str,
        default=None,
        help="场景目录 (默认: sumo_simulation/environments)"
    )
    parser.add_argument(
        "--warmup-steps",
        type=int,
        default=300,
        help="预热步数 (默认: 300)"
    )
    parser.add_argument(
        "--min-green-offset",
        type=float,
        default=2.0,
        help="最小绿偏移范围 (默认: 2.0)"
    )
    parser.add_argument(
        "--max-green-offset",
        type=float,
        default=5.0,
        help="最大绿偏移范围 (默认: 5.0)"
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="使用SUMO GUI（仅用于调试）"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="详细输出"
    )
    
    return parser.parse_args()


def main():
    args = parse_args()
    
    # 构建配置
    config = GRPOConfig(
        extend_seconds=args.extend_seconds,
        min_green_offset_range=args.min_green_offset,
        max_green_offset_range=args.max_green_offset,
        warmup_steps=args.warmup_steps,
        use_gui=args.gui,
        num_workers=args.parallel,
    )
    
    if args.output_dir:
        config.output_dir = args.output_dir
    if args.scenarios_dir:
        config.scenarios_dir = args.scenarios_dir
    
    print("=" * 60)
    print("GRPO数据集生成器")
    print("=" * 60)
    print(f"决策延长秒数: {config.extend_seconds}")
    print(f"最小绿偏移范围: ±{config.min_green_offset_range}s")
    print(f"最大绿偏移范围: ±{config.max_green_offset_range}s")
    print(f"预热步数: {config.warmup_steps}")
    print(f"并行进程数: {config.num_workers}")
    print(f"输出目录: {config.output_dir}")
    print("=" * 60)
    
    # 确定要处理的场景
    if args.scenario:
        scenarios = [args.scenario]
    elif args.scenarios:
        scenarios = [s.strip() for s in args.scenarios.split(",")]
    else:
        scenarios = None  # 处理所有
    
    # 运行
    if scenarios and len(scenarios) == 1 and args.parallel <= 1:
        # 单场景串行
        generator = GRPODatasetGenerator(config)
        entries = generator.generate_for_scenario(scenarios[0])
        print(f"\n完成！共生成 {len(entries)} 条数据")
    else:
        # 多场景或并行
        runner = ParallelRunner(config)
        results = runner.run(scenarios)
        total = sum(results.values())
        print(f"\n完成！共生成 {total} 条数据")


if __name__ == "__main__":
    main()
