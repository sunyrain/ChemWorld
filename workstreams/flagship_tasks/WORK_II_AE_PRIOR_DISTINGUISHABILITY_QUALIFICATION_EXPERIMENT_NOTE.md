# Work II A-E prior-distinguishability qualification

Status: frozen before execution; provider-free; participant outcomes forbidden.

## Question

Before any formal participant run, do the exact two descriptor rows transposed between the aligned and
misindexed A-E priors produce a registered, observable metric-vector difference that exceeds paired
observation noise in two independent recipe regions and is reachable within the eight-experiment cell
budget?

## Units and coverage

- Five frozen A-E tasks × their five frozen public-formal worlds.
- Two frozen background regions per task-world (`0.25` and `0.75` on every non-target recipe
  coordinate).
- In each region, execute both transposed target categories with three paired keyed-noise replicates.
- Total planned denominator: 25 task-worlds, 50 regions, 150 paired replicates and 300 provider-free
  evaluator executions. No participant artifact or participant outcome is read.

## Measurements and frozen decisions

- Read the registered metric vector from each campaign checkpoint contract.
- Per region calculate mean normalized L1 vector separation, maximum single-metric separation and
  paired-noise SNR, with the exact formulas and thresholds in
  `configs/benchmark/work_ii_formal_design_v0.1.json`.
- Require finite bounded metrics, committed execution and exact replay for every unit.
- A region passes all metric-vector/noise checks; a world requires both regions and at most four
  distinct category-region recipes, which is within the frozen eight-round and six-unique-recipe
  resource contract. Every world and every task must pass.

Any missing metric, execution/replay failure, denominator drift, stale binding or failed region is
retained and fails closed. Threshold relaxation, task deletion and result-directed replacement are
forbidden; a failure requires redesign and refreeze of the complete A-E block.

## Outputs

- A self-hashed machine-readable qualification report with exact denominators and all failures.
- A concise Markdown summary generated from that report.
- Per-execution trajectories and replay receipts under the explicitly selected output directory.

