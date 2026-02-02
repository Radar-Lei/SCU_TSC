# Phase 5: Max Pressure Baseline集成 - Context

**Gathered:** 2026-02-02
**Status:** Ready for planning

## Phase Boundary

将Max Pressure算法作为baseline比较器集成到GRPO训练的reward计算中，实现模型决策与baseline决策的统计追踪和相对reward计算，完成MAXP-01需求。

## Implementation Decisions

### Baseline集成策略
- **每个样本都计算baseline**：在每次reward计算时，都获取baseline决策并与模型决策比较
- **相对reward设计**：模型决策的TSC效果需要与baseline决策的TSC效果进行比较来计算tsc reward
  - 模型决策SUMO仿真结果比baseline决策好 → 正tsc reward
  - baseline决策SUMO仿真结果比模型决策好 → 负tsc reward
- **智能缓存策略**：先检查缓存，没有时才运行SUMO；避免重复运行相同状态的仿真
- **相对改善率比较**：使用`(delta模型 - delta_baseline) / scale`归一化（类似现有tsc_reward_fn设计）
- **完整状态哈希缓存键**：使用完整的SUMO状态（phase_queues, current_phase等）作为缓存键

### 统计追踪粒度
- **追踪指标**：
  - 模型优于baseline率：追踪模型决策优于baseline的比例
  - 平均reward比较：追踪模型平均reward vs baseline平均reward
- **统计频率**：指定训练step进行信息统计（可配置，如每100步统计一次）
- **统计存储**：写入日志文件，供后续分析
- **统计聚合**：累计统计（从训练开始到当前的整体统计）

### 配置激活方式
- **根据训练模式自动决定**：如SFT禁用，GRPO启用baseline追踪
- **配置层级**：`reward.max_pressure.baseline.*`
- **配置项**：
  - `enable_baseline_tracking`：控制baseline追踪是否启用
  - `baseline_stats_interval`：统计信息记录的step间隔
  - `baseline_cache_size`：baseline仿真缓存的大小限制
  - `verbose_baseline_logging`：是否在日志中详细输出baseline比较信息
- **CLI覆盖**：支持所有baseline配置项通过命令行参数覆盖

### 日志输出格式
- **输出时机**：按统计间隔输出（由baseline_stats_interval控制）
- **信息格式**：简单文本格式，如"Baseline Accuracy: 0.65, Model Better: 60%"
- **与现有日志集成**：合并到reward统计部分，与format_accuracy、avg_tsc_reward等一起输出
- **缓存信息**：不显示缓存统计信息，仅显示模型vs baseline的比较结果

### Claude's Discretion
- 缓存实现的具体数据结构（dict、LRU cache等）
- scale参数的具体值（保持与现有tsc_reward_fn一致或调整）
- 统计信息输出的详细程度（在简单文本框架内的具体措辞）

## Specific Ideas

- Reward计算需要运行两次SUMO仿真（模型决策和baseline决策），通过智能缓存避免重复计算
- Baseline决策来自现有的max_pressure算法实现
- 统计信息帮助理解模型是否学习到超越baseline的策略

## Deferred Ideas

None — discussion stayed within phase scope

---

*Phase: 05-max-pressure-baseline集成*
*Context gathered: 2026-02-02*
