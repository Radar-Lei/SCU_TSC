# Codebase Structure

**Analysis Date:** 2026-02-03

## Directory Layout

```
SCU_TSC/
├── config/                 # Centralized configuration files
├── data/                   # Generated datasets and training data
│   ├── grpo_datasets/      # Datasets for RL training
│   └── sft_datasets/       # Datasets for supervised training
├── docker/                 # Containerization scripts
├── grpo/                   # Core logic for GRPO and TSC
│   ├── training.py         # Main GRPO training script
│   ├── reward.py           # Reward logic and helpers
│   ├── sumo_interface.py   # SUMO simulation wrapper
│   └── ...                 # Dataset generators and builders
├── model/                  # Model checkpoints and exports
├── sumo_simulation/        # SUMO environment definitions
│   ├── environments/       # Specific traffic scenarios (grid, arterial)
│   └── sumo_simulator.py   # General simulation manager
├── unsloth_compiled_cache/ # Optimized kernels for LLM training
└── [scripts]               # Top-level utility scripts
```

## Directory Purposes

**grpo/:**
- Purpose: Primary source code for the project.
- Contains: Training scripts, reward calculation, and dataset generation logic.
- Key files: `grpo/training.py`, `grpo/sumo_reward.py`, `grpo/config.py`.

**sumo_simulation/:**
- Purpose: Infrastructure for running traffic simulations.
- Contains: Scenario files (.sumocfg, .net.xml) and the simulator wrapper.
- Key files: `sumo_simulation/sumo_simulator.py`.

**config/:**
- Purpose: Configuration management.
- Contains: YAML files and Python loaders.
- Key files: `config/training_config.yaml`.

**data/:**
- Purpose: Storage for intermediate and final datasets.
- Contains: JSON files and SUMO state files.

## Key File Locations

**Entry Points:**
- `grpo/training.py`: Main entry for GRPO RL training.
- `grpo/sft_training.py`: Main entry for SFT supervised training.
- `grpo/generate_grpo_dataset.py`: Script to generate RL training data.

**Configuration:**
- `config/training_config.yaml`: The single source of truth for training and simulation parameters.
- `grpo/config.py`: Python dataclasses representing the configuration.

**Core Logic:**
- `grpo/sumo_reward.py`: Implementation of the simulation-in-the-loop reward calculation.
- `sumo_simulation/sumo_simulator.py`: Encapsulation of SUMO TraCI logic.

**Testing:**
- `test_stratified_split.py`: Utility for testing dataset splitting.
- (Standard unit tests not detected; logic verified via script execution)

## Naming Conventions

**Files:**
- Snake Case: `generate_grpo_dataset.py`, `sumo_interface.py`.

**Directories:**
- Snake Case: `sumo_simulation`, `grpo_datasets`.

**Classes:**
- Pascal Case: `SUMOInterface`, `GRPOTrainingConfig`, `SUMOSimulator`.

## Where to Add New Code

**New Training Logic:**
- Add to `grpo/` and update `grpo/training.py` or create a new trainer script.

**New Reward Metric:**
- Implementation: `grpo/reward.py` or `grpo/sumo_reward.py`.
- Config: Add parameter to `config/training_config.yaml` and `grpo/config.py`.

**New Traffic Scenario:**
- Primary files: `sumo_simulation/environments/[scenario_name]/`.
- Ensure a `.sumocfg` exists and is referenced in the training config.

**New Prompt Template:**
- Implementation: `grpo/prompt_builder.py`.
- Update the `SYSTEM_PROMPT` in `grpo/config.py` if global.

## Special Directories

**unsloth_compiled_cache/:**
- Purpose: Contains Unsloth-optimized Python files for faster training.
- Generated: Yes
- Committed: No (usually ignored in .gitignore, though present here)

**model/:**
- Purpose: Storage for large model weights.
- Generated: Yes
- Committed: No (contains .gitkeep or specific exports)

---

*Structure analysis: 2026-02-03*
