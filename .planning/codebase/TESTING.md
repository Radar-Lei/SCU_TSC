# Testing Patterns

**Analysis Date:** 2025-02-02

## Test Framework

**Runner:**
- No formal test framework (pytest, unittest, etc.) detected
- Manual testing via dedicated test scripts
- No test configuration files (pytest.ini, setup.cfg, tox.ini)

**Assertion Library:**
- Built-in `assert` statements only

**Run Commands:**
```bash
# Manual test execution
python -m grpo.test_generator --single arterial4x4_1
python -m grpo.test_generator --parallel 8

# No automated test runner
```

## Test File Organization

**Location:**
- Tests co-located with source code in `/home/samuel/SCU_TSC/grpo/`
- Test file: `test_generator.py`
- No separate `tests/` directory

**Naming:**
- Test files: `test_<module>.py` pattern (only one: `test_generator.py`)
- Not following strict `test_` prefix convention for all test code

**Structure:**
```
grpo/
├── __init__.py
├── config.py
├── dataset_generator.py
├── generate_grpo_dataset.py
├── generate_sft_dataset.py
├── parallel_runner.py
├── prompt_builder.py
├── sft_training.py
├── sumo_interface.py
└── test_generator.py          # Test file
```

## Test Structure

**Suite Organization:**
```python
# From /home/samuel/SCU_TSC/grpo/test_generator.py
def main():
    args = parse_args()

    print("=" * 60)
    print("GRPO数据生成器测试")
    print("=" * 60)

    # 基础测试（不需要SUMO）
    test_config()
    test_timestamp_generator()
    test_prompt_builder()

    # 完整测试（需要SUMO）
    try:
        if args.single:
            test_single_scenario(args.single, args.warmup_steps)
        else:
            test_parallel_all_scenarios(args.parallel, args.warmup_steps)
    except Exception as e:
        print(f"\n仿真测试失败: {e}")
        print("请确保SUMO已正确安装")
```

**Patterns:**

**1. Simple unit tests (no dependencies):**
```python
def test_config():
    """测试配置"""
    print("\n=== 测试配置 ===")

    config = GRPOConfig()
    print(f"默认决策秒数: {config.extend_seconds}")
    print(f"默认并行数: {config.num_workers}")
    print(f"场景目录: {config.scenarios_dir}")
    print(f"输出目录: {config.output_dir}")

    assert config.extend_seconds == 5
    print("✓ 配置加载正确")
```

**2. Function output validation:**
```python
def test_prompt_builder():
    """测试Prompt构建器"""
    print("\n=== 测试Prompt构建器 ===")

    prompt = build_extend_decision_prompt(
        crossing_id=1234,
        as_of="2025-01-01 08:30:00",
        phase_order=[0, 2, 4, 6],
        current_phase_id=2,
        phase_metrics={0: 3.5, 2: 1.2, 4: 5.8, 6: 0.0}
    )

    print("生成的Prompt:")
    print(prompt)

    # 验证JSON格式
    data = json.loads(prompt)
    assert data["crossing_id"] == 1234
    assert data["state"]["current_phase_id"] == 2
    print("✓ Prompt格式正确")
```

**3. Integration tests (with external dependencies):**
```python
def test_single_scenario(scenario_name: str, warmup_steps: int = 100):
    """测试单场景数据生成（实际运行SUMO）"""
    print(f"\n=== 测试单场景数据生成: {scenario_name} ===")

    config = GRPOConfig(
        warmup_steps=warmup_steps,
        use_gui=False,
        num_workers=1,
    )

    generator = GRPODatasetGenerator(config)

    # 检查场景是否存在
    scenario_dir = os.path.join(config.scenarios_dir, scenario_name)
    if not os.path.exists(scenario_dir):
        print(f"跳过：场景 {scenario_name} 不存在")
        return None

    # ... run actual SUMO simulation
    entries = generator.generate_for_scenario(
        scenario_name=scenario_name,
        output_dir=output_dir
    )

    if entries:
        print(f"✓ 生成了 {len(entries)} 条数据")
```

**Setup pattern:**
- Manual setup in each test function
- No `setUp()` / `tearDown()` methods
- Each test creates its own config/objects

**Teardown pattern:**
- Manual cleanup (e.g., `finally` blocks for SUMO connection)
- No automatic teardown

**Assertion pattern:**
- Simple `assert` statements
- Manual print statements for test status (`✓`, `✗` indicators)
- No assertion helpers or custom matchers

## Mocking

**Framework:** None (no mock library usage detected)

**Patterns:**
- No mocking used in tests
- Tests run against real SUMO simulator
- Tests require SUMO to be installed and configured
- No test doubles or fakes

**What to Mock:**
- Currently nothing is mocked
- SUMO interface could be mocked for unit tests (but not implemented)

**What NOT to Mock:**
- Not applicable - no mocking framework used

## Fixtures and Factories

**Test Data:**
- Hardcoded test values in test functions
- No external fixture files
- No factory functions

**Example:**
```python
def test_timestamp_generator():
    """测试时间戳生成"""
    print("\n=== 测试时间戳生成 ===")

    ts1 = generate_timestamp(0)
    print(f"仿真时间 0s: {ts1}")
    assert ts1 == "2025-01-01 00:00:00"

    ts2 = generate_timestamp(3661)  # 1小时1分1秒
    print(f"仿真时间 3661s: {ts2}")
    assert ts2 == "2025-01-01 01:01:01"

    print("✓ 时间戳生成正确")
```

**Location:**
- Test data embedded in test functions
- No separate fixtures directory

## Coverage

**Requirements:** None enforced

**View Coverage:**
```bash
# No coverage tool configured
# No coverage reporting available
```

**Coverage gaps:**
- Most code has no test coverage
- Only basic validation in `test_generator.py`
- No unit tests for individual functions
- No integration tests for data pipelines

## Test Types

**Unit Tests:**
- **Scope:** Very limited
- **Examples:**
  - `test_config()` - validates default config values
  - `test_timestamp_generator()` - tests time conversion
  - `test_prompt_builder()` - validates JSON output format
- **Approach:** Simple assertion-based validation

**Integration Tests:**
- **Scope:** Full SUMO simulation runs
- **Examples:**
  - `test_single_scenario()` - runs complete data generation for one scenario
  - `test_parallel_all_scenarios()` - runs parallel generation across all scenarios
- **Approach:** Execute actual SUMO simulations and validate output files exist

**E2E Tests:**
- **Framework:** Not used
- **No end-to-end tests** covering full pipeline from data generation to training

## Common Patterns

**Manual test orchestration:**
```python
def main():
    # Parse CLI args for test configuration
    args = parse_args()

    # Run basic tests
    test_config()
    test_timestamp_generator()
    test_prompt_builder()

    # Run integration tests (may fail if SUMO not installed)
    try:
        if args.single:
            test_single_scenario(args.single, args.warmup_steps)
        else:
            test_parallel_all_scenarios(args.parallel, args.warmup_steps)
    except Exception as e:
        print(f"\n仿真测试失败: {e}")
```

**Print-based test reporting:**
```python
print("\n=== 测试Prompt构建器 ===")
print("✓ Prompt格式正确")
print(f"✓ 生成了 {len(entries)} 条数据")
print("✗ 未生成任何数据")
```

**Exception handling in tests:**
```python
try:
    # Run test that may fail
    test_single_scenario(args.single, args.warmup_steps)
except Exception as e:
    print(f"\n仿真测试失败: {e}")
    print("请确保SUMO已正确安装")
```

## Validation Functions

**Custom validation in `/home/samuel/SCU_TSC/rou_month_generator.py`:**
```python
def validate_rou(
    *,
    rou_path: str,
    hour_seconds: int,
    expect_hours: Optional[int] = None,
    quiet: bool = False,
) -> Dict[str, object]:
    """
    验证生成的 .rou.xml 文件格式正确性

    检查:
    - XML 结构
    - depart 时间单调性
    - vehicle id 序号递增
    - hour index 范围
    """
    # ... validation logic
    return {
        "vehicles": vehicle_count,
        "hourly_counts": hourly_counts,
    }
```

## Test Data Locations

**No dedicated test data directories:**
- Test scenarios are in `/home/samuel/SCU_TSC/sumo_simulation/environments/`
- Generated test output goes to `/home/samuel/SCU_TSC/data/grpo_datasets/`

## Running Tests

**Manual execution required:**
```bash
# Run basic validation tests (no SUMO needed)
python -m grpo.test_generator --single <scenario>

# Run parallel tests across all scenarios
python -m grpo.test_generator --parallel 8
```

**No CI/CD integration detected:**
- No GitHub Actions, GitLab CI, or other CI configuration
- No automated test execution on commit/push

## Testing Gaps

**Areas without test coverage:**

1. **SUMO interface (`sumo_interface.py`):**
   - No unit tests for TraCI wrapper methods
   - No tests for phase calculation logic
   - No tests for queue counting

2. **Dataset generation (`dataset_generator.py`):**
   - No tests for decision point logic
   - No tests for data entry creation
   - No tests for filtering logic

3. **SFT training (`sft_training.py`):**
   - No tests for data loading
   - No tests for model training
   - No tests for checkpoint saving

4. **Prompt building (`prompt_builder.py`):**
   - Basic JSON format validation only
   - No tests for timestamp edge cases
   - No tests for malformed input

5. **Parallel execution (`parallel_runner.py`):**
   - No tests for port assignment
   - No tests for process pooling
   - No tests for error handling

## Recommendations for Testing

**Unit testing framework needed:**
- Consider adopting `pytest` for structured testing
- Add `pytest.ini` configuration
- Separate unit tests from integration tests

**Mocking for SUMO:**
- Create mock SUMO interface for unit tests
- Use `unittest.mock` or `pytest-mock`
- Test business logic without running actual simulations

**Test data fixtures:**
- Create `tests/fixtures/` directory
- Store sample SUMO configuration files
- Store sample JSON datasets for validation

**Coverage goals:**
- Aim for >80% coverage on core logic
- Focus on data processing and transformation code
- External integration (SUMO) can have lower coverage

---

*Testing analysis: 2025-02-02*
