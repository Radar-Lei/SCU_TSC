# TSC-GRPO: 基于SUMO仿真的交通信号控制GRPO训练系统

## What This Is

一个使用GRPO（Group Relative Policy Optimization）强化学习算法微调大语言模型的交通信号控制系统。系统通过SUMO交通仿真环境训练Qwen2.5-0.5B-Instruct模型，使其能够根据实时交通状态做出智能信号灯相位延长决策，优化路口通行效率。

## Core Value

模型能够根据SUMO仿真状态的相位排队信息，准确判断是否延长当前绿灯相位，以最小化整个交叉口的排队车辆数。

## Requirements

### Validated

<!-- 已实现的功能组件 -->

- ✓ **GRPO数据集生成器** — 运行SUMO仿真，在决策点收集状态数据并保存仿真快照
- ✓ **SFT数据集生成器** — 从GRPO数据集生成监督学习格式数据，用于格式训练
- ✓ **SFT训练脚本** — 使用Unsloth对Qwen2.5-0.5B-Instruct进行LoRA微调，学习JSON输出格式
- ✓ **SUMO接口封装** — 封装SUMO TraCI接口，提供交通灯控制、状态查询、仿真步进等功能
- ✓ **Prompt构建器** — 构建符合任务要求的输入提示格式
- ✓ **基础配置管理** — GRPO数据生成的配置参数管理
- ✓ **并行场景处理** — 支持多场景并行生成数据集
- ✓ **Docker运行环境** — 容器化的训练环境配置

### Active

<!-- 当前需要实现的功能 -->

- [ ] **GRPO训练脚本** (`grpo_training.py`)
  - 实现完整的GRPO训练流程
  - 集成Unsloth和TRL库的GRPOTrainer
  - 支持从SFT模型继续训练
  - 实现reward函数链（format_reward_fn + tsc_reward_fn）
  - 支持多reward函数的组合训练
  - 实现训练过程中的模型保存和评估

- [ ] **Format Reward函数** (`format_reward_fn`)
  - 验证模型输出严格符合 `{"extend": "yes/no"}` 格式
  - 对格式错误给予负奖励
  - 支持容错匹配（允许空格、大小写变体）

- [ ] **TSC Reward函数** (`tsc_reward_fn`)
  - 实现Max Pressure算法作为baseline
  - 根据决策后的排队车辆数计算连续奖励
  - 支持从保存的仿真状态恢复并推进仿真
  - 实现"延长"和"切换"两种决策的仿真逻辑

- [ ] **Max Pressure算法实现**
  - 简单启发式：当前相位控制车道排队数 → 其他相位最大排队数
  - 如果当前相位排队数最大 → 建议延长
  - 否则 → 建议切换
  - 作为reward计算的基准参照

- [ ] **中央配置管理系统**
  - 配置文件：`training_config.yaml` 管理所有超参数
  - 支持命令行参数覆盖配置文件
  - SFT和GRPO训练的超参数统一管理
  - 支持不同场景/环境的配置切换

- [ ] **完整的一键运行流程**
  - 完善 `publish.sh` 确保四步流程无缝衔接
  - 每步的失败检测和错误处理
  - 进度日志和状态监控
  - 训练结果的验证和测试

- [ ] **数据验证和测试工具**
  - 验证生成的数据集格式正确性
  - 测试SUMO状态文件的加载和恢复
  - 单元测试：reward函数的边界情况
  - 集成测试：端到端的小规模训练验证

### Out of Scope

<!-- 明确不包含的功能 -->

- **多路口协同控制** — 当前仅支持单个交叉口的独立控制
- **动态相位顺序** — 相位执行顺序固定，不支持动态重排
- **其他强化学习算法** — 仅使用GRPO，不实现PPO、DQN等
- **实时在线训练** — 训练流程离线进行，不支持在线学习
- **模型推理服务** — 不包含模型部署和推理API的开发
- **可视化界面** — 不提供Web UI或可视化控制面板
- **多目标优化** — 仅优化排队车辆数，不考虑等待时间、油耗等

## Context

### 技术环境

- **基础模型**: Qwen2.5-0.5B-Instruct (instruct模型，非reasoner)
- **训练框架**: Unsloth + TRL (GRPOTrainer)
- **仿真环境**: SUMO (Simulation of Urban MObility)
- **硬件环境**: NVIDIA GPU（通过Docker容器访问）
- **编程语言**: Python 3.10+

### 仿真场景

- 场景目录: `/home/samuel/SCU_TSC/sumo_simulation/environments`
- 场景数量: 13个（12个arterial4x4变体 + 1个chengdu）
- 决策间隔: 可配置（默认5秒）
- 随机种子: 固定种子确保可复现性

### 训练流程

```
1. GRPO数据生成
   └─> 运行SUMO仿真，在每个决策点保存状态和prompt

2. SFT数据生成
   └─> 从GRPO数据采样，添加随机yes/no标签

3. SFT训练
   └─> 教会模型输出 {"extend": "yes/no"} 格式

4. GRPO训练
   └─> 基于reward信号优化决策能力
       ├─ format_reward_fn: 检查输出格式
       └─ tsc_reward_fn: 与max pressure比较，评估排队数变化
```

### 已知问题

- **SFT训练效果不佳**: 从 `.docker_sft_test.log` 观察，training loss下降但evaluation loss下降不明显
  - 可能原因：数据量不足（1000条采样）
  - 可能原因：随机标签导致学习信号弱
  - 可能原因：过拟合训练集

## Constraints

- **模型**: 必须使用Qwen2.5-0.5B-Instruct，不可更换为其他模型
- **格式**: 模型输出必须严格符合 `{"extend": "yes/no"}` JSON格式
- **仿真**: 决策评估必须基于SUMO仿真的真实推进，不可使用近似或模拟
- **相位**: 相位顺序固定，不可跳相、不可重排，只能延长或切换到下一相位
- **状态**: GRPO训练时必须从保存的XML状态文件恢复仿真
- **配置**: 所有超参数必须通过配置文件+命令行参数管理，便于调整
- **可复现性**: 数据生成和训练必须使用固定随机种子
- **Docker**: 完整流程必须能通过 `docker/publish.sh` 一键运行

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| 使用Instruct模型而非Reasoner | 项目目标是简单的二元决策（yes/no），不需要复杂推理链 | — Pending |
| SFT使用随机标签 | SFT仅用于格式学习，决策正确性由后续GRPO优化 | ⚠️ Revisit（效果不佳） |
| Reward与Max Pressure比较 | Max Pressure是经典交通控制算法，提供合理的baseline | — Pending |
| 串行数据生成 | GRPO数据 → SFT数据，依赖关系明确，简化流程 | ✓ Good |
| 配置文件+命令行参数 | 兼顾便利性和灵活性，便于实验不同超参数 | — Pending |
| 全场景全量训练 | 确保模型泛化性，避免过拟合特定场景 | — Pending |

---
*Last updated: 2025-02-02 after project initialization*
