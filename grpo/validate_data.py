#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据验证脚本 - 在训练前快速检查数据集格式和正确性

验证内容：
- GRPO数据集格式验证
- SFT数据集格式验证
- SUMO状态文件验证（抽样）
- 配置文件和系统依赖验证

用法:
    python -m grpo.validate_data              # 验证所有
    python -m grpo.validate_data --grpo-only  # 仅验证GRPO
    python -m grpo.validate_data --verify-sumo  # 验证SUMO文件
"""

import os
import sys
import json
import random
import argparse
import subprocess
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path

# 添加项目根目录到路径
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_DIR)


# ============== 容器环境检测 ==============

def is_running_in_container() -> bool:
    """
    检测是否在容器内运行

    Returns:
        bool: 是否在容器内
    """
    # 方法1: 检查 /proc/1/cgroup
    try:
        with open('/proc/1/cgroup', 'r') as f:
            content = f.read()
            if 'docker' in content or 'lxc' in content or 'kubepods' in content:
                return True
    except (FileNotFoundError, PermissionError):
        pass

    # 方法2: 检查环境变量
    if os.environ.get(' container') is not None:
        return True

    return False


def get_project_dir() -> str:
    """
    获取项目根目录（容器环境适配）

    Returns:
        str: 项目根目录的绝对路径
    """
    if is_running_in_container():
        # 容器内使用固定路径
        return "/home/samuel/SCU_TSC"
    else:
        # 主机环境使用PROJECT_DIR或通过路径解析
        if "PROJECT_DIR" in os.environ:
            return os.environ["PROJECT_DIR"]
        # 自动检测（当前文件所在目录的父目录）
        return PROJECT_DIR


# ============== 验证结果收集 ==============

class ValidationResult:
    """验证结果收集器"""

    def __init__(self, category: str):
        self.category = category
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def add_error(self, message: str):
        """添加错误信息"""
        self.errors.append(message)

    def add_warning(self, message: str):
        """添加警告信息"""
        self.warnings.append(message)

    def has_errors(self) -> bool:
        """是否有错误"""
        return len(self.errors) > 0

    def has_warnings(self) -> bool:
        """是否有警告"""
        return len(self.warnings) > 0

    def is_valid(self) -> bool:
        """是否验证通过"""
        return len(self.errors) == 0

    def format_output(self) -> str:
        """格式化输出"""
        if self.is_valid() and not self.has_warnings():
            return ""

        lines = []
        if self.errors:
            lines.append(f"[ERROR] {self.category}验证失败:")
            for error in self.errors:
                lines.append(f"  - {error}")

        if self.warnings:
            lines.append(f"[WARNING] {self.category}警告:")
            for warning in self.warnings:
                lines.append(f"  - {warning}")

        return "\n".join(lines)


# ============== GRPO数据集验证 ==============

def validate_grpo_dataset(
    grpo_datasets_dir: Optional[str] = None,
    verbose: bool = False
) -> ValidationResult:
    """
    验证GRPO数据集

    验证项：
    1. 文件存在性：data/grpo_datasets/*/grpo_dataset.json存在
    2. JSON格式：文件可解析为有效JSON
    3. 必需字段：每条数据包含 id, prompt, scenario, junction_id, state_file
    4. 字段类型检查：各字段类型正确
    5. 数据量检查：每个场景至少有10条数据
    6. state_file路径存在性检查

    Args:
        grpo_datasets_dir: GRPO数据集根目录（None则自动检测）
        verbose: 是否显示详细进度信息

    Returns:
        ValidationResult对象
    """
    result = ValidationResult("GRPO数据集")

    # 自动检测路径
    if grpo_datasets_dir is None:
        project_dir = get_project_dir()
        grpo_datasets_dir = os.path.join(project_dir, "data/grpo_datasets")

    if verbose:
        print(f"验证GRPO数据集: {grpo_datasets_dir}")

    # 检查目录是否存在
    if not os.path.isdir(grpo_datasets_dir):
        result.add_error(f"GRPO数据集目录不存在: {grpo_datasets_dir}")
        return result

    # 获取所有场景目录
    scenario_dirs = []
    try:
        for entry in os.listdir(grpo_datasets_dir):
            scenario_path = os.path.join(grpo_datasets_dir, entry)
            if os.path.isdir(scenario_path):
                scenario_dirs.append((entry, scenario_path))
    except Exception as e:
        result.add_error(f"读取GRPO数据集目录失败: {e}")
        return result

    if not scenario_dirs:
        result.add_error(f"GRPO数据集目录为空: {grpo_datasets_dir}")
        return result

    if verbose:
        print(f"  找到 {len(scenario_dirs)} 个场景目录")

    # 验证每个场景
    for scenario_name, scenario_dir in scenario_dirs:
        dataset_file = os.path.join(scenario_dir, "grpo_dataset.json")

        # 检查文件存在性
        if not os.path.isfile(dataset_file):
            result.add_error(f"场景 {scenario_name}: grpo_dataset.json文件不存在")
            continue

        # 尝试解析JSON
        try:
            with open(dataset_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            result.add_error(f"场景 {scenario_name}: JSON格式错误 - {e}")
            continue
        except Exception as e:
            result.add_error(f"场景 {scenario_name}: 读取文件失败 - {e}")
            continue

        # 检查数据类型
        if not isinstance(data, list):
            result.add_error(f"场景 {scenario_name}: 数据应该是数组格式")
            continue

        # 检查数据量
        if len(data) < 10:
            result.add_error(f"场景 {scenario_name}: 数据量不足，只有 {len(data)} 条，至少需要10条")
            continue

        if verbose:
            print(f"  场景 {scenario_name}: {len(data)} 条数据")

        # 验证每条数据
        required_fields = {
            "id": str,
            "prompt": str,
            "scenario": str,
            "junction_id": str,
            "state_file": str,
        }

        for idx, entry in enumerate(data, start=1):
            # 检查必需字段
            for field, expected_type in required_fields.items():
                if field not in entry:
                    result.add_error(f"场景 {scenario_name}: 第{idx}条数据缺少{field}字段")
                    continue

                # 检查字段类型
                if not isinstance(entry[field], expected_type):
                    result.add_error(
                        f"场景 {scenario_name}: 第{idx}条数据{field}字段类型错误，"
                        f"期望{expected_type.__name__}，实际{type(entry[field]).__name__}"
                    )

            # 检查prompt非空
            if "prompt" in entry and isinstance(entry["prompt"], str):
                if not entry["prompt"].strip():
                    result.add_error(f"场景 {scenario_name}: 第{idx}条数据prompt字段为空")

            # 检查state_file路径存在性
            if "state_file" in entry and isinstance(entry["state_file"], str):
                state_file_path = os.path.join(scenario_dir, entry["state_file"])
                if not os.path.isfile(state_file_path):
                    result.add_error(
                        f"场景 {scenario_name}: 第{idx}条数据state_file不存在: {entry['state_file']}"
                    )

    return result


# ============== SFT数据集验证 ==============

def validate_sft_dataset(
    sft_dataset_file: Optional[str] = None,
    verbose: bool = False
) -> ValidationResult:
    """
    验证SFT数据集

    验证项：
    1. 文件存在性：data/sft_datasets/sft_dataset.json存在
    2. JSON格式：文件可解析为有效JSON
    3. 必需字段：id, messages, scenario
    4. messages格式验证：
       - 至少3条消息（system, user, assistant）
       - role字段正确
       - assistant.content是有效JSON且格式为{"extend": "yes"|"no"}

    Args:
        sft_dataset_file: SFT数据集文件路径（None则自动检测）
        verbose: 是否显示详细进度信息

    Returns:
        ValidationResult对象
    """
    result = ValidationResult("SFT数据集")

    # 自动检测路径
    if sft_dataset_file is None:
        project_dir = get_project_dir()
        sft_dataset_file = os.path.join(project_dir, "data/sft_datasets/sft_dataset.json")

    if verbose:
        print(f"验证SFT数据集: {sft_dataset_file}")

    # 检查文件存在性
    if not os.path.isfile(sft_dataset_file):
        result.add_error(f"SFT数据集文件不存在: {sft_dataset_file}")
        return result

    # 尝试解析JSON
    try:
        with open(sft_dataset_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        result.add_error(f"JSON格式错误 - {e}")
        return result
    except Exception as e:
        result.add_error(f"读取文件失败 - {e}")
        return result

    # 检查数据类型
    if not isinstance(data, list):
        result.add_error(f"数据应该是数组格式")
        return result

    if verbose:
        print(f"  共 {len(data)} 条数据")

    # 验证每条数据
    required_fields = {
        "id": str,
        "messages": list,
        "scenario": str,
    }

    for idx, entry in enumerate(data, start=1):
        # 检查必需字段
        for field, expected_type in required_fields.items():
            if field not in entry:
                result.add_error(f"第{idx}条数据缺少{field}字段")
                continue

            if not isinstance(entry[field], expected_type):
                result.add_error(
                    f"第{idx}条数据{field}字段类型错误，"
                    f"期望{expected_type.__name__}，实际{type(entry[field]).__name__}"
                )

        # 检查messages格式
        if "messages" in entry and isinstance(entry["messages"], list):
            messages = entry["messages"]

            # 检查消息数量
            if len(messages) < 3:
                result.add_error(f"第{idx}条数据messages数量不足，至少需要3条，实际{len(messages)}条")
                continue

            # 检查role字段
            roles = {msg.get("role") for msg in messages if isinstance(msg, dict)}
            required_roles = {"system", "user", "assistant"}

            missing_roles = required_roles - roles
            if missing_roles:
                result.add_error(
                    f"第{idx}条数据messages缺少必需role: {', '.join(missing_roles)}"
                )

            # 验证assistant.content格式
            for msg_idx, msg in enumerate(messages):
                if not isinstance(msg, dict):
                    continue

                role = msg.get("role")
                content = msg.get("content")

                if role == "assistant" and isinstance(content, str):
                    # 尝试解析为JSON
                    try:
                        content_json = json.loads(content)
                        if not isinstance(content_json, dict):
                            result.add_error(
                                f"第{idx}条数据第{msg_idx + 1}条消息的content应该是JSON对象"
                            )
                        elif "extend" not in content_json:
                            result.add_error(
                                f"第{idx}条数据第{msg_idx + 1}条消息的content缺少extend字段"
                            )
                        else:
                            extend_value = content_json["extend"]
                            if extend_value not in ["yes", "no"]:
                                result.add_error(
                                    f"第{idx}条数据第{msg_idx + 1}条消息的extend字段值应该是'yes'或'no'，"
                                    f"实际'{extend_value}'"
                                )
                    except json.JSONDecodeError:
                        result.add_error(
                            f"第{idx}条数据第{msg_idx + 1}条消息的content不是有效JSON"
                        )

    return result


# ============== SUMO状态文件验证 ==============

def validate_sumo_state_files(
    grpo_datasets_dir: Optional[str] = None,
    sample_size: int = 10,
    verbose: bool = False
) -> ValidationResult:
    """
    验证SUMO状态文件（抽样验证）

    验证策略（快速验证）：
    1. 抽样验证：随机抽取10个state_file路径
    2. 文件存在性：文件存在
    3. XML格式：文件可解析为有效XML（使用ElementTree）
    4. 根元素：根元素是<snapshot>

    Args:
        grpo_datasets_dir: GRPO数据集根目录（None则自动检测）
        sample_size: 抽样数量
        verbose: 是否显示详细进度信息

    Returns:
        ValidationResult对象
    """
    result = ValidationResult("SUMO状态文件")

    # 自动检测路径
    if grpo_datasets_dir is None:
        project_dir = get_project_dir()
        grpo_datasets_dir = os.path.join(project_dir, "data/grpo_datasets")

    if verbose:
        print(f"验证SUMO状态文件（抽样{sample_size}个）")

    # 收集所有state_file路径
    state_files = []

    if not os.path.isdir(grpo_datasets_dir):
        result.add_error(f"GRPO数据集目录不存在: {grpo_datasets_dir}")
        return result

    try:
        for scenario_name in os.listdir(grpo_datasets_dir):
            scenario_dir = os.path.join(grpo_datasets_dir, scenario_name)
            if not os.path.isdir(scenario_dir):
                continue

            dataset_file = os.path.join(scenario_dir, "grpo_dataset.json")
            if not os.path.isfile(dataset_file):
                continue

            try:
                with open(dataset_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                for entry in data:
                    if "state_file" in entry and "scenario" in entry:
                        state_file_path = os.path.join(scenario_dir, entry["state_file"])
                        state_files.append((entry["scenario"], state_file_path))
            except Exception:
                # 忽略解析错误，继续收集
                pass
    except Exception as e:
        result.add_error(f"扫描state_file失败: {e}")
        return result

    if not state_files:
        result.add_error("没有找到任何state_file")
        return result

    if verbose:
        print(f"  共找到 {len(state_files)} 个state_file")

    # 抽样
    if len(state_files) > sample_size:
        state_files = random.sample(state_files, sample_size)

    if verbose:
        print(f"  抽样验证 {len(state_files)} 个文件")

    # 验证每个抽样文件
    for scenario, state_file_path in state_files:
        # 检查文件存在性
        if not os.path.isfile(state_file_path):
            result.add_error(f"{state_file_path}: 文件不存在")
            continue

        # 尝试解析XML
        try:
            tree = ET.parse(state_file_path)
            root = tree.getroot()

            # 检查根元素
            if root.tag != "snapshot":
                result.add_warning(
                    f"{state_file_path}: 根元素不是<snapshot>，实际<{root.tag}>"
                )
        except ET.ParseError as e:
            result.add_error(f"{state_file_path}: XML解析失败 - {e}")
        except Exception as e:
            result.add_error(f"{state_file_path}: 读取失败 - {e}")

    return result


# ============== 配置和系统依赖验证 ==============

def validate_config_and_environment(
    config_file: Optional[str] = None,
    verbose: bool = False
) -> ValidationResult:
    """
    验证配置文件和系统依赖

    验证项：
    1. 配置文件存在性和YAML格式
    2. 必需配置项
    3. Python包导入测试
    4. SUMO环境

    Args:
        config_file: 配置文件路径（None则自动检测）
        verbose: 是否显示详细进度信息

    Returns:
        ValidationResult对象
    """
    result = ValidationResult("配置和环境")

    # 自动检测路径
    if config_file is None:
        project_dir = get_project_dir()
        config_file = os.path.join(project_dir, "config/training_config.yaml")

    if verbose:
        print(f"验证配置文件: {config_file}")

    # 检查配置文件存在性
    if not os.path.isfile(config_file):
        result.add_error(f"配置文件不存在: {config_file}")
        # 继续其他验证
    else:
        # 尝试解析YAML
        try:
            import yaml
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)

            if verbose:
                print("  YAML格式正确")

            # 检查必需配置项
            required_keys = [
                ("training", "sft", "model_name"),
                ("training", "grpo", "model_path"),
                ("paths", "data_dir"),
            ]

            for key_path in required_keys:
                current = config
                try:
                    for key in key_path:
                        current = current[key]
                except (KeyError, TypeError):
                    result.add_error(
                        f"配置文件缺少必需配置项: {'.'.join(key_path)}"
                    )

        except ImportError:
            result.add_error("yaml包未安装，请运行: pip install pyyaml")
        except Exception as e:
            result.add_error(f"解析配置文件失败: {e}")

    # 检查Python包
    # 注意：unsloth 必须在 transformers 之前导入，以确保优化生效
    # 使用有序列表而非字典，确保导入顺序
    required_packages = [
        ("torch", "深度学习框架"),
        ("unsloth", "Unsloth优化库"),  # 必须在 transformers 之前
        ("transformers", "Hugging Face Transformers"),
        ("trl", "TRL强化学习训练库"),
    ]

    for package, description in required_packages:
        try:
            __import__(package)
            if verbose:
                print(f"  {package}: 已安装")
        except ImportError:
            result.add_error(f"{description} ({package}) 未安装")

    # 检查SUMO环境
    sumo_home = os.environ.get("SUMO_HOME")
    if not sumo_home:
        result.add_error("SUMO_HOME环境变量未设置")
    else:
        if verbose:
            print(f"  SUMO_HOME: {sumo_home}")

        # 检查sumo命令
        try:
            result_run = subprocess.run(
                ["sumo", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result_run.returncode == 0:
                if verbose:
                    print(f"  SUMO命令可用")
            else:
                result.add_warning("sumo命令不可用")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            result.add_warning("sumo命令不可用")

    return result


# ============== CLI入口 ==============

def parse_args():
    parser = argparse.ArgumentParser(
        description="数据验证脚本 - 在训练前快速检查数据集格式和正确性",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # 验证选项
    parser.add_argument(
        "--grpo-only",
        action="store_true",
        help="仅验证GRPO数据集"
    )
    parser.add_argument(
        "--sft-only",
        action="store_true",
        help="仅验证SFT数据集"
    )
    parser.add_argument(
        "--verify-sumo",
        action="store_true",
        help="验证SUMO状态文件（抽样）"
    )
    parser.add_argument(
        "--check-env",
        action="store_true",
        help="检查配置和依赖"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="显示详细进度信息"
    )

    # 环境选项
    parser.add_argument(
        "--container-mode",
        action="store_true",
        help="强制使用容器模式路径（/home/samuel/SCU_TSC）"
    )

    # 路径选项
    parser.add_argument(
        "--grpo-dir",
        type=str,
        default=None,
        help="GRPO数据集目录（默认: 自动检测）"
    )
    parser.add_argument(
        "--sft-file",
        type=str,
        default=None,
        help="SFT数据集文件（默认: 自动检测）"
    )
    parser.add_argument(
        "--config-file",
        type=str,
        default=None,
        help="配置文件（默认: 自动检测）"
    )
    parser.add_argument(
        "--sample-size",
        type=int,
        default=10,
        help="SUMO状态文件抽样数量 (默认: 10)"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    try:
        # 处理容器模式
        if args.container_mode:
            os.environ["VALIDATION_CONTAINER_MODE"] = "1"
            if args.verbose:
                print("容器模式：使用固定路径 /home/samuel/SCU_TSC")

        # 确定要运行的验证
        results = []

        if args.grpo_only:
            # 仅GRPO
            results.append(validate_grpo_dataset(args.grpo_dir, args.verbose))
        elif args.sft_only:
            # 仅SFT
            results.append(validate_sft_dataset(args.sft_file, args.verbose))
        elif args.check_env:
            # 仅环境检查
            results.append(validate_config_and_environment(args.config_file, args.verbose))
        elif args.verify_sumo:
            # 仅SUMO验证
            results.append(validate_sumo_state_files(args.grpo_dir, args.sample_size, args.verbose))
        else:
            # 默认：运行所有验证
            if args.verbose:
                print("运行所有验证...")

            results.append(validate_grpo_dataset(args.grpo_dir, args.verbose))
            results.append(validate_sft_dataset(args.sft_file, args.verbose))
            results.append(validate_sumo_state_files(args.grpo_dir, args.sample_size, args.verbose))
            results.append(validate_config_and_environment(args.config_file, args.verbose))

        # 收集所有输出
        all_outputs = []
        has_errors = False

        for result in results:
            output = result.format_output()
            if output:
                all_outputs.append(output)
                if result.has_errors():
                    has_errors = True

        # 输出结果
        if all_outputs:
            print("\n" + "\n".join(all_outputs), file=sys.stderr if has_errors else sys.stdout)
            return 1 if has_errors else 0
        else:
            # 所有验证通过，静默成功
            if args.verbose:
                print("\n✓ 所有验证通过")
            return 0

    except Exception as e:
        # 捕获意外错误
        print(f"[ERROR] 发生意外错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
