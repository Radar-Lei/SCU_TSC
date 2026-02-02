---
phase: 05-max-pressure-baseline-integration
plan: 01
subsystem: reward-calculation
tags: [max-pressure, baseline, reward-comparison, grpo]

# Dependency graph
requires:
  - phase: 02-max-pressure-algorithm-config
    provides: Max Pressure决策函数和配置类
  - phase: 01-grpo-training-core
    provides: reward计算基础设施
provides:
  - 扩展的compute_reward()函数，支持Max Pressure baseline比较
  - 扩展的batch_compute_reward()函数，支持批量baseline计算和准确率统计
  - baseline决策信息集成到reward返回值中
affects: [06-grpo-training-loop-integration, reward-monitoring]

# Tech tracking
tech-stack:
  added: []
  patterns:
  - "Optional baseline comparison pattern: reward函数接受可选的baseline参数"
  - "Graceful degradation: baseline计算失败时不中断reward计算"
  - "Batch baseline pre-computation: 在TSC计算前批量计算baseline决策"

key-files:
  created: []
  modified:
  - grpo/reward.py - 扩展reward计算函数，添加Max Pressure baseline比较

key-decisions:
  - "baseline比较完全可选：所有新参数为可选，保持向后兼容"
  - "早期baseline计算：在format_reward后、TSC计算前进行baseline决策，避免不必要的SUMO仿真"
  - "错误容忍策略：baseline计算失败时记录错误但不中断reward计算"
  - "统计信息输出：通过print()输出baseline准确率，暂不扩展RewardStats dataclass"

patterns-established:
  - "Baseline comparison pattern: 可选的enable_baseline参数控制是否进行baseline比较"
  - "Three-tier baseline info: baseline_decision, model_decision, matches_baseline"
  - "Graceful degradation: baseline_info包含baseline_error字段记录失败原因"

# Metrics
duration: 2min
completed: 2026-02-02
---

# Phase 5 Plan 1: Max Pressure Baseline集成到Reward计算 Summary

**扩展compute_reward()和batch_compute_reward()函数，集成Max Pressure baseline决策比较，支持可选的baseline准确率统计**

## Performance

- **Duration:** 2 min
- **Started:** 2026-02-02T11:38:05Z
- **Completed:** 2026-02-02T11:39:52Z
- **Tasks:** 2
- **Files modified:** 1

## Accomplishments

- compute_reward()函数支持Max Pressure baseline比较，当enable_baseline=True时自动调用max_pressure_decision_from_prompt()
- batch_compute_reward()函数支持批量baseline计算，使用batch_max_pressure_decision()预计算所有baseline决策
- baseline决策信息（baseline_decision, model_decision, matches_baseline）集成到reward返回值中
- 添加baseline准确率统计输出：`Baseline Accuracy: XX.XX% (N/M)`
- 完整的错误处理：捕获ValueError, KeyError, json.JSONDecodeError，失败时记录baseline_error
- 保持完全向后兼容：所有新参数为可选，默认值为None或False

## Task Commits

Each task was committed atomically:

1. **Task 1: 扩展compute_reward()添加baseline比较** - `6479e79` (feat)
2. **Task 2: 扩展batch_compute_reward()支持baseline** - `ee4cac3` (feat)

**Plan metadata:** [待提交] (docs: complete plan)

_Note: TDD tasks may have multiple commits (test → feat → refactor)_

## Files Created/Modified

- `grpo/reward.py` - 扩展compute_reward()和batch_compute_reward()函数，添加Max Pressure baseline比较逻辑

## Decisions Made

- **Baseline比较时机：** 在format_reward计算后、TSC reward计算前进行baseline决策，这样可以利用format验证结果提取模型决策，同时避免在format无效时进行不必要的baseline计算
- **参数传递策略：** compute_reward()接受单个时间参数（green_elapsed, min_green, max_green），batch_compute_reward()接受时间参数列表（green_elapsed_list, min_green_list, max_green_list），保持API一致性
- **错误处理策略：** baseline计算失败时设置baseline_info = {"baseline_error": str(e)}，而不是抛出异常或中断reward计算，确保baseline功能失败不影响训练流程
- **统计信息输出：** 通过print()输出baseline准确率，而不是扩展RewardStats dataclass，最小化对现有代码的影响
- **配置传递：** 接受mp_config参数（MaxPressureConfig类型），如果为None则使用默认配置MaxPressureConfig()，提供灵活性同时保持易用性

## Deviations from Plan

None - plan executed exactly as written.

## Authentication Gates

None encountered during execution.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- reward.py已集成Max Pressure baseline比较功能
- compute_reward()和batch_compute_reward()函数支持可选的baseline参数
- baseline决策信息和准确率统计可用于训练监控和评估
- ready for next phase: 在训练循环中启用baseline比较，监控模型与Max Pressure baseline的一致性

---
*Phase: 05-max-pressure-baseline-integration*
*Completed: 2026-02-02*
