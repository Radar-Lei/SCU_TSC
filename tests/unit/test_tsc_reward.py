# -*- coding: utf-8 -*-
"""
TSC reward函数单元测试

测试sumo_reward模块的函数：
- normalize_reward归一化函数
- calculate_tsc_reward_single单样本计算（使用mock）
- 批量reward计算（标记为integration，需要真实SUMO）
- prompt解析函数
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import math
from grpo.sumo_reward import (
    normalize_reward,
    calculate_tsc_reward_single,
    extract_decision_from_output,
    parse_prompt_for_decision_info,
    TSCResult,
)


class TestNormalizeReward:
    """测试归一化函数"""

    @pytest.mark.parametrize("delta,scale,expected_range", [
        (10, 10.0, (-1, 0)),      # 正delta -> 负reward
        (-10, 10.0, (0, 1)),     # 负delta -> 正reward
        (0, 10.0, 0),            # 零delta -> 零reward
        (100, 10.0, -1),         # 极大正delta -> -1
        (-100, 10.0, 1),         # 极大负delta -> 1
    ])
    def test_normalize_reward_returns_correct_range(self, delta, scale, expected_range):
        """测试归一化返回值在正确范围内"""
        result = normalize_reward(delta, scale)

        if isinstance(expected_range, tuple):
            assert expected_range[0] <= result <= expected_range[1]
        else:
            # 使用近似比较处理浮点精度
            assert result == pytest.approx(expected_range, abs=0.0001)

    def test_normalize_positive_delta(self):
        """正delta（排队增加）返回负reward"""
        result = normalize_reward(10, scale=10.0)
        assert result < 0
        # tanh(-1) ≈ -0.76
        assert -1 < result < 0

    def test_normalize_negative_delta(self):
        """负delta（排队减少）返回正reward"""
        result = normalize_reward(-10, scale=10.0)
        assert result > 0
        # tanh(1) ≈ 0.76
        assert 0 < result < 1

    def test_normalize_zero_delta(self):
        """零delta返回零reward"""
        result = normalize_reward(0, scale=10.0)
        assert result == 0.0

    @pytest.mark.parametrize("scale", [1.0, 5.0, 10.0, 20.0, 100.0])
    def test_normalize_with_different_scales(self, scale):
        """测试不同scale参数"""
        delta = 10
        result = normalize_reward(delta, scale)

        # scale越大，归一化后的值越接近0
        expected = math.tanh(-delta / scale)
        assert abs(result - expected) < 0.0001

    def test_normalize_extreme_values(self):
        """测试极值"""
        # 极大正delta
        result = normalize_reward(1000, scale=10.0)
        assert result == pytest.approx(-1.0, abs=0.0001)

        # 极大负delta
        result = normalize_reward(-1000, scale=10.0)
        assert result == pytest.approx(1.0, abs=0.0001)

        # 非常小的scale
        result = normalize_reward(100, scale=0.1)
        assert result == pytest.approx(-1.0, abs=0.0001)


class TestExtractDecisionFromOutput:
    """测试从输出提取决策"""

    @pytest.mark.parametrize("output,expected", [
        ('{"extend": "yes"}', "yes"),
        ('{"extend": "no"}', "no"),
        ('Some text {"extend": "yes"} more', "yes"),
        ('{"extend":"yes"}', "yes"),
        ('{"Extend": "yes"}', "yes"),  # 不区分大小写
    ])
    def test_extract_decision_success(self, output, expected):
        """成功提取决策"""
        result = extract_decision_from_output(output)
        assert result == expected

    @pytest.mark.parametrize("output", [
        "no decision here",
        '{"wrong_key": "yes"}',
        "",
        "just random text",
        '{"extend": "invalid"}',
    ])
    def test_extract_decision_failure(self, output):
        """无法提取决策返回None"""
        result = extract_decision_from_output(output)
        assert result is None


class TestParsePromptForDecisionInfo:
    """测试从prompt解析决策信息"""

    def test_parse_valid_prompt(self):
        """解析有效prompt"""
        prompt = '''
        {
            "crossing_id": "cluster_11123112",
            "state": {
                "current_phase_id": 0,
                "phase_metrics_by_id": {
                    "0": {"avg_queue_veh": 10.0}
                }
            },
            "phase_order": [0, 1, 2, 3]
        }
        '''

        info = parse_prompt_for_decision_info(prompt)

        assert info["tl_id_hash"] == "cluster_11123112"
        assert info["current_phase_id"] == 0
        assert info["phase_order"] == [0, 1, 2, 3]

    def test_parse_missing_crossing_id(self):
        """缺少crossing_id时返回None"""
        prompt = '''
        {
            "state": {
                "current_phase_id": 0
            },
            "phase_order": [0, 1, 2, 3]
        }
        '''

        info = parse_prompt_for_decision_info(prompt)

        assert info["tl_id_hash"] is None
        assert info["current_phase_id"] == 0

    def test_parse_invalid_json(self):
        """无效JSON应抛出异常"""
        prompt = "not a json"

        with pytest.raises(Exception):  # JSONDecodeError
            parse_prompt_for_decision_info(prompt)


class TestCalculateTSCRewardSingle:
    """测试单样本TSC reward计算（使用mock）"""

    @patch('grpo.sumo_reward.SUMOInterface')
    def test_calculate_success(self, mock_sumo_class):
        """测试成功计算reward"""
        # 配置mock
        mock_sumo = Mock()
        mock_sumo_class.return_value = mock_sumo

        mock_sumo.start_from_state.return_value = True
        mock_sumo.get_traffic_lights.return_value = ["tl_0"]
        mock_sumo.get_total_queue_count.side_effect = [10, 8]  # before, after

        prompt = '''
        {
            "crossing_id": "cluster_11123112",
            "state": {
                "current_phase_id": 0,
                "phase_metrics_by_id": {"0": {"avg_queue_veh": 10.0}}
            },
            "phase_order": [0, 1, 2, 3]
        }
        '''

        config = Mock()
        config.extend_seconds = 5
        config.sumocfg_path = "/path/to/config.sumocfg"

        result = calculate_tsc_reward_single(
            state_file="/path/to/state.xml",
            prompt=prompt,
            decision="yes",
            config=config
        )

        assert result.success is True
        assert result.queue_before == 10
        assert result.queue_after == 8
        assert result.delta == -2
        # delta=-2, scale=10 -> tanh(0.2) ≈ 0.197
        assert result.reward > 0

    @patch('grpo.sumo_reward.SUMOInterface')
    def test_calculate_sumo_start_failure(self, mock_sumo_class):
        """测试SUMO启动失败"""
        mock_sumo = Mock()
        mock_sumo_class.return_value = mock_sumo
        mock_sumo.start_from_state.return_value = False

        prompt = '{"state": {"current_phase_id": 0}, "phase_order": [0]}'

        config = Mock()
        config.extend_seconds = 5
        config.sumocfg_path = "/path/to/config.sumocfg"

        result = calculate_tsc_reward_single(
            state_file="/path/to/state.xml",
            prompt=prompt,
            decision="yes",
            config=config
        )

        assert result.success is False
        assert "Failed to start SUMO" in result.error
        assert result.reward == 0.0

    @patch('grpo.sumo_reward.SUMOInterface')
    def test_calculate_no_traffic_light(self, mock_sumo_class):
        """测试没有找到交通灯"""
        mock_sumo = Mock()
        mock_sumo_class.return_value = mock_sumo
        mock_sumo.start_from_state.return_value = True
        mock_sumo.get_traffic_lights.return_value = []

        prompt = '{"state": {"current_phase_id": 0}, "phase_order": [0]}'

        config = Mock()
        config.extend_seconds = 5
        config.sumocfg_path = "/path/to/config.sumocfg"

        result = calculate_tsc_reward_single(
            state_file="/path/to/state.xml",
            prompt=prompt,
            decision="yes",
            config=config
        )

        assert result.success is False
        assert "No traffic lights" in result.error
        assert result.reward == 0.0

    @patch('grpo.sumo_reward.SUMOInterface')
    def test_calculate_with_no_decision(self, mock_sumo_class):
        """测试无法提取决策"""
        prompt = '{"state": {"current_phase_id": 0}, "phase_order": [0]}'
        decision = None  # 无法提取决策

        config = Mock()
        config.extend_seconds = 5

        result = calculate_tsc_reward_single(
            state_file="/path/to/state.xml",
            prompt=prompt,
            decision=decision,
            config=config
        )

        # 应该在调用前就失败，不会创建SUMO
        assert result.success is False
        assert result.reward == 0.0

    @patch('grpo.sumo_reward.SUMOInterface')
    def test_calculate_switch_phase(self, mock_sumo_class):
        """测试切换相位决策"""
        mock_sumo = Mock()
        mock_sumo_class.return_value = mock_sumo

        mock_sumo.start_from_state.return_value = True
        mock_sumo.get_traffic_lights.return_value = ["tl_0"]
        mock_sumo.get_total_queue_count.side_effect = [10, 12]  # before, after
        mock_sumo.set_phase.return_value = None

        prompt = '''
        {
            "state": {
                "current_phase_id": 0,
                "phase_metrics_by_id": {"0": {"avg_queue_veh": 10.0}}
            },
            "phase_order": [0, 1, 2, 3]
        }
        '''

        config = Mock()
        config.extend_seconds = 5
        config.sumocfg_path = "/path/to/config.sumocfg"

        result = calculate_tsc_reward_single(
            state_file="/path/to/state.xml",
            prompt=prompt,
            decision="no",  # 切换相位
            config=config
        )

        assert result.success is True
        mock_sumo.set_phase.assert_called_once()
        assert result.delta == 2
        # delta=+2 -> 负reward
        assert result.reward < 0


class TestIntegrationWithRealSUMO:
    """集成测试（需要真实SUMO环境）"""

    @pytest.mark.integration
    def test_batch_compute_reward_with_real_sumo(self, sumo_test_data):
        """测试真实SUMO环境的批量reward计算"""
        if not sumo_test_data["has_sumo_data"]:
            pytest.skip("No SUMO test data available")

        # 这个测试需要真实的SUMO环境和状态文件
        # 在docker容器中运行
        pass

    @pytest.mark.integration
    def test_end_to_end_reward_calculation(self, sumo_test_data):
        """端到端reward计算测试"""
        if not sumo_test_data["has_sumo_data"]:
            pytest.skip("No SUMO test data available")

        # 完整测试流程：prompt -> format -> SUMO -> reward
        pass


class TestTSCRewardEdgeCases:
    """测试边界情况"""

    @patch('grpo.sumo_reward.SUMOInterface')
    def test_queue_delta_zero(self, mock_sumo_class):
        """排队数不变"""
        mock_sumo = Mock()
        mock_sumo_class.return_value = mock_sumo

        mock_sumo.start_from_state.return_value = True
        mock_sumo.get_traffic_lights.return_value = ["tl_0"]
        mock_sumo.get_total_queue_count.side_effect = [10, 10]  # 不变

        prompt = '{"state": {"current_phase_id": 0}, "phase_order": [0]}'

        config = Mock()
        config.extend_seconds = 5
        config.sumocfg_path = "/path/to/config.sumocfg"

        result = calculate_tsc_reward_single(
            state_file="/path/to/state.xml",
            prompt=prompt,
            decision="yes",
            config=config
        )

        assert result.delta == 0
        assert result.reward == 0.0

    @patch('grpo.sumo_reward.SUMOInterface')
    def test_exception_handling(self, mock_sumo_class):
        """测试异常处理"""
        mock_sumo = Mock()
        mock_sumo_class.return_value = mock_sumo
        mock_sumo.start_from_state.side_effect = Exception("SUMO crashed")

        prompt = '{"state": {"current_phase_id": 0}, "phase_order": [0]}'

        config = Mock()
        config.extend_seconds = 5
        config.sumocfg_path = "/path/to/config.sumocfg"

        result = calculate_tsc_reward_single(
            state_file="/path/to/state.xml",
            prompt=prompt,
            decision="yes",
            config=config
        )

        assert result.success is False
        assert "SUMO crashed" in result.error
        assert result.reward == 0.0
