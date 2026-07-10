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
`chemworld-physical-chemistry-v0.2`, with versioned task, scenario, mechanism,
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
Every benchmark claim must preserve the task maturity metadata. Runtime
crystallization, continuous-flow PFR, and extraction/wash are professional
candidates in their stated domains; remaining bounded fallbacks such as drying,
concentration, and transfer stay explicitly labeled as proxies.
