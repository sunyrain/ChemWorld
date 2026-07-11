# ChemWorld-Bench

ChemWorld-Bench is a mechanism-driven, replayable benchmark for closed-loop
virtual chemical experimentation. Agents operate a shared physical-chemical
world through Gymnasium under partial observability, finite budgets, safety
constraints, and measurement costs.

## Quick Start

```bash
python -m pip install -e ".[dev]"
```

```python
import gymnasium as gym
import chemworld

env = gym.make("ChemWorld", task_id="reaction-to-assay", seed=0)
observation, info = env.reset(seed=0)
```

The current release contains 15 task slices under
`chemworld-physical-chemistry-v0.4`, with versioned task, scenario, mechanism,
observation, scoring, trajectory, and replay contracts.

## Documentation Map

| Goal | Documentation |
| --- | --- |
| Install and run an episode | [Getting Started](../getting_started.md) |
| Select and evaluate tasks | [Tasks](../tasks.md), [Task Cards](../task_cards.md), [Benchmark Protocol](../benchmark_protocol.md) |
| Build an agent | [Agent Interface](../agent_interface.md), [Operations](../operations.md), [Wrappers](../wrappers.md) |
| Understand the system | [Architecture](../architecture.md), [World Law](../world_law.md), [Physchem Models](../physchem_core_design.md) |
| Reproduce a release | [Validation](../validation.md), [Submission](../submission.md), [Release Integrity](../release_integrity.md) |
| Interpret scientific limits | [Model Maturity](../model_maturity.md), [Limitations](../limitations.md) |

## Scope

ChemWorld is not a real reaction predictor, commercial process simulator, DFT
wrapper, or robot controller. It is a controllable virtual research environment.
Every benchmark claim must preserve task maturity metadata. World Law v0.4 has
no formal runtime fallback route: drying, vacuum concentration, transfer, LLE,
crystallization, flow, and distillation execute explicit bounded providers. This
does not make them real-chemistry predictors. The v0.4 bundle is a backend
candidate and contains no publishable method ranking yet.
