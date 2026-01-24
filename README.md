# 1. 生成合成数据 (让模型学会格式)
SCRIPT_NAME=generate_synthetic_sft_dataset.py ./docker/publish.sh

# 2. 运行 SFT 训练 (快速微调)
SCRIPT_NAME=train_sft.py ./docker/publish.sh

# 3. 重新开始 GRPO 训练 (模型现在会输出正确格式了，GRPO 将开始优化策略)
./docker/publish.sh