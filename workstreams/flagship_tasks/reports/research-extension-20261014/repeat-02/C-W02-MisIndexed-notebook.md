# repeat-02 / C-W02-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T17:37:35.024663+00:00; available public operations: 0; reviewed through: None.

# Initial hypotheses

H1 [tentative] Solvent S2 should favor low-occlusion growth and lower solubility, so with deliberate seeding and slow cooling it should give purer, larger crystals and better recovery than S0; the nominal dossier may be misindexed. Test first with catalyst C1, moderate reaction temperature, then seeded slow cooling.

H2 [tentative] Excessively fast/deep cooling will increase nucleation and fines; a warm seed point followed by slow staged cooling and a growth hold should reduce fines, though possibly at some recovery cost.

H3 [tentative] Catalyst C1 is the best starting reaction catalyst based on nominal activity. HPLC conversion/selectivity will be used selectively to distinguish upstream reaction limitations from crystallization limitations.

Decision rule: prioritize batches satisfying purity >=0.80 and fines <=0.50, then maximize crystal_yield; revise solvent/catalyst and thermal history when measurements contradict these expectations.

## Revision 2

Recorded: 2026-10-13T17:39:06.673513+00:00; available public operations: 16; reviewed through: runner-operation-0016.

# Working hypotheses after batch 1

H1 [partly supported, narrow scope] S2/C1 at 350 K produced full conversion and high final crystal purity (~0.992), with crystallization recovery ~0.471 (events runner-operation-0007, -0016). Thus S2 is promising for recovery/purity, although catalyst/selectivity is not yet optimized.

H2 [supported qualitatively for problem diagnosis] A 0.05 g seed followed by quench and cooling to 270 K generated overwhelmingly fine particles (particle and final assays at runner-operation-0011 and -0016; fines ~1, size index ~0.04). Long low-temperature holding/continued same-temperature crystallization did not provide evidence of enough coarsening because no fresh intermediate particle assay was taken; final result remained poor.

H4 [tentative] The abrupt post-reaction quench/deep cooling likely triggers excessive secondary nucleation. Prediction: substantially higher seed loading introduced before quench, plus staged/shallow cooling, should reduce fines; if fines remain near 1, solvent choice or a dissolution/reheat cycle is required.

Decision: preserve S2/C1 reaction initially, vary seed timing/dose and thermal history before changing chemistry. Quality feasibility requires fines <=0.50; batch 1 fails despite high purity/recovery.

## Revision 3

Recorded: 2026-10-13T17:40:21.725391+00:00; available public operations: 82; reviewed through: runner-operation-0082.

# Working hypotheses after batch 5

H1 [supported in tested scope] S2/C1 reliably gives high crystal purity (~0.98-1.00) and recovery around 0.45-0.47 across batches 1, 2, 4, and 5.

H2 [supported] The abrupt quench, not simply final temperature or seeding, is the principal observed fines driver. Quenched S2 batches ended with fines ~1 (events runner-operation-0016, -0039, -0066), whereas batch 5 omitted quench and used slow staged cooling 350→330→320→310→300→290 K, achieving fines ~0.394 at comparable recovery ~0.461 and purity ~0.983 (runner-operation-0082). This is a large difference, though thermal history includes longer staging and cannot isolate quench alone.

H3 [unresolved] Reheat/redissolution after a quenched nucleation event did not rescue fines in batch 4, suggesting initial nucleation history may be hard to reverse under tested 300 K reheat.

Prediction: extending the successful no-quench staged trajectory to 280 or 270 K should improve recovery while keeping fines below 0.50 if nucleation remains controlled. If fines cross 0.50, select the warmer endpoint or add finer temperature increments.

## Revision 4

Recorded: 2026-10-13T17:41:40.566351+00:00; available public operations: 140; reviewed through: runner-operation-0140.

# Working hypotheses after batch 8

H1 [supported in tested scope] At 0.04 mol reagent in 0.075 L S2, no-quench 10 K staged cooling preserves acceptable fines while deeper endpoints improve recovery: batch 5 (290 K) recovery ~0.461/fines ~0.394; batch 6 (270 K) ~0.507/~0.402; batch 7 (250 K) ~0.534/~0.371 (events -0082, -0100, -0120). Differences include assay noise, but the monotonic recovery trend is consistent and all meet purity/fines constraints.

H2 [supported, concentration boundary] Raising loading concentration by reducing S2 volume from 0.075 to 0.040 L increased recovery numerically to ~0.546 but caused fines ~0.987 (batch 8, runner-operation-0140), so that batch fails quality. Slow staged cooling alone cannot suppress nucleation at this high concentration.

Prediction: an intermediate S2 volume around 0.065 L may retain the recovery advantage without crossing fines 0.50. A result near or above 0.50 fines would favor returning to 0.075 L as the robust setting.

## Revision 5

Recorded: 2026-10-13T17:43:46.323581+00:00; available public operations: 219; reviewed through: runner-operation-0219.

# Final source-stage conclusions

H1 [supported in tested scope] The most important controllable quality lever was avoiding abrupt quench and using slow staged cooling. For S2/C1, no-quench 10 K stages from 350 K down to 250 K consistently produced acceptable purity/fines in batches 7, 10, and 12 (final assays runner-operation-0120, -0180, -0219), whereas quenched histories produced fines near 1.

H2 [supported with boundary] Concentration has a sharp fines penalty. At 0.04 mol reagent, 0.075 L S2 gave recovery ~0.534 with fines ~0.371 in batch 7; 0.070 L gave ~0.532/~0.310 in batch 10; 0.065 L gave ~0.532/~0.537 and failed; 0.040 L gave ~0.546/~0.987 and failed. The nonmonotone noisy fines values mean the exact boundary is unresolved, but 0.070-0.075 L is the demonstrated feasible region.

H3 [supported] Catalyst identity changes both upstream target loading and apparent crystallization behavior. C2 at otherwise similar 0.070 L conditions gave much lower recovery (~0.371) than C1 (~0.532) while having very low fines (batch 11 versus 10); C1 is preferred for the stated recovery objective.

Final decision: recommend completed batch 7 because it has the highest observed crystal_yield (~0.5335) among batches satisfying purity >=0.80 and fines <=0.50; purity ~0.9857 and fines ~0.3707 provide margin. Batches 10 and 12 independently support the same C1/S2/no-quench staged-cooling process family, though their recoveries were slightly lower (~0.5317 and ~0.5246). A future change would be warranted if replicate uncertainty showed batch 10's lower fines and comparable recovery more robust than batch 7.
