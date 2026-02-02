# -*- coding: utf-8 -*-
"""
Pytest共享fixture文件

提供测试中常用的fixture和测试数据工厂
"""

import pytest
import json
import tempfile
import os
from typing import Dict, Any, List, Callable
from pathlib import Path


# ============== 测试数据工厂fixture ==============

@pytest.fixture
def make_prompt() -> Callable[[Dict[str, Any]], str]:
    """
    工厂模式fixture：生成测试prompt数据

    Returns:
        返回一个函数，该函数接收字典参数并返回JSON字符串

    Examples:
        >>> make_prompt = request.getfixturevalue("make_prompt")
        >>> prompt = make_prompt({
        ...     "crossing_id": "cluster_11123112",
        ...     "state": {
        ...         "current_phase_id": 0,
        ...         "phase_metrics_by_id": {
        ...             0: {"avg_queue_veh": 10.0},
        ...             1: {"avg_queue_veh": 5.0}
        ...         }
        ...     },
        ...     "phase_order": [0, 1, 2, 3]
        ... })
    """
    def _factory(data: Dict[str, Any]) -> str:
        """将字典转换为JSON字符串"""
        return json.dumps(data, ensure_ascii=False)

    return _factory


@pytest.fixture
def format_reward_test_cases() -> Dict[str, List[Dict[str, Any]]]:
    """
    format_reward_fn的测试用例数据

    Returns:
        包含strict_valid, partial_valid, invalid三类测试用例的字典

    Examples:
        >>> cases = request.getfixturevalue("format_reward_test_cases")
        >>> strict_cases = cases["strict_valid"]
        >>> assert strict_cases[0]["output"] == '{"extend": "yes"}'
    """
    return {
        "strict_valid": [
            {"output": '{"extend": "yes"}', "expected_reward": 1.0, "expected_decision": "yes"},
            {"output": '{"extend": "no"}', "expected_reward": 1.0, "expected_decision": "no"},
            {"output": '{"extend":"yes"}', "expected_reward": 1.0, "expected_decision": "yes"},
            {"output": '{"extend":"no"}', "expected_reward": 1.0, "expected_decision": "no"},
        ],
        "partial_valid": [
            {"output": '{ "extend": "yes" }', "expected_reward": -0.5, "expected_decision": "yes"},
            {"output": '{\n  "extend": "no"\n}', "expected_reward": -0.5, "expected_decision": "no"},
            {"output": '{"extend": "yes", "extra": "field"}', "expected_reward": -0.5, "expected_decision": "yes"},
            {"output": 'Some text {"extend": "no"} more text', "expected_reward": -0.5, "expected_decision": "no"},
        ],
        "invalid": [
            {"output": "", "expected_reward": -10.0, "expected_decision": None},
            {"output": "not a json", "expected_reward": -10.0, "expected_decision": None},
            {"output": '{"wrong_key": "yes"}', "expected_reward": -10.0, "expected_decision": None},
            {"output": '{"extend": "invalid"}', "expected_reward": -10.0, "expected_decision": None},
            {"output": None, "expected_reward": -10.0, "expected_decision": None},
        ]
    }


@pytest.fixture
def max_pressure_test_cases() -> Dict[str, Any]:
    """
    Max Pressure算法的测试用例数据

    Returns:
        包含时间约束、压力决策、边界情况的测试数据

    Examples:
        >>> cases = request.getfixturevalue("max_pressure_test_cases")
        >>> time_constraints = cases["time_constraints"]
        >>> assert time_constraints["below_min"]["expected"] == "yes"
    """
    return {
        "time_constraints": {
            "below_min": {
                "green_elapsed": 5.0,
                "min_green": 10.0,
                "max_green": 60.0,
                "current_phase_id": 0,
                "phase_queues": {0: 5.0, 1: 10.0, 2: 3.0},
                "expected": "yes",  # 小于最小绿必须延长
            },
            "above_max": {
                "green_elapsed": 60.0,
                "min_green": 10.0,
                "max_green": 60.0,
                "current_phase_id": 0,
                "phase_queues": {0: 100.0, 1: 1.0, 2: 1.0},
                "expected": "no",  # 超过最大绿必须切换
            },
            "within_range": {
                "green_elapsed": 15.0,
                "min_green": 10.0,
                "max_green": 60.0,
                "current_phase_id": 0,
                "phase_queues": {0: 10.0, 1: 5.0, 2: 3.0},
                "expected": "yes",  # 当前相位排队最大
            },
        },
        "pressure_decision": {
            "current_highest": {
                "current_phase_id": 0,
                "phase_queues": {0: 10.0, 1: 5.0, 2: 3.0},
                "expected": "yes",
            },
            "other_highest": {
                "current_phase_id": 0,
                "phase_queues": {0: 5.0, 1: 10.0, 2: 3.0},
                "expected": "no",
            },
            "equal_queues": {
                "current_phase_id": 0,
                "phase_queues": {0: 5.0, 1: 5.0, 2: 5.0},
                "expected": "yes",  # 延长当前
            },
        },
        "edge_cases": {
            "single_phase": {
                "current_phase_id": 0,
                "phase_queues": {0: 10.0},
                "expected": "yes",
            },
            "negative_queues": {
                "current_phase_id": 0,
                "phase_queues": {0: 5.0, 1: -1.0, 2: 3.0},
                "expected": "yes",  # 当前相位最大
            },
        }
    }


@pytest.fixture(scope="module")
def sumo_test_data() -> Dict[str, Any]:
    """
    模块级SUMO测试数据fixture

    提供小规模SUMO仿真测试数据，避免重复创建

    Returns:
        包含SUMO状态文件路径和测试配置的字典

    Note:
        这个fixture使用scope="module"以在模块内共享数据
        实际SUMO测试需要在docker容器中运行
    """
    # 检查是否有实际的SUMO状态文件
    data_dir = Path(__file__).parent.parent / "fixtures" / "testdata"
    state_file = None

    if data_dir.exists():
        # 查找第一个.sumo.xml状态文件
        for f in data_dir.rglob("*.sumo.xml"):
            state_file = str(f)
            break

    return {
        "state_file": state_file,
        "has_sumo_data": state_file is not None,
        "test_scenarios_dir": "sumo_simulation/environments",
    }


@pytest.fixture
def temp_config_file() -> Callable[[Dict[str, Any]], str]:
    """
    临时配置文件fixture（自动清理）

    工厂模式fixture，创建临时YAML配置文件并在测试后自动清理

    Returns:
        返回一个函数，该函数接收配置字典并返回临时文件路径

    Yields:
        临时文件路径

    Examples:
        >>> make_config = request.getfixturevalue("temp_config_file")
        >>> config_path = make_config({"training": {"sft": {"learning_rate": 0.5}}})
        >>> # 使用config_path测试
        >>> # 测试结束后文件自动删除
    """
    import tempfile
    import yaml

    def _factory(config_data: Dict[str, Any]) -> str:
        """创建临时配置文件"""
        fd, path = tempfile.mkstemp(suffix='.yaml', text=True)
        try:
            with os.fdopen(fd, 'w') as f:
                yaml.dump(config_data, f, allow_unicode=True)
            return path
        except:
            os.close(fd)
            raise

    return _factory


@pytest.fixture
def sample_prompt_data() -> Dict[str, Any]:
    """
    标准样本prompt数据

    Returns:
        包含完整prompt结构的字典
    """
    return {
        "crossing_id": "cluster_11123112",
        "state": {
            "current_phase_id": 0,
            "phase_metrics_by_id": {
                0: {"avg_queue_veh": 10.0},
                1: {"avg_queue_veh": 5.0},
                2: {"avg_queue_veh": 3.0},
                3: {"avg_queue_veh": 7.0}
            }
        },
        "phase_order": [0, 1, 2, 3]
    }


@pytest.fixture
def sample_config_data() -> Dict[str, Any]:
    """
    标准训练配置数据

    Returns:
        包含完整训练配置的字典
    """
    return {
        "training": {
            "sft": {
                "model_name": "unsloth/Qwen2.5-0.5B-Instruct",
                "max_seq_length": 2048,
                "lora_rank": 32,
                "num_epochs": 3,
                "batch_size": 2,
                "gradient_accumulation_steps": 4,
                "learning_rate": 2.0e-4,
                "warmup_steps": 5,
                "optim": "adamw_8bit",
                "weight_decay": 0.001,
                "lr_scheduler_type": "linear",
                "seed": 3407,
                "logging_steps": 5,
                "save_steps": 50,
                "eval_percent": 0.05,
                "eval_limit": 100,
                "eval_steps": 30,
            },
            "grpo": {
                "model_path": "dummy",
                "max_seq_length": 2048,
                "learning_rate": 1.0e-5,
                "batch_size": 2,
                "gradient_accumulation_steps": 4,
                "num_generations": 4,
                "temperature": 0.9,
                "kl_coeff": 0.1,
                "max_new_tokens": 50,
                "top_p": 0.9,
                "repetition_penalty": 1.0,
                "num_train_epochs": 3,
                "warmup_steps": 10,
                "logging_steps": 5,
                "save_steps": 50,
                "optim": "adamw_8bit",
                "lora_rank": 32,
                "gradient_checkpointing": True,
                "seed": 3407,
            }
        },
        "simulation": {
            "sumo": {
                "time_step": 1.0,
                "max_time": 3600,
                "warmup_steps": 300,
                "extend_seconds": 5,
                "min_green_time": 10.0,
                "max_green_time": 60.0,
                "min_green_offset_range": 2.0,
                "max_green_offset_range": 5.0,
                "default_min_green": 10.0,
                "default_max_green": 60.0,
                "max_workers": 4,
                "port_range": [10000, 60000],
            }
        },
        "reward": {
            "chain": {
                "format_weight": 1.0,
                "tsc_weight": 1.0
            },
            "format": {
                "strict": 1.0,
                "partial": -0.5,
                "invalid": -10.0,
                "extract_regex": r'\{["\s]*extend["\s]*:\s*["\s]*(yes|no)["\s]*(?:,|\})'
            },
            "tsc": {
                "reward_scale": 10.0
            },
            "max_pressure": {
                "min_green_offset": 0.0,
                "max_green_override": False,
                "pressure_threshold": 0.0
            }
        },
        "paths": {
            "data_dir": "/home/samuel/SCU_TSC/data",
            "grpo_dataset_dir": "/home/samuel/SCU_TSC/data/grpo_datasets",
            "sft_dataset_dir": "/home/samuel/SCU_TSC/data/sft_datasets",
            "sft_model_dir": "/home/samuel/SCU_TSC/model/sft_model",
            "grpo_model_dir": "/home/samuel/SCU_TSC/model/grpo_model",
            "grpo_config": "/home/samuel/SCU_TSC/config/grpo_config.yaml",
        },
        "logging": {
            "use_wandb": False,
            "wandb_project": "scu-tsc-grpo",
            "wandb_run_name": None
        }
    }
