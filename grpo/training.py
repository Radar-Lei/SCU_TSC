#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GRPO训练脚本

使用unsloth和TRL的GRPOTrainer对SFT模型进行强化学习微调，
训练模型优化交通信号控制决策。

用法:
    python grpo/training.py
    python grpo/training.py --config config/training_config.yaml
    python grpo/training.py --config config/training_config.yaml --output-dir ./my_model

配置文件:
    使用 config/training_config.yaml 作为中央配置文件,包含SFT和GRPO的所有训练参数。
    配置结构: training.grpo.* (GRPO参数), simulation.* (仿真参数), reward.* (奖励配置)
"""

import os
import sys
import json
import argparse
from typing import Optional, List, Dict, Any, Callable

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from grpo.reward import compute_reward, batch_compute_reward, RewardChainConfig, RewardStats
from grpo.sumo_reward import ParallelSUMORewardCalculator
from grpo.config import GRPOTrainingConfig


def load_grpo_dataset(dataset_path: str):
    """
    加载GRPO数据集

    Args:
        dataset_path: 数据集路径，可以是：
                     - 单个JSON文件
                     - 目录（自动扫描所有grpo_dataset.json）

    Returns:
        dataset: HuggingFace Dataset对象，格式为TRL GRPOTrainer期望的格式
    """
    from datasets import Dataset
    import glob
    from grpo.config import SYSTEM_PROMPT

    # 检查是文件还是目录
    if os.path.isfile(dataset_path):
        json_files = [dataset_path]
    elif os.path.isdir(dataset_path):
        # 扫描目录下所有grpo_dataset.json
        json_files = glob.glob(os.path.join(dataset_path, "*/grpo_dataset.json"))
        if not json_files:
            raise ValueError(f"在目录 {dataset_path} 中未找到任何 grpo_dataset.json 文件")
    else:
        raise ValueError(f"dataset_path 既不是文件也不是目录: {dataset_path}")

    # 读取所有数据
    all_data = []
    for json_file in json_files:
        print(f"正在加载数据集: {json_file}")
        # 获取场景目录（grpo_dataset.json 所在目录）
        scenario_dir = os.path.dirname(json_file)
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # 将 state_file 转换为绝对路径，并保存场景目录
            for item in data:
                # 转换 state_file 为绝对路径
                state_file = item.get("state_file", "")
                if state_file and not os.path.isabs(state_file):
                    item["state_file"] = os.path.join(scenario_dir, state_file)
                # 保存场景目录（用于后续查找 sumocfg）
                item["scenario_dir"] = scenario_dir
            all_data.extend(data)

    print(f"总共加载了 {len(all_data)} 条GRPO数据")

    # 转换为TRL GRPOTrainer期望的格式
    # GRPOTrainer期望：prompt是一个messages列表，格式为 [{"role": "system", "content": ...}, {"role": "user", "content": ...}]
    grpo_data = []
    for item in all_data:
        # 获取原始JSON prompt
        raw_prompt = item.get("prompt", "")
        
        # 构建完整的 system prompt (包含JSON示例)
        # 使用 replace 而不是 format，因为模板中包含其他花括号（如 {"extend": "yes/no"}）
        full_system_prompt = SYSTEM_PROMPT.replace("{extend_decision_input_json}", raw_prompt)
        
        # 构建messages格式的prompt
        # GRPOTrainer期望的格式: [{"role": "system", "content": ...}, {"role": "user", "content": ...}]
        messages = [
            {"role": "system", "content": full_system_prompt},
            {"role": "user", "content": raw_prompt}
        ]
        
        grpo_data.append({
            "prompt": messages,  # 使用messages格式，供GRPOTrainer使用
            "raw_prompt": raw_prompt,  # 保存原始JSON字符串，供reward计算和baseline使用
            "id": item.get("id", ""),
            "scenario": item.get("scenario", ""),
            "junction_id": item.get("junction_id", ""),
            # 保存state_file路径，用于reward计算
            "state_file": item.get("state_file", ""),
            # 保存时间参数，用于Max Pressure baseline计算
            "current_green_elapsed": item.get("current_green_elapsed", None),
            "min_green": item.get("min_green", None),
            "max_green": item.get("max_green", None),
            # 暂时不包含expert_decision，因为GRPO需要通过reward函数评估
        })

    dataset = Dataset.from_list(grpo_data)
    print(f"转换为GRPO格式: {len(dataset)} 条数据")

    return dataset


def create_reward_function(
    chain_config: RewardChainConfig,
    sumo_config,
    dataset,
    enable_baseline_tracking: bool = False,
    mp_config = None
) -> Callable:
    """
    创建GRPOTrainer使用的reward函数

    GRPOTrainer期望的签名: (prompts, outputs, **kwargs) -> List[float]

    Args:
        chain_config: Reward函数链配置
        sumo_config: SUMO配置
        dataset: 数据集（用于获取state_files）
        enable_baseline_tracking: 是否启用Max Pressure baseline追踪
        mp_config: Max Pressure配置对象

    Returns:
        reward函数
    """
    # 预加载state_files（按数据集顺序）
    state_files = dataset["state_file"]

    # 预加载原始 JSON prompts（用于TSC reward计算和baseline计算）
    # raw_prompt 是原始 JSON 字符串，prompt 是 messages 格式（供 GRPOTrainer 使用）
    column_names = dataset.column_names
    raw_prompts = dataset["raw_prompt"] if "raw_prompt" in column_names else dataset["prompt"]

    # 预加载时间参数（用于Max Pressure baseline计算）
    green_elapsed_list = dataset["current_green_elapsed"] if "current_green_elapsed" in column_names else [None] * len(dataset)
    min_green_list = dataset["min_green"] if "min_green" in column_names else [None] * len(dataset)
    max_green_list = dataset["max_green"] if "max_green" in column_names else [None] * len(dataset)

    # 预计算baseline决策（如果启用）
    baseline_decisions = None
    if enable_baseline_tracking:
        try:
            from grpo.max_pressure import batch_max_pressure_decision, MaxPressureConfig

            # 使用提供的配置或默认配置
            baseline_config = mp_config if mp_config is not None else MaxPressureConfig()

            # 批量计算baseline决策
            # 使用 raw_prompt（原始JSON字符串），而不是 prompt（messages格式）
            baseline_decisions = batch_max_pressure_decision(
                prompts=dataset["raw_prompt"],
                green_elapsed_list=green_elapsed_list,
                min_green_list=min_green_list,
                max_green_list=max_green_list,
                config=baseline_config
            )
            print(f"已预计算 {len(baseline_decisions)} 个baseline决策")
        except Exception as e:
            print(f"警告: Baseline预计算失败: {e}")
            print(f"禁用baseline追踪")
            enable_baseline_tracking = False
            baseline_decisions = None

    def reward_fn(completions, prompts=None, **kwargs) -> List[float]:
        """
        GRPOTrainer调用的reward函数
        
        新版TRL的签名是 (completions, prompts=None, **kwargs)
        - completions: 列表，每个元素是 messages 格式，如 [[{"role": "assistant", "content": "..."}], ...]
        - prompts: 可选，prompts列表
        """
        # 调试：打印 completions 的格式
        if len(completions) > 0:
            print(f"\n[DEBUG] completions type: {type(completions)}")
            print(f"[DEBUG] completions length: {len(completions)}")
            print(f"[DEBUG] completions[0] type: {type(completions[0])}")
            print(f"[DEBUG] completions[0] value: {completions[0][:200] if isinstance(completions[0], str) else completions[0]}")
            if len(completions) > 1:
                print(f"[DEBUG] completions[1] type: {type(completions[1])}")
                print(f"[DEBUG] completions[1] value: {completions[1][:200] if isinstance(completions[1], str) else completions[1]}")
        
        # 从 completions 中提取 outputs（模型生成的文本）
        # completions 格式: [[{"role": "assistant", "content": "..."}], ...]
        outputs = []
        for completion in completions:
            if isinstance(completion, list) and len(completion) > 0:
                # messages 格式
                if isinstance(completion[0], dict) and "content" in completion[0]:
                    outputs.append(completion[0]["content"])
                else:
                    outputs.append(str(completion[0]))
            elif isinstance(completion, str):
                outputs.append(completion)
            else:
                outputs.append(str(completion))
        
        # 调试：打印提取后的 outputs
        if len(outputs) > 0:
            print(f"[DEBUG] outputs[0]: {outputs[0][:200] if len(outputs[0]) > 200 else outputs[0]}")
        
        # 确保prompts和state_files长度匹配
        # 注意: GRPO可能对每个prompt生成多个output，需要正确对齐
        n = len(outputs)
        aligned_state_files = state_files[:n] if len(state_files) >= n else state_files

        # 对齐时间参数
        aligned_green_elapsed = green_elapsed_list[:n] if len(green_elapsed_list) >= n else green_elapsed_list
        aligned_min_green = min_green_list[:n] if len(min_green_list) >= n else min_green_list
        aligned_max_green = max_green_list[:n] if len(max_green_list) >= n else max_green_list

        # 构建 prompts 列表（用于 TSC reward 计算和 baseline 计算）
        # 使用 raw_prompts（原始 JSON 字符串），而不是 prompt（messages 格式）
        prompts_to_use = raw_prompts[:n] if len(raw_prompts) >= n else raw_prompts

        rewards, stats = batch_compute_reward(
            prompts=prompts_to_use,
            outputs=outputs,
            state_files=aligned_state_files,
            chain_config=chain_config,
            sumo_config=sumo_config,
            green_elapsed_list=aligned_green_elapsed,
            min_green_list=aligned_min_green,
            max_green_list=aligned_max_green,
            enable_baseline=enable_baseline_tracking,
            mp_config=mp_config
        )

        # 打印统计信息
        print(f"\n{'='*50}")
        print(f"Reward Statistics:")
        print(f"  Total: {stats.total_count}")
        print(f"  Format accuracy: {stats.format_accuracy:.1%}")
        print(f"  Strict: {stats.strict_format_count}, Partial: {stats.partial_format_count}, Invalid: {stats.invalid_format_count}")
        print(f"  Avg format reward: {stats.avg_format_reward:.3f}")
        print(f"  Avg TSC reward: {stats.avg_tsc_reward:.3f}")
        print(f"  Avg final reward: {stats.avg_final_reward:.3f}")

        # 计算并打印baseline准确率（如果启用）
        if enable_baseline_tracking and baseline_decisions is not None:
            try:
                from grpo.reward import extract_decision
                from grpo.max_pressure import compare_with_baseline

                # 提取模型决策
                model_decisions = [
                    extract_decision(o, chain_config.extract_regex)
                    for o in outputs
                    if extract_decision(o, chain_config.extract_regex) is not None
                ]

                # 对齐baseline决策
                aligned_baseline = baseline_decisions[:len(model_decisions)] if len(baseline_decisions) >= len(model_decisions) else baseline_decisions

                # 计算准确率
                if model_decisions and len(model_decisions) == len(aligned_baseline):
                    matches = compare_with_baseline(model_decisions, aligned_baseline)
                    accuracy = sum(matches) / len(matches) if matches else 0.0
                    print(f"  Baseline Accuracy: {accuracy:.2%} ({sum(matches)}/{len(matches)})")
                else:
                    print(f"  Baseline Comparison: Skipped (decision count mismatch)")
            except Exception as e:
                print(f"  Baseline Comparison Error: {e}")

        print(f"{'='*50}\n")

        return rewards

    return reward_fn


def reward_function_placeholder(prompts: List[str], outputs: List[str], **kwargs) -> List[float]:
    """
    Reward函数占位符（已弃用）

    在01-04中已实现完整的reward函数链，请使用create_reward_function创建reward函数。

    此函数保留仅用于向后兼容。
    """
    print("警告: 使用占位符reward函数（返回固定0.0）")
    print("      请使用create_reward_function创建完整的reward函数链")

    # 返回固定值
    return [0.0] * len(outputs)


def train_grpo(
    config,
    training_config=None,
    model_path: str = None,
    dataset_path: str = None,
    output_dir: str = None,
    learning_rate: float = None,
    batch_size: int = None,
    num_epochs: int = None,
    max_steps: int = None,
):
    """
    执行GRPO训练

    优先级：命令行参数 > 配置文件 > 默认值

    Args:
        config: GRPOTrainingConfig配置对象（来自grpo_config.yaml或从training_config转换）
        training_config: TrainingConfig配置对象（可选，来自training_config.yaml）
        model_path: 模型路径（覆盖配置文件）
        dataset_path: 数据集路径（覆盖配置文件）
        output_dir: 输出目录（覆盖配置文件）
        learning_rate: 学习率（覆盖配置文件）
        batch_size: 批次大小（覆盖配置文件）
        num_epochs: 训练轮数（覆盖配置文件）
        max_steps: 最大训练步数（覆盖配置文件）
    """
    # 应用命令行参数覆盖
    if model_path is not None:
        config.model_path = model_path
    if dataset_path is not None:
        config.dataset_path = dataset_path
    if output_dir is not None:
        config.output_dir = output_dir
    if learning_rate is not None:
        config.learning_rate = learning_rate
    if batch_size is not None:
        config.batch_size = batch_size
    if num_epochs is not None:
        config.num_train_epochs = num_epochs

    # 如果提供了training_config，打印信息
    if training_config is not None:
        print("使用training_config.yaml中的配置")

    print("=" * 60)
    print("GRPO训练")
    print("=" * 60)
    print(f"模型路径: {config.model_path}")
    print(f"数据集路径: {config.dataset_path}")
    print(f"输出目录: {config.output_dir}")
    print(f"学习率: {config.learning_rate}")
    print(f"批次大小: {config.batch_size}")
    print(f"梯度累积步数: {config.gradient_accumulation_steps}")
    print(f"生成候选数: {config.num_generations}")
    print(f"温度: {config.temperature}")
    print(f"KL系数: {config.kl_coeff}")
    print(f"训练轮数: {config.num_train_epochs}")
    print(f"Format权重: {config.reward.format_weight}")
    print(f"TSC权重: {config.reward.tsc_weight}")

    # 打印baseline配置
    enable_baseline = getattr(config, 'enable_baseline', False)
    print(f"Baseline追踪: {'启用' if enable_baseline else '禁用'}")
    if enable_baseline:
        baseline_config = getattr(config, 'baseline_config', None)
        if baseline_config is not None:
            print(f"  - 最小绿偏移: {baseline_config.min_green_offset}s")
            print(f"  - 压力阈值: {baseline_config.pressure_threshold}")
            print(f"  - 允许覆盖最大绿: {baseline_config.max_green_override}")

    print("=" * 60)

    # 导入依赖
    if isinstance(getattr(config, "model_path", None), str) and os.path.isdir(config.model_path):
        os.environ["UNSLOTH_USE_MODELSCOPE"] = "0"
    from unsloth import FastLanguageModel
    from trl import GRPOTrainer, GRPOConfig
    from transformers import TrainingArguments
    import torch

    # 加载SFT模型
    print("\n正在加载SFT模型...")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=config.model_path,
        max_seq_length=config.max_seq_length,
        load_in_4bit=False,  # GRPO训练使用16bit
        dtype=None,  # 自动检测
    )

    # 添加LoRA适配器（如果SFT模型未包含）
    print("正在配置LoRA...")
    model = FastLanguageModel.get_peft_model(
        model,
        r=config.lora_rank,
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj",
        ],
        lora_alpha=config.lora_rank * 2,
        use_gradient_checkpointing="unsloth" if config.gradient_checkpointing else False,
        random_state=config.seed,
    )

    # 加载数据集
    print("\n正在加载数据集...")
    train_dataset = load_grpo_dataset(config.dataset_path)
    print(f"加载了 {len(train_dataset)} 条训练数据")

    # 创建reward函数链配置
    print("\n正在配置reward函数链...")
    from types import SimpleNamespace
    reward_chain_config = RewardChainConfig(
        format_weight=config.reward.format_weight,
        tsc_weight=config.reward.tsc_weight,
        format_strict=config.format_reward.strict,
        format_partial=config.format_reward.partial,
        format_invalid=config.format_reward.invalid,
        extract_regex=config.format_reward.extract_regex
    )

    # 创建SUMO配置
    sumo_config = SimpleNamespace(
        max_workers=config.sumo.max_workers,
        extend_seconds=config.sumo.extend_seconds,
        reward_scale=config.sumo.reward_scale,
        port_range=config.sumo.port_range
    )

    # 创建reward函数
    reward_fn = create_reward_function(
        chain_config=reward_chain_config,
        sumo_config=sumo_config,
        dataset=train_dataset,
        enable_baseline_tracking=getattr(config, 'enable_baseline', False),
        mp_config=getattr(config, 'baseline_config', None)
    )

    # 配置GRPO训练参数
    print("正在配置GRPO训练参数...")

    # 创建TRL的GRPOConfig（注意区别于我们自己的GRPOTrainingConfig）
    grpo_config = GRPOConfig(
        # 训练批次参数
        per_device_train_batch_size=config.batch_size,
        gradient_accumulation_steps=config.gradient_accumulation_steps,
        learning_rate=config.learning_rate,

        # GRPO特定参数
        num_generations=config.num_generations,
        temperature=config.temperature,
        max_completion_length=config.max_new_tokens,
        top_p=config.top_p,
        repetition_penalty=config.repetition_penalty,

        # KL散度控制（beta参数）
        beta=config.kl_coeff,

        # 训练参数
        num_train_epochs=config.num_train_epochs,
        max_steps=max_steps if max_steps is not None else -1,
        warmup_steps=config.warmup_steps,
        logging_steps=config.logging_steps,
        save_steps=config.save_steps,
        optim=config.optim,

        # 输出路径
        output_dir=config.output_dir,

        # 其他参数
        seed=config.seed,
        report_to="wandb" if config.use_wandb else "none",
        save_total_limit=2,
        
        # 禁用移除未使用的列，确保reward计算可以访问state_file等元数据
        remove_unused_columns=False,
    )

    # 设置wandb run名称
    if config.use_wandb and config.wandb_run_name:
        import wandb
        wandb.init(project=config.wandb_project, name=config.wandb_run_name)

    # 创建GRPO训练器
    print("\n正在创建GRPO训练器...")
    trainer = GRPOTrainer(
        model=model,
        reward_funcs=reward_fn,  # 使用完整的reward函数链
        args=grpo_config,
        train_dataset=train_dataset,
    )

    # 开始训练
    print("\n开始训练...")
    trainer.train()

    # 保存模型
    print(f"\n正在保存模型到 {config.output_dir}...")
    model.save_pretrained(config.output_dir)
    tokenizer.save_pretrained(config.output_dir)

    # 同时保存merged模型（用于推理）
    merged_dir = os.path.join(config.output_dir, "merged")
    print(f"正在保存合并后的模型到 {merged_dir}...")
    model.save_pretrained_merged(merged_dir, tokenizer, save_method="merged_16bit")

    print("\nGRPO训练完成!")
    print(f"LoRA模型: {config.output_dir}")
    print(f"合并模型: {merged_dir}")

    return model, tokenizer


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="GRPO训练脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="训练配置文件路径（支持grpo_config.yaml或training_config.yaml）"
    )

    # 支持命令行参数覆盖配置文件
    parser.add_argument(
        "--model-path",
        type=str,
        default=None,
        help="SFT模型路径（覆盖配置文件）"
    )
    parser.add_argument(
        "--dataset-path",
        type=str,
        default=None,
        help="GRPO数据集路径（覆盖配置文件）"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="模型输出目录（覆盖配置文件）"
    )
    parser.add_argument(
        "--learning-rate",
        type=float,
        default=None,
        help="学习率（覆盖配置文件）"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=None,
        help="批次大小（覆盖配置文件）"
    )
    parser.add_argument(
        "--num-epochs",
        type=int,
        default=None,
        help="训练轮数（覆盖配置文件）"
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=None,
        help="最大训练步数（覆盖配置文件，用于调试）"
    )

    return parser.parse_args()


def main():
    """主函数"""
    args = parse_args()

    # 确定配置文件类型
    if args.config is None:
        # 默认使用training_config.yaml
        config_path = "config/training_config.yaml"
        use_training_config = True
    else:
        config_path = args.config
        # 根据文件名判断配置类型
        if "training_config.yaml" in args.config:
            use_training_config = True
        else:
            use_training_config = False

    # 加载配置
    from grpo.config import GRPOTrainingConfig, load_training_config

    if use_training_config:
        # 使用training_config.yaml
        training_config = load_training_config(config_path)
        config = training_config.grpo  # 转换为GRPOTrainingConfig
        print(f"已加载中央训练配置: {config_path}")
    else:
        # 使用grpo_config.yaml
        config = GRPOTrainingConfig.from_yaml(config_path)
        training_config = None
        print(f"已加载GRPO训练配置: {config_path}")

    # 执行训练
    train_grpo(
        config,
        training_config=training_config,
        model_path=args.model_path,
        dataset_path=args.dataset_path,
        output_dir=args.output_dir,
        learning_rate=args.learning_rate,
        batch_size=args.batch_size,
        num_epochs=args.num_epochs,
        max_steps=args.max_steps,
    )


if __name__ == "__main__":
    main()
