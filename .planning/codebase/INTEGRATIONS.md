# External Integrations

**Analysis Date:** 2026-02-03

## APIs & External Services

**LLM Model Providers:**
- HuggingFace - Primary source for base models (e.g., `unsloth/Qwen2.5-0.5B-Instruct`).
- ModelScope - Optional support via `UNSLOTH_USE_MODELSCOPE` env var in `grpo/training.py`.

## Data Storage

**Databases:**
- None detected. The project uses local file storage for datasets and simulation states.

**File Storage:**
- Local Filesystem:
  - JSON: Datasets stored in `data/grpo_datasets/` and `data/sft_datasets/`.
  - XML: SUMO network, route, and state files.
  - YAML: Configuration files in `config/`.

**Caching:**
- `unsloth_compiled_cache/`: Local cache for Unsloth-optimized kernels and trainers.

## Authentication & Identity

**Auth Provider:**
- None - Local execution and open-access models.
- WandB API Key - Required if `use_wandb` is enabled for experiment tracking.

## Monitoring & Observability

**Error Tracking:**
- Local logging via standard output and potentially WandB.

**Logs:**
- Console logging in training and simulation scripts.
- WandB (Optional) - Configured in `config/training_config.yaml` under `logging`.

## CI/CD & Deployment

**Hosting:**
- Local or Cloud GPU servers (e.g., RunPod, Lambda Labs, or local workstation).

**CI Pipeline:**
- Not detected in the codebase.

## Environment Configuration

**Required env vars:**
- `SUMO_HOME`: Path to the SUMO installation directory (critical for `traci`).
- `PYTHONPATH`: Often used to include the project root for module imports.

**Secrets location:**
- Not explicitly defined, likely handled via standard environment variables or shell configuration for WandB.

## Webhooks & Callbacks

**Incoming:**
- None.

**Outgoing:**
- WandB API calls for metrics reporting (if enabled).

---

*Integration audit: 2026-02-03*
