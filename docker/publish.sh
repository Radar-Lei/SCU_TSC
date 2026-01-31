#!/usr/bin/env bash
set -euo pipefail

################################################################################
# GRPO信控模型训练 - 一键运行脚本
#
# 完整流程：GRPO数据生成 -> SFT数据生成 -> SFT训练 -> GRPO训练
#
# 用法:
#   ./docker/publish.sh
#
# 配置参数（通过环境变量）：
#   PARALLEL       - 并行进程数 (默认: 4)
#   EXTEND_SECONDS - 决策延长秒数 (默认: 5)
#   WARMUP_STEPS   - 预热步数 (默认: 300)
#   SCENARIOS      - 场景列表，逗号分隔 (默认: 空=所有场景)
################################################################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

# 容器配置
CONTAINER_NAME="${CONTAINER_NAME:-qwen3-tsc-grpo}"
IMAGE_NAME="${IMAGE_NAME:-qwen3-tsc-grpo}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
DOCKERFILE="${DOCKERFILE:-${SCRIPT_DIR}/Dockerfile}"
CONTAINER_WORKDIR="/home/samuel/SCU_TSC"

# 目录配置
HOST_MODEL_DIR="${HOST_MODEL_DIR:-${PROJECT_DIR}/model}"
HOST_DATA_DIR="${HOST_DATA_DIR:-${PROJECT_DIR}/data}"

# GRPO生成配置
PARALLEL="${PARALLEL:-4}"
EXTEND_SECONDS="${EXTEND_SECONDS:-5}"
WARMUP_STEPS="${WARMUP_STEPS:-300}"
SCENARIOS="${SCENARIOS:-}"

# 日志
LOG_FILE="${PROJECT_DIR}/.docker_run.log"

# 清理已有容器
if [[ "${STOP_EXISTING:-1}" == "1" ]]; then
  existing="$(docker ps -a --filter "name=^/${CONTAINER_NAME}$" --format '{{.Names}}' 2>/dev/null || true)"
  if [[ -n "${existing}" ]]; then
    echo "[publish] removing existing container ${CONTAINER_NAME}"
    docker rm -f "${CONTAINER_NAME}" 2>/dev/null || true
  fi
fi

# 检查GPU
echo "[publish] checking GPU availability..."
if ! command -v nvidia-smi &>/dev/null; then
  echo "[publish] warning: nvidia-smi not found, GPU may not be available"
fi

# 构建镜像
echo "[publish] building image ${IMAGE_NAME}:${IMAGE_TAG} from ${DOCKERFILE}"
docker build -t "${IMAGE_NAME}:${IMAGE_TAG}" -f "${DOCKERFILE}" "${SCRIPT_DIR}/.."

# 创建目录
mkdir -p "${HOST_MODEL_DIR}"
mkdir -p "${HOST_DATA_DIR}"

# 构建运行命令
if [[ -n "${SCENARIOS}" ]]; then
  GRPO_GENERATE_CMD="python -m grpo.generate_grpo_dataset --scenarios ${SCENARIOS} --parallel ${PARALLEL} --extend-seconds ${EXTEND_SECONDS} --warmup-steps ${WARMUP_STEPS}"
else
  GRPO_GENERATE_CMD="python -m grpo.generate_grpo_dataset --all --parallel ${PARALLEL} --extend-seconds ${EXTEND_SECONDS} --warmup-steps ${WARMUP_STEPS}"
fi

echo ""
echo "=========================================="
echo "GRPO信控模型训练 - 完整流程"
echo "=========================================="
echo "[publish] container: ${CONTAINER_NAME}"
echo "[publish] image: ${IMAGE_NAME}:${IMAGE_TAG}"
echo "[publish] parallel: ${PARALLEL}"
echo "[publish] extend_seconds: ${EXTEND_SECONDS}"
echo "[publish] warmup_steps: ${WARMUP_STEPS}"
echo "[publish] scenarios: ${SCENARIOS:-all}"
echo "[publish] log file: ${LOG_FILE}"
echo "=========================================="
echo ""

# 运行完整流程
docker run \
  --gpus all \
  --name "${CONTAINER_NAME}" \
  --shm-size=32GB \
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
  -e UNSLOTH_VLLM_STANDBY=1 \
  -e SUMO_HOME=/usr/share/sumo \
  "${IMAGE_NAME}:${IMAGE_TAG}" \
  -c "
set -e
cd ${CONTAINER_WORKDIR}

echo '=== Step 1/4: 生成GRPO数据集 ==='
${GRPO_GENERATE_CMD}

echo '=== Step 2/4: 生成SFT数据集 ==='
python -m grpo.generate_sft_dataset

echo '=== Step 3/4: SFT训练 ==='
python -m grpo.sft_training

echo '=== Step 4/4: GRPO训练 ==='
python -m grpo.grpo_training

echo '=== 完成！==='
" 2>&1 | tee "${LOG_FILE}"; EXIT_CODE=${PIPESTATUS[0]}

echo ""
echo "[publish] done: ${CONTAINER_NAME}"
echo "[publish] exit code: ${EXIT_CODE}"
echo "[publish] log file: ${LOG_FILE}"

if [[ -f "${LOG_FILE}" && -s "${LOG_FILE}" ]]; then
  echo ""
  echo "=== Last 50 lines of log ==="
  tail -50 "${LOG_FILE}"
fi

# 清理容器
docker rm -f "${CONTAINER_NAME}" 2>/dev/null || true
