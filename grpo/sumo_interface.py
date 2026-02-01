# -*- coding: utf-8 -*-
"""
SUMO仿真接口封装

提供GRPO数据生成所需的SUMO操作接口，包括：
- 启动/关闭仿真
- 保存/加载仿真状态
- 获取相位信息（仅有效绿灯相位）
- 获取排队车辆数
"""

import os
import sys
import random
import socket
import xml.etree.ElementTree as ET
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass

# 配置 SUMO_HOME
if 'SUMO_HOME' not in os.environ:
    possible_paths = [
        "/usr/share/sumo",
        "/usr/local/share/sumo",
        "/usr/lib/sumo",
        "/opt/homebrew/opt/sumo/share/sumo",
        "/usr/local/opt/sumo/share/sumo",
    ]
    for path in possible_paths:
        if os.path.exists(path):
            os.environ['SUMO_HOME'] = path
            break

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)

try:
    import traci
    from traci.exceptions import TraCIException
except ImportError:
    sys.exit("错误: 无法导入 traci。请检查 SUMO 是否安装或运行 'pip install traci'")


def find_available_port(start: int = 10000, end: int = 60000, max_attempts: int = 100) -> Optional[int]:
    """
    查找可用端口

    尝试绑定端口来检测是否可用。

    Args:
        start: 起始端口号
        end: 结束端口号
        max_attempts: 最大尝试次数

    Returns:
        可用端口号，失败返回None
    """
    for _ in range(max_attempts):
        port = random.randint(start, end)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            continue
    return None


@dataclass
class PhaseInfo:
    """相位信息"""
    phase_id: int           # 相位在SUMO程序中的索引
    state: str              # 相位状态字符串 (如 "GGGrrr")
    duration: float         # 相位持续时间
    min_dur: float          # 最小持续时间
    max_dur: float          # 最大持续时间
    controlled_lanes: List[str]  # 该相位控制的车道（绿灯车道）


class SUMOInterface:
    """SUMO仿真接口"""
    
    def __init__(self, config_file: str, port: Optional[int] = None, 
                 gui: bool = False, verbose: bool = False):
        """
        初始化SUMO接口
        
        Args:
            config_file: SUMO配置文件路径 (.sumocfg)
            port: TraCI端口号（None则随机选择）
            gui: 是否使用GUI
            verbose: 是否输出详细日志
        """
        self.config_file = os.path.abspath(config_file)
        self.port = port
        self.gui = gui
        self.verbose = verbose
        self.connected = False
        
        # 解析配置文件获取网络文件路径
        self.net_file = self._parse_net_file()
        
        # 缓存相位信息
        self._phase_cache: Dict[str, List[PhaseInfo]] = {}
        
    def _parse_net_file(self) -> Optional[str]:
        """从sumocfg解析网络文件路径"""
        try:
            tree = ET.parse(self.config_file)
            root = tree.getroot()
            for elem in root.iter('net-file'):
                net_file = elem.get('value')
                if net_file:
                    config_dir = os.path.dirname(self.config_file)
                    return os.path.join(config_dir, net_file)
        except Exception as e:
            if self.verbose:
                print(f"解析配置文件失败: {e}")
        return None
    
    def start(self, warmup_steps: int = 0) -> bool:
        """
        启动SUMO仿真

        Args:
            warmup_steps: 预热步数

        Returns:
            是否启动成功
        """
        try:
            # 关闭已有连接
            if self.connected:
                self.close()

            # 查找SUMO可执行文件
            binary_name = "sumo-gui" if self.gui else "sumo"
            sumo_binary = self._find_sumo_binary(binary_name)

            # 构建启动命令
            sumo_cmd = [
                sumo_binary,
                "-c", self.config_file,
                "--step-length", "1.0",
                "--no-warnings", "true",
                "--start",
                "--no-step-log",
                "--duration-log.disable", "true",
            ]

            # 启动SUMO（带重试）
            max_retries = 10 if self.port is None else 3
            for attempt in range(max_retries):
                try:
                    # 如果端口未指定，使用find_available_port查找
                    port = self.port
                    if port is None:
                        port = find_available_port()
                        if port is None:
                            print("无法找到可用端口")
                            return False

                    if self.verbose:
                        print(f"启动SUMO，端口: {port} (尝试 {attempt+1}/{max_retries})")

                    traci.start(sumo_cmd, port=port)
                    self.connected = True

                    # 执行预热
                    for _ in range(warmup_steps):
                        traci.simulationStep()

                    if self.verbose:
                        print(f"SUMO启动成功，已预热 {warmup_steps} 步")
                    return True

                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    import time
                    time.sleep(random.random() * 0.5)

        except Exception as e:
            print(f"启动SUMO失败: {e}")
            self.connected = False
            return False

        return False
    
    def _find_sumo_binary(self, binary_name: str) -> str:
        """查找SUMO可执行文件"""
        candidates = [
            os.path.join(os.environ.get('SUMO_HOME', ''), 'bin', binary_name),
            f"/usr/bin/{binary_name}",
            f"/usr/local/bin/{binary_name}",
            f"/opt/homebrew/bin/{binary_name}",
        ]
        for path in candidates:
            if os.path.exists(path):
                return path
        return binary_name  # 使用PATH中的命令
    
    def close(self):
        """关闭仿真连接"""
        try:
            if self.connected:
                traci.close()
        except Exception:
            pass
        finally:
            self.connected = False

    def start_from_state(self, state_file: str, port: Optional[int] = None) -> bool:
        """
        从状态文件恢复并启动仿真

        Args:
            state_file: 状态文件路径
            port: TraCI端口（None则使用实例的port或随机选择）

        Returns:
            是否启动成功
        """
        if not self.start(port=port):
            return False
        return self.load_state(state_file)
    
    def step(self) -> bool:
        """
        执行一步仿真
        
        Returns:
            仿真是否仍在运行
        """
        try:
            if not self.connected:
                return False
            traci.simulationStep()
            # 检查仿真是否结束
            return traci.simulation.getMinExpectedNumber() > 0
        except TraCIException:
            return False
    
    def get_simulation_time(self) -> float:
        """获取当前仿真时间"""
        try:
            return traci.simulation.getTime()
        except TraCIException:
            return 0.0
    
    def save_state(self, filepath: str) -> bool:
        """
        保存仿真状态
        
        Args:
            filepath: 状态文件保存路径
            
        Returns:
            是否保存成功
        """
        try:
            traci.simulation.saveState(filepath)
            return True
        except TraCIException as e:
            print(f"保存仿真状态失败: {e}")
            return False
    
    def load_state(self, filepath: str) -> bool:
        """
        加载仿真状态
        
        Args:
            filepath: 状态文件路径
            
        Returns:
            是否加载成功
        """
        try:
            traci.simulation.loadState(filepath)
            return True
        except TraCIException as e:
            print(f"加载仿真状态失败: {e}")
            return False
    
    def get_traffic_lights(self) -> List[str]:
        """获取所有信号灯ID"""
        try:
            return list(traci.trafficlight.getIDList())
        except TraCIException:
            return []
    
    def get_valid_phases(self, tl_id: str, config: Any = None) -> List[PhaseInfo]:
        """
        获取信号灯的有效相位列表（只包含有绿灯的相位）
        
        Args:
            tl_id: 信号灯ID
            config: GRPOConfig配置对象，用于获取默认min/max green
            
        Returns:
            有效相位列表
        """
        # 检查缓存
        if tl_id in self._phase_cache:
            return self._phase_cache[tl_id]
        
        try:
            # 获取相位定义
            logics = traci.trafficlight.getAllProgramLogics(tl_id)
            if not logics:
                return []
            
            phases = logics[0].phases
            controlled_links = traci.trafficlight.getControlledLinks(tl_id)
            
            valid_phases = []
            for idx, phase in enumerate(phases):
                state = phase.state
                
                # 检查是否有绿灯 ('G' 或 'g')
                if 'G' not in state and 'g' not in state:
                    continue  # 跳过无绿灯的相位（如纯黄灯或全红）
                
                # 获取绿灯控制的车道
                green_lanes = []
                for i, char in enumerate(state):
                    if char in ['G', 'g'] and i < len(controlled_links):
                        if controlled_links[i]:
                            from_lane = controlled_links[i][0][0]
                            if from_lane not in green_lanes:
                                green_lanes.append(from_lane)
                
                # 获取min/max duration
                min_dur = getattr(phase, 'minDur', None)
                max_dur = getattr(phase, 'maxDur', None)
                
                # 使用默认值
                if config:
                    if min_dur is None or min_dur <= 0:
                        min_dur = config.default_min_green
                    if max_dur is None or max_dur <= 0:
                        max_dur = config.default_max_green
                else:
                    if min_dur is None or min_dur <= 0:
                        min_dur = 10.0
                    if max_dur is None or max_dur <= 0:
                        max_dur = 60.0
                
                phase_info = PhaseInfo(
                    phase_id=idx,
                    state=state,
                    duration=phase.duration,
                    min_dur=min_dur,
                    max_dur=max_dur,
                    controlled_lanes=green_lanes
                )
                valid_phases.append(phase_info)
            
            # 缓存结果
            self._phase_cache[tl_id] = valid_phases
            return valid_phases
            
        except TraCIException as e:
            print(f"获取相位信息失败: {e}")
            return []
    
    def get_current_phase_index(self, tl_id: str) -> int:
        """获取当前相位索引（SUMO内部索引）"""
        try:
            return traci.trafficlight.getPhase(tl_id)
        except TraCIException:
            return 0
    
    def get_phase_elapsed_time(self, tl_id: str) -> float:
        """
        获取当前相位已持续的时间
        
        Returns:
            当前相位已持续时间（秒）
        """
        try:
            # getPhaseDuration 返回总时长，getNextSwitch 返回切换时刻
            phase_duration = traci.trafficlight.getPhaseDuration(tl_id)
            next_switch = traci.trafficlight.getNextSwitch(tl_id)
            current_time = traci.simulation.getTime()
            remaining = next_switch - current_time
            elapsed = phase_duration - remaining
            return max(0.0, elapsed)
        except TraCIException:
            return 0.0
    
    def set_phase(self, tl_id: str, phase_index: int):
        """设置信号灯相位"""
        try:
            traci.trafficlight.setPhase(tl_id, phase_index)
        except TraCIException as e:
            print(f"设置相位失败: {e}")
    
    def extend_phase(self, tl_id: str, extend_seconds: float):
        """
        延长当前相位
        
        Args:
            tl_id: 信号灯ID
            extend_seconds: 延长秒数
        """
        try:
            current_duration = traci.trafficlight.getPhaseDuration(tl_id)
            new_duration = current_duration + extend_seconds
            traci.trafficlight.setPhaseDuration(tl_id, new_duration)
        except TraCIException as e:
            print(f"延长相位失败: {e}")
    
    def get_lane_queue_count(self, lane_id: str) -> int:
        """获取车道排队车辆数（停止的车辆）"""
        try:
            return traci.lane.getLastStepHaltingNumber(lane_id)
        except TraCIException:
            return 0
    
    def get_phase_avg_queue(self, tl_id: str, phase_index: int) -> float:
        """
        获取指定相位控制车道的平均排队车辆数
        
        Args:
            tl_id: 信号灯ID
            phase_index: 相位索引（SUMO内部索引）
            
        Returns:
            平均排队车辆数
        """
        try:
            # 获取相位信息
            valid_phases = self.get_valid_phases(tl_id)
            target_phase = None
            for p in valid_phases:
                if p.phase_id == phase_index:
                    target_phase = p
                    break
            
            if not target_phase or not target_phase.controlled_lanes:
                return 0.0
            
            total_queue = sum(
                self.get_lane_queue_count(lane) 
                for lane in target_phase.controlled_lanes
            )
            return total_queue / len(target_phase.controlled_lanes)
            
        except Exception:
            return 0.0
    
    def get_all_phases_queue(self, tl_id: str) -> Dict[int, float]:
        """
        获取所有有效相位的平均排队车辆数
        
        Returns:
            {phase_id: avg_queue_veh}
        """
        result = {}
        valid_phases = self.get_valid_phases(tl_id)
        for phase in valid_phases:
            result[phase.phase_id] = self.get_phase_avg_queue(tl_id, phase.phase_id)
        return result
    
    def get_total_queue_count(self, tl_id: str) -> int:
        """获取信号灯控制的所有车道的总排队车辆数"""
        try:
            controlled_lanes = traci.trafficlight.getControlledLanes(tl_id)
            total = 0
            for lane in set(controlled_lanes):
                total += self.get_lane_queue_count(lane)
            return total
        except TraCIException:
            return 0
