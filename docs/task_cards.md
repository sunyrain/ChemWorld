# Task Cards

Task cards are the release-facing benchmark contract for each registered task.
They are generated from `TaskSpec`, scenario cards, runtime profiles, and
maturity metadata so CLI output, docs, and leaderboard artifacts do not drift.

Inspect a card:

```bash
chemworld tasks card reaction-optimization-standard
```

Each card contains:

- task id, motivation, difficulty, and recommended use;
- shared `world_law_id` and scenario id;
- allowed operations and instruments;
- budget, episode mode, seed policy, and termination policy;
- online reward and leaderboard metric definitions;
- success metrics and safety limit;
- scenario card and split;
- kernel maturity, physics maturity, and proxy policy;
- reference baseline slots and recommended agent families;
- known failure modes.

## Current Registry Matrix

This table is a compact snapshot. The authoritative version is always the CLI
card generated from the registry.

| Task | Split | Mode | Budget | Maturity | Proxy | Scenario |
| --- | --- | --- | ---: | --- | --- | --- |
| `electrochemical-conversion` | `public-test` | `campaign` | 48 | `lite` | `false` | `electrochemical-conversion` |
| `flow-reaction-optimization` | `public-test` | `campaign` | 60 | `proxy` | `true` | `flow-reaction-optimization` |
| `low-budget-characterization` | `public-test` | `campaign` | 18 | `lite` | `false` | `low-budget-characterization` |
| `partition-discovery` | `public-test` | `campaign` | 48 | `proxy` | `true` | `partition-discovery` |
| `public-private-generalization` | `private-eval` | `campaign` | 72 | `lite` | `false` | `generalization` |
| `purity-yield-tradeoff` | `public-test` | `campaign` | 90 | `proxy` | `true` | `purity-yield-tradeoff` |
| `reaction-mechanism-explanation` | `public-test` | `campaign` | 36 | `lite` | `false` | `reaction-mechanism` |
| `reaction-optimization-standard` | `public-test` | `campaign` | 72 | `lite` | `false` | `reaction-optimization` |
| `reaction-safety-constrained` | `public-test` | `campaign` | 72 | `lite` | `false` | `reaction-safety` |
| `reaction-to-assay` | `public-dev` | `single_experiment` | 18 | `lite` | `false` | `reaction-to-assay` |
| `reaction-to-crystallization` | `public-test` | `single_experiment` | 72 | `proxy` | `true` | `reaction-to-crystallization` |
| `reaction-to-distillation` | `public-test` | `single_experiment` | 72 | `lite` | `false` | `reaction-to-distillation` |
| `reaction-to-purification` | `public-test` | `single_experiment` | 90 | `proxy` | `true` | `reaction-to-purification` |
| `tool-agent-planning` | `public-dev` | `single_experiment` | 48 | `proxy` | `true` | `tool-agent-planning` |

## Baseline Rows

Task cards contain baseline reference slots. Public release tables should be
filled by:

```bash
chemworld baselines report \
  --tasks reaction-optimization-standard reaction-to-distillation \
  --agents random scripted_chemistry gp_bo safe_gp_bo \
  --seeds 0 1 2 \
  --output-dir runs/baseline_report
```

The generated baseline artifact, not a hand-written table, is the source of
truth for release numbers.

## Release Rule

A task should not be treated as release-ready until it has:

- fixed public seeds and documented private-eval policy;
- a generated task card checked into the paper artifact;
- reference baseline rows for the relevant agent families;
- replay-verified trajectories for official baseline runs;
- maturity metadata in task cards, trajectories, baseline rows, and submission
  summaries;
- known failure modes and intended use.
