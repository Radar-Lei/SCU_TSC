# Requirements: TSC-GRPO

**Defined:** 2025-02-02
**Core Value:** 模型能够根据SUMO仿真状态的相位排队信息，准确判断是否延长当前绿灯相位，以最小化整个交叉口的排队车辆数。

## v1 Requirements

### GRPO训练核心

- [ ] **GRPO-01**: 实现完整的GRPO训练脚本
  - 支持从SFT训练好的模型继续训练
  - 集成Unsloth的FastLanguageModel和TRL的GRPOTrainer
  - 支持配置文件和命令行参数管理超参数
  - 实现训练过程中的检查点保存和恢复
  - 记录训练日志（loss、reward、KL散度等）

- [ ] **GRPO-02**: 实现reward函数链
  - 支持多个reward函数的组合
  - format_reward_fn：检查输出格式正确性
  - tsc_reward_fn：基于Max Pressure算法评估决策质量
  - reward权重可配置

- [ ] **GRPO-03**: 实现format_reward_fn
  - 验证输出是否为有效JSON
  - 验证JSON结构为 `{"extend": "yes/no"}`
  - 允许合理的空格和大小写变体
  - 格式错误给予负奖励（如-2.0）
  - 格式正确给予正奖励（如+1.0）

- [ ] **GRPO-04**: 实现tsc_reward_fn
  - 实现Max Pressure算法（简单启发式baseline）
  - 从保存的SUMO状态文件恢复仿真
  - 根据模型决策推进仿真：
    - 延长（yes）：当前相位延长N秒
    - 切换（no）：切换到下一相位并推进N秒
  - 计算推进后的排队车辆数
  - 根据与Max Pressure决策的一致性和排队数变化给予连续奖励

### Max Pressure算法

- [ ] **MAXP-01**: 实现Max Pressure算法
  - 输入：各相位的平均排队车辆数
  - 逻辑：找出所有相位中排队数最大的相位
  - 输出：建议是否延长当前相位
  - 当前相位排队最大 → 建议延长（yes）
  - 其他相位排队更大 → 建议切换（no）

### 配置管理

- [ ] **CONFIG-01**: 创建中央训练配置文件
  - SFT训练超参数：learning_rate, batch_size, num_epochs等
  - GRPO训练超参数：learning_rate, temperature, num_generations等
  - Reward函数权重：format_reward_weight, tsc_reward_weight
  - 仿真参数：extend_seconds, max_steps等
  - 支持不同环境的配置切换（如dev、test、prod）

- [ ] **CONFIG-02**: 实现配置加载逻辑
  - 优先级：命令行参数 > 配置文件 > 默认值
  - 支持YAML格式的配置文件
  - 配置验证：检查必需参数和参数范围

### 训练流程集成

- [ ] **TRAIN-01**: 完善 `docker/publish.sh`
  - 四步流程：GRPO数据 → SFT数据 → SFT训练 → GRPO训练
  - 每步失败时停止并报告错误
  - 完整的日志记录
  - 训练结束后的模型输出路径报告

- [ ] **TRAIN-02**: 添加数据验证步骤
  - 验证GRPO数据集格式正确性
  - 检查SUMO状态文件可加载
  - 测试prompt格式符合要求
  - 在训练前运行验证，提前发现问题

### 测试和验证

- [ ] **TEST-01**: 单元测试
  - 测试format_reward_fn的边界情况
  - 测试Max Pressure算法的正确性
  - 测试配置加载和参数验证

- [ ] **TEST-02**: 集成测试
  - 小规模训练验证（少量数据、少量步数）
  - 端到端流程测试
  - 验证reward函数组合工作正常

## v2 Requirements

Deferred to future release.

## Out of Scope

| Feature | Reason |
|---------|--------|
| 多路口协同控制 | 当前仅支持单个交叉口的独立控制 |
| 动态相位顺序 | 相位执行顺序固定，不支持动态重排 |
| 其他强化学习算法 | 仅使用GRPO，不实现PPO、DQN等 |
| 实时在线训练 | 训练流程离线进行，不支持在线学习 |
| 模型推理服务 | 不包含模型部署和推理API的开发 |
| 可视化界面 | 不提供Web UI或可视化控制面板 |
| 多目标优化 | 仅优化排队车辆数，不考虑等待时间、油耗等 |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| GRPO-01 | Phase 1 | Pending |
| GRPO-02 | Phase 1 | Pending |
| GRPO-03 | Phase 1 | Pending |
| GRPO-04 | Phase 1 | Pending |
| MAXP-01 | Phase 2 | Pending |
| CONFIG-01 | Phase 2 | Pending |
| CONFIG-02 | Phase 2 | Pending |
| TRAIN-01 | Phase 3 | Pending |
| TRAIN-02 | Phase 3 | Pending |
| TEST-01 | Phase 4 | Pending |
| TEST-02 | Phase 4 | Pending |

**Coverage:**
- v1 requirements: 11 total
- Mapped to phases: 11
- Unmapped: 0 ✓

---
*Requirements defined: 2025-02-02*
*Last updated: 2025-02-02 after initial definition*
