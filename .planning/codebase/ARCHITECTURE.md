# Architecture

**Analysis Date:** 2025-02-03

## Pattern Overview

**Overall:** Modular Reinforcement Learning Pipeline with Traffic Simulation Backend

**Key Characteristics:**
- Two-stage training: SFT (Supervised Fine-Tuning) for format learning, followed by GRPO (Group Relative Policy Optimization) for decision optimization
- SUMO traffic simulation as environment simulator providing reward signals
- Reward chain combining format validation and TSC (Traffic Signal Control) performance metrics
- Parallel execution for data generation and reward calculation
- Centralized YAML configuration management

## Layers

**Data Generation Layer:**
- Purpose: Generate training data by running SUMO simulations and collecting traffic states at decision points
- Location: `/home/samuel/SCU_TSC/grpo/dataset_generator.py`, `/home/samuel/SCU_TSC/grpo/generate_grpo_dataset.py`
- Contains: `GRPODatasetGenerator`, `GRPODataEntry`, parallel execution via `parallel_runner.py`
- Depends on: SUMO interface (`sumo_interface.py`), prompt builder (`prompt_builder.py`), config (`config.py`)
- Used by: Training pipeline for SFT and GRPO datasets

**Configuration Layer:**
- Purpose: Centralized configuration management for training, simulation, and reward parameters
- Location: `/home/samuel/SCU_TSC/grpo/config.py`, `/home/samuel/SCU_TSC/config/training_config.yaml`, `/home/samuel/SCU_TSC/config/read_config.py`
- Contains: `GRPOConfig`, `GRPOTrainingConfig`, `SFTTrainingConfig`, `TrainingConfig`, `RewardChainConfig`, `SUMOConfig`
- Depends on: PyYAML for config file parsing
- Used by: All modules (training, data generation, reward calculation)

**SUMO Interface Layer:**
- Purpose: Abstraction over SUMO traffic simulation TraCI API
- Location: `/home/samuel/SCU_TSC/grpo/sumo_interface.py`
- Contains: `SUMOInterface`, `PhaseInfo`, `find_available_port()`
- Depends on: SUMO TraCI library
- Used by: Data generator, reward calculator, legacy simulator (`sumo_simulation/sumo_simulator.py`)

**Reward Calculation Layer:**
- Purpose: Compute reward signals combining format correctness and traffic performance
- Location: `/home/samuel/SCU_TSC/grpo/reward.py`, `/home/samuel/SCU_TSC/grpo/sumo_reward.py`, `/home/samuel/SCU_TSC/grpo/max_pressure.py`
- Contains: `format_reward_fn()`, `batch_compute_reward()`, `ParallelSUMORewardCalculator`, `max_pressure_decision()`
- Depends on: SUMO interface, regex/JSON parsing for format validation
- Used by: GRPO trainer for policy optimization

**Training Layer:**
- Purpose: Model training using Unsloth and TRL libraries
- Location: `/home/samuel/SCU_TSC/grpo/sft_training.py`, `/home/samuel/SCU_TSC/grpo/training.py`
- Contains: `train_sft()`, `train_grpo()`, `load_sft_dataset()`, `load_grpo_dataset()`, `create_reward_function()`
- Depends on: Unsloth (FastLanguageModel), TRL (SFTTrainer, GRPOTrainer), reward functions
- Used by: Command-line execution and model development

**Legacy Simulation Layer:**
- Purpose: Original SUMO simulator with extended features (max-pressure, historical data collection)
- Location: `/home/samuel/SCU_TSC/sumo_simulation/sumo_simulator.py`
- Contains: `SUMOSimulator` class with comprehensive traffic data collection and analysis
- Depends on: SUMO TraCI
- Used by: Direct simulation control, historical data analysis

## Data Flow

**Data Generation Flow:**

1. SUMO scenario selection from `/home/samuel/SCU_TSC/sumo_simulation/environments/`
2. SUMOInterface initializes simulation with warmup period
3. Main simulation loop:
   - Step simulation forward
   - Detect decision points (at min_green_time and every extend_seconds thereafter)
   - Collect phase queue metrics via `get_all_phases_queue()`
   - Save simulation state to XML file (for later reward calculation)
   - Build JSON prompt via `build_extend_decision_prompt()`
   - Create `GRPODataEntry` with all context
4. Save dataset to `/home/samuel/SCU_TSC/data/grpo_datasets/{scenario}/grpo_dataset.json`

**SFT Training Flow:**

1. Load SFT dataset from `/home/samuel/SCU_TSC/data/sft_datasets/sft_dataset.json`
2. Format data with chat template (system + user messages)
3. Load base model (unsloth/Qwen2.5-0.5B-Instruct)
4. Apply LoRA adapters
5. Train with SFTTrainer to learn output format `{"extend": "yes/no"}`
6. Validate format accuracy on test samples
7. Save model to `/home/samuel/SCU_TSC/model/sft_model/`

**GRPO Training Flow:**

1. Load GRPO dataset(s) from `/home/samuel/SCU_TSC/data/grpo_datasets/`
2. Load SFT model as starting point
3. Create reward function chain:
   - Format reward: validates `{"extend": "yes/no"}` structure
   - TSC reward: runs SUMO simulation to evaluate queue improvement
   - Optional: Max Pressure baseline comparison
4. Configure GRPOTrainer with:
   - Model, tokenizer, reward functions
   - Generation parameters (temperature, top_p, num_generations)
   - Training hyperparameters (learning rate, batch size, KL coefficient)
5. Training loop:
   - Generate multiple completions per prompt (num_generations)
   - Calculate rewards using ParallelSUMORewardCalculator
   - Update policy via GRPO algorithm
6. Save model to `/home/samuel/SCU_TSC/model/grpo_model/`

**Reward Calculation Flow:**

1. Extract model decision from output using regex
2. Format reward scoring:
   - Strict: exact JSON match (+1.0)
   - Partial: regex extraction success (-0.5)
   - Invalid: no extraction (-10.0)
3. If valid format, calculate TSC reward:
   - Load SUMO state file
   - Execute decision (extend or switch phase)
   - Simulate for extend_seconds
   - Measure queue change: reward = tanh(-delta_queue / scale)
4. Combine rewards: final = format_weight * format_reward + tsc_weight * tsc_reward

**State Management:**
- SUMO state files (XML) saved at each decision point during data generation
- State files loaded during reward calculation to recreate exact traffic conditions
- Supports parallel reward calculation via multiprocessing (each worker gets unique port)

## Key Abstractions

**GRPODataEntry:**
- Purpose: Single training example with all context needed for decision making
- Examples: `/home/samuel/SCU_TSC/grpo/dataset_generator.py`
- Pattern: dataclass with fields: id, scenario, junction_id, simulation_time, phase info, prompt JSON, state_file path

**SUMOInterface:**
- Purpose: Clean abstraction over TraCI API with error handling and port management
- Examples: `/home/samuel/SCU_TSC/grpo/sumo_interface.py`
- Pattern: Context manager style with `start()`, `step()`, `close()` methods; caches phase information

**RewardChainConfig:**
- Purpose: Configure multi-component reward function
- Examples: `/home/samuel/SCU_TSC/grpo/config.py`, `/home/samuel/SCU_TSC/grpo/reward.py`
- Pattern: dataclass combining format_reward, tsc_reward weights and individual component configs

**TrainingConfig (Central Configuration):**
- Purpose: Single source of truth for all training parameters
- Examples: `/home/samuel/SCU_TSC/config/training_config.yaml`, loaded via `/home/samuel/SCU_TSC/grpo/config.py`
- Pattern: YAML file with sections: training (sft, grpo), simulation (sumo, scenarios), reward (chain, format, tsc, max_pressure), paths, logging

**ParallelSUMORewardCalculator:**
- Purpose: Parallel execution of SUMO-based reward calculations
- Examples: `/home/samuel/SCU_TSC/grpo/sumo_reward.py`
- Pattern: Process pool with worker function `calculate_tsc_reward_worker()`

## Entry Points

**SFT Training:**
- Location: `/home/samuel/SCU_TSC/grpo/sft_training.py`
- Triggers: `python -m grpo.sft_training` or `python grpo/sft_training.py`
- Responsibilities: Load SFT dataset, train model on format learning, validate and save checkpoints

**GRPO Training:**
- Location: `/home/samuel/SCU_TSC/grpo/training.py`
- Triggers: `python -m grpo.training` or `python grpo/training.py`
- Responsibilities: Load GRPO dataset, configure reward chain, run GRPO optimization

**Data Generation:**
- Location: `/home/samuel/SCU_TSC/grpo/generate_grpo_dataset.py`, `/home/samuel/SCU_TSC/grpo/parallel_runner.py`
- Triggers: `python -m grpo.generate_grpo_dataset` or via `parallel_runner.py`
- Responsibilities: Run SUMO simulations, collect decision points, save datasets

**SUMO Simulator (Legacy):**
- Location: `/home/samuel/SCU_TSC/sumo_simulation/sumo_simulator.py`
- Triggers: `python sumo_simulation/sumo_simulator.py [--env SCENARIO] [--grpo]`
- Responsibilities: Direct simulation control, historical data collection, max-pressure control

**Configuration Reader:**
- Location: `/home/samuel/SCU_TSC/config/read_config.py`
- Triggers: `python config/read_config.py --key simulation.sumo.max_workers`
- Responsibilities: Extract nested config values from YAML for shell scripting

## Error Handling

**Strategy:** Try-except with fallback defaults

**Patterns:**
- SUMO connection failures: Retry with random ports (up to 10 attempts)
- Format parsing failures: Return invalid_format reward (-10.0)
- SUMO reward calculation failures: Return 0.0 reward with error logging
- Missing state files: Skip sample or return error TSCResult
- Phase ID validation: Raise ValueError with helpful message listing available phases

**Configuration validation:**
- `GRPOTrainingConfig.__post_init__()` validates numeric ranges (learning_rate > 0, temperature in [0,2], etc.)
- `TrainingConfig.from_yaml()` ensures required sections exist
- `MaxPressureConfig` parameters validated in decision function

## Cross-Cutting Concerns

**Logging:**
- Approach: Print statements with scenario/task prefixes (e.g., `[scenario_name] message`)
- Training: Uses TRL/Unsloth built-in logging (log steps, wandb integration)
- Configuration: `verbose` flag controls SUMO startup/warmup logs

**Validation:**
- Format: JSON parsing + regex fallback for `{"extend": "yes/no"}` output
- Decision: Time constraints (min_green, max_green), phase existence checks
- Config: Range validation in dataclass `__post_init__` methods

**Authentication:**
- Not applicable (local training, no external services)

**Parallel Execution:**
- Data generation: Multiprocessing via `parallel_runner.py`
- Reward calculation: `ParallelSUMORewardCalculator` with process pool
- Port management: `find_available_port()` for avoiding SUMO port conflicts

**Random Seed Control:**
- Fixed seed (3407) for training reproducibility
- Random offsets for green time parameters during data generation (for diversity)
---

*Architecture analysis: 2025-02-03*
