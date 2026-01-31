# -*- coding: utf-8 -*-
"""
Prompt构建器

生成符合用户指定格式的决策Prompt。
"""

import json
from datetime import datetime
from typing import Dict, List, Any


def build_extend_decision_prompt(
    crossing_id: int,
    as_of: str,
    phase_order: List[int],
    current_phase_id: int,
    phase_metrics: Dict[int, float]
) -> str:
    """
    构建延长决策的Prompt
    
    Args:
        crossing_id: 路口ID（数字）
        as_of: 时间戳字符串 (YYYY-MM-DD HH:MM:SS)
        phase_order: 相位执行顺序列表
        current_phase_id: 当前绿灯相位ID
        phase_metrics: 各相位的平均排队车辆数 {phase_id: avg_queue_veh}
        
    Returns:
        JSON格式的prompt字符串
    """
    # 构建phase_metrics_by_id
    phase_metrics_by_id = {
        str(phase_id): {"avg_queue_veh": round(avg_queue, 2)}
        for phase_id, avg_queue in phase_metrics.items()
    }
    
    # 构建完整的输入JSON
    input_json = {
        "crossing_id": crossing_id,
        "as_of": as_of,
        "phase_order": phase_order,
        "state": {
            "current_phase_id": current_phase_id,
            "phase_metrics_by_id": phase_metrics_by_id
        }
    }
    
    return json.dumps(input_json, ensure_ascii=False, indent=2)


def build_full_prompt(
    crossing_id: int,
    as_of: str,
    phase_order: List[int],
    current_phase_id: int,
    phase_metrics: Dict[int, float],
    system_prompt_template: str
) -> str:
    """
    构建完整的Prompt（包含系统提示和输入JSON）
    
    Args:
        crossing_id: 路口ID
        as_of: 时间戳
        phase_order: 相位顺序
        current_phase_id: 当前相位ID
        phase_metrics: 各相位平均排队数
        system_prompt_template: 系统提示模板
        
    Returns:
        完整的prompt字符串
    """
    input_json = build_extend_decision_prompt(
        crossing_id=crossing_id,
        as_of=as_of,
        phase_order=phase_order,
        current_phase_id=current_phase_id,
        phase_metrics=phase_metrics
    )
    
    return system_prompt_template.format(extend_decision_input_json=input_json)


def generate_timestamp(simulation_time: float, base_date: str = "2025-01-01") -> str:
    """
    根据仿真时间生成时间戳字符串
    
    Args:
        simulation_time: 仿真时间（秒）
        base_date: 基准日期
        
    Returns:
        YYYY-MM-DD HH:MM:SS 格式的时间戳
    """
    base = datetime.strptime(base_date, "%Y-%m-%d")
    hours = int(simulation_time // 3600)
    minutes = int((simulation_time % 3600) // 60)
    seconds = int(simulation_time % 60)
    
    result = base.replace(
        hour=hours % 24,
        minute=minutes,
        second=seconds
    )
    return result.strftime("%Y-%m-%d %H:%M:%S")
