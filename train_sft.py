
import os
import torch
from unsloth import FastLanguageModel
from trl import SFTConfig, SFTTrainer
from datasets import load_from_disk
from unsloth.chat_templates import get_chat_template
from transformers import EarlyStoppingCallback

# ==================== Config ====================
max_seq_length = 2048
lora_rank = 32
# model_name = "rd211/Qwen3-0.6B-Instruct"
model_name = "Qwen/Qwen2.5-0.5B-Instruct"
output_dir = "checkpoints/sft_tsc_synthetic"
dataset_path = "sft_dataset_synthetic"

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

# ==================== Load Dataset ====================
if not os.path.isdir(dataset_path):
    raise FileNotFoundError(f"Dataset not found: {dataset_path}. Run generate_synthetic_sft_dataset.py first.")

dataset = load_from_disk(dataset_path)
print(f"Loaded {len(dataset)} samples for SFT.")

# Split dataset into train and test
dataset = dataset.train_test_split(test_size=0.05, seed=42)
train_dataset = dataset["train"]
eval_dataset = dataset["test"]

# Limit eval dataset to 200 samples for speed
if len(eval_dataset) > 500:
    eval_dataset = eval_dataset.select(range(500))

print(f"Train samples: {len(train_dataset)}")
print(f"Eval samples: {len(eval_dataset)}")

# ==================== Configure Trainer ====================
# Apply chat template
tokenizer = get_chat_template(
    tokenizer,
    chat_template="qwen-2.5", 
)

# Formatting function for chat 
def formatting_prompts_func(examples):
    convos = examples["messages"]
    
    # Logic to handle both batched and non-batched inputs
    if isinstance(convos, list) and len(convos) > 0 and isinstance(convos[0], dict):
        # Single conversation (list of dicts)
        texts = [tokenizer.apply_chat_template(convos, tokenize=False, add_generation_prompt=False)]
    else:
        # Batch of conversations (list of lists of dicts)
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
        num_train_epochs=3, # Increase epochs relying on early stopping
        per_device_train_batch_size=2,
        per_device_eval_batch_size=1,
        gradient_accumulation_steps=4,
        learning_rate=2e-4, 
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        fp16_full_eval=not torch.cuda.is_bf16_supported(),
        bf16_full_eval=torch.cuda.is_bf16_supported(),
        logging_steps=10,
        eval_strategy="steps",
        eval_steps=30, # Evaluate every 30 steps
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
    callbacks=[EarlyStoppingCallback(early_stopping_patience=3)] # Stop if no improvement for 3 eval steps (90 steps)
)


print("Starting SFT Training with Early Stopping...")
trainer.train()

print(f"Saving model to {output_dir}")
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)
print("Done.")
