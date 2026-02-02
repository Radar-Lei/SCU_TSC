# 技术债务与关注点

## 概述

该文档记录当前代码库中的技术债务、已知问题和需要关注的领域。

## 技术债务

### 配置管理
- **硬编码路径**: `sumo_simulator.py` 和 `sumo_interface.py` 中存在多个硬编码的 SUMO 安装路径
  - 影响文件: `sumo_simulation/sumo_simulator.py:21-35`, `grpo/sumo_interface.py:22-32`
  - 建议: 使用环境变量或配置文件统一管理

### 代码重复
- **SUMO_HOME 配置重复**: 在多个文件中重复相同的 SUMO_HOME 路径查找逻辑
  - 影响文件: `sumo_simulator.py`, `sumo_interface.py`
  - 建议: 提取到共享工具模块

### 错误处理
- **广泛的 try-except 块**: 多处使用 `except Exception` 捕获所有异常
  - 影响文件: `grpo/sumo_interface.py`, `sumo_simulation/sumo_simulator.py`
  - 建议: 使用更具体的异常类型

## 性能关注点

### 缓存机制
- **相位信息缓存**: `SUMOInterface._phase_cache` 缓存机制有效，但缺少缓存失效策略
  - 位置: `grpo/sumo_interface.py:105`

### 并行处理
- **端口冲突**: 并行运行时可能存在端口冲突风险
  - 位置: `grpo/sumo_interface.py:45-67`
  - 缓解措施: 已实现随机端口查找机制

### 大文件
- **大型自动生成文件**: `unsloth_compiled_cache/` 包含大量自动生成的训练器代码（约 42K 行总计）
  - 影响: 代码库体积大，可能影响 git 性能
  - 建议: 考虑添加到 `.gitignore` 或使用 git-lfs

## 安全关注点

### 输入验证
- **路径注入风险**: 文件路径处理缺少充分的验证
  - 影响: 配置文件加载、状态文件保存/加载
  - 建议: 添加路径验证和白名单机制

### 依赖管理
- **未锁定版本**: 部分依赖可能未指定具体版本
  - 建议: 使用 `requirements.txt` 或 `poetry.lock` 锁定依赖版本

## 可维护性关注点

### 文档
- **中文注释与文档混用**: 代码注释和文档字符串混用中英文
  - 影响: 国际化协作可能受限
  - 建议: 统一使用英文或建立文档标准

### 测试覆盖
- **测试文件分散**: 测试文件（如 `test_stratified_split.py`）存在于根目录而非专门的测试目录
  - 建议: 建立 `tests/` 目录结构

### 模块结构
- **循环导入风险**: `sumo_simulator.py:56-57` 注释提到避免循环导入问题
  - 建议: 重构模块依赖关系

## 数据管理

### 模型文件
- **大型模型文件**: `model/` 目录包含检查点和预训练模型
  - 建议: 使用 Git LFS 管理大型二进制文件
  - 建议: 添加 `.gitattributes` 配置

### 临时文件
- **缓存文件**: `__pycache__` 目录应添加到 `.gitignore`

## 配置问题

### YAML 配置
- **配置验证**: `config/training_config.yaml` 缺少架构验证
  - 建议: 使用 pydantic 或 marshmallow 验证配置

## 依赖关系

### 外部依赖
- **SUMO 版本兼容性**: 代码依赖 SUMO TraCI，但未明确最低版本要求
  - 建议: 在 README 中声明 SUMO 版本要求

### Python 版本
- **Python 3.12**: 代码使用 Python 3.12 特性（从 `__pycache__` 文件名可见）
  - 建议: 在 `pyproject.toml` 中明确声明 `python = "^3.12"`

## 优先级建议

**高优先级**:
1. 添加 `.gitignore` 排除 `__pycache__` 和编译缓存
2. 使用 Git LFS 管理模型文件
3. 统一 SUMO_HOME 配置逻辑

**中优先级**:
4. 改进错误处理的粒度
5. 建立测试目录结构
6. 添加配置验证机制

**低优先级**:
7. 统一文档语言标准
8. 重构避免循环导入
