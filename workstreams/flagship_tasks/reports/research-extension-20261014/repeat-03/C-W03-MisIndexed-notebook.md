# repeat-03 / C-W03-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T18:10:22.051453+00:00; available public operations: 0; reviewed through: None.

# Hypothesis notebook

## H1 [tentative]
Within the tested anonymous-material space, solvent S2 should favor larger, purer crystals and fewer fines because its dossier indicates high growth, low nucleation, and low occlusion; its lower solubility may also improve recovery. A deliberately seeded, slow-cooling/low-temperature hold process should outperform an unseeded rapid cool on crystal yield while meeting purity >=0.80 and fines <=0.50.

## H2 [tentative]
Reaction performance will likely favor catalyst C1 by nominal activity, but catalyst identity and thermal severity may trade conversion against byproduct/degradation. Initial screening will compare catalysts/solvents and then focus on crystallization history.

**Pre-experiment prediction:** A moderate catalyst charge, warm reaction hold, S2 solvent, seed near onset of cooling, slow cooling, and a cold growth hold will be feasible and superior to a fast/unseeded baseline. This would change if early assays show poor conversion, purity below specification, or excessive fines.

## Revision 2

Recorded: 2026-10-13T18:12:01.239975+00:00; available public operations: 27; reviewed through: runner-operation-0027.

# Hypothesis notebook

## H1 [partly supported; fines prediction rejected]
S2 with seeded cooling gives high crystal purity and substantial crystallization recovery, but the expectation of few fines is contradicted. Batch 1 final assay (runner-operation-0014) gave crystal yield ~0.464 and purity ~0.985 but fines ~0.997; batch 2 (slower, warmer cooling and lower seed) remained ~1.00 fines with yield ~0.402 (runner-operation-0027). Thus modest changes in seed (0.05 to 0.01 g), terminal temperature (275 to 290 K), and hold did not reach the fines constraint. Differences are confounded by reaction temperature and cooling history, and no repeatability estimate exists.

## H2 [unresolved]
C1 produces complete apparent conversion in S2 at both tested reaction temperatures, but selectivity is only about 0.55-0.58 and byproduct signal about 0.32 (runner-operation-0007, runner-operation-0027). Reaction severity may affect degradation, but crystallization purity nevertheless exceeded specification.

## H3 [tentative, prospective]
The extreme number-fines fraction may require Ostwald-ripening-like thermal cycling or a solvent with less nucleation rather than simple slower cooling. Next tests will compare S3 and/or reheat/recool near the dissolution boundary. A material drop in fines, especially below 0.50 with preserved purity, would support this; no change would shift focus to higher-temperature growth/longer cycling or altered seed dose.

## Revision 3

Recorded: 2026-10-13T18:15:49.385486+00:00; available public operations: 186; reviewed through: runner-operation-0186.

# Hypothesis notebook

## H1 [supported only for purity/recovery; rejected for fines under direct cooling]
S2 consistently supported high crystal purity and useful recovery, but direct one-stage cooling produced predominantly sub-20 um particles. Examples include batch 1 (runner-operation-0014) and batch 5 (runner-operation-0083). Long isothermal holding alone did not resolve fines, so time at the terminal temperature is not sufficient in this tested scope.

## H2 [supported in tested scope]
Upstream loading strongly changes particle outcome. Lowering reagent loading from the high-loading regime reduced fines in batch 6 (runner-operation-0096), and very low loading in batch 8 produced zero measured fines and excellent CSD quality but only ~0.017 crystal yield (runner-operation-0122). The response is nonlinear: modestly higher loads caused renewed excessive fines (runner-operation-0135, runner-operation-0148). This supports a supersaturation/secondary-nucleation threshold interpretation, though seed-to-product ratio and concentration are confounded.

## H3 [supported in a narrow recipe window]
Staged cooling can keep fines below specification at a useful loading. Batch 11 used S2, C1, 0.010 mol reagent in 0.080 L solvent, 0.00125 mol catalyst, 340 K reaction, 0.05 g seed, then sequential 4 h cooling stages at 295, 290, 285, 280, and 275 K plus a 4 h cold hold. It achieved final crystal yield ~0.281, purity ~0.997, and fines ~0.188 (runner-operation-0165). Its preceding particle measurement also showed fines ~0.199 (runner-operation-0162), supporting rather than contradicting the final result.

Higher loading was not safely transferable: batch 12 used a finer staged schedule but at 0.015 mol reagent and recovered ~0.367 with fines ~1.0 (runner-operation-0186). Thus loading, not merely ramp subdivision, bounds the successful regime.

## Decision
Recommend completed batch 11 because it has the highest observed crystal yield among batches meeting both purity >=0.80 and fines <=0.50. Batch 8 also met quality constraints but had much lower recovery. Batch 12 recovered more but failed the fines constraint. Uncertainty remains from single-batch comparisons and instrument noise; the selection would change if a replicate or nearby loading demonstrated higher recovery with fines reliably below 0.50.
