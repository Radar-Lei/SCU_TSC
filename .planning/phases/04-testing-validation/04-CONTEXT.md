# Phase 4: 测试、验证和完善 - Context

**Gathered:** 2026-02-02
**Status:** Ready for planning

<domain>
## Phase Boundary

通过单元测试和集成测试验证系统各组件正确性，确保端到端流程稳定运行。

测试覆盖reward函数、Max Pressure算法、配置加载、小规模端到端训练流程。不添加新功能，仅验证已实现功能的正确性和稳定性。

</domain>

<decisions>
## Implementation Decisions

### 单元测试框架

**测试框架选择：**
- 使用pytest作为主要测试框架（现代、功能丰富、自动发现、fixture系统）
- 测试文件按功能模块组织在tests/目录下：
  - `tests/test_format_reward.py`
  - `tests/test_tsc_reward.py`
  - `tests/test_max_pressure.py`
  - `tests/test_config.py`
  - `tests/test_integration.py`

**测试函数命名：**
- 使用详细描述性命名，清晰表达测试意图
- 示例：`test_format_reward_strict_valid_json_returns_1_0`
- 示例：`test_tsc_reward_normalization_positive_delta_within_range`
- 示例：`test_max_pressure_given_minimum_green_time_when_pressure_high_then_returns_yes`

**SUMO测试策略：**
- ✅ 使用真实SUMO仿真运行测试（不使用mock或假SUMO）
- ✅ 复用现有的SUMO数据集（tests/fixtures/复用现有数据）
- ✅ 测试环境需要docker容器（因为SUMO和unsloth在docker中）

### 测试覆盖范围

**format_reward_fn边界情况测试：**
- ✅ 空/无效输入：空字符串、None、仅空格、特殊字符
- ✅ 格式错误的JSON：缺失花括号、字段名拼写错误、多余逗号、非JSON字符串
- ✅ 有效变体：完全合规、字段多余、字段缺失、大小写不一致
- ✅ 极端情况：超大输入、嵌套JSON、Unicode字符、混合格式

**Max Pressure算法边界情况测试：**
- ✅ 输入数据异常：空字典、None、缺失必需字段、字段类型错误
- ✅ 排队数值边界：排队数为0、负数、极大值、浮点数
- ✅ 相位配置：单相位、双相位、四相位、非标准相位数
- ✅ 时间约束边界：最小绿灯时间已达、已达最大绿灯时间、边界值刚好触发

**配置加载测试：**
- ✅ 文件问题：文件不存在、YAML语法错误、编码错误
- ✅ 配置内容错误：必需字段缺失、类型错误、数值超出范围
- ✅ 优先级覆盖：CLI参数覆盖YAML、部分覆盖、全部覆盖、冲突处理
- ✅ 验证逻辑：默认值测试、边界值测试、可选字段测试

**tsc_reward_fn边界情况测试：**
- ✅ SUMO执行失败：SUMO进程启动失败、端口冲突、仿真崩溃、超时
- ✅ 排队数值极端：排队数为0、负数、极大值、所有相位0排队
- ✅ 批量处理边界：单样本、大批量（100+）、并行worker数量边界
- ✅ 归一化边界：delta为0、极大delta、负delta、scale为0或极小值

### 集成测试策略

**测试数据规模：**
- ✅ 使用中等规模进行集成测试
- ✅ 50条GRPO数据、20条SFT数据、10步训练
- ✅ 平衡测试时间和验证有效性

**测试数据准备：**
- ✅ 测试脚本运行时动态生成小规模数据
- ✅ 生成后的数据可复用（避免每次重新生成）

**验证检查点：**
- ✅ 模型输出验证：检查模型文件存在、大小合理、可加载
- ✅ 训练日志验证：检查训练日志无ERROR、有reward统计、loss下降
- ✅ 数据格式验证：SFT训练后GRPO数据可加载、格式正确
- ✅ 执行时间验证：整个流程在合理时间内完成（如30分钟内）

**失败处理：**
- ✅ 继续执行后续步骤，收集所有失败信息
- ✅ 最终输出完整的错误报告
- ✅ 便于一次性发现所有问题

### 测试执行和CI

**测试执行方式：**
- ✅ 创建脚本 `scripts/run_tests.sh` 自动运行测试
- ✅ 脚本自动启动docker容器并在容器中执行pytest
- ✅ 开发者运行脚本即可完成全部测试

**测试分类标记：**
- ✅ 使用 `@pytest.mark.integration` 标记依赖SUMO/unsloth的测试
- ✅ 便于选择性运行不同类型的测试

**代码覆盖率：**
- ✅ 不设置覆盖率目标，仅测试关键路径和边界情况
- ✅ 关注测试质量而非覆盖率数字

**CI集成：**
- ✅ 暂不配置GitHub Actions或其他CI系统
- ✅ 仅本地docker测试满足当前需求

### Claude's Discretion

- pytest配置文件（pytest.ini或pyproject.toml）的具体参数设置
- 测试夹具（fixture）的具体实现方式
- 动态生成测试数据的具体脚本逻辑
- scripts/run_tests.sh脚本的详细实现
- SUMO测试数据的抽样策略

</decisions>

<specifics>
## Specific Ideas

- "所有测试必须在docker容器中运行，因为SUMO和unsloth都在docker中"
- "创建scripts/run_tests.sh脚本，让测试运行自动化"
- "集成测试使用中等规模数据（50条GRPO、20条SFT、10步），平衡时间和有效性"
- "测试失败时收集所有错误而不是立即停止，便于一次性发现所有问题"

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 04-testing-validation*
*Context gathered: 2026-02-02*
