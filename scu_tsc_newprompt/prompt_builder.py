import datetime as _dt
import hashlib
from typing import Any, Dict, List, Optional


def stable_crossing_id(scenario_name: str, tl_id: str) -> int:
    """
    Derive a deterministic positive int ID from (scenario, tl_id).
    """
    h = hashlib.md5(f"{scenario_name}::{tl_id}".encode("utf-8")).hexdigest()
    return int(h[:8], 16)


def now_str() -> str:
    return _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def build_cycle_predict_input_json(
    *,
    scenario_name: str,
    tl_id: str,
    phase_order: List[int],
    phase_limits: Dict[str, Dict[str, int]],
    recent_cycles: List[Dict[str, Any]],
    include_windows_recent_past: bool = True,
    windows_recent_past: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Build the JSON payload expected by new_prompt_training.md.

    Important:
    - Only recent_cycles is required; yesterday/last_week are set to null.
    - phase_limits keys are stringified phase ids, matching the template.
    - 不再包含 cycle_constraints（周期总时长约束），只使用 phase_limits 中的 min_green/max_green。
    """
    payload: Dict[str, Any] = {
        "crossing_id": stable_crossing_id(scenario_name, tl_id),
        "as_of": now_str(),
        "phase_order": phase_order,
        "phase_limits": phase_limits,
        "history": {
            "recent_cycles": recent_cycles,
            "cycle_times": [],
            "windows": {
                "recent_past": windows_recent_past if (include_windows_recent_past and windows_recent_past) else None,
                "yesterday_same_time": None,
                "last_week_same_time": None,
            },
        },
    }
    return payload


def wrap_prompt_with_markers(payload: Dict[str, Any]) -> str:
    """
    Wrap JSON with the same markers used in new_prompt_training.md.
    """
    import json

    json_text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return f"【cycle_predict_input_json】{json_text}【/cycle_predict_input_json】"


def _wrap_prompt_with_marker(payload: Dict[str, Any], marker: str) -> str:
    """
    Wrap JSON with a custom marker.
    """
    import json

    json_text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return f"【{marker}】{json_text}【/{marker}】"


def build_signal_step_input_json(
    *,
    scenario_name: str,
    tl_id: str,
    phase_ids: List[int],
    phase_lane_map: Dict[str, List[str]],
    current_phase_id: int,
    current_phase_elapsed_sec: int,
    current_phase_planned_green_sec: int,
    phase_metrics_now: List[Dict[str, Any]],
    as_of: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Build payload for signal_step_input_json.
    """
    payload: Dict[str, Any] = {
        "crossing_id": stable_crossing_id(scenario_name, tl_id),
        "as_of": as_of or now_str(),
        "scenario": {
            "phase_ids": phase_ids,
            "phase_lane_map": phase_lane_map,
        },
        "state": {
            "current_phase_id": int(current_phase_id),
            "current_phase_elapsed_sec": int(current_phase_elapsed_sec),
            "current_phase_planned_green_sec": int(current_phase_planned_green_sec),
            "phase_metrics_now": phase_metrics_now,
        },
    }
    return payload


def wrap_signal_step_prompt(payload: Dict[str, Any]) -> str:
    """
    Wrap JSON with signal_step_input_json markers.
    """
    return _wrap_prompt_with_marker(payload, "signal_step_input_json")


def build_extend_decision_input_json(
    *,
    scenario_name: str,
    tl_id: str,
    phase_order: List[int],
    phase_limits: Dict[str, Dict[str, int]],
    phase_lane_map: Dict[str, List[str]],
    current_phase_id: int,
    current_phase_elapsed_sec: int,
    wait_time_for_phase_change: int,
    phase_metrics_now: List[Dict[str, Any]],
    as_of: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Build payload for extend_decision_input_json.
    """
    payload: Dict[str, Any] = {
        "crossing_id": stable_crossing_id(scenario_name, tl_id),
        "as_of": as_of or now_str(),
        "phase_order": phase_order,
        "phase_limits": phase_limits,
        "scenario": {
            "phase_lane_map": phase_lane_map,
        },
        "state": {
            "current_phase_id": int(current_phase_id),
            "current_phase_elapsed_sec": int(current_phase_elapsed_sec),
            "wait_time_for_phase_change": int(wait_time_for_phase_change),
            "phase_metrics_now": phase_metrics_now,
        },
    }
    return payload


def wrap_extend_decision_prompt(payload: Dict[str, Any]) -> str:
    """
    Wrap JSON with extend_decision_input_json markers.
    """
    return _wrap_prompt_with_marker(payload, "extend_decision_input_json")


