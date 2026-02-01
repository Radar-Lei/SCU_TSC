# Codebase Concerns

**Analysis Date:** 2025-02-02

## Tech Debt

**Hardcoded User Paths:**
- Issue: Multiple files contain hardcoded paths to `/home/samuel/SCU_TSC`, making the code non-portable across different users and systems
- Files: `grpo/config.py:50`, `grpo/config.py:53`, `grpo/sft_training.py:80`, `grpo/sft_training.py:81`, `grpo/sft_training.py:243`, `grpo/sft_training.py:249`, `grpo/generate_sft_dataset.py:167`, `grpo/generate_sft_dataset.py:173`
- Impact: Code cannot run on other machines without modifications; requires manual path replacement for each deployment
- Fix approach: Replace hardcoded paths with environment variables or relative path resolution using `pathlib.Path` or `os.path.dirname(os.path.abspath(__file__))`

**SUMO_HOME Environment Variable Discovery:**
- Issue: SUMO_HOME path discovery is duplicated across multiple files with different hardcoded path lists
- Files: `grpo/sumo_interface.py:20-35`, `sumo_simulation/sumo_simulator.py:17-35`
- Impact: Maintenance burden when adding new SUMO installation paths; inconsistent behavior between modules
- Fix approach: Create a single shared utility module for SUMO environment configuration

**Duplicate SUMO Interface Implementations:**
- Issue: Two separate SUMO wrapper implementations exist (`grpo/sumo_interface.py` and `sumo_simulation/sumo_simulator.py`) with overlapping functionality
- Files: `grpo/sumo_interface.py` (428 lines), `sumo_simulation/sumo_simulator.py` (2091 lines)
- Impact: Code duplication, inconsistent behavior, double maintenance effort
- Fix approach: Consolidate into a single shared SUMO interface module; `grpo/sumo_interface.py` could become a lightweight wrapper around the full simulator

**Generated Files in Source Tree:**
- Issue: `unsloth_compiled_cache/` directory contains auto-generated files that should not be version-controlled
- Files: `unsloth_compiled_cache/Unsloth*.py`, `unsloth_compiled_cache/.locks/`
- Impact: Repository bloat; merge conflicts; unnecessary storage usage
- Fix approach: Add to `.gitignore` (currently missing from gitignore entries)

## Known Bugs

**Bare Except Blocks:**
- Symptoms: Exceptions are silently caught without logging, making debugging extremely difficult
- Files: `sumo_simulation/sumo_simulator.py:290`, `sumo_simulation/sumo_simulator.py:314`, `sumo_simulation/sumo_simulator.py:438`, `sumo_simulation/sumo_simulator.py:1146`, `sumo_simulation/sumo_simulator.py:1767`, multiple files in `unsloth_compiled_cache/`
- Trigger: Any TraCI exception during simulation connection or execution
- Workaround: None known; errors are silently ignored
- Fix approach: Replace `except:` with `except Exception as e:` and add proper logging

**sys.exit() Call on Import Failure:**
- Symptoms: Program terminates immediately if traci cannot be imported, with no graceful handling
- Files: `grpo/sumo_interface.py:41`
- Trigger: Running on system without SUMO properly installed
- Workaround: Install SUMO before import
- Fix approach: Use lazy import within functions, raise proper ImportError with installation instructions

**Random Decision Labels in SFT Training:**
- Symptoms: SFT dataset generation uses `random.choice(["yes", "no"])` for training labels
- Files: `grpo/generate_sft_dataset.py:77`
- Trigger: Every SFT dataset generation run
- Workaround: None
- Fix approach: This may be intentional for format-only training, but should be documented; if actual decision quality matters, need to implement expert policy

## Security Considerations

**No Input Validation:**
- Risk: User-provided file paths (scenario directories, output paths) are not validated before use
- Files: `grpo/dataset_generator.py:199-208`, `grpo/parallel_runner.py:38-48`
- Current mitigation: None
- Recommendations: Add path validation to prevent directory traversal attacks; ensure paths are within expected directories

**Unrestricted File Operations:**
- Risk: State files and dataset files are written to arbitrary locations without permission checks
- Files: `grpo/dataset_generator.py:344-350`, `grpo/dataset_generator.py:382-392`
- Current mitigation: None
- Recommendations: Validate output directory permissions; check for existing files before overwriting

**Docker Container Runs as Root:**
- Risk: Dockerfile contains `USER root`, containers run with elevated privileges
- Files: `docker/Dockerfile:3`
- Current mitigation: None
- Recommendations: Create and use non-root user in Dockerfile

## Performance Bottlenecks

**Large Monolithic Simulator File:**
- Problem: `sumo_simulation/sumo_simulator.py` is 2091 lines, containing multiple responsibilities
- Files: `sumo_simulation/sumo_simulator.py`
- Cause: Accumulation of features over time without refactoring
- Improvement path: Split into smaller modules: core simulation interface, data collection, signal control, GRPO mode

**Simulation State File I/O:**
- Problem: Every decision point may save an XML state file to disk
- Files: `grpo/dataset_generator.py:347-350`
- Cause: Synchronous file I/O during simulation loop
- Improvement path: Use asynchronous I/O or batch state writes; implement `state_save_interval` more aggressively

**No Caching of Phase Information:**
- Problem: Phase metadata is queried repeatedly from SUMO during simulation
- Files: `grpo/sumo_interface.py:245-318` (partially cached, but only per-TL)
- Cause: Each simulation step may query phase information
- Improvement path: Ensure all phase data is cached at startup; validate cache invalidation

**Random Data Filtering:**
- Problem: Probabilistic data filtering using `random.random()` may discard valuable training data
- Files: `grpo/dataset_generator.py:326-340`
- Cause: Heuristic to reduce low-queue scenarios
- Improvement path: Make filtering configurable; consider stratified sampling instead

## Fragile Areas

**SUMO Port Assignment:**
- Files: `grpo/parallel_runner.py:100`, `grpo/sumo_interface.py:130`
- Why fragile: Port conflicts can occur if base_port + offset collides with existing services; random ports may still conflict
- Safe modification: Use proper port range scanning; add retry logic with different port ranges
- Test coverage: No tests for port conflict scenarios

**TraCI Connection Lifecycle:**
- Files: `grpo/sumo_interface.py:96-156`, `sumo_simulation/sumo_simulator.py:293-438`
- Why fragile: Connection state tracking is manual; exceptions during startup may leave zombie SUMO processes
- Safe modification: Use context managers for connection lifecycle; add process cleanup in finally blocks
- Test coverage: No tests for connection failure scenarios

**Phase Duration Calculations:**
- Files: `grpo/sumo_interface.py:327-343`, `grpo/dataset_generator.py:88-124`
- Why fragile: Float comparison for decision point detection uses tolerance; edge cases around min_green boundaries
- Safe modification: Use integer time steps internally; document tolerance semantics
- Test coverage: No unit tests for decision point logic

**Multiprocessing with Shared State:**
- Files: `grpo/parallel_runner.py:78-128`
- Why fragile: SUMO instances share no state but use port-based isolation; race conditions possible if port allocation fails
- Safe modification: Add proper port allocation service; ensure process cleanup on failure
- Test coverage: No integration tests for parallel execution

## Scaling Limits

**Single Machine Processing:**
- Current capacity: Limited by CPU cores and SUMO instances per machine
- Limit: Cannot distribute across multiple machines
- Scaling path: Implement distributed task queue (Redis, Celery) for multi-machine GRPO dataset generation

**SUMO Simulation Throughput:**
- Current capacity: One SUMO process per scenario per CPU core
- Limit: Real-time simulation is ~1-10x slower than real time depending on scenario complexity
- Scaling path: Use SUMO's parallel execution capabilities; consider scenario pre-processing

**Model Training Memory:**
- Current capacity: Limited by GPU memory; default batch_size=2
- Limit: Full SFT training may OOM on smaller GPUs
- Scaling path: Implement gradient accumulation; add automatic batch size tuning based on available GPU memory

## Dependencies at Risk

**Unsloth Compiled Cache:**
- Risk: Auto-generated Python files in `unsloth_compiled_cache/` may become incompatible when Unsloth library updates
- Impact: Training may fail with cryptic errors; need to delete cache and regenerate
- Migration plan: Delete `unsloth_compiled_cache/` directory on library version change; add to `.gitignore`

**SUMO Version Compatibility:**
- Risk: Code may be tied to specific SUMO version features
- Impact: SUMO upgrades may break TraCI API usage
- Migration plan: Add SUMO version detection and compatibility layer; document tested SUMO versions

**Python 3.13 Dependency:**
- Risk: `sumo_simulation/pyproject.toml` specifies `requires-python = ">=3.13"`
- Impact: Many systems don't have Python 3.13 yet; limits deployment options
- Migration plan: Test on Python 3.11-3.12; lower minimum version if compatible

**ModelScope Dependency:**
- Risk: ModelScope is Chinese-specific model hub; may have reliability or access issues
- Impact: Cannot download models if ModelScope is unavailable
- Migration plan: Add fallback to HuggingFace for model downloads

## Missing Critical Features

**No Test Suite:**
- Problem: No unit tests, integration tests, or test infrastructure found
- Blocks: Safe refactoring; confidence in code correctness
- Priority: High

**No Logging Framework:**
- Problem: All logging uses `print()` statements; no log levels, structured logging, or log rotation
- Blocks: Production deployment; debugging in containerized environments
- Priority: High

**No Configuration Management:**
- Problem: Configuration scattered across multiple files; no unified config loading
- Blocks: Easy experimentation with different parameters
- Priority: Medium

**No Error Recovery in Data Generation:**
- Problem: If single scenario fails during parallel generation, entire batch may be affected
- Blocks: Large-scale dataset generation
- Priority: Medium

**No Data Validation:**
- Problem: Generated datasets are not validated for schema correctness
- Blocks: Catching data quality issues before training
- Priority: Medium

## Test Coverage Gaps

**What's not tested:**
- SUMO connection lifecycle and error handling
- Phase calculation and decision point detection logic
- Data filtering logic and probability calculations
- Port allocation and conflict resolution
- State file save/load operations
- Prompt building and JSON format validation

**Files:**
- `grpo/sumo_interface.py`: 0% test coverage
- `grpo/dataset_generator.py`: 0% test coverage
- `grpo/parallel_runner.py`: 0% test coverage
- `grpo/prompt_builder.py`: 0% test coverage

**Risk:** Core data generation logic has no automated tests; bugs only discovered during manual runs

**Priority:** High - Add unit tests for decision point logic, phase calculations, and data format validation

---

*Concerns audit: 2025-02-02*
