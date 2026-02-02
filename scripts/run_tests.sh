#!/bin/bash
# Docker容器内测试执行脚本
#
# 自动化docker容器内的pytest测试执行，支持单元/集成测试过滤
#
# 用法:
#   ./scripts/run_tests.sh [选项]
#
# 选项:
#   -u, --unit-only      只运行单元测试（跳过SUMO依赖）
#   -i, --integration    只运行集成测试（需要SUMO）
#   -a, --all            运行所有测试（默认）
#   -k, --keep-going     遇到失败继续运行
#   -v, --verbose        详细输出
#   -h, --help           显示帮助信息

set -euo pipefail

# ==================== 默认配置 ====================

# Docker容器配置
CONTAINER_NAME="${CONTAINER_NAME:-qwen3-tsc-grpo}"
CONTAINER_WORKDIR="${CONTAINER_WORKDIR:-/home/samuel/SCU_TSC}"

# 测试配置
PYTEST_CMD="python -m pytest"
PYTEST_ARGS="-v"
TEST_PATTERN="tests/"

# 运行模式
MODE="all"  # all, unit, integration
KEEP_GOING=false

# ==================== 帮助信息 ====================

show_help() {
    cat << EOF
Docker容器内测试执行脚本

用法: $(basename "$0") [选项]

选项:
    -u, --unit-only      只运行单元测试（跳过SUMO依赖）
    -i, --integration    只运行集成测试（需要SUMO）
    -a, --all            运行所有测试（默认）
    -k, --keep-going     遇到失败继续运行（使用 --maxfail=999）
    -v, --verbose        详细输出（添加 -vv 到pytest）
    -h, --help           显示此帮助信息

环境变量:
    CONTAINER_NAME       Docker容器名称（默认: qwen3-tsc-grpo）
    CONTAINER_WORKDIR    容器内工作目录（默认: /home/samuel/SCU_TSC）

示例:
    # 运行所有测试
    $(basename "$0")

    # 只运行单元测试
    $(basename "$0") -u

    # 只运行集成测试
    $(basename "$0") -i

    # 遇到失败继续运行
    $(basename "$0") -a -k

    # 使用自定义容器名称
    CONTAINER_NAME=my-container $(basename "$0") -u

EOF
}

# ==================== 参数解析 ====================

while [[ $# -gt 0 ]]; do
    case $1 in
        -u|--unit-only)
            MODE="unit"
            shift
            ;;
        -i|--integration)
            MODE="integration"
            shift
            ;;
        -a|--all)
            MODE="all"
            shift
            ;;
        -k|--keep-going)
            KEEP_GOING=true
            shift
            ;;
        -v|--verbose)
            PYTEST_ARGS="$PYTEST_ARGS -vv"
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "错误: 未知选项 $1"
            echo "使用 -h 查看帮助"
            exit 1
            ;;
    esac
done

# ==================== Docker检查 ====================

echo "========================================"
echo "Docker测试执行脚本"
echo "========================================"
echo ""

# 检查docker是否可用
if ! command -v docker &> /dev/null; then
    echo "错误: docker命令未找到"
    echo "请确保docker已安装且在PATH中"
    exit 1
fi

# 检查容器是否运行
if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "错误: Docker容器 '${CONTAINER_NAME}' 未运行"
    echo ""
    echo "请先启动容器:"
    echo "  docker start ${CONTAINER_NAME}"
    echo ""
    echo "或使用docker/publish.sh启动完整的训练环境"
    exit 1
fi

echo "✓ 找到运行中的容器: ${CONTAINER_NAME}"
echo ""

# ==================== 构建pytest命令 ====================

case $MODE in
    unit)
        echo "运行模式: 单元测试（-m 'not integration'）"
        MARKER_EXPR='-m "not integration"'
        ;;
    integration)
        echo "运行模式: 集成测试（-m integration）"
        MARKER_EXPR='-m integration'
        ;;
    all)
        echo "运行模式: 所有测试"
        MARKER_EXPR=""
        ;;
    *)
        echo "错误: 未知模式 ${MODE}"
        exit 1
        ;;
esac

if [ "$KEEP_GOING" = true ]; then
    echo "失败处理: 继续运行 (--maxfail=999)"
    MAXFAIL_ARG="--maxfail=999"
else
    MAXFAIL_ARG=""
fi

echo ""

# 构建完整的pytest命令
PYTEST_FULL_CMD="${PYTEST_CMD} ${TEST_PATTERN} ${PYTEST_ARGS} ${MARKER_EXPR} ${MAXFAIL_ARG}"

echo "执行命令:"
echo "  ${PYTEST_FULL_CMD}"
echo ""
echo "========================================"
echo ""

# ==================== 执行测试 ====================

# 在容器中执行pytest
docker exec "${CONTAINER_NAME}" bash -c \
    "cd ${CONTAINER_WORKDIR} && ${PYTEST_FULL_CMD}"

TEST_EXIT_CODE=$?

# ==================== 结果处理 ====================

echo ""
echo "========================================"

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "✓ 所有测试通过！"
    exit 0
else
    echo "✗ 测试失败 (退出码: ${TEST_EXIT_CODE})"
    exit $TEST_EXIT_CODE
fi
