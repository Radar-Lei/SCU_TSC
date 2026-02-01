#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GRPO训练脚本

使用unsloth和TRL的GRPOTrainer对SFT模型进行强化学习微调，
训练模型优化交通信号控制决策。

用法:
    python grpo/training.py
    python grpo/training.py --config config/grpo_config.yaml
    python grpo/training.py --config config/grpo_config.yaml --output-dir ./my_model
"""

import os
import sys
import json
import argparse
from typing import Optional, List, Dict, Any

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            all_data.extend(data)

    print(f"总共加载了 {len(all_data)} 条GRPO数据")

    # 转换为TRL GRPOTrainer期望的格式
    # GRPOTrainer期望的数据格式：
    # - prompt: messages格式或字符串
    # - 其他可选字段
    grpo_data = []
    for item in all_data:
        # 获取prompt字符串
        prompt = item.get("prompt", "")

        # 转换为messages格式: [{"role": "user", "content": SYSTEM_PROMPT + prompt}]
        # 这里先使用字符串格式，GRPOTrainer会自动处理
        grpo_data.append({
            "prompt": prompt,
            "id": item.get("id", ""),
            "scenario": item.get("scenario", ""),
            "junction_id": item.get("junction_id", ""),
            # 暂时不包含expert_decision，因为GRPO需要通过reward函数评估
        })

    dataset = Dataset.from_list(grpo_data)
    print(f"转换为GRPO格式: {len(dataset)} 条数据")

    return dataset


def reward_function_placeholder(prompts: List[str], outputs: List[str], **kwargs) -> List[float]:
    """
    Reward函数占位符

    在01-02和01-03中实现具体的reward逻辑：
    - 01-02: 格式检查reward（JSON格式、extend字段）
    - 01-03: TSC reward（SUMO仿真评估排队车辆数）

    当前占位符返回固定值0.0，便于框架测试。

    Args:
        prompts: prompt列表
        outputs: 模型生成的response列表
        **kwargs: 其他参数

    Returns:
        reward_scores: reward分数列表
    """
    print("警告: 使用占位符reward函数（返回固定0.0）")
    print("      在01-02和01-03中将实现具体reward逻辑")

    # 返回固定值
    return [0.0] * len(outputs)


def train_grpo(config):
    """
    执行GRPO训练

    Args:
        config: GRPOTrainingConfig配置对象
    """
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
    print("=" * 60)

    # 导入依赖
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

    # 配置GRPO训练参数
    print("正在配置GRPO训练参数...")

    # 创建TRL的GRPOConfig（注意区别于我们自己的GRPOTrainingConfig）
    grpo_config = GRPOConfig(
        # 模型和生成参数
        model_name=config.model_path,
        learning_rate=config.learning_rate,
        batch_size=config.batch_size,
        gradient_accumulation_steps=config.gradient_accumulation_steps,

        # GRPO特定参数
        num_generations=config.num_generations,
        temperature=config.temperature,
        max_new_tokens=config.max_new_tokens,
        top_p=config.top_p,
        repetition_penalty=config.repetition_penalty,

        # KL散度控制
        kl_coeff=config.kl_coeff,

        # 训练参数
        num_train_epochs=config.num_train_epochs,
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
    )

    # 设置wandb run名称
    if config.use_wandb and config.wandb_run_name:
        import wandb
        wandb.init(project=config.wandb_project, name=config.wandb_run_name)

    # 创建GRPO训练器
    print("\n正在创建GRPO训练器...")
    trainer = GRPOTrainer(
        model=model,
        reward_funcs=reward_function_placeholder,
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
        default="/home/samuel/SCU_TSC/config/grpo_config.yaml",
        help="GRPO训练配置文件路径（YAML格式）"
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

    # 加载配置文件
    from grpo.config import GRPOTrainingConfig

    config = GRPOTrainingConfig.from_yaml(args.config)

    # 命令行参数覆盖配置文件
    if args.model_path:
        config.model_path = args.model_path
    if args.dataset_path:
        config.dataset_path = args.dataset_path
    if args.output_dir:
        config.output_dir = args.output_dir
    if args.learning_rate:
        config.learning_rate = args.learning_rate
    if args.batch_size:
        config.batch_size = args.batch_size
    if args.num_epochs:
        config.num_train_epochs = args.num_epochs

    # 执行训练
    train_grpo(config)


if __name__ == "__main__":
    main()
