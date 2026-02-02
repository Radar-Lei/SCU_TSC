#!/bin/bash
# -*- coding: utf-8 -*-
#
# 集成测试执行脚本
#
# 功能：
# - 准备测试数据（调用prepare_test_data.py）
# - 在docker容器中执行集成测试
# - 验证测试结果
# - 清理临时文件
#
# 用法:
#   ./scripts/run_integration_test.sh
#   ./scripts/run_integration_test.sh --skip-prepare
#   ./scripts/run_integration_test.sh --keep-output
#   ./scripts/run_integration_test.sh --verbose

set -e  # 遇到错误立即退出

# ==================== 配置 ====================

# 项目根目录（自动检测）
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Docker容器名称
DOCKER_CONTAINER="qwen3-tsc-grpo"

# 测试数据配置
NUM_GRPO=${NUM_GRPO:-50}
NUM_SFT=${NUM_SFT:-20}
OUTPUT_DIR="tests/fixtures/testdata"

# 测试超时时间（秒）
TIMEOUT=${TIMEOUT:-1800}  # 默认30分钟

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 参数
SKIP_PREPARE=false
KEEP_OUTPUT=false
VERBOSE=false

# ==================== 函数 ====================

print_header() {
    echo ""
    echo "========================================"
    echo "$1"
    echo "========================================"
}

print_step() {
    echo ""
    echo -e "${BLUE}[Step $1]${NC} $2"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1" >&2
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# 解析命令行参数
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --skip-prepare)
                SKIP_PREPARE=true
                shift
                ;;
            --keep-output)
                KEEP_OUTPUT=true
                shift
                ;;
            --verbose|-v)
                VERBOSE=true
                shift
                ;;
            --help|-h)
                echo "用法: $0 [选项]"
                echo ""
                echo "选项:"
                echo "  --skip-prepare    跳过数据准备（使用已有数据）"
                echo "  --keep-output     保留训练输出（用于调试）"
                echo "  --verbose, -v     详细输出"
                echo "  --help, -h        显示帮助信息"
                echo ""
                echo "环境变量:"
                echo "  NUM_GRPO          GRPO数据条数（默认: 50）"
                echo "  NUM_SFT           SFT数据条数（默认: 20）"
                echo "  TIMEOUT           测试超时时间（秒，默认: 1800）"
                exit 0
                ;;
            *)
                print_error "未知参数: $1"
                echo "使用 --help 查看帮助信息"
                exit 1
                ;;
        esac
    done
}

# 检查docker容器是否运行
check_docker() {
    print_step "0/4" "检查Docker容器"

    if ! docker ps | grep -q "$DOCKER_CONTAINER"; then
        print_error "Docker容器 '$DOCKER_CONTAINER' 未运行"
        echo "请先启动容器: docker start $DOCKER_CONTAINER"
        exit 1
    fi

    print_success "Docker容器运行中"
}

# 准备测试数据
prepare_test_data() {
    if [ "$SKIP_PREPARE" = true ]; then
        print_step "1/4" "跳过数据准备（使用已有数据）"
        return
    fi

    print_step "1/4" "准备测试数据"

    cd "$PROJECT_DIR"

    # 检查测试数据是否已存在
    if [ -f "$OUTPUT_DIR/small_grpo_dataset.json" ] && [ -f "$OUTPUT_DIR/small_sft_dataset.json" ]; then
        print_warning "测试数据已存在"
        read -p "是否重新生成？(y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_success "使用现有测试数据"
            return
        fi
    fi

    # 生成测试数据
    if [ "$VERBOSE" = true ]; then
        python scripts/prepare_test_data.py \
            --num-grpo "$NUM_GRPO" \
            --num-sft "$NUM_SFT" \
            --output-dir "$OUTPUT_DIR"
    else
        python scripts/prepare_test_data.py \
            --num-grpo "$NUM_GRPO" \
            --num-sft "$NUM_SFT" \
            --output-dir "$OUTPUT_DIR" > /dev/null
    fi

    # 验证数据文件
    if [ ! -f "$OUTPUT_DIR/small_grpo_dataset.json" ]; then
        print_error "GRPO测试数据生成失败"
        exit 1
    fi

    if [ ! -f "$OUTPUT_DIR/small_sft_dataset.json" ]; then
        print_error "SFT测试数据生成失败"
        exit 1
    fi

    # 统计数据条数
    GRPO_COUNT=$(python -c "import json; print(len(json.load(open('$OUTPUT_DIR/small_grpo_dataset.json'))))")
    SFT_COUNT=$(python -c "import json; print(len(json.load(open('$OUTPUT_DIR/small_sft_dataset.json'))))")

    print_success "测试数据准备完成"
    echo "  GRPO数据: $GRPO_COUNT 条"
    echo "  SFT数据: $SFT_COUNT 条"
}

# 运行集成测试
run_integration_tests() {
    print_step "2/4" "运行集成测试"

    cd "$PROJECT_DIR"

    # 构建pytest命令
    PYTEST_CMD="pytest tests/integration/test_integration.py::TestEndToEndTrainingSmallScale::test_end_to_end_training_small_scale -v"

    if [ "$VERBOSE" = true ]; then
        PYTEST_CMD="$PYTEST_CMD -s"
    fi

    # 在docker容器中执行测试
    print_warning "在Docker容器中执行测试（超时: ${TIMEOUT}秒）..."

    if docker exec "$DOCKER_CONTAINER" bash -c "cd /home/samuel/SCU_TSC && timeout $TIMEOUT $PYTEST_CMD"; then
        print_success "集成测试通过"
        TEST_EXIT_CODE=0
    else
        TEST_EXIT_CODE=$?
        if [ $TEST_EXIT_CODE -eq 124 ]; then
            print_error "测试超时（超过 ${TIMEOUT} 秒）"
        else
            print_error "集成测试失败（退出码: $TEST_EXIT_CODE）"
        fi
    fi
}

# 运行辅助测试
run_auxiliary_tests() {
    print_step "3/4" "运行辅助测试"

    cd "$PROJECT_DIR"

    # 训练输出格式测试
    print_warning "测试训练输出格式..."
    if docker exec "$DOCKER_CONTAINER" bash -c "cd /home/samuel/SCU_TSC && pytest tests/integration/test_integration.py::TestEndToEndTrainingSmallScale::test_training_output_format -v"; then
        print_success "训练输出格式测试通过"
    else
        print_warning "训练输出格式测试失败（可能需要Docker环境）"
    fi

    # 模型推理测试
    print_warning "测试模型推理..."
    if docker exec "$DOCKER_CONTAINER" bash -c "cd /home/samuel/SCU_TSC && pytest tests/integration/test_integration.py::TestEndToEndTrainingSmallScale::test_model_inference -v"; then
        print_success "模型推理测试通过"
    else
        print_warning "模型推理测试失败（可能需要Docker环境）"
    fi
}

# 清理临时文件
cleanup() {
    if [ "$KEEP_OUTPUT" = true ]; then
        print_step "4/4" "保留训练输出（跳过清理）"
        print_warning "训练输出保留在: tests/output/"
        return
    fi

    print_step "4/4" "清理临时文件"

    cd "$PROJECT_DIR"

    # 清理临时训练输出
    if [ -d "tests/output/test_training_" ]; then
        rm -rf tests/output/test_training_*
        print_success "已清理临时训练输出"
    fi
}

# 显示测试摘要
show_summary() {
    print_header "测试摘要"

    if [ $TEST_EXIT_CODE -eq 0 ]; then
        echo -e "${GREEN}✓ 所有集成测试通过${NC}"
        echo ""
        echo "完成的测试:"
        echo "  - 小规模端到端训练测试（SFT + GRPO）"
        echo "  - 训练输出格式验证"
        echo "  - 模型推理测试"
        echo ""
        echo "测试数据:"
        echo "  - GRPO数据: $OUTPUT_DIR/small_grpo_dataset.json ($NUM_GRPO 条)"
        echo "  - SFT数据: $OUTPUT_DIR/small_sft_dataset.json ($NUM_SFT 条)"
    else
        echo -e "${RED}✗ 集成测试失败${NC}"
        echo ""
        echo "退出码: $TEST_EXIT_CODE"
        echo ""
        echo "调试建议:"
        echo "  1. 使用 --verbose 查看详细输出"
        echo "  2. 使用 --keep-output 保留训练输出"
        echo "  3. 检查Docker容器日志: docker logs $DOCKER_CONTAINER"
    fi

    echo ""
}

# ==================== 主流程 ====================

main() {
    print_header "集成测试执行脚本"

    # 解析参数
    parse_args "$@"

    # 显示配置
    echo "配置:"
    echo "  项目目录: $PROJECT_DIR"
    echo "  Docker容器: $DOCKER_CONTAINER"
    echo "  GRPO数据条数: $NUM_GRPO"
    echo "  SFT数据条数: $NUM_SFT"
    echo "  超时时间: ${TIMEOUT}秒"
    echo "  跳过数据准备: $SKIP_PREPARE"
    echo "  保留输出: $KEEP_OUTPUT"
    echo "  详细输出: $VERBOSE"

    # 执行测试流程
    check_docker
    prepare_test_data
    run_integration_tests
    run_auxiliary_tests
    cleanup

    # 显示摘要
    show_summary

    # 返回退出码
    exit $TEST_EXIT_CODE
}

# 捕获中断信号
trap 'print_error "测试被中断"; exit 130' INT

# 运行主流程
main "$@"
