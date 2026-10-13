# C-24 — model-authored source notebook

Development replication. Each version is the model's scientific account, not verified environment truth. Posttest answers are separate in the JSON record.

## Revision 1

Recorded: 2026-10-13T04:51:21.147661+00:00; public operations available: 0; reviewed through: not specified.

# Pre-campaign hypotheses

H1 [tentative] Solvent S2 should favor high recovery and larger, cleaner crystals because its nominal solubility and nucleation are low while growth is high; S1 is a plausible purity/robustness comparator. This prior could fail because world-specific residuals may dominate.

H2 [tentative] A high upstream loading with catalyst C1 or C3, followed by cooling, modest seeding, and sufficient cold growth/hold should exceed the 0.10 recovery target. Slower cooling and a warm-to-cold staged history should reduce fines versus an abrupt crash, though possibly at some recovery cost.

Initial test: use full reagent loading in S2 with a moderate catalyst dose, react hot, then compare seeded staged cooling against later unseeded/fast and dose variants. I will revise if assay evidence contradicts this ordering.

---

## Revision 2

Recorded: 2026-10-13T04:53:07.629637+00:00; public operations available: 73; reviewed through: runner-operation-0073.

# Working hypotheses after batches 1–5

H1 [supported in this scope] Solvent S2 supports high crystallization purity (~0.98–1.00) and recovery around 0.38–0.42 under tested C1 reaction conditions (final assays, events runner-operation-0015 and subsequent batch-final events through batch 5). This is crystallization-stage recovery, not overall reaction yield.

H2 [supported but confounded] Extending/staging cooling and the cold hold sharply reduced fines versus batch 1 (about 0.64 to about 0.51–0.53) and increased CSD quality. Because duration, staging, seed dose, and particle history changed together, the causal contribution of each remains unresolved. Batch-to-batch differences among seed 0, 0.005, and 0.05 g are small relative to the broad protocol change and do not yet establish a monotonic seed effect.

H3 [tentative] Fines near the 0.50 limit may be reduced by lower nucleation solvent S1/S2 choices, lower agitation, longer warm growth, or a reheat/recool anneal. Prediction: an annealed or more growth-favoring history should raise size/CSD and lower fines without sacrificing purity; a result above ~0.55 fines would count against that specific recipe, while recognizing assay noise.

Decision: screen solvent/catalyst and thermal-history factors, then replicate the best quality-constrained recipe. Upstream selectivity is only ~0.50 for C1/S2 at 380 K, so catalyst/temperature screening could improve overall score but the recommendation remains governed first by recovery, purity, and fines.

---

## Revision 3

Recorded: 2026-10-13T04:55:26.821576+00:00; public operations available: 258; reviewed through: runner-operation-0258.

# Working hypotheses after batches 1–16

H1 [supported in tested scope] S2 is the best solvent tested for the fines constraint. S1, S0, and S3 gave substantially higher fines (approximately 0.86, 0.71, and 0.62 respectively in batches 6–8) despite good purity; this is consistent with, but not proof of, the nominal low nucleation/high growth prior for S2.

H2 [supported in tested scope] Thermal history dominates fines control. A very slow multistage descent plus prolonged cold growth produced quality-constrained outcomes: batch 13 fines ~0.483 and batch 15 ~0.499, whereas stopping warmer at 300 K (batch 14) gave ~0.739 fines. Batch 16's reheat/recool cycle also met the constraint (~0.473) but recovery was lower (~0.387), so annealing is not yet preferable.

H3 [tentative] Continued growth at low temperature trades time for lower fines and can preserve or raise recovery. Batch 15 at 250 K gave the highest constrained recovery so far (~0.444) but is borderline on fines relative to assay noise (reported std 0.018); batch 13 is more robust on fines but lower recovery (~0.384). Prediction before replication: repeating or extending the batch-15 cold hold should keep recovery near or above 0.42 and move fines below 0.50 often enough to support selection; failure in repeats would indicate the apparent advantage is noise or uncontrolled process variability.

Catalyst comparisons at a shared recipe showed no compelling improvement over C1 for the constrained objective; C0 raised recovery numerically but missed fines, and C2/C3 did not improve recovery. Final selection will prioritize measured recovery among batches meeting purity >=0.80 and fines <=0.50, with preference for replication and margin from the fines boundary.

---

## Revision 4

Recorded: 2026-10-13T04:57:43.561772+00:00; public operations available: 425; reviewed through: runner-operation-0425.

# Final source-stage interpretation (24 batches)

H1 [supported in this campaign] Solvent S2 with deep, multistage cooling is the most reliable tested route to the joint purity/fines region. Material screens in batches 6–11 and warm stopping in batch 14 produced clearly worse fines than the best S2 cold-growth histories.

H2 [supported, scope-limited] Continuing growth to 250 K after staged cooling can meet the fines constraint with high recovery, but replicate scatter is material: batch 17 achieved recovery 0.456, purity 1.000, fines 0.459 (runner-operation-0278), while nominally similar batch 24 measured fines 0.519 (runner-operation-0425). Thus a point estimate near 0.50 is not a robust guarantee; process variability/noise remains unresolved.

H3 [supported for one tested condition; needs replication] Raising the reaction temperature to 410 K before the same S2 staged cold-growth sequence produced a large fines reduction in batch 23 (0.140), high CSD quality (0.796), purity 0.999, and recovery 0.429 (runner-operation-0406). The contrast with 350 K (batch 22, fines ~0.999) is too large to ignore, but each temperature was tested once and upstream degradation increased at 410 K. This suggests upstream state strongly affects later nucleation, not merely reaction yield.

H4 [unresolved tradeoff] Anneal/recool histories can pass the constraint. Batch 21 has the highest measured recovery among passing batches (0.459) with purity 0.991 and fines 0.498 (runner-operation-0367), but it is borderline given assay noise; batch 17 has nearly equal recovery and a larger fines margin. Batch 23 is the most robust fines result but sacrifices recovery.

Decision: recommend batch 21 because the authoritative goal is maximum measured crystallization-stage recovery subject to pointwise purity >=0.80 and fines <=0.50. Operationally, batch 17 is the more conservative robustness alternative, and batch 23 is the low-fines alternative. I would change the recommendation if replicate evidence showed batch 21's true fines exceed 0.50 or if robust constraint satisfaction rather than measured-point feasibility were required.

---
