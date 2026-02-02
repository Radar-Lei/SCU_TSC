# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2025-02-02)

**Core value:** 模型能够根据SUMO仿真状态的相位排队信息，准确判断是否延长当前绿灯相位，以最小化整个交叉口的排队车辆数。
**Current focus:** Phase 2: Max Pressure算法和配置管理

## Current Position

Phase: 2 of 4 (Max Pressure算法和配置管理)
Plan: 1 of 3 in current phase
Status: In progress
Last activity: 2026-02-02 — Completed 02-01-PLAN.md (Max Pressure算法实现)

Progress: [██░░░░░░░░░░░░░░░░░░░] 33% (1/3 plans in Phase 2)

## Performance Metrics

**Velocity:**
- Total plans completed: 5
- Average duration: 9m 6s
- Total execution time: 45m 34s

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 1. GRPO训练核心基础设施 | 4 | 4 | 7m 48s |
| 2. Max Pressure算法和配置管理 | 1 | 3 | 22m 0s |
| 3. 训练流程集成 | 0 | 0 | - |
| 4. 测试、验证和完善 | 0 | 0 | - |

**Recent Trend:**
- Last 5 plans: 9m 6s
- Trend: On track

*Updated after each plan completion*

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

**From 01-01:**
- 创建独立的GRPOTrainingConfig类（区别于GRPOConfig数据生成配置）
- 数据格式在load_grpo_dataset中转换为TRL GRPOTrainer期望的格式
- 使用占位符reward函数（返回0.0）便于框架测试
- CLI参数可以覆盖YAML配置（优先级：CLI > YAML > 默认）

**From 01-02:**
- Format reward采用三级评分机制：严格+1.0、部分-0.5、无效-10.0
- 正则表达式可配置，支持带额外字段的JSON提取
- FormatResult提供详细的验证结果（is_strict、is_partial、extracted_decision）
- format_reward_fn与配置系统完全集成

**From 01-03:**
- 使用tanh(delta/scale)归一化reward到[-1,1]，scale=10.0
- 并行计算使用multiprocessing.Pool，worker函数必须是模块级函数
- 端口检查通过socket.bind()测试，随机端口范围10000-60000
- 任何SUMO进程失败时整个batch失败（fast-fail策略)

**From 01-04:**
- Early-return优化：format完全无效时跳过TSC仿真计算，节省大量时间
- 可配置的reward权重：format_weight和tsc_weight允许平衡格式正确性和TSC性能
- 批量处理优化：只对format有效（strict或partial）的样本运行TSC仿真
- Reward统计信息：每次计算后打印format准确率和平均reward，便于训练监控

**From 02-01:**
- Max Pressure算法采用简化版公式：pressure = queue_count（完整公式需upstream-downstream，但只有avg_queue_veh）
- 保守的错误处理策略：prompt解析失败时返回'no'（切换相位），避免不安全决策
- 时间约束优先级：最小绿/最大绿时间约束优先于压力比较
- Phase ID类型规范化：JSON字符串键转换为int，避免类型不匹配

### Pending Todos

[From .planning/todos/pending/ — ideas captured during sessions]

None yet.

### Blockers/Concerns

[Issues that affect future work]

None yet.

## Session Continuity

Last session: 2026-02-02
Stopped at: Completed 02-01-PLAN.md (Max Pressure算法实现)
Resume file: None
