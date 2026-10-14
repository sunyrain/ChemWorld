# repeat-01 / C-W05-Opaque — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T10:53:09.117231+00:00; available public operations: 0; reviewed through: None.

# Initial hypotheses

H1 [tentative] Reaction performance will depend strongly on anonymous catalyst identity and temperature; a small factorial screen should identify a productive region. Prediction: at least one catalyst at elevated but sub-degradation temperature will exceed the 0.10 overall crystal-recovery feasibility target after cooling.

H2 [tentative] Slow cooling with moderate seed loading and a growth hold should reduce fines versus unseeded/rapid cooling, but excessive seed may inflate number-weighted fines. Prediction: 0.3–0.6 g seed with slow cooling will be more likely to meet fines <=0.50 than no seed or 1 g seed.

H3 [tentative] Solvent identity controls solubility and hence recovery/purity. Initial batches will screen solvent/catalyst combinations; later batches will refine thermal history and loading. Conclusions will remain provisional because final-assay noise and batch confounding are nonzero.

## Revision 2

Recorded: 2026-10-14T10:55:17.104695+00:00; available public operations: 56; reviewed through: runner-operation-0056.

# Working hypotheses after batch 4

H1 [supported in tested scope] C0 at 360 K for 3600 s gives high conversion and roughly 0.60 reaction yield in S0/S1. Final crystal purity has been >=0.985 in batches 1–4, so present limitation is morphology rather than purity.

H2 [revised] Seed/cooling effects are solvent-dependent. In S0, increasing seed to 0.05 g and using two 14400 s cooling stages numerically reduced fines from 0.861 (batch 1, event runner-operation-0013) to 0.583 (batch 2, runner-operation-0026), still outside spec. Delaying seed to 320 K and adding a 310 K reheat/recool did not improve S0 morphology (batch 3, runner-operation-0043); this route is shelved unless another solvent changes behavior.

H3 [supported, S1 versus S0 comparison] Switching only solvent from S0 to S1 under the batch-2 thermal recipe produced the first specification-meeting material: yield 0.510, purity 1.000, fines 0.368 (batch 4, runner-operation-0056), versus batch 2 yield 0.482 and fines 0.583. Difference exceeds the stated assay noise, though there is no replicate yet. Prediction: S1 will remain the preferred solvent unless S2/S3 improve recovery while retaining fines <=0.50.

Decision: screen S2/S3 with C0, then catalysts C1–C3 in the best solvent. Preserve the hot-seed, two-stage slow-cooling recipe as the morphology baseline.

## Revision 3

Recorded: 2026-10-14T10:57:19.547353+00:00; available public operations: 160; reviewed through: runner-operation-0160.

# Final source-stage hypotheses and decision

H1 [supported in this campaign scope] Solvent identity dominates the recovery/morphology tradeoff under the common C0, 360 K/3600 s reaction and hot-seeded two-stage cooling recipe. S1 gave the highest specification-compliant recovery observed: batch 4 yield 0.510, purity 1.000, fines 0.368 (runner-operation-0056). S2 further reduced fines to 0.260 but lowered recovery to 0.433 (batch 5, runner-operation-0069); S3 failed the fines constraint and had only 0.389 recovery (batch 6, runner-operation-0082).

H2 [supported for screened catalysts] With S1 and the common thermal recipe, C0 produced 0.510 recovery (batch 4). C1, C2, and C3 produced 0.495, 0.465, and 0.498 respectively (batches 7–9; runner-operation-0095, -0108, -0121). Differences between C0 and C3 are near assay uncertainty, so C0 is preferred on observed maximum rather than a definitive catalyst-effect claim.

H3 [supported tradeoff; threshold region unresolved] Increasing concentration by reducing S1 from 0.060 L to 0.050 or 0.040 L numerically raised recovery to 0.521–0.538 but increased fines beyond 0.50 (batches 10–12; runner-operation-0134, -0147, -0160). An extra 278 K growth stage in batch 12 did not restore compliance. Thus higher concentration is not recommended without finer solvent-volume or seeding/cooling optimization.

H4 [unresolved repeatability] Batch 4 was not exactly replicated; final-assay uncertainty is much smaller than its margins to the purity and fines limits, but broader process repeatability is unknown.

Decision: recommend completed batch 4 because it has the maximum observed crystal_yield among batches satisfying purity >=0.80 and fines <=0.50. Its recipe used 0.04 mol reagent, 0.06 L S1, 0.005 mol C0, 360 K for 3600 s, 0.05 g seed at the hot stage, 14400 s cooling to 300 K then 14400 s to 278 K, followed by filtration.
