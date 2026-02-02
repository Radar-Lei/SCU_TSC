# 架构研究: 离线RL训练系统(GRPO for TSC)

**领域:** 交通信号控制的离线强化学习系统
**研究日期:** 2026-02-03
**置信度:** HIGH

## 推荐架构

### 系统概览

离线RL系统的核心特征是将数据生成与训练分离,实现两阶段流水线:

```
┌─────────────────────────────────────────────────────────────┐
│                   Phase 1: 数据生成阶段                      │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │ SUMO仿真器  │→ │ 决策点采集  │→ │ 双动作模拟  │          │
│  │             │  │             │  │ (延长/切换) │          │
│  └─────────────┘  └─────────────┘  └──────┬──────┘          │
│                                            ↓                 │
│                                    ┌───────────────┐         │
│                                    │ 四元组数据集  │         │
│                                    │ + 状态快照    │         │
│                                    └───────┬───────┘         │
├────────────────────────────────────────────┼─────────────────┤
│                   Phase 2: 训练阶段          ↓                │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │ 数据加载器  │→ │ Reward计算  │→ │ GRPO训练器  │          │
│  │             │  │  (双权重)   │  │  (TRL)      │          │
│  └─────────────┘  └─────────────┘  └──────┬──────┘          │
│                                            ↓                 │
│                                    ┌───────────────┐         │
│                                    │ 优化后的策略  │         │
│                                    └───────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

### 组件职责

| 组件 | 职责 | 典型实现 |
|------|------|---------|
| **数据生成层** | | |
| SUMO仿真器接口 | 管理仿真生命周期,状态保存/加载 | `grpo/sumo_interface.py` (TraCI包装) |
| 决策点检测器 | 识别需要决策的时刻(每5秒或最小绿到达) | `grpo/dataset_generator.py` |
| 双动作执行器 | 对每个决策点运行两次仿真(延长/切换) | 未实现(需新建) |
| 数据序列化器 | 保存四元组+元数据到JSON | `grpo/dataset_generator.py` |
| **训练层** | | |
| 数据集加载器 | 解析JSON,转换为HF Dataset | `grpo/training.py:load_grpo_dataset()` |
| Prompt构造器 | 将排队数据转为LLM输入 | `grpo/prompt_builder.py` |
| Format Reward | 验证模型输出格式(JSON合规性) | `grpo/reward.py:format_reward_fn()` |
| TSC Reward | 基于SUMO仿真计算交通指标奖励 | `grpo/sumo_reward.py` (并行执行) |
| Reward组合器 | 按权重合并format+TSC奖励 | `grpo/reward.py:batch_compute_reward()` |
| GRPO训练器 | 使用TRL库执行group相对策略优化 | `grpo/training.py:train_grpo()` |
| **存储层** | | |
| 状态快照存储 | SUMO `.xml`状态文件 | `data/grpo_datasets/{scenario}/states/` |
| 数据集存储 | JSON格式的训练数据 | `data/grpo_datasets/{scenario}/grpo_dataset.json` |
| 模型检查点 | LoRA权重+合并模型 | `model/grpo_output/` |

## 推荐项目结构

```
grpo/
├── data_generation/        # 数据生成阶段(新建)
│   ├── __init__.py
│   ├── sumo_interface.py   # 移动自grpo/(复用现有)
│   ├── decision_detector.py # 决策点检测逻辑(从dataset_generator.py提取)
│   ├── dual_action_simulator.py # 双动作仿真器(新建核心)
│   └── dataset_serializer.py    # 数据保存(从dataset_generator.py提取)
├── training/               # 训练阶段
│   ├── __init__.py
│   ├── dataset_loader.py   # 数据加载(从training.py提取)
│   ├── reward_calculator.py # Reward函数链(整合reward.py + sumo_reward.py)
│   └── grpo_trainer.py     # 训练入口(从training.py重构)
├── shared/                 # 共享组件
│   ├── __init__.py
│   ├── config.py           # 配置管理(复用现有)
│   └── prompt_builder.py   # Prompt生成(复用现有)
└── scripts/                # 入口脚本
    ├── generate_dataset.py # Phase 1入口
    └── train_grpo.py       # Phase 2入口

data/
├── grpo_datasets/          # 生成的数据集
│   └── {scenario_name}/
│       ├── grpo_dataset.json  # 训练数据
│       └── states/             # SUMO状态快照
│           └── state_*.xml
└── sft_datasets/           # SFT数据(可选,如需预训练)

sumo_simulation/            # SUMO场景定义(保持不变)
└── environments/
    └── {scenario_name}/
        ├── *.net.xml
        ├── *.rou.xml
        └── *.sumocfg
```

### 结构理由

- **`data_generation/`**: 明确分离数据生成逻辑,独立于训练流程,支持离线数据复用
- **`training/`**: 训练阶段仅依赖预生成数据,无SUMO实时调用,简化依赖
- **`shared/`**: config和prompt_builder在两阶段间共享,避免重复
- **`scripts/`**: 清晰的入口点,用户只需运行两个脚本

## 架构模式

### 模式1: 离线数据生成(Offline Data Generation)

**什么:** 将环境交互前置,生成固定数据集,训练时仅读取
**何时使用:** 当仿真环境耗时且状态可复现时
**权衡:**
- **优点**: 训练稳定,可调试,数据可复用,支持分布式训练
- **缺点**: 数据分布固定,无法在线探索,需要大量存储空间

**示例:**
```python
# Phase 1: 数据生成(运行一次)
generator = DataGenerator(sumo_config)
for scenario in scenarios:
    dataset = generator.generate(scenario)
    dataset.save(f"data/{scenario}/dataset.json")

# Phase 2: 训练(可多次运行,调整超参数)
trainer = GRPOTrainer(model, reward_fn)
dataset = load_dataset("data/*/dataset.json")
trainer.train(dataset)
```

### 模式2: 双动作仿真(Dual-Action Simulation)

**什么:** 对每个决策点,提前模拟两种动作的结果,存储为数据
**何时使用:** 当动作空间小(二元决策)且后果可预测时
**权衡:**
- **优点**: 避免训练时实时仿真,Reward计算变为查表操作
- **缺点**: 数据生成时间翻倍,存储需求增加

**示例:**
```python
# 在决策点t,当前排队Q
for decision_point in simulation:
    state_before = get_queue_length()

    # 模拟动作0: 延长当前相位
    state_after_extend = simulate_extend(5_seconds)

    # 模拟动作1: 切换到下一相位
    reset_to(decision_point)  # 回退
    state_after_switch = simulate_switch()

    # 保存四元组
    data.append({
        "state": state_before,
        "next_state_extend": state_after_extend,
        "next_state_switch": state_after_switch,
        "metadata": {...}
    })
```

### 模式3: Reward函数链(Reward Chain)

**什么:** 将Reward分解为多个组件(Format + Domain Metric),按权重组合
**何时使用:** 当需要平衡多个优化目标时
**权衡:**
- **优点**: 灵活调整权重,独立调试各组件,可解释性强
- **缺点**: 需要手动调整权重,可能导致目标冲突

**示例:**
```python
def compute_reward(prompt, output, state_file):
    # 组件1: Format验证
    format_result = format_reward_fn(output)
    if format_result.invalid:
        return -10.0  # 早停

    # 组件2: TSC指标(排队长度)
    decision = extract_decision(output)
    tsc_reward = calculate_queue_reduction(state_file, decision)

    # 加权组合
    final = w_format * format_result.reward + w_tsc * tsc_reward
    return final
```

## 数据流

### 数据生成流(Phase 1)

```
[SUMO仿真启动]
    ↓
[Warmup N步] (让交通流稳定)
    ↓
[主循环: 每步检查]
    ├─ 是否到达决策点? (min_green或每5秒)
    │   ├─ 否 → 继续仿真
    │   └─ 是 ↓
    ├─ 记录当前排队长度 Q_current
    ├─ 保存SUMO状态 → state_t.xml
    ├─ 分支1: 延长相位
    │   ├─ 执行extend_seconds步仿真
    │   ├─ 记录Q_after_extend
    │   └─ 加载state_t.xml(回退)
    ├─ 分支2: 切换相位
    │   ├─ 执行相位切换+仿真
    │   ├─ 记录Q_after_switch
    │   └─ 加载state_t.xml(回退)
    ├─ 保存数据条目:
    │   {
    │     "id": "scenario_tl_time_count",
    │     "prompt": "{JSON格式的状态}",
    │     "state_file": "states/state_t.xml",
    │     "queue_current": Q_current,
    │     "queue_extend": Q_after_extend,
    │     "queue_switch": Q_after_switch,
    │     "metadata": {...}
    │   }
    └─ 继续从state_t.xml仿真
    ↓
[仿真结束] → 保存grpo_dataset.json
```

### 训练流(Phase 2)

```
[加载grpo_dataset.json]
    ↓
[转换为HF Dataset]
    ├─ prompt → messages格式([{role: system, content: ...}, {role: user, content: ...}])
    ├─ 保留queue_*字段(用于reward计算)
    └─ 转换state_file为绝对路径
    ↓
[GRPO训练循环]
    ├─ 采样batch
    ├─ LLM生成多个候选(num_generations=4)
    │   输出: ["{\"extend\": \"yes\"}", "{\"extend\": \"no\"}", ...]
    ├─ Reward计算(并行):
    │   ├─ Format验证(JSON合规性)
    │   │   ├─ 严格: +1.0
    │   │   ├─ 部分: -0.5
    │   │   └─ 无效: -10.0
    │   ├─ TSC Reward(基于预生成数据):
    │   │   decision = extract_decision(output)
    │   │   if decision == "yes":
    │   │       delta = queue_current - queue_extend
    │   │   else:
    │   │       delta = queue_current - queue_switch
    │   │   tsc_reward = delta * reward_scale
    │   └─ 组合: final = w_format * format_r + w_tsc * tsc_r
    ├─ GRPO更新:
    │   ├─ 计算group内相对优势
    │   ├─ 加权策略梯度
    │   └─ KL惩罚(避免偏离参考模型)
    └─ 保存检查点
    ↓
[训练完成] → 导出合并模型
```

### 关键数据流

1. **SUMO状态快照**: 生成时保存,训练时仅在Reward计算时可能加载(如需重新验证)
2. **四元组数据**: 核心训练数据,包含当前状态+两种动作的后果
3. **Messages格式转换**: HuggingFace Dataset → TRL GRPOTrainer期望的格式
4. **Reward缓存**: TSC Reward基于预生成数据查表,无需重新仿真

## 扩展性考虑

| 规模 | 架构调整 |
|-----|----------|
| 0-100条数据 | 单机生成+训练,无需优化 |
| 100-10K条数据 | 并行数据生成(多进程),批量Reward计算 |
| 10K-1M条数据 | 分布式数据生成,数据集分片,Reward计算缓存 |

### 扩展优先级

1. **首要瓶颈**: 数据生成(SUMO仿真慢)
   - 解决方案: 多进程并行生成多个scenario,每个scenario独立SUMO实例
   - 当前实现: `grpo/parallel_runner.py`已支持

2. **次要瓶颈**: Reward计算(训练时并行SUMO调用)
   - 解决方案: 使用预生成数据的四元组,避免实时仿真
   - 目标架构: Reward计算变为纯数学运算(查表+计算排队差)

## 反模式

### 反模式1: 训练时实时SUMO调用

**人们会做:** 在Reward函数中启动SUMO仿真,执行模型决策
**为什么错误:**
- SUMO启动耗时(0.5-2秒/实例)
- 并发上限(端口冲突)
- 训练不稳定(SUMO崩溃导致训练中断)
- 无法复现(仿真随机性)
**正确做法:** 数据生成阶段完成所有SUMO调用,训练时仅读取预生成结果

### 反模式2: 单一Reward函数

**人们会做:** 直接计算TSC指标,忽略Format验证
**为什么错误:**
- 模型可能输出无效格式,导致决策提取失败
- 无法引导模型学习正确的输出格式
- 调试困难(无法区分格式错误vs决策错误)
**正确做法:** 使用Reward链,先验证格式(早停无效输出),再计算Domain Reward

### 反模式3: 状态快照缺失

**人们会做:** 仅保存排队数据,不保存SUMO状态
**为什么错误:**
- 无法验证数据正确性
- 无法调试异常Reward
- 无法扩展到新的Reward函数(如等待时间)
**正确做法:** 定期保存SUMO状态快照,支持回溯验证

## 集成点

### 与现有SUMO设置集成

| 集成点 | 通信方式 | 注意事项 |
|-------|---------|---------|
| SUMO配置文件 | 文件路径(`*.sumocfg`) | 必须包含`<save-state>`配置 |
| TraCI接口 | TCP端口(50000-51000) | 使用端口池避免冲突 |
| 状态文件 | XML文件读写 | 确保路径权限,文件大小可能达到数MB |
| 场景目录 | 目录扫描 | 约定:`sumo_simulation/environments/{scenario}/` |

### 内部边界

| 边界 | 通信 | 考虑事项 |
|-----|------|---------|
| 数据生成 ↔ 训练 | JSON文件 | 使用相对路径(支持迁移),版本化schema |
| Reward组件间 | 函数调用 | Format先行(早停),TSC延迟计算(仅格式有效时) |
| 数据集 ↔ GRPOTrainer | HF Dataset | 保留元数据字段(`remove_unused_columns=False`) |

## 构建顺序建议

基于依赖关系,推荐构建顺序:

1. **数据生成核心**(阻塞后续)
   - `dual_action_simulator.py`: 双动作仿真逻辑
   - 修改`dataset_generator.py`: 集成双动作,保存四元组

2. **数据格式定义**(影响训练层)
   - 确定JSON schema(四元组+元数据)
   - 编写数据验证脚本

3. **Reward重构**(训练核心)
   - 简化`sumo_reward.py`: 移除实时仿真,改为查表
   - 保持`reward.py`的链式结构

4. **训练入口**(集成点)
   - 修改`training.py`: 适配新数据格式
   - 测试端到端流程

5. **验证与优化**(质量保证)
   - 数据分布分析
   - Reward分布可视化
   - 训练曲线监控

## 来源

- **离线RL架构**: 基于现代ML流水线最佳实践(模块化,可复现,数据与训练分离)
- **GRPO实现**: 参考TRL库文档和`Qwen3_(4B)_GRPO.ipynb`结构
- **SUMO集成**: 基于现有`grpo/sumo_interface.py`和TraCI官方文档
- **Reward设计**: 参考RLHF文献(format先行,domain指标后行)

**置信度说明**:
- 数据生成流: HIGH(基于现有`dataset_generator.py`深度分析)
- 训练流: HIGH(基于现有`training.py`和`reward.py`代码验证)
- 扩展性建议: MEDIUM(基于通用ML系统经验,未针对TSC场景实测)

---
*架构研究: TSC离线RL系统*
*研究日期: 2026-02-03*
