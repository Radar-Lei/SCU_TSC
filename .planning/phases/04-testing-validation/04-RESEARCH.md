# Phase 04: 测试、验证和完善 - Research

**研究日期:** 2026-02-02
**领域:** Python测试框架、pytest最佳实践、ML模型测试、SUMO仿真测试
**置信度:** HIGH

## Summary

本次研究聚焦于Phase 04的测试实现策略，涵盖了pytest框架的深入应用、ML/AI代码测试模式、SUMO仿真测试的特殊处理，以及Docker容器中的测试执行模式。

**核心研究发现:**
1. **pytest配置**: 推荐使用`pytest.ini`而非`pyproject.toml`，因为其优先级更高且更专注
2. **Fixture模式**: 对于SUMO测试数据，应使用"工厂模式fixture"和"scope=module"的组合策略
3. **标记系统**: 必须在配置文件中注册自定义标记(`@pytest.mark.integration`)以避免警告
4. **测试组织**: 按功能模块组织测试文件，使用`conftest.py`共享fixture
5. **Docker执行**: 通过shell脚本启动容器并执行pytest，使用`--continue-on-collection-errors`和`--maxfail`策略
6. **失败处理**: 使用`pytest -x`或`--maxfail=N`结合自定义钩子收集所有错误

**主要建议:** 使用pytest.ini作为配置文件，采用模块级fixture管理SUMO测试数据，通过scripts/run_tests.sh自动化Docker容器中的测试执行，使用@pytest.mark.integration区分单元测试和集成测试。

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| **pytest** | 8.0+ | Python测试框架 | 行业标准，功能丰富，插件生态成熟，官方文档完善 |
| **pytest-cov** | 5.0+ | 代码覆盖率测量(可选) | pytest官方推荐的覆盖率工具，虽然本项目不设置覆盖率目标 |
| **pytest-html** | 4.1+ | HTML测试报告(可选) | 生成可读性强的测试报告 |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| **pytest-xdist** | 3.6+ | 并行测试执行 | 当需要加速SUMO集成测试时(多个worker并行运行) |
| **pytest-timeout** | 2.3+ | 测试超时控制 | SUMO测试可能耗时，防止测试挂起 |
| **pytest-benchmark** | 4.0+ | 性能基准测试 | 如果需要测试reward函数性能 |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| pytest.ini | pyproject.toml | pyproject.toml更现代但优先级较低;pytest.ini更专注且被广泛使用 |
| 显式fixture | @pytest.mark.usefixtures | usefixtures用于不需要访问fixture对象的场景，显式传递更清晰 |
| yield fixture | addfinalizer | yield更简洁且推荐，addfinalizer仅在复杂场景使用 |

**Installation:**
```bash
# 核心依赖
pip install pytest>=8.0

# 可选依赖(根据需要)
pip install pytest-xdist pytest-timeout pytest-html

# 安装到requirements.txt
echo "pytest>=8.0" >> requirements.txt
```

## Architecture Patterns

### 推荐的项目结构

```
tests/
├── conftest.py                    # 全局共享fixture和pytest钩子
├── __init__.py                    # 空文件，标记为包
├── unit/                          # 单元测试目录
│   ├── __init__.py
│   ├── test_format_reward.py      # format_reward_fn单元测试
│   ├── test_tsc_reward.py         # tsc_reward_fn单元测试
│   ├── test_max_pressure.py       # Max Pressure算法单元测试
│   └── test_config.py             # 配置加载单元测试
├── integration/                   # 集成测试目录
│   ├── __init__.py
│   └── test_integration.py        # 端到端训练流程集成测试
└── fixtures/                      # 测试数据fixture目录
    ├── __init__.py
    ├── conftest.py                # SUMO相关fixture
    └── testdata/                  # 静态测试数据
        ├── sample_prompts.json
        └── sample_sumo_states/
```

### Pattern 1: 工厂模式Fixture (Factory as Fixture)

**What:** fixture返回一个函数而非直接返回数据，允许在测试中多次创建不同的测试数据

**When to use:**
- 需要在单个测试中创建多个变体测试数据
- 测试数据需要参数化
- 需要管理fixture创建的对象生命周期

**Example:**
```python
# tests/fixtures/conftest.py
import pytest
from typing import Dict, Any

@pytest.fixture
def make_prompt():
    """工厂模式fixture: 生成不同类型的测试prompt"""
    def _make_prompt(
        phase_id: int = 0,
        green_elapsed: float = 15.0,
        avg_queue_veh: float = 10.0
    ) -> str:
        prompt_data = {
            "state": {
                "current_phase_id": phase_id,
                "green_elapsed": green_elapsed,
                "phase_metrics_by_id": {
                    phase_id: {"avg_queue_veh": avg_queue_veh}
                }
            }
        }
        return json.dumps(prompt_data)

    return _make_prompt

# tests/unit/test_max_pressure.py
def test_max_pressure_single_phase(make_prompt):
    """测试单相位场景"""
    prompt = make_prompt(phase_id=0, avg_queue_veh=10.0)
    result = max_pressure_decision_from_prompt(prompt, 15.0, 10.0, 60.0, config)
    assert result == 'yes'

def test_max_pressure_multiple_phases(make_prompt):
    """测试多相位场景 - 可以创建多个prompt"""
    prompt1 = make_prompt(phase_id=0, avg_queue_veh=10.0)
    prompt2 = make_prompt(phase_id=1, avg_queue_veh=5.0)
    # ...
```

**Why recommended:**
- 避免重复的测试数据创建代码
- 使测试更简洁和可维护
- 支持灵活的测试数据变体

### Pattern 2: 模块级Scope Fixture

**What:** 使用`scope="module"`的fixture在整个测试模块中只创建一次，提高性能

**When to use:**
- SUMO测试数据加载耗时
- 数据在多个测试间可复用
- 测试不修改共享状态

**Example:**
```python
# tests/fixtures/conftest.py
import pytest
import json
from pathlib import Path

@pytest.fixture(scope="module")
def sumo_test_data():
    """模块级fixture: 加载SUMO测试数据(仅加载一次)"""
    test_data_dir = Path(__file__).parent / "testdata"

    # 加载所有测试数据
    prompts_file = test_data_dir / "sample_prompts.json"
    with open(prompts_file) as f:
        prompts = json.load(f)

    # 返回共享数据
    yield {
        "prompts": prompts,
        "data_dir": test_data_dir
    }

    # 清理代码(可选)

# tests/unit/test_tsc_reward.py
def test_tsc_reward_normal_case(sumo_test_data):
    """多个测试共享同一份sumo_test_data"""
    prompt = sumo_test_data["prompts"][0]
    # ...测试逻辑
```

**Why recommended:**
- 显著提升测试执行速度(SUMO数据加载可能很慢)
- 减少重复的I/O操作
- 符合pytest最佳实践

### Pattern 3: 参数化测试 (Parametrize)

**What:** 使用`@pytest.mark.parametrize`运行同一测试函数多次，每次使用不同输入

**When to use:**
- 测试边界情况和正常情况
- 需要覆盖多种输入变体
- 避免编写重复的测试函数

**Example:**
```python
# tests/unit/test_format_reward.py
import pytest
from grpo.reward import format_reward_fn

@pytest.mark.parametrize("output,expected_reward,is_strict", [
    # 严格格式
    ('{"extend": "yes"}', 1.0, True),
    ('{"extend": "no"}', 1.0, True),

    # 部分遵守(带额外空格)
    ('{ "extend" : "yes" }', -0.5, False),
    ('{"extend": "yes", "extra": "field"}', -0.5, False),

    # 完全无效
    ('invalid json', -10.0, False),
    ('{"extend": "maybe"}', -10.0, False),
    ('', -10.0, False),
    (None, -10.0, False),
])
def test_format_reward_fn_variations(output, expected_reward, is_strict):
    """测试format_reward_fn的各种输入变体"""
    result = format_reward_fn(output)
    assert result.reward == expected_reward
    assert result.is_strict == is_strict
```

**Why recommended:**
- 减少代码重复
- 清晰展示测试覆盖的边界情况
- pytest会为每个参数生成独立的测试报告

### Pattern 4: 集成测试标记

**What:** 使用`@pytest.mark.integration`标记依赖SUMO/unsloth的集成测试

**When to use:**
- 区分快速单元测试和慢速集成测试
- 需要选择性运行测试(如本地只跑单元测试)

**Example:**
```python
# pytest.ini
[pytest]
markers =
    integration: marks tests as integration tests (depend on SUMO/unsloth)
    slow: marks tests as slow (deselect with '-m "not slow"')

# tests/integration/test_integration.py
import pytest
from grpo.reward import batch_compute_reward

@pytest.mark.integration
def test_end_to_end_training_small_scale():
    """小规模端到端训练测试(需要SUMO和unsloth)"""
    # ...测试逻辑

# 运行方式:
# pytest                           # 运行所有测试
# pytest -m "not integration"      # 只运行单元测试
# pytest -m integration            # 只运行集成测试
```

**Why recommended:**
- 明确区分测试类型
- 支持快速反馈(开发时只跑单元测试)
- 符合pytest官方最佳实践

### Pattern 5: 安全的Fixture Teardown

**What:** 使用yield fixture确保资源被正确清理

**When to use:**
- fixture创建了需要清理的资源(临时文件、数据库连接、SUMO进程)

**Example:**
```python
# tests/fixtures/conftest.py
import pytest
import tempfile
import shutil

@pytest.fixture
def temp_sumo_scenario():
    """创建临时SUMO场景目录，测试后自动清理"""
    temp_dir = tempfile.mkdtemp(prefix="sumo_test_")

    # 创建测试文件
    scenario_file = Path(temp_dir) / "scenario.net.xml"
    scenario_file.write_text("<network/>")

    yield temp_dir  # 提供给测试

    # 清理: 无论测试成功或失败都会执行
    shutil.rmtree(temp_dir, ignore_errors=True)

# 使用
def test_sumo_scenario(temp_sumo_scenario):
    """测试结束后temp_sumo_scenario目录会被自动删除"""
    assert Path(temp_sumo_scenario).exists()
```

**Why recommended:**
- 保证测试环境清洁
- 避免测试间相互干扰
- 符合pytest最佳实践

### Anti-Patterns to Avoid

- **重复测试数据创建:** 不要在每个测试中手动创建相似的测试数据，应使用fixture或parametrize
- **全局可变状态:** 避免在测试间共享可变状态(除非是设计如此的模块级fixture)
- **过度使用scope="session":** 除非必要，避免session级fixture，因为可能导致测试耦合
- **忽略fixture清理:** 使用资源(文件、连接、进程)的fixture必须有清理逻辑
- **测试函数命名不清晰:** 避免`test_1`, `test_2`这样的命名，使用描述性名称

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| 测试数据生成 | 手动编写复杂的测试数据创建逻辑 | pytest fixtures (工厂模式) | fixture提供依赖注入、自动清理、scope管理 |
| 参数化测试 | 为每个测试用例编写单独的测试函数 | @pytest.mark.parametrize | 更简洁、清晰的测试报告、避免重复代码 |
| 测试选择 | 使用文件名或注释标记测试类型 | @pytest.mark.* 标记系统 | 原生支持、命令行过滤、可组合条件 |
| 断言消息 | 手动编写详细的错误消息 | pytest自动的assert内省 | pytest会自动显示详细的差异信息 |
| 测试发现 | 自定义测试加载逻辑 | pytest的测试发现 | 按命名约定自动发现、支持多种模式 |
| 并行测试 | 手动管理多进程 | pytest-xdist | 成熟的解决方案、自动负载均衡 |

**Key insight:** pytest已经提供了大量经过验证的机制，重新发明轮子不仅浪费时间，而且容易引入bug。特别是在SUMO测试这种复杂场景中，使用成熟的fixture和scope机制可以大大简化代码。

## Common Pitfalls

### Pitfall 1: 不注册自定义标记

**What goes wrong:** 使用`@pytest.mark.integration`等自定义标记时，pytest会发出警告:
```
PytestUnknownMarkWarning: 'integration' is not a registered marker
```

**Why it happens:** pytest要求在配置文件中显式注册自定义标记，以避免拼写错误

**How to avoid:**
```ini
# pytest.ini
[pytest]
markers =
    integration: marks tests as integration tests (depend on SUMO/unsloth)
    slow: marks tests as slow running
    summation: marks tests related to summation features
```

**Warning signs:** pytest输出中包含`PytestUnknownMarkWarning`

### Pitfall 2: Fixture修改导致测试耦合

**What goes wrong:** 测试A修改了fixture返回的对象，测试B因看到了修改后的状态而失败

**Why it happens:** 使用了模块级或会话级fixture，但测试修改了共享状态

**How to avoid:**
```python
# 错误: 共享可变状态
@pytest.fixture(scope="module")
def shared_list():
    return []  # 多个测试会看到同一个list

def test_a(shared_list):
    shared_list.append(1)  # 修改了共享状态!

def test_b(shared_list):
    assert shared_list == []  # 失败! shared_list是[1]

# 正确: 每次测试获得新副本
@pytest.fixture(scope="module")
def make_list():
    def _make():
        return []
    return _make

def test_a(make_list):
    lst = make_list()
    lst.append(1)  # 只影响这个测试

def test_b(make_list):
    assert make_list() == []  # 通过
```

### Pitfall 3: SUMO测试未使用mock导致测试缓慢

**What goes wrong:** 每次测试都启动完整的SUMO仿真，测试套件执行时间过长

**Why it happens:** 直接集成测试SUMO，未分离单元测试和集成测试

**How to avoid:**
```python
# 单元测试: mock SUMO调用(快速)
import pytest
from unittest.mock import patch

def test_tsc_reward_calculation():
    """测试reward计算逻辑(不实际运行SUMO)"""
    with patch('grpo.sumo_reward.run_sumo_simulation') as mock_sumo:
        mock_sumo.return_value = {"queue_before": 10, "queue_after": 8}
        # ...测试计算逻辑

# 集成测试: 实际运行SUMO(标记为integration)
@pytest.mark.integration
def test_tsc_reward_with_real_sumo():
    """测试完整的SUMO reward计算(慢速)"""
    # ...实际SUMO调用
```

### Pitfall 4: 测试数据硬编码导致难以维护

**What goes wrong:** 测试数据散布在各个测试函数中，修改困难

**Why it happens:** 没有集中管理测试数据fixture

**How to avoid:**
```python
# tests/fixtures/conftest.py
@pytest.fixture
def format_reward_test_cases():
    """集中管理format_reward_fn的测试用例"""
    return {
        "strict_valid": [
            ('{"extend": "yes"}', 1.0, True),
            ('{"extend": "no"}', 1.0, True),
        ],
        "partial_valid": [
            ('{ "extend" : "yes" }', -0.5, False),
        ],
        "invalid": [
            ('invalid', -10.0, False),
            ('', -10.0, False),
        ]
    }

# tests/unit/test_format_reward.py
def test_format_reward_strict_valid(format_reward_test_cases):
    for output, expected_reward, is_strict in format_reward_test_cases["strict_valid"]:
        result = format_reward_fn(output)
        assert result.reward == expected_reward
```

### Pitfall 5: 未处理SUMO测试的异步超时

**What goes wrong:** SUMO测试偶尔挂起，整个测试套件无法完成

**Why it happens:** SUMO仿真可能遇到意外情况而卡住

**How to avoid:**
```ini
# pytest.ini
[pytest]
# 设置测试超时(需要pytest-timeout插件)
timeout = 300  # 5分钟超时
```

```python
# 或使用@pytest.mark.timeout标记特定测试
import pytest

@pytest.mark.integration
@pytest.mark.timeout(600)  # 10分钟超时
def test_slow_integration():
    # ...可能很慢的集成测试
```

### Pitfall 6: Docker容器中测试路径问题

**What goes wrong:** 测试在宿主机上通过，但在Docker容器中失败，提示找不到文件

**Why it happens:** 容器内的工作目录或文件挂载路径与预期不符

**How to avoid:**
```bash
# scripts/run_tests.sh
#!/usr/bin/env bash

# 使用绝对路径或明确的相对路径
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONTAINER_WORKDIR="/home/samuel/SCU_TSC"

docker exec -it $CONTAINER_NAME \
    pytest $CONTAINER_WORKDIR/tests \
        -v \
        --rootdir=$CONTAINER_WORKDIR
```

```python
# 测试中使用 pathlib.Path 处理路径
from pathlib import Path

@pytest.fixture
def test_data_dir():
    # 使用相对于测试文件的路径
    return Path(__file__).parent / "testdata"
```

## Code Examples

### 示例1: format_reward_fn的完整测试

```python
# tests/unit/test_format_reward.py
import pytest
from grpo.reward import format_reward_fn, FormatResult

class TestFormatRewardStrictValid:
    """测试严格有效格式"""

    @pytest.mark.parametrize("output", [
        '{"extend": "yes"}',
        '{"extend": "no"}',
        '{"extend":"yes"}',  # 无空格
        '{ "extend" : "yes" }',  # 多余空格但仍严格有效
    ])
    def test_strict_valid_json_returns_positive_reward(self, output):
        """严格有效的JSON应返回正奖励"""
        result = format_reward_fn(output)
        assert result.reward == 1.0
        assert result.is_strict is True
        assert result.is_partial is False
        assert result.extracted_decision in ["yes", "no"]

class TestFormatRewardPartialValid:
    """测试部分有效格式"""

    @pytest.mark.parametrize("output,expected_decision", [
        ('{"extend": "yes", "extra": "field"}', 'yes'),  # 额外字段
        ('text before {"extend": "no"} text after', 'no'),  # 嵌入文本
        ('{\n"extend":\n"yes"\n}', 'yes'),  # 换行
    ])
    def test_partial_valid_json_returns_partial_reward(self, output, expected_decision):
        """部分有效的JSON应返回部分奖励"""
        result = format_reward_fn(output)
        assert result.reward == -0.5
        assert result.is_strict is False
        assert result.is_partial is True
        assert result.extracted_decision == expected_decision

class TestFormatRewardInvalid:
    """测试无效格式"""

    @pytest.mark.parametrize("output", [
        'invalid json',
        '{"extend": "maybe"}',  # 错误的extend值
        '{"wrong_key": "yes"}',  # 缺少extend键
        '',  # 空字符串
        None,  # None值
    ])
    def test_invalid_format_returns_penalty(self, output):
        """无效格式应返回惩罚"""
        result = format_reward_fn(output)
        assert result.reward == -10.0
        assert result.is_strict is False
        assert result.is_partial is False
        assert result.extracted_decision is None
```

**Source:** 基于pytest官方parametrize文档和项目代码中的format_reward_fn实现

### 示例2: Max Pressure算法测试

```python
# tests/unit/test_max_pressure.py
import pytest
from grpo.max_pressure import (
    max_pressure_decision,
    max_pressure_decision_from_prompt,
    MaxPressureConfig
)

class TestMaxPressureTimeConstraints:
    """测试时间约束逻辑"""

    @pytest.fixture
    def sample_phase_queues(self):
        return {0: 10.0, 1: 5.0, 2: 3.0}

    def test_below_min_green_must_extend(self, sample_phase_queues):
        """小于最小绿灯时间必须延长"""
        config = MaxPressureConfig()
        decision = max_pressure_decision(
            current_phase_id=0,
            phase_queues=sample_phase_queues,
            green_elapsed=5.0,  # 小于min_green=10
            min_green=10.0,
            max_green=60.0,
            config=config
        )
        assert decision == 'yes'

    def test_above_max_green_must_switch(self, sample_phase_queues):
        """超过最大绿灯时间必须切换"""
        config = MaxPressureConfig()
        decision = max_pressure_decision(
            current_phase_id=0,
            phase_queues=sample_phase_queues,
            green_elapsed=60.0,  # 等于max_green=60
            min_green=10.0,
            max_green=60.0,
            config=config
        )
        assert decision == 'no'

class TestMaxPressureDecision:
    """测试Max Pressure决策逻辑"""

    @pytest.mark.parametrize("queues,phase_id,expected", [
        ({0: 10.0, 1: 5.0, 2: 3.0}, 0, 'yes'),  # 当前相位排队最大
        ({0: 5.0, 1: 10.0, 2: 3.0}, 0, 'no'),   # 其他相位排队更大
        ({0: 10.0, 1: 10.0, 2: 3.0}, 0, 'yes'),  # 排队相等，延长当前
        ({0: 0.0, 1: 0.0, 2: 0.0}, 0, 'yes'),    # 所有相位为0，延长当前
    ])
    def test_pressure_based_decision(self, queues, phase_id, expected):
        """测试基于压力的决策"""
        config = MaxPressureConfig()
        decision = max_pressure_decision(
            current_phase_id=phase_id,
            phase_queues=queues,
            green_elapsed=15.0,  # 在[min_green, max_green]范围内
            min_green=10.0,
            max_green=60.0,
            config=config
        )
        assert decision == expected

class TestMaxPressureEdgeCases:
    """测试边界情况"""

    def test_empty_phase_queues_raises_error(self):
        """空phase_queues应抛出ValueError"""
        config = MaxPressureConfig()
        with pytest.raises(ValueError, match="当前相位ID.*不存在"):
            max_pressure_decision(
                current_phase_id=0,
                phase_queues={},
                green_elapsed=15.0,
                min_green=10.0,
                max_green=60.0,
                config=config
            )

    def test_missing_current_phase_raises_error(self):
        """缺少当前相位应抛出ValueError"""
        config = MaxPressureConfig()
        with pytest.raises(ValueError, match="当前相位ID.*不存在"):
            max_pressure_decision(
                current_phase_id=5,  # 不存在
                phase_queues={0: 10.0, 1: 5.0},
                green_elapsed=15.0,
                min_green=10.0,
                max_green=60.0,
                config=config
            )

    @pytest.mark.parametrize("queue_value", [
        -1.0,   # 负数
        -100.0, # 大负数
    ])
    def test_negative_queue_values(self, queue_value):
        """负排队数应被正确处理"""
        config = MaxPressureConfig()
        # 实际实现可能需要处理负数
        decision = max_pressure_decision(
            current_phase_id=0,
            phase_queues={0: queue_value, 1: 0.0},
            green_elapsed=15.0,
            min_green=10.0,
            max_green=60.0,
            config=config
        )
        # 验证决策合理性
        assert decision in ['yes', 'no']
```

**Source:** 基于项目max_pressure.py实现和pytest边界测试最佳实践

### 示例3: 配置加载测试

```python
# tests/unit/test_config.py
import pytest
from grpo.config import load_training_config
from pathlib import Path
import tempfile
import yaml

class TestConfigLoading:
    """测试配置加载"""

    def test_load_valid_config(self):
        """测试加载有效配置"""
        config_file = Path("config/training_config.yaml")
        if not config_file.exists():
            pytest.skip(f"{config_file} not found")

        config = load_training_config(str(config_file))

        # 验证必需的配置节存在
        assert hasattr(config, 'sft')
        assert hasattr(config, 'grpo')
        assert hasattr(config, 'simulation')
        assert hasattr(config, 'reward')

    @pytest.mark.parametrize("missing_field", [
        "training.sft",
        "training.grpo",
        "simulation",
        "reward",
    ])
    def test_missing_required_field_raises_error(self, missing_field):
        """缺少必需字段应抛出错误"""
        config_data = {
            "training": {
                "sft": {"model_path": "dummy"},
                "grpo": {"model_path": "dummy"},
            },
            "simulation": {},
            "reward": {},
            "paths": {},
            "logging": {}
        }

        # 移除必需字段
        parts = missing_field.split('.')
        if parts[0] == "training":
            del config_data["training"][parts[1]]
        else:
            del config_data[parts[0]]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            temp_file = f.name

        try:
            with pytest.raises(ValueError, match=".*必需.*"):
                load_training_config(temp_file)
        finally:
            Path(temp_file).unlink()

class TestConfigOverride:
    """测试配置覆盖"""

    def test_cli_args_override_yaml(self):
        """测试CLI参数覆盖YAML配置"""
        # 这个测试可能需要mock sys.argv或使用配置覆盖API
        # 具体实现取决于grpo.config的设计
        pass

    def test_partial_override(self):
        """测试部分配置覆盖"""
        # 测试只覆盖部分字段，其他字段使用YAML值
        pass
```

**Source:** 基于项目配置系统设计

### 示例4: 集成测试(带SUMO)

```python
# tests/integration/test_integration.py
import pytest
import json
from pathlib import Path

# 标记为集成测试
pytestmark = pytest.mark.integration

@pytest.fixture(scope="module")
def small_test_data():
    """准备小规模测试数据(50条GRPO, 20条SFT)"""
    # 这里可以生成或加载预先准备的小规模数据
    test_data_dir = Path(__file__).parent.parent / "fixtures" / "testdata"

    grpo_data_file = test_data_dir / "small_grpo_dataset.json"
    sft_data_file = test_data_dir / "small_sft_dataset.json"

    return {
        "grpo_file": str(grpo_data_file),
        "sft_file": str(sft_data_file),
        "num_grpo": 50,
        "num_sft": 20,
    }

def test_end_to_end_small_scale_training(small_test_data, tmp_path):
    """
    小规模端到端训练测试

    验证点:
    1. SFT训练成功完成
    2. GRPO训练成功完成
    3. 输出模型文件存在
    4. 训练日志无ERROR
    """
    from grpo.training import run_training

    # 准备输出目录
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # 运行训练(10步)
    result = run_training(
        grpo_data_file=small_test_data["grpo_file"],
        sft_data_file=small_test_data["sft_file"],
        output_dir=str(output_dir),
        num_train_steps=10,  # 小规模: 10步
    )

    # 验证输出
    assert result.success, f"训练失败: {result.error}"
    assert (output_dir / "model" / "adapter_model.safetensors").exists()
    assert result.training_log_has_errors() is False
    assert result.final_loss > 0

def test_reward_chain_with_sumo(small_test_data):
    """测试reward函数链(包含SUMO调用)"""
    from grpo.reward import batch_compute_reward, RewardChainConfig
    from grpo.config import SimulationConfig

    # 加载少量样本
    with open(small_test_data["grpo_file"]) as f:
        data = json.load(f)

    samples = data[:5]  # 只测试5个样本
    prompts = [s["prompt"] for s in samples]
    outputs = ['{"extend": "yes"}'] * len(samples)
    state_files = [s.get("state_file", "") for s in samples]

    # 配置
    chain_config = RewardChainConfig(
        format_weight=1.0,
        tsc_weight=1.0,
    )
    sumo_config = SimulationConfig(
        max_workers=2,  # 减少并行数
        time_step=1.0,
        extend_seconds=5,
    )

    # 计算reward
    rewards, stats = batch_compute_reward(
        prompts=prompts,
        outputs=outputs,
        state_files=state_files,
        chain_config=chain_config,
        sumo_config=sumo_config,
    )

    # 验证
    assert len(rewards) == len(samples)
    assert all(isinstance(r, float) for r in rewards)
    assert stats.total_count == len(samples)
    assert stats.format_accuracy > 0
```

**Source:** 基于CONTEXT.md中的集成测试要求和SUMO测试模式

### 示例5: scripts/run_tests.sh实现

```bash
#!/usr/bin/env bash
set -euo pipefail

################################################################################
# Pytest测试执行脚本
#
# 用法:
#   ./scripts/run_tests.sh [options]
#
# 选项:
#   -u, --unit-only       只运行单元测试
#   -i, --integration     只运行集成测试
#   -a, --all             运行所有测试(默认)
#   -k, --keep-going      遇到失败继续运行
#   -v, --verbose         详细输出
#   --cov                 生成覆盖率报告(可选)
################################################################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Docker配置
CONTAINER_NAME="${CONTAINER_NAME:-qwen3-tsc-grpo}"
CONTAINER_WORKDIR="${CONTAINER_WORKDIR:-/home/samuel/SCU_TSC}"

# 默认参数
RUN_UNIT=true
RUN_INTEGRATION=true
KEEP_GOING=false
VERBOSE=false
COVERAGE=false
PYTEST_ARGS=""

################################################################################
# 解析命令行参数
################################################################################

while [[ $# -gt 0 ]]; do
    case $1 in
        -u|--unit-only)
            RUN_INTEGRATION=false
            shift
            ;;
        -i|--integration)
            RUN_UNIT=false
            shift
            ;;
        -a|--all)
            RUN_UNIT=true
            RUN_INTEGRATION=true
            shift
            ;;
        -k|--keep-going)
            KEEP_GOING=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            PYTEST_ARGS="$PYTEST_ARGS -v"
            shift
            ;;
        --cov)
            COVERAGE=true
            shift
            ;;
        -h|--help)
            echo "用法: $0 [选项]"
            echo ""
            echo "选项:"
            echo "  -u, --unit-only       只运行单元测试"
            echo "  -i, --integration     只运行集成测试"
            echo "  -a, --all             运行所有测试(默认)"
            echo "  -k, --keep-going      遇到失败继续运行"
            echo "  -v, --verbose         详细输出"
            echo "  --cov                 生成覆盖率报告"
            echo "  -h, --help            显示此帮助信息"
            exit 0
            ;;
        *)
            echo -e "${RED}[ERROR] 未知选项: $1${NC}" >&2
            exit 1
            ;;
    esac
done

################################################################################
# 辅助函数
################################################################################

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# 构建pytest选择器
build_marker_expression() {
    local markers=""

    if $RUN_UNIT && ! $RUN_INTEGRATION; then
        markers="not integration"
    elif ! $RUN_UNIT && $RUN_INTEGRATION; then
        markers="integration"
    else
        markers=""  # 运行所有
    fi

    echo "$markers"
}

# 构建pytest参数
build_pytest_args() {
    local args="$PYTEST_ARGS"

    # 添加marker选择
    local markers=$(build_marker_expression)
    if [[ -n "$markers" ]]; then
        args="$args -m \"$markers\""
    fi

    # 失败处理
    if $KEEP_GOING; then
        # 不在第一个失败时停止
        args="$args --maxfail=999"
    else
        # 第一个失败时停止
        args="$args -x"
    fi

    # 覆盖率
    if $COVERAGE; then
        args="$args --cov=grpo --cov-report=html --cov-report=term"
    fi

    # 添加其他有用选项
    args="$args --tb=short --strict-markers"

    echo "$args"
}

################################################################################
# 主逻辑
################################################################################

main() {
    log_info "开始运行测试..."

    # 检查容器是否运行
    if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        log_error "容器 ${CONTAINER_NAME} 未运行"
        log_info "请先启动容器: docker start ${CONTAINER_NAME}"
        exit 1
    fi

    # 构建pytest命令
    local pytest_args=$(build_pytest_args)
    local pytest_cmd="pytest ${pytest_args} ${CONTAINER_WORKDIR}/tests"

    log_info "执行命令: docker exec -it ${CONTAINER_NAME} ${pytest_cmd}"

    # 执行测试
    if docker exec -it "${CONTAINER_NAME}" bash -c "${pytest_cmd}"; then
        log_success "所有测试通过!"

        # 如果生成了覆盖率报告
        if $COVERAGE; then
            log_info "覆盖率报告: ${CONTAINER_WORKDIR}/htmlcov/index.html"
        fi

        exit 0
    else
        local exit_code=$?

        if $KEEP_GOING; then
            log_warning "部分测试失败(退出码: ${exit_code})"
            log_info "运行 'pytest --lf' 查看失败的测试"
        else
            log_error "测试失败(退出码: ${exit_code})"
        fi

        exit $exit_code
    fi
}

main "$@"
```

**Source:** 基于项目docker/publish.sh模式和pytest最佳实践

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| unittest.TestCase类 | 独立测试函数+fixture | pytest 1.0+ (2010s) | 更简洁、更灵活、更易组合 |
| setup.cfg/pytest.ini | pytest.toml或pyproject.toml | pytest 9.0 (2024) | 更现代的配置管理,向后兼容 |
| 手动测试发现 | 自动测试发现 | pytest早期版本 | 开箱即用,遵循约定 |
| 硬编码测试数据 | fixture + parametrize | pytest成熟期 | 更易维护,更好的测试覆盖率 |

**Deprecated/outdated:**
- **直接使用unittest**: 虽然pytest支持unittest,但新项目不应使用,应使用pytest原生风格
- **setup.cfg用于pytest配置**: 官方不再推荐,可能导致解析问题
- **在测试函数中直接创建测试数据**: 应使用fixture实现数据复用和清理

## Open Questions

1. **SUMO测试数据的生成策略**
   - What we know: 需要使用现有SUMO数据集，需要小规模数据(50 GRPO, 20 SFT)
   - What's unclear: 是动态生成测试数据还是使用静态预生成的数据文件?
   - Recommendation: 创建独立的数据生成脚本`scripts/generate_test_data.py`，预生成测试数据到`tests/fixtures/testdata/`，避免每次测试都重新生成

2. **pytest配置文件的最终选择**
   - What we know: pytest.ini优先级最高且广泛使用
   - What's unclear: 项目是否已经有pyproject.toml用于其他目的?
   - Recommendation: 使用`pytest.ini`，因为更专注且避免与项目其他配置混合

3. **测试超时的具体阈值**
   - What we know: SUMO测试可能耗时，需要设置超时
   - What's unclear: 单个SUMO测试的合理超时时间是多少?
   - Recommendation: 单个SUMO测试设置为5分钟超时，整个测试套件设置为30分钟超时

4. **测试报告的格式和存储**
   - What we know: 测试结果需要可读性强
   - What's unclear: 是否需要HTML测试报告?报告存储在哪里?
   - Recommendation: 使用`--html=.pytest_reports/report.html`生成HTML报告，可选功能，默认不启用

## Sources

### Primary (HIGH confidence)
- pytest官方文档 - https://docs.pytest.org/en/stable/ (核心功能、fixture、parametrize、配置)
- pytest fixture文档 - https://docs.pytest.org/en/stable/how-to/fixtures.html (fixture最佳实践、scope、yield)
- pytest标记文档 - https://docs.pytest.org/en/stable/how-to/mark.html (自定义标记注册)
- pytest配置文档 - https://docs.pytest.org/en/stable/reference/customize.html (配置文件格式和优先级)
- pytest失败处理 - https://docs.pytest.org/en/stable/how-to/failures.html (maxfail、-x选项)

### Secondary (MEDIUM confidence)
- Real Python: Effective Python Testing With pytest - https://realpython.com/pytest-python-testing/ (pytest基础教程和最佳实践)
- OneUptime: How to Configure pytest (2026) - https://oneuptime.com/blog/post/2026-01-24-configure-pytest-python-testing/view (现代pytest配置指南)
- Fiddler: Advanced Pytest Patterns (2024) - https://www.fiddler.ai/blog/advanced-pytest-patterns-harnessing-the-power-of-parametrization-and-factory-methods (高级模式: parametrize和工厂模式)
- TestDriven.io: Docker Best Practices (2024) - https://testdriven.io/blog/docker-best-practices/ (Docker和测试集成)
- pytest-mark.parametrize最佳实践 - 多个社区文章和StackOverflow讨论验证

### Tertiary (LOW confidence)
- LambdaTest: Parameterization in Pytest (2026) - https://www.testmu.ai/blog/parameterization-in-pytest-with-selenium/ (parametrize用例)
- Medium: pytest配置实践 (2025) - 多篇Medium文章关于pytest.ini vs pyproject.toml的选择
- StackOverflow: pytest执行和Docker集成 - 多个问题讨论Docker中运行pytest的最佳实践

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - pytest是Python测试的既定标准，所有建议基于官方文档
- Architecture: HIGH - 所有模式来自pytest官方文档和广泛验证的最佳实践
- Pitfalls: HIGH - 基于官方警告、文档和常见的pytest问题
- SUMO测试: MEDIUM - SUMO测试策略基于项目需求，一般ML测试模式来自社区最佳实践
- Docker执行: MEDIUM - Docker模式基于项目现有脚本，经社区模式验证

**Research date:** 2026-02-02
**Valid until:** 2026-06-02 (4个月 - pytest稳定，但插件生态可能有更新)

---

*Phase: 04-testing-validation*
*Research completed: 2026-02-02*
*Researcher: gsd-phase-researcher*
