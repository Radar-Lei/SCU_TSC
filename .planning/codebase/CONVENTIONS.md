# Coding Conventions

**Analysis Date:** 2025-02-02

## File Encoding

**All Python files use:**
- UTF-8 encoding
- Explicit encoding declaration on first line: `# -*- coding: utf-8 -*-`
- Shebang for executable scripts: `#!/usr/bin/env python3`

**Example:**
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module docstring
"""
```

## Naming Patterns

**Files:**
- **Modules**: `snake_case.py` (e.g., `sumo_interface.py`, `dataset_generator.py`)
- **Executable scripts**: `snake_case.py` with shebang (e.g., `convert_to_gguf.py`)
- **Test files**: `test_generator.py` (not using `test_` prefix convention)
- **Private modules**: No leading underscore convention used

**Functions:**
- **Public**: `snake_case` (e.g., `load_sft_dataset`, `build_extend_decision_prompt`)
- **Private**: `_leading_underscore` (e.g., `_local_tag`, `_parse_float`)
- **Internal helpers**: `_private` (e.g., `_find_sumocfg`, `_get_randomized_green_times`)

**Classes:**
- **PascalCase** (e.g., `GRPODatasetGenerator`, `SUMOInterface`, `ParallelRunner`)
- **Dataclasses**: `PascalCase` (e.g., `PhaseInfo`, `GRPODataEntry`, `TemplateVehicle`)

**Constants:**
- **UPPER_CASE** (e.g., `SYSTEM_PROMPT`, `DEFAULT_CONFIG`)
- **Module-level**: Usually dataclass instances (e.g., `DEFAULT_CONFIG = GRPOConfig()`)

**Variables:**
- **Local**: `snake_case` (e.g., `scenario_name`, `output_dir`, `warmup_steps`)
- **Type hints present**: Most functions use `typing` module

## Code Style

**Indentation:**
- 4 spaces (no tabs detected)

**Line length:**
- Not strictly enforced, but generally under 100 characters
- Some longer lines for function signatures with type hints

**Imports:**
1. Standard library first
2. Third-party imports second
3. Local imports third (using `from .module import ...` for relative imports)

**Example from `/home/samuel/SCU_TSC/grpo/dataset_generator.py`:**
```python
import os
import json
import random
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime

from .config import GRPOConfig, SYSTEM_PROMPT
from .sumo_interface import SUMOInterface, PhaseInfo
from .prompt_builder import build_extend_decision_prompt
```

**Type hints:**
- Extensive use of `typing` module (`Optional`, `List`, `Dict`, `Tuple`, `Any`)
- Return types always specified
- Parameter types specified in most functions

**Docstrings:**
- **Google-style** docstrings with triple quotes
- **Module docstrings**: Present in all files
- **Function docstrings**: Consistent format with `Args:`, `Returns:` sections

**Example from `/home/samuel/SCU_TSC/grpo/sumo_interface.py`:**
```python
def get_valid_phases(self, tl_id: str, config: Any = None) -> List[PhaseInfo]:
    """
    获取信号灯的有效相位列表（只包含有绿灯的相位）

    Args:
        tl_id: 信号灯ID
        config: GRPOConfig配置对象，用于获取默认min/max green

    Returns:
        有效相位列表
    """
```

## Import Organization

**Order:**
1. Standard library (`os`, `sys`, `json`, `random`, `argparse`)
2. Third-party libraries (`from typing import ...`, `from dataclasses import ...`)
3. Local relative imports (`from .config import ...`)

**Path management:**
- **Scripts use path manipulation for module imports**:
```python
# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

**Relative imports within packages:**
- Use `from .module import name` (dot notation for sibling modules)
- Example: `from .config import GRPOConfig, SYSTEM_PROMPT`

## Error Handling

**Patterns:**

**Try-except with specific exceptions:**
```python
# From /home/samuel/SCU_TSC/grpo/sumo_interface.py
try:
    import traci
    from traci.exceptions import TraCIException
except ImportError:
    sys.exit("错误: 无法导入 traci。请检查 SUMO 是否安装或运行 'pip install traci'")
```

**Return None on error (no exception propagation):**
```python
def _find_sumocfg(self, scenario_dir: str) -> Optional[str]:
    try:
        tree = ET.parse(scenario_dir)
        # ... processing
    except Exception as e:
        if self.verbose:
            print(f"解析配置文件失败: {e}")
    return None
```

**Return empty list on failure:**
```python
def get_traffic_lights(self) -> List[str]:
    try:
        return list(traci.trafficlight.getIDList())
    except TraCIException:
        return []
```

**Error messages:**
- Chinese error messages used
- Context included in error messages (e.g., `[{scenario_name}]` prefix)
- `print()` used for error output, not `logging` module

**Validation:**
- Input validation at function entry (e.g., file existence checks)
- Use of `Optional` return types for error cases

## Logging

**Framework:** `print()` statements (no logging library)

**Patterns:**

**Progress indicators:**
```python
# From /home/samuel/SCU_TSC/grpo/dataset_generator.py
if step_count % 1000 == 0:
    print(f"[{scenario_name}] 步数: {step_count}, 时间: {sim_time:.0f}s, 数据: {len(data_entries)}条")
```

**Section separators:**
```python
print("=" * 60)
print("SFT训练")
print("=" * 60)
```

**Verbose flags:**
```python
if self.verbose:
    print(f"启动SUMO，端口: {port} (尝试 {attempt+1}/{max_retries})")
```

**No structured logging:**
- No log levels (DEBUG, INFO, WARNING, ERROR)
- No log file output
- All output to stdout/stderr

## Comments

**When to Comment:**

**Module-level documentation:**
- All modules have descriptive docstrings explaining purpose

**Function documentation:**
- All public functions have docstrings with Args/Returns

**Inline comments:**
- Used for explaining complex logic
- Used for noting workarounds

**Example from `/home/samuel/SCU_TSC/grpo/sumo_interface.py`:**
```python
# 检测相位是否切换
if tl_id in last_phase_indices:
    if current_sumo_phase != last_phase_indices[tl_id]:
        phase_start_times[tl_id] = sim_time
```

**Chinese comments:**
- Comments and docstrings in Chinese throughout codebase
- Variable names and function names in English

## JSDoc/TSDoc

**Not applicable** - Python codebase using Google-style docstrings

**Docstring format:**
```python
def function_name(param1: type, param2: type) -> return_type:
    """
    简短描述

    Args:
        param1: 参数1描述
        param2: 参数2描述

    Returns:
        返回值描述
    """
```

## Function Design

**Size:**
- No strict size limit enforced
- Functions typically 20-60 lines
- Some longer functions (e.g., `generate_for_scenario` ~60 lines)

**Parameters:**
- **Positional parameters** for required arguments
- **Keyword parameters with defaults** for optional arguments
- Extensive use of `Optional[T]` for nullable parameters
- Use of `*` to separate positional from keyword arguments in argparse

**Example from `/home/samuel/SCU_TSC/grpo/sft_training.py`:**
```python
def train_sft(
    model_name: str = "unsloth/Qwen2.5-0.5B-Instruct",
    dataset_path: str = "/home/samuel/SCU_TSC/data/sft_datasets/sft_dataset.json",
    output_dir: str = "/home/samuel/SCU_TSC/model/sft_model",
    max_seq_length: int = 2048,
    lora_rank: int = 32,
    num_epochs: int = 3,
    batch_size: int = 2,
    learning_rate: float = 2e-4,
    max_steps: Optional[int] = None,
    # ... more params
):
```

**Return Values:**
- Always typed return values
- Return `None` for void functions
- Return `Optional[T]` for functions that can fail
- Return tuples for multiple values

## Module Design

**Exports:**
- **`__all__`** defined in package `__init__.py`
- Example from `/home/samuel/SCU_TSC/grpo/__init__.py`:
```python
from .config import GRPOConfig, DEFAULT_CONFIG, SYSTEM_PROMPT

__all__ = ['GRPOConfig', 'DEFAULT_CONFIG', 'SYSTEM_PROMPT']
```

**Barrel Files:**
- `/home/samuel/SCU_TSC/grpo/__init__.py` exports main config items

**Module structure by functionality:**
- `config.py` - Configuration and constants
- `sumo_interface.py` - SUMO API wrapper
- `prompt_builder.py` - Prompt construction utilities
- `dataset_generator.py` - Core generation logic
- `parallel_runner.py` - Parallel execution
- `generate_grpo_dataset.py` - CLI entry point
- `sft_training.py` - Training logic
- `generate_sft_dataset.py` - SFT data generation

## Command-Line Interface

**argparse usage:**
- Consistent pattern across all CLI scripts
- `parse_args()` function returns parsed arguments
- `RawDescriptionHelpFormatter` for custom help text
- Mutually exclusive groups where appropriate

**Example from `/home/samuel/SCU_TSC/grpo/generate_grpo_dataset.py`:**
```python
def parse_args():
    parser = argparse.ArgumentParser(
        description="GRPO数据集生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--scenario", "-s", type=str, help="单个场景名称")
    group.add_argument("--scenarios", type=str, help="多个场景名称，逗号分隔")
    group.add_argument("--all", "-a", action="store_true", help="处理所有场景")
    return parser.parse_args()
```

## Configuration

**Dataclasses for config:**
- Use `@dataclass` for configuration objects
- Default values in dataclass fields
- `__post_init__` for validation/computation

**Example from `/home/samuel/SCU_TSC/grpo/config.py`:**
```python
@dataclass
class GRPOConfig:
    """GRPO数据集生成配置"""
    extend_seconds: int = 5
    warmup_steps: int = 300
    # ... more fields

    def __post_init__(self):
        os.makedirs(self.output_dir, exist_ok=True)
        if self.num_workers == 0:
            import multiprocessing
            self.num_workers = max(1, multiprocessing.cpu_count() - 1)
```

## String Formatting

**f-strings preferred:**
```python
print(f"[{scenario_name}] 步数: {step_count}, 时间: {sim_time:.0f}s")
```

**`.format()` for template strings:**
```python
SYSTEM_PROMPT = """...
【extend_decision_input_json】
{extend_decision_input_json}
【/extend_decision_input_json】
...
"""
```

**String concatenation with `+`:**
- Used for building file paths (alongside `os.path.join`)

## File I/O

**Encoding always specified:**
```python
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
```

**Context managers:** Always use `with` statements for file operations

**JSON handling:**
- `json.load()` for reading
- `json.dump()` with `ensure_ascii=False, indent=2` for writing
- `json.dumps()` for string conversion

## Path Handling

**Always convert to absolute paths:**
```python
self.config_file = os.path.abspath(config_file)
```

**Use `os.path` functions:**
- `os.path.join()` for path construction
- `os.path.dirname()`, `os.path.abspath()` for path manipulation
- `pathlib.Path` used in some modules (e.g., `/home/samuel/SCU_TSC/rou_month_generator.py`)

## Concurrency

**multiprocessing for parallel execution:**
```python
from multiprocessing import Pool

with Pool(processes=num_workers) as pool:
    all_entries = pool.map(run_single_scenario, tasks)
```

**Threading:**
- Used in `/home/samuel/SCU_TSC/sumo_simulation/sumo_simulator.py`

---

*Convention analysis: 2025-02-02*
