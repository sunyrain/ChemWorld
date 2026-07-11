# ChemWorld-Bench

ChemWorld-Bench is a replayable Gymnasium environment for studying how agents plan,
measure, and adapt across virtual chemical experiments. It exposes one versioned
interaction contract across classical optimization, active learning, reinforcement
learning, LLM tool agents, and human learners.

ChemWorld is not a reaction predictor, process simulator, laboratory controller, or
safety system. Its outputs are properties of a controlled virtual world.

## Start in five minutes

ChemWorld supports Python 3.11 and 3.12.

```bash
git clone https://github.com/sunyrain/ChemWorld.git
cd ChemWorld
python -m pip install -e ".[dev]"
```

Run and independently verify a complete trajectory:

```bash
chemworld tasks list
chemworld run --task reaction-to-assay --agent random --seed 0
chemworld verify --constitution --submission runs/<trajectory>.jsonl
chemworld evaluate --submission runs/<trajectory>.jsonl
```

`chemworld evaluate` replays the trajectory and recomputes metrics. It does not trust a
score supplied by the agent.

## Use the environment

```python
import gymnasium as gym
import chemworld

env = gym.make("ChemWorld", task_id="reaction-to-assay", seed=0)
observation, info = env.reset(seed=0)

action = {"operation": "add_reagent", "amount_mol": 0.01}
check = env.unwrapped.validate_action(action)
if check["valid"]:
    observation, reward, terminated, truncated, info = env.step(action)

env.close()
```

Unmeasured array values are `NaN` (`null` in JSONL). Read `observed_mask` or
`observed_keys` before using an observation field.

## Visual interfaces

```bash
python -m apps.task_lab.server --port 8876
```

- Agent Observatory: <http://127.0.0.1:8876/agent/>
- Student Lab: <http://127.0.0.1:8876/student/>

Classical agents work offline. Online model credentials are read only from process
environment variables and must not be committed or included in evaluation artifacts.

## Current evidence status

The runtime, task contracts, resource accounting, trajectory replay, score binding, and
public evaluation controls are operational. The complete benchmark is not yet validated.

A fresh-cohort 160-run comparison evaluated structured GP optimization against random
search over four core research tasks (20 paired seeds, 40 experiments per run). Every
trajectory replayed successfully. All objective and cost non-inferiority rules passed,
but safety non-inferiority failed in flow, crystallization, and distillation. The complete
pre-registered joint rule therefore failed and does not support a method claim or leaderboard.

RL training results, live-LLM comparisons, mechanism-family generalization, a searched
reference portfolio, salted private evaluation, and independent reproduction remain
open evidence gates. See the [scientific status](https://sunyrain.github.io/ChemWorld/benchmark_release/)
and [limitations](https://sunyrain.github.io/ChemWorld/limitations/) before citing results.

## Documentation map

| Goal | Documentation |
| --- | --- |
| Install and run an episode | [Getting started](https://sunyrain.github.io/ChemWorld/getting_started/) |
| Choose a task | [Task catalogue](https://sunyrain.github.io/ChemWorld/tasks/) |
| Build an agent | [Agent interface](https://sunyrain.github.io/ChemWorld/agent_interface/) |
| Run a fair comparison | [Benchmark protocol](https://sunyrain.github.io/ChemWorld/benchmark_protocol/) |
| Inspect the architecture | [Architecture](https://sunyrain.github.io/ChemWorld/architecture/) |
| Use the visual lab | [Task Lab](https://sunyrain.github.io/ChemWorld/interactive_task_lab/) |
| Interpret evidence | [Scientific status](https://sunyrain.github.io/ChemWorld/benchmark_release/) |

## Quality gates

Install the complete development surface and run the release checks:

```bash
python -m pip install -e ".[dev,docs,physchem-ref]"
python scripts/run_release_gate.py
```

The standard gate verifies formatting, typing, tests, documentation, wheel resources,
runtime integration, replay, and reference-backed physical-chemistry slices. Passing it
establishes software integrity; it does not by itself authorize a scientific benchmark
claim.
