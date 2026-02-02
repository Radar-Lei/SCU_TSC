# Requirements: TSC GRPO训练系统重构

**定义日期:** 2026-02-03
**核心价值:** 通过前置SUMO仿真到数据生成阶段,使GRPO训练时不需要实时调用仿真环境,从而大幅简化系统架构,提高代码可维护性。

## v0.1 Requirements (原型验证版)

### 数据生成 (Data Generation)

- [ ] **DG-01**: 系统可以在决策点保存SUMO仿真状态
- [ ] **DG-02**: 系统可以从保存的状态加载并继续仿真
- [ ] **DG-03**: 系统可以验证状态保存/加载的完整性(保存→加载→对比排队数一致)
- [ ] **DG-04**: 系统可以从同一状态分叉执行延长动作(action=0)
- [ ] **DG-05**: 系统可以从同一状态分叉执行切换动作(action=1)
- [ ] **DG-06**: 系统记录双动作仿真结果为四元组(current_queue, next_queue_0, next_queue_1, metadata)
- [ ] **DG-07**: 系统固定SUMO随机种子确保分支仿真环境一致性
- [ ] **DG-08**: 系统记录分支一致性哈希值用于验证
- [ ] **DG-09**: 系统支持多场景并行数据生成
- [ ] **DG-10**: 系统使用预分配端口池避免并行SUMO实例端口冲突
- [ ] **DG-11**: 系统合并多场景数据为统一训练集

### 数据格式 (Data Format)

- [ ] **DF-01**: 数据格式标准化为GRPODataEntry结构
- [ ] **DF-02**: 数据包含id/scenario/junction_id/simulation_time字段
- [ ] **DF-03**: 数据包含phase_info(当前相位信息)
- [ ] **DF-04**: 数据包含queue_data(current/next_0/next_1排队长度)
- [ ] **DF-05**: 数据包含metadata(状态文件路径/决策约束等)
- [ ] **DF-06**: 数据序列化为JSON格式保存
- [ ] **DF-07**: 数据可通过Dataset.from_list加载为HuggingFace Dataset

### Reward函数 (Reward Functions)

- [ ] **RW-01**: 系统实现格式验证reward函数(format_reward_fn)
- [ ] **RW-02**: 格式验证支持strict级别(完全符合格式,+1.0)
- [ ] **RW-03**: 格式验证支持partial级别(部分符合格式,-0.5)
- [ ] **RW-04**: 格式验证支持invalid级别(完全违反格式,-10.0)
- [ ] **RW-05**: 系统使用正则表达式提取决策(yes/no)
- [ ] **RW-06**: 系统实现TSC领域reward函数(tsc_reward_fn)
- [ ] **RW-07**: TSC reward基于排队长度差异计算连续奖励值
- [ ] **RW-08**: TSC reward从预生成数据查表获取(next_queue_0/next_queue_1)
- [ ] **RW-09**: 系统实现reward函数链(format_weight × format_reward + tsc_weight × tsc_reward)
- [ ] **RW-10**: 系统记录reward统计信息(RewardStats: format/tsc/combined分布)

### SFT预训练 (Supervised Fine-Tuning)

- [ ] **SFT-01**: 系统实现SFT阶段用于格式对齐
- [ ] **SFT-02**: SFT阶段使用标准输出格式的示例数据
- [ ] **SFT-03**: SFT阶段训练模型学习正确的输出格式(yes/no)
- [ ] **SFT-04**: SFT阶段保存格式对齐后的checkpoint作为GRPO起点

### GRPO训练 (GRPO Training)

- [ ] **TR-01**: 系统集成TRL GRPOTrainer
- [ ] **TR-02**: 系统集成Unsloth FastLanguageModel加速训练
- [ ] **TR-03**: 系统从SFT checkpoint加载模型作为GRPO起点
- [ ] **TR-04**: 系统配置GRPOConfig参数(num_generations≥4)
- [ ] **TR-05**: 系统在启动时断言num_generations≥4(避免退化为普通策略梯度)
- [ ] **TR-06**: 系统使用统一prompt_builder构建输入
- [ ] **TR-07**: 系统输入格式为JSON(crossing_id/as_of/phase_order/queue/constraints)
- [ ] **TR-08**: 系统支持checkpoint保存和恢复训练
- [ ] **TR-09**: 系统记录训练日志(loss/reward/format_ratio等)
- [ ] **TR-10**: 系统参考Qwen3_(4B)_GRPO.ipynb框架结构
- [ ] **TR-11**: 系统支持LoRA训练模式

### 模型推理 (Model Inference)

- [ ] **IF-01**: 系统可以合并LoRA权重到基础模型
- [ ] **IF-02**: 系统可以导出16bit模型
- [ ] **IF-03**: 系统提供推理接口加载训练后模型
- [ ] **IF-04**: 推理接口可以接收交通状态输入
- [ ] **IF-05**: 推理接口可以输出决策建议(yes/no)

### 代码架构 (Code Architecture)

- [ ] **AR-01**: 数据生成代码组织在grpo/data_generation/目录
- [ ] **AR-02**: 训练代码组织在grpo/training/目录
- [ ] **AR-03**: 共享组件组织在grpo/shared/目录
- [ ] **AR-04**: 提供scripts/generate_dataset.py入口脚本
- [ ] **AR-05**: 提供scripts/train_grpo.py入口脚本
- [ ] **AR-06**: 删除或重构实时SUMO调用相关代码
- [ ] **AR-07**: 删除冗余的中间抽象层

## v0.2+ Requirements (未来增强)

### 基线对比
- **BL-01**: 系统实现Max Pressure算法baseline
- **BL-02**: 系统批量计算baseline决策
- **BL-03**: 系统统计模型决策vs baseline准确率
- **BL-04**: 系统支持相对基线奖励(use_relative_baseline)

### 性能优化
- **PF-01**: 系统使用并行SUMO进程池计算reward
- **PF-02**: 系统集成WandB可视化训练曲线
- **PF-03**: 系统支持分层数据集划分(stratified_split)

### 高级功能
- **AD-01**: 系统支持多时刻历史状态输入
- **AD-02**: 系统支持多目标优化(排队+等待时间+通行量)
- **AD-03**: 系统支持自适应reward权重调整
- **AD-04**: 系统支持Curriculum Learning渐进式难度

## Out of Scope (明确排除)

| Feature | Reason |
|---------|--------|
| 实时SUMO仿真在训练循环中 | 架构复杂、调试困难,这正是重构要消除的 |
| 硬编码0/1二元reward | 训练信号稀疏,无法反映"接近正确"的价值 |
| 多时刻历史状态(v0.1) | v0.1聚焦当前时刻决策,历史状态延后到v0.2+ |
| 多目标优化(v0.1) | v0.1聚焦排队长度单一指标,验证后再扩展 |
| 所有决策点保存状态 | 磁盘浪费,使用state_save_interval间隔保存即可 |
| 完美格式强制 | 训练初期过严导致无有效梯度,使用多级奖励渐进引导 |
| 同步数据生成 | 多场景生成慢,使用并行生成提升效率 |

## Traceability (需求到阶段映射)

*此部分将在创建ROADMAP.md时填充*

| Requirement | Phase | Status |
|-------------|-------|--------|
| (待填充) | (待填充) | Pending |

**Coverage:**
- v0.1 requirements: 46 total
- Mapped to phases: 0 (待roadmap创建)
- Unmapped: 46 ⚠️

---
*Requirements defined: 2026-02-03*
*Last updated: 2026-02-03 after initial definition*
