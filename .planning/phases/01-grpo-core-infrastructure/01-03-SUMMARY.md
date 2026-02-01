---
phase: 01-grpo-core-infrastructure
plan: 03
subsystem: reward-calculation
tags: [sumo, traffic-simulation, reward-function, parallel-processing, multiprocessing]

# Dependency graph
requires:
  - phase: 01-grpo-core-infrastructure
    plan: 01
    provides: GRPO训练脚本框架，SUMOInterface基础接口，数据结构定义
provides:
  - TSC reward计算函数（单样本和批量版本）
  - 并行SUMO reward计算器（多进程架构）
  - 端口检查和随机分配机制
  - Reward归一化方法（tanh函数）
affects: [01-04-integrated-reward, 02-algorithm-config]

# Tech tracking
tech-stack:
  added: [multiprocessing.Pool, socket port binding, traci state loading]
  patterns: [worker函数模块级定义用于pickle，SimpleNamespace配置重建]

key-files:
  created:
    - grpo/sumo_reward.py
  modified:
    - grpo/sumo_interface.py
    - grpo/config.py
    - config/grpo_config.yaml
    - grpo/__init__.py

key-decisions:
  - "使用tanh(delta/scale)归一化reward到[-1,1]，scale=10.0"
  - "并行计算使用multiprocessing.Pool，worker函数必须是模块级函数"
  - "端口检查通过socket.bind()测试，随机端口范围10000-60000"
  - "任何SUMO进程失败时整个batch失败（fast-fail策略）"

patterns-established:
  - "Pattern 1: 从状态文件恢复SUMO仿真进行what-if分析"
  - "Pattern 2: 根据决策yes/no分别执行延长相位/切换相位操作"
  - "Pattern 3: 排队数变化delta作为负reward（改善为正，恶化为负）"

# Metrics
duration: 15min
completed: 2026-02-02
---

# Phase 01 Plan 03: SUMO Reward计算和并行仿真架构 Summary

**基于SUMO仿真的TSC reward计算系统，使用多进程并行架构，tanh归一化排队数变化到[-1,1]**

## Performance

- **Duration:** 15 min
- **Started:** 2026-02-01T18:17:23Z
- **Completed:** 2026-02-01T18:32:23Z (estimated)
- **Tasks:** 4
- **Files modified:** 5 (1 created, 4 modified)

## Accomplishments

- 实现了从SUMO状态文件恢复仿真进行what-if分析的完整流程
- 建立了根据决策（yes/no）推进仿真的机制：延长相位 vs 切换相位
- 实现了排队数变化到reward的归一化（tanh函数，scale=10.0）
- 构建了多进程并行SUMO reward计算架构，支持max_workers配置
- 添加了端口检查和随机分配机制，避免端口冲突

## Task Commits

Each task was committed atomically:

1. **Task 1: 更新sumo_interface.py添加端口检查和恢复方法** - `b625109` (feat)
2. **Task 2: 创建sumo_reward.py并实现tsc_reward_fn** - `15b127c` (feat)
3. **Task 3: 实现并行SUMO reward计算器** - `74c3e1e` (feat)
4. **Task 4: 更新配置和导出** - `18cec94` (feat)

**Plan metadata:** (to be committed after STATE.md update)

## Files Created/Modified

### Created

- `grpo/sumo_reward.py` - TSC reward计算核心模块
  - `TSCResult`数据类：记录reward、排队数、成功状态
  - `parse_prompt_for_decision_info()`：从prompt JSON提取决策所需信息
  - `extract_decision_from_output()`：从模型输出提取yes/no决策（正则匹配）
  - `normalize_reward()`：使用tanh将排队数变化归一化到[-1,1]
  - `calculate_tsc_reward_single()`：单样本reward计算（从状态文件恢复→执行决策→计算reward）
  - `calculate_tsc_reward_worker()`：模块级worker函数（用于多进程pickle）
  - `tsc_reward_fn()`：批量reward计算（单样本for循环版本）
  - `ParallelSUMORewardCalculator`类：多进程并行计算器

### Modified

- `grpo/sumo_interface.py` - SUMO接口增强
  - 添加`find_available_port()`：模块级函数，通过socket.bind()检测端口可用性
  - 更新`start()`方法：使用find_available_port()进行端口检查，提高重试次数到10次
  - 添加`start_from_state()`：封装从状态文件恢复并启动仿真的流程
  - 导入socket模块用于端口绑定检查

- `grpo/config.py` - 训练配置扩展
  - 添加`port_range: List[int]`字段（默认[10000, 60000]）
  - 添加`reward_scale: float`字段（默认10.0）
  - 更新`to_dict()`方法包含新字段

- `config/grpo_config.yaml` - 配置文件更新
  - 添加`port_range: [10000, 60000]`端口范围配置
  - 添加`reward_scale: 10.0`归一化参数
  - 更新注释说明SUMO仿真参数用途

- `grpo/__init__.py` - 模块导出更新
  - 导出`tsc_reward_fn`、`calculate_tsc_reward_single`
  - 导出`ParallelSUMORewardCalculator`、`TSCResult`

## Decisions Made

### 1. Reward归一化方法选择

**Decision:** 使用tanh函数归一化，scale参数设为10.0

**Rationale:**
- tanh提供平滑的[-1, 1]映射，避免硬clipping的梯度消失
- scale=10.0意味着±10辆车的变化达到饱和（合理范围，避免极端值主导）
- 公式：`reward = tanh(-delta / scale)`，delta为负（改善）时reward为正

### 2. 并行计算架构

**Decision:** 使用multiprocessing.Pool，worker函数必须是模块级函数

**Rationale:**
- SUMO仿真是CPU密集型，多进程可以真正并行（绕过GIL）
- Python的pickle需要函数在模块级别（不是类方法或闭包）
- 使用SimpleNamespace重建配置对象，避免复杂的序列化问题

### 3. 错误处理策略

**Decision:** 任何SUMO进程失败时整个batch失败（fast-fail）

**Rationale:**
- GRPO训练需要完整的reward向量，部分失败会导致batch不一致
- 快速失败可以让训练流程及时发现问题，而不是产生错误的梯度
- 失败原因记录在TSCResult.error中，便于调试

### 4. 端口分配策略

**Decision:** 随机端口范围10000-60000，启动前检查可用性

**Rationale:**
- 避免硬编码端口导致的冲突（并行计算尤其重要）
- socket.bind()是检测端口可用性的可靠方法
- 大范围端口池支持高并发（max_workers=4时需要4个不同端口）

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None - all tasks completed smoothly with verification passing.

## Architecture Highlights

### TSC Reward计算流程

1. **输入处理**
   - 从prompt JSON解析：tl_id_hash, current_phase_id, phase_order
   - 从模型输出提取决策：正则匹配`{extend: yes/no}`

2. **SUMO仿真恢复**
   - 使用`SUMOInterface.start_from_state(state_file)`恢复仿真
   - 随机端口分配（find_available_port()）
   - 记录初始排队数：`queue_before`

3. **决策执行**
   - yes → `sumo.extend_phase(tl_id, extend_seconds)`
   - no → 找phase_order中下一个phase_id并调用`sumo.set_phase()`
   - 推进仿真：for _ in range(extend_seconds): `sumo.step()`

4. **Reward计算**
   - 记录结束排队数：`queue_after`
   - 计算变化：`delta = queue_after - queue_before`
   - 归一化：`reward = tanh(-delta / 10.0)`
   - 改善（delta<0）→ reward>0，恶化（delta>0）→ reward<0

### 并行计算架构

```
ParallelSUMORewardCalculator.calculate_batch()
  ├─ 准备任务列表：zip(prompts, outputs, state_files)
  ├─ 配置转字典：config.__dict__
  └─ multiprocessing.Pool(max_workers)
       └─ pool.starmap(calculate_tsc_reward_worker, tasks)
            └─ 每个worker进程：
                 ├─ 重建config: SimpleNamespace(**config_dict)
                 ├─ 提取决策: extract_decision_from_output()
                 └─ 调用calculate_tsc_reward_single()
```

### 配置传播

```python
# YAML配置 → GRPOTrainingConfig对象
config = GRPOTrainingConfig.from_yaml("config/grpo_config.yaml")

# 训练时传递给reward函数
rewards = tsc_reward_fn(prompts, outputs, state_files, config)

# 单样本计算时使用
sumocfg_path = getattr(config, 'sumocfg_path', None)  # 需要扩展
extend_seconds = getattr(config, 'extend_seconds', 5)
```

**Note:** 当前实现在`calculate_tsc_reward_single`中尝试从state_file路径推断sumocfg，这在未来可能需要优化（例如在数据集中直接存储sumocfg_path）。

## Next Phase Readiness

### Ready for Next Phase (01-04: Integrated Reward)

- ✅ TSC reward函数完整实现（单样本和批量）
- ✅ 并行计算架构就绪
- ✅ 配置系统已扩展（port_range, reward_scale）
- ✅ 从grpo包导出所有必需函数

### Recommendations for 01-04

1. **Integrated Reward函数**需要组合format_reward和tsc_reward：
   ```python
   def integrated_reward_fn(prompts, outputs, state_files, config):
       format_rewards = format_reward_fn(outputs, config)
       tsc_rewards = tsc_reward_fn(prompts, outputs, state_files, config)
       return [
           config.format_weight * fr + config.tsc_weight * tr
           for fr, tr in zip(format_rewards, tsc_rewards)
       ]
   ```

2. **错误处理策略**需要在集成时统一：
   - format_reward不会失败（总能返回数值）
   - tsc_reward可能失败（返回0.0或抛出异常）
   - 集成函数需要决定：部分失败时如何处理

3. **性能优化**建议：
   - 小batch（batch_size=2, num_generations=4 → 总共8个样本）可以不用并行
   - 大batch（未来扩展）时启用ParallelSUMORewardCalculator
   - 可以添加config参数控制是否启用并行：`use_parallel_reward`

### Blockers/Concerns

None - this phase is complete and ready for integration.

---
*Phase: 01-grpo-core-infrastructure*
*Plan: 03*
*Completed: 2026-02-02*
