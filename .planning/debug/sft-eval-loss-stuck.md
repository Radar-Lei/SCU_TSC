---
status: diagnosed
trigger: "调试SFT训练中training loss快速下降但evaluation loss下降缓慢的问题"
created: 2026-02-02T00:00:00Z
updated: 2026-02-02T00:30:00Z
---

## Current Focus

hypothesis: 根因已确认 - 数据划分方式存在严重缺陷
test: 综合分析所有证据，确认根因
expecting: 三个问题共同导致evaluation loss下降缓慢
next_action: 总结根因并撰写诊断报告

## 根因分析

**问题1：验证集场景单一**
- 验证集100%来自arterial4x4_90场景
- 训练集中arterial4x4_90只占6.5%（759/11658）
- 模型主要学习其他11个场景（93.5%），但验证只在一个未见过的场景上测试
- 导致：模型在训练场景上过拟合，在验证场景上泛化差

**问题2：时间序列数据泄露**
- 验证集是arterial4x4_90场景的时间序列**后续片段**
- 训练集时间范围：302-7082
- 验证集时间范围：7107-10981（完全在训练集之后）
- 验证集的决策模式（56% Yes）与训练集（44.9% Yes）显著不同
- 导致：模型遇到的是**未来时段的不同交通模式**，无法泛化

**问题3：数据划分方法错误**
- 代码使用顺序划分：前N条训练，后M条验证
- 数据集按场景聚类排列（同一场景连续存放）
- 没有随机打乱或分层抽样
- 导致：训练/验证集分布严重不一致

## Evidence

- timestamp: 2026-02-02T00:15:00Z
  checked: SFT数据集场景分布
  found:
    * 训练集(11,658条): 12个场景混合，arterial4x4_90占759条(6.5%)
    * 验证集(100条): 100%来自arterial4x4_90单一场景
    * 数据集按场景顺序排列：arterial4x4_99 -> ... -> chengdu -> arterial4x4_90
  implication: 训练集和验证集场景分布严重不匹配，模型主要学习其他11个场景(占93.5%)，但验证时只测试arterial4x4_90场景

- timestamp: 2026-02-02T00:20:00Z
  checked: 数据集组织结构和时间序列特征
  found:
    * 数据集按场景聚类排列（同一场景的数据连续存放）
    * arterial4x4_90位于最后，索引范围: 10899-11757 (共859条)
    * 训练集包含arterial4x4_90的前759条（索引10899-11657）
    * 验证集包含arterial4x4_90的后100条（索引11658-11757）
    * 时间戳分析：训练集arterial4x4_90时间范围302-7082，验证集时间范围7107-10981
    * 验证集是arterial4x4_90场景的**时间序列后续片段**（不是随机抽样）
    * 决策模式差异：
      - 训练集arterial4x4_90: Yes 44.9%, No 55.1%
      - 验证集arterial4x4_90: Yes 56.0%, No 44.0%
      - 训练集整体: Yes 49.5%, No 50.5%
  implication:
    * 验证集不是训练集的随机样本，而是**时间上的未来数据**
    * 验证集的决策模式(56% Yes)与训练集中的arterial4x4_90(44.9% Yes)差异显著
    * 存在**数据泄露风险**：模型可能无法泛化到时间序列的未来数据

- timestamp: 2026-02-02T00:25:00Z
  checked: SFT训练代码的数据划分逻辑 (sft_training.py:59-60)
  found:
    * 代码使用简单的顺序划分：`dataset.select(range(train_count))` 和 `dataset.select(range(train_count, len(dataset)))`
    * 没有随机打乱（shuffle）
    * 没有按场景分层抽样
    * 配置中eval_percent=0.05, eval_limit=300，但实际只取了100条（受数据总量限制）
  implication:
    * 数据划分方式**错误**：对于按场景顺序排列的数据集，顺序划分会导致训练/验证集分布不一致
    * 应该使用**随机分层抽样**确保验证集代表所有场景

## Eliminated

## Resolution

root_cause:
  - **主要问题**：SFT训练的数据划分方式存在严重缺陷，导致训练集和验证集分布不一致
  - **具体原因**：
    1. 验证集场景单一：100%来自arterial4x4_90场景，而训练集只包含6.5%的该场景数据
    2. 时间序列数据泄露：验证集是arterial4x4_90场景的时间后续片段（7107-10981），而训练集只有前期数据（302-7082）
    3. 数据划分方法错误：代码使用简单顺序划分（sft_training.py:59-60），数据集按场景聚类排列，没有随机打乱或分层抽样
  - **影响机制**：
    * 模型主要学习其他11个场景（占训练集93.5%），在 arterial4x4_90 场景上泛化能力差
    * 训练集和验证集的决策模式不同（训练集44.9% Yes vs 验证集56% Yes），说明验证集是不同的交通模式
    * 模型在训练集上快速过拟合（training loss 0.028），但在验证集上无法泛化（evaluation loss 0.99）

fix:
  - **立即修复**：修改 sft_training.py 的数据划分逻辑
    - 使用随机分层抽样，确保验证集包含所有场景
    - 确保验证集是训练集的随机样本，而非时间序列后续片段
  - **建议实现方式**：
    ```python
    # 方案1：使用datasets库的train_test_split with stratify
    from sklearn.model_selection import train_test_split
    import pandas as pd

    # 获取scenario列表用于分层
    scenarios = [item['scenario'] for item in dataset]
    indices = list(range(len(dataset)))

    # 分层抽样
    train_indices, eval_indices = train_test_split(
        indices,
        test_size=0.05,
        stratify=scenarios,  # 按场景分层
        random_state=3407
    )

    train_data = dataset.select(train_indices)
    eval_data = dataset.select(eval_indices)
    ```

  - **超参数调整**（辅助）：
    * 增加权重衰减：0.001 -> 0.01（加强正则化）
    * 降低学习率：2e-4 -> 1e-4（减缓过拟合）
    * 添加early stopping（基于evaluation loss）

verification: []
files_changed: []
