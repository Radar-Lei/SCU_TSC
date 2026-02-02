#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置读取辅助脚本

用法:
    python config/read_config.py --key simulation.sumo.max_workers
    python config/read_config.py --key parallel --default 4
"""

import argparse
import json
import sys
import os
from pathlib import Path

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


def read_yaml_config(config_path):
    """读取YAML配置文件"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_nested_value(data, key_path):
    """从嵌套字典中获取值

    Args:
        data: 配置字典
        key_path: 点分隔的键路径，如 'simulation.sumo.max_workers'

    Returns:
        找到的值，如果不存在则返回None
    """
    keys = key_path.split('.')
    value = data

    for key in keys:
        if isinstance(value, dict):
            value = value.get(key)
        else:
            return None

        if value is None:
            return None

    return value


def main():
    parser = argparse.ArgumentParser(
        description="从YAML配置文件读取参数值",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--config", "-c",
        type=str,
        default=str(PROJECT_ROOT / "config" / "training_config.yaml"),
        help=f"配置文件路径 (默认: config/training_config.yaml)"
    )

    parser.add_argument(
        "--key", "-k",
        type=str,
        required=True,
        help="要读取的配置键（支持点分隔路径，如 simulation.sumo.max_workers）"
    )

    parser.add_argument(
        "--default", "-d",
        type=str,
        default=None,
        help="默认值（如果键不存在）"
    )

    parser.add_argument(
        "--output", "-o",
        choices=["raw", "json", "export"],
        default="raw",
        help="输出格式: raw=原始值, json=JSON格式, export=shell export语句"
    )

    args = parser.parse_args()

    # 读取配置
    config = read_yaml_config(args.config)

    # 获取值
    value = get_nested_value(config, args.key)

    if value is None and args.default is not None:
        value = args.default

    # 输出
    if args.output == "raw":
        print(value)
    elif args.output == "json":
        print(json.dumps(value))
    elif args.output == "export":
        # 生成shell export语句
        key_upper = args.key.split('.')[-1].upper()
        print(f"export {key_upper}={value}")


if __name__ == "__main__":
    main()
