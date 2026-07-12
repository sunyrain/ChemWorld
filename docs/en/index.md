# ChemWorld-Bench

**Give an agent a virtual chemistry lab, a finite budget, and incomplete information—then inspect every decision it makes.**

ChemWorld-Bench is a replayable Gymnasium environment for closed-loop experimental decision making. RL, Bayesian
optimization, LLM tool agents, and student programs share the same tasks, actions, observations, budgets, and
evaluation contracts. Scores are recomputed from trajectories rather than trusted from submissions.

## Start here

| I want to… | Read |
| --- | --- |
| Run my first experiment | [Getting started](../getting_started.md) |
| Choose a task | [Task catalog](../tasks.md) |
| Build an agent | [Agent interface](../agent_interface.md) |
| Watch an agent or operate the lab | [Task Lab](../interactive_task_lab.md) |
| Compare methods fairly | [Benchmark protocol](../benchmark_protocol.md) |
| Understand current evidence | [Scientific status](../benchmark_release.md) |

## Five-minute run

```bash
python -m pip install -e ".[dev]"
chemworld run --task reaction-to-assay --agent random --seed 0
chemworld verify --constitution --submission runs/<trajectory>.jsonl
chemworld evaluate --submission runs/<trajectory>.jsonl
```

The run writes a trajectory and manifest under `runs/`. Verification checks the schema, versioned contracts,
physical constitution, and deterministic replay. Evaluation then recomputes the result from that trajectory.

## What the environment provides

- 15 task slices spanning reaction, separation, crystallization, flow, electrochemistry, and equilibrium;
- versioned task, scenario, mechanism, observation, scoring, and replay contracts;
- public action affordances and observation views for RL, BO, LLM, and human users;
- explicit operational-risk, cost, measurement, and experiment budgets;
- trajectory replay and score binding for reproducible evaluation.

## Evidence status

ChemWorld is an operational research environment and a **benchmark candidate**, not a validated leaderboard.
Software controls and replay infrastructure are available. Safe-GP and single-task SAC experiments provide useful
development evidence, while also exposing safety trade-offs and checkpoint-selection failures. Formal multi-method
RL/LLM evaluation, private-world generalization, and independent reproduction remain incomplete.

That distinction is intentional: the project is ready for agent development, teaching, protocol research, and
diagnostic experiments, but not yet for SOTA or real-chemistry claims.

## Scope

ChemWorld studies decisions inside a versioned virtual world. It is not a real-reaction predictor, commercial
process simulator, laboratory controller, or safety system. See [model maturity](../model_maturity.md) and
[limitations](../limitations.md) before interpreting physical results.
