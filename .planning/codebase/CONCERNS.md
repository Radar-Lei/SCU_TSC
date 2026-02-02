# Codebase Concerns

**Analysis Date:** 2025-02-03

## Tech Debt

**Large Monolithic File:**
- Issue: `sumo_simulation/sumo_simulator.py` contains 2091 lines of code
- Files: `/home/samuel/SCU_TSC/sumo_simulation/sumo_simulator.py`
- Impact: Difficult to maintain, test, and navigate. Contains mixed concerns (simulation control, data collection, GRPO evaluation, metrics calculation)
- Fix approach: Refactor into smaller modules by responsibility:
  - `sumo_core.py` - basic simulation control
  - `traffic_data_collector.py` - data collection methods
  - `grpo_evaluator.py` - GRPO-specific evaluation methods
  - `metrics_calculator.py` - traffic metrics computation

**Configuration Complexity:**
- Issue: `grpo/config.py` contains 746 lines with multiple overlapping config classes (`GRPOConfig`, `GRPOTrainingConfig`, `SFTTrainingConfig`, `TrainingConfig`, etc.)
- Files: `/home/samuel/SCU_TSC/grpo/config.py`
- Impact: Confusing which config to use when. Multiple ways to load same config. Risk of inconsistency
- Fix approach: Consolidate into a single hierarchical config with clear inheritance. Use dataclass composition over separate classes

**Debug Prints in Production Code:**
- Issue: Debug print statements in `grpo/training.py` lines 189-195 are active during training
- Files: `/home/samuel/SCU_TSC/grpo/training.py`
- Impact: Clutters training logs, affects performance
- Fix approach: Replace with proper logging framework (e.g., `logging` module) and use log levels

## Known Bugs

**SUMO Port Conflict in Parallel Execution:**
- Symptoms: Random "port already in use" errors when running multiple SUMO instances in parallel
- Files: `/home/samuel/SCU_TSC/grpo/parallel_runner.py`, `/home/samuel/SCU_TSC/grpo/sumo_interface.py`
- Trigger: Running data generation with `--parallel > 1`
- Workaround: Use sequential execution or manually specify ports
- Root cause: `find_available_port()` has race condition - port may be taken between check and bind

**Reward Calculation Silent Failures:**
- Symptoms: TSC reward sometimes returns 0.0 without clear indication of failure
- Files: `/home/samuel/SCU_TSC/grpo/sumo_reward.py`
- Trigger: SUMO state file corruption or SUMO binary crashes
- Workaround: Check logs for "TSC reward计算失败" messages
- Root cause: `calculate_tsc_reward_single()` catches all exceptions and returns generic failure

**Data Entry State File References:**
- Symptoms: Some GRPO dataset entries have empty `state_file` field
- Files: `/home/samuel/SCU_TSC/grpo/dataset_generator.py`
- Trigger: When `state_save_interval > 1` in config
- Workaround: Set `state_save_interval=1` to save all states
- Root cause: Lines 347-351 conditionally skip state file saving, leaving empty string

## Security Considerations

**Path Traversal in State File Loading:**
- Risk: State file paths from user-controlled JSON could access arbitrary files
- Files: `/home/samuel/SCU_TSC/grpo/sumo_reward.py`, `/home/samuel/SCU_TSC/grpo/training.py`
- Current mitigation: None - paths are used directly in `os.path.join()`
- Recommendations:
  - Validate state_file paths are within expected scenario directories
  - Use `os.path.normpath()` and `os.path.abspath()` to detect escape attempts
  - Add allowlist of permitted directories

**Uncontrolled SUMO Command Execution:**
- Risk: SUMO binary path from environment could be manipulated
- Files: `/home/samuel/SCU_TSC/sumo_simulation/sumo_simulator.py`, `/home/samuel/SCU_TSC/grpo/sumo_interface.py`
- Current mitigation: Limited validation of SUMO_HOME and binary paths
- Recommendations:
  - Validate SUMO binary paths against allowlist
  - Use absolute paths only, no PATH searching
  - Check binary permissions and signatures

**Subprocess Timeout Not Enforced:**
- Risk: SUMO processes could hang indefinitely
- Files: `/home/samuel/SCU_TSC/grpo/validate_data.py` (line 592)
- Current mitigation: 5 second timeout on version check only, not on SUMO execution
- Recommendations: Add timeout wrappers to all SUMO execution calls

## Performance Bottlenecks

**SUMO Sequential Reward Calculation:**
- Problem: Each reward calculation spawns new SUMO process, loads state, runs simulation, exits
- Files: `/home/samuel/SCU_TSC/grpo/sumo_reward.py`
- Cause: Process-per-sample architecture with cold start overhead
- Improvement path:
  - Use persistent SUMO processes with keep-alive connections
  - Batch multiple state evaluations per SUMO instance
  - Implement SUMO process pool instead of per-sample spawning

**Large Dataset JSON Loading:**
- Problem: Entire GRPO datasets loaded into memory during training
- Files: `/home/samuel/SCU_TSC/grpo/training.py`
- Cause: `load_grpo_dataset()` uses `json.load()` on full file
- Improvement path:
  - Use memory-mapped JSON or streaming parsers
  - Implement lazy loading with on-demand state file access
  - Consider database format for large datasets

**No Result Caching:**
- Problem: Same (prompt, decision) pairs re-evaluated in SUMO multiple times during GRPO training
- Files: `/home/samuel/SCU_TSC/grpo/reward.py`, `/home/samuel/SCU_TSC/grpo/sumo_reward.py`
- Cause: No caching mechanism for TSC reward calculations
- Improvement path:
  - Implement LRU cache keyed by (state_file_hash, decision)
  - Store computed rewards in local database
  - Pre-compute rewards for training dataset

## Fragile Areas

**SUMO State File Compatibility:**
- Files: `/home/samuel/SCU_TSC/grpo/sumo_interface.py`, `/home/samuel/SCU_TSC/grpo/sumo_reward.py`
- Why fragile: State files depend on exact SUMO version, network file, and configuration
- Safe modification:
  - Always validate state file version compatibility before use
  - Re-generate state files when SUMO version changes
  - Add state file schema versioning
- Test coverage: Limited - state file loading has minimal unit tests

**Data Format Assumptions:**
- Files: `/home/samuel/SCU_TSC/grpo/dataset_generator.py`, `/home/samuel/SCU_TSC/grpo/prompt_builder.py`
- Why fragile: Tightly coupled to specific JSON structure with hardcoded field names
- Safe modification:
  - Use schema validation (pydantic/jsonschema)
  - Create data models with clear serialization/deserialization
  - Write migration scripts for format changes
- Test coverage: Moderate - `grpo/validate_data.py` exists but not run in CI

**Configuration Parameter Interaction:**
- Files: `/home/samuel/SCU_TSC/grpo/config.py`
- Why fragile: Many interdependent parameters (min_green, max_green, extend_seconds, temperature, etc.)
- Safe modification:
  - Add parameter validation rules
  - Document allowed value ranges and interactions
  - Create config validation tests
- Test coverage: Good - extensive `__post_init__` validation

## Scaling Limits

**SUMO Process Parallelization:**
- Current capacity: ~4-8 parallel SUMO workers
- Limit: System memory and CPU cores. Each SUMO instance uses ~200-500MB
- Scaling path:
  - Distribute across multiple machines
  - Use containerized SUMO instances with resource limits
  - Implement job queue for SUMO evaluations

**Dataset Size:**
- Current capacity: ~10,000-50,000 training samples before memory issues
- Limit: In-memory dataset loading in `load_grpo_dataset()`
- Scaling path:
  - Implement streaming data loaders
  - Use disk-backed caching
  - Consider out-of-core training approaches

**GRPO Training Memory:**
- Current capacity: Batch size 2-4 depending on model size and sequence length
- Limit: GPU memory, especially with gradient accumulation
- Scaling path:
  - Implement gradient checkpointing (partially done)
  - Use mixed precision training
  - Distribute training across multiple GPUs

## Dependencies at Risk

**Unsloth Version Compatibility:**
- Risk: Unsloth releases often break TRL compatibility
- Impact: Training scripts fail with import errors or runtime errors
- Migration plan:
  - Pin specific working versions in requirements.txt
  - Test upgrade path in isolation before deployment
  - Consider switching to standard PEFT for stability

**SUMO Installation Variability:**
- Risk: SUMO installation paths vary across systems (Homebrew, apt, source)
- Impact: `find_sumo_binary()` heuristic fails in some environments
- Migration plan:
  - Document supported installation methods
  - Provide Docker container with pre-installed SUMO
  - Add SUMO detection tests to CI

**TRL GRPO API Changes:**
- Risk: TRL library is under active development, GRPOTrainer API may change
- Impact: `grpo/training.py` reward function signature may become incompatible
- Migration plan:
  - Pin TRL version in requirements
  - Monitor TRL release notes for breaking changes
  - Abstract reward function interface to absorb API changes

## Missing Critical Features

**No Model Evaluation Pipeline:**
- Problem: No automated evaluation of trained models on test scenarios
- Blocks: Assessing model quality, comparing different training runs
- Status: Manual evaluation through ad-hoc scripts

**No Checkpoint Resume:**
- Problem: Training cannot resume from interruption without starting from scratch
- Blocks: Long-running training jobs on unreliable infrastructure
- Status: Trainer saves checkpoints but no resume mechanism in training scripts

**No Data Versioning:**
- Problem: No tracking of which dataset version was used for training
- Blocks: Reproducibility, debugging training issues
- Status: Dataset files have no version metadata

## Test Coverage Gaps

**SUMO Interface Not Unit Tested:**
- What's not tested: Port allocation, state file loading, phase control
- Files: `/home/samuel/SCU_TSC/grpo/sumo_interface.py`
- Risk: Refactoring may break SUMO integration
- Priority: High - core functionality with complex error handling

**Reward Calculation Not Unit Tested:**
- What's not tested: Format reward regex matching, TSC reward edge cases
- Files: `/home/samuel/SCU_TSC/grpo/reward.py`, `/home/samuel/SCU_TSC/grpo/sumo_reward.py`
- Risk: Reward signal errors directly affect training quality
- Priority: High - directly impacts model learning

**Max Pressure Algorithm Not Tested:**
- What's not tested: Decision logic with various queue configurations
- Files: `/home/samuel/SCU_TSC/grpo/max_pressure.py`
- Risk: Baseline comparison may be incorrect
- Priority: Medium - important for evaluation but not critical for training

**Data Generation Not Integration Tested:**
- What's not tested: End-to-end GRPO dataset generation
- Files: `/home/samuel/SCU_TSC/grpo/dataset_generator.py`
- Risk: Dataset format changes break training
- Priority: Medium - validation script exists but not automated

---

*Concerns audit: 2025-02-03*
