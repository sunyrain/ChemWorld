# repeat-03 / C-W02-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T18:02:37.123372+00:00; available public operations: 0; reviewed through: None.

# Initial hypotheses

H1 [tentative] Solvent S2 should favor larger, purer crystals because its nominal growth is high and impurity occlusion/nucleation are low; its lower solubility may also raise crystallization recovery. Slow cooling, moderate seeding, and a cold hold should reduce fines relative to rapid unseeded cooling.

H2 [tentative] Catalyst C1 is the best initial reaction choice from nominal activity, but C2/C3 remain plausible because fixed-world residuals are hidden. Initial screens will compare reaction conversion/selectivity and downstream recovery.

Prediction before batch 1: C1/S2, full reagent charge, warm reaction, controlled slow cooling with seed and cold hold will clear purity 0.80 and fines 0.50; if recovery is low, extend/cool growth rather than infer catalyst failure.

## Revision 2

Recorded: 2026-10-13T18:05:30.470263+00:00; available public operations: 168; reviewed through: runner-operation-0168.

# Final source-stage hypotheses

H1 [supported in tested scope] Solvent/thermal history strongly controls crystallization quality. With four direct 250 K growth stages, S2/C0 gave recovery 0.579 and fines 0.351 (runner-operation-0092), while S1/C1 gave recovery 0.586 and fines 0.483 (runner-operation-0120). S3 and S0 under the same direct-cooling pattern failed the fines constraint (0.633 and 0.761; runner-operation-0106 and runner-operation-0134). These are process-level comparisons and catalyst/upstream differences remain a possible confound where not matched.

H2 [supported in this scope] Staged slow cooling (320→300→280→260→250 K, 14,400 s per stage) with C0/S1 and 0.05 g seed sharply improved the observed size distribution while retaining high recovery: batch 11 measured recovery 0.618, purity 0.991, fines 0.218 (runner-operation-0149). This supports staged supersaturation generation over direct quenching for S1. A matched C0/S1 direct-cooling experiment was not run, so the magnitude attributable solely to staging is unresolved.

H3 [unresolved incremental benefit] Four additional 250 K growth stages in batch 12 produced recovery 0.621, purity 0.992, fines 0.226 (runner-operation-0168), versus batch 11 recovery 0.618. The 0.003 recovery difference is smaller than the stated single-assay noise scale (0.01), so extra cold residence is not established as a true recovery gain. Both recipes comfortably meet purity and fines constraints; batch 12 has the highest observed recovery.

H4 [supported] Seed dose affected size more clearly than recovery in the matched C1/S2 direct-cooling pair: 0.05 g seed gave recovery 0.504 and size 0.112 (runner-operation-0024), versus 0.01 g recovery 0.503 and size 0.072 (runner-operation-0036). The recovery difference is negligible at assay resolution; the size difference is suggestive but lacks replication.

Decision: recommend batch 12 because it has the campaign-high observed seed-excluded recovery and wide quality-constraint margins. Batch 11 is the shorter near-equivalent alternative; I would switch to it if cycle time is valued or replicate data fail to confirm the small batch-12 recovery advantage.
