# -*- coding: utf-8 -*-
"""
format_reward_fn单元测试

测试format_reward_fn的所有边界情况：
- 严格有效格式（strict valid）
- 部分有效格式（partial valid）
- 无效格式（invalid）
- 自定义正则表达式
- extract_decision函数
"""

import pytest
from grpo.reward import format_reward_fn, extract_decision, FormatResult


class TestFormatRewardStrictValid:
    """测试严格有效格式"""

    @pytest.mark.parametrize("output,expected_decision", [
        ('{"extend": "yes"}', "yes"),
        ('{"extend": "no"}', "no"),
        ('{"extend":"yes"}', "yes"),  # 无空格
        ('{"extend":"no"}', "no"),    # 无空格
        ('{ "extend" : "yes" }', "yes"),  # 额外空格但严格JSON
        ('{ "extend" : "no" }', "no"),
    ])
    def test_strict_valid_json_returns_1_0(self, output, expected_decision):
        """严格有效格式应返回reward=1.0, is_strict=True"""
        result = format_reward_fn(output)

        assert result.reward == 1.0
        assert result.is_strict is True
        assert result.is_partial is False
        assert result.extracted_decision == expected_decision

    def test_strict_valid_case_insensitive(self):
        """严格格式中extend值不区分大小写（应为小写）"""
        result_yes = format_reward_fn('{"extend": "YES"}')
        assert result_yes.reward == 1.0
        assert result_yes.extracted_decision == "yes"

        result_no = format_reward_fn('{"extend": "NO"}')
        assert result_no.reward == 1.0
        assert result_no.extracted_decision == "no"


class TestFormatRewardPartialValid:
    """测试部分有效格式"""

    @pytest.mark.parametrize("output,expected_decision", [
        ('Some text {"extend": "yes"} more text', "yes"),
        ('{"extend": "yes", "extra_field": "value"}', "yes"),  # 额外字段
        ('{"extend": "yes", }', "yes"),  # 尾随逗号
    ])
    def test_partial_valid_returns_negative_0_5(self, output, expected_decision):
        """部分有效格式应返回reward=-0.5, is_partial=True"""
        result = format_reward_fn(output)

        assert result.reward == -0.5
        assert result.is_strict is False
        assert result.is_partial is True
        assert result.extracted_decision == expected_decision

    @pytest.mark.parametrize("output,expected_decision", [
        ('{\n  "extend": "no"\n}', "no"),  # 换行
        ('  {  "extend"  :  "no"  }  ', "no"),  # 大量空格
    ])
    def test_whitespace_is_still_strict_json(self, output, expected_decision):
        """换行和空格仍然是严格JSON格式（json.loads可解析）"""
        result = format_reward_fn(output)

        # 这些实际上会被JSON.loads解析为严格格式
        assert result.reward == 1.0
        assert result.is_strict is True
        assert result.extracted_decision == expected_decision


class TestFormatRewardInvalid:
    """测试无效格式"""

    @pytest.mark.parametrize("output", [
        "",                     # 空字符串
        "   ",                 # 仅空格
        "not a json at all",   # 非JSON
        '{"wrong_key": "yes"}', # 错误的键
        '{"extend": "invalid"}', # 无效的extend值
        '{"extend": true}',    # 非字符串值
        '{"extend": 1}',       # 数字值
        '{"extend": "yes"',    # 缺少右花括号
        'extend": "yes"}',     # 缺少左花括号
    ])
    def test_invalid_returns_negative_10_0(self, output):
        """无效格式应返回reward=-10.0, is_strict=False, is_partial=False"""
        result = format_reward_fn(output)

        assert result.reward == -10.0
        assert result.is_strict is False
        assert result.is_partial is False
        assert result.extracted_decision is None

    def test_none_input_returns_invalid(self):
        """None输入应返回invalid"""
        result = format_reward_fn(None)
        assert result.reward == -10.0
        assert result.is_strict is False
        assert result.is_partial is False
        assert result.extracted_decision is None


class TestFormatRewardCustomRegex:
    """测试自定义正则表达式"""

    def test_custom_regex_pattern(self):
        """测试自定义正则表达式参数"""
        custom_regex = r'DECISION[:\s]+(yes|no)'

        result = format_reward_fn('DECISION: yes', regex=custom_regex)
        assert result.reward == -0.5  # 部分有效（通过正则提取）
        assert result.extracted_decision == "yes"

        result = format_reward_fn('DECISION: no', regex=custom_regex)
        assert result.reward == -0.5
        assert result.extracted_decision == "no"

    def test_custom_regex_fallback_to_json_when_no_match(self):
        """自定义正则表达式不匹配时，如果JSON严格格式仍应返回strict"""
        custom_regex = r'DECISION[:\s]+(yes|no)'

        # 虽然自定义正则不匹配，但这是严格JSON格式
        result = format_reward_fn('{"extend": "yes"}', regex=custom_regex)
        assert result.reward == 1.0  # 严格JSON
        assert result.is_strict is True


class TestExtractDecision:
    """测试extract_decision辅助函数"""

    @pytest.mark.parametrize("text,expected", [
        ('{"extend": "yes"}', "yes"),
        ('{"extend": "no"}', "no"),
        ('Some text {"extend": "yes"} more', "yes"),
        ('{"extend":"yes"}', "yes"),
        ('{  "extend"  :  "no"  }', "no"),
        ('{"Extend": "yes"}', "yes"),  # 不区分大小写
        ('{"EXTEND": "NO"}', "no"),
    ])
    def test_extract_decision_success(self, text, expected):
        """成功提取决策"""
        result = extract_decision(text, r'\{["\s]*extend["\s]*:\s*["\s]*(yes|no)["\s]*(?:,|\})')
        assert result == expected

    @pytest.mark.parametrize("text", [
        "no decision here",
        '{"wrong_key": "yes"}',
        "",
        "just random text",
    ])
    def test_extract_decision_failure(self, text):
        """无法提取决策应返回None"""
        result = extract_decision(text, r'\{["\s]*extend["\s]*:\s*["\s]*(yes|no)["\s]*(?:,|\})')
        assert result is None

    def test_extract_decision_with_custom_regex(self):
        """测试自定义正则表达式"""
        custom_regex = r'DECISION[:\s]+(yes|no)'

        result = extract_decision('DECISION: yes', custom_regex)
        assert result == "yes"

        result = extract_decision('DECISION: no', custom_regex)
        assert result == "no"


class TestFormatRewardCustomRewards:
    """测试自定义reward值"""

    def test_custom_strict_reward(self):
        """测试自定义strict_reward参数"""
        result = format_reward_fn('{"extend": "yes"}', strict_reward=5.0)
        assert result.reward == 5.0
        assert result.is_strict is True

    def test_custom_partial_reward(self):
        """测试自定义partial_reward参数"""
        result = format_reward_fn('text {"extend": "yes"}', partial_reward=-1.0)
        assert result.reward == -1.0
        assert result.is_partial is True

    def test_custom_invalid_reward(self):
        """测试自定义invalid_reward参数"""
        result = format_reward_fn('invalid', invalid_reward=-5.0)
        assert result.reward == -5.0
        assert result.is_strict is False
        assert result.is_partial is False


class TestFormatRewardEdgeCases:
    """测试边界情况"""

    def test_empty_json_object(self):
        """空JSON对象"""
        result = format_reward_fn('{}')
        assert result.reward == -10.0
        assert result.extracted_decision is None

    def test_json_with_null_fields(self):
        """JSON中包含null字段"""
        result = format_reward_fn('{"extend": null}')
        assert result.reward == -10.0

    def test_json_array(self):
        """JSON数组而非对象"""
        result = format_reward_fn('["extend", "yes"]')
        assert result.reward == -10.0

    def test_nested_json(self):
        """嵌套JSON（非严格格式）"""
        result = format_reward_fn('{"data": {"extend": "yes"}}')
        # 正则应该能提取到
        assert result.reward == -0.5
        assert result.extracted_decision == "yes"

    def test_multiple_extend_fields(self):
        """多个extend字段（JSON解析取最后一个值，仍为严格格式）"""
        result = format_reward_fn('{"extend": "yes", "extend": "no"}')
        # JSON.loads会取最后一个值，且只有唯一键"extend"
        assert result.reward == 1.0  # 严格格式
        assert result.is_strict is True
        assert result.extracted_decision == "no"

    def test_unicode_characters(self):
        """Unicode字符"""
        result = format_reward_fn('{"extend": "yes"} 你好世界')
        assert result.reward == -0.5
        assert result.extracted_decision == "yes"

    def test_very_long_output(self):
        """非常长的输出"""
        long_output = "x" * 10000 + ' {"extend": "yes"} ' + "y" * 10000
        result = format_reward_fn(long_output)
        assert result.reward == -0.5
        assert result.extracted_decision == "yes"
