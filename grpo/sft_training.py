#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SFT训练脚本

使用unsloth对Qwen2.5-0.5B-Instruct进行LoRA微调，
训练模型输出正确的JSON格式 {"extend": "yes/no"}。

用法:
    python -m grpo.sft_training
    python -m grpo.sft_training --config config/training_config.yaml
    python -m grpo.sft_training --max-steps 100 --output-dir ./my_model
"""

import os
import sys
import json
import argparse
from typing import Optional

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_sft_dataset(dataset_path: str, eval_percent: float = 0.05, eval_limit: int = 100):
    """
    加载SFT数据集
    
    Args:
        dataset_path: 数据集JSON或JSONL文件路径
        eval_percent: 验证集比例 (默认 0.05 = 5%)
        eval_limit: 验证集最大数量 (默认 100)
        
    Returns:
        train_dataset: 训练集 HuggingFace Dataset 对象
        eval_dataset: 验证集 HuggingFace Dataset 对象 (可能为 None)
    """
    from datasets import Dataset
    
    if dataset_path.endswith('.jsonl'):
        with open(dataset_path, 'r', encoding='utf-8') as f:
            data = [json.loads(line) for line in f]
    else:
        with open(dataset_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    
    dataset = Dataset.from_list(data)
    print(f"加载了 {len(dataset)} 条SFT数据")
    
    if eval_percent <= 0 or eval_percent >= 1:
        return dataset, None
    
    eval_count = max(1, min(int(len(dataset) * eval_percent), eval_limit))
    train_count = len(dataset) - eval_count
    
    if eval_count < 1:
        return dataset, None
    
    train_data = dataset.select(range(train_count))
    eval_data = dataset.select(range(train_count, len(dataset)))
    
    print(f"划分训练集: {len(train_data)} 条, 验证集: {len(eval_data)} 条")
    
    return train_data, eval_data


def format_for_training(example, tokenizer):
    """
    将对话格式转换为训练文本
    """
    text = tokenizer.apply_chat_template(
        example["messages"],
        tokenize=False,
        add_generation_prompt=False
    )
    return {"text": text}


def train_sft(
    config=None,
    model_name: str = "unsloth/Qwen2.5-0.5B-Instruct",
    dataset_path: str = "/home/samuel/SCU_TSC/data/sft_datasets/sft_dataset.json",
    output_dir: str = "/home/samuel/SCU_TSC/model/sft_model",
    max_seq_length: int = 2048,
    lora_rank: int = 32,
    num_epochs: int = 3,
    batch_size: int = 2,
    gradient_accumulation_steps: int = 4,
    learning_rate: float = 2e-4,
    max_steps: Optional[int] = None,
    logging_steps: int = 5,
    save_steps: int = 50,
    eval_percent: float = 0.05,
    eval_limit: int = 100,
    eval_steps: int = 30,
    warmup_steps: int = 5,
    optim: str = "adamw_8bit",
    weight_decay: float = 0.001,
    lr_scheduler_type: str = "linear",
    seed: int = 3407,
):
    """
    执行SFT训练

    Args:
        config: TrainingConfig配置对象（可选，从training_config.yaml加载）
        model_name: 基础模型路径
        dataset_path: SFT数据集路径
        output_dir: 模型输出目录
        max_seq_length: 最大序列长度
        lora_rank: LoRA秩
        num_epochs: 训练轮数
        batch_size: 批次大小
        gradient_accumulation_steps: 梯度累积步数
        learning_rate: 学习率
        max_steps: 最大训练步数（可选，用于调试）
        logging_steps: 日志记录间隔
        save_steps: 模型保存间隔
        eval_percent: 验证集比例 (默认 0.05 = 5%)
        eval_limit: 验证集最大数量 (默认 100)
        eval_steps: 评估步数间隔 (默认 30)
        warmup_steps: 预热步数
        optim: 优化器
        weight_decay: 权重衰减
        lr_scheduler_type: 学习率调度器类型
        seed: 随机种子
    """
    # 如果提供了config，使用config.sft中的值作为默认值
    if config is not None:
        sft_config = config.sft
        # 只使用参数为None或默认值时，才从config中获取
        if model_name == "unsloth/Qwen2.5-0.5B-Instruct":
            model_name = sft_config.model_name
        if max_seq_length == 2048:
            max_seq_length = sft_config.max_seq_length
        if lora_rank == 32:
            lora_rank = sft_config.lora_rank
        if num_epochs == 3:
            num_epochs = sft_config.num_epochs
        if batch_size == 2:
            batch_size = sft_config.batch_size
        if gradient_accumulation_steps == 4:
            gradient_accumulation_steps = sft_config.gradient_accumulation_steps
        if learning_rate == 2e-4:
            learning_rate = sft_config.learning_rate
        if logging_steps == 5:
            logging_steps = sft_config.logging_steps
        if save_steps == 50:
            save_steps = sft_config.save_steps
        if eval_percent == 0.05:
            eval_percent = sft_config.eval_percent
        if eval_limit == 100:
            eval_limit = sft_config.eval_limit
        if eval_steps == 30:
            eval_steps = sft_config.eval_steps
        if warmup_steps == 5:
            warmup_steps = sft_config.warmup_steps
        if optim == "adamw_8bit":
            optim = sft_config.optim
        if weight_decay == 0.001:
            weight_decay = sft_config.weight_decay
        if lr_scheduler_type == "linear":
            lr_scheduler_type = sft_config.lr_scheduler_type
        if seed == 3407:
            seed = sft_config.seed

    print("=" * 60)
    print("SFT训练")
    print("=" * 60)
    print(f"基础模型: {model_name}")
    print(f"数据集: {dataset_path}")
    print(f"输出目录: {output_dir}")
    print(f"LoRA秩: {lora_rank}")
    print(f"训练轮数: {num_epochs}")
    print(f"批次大小: {batch_size}")
    print(f"梯度累积步数: {gradient_accumulation_steps}")
    print(f"学习率: {learning_rate}")
    print(f"最大步数: {max_steps or '无限制'}")
    print(f"验证集比例: {eval_percent * 100}% (上限 {eval_limit} 条)")
    print(f"评估间隔: {eval_steps} 步")
    print(f"预热步数: {warmup_steps}")
    print(f"优化器: {optim}")
    print(f"权重衰减: {weight_decay}")
    print(f"学习率调度器: {lr_scheduler_type}")
    print(f"随机种子: {seed}")
    print("=" * 60)
    
    # 导入依赖
    from unsloth import FastLanguageModel
    from trl import SFTTrainer, SFTConfig
    import torch
    
    # 加载模型
    print("\n正在加载模型...")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=model_name,
        max_seq_length=max_seq_length,
        load_in_4bit=False,  # 使用16bit训练
        dtype=None,  # 自动检测
    )
    
    # 添加LoRA适配器
    print("正在配置LoRA...")
    model = FastLanguageModel.get_peft_model(
        model,
        r=lora_rank,
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj",
        ],
        lora_alpha=lora_rank * 2,
        use_gradient_checkpointing="unsloth",
        random_state=3407,
    )
    
    # 加载数据集
    print("\n正在加载数据集...")
    train_dataset, eval_dataset = load_sft_dataset(dataset_path, eval_percent, eval_limit)
    
    # 格式化训练数据
    print("正在格式化训练数据...")
    train_dataset = train_dataset.map(
        lambda x: format_for_training(x, tokenizer),
        remove_columns=train_dataset.column_names
    )
    
    # 格式化验证数据（如果有）
    if eval_dataset is not None:
        print("正在格式化验证数据...")
        eval_dataset = eval_dataset.map(
            lambda x: format_for_training(x, tokenizer),
            remove_columns=eval_dataset.column_names
        )
    
    # 配置训练参数
    training_args = SFTConfig(
        output_dir=output_dir,
        dataset_text_field="text",
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=gradient_accumulation_steps,
        warmup_steps=warmup_steps,
        num_train_epochs=num_epochs,
        max_steps=max_steps if max_steps else -1,
        learning_rate=learning_rate,
        logging_steps=logging_steps,
        eval_strategy="steps" if eval_dataset is not None else "no",
        eval_steps=eval_steps,
        save_steps=save_steps,
        optim=optim,
        weight_decay=weight_decay,
        lr_scheduler_type=lr_scheduler_type,
        seed=seed,
        report_to="none",
        save_total_limit=2,
    )
    
    # 创建训练器
    print("\n正在创建训练器...")
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        args=training_args,
    )
    
    # 开始训练
    print("\n开始训练...")
    trainer.train()
    
    # 保存模型
    print(f"\n正在保存模型到 {output_dir}...")
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    # 同时保存merged模型（用于推理）
    merged_dir = os.path.join(output_dir, "merged")
    print(f"正在保存合并后的模型到 {merged_dir}...")
    model.save_pretrained_merged(merged_dir, tokenizer, save_method="merged_16bit")
    
    print("\nSFT训练完成!")
    print(f"LoRA模型: {output_dir}")
    print(f"合并模型: {merged_dir}")
    
    return model, tokenizer


def parse_args():
    parser = argparse.ArgumentParser(
        description="SFT训练脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # 配置文件参数
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="中央训练配置文件路径（training_config.yaml）"
    )

    parser.add_argument(
        "--model-name",
        type=str,
        default="unsloth/Qwen2.5-0.5B-Instruct",
        help="基础模型路径或HuggingFace模型ID"
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default="/home/samuel/SCU_TSC/data/sft_datasets/sft_dataset.json",
        help="SFT数据集路径"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="/home/samuel/SCU_TSC/model/sft_model",
        help="模型输出目录"
    )
    parser.add_argument(
        "--max-seq-length",
        type=int,
        default=2048,
        help="最大序列长度"
    )
    parser.add_argument(
        "--lora-rank",
        type=int,
        default=32,
        help="LoRA秩"
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=3,
        help="训练轮数"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=2,
        help="批次大小"
    )
    parser.add_argument(
        "--gradient-accumulation-steps",
        type=int,
        default=4,
        help="梯度累积步数"
    )
    parser.add_argument(
        "--learning-rate",
        type=float,
        default=2e-4,
        help="学习率"
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=None,
        help="最大训练步数（用于调试）"
    )
    parser.add_argument(
        "--logging-steps",
        type=int,
        default=5,
        help="日志记录间隔"
    )
    parser.add_argument(
        "--save-steps",
        type=int,
        default=50,
        help="模型保存间隔"
    )
    parser.add_argument(
        "--eval-percent",
        type=float,
        default=0.05,
        help="验证集比例 (默认 0.05 = 5%)"
    )
    parser.add_argument(
        "--eval-limit",
        type=int,
        default=100,
        help="验证集最大数量 (默认 100)"
    )
    parser.add_argument(
        "--eval-steps",
        type=int,
        default=30,
        help="评估步数间隔 (默认 30)"
    )
    parser.add_argument(
        "--warmup-steps",
        type=int,
        default=5,
        help="预热步数"
    )
    parser.add_argument(
        "--optim",
        type=str,
        default="adamw_8bit",
        help="优化器"
    )
    parser.add_argument(
        "--weight-decay",
        type=float,
        default=0.001,
        help="权重衰减"
    )
    parser.add_argument(
        "--lr-scheduler-type",
        type=str,
        default="linear",
        help="学习率调度器类型"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=3407,
        help="随机种子"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    # 加载配置文件（如果提供）
    config = None
    if args.config:
        from grpo.config import load_training_config
        config = load_training_config(args.config)
        print(f"已加载配置文件: {args.config}")

    # 执行训练（config作为可选参数传入）
    train_sft(
        config=config,
        model_name=args.model_name,
        dataset_path=args.dataset,
        output_dir=args.output_dir,
        max_seq_length=args.max_seq_length,
        lora_rank=args.lora_rank,
        num_epochs=args.epochs,
        batch_size=args.batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        learning_rate=args.learning_rate,
        max_steps=args.max_steps,
        logging_steps=args.logging_steps,
        save_steps=args.save_steps,
        eval_percent=args.eval_percent,
        eval_limit=args.eval_limit,
        eval_steps=args.eval_steps,
        warmup_steps=args.warmup_steps,
        optim=args.optim,
        weight_decay=args.weight_decay,
        lr_scheduler_type=args.lr_scheduler_type,
        seed=args.seed,
    )


if __name__ == "__main__":
    main()
