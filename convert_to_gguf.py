#!/usr/bin/env python3
"""
将 Unsloth LoRA checkpoint 转换为 GGUF 格式。

用法:
    python convert_to_gguf.py [--checkpoint CHECKPOINT_PATH] [--output OUTPUT_DIR] [--quantization METHOD]

示例:
    python convert_to_gguf.py
    python convert_to_gguf.py --checkpoint checkpoints/grpo_tsc_two_scenarios/checkpoint-4000
    python convert_to_gguf.py --quantization q4_k_m
"""

import os
import sys
import argparse

# 确保环境变量在导入前设置
os.environ["UNSLOTH_USE_MODELSCOPE"] = "1"
os.environ["MODELSCOPE_CACHE"] = "model"
os.environ["HF_HOME"] = "model"


def main():
    parser = argparse.ArgumentParser(description="将 Unsloth LoRA checkpoint 转换为 GGUF 格式")
    parser.add_argument(
        "--checkpoint",
        type=str,
        default="checkpoints/grpo_tsc_two_scenarios/checkpoint-4000",
        help="要转换的 checkpoint 路径 (默认: checkpoints/grpo_tsc_two_scenarios/checkpoint-4000)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="GGUF 输出目录 (默认: {checkpoint}_gguf)",
    )
    parser.add_argument(
        "--quantization",
        type=str,
        default="f16",
        choices=["f16", "q4_k_m", "q5_k_m", "q8_0", "q4_0", "q5_0", "q5_1", "q8_1"],
        help="量化方法 (默认: f16)",
    )
    parser.add_argument(
        "--max_seq_length",
        type=int,
        default=2048,
        help="最大序列长度 (默认: 2048)",
    )
    args = parser.parse_args()

    checkpoint_path = args.checkpoint
    output_dir = args.output or f"{checkpoint_path}_gguf"
    quantization_method = args.quantization

    # 验证 checkpoint 存在
    if not os.path.isdir(checkpoint_path):
        print(f"❌ 错误: checkpoint 目录不存在: {checkpoint_path}")
        sys.exit(1)

    # 检查必要的文件
    weights_files = ["adapter_model.safetensors", "adapter_model.bin"]
    
    has_config = os.path.isfile(os.path.join(checkpoint_path, "adapter_config.json"))
    has_weights = any(os.path.isfile(os.path.join(checkpoint_path, f)) for f in weights_files)
    
    if not has_config or not has_weights:
        print(f"❌ 错误: 无效的 checkpoint 目录: {checkpoint_path}")
        print(f"   需要 adapter_config.json 和 adapter_model.safetensors/bin")
        sys.exit(1)

    print(f"📦 Checkpoint 路径: {checkpoint_path}")
    print(f"📁 输出目录: {output_dir}")
    print(f"🔧 量化方法: {quantization_method}")
    print()

    # 导入依赖
    print("⏳ 加载依赖...")
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import PeftModel
    import json

    # 读取 adapter_config 获取 base_model 路径
    adapter_config_path = os.path.join(checkpoint_path, "adapter_config.json")
    with open(adapter_config_path, "r") as f:
        adapter_config = json.load(f)
    
    base_model_name = adapter_config.get("base_model_name_or_path", "")
    print(f"📌 基础模型: {base_model_name}")

    # 加载基础模型
    print(f"⏳ 加载基础模型...")
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True,
    )
    tokenizer = AutoTokenizer.from_pretrained(base_model_name, trust_remote_code=True)

    # 加载 LoRA 适配器
    print(f"⏳ 加载 LoRA 适配器...")
    model = PeftModel.from_pretrained(base_model, checkpoint_path)

    # 合并 LoRA 权重
    print(f"⏳ 合并 LoRA 权重...")
    model = model.merge_and_unload()

    # 确保输出目录存在
    merged_dir = output_dir + "_merged"
    os.makedirs(merged_dir, exist_ok=True)

    # 保存合并后的模型
    print(f"⏳ 保存合并后的模型到: {merged_dir}")
    model.save_pretrained(merged_dir, safe_serialization=True)
    tokenizer.save_pretrained(merged_dir)
    print(f"✅ 合并后的模型已保存到: {merged_dir}")

    # 使用 llama.cpp 转换为 GGUF
    print()
    print(f"⏳ 正在转换为 GGUF ({quantization_method})...")
    
    # 尝试导入并使用 unsloth 的 GGUF 转换（从合并后的模型）
    try:
        from unsloth import FastLanguageModel
        
        # 重新加载合并后的模型（使用 unsloth）
        print("⏳ 使用 Unsloth 加载合并后的模型进行 GGUF 转换...")
        merged_model, merged_tokenizer = FastLanguageModel.from_pretrained(
            model_name=merged_dir,
            max_seq_length=args.max_seq_length,
            load_in_4bit=False,
            fast_inference=False,
        )
        
        os.makedirs(output_dir, exist_ok=True)
        merged_model.save_pretrained_gguf(
            output_dir,
            merged_tokenizer,
            quantization_method=quantization_method,
        )
        print(f"✅ GGUF 转换完成！")
        
    except Exception as e:
        print(f"⚠️ Unsloth GGUF 转换失败: {e}")
        print()
        print("请手动使用 llama.cpp 进行转换:")
        print(f"  1. git clone https://github.com/ggerganov/llama.cpp")
        print(f"  2. cd llama.cpp && pip install -r requirements.txt")
        print(f"  3. python convert_hf_to_gguf.py {merged_dir} --outtype {quantization_method}")
        print()
        print(f"✅ 合并后的 HuggingFace 模型已保存到: {merged_dir}")
        return

    # 列出生成的文件
    print()
    print(f"📁 输出文件:")
    for f in os.listdir(output_dir):
        filepath = os.path.join(output_dir, f)
        if os.path.isfile(filepath):
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            print(f"   - {f} ({size_mb:.2f} MB)")


if __name__ == "__main__":
    main()
