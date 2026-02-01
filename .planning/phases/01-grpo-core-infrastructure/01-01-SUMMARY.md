# Phase 1 Plan 01: GRPO训练脚本框架 Summary

**Phase:** 01-grpo-core-infrastructure
**Plan:** 01
**Completed:** 2026-02-02
**Duration:** 2m 15s
**Subsystem:** GRPO训练基础设施
**Tags:** grpo, training, config, unsloth, trl

---

## One-Liner

创建GRPO训练配置系统和脚本框架，集成Unsloth FastLanguageModel和TRL GRPOTrainer，实现YAML配置管理和数据加载功能。

## Delivered Artifacts

### 1. 配置系统

**File:** `config/grpo_config.yaml`
- 完整的GRPO训练超参数配置
- 模型配置：model_path, max_seq_length
- GRPO核心参数：learning_rate, batch_size, num_generations, temperature, kl_coeff
- 生成控制：max_new_tokens, top_p, repetition_penalty
- 训练参数：epochs, warmup, logging, optimizer
- Reward权重（预留01-02, 01-03）
- SUMO仿真参数（预留01-03）
- 数据和输出路径配置

**File:** `grpo/config.py` (新增GRPOTrainingConfig类)
- `GRPOTrainingConfig` dataclass：完整的配置数据类
- `from_yaml(cls, path)` 类方法：从YAML加载配置
- `to_dict(self)` 方法：转换为字典
- `__post_init__` 方法：参数验证（范围检查、必需参数）
- `load_config(path)` 便捷函数
- 保留了原有的`GRPOConfig`类（数据生成配置）

### 2. 训练脚本

**File:** `grpo/training.py`

**导出的函数:**
- `load_grpo_dataset(dataset_path: str) -> Dataset`
  - 支持单文件和目录扫描（自动查找grpo_dataset.json）
  - 转换为TRL GRPOTrainer期望的格式
  - 返回HuggingFace Dataset对象

- `train_grpo(config: GRPOTrainingConfig)`
  - 使用FastLanguageModel.from_pretrained加载SFT模型
  - 添加LoRA适配器（可配置秩）
  - 创建TRL的GRPOConfig和GRPOTrainer
  - 集成占位符reward函数（返回0.0）
  - 保存LoRA模型和merged模型

- `reward_function_placeholder(prompts, outputs, **kwargs) -> List[float]`
  - 占位符reward函数
  - 在01-02（格式检查）和01-03（TSC reward）中实现具体逻辑

- `parse_args()` 和 `main()`
  - 支持--config参数指定配置文件
  - 支持命令行参数覆盖配置（优先级：CLI > YAML > 默认）
  - 参数：--model-path, --dataset-path, --output-dir, --learning-rate, --batch-size, --num-epochs, --max-steps

### 3. 模块导出

**File:** `grpo/__init__.py`
- 导出train_grpo, load_grpo_dataset（训练相关）
- 导出GRPOTrainingConfig, load_config（配置相关）
- 保留原有导出：GRPOConfig, DEFAULT_CONFIG, SYSTEM_PROMPT（数据生成相关）

---

## Technical Decisions

### 1. 配置类命名分离

**决策:** 创建新的`GRPOTrainingConfig`类，而不是修改现有的`GRPOConfig`

**原因:**
- `GRPOConfig`用于数据集生成（已有的）
- `GRPOTrainingConfig`用于训练配置（新增）
- 避免命名冲突和职责混淆
- 两个类关注点不同（数据生成 vs 模型训练）

### 2. 数据格式转换

**决策:** 在load_grpo_dataset中转换为TRL GRPOTrainer期望的格式

**实现:**
- 读取GRPO数据集JSON文件
- 提取prompt字段
- 转换为格式：`{"prompt": prompt, "id": ..., "scenario": ..., "junction_id": ...}`
- 使用datasets.Dataset.from_list()创建Dataset对象

**未来考虑:** 暂不包含expert_decision字段，因为GRPO需要通过reward函数动态评估

### 3. Reward函数占位符设计

**决策:** 创建占位符reward函数返回固定0.0

**原因:**
- 框架可以立即测试（不依赖具体reward逻辑）
- 在01-02和01-03中分别实现：
  - 01-02: 格式检查reward（JSON格式验证、extend字段验证）
  - 01-03: TSC reward（SUMO仿真评估排队车辆数）
- 清晰标记"占位符"状态，避免误用

### 4. CLI参数覆盖机制

**决策:** 支持命令行参数覆盖YAML配置

**优先级:** 命令行 > 配置文件 > 默认值

**实现:**
- 先加载YAML配置
- 检查命令行参数（使用argparse的default=None）
- 如果CLI参数非None，覆盖配置对象属性

---

## Tech Stack

**Added:**
- `pyyaml`: YAML配置文件解析

**Used:**
- `unsloth.FastLanguageModel`: 模型加载和LoRA配置
- `trl.GRPOTrainer`: GRPO训练器
- `trl.GRPOConfig`: TRL的GRPO配置类
- `datasets.Dataset`: HuggingFace数据集格式

**Patterns:**
- 配置文件 → Dataclass → 验证 → 使用
- CLI参数覆盖YAML配置
- 占位符函数用于渐进式开发

---

## File Changes

### Created
- `config/grpo_config.yaml`: GRPO训练配置文件
- `grpo/training.py`: GRPO训练主脚本

### Modified
- `grpo/config.py`: 添加GRPOTrainingConfig类和load_config函数
- `grpo/__init__.py`: 更新模块导出

---

## Key Code References

### 配置加载模式
```python
# 从YAML加载配置
config = GRPOTrainingConfig.from_yaml("config/grpo_config.yaml")

# 转换为字典
config_dict = config.to_dict()
```

### 模型加载（参考SFT训练）
```python
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=config.model_path,
    max_seq_length=config.max_seq_length,
    load_in_4bit=False,
)

# 添加LoRA适配器
model = FastLanguageModel.get_peft_model(
    model,
    r=config.lora_rank,
    target_modules=[...],
    use_gradient_checkpointing="unsloth",
)
```

### 数据加载
```python
# 支持单文件或目录
dataset = load_grpo_dataset(config.dataset_path)

# 自动扫描目录中的grpo_dataset.json
json_files = glob.glob(os.path.join(dataset_path, "*/grpo_dataset.json"))
```

### GRPOTrainer初始化
```python
grpo_config = GRPOConfig(
    learning_rate=config.learning_rate,
    batch_size=config.batch_size,
    num_generations=config.num_generations,
    temperature=config.temperature,
    kl_coeff=config.kl_coeff,
    # ... 其他参数
)

trainer = GRPOTrainer(
    model=model,
    reward_funcs=reward_function_placeholder,  # 占位符
    args=grpo_config,
    train_dataset=train_dataset,
)
```

---

## Dependencies

### Requires
- 无前置依赖（Phase 1的第一个计划）

### Provides
- GRPO训练配置系统（供01-02, 01-03使用）
- 训练脚本框架（供01-02, 01-03, 01-04使用）
- 数据加载函数（供所有训练计划使用）

### Affects
- 01-02: 将实现格式检查reward函数
- 01-03: 将实现TSC reward函数和SUMO集成
- 01-04: 将集成所有reward函数并完成训练流程

---

## Integration Points

### 与SFT训练的差异

| 方面 | SFT训练 | GRPO训练 |
|------|---------|----------|
| 训练器 | SFTTrainer | GRPOTrainer |
| 配置类 | SFTConfig | GRPOConfig |
| 数据格式 | messages + text | prompt + reward |
| 标签 | 静态（固定response） | 动态（通过reward函数评估） |
| 目标 | 学习输出格式 | 优化决策质量 |

### 数据流

```
GRPO数据集 (JSON)
    ↓
load_grpo_dataset()
    ↓
Dataset对象 (TRL格式)
    ↓
GRPOTrainer
    ↓
生成多个候选response
    ↓
reward_function_placeholder() (当前: 返回0.0)
    ↓
01-02: 格式检查reward
01-03: TSC reward (SUMO仿真)
    ↓
策略梯度更新
```

---

## Deviations from Plan

**None** - 计划执行完全按照设计：

1. ✓ 创建config/grpo_config.yaml包含所有超参数
2. ✓ 创建GRPOTrainingConfig类包含from_yaml()和to_dict()
3. ✓ 创建grpo/training.py包含所有必需函数
4. ✓ 更新grpo/__init__.py导出新函数
5. ✓ 所有验证测试通过

---

## Usage Examples

### 基本训练
```bash
python grpo/training.py
```

### 指定配置文件
```bash
python grpo/training.py --config config/grpo_config.yaml
```

### 覆盖配置参数
```bash
python grpo/training.py \
    --config config/grpo_config.yaml \
    --output-dir ./my_grpo_model \
    --batch-size 4 \
    --learning-rate 5e-6
```

### 调试模式（限制训练步数）
```bash
python grpo/training.py \
    --config config/grpo_config.yaml \
    --max-steps 10
```

---

## Next Phase Readiness

### Completed
- ✓ 配置系统可以管理所有超参数
- ✓ 训练脚本框架可以加载模型和数据
- ✓ 占位符reward函数允许框架测试
- ✓ CLI参数覆盖支持灵活配置

### Next Steps
- **01-02**: 实现格式检查reward函数
  - 验证JSON格式
  - 验证extend字段
  - 集成到GRPOTrainer

- **01-03**: 实现TSC reward函数
  - SUMO仿真集成
  - 排队车辆数评估
  - 并行仿真处理

- **01-04**: 完整训练流程
  - 组合所有reward函数
  - 端到端训练测试
  - 模型保存和加载验证

### Blockers
无 - 所有基础架构已就绪，可以开始01-02。

---

## Commits

| Commit | Message | Files |
|--------|---------|-------|
| b4a479f | feat(01-01): create GRPO training config and dataclass | config/grpo_config.yaml, grpo/config.py |
| 4b80a62 | feat(01-01): create GRPO training script framework | grpo/training.py |
| 0bcf9a1 | feat(01-01): update grpo module exports | grpo/__init__.py |
