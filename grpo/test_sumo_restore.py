#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SUMO仿真从状态恢复测试脚本

验证TSC reward计算能够从SUMO状态文件恢复仿真，执行决策，并计算排队数变化
"""

import sys
import os
import json
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from grpo.sumo_reward import calculate_tsc_reward_single, TSCResult
from types import SimpleNamespace


def test_sumo_restore_from_state():
    """测试SUMO仿真从状态恢复"""
    print("=" * 60)
    print("SUMO仿真从状态恢复测试")
    print("=" * 60)

    # 查找测试数据
    dataset_path = "data/grpo_datasets/arterial4x4_99/grpo_dataset.json"

    if not os.path.exists(dataset_path):
        print(f"❌ 测试数据不存在: {dataset_path}")
        print("   请先运行数据生成脚本创建GRPO数据集")
        return False

    # 读取第一条数据
    print(f"\n1. 读取测试数据: {dataset_path}")
    with open(dataset_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if len(data) == 0:
        print("❌ 数据集为空")
        return False

    # 获取第一条数据
    sample = data[0]
    print(f"   ID: {sample['id']}")
    print(f"   scenario: {sample['scenario']}")
    print(f"   junction_id: {sample['junction_id']}")
    print(f"   state_file: {sample['state_file']}")

    # 构建完整路径
    state_file = os.path.join(
        "data/grpo_datasets",
        sample['scenario'],
        sample['state_file']
    )

    if not os.path.exists(state_file):
        print(f"❌ 状态文件不存在: {state_file}")
        return False

    print(f"   完整路径: {state_file}")
    print(f"   ✅ 状态文件存在")

    # 构建prompt（模拟GRPO训练时的prompt格式）
    prompt_data = {
        "crossing_id": sample['junction_id'],
        "state": {
            "current_phase_id": sample['current_phase_id']
        },
        "phase_order": sample['phase_order']
    }
    prompt = json.dumps(prompt_data, ensure_ascii=False)

    # 创建配置
    # 根据scenario推断sumocfg路径
    scenario_dir = f"sumo_simulation/environments/{sample['scenario']}"
    sumocfg_path = os.path.join(scenario_dir, f"{sample['scenario'].split('_')[0]}.sumocfg")

    if not os.path.exists(sumocfg_path):
        # 尝试其他可能的文件名
        import glob
        sumocfg_files = glob.glob(os.path.join(scenario_dir, "*.sumocfg"))
        if sumocfg_files:
            sumocfg_path = sumocfg_files[0]
        else:
            print(f"❌ 找不到sumocfg文件: {scenario_dir}")
            return False

    print(f"   sumocfg: {sumocfg_path}")

    config = SimpleNamespace(
        extend_seconds=5,
        reward_scale=10.0,
        sumocfg_path=sumocfg_path,
    )

    # 测试决策：延长相位
    print("\n2. 测试决策: yes (延长相位)")
    result_yes = calculate_tsc_reward_single(
        state_file=state_file,
        prompt=prompt,
        decision="yes",
        config=config
    )

    if result_yes.success:
        print(f"   ✅ 仿真成功")
        print(f"   queue_before: {result_yes.queue_before}")
        print(f"   queue_after:  {result_yes.queue_after}")
        print(f"   delta:        {result_yes.delta}")
        print(f"   reward:       {result_yes.reward:.4f}")
    else:
        print(f"   ❌ 仿真失败: {result_yes.error}")
        return False

    # 测试决策：切换相位
    print("\n3. 测试决策: no (切换相位)")
    result_no = calculate_tsc_reward_single(
        state_file=state_file,
        prompt=prompt,
        decision="no",
        config=config
    )

    if result_no.success:
        print(f"   ✅ 仿真成功")
        print(f"   queue_before: {result_no.queue_before}")
        print(f"   queue_after:  {result_no.queue_after}")
        print(f"   delta:        {result_no.delta}")
        print(f"   reward:       {result_no.reward:.4f}")
    else:
        print(f"   ❌ 仿真失败: {result_no.error}")
        return False

    # 验证reward在[-1, 1]范围内
    print("\n4. 验证reward范围")
    if -1.0 <= result_yes.reward <= 1.0:
        print(f"   ✅ yes决策reward在[-1, 1]范围内: {result_yes.reward:.4f}")
    else:
        print(f"   ❌ yes决策reward超出范围: {result_yes.reward}")
        return False

    if -1.0 <= result_no.reward <= 1.0:
        print(f"   ✅ no决策reward在[-1, 1]范围内: {result_no.reward:.4f}")
    else:
        print(f"   ❌ no决策reward超出范围: {result_no.reward}")
        return False

    # 验证排队数为非负整数
    print("\n5. 验证排队数合理性")
    if result_yes.queue_before >= 0 and result_yes.queue_after >= 0:
        print(f"   ✅ yes决策排队数为非负")
    else:
        print(f"   ❌ yes决策排队数为负")
        return False

    if result_no.queue_before >= 0 and result_no.queue_after >= 0:
        print(f"   ✅ no决策排队数为非负")
    else:
        print(f"   ❌ no决策排队数为负")
        return False

    print("\n" + "=" * 60)
    print("✅ SUMO仿真从状态恢复验证通过")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_sumo_restore_from_state()
    sys.exit(0 if success else 1)
