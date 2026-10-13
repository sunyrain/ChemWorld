# repeat-02 / C-W01-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T17:32:35.359641+00:00; available public operations: 0; reviewed through: None.

# Hypothesis notebook

## H1 [tentative]
Within the anonymous-material scope, catalyst C1 and solvent S2 are the starting candidates: dossier values suggest C1 favors reaction activity while S2 favors crystal growth, low impurity occlusion, and lower solubility/nucleation. I expect a warm reaction followed by controlled seeded cooling and a low-temperature hold to give feasible recovery with purity ≥0.80 and fines ≤0.50.

**First test:** 0.04 mol reagent, 0.005 mol C1, 0.08 L S2; react warm, quench, seed modestly, cool slowly, hold, filter. A poor reaction HPLC result would weaken the catalyst/solvent activity prior; poor purity or high fines would motivate gentler supersaturation or lower seed dose.

## Revision 2

Recorded: 2026-10-13T17:34:30.581468+00:00; available public operations: 52; reviewed through: runner-operation-0052.

# Hypothesis notebook

## H1 [supported in tested scope]
Solvent S2 with catalyst C1 can meet both quality constraints. Batch 2 (event runner-operation-0027) and batch 3 (runner-operation-0039) had high purity and fines well below 0.50; cooling to 250 K in batch 3 increased measured recovery relative to 270 K in batch 2 while reaction time also changed, so the temperature effect is promising but not isolated.

## H2 [supported in tested scope]
Large seed charge is detrimental to number-weighted size/fines: 0.05 g in batch 1 produced essentially all fines (runner-operation-0015), whereas 0.001 g or 0.0002 g under slower direct cooling produced fines about 0.27–0.29 (runner-operation-0027, -0039, -0052). Cooling/hold history is confounded with seed dose, so the causal magnitude remains unresolved.

## H3 [tentative]
At 250 K, very low seed or unseeded crystallization may preserve recovery while increasing size by reducing crystal count. Batch 4 reached the best observed recovery (~0.65) with compliant purity/fines (runner-operation-0052). Next test removes seed under otherwise similar slow-cool/long-hold conditions; absent or highly fine crystals would reject this direction.

## Revision 3

Recorded: 2026-10-13T17:35:16.319583+00:00; available public operations: 90; reviewed through: runner-operation-0090.

# Hypothesis notebook

## H1 [supported in tested scope]
C1/S2 with slow cooling to 250 K repeatedly meets purity and fines constraints at 0.08 and 0.04 L solvent loadings (final assays runner-operation-0039, -0052, -0064, -0077).

## H2 [supported directionally, boundary found]
Reducing solvent from 0.08 to 0.04 L increased measured crystal recovery to ~0.67 while retaining compliant fines (batch 6, runner-operation-0077). Further reduction to 0.02 L caused essentially all fines and lower measured recovery (batch 7, runner-operation-0090). Thus the useful loading window has a boundary between 0.02 and 0.04 L; concentration-driven nucleation/kinetic trapping is a plausible alternative to a simple solubility explanation.

## H3 [unresolved]
Seed doses ≤0.001 g and no seed all worked at moderate loading, with small recovery differences comparable to stated assay noise and batch variation. Large 0.05 g seed remains clearly unsuitable under the tested history.

**Next decision:** test an intermediate 0.03 L loading with a partial reheat/recool cycle intended to dissolve fines and regrow fewer crystals. If fines remain >0.50, retain 0.04 L as the practical boundary.

## Revision 4

Recorded: 2026-10-13T17:35:59.824502+00:00; available public operations: 132; reviewed through: runner-operation-0132.

# Hypothesis notebook

## H1 [supported in tested scope]
C1/S2, 360 K/900 s reaction, slow cooling to 250 K, very low seed, and low-speed hold can produce high-purity compliant crystals.

## H2 [supported; sharp boundary]
Loading dominates fines nonlinearly. At 0.03 L solvent, neither a reheat/recool cycle nor four-stage slower cooling prevented nearly all-fines populations (runner-operation-0104, -0119), despite recoveries near 0.68. At 0.035 L, the same direct slow-cool family gave fines ~0.15 and recovery ~0.676 (runner-operation-0132). This brackets a sharp useful boundary between 0.030 and 0.035 L for 0.04 mol charge under tested conditions.

## H3 [unresolved]
Differences among compliant recoveries near 0.65–0.68 are modest relative to uncontrolled batch variation and assay noise; the 0.035 L result is nevertheless the current best measured compliant batch. Next test at 0.0325 L targets the boundary. A fines result >0.50 will favor 0.035–0.04 L for robustness; a compliant result with higher recovery will justify narrowing downward.

## Revision 5

Recorded: 2026-10-13T17:36:36.372641+00:00; available public operations: 157; reviewed through: runner-operation-0157.

# Hypothesis notebook

## H1 [supported in tested scope]
A robust compliant region uses catalyst C1, solvent S2, 0.04 mol reagent, warm reaction near 360 K, slow cooling to 250 K, very low seed, and low-speed cold holding. Multiple batches met purity ≥0.80 and fines ≤0.50.

## H2 [supported; loading optimum is constraint-limited]
Concentrating from 0.08 toward 0.035–0.04 L solvent improved measured crystallization recovery while remaining compliant. At 0.030 L and 0.020 L, fines rose to approximately unity (runner-operation-0090, -0104, -0119), and neither staged cooling nor partial reheat rescued the 0.030 L case. Thus maximizing recovery is limited by a sharp fines boundary rather than purity in this explored region.

## H3 [supported operational choice, quantitative effect unresolved]
Very low seed (0.0002 g) with slow cooling is preferable to 0.05 g seed, which caused nearly all fines (runner-operation-0015). At modest loading, low seed and no seed both worked; their small recovery differences are not isolated from batch variability.

## Final decision
Batch 10 is the best measured compliant completed batch: recovery 0.6762, purity 0.9874, fines 0.1453 (runner-operation-0132). Its 0.035 L recipe was independently repeated in batch 12 and remained compliant (recovery 0.6701, purity 1.0, fines 0.1359; runner-operation-0157), supporting robustness. Batch 8 had a numerically higher recovery (~0.684) but is ineligible because fines were ~0.987 (runner-operation-0104). Recommend batch 10; the result that would change this decision is a compliant replicate below 0.035 L with recovery exceeding the current best.
