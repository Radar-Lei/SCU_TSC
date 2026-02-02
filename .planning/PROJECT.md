# TSC GRPO 训练系统重构

## What This Is

一个基于GRPO的交通信号控制(TSC)策略训练系统。通过将SUMO仿真前置到数据生成阶段,生成包含两种决策结果的训练数据,简化GRPO训练流程,让模型学习在给定交通状态下做出最优的二元决策(延长当前相位/切换到下一相位)。

## Core Value

通过前置SUMO仿真到数据生成阶段,使GRPO训练时不需要实时调用仿真环境,从而大幅简化系统架构,提高代码可维护性。

## Current Milestone: v0.1 原型验证版

**目标:** 建立完整的离线强化学习训练流程,验证核心架构可行性

**目标功能:**
- 双动作仿真数据生成(延长/切换)
- 四元组数据格式标准化
- 多级格式奖励 + 连续TSC奖励
- SFT预训练 + GRPO训练端到端流程
- 并行数据生成
- 模型推理接口

## Requirements

### Validated

- ✓ SUMO交通仿真环境已配置 — existing
- ✓ Docker运行环境已就绪 — existing
- ✓ 基础的GRPO训练框架存在(参考Qwen3实现) — existing

### Active (v0.1)

- [ ] 数据生成: 双动作仿真器、状态保存/加载验证、并行生成、端口管理 (DG-01~11)
- [ ] 数据格式: GRPODataEntry标准化、JSON序列化、HF Dataset集成 (DF-01~07)
- [ ] Reward函数: 多级格式验证、连续TSC奖励、reward链、统计追踪 (RW-01~10)
- [ ] SFT预训练: 格式对齐训练、checkpoint保存 (SFT-01~04)
- [ ] GRPO训练: TRL/Unsloth集成、参数验证、日志监控、参考Qwen3框架 (TR-01~11)
- [ ] 模型推理: LoRA合并、16bit导出、推理接口 (IF-01~05)
- [ ] 代码架构: 目录重组、入口脚本、清理冗余 (AR-01~07)

### Out of Scope (v0.1)

- 实时SUMO仿真在GRPO训练循环中 — 这正是我们要消除的复杂性
- 硬编码的0/1 reward — 使用基于排队长度差异的连续reward更合理
- 多时刻历史状态 — v0.1只使用决策时刻的排队长度作为输入
- 多目标优化(等待时间、通行量等) — v0.1聚焦于排队长度单一指标
- Max Pressure基线对比 — v0.1不做算法对比,延后到v0.2+
- 并行SUMO奖励计算 — v0.1使用查表式奖励,延后到v0.2+
- WandB集成 — v0.1使用基础日志,延后到v0.2+

## Context

**现状:**
- 现有实现可工作但架构过于复杂,在GRPO训练时实时调用SUMO导致代码难以维护
- 发现决策本质是二元的(延长/切换),可以在数据生成时就模拟两种选择的结果
- 有可参考的Qwen3_(4B)_GRPO.ipynb实现

**核心洞察:**
固定时间间隔(5秒)决策一次,每次决策只需要当前排队长度作为输入,两种动作(延长/切换)都可以提前通过SUMO仿真得到结果状态,因此完全可以将仿真前置到数据生成阶段。

**技术背景:**
- SUMO(Simulation of Urban MObility)作为交通仿真引擎
- GRPO(Group Relative Policy Optimization)作为强化学习算法
- 必须在Docker容器中运行(通过docker/publish.sh)

## Constraints

- **运行环境**: 必须在Docker容器中运行 — SUMO环境依赖Docker配置
- **仿真引擎**: 必须使用现有SUMO环境和脚本 — 已配置且稳定
- **决策频率**: 固定5秒间隔决策 — 与现有系统保持一致
- **数据源**: 复用现有SUMO场景和路网配置 — 保证实验可比性

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| 将SUMO仿真前置到数据生成阶段 | 消除训练时的实时仿真调用,简化架构 | — Pending |
| 使用排队长度作为唯一状态/reward指标 | 决策每5秒发生,等待时间不适合,排队长度更直接反映交通状态 | — Pending |
| 采用连续reward而非0/1二元reward | 即使决策不是最优,也应根据实际差距给予分数,避免过于绝对的评价 | — Pending |
| 参考Qwen3_(4B)_GRPO.ipynb框架结构 | 已验证的GRPO实现,减少重新设计的风险 | — Pending |
| 数据格式为四元组(queue, next_queue_0, next_queue_1, metadata) | 简洁且包含训练所需的全部信息 | — Pending |
| 增加SFT预训练阶段 | 训练初期格式对齐,避免GRPO难以收敛 | — Pending |
| v0.1不包含Max Pressure基线对比 | 聚焦核心架构验证,算法对比延后到v0.2+ | — Pending |

---
*Last updated: 2026-02-03 after milestone v0.1 initialization*
