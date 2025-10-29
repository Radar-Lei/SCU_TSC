import os
import sys
import torch
from peft import PeftModel
from transformers import AutoTokenizer

# 设置环境变量
os.environ["HF_HOME"] = 'model'
os.environ["MODELSCOPE_CACHE"] = 'model'

from unsloth import FastLanguageModel

# ============ 配置参数 ============
BASE_MODEL = "unsloth/Qwen3-4B-Instruct-2507"
LORA_PATH = "tsc_grpo_saved_lora"
HF_REPO_ID = "DavidRay93/Qwen3-4B-TSC-GRPO-Test"
HF_TOKEN = ""  # 替换为你的 HF token
TEMP_LOCATION = "/root/autodl-tmp/saved_models"
MAX_SEQ_LENGTH = 1024
LORA_RANK = 32

print("="*60)
print("开始加载微调模型...")
print("="*60)

# ============ 第一步：加载基础模型 ============
print("\n[步骤1] 加载基础模型...")
try:
    base_model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=BASE_MODEL,
        max_seq_length=MAX_SEQ_LENGTH,
        load_in_4bit=False,
        fast_inference=True,
        max_lora_rank=LORA_RANK,
        gpu_memory_utilization=0.9,
    )
    print("✓ 基础模型加载成功")
except Exception as e:
    print(f"✗ 基础模型加载失败: {e}")
    sys.exit(1)

# ============ 第二步：加载 LoRA 权重 ============
print("\n[步骤2] 加载 LoRA 权重...")
try:
    peft_model = PeftModel.from_pretrained(
        base_model,
        LORA_PATH,
        is_trainable=False
    )
    print("✓ LoRA 权重加载成功")
except Exception as e:
    print(f"✗ LoRA 权重加载失败: {e}")
    sys.exit(1)

# ============ 第三步：合并权重 ============
print("\n[步骤3] 合并 LoRA 权重到基础模型...")
try:
    merged_model = peft_model.merge_and_unload()
    print("✓ 权重合并成功")
except Exception as e:
    print(f"✗ 权重合并失败: {e}")
    sys.exit(1)

# ============ 第四步：为推理优化模型 ============
print("\n[步骤4] 为推理优化模型...")
try:
    merged_model = FastLanguageModel.for_inference(merged_model)
    print("✓ 推理优化完成")
except Exception as e:
    print(f"✗ 推理优化失败: {e}")
    sys.exit(1)

# ============ 第五步：发布模型到 Hub ============
print("\n[步骤5] 发布模型到 Hugging Face Hub...")
try:
    # 创建临时文件夹
    os.makedirs(TEMP_LOCATION, exist_ok=True)
    
    print(f"  - 正在转换为 GGUF 格式...")
    print(f"  - 目标 Repo: {HF_REPO_ID}")
    print(f"  - 量化方法: f16")
    
    merged_model.push_to_hub_gguf(
        HF_REPO_ID,
        tokenizer,
        quantization_method=["f16"],
        token=HF_TOKEN,
        temporary_location=TEMP_LOCATION,
    )
    print("✓ 模型发布成功！")
    
except Exception as e:
    print(f"✗ 模型发布失败: {e}")
    print("\n错误排查提示:")
    print("  1. 检查 HF_TOKEN 是否正确")
    print("  2. 检查网络连接")
    print("  3. 确保有足够的磁盘空间在临时位置")
    sys.exit(1)

# ============ 完成 ============
print("\n" + "="*60)
print("✓ 所有步骤完成！")
print("="*60)
print(f"\n模型已成功发布到: https://huggingface.co/{HF_REPO_ID}")
print("\n使用示例:")
print("```python")
print("from transformers import AutoModelForCausalLM, AutoTokenizer")
print(f"model = AutoModelForCausalLM.from_pretrained('{HF_REPO_ID}')")
print(f"tokenizer = AutoTokenizer.from_pretrained('{HF_REPO_ID}')")
print("```")


"""
screen
source .venv/bin/activate
xray-start
source /etc/xray_proxy
python upload_model_to_hub.py > upload_model_to_hub.log 2>&1
"""