# repeat-02 / C-W04-Aligned — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T11:11:18.258633+00:00; available public operations: 0; reviewed through: None.

# Hypotheses

**H1 [tentative]** Solvent S2 should favor recovery of relatively large, pure crystals because its dossier indicates low solubility, high growth, low nucleation and low occlusion. S1 is a conservative comparator; S0 may give more fines and occlusion.

**H2 [tentative]** Catalyst C1 at near-maximum loading and a hot reaction hold should give robust conversion, but C3 may be superior in this fixed world despite the nominal prior. Initial test: C1/S2, 0.04 mol reagent, 0.005 mol catalyst, react near 360 K, then cool slowly with modest seed and hold cold. A particle measurement before filtration should show fines <=0.50 if the growth prior is useful.

**Decision rule (prospective):** First establish a feasible recipe, then vary catalyst/solvent and thermal/seeding history. Prefer the highest final crystal_yield among batches meeting purity >=0.80 and fines <=0.50; apparent differences comparable to stated assay noise will remain unresolved without corroboration.

## Revision 2

Recorded: 2026-10-14T11:13:11.964033+00:00; available public operations: 50; reviewed through: runner-operation-0050.

# Hypotheses

**H1 [supported for crystallization shape, scope: S2]** Low seed (0.005 g per 0.04 mol charge) with a 14,400 s cool gives much fewer fines than 0.020 g seed despite recipe confounds: batch 2 fines 0.340 versus batch 1 0.515, with purity 0.982 versus 0.988. Batch 2 therefore establishes feasibility (yield 0.400, purity and fines in specification). The seed effect is not isolated because cooling profile and catalyst also differed. Test C1 with the low-seed profile.

**H2 [supported in tested conditions]** S2 reliably yields very high crystal purity (0.982-1.000 in batches 1-4); crystallization purity is not currently limiting.

**H3 [tentative catalyst ranking]** C2 is disfavored at 345 K (batch 3 final reaction yield 0.420, crystal yield 0.337). C0 at 360 K and C3 at 345 K gave similar crystal yield near 0.400 (batches 2 and 4); C1 at 360 K had higher 0.416 but excess fines under its high-seed history (batch 1). Because temperatures and profiles differ, catalyst main effects remain partly confounded. Next test C1 at lower temperature/longer time with the low-seed S2 process; improved selectivity without incomplete conversion would support moving below 360 K.

**Decision:** Continue prioritizing seed 0.005 g and long cooling. A result with final conversion near 1 and lower byproduct/degradation at lower reaction temperature would justify further temperature optimization.

## Revision 3

Recorded: 2026-10-14T11:14:04.829438+00:00; available public operations: 86; reviewed through: runner-operation-0086.

# Hypotheses

**H1 [supported in tested S2 process]** Low seed (0.005 g) plus a 14,400 s cool to 270-275 K consistently controls fines: batches 2, 3, 6, and 7 gave 0.330-0.376, while batch 4 was marginal at 0.489. The high-seed batch 1 failed fines at 0.515. Catalyst remains a possible modifier.

**H2 [supported]** S2 gives high final crystal purity (>=0.976 in all completed batches), so reaction yield and recovery dominate optimization.

**H3 [supported over 330-400 K for C1/S2, but optimum unresolved]** Raising reaction temperature while shortening the hold strongly improved selectivity and crystal recovery: batch 5 (330 K, 7200 s) crystal yield 0.287; batch 6 (380 K, 1800 s) 0.567; batch 7 (400 K, 1200 s) 0.633. Corresponding final selectivity rose from 0.371 to 0.629 to 0.673, while degradation warning fell. This contradicts the prior concern that lower temperature would suppress degradation in this world.

**Prediction before batch 8:** C1/S2 at 420 K for about 900 s should continue the observed trend if the optimum lies above 400 K, giving crystal yield above batch 7 while retaining purity >=0.80 and fines <=0.50. A lower yield or increased degradation would bracket the temperature optimum near 400 K.

**Decision:** Use remaining batches to bracket the high-temperature optimum and then refine crystallization recovery around the best reaction condition.

## Revision 4

Recorded: 2026-10-14T11:14:55.479286+00:00; available public operations: 122; reviewed through: runner-operation-0122.

# Hypotheses

**H1 [supported in tested S2 process]** Seed 0.005 g and cooling to 270-275 K controls fines when substantial crystallization occurs. Batch 8 at 420 K reaction gave the current best qualified recovery: crystal yield 0.673, purity 0.986, fines 0.354.

**H2 [supported]** C1/S2 reaction selectivity increases strongly from 330 through 440 K under shorter high-temperature holds; liquid-phase yield reached about 0.77 at 440 K (batches 9-10).

**H3 [new, supported by replication]** A sharp crystallization/recovery cliff occurs after the 440 K reaction: batches 9 and 10 both produced crystal yield near 0.008-0.009 despite high liquid reaction yield, very low fines, and large-particle indices. Changing final cooling target from 265 to 270 K did not restore recovery. Therefore the loss is associated with the upstream 440 K history rather than simply the 265 K endpoint. Possible alternatives are a noncrystallizing product state or an unobserved solubility/history change; liquid HPLC alone cannot distinguish them.

**Prediction before batch 11:** An intermediate reaction at 430 K/750 s should test the boundary. Recovery near batch 8 would place the cliff above 430 K; recovery near batches 9-10 would place it at or below 430 K.

**Decision:** Do not recommend 440 K despite superior reaction assay. Bracket the transition and reserve the final batch for confirmation/refinement near the best safe side.

## Revision 5

Recorded: 2026-10-14T11:15:46.309097+00:00; available public operations: 146; reviewed through: runner-operation-0146.

# Final hypotheses and decision

**H1 [supported in this campaign]** The best qualified region is C1/S2 with a short high-temperature reaction at 420-430 K, 0.005 g seed per 0.04 mol charge, and slow/long cooling to 270 K. Batches 8, 11, and 12 all gave crystal yield about 0.673-0.678, purity 0.986-1.000, and fines 0.354-0.385 (events runner-operation-0098, -0133, -0146).

**H2 [supported, sharp boundary]** Raising the reaction history to 440 K increased liquid reaction yield but reproducibly destroyed crystal recovery: batches 9 and 10 had crystal yield only 0.0079 and 0.0090 (events runner-operation-0110, -0122). The 430 K batch restored 0.675 recovery, placing the cliff between the tested 430 and 440 K conditions. Mechanistic cause remains unresolved.

**H3 [supported with confounding noted]** Low seed/long cooling controls fines relative to the initial high-seed history. Batch 1 (0.020 g seed) had fines 0.515, whereas qualified low-seed batches were mostly 0.33-0.39. Catalyst, temperature, and cooling differences prevent attributing the entire contrast to seed alone.

**H4 [unresolved]** Extending the 270 K hold from 14,400 s to 28,800 s may improve size (batch 12 size index 0.105 versus batch 11 0.083), but the yield difference 0.678 versus 0.675 is smaller than final-assay crystal-yield noise and is not evidence of a recovery effect without replication.

**Final decision:** Recommend completed batch 12 because it has the highest observed qualified crystal_yield (0.678), purity 1.000, fines 0.385, and a somewhat larger measured size than batch 11. Batch 11 is essentially tied on recovery and is the shorter process; this recommendation would change if repeatability favored batch 11 or if throughput/time were weighted materially.
