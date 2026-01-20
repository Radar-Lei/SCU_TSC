import os
import json
import random
import re
from datasets import load_from_disk, Dataset

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
                # 从 prompt 中提取 max_extend_sec，默认为 8
                max_extend_sec = data.get("max_extend_sec", 8)
                extend_sec = random.randint(1, max_extend_sec)
                
            return json.dumps({
                "extend": should_extend,
                "extend_sec": extend_sec
            })
            
    return None

def main():
    INPUT_PATH = "grpo_dataset_two_scenarios"
    OUTPUT_PATH = "sft_dataset_synthetic"
    
    if not os.path.exists(INPUT_PATH):
        print(f"Error: {INPUT_PATH} not found.")
        return

    print(f"Loading dataset from {INPUT_PATH}...")
    dataset = load_from_disk(INPUT_PATH)
    
    # Limit dataset to 2000 samples for SFT (doesn't need too much data)
    MAX_SFT_SAMPLES = 2000
    if len(dataset) > MAX_SFT_SAMPLES:
        print(f"Dataset has {len(dataset)} samples, limiting to {MAX_SFT_SAMPLES} for SFT...")
        random.seed(42)
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
