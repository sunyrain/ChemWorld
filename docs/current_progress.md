# Current Progress

This document summarizes the current implementation state of ChemWorld-Bench.
The platform is now organized around one public environment,
`ChemWorld`, backed by the Chemical World Model foundation layer.

## What Exists

The repository currently provides:

- a Python package installable with `python -m pip install -e ".[dev]"`;
- one Gymnasium environment, `ChemWorld`;
- a unified task registry over one shared world law;
- an event-driven reaction transition model;
- a phase partition and downstream separation module;
- executable physical constitution checks;
- noisy, partial instrument observations with explicit `observed_mask` fields;
- standard trajectory logging, replay verification, metrics, and leaderboard
  aggregation;
- official baseline agents;
- local CLI workflows;
- documentation, runnable example scripts, and executed notebooks.
- a twelve-day executed tutorial sequence under `notebooks/tutorials/`.

## Scientific Model

`ChemWorld` currently models a virtual 100 mL jacketed reaction and separation
workflow. The hidden state includes species amounts, active/dead catalyst,
phase ledgers, volume, temperature, pressure proxy, elapsed time, cost, risk,
and sample consumption.

The reaction network is:

- `A -> P`, target product formation;
- `A -> B`, byproduct formation;
- `P -> D`, product degradation;
- `A + P -> E`, coupled impurity formation;
- `Cat_active -> Cat_dead`, catalyst deactivation.

Continuous dynamics are integrated with `scipy.integrate.solve_ivp`. Rate
constants follow Arrhenius temperature dependence and are modified by catalyst,
solvent, catalyst activity, concentration, and stirring speed. Temperature is
updated through a simplified energy balance with jacket heat, heat loss, and
reaction heat.

Downstream processing tracks aqueous/organic phase volume, product
partitioning, impurity carryover, phase settling, separation loss, washing,
drying, concentration, transfer loss, purity, recovery, solvent loss, and
process mass-balance error.

## Foundation Layer

`chemworld.foundation` contains the reusable base layer:

- ontology primitives: `Substance`, `Vessel`, `Instrument`, `Operation`,
  `Reaction`, and `StateVariable`;
- lightweight units and conversions;
- `WorldState`, public `Observation`, `Ledger`, and `OperationRecord`;
- `PhysicalConstitution` checks for non-negativity, unit validity, vessel
  bounds, risk range, material conservation, observation non-omniscience,
  measurement cost, and action preconditions;
- transition and observation kernel protocols.

Learned local world-model interfaces now live in `chemworld.models`, not in the
foundation layer. This keeps the hidden physical world separate from the
student or agent belief state inferred from trajectories.

## Public Interface

The Gym API is:

```python
import gymnasium as gym
import chemworld

env = gym.make(
    "ChemWorld",
    task_id="reaction-optimization-standard",
    seed=42,
)
obs, info = env.reset()
obs, reward, terminated, truncated, info = env.step(
    {"operation": "add_solvent", "volume_L": 0.03, "solvent": 2}
)
```

Supported operations are:

- `add_solvent`;
- `add_reagent`;
- `add_catalyst`;
- `heat`;
- `wait`;
- `sample`;
- `quench`;
- `add_phase`;
- `add_extractant`;
- `mix`;
- `settle`;
- `separate_phase`;
- `wash`;
- `dry`;
- `concentrate`;
- `transfer`;
- `terminate`;
- `measure`.

Supported instruments are:

- `hplc`;
- `gc`;
- `uvvis`;
- `final_assay`.

## Benchmark Layer

The CLI supports:

```bash
chemworld run
chemworld evaluate
chemworld verify
chemworld leaderboard
chemworld suite
chemworld inspect-constitution
```

Every run can produce a trajectory JSONL and a submission manifest. Replay
verification recomputes environment transitions and observations from the
recorded operations. `verify --constitution` also requires recorded
constitution checks and action preconditions to pass.

Trajectory observations distinguish measured values from unknown values. Unseen
fields are serialized as `null` in JSONL, represented as `NaN` in Gym arrays, and
tracked with `observed_mask` and `observed_keys`. Official leaderboard metrics
use `leaderboard_score`, which is only populated by final-assay measurements;
`observed_reward` remains available as online feedback for agents.

Instrument observations also carry `raw_signal`, `processed_estimate`, and
`uncertainty` fields. These make the observation kernel closer to a real
instrument workflow: instruments produce signals, processed estimates are
derived from those signals, and agents maintain a belief state from the observed
trajectory.

Failed action preconditions now return empty, non-informative observations and
explicit `error_message` fields. Final assay is treated as a terminal scoring
event: it requires a terminated reaction, ends the episode, and cannot be used
to create repeated leaderboard scores.

## Baselines

Current official agents include:

- `random`;
- `scripted_chemistry`;
- `lhs`;
- `greedy`;
- `gp_bo`;
- `rf_ei`;
- `safe_gp_bo`;
- `llm_planner` adapter;
- `llm_replay` adapter.

Recipe-space optimizers such as LHS and BO internally choose terminal recipe
parameters, then execute them as event sequences. This keeps the public
environment interface unified while still supporting standard optimizer
baselines.

## Data And Ethics

The data layer includes:

- versioned trajectory records;
- JSONL logging;
- submission manifests;
- anonymization helpers for human pilot data;
- structured explanation fields.

Human data use should still require informed consent, separation of teaching
grades from research use, and removal of identifiable text before release.

## Current Validation

The current codebase passes:

```text
ruff check .
mypy src/chemworld
pytest
mkdocs build --strict
```

At the time of this document, the local test suite contains 44 tests covering
the environment, foundation checks, baselines, CLI, replay verification,
metrics, reproducibility, validation, anonymization, and suite/leaderboard
flows.

## Current Limitations

The platform is intentionally not a real reaction predictor, molecular
simulator, DFT wrapper, process simulator, or robot-lab controller. The current
model is qualitative and benchmark-oriented. It aims to be physically
plausible enough for closed-loop decision research and teaching, not to model
one named real chemical system.

The current release has one shared world law with reaction and
phase/separation modules. Future work should add more physical modules under
`ChemWorld` only after the benchmark protocol, private evaluation workflow,
and baseline reporting are stable.

## Recommended Next Steps

Near-term engineering work:

- add signed private-eval result manifests;
- add stronger baseline calibration tables;
- add richer explanation schemas and scoring rubrics;
- add paper-artifact scripts for reproducible tables;
- calibrate the mechanism-explanation rubric with expert examples.

Near-term research work:

- compare human, BO, LLM replay, and human-plus-LLM strategies;
- study public-test to private-eval generalization;
- analyze safety-aware exploration behavior;
- analyze whether mechanism explanations correlate with optimization quality.


