# repeat-01 / C-W01-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T10:26:43.753343+00:00; available public operations: 0; reviewed through: None.

# Working hypotheses

## H1 [tentative]
Catalyst C1 and solvent S2 are initial leads: the dossier suggests high reaction activity for C1 and low solubility/high growth/low occlusion for S2. A complete charge (0.040 mol reagent, 0.005 mol catalyst, 0.080 L solvent) heated moderately then cooled slowly with a modest seed dose should exceed the 0.10 recovery feasibility target while retaining purity >=0.80 and fines <=0.50.

**Pre-experiment prediction:** Batch 1 using C1/S2, reaction near 350 K, slow cooling toward 278 K, and 0.5 g seed will form assayable crystals with purity above the constraint and fewer fines than an unseeded or faster-cooled counterpart.

## H2 [tentative]
Within a productive chemistry, slower cooling and a post-seed growth hold should trade longer time for larger particles/fewer fines. Excessive seed may reduce seed-excluded yield or produce many counted fines; reheating after nucleation may selectively dissolve fines but could reduce recovery.

Decision plan: first establish reaction/crystallization feasibility, then vary catalyst/solvent and thermal/seed history. Treat instrument differences smaller than their stated noise as unresolved unless supported by larger contrasts or repeats.

## Revision 2

Recorded: 2026-10-14T10:28:27.381269+00:00; available public operations: 48; reviewed through: runner-operation-0048.

# Working hypotheses

## H1 [supported only for solvent S2 / 350 K screen]
Solvent S2 gives high-purity feasible crystals across catalysts. Contrary to the nominal activity prior, C0 is the leading catalyst in this screen: batch 2 gave crystal yield 0.416, purity 0.983, fines 0.394, and size index 0.110 (final assay event runner-operation-0024). C1 and C3 had similar recovery (~0.411-0.417) but smaller/noisier particles or higher degradation (runner-operation-0012, runner-operation-0048); C2 was materially worse in recovery at 0.323 (runner-operation-0036). Single batches and coupled assay noise leave the small C0/C1/C3 ordering unresolved, but C2 is deprioritized.

**Prediction before solvent screen:** holding C0 and the thermal history fixed, S2 should remain best for recovery and fines because its dossier indicates low solubility/nucleation and high growth; S0 is expected to worsen fines/occlusion, while S1 may improve reaction but retain more product in solution.

## H2 [tentative]
Slower/deeper cooling and post-seed growth should reduce fines and may improve recovery. The initial seeded S2 conditions already satisfy purity/fines constraints. A deeper 250 K endpoint is expected to raise recovery but could increase nucleation/fines; a longer moderate cool may raise size with less fines penalty.

## Revision 3

Recorded: 2026-10-14T10:30:38.484352+00:00; available public operations: 144; reviewed through: runner-operation-0144.

# Final source-stage hypotheses and decision

## H1 [supported in the tested domain]
C0/S2 is the best feasible material pairing tested. The solvent screen strongly separated particle quality: S0, S1 and S3 produced fines fractions 0.872, 0.689 and 0.801 under the baseline history (runner-operation-0060, -0072, -0084), whereas C0/S2 gave 0.394 with recovery 0.416 (runner-operation-0024). Thus S2's nominal low-nucleation/high-growth prior is directionally supported. Catalyst C2 is inferior here; small differences among C0/C1/C3 are less certain, but C0 was carried forward based on reaction and CSD balance.

## H2 [supported for C0/S2]
Deeper cooling to 250 K increased feasible recovery from 0.416 at 278 K to 0.482 at 250 K (runner-operation-0024 versus -0108). Extending the 250 K cooling/growth period from 7200 to 14400 s left recovery essentially unchanged within assay noise (0.482 to 0.483) but reduced fines from 0.450 to 0.285 and increased size/CSD quality (runner-operation-0108 versus -0120). This supports continued growth/aging rather than early stopping when particle quality matters.

## H3 [unresolved seed-dose effect]
At the long/deep C0/S2 condition, lowering seed from 0.05 g to 0.01 g gave numerically lower recovery (0.474 vs 0.483) but better fines/CSD (0.264/0.742 vs 0.285/0.712; runner-operation-0132 versus -0120). The recovery difference is comparable to single-assay uncertainty and is not evidence of a yield penalty without replication. A future repeat should compare these doses.

## Boundary / rejected high-upside alternative
S0 improved reaction/product and crystal recovery: the final long/deep low-seed S0 batch reached recovery 0.526 and purity 0.987, but fines remained 0.685, violating the required <=0.50 constraint (runner-operation-0144). It is therefore not recommendable despite the higher recovery; thermal/seed changes did not rescue its CSD enough.

## Final decision
Recommend lifecycle batch 10. It has the highest observed feasible crystal recovery (0.483) among completed batches, with purity 0.979 and fines 0.285 comfortably satisfying constraints (runner-operation-0120). Batch 11 is a viable quality-focused alternative but has lower observed recovery; batch 12 is excluded for fines.
