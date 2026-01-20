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
    Wrap JSON with signal_step_input_json markers and full task description.
    """
    import json
    json_text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    
    prompt = f"""你是交通信号控制优化专家。【signal_step_input_json】{json_text}【/signal_step_input_json】

字段含义（仅说明含义）：
* state.phase_metrics_now[*].avg_queue_veh：该相位在当前时刻的平均排队车辆数（辆）；可由该相位所控制车道的排队车辆数取平均得到。
* state.phase_metrics_now[*].avg_passed_veh_in_current_green：该相位在"当前正在执行的绿灯相位"内至当前时刻累计通过车辆数（辆）；只有当前相位通常会 >0，非当前相位一般为 0。

任务（必须完成）：
1. 基于输入 JSON 的 scenario 与 state，自行决定决策策略/参数，评估各相位当前需求强度并做出"下一步动作"（仅在内部使用，不输出任何预测过程/中间值）。
2. 输出：下一个信号相位 next_phase_id，以及该相位绿灯持续时间 green_sec（单位：秒）。

要求（必须遵守）：
1. 你必须显式利用 avg_queue_veh 与 passed_veh_in_current_green 来决策；不得无视输入随意给出答案。
2. 在缺少任何额外硬约束（不提供 cycle_constraints / phase_order / phase_limits / history）的情况下：
   * next_phase_id 必须来自 scenario.phase_ids；
   * green_sec 必须为正整数秒，且必须在 [1, 120] 范围内；
   * green_sec 必须"合理"：队列更大/通过更少的相位倾向给更长绿；队列更小/通过更多的相位倾向给更短绿；
   * 若多相位需求接近，可优先切换到非当前相位以降低其他相位等待的累积风险。

输出要求（必须严格遵守）：
1. 只输出最终 JSON（不要任何说明、不要 Markdown 代码块、不要额外文本、不要复述规则、不要输出推理过程）。
2. JSON 必须为对象，且仅包含两个字段：
   {{"next_phase_id": <int>, "green_sec": <int>}}
3. green_sec 必须在 [1, 120] 范围内。
4. 不允许输出其它字段，不允许添加任何解释性文本。"""
    
    return prompt


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
    
    Note: phase_metrics_now is a list but will be converted to phase_metrics_by_id (dict) in the payload.
    """
    # Convert list to dict by phase_id
    phase_metrics_by_id: Dict[str, Dict[str, Any]] = {}
    for m in phase_metrics_now:
        pid = str(m.get("phase_id", ""))
        phase_metrics_by_id[pid] = {
            "avg_queue_veh": m.get("avg_queue_veh", 0.0),
            "avg_passed_veh_in_current_green": m.get("avg_passed_veh_in_current_green", 0.0),
        }
    
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
            "phase_metrics_by_id": phase_metrics_by_id,
        },
    }
    return payload


def wrap_extend_decision_prompt(payload: Dict[str, Any]) -> str:
    """
    Wrap JSON with extend_decision_input_json markers and full task description.
    """
    import json
    json_text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    
    prompt = f"""你是交通信号控制优化专家。

【extend_decision_input_json】{json_text}【/extend_decision_input_json】

字段含义（仅说明含义）：

* phase_order：相位执行顺序，循环执行；不可跳相、不可重排。
* phase_limits.*.min_green / max_green：该相位单次绿灯的最小/最大持续时间（秒）。
* state.current_phase_elapsed_sec：当前相位已执行的绿灯时长（秒）。
* state.wait_time_for_phase_change：从"现在"到能够完成相位切换所需的等待时间（秒）；该时间会占用当前相位的剩余时间预算。
* state.phase_metrics_by_id[pid].avg_queue_veh：该相位在当前时刻的平均排队车辆数（辆）。
* state.phase_metrics_by_id[pid].avg_passed_veh_in_current_green：该相位在"当前正在执行的绿灯相位"内至当前时刻累计平均通过车辆数（辆）；通常只有当前相位会 >0，非当前绿灯相位一般为 0。

任务（必须完成）：

1. 基于输入 JSON 的 scenario 与 state，自行决定决策策略/参数，判断"是否需要延长当前绿灯相位"。
2. 若需要延长，给出延长时间 extend_sec（单位：秒）。

要求（必须遵守）：

1. 你必须显式利用 avg_queue_veh 与 avg_passed_veh_in_current_green 来决策；不得无视输入随意给出答案。
2. 延长决策必须考虑当前相位与其他相位的相对需求：当前相位队列大且仍在有效放行（通过增长）时更倾向延长；其他相位队列明显更大时更倾向不延长以尽快切换。
3. 不得编造不存在的观测数据。

硬约束（必须满足）：

1. 相位顺序固定：按 phase_order 循环推进；本任务只允许决定"是否延长当前相位"，不允许改变相位顺序或直接切到其他相位。
2. 相位时长约束（以"到完成切换"为止的当前相位总占用时间"为准）：

   * 定义：total_occupied_sec = state.current_phase_elapsed_sec + extend_sec + state.wait_time_for_phase_change
   * 必须满足：phase_limits[current_phase_id].min_green ≤ total_occupied_sec ≤ phase_limits[current_phase_id].max_green

3. extend_sec 必须为整数秒，且 extend_sec ≥ 0。
4. 若 state.current_phase_elapsed_sec + state.wait_time_for_phase_change 已经 ≥ phase_limits[current_phase_id].max_green，则必须输出不延长：extend="否", extend_sec=0。
5. 若 state.current_phase_elapsed_sec + state.wait_time_for_phase_change < phase_limits[current_phase_id].min_green，则为了满足最小绿灯约束，你必须输出延长：extend="是"，且
   extend_sec ≥ phase_limits[current_phase_id].min_green - (state.current_phase_elapsed_sec + state.wait_time_for_phase_change)。

输出要求（必须严格遵守）：

1. 只输出最终 JSON（不要任何说明、不要 Markdown、不要额外文本、不要输出推理过程）。
2. JSON 顶层必须是对象，且仅包含两个字段：
   {{"extend": "<是/否>", "extend_sec": <int>}}
3. 不允许输出其它字段。"""
    
    return prompt


