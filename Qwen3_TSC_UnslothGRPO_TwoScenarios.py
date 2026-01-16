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
# ======================================================================

# %%
from generate_grpo_dataset import main as generate_main, CONFIG

DATASET_PATH = "grpo_dataset_two_scenarios"

if not os.path.isdir(DATASET_PATH):
    print(f"⚠️ Dataset 不存在: {DATASET_PATH}")
    print("开始生成 dataset...")

    CONFIG.update({
        "output_dir": DATASET_PATH,
        "state_dir": "grpo_states_two_scenarios",
        "dataset_mode": "two_scenarios",
        "steps_per_tl_signal_step": 10,
        "steps_per_tl_extend_decision": 10,
        "decision_lead_sec": 10,
        "phase_duration_scale_range": (0.7, 1.3),
        "extend_min_green_range": (5, 20),
        "extend_max_green_range": (25, 120),
        "extend_wait_time_range": (5, 25),
        "num_workers": 16,
    })

    print("当前配置:")
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


resume_from = CHECKPOINT_DIR if _looks_like_checkpoint(CHECKPOINT_DIR) else BASE_MODEL_DIR
if resume_from == CHECKPOINT_DIR:
    print(f"✓ 从 checkpoint 继续训练: {CHECKPOINT_DIR}")
else:
    print(f"ℹ 从基础模型开始: {BASE_MODEL_DIR}")

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=resume_from,
    max_seq_length=max_seq_length,
    load_in_4bit=False,
    fast_inference=False,
    max_lora_rank=lora_rank,
    gpu_memory_utilization=0.8,
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
print(dataset[0])

# ======================================================================
# ## 4. 导入 Reward Function
# ======================================================================

# %%
from tsc_reward_function import tsc_reward_fn, cleanup_global_pool

print("✓ Reward function 加载成功")

# ======================================================================
# ## 5. 配置 GRPOTrainer
# ======================================================================

# %%
from trl import GRPOConfig, GRPOTrainer

config = GRPOConfig(
    output_dir="checkpoints/grpo_tsc_two_scenarios",

    # 批次配置
    per_device_train_batch_size=1,
    num_generations=4,
    gradient_accumulation_steps=4,

    # 生成配置
    max_completion_length=128,  
    temperature=0.8,  
    top_p=0.95,  # 从0.95降到0.9
    top_k=50,  # 从50降到30

    # 训练配置
    learning_rate=2e-6,
    num_train_epochs=1,
    max_steps=-1,

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

print("✓ GRPOConfig 配置完成")

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

