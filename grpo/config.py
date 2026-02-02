# -*- coding: utf-8 -*-
"""
GRPO配置模块

包含多个配置类：
1. GRPOConfig: 数据集生成配置（原有的）
2. GRPOTrainingConfig: GRPO训练配置（用于grpo_config.yaml）
3. TrainingConfig: 中央训练配置（用于training_config.yaml）
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from pathlib import Path
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
class FormatRewardConfig:
    """Format Reward配置"""

    strict: float = 1.0
    partial: float = -0.5
    invalid: float = -10.0
    extract_regex: str = r'\{["\s]*extend["\s]*:\s*["\s]*(yes|no)["\s]*(?:,|\})'


@dataclass
class SUMOConfig:
    """SUMO仿真配置"""
    max_workers: int = 4
    port_range: List[int] = field(default_factory=lambda: [10000, 60000])
    extend_seconds: int = 5
    reward_scale: float = 10.0


@dataclass
class RewardChainConfig:
    """Reward函数链配置"""
    format_weight: float = 1.0
    tsc_weight: float = 1.0


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

    # ============== 嵌套配置 ==============
    reward: RewardChainConfig = field(default_factory=RewardChainConfig)
    format_reward: FormatRewardConfig = field(default_factory=FormatRewardConfig)
    sumo: SUMOConfig = field(default_factory=SUMOConfig)

    def __post_init__(self):
        """参数验证"""
        # 验证数值范围
        if self.learning_rate <= 0:
            raise ValueError(f"grpo.learning_rate必须大于0，当前值: {self.learning_rate}")

        if self.batch_size <= 0:
            raise ValueError(f"grpo.batch_size必须大于0，当前值: {self.batch_size}")

        if self.num_generations <= 0:
            raise ValueError(f"grpo.num_generations必须大于0，当前值: {self.num_generations}")

        if not (0 <= self.temperature <= 2):
            raise ValueError(f"grpo.temperature必须在[0, 2]范围内，当前值: {self.temperature}")

        if not (0 <= self.top_p <= 1):
            raise ValueError(f"grpo.top_p必须在[0, 1]范围内，当前值: {self.top_p}")

        if self.kl_coeff < 0:
            raise ValueError(f"grpo.kl_coeff必须非负，当前值: {self.kl_coeff}")

        # 新增验证
        if self.num_train_epochs <= 0:
            raise ValueError(f"grpo.num_train_epochs必须大于0，当前值: {self.num_train_epochs}")

        if self.gradient_accumulation_steps <= 0:
            raise ValueError(f"grpo.gradient_accumulation_steps必须大于0，当前值: {self.gradient_accumulation_steps}")

        if not (0 <= self.repetition_penalty <= 2):
            raise ValueError(f"grpo.repetition_penalty必须在[0, 2]范围内，当前值: {self.repetition_penalty}")

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

        # 处理嵌套配置
        reward_data = data.pop('reward', {})
        format_data = data.pop('format_reward', {})
        sumo_data = data.pop('sumo', {})

        return cls(
            reward=RewardChainConfig(**reward_data),
            format_reward=FormatRewardConfig(**format_data),
            sumo=SUMOConfig(**sumo_data),
            **data
        )

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
            "dataset_path": self.dataset_path,
            "output_dir": self.output_dir,
            "use_wandb": self.use_wandb,
            "wandb_project": self.wandb_project,
            "wandb_run_name": self.wandb_run_name,
            "lora_rank": self.lora_rank,
            "gradient_checkpointing": self.gradient_checkpointing,
            "seed": self.seed,
            "reward": {
                "format_weight": self.reward.format_weight,
                "tsc_weight": self.reward.tsc_weight,
            },
            "format_reward": {
                "strict": self.format_reward.strict,
                "partial": self.format_reward.partial,
                "invalid": self.format_reward.invalid,
                "extract_regex": self.format_reward.extract_regex,
            },
            "sumo": {
                "max_workers": self.sumo.max_workers,
                "port_range": self.sumo.port_range,
                "extend_seconds": self.sumo.extend_seconds,
                "reward_scale": self.sumo.reward_scale,
            },
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


# ============== 中央训练配置类 ==============

@dataclass
class SFTTrainingConfig:
    """SFT训练配置"""

    # ============== 模型配置 ==============
    model_name: str = "unsloth/Qwen2.5-0.5B-Instruct"
    max_seq_length: int = 2048
    lora_rank: int = 32

    # ============== 训练参数 ==============
    num_epochs: int = 3
    batch_size: int = 2
    gradient_accumulation_steps: int = 4
    learning_rate: float = 2.0e-4
    max_steps: Optional[int] = None
    warmup_steps: int = 5
    optim: str = "adamw_8bit"
    weight_decay: float = 0.001
    lr_scheduler_type: str = "linear"
    seed: int = 3407

    # ============== 日志和保存 ==============
    logging_steps: int = 5
    save_steps: int = 50

    # ============== 评估参数 ==============
    eval_percent: float = 0.05
    eval_limit: int = 100
    eval_steps: int = 30

    def __post_init__(self):
        """参数验证"""
        # 数值范围验证
        if self.learning_rate <= 0 or self.learning_rate > 1:
            raise ValueError(f"sft.learning_rate必须在(0, 1]范围内，当前值: {self.learning_rate}")

        if self.batch_size <= 0:
            raise ValueError(f"sft.batch_size必须大于0，当前值: {self.batch_size}")

        if self.lora_rank <= 0:
            raise ValueError(f"sft.lora_rank必须大于0，当前值: {self.lora_rank}")

        if not (0 < self.eval_percent < 1):
            raise ValueError(f"sft.eval_percent必须在(0, 1)范围内，当前值: {self.eval_percent}")

        if self.num_epochs <= 0:
            raise ValueError(f"sft.num_epochs必须大于0，当前值: {self.num_epochs}")


@dataclass
class SimulationConfig:
    """SUMO仿真配置"""

    # 时间参数
    time_step: float = 1.0
    max_time: int = 3600
    warmup_steps: int = 300

    # 绿灯时间参数
    extend_seconds: int = 5
    min_green_time: float = 10.0
    max_green_time: float = 60.0
    min_green_offset_range: float = 2.0
    max_green_offset_range: float = 5.0
    default_min_green: float = 10.0
    default_max_green: float = 60.0

    # 并行参数
    max_workers: int = 4
    port_range: List[int] = field(default_factory=lambda: [10000, 60000])

    def __post_init__(self):
        """参数验证"""
        if self.time_step <= 0:
            raise ValueError(f"simulation.time_step必须大于0，当前值: {self.time_step}")

        if self.max_time <= 0:
            raise ValueError(f"simulation.max_time必须大于0，当前值: {self.max_time}")

        if self.extend_seconds <= 0:
            raise ValueError(f"simulation.extend_seconds必须大于0，当前值: {self.extend_seconds}")

        if self.min_green_time >= self.max_green_time:
            raise ValueError(f"simulation.min_green_time({self.min_green_time})必须小于max_green_time({self.max_green_time})")

        if self.min_green_offset_range < 0:
            raise ValueError(f"simulation.min_green_offset_range必须非负，当前值: {self.min_green_offset_range}")

        if self.max_green_offset_range < 0:
            raise ValueError(f"simulation.max_green_offset_range必须非负，当前值: {self.max_green_offset_range}")

        if self.max_workers < 0:
            raise ValueError(f"simulation.max_workers必须非负，当前值: {self.max_workers}")

        if len(self.port_range) != 2 or self.port_range[0] >= self.port_range[1]:
            raise ValueError(f"simulation.port_range必须是[start, end]格式且start < end，当前值: {self.port_range}")


@dataclass
class ScenariosConfig:
    """场景配置"""
    scenarios_dir: str = "/home/samuel/SCU_TSC/sumo_simulation/environments"
    num_workers: int = 0  # 0表示使用CPU核心数-1


@dataclass
class MaxPressureConfig:
    """Max Pressure配置（预留）"""
    min_green_offset: float = 0.0
    max_green_override: bool = False
    pressure_threshold: float = 0.0


@dataclass
class FormatRewardSectionConfig:
    """Format Reward配置段"""
    strict: float = 1.0
    partial: float = -0.5
    invalid: float = -10.0
    extract_regex: str = r'\{["\s]*extend["\s]*:\s*["\s]*(yes|no)["\s]*(?:,|\})'

    def __post_init__(self):
        """参数验证"""
        # strict应该大于partial
        if self.strict < self.partial:
            raise ValueError(f"reward.format.strict({self.strict})应该大于partial({self.partial})")

        # partial应该大于invalid
        if self.partial < self.invalid:
            raise ValueError(f"reward.format.partial({self.partial})应该大于invalid({self.invalid})")


@dataclass
class TSCRewardSectionConfig:
    """TSC Reward配置段"""
    reward_scale: float = 10.0

    def __post_init__(self):
        """参数验证"""
        if self.reward_scale <= 0:
            raise ValueError(f"reward.tsc.reward_scale必须大于0，当前值: {self.reward_scale}")


@dataclass
class RewardSectionConfig:
    """Reward配置段"""
    chain: Dict[str, float] = field(default_factory=lambda: {"format_weight": 1.0, "tsc_weight": 1.0})
    format: FormatRewardSectionConfig = field(default_factory=FormatRewardSectionConfig)
    tsc: TSCRewardSectionConfig = field(default_factory=TSCRewardSectionConfig)
    max_pressure: MaxPressureConfig = field(default_factory=MaxPressureConfig)

    def __post_init__(self):
        """参数验证"""
        if self.chain.get("format_weight", 1.0) < 0:
            raise ValueError(f"reward.format_weight必须非负，当前值: {self.chain.get('format_weight')}")

        if self.chain.get("tsc_weight", 1.0) < 0:
            raise ValueError(f"reward.tsc_weight必须非负，当前值: {self.chain.get('tsc_weight')}")


@dataclass
class PathsConfig:
    """路径配置"""
    data_dir: str = "/home/samuel/SCU_TSC/data"
    grpo_dataset_dir: str = "/home/samuel/SCU_TSC/data/grpo_datasets"
    sft_dataset_dir: str = "/home/samuel/SCU_TSC/data/sft_datasets"
    sft_model_dir: str = "/home/samuel/SCU_TSC/model/sft_model"
    grpo_model_dir: str = "/home/samuel/SCU_TSC/model/grpo_model"
    grpo_config: str = "/home/samuel/SCU_TSC/config/grpo_config.yaml"


@dataclass
class LoggingConfig:
    """日志配置"""
    use_wandb: bool = False
    wandb_project: str = "scu-tsc-grpo"
    wandb_run_name: Optional[str] = None


@dataclass
class TrainingConfig:
    """中央训练配置类

    从training_config.yaml加载所有训练、仿真、reward和路径配置
    """

    # 原始数据（保留以便访问完整配置）
    training: Dict[str, Any]
    simulation: Dict[str, Any]
    reward: RewardSectionConfig
    paths: PathsConfig
    logging: LoggingConfig

    def __post_init__(self):
        """初始化后处理"""
        # 确保路径配置是PathsConfig实例
        if not isinstance(self.paths, PathsConfig):
            self.paths = PathsConfig(**self.paths)

        # 确保日志配置是LoggingConfig实例
        if not isinstance(self.logging, LoggingConfig):
            # 处理wandb_run_name为null的情况
            if isinstance(self.logging, dict):
                if self.logging.get('wandb_run_name') == 'null':
                    self.logging['wandb_run_name'] = None
            self.logging = LoggingConfig(**self.logging)

        # 确保reward配置是RewardSectionConfig实例
        if not isinstance(self.reward, RewardSectionConfig):
            reward_data = self.reward
            if isinstance(reward_data, dict):
                format_data = reward_data.get('format', {})
                tsc_data = reward_data.get('tsc', {})
                max_pressure_data = reward_data.get('max_pressure', {})
                self.reward = RewardSectionConfig(
                    chain=reward_data.get('chain', {"format_weight": 1.0, "tsc_weight": 1.0}),
                    format=FormatRewardSectionConfig(**format_data),
                    tsc=TSCRewardSectionConfig(**tsc_data),
                    max_pressure=MaxPressureConfig(**max_pressure_data)
                )

        # 验证必需参数存在
        required_training_keys = ['sft', 'grpo']
        for key in required_training_keys:
            if key not in self.training:
                raise ValueError(f"training.{key}是必需参数，但配置文件中缺失")

    @classmethod
    def from_yaml(cls, path: str) -> "TrainingConfig":
        """
        从training_config.yaml加载配置

        Args:
            path: YAML配置文件路径

        Returns:
            TrainingConfig实例
        """
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        # 提取各段
        training_data = data.get('training', {})
        simulation_data = data.get('simulation', {})
        reward_data = data.get('reward', {})
        paths_data = data.get('paths', {})
        logging_data = data.get('logging', {})

        # 构建paths配置
        paths_config = PathsConfig(**paths_data)

        # 构建logging配置
        if logging_data.get('wandb_run_name') == 'null':
            logging_data['wandb_run_name'] = None
        logging_config = LoggingConfig(**logging_data)

        # 构建reward配置
        format_data = reward_data.get('format', {})
        tsc_data = reward_data.get('tsc', {})
        max_pressure_data = reward_data.get('max_pressure', {})
        reward_config = RewardSectionConfig(
            chain=reward_data.get('chain', {"format_weight": 1.0, "tsc_weight": 1.0}),
            format=FormatRewardSectionConfig(**format_data),
            tsc=TSCRewardSectionConfig(**tsc_data),
            max_pressure=MaxPressureConfig(**max_pressure_data)
        )

        return cls(
            training=training_data,
            simulation=simulation_data,
            reward=reward_config,
            paths=paths_config,
            logging=logging_config
        )

    @property
    def sft(self) -> SFTTrainingConfig:
        """返回SFT配置"""
        sft_data = self.training.get('sft', {})
        return SFTTrainingConfig(**sft_data)

    @property
    def grpo(self) -> GRPOTrainingConfig:
        """返回GRPO配置（转换为GRPOTrainingConfig实例）"""
        grpo_data = self.training.get('grpo', {})

        # 构建嵌套配置
        reward_chain_data = {
            "format_weight": self.reward.chain.get("format_weight", 1.0),
            "tsc_weight": self.reward.chain.get("tsc_weight", 1.0)
        }

        format_reward_data = {
            "strict": self.reward.format.strict,
            "partial": self.reward.format.partial,
            "invalid": self.reward.format.invalid,
            "extract_regex": self.reward.format.extract_regex
        }

        sumo_data = {
            "max_workers": self.simulation.get('sumo', {}).get('max_workers', 4),
            "port_range": self.simulation.get('sumo', {}).get('port_range', [10000, 60000]),
            "extend_seconds": self.simulation.get('sumo', {}).get('extend_seconds', 5),
            "reward_scale": self.reward.tsc.reward_scale
        }

        return GRPOTrainingConfig(
            reward=RewardChainConfig(**reward_chain_data),
            format_reward=FormatRewardConfig(**format_reward_data),
            sumo=SUMOConfig(**sumo_data),
            **grpo_data
        )

    @property
    def sumo(self) -> SimulationConfig:
        """返回SUMO仿真配置"""
        sumo_data = self.simulation.get('sumo', {})
        return SimulationConfig(**sumo_data)

    @property
    def scenarios(self) -> ScenariosConfig:
        """返回场景配置"""
        scenarios_data = self.simulation.get('scenarios', {})
        return ScenariosConfig(**scenarios_data)


def load_training_config(path: str = "config/training_config.yaml") -> TrainingConfig:
    """
    便捷函数：加载中央训练配置

    Args:
        path: training_config.yaml路径

    Returns:
        TrainingConfig实例
    """
    return TrainingConfig.from_yaml(path)

