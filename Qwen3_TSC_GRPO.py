import os
import sys

# 禁用 ipywidgets 进度条，使用命令行版本的 tqdm
os.environ["UNSLOTH_VLLM_STANDBY"] = "1" # [NEW] Extra 30% context lengths! # To enable memory efficient GRPO with vLLM
os.environ["UNSLOTH_USE_MODELSCOPE"] = "1"

from unsloth import FastLanguageModel
import torch

max_seq_length = 1024
lora_rank = 32

os.environ["HF_HOME"] = 'model'
os.environ["MODELSCOPE_CACHE"] = 'model'

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/Qwen3-4B-Instruct-2507",
    max_seq_length = max_seq_length,
    load_in_4bit = False,
    fast_inference = True,
    max_lora_rank = lora_rank,
    gpu_memory_utilization = 0.9,
    # local_files_only = True,  # 强制使用本地文件
)

model = FastLanguageModel.get_peft_model(
    model,
    r = lora_rank,
    target_modules = [
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",
    ],
    lora_alpha = lora_rank*2,
    use_gradient_checkpointing = "unsloth",
    random_state = 3407,
)

import json
import re
from datasets import Dataset
from sklearn.model_selection import train_test_split

# 加载 TSC 数据集
with open('./data_TSC/tsc_sft_dataset.json', 'r', encoding='utf-8') as f:
    tsc_data = json.load(f)

print(f"总数据量: {len(tsc_data)}")

# 分割数据集：95% 训练，5% 测试
train_data, test_data = train_test_split(tsc_data, test_size=0.05, random_state=42)

print(f"训练集大小: {len(train_data)}")
print(f"测试集大小: {len(test_data)}")

# 提取答案函数 - 严格格式要求
def extract_phase_answer(text: str) -> str | None:
    """从输出中提取相位数字，严格要求格式为：下一个信号相位：数字"""
    if not text or not isinstance(text, str):
        return None
    
    # 规范化：去除多余空格和特殊字符
    text = text.strip().replace(' ', '')
    
    # 尝试多种分隔符和格式
    patterns = [
        r'下一个信号相位[:：]\d+',  # 原始格式
        r'下一个信号相位[:：]\s*(\d+)',  # 带空格
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            # 提取数字
            digits = re.findall(r'\d+', match.group(0))
            if digits:
                return digits[-1]  # 返回最后一个数字
    
    return None

# def extract_phase_answer(text: str) -> str | None:
#     """从输出中提取相位数字，严格要求格式为：下一个信号相位：数字"""
#     # 只匹配严格格式：下一个信号相位：数字
#     pattern = r'下一个信号相位[:：]\s*(\d+)'
#     match = re.search(pattern, text)
#     if match:
#         return match.group(1)
#     return None

# 准备训练数据集
def prepare_dataset(data):
    dataset_list = []
    for item in data:
        # 修改系统提示，强制格式为 "下一个信号相位：数字"
        system_prompt = "你是一位交通管理专家。你可以运用你的交通常识知识来解决交通信号控制任务。根据给定的交通场景和状态，预测下一个信号相位。你必须直接回答，格式必须是：下一个信号相位：{数字}（其中数字是0-9之间的单个数字）"
        
        prompt = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": item["input"]},
        ]
        answer = extract_phase_answer(item["output"])
        dataset_list.append({
            "prompt": prompt,
            "answer": answer,
        })
    return Dataset.from_list(dataset_list)

train_dataset = prepare_dataset(train_data)
test_dataset = prepare_dataset(test_data)

print(f"训练集样例:")
print(f"Prompt: {train_dataset[0]['prompt']}")
print(f"Answer: {train_dataset[0]['answer']}")


from tqdm import tqdm

def evaluate_model(model, tokenizer, test_dataset, max_samples=100):
    """评估模型在测试集上的准确率"""
    correct = 0
    total = 0
    
    # 只测试前 max_samples 个样本以节省时间
    test_samples = min(max_samples, len(test_dataset))
    
    FastLanguageModel.for_inference(model)  # 启用推理模式
    
    for i in tqdm(range(test_samples), desc="评估中"):
        item = test_dataset[i]
        
        # 构建输入
        messages = item['prompt']
        inputs = tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(model.device)
        
        # 生成回答
        outputs = model.generate(
            input_ids=inputs,
            max_new_tokens=128,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id,
        )
        
        # 解码输出
        response = tokenizer.decode(outputs[0][inputs.shape[1]:], skip_special_tokens=True)
        
        # 提取预测的相位
        predicted_phase = extract_phase_answer(response)
        true_phase = item['answer']
        
        if predicted_phase == true_phase:
            correct += 1
        total += 1
        
        # 打印前5个样例
        if i < 5:
            print(f"\n样例 {i+1}:")
            print(f"真实相位: {true_phase}")
            print(f"预测相位: {predicted_phase}")
            print(f"模型回答: {response[:200]}...")
    
    accuracy = correct / total if total > 0 else 0
    print(f"\n准确率: {accuracy:.2%} ({correct}/{total})")
    return accuracy

print("="*50)
print("微调前模型准确率:")
print("="*50)
accuracy_before = evaluate_model(model, tokenizer, test_dataset, max_samples=500)


import gc
# 验证输出格式
def is_valid_format(text: str) -> bool:
    """验证文本是否满足严格格式：下一个信号相位：数字"""
    pattern = r'^下一个信号相位[:：]\s*\d+\s*$'
    return bool(re.match(pattern, text.strip()))

# 奖励函数：检查预测的相位是否正确
def correctness_reward_func(prompts, completions, answer, **kwargs) -> list[float]:
    responses = [completion[0]["content"] for completion in completions]
    q = prompts[0][-1]["content"][:100]  # 只显示前100字符
    extracted_responses = [extract_phase_answer(r) for r in responses]
    
    print(
        "-" * 20,
        f"\n问题:\n{q}...",
        f"\n正确答案:\n{answer[0]}",
        f"\n模型回答:\n{responses[0][:150]}...",
        f"\n提取结果:\n{extracted_responses[0]}",
    )
    result = [2.0 if r == a else 0.0 for r, a in zip(extracted_responses, answer)]

    del responses, extracted_responses
    torch.cuda.empty_cache()
    gc.collect()
    
    return result


# 奖励函数：严格验证格式 - 下一个信号相位：数字
def format_reward_func(completions, **kwargs) -> list[float]:
    responses = [completion[0]["content"] for completion in completions]
    # 严格检查格式是否为 "下一个信号相位：数字"
    rewards = []
    for r in responses:
        if is_valid_format(r):
            rewards.append(0.5)  # 格式正确得到1.0分
        else:
            rewards.append(0.0)  # 格式不正确得到0分
    return rewards


def length_penalty_func(completions, **kwargs) -> list[float]:
    """Penalizes completions that are too long."""
    responses = [completion[0]["content"] for completion in completions]
    rewards = []
    for r in responses:
        # The ideal answer is ~7 tokens.
        # Give 0 penalty for <= 15 tokens.
        # Give an increasingly negative reward for anything longer.
        if len(r) <= 15:
            rewards.append(0.0)
        else:
            rewards.append(-0.1 * (len(r) - 15)) # Penalize -0.1 for each token over 15
    return rewards

from trl import GRPOConfig, GRPOTrainer

max_prompt_length = 896  # TSC 的输入比较长

training_args = GRPOConfig(
    learning_rate=5e-6,
    adam_beta1=0.9,
    adam_beta2=0.99,
    weight_decay=0.1,
    warmup_ratio=0.1,
    lr_scheduler_type="cosine",
    optim="paged_adamw_8bit",
    logging_steps=10,
    # num_iterations = 2,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    num_generations=4,
    max_prompt_length=max_prompt_length,
    max_completion_length=max_seq_length - max_prompt_length,
    # max_steps=20000,  # 根据需要调整
    save_steps=10000,
    num_train_epochs=1,
    max_grad_norm=1.0,
    report_to="none",
    output_dir="outputs_tsc",

    gradient_checkpointing=True,  # 启用梯度检查点
    dataloader_pin_memory=False,  # 关闭固定内存
)

trainer = GRPOTrainer(
    model=model,
    processing_class=tokenizer,
    reward_funcs=[
        correctness_reward_func,
        format_reward_func,
        length_penalty_func,
    ],
    args=training_args,
    train_dataset=train_dataset,
)


print("开始训练...")
trainer.train()

model.save_lora("tsc_grpo_saved_lora")
print("模型已保存到 tsc_grpo_saved_lora")


from peft import PeftModel
import torch

# ============ 方案A：直接使用微调后的模型（权重已保存） ============
# 加载微调后的 LoRA 权重并合并
print("加载微调后的 LoRA 权重...")

# 重新加载基础模型用于推理
base_model = model.get_base_model()

# 加载 LoRA 权重
peft_model = PeftModel.from_pretrained(
    base_model,
    "tsc_grpo_saved_lora",
    is_trainable=False
)

# 合并 LoRA 权重到基础模型
merged_model = peft_model.merge_and_unload()
print("LoRA 权重已合并")

# ============ 使用 Transformers 进行推理 ============
def evaluate_with_vllm(tokenizer, test_dataset, merged_model, max_samples=100):
    """使用微调后的模型进行推理和准确率评估"""
    correct = 0
    total = 0
    
    test_samples = min(max_samples, len(test_dataset))
    
    # 启用推理模式
    FastLanguageModel.for_inference(merged_model)
    
    for i in tqdm(range(test_samples), desc="推理中"):
        item = test_dataset[i]
        
        # 构建输入
        messages = item['prompt']
        inputs = tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(merged_model.device)
        
        # Transformers 推理参数（兼容 Unsloth）
        with torch.no_grad():
            outputs = merged_model.generate(
                input_ids=inputs,
                max_new_tokens=128,
                temperature=0.7,
                do_sample=True,
                top_k=50,
                pad_token_id=tokenizer.pad_token_id,
            )
        
        # 提取生成的文本
        response = tokenizer.decode(outputs[0][inputs.shape[1]:], skip_special_tokens=True)
        
        # 提取预测的相位
        predicted_phase = extract_phase_answer(response)
        true_phase = item['answer']
        
        if predicted_phase == true_phase:
            correct += 1
        total += 1
        
        # 打印前5个样例
        if i < 5:
            print(f"\n样例 {i+1}:")
            print(f"真实相位: {true_phase}")
            print(f"预测相位: {predicted_phase}")
            print(f"模型回答: {response[:200]}...")
    
    accuracy = correct / total if total > 0 else 0
    print(f"\n准确率: {accuracy:.2%} ({correct}/{total})")
    return accuracy

print("="*50)
print("微调后模型准确率（vLLM）:")
print("="*50)
accuracy_after = evaluate_with_vllm(tokenizer, test_dataset, merged_model, max_samples=500)


print("\n" + "="*50)
print("准确率对比")
print("="*50)
print(f"微调前准确率: {accuracy_before:.2%}")
print(f"微调后准确率: {accuracy_after:.2%}")
print(f"提升幅度: {(accuracy_after - accuracy_before):.2%}")
print("="*50)

# screen
# source .venv/bin/activate
# xray-start
# source /etc/xray_proxy
# python Qwen3_TSC_GRPO.py > training_output.log 2>&1