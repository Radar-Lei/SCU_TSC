# 技术栈研究

**项目:** TSC GRPO训练系统重构
**研究日期:** 2026-02-03
**置信度:** MEDIUM

## 推荐技术栈

### 核心训练框架

| 技术 | 版本 | 用途 | 推荐理由 |
|------|------|------|---------|
| Unsloth | 2025.5+ | LLM快速训练加速 | 提供FastLanguageModel和优化的GRPO Trainer,内存效率高2倍,训练速度快2倍,已在Qwen3_(4B)_GRPO.ipynb中验证可行 |
| TRL (Transformers RL) | 0.22.2+ | 强化学习训练库 | Hugging Face官方RL库,提供GRPOTrainer和GRPOConfig,生态成熟,与Transformers深度集成 |
| PyTorch | 2.0+ | 深度学习框架 | 标准DL框架,Unsloth和TRL的底层依赖,无需更换 |
| Transformers | 4.56+ | 模型加载和推理 | Hugging Face核心库,负责模型加载、tokenizer、chat template |

**关键决策: 使用Unsloth + TRL的组合**
- Unsloth封装了FastLanguageModel.from_pretrained,自动处理量化和LoRA
- TRL提供GRPOTrainer,接受`reward_funcs`参数,支持离线数据训练
- 两者配合使用:Unsloth负责模型优化,TRL负责GRPO算法实现
- 参考实现已验证可行(Qwen3_(4B)_GRPO.ipynb)

### SUMO仿真集成

| 技术 | 版本 | 用途 | 推荐理由 |
|------|------|------|---------|
| TraCI | SUMO 1.19+ | SUMO Python接口 | 项目现有使用,稳定可靠,用于数据生成阶段的仿真运行 |
| LibSUMO | SUMO 1.19+ (可选) | 高性能仿真接口 | 2025年推荐,比TraCI快(无进程间通信),适合大规模数据生成,可作为优化选项 |
| Python-SUMO | 自带 | 网络文件解析 | sumolib库,用于读取路网、解析相位配置 |

**关键决策: 数据生成阶段保留TraCI,可选迁移LibSUMO**
- 当前使用TraCI已稳定,无需立即更换
- 若数据生成速度成为瓶颈,可迁移至LibSUMO(import libsumo as traci,API兼容)
- LibSUMO不支持并行仿真实例,需配合multiprocessing使用

### 数据管道

| 技术 | 版本 | 用途 | 推荐理由 |
|------|------|------|---------|
| Datasets | 2.18+ | 数据集加载和处理 | Hugging Face官方库,与TRL GRPOTrainer深度集成,支持Dataset.from_list快速构建 |
| JSON | 标准库 | 数据存储格式 | 当前使用,简单易调试,适合中小规模数据集(数千到数万条),无需更换 |
| Parquet (可选) | - | 大规模数据存储 | 若数据集超过10万条,可迁移至Parquet(列式存储,压缩率高,加载快),Datasets原生支持 |

**关键决策: 保留JSON格式,超大规模时考虑Parquet**
- 当前JSON格式(grpo_dataset.json)简单直观,便于调试
- Datasets库可直接from_list构建,无需复杂转换
- Parquet优势:压缩率高3-10倍,列式读取快,但需额外转换步骤
- 建议:数据集\u003c5万条时保留JSON,\u003e10万条时迁移Parquet

### 数据生成优化

| 技术 | 版本 | 用途 | 推荐理由 |
|------|------|------|---------|
| multiprocessing | 标准库 | 并行SUMO仿真 | Python标准库,当前已使用,适合并行运行多个SUMO实例 |
| joblib (可选) | 1.3+ | 任务调度 | 更高级的并行库,支持进度条、缓存,可作为multiprocessing的替代 |

**关键决策: 保留multiprocessing,可选升级joblib**
- multiprocessing已满足需求,无需强制更换
- joblib优势:更友好的进度显示(tqdm集成)、任务缓存、异常处理
- 建议:若需更好的监控体验,可迁移joblib.Parallel

### 模型和优化

| 库 | 版本 | 用途 | 何时使用 |
|------|------|------|---------|
| LoRA (通过Unsloth) | - | 参数高效微调 | 所有训练阶段,减少显存占用,加快训练速度 |
| bitsandbytes | 0.43+ | 量化和8bit优化器 | Unsloth依赖,提供adamw_8bit,降低优化器内存 |
| vLLM | 0.8.5+ | 快速推理和生成 | GRPO训练中的候选生成(GRPOTrainer内部使用),SamplingParams配置采样 |
| xformers | 0.0.29+ | 注意力优化 | Unsloth依赖,加速Transformer attention计算 |

**关键决策: 依赖Unsloth自动处理优化**
- Unsloth.FastLanguageModel自动配置LoRA、量化、xformers
- TRL.GRPOTrainer自动使用vLLM进行候选生成
- 开发者只需配置GRPOConfig参数,底层优化由库处理

### 开发工具

| 工具 | 用途 | 备注 |
|------|------|------|
| Docker | 容器化运行环境 | 必须使用,SUMO环境依赖Docker配置,通过docker/publish.sh启动 |
| wandb (可选) | 实验跟踪 | 可选,GRPOConfig.report_to="wandb"启用,记录reward曲线、KL散度等 |
| tensorboard (可选) | 本地可视化 | 可选,轻量级替代wandb,report_to="tensorboard" |

## 安装指南

### 核心依赖
```bash
# Unsloth (包含TRL、Transformers、PyTorch等)
pip install unsloth

# 显式安装特定版本(推荐)
pip install unsloth[colab-new]  # 或直接 pip install unsloth
pip install transformers==4.56.2
pip install trl==0.22.2

# 数据处理
pip install datasets

# SUMO (Docker环境中已安装,无需手动安装)
# 如在本地开发,需安装SUMO 1.19+
```

### 可选依赖
```bash
# 实验跟踪
pip install wandb

# 高级并行
pip install joblib tqdm

# 若迁移Parquet
pip install pyarrow  # Datasets自动使用
```

### Docker环境
```bash
# 启动容器(SUMO环境)
cd docker
./publish.sh

# 容器内训练
docker exec -it <container_name> bash
cd /workspace
python grpo/training.py --config config/training_config.yaml
```

## 架构决策记录

### 为什么使用Unsloth而非原生PyTorch?
- **内存效率**: Unsloth通过梯度检查点、Flash Attention优化,内存占用降低50%
- **训练速度**: 2倍加速,Tesla T4上可训练Qwen2.5-0.5B
- **开箱即用**: FastLanguageModel自动配置LoRA、量化、优化器
- **GRPO支持**: 提供优化的GRPOTrainer(继承自TRL),已在参考实现中验证

### 为什么使用TRL GRPOTrainer而非自实现?
- **算法正确性**: Hugging Face官方实现,经过社区验证
- **生态集成**: 与Transformers、Datasets深度集成,API一致
- **vLLM加速**: 内置vLLM支持,候选生成速度快
- **易维护**: 避免重复造轮子,降低维护成本
- **参考文献**: DeepSeek R1、Qwen等SOTA模型使用相同技术栈

### 为什么数据格式选择JSON而非HDF5?
- **可读性**: JSON人类可读,便于调试和验证数据质量
- **灵活性**: 易于添加新字段(metadata、episode info等),无需重建数据集
- **工具支持**: jq、python json库等生态丰富
- **规模适中**: 项目数据集规模预计数千到数万条,JSON性能足够
- **迁移路径**: 若未来需要,Datasets支持无缝迁移至Parquet

### 为什么保留TraCI而非立即迁移LibSUMO?
- **稳定性**: TraCI在项目中已使用,稳定可靠
- **兼容性**: LibSUMO API与TraCI兼容,迁移成本低
- **并行方案**: LibSUMO不支持多实例,需配合multiprocessing,与当前方案类似
- **性能**: 数据生成是一次性任务,TraCI性能已足够
- **建议**: 若数据生成成为瓶颈,可在优化阶段迁移LibSUMO

## 不推荐使用的技术

| 技术 | 原因 | 替代方案 |
|------|------|---------|
| Stable-Baselines3 | 通用RL库,不适合LLM训练,缺少GRPO支持 | TRL (专为LLM设计) |
| RLlib (Ray) | 过于重量级,增加系统复杂度,学习曲线陡峭 | TRL + Unsloth |
| OpenAI Gym | 通用环境接口,不适合离线数据训练 | 直接使用Datasets |
| PPO (标准) | 相比GRPO样本效率低,训练不稳定 | GRPO (group-based优化) |
| DPO/RLHF | 需要偏好对比数据,不适合连续reward场景 | GRPO (适合数值reward) |
| Flow (SUMO-RL) | 已弃用,社区不活跃 | 自定义SUMO集成(当前方案) |

## 版本兼容性

### 已验证组合(来自Qwen3_(4B)_GRPO.ipynb)
```python
unsloth == 2025.5.7
vllm == 0.8.5.post1  # Unsloth自动安装
transformers == 4.51.3  # 推荐4.56.2
trl == 0.22.2
torch == 2.6.0+cu124
xformers == 0.0.29.post3
bitsandbytes == (自动安装)
```

### 关键兼容性说明
- **Unsloth版本**: 推荐2025.5+,支持Qwen2.5、Llama3等模型
- **TRL版本**: 0.22.2+支持新版GRPOTrainer(completions参数格式)
- **Transformers**: 4.56.2修复了chat template bug,推荐使用
- **CUDA**: 需要CUDA 11.8+,建议12.4
- **GPU**: 最低Tesla T4 (14GB显存),推荐A100/H100

### 冲突避免
- Unsloth与某些transformers版本冲突,建议使用Unsloth推荐的版本
- vLLM版本由Unsloth管理,不要手动指定版本
- bitsandbytes需匹配CUDA版本,通过pip自动安装

## 配置模板

### GRPOConfig (TRL)
```python
from trl import GRPOConfig
from vllm import SamplingParams

# GRPO训练配置
grpo_config = GRPOConfig(
    # 批次和梯度
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,

    # GRPO核心参数
    num_generations=4,          # 每个prompt生成4个候选
    temperature=0.9,            # 采样温度
    beta=0.1,                   # KL散度系数

    # 生成控制
    max_completion_length=50,   # 最大生成长度
    top_p=0.9,
    repetition_penalty=1.0,

    # 训练参数
    learning_rate=1e-5,
    num_train_epochs=3,
    warmup_steps=10,

    # 优化器
    optim="adamw_8bit",

    # 输出
    output_dir="./grpo_model",
    logging_steps=5,
    save_steps=50,

    # 其他
    remove_unused_columns=False,  # 重要:保留state_file等元数据供reward使用
)

# vLLM采样参数(候选生成)
vllm_sampling_params = SamplingParams(
    temperature=1.0,
    top_p=1.0,
    top_k=-1,
    min_p=0.1,
    stop=[tokenizer.eos_token],
)
```

### Unsloth模型加载
```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Qwen2.5-0.5B-Instruct",
    max_seq_length=2048,
    load_in_4bit=False,      # GRPO训练使用16bit
    fast_inference=True,     # 启用vLLM
    gpu_memory_utilization=0.9,
)

# 添加LoRA
model = FastLanguageModel.get_peft_model(
    model,
    r=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_alpha=64,
    use_gradient_checkpointing="unsloth",
)
```

### Datasets格式
```python
from datasets import Dataset

# GRPO期望的格式
grpo_data = [
    {
        "prompt": [  # messages格式
            {"role": "system", "content": "系统提示..."},
            {"role": "user", "content": "输入JSON..."}
        ],
        # 元数据(供reward函数使用)
        "state_file": "/path/to/state.xml",
        "current_green_elapsed": 15.0,
        "min_green": 10.0,
        "max_green": 60.0,
    },
    # ... 更多数据
]

dataset = Dataset.from_list(grpo_data)
```

## 数据流架构

```
SUMO仿真 (数据生成)
    ↓
JSON文件 (grpo_dataset.json)
    ↓
Datasets.from_list (加载)
    ↓
GRPOTrainer (训练循环)
    ├─ vLLM (候选生成)
    ├─ reward_fn (评分)
    └─ 策略更新
    ↓
保存LoRA权重
```

## 性能基准

### Tesla T4 (14GB) - 参考自Qwen3_(4B)_GRPO.ipynb
- **模型**: Qwen2.5-0.5B / Qwen3-4B
- **批次大小**: 1-2 (num_generations=4时effective_batch=4-8)
- **训练速度**: ~1-2 steps/min (包含候选生成和reward计算)
- **显存占用**: ~10-12GB (LoRA rank=32, 16bit训练)
- **数据集**: 1万条数据,训练100 steps约2小时

### 优化建议
- **增加并行度**: 多GPU训练(DDP),线性加速
- **减少生成长度**: max_completion_length=30 (当前决策只需{"extend":"yes/no"})
- **减少候选数**: num_generations=2 (若reward稳定)
- **量化推理**: 使用4bit推理加速候选生成(fast_inference=True)

## 源链接

### 官方文档
- TRL GRPOTrainer: https://github.com/huggingface/trl
- Unsloth: https://github.com/unslothai/unsloth
- Datasets: https://huggingface.co/docs/datasets
- SUMO: https://sumo.dlr.de/docs/

### 参考实现
- Qwen3_(4B)_GRPO.ipynb (项目本地)
- Unsloth GRPO示例: https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Qwen3_(4B)-GRPO.ipynb

### 研究来源
- WebSearch: GRPO reinforcement learning 2025 (LOW confidence - 需验证)
- WebSearch: SUMO Python integration 2025 (MEDIUM confidence - LibSUMO推荐)
- 本地代码分析: grpo/training.py, grpo/dataset_generator.py (HIGH confidence)

---
*技术栈研究 - TSC GRPO训练系统重构*
*研究时间: 2026-02-03*
