# Architecture

**Analysis Date:** 2025-02-02

## Pattern Overview

**Overall:** Multi-Stage Pipeline for Traffic Signal Control RL Training

**Key Characteristics:**
- Simulation-driven data collection pipeline using SUMO traffic simulator
- Multi-stage training data generation (GRPO dataset → SFT dataset → Model training)
- Parallelizable scenario processing for data collection
- State management for counterfactual reasoning in reinforcement learning

## Layers

**Data Generation Layer (grpo/):**
- Purpose: Generate training data through SUMO simulation and expert policy
- Location: `/home/samuel/SCU_TSC/grpo/`
- Contains: Dataset generators, configuration, SUMO interface, prompt builders
- Depends on: SUMO (via TraCI), Python multiprocessing
- Used by: Training scripts, evaluation pipelines

**Simulation Interface Layer:**
- Purpose: Abstract SUMO TraCI operations for traffic simulation control
- Location: `/home/samuel/SCU_TSC/grpo/sumo_interface.py`
- Contains: `SUMOInterface` class, `PhaseInfo` dataclass
- Depends on: SUMO TraCI library, SUMO binary
- Used by: `GRPODatasetGenerator`, `SUMOSimulator`

**Training Layer:**
- Purpose: Train language models using generated datasets (SFT, eventually GRPO)
- Location: `/home/samuel/SCU_TSC/grpo/sft_training.py`
- Contains: `train_sft()` function, dataset loading utilities
- Depends on: Unsloth, HuggingFace transformers/datasets, PyTorch
- Used by: Training pipelines

**Simulation Engine Layer (sumo_simulation/):**
- Purpose: Complete SUMO simulator wrapper with state management and metrics
- Location: `/home/samuel/SCU_TSC/sumo_simulation/sumo_simulator.py`
- Contains: `SUMOSimulator` class with traffic light control, data collection, GRPO evaluation
- Depends on: SUMO TraCI
- Used by: Legacy code, some evaluation scenarios

## Data Flow

**GRPO Dataset Generation:**

1. **Initialization**: `GRPOConfig` defines parameters (extend_seconds, warmup_steps, etc.)
2. **Scenario Discovery**: `ParallelRunner.get_all_scenarios()` scans `/home/samuel/SCU_TSC/sumo_simulation/environments/` for `.sumocfg` files
3. **SUMO Launch**: `SUMOInterface.start()` launches SUMO binary with TraCI connection, executes warmup steps
4. **Data Collection Loop** (`GRPODatasetGenerator._run_collection_loop()`):
   - Step simulation forward
   - Track each traffic light's phase changes and green time elapsed
   - At decision points (min_green, then every extend_seconds), collect:
     - Current phase ID, green elapsed time, min/max green times
     - Phase order (valid phases only)
     - Queue counts for all phases (`get_all_phases_queue()`)
   - Save simulation state XML (optional, controlled by `state_save_interval`)
   - Create `GRPODataEntry` with prompt JSON
5. **Filtering**: Probabilistic filtering based on non-zero phase ratio to reduce low-traffic samples
6. **Output**: Save `grpo_dataset.json` with entries containing prompt, state file reference, metadata

**SFT Dataset Generation:**

1. **Load GRPO Data**: `load_grpo_datasets()` reads all scenario `grpo_dataset.json` files
2. **Transform**: `create_sft_entry()` wraps each prompt with system prompt and adds random yes/no response
3. **Format**: Creates HuggingFace chat format with system/user/assistant messages
4. **Save**: Outputs `sft_dataset.json` and `sft_dataset.jsonl`

**SFT Training:**

1. **Load Dataset**: `load_sft_dataset()` loads and splits into train/eval
2. **Format**: `format_for_training()` applies chat template to create training text
3. **Train**: Unsloth `FastLanguageModel` + `SFTTrainer` trains LoRA adapter on Qwen2.5-0.5B-Instruct
4. **Save**: Saves LoRA checkpoint and merged 16-bit model

**State Management Flow:**

- **Purpose**: Enable counterfactual reasoning (evaluating multiple actions from same state)
- **Save**: `SUMOInterface.save_state()` writes current simulation state to XML
- **Restore**: `SUMOInterface.load_state()` restores simulation to exact state
- **Use Case**: `step_with_state_reload()` in `SUMOSimulator` evaluates all phase×duration combinations from a checkpoint

## Key Abstractions

**GRPODataEntry:**
- Purpose: Single training data point with traffic state and metadata
- Examples: `/home/samuel/SCU_TSC/grpo/dataset_generator.py` (line 20-38)
- Pattern: Python dataclass with fields: id, scenario, junction_id, simulation_time, current_phase_id, phase_order, phase_metrics, prompt, state_file

**PhaseInfo:**
- Purpose: Represents a traffic signal phase with metadata
- Examples: `/home/samuel/SCU_TSC/grpo/sumo_interface.py` (line 44-52)
- Pattern: Dataclass with phase_id, state, duration, min_dur, max_dur, controlled_lanes

**GRPOConfig:**
- Purpose: Centralized configuration for data generation
- Examples: `/home/samuel/SCU_TSC/grpo/config.py` (line 13-76)
- Pattern: Dataclass with @dataclass decorator, __post_init__ for auto-setup (directory creation, CPU count detection)

**System Prompt Template:**
- Purpose: Instruction template for LLM-based traffic signal control
- Examples: `/home/samuel/SCU_TSC/grpo/config.py` (line 82-111)
- Pattern: Multi-line string with {extend_decision_input_json} placeholder, replaced via str.replace() to avoid format() conflicts

## Entry Points

**Data Generation:**
- Location: `/home/samuel/SCU_TSC/grpo/generate_grpo_dataset.py`
- Triggers: Command-line invocation with `python -m grpo.generate_grpo_dataset --scenario <name>` or `--all`
- Responsibilities: Argument parsing, config building, invokes `ParallelRunner.run()` or `GRPODatasetGenerator.generate_for_scenario()`

**SFT Dataset Generation:**
- Location: `/home/samuel/SCU_TSC/grpo/generate_sft_dataset.py`
- Triggers: `python -m grpo.generate_sft_dataset [--sample-size N]`
- Responsibilities: Loads GRPO datasets, transforms to SFT format with random labels

**SFT Training:**
- Location: `/home/samuel/SCU_TSC/grpo/sft_training.py`
- Triggers: `python -m grpo.sft_training [--dataset PATH] [--output-dir DIR]`
- Responsibilities: Loads dataset, trains LoRA adapter, saves model

**SUMO Simulator (Legacy/Standalone):**
- Location: `/home/samuel/SCU_TSC/sumo_simulation/sumo_simulator.py`
- Triggers: Direct script execution or `initialize_sumo()` call
- Responsibilities: Full-featured SUMO wrapper with metrics collection, max-pressure control, GRPO evaluation methods

**Testing:**
- Location: `/home/samuel/SCU_TSC/grpo/test_generator.py`
- Triggers: `python -m grpo.test_generator --single <scenario>` or `--parallel N`
- Responsibilities: Unit tests for prompt builder, config; integration tests for data generation

## Error Handling

**Strategy:** Try-except with graceful degradation

**Patterns:**
- SUMO connection failures: Retry with random ports (up to 10 attempts), raise exception if all fail
- File I/O errors: Print error message, return empty list/dict
- TraCI exceptions: Catch `traci.exceptions.TraCIException`, return default values (0, empty dict)
- Scenario filtering: Skip missing/invalid scenarios, continue with valid ones

**SUMO Binary Detection:**
- Search multiple common installation paths
- Fall back to PATH lookup
- Exit with error if not found

## Cross-Cutting Concerns

**Logging:** Print statements with scenario prefixes (e.g., `[scenario_name] message`)

**Validation:**
- Check scenario directory exists before processing
- Validate .sumocfg file presence
- Filter out phases without green lights (only 'G' or 'g' in state string)

**Authentication:** None (local execution only)

**Configuration Management:**
- Centralized in `GRPOConfig` dataclass
- Environment-based: `SUMO_HOME` auto-detection from multiple paths
- Command-line overrides via argparse in entry point scripts

---

*Architecture analysis: 2025-02-02*
