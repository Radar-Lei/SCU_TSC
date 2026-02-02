#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_data.py的单元测试

测试各种错误检测功能：
- GRPO数据集格式错误
- SFT数据集格式错误
- SUMO状态文件损坏
- 配置文件错误
"""

import os
import sys
import json
import tempfile
import shutil
import unittest
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from grpo.validate_data import (
    validate_grpo_dataset,
    validate_sft_dataset,
    validate_sumo_state_files,
    validate_config_and_environment,
    ValidationResult
)


class TestValidationResult(unittest.TestCase):
    """测试ValidationResult类"""

    def test_valid_result(self):
        """测试验证通过的情况"""
        result = ValidationResult("测试类别")
        self.assertTrue(result.is_valid())
        self.assertFalse(result.has_errors())
        self.assertEqual(result.format_output(), "")

    def test_error_result(self):
        """测试错误情况"""
        result = ValidationResult("测试类别")
        result.add_error("错误信息")
        self.assertFalse(result.is_valid())
        self.assertTrue(result.has_errors())
        output = result.format_output()
        self.assertIn("ERROR", output)
        self.assertIn("错误信息", output)

    def test_warning_result(self):
        """测试警告情况"""
        result = ValidationResult("测试类别")
        result.add_warning("警告信息")
        self.assertTrue(result.is_valid())  # 警告不影响有效性
        self.assertTrue(result.has_warnings())
        output = result.format_output()
        self.assertIn("WARNING", output)
        self.assertIn("警告信息", output)


class TestGRPOValidation(unittest.TestCase):
    """测试GRPO数据集验证"""

    def setUp(self):
        """创建临时测试目录"""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """清理临时目录"""
        shutil.rmtree(self.test_dir)

    def test_missing_directory(self):
        """测试目录不存在的情况"""
        result = validate_grpo_dataset(os.path.join(self.test_dir, "nonexistent"))
        self.assertFalse(result.is_valid())
        self.assertTrue(any("不存在" in err for err in result.errors))

    def test_empty_directory(self):
        """测试空目录"""
        result = validate_grpo_dataset(self.test_dir)
        self.assertFalse(result.is_valid())
        self.assertTrue(any("为空" in err for err in result.errors))

    def test_missing_dataset_file(self):
        """测试缺少grpo_dataset.json文件"""
        # 创建场景目录但没有数据集文件
        scenario_dir = os.path.join(self.test_dir, "test_scenario")
        os.makedirs(scenario_dir)

        result = validate_grpo_dataset(self.test_dir)
        self.assertFalse(result.is_valid())
        self.assertTrue(any("grpo_dataset.json文件不存在" in err for err in result.errors))

    def test_invalid_json(self):
        """测试无效JSON格式"""
        scenario_dir = os.path.join(self.test_dir, "test_scenario")
        os.makedirs(scenario_dir)
        dataset_file = os.path.join(scenario_dir, "grpo_dataset.json")

        # 写入无效JSON
        with open(dataset_file, 'w') as f:
            f.write("{invalid json")

        result = validate_grpo_dataset(self.test_dir)
        self.assertFalse(result.is_valid())
        self.assertTrue(any("JSON格式错误" in err for err in result.errors))

    def test_wrong_data_type(self):
        """测试数据类型错误（应该是数组）"""
        scenario_dir = os.path.join(self.test_dir, "test_scenario")
        os.makedirs(scenario_dir)
        dataset_file = os.path.join(scenario_dir, "grpo_dataset.json")

        # 写入对象而非数组
        with open(dataset_file, 'w') as f:
            json.dump({"not": "an array"}, f)

        result = validate_grpo_dataset(self.test_dir)
        self.assertFalse(result.is_valid())
        self.assertTrue(any("数组格式" in err for err in result.errors))

    def test_insufficient_data(self):
        """测试数据量不足"""
        scenario_dir = os.path.join(self.test_dir, "test_scenario")
        os.makedirs(scenario_dir)
        dataset_file = os.path.join(scenario_dir, "grpo_dataset.json")

        # 写入少于10条数据
        data = [
            {
                "id": "test_1",
                "prompt": "test prompt",
                "scenario": "test_scenario",
                "junction_id": "test_junction",
                "state_file": "test.xml"
            }
        ] * 5  # 只有5条

        with open(dataset_file, 'w') as f:
            json.dump(data, f)

        result = validate_grpo_dataset(self.test_dir)
        self.assertFalse(result.is_valid())
        self.assertTrue(any("数据量不足" in err for err in result.errors))

    def test_missing_required_fields(self):
        """测试缺少必需字段"""
        scenario_dir = os.path.join(self.test_dir, "test_scenario")
        os.makedirs(scenario_dir)
        dataset_file = os.path.join(scenario_dir, "grpo_dataset.json")

        # 创建缺少prompt字段的数据
        data = [
            {
                "id": f"test_{i}",
                "scenario": "test_scenario",
                "junction_id": "test_junction",
                "state_file": "test.xml"
            }
            for i in range(10)
        ]

        with open(dataset_file, 'w') as f:
            json.dump(data, f)

        result = validate_grpo_dataset(self.test_dir)
        self.assertFalse(result.is_valid())
        self.assertTrue(any("缺少prompt字段" in err for err in result.errors))

    def test_wrong_field_type(self):
        """测试字段类型错误"""
        scenario_dir = os.path.join(self.test_dir, "test_scenario")
        os.makedirs(scenario_dir)
        dataset_file = os.path.join(scenario_dir, "grpo_dataset.json")

        # 创建id为数字而非字符串的数据
        data = [
            {
                "id": i,  # 应该是字符串
                "prompt": "test prompt",
                "scenario": "test_scenario",
                "junction_id": "test_junction",
                "state_file": "test.xml"
            }
            for i in range(10)
        ]

        with open(dataset_file, 'w') as f:
            json.dump(data, f)

        result = validate_grpo_dataset(self.test_dir)
        self.assertFalse(result.is_valid())
        self.assertTrue(any("id字段类型错误" in err for err in result.errors))

    def test_empty_prompt(self):
        """测试prompt为空"""
        scenario_dir = os.path.join(self.test_dir, "test_scenario")
        os.makedirs(scenario_dir)
        dataset_file = os.path.join(scenario_dir, "grpo_dataset.json")

        # 创建空prompt的数据
        data = [
            {
                "id": f"test_{i}",
                "prompt": "   ",  # 空白字符串
                "scenario": "test_scenario",
                "junction_id": "test_junction",
                "state_file": "test.xml"
            }
            for i in range(10)
        ]

        with open(dataset_file, 'w') as f:
            json.dump(data, f)

        result = validate_grpo_dataset(self.test_dir)
        self.assertFalse(result.is_valid())
        self.assertTrue(any("prompt字段为空" in err for err in result.errors))

    def test_missing_state_file(self):
        """测试state_file文件不存在"""
        scenario_dir = os.path.join(self.test_dir, "test_scenario")
        os.makedirs(scenario_dir)
        dataset_file = os.path.join(scenario_dir, "grpo_dataset.json")

        # 创建引用不存在的state_file的数据
        data = [
            {
                "id": f"test_{i}",
                "prompt": "test prompt",
                "scenario": "test_scenario",
                "junction_id": "test_junction",
                "state_file": "nonexistent/state.xml"  # 不存在
            }
            for i in range(10)
        ]

        with open(dataset_file, 'w') as f:
            json.dump(data, f)

        result = validate_grpo_dataset(self.test_dir)
        self.assertFalse(result.is_valid())
        self.assertTrue(any("state_file不存在" in err for err in result.errors))

    def test_valid_dataset(self):
        """测试有效的GRPO数据集"""
        scenario_dir = os.path.join(self.test_dir, "test_scenario")
        os.makedirs(scenario_dir)
        dataset_file = os.path.join(scenario_dir, "grpo_dataset.json")

        # 创建state_file
        state_file_dir = os.path.join(scenario_dir, "states")
        os.makedirs(state_file_dir)
        state_file = os.path.join(state_file_dir, "state.xml")
        with open(state_file, 'w') as f:
            f.write('<snapshot/>')

        # 创建有效数据
        data = [
            {
                "id": f"test_{i}",
                "prompt": "test prompt",
                "scenario": "test_scenario",
                "junction_id": "test_junction",
                "state_file": "states/state.xml"
            }
            for i in range(10)
        ]

        with open(dataset_file, 'w') as f:
            json.dump(data, f)

        result = validate_grpo_dataset(self.test_dir)
        self.assertTrue(result.is_valid())
        self.assertEqual(result.format_output(), "")


class TestSFTValidation(unittest.TestCase):
    """测试SFT数据集验证"""

    def setUp(self):
        """创建临时测试文件"""
        self.test_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.test_path = self.test_file.name
        self.test_file.close()

    def tearDown(self):
        """删除临时文件"""
        if os.path.exists(self.test_path):
            os.unlink(self.test_path)

    def test_missing_file(self):
        """测试文件不存在"""
        result = validate_sft_dataset("/nonexistent/sft_dataset.json")
        self.assertFalse(result.is_valid())
        self.assertTrue(any("不存在" in err for err in result.errors))

    def test_invalid_json(self):
        """测试无效JSON"""
        with open(self.test_path, 'w') as f:
            f.write("{invalid json")

        result = validate_sft_dataset(self.test_path)
        self.assertFalse(result.is_valid())
        self.assertTrue(any("JSON格式错误" in err for err in result.errors))

    def test_wrong_data_type(self):
        """测试数据类型错误"""
        with open(self.test_path, 'w') as f:
            json.dump({"not": "an array"}, f)

        result = validate_sft_dataset(self.test_path)
        self.assertFalse(result.is_valid())
        self.assertTrue(any("数组格式" in err for err in result.errors))

    def test_missing_required_fields(self):
        """测试缺少必需字段"""
        data = [
            {
                "id": "test_1",
                "messages": []  # 缺少scenario
            }
        ]

        with open(self.test_path, 'w') as f:
            json.dump(data, f)

        result = validate_sft_dataset(self.test_path)
        self.assertFalse(result.is_valid())
        self.assertTrue(any("缺少scenario字段" in err or "缺少messages字段" in err
                          for err in result.errors))

    def test_insufficient_messages(self):
        """测试messages数量不足"""
        data = [
            {
                "id": "test_1",
                "messages": [
                    {"role": "system", "content": "system"},
                    {"role": "user", "content": "user"}
                    # 缺少assistant
                ],
                "scenario": "test"
            }
        ]

        with open(self.test_path, 'w') as f:
            json.dump(data, f)

        result = validate_sft_dataset(self.test_path)
        self.assertFalse(result.is_valid())
        self.assertTrue(any("messages数量不足" in err for err in result.errors))

    def test_missing_required_roles(self):
        """测试缺少必需的role"""
        data = [
            {
                "id": "test_1",
                "messages": [
                    {"role": "system", "content": "system"},
                    {"role": "user", "content": "user"},
                    {"role": "user", "content": "user2"}  # 应该是assistant
                ],
                "scenario": "test"
            }
        ]

        with open(self.test_path, 'w') as f:
            json.dump(data, f)

        result = validate_sft_dataset(self.test_path)
        self.assertFalse(result.is_valid())
        self.assertTrue(any("缺少必需role" in err and "assistant" in err
                          for err in result.errors))

    def test_invalid_assistant_content_format(self):
        """测试assistant.content格式错误"""
        data = [
            {
                "id": "test_1",
                "messages": [
                    {"role": "system", "content": "system"},
                    {"role": "user", "content": "user"},
                    {"role": "assistant", "content": "not json"}  # 不是JSON
                ],
                "scenario": "test"
            }
        ]

        with open(self.test_path, 'w') as f:
            json.dump(data, f)

        result = validate_sft_dataset(self.test_path)
        self.assertFalse(result.is_valid())
        self.assertTrue(any("不是有效JSON" in err for err in result.errors))

    def test_invalid_extend_value(self):
        """测试extend字段值错误"""
        data = [
            {
                "id": "test_1",
                "messages": [
                    {"role": "system", "content": "system"},
                    {"role": "user", "content": "user"},
                    {"role": "assistant", "content": '{"extend": "maybe"}'}  # 应该是yes/no
                ],
                "scenario": "test"
            }
        ]

        with open(self.test_path, 'w') as f:
            json.dump(data, f)

        result = validate_sft_dataset(self.test_path)
        self.assertFalse(result.is_valid())
        self.assertTrue(any("extend字段值应该是" in err for err in result.errors))

    def test_valid_sft_dataset(self):
        """测试有效的SFT数据集"""
        data = [
            {
                "id": f"test_{i}",
                "messages": [
                    {"role": "system", "content": "system prompt"},
                    {"role": "user", "content": "user prompt"},
                    {"role": "assistant", "content": '{"extend": "yes"}'}
                ],
                "scenario": "test"
            }
            for i in range(10)
        ]

        with open(self.test_path, 'w') as f:
            json.dump(data, f)

        result = validate_sft_dataset(self.test_path)
        self.assertTrue(result.is_valid())
        self.assertEqual(result.format_output(), "")


class TestSUMOValidation(unittest.TestCase):
    """测试SUMO状态文件验证"""

    def setUp(self):
        """创建临时测试目录"""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """清理临时目录"""
        shutil.rmtree(self.test_dir)

    def test_missing_directory(self):
        """测试目录不存在"""
        result = validate_sumo_state_files(os.path.join(self.test_dir, "nonexistent"))
        self.assertFalse(result.is_valid())
        self.assertTrue(any("不存在" in err for err in result.errors))

    def test_no_state_files(self):
        """测试没有state_file的情况"""
        # 创建空目录
        scenario_dir = os.path.join(self.test_dir, "test_scenario")
        os.makedirs(scenario_dir)

        result = validate_sumo_state_files(self.test_dir, sample_size=10)
        self.assertFalse(result.is_valid())
        self.assertTrue(any("没有找到任何state_file" in err for err in result.errors))

    def test_missing_state_file(self):
        """测试state_file文件不存在"""
        scenario_dir = os.path.join(self.test_dir, "test_scenario")
        os.makedirs(scenario_dir)
        dataset_file = os.path.join(scenario_dir, "grpo_dataset.json")

        # 创建引用不存在state_file的数据
        data = [
            {
                "id": "test_1",
                "prompt": "test",
                "scenario": "test_scenario",
                "junction_id": "test",
                "state_file": "nonexistent/state.xml"
            }
        ]

        with open(dataset_file, 'w') as f:
            json.dump(data, f)

        result = validate_sumo_state_files(self.test_dir, sample_size=10)
        self.assertFalse(result.is_valid())
        self.assertTrue(any("文件不存在" in err for err in result.errors))

    def test_invalid_xml(self):
        """测试无效XML"""
        scenario_dir = os.path.join(self.test_dir, "test_scenario")
        os.makedirs(scenario_dir)
        dataset_file = os.path.join(scenario_dir, "grpo_dataset.json")
        state_file = os.path.join(scenario_dir, "state.xml")

        # 创建无效XML
        with open(state_file, 'w') as f:
            f.write("<invalid>")

        data = [
            {
                "id": "test_1",
                "prompt": "test",
                "scenario": "test_scenario",
                "junction_id": "test",
                "state_file": "state.xml"
            }
        ]

        with open(dataset_file, 'w') as f:
            json.dump(data, f)

        result = validate_sumo_state_files(self.test_dir, sample_size=10)
        self.assertFalse(result.is_valid())
        self.assertTrue(any("XML解析失败" in err for err in result.errors))

    def test_valid_state_files(self):
        """测试有效的状态文件"""
        scenario_dir = os.path.join(self.test_dir, "test_scenario")
        os.makedirs(scenario_dir)
        dataset_file = os.path.join(scenario_dir, "grpo_dataset.json")
        state_file = os.path.join(scenario_dir, "state.xml")

        # 创建有效XML
        with open(state_file, 'w') as f:
            f.write('<snapshot/>')

        data = [
            {
                "id": "test_1",
                "prompt": "test",
                "scenario": "test_scenario",
                "junction_id": "test",
                "state_file": "state.xml"
            }
        ]

        with open(dataset_file, 'w') as f:
            json.dump(data, f)

        result = validate_sumo_state_files(self.test_dir, sample_size=10)
        self.assertTrue(result.is_valid())
        self.assertEqual(result.format_output(), "")


if __name__ == "__main__":
    # 运行测试
    unittest.main(verbosity=2)
