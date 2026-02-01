# Phase 1: GRPO训练核心基础设施 - Context

**Gathered:** 2025-02-02
**Status:** Ready for planning

<domain>
## Phase Boundary

建立完整的GRPO训练流程，支持从SFT模型继续训练，实现reward函数评估框架。核心功能包括GRPO训练脚本、format_reward_fn（三级评分）、tsc_reward_fn（SUMO仿真）、并行SUMO仿真架构。

</domain>

<decisions>
## Implementation Decisions

### 训练超参数管理
- **参数来源优先级**：YAML配置文件设置默认值 + 命令行参数可覆盖
- **缺失参数处理**：缺少必需参数时交互式提示用户输入
- **SFT模型路径**：在配置文件中设置model_path作为默认值
- **参数范围**：包含GRPO核心参数（KL散度系数、采样温度）、生成控制参数（max_new_tokens、top_p、repetition_penalty）、完整训练参数（优化器类型、梯度裁剪、warmup步数）

### SUMO仿真恢复机制
- **状态文件使用**：单文件独立计算（每个状态文件读取 → 恢复 → 推进 → 计算reward）
- **恢复起点**：从状态文件中保存的仿真时间点继续推进
- **推进时长**：可配置时长（在配置文件中设置）
- **相位顺序**：使用SUMO网络文件中定义的默认相位顺序
- **TSC决策逻辑**：
  - 模型输出"是"（延长）→ 当前相位绿灯延长配置的时长 → 推进仿真 → 计算reward
  - 模型输出"否"（切换）→ 切换到下一个相位（固定顺序）→ 推进配置时长 → 计算reward

### 并行仿真架构
- **端口分配策略**：系统随机分配空闲端口
- **进程数控制**：在配置文件中设置固定的最大并行进程数
- **失败处理**：任何SUMO进程失败（崩溃、端口冲突等）时，整个batch的reward计算失败并报错
- **端口冲突预防**：启动SUMO前预检查端口是否可用，不可用时尝试其他端口

### Reward函数链设计
- **三级format评分机制**：
  1. **严格format** → 弱正分（如+1）+ tsc_reward加权
  2. **部分遵守format**（能通过正则提取yes/no）→ 弱负分（如-0.5）+ tsc_reward加权
  3. **完全不遵守format** → 强负分（如-10），直接返回，不计算tsc_reward
- **正则规则**：在配置文件中定义用于提取yes/no的正则表达式模式
- **权重调整策略**：基于format准确率动态调整
  - 监控format准确率，当达到配置的阈值（如95%）后降低format权重
  - 在配置文件中设置target_format_accuracy和min_format_weight参数
- **加权组合**：final_reward = format_weight × format_reward + tsc_weight × tsc_reward

### Claude's Discretion
- SUMO仿真的具体启动参数和命令行选项
- Python多进程的具体实现方式（Process/Pool/ProcessPoolExecutor）
- Format验证的具体解析逻辑（JSON schema定义、字段名等）
- TSC reward的具体计算公式（如何衡量排队车辆数变化）

</decisions>

<specifics>
## Specific Ideas

- 状态文件是由数据生成器预生成的，每个状态文件独立使用
- Format奖励采用软约束机制：即使不完全遵守格式，只要能提取有效决策就继续计算TSC reward
- 动态权重调整确保训练早期关注format正确性，后期更关注TSC性能
- 端口预检查机制避免SUMO启动失败影响整个batch

</specifics>

<deferred>
## Deferred Ideas

无 — 讨论保持在Phase 1范围内（GRPO训练核心基础设施）

</deferred>

---

*Phase: 01-grpo-core-infrastructure*
*Context gathered: 2025-02-02*
