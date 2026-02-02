# Feature Research

**Domain:** 离线强化学习训练系统(Offline RL Training System)
**Researched:** 2026-02-03
**Confidence:** HIGH

## Feature Landscape

### Table Stakes (Users Expect These)

Features users expect. Missing = product feels incomplete.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| 预生成仿真数据 | 系统核心价值:前置SUMO仿真,避免训练时实时调用 | HIGH | 需为每个决策点运行两次SUMO(延长/切换),记录结果状态 |
| 标准化数据格式 | 训练器需要一致的输入格式 | LOW | 四元组:(current_queue, next_queue_0, next_queue_1, metadata) |
| 格式验证与奖励 | GRPO需要验证模型输出格式并打分 | MEDIUM | 已有实现:format_reward_fn,支持strict/partial/invalid三级 |
| TSC领域奖励计算 | 评估决策质量的核心机制 | HIGH | 基于排队长度差异的连续reward,需并行SUMO仿真 |
| 批量数据生成 | 单个场景数据量不足以训练 | MEDIUM | 多场景并行生成,合并为训练集 |
| 训练状态保存 | 恢复训练或增量训练必需 | LOW | 使用标准checkpoint机制 |
| 模型推理接口 | 训练后需部署使用 | MEDIUM | 已有LoRA合并和16bit导出 |

### Differentiators (Competitive Advantage)

Features that set product apart. Not expected, but valued.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| 连续reward函数 | 比0/1二元reward更细粒度,即使不是最优也给予分数 | MEDIUM | 基于排队长度差异的比例计算,避免过于绝对的评价 |
| Max Pressure基线追踪 | 提供可解释的baseline,帮助理解模型决策质量 | MEDIUM | 已实现:batch_max_pressure_decision |
| 相对基线奖励 | 奖励相对于baseline的改进而非绝对值 | MEDIUM | use_relative_baseline配置项,已集成到reward链 |
| 并行SUMO奖励计算 | 训练时批量计算TSC reward不成为瓶颈 | HIGH | ParallelSUMORewardCalculator,多进程池 |
| 多级格式奖励 | 区分严格遵守/部分遵守/完全违反格式,渐进式引导 | LOW | strict(+1.0)/partial(-0.5)/invalid(-10.0) |
| 决策点自适应过滤 | 根据有效相位比例概率性保留数据,避免无意义样本 | MEDIUM | keep_probability = non_zero_phases / total_phases |
| 数据集分层划分 | 按决策有效性分层抽样,保证训练集质量平衡 | MEDIUM | stratified_split考虑can_extend和相位有效性 |
| 格式化JSON prompt | 结构化输入降低学习难度 | LOW | 统一crossing_id/as_of/phase_order格式 |

### Anti-Features (Commonly Requested, Often Problematic)

Features that seem good but create problems.

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| 实时SUMO仿真 | 看起来更"真实" | 1. 训练速度慢(每步都要启动SUMO) 2. 架构复杂(需管理SUMO进程池) 3. 调试困难(仿真环境不确定性) | 将仿真前置到数据生成阶段,训练时使用预生成数据 |
| 多时刻历史状态 | 想要更多上下文信息 | 1. 增加模型复杂度 2. 数据格式复杂 3. v1决策本质是当前时刻的二元选择 | v1聚焦当前排队长度,v2再考虑历史 |
| 硬编码0/1二元reward | 实现简单 | 过于绝对,无法反映"接近正确"的决策价值,训练信号稀疏 | 使用基于排队长度差异的连续reward |
| 多目标优化 | 想要优化等待时间/通行量等多指标 | 1. 目标冲突难以权衡 2. 增加reward函数复杂度 3. v1聚焦单一指标更易验证 | v1聚焦排队长度,验证后再扩展 |
| 所有决策点都保存状态 | 以为需要完整回放 | 磁盘空间浪费,实际上间隔保存(state_save_interval)即可 | 每N个决策点保存一次状态文件 |
| 完美格式强制 | 希望模型100%遵守格式 | 训练初期过于严格会导致无有效梯度,模型无法学习 | 多级格式奖励,渐进式引导 |
| 所有无效格式立即丢弃 | 想要"纯净"数据 | 训练初期大量样本被丢弃,损失训练信号 | 部分遵守格式也给予负奖励(partial_reward),引导而非惩罚 |
| 同步数据生成 | 实现简单 | 多场景生成慢,等待时间长 | 使用并行生成(parallel_runner.py) |

## Feature Dependencies

```
数据生成
    ├──requires──> SUMO仿真接口(sumo_interface.py)
    ├──requires──> 决策点识别(_is_decision_point)
    └──requires──> 相位排队数采集(get_all_phases_queue)

数据格式标准化
    ├──requires──> GRPODataEntry数据类
    ├──requires──> prompt_builder.py
    └──enables──> 训练数据加载(load_grpo_dataset)

格式验证与奖励
    ├──requires──> 正则表达式提取(extract_decision)
    ├──requires──> JSON严格解析
    └──enables──> 多级奖励机制

TSC领域奖励
    ├──requires──> 格式验证成功(提取出决策)
    ├──requires──> SUMO状态文件
    ├──requires──> 并行SUMO计算器(ParallelSUMORewardCalculator)
    └──enhances──> 最终奖励组合(format_weight + tsc_weight)

Max Pressure基线
    ├──requires──> 相位排队数据(从prompt提取)
    ├──requires──> 时间参数(green_elapsed, min_green, max_green)
    └──enables──> 相对基线奖励(use_relative_baseline)

并行数据生成
    ├──requires──> 端口分配机制(避免SUMO冲突)
    ├──requires──> 进程池管理
    └──enables──> 多场景快速生成

相对基线奖励
    ├──requires──> Max Pressure基线决策
    ├──requires──> TSC奖励计算
    └──conflicts──> 绝对奖励模式
```

### Dependency Notes

- **数据生成 requires SUMO仿真接口**: 必须先实现稳定的SUMO接口才能生成数据
- **TSC奖励 requires 格式验证**: 只有格式正确的输出才能计算TSC奖励,无效格式直接返回格式惩罚
- **相对基线奖励 requires Max Pressure**: 必须先计算baseline决策,才能计算相对改进
- **并行生成 requires 端口管理**: 避免多个SUMO实例端口冲突

## MVP Definition

### Launch With (v1 - 重构阶段)

Minimum viable product — what's needed to validate the concept.

- [x] **预生成仿真数据** — 核心价值,消除实时SUMO调用
  - 为每个决策点运行两次SUMO(延长action=0, 切换action=1)
  - 记录(current_queue, next_queue_0, next_queue_1, metadata)

- [x] **标准化数据格式** — 训练器输入
  - GRPODataEntry: id/scenario/junction_id/simulation_time/phase_info/queue_data
  - 四元组格式保存为JSON

- [x] **格式验证与奖励** — 基础训练信号
  - format_reward_fn: strict/partial/invalid三级
  - 正则提取决策:"yes"/"no"

- [x] **TSC领域奖励** — 评估决策质量
  - 基于排队长度差异的连续reward
  - 并行SUMO仿真计算

- [x] **奖励函数链** — 组合多个奖励源
  - format_weight × format_reward + tsc_weight × tsc_reward
  - 统计信息追踪(RewardStats)

- [ ] **参考Qwen3框架结构** — 已验证的实现
  - SFT预训练阶段(格式对齐)
  - GRPO训练阶段(策略优化)
  - 推理阶段(LoRA加载)

### Add After Validation (v1.x)

Features to add once core is working.

- [ ] **Max Pressure基线追踪** — 可解释性
  - trigger: v1训练完成后,需要理解模型决策质量
  - batch_max_pressure_decision批量计算
  - baseline准确率统计

- [ ] **相对基线奖励** — 引导模型超越baseline
  - trigger: 绝对reward训练效果不佳时启用
  - use_relative_baseline配置
  - reward = (model_decision_outcome - baseline_outcome) × scale

- [ ] **数据集分层划分** — 训练集质量
  - trigger: 发现训练数据分布不均衡
  - 按can_extend/相位有效性分层抽样
  - 保证训练/验证集平衡

- [ ] **WandB集成** — 训练监控
  - trigger: 需要可视化训练曲线和指标
  - use_wandb配置项
  - 自动记录reward/loss/baseline_accuracy

- [ ] **配置文件统一** — 维护便利性
  - trigger: 多个配置文件(grpo_config/training_config)混乱
  - 统一为training_config.yaml
  - 分段管理sft/grpo/simulation/reward配置

### Future Consideration (v2+)

Features to defer until product-market fit is established.

- [ ] **多时刻历史状态** — 更丰富的上下文
  - 延迟原因: v1决策本质是当前时刻二元选择,加入历史会增加复杂度
  - 实现: 扩展数据格式为(history_queues, current_queue, next_queue_0, next_queue_1)
  - 价值: 可能提升决策质量,但需验证v1效果

- [ ] **多目标优化** — 综合指标
  - 延迟原因: v1聚焦排队长度单一指标,验证后再扩展
  - 实现: reward = w1×queue + w2×waiting_time + w3×throughput
  - 价值: 更全面的交通优化,但权衡复杂

- [ ] **自适应reward权重** — 动态调整
  - 延迟原因: v1使用固定权重(format_weight/tsc_weight),v2可探索自适应
  - 实现: 根据训练进度动态调整format/tsc权重
  - 价值: 训练初期重格式,后期重TSC

- [ ] **Curriculum Learning** — 渐进式难度
  - 延迟原因: v1使用所有数据,v2可按难度排序
  - 实现: 简单场景(低流量) → 复杂场景(高流量/多路口)
  - 价值: 可能加速收敛,但需验证

- [ ] **模型蒸馏** — 部署优化
  - 延迟原因: v1关注训练效果,v2考虑部署效率
  - 实现: 将大模型蒸馏为小模型(便于嵌入式设备)
  - 价值: 实际部署需要,但非训练系统核心

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| 预生成仿真数据 | HIGH | HIGH | P1 |
| 标准化数据格式 | HIGH | LOW | P1 |
| 格式验证与奖励 | HIGH | MEDIUM | P1 |
| TSC领域奖励 | HIGH | HIGH | P1 |
| 奖励函数链 | HIGH | MEDIUM | P1 |
| 参考Qwen3框架 | HIGH | MEDIUM | P1 |
| Max Pressure基线 | MEDIUM | MEDIUM | P2 |
| 相对基线奖励 | MEDIUM | MEDIUM | P2 |
| 数据集分层划分 | MEDIUM | LOW | P2 |
| WandB集成 | LOW | LOW | P2 |
| 配置文件统一 | LOW | LOW | P2 |
| 多时刻历史 | MEDIUM | HIGH | P3 |
| 多目标优化 | MEDIUM | HIGH | P3 |
| 自适应权重 | LOW | MEDIUM | P3 |
| Curriculum Learning | LOW | MEDIUM | P3 |
| 模型蒸馏 | MEDIUM | HIGH | P3 |

**Priority key:**
- P1: Must have for launch (v1重构阶段)
- P2: Should have, add when possible (v1.x增强阶段)
- P3: Nice to have, future consideration (v2探索阶段)

## Competitor Feature Analysis

对比参考系统与目标系统:

| Feature | 现有实现(实时SUMO) | Qwen3_(4B)_GRPO.ipynb | 本系统(离线RL) |
|---------|-------------------|----------------------|---------------|
| 数据生成方式 | 训练时实时调用SUMO | 数学问题数据集(预生成) | SUMO预仿真生成四元组 |
| 决策空间 | 二元(延长/切换) | 生成式文本(推理过程) | 二元(延长/切换) |
| 格式验证 | 无(假设总是有效) | 多标签(reasoning_start/end/solution) | 三级(strict/partial/invalid) |
| 领域奖励 | 实时SUMO reward | 答案正确性验证 | 离线SUMO排队长度差异 |
| 基线对比 | 无 | 无 | Max Pressure算法baseline |
| 训练架构 | 复杂(GRPO+SUMO进程管理) | 简洁(GRPO+数据集) | 简洁(GRPO+预生成数据) |
| 可维护性 | 低(实时依赖复杂) | 高(纯数据驱动) | 高(仿真前置) |

**本系统优势:**
1. **架构简洁**: 借鉴Qwen3的纯数据驱动模式,消除实时SUMO复杂性
2. **领域专用**: 保留TSC特定的reward计算(排队长度/Max Pressure)
3. **可解释性**: Max Pressure baseline提供可解释的对比基准
4. **渐进引导**: 多级格式奖励,避免训练初期过于严格

## Domain-Specific Insights

### 交通信号控制(TSC)领域特性

1. **决策频率固定**: 5秒间隔决策,不同于一般RL的可变频率
2. **状态观测**: 排队长度是最直接的状态表示,比等待时间更适合短周期决策
3. **二元决策**: 每个决策点只有延长/切换两个动作,简化了动作空间
4. **相位约束**: 必须按phase_order顺序执行,不能随意跳转
5. **时间约束**: min_green ≤ 当前绿灯时长 ≤ max_green

### 离线RL with SUMO特性

1. **仿真确定性**: 给定状态+动作,SUMO仿真结果确定,可重现
2. **仿真成本**: 启动SUMO有固定开销(~数秒),批量/并行计算更高效
3. **状态文件**: SUMO支持保存/加载状态,使得"分支"仿真成为可能
4. **双仿真策略**: 每个决策点运行两次仿真(延长/切换),提前获知两种结果

### GRPO训练特性

1. **多候选生成**: num_generations控制每个prompt生成多个候选
2. **组内比较**: 同一prompt的多个候选相互比较,学习相对优劣
3. **KL正则化**: beta参数控制策略与参考策略的散度,防止过度偏离
4. **格式对齐重要性**: 训练初期需要SFT阶段预训练格式,否则GRPO难以收敛

## Sources

基于以下来源综合分析:

**项目代码:**
- `/home/samuel/SCU_TSC/grpo/dataset_generator.py` — 数据生成逻辑
- `/home/samuel/SCU_TSC/grpo/training.py` — GRPO训练流程
- `/home/samuel/SCU_TSC/grpo/reward.py` — 奖励函数链
- `/home/samuel/SCU_TSC/Qwen3_(4B)_GRPO.ipynb` — 参考实现

**领域知识:**
- 离线强化学习最佳实践(Offline RL best practices, 2026)
- GRPO数据集格式特性(GRPO dataset format features, 2026)
- 交通信号控制RL数据生成(Traffic signal control RL data generation, 2026)

**技术背景:**
- SUMO(Simulation of Urban MObility)仿真引擎文档
- TRL(Transformer Reinforcement Learning)库GRPOTrainer API
- Unsloth框架LoRA训练优化

---
*Feature research for: TSC GRPO训练系统重构*
*Researched: 2026-02-03*
