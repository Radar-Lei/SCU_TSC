# -*- coding: utf-8 -*-
# Generated from Jupyter notebook: Qwen3_TSC_UnslothGRPO_TwoScenarios.ipynb

# %% [markdown]
# # TSC 标准 Unsloth GRPO 训练（两大场景）
# 
# 使用标准 Unsloth GRPOTrainer + 离线 Dataset + Reward Function 回溯 SUMO 评估

# %% [markdown]
# ## 1. 环境配置

# %% [code] cell 1
import os
import sys

os.environ["UNSLOTH_USE_MODELSCOPE"] = "1"
os.environ["UNSLOTH_VLLM_STANDBY"] = "1"
os.environ["MODELSCOPE_CACHE"] = "model"
os.environ["HF_HOME"] = "model"
print("环境变量已设置")

# %% [markdown]
# ## 1.5 生成/检查 Dataset（可选）
# 
# 如果 dataset 不存在，此 cell 会自动生成；如果已存在，则跳过。

# %% [code] cell 2
from generate_grpo_dataset import main as generate_main, CONFIG

DATASET_PATH = "grpo_dataset_two_scenarios"
FORCE_REGEN = os.getenv("FORCE_REGEN", "").strip() == "1"

if FORCE_REGEN or not os.path.isdir(DATASET_PATH):
    if FORCE_REGEN and os.path.isdir(DATASET_PATH):
        print(f"⚠️ FORCE_REGEN=1，重新生成 dataset: {DATASET_PATH}")
    else:
        print(f"⚠️ Dataset 不存在: {DATASET_PATH}")
    print("开始生成 dataset...")

    # 快速验证模式：取消下面注释以使用小规模dataset
    # QUICK_VERIFY = True
    QUICK_VERIFY = False  # 正式训练设为 False

    CONFIG.update({
        "output_dir": DATASET_PATH,
        "state_dir": "grpo_states_two_scenarios",
        "dataset_mode": "two_scenarios",
        "steps_per_tl_signal_step": 20,   # 每TL生成10个signal_step样本
        "steps_per_tl_extend_decision": 20,  # 每TL生成100个extend_decision样本
        "decision_lead_sec": 10,
        "phase_duration_scale_range": (0.7, 1.3),
        "extend_min_green_range": (10, 45),
        "extend_max_green_range": (80, 120),
        "extend_wait_time_range": (2, 5),
        "max_extend_sec": 8,  # extend_decision 中 extend_sec 的最大值
        "max_tl_per_scenario": 10,  
        "num_workers": 16,
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

# %% [markdown]
# ## 1.8 Generate Synthetic SFT Dataset
# 
# Based on the GRPO dataset, generate synthetic responses to create an SFT dataset.

# %% [code] cell 3
import os
import json
import random
import re
from datasets import load_from_disk, Dataset

def looks_like_hf_dataset_dir(path: str, required_columns: set[str] | None = None) -> bool:
    if not os.path.isdir(path):
        return False
    try:
        names = os.listdir(path)
    except Exception:
        return False
    has_arrow = any(n.endswith(".arrow") for n in names)
    has_markers = any(n in {"state.json", "dataset_info.json"} for n in names)
    if not (has_arrow or has_markers):
        return False
    try:
        ds = load_from_disk(path)
    except Exception:
        return False
    if required_columns:
        if hasattr(ds, "column_names"):
            cols = set(ds.column_names or [])
        elif hasattr(ds, "keys"):
            first_key = next(iter(ds.keys()), None)
            cols = set(ds[first_key].column_names or []) if first_key else set()
        else:
            cols = set()
        if not required_columns.issubset(cols):
            return False
    return True

def extract_json_content(text, marker):
    pattern = f"【{marker}】(.*?)【/{marker}】"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return json.loads(match.group(1))
    return None

def generate_synthetic_response(messages):
    user_content = messages[-1]['content']
    
    # Check task type
    if "【signal_step_input_json】" in user_content:
        data = extract_json_content(user_content, "signal_step_input_json")
        if data:
            # Heuristic for signal_step
            scenario = data.get("scenario", {})
            phase_ids = scenario.get("phase_ids", [1, 3])
            
            # Simple heuristic: pick valid phase, valid time
            # Ideally pick a random one to prevent bias to one phase
            next_phase_id = random.choice(phase_ids)
            green_sec = random.randint(10, 60)
            
            return json.dumps({
                "next_phase_id": next_phase_id,
                "green_sec": green_sec
            })
            
    elif "【extend_decision_input_json】" in user_content:
        data = extract_json_content(user_content, "extend_decision_input_json")
        if data:
            # Heuristic for extend_decision
            # Simple heuristic: 50% yes/no
            should_extend = random.choice(["是", "否"])
            extend_sec = 0
            if should_extend == "是":
                extend_sec = random.randint(5, 30)
                
            return json.dumps({
                "extend": should_extend,
                "extend_sec": extend_sec
            })
            
    return None

def main():
    INPUT_PATH = "grpo_dataset_two_scenarios"
    OUTPUT_PATH = "sft_dataset_synthetic"
    force_regen = os.getenv("FORCE_REGEN", "").strip() == "1"
    
    if not os.path.exists(INPUT_PATH):
        print(f"Error: {INPUT_PATH} not found.")
        return
    if (not force_regen) and looks_like_hf_dataset_dir(OUTPUT_PATH, required_columns={"messages"}):
        print(f"✓ Synthetic SFT dataset 已存在: {OUTPUT_PATH}，跳过生成")
        return
    if force_regen:
        print("FORCE_REGEN=1，忽略已存在检查，继续生成 synthetic SFT dataset")

    print(f"Loading dataset from {INPUT_PATH}...")
    dataset = load_from_disk(INPUT_PATH)
    
    # Limit dataset to 3000 samples for SFT (doesn't need too much data)
    MAX_SFT_SAMPLES = 3000
    if len(dataset) > MAX_SFT_SAMPLES:
        print(f"Dataset has {len(dataset)} samples, limiting to {MAX_SFT_SAMPLES} for SFT...")
        indices = random.sample(range(len(dataset)), MAX_SFT_SAMPLES)
        dataset = dataset.select(indices)
    
    new_data = []
    
    print("Generating synthetic responses...")
    for item in dataset:
        prompt_messages = item['prompt'] # List of {role, content}
        
        response_json = generate_synthetic_response(prompt_messages)
        
        if response_json:
            # Create full conversation for SFT
            # Clone messages to avoid modifying original reference if any
            new_messages = [m.copy() for m in prompt_messages]
            new_messages.append({
                "role": "assistant",
                "content": response_json
            })
            
            new_data.append({
                "messages": new_messages
            })
    
    if not new_data:
        print("No valid samples generated!")
        return
        
    print(f"Generated {len(new_data)} samples.")
    
    # Create new dataset
    sft_dataset = Dataset.from_list(new_data)
    sft_dataset.save_to_disk(OUTPUT_PATH)
    print(f"Saved synthetic SFT dataset to {OUTPUT_PATH}")

    # Verify one sample
    print("\nSample 0:")
    print(json.dumps(sft_dataset[0]["messages"][-1], ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

# %% [markdown]
# ## 1.9 SFT Training
# 
# Train the model on the synthetic SFT dataset before GRPO.

# %% [code] cell 4

import os
import torch
from unsloth import FastLanguageModel
from trl import SFTConfig, SFTTrainer
from datasets import load_from_disk
from unsloth.chat_templates import get_chat_template
from transformers import EarlyStoppingCallback

# ==================== Config ====================
max_seq_length = 1024
lora_rank = 32
# model_name = "rd211/Qwen3-0.6B-Instruct"
model_name = "Qwen/Qwen2.5-0.5B-Instruct"
output_dir = "checkpoints/sft_tsc_synthetic"
dataset_path = "sft_dataset_synthetic"
force_sft_train = os.getenv("FORCE_SFT_TRAIN", "").strip() == "1"

def looks_like_lora_checkpoint(path: str) -> bool:
    if not os.path.isdir(path):
        return False
    marker_files = [
        "adapter_config.json",
        "adapter_model.safetensors",
        "adapter_model.bin",
    ]
    has_config = os.path.isfile(os.path.join(path, "adapter_config.json"))
    has_weights = any(os.path.isfile(os.path.join(path, f)) for f in marker_files[1:])
    return bool(has_config and has_weights)

if looks_like_lora_checkpoint(output_dir) and (not force_sft_train):
    print(f"✓ SFT 已完成: {output_dir}，跳过训练")
else:
    if force_sft_train:
        print("FORCE_SFT_TRAIN=1，忽略已存在检查，继续进行 SFT 训练")
    # ==================== Load Model ====================
    print(f"Loading model: {model_name}")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=model_name,
        max_seq_length=max_seq_length,
        load_in_4bit=False,
        fast_inference=False,
        max_lora_rank=lora_rank,
        gpu_memory_utilization=0.7,
    )

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
    model.config.use_cache = False

    if not os.path.isdir(dataset_path):
        raise FileNotFoundError(f"Dataset not found: {dataset_path}. Run generate_synthetic_sft_dataset.py first.")

    dataset = load_from_disk(dataset_path)
    print(f"Loaded {len(dataset)} samples for SFT.")

    dataset = dataset.train_test_split(test_size=0.05, seed=42)
    train_dataset = dataset["train"]
    eval_dataset = dataset["test"]

    if len(eval_dataset) > 500:
        eval_dataset = eval_dataset.select(range(500))

    print(f"Train samples: {len(train_dataset)}")
    print(f"Eval samples: {len(eval_dataset)}")

    tokenizer = get_chat_template(
        tokenizer,
        chat_template="qwen-2.5", 
    )

    def formatting_prompts_func(examples):
        convos = examples["messages"]
        
        if isinstance(convos, list) and len(convos) > 0 and isinstance(convos[0], dict):
            texts = [tokenizer.apply_chat_template(convos, tokenize=False, add_generation_prompt=False)]
        else:
            texts = [tokenizer.apply_chat_template(convo, tokenize=False, add_generation_prompt=False) for convo in convos]
            
        return texts

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        max_seq_length=max_seq_length,
        dataset_num_proc=2,
        packing=False, 
        formatting_func=formatting_prompts_func,
        args=SFTConfig(
            output_dir=output_dir,
            num_train_epochs=3,
            per_device_train_batch_size=4,
            per_device_eval_batch_size=1,
            gradient_accumulation_steps=4,
            learning_rate=2e-4, 
            fp16=not torch.cuda.is_bf16_supported(),
            bf16=torch.cuda.is_bf16_supported(),
            fp16_full_eval=not torch.cuda.is_bf16_supported(),
            bf16_full_eval=torch.cuda.is_bf16_supported(),
            logging_steps=10,
            eval_strategy="steps",
            eval_steps=30,
            save_strategy="steps",
            save_steps=30,
            load_best_model_at_end=True,
            metric_for_best_model="eval_loss",
            greater_is_better=False,
            optim="adamw_8bit",
            weight_decay=0.01,
            lr_scheduler_type="linear",
            seed=3407,
            report_to="none",
        ),
        callbacks=[EarlyStoppingCallback(early_stopping_patience=3)]
    )

    print("Starting SFT Training with Early Stopping...")
    trainer.train()

    print(f"Saving model to {output_dir}")
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print("Done.")

    import gc
    try:
        del model, tokenizer, trainer
    except NameError:
        pass
    gc.collect()
    torch.cuda.empty_cache()
    print("Memory cleaned up for GRPO stage.")

# %% [markdown]
# ## 2. 加载模型

# %% [code] cell 5
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
GRPO_CHECKPOINT_DIR = "checkpoints/grpo_tsc_two_scenarios"

def _find_latest_checkpoint(checkpoint_dir: str) -> str | None:
    """Find the latest valid checkpoint in a directory."""
    if not os.path.isdir(checkpoint_dir):
        return None
    candidates = []
    for name in os.listdir(checkpoint_dir):
        path = os.path.join(checkpoint_dir, name)
        if _looks_like_checkpoint(path):
            # Extract step number if possible (e.g., checkpoint-100)
            try:
                step = int(name.split('-')[-1])
            except (ValueError, IndexError):
                step = 0
            candidates.append((step, path))
    if not candidates:
        return None
    # Return the checkpoint with the highest step number
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1]

resume_from = CHECKPOINT_DIR if _looks_like_checkpoint(CHECKPOINT_DIR) else BASE_MODEL_DIR

# Priority: CHECKPOINT_DIR (latest symlink) > GRPO checkpoints > SFT checkpoint > base model
if _looks_like_checkpoint(CHECKPOINT_DIR):
    print(f"✓ 从 checkpoint 继续训练: {CHECKPOINT_DIR}")
    resume_from = CHECKPOINT_DIR
else:
    # Check for checkpoints in grpo_tsc_two_scenarios
    grpo_latest = _find_latest_checkpoint(GRPO_CHECKPOINT_DIR)
    if grpo_latest:
        print(f"✓ 从 GRPO checkpoint 继续训练: {grpo_latest}")
        resume_from = grpo_latest
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
    fast_inference=True,
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

# %% [markdown]
# ## 3. 加载 Dataset

# %% [code] cell 6
from datasets import load_from_disk
from datasets import Dataset

DATASET_PATH = "grpo_dataset_two_scenarios"
EVAL_TEST_SIZE = 0.001
EVAL_MAX_SAMPLES = 64
EVAL_SEED = 42

if not os.path.isdir(DATASET_PATH):
    raise FileNotFoundError(
        f"Dataset 不存在: {DATASET_PATH}\n"
        "请先运行 generate_grpo_dataset.py 生成离线 dataset"
    )

dataset = load_from_disk(DATASET_PATH)
print(f"✓ Dataset 加载成功: {DATASET_PATH}")
print(f"样本数: {len(dataset)}")

# Split out a small eval set to track real progress.
# Prefer stratified split by task_type so both tasks appear in eval.
try:
    if isinstance(dataset, Dataset) and ("task_type" in dataset.column_names):
        try:
            # Try stratified split first
            split = dataset.train_test_split(
                test_size=EVAL_TEST_SIZE,
                seed=EVAL_SEED,
                stratify_by_column="task_type",
            )
        except Exception as strat_err:
            # Fallback to non-stratified split if stratification fails
            print(f"⚠️ Stratified split failed ({strat_err}), using random split")
            split = dataset.train_test_split(test_size=EVAL_TEST_SIZE, seed=EVAL_SEED)
    else:
        split = dataset.train_test_split(test_size=EVAL_TEST_SIZE, seed=EVAL_SEED)

    train_dataset = split["train"]
    eval_dataset = split["test"]
    if len(eval_dataset) > EVAL_MAX_SAMPLES:
        eval_dataset = eval_dataset.select(range(EVAL_MAX_SAMPLES))

    print(f"✓ Train/Eval split: train={len(train_dataset)}, eval={len(eval_dataset)}")
    if "task_type" in train_dataset.column_names:
        from collections import Counter
        print("  - eval task_type counts:", Counter(eval_dataset["task_type"]))
except Exception as e:
    print(f"⚠️ Train/Eval split failed completely: {e}")
    train_dataset = dataset
    eval_dataset = None

# NOTE: Do NOT apply chat template here!
# GRPOTrainer expects prompt to be a list of messages, not a formatted string.
# It will apply the chat template internally using processing_class (tokenizer).
print("示例 Prompt (message list):")
print(dataset[0]["prompt"])

# %% [code] cell 7
print(dataset[60]["prompt"])

# %% [markdown]
# ## 4. 导入 Reward Function

# %% [code] cell 8
from tsc_reward_function import (
    tsc_reward_sim_fn,
    tsc_reward_format_fn,
    tsc_reward_constraint_fn,  # 新增
    cleanup_global_pool,
    reward_diag_snapshot,
    reward_diag_last,   
)
from transformers import TrainerCallback


class RewardDiagnosticsCallback(TrainerCallback):
    def __init__(self, kl_spike_threshold: float = 5.0):
        self.kl_spike_threshold = float(kl_spike_threshold)

    def on_log(self, args, state, control, logs=None, **kwargs):
        if not logs:
            return
        if not getattr(state, "is_world_process_zero", True):
            return

        # Periodic window summary (aligned to logging)
        if getattr(args, "logging_steps", None) and state.global_step % int(args.logging_steps) == 0:
            snap = reward_diag_snapshot(reset=True)
            total = snap.get("window_total", 0)
            invalid = snap.get("window_invalid", 0)
            rate = (invalid / total) if total else 0.0
            print(
                f"[reward_diag] steps {snap.get('window_start_step')}..{state.global_step} "
                f"invalid_rate={rate:.3f} ({invalid}/{total})"
            )
            by_task_total = snap.get("window_total_by_task", {}) or {}
            by_task_invalid = snap.get("window_invalid_by_task", {}) or {}
            by_reason = snap.get("window_reason_by_task", {}) or {}
            for task, t_total in sorted(by_task_total.items()):
                t_invalid = int(by_task_invalid.get(task, 0))
                t_rate = (t_invalid / t_total) if t_total else 0.0
                reasons = by_reason.get(task, {}) or {}
                reasons = {k: v for k, v in reasons.items() if k != "ok"}
                top = sorted(reasons.items(), key=lambda kv: kv[1], reverse=True)[:5]
                top_str = ", ".join([f"{k}:{v}" for k, v in top]) if top else "n/a"
                print(
                    f"[reward_diag]  - {task}: invalid_rate={t_rate:.3f} "
                    f"({t_invalid}/{t_total}) top={top_str}"
                )

        # KL spike dump
        kl = logs.get("kl", None)
        try:
            if kl is not None and float(kl) >= self.kl_spike_threshold:
                batch = reward_diag_last(state.global_step) or {}
                print(
                    f"[reward_diag] KL spike at step={state.global_step} kl={float(kl):.4f} batch={batch}"
                )
        except Exception:
            pass


diag_callback = RewardDiagnosticsCallback(kl_spike_threshold=5.0)

print("✓ Reward function 加载成功")

# %% [markdown]
# ## 5. 配置 GRPOTrainer

# %% [code] cell 9
from trl import GRPOConfig, GRPOTrainer

# 快速验证模式：取消下面注释以使用短训练
# QUICK_VERIFY = True
QUICK_VERIFY = False  # 正式训练设为 False

# Eval 配置：eval_dataset 为空则自动禁用
DO_EVAL = False
EVAL_STEPS = 20
EVAL_BATCH_SIZE = 4  # 必须能整除 num_generations

config = GRPOConfig(
    output_dir="checkpoints/grpo_tsc_two_scenarios",

    # 批次配置
    per_device_train_batch_size=2,
    num_generations=4,  # Keep at 4 for proper GRPO
    gradient_accumulation_steps=4,

    # 生成配置
    max_completion_length=128,  
    temperature=0.8,
    top_p=0.9,
    top_k=40,
    use_vllm=False,

    # 训练配置
    learning_rate=2e-6,
    num_train_epochs=3,
    max_steps=-1,

    # GRPO 特定
    scale_rewards=True,

    # Eval (track real progress on held-out states)
    do_eval=DO_EVAL,
    eval_strategy="steps" if DO_EVAL else "no",
    eval_steps=EVAL_STEPS,
    eval_on_start=DO_EVAL,
    per_device_eval_batch_size=EVAL_BATCH_SIZE,

    # 日志与保存
    logging_steps=5,
    save_steps=100,
    # save_total_limit=1,

    # 优化器
    optim="adamw_torch",
    weight_decay=0.001,
    warmup_ratio=0.1,
    beta=0.01,             # KL 系数（0.0 默认不加载 ref）:contentReference[oaicite:1]{index=1}
    max_grad_norm=0.5,    # 梯度裁剪（防 KL spike）

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

# %% [markdown]
# ## 6. 创建 GRPOTrainer 并开始训练

# %% [code] cell 10
# Ensure output directory exists and is writable
import os
import stat

output_dir = config.output_dir
os.makedirs(output_dir, exist_ok=True)

# Verify we can write to the directory
test_file = os.path.join(output_dir, '.write_test')
try:
    with open(test_file, 'w') as f:
        f.write('test')
    os.remove(test_file)
    print(f"✓ Output directory {output_dir} is writable")
except PermissionError:
    print(f"⚠️ Cannot write to {output_dir}, attempting to fix permissions...")
    # Try to change permissions if we own the directory
    try:
        os.chmod(output_dir, stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH | stat.S_IXOTH)
        print(f"✓ Permissions fixed for {output_dir}")
    except Exception as e:
        raise PermissionError(
            f"Cannot write to checkpoint directory: {output_dir}\n"
            f"Please run: sudo chown -R $(whoami) {output_dir}"
        ) from e

trainer = GRPOTrainer(
    model=model,
    processing_class=tokenizer,
    args=config,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    reward_funcs=[tsc_reward_sim_fn, tsc_reward_format_fn, tsc_reward_constraint_fn],
    callbacks=[diag_callback],
)



print("✓ GRPOTrainer 创建成功")
print(f"训练样本数: {len(train_dataset)}")
print(f"评估样本数: {0 if eval_dataset is None else len(eval_dataset)}")
print(f"每 epoch steps: {len(trainer.get_train_dataloader())}")

print("\n" + "="*60)
print("开始 GRPO 训练")
print("="*60 + "\n")

trainer.train()

print("\n" + "="*60)
print("训练完成")
print("="*60)

# %% [markdown]
# ## 7. 保存最终模型

# %% [code] cell 11
final_output_dir = "checkpoints/grpo_tsc_two_scenarios_final"
trainer.save_model(final_output_dir)
tokenizer.save_pretrained(final_output_dir)
print(f"✓ 最终模型已保存到: {final_output_dir}")

# %% [markdown]
# ## 8. 清理资源

# %% [code] cell 12
cleanup_global_pool()
print("✓ Simulator 池已清理")

# %% [markdown]
# ## 9. 测试推理（可选）

# %% [code] cell 13
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
