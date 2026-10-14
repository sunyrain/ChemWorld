# repeat-03 / C-W05-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T11:37:27.325838+00:00; available public operations: 0; reviewed through: None.

# Pre-experimental hypotheses

**H1 [tentative].** Solvent S2 should favor the specification because its nominal low solubility and nucleation tendency plus high growth imply stronger recovery with fewer/larger particles; S3 is the conservative alternative. This may be overturned by fixed-world residuals.

**H2 [tentative].** Catalyst C1 is the initial reaction-screen choice from nominal activity. At fixed charge, adequate hot residence should increase conversion, while excessive temperature/time may raise degradation. A first batch at moderate-high temperature will test feasibility.

**H3 [tentative].** Slow cooling, modest seeding, and a cold hold should reduce fines compared with unseeded/fast cooling. Particle sizing will be used selectively to distinguish thermal-history effects.

## Revision 2

Recorded: 2026-10-14T11:38:57.781268+00:00; available public operations: 51; reviewed through: runner-operation-0051.

# Working hypotheses after batches 1–5

**H1 [supported in tested scope].** S2 supports high-purity crystal recovery: all five S2 batches gave final purity about 0.98–1.00. Batch 2–5 slow 14,400 s cooling to 270 K also reduced fines to about 0.32–0.34, unlike batch 1's shorter cooling plus ambient-warming hold (fines 0.527). Thermal history is confounded with reaction conditions in batch 1, so the cooling interpretation remains provisional.

**H2 [supported for 360 K/1800 s, S2].** Catalyst C3 gave the highest observed final crystal yield (0.528, event runner-operation-0041) among C0/C1/C2/C3 under the matched recipe; C0 0.502, C1 0.484, C2 0.413. Single runs and assay noise mean modest C3–C0 differences are not yet repeatability evidence, but C3 is the optimization choice.

**H3 [revised].** 380 K/3600 s is unnecessarily severe: batch 1 had degradation warning 0.243 and lower final yield than moderate 360 K/1800 s batches. Moderate conditions retained near-complete conversion and improved selectivity. Next: screen solvent identity at fixed C3, then optimize seeding/cold endpoint around S2/C3.

## Revision 3

Recorded: 2026-10-14T11:40:07.238692+00:00; available public operations: 121; reviewed through: runner-operation-0121.

# Final source-stage synthesis

**H1 [supported in this campaign].** Solvent identity strongly affected the recovery–fines tradeoff at matched C3/360 K/1800 s/270 K cooling. S1 gave 0.605 crystal yield with fines 0.346 (runner-operation-0071), whereas S0 gave higher reaction yield but fines 0.755 and S3 fines 0.694 (runner-operation-0061, -0081). S2 was feasible but lower crystal recovery (best 0.528 in the matched catalyst screen, runner-operation-0041).

**H2 [supported in tested scope].** C3 was the best catalyst choice in the S2 matched screen; the C3–C0 margin is modest and unreplicated, but later S1/C3 runs repeatedly met purity and fines constraints.

**H3 [supported with uncertainty].** Lowering the S1 crystallization endpoint from 270 to 250 K increased observed recovery from roughly 0.60 to 0.62–0.63 while retaining fines below 0.50 (runner-operation-0101, -0111). Seed 0.01 versus 0.05 g did not show a resolved effect relative to assay/particle uncertainty. The 0.04 L concentrated batch reached 0.633 yield but fines 0.487 (runner-operation-0121), too close to the 0.50 limit given stated 0.018 assay noise.

**Decision.** Recommend batch 10 rather than batch 12: batch 10 has essentially the same recovery within measurement resolution (0.630 vs 0.633) but a more defensible fines margin (0.433 vs 0.487), with purity 0.981. This decision would change if replicated concentrated batches demonstrate underlying fines safely below 0.50 without sacrificing recovery.
