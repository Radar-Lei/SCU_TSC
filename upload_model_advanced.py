#!/usr/bin/env python3
"""
高级模型发布脚本 - 支持多种配置方式和推理测试
"""

import os
import sys
import argparse
import json
from pathlib import Path
from peft import PeftModel
from transformers import AutoTokenizer

os.environ["HF_HOME"] = 'model'
os.environ["MODELSCOPE_CACHE"] = 'model'

from unsloth import FastLanguageModel
import torch

class ModelUploader:
    def __init__(self, config_path=None):
        """初始化上传器"""
        self.config = self._load_config(config_path) if config_path else self._default_config()
        self.model = None
        self.tokenizer = None
        self.merged_model = None
        
    def _default_config(self):
        """默认配置"""
        return {
            "base_model": "unsloth/Qwen3-4B-Instruct-2507",
            "lora_path": "tsc_grpo_saved_lora",
            "hf_repo_id": "DavidRay93/Qwen3-4B-TSC-GRPO-Test",
            "hf_token": os.getenv("HF_TOKEN", "YOUR_HUGGINGFACE_TOKEN_HERE"),
            "temp_location": "/root/autodl-tmp/saved_models",
            "max_seq_length": 1024,
            "lora_rank": 32,
            "quantization_method": ["f16", "q8_0"],
            "gpu_memory_utilization": 0.9,
        }
    
    def _load_config(self, config_path):
        """从 JSON 文件加载配置"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"✓ 从 {config_path} 加载配置")
            return {**self._default_config(), **config}
        except Exception as e:
            print(f"✗ 加载配置文件失败: {e}")
            return self._default_config()
    
    def validate_paths(self):
        """验证必要的路径"""
        print("\n[验证] 检查必要文件...")
        
        if not Path(self.config["lora_path"]).exists():
            print(f"✗ LoRA 路径不存在: {self.config['lora_path']}")
            return False
        
        print(f"✓ LoRA 路径存在: {self.config['lora_path']}")
        
        if self.config["hf_token"] == "YOUR_HUGGINGFACE_TOKEN_HERE":
            print("⚠️  警告: 请在配置中设置 HF_TOKEN")
            return False
        
        print("✓ HF_TOKEN 已设置")
        return True
    
    def load_base_model(self):
        """加载基础模型"""
        print("\n[步骤1] 加载基础模型...")
        try:
            self.model, self.tokenizer = FastLanguageModel.from_pretrained(
                model_name=self.config["base_model"],
                max_seq_length=self.config["max_seq_length"],
                load_in_4bit=False,
                fast_inference=True,
                max_lora_rank=self.config["lora_rank"],
                gpu_memory_utilization=self.config["gpu_memory_utilization"],
            )
            print("✓ 基础模型加载成功")
            return True
        except Exception as e:
            print(f"✗ 基础模型加载失败: {e}")
            return False
    
    def load_lora_weights(self):
        """加载 LoRA 权重"""
        print("\n[步骤2] 加载 LoRA 权重...")
        try:
            peft_model = PeftModel.from_pretrained(
                self.model,
                self.config["lora_path"],
                is_trainable=False
            )
            print("✓ LoRA 权重加载成功")
            return peft_model
        except Exception as e:
            print(f"✗ LoRA 权重加载失败: {e}")
            return None
    
    def merge_weights(self, peft_model):
        """合并权重"""
        print("\n[步骤3] 合并 LoRA 权重到基础模型...")
        try:
            self.merged_model = peft_model.merge_and_unload()
            print("✓ 权重合并成功")
            return True
        except Exception as e:
            print(f"✗ 权重合并失败: {e}")
            return False
    
    def optimize_for_inference(self):
        """优化推理"""
        print("\n[步骤4] 为推理优化模型...")
        try:
            self.merged_model = FastLanguageModel.for_inference(self.merged_model)
            print("✓ 推理优化完成")
            return True
        except Exception as e:
            print(f"✗ 推理优化失败: {e}")
            return False
    
    def test_inference(self, test_prompts=None):
        """测试推理能力"""
        if test_prompts is None:
            test_prompts = [
                "你是一位交通管理专家。根据给定的交通场景，预测下一个信号相位。\n当前场景：主干道车流密集，侧道车流稀少\n下一个信号相位是：",
            ]
        
        print("\n[可选] 测试推理能力...")
        try:
            FastLanguageModel.for_inference(self.merged_model)
            
            for i, prompt in enumerate(test_prompts, 1):
                print(f"\n测试 {i}: {prompt[:50]}...")
                
                inputs = self.tokenizer(
                    prompt,
                    return_tensors="pt",
                    padding=True,
                ).to(self.merged_model.device)
                
                with torch.no_grad():
                    outputs = self.merged_model.generate(
                        input_ids=inputs["input_ids"],
                        max_new_tokens=64,
                        temperature=0.7,
                        do_sample=True,
                        pad_token_id=self.tokenizer.pad_token_id,
                    )
                
                response = self.tokenizer.decode(
                    outputs[0][inputs["input_ids"].shape[1]:],
                    skip_special_tokens=True
                )
                print(f"回答: {response}")
                
            print("\n✓ 推理测试完成")
            return True
        except Exception as e:
            print(f"✗ 推理测试失败: {e}")
            return False
    
    def upload_to_hub(self):
        """上传到 Hub"""
        print("\n[步骤5] 发布模型到 Hugging Face Hub...")
        try:
            os.makedirs(self.config["temp_location"], exist_ok=True)
            
            print(f"  - 目标 Repo: {self.config['hf_repo_id']}")
            print(f"  - 量化方法: {', '.join(self.config['quantization_method'])}")
            print(f"  - 临时位置: {self.config['temp_location']}")
            
            self.merged_model.push_to_hub_gguf(
                self.config["hf_repo_id"],
                self.tokenizer,
                quantization_method=self.config["quantization_method"],
                token=self.config["hf_token"],
                temporary_location=self.config["temp_location"],
            )
            print("✓ 模型发布成功！")
            return True
        except Exception as e:
            print(f"✗ 模型发布失败: {e}")
            print("\n错误排查:")
            print("  1. 检查 HF_TOKEN 是否正确")
            print("  2. 检查网络连接")
            print("  3. 确保有足够的磁盘空间")
            return False
    
    def run(self, test=False, upload=True):
        """执行完整流程"""
        print("=" * 70)
        print("Qwen3-4B TSC GRPO 模型发布工具")
        print("=" * 70)
        
        # 验证路径
        if not self.validate_paths():
            return False
        
        # 加载模型
        if not self.load_base_model():
            return False
        
        # 加载 LoRA
        peft_model = self.load_lora_weights()
        if peft_model is None:
            return False
        
        # 合并权重
        if not self.merge_weights(peft_model):
            return False
        
        # 优化推理
        if not self.optimize_for_inference():
            return False
        
        # 可选：测试推理
        if test:
            self.test_inference()
        
        # 发布到 Hub
        if upload:
            if not self.upload_to_hub():
                return False
        
        # 完成
        print("\n" + "=" * 70)
        print("✓ 所有步骤完成！")
        print("=" * 70)
        print(f"\n模型已发布到: https://huggingface.co/{self.config['hf_repo_id']}")
        print("\n快速开始:")
        print("```python")
        print("from transformers import AutoModelForCausalLM, AutoTokenizer")
        print(f"model = AutoModelForCausalLM.from_pretrained('{self.config['hf_repo_id']}')")
        print(f"tokenizer = AutoTokenizer.from_pretrained('{self.config['hf_repo_id']}')")
        print("```")
        return True


def create_config_template():
    """创建配置文件模板"""
    template = {
        "base_model": "unsloth/Qwen3-4B-Instruct-2507",
        "lora_path": "tsc_grpo_saved_lora",
        "hf_repo_id": "your_username/Qwen3-4B-TSC-GRPO",
        "hf_token": "hf_your_token_here",
        "temp_location": "/root/autodl-tmp/saved_models",
        "max_seq_length": 1024,
        "lora_rank": 32,
        "quantization_method": ["f16", "q8_0"],
        "gpu_memory_utilization": 0.9,
    }
    
    config_path = "upload_config.json"
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(template, f, indent=2, ensure_ascii=False)
    
    print(f"✓ 配置模板已创建: {config_path}")
    print("  请编辑文件并填入实际的值后运行脚本")


def main():
    parser = argparse.ArgumentParser(
        description="Qwen3-4B TSC GRPO 模型发布工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 使用默认配置
  python upload_model_advanced.py --hf-token YOUR_TOKEN

  # 使用配置文件
  python upload_model_advanced.py --config upload_config.json

  # 测试推理（不上传）
  python upload_model_advanced.py --hf-token YOUR_TOKEN --test --no-upload

  # 生成配置模板
  python upload_model_advanced.py --create-config
        """
    )
    
    parser.add_argument(
        "--config",
        type=str,
        help="配置文件路径 (JSON 格式)"
    )
    parser.add_argument(
        "--hf-token",
        type=str,
        help="Hugging Face Token"
    )
    parser.add_argument(
        "--hf-repo-id",
        type=str,
        help="目标 Repo ID (format: username/repo-name)"
    )
    parser.add_argument(
        "--lora-path",
        type=str,
        help="LoRA 权重路径"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="执行推理测试"
    )
    parser.add_argument(
        "--no-upload",
        action="store_true",
        help="不上传到 Hub（仅测试推理）"
    )
    parser.add_argument(
        "--create-config",
        action="store_true",
        help="创建配置文件模板"
    )
    
    args = parser.parse_args()
    
    # 处理特殊命令
    if args.create_config:
        create_config_template()
        return 0
    
    # 初始化上传器
    uploader = ModelUploader(config_path=args.config)
    
    # 覆盖命令行参数
    if args.hf_token:
        uploader.config["hf_token"] = args.hf_token
    if args.hf_repo_id:
        uploader.config["hf_repo_id"] = args.hf_repo_id
    if args.lora_path:
        uploader.config["lora_path"] = args.lora_path
    
    # 执行
    upload = not args.no_upload
    success = uploader.run(test=args.test, upload=upload)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())





