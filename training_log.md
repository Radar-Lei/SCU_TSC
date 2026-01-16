
============================================================
Training Run: 2026-01-16 10:11:32
============================================================

[publish] 构建镜像 unsloth-tsc-grpo:latest
[publish] 基础镜像: nvcr.io/nvidia/pytorch:25.11-py3
[publish] 项目目录: /home/samuel/unsloth_dgx/workspace/SCU_TSC
#0 building with "default" instance using docker driver

#1 [internal] load build definition from Dockerfile
#1 DONE 0.0s

#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 2.97kB done
#1 DONE 0.0s

#2 [internal] load metadata for nvcr.io/nvidia/pytorch:25.11-py3
#2 DONE 0.0s

#3 [internal] load .dockerignore
#3 transferring context: 2B done
#3 DONE 0.0s

#4 [ 1/11] FROM nvcr.io/nvidia/pytorch:25.11-py3
#4 DONE 0.0s

#5 [internal] load build context
#5 transferring context: 35B done
#5 DONE 0.0s

#6 [ 6/11] RUN python -m pip install --no-cache-dir --no-deps --retries 20 --timeout 120 --resume-retries 50     unsloth     unsloth_zoo
#6 CACHED

#7 [ 8/11] RUN python -m pip install --no-cache-dir --retries 20 --timeout 120 --resume-retries 50 traci
#7 CACHED

#8 [ 4/11] RUN python -m pip install --no-cache-dir "pip==25.2"
#8 CACHED

#9 [ 9/11] WORKDIR /workspace
#9 CACHED

#10 [ 5/11] RUN python -m pip install --no-cache-dir --retries 20 --timeout 120 --resume-retries 50     transformers     peft     hf_transfer     "datasets==4.3.0"     "trl==0.26.1"     modelscope
#10 CACHED

#11 [ 3/11] RUN apt-get update &&     (apt-get install -y --no-install-recommends sumo sumo-tools ||      echo "Warning: SUMO packages not available, will rely on Python traci only") &&     rm -rf /var/lib/apt/lists/*
#11 CACHED

#12 [ 2/11] RUN apt-get update && apt-get install -y --no-install-recommends     software-properties-common     wget     ca-certificates     gnupg     lsb-release     libgl1     libglx-mesa0     && rm -rf /var/lib/apt/lists/*
#12 CACHED

#13 [10/11] COPY entrypoint.sh /usr/local/bin/entrypoint.sh
#13 CACHED

#14 [ 7/11] RUN python -m pip install --no-cache-dir --no-deps --retries 20 --timeout 120 --resume-retries 50 bitsandbytes ||     echo "Warning: bitsandbytes install failed on $(uname -m); continuing without bitsandbytes"
#14 CACHED

#15 [11/11] RUN chmod +x /usr/local/bin/entrypoint.sh
#15 CACHED

#16 exporting to image
#16 exporting layers done
#16 writing image sha256:9b8d3e0164635be1497ec400dae39fe93468154f196925d77a0f83a8809ad738 done
#16 naming to docker.io/library/unsloth-tsc-grpo:latest done
#16 DONE 0.0s
[publish] 镜像构建完成: unsloth-tsc-grpo:latest

============================================================
[publish] 运行配置:
  镜像: unsloth-tsc-grpo:latest
  容器名: unsloth-tsc-training
  GPU: all
  训练脚本: Qwen3_TSC_UnslothGRPO_TwoScenarios.py
  交互模式: 0
  后台运行: 0
  日志文件: /home/samuel/unsloth_dgx/workspace/SCU_TSC/training_log.md
============================================================

============================================================
Unsloth TSC GRPO Training Environment
============================================================
[entrypoint] 检查 SUMO 安装...
[entrypoint] SUMO 已安装: Eclipse SUMO sumo Version 1.18.0
[entrypoint] 检查 Python 依赖...
[entrypoint] PyTorch: 2.10.0a0+b558c986e8.nv25.11
[entrypoint] Transformers: 4.57.5
[entrypoint] TRL: 0.26.1
🦥 Unsloth: Will patch your computer to enable 2x faster free finetuning.
🦥 Unsloth Zoo will now patch everything to make training faster!
[entrypoint] Unsloth: OK
[entrypoint] CUDA: 13.0
[entrypoint] GPU: NVIDIA GB10
[entrypoint] GPU Memory: 119.7 GB
[entrypoint] traci: OK
[entrypoint] HF_HOME=/workspace/model
[entrypoint] 工作目录: /workspace

[entrypoint] 项目文件:
-rw-rw-r-- 1 ubuntu ubuntu 32202 Jan 15 12:09 /workspace/Qwen3_(4B)_GRPO.py
-rw-rw-r-- 1 ubuntu ubuntu 43464 Jan 15 12:09 /workspace/Qwen3_TSC_GRPO.py
-rw-rw-r-- 1 ubuntu ubuntu 54376 Jan 15 12:09 /workspace/Qwen3_TSC_GRPO_new_prompt.py
-rw-rw-r-- 1 ubuntu ubuntu  8741 Jan 15 12:09 /workspace/Qwen3_TSC_StandardGRPO.py
-rw-rw-r-- 1 ubuntu ubuntu  8081 Jan 16 02:11 /workspace/Qwen3_TSC_UnslothGRPO_TwoScenarios.py
-rw-rw-r-- 1 ubuntu ubuntu 29071 Jan 15 14:10 /workspace/generate_grpo_dataset.py
-rw-rw-r-- 1 ubuntu ubuntu 30556 Jan 15 15:22 /workspace/tsc_reward_function.py

============================================================
[entrypoint] 执行: python Qwen3_TSC_UnslothGRPO_TwoScenarios.py
============================================================

环境变量已设置
✓ Dataset 已存在: grpo_dataset_two_scenarios
🦥 Unsloth: Will patch your computer to enable 2x faster free finetuning.
🦥 Unsloth Zoo will now patch everything to make training faster!
ℹ 从基础模型开始: Qwen/Qwen2.5-0.5B-Instruct
Downloading Model from https://www.modelscope.cn to directory: model/models/unsloth/Qwen2.5-0.5B-Instruct
2026-01-16 02:11:48,186 - modelscope - INFO - Target directory already exists, skipping creation.
==((====))==  Unsloth 2026.1.2: Fast Qwen2 patching. Transformers: 4.57.5.
   \\   /|    NVIDIA GB10. Num GPUs = 1. Max memory: 119.698 GB. Platform: Linux.
O^O/ \_/ \    Torch: 2.10.0a0+b558c986e8.nv25.11. CUDA: 12.1. CUDA Toolkit: 13.0. Triton: 3.5.0
\        /    Bfloat16 = TRUE. FA [Xformers = None. FA2 = True]
 "-____-"     Free license: http://github.com/unslothai/unsloth
Unsloth: Fast downloading is enabled - ignore downloading bars which are red colored!
Unsloth 2026.1.2 patched 24 layers with 24 QKV layers, 24 O layers and 24 MLP layers.
✓ Dataset 加载成功: grpo_dataset_two_scenarios
样本数: 100
{'prompt': [{'content': '你是交通信号控制优化专家。【signal_step_input_json】{"crossing_id":735900497,"as_of":"2026-01-15 15:24:52","scenario":{"phase_ids":[1,3],"phase_lane_map":{"1":["458891623#6.319_1","458891623#6.319_2","458891623#6.319_3","458891623#6.319_0"],"3":["476664219#5_0","476664219#5_1"]}},"state":{"current_phase_id":3,"current_phase_elapsed_sec":12,"current_phase_planned_green_sec":22,"phase_metrics_now":[{"phase_id":1,"avg_queue_veh":0.0,"avg_passed_veh_in_current_green":0.0},{"phase_id":3,"avg_queue_veh":0.0,"avg_passed_veh_in_current_green":0.0}]}}【/signal_step_input_json】\n\n字段含义（仅说明含义）：\n* state.phase_metrics_now[*].avg_queue_veh：该相位在当前时刻的平均排队车辆数（辆）；可由该相位所控制车道的排队车辆数取平均得到。\n* state.phase_metrics_now[*].avg_passed_veh_in_current_green：该相位在"当前正在执行的绿灯相位"内至当前时刻累计通过车辆数（辆）；只有当前相位通常会 >0，非当前相位一般为 0。\n\n任务（必须完成）：\n1. 基于输入 JSON 的 scenario 与 state，自行决定决策策略/参数，评估各相位当前需求强度并做出"下一步动作"（仅在内部使用，不输出任何预测过程/中间值）。\n2. 输出：下一个信号相位 next_phase_id，以及该相位绿灯持续时间 green_sec（单位：秒）。\n\n要求（必须遵守）：\n1. 你必须显式利用 avg_queue_veh 与 passed_veh_in_current_green 来决策；不得无视输入随意给出答案。\n2. 在缺少任何额外硬约束（不提供 cycle_constraints / phase_order / phase_limits / history）的情况下：\n   * next_phase_id 必须来自 scenario.phase_ids；\n   * green_sec 必须为正整数秒；\n   * green_sec 必须"合理"：队列更大/通过更少的相位倾向给更长绿；队列更小/通过更多的相位倾向给更短绿；\n   * 若多相位需求接近，可优先切换到非当前相位以降低其他相位等待的累积风险。\n\n输出要求（必须严格遵守）：\n1. 只输出最终 JSON（不要任何说明、不要 Markdown、不要额外文本、不要输出推理过程）。\n2. JSON 必须为对象，且仅包含两个字段：\n   {"next_phase_id": <int>, "green_sec": <int>}\n3. 不允许输出其它字段。', 'role': 'user'}], 'state_path': 'grpo_states_two_scenarios/chengdu/1492574988_signal_step_0_t383.xml', 'scenario': 'chengdu', 'tl_id': '1492574988', 'task_type': 'signal_step', 'phase_ids': [1, 3], 'phase_lane_map': {'1': ['458891623#6.319_1', '458891623#6.319_2', '458891623#6.319_3', '458891623#6.319_0'], '3': ['476664219#5_0', '476664219#5_1']}, 'decision_lead_sec': 10}
✓ Reward function 加载成功
✓ GRPOConfig 配置完成
✓ GRPOTrainer 创建成功
训练样本数: 100
每 epoch steps: 400

============================================================
开始 GRPO 训练
============================================================

The model is already on multiple devices. Skipping the move to device specified in `args`.
==((====))==  Unsloth - 2x faster free finetuning | Num GPUs used = 1
   \\   /|    Num examples = 100 | Num Epochs = 1 | Total steps = 100
O^O/ \_/ \    Batch size per device = 1 | Gradient accumulation steps = 4
\        /    Data Parallel GPUs = 1 | Total batch size (1 x 4 x 1) = 4
 "-____-"     Trainable parameters = 17,596,416 of 511,629,184 (3.44% trained)

  0%|          | 0/100 [00:00<?, ?it/s]
======================================================================
[DEBUG] Completion #1
======================================================================
原始输出:
```json
{
  "extend": "是",
  "extend_sec": 0
}
```
======================================================================

DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumoDEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo

Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~351500.00UPS, TraCI: 63ms, vehicles TOT 1577 ACT 703 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~703000.00UPS, TraCI: 63ms, vehicles TOT 1577 ACT 703 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~703000.00UPS, TraCI: 62ms, vehicles TOT 1577 ACT 703 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~351500.00UPS, TraCI: 62ms, vehicles TOT 1577 ACT 703 BUF 

  1%|          | 1/100 [00:10<17:25, 10.56s/it]
======================================================================
[DEBUG] Completion #2
======================================================================
原始输出:
{
    "extend": "是",
    "extend_sec": 14
}
======================================================================

DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumoDEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo

Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0

DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
 Retrying in 1 secondsStarting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0

 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
  - 提取的不是dict: <class 'NoneType'>
[DEBUG] extend_decision 解析失败，原始输出: 根据输入 JSON 中的 phase_order 和 state，我们可以计算出当前绿灯相位的总时长。假设相位的总时长为 total_green_sec，那么我们有：

1. current_phase_elapsed_sec: 当前相位的时长
2. wait_time_for_phase_change: 从"现在"到能够完成相位切换所需的等待时间（秒）
3. final_green_sec: 当前绿灯相位的总时长，即 final_green_sec = state.current_phase_elapsed_sec + extend_sec

根据题目要求，我们只需要输出是否需要延长当前绿灯
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~603000.00UPS, TraCI: 76ms, vehicles TOT 1217 ACT 603 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~603000.00UPS, TraCI: 75ms, vehicles TOT 1217 ACT 603 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 1ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~603000.00UPS, TraCI: 75ms, vehicles TOT 1217 ACT 603 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~603000.00UPS, TraCI: 74ms, vehicles TOT 1217 ACT 603 BUF

  2%|▏         | 2/100 [00:15<11:58,  7.33s/it]
======================================================================
[DEBUG] Completion #3
======================================================================
原始输出:
{"next_phase_id": 1, "green_sec": 0}
======================================================================

DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMOSuccessfully connected to SUMO

Starting warmup phase...
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
[DEBUG] next_phase_id=2 不在 phase_ids=[1, 3]
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~289000.00UPS, TraCI: 60ms, vehicles TOT 961 ACT 578 BUF 0
  - green_sec <= 0: 0
[DEBUG] signal_step 解析失败，原始输出: {"next_phase_id": 1, "green_sec": 0}
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~578000.00UPS, TraCI: 60ms, vehicles TOT 961 ACT 578 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (33ms ~= 30.30*RT, ~28454.55UPS, TraCI: 59ms, vehicles TOT 1322 ACT 939 BUF 3
Step #507.00 (3ms ~= 333.33*RT, ~323333.33UPS, TraCI: 0ms, vehicles TOT 1369 ACT 970 BUF 1
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (32ms ~= 31.25*RT, ~29343.75UPS, TraCI: 60ms, vehicles TOT 1322 ACT 939 BUF 3
Step #512.00 (4ms ~= 250.00*RT, ~244250.00UPS, TraCI: 1ms, vehicles TOT 1387 ACT 977 BUF 9

  3%|▎         | 3/100 [00:18<08:20,  5.16s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumoStarting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0

Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds Retrying in 1 seconds

Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (31ms ~= 32.26*RT, ~27322.58UPS, TraCI: 64ms, vehicles TOT 1131 ACT 847 BUF 2
Step #449.00 (4ms ~= 250.00*RT, ~215500.00UPS, TraCI: 0ms, vehicles TOT 1160 ACT 862 BUF 8
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (30ms ~= 33.33*RT, ~28233.33UPS, TraCI: 65ms, vehicles TOT 1131 ACT 847 BUF 2
Step #453.00 (4ms ~= 250.00*RT, ~214750.00UPS, TraCI: 1ms, vehicles TOT 1168 ACT 859 BUF 7
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (31ms ~= 32.26*RT, ~27322.58UPS, TraCI: 64ms, vehicles TOT 1131 ACT 847 BUF 2
Step #478.00 (3ms ~= 333.33*RT, ~286666.67UPS, TraCI: 0ms, vehicles TOT 1218 ACT 860 BUF 9
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 1ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (31ms ~= 32.26*RT, ~27322.58UPS, TraCI: 65ms, vehicles TOT 1131 ACT 847 BUF 2
Step #478.00 (2ms ~= 500.00*RT, ~430500.00UPS, TraCI: 0ms, vehicles TOT 1218 ACT 861 BUF 9

  4%|▍         | 4/100 [00:20<06:39,  4.16s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds Retrying in 1 seconds

Successfully connected to SUMO
Starting warmup phase...
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
  - 类型错误: next_phase_id=<class 'int'>, green_sec=<class 'float'>
[DEBUG] signal_step 解析失败，原始输出: {"next_phase_id": 3, "green_sec": 12.0}
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~281500.00UPS, TraCI: 66ms, vehicles TOT 812 ACT 563 BUF 0
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (30ms ~= 33.33*RT, ~26666.67UPS, TraCI: 66ms, vehicles TOT 1052 ACT 800 BUF 1
Step #463.00 (3ms ~= 333.33*RT, ~277333.33UPS, TraCI: 0ms, vehicles TOT 1163 ACT 832 BUF 7
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (31ms ~= 32.26*RT, ~25806.45UPS, TraCI: 65ms, vehicles TOT 1052 ACT 800 BUF 1
Step #463.00 (3ms ~= 333.33*RT, ~277000.00UPS, TraCI: 0ms, vehicles TOT 1163 ACT 831 BUF 7
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (30ms ~= 33.33*RT, ~26666.67UPS, TraCI: 66ms, vehicles TOT 1052 ACT 800 BUF 1
Step #484.00 (2ms ~= 500.00*RT, ~414000.00UPS, TraCI: 0ms, vehicles TOT 1201 ACT 828 BUF 9

  5%|▌         | 5/100 [00:23<05:51,  3.70s/it]
                                               
{'loss': 0.0, 'grad_norm': 3.1875, 'learning_rate': 1.6e-07, 'num_tokens': 16061.0, 'completions/mean_length': 23.65, 'completions/min_length': 17.0, 'completions/max_length': 41.8, 'completions/clipped_ratio': 0.05, 'completions/mean_terminated_length': 18.033333396911623, 'completions/min_terminated_length': 17.0, 'completions/max_terminated_length': 20.0, 'rewards/tsc_reward_fn/mean': -0.25192307829856875, 'rewards/tsc_reward_fn/std': 0.9126509189605713, 'reward': -0.25192307829856875, 'reward_std': 0.9126509189605713, 'frac_reward_zero_std': 0.4, 'completion_length': 23.65, 'kl': 0.00018550805398263038, 'step_time': 4.696804464404704, 'epoch': 0.05}

  5%|▌         | 5/100 [00:23<05:51,  3.70s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumoDEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo

Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0

 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMOSuccessfully connected to SUMOSuccessfully connected to SUMO


Starting warmup phase...
Starting warmup phase...Starting warmup phase...

Warmup progress: 0/300
Warmup progress: 0/300
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
[DEBUG] next_phase_id=399226823 不在 phase_ids=[1, 3]
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~533000.00UPS, TraCI: 48ms, vehicles TOT 744 ACT 533 BUF 
  - green_sec <= 0: 0
[DEBUG] signal_step 解析失败，原始输出: {"next_phase_id": 3, "green_sec": 0}
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~533000.00UPS, TraCI: 49ms, vehicles TOT 744 ACT 533 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (23ms ~= 43.48*RT, ~31608.70UPS, TraCI: 48ms, vehicles TOT 939 ACT 727 BUF 22
Step #394.00 (2ms ~= 500.00*RT, ~379500.00UPS, TraCI: 1ms, vehicles TOT 981 ACT 759 BUF 6)
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (23ms ~= 43.48*RT, ~31608.70UPS, TraCI: 48ms, vehicles TOT 939 ACT 727 BUF 22
Step #401.00 (2ms ~= 500.00*RT, ~380500.00UPS, TraCI: 1ms, vehicles TOT 994 ACT 761 BUF 7)

  6%|▌         | 6/100 [00:26<05:15,  3.35s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
 Retrying in 1 seconds Retrying in 1 seconds

Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
  - green_sec <= 0: 0
[DEBUG] signal_step 解析失败，原始输出: {"next_phase_id": 1, "green_sec": 0}
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~553000.00UPS, TraCI: 47ms, vehicles TOT 782 ACT 553 BUF 
[DEBUG] next_phase_id=3858789814 不在 phase_ids=[1, 3]
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~553000.00UPS, TraCI: 48ms, vehicles TOT 782 ACT 553 BUF 
Step #0.00 (1ms ~= 1000.00*RT, ~0.00UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)          
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (24ms ~= 41.67*RT, ~32000.00UPS, TraCI: 47ms, vehicles TOT 999 ACT 768 BUF 20
Step #412.00 (3ms ~= 333.33*RT, ~261666.67UPS, TraCI: 0ms, vehicles TOT 1033 ACT 785 BUF 1
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (24ms ~= 41.67*RT, ~32000.00UPS, TraCI: 47ms, vehicles TOT 999 ACT 768 BUF 20
Step #448.00 (2ms ~= 500.00*RT, ~404000.00UPS, TraCI: 1ms, vehicles TOT 1108 ACT 808 BUF 5

  7%|▋         | 7/100 [00:29<04:53,  3.15s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
 Retrying in 1 seconds
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
  - 提取的不是dict: <class 'NoneType'>
[DEBUG] extend_decision 解析失败，原始输出: 根据给定的输入 JSON，我们需要判断是否需要延长当前绿灯相位。根据输入中的 phase_order 和 state，我们可以确定当前相位的队列大小，以及相位内绿灯时长和等待时间。

首先，我们需要计算当前相位的队列大小和当前绿灯时长：
- state.current_phase_elapsed_sec
- state.wait_time_for_phase_change

然后，我们检查这个队列大小是否大于当前绿灯时长（phase_limits[current_phase_id].max_green），如果是，则需要延长；否则，不需要延长。

由于输出 JSON 是单行字符串，无法直接编写 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~312500.00UPS, TraCI: 71ms, vehicles TOT 1330 ACT 625 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~625000.00UPS, TraCI: 71ms, vehicles TOT 1330 ACT 625 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~312500.00UPS, TraCI: 70ms, vehicles TOT 1330 ACT 625 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~625000.00UPS, TraCI: 70ms, vehicles TOT 1330 ACT 625 BUF

  8%|▊         | 8/100 [00:33<05:35,  3.65s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
  - 类型错误: next_phase_id=<class 'int'>, green_sec=<class 'float'>
[DEBUG] signal_step 解析失败，原始输出: {"next_phase_id": 3, "green_sec": 15.0}
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~554000.00UPS, TraCI: 48ms, vehicles TOT 785 ACT 554 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (23ms ~= 43.48*RT, ~33086.96UPS, TraCI: 47ms, vehicles TOT 994 ACT 761 BUF 28
Step #415.00 (3ms ~= 333.33*RT, ~263000.00UPS, TraCI: 0ms, vehicles TOT 1042 ACT 789 BUF 1
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (23ms ~= 43.48*RT, ~33086.96UPS, TraCI: 47ms, vehicles TOT 994 ACT 761 BUF 28
Step #440.00 (2ms ~= 500.00*RT, ~407000.00UPS, TraCI: 0ms, vehicles TOT 1099 ACT 814 BUF 6
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (23ms ~= 43.48*RT, ~33086.96UPS, TraCI: 47ms, vehicles TOT 994 ACT 761 BUF 28
Step #440.00 (2ms ~= 500.00*RT, ~407000.00UPS, TraCI: 0ms, vehicles TOT 1099 ACT 814 BUF 6

  9%|▉         | 9/100 [00:36<05:06,  3.37s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (31ms ~= 32.26*RT, ~27903.23UPS, TraCI: 64ms, vehicles TOT 1162 ACT 865 BUF 1
Step #468.00 (3ms ~= 333.33*RT, ~292000.00UPS, TraCI: 1ms, vehicles TOT 1215 ACT 876 BUF 1
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (31ms ~= 32.26*RT, ~27903.23UPS, TraCI: 64ms, vehicles TOT 1162 ACT 865 BUF 1
Step #490.00 (3ms ~= 333.33*RT, ~292000.00UPS, TraCI: 0ms, vehicles TOT 1254 ACT 876 BUF 1
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (31ms ~= 32.26*RT, ~27903.23UPS, TraCI: 64ms, vehicles TOT 1162 ACT 865 BUF 1
Step #518.00 (2ms ~= 500.00*RT, ~439000.00UPS, TraCI: 1ms, vehicles TOT 1312 ACT 878 BUF 9
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (2ms ~= 500.00*RT, ~164000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1)
Step #300.00 (31ms ~= 32.26*RT, ~27903.23UPS, TraCI: 64ms, vehicles TOT 1162 ACT 865 BUF 1
Step #548.00 (2ms ~= 500.00*RT, ~424000.00UPS, TraCI: 1ms, vehicles TOT 1357 ACT 848 BUF 1
Step #578.00 (2ms ~= 500.00*RT, ~417500.00UPS, TraCI: 0ms, vehicles TOT 1426 ACT 835 BUF 1

 10%|█         | 10/100 [00:39<04:55,  3.28s/it]
                                                
{'loss': 0.0, 'grad_norm': 3.9375, 'learning_rate': 3.6e-07, 'num_tokens': 31949.0, 'completions/mean_length': 24.2, 'completions/min_length': 15.8, 'completions/max_length': 45.4, 'completions/clipped_ratio': 0.05, 'completions/mean_terminated_length': 18.666666793823243, 'completions/min_terminated_length': 15.8, 'completions/max_terminated_length': 24.4, 'rewards/tsc_reward_fn/mean': -0.20230768918991088, 'rewards/tsc_reward_fn/std': 0.9640222072601319, 'reward': -0.20230768918991088, 'reward_std': 0.9640222072601319, 'frac_reward_zero_std': 0.2, 'completion_length': 24.2, 'kl': 0.000633394553369726, 'step_time': 3.1603063910093625, 'epoch': 0.1}

 10%|█         | 10/100 [00:39<04:55,  3.28s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumoStarting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0

Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds Retrying in 1 seconds

DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMOSuccessfully connected to SUMO

Starting warmup phase...Starting warmup phase...

Warmup progress: 0/300
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (30ms ~= 33.33*RT, ~27866.67UPS, TraCI: 65ms, vehicles TOT 1117 ACT 836 BUF 2
Step #446.00 (3ms ~= 333.33*RT, ~287333.33UPS, TraCI: 0ms, vehicles TOT 1155 ACT 862 BUF 7
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (30ms ~= 33.33*RT, ~27866.67UPS, TraCI: 65ms, vehicles TOT 1117 ACT 836 BUF 2
Step #445.00 (4ms ~= 250.00*RT, ~215750.00UPS, TraCI: 1ms, vehicles TOT 1155 ACT 863 BUF 7
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (31ms ~= 32.26*RT, ~26967.74UPS, TraCI: 64ms, vehicles TOT 1117 ACT 836 BUF 2
Step #454.00 (3ms ~= 333.33*RT, ~285666.67UPS, TraCI: 1ms, vehicles TOT 1167 ACT 857 BUF 7
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (30ms ~= 33.33*RT, ~27866.67UPS, TraCI: 65ms, vehicles TOT 1117 ACT 836 BUF 2
Step #474.00 (2ms ~= 500.00*RT, ~430500.00UPS, TraCI: 1ms, vehicles TOT 1208 ACT 861 BUF 1

 11%|█         | 11/100 [00:42<04:38,  3.12s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~582000.00UPS, TraCI: 59ms, vehicles TOT 1025 ACT 582 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~582000.00UPS, TraCI: 57ms, vehicles TOT 1025 ACT 582 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~291000.00UPS, TraCI: 59ms, vehicles TOT 1025 ACT 582 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~291000.00UPS, TraCI: 57ms, vehicles TOT 1025 ACT 582 BUF 

 12%|█▏        | 12/100 [00:45<04:23,  3.00s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds Retrying in 1 seconds

 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~308000.00UPS, TraCI: 72ms, vehicles TOT 1289 ACT 616 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 1ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~308000.00UPS, TraCI: 74ms, vehicles TOT 1289 ACT 616 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 1ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~616000.00UPS, TraCI: 72ms, vehicles TOT 1289 ACT 616 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (2ms ~= 500.00*RT, ~164000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1)
Step #300.00 (1ms ~= 1000.00*RT, ~616000.00UPS, TraCI: 72ms, vehicles TOT 1289 ACT 616 BUF

 13%|█▎        | 13/100 [00:47<04:16,  2.94s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds Retrying in 1 seconds Retrying in 1 seconds


Successfully connected to SUMOSuccessfully connected to SUMO

Starting warmup phase...Starting warmup phase...

Warmup progress: 0/300
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
  - green_sec <= 0: 0
[DEBUG] signal_step 解析失败，原始输出: {"next_phase_id": 2093656823, "green_sec": 0}
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~593000.00UPS, TraCI: 54ms, vehicles TOT 1121 ACT 593 BUF
  - green_sec <= 0: 0
[DEBUG] signal_step 解析失败，原始输出: {"next_phase_id": 1, "green_sec": 0}
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~296500.00UPS, TraCI: 53ms, vehicles TOT 1121 ACT 593 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (34ms ~= 29.41*RT, ~32058.82UPS, TraCI: 54ms, vehicles TOT 1619 ACT 1090 BUF 
Step #603.00 (4ms ~= 250.00*RT, ~281000.00UPS, TraCI: 0ms, vehicles TOT 1707 ACT 1124 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 1ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (35ms ~= 28.57*RT, ~31142.86UPS, TraCI: 52ms, vehicles TOT 1619 ACT 1090 BUF 
Step #666.00 (3ms ~= 333.33*RT, ~376666.67UPS, TraCI: 0ms, vehicles TOT 1866 ACT 1130 BUF 

 14%|█▍        | 14/100 [00:51<04:16,  2.98s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMOSuccessfully connected to SUMO

Starting warmup phase...
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~701000.00UPS, TraCI: 62ms, vehicles TOT 1617 ACT 701 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~701000.00UPS, TraCI: 63ms, vehicles TOT 1617 ACT 701 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~350500.00UPS, TraCI: 61ms, vehicles TOT 1617 ACT 701 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~701000.00UPS, TraCI: 60ms, vehicles TOT 1617 ACT 701 BUF

 15%|█▌        | 15/100 [00:53<04:09,  2.93s/it]
                                                

 15%|█▌        | 15/100 [00:53<04:09,  2.93s/it]{'loss': 0.0, 'grad_norm': 0.0026397705078125, 'learning_rate': 5.6e-07, 'num_tokens': 50425.0, 'completions/mean_length': 20.2, 'completions/min_length': 14.8, 'completions/max_length': 25.2, 'completions/clipped_ratio': 0.0, 'completions/mean_terminated_length': 20.2, 'completions/min_terminated_length': 14.8, 'completions/max_terminated_length': 25.2, 'rewards/tsc_reward_fn/mean': -1.221204823255539, 'rewards/tsc_reward_fn/std': 0.4784842491149902, 'reward': -1.221204823255539, 'reward_std': 0.4784842491149902, 'frac_reward_zero_std': 0.8, 'completion_length': 20.2, 'kl': 0.0010878435910854022, 'step_time': 2.802683320979122, 'epoch': 0.15}
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumoDEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo

 Retrying in 1 seconds
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds Retrying in 1 seconds Retrying in 1 seconds


Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMOSuccessfully connected to SUMO

Starting warmup phase...
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
  - green_sec <= 0: 0
[DEBUG] signal_step 解析失败，原始输出: {"next_phase_id": 3858789816, "green_sec": 0}
  - green_sec <= 0: 0
[DEBUG] signal_step 解析失败，原始输出: {"next_phase_id": 3, "green_sec": 0}
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~574000.00UPS, TraCI: 60ms, vehicles TOT 952 ACT 574 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~287000.00UPS, TraCI: 60ms, vehicles TOT 952 ACT 574 BUF 0
  - green_sec <= 0: 0
[DEBUG] signal_step 解析失败，原始输出: {"next_phase_id": 2, "green_sec": 0}
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~287000.00UPS, TraCI: 60ms, vehicles TOT 952 ACT 574 BUF 0
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (32ms ~= 31.25*RT, ~28750.00UPS, TraCI: 60ms, vehicles TOT 1298 ACT 920 BUF 4
Step #500.00 (2ms ~= 500.00*RT, ~478000.00UPS, TraCI: 1ms, vehicles TOT 1349 ACT 956 BUF 1

 16%|█▌        | 16/100 [00:56<04:02,  2.88s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumoDEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo

Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Successfully connected to SUMOStarting warmup phase...

Starting warmup phase...
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 0/300
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~588000.00UPS, TraCI: 54ms, vehicles TOT 1118 ACT 588 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~588000.00UPS, TraCI: 54ms, vehicles TOT 1118 ACT 588 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~588000.00UPS, TraCI: 53ms, vehicles TOT 1118 ACT 588 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~588000.00UPS, TraCI: 53ms, vehicles TOT 1118 ACT 588 BUF

 17%|█▋        | 17/100 [00:59<03:53,  2.82s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMOSuccessfully connected to SUMO

Starting warmup phase...
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
  - green_sec <= 0: 0
[DEBUG] signal_step 解析失败，原始输出: {"next_phase_id": 1, "green_sec": 0}
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 1ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~285000.00UPS, TraCI: 65ms, vehicles TOT 844 ACT 570 BUF 0
[DEBUG] next_phase_id=2 不在 phase_ids=[1, 3]
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~570000.00UPS, TraCI: 65ms, vehicles TOT 844 ACT 570 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (31ms ~= 32.26*RT, ~26806.45UPS, TraCI: 65ms, vehicles TOT 1108 ACT 831 BUF 2
Step #461.00 (3ms ~= 333.33*RT, ~285333.33UPS, TraCI: 0ms, vehicles TOT 1182 ACT 856 BUF 7
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 1ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (31ms ~= 32.26*RT, ~26806.45UPS, TraCI: 64ms, vehicles TOT 1108 ACT 831 BUF 2
Step #481.00 (3ms ~= 333.33*RT, ~286000.00UPS, TraCI: 0ms, vehicles TOT 1218 ACT 858 BUF 8

 18%|█▊        | 18/100 [01:01<03:47,  2.77s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
[DEBUG] next_phase_id=3858789814 不在 phase_ids=[1, 3]
[DEBUG] next_phase_id=2 不在 phase_ids=[1, 3]
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~274000.00UPS, TraCI: 48ms, vehicles TOT 766 ACT 548 BUF 0
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~548000.00UPS, TraCI: 48ms, vehicles TOT 766 ACT 548 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (22ms ~= 45.45*RT, ~34045.45UPS, TraCI: 48ms, vehicles TOT 967 ACT 749 BUF 21
Step #403.00 (3ms ~= 333.33*RT, ~255666.67UPS, TraCI: 0ms, vehicles TOT 1001 ACT 767 BUF 8
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (23ms ~= 43.48*RT, ~32565.22UPS, TraCI: 48ms, vehicles TOT 967 ACT 749 BUF 21
Step #439.00 (2ms ~= 500.00*RT, ~396500.00UPS, TraCI: 0ms, vehicles TOT 1080 ACT 793 BUF 9

 19%|█▉        | 19/100 [01:04<03:44,  2.77s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo

Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~667000.00UPS, TraCI: 67ms, vehicles TOT 1466 ACT 667 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 1ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~333500.00UPS, TraCI: 66ms, vehicles TOT 1466 ACT 667 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~667000.00UPS, TraCI: 66ms, vehicles TOT 1466 ACT 667 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~667000.00UPS, TraCI: 66ms, vehicles TOT 1466 ACT 667 BUF

 20%|██        | 20/100 [01:07<03:41,  2.77s/it]
                                                

 20%|██        | 20/100 [01:07<03:41,  2.77s/it]{'loss': 0.0, 'grad_norm': 0.000370025634765625, 'learning_rate': 7.599999999999999e-07, 'num_tokens': 67226.0, 'completions/mean_length': 19.65, 'completions/min_length': 17.8, 'completions/max_length': 22.8, 'completions/clipped_ratio': 0.0, 'completions/mean_terminated_length': 19.65, 'completions/min_terminated_length': 17.8, 'completions/max_terminated_length': 22.8, 'rewards/tsc_reward_fn/mean': -0.8612499952316284, 'rewards/tsc_reward_fn/std': 1.441733717918396, 'reward': -0.8612499952316284, 'reward_std': 1.4417337656021119, 'frac_reward_zero_std': 0.4, 'completion_length': 19.65, 'kl': 0.00034100228403985964, 'step_time': 2.6930681221827397, 'epoch': 0.2}
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds Retrying in 1 seconds

DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
  - green_sec <= 0: 0
[DEBUG] signal_step 解析失败，原始输出: {"next_phase_id": 1, "green_sec": 0}
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~588000.00UPS, TraCI: 60ms, vehicles TOT 977 ACT 588 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (33ms ~= 30.30*RT, ~28515.15UPS, TraCI: 59ms, vehicles TOT 1333 ACT 941 BUF 4
Step #514.00 (4ms ~= 250.00*RT, ~245000.00UPS, TraCI: 0ms, vehicles TOT 1392 ACT 980 BUF 1
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (32ms ~= 31.25*RT, ~29406.25UPS, TraCI: 60ms, vehicles TOT 1333 ACT 941 BUF 4
Step #541.00 (3ms ~= 333.33*RT, ~323333.33UPS, TraCI: 1ms, vehicles TOT 1439 ACT 970 BUF 9
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (33ms ~= 30.30*RT, ~28515.15UPS, TraCI: 60ms, vehicles TOT 1333 ACT 941 BUF 4
Step #551.00 (3ms ~= 333.33*RT, ~323333.33UPS, TraCI: 1ms, vehicles TOT 1459 ACT 970 BUF 1

 21%|██        | 21/100 [01:10<03:36,  2.74s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumoDEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo

Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0

DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds Retrying in 1 seconds

 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~299500.00UPS, TraCI: 76ms, vehicles TOT 1211 ACT 599 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (2ms ~= 500.00*RT, ~164000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1)
Step #300.00 (2ms ~= 500.00*RT, ~299500.00UPS, TraCI: 75ms, vehicles TOT 1211 ACT 599 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~599000.00UPS, TraCI: 75ms, vehicles TOT 1211 ACT 599 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~299500.00UPS, TraCI: 74ms, vehicles TOT 1211 ACT 599 BUF 

 22%|██▏       | 22/100 [01:12<03:33,  2.74s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (2ms ~= 500.00*RT, ~164000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1)
Step #300.00 (1ms ~= 1000.00*RT, ~597000.00UPS, TraCI: 61ms, vehicles TOT 995 ACT 597 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~298500.00UPS, TraCI: 61ms, vehicles TOT 995 ACT 597 BUF 0
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~298500.00UPS, TraCI: 59ms, vehicles TOT 995 ACT 597 BUF 0
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~597000.00UPS, TraCI: 60ms, vehicles TOT 995 ACT 597 BUF 

 23%|██▎       | 23/100 [01:15<03:31,  2.74s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumoDEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumoDEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo


Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0

Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds Retrying in 1 seconds

 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
[DEBUG] next_phase_id=2 不在 phase_ids=[1, 3]
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 1ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~582000.00UPS, TraCI: 65ms, vehicles TOT 869 ACT 582 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (32ms ~= 31.25*RT, ~26687.50UPS, TraCI: 64ms, vehicles TOT 1141 ACT 854 BUF 2
Step #453.00 (3ms ~= 333.33*RT, ~286666.67UPS, TraCI: 1ms, vehicles TOT 1171 ACT 860 BUF 7
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (31ms ~= 32.26*RT, ~27548.39UPS, TraCI: 65ms, vehicles TOT 1141 ACT 854 BUF 2
Step #455.00 (3ms ~= 333.33*RT, ~286666.67UPS, TraCI: 1ms, vehicles TOT 1175 ACT 860 BUF 7
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (31ms ~= 32.26*RT, ~27548.39UPS, TraCI: 64ms, vehicles TOT 1141 ACT 854 BUF 2
Step #455.00 (4ms ~= 250.00*RT, ~215000.00UPS, TraCI: 0ms, vehicles TOT 1175 ACT 860 BUF 7

 24%|██▍       | 24/100 [01:18<03:25,  2.71s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds Retrying in 1 seconds

 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~312000.00UPS, TraCI: 70ms, vehicles TOT 1343 ACT 624 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~624000.00UPS, TraCI: 70ms, vehicles TOT 1343 ACT 624 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 1ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~624000.00UPS, TraCI: 70ms, vehicles TOT 1343 ACT 624 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~624000.00UPS, TraCI: 70ms, vehicles TOT 1343 ACT 624 BUF

 25%|██▌       | 25/100 [01:20<03:22,  2.70s/it]
                                                

 25%|██▌       | 25/100 [01:20<03:22,  2.70s/it]{'loss': 0.0, 'grad_norm': 0.000255584716796875, 'learning_rate': 9.6e-07, 'num_tokens': 84385.0, 'completions/mean_length': 20.15, 'completions/min_length': 19.0, 'completions/max_length': 21.6, 'completions/clipped_ratio': 0.0, 'completions/mean_terminated_length': 20.15, 'completions/min_terminated_length': 19.0, 'completions/max_terminated_length': 21.6, 'rewards/tsc_reward_fn/mean': -0.8183333396911621, 'rewards/tsc_reward_fn/std': 1.0494117498397828, 'reward': -0.8183333396911621, 'reward_std': 1.0494117259979248, 'frac_reward_zero_std': 0.6, 'completion_length': 20.15, 'kl': 0.000501050610182574, 'step_time': 2.6582742535800206, 'epoch': 0.25}
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
[DEBUG] next_phase_id=2 不在 phase_ids=[1, 3]
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~553000.00UPS, TraCI: 48ms, vehicles TOT 788 ACT 553 BUF 
  - 类型错误: next_phase_id=<class 'int'>, green_sec=<class 'float'>
[DEBUG] signal_step 解析失败，原始输出: {"next_phase_id": 3, "green_sec": 12.0}
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~553000.00UPS, TraCI: 48ms, vehicles TOT 788 ACT 553 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (24ms ~= 41.67*RT, ~31875.00UPS, TraCI: 46ms, vehicles TOT 1001 ACT 765 BUF 3
Step #426.00 (2ms ~= 500.00*RT, ~395000.00UPS, TraCI: 1ms, vehicles TOT 1061 ACT 790 BUF 9
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (23ms ~= 43.48*RT, ~33260.87UPS, TraCI: 48ms, vehicles TOT 1001 ACT 765 BUF 3
Step #442.00 (2ms ~= 500.00*RT, ~408000.00UPS, TraCI: 1ms, vehicles TOT 1105 ACT 816 BUF 6

 26%|██▌       | 26/100 [01:23<03:21,  2.72s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~672000.00UPS, TraCI: 66ms, vehicles TOT 1492 ACT 672 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~672000.00UPS, TraCI: 65ms, vehicles TOT 1492 ACT 672 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~336000.00UPS, TraCI: 64ms, vehicles TOT 1492 ACT 672 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~672000.00UPS, TraCI: 64ms, vehicles TOT 1492 ACT 672 BUF

 27%|██▋       | 27/100 [01:26<03:18,  2.72s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~352500.00UPS, TraCI: 66ms, vehicles TOT 1538 ACT 705 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~352500.00UPS, TraCI: 65ms, vehicles TOT 1538 ACT 705 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~705000.00UPS, TraCI: 66ms, vehicles TOT 1538 ACT 705 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~352500.00UPS, TraCI: 65ms, vehicles TOT 1538 ACT 705 BUF 

 28%|██▊       | 28/100 [01:29<03:16,  2.74s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumoDEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo

Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0

 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
  - 类型错误: next_phase_id=<class 'int'>, green_sec=<class 'float'>
[DEBUG] signal_step 解析失败，原始输出: {"next_phase_id": 3, "green_sec": 2.0}
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~284000.00UPS, TraCI: 65ms, vehicles TOT 840 ACT 568 BUF 0
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (31ms ~= 32.26*RT, ~26774.19UPS, TraCI: 66ms, vehicles TOT 1103 ACT 830 BUF 1
Step #450.00 (3ms ~= 333.33*RT, ~285000.00UPS, TraCI: 0ms, vehicles TOT 1154 ACT 855 BUF 6
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (31ms ~= 32.26*RT, ~26774.19UPS, TraCI: 65ms, vehicles TOT 1103 ACT 830 BUF 1
Step #446.00 (2ms ~= 500.00*RT, ~427500.00UPS, TraCI: 0ms, vehicles TOT 1148 ACT 855 BUF 6
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (32ms ~= 31.25*RT, ~25937.50UPS, TraCI: 64ms, vehicles TOT 1103 ACT 830 BUF 1
Step #500.00 (2ms ~= 500.00*RT, ~426000.00UPS, TraCI: 0ms, vehicles TOT 1246 ACT 852 BUF 1

 29%|██▉       | 29/100 [01:32<03:15,  2.75s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (2ms ~= 500.00*RT, ~90500.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1) 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (30ms ~= 33.33*RT, ~26366.67UPS, TraCI: 67ms, vehicles TOT 1039 ACT 791 BUF 2
Step #431.00 (4ms ~= 250.00*RT, ~203750.00UPS, TraCI: 0ms, vehicles TOT 1089 ACT 815 BUF 8
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (30ms ~= 33.33*RT, ~26366.67UPS, TraCI: 67ms, vehicles TOT 1039 ACT 791 BUF 2
Step #447.00 (3ms ~= 333.33*RT, ~276000.00UPS, TraCI: 0ms, vehicles TOT 1124 ACT 828 BUF 6
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (30ms ~= 33.33*RT, ~26366.67UPS, TraCI: 66ms, vehicles TOT 1039 ACT 791 BUF 2
Step #447.00 (2ms ~= 500.00*RT, ~414000.00UPS, TraCI: 0ms, vehicles TOT 1124 ACT 828 BUF 6
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (30ms ~= 33.33*RT, ~26366.67UPS, TraCI: 67ms, vehicles TOT 1039 ACT 791 BUF 2
Step #511.00 (2ms ~= 500.00*RT, ~416500.00UPS, TraCI: 0ms, vehicles TOT 1252 ACT 833 BUF 9
Step #541.00 (3ms ~= 333.33*RT, ~265666.67UPS, TraCI: 0ms, vehicles TOT 1293 ACT 797 BUF 1

 30%|███       | 30/100 [01:35<03:17,  2.82s/it]
                                                

 30%|███       | 30/100 [01:35<03:17,  2.82s/it]{'loss': 0.0, 'grad_norm': 3.078125, 'learning_rate': 1.16e-06, 'num_tokens': 101061.0, 'completions/mean_length': 19.2, 'completions/min_length': 15.8, 'completions/max_length': 23.0, 'completions/clipped_ratio': 0.0, 'completions/mean_terminated_length': 19.2, 'completions/min_terminated_length': 15.8, 'completions/max_terminated_length': 23.0, 'rewards/tsc_reward_fn/mean': -0.7568749904632568, 'rewards/tsc_reward_fn/std': 0.4707077622413635, 'reward': -0.7568749904632568, 'reward_std': 0.47070775828324257, 'frac_reward_zero_std': 0.4, 'completion_length': 19.2, 'kl': 0.0004606483460520394, 'step_time': 2.775209777400596, 'epoch': 0.3}
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumoDEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo

Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0

DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds Retrying in 1 seconds

DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (2ms ~= 500.00*RT, ~164000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1)
Step #300.00 (2ms ~= 500.00*RT, ~330500.00UPS, TraCI: 67ms, vehicles TOT 1454 ACT 661 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~330500.00UPS, TraCI: 66ms, vehicles TOT 1454 ACT 661 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~661000.00UPS, TraCI: 66ms, vehicles TOT 1454 ACT 661 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~330500.00UPS, TraCI: 66ms, vehicles TOT 1454 ACT 661 BUF 

 31%|███       | 31/100 [01:37<03:13,  2.80s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds Retrying in 1 seconds

Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~619000.00UPS, TraCI: 72ms, vehicles TOT 1321 ACT 619 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~309500.00UPS, TraCI: 70ms, vehicles TOT 1321 ACT 619 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~619000.00UPS, TraCI: 72ms, vehicles TOT 1321 ACT 619 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 1ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~619000.00UPS, TraCI: 71ms, vehicles TOT 1321 ACT 619 BUF

 32%|███▏      | 32/100 [01:40<03:09,  2.78s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
 Retrying in 1 seconds
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~386500.00UPS, TraCI: 82ms, vehicles TOT 1835 ACT 773 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~773000.00UPS, TraCI: 82ms, vehicles TOT 1835 ACT 773 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~773000.00UPS, TraCI: 82ms, vehicles TOT 1835 ACT 773 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~773000.00UPS, TraCI: 82ms, vehicles TOT 1835 ACT 773 BUF

 33%|███▎      | 33/100 [01:43<03:07,  2.79s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumoDEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo

Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~363000.00UPS, TraCI: 60ms, vehicles TOT 1666 ACT 726 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 1ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~363000.00UPS, TraCI: 60ms, vehicles TOT 1666 ACT 726 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~363000.00UPS, TraCI: 60ms, vehicles TOT 1666 ACT 726 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~726000.00UPS, TraCI: 61ms, vehicles TOT 1666 ACT 726 BUF

 34%|███▍      | 34/100 [01:46<03:03,  2.78s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumoDEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo

Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0

DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
  - 提取的不是dict: <class 'NoneType'>
[DEBUG] extend_decision 解析失败，原始输出: 根据输入的 JSON 数据，我将执行以下决策：

1. 目标绿灯相位：1相位。
2. 取决于当前绿灯相位的排队车辆数（avg_queue_veh）和绿灯相位的可用时间（wait_time_for_phase_change）。
3. 统计当前绿灯相位的排队车辆数（avg_queue_veh），并计算该相位在等待时间内的通过车辆数（avg_passed_veh_in_current_green）。
4. 比较当前相位的排队车辆数和当前绿灯相位的排队车辆数
  - 提取的不是dict: <class 'NoneType'>
[DEBUG] extend_decision 解析失败，原始输出: 根据输入的 JSON 数据和硬约束，决策策略如下：

- 如果 current_phase_elapsed_sec + extend_sec 未超过 phase_limits[current_phase_id].max_green，那么需要延长当前绿灯相位。
- 在计算需要延长的秒数 extend_sec 时，需要考虑当前相位与其他相位的相对需求：当前相位队列大且仍在有效放行（通过增长）时更倾向延长；其他相位队列明显更大时更倾向不延长以尽快切换。

根据以上分析，以下是可能的决策结果：

```json
{
  "extend": "是",
  "extend
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (2ms ~= 500.00*RT, ~90500.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1) 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~579000.00UPS, TraCI: 55ms, vehicles TOT 1079 ACT 579 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~289500.00UPS, TraCI: 55ms, vehicles TOT 1079 ACT 579 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~289500.00UPS, TraCI: 54ms, vehicles TOT 1079 ACT 579 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (2ms ~= 500.00*RT, ~164000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1)
Step #300.00 (1ms ~= 1000.00*RT, ~579000.00UPS, TraCI: 54ms, vehicles TOT 1079 ACT 579 BUF

 35%|███▌      | 35/100 [01:50<03:38,  3.36s/it]
                                                

 35%|███▌      | 35/100 [01:50<03:38,  3.36s/it]{'loss': 0.0, 'grad_norm': 0.000232696533203125, 'learning_rate': 1.3600000000000001e-06, 'num_tokens': 121761.0, 'completions/mean_length': 32.4, 'completions/min_length': 20.4, 'completions/max_length': 44.2, 'completions/clipped_ratio': 0.1, 'completions/mean_terminated_length': 21.85, 'completions/min_terminated_length': 20.4, 'completions/max_terminated_length': 23.2, 'rewards/tsc_reward_fn/mean': -2.0, 'rewards/tsc_reward_fn/std': 0.0, 'reward': -2.0, 'reward_std': 0.0, 'frac_reward_zero_std': 1.0, 'completion_length': 32.4, 'kl': 0.00034596752066136106, 'step_time': 3.1144531205995007, 'epoch': 0.35}
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo

Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds Retrying in 1 seconds

 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~619000.00UPS, TraCI: 73ms, vehicles TOT 1278 ACT 619 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 1ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~619000.00UPS, TraCI: 73ms, vehicles TOT 1278 ACT 619 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~309500.00UPS, TraCI: 72ms, vehicles TOT 1278 ACT 619 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~619000.00UPS, TraCI: 72ms, vehicles TOT 1278 ACT 619 BUF

 36%|███▌      | 36/100 [01:53<03:22,  3.17s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds Retrying in 1 seconds

 Retrying in 1 seconds
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 1ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~288000.00UPS, TraCI: 64ms, vehicles TOT 888 ACT 576 BUF 0
  - 提取的不是dict: <class 'NoneType'>
[DEBUG] extend_decision 解析失败，原始输出: 为了提供帮助，我需要更多的具体信息。请提供以下内容：

1. 输入 JSON 中 phase_order 和 phase_limits 的详细信息。
2. 输入 JSON 中 state 的详细信息，包括 current_phase_elapsed_sec 和 wait_time_for_phase_change。
3. 相应的 phase_ids 和 phase_limits 对应的 values。

根据这些信息，我可以更好地理解你的需求，并提供针对性的决策建议。
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~288000.00UPS, TraCI: 63ms, vehicles TOT 888 ACT 576 BUF 0
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~576000.00UPS, TraCI: 64ms, vehicles TOT 888 ACT 576 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 1ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~576000.00UPS, TraCI: 64ms, vehicles TOT 888 ACT 576 BUF 

 37%|███▋      | 37/100 [01:57<03:33,  3.38s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
  - 类型错误: next_phase_id=<class 'int'>, green_sec=<class 'float'>
[DEBUG] signal_step 解析失败，原始输出: {"next_phase_id": 3, "green_sec": 1.0}
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~277000.00UPS, TraCI: 47ms, vehicles TOT 787 ACT 554 BUF 0
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (2ms ~= 500.00*RT, ~164000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1)
Step #300.00 (23ms ~= 43.48*RT, ~33521.74UPS, TraCI: 48ms, vehicles TOT 1005 ACT 771 BUF 2
Step #417.00 (2ms ~= 500.00*RT, ~397000.00UPS, TraCI: 1ms, vehicles TOT 1049 ACT 794 BUF 1
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (23ms ~= 43.48*RT, ~33521.74UPS, TraCI: 47ms, vehicles TOT 1005 ACT 771 BUF 2
Step #442.00 (2ms ~= 500.00*RT, ~407000.00UPS, TraCI: 1ms, vehicles TOT 1103 ACT 814 BUF 6
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (23ms ~= 43.48*RT, ~33521.74UPS, TraCI: 47ms, vehicles TOT 1005 ACT 771 BUF 2
Step #472.00 (2ms ~= 500.00*RT, ~403000.00UPS, TraCI: 0ms, vehicles TOT 1161 ACT 806 BUF 1

 38%|███▊      | 38/100 [02:00<03:17,  3.19s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 1ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (31ms ~= 32.26*RT, ~25838.71UPS, TraCI: 66ms, vehicles TOT 1061 ACT 801 BUF 2
Step #431.00 (3ms ~= 333.33*RT, ~274666.67UPS, TraCI: 1ms, vehicles TOT 1098 ACT 824 BUF 1
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 1ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (31ms ~= 32.26*RT, ~25838.71UPS, TraCI: 66ms, vehicles TOT 1061 ACT 801 BUF 2
Step #440.00 (3ms ~= 333.33*RT, ~280000.00UPS, TraCI: 0ms, vehicles TOT 1125 ACT 840 BUF 7
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (2ms ~= 500.00*RT, ~164000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1)
Step #300.00 (30ms ~= 33.33*RT, ~26700.00UPS, TraCI: 66ms, vehicles TOT 1061 ACT 801 BUF 2
Step #441.00 (3ms ~= 333.33*RT, ~279666.67UPS, TraCI: 0ms, vehicles TOT 1127 ACT 839 BUF 7
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (31ms ~= 32.26*RT, ~25838.71UPS, TraCI: 66ms, vehicles TOT 1061 ACT 801 BUF 2
Step #441.00 (2ms ~= 500.00*RT, ~419500.00UPS, TraCI: 0ms, vehicles TOT 1127 ACT 839 BUF 7

 39%|███▉      | 39/100 [02:02<03:06,  3.06s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds Retrying in 1 seconds Retrying in 1 seconds


 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Successfully connected to SUMO
Starting warmup phase...
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300Warmup progress: 0/300

Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (23ms ~= 43.48*RT, ~33521.74UPS, TraCI: 47ms, vehicles TOT 1004 ACT 771 BUF 1
Step #413.00 (4ms ~= 250.00*RT, ~197000.00UPS, TraCI: 0ms, vehicles TOT 1038 ACT 788 BUF 1
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (23ms ~= 43.48*RT, ~33521.74UPS, TraCI: 47ms, vehicles TOT 1004 ACT 771 BUF 1
Step #419.00 (4ms ~= 250.00*RT, ~197750.00UPS, TraCI: 0ms, vehicles TOT 1049 ACT 791 BUF 1
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (23ms ~= 43.48*RT, ~33521.74UPS, TraCI: 47ms, vehicles TOT 1004 ACT 771 BUF 1
Step #419.00 (3ms ~= 333.33*RT, ~263666.67UPS, TraCI: 1ms, vehicles TOT 1049 ACT 791 BUF 1
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (23ms ~= 43.48*RT, ~33521.74UPS, TraCI: 47ms, vehicles TOT 1004 ACT 771 BUF 1
Step #419.00 (4ms ~= 250.00*RT, ~197750.00UPS, TraCI: 0ms, vehicles TOT 1049 ACT 791 BUF 1

 40%|████      | 40/100 [02:05<02:57,  2.95s/it]
                                                

 40%|████      | 40/100 [02:05<02:57,  2.95s/it]{'loss': 0.0, 'grad_norm': 0.00024318695068359375, 'learning_rate': 1.5599999999999999e-06, 'num_tokens': 138077.0, 'completions/mean_length': 21.6, 'completions/min_length': 15.4, 'completions/max_length': 34.6, 'completions/clipped_ratio': 0.0, 'completions/mean_terminated_length': 21.6, 'completions/min_terminated_length': 15.4, 'completions/max_terminated_length': 34.6, 'rewards/tsc_reward_fn/mean': -0.5842424154281616, 'rewards/tsc_reward_fn/std': 0.5536227226257324, 'reward': -0.5842424154281616, 'reward_std': 0.5536227107048035, 'frac_reward_zero_std': 0.6, 'completion_length': 21.6, 'kl': 0.0006848548058769665, 'step_time': 2.9279591444006656, 'epoch': 0.4}
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumoDEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo

Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0

DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMOSuccessfully connected to SUMO

Starting warmup phase...Starting warmup phase...

Warmup progress: 0/300
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
[DEBUG] next_phase_id=395388661 不在 phase_ids=[1, 3]
[DEBUG] next_phase_id=2 不在 phase_ids=[1, 3]
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~558000.00UPS, TraCI: 66ms, vehicles TOT 800 ACT 558 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~558000.00UPS, TraCI: 67ms, vehicles TOT 800 ACT 558 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (31ms ~= 32.26*RT, ~25548.39UPS, TraCI: 66ms, vehicles TOT 1036 ACT 792 BUF 1
Step #449.00 (3ms ~= 333.33*RT, ~274666.67UPS, TraCI: 1ms, vehicles TOT 1122 ACT 824 BUF 6
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (31ms ~= 32.26*RT, ~25548.39UPS, TraCI: 66ms, vehicles TOT 1036 ACT 792 BUF 1
Step #449.00 (3ms ~= 333.33*RT, ~274666.67UPS, TraCI: 1ms, vehicles TOT 1122 ACT 824 BUF 6

 41%|████      | 41/100 [02:08<02:54,  2.96s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMOSuccessfully connected to SUMO
Starting warmup phase...

Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~294500.00UPS, TraCI: 51ms, vehicles TOT 1154 ACT 589 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~294500.00UPS, TraCI: 51ms, vehicles TOT 1154 ACT 589 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~294500.00UPS, TraCI: 51ms, vehicles TOT 1154 ACT 589 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~589000.00UPS, TraCI: 51ms, vehicles TOT 1154 ACT 589 BUF

 42%|████▏     | 42/100 [02:11<02:46,  2.88s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumoDEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo

Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0

 Retrying in 1 seconds
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMOSuccessfully connected to SUMO

Starting warmup phase...Starting warmup phase...

Warmup progress: 0/300Successfully connected to SUMO

Warmup progress: 0/300Starting warmup phase...

Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~292000.00UPS, TraCI: 56ms, vehicles TOT 1061 ACT 584 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~584000.00UPS, TraCI: 57ms, vehicles TOT 1061 ACT 584 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~292000.00UPS, TraCI: 57ms, vehicles TOT 1061 ACT 584 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~584000.00UPS, TraCI: 56ms, vehicles TOT 1061 ACT 584 BUF

 43%|████▎     | 43/100 [02:13<02:41,  2.83s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (30ms ~= 33.33*RT, ~27033.33UPS, TraCI: 65ms, vehicles TOT 1082 ACT 811 BUF 2
Step #437.00 (4ms ~= 250.00*RT, ~212000.00UPS, TraCI: 0ms, vehicles TOT 1130 ACT 848 BUF 8
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (31ms ~= 32.26*RT, ~26161.29UPS, TraCI: 65ms, vehicles TOT 1082 ACT 811 BUF 2
Step #441.00 (4ms ~= 250.00*RT, ~212250.00UPS, TraCI: 0ms, vehicles TOT 1137 ACT 849 BUF 8
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (30ms ~= 33.33*RT, ~27033.33UPS, TraCI: 65ms, vehicles TOT 1082 ACT 811 BUF 2
Step #446.00 (3ms ~= 333.33*RT, ~283666.67UPS, TraCI: 0ms, vehicles TOT 1145 ACT 851 BUF 7
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (2ms ~= 500.00*RT, ~164000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1)
Step #300.00 (30ms ~= 33.33*RT, ~27033.33UPS, TraCI: 65ms, vehicles TOT 1082 ACT 811 BUF 2
Step #446.00 (3ms ~= 333.33*RT, ~283666.67UPS, TraCI: 0ms, vehicles TOT 1145 ACT 851 BUF 7

 44%|████▍     | 44/100 [02:16<02:37,  2.81s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds Retrying in 1 seconds

DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
  - 类型错误: next_phase_id=<class 'int'>, green_sec=<class 'float'>
[DEBUG] signal_step 解析失败，原始输出: {"next_phase_id": 3, "green_sec": 0.0}
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~580000.00UPS, TraCI: 63ms, vehicles TOT 905 ACT 580 BUF 
  - 类型错误: next_phase_id=<class 'int'>, green_sec=<class 'float'>
[DEBUG] signal_step 解析失败，原始输出: {"next_phase_id": 3, "green_sec": 2.0}
[DEBUG] next_phase_id=2093656822 不在 phase_ids=[1, 3]
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~580000.00UPS, TraCI: 63ms, vehicles TOT 905 ACT 580 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~580000.00UPS, TraCI: 63ms, vehicles TOT 905 ACT 580 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (32ms ~= 31.25*RT, ~27375.00UPS, TraCI: 63ms, vehicles TOT 1202 ACT 876 BUF 3
Step #472.00 (2ms ~= 500.00*RT, ~452000.00UPS, TraCI: 1ms, vehicles TOT 1251 ACT 904 BUF 1

 45%|████▌     | 45/100 [02:19<02:37,  2.86s/it]
                                                

 45%|████▌     | 45/100 [02:19<02:37,  2.86s/it]{'loss': 0.0, 'grad_norm': 4.84375, 'learning_rate': 1.7599999999999999e-06, 'num_tokens': 154951.0, 'completions/mean_length': 21.7, 'completions/min_length': 19.0, 'completions/max_length': 27.4, 'completions/clipped_ratio': 0.0, 'completions/mean_terminated_length': 21.7, 'completions/min_terminated_length': 19.0, 'completions/max_terminated_length': 27.4, 'rewards/tsc_reward_fn/mean': -0.6300000190734864, 'rewards/tsc_reward_fn/std': 0.8041245937347412, 'reward': -0.6300000190734864, 'reward_std': 0.8041245937347412, 'frac_reward_zero_std': 0.4, 'completion_length': 21.7, 'kl': 0.0007510325027396903, 'step_time': 2.7869875077914914, 'epoch': 0.45}
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumoDEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo

DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds Retrying in 1 seconds Retrying in 1 seconds


Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
  - green_sec <= 0: 0
[DEBUG] signal_step 解析失败，原始输出: {"next_phase_id": 3, "green_sec": 0}
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~555000.00UPS, TraCI: 67ms, vehicles TOT 793 ACT 555 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (30ms ~= 33.33*RT, ~25833.33UPS, TraCI: 67ms, vehicles TOT 1015 ACT 775 BUF 2
Step #418.00 (2ms ~= 500.00*RT, ~400000.00UPS, TraCI: 1ms, vehicles TOT 1055 ACT 800 BUF 1
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (31ms ~= 32.26*RT, ~25000.00UPS, TraCI: 66ms, vehicles TOT 1015 ACT 775 BUF 2
Step #421.00 (3ms ~= 333.33*RT, ~265666.67UPS, TraCI: 0ms, vehicles TOT 1059 ACT 797 BUF 1
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (30ms ~= 33.33*RT, ~25833.33UPS, TraCI: 66ms, vehicles TOT 1015 ACT 775 BUF 2
Step #426.00 (2ms ~= 500.00*RT, ~397500.00UPS, TraCI: 0ms, vehicles TOT 1066 ACT 795 BUF 8

 46%|████▌     | 46/100 [02:22<02:29,  2.78s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~382500.00UPS, TraCI: 84ms, vehicles TOT 1795 ACT 765 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~382500.00UPS, TraCI: 84ms, vehicles TOT 1795 ACT 765 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 1ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~765000.00UPS, TraCI: 84ms, vehicles TOT 1795 ACT 765 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 1ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~382500.00UPS, TraCI: 85ms, vehicles TOT 1795 ACT 765 BUF 

 47%|████▋     | 47/100 [02:25<02:27,  2.78s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds Retrying in 1 seconds

Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~594000.00UPS, TraCI: 52ms, vehicles TOT 1183 ACT 594 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~594000.00UPS, TraCI: 50ms, vehicles TOT 1183 ACT 594 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~594000.00UPS, TraCI: 51ms, vehicles TOT 1183 ACT 594 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~297000.00UPS, TraCI: 51ms, vehicles TOT 1183 ACT 594 BUF 

 48%|████▊     | 48/100 [02:28<02:39,  3.06s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (31ms ~= 32.26*RT, ~27677.42UPS, TraCI: 64ms, vehicles TOT 1149 ACT 858 BUF 2
Step #456.00 (3ms ~= 333.33*RT, ~288333.33UPS, TraCI: 1ms, vehicles TOT 1182 ACT 865 BUF 7
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (30ms ~= 33.33*RT, ~28600.00UPS, TraCI: 64ms, vehicles TOT 1149 ACT 858 BUF 2
Step #463.00 (3ms ~= 333.33*RT, ~290000.00UPS, TraCI: 1ms, vehicles TOT 1202 ACT 870 BUF 7
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (2ms ~= 500.00*RT, ~164000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1)
Step #300.00 (31ms ~= 32.26*RT, ~27677.42UPS, TraCI: 64ms, vehicles TOT 1149 ACT 858 BUF 2
Step #456.00 (3ms ~= 333.33*RT, ~288333.33UPS, TraCI: 1ms, vehicles TOT 1182 ACT 865 BUF 7
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (31ms ~= 32.26*RT, ~27677.42UPS, TraCI: 64ms, vehicles TOT 1149 ACT 858 BUF 2
Step #482.00 (2ms ~= 500.00*RT, ~435500.00UPS, TraCI: 1ms, vehicles TOT 1234 ACT 871 BUF 9

 49%|████▉     | 49/100 [02:31<02:31,  2.97s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds Retrying in 1 seconds

Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~665000.00UPS, TraCI: 68ms, vehicles TOT 1445 ACT 665 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~665000.00UPS, TraCI: 67ms, vehicles TOT 1445 ACT 665 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~665000.00UPS, TraCI: 67ms, vehicles TOT 1445 ACT 665 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~665000.00UPS, TraCI: 68ms, vehicles TOT 1445 ACT 665 BUF

 50%|█████     | 50/100 [02:34<02:24,  2.89s/it]{'loss': 0.0, 'grad_norm': 0.000263214111328125, 'learning_rate': 1.96e-06, 'num_tokens': 172506.0, 'completions/mean_length': 22.75, 'completions/min_length': 17.4, 'completions/max_length': 33.6, 'completions/clipped_ratio': 0.0, 'completions/mean_terminated_length': 22.75, 'completions/min_terminated_length': 17.4, 'completions/max_terminated_length': 33.6, 'rewards/tsc_reward_fn/mean': -0.85, 'rewards/tsc_reward_fn/std': 0.4516611576080322, 'reward': -0.85, 'reward_std': 0.4516611576080322, 'frac_reward_zero_std': 0.6, 'completion_length': 22.75, 'kl': 0.000723770178592531, 'step_time': 2.8748335402226077, 'epoch': 0.5}

                                                

 50%|█████     | 50/100 [02:34<02:24,  2.89s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumoDEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo

Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0

DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
  - 类型错误: next_phase_id=<class 'int'>, green_sec=<class 'float'>
[DEBUG] signal_step 解析失败，原始输出: {"next_phase_id": 3, "green_sec": 0.01}
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~548000.00UPS, TraCI: 48ms, vehicles TOT 767 ACT 548 BUF 
  - 类型错误: next_phase_id=<class 'int'>, green_sec=<class 'float'>
[DEBUG] signal_step 解析失败，原始输出: {"next_phase_id": 3, "green_sec": 0.5}
[DEBUG] next_phase_id=2 不在 phase_ids=[1, 3]
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~548000.00UPS, TraCI: 48ms, vehicles TOT 767 ACT 548 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~548000.00UPS, TraCI: 49ms, vehicles TOT 767 ACT 548 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (23ms ~= 43.48*RT, ~32739.13UPS, TraCI: 48ms, vehicles TOT 973 ACT 753 BUF 21
Step #411.00 (2ms ~= 500.00*RT, ~387000.00UPS, TraCI: 0ms, vehicles TOT 1020 ACT 774 BUF 1

 51%|█████     | 51/100 [02:36<02:18,  2.82s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
  - green_sec <= 0: 0
[DEBUG] signal_step 解析失败，原始输出: ```json
{
  "next_phase_id": 3,
  "green_sec": 0
}
```
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~291000.00UPS, TraCI: 65ms, vehicles TOT 866 ACT 582 BUF 0
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 1ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (31ms ~= 32.26*RT, ~27548.39UPS, TraCI: 64ms, vehicles TOT 1140 ACT 854 BUF 1
Step #459.00 (3ms ~= 333.33*RT, ~288333.33UPS, TraCI: 0ms, vehicles TOT 1187 ACT 865 BUF 7
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (2ms ~= 500.00*RT, ~164000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1)
Step #300.00 (31ms ~= 32.26*RT, ~27548.39UPS, TraCI: 64ms, vehicles TOT 1140 ACT 854 BUF 1
Step #498.00 (3ms ~= 333.33*RT, ~287333.33UPS, TraCI: 0ms, vehicles TOT 1258 ACT 862 BUF 1
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (31ms ~= 32.26*RT, ~27548.39UPS, TraCI: 65ms, vehicles TOT 1140 ACT 854 BUF 1
Step #498.00 (3ms ~= 333.33*RT, ~288333.33UPS, TraCI: 1ms, vehicles TOT 1259 ACT 865 BUF 9

 52%|█████▏    | 52/100 [02:39<02:15,  2.83s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~338000.00UPS, TraCI: 66ms, vehicles TOT 1491 ACT 676 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~338000.00UPS, TraCI: 65ms, vehicles TOT 1491 ACT 676 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~676000.00UPS, TraCI: 65ms, vehicles TOT 1491 ACT 676 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~676000.00UPS, TraCI: 65ms, vehicles TOT 1491 ACT 676 BUF

 53%|█████▎    | 53/100 [02:42<02:11,  2.79s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumoDEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo

Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (23ms ~= 43.48*RT, ~31913.04UPS, TraCI: 48ms, vehicles TOT 948 ACT 734 BUF 20
Step #403.00 (3ms ~= 333.33*RT, ~254666.67UPS, TraCI: 1ms, vehicles TOT 998 ACT 764 BUF 7)
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (24ms ~= 41.67*RT, ~30583.33UPS, TraCI: 47ms, vehicles TOT 948 ACT 734 BUF 20
Step #395.00 (3ms ~= 333.33*RT, ~254000.00UPS, TraCI: 1ms, vehicles TOT 984 ACT 762 BUF 7)
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (2ms ~= 500.00*RT, ~164000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1)
Step #300.00 (23ms ~= 43.48*RT, ~31913.04UPS, TraCI: 48ms, vehicles TOT 948 ACT 734 BUF 20
Step #415.00 (3ms ~= 333.33*RT, ~257000.00UPS, TraCI: 0ms, vehicles TOT 1023 ACT 771 BUF 1
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (2ms ~= 500.00*RT, ~164000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1)
Step #300.00 (23ms ~= 43.48*RT, ~31913.04UPS, TraCI: 48ms, vehicles TOT 948 ACT 734 BUF 20
Step #415.00 (2ms ~= 500.00*RT, ~384500.00UPS, TraCI: 0ms, vehicles TOT 1022 ACT 769 BUF 1

 54%|█████▍    | 54/100 [02:45<02:06,  2.76s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo Retrying in 1 seconds

Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 1ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~298000.00UPS, TraCI: 52ms, vehicles TOT 1168 ACT 596 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~298000.00UPS, TraCI: 51ms, vehicles TOT 1168 ACT 596 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~298000.00UPS, TraCI: 51ms, vehicles TOT 1168 ACT 596 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (2ms ~= 500.00*RT, ~164000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1)
Step #300.00 (2ms ~= 500.00*RT, ~298000.00UPS, TraCI: 52ms, vehicles TOT 1168 ACT 596 BUF 

 55%|█████▌    | 55/100 [02:47<02:03,  2.75s/it]{'loss': 0.0, 'grad_norm': 0.0013275146484375, 'learning_rate': 1.84e-06, 'num_tokens': 188905.0, 'completions/mean_length': 19.55, 'completions/min_length': 16.0, 'completions/max_length': 23.6, 'completions/clipped_ratio': 0.0, 'completions/mean_terminated_length': 19.55, 'completions/min_terminated_length': 16.0, 'completions/max_terminated_length': 23.6, 'rewards/tsc_reward_fn/mean': -0.5082931280136108, 'rewards/tsc_reward_fn/std': 0.9702445030212402, 'reward': -0.5082931280136108, 'reward_std': 0.9702444791793823, 'frac_reward_zero_std': 0.4, 'completion_length': 19.55, 'kl': 0.0011865794374898541, 'step_time': 2.69120678579784, 'epoch': 0.55}

                                                

 55%|█████▌    | 55/100 [02:47<02:03,  2.75s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds Retrying in 1 seconds

Successfully connected to SUMOSuccessfully connected to SUMOSuccessfully connected to SUMO


Starting warmup phase...
Starting warmup phase...Starting warmup phase...

Warmup progress: 0/300Warmup progress: 0/300Warmup progress: 0/300


Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (31ms ~= 32.26*RT, ~26129.03UPS, TraCI: 65ms, vehicles TOT 1080 ACT 810 BUF 2
Step #436.00 (4ms ~= 250.00*RT, ~210250.00UPS, TraCI: 0ms, vehicles TOT 1123 ACT 841 BUF 1
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (31ms ~= 32.26*RT, ~26129.03UPS, TraCI: 65ms, vehicles TOT 1080 ACT 810 BUF 2
Step #436.00 (4ms ~= 250.00*RT, ~210250.00UPS, TraCI: 0ms, vehicles TOT 1123 ACT 841 BUF 1
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 1ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (30ms ~= 33.33*RT, ~27000.00UPS, TraCI: 66ms, vehicles TOT 1080 ACT 810 BUF 2
Step #441.00 (4ms ~= 250.00*RT, ~212000.00UPS, TraCI: 0ms, vehicles TOT 1136 ACT 848 BUF 8
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (32ms ~= 31.25*RT, ~25312.50UPS, TraCI: 65ms, vehicles TOT 1080 ACT 810 BUF 2
Step #450.00 (2ms ~= 500.00*RT, ~425000.00UPS, TraCI: 1ms, vehicles TOT 1151 ACT 850 BUF 6

 56%|█████▌    | 56/100 [02:50<02:01,  2.75s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (2ms ~= 500.00*RT, ~164000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1)
Step #300.00 (1ms ~= 1000.00*RT, ~613000.00UPS, TraCI: 72ms, vehicles TOT 1307 ACT 613 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~613000.00UPS, TraCI: 71ms, vehicles TOT 1307 ACT 613 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~613000.00UPS, TraCI: 71ms, vehicles TOT 1307 ACT 613 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~306500.00UPS, TraCI: 70ms, vehicles TOT 1307 ACT 613 BUF 

 57%|█████▋    | 57/100 [02:53<01:58,  2.75s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMOSuccessfully connected to SUMO

Starting warmup phase...
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
  - green_sec <= 0: 0
[DEBUG] signal_step 解析失败，原始输出: {"next_phase_id": 1, "green_sec": 0}
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~275500.00UPS, TraCI: 48ms, vehicles TOT 772 ACT 551 BUF 0
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (2ms ~= 500.00*RT, ~164000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1)
Step #300.00 (23ms ~= 43.48*RT, ~32956.52UPS, TraCI: 48ms, vehicles TOT 979 ACT 758 BUF 17
Step #404.00 (3ms ~= 333.33*RT, ~256666.67UPS, TraCI: 0ms, vehicles TOT 1004 ACT 770 BUF 1
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (24ms ~= 41.67*RT, ~31583.33UPS, TraCI: 47ms, vehicles TOT 979 ACT 758 BUF 17
Step #426.00 (2ms ~= 500.00*RT, ~389500.00UPS, TraCI: 0ms, vehicles TOT 1046 ACT 779 BUF 9
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (23ms ~= 43.48*RT, ~32956.52UPS, TraCI: 47ms, vehicles TOT 979 ACT 758 BUF 17
Step #426.00 (2ms ~= 500.00*RT, ~389500.00UPS, TraCI: 1ms, vehicles TOT 1046 ACT 779 BUF 9

 58%|█████▊    | 58/100 [02:56<01:55,  2.74s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 1ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~579000.00UPS, TraCI: 65ms, vehicles TOT 900 ACT 579 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~579000.00UPS, TraCI: 64ms, vehicles TOT 900 ACT 579 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~579000.00UPS, TraCI: 63ms, vehicles TOT 900 ACT 579 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~579000.00UPS, TraCI: 63ms, vehicles TOT 900 ACT 579 BUF 

 59%|█████▉    | 59/100 [02:58<01:52,  2.74s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds Retrying in 1 seconds

 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (32ms ~= 31.25*RT, ~26843.75UPS, TraCI: 64ms, vehicles TOT 1176 ACT 859 BUF 3
Step #470.00 (4ms ~= 250.00*RT, ~223500.00UPS, TraCI: 1ms, vehicles TOT 1237 ACT 894 BUF 1
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 1ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (32ms ~= 31.25*RT, ~26843.75UPS, TraCI: 62ms, vehicles TOT 1176 ACT 859 BUF 3
Step #490.00 (3ms ~= 333.33*RT, ~297333.33UPS, TraCI: 0ms, vehicles TOT 1274 ACT 892 BUF 1
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (32ms ~= 31.25*RT, ~26843.75UPS, TraCI: 63ms, vehicles TOT 1176 ACT 859 BUF 3
Step #515.00 (3ms ~= 333.33*RT, ~301000.00UPS, TraCI: 1ms, vehicles TOT 1327 ACT 903 BUF 9
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (31ms ~= 32.26*RT, ~27709.68UPS, TraCI: 63ms, vehicles TOT 1176 ACT 859 BUF 3
Step #521.00 (3ms ~= 333.33*RT, ~298000.00UPS, TraCI: 0ms, vehicles TOT 1333 ACT 894 BUF 9

 60%|██████    | 60/100 [03:01<01:52,  2.81s/it]{'loss': 0.0, 'grad_norm': 5.96875, 'learning_rate': 1.6399999999999998e-06, 'num_tokens': 205970.0, 'completions/mean_length': 20.45, 'completions/min_length': 18.4, 'completions/max_length': 24.2, 'completions/clipped_ratio': 0.0, 'completions/mean_terminated_length': 20.45, 'completions/min_terminated_length': 18.4, 'completions/max_terminated_length': 24.2, 'rewards/tsc_reward_fn/mean': -0.5006726503372192, 'rewards/tsc_reward_fn/std': 1.3941056549549102, 'reward': -0.5006726503372192, 'reward_std': 1.394105648994446, 'frac_reward_zero_std': 0.4, 'completion_length': 20.45, 'kl': 0.0010413403848360757, 'step_time': 2.7519163490040226, 'epoch': 0.6}

                                                

 60%|██████    | 60/100 [03:01<01:52,  2.81s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~703000.00UPS, TraCI: 62ms, vehicles TOT 1609 ACT 703 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~703000.00UPS, TraCI: 62ms, vehicles TOT 1609 ACT 703 BUF
  - 提取的不是dict: <class 'NoneType'>
[DEBUG] extend_decision 解析失败，原始输出: 为了帮助你决定是否需要延长当前绿灯相位，我需要先根据输入的 scenario 和 state 获取相位的绿灯时长、当前绿灯时长、当前是否可以切换绿灯以及其他相关信息。由于我无法直接获取这些数据，我将基于现有的假设来解释如何判断需要延长相位。

首先，我需要验证当前绿灯相位的时长。如果绿灯相位已经足够长，那么不需要延长；如果绿灯相位非常短（如"3"），则需要考虑是否可以延长。

基于输入的 phase_order 和 state，我们可以判断以下几种
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~703000.00UPS, TraCI: 61ms, vehicles TOT 1609 ACT 703 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 1ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~703000.00UPS, TraCI: 62ms, vehicles TOT 1609 ACT 703 BUF
Unsloth: Will smartly offload gradients to save VRAM!

 61%|██████    | 61/100 [03:06<02:13,  3.41s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~290500.00UPS, TraCI: 53ms, vehicles TOT 1107 ACT 581 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~581000.00UPS, TraCI: 54ms, vehicles TOT 1107 ACT 581 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~581000.00UPS, TraCI: 53ms, vehicles TOT 1107 ACT 581 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~581000.00UPS, TraCI: 53ms, vehicles TOT 1107 ACT 581 BUF

 62%|██████▏   | 62/100 [03:09<02:01,  3.20s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMOSuccessfully connected to SUMO

Starting warmup phase...
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
  - green_sec <= 0: 0
[DEBUG] signal_step 解析失败，原始输出: {"next_phase_id": 1, "green_sec": 0}
  - green_sec <= 0: 0
[DEBUG] signal_step 解析失败，原始输出: {"next_phase_id": 3, "green_sec": 0}
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~294000.00UPS, TraCI: 57ms, vehicles TOT 1046 ACT 588 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (2ms ~= 500.00*RT, ~164000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1)
Step #300.00 (2ms ~= 500.00*RT, ~294000.00UPS, TraCI: 56ms, vehicles TOT 1046 ACT 588 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (34ms ~= 29.41*RT, ~30000.00UPS, TraCI: 56ms, vehicles TOT 1479 ACT 1020 BUF 
Step #551.00 (4ms ~= 250.00*RT, ~257500.00UPS, TraCI: 1ms, vehicles TOT 1522 ACT 1030 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (32ms ~= 31.25*RT, ~31875.00UPS, TraCI: 57ms, vehicles TOT 1479 ACT 1020 BUF 
Step #551.00 (3ms ~= 333.33*RT, ~343333.33UPS, TraCI: 1ms, vehicles TOT 1522 ACT 1030 BUF 

 63%|██████▎   | 63/100 [03:11<01:51,  3.02s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo

Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumoDEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo

Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0

 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds Retrying in 1 seconds

Successfully connected to SUMOSuccessfully connected to SUMO

Starting warmup phase...
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
[DEBUG] next_phase_id=3858790114 不在 phase_ids=[1, 3]
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~584000.00UPS, TraCI: 62ms, vehicles TOT 971 ACT 584 BUF 
[DEBUG] next_phase_id=3858789815 不在 phase_ids=[1, 3]
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (2ms ~= 500.00*RT, ~90500.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1) 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~584000.00UPS, TraCI: 59ms, vehicles TOT 971 ACT 584 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (32ms ~= 31.25*RT, ~29312.50UPS, TraCI: 61ms, vehicles TOT 1328 ACT 938 BUF 4
Step #527.00 (3ms ~= 333.33*RT, ~322000.00UPS, TraCI: 1ms, vehicles TOT 1410 ACT 966 BUF 1
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (32ms ~= 31.25*RT, ~29312.50UPS, TraCI: 60ms, vehicles TOT 1328 ACT 938 BUF 4
Step #547.00 (3ms ~= 333.33*RT, ~322666.67UPS, TraCI: 0ms, vehicles TOT 1447 ACT 968 BUF 1

 64%|██████▍   | 64/100 [03:14<01:47,  2.98s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumoDEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo

Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0

 Retrying in 1 seconds Retrying in 1 seconds

DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~643000.00UPS, TraCI: 69ms, vehicles TOT 1381 ACT 643 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~321500.00UPS, TraCI: 68ms, vehicles TOT 1381 ACT 643 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~643000.00UPS, TraCI: 69ms, vehicles TOT 1381 ACT 643 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~643000.00UPS, TraCI: 68ms, vehicles TOT 1381 ACT 643 BUF

 65%|██████▌   | 65/100 [03:19<02:02,  3.51s/it]
                                                

 65%|██████▌   | 65/100 [03:19<02:02,  3.51s/it]{'loss': 0.0, 'grad_norm': 0.00113677978515625, 'learning_rate': 1.44e-06, 'num_tokens': 224708.0, 'completions/mean_length': 31.1, 'completions/min_length': 17.0, 'completions/max_length': 65.0, 'completions/clipped_ratio': 0.1, 'completions/mean_terminated_length': 20.21666717529297, 'completions/min_terminated_length': 17.0, 'completions/max_terminated_length': 22.8, 'rewards/tsc_reward_fn/mean': -1.4349999904632569, 'rewards/tsc_reward_fn/std': 0.7401551723480224, 'reward': -1.4349999904632569, 'reward_std': 0.7401551723480224, 'frac_reward_zero_std': 0.6, 'completion_length': 31.1, 'kl': 0.0027056579463533128, 'step_time': 3.516423022199888, 'epoch': 0.65}
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds Retrying in 1 seconds

 Retrying in 1 seconds
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 1ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (30ms ~= 33.33*RT, ~26533.33UPS, TraCI: 67ms, vehicles TOT 1057 ACT 796 BUF 3
Step #440.00 (3ms ~= 333.33*RT, ~280000.00UPS, TraCI: 1ms, vehicles TOT 1126 ACT 840 BUF 7
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (30ms ~= 33.33*RT, ~26533.33UPS, TraCI: 66ms, vehicles TOT 1057 ACT 796 BUF 3
Step #443.00 (3ms ~= 333.33*RT, ~280333.33UPS, TraCI: 0ms, vehicles TOT 1130 ACT 841 BUF 7
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (31ms ~= 32.26*RT, ~25677.42UPS, TraCI: 65ms, vehicles TOT 1057 ACT 796 BUF 3
Step #440.00 (2ms ~= 500.00*RT, ~420000.00UPS, TraCI: 0ms, vehicles TOT 1126 ACT 840 BUF 7
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (31ms ~= 32.26*RT, ~25677.42UPS, TraCI: 65ms, vehicles TOT 1057 ACT 796 BUF 3
Step #440.00 (2ms ~= 500.00*RT, ~420000.00UPS, TraCI: 0ms, vehicles TOT 1126 ACT 840 BUF 7

 66%|██████▌   | 66/100 [03:22<01:51,  3.29s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumoDEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo

Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0

DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 1ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (33ms ~= 30.30*RT, ~29696.97UPS, TraCI: 59ms, vehicles TOT 1386 ACT 980 BUF 3
Step #543.00 (5ms ~= 200.00*RT, ~197400.00UPS, TraCI: 0ms, vehicles TOT 1457 ACT 987 BUF 8
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 1ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (32ms ~= 31.25*RT, ~30625.00UPS, TraCI: 61ms, vehicles TOT 1386 ACT 980 BUF 3
Step #565.00 (4ms ~= 250.00*RT, ~246500.00UPS, TraCI: 1ms, vehicles TOT 1509 ACT 986 BUF 1
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (33ms ~= 30.30*RT, ~29696.97UPS, TraCI: 60ms, vehicles TOT 1386 ACT 980 BUF 3
Step #565.00 (3ms ~= 333.33*RT, ~328666.67UPS, TraCI: 1ms, vehicles TOT 1509 ACT 986 BUF 1
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (2ms ~= 500.00*RT, ~164000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1)
Step #300.00 (33ms ~= 30.30*RT, ~29696.97UPS, TraCI: 62ms, vehicles TOT 1386 ACT 980 BUF 3
Step #561.00 (3ms ~= 333.33*RT, ~327666.67UPS, TraCI: 1ms, vehicles TOT 1495 ACT 983 BUF 1

 67%|██████▋   | 67/100 [03:25<01:44,  3.18s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumoDEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo

DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0

 Retrying in 1 seconds
 Retrying in 1 seconds Retrying in 1 seconds

 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (2ms ~= 500.00*RT, ~164000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1)
Step #300.00 (32ms ~= 31.25*RT, ~29968.75UPS, TraCI: 60ms, vehicles TOT 1355 ACT 959 BUF 4
Step #526.00 (4ms ~= 250.00*RT, ~244250.00UPS, TraCI: 0ms, vehicles TOT 1419 ACT 977 BUF 9
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (32ms ~= 31.25*RT, ~29968.75UPS, TraCI: 60ms, vehicles TOT 1355 ACT 959 BUF 4
Step #521.00 (5ms ~= 200.00*RT, ~196600.00UPS, TraCI: 0ms, vehicles TOT 1411 ACT 983 BUF 1
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 1ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (33ms ~= 30.30*RT, ~29060.61UPS, TraCI: 60ms, vehicles TOT 1355 ACT 959 BUF 4
Step #569.00 (3ms ~= 333.33*RT, ~323333.33UPS, TraCI: 0ms, vehicles TOT 1504 ACT 970 BUF 1
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (33ms ~= 30.30*RT, ~29060.61UPS, TraCI: 59ms, vehicles TOT 1355 ACT 959 BUF 4
Step #569.00 (3ms ~= 333.33*RT, ~323333.33UPS, TraCI: 0ms, vehicles TOT 1504 ACT 970 BUF 1

 68%|██████▊   | 68/100 [03:28<01:38,  3.09s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumoDEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo

Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0

 Retrying in 1 seconds
 Retrying in 1 seconds
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds Retrying in 1 seconds

Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300Warmup progress: 0/300

Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 1ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~590000.00UPS, TraCI: 59ms, vehicles TOT 1024 ACT 590 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~295000.00UPS, TraCI: 57ms, vehicles TOT 1024 ACT 590 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~295000.00UPS, TraCI: 58ms, vehicles TOT 1024 ACT 590 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~590000.00UPS, TraCI: 58ms, vehicles TOT 1024 ACT 590 BUF

 69%|██████▉   | 69/100 [03:30<01:32,  2.98s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds Retrying in 1 seconds

 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMOSuccessfully connected to SUMO

Starting warmup phase...Starting warmup phase...

Warmup progress: 0/300Warmup progress: 0/300

Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 1ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~580000.00UPS, TraCI: 56ms, vehicles TOT 1058 ACT 580 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~290000.00UPS, TraCI: 55ms, vehicles TOT 1058 ACT 580 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~580000.00UPS, TraCI: 56ms, vehicles TOT 1058 ACT 580 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~580000.00UPS, TraCI: 56ms, vehicles TOT 1058 ACT 580 BUF

 70%|███████   | 70/100 [03:33<01:26,  2.90s/it]
                                                

 70%|███████   | 70/100 [03:33<01:26,  2.90s/it]{'loss': 0.0, 'grad_norm': 0.000598907470703125, 'learning_rate': 1.24e-06, 'num_tokens': 240722.0, 'completions/mean_length': 19.9, 'completions/min_length': 15.6, 'completions/max_length': 23.8, 'completions/clipped_ratio': 0.0, 'completions/mean_terminated_length': 19.9, 'completions/min_terminated_length': 15.6, 'completions/max_terminated_length': 23.8, 'rewards/tsc_reward_fn/mean': 0.15, 'rewards/tsc_reward_fn/std': 0.7, 'reward': 0.15, 'reward_std': 0.7, 'frac_reward_zero_std': 0.4, 'completion_length': 19.9, 'kl': 0.0023361253195616884, 'step_time': 2.7679034242057243, 'epoch': 0.7}
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
  - 类型错误: next_phase_id=<class 'int'>, green_sec=<class 'float'>
[DEBUG] signal_step 解析失败，原始输出: {"next_phase_id": 3, "green_sec": 3.0}
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~581000.00UPS, TraCI: 64ms, vehicles TOT 879 ACT 581 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (31ms ~= 32.26*RT, ~28032.26UPS, TraCI: 64ms, vehicles TOT 1169 ACT 869 BUF 1
Step #462.00 (4ms ~= 250.00*RT, ~219000.00UPS, TraCI: 0ms, vehicles TOT 1205 ACT 876 BUF 8
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (31ms ~= 32.26*RT, ~28032.26UPS, TraCI: 64ms, vehicles TOT 1169 ACT 869 BUF 1
Step #466.00 (3ms ~= 333.33*RT, ~293000.00UPS, TraCI: 0ms, vehicles TOT 1216 ACT 879 BUF 1
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (31ms ~= 32.26*RT, ~28032.26UPS, TraCI: 63ms, vehicles TOT 1169 ACT 869 BUF 1
Step #479.00 (3ms ~= 333.33*RT, ~291666.67UPS, TraCI: 0ms, vehicles TOT 1237 ACT 875 BUF 1

 71%|███████   | 71/100 [03:36<01:21,  2.82s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (34ms ~= 29.41*RT, ~31470.59UPS, TraCI: 53ms, vehicles TOT 1595 ACT 1070 BUF 
Step #588.00 (5ms ~= 200.00*RT, ~223000.00UPS, TraCI: 1ms, vehicles TOT 1668 ACT 1115 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (34ms ~= 29.41*RT, ~31470.59UPS, TraCI: 52ms, vehicles TOT 1595 ACT 1070 BUF 
Step #588.00 (4ms ~= 250.00*RT, ~278750.00UPS, TraCI: 1ms, vehicles TOT 1668 ACT 1115 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (34ms ~= 29.41*RT, ~31470.59UPS, TraCI: 54ms, vehicles TOT 1595 ACT 1070 BUF 
Step #598.00 (4ms ~= 250.00*RT, ~279000.00UPS, TraCI: 1ms, vehicles TOT 1695 ACT 1116 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (34ms ~= 29.41*RT, ~31470.59UPS, TraCI: 52ms, vehicles TOT 1595 ACT 1070 BUF 
Step #598.00 (3ms ~= 333.33*RT, ~372000.00UPS, TraCI: 0ms, vehicles TOT 1695 ACT 1116 BUF 

 72%|███████▏  | 72/100 [03:39<01:19,  2.83s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumoDEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo

Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0

DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~302000.00UPS, TraCI: 76ms, vehicles TOT 1213 ACT 604 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~604000.00UPS, TraCI: 75ms, vehicles TOT 1213 ACT 604 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~302000.00UPS, TraCI: 75ms, vehicles TOT 1213 ACT 604 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~604000.00UPS, TraCI: 75ms, vehicles TOT 1213 ACT 604 BUF

 73%|███████▎  | 73/100 [03:41<01:15,  2.80s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
  - green_sec <= 0: 0
[DEBUG] signal_step 解析失败，原始输出: {"next_phase_id": 3, "green_sec": 0}
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~556000.00UPS, TraCI: 67ms, vehicles TOT 791 ACT 556 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (30ms ~= 33.33*RT, ~25633.33UPS, TraCI: 67ms, vehicles TOT 1006 ACT 769 BUF 2
Step #425.00 (2ms ~= 500.00*RT, ~395500.00UPS, TraCI: 1ms, vehicles TOT 1060 ACT 791 BUF 8
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (30ms ~= 33.33*RT, ~25633.33UPS, TraCI: 67ms, vehicles TOT 1006 ACT 769 BUF 2
Step #482.00 (3ms ~= 333.33*RT, ~270000.00UPS, TraCI: 0ms, vehicles TOT 1181 ACT 810 BUF 8
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (30ms ~= 33.33*RT, ~25633.33UPS, TraCI: 66ms, vehicles TOT 1006 ACT 769 BUF 2
Step #470.00 (4ms ~= 250.00*RT, ~203750.00UPS, TraCI: 0ms, vehicles TOT 1159 ACT 815 BUF 8

 74%|███████▍  | 74/100 [03:44<01:14,  2.86s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumoDEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo

Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0

DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds Retrying in 1 seconds

 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
  - green_sec <= 0: 0
[DEBUG] signal_step 解析失败，原始输出: {"next_phase_id": 1, "green_sec": 0}
[DEBUG] next_phase_id=2 不在 phase_ids=[1, 3]
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~535000.00UPS, TraCI: 49ms, vehicles TOT 743 ACT 535 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~535000.00UPS, TraCI: 48ms, vehicles TOT 743 ACT 535 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (24ms ~= 41.67*RT, ~30250.00UPS, TraCI: 48ms, vehicles TOT 937 ACT 726 BUF 20
Step #400.00 (2ms ~= 500.00*RT, ~379500.00UPS, TraCI: 1ms, vehicles TOT 990 ACT 759 BUF 9)
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (23ms ~= 43.48*RT, ~31565.22UPS, TraCI: 48ms, vehicles TOT 937 ACT 726 BUF 20
Step #408.00 (2ms ~= 500.00*RT, ~380000.00UPS, TraCI: 1ms, vehicles TOT 1004 ACT 760 BUF 9

 75%|███████▌  | 75/100 [03:47<01:10,  2.81s/it]
                                                

 75%|███████▌  | 75/100 [03:47<01:10,  2.81s/it]{'loss': 0.0, 'grad_norm': 3.015625, 'learning_rate': 1.04e-06, 'num_tokens': 257056.0, 'completions/mean_length': 18.7, 'completions/min_length': 15.8, 'completions/max_length': 22.4, 'completions/clipped_ratio': 0.0, 'completions/mean_terminated_length': 18.7, 'completions/min_terminated_length': 15.8, 'completions/max_terminated_length': 22.4, 'rewards/tsc_reward_fn/mean': 0.4598914623260498, 'rewards/tsc_reward_fn/std': 1.8852862939238548, 'reward': 0.4598914623260498, 'reward_std': 1.8852862939238548, 'frac_reward_zero_std': 0.2, 'completion_length': 18.7, 'kl': 0.00195437409565784, 'step_time': 2.7441984460048845, 'epoch': 0.75}
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~624000.00UPS, TraCI: 75ms, vehicles TOT 1269 ACT 624 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~312000.00UPS, TraCI: 73ms, vehicles TOT 1269 ACT 624 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~624000.00UPS, TraCI: 74ms, vehicles TOT 1269 ACT 624 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~624000.00UPS, TraCI: 74ms, vehicles TOT 1269 ACT 624 BUF

 76%|███████▌  | 76/100 [03:50<01:07,  2.81s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds Retrying in 1 seconds

 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~632000.00UPS, TraCI: 70ms, vehicles TOT 1352 ACT 632 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 1ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~632000.00UPS, TraCI: 71ms, vehicles TOT 1352 ACT 632 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~632000.00UPS, TraCI: 70ms, vehicles TOT 1352 ACT 632 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~316000.00UPS, TraCI: 69ms, vehicles TOT 1352 ACT 632 BUF 

 77%|███████▋  | 77/100 [03:52<01:04,  2.79s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~305500.00UPS, TraCI: 74ms, vehicles TOT 1251 ACT 611 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~611000.00UPS, TraCI: 73ms, vehicles TOT 1251 ACT 611 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~611000.00UPS, TraCI: 75ms, vehicles TOT 1251 ACT 611 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~305500.00UPS, TraCI: 72ms, vehicles TOT 1251 ACT 611 BUF 

 78%|███████▊  | 78/100 [03:55<01:01,  2.78s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumoDEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo

Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0

DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMOSuccessfully connected to SUMO

Starting warmup phase...Starting warmup phase...

Warmup progress: 0/300
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~298000.00UPS, TraCI: 55ms, vehicles TOT 1125 ACT 596 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~596000.00UPS, TraCI: 54ms, vehicles TOT 1125 ACT 596 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~596000.00UPS, TraCI: 55ms, vehicles TOT 1125 ACT 596 BUF
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~298000.00UPS, TraCI: 54ms, vehicles TOT 1125 ACT 596 BUF 

 79%|███████▉  | 79/100 [03:58<00:58,  2.76s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumoDEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo

Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0

 Retrying in 1 seconds Retrying in 1 seconds

DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMO
Starting warmup phase...
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300Warmup progress: 0/300

Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
[DEBUG] next_phase_id=399227244 不在 phase_ids=[1, 3]
[DEBUG] next_phase_id=399226823 不在 phase_ids=[1, 3]
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (2ms ~= 500.00*RT, ~269500.00UPS, TraCI: 48ms, vehicles TOT 755 ACT 539 BUF 0
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1)                 
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (1ms ~= 1000.00*RT, ~539000.00UPS, TraCI: 48ms, vehicles TOT 755 ACT 539 BUF 
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 0ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (22ms ~= 45.45*RT, ~33454.55UPS, TraCI: 49ms, vehicles TOT 953 ACT 736 BUF 23
Step #409.00 (2ms ~= 500.00*RT, ~385000.00UPS, TraCI: 0ms, vehicles TOT 1012 ACT 770 BUF 9
Step #0.00 (0ms ?*RT. ?UPS, TraCI: 1ms, vehicles TOT 0 ACT 0 BUF 0)                       
Step #100.00 (1ms ~= 1000.00*RT, ~181000.00UPS, TraCI: 0ms, vehicles TOT 187 ACT 181 BUF 1
Step #200.00 (1ms ~= 1000.00*RT, ~328000.00UPS, TraCI: 0ms, vehicles TOT 370 ACT 328 BUF 1
Step #300.00 (23ms ~= 43.48*RT, ~32000.00UPS, TraCI: 48ms, vehicles TOT 953 ACT 736 BUF 23
Step #456.00 (2ms ~= 500.00*RT, ~392000.00UPS, TraCI: 1ms, vehicles TOT 1109 ACT 784 BUF 6

 80%|████████  | 80/100 [04:01<00:55,  2.78s/it]{'loss': 0.0, 'grad_norm': 5.21875, 'learning_rate': 8.399999999999999e-07, 'num_tokens': 275399.0, 'completions/mean_length': 20.55, 'completions/min_length': 18.0, 'completions/max_length': 23.6, 'completions/clipped_ratio': 0.0, 'completions/mean_terminated_length': 20.55, 'completions/min_terminated_length': 18.0, 'completions/max_terminated_length': 23.6, 'rewards/tsc_reward_fn/mean': -1.6538461565971374, 'rewards/tsc_reward_fn/std': 0.46553821563720704, 'reward': -1.6538461565971374, 'reward_std': 0.46553821563720704, 'frac_reward_zero_std': 0.8, 'completion_length': 20.55, 'kl': 0.005380698275985196, 'step_time': 2.736654176202137, 'epoch': 0.8}

                                                

 80%|████████  | 80/100 [04:01<00:55,  2.78s/it]DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
DEBUG: 使用的 SUMO 路径是: /usr/share/sumo/bin/sumo
Starting SUMO with command: /usr/share/sumo/bin/sumo -c /workspace/sumo_simulation/environments/chengdu/chengdu.sumocfg --step-length 1.0 --no-warnings true --start --device.rerouting.probability 0
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
 Retrying in 1 seconds
Successfully connected to SUMOSuccessfully connected to SUMO

Starting warmup phase...Starting warmup phase...

Warmup progress: 0/300
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Successfully connected to SUMO
Starting warmup phase...
Warmup progress: 0/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 100/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup progress: 200/300
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
Warmup completed. Starting real-time simulation.
  - green_sec <= 0: 0
[DEBUG] signal_step 解析失败，原始输出: ```json
{
    "next_phase_id": 3,
    "green_sec": 0
}
```
