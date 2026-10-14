# repeat-03 / C-W04-Opaque — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T12:04:40.111258+00:00; available public operations: 0; reviewed through: None.

# Working hypotheses

## H1 [tentative; pre-experiment]
Catalyst and solvent identities will materially affect target formation, so an initial material screen should precede thermal-history optimization. I expect hotter reaction holds to raise conversion but very long/hot exposure may increase byproduct or degradation.

## H2 [tentative; pre-experiment]
For a productive reaction, seeded slow cooling followed by a cold hold should improve recovery and reduce fines versus abrupt unseeded cooling. A moderate seed dose should mainly control nucleation; because reported recovery excludes seed, excessive seed is not intrinsically beneficial.

**Planned falsification:** use early batches to screen catalyst/solvent combinations under a common reaction and crystallization protocol, then perturb cooling/hold and loading around the best feasible condition. I will prioritize assay-qualified recovery (purity >=0.80, fines <=0.50), not the native composite score.

## Revision 2

Recorded: 2026-10-14T12:08:07.633558+00:00; available public operations: 111; reviewed through: runner-operation-0111.

# Working hypotheses

## H1 [supported in screened scope]
Material identity matters, but solvent choice has had the clearest particle-quality consequence under the common 360 K reaction and seeded cooling protocol. S0 batches remained extremely fine (final-assay fines 0.945–1.00 in events runner-operation-0015, -0028, -0046, -0059). With C1 and otherwise comparable crystallization, S1, S2, and S3 reduced fines to 0.588, 0.504, and 0.696 respectively (runner-operation-0072, -0085, -0098). These are numerical contrasts with multiple simultaneous solvent-specific reaction/solubility effects; they do not isolate mechanism.

## H2 [supported in S2/C1 scope]
Stopping seeded S2 crystallization warmer improved particle acceptability without a clear recovery penalty: 290 K gave crystal yield 0.413, purity 0.981, and fines 0.471 (runner-operation-0111), versus 285 K yield 0.414, purity 1.000, and fines 0.504 (runner-operation-0085). The fines shift exceeds either instrument's stated single-measurement noise scale, but repeatability is not yet established. Prediction: 288–290 K should remain near the fines limit and may maximize qualified recovery.

## H3 [revised / unresolved]
The initial general claim that more seeding and longer/cycled growth necessarily reduce fines is not supported. S0 remained fine across seed doses and a prolonged thermal cycle (runner-operation-0015 through -0059), and extended 295 K processing in batch 3 did not improve the final distribution (runner-operation-0046). Solvent-dependent nucleation/solubility is an alternative explanation. I will now optimize near S2/C1 and treat fines <=0.50 as the binding stopping criterion.

**Decision:** batch 8 is the first assay-qualified result. Remaining batches will test a slightly colder stop, catalyst choice, and seed/thermal-history robustness; I will retain batch 8 unless another completed batch has higher recovery while meeting both constraints.

## Revision 3

Recorded: 2026-10-14T12:09:17.812623+00:00; available public operations: 162; reviewed through: runner-operation-0162.

# Final source-stage notebook

## H1 [supported in tested scope]
S2 with C1 and a 288–290 K stopping window produced the only robust cluster of assay-qualified outcomes. Batches 8, 10, and 11 all met purity >=0.80 and fines <=0.50 (runner-operation-0111, -0137, -0150), with seed-excluded crystal recoveries 0.413, 0.410, and 0.396. Batch 9 with C0 also just met the constraints but had lower recovery, 0.390 (runner-operation-0124). Thus C1 is preferred over C0 in S2 under this protocol, while the exact size of that catalyst effect remains confounded by batch variation.

## H2 [supported, bounded]
The final crystallization stop is a binding trade-off. At 285 K with C1/S2, recovery was 0.414 but fines were 0.504, narrowly failing (runner-operation-0085). At 288–290 K, recoveries were similar within assay noise while fines were 0.471–0.496 in three qualified batches (runner-operation-0111, -0137, -0150). This supports stopping near 290 K rather than continuing colder growth. Exact temperature ranking is unresolved because recovery differences are on the order of the reported assay noise and exact 290 K replication differed numerically.

## H3 [rejected in tested form]
Lowering the reaction temperature to 350 K while extending the hold to 5400 s did not preserve recovery: batch 12 gave recovery 0.320 with higher byproduct/degradation signals, despite acceptable purity and fines (runner-operation-0162). The combined temperature-duration perturbation is confounded, so it does not isolate a temperature effect; nevertheless this recipe is not preferred.

## Final decision
Select lifecycle batch 8 (runner-operation-0111): crystal yield 0.413, purity 0.981, fines 0.471. It has the highest observed recovery among batches that satisfy both explicit quality constraints. Batch 6 had a numerically similar recovery (0.414) but failed the fines constraint, and later qualified repeats did not exceed batch 8.
