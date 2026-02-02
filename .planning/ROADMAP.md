# Roadmap: TSC GRPO训练系统重构

## Overview

通过4阶段渐进式重构,将SUMO仿真前置到数据生成阶段,建立离线强化学习训练流程。从数据生成架构重构开始,确保双动作仿真和状态保存机制的正确性;然后重构Reward函数实现查表式奖励计算;接着集成GRPO训练器完成端到端流程;最后通过全面验证确保模型质量和泛化能力。

## Phases

**Phase编号:**
- 整数Phase (1, 2, 3): 计划中的里程碑工作
- 小数Phase (2.1, 2.2): 紧急插入 (标记为INSERTED)

小数Phase按数字顺序出现在相邻整数之间。

- [ ] **Phase 1: 数据生成架构重构** - 建立双动作仿真和状态验证机制
- [ ] **Phase 2: Reward函数重构** - 实现查表式奖励计算和多级评分
- [ ] **Phase 3: GRPO训练集成** - 集成TRL训练器完成端到端流程
- [ ] **Phase 4: 验证与优化** - 模型评估和推理接口实现

## Phase Details

### Phase 1: 数据生成架构重构
**目标**: 建立正确的离线数据生成流程,生成包含双动作仿真结果的四元组数据集
**依赖**: 无 (第一个phase)
**需求**: DG-01, DG-02, DG-03, DG-04, DG-05, DG-06, DG-07, DG-08, DG-09, DG-10, DG-11, DF-01, DF-02, DF-03, DF-04, DF-05, DF-06, DF-07, AR-01, AR-02, AR-03, AR-04
**成功标准** (必须为TRUE的状态):
  1. 系统可以保存SUMO仿真状态并从同一状态加载,验证排队长度一致性
  2. 系统可以从同一保存状态分叉执行延长(action=0)和切换(action=1)两个仿真分支,记录为四元组数据
  3. 多场景可以并行生成数据,使用端口池避免SUMO实例冲突
  4. 生成的数据集符合GRPODataEntry标准格式,可通过Dataset.from_list加载为HuggingFace Dataset
**Plans**: TBD

Plans:
- [ ] 01-01: TBD

### Phase 2: Reward函数重构
**目标**: 基于预生成数据实现查表式Reward计算,支持格式验证和TSC指标的链式组合
**依赖**: Phase 1
**需求**: RW-01, RW-02, RW-03, RW-04, RW-05, RW-06, RW-07, RW-08, RW-09, RW-10
**成功标准** (必须为TRUE的状态):
  1. 格式验证Reward函数可以通过正则表达式提取yes/no决策,支持strict(+1.0)/partial(-0.5)/invalid(-10.0)三级评分
  2. TSC领域Reward函数可以从预生成数据查表获取next_queue_0/next_queue_1,基于排队长度差异计算连续奖励值
  3. Reward函数链可以组合格式验证和TSC指标,使用可配置权重(format_weight, tsc_weight)
  4. 系统记录RewardStats统计信息,包含format/tsc/combined的分布数据
**Plans**: TBD

Plans:
- [ ] 02-01: TBD

### Phase 3: GRPO训练集成
**目标**: 集成TRL GRPOTrainer和Unsloth加速库,完成SFT预训练到GRPO训练的端到端流程
**依赖**: Phase 2
**需求**: SFT-01, SFT-02, SFT-03, SFT-04, TR-01, TR-02, TR-03, TR-04, TR-05, TR-06, TR-07, TR-08, TR-09, TR-10, TR-11, AR-05, AR-06, AR-07
**成功标准** (必须为TRUE的状态):
  1. SFT阶段可以使用标准输出格式的示例训练模型学习yes/no格式,保存checkpoint作为GRPO起点
  2. GRPO训练可以从SFT checkpoint加载模型,使用GRPOConfig配置参数(num_generations>=4已断言验证)
  3. 训练过程使用统一prompt_builder构建JSON格式输入(crossing_id/as_of/phase_order/queue/constraints)
  4. 训练日志记录loss/reward/format_ratio等指标,支持checkpoint保存和恢复训练
  5. 参考Qwen3_(4B)_GRPO.ipynb框架结构,集成Unsloth FastLanguageModel和LoRA训练模式
**Plans**: TBD

Plans:
- [ ] 03-01: TBD

### Phase 4: 验证与优化
**目标**: 全面验证模型性能,实现推理接口,确保模型可部署和泛化能力
**依赖**: Phase 3
**需求**: IF-01, IF-02, IF-03, IF-04, IF-05
**成功标准** (必须为TRUE的状态):
  1. 系统可以合并LoRA权重到基础模型并导出16bit模型
  2. 推理接口可以加载训练后模型,接收交通状态输入(JSON格式),输出决策建议(yes/no)
  3. 测试集评估覆盖不同场景和时间段,验证模型泛化能力
**Plans**: TBD

Plans:
- [ ] 04-01: TBD

## Progress

**执行顺序:**
Phase按数字顺序执行: 1 → 2 → 3 → 4

| Phase | Plans完成 | Status | 完成日期 |
|-------|-----------|--------|----------|
| 1. 数据生成架构重构 | 0/TBD | Not started | - |
| 2. Reward函数重构 | 0/TBD | Not started | - |
| 3. GRPO训练集成 | 0/TBD | Not started | - |
| 4. 验证与优化 | 0/TBD | Not started | - |

---
*Roadmap created: 2026-02-03*
*Last updated: 2026-02-03*
