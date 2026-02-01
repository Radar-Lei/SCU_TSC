# Technology Stack

**Analysis Date:** 2025-02-02

## Languages

**Primary:**
- Python 3.13+ - Core language for all modules (GRPO, SFT training, SUMO interface)

**Secondary:**
- Bash - Docker automation scripts and test runners
- Jupyter Notebook - Experiment tracking (`Qwen3_(4B)_GRPO.ipynb`)

## Runtime

**Environment:**
- Python 3.13+ (required by `sumo_simulation/pyproject.toml`)

**Package Manager:**
- pip (via system package installation in Docker)
- Lockfile: Present (Docker layer caching)

## Frameworks

**Core:**
- Unsloth - Model fine-tuning framework for LoRA/GRPO training
  - FastLanguageModel for model loading and inference
  - LoRA adapter management
  - GGUF conversion support
- TRL (Transformer Reinforcement Learning) - Training framework
  - SFTTrainer, SFTConfig for supervised fine-tuning
  - GRPOTrainer, GRPOConfig for reinforcement learning
- Transformers (HuggingFace) - Model loading and tokenizer
- PEFT - LoRA model merging (`from peft import PeftModel`)

**Testing:**
- No dedicated test framework detected (test scripts are Bash-based)

**Build/Dev:**
- Docker + NVIDIA Container Toolkit - Containerized GPU training environment
- vLLM - Fast inference engine for generation

## Key Dependencies

**Critical:**
- torch - PyTorch for model training and inference
- traci>=1.23.0 - SUMO Traffic Control Interface for traffic simulation
- unsloth - Primary training framework
- trl - Training utilities (SFT, GRPO)
- datasets - HuggingFace datasets library
- transformers - Model/tokenizer handling
- peft - LoRA adapter management

**Infrastructure:**
- modelscope - Model distribution platform (Chinese alternative to HuggingFace)
  - Used via `UNSLOTH_USE_MODELSCOPE=1` environment variable
- vllm - Fast LLM inference
- openai>=1.77.0 - OpenAI API client
- anthropic==0.49.0 - Anthropic API client
- dashscope>=1.24.6 - Alibaba cloud LLM API
- fastapi==0.115.8 - API server framework
- mcp==1.6.0 - Model Context Protocol

**Utilities:**
- numpy==2.2.1 - Numerical computing
- loguru==0.7.3 - Logging
- streamlit, plotly>=6.3.0 - Visualization
- watchdog>=6.0.0 - File watching

## Configuration

**Environment:**
- Environment variables for configuration (no .env files detected)
- Key configs required:
  - `SUMO_HOME` - SUMO installation path
  - `HF_HOME` - HuggingFace cache directory
  - `MODELSCOPE_CACHE` - ModelScope cache directory
  - `UNSLOTH_USE_MODELSCOPE=1` - Enable ModelScope for model downloads

**Build:**
- Dockerfile at `/home/samuel/SCU_TSC/docker/Dockerfile`
- Base image: `unsloth/unsloth:dgxspark-latest`
- SUMO installation via PPA

## Platform Requirements

**Development:**
- Linux (Ubuntu-based Docker container)
- NVIDIA GPU with CUDA support
- 16GB+ GPU VRAM recommended
- SUMO traffic simulator

**Production:**
- Docker with NVIDIA Container Toolkit
- CUDA 12.4+ support
- GPU inference/training capability

---

*Stack analysis: 2025-02-02*
