# repeat-03 / C-W03-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T11:59:17.113731+00:00; available public operations: 0; reviewed through: None.

# Hypothesis notebook

## H1 [tentative]
Solvent S2 should favor larger, purer crystals and fewer fines because its nominal growth is high and nucleation/occlusion low, but its low solubility may improve recovery. Catalyst C1 is the initial reaction prior because its nominal activity is highest. A moderate hot reaction followed by seeded slow cooling and a low-temperature hold should therefore give feasible recovery with purity >=0.80 and fines <=0.50.

**Pre-experiment test:** Batch 1 will use full reagent/catalyst loading in S2, react hot, then seed and cool slowly. If conversion or recovery is poor, vary catalyst/temperature; if fines fail, reduce seed dose and/or slow cooling/extend growth hold. Material dossier is only a prior and may be misindexed.

## Revision 2

Recorded: 2026-10-14T12:02:20.588040+00:00; available public operations: 61; reviewed through: runner-operation-0061.

# Hypothesis notebook

## H1 [supported in scope]
S2 consistently permits very high crystal purity after filtration. Single 14,400 s cooling to 275 K can satisfy fines, but repeating the cold stage can increase recovery while producing excessive fines (B2/B3 final assays: runner-operation-0027, runner-operation-0039). Thus recovery/fines tradeoff is dominated by thermal history rather than purity in this region.

## H2 [supported in scope]
C2 is inferior for target formation under 340 K/1800 s (HPLC runner-operation-0045) versus C0/C1/C3 screens. C1 and C3 are leading reaction catalysts; C1 at 340 K/1800 s had about 0.61 selectivity (runner-operation-0021), while overly severe C1 at 360 K/3600 s reached full conversion but more byproduct (runner-operation-0007).

## H3 [unresolved]
Batch-to-batch fines differ substantially even with nominally similar single-stage 275 K cooling (runner-operation-0015, -0050, -0061). Upstream impurity profile, catalyst identity, and seed effectiveness are confounded. Prediction: a larger seed dose and slightly warmer endpoint should reduce fines, though possibly at recovery cost.

**Decision:** retain S2, focus on C1/C3 with less severe reaction and single controlled cooling. Avoid repeated cold stages unless a later intervention demonstrably controls fines.

## Revision 3

Recorded: 2026-10-14T12:04:42.860602+00:00; available public operations: 128; reviewed through: runner-operation-0128.

# Hypothesis notebook

## H1 [supported in tested scope]
S2 gives excellent filtered crystal purity across all completed conditions. Crystal recovery and fines are jointly governed by upstream target/impurity composition and crystallization supersaturation.

## H2 [supported in tested scope]
C1 at 350 K for 1800 s followed by 0.02 g seed and one 14,400 s cooling stage is the best observed feasible window. B10 at 275 K and B11 at 270 K both met purity/fines constraints and gave crystal_yield about 0.560 (runner-operation-0117, runner-operation-0128). The endpoint difference is numerically small relative to assay noise and run variability, so an endpoint effect is unresolved.

## H3 [supported]
Very high upstream target formation under 340 K/900 s did not translate into compliant solids at tested endpoints (B6-B9); fines stayed above 0.58. Conversely, severe 360 K/3600 s lowered selectivity but produced a feasible B1. This supports an impurity/supersaturation-mediated fines tradeoff rather than maximizing reaction yield alone.

## H4 [rejected in tested scope]
Increasing seed from 0.02 g to 0.05 g did not suppress fines (runner-operation-0072), and 0.005 g also failed (runner-operation-0080/-0086). A 300 K reheat/recool cycle did not improve the particle distribution (runner-operation-0083).

**Final test prediction:** repeating the 350 K/1800 s upstream window with a 265 K endpoint may slightly raise recovery while remaining near the fines limit. If fines exceed 0.50, prefer B10/B11 rather than the colder endpoint.

## Revision 4

Recorded: 2026-10-14T12:05:17.149329+00:00; available public operations: 139; reviewed through: runner-operation-0139.

# Hypothesis notebook

## H1 [supported in tested scope]
S2 with C1 provides a robust high-purity route. The best observed upstream window was 0.04 mol reagent, 0.08 L S2, 0.005 mol C1, heated at 350 K for 1800 s with 500 rpm stirring.

## H2 [supported in tested scope]
With that upstream window, 0.02 g seed and one 14,400 s cooling stage over 275–265 K repeatedly met purity and fines specifications (B10–B12, runner-operation-0117, -0128, -0139). Colder endpoint differences are small and confounded with run variability, but B12 at 265 K had the highest observed compliant crystal_yield (0.571), purity 0.995, and fines 0.424.

## H3 [supported]
Maximizing liquid-phase target yield alone is not sufficient: 340 K/900 s produced higher-selectivity reaction mixtures but excessive fines in the tested crystallizations. Repeated cold stages increased fines, and a reheat/recool intervention did not rescue the distribution.

## Decision
Recommend completed Batch 12. It maximizes observed seed-excluded crystal recovery among batches satisfying purity >=0.80 and fines <=0.50. B10/B11 independently support the same process window, though exact endpoint ranking remains unresolved within assay/process variability.
