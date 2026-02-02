#!/usr/bin/env bash
set -euo pipefail

################################################################################
# CLI参数覆盖测试脚本
#
# 用法:
#   ./docker/test_cli_override.sh
################################################################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

# 容器配置
CONTAINER_NAME="${CONTAINER_NAME:-qwen3-cli-test}"
IMAGE_NAME="${IMAGE_NAME:-qwen3-tsc-grpo}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
DOCKERFILE="${DOCKERFILE:-${SCRIPT_DIR}/Dockerfile}"
CONTAINER_WORKDIR="/home/samuel/SCU_TSC"

echo ""
echo "=========================================="
echo "CLI参数覆盖测试"
echo "=========================================="
echo "[test_cli] container: ${CONTAINER_NAME}"
echo "[test_cli] image: ${IMAGE_NAME}:${IMAGE_TAG}"
echo "=========================================="
echo ""

# 清理已有容器
existing="$(docker ps -a --filter "name=^/${CONTAINER_NAME}$" --format '{{.Names}}' 2>/dev/null || true)"
if [[ -n "${existing}" ]]; then
  echo "[test_cli] removing existing container ${CONTAINER_NAME}"
  docker rm -f "${CONTAINER_NAME}" 2>/dev/null || true
fi

# 检查镜像是否存在
if ! docker image inspect "${IMAGE_NAME}:${IMAGE_TAG}" &>/dev/null; then
  echo "[test_cli] building image ${IMAGE_NAME}:${IMAGE_TAG}..."
  docker build -t "${IMAGE_NAME}:${IMAGE_TAG}" -f "${DOCKERFILE}" "${SCRIPT_DIR}/.."
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
  -v "${PROJECT_DIR}:${CONTAINER_WORKDIR}:rw" \
  -w "${CONTAINER_WORKDIR}" \
  "${IMAGE_NAME}:${IMAGE_TAG}" \
  -c "
set -e
cd ${CONTAINER_WORKDIR}

echo '=== 测试CLI参数覆盖 ==='
python -m grpo.test_cli_override

echo ''
echo '=== 测试完成！==='
" 2>&1

EXIT_CODE=$?

echo ""
echo "[test_cli] done: ${CONTAINER_NAME}"
echo "[test_cli] exit code: ${EXIT_CODE}"

# 清理容器
docker rm -f "${CONTAINER_NAME}" 2>/dev/null || true

exit ${EXIT_CODE}
