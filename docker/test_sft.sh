#!/usr/bin/env bash
set -euo pipefail

################################################################################
# SFT数据生成与训练测试脚本
#
# 用法:
#   ./docker/test_sft.sh
#
# 环境变量配置（可选）：
#   SFT_SAMPLE_SIZE   - SFT数据采样数量 (默认: 500)
#   SFT_MAX_STEPS     - 训练最大步数 (默认: 50，用于快速测试)
#   FULL_TRAINING     - 设为1则进行完整训练 (默认: 0)
################################################################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

# 配置参数
SFT_SAMPLE_SIZE="${SFT_SAMPLE_SIZE:-500}"
SFT_MAX_STEPS="${SFT_MAX_STEPS:-50}"
FULL_TRAINING="${FULL_TRAINING:-0}"

# 容器配置
CONTAINER_NAME="${CONTAINER_NAME:-qwen3-sft-test}"
IMAGE_NAME="${IMAGE_NAME:-qwen3-tsc-grpo}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
DOCKERFILE="${DOCKERFILE:-${SCRIPT_DIR}/Dockerfile}"
CONTAINER_WORKDIR="/home/samuel/SCU_TSC"

# 目录配置
HOST_MODEL_DIR="${HOST_MODEL_DIR:-${PROJECT_DIR}/model}"
HOST_DATA_DIR="${HOST_DATA_DIR:-${PROJECT_DIR}/data}"

# 日志
LOG_FILE="${PROJECT_DIR}/.docker_sft_test.log"

echo ""
echo "=========================================="
echo "SFT数据生成与训练测试"
echo "=========================================="
echo "[test_sft] container: ${CONTAINER_NAME}"
echo "[test_sft] image: ${IMAGE_NAME}:${IMAGE_TAG}"
echo "[test_sft] sample_size: ${SFT_SAMPLE_SIZE}"
echo "[test_sft] max_steps: ${SFT_MAX_STEPS}"
echo "[test_sft] full_training: ${FULL_TRAINING}"
echo "[test_sft] log file: ${LOG_FILE}"
echo "=========================================="
echo ""

# 清理已有容器
existing="$(docker ps -a --filter "name=^/${CONTAINER_NAME}$" --format '{{.Names}}' 2>/dev/null || true)"
if [[ -n "${existing}" ]]; then
  echo "[test_sft] removing existing container ${CONTAINER_NAME}"
  docker rm -f "${CONTAINER_NAME}" 2>/dev/null || true
fi

# 检查镜像是否存在
if ! docker image inspect "${IMAGE_NAME}:${IMAGE_TAG}" &>/dev/null; then
  echo "[test_sft] building image ${IMAGE_NAME}:${IMAGE_TAG}..."
  docker build -t "${IMAGE_NAME}:${IMAGE_TAG}" -f "${DOCKERFILE}" "${SCRIPT_DIR}/.."
fi

# 创建目录
mkdir -p "${HOST_MODEL_DIR}"
mkdir -p "${HOST_DATA_DIR}"

# 构建训练命令
if [[ "${FULL_TRAINING}" == "1" ]]; then
  SFT_TRAIN_CMD="python -m grpo.sft_training"
else
  SFT_TRAIN_CMD="python -m grpo.sft_training --max-steps ${SFT_MAX_STEPS}"
fi

# 运行测试
docker run \
  --gpus all \
  --name "${CONTAINER_NAME}" \
  --shm-size=16GB \
  --user "$(id -u):$(id -g)" \
  --ulimit memlock=-1 \
  --ulimit stack=67108864 \
  --entrypoint /bin/bash \
  -v "${HOST_MODEL_DIR}:/home/samuel/SCU_TSC/model:rw" \
  -v "${HOST_DATA_DIR}:/home/samuel/SCU_TSC/data:rw" \
  -v "${PROJECT_DIR}:${CONTAINER_WORKDIR}:rw" \
  -w "${CONTAINER_WORKDIR}" \
  -e HF_HOME=/home/samuel/SCU_TSC/model \
  -e MODELSCOPE_CACHE=/home/samuel/SCU_TSC/model \
  -e UNSLOTH_USE_MODELSCOPE=1 \
  "${IMAGE_NAME}:${IMAGE_TAG}" \
  -c "
set -e
cd ${CONTAINER_WORKDIR}

echo '=== Step 1/2: 生成SFT数据集 ==='
python -m grpo.generate_sft_dataset --sample-size ${SFT_SAMPLE_SIZE}

echo ''
echo '=== Step 2/2: SFT训练 ==='
${SFT_TRAIN_CMD}

echo ''
echo '=== 测试完成！==='
" 2>&1 | tee "${LOG_FILE}"; EXIT_CODE=${PIPESTATUS[0]}

echo ""
echo "[test_sft] done: ${CONTAINER_NAME}"
echo "[test_sft] exit code: ${EXIT_CODE}"
echo "[test_sft] log file: ${LOG_FILE}"

# 清理容器
docker rm -f "${CONTAINER_NAME}" 2>/dev/null || true

exit ${EXIT_CODE}
