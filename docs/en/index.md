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
leaderboard. The latest frozen classical diagnostic contains 160 replay-verified runs over
four tasks, two methods, and twenty paired seeds. Structured GP passed the objective-only rule
on all four tasks, but had a higher observed risk-budget exceedance rate on three tasks. The
protocol had not pre-registered safety and cost non-inferiority margins, so the run does not
support a complete method claim.

Full-budget RL, paired live-LLM evaluation, mechanism-family generalization, independent
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
