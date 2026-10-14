# repeat-02 / C-W01-Aligned — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T11:20:30.299174+00:00; available public operations: 0; reviewed through: None.

# Initial hypotheses

H1 [tentative] Solvent S2 should favor recovery of relatively large, low-occlusion crystals because its nominal solubility and nucleation are low while growth is high; S1 is a purity-oriented comparator. This prior may be wrong or misindexed.

H2 [tentative] Catalyst C1 or C3 at moderate loading and elevated reaction temperature should provide useful conversion without excessive degradation; the first batch will test C1/S2.

Prediction before batch 1: a 0.04 mol reagent charge in 0.08 L S2, 0.005 mol C1, heated near 360 K then slowly cooled with modest seed and held, should exceed 0.10 seed-excluded recovery and meet fines <=0.50; purity is uncertain. If reaction conversion is poor, extend/higher-temperature reaction or change catalyst; if purity/fines fail despite conversion, adjust solvent and thermal history.

## Revision 2

Recorded: 2026-10-14T11:23:14.090615+00:00; available public operations: 94; reviewed through: runner-operation-0094.

# Working hypotheses after batches 1–9

H1 [supported in tested scope] S2 supports high-purity crystal recovery. Across completed batches, all S2 recipes produced purity well above 0.80. Catalyst/thermal choices altered upstream target yield, so S2 alone is not sufficient for maximum recovery.

H2 [supported in tested scope] C0 is the strongest tested catalyst for recovery near 355–365 K. Batch 4 (C0, 365 K, 0.08 L) reached crystal yield about 0.516, exceeding C1/C2/C3 comparators (events runner-operation-0014, -0024, -0034, -0044). Because catalyst and temperature were not fully factorial, interaction remains possible.

H3 [supported with a boundary] Increasing concentration by reducing S2 from 0.08 to 0.04 L increased crystal yield to about 0.552 while meeting purity and fines constraints (runner-operation-0084). Further reduction to 0.03 L did not improve yield materially and caused fines fraction to saturate at 1.0 (runner-operation-0094); thus the usable concentration window has a sharp morphology boundary between 0.03 and 0.04 L for the tested seed/cooling schedule.

H4 [tentative] Lower crystallization endpoint increases recovery: 0.06 L at 250 K and 0.08 L at 258 K outperformed warmer related runs, but these comparisons are confounded by concentration, catalyst, and reaction history. Test around 0.04 L while changing seed/thermal history.

Decision: retain C0/S2, 0.04 mol reagent, 0.04 L solvent, 0.005 mol catalyst, reaction near 355 K for 3600 s as the current base. Optimize morphology/recovery near the 0.04 L concentration boundary; abandon 0.03 L unless reheating or slower staged cooling demonstrably suppresses fines.

## Revision 3

Recorded: 2026-10-14T11:24:14.684522+00:00; available public operations: 127; reviewed through: runner-operation-0127.

# Final source-stage interpretation

H1 [supported in tested scope] S2 with C0 is the best material pair tested for feasible recovery. C0 outperformed the other catalysts in the explored S2 recipes, though catalyst-by-solvent interactions remain untested.

H2 [supported with a sharp scope boundary] At 0.04 mol reagent, reducing S2 volume from 0.08 toward 0.04 L improved recovery while preserving purity and fines. At 0.03 L, final recovery remained near 0.55 but fines reached 1.0 (runner-operation-0094), so concentration cannot be extrapolated monotonically below 0.04 L.

H3 [supported in this schedule] Batch 8 is the highest observed feasible recovery: crystal_yield 0.5521, purity 0.9848, fines 0.3770 (runner-operation-0084). Its recipe used 0.04 L S2, 0.04 mol reagent, 0.005 mol C0, 355 K for 3600 s, 0.05 g seed, direct 14400 s cooling to 250 K, filtration.

H4 [not supported] More elaborate thermal histories did not improve the base recipe. Staged cooling (batch 10), partial reheat/recool (batch 11), and an additional 14400 s cold continuation (batch 12) gave lower observed recovery and/or worse fines (runner-operation-0105, -0117, -0127). These are numerical differences from single batches, not established causal effects; run-to-run variability is not separately quantified.

Final decision: recommend completed batch 8. It maximizes observed recovery among batches satisfying purity >=0.80 and fines <=0.50. Batch 9 had similar recovery but is infeasible because fines were 1.0. The recommendation would change if replication showed batch 8's recovery advantage was noise, or if a narrowly intermediate solvent volume between 0.03 and 0.04 L met the fines limit with higher recovery.
