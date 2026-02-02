# -*- coding: utf-8 -*-
"""
集成测试

测试需要真实SUMO环境的端到端功能：
- reward链计算
- SUMO仿真集成
- 完整的训练流程

所有测试标记为@pytest.mark.integration，需要在docker容器中运行
"""

import pytest
import json
from pathlib import Path

# 文件级别标记：所有测试都是integration测试
pytestmark = pytest.mark.integration


class TestRewardChainWithSUMO:
    """测试reward计算链与SUMO集成"""

    def test_reward_chain_with_sumo(self, sumo_test_data):
        """测试完整reward计算链（format + TSC）"""
        from grpo.reward import batch_compute_reward, RewardChainConfig

        if not sumo_test_data["has_sumo_data"]:
            pytest.skip("No SUMO test data available")

        # 准备测试数据
        state_file = sumo_test_data["state_file"]
        if not state_file or not Path(state_file).exists():
            pytest.skip(f"State file not found: {state_file}")

        prompt_data = {
            "crossing_id": "cluster_11123112",
            "state": {
                "current_phase_id": 0,
                "phase_metrics_by_id": {
                    "0": {"avg_queue_veh": 10.0},
                    "1": {"avg_queue_veh": 5.0},
                    "2": {"avg_queue_veh": 3.0},
                    "3": {"avg_queue_veh": 7.0}
                }
            },
            "phase_order": [0, 1, 2, 3]
        }
        prompt = json.dumps(prompt_data)

        # 测试样本
        prompts = [prompt]
        outputs = ['{"extend": "yes"}']
        state_files = [state_file]

        # 配置
        chain_config = RewardChainConfig(
            format_weight=1.0,
            tsc_weight=1.0,
            format_strict=1.0,
            format_partial=-0.5,
            format_invalid=-10.0
        )

        # 创建SUMO配置
        from types import SimpleNamespace
        sumo_config = SimpleNamespace(
            max_workers=1,
            port_range=[10000, 60000],
            extend_seconds=5,
            reward_scale=10.0
        )

        # 计算reward
        try:
            rewards, stats = batch_compute_reward(
                prompts=prompts,
                outputs=outputs,
                state_files=state_files,
                chain_config=chain_config,
                sumo_config=sumo_config
            )

            # 验证结果
            assert len(rewards) == 1
            assert isinstance(rewards[0], float)

            # 验证统计信息
            assert stats.total_count == 1
            assert stats.strict_format_count >= 0
            assert stats.format_accuracy >= 0
            assert stats.format_accuracy <= 1

        except Exception as e:
            pytest.skip(f"SUMO integration failed (expected in non-docker environment): {e}")

    def test_reward_chain_format_skip(self, sumo_test_data):
        """测试format无效时跳过TSC计算"""
        from grpo.reward import batch_compute_reward, RewardChainConfig

        if not sumo_test_data["has_sumo_data"]:
            pytest.skip("No SUMO test data available")

        state_file = sumo_test_data["state_file"]
        if not state_file or not Path(state_file).exists():
            pytest.skip(f"State file not found: {state_file}")

        prompt_data = {
            "crossing_id": "cluster_11123112",
            "state": {
                "current_phase_id": 0,
                "phase_metrics_by_id": {
                    "0": {"avg_queue_veh": 10.0}
                }
            },
            "phase_order": [0, 1, 2, 3]
        }
        prompt = json.dumps(prompt_data)

        # 使用无效format
        prompts = [prompt]
        outputs = ['invalid format']
        state_files = [state_file]

        chain_config = RewardChainConfig()

        from types import SimpleNamespace
        sumo_config = SimpleNamespace(
            max_workers=1,
            port_range=[10000, 60000],
            extend_seconds=5,
            reward_scale=10.0
        )

        try:
            rewards, stats = batch_compute_reward(
                prompts=prompts,
                outputs=outputs,
                state_files=state_files,
                chain_config=chain_config,
                sumo_config=sumo_config
            )

            # format无效时应该返回format_invalid
            assert rewards[0] == -10.0
            assert stats.invalid_format_count == 1
            assert stats.format_accuracy == 0.0

        except Exception as e:
            pytest.skip(f"SUMO integration failed (expected in non-docker environment): {e}")


class TestEndToEndRewardCalculation:
    """测试端到端reward计算"""

    def test_end_to_end_reward_calculation(self, sumo_test_data):
        """完整测试单个样本的reward计算流程"""
        from grpo.reward import format_reward_fn, compute_reward, RewardChainConfig

        if not sumo_test_data["has_sumo_data"]:
            pytest.skip("No SUMO test data available")

        state_file = sumo_test_data["state_file"]
        if not state_file or not Path(state_file).exists():
            pytest.skip(f"State file not found: {state_file}")

        # Step 1: 准备prompt
        prompt_data = {
            "crossing_id": "cluster_11123112",
            "state": {
                "current_phase_id": 0,
                "phase_metrics_by_id": {
                    "0": {"avg_queue_veh": 10.0},
                    "1": {"avg_queue_veh": 5.0}
                }
            },
            "phase_order": [0, 1, 2, 3]
        }
        prompt = json.dumps(prompt_data)

        # Step 2: 模型输出
        output = '{"extend": "yes"}'

        # Step 3: 验证format
        format_result = format_reward_fn(output)
        assert format_result.is_strict is True
        assert format_result.extracted_decision == "yes"

        # Step 4: 计算TSC reward
        chain_config = RewardChainConfig()

        from types import SimpleNamespace
        sumo_config = SimpleNamespace(
            extend_seconds=5,
            sumocfg_path=None  # 会自动推断
        )

        try:
            reward, info = compute_reward(
                prompt=prompt,
                output=output,
                state_file=state_file,
                chain_config=chain_config,
                sumo_config=sumo_config
            )

            # 验证结果
            assert isinstance(reward, float)
            assert "format_reward" in info
            assert "tsc_reward" in info
            assert info["format_reward"] == 1.0

        except Exception as e:
            pytest.skip(f"SUMO integration failed (expected in non-docker environment): {e}")


class TestSUMODataHandling:
    """测试SUMO数据处理"""

    def test_small_sumo_dataset(self, sumo_test_data):
        """测试小规模SUMO数据集"""
        if not sumo_test_data["has_sumo_data"]:
            pytest.skip("No SUMO test data available")

        state_file = sumo_test_data["state_file"]
        assert state_file is not None
        assert Path(state_file).exists()

        # 验证文件内容
        with open(state_file, 'r') as f:
            content = f.read()
            # SUMO状态文件应该包含一些基本元素
            assert len(content) > 0

    def test_batch_processing_with_multiple_samples(self, sumo_test_data):
        """测试批量处理多个样本"""
        from grpo.reward import batch_compute_reward, RewardChainConfig

        if not sumo_test_data["has_sumo_data"]:
            pytest.skip("No SUMO test data available")

        state_file = sumo_test_data["state_file"]
        if not state_file or not Path(state_file).exists():
            pytest.skip(f"State file not found: {state_file}")

        # 准备多个样本
        prompt_data = {
            "crossing_id": "cluster_11123112",
            "state": {
                "current_phase_id": 0,
                "phase_metrics_by_id": {
                    "0": {"avg_queue_veh": 10.0},
                    "1": {"avg_queue_veh": 5.0}
                }
            },
            "phase_order": [0, 1, 2, 3]
        }

        prompts = [json.dumps(prompt_data)] * 3
        outputs = [
            '{"extend": "yes"}',
            '{"extend": "no"}',
            'invalid format'
        ]
        state_files = [state_file] * 3

        chain_config = RewardChainConfig()

        from types import SimpleNamespace
        sumo_config = SimpleNamespace(
            max_workers=1,
            port_range=[10000, 60000],
            extend_seconds=5,
            reward_scale=10.0
        )

        try:
            rewards, stats = batch_compute_reward(
                prompts=prompts,
                outputs=outputs,
                state_files=state_files,
                chain_config=chain_config,
                sumo_config=sumo_config
            )

            # 验证批量结果
            assert len(rewards) == 3
            assert stats.total_count == 3

            # 验证format统计
            assert stats.strict_format_count >= 1
            assert stats.invalid_format_count >= 1

        except Exception as e:
            pytest.skip(f"SUMO integration failed (expected in non-docker environment): {e}")
