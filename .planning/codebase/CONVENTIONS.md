# Coding Conventions

**Analysis Date:** 2025-02-03

## File Naming

**Python Files:**
- Use `snake_case` for module names: `config.py`, `sumo_interface.py`, `dataset_generator.py`
- Test files prefixed with `test_`: `test_stratified_split.py`
- Private modules use leading underscore for internal-only: `__init__.py` exports public API only

**Configuration Files:**
- YAML configs use `snake_case`: `training_config.yaml`
- JSON datasets use `snake_case`: `grpo_dataset.json`, `sft_dataset.json`

**Data Files:**
- State files use pattern: `state_{tl_id}_{time}_{count}.xml`
- Checkpoint files use pattern: `temp_grpo_checkpoint_{tl_id}_{time}.xml`

## Code Style

**Formatting:**
- No explicit formatting tool configured (no `.prettierrc`, `black.toml`, or `ruff.toml`)
- Use 4-space indentation for Python (standard PEP 8)
- Line length appears to be around 100-120 characters based on code review

**Linting:**
- No explicit linting configuration (no `.eslintrc`, `pylintrc`, or `ruff.toml`)

**Type Hints:**
- Type hints used consistently in function signatures
- Use `typing` module for complex types: `List`, `Dict`, `Optional`, `Tuple`, `Any`
- `TYPE_CHECKING` pattern used to avoid circular imports:
  ```python
  from typing import TYPE_CHECKING
  if TYPE_CHECKING:
      from grpo.max_pressure import MaxPressureConfig
  ```

## Import Organization

**Order (observed in `/home/samuel/SCU_TSC/grpo/config.py`, `/home/samuel/SCU_TSC/sumo_simulation/sumo_simulator.py`):**

1. Standard library imports
2. Third-party imports
3. Local application imports (with `from .` for relative imports within packages)
4. TYPE_CHECKING imports for type hints only

**Example from `/home/samuel/SCU_TSC/grpo/config.py`:**
```python
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
from pathlib import Path
import os
import yaml
import warnings

if TYPE_CHECKING:
    from grpo.max_pressure import MaxPressureConfig

# Actual import for runtime use
from grpo.max_pressure import MaxPressureConfig
```

**Path Aliases:**
- No explicit path aliases configured
- Uses `sys.path.insert(0, ...)` pattern for module imports in scripts
- Project root added to path in standalone scripts

## Naming Patterns

**Functions:**
- Use `snake_case` for function names: `load_grpo_dataset()`, `compute_reward()`, `batch_format_reward()`
- Private methods use single underscore prefix: `_is_decision_point()`, `_parse_net_file()`
- Factory functions use `create_` prefix: `create_reward_function()`

**Variables:**
- Use `snake_case`: `green_elapsed`, `min_green`, `max_green`, `phase_order`
- Constants use `UPPER_SNAKE_CASE`: `SYSTEM_PROMPT`, `DEFAULT_CONFIG`

**Classes:**
- Use `PascalCase`: `SUMOInterface`, `GRPODatasetGenerator`, `MaxPressureConfig`, `RewardStats`
- Abstract classes or interfaces not explicitly marked (no ABC usage detected)

**Dataclasses:**
- Heavily used for configuration and data structures
- Use `@dataclass` decorator with type hints
- Example from `/home/samuel/SCU_TSC/grpo/config.py`:
  ```python
  @dataclass
  class GRPOTrainingConfig:
      model_path: str
      max_seq_length: int = 2048
      learning_rate: float = 1.0e-5
      batch_size: int = 2
  ```

## Error Handling

**Patterns:**

**1. Exception catching with specific types:**
```python
# From sumo_interface.py
except TraCIException:
    return False

# From reward.py
except (ValueError, KeyError, json.JSONDecodeError) as e:
    baseline_info = {"baseline_error": str(e)}
```

**2. Try-finally for resource cleanup:**
```python
# From sumo_interface.py
try:
    if self.connected:
        traci.close()
except Exception:
    pass
finally:
    self.connected = False
```

**3. Return error objects instead of raising (dataclass pattern):**
```python
# From sumo_reward.py
@dataclass
class TSCResult:
    reward: float
    success: bool
    error: Optional[str] = None
```

**4. Value validation in `__post_init__`:**
```python
# From config.py
def __post_init__(self):
    if self.learning_rate <= 0:
        raise ValueError(f"grpo.learning_rate必须大于0，当前值: {self.learning_rate}")
```

**5. Warning for non-critical issues:**
```python
# From config.py
if self.enable_baseline and self.baseline_config is None:
    warnings.warn(
        "enable_baseline=True但baseline_config为None，baseline功能可能无法正常工作",
        UserWarning
    )
```

## Logging

**Framework:** Print statements (no structured logging library like `logging` module)

**Patterns:**

**1. Progress logging with prefixes:**
```python
# From dataset_generator.py
print(f"[{scenario_name}] 开始生成GRPO数据集...")
print(f"[{scenario_name}] 配置文件: {sumocfg}")
print(f"[{scenario_name}] 生成完成，共 {len(data_entries)} 条数据")
```

**2. Section separators for clarity:**
```python
# From training.py
print("=" * 60)
print("GRPO训练")
print("=" * 60)
```

**3. Conditional logging with verbose flag:**
```python
# From sumo_interface.py
if self.verbose:
    print(f"启动SUMO，端口: {actual_port} (尝试 {attempt+1}/{max_retries})")
```

**4. Debug logging (can be disabled):**
```python
# From training.py
print(f"[DEBUG] completions type: {type(completions)}")
print(f"[DEBUG] outputs[0]: {outputs[0][:200] if len(outputs[0]) > 200 else outputs[0]}")
```

**5. Statistics summary:**
```python
# From reward.py (batch_compute_reward)
print(f"\n{'='*50}")
print(f"Reward Statistics:")
print(f"  Total: {stats.total_count}")
print(f"  Format accuracy: {stats.format_accuracy:.1%}")
print(f"{'='*50}\n")
```

## Comments

**When to Comment:**

**1. Module-level docstrings (UTF-8 encoding declared):**
```python
# -*- coding: utf-8 -*-
"""
GRPO训练脚本

使用unsloth和TRL的GRPOTrainer对SFT模型进行强化学习微调，
训练模型优化交通信号控制决策。
"""
```

**2. Complex algorithm explanations:**
```python
# From max_pressure.py
"""
决策逻辑：
1. 时间约束检查：
   - 如果 green_elapsed < min_green: 必须返回 'yes'（不能提前切换）
   - 如果 green_elapsed >= max_green: 必须返回 'no'（不能超时延长）

2. Max Pressure决策：
   - 计算当前相位的压力：current_pressure = phase_queues[current_phase_id]
   - 找出其他相位的最大压力：max_other_pressure
   - 如果 current_pressure >= max_other_pressure + pressure_threshold: 返回 'yes'
   - 否则返回 'no'
"""
```

**3. Inline comments for non-obvious logic:**
```python
# From dataset_generator.py
# 使用 replace 而不是 format，因为模板中包含其他花括号（如 {"extend": "yes/no"}）
full_system_prompt = SYSTEM_PROMPT.replace("{extend_decision_input_json}", raw_prompt)

# 处理浮点数比较的容差
tolerance = 0.5
if abs(green_elapsed - min_green) < tolerance:
    return True
```

**4. TODO/FIXME tracking:**
- No TODO/FIXME comments found in the codebase (grepped for them)

## JSDoc/TSDoc

**Usage Pattern:** Python docstrings (Google style not strictly enforced)

**Function docstrings:**
```python
def load_grpo_dataset(dataset_path: str):
    """
    加载GRPO数据集

    Args:
        dataset_path: 数据集路径，可以是：
                     - 单个JSON文件
                     - 目录（自动扫描所有grpo_dataset.json）

    Returns:
        dataset: HuggingFace Dataset对象，格式为TRL GRPOTrainer期望的格式
    """
```

**Class docstrings:**
```python
class SUMOInterface:
    """SUMO仿真接口"""
```

**Dataclass docstrings:**
```python
@dataclass
class FormatResult:
    """格式验证结果"""
    reward: float
    is_strict: bool
    is_partial: bool
    extracted_decision: Optional[str]  # "yes", "no", or None
```

## Function Design

**Size:** Functions tend to be medium to large (50-200 lines common)

**Parameters:**
- Use type hints for all parameters
- Default values for optional parameters
- Configuration objects for multiple related parameters
- Example from `/home/samuel/SCU_TSC/grpo/config.py`:
  ```python
  def __post_init__(self):
      # Parameter validation
      if self.learning_rate <= 0:
          raise ValueError(f"grpo.learning_rate必须大于0，当前值: {self.learning_rate}")
  ```

**Return Values:**
- Single values: direct return
- Multiple values: tuple return `(final_reward, info_dict)`
- Error cases: return error objects or None
- Example from `/home/samuel/SCU_TSC/grpo/reward.py`:
  ```python
  def compute_reward(...) -> Tuple[float, Dict[str, Any]]:
      """Returns (final_reward, info_dict)"""
      # ... computation ...
      return final_reward, info_dict
  ```

## Module Design

**Exports:** Explicit `__all__` not commonly used

**Barrel Files:** `/home/samuel/SCU_TSC/grpo/__init__.py` exists but appears minimal

**Package Structure:**
```
grpo/
├── __init__.py              # Public API exports
├── config.py                # Configuration classes
├── training.py              # GRPO training entry point
├── sft_training.py          # SFT training entry point
├── reward.py                # Reward functions
├── sumo_reward.py           # SUMO-based reward calculation
├── sumo_interface.py        # SUMO simulation wrapper
├── dataset_generator.py     # GRPO dataset generation
├── prompt_builder.py        # Prompt construction
├── max_pressure.py          # Max Pressure baseline algorithm
└── validate_data.py         # Data validation utilities
```

**Import Patterns:**
- Relative imports within package: `from .reward import compute_reward`
- Absolute imports for external packages: `from datasets import Dataset`
- Type-only imports using `TYPE_CHECKING` to avoid circular dependencies

## Configuration Management

**Central Configuration:** `/home/samuel/SCU_TSC/config/training_config.yaml`

**Pattern:**
1. YAML file contains all hyperparameters
2. Python dataclasses map to YAML sections
3. `@dataclass` with `__post_init__` for validation
4. Helper functions like `load_training_config()` for loading

**Example from `/home/samuel/SCU_TSC/grpo/config.py`:**
```python
@dataclass
class TrainingConfig:
    training: Dict[str, Any]
    simulation: Dict[str, Any]
    reward: RewardSectionConfig
    paths: PathsConfig
    logging: LoggingConfig

    @classmethod
    def from_yaml(cls, path: str) -> "TrainingConfig":
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        # ... parse sections ...
        return cls(...)
```

## String Formatting

**F-strings preferred:**
```python
print(f"[{scenario_name}] 生成完成，共 {len(data_entries)} 条数据")
```

**Multi-line strings for templates:**
```python
SYSTEM_PROMPT = """你是交通信号控制优化专家。

你将收到一个路口在当前时刻的相位排队信息，需要判断是否延长"当前绿灯相位"。
"""
```

**Concatenation for building complex strings:**
```python
full_system_prompt = SYSTEM_PROMPT.replace("{extend_decision_input_json}", raw_prompt)
```

## Concurrency

**Multiprocessing for parallel SUMO simulations:**
```python
# From sumo_reward.py
from multiprocessing import Pool

with Pool(processes=self.max_workers) as pool:
    results = pool.starmap(
        calculate_tsc_reward_worker,
        [(p, o, s, config_dict) for p, o, s in tasks]
    )
```

**Thread for background simulation:**
```python
# From sumo_simulator.py
from threading import Thread, Event

_simulation_thread = Thread(target=run_simulation, daemon=True)
_simulation_thread.start()
```

## Resource Management

**Context managers not heavily used; prefer explicit cleanup:**
```python
# From sumo_interface.py
def close(self):
    try:
        if self.connected:
            traci.close()
    except Exception:
        pass
    finally:
        self.connected = False
```

**File operations with explicit encoding:**
```python
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

## Constants

**Module-level constants:**
```python
# From config.py
SYSTEM_PROMPT = """..."""  # Template string

DEFAULT_CONFIG = GRPOConfig()  # Default instance
```

**Hardcoded values in classes:**
```python
# From dataset_generator.py
step_count = 0
max_steps = 1000000  # Safety limit
```

---

*Convention analysis: 2025-02-03*
