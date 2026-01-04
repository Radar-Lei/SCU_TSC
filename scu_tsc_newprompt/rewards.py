import json
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class ParsedPlan:
    plan: Optional[List[Dict[str, int]]]
    error: Optional[str]


def _extract_json_array(text: str) -> Optional[str]:
    """
    Extract the first JSON array substring from text.
    Tolerant to extra whitespace / accidental prefix/suffix.
    """
    if not text:
        return None
    s = text.strip()
    # fast path
    if s.startswith("[") and s.endswith("]"):
        return s
    # heuristic: find outermost [...]
    m = re.search(r"\[[\s\S]*\]", s)
    return m.group(0) if m else None


def parse_plan_from_completion(text: str) -> ParsedPlan:
    arr = _extract_json_array(text)
    if arr is None:
        return ParsedPlan(plan=None, error="no_json_array")
    try:
        obj = json.loads(arr)
    except Exception:
        return ParsedPlan(plan=None, error="json_parse_error")
    if not isinstance(obj, list):
        return ParsedPlan(plan=None, error="not_list")
    plan: List[Dict[str, int]] = []
    for it in obj:
        if not isinstance(it, dict):
            return ParsedPlan(plan=None, error="item_not_object")
        if set(it.keys()) != {"phase_id", "final"}:
            return ParsedPlan(plan=None, error="bad_keys")
        pid = it.get("phase_id")
        fin = it.get("final")
        if not isinstance(pid, int) or not isinstance(fin, int):
            return ParsedPlan(plan=None, error="non_int_fields")
        plan.append({"phase_id": pid, "final": fin})
    return ParsedPlan(plan=plan, error=None)


def score_constraints_and_format(
    *,
    completion_text: str,
    phase_order: List[int],
    phase_limits: Dict[str, Dict[str, int]],
    cycle_constraints: Dict[str, int],
) -> Tuple[float, Dict[str, Any], Optional[List[Dict[str, int]]]]:
    """
    Returns: (score 0..1, info dict, parsed plan or None)
    
    硬约束（无法执行）：
    - 格式错误（无法解析 JSON）
    - 相位数量不匹配
    - 相位顺序错误
    
    软约束（可执行但扣分）：
    - phase_limits 越界：根据偏离量计算惩罚
    - cycle 总时长越界：根据偏离量计算惩罚
    """
    info: Dict[str, Any] = {
        "format_ok": False,
        "order_ok": False,
        "bounds_ok": False,
        "cycle_ok": False,
        "bounds_penalty": 0.0,
        "cycle_penalty": 0.0,
        "error": None,
    }

    parsed = parse_plan_from_completion(completion_text)
    if parsed.error:
        info["error"] = parsed.error
        return 0.0, info, None
    assert parsed.plan is not None

    plan = parsed.plan
    n = len(phase_order)
    if len(plan) != n:
        info["error"] = "wrong_length"
        return 0.0, info, None

    # format ok (strict keys & ints already checked)
    info["format_ok"] = True

    # order check (硬约束：顺序必须正确才能执行)
    out_phase_ids = [x["phase_id"] for x in plan]
    if out_phase_ids != phase_order:
        info["error"] = "bad_order"
        return 0.1, info, None  # 格式正确但顺序错，无法执行
    
    info["order_ok"] = True

    # ========== 以下是软约束，计算偏离惩罚 ==========
    
    # bounds check (软约束)
    total_bounds_deviation = 0.0  # 总偏离秒数
    max_possible_deviation = 0.0  # 用于归一化
    
    for x in plan:
        pid = x["phase_id"]
        lim = phase_limits.get(str(pid))
        if not lim:
            # 如果找不到限制，跳过
            continue
        mn = int(lim["min_green"])
        mx = int(lim["max_green"])
        val = int(x["final"])
        
        # 计算偏离量
        if val < mn:
            total_bounds_deviation += (mn - val)
        elif val > mx:
            total_bounds_deviation += (val - mx)
        
        # 最大可能偏离 = max(val 可能的偏离)
        max_possible_deviation += max(mx, 120)  # 假设最大可能值是 120 秒
    
    # 归一化 bounds 惩罚到 [0, 1]
    # 使用 soft 函数：deviation 越大，惩罚越大，但不会超过 1
    bounds_penalty = min(1.0, total_bounds_deviation / max(60.0, max_possible_deviation * 0.3))
    info["bounds_penalty"] = bounds_penalty
    info["bounds_ok"] = (total_bounds_deviation == 0)

    # cycle check (软约束)
    total = sum(int(x["final"]) for x in plan)
    cmin = int(cycle_constraints["cycle_min_sec"])
    cmax = int(cycle_constraints["cycle_max_sec"])
    
    cycle_deviation = 0.0
    if total < cmin:
        cycle_deviation = cmin - total
    elif total > cmax:
        cycle_deviation = total - cmax
    
    # 归一化 cycle 惩罚
    # 偏离 60 秒时惩罚达到 1.0
    cycle_penalty = min(1.0, cycle_deviation / 60.0)
    info["cycle_penalty"] = cycle_penalty
    info["cycle_ok"] = (cycle_deviation == 0)
    
    # 计算最终分数
    # 基础分 = 1.0（格式和顺序都正确）
    # 扣除 bounds 惩罚（权重 0.3）和 cycle 惩罚（权重 0.3）
    # 最低分 0.4（格式和顺序正确的保底分）
    base_score = 1.0
    constraint_penalty = 0.3 * bounds_penalty + 0.3 * cycle_penalty
    final_score = max(0.4, base_score - constraint_penalty)
    
    return final_score, info, plan


def compute_soft_constraint_reward(
    plan: List[Dict[str, int]],
    phase_limits: Dict[str, Dict[str, int]],
    cycle_constraints: Dict[str, int],
) -> Tuple[float, Dict[str, Any]]:
    """
    单独计算软约束的 reward（用于仿真后的额外评估）。
    返回 (reward, info)，reward 在 [-1, 0] 范围，0 表示完全满足约束。
    """
    info = {
        "bounds_deviation_sec": 0.0,
        "cycle_deviation_sec": 0.0,
    }
    
    # bounds deviation
    total_bounds_deviation = 0.0
    for x in plan:
        pid = x["phase_id"]
        lim = phase_limits.get(str(pid))
        if not lim:
            continue
        mn = int(lim["min_green"])
        mx = int(lim["max_green"])
        val = int(x["final"])
        
        if val < mn:
            total_bounds_deviation += (mn - val)
        elif val > mx:
            total_bounds_deviation += (val - mx)
    
    info["bounds_deviation_sec"] = total_bounds_deviation
    
    # cycle deviation
    total = sum(int(x["final"]) for x in plan)
    cmin = int(cycle_constraints["cycle_min_sec"])
    cmax = int(cycle_constraints["cycle_max_sec"])
    
    cycle_deviation = 0.0
    if total < cmin:
        cycle_deviation = cmin - total
    elif total > cmax:
        cycle_deviation = total - cmax
    
    info["cycle_deviation_sec"] = cycle_deviation
    
    # 计算惩罚 reward（负值）
    # 每偏离 10 秒，惩罚 0.1
    total_deviation = total_bounds_deviation + cycle_deviation
    penalty_reward = -min(1.0, total_deviation / 100.0)
    
    return penalty_reward, info
