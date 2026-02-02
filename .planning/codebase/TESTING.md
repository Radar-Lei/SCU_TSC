# Testing Patterns

**Analysis Date:** 2026-02-03

## Test Framework

**Runner:**
- Primarily uses manual test scripts executed via `python3`.
- `pytest` or `unittest` configuration files are not explicitly present in the root, but the codebase contains scripts like `test_stratified_split.py`.

**Assertion Library:**
- Uses standard Python `assert` statements or manual checks with `if` conditions and `print` statements.

**Run Commands:**
```bash
python3 test_stratified_split.py    # Run specific dataset split validation
```

## Test File Organization

**Location:**
- Test scripts are located in the root directory: `test_stratified_split.py`.
- No dedicated `tests/` directory was found.

**Naming:**
- Prefix `test_` is used for test scripts and functions: `test_stratified_split.py`, `def test_stratified_split()`.

**Structure:**
```
[project-root]/
└── test_stratified_split.py
```

## Test Structure

**Suite Organization:**
```python
def test_stratified_split():
    """测试分层抽样效果"""
    # 1. Setup / Load Data
    dataset_path = "..."
    train_dataset, eval_dataset = load_sft_dataset(dataset_path, ...)

    # 2. Assertions / Checks
    if eval_dataset is None:
        print("❌ 验证集为空，测试失败")
        return False

    # 3. Reporting
    print("场景分布统计")
    # ... logic to compare distributions ...
    if success:
        print("✅ 修复成功！")
        return True
```

**Patterns:**
- **Setup pattern:** Usually involves loading a JSON dataset or initializing a configuration.
- **Teardown pattern:** Not explicitly used in existing scripts; relies on Python's garbage collection.
- **Assertion pattern:** Manual checks followed by status messages (✅/❌/⚠️).

## Mocking

**Framework:**
- No formal mocking framework (like `unittest.mock`) was observed in the checked files.

**Patterns:**
- The codebase uses a "Parallel Runner" and "Interface" pattern which could facilitate mocking, but current tests appear to run against real or sampled data.

**What to Mock:**
- SUMO simulation (`traci`) is a prime candidate for mocking in future unit tests to avoid dependency on the SUMO installation.

**What NOT to Mock:**
- Data processing logic (like `load_sft_dataset`) is tested directly.

## Fixtures and Factories

**Test Data:**
- Relies on existing data files in `data/sft_datasets/` or `data/grpo_datasets/`.
- `sampling` logic is used to create subsets for evaluation.

**Location:**
- Data files live in `data/`.

## Coverage

**Requirements:**
- None enforced.

**View Coverage:**
- No coverage tool configured.

## Test Types

**Unit Tests:**
- Minimal. Logic is mostly integrated.

**Integration Tests:**
- The `test_stratified_split.py` script acts as an integration test for the dataset loading and splitting logic.

**E2E Tests:**
- Not used. Training runs (via notebooks or scripts) serve as the primary validation for the full pipeline.

## Common Patterns

**Async Testing:**
- Not applicable. The codebase uses synchronous calls and multi-processing for concurrency.

**Error Testing:**
- Validates failure modes (e.g., "验证集为空，测试失败") within the test scripts.

---

*Testing analysis: 2026-02-03*
