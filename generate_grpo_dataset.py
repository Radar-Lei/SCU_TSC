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
from typing import Any, Dict, List, Tuple
from datasets import Dataset
from pathlib import Path
import multiprocessing as mp
from functools import partial

# 添加项目路径
sumo_sim_path = os.path.join(os.getcwd(), 'sumo_simulation')
if sumo_sim_path not in sys.path:
    sys.path.insert(0, sumo_sim_path)

from sumo_simulator import SUMOSimulator

# 添加 scu_tsc_newprompt 到路径
sys.path.insert(0, os.getcwd())
from scu_tsc_newprompt.phase_parser import get_net_phase_minmax_one_based, get_phase_order_one_based, get_green_phase_order_one_based
from scu_tsc_newprompt.constraint_sampler import sample_phase_limits_hybrid
from scu_tsc_newprompt.prompt_builder import (
    build_cycle_predict_input_json,
    wrap_prompt_with_markers,
    build_signal_step_input_json,
    wrap_signal_step_prompt,
    build_extend_decision_input_json,
    wrap_extend_decision_prompt,
)


# ==================== 配置 ====================
CONFIG = {
    'gui': False,
    'warmup_steps': 80,
    'steps_per_tl': 20,          # 每个信号灯采样多少个时间步
    'steps_per_tl_signal_step': 10,
    'steps_per_tl_extend_decision': 10,
    'max_tl_per_scenario': 5,    # 每个场景最多取多少个信号灯（限制 dataset 大小）
    'recent_cycles_maxlen': 12,
    'state_dir': 'grpo_states',  # SUMO state 保存目录
    'output_dir': 'grpo_dataset', # dataset 输出目录
    'priority_scenarios': ['cologne8', 'ingolstadt21'],  # 优先采样的场景
    'skip_tl_ids': [],     # 跳过的信号灯
    'num_workers': 8,            # 并行 worker 数量（建议 CPU 核心数的 50-75%）
    'dataset_mode': 'two_scenarios',  # 'cycle_predict' | 'two_scenarios'
    'decision_lead_sec': 10,
    'phase_duration_scale_range': (0.7, 1.3),
    'extend_min_green_range': (5, 20),
    'extend_max_green_range': (45, 120),
    'extend_wait_time_range': (5, 25),
    'parallel_port_base': 30000,  # 并行端口基址（worker_i 使用 base + i*100 范围内的端口）
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


def discover_sumo_scenarios(sumo_root: str) -> Dict[str, Dict]:
    """从 sumo_simulation/ 下发现可用场景"""
    scenarios: Dict[str, Dict] = {}
    if not os.path.isdir(sumo_root):
        print(f"警告: sumo_simulation 目录不存在: {sumo_root}")
        return scenarios

    for name in sorted(os.listdir(sumo_root)):
        scenario_dir = os.path.join(sumo_root, name)
        if not os.path.isdir(scenario_dir) or name.startswith('.'):
            continue
        if name in {"sumo_sim", "__pycache__"}:
            continue

        sumocfg = None
        net_xml = None

        for f in os.listdir(scenario_dir):
            if f.endswith('.sumocfg'):
                sumocfg = os.path.join(scenario_dir, f)
                break

        for f in os.listdir(scenario_dir):
            if f.endswith('.net.xml'):
                net_xml = os.path.join(scenario_dir, f)
                break

        if sumocfg and net_xml:
            tl_ids = extract_traffic_light_ids(net_xml)
            if tl_ids:
                scenarios[name] = {
                    'sumocfg': sumocfg,
                    'net': net_xml,
                    'tl_ids': tl_ids,
                }

    return scenarios


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


def _is_green_phase(phase_state: str) -> bool:
    if not phase_state:
        return False
    return ("G" in phase_state) or ("g" in phase_state)


def _get_current_phase_state(simulator: SUMOSimulator, tl_id: str) -> Tuple[int, str]:
    info = simulator.get_phase_info(tl_id)
    current_idx = int(info.get('current_phase_index', 0))
    phase_states = info.get('phase_states', [])
    state = phase_states[current_idx] if current_idx < len(phase_states) else ""
    return current_idx, state


def _build_phase_lane_map(simulator: SUMOSimulator, tl_id: str, phase_ids: List[int]) -> Dict[str, List[str]]:
    phase_lane_map: Dict[str, List[str]] = {}
    for phase_id in phase_ids:
        phase_idx = phase_id - 1
        lanes = simulator.get_phase_controlled_lanes(tl_id, phase_idx).get('incoming_lanes', [])
        phase_lane_map[str(phase_id)] = list(lanes)
    return phase_lane_map


def _randomize_tl_program_durations(
    tl_id: str,
    scale_range: Tuple[float, float],
    rng: random.Random,
) -> List[int]:
    """
    随机缩放信号灯程序的相位时长，并返回修改后的durations列表（用于回放时复现）。
    
    Returns:
        List[int]: 各相位的duration列表（秒）；失败时返回空列表
    """
    import traci

    try:
        logics = traci.trafficlight.getAllProgramLogics(tl_id)
        if not logics:
            return []
        logic = logics[0]
        phases = []
        durations = []
        for ph in logic.phases:
            scale = rng.uniform(scale_range[0], scale_range[1])
            new_dur = max(1, int(round(ph.duration * scale)))
            phases.append(traci.trafficlight.Phase(new_dur, ph.state, ph.minDur, ph.maxDur, ph.next))
            durations.append(new_dur)
        new_logic = traci.trafficlight.Logic(
            logic.programID,
            logic.type,
            logic.currentPhaseIndex,
            phases,
            logic.subParameter,
        )
        traci.trafficlight.setProgramLogic(tl_id, new_logic)
        return durations
    except Exception:
        # 若修改失败，保持默认配时
        return []


def _init_phase_tracking(simulator: SUMOSimulator, tl_id: str) -> Dict[str, Any]:
    import traci

    phase_idx, phase_state = _get_current_phase_state(simulator, tl_id)
    lanes = simulator.get_phase_controlled_lanes(tl_id, phase_idx).get('incoming_lanes', [])
    lane_prev_ids = {}
    for ln in lanes:
        try:
            lane_prev_ids[ln] = set(traci.lane.getLastStepVehicleIDs(ln))
        except Exception:
            lane_prev_ids[ln] = set()
    return {
        "phase_idx": phase_idx,
        "phase_state": phase_state,
        "phase_start_time": float(traci.simulation.getTime()),
        "passed_total": 0.0,
        "lane_prev_ids": lane_prev_ids,
    }


def _step_and_track(simulator: SUMOSimulator, tl_id: str, track: Dict[str, Any]):
    import traci

    simulator.step()
    current_time = float(traci.simulation.getTime())
    phase_idx, phase_state = _get_current_phase_state(simulator, tl_id)
    if phase_idx != track["phase_idx"]:
        track["phase_idx"] = phase_idx
        track["phase_state"] = phase_state
        track["phase_start_time"] = current_time
        track["passed_total"] = 0.0
        lanes = simulator.get_phase_controlled_lanes(tl_id, phase_idx).get('incoming_lanes', [])
        lane_prev_ids = {}
        for ln in lanes:
            try:
                lane_prev_ids[ln] = set(traci.lane.getLastStepVehicleIDs(ln))
            except Exception:
                lane_prev_ids[ln] = set()
        track["lane_prev_ids"] = lane_prev_ids
        return

    track["phase_state"] = phase_state
    if not _is_green_phase(phase_state):
        return

    passed_increment = 0.0
    for ln, prev_ids in track["lane_prev_ids"].items():
        try:
            curr_ids = set(traci.lane.getLastStepVehicleIDs(ln))
        except Exception:
            curr_ids = set()
        passed_increment += float(len(prev_ids - curr_ids))
        track["lane_prev_ids"][ln] = curr_ids
    track["passed_total"] += passed_increment


def _collect_phase_metrics_now(
    simulator: SUMOSimulator,
    tl_id: str,
    phase_ids: List[int],
    current_phase_id: int,
    current_phase_passed_total: float,
) -> List[Dict[str, Any]]:
    import traci

    metrics = []
    for phase_id in phase_ids:
        phase_idx = phase_id - 1
        lanes = simulator.get_phase_controlled_lanes(tl_id, phase_idx).get('incoming_lanes', [])
        if lanes:
            total_queue = 0.0
            for ln in lanes:
                try:
                    total_queue += traci.lane.getLastStepHaltingNumber(ln)
                except Exception:
                    pass
            avg_queue = total_queue / max(1, len(lanes))
        else:
            avg_queue = 0.0
        passed = current_phase_passed_total if phase_id == current_phase_id else 0.0
        metrics.append({
            "phase_id": int(phase_id),
            "avg_queue_veh": float(round(avg_queue, 3)),
            "avg_passed_veh_in_current_green": float(round(passed, 3)),
        })
    return metrics


def _sample_phase_limits_uniform(
    phase_order: List[int],
    rng: random.Random,
    min_range: Tuple[int, int],
    max_range: Tuple[int, int],
) -> Dict[str, Dict[str, int]]:
    limits: Dict[str, Dict[str, int]] = {}
    min_lo, min_hi = min_range
    max_lo, max_hi = max_range
    for phase_id in phase_order:
        mn = rng.randint(min_lo, min_hi)
        mx = rng.randint(max_lo, max_hi)
        if mx <= mn + 5:
            mx = mn + 6
        limits[str(phase_id)] = {"min_green": int(mn), "max_green": int(mx)}
    return limits


def build_user_prompt(payload: dict) -> str:
    """构建用户 prompt"""
    return wrap_prompt_with_markers(payload) + "\n\n" + USER_INSTRUCTIONS


def generate_dataset_for_one_tl(
    scenario_name: str,
    tl_id: str,
    env_info: dict,
    state_root: str,
    port: int = None,
) -> List[dict]:
    """为一个信号灯生成 dataset 样本
    
    Args:
        port: 指定的 SUMO 端口（用于避免并行冲突）
    """
    
    simulator = SUMOSimulator(
        config_file=env_info['sumocfg'],
        junctions_file=None,
        gui=CONFIG['gui'],
        port=port,
    )
    
    if not simulator.start_simulation():
        print(f"✗ 启动失败: {scenario_name}/{tl_id}")
        return []

    # warmup
    for _ in range(CONFIG['warmup_steps']):
        if simulator.is_connected():
            simulator.step()

    # 解析相位信息（只保留绿灯相位）
    phase_order = get_green_phase_order_one_based(env_info['net'], tl_id)
    if not phase_order:
        print(f"✗ 无有效绿灯相位: {scenario_name}/{tl_id}")
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


def generate_dataset_for_one_tl_two_scenarios(
    scenario_name: str,
    tl_id: str,
    env_info: dict,
    state_root: str,
    port: int = None,
) -> List[dict]:
    """为一个信号灯生成两大场景 dataset 样本
    
    Args:
        port: 指定的 SUMO 端口（用于避免并行冲突）
    """
    import traci

    simulator = SUMOSimulator(
        config_file=env_info['sumocfg'],
        junctions_file=None,
        gui=CONFIG['gui'],
        additional_options=['--device.rerouting.probability', '0'],  # 禁用动态重路由
        port=port,
    )

    if not simulator.start_simulation():
        print(f"✗ 启动失败: {scenario_name}/{tl_id}")
        return []

    for _ in range(CONFIG['warmup_steps']):
        if simulator.is_connected():
            simulator.step()

    phase_order = get_green_phase_order_one_based(env_info['net'], tl_id)
    if not phase_order:
        print(f"✗ 无有效绿灯相位: {scenario_name}/{tl_id}")
        simulator.close()
        return []

    phase_ids = list(phase_order)
    phase_lane_map = _build_phase_lane_map(simulator, tl_id, phase_ids)

    state_dir = os.path.join(state_root, scenario_name)
    os.makedirs(state_dir, exist_ok=True)

    samples: List[dict] = []
    rng_base = random.Random(hash(scenario_name) ^ hash(tl_id))
    
    # Helper: check if all phases have 0 queue and 0 passed vehicles (empty traffic)
    def _is_empty_traffic_sample(phase_metrics: List[Dict[str, Any]]) -> bool:
        """
        Returns True if all phases have avg_queue_veh == 0 and avg_passed_veh_in_current_green == 0.
        """
        for m in phase_metrics:
            if m.get('avg_queue_veh', 0) > 0 or m.get('avg_passed_veh_in_current_green', 0) > 0:
                return False
        return True

    # 初始化相位跟踪
    track = _init_phase_tracking(simulator, tl_id)

    # ========== 场景1: signal_step ==========
    steps_signal = CONFIG.get('steps_per_tl_signal_step', CONFIG['steps_per_tl'])
    decision_lead_sec = int(CONFIG.get('decision_lead_sec', 10))
    scale_range = CONFIG.get('phase_duration_scale_range', (0.7, 1.3))

    for step_idx in range(steps_signal):
        if not simulator.is_connected():
            break

        rng = random.Random((hash(scenario_name) ^ hash(tl_id) ^ step_idx) & 0xFFFFFFFF)
        tls_phase_durations = _randomize_tl_program_durations(tl_id, scale_range, rng)

        # 推进到绿灯结束前 decision_lead_sec 秒
        max_guard_steps = 600
        guard = 0
        while guard < max_guard_steps:
            phase_idx, phase_state = _get_current_phase_state(simulator, tl_id)
            remaining = traci.trafficlight.getNextSwitch(tl_id) - traci.simulation.getTime()
            if _is_green_phase(phase_state) and remaining <= decision_lead_sec:
                break
            _step_and_track(simulator, tl_id, track)
            guard += 1

        if guard >= max_guard_steps:
            continue

        phase_idx, phase_state = _get_current_phase_state(simulator, tl_id)
        current_phase_id = phase_idx + 1
        remaining = traci.trafficlight.getNextSwitch(tl_id) - traci.simulation.getTime()
        decision_remaining_sec = int(max(0, round(remaining)))
        
        # 用 track 计算 elapsed（更稳定）
        current_elapsed = int(round(traci.simulation.getTime() - track["phase_start_time"]))
        current_planned_green = current_elapsed + decision_remaining_sec

        phase_metrics_now = _collect_phase_metrics_now(
            simulator,
            tl_id,
            phase_ids,
            current_phase_id,
            track["passed_total"],
        )

        payload = build_signal_step_input_json(
            scenario_name=scenario_name,
            tl_id=tl_id,
            phase_ids=phase_ids,
            phase_lane_map=phase_lane_map,
            current_phase_id=current_phase_id,
            current_phase_elapsed_sec=current_elapsed,
            current_phase_planned_green_sec=current_planned_green,
            phase_metrics_now=phase_metrics_now,
        )

        full_prompt = wrap_signal_step_prompt(payload)
        messages = [
            {"role": "system", "content": "You are a traffic signal control expert. Output only valid JSON without any explanation."},
            {"role": "user", "content": full_prompt}
        ]

        # Filter out 90% of "empty traffic" samples
        if _is_empty_traffic_sample(phase_metrics_now):
            if rng.random() > 0.1:  # Keep only 10%
                for _ in range(5):
                    _step_and_track(simulator, tl_id, track)
                continue

        current_time = traci.simulation.getTime()
        state_filename = f"{tl_id}_signal_step_{step_idx}_t{int(current_time)}.xml"
        state_path = os.path.join(state_dir, state_filename)
        traci.simulation.saveState(state_path)

        samples.append({
            'prompt': messages,
            'state_path': state_path,
            'scenario': scenario_name,
            'tl_id': tl_id,
            'task_type': 'signal_step',
            'phase_ids': phase_ids,
            'phase_lane_map': phase_lane_map,
            'decision_lead_sec': decision_lead_sec,
            'decision_remaining_sec': decision_remaining_sec,
            'current_phase_elapsed_sec': current_elapsed,
            'current_phase_planned_green_sec': current_planned_green,
            'sumocfg_path': env_info['sumocfg'],
            'tls_phase_durations': tls_phase_durations,
        })

        # 轻微推进仿真，避免同一状态
        for _ in range(5):
            _step_and_track(simulator, tl_id, track)

    # ========== 场景2: extend_decision ==========
    steps_extend = CONFIG.get('steps_per_tl_extend_decision', CONFIG['steps_per_tl'])
    min_range = CONFIG.get('extend_min_green_range', (5, 20))
    max_range = CONFIG.get('extend_max_green_range', (25, 120))
    wait_range = CONFIG.get('extend_wait_time_range', (5, 25))

    for step_idx in range(steps_extend):
        if not simulator.is_connected():
            break

        rng = random.Random((hash(scenario_name) ^ hash(tl_id) ^ (step_idx + 999)) & 0xFFFFFFFF)
        phase_limits = _sample_phase_limits_uniform(phase_order, rng, min_range, max_range)
        wait_time = rng.randint(wait_range[0], wait_range[1])

        # 目标决策时刻
        current_phase_id = track["phase_idx"] + 1
        limits = phase_limits.get(str(current_phase_id), None)
        if not limits:
            target_elapsed = rng.randint(5, 20)
        else:
            min_green = int(limits["min_green"])
            max_green = int(limits["max_green"])
            if step_idx == 0:
                target_elapsed = min_green
            else:
                target_elapsed = rng.randint(min_green, max_green)

        # 推进到决策时刻（确保当前相位持续时间足够）
        max_guard_steps = 600
        guard = 0
        while guard < max_guard_steps:
            phase_idx, phase_state = _get_current_phase_state(simulator, tl_id)
            if not _is_green_phase(phase_state):
                _step_and_track(simulator, tl_id, track)
                guard += 1
                continue

            elapsed = int(round(traci.simulation.getTime() - track["phase_start_time"]))
            if elapsed >= target_elapsed:
                break
            # 适当延长当前相位，保证能到达目标时刻
            traci.trafficlight.setPhaseDuration(tl_id, max(5, target_elapsed - elapsed))
            _step_and_track(simulator, tl_id, track)
            guard += 1

        if guard >= max_guard_steps:
            continue

        current_phase_id = track["phase_idx"] + 1
        elapsed = int(round(traci.simulation.getTime() - track["phase_start_time"]))
        
        # 记录当前 TLS 程序的 durations（用于回放时复现）
        try:
            logics = traci.trafficlight.getAllProgramLogics(tl_id)
            tls_phase_durations = [int(ph.duration) for ph in logics[0].phases] if logics else []
        except Exception:
            tls_phase_durations = []

        phase_metrics_now = _collect_phase_metrics_now(
            simulator,
            tl_id,
            phase_ids,
            current_phase_id,
            track["passed_total"],
        )

        payload = build_extend_decision_input_json(
            scenario_name=scenario_name,
            tl_id=tl_id,
            phase_order=phase_order,
            phase_limits=phase_limits,
            phase_lane_map=phase_lane_map,
            current_phase_id=current_phase_id,
            current_phase_elapsed_sec=elapsed,
            wait_time_for_phase_change=wait_time,
            phase_metrics_now=phase_metrics_now,
        )

        full_prompt = wrap_extend_decision_prompt(payload)
        messages = [
            {"role": "system", "content": "You are a traffic signal control expert. Output only valid JSON without any explanation."},
            {"role": "user", "content": full_prompt}
        ]

        # Filter out 90% of "empty traffic" samples
        if _is_empty_traffic_sample(phase_metrics_now):
            if rng.random() > 0.1:  # Keep only 10%
                for _ in range(5):
                    _step_and_track(simulator, tl_id, track)
                continue

        current_time = traci.simulation.getTime()
        state_filename = f"{tl_id}_extend_decision_{step_idx}_t{int(current_time)}.xml"
        state_path = os.path.join(state_dir, state_filename)
        traci.simulation.saveState(state_path)

        samples.append({
            'prompt': messages,
            'state_path': state_path,
            'scenario': scenario_name,
            'tl_id': tl_id,
            'task_type': 'extend_decision',
            'phase_order': phase_order,
            'phase_limits': phase_limits,
            'phase_lane_map': phase_lane_map,
            'wait_time_for_phase_change': wait_time,
            'current_phase_elapsed_sec': elapsed,
            'sumocfg_path': env_info['sumocfg'],
            'tls_phase_durations': tls_phase_durations,
        })

        for _ in range(5):
            _step_and_track(simulator, tl_id, track)

    simulator.close()
    return samples


def _worker_process_tl(args: Tuple) -> Tuple[str, str, List[dict]]:
    """
    Worker 函数：处理单个 (scenario, tl_id)
    用于 multiprocessing.Pool
    
    Returns:
        (scenario_name, tl_id, samples)
    """
    scenario_name, tl_id, env_info, state_root, dataset_mode, worker_id, port_base = args
    
    # 为该 worker 分配固定端口
    assigned_port = port_base + worker_id * 100
    
    try:
        if dataset_mode == 'two_scenarios':
            samples = generate_dataset_for_one_tl_two_scenarios(
                scenario_name=scenario_name,
                tl_id=tl_id,
                env_info=env_info,
                state_root=state_root,
                port=assigned_port,
            )
        else:
            samples = generate_dataset_for_one_tl(
                scenario_name=scenario_name,
                tl_id=tl_id,
                env_info=env_info,
                state_root=state_root,
                port=assigned_port,
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
    
    dataset_mode = CONFIG.get('dataset_mode', 'cycle_predict')

    # 发现场景（仅使用 sumo_simulation/environments）
    environments_root = os.path.join(os.getcwd(), 'sumo_simulation', 'environments')
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
    # 使用 spawn 上下文和固定端口池
    port_base = CONFIG.get('parallel_port_base', 30000)
    worker_args = []
    for worker_id, (scenario_name, tl_id) in enumerate(all_pairs):
        env_info = available_envs[scenario_name]
        worker_args.append((scenario_name, tl_id, env_info, state_root, dataset_mode, worker_id % num_workers, port_base))
    
    all_samples = []
    
    # 并行处理
    if num_workers > 1:
        print(f"\n开始并行生成（{num_workers} workers）...")
        print(f"端口范围: {port_base}-{port_base + num_workers * 100}")
        
        # 使用 spawn 上下文避免 fork 的线程安全问题
        mp_context = mp.get_context("spawn")
        with mp_context.Pool(processes=num_workers) as pool:
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
