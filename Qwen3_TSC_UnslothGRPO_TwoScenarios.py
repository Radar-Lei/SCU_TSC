# -*- coding: utf-8 -*-
# 从 Qwen3_TSC_UnslothGRPO_TwoScenarios.ipynb 自动转换

# ======================================================================
# # TSC 标准 Unsloth GRPO 训练（两大场景）
# 
# 使用标准 Unsloth GRPOTrainer + 离线 Dataset + Reward Function 回溯 SUMO 评估
# ======================================================================

# ======================================================================
# ## 1. 环境配置
# ======================================================================

# %%
import os
import sys

os.environ["UNSLOTH_USE_MODELSCOPE"] = "1"

print("环境变量已设置")

# ======================================================================
# ## 1.5 生成/检查 Dataset（可选）
# 
# 如果 dataset 不存在，此 cell 会自动生成；如果已存在，则跳过。
# 
# 快速验证模式配置（验证改动是否生效）：
#   - steps_per_tl_signal_step: 2       # 每场景每TL的signal_step样本数（默认10）
#   - steps_per_tl_extend_decision: 2   # 每场景每TL的extend_decision样本数（默认10）
#   - max_tl_per_scenario: 2            # 每场景最多TL数（默认5）
#   - num_workers: 4                    # 并行worker数（默认16）
# 正式训练时恢复到默认值。
# ======================================================================

# %%
from generate_grpo_dataset import main as generate_main, CONFIG

DATASET_PATH = "grpo_dataset_two_scenarios"

if not os.path.isdir(DATASET_PATH):
    print(f"⚠️ Dataset 不存在: {DATASET_PATH}")
    print("开始生成 dataset...")

    # 快速验证模式：取消下面注释以使用小规模dataset
    # QUICK_VERIFY = True
    QUICK_VERIFY = False  # 正式训练设为 False

    CONFIG.update({
        "output_dir": DATASET_PATH,
        "state_dir": "grpo_states_two_scenarios",
        "dataset_mode": "two_scenarios",
        "steps_per_tl_signal_step": 100,   # 每TL生成100个signal_step样本
        "steps_per_tl_extend_decision": 100,  # 每TL生成100个extend_decision样本
        "decision_lead_sec": 10,
        "phase_duration_scale_range": (0.7, 1.3),
        "extend_min_green_range": (5, 20),
        "extend_max_green_range": (25, 120),
        "extend_wait_time_range": (5, 25),
        "max_tl_per_scenario": 10,  # 每场景最多10个TL
        "num_workers": 4 if QUICK_VERIFY else 16,
    })

    print("当前配置:")
    print(f"  - 模式: {'快速验证' if QUICK_VERIFY else '正式训练'}")
    print(f"  - warmup_steps: {CONFIG['warmup_steps']}")
    print(f"  - steps_per_tl_signal_step: {CONFIG['steps_per_tl_signal_step']}")
    print(f"  - steps_per_tl_extend_decision: {CONFIG['steps_per_tl_extend_decision']}")
    print(f"  - max_tl_per_scenario: {CONFIG['max_tl_per_scenario']}")
    print(f"  - num_workers: {CONFIG['num_workers']}")

    generate_main()
else:
    print(f"✓ Dataset 已存在: {DATASET_PATH}")

# ======================================================================
# ## 2. 加载模型
# ======================================================================

# %%
from unsloth import FastLanguageModel
import torch

max_seq_length = 2048
lora_rank = 32

os.environ["HF_HOME"] = "model"
os.environ["MODELSCOPE_CACHE"] = "model"

# BASE_MODEL_DIR = "model/models/qwen3-4B-SFT"
BASE_MODEL_DIR = "Qwen/Qwen2.5-0.5B-Instruct"
# BASE_MODEL_DIR = "rd211/Qwen3-0.6B-Instruct"
CHECKPOINT_DIR = "checkpoints/grpo_tsc_two_scenarios_latest"


def _looks_like_checkpoint(path: str) -> bool:
    if not os.path.isdir(path):
        return False
    marker_files = [
        "adapter_config.json",
        "adapter_model.safetensors",
        "adapter_model.bin",
        "config.json",
    ]
    return any(os.path.isfile(os.path.join(path, f)) for f in marker_files)



SFT_CHECKPOINT_DIR = "checkpoints/sft_tsc_synthetic"

resume_from = CHECKPOINT_DIR if _looks_like_checkpoint(CHECKPOINT_DIR) else BASE_MODEL_DIR

if _looks_like_checkpoint(CHECKPOINT_DIR):
    print(f"✓ 从 checkpoint 继续训练: {CHECKPOINT_DIR}")
    resume_from = CHECKPOINT_DIR
elif _looks_like_checkpoint(SFT_CHECKPOINT_DIR):
    print(f"✓ 从 SFT 模型开始训练: {SFT_CHECKPOINT_DIR}")
    resume_from = SFT_CHECKPOINT_DIR
else:
    print(f"ℹ 从基础模型开始: {BASE_MODEL_DIR}")
    resume_from = BASE_MODEL_DIR

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=resume_from,
    max_seq_length=max_seq_length,
    load_in_4bit=False,
    fast_inference=False,  # DGX Spark 上 vLLM 有兼容性问题，已禁用
    max_lora_rank=lora_rank,
    gpu_memory_utilization=0.6,
)

if resume_from == BASE_MODEL_DIR:
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
else:
    try:
        model.gradient_checkpointing_enable()
    except Exception:
        pass
    _trainable = [p for p in model.parameters() if p.requires_grad]
    if len(_trainable) == 0:
        for name, p in model.named_parameters():
            if "lora" in name.lower():
                p.requires_grad = True
        print("⚠️ checkpoint 未检测到可训练参数，已强制启用 LoRA 参数训练")

# Fix for GRPO generation: Must use left padding (applies to ALL cases)
tokenizer.padding_side = "left"
if tokenizer.pad_token_id is None:
    tokenizer.pad_token_id = tokenizer.eos_token_id

# Apply the same chat template as SFT training
from unsloth.chat_templates import get_chat_template
tokenizer = get_chat_template(
    tokenizer,
    chat_template="qwen-2.5",  # Must match SFT training template
)
print("✓ Applied qwen-2.5 chat template to match SFT training")

# Ensure BOS token is preserved - this is critical for generation
if tokenizer.bos_token_id is None:
    # For Qwen, <|im_start|> acts as BOS in chat context
    tokenizer.bos_token_id = tokenizer.convert_tokens_to_ids("<|im_start|>")
    print(f"设置 bos_token_id: {tokenizer.bos_token_id}")

print(f"Tokenizer padding_side: {tokenizer.padding_side}")
print(f"Tokenizer pad_token_id: {tokenizer.pad_token_id}")
print(f"Tokenizer bos_token_id: {tokenizer.bos_token_id}")

# ======================================================================
# ## 3. 加载 Dataset
# ======================================================================

# %%
from datasets import load_from_disk

DATASET_PATH = "grpo_dataset_two_scenarios"

if not os.path.isdir(DATASET_PATH):
    raise FileNotFoundError(
        f"Dataset 不存在: {DATASET_PATH}\n"
        "请先运行 generate_grpo_dataset.py 生成离线 dataset"
    )

dataset = load_from_disk(DATASET_PATH)
print(f"✓ Dataset 加载成功: {DATASET_PATH}")
print(f"样本数: {len(dataset)}")

# NOTE: Do NOT apply chat template here!
# GRPOTrainer expects prompt to be a list of messages, not a formatted string.
# It will apply the chat template internally using processing_class (tokenizer).
print("示例 Prompt (message list):")
print(dataset[0]["prompt"])

# ======================================================================
# ## 4. 导入 Reward Function
# ======================================================================

# %%
from tsc_reward_function import tsc_reward_fn, cleanup_global_pool

print("✓ Reward function 加载成功")

# ======================================================================
# ## 5. 配置 GRPOTrainer
# 
# 快速验证模式：max_steps=20（默认-1为全epoch）
# 正式训练时设回 -1
# ======================================================================

# %%
from trl import GRPOConfig, GRPOTrainer

# 快速验证模式：取消下面注释以使用短训练
# QUICK_VERIFY = True
QUICK_VERIFY = False  # 正式训练设为 False

config = GRPOConfig(
    output_dir="checkpoints/grpo_tsc_two_scenarios",

    # 批次配置
    per_device_train_batch_size=1,
    num_generations=4,  # Keep at 4 for proper GRPO
    gradient_accumulation_steps=4,

    # 生成配置
    max_completion_length=128,  
    temperature=0.7,
    top_p=0.9,
    top_k=40,
    use_vllm=False,  # DGX Spark 上 vLLM LoRA 兼容性问题，已禁用

    # 训练配置
    learning_rate=2e-6,
    num_train_epochs=1,
    max_steps=20 if QUICK_VERIFY else -1,  # 快速验证：20步；正式训练：全epoch

    # GRPO 特定
    scale_rewards=True,

    # 日志与保存
    logging_steps=5,
    save_steps=100,
    save_total_limit=3,

    # 优化器
    optim="adamw_torch",
    weight_decay=0.01,
    warmup_steps=50,

    # 其他
    bf16=True,
    report_to="none",
    remove_unused_columns=False,
)

print(f"✓ GRPOConfig 配置完成 (模式: {'快速验证' if QUICK_VERIFY else '正式训练'})")
if QUICK_VERIFY:
    print(f"  - max_steps: {config.max_steps} (验证模式)")
else:
    print(f"  - max_steps: {config.max_steps} (全epoch)")

# ======================================================================
# ## 6. 创建 GRPOTrainer 并开始训练
# ======================================================================

# %%
trainer = GRPOTrainer(
    model=model,
    processing_class=tokenizer,
    args=config,
    train_dataset=dataset,
    reward_funcs=tsc_reward_fn,
)



print("✓ GRPOTrainer 创建成功")
print(f"训练样本数: {len(dataset)}")
print(f"每 epoch steps: {len(trainer.get_train_dataloader())}")

print("\n" + "="*60)
print("开始 GRPO 训练")
print("="*60 + "\n")

trainer.train()

print("\n" + "="*60)
print("训练完成")
print("="*60)

# ======================================================================
# ## 7. 保存最终模型
# ======================================================================

# %%
final_output_dir = "checkpoints/grpo_tsc_two_scenarios_final"
trainer.save_model(final_output_dir)
tokenizer.save_pretrained(final_output_dir)
print(f"✓ 最终模型已保存到: {final_output_dir}")

# ======================================================================
# ## 8. 清理资源
# ======================================================================

# %%
cleanup_global_pool()
print("✓ Simulator 池已清理")

# ======================================================================
# ## 9. 测试推理（可选）
# ======================================================================

# %%
FastLanguageModel.for_inference(model)

test_sample = dataset[0]
test_prompt = test_sample["prompt"]

prompt_text = tokenizer.apply_chat_template(test_prompt, tokenize=False, add_generation_prompt=True)
inputs = tokenizer(prompt_text, return_tensors="pt").to(model.device)

print("测试生成:")
print("-" * 60)

outputs = model.generate(
    **inputs,
    max_new_tokens=256,
    temperature=0.7,
    top_p=0.9,
    do_sample=True,
)

generated_text = tokenizer.decode(outputs[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
print(generated_text)
print("-" * 60)

