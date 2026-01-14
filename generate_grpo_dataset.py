"""
离线生成 GRPO 训练 Dataset

遍历场景/信号灯/时间步，为每个时间点：
1. 收集历史数据并构建 prompt
2. 保存 SUMO state 到磁盘
3. 记录 dataset 条目（prompt + state_path + metadata）

生成的 dataset 供标准 Unsloth GRPOTrainer 使用。
"""

import os
import sys
import json
import random
import datetime
import xml.etree.ElementTree as ET
from collections import deque
from typing import Dict, List, Tuple
from datasets import Dataset
from pathlib import Path
from multiprocessing import Pool, cpu_count
from functools import partial

# 添加项目路径
sumo_sim_path = os.path.join(os.getcwd(), 'sumo_simulation')
if sumo_sim_path not in sys.path:
    sys.path.insert(0, sumo_sim_path)

from sumo_simulator import SUMOSimulator

# 添加 scu_tsc_newprompt 到路径
sys.path.insert(0, os.getcwd())
from scu_tsc_newprompt.phase_parser import get_net_phase_minmax_one_based, get_phase_order_one_based
from scu_tsc_newprompt.constraint_sampler import sample_phase_limits_hybrid
from scu_tsc_newprompt.prompt_builder import build_cycle_predict_input_json, wrap_prompt_with_markers


# ==================== 配置 ====================
CONFIG = {
    'gui': False,
    'warmup_steps': 80,
    'steps_per_tl': 20,          # 每个信号灯采样多少个时间步
    'max_tl_per_scenario': 5,    # 每个场景最多取多少个信号灯（限制 dataset 大小）
    'recent_cycles_maxlen': 12,
    'state_dir': 'grpo_states',  # SUMO state 保存目录
    'output_dir': 'grpo_dataset', # dataset 输出目录
    'priority_scenarios': ['cologne8', 'ingolstadt21'],  # 优先采样的场景
    'skip_tl_ids': [],     # 跳过的信号灯
    'num_workers': 4,            # 并行 worker 数量（建议 CPU 核心数的 50-75%）
}

SYSTEM_PROMPT = """你是交通信号配时优化专家。
你将收到一个 JSON（用【cycle_predict_input_json】...【/cycle_predict_input_json】包裹）。
你的任务是：在满足硬约束前提下，输出下一周期各相位最终绿灯时间 final（单位：秒）。
注意：history 数据可能不完整（例如 only recent_cycles；yesterday_same_time/last_week_same_time 可能为 null），必须基于可用部分输出结果。
只输出最终 JSON 数组(list)，不要输出任何解释/过程。
"""

USER_INSTRUCTIONS = """任务（必须完成）：
1) 基于输入 JSON 的 history.* 历史数据，自行决定预测算法/模型/参数，预测"下一周期各相位需求强度"（仅在内部使用，不输出过程/中间值）。
2) 在满足硬约束前提下，输出下一周期各相位最终绿灯时间 final（单位：秒）。

要求（必须遵守）：
1) history 数据可能不完整（仅 recent_cycles；windows.yesterday_same_time / last_week_same_time 可能为 null）；这是正常情况，请基于可用部分完成预测，并且必须继续输出结果。
2) 若 history 中存在有效数据，请使用它完成预测并体现在结果中；不要忽略 history 数据随意分配。
3) 若 history 数据缺失/异常/几乎全为 0，仍需输出满足硬约束的可执行方案，但不得编造不存在的数据。
4) 只输出最终 JSON，不要输出任何解释/过程。

输出要求（必须严格遵守）：
1) 只输出最终 JSON（不要任何说明、不要 Markdown）。
2) JSON 顶层必须是数组(list)；数组长度必须等于相位数。
3) 数组元素必须为对象：{"phase_id": <int>, "final": <int>}；不允许输出其它字段。
4) phase_id 必须覆盖全部相位且不重复，并且顺序必须与 phase_order 完全一致。
"""


def discover_environments(environments_root: str) -> Dict[str, Dict]:
    """发现所有可用场景"""
    environments: Dict[str, Dict] = {}
    if not os.path.isdir(environments_root):
        print(f"警告: environments 目录不存在: {environments_root}")
        return environments

    for scenario_name in sorted(os.listdir(environments_root)):
        scenario_dir = os.path.join(environments_root, scenario_name)
        if not os.path.isdir(scenario_dir) or scenario_name.startswith('.'):
            continue

        sumocfg = None
        for f in os.listdir(scenario_dir):
            if f.endswith('.sumocfg'):
                sumocfg = os.path.join(scenario_dir, f)
                break

        net_xml = None
        for f in os.listdir(scenario_dir):
            if f.endswith('.net.xml'):
                net_xml = os.path.join(scenario_dir, f)
                break

        if sumocfg and net_xml:
            tl_ids = extract_traffic_light_ids(net_xml)
            if tl_ids:
                environments[scenario_name] = {
                    'sumocfg': sumocfg,
                    'net': net_xml,
                    'tl_ids': tl_ids,
                }

    return environments


def extract_traffic_light_ids(net_xml_path: str) -> List[str]:
    """从 net.xml 提取信号灯 ID"""
    tl_ids: List[str] = []
    try:
        for _event, elem in ET.iterparse(net_xml_path, events=("end",)):
            if elem.tag == "tlLogic":
                tl_id = elem.attrib.get("id")
                if tl_id and tl_id not in tl_ids:
                    tl_ids.append(tl_id)
                elem.clear()
    except Exception as e:
        print(f"解析 {net_xml_path} 失败: {e}")
    return tl_ids


def collect_phase_waits_snapshot(simulator: SUMOSimulator, tl_id: str, phase_order: List[int]) -> List[dict]:
    """收集当前时刻各相位的等待车辆数（作为 avg_wait 代理）"""
    import traci
    waits = []
    for phase_id in phase_order:
        phase_idx = phase_id - 1
        lanes = simulator.get_phase_controlled_lanes(tl_id, phase_idx).get('incoming_lanes', [])
        if not lanes:
            avg = 0.0
        else:
            total = 0.0
            for ln in lanes:
                try:
                    total += traci.lane.getLastStepHaltingNumber(ln)
                except Exception:
                    pass
            avg = total / max(1, len(lanes))
        waits.append({'phase_id': int(phase_id), 'avg_wait': float(round(avg, 2))})
    return waits


def build_user_prompt(payload: dict) -> str:
    """构建用户 prompt"""
    return wrap_prompt_with_markers(payload) + "\n\n" + USER_INSTRUCTIONS


def generate_dataset_for_one_tl(
    scenario_name: str,
    tl_id: str,
    env_info: dict,
    state_root: str,
) -> List[dict]:
    """为一个信号灯生成 dataset 样本"""
    
    simulator = SUMOSimulator(
        config_file=env_info['sumocfg'],
        junctions_file=None,
        gui=CONFIG['gui'],
    )
    
    if not simulator.start_simulation():
        print(f"✗ 启动失败: {scenario_name}/{tl_id}")
        return []

    # warmup
    for _ in range(CONFIG['warmup_steps']):
        if simulator.is_connected():
            simulator.step()

    # 解析相位信息
    phase_order = get_phase_order_one_based(env_info['net'], tl_id)
    if not phase_order:
        print(f"✗ 未解析到相位: {scenario_name}/{tl_id}")
        simulator.close()
        return []

    net_minmax = get_net_phase_minmax_one_based(env_info['net'], tl_id)
    recent_cycles_buf = deque(maxlen=CONFIG['recent_cycles_maxlen'])

    # 创建 state 目录
    state_dir = os.path.join(state_root, scenario_name)
    os.makedirs(state_dir, exist_ok=True)

    samples = []

    for step_idx in range(CONFIG['steps_per_tl']):
        if not simulator.is_connected():
            break

        # 随机化约束
        rng = random.Random((hash(scenario_name) ^ hash(tl_id) ^ step_idx) & 0xFFFFFFFF)
        phase_limits = sample_phase_limits_hybrid(phase_order, net_minmax, rng=rng)

        # 构建 prompt
        payload = build_cycle_predict_input_json(
            scenario_name=scenario_name,
            tl_id=tl_id,
            phase_order=phase_order,
            phase_limits=phase_limits,
            recent_cycles=list(recent_cycles_buf),
            include_windows_recent_past=True,
            windows_recent_past=None,
        )

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(payload)},
        ]

        # 保存 SUMO state（使用自定义路径）
        import traci
        current_time = traci.simulation.getTime()
        state_filename = f"{tl_id}_step{step_idx}_t{int(current_time)}.xml"
        state_path = os.path.join(state_dir, state_filename)
        traci.simulation.saveState(state_path)

        # 记录样本
        samples.append({
            'prompt': messages,
            'state_path': state_path,
            'scenario': scenario_name,
            'tl_id': tl_id,
            'phase_order': phase_order,
            'phase_limits': phase_limits,
            'step_idx': step_idx,
        })

        # 执行一个默认周期（推进仿真）
        waits = collect_phase_waits_snapshot(simulator, tl_id, phase_order)
        recent_cycles_buf.append({
            'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'phase_waits': waits,
        })

        # 执行默认方案（均分绿灯时间）
        for pid in phase_order:
            traci.trafficlight.setPhase(tl_id, pid - 1)
            for _ in range(20):  # 默认每相位 20 秒
                if simulator.is_connected():
                    simulator.step()

    simulator.close()
    return samples


def _worker_process_tl(args: Tuple) -> Tuple[str, str, List[dict]]:
    """
    Worker 函数：处理单个 (scenario, tl_id)
    用于 multiprocessing.Pool
    
    Returns:
        (scenario_name, tl_id, samples)
    """
    scenario_name, tl_id, env_info, state_root = args
    
    try:
        samples = generate_dataset_for_one_tl(
            scenario_name=scenario_name,
            tl_id=tl_id,
            env_info=env_info,
            state_root=state_root,
        )
        return (scenario_name, tl_id, samples)
    except Exception as e:
        print(f"✗ Worker 失败 [{scenario_name}/{tl_id}]: {e}")
        import traceback
        traceback.print_exc()
        return (scenario_name, tl_id, [])


def main(num_workers: int = None):
    """主函数：并行遍历场景/信号灯，生成 dataset
    
    Args:
        num_workers: 并行 worker 数量，None 则使用 CONFIG 中的值
    """
    if num_workers is None:
        num_workers = CONFIG.get('num_workers', 4)
    
    # 发现场景
    environments_root = os.path.join(os.getcwd(), 'sumo_simulation/environments')
    available_envs = discover_environments(environments_root)
    print(f"发现场景数: {len(available_envs)}")
    
    # 构建训练列表（优先场景排前）
    priority_scenarios = set(CONFIG['priority_scenarios'])
    skip_tl_ids = set(CONFIG['skip_tl_ids'])
    
    priority_pairs = []
    other_pairs = []
    
    for scenario_name, info in available_envs.items():
        tl_ids = info['tl_ids'][:CONFIG['max_tl_per_scenario']]
        for tl_id in tl_ids:
            if tl_id in skip_tl_ids:
                continue
            pair = (scenario_name, tl_id)
            if scenario_name in priority_scenarios:
                priority_pairs.append(pair)
            else:
                other_pairs.append(pair)
    
    random.shuffle(priority_pairs)
    random.shuffle(other_pairs)
    all_pairs = priority_pairs + other_pairs
    
    print(f"总训练组合数: {len(all_pairs)}")
    print(f"  优先场景: {len(priority_pairs)}")
    print(f"  其他场景: {len(other_pairs)}")
    print(f"  并行 workers: {num_workers}")
    
    # 创建输出目录
    state_root = CONFIG['state_dir']
    os.makedirs(state_root, exist_ok=True)
    
    # 准备参数列表（每个 worker 需要的参数）
    worker_args = []
    for scenario_name, tl_id in all_pairs:
        env_info = available_envs[scenario_name]
        worker_args.append((scenario_name, tl_id, env_info, state_root))
    
    all_samples = []
    
    # 并行处理
    if num_workers > 1:
        print(f"\n开始并行生成（{num_workers} workers）...")
        with Pool(processes=num_workers) as pool:
            # 使用 imap_unordered 可以边完成边处理结果
            results = pool.imap_unordered(_worker_process_tl, worker_args, chunksize=1)
            
            for i, (scenario_name, tl_id, samples) in enumerate(results, 1):
                all_samples.extend(samples)
                print(f"[{i}/{len(all_pairs)}] ✓ {scenario_name}/{tl_id}: {len(samples)} 个样本，累计 {len(all_samples)} 个")
    else:
        # 单进程模式（调试用）
        print("\n单进程模式...")
        for i, args in enumerate(worker_args, 1):
            scenario_name, tl_id, samples = _worker_process_tl(args)
            all_samples.extend(samples)
            print(f"[{i}/{len(all_pairs)}] ✓ {scenario_name}/{tl_id}: {len(samples)} 个样本，累计 {len(all_samples)} 个")
    
    # 转换为 HuggingFace Dataset
    print(f"\n生成 Dataset，总样本数: {len(all_samples)}")
    dataset = Dataset.from_list(all_samples)
    
    # 保存到磁盘
    output_dir = CONFIG['output_dir']
    dataset.save_to_disk(output_dir)
    print(f"✓ Dataset 已保存到: {output_dir}")
    
    # 打印统计信息
    print("\n=== Dataset 统计 ===")
    print(f"总样本数: {len(dataset)}")
    scenarios = set(s['scenario'] for s in all_samples)
    print(f"场景数: {len(scenarios)}")
    tl_ids = set(s['tl_id'] for s in all_samples)
    print(f"信号灯数: {len(tl_ids)}")
    
    return dataset


if __name__ == '__main__':
    main()
