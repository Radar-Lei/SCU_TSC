# -*- coding: utf-8 -*-
"""
GRPO Reward函数模块

包含format_reward_fn和相关辅助函数，用于验证模型输出格式并计算奖励。
"""

import json
import re
from typing import Optional, List
from dataclasses import dataclass


@dataclass
class FormatResult:
    """格式验证结果"""
    reward: float
    is_strict: bool
    is_partial: bool
    extracted_decision: Optional[str]  # "yes", "no", or None


def extract_decision(text: str, regex: str) -> Optional[str]:
    """
    使用正则表达式从文本中提取yes/no决策

    Args:
        text: 待提取的文本
        regex: 正则表达式，默认提取 {"extend": "yes/no"} 格式

    Returns:
        小写的 "yes" 或 "no"，或 None
    """
    try:
        match = re.search(regex, text, re.IGNORECASE | re.DOTALL)
        if match:
            decision = match.group(1).lower()
            if decision in ["yes", "no"]:
                return decision
    except Exception:
        pass
    return None


def format_reward_fn(
    output: str,
    regex: str = None,
    strict_reward: float = 1.0,
    partial_reward: float = -0.5,
    invalid_reward: float = -10.0
) -> FormatResult:
    """
    验证模型输出格式并返回奖励

    评分机制:
    1. 严格format → +strict_reward: 精确匹配 {"extend": "yes"} 或 {"extend": "no"}
    2. 部分遵守format → +partial_reward: 能通过正则提取yes/no（如带额外空格、换行）
    3. 完全不遵守format → +invalid_reward: 无法提取决策或格式错误

    Args:
        output: 模型输出的文本
        regex: 正则表达式，默认匹配 {"extend": "yes/no"} 及其变体
        strict_reward: 严格格式的奖励值
        partial_reward: 部分遵守格式的奖励值
        invalid_reward: 完全不遵守格式的奖励值

    Returns:
        FormatResult对象，包含reward和格式验证结果
    """
    # 默认正则表达式：匹配 {"extend": "yes/no"} 及其变体
    # 允许yes/no后有逗号或右括号，以处理带额外字段的JSON
    if regex is None:
        regex = r'\{["\s]*extend["\s]*:\s*["\s]*(yes|no)["\s]*(?:,|\})'

    # 第一步：尝试严格JSON解析
    try:
        parsed = json.loads(output.strip())

        # 验证是否为字典
        if isinstance(parsed, dict):
            # 验证是否只有"extend"键
            if len(parsed) == 1 and "extend" in parsed:
                value = parsed["extend"]
                # 验证值是否为"yes"或"no"
                if isinstance(value, str) and value.lower() in ["yes", "no"]:
                    return FormatResult(
                        reward=strict_reward,
                        is_strict=True,
                        is_partial=False,
                        extracted_decision=value.lower()
                    )
    except (json.JSONDecodeError, TypeError, ValueError):
        pass

    # 第二步：如果不是严格格式，使用正则提取
    decision = extract_decision(output, regex)
    if decision:
        return FormatResult(
            reward=partial_reward,
            is_strict=False,
            is_partial=True,
            extracted_decision=decision
        )

    # 第三步：都不成功，返回无效奖励
    return FormatResult(
        reward=invalid_reward,
        is_strict=False,
        is_partial=False,
        extracted_decision=None
    )


def batch_format_reward(outputs: List[str], **kwargs) -> List[float]:
    """
    批量处理版本，供GRPOTrainer使用

    Args:
        outputs: 模型输出列表
        **kwargs: 传递给format_reward_fn的参数

    Returns:
        每个output的reward列表
    """
    rewards = []
    for output in outputs:
        result = format_reward_fn(output, **kwargs)
        rewards.append(result.reward)
    return rewards
