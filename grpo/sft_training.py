#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SFT训练脚本

使用unsloth对Qwen2.5-0.5B-Instruct进行LoRA微调，
训练模型输出正确的JSON格式 {"extend": "yes/no"}。

用法:
    python -m grpo.sft_training
    python -m grpo.sft_training --max-steps 100 --output-dir ./my_model
"""

import os
import sys
import json
import argparse
from typing import Optional

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_sft_dataset(dataset_path: str):
    """
    加载SFT数据集
    
    Args:
        dataset_path: 数据集JSON或JSONL文件路径
        
    Returns:
        HuggingFace Dataset对象
    """
    from datasets import Dataset
    
    # 读取数据
    if dataset_path.endswith('.jsonl'):
        with open(dataset_path, 'r', encoding='utf-8') as f:
            data = [json.loads(line) for line in f]
    else:
        with open(dataset_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    
    # 转换为Dataset格式
    dataset = Dataset.from_list(data)
    print(f"加载了 {len(dataset)} 条SFT数据")
    
    return dataset


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
    model_name: str = "unsloth/Qwen2.5-0.5B-Instruct",
    dataset_path: str = "/home/samuel/SCU_TSC/data/sft_datasets/sft_dataset.json",
    output_dir: str = "/home/samuel/SCU_TSC/model/sft_model",
    max_seq_length: int = 2048,
    lora_rank: int = 32,
    num_epochs: int = 3,
    batch_size: int = 2,
    learning_rate: float = 2e-4,
    max_steps: Optional[int] = None,
    logging_steps: int = 5,
    save_steps: int = 50,
):
    """
    执行SFT训练
    
    Args:
        model_name: 基础模型路径
        dataset_path: SFT数据集路径
        output_dir: 模型输出目录
        max_seq_length: 最大序列长度
        lora_rank: LoRA秩
        num_epochs: 训练轮数
        batch_size: 批次大小
        learning_rate: 学习率
        max_steps: 最大训练步数（可选，用于调试）
        logging_steps: 日志记录间隔
        save_steps: 模型保存间隔
    """
    print("=" * 60)
    print("SFT训练")
    print("=" * 60)
    print(f"基础模型: {model_name}")
    print(f"数据集: {dataset_path}")
    print(f"输出目录: {output_dir}")
    print(f"LoRA秩: {lora_rank}")
    print(f"训练轮数: {num_epochs}")
    print(f"批次大小: {batch_size}")
    print(f"学习率: {learning_rate}")
    print(f"最大步数: {max_steps or '无限制'}")
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
    dataset = load_sft_dataset(dataset_path)
    
    # 格式化数据
    print("正在格式化数据...")
    dataset = dataset.map(
        lambda x: format_for_training(x, tokenizer),
        remove_columns=dataset.column_names
    )
    
    # 配置训练参数
    training_args = SFTConfig(
        output_dir=output_dir,
        dataset_text_field="text",
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=4,
        warmup_steps=5,
        num_train_epochs=num_epochs,
        max_steps=max_steps if max_steps else -1,
        learning_rate=learning_rate,
        logging_steps=logging_steps,
        save_steps=save_steps,
        optim="adamw_8bit",
        weight_decay=0.001,
        lr_scheduler_type="linear",
        seed=3407,
        report_to="none",
        save_total_limit=2,
    )
    
    # 创建训练器
    print("\n正在创建训练器...")
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset,
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
    
    return parser.parse_args()


def main():
    args = parse_args()
    
    train_sft(
        model_name=args.model_name,
        dataset_path=args.dataset,
        output_dir=args.output_dir,
        max_seq_length=args.max_seq_length,
        lora_rank=args.lora_rank,
        num_epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        max_steps=args.max_steps,
        logging_steps=args.logging_steps,
        save_steps=args.save_steps,
    )


if __name__ == "__main__":
    main()
