#!/usr/bin/env bash
# =============================================================================
# Unsloth TSC GRPO Training - Docker 构建/运行脚本
#
# 用法:
#   ./docker/publish.sh                    # 构建并运行训练
#   RUN=0 ./docker/publish.sh              # 仅构建镜像
#   INTERACTIVE=1 ./docker/publish.sh      # 交互模式（进入 bash）
#   DETACH=1 ./docker/publish.sh           # 后台运行
#
# 环境变量:
#   BASE_IMAGE       - 基础镜像 (默认: nvcr.io/nvidia/pytorch:25.11-py3)
#   PIP_INDEX_URL    - pip 源（传给 Dockerfile 的 build-arg，可选）
#   IMAGE_NAME       - 构建的镜像名 (默认: unsloth-tsc-grpo)
#   IMAGE_TAG        - 镜像标签 (默认: latest)
#   CONTAINER_NAME   - 容器名 (默认: unsloth-tsc-training)
#   RUN              - 是否运行容器 (默认: 1)
#   INTERACTIVE      - 是否交互模式 (默认: 0)
#   DETACH           - 是否后台运行 (默认: 0)
#   STOP_EXISTING    - 是否停止已有同名容器 (默认: 1)
#   GPU_DEVICE       - 使用的 GPU 设备 (默认: all)
#   SCRIPT_NAME      - 要运行的训练脚本 (默认: Qwen3_TSC_UnslothGRPO_TwoScenarios.py)
# =============================================================================

set -euo pipefail

# 获取脚本所在目录和项目根目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

# =============================================================================
# 默认配置
# =============================================================================

BASE_IMAGE="${BASE_IMAGE:-gogamza/unsloth-vllm-gb10:latest}"
PIP_INDEX_URL="${PIP_INDEX_URL:-}"
IMAGE_NAME="${IMAGE_NAME:-unsloth-tsc-grpo}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
CONTAINER_NAME="${CONTAINER_NAME:-unsloth-tsc-training}"

RUN="${RUN:-1}"
INTERACTIVE="${INTERACTIVE:-0}"
DETACH="${DETACH:-0}"
STOP_EXISTING="${STOP_EXISTING:-1}"
AUTO_REMOVE="${AUTO_REMOVE:-0}"

GPU_DEVICE="${GPU_DEVICE:-all}"
SCRIPT_NAME="${SCRIPT_NAME:-Qwen3_TSC_UnslothGRPO_TwoScenarios.py}"

# 数据目录
HOST_MODEL_DIR="${HOST_MODEL_DIR:-${ROOT_DIR}/model}"
HOST_CHECKPOINT_DIR="${HOST_CHECKPOINT_DIR:-${ROOT_DIR}/checkpoints}"
HOST_DATASET_DIR="${HOST_DATASET_DIR:-${ROOT_DIR}/grpo_dataset_two_scenarios}"
HOST_STATE_DIR="${HOST_STATE_DIR:-${ROOT_DIR}/grpo_states_two_scenarios}"

# 日志文件
LOG_FILE="${LOG_FILE:-${ROOT_DIR}/training_log.md}"

# =============================================================================
# 日志初始化
# =============================================================================

# 日志辅助函数
log_msg() {
    echo "$@" | tee -a "${LOG_FILE}"
}

# 添加运行时间戳到日志
{
    echo ""
    echo "============================================================"
    echo "Training Run: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "============================================================"
    echo ""
} >> "${LOG_FILE}"

# =============================================================================
# 预处理：清理已有容器
# =============================================================================

if [[ "${STOP_EXISTING}" == "1" ]]; then
    existing="$(docker ps -a --filter "name=^/${CONTAINER_NAME}$" --format '{{.Names}}' 2>/dev/null || true)"
    if [[ -n "${existing}" ]]; then
        log_msg "[publish] 停止并删除已有容器: ${CONTAINER_NAME}"
        docker rm -f "${CONTAINER_NAME}" 2>/dev/null || true
    fi
fi

# =============================================================================
# 构建镜像
# =============================================================================

log_msg "[publish] 构建镜像 ${IMAGE_NAME}:${IMAGE_TAG}"
log_msg "[publish] 基础镜像: ${BASE_IMAGE}"
if [[ -n "${PIP_INDEX_URL}" ]]; then
    log_msg "[publish] PIP_INDEX_URL: ${PIP_INDEX_URL}"
fi
log_msg "[publish] 项目目录: ${ROOT_DIR}"

build_args=(--build-arg "BASE_IMAGE=${BASE_IMAGE}")
if [[ -n "${PIP_INDEX_URL}" ]]; then
    build_args+=(--build-arg "PIP_INDEX_URL=${PIP_INDEX_URL}")
fi

docker build \
    -f "${SCRIPT_DIR}/Dockerfile" \
    "${build_args[@]}" \
    -t "${IMAGE_NAME}:${IMAGE_TAG}" \
    "${SCRIPT_DIR}" 2>&1 | tee -a "${LOG_FILE}"

log_msg "[publish] 镜像构建完成: ${IMAGE_NAME}:${IMAGE_TAG}"

# =============================================================================
# 运行容器
# =============================================================================

if [[ "${RUN}" != "1" ]]; then
    log_msg "[publish] RUN=0, 跳过容器运行"
    exit 0
fi

# 创建必要的目录
mkdir -p "${HOST_MODEL_DIR}" "${HOST_CHECKPOINT_DIR}"

# 构建运行参数
RUN_ARGS=""

# GPU 配置
if [[ "${GPU_DEVICE}" == "all" ]]; then
    RUN_ARGS+=" --gpus all"
elif [[ -n "${GPU_DEVICE}" ]]; then
    RUN_ARGS+=" --gpus device=${GPU_DEVICE}"
fi

# 挂载项目代码（挂载到 /workspace/app 避免覆盖镜像中的 /workspace/vllm）
RUN_ARGS+=" -v ${ROOT_DIR}:/workspace/app"
RUN_ARGS+=" -w /workspace/app"

# 挂载模型缓存目录
RUN_ARGS+=" -v ${HOST_MODEL_DIR}:/workspace/app/model"

# 挂载 checkpoint 目录
RUN_ARGS+=" -v ${HOST_CHECKPOINT_DIR}:/workspace/app/checkpoints"

# 设置环境变量
RUN_ARGS+=" -e HF_HOME=/workspace/app/model"
RUN_ARGS+=" -e MODELSCOPE_CACHE=/workspace/app/model"
RUN_ARGS+=" -e HF_HUB_ENABLE_HF_TRANSFER=1"
RUN_ARGS+=" -e PYTHONUNBUFFERED=1"

# 使用当前用户运行容器，避免生成 root 权限文件
RUN_ARGS+=" --user $(id -u):$(id -g)"

# 共享内存大小（大模型训练需要）
RUN_ARGS+=" --shm-size=64g"

# IPC 模式
RUN_ARGS+=" --ipc=host"
RUN_ARGS+=" --ulimit memlock=-1"
RUN_ARGS+=" --ulimit stack=67108864"

# vLLM 环境变量
RUN_ARGS+=" -e VLLM_USE_V1=1"
RUN_ARGS+=" -e VLLM_ATTENTION_BACKEND=FLASHINFER"
RUN_ARGS+=" -e VLLM_CUDA_GRAPH_MODE=full_and_piecewise"
RUN_ARGS+=" -e NCCL_IB_DISABLE=0"

# 运行标志
run_flags=()
if [[ "${DETACH}" == "1" ]]; then
    run_flags+=("-d")
fi
if [[ "${AUTO_REMOVE}" == "1" ]]; then
    run_flags+=("--rm")
fi
if [[ "${INTERACTIVE}" == "1" ]]; then
    run_flags+=("-it")
fi

# 确定运行命令
if [[ "${INTERACTIVE}" == "1" ]]; then
    RUN_CMD="/bin/bash"
else
    RUN_CMD="python ${SCRIPT_NAME}"
fi

log_msg ""
log_msg "============================================================"
log_msg "[publish] 运行配置:"
log_msg "  镜像: ${IMAGE_NAME}:${IMAGE_TAG}"
log_msg "  容器名: ${CONTAINER_NAME}"
log_msg "  GPU: ${GPU_DEVICE}"
log_msg "  训练脚本: ${SCRIPT_NAME}"
log_msg "  交互模式: ${INTERACTIVE}"
log_msg "  后台运行: ${DETACH}"
log_msg "  日志文件: ${LOG_FILE}"
log_msg "============================================================"
log_msg ""

# 运行容器
# shellcheck disable=SC2086
if [[ "${INTERACTIVE}" == "1" ]] || [[ "${DETACH}" == "1" ]]; then
    # 交互模式或后台模式不使用 tee（避免干扰交互或后台运行）
    docker run \
        "${run_flags[@]}" \
        --name "${CONTAINER_NAME}" \
        ${RUN_ARGS} \
        "${IMAGE_NAME}:${IMAGE_TAG}" \
        ${RUN_CMD}
else
    # 前台非交互模式：输出到终端并追加到日志文件
    docker run \
        "${run_flags[@]}" \
        --name "${CONTAINER_NAME}" \
        ${RUN_ARGS} \
        "${IMAGE_NAME}:${IMAGE_TAG}" \
        ${RUN_CMD} 2>&1 | tee -a "${LOG_FILE}"
fi

# 如果是后台运行，显示日志提示
if [[ "${DETACH}" == "1" ]]; then
    log_msg ""
    log_msg "[publish] 容器已在后台启动"
    log_msg "[publish] 查看日志: docker logs -f ${CONTAINER_NAME}"
    log_msg "[publish] 进入容器: docker exec -it ${CONTAINER_NAME} bash"
    log_msg "[publish] 停止容器: docker stop ${CONTAINER_NAME}"
fi

log_msg ""
log_msg "[publish] 完成: ${IMAGE_NAME}:${IMAGE_TAG}"

# 记录完成时间到日志
{
    echo ""
    echo "Finished at: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "============================================================"
    echo ""
} >> "${LOG_FILE}"
