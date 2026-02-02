#!/usr/bin/env bash
set -euo pipefail

################################################################################
# GRPO数据生成器测试脚本
#
# 用法:
#   ./docker/test.sh
################################################################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

CONTAINER_NAME="grpo-test"
IMAGE_NAME="${IMAGE_NAME:-qwen3-tsc-grpo}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
DOCKERFILE="${DOCKERFILE:-${SCRIPT_DIR}/Dockerfile}"
CONTAINER_WORKDIR="/home/samuel/SCU_TSC"

# 清理已有容器
docker rm -f "${CONTAINER_NAME}" 2>/dev/null || true

# 构建镜像
echo "[test] building image ${IMAGE_NAME}:${IMAGE_TAG}"
docker build -t "${IMAGE_NAME}:${IMAGE_TAG}" -f "${DOCKERFILE}" "${SCRIPT_DIR}/.."

echo ""
echo "=========================================="
echo "GRPO数据生成器测试 - 并行处理所有场景"
echo "=========================================="

# 运行测试（并行处理所有场景，使用8个进程）
docker run \
  --gpus all \
  --name "${CONTAINER_NAME}" \
  --shm-size=8GB \
  --user "$(id -u):$(id -g)" \ 
  --entrypoint /bin/bash \
  -v "${PROJECT_DIR}:${CONTAINER_WORKDIR}:rw" \
  -w "${CONTAINER_WORKDIR}" \
  -e SUMO_HOME=/usr/share/sumo \
  -e HOME="${HOME}" \
  "${IMAGE_NAME}:${IMAGE_TAG}" \
  -c "cd ${CONTAINER_WORKDIR} && python -m grpo.test_generator --parallel 8 --warmup-steps 100"

EXIT_CODE=$?

echo ""
echo "[test] exit code: ${EXIT_CODE}"

# 清理
docker rm -f "${CONTAINER_NAME}" 2>/dev/null || true

exit ${EXIT_CODE}
