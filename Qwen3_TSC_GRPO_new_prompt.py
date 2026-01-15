# -*- coding: utf-8 -*-
# 从 Qwen3_TSC_GRPO_new_prompt.ipynb 自动转换

# ======================================================================
# ### TSC GRPO 训练 - new_prompt_training JSON 协议（保留仿真回溯评估）
# 
# 
# ======================================================================

# %%
import os
os.environ["UNSLOTH_USE_MODELSCOPE"] = "1"


# %%
import subprocess
result = subprocess.run('bash -c "source /etc/network_turbo && env | grep proxy"', shell=True, capture_output=True, text=True)
for line in result.stdout.splitlines():
    if '=' in line:
        var, value = line.split('=', 1)
        os.environ[var] = value


# ======================================================================
# ### 加载模型
# 
# 
# ======================================================================

# %%
from unsloth import FastLanguageModel
import torch
import os

max_seq_length = 2048  # 增加序列长度以容纳完整的 prompt + completion
lora_rank = 32

os.environ["HF_HOME"] = 'model'
os.environ["MODELSCOPE_CACHE"] = 'model'

# ====== 断点续训：有 checkpoint 就继续微调；没有就从 base 模型开始 ======
BASE_MODEL_DIR = "model/models/qwen3-4B-SFT"
CHECKPOINT_DIR = "checkpoints/newprompt_grpo_latest"

def _looks_like_checkpoint(path: str) -> bool:
    if not os.path.isdir(path):
        return False
    # PEFT/LoRA 常见标志文件（任意一个即可认为可加载）
    marker_files = [
        "adapter_config.json",
        "adapter_model.safetensors",
        "adapter_model.bin",
        "config.json",
    ]
    return any(os.path.isfile(os.path.join(path, f)) for f in marker_files)

resume_from = CHECKPOINT_DIR if _looks_like_checkpoint(CHECKPOINT_DIR) else BASE_MODEL_DIR
if resume_from == CHECKPOINT_DIR:
    print(f"✓ 检测到 checkpoint，将从此继续微调: {CHECKPOINT_DIR}")
else:
    print(f"ℹ 未检测到 checkpoint，将从基础模型开始: {BASE_MODEL_DIR}")

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = resume_from,
    max_seq_length = max_seq_length,
    load_in_4bit = False,
    fast_inference = False,
    max_lora_rank = lora_rank,
    gpu_memory_utilization = 0.8,
)

# 若是从 base 模型开始，需要创建 LoRA；若是从 checkpoint 加载，一般已包含 LoRA（无需重复包一层）
if resume_from == BASE_MODEL_DIR:
    model = FastLanguageModel.get_peft_model(
        model,
        r = lora_rank,
        target_modules = [
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj",
        ],
        lora_alpha = lora_rank * 2,
        use_gradient_checkpointing = "unsloth",
        random_state = 3407,
    )
else:
    # 尽量开启梯度检查点（如果当前模型类型支持）
    try:
        model.gradient_checkpointing_enable()
    except Exception:
        pass

    # 保险：有些版本从 checkpoint 加载后 LoRA 参数可能默认不可训练
    _trainable = [p for p in model.parameters() if p.requires_grad]
    if len(_trainable) == 0:
        for name, p in model.named_parameters():
            if "lora" in name.lower():
                p.requires_grad = True
        print("⚠️ checkpoint 加载后未检测到可训练参数，已强制启用 LoRA 参数训练")


# ======================================================================
# ### 场景发现 & 仿真器
# 
# 
# ======================================================================

# %%
import json
import random
import sys
import xml.etree.ElementTree as ET
from collections import deque
from typing import Dict, List, Tuple


def discover_environments(environments_root: str) -> Dict[str, Dict]:
    environments: Dict[str, Dict] = {}
    if not os.path.isdir(environments_root):
        print(f"警告: environments 目录不存在: {environments_root}")
        return environments

    for scenario_name in sorted(os.listdir(environments_root)):
        scenario_dir = os.path.join(environments_root, scenario_name)
        if not os.path.isdir(scenario_dir) or scenario_name.startswith('.'):
            continue

        sumocfg = None
        for f in os.listdir(scenario_dir):
            if f.endswith('.sumocfg'):
                sumocfg = os.path.join(scenario_dir, f)
                break

        net_xml = None
        for f in os.listdir(scenario_dir):
            if f.endswith('.net.xml'):
                net_xml = os.path.join(scenario_dir, f)
                break

        if sumocfg and net_xml:
            tl_ids = extract_traffic_light_ids(net_xml)
            if tl_ids:
                environments[scenario_name] = {
                    'sumocfg': sumocfg,
                    'net': net_xml,
                    'tl_ids': tl_ids,
                }

    return environments


def extract_traffic_light_ids(net_xml_path: str) -> List[str]:
    tl_ids: List[str] = []
    try:
        for _event, elem in ET.iterparse(net_xml_path, events=("end",)):
            if elem.tag == "tlLogic":
                tl_id = elem.attrib.get("id")
                if tl_id and tl_id not in tl_ids:
                    tl_ids.append(tl_id)
                elem.clear()
    except Exception as e:
        print(f"解析 {net_xml_path} 失败: {e}")
    return tl_ids


ENVIRONMENTS_ROOT = os.path.join(os.getcwd(), 'sumo_simulation/environments')
AVAILABLE_ENVIRONMENTS = discover_environments(ENVIRONMENTS_ROOT)
print(f"发现场景数: {len(AVAILABLE_ENVIRONMENTS)}")
total_intersections = sum(len(env['tl_ids']) for env in AVAILABLE_ENVIRONMENTS.values())
print(f"总交叉口数量: {total_intersections}")

# 添加 sumo_simulation 目录到 Python 路径
sumo_sim_path = os.path.join(os.getcwd(), 'sumo_simulation')
if sumo_sim_path not in sys.path:
    sys.path.insert(0, sumo_sim_path)

from sumo_simulator import SUMOSimulator


# ======================================================================
# ### new_prompt 构造、解析、奖励（含回溯评估）
# 
# 
# ======================================================================

# %%
import datetime
import gc

from scu_tsc_newprompt.phase_parser import get_net_phase_minmax_one_based, get_phase_order_one_based
from scu_tsc_newprompt.constraint_sampler import sample_phase_limits_hybrid
from scu_tsc_newprompt.prompt_builder import build_cycle_predict_input_json, wrap_prompt_with_markers
from scu_tsc_newprompt.rewards import (
    score_constraints_and_format,
    AdaptiveScaler,
    compute_sim_reward_adaptive,
    compute_total_reward,
)


SYSTEM_PROMPT = """你是交通信号配时优化专家。
你将收到一个 JSON（用【cycle_predict_input_json】...【/cycle_predict_input_json】包裹）。
你的任务是：在满足硬约束前提下，输出下一周期各相位最终绿灯时间 final（单位：秒）。
注意：history 数据可能不完整（例如 only recent_cycles；yesterday_same_time/last_week_same_time 可能为 null），必须基于可用部分输出结果。
只输出最终 JSON 数组(list)，不要输出任何解释/过程。
"""

USER_INSTRUCTIONS = """任务（必须完成）：
1) 基于输入 JSON 的 history.* 历史数据，自行决定预测算法/模型/参数，预测“下一周期各相位需求强度”（仅在内部使用，不输出过程/中间值）。
2) 在满足硬约束前提下，输出下一周期各相位最终绿灯时间 final（单位：秒）。

要求（必须遵守）：
1) history 数据可能不完整（仅 recent_cycles；windows.yesterday_same_time / last_week_same_time 可能为 null）；这是正常情况，请基于可用部分完成预测，并且必须继续输出结果。
2) 若 history 中存在有效数据，请使用它完成预测并体现在结果中；不要忽略 history 数据随意分配。
3) 若 history 数据缺失/异常/几乎全为 0，仍需输出满足硬约束的可执行方案，但不得编造不存在的数据。
4) 只输出最终 JSON，不要输出任何解释/过程。

输出要求（必须严格遵守）：
1) 只输出最终 JSON（不要任何说明、不要 Markdown）。
2) JSON 顶层必须是数组(list)；数组长度必须等于相位数。
3) 数组元素必须为对象：{"phase_id": <int>, "final": <int>}；不允许输出其它字段。
4) phase_id 必须覆盖全部相位且不重复，并且顺序必须与 phase_order 完全一致。
"""


def build_user_prompt(payload: dict) -> str:
    return wrap_prompt_with_markers(payload) + "\n\n" + USER_INSTRUCTIONS


def collect_phase_waits_snapshot(simulator: SUMOSimulator, tl_id: str, phase_order: List[int]) -> List[dict]:
    """用当前时刻各相位 incoming lanes 的停止车辆数，作为 avg_wait 的代理。"""
    import traci

    waits = []
    for phase_id in phase_order:
        phase_idx = phase_id - 1
        lanes = simulator.get_phase_controlled_lanes(tl_id, phase_idx).get('incoming_lanes', [])
        if not lanes:
            avg = 0.0
        else:
            total = 0.0
            for ln in lanes:
                try:
                    total += traci.lane.getLastStepHaltingNumber(ln)
                except Exception:
                    pass
            avg = total / max(1, len(lanes))
        waits.append({'phase_id': int(phase_id), 'avg_wait': float(round(avg, 2))})
    return waits


def evaluate_plan_once(simulator: SUMOSimulator, tl_id: str, plan: List[dict]) -> dict:
    """执行一个整周期方案并返回指标（在当前仿真状态下直接前进）。"""
    import traci

    # 统一收集所有相位可能涉及的 incoming lanes（用于粗略 passed/queue 统计）
    phase_info = simulator.get_phase_info(tl_id)
    n = int(phase_info.get('num_phases', 0))
    all_lanes = set()
    for idx in range(n):
        all_lanes.update(simulator.get_phase_controlled_lanes(tl_id, idx).get('incoming_lanes', []))
    all_lanes = list(all_lanes)

    vehicles_before = set()
    for ln in all_lanes:
        try:
            vehicles_before.update(traci.lane.getLastStepVehicleIDs(ln))
        except Exception:
            pass

    total_queue_proxy = 0.0
    for step in plan:
        pid = int(step['phase_id'])
        dur = int(step['final'])
        traci.trafficlight.setPhase(tl_id, pid - 1)
        for _ in range(max(0, dur)):
            traci.simulationStep()
            q = 0.0
            for ln in all_lanes:
                try:
                    q += traci.lane.getLastStepHaltingNumber(ln)
                except Exception:
                    pass
            total_queue_proxy += q

    vehicles_after = set()
    queue_end = 0.0
    for ln in all_lanes:
        try:
            vehicles_after.update(traci.lane.getLastStepVehicleIDs(ln))
            queue_end += traci.lane.getLastStepHaltingNumber(ln)
        except Exception:
            pass

    passed = len(vehicles_before - vehicles_after)
    return {
        'passed_vehicles': float(passed),
        'queue_vehicles': float(queue_end),
        'total_queue_proxy': float(total_queue_proxy),
        'sim_time': float(traci.simulation.getTime()),
    }


def evaluate_multiple_plans_with_rollback(simulator: SUMOSimulator, tl_id: str, plans: List[List[dict]]) -> List[dict]:
    """对多个候选方案做回溯评估：同一检查点下逐个执行/恢复，最后回到原状态。"""
    state_file = simulator.save_simulation_state(tl_id)
    results = []
    try:
        for p in plans:
            simulator.restore_simulation_state(state_file)
            results.append(evaluate_plan_once(simulator, tl_id, p))
        simulator.restore_simulation_state(state_file)
    finally:
        simulator.cleanup_state_file(state_file)
    return results


# ======================================================================
# ### GRPO 训练（每步：构造 JSON prompt → 生成 N 个方案 → 回溯评估 → 更新 → 执行最优推进）
# 
# 
# ======================================================================

# %%
import torch.nn.functional as F
from torch.optim import AdamW
from transformers import get_cosine_schedule_with_warmup
import re
import sys

TRAIN_CONFIG = {
    'gui': False,
    'max_tl_per_scenario': 21,
    'warmup_steps': 80,
    'steps_per_tl': 10,
    'num_generations': 8,
    'learning_rate': 2e-6,
    'max_new_tokens': 256,
    'temperature': 1,
    'top_p': 0.95,
    'top_k': 50,
    'gradient_accumulation_steps': 8,
    'log_interval': 2,
    'clear_cache_interval': 5,
    # recent_cycles 窗口
    'recent_cycles_maxlen': 12,
    # ========== 新版 reward 配置 ==========
    # 仿真指标权重（归一化后加权）
    'w_passed': 1.0,      # 通过车辆数权重
    'w_queue': 1.0,       # 排队车辆数权重（负向）
    'w_proxy': 0.2,       # 累积排队权重（负向，辅助）
    # 总 reward 组合权重
    'w_sim': 1.5,         # 仿真 reward 权重
    'w_constraint': 1.5,  # 约束惩罚权重
    # 软约束归一化尺度（秒）
    'D0': 25.0,
    # 日志文件路径
    'log_file': 'training.log',
    # 跳过的交叉口 ID 列表（在所有场景中跳过这些 tl_id）
    'skip_tl_ids': ['nt12'],  # 例如: ['nt12', 'nt13', 'junction_abc']
    # 优先训练的场景列表（这些场景会优先排在训练队列前面）
    'priority_scenarios': ['cologne8', 'ingolstadt21'],  # 例如: ['cologne8', 'ingolstadt21', 'arterial4x4_1400']
}


# ========== 日志和训练跳过工具 ==========
class TeeLogger:
    """同时输出到控制台和文件的日志类"""
    def __init__(self, log_file):
        self.log_file = log_file
        self.terminal = sys.stdout
        # 以追加模式打开日志文件
        self.log = open(log_file, 'a', encoding='utf-8', buffering=1)
    
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
    
    def flush(self):
        self.terminal.flush()
        self.log.flush()
    
    def close(self):
        self.log.close()


def parse_completed_trainings(log_file: str) -> set:
    """
    解析 training.log，返回已完成训练的 (scenario, tl_id) 组合集合。
    
    判断标准：
    1. 找到 "=== [数字/数字] scenario/tl_id ===" 开始一个训练记录
    2. 在该记录后找到 "✓ checkpoint 已保存到" 确认训练完成
    """
    if not os.path.exists(log_file):
        return set()
    
    completed = set()
    current_pair = None
    
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            # 匹配训练开始行：=== [数字/数字] scenario/tl_id ===
            match_start = re.search(r'===\s*\[\d+/\d+\]\s+([^/]+)/(\S+)\s+===', line)
            if match_start:
                current_pair = (match_start.group(1), match_start.group(2))
                continue
            
            # 匹配 checkpoint 保存行：✓ checkpoint 已保存到
            if current_pair and '✓ checkpoint 已保存到' in line:
                completed.add(current_pair)
                current_pair = None
    
    return completed


def compute_grpo_loss(model, tokenizer, prompt_ids, completion_ids, rewards):
    device = next(model.parameters()).device
    
    # 截断 prompt 和 completion 以适应 max_seq_length
    max_len = max_seq_length
    prompt_len = prompt_ids.shape[1]
    completion_len = completion_ids.shape[1]
    total_len = prompt_len + completion_len
    
    if total_len > max_len:
        # 优先保留 completion，截断 prompt
        available_for_prompt = max(256, max_len - completion_len)  # 至少保留 256 个 prompt token
        if prompt_len > available_for_prompt:
            prompt_ids = prompt_ids[:, -available_for_prompt:]  # 保留 prompt 末尾
            prompt_len = available_for_prompt
        # 如果还是超长，截断 completion
        if prompt_len + completion_len > max_len:
            completion_ids = completion_ids[:, :max_len - prompt_len]
            completion_len = completion_ids.shape[1]
    
    input_ids = torch.cat([prompt_ids, completion_ids], dim=1).to(device)
    outputs = model(input_ids=input_ids)
    logits = outputs.logits

    # 确保维度匹配
    completion_logits = logits[:, prompt_len - 1 : prompt_len - 1 + completion_len, :]
    completion_targets = completion_ids.to(device)
    
    # 确保维度一致
    min_len = min(completion_logits.shape[1], completion_targets.shape[1])
    completion_logits = completion_logits[:, :min_len, :]
    completion_targets = completion_targets[:, :min_len]

    log_probs = F.log_softmax(completion_logits, dim=-1)
    token_log_probs = torch.gather(log_probs, 2, completion_targets.unsqueeze(-1)).squeeze(-1)

    attention_mask = (completion_targets != tokenizer.pad_token_id).float()
    seq_log_probs = (token_log_probs * attention_mask).sum(dim=1) / (attention_mask.sum(dim=1) + 1e-8)

    rewards_tensor = torch.tensor(rewards, dtype=torch.float32, device=device)
    
    # 防止 std=0 的情况（发生在所有 reward 相同时）
    if rewards_tensor.std() < 1e-6:
        # 所有 reward 相同时，给一个极小的随机扰动，避免 loss=0
        rewards_tensor = rewards_tensor + torch.randn_like(rewards_tensor) * 1e-4
    
    rewards_normalized = (rewards_tensor - rewards_tensor.mean()) / (rewards_tensor.std() + 1e-8)

    policy_loss = -(seq_log_probs * rewards_normalized).mean()

    return policy_loss, {
        'policy_loss': float(policy_loss.item()),
        'mean_reward': float(rewards_tensor.mean().item()),
        'reward_std': float(rewards_tensor.std().item()),
    }


def build_scenario_tl_list() -> List[Tuple[str, str]]:
    """构建训练组合列表，优先场景会排在前面"""
    priority_scenarios = set(TRAIN_CONFIG.get('priority_scenarios', []))
    
    priority_pairs: List[Tuple[str, str]] = []
    other_pairs: List[Tuple[str, str]] = []
    
    for scenario_name, info in AVAILABLE_ENVIRONMENTS.items():
        for tl_id in info['tl_ids'][: TRAIN_CONFIG['max_tl_per_scenario']]:
            pair = (scenario_name, tl_id)
            if scenario_name in priority_scenarios:
                priority_pairs.append(pair)
            else:
                other_pairs.append(pair)
    
    # 分别打乱优先和非优先场景的顺序
    random.shuffle(priority_pairs)
    random.shuffle(other_pairs)
    
    # 优先场景排在前面
    result = priority_pairs + other_pairs
    
    if priority_scenarios:
        print(f"✓ 优先场景: {list(priority_scenarios)}, 生成 {len(priority_pairs)} 个训练组合")
        print(f"  其他场景: {len(other_pairs)} 个训练组合")
    
    return result

def train_one_tl(scenario_name: str, tl_id: str) -> bool:
    env_info = AVAILABLE_ENVIRONMENTS[scenario_name]

    simulator = SUMOSimulator(
        config_file=env_info['sumocfg'],
        junctions_file=None,
        gui=TRAIN_CONFIG['gui'],
    )
    if not simulator.start_simulation():
        print(f"✗ 启动失败: {scenario_name}/{tl_id}")
        return False

    # warmup
    for _ in range(TRAIN_CONFIG['warmup_steps']):
        if simulator.is_connected():
            simulator.step()

    # phase order from net.xml (1-based)
    phase_order = get_phase_order_one_based(env_info['net'], tl_id)
    if not phase_order:
        print(f"✗ 未解析到相位: {scenario_name}/{tl_id}")
        simulator.close()
        return False

    net_minmax = get_net_phase_minmax_one_based(env_info['net'], tl_id)

    # history buffer: recent_cycles only
    recent_cycles_buf = deque(maxlen=TRAIN_CONFIG['recent_cycles_maxlen'])

    # 自适应尺度器（按路口维护 P95）
    scaler = AdaptiveScaler()
    
    # optimizer
    trainable_params = [p for p in model.parameters() if p.requires_grad]
    optimizer = AdamW(trainable_params, lr=TRAIN_CONFIG['learning_rate'], weight_decay=0.01)
    scheduler = get_cosine_schedule_with_warmup(
        optimizer,
        num_warmup_steps=int(TRAIN_CONFIG['steps_per_tl'] * 0.1),
        num_training_steps=TRAIN_CONFIG['steps_per_tl'],
    )
    optimizer.zero_grad()

    for step_idx in range(TRAIN_CONFIG['steps_per_tl']):
        if not simulator.is_connected():
            break

        # 随机化约束（每步变化），同一 (scenario, tl, step) 可复现
        rng = random.Random((hash(scenario_name) ^ hash(tl_id) ^ step_idx) & 0xFFFFFFFF)
        phase_limits = sample_phase_limits_hybrid(phase_order, net_minmax, rng=rng)

        payload = build_cycle_predict_input_json(
            scenario_name=scenario_name,
            tl_id=tl_id,
            phase_order=phase_order,
            phase_limits=phase_limits,
            recent_cycles=list(recent_cycles_buf),
            include_windows_recent_past=True,
            windows_recent_past=None,
        )

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(payload)},
        ]
        prompt_text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        prompt_ids = tokenizer(prompt_text, return_tensors="pt", add_special_tokens=False).input_ids

        device = next(model.parameters()).device
        prompt_ids_batch = prompt_ids.repeat(TRAIN_CONFIG['num_generations'], 1).to(device)

        # generate
        FastLanguageModel.for_inference(model)
        with torch.no_grad():
            generated = model.generate(
                input_ids=prompt_ids_batch,
                max_new_tokens=TRAIN_CONFIG['max_new_tokens'],
                temperature=TRAIN_CONFIG['temperature'],
                top_p=TRAIN_CONFIG['top_p'],
                top_k=TRAIN_CONFIG['top_k'],
                do_sample=True,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id,
            )
        completion_ids = generated[:, prompt_ids.shape[1] :].clone().detach()
        FastLanguageModel.for_training(model)
        completions = tokenizer.batch_decode(completion_ids, skip_special_tokens=True)

        # constraint score + parse（软约束检查，只检查 min_green/max_green）
        # 新版：约束分数在 [-1.5, 0] 范围（满足为 0，越违反越负）
        parsed_plans: List[List[dict] | None] = []
        constraint_scores: List[float] = []
        for i, txt in enumerate(completions):
            s, _info, plan = score_constraints_and_format(
                completion_text=txt,
                phase_order=phase_order,
                phase_limits=phase_limits,
                D0=TRAIN_CONFIG['D0'],
            )
            constraint_scores.append(float(s))
            parsed_plans.append(plan)
            
            # === 调试：每2 steps 打印所有 completion ===
            if step_idx % 2 == 0:
                print(f"\n[DEBUG step={step_idx} gen={i}] constraint_score={s:.2f} error={_info.get('error')}")
                print(f"  bounds_deviation_sec={_info.get('bounds_deviation_sec', 0):.1f}")
                print(f"  completion={repr(txt[:300])}")

        # 回溯仿真评估：只对“满足全部硬约束”的候选做回溯（省算力）
        plans_for_sim: List[List[dict]] = []
        sim_map: Dict[int, int] = {}
        for i, p in enumerate(parsed_plans):
            if p is not None:  # 只要 plan 解析成功就进行仿真评估（软约束）
                sim_map[i] = len(plans_for_sim)
                plans_for_sim.append(p)

        # 仿真评估：计算交通指标（使用自适应尺度 + 绝对指标）
        sim_rewards = [0.0] * len(completions)
        sim_results_all: List[Dict[str, float] | None] = [None] * len(completions)
        
        if plans_for_sim:
            sim_results = evaluate_multiple_plans_with_rollback(simulator, tl_id, plans_for_sim)
            
            # 更新自适应尺度器（用本轮评估结果）
            scaler.add_observations_batch(sim_results)
            
            # 异常检测：跳过未收集到有效数据的路口
            scales = scaler.get_scales()
            if scales == (1.0, 1.0, 1):
                print(f"⚠️ 警告: {scenario_name}/{tl_id} 未收集到有效仿真数据（scales未更新），跳过此路口")
                simulator.close()
                return False
            
            for i in sim_map:
                r = sim_results[sim_map[i]]
                sim_results_all[i] = r
                
                # 使用自适应尺度计算 sim_reward（绝对指标）
                sim_reward, _sim_info = compute_sim_reward_adaptive(
                    result=r,
                    scaler=scaler,
                    baseline_result=None,
                    w_passed=TRAIN_CONFIG['w_passed'],
                    w_queue=TRAIN_CONFIG['w_queue'],
                    w_proxy=TRAIN_CONFIG['w_proxy'],
                )
                sim_rewards[i] = float(sim_reward)

        # total reward = w_sim * sim_reward + w_constraint * constraint_score
        rewards = [
            compute_total_reward(
                constraint_score=constraint_scores[i],
                sim_reward=sim_rewards[i],
                w_sim=TRAIN_CONFIG['w_sim'],
                w_constraint=TRAIN_CONFIG['w_constraint'],
            )
            for i in range(len(completions))
        ]

        # GRPO update
        prompt_ids_for_loss = prompt_ids_batch.clone()
        completion_ids_for_loss = completion_ids.clone()
        loss, info = compute_grpo_loss(model, tokenizer, prompt_ids_for_loss, completion_ids_for_loss, rewards)
        (loss / TRAIN_CONFIG['gradient_accumulation_steps']).backward()

        if (step_idx + 1) % TRAIN_CONFIG['gradient_accumulation_steps'] == 0:
            torch.nn.utils.clip_grad_norm_(trainable_params, max_norm=1.0)
            optimizer.step()
            scheduler.step()
            optimizer.zero_grad()

        # 执行最优（推进单条真实轨迹）
        best_i = max(range(len(rewards)), key=lambda i: rewards[i])
        best_plan = parsed_plans[best_i]

        if best_plan is None:
            for _ in range(10):
                if simulator.is_connected():
                    simulator.step()
            # best_plan 无效时不更新 baseline
        else:
            waits = collect_phase_waits_snapshot(simulator, tl_id, phase_order)
            recent_cycles_buf.append(
                {
                    'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'phase_waits': waits,
                }
            )
            # 执行最优 plan
            evaluate_plan_once(simulator, tl_id, best_plan)

        if (step_idx + 1) % TRAIN_CONFIG['log_interval'] == 0:
            valid_plans = sum(1 for p in parsed_plans if p is not None)
            scales = scaler.get_scales()
            print(
                f"[{scenario_name}/{tl_id}] step {step_idx+1}/{TRAIN_CONFIG['steps_per_tl']} "
                f"loss={info['policy_loss']:.4f} mean_r={info['mean_reward']:.3f} std={info['reward_std']:.3f} "
                f"valid={valid_plans}/{len(parsed_plans)} "
                f"best_c={constraint_scores[best_i]:.2f} best_sim={sim_rewards[best_i]:.2f} "
                f"scales=({scales[0]:.1f},{scales[1]:.1f},{scales[2]:.0f})"
            )

        # cleanup
        del loss, generated, completion_ids_for_loss, prompt_ids_for_loss
        gc.collect()
        if torch.cuda.is_available() and (step_idx + 1) % TRAIN_CONFIG['clear_cache_interval'] == 0:
            torch.cuda.empty_cache()

    simulator.close()
    return True


pairs = build_scenario_tl_list()
print(f"训练组合数: {len(pairs)}")

# 先跑前若干个路口（避免一次训练过大）
MAX_TRAIN_TLS = 7000
import shutil
save_dir = "checkpoints/newprompt_grpo_latest"

# ========== 设置日志输出 ==========
log_file = TRAIN_CONFIG['log_file']
# 确保日志文件存在（不存在则创建空白文件）
if not os.path.exists(log_file):
    open(log_file, 'w', encoding='utf-8').close()
    print(f"✓ 创建新日志文件: {log_file}")
else:
    print(f"✓ 使用现有日志文件: {log_file}")

# 重定向 stdout 到 TeeLogger（同时输出到控制台和文件）
tee_logger = TeeLogger(log_file)
sys.stdout = tee_logger

# ========== 解析已完成的训练组合 ==========
completed_trainings = parse_completed_trainings(log_file)
print(f"已完成训练的组合数: {len(completed_trainings)}")
if completed_trainings:
    print(f"已完成的前几个: {list(completed_trainings)[:5]}")

# ========== 跳过列表配置 ==========
skip_tl_ids = set(TRAIN_CONFIG['skip_tl_ids'])
if skip_tl_ids:
    print(f"配置跳过的交叉口: {list(skip_tl_ids)}")

# ========== 主训练循环 ==========
skipped_count = 0
skipped_by_config_count = 0
trained_count = 0

for i, (sc, tl) in enumerate(pairs[:MAX_TRAIN_TLS], start=1):
    # 检查是否在配置的跳过列表中
    if tl in skip_tl_ids:
        print(f"\n⊘ 跳过 [{i}/{min(MAX_TRAIN_TLS, len(pairs))}] {sc}/{tl} (配置跳过)")
        skipped_by_config_count += 1
        continue
    
    # 检查是否已经训练过
    if (sc, tl) in completed_trainings:
        print(f"\n⊘ 跳过 [{i}/{min(MAX_TRAIN_TLS, len(pairs))}] {sc}/{tl} (已训练)")
        skipped_count += 1
        continue
    
    print(f"\n=== [{i}/{min(MAX_TRAIN_TLS, len(pairs))}] {sc}/{tl} ===")
    _ok = train_one_tl(sc, tl)
    trained_count += 1
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    
    # 每训练完一个交叉口保存一次 checkpoint（覆盖保存）
    if os.path.isdir(save_dir):
        shutil.rmtree(save_dir)
    os.makedirs(save_dir, exist_ok=True)
    model.save_pretrained(save_dir)
    print(f"✓ checkpoint 已保存到 {save_dir} (完成 {trained_count}/{min(MAX_TRAIN_TLS, len(pairs))} 个交叉口)")

# ========== 训练结束，输出统计 ==========
print(f"\n{'='*60}")
print(f"训练完成！")
print(f"  本次训练: {trained_count} 个交叉口")
print(f"  跳过 (配置): {skipped_by_config_count} 个交叉口")
print(f"  跳过 (已训练): {skipped_count} 个交叉口")
print(f"  总计: {len(completed_trainings) + trained_count} 个交叉口已完成")
print(f"{'='*60}")

# 恢复 stdout 并关闭日志文件
sys.stdout = tee_logger.terminal
tee_logger.close()
print("✓ 日志已保存")


# ======================================================================
# ## 存为GGUF
# ======================================================================

# %%
# 导入必要的库
import os
import torch
from unsloth import FastLanguageModel

# 设置环境变量
os.environ["HF_HOME"] = 'model'
os.environ["MODELSCOPE_CACHE"] = 'model'
os.environ["UNSLOTH_USE_MODELSCOPE"] = "1"

# 配置参数
max_seq_length = 2048  # 与训练时保持一致
lora_rank = 32
checkpoint_path = "checkpoints/newprompt_grpo_latest"
base_model_path = "model/models/qwen3-4B-SFT"
output_path = "save_upload_model"
merged_path = "save_upload_model_merged"  # 先保存 merged 模型

print("正在从 checkpoint 加载模型（包含 LoRA）...")
# ========== 方法：直接从 checkpoint 加载（推荐）==========
# checkpoint 已经包含完整的 LoRA 配置，直接加载即可
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = checkpoint_path,  # 直接加载 checkpoint
    max_seq_length = max_seq_length,
    load_in_4bit = False,
    fast_inference = False,
    max_lora_rank = lora_rank,
)

print("✓ 模型加载完成！")
print(f"正在 merge LoRA 权重并保存到 {merged_path}...")

# ========== Step 1: Merge LoRA 权重到 base 模型 ==========
model = model.merge_and_unload()  # 将 LoRA 权重合并到 base 模型
print("✓ LoRA 权重已 merge")

# ========== Step 2: 保存 merged 模型为 HF 格式 ==========
model.save_pretrained(merged_path)
tokenizer.save_pretrained(merged_path)
print(f"✓ Merged 模型已保存到: {merged_path}")

# ========== Step 3: 转换为 GGUF（不需要网络）==========
print(f"\n正在转换为 GGUF 格式到 {output_path}...")
print("提示：如果仍然遇到网络问题，可以手动使用 llama.cpp 转换")

try:
    # 重新加载 merged 模型用于 GGUF 转换
    model_for_gguf, _ = FastLanguageModel.from_pretrained(
        model_name = merged_path,
        max_seq_length = max_seq_length,
        load_in_4bit = False,
        fast_inference = False,
    )
    
    model_for_gguf.save_pretrained_gguf(output_path, tokenizer, quantization_method="f16")
    print(f"\n✓ 模型已成功保存为 GGUF 格式到: {output_path}")
    
except Exception as e:
    print(f"\n⚠️ GGUF 转换失败: {e}")
    print(f"\n但不用担心！Merged 模型已保存到: {merged_path}")
    print("\n你可以使用以下方式手动转换为 GGUF：")
    print("方法1: 使用 llama.cpp (如果已安装)")
    print(f"  python /path/to/llama.cpp/convert_hf_to_gguf.py {merged_path} --outfile {output_path}/model.gguf --outtype f16")
    print("\n方法2: 在有网络的环境重新运行 GGUF 转换")
    print("\n方法3: 直接使用 HF 格式模型（ollama 和大多数工具都支持）")

print("\n" + "="*60)
print("保存完成！")
print(f"  - HF 格式 (merged): {merged_path}")
print(f"  - GGUF 格式: {output_path} (如果转换成功)")
print("="*60)

# python llama.cpp/convert_hf_to_gguf.py save_upload_model_merged --outfile save_upload_model/model.gguf --outtype f16

# ======================================================================
# ## 训练统计
# ======================================================================

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
# 图1: 约束违反比例随训练进行的变化（改进版 - 按交叉口汇总 + 移动平均）
# 问题：每个 step 只有 8 个样本，粒度太细看不出趋势
# 改进：1) 按训练组合（交叉口）汇总  2) 添加移动平均  3) 添加阶段对比

if len(df_debug) > 0:
    # ===== 方法1: 按训练组合（交叉口）汇总 =====
    # 每个交叉口有约 40 个样本（5个记录步骤 × 8个生成），更能反映真实趋势
    combo_stats = df_debug.groupby('combination_idx').agg({
        'bounds_deviation_sec': [
            ('violation_count', lambda x: (x > 0).sum()),
            ('total_count', 'count'),
            ('violation_rate', lambda x: (x > 0).sum() / len(x) * 100),
            ('mean_deviation', lambda x: x[x > 0].mean() if (x > 0).any() else 0)
        ],
        'scenario_tl': 'first'
    }).reset_index()
    combo_stats.columns = ['combination_idx', 'violation_count', 'total_count', 
                            'violation_rate', 'mean_deviation', 'scenario_tl']
    
    # 绘图 - 3 行布局
    fig, axes = plt.subplots(3, 1, figsize=(14, 14))
    
    # ===== 子图1: 按交叉口的违反比例 + 移动平均 =====
    ax1 = axes[0]
    
    # 原始数据（散点）
    ax1.scatter(combo_stats['combination_idx'], combo_stats['violation_rate'], 
                alpha=0.3, s=20, color='#e74c3c', label='每个交叉口')
    
    # 移动平均线（关键！）
    window_size = max(20, len(combo_stats) // 20)  # 动态窗口大小
    combo_stats_sorted = combo_stats.sort_values('combination_idx')
    combo_stats_sorted['violation_rate_smooth'] = combo_stats_sorted['violation_rate'].rolling(
        window=window_size, center=True, min_periods=1).mean()
    
    ax1.plot(combo_stats_sorted['combination_idx'], combo_stats_sorted['violation_rate_smooth'], 
             linewidth=3, color='#c0392b', label=f'移动平均 (窗口={window_size})')
    
    ax1.set_xlabel('训练交叉口编号' if not USE_ENGLISH else 'Intersection Index', fontsize=12)
    ax1.set_ylabel(LABELS['violation_rate'], fontsize=12)
    ax1.set_title('约束违反比例随训练进行的变化（按交叉口汇总）' if not USE_ENGLISH else 
                  'Constraint Violation Rate Over Training (Per Intersection)', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10, loc='upper right')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(left=0)
    ax1.set_ylim(bottom=0, top=100)
    
    # ===== 子图2: 平均偏离值（仅违反样本）随训练的变化 =====
    ax2 = axes[1]
    
    # 筛选有违反的交叉口
    combo_with_violation = combo_stats[combo_stats['mean_deviation'] > 0]
    
    ax2.scatter(combo_with_violation['combination_idx'], combo_with_violation['mean_deviation'], 
                alpha=0.4, s=25, color='#e67e22', label='每个交叉口的平均偏离')
    
    # 移动平均
    if len(combo_with_violation) > window_size:
        combo_with_violation_sorted = combo_with_violation.sort_values('combination_idx')
        combo_with_violation_sorted['deviation_smooth'] = combo_with_violation_sorted['mean_deviation'].rolling(
            window=window_size, center=True, min_periods=1).mean()
        ax2.plot(combo_with_violation_sorted['combination_idx'], combo_with_violation_sorted['deviation_smooth'], 
                 linewidth=3, color='#d35400', label=f'移动平均 (窗口={window_size})')
    
    ax2.set_xlabel('训练交叉口编号' if not USE_ENGLISH else 'Intersection Index', fontsize=12)
    ax2.set_ylabel('平均偏离值 (秒)' if not USE_ENGLISH else 'Mean Deviation (seconds)', fontsize=12)
    ax2.set_title('约束偏离严重程度随训练的变化' if not USE_ENGLISH else 
                  'Constraint Deviation Severity Over Training', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10, loc='upper right')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(left=0)
    
    # ===== 子图3: 按训练阶段的箱线图对比 =====
    ax3 = axes[2]
    
    # 将训练过程分为前、中、后三个阶段
    n = len(combo_stats)
    stage_1_rates = combo_stats.iloc[:n//3]['violation_rate']
    stage_2_rates = combo_stats.iloc[n//3:2*n//3]['violation_rate']
    stage_3_rates = combo_stats.iloc[2*n//3:]['violation_rate']
    
    positions = [1, 2, 3]
    data_to_plot = [stage_1_rates, stage_2_rates, stage_3_rates]
    labels = [LABELS['early'], LABELS['mid'], LABELS['late']]
    colors = ['#3498db', '#f39c12', '#2ecc71']
    
    bp = ax3.boxplot(data_to_plot, positions=positions, widths=0.6,
                     patch_artist=True, labels=labels,
                     showmeans=True, meanline=True)
    
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax3.set_ylabel(LABELS['violation_rate'], fontsize=12)
    ax3.set_xlabel(LABELS['stage'], fontsize=12)
    ax3.set_title('不同训练阶段的约束违反比例对比' if not USE_ENGLISH else 
                  'Constraint Violation Rate by Training Stage', fontsize=14, fontweight='bold')
    ax3.grid(True, alpha=0.3, axis='y')
    
    # 添加统计文本
    early_mean = stage_1_rates.mean()
    mid_mean = stage_2_rates.mean()
    late_mean = stage_3_rates.mean()
    
    stats_text = (f'Early mean: {early_mean:.1f}%\n'
                  f'Mid mean: {mid_mean:.1f}%\n'
                  f'Late mean: {late_mean:.1f}%')
    ax3.text(0.02, 0.98, stats_text, transform=ax3.transAxes,
            fontsize=11, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    # 趋势判断
    if late_mean < early_mean * 0.9:
        trend = "📉 下降趋势 (改善)"
        trend_color = 'green'
    elif late_mean > early_mean * 1.1:
        trend = "📈 上升趋势 (恶化)"
        trend_color = 'red'
    else:
        trend = "➡️ 基本持平"
        trend_color = 'orange'
    
    ax3.text(0.98, 0.98, f'整体趋势: {trend}' if not USE_ENGLISH else f'Trend: {trend}', 
             transform=ax3.transAxes, fontsize=12, verticalalignment='top', 
             horizontalalignment='right', color=trend_color, fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('analysis_violation_timeseries.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # 打印详细统计
    print(f"✓ 改进版时间序列图已保存为: analysis_violation_timeseries.png")
    print(f"\n📊 统计摘要:")
    print(f"  训练交叉口总数: {len(combo_stats)}")
    print(f"  整体违反比例: {combo_stats['violation_rate'].mean():.1f}% ± {combo_stats['violation_rate'].std():.1f}%")
    print(f"\n📈 各阶段违反比例均值:")
    print(f"  前期 (0-33%):   {early_mean:.1f}% (样本数: {len(stage_1_rates)})")
    print(f"  中期 (33-66%):  {mid_mean:.1f}% (样本数: {len(stage_2_rates)})")
    print(f"  后期 (66-100%): {late_mean:.1f}% (样本数: {len(stage_3_rates)})")
    print(f"\n  {'✅ 约束违反比例随训练下降' if late_mean < early_mean else '⚠️ 约束违反比例随训练上升或持平'}")
    
else:
    print("⚠️ 没有数据可绘制")

# %%
# 图2: bounds_deviation_sec 不为0的偏离值大小分布
if len(df_debug) > 0:
    # 筛选出不为0的偏离值
    violations = df_debug[df_debug['bounds_deviation_sec'] > 0]['bounds_deviation_sec']
    
    if len(violations) > 0:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # 子图1: 直方图
        ax1.hist(violations, bins=50, color='#e67e22', alpha=0.7, edgecolor='black')
        ax1.set_xlabel(LABELS['deviation_size'], fontsize=12)
        ax1.set_ylabel(LABELS['sample_count'], fontsize=12)
        ax1.set_title(LABELS['title_deviation_hist'], fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # 添加统计信息
        mean_val = violations.mean()
        median_val = violations.median()
        max_val = violations.max()
        ax1.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'{LABELS["mean"]}: {mean_val:.1f}s')
        ax1.axvline(median_val, color='blue', linestyle='--', linewidth=2, label=f'{LABELS["median"]}: {median_val:.1f}s')
        ax1.legend(fontsize=10)
        
        # 子图2: 箱线图 + 小提琴图
        parts = ax2.violinplot([violations], positions=[0], widths=0.7,
                                showmeans=True, showmedians=True)
        for pc in parts['bodies']:
            pc.set_facecolor('#9b59b6')
            pc.set_alpha(0.6)
        
        ax2.boxplot([violations], positions=[0], widths=0.3, 
                    patch_artist=True,
                    boxprops=dict(facecolor='#3498db', alpha=0.7),
                    medianprops=dict(color='red', linewidth=2))
        
        ax2.set_ylabel(LABELS['deviation_size'], fontsize=12)
        ax2.set_title(LABELS['title_deviation_violin'], fontsize=14, fontweight='bold')
        ax2.set_xticks([0])
        ax2.set_xticklabels(['bounds_deviation_sec'])
        ax2.grid(True, alpha=0.3, axis='y')
        
        # 添加统计文本（使用英文以避免字体问题）
        stats_text = f'Samples: {len(violations)}\nMean: {mean_val:.2f}s\nMedian: {median_val:.2f}s\nMax: {max_val:.2f}s\nMin: {violations.min():.2f}s'
        ax2.text(0.5, 0.95, stats_text, transform=ax2.transAxes,
                fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        plt.savefig('analysis_deviation_distribution.png', dpi=150, bbox_inches='tight')
        plt.show()
        
        print(f"✓ 分布图已保存为: analysis_deviation_distribution.png")
        print(f"\n统计摘要:")
        print(f"  - 违反约束样本数: {len(violations)}")
        print(f"  - 均值: {mean_val:.2f} 秒")
        print(f"  - 中位数: {median_val:.2f} 秒")
        print(f"  - 标准差: {violations.std():.2f} 秒")
        print(f"  - 最小值: {violations.min():.2f} 秒")
        print(f"  - 最大值: {max_val:.2f} 秒")
        print(f"  - 25%分位数: {violations.quantile(0.25):.2f} 秒")
        print(f"  - 75%分位数: {violations.quantile(0.75):.2f} 秒")
    else:
        print("✓ 所有样本都满足约束条件 (bounds_deviation_sec = 0)")
else:
    print("⚠️ 没有数据可绘制")

# %%
# 图3: Training Loss 随训练进行的变化
if len(df_loss) > 0:
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # 子图1: 原始 Loss（使用 global_step）
    ax1.plot(df_loss['global_step'], df_loss['loss'], 
             linewidth=1.5, alpha=0.6, color='gray', label=LABELS['original_loss'])
    
    # 添加移动平均线（平滑）
    if len(df_loss) >= 10:
        window_size = min(20, len(df_loss) // 5)
        # 按 global_step 排序后再计算移动平均
        df_loss_sorted = df_loss.sort_values('global_step')
        df_loss_sorted['loss_smooth'] = df_loss_sorted['loss'].rolling(window=window_size, center=True).mean()
        ax1.plot(df_loss_sorted['global_step'], df_loss_sorted['loss_smooth'], 
                linewidth=2.5, color='#e74c3c', label=f'{LABELS["smoothed_loss"]} (window={window_size})')
    
    ax1.set_xlabel(LABELS['step'], fontsize=12)
    ax1.set_ylabel(LABELS['loss'], fontsize=12)
    ax1.set_title(LABELS['title_loss'], fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(left=0)
    
    # 子图2: Loss 的分布（按训练阶段）
    # 将训练过程分为前、中、后三个阶段
    n = len(df_loss)
    stage_1 = df_loss.iloc[:n//3]['loss']
    stage_2 = df_loss.iloc[n//3:2*n//3]['loss']
    stage_3 = df_loss.iloc[2*n//3:]['loss']
    
    positions = [1, 2, 3]
    data_to_plot = [stage_1, stage_2, stage_3]
    labels = [LABELS['early'], LABELS['mid'], LABELS['late']]
    colors = ['#3498db', '#f39c12', '#2ecc71']
    
    bp = ax2.boxplot(data_to_plot, positions=positions, widths=0.6,
                     patch_artist=True, labels=labels,
                     showmeans=True, meanline=True)
    
    # 设置颜色
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax2.set_ylabel(LABELS['loss'], fontsize=12)
    ax2.set_xlabel(LABELS['stage'], fontsize=12)
    ax2.set_title(LABELS['title_loss_stage'], fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # 添加统计文本（使用英文以避免字体问题）
    stats_text = (f'Early mean: {stage_1.mean():.4f}\n'
                  f'Mid mean: {stage_2.mean():.4f}\n'
                  f'Late mean: {stage_3.mean():.4f}')
    ax2.text(0.02, 0.98, stats_text, transform=ax2.transAxes,
            fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('analysis_loss_timeseries.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    print(f"✓ Loss 时间序列图已保存为: analysis_loss_timeseries.png")
    print(f"  累积训练步数范围: 0 - {df_loss['global_step'].max():.0f}")
    print(f"\nLoss 统计摘要:")
    print(f"  - 记录数: {len(df_loss)}")
    print(f"  - 整体均值: {df_loss['loss'].mean():.4f}")
    print(f"  - 整体标准差: {df_loss['loss'].std():.4f}")
    print(f"  - 最小值: {df_loss['loss'].min():.4f}")
    print(f"  - 最大值: {df_loss['loss'].max():.4f}")
    print(f"  - 前期均值: {stage_1.mean():.4f}")
    print(f"  - 中期均值: {stage_2.mean():.4f}")
    print(f"  - 后期均值: {stage_3.mean():.4f}")
else:
    print("⚠️ 没有 Loss 数据可绘制")

