# 将 LoRA Checkpoint 转换为 GGUF 格式

本文档说明如何将 Unsloth 训练的 LoRA checkpoint 转换为 GGUF 格式，以便在 llama.cpp、ollama 等推理框架中使用。

## 前置条件

- 已安装的 Python 环境 (推荐使用项目的 `.venv`)
- 一个有效的 LoRA checkpoint，例如 `checkpoints/grpo_tsc_two_scenarios/checkpoint-5000`

## 方法一：使用项目脚本（推荐）

### 步骤 1：合并 LoRA 权重

运行项目提供的 `convert_to_gguf.py` 脚本，该脚本会自动合并 LoRA 适配器到基础模型：

```bash
# 激活虚拟环境
source .venv/bin/activate

# 运行转换脚本
python convert_to_gguf.py --checkpoint checkpoints/grpo_tsc_two_scenarios/checkpoint-5000
```

这会在 checkpoint 目录下生成一个合并后的 HuggingFace 模型：
```
checkpoints/grpo_tsc_two_scenarios/checkpoint-5000_gguf_merged/
```

### 步骤 2：转换为 GGUF

如果脚本的自动 GGUF 转换失败（网络问题等），手动执行以下步骤：

```bash
# 克隆 llama.cpp（如果尚未克隆）
git clone --depth 1 https://github.com/ggerganov/llama.cpp /tmp/llama.cpp

# 使用 llama.cpp 的转换脚本
PYTHONPATH=/tmp/llama.cpp/gguf-py .venv/bin/python /tmp/llama.cpp/convert_hf_to_gguf.py \
    checkpoints/grpo_tsc_two_scenarios/checkpoint-5000_gguf_merged \
    --outtype f16 \
    --outfile checkpoints/grpo_tsc_two_scenarios/checkpoint-5000.gguf
```

## 方法二：手动操作

### 步骤 1：加载并合并模型

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import json

# 读取 adapter 配置
checkpoint_path = "checkpoints/grpo_tsc_two_scenarios/checkpoint-5000"
with open(f"{checkpoint_path}/adapter_config.json", "r") as f:
    config = json.load(f)
base_model_name = config["base_model_name_or_path"]

# 加载基础模型
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_name,
    torch_dtype=torch.float16,
    device_map="auto",
)
tokenizer = AutoTokenizer.from_pretrained(base_model_name)

# 加载并合并 LoRA
model = PeftModel.from_pretrained(base_model, checkpoint_path)
model = model.merge_and_unload()

# 保存合并后的模型
output_dir = f"{checkpoint_path}_merged"
model.save_pretrained(output_dir, safe_serialization=True)
tokenizer.save_pretrained(output_dir)
```

### 步骤 2：转换为 GGUF

```bash
python /path/to/llama.cpp/convert_hf_to_gguf.py \
    checkpoints/grpo_tsc_two_scenarios/checkpoint-5000_merged \
    --outtype f16 \
    --outfile checkpoint-5000.gguf
```

## 量化选项

`--outtype` 参数支持以下格式：

| 格式 | 大小 | 说明 |
|------|------|------|
| `f32` | 最大 | 32位浮点，完全精度 |
| `f16` | 大 | 16位浮点，推荐 |
| `bf16` | 大 | BFloat16，需要硬件支持 |
| `q8_0` | 中 | 8位量化，几乎无损 |

如需进一步量化（如 q4_k_m），需先编译 llama.cpp：

```bash
cd /tmp/llama.cpp
make -j

# 量化为 q4_k_m
./llama-quantize checkpoint-5000.gguf checkpoint-5000-q4_k_m.gguf q4_k_m
```

常用量化格式：
- `q4_k_m` - 4位量化，体积最小，推理速度快
- `q5_k_m` - 5位量化，平衡体积和精度
- `q8_0` - 8位量化，精度最高

## 使用生成的 GGUF

### 使用 ollama

```bash
# 创建 Modelfile
cat > Modelfile << EOF
FROM ./checkpoint-5000.gguf
EOF

# 导入模型
ollama create tsc-model -f Modelfile

# 运行
ollama run tsc-model
```

### 使用 llama.cpp

```bash
cd /tmp/llama.cpp
make -j
./llama-cli -m /path/to/checkpoint-5000.gguf -p "Your prompt here"
```

## 故障排除

### 问题：`ModuleNotFoundError: No module named 'unsloth'`

确保使用正确的 Python 环境：
```bash
.venv/bin/python convert_to_gguf.py ...
```

### 问题：网络连接失败

使用国内镜像源：
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple package_name
```

### 问题：`UnboundLocalError` in unsloth

这是 unsloth 库的已知 bug。使用本项目的 `convert_to_gguf.py` 脚本可以绑过这个问题（先用 PEFT 合并，再转换）。


source .venv/bin/activate
python convert_to_gguf.py --checkpoint checkpoints/grpo_tsc_two_scenarios/checkpoint-1000


PYTHONPATH=/tmp/llama.cpp/gguf-py .venv/bin/python /tmp/llama.cpp/convert_hf_to_gguf.py checkpoints/grpo_tsc_two_scenarios/checkpoint-1000_gguf_merged --outtype f16 --outfile checkpoints/grpo_tsc_two_scenarios/checkpoint-1000.gguf

