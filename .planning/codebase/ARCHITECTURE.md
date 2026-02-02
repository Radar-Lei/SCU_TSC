# Architecture

**Analysis Date:** 2026-02-03

## Pattern Overview

**Overall:** Reinforcement Learning with Simulation-in-the-loop (GRPO for TSC)

**Key Characteristics:**
- **Simulation-Driven Rewards:** Rewards are not static; they are calculated by running actual SUMO simulations for each model completion.
- **Hierarchical Training:** Supports Supervised Fine-Tuning (SFT) followed by Group Relative Policy Optimization (GRPO).
- **Parallelized Evaluation:** Uses multi-processing to run multiple SUMO instances in parallel for high-throughput reward calculation.

## Layers

**Simulation Layer:**
- Purpose: Interfaces with the SUMO traffic simulator.
- Location: `sumo_simulation/sumo_simulator.py`, `grpo/sumo_interface.py`
- Contains: TraCI wrappers, state saving/loading logic, vehicle/queue metrics collection.
- Depends on: SUMO (external binaries), `traci`
- Used by: Reward Layer, Data Generation Layer

**Data Generation Layer:**
- Purpose: Generates training datasets for SFT and GRPO.
- Location: `grpo/dataset_generator.py`, `grpo/generate_grpo_dataset.py`, `grpo/generate_sft_dataset.py`
- Contains: Scenario execution logic, prompt building, state sampling.
- Depends on: Simulation Layer, `grpo/prompt_builder.py`
- Used by: Training Layer

**Reward Layer:**
- Purpose: Evaluates model decisions by simulating the outcome and calculating traffic metrics.
- Location: `grpo/reward.py`, `grpo/sumo_reward.py`
- Contains: Reward functions (e.g., queue length reduction), parallel reward calculators.
- Depends on: Simulation Layer
- Used by: Training Layer (via GRPOTrainer)

**Training Layer:**
- Purpose: Fine-tunes Large Language Models (LLMs) for traffic decision making.
- Location: `grpo/training.py`, `grpo/sft_training.py`
- Contains: Unsloth/TRL trainer initialization, dataset loading, LoRA configuration.
- Depends on: Reward Layer, `grpo/config.py`
- Used by: End users/scripts

## Data Flow

**GRPO Training Flow:**

1. **Prompt Loading:** Load prompts and initial SUMO states from `data/grpo_datasets/`.
2. **Model Generation:** The LLM generates multiple "extend" decisions (yes/no) for each prompt.
3. **Parallel Simulation:** `ParallelSUMORewardCalculator` launches SUMO instances to simulate each decision starting from the saved state.
4. **Reward Computation:** `grpo/sumo_reward.py` calculates the reward based on the change in queue length before and after the decision window.
5. **Policy Update:** GRPOTrainer updates the model weights based on relative rewards within the group.

**State Management:**
- SUMO simulation states are saved as files (`.xml`) and referenced in datasets to allow jumping to specific points in time during training.

## Key Abstractions

**SUMOInterface:**
- Purpose: Low-level wrapper for SUMO TraCI operations.
- Examples: `grpo/sumo_interface.py`
- Pattern: Adapter

**Reward Calculator:**
- Purpose: Abstracting the complexity of running simulations to get a single numeric reward.
- Examples: `grpo/sumo_reward.py`
- Pattern: Strategy / Proxy

## Entry Points

**GRPO Training:**
- Location: `grpo/training.py`
- Triggers: CLI command `python grpo/training.py`
- Responsibilities: Main entry point for RL fine-tuning.

**SFT Training:**
- Location: `grpo/sft_training.py`
- Triggers: CLI command `python grpo/sft_training.py`
- Responsibilities: Main entry point for supervised fine-tuning.

**Data Generation:**
- Location: `grpo/generate_grpo_dataset.py`
- Triggers: CLI command `python grpo/generate_grpo_dataset.py`
- Responsibilities: Generates the initial prompts and states for RL.

## Error Handling

**Strategy:** Exception catching with fallback/retry for simulation failures.

**Patterns:**
- TraCI port conflict resolution via `find_available_port`.
- Try-except blocks around SUMO simulation steps to handle crashed instances.

## Cross-Cutting Concerns

**Logging:** Uses standard `logging` and print statements for training progress and simulation status.
**Validation:** `grpo/validate_data.py` ensures datasets are correctly formatted before training.
**Configuration:** Centralized YAML configuration handled by `config/read_config.py` and `grpo/config.py`.

---

*Architecture analysis: 2026-02-03*
