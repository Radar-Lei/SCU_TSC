import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class TLPhase:
    """A single SUMO tlLogic phase parsed from net.xml."""

    index_0_based: int
    duration: Optional[int]
    min_dur: Optional[int]
    max_dur: Optional[int]
    state: Optional[str]


def parse_tl_phases_from_net(net_xml_path: str, tl_id: str) -> List[TLPhase]:
    """
    Parse tlLogic phases for a given traffic light id from a SUMO net.xml.

    Notes:
    - Some net.xml may omit minDur/maxDur; we keep them as None in that case.
    - We parse only the first matching <tlLogic id="...">.
    """
    phases: List[TLPhase] = []
    in_target = False
    phase_idx = 0

    for event, elem in ET.iterparse(net_xml_path, events=("start", "end")):
        if event == "start" and elem.tag == "tlLogic":
            in_target = (elem.attrib.get("id") == tl_id)
            phase_idx = 0

        if event == "end" and elem.tag == "phase" and in_target:
            def _to_int(x: Optional[str]) -> Optional[int]:
                if x is None:
                    return None
                try:
                    return int(float(x))
                except Exception:
                    return None

            duration = _to_int(elem.attrib.get("duration"))
            min_dur = _to_int(elem.attrib.get("minDur"))
            max_dur = _to_int(elem.attrib.get("maxDur"))
            state = elem.attrib.get("state")
            phases.append(
                TLPhase(
                    index_0_based=phase_idx,
                    duration=duration,
                    min_dur=min_dur,
                    max_dur=max_dur,
                    state=state,
                )
            )
            phase_idx += 1
            elem.clear()

        if event == "end" and elem.tag == "tlLogic":
            if in_target:
                # done with target tlLogic
                break
            in_target = False
            elem.clear()

    return phases


def get_phase_order_one_based(net_xml_path: str, tl_id: str) -> List[int]:
    """Return phase order as 1-based list [1..N] for this tl_id."""
    phases = parse_tl_phases_from_net(net_xml_path, tl_id)
    n = len(phases)
    return list(range(1, n + 1))


def get_net_phase_minmax_one_based(net_xml_path: str, tl_id: str) -> Dict[int, Tuple[int, int]]:
    """
    Return {phase_id_1_based: (minDur, maxDur)} for phases that have both.
    """
    out: Dict[int, Tuple[int, int]] = {}
    phases = parse_tl_phases_from_net(net_xml_path, tl_id)
    for p in phases:
        if p.min_dur is None or p.max_dur is None:
            continue
        if p.max_dur <= 0:
            continue
        mn = max(1, int(p.min_dur))
        mx = max(mn + 1, int(p.max_dur))
        out[p.index_0_based + 1] = (mn, mx)
    return out


def _is_green_phase_state(state: Optional[str]) -> bool:
    """判断相位 state 字符串是否包含绿灯"""
    if not state:
        return False
    return ("G" in state) or ("g" in state)


def get_green_phase_order_one_based(net_xml_path: str, tl_id: str) -> List[int]:
    """
    Return 1-based phase IDs that contain green light (G/g).
    
    过滤掉黄灯/全红等过渡相位，只返回包含绿灯信号的相位。
    """
    phases = parse_tl_phases_from_net(net_xml_path, tl_id)
    return [p.index_0_based + 1 for p in phases if _is_green_phase_state(p.state)]


