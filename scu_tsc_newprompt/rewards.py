import json
import math
import re
from collections import deque
from dataclasses import dataclass, field
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
    D0: float = 30.0,  # 软约束归一化尺度（秒）
) -> Tuple[float, Dict[str, Any], Optional[List[Dict[str, int]]]]:
    """
    Returns: (score in [-1.5, 0], info dict, parsed plan or None)
    
    硬约束（无法执行，返回强负分 + plan=None）：
    - 格式错误（无法解析 JSON）→ -1.5
    - 相位数量不匹配 → -1.5
    - 相位顺序错误 → -1.2
    
    软约束（可执行，返回 [-1, 0] 惩罚）：
    - phase_limits 越界：R_c = -clip(deviation_sec / D0, 0, 1)
    """
    info: Dict[str, Any] = {
        "format_ok": False,
        "order_ok": False,
        "bounds_ok": False,
        "bounds_deviation_sec": 0.0,
        "error": None,
    }

    parsed = parse_plan_from_completion(completion_text)
    if parsed.error:
        info["error"] = parsed.error
        return -1.5, info, None  # 硬约束：格式错误
    assert parsed.plan is not None

    plan = parsed.plan
    n = len(phase_order)
    if len(plan) != n:
        info["error"] = "wrong_length"
        return -1.5, info, None  # 硬约束：长度错误

    # format ok (strict keys & ints already checked)
    info["format_ok"] = True

    # order check (硬约束：顺序必须正确才能执行)
    out_phase_ids = [x["phase_id"] for x in plan]
    if out_phase_ids != phase_order:
        info["error"] = "bad_order"
        return -1.2, info, None  # 硬约束：顺序错误（格式对但不可执行）
    
    info["order_ok"] = True

    # ========== 以下是软约束，计算偏离惩罚 ==========
    
    # bounds check (软约束)
    total_bounds_deviation = 0.0  # 总偏离秒数
    
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
    
    info["bounds_deviation_sec"] = total_bounds_deviation
    info["bounds_ok"] = (total_bounds_deviation == 0)
    
    # 软约束惩罚：R_c = -clip(deviation / D0, 0, 1)，范围 [-1, 0]
    constraint_penalty = min(1.0, total_bounds_deviation / D0)
    final_score = -constraint_penalty  # 满足约束时为 0，越界越负
    
    return final_score, info, plan


def compute_soft_constraint_reward(
    plan: List[Dict[str, int]],
    phase_limits: Dict[str, Dict[str, int]],
    D0: float = 30.0,
) -> Tuple[float, Dict[str, Any]]:
    """
    单独计算软约束的 reward（用于仿真后的额外评估）。
    只检查 min_green / max_green 边界约束。
    返回 (reward, info)，reward 在 [-1, 0] 范围，0 表示完全满足约束。
    
    使用 clip 方式：R_c = -clip(deviation_sec / D0, 0, 1)
    """
    info = {
        "bounds_deviation_sec": 0.0,
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
    
    # 软约束惩罚：R_c = -clip(deviation / D0, 0, 1)
    penalty_reward = -min(1.0, total_bounds_deviation / D0)
    
    return penalty_reward, info


# ==================== 自适应尺度器（按路口维护 P95）====================


@dataclass
class MetricBuffer:
    """单个指标的滑动窗口缓冲区"""
    values: deque = field(default_factory=lambda: deque(maxlen=200))
    scale: float = 1.0  # 当前 P95 尺度
    
    def add(self, v: float):
        self.values.append(v)
        self._update_scale()
    
    def add_batch(self, vs: List[float]):
        for v in vs:
            self.values.append(v)
        self._update_scale()
    
    def _update_scale(self):
        if len(self.values) < 5:
            return  # 数据太少，保持默认
        sorted_vals = sorted(self.values)
        idx = int(len(sorted_vals) * 0.95)
        idx = min(idx, len(sorted_vals) - 1)
        p95 = sorted_vals[idx]
        self.scale = max(1.0, p95)  # 至少为 1，防止除零


@dataclass
class AdaptiveScaler:
    """
    按路口 (tl_id) 维护 passed / queue / total_queue_proxy 的 P95 尺度。
    用于归一化仿真指标，使不同路口的 reward 具有可比性。
    """
    passed_buf: MetricBuffer = field(default_factory=MetricBuffer)
    queue_buf: MetricBuffer = field(default_factory=MetricBuffer)
    proxy_buf: MetricBuffer = field(default_factory=MetricBuffer)
    
    # 默认尺度（用于首次评估/冷启动）
    default_passed_scale: float = 20.0
    default_queue_scale: float = 30.0
    default_proxy_scale: float = 2000.0
    
    def add_observation(self, passed: float, queue: float, proxy: float):
        """添加一次评估观测"""
        self.passed_buf.add(passed)
        self.queue_buf.add(queue)
        self.proxy_buf.add(proxy)
    
    def add_observations_batch(self, results: List[Dict[str, float]]):
        """批量添加多个评估结果"""
        for r in results:
            self.passed_buf.add(r.get('passed_vehicles', 0.0))
            self.queue_buf.add(r.get('queue_vehicles', 0.0))
            self.proxy_buf.add(r.get('total_queue_proxy', 0.0))
    
    def get_scales(self) -> Tuple[float, float, float]:
        """返回 (passed_scale, queue_scale, proxy_scale)"""
        p = self.passed_buf.scale if len(self.passed_buf.values) >= 5 else self.default_passed_scale
        q = self.queue_buf.scale if len(self.queue_buf.values) >= 5 else self.default_queue_scale
        z = self.proxy_buf.scale if len(self.proxy_buf.values) >= 5 else self.default_proxy_scale
        return (p, q, z)
    
    def warmup_from_results(self, results: List[Dict[str, float]]):
        """用 warmup 阶段的数据初始化尺度"""
        self.add_observations_batch(results)


def compute_sim_reward_adaptive(
    result: Dict[str, float],
    scaler: AdaptiveScaler,
    baseline_result: Optional[Dict[str, float]] = None,  # 保留参数但不再使用
    w_passed: float = 1.0,
    w_queue: float = 1.0,
    w_proxy: float = 0.2,
) -> Tuple[float, Dict[str, Any]]:
    """
    计算仿真 reward（绝对指标，统一尺度版本）。
    
    Args:
        result: 当前 plan 的仿真结果
        scaler: 该路口的 AdaptiveScaler
        baseline_result: 不再使用（为兼容性保留）
        w_passed / w_queue / w_proxy: 各指标权重
    
    Returns:
        (sim_reward, info_dict)
        sim_reward 在 [-1.5, 1.5] 范围（与 constraint_score 对称）
    """
    P0, Q0, Z0 = scaler.get_scales()
    
    passed = result.get('passed_vehicles', 0.0)
    queue = result.get('queue_vehicles', 0.0)
    proxy = result.get('total_queue_proxy', 0.0)
    
    # 使用绝对值（不使用 baseline delta）
    # tanh 归一化到 [-1, 1] 区间
    R_passed = math.tanh(passed / P0)      # passed 越多越好 → 正
    R_queue = -math.tanh(queue / Q0)       # queue 越少越好 → 负
    R_proxy = -math.tanh(proxy / Z0)       # proxy 越小越好 → 负
    
    # 加权平均（归一化权重和）
    total_weight = w_passed + w_queue + w_proxy
    sim_reward_normalized = (
        w_passed * R_passed + 
        w_queue * R_queue + 
        w_proxy * R_proxy
    ) / total_weight  # 归一化到 [-1, 1]
    
    # 缩放到 [-1.5, 1.5] 以匹配 constraint_score 的范围
    sim_reward = sim_reward_normalized * 1.5
    
    info = {
        'passed': passed,
        'queue': queue,
        'proxy': proxy,
        'scales': (P0, Q0, Z0),
        'R_passed': R_passed,
        'R_queue': R_queue,
        'R_proxy': R_proxy,
        'sim_reward_normalized': sim_reward_normalized,
    }
    
    return sim_reward, info


def compute_total_reward(
    constraint_score: float,
    sim_reward: float,
    w_sim: float = 1.0,
    w_constraint: float = 0.3,
) -> float:
    """
    计算总 reward = w_sim * sim_reward + w_constraint * constraint_score
    
    constraint_score: [-1.5, 0]（硬约束更负，满足软约束为 0）
    sim_reward: 大致 [-2, 2]（取决于 tanh 归一化）
    """
    return w_sim * sim_reward + w_constraint * constraint_score
