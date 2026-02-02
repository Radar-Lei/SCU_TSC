# Testing Patterns

**Analysis Date:** 2025-02-03

## Test Framework

**Runner:**
- No formal test framework configured (no pytest, unittest, or vitest config detected)
- Standalone test scripts run directly with Python
- Manual test execution via `python test_script.py`

**Assertion Library:**
- Standard `assert` statements for simple checks
- Custom validation functions for complex assertions

**Run Commands:**
```bash
# Run standalone test script
python test_stratified_split.py

# Run SFT training with built-in format validation
python -m grpo.sft_training

# No global test command (no Makefile or test script)
```

## Test File Organization

**Location:**
- Test files at project root: `/home/samuel/SCU_TSC/test_stratified_split.py`
- No dedicated `tests/` directory

**Naming:**
- Test files prefixed with `test_`: `test_stratified_split.py`
- Test functions prefixed with `test_`: `def test_stratified_split():`

**Structure:**
```
/home/samuel/SCU_TSC/
├── test_stratified_split.py    # Data split validation test
├── grpo/
│   ├── sft_training.py          # Contains built-in format validation
│   ├── validate_data.py         # Data validation utilities
│   └── training.py              # Training with debug prints
└── config/
    └── read_config.py           # Config reading utility (not a test)
```

## Test Structure

**Suite Organization:**

From `/home/samuel/SCU_TSC/test_stratified_split.py`:
```python
def test_stratified_split():
    """测试分层抽样效果"""

    print("=" * 60)
    print("测试分层抽样数据划分")
    print("=" * 60)

    # Arrange: Load dataset
    dataset_path = "/home/samuel/SCU_TSC/data/sft_datasets/sft_dataset.json"
    train_dataset, eval_dataset = load_sft_dataset(
        dataset_path,
        eval_percent=0.05,
        eval_limit=100
    )

    # Act: Collect statistics
    train_scenarios = [item['scenario'] for item in train_dataset]
    eval_scenarios = [item['scenario'] for item in eval_dataset]

    # Assert: Validate results
    num_eval_scenarios = len(eval_counts)
    if num_eval_scenarios >= 3:
        print(f"✓ 验证集包含 {num_eval_scenarios} 个场景")

    max_ratio_diff = 0
    for scenario in all_scenarios:
        train_ratio = train_counts.get(scenario, 0) / len(train_dataset)
        eval_ratio = eval_counts.get(scenario, 0) / len(eval_dataset)
        ratio_diff = abs(train_ratio - eval_ratio)
        max_ratio_diff = max(max_ratio_diff, ratio_diff)

    if max_ratio_diff < 0.05:
        print(f"✓ 场景分布一致 (最大比例差异: {max_ratio_diff*100:.2f}%)")

    # Return boolean result
    return num_eval_scenarios >= 3 and max_ratio_diff < 0.05
```

**Patterns:**

1. **Setup pattern:** No explicit setup/teardown; resources created inline
2. **Teardown pattern:** Not used (no resource cleanup in tests)
3. **Assertion pattern:** Custom validation with print statements and boolean return

## Mocking

**Framework:** No mocking framework detected (no `unittest.mock`, `pytest.mock`, or `responses`)

**Patterns:**

**Manual stubbing for SUMO simulation:**
```python
# From sft_training.py - format validation section
# After training, validate with actual model inference
FastLanguageModel.for_inference(model)

test_samples = random.sample(raw_data, min(5, len(raw_data)))
format_regex = re.compile(r'\{\s*"extend"\s*:\s*"(yes|no)"\s*\}')

for i, sample in enumerate(test_samples):
    # Generate prediction
    outputs = model.generate(**inputs, max_new_tokens=50, temperature=0.1)
    generated = tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)

    # Check format
    match = format_regex.search(generated)
    is_correct = match is not None
```

**Configuration override for testing:**
```python
# From training.py - using SimpleNamespace for config
from types import SimpleNamespace
sumo_config = SimpleNamespace(
    max_workers=config.sumo.max_workers,
    extend_seconds=config.sumo.extend_seconds,
    reward_scale=config.sumo.reward_scale,
    port_range=config.sumo.port_range
)
```

**What to Mock:**
- SUMO simulation (TraCI connection) - typically bypassed with real SUMO in tests
- External APIs - none detected in this codebase

**What NOT to Mock:**
- Data processing functions (tested with real data)
- Configuration loading (uses real YAML files)
- Reward calculations (tested with actual SUMO simulations)

## Fixtures and Factories

**Test Data:**
No dedicated fixtures directory. Data comes from:

1. **Generated datasets:** `/home/samuel/SCU_TSC/data/grpo_datasets/`, `/home/samuel/SCU_TSC/data/sft_datasets/`
2. **SUMO state files:** Located in `states/` subdirectories of each scenario
3. **Real traffic scenarios:** Under `/home/samuel/SCU_TSC/sumo_simulation/environments/`

**Location:**
```
/home/samuel/SCU_TSC/
├── data/
│   ├── grpo_datasets/
│   │   ├── arterial4x4_90/
│   │   │   └── grpo_dataset.json
│   │   ├── arterial4x4_91/
│   │   │   └── grpo_dataset.json
│   │   └── ... (multiple scenarios)
│   └── sft_datasets/
│       └── sft_dataset.json
└── sumo_simulation/
    └── environments/
        ├── arterial4x4_90/
        │   ├── arterial4x4_90.sumocfg
        │   └── states/          # SUMO checkpoint files
        └── ...
```

**Data generation:**
From `/home/samuel/SCU_TSC/grpo/generate_grpo_dataset.py` (inferred from config):
```python
# Data is generated by running SUMO simulations
generator = GRPODatasetGenerator(config)
entries = generator.generate_for_scenario(
    scenario_name="arterial4x4_90",
    output_dir=output_dir,
    port=port
)
```

## Coverage

**Requirements:** None enforced (no coverage tool configured)

**View Coverage:**
```bash
# No coverage command available
# No .coveragerc or pyproject.toml with coverage settings
```

**Coverage status:** Unknown - no coverage measurement in place

## Test Types

**Unit Tests:**
- Limited use; most tests are integration tests
- Example: Configuration value validation in `__post_init__` methods
- No formal unit test framework

**Integration Tests:**
- Primary test type in this codebase
- SUMO simulation tests require full SUMO installation
- Training pipeline tests use actual models
- From `/home/samuel/SCU_TSC/test_stratified_split.py`:
  ```python
  # Tests data loading and stratified split
  train_dataset, eval_dataset = load_sft_dataset(
      dataset_path,
      eval_percent=0.05,
      eval_limit=100
  )
  ```

**E2E Tests:**
- Not explicitly implemented
- Manual testing through running full training pipeline
- SFT training includes built-in format validation that acts as E2E test:
  ```python
  # From sft_training.py - validates model learned format correctly
  accuracy = correct_count / len(test_samples) * 100
  if accuracy >= 80:
      print("✓ SFT成功：模型已学会正确的JSON格式！")
  ```

## Common Patterns

**Async Testing:**
Not applicable - codebase is synchronous (no async/await)

**Error Testing:**
```python
# From config.py - ValueError raised for invalid config
def __post_init__(self):
    if self.learning_rate <= 0:
        raise ValueError(f"grpo.learning_rate必须大于0，当前值: {self.learning_rate}")

# From test_stratified_split.py - explicit validation
if num_eval_scenarios >= 3 and max_ratio_diff < 0.05:
    print("✅ 修复成功！数据划分合理")
    return True
else:
    print("⚠️  修复部分成功，建议进一步调整")
    return False
```

**Data Validation Testing:**
From `/home/samuel/SCU_TSC/grpo/validate_data.py` (inferred):
```python
# Pattern: Validate dataset structure before training
# - Check required fields exist
# - Validate data types
# - Check for empty or null values
```

**Format Validation Testing:**
From `/home/samuel/SCU_TSC/grpo/sft_training.py` (lines 342-419):
```python
# Built-in format validation after SFT training
print("\n" + "=" * 60)
print("SFT格式验证")
print("=" * 60)

FastLanguageModel.for_inference(model)

# Load test samples
test_samples = random.sample(raw_data, min(5, len(raw_data)))

format_regex = re.compile(r'\{\s*"extend"\s*:\s*"(yes|no)"\s*\}')

correct_count = 0
for i, sample in enumerate(test_samples):
    # Generate output
    outputs = model.generate(**inputs, max_new_tokens=50, temperature=0.1)

    # Check format compliance
    match = format_regex.search(generated)
    is_correct = match is not None

    if is_correct:
        correct_count += 1

# Report results
accuracy = correct_count / len(test_samples) * 100
print(f"格式验证结果: {correct_count}/{len(test_samples)} ({accuracy:.1f}%)")
```

**Reward Function Testing:**
From `/home/samuel/SCU_TSC/grpo/reward.py`:
```python
# Format reward validation with regex
def format_reward_fn(output: str, ...) -> FormatResult:
    # Step 1: Try strict JSON parsing
    try:
        parsed = json.loads(output.strip())
        if isinstance(parsed, dict) and len(parsed) == 1 and "extend" in parsed:
            if isinstance(parsed["extend"], str) and parsed["extend"].lower() in ["yes", "no"]:
                return FormatResult(reward=strict_reward, is_strict=True, ...)

    # Step 2: Fall back to regex extraction
    decision = extract_decision(output, regex)
    if decision:
        return FormatResult(reward=partial_reward, is_partial=True, ...)

    # Step 3: Invalid format
    return FormatResult(reward=invalid_reward, is_strict=False, is_partial=False, ...)
```

## Debug Testing

**Debug prints in training:**
From `/home/samuel/SCU_TSC/grpo/training.py`:
```python
# Debug output for reward function inspection
if len(completions) > 0:
    print(f"\n[DEBUG] completions type: {type(completions)}")
    print(f"[DEBUG] completions length: {len(completions)}")
    print(f"[DEBUG] completions[0] type: {type(completions[0])}")
    print(f"[DEBUG] completions[0] value: {completions[0][:200] if isinstance(completions[0], str) else completions[0]}")
```

**Statistics output:**
From `/home/samuel/SCU_TSC/grpo/reward.py` (batch_compute_reward):
```python
# Print reward statistics during training
print(f"\n{'='*50}")
print(f"Reward Statistics:")
print(f"  Total: {stats.total_count}")
print(f"  Format accuracy: {stats.format_accuracy:.1%}")
print(f"  Strict: {stats.strict_format_count}, Partial: {stats.partial_format_count}")
print(f"  Invalid: {stats.invalid_format_count}")
print(f"  Avg format reward: {stats.avg_format_reward:.3f}")
print(f"  Avg TSC reward: {stats.avg_tsc_reward:.3f}")
print(f"  Avg final reward: {stats.avg_final_reward:.3f}")
print(f"{'='*50}\n")
```

## Manual Testing

**SUMO Simulation Testing:**
```bash
# From sumo_simulator.py - manual testing via CLI
python sumo_simulator.py --env arterial4x4_90 --tl-id cluster_123

# List available environments
python sumo_simulator.py --list-envs

# List traffic lights for a scenario
python sumo_simulator.py --list-tls arterial4x4_90

# GRPO training data generation
python sumo_simulator.py --grpo --tl-id cluster_123
```

**Config Reading:**
```bash
# From config/read_config.py
python config/read_config.py --key simulation.sumo.max_workers
python config/read_config.py --key training.grpo.batch_size --output json
```

## Test Data Generation

**GRPO Dataset Generation:**
From `/home/samuel/SCU_TSC/grpo/generate_grpo_dataset.py` (inferred):
```python
# Generates GRPO training data by running SUMO simulations
# Each scenario produces grpo_dataset.json with state file references

# Process:
# 1. Start SUMO with scenario config
# 2. Run simulation until decision points
# 3. Save state file at each decision point
# 4. Record prompt, state_file, and metadata
# 5. Output to grpo_dataset.json
```

**SFT Dataset Generation:**
```python
# From grpo/generate_sft_dataset.py (inferred)
# Generates SFT training data with expert decisions
# Format: {"messages": [...], "response": {"extend": "yes/no"}}
```

## Validation Patterns

**Stratified Sampling Validation:**
From `/home/samuel/SCU_TSC/grpo/sft_training.py`:
```python
from sklearn.model_selection import train_test_split

# Stratified split by scenario
train_indices, eval_indices = train_test_split(
    indices,
    test_size=eval_count,
    stratify=scenarios,  # Ensures proportional scenario distribution
    random_state=3407
)
```

**Data Validation:**
```python
# From validate_data.py (inferred)
# - Check dataset completeness
# - Validate JSON structure
# - Ensure state files exist
# - Verify phase data integrity
```

## Baseline Comparison Testing

From `/home/samuel/SCU_TSC/grpo/max_pressure.py`:
```python
def compare_with_baseline(
    model_decisions: List[str],
    baseline_decisions: List[str]
) -> List[bool]:
    """
    比较模型决策与baseline决策

    评估模型与Max Pressure baseline的一致性。
    """
    if len(model_decisions) != len(baseline_decisions):
        raise ValueError(
            f"决策列表长度不一致: "
            f"model={len(model_decisions)}, baseline={len(baseline_decisions)}"
        )

    matches = [
        m.lower() == b.lower()
        for m, b in zip(model_decisions, baseline_decisions)
    ]

    return matches
```

## Training Validation

**Post-Training Evaluation:**
From `/home/samuel/SCU_TSC/grpo/sft_training.py`:
```python
# After training, validate model output format
accuracy = correct_count / len(test_samples) * 100

if accuracy >= 80:
    print("✓ SFT成功：模型已学会正确的JSON格式！")
elif accuracy >= 50:
    print("△ SFT部分成功：模型正在学习格式，可能需要更多训练")
else:
    print("✗ SFT失败：模型未能学会格式，请检查训练配置")
```

---

*Testing analysis: 2025-02-03*
