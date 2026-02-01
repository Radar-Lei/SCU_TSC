# External Integrations

**Analysis Date:** 2025-02-02

## APIs & External Services

**Model Distribution:**
- HuggingFace - Primary model hub
  - SDK/Client: transformers, huggingface_hub
  - Models: unsloth/Qwen2.5-0.5B-Instruct, unsloth/Qwen3-4B-Base
  - Auth: Configured via HF_HOME environment

**ModelScope (Alibaba):**
- Chinese model distribution platform
  - SDK/Client: modelscope Python package
  - Environment: `UNSLOTH_USE_MODELSCOPE=1`, `MODELSCOPE_CACHE=/home/samuel/SCU_TSC/model`
  - Purpose: Alternative model download source for China

**LLM API Providers:**
- OpenAI API
  - SDK: openai>=1.77.0
  - Usage: Not directly used in main codebase (dependency only)

- Anthropic Claude
  - SDK: anthropic==0.49.0
  - Usage: Not directly used in main codebase (dependency only)

- Dashscope (Alibaba Cloud)
  - SDK: dashscope>=1.24.6
  - Usage: Not directly used in main codebase (dependency only)

## Data Storage

**Databases:**
- None (JSON-based data storage)

**File Storage:**
- Local filesystem only
  - GRPO datasets: `/home/samuel/SCU_TSC/data/grpo_datasets/`
  - SFT datasets: `/home/samuel/SCU_TSC/data/sft_datasets/`
  - Models: `/home/samuel/SCU_TSC/model/`

**Data Format:**
- JSON for datasets (`grpo_dataset.json`, `sft_dataset.json`)
- JSONL for compatibility with HuggingFace datasets
- XML for SUMO simulation states

**Caching:**
- HuggingFace cache: `HF_HOME=/home/samuel/SCU_TSC/model`
- ModelScope cache: `MODELSCOPE_CACHE=/home/samuel/SCU_TSC/model`
- Unsloth compiled cache: `.unsloth_compiled_cache/`

## Authentication & Identity

**Auth Provider:**
- None (no user authentication)
- API-based model access via environment configuration

**Implementation:**
- Model downloads use public HuggingFace/ModelScope hubs
- No API keys required for base model access

## Monitoring & Observability

**Error Tracking:**
- None detected (report_to="none" in training configs)

**Logs:**
- Loguru for Python logging
- Training logs: `.docker_sft_test.log`
- Console output for Docker scripts

**Monitoring:**
- No external monitoring services configured

## CI/CD & Deployment

**Hosting:**
- Local/Docker-based deployment
- No cloud hosting configured

**CI Pipeline:**
- None (manual execution via Docker scripts)

**Deployment Artifacts:**
- Docker images built from `/home/samuel/SCU_TSC/docker/Dockerfile`
- Image naming: `qwen3-tsc-grpo:latest`

## Environment Configuration

**Required env vars:**

```bash
# SUMO Traffic Simulator
SUMO_HOME=/usr/share/sumo

# Model Caching
HF_HOME=/home/samuel/SCU_TSC/model
MODELSCOPE_CACHE=/home/samuel/SCU_TSC/model
UNSLOTH_USE_MODELSCOPE=1

# Training (optional)
SFT_SAMPLE_SIZE=500
SFT_MAX_STEPS=50
FULL_TRAINING=0
```

**Secrets location:**
- No secrets management system detected
- No API keys in repository
- Environment-specific configuration in Docker scripts

## Webhooks & Callbacks

**Incoming:**
- None (no API server endpoints exposed)

**Outgoing:**
- None (no external webhooks configured)

## Simulation Integration

**SUMO Traffic Simulator:**
- Purpose: Traffic signal control simulation
- Integration: TraCI (Traffic Control Interface) Python library
- Connection: TCP on random ports (10000-60000)
- Location: `/home/samuel/SCU_TSC/sumo_simulation/environments/`
- Auth: None (local process communication)

**Key Files:**
- SUMO interface: `/home/samuel/SCU_TSC/grpo/sumo_interface.py`
- Scenarios: Multiple SUMO .sumocfg files in environments directory

---

*Integration audit: 2025-02-02*
