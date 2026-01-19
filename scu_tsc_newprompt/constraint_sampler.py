import random
from typing import Dict, List, Optional, Tuple


def _clamp(x: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, x))


def sample_phase_limits_hybrid(
    phase_order: List[int],
    net_minmax_one_based: Optional[Dict[int, Tuple[int, int]]] = None,
    rng: Optional[random.Random] = None,
    *,
    global_min_range: Tuple[int, int] = (10, 45),
    global_max_cap: int = 120,
) -> Dict[str, Dict[str, int]]:
    """
    Hybrid sampling of per-phase min_green / max_green.

    - If net.xml provides minDur/maxDur for a phase, use them as base and jitter.
    - Otherwise sample from global ranges.

    Returns dict keyed by phase_id as *string* (to match prompt schema).
    """
    if rng is None:
        rng = random.Random()
    if net_minmax_one_based is None:
        net_minmax_one_based = {}

    limits: Dict[str, Dict[str, int]] = {}
    min_lo, min_hi = global_min_range

    for phase_id in phase_order:
        if phase_id in net_minmax_one_based:
            base_min, base_max = net_minmax_one_based[phase_id]
            base_min = _clamp(int(base_min), 1, global_max_cap - 2)
            base_max = _clamp(int(base_max), base_min + 1, global_max_cap)

            # jitter but keep feasible
            mn = _clamp(base_min + rng.randint(-2, 3), 1, base_max - 1)
            mx = _clamp(base_max + rng.randint(-10, 11), mn + 1, global_max_cap)
        else:
            mn = rng.randint(min_lo, min_hi)
            mx = mn + rng.randint(5, 75)
            mx = _clamp(mx, mn + 1, global_max_cap)

        limits[str(phase_id)] = {"min_green": int(mn), "max_green": int(mx)}

    return limits


def sample_cycle_constraints(
    phase_limits: Dict[str, Dict[str, int]],
    rng: Optional[random.Random] = None,
    *,
    extra_slack_range: Tuple[int, int] = (5, 120),
) -> Dict[str, int]:
    """
    Sample cycle_min_sec / cycle_max_sec consistent with phase_limits.

    Ensures feasibility:
      sum(min_green) <= cycle_max_sec
      sum(max_green) >= cycle_min_sec
      cycle_min_sec < cycle_max_sec
    """
    if rng is None:
        rng = random.Random()

    mins = [int(v["min_green"]) for v in phase_limits.values()]
    maxs = [int(v["max_green"]) for v in phase_limits.values()]
    sum_min = sum(mins)
    sum_max = sum(maxs)

    # Defensive: enforce at least 1s of slack by bumping max if needed.
    if sum_max <= sum_min:
        sum_max = sum_min + 1

    for _ in range(200):
        # pick a feasible min close to sum_min
        cycle_min = rng.randint(sum_min, min(sum_max - 1, sum_min + 90))

        slack_lo, slack_hi = extra_slack_range
        cycle_max_upper = min(sum_max, cycle_min + rng.randint(slack_lo, slack_hi))
        if cycle_max_upper <= cycle_min:
            continue
        cycle_max = rng.randint(cycle_min + 1, cycle_max_upper)

        # feasibility check
        if cycle_min <= sum_max and cycle_max >= sum_min and cycle_min < cycle_max:
            return {"cycle_min_sec": int(cycle_min), "cycle_max_sec": int(cycle_max)}

    # fallback: widest feasible band
    return {"cycle_min_sec": int(sum_min), "cycle_max_sec": int(max(sum_min + 1, sum_max))}


