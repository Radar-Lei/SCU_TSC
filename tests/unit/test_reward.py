# -*- coding: utf-8 -*-
"""
Reward函数单元测试

测试compute_reward()和batch_compute_reward()函数，包括：
- format reward计算
- TSC reward计算（使用mock）
- Max Pressure baseline比较
- 批量reward计算
- 统计信息
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import json
from grpo.reward import (
    compute_reward,
    batch_compute_reward,
    format_reward_fn,
    extract_decision,
    FormatResult,
    RewardStats,
    RewardChainConfig,
)


# ============== Fixtures ==============

@pytest.fixture
def sample_prompt():
    """标准样本prompt JSON字符串"""
    data = {
        "crossing_id": "cluster_11123112",
        "state": {
            "current_phase_id": 0,
            "phase_metrics_by_id": {
                "0": {"avg_queue_veh": 10.0},
                "1": {"avg_queue_veh": 5.0},
                "2": {"avg_queue_veh": 3.0},
            }
        },
        "phase_order": [0, 1, 2, 3]
    }
    return json.dumps(data)


@pytest.fixture
def chain_config():
    """Reward函数链配置"""
    return RewardChainConfig(
        format_weight=1.0,
        tsc_weight=1.0,
        format_strict=1.0,
        format_partial=-0.5,
        format_invalid=-10.0,
        extract_regex=r'\{["\s]*extend["\s]*:\s*["\s]*(yes|no)["\s]*\}'
    )


@pytest.fixture
def sumo_config():
    """SUMO配置mock"""
    config = Mock()
    config.extend_seconds = 5
    config.sumocfg_path = "/path/to/config.sumocfg"
    config.max_workers = 4
    return config


@pytest.fixture
def mock_tsc_reward_fn():
    """Mock TSC reward函数"""
    def mock_fn(state_file, prompt, decision, config):
        from grpo.sumo_reward import TSCResult
        return TSCResult(
            success=True,
            queue_before=10,
            queue_after=8,
            delta=-2,
            reward=0.5  # 简化的reward值
        )
    return mock_fn


# ============== compute_reward() baseline测试 ==============

class TestComputeRewardWithBaseline:
    """测试compute_reward()的Max Pressure baseline比较功能"""

    @patch('grpo.max_pressure.max_pressure_decision_from_prompt')
    def test_compute_reward_with_baseline_enabled(self, mock_baseline_fn, sample_prompt, chain_config, sumo_config, mock_tsc_reward_fn):
        """测试启用baseline时的reward计算"""
        # Mock Max Pressure决策返回'yes'
        mock_baseline_fn.return_value = 'yes'

        output = '{"extend": "yes"}'
        state_file = "/path/to/state.xml"

        reward, info = compute_reward(
            prompt=sample_prompt,
            output=output,
            state_file=state_file,
            chain_config=chain_config,
            sumo_config=sumo_config,
            tsc_reward_fn=mock_tsc_reward_fn,
            green_elapsed=15.0,
            min_green=10.0,
            max_green=60.0,
            enable_baseline=True,
            mp_config=None
        )

        # 验证reward值
        assert isinstance(reward, float)

        # 验证info包含baseline字段
        assert "baseline_decision" in info
        assert "model_decision" in info
        assert "matches_baseline" in info

        # 验证baseline决策
        assert info["baseline_decision"] == 'yes'
        assert info["model_decision"] == 'yes'  # 从output提取
        assert info["matches_baseline"] is True  # 决策匹配

        # 验证其他字段
        assert info["format_reward"] == 1.0  # 严格格式
        assert info["tsc_reward"] == 0.5

    @patch('grpo.max_pressure.max_pressure_decision_from_prompt')
    def test_compute_reward_baseline_decision_differs(self, mock_baseline_fn, sample_prompt, chain_config, sumo_config, mock_tsc_reward_fn):
        """测试baseline决策与模型决策不同的情况"""
        # Mock Max Pressure决策返回'no'（与模型不同）
        mock_baseline_fn.return_value = 'no'

        output = '{"extend": "yes"}'
        state_file = "/path/to/state.xml"

        reward, info = compute_reward(
            prompt=sample_prompt,
            output=output,
            state_file=state_file,
            chain_config=chain_config,
            sumo_config=sumo_config,
            tsc_reward_fn=mock_tsc_reward_fn,
            green_elapsed=15.0,
            min_green=10.0,
            max_green=60.0,
            enable_baseline=True,
            mp_config=None
        )

        # 验证baseline比较
        assert info["baseline_decision"] == 'no'
        assert info["model_decision"] == 'yes'
        assert info["matches_baseline"] is False

    def test_compute_reward_baseline_disabled(self, sample_prompt, chain_config, sumo_config, mock_tsc_reward_fn):
        """测试禁用baseline时不包含baseline字段"""
        output = '{"extend": "yes"}'
        state_file = "/path/to/state.xml"

        reward, info = compute_reward(
            prompt=sample_prompt,
            output=output,
            state_file=state_file,
            chain_config=chain_config,
            sumo_config=sumo_config,
            tsc_reward_fn=mock_tsc_reward_fn,
            green_elapsed=15.0,
            min_green=10.0,
            max_green=60.0,
            enable_baseline=False,  # 禁用baseline
            mp_config=None
        )

        # 验证不包含baseline字段
        assert "baseline_decision" not in info
        assert "model_decision" not in info
        assert "matches_baseline" not in info

        # 验证其他字段正常
        assert "format_reward" in info
        assert "tsc_reward" in info

    def test_compute_reward_baseline_missing_time_params(self, sample_prompt, chain_config, sumo_config, mock_tsc_reward_fn):
        """测试缺少时间参数时不进行baseline计算"""
        output = '{"extend": "yes"}'
        state_file = "/path/to/state.xml"

        # 不提供时间参数
        reward, info = compute_reward(
            prompt=sample_prompt,
            output=output,
            state_file=state_file,
            chain_config=chain_config,
            sumo_config=sumo_config,
            tsc_reward_fn=mock_tsc_reward_fn,
            green_elapsed=None,  # 缺少时间参数
            min_green=10.0,
            max_green=60.0,
            enable_baseline=True,
            mp_config=None
        )

        # 验证不包含baseline字段（因为缺少时间参数）
        assert "baseline_decision" not in info
        assert "model_decision" not in info

    @patch('grpo.max_pressure.max_pressure_decision_from_prompt')
    def test_compute_reward_baseline_error_handling(self, mock_baseline_fn, sample_prompt, chain_config, sumo_config, mock_tsc_reward_fn):
        """测试baseline计算失败时的错误处理"""
        # Mock抛出异常
        mock_baseline_fn.side_effect = ValueError("Invalid prompt JSON")

        output = '{"extend": "yes"}'
        state_file = "/path/to/state.xml"

        reward, info = compute_reward(
            prompt=sample_prompt,
            output=output,
            state_file=state_file,
            chain_config=chain_config,
            sumo_config=sumo_config,
            tsc_reward_fn=mock_tsc_reward_fn,
            green_elapsed=15.0,
            min_green=10.0,
            max_green=60.0,
            enable_baseline=True,
            mp_config=None
        )

        # 验证包含错误信息
        assert "baseline_error" in info
        assert "Invalid prompt JSON" in info["baseline_error"]

        # 验证其他字段正常
        assert "format_reward" in info
        assert "tsc_reward" in info

    @patch('grpo.max_pressure.max_pressure_decision_from_prompt')
    def test_compute_reward_baseline_with_invalid_output(self, mock_baseline_fn, sample_prompt, chain_config, sumo_config, mock_tsc_reward_fn):
        """测试output无效时baseline仍能计算但matches_baseline为None"""
        mock_baseline_fn.return_value = 'yes'

        # 无效output（无法提取决策）
        output = "invalid output"
        state_file = "/path/to/state.xml"

        reward, info = compute_reward(
            prompt=sample_prompt,
            output=output,
            state_file=state_file,
            chain_config=chain_config,
            sumo_config=sumo_config,
            tsc_reward_fn=mock_tsc_reward_fn,
            green_elapsed=15.0,
            min_green=10.0,
            max_green=60.0,
            enable_baseline=True,
            mp_config=None
        )

        # 由于format无效，应该early return，不计算baseline
        assert reward == -10.0  # format_invalid reward
        assert info["reason"] == "invalid_format"


# ============== batch_compute_reward() baseline测试 ==============

class TestBatchComputeRewardWithBaseline:
    """测试batch_compute_reward()的Max Pressure baseline功能"""

    @patch('grpo.max_pressure.batch_max_pressure_decision')
    @patch('grpo.sumo_reward.ParallelSUMORewardCalculator')
    def test_batch_compute_reward_with_baseline_enabled(self, mock_calculator_class, mock_batch_baseline_fn, sample_prompt, chain_config, sumo_config):
        """测试启用baseline时的批量reward计算"""
        # Mock baseline决策
        mock_batch_baseline_fn.return_value = ['yes', 'no', 'yes']

        # Mock SUMO计算器
        mock_calculator = Mock()
        mock_calculator.calculate_batch.return_value = [0.5, 0.3, 0.7]
        mock_calculator_class.return_value = mock_calculator

        prompts = [sample_prompt, sample_prompt, sample_prompt]
        outputs = ['{"extend": "yes"}', '{"extend": "no"}', '{"extend": "yes"}']
        state_files = ["/path/to/state1.xml", "/path/to/state2.xml", "/path/to/state3.xml"]
        green_elapsed_list = [15.0, 20.0, 25.0]
        min_green_list = [10.0, 10.0, 10.0]
        max_green_list = [60.0, 60.0, 60.0]

        rewards, stats = batch_compute_reward(
            prompts=prompts,
            outputs=outputs,
            state_files=state_files,
            chain_config=chain_config,
            sumo_config=sumo_config,
            green_elapsed_list=green_elapsed_list,
            min_green_list=min_green_list,
            max_green_list=max_green_list,
            enable_baseline=True,
            mp_config=None
        )

        # 验证返回值
        assert isinstance(rewards, list)
        assert len(rewards) == 3
        assert isinstance(stats, RewardStats)

        # 验证统计信息
        assert stats.total_count == 3
        assert stats.strict_format_count == 3

        # 验证batch_max_pressure_decision被调用
        mock_batch_baseline_fn.assert_called_once()

    @patch('grpo.max_pressure.batch_max_pressure_decision')
    @patch('grpo.sumo_reward.ParallelSUMORewardCalculator')
    def test_batch_compute_reward_baseline_time_params_truncation(self, mock_calculator_class, mock_batch_baseline_fn, sample_prompt, chain_config, sumo_config):
        """测试时间参数长度与outputs长度不一致时的截断"""
        mock_batch_baseline_fn.return_value = ['yes', 'no']

        mock_calculator = Mock()
        mock_calculator.calculate_batch.return_value = [0.5, 0.3]
        mock_calculator_class.return_value = mock_calculator

        prompts = [sample_prompt, sample_prompt]
        outputs = ['{"extend": "yes"}', '{"extend": "no"}']
        state_files = ["/path/to/state1.xml", "/path/to/state2.xml"]

        # 时间参数长度为3（超过outputs长度2）
        green_elapsed_list = [15.0, 20.0, 25.0]
        min_green_list = [10.0, 10.0, 10.0]
        max_green_list = [60.0, 60.0, 60.0]

        rewards, stats = batch_compute_reward(
            prompts=prompts,
            outputs=outputs,
            state_files=state_files,
            chain_config=chain_config,
            sumo_config=sumo_config,
            green_elapsed_list=green_elapsed_list,
            min_green_list=min_green_list,
            max_green_list=max_green_list,
            enable_baseline=True,
            mp_config=None
        )

        # 验证结果正确
        assert len(rewards) == 2
        assert stats.total_count == 2

        # 验证调用时使用了截断的长度
        call_args = mock_batch_baseline_fn.call_args
        assert len(call_args[1]['prompts']) == 2
        assert len(call_args[1]['green_elapsed_list']) == 2

    @patch('grpo.max_pressure.batch_max_pressure_decision')
    @patch('grpo.sumo_reward.ParallelSUMORewardCalculator')
    def test_batch_compute_reward_baseline_disabled(self, mock_calculator_class, mock_batch_baseline_fn, sample_prompt, chain_config, sumo_config):
        """测试禁用baseline时不调用batch_max_pressure_decision"""
        mock_calculator = Mock()
        mock_calculator.calculate_batch.return_value = [0.5, 0.3]
        mock_calculator_class.return_value = mock_calculator

        prompts = [sample_prompt, sample_prompt]
        outputs = ['{"extend": "yes"}', '{"extend": "no"}']
        state_files = ["/path/to/state1.xml", "/path/to/state2.xml"]

        rewards, stats = batch_compute_reward(
            prompts=prompts,
            outputs=outputs,
            state_files=state_files,
            chain_config=chain_config,
            sumo_config=sumo_config,
            enable_baseline=False,  # 禁用baseline
            mp_config=None
        )

        # 验证不调用baseline函数
        mock_batch_baseline_fn.assert_not_called()

        # 验证返回值正常
        assert len(rewards) == 2
        assert stats.total_count == 2


# ============== baseline比较和统计函数测试 ==============

class TestBaselineComparisonAndStats:
    """测试baseline比较和统计相关功能"""

    def test_extract_decision_yes_no(self):
        """测试extract_decision提取yes/no"""
        text = '{"extend": "yes"}'
        result = extract_decision(text, r'\{["\s]*extend["\s]*:\s*["\s]*(yes|no)["\s]*\}')
        assert result == 'yes'

        text = '{"extend": "no"}'
        result = extract_decision(text, r'\{["\s]*extend["\s]*:\s*["\s]*(yes|no)["\s]*\}')
        assert result == 'no'

    def test_extract_decision_returns_none_for_invalid(self):
        """测试extract_decision对无效输入返回None"""
        text = "invalid text"
        result = extract_decision(text, r'\{["\s]*extend["\s]*:\s*["\s]*(yes|no)["\s]*\}')
        assert result is None

    @patch('grpo.max_pressure.max_pressure_decision_from_prompt')
    def test_baseline_info_dict_structure(self, mock_baseline_fn, sample_prompt, chain_config, sumo_config, mock_tsc_reward_fn):
        """验证baseline_info字典结构和字段类型"""
        mock_baseline_fn.return_value = 'yes'

        output = '{"extend": "yes"}'
        state_file = "/path/to/state.xml"

        reward, info = compute_reward(
            prompt=sample_prompt,
            output=output,
            state_file=state_file,
            chain_config=chain_config,
            sumo_config=sumo_config,
            tsc_reward_fn=mock_tsc_reward_fn,
            green_elapsed=15.0,
            min_green=10.0,
            max_green=60.0,
            enable_baseline=True,
            mp_config=None
        )

        # 验证baseline字段存在
        assert "baseline_decision" in info
        assert "model_decision" in info
        assert "matches_baseline" in info

        # 验证字段类型
        assert isinstance(info["baseline_decision"], str)
        assert info["baseline_decision"] in ['yes', 'no']

        assert isinstance(info["model_decision"], str)
        assert info["model_decision"] in ['yes', 'no']

        assert isinstance(info["matches_baseline"], bool)

    @patch('grpo.max_pressure.max_pressure_decision_from_prompt')
    @patch('grpo.max_pressure.batch_max_pressure_decision')
    @patch('grpo.sumo_reward.ParallelSUMORewardCalculator')
    def test_end_to_end_baseline_flow(self, mock_calculator_class, mock_batch_baseline_fn, sample_prompt, chain_config, sumo_config):
        """端到端测试：从prompt解析到baseline决策的完整流程"""
        # Mock baseline决策
        mock_batch_baseline_fn.return_value = ['yes', 'yes', 'no', 'no']

        # Mock SUMO计算器
        mock_calculator = Mock()
        mock_calculator.calculate_batch.return_value = [0.5, 0.3, 0.7, 0.4]
        mock_calculator_class.return_value = mock_calculator

        prompts = [sample_prompt] * 4
        outputs = [
            '{"extend": "yes"}',  # 匹配baseline
            '{"extend": "no"}',   # 不匹配baseline
            '{"extend": "no"}',   # 匹配baseline
            '{"extend": "yes"}'   # 不匹配baseline
        ]
        state_files = [f"/path/to/state{i}.xml" for i in range(4)]
        green_elapsed_list = [15.0, 20.0, 25.0, 30.0]
        min_green_list = [10.0] * 4
        max_green_list = [60.0] * 4

        rewards, stats = batch_compute_reward(
            prompts=prompts,
            outputs=outputs,
            state_files=state_files,
            chain_config=chain_config,
            sumo_config=sumo_config,
            green_elapsed_list=green_elapsed_list,
            min_green_list=min_green_list,
            max_green_list=max_green_list,
            enable_baseline=True,
            mp_config=None
        )

        # 验证batch计算成功
        assert len(rewards) == 4
        assert stats.total_count == 4

        # 验证batch_max_pressure_decision被调用
        mock_batch_baseline_fn.assert_called_once()

        # 捕获并验证打印的baseline统计信息
        # 注意：实际测试中需要使用capsys或capfd捕获stdout


# ============== 边界情况测试 ==============

class TestBaselineEdgeCases:
    """测试baseline功能的边界情况"""

    @patch('grpo.max_pressure.max_pressure_decision_from_prompt')
    def test_baseline_with_partial_format(self, mock_baseline_fn, sample_prompt, chain_config, sumo_config, mock_tsc_reward_fn):
        """测试部分格式（partial）时baseline仍能计算"""
        mock_baseline_fn.return_value = 'yes'

        # 部分格式（带额外文本）
        output = 'Some text {"extend": "yes"} more'
        state_file = "/path/to/state.xml"

        reward, info = compute_reward(
            prompt=sample_prompt,
            output=output,
            state_file=state_file,
            chain_config=chain_config,
            sumo_config=sumo_config,
            tsc_reward_fn=mock_tsc_reward_fn,
            green_elapsed=15.0,
            min_green=10.0,
            max_green=60.0,
            enable_baseline=True,
            mp_config=None
        )

        # 验证baseline信息正常
        assert info["baseline_decision"] == 'yes'
        assert info["model_decision"] == 'yes'
        assert info["matches_baseline"] is True
        assert info["is_partial"] is True
        assert info["is_strict"] is False

    def test_baseline_with_none_time_params(self, sample_prompt, chain_config, sumo_config, mock_tsc_reward_fn):
        """测试时间参数全部为None时不进行baseline计算"""
        output = '{"extend": "yes"}'
        state_file = "/path/to/state.xml"

        reward, info = compute_reward(
            prompt=sample_prompt,
            output=output,
            state_file=state_file,
            chain_config=chain_config,
            sumo_config=sumo_config,
            tsc_reward_fn=mock_tsc_reward_fn,
            green_elapsed=None,
            min_green=None,
            max_green=None,
            enable_baseline=True,
            mp_config=None
        )

        # 验证不包含baseline字段
        assert "baseline_decision" not in info
        assert "model_decision" not in info

    @patch('grpo.max_pressure.batch_max_pressure_decision')
    @patch('grpo.sumo_reward.ParallelSUMORewardCalculator')
    def test_batch_baseline_with_mixed_format_validity(self, mock_calculator_class, mock_batch_baseline_fn, sample_prompt, chain_config, sumo_config):
        """测试batch中包含混合格式有效性时的baseline计算"""
        mock_batch_baseline_fn.return_value = ['yes', 'yes', 'yes']

        mock_calculator = Mock()
        mock_calculator.calculate_batch.return_value = [0.5, 0.3, 0.7]
        mock_calculator_class.return_value = mock_calculator

        prompts = [sample_prompt] * 3
        outputs = [
            '{"extend": "yes"}',  # strict
            'text {"extend": "yes"}',  # partial
            'invalid'  # invalid（不会计算TSC）
        ]
        state_files = [f"/path/to/state{i}.xml" for i in range(3)]
        green_elapsed_list = [15.0, 20.0, 25.0]
        min_green_list = [10.0] * 3
        max_green_list = [60.0] * 3

        rewards, stats = batch_compute_reward(
            prompts=prompts,
            outputs=outputs,
            state_files=state_files,
            chain_config=chain_config,
            sumo_config=sumo_config,
            green_elapsed_list=green_elapsed_list,
            min_green_list=min_green_list,
            max_green_list=max_green_list,
            enable_baseline=True,
            mp_config=None
        )

        # 验证统计
        assert stats.total_count == 3
        assert stats.strict_format_count == 1
        assert stats.partial_format_count == 1
        assert stats.invalid_format_count == 1

        # 验证baseline函数仍被调用
        mock_batch_baseline_fn.assert_called_once()
