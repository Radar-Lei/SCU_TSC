---
status: resolved
trigger: "调查配置文件混乱问题: config-file-confusion"
created: 2026-02-02T00:00:00Z
updated: 2026-02-02T01:30:00Z
---

## Current Focus

hypothesis: 配置文件设计意图明确:grpo_config.yaml用于数据生成,training_config.yaml用于训练,但实际使用中存在混淆
test: 验证设计意图并制定合并方案
expecting: 确认是否需要合并配置文件
next_action: 根据发现制定修复方案

## Symptoms

expected: 应该合并为一个配置文件,结构清晰,职责明确
actual:
- 参数重复出现在两个文件中(learning_rate, batch_size, gradient_accumulation_steps, logging_steps, save_steps, warmup_steps, optim, lora_rank, seed, max_seq_length等)
- 参数位置不明确,不清楚应该在哪个文件中配置
- 配置结构混乱,training_config.yaml有嵌套结构(grpo.sft, training.grpo),grpo_config.yaml是扁平结构
- Reward配置完全重复(format_reward, reward.chain)
- SUMO仿真配置部分重复(sumo配置在两个文件中都有)
errors:
- 代码中配置读取逻辑不清晰
- 修改参数时容易出错(可能修改了错误的配置文件)
- 难以配置训练参数
reproduction:
1. 查看 config/grpo_config.yaml - 包含GRPO训练的所有参数(扁平结构)
2. 查看 config/training_config.yaml - 包含SFT和GRPO的嵌套结构参数
3. 尝试修改GRPO的学习率时,需要在两个地方修改
4. 代码中使用read_config.py读取,但不确定优先级和合并逻辑
started: 项目创建时就这样了,历史遗留问题

## Eliminated

## Evidence

- timestamp: 2026-02-02T00:15:00Z
  checked: grpo/training.py的main函数配置加载逻辑
  found: 代码根据文件名判断配置类型:包含"training_config.yaml"使用TrainingConfig,否则使用GRPOTrainingConfig
  implication: 两个配置文件是互斥的,不是合并关系

- timestamp: 2026-02-02T00:20:00Z
  checked: grpo/config.py的配置类定义
  found: TrainingConfig.grpo属性返回GRPOTrainingConfig实例,从training.training.grpo转换
  implication: training_config.yaml中的grpo段会被转换为GRPOTrainingConfig

- timestamp: 2026-02-02T00:25:00Z
  checked: config/training_config.yaml文件结构
  found: 嵌套结构training.sft和training.grpo,包含SFT和GRPO所有参数
  implication: training_config.yaml是中央配置文件,包含所有训练参数

- timestamp: 2026-02-02T00:28:00Z
  checked: config/grpo_config.yaml文件结构
  found: 扁平结构,直接包含GRPO训练的所有参数
  implication: grpo_config.yaml是GRPO专用配置文件,结构更简洁

- timestamp: 2026-02-02T00:30:00Z
  checked: CONFIG_FIX_SUMMARY.md文档
  found: 文档明确说明"统一使用 config/training_config.yaml 作为主配置文件"
  implication: 项目意图是使用training_config.yaml作为单一配置源

- timestamp: 2026-02-02T01:00:00Z
  checked: 数据生成脚本使用配置的情况
  found: generate_grpo_dataset.py使用GRPOConfig类(用于数据生成,不是训练),该类来自grpo.config且不读取YAML文件
  implication: grpo_config.yaml文件名具有误导性,GRPOConfig类直接使用Python默认值,不读取grpo_config.yaml

- timestamp: 2026-02-02T01:05:00Z
  checked: .planning/STATE.md的设计意图说明
  found: "保持向后兼容:grpo_config.yaml继续用于数据生成,training_config.yaml用于训练"
  implication: 原设计意图是分离数据生成和训练配置,但实现时数据生成代码并未使用YAML文件

## Resolution

root_cause:
  1. **配置文件职责混淆**: 项目存在两个配置文件,但设计意图与实际使用不符
     - grpo_config.yaml: 名义上用于"数据生成",实际数据生成代码(GRPOConfig类)不读取YAML文件
     - training_config.yaml: 实际用于训练,包含SFT和GRPO所有参数

  2. **参数完全重复**: 19个GRPO训练参数在两个文件中完全重复,增加维护负担和出错风险
     - 所有重复参数值当前一致,但修改时容易遗漏其中一个
     - reward配置(sumo, format_reward)在两个文件中结构不同但功能相同

  3. **文档与代码不一致**:
     - 文档STATE.md说"grpo_config.yaml继续用于数据生成"
     - 实际数据生成代码使用GRPOConfig类的Python默认值,不读取YAML
     - 训练代码可以同时支持两个配置文件(通过文件名判断),但推荐使用training_config.yaml

fix:
  删除grpo_config.yaml文件,统一使用training_config.yaml:
  1. ✓ 删除config/grpo_config.yaml
  2. ✓ 更新grpo/training.py的示例文档,只引用training_config.yaml
  3. ✓ 更新grpo/config.py的文档,删除对grpo_config.yaml的引用
  4. ✓ 从config/training_config.yaml删除paths.grpo_config配置项
  5. ✓ 从grpo/config.py的PathsConfig类删除grpo_config字段
  6. ✓ 更新GRPOConfig和GRPOTrainingConfig类的文档,明确说明配置来源

  理由:
  - training_config.yaml已经包含所有训练参数(training.sft和training.grpo)
  - 代码已经支持通过training_config.yaml进行GRPO训练
  - 简化配置管理,避免参数不一致的风险
  - 符合CONFIG_FIX_SUMMARY.md中"统一使用training_config.yaml"的修复方向

verification:
  - ✓ config/training_config.yaml加载成功
  - ✓ 配置类正常工作(SFT, GRPO, SUMO配置均可访问)
  - ✓ tests/unit/test_config.py::TestTrainingConfig::test_full_config_loading通过
  - ✓ grpo_config.yaml文件已删除

files_changed:
  - config/grpo_config.yaml (已删除)
  - config/training_config.yaml (删除paths.grpo_config字段)
  - grpo/config.py (更新文档和PathsConfig类)
  - grpo/training.py (更新用法文档)