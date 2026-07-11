# ChemWorld-Bench

ChemWorld-Bench is a research-grade benchmark for closed-loop virtual chemical
experimentation. The official environment, `ChemWorld`, asks agents to operate
inside one shared physical-chemical world law: reaction kinetics, phase
partition, downstream separation, noisy instruments, cost, safety, and
finite-budget decision making. It is built on a Chemical World Model foundation:
event-driven operations, transition kernels, instrument measurements, state
ledgers, and executable physical constitution checks.

The project is intentionally not a real reaction predictor and not a robot lab
controller. It studies local world-model learning and experimental decision
making in constrained virtual chemical environments.

## Install

```bash
python -m pip install -e ".[dev]"
```

If `python` is a Windows app alias, install a real Python 3.11+ interpreter and
make sure it appears first on `PATH`.

For release and scientific-reference validation, install the complete gate
dependencies and run the release command:

```bash
python -m pip install -e ".[dev,docs,physchem-ref]"
python scripts/run_release_gate.py
```

## Quick Start

```python
import gymnasium as gym
import chemworld

env = gym.make(
    "ChemWorld",
    task_id="reaction-optimization-standard",
    seed=42,
)

obs, info = env.reset()
action = env.action_space.sample()
obs, reward, terminated, truncated, info = env.step(action)
```

Run an official baseline:

```bash
chemworld run --env ChemWorld --agent random --budget 30 --seed 42
chemworld verify --submission runs/random_ChemWorld_public-dev_balanced_seed42.jsonl
chemworld evaluate --submission runs/random_ChemWorld_public-dev_balanced_seed42.jsonl
chemworld leaderboard --results results/*.json
chemworld suite --agent gp_bo --world-splits public-test private-eval --seeds 0 1 2
chemworld tasks readiness
chemworld baselines report --preset serious --output-dir runs/serious_baselines
python scripts/check_frozen_benchmark.py

chemworld inspect-constitution --env ChemWorld
chemworld run --task reaction-to-assay --agent random
chemworld run --task reaction-to-purification --agent scripted_chemistry
chemworld verify --constitution --submission runs/random_ChemWorld_public-dev_balanced_seed42.jsonl
```

`chemworld run` writes both a trajectory JSONL file and a submission manifest
with the agent metadata, dependency versions, platform, source digest, and
reproducible command. If the package is inside a real git repository, the
manifest also records the current commit hash.

Start the local Agent progress and student-feedback interface:

```bash
python -m apps.task_lab.server --port 8876
```

Open `/agent/` for the Agent Observatory or `/student/` for the Student Lab. The
student experience works offline. Agent evaluations support DeepSeek V4 Pro plus
random recipe, Latin hypercube, local search, GP-PI, GP-UCB, GP-EI, RF-EI, and
safety-constrained GP active-learning backends. Extended 1–4× campaign
budgets are kept separate from official scores, and every result is replay verified
under `runs/task_lab/`. See `apps/task_lab/README.md` for secure key setup, commands,
and score semantics.

Material actions retain stable numeric protocol values while the public interfaces show
semantic solvent and catalyst labels. Named solvents identify real components, but the
current reaction-task effects remain calibrated benchmark categories; anonymous
catalysts are never presented as real formulations. See `docs/material_identity.md`.

## Architecture

- `chemworld.world`: operation, scenario, observation, scoring, and world-law contracts.
- `chemworld.runtime`: transactional kernels and domain-service orchestration.
- `chemworld.physchem`: local physical-chemistry kernels for properties,
  EOS, equilibrium, reactors, separations, transport, spectroscopy, and
  thermochemistry.
- `chemworld.foundation`: ontology, units, state ledger, constitution checks,
  transition/observation kernel protocols, surrogate interfaces.
- `chemworld.envs`: Gymnasium environments and registration.
- `chemworld.tasks`: task contracts over the shared world law.
- `chemworld.agents`: baseline agents and LLM adapter interfaces.
- `chemworld.eval`: runners, metrics, leaderboard aggregation.
- `chemworld.data`: trajectory schema, logging, anonymization utilities.

See `docs/architecture.md` and `docs/benchmark_protocol.md` for the research
protocol. The current candidate status and remaining release gates are described in
`docs/benchmark_release.md`.

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

The published documentation is available at
<https://sunyrain.github.io/ChemWorld/>. See `docs/getting_started.md` for the
first-run guide, `docs/demos.md` for examples, and `docs/model_maturity.md` for
the scientific validity boundaries.

Collaborative development follows a mandatory [claim-before-work](claims/README.md)
protocol. Active claims are checked by the local release gate.
