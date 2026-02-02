# Docker 测试脚本使用说明

本文档介绍项目中两个 Docker 测试脚本的使用方法和参数配置。

## 概述

测试脚本按以下顺序执行：

1. **test_init_dataset_generation.sh** - GRPO 数据生成器测试
2. **test_sft.sh** - SFT 数据生成与训练测试

两个测试都使用 Docker 容器运行，需要 GPU 支持。

---

## 前置要求

- Docker 与 NVIDIA Container Toolkit
- CUDA 驱动（支持 GPU）
- SUMO 环境变量 `SUMO_HOME`
- 至少 16GB GPU 显存

---

## 测试一：GRPO 数据生成器测试

### 功能说明

生成交通信号灯控制场景的 GRPO 数据集，测试数据生成流程是否正常工作。

### 脚本位置

```bash
docker/test_init_dataset_generation.sh
```

### 默认行为

- 并行处理所有场景
- 使用 8 个进程
- 预热步数：100

### 环境变量参数

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| `IMAGE_NAME` | `qwen3-tsc-grpo` | Docker 镜像名称 |
| `IMAGE_TAG` | `latest` | Docker 镜像标签 |
| `DOCKERFILE` | `${SCRIPT_DIR}/Dockerfile` | Dockerfile 路径 |

### Python 脚本参数

脚本内部调用 `python -m grpo.test_generator`，支持以下参数：

| 参数 | 默认值 | 说明 |
|-----|--------|------|
| `--parallel` 或 `-p` | 0 | 并行进程数，0 表示使用配置默认值 |
| `--warmup-steps` | 100 | 仿真预热步数 |
| `--single` 或 `-s` | 无 | 只测试单个场景，值为场景名称 |

### 使用示例

```bash
# 使用默认配置运行
./docker/test_init_dataset_generation.sh

# 自定义镜像和标签
IMAGE_NAME=my-grpo-image IMAGE_TAG=v1 ./docker/test_init_dataset_generation.sh

# 只测试单个场景 arterial4x4_1
docker run --gpus all \
  -v "$(pwd):/home/samuel/SCU_TSC:rw" \
  -w /home/samuel/SCU_TSC \
  -e SUMO_HOME=/usr/share/sumo \
  qwen3-tsc-grpo:latest \
  python -m grpo.test_generator --single arterial4x4_1 --warmup-steps 50

# 自定义并行进程数为 4
python -m grpo.test_generator --parallel 4 --warmup-steps 100
```

### 输出说明

- 数据输出目录：`/home/samuel/SCU_TSC/data/grpo_datasets/<场景名>/grpo_dataset.json`

---

## 测试二：SFT 数据生成与训练测试

### 功能说明

从 GRPO 数据集生成 SFT 格式数据，并进行模型微调训练。测试流程包括：
1. 生成 SFT 数据集
2. 使用 Unsloth 进行 LoRA 微调

### 脚本位置

```bash
docker/test_sft.sh
```

### 默认行为

- 生成 500 条 SFT 训练数据
- 快速训练模式（最多 50 步）

### 环境变量参数

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| `SFT_SAMPLE_SIZE` | 500 | SFT 数据采样数量 |
| `SFT_MAX_STEPS` | 50 | 训练最大步数（快速测试模式） |
| `FULL_TRAINING` | 0 | 设为 1 则进行完整训练（无步数限制） |
| `CONTAINER_NAME` | `qwen3-sft-test` | Docker 容器名称 |
| `IMAGE_NAME` | `qwen3-tsc-grpo` | Docker 镜像名称 |
| `IMAGE_TAG` | `latest` | Docker 镜像标签 |
| `DOCKERFILE` | `${SCRIPT_DIR}/Dockerfile` | Dockerfile 路径 |
| `HOST_MODEL_DIR` | `${PROJECT_DIR}/model` | 主机模型目录（挂载点） |
| `HOST_DATA_DIR` | `${PROJECT_DIR}/data` | 主机数据目录（挂载点） |

### 使用示例

```bash
# 使用默认配置运行
./docker/test_sft.sh

# 增加采样数量到 1000 条
SFT_SAMPLE_SIZE=1000 ./docker/test_sft.sh

# 完整训练模式（无步数限制）
FULL_TRAINING=1 ./docker/test_sft.sh

# 自定义容器名称和模型目录
CONTAINER_NAME=my-sft-test HOST_MODEL_DIR=/tmp/my_model ./docker/test_sft.sh

# 自定义镜像版本
IMAGE_TAG=dev ./docker/test_sft.sh
```

### 输出说明

- SFT 数据集：`/home/samuel/SCU_TSC/data/sft_datasets/sft_dataset.json`
- LoRA 模型：`/home/samuel/SCU_TSC/model/sft_model/`
- 合并模型：`/home/samuel/SCU_TSC/model/sft_model/merged/`
- 日志文件：`/home/samuel/SCU_TSC/.docker_sft_test.log`

---

## 完整测试流程

### 顺序执行两个测试

```bash
# 第一步：生成 GRPO 数据
./docker/test_init_dataset_generation.sh

# 第二步：生成 SFT 数据并训练
./docker/test_sft.sh
```

### 自定义完整流程

```bash
# 生成更多 GRPO 数据后进行训练
./docker/test_init_dataset_generation.sh
SFT_SAMPLE_SIZE=1000 SFT_MAX_STEPS=100 ./docker/test_sft.sh
```

---

## 数据流向

```
SUMO 场景
    ↓
test_init_dataset_generation.sh
    ↓
GRPO 数据集 (/home/samuel/SCU_TSC/data/grpo_datasets)
    ↓
test_sft.sh → generate_sft_dataset
    ↓
SFT 数据集 (/home/samuel/SCU_TSC/data/sft_datasets)
    ↓
test_sft.sh → sft_training
    ↓
训练模型 (/home/samuel/SCU_TSC/model/sft_model)
```

---

## 常见问题

### Q: 容器启动失败

检查 GPU 驱动和 NVIDIA Container Toolkit 是否正确安装：
```bash
docker run --gpus all nvidia/cuda:12.0-base-ubuntu22.04 nvidia-smi
```

### Q: 内存不足

确保主机有足够内存，Docker 容器共享内存大小可通过 `--shm-size` 参数调整。

### Q: 训练速度慢

- 减少 `SFT_SAMPLE_SIZE`
- 使用 `SFT_MAX_STEPS` 限制训练步数
- 确保使用 GPU 运行

### Q: 模型下载失败

检查网络连接，或设置代理：
```bash
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=http://proxy:port
```
