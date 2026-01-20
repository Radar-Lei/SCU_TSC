"""
TSC GRPO Reward Function

用于标准 Unsloth GRPOTrainer 的 reward 计算函数。
在 reward 计算时：
1. 从 dataset 字段恢复 SUMO state
2. 解析 completion（JSON 格式的信号配时方案）
3. 使用 rollback 评估交通指标
4. 返回每个 completion 的 reward

关键：同一 prompt 的多个 completion 共享同一个 SUMO state checkpoint。
"""

import os
import sys
import torch
from typing import List, Dict, Any, Union
from collections import defaultdict, Counter
import json
import re
import multiprocessing as mp
from functools import partial
import atexit

# 添加项目路径
sumo_sim_path = os.path.join(os.getcwd(), 'sumo_simulation')
if sumo_sim_path not in sys.path:
    sys.path.insert(0, sumo_sim_path)

from sumo_simulator import SUMOSimulator

sys.path.insert(0, os.getcwd())
from scu_tsc_newprompt.rewards import (
    score_constraints_and_format,
    AdaptiveScaler,
    compute_sim_reward_adaptive,
    compute_total_reward,
)


# ==================== 全局配置 ====================
REWARD_CONFIG = {
    'gui': False,
    # SUMO 输出控制：False 时屏蔽 SUMO 启动/预热/step 日志（推荐训练时关闭）
    'sim_verbose': False,
    'w_passed': 1.0,
    'w_queue': 1.0,
    'w_proxy': 0.2,
    'w_sim': 1.5,
    'w_constraint': 1.5,
    # 'D0': 25.0,  # 软约束归一化尺度
    'alpha_passed': 0.5,
    'beta_queue': 1.0,
    'invalid_output_reward': -2.0,
    # Multi-reward mode (when using GRPOTrainer(reward_funcs=[sim, format]))
    'format_reward_valid': 0.0,
    'format_reward_invalid': -1.0,
    'sim_reward_clip_min': -1.0,
    'sim_reward_clip_max': 1.0,
    'parallel_workers': 16,  # 并行 SUMO worker 数量（使用固定端口池避免冲突）
    'parallel_port_base': 40000,  # 并行端口基址（worker_i 使用 base + i*100 范围内的端口）
    'green_sec_min': 1,     # signal_step 的 green_sec 下限
    'green_sec_max': 120,   # signal_step 的 green_sec 上限
}


# ==================== 全局 forkserver 进程池（常驻） ====================
# 使用 forkserver 模式避免 fork 的线程安全问题，同时避免 spawn 与 vLLM 的 CUDA 冲突
# Note: spawn 模式在 vLLM 环境下会导致 CUDA 重初始化死锁
try:
    _MP_CONTEXT = mp.get_context("forkserver")
except ValueError:
    # forkserver 不可用时回退到 fork
    _MP_CONTEXT = mp.get_context("fork")
_GLOBAL_MP_POOL = None  # 延迟初始化
_MP_POOL_INITIALIZED = False  # 标记是否已尝试初始化

# Worker 端口分配：每个 worker 获得一个固定端口
# 使用进程本地存储来保存 worker 的分配端口
_WORKER_PORT: Dict[str, int] = {}  # 进程本地变量（spawn 模式下每个 worker 独立）


# ==================== Reward Diagnostics ====================
_REWARD_DIAG: Dict[str, Any] = {
    "window_start_step": None,
    "window_total": 0,
    "window_invalid": 0,
    "window_total_by_task": Counter(),
    "window_invalid_by_task": Counter(),
    "window_reason_by_task": {},  # task_type -> Counter
    "last_batch_by_step": {},  # global_step -> dict
    "max_steps_kept": 300,
}


def reward_diag_snapshot(reset: bool = False) -> Dict[str, Any]:
    """
    Snapshot diagnostics accumulated since last reset.
    Designed to be called from a TrainerCallback on log events.
    """
    reason_by_task = {
        task: dict(counter)
        for task, counter in _REWARD_DIAG.get("window_reason_by_task", {}).items()
    }
    snap = {
        "window_start_step": _REWARD_DIAG.get("window_start_step"),
        "window_total": int(_REWARD_DIAG.get("window_total", 0)),
        "window_invalid": int(_REWARD_DIAG.get("window_invalid", 0)),
        "window_total_by_task": dict(_REWARD_DIAG.get("window_total_by_task", {})),
        "window_invalid_by_task": dict(_REWARD_DIAG.get("window_invalid_by_task", {})),
        "window_reason_by_task": reason_by_task,
    }
    if reset:
        _REWARD_DIAG["window_start_step"] = None
        _REWARD_DIAG["window_total"] = 0
        _REWARD_DIAG["window_invalid"] = 0
        _REWARD_DIAG["window_total_by_task"] = Counter()
        _REWARD_DIAG["window_invalid_by_task"] = Counter()
        _REWARD_DIAG["window_reason_by_task"] = {}
    return snap


def reward_diag_last(global_step: int) -> Union[Dict[str, Any], None]:
    """Return per-batch diagnostics stored for a given global_step."""
    try:
        val = _REWARD_DIAG.get("last_batch_by_step", {}).get(int(global_step))
        if val is None:
            val = _REWARD_DIAG.get("last_batch_latest")
        return val
    except Exception:
        return None


def _worker_initializer(worker_id: int, port_base: int):
    """
    Worker 初始化函数（在每个 worker 进程启动时调用）
    为该 worker 分配一个固定端口
    """
    global _WORKER_PORT
    assigned_port = port_base + worker_id * 100  # 每个 worker 分配 100 个端口的空间
    _WORKER_PORT["port"] = assigned_port
    # 静默初始化，不打印日志


def _get_worker_port() -> int:
    """获取当前 worker 的分配端口"""
    return _WORKER_PORT.get("port", None)


def _ensure_mp_pool_initialized():
    """确保全局进程池已初始化（延迟初始化，避免import时启动）"""
    global _GLOBAL_MP_POOL, _MP_POOL_INITIALIZED
    
    # 如果已经尝试过初始化（成功或失败），直接返回
    if _MP_POOL_INITIALIZED:
        return _GLOBAL_MP_POOL
    
    _MP_POOL_INITIALIZED = True
    
    if _GLOBAL_MP_POOL is None:
        num_workers = REWARD_CONFIG['parallel_workers']
        if num_workers > 0:
            port_base = REWARD_CONFIG.get('parallel_port_base', 20000)
            print(f"[tsc_reward_function] 初始化进程池，workers={num_workers}，端口范围={port_base}-{port_base + num_workers * 100}")
            
            try:
                # 改用 imap_unordered + 任务内分配端口的方式
                _GLOBAL_MP_POOL = _MP_CONTEXT.Pool(processes=num_workers)
                # 注册 atexit 钩子确保程序退出时清理
                atexit.register(_cleanup_mp_pool)
                print(f"[tsc_reward_function] 进程池初始化成功")
            except Exception as e:
                print(f"[tsc_reward_function] 进程池初始化失败，将使用串行模式: {e}")
                _GLOBAL_MP_POOL = None
    return _GLOBAL_MP_POOL


def _cleanup_mp_pool():
    """清理全局进程池"""
    global _GLOBAL_MP_POOL
    if _GLOBAL_MP_POOL is not None:
        try:
            print("[tsc_reward_function] 关闭进程池...")
            _GLOBAL_MP_POOL.close()
            _GLOBAL_MP_POOL.join()
            print("[tsc_reward_function] 进程池已关闭")
        except Exception as e:
            print(f"[tsc_reward_function] 进程池关闭失败: {e}")
        finally:
            _GLOBAL_MP_POOL = None


# ==================== Simulator 池管理 ====================
class SimulatorPool:
    """
    管理 SUMO simulator 实例的对象池。
    为每个 (scenario, sumocfg) 维护一个 simulator 实例，避免频繁创建/销毁。
    """
    
    def __init__(self):
        self._pool: Dict[str, SUMOSimulator] = {}
        self._scalers: Dict[str, AdaptiveScaler] = {}  # 每个 tl_id 一个 scaler
    
    def get_simulator(self, scenario: str, sumocfg: str) -> SUMOSimulator:
        """获取或创建 simulator"""
        key = f"{scenario}:{sumocfg}"
        
        if key not in self._pool:
            if REWARD_CONFIG.get("sim_verbose", False):
                print(f"[SimulatorPool] 创建新 simulator: {scenario}")
            sim = SUMOSimulator(
                config_file=sumocfg,
                junctions_file=None,
                gui=REWARD_CONFIG['gui'],
                additional_options=['--device.rerouting.probability', '0'],  # 禁用动态重路由
                verbose=bool(REWARD_CONFIG.get("sim_verbose", False)),
            )
            if not sim.start_simulation():
                raise RuntimeError(f"无法启动 SUMO simulator: {scenario}")
            self._pool[key] = sim
        
        return self._pool[key]
    
    def get_scaler(self, tl_id: str) -> AdaptiveScaler:
        """获取或创建 scaler"""
        if tl_id not in self._scalers:
            self._scalers[tl_id] = AdaptiveScaler()
        return self._scalers[tl_id]
    
    def close_all(self):
        """关闭所有 simulator"""
        for sim in self._pool.values():
            try:
                sim.close()
            except Exception as e:
                print(f"关闭 simulator 失败: {e}")
        self._pool.clear()
        self._scalers.clear()


# 全局 simulator 池
_GLOBAL_POOL = SimulatorPool()


# ==================== 评估辅助函数 ====================
def evaluate_plan_once_reward_fn(
    simulator: SUMOSimulator,
    tl_id: str,
    plan: List[dict]
) -> dict:
    """
    在当前 SUMO state 下执行一个信号配时方案并返回交通指标。
    
    Args:
        simulator: SUMO 仿真器实例
        tl_id: 信号灯 ID
        plan: 配时方案 [{"phase_id": int, "final": int}, ...]
    
    Returns:
        dict: {"passed_vehicles": float, "queue_vehicles": float, "total_queue_proxy": float, "sim_time": float}
    """
    import traci
    
    # 收集所有相位控制的 lanes
    phase_info = simulator.get_phase_info(tl_id)
    n = int(phase_info.get('num_phases', 0))
    all_lanes = set()
    for idx in range(n):
        all_lanes.update(simulator.get_phase_controlled_lanes(tl_id, idx).get('incoming_lanes', []))
    all_lanes = list(all_lanes)
    
    # 记录执行前的车辆
    vehicles_before = set()
    for ln in all_lanes:
        try:
            vehicles_before.update(traci.lane.getLastStepVehicleIDs(ln))
        except Exception:
            pass
    
    # 执行配时方案
    total_queue_proxy = 0.0
    for step in plan:
        pid = int(step['phase_id'])
        dur = int(step['final'])
        traci.trafficlight.setPhase(tl_id, pid - 1)
        for _ in range(max(0, dur)):
            traci.simulationStep()
            q = 0.0
            for ln in all_lanes:
                try:
                    q += traci.lane.getLastStepHaltingNumber(ln)
                except Exception:
                    pass
            total_queue_proxy += q
    
    # 记录执行后的车辆和排队
    vehicles_after = set()
    queue_end = 0.0
    for ln in all_lanes:
        try:
            vehicles_after.update(traci.lane.getLastStepVehicleIDs(ln))
            queue_end += traci.lane.getLastStepHaltingNumber(ln)
        except Exception:
            pass
    
    passed = len(vehicles_before - vehicles_after)
    
    return {
        'passed_vehicles': float(passed),
        'queue_vehicles': float(queue_end),
        'total_queue_proxy': float(total_queue_proxy),
        'sim_time': float(traci.simulation.getTime()),
    }


def _extract_json_object(text: str) -> Union[Dict[str, Any], None]:
    """
    提取JSON对象，使用最后一个匹配的 {...}（更容错）。
    """
    if not text:
        return None
    s = text.strip()
    
    # 快速路径：纯JSON
    if s.startswith("{") and s.endswith("}"):
        try:
            return json.loads(s)
        except Exception:
            pass
    
    # 查找所有 {...} 匹配，取最后一个（通常是真正的JSON输出）
    matches = list(re.finditer(r"\{[^{}]*\}", s))
    if not matches:
        # 尝试更复杂的嵌套匹配
        matches = list(re.finditer(r"\{[\s\S]*?\}", s))
    
    # 从后往前尝试解析
    for m in reversed(matches):
        try:
            obj = json.loads(m.group(0))
            if isinstance(obj, dict):
                return obj
        except Exception:
            continue
    
    return None


def _parse_signal_step_output(text: str, debug: bool = False) -> Union[Dict[str, int], None]:
    """
    解析 signal_step 输出，容忍多余字段和数值字符串。
    """
    obj = _extract_json_object(text)
    if not isinstance(obj, dict):
        if debug: print(f"  - 提取的不是dict: {type(obj)}")
        return None
    
    # 容忍多余字段，只检查必需字段是否存在
    if "next_phase_id" not in obj or "green_sec" not in obj:
        if debug: print(f"  - 缺少必需字段: {set(obj.keys())} 需要 {{next_phase_id, green_sec}}")
        return None
    
    # 容忍数值字符串，尝试转换
    try:
        next_phase_id = obj.get("next_phase_id")
        if isinstance(next_phase_id, str):
            next_phase_id = int(next_phase_id)
        elif not isinstance(next_phase_id, int):
            if debug: print(f"  - next_phase_id 无法转为 int: {next_phase_id}")
            return None
        
        green_sec = obj.get("green_sec")
        if isinstance(green_sec, str):
            green_sec = int(green_sec)
        elif not isinstance(green_sec, int):
            if debug: print(f"  - green_sec 无法转为 int: {green_sec}")
            return None
        
        if green_sec <= 0:
            if debug: print(f"  - green_sec <= 0: {green_sec}")
            return None
        
        return {"next_phase_id": int(next_phase_id), "green_sec": int(green_sec)}
    
    except (ValueError, TypeError) as e:
        if debug: print(f"  - 转换错误: {e}")
        return None


def _parse_extend_decision_output(text: str, debug: bool = False) -> Union[Dict[str, Any], None]:
    """
    解析 extend_decision 输出，容忍多余字段、数值字符串和extend同义值。
    """
    obj = _extract_json_object(text)
    if not isinstance(obj, dict):
        if debug: print(f"  - 提取的不是dict: {type(obj)}")
        return None
    
    # 容忍多余字段，只检查必需字段
    if "extend" not in obj or "extend_sec" not in obj:
        if debug: print(f"  - 缺少必需字段: {set(obj.keys())} 需要 {{extend, extend_sec}}")
        return None
    
    try:
        # 容忍 extend 的同义值
        extend = obj.get("extend")
        if isinstance(extend, str):
            extend_lower = extend.lower().strip()
            # 兼容模型输出把中文写成字面量转义（例如 "\\u662f"），此时 json.loads 后会得到 "\u662f"
            if re.search(r"\\u[0-9a-fA-F]{4}", extend_lower):
                try:
                    extend_decoded = extend_lower.encode("utf-8").decode("unicode_escape").lower().strip()
                    extend_lower = extend_decoded
                except Exception:
                    pass
            # 映射同义值
            if extend_lower in ("是", "yes", "true", "1", "延长"):
                extend = "是"
            elif extend_lower in ("否", "no", "false", "0", "不延长"):
                extend = "否"
            else:
                if debug: print(f"  - extend值无法识别: {extend}")
                return None
        elif isinstance(extend, bool):
            extend = "是" if extend else "否"
        else:
            if debug: print(f"  - extend类型错误: {type(extend)}")
            return None
        
        # 容忍数值字符串
        extend_sec = obj.get("extend_sec")
        if isinstance(extend_sec, str):
            extend_sec = int(extend_sec)
        elif not isinstance(extend_sec, int):
            if debug: print(f"  - extend_sec 无法转为 int: {extend_sec}")
            return None
        
        if extend_sec < 0:
            if debug: print(f"  - extend_sec < 0: {extend_sec}")
            return None
        
        return {"extend": extend, "extend_sec": int(extend_sec)}
    
    except (ValueError, TypeError) as e:
        if debug: print(f"  - 转换错误: {e}")
        return None


# ==================== Reward Function Split (Parse / Validate / Score / Aggregate) ====================
def parse_output(
    completion_text: str,
    task_type: str,
    *,
    debug: bool = False,
) -> tuple[Union[Dict[str, Any], None], str]:
    """
    Parse a completion into a normalized action dict for a given task type.

    Returns:
        (action, reason)
        - action: normalized dict or None if parsing failed
        - reason: reason code (e.g. *_parse_failed, ok)
    """
    if task_type == "signal_step":
        parsed = _parse_signal_step_output(completion_text, debug=debug)
        if not parsed:
            return None, "signal_step_parse_failed"
        return parsed, "ok"

    if task_type == "extend_decision":
        parsed = _parse_extend_decision_output(completion_text, debug=debug)
        if not parsed:
            return None, "extend_decision_parse_failed"
        return parsed, "ok"

    return None, "unsupported_task_type"


def validate_action(
    task_type: str,
    action: Dict[str, Any],
    *,
    phase_ids: Union[List[int], None] = None,
    green_sec_min: Union[int, None] = None,
    green_sec_max: Union[int, None] = None,
    phase_limits: Union[Dict[str, Any], None] = None,
    current_phase_id: Union[int, None] = None,
    current_elapsed_sec: Union[int, None] = None,
    wait_time_for_phase_change: Union[int, None] = None,
) -> tuple[bool, str, Dict[str, Any]]:
    """
    Validate an action against task constraints. Returns (is_valid, reason, normalized_action).

    Notes:
      - For extend_decision, when already at max_green (considering wait_time), we normalize to extend="否"
        if extend_sec==0; otherwise mark invalid with a dedicated reason.
    """
    wait_time = int(wait_time_for_phase_change or 0)

    if task_type == "signal_step":
        next_phase_id = int(action.get("next_phase_id"))
        green_sec = int(action.get("green_sec"))

        if phase_ids and next_phase_id not in phase_ids:
            return False, "signal_step_phase_id_invalid", action

        min_green = int(REWARD_CONFIG["green_sec_min"] if green_sec_min is None else green_sec_min)
        max_green = int(REWARD_CONFIG["green_sec_max"] if green_sec_max is None else green_sec_max)
        if not (min_green <= green_sec <= max_green):
            return False, "signal_step_green_out_of_range", action

        return True, "ok", action

    if task_type == "extend_decision":
        if not phase_limits:
            return False, "extend_decision_phase_limits_missing", action

        if current_phase_id is None:
            return False, "extend_decision_current_phase_missing", action

        limits = phase_limits.get(str(int(current_phase_id)), None) if isinstance(phase_limits, dict) else None
        if not limits:
            return False, "extend_decision_limits_missing_for_phase", action

        min_green = int(limits["min_green"])
        max_green = int(limits["max_green"])

        if current_elapsed_sec is None:
            return False, "extend_decision_current_elapsed_missing", action

        extend = str(action.get("extend"))
        extend_sec = int(action.get("extend_sec"))

        if int(current_elapsed_sec) + wait_time >= max_green:
            if extend_sec != 0:
                return False, "extend_decision_extend_when_at_max_green", action
            # normalize (avoid counting as error later)
            action = {**action, "extend": "否"}
            extend = "否"

        if extend == "否" and extend_sec != 0:
            return False, "extend_decision_extend_sec_nonzero_when_no", action

        final_green = int(current_elapsed_sec) + extend_sec
        if not (min_green <= final_green + wait_time <= max_green):
            return False, "extend_decision_final_green_out_of_bounds", action

        return True, "ok", action

    return False, "unsupported_task_type", action


def aggregate_reward(
    *,
    valid: bool,
    sim_reward: float,
    invalid_reward: float,
    reward_components: Dict[str, Any],
    error_tags: List[str],
    reason: str,
) -> Dict[str, Any]:
    """
    Aggregate reward components into a scalar reward, while carrying diagnostics.
    """
    final_reward = float(sim_reward) if valid else float(invalid_reward)
    if not valid:
        reward_components = {**(reward_components or {}), "invalid": 1.0}
    return {
        "reward": final_reward,
        "reward_components": reward_components or {},
        "error_tags": error_tags or [],
        "reason": reason,
    }


def score_signal_step(
    simulator: "SUMOSimulator",
    tl_id: str,
    action: Dict[str, Any],
    *,
    phase_ids: Union[List[int], None],
    decision_lead_sec: int,
    decision_remaining_sec: Union[int, None],
    tls_phase_durations: Union[List[Any], None],
    green_sec_min: Union[int, None] = None,
    green_sec_max: Union[int, None] = None,
) -> Dict[str, Any]:
    """
    Score a signal_step action by running a short SUMO roll-forward.
    """
    invalid = float(REWARD_CONFIG["invalid_output_reward"])
    ok, reason, action = validate_action(
        "signal_step",
        action,
        phase_ids=phase_ids,
        green_sec_min=green_sec_min,
        green_sec_max=green_sec_max,
    )
    if not ok:
        return aggregate_reward(
            valid=False,
            sim_reward=0.0,
            invalid_reward=invalid,
            reward_components={"task": "signal_step"},
            error_tags=[reason],
            reason=reason,
        )

    import traci

    _apply_tls_phase_durations(tl_id, tls_phase_durations or [])

    decision_rem = decision_remaining_sec if decision_remaining_sec is not None else int(decision_lead_sec)
    for _ in range(int(max(0, decision_rem))):
        traci.simulationStep()

    next_phase_id = int(action["next_phase_id"])
    green_sec = int(action["green_sec"])
    sim_metrics = _simulate_phase_window(simulator, tl_id, next_phase_id, green_sec)

    avg_passed = float(sim_metrics["avg_passed_veh"])
    avg_queue = float(sim_metrics["avg_queue_veh"])
    sim_reward = float(REWARD_CONFIG["alpha_passed"] * avg_passed - REWARD_CONFIG["beta_queue"] * avg_queue)

    final_reason = "ok"
    if sim_metrics.get("non_green_phase"):
        final_reason = "signal_step_target_phase_not_green"
    elif sim_metrics.get("duration_zero"):
        final_reason = "signal_step_duration_zero"

    return aggregate_reward(
        valid=True,
        sim_reward=sim_reward,
        invalid_reward=invalid,
        reward_components={
            "task": "signal_step",
            "sim_avg_passed": avg_passed,
            "sim_avg_queue": avg_queue,
            "sim_reward": sim_reward,
        },
        error_tags=[] if final_reason == "ok" else [final_reason],
        reason=final_reason,
    )


def score_extend_decision(
    simulator: "SUMOSimulator",
    tl_id: str,
    action: Dict[str, Any],
    *,
    phase_limits: Union[Dict[str, Any], None],
    wait_time_for_phase_change: int,
    current_elapsed_sec: Union[int, None],
    tls_phase_durations: Union[List[Any], None],
) -> Dict[str, Any]:
    """
    Score an extend_decision action by validating bounds and simulating the phase window.
    """
    invalid = float(REWARD_CONFIG["invalid_output_reward"])

    import traci

    _apply_tls_phase_durations(tl_id, tls_phase_durations or [])

    # Identify current phase + elapsed (prefer dataset-provided elapsed)
    current_phase_idx = traci.trafficlight.getPhase(tl_id)
    current_phase_id = int(current_phase_idx) + 1

    if current_elapsed_sec is None:
        planned_green = int(round(traci.trafficlight.getPhaseDuration(tl_id)))
        remaining = traci.trafficlight.getNextSwitch(tl_id) - traci.simulation.getTime()
        current_elapsed_sec = int(max(0, round(planned_green - remaining)))
    else:
        current_elapsed_sec = int(current_elapsed_sec)

    ok, reason, action = validate_action(
        "extend_decision",
        action,
        phase_limits=phase_limits,
        current_phase_id=current_phase_id,
        current_elapsed_sec=current_elapsed_sec,
        wait_time_for_phase_change=wait_time_for_phase_change,
    )
    if not ok:
        return aggregate_reward(
            valid=False,
            sim_reward=0.0,
            invalid_reward=invalid,
            reward_components={"task": "extend_decision", "current_phase_id": current_phase_id},
            error_tags=[reason],
            reason=reason,
        )

    extend = str(action["extend"])
    extend_sec = int(action["extend_sec"])
    duration = extend_sec + int(wait_time_for_phase_change) if extend == "是" else int(wait_time_for_phase_change)
    sim_metrics = _simulate_phase_window(simulator, tl_id, current_phase_id, duration)

    avg_passed = float(sim_metrics["avg_passed_veh"])
    avg_queue = float(sim_metrics["avg_queue_veh"])
    sim_reward = float(REWARD_CONFIG["alpha_passed"] * avg_passed - REWARD_CONFIG["beta_queue"] * avg_queue)

    final_reason = "ok"
    if sim_metrics.get("non_green_phase"):
        final_reason = "extend_decision_target_phase_not_green"
    elif sim_metrics.get("duration_zero"):
        final_reason = "extend_decision_duration_zero"

    return aggregate_reward(
        valid=True,
        sim_reward=sim_reward,
        invalid_reward=invalid,
        reward_components={
            "task": "extend_decision",
            "current_phase_id": current_phase_id,
            "current_elapsed_sec": int(current_elapsed_sec),
            "duration": int(duration),
            "sim_avg_passed": avg_passed,
            "sim_avg_queue": avg_queue,
            "sim_reward": sim_reward,
        },
        error_tags=[] if final_reason == "ok" else [final_reason],
        reason=final_reason,
    )


def _extract_phase_limits_from_prompt(prompt_messages: List[dict]) -> Union[Dict[str, Any], None]:
    """
    从 prompt 文本中提取 phase_limits（用于 extend_decision 任务）。
    
    当 dataset 没有 phase_limits 列时，从 prompt 中的 JSON 提取。
    """
    if not prompt_messages:
        return None
    
    # 获取 user message 内容
    user_content = None
    for msg in prompt_messages:
        if msg.get('role') == 'user':
            user_content = msg.get('content', '')
            break
    
    if not user_content:
        return None
    
    # 提取 extend_decision_input_json
    match = re.search(r'【extend_decision_input_json】(.*?)【/extend_decision_input_json】', user_content, re.DOTALL)
    if not match:
        return None
    
    try:
        data = json.loads(match.group(1))
        return data.get('phase_limits')
    except Exception:
        return None


def _extract_wait_time_from_prompt(prompt_messages: List[dict]) -> Union[int, None]:
    """
    从 prompt 文本中提取 wait_time_for_phase_change（用于 extend_decision 任务）。
    """
    if not prompt_messages:
        return None
    
    user_content = None
    for msg in prompt_messages:
        if msg.get('role') == 'user':
            user_content = msg.get('content', '')
            break
    
    if not user_content:
        return None
    
    match = re.search(r'【extend_decision_input_json】(.*?)【/extend_decision_input_json】', user_content, re.DOTALL)
    if not match:
        return None
    
    try:
        data = json.loads(match.group(1))
        state = data.get('state', {})
        return state.get('wait_time_for_phase_change')
    except Exception:
        return None


def _extract_current_phase_id_from_prompt(prompt_messages: List[dict]) -> Union[int, None]:
    """
    从 prompt 文本中提取 current_phase_id（用于 extend_decision / signal_step 的无仿真校验兜底）。
    """
    if not prompt_messages:
        return None

    user_content = None
    for msg in prompt_messages:
        if msg.get("role") == "user":
            user_content = msg.get("content", "")
            break

    if not user_content:
        return None

    # extend_decision_input_json / signal_step_input_json 都包含 state.current_phase_id
    for tag in ("extend_decision_input_json", "signal_step_input_json"):
        match = re.search(rf"【{tag}】(.*?)【/{tag}】", user_content, re.DOTALL)
        if not match:
            continue
        try:
            data = json.loads(match.group(1))
            state = data.get("state", {}) or {}
            v = state.get("current_phase_id", None)
            if v is None:
                continue
            return int(v)
        except Exception:
            continue

    return None


def _apply_tls_phase_durations(tl_id: str, durations: List[int]):
    """
    应用保存的 TLS 程序相位时长（用于回放时复现随机配时）。
    
    Args:
        tl_id: 信号灯ID
        durations: 各相位的duration列表
    """
    import traci
    
    if not durations:
        return
    
    try:
        logics = traci.trafficlight.getAllProgramLogics(tl_id)
        if not logics:
            return
        logic = logics[0]
        
        # 确保durations数量与phases数量匹配
        if len(durations) != len(logic.phases):
            return
        
        phases = []
        for i, ph in enumerate(logic.phases):
            new_dur = durations[i]
            phases.append(traci.trafficlight.Phase(new_dur, ph.state, ph.minDur, ph.maxDur, ph.next))
        
        new_logic = traci.trafficlight.Logic(
            logic.programID,
            logic.type,
            logic.currentPhaseIndex,
            phases,
            logic.subParameter,
        )
        traci.trafficlight.setProgramLogic(tl_id, new_logic)
    except Exception as e:
        print(f"应用 tls_phase_durations 失败: {e}")


def _get_phase_incoming_lanes(simulator: SUMOSimulator, tl_id: str, phase_id: int) -> List[str]:
    phase_idx = max(0, int(phase_id) - 1)
    info = simulator.get_phase_controlled_lanes(tl_id, phase_idx)
    return list(info.get("incoming_lanes", []))


def _simulate_phase_window(
    simulator: SUMOSimulator,
    tl_id: str,
    phase_id: int,
    duration_sec: int,
) -> Dict[str, float]:
    import traci

    duration = max(0, int(duration_sec))
    lanes = _get_phase_incoming_lanes(simulator, tl_id, phase_id)
    vehicles_before = set()
    for ln in lanes:
        try:
            vehicles_before.update(traci.lane.getLastStepVehicleIDs(ln))
        except Exception:
            pass

    if duration <= 0:
        return {
            "passed_total": 0.0,
            "avg_passed_veh": 0.0,
            "avg_queue_veh": 0.0,
            "non_green_phase": False,
            "duration_zero": True,
        }

    # 防御性检查：确保目标相位是绿灯相位
    phase_info = simulator.get_phase_info(tl_id)
    phase_states = phase_info.get('phase_states', [])
    target_idx = max(0, int(phase_id) - 1)
    if target_idx < len(phase_states):
        target_state = phase_states[target_idx]
        if not (("G" in target_state) or ("g" in target_state)):
            # 非绿灯相位，返回零 reward
            return {
                "passed_total": 0.0,
                "avg_passed_veh": 0.0,
                "avg_queue_veh": 0.0,
                "non_green_phase": True,
                "duration_zero": False,
            }

    traci.trafficlight.setPhase(tl_id, target_idx)
    traci.trafficlight.setPhaseDuration(tl_id, duration)

    total_queue = 0.0
    for _ in range(duration):
        traci.simulationStep()
        q = 0.0
        for ln in lanes:
            try:
                q += traci.lane.getLastStepHaltingNumber(ln)
            except Exception:
                pass
        total_queue += q

    vehicles_after = set()
    for ln in lanes:
        try:
            vehicles_after.update(traci.lane.getLastStepVehicleIDs(ln))
        except Exception:
            pass

    passed_total = float(len(vehicles_before - vehicles_after))
    avg_passed_veh = passed_total / max(1, duration)  # 平均通过车辆数
    avg_queue = float(total_queue / max(1, duration))
    return {
        "passed_total": passed_total,
        "avg_passed_veh": avg_passed_veh,
        "avg_queue_veh": avg_queue,
        "non_green_phase": False,
        "duration_zero": False,
    }


# ==================== Multi-Reward Functions (GRPOTrainer reward_funcs=[...]) ====================
def tsc_reward_format_fn(
    prompts: Union[List[str], List[List[dict]]],
    completions: Union[List[str], List[List[dict]]],
    completion_ids: List[List[int]],
    **kwargs,
) -> List[float]:
    """
    Format/constraint reward: penalize invalid outputs (parse/bounds), otherwise 0.

    This function also drives reward_diag invalid-rate accounting (so you still get the same
    [reward_diag] invalid_rate / top reasons output).
    """
    valid_reward = float(REWARD_CONFIG.get("format_reward_valid", 0.5))
    invalid_reward = float(REWARD_CONFIG.get("format_reward_invalid", -0.5))

    task_types = kwargs.get("task_type", [])
    phase_ids_list = kwargs.get("phase_ids", [])
    phase_limits_list = kwargs.get("phase_limits", [])
    wait_times = kwargs.get("wait_time_for_phase_change", [])
    elapsed_list = kwargs.get("current_phase_elapsed_sec", [])

    completion_texts: List[str] = []
    for c in completions:
        if isinstance(c, list) and len(c) > 0 and isinstance(c[-1], dict):
            completion_texts.append(c[-1].get("content", ""))
        else:
            completion_texts.append(str(c))

    # 优先使用 kwargs 中的 num_generations；否则用 prompts 长度推断
    num_generations = kwargs.get('num_generations')
    if not num_generations:
        num_generations = len(completion_texts) // max(1, len(prompts))
    num_generations = max(1, int(num_generations))
    
    # 检测 task_types 是否按 completion 展开
    task_types_expanded = (len(task_types) == len(completion_texts))

    trainer_state = kwargs.get("trainer_state", None)
    global_step = getattr(trainer_state, "global_step", None)
    if _REWARD_DIAG.get("window_start_step") is None and global_step is not None:
        _REWARD_DIAG["window_start_step"] = int(global_step)
    
    # Completion logging: log first 3 completions every 5 steps
    if global_step is not None and int(global_step) % 5 == 0:
        print(f"\n[completion_log] step={global_step}, num_completions={len(completion_texts)}")
        for idx, ct in enumerate(completion_texts[:3]):
            task_type = task_types[idx] if (task_types and idx < len(task_types)) else "unknown"
            print(f"  [{idx}] ({task_type}): {ct[:150]}{'...' if len(ct) > 150 else ''}")

    rewards: List[float] = []
    reasons: List[str] = []

    for i, completion_text in enumerate(completion_texts):
        sample_idx = i if task_types_expanded else (i // max(1, num_generations))
        task_type = task_types[sample_idx] if (task_types and sample_idx < len(task_types)) else None

        action, reason = parse_output(completion_text, str(task_type), debug=False)
        if not action:
            rewards.append(invalid_reward)
            reasons.append(reason)
            continue

        phase_ids = phase_ids_list[sample_idx] if phase_ids_list else None
        phase_limits = phase_limits_list[sample_idx] if phase_limits_list else None
        wait_time = int(wait_times[sample_idx]) if wait_times and sample_idx < len(wait_times) else 0
        elapsed = int(elapsed_list[sample_idx]) if elapsed_list and sample_idx < len(elapsed_list) else None

        current_phase_id = None
        if str(task_type) == "extend_decision":
            prompt_messages = prompts[sample_idx] if sample_idx < len(prompts) else None
            if isinstance(prompt_messages, list):
                current_phase_id = _extract_current_phase_id_from_prompt(prompt_messages)
                # Fallback: 如果 dataset 中缺失 phase_limits，从 prompt 提取
                if not phase_limits:
                    phase_limits = _extract_phase_limits_from_prompt(prompt_messages)
                # Fallback: 如果 dataset 中缺失 wait_time，从 prompt 提取
                if not wait_time:
                    extracted_wait = _extract_wait_time_from_prompt(prompt_messages)
                    if extracted_wait is not None:
                        wait_time = int(extracted_wait)

        ok, v_reason, _action2 = validate_action(
            str(task_type),
            action,
            phase_ids=phase_ids,
            phase_limits=phase_limits,
            current_phase_id=current_phase_id,
            current_elapsed_sec=elapsed,
            wait_time_for_phase_change=wait_time,
        )
        if not ok:
            rewards.append(invalid_reward)
            reasons.append(v_reason)
            continue

        rewards.append(valid_reward)
        reasons.append("ok")

    # Diagnostics aggregation (treat invalid when this format reward hits invalid penalty)
    try:
        _REWARD_DIAG["window_total"] += len(rewards)
        for i, (r, reason) in enumerate(zip(rewards, reasons)):
            sample_idx = i if task_types_expanded else (i // max(1, num_generations))
            task_type = task_types[sample_idx] if (task_types and sample_idx < len(task_types)) else "unknown"
            _REWARD_DIAG["window_total_by_task"][task_type] += 1
            if float(r) == invalid_reward:
                _REWARD_DIAG["window_invalid"] += 1
                _REWARD_DIAG["window_invalid_by_task"][task_type] += 1
            _REWARD_DIAG.setdefault("window_reason_by_task", {}).setdefault(task_type, Counter())[reason] += 1
        
        # Store per-batch diagnostics for KL spike debugging
        if global_step is not None:
            batch_info = {
                "num_completions": len(completion_texts),
                "num_generations": num_generations,
                "sample_completions": completion_texts[:3],
                "sample_reasons": reasons[:3],
                "sample_rewards": [float(r) for r in rewards[:3]],
                "task_types": list(set(task_types)) if task_types else [],
                "invalid_count": sum(1 for r in rewards if float(r) == invalid_reward),
            }
            _REWARD_DIAG["last_batch_by_step"][int(global_step)] = batch_info
            _REWARD_DIAG["last_batch_latest"] = batch_info
            # Cleanup old entries (keep only last max_steps_kept)
            max_kept = _REWARD_DIAG.get("max_steps_kept", 300)
            if len(_REWARD_DIAG["last_batch_by_step"]) > max_kept:
                oldest = min(_REWARD_DIAG["last_batch_by_step"].keys())
                del _REWARD_DIAG["last_batch_by_step"][oldest]
    except Exception:
        pass

    return rewards


def _simulate_valid_action_worker(args: tuple) -> tuple[float, str]:
    """
    Parallel worker: assumes parse/format validation already passed. Returns (sim_reward, reason).
    args tuple now includes a `port` field at the end for fixed port assignment.
    """
    # 解包参数，最后一个是 port（可选）
    if len(args) == 14:
        (
            task_type,
            action,
            state_path,
            scenario,
            tl_id,
            sumocfg,
            phase_ids,
            decision_lead_sec,
            decision_remaining_sec,
            wait_time,
            phase_limits,
            current_elapsed_sec,
            tls_phase_durations,
            port,
        ) = args
    else:
        (
            task_type,
            action,
            state_path,
            scenario,
            tl_id,
            sumocfg,
            phase_ids,
            decision_lead_sec,
            decision_remaining_sec,
            wait_time,
            phase_limits,
            current_elapsed_sec,
            tls_phase_durations,
        ) = args
        port = None

    try:
        simulator = SUMOSimulator(
            config_file=sumocfg,
            junctions_file=None,
            gui=False,
            additional_options=["--device.rerouting.probability", "0"],
            verbose=False,
            port=port,  # 使用分配的固定端口
        )
        if not simulator.start_simulation():
            return 0.0, "start_simulation_failed"
        if not os.path.exists(state_path):
            simulator.close()
            return 0.0, "state_path_missing"
        simulator.restore_simulation_state(state_path)

        if task_type == "signal_step":
            out = score_signal_step(
                simulator,
                tl_id,
                action,
                phase_ids=phase_ids,
                decision_lead_sec=int(decision_lead_sec),
                decision_remaining_sec=decision_remaining_sec,
                tls_phase_durations=tls_phase_durations,
            )
            simulator.close()
            return float(out["reward"]), str(out["reason"])

        if task_type == "extend_decision":
            out = score_extend_decision(
                simulator,
                tl_id,
                action,
                phase_limits=phase_limits,
                wait_time_for_phase_change=int(wait_time or 0),
                current_elapsed_sec=current_elapsed_sec,
                tls_phase_durations=tls_phase_durations,
            )
            simulator.close()
            return float(out["reward"]), str(out["reason"])

        simulator.close()
        return 0.0, "unsupported_task_type"
    except Exception as e:
        try:
            simulator.close()
        except Exception:
            pass
        return 0.0, f"exception:{type(e).__name__}"


def tsc_reward_sim_fn(
    prompts: Union[List[str], List[List[dict]]],
    completions: Union[List[str], List[List[dict]]],
    completion_ids: List[List[int]],
    **kwargs,
) -> List[float]:
    """
    Simulation reward: run SUMO roll-forward for valid actions, otherwise 0.
    """
    state_paths = kwargs.get("state_path", [])
    scenarios = kwargs.get("scenario", [])
    tl_ids = kwargs.get("tl_id", [])
    task_types = kwargs.get("task_type", [])
    phase_ids_list = kwargs.get("phase_ids", [])
    phase_limits_list = kwargs.get("phase_limits", [])
    decision_lead_secs = kwargs.get("decision_lead_sec", [])
    decision_remaining_secs = kwargs.get("decision_remaining_sec", [])
    wait_times = kwargs.get("wait_time_for_phase_change", [])
    elapsed_list = kwargs.get("current_phase_elapsed_sec", [])
    tls_durs_list = kwargs.get("tls_phase_durations", [])
    sumocfg_paths = kwargs.get("sumocfg_path", [])

    if not state_paths:
        raise ValueError("tsc_reward_sim_fn 需要 state_path 字段")

    completion_texts: List[str] = []
    for c in completions:
        if isinstance(c, list) and len(c) > 0 and isinstance(c[-1], dict):
            completion_texts.append(c[-1].get("content", ""))
        else:
            completion_texts.append(str(c))

    # 优先使用 kwargs 中的 num_generations；否则用 prompts 长度推断
    num_generations = kwargs.get('num_generations')
    if not num_generations:
        num_generations = len(completion_texts) // max(1, len(prompts))
    num_generations = max(1, int(num_generations))
    
    # 检测 state_paths 是否按 completion 展开
    state_paths_expanded = (len(state_paths) == len(completion_texts))
    sim_rewards = [0.0] * len(completion_texts)

    tasks = []
    task_indices = []

    for i, completion_text in enumerate(completion_texts):
        sample_idx = i if state_paths_expanded else (i // max(1, num_generations))
        task_type = task_types[sample_idx] if (task_types and sample_idx < len(task_types)) else None

        action, _reason = parse_output(completion_text, str(task_type), debug=False)
        if not action:
            continue

        phase_ids = phase_ids_list[sample_idx] if phase_ids_list else None
        phase_limits = phase_limits_list[sample_idx] if phase_limits_list else None
        wait_time = int(wait_times[sample_idx]) if wait_times and sample_idx < len(wait_times) else 0
        elapsed = int(elapsed_list[sample_idx]) if elapsed_list and sample_idx < len(elapsed_list) else None
        tls_durs = tls_durs_list[sample_idx] if tls_durs_list and sample_idx < len(tls_durs_list) else []

        current_phase_id = None
        if str(task_type) == "extend_decision":
            prompt_messages = prompts[sample_idx] if sample_idx < len(prompts) else None
            if isinstance(prompt_messages, list):
                current_phase_id = _extract_current_phase_id_from_prompt(prompt_messages)
                # Fallback: 如果 dataset 中缺失 phase_limits，从 prompt 提取
                if not phase_limits:
                    phase_limits = _extract_phase_limits_from_prompt(prompt_messages)
                # Fallback: 如果 dataset 中缺失 wait_time，从 prompt 提取
                if not wait_time:
                    extracted_wait = _extract_wait_time_from_prompt(prompt_messages)
                    if extracted_wait is not None:
                        wait_time = int(extracted_wait)

        ok, _v_reason, action = validate_action(
            str(task_type),
            action,
            phase_ids=phase_ids,
            phase_limits=phase_limits,
            current_phase_id=current_phase_id,
            current_elapsed_sec=elapsed,
            wait_time_for_phase_change=wait_time,
        )
        if not ok:
            continue

        # Resolve sumocfg
        if sumocfg_paths and sample_idx < len(sumocfg_paths):
            sumocfg = sumocfg_paths[sample_idx]
        else:
            scenario_dir = os.path.join("sumo_simulation/environments", scenarios[sample_idx])
            sumocfg = None
            for f in os.listdir(scenario_dir):
                if f.endswith(".sumocfg"):
                    sumocfg = os.path.join(scenario_dir, f)
                    break
        if not sumocfg:
            continue

        tasks.append(
            (
                str(task_type),
                action,
                state_paths[sample_idx],
                scenarios[sample_idx],
                tl_ids[sample_idx],
                sumocfg,
                phase_ids,
                decision_lead_secs[sample_idx] if decision_lead_secs else 10,
                decision_remaining_secs[sample_idx] if decision_remaining_secs and sample_idx < len(decision_remaining_secs) else None,
                wait_time,
                phase_limits,
                elapsed,
                tls_durs,
            )
        )
        task_indices.append(i)

    if not tasks:
        return sim_rewards

    if REWARD_CONFIG.get("parallel_workers", 0) > 0 and len(tasks) > 1:
        pool = _ensure_mp_pool_initialized()
        if pool is None:
            results = list(map(_simulate_valid_action_worker, tasks))
        else:
            try:
                # 为每个任务分配固定端口
                port_base = REWARD_CONFIG.get('parallel_port_base', 20000)
                num_workers = REWARD_CONFIG.get('parallel_workers', 16)
                tasks_with_ports = []
                for i, task in enumerate(tasks):
                    # 为每个任务分配一个worker端口（循环使用）
                    worker_id = i % num_workers
                    port = port_base + worker_id * 100
                    # 将port追加到任务元组末尾
                    tasks_with_ports.append(task + (port,))
                
                results = pool.map(_simulate_valid_action_worker, tasks_with_ports, chunksize=1)
            except Exception as e:
                print(f"[tsc_reward_sim_fn] 并行执行失败，回退到串行: {e}")
                results = list(map(_simulate_valid_action_worker, tasks))
    else:
        results = list(map(_simulate_valid_action_worker, tasks))

    for idx, (r, _reason) in zip(task_indices, results):
        clip_min = float(REWARD_CONFIG.get("sim_reward_clip_min", -1.0))
        clip_max = float(REWARD_CONFIG.get("sim_reward_clip_max", 1.0))
        rr = float(r)
        if rr != rr:  # NaN guard
            rr = 0.0
        if rr < clip_min:
            rr = clip_min
        elif rr > clip_max:
            rr = clip_max
        sim_rewards[idx] = rr

    return sim_rewards


# ==================== 并行 Worker 函数 ====================
def _evaluate_single_completion(args: tuple) -> float:
    """
    并行worker函数：评估单个completion的reward
    
    Args:
        args: (completion_text, state_path, scenario, tl_id, sumocfg, task_type, ..., port)
    
    Returns:
        float: 该completion的reward
    """
    # 解包参数，最后一个是 port（可选）
    if len(args) == 15:
        (completion_text, state_path, scenario, tl_id, sumocfg,
         task_type, phase_ids, decision_lead_sec, decision_remaining_sec,
         wait_time, phase_order, phase_limits, current_elapsed,
         tls_phase_durations, port) = args
    else:
        (completion_text, state_path, scenario, tl_id, sumocfg,
         task_type, phase_ids, decision_lead_sec, decision_remaining_sec,
         wait_time, phase_order, phase_limits, current_elapsed,
         tls_phase_durations) = args
        port = None

    invalid = float(REWARD_CONFIG["invalid_output_reward"])
    try:
        # 创建独立的simulator实例
        simulator = SUMOSimulator(
            config_file=sumocfg,
            junctions_file=None,
            gui=False,  # 并行worker强制关闭GUI
            additional_options=['--device.rerouting.probability', '0'],
            verbose=False,
            port=port,  # 使用分配的固定端口
        )
        
        if not simulator.start_simulation():
            return invalid
        
        # 恢复SUMO state
        if not os.path.exists(state_path):
            simulator.close()
            return invalid
        
        simulator.restore_simulation_state(state_path)
        
        # 根据task_type计算reward
        if task_type == "signal_step":
            action, _reason = parse_output(completion_text, "signal_step", debug=True)
            if not action:
                simulator.close()
                return invalid
            result = score_signal_step(
                simulator,
                tl_id,
                action,
                phase_ids=phase_ids,
                decision_lead_sec=int(decision_lead_sec),
                decision_remaining_sec=decision_remaining_sec,
                tls_phase_durations=tls_phase_durations,
            )
            simulator.close()
            return float(result["reward"])
        
        elif task_type == "extend_decision":
            action, _reason = parse_output(completion_text, "extend_decision", debug=True)
            if not action:
                simulator.close()
                return invalid
            result = score_extend_decision(
                simulator,
                tl_id,
                action,
                phase_limits=phase_limits,
                wait_time_for_phase_change=int(wait_time or 0),
                current_elapsed_sec=current_elapsed,
                tls_phase_durations=tls_phase_durations,
            )
            simulator.close()
            return float(result["reward"])
        
        else:
            # 旧任务类型（cycle_predict等）
            simulator.close()
            return invalid
    
    except Exception as e:
        print(f"评估失败 [{scenario}/{tl_id}]: {e}")
        try:
            simulator.close()
        except:
            pass
        return invalid


# Diagnostics-friendly worker: returns (reward, reason_code)
# args tuple now includes a `port` field at the end for fixed port assignment
def _evaluate_single_completion_diag(args: tuple) -> tuple[float, str]:
    # 解包参数，最后一个是 port（可选）
    if len(args) == 15:
        (completion_text, state_path, scenario, tl_id, sumocfg,
         task_type, phase_ids, decision_lead_sec, decision_remaining_sec,
         wait_time, phase_order, phase_limits, current_elapsed,
         tls_phase_durations, port) = args
    else:
        # 兼容旧格式（无 port 参数）
        (completion_text, state_path, scenario, tl_id, sumocfg,
         task_type, phase_ids, decision_lead_sec, decision_remaining_sec,
         wait_time, phase_order, phase_limits, current_elapsed,
         tls_phase_durations) = args
        port = None

    invalid = float(REWARD_CONFIG["invalid_output_reward"])
    try:
        simulator = SUMOSimulator(
            config_file=sumocfg,
            junctions_file=None,
            gui=False,
            additional_options=['--device.rerouting.probability', '0'],
            verbose=False,
            port=port,  # 使用分配的固定端口
        )
        if not simulator.start_simulation():
            return invalid, "start_simulation_failed"

        if not os.path.exists(state_path):
            simulator.close()
            return invalid, "state_path_missing"

        simulator.restore_simulation_state(state_path)

        if task_type == "signal_step":
            action, reason = parse_output(completion_text, "signal_step", debug=True)
            if not action:
                simulator.close()
                return invalid, reason
            result = score_signal_step(
                simulator,
                tl_id,
                action,
                phase_ids=phase_ids,
                decision_lead_sec=int(decision_lead_sec),
                decision_remaining_sec=decision_remaining_sec,
                tls_phase_durations=tls_phase_durations,
            )
            simulator.close()
            return float(result["reward"]), str(result["reason"])

        if task_type == "extend_decision":
            action, reason = parse_output(completion_text, "extend_decision", debug=True)
            if not action:
                simulator.close()
                return invalid, reason
            result = score_extend_decision(
                simulator,
                tl_id,
                action,
                phase_limits=phase_limits,
                wait_time_for_phase_change=int(wait_time or 0),
                current_elapsed_sec=current_elapsed,
                tls_phase_durations=tls_phase_durations,
            )
            simulator.close()
            return float(result["reward"]), str(result["reason"])

        simulator.close()
        return invalid, "unsupported_task_type"

    except Exception as e:
        print(f"评估失败 [{scenario}/{tl_id}]: {e}")
        try:
            simulator.close()
        except Exception:
            pass
        return invalid, "exception"


# ==================== 主 Reward 函数 ====================
def tsc_reward_fn(
    prompts: Union[List[str], List[List[dict]]],
    completions: Union[List[str], List[List[dict]]],
    completion_ids: List[List[int]],
    **kwargs
) -> List[float]:
    """
    TSC GRPO Reward Function
    
    Args:
        prompts: 批次内的 prompt 列表（字符串或 messages）
        completions: 对应的 completion 列表（字符串）
        completion_ids: completion 的 token id 列表
        **kwargs: Dataset 中的额外字段，必须包含：
            - state_path: List[str] - SUMO state 文件路径
            - scenario: List[str] - 场景名
            - tl_id: List[str] - 信号灯 ID
            - phase_order: List[List[int]] - 相位顺序
            - phase_limits: List[Dict] - 相位约束
    
    Returns:
        List[float]: 每个 completion 的 reward（长度 = len(completions)）
    
    注意：
        - prompts/completions 长度 = batch_size × num_generations
        - 同一 prompt 的 G 个 completion 使用同一个 state_path（连续排列）
    """
    
    # 提取 dataset 字段
    state_paths = kwargs.get('state_path', [])
    scenarios = kwargs.get('scenario', [])
    tl_ids = kwargs.get('tl_id', [])
    phase_orders = kwargs.get('phase_order', [])
    phase_limits_list = kwargs.get('phase_limits', [])
    task_types = kwargs.get('task_type', [])
    phase_ids_list = kwargs.get('phase_ids', [])
    phase_lane_maps = kwargs.get('phase_lane_map', [])
    decision_lead_secs = kwargs.get('decision_lead_sec', [])
    wait_times = kwargs.get('wait_time_for_phase_change', [])
    
    if not state_paths:
        raise ValueError("reward_fn 需要 state_path 字段")
    
    # 将 completions 转为文本（如果是 messages 格式）
    completion_texts = []
    for c in completions:
        if isinstance(c, list) and len(c) > 0 and isinstance(c[-1], dict):
            # messages 格式：取最后一条消息（通常是 assistant 输出）
            completion_texts.append(c[-1].get('content', ''))
        else:
            completion_texts.append(str(c))
    
    # 计算每个 prompt 生成的 completions 数量
    # 优先使用 kwargs 中的 num_generations；否则用 prompts 长度推断（prompts 通常不展开）
    num_generations = kwargs.get('num_generations')
    if not num_generations:
        num_generations = len(completion_texts) // max(1, len(prompts))
    num_generations = max(1, int(num_generations))
    
    # 检测 state_paths 是否按 completion 展开（长度 == completions）
    state_paths_expanded = (len(state_paths) == len(completion_texts))

    trainer_state = kwargs.get("trainer_state", None)
    global_step = getattr(trainer_state, "global_step", None)
    
    # [Fix] Store latest batch consistently
    if global_step is None:
        # If not provided, try to infer or just use a placeholder
        pass

    if _REWARD_DIAG.get("window_start_step") is None and global_step is not None:
        _REWARD_DIAG["window_start_step"] = int(global_step)
    
    # ========== 调试输出（前3条completion） ==========
    if not hasattr(tsc_reward_fn, '_debug_printed'):
        tsc_reward_fn._debug_printed = 0
    
    if tsc_reward_fn._debug_printed < 3:
        print(f"\n{'='*70}")
        print(f"[DEBUG] Completion #{tsc_reward_fn._debug_printed + 1}")
        print(f"{'='*70}")
        if completion_texts:
            raw = completion_texts[0][:500]
            pretty = raw
            try:
                # 尽量把 "\\u662f" 这类字面量转义解码成中文，便于人工查看
                if re.search(r"\\u[0-9a-fA-F]{4}", raw):
                    pretty = raw.encode("utf-8").decode("unicode_escape")
                # 如果能解析成 JSON，针对已知任务类型打印规范化结果（“是/否”）
                if isinstance(_extract_json_object(raw), dict):
                    parsed_ext = _parse_extend_decision_output(raw, debug=False)
                    if parsed_ext:
                        pretty = json.dumps(parsed_ext, ensure_ascii=False)
                    else:
                        parsed_step = _parse_signal_step_output(raw, debug=False)
                        if parsed_step:
                            pretty = json.dumps(parsed_step, ensure_ascii=False)
            except Exception:
                pass
            print(f"原始输出:\n{pretty}")
            print(f"{'='*70}\n")
        tsc_reward_fn._debug_printed += 1
    
    # ========== 并行模式 ==========
    if REWARD_CONFIG['parallel_workers'] > 0 and len(completion_texts) > 1:
        # 准备并行任务参数
        tasks = []
        for i in range(len(completion_texts)):
            # 如果 state_paths 按 completion 展开，直接用 i；否则按组索引
            sample_idx = i if state_paths_expanded else (i // num_generations)
            
            state_path = state_paths[sample_idx]
            scenario = scenarios[sample_idx]
            tl_id = tl_ids[sample_idx]
            completion_text = completion_texts[i]
            
            task_type = task_types[sample_idx] if task_types else None
            phase_ids = phase_ids_list[sample_idx] if phase_ids_list else None
            decision_lead_sec = decision_lead_secs[sample_idx] if decision_lead_secs else 10
            wait_time = wait_times[sample_idx] if wait_times else 0
            
            # 提取新增字段
            sumocfg_paths = kwargs.get('sumocfg_path', [])
            decision_remaining_secs = kwargs.get('decision_remaining_sec', [])
            elapsed_list = kwargs.get('current_phase_elapsed_sec', [])
            tls_durs_list = kwargs.get('tls_phase_durations', [])
            
            # 优先使用 dataset 的 sumocfg_path，否则兜底查找
            if sumocfg_paths and sample_idx < len(sumocfg_paths):
                sumocfg = sumocfg_paths[sample_idx]
            else:
                scenario_dir = os.path.join('sumo_simulation/environments', scenario)
                sumocfg = None
                for f in os.listdir(scenario_dir):
                    if f.endswith('.sumocfg'):
                        sumocfg = os.path.join(scenario_dir, f)
                        break
            
            if not sumocfg:
                tasks.append(None)  # 标记为无效任务
                continue
            
            # phase_order和phase_limits只在某些任务类型中需要
            phase_order = None
            phase_limits = None
            current_elapsed = None
            decision_remaining_sec = None
            tls_phase_durations = []
            
            if task_type == "signal_step":
                if decision_remaining_secs and sample_idx < len(decision_remaining_secs):
                    decision_remaining_sec = decision_remaining_secs[sample_idx]
                if tls_durs_list and sample_idx < len(tls_durs_list):
                    tls_phase_durations = tls_durs_list[sample_idx]
            elif task_type == "extend_decision":
                if phase_orders and sample_idx < len(phase_orders):
                    phase_order = phase_orders[sample_idx]
                
                # phase_limits: 优先从 dataset 列获取，fallback 从 prompt 提取
                if phase_limits_list and sample_idx < len(phase_limits_list) and phase_limits_list[sample_idx]:
                    phase_limits = phase_limits_list[sample_idx]
                else:
                    prompt_messages = prompts[sample_idx] if sample_idx < len(prompts) else None
                    if isinstance(prompt_messages, list):
                        phase_limits = _extract_phase_limits_from_prompt(prompt_messages)
                
                # wait_time: 优先从 dataset 列获取，fallback 从 prompt 提取
                if not (wait_times and sample_idx < len(wait_times) and wait_times[sample_idx] is not None):
                    prompt_messages = prompts[sample_idx] if sample_idx < len(prompts) else None
                    if isinstance(prompt_messages, list):
                        extracted_wait = _extract_wait_time_from_prompt(prompt_messages)
                        if extracted_wait is not None:
                            wait_time = extracted_wait
                
                if elapsed_list and sample_idx < len(elapsed_list):
                    current_elapsed = elapsed_list[sample_idx]
                if tls_durs_list and sample_idx < len(tls_durs_list):
                    tls_phase_durations = tls_durs_list[sample_idx]
            
            tasks.append((
                completion_text, state_path, scenario, tl_id, sumocfg,
                task_type, phase_ids, decision_lead_sec, decision_remaining_sec,
                wait_time, phase_order, phase_limits, current_elapsed,
                tls_phase_durations
                # port 将在下面分配
            ))
        
        # 使用全局常驻 spawn 进程池并行计算
        pool = _ensure_mp_pool_initialized()
        if pool is None:
            # 进程池未启用，回退到顺序模式
            print("[警告] 进程池未启用，回退到顺序模式")
        else:
            # 过滤掉 None 任务，记录索引映射
            valid_tasks = []
            valid_indices = []
            invalid_reward = float(REWARD_CONFIG['invalid_output_reward'])
            
            # 获取端口池配置
            port_base = REWARD_CONFIG.get('parallel_port_base', 20000)
            num_workers = max(1, REWARD_CONFIG.get('parallel_workers', 8))
            
            for i, task in enumerate(tasks):
                if task is None:
                    pass  # 稍后填充
                else:
                    # 为每个任务分配一个唯一端口（基于任务索引循环分配）
                    # 使用模运算确保端口在 worker 池范围内循环
                    assigned_port = port_base + (i % num_workers) * 100
                    # 将端口添加到任务 tuple 末尾
                    task_with_port = task + (assigned_port,)
                    valid_tasks.append(task_with_port)
                    valid_indices.append(i)
            
            # 使用 map 并行执行所有有效任务（返回 (reward, reason)）
            try:
                results = pool.map(_evaluate_single_completion_diag, valid_tasks, chunksize=1)
            except Exception as e:
                print(f"[错误] 进程池 map 失败: {e}")
                results = [(invalid_reward, "parallel_exception")] * len(valid_tasks)
            
            # 组装最终结果
            final_rewards = [invalid_reward] * len(tasks)
            final_reasons = ["sumocfg_missing" if task is None else "unknown" for task in tasks]
            for idx, (reward, reason) in zip(valid_indices, results):
                final_rewards[idx] = float(reward)
                final_reasons[idx] = str(reason)

            # Diagnostics (parallel mode: has reasons via diag worker)
            try:
                invalid_value = float(REWARD_CONFIG["invalid_output_reward"])
                _REWARD_DIAG["window_total"] += len(final_rewards)
                for i, (r, reason) in enumerate(zip(final_rewards, final_reasons)):
                    sample_idx = i if state_paths_expanded else (i // max(1, num_generations))
                    task_type = task_types[sample_idx] if (task_types and sample_idx < len(task_types)) else "unknown"
                    _REWARD_DIAG["window_total_by_task"][task_type] += 1
                    if float(r) == invalid_value:
                        _REWARD_DIAG["window_invalid"] += 1
                        _REWARD_DIAG["window_invalid_by_task"][task_type] += 1
                    _REWARD_DIAG.setdefault("window_reason_by_task", {}).setdefault(task_type, Counter())[reason] += 1

                # Calculate batch diagnostics ALWAYS
                # grouped std per prompt
                group_stds = []
                if num_generations > 0 and (len(final_rewards) % num_generations == 0):
                    for j in range(0, len(final_rewards), num_generations):
                        grp = [float(x) for x in final_rewards[j : j + num_generations]]
                        if len(grp) == num_generations and len(grp) > 1:
                            m = sum(grp) / len(grp)
                            var = sum((x - m) ** 2 for x in grp) / (len(grp) - 1)
                            group_stds.append(var ** 0.5)
                        else:
                            group_stds.append(0.0)
                frac_zero_std = None
                if group_stds:
                    frac_zero_std = sum(1 for s in group_stds if abs(s) < 1e-12) / len(group_stds)

                sorted_rewards = sorted(float(x) for x in final_rewards)
                med = sorted_rewards[len(sorted_rewards) // 2] if sorted_rewards else 0.0
                batch_diag = {
                    "n": len(final_rewards),
                    "num_generations": int(num_generations),
                    "reward_min": float(min(sorted_rewards)) if sorted_rewards else 0.0,
                    "reward_median": float(med),
                    "reward_max": float(max(sorted_rewards)) if sorted_rewards else 0.0,
                    "reward_invalid_count": int(sum(1 for x in final_rewards if float(x) == invalid_value)),
                    "frac_reward_zero_std": frac_zero_std,
                }
                
                # Store latest
                _REWARD_DIAG["last_batch_latest"] = batch_diag

                if global_step is not None:
                    step_key = int(global_step)
                    _REWARD_DIAG.setdefault("last_batch_by_step", {})[step_key] = batch_diag

                    # Bound memory
                    if len(_REWARD_DIAG["last_batch_by_step"]) > int(_REWARD_DIAG.get("max_steps_kept", 300)):
                        for k in sorted(_REWARD_DIAG["last_batch_by_step"].keys())[:50]:
                            _REWARD_DIAG["last_batch_by_step"].pop(k, None)
            except Exception:
                pass

            return final_rewards
    
    # ========== 顺序模式（原有逻辑） ==========
    rewards: List[float] = []
    reasons: List[str] = []
    
    # 按样本逐个评估（每个样本对应一个 state_path）
    for i in range(len(completion_texts)):
        # 计算原始样本索引（同一 prompt 的多个 completions 共享相同的 dataset 字段）
        # 如果 state_paths 按 completion 展开，直接用 i
        sample_idx = i if state_paths_expanded else (i // num_generations)
        
        state_path = state_paths[sample_idx]
        scenario = scenarios[sample_idx]
        tl_id = tl_ids[sample_idx]
        completion_text = completion_texts[i]

        task_type = task_types[sample_idx] if task_types else None
        phase_ids = phase_ids_list[sample_idx] if phase_ids_list else None
        decision_lead_sec = decision_lead_secs[sample_idx] if decision_lead_secs else 10
        
        # wait_time: 优先从 dataset 列获取，fallback 从 prompt 提取
        if wait_times and sample_idx < len(wait_times) and wait_times[sample_idx] is not None:
            wait_time = wait_times[sample_idx]
        else:
            # Fallback: 从 prompt 中提取 wait_time_for_phase_change
            prompt_messages = prompts[sample_idx] if sample_idx < len(prompts) else None
            if isinstance(prompt_messages, list):
                extracted_wait = _extract_wait_time_from_prompt(prompt_messages)
                wait_time = extracted_wait if extracted_wait is not None else 0
            else:
                wait_time = 0
        
        # phase_order 和 phase_limits 只在某些任务类型中存在，延迟访问
        phase_order = None
        phase_limits = None
        
        # 优先使用 dataset 的 sumocfg_path，否则兜底查找
        sumocfg_paths = kwargs.get('sumocfg_path', [])
        if sumocfg_paths and sample_idx < len(sumocfg_paths):
            sumocfg = sumocfg_paths[sample_idx]
        else:
            # 兜底：从 state_path 推断
            scenario_dir = os.path.join('sumo_simulation/environments', scenario)
            sumocfg = None
            for f in os.listdir(scenario_dir):
                if f.endswith('.sumocfg'):
                    sumocfg = os.path.join(scenario_dir, f)
                    break
        
        if not sumocfg:
            print(f"警告: 找不到 sumocfg for {scenario}, 返回负奖励")
            rewards.append(-2.0)
            reasons.append("sumocfg_missing")
            continue
        
        try:
            # 获取 simulator（复用或创建）
            simulator = _GLOBAL_POOL.get_simulator(scenario, sumocfg)
            scaler = _GLOBAL_POOL.get_scaler(tl_id)
            
            # 恢复 SUMO state
            if not os.path.exists(state_path):
                print(f"警告: state 文件不存在: {state_path}")
                rewards.append(float(REWARD_CONFIG['invalid_output_reward']))
                reasons.append("state_path_missing")
                continue
            
            simulator.restore_simulation_state(state_path)

            if task_type in ("signal_step", "extend_decision"):
                if task_type == "signal_step":
                    action, reason = parse_output(completion_text, "signal_step", debug=True)
                    if not action:
                        rewards.append(float(REWARD_CONFIG["invalid_output_reward"]))
                        reasons.append(reason)
                        continue

                    tls_phase_durations_list = kwargs.get("tls_phase_durations", [])
                    tls_durs = tls_phase_durations_list[sample_idx] if tls_phase_durations_list and sample_idx < len(tls_phase_durations_list) else []

                    decision_remaining_secs = kwargs.get("decision_remaining_sec", [])
                    decision_rem = (
                        decision_remaining_secs[sample_idx]
                        if decision_remaining_secs and sample_idx < len(decision_remaining_secs)
                        else None
                    )

                    result = score_signal_step(
                        simulator,
                        tl_id,
                        action,
                        phase_ids=phase_ids,
                        decision_lead_sec=int(decision_lead_sec),
                        decision_remaining_sec=decision_rem,
                        tls_phase_durations=tls_durs,
                    )
                    rewards.append(float(result["reward"]))
                    reasons.append(str(result["reason"]))
                    continue

                if task_type == "extend_decision":
                    action, reason = parse_output(completion_text, "extend_decision", debug=True)
                    if not action:
                        rewards.append(float(REWARD_CONFIG["invalid_output_reward"]))
                        reasons.append(reason)
                        continue

                    tls_phase_durations_list = kwargs.get("tls_phase_durations", [])
                    tls_durs = tls_phase_durations_list[sample_idx] if tls_phase_durations_list and sample_idx < len(tls_phase_durations_list) else []

                    elapsed_list = kwargs.get("current_phase_elapsed_sec", [])
                    elapsed = int(elapsed_list[sample_idx]) if elapsed_list and sample_idx < len(elapsed_list) else None

                    # phase_limits: 优先 dataset 列；否则从 prompt 提取
                    phase_limits = None
                    if phase_limits_list and sample_idx < len(phase_limits_list) and phase_limits_list[sample_idx]:
                        phase_limits = phase_limits_list[sample_idx]
                    else:
                        prompt_messages = prompts[sample_idx] if sample_idx < len(prompts) else None
                        if isinstance(prompt_messages, list):
                            phase_limits = _extract_phase_limits_from_prompt(prompt_messages)

                    result = score_extend_decision(
                        simulator,
                        tl_id,
                        action,
                        phase_limits=phase_limits,
                        wait_time_for_phase_change=int(wait_time or 0),
                        current_elapsed_sec=elapsed,
                        tls_phase_durations=tls_durs,
                    )
                    rewards.append(float(result["reward"]))
                    reasons.append(str(result["reason"]))
                    continue

            # ===== 旧任务: cycle_predict =====
            # cycle_predict 任务需要 phase_order 和 phase_limits
            if phase_orders and sample_idx < len(phase_orders):
                phase_order = phase_orders[sample_idx]
            else:
                rewards.append(float(REWARD_CONFIG['invalid_output_reward']))
                reasons.append("cycle_predict_phase_order_missing")
                continue
            
            if phase_limits_list and sample_idx < len(phase_limits_list):
                phase_limits = phase_limits_list[sample_idx]
            else:
                rewards.append(float(REWARD_CONFIG['invalid_output_reward']))
                reasons.append("cycle_predict_phase_limits_missing")
                continue
            
            constraint_score, info, plan = score_constraints_and_format(
                completion_text=completion_text,
                phase_order=phase_order,
                phase_limits=phase_limits,
                D0=REWARD_CONFIG['D0'],
            )

            if plan is None:
                reward = compute_total_reward(
                    constraint_score=constraint_score,
                    sim_reward=0.0,
                    w_sim=REWARD_CONFIG['w_sim'],
                    w_constraint=REWARD_CONFIG['w_constraint'],
                )
                rewards.append(float(reward))
                reasons.append(f"cycle_predict_hard_constraint:{info.get('error')}")
                continue

            sim_result = evaluate_plan_once_reward_fn(simulator, tl_id, plan)

            scaler.add_observation(
                passed=sim_result['passed_vehicles'],
                queue=sim_result['queue_vehicles'],
                proxy=sim_result['total_queue_proxy'],
            )

            sim_reward, _sim_info = compute_sim_reward_adaptive(
                result=sim_result,
                scaler=scaler,
                baseline_result=None,
                w_passed=REWARD_CONFIG['w_passed'],
                w_queue=REWARD_CONFIG['w_queue'],
                w_proxy=REWARD_CONFIG['w_proxy'],
            )

            total_reward = compute_total_reward(
                constraint_score=constraint_score,
                sim_reward=sim_reward,
                w_sim=REWARD_CONFIG['w_sim'],
                w_constraint=REWARD_CONFIG['w_constraint'],
            )

            rewards.append(float(total_reward))
            reasons.append("ok")
            
        except Exception as e:
            print(f"评估失败 [{scenario}/{tl_id}]: {e}")
            import traceback
            traceback.print_exc()
            rewards.append(float(REWARD_CONFIG['invalid_output_reward']))
            reasons.append("exception")

    # Diagnostics aggregation (sequential mode)
    try:
        invalid_value = float(REWARD_CONFIG["invalid_output_reward"])
        _REWARD_DIAG["window_total"] += len(rewards)
        for i, (r, reason) in enumerate(zip(rewards, reasons)):
            sample_idx = i if state_paths_expanded else (i // max(1, num_generations))
            task_type = task_types[sample_idx] if (task_types and sample_idx < len(task_types)) else "unknown"
            _REWARD_DIAG["window_total_by_task"][task_type] += 1
            if float(r) == invalid_value:
                _REWARD_DIAG["window_invalid"] += 1
                _REWARD_DIAG["window_invalid_by_task"][task_type] += 1
            _REWARD_DIAG.setdefault("window_reason_by_task", {}).setdefault(task_type, Counter())[reason] += 1

        # Calculate batch diagnostics ALWAYS
        # grouped std per prompt
        group_stds = []
        if num_generations > 0 and (len(rewards) % num_generations == 0):
            for j in range(0, len(rewards), num_generations):
                grp = [float(x) for x in rewards[j : j + num_generations]]
                if len(grp) == num_generations and len(grp) > 1:
                    m = sum(grp) / len(grp)
                    var = sum((x - m) ** 2 for x in grp) / (len(grp) - 1)
                    group_stds.append(var ** 0.5)
                else:
                    group_stds.append(0.0)
        frac_zero_std = None
        if group_stds:
            frac_zero_std = sum(1 for s in group_stds if abs(s) < 1e-12) / len(group_stds)

        sorted_rewards = sorted(float(x) for x in rewards)
        med = sorted_rewards[len(sorted_rewards) // 2] if sorted_rewards else 0.0
        batch_diag = {
            "n": len(rewards),
            "num_generations": int(num_generations),
            "reward_min": float(min(sorted_rewards)) if sorted_rewards else 0.0,
            "reward_median": float(med),
            "reward_max": float(max(sorted_rewards)) if sorted_rewards else 0.0,
            "reward_invalid_count": int(sum(1 for x in rewards if float(x) == invalid_value)),
            "frac_reward_zero_std": frac_zero_std,
        }
        
        # Store latest
        _REWARD_DIAG["last_batch_latest"] = batch_diag

        if global_step is not None:
            step_key = int(global_step)
            _REWARD_DIAG.setdefault("last_batch_by_step", {})[step_key] = batch_diag

            # Bound memory
            if len(_REWARD_DIAG["last_batch_by_step"]) > int(_REWARD_DIAG.get("max_steps_kept", 300)):
                for k in sorted(_REWARD_DIAG["last_batch_by_step"].keys())[:50]:
                    _REWARD_DIAG["last_batch_by_step"].pop(k, None)
    except Exception:
        pass
    
    return rewards


def cleanup_global_pool():
    """清理全局 simulator 池和进程池（训练结束时调用）"""
    _GLOBAL_POOL.close_all()
    _cleanup_mp_pool()


# ==================== 测试代码 ====================
if __name__ == '__main__':
    # 简单测试
    print("Reward function 模块加载成功")
    print(f"配置: {REWARD_CONFIG}")
