# Roadmap: TSC-GRPO

## Overview

从已实现的SFT训练和数据生成基础设施出发，构建完整的GRPO强化学习训练系统。Phase 1建立GRPO训练核心和reward函数框架，Phase 2实现Max Pressure baseline算法和配置管理系统，Phase 3集成完整的端到端训练流程，Phase 4通过测试验证确保系统稳定运行，Phase 5集成Max Pressure baseline到训练流程完成Milestone v1。

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: GRPO训练核心基础设施** - 建立GRPO训练脚本和reward函数框架
- [x] **Phase 2: Max Pressure算法和配置管理** - 实现baseline算法和配置系统
- [x] **Phase 3: 训练流程集成** - 完善端到端训练流程和数据验证
- [x] **Phase 4: 测试、验证和完善** - 通过单元测试和集成测试确保系统稳定性
- [x] **Phase 5: Max Pressure Baseline集成** - 将Max Pressure算法集成到训练流程，完成MAXP-01需求

## Phase Details

### Phase 1: GRPO训练核心基础设施
**Goal**: 建立完整的GRPO训练流程，支持从SFT模型继续训练，实现reward函数评估框架
**Depends on**: 无（已有SFT训练脚本和数据生成器）
**Requirements**: GRPO-01, GRPO-02, GRPO-03, GRPO-04
**Success Criteria** (what must be TRUE):
  1. 运行 `python grpo/training.py --config config/grpo_config.yaml` 启动GRPO训练
  2. 训练脚本能够加载SFT模型作为起点
  3. format_reward_fn正确实现三级评分（±1/-0.5/-10）
  4. tsc_reward_fn基于SUMO仿真计算排队数变化，归一化到[-1,1]
  5. 并行SUMO仿真架构工作正常（多进程、随机端口分配、错误处理）
  6. Reward函数链正确组合format和tsc rewards，权重可配置
  7. 训练日志显示reward统计信息
**Plans**: 4 plans

Plans:
- [x] 01-01: 创建GRPO训练脚本框架（配置文件、数据加载、GRPOTrainer集成）
- [x] 01-02: 实现format_reward_fn（三级评分：严格+1、部分-0.5、完全不遵守-10）
- [x] 01-03: 实现tsc_reward_fn和并行SUMO仿真架构（多进程、随机端口、错误处理）
- [x] 01-04: 实现reward函数链，组合format和tsc rewards

### Phase 2: Max Pressure算法和配置管理
**Goal**: 实现Max Pressure baseline算法用于reward计算，建立中央配置管理系统
**Depends on**: Phase 1
**Requirements**: MAXP-01, CONFIG-01, CONFIG-02
**Success Criteria** (what must be TRUE):
  1. Max Pressure算法根据各相位排队数输出是否延长的建议（yes/no）
  2. training_config.yaml包含所有SFT和GRPO训练的超参数
  3. 命令行参数能够覆盖配置文件中的对应参数
  4. 配置加载时验证必需参数存在且在合理范围内
**Plans**: 3 plans

Plans:
- [x] 02-01: 实现Max Pressure算法，根据各相位排队数判断是否延长当前相位
- [x] 02-02: 创建training_config.yaml，包含所有训练和仿真超参数
- [x] 02-03: 实现配置加载逻辑，支持YAML文件、命令行参数和默认值的优先级覆盖

### Phase 3: 训练流程集成
**Goal**: 完善docker/publish.sh，实现完整的四步训练流程，添加数据验证步骤
**Depends on**: Phase 2
**Requirements**: TRAIN-01, TRAIN-02
**Success Criteria** (what must be TRUE):
  1. 运行docker/publish.sh执行完整的四步流程（GRPO数据→SFT数据→SFT训练→GRPO训练）
  2. 任何步骤失败时脚本停止并输出错误信息
  3. 训练结束后输出最终模型的保存路径
  4. 数据验证步骤在训练前检查GRPO数据集格式和SUMO状态文件可加载性
**Plans**: 3 plans

Plans:
- [x] 03-01: 完善docker/publish.sh，添加失败检测、依赖检查和训练摘要
- [x] 03-02: 实现数据验证脚本，检查GRPO/SFT数据集和SUMO状态文件
- [x] 03-03: 将数据验证步骤集成到publish.sh训练流程中

### Phase 4: 测试、验证和完善
**Goal**: 通过单元测试和集成测试验证系统各组件正确性，确保端到端流程稳定运行
**Depends on**: Phase 3
**Requirements**: TEST-01, TEST-02
**Success Criteria** (what must be TRUE):
  1. 单元测试覆盖format_reward_fn的边界情况（空输出、错误JSON、有效变体）
  2. 单元测试验证Max Pressure算法在各种输入下的正确性
  3. 小规模训练验证（50条GRPO数据、20条SFT数据、10步训练）成功完成且无错误
  4. 端到端测试运行完整流程并输出训练好的模型
**Plans**: 2 plans

Plans:
- [x] 04-01: 编写单元测试，覆盖reward函数、Max Pressure算法和配置加载
- [x] 04-02: 编写集成测试，验证小规模端到端训练流程

### Phase 5: Max Pressure Baseline集成
**Goal**: 将Max Pressure算法集成到GRPO训练流程中，实现baseline比较和统计追踪，完成MAXP-01需求
**Depends on**: Phase 4
**Requirements**: MAXP-01-baseline-comparison
**Gap Closure**: 关闭Milestone v1审计中发现的需求差距和集成差距

**Success Criteria** (what must be TRUE):
  1. Max Pressure决策函数在reward计算中被调用
  2. 训练日志显示baseline准确率统计信息
  3. compare_with_baseline()和compute_baseline_accuracy()函数被使用
  4. training_config.yaml中reward.max_pressure.*配置项被激活
  5. 单元测试验证baseline比较功能正常
  6. 集成测试验证完整训练流程包含baseline追踪
**Plans**: 5 plans

Plans:
- [x] 05-01: 扩展reward计算函数，添加baseline比较逻辑到compute_reward()
- [x] 05-02: 增强训练脚本，添加baseline统计追踪到create_reward_function()
- [x] 05-03: 激活training_config.yaml中baseline配置项，添加enable_baseline_tracking参数
- [x] 05-04: 编写单元测试，验证baseline比较和统计功能
- [x] 05-05: 编写集成测试，验证baseline追踪在完整训练流程中工作

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. GRPO训练核心基础设施 | 4/4 | ✓ Complete | 2025-02-02 |
| 2. Max Pressure算法和配置管理 | 3/3 | ✓ Complete | 2026-02-02 |
| 3. 训练流程集成 | 3/3 | ✓ Complete | 2026-02-02 |
| 4. 测试、验证和完善 | 2/2 | ✓ Complete | 2026-02-02 |
| 5. Max Pressure Baseline集成 | 5/5 | ✓ Complete | 2026-02-02 |
