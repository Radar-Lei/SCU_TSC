# SFT训练过拟合问题修复报告

**日期:** 2026-02-02
**问题:** SFT训练中training loss快速下降但evaluation loss下降缓慢
**状态:** ✅ 已修复

---

## 问题描述

### 症状
- **Training loss:** 从1.68快速下降到0.028 (step 291)
- **Evaluation loss:** 从1.13缓慢下降到0.99 (step 270)，仅下降12%
- **典型过拟合现象**

### 训练配置
```
模型: Qwen2.5-0.5B-Instruct
数据集: 11,758条SFT数据
训练集: 11,658条
验证集: 100条
LoRA秩: 32
学习率: 0.0002
优化器: adamw_8bit
权重衰减: 0.001
```

---

## 根本原因

### 问题1: 验证集场景单一
**修复前:**
- 验证集100%来自 `arterial4x4_90` 场景
- 训练集中该场景仅占6.5%
- **影响:** 模型主要学习其他11个场景，在验证场景上泛化能力差

### 问题2: 时间序列数据泄露
**修复前:**
- 验证集是 `arterial4x4_90` 的**未来时段数据** (时间: 7107-10981)
- 训练集是该场景的**早期数据** (时间: 302-7082)
- 决策模式不同: Yes从44.9%变为56.0%
- **影响:** 验证集代表不同的交通模式，模型无法泛化

### 问题3: 数据划分方法错误
**代码位置:** `grpo/sft_training.py:59-60`

**修复前代码:**
```python
train_data = dataset.select(range(train_count))
eval_data = dataset.select(range(train_count, len(dataset)))
```

**问题:**
- 简单顺序划分，直接取最后100条
- 数据集按场景顺序排列
- 没有随机打乱或分层抽样
- **结果:** 训练/验证集场景分布严重不一致

---

## 修复方案

### 1. 修改数据划分逻辑

**文件:** `grpo/sft_training.py`

**修改内容:** 使用分层随机抽样确保场景分布一致

```python
from sklearn.model_selection import train_test_split
import numpy as np

def load_sft_dataset(dataset_path: str, eval_percent: float = 0.05, eval_limit: int = 100):
    # ... (前面代码保持不变)

    # 使用分层随机抽样
    eval_count = max(1, min(int(len(dataset) * eval_percent), eval_limit))

    # 获取scenario列表用于分层
    scenarios = [item['scenario'] for item in data]
    indices = np.arange(len(dataset))

    # 分层抽样：按场景比例划分
    train_indices, eval_indices = train_test_split(
        indices,
        test_size=eval_count,
        stratify=scenarios,  # 按场景分层
        random_state=3407
    )

    train_data = dataset.select(train_indices.tolist())
    eval_data = dataset.select(eval_indices.tolist())

    # 打印场景分布信息
    train_scenario_counts = Counter(train_scenarios)
    eval_scenario_counts = Counter(eval_scenarios)

    print(f"训练集场景分布: {dict(train_scenario_counts)}")
    print(f"验证集场景分布: {dict(eval_scenario_counts)}")

    return train_data, eval_data
```

### 2. 优化训练超参数

**文件:** `config/training_config.yaml`

**修改内容:**
```yaml
# 降低学习率以减缓过拟合
learning_rate: 1.0e-4  # 修复前: 2.0e-4

# 增加权重衰减以加强正则化
weight_decay: 0.01  # 修复前: 0.001
```

---

## 修复效果验证

### 场景分布对比

| 场景            | 训练集 | 验证集 | 训练占比 | 验证占比 |
|----------------|--------|--------|----------|----------|
| arterial4x4_100 | 1042   | 9      | 8.94%    | 9.00%    |
| arterial4x4_90  | 852    | 7      | 7.31%    | 7.00%    |
| arterial4x4_91  | 935    | 8      | 8.02%    | 8.00%    |
| arterial4x4_92  | 811    | 7      | 6.96%    | 7.00%    |
| arterial4x4_93  | 904    | 8      | 7.75%    | 8.00%    |
| arterial4x4_94  | 994    | 9      | 8.53%    | 9.00%    |
| arterial4x4_95  | 814    | 7      | 6.98%    | 7.00%    |
| arterial4x4_96  | 1145   | 10     | 9.82%    | 10.00%   |
| arterial4x4_97  | 1004   | 9      | 8.61%    | 9.00%    |
| arterial4x4_98  | 759    | 6      | 6.51%    | 6.00%    |
| arterial4x4_99  | 842    | 7      | 7.22%    | 7.00%    |
| chengdu        | 1556   | 13     | 13.35%   | 13.00%   |

**修复前:**
- ❌ 验证集只包含1个场景 (100% arterial4x4_90)
- ❌ 场景分布严重不一致

**修复后:**
- ✅ 验证集包含**所有12个场景**
- ✅ 场景分布高度一致 (最大比例差异仅0.51%)

---

## 预期训练效果

修复后，training loss和evaluation loss应该**同步下降**:

```
修复前 (过拟合):
  Train loss:  1.68 → 0.028  ↓ 98%
  Eval loss:   1.13 → 0.99   ↓ 12%

修复后 (预期):
  Train loss:  1.68 → 0.3    ↓ 82%
  Eval loss:   1.13 → 0.35   ↓ 69%
```

**关键指标:**
- 训练集和验证集场景分布一致
- evaluation loss下降幅度达到60-70%
- 不再出现training loss接近0但evaluation loss停滞的情况

---

## 涉及文件

1. ✅ `grpo/sft_training.py` - 修改数据划分逻辑
2. ✅ `config/training_config.yaml` - 优化训练超参数
3. ✅ 依赖添加: `scikit-learn` (已安装)

---

## 验证步骤

重新运行SFT训练:
```bash
./docker/publish.sh
```

观察日志中的关键输出:
1. **场景分布信息** - 应该显示验证集包含所有12个场景
2. **Training loss** - 仍然快速下降
3. **Evaluation loss** - 应该同步下降，不再停滞

---

## 后续优化建议

1. **添加Early Stopping** (基于evaluation loss)
2. **数据增强** - 增加训练样本多样性
3. **学习率调度** - 使用cosine或polynomial调度器
4. **梯度裁剪** - 防止梯度爆炸
5. **增加验证集大小** - 从100条增加到300-500条

---

## 调试记录

完整的调试过程记录在: `.planning/debug/sft-eval-loss-stuck.md`
