---
phase: 02-max-pressure-config
plan: 01
subsystem: traffic-control-algorithm
tags: [max-pressure, baseline, traffic-signal-control, queue-based-decision]

# Dependency graph
requires:
  - phase: 01-grpo-core-infrastructure
    provides: grpo module structure, reward calculation framework, SUMO interface
provides:
  - Max Pressure baseline algorithm implementation for traffic signal control
  - Configurable decision function with time constraints (min/max green time)
  - Batch processing capability for baseline comparison in reward calculation
  - Evaluation metrics for comparing model decisions against baseline
affects: [reward-calculation, training-evaluation, baseline-comparison]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Simplified Max Pressure formula: pressure = queue_count (upstream only)"
    - "Time constraint enforcement: min_green and max_green boundaries"
    - "Batch processing with error handling: conservative 'no' fallback on parse errors"
    - "Phase ID type normalization: JSON string keys converted to int"

key-files:
  created:
    - grpo/max_pressure.py
  modified:
    - grpo/__init__.py

key-decisions:
  - "Simplified Max Pressure to pressure=queue_count (full formula is upstream-downstream, but only avg_queue_veh available)"
  - "Conservative error handling: return 'no' (switch phase) on parse failures to avoid unsafe decisions"
  - "Batch functions included from start (Task 1) for consistency with existing batch_reward patterns"

patterns-established:
  - "Baseline pattern: algorithm implements same yes/no interface as model for direct comparison"
  - "Config class pattern: dataclass with offset/override/threshold parameters for flexibility"
  - "Error handling pattern: batch functions catch exceptions and return safe defaults"

# Metrics
duration: 22min
completed: 2026-02-02
---

# Phase 2 Plan 1: Max Pressure算法实现总结

**Max Pressure baseline算法实现，支持时间约束、批量处理和与模型决策的baseline比较评估**

## Performance

- **Duration:** 22 min
- **Started:** 2026-02-02T05:15:06Z
- **Completed:** 2026-02-02T05:37:16Z
- **Tasks:** 3
- **Files modified:** 2

## Accomplishments

- 实现了完整的Max Pressure baseline算法，支持基于排队数的相位压力计算
- 添加了严格的时间约束检查（最小绿/最大绿时间），确保决策符合交通信号规范
- 提供了批量处理函数，便于在reward计算中与模型输出进行批量比较
- 实现了baseline评估指标（准确率、匹配列表），用于监控训练进展

## Task Commits

Each task was committed atomically:

1. **Task 1: 创建Max Pressure算法核心函数** - `d9a63d2` (feat)
2. **Task 2: 更新模块导出和配置集成** - `bac1aa4` (feat)
3. **Task 3: 添加batch决策函数** - (included in Task 1)

**Bug fix:** `c155d23` (fix)
**Plan metadata:** (to be committed)

## Files Created/Modified

- `grpo/max_pressure.py` - Max Pressure算法核心实现（351行）
  - `MaxPressureConfig`: 配置数据类，支持偏移、覆盖、阈值参数
  - `compute_phase_pressure()`: 压力计算函数（简化版：pressure = queue_count）
  - `max_pressure_decision()`: 核心决策函数，考虑时间约束和压力比较
  - `max_pressure_decision_from_prompt()`: 从JSON prompt提取信息的便捷函数
  - `batch_max_pressure_decision()`: 批量决策函数，带错误处理
  - `compare_with_baseline()`: 模型与baseline决策比较
  - `compute_baseline_accuracy()`: 计算一致性准确率

- `grpo/__init__.py` - 添加Max Pressure函数到模块导出
  - 导出所有Max Pressure相关函数和配置类
  - 保持与现有reward函数导出风格一致

## Decisions Made

- **简化Max Pressure公式**: 使用pressure = queue_count而非完整的upstream - downstream公式，因为当前数据结构只有avg_queue_veh（上游排队）
- **保守的错误处理策略**: 批量决策中，当prompt解析失败时返回'no'（切换相位），避免在数据异常时做出不安全的延长决策
- **时间约束优先级**: 最小绿时间和最大绿时间约束优先于压力比较，确保决策符合交通信号基本安全规范
- **Phase ID类型规范化**: 在max_pressure_decision_from_prompt中将JSON字符串键转换为int，避免类型不匹配错误

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] 修复json模块导入缺失**

- **Found during:** Task 3 验证阶段
- **Issue:** batch_max_pressure_decision函数的except块中使用json.JSONDecodeError，但json模块未在模块级别导入
- **Fix:** 在模块顶部添加`import json`
- **Files modified:** grpo/max_pressure.py
- **Verification:** 所有验证测试通过，包括批量决策错误处理
- **Committed in:** `c155d23`

**2. [Rule 1 - Bug] 修复phase_id类型处理**

- **Found during:** Task 3 验证阶段
- **Issue:** JSON解析后phase_metrics的键可能是字符串，导致与current_phase_id（整数）比较失败
- **Fix:** 在max_pressure_decision_from_prompt中使用`int(phase_id)`强制类型转换
- **Files modified:** grpo/max_pressure.py
- **Verification:** 批量决策测试通过，包括从JSON正确提取相位ID
- **Committed in:** `c155d23`

---

**Total deviations:** 2 auto-fixed (2 bugs)
**Impact on plan:** 两个bug修复都是代码正确性问题，不影响功能范围。批量函数在Task 1中已实现（原计划Task 3），实际提高了执行效率。

## Issues Encountered

无重大问题。执行过程中的两个bug都在验证阶段发现并快速修复。

## User Setup Required

None - 无需外部服务配置或用户手动设置。

## Next Phase Readiness

**已就绪的功能:**
- Max Pressure baseline算法可用于reward计算中的baseline比较
- 批量处理接口已就绪，可直接集成到reward chain中
- 评估指标（准确率、匹配列表）可用于训练监控

**后续阶段建议:**
- Phase 2-02: 可在reward计算中集成Max Pressure baseline作为参考
- Phase 3: 可使用compute_baseline_accuracy()追踪模型相对于baseline的改进
- 可选：如果需要更复杂的Max Pressure变体，可扩展MaxPressureConfig（如添加下游车辆数权重）

**无阻塞问题。**

---
*Phase: 02-max-pressure-config*
*Completed: 2026-02-02*
