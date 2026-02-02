#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
综合功能测试脚本（测试8-11）

验证：
8. 并行SUMO Reward计算
9. Reward函数链组合
10. Early-return优化
11. 批量Reward计算
"""

import sys
import os
import json
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from grpo.sumo_reward import ParallelSUMORewardCalculator
from grpo.reward import compute_reward, batch_compute_reward, format_reward_fn
from grpo.config import GRPOTrainingConfig
from types import SimpleNamespace


def test_parallel_sumo_calculator():
    """测试8: 并行SUMO Reward计算"""
    print("\n" + "=" * 60)
    print("测试8: 并行SUMO Reward计算")
    print("=" * 60)

    # 读取测试数据
    dataset_path = "data/grpo_datasets/arterial4x4_99/grpo_dataset.json"
    if not os.path.exists(dataset_path):
        print("⚠️  测试数据不存在，跳过此测试")
        return None

    with open(dataset_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 取前2条数据
    samples = data[:2]

    # 准备输入
    state_files = []
    prompts = []
    outputs = []

    for sample in samples:
        state_file = os.path.join(
            "data/grpo_datasets",
            sample['scenario'],
            sample['state_file']
        )
        prompt_data = {
            "crossing_id": sample['junction_id'],
            "state": {"current_phase_id": sample['current_phase_id']},
            "phase_order": sample['phase_order']
        }

        state_files.append(state_file)
        prompts.append(json.dumps(prompt_data, ensure_ascii=False))
        outputs.append('{"extend": "yes"}')  # 添加对应的输出

    # 创建配置
    scenario_dir = "sumo_simulation/environments/" + samples[0]['scenario']
    import glob
    sumocfg_files = glob.glob(os.path.join(scenario_dir, "*.sumocfg"))
    if not sumocfg_files:
        print("⚠️  找不到sumocfg文件，跳过此测试")
        return None

    config = SimpleNamespace(
        max_workers=2,
        extend_seconds=5,
        reward_scale=10.0,
        sumocfg_path=sumocfg_files[0],
        port_range=[10000, 60000],
    )

    # 创建并行计算器
    calculator = ParallelSUMORewardCalculator(config)

    # 并行计算（修正：传入config参数）
    print(f"  并行计算 {len(state_files)} 个样本的TSC reward...")
    results = calculator.calculate_batch(prompts, outputs, state_files, config)

    # 验证结果
    if len(results) == len(state_files):
        print(f"  ✅ 返回结果数量正确: {len(results)}")
    else:
        print(f"  ❌ 返回结果数量错误: 期望 {len(state_files)}, 实际 {len(results)}")
        return False

    for i, result in enumerate(results):
        if result.success:
            print(f"  样本{i+1}: reward={result.reward:.4f}, queue_before={result.queue_before}, queue_after={result.queue_after}")
        else:
            print(f"  ❌ 样本{i+1}失败: {result.error}")
            return False

    print("  ✅ 并行SUMO Reward计算验证通过")
    return True


def test_reward_chain():
    """测试9 & 10: Reward函数链组合和Early-return优化"""
    print("\n" + "=" * 60)
    print("测试9 & 10: Reward函数链组合和Early-return优化")
    print("=" * 60)

    # 加载配置
    config = GRPOTrainingConfig.from_yaml("config/grpo_config.yaml")

    # 创建reward链配置
    from grpo.reward import RewardChainConfig
    chain_config = RewardChainConfig(
        format_weight=config.reward.format_weight,
        tsc_weight=config.reward.tsc_weight,
        format_strict=config.format_reward.strict,
        format_partial=config.format_reward.partial,
        format_invalid=config.format_reward.invalid,
        extract_regex=config.format_reward.extract_regex
    )

    # 创建sumo配置
    sumo_config = SimpleNamespace(
        max_workers=config.sumo.max_workers,
        extend_seconds=config.sumo.extend_seconds,
        reward_scale=config.sumo.reward_scale,
        port_range=config.sumo.port_range,
    )

    # 测试用例1: 严格格式 + Mock TSC reward
    print("\n  测试用例1: 严格格式（Mock TSC reward）")
    prompt = '{"test": "prompt"}'
    output = '{"extend": "yes"}'
    state_file = None  # 不需要实际文件

    # Mock TSC reward函数
    def mock_tsc_fn(p, o, s, cfg):
        return [0.5]

    result, info = compute_reward(
        prompt, output, state_file,
        chain_config, sumo_config, tsc_reward_fn=mock_tsc_fn
    )

    expected = config.reward.format_weight * config.format_reward.strict + config.reward.tsc_weight * 0.5
    if abs(result - expected) < 0.001:
        print(f"    ✅ reward正确: {result:.4f} (format: {config.format_reward.strict}, tsc: 0.5)")
    else:
        print(f"    ❌ reward错误: {result:.4f} (期望: {expected:.4f})")
        return False

    # 测试用例2: Early-return（无效格式，跳过TSC）
    print("\n  测试用例2: Early-return优化（无效格式）")
    output_invalid = "invalid text"

    result, info = compute_reward(
        prompt, output_invalid, state_file,
        chain_config, sumo_config, tsc_reward_fn=mock_tsc_fn
    )

    expected = config.reward.format_weight * config.format_reward.invalid  # 只有format reward，没有TSC
    if abs(result - expected) < 0.001:
        print(f"    ✅ Early-return成功: {result:.4f} (仅format reward: {config.format_reward.invalid})")
        print(f"    ✅ 跳过了TSC仿真计算")
    else:
        print(f"    ❌ Early-return失败: {result:.4f} (期望: {expected:.4f})")
        return False

    print("\n  ✅ Reward函数链组合和Early-return验证通过")
    return True


def test_batch_compute_reward():
    """测试11: 批量Reward计算"""
    print("\n" + "=" * 60)
    print("测试11: 批量Reward计算")
    print("=" * 60)

    # 加载配置
    config = GRPOTrainingConfig.from_yaml("config/grpo_config.yaml")

    from grpo.reward import RewardChainConfig
    chain_config = RewardChainConfig(
        format_weight=config.reward.format_weight,
        tsc_weight=config.reward.tsc_weight,
        format_strict=config.format_reward.strict,
        format_partial=config.format_reward.partial,
        format_invalid=config.format_reward.invalid,
        extract_regex=config.format_reward.extract_regex
    )

    # 创建sumo配置
    sumo_config = SimpleNamespace(
        max_workers=config.sumo.max_workers,
        extend_seconds=config.sumo.extend_seconds,
        reward_scale=config.sumo.reward_scale,
        port_range=config.sumo.port_range,
    )

    # 准备批量输入
    prompts = ["test"] * 3
    outputs = [
        '{"extend": "yes"}',      # 严格格式
        'Decision: {"extend": "no"}',  # 部分格式
        'invalid text'            # 无效格式
    ]
    state_files = [None] * 3

    # Mock TSC reward函数
    def mock_tsc_fn(prompts, outputs, state_files, config):
        return [0.3, 0.2, 0.1]

    results, stats = batch_compute_reward(
        prompts, outputs, state_files,
        chain_config, sumo_config, tsc_reward_fn=mock_tsc_fn
    )

    print(f"  批量计算 {len(prompts)} 个样本的reward:")
    for i, result in enumerate(results):
        print(f"    样本{i+1}: {result:.4f}")

    # 验证结果数量
    if len(results) == len(prompts):
        print(f"  ✅ 返回结果数量正确: {len(results)}")
    else:
        print(f"  ❌ 返回结果数量错误")
        return False

    # 验证第一个样本（严格格式）
    expected_0 = config.reward.format_weight * config.format_reward.strict + config.reward.tsc_weight * 0.3
    if abs(results[0] - expected_0) < 0.001:
        print(f"  ✅ 样本1 reward正确")
    else:
        print(f"  ❌ 样本1 reward错误")
        return False

    print("  ✅ 批量Reward计算验证通过")
    return True


def main():
    """运行所有测试"""
    print("=" * 60)
    print("综合功能测试（测试8-11）")
    print("=" * 60)

    results = {}

    # 测试8: 并行SUMO Reward计算
    try:
        results['test8'] = test_parallel_sumo_calculator()
    except Exception as e:
        print(f"❌ 测试8异常: {e}")
        results['test8'] = False

    # 测试9 & 10: Reward函数链组合和Early-return
    try:
        results['test9_10'] = test_reward_chain()
    except Exception as e:
        print(f"❌ 测试9&10异常: {e}")
        results['test9_10'] = False

    # 测试11: 批量Reward计算
    try:
        results['test11'] = test_batch_compute_reward()
    except Exception as e:
        print(f"❌ 测试11异常: {e}")
        results['test11'] = False

    # 汇总结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)

    passed = sum(1 for v in results.values() if v is True)
    failed = sum(1 for v in results.values() if v is False)
    skipped = sum(1 for v in results.values() if v is None)

    print(f"  测试8 (并行SUMO): {results.get('test8', 'N/A')}")
    print(f"  测试9&10 (Reward链&Early-return): {results.get('test9_10', 'N/A')}")
    print(f"  测试11 (批量计算): {results.get('test11', 'N/A')}")
    print()
    print(f"  通过: {passed}, 失败: {failed}, 跳过: {skipped}")

    if failed == 0:
        print("\n✅ 所有完成的测试通过")
        return True
    else:
        print(f"\n❌ {failed} 个测试失败")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
