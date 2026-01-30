#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
CONTAINER_NAME="${CONTAINER_NAME:-qwen3-tsc-grpo}"
IMAGE_NAME="${IMAGE_NAME:-qwen3-tsc-grpo}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
DOCKERFILE="${DOCKERFILE:-${SCRIPT_DIR}/Dockerfile}"
RUN_SCRIPT="${RUN_SCRIPT:-Qwen3_TSC_UnslothGRPO_TwoScenarios.py}"
HOST_MODEL_DIR="${HOST_MODEL_DIR:-${PROJECT_DIR}/model}"
HOST_DATA_DIR="${HOST_DATA_DIR:-${PROJECT_DIR}/.tsc-data}"
CONTAINER_WORKDIR="/home/samuel/SCU_TSC"
DETACH="${DETACH:-0}"
DEBUG="${DEBUG:-0}"
LOG_FILE="${PROJECT_DIR}/.docker_run.log"

if [[ "${STOP_EXISTING:-1}" == "1" ]]; then
  existing="$(docker ps -a --filter "name=^/${CONTAINER_NAME}$" --format '{{.Names}}' 2>/dev/null || true)"
  if [[ -n "${existing}" ]]; then
    echo "[publish] removing existing container ${CONTAINER_NAME}"
    docker rm -f "${CONTAINER_NAME}" 2>/dev/null || true
  fi
fi

echo "[publish] checking GPU availability..."
if ! command -v nvidia-smi &>/dev/null; then
  echo "[publish] warning: nvidia-smi not found, GPU may not be available"
fi

echo "[publish] building image ${IMAGE_NAME}:${IMAGE_TAG} from ${DOCKERFILE}"
docker build -t "${IMAGE_NAME}:${IMAGE_TAG}" -f "${DOCKERFILE}" "${SCRIPT_DIR}/.."

if [[ -d "${HOST_MODEL_DIR}" ]]; then
  echo "[publish] model directory exists: ${HOST_MODEL_DIR}"
else
  echo "[publish] creating model directory: ${HOST_MODEL_DIR}"
  mkdir -p "${HOST_MODEL_DIR}"
fi

mkdir -p "${HOST_DATA_DIR}"

echo "[publish] container image: ${IMAGE_NAME}:${IMAGE_TAG}"
echo "[publish] container name: ${CONTAINER_NAME}"
echo "[publish] script to run: ${RUN_SCRIPT}"
echo "[publish] working directory: ${CONTAINER_WORKDIR}"
echo "[publish] shared memory: 32GB"
echo "[publish] ulimit memlock: unlimited"
echo "[publish] ulimit stack: 64MB"

echo ""
echo "=========================================="
echo "CUDA Device Reset Instructions:"
echo "=========================================="
echo "If you encounter RuntimeError about tensors on different devices:"
echo ""
echo "1. Restart kernel in container:"
echo "   docker exec ${CONTAINER_NAME} python -c \"import sys; sys.exit(0)\""
echo ""
echo "2. Stop and restart container:"
echo "   docker rm -f ${CONTAINER_NAME}"
echo "   bash $(readlink -f "${BASH_SOURCE[0]}")"
echo ""
echo "3. Reset GPU (if available):"
echo "   sudo nvidia-smi --reset"
echo "   or"
echo "   sudo systemctl restart nvidia-persistenced"
echo ""
echo "=========================================="
echo ""

docker run \
  --gpus all \
  --name "${CONTAINER_NAME}" \
  --shm-size=32GB \
  --ulimit memlock=-1 \
  --ulimit stack=67108864 \
  --entrypoint /bin/bash \
  -u "$(id -u):$(id -g)" \
  -v "${HOST_MODEL_DIR}:/home/samuel/SCU_TSC/model:rw" \
  -v "${HOST_DATA_DIR}:/home/samuel/SCU_TSC/.tsc-data:rw" \
  -v "${PROJECT_DIR}:${CONTAINER_WORKDIR}:rw" \
  -w "${CONTAINER_WORKDIR}" \
  -e HF_HOME=/home/samuel/SCU_TSC/model \
  -e MODELSCOPE_CACHE=/home/samuel/SCU_TSC/model \
  -e UNSLOTH_USE_MODELSCOPE=1 \
  -e UNSLOTH_VLLM_STANDBY=1 \
  -e SUMO_HOME=/usr/share/sumo \
  "${IMAGE_NAME}:${IMAGE_TAG}" \
  -c "cd ${CONTAINER_WORKDIR} && python ${RUN_SCRIPT}" 2>&1 | tee "${LOG_FILE}"; EXIT_CODE=${PIPESTATUS[0]}

echo ""
echo "[publish] done: ${CONTAINER_NAME}"
echo "[publish] exit code: ${EXIT_CODE}"
echo "[publish] log file: ${LOG_FILE}"
if [[ -f "${LOG_FILE}" && -s "${LOG_FILE}" ]]; then
  echo ""
  echo "=== Last 100 lines of log ==="
  tail -100 "${LOG_FILE}"
fi

docker rm -f "${CONTAINER_NAME}" 2>/dev/null || true
