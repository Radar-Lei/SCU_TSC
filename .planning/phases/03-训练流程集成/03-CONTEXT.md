# Phase 3: 训练流程集成 - Context

**Gathered:** 2026-02-02
**Status:** Ready for planning

<domain>
## Phase Boundary

完善docker/publish.sh脚本，实现完整的四步训练流程（GRPO数据生成→SFT数据合并→SFT训练→GRPO训练），并添加数据验证步骤确保训练前数据质量。训练流程集成和自动化是核心范围，具体算法优化属于其他阶段。

</domain>

<decisions>
## Implementation Decisions

### 脚本行为模式
- **失败策略：** 快速停止（默认）— 任何步骤失败立即停止训练流程
- **日志记录：** 自适应模式 — 正常时简洁日志，失败时自动显示详细输出
- **进度显示：** 动态指示器 — 显示spinner和当前步骤名称
- **错误通知：** 高亮显示 — 在stderr输出红色错误信息+失败步骤详情

### 数据验证策略
- **验证项：** 全覆盖 — GRPO数据集格式、SUMO状态文件、模型和配置文件、系统环境
- **失败策略：** 严格停止 — 任何验证失败立即停止训练流程
- **验证时机：** 训练前统一验证 — 在整个publish.sh开始前验证一次所有数据
- **验证报告：** 仅失败项 — 成功时不输出，失败时显示详细信息

### 训练输出管理
- **模型保存：** 日期命名 — outputs/YYYY-MM-DD/、outputs/YYYY-MM-DD_sft/、outputs/YYYY-MM-DD_grpo/
- **中间文件：** 保留最近几个 — 保留最近N个SFT训练checkpoint，删除旧的
- **临时文件：** 自动清理 — 脚本结束后立即删除所有临时文件
- **输出摘要：** 显示摘要 — 训练成功完成后显示最终模型路径、训练时间、数据集大小等关键信息

### 部署和环境配置
- **执行环境：** Docker内执行 — 在Docker容器内执行publish.sh，环境隔离
- **配置文件：** 默认+覆盖 — 默认config/目录，支持--config参数覆盖
- **环境变量：** 仅配置文件 — 所有配置通过YAML文件，不使用环境变量
- **依赖检查：** 启动时检查 — 脚本开始时检查所有依赖（CUDA、SUMO、Python包）

### Claude's Discretion
- 保留checkpoint的具体数量（N值）
- 临时文件清理的具体实现方式
- 日志文件的具体命名和存储位置
- 动态spinner的具体实现细节

</decisions>

<specifics>
## Specific Ideas

- publish.sh应该像现代CI/CD脚本一样清晰、可靠
- 数据验证要快（几秒内完成），不要让用户等很久才发现问题
- 训练成功后应该让人一眼就能看到最重要的信息（模型在哪）

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 03-训练流程集成*
*Context gathered: 2026-02-02*
