# -*- coding: utf-8 -*-
"""
GRPO Reward函数模块

包含format_reward_fn、reward函数链和相关辅助函数，用于验证模型输出格式并计算奖励。
"""

import json
import re
from typing import Optional, List, Tuple, Callable, Dict, Any
from dataclasses import dataclass


@dataclass
class FormatResult:
    """格式验证结果"""
    reward: float
    is_strict: bool
    is_partial: bool
    extracted_decision: Optional[str]  # "yes", "no", or None


@dataclass
class RewardStats:
    """Reward统计信息"""
    total_count: int
    strict_format_count: int
    partial_format_count: int
    invalid_format_count: int
    avg_format_reward: float
    avg_tsc_reward: float
    avg_final_reward: float
    format_accuracy: float  # (strict + partial) / total


@dataclass
class RewardChainConfig:
    """Reward函数链配置"""
    format_weight: float = 1.0
    tsc_weight: float = 1.0
    # Format reward评分
    format_strict: float = 1.0
    format_partial: float = -0.5
    format_invalid: float = -10.0
    # 正则表达式
    extract_regex: str = r'\{["\s]*extend["\s]*:\s*["\s]*(yes|no)["\s]*\}'


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


def compute_reward(
    prompt: str,
    output: str,
    state_file: str,
    chain_config: RewardChainConfig,
    sumo_config: Any,
    tsc_reward_fn: Callable = None
) -> Tuple[float, Dict[str, Any]]:
    """
    计算单个样本的reward

    Args:
        prompt: 输入prompt
        output: 模型输出
        state_file: SUMO状态文件路径
        chain_config: Reward函数链配置
        sumo_config: SUMO配置
        tsc_reward_fn: TSC reward函数（可选，用于测试）

    Returns:
        (final_reward, info_dict)
    """
    # 1. 计算format reward
    format_result = format_reward_fn(
        output,
        regex=chain_config.extract_regex,
        strict_reward=chain_config.format_strict,
        partial_reward=chain_config.format_partial,
        invalid_reward=chain_config.format_invalid
    )

    # 2. 如果完全不遵守format，直接返回
    if not format_result.is_partial and not format_result.is_strict:
        return format_result.reward, {
            "format_reward": format_result.reward,
            "tsc_reward": 0.0,
            "reason": "invalid_format"
        }

    # 3. 计算TSC reward
    if tsc_reward_fn is None:
        from .sumo_reward import calculate_tsc_reward_single
        tsc_reward_fn = calculate_tsc_reward_single

    # 从output提取决策
    decision = format_result.extracted_decision
    if decision is None:
        # 无法提取决策，返回format reward
        return format_result.reward, {
            "format_reward": format_result.reward,
            "tsc_reward": 0.0,
            "reason": "no_decision_extracted"
        }

    tsc_result = tsc_reward_fn(state_file, prompt, decision, sumo_config)
    tsc_reward = tsc_result.reward if tsc_result.success else 0.0

    # 4. 组合reward
    final_reward = (
        chain_config.format_weight * format_result.reward +
        chain_config.tsc_weight * tsc_reward
    )

    return final_reward, {
        "format_reward": format_result.reward,
        "tsc_reward": tsc_reward,
        "is_strict": format_result.is_strict,
        "is_partial": format_result.is_partial,
    }


def batch_compute_reward(
    prompts: List[str],
    outputs: List[str],
    state_files: List[str],
    chain_config: RewardChainConfig,
    sumo_config: Any
) -> Tuple[List[float], RewardStats]:
    """
    批量计算reward（GRPOTrainer调用接口）

    Args:
        prompts: 输入prompt列表
        outputs: 模型输出列表
        state_files: 状态文件路径列表
        chain_config: Reward函数链配置
        sumo_config: SUMO配置

    Returns:
        (rewards列表, 统计信息)
    """
    from .sumo_reward import ParallelSUMORewardCalculator

    # 先计算所有format reward
    format_results = [
        format_reward_fn(
            output,
            regex=chain_config.extract_regex,
            strict_reward=chain_config.format_strict,
            partial_reward=chain_config.format_partial,
            invalid_reward=chain_config.format_invalid
        )
        for output in outputs
    ]

    # 筛选需要计算TSC的样本
    needs_tsc_indices = [
        i for i, r in enumerate(format_results)
        if r.is_strict or r.is_partial
    ]

    # 批量计算TSC reward（使用并行）
    tsc_rewards = [0.0] * len(outputs)
    if needs_tsc_indices:
        calculator = ParallelSUMORewardCalculator(max_workers=sumo_config.max_workers)

        # 准备需要计算TSC的样本
        tsc_prompts = [prompts[i] for i in needs_tsc_indices]
        tsc_outputs = [outputs[i] for i in needs_tsc_indices]
        tsc_state_files = [state_files[i] for i in needs_tsc_indices]

        try:
            tsc_results = calculator.calculate_batch(
                prompts=tsc_prompts,
                outputs=tsc_outputs,
                state_files=tsc_state_files,
                config=sumo_config
            )
            for idx, reward in zip(needs_tsc_indices, tsc_results):
                tsc_rewards[idx] = reward
        except RuntimeError as e:
            # SUMO计算失败，所有TSC reward为0
            print(f"Warning: TSC reward calculation failed: {e}")
            print(f"Using format reward only for {len(needs_tsc_indices)} samples")

    # 组合最终reward
    final_rewards = []
    for i, format_result in enumerate(format_results):
        final_reward = (
            chain_config.format_weight * format_result.reward +
            chain_config.tsc_weight * tsc_rewards[i]
        )
        final_rewards.append(final_reward)

    # 计算统计信息
    stats = RewardStats(
        total_count=len(outputs),
        strict_format_count=sum(1 for r in format_results if r.is_strict),
        partial_format_count=sum(1 for r in format_results if r.is_partial),
        invalid_format_count=sum(1 for r in format_results if not r.is_strict and not r.is_partial),
        avg_format_reward=sum(r.reward for r in format_results) / len(outputs),
        avg_tsc_reward=sum(tsc_rewards) / len(outputs),
        avg_final_reward=sum(final_rewards) / len(outputs),
        format_accuracy=(sum(1 for r in format_results if r.is_strict or r.is_partial) / len(outputs))
    )

    return final_rewards, stats
