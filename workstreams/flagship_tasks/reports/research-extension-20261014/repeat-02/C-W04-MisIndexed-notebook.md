# repeat-02 / C-W04-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T17:18:50.288979+00:00; available public operations: 0; reviewed through: None.

# Working hypotheses

H1 [tentative] Solvent S2 should favor high recovery with acceptable purity and low fines because its nominal dossier combines low solubility, high growth, low nucleation and low impurity occlusion. S3 is the main alternative; S1 may improve reaction formation but risks weaker crystallization.

H2 [tentative] Catalyst C1 is the first reaction-screen choice from nominal activity, but C2/C3 may outperform through fixed world residuals. Prediction: with equal charge and thermal history, the best catalyst gives higher target formation without a large byproduct penalty.

H3 [tentative] A hot reaction followed by seeded, gradual cooling and a cold hold should favor growth over spontaneous fines. Reheating/recooling may reduce fines but could sacrifice recovery. Initial test: full 0.04 mol reagent, 0.005 mol catalyst, 0.08 L S2, 1 g seed; react near 360 K, then seed and cool slowly to about 275 K with a hold and filtration.

Decision rule: prioritize final crystal_yield only among batches meeting purity >=0.80 and fines <=0.50; revise material and thermal choices after measured evidence.

## Revision 2

Recorded: 2026-10-13T17:21:06.975210+00:00; available public operations: 48; reviewed through: runner-operation-0048.

# Working hypotheses

H1 [partly supported] S2 gives high crystallization recovery and purity, but the tested direct-cooling processes fail the fines constraint. Final assays gave recovery about 0.42 and 0.45 with purity about 0.99, while fines were essentially 1 (events runner-operation-0015 and -0048).

H2 [unresolved] C1 produces complete conversion but only moderate selectivity under tested hot reactions. The lower-temperature/shorter batch had numerically lower byproduct and degradation than the first, but reaction conditions and crystallization history are confounded; catalyst alternatives remain untested.

H3 [rejected for tested scope] Increasing seed from 0.05 g to 1.0 g did not solve fines under direct cooling to 275 K: in-process fines remained about 0.99 (runner-operation-0045). Seed dose alone is not the dominant lever here.

H4 [tentative, prospective] Burst nucleation during a single deep cool may dominate. A staged slow cool, beginning while still hot and allowing growth at mild supersaturation, should increase size and reduce fines. Solvent S3 is a useful alternative because nominal nucleation and occlusion are lower than S1/S0, although its growth is below S2.

Decision rule remains: maximize final crystal_yield only among purity >=0.80 and fines <=0.50. Next test S3 with staged cooling and small seed; later separate solvent from staging if promising.

## Revision 3

Recorded: 2026-10-13T17:23:37.558089+00:00; available public operations: 149; reviewed through: runner-operation-0149.

# Working hypotheses

H1 [supported in tested scope] Solvent S3 with staged cooling supports acceptable purity and low fines. Direct filtration after stages to 280 K met specifications with recovery ~0.44 and fines ~0.24 (runner-operation-0096); extension to 265 and 250 K increased observed recovery to ~0.46 and ~0.50 while fines stayed ~0.18 and ~0.12 (runner-operation-0112, -0129).

H2 [unresolved] Catalyst C3 is compatible with the best S3 crystallizations, but catalyst effects on reaction selectivity are not isolated from batch variability. Since crystallization recovery is conditional on pre-separation target, upstream catalyst is secondary unless purity changes.

H3 [rejected for broad claim; narrower effect supported] Seed dose alone did not fix direct cooling, but small seeding plus staged cooling works. The dominant evidence favors thermal trajectory over seed mass.

H4 [supported] Deep cooling in 15 K stages suppresses fines rather than causing the feared burst under S3. The best completed batch reached recovery ~0.496, purity ~0.970, fines ~0.123 (runner-operation-0129). Extra cold residence gave only a small numerical recovery increase to ~0.501, within final-assay noise, while retaining quality (runner-operation-0149); a residence effect remains unresolved.

Prospective tests: reduce seed to 0.005 g under the successful staged trajectory; then increase upstream concentration by reducing S3 volume to 0.06 L. Either is retained only if final purity >=0.80 and fines <=0.50. Final confirmation should replicate the best robust recipe.

## Revision 4

Recorded: 2026-10-13T17:25:14.799627+00:00; available public operations: 228; reviewed through: runner-operation-0228.

# Final working synthesis

H1 [supported in tested scope] S3 plus small seeding and staged cooling from the reaction temperature to 250 K repeatedly met purity and fines constraints. Batches 7, 8, 9 and 12 all gave final recovery about 0.49–0.50, purity about 0.97–0.98 and fines about 0.12–0.15 (runner-operation-0129, -0149, -0169, -0228). This repeatability is stronger evidence than any single difference.

H2 [supported comparatively, scope limited] Staged cooling is necessary in the tested region: direct-cooling S2 batches had fines near 1 (runner-operation-0015, -0048), whereas staged S3 batches were comfortably below 0.50. Solvent and thermal history were not fully factorial, so their individual contributions remain partly confounded.

H3 [unresolved small effects] Extending residence at 250 K and changing seed from 0.05 to 0.005 g caused only small numerical recovery differences relative to final-assay noise; no firm effect is claimed. The 0.05 g condition has more successful replication.

H4 [supported tradeoff] Higher loading (0.06 L S3) retained recovery near 0.50 but raised fines to about 0.43 (runner-operation-0189). S2 staged to 250 K also met constraints but had lower recovery ~0.48 and higher fines ~0.42 (runner-operation-0209). Thus 0.08 L S3 has the more robust quality margin.

Decision: recommend completed batch 8 because it has the highest observed eligible crystal_yield (~0.501) with purity ~0.970 and fines ~0.123 (runner-operation-0149), and its behavior is corroborated by batches 7, 9 and 12. Conditions represented: 0.04 mol reagent, 0.08 L S3, 0.005 mol C3, 340 K/1800 s reaction, 0.05 g seed, 15 K staged 14400 s cools through 325/310/295/280/265/250 K, followed by three additional 14400 s periods at 250 K and filtration. Batch 8's numerical lead over nearby replicates is not asserted as statistically decisive.
