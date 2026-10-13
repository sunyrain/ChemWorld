# repeat-01 / C-W02-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T16:52:44.098844+00:00; available public operations: 0; reviewed through: None.

# Working hypotheses

**H1 [tentative]** Within the nominal dossier scope, solvent S2 should give the best purity and coarse-particle outcome because it combines low impurity occlusion and nucleation with high growth; its lower solubility may also improve crystallization recovery. S3 is the fallback if S2 sacrifices reaction performance.

**H2 [tentative]** Catalyst C1 is the reaction-screening lead from nominal activity, while C2/C3 remain plausible due to fixed-world residuals.

**Pre-specified first test.** Use a high reagent/catalyst loading in S2, drive reaction hot, then seed and cool slowly with a cold hold before filtration. Expect purity >=0.80 and fines <=0.50; recovery may exceed the 0.10 feasibility target. If reaction conversion is poor, screen catalyst/solvent before refining thermal history; if fines are excessive, reduce seed dose and slow/interrupt cooling.

## Revision 2

Recorded: 2026-10-13T16:54:01.650535+00:00; available public operations: 47; reviewed through: runner-operation-0047.

# Working hypotheses

**H1 [supported in tested scope]** S2 with deep cooling produces high-purity crystals meeting both quality constraints. Final assays 1–4 all gave purity about 0.99–1.00 and fines 0.32–0.47 (events runner-operation-0013, -0024, -0035, -0047).

**H2 [unresolved]** A small seed dose near 0.001 g appears preferable to 0.01 g for particle quality: batch 2 had lower fines and larger size than batch 1, but cooling temperature/duration also changed, so causality is confounded. Near-zero seed in batch 3 did not clearly improve recovery and reduced measured size relative to batch 2.

**H3 [tentative]** A long cold hold after slow cooling may raise recovery: batch 4 measured 0.526 versus about 0.511 in batches 2–3. This numerical difference is modest relative to single-assay uncertainty and lacks replication. Test by varying thermal history and later replicate the strongest recipe.

**Reaction scope.** C1/S2 at 390 K reaches essentially full conversion but only ~0.57 selectivity with a degradation warning near 0.23; since crystallization recovery is conditional on pre-separation target, current priority remains crystal recovery and quality unless upstream changes materially affect purity.

## Revision 3

Recorded: 2026-10-13T16:56:00.364662+00:00; available public operations: 147; reviewed through: runner-operation-0147.

# Final source-stage hypotheses and decision

**H1 [supported in tested scope]** Solvent S2, a small 0.001 g seed dose, slow cooling to 250 K over 14,400 s, and a 14,400 s cold hold robustly produced high-purity, low-fines crystals at moderate concentration. Across the 0.02–0.04 L solvent tests, purity stayed about 0.99 and fines were 0.21–0.29 (events runner-operation-0100, -0112, -0124, -0136).

**H2 [supported qualitatively]** Cooling rate controls fines strongly. Rapid cooling followed by a cold hold gave recovery 0.534 but fines 0.785 (runner-operation-0073); a reheat/recool cycle did not rescue that population (fines 0.753, runner-operation-0088). Slow cooling is therefore required within this recipe family.

**H3 [narrowed]** Concentrating from 0.08 L to 0.04 L improved the observed combination of recovery and particle quality (batch 8 versus earlier batches), but a monotonic concentration–recovery effect is not established: 0.02–0.04 L recoveries were close and assay/process variation is visible. At 0.01 L, recovery remained high (0.554) but fines reached 1.0, failing the constraint (runner-operation-0147). Thus the useful concentration window is bounded away from 0.01 L.

**Replication/confound.** The exact 0.04 L recipe gave recovery 0.553 in batch 8 and 0.536 in batch 11; both met quality constraints, so the numerical recovery difference should not be treated as a proven recipe effect. Batch 8 remains the completed run with the highest measured feasible recovery.

**Decision.** Recommend lifecycle batch 8: measured crystal recovery 0.553, purity 0.989, fines 0.275 (runner-operation-0100). Batch 12 had marginally higher measured recovery but is ineligible because fines were 1.0. Future work would replicate batches 8/11 and map 0.035–0.05 L before claiming a precise optimum.
