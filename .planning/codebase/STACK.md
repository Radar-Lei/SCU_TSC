# Technology Stack

**Analysis Date:** 2025-02-03

## Languages

**Primary:**
- Python 3.13+ - All training, simulation, and data processing code

**Secondary:**
- Shell (Bash) - Docker automation and entrypoint scripts
- YAML - Configuration files

## Runtime

**Environment:**
- Python 3.13 (required by `sumo_simulation/pyproject.toml`)
- CUDA (for GPU training with Unsloth)

**Package Manager:**
- pip (via pyproject.toml)
- Lockfile: Not detected (uses fixed version pins in pyproject.toml)

## Frameworks

**Core:**
- unsloth (latest) - Efficient LLM fine-tuning with LoRA/QLoRA
- trl (Hugging Face TRL) - RLHF training (SFTTrainer, GRPOTrainer)
- transformers (Hugging Face) - Base model loading and tokenization
- torch - PyTorch for deep learning operations

**Data Processing:**
- datasets (Hugging Face) - Dataset management and loading
- scikit-learn - Data stratification and train/test splitting
- numpy - Numerical operations

**Simulation:**
- SUMO 1.x+ - Traffic simulation (via TraCI Python interface)
- traci >=1.23.0 - SUMO Traffic Control Interface

**Build/Dev:**
- Docker - Containerization for reproducible environments

## Key Dependencies

**Critical:**
- unsloth - Fast LLM fine-tuning (must import before transformers)
- trl - GRPO and SFT training implementations
- torch - Deep learning framework with CUDA support
- traci - SUMO Python control interface

**Infrastructure:**
- pyyaml - YAML configuration parsing
- scikit-learn - Stratified dataset splitting

**From `sumo_simulation/pyproject.toml`:**
- anthropic==0.49.0 - Anthropic API client
- fastapi==0.115.8 - API server framework
- loguru==0.7.3 - Structured logging
- mcp==1.6.0 - MCP protocol support
- numpy==2.2.1 - Numerical computing
- openai>=1.77.0 - OpenAI API client
- streamlit - Streamlit UI framework
- plotly>=6.3.0 - Interactive plotting
- dashscope>=1.24.6 - Alibaba Cloud LLM API
- watchdog>=6.0.0 - File system monitoring

## Configuration

**Environment:**
- Central YAML config: `/home/samuel/SCU_TSC/config/training_config.yaml`
- SUMO environment: `SUMO_HOME` (auto-detected from multiple paths)
- CUDA environment: CUDA_PATH in Docker container

**Build:**
- Dockerfile: `/home/samuel/SCU_TSC/docker/Dockerfile`
- Base image: `unsloth/unsloth:dgxspark-latest`
- SUMO installation: PPA `ppa:sumo/stable`

## Platform Requirements

**Development:**
- Linux (Ubuntu/Debian preferred for SUMO compatibility)
- Python 3.13+
- CUDA-capable GPU (for training)
- SUMO 1.x+ installation

**Production:**
- Docker container with GPU support
- SUMO simulation environment
- Model storage for SFT and GRPO model checkpoints

---

*Stack analysis: 2025-02-03*
