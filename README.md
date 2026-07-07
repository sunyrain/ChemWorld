# ChemWorld-Bench

ChemWorld-Bench is a research-grade benchmark for closed-loop virtual chemical
experimentation. The first environment, `BatchReactorWorld`, asks agents to
optimize a hidden semi-mechanistic batch reactor under a finite experiment
budget, noisy observations, cost, and safety constraints. It is built on a
Chemical World Model foundation: event-driven operations, ODE dynamics,
instrument measurements, state ledgers, and executable physical constitution
checks.

The project is intentionally not a real reaction predictor and not a robot lab
controller. It studies local world-model learning and experimental decision
making in constrained virtual chemical environments.

## Install

```bash
python -m pip install -e ".[dev]"
```

If `python` is a Windows app alias, install a real Python 3.11+ interpreter and
make sure it appears first on `PATH`.

## Quick Start

```python
import gymnasium as gym
import chemworld

env = gym.make(
    "BatchReactorWorld",
    world_split="public-dev",
    budget=30,
    objective="balanced",
    seed=42,
)

obs, info = env.reset()
action = env.action_space.sample()
obs, reward, terminated, truncated, info = env.step(action)
```

Run an official baseline:

```bash
chemworld run --env BatchReactorWorld --agent random --budget 30 --seed 42
chemworld verify --submission runs/random_BatchReactorWorld_public-dev_balanced_seed42.jsonl
chemworld evaluate --submission runs/random_BatchReactorWorld_public-dev_balanced_seed42.jsonl
chemworld leaderboard --results results/*.json
chemworld suite --agent gp_bo --world-splits public-test private-eval --seeds 0 1 2

chemworld inspect-constitution --env BatchReactorWorld
chemworld run --env BatchReactorWorld --agent random --budget 12
chemworld verify --constitution --submission runs/random_BatchReactorWorld_public-dev_balanced_seed42.jsonl
```

`chemworld run` writes both a trajectory JSONL file and a submission manifest
with the agent metadata, dependency versions, platform, source digest, and
reproducible command. If the package is inside a real git repository, the
manifest also records the current commit hash.

## Architecture

- `chemworld.core`: semi-mechanistic reactor worlds, objectives, action specs.
- `chemworld.foundation`: ontology, units, state ledger, constitution checks,
  transition/observation kernel protocols, surrogate interfaces.
- `chemworld.envs`: Gymnasium environments and registration.
- `chemworld.agents`: baseline agents and LLM adapter interfaces.
- `chemworld.eval`: runners, metrics, leaderboard aggregation.
- `chemworld.data`: trajectory schema, logging, anonymization utilities.

See `docs/architecture.md` and `docs/benchmark_protocol.md` for the research
protocol.

Observations are partial by design. Unmeasured quantities are represented as
`NaN` in Gym arrays and `null` in trajectory JSONL, with `observed_mask` and
`observed_keys` recording what an agent actually observed. Official leaderboard
metrics use `leaderboard_score` from final-assay events rather than intermediate
instrument feedback.

## Examples

```bash
python examples/demo_manual_event_sequence.py
python examples/demo_compare_baselines.py
python examples/demo_verify_and_inspect.py
```

Notebook walkthrough:

```bash
python -m pip install -e ".[dev,notebooks]"
jupyter notebook notebooks/full_workflow_demo.ipynb
jupyter notebook notebooks/physics_sanity_check.ipynb
jupyter notebook notebooks/tutorials/day_01_enter_virtual_lab.ipynb
```

See `docs/current_progress.md` for the current platform status and
`docs/demos.md` for demo details.
