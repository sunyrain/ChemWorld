# ChemWorld-Bench

ChemWorld-Bench is a replayable Gymnasium environment for studying closed-loop decision
making in virtual chemical experiments. Agents act under partial observability, finite
experimental budgets, operational-risk limits, and measurement costs.

## Quick start

```bash
python -m pip install -e ".[dev]"
chemworld run --task reaction-to-assay --agent random --seed 0
chemworld verify --constitution --submission runs/<trajectory>.jsonl
chemworld evaluate --submission runs/<trajectory>.jsonl
```

The evaluator replays trajectories and recomputes metrics rather than trusting a submitted
score. Fifteen task slices share World Law v0.4 and versioned task, scenario, mechanism,
observation, scoring, and replay contracts.

## Evidence status

ChemWorld is an operational research environment and a benchmark candidate, not a validated
leaderboard. After an unconstrained GP diagnostic exposed safety regressions, Safe-GP was
repaired on development worlds and frozen before an untouched 240-run confirmation over four
tasks, three methods, and twenty paired seeds. All trajectories passed a second independent
replay. Safe-GP passed every safety and cost rule and improved the objective on every task,
but its flow effect (0.018752) missed the pre-registered SESOI (0.020000). The complete joint
rule therefore failed and does not support a method claim.

A single-seed SAC development run completed exactly 100,000 training steps, but its 80k
checkpoint outperformed the 100k checkpoint and therefore requires pooled multi-seed selection.
All six research tasks now expose executable, calibrated mechanism or constitutive-law families;
agent identification and transfer have not been measured. Operation-level Pro/Flash adapters and
a causally isolated assigned-versus-masked spectrum condition pass offline controls, but no real
provider trajectories exist. Multi-seed RL, live-LLM evaluation, mechanism adaptation, independent
reference search, salted private evaluation, and independent reproduction remain open.

## Documentation map

| Goal | Documentation |
| --- | --- |
| Install and run | [Getting Started](../getting_started.md) |
| Select tasks | [Tasks](../tasks.md), [Task Cards](../task_cards.md) |
| Build an agent | [Agent Interface](../agent_interface.md), [Operations](../operations.md) |
| Run a comparison | [Benchmark Protocol](../benchmark_protocol.md), [Baselines](../baseline_reference.md) |
| Understand the system | [Architecture](../architecture.md), [World Law](../world_law.md) |
| Audit evidence | [Scientific Status](../benchmark_release.md), [Release Integrity](../release_integrity.md) |
| Interpret boundaries | [Model Maturity](../model_maturity.md), [Limitations](../limitations.md) |

## Scope

ChemWorld is not a real-reaction predictor, commercial process simulator, laboratory
controller, or safety system. Explicit provider routes and `proxy_allowed=false` describe
software routing; they do not establish real-world predictive accuracy or industrial
validation.
