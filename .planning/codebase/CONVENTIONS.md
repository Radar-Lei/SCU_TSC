# Coding Conventions

**Analysis Date:** 2026-02-03

## Naming Patterns

**Files:**
- Snake case is used for Python source files: `sumo_interface.py`, `reward.py`, `dataset_generator.py`.
- Upper case is used for planning documents: `STACK.md`, `ARCHITECTURE.md`.
- Jupyter notebooks use mixed case: `Qwen3_(4B)_GRPO.ipynb`.

**Functions:**
- Snake case is the standard for functions: `extract_decision()`, `format_reward_fn()`, `calculate_tsc_reward_single()`.
- Internal helper methods in classes use a leading underscore: `_parse_net_file()`, `_find_sumo_binary()`.

**Variables:**
- Snake case for local variables and parameters: `config_file`, `tl_id`, `green_lanes`.
- Constants are written in screaming snake case: `DEFAULT_CONFIG`, `SYSTEM_PROMPT`.

**Types:**
- PascalCase (UpperCamelCase) for classes: `SUMOInterface`, `PhaseInfo`, `GRPOConfig`, `RewardStats`.
- `dataclass` is heavily used for structured data types: `FormatResult`, `TSCResult`, `RewardChainConfig`.

## Code Style

**Formatting:**
- Python code follows PEP 8 standards generally.
- UTF-8 encoding is explicitly declared at the top of files: `# -*- coding: utf-8 -*-`.
- Indentation is 4 spaces.

**Linting:**
- Not strictly enforced by configuration files in the root, but the code shows consistent usage of type hints (`typing` module).

## Import Organization

**Order:**
1. Standard library imports (e.g., `os`, `sys`, `json`, `re`).
2. Third-party library imports (e.g., `yaml`, `traci`, `torch`).
3. Local module imports (e.g., `from .sumo_interface import ...`).

**Path Aliases:**
- No path aliases detected. Standard relative and absolute imports are used.

## Error Handling

**Patterns:**
- Extensive use of `try...except` blocks, especially around TraCI/SUMO operations and JSON parsing: `traci.exceptions.TraCIException`.
- Error messages are often printed to the console or returned within result objects: `TSCResult(success=False, error="...")`.
- Some critical failures lead to `sys.exit()` with an error message.

## Logging

**Framework:**
- Primarily uses `print()` for console logging.
- `wandb` (Weights & Biases) is integrated for training progress tracking.

**Patterns:**
- Verbose flags in classes control the amount of console output.
- Training loops log metrics like loss, reward, and accuracy at regular intervals (defined by `logging_steps`).

## Comments

**When to Comment:**
- Docstrings are used for almost all functions and classes to describe purpose, arguments, and return values.
- Inline comments are used to explain complex logic or configuration steps (e.g., setting up `SUMO_HOME`).

**JSDoc/TSDoc:**
- Uses Python's standard docstring format (often Google-style or similar):
  ```python
  """
  Brief description.

  Args:
      arg1: description

  Returns:
      description
  """
  ```

## Function Design

**Size:**
- Functions are generally modular and focused on a single responsibility.
- Large operations (like reward calculation) are split into `single` and `batch` versions.

**Parameters:**
- Uses a mix of positional and keyword arguments.
- Heavy use of type hints for clarity.
- Configuration objects are often passed as a single `config` parameter.

**Return Values:**
- Frequently returns `dataclass` instances or `Tuples` for complex results.
- Boolean return values are common for success/failure status.

## Module Design

**Exports:**
- Modules expose classes and functions for external use.
- `__init__.py` files are present in packages (like `grpo/`) to facilitate imports.

**Barrel Files:**
- `grpo/__init__.py` is used but seems to have minimal logic beyond package declaration.

---

*Convention analysis: 2026-02-03*
