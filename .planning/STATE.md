# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2025-02-02)

**Core value:** 模型能够根据SUMO仿真状态的相位排队信息，准确判断是否延长当前绿灯相位，以最小化整个交叉口的排队车辆数。
**Current focus:** Phase 3: 训练流程集成

## Current Position

Phase: 3 of 4 (训练流程集成)
Plan: 3 of 3 in current phase
Status: Phase 3 complete
Last activity: 2026-02-02 — Completed 03-03-PLAN.md (集成验证到训练流程)

Progress: [████████████████████████] 100% (3/3 plans in Phase 3)

## Performance Metrics

**Velocity:**
- Total plans completed: 10
- Average duration: 5m 55s
- Total execution time: 58m 58s

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 1. GRPO训练核心基础设施 | 4 | 4 | 7m 48s |
| 2. Max Pressure算法和配置管理 | 3 | 3 | 5m 16s |
| 3. 训练流程集成 | 3 | 3 | 4m 25s |
| 4. 测试、验证和完善 | 0 | 0 | - |

**Recent Trend:**
- Last 5 plans: 4m 44s
- Trend: Accelerating

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

**From 02-02:**
- 创建中央训练配置文件training_config.yaml（区别于grpo_config.yaml）
- 配置按功能分层：training (SFT/GRPO)、simulation (SUMO)、reward (format/TSC/max_pressure)、paths、logging
- TrainingConfig类层次结构镜像YAML嵌套结构，使用property方法提供便捷访问
- 保持向后兼容：grpo_config.yaml继续用于数据生成，training_config.yaml用于训练
- 配置优先级：CLI参数 > 配置文件 > 默认值

**From 02-03:**
- 所有配置类在`__post_init__`中自动验证参数范围和约束
- 使用ValueError统一错误类型，错误信息包含参数名和当前值
- 命令行参数覆盖通过默认值比较检测（而非None检查）
- 验证测试套件覆盖所有主要验证规则和边界情况

**From 03-01:**
- docker/publish.sh升级为现代化CI/CD脚本（144行→330行）
- 双重依赖检查机制：主机侧+容器内，确保CUDA/SUMO/Python包可用
- 动态进度指示器：[Step N/4]标记+✓完成标记，ANSI颜色美化
- 失败快速停止：子shell错误捕获+红色错误信息+exit 1
- 训练摘要输出：训练时间+数据集大小+模型路径（outputs/YYYY-MM-DD_sft/和outputs/YYYY-MM-DD_grpo/）

**From 03-02:**
- 数据验证脚本采用静默成功模式（验证通过时不输出，失败时输出详细错误）
- SUMO状态文件采用抽样验证策略（默认10个文件）实现快速验证
- ValidationResult统一收集器模式（errors + warnings，格式化输出）
- 退出码标准化：0=通过、1=验证失败、2=意外错误
- 模块化验证函数设计（validate_grpo_dataset、validate_sft_dataset、validate_sumo_state_files、validate_config_and_environment）
- CLI支持多种验证组合（--grpo-only、--sft-only、--verify-sumo、--check-env、--verbose）

**From 03-03:**
- 验证时机：在整个训练流程开始前验证一次（Step 0/5），而不是每个训练步骤前都验证
- 路径策略：容器内使用固定路径`/home/samuel/SCU_TSC`，主机使用环境变量`PROJECT_DIR`或自动检测
- 容器环境检测：通过检查`/proc/1/cgroup`判断是否在容器内运行
- 错误处理：验证失败时输出红色错误信息到stderr，立即退出不执行任何训练步骤
- 验证耗时：记录验证耗时并在训练摘要中显示，便于监控验证性能
- 退出码规范：验证失败返回1，异常返回2，成功返回0

### Pending Todos

[From .planning/todos/pending/ — ideas captured during sessions]

None yet.

### Blockers/Concerns

[Issues that affect future work]

- **pytest未安装：** 当前环境没有pytest，测试手动验证通过。建议Phase 4中安装pytest并集成CI/CD
- **覆盖检测局限性：** 默认值比较方法在用户显式传入默认值时无法区分（罕见情况）

## Session Continuity

Last session: 2026-02-02
Stopped at: Completed 03-03-PLAN.md (集成验证到训练流程)
Resume file: None
