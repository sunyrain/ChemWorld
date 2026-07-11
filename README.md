# ChemWorld-Bench

ChemWorld-Bench is a replayable environment for studying closed-loop decision
making in virtual chemical experiments. Agents choose operations, request
measurements, manage finite budgets, and improve later experiments from earlier
observations. The environment combines reaction, phase, separation, instrument,
cost, and safety models behind one versioned Gymnasium interface.

ChemWorld is a research environment, not a real-reaction predictor, process
design package, or laboratory controller. Numerical outputs describe the
versioned virtual world only.

## Install

ChemWorld requires Python 3.11 or newer.

```bash
git clone https://github.com/sunyrain/ChemWorld.git
cd ChemWorld
python -m pip install -e ".[dev]"
```

Install the documentation and scientific-reference dependencies when you need
the complete local quality gate:

```bash
python -m pip install -e ".[dev,docs,physchem-ref]"
```

## Run an episode

```python
import gymnasium as gym
import chemworld

env = gym.make(
    "ChemWorld",
    task_id="reaction-to-assay",
    seed=0,
)

observation, info = env.reset(seed=0)
observation, reward, terminated, truncated, info = env.step(
    {"operation": "add_reagent", "amount_mol": 0.01}
)
env.close()
```

Unmeasured array fields are `NaN`; their JSONL representation is `null`.
Always use `observed_mask` or `observed_keys` before consuming a field.

## Run and verify an agent

```bash
chemworld tasks list
chemworld run --task reaction-to-assay --agent random --seed 0
chemworld verify --constitution --submission runs/<trajectory>.jsonl
chemworld evaluate --submission runs/<trajectory>.jsonl
```

`chemworld run` writes a trajectory and a manifest containing the task and
environment contracts, agent metadata, dependencies, source digest, and a
reproducible command. Evaluation replays the trajectory instead of trusting a
submitted score.

## Choose an entry point

| Goal | Start here |
| --- | --- |
| Learn the API | [Getting started](https://sunyrain.github.io/ChemWorld/getting_started/) |
| Select a task | [Task catalogue](https://sunyrain.github.io/ChemWorld/tasks/) |
| Build an agent | [Agent interface](https://sunyrain.github.io/ChemWorld/agent_interface/) |
| Run the benchmark | [Evaluation protocol](https://sunyrain.github.io/ChemWorld/benchmark_protocol/) |
| Use the visual lab | [Task Lab](https://sunyrain.github.io/ChemWorld/interactive_task_lab/) |
| Interpret results | [Scientific status](https://sunyrain.github.io/ChemWorld/benchmark_release/) |

Start the local visual interface with:

```bash
python -m apps.task_lab.server --port 8876
```

Open <http://127.0.0.1:8876/agent/> for the Agent Observatory or
<http://127.0.0.1:8876/student/> for the Student Lab. Classical agents run
offline. Online model adapters require provider credentials supplied through
environment variables; credentials must never be committed to the repository.

## Scientific status

The runtime, contracts, replay chain, and local release checks are operational.
The six-task research suite remains a benchmark candidate: current evidence
supports a provisional four-task core, while confirmatory vNext runs, RL and
live-LLM comparisons, complete security checks, and independent reproduction
are still required before a validated leaderboard or state-of-the-art claim.

The public documentation distinguishes structural readiness from empirical
validity and lists supported, exploratory, and prohibited claims. See
[Benchmark status](https://sunyrain.github.io/ChemWorld/benchmark_release/) and
[Limitations](https://sunyrain.github.io/ChemWorld/limitations/) before citing
results.

## Local quality gate

```bash
python scripts/run_release_gate.py
```

The gate checks formatting, typing, tests, documentation, frozen contracts,
replay integrity, and reference-backed physical-chemistry slices.
