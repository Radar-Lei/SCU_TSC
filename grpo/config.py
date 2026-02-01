# -*- coding: utf-8 -*-
"""
GRPO配置模块

包含两个配置类：
1. GRPOConfig: 数据集生成配置（原有的）
2. GRPOTrainingConfig: GRPO训练配置（新增）
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import os
import yaml


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


@dataclass
class GRPOTrainingConfig:
    """GRPO训练配置"""

    # ============== 模型配置 ==============
    model_path: str
    max_seq_length: int = 2048

    # ============== GRPO核心参数 ==============
    learning_rate: float = 1.0e-5
    batch_size: int = 2
    gradient_accumulation_steps: int = 4
    num_generations: int = 4
    temperature: float = 0.9
    kl_coeff: float = 0.1

    # ============== 生成控制参数 ==============
    max_new_tokens: int = 50
    top_p: float = 0.9
    repetition_penalty: float = 1.0

    # ============== 训练参数 ==============
    num_train_epochs: int = 3
    warmup_steps: int = 10
    logging_steps: int = 5
    save_steps: int = 50
    optim: str = "adamw_8bit"

    # ============== Reward权重 ==============
    format_weight: float = 1.0
    tsc_weight: float = 1.0

    # ============== SUMO仿真参数 ==============
    max_workers: int = 4
    extend_seconds: int = 5

    # ============== 数据路径 ==============
    dataset_path: str = "/home/samuel/SCU_TSC/data/grpo_datasets"

    # ============== 输出路径 ==============
    output_dir: str = "/home/samuel/SCU_TSC/model/grpo_model"

    # ============== 日志配置 ==============
    use_wandb: bool = False
    wandb_project: str = "scu-tsc-grpo"
    wandb_run_name: Optional[str] = None

    # ============== 高级参数 ==============
    lora_rank: int = 32
    gradient_checkpointing: bool = True
    seed: int = 3407

    def __post_init__(self):
        """参数验证"""
        # 验证数值范围
        if self.learning_rate <= 0:
            raise ValueError(f"learning_rate必须大于0，当前值: {self.learning_rate}")

        if self.batch_size <= 0:
            raise ValueError(f"batch_size必须大于0，当前值: {self.batch_size}")

        if self.num_generations <= 0:
            raise ValueError(f"num_generations必须大于0，当前值: {self.num_generations}")

        if not (0 <= self.temperature <= 2):
            raise ValueError(f"temperature必须在[0, 2]范围内，当前值: {self.temperature}")

        if not (0 <= self.top_p <= 1):
            raise ValueError(f"top_p必须在[0, 1]范围内，当前值: {self.top_p}")

        if self.kl_coeff < 0:
            raise ValueError(f"kl_coeff必须非负，当前值: {self.kl_coeff}")

        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)

    @classmethod
    def from_yaml(cls, path: str) -> "GRPOTrainingConfig":
        """
        从YAML文件加载配置

        Args:
            path: YAML配置文件路径

        Returns:
            GRPOTrainingConfig实例
        """
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        # 处理wandb_run_name为None的情况
        if "wandb_run_name" in data and data["wandb_run_name"] == "null":
            data["wandb_run_name"] = None

        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典

        Returns:
            配置字典
        """
        return {
            "model_path": self.model_path,
            "max_seq_length": self.max_seq_length,
            "learning_rate": self.learning_rate,
            "batch_size": self.batch_size,
            "gradient_accumulation_steps": self.gradient_accumulation_steps,
            "num_generations": self.num_generations,
            "temperature": self.temperature,
            "kl_coeff": self.kl_coeff,
            "max_new_tokens": self.max_new_tokens,
            "top_p": self.top_p,
            "repetition_penalty": self.repetition_penalty,
            "num_train_epochs": self.num_train_epochs,
            "warmup_steps": self.warmup_steps,
            "logging_steps": self.logging_steps,
            "save_steps": self.save_steps,
            "optim": self.optim,
            "format_weight": self.format_weight,
            "tsc_weight": self.tsc_weight,
            "max_workers": self.max_workers,
            "extend_seconds": self.extend_seconds,
            "dataset_path": self.dataset_path,
            "output_dir": self.output_dir,
            "use_wandb": self.use_wandb,
            "wandb_project": self.wandb_project,
            "wandb_run_name": self.wandb_run_name,
            "lora_rank": self.lora_rank,
            "gradient_checkpointing": self.gradient_checkpointing,
            "seed": self.seed,
        }


def load_config(path: str) -> GRPOTrainingConfig:
    """
    便捷函数：加载GRPO训练配置

    Args:
        path: YAML配置文件路径

    Returns:
        GRPOTrainingConfig实例
    """
    return GRPOTrainingConfig.from_yaml(path)

