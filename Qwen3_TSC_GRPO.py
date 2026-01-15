# -*- coding: utf-8 -*-
# 从 Qwen3_TSC_GRPO.ipynb 自动转换

# ======================================================================
# ### TSC 交通信号控制微调 - Non-Thinking 版本
# 
# ======================================================================

# ======================================================================
# ### Installation
# 
# ======================================================================

# %%
import os
# os.environ["UNSLOTH_VLLM_STANDBY"] = "1" # [NEW] Extra 30% context lengths! # To enable memory efficient GRPO with vLLM
os.environ["UNSLOTH_USE_MODELSCOPE"] = "1"

# %%
import subprocess 
import os 
result = subprocess.run('bash -c "source /etc/network_turbo && env | grep proxy"', shell=True, capture_output=True, text=True)
output = result.stdout
for line in output.splitlines():
	if '=' in line:
		var, value = line.split('=', 1)
		os.environ[var] = value

# ======================================================================
# ### 加载模型
# 
# ======================================================================

# %%
from unsloth import FastLanguageModel
import torch

max_seq_length = 1024
lora_rank = 32

os.environ["HF_HOME"] = 'model'
os.environ["MODELSCOPE_CACHE"] = 'model'

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "model/models/qwen3-4B-SFT",
    max_seq_length = max_seq_length,
    load_in_4bit = False,
    fast_inference = False,
    max_lora_rank = lora_rank,
    gpu_memory_utilization = 0.8,
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

# ======================================================================
# ### 加载 TSC 数据集
# 
# ======================================================================

# %%
import json
import re
import os
import xml.etree.ElementTree as ET
from datasets import Dataset
from typing import Dict, List, Tuple

# ==================== 场景发现与配置 ====================

def discover_environments(environments_root: str) -> Dict[str, Dict]:
    """
    扫描 environments/ 目录，发现所有可用的仿真场景
    
    返回:
        dict: {场景名: {'sumocfg': 配置文件路径, 'net': 路网文件路径, 'tl_ids': 信号灯ID列表}}
    """
    environments = {}
    
    if not os.path.isdir(environments_root):
        print(f"警告: environments 目录不存在: {environments_root}")
        return environments
    
    for scenario_name in sorted(os.listdir(environments_root)):
        scenario_dir = os.path.join(environments_root, scenario_name)
        if not os.path.isdir(scenario_dir) or scenario_name.startswith('.'):
            continue
        
        # 查找 .sumocfg 文件
        sumocfg = None
        for f in os.listdir(scenario_dir):
            if f.endswith('.sumocfg'):
                sumocfg = os.path.join(scenario_dir, f)
                break
        
        # 查找 .net.xml 文件
        net_xml = None
        for f in os.listdir(scenario_dir):
            if f.endswith('.net.xml'):
                net_xml = os.path.join(scenario_dir, f)
                break
        
        if sumocfg and net_xml:
            # 从 net.xml 提取信号灯 ID
            tl_ids = extract_traffic_light_ids(net_xml)
            if tl_ids:
                environments[scenario_name] = {
                    'sumocfg': sumocfg,
                    'net': net_xml,
                    'tl_ids': tl_ids
                }
    
    return environments


def extract_traffic_light_ids(net_xml_path: str) -> List[str]:
    """
    从 net.xml 文件中提取所有信号灯 ID
    """
    tl_ids = []
    try:
        for event, elem in ET.iterparse(net_xml_path, events=("end",)):
            if elem.tag == "tlLogic":
                tl_id = elem.attrib.get("id")
                if tl_id and tl_id not in tl_ids:
                    tl_ids.append(tl_id)
                elem.clear()
    except Exception as e:
        print(f"解析 {net_xml_path} 失败: {e}")
    return tl_ids


# ==================== 发现所有场景 ====================
ENVIRONMENTS_ROOT = os.path.join(os.getcwd(), 'sumo_simulation/environments')
AVAILABLE_ENVIRONMENTS = discover_environments(ENVIRONMENTS_ROOT)

print("="*60)
print("发现的仿真场景：")
print("="*60)

total_tl_count = 0
for scenario_name, info in AVAILABLE_ENVIRONMENTS.items():
    tl_count = len(info['tl_ids'])
    total_tl_count += tl_count
    print(f"  {scenario_name}: {tl_count} 个信号交叉口")
    # 显示前5个信号灯ID
    preview = info['tl_ids'][:5]
    suffix = "..." if len(info['tl_ids']) > 5 else ""
    print(f"    信号灯: {preview}{suffix}")

print("="*60)
print(f"共 {len(AVAILABLE_ENVIRONMENTS)} 个场景, {total_tl_count} 个信号交叉口")
print("="*60)

# %%
# ==================== 模型输出解析函数 ====================

def extract_phase_and_duration(text: str) -> tuple[int | None, int | None]:
    """
    从模型输出中提取相位和持续时间
    
    支持格式：
    - "下一个信号相位：2，持续时间：30秒"
    - "下一个信号相位：2，持续时间为30秒"
    - "下一个信号相位：2，持续时间30"
    
    返回:
        tuple: (相位索引, 持续时间秒数)，无法提取时返回 (None, None)
    """
    if not text or not isinstance(text, str):
        return None, None
    
    text = text.strip()
    
    # 提取相位
    phase = None
    phase_patterns = [
        r'下一个信号相位[:：]\s*(\d+)',
        r'相位[:：]\s*(\d+)',
        r'phase[:：]?\s*(\d+)',
    ]
    for pattern in phase_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            phase = int(match.group(1))
            break
    
    # 提取持续时间
    duration = None
    duration_patterns = [
        r'持续时间[:：]?\s*[为]?\s*(\d+)\s*秒?',
        r'时间[:：]?\s*(\d+)\s*秒',
        r'duration[:：]?\s*(\d+)',
        r'(\d+)\s*秒',
    ]
    for pattern in duration_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            duration = int(match.group(1))
            duration = max(5, min(duration, 120))
            break
    
    if duration is None and phase is not None:
        duration = 30
    
    return phase, duration


# ==================== 系统提示（在线仿真训练专用）====================
SYSTEM_PROMPT = """你是一位交通管理专家。你可以运用你的交通常识知识来解决交通信号控制任务。
根据给定的交通场景和状态，预测下一个信号相位及其持续时间。
你必须直接回答，格式必须是：下一个信号相位：{数字}，持续时间：{秒数}秒
其中数字是相位索引（从0开始），秒数是持续时间（通常在20-90秒之间）。"""


# ==================== 多场景在线数据集生成 ====================
def generate_multi_scenario_dataset(simulators_info: List[Tuple], samples_per_tl: int = 10) -> Dataset:
    """
    从多个场景的多个信号交叉口生成训练数据集
    
    参数:
        simulators_info: [(simulator, tl_id, scenario_name), ...] 已初始化的仿真器信息列表
        samples_per_tl: 每个信号灯生成的样本数
        
    返回:
        Dataset: 包含多场景交通状态的数据集
    """
    dataset_list = []
    
    for simulator, tl_id, scenario_name in simulators_info:
        if simulator is None or not simulator.is_connected():
            continue
        
        for i in range(samples_per_tl):
            # 获取当前交通状态
            traffic_state = simulator.get_current_traffic_state_prompt(tl_id)
            
            if traffic_state:
                # 添加场景信息到 prompt
                enhanced_prompt = f"[场景: {scenario_name}, 信号灯: {tl_id}]\n{traffic_state}"
                
                prompt = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": enhanced_prompt},
                ]
                dataset_list.append({
                    "prompt": prompt,
                    "answer": None,
                    "scenario": scenario_name,
                    "tl_id": tl_id,
                })
            
            # 推进仿真
            for _ in range(10):
                simulator.step()
    
    return Dataset.from_list(dataset_list)


print("在线仿真数据集生成函数已定义")
print(f"系统提示长度: {len(SYSTEM_PROMPT)} 字符")

# ======================================================================
# ### 定义奖励函数
# 
# ======================================================================

# %%
# ==================== 多场景仿真器管理 ====================
import sys
import random

# 添加 sumo_simulation 目录到 Python 路径
sumo_sim_path = os.path.join(os.getcwd(), 'sumo_simulation')
if sumo_sim_path not in sys.path:
    sys.path.insert(0, sumo_sim_path)

from sumo_simulator import SUMOSimulator, stop_simulation

# ==================== GRPO 训练配置 ====================
GRPO_CONFIG = {
    'gui': True,              # 是否使用 GUI（False = 无头模式，更快）
    'warmup_steps': 300,       # 预热步数
    'reward_alpha': 1.0,       # 通过车辆数权重
    'reward_beta': 0.5,        # 排队车辆数惩罚权重
    'samples_per_tl': 20,      # 每个信号灯生成的样本数
    'max_tl_per_scenario': 5,  # 每个场景最多使用的信号灯数量（避免过大场景）
}

# 全局状态：当前活跃的仿真器和信号灯信息
_active_simulator = None
_active_scenario = None
_active_tl_id = None
_all_scenarios_tls = []  # [(scenario_name, tl_id), ...] 所有场景的信号灯列表


def build_scenario_tl_list():
    """
    构建所有场景的信号灯列表，用于训练时随机选择
    """
    global _all_scenarios_tls
    _all_scenarios_tls = []
    
    for scenario_name, info in AVAILABLE_ENVIRONMENTS.items():
        tl_ids = info['tl_ids'][:GRPO_CONFIG['max_tl_per_scenario']]
        for tl_id in tl_ids:
            _all_scenarios_tls.append((scenario_name, tl_id))
    
    random.shuffle(_all_scenarios_tls)
    print(f"构建训练列表: {len(_all_scenarios_tls)} 个 (场景, 信号灯) 组合")
    return _all_scenarios_tls


def init_scenario_simulator(scenario_name: str) -> SUMOSimulator | None:
    """
    初始化指定场景的仿真器
    """
    global _active_simulator, _active_scenario
    
    # 如果当前场景已经初始化，直接返回
    if _active_simulator is not None and _active_scenario == scenario_name:
        return _active_simulator
    
    # 关闭之前的仿真器
    cleanup_active_simulator()
    
    # 获取场景配置
    if scenario_name not in AVAILABLE_ENVIRONMENTS:
        print(f"错误: 场景 {scenario_name} 不存在")
        return None
    
    env_info = AVAILABLE_ENVIRONMENTS[scenario_name]
    
    print(f"正在初始化场景: {scenario_name}")
    
    try:
        _active_simulator = SUMOSimulator(
            config_file=env_info['sumocfg'],
            junctions_file=None,  # environments 场景通常没有 JSON 配置
            gui=GRPO_CONFIG['gui'],
        )
        
        if _active_simulator.start_simulation():
            _active_scenario = scenario_name
            print(f"✓ 场景 {scenario_name} 初始化成功")
            return _active_simulator
        else:
            print(f"✗ 场景 {scenario_name} 启动失败")
            _active_simulator = None
            return None
            
    except Exception as e:
        print(f"✗ 场景 {scenario_name} 初始化错误: {e}")
        _active_simulator = None
        return None


def switch_to_scenario_tl(scenario_name: str, tl_id: str) -> bool:
    """
    切换到指定场景和信号灯
    """
    global _active_tl_id
    
    simulator = init_scenario_simulator(scenario_name)
    if simulator is None:
        return False
    
    _active_tl_id = tl_id
    return True


def get_active_simulator():
    """获取当前活跃的仿真器"""
    return _active_simulator


def get_active_tl_id():
    """获取当前活跃的信号灯ID"""
    return _active_tl_id


def get_active_scenario():
    """获取当前活跃的场景名"""
    return _active_scenario


def cleanup_active_simulator():
    """清理当前活跃的仿真器"""
    global _active_simulator, _active_scenario, _active_tl_id
    
    if _active_simulator is not None:
        try:
            _active_simulator.close()
        except:
            pass
        _active_simulator = None
        _active_scenario = None
        _active_tl_id = None


# 构建场景信号灯列表
build_scenario_tl_list()

print(f"\n多场景仿真管理器已初始化")
print(f"  - 可用场景: {len(AVAILABLE_ENVIRONMENTS)}")
print(f"  - 训练组合: {len(_all_scenarios_tls)}")

# %%
import gc

# ==================== 格式验证 ====================
def is_valid_format(text: str) -> bool:
    """验证文本是否满足格式：下一个信号相位：数字，持续时间：数字秒"""
    patterns = [
        r'下一个信号相位[:：]\s*\d+[,，]\s*持续时间[:：]?\s*[为]?\s*\d+\s*秒?',
        r'下一个信号相位[:：]\s*\d+',
    ]
    text = text.strip()
    for pattern in patterns:
        if re.match(pattern, text):
            return True
    return False


# ==================== 基于仿真的奖励函数（顺序训练模式）====================
def simulation_reward_func(prompts, completions, **kwargs) -> list[float]:
    """
    基于 SUMO 仿真的奖励函数
    
    顺序训练模式下，仿真器已在 train_single_tl 中初始化，
    直接使用当前活跃的仿真器和信号灯。
    """
    simulator = get_active_simulator()
    tl_id = get_active_tl_id()
    scenario_name = get_active_scenario()
    
    # 如果仿真器未初始化或已断开，回退到格式奖励
    if simulator is None or not simulator.is_connected() or tl_id is None:
        print("[WARN] 仿真器未连接，使用格式奖励")
        return format_reward_func(completions, **kwargs)
    
    responses = [completion[0]["content"] for completion in completions]
    alpha = GRPO_CONFIG['reward_alpha']
    beta = GRPO_CONFIG['reward_beta']
    
    # 解析决策
    actions = []
    for r in responses:
        phase, duration = extract_phase_and_duration(r)
        if phase is None:
            phase = 0
        if duration is None:
            duration = 30
        actions.append((phase, duration))
    
    # 仿真评估
    try:
        results = simulator.evaluate_multiple_actions_for_grpo(tl_id, actions)
        
        rewards = []
        for result in results:
            passed = result.get('passed_vehicles', 0)
            queue = result.get('queue_vehicles', 0)
            reward = alpha * passed - beta * queue
            reward = max(-2.0, min(2.0, reward / 10.0))
            rewards.append(reward)
        
        # 调试输出
        print(f"[仿真] {scenario_name}/{tl_id}: ", end="")
        for action, reward in zip(actions, rewards):
            print(f"P{action[0]}D{action[1]}→{reward:.2f} ", end="")
        print()
        
        # 推进仿真，为下一个样本准备不同的交通状态
        for _ in range(10):
            simulator.step()
        
        return rewards
        
    except Exception as e:
        print(f"[ERROR] 仿真奖励失败 ({scenario_name}/{tl_id}): {e}")
        # 仿真可能已结束，清理仿真器以便下次重新初始化
        cleanup_active_simulator()
        return format_reward_func(completions, **kwargs)


def format_reward_func(completions, **kwargs) -> list[float]:
    """格式奖励"""
    responses = [completion[0]["content"] for completion in completions]
    return [0.5 if is_valid_format(r) else 0.0 for r in responses]


def length_penalty_func(completions, **kwargs) -> list[float]:
    """长度惩罚"""
    responses = [completion[0]["content"] for completion in completions]
    rewards = []
    for r in responses:
        if len(r) <= 40:
            rewards.append(0.0)
        else:
            rewards.append(-0.05 * (len(r) - 40))
    return rewards


print("奖励函数已定义：")
print("  - simulation_reward_func: 基于 SUMO 仿真的奖励（顺序训练模式）")
print("  - format_reward_func: 格式验证奖励")
print("  - length_penalty_func: 长度惩罚")

# ======================================================================
# ### 配置并开始 GRPO 训练
# 
# ======================================================================

# %%
import torch.nn.functional as F
from torch.optim import AdamW
from transformers import get_cosine_schedule_with_warmup

# ==================== 真正的在线 GRPO 训练配置 ====================
# 每一步训练：获取当前状态 → 生成决策 → 评估 → 更新模型 → 执行最佳决策推进仿真

ONLINE_CONFIG = {
    'steps_per_tl': 200,           # 每个信号交叉口的训练步数
    'num_generations': 4,          # 每步生成的决策数量（减少以节省内存）
    'learning_rate': 1e-6,         # 学习率
    'max_new_tokens': 48,          # 生成的最大token数（减少以节省内存）
    'temperature': 0.7,            # 生成温度
    'gradient_accumulation_steps': 4,  # 梯度累积步数
    'save_after_each_tl': True,    # 每个交叉口训练完是否保存
    'log_interval': 10,            # 日志输出间隔
    'reward_alpha': 1.0,           # 通过车辆数权重
    'reward_beta': 0.5,            # 排队车辆数惩罚权重
    'kl_coef': 0.1,                # KL 散度惩罚系数
    'clip_range': 0.2,             # PPO/GRPO clip 范围
    'clear_cache_interval': 5,     # 每多少步清理一次 GPU 缓存
}

print("="*60)
print("在线 GRPO 训练配置")
print("="*60)
print(f"  - 场景数量: {len(AVAILABLE_ENVIRONMENTS)}")
print(f"  - 信号交叉口总数: {len(_all_scenarios_tls)}")
print(f"  - 每交叉口训练步数: {ONLINE_CONFIG['steps_per_tl']}")
print(f"  - 每步生成决策数: {ONLINE_CONFIG['num_generations']}")
print(f"  - 学习率: {ONLINE_CONFIG['learning_rate']}")
print("="*60)


def compute_grpo_loss(model, tokenizer, prompt_ids, completion_ids, rewards, 
                       old_log_probs=None, kl_coef=0.1, clip_range=0.2):
    """
    计算 GRPO 损失函数
    
    GRPO 核心思想：
    - 对于同一个 prompt，生成多个 completions
    - 使用 reward 的相对排名来更新策略
    - 高奖励的 completion 增加概率，低奖励的减少概率
    """
    device = next(model.parameters()).device
    
    # 合并 prompt 和 completion
    input_ids = torch.cat([prompt_ids, completion_ids], dim=1).to(device)
    
    # 获取模型输出的 logits
    # 注意：不使用 autocast，因为 Unsloth LoRA 内核需要一致的数据类型
    outputs = model(input_ids=input_ids)
    logits = outputs.logits
    
    # 只计算 completion 部分的 log probabilities
    prompt_len = prompt_ids.shape[1]
    completion_logits = logits[:, prompt_len-1:-1, :]  # 预测 completion tokens
    completion_targets = completion_ids.to(device)
    
    # 计算 log probabilities
    log_probs = F.log_softmax(completion_logits, dim=-1)
    token_log_probs = torch.gather(log_probs, 2, completion_targets.unsqueeze(-1)).squeeze(-1)
    
    # 对每个 completion 求和得到序列 log prob
    # 使用 attention mask 忽略 padding
    attention_mask = (completion_targets != tokenizer.pad_token_id).float()
    seq_log_probs = (token_log_probs * attention_mask).sum(dim=1) / (attention_mask.sum(dim=1) + 1e-8)
    
    # 归一化奖励（GRPO 的核心：使用相对奖励）
    rewards_tensor = torch.tensor(rewards, dtype=torch.float32, device=device)
    rewards_normalized = (rewards_tensor - rewards_tensor.mean()) / (rewards_tensor.std() + 1e-8)
    
    # GRPO 损失：-log_prob * normalized_reward
    # 高奖励的 completion 会增加其 log_prob（减少负 loss）
    # 低奖励的 completion 会减少其 log_prob
    policy_loss = -(seq_log_probs * rewards_normalized).mean()
    
    # 可选：添加 KL 散度惩罚（如果有参考模型的 log_probs）
    kl_loss = 0.0
    if old_log_probs is not None:
        old_log_probs = torch.tensor(old_log_probs, device=device)
        kl_div = seq_log_probs - old_log_probs
        kl_loss = kl_coef * kl_div.mean()
    
    total_loss = policy_loss + kl_loss
    
    return total_loss, {
        'policy_loss': policy_loss.item(),
        'kl_loss': kl_loss if isinstance(kl_loss, float) else kl_loss.item(),
        'mean_reward': rewards_tensor.mean().item(),
        'mean_log_prob': seq_log_probs.mean().item(),
    }


def online_train_single_tl(scenario_name: str, tl_id: str, tl_index: int, total_tls: int):
    """
    对单个信号交叉口进行真正的在线 GRPO 训练
    
    每一步训练：
    1. 从当前仿真状态获取交通数据 → 构造 prompt
    2. 模型生成 num_generations 个决策
    3. 评估每个决策（保存状态 → 执行 → 计算奖励 → 恢复状态）
    4. 计算 GRPO loss，更新模型
    5. 选择最佳决策，真正执行它，推进仿真
    """
    print("\n" + "="*60)
    print(f"[{tl_index}/{total_tls}] 场景: {scenario_name}, 信号灯: {tl_id}")
    print("="*60)
    
    # 1. 初始化仿真器
    print("正在初始化仿真器...")
    if not switch_to_scenario_tl(scenario_name, tl_id):
        print(f"✗ 无法初始化 {scenario_name}/{tl_id}，跳过")
        return False
    
    simulator = get_active_simulator()
    if simulator is None or not simulator.is_connected():
        print(f"✗ 仿真器未连接，跳过")
        return False
    
    print("✓ 仿真器已就绪")
    
    # 2. 设置优化器
    # 只优化 LoRA 参数
    trainable_params = [p for p in model.parameters() if p.requires_grad]
    optimizer = AdamW(trainable_params, lr=ONLINE_CONFIG['learning_rate'], weight_decay=0.1)
    
    num_steps = ONLINE_CONFIG['steps_per_tl']
    scheduler = get_cosine_schedule_with_warmup(
        optimizer,
        num_warmup_steps=int(num_steps * 0.1),
        num_training_steps=num_steps
    )
    
    # 训练统计
    total_loss = 0.0
    total_reward = 0.0
    step_count = 0
    
    print(f"开始在线 GRPO 训练（{num_steps} 步）...")
    print(f"每步: 获取状态 → 生成 {ONLINE_CONFIG['num_generations']} 个决策 → 评估 → 更新 → 执行最佳决策")
    
    # 3. 在线训练主循环
    # 清理 GPU 内存
    gc.collect()
    torch.cuda.empty_cache()
    
    # 注意：使用 FastLanguageModel.for_training/for_inference 来正确切换模式
    optimizer.zero_grad()
    
    for step in range(num_steps):
        # 检查仿真器连接状态
        if not simulator.is_connected():
            print(f"\n仿真在第 {step} 步结束，完成训练")
            break
        
        # ========== Step A: 从当前仿真状态获取 prompt ==========
        traffic_state = simulator.get_current_traffic_state_prompt(tl_id)
        if not traffic_state:
            # 推进仿真并跳过
            for _ in range(10):
                if simulator.is_connected():
                    simulator.step()
            continue
        
        # 构造完整 prompt
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": traffic_state},
        ]
        
        # 编码 prompt
        prompt_text = tokenizer.apply_chat_template(
            messages, 
            tokenize=False, 
            add_generation_prompt=True
        )
        prompt_ids = tokenizer(prompt_text, return_tensors="pt", add_special_tokens=False).input_ids
        
        # ========== Step B: 生成多个决策 ==========
        device = next(model.parameters()).device
        prompt_ids_batch = prompt_ids.repeat(ONLINE_CONFIG['num_generations'], 1).to(device)
        
        # 切换到推理模式进行生成
        FastLanguageModel.for_inference(model)
        with torch.no_grad():
            generated = model.generate(
                input_ids=prompt_ids_batch,
                max_new_tokens=ONLINE_CONFIG['max_new_tokens'],
                temperature=ONLINE_CONFIG['temperature'],
                do_sample=True,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id,
            )
        # 提取 completion 部分（在推理模式下）
        completion_ids = generated[:, prompt_ids.shape[1]:].clone().detach()
        
        # 切换回训练模式
        FastLanguageModel.for_training(model)
        
        # 解码生成的文本
        completions = tokenizer.batch_decode(completion_ids, skip_special_tokens=True)
        
        # ========== Step C: 解析决策并评估 ==========
        actions = []
        for comp in completions:
            phase, duration = extract_phase_and_duration(comp)
            if phase is None:
                phase = 0
            if duration is None:
                duration = 30
            actions.append((phase, duration))
        
        # 使用仿真评估所有决策
        try:
            results = simulator.evaluate_multiple_actions_for_grpo(tl_id, actions)
        except Exception as e:
            print(f"\n[ERROR] 评估失败: {e}")
            break
        
        # 计算奖励
        alpha = ONLINE_CONFIG['reward_alpha']
        beta = ONLINE_CONFIG['reward_beta']
        rewards = []
        for result in results:
            passed = result.get('passed_vehicles', 0)
            queue = result.get('queue_vehicles', 0)
            reward = alpha * passed - beta * queue
            reward = max(-2.0, min(2.0, reward / 10.0))  # 归一化
            rewards.append(reward)
        
        # 添加格式奖励
        for i, comp in enumerate(completions):
            if is_valid_format(comp):
                rewards[i] += 0.5
        
        # ========== Step D: 计算 GRPO loss 并更新 ==========
        # 确保张量可用于梯度计算（需要 clone 以脱离推理模式）
        prompt_ids_for_loss = prompt_ids_batch.clone()
        completion_ids_for_loss = completion_ids.clone()
        
        loss, loss_info = compute_grpo_loss(
            model, tokenizer,
            prompt_ids_for_loss, completion_ids_for_loss,
            rewards,
            kl_coef=ONLINE_CONFIG['kl_coef'],
            clip_range=ONLINE_CONFIG['clip_range']
        )
        
        # 梯度累积
        loss = loss / ONLINE_CONFIG['gradient_accumulation_steps']
        loss.backward()
        
        if (step + 1) % ONLINE_CONFIG['gradient_accumulation_steps'] == 0:
            torch.nn.utils.clip_grad_norm_(trainable_params, max_norm=1.0)
            optimizer.step()
            scheduler.step()
            optimizer.zero_grad()
        
        # ========== Step E: 执行最佳决策，推进仿真 ==========
        best_idx = rewards.index(max(rewards))
        best_phase, best_duration = actions[best_idx]
        
        # 真正执行最佳决策！
        try:
            import traci
            traci.trafficlight.setPhase(tl_id, best_phase)
            for _ in range(best_duration):
                if simulator.is_connected():
                    simulator.step()
                else:
                    break
        except Exception as e:
            print(f"\n[ERROR] 执行决策失败: {e}")
            break
        
        # 统计
        loss_value = loss.item() * ONLINE_CONFIG['gradient_accumulation_steps']
        max_reward = max(rewards)
        total_loss += loss_value
        total_reward += max_reward
        step_count += 1
        
        # 清理中间张量，释放内存
        del loss, prompt_ids, prompt_ids_batch, prompt_ids_for_loss
        del generated, completion_ids, completion_ids_for_loss
        del completions, actions, results, rewards, loss_info
        
        # 定期清理 GPU 缓存
        if (step + 1) % ONLINE_CONFIG['clear_cache_interval'] == 0:
            gc.collect()
            torch.cuda.empty_cache()
        
        # 日志
        if (step + 1) % ONLINE_CONFIG['log_interval'] == 0:
            avg_loss = total_loss / step_count
            avg_reward = total_reward / step_count
            print(f"  Step {step+1}/{num_steps} | Loss: {avg_loss:.4f} | Avg Reward: {avg_reward:.3f} | "
                  f"Best: P{best_phase}D{best_duration}s")
    
    # 4. 训练完成
    print(f"\n✓ {scenario_name}/{tl_id} 训练完成！共 {step_count} 步")
    print(f"  平均损失: {total_loss/max(1,step_count):.4f}")
    print(f"  平均奖励: {total_reward/max(1,step_count):.3f}")
    
    # 5. 清理仿真器
    cleanup_active_simulator()
    
    # 6. 保存检查点
    if ONLINE_CONFIG['save_after_each_tl'] and step_count > 0:
        checkpoint_dir = "checkpoints/tsc_latest"
        import shutil
        if os.path.isdir(checkpoint_dir):
            shutil.rmtree(checkpoint_dir)
        os.makedirs(checkpoint_dir, exist_ok=True)
        model.save_pretrained(checkpoint_dir)
        print(f"  ✓ 模型已保存到 {checkpoint_dir}")
    
    return step_count > 0

# %%
# ==================== 在线 GRPO 训练主循环 ====================
# 真正的在线训练：每步从仿真获取状态 → 生成决策 → 评估 → 更新 → 执行最佳决策

print("="*60)
print("开始在线 GRPO 训练")
print("="*60)
print("训练流程（每一步）：")
print("  1. 从当前仿真状态获取交通数据")
print("  2. 模型生成多个信号控制决策")
print("  3. 仿真评估每个决策（使用状态保存/恢复）")
print("  4. 计算 GRPO loss，更新模型权重")
print("  5. 执行最佳决策，推进仿真到下一个决策点")
print("="*60)
print(f"总共 {len(AVAILABLE_ENVIRONMENTS)} 个场景，{len(_all_scenarios_tls)} 个信号交叉口")
print("="*60)

# 按场景分组
scenarios_order = {}
for scenario_name, tl_id in _all_scenarios_tls:
    if scenario_name not in scenarios_order:
        scenarios_order[scenario_name] = []
    scenarios_order[scenario_name].append(tl_id)

# 训练统计
training_stats = {
    'total': len(_all_scenarios_tls),
    'completed': 0,
    'failed': 0,
    'total_steps': 0,
}

try:
    tl_index = 0
    
    for scenario_name in sorted(scenarios_order.keys()):
        tl_ids = scenarios_order[scenario_name]
        
        print("\n" + "#"*60)
        print(f"# 场景: {scenario_name}")
        print(f"# 信号交叉口数量: {len(tl_ids)}")
        print("#"*60)
        
        for tl_id in tl_ids:
            tl_index += 1
            
            # 使用新的在线训练函数
            success = online_train_single_tl(
                scenario_name=scenario_name,
                tl_id=tl_id,
                tl_index=tl_index,
                total_tls=training_stats['total']
            )
            
            if success:
                training_stats['completed'] += 1
            else:
                training_stats['failed'] += 1
            
            # 清理 GPU 内存
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        
        print(f"\n✓ 场景 {scenario_name} 的所有信号交叉口训练完成")
    
    print("\n" + "="*60)
    print("✓ 所有场景在线训练完成！")
    print("="*60)

except KeyboardInterrupt:
    print("\n" + "="*60)
    print("⚠️ 训练被用户中断")
    print("="*60)

except Exception as e:
    print("\n" + "="*60)
    print(f"✗ 训练出错: {e}")
    print("="*60)
    import traceback
    traceback.print_exc()

finally:
    # 确保清理仿真器
    cleanup_active_simulator()
    
    # 打印统计
    skipped = training_stats['total'] - training_stats['completed'] - training_stats['failed']
    print("\n" + "="*60)
    print("训练统计:")
    print(f"  - 总信号交叉口: {training_stats['total']}")
    print(f"  - 成功完成: {training_stats['completed']}")
    print(f"  - 失败: {training_stats['failed']}")
    print(f"  - 跳过: {skipped}")
    print("="*60)

# %%
### 检查训练后的权重是否被修改
import torch

print("检查微调后的权重...")
print("="*50)

# 获取 LoRA 模块的权重
lora_modules_with_weights = {}
for name, module in model.named_modules():
    if hasattr(module, 'lora_A') and hasattr(module, 'lora_B'):
        # 检查权重是否被修改（非零）
        A_norm = torch.norm(module.lora_A.default.weight if hasattr(module.lora_A, 'default') else module.lora_A.weight).item()
        B_norm = torch.norm(module.lora_B.default.weight if hasattr(module.lora_B, 'default') else module.lora_B.weight).item()
        
        if A_norm > 0 or B_norm > 0:
            lora_modules_with_weights[name] = (A_norm, B_norm)
            print(f"✓ {name}")
            print(f"  - lora_A norm: {A_norm:.6f}")
            print(f"  - lora_B norm: {B_norm:.6f}")

if not lora_modules_with_weights:
    print("⚠️  警告: 没有找到非零的 LoRA 权重！")
else:
    print(f"\n总共找到 {len(lora_modules_with_weights)} 个有非零权重的 LoRA 模块")

print("="*50)

# ======================================================================
# ### 保存模型
# 
# ======================================================================

# ======================================================================
# ### HuggingFace 发布
# ======================================================================

# %%
model.save_pretrained_gguf("save_upload_model", tokenizer, quantization_method = "f16")

# %%
model.push_to_hub_gguf(
    "DavidRay93/Qwen3-4B-TSC-GRPO-Test",
    tokenizer,
    quantization_method=["f16"],
    token="YOUR_HUGGINGFACE_TOKEN_HERE",
    temporary_location="/root/autodl-tmp/saved_models",  # 指定保存和转换的文件夹路径
)

# %%
# 解析 training.log
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.font_manager as fm

# 设置中文字体（Ubuntu 系统）
# 尝试查找系统中可用的中文字体
available_fonts = [f.name for f in fm.fontManager.ttflist]
chinese_fonts = ['WenQuanYi Micro Hei', 'WenQuanYi Zen Hei', 'Noto Sans CJK SC', 
                 'Noto Sans CJK TC', 'Droid Sans Fallback', 'AR PL UMing CN', 
                 'SimHei', 'Microsoft YaHei']

# 选择第一个可用的中文字体
selected_font = None
for font in chinese_fonts:
    if font in available_fonts:
        selected_font = font
        break

USE_ENGLISH = False
if selected_font:
    rcParams['font.sans-serif'] = [selected_font]
    # print(f"✓ 使用中文字体: {selected_font}")
else:
    # 如果没有找到中文字体，使用英文标签
    print("⚠️ 未找到中文字体，将使用英文标签")
    USE_ENGLISH = True

rcParams['axes.unicode_minus'] = False

# 定义中英文标签字典
LABELS = {
    'step': 'Global Training Step' if USE_ENGLISH else '累积训练步数',
    'violation_count': 'Violation Count' if USE_ENGLISH else '违反约束的样本数',
    'violation_rate': 'Violation Rate (%)' if USE_ENGLISH else '违反约束的比例 (%)',
    'title_violation_count': 'Constraint Violations Over Training' if USE_ENGLISH else '约束违反数量随训练进行的变化',
    'title_violation_rate': 'Constraint Violation Rate Over Training' if USE_ENGLISH else '约束违反比例随训练进行的变化',
    'deviation_size': 'Deviation Size (seconds)' if USE_ENGLISH else '偏离值大小 (秒)',
    'sample_count': 'Sample Count' if USE_ENGLISH else '样本数量',
    'title_deviation_hist': 'Constraint Deviation Distribution (Histogram)' if USE_ENGLISH else '约束偏离值分布 (直方图)',
    'title_deviation_violin': 'Constraint Deviation Distribution (Box & Violin)' if USE_ENGLISH else '约束偏离值分布 (箱线图 + 小提琴图)',
    'mean': 'Mean' if USE_ENGLISH else '均值',
    'median': 'Median' if USE_ENGLISH else '中位数',
    'loss': 'Loss',
    'title_loss': 'Training Loss Over Time' if USE_ENGLISH else 'Training Loss 随训练进行的变化',
    'title_loss_stage': 'Loss Distribution by Training Stage' if USE_ENGLISH else '不同训练阶段的 Loss 分布',
    'stage': 'Training Stage' if USE_ENGLISH else '训练阶段',
    'early': 'Early\n(0-33%)' if USE_ENGLISH else '前期\n(0-33%)',
    'mid': 'Mid\n(33-66%)' if USE_ENGLISH else '中期\n(33-66%)',
    'late': 'Late\n(66-100%)' if USE_ENGLISH else '后期\n(66-100%)',
    'original_loss': 'Original Loss' if USE_ENGLISH else '原始 Loss',
    'smoothed_loss': 'Moving Average' if USE_ENGLISH else '移动平均',
}

log_file = 'training.log'

# 解析数据
debug_data = []  # 存储 bounds_deviation_sec 数据
loss_data = []   # 存储 loss 数据

with open(log_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 第一遍：解析训练组合和累积 step
i = 0
sample_count = 0
current_combination_idx = 0  # 当前训练组合编号（从 0 开始）
global_step_offset = 0  # 全局累积的 step 偏移量
max_step_in_combination = 10  # 每个训练组合的最大 step 数
current_scenario_tl = None  # 当前的 scenario/tl 组合

while i < len(lines):
    line = lines[i].strip()
    
    # 匹配新训练组合的开始: === [数字/数字] scenario/tl_id ===
    combo_match = re.search(r'===\s*\[(\d+)/\d+\]\s+([^/]+)/(\S+)\s+===', line)
    if combo_match:
        combo_num = int(combo_match.group(1))
        scenario = combo_match.group(2)
        tl_id = combo_match.group(3)
        new_scenario_tl = f"{scenario}/{tl_id}"
        
        # 如果是新的训练组合，更新偏移量
        if new_scenario_tl != current_scenario_tl and current_scenario_tl is not None:
            global_step_offset += max_step_in_combination
            current_combination_idx += 1
        
        current_scenario_tl = new_scenario_tl
    
    # 匹配 DEBUG 行: [DEBUG step=X gen=Y]
    debug_match = re.search(r'\[DEBUG step=(\d+) gen=(\d+)\]', line)
    if debug_match:
        local_step = int(debug_match.group(1))
        gen = int(debug_match.group(2))
        global_step = global_step_offset + local_step  # 累积的全局 step
        sample_count += 1
        
        # 下一行应该包含 bounds_deviation_sec
        if i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            dev_match = re.search(r'bounds_deviation_sec=([\d.]+)', next_line)
            if dev_match:
                deviation = float(dev_match.group(1))
                debug_data.append({
                    'sample_idx': sample_count,
                    'local_step': local_step,
                    'global_step': global_step,
                    'combination_idx': current_combination_idx,
                    'scenario_tl': current_scenario_tl,
                    'gen': gen,
                    'bounds_deviation_sec': deviation
                })
    
    # 匹配 loss 行: [scenario/tl] step X/Y loss=
    loss_match = re.search(r'\[([^\]]+)\]\s+step\s+(\d+)/\d+\s+loss=([-\d.]+)', line)
    if loss_match:
        scenario_tl = loss_match.group(1)
        local_step = int(loss_match.group(2))
        loss_val = float(loss_match.group(3))
        
        # 计算 global_step（使用当前的偏移量）
        global_step = global_step_offset + local_step
        
        loss_data.append({
            'local_step': local_step,
            'global_step': global_step,
            'combination_idx': current_combination_idx,
            'scenario_tl': scenario_tl,
            'loss': loss_val
        })
    
    i += 1

# 转为 DataFrame
df_debug = pd.DataFrame(debug_data)
df_loss = pd.DataFrame(loss_data)

print(f"✓ 解析完成")
print(f"  - 总样本数: {len(df_debug)}")
print(f"  - 训练组合数: {current_combination_idx + 1}")
print(f"  - 总训练步数记录: {len(df_loss)}")
if len(df_debug) > 0:
    print(f"  - 累积训练步数范围: {df_debug['global_step'].min():.0f} - {df_debug['global_step'].max():.0f}")
print(f"  - bounds_deviation_sec 不为0的样本数: {(df_debug['bounds_deviation_sec'] > 0).sum()}")
print(f"  - 违反约束比例: {(df_debug['bounds_deviation_sec'] > 0).sum() / len(df_debug) * 100:.2f}%")

# 显示前几个组合的信息
if len(df_debug) > 0:
    print(f"\n前几个训练组合:")
    for idx in range(min(5, current_combination_idx + 1)):
        combo_data = df_debug[df_debug['combination_idx'] == idx]
        if len(combo_data) > 0:
            scenario_tl = combo_data.iloc[0]['scenario_tl']
            step_range = f"{combo_data['global_step'].min():.0f}-{combo_data['global_step'].max():.0f}"
            print(f"  [{idx}] {scenario_tl}: global_step {step_range}")

# %%
# 图1: 约束违反数量随训练进行的变化（时间序列图）
# 按 global_step 分组，统计每个 step 中违反约束的样本数量

if len(df_debug) > 0:
    # 计算每个 global_step 的违反数量和总数量
    step_stats = df_debug.groupby('global_step').agg({
        'bounds_deviation_sec': [
            ('violation_count', lambda x: (x > 0).sum()),
            ('total_count', 'count'),
            ('violation_rate', lambda x: (x > 0).sum() / len(x) * 100)
        ]
    }).reset_index()
    
    # 简化列名
    step_stats.columns = ['global_step', 'violation_count', 'total_count', 'violation_rate']
    
    # 绘图
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # 子图1: 违反约束的样本数量
    ax1.plot(step_stats['global_step'], step_stats['violation_count'], 
             marker='o', linewidth=2, markersize=4, color='#e74c3c')
    ax1.fill_between(step_stats['global_step'], 0, step_stats['violation_count'], 
                      alpha=0.3, color='#e74c3c')
    ax1.set_xlabel(LABELS['step'], fontsize=12)
    ax1.set_ylabel(LABELS['violation_count'], fontsize=12)
    ax1.set_title(LABELS['title_violation_count'], fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(left=0)
    ax1.set_ylim(bottom=0)
    
    # 子图2: 违反约束的比例 (%)
    ax2.plot(step_stats['global_step'], step_stats['violation_rate'], 
             marker='s', linewidth=2, markersize=4, color='#3498db')
    ax2.fill_between(step_stats['global_step'], 0, step_stats['violation_rate'], 
                      alpha=0.3, color='#3498db')
    ax2.set_xlabel(LABELS['step'], fontsize=12)
    ax2.set_ylabel(LABELS['violation_rate'], fontsize=12)
    ax2.set_title(LABELS['title_violation_rate'], fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(left=0)
    ax2.set_ylim(bottom=0, top=100)
    
    plt.tight_layout()
    plt.savefig('analysis_violation_timeseries.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    print(f"✓ 时间序列图已保存为: analysis_violation_timeseries.png")
    print(f"  累积训练步数范围: 0 - {step_stats['global_step'].max():.0f}")
else:
    print("⚠️ 没有数据可绘制")

