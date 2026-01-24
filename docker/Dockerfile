# =============================================================================
# 基于 gogamza/unsloth-vllm-gb10:latest 的极简 SUMO 增强镜像
# 
# 基础镜像已包含: unsloth, vllm (editable), trl
# 本 Dockerfile 仅添加 Python 包，避免系统依赖冲突
# =============================================================================

ARG BASE_IMAGE=gogamza/unsloth-vllm-gb10:latest
FROM ${BASE_IMAGE}

LABEL maintainer="SCU_TSC"
LABEL description="Unsloth + vLLM + TRL + SUMO for Traffic Signal Control"

# =============================================================================
# 仅安装 Python 依赖（避免系统包影响 vLLM）
# =============================================================================

# 安装项目需要的 Python 包（包括 traci 和 sumolib）
RUN pip install --no-cache-dir \
  traci \
  sumolib \
  pandas \
  matplotlib \
  tqdm \
  pyyaml \
  modelscope \
  && pip cache purge

# =============================================================================
# 设置环境变量
# =============================================================================

# SUMO 环境变量（使用 traci 包自带的 Python 接口，无需系统 SUMO）
ENV SUMO_HOME=/usr/share/sumo
ENV LIBSUMO_AS_TRACI=0

# 默认环境变量
ENV HF_HOME=/workspace/app/model
ENV MODELSCOPE_CACHE=/workspace/app/model
ENV HF_HUB_ENABLE_HF_TRANSFER=1
ENV PYTHONUNBUFFERED=1

# vLLM 环境变量
ENV VLLM_USE_V1=1
ENV VLLM_ATTENTION_BACKEND=FLASHINFER
ENV VLLM_CUDA_GRAPH_MODE=full_and_piecewise
ENV NCCL_IB_DISABLE=0

WORKDIR /workspace/app

# 复制入口脚本
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/bin/bash"]
