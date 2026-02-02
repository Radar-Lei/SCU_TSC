# External Integrations

**Analysis Date:** 2025-02-03

## APIs & External Services

**LLM Providers:**
- Anthropic Claude - `anthropic==0.49.0` in `/home/samuel/SCU_TSC/sumo_simulation/pyproject.toml`
  - Purpose: LLM API integration (likely for evaluation/comparison)
  - SDK: `anthropic` package
  - Auth: Environment variable (standard ANTHROPIC_API_KEY)

- OpenAI - `openai>=1.77.0` in `/home/samuel/SCU_TSC/sumo_simulation/pyproject.toml`
  - Purpose: OpenAI API integration
  - SDK: `openai` package
  - Auth: Environment variable (standard OPENAI_API_KEY)

- Alibaba Dashscope - `dashscope>=1.24.6` in `/home/samuel/SCU_TSC/sumo_simulation/pyproject.toml`
  - Purpose: Alibaba Cloud Qwen API integration
  - SDK: `dashscope` package
  - Auth: Environment variable (DASHSCOPE_API_KEY)

- ModelScope - Used in Docker container
  - Purpose: Chinese model hub (alternative to Hugging Face)
  - Installation: `pip install modelscope` in Dockerfile

## Data Storage

**Databases:**
- None detected (project uses file-based storage)

**File Storage:**
- Local filesystem - All datasets, models, and simulation states stored locally
  - Data directory: `/home/samuel/SCU_TSC/data/`
    - GRPO datasets: `data/grpo_datasets/`
    - SFT datasets: `data/sft_datasets/`
  - Model directory: `/home/samuel/SCU_TSC/model/`
    - SFT models: `model/sft_model/`
    - GRPO models: `model/grpo_model/`
  - Simulation environments: `/home/samuel/SCU_TSC/sumo_simulation/environments/`

**Caching:**
- Unsloth compiled cache: `/home/samuel/SCU_TSC/unsloth_compiled_cache/`
  - Contains cached Unsloth trainer implementations
  - Lock files: `.locks/` subdirectory

## Authentication & Identity

**Auth Provider:**
- Custom - No centralized auth provider detected
  - API keys stored as environment variables
  - No auth configuration files detected

## Monitoring & Observability

**Error Tracking:**
- None detected (no Sentry, Rollbar, etc.)

**Logs:**
- Loguru - `loguru==0.7.3` in `/home/samuel/SCU_TSC/sumo_simulation/pyproject.toml`
  - Structured logging throughout the codebase
  - Usage: Console/file logging for training and simulation

- Docker run log: `/home/samuel/SCU_TSC/.docker_run.log`
  - Captures Docker container output

- WandB (Weights & Biases) - Optional integration
  - Configured in `config/training_config.yaml` under `logging.use_wandb`
  - Project: "scu-tsc-grpo"
  - Controlled by `use_wandb: false` (disabled by default)

## CI/CD & Deployment

**Hosting:**
- Local/Docker - No cloud hosting detected
  - Docker containerization via `/home/samuel/SCU_TSC/docker/Dockerfile`
  - Base image: `unsloth/unsloth:dgxspark-latest`

**CI Pipeline:**
- Shell scripts - Custom automation
  - `/home/samuel/SCU_TSC/docker/publish.sh` - Main workflow orchestrator
  - `/home/samuel/SCU_TSC/docker/entrypoint.sh` - Container entry point
  - `/home/samuel/SCU_TSC/docker/cleanup.sh` - Resource cleanup

## Environment Configuration

**Required env vars:**
- `SUMO_HOME` - SUMO installation path (auto-detected if not set)
- `ANTHROPIC_API_KEY` - For Anthropic Claude API (optional)
- `OPENAI_API_KEY` - For OpenAI API (optional)
- `DASHSCOPE_API_KEY` - For Alibaba Dashscope API (optional)
- `WANDB_API_KEY` - For Weights & Biases logging (if use_wandb enabled)

**Secrets location:**
- Environment variables only (no secrets manager integration)
- No .env files detected in project root

## Webhooks & Callbacks

**Incoming:**
- None detected (no FastAPI routes defined in analyzed code)

**Outgoing:**
- None detected (no external webhook calls in analyzed code)

## Simulation Integration

**SUMO Traffic Simulator:**
- TraCI (Traffic Control Interface) - `traci>=1.23.0`
  - Python control interface for SUMO
  - Used for real-time traffic simulation control
  - State save/load for GRPO counterfactual evaluation
  - Multi-worker parallel simulation support
  - Port range: 10000-60000 for parallel instances

**SUMO Configuration:**
- Multiple scenario environments: `/home/samuel/SCU_TSC/sumo_simulation/environments/`
  - arterial4x4_* scenarios (100, 90-99)
  - chengdu scenario
- Each scenario contains:
  - `.sumocfg` configuration files
  - `.net.xml` network definition files
  - Traffic flow definitions

## Model Hub Integration

**Hugging Face:**
- Direct model downloads via transformers/unsloth
  - Base model: `unsloth/Qwen2.5-0.5B-Instruct`
  - Used for SFT training initialization

**GGUF Conversion:**
- `/home/samuel/SCU_TSC/convert_to_gguf.py`
  - Converts trained models to GGUF format
  - Uses Unsloth's GGUF conversion utilities

---

*Integration audit: 2025-02-03*
