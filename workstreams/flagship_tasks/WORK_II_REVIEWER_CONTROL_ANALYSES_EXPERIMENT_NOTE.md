# Work II reviewer control analyses

Status: frozen before derived-data generation; provider-free reviewer follow-up.

## Question and units

This block asks whether the reported executable-law loss is attributable to the participant rather
than the typed-law interface, and whether the W2-50 law--action result survives continuous and
threshold-sensitive analysis. It reuses exactly the 135 current-composite evaluator cells and the 45
scheduled W2-50 cells (42 eligible, three retained failures). It creates no participant, provider, or
physical-experiment observations and does not change either historical denominator.

## Measurements

- W2-50: cell-level Pearson and Spearman associations of final-law normalized MAE with normalized
  regret and selected rank, pooled and task-stratified; task/world-cluster bootstrap intervals; and
  the adequate-law/correct-action table at frozen thresholds 0.05, 0.075, 0.10, 0.15, 0.20, 0.25,
  and 0.30.
- Schema capacity: for every final prediction query and metric, fit the best legal identity-link law
  using the registered feature coordinates and the existing typed-law bases. Report full-schema,
  participant-term-matched, and leave-one-query-out errors against the participant's final explicit
  predictions and evaluator truth. Validate every fitted law through the production law parser and
  executor.
- Decompose observed prediction-to-law loss into participant distillation gap and residual
  same-schema representation gap. Same-coordinate fits are explicitly in-domain capacity controls,
  not claims of global mechanistic recovery.

## Fixed analysis and failure rules

- Only cells already eligible under their original block enter action correlations. The three W2-50
  failures remain in the scheduled denominator and are never imputed.
- Bootstrap resamples the frozen task/world cluster, retaining all eligible arms in that cluster;
  10,000 resamples and seed 20260827 are fixed before analysis.
- Schema bases, query coordinates, target predictions, truth, bounds, and participant term budgets
  are read from preserved artifacts. Outcome values never select cells, thresholds, tasks, or bases.
- A fitted law counts as executable only if the production parser accepts it and its predictions
  reproduce the independently computed design-matrix predictions within 1e-10. All failures and
  exact denominators are emitted. No unfavorable result is replaced.

## Expected outputs

A machine-readable summary with all 42 eligible W2-50 rows, all 135 schema-capacity rows, exact
denominators and failures; a concise Chinese report; and plot-ready derived data for manuscript
integration.
