# repeat-01 / C-W05-Aligned — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T10:54:44.149145+00:00; available public operations: 0; reviewed through: None.

# Hypothesis notebook

## H1 [tentative]
At equal loading and reaction history, solvent S2 should favor recovery and larger/cleaner crystals because its dossier gives low solubility, high growth, low nucleation, and low occlusion; S1 is the main alternative. A slow seeded cool with a cold hold should reduce fines relative to an unseeded or rapid cool. This is a prior, not experimental evidence.

## H2 [tentative]
Catalyst C1 is the conservative first reaction choice (high nominal activity with modest variability); C3 may outperform it. Initial test: 0.04 mol reagent, 0.08 L solvent, 0.005 mol catalyst, hot reaction, quench/cool, seed, hold, filter. I will change material choice if HPLC/final assays contradict these expectations.

## Revision 2

Recorded: 2026-10-14T10:56:47.760743+00:00; available public operations: 27; reviewed through: runner-operation-0027.

# Hypothesis notebook

## H1 [partly supported]
S2 processes can give very pure crystals, but fines depend strongly on thermal/seeding history. Batch 1 (events 0006–0016) gave purity 0.986 but fines 0.531; batch 2 (0021–0027), using much less seed and a single slower 14,400 s cool, met the fines constraint at 0.480 with purity 0.982. The designs also differed in reaction temperature/time and an intervening warm hold, so the causal contribution of seed dose versus cooling history remains unresolved. I will retain the batch-2 crystallization protocol while screening catalysts.

## H2 [unresolved]
C1/S2 reaction selectivity remained only about 0.47–0.48 in both tested reaction schedules, while conversion was near complete. The numerical differences do not establish a temperature effect. Catalyst identity is now the main test factor; prediction before batches 3–5: C3 or C2 may improve target formation relative to C1, while C0 likely underperforms nominally. A final assay yield increase under otherwise matched conditions will change the preferred catalyst.

## Revision 3

Recorded: 2026-10-14T10:57:34.601248+00:00; available public operations: 72; reviewed through: runner-operation-0072.

# Hypothesis notebook

## H1 [narrowed]
The batch-2 fines success did not generalize across catalysts under the nominally same S2/0.01 g seed/direct slow-cool protocol: batches 3–5 gave fines about 0.590, 0.504, and 0.681. Thus catalyst-dependent composition or uncontrolled process variability materially affects particle outcomes; S2 alone is insufficient to ensure the fines limit. Batch 6 reduced seed to 0.001 g and staged the cool, but fines worsened to 0.612 while size fell, opposing the low-seed hypothesis in the C3/S2 scope. Next tests will change solvent while keeping C3 and the simpler 0.01 g seed slow cool.

## H2 [supported in tested S2 schedule]
C3 produced the highest recovery in the matched catalyst screen: batch 3 crystal yield 0.436 versus C1 0.368, C2 0.303, and C0 0.406; batch 6 repeated C3 at 0.461 despite altered crystallization. C3 therefore remains the reaction lead, although neither C3 batch met the fines constraint. C1 batch 2 is the current feasible fallback.

## H3 [tentative]
S1's lower nominal nucleation and occlusion tendencies may reduce C3 fines, at some recovery cost from higher solubility than S2. S3 is a higher-activity alternative but may worsen purity/occlusion. A feasible C3 solvent result would supersede batch 2 if its recovery exceeds 0.368.

## Revision 4

Recorded: 2026-10-14T10:58:19.426570+00:00; available public operations: 105; reviewed through: runner-operation-0105.

# Hypothesis notebook

## H1 [supported only as solvent ranking for fines]
Changing C3 from S2 to S1 or S3 increased rather than decreased fines (batches 7 and 8: 0.987 and 0.648). C1/S1 also failed at 0.659 (batch 9). Despite S1 giving the highest observed recovery (0.532 with C3), its particle distribution makes it infeasible. The dossier nucleation prior is therefore contradicted for these realized processes; S2 remains preferred for constraint control.

## H2 [supported in tested schedules]
C3 improves reaction/product recovery but creates a recovery–fines tradeoff: C3/S2 yielded 0.436–0.461 with fines 0.590–0.612, whereas feasible C1/S2 batch 2 yielded 0.368 with fines 0.480. Solvent changes raised C3 recovery but did not solve fines.

## H4 [tentative, pre-batch 10]
A high seed dose plus a cooling–reheat–recooling cycle may dissolve fines and regrow remaining crystals, lowering C3/S2 fines below 0.50 while retaining recovery above batch 2. Failure would favor using C1/S2 or testing upstream dilution/loading rather than further solvent changes.

## Revision 5

Recorded: 2026-10-14T10:59:01.978571+00:00; available public operations: 128; reviewed through: runner-operation-0128.

# Hypothesis notebook

## H1 [supported only as solvent ranking for fines]
S2 is the best tested solvent for fines control; S1 and S3 failed clearly under matched C3 schedules.

## H2 [supported with tradeoff]
C3 improves recovery, but standard full loading gave excessive fines. Batch 10's high-seed thermal cycle worsened fines to 0.819, rejecting that remedy in the tested scope.

## H5 [tentative, pre-batch 12]
Reducing C3/S2 reagent loading from 0.04 to 0.03 mol improved selectivity and recovery fraction (batch 11 yield 0.488) and lowered fines to 0.529, though it remained outside specification. A further reduction to 0.02 mol at unchanged solvent, catalyst, seed, and slow cool is predicted to cross the fines limit while retaining recovery above the feasible batch-2 value of 0.368. If it fails, batch 2 remains the only clear feasible recommendation.

## Revision 6

Recorded: 2026-10-14T10:59:28.322009+00:00; available public operations: 138; reviewed through: runner-operation-0138.

# Hypothesis notebook

## H1 [supported in tested campaign scope]
S2 was the best tested solvent for satisfying particle constraints. S1 increased recovery but produced excessive fines, and S3 also failed the fines limit (batches 7–9).

## H2 [supported with resolved operating condition]
C3 was the strongest recovery catalyst but required reduced upstream reagent loading to control fines. Full-load C3/S2 batches 3 and 6 achieved recovery 0.436–0.461 but fines 0.590–0.612; a high-seed thermal cycle in batch 10 worsened fines to 0.819. Reducing reagent charge to 0.03 mol in batch 11 raised recovery fraction to 0.488 and lowered fines to 0.529, suggesting a loading trend but still failing specification.

## H5 [supported by final test]
At 0.02 mol reagent, 0.08 L S2, 0.005 mol C3, 330 K/1800 s reaction, 0.01 g seed, and a 270 K/14,400 s cool, batch 12 achieved crystal yield 0.520, purity 0.994, and fines 0.387 (event 0138). This is the highest observed recovery among batches meeting purity >=0.80 and fines <=0.50. Batch 2 is an independent feasible fallback (yield 0.368, fines 0.480), but it is materially lower recovery.

## Decision
Recommend completed batch 12. Scope caveat: the apparent loading trend has only one batch at each loading, so repeatability and separate catalyst/loading effects remain unresolved; nonetheless the observed final assay satisfies both constraints with appreciable margin.
