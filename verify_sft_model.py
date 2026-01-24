
from unsloth import FastLanguageModel
import torch
import json
from transformers import TextStreamer

# 1. Load SFT Model
model_name = "checkpoints/sft_tsc_synthetic"
print(f"Loading SFT model from: {model_name}")

max_seq_length = 2048
lora_rank = 32

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=model_name,
    max_seq_length=max_seq_length,
    load_in_4bit=False, 
    fast_inference=False,
    max_lora_rank=lora_rank,
    gpu_memory_utilization=0.6,
)
FastLanguageModel.for_inference(model)

# 2. Prepare a test prompt
# A minimal signal_step prompt similar to what we trained on
json_payload = {
    "crossing_id": 12345,
    "state": {
        "current_phase_id": 1,
        "phase_metrics_now": [
            {"phase_id": 1, "avg_queue_veh": 10.0},
            {"phase_id": 2, "avg_queue_veh": 5.0}
        ]
    },
    "scenario": {"phase_ids": [1, 2]}
}
json_text = json.dumps(json_payload, ensure_ascii=False)

# Mimic the prompt format used in training
# NOTE: We must use the exact same template/string format
prompt_content = f"""你是交通信号控制优化专家。【signal_step_input_json】{json_text}【/signal_step_input_json】

1. 输出：下一个信号相位 next_phase_id，以及该相位绿灯持续时间 green_sec（单位：秒）。
要求：只输出最终 JSON，例如 {{"next_phase_id": 1, "green_sec": 30}}。
"""

messages = [
    {"role": "user", "content": prompt_content}
]

# 3. Apply Chat Template
prompt_str = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

print("\n========== Input Prompt ==========")
print(prompt_str)
print("==================================\n")

# 4. Generate
inputs = tokenizer(prompt_str, return_tensors="pt").to("cuda")

print("Generating response...")
streamer = TextStreamer(tokenizer, skip_prompt=True)
_ = model.generate(
    **inputs,
    streamer=streamer,
    max_new_tokens=128,
    temperature=0.1,
    do_sample=False, 
)
