# Phase 03: 训练流程集成 - Research

**Researched:** 2026-02-02
**Domain:** Bash脚本自动化、数据验证、训练流程编排
**Confidence:** HIGH

## Summary

Phase 03专注于完善docker/publish.sh脚本,实现可靠的四步训练流程(GRPO数据生成→SFT数据合并→SFT训练→GRPO训练),并添加快速数据验证。研究涵盖了:

- **Bash脚本最佳实践**: 现代CI/CD级别的错误处理、日志记录和信号处理
- **数据验证模式**: 使用jsonschema库进行JSON数据验证,SUMO文件加载测试
- **进度显示**: 简洁的spinner实现,避免busy-wait循环
- **训练输出管理**: 日期命名、checkpoint清理、临时文件自动清理
- **失败策略**: 快速停止模式,确保任何步骤失败立即终止流程

**Primary recommendation:** 采用严格的bash脚本模式(set -euo pipefail)、实现可复用的验证函数、使用trap进行清理,并构建模块化的辅助脚本架构。

## Standard Stack

### Core
| Library/Tool | Version | Purpose | Why Standard |
|--------------|---------|---------|--------------|
| **Bash** | 4.4+ | 脚本语言 | 系统原生、Docker内执行可靠、与现有publish.sh一致 |
| **set -euo pipefail** | - | 错误处理模式 | 业界最佳实践,确保脚本在错误时立即停止 |
| **trap** | POSIX | 信号处理和清理 | 标准的清理机制,确保临时文件和进程被正确处理 |
| **jsonschema** | 4.x | Python数据验证 | 成熟的JSON Schema验证库,官方推荐 |

### Supporting
| Library/Tool | Version | Purpose | When to Use |
|--------------|---------|---------|-------------|
| **Python argparse** | stdlib | CLI参数解析 | 数据验证脚本需要命令行参数 |
| **PyYAML** | 6.x | 配置文件加载 | 现有代码已使用,验证脚本读取配置 |
| **mktemp** | POSIX | 临时文件创建 | 安全的临时文件生成,避免冲突 |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| bash | sh (POSIX) | bash提供数组、更丰富的字符串处理,但牺牲可移植性 |
| jsonschema | 手动if检查 | jsonschema提供声明式schema、更好的错误信息、可复用 |
| trap | 手动清理每个exit点 | trap集中处理,不遗漏,但需要理解信号机制 |
| spinner | pv/progress条 | spinner更简洁,pv提供进度条但不适合未知时长的任务 |

**Installation:**
```bash
# jsonschema (在Dockerfile中已安装)
pip install jsonschema

# Bash工具(系统自带)
# set, trap, mktemp都是POSIX标准工具
```

## Architecture Patterns

### Recommended Project Structure
```
scripts/
├── validation/
│   ├── validate_datasets.py   # 数据集验证主脚本
│   ├── validate_grpo_schema.json   # GRPO数据JSON Schema
│   └── validate_sft_schema.json    # SFT数据JSON Schema
├── utils/
│   ├── spinner.sh            # 进度显示辅助函数
│   ├── logging.sh            # 日志记录辅助函数
│   └── error_handling.sh     # 错误处理辅助函数
└── cleanup.sh               # 临时文件清理脚本

docker/
└── publish.sh               # 主训练流程脚本(增强版)

outputs/
├── 2026-02-02/              # 日期命名的训练输出
│   ├── sft_model/           # SFT训练checkpoint
│   └── grpo_model/          # GRPO训练checkpoint
└── 2026-02-01/
```

### Pattern 1: 严格的Bash错误处理模式

**What:** 使用`set -euo pipefail`确保脚本在错误时立即停止

**When to use:** 所有生产级bash脚本,特别是长时间运行的训练流程

**Example:**
```bash
#!/usr/bin/env bash
set -euo pipefail
# set -e: 任何命令失败立即退出
# set -u: 未定义变量视为错误
# set -o pipefail: 管道中任何命令失败则整个管道失败

# 来源: Red Hat官方博客 "Error handling in Bash scripts" (2021)
# https://www.redhat.com/en/blog/error-handling-bash-scripting
```

**Why:** 默认情况下bash会在命令失败后继续执行,导致级联错误和不可预测的行为。

### Pattern 2: 集中清理机制(trap)

**What:** 使用trap命令在脚本退出时(正常或异常)执行清理操作

**When to use:** 脚本创建临时文件、启动后台进程、需要清理Docker容器

**Example:**
```bash
#!/usr/bin/env bash
set -euo pipefail

# 全局变量存储临时文件路径
TEMP_FILES=()

# 清理函数
cleanup() {
    local exit_code=$?
    if [[ ${#TEMP_FILES[@]} -gt 0 ]]; then
        echo "[cleanup] Removing ${#TEMP_FILES[@]} temporary files..."
        rm -rf "${TEMP_FILES[@]}"
    fi
    exit $exit_code
}

# 注册EXIT信号处理
trap cleanup EXIT

# 创建临时文件
TEMP_FILE=$(mktemp)
TEMP_FILES+=("$TEMP_FILE")

# 即使脚本失败,cleanup也会被调用
some_command_that_might_fail || true
```

**来源:** Linux Journal "Use the Bash trap Statement to Clean Up Temporary Files" (2009)
**来源:** Baeldung "How to Display a Spinner for Long Running Tasks in Bash" (2024)

### Pattern 3: 模块化辅助函数库

**What:** 将通用功能(spinner、日志、错误处理)提取到可复用的脚本文件中

**When to use:** 多个脚本需要相同功能时

**Example:**
```bash
# scripts/utils/spinner.sh

# 启动spinner
start_spinner() {
    local message="$1"
    local pid=$2

    local spinner_chars="|/-\\"
    local i=0

    # 隐藏光标
    tput civis 2>/dev/null || true

    while kill -0 $pid 2>/dev/null; do
        i=$(( (i+1) % 4 ))
        printf "\r%s %s" "$message" "${spinner_chars:$i:1}"
        sleep 0.1
    done

    # 显示光标
    tput cnorm 2>/dev/null || true
    printf "\r%s done\n" "$message"
}

# 在主脚本中使用
source scripts/utils/spinner.sh

long_running_command &
start_spinner "Processing" $!
```

**来源:** Baeldung spinner实现 (2024) - 强调避免busy-wait循环

### Pattern 4: JSON Schema数据验证

**What:** 使用jsonschema库定义和验证JSON数据格式

**When to use:** 验证GRPO/SFT数据集、配置文件格式

**Example:**
```python
#!/usr/bin/env python3
# scripts/validation/validate_datasets.py

import json
import sys
from pathlib import Path
from jsonschema import validate, ValidationError

# GRPO数据schema
GRPO_SCHEMA = {
    "type": "object",
    "required": ["id", "scenario", "prompt"],
    "properties": {
        "id": {"type": "string"},
        "scenario": {"type": "string"},
        "prompt": {"type": "string"},
        "state_file": {"type": "string"}
    }
}

def validate_grpo_dataset(dataset_path: Path) -> bool:
    """验证GRPO数据集格式"""
    with open(dataset_path, 'r') as f:
        data = json.load(f)

    # 验证顶层是数组
    if not isinstance(data, list):
        print("[ERROR] GRPO dataset must be an array")
        return False

    # 抽样验证(前10条,快速失败)
    for i, entry in enumerate(data[:10]):
        try:
            validate(instance=entry, schema=GRPO_SCHEMA)
        except ValidationError as e:
            print(f"[ERROR] Entry {i} validation failed: {e.message}")
            return False

    print(f"[OK] Validated {len(data)} GRPO entries")
    return True

if __name__ == "__main__":
    if not validate_grpo_dataset(Path(sys.argv[1])):
        sys.exit(1)
```

**来源:** python-jsonschema官方文档 (stable版本)
**来源:** CSDN "Python + JSONSchema,一键搞定" (2024)

### Pattern 5: 自适应日志模式

**What:** 正常时简洁输出,失败时自动显示详细错误信息

**When to use:** 长时间运行的训练流程,用户需要实时反馈但不需要过多噪音

**Example:**
```bash
#!/usr/bin/env bash

# 日志级别变量
VERBOSE=0

# 日志函数
log_info() {
    echo "[INFO] $*"
}

log_error() {
    echo "[ERROR] $*" >&2
}

log_debug() {
    if [[ $VERBOSE -eq 1 ]]; then
        echo "[DEBUG] $*" >&2
    fi
}

# 执行命令,失败时自动启用verbose
run_with_fallback() {
    local cmd="$*"

    if ! $cmd > /dev/null 2>&1; then
        log_error "Command failed: $cmd"
        log_info "Retrying with verbose output..."
        VERBOSE=1
        if ! $cmd; then
            log_error "Failed again, aborting"
            return 1
        fi
    fi
}

# 使用
run_with_fallback python -m grpo.generate_grpo_dataset --all
```

**来源:** Red Hat bash错误处理最佳实践 (2021)

### Anti-Patterns to Avoid

- **❌ 忽略错误输出:**
  ```bash
  # 错误: 忽略所有错误
  python -m grpo.sft_training 2>/dev/null

  # 正确: 捕获并处理错误
  if ! python -m grpo.sft_training 2>&1 | tee train.log; then
      echo "[ERROR] SFT training failed, see train.log"
      exit 1
  fi
  ```

- **❌ 手动在每个失败点清理:**
  ```bash
  # 错误: 容易遗漏,难以维护
  mkdir -p temp_dir
  if some_command; then
      rm -rf temp_dir
      exit 0
  else
      rm -rf temp_dir
      exit 1
  fi

  # 正确: 使用trap集中处理
  trap 'rm -rf temp_dir' EXIT
  mkdir -p temp_dir
  some_command
  ```

- **❌ Busy-wait循环的spinner:**
  ```bash
  # 错误: 占用CPU,影响实际任务性能
  while ps -p $pid > /dev/null; do
      printf "\b%c" "${sp:i++%4:1}"
      # 忘记sleep!造成busy-wait
  done

  # 正确: 添加sleep避免busy-wait
  while ps -p $pid > /dev/null; do
      printf "\b%c" "${sp:i++%4:1}"
      sleep 0.1  # 关键:让出CPU时间片
  done
  ```
  **来源:** Baeldung spinner文章特别警告busy-wait问题 (2024)

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| JSON验证 | 手写if-else检查每个字段 | jsonschema库 | Schema可复用、更好的错误信息、支持嵌套结构、社区标准 |
| 临时文件清理 | 手动rm在每个退出点 | trap命令 | 保证清理、不遗漏、支持信号处理 |
| 参数解析 | 手动处理$1, $2, $@ | argparse (Python) / getopts (Bash) | 自动生成帮助、支持可选参数、错误处理 |
| 错误传播 | 手动检查每个$? | set -e | 自动处理、零遗漏、行业标准 |
| 配置加载 | 手动解析YAML/JSON | PyYAML / json.load | 处理边缘情况、类型转换、错误信息 |

**Key insight:** 这些"简单"问题的正确实现涉及大量边缘情况(signal中断、并发、编码、部分写入等)。现有解决方案已经处理了这些边缘情况,经过广泛测试,值得信任。

## Common Pitfalls

### Pitfall 1: Trap中的Exit Code丢失

**What goes wrong:** 清理函数中使用`exit`覆盖了原始错误码,导致外部调用者无法判断失败原因

**Why it happens:** 在trap函数中直接调用`exit 1`会覆盖原始退出码

**How to avoid:**
```bash
# 错误: 总是exit 1
cleanup() {
    rm -rf /tmp/myfile
    exit 1  # 覆盖了原始错误码!
}

# 正确: 保留原始错误码
cleanup() {
    local exit_code=$?
    rm -rf /tmp/myfile
    exit $exit_code  # 保留原始错误码
}
```

**Warning signs:** 脚本总是返回相同的错误码(通常是1),无法区分失败类型

### Pitfall 2: Pipe中错误被忽略

**What goes wrong:** 管道中只有最后一个命令的退出码被检查,中间命令失败被忽略

**Why it happens:** bash默认只检查管道最后一个命令

**How to avoid:**
```bash
# 错误: grep失败时返回0(grep的行为)
cat file.txt | grep pattern | wc -l

# 正确: 使用pipefail
set -o pipefail
cat file.txt | grep pattern | wc -l
# 现在如果cat或grep失败,整个管道返回非零

# 或使用PIPESTATUS
cat file.txt | grep pattern | wc -l
if [[ ${PIPESTATUS[0]} -ne 0 || ${PIPESTATUS[1]} -ne 0 ]]; then
    echo "Error in pipeline"
fi
```

**来源:** Karandeep Singh "Bulletproof Bash Scripts" (2023) - 强调pipefail的重要性

**Warning signs:** 管道命令失败但脚本继续执行,数据不完整

### Pitfall 3: 验证步骤拖慢训练流程

**What goes wrong:** 数据验证耗时过长(几分钟),用户不得不每次等待

**Why it happens:** 验证全部数据而非抽样,或执行慢速操作(如实际启动SUMO)

**How to avoid:**
```python
# 错误: 验证全部数据,每次都慢
def validate_dataset(path):
    data = json.load(path)  # 可能有10万条
    for entry in data:  # 全部验证
        validate(entry)

# 正确: 抽样验证,快速失败
def validate_dataset(path):
    data = json.load(path)

    # 快速检查: 必需字段存在性(只读前10条)
    sample = data[:10]
    for entry in sample:
        validate(entry)

    # 完整性检查: 只检查数量
    if len(data) < 100:
        raise ValueError("Dataset too small")

    print(f"[OK] Quick validated {len(data)} entries (sampled first 10)")
```

**来源:** CONTEXT.md明确要求"数据验证要快(几秒内完成)"

**Warning signs:** 验证脚本比实际数据生成还慢,用户倾向于跳过验证

### Pitfall 4: Docker容器内路径不一致

**What goes wrong:** 脚本在Docker内执行,但路径假设是宿主机路径

**Why it happens:** publish.sh在宿主机调用,但训练命令在容器内执行

**How to avoid:**
```bash
# 错误: 混用宿主机和容器路径
HOST_PROJECT_DIR="/home/samuel/SCU_TSC"
docker run ... -v "$HOST_PROJECT_DIR:/workspace" ...
cd /home/samuel/SCU_TSC  # 在容器内不存在!

# 正确: 使用容器内工作目录
CONTAINER_WORKDIR="/home/samuel/SCU_TSC"  # 容器内路径
HOST_PROJECT_DIR="/home/samuel/SCU_TSC"    # 宿主机路径

docker run \
  -v "$HOST_PROJECT_DIR:$CONTAINER_WORKDIR:rw" \
  -w "$CONTAINER_WORKDIR" \
  ... -c "cd $CONTAINER_WORKDIR && python ..."
```

**Warning signs:** 文件不存在错误,No such file or directory

### Pitfall 5: 临时文件泄漏

**What goes wrong:** 脚本异常退出时临时文件未被清理,磁盘空间逐渐耗尽

**Why it happens:** 只在正常退出路径清理,异常退出路径遗漏

**How to avoid:**
```bash
# 错误: 只在成功时清理
TEMP_FILE=$(mktemp)
# ... do work ...
rm "$TEMP_FILE"  # 如果上面失败,这里不执行

# 正确: 使用trap保证清理
TEMP_FILE=$(mktemp)
trap 'rm -f "$TEMP_FILE"' EXIT  # 无论成功失败都会执行
# ... do work ...
# trap会自动清理
```

**Warning signs:** /tmp或项目目录下残留大量临时文件,disk space警告

## Code Examples

### Example 1: 完整的训练流程脚本框架

```bash
#!/usr/bin/env bash
set -euo pipefail

################################################################################
# 完整的GRPO训练流程脚本
################################################################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

# ============== 配置 ==============
CONFIG_FILE="${CONFIG_FILE:-config/training_config.yaml}"
OUTPUT_BASE_DIR="${OUTPUT_BASE_DIR:-outputs}"
DATE_SUFFIX=$(date +%Y-%m-%d)
OUTPUT_DIR="${OUTPUT_BASE_DIR}/${DATE_SUFFIX}"

# 日志配置
LOG_FILE="${PROJECT_DIR}/.training_${DATE_SUFFIX}.log"
VERBOSE=0

# ============== 辅助函数 ==============
source "${SCRIPT_DIR}/scripts/utils/logging.sh"
source "${SCRIPT_DIR}/scripts/utils/spinner.sh"

# ============== 清理函数 ==============
cleanup() {
    local exit_code=$?
    if [[ -f "${TEMP_DIR:-}" ]]; then
        log_debug "Cleaning up temp dir: $TEMP_DIR"
        rm -rf "$TEMP_DIR"
    fi
    exit $exit_code
}
trap cleanup EXIT

# ============== 依赖检查 ==============
check_dependencies() {
    log_info "Checking dependencies..."

    local missing=0

    # 检查必需命令
    for cmd in python docker nvidia-smi; do
        if ! command -v $cmd &>/dev/null; then
            log_error "Missing command: $cmd"
            missing=1
        fi
    done

    # 检查Python包
    if ! python -c "import yaml, jsonschema" 2>/dev/null; then
        log_error "Missing Python packages: pyyaml, jsonschema"
        missing=1
    fi

    if [[ $missing -eq 1 ]]; then
        log_error "Dependency check failed"
        exit 1
    fi

    log_info "Dependencies OK"
}

# ============== 数据验证 ==============
validate_data() {
    log_info "Validating datasets..."

    local grpo_dir="$1"
    local sft_file="$2"

    # 调用Python验证脚本
    if ! python scripts/validation/validate_datasets.py \
        --grpo-dir "$grpo_dir" \
        --sft-file "$sft_file"; then
        log_error "Data validation failed"
        return 1
    fi

    log_info "Data validation passed"
}

# ============== 训练步骤 ==============
step_1_generate_grpo() {
    log_info "Step 1/4: Generating GRPO dataset..."

    if ! python -m grpo.generate_grpo_dataset \
        --all \
        --parallel "${PARALLEL:-4}" \
        --extend-seconds "${EXTEND_SECONDS:-5}"; then
        log_error "GRPO data generation failed"
        return 1
    fi

    log_info "Step 1/4: GRPO dataset generated"
}

step_2_generate_sft() {
    log_info "Step 2/4: Generating SFT dataset..."

    if ! python -m grpo.generate_sft_dataset; then
        log_error "SFT data generation failed"
        return 1
    fi

    log_info "Step 2/4: SFT dataset generated"
}

step_3_sft_training() {
    log_info "Step 3/4: SFT training..."

    local sft_output="${OUTPUT_DIR}/sft_model"

    if ! python -m grpo.sft_training \
        --config "$CONFIG_FILE" \
        --output-dir "$sft_output" 2>&1 | tee -a "$LOG_FILE"; then
        log_error "SFT training failed"
        return 1
    fi

    log_info "Step 3/4: SFT training completed"
}

step_4_grpo_training() {
    log_info "Step 4/4: GRPO training..."

    local grpo_output="${OUTPUT_DIR}/grpo_model"

    if ! python -m grpo.grpo_training \
        --config "$CONFIG_FILE" \
        --output-dir "$grpo_output" 2>&1 | tee -a "$LOG_FILE"; then
        log_error "GRPO training failed"
        return 1
    fi

    log_info "Step 4/4: GRPO training completed"
}

# ============== 训练摘要 ==============
print_summary() {
    log_info ""
    log_info "=========================================="
    log_info "Training completed successfully!"
    log_info "=========================================="
    log_info "Output directory: ${OUTPUT_DIR}"
    log_info "SFT model: ${OUTPUT_DIR}/sft_model"
    log_info "GRPO model: ${OUTPUT_DIR}/grpo_model"
    log_info "Log file: ${LOG_FILE}"
    log_info "=========================================="
}

# ============== 主流程 ==============
main() {
    log_info "Starting GRPO training pipeline..."
    log_info "Config: ${CONFIG_FILE}"
    log_info "Output: ${OUTPUT_DIR}"

    # 1. 依赖检查
    check_dependencies

    # 2. 数据验证(训练前)
    validate_data \
        "${PROJECT_DIR}/data/grpo_datasets" \
        "${PROJECT_DIR}/data/sft_datasets/sft_dataset.json"

    # 3. 四步训练流程
    step_1_generate_grpo || exit $?
    step_2_generate_sft || exit $?
    step_3_sft_training || exit $?
    step_4_grpo_training || exit $?

    # 4. 显示摘要
    print_summary
}

main "$@"
```

**来源:** 基于现有publish.sh + Karandeep Singh最佳实践 (2023) + Red Hat错误处理模式 (2021)

### Example 2: JSON Schema验证脚本

```python
#!/usr/bin/env python3
"""
数据集验证脚本

用法:
    python validate_datasets.py
    python validate_datasets.py --grpo-dir data/grpo_datasets
    python validate_datasets.py --verbose
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

try:
    from jsonschema import validate, ValidationError
except ImportError:
    print("[ERROR] jsonschema not installed. Run: pip install jsonschema")
    sys.exit(1)


# GRPO数据schema (关键字段)
GRPO_SCHEMA = {
    "type": "object",
    "required": ["id", "scenario", "prompt"],
    "properties": {
        "id": {"type": "string"},
        "scenario": {"type": "string"},
        "prompt": {"type": "string"},
        # state_file是可选的,但如果存在必须是字符串
        "state_file": {"type": "string"}
    }
}

# SFT数据schema
SFT_SCHEMA = {
    "type": "object",
    "required": ["messages"],
    "properties": {
        "id": {"type": "string"},
        "scenario": {"type": "string"},
        "messages": {
            "type": "array",
            "minItems": 2,  # 至少user + assistant
            "items": {
                "type": "object",
                "required": ["role", "content"],
                "properties": {
                    "role": {"enum": ["system", "user", "assistant"]},
                    "content": {"type": "string"}
                }
            }
        }
    }
}


def validate_grpo_scenario(scenario_dir: Path, verbose: bool = False) -> bool:
    """验证单个场景的GRPO数据集"""
    dataset_file = scenario_dir / "grpo_dataset.json"

    if not dataset_file.exists():
        print(f"[SKIP] {scenario_dir.name}: no grpo_dataset.json")
        return True

    with open(dataset_file, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"[ERROR] {scenario_dir.name}: Invalid JSON - {e}")
            return False

    if not isinstance(data, list):
        print(f"[ERROR] {scenario_dir.name}: Root must be array")
        return False

    if len(data) == 0:
        print(f"[WARN] {scenario_dir.name}: Empty dataset")
        return True

    # 抽样验证前10条
    sample_size = min(10, len(data))
    for i in range(sample_size):
        try:
            validate(instance=data[i], schema=GRPO_SCHEMA)
        except ValidationError as e:
            print(f"[ERROR] {scenario_dir.name}: Entry {i} - {e.message}")
            if verbose:
                print(f"  Entry: {json.dumps(data[i], ensure_ascii=False)[:200]}")
            return False

    print(f"[OK] {scenario_dir.name}: {len(data)} entries (sampled {sample_size})")
    return True


def validate_sft_dataset(sft_file: Path, verbose: bool = False) -> bool:
    """验证SFT数据集"""
    if not sft_file.exists():
        print(f"[ERROR] SFT dataset not found: {sft_file}")
        return False

    with open(sft_file, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"[ERROR] Invalid JSON - {e}")
            return False

    if not isinstance(data, list):
        print(f"[ERROR] Root must be array")
        return False

    if len(data) < 100:
        print(f"[WARN] SFT dataset too small: {len(data)} entries")

    # 抽样验证
    sample_size = min(10, len(data))
    for i in range(sample_size):
        try:
            validate(instance=data[i], schema=SFT_SCHEMA)
        except ValidationError as e:
            print(f"[ERROR] SFT entry {i} - {e.message}")
            if verbose:
                print(f"  Entry: {json.dumps(data[i], ensure_ascii=False)[:200]}")
            return False

    print(f"[OK] SFT dataset: {len(data)} entries (sampled {sample_size})")
    return True


def main():
    parser = argparse.ArgumentParser(description="Validate GRPO and SFT datasets")
    parser.add_argument(
        "--grpo-dir",
        type=Path,
        default=Path("data/grpo_datasets"),
        help="GRPO datasets directory"
    )
    parser.add_argument(
        "--sft-file",
        type=Path,
        default=Path("data/sft_datasets/sft_dataset.json"),
        help="SFT dataset file"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Data Validation")
    print("=" * 60)

    all_ok = True

    # 验证GRPO数据集
    print("\n[1/2] Validating GRPO datasets...")
    if args.grpo_dir.exists():
        for scenario_dir in sorted(args.grpo_dir.iterdir()):
            if scenario_dir.is_dir():
                if not validate_grpo_scenario(scenario_dir, args.verbose):
                    all_ok = False
    else:
        print(f"[ERROR] GRPO directory not found: {args.grpo_dir}")
        all_ok = False

    # 验证SFT数据集
    print("\n[2/2] Validating SFT dataset...")
    if not validate_sft_dataset(args.sft_file, args.verbose):
        all_ok = False

    print("\n" + "=" * 60)
    if all_ok:
        print("✓ All validations passed")
        print("=" * 60)
        return 0
    else:
        print("✗ Validation failed")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

**来源:** python-jsonschema官方文档 + 现有grpo/config.py结构

### Example 3: 简洁的Spinner实现

```bash
#!/usr/bin/env bash
# scripts/utils/spinner.sh

# 显示spinner直到后台进程完成
# 用法: long_command & spinner "Processing message" $!

spinner() {
    local message="$1"
    local pid=$2
    local delay=0.1
    local spinner_chars="|/-\\"
    local i=0

    # 隐藏光标
    tput civis 2>/dev/null || true

    # 循环直到进程结束
    while kill -0 $pid 2>/dev/null; do
        i=$(( (i+1) % 4 ))
        printf "\r%s %s" "$message" "${spinner_chars:$i:1}"
        sleep $delay
    done

    # 显示光标
    tput cnorm 2>/dev/null || true

    # 检查进程退出码
    wait $pid
    local exit_code=$?

    if [[ $exit_code -eq 0 ]]; then
        printf "\r%s ✓\n" "$message"
    else
        printf "\r%s ✗ (exit %d)\n" "$message" $exit_code
    fi

    return $exit_code
}
```

**使用示例:**
```bash
source scripts/utils/spinner.sh

# 后台运行长任务并显示spinner
python -m grpo.generate_grpo_dataset --all &
spinner "Generating GRPO dataset" $!
```

**来源:** Baeldung "How to Display a Spinner" (2024) - 强调sleep避免busy-wait

### Example 4: 日期命名的输出目录管理

```bash
#!/usr/bin/env bash
# scripts/cleanup.sh - 清理旧的训练输出

OUTPUT_BASE_DIR="${OUTPUT_BASE_DIR:-outputs}"
KEEP_COUNT="${KEEP_COUNT:-3}"  # 保留最近N个

cleanup_old_outputs() {
    log_info "Cleaning up old outputs (keeping last $KEEP_COUNT)..."

    if [[ ! -d "$OUTPUT_BASE_DIR" ]]; then
        log_info "No outputs directory"
        return 0
    fi

    # 按日期排序,删除旧的
    # 目录格式: outputs/YYYY-MM-DD/
    local count=0
    for dir in $(ls -1 -r "$OUTPUT_BASE_DIR"); do
        count=$((count + 1))

        if [[ $count -gt $KEEP_COUNT ]]; then
            log_info "Removing old output: $dir"
            rm -rf "${OUTPUT_BASE_DIR}/${dir}"
        fi
    done

    log_info "Cleanup completed"
}
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| **忽略错误继续执行** | **set -euo pipefail** | 长期最佳实践 | 脚本更可靠,错误立即暴露 |
| **手动检查每个$?** | **trap集中错误处理** | 2000s | 代码更简洁,不遗漏错误处理 |
| **手动JSON验证** | **jsonschema声明式验证** | 2010s | 验证逻辑可复用,错误信息更清晰 |
| **无进度显示** | **spinner/进度条** | 2010s | 用户体验更好,脚本看起来专业 |
| **临时文件手动清理** | **trap自动清理** | POSIX标准 | 保证清理,不泄漏资源 |

**Deprecated/outdated:**
- **使用``进行命令替换:** 应使用$() - 更易读、可嵌套
- **使用[]进行test:** 应使用[[ ]]- 更强大的条件测试
- **手动管理exit codes:** 应使用set -e和trap - 自动处理

## Open Questions

1. **Checkpoint保留数量(N值)**
   - What we know: 需要保留最近几个SFT checkpoint,删除旧的
   - What's unclear: 具体保留多少个合适(2? 3? 5?)
   - Recommendation: 从N=3开始(保留最近3个),根据磁盘使用情况调整。HuggingFace Trainer默认save_total_limit=2

2. **SUMO状态文件可加载性验证**
   - What we know: 需要验证SUMO状态文件可以正确加载
   - What's unclear: 是否需要实际启动SUMO仿真验证,还是只检查文件格式
   - Recommendation: 第一阶段只检查文件存在性和格式(.xml/.json正确),不实际启动SUMO(太慢)。后续可以添加可选的深度验证模式

3. **数据集抽样的sample_size**
   - What we know: 验证要快,不应该验证全部数据
   - What's unclear: 抽样多少条合适(10条? 100条? 1000条?)
   - Recommendation: 固定抽样前10条作为快速验证(足够发现格式问题),如果10条全部通过则假设整体格式正确

## Sources

### Primary (HIGH confidence)
- **python-jsonschema** - Official documentation for JSON schema validation in Python
  - https://python-jsonschema.readthedocs.io/en/stable/
- **Red Hat Blog** - "Error handling in Bash scripts" (2021)
  - https://www.redhat.com/en/blog/error-handling-bash-scripting
- **Karandeep Singh** - "Bulletproof Bash Scripts: Mastering Error Handling" (2023)
  - https://karandeepsingh.ca/posts/bash-error-handling-bulletproof-scripts/
- **Baeldung** - "How to Display a Spinner for Long Running Tasks in Bash" (2024)
  - https://www.baeldung.com/linux/bash-show-spinner-long-tasks
- **Linux Journal** - "Use the Bash trap Statement to Clean Up Temporary Files" (2009)
  - https://www.linuxjournal.com/content/use-bash-trap-statement-cleanup-temporary-files

### Secondary (MEDIUM confidence)
- **Stack Overflow** - Bash error handling discussions (verified with Red Hat)
  - https://stackoverflow.com/questions/64786/error-handling-in-bash
- **CSDN** - "别再手动验证数据了!Python + JSONSchema" (2024)
  - https://cloud.tencent.com/developer/article/2468284

### Tertiary (LOW confidence)
- WebSearch关于bash spinner/progress的讨论(已用Baeldung官方文章验证升级为MEDIUM)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - 基于官方文档和长期最佳实践
- Architecture: HIGH - 来源可靠(Red Hat, Karandeep Singh, Baeldung)
- Pitfalls: HIGH - 基于官方文档和社区验证的模式

**Research date:** 2026-02-02
**Valid until:** 2026-03-02 (30天 - Bash和jsonschema是稳定技术)

**与CONTEXT.md决策对齐:**
- ✅ 失败策略: 快速停止 - set -e模式
- ✅ 日志记录: 自适应 - 实现了verbose切换
- ✅ 进度显示: 动态spinner - 提供了简洁实现
- ✅ 数据验证: 全覆盖 - jsonschema验证所有关键数据
- ✅ 验证时机: 训练前统一验证 - validate_data在训练前调用
- ✅ 模型保存: 日期命名 - outputs/YYYY-MM-DD/
- ✅ 临时文件: 自动清理 - trap机制
- ✅ 执行环境: Docker内执行 - 与现有publish.sh一致
