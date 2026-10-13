# repeat-02 / C-W03-Opaque — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T11:46:02.103888+00:00; available public operations: 0; reviewed through: None.

# Pre-experiment hypotheses

H1 [tentative] Reaction performance will depend strongly on anonymous catalyst/solvent and temperature; a broad first-pass screen across identities is more valuable than early replication.

H2 [tentative] For crystallization, moderate seed loading plus slow cooling and a cold hold should improve recovery while limiting fines; excessively rapid/deep cooling may increase recovery but worsen fines.

Prediction for batch 1: a maximum legal reagent charge with catalyst C0 in S0, heated near 360 K, then seeded and slowly cooled to about 278 K will produce detectable crystals and may reach the initial 0.10 recovery target. I will revise identity and thermal choices from assays; evidence is initially absent.

## Revision 2

Recorded: 2026-10-13T11:47:55.172760+00:00; available public operations: 67; reviewed through: runner-operation-0067.

# Working hypotheses after five batches

H1 [supported in tested recipe] Solvent identity strongly controls crystallization morphology. Under C0, 360 K/1 h, 0.005 g seed and staged 320→300→278 K cooling plus cold hold, S2 gave the best observed recovery (0.476) with purity 1.00 and fines 0.281 (event runner-operation-0053). S1 also met constraints (recovery 0.445, fines 0.393; runner-operation-0039), whereas S0 and S3 had fines near 0.7 (runner-operation-0025, runner-operation-0067). Numerical differences are much larger than stated assay noise, but recipes are unreplicated.

H2 [unresolved] Staging/holding may enlarge crystals relative to direct cooling, but batch 1 vs 2 changed seed dose and therefore is confounded; do not attribute the size difference solely to thermal history.

H3 [testable] Within S2, deeper final cooling should raise seed-excluded recovery; the fines margin (0.281 vs limit 0.50) may permit cooling below 278 K. I will test 260 K and 250 K while retaining slow staged cooling, then vary seed dose/hold to recover morphology if fines rise.

Decision: prioritize S2 for recovery optimization. Catalyst identity and reaction temperature remain secondary factors because crystal recovery is normalized to pre-separation target, though they may influence crystal purity or impurity occlusion.

## Revision 3

Recorded: 2026-10-13T11:49:43.450424+00:00; available public operations: 165; reviewed through: runner-operation-0165.

# Final source-stage hypotheses

H1 [supported in tested scope] S2 is the preferred crystallization solvent. Across the common C0/staged recipe it provided recoveries 0.476–0.537 with fines 0.219–0.281 and purity 0.981–1.00 (events runner-operation-0053, -0081, -0095, -0109, -0165). S1 was feasible but lower recovery (0.445; -0039); S0/S3 failed the fines constraint in tested recipes (-0025, -0067).

H2 [supported trend, not a fitted law] Deeper final cooling in S2 increased observed seed-excluded recovery without compromising fines: 278 K gave 0.476, 260 K 0.515, and 250 K 0.532 under otherwise closely related staged histories (-0053, -0081, -0095). Some intermediate stage durations/targets also changed, so exact temperature causality remains mildly confounded.

H3 [unresolved seed effect] Raising seed from 0.005 to 0.05 g at the 250 K recipe gave 0.537 recovery and 0.228 fines (-0109) versus 0.532 and 0.219 (-0095). These small differences are comparable to measurement/process variability; no strong seed-dose effect is claimed. The 0.05 g recipe is nevertheless operationally feasible and was replicated in batch 12: recovery 0.523, purity 0.996, fines 0.243 (-0165).

H4 [supported ranking in this recipe] C0 was the best tested catalyst for recovery. Under the common S2/250 K/0.05 g seed recipe, C1, C2, and C3 gave recoveries 0.524, 0.448, and 0.474 (-0123, -0137, -0151), versus C0 results 0.537 and 0.523 (-0109, -0165). C0 vs C1 is close; C2/C3 are clearly less attractive on observed recovery.

Final decision: recommend batch 8 because it has the highest observed compliant recovery (0.537), purity 0.981, and fines 0.228. Batch 12 independently supports the same recipe's feasibility, though the two recovery values show meaningful process/assay variability and do not establish batch 8 as deterministically superior.
