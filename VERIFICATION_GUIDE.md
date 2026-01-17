# GRPO-SUMO 回放对齐验证指南

本文档说明如何验证改动是否生效（reward不再全是-2、std>0、单step耗时稳定）。

## 改动摘要

本次改动解决了以下关键问题：

1. **Dataset字段对齐**：添加 `decision_remaining_sec`, `current_phase_elapsed_sec`, `sumocfg_path`, `tls_phase_durations` 等字段
2. **Reward回放对齐**：
   - signal_step 使用 `decision_remaining_sec` 推进到决策点
   - extend_decision 使用 dataset 的 `current_phase_elapsed_sec`
   - 回放后应用 `tls_phase_durations` 复现随机配时
   - 添加 `green_sec` 硬上限 [1, 120]
   - 改用平均通过车辆数计算奖励
3. **JSON解析容错**：
   - 提取最后一个 JSON 对象
   - 容忍多余字段
   - 容忍数值字符串（如 `"3"` → `3`）
   - extend 值允许同义映射（yes/true → "是"）
4. **Prompt优化**：明确范围、强调只输出JSON不复述规则

## 快速验证步骤（Docker环境）

### 1. 启用快速验证模式

编辑 `Qwen3_TSC_UnslothGRPO_TwoScenarios.py`，在两处设置：

```python
# 第一处：Dataset生成配置
QUICK_VERIFY = True  # 改为 True

# 第二处：训练配置
QUICK_VERIFY = True  # 改为 True
```

这会将配置改为：
- Dataset: 每场景每TL只生成2个signal_step + 2个extend_decision样本
- 训练: 只训练20个step

### 2. 清理旧dataset（如果存在）

```bash
rm -rf grpo_dataset_two_scenarios grpo_states_two_scenarios
```

### 3. 运行Docker训练

```bash
cd /home/samuel/unsloth_dgx/workspace/SCU_TSC
./docker/publish.sh
```

### 4. 观察验证指标

训练开始后，观察日志中的以下指标（约在第5、10、15、20步）：

**成功标志：**
- ✅ `rewards/tsc_reward_fn/mean` **不应长期固定为 -2.0**
- ✅ `rewards/tsc_reward_fn/std` **应 > 0**（至少在某些step）
- ✅ `reward_std` **应 > 0**（至少在某些step）
- ✅ 单个训练step耗时应在合理范围（不应因超长green_sec拖到分钟级）
- ✅ 日志中 `[DEBUG] signal_step/extend_decision 解析失败` 的比例应显著降低

**示例好的输出：**
```
{'loss': 0.023, 'rewards/tsc_reward_fn/mean': -0.5, 'rewards/tsc_reward_fn/std': 0.3, 'reward_std': 0.3, ...}
```

**示例坏的输出（改动前）：**
```
{'loss': 0.0, 'rewards/tsc_reward_fn/mean': -2.0, 'rewards/tsc_reward_fn/std': 0.0, 'reward_std': 0.0, ...}
```

### 5. 检查解析失败率

在日志中搜索 `[DEBUG]`：

```bash
# 如果训练在后台运行
docker logs -f unsloth-tsc-training | grep "DEBUG.*解析失败"
```

解析失败应显著减少（从 >90% 降到 <30%）。

## 正式训练配置

验证通过后，恢复正式训练配置：

1. 编辑 `Qwen3_TSC_UnslothGRPO_TwoScenarios.py`，两处设置：
   ```python
   QUICK_VERIFY = False  # 改回 False
   ```

2. 清理验证用的小dataset：
   ```bash
   rm -rf grpo_dataset_two_scenarios grpo_states_two_scenarios
   ```

3. 重新运行完整训练：
   ```bash
   ./docker/publish.sh
   ```

## 预期改善效果

| 指标 | 改动前 | 改动后（预期） |
|------|--------|----------------|
| reward均值 | 固定 -2.0 | 变化范围 [-2, 1+] |
| reward_std | 0.0 | > 0（通常0.1-1.0） |
| 解析失败率 | >90% | <30% |
| 单step耗时 | 不稳定/可能很长 | 稳定（秒级） |
| 训练有效性 | 无效（全invalid） | 有效（有梯度更新） |

## 故障排查

### 问题1：reward仍然全是-2.0

**可能原因：**
- Dataset未重新生成（仍使用旧字段）
- reward_fn未正确加载新字段

**解决：**
```bash
# 确认删除旧dataset
rm -rf grpo_dataset_two_scenarios grpo_states_two_scenarios
# 重新运行
./docker/publish.sh
```

### 问题2：解析失败率仍然很高

**可能原因：**
- 模型未正确应用prompt修改
- JSON解析逻辑未生效

**检查：**
- 查看生成的completion（日志中 `[DEBUG] Completion #1-3`）
- 确认模型是否输出了JSON格式

### 问题3：训练很慢/卡死

**可能原因：**
- 并行worker冲突（虽然已默认关闭）
- green_sec超长（虽然已加上限）

**检查：**
```python
# 确认 tsc_reward_function.py 中：
REWARD_CONFIG['parallel_workers'] = 0  # 应为0
REWARD_CONFIG['green_sec_max'] = 120  # 应有上限
```

## 联系与支持

如验证失败或遇到问题，请保留以下信息以便排查：
- Docker容器日志（完整）
- Dataset样本示例（`dataset[0]`）
- 训练日志中的前3个DEBUG completion输出
