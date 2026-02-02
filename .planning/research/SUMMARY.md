# 项目研究总结

**项目:** TSC GRPO训练系统重构
**领域:** 离线强化学习训练系统 (交通信号控制)
**研究日期:** 2026-02-03
**置信度:** HIGH

## 综合概述

本项目旨在重构交通信号控制(TSC)的GRPO训练系统,核心目标是将数据生成与训练分离,实现**离线强化学习**架构。当前系统的主要问题是训练时需要实时调用SUMO仿真,导致架构复杂、调试困难。研究表明,通过前置SUMO仿真到数据生成阶段,可以显著简化训练流程,同时提高可维护性和可重现性。

推荐方案采用**Unsloth + TRL**技术栈,使用**双动作仿真**模式在数据生成时为每个决策点预计算延长/切换两种动作的后果,训练时仅需查表计算奖励。这种设计借鉴了Qwen3 GRPO参考实现的纯数据驱动模式,消除了训练时的SUMO依赖。Reward函数采用**链式结构**(格式验证 + TSC指标),支持渐进式引导模型学习。

关键风险包括:SUMO状态保存/加载的完整性验证缺失、离线数据分布偏差导致过拟合、Docker环境下端口冲突。缓解策略是在Phase 1建立严格的状态验证机制、实施分层采样确保数据多样性、使用预分配端口池避免并发冲突。

## 核心发现

### 推荐技术栈

**核心决策:使用Unsloth + TRL组合而非自实现GRPO**。Unsloth提供FastLanguageModel进行内存优化和训练加速(2倍速,50%内存),TRL提供经过验证的GRPOTrainer实现。这一组合已在Qwen3_(4B)_GRPO.ipynb中得到验证,可直接复用。

**核心技术:**
- **Unsloth (2025.5+)**: LLM快速训练加速,自动配置LoRA、量化、xformers优化,训练速度快2倍
- **TRL (0.22.2+)**: 提供GRPOTrainer和GRPOConfig,生态成熟,与Transformers深度集成
- **TraCI/LibSUMO**: SUMO仿真接口,当前使用TraCI稳定可靠,可选迁移LibSUMO提升性能
- **Datasets**: HuggingFace数据集库,与TRL GRPOTrainer深度集成,支持Dataset.from_list快速构建
- **Docker**: 必须使用,SUMO环境依赖Docker配置

**关键版本兼容性:**
- Transformers 4.56.2+ (修复chat template bug)
- PyTorch 2.0+, CUDA 11.8+
- 最低GPU: Tesla T4 (14GB显存)

### 核心功能定义

**必需功能(Table Stakes):**
- **预生成仿真数据**: 系统核心价值,前置SUMO仿真到数据生成阶段,避免训练时实时调用(HIGH complexity)
- **标准化数据格式**: 四元组(current_queue, next_queue_0, next_queue_1, metadata),确保训练器输入一致(LOW complexity)
- **格式验证与奖励**: GRPO需要验证模型输出格式并打分,已实现strict/partial/invalid三级(MEDIUM complexity)
- **TSC领域奖励计算**: 基于排队长度差异的连续reward,需并行SUMO仿真(HIGH complexity)
- **批量数据生成**: 多场景并行生成,合并为训练集(MEDIUM complexity)
- **训练状态保存**: checkpoint机制支持恢复训练(LOW complexity)
- **模型推理接口**: LoRA合并和16bit导出(MEDIUM complexity)

**竞争优势功能(Differentiators):**
- **连续reward函数**: 比0/1二元reward更细粒度,基于排队长度差异的比例计算(MEDIUM complexity)
- **Max Pressure基线追踪**: 提供可解释的baseline,帮助理解模型决策质量(MEDIUM complexity)
- **相对基线奖励**: 奖励相对于baseline的改进而非绝对值,已有use_relative_baseline配置(MEDIUM complexity)
- **并行SUMO奖励计算**: ParallelSUMORewardCalculator,多进程池避免训练瓶颈(HIGH complexity)
- **多级格式奖励**: strict(+1.0)/partial(-0.5)/invalid(-10.0)渐进式引导(LOW complexity)

**反模式(应避免):**
- **实时SUMO仿真**: 训练速度慢、架构复杂、调试困难 → 改为预生成数据
- **多时刻历史状态**: 增加复杂度但v1不需要 → 延迟到v2
- **硬编码0/1二元reward**: 训练信号稀疏 → 使用连续reward
- **所有决策点都保存状态**: 磁盘浪费 → 使用state_save_interval

### 架构方案

**核心模式:两阶段离线流水线**

```
Phase 1: 数据生成
  SUMO仿真 → 决策点采集 → 双动作模拟 → 四元组数据集 + 状态快照

Phase 2: 训练
  数据加载 → Reward计算(双权重) → GRPO训练 → 优化后的策略
```

**推荐项目结构:**
```
grpo/
├── data_generation/        # 数据生成阶段(新建)
│   ├── sumo_interface.py   # 移动自grpo/
│   ├── decision_detector.py # 决策点检测(从dataset_generator.py提取)
│   ├── dual_action_simulator.py # 双动作仿真器(新建核心)
│   └── dataset_serializer.py    # 数据保存
├── training/               # 训练阶段
│   ├── dataset_loader.py   # 数据加载
│   ├── reward_calculator.py # Reward函数链
│   └── grpo_trainer.py     # 训练入口
├── shared/                 # 共享组件
│   ├── config.py
│   └── prompt_builder.py
└── scripts/
    ├── generate_dataset.py # Phase 1入口
    └── train_grpo.py       # Phase 2入口
```

**关键架构模式:**
1. **离线数据生成**: 环境交互前置,训练时仅读取,优点是稳定、可调试、可复用
2. **双动作仿真**: 每个决策点提前模拟延长/切换两种结果,Reward计算变为查表
3. **Reward函数链**: Format验证先行(早停无效输出),TSC指标后行(仅格式有效时计算)

**数据流:**
- 数据生成: SUMO保存state → 加载state执行延长 → 再次加载state执行切换 → 保存四元组
- 训练: 加载JSON → 转换为HF Dataset → GRPOTrainer生成候选 → Reward计算(查表) → 策略更新

### 关键陷阱

基于代码分析和领域知识,识别出8个关键陷阱:

1. **数据生成时状态不完整**(CRITICAL) — SUMO的saveState不保存完整状态,导致训练时无法重现
   - 预防:立即验证策略(save→load→对比排队数)、元数据冗余、状态往返测试
   - 所属阶段:Phase 1 (数据生成重构)

2. **延长/切换两个分支环境不一致**(CRITICAL) — 两次仿真的随机性不同,无法公平比较决策效果
   - 预防:从同一state分叉、固定随机种子、记录分支一致性哈希
   - 所属阶段:Phase 1 (数据生成重构)

3. **排队长度作为唯一指标丢失动态信息**(MODERATE) — 可能过度简化,忽略等待时间、通行量等
   - 预防:保留更多信息作为备用、记录趋势特征、多目标验证
   - 所属阶段:Phase 2 (Reward函数设计)、Phase 4 (验证测试)

4. **GRPO num_generations设置错误**(CRITICAL) — 设为1会导致无group对比,GRPO退化为普通策略梯度
   - 预防:最小值断言(>=4)、配置文件注释、训练日志监控
   - 所属阶段:Phase 3 (GRPO训练集成)

5. **Docker端口冲突**(CRITICAL) — 并行SUMO实例因端口冲突无法同时启动
   - 预防:预分配端口池、文件锁机制、重试+指数退避
   - 所属阶段:Phase 1 (数据生成重构)

6. **相位约束随机偏移不一致**(MODERATE) — 数据生成时有随机偏移但训练时模型不知道
   - 预防:约束作为输入、标准化约束(v1不使用随机偏移)、训练时验证
   - 所属阶段:Phase 2 (Reward函数设计)

7. **离线数据分布偏差**(CRITICAL) — 模型过拟合到数据生成策略,泛化性能差
   - 预防:数据审查、平衡采样、领域随机化、保守策略
   - 所属阶段:Phase 1 (数据生成)、Phase 4 (验证测试)

8. **Reward格式检查过严**(MODERATE) — 训练初期格式错误导致无有效梯度
   - 预防:渐进式惩罚、Partial credit、SFT预训练、监控指标
   - 所属阶段:Phase 2 (Reward设计)、Phase 3 (训练集成)

## 路线图建议

基于研究发现,建议采用**4阶段渐进式重构**:

### Phase 1: 数据生成架构重构
**理由:** 数据生成是整个系统的基础,必须首先建立正确的离线数据生成流程,否则后续训练基于错误数据。

**交付内容:**
- 双动作仿真器(dual_action_simulator.py)
- 四元组数据格式(current_queue, next_queue_0, next_queue_1, metadata)
- SUMO状态保存/加载验证机制
- 并行数据生成(解决端口冲突)
- 数据集质量审查工具

**涉及功能:**
- 预生成仿真数据(必需)
- 标准化数据格式(必需)
- 批量数据生成(必需)

**规避陷阱:**
- 陷阱1:状态不完整 → 建立save→load→verify测试
- 陷阱2:分支不一致 → 从同一state分叉,固定种子
- 陷阱5:端口冲突 → 预分配端口池
- 陷阱7:分布偏差 → 数据审查和分层采样

**估算工作量:** 高(涉及核心架构改变)

### Phase 2: Reward函数重构
**理由:** 在正确的数据基础上,设计合理的Reward函数是训练成功的关键。需要平衡格式验证和TSC指标,避免过早收敛。

**交付内容:**
- 简化TSC Reward计算(基于预生成数据查表)
- 格式验证与多级奖励机制
- Reward函数链(format_weight + tsc_weight)
- Reward分布可视化工具
- 基线对比准备(Max Pressure)

**涉及功能:**
- 格式验证与奖励(必需)
- TSC领域奖励计算(必需)
- 连续reward函数(优势)
- 多级格式奖励(优势)

**规避陷阱:**
- 陷阱3:指标不足 → 保留补充特征,多目标验证
- 陷阱6:约束不一致 → v1简化约束,约束作为输入
- 陷阱8:格式过严 → 渐进式惩罚,监控format vs tsc比例

**估算工作量:** 中(基于现有代码重构)

### Phase 3: GRPO训练集成
**理由:** 在数据和Reward就绪后,集成GRPO训练器,完成端到端流程。此阶段需要仔细配置GRPO参数,确保训练稳定。

**交付内容:**
- 数据加载器适配新格式
- GRPOTrainer配置和参数验证
- SFT预训练流程(可选,用于格式对齐)
- 训练监控和日志
- Checkpoint管理

**涉及功能:**
- 参考Qwen3框架结构(必需)
- 训练状态保存(必需)
- WandB集成(可选,增强)

**规避陷阱:**
- 陷阱4:num_generations错误 → 启动时断言>=4
- 陷阱8:格式过严 → 监控训练动态,调整权重

**估算工作量:** 中(基于TRL库,主要是集成和配置)

### Phase 4: 验证与优化
**理由:** 训练完成后,需要全面验证模型性能,检测泛化能力,识别需要改进的地方。

**交付内容:**
- 测试集评估(不同场景/时间段)
- Max Pressure baseline对比
- 多指标评估(排队、等待时间、通行量)
- 模型推理接口和部署准备
- 性能分析和优化建议

**涉及功能:**
- Max Pressure基线追踪(增强)
- 相对基线奖励(可选)
- 模型推理接口(必需)

**规避陷阱:**
- 陷阱3:指标不足 → 多指标验证
- 陷阱7:分布偏差 → 泛化性能测试

**估算工作量:** 中(主要是测试和分析)

### 阶段排序理由

1. **数据生成优先**: 离线RL的核心是数据质量,必须首先建立正确的数据生成流程
2. **Reward设计其次**: 在正确数据基础上设计Reward,避免后期重新生成数据
3. **训练集成第三**: 数据和Reward就绪后集成训练器,降低调试难度
4. **验证收尾**: 训练完成后全面评估,识别改进方向

### 研究标记

**需要深入研究的阶段:**
- **Phase 1**: SUMO状态保存/加载机制的技术细节,需要查阅SUMO官方文档和社区讨论
- **Phase 2**: 连续reward函数的设计权衡,可能需要实验验证

**模式成熟的阶段(可跳过研究):**
- **Phase 3**: TRL GRPOTrainer文档完善,Qwen3参考实现可直接复用
- **Phase 4**: 标准ML模型评估流程,无需特殊研究

## 置信度评估

| 领域 | 置信度 | 说明 |
|------|--------|------|
| 技术栈 | HIGH | 基于Qwen3_(4B)_GRPO.ipynb验证的组合,TRL和Unsloth文档完善 |
| 功能定义 | HIGH | 基于现有代码深度分析和离线RL最佳实践 |
| 架构方案 | HIGH | 基于现有dataset_generator.py和training.py结构,经过实际验证 |
| 陷阱识别 | HIGH | 基于代码审查发现的具体问题 + RL/SUMO领域共识 |

**总体置信度:** HIGH

### 需要解决的差距

虽然总体置信度高,但以下领域需要在实施阶段验证:

1. **SUMO状态完整性**: SUMO saveState的确切行为需要实验验证,特别是随机数生成器和车辆插入计划是否被保存
2. **Qwen模型特定行为**: 当前参考Qwen3实现,但未研究Qwen在TSC任务上的特殊表现,需要训练初期密切监控
3. **排队长度指标充分性**: v1使用排队长度作为唯一指标是合理简化,但需要通过实验验证是否足够
4. **离线数据覆盖度**: 数据生成策略能否覆盖足够的状态空间需要通过数据审查确认
5. **Docker并发稳定性**: 端口分配机制在高并发下的表现需要压力测试

**处理策略:**
- 差距1-2在Phase 1建立测试用例验证
- 差距3在Phase 4通过多指标评估检测
- 差距4在Phase 1数据审查阶段识别
- 差距5在Phase 1并行测试中验证

## 信息来源

### 主要来源(HIGH置信度)
- 项目代码库:
  - `/home/samuel/SCU_TSC/grpo/dataset_generator.py` — 数据生成流程
  - `/home/samuel/SCU_TSC/grpo/training.py` — GRPO训练流程
  - `/home/samuel/SCU_TSC/grpo/reward.py` — Reward函数链
  - `/home/samuel/SCU_TSC/grpo/sumo_interface.py` — SUMO接口
  - `/home/samuel/SCU_TSC/Qwen3_(4B)_GRPO.ipynb` — 参考实现
- 官方文档:
  - TRL GRPOTrainer: https://github.com/huggingface/trl
  - Unsloth: https://github.com/unslothai/unsloth
  - SUMO: https://sumo.dlr.de/docs/

### 次要来源(MEDIUM置信度)
- 离线强化学习最佳实践(2020-2025 RL领域共识)
- GRPO算法原理(Group Relative Policy Optimization)
- SUMO社区讨论(状态保存局限性)

### 第三来源(LOW置信度,需验证)
- WebSearch: GRPO reinforcement learning 2025
- WebSearch: SUMO Python integration 2025
- 通用Docker并发和端口管理经验

---
*研究完成日期: 2026-02-03*
*准备进入路线图规划: 是*
