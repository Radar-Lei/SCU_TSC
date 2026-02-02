# -*- coding: utf-8 -*-
"""
Max Pressure算法单元测试

测试max_pressure_decision和相关函数的所有逻辑：
- 时间约束（最小绿、最大绿时间）
- 压力比较决策
- 边界情况（空队列、负排队数、单相位等）
- prompt解析
- 批量决策
"""

import pytest
import json
from grpo.max_pressure import (
    max_pressure_decision,
    max_pressure_decision_from_prompt,
    batch_max_pressure_decision,
    compute_phase_pressure,
    MaxPressureConfig,
)


class TestMaxPressureTimeConstraints:
    """测试时间约束逻辑"""

    def test_below_min_green_must_extend(self):
        """小于最小绿灯时间必须延长"""
        config = MaxPressureConfig()
        queues = {0: 5.0, 1: 10.0, 2: 3.0}

        # green_elapsed < min_green，即使其他相位排队更大，也必须延长
        decision = max_pressure_decision(
            current_phase_id=0,
            phase_queues=queues,
            green_elapsed=5.0,
            min_green=10.0,
            max_green=60.0,
            config=config
        )

        assert decision == 'yes'

    def test_above_max_green_must_switch(self):
        """超过最大绿灯时间必须切换"""
        config = MaxPressureConfig()
        queues = {0: 100.0, 1: 1.0, 2: 1.0}

        # green_elapsed >= max_green，即使当前相位排队最大，也必须切换
        decision = max_pressure_decision(
            current_phase_id=0,
            phase_queues=queues,
            green_elapsed=60.0,
            min_green=10.0,
            max_green=60.0,
            config=config
        )

        assert decision == 'no'

    def test_at_boundary_min_green(self):
        """测试最小绿时间边界"""
        config = MaxPressureConfig()
        queues = {0: 5.0, 1: 10.0, 2: 3.0}

        # green_elapsed == min_green，可以进行压力比较
        decision = max_pressure_decision(
            current_phase_id=0,
            phase_queues=queues,
            green_elapsed=10.0,
            min_green=10.0,
            max_green=60.0,
            config=config
        )

        # 当前相位排队不是最大，应切换
        assert decision == 'no'

    def test_at_boundary_max_green(self):
        """测试最大绿时间边界"""
        config = MaxPressureConfig()
        queues = {0: 100.0, 1: 1.0, 2: 1.0}

        # green_elapsed == max_green，必须切换
        decision = max_pressure_decision(
            current_phase_id=0,
            phase_queues=queues,
            green_elapsed=60.0,
            min_green=10.0,
            max_green=60.0,
            config=config
        )

        assert decision == 'no'

    def test_min_green_offset(self):
        """测试最小绿时间偏移"""
        config = MaxPressureConfig(min_green_offset=2.0)
        queues = {0: 5.0, 1: 10.0, 2: 3.0}

        # effective_min_green = 10 + 2 = 12
        # green_elapsed = 11 < 12，必须延长
        decision = max_pressure_decision(
            current_phase_id=0,
            phase_queues=queues,
            green_elapsed=11.0,
            min_green=10.0,
            max_green=60.0,
            config=config
        )

        assert decision == 'yes'

    def test_max_green_override(self):
        """测试最大绿时间覆盖"""
        config = MaxPressureConfig(max_green_override=True)
        queues = {0: 100.0, 1: 1.0, 2: 1.0}

        # 即使超过max_green，如果允许覆盖，仍基于压力决策
        decision = max_pressure_decision(
            current_phase_id=0,
            phase_queues=queues,
            green_elapsed=65.0,
            min_green=10.0,
            max_green=60.0,
            config=config
        )

        # 当前相位排队最大，应延长
        assert decision == 'yes'


class TestMaxPressureDecision:
    """测试压力比较决策"""

    @pytest.mark.parametrize("current_phase,queues,expected", [
        (0, {0: 10.0, 1: 5.0, 2: 3.0}, 'yes'),  # 当前相位排队最大
        (0, {0: 10.0, 1: 10.0, 2: 3.0}, 'yes'),  # 当前相位等于最大
        (0, {0: 5.0, 1: 10.0, 2: 3.0}, 'no'),   # 其他相位排队更大
        (1, {0: 5.0, 1: 15.0, 2: 3.0}, 'yes'),  # 当前相位排队明显最大
        (2, {0: 8.0, 1: 6.0, 2: 7.0}, 'no'),    # 当前相位不是最大
    ])
    def test_pressure_decision_within_time_range(self, current_phase, queues, expected):
        """时间范围内基于压力决策"""
        config = MaxPressureConfig()

        decision = max_pressure_decision(
            current_phase_id=current_phase,
            phase_queues=queues,
            green_elapsed=15.0,  # 在min_green和max_green之间
            min_green=10.0,
            max_green=60.0,
            config=config
        )

        assert decision == expected

    def test_equal_queues_extend_current(self):
        """所有相位排队相等时延长当前相位"""
        config = MaxPressureConfig()
        queues = {0: 5.0, 1: 5.0, 2: 5.0}

        decision = max_pressure_decision(
            current_phase_id=0,
            phase_queues=queues,
            green_elapsed=15.0,
            min_green=10.0,
            max_green=60.0,
            config=config
        )

        assert decision == 'yes'

    def test_pressure_threshold(self):
        """测试压力阈值"""
        config = MaxPressureConfig(pressure_threshold=2.0)
        queues = {0: 10.0, 1: 9.0, 2: 3.0}

        # 当前相位10，其他最大9，差值1 < 阈值2，不延长
        decision = max_pressure_decision(
            current_phase_id=0,
            phase_queues=queues,
            green_elapsed=15.0,
            min_green=10.0,
            max_green=60.0,
            config=config
        )

        assert decision == 'no'

        # 增大差值
        queues = {0: 12.0, 1: 9.0, 2: 3.0}
        decision = max_pressure_decision(
            current_phase_id=0,
            phase_queues=queues,
            green_elapsed=15.0,
            min_green=10.0,
            max_green=60.0,
            config=config
        )

        assert decision == 'yes'


class TestMaxPressureEdgeCases:
    """测试边界情况"""

    def test_empty_phase_queues_raises_error(self):
        """空phase_queues应抛出ValueError"""
        config = MaxPressureConfig()

        with pytest.raises(ValueError, match="当前相位.*不存在"):
            max_pressure_decision(
                current_phase_id=0,
                phase_queues={},
                green_elapsed=15.0,
                min_green=10.0,
                max_green=60.0,
                config=config
            )

    def test_missing_current_phase_raises_error(self):
        """缺少当前相位应抛出ValueError"""
        config = MaxPressureConfig()
        queues = {0: 10.0, 1: 5.0, 2: 3.0}

        with pytest.raises(ValueError, match="当前相位.*不存在"):
            max_pressure_decision(
                current_phase_id=3,  # 不存在的相位
                phase_queues=queues,
                green_elapsed=15.0,
                min_green=10.0,
                max_green=60.0,
                config=config
            )

    def test_single_phase_always_extend(self):
        """单相位场景总是延长"""
        config = MaxPressureConfig()
        queues = {0: 10.0}

        decision = max_pressure_decision(
            current_phase_id=0,
            phase_queues=queues,
            green_elapsed=15.0,
            min_green=10.0,
            max_green=60.0,
            config=config
        )

        assert decision == 'yes'

    def test_negative_queue_values(self):
        """负排队数处理（虽然不合理，但不应该崩溃）"""
        config = MaxPressureConfig()
        queues = {0: 5.0, 1: -1.0, 2: 3.0}

        decision = max_pressure_decision(
            current_phase_id=0,
            phase_queues=queues,
            green_elapsed=15.0,
            min_green=10.0,
            max_green=60.0,
            config=config
        )

        # 当前相位5 > 其他最大3，应延长
        assert decision == 'yes'

    def test_all_zero_queues(self):
        """所有相位排队为0"""
        config = MaxPressureConfig()
        queues = {0: 0.0, 1: 0.0, 2: 0.0}

        decision = max_pressure_decision(
            current_phase_id=0,
            phase_queues=queues,
            green_elapsed=15.0,
            min_green=10.0,
            max_green=60.0,
            config=config
        )

        # 所有相位排队相等，延长当前
        assert decision == 'yes'


class TestMaxPressureDecisionFromPrompt:
    """测试从prompt解析并决策"""

    def test_valid_json_prompt(self):
        """测试有效的JSON prompt"""
        config = MaxPressureConfig()
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

        decision = max_pressure_decision_from_prompt(
            prompt=prompt,
            green_elapsed=15.0,
            min_green=10.0,
            max_green=60.0,
            config=config
        )

        assert decision == 'yes'

    def test_missing_current_phase_id_raises_error(self):
        """缺少current_phase_id应抛出KeyError"""
        config = MaxPressureConfig()
        prompt_data = {
            "state": {
                "phase_metrics_by_id": {
                    "0": {"avg_queue_veh": 10.0}
                }
            }
        }
        prompt = json.dumps(prompt_data)

        with pytest.raises(KeyError):
            max_pressure_decision_from_prompt(
                prompt=prompt,
                green_elapsed=15.0,
                min_green=10.0,
                max_green=60.0,
                config=config
            )

    def test_missing_phase_metrics_raises_error(self):
        """缺少phase_metrics_by_id应抛出KeyError"""
        config = MaxPressureConfig()
        prompt_data = {
            "state": {
                "current_phase_id": 0
            }
        }
        prompt = json.dumps(prompt_data)

        with pytest.raises(KeyError):
            max_pressure_decision_from_prompt(
                prompt=prompt,
                green_elapsed=15.0,
                min_green=10.0,
                max_green=60.0,
                config=config
            )

    def test_invalid_json_raises_error(self):
        """无效JSON应抛出JSONDecodeError"""
        config = MaxPressureConfig()

        with pytest.raises(json.JSONDecodeError):
            max_pressure_decision_from_prompt(
                prompt="not a json",
                green_elapsed=15.0,
                min_green=10.0,
                max_green=60.0,
                config=config
            )


class TestBatchMaxPressureDecision:
    """测试批量决策"""

    def test_batch_all_valid(self):
        """测试批量决策全部有效"""
        config = MaxPressureConfig()
        prompts = [
            json.dumps({
                "state": {
                    "current_phase_id": 0,
                    "phase_metrics_by_id": {"0": {"avg_queue_veh": 10.0}, "1": {"avg_queue_veh": 5.0}}
                }
            }),
            json.dumps({
                "state": {
                    "current_phase_id": 0,
                    "phase_metrics_by_id": {"0": {"avg_queue_veh": 5.0}, "1": {"avg_queue_veh": 10.0}}
                }
            }),
        ]
        green_elapsed_list = [15.0, 15.0]
        min_green_list = [10.0, 10.0]
        max_green_list = [60.0, 60.0]

        decisions = batch_max_pressure_decision(
            prompts=prompts,
            green_elapsed_list=green_elapsed_list,
            min_green_list=min_green_list,
            max_green_list=max_green_list,
            config=config
        )

        assert decisions == ['yes', 'no']

    def test_batch_with_errors(self):
        """测试批量决策包含错误（返回'no'保守策略）"""
        config = MaxPressureConfig()
        prompts = [
            json.dumps({
                "state": {
                    "current_phase_id": 0,
                    "phase_metrics_by_id": {"0": {"avg_queue_veh": 10.0}, "1": {"avg_queue_veh": 5.0}}
                }
            }),
            "invalid json",  # 无效JSON
            json.dumps({
                "state": {
                    "current_phase_id": 0,
                    "phase_metrics_by_id": {"0": {"avg_queue_veh": 10.0}, "1": {"avg_queue_veh": 5.0}}
                }
            }),
        ]
        green_elapsed_list = [15.0, 15.0, 15.0]
        min_green_list = [10.0, 10.0, 10.0]
        max_green_list = [60.0, 60.0, 60.0]

        decisions = batch_max_pressure_decision(
            prompts=prompts,
            green_elapsed_list=green_elapsed_list,
            min_green_list=min_green_list,
            max_green_list=max_green_list,
            config=config
        )

        assert decisions == ['yes', 'no', 'yes']

    def test_batch_mismatched_lengths(self):
        """测试批量决策长度不匹配（应只处理到最短长度）"""
        config = MaxPressureConfig()
        prompts = [
            json.dumps({
                "state": {
                    "current_phase_id": 0,
                    "phase_metrics_by_id": {"0": {"avg_queue_veh": 10.0}}
                }
            }),
            json.dumps({
                "state": {
                    "current_phase_id": 0,
                    "phase_metrics_by_id": {"0": {"avg_queue_veh": 10.0}}
                }
            }),
        ]
        green_elapsed_list = [15.0]  # 只有1个
        min_green_list = [10.0, 10.0]
        max_green_list = [60.0, 60.0]

        # zip会停止在最短长度
        decisions = batch_max_pressure_decision(
            prompts=prompts,
            green_elapsed_list=green_elapsed_list,
            min_green_list=min_green_list,
            max_green_list=max_green_list,
            config=config
        )

        assert len(decisions) == 1
        assert decisions[0] == 'yes'


class TestComputePhasePressure:
    """测试相位压力计算"""

    def test_compute_pressure_simple(self):
        """测试简单压力计算"""
        queues = {0: 10.0, 1: 5.0, 2: 3.0}
        pressures = compute_phase_pressure(queues)

        assert pressures == {0: 10.0, 1: 5.0, 2: 3.0}

    def test_compute_pressure_with_negative_values(self):
        """测试包含负值的压力计算"""
        queues = {0: 5.0, 1: -1.0, 2: 3.0}
        pressures = compute_phase_pressure(queues)

        assert pressures == {0: 5.0, 1: -1.0, 2: 3.0}

    def test_compute_pressure_empty(self):
        """测试空队列"""
        pressures = compute_phase_pressure({})

        assert pressures == {}


class TestMaxPressureIntegrationWithMakePrompt:
    """测试与make_prompt fixture的集成"""

    def test_with_make_prompt_fixture(self, make_prompt):
        """使用make_prompt工厂创建测试数据"""
        config = MaxPressureConfig()

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

        prompt = make_prompt(prompt_data)

        decision = max_pressure_decision_from_prompt(
            prompt=prompt,
            green_elapsed=15.0,
            min_green=10.0,
            max_green=60.0,
            config=config
        )

        assert decision == 'yes'
