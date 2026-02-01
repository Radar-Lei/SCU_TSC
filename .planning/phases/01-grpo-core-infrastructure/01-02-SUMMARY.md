# Phase 1 Plan 02: Format Reward函数实现

**Plan:** 01-02
**Status:** Complete
**Duration:** ~5 minutes
**Tasks:** 3/3

---

## 实现概述

实现了format_reward_fn函数，用于验证模型输出是否符合JSON格式要求，采用三级评分机制确保模型学习输出正确格式的决策。

**核心目标**: 确保模型学习输出严格格式的JSON `{"extend": "yes/no"}`，这是有效进行TSC决策的前提。

---

## 核心功能

### 1. FormatResult数据类

```python
@dataclass
class FormatResult:
    reward: float
    is_strict: bool
    is_partial: bool
    extracted_decision: Optional[str]  # "yes", "no", or None
```

### 2. format_reward_fn核心函数

**三级评分机制**:

1. **严格格式 (+1.0)**: 精确匹配 `{"extend": "yes"}` 或 `{"extend": "no"}`
   - JSON解析成功
   - 只有一个"extend"键
   - 值为"yes"或"no"

2. **部分遵守格式 (-0.5)**: 能通过正则提取yes/no
   - 带额外文本：`Decision: {"extend": "yes"} based on analysis.`
   - 带额外字段：`{"extend": "no", "reason": "low queue"}`
   - 大小写不敏感：`{"extend": "YES"}`

3. **完全不遵守格式 (-10.0)**: 无法提取决策
   - 空字符串
   - 无效JSON
   - 错误的决策值（如"maybe"）

### 3. extract_decision辅助函数

使用正则表达式从文本中提取决策：
- 默认正则：`r'\{["\s]*extend["\s]*:\s*["\s]*(yes|no)["\s]*(?:,|\})'`
- 允许yes/no后有逗号或右括号（处理带额外字段的JSON）
- 大小写不敏感
- 返回小写的"yes"、"no"或None

### 4. batch_format_reward批量处理

供GRPOTrainer使用的批量版本，接受输出列表并返回奖励列表。

---

## 配置管理

### config/grpo_config.yaml新增配置

```yaml
# ============== Format Reward配置 ==============
# format_reward_fn的三级评分参数
format_reward:
  strict: 1.0          # 严格格式奖励
  partial: -0.5        # 部分遵守格式惩罚
  invalid: -10.0       # 完全不遵守格式惩罚
  extract_regex: '\{["\s]*extend["\s]*:\s*["\s]*(yes|no)["\s]*(?:,|\})'
```

### grpo/config.py新增配置类

```python
@dataclass
class FormatRewardConfig:
    """Format Reward配置"""
    strict: float = 1.0
    partial: float = -0.5
    invalid: float = -10.0
    extract_regex: str = r'\{["\s]*extend["\s]*:\s*["\s]*(yes|no)["\s]*(?:,|\})'
```

GRPOTrainingConfig新增字段：
```python
format_reward: FormatRewardConfig = field(default_factory=FormatRewardConfig)
```

---

## 测试验证

所有测试场景均通过：

| 测试场景 | 输入 | 预期Reward | 预期is_strict | 预期is_partial | 状态 |
|---------|------|-----------|--------------|---------------|------|
| 严格格式-yes | `{"extend": "yes"}` | +1.0 | True | False | ✓ |
| 严格格式-no | `{"extend": "no"}` | +1.0 | True | False | ✓ |
| 严格格式-带空格 | `{"extend": "yes"  }` | +1.0 | True | False | ✓ |
| 严格格式-带换行 | `{\n  "extend": "yes"\n}` | +1.0 | True | False | ✓ |
| 部分格式-带额外文本 | `Decision: {"extend": "yes"}` | -0.5 | False | True | ✓ |
| 部分格式-带额外字段 | `{"extend": "no", "reason": "..."}` | -0.5 | False | True | ✓ |
| 无效格式 | `invalid output` | -10.0 | False | False | ✓ |
| 空字符串 | `` | -10.0 | False | False | ✓ |
| 大小写不敏感 | `{"extend": "YES"}` | +1.0 | True | False | ✓ |
| 错误决策值 | `{"extend": "maybe"}` | -10.0 | False | False | ✓ |

---

## 正则表达式设计

**优化过程**:
1. 初始版本：`r'\{["\s]*extend["\s]*:\s*["\s]*(yes|no)["\s]*\}'`
   - 问题：无法处理带额外字段的JSON（如`{"extend": "no", "reason": "..."}`）

2. 优化版本：`r'\{["\s]*extend["\s]*:\s*["\s]*(yes|no)["\s]*(?:,|\})'`
   - 改进：允许yes/no后有逗号或右括号
   - 效果：能正确提取带额外字段的JSON中的决策

**配置化优势**:
- 正则表达式可通过YAML配置文件修改
- 不同场景可使用不同的提取规则
- 无需修改代码即可调整格式验证逻辑

---

## 关键文件

| 文件 | 作用 | 新增/修改 |
|------|------|----------|
| `grpo/reward.py` | Reward函数模块 | 新建 |
| `config/grpo_config.yaml` | 配置文件 | 新增format_reward段 |
| `grpo/config.py` | 配置类 | 新增FormatRewardConfig类 |
| `grpo/__init__.py` | 模块导出 | 新增reward函数导出 |

---

## 模块导出

可以直接从grpo包导入：
```python
from grpo import format_reward_fn, extract_decision, FormatResult
```

也可以从子模块导入：
```python
from grpo.reward import format_reward_fn, extract_decision, FormatResult
```

---

## 设计亮点

1. **严格的JSON验证**: 使用json.loads进行真正的JSON解析，确保格式完全正确
2. **容错的正则提取**: 即使JSON不严格，也能提取出决策给予部分奖励
3. **配置化参数**: 所有评分和正则表达式都可通过配置文件调整
4. **批量处理支持**: batch_format_reward便于GRPOTrainer集成
5. **详细的结果信息**: FormatResult提供is_strict、is_partial等标志，便于调试和分析

---

## 与其他模块的集成

**训练脚本集成** (grpo/training.py):
- 导入format_reward_fn用于计算format reward
- 结合config.format_reward参数配置
- 与tsc_reward_fn组合形成总reward

**未来TSC reward集成** (01-03):
- 总reward = format_weight * format_reward + tsc_weight * tsc_reward
- format_weight控制格式的重要性
- 格式验证通过后才能进行TSC评估

---

## 下一步

**01-03: TSC Reward函数**:
- 实现tsc_reward_fn，基于SUMO仿真评估决策质量
- 使用format_reward_fn提取的决策驱动仿真
- 组合格式和TSC reward形成完整reward信号

---

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] 正则表达式无法提取带额外字段的JSON**

- **Found during:** Task 1 verification
- **Issue:** 初始正则 `r'\{["\s]*extend["\s]*:\s*["\s]*(yes|no)["\s]*\}'` 无法匹配 `{"extend": "no", "reason": "low queue"}` 这类带额外字段的JSON
- **Fix:** 优化正则为 `r'\{["\s]*extend["\s]*:\s*["\s]*(yes|no)["\s]*(?:,|\})'`，允许yes/no后有逗号或右括号
- **Files modified:** grpo/reward.py
- **Commit:** b625109

**2. [Rule 1 - Bug] 文档字符串中无效的转义序列警告**

- **Found during:** Task 1 verification
- **Issue:** docstring中的反斜杠导致SyntaxWarning
- **Fix:** 从文档字符串中移除正则表达式的具体表示，改用描述性语言
- **Files modified:** grpo/reward.py
- **Commit:** b625109

---

## Authentication Gates

None encountered during this plan.
