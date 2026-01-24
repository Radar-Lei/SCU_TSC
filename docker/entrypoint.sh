#!/usr/bin/env bash
# =============================================================================
# Unsloth TSC GRPO Training - 容器入口脚本
#
# 功能:
#   1. 验证 SUMO 安装
#   2. 验证 Python 依赖
#   3. 设置环境变量
#   4. 执行训练脚本
# =============================================================================

set -e

echo "============================================================"
echo "Unsloth TSC GRPO Training Environment"
echo "============================================================"

# =============================================================================
# 验证 SUMO 安装
# =============================================================================

echo "[entrypoint] 检查 SUMO 安装..."
if command -v sumo &> /dev/null; then
    SUMO_VERSION=$(sumo --version 2>&1 | head -n 1 || echo "unknown")
    echo "[entrypoint] SUMO 已安装: ${SUMO_VERSION}"
else
    echo "[entrypoint] 警告: SUMO 未找到，reward 评估功能可能不可用"
fi

if [[ -z "${SUMO_HOME:-}" ]]; then
    export SUMO_HOME="/usr/share/sumo"
    echo "[entrypoint] 设置 SUMO_HOME=${SUMO_HOME}"
fi

# =============================================================================
# 验证 Python 依赖
# =============================================================================

echo "[entrypoint] 检查 Python 依赖..."

python -c "import torch; print(f'[entrypoint] PyTorch: {torch.__version__}')"
python -c "import transformers; print(f'[entrypoint] Transformers: {transformers.__version__}')"
python -c "import trl; print(f'[entrypoint] TRL: {trl.__version__}')"
python -c "import unsloth; print('[entrypoint] Unsloth: OK')" 2>/dev/null || echo "[entrypoint] Unsloth: (version check skipped)"

# 检查 CUDA
python -c "
import torch
if torch.cuda.is_available():
    print(f'[entrypoint] CUDA: {torch.version.cuda}')
    print(f'[entrypoint] GPU: {torch.cuda.get_device_name(0)}')
    print(f'[entrypoint] GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB')
else:
    print('[entrypoint] 警告: CUDA 不可用')
"

# 检查 traci（SUMO Python 接口）
python -c "import traci; print('[entrypoint] traci: OK')" 2>/dev/null || echo "[entrypoint] 警告: traci 未安装"

# =============================================================================
# 设置环境变量
# =============================================================================

# HuggingFace 配置
export HF_HOME="${HF_HOME:-/workspace/model}"
export MODELSCOPE_CACHE="${MODELSCOPE_CACHE:-/workspace/model}"
export HF_HUB_ENABLE_HF_TRANSFER="${HF_HUB_ENABLE_HF_TRANSFER:-1}"

# Python 配置
export PYTHONUNBUFFERED=1
export PYTHONPATH="${PYTHONPATH:-}:/workspace"

echo "[entrypoint] HF_HOME=${HF_HOME}"
echo "[entrypoint] 工作目录: $(pwd)"

# =============================================================================
# 显示项目文件
# =============================================================================

echo ""
echo "[entrypoint] 项目文件:"
ls -la /workspace/app/*.py 2>/dev/null | head -10 || echo "  (无 Python 文件)"

# =============================================================================
# 执行命令
# =============================================================================

echo ""
echo "============================================================"
echo "[entrypoint] 执行: $@"
echo "============================================================"
echo ""

exec "$@"
