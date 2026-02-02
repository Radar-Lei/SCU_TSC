---
status: testing
phase: 01-grpo-core-infrastructure
source: 01-01-SUMMARY.md, 01-02-SUMMARY.md, 01-03-SUMMARY.md, 01-04-SUMMARY.md
started: 2026-02-02T02:30:00Z
updated: 2026-02-02T04:15:00Z
---

## Current Test
<!-- OVERWRITE each test - shows where we are -->

number: 8
name: 并行SUMO Reward计算
expected: |
  ParallelSUMORewardCalculator可以使用多进程并行计算多个样本的TSC reward，每个SUMO实例使用不同的随机端口
awaiting: user response

## Tests

### 1. 配置文件完整性
expected: config/grpo_config.yaml文件存在且包含所有必需的配置项（模型、GRPO参数、生成控制、训练参数、Reward权重、Format reward、SUMO配置）
result: pass

### 2. 配置类加载YAML
expected: 使用GRPOTrainingConfig.from_yaml("config/grpo_config.yaml")可以成功加载配置，转换为dict时包含所有字段
result: pass

### 3. CLI参数覆盖配置
expected: 运行python grpo/training.py --learning-rate 1e-5 --batch-size 4可以覆盖YAML配置中的对应参数
result: pass

### 4. Format Reward三级评分
expected: format_reward_fn对三种输入返回正确的reward：严格格式{"extend": "yes"}返回+1.0，部分格式Decision: {"extend": "yes"}返回-0.5，无效格式invalid text返回-10.0
result: pass

### 5. Format Reward配置化
expected: config/grpo_config.yaml中的format_reward段可以自定义三级评分的值（strict/partial/invalid）
result: pass

### 6. TSC Reward归一化
expected: tsc_reward_fn计算排队数变化后，使用tanh(-delta/10.0)归一化到[-1,1]范围，改善（delta<0）返回正reward
result: pass

### 7. SUMO仿真从状态恢复
expected: TSC reward计算能够从SUMO状态文件恢复仿真，执行决策（yes延长相位，no切换相位），并计算排队数变化
result: pass

### 8. 并行SUMO Reward计算
expected: ParallelSUMORewardCalculator可以使用多进程并行计算多个样本的TSC reward，每个SUMO实例使用不同的随机端口
result: [pending]

### 9. Reward函数链组合
expected: compute_reward函数组合format_reward和tsc_reward，使用配置的权重（format_weight和tsc_weight）计算加权总reward
result: [pending]

### 10. Early-return优化
expected: 当format完全无效时（extract_decision返回None），跳过TSC仿真计算，直接返回format_reward=-10.0以节省计算时间
result: [pending]

### 11. 批量Reward计算
expected: batch_compute_reward可以处理批量输入（prompts列表、outputs列表、state_files列表），返回对应的reward列表
result: [pending]

### 12. GRPO训练脚本启动
expected: 运行python grpo/training.py --config config/grpo_config.yaml可以启动GRPO训练（使用SFT模型作为起点）
result: [pending]

### 13. 训练日志Reward统计
expected: 训练过程中打印reward统计信息，包括format准确率（strict+partial比例）、平均format reward、平均TSC reward、平均总reward
result: [pending]

### 14. 训练输出模型保存
expected: 训练完成后，LoRA模型保存在output_dir/lora_model，合并后的完整模型保存在output_dir/merged_model
result: [pending]

## Summary

total: 14
passed: 7
issues: 0
pending: 7
skipped: 0

## Gaps

[none yet]
