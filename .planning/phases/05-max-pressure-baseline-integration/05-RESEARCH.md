# Phase 5: Max Pressure Baseline集成 - Research

**研究时间**: 2026-02-02
**领域**: GRPO训练中集成Max Pressure baseline算法
**置信度**: HIGH

## Summary

本Phase研究如何将已实现的Max Pressure算法（grpo/max_pressure.py，350行）集成到GRPO训练流程中，解决v1审计中发现的关键集成差距。

**核心发现**：
1. Max Pressure算法已完整实现但孤立，5个关键函数未被使用
2. 时间参数（green_elapsed, min_green, max_green）保存在数据集中但不在prompt JSON中
3. 需要在reward计算和训练脚本两个位置集成baseline功能
4. 配置系统已预留reward.max_pressure.*字段，仅需激活

**主要建议**：
采用审计报告推荐的混合方案：在reward计算层添加baseline比较逻辑，在训练层添加统计追踪。这样既能评估单样本质量，又能追踪训练进度。

## Standard Stack

### Core
| 组件 | 版本/位置 | 用途 | 为什么标准 |
|------|----------|------|-----------|
| `grpo/max_pressure.py` | 已存在(350行) | Max Pressure算法实现 | 已完整实现并测试(29个测试通过) |
| `grpo/reward.py` | 已存在 | Reward计算函数 | reward函数链核心 |
| `grpo/training.py` | 已存在 | GRPO训练脚本 | GRPOTrainer集成点 |
| `grpo/config.py` | 已存在 | 配置系统 | MaxPressureConfig已定义 |

### Supporting
| 组件 | 用途 | 使用场景 |
|------|------|----------|
| `max_pressure_decision_from_prompt()` | 单样本baseline决策 | reward计算中比较 |
| `batch_max_pressure_decision()` | 批量baseline决策 | 预计算所有baseline |
| `compare_with_baseline()` | 决策一致性比较 | 统计准确率 |
| `compute_baseline_accuracy()` | 计算baseline准确率 | 训练日志输出 |

### Alternatives Considered
| 方案 | 优点 | 缺点 | 何时使用 |
|------|------|------|----------|
| 仅在reward.py集成 | 简单，侵入性小 | 无法追踪整体训练进度 | 仅需单样本评估时 |
| 仅在training.py集成 | 集中管理统计 | 需要修改数据集加载流程 | 仅需训练级统计时 |
| **混合方案(推荐)** | 兼顾单样本和整体统计 | 两处都需要修改 | **生产环境** |

## Architecture Patterns

### Pattern 1: 单样本Baseline比较（Reward层）

**What**: 在`compute_reward()`和`batch_compute_reward()`中添加baseline比较逻辑

**When to use**: 需要在reward计算时评估模型决策与baseline的一致性

**Integration Point**: `grpo/reward.py`

**关键挑战**: 时间参数不在prompt JSON中，需要从数据集条目获取

**解决方案**:
```python
# 方案A: 修改batch_compute_reward签名，添加时间参数
def batch_compute_reward(
    prompts: List[str],
    outputs: List[str],
    state_files: List[str],
    chain_config: RewardChainConfig,
    sumo_config: Any,
    green_elapsed_list: List[float] = None,  # 新增
    min_green_list: List[float] = None,      # 新增
    max_green_list: List[float] = None,      # 新增
    enable_baseline: bool = False             # 新增
) -> Tuple[List[float], RewardStats]

# 方案B: 在dataset中添加时间字段，通过state_files对齐
# training.py中预加载时间参数，传递给reward_fn
```

**推荐**: 方案A（显式传递参数），因为：
1. 类型明确，易于测试
2. 不依赖隐式对齐逻辑
3. 向后兼容（参数可选）

### Pattern 2: 训练级Baseline统计（Training层）

**What**: 在`create_reward_function()`中预计算baseline决策，追踪整体准确率

**When to use**: 需要在训练过程中监控模型相对于baseline的改进

**Integration Point**: `grpo/training.py`

**实现步骤**:
```python
def create_reward_function(
    chain_config: RewardChainConfig,
    sumo_config,
    dataset,
    enable_baseline_tracking: bool = False  # 新增
) -> Callable:
    # 1. 预加载时间参数（从dataset）
    green_elapsed_list = dataset.get("current_green_elapsed", [])
    min_green_list = dataset.get("min_green", [])
    max_green_list = dataset.get("max_green", [])

    # 2. 预计算baseline决策
    if enable_baseline_tracking:
        from grpo.max_pressure import batch_max_pressure_decision, MaxPressureConfig
        mp_config = MaxPressureConfig(
            min_green_offset=sumo_config.max_pressure_min_green_offset,
            max_green_override=sumo_config.max_pressure_max_green_override,
            pressure_threshold=sumo_config.max_pressure_pressure_threshold
        )
        baseline_decisions = batch_max_pressure_decision(
            prompts=dataset["prompt"],
            green_elapsed_list=green_elapsed_list,
            min_green_list=min_green_list,
            max_green_list=max_green_list,
            config=mp_config
        )
    else:
        baseline_decisions = None

    def reward_fn(prompts, outputs, **kwargs):
        # ... 现有reward计算 ...

        # 新增: baseline统计
        if baseline_decisions:
            from grpo.max_pressure import compare_with_baseline, compute_baseline_accuracy
            model_decisions = [extract_decision(o) for o in outputs]
            matches = compare_with_baseline(
                model_decisions,
                baseline_decisions[:len(prompts)]
            )
            accuracy = compute_baseline_accuracy(model_decisions, matches)
            print(f"Baseline Accuracy: {accuracy:.2%} ({sum(matches)}/{len(matches)})")

        return rewards

    return reward_fn
```

### Pattern 3: 配置激活（Config层）

**What**: 在配置系统中激活Max Pressure相关配置

**When to use**: 需要配置baseline追踪行为

**Integration Point**: `config/training_config.yaml`, `grpo/config.py`

**当前状态**: 配置字段已存在但未使用

**需要激活**:
```yaml
# config/training_config.yaml
reward:
  max_pressure:
    enabled: true  # 激活baseline追踪
    min_green_offset: 0.0
    max_green_override: false
    pressure_threshold: 0.0
```

**配置加载**:
```python
# grpo/config.py - 已有MaxPressureConfig，需要在GRPOTrainingConfig中集成
@dataclass
class GRPOTrainingConfig:
    # ... 现有字段 ...

    # 新增
    enable_baseline: bool = False  # 是否启用baseline追踪
    baseline_config: MaxPressureConfig = field(default_factory=MaxPressureConfig)

    def __post_init__(self):
        # ... 现有验证 ...
        # 验证baseline配置一致性
        if self.enable_baseline and not self.baseline_config:
            raise ValueError("enable_baseline=True时必须提供baseline_config")
```

### Anti-Patterns to Avoid

- **直接在reward函数中解析时间参数**: 从prompt JSON解析时间参数会失败，因为prompt中不包含这些字段
- **硬编码默认时间值**: 使用固定的min_green=10, max_green=60会导致baseline决策不准确
- **每次reward计算都重新计算baseline**: 应该在训练开始前预计算，避免重复计算
- **忽略错误处理**: Max Pressure决策可能失败（JSON解析错误），应该返回'no'（保守策略）而非崩溃

## Don't Hand-Roll

| 问题 | 不要构建 | 使用替代 | 原因 |
|------|----------|----------|------|
| 时间参数提取 | 手写解析逻辑 | 使用dataset字段 | 数据集中已有`current_green_elapsed`, `min_green`, `max_green` |
| Baseline决策算法 | 自己实现Max Pressure | `max_pressure_decision_from_prompt()` | 已实现并测试通过 |
| 批量决策处理 | 手动循环和错误处理 | `batch_max_pressure_decision()` | 已包含错误处理逻辑 |
| 决策比较 | 手写比较逻辑 | `compare_with_baseline()` | 处理大小写标准化 |
| 准确率计算 | 手写统计 | `compute_baseline_accuracy()` | 已测试验证 |

**关键洞察**: Max Pressure模块已完整实现所有需要的函数，不要重复实现。

## Common Pitfalls

### Pitfall 1: 时间参数缺失错误

**What goes wrong**: 调用`max_pressure_decision_from_prompt()`时，尝试从prompt JSON中提取时间参数，导致KeyError

**Why it happens**: Prompt JSON（由`prompt_builder.py`生成）只包含：
- `crossing_id`
- `as_of` (timestamp)
- `phase_order`
- `state.current_phase_id`
- `state.phase_metrics_by_id`

**不包含**:
- `current_green_elapsed`
- `min_green`
- `max_green`

**How to avoid**:
1. 从dataset中获取时间参数（dataset中已保存）
2. 显式传递给`max_pressure_decision()`（而非`max_pressure_decision_from_prompt()`）
3. 或者修改`batch_max_pressure_decision()`接受dataset参数

**Warning signs**:
```python
# 错误模式
try:
    decision = max_pressure_decision_from_prompt(prompt, ...)  # 会KeyError
except KeyError as e:
    # 如果这里捕获current_green_elapsed等错误，说明模式错误
```

### Pitfall 2: 配置字段未激活

**What goes wrong**: `training_config.yaml`中定义了`reward.max_pressure.*`字段，但代码中未读取

**Why it happens**: 配置类（`GRPOTrainingConfig`）未包含Max Pressure配置字段

**How to avoid**:
1. 在`GRPOTrainingConfig`中添加`baseline_config: MaxPressureConfig`
2. 在`from_yaml()`中解析`reward.max_pressure`字段
3. 在`create_reward_function()`中传递`baseline_config`

**Warning signs**:
```python
# 配置文件中有
reward:
  max_pressure:
    enabled: true

# 但代码中
config = GRPOTrainingConfig.from_yaml(path)
print(config.baseline_config)  # AttributeError
```

### Pitfall 3: Baseline决策与模型决策长度不匹配

**What goes wrong**: 调用`compare_with_baseline()`时，两个列表长度不一致导致ValueError

**Why it happens**:
1. GRPO训练时每个prompt生成多个output（num_generations > 1）
2. Baseline决策只计算了dataset长度（每个prompt一个baseline）
3. 比较时未正确对齐

**How to avoid**:
```python
# 正确对齐
n = len(outputs)
aligned_baselines = baseline_decisions[:n]  # 或使用prompts索引对齐
matches = compare_with_baseline(model_decisions, aligned_baselines)
```

**Warning signs**:
```
ValueError: 决策列表长度不一致: model=8, baseline=2
```

### Pitfall 4: 单元测试Mock不足

**What goes wrong**: 测试baseline比较功能时，未正确mock Max Pressure决策

**Why it happens**: `batch_max_pressure_decision()`需要解析prompt JSON，测试数据准备复杂

**How to avoid**:
```python
# 使用fixture准备完整测试数据
@pytest.fixture
def baseline_integration_data():
    prompts = [
        json.dumps({"state": {"current_phase_id": 0, "phase_metrics_by_id": {...}}})
    ]
    green_elapsed_list = [15.0]
    min_green_list = [10.0]
    max_green_list = [60.0]
    return {
        "prompts": prompts,
        "green_elapsed_list": green_elapsed_list,
        "min_green_list": min_green_list,
        "max_green_list": max_green_list
    }

# 或者直接mock
from unittest.mock import patch
with patch('grpo.max_pressure.max_pressure_decision_from_prompt') as mock_mp:
    mock_mp.return_value = 'yes'
    # 测试逻辑
```

**Warning signs**: 测试需要准备大量SUMO状态文件才能运行

## Code Examples

### Example 1: 扩展compute_reward添加baseline比较

```python
# grpo/reward.py

def compute_reward(
    prompt: str,
    output: str,
    state_file: str,
    chain_config: RewardChainConfig,
    sumo_config: Any,
    tsc_reward_fn: Callable = None,
    # 新增参数
    green_elapsed: float = None,
    min_green: float = None,
    max_green: float = None,
    enable_baseline: bool = False,
    mp_config: MaxPressureConfig = None
) -> Tuple[float, Dict[str, Any]]:
    """
    计算单个样本的reward（可选baseline比较）
    """
    # 1. 现有format reward计算
    format_result = format_reward_fn(
        output,
        regex=chain_config.extract_regex,
        strict_reward=chain_config.format_strict,
        partial_reward=chain_config.format_partial,
        invalid_reward=chain_config.format_invalid
    )

    # 2. 现有early return逻辑
    if not format_result.is_partial and not format_result.is_strict:
        return format_result.reward, {
            "format_reward": format_result.reward,
            "tsc_reward": 0.0,
            "reason": "invalid_format"
        }

    # 3. 新增: baseline比较
    baseline_info = {}
    if enable_baseline and all(x is not None for x in [green_elapsed, min_green, max_green]):
        from grpo.max_pressure import max_pressure_decision_from_prompt

        try:
            baseline_decision = max_pressure_decision_from_prompt(
                prompt=prompt,
                green_elapsed=green_elapsed,
                min_green=min_green,
                max_green=max_green,
                config=mp_config or MaxPressureConfig()
            )
            model_decision = format_result.extracted_decision

            baseline_info = {
                "baseline_decision": baseline_decision,
                "model_decision": model_decision,
                "matches_baseline": (model_decision == baseline_decision) if model_decision else None
            }
        except (ValueError, KeyError, json.JSONDecodeError) as e:
            baseline_info = {"baseline_error": str(e)}

    # 4. 现有TSC reward计算
    if tsc_reward_fn is None:
        from .sumo_reward import calculate_tsc_reward_single
        tsc_reward_fn = calculate_tsc_reward_single

    decision = format_result.extracted_decision
    if decision is None:
        return format_result.reward, {
            "format_reward": format_result.reward,
            "tsc_reward": 0.0,
            "reason": "no_decision_extracted",
            **baseline_info
        }

    tsc_result = tsc_reward_fn(state_file, prompt, decision, sumo_config)
    tsc_reward = tsc_result.reward if tsc_result.success else 0.0

    # 5. 组合reward
    final_reward = (
        chain_config.format_weight * format_result.reward +
        chain_config.tsc_weight * tsc_reward
    )

    return final_reward, {
        "format_reward": format_result.reward,
        "tsc_reward": tsc_reward,
        "is_strict": format_result.is_strict,
        "is_partial": format_result.is_partial,
        **baseline_info  # 合并baseline信息
    }
```

### Example 2: 修改batch_compute_reward支持baseline

```python
# grpo/reward.py

def batch_compute_reward(
    prompts: List[str],
    outputs: List[str],
    state_files: List[str],
    chain_config: RewardChainConfig,
    sumo_config: Any,
    # 新增参数
    green_elapsed_list: List[float] = None,
    min_green_list: List[float] = None,
    max_green_list: List[float] = None,
    enable_baseline: bool = False,
    mp_config: MaxPressureConfig = None
) -> Tuple[List[float], RewardStats]:
    """
    批量计算reward（支持baseline比较）
    """
    from .sumo_reward import ParallelSUMORewardCalculator

    # 先计算所有format reward
    format_results = [
        format_reward_fn(
            output,
            regex=chain_config.extract_regex,
            strict_reward=chain_config.format_strict,
            partial_reward=chain_config.format_partial,
            invalid_reward=chain_config.format_invalid
        )
        for output in outputs
    ]

    # 新增: 预计算baseline决策
    baseline_decisions = []
    if enable_baseline and all(x is not None for x in [green_elapsed_list, min_green_list, max_green_list]):
        from grpo.max_pressure import batch_max_pressure_decision
        try:
            baseline_decisions = batch_max_pressure_decision(
                prompts=prompts[:len(outputs)],
                green_elapsed_list=green_elapsed_list[:len(outputs)],
                min_green_list=min_green_list[:len(outputs)],
                max_green_list=max_green_list[:len(outputs)],
                config=mp_config or MaxPressureConfig()
            )
        except Exception as e:
            print(f"Warning: Baseline calculation failed: {e}")

    # 筛选需要计算TSC的样本
    needs_tsc_indices = [
        i for i, r in enumerate(format_results)
        if r.is_strict or r.is_partial
    ]

    # 批量计算TSC reward（使用并行）
    tsc_rewards = [0.0] * len(outputs)
    if needs_tsc_indices:
        calculator = ParallelSUMORewardCalculator(max_workers=sumo_config.max_workers)

        # 准备需要计算TSC的样本
        tsc_prompts = [prompts[i] for i in needs_tsc_indices]
        tsc_outputs = [outputs[i] for i in needs_tsc_indices]
        tsc_state_files = [state_files[i] for i in needs_tsc_indices]

        try:
            tsc_results = calculator.calculate_batch(
                prompts=tsc_prompts,
                outputs=tsc_outputs,
                state_files=tsc_state_files,
                config=sumo_config
            )
            for idx, reward in zip(needs_tsc_indices, tsc_results):
                tsc_rewards[idx] = reward
        except RuntimeError as e:
            print(f"Warning: TSC reward calculation failed: {e}")

    # 组合最终reward
    final_rewards = []
    for i, format_result in enumerate(format_results):
        final_reward = (
            chain_config.format_weight * format_result.reward +
            chain_config.tsc_weight * tsc_rewards[i]
        )
        final_rewards.append(final_reward)

    # 新增: 计算baseline统计
    baseline_matches = 0
    if baseline_decisions:
        from grpo.max_pressure import compare_with_baseline
        model_decisions = [
            r.extracted_decision for r in format_results
            if r.extracted_decision is not None
        ]
        if model_decisions and len(model_decisions) == len(baseline_decisions):
            matches = compare_with_baseline(model_decisions, baseline_decisions)
            baseline_matches = sum(matches)

    # 计算统计信息
    stats = RewardStats(
        total_count=len(outputs),
        strict_format_count=sum(1 for r in format_results if r.is_strict),
        partial_format_count=sum(1 for r in format_results if r.is_partial),
        invalid_format_count=sum(1 for r in format_results if not r.is_strict and not r.is_partial),
        avg_format_reward=sum(r.reward for r in format_results) / len(outputs),
        avg_tsc_reward=sum(tsc_rewards) / len(outputs),
        avg_final_reward=sum(final_rewards) / len(outputs),
        format_accuracy=(sum(1 for r in format_results if r.is_strict or r.is_partial) / len(outputs))
    )

    # 扩展stats（可选：添加baseline_matches字段）
    # 注意：RewardStats是dataclass，可能需要扩展定义

    return final_rewards, stats
```

### Example 3: 修改create_reward_function添加统计追踪

```python
# grpo/training.py

def create_reward_function(
    chain_config: RewardChainConfig,
    sumo_config,
    dataset,
    enable_baseline_tracking: bool = False,  # 新增
    mp_config: MaxPressureConfig = None       # 新增
) -> Callable:
    """
    创建reward函数（支持baseline追踪）
    """
    # 预加载state_files（按数据集顺序）
    state_files = dataset["state_file"]

    # 新增: 预加载时间参数
    green_elapsed_list = dataset.get("current_green_elapsed", [None] * len(dataset))
    min_green_list = dataset.get("min_green", [None] * len(dataset))
    max_green_list = dataset.get("max_green", [None] * len(dataset))

    # 新增: 预计算baseline决策
    baseline_decisions = None
    if enable_baseline_tracking:
        from grpo.max_pressure import batch_max_pressure_decision

        try:
            baseline_decisions = batch_max_pressure_decision(
                prompts=dataset["prompt"],
                green_elapsed_list=green_elapsed_list,
                min_green_list=min_green_list,
                max_green_list=max_green_list,
                config=mp_config or MaxPressureConfig()
            )
            print(f"预计算{len(baseline_decisions)}个baseline决策")
        except Exception as e:
            print(f"Warning: Baseline预计算失败: {e}")
            enable_baseline_tracking = False

    def reward_fn(prompts: List[str], outputs: List[str], **kwargs) -> List[float]:
        """
        GRPOTrainer调用的reward函数
        """
        # 确保prompts和state_files长度匹配
        n = len(outputs)
        aligned_state_files = state_files[:n] if len(state_files) >= n else state_files

        # 对齐时间参数
        aligned_green_elapsed = green_elapsed_list[:n]
        aligned_min_green = min_green_list[:n]
        aligned_max_green = max_green_list[:n]

        rewards, stats = batch_compute_reward(
            prompts=prompts[:n],
            outputs=outputs,
            state_files=aligned_state_files,
            chain_config=chain_config,
            sumo_config=sumo_config,
            green_elapsed_list=aligned_green_elapsed,
            min_green_list=aligned_min_green,
            max_green_list=aligned_max_green,
            enable_baseline=enable_baseline_tracking,
            mp_config=mp_config
        )

        # 打印统计信息
        print(f"\n{'='*50}")
        print(f"Reward Statistics:")
        print(f"  Total: {stats.total_count}")
        print(f"  Format accuracy: {stats.format_accuracy:.1%}")
        print(f"  Strict: {stats.strict_format_count}, Partial: {stats.partial_format_count}, Invalid: {stats.invalid_format_count}")
        print(f"  Avg format reward: {stats.avg_format_reward:.3f}")
        print(f"  Avg TSC reward: {stats.avg_tsc_reward:.3f}")
        print(f"  Avg final reward: {stats.avg_final_reward:.3f}")

        # 新增: 打印baseline统计
        if enable_baseline_tracking and baseline_decisions:
            from grpo.max_pressure import compare_with_baseline, compute_baseline_accuracy
            model_decisions = [
                extract_decision(o) for o in outputs
                if extract_decision(o) is not None
            ]
            if model_decisions:
                aligned_baselines = baseline_decisions[:len(model_decisions)]
                try:
                    accuracy = compute_baseline_accuracy(model_decisions, aligned_baselines)
                    matches = compare_with_baseline(model_decisions, aligned_baselines)
                    print(f"  Baseline Accuracy: {accuracy:.2%} ({sum(matches)}/{len(matches)})")
                except Exception as e:
                    print(f"  Baseline comparison failed: {e}")

        print(f"{'='*50}\n")

        return rewards

    return reward_fn
```

### Example 4: 激活配置文件

```yaml
# config/training_config.yaml

# ============== Reward配置 ==============
reward:
  # Reward函数链权重
  chain:
    format_weight: 1.0
    tsc_weight: 1.0

  # Format Reward参数
  format:
    strict: 1.0
    partial: -0.5
    invalid: -10.0
    extract_regex: '\{["\s]*extend["\s]*:\s*["\s]*(yes|no)["\s]*(?:,|\})'

  # TSC Reward参数
  tsc:
    reward_scale: 10.0

  # Max Pressure配置（激活）
  max_pressure:
    enabled: true  # 新增：启用baseline追踪
    min_green_offset: 0.0
    max_green_override: false
    pressure_threshold: 0.0
```

```python
# grpo/config.py - 扩展GRPOTrainingConfig

@dataclass
class GRPOTrainingConfig:
    """GRPO训练配置"""

    # ... 现有字段 ...

    # 新增: baseline配置
    enable_baseline: bool = field(default=False)
    baseline_config: MaxPressureConfig = field(default_factory=MaxPressureConfig)

    @classmethod
    def from_yaml(cls, path: str) -> "GRPOTrainingConfig":
        """从YAML文件加载配置"""
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        # 处理嵌套配置
        reward_data = data.pop('reward', {})
        format_data = reward_data.pop('format', {})
        tsc_data = reward_data.pop('tsc', {})
        max_pressure_data = reward_data.pop('max_pressure', {})  # 新增

        # 新增: 提取baseline配置
        baseline_enabled = max_pressure_data.pop('enabled', False)
        baseline_config = MaxPressureConfig(**max_pressure_data)

        return cls(
            reward=RewardChainConfig(**reward_data),
            format_reward=FormatRewardConfig(**format_data),
            sumo=SUMOConfig(**sumo_data),
            enable_baseline=baseline_enabled,      # 新增
            baseline_config=baseline_config,       # 新增
            **data
        )
```

### Example 5: 训练脚本中启用baseline

```python
# grpo/training.py - 修改train_grpo函数

def train_grpo(
    config,
    model_path: str = None,
    dataset_path: str = None,
    output_dir: str = None,
    learning_rate: float = None,
    batch_size: int = None,
    num_epochs: int = None,
    max_steps: int = None,
):
    """执行GRPO训练"""

    # ... 现有参数覆盖逻辑 ...

    # 打印配置时添加baseline信息
    print("=" * 60)
    print("GRPO训练")
    print("=" * 60)
    print(f"模型路径: {config.model_path}")
    # ... 其他配置 ...
    print(f"Format权重: {config.format_weight}")
    print(f"TSC权重: {config.tsc_weight}")
    # 新增
    print(f"Baseline追踪: {'启用' if config.enable_baseline else '禁用'}")
    if config.enable_baseline:
        print(f"  - Min green offset: {config.baseline_config.min_green_offset}")
        print(f"  - Max green override: {config.baseline_config.max_green_override}")
        print(f"  - Pressure threshold: {config.baseline_config.pressure_threshold}")
    print("=" * 60)

    # ... 加载数据集 ...

    # 创建reward函数时传递baseline配置
    reward_fn = create_reward_function(
        chain_config=reward_chain_config,
        sumo_config=sumo_config,
        dataset=train_dataset,
        enable_baseline_tracking=config.enable_baseline,  # 新增
        mp_config=config.baseline_config                   # 新增
    )

    # ... 其余训练逻辑保持不变 ...
```

## State of the Art

### 当前系统状态

| 组件 | 状态 | 证据 |
|------|------|------|
| Max Pressure算法实现 | ✓ 已完成 | grpo/max_pressure.py (350行)，29个测试通过 |
| Max Pressure配置定义 | ✓ 已完成 | MaxPressureConfig类在config.py中定义 |
| 配置文件字段 | ✓ 已预留 | training_config.yaml中reward.max_pressure.* |
| Baseline函数导出 | ✓ 已完成 | `grpo/__init__.py`导出5个函数 |
| Reward函数集成 | ✗ 未集成 | reward.py未导入max_pressure |
| 训练脚本集成 | ✗ 未集成 | training.py未导入max_pressure |
| 时间参数访问 | ⚠ 需要处理 | 在dataset中但不在prompt JSON中 |

### 数据流分析

**现有流程**:
```
GRPO Dataset (JSON)
  ├─ prompt (JSON字符串，不含时间参数)
  ├─ current_green_elapsed
  ├─ min_green
  ├─ max_green
  └─ state_file
    ↓
load_grpo_dataset() (training.py)
  ├─ 提取: prompt, id, scenario, junction_id, state_file
  └─ 丢弃: current_green_elapsed, min_green, max_green  ❌ 问题！
    ↓
create_reward_function()
  └─ 仅有: prompts, state_files
    ↓
batch_compute_reward()
  └─ 无法调用Max Pressure（缺少时间参数）
```

**修复后流程**:
```
GRPO Dataset (JSON)
  ├─ prompt (JSON字符串，不含时间参数)
  ├─ current_green_elapsed  ✓ 保留
  ├─ min_green              ✓ 保留
  ├─ max_green              ✓ 保留
  └─ state_file
    ↓
load_grpo_dataset() (training.py)
  ├─ 提取: prompt, id, scenario, junction_id, state_file
  ├─ 提取: current_green_elapsed, min_green, max_green  ✓ 修复
  └─ 返回完整的Dataset对象
    ↓
create_reward_function()
  ├─ 预加载时间参数到列表
  ├─ (可选) 预计算baseline决策
  └─ 返回reward_fn
    ↓
reward_fn()
  ├─ 调用batch_compute_reward()
  ├─ 传递时间参数
  └─ 计算baseline统计
    ↓
batch_compute_reward()
  ├─ 调用batch_max_pressure_decision()
  ├─ 比较模型决策与baseline
  └─ 返回reward + 统计信息
```

### 集成差距总结

| 差距类型 | 描述 | 影响 | 修复方案 |
|---------|------|------|----------|
| 数据加载差距 | `load_grpo_dataset()`未保留时间参数 | 无法调用Max Pressure | 扩展Dataset包含时间字段 |
| Reward层差距 | `compute_reward()`未集成baseline | 无法评估单样本一致性 | 添加baseline比较逻辑 |
| Training层差距 | `create_reward_function()`未追踪baseline | 无法监控训练进度 | 添加统计追踪逻辑 |
| 配置激活差距 | `reward.max_pressure.*`未读取 | 无法配置baseline行为 | 扩展配置类加载逻辑 |

## Open Questions

### Q1: 时间参数传递方式

**What we know**:
- Dataset中有`current_green_elapsed`, `min_green`, `max_green`字段
- Prompt JSON中不包含这些字段
- `load_grpo_dataset()`当前未提取这些字段

**What's unclear**:
- 是否应该修改`load_grpo_dataset()`返回的Dataset结构？
- 还是应该在training.py中单独处理时间参数？

**Recommendation**:
修改`load_grpo_dataset()`保留时间参数：
```python
grpo_data.append({
    "prompt": prompt,
    "id": item.get("id", ""),
    "scenario": item.get("scenario", ""),
    "junction_id": item.get("junction_id", ""),
    "state_file": item.get("state_file", ""),
    # 新增
    "current_green_elapsed": item.get("current_green_elapsed"),
    "min_green": item.get("min_green"),
    "max_green": item.get("max_green"),
})
```

### Q2: RewardStats是否需要扩展

**What we know**:
- `RewardStats`定义了统计信息字段
- 当前不包含baseline相关字段

**What's unclear**:
- 是否应该在`RewardStats`中添加`baseline_matches`字段？
- 还是应该通过其他方式（如返回dict）传递baseline统计？

**Recommendation**:
暂时不扩展`RewardStats`，通过info dict返回baseline信息：
```python
# compute_reward返回
return final_reward, {
    "format_reward": ...,
    "tsc_reward": ...,
    "baseline_info": {
        "baseline_decision": "yes",
        "model_decision": "yes",
        "matches_baseline": True
    }
}

# batch_compute_reward可以在stats中添加
# 或者通过额外的返回值
return rewards, stats, baseline_stats  # 新增返回值
```

### Q3: 错误处理策略

**What we know**:
- `batch_max_pressure_decision()`在错误时返回'no'（保守策略）
- 这可能导致baseline准确率偏低

**What's unclear**:
- 是否应该记录baseline计算失败的情况？
- 失败率多少时应该警告用户？

**Recommendation**:
在`create_reward_function()`中添加错误计数：
```python
baseline_errors = 0
for i, (prompt, green_elapsed, min_green, max_green) in enumerate(...):
    try:
        baseline = max_pressure_decision_from_prompt(...)
    except Exception as e:
        baseline_errors += 1

if baseline_errors > 0:
    print(f"Warning: {baseline_errors}/{len(prompts)} baseline decisions failed (returned 'no')")
```

## Sources

### Primary (HIGH confidence)

- **grpo/max_pressure.py** (350行) - Max Pressure算法完整实现
  - 5个关键函数：max_pressure_decision, max_pressure_decision_from_prompt, batch_max_pressure_decision, compare_with_baseline, compute_baseline_accuracy
  - MaxPressureConfig配置类
  - 29个单元测试全部通过

- **grpo/reward.py** (324行) - Reward计算函数
  - compute_reward() - 单样本reward计算
  - batch_compute_reward() - 批量reward计算
  - RewardStats统计信息
  - 与GRPOTrainer集成点

- **grpo/training.py** (464行) - GRPO训练脚本
  - create_reward_function() - reward函数创建器
  - train_grpo() - 主训练函数
  - load_grpo_dataset() - 数据集加载
  - 与TRL GRPOTrainer集成

- **grpo/config.py** (662行) - 配置系统
  - MaxPressureConfig类定义
  - GRPOTrainingConfig类
  - YAML配置加载逻辑

- **config/training_config.yaml** (114行) - 中央配置文件
  - reward.max_pressure.*字段已定义

- **.planning/v1-MILESTONE-AUDIT.md** (821行) - 审计报告
  - 集成差距分析
  - 推荐修复方案
  - 修复方案示例代码

### Secondary (MEDIUM confidence)

- **grpo/dataset_generator.py** (450+行) - 数据集生成器
  - GRPODataEntry数据类定义
  - _create_data_entry() - 创建数据条目
  - _save_dataset() - 保存数据集（使用asdict转换）
  - 确认时间参数保存在数据集中

- **grpo/prompt_builder.py** (108行) - Prompt构建器
  - build_extend_decision_prompt() - 构建prompt JSON
  - 确认prompt中不包含时间参数

- **tests/unit/test_max_pressure.py** (523行) - Max Pressure测试
  - 29个测试用例
  - 测试模式参考

### Tertiary (LOW confidence)

无 - 本Phase研究主要依赖源代码分析和审计报告，未使用WebSearch。

## Metadata

**Confidence breakdown**:
- Standard stack: **HIGH** - 基于实际代码审查，Max Pressure模块已完整实现
- Architecture: **HIGH** - 基于代码结构和审计报告的推荐方案
- Pitfalls: **HIGH** - 基于代码分析发现的关键问题（时间参数缺失、配置未激活）
- Integration points: **HIGH** - 明确的代码位置和修改策略

**Research date**: 2026-02-02
**Valid until**: 30天（2026-03-04）- 代码库稳定，除非有重大架构变更

**Next steps for planner**:
1. 决定时间参数传递方式（修改Dataset vs. 单独处理）
2. 决定RewardStats扩展策略（扩展类 vs. 额外返回值）
3. 规划5个Plan的具体任务和验收标准
4. 确定向后兼容性要求（是否需要支持旧版数据集？）
