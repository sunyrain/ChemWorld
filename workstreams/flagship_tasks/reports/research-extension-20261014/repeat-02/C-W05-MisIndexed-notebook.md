# repeat-02 / C-W05-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T17:29:03.817639+00:00; available public operations: 0; reviewed through: None.

# Hypothesis notebook

## H1 [tentative]
Within the nominal dossier scope, solvent S2 should favor crystal growth and low impurity occlusion, so a reacted solution cooled slowly with modest seed should give purity above 0.80 and fewer fines than S0. Its lower solubility may also improve crystallization recovery. This may fail if the fixed-world solvent residual reverses the nominal ordering.

## H2 [tentative]
Catalyst C1 is the initial reaction choice because its nominal activity is highest; moderate-hot reaction conditions should raise target available for crystallization, while excessive temperature/time may increase degradation. A first test will use C1/S2, then later batches will vary reaction loading, seed dose, cooling and holding.

## Pre-experiment expectation
For batch 1, C1/S2 with full reagent/catalyst loading, a hot reaction hold, modest seeding, slow cooling and a cold hold is expected to produce measurable seed-excluded recovery (>0.10), purity >=0.80, and fines <=0.50. Particle sizing before filtration will test the fines expectation.

## Revision 2

Recorded: 2026-10-13T17:30:54.222433+00:00; available public operations: 36; reviewed through: runner-operation-0036.

# Hypothesis notebook

## H1 [supported in tested S2 conditions]
Solvent S2 can deliver on-spec crystallization: all first three final assays had purity well above 0.80 and fines below 0.50 (events runner-operation-0014, -0025, -0036). Cooling to 250 K in batch 2 increased observed crystal recovery to 0.473 versus 0.395 in batch 1, which cooled only to 275 K and then warmed during a wait. Temperature history and reaction conditions are confounded, so the size of the cooling effect is unresolved.

## H2 [revised]
Hotter/longer reaction conditions appear harmful to selectivity/degradation: batch 1 at 370 K for 3600 s had final selectivity about 0.497 and degradation warning 0.218, while batch 2 at 350 K for 1800 s had selectivity about 0.564 and degradation warning 0.073 (same C1/S2/loading). I will avoid the hotter history unless later evidence contradicts this.

## H3 [unresolved]
A 0.05 g seed dose may improve recovery/size relative to 0.005 g, but batches 2 and 3 also differ in reaction temperature; observed recovery was 0.473 versus 0.437. A matched seed-dose comparison is needed.

## Decision
Keep 250 K long cooling as the working crystallization condition; test solvent and catalyst choices, then return to matched thermal/seed optimization. Claims will change if another solvent gives higher on-spec recovery or if matched S2 runs reverse the current seed-dose ordering.

## Revision 3

Recorded: 2026-10-13T17:31:48.371431+00:00; available public operations: 80; reviewed through: runner-operation-0080.

# Hypothesis notebook

## H1 [supported in tested scope]
S2 is the only screened solvent meeting both crystal quality constraints under the common 340 K reaction / 250 K crystallization recipe. S2 batches 3–4 had purity 0.991–1.000 and fines 0.380–0.397 (events runner-operation-0036, -0047). S3, S1 and S0 gave fines 0.769, 0.616 and 0.768 respectively (events -0058, -0069, -0080), despite acceptable purity. Thus their higher or similar numerical recoveries are not feasible for the stated goal.

## H2 [supported directionally]
Avoid the 370 K/3600 s reaction history because of its larger degradation warning (event -0014) than the shorter, cooler runs. Reaction effects on crystallization recovery remain secondary because recovery is normalized to target present before separation.

## H3 [unresolved small effect]
At matched 340 K reaction and 250 K cooling, increasing seed from 0.005 to 0.05 g changed observed recovery from 0.437 to 0.452 (events -0036, -0047), while final size changed only from 0.066 to 0.077 and fines from 0.380 to 0.397. These differences are small relative to single-run measurement noise/process variation; do not claim a seed effect yet.

## Decision
Restrict optimization to S2. Next screen catalyst identity under the common recipe, then test extended cold history and a clearly larger seed dose. Another solvent would be reconsidered only if a changed thermal/seed history brings fines below 0.50 while preserving its recovery advantage.

## Revision 4

Recorded: 2026-10-13T17:33:07.887443+00:00; available public operations: 133; reviewed through: runner-operation-0133.

# Hypothesis notebook

## H1 [supported in tested scope]
S2 remains the robust solvent for the fines constraint. Under the common recipe, C0 gave the best feasible observed recovery: 0.500 with purity 0.978 and fines 0.412 (event runner-operation-0091). C2 was feasible but lower recovery (0.387, event -0102). C3 gave higher numerical recovery (0.525) but missed the fines constraint at 0.534 (event -0113).

## H2 [supported directionally]
A tenfold seed increase from 0.05 to 0.50 g with C3 moved fines from 0.534 to 0.516 and recovery from 0.525 to 0.516 (events -0113 and -0133). The differences are modest and the high-seed run still fails the fines constraint; large seed is therefore not adopted as the final strategy.

## H3 [unresolved small effect]
The matched C1 seed comparison (0.005 versus 0.05 g) showed only small differences (events -0036, -0047). Across current evidence, catalyst/solvent identity and cold endpoint dominate seed-dose changes in practical importance.

## Final-batch prediction
For batch 12, use C0/S2 at 340 K for 1800 s, 0.05 g seed, and two consecutive 250 K crystallization periods. Prediction made before execution: extended cold residence should raise recovery above batch 8's 0.500 while retaining purity >=0.80 and fines <=0.50. I will prefer it only if the final assay confirms both constraints; otherwise batch 8 remains the recommendation.

## Revision 5

Recorded: 2026-10-13T17:33:32.855481+00:00; available public operations: 144; reviewed through: runner-operation-0144.

# Hypothesis notebook

## H1 [supported in campaign scope]
S2 was the only solvent providing a robust fines margin under the common crystallization recipe. S0, S1 and S3 had acceptable purity but failed the fines constraint in their screened runs (events runner-operation-0058, -0069, -0080). This is a local benchmark conclusion, not a universal solvent claim.

## H2 [supported in tested scope]
The recommended reaction/crystallization combination is C0/S2, 0.04 mol reagent and 0.005 mol catalyst in 0.08 L solvent, reacted at 340 K for 1800 s with 500 rpm stirring, seeded with 0.05 g, cooled to 250 K over 14400 s, then filtered. Batch 8 measured crystal recovery 0.500, purity 0.978 and fines 0.412 (event -0091), the highest observed recovery among batches satisfying both quality constraints.

## H3 [unresolved]
A second consecutive cold period did not improve the response: batch 12 measured recovery 0.486, purity 0.993 and fines 0.427 (event -0144). This numerical difference from batch 8 is small enough that repeatability remains unresolved; nevertheless, the extra cold period adds time without observed benefit, so it is not recommended.

## H4 [bounded alternative]
C3 produced higher numerical recovery (0.525) but fines 0.534 (event -0113). Raising seed tenfold reduced fines only to 0.516 while recovery was 0.516 (event -0133), still off-spec. C3 could be revisited with a different controlled growth/redissolution strategy, but current evidence does not support recommending it.

## Final decision
Select completed batch 8. It has the highest measured recovery among on-spec batches and a comfortable fines margin relative to the 0.50 boundary. Batch 12 is also on-spec but lower in observed recovery; batches 6, 7, 10 and 11 have tempting recovery values but fail the fines requirement.
