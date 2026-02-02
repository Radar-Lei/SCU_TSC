#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置验证测试

测试所有配置类的参数验证逻辑：
- 必需参数缺失
- 参数范围验证
- 类型验证
- 配置覆盖优先级
"""

import pytest
from grpo.config import (
    SFTTrainingConfig,
    GRPOTrainingConfig,
    SimulationConfig,
    RewardSectionConfig,
    FormatRewardSectionConfig,
    TSCRewardSectionConfig,
    TrainingConfig,
    load_training_config,
)


class TestSFTTrainingConfig:
    """测试SFTTrainingConfig验证"""

    def test_learning_rate_validation(self):
        """测试学习率范围验证"""
        # 学习率 > 1 应该失败
        with pytest.raises(ValueError, match="learning_rate.*范围"):
            SFTTrainingConfig(learning_rate=2.0)

        # 学习率 <= 0 应该失败
        with pytest.raises(ValueError, match="learning_rate.*范围"):
            SFTTrainingConfig(learning_rate=0.0)

        with pytest.raises(ValueError, match="learning_rate.*范围"):
            SFTTrainingConfig(learning_rate=-1.0)

        # 正常学习率应该成功
        config = SFTTrainingConfig(learning_rate=0.5)
        assert config.learning_rate == 0.5

    def test_batch_size_validation(self):
        """测试批次大小验证"""
        with pytest.raises(ValueError, match="batch_size.*大于0"):
            SFTTrainingConfig(batch_size=0)

        with pytest.raises(ValueError, match="batch_size.*大于0"):
            SFTTrainingConfig(batch_size=-1)

        # 正常批次大小应该成功
        config = SFTTrainingConfig(batch_size=4)
        assert config.batch_size == 4

    def test_lora_rank_validation(self):
        """测试LoRA秩验证"""
        with pytest.raises(ValueError, match="lora_rank.*大于0"):
            SFTTrainingConfig(lora_rank=0)

        with pytest.raises(ValueError, match="lora_rank.*大于0"):
            SFTTrainingConfig(lora_rank=-1)

        # 正常LoRA秩应该成功
        config = SFTTrainingConfig(lora_rank=64)
        assert config.lora_rank == 64

    def test_eval_percent_validation(self):
        """测试验证集比例验证"""
        # eval_percent必须在(0, 1)范围内
        with pytest.raises(ValueError, match="eval_percent.*范围"):
            SFTTrainingConfig(eval_percent=0.0)

        with pytest.raises(ValueError, match="eval_percent.*范围"):
            SFTTrainingConfig(eval_percent=1.0)

        with pytest.raises(ValueError, match="eval_percent.*范围"):
            SFTTrainingConfig(eval_percent=-0.1)

        with pytest.raises(ValueError, match="eval_percent.*范围"):
            SFTTrainingConfig(eval_percent=1.5)

        # 正常比例应该成功
        config = SFTTrainingConfig(eval_percent=0.1)
        assert config.eval_percent == 0.1

    def test_num_epochs_validation(self):
        """测试训练轮数验证"""
        with pytest.raises(ValueError, match="num_epochs.*大于0"):
            SFTTrainingConfig(num_epochs=0)

        with pytest.raises(ValueError, match="num_epochs.*大于0"):
            SFTTrainingConfig(num_epochs=-1)

        # 正常轮数应该成功
        config = SFTTrainingConfig(num_epochs=5)
        assert config.num_epochs == 5


class TestGRPOTrainingConfig:
    """测试GRPOTrainingConfig验证"""

    def test_learning_rate_validation(self):
        """测试学习率验证"""
        with pytest.raises(ValueError, match="learning_rate.*大于0"):
            GRPOTrainingConfig(model_path="dummy", learning_rate=0.0)

        with pytest.raises(ValueError, match="learning_rate.*大于0"):
            GRPOTrainingConfig(model_path="dummy", learning_rate=-1.0)

        # 正常学习率应该成功
        config = GRPOTrainingConfig(model_path="dummy", learning_rate=1.0e-4)
        assert config.learning_rate == 1.0e-4

    def test_num_train_epochs_validation(self):
        """测试训练轮数验证"""
        with pytest.raises(ValueError, match="num_train_epochs.*大于0"):
            GRPOTrainingConfig(model_path="dummy", num_train_epochs=0)

        with pytest.raises(ValueError, match="num_train_epochs.*大于0"):
            GRPOTrainingConfig(model_path="dummy", num_train_epochs=-1)

        # 正常轮数应该成功
        config = GRPOTrainingConfig(model_path="dummy", num_train_epochs=5)
        assert config.num_train_epochs == 5

    def test_gradient_accumulation_steps_validation(self):
        """测试梯度累积步数验证"""
        with pytest.raises(ValueError, match="gradient_accumulation_steps.*大于0"):
            GRPOTrainingConfig(model_path="dummy", gradient_accumulation_steps=0)

        with pytest.raises(ValueError, match="gradient_accumulation_steps.*大于0"):
            GRPOTrainingConfig(model_path="dummy", gradient_accumulation_steps=-1)

        # 正常步数应该成功
        config = GRPOTrainingConfig(model_path="dummy", gradient_accumulation_steps=8)
        assert config.gradient_accumulation_steps == 8

    def test_repetition_penalty_validation(self):
        """测试重复惩罚验证"""
        with pytest.raises(ValueError, match="repetition_penalty.*范围"):
            GRPOTrainingConfig(model_path="dummy", repetition_penalty=-0.1)

        with pytest.raises(ValueError, match="repetition_penalty.*范围"):
            GRPOTrainingConfig(model_path="dummy", repetition_penalty=2.5)

        # 正常惩罚值应该成功
        config = GRPOTrainingConfig(model_path="dummy", repetition_penalty=1.2)
        assert config.repetition_penalty == 1.2


class TestSimulationConfig:
    """测试SimulationConfig验证"""

    def test_time_step_validation(self):
        """测试时间步长验证"""
        with pytest.raises(ValueError, match="time_step.*大于0"):
            SimulationConfig(time_step=0.0)

        with pytest.raises(ValueError, match="time_step.*大于0"):
            SimulationConfig(time_step=-1.0)

        # 正常步长应该成功
        config = SimulationConfig(time_step=0.5)
        assert config.time_step == 0.5

    def test_green_time_validation(self):
        """测试绿灯时间验证"""
        # min_green_time >= max_green_time 应该失败
        with pytest.raises(ValueError, match="min_green.*max_green"):
            SimulationConfig(min_green_time=60, max_green_time=30)

        with pytest.raises(ValueError, match="min_green.*max_green"):
            SimulationConfig(min_green_time=30, max_green_time=30)

        # 正常时间应该成功
        config = SimulationConfig(min_green_time=10, max_green_time=60)
        assert config.min_green_time == 10
        assert config.max_green_time == 60

    def test_extend_seconds_validation(self):
        """测试延长秒数验证"""
        with pytest.raises(ValueError, match="extend_seconds.*大于0"):
            SimulationConfig(extend_seconds=0)

        with pytest.raises(ValueError, match="extend_seconds.*大于0"):
            SimulationConfig(extend_seconds=-5)

        # 正常秒数应该成功
        config = SimulationConfig(extend_seconds=10)
        assert config.extend_seconds == 10

    def test_max_time_validation(self):
        """测试最大时间验证"""
        with pytest.raises(ValueError, match="max_time.*大于0"):
            SimulationConfig(max_time=0)

        with pytest.raises(ValueError, match="max_time.*大于0"):
            SimulationConfig(max_time=-100)

        # 正常时间应该成功
        config = SimulationConfig(max_time=7200)
        assert config.max_time == 7200

    def test_offset_range_validation(self):
        """测试偏移范围验证"""
        with pytest.raises(ValueError, match="min_green_offset_range.*非负"):
            SimulationConfig(min_green_offset_range=-1.0)

        with pytest.raises(ValueError, match="max_green_offset_range.*非负"):
            SimulationConfig(max_green_offset_range=-1.0)

        # 正常范围应该成功
        config = SimulationConfig(min_green_offset_range=3.0, max_green_offset_range=6.0)
        assert config.min_green_offset_range == 3.0
        assert config.max_green_offset_range == 6.0

    def test_max_workers_validation(self):
        """测试最大工作进程数验证"""
        with pytest.raises(ValueError, match="max_workers.*非负"):
            SimulationConfig(max_workers=-1)

        # 正常进程数应该成功
        config = SimulationConfig(max_workers=8)
        assert config.max_workers == 8

    def test_port_range_validation(self):
        """测试端口范围验证"""
        # 长度不是2
        with pytest.raises(ValueError, match="port_range.*start.*end"):
            SimulationConfig(port_range=[10000])

        with pytest.raises(ValueError, match="port_range.*start.*end"):
            SimulationConfig(port_range=[10000, 20000, 30000])

        # start >= end
        with pytest.raises(ValueError, match="port_range.*start.*end"):
            SimulationConfig(port_range=[20000, 10000])

        with pytest.raises(ValueError, match="port_range.*start.*end"):
            SimulationConfig(port_range=[10000, 10000])

        # 正常范围应该成功
        config = SimulationConfig(port_range=[10000, 60000])
        assert config.port_range == [10000, 60000]


class TestRewardConfig:
    """测试Reward配置验证"""

    def test_format_reward_validation(self):
        """测试Format reward验证"""
        # strict < partial 应该失败
        with pytest.raises(ValueError, match="strict.*partial"):
            FormatRewardSectionConfig(strict=0.5, partial=1.0, invalid=-10.0)

        # partial < invalid 应该失败（-10 < -5）
        with pytest.raises(ValueError, match="partial.*invalid"):
            FormatRewardSectionConfig(strict=1.0, partial=-10.0, invalid=-5.0)

        # 正常值应该成功
        config = FormatRewardSectionConfig(strict=1.0, partial=-0.5, invalid=-10.0)
        assert config.strict == 1.0
        assert config.partial == -0.5
        assert config.invalid == -10.0

    def test_tsc_reward_validation(self):
        """测试TSC reward验证"""
        with pytest.raises(ValueError, match="reward_scale.*大于0"):
            TSCRewardSectionConfig(reward_scale=0.0)

        with pytest.raises(ValueError, match="reward_scale.*大于0"):
            TSCRewardSectionConfig(reward_scale=-1.0)

        # 正常值应该成功
        config = TSCRewardSectionConfig(reward_scale=20.0)
        assert config.reward_scale == 20.0

    def test_reward_chain_validation(self):
        """测试reward chain权重验证"""
        # format_weight < 0 应该失败
        with pytest.raises(ValueError, match="format_weight.*非负"):
            RewardSectionConfig(chain={"format_weight": -1.0, "tsc_weight": 1.0})

        # tsc_weight < 0 应该失败
        with pytest.raises(ValueError, match="tsc_weight.*非负"):
            RewardSectionConfig(chain={"format_weight": 1.0, "tsc_weight": -1.0})

        # 正常值应该成功
        config = RewardSectionConfig(chain={"format_weight": 2.0, "tsc_weight": 1.0})
        assert config.chain["format_weight"] == 2.0
        assert config.chain["tsc_weight"] == 1.0


class TestTrainingConfig:
    """测试TrainingConfig验证"""

    def test_missing_required_parameters(self):
        """测试必需参数缺失"""
        # 缺少grpo
        with pytest.raises(ValueError, match="grpo.*必需"):
            TrainingConfig(
                training={"sft": {}},
                simulation={},
                reward={},
                paths={},
                logging={}
            )

        # 缺少sft
        with pytest.raises(ValueError, match="sft.*必需"):
            TrainingConfig(
                training={"grpo": {}},
                simulation={},
                reward={},
                paths={},
                logging={}
            )

    def test_full_config_loading(self):
        """测试完整配置加载"""
        # 这个测试需要config/training_config.yaml存在
        import os
        config_path = "config/training_config.yaml"
        if not os.path.exists(config_path):
            pytest.skip(f"{config_path} not found")

        config = load_training_config(config_path)

        # 验证SFT配置
        sft = config.sft
        assert sft.learning_rate > 0
        assert sft.batch_size > 0

        # 验证GRPO配置
        grpo = config.grpo
        assert grpo.learning_rate > 0
        assert grpo.batch_size > 0

        # 验证路径配置
        paths = config.paths
        assert paths.sft_dataset_dir
        assert paths.grpo_dataset_dir


class TestConfigLoading:
    """测试配置文件加载"""

    def test_load_valid_config(self, temp_config_file, sample_config_data):
        """测试加载有效配置文件"""
        config_path = temp_config_file(sample_config_data)

        config = load_training_config(config_path)

        # 验证SFT配置
        sft = config.sft
        assert sft.learning_rate == 2.0e-4
        assert sft.batch_size == 2
        assert sft.lora_rank == 32

        # 验证GRPO配置
        grpo = config.grpo
        assert grpo.learning_rate == 1.0e-5
        assert grpo.batch_size == 2

        # 验证路径配置
        paths = config.paths
        assert "/home/samuel/SCU_TSC/data" in paths.data_dir

    def test_load_missing_file(self):
        """测试加载不存在的配置文件"""
        with pytest.raises(FileNotFoundError):
            load_training_config("/nonexistent/config.yaml")

    def test_load_invalid_yaml(self, temp_config_file):
        """测试加载无效YAML"""
        # 创建无效YAML文件
        import tempfile
        import os

        fd, path = tempfile.mkstemp(suffix='.yaml', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                f.write("invalid: yaml: content: :\n")  # 无效YAML

            with pytest.raises(Exception):  # YAMLError
                load_training_config(path)
        finally:
            os.unlink(path) if os.path.exists(path) else None


class TestConfigOverride:
    """测试配置覆盖"""

    def test_nested_config_structure(self, temp_config_file, sample_config_data):
        """测试嵌套配置结构"""
        config_path = temp_config_file(sample_config_data)
        config = load_training_config(config_path)

        # 测试嵌套的reward配置
        assert config.reward.format.strict == 1.0
        assert config.reward.format.partial == -0.5
        assert config.reward.format.invalid == -10.0

        # 测试嵌套的chain配置
        assert config.reward.chain["format_weight"] == 1.0
        assert config.reward.chain["tsc_weight"] == 1.0

    def test_partial_override(self, temp_config_file, sample_config_data):
        """测试部分覆盖配置"""
        # 修改部分配置
        modified_data = sample_config_data.copy()
        modified_data["training"]["sft"]["learning_rate"] = 1.0e-3

        config_path = temp_config_file(modified_data)
        config = load_training_config(config_path)

        # 验证覆盖的值
        assert config.sft.learning_rate == 1.0e-3

        # 验证其他值未变
        assert config.sft.batch_size == 2

    def test_property_methods(self, temp_config_file, sample_config_data):
        """测试property方法"""
        config_path = temp_config_file(sample_config_data)
        config = load_training_config(config_path)

        # 测试sft property
        sft = config.sft
        assert isinstance(sft, SFTTrainingConfig)
        assert hasattr(sft, 'learning_rate')

        # 测试grpo property
        grpo = config.grpo
        assert isinstance(grpo, GRPOTrainingConfig)
        assert hasattr(grpo, 'learning_rate')

        # 测试sumo property
        sumo = config.sumo
        assert isinstance(sumo, SimulationConfig)
        assert sumo.time_step == 1.0

    def test_reward_chain_weights(self, temp_config_file, sample_config_data):
        """测试reward chain权重配置"""
        config_path = temp_config_file(sample_config_data)
        config = load_training_config(config_path)

        # 访问嵌套的reward配置
        assert config.reward.chain["format_weight"] == 1.0
        assert config.reward.chain["tsc_weight"] == 1.0

        # 修改权重
        modified_data = sample_config_data.copy()
        modified_data["reward"]["chain"]["format_weight"] = 2.0
        modified_data["reward"]["chain"]["tsc_weight"] = 0.5

        config_path = temp_config_file(modified_data)
        config = load_training_config(config_path)

        assert config.reward.chain["format_weight"] == 2.0
        assert config.reward.chain["tsc_weight"] == 0.5


class TestConfigIntegrationWithSampleData:
    """测试配置与样本数据的集成"""

    def test_config_with_sample_prompt_data(self, sample_prompt_data):
        """测试配置与样本prompt数据"""
        # 只验证样本数据结构正确
        assert "state" in sample_prompt_data
        assert "current_phase_id" in sample_prompt_data["state"]
        assert "phase_order" in sample_prompt_data
        assert isinstance(sample_prompt_data["phase_order"], list)

    def test_config_with_sample_config_data(self, sample_config_data):
        """测试配置与样本配置数据"""
        # 验证必需的顶级键
        assert "training" in sample_config_data
        assert "simulation" in sample_config_data
        assert "reward" in sample_config_data
        assert "paths" in sample_config_data

        # 验证嵌套结构
        assert "sft" in sample_config_data["training"]
        assert "grpo" in sample_config_data["training"]

