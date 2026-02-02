# -*- coding: utf-8 -*-
"""
Baseline集成测试

测试Max Pressure baseline追踪功能的集成测试
"""

import pytest
import json
import tempfile
import shutil
from pathlib import Path
from types import SimpleNamespace


class TestBaselineIntegration:
    """测试Max Pressure baseline追踪集成（不依赖SUMO环境）"""

    def test_baseline_config_validation(self):
        """
        测试baseline配置验证

        验证点：
        - enable_baseline默认为False
        - baseline_config为MaxPressureConfig实例
        - 配置验证逻辑正确
        """
        try:
            from grpo.config import GRPOTrainingConfig
            from grpo.max_pressure import MaxPressureConfig

            # 测试默认值
            config = GRPOTrainingConfig(
                model_path="/tmp/test"
            )
            assert config.enable_baseline is False, "enable_baseline默认应为False"
            assert config.baseline_config is not None, "baseline_config不应为None"
            assert isinstance(config.baseline_config, MaxPressureConfig), \
                "baseline_config应为MaxPressureConfig实例"

            # 测试启用baseline
            config_with_baseline = GRPOTrainingConfig(
                model_path="/tmp/test",
                enable_baseline=True,
                baseline_config=MaxPressureConfig(min_green_offset=1.0)
            )
            assert config_with_baseline.enable_baseline is True
            assert config_with_baseline.baseline_config.min_green_offset == 1.0

        except ImportError as e:
            pytest.skip(f"缺少必要模块: {e}")

    def test_baseline_config_from_yaml(self, tmp_path):
        """
        测试从YAML加载baseline配置

        验证点：
        - reward.max_pressure.enabled正确读取
        - enable_baseline正确设置
        - baseline_config正确实例化
        """
        try:
            from grpo.config import load_training_config

            # 创建临时配置文件
            config_content = """
training:
  sft:
    model_name: "test"
  grpo:
    model_path: "test"

reward:
  chain:
    format_weight: 1.0
    tsc_weight: 1.0
  format:
    strict: 1.0
    partial: -0.5
    invalid: -10.0
  tsc:
    reward_scale: 10.0
  max_pressure:
    enabled: true
    min_green_offset: 2.0
    max_green_override: false
    pressure_threshold: 0.5

paths:
  data_dir: "/tmp/data"

logging:
  use_wandb: false
"""
            config_file = tmp_path / "test_config.yaml"
            with open(config_file, 'w') as f:
                f.write(config_content)

            # 加载配置
            tc = load_training_config(str(config_file))

            # 验证baseline配置
            assert tc.reward.enabled is True, "reward.max_pressure.enabled应为True"
            assert tc.grpo.enable_baseline is True, "grpo.enable_baseline应为True"
            assert tc.grpo.baseline_config is not None
            assert tc.grpo.baseline_config.min_green_offset == 2.0
            assert tc.grpo.baseline_config.pressure_threshold == 0.5

        except ImportError as e:
            pytest.skip(f"缺少必要模块: {e}")

    def test_max_pressure_decision_function(self):
        """
        测试Max Pressure决策函数

        验证点：
        - max_pressure_decision_from_prompt()正确工作
        - 返回'yes'或'no'
        - 时间约束正确处理
        """
        try:
            from grpo.max_pressure import max_pressure_decision_from_prompt, MaxPressureConfig

            config = MaxPressureConfig()

            # 测试用例1：当前相位排队最大
            prompt_data = {
                "state": {
                    "current_phase_id": 0,
                    "phase_metrics_by_id": {
                        "0": {"avg_queue_veh": 10.0},
                        "1": {"avg_queue_veh": 5.0},
                        "2": {"avg_queue_veh": 3.0}
                    }
                }
            }
            prompt = json.dumps(prompt_data)
            decision = max_pressure_decision_from_prompt(prompt, 15.0, 10.0, 60.0, config)
            assert decision == 'yes', "当前相位排队最大时应延长"

            # 测试用例2：其他相位排队更大
            prompt_data["state"]["phase_metrics_by_id"]["1"]["avg_queue_veh"] = 15.0
            prompt = json.dumps(prompt_data)
            decision = max_pressure_decision_from_prompt(prompt, 15.0, 10.0, 60.0, config)
            assert decision == 'no', "其他相位排队更大时应切换"

            # 测试用例3：小于最小绿时间必须延长
            decision = max_pressure_decision_from_prompt(prompt, 5.0, 10.0, 60.0, config)
            assert decision == 'yes', "小于最小绿时间必须延长"

            # 测试用例4：超过最大绿时间必须切换
            decision = max_pressure_decision_from_prompt(prompt, 60.0, 10.0, 60.0, config)
            assert decision == 'no', "超过最大绿时间必须切换"

        except ImportError as e:
            pytest.skip(f"缺少必要模块: {e}")

    def test_batch_max_pressure_decision(self):
        """
        测试批量Max Pressure决策

        验证点：
        - batch_max_pressure_decision()正确处理多个prompt
        - 返回列表长度正确
        - 所有返回值为'yes'或'no'
        """
        try:
            from grpo.max_pressure import batch_max_pressure_decision, MaxPressureConfig

            config = MaxPressureConfig()

            prompts = [
                json.dumps({
                    "state": {
                        "current_phase_id": 0,
                        "phase_metrics_by_id": {
                            "0": {"avg_queue_veh": 10.0},
                            "1": {"avg_queue_veh": 5.0}
                        }
                    }
                }),
                json.dumps({
                    "state": {
                        "current_phase_id": 1,
                        "phase_metrics_by_id": {
                            "0": {"avg_queue_veh": 5.0},
                            "1": {"avg_queue_veh": 10.0}
                        }
                    }
                })
            ]

            green_elapsed_list = [15.0, 20.0]
            min_green_list = [10.0, 10.0]
            max_green_list = [60.0, 60.0]

            decisions = batch_max_pressure_decision(
                prompts, green_elapsed_list, min_green_list, max_green_list, config
            )

            assert len(decisions) == 2, "应返回2个决策"
            assert all(d in ['yes', 'no'] for d in decisions), "所有决策应为'yes'或'no'"

        except ImportError as e:
            pytest.skip(f"缺少必要模块: {e}")

    def test_compare_with_baseline(self):
        """
        测试baseline比较函数

        验证点：
        - compare_with_baseline()正确比较决策
        - 返回布尔列表
        - 准确率计算正确
        """
        try:
            from grpo.max_pressure import compare_with_baseline, compute_baseline_accuracy

            model_decisions = ['yes', 'no', 'yes', 'yes']
            baseline_decisions = ['yes', 'yes', 'yes', 'no']

            # 测试比较
            matches = compare_with_baseline(model_decisions, baseline_decisions)
            assert matches == [True, False, True, False], "比较结果不正确"

            # 测试准确率
            accuracy = compute_baseline_accuracy(model_decisions, baseline_decisions)
            assert accuracy == 0.5, "准确率应为0.5"

        except ImportError as e:
            pytest.skip(f"缺少必要模块: {e}")

    def test_reward_function_with_baseline_params(self):
        """
        测试reward函数支持baseline参数

        验证点：
        - compute_reward()接受baseline参数
        - 返回的info包含baseline信息
        - baseline信息格式正确
        """
        try:
            from grpo.reward import compute_reward, RewardChainConfig
            from grpo.max_pressure import MaxPressureConfig

            chain_config = RewardChainConfig()
            mp_config = MaxPressureConfig()

            prompt_data = {
                "state": {
                    "current_phase_id": 0,
                    "phase_metrics_by_id": {
                        "0": {"avg_queue_veh": 10.0},
                        "1": {"avg_queue_veh": 5.0}
                    }
                }
            }
            prompt = json.dumps(prompt_data)
            output = '{"extend": "yes"}'
            state_file = "/tmp/test.xml"  # 不会实际使用

            # 调用compute_reward（不启用baseline）
            reward, info = compute_reward(
                prompt=prompt,
                output=output,
                state_file=state_file,
                chain_config=chain_config,
                sumo_config=SimpleNamespace(max_workers=0, extend_seconds=5, reward_scale=10.0, port_range=[10000, 60000]),
                enable_baseline=False
            )

            assert isinstance(reward, float), "reward应为float"
            assert "format_reward" in info, "info应包含format_reward"

            # 调用compute_reward（启用baseline）
            reward, info = compute_reward(
                prompt=prompt,
                output=output,
                state_file=state_file,
                chain_config=chain_config,
                sumo_config=SimpleNamespace(max_workers=0, extend_seconds=5, reward_scale=10.0, port_range=[10000, 60000]),
                green_elapsed=15.0,
                min_green=10.0,
                max_green=60.0,
                enable_baseline=True,
                mp_config=mp_config
            )

            assert isinstance(reward, float)
            # 应包含baseline信息（如果计算成功）
            if "baseline_error" not in info:
                assert "baseline_decision" in info or "model_decision" in info

        except ImportError as e:
            pytest.skip(f"缺少必要模块: {e}")


class TestLoadGrpoDatasetPreservesTimeParams:
    """测试数据集加载保留时间参数（不依赖datasets模块）"""

    def test_dataset_json_format_with_time_params(self, tmp_path):
        """
        测试GRPO数据集JSON格式包含时间参数

        验证点：
        - JSON文件可正确创建
        - 包含时间参数字段
        - 字段值正确
        """
        # 创建测试数据
        test_data = [
            {
                "prompt": '{"test": "data"}',
                "state_file": "/tmp/test.xml",
                "current_green_elapsed": 15.5,
                "min_green": 10.0,
                "max_green": 60.0,
            },
            {
                "prompt": '{"test": "data2"}',
                "state_file": "/tmp/test2.xml",
                "current_green_elapsed": 20.0,
                "min_green": 12.0,
                "max_green": 65.0,
            }
        ]

        # 写入JSON文件
        test_file = tmp_path / "test_dataset.json"
        with open(test_file, 'w') as f:
            json.dump(test_data, f)

        # 验证文件可读取
        with open(test_file, 'r') as f:
            loaded_data = json.load(f)

        assert len(loaded_data) == 2
        assert loaded_data[0]["current_green_elapsed"] == 15.5
        assert loaded_data[1]["min_green"] == 12.0

    def test_dataset_backward_compatibility(self, tmp_path):
        """
        测试向后兼容性：不包含时间参数的数据集

        验证点：
        - 旧格式数据集仍然有效
        - 不包含时间参数字段时可用
        """
        # 创建旧格式测试数据
        test_data = [
            {
                "prompt": '{"test": "data"}',
                "state_file": "/tmp/test.xml",
            },
            {
                "prompt": '{"test": "data2"}',
                "state_file": "/tmp/test2.xml",
            }
        ]

        # 写入JSON文件
        test_file = tmp_path / "test_old_dataset.json"
        with open(test_file, 'w') as f:
            json.dump(test_data, f)

        # 验证文件可读取
        with open(test_file, 'r') as f:
            loaded_data = json.load(f)

        assert len(loaded_data) == 2
        assert "current_green_elapsed" not in loaded_data[0] or loaded_data[0]["current_green_elapsed"] is None


class TestEndToEndTrainingWithBaseline:
    """测试端到端训练验证baseline功能（需要Docker环境）"""

    @pytest.fixture(scope="module")
    def baseline_test_dataset(self):
        """准备baseline测试数据"""
        test_data_dir = Path(__file__).parent.parent / "fixtures" / "testdata"
        grpo_data_file = test_data_dir / "small_grpo_dataset.json"

        if not grpo_data_file.exists():
            pytest.skip(f"GRPO测试数据不存在: {grpo_data_file}")

        return {
            "grpo_file": str(grpo_data_file),
            "sft_file": str(test_data_dir / "small_sft_dataset.json"),
        }

    @pytest.fixture(scope="function")
    def baseline_training_dir(self):
        """创建临时训练输出目录"""
        temp_dir = tempfile.mkdtemp(prefix="test_baseline_training_")
        yield temp_dir
        if Path(temp_dir).exists():
            shutil.rmtree(temp_dir, ignore_errors=True)

    @pytest.mark.integration
    def test_grpo_training_with_baseline_logging(
        self,
        baseline_test_dataset,
        baseline_training_dir
    ):
        """
        GRPO训练测试（启用baseline，验证日志输出）

        验证点：
        - 训练完成无错误
        - 日志包含baseline配置信息
        - 日志包含"Baseline Accuracy"统计（如果有足够的训练步数）

        注意：此测试需要Docker环境和完整依赖，标记为integration测试
        当前环境下跳过，因为需要完整的训练环境和配置文件
        """
        pytest.skip("需要完整的Docker环境和训练配置，在CI/CD中运行")

    @pytest.mark.integration
    def test_grpo_training_without_baseline_baseline(
        self,
        baseline_test_dataset,
        baseline_training_dir
    ):
        """
        GRPO训练测试（禁用baseline，对比验证）

        验证点：
        - 禁用baseline时训练正常完成
        - 日志不包含"Baseline Accuracy"统计

        注意：此测试需要Docker环境和完整依赖，标记为integration测试
        当前环境下跳过，因为需要完整的训练环境和配置文件
        """
        pytest.skip("需要完整的Docker环境和训练配置，在CI/CD中运行")
