# -*- coding: utf-8 -*-
"""
GRPO数据集生成器配置模块

所有可配置参数集中在此文件，便于用户修改。
"""

from dataclasses import dataclass, field
from typing import List, Optional
import os


@dataclass
class GRPOConfig:
    """GRPO数据集生成配置"""
    
    # ============== 决策参数 ==============
    # 每次决策延长的秒数
    extend_seconds: int = 5
    
    # 最小绿灯时间偏移范围 (秒)，用于增加数据多样性
    # 实际最小绿 = SUMO配置最小绿 + random.uniform(-min_green_offset_range, +min_green_offset_range)
    min_green_offset_range: float = 2.0
    
    # 最大绿灯时间偏移范围 (秒)
    max_green_offset_range: float = 5.0
    
    # 默认最小绿灯时间 (秒)，当SUMO配置中无法获取时使用
    default_min_green: float = 10.0
    
    # 默认最大绿灯时间 (秒)
    default_max_green: float = 60.0
    
    # ============== 仿真参数 ==============
    # 预热步数（让车辆进入路网）
    warmup_steps: int = 300
    
    # 仿真步长 (秒)
    step_length: float = 1.0
    
    # 是否使用GUI（生成数据时建议关闭）
    use_gui: bool = False
    
    # ============== 并行参数 ==============
    # 并行进程数（0表示使用CPU核心数）
    num_workers: int = 0
    
    # ============== 路径参数 ==============
    # SUMO仿真场景根目录
    scenarios_dir: str = "/home/samuel/SCU_TSC/sumo_simulation/environments"
    
    # 数据输出根目录
    output_dir: str = "/home/samuel/SCU_TSC/data/grpo_datasets"
    
    # ============== 数据参数 ==============
    # 仿真状态保存间隔（每N个决策点保存一次状态文件）
    # 设为1表示每个决策点都保存
    state_save_interval: int = 1
    
    # ============== 场景过滤 ==============
    # 要处理的场景列表（空列表表示处理所有场景）
    scenarios: List[str] = field(default_factory=list)
    
    # 排除的场景列表
    exclude_scenarios: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """初始化后处理"""
        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 自动检测并行进程数
        if self.num_workers == 0:
            import multiprocessing
            self.num_workers = max(1, multiprocessing.cpu_count() - 1)


# 默认配置实例
DEFAULT_CONFIG = GRPOConfig()


# 系统Prompt模板
SYSTEM_PROMPT = """你是交通信号控制优化专家。

你将收到一个路口在当前时刻的相位排队信息，需要判断是否延长"当前绿灯相位"。

【extend_decision_input_json】
{extend_decision_input_json}
【/extend_decision_input_json】

字段含义（仅说明含义）：
- phase_order：相位执行顺序，循环执行；不可跳相、不可重排，切换相位只能切换到当前相位的下一个相位。
- state.current_phase_id：当前正在放行的相位 ID。
- state.phase_metrics_by_id[phase_id].avg_queue_veh：该相位绿灯所控制车道在当前时刻的平均排队车辆数（辆）。

任务（必须完成）：
- 基于输入 JSON 的 state 与 phase_order，判断是否需要延长当前绿灯相位。

决策要求（必须遵守）：
1) 你必须显式使用 avg_queue_veh 做决策：至少比较"当前相位"与"其他相位"的 avg_queue_veh 相对大小后再给出结论。
2) 延长是一个"相对需求"决策：
   - 当前相位 avg_queue_veh 较大，且明显高于多数其他相位时，更倾向延长；
   - 若存在一个或多个后续相位 avg_queue_veh 明显更大（例如显著高于当前相位），更倾向不延长以尽快切换；
3) 不得编造任何不存在的观测数据；只能使用输入 JSON 中给出的字段与数值。

输出要求（必须严格遵守）：
- 只输出最终 JSON（不要任何说明、不要 Markdown、不要额外文本、不要输出推理过程）。
- JSON 顶层必须是对象，且仅包含一个字段：
  {"extend": "<yes/no>"}
- extend 的取值只能是"yes"或"no"，不允许输出其它字段或其它取值。
"""
