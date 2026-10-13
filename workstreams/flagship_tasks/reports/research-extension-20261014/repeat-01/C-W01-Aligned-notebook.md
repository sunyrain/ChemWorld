# repeat-01 / C-W01-Aligned — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T11:07:46.087868+00:00; available public operations: 0; reviewed through: None.

# Working hypotheses

## H1 [tentative]
Solvent S2 should favor recovery of larger, purer crystals because its nominal solubility, nucleation, growth, and occlusion properties are favorable relative to the other solvents. A slow seeded cooling trajectory should reduce fines versus an unseeded or rapid cool. This prior will be rejected or narrowed if early final assays show low purity, high fines, or poor recovery.

## H2 [tentative]
Catalyst C1 is the safest initial reaction choice because of its high nominal activity with lower stated variability than C2/C3. Reaction conversion and selectivity may still be world-specific. Initial test: maximal allowed reagent/catalyst in 0.08 L S2, moderate-hot reaction, quench, seed near saturation, slow cool, hold, filter.

## Decision rule
Optimize crystal_yield only among batches satisfying purity >=0.80 and fines <=0.50. Use measured final assays as authoritative; use particle-size measurements to adapt thermal/seeding history, not as replacements for final assay.

## Revision 2

Recorded: 2026-10-13T11:09:40.920482+00:00; available public operations: 28; reviewed through: runner-operation-0028.

# Working hypotheses

## H1 [narrowed; unresolved]
S2 gives high crystal purity (~0.99) and recovery (~0.48) in batches 1–2, but both fail the fines constraint badly (final fines ~1.00; events runner-operation-0013 and -0028). Reducing seed from 0.05 g to 0.005 g and using three 14,400 s cooling stages increased measured size only modestly; it did not reduce fines. Thus seed dose and simple cooling duration alone are insufficient in this S2 scope. The next test changes solvent and adds a fines-dissolution reheat/recool cycle.

## H2 [supported only for conversion; selectivity poor]
C1 at 360 K for 3600 s gives complete conversion but only ~0.59 selectivity and ~0.18 degradation warning (events runner-operation-0006, -0013, -0028). Crystal purity nevertheless remains high after filtration, so reaction selectivity is not yet the binding quality constraint. Catalyst alternatives remain unresolved.

## H3 [tentative, prospective]
S1's lower nominal nucleation tendency and higher solubility than S2 may suppress formation of excessive nuclei. A controlled reheat after initial crystallization may preferentially dissolve fines, and slow recooling may transfer mass to survivors. Prediction for batch 3: fines should decrease materially relative to batches 1–2, though recovery may fall.

## Decision rule
Recommend the highest crystal_yield only among final assays with purity >=0.80 and fines <=0.50. If solvent change plus reheat does not approach the fines constraint, test lower supersaturation (less reagent or more soluble solvent S0/S3) and/or prolonged warm growth before final cooling.

## Revision 3

Recorded: 2026-10-13T11:10:35.405128+00:00; available public operations: 59; reviewed through: runner-operation-0059.

# Working hypotheses

## H1 [rejected in broad form]
The expectation that S2 plus slow cooling would itself control fines is rejected for deep cooling to 270 K. Batches 1, 2, and 4 all show final fines near 1 despite seeded/unseeded operation and long staged cooling (events runner-operation-0013, -0028, -0059). S1 with a mild reheat/recool also failed (runner-operation-0044). Purity is consistently excellent, so impurity occlusion is not the limiting mechanism.

## H2 [supported in tested conditions]
C3 at 350 K/2400 s gives lower degradation warning (~0.09) than C1 at 360 K/3600 s (~0.18), while preserving useful target yield and slightly better crystal recovery (batch 4 versus batches 1–2; runner-operation-0059). This numerical contrast is confounded by catalyst, temperature/time, and lack of seed, so the causal factor is unresolved; use the C3 recipe provisionally.

## H3 [tentative, prospective]
Deep cooling likely creates a late burst of secondary nucleation that dominates the number-weighted distribution. Stopping crystallization warm (around 300 K), after a long growth hold, should trade recovery for substantially lower fines. Batch 5 will test this directly without seed. If fines remain near 1, test low reactant loading / higher-solubility S3 to reduce supersaturation.

## Decision rule
Quality gates remain purity >=0.80 and fines <=0.50. Once feasibility is reached, increase recovery by lowering the stop temperature incrementally or by warm ripening rather than immediately returning to 270 K.

## Revision 4

Recorded: 2026-10-13T11:11:36.479674+00:00; available public operations: 103; reviewed through: runner-operation-0103.

# Working hypotheses

## H1 [rejected for S2]
Within tested S2 conditions, neither deep staged cooling, warm stopping at 300 K, three warm reheat/recool cycles, nor rapid cooling produces acceptable fines. Final fines remain ~0.99–1.00 (runner-operation-0013, -0028, -0059, -0071, -0091, -0103). Thermal cycling also reduced size. The likely dominant factor is solvent-specific nucleation/particle population rather than cooling time alone.

## H2 [provisionally supported]
C3 at 350 K/2400 s continues to give complete or near-complete conversion, lower degradation warning (~0.09–0.11), high crystal purity, and recovery up to ~0.54. Keep this upstream recipe while screening solvents, noting that solvent and catalyst effects are not independently replicated.

## H3 [tentative, prospective]
The nominal solvent dossier may be incomplete or misleading for number-weighted fines. Screen S3 then S0 under a common seeded crystallization schedule. Their higher solubility may reduce supersaturation and nucleus count even though nominal growth/nucleation priors are less favorable. A material effect requires a large change beyond the ~0.015–0.018 measurement noise, ideally replicated.

## Decision rule
If a solvent yields fines <=0.50 with purity >=0.80, use remaining batches to optimize its stop temperature, seed use, and hold. Otherwise test S1/S3 at reduced reagent loading as a direct supersaturation intervention.

## Revision 5

Recorded: 2026-10-13T11:13:27.734897+00:00; available public operations: 157; reviewed through: runner-operation-0157.

# Working hypotheses

## H1 [supported for particle quality, not recovery]
The configured feedback-control ramp at 0.001 K/s transformed particle quality: batch 11 gave particle-size fines 0.0045 and size 0.384 before filtration, with final fines 0 and size 0.396 (runner-operation-0154, -0157). This is a decisive change from every direct `cool_crystallize` schedule, all of which produced fines near 1. However, seed-excluded recovery was essentially zero (8e-6), implying the control ramp matured/preserved seed crystals without precipitating appreciable target. Thus batch 11 meets quality but not the feasibility recovery target.

## H2 [supported in tested direct-crystallization scope]
Direct `cool_crystallize` operations deliver substantial recovery (~0.42–0.55) and high purity but create an unacceptable number of fines, across solvents, seed choices, temperatures, and histories. Reduced loading also failed to improve fines (runner-operation-0141).

## H3 [tentative, prospective]
A hybrid should combine both regimes: first mature a small seed population with a slow configured-control ramp to ~295 K, then invoke a long isothermal `cool_crystallize` hold at that same warm temperature to deposit target onto the established crystals. Prediction for batch 12: recovery should rise well above batch 11 while particle fines remain far below the direct-cooling results. Filtering warm avoids the late secondary-nucleation regime. Failure would indicate that `cool_crystallize` intrinsically initiates a new fine population regardless of pre-existing large crystals.

## Decision rule
Recommend batch 12 if it satisfies purity >=0.80 and fines <=0.50 with recovery above batch 11. Otherwise batch 11 is the only known quality-compliant process, but clearly state that it misses the 0.10 feasibility target.

## Revision 6

Recorded: 2026-10-13T11:13:58.338540+00:00; available public operations: 171; reviewed through: runner-operation-0171.

# Final source-stage hypotheses and decision

## H1 [supported in campaign scope]
The operation class, not simply nominal solvent, seed amount, loading, or elapsed cooling time, controlled the number-weighted particle population. Every batch containing a direct `cool_crystallize` operation produced final fines near 0.99–1.00, including the hybrid batch 12 after slow seed maturation (runner-operation-0171). These batches generally achieved recovery ~0.42–0.55 and purity >=0.97, so their failure is specifically the fines gate.

## H2 [supported with an important limitation]
A configured 0.001 K/s control ramp without direct `cool_crystallize` gave large, high-quality particles and final fines 0 in batch 11 (runner-operation-0154, -0157), but seed-excluded recovery was only 0.0000083. This strongly suggests the observed solids were essentially the purchased seed population; the result satisfies the stated purity/fines constraints but misses the 0.10 feasibility target and is not an effective recovery process.

## H3 [rejected]
The proposed hybrid of controlled seed maturation followed by warm direct crystallization did not preserve particle quality: batch 12 returned fines 1.00 and size 0.055 while recovery rose to 0.472 (runner-operation-0168, -0171). Thus, in this tested system, invoking direct crystallization creates a dominant new fine population even with pre-existing large seeds.

## Final decision
Select lifecycle batch 11 because it is the only completed batch satisfying both hard quality constraints (purity 1.00, fines 0.00). State clearly that its recovery is effectively zero and below the initial 0.10 feasibility target; no tested batch combined acceptable fines with practically useful recovery. Batch 12 and batch 9 had higher recovery but are ineligible because fines were 1.00.
