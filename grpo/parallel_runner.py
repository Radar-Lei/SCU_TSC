# -*- coding: utf-8 -*-
"""
并行执行器

使用multiprocessing并行运行多个场景的数据生成。
"""

import os
import json
from multiprocessing import Pool
from typing import List, Optional
from dataclasses import asdict

from .config import GRPOConfig
from .dataset_generator import GRPODatasetGenerator, run_single_scenario


class ParallelRunner:
    """并行执行器"""
    
    def __init__(self, config: Optional[GRPOConfig] = None):
        """
        初始化并行执行器
        
        Args:
            config: 配置对象
        """
        self.config = config or GRPOConfig()
    
    def get_all_scenarios(self) -> List[str]:
        """
        获取所有可用的场景名称
        
        Returns:
            场景名称列表
        """
        scenarios_dir = self.config.scenarios_dir
        if not os.path.isdir(scenarios_dir):
            return []
        
        scenarios = []
        for name in os.listdir(scenarios_dir):
            scenario_path = os.path.join(scenarios_dir, name)
            if os.path.isdir(scenario_path):
                # 检查是否有.sumocfg文件
                has_sumocfg = any(f.endswith('.sumocfg') for f in os.listdir(scenario_path))
                if has_sumocfg:
                    scenarios.append(name)
        
        return sorted(scenarios)
    
    def filter_scenarios(self, scenarios: Optional[List[str]] = None) -> List[str]:
        """
        过滤场景列表
        
        Args:
            scenarios: 指定的场景列表，None则使用所有场景
            
        Returns:
            过滤后的场景列表
        """
        all_scenarios = self.get_all_scenarios()
        
        # 如果指定了场景列表
        if scenarios:
            filtered = [s for s in scenarios if s in all_scenarios]
        elif self.config.scenarios:
            filtered = [s for s in self.config.scenarios if s in all_scenarios]
        else:
            filtered = all_scenarios
        
        # 排除指定场景
        if self.config.exclude_scenarios:
            filtered = [s for s in filtered if s not in self.config.exclude_scenarios]
        
        return filtered
    
    def run(self, scenarios: Optional[List[str]] = None) -> dict:
        """
        并行运行多个场景的数据生成
        
        Args:
            scenarios: 场景列表，None则使用所有场景
            
        Returns:
            {scenario_name: entry_count}
        """
        scenarios_to_run = self.filter_scenarios(scenarios)
        
        if not scenarios_to_run:
            print("没有找到可运行的场景")
            return {}
        
        print(f"准备运行 {len(scenarios_to_run)} 个场景:")
        for s in scenarios_to_run:
            print(f"  - {s}")
        
        # 准备并行参数
        config_dict = asdict(self.config)
        base_port = 20000
        
        tasks = []
        for i, scenario_name in enumerate(scenarios_to_run):
            output_dir = os.path.join(self.config.output_dir, scenario_name)
            port = base_port + i * 10  # 每个场景使用不同端口段
            tasks.append((scenario_name, config_dict, output_dir, port))
        
        # 并行执行
        results = {}
        num_workers = min(self.config.num_workers, len(tasks))
        
        print(f"\n使用 {num_workers} 个进程并行执行...")
        
        if num_workers <= 1:
            # 串行执行
            for task in tasks:
                scenario_name = task[0]
                entries = run_single_scenario(task)
                results[scenario_name] = len(entries)
        else:
            # 并行执行
            with Pool(processes=num_workers) as pool:
                all_entries = pool.map(run_single_scenario, tasks)
            
            for task, entries in zip(tasks, all_entries):
                scenario_name = task[0]
                results[scenario_name] = len(entries)
        
        # 汇总结果
        print("\n=== 生成结果汇总 ===")
        total = 0
        for scenario, count in sorted(results.items()):
            print(f"  {scenario}: {count} 条数据")
            total += count
        print(f"  总计: {total} 条数据")
        
        # 保存汇总结果
        summary_file = os.path.join(self.config.output_dir, "generation_summary.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump({
                "scenarios": results,
                "total": total,
                "config": config_dict
            }, f, ensure_ascii=False, indent=2)
        print(f"\n汇总结果已保存: {summary_file}")
        
        return results


def run_parallel(
    scenarios: Optional[List[str]] = None,
    config: Optional[GRPOConfig] = None
) -> dict:
    """
    便捷函数：并行运行数据生成
    
    Args:
        scenarios: 场景列表
        config: 配置对象
        
    Returns:
        {scenario_name: entry_count}
    """
    runner = ParallelRunner(config)
    return runner.run(scenarios)
