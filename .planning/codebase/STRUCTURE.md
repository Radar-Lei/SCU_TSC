# Codebase Structure

**Analysis Date:** 2025-02-02

## Directory Layout

```
/home/samuel/SCU_TSC/
├── grpo/                    # GRPO数据生成和训练模块
│   ├── __init__.py          # 模块初始化，导出config
│   ├── config.py            # 配置类 (GRPOConfig) 和系统提示词模板
│   ├── dataset_generator.py # 核心数据生成器 (GRPODatasetGenerator)
│   ├── generate_grpo_dataset.py  # GRPO数据生成入口脚本
│   ├── generate_sft_dataset.py   # SFT数据集转换脚本
│   ├── parallel_runner.py   # 并行执行器 (ParallelRunner)
│   ├── prompt_builder.py    # Prompt构建工具函数
│   ├── sft_training.py      # SFT训练脚本
│   ├── sumo_interface.py    # SUMO TraCI接口封装 (SUMOInterface)
│   └── test_generator.py    # 测试脚本
├── sumo_simulation/         # SUMO仿真相关
│   ├── environments/        # 仿真场景目录 (arterial4x4_*, chengdu等)
│   ├── arterial4x4/         # 旧版场景目录 (多个子目录)
│   ├── .venv/               # Python虚拟环境
│   ├── pyproject.toml       # Python项目配置
│   └── sumo_simulator.py    # 完整的SUMO仿真器类 (SUMOSimulator)
├── data/                    # 数据存储目录
│   ├── grpo_datasets/       # GRPO数据集输出 (按场景分组)
│   └── sft_datasets/        # SFT数据集输出
├── model/                   # 模型输出目录
│   └── sft_model/           # 训练后的SFT模型
├── docker/                  # Docker配置
│   ├── Dockerfile           # 基于unsloth/unsloth的镜像
│   ├── entrypoint.sh        # 容器入口脚本
│   ├── publish.sh           # 镜像发布脚本
│   ├── test_init_dataset_generation.sh  # 数据生成测试脚本
│   ├── test_sft.sh          # SFT训练测试脚本
│   └── README.md            # Docker使用说明
├── unsloth_compiled_cache/  # Unsloth编译缓存 (自动生成)
│   ├── UnslothGRPOTrainer.py  # GRPO训练器编译缓存
│   ├── UnslothSFTTrainer.py   # SFT训练器编译缓存
│   └── ... (其他RL算法训练器缓存)
├── .planning/               # 项目规划文档目录
│   └── codebase/            # 代码库分析文档
├── convert_to_gguf.py       # GGUF格式转换工具
├── rou_month_generator.py   # 月份路线生成器
└── Qwen3_(4B)_GRPO.ipynb    # Jupyter notebook (实验/分析)
```

## Directory Purposes

**grpo/**:
- Purpose: GRPO (Group Relative Policy Optimization) 数据生成和SFT训练核心模块
- Contains: 数据生成器、SUMO接口、配置管理、训练脚本
- Key files: `dataset_generator.py`, `sumo_interface.py`, `sft_training.py`

**sumo_simulation/environments/**:
- Purpose: SUMO仿真场景定义文件存储
- Contains: `.sumocfg` 配置文件, `.net.xml` 网络文件, 路线文件
- Key files: `arterial4x4_90/`, `arterial4x4_91/`, ..., `chengdu/`

**sumo_simulation/arterial4x4/**:
- Purpose: 旧版场景目录 (多个arterial4x4变体)
- Contains: 场景编号子目录 (如 arterial4x4_297/, arterial4x4_361/)
- Generated: 仿真场景数据文件

**data/grpo_datasets/**:
- Purpose: GRPO数据集输出目录
- Contains: 按场景分组的子目录，每个包含 `grpo_dataset.json` 和 `states/` 目录
- Generated: 由 `generate_grpo_dataset.py` 生成

**data/sft_datasets/**:
- Purpose: SFT训练数据集输出目录
- Contains: `sft_dataset.json` 和 `sft_dataset.jsonl`
- Generated: 由 `generate_sft_dataset.py` 生成

**model/**:
- Purpose: 训练模型输出目录
- Contains: SFT训练保存的LoRA模型和合并后的模型
- Generated: 由 `sft_training.py` 生成

**docker/**:
- Purpose: Docker容器化配置
- Contains: Dockerfile、测试脚本、发布脚本
- Key files: `Dockerfile`, `test_sft.sh`, `test_init_dataset_generation.sh`

**unsloth_compiled_cache/**:
- Purpose: Unsloth库自动生成的JIT编译缓存
- Contains: 各种RL算法训练器的编译缓存
- Generated: Unsloth运行时自动生成，不应手动修改

## Key File Locations

**Entry Points:**
- `/home/samuel/SCU_TSC/grpo/generate_grpo_dataset.py`: GRPO数据生成主入口
- `/home/samuel/SCU_TSC/grpo/generate_sft_dataset.py`: SFT数据集转换入口
- `/home/samuel/SCU_TSC/grpo/sft_training.py`: SFT训练入口

**Configuration:**
- `/home/samuel/SCU_TSC/grpo/config.py`: GRPO配置类和系统提示词
- `/home/samuel/SCU_TSC/sumo_simulation/pyproject.toml`: Python依赖配置

**Core Logic:**
- `/home/samuel/SCU_TSC/grpo/dataset_generator.py`: 数据生成核心逻辑
- `/home/samuel/SCU_TSC/grpo/sumo_interface.py`: SUMO接口封装
- `/home/samuel/SCU_TSC/grpo/prompt_builder.py`: Prompt构建工具

**Testing:**
- `/home/samuel/SCU_TSC/grpo/test_generator.py`: 数据生成器测试
- `/home/samuel/SCU_TSC/docker/test_sft.sh`: SFT训练Docker测试
- `/home/samuel/SCU_TSC/docker/test_init_dataset_generation.sh`: 数据生成Docker测试

**Simulation:**
- `/home/samuel/SCU_TSC/sumo_simulation/sumo_simulator.py`: 完整的SUMO仿真器 (遗留代码，部分功能被grpo/sumo_interface.py替代)

## Naming Conventions

**Files:**
- 模块文件: `lowercase_with_underscores.py` (如 `dataset_generator.py`, `sumo_interface.py`)
- 入口脚本: `verb_noun.py` (如 `generate_grpo_dataset.py`, `generate_sft_dataset.py`)
- 测试脚本: `test_<module>.py` (如 `test_generator.py`)
- 配置文件: `config.py` 或 `<name>.toml` (如 `pyproject.toml`)

**Directories:**
- 功能模块: `lowercase` (如 `grpo/`, `docker/`)
- 数据输出: `plural_noun` (如 `datasets/`, `models/`)
- 仿真场景: `pattern_number` (如 `arterial4x4_90/`, `arterial4x4_91/`)

**Classes:**
- 驼峰命名: `GRPODatasetGenerator`, `SUMOInterface`, `ParallelRunner`
- 数据类: `@dataclass class Name` (如 `GRPODataEntry`, `PhaseInfo`, `GRPOConfig`)

**Functions:**
- 下划线命名: `generate_for_scenario()`, `build_extend_decision_prompt()`, `load_sft_dataset()`
- 私有方法: `_method_name()` (如 `_run_collection_loop()`, `_find_sumocfg()`)

**Constants:**
- 全大写下划线: `DEFAULT_CONFIG`, `SYSTEM_PROMPT`

## Where to Add New Code

**New GRPO Scenario/Data Processing:**
- Primary code: `/home/samuel/SCU_TSC/grpo/dataset_generator.py`
- Add new methods to `GRPODatasetGenerator` class

**New SUMO Interface Methods:**
- Primary code: `/home/samuel/SCU_TSC/grpo/sumo_interface.py`
- Add new methods to `SUMOInterface` class

**New Training Pipeline (e.g., DPO, PPO):**
- Implementation: `/home/samuel/SCU_TSC/grpo/<name>_training.py`
- Follow pattern of `sft_training.py`: argument parsing, dataset loading, training function

**New Prompt Templates:**
- Implementation: `/home/samuel/SCU_TSC/grpo/prompt_builder.py`
- Add new `build_<type>_prompt()` function

**New Configuration Options:**
- Implementation: `/home/samuel/SCU_TSC/grpo/config.py`
- Add fields to `GRPOConfig` dataclass

**New SUMO Scenarios:**
- Simulation files: `/home/samuel/SCU_TSC/sumo_simulation/environments/<scenario_name>/`
- Required: `<scenario_name>.sumocfg`, `<scenario_name>.net.xml`

**Utilities:**
- Shared helpers: `/home/samuel/SCU_TSC/grpo/<utility_name>.py`
- Import in needed modules

## Special Directories

**unsloth_compiled_cache/**:
- Purpose: Unsloth JIT编译缓存，加速训练器初始化
- Generated: 是，由Unsloth自动生成
- Committed: 是，缓存已提交到仓库以加速冷启动

**sumo_simulation/.venv/**:
- Purpose: Python虚拟环境 (用于sumo_simulation/目录的独立开发)
- Generated: 是
- Committed: 否，通常在 .gitignore 中

**data/**:
- Purpose: 训练数据和模型输出
- Generated: 是
- Committed: 部分，数据集通常提交，模型checkpoint可能不提交

**.planning/**:
- Purpose: 项目规划和代码库分析文档
- Generated: 否，人工维护
- Committed: 是

---

*Structure analysis: 2025-02-02*
