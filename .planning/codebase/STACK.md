# Technology Stack

**Analysis Date:** 2026-02-03

## Languages

**Primary:**
- Python 3.13+ - Core logic, training scripts, simulation interface, and data processing.

**Secondary:**
- XML - SUMO configuration files (`.sumocfg`, `.net.xml`, `.rou.xml`) and simulation state files.
- YAML - Configuration files for training and simulation.

## Runtime

**Environment:**
- Linux (Ubuntu/Debian recommended for SUMO compatibility)
- NVIDIA GPU with CUDA support (required for LLM training and inference via Unsloth)

**Package Manager:**
- pip - Used for managing Python dependencies.
- venv - Virtual environment detected in `sumo_simulation/.venv/`.

## Frameworks

**Core:**
- Unsloth - Optimized LLM fine-tuning (SFT and GRPO). Used in `grpo/training.py`.
- HuggingFace Transformers & TRL (Transformer Reinforcement Learning) - Foundation for GRPO training.
- PyTorch - Underlying deep learning framework.

**Simulation:**
- SUMO (Simulation of Urban MObility) - Traffic simulation engine.
- TraCI (Traffic Control Interface) - Python API for interacting with SUMO in real-time.

**Data Processing:**
- Pandas/NumPy - Inferred for data manipulation in dataset generation.
- Datasets (HuggingFace) - Used for managing training data.

## Key Dependencies

**Critical:**
- `unsloth` - Provides `FastLanguageModel` for high-performance training.
- `trl` - Provides `GRPOTrainer` for reinforcement learning.
- `traci` - Essential for communicating with the SUMO simulation engine.
- `sumolib` - Helper library for SUMO network and file parsing.

**Infrastructure:**
- `PyYAML` - Used in `config/read_config.py` for parsing configuration.
- `wandb` (Weights & Biases) - Optional integration for experiment tracking.

## Configuration

**Environment:**
- `SUMO_HOME`: Environment variable required to locate SUMO tools and binaries.
- Configured via `config/training_config.yaml`.

**Build:**
- No formal build system (script-based execution).
- `convert_to_gguf.py` - For exporting models to GGUF format.

## Platform Requirements

**Development:**
- SUMO installed and reachable via `SUMO_HOME`.
- Python 3.10+ (scripts show usage of 3.13 features/paths).
- CUDA-compatible GPU (NVIDIA).

**Production:**
- Deployment typically involves a Linux environment with GPU acceleration and SUMO installed.

---

*Stack analysis: 2026-02-03*
