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
    cycle_constraints: Dict[str, int],
    recent_cycles: List[Dict[str, Any]],
    include_windows_recent_past: bool = True,
    windows_recent_past: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Build the JSON payload expected by new_prompt_training.md.

    Important:
    - Only recent_cycles is required; yesterday/last_week are set to null.
    - phase_limits keys are stringified phase ids, matching the template.
    """
    payload: Dict[str, Any] = {
        "crossing_id": stable_crossing_id(scenario_name, tl_id),
        "as_of": now_str(),
        "phase_order": phase_order,
        "phase_limits": phase_limits,
        "cycle_constraints": cycle_constraints,
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


