# Phase 2: Max Pressure算法和配置管理 - Context

**Gathered:** 2026-02-02
**Status:** Ready for planning

## Phase Boundary

实现Max Pressure baseline算法用于reward计算参考，建立中央配置管理系统（training_config.yaml + 配置加载逻辑）。不涉及训练流程集成（Phase 3）或测试（Phase 4）。

## Implementation Decisions

### Max Pressure输入输出接口
- **输入格式**：原始排队数字典 `{'phase_1': 5, 'phase_2': 3, ...}`
- **输出格式**：字符串 `'yes'` 或 `'no'`（与模型输出对齐）
- **上下文需求**：需要当前相位ID和已持续时间作为额外输入
- **压力计算**：标准公式 `pressure = upstream_queues - downstream_queues`
- **决策逻辑**：延长判断 - 当前相位压力 >= 其他相位时返回'yes'，否则返回'no'

### 配置参数粒度
- **训练参数**：全部可配置（所有TRL GRPOTrainer参数：学习率、batch size、KL系数等）
- **仿真参数**：可配置（SUMO相关：time_step、max_time、端口范围等）
- **Reward参数**：全部可配置（format_weight、tsc_weight、归一化scale等）
- **参数组织**：分组结构（training、simulation、reward、paths等分段）
- **路径配置**：相对路径约定 - 配置根目录，子路径按约定自动生成

### 配置验证严格度
- **缺失处理**：严格失败 - 必需参数缺失时立即抛出异常，训练不启动
- **范围验证**：严格验证 - 学习率、batch size等参数超出合理范围时抛出异常
- **类型验证**：严格类型检查 - 类型错误时立即失败，不尝试自动转换

### Max Pressure算法变体
- **标准公式**：使用标准Max Pressure公式 `P(i) = Σ(upstream_queues) - Σ(downstream_queues)`
- **车辆权重**：统一权重 - 只计算车辆数量，不考虑等待时间或车辆类型
- **时间限制**：最小/最大绿灯时间限制
  - 当前持续时间 < min_green_time → 必须延长（不能切换）
  - 当前持续时间 >= max_green_time → 必须切换（不能延长）
  - 在两者之间 → 根据Max Pressure压力判断是否延长
- **配置复用**：复用数据生成程序中读取SUMO配置文件（min_green_time、max_green_time）的逻辑

## Specific Ideas

- Max Pressure算法的输出格式应该与模型输出对齐（字符串'yes'/'no'），便于在reward计算中直接比较
- 配置文件按功能分组，每个分段在YAML中用注释清晰标注
- 相对路径约定：例如配置`data_dir: ./data`，则GRPO数据路径自动为`./data/grpo`

## Deferred Ideas

无 — 讨论保持在Phase 2范围内。

---

*Phase: 02-max-pressure-config*
*Context gathered: 2026-02-02*
