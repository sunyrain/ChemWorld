# repeat-01 / C-W04-Aligned — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-14T10:45:59.358242+00:00; available public operations: 0; reviewed through: None.

# Working hypotheses

## H1 [tentative]
Within the anonymous dossier, solvent S2 should favor large, purer crystals (high growth, low nucleation and occlusion) and lower solubility should improve recovery; S1 is a plausible second choice. This may be overturned by fixed-world residuals.

## H2 [tentative]
A high-activity catalyst at moderate thermal severity, followed by seeded slow cooling and a growth hold, should combine conversion with low fines. Excessive seed dose or rapid cooling is expected to raise number-weighted fines, while insufficient conversion will cap overall crystal yield.

## Initial test
Start with a full 0.04 mol reagent charge, S2, a moderate catalyst charge, heated reaction, then modest seeding and controlled cooling/hold. A final assay and one diagnostic measurement will determine whether to prioritize upstream conversion, recovery, or particle quality next.

## Revision 2

Recorded: 2026-10-14T10:48:33.102828+00:00; available public operations: 97; reviewed through: runner-operation-0097.

# Working hypotheses

## H1 [supported in tested scope]
Solvent identity is consequential. At the common C1/370 K reaction and similar crystallization history, S1 gave higher overall crystal recovery than S2 (batch 7 final event runner-operation-0085 versus batch 1 runner-operation-0013), though batch 7 narrowly failed the fines constraint. S3 produced excessive fines and lower recovery (runner-operation-0073). The comparisons are single batches and therefore numerical, not yet repeatability evidence.

## H2 [supported in tested scope]
For S1, increasing seed from 0.02 g and lengthening cooling/aging produced a qualifying batch: batch 8 reached about 0.476 seed-excluded recovery, 0.980 purity, and 0.449 fines (runner-operation-0097). The preceding particle-size reading also predicted compliant fines (runner-operation-0094), supporting rather than proving that the changed crystallization history reduced fines relative to batch 7.

## H3 [tentative]
Upstream conversion is already saturated near unity, so further recovery gains should come from selectivity and crystallization recovery rather than longer reaction time. C1 was at least as good as C0/C2/C3 in the S2 screen (runner-operation-0013, -0037, -0049, -0061), but solvent and run noise remain confounded with no replicate.

## Decision
Use remaining batches to replicate/refine the S1/C1 process. Test seed dose, cooling endpoint, and reaction temperature while retaining slow cooling plus aging. A higher recovery that remains clearly below 0.50 fines would replace batch 8; otherwise retain batch 8.

## Revision 3

Recorded: 2026-10-14T10:50:10.334272+00:00; available public operations: 152; reviewed through: runner-operation-0152.

# Final working interpretation

## H1 [supported in tested scope]
S1/C1 was the strongest tested material combination. Raising the reaction temperature from 370 K to 390–410 K while shortening residence time increased reaction yield and subsequent crystal recovery (runner-operation-0109 and runner-operation-0121 versus runner-operation-0097). This trend is bounded to the tested duration/temperature combinations and is not a general kinetic law.

## H2 [supported but variable]
A 0.05 g seed dose with slow cooling to 285 K and a long low-agitation aging period can satisfy the fines constraint, as in batches 8 and 9 (runner-operation-0097, runner-operation-0109), but batch 10 narrowly failed under nominally similar crystallization conditions (runner-operation-0121). Thus particle quality has meaningful run-to-run or upstream-history sensitivity; the numerical differences should not be treated as precisely reproducible.

## H3 [not supported]
The tested staged cooling and reheating/recooling interventions did not improve fines. Batch 11 remained just above the fines limit after mild reheat (runner-operation-0136); batch 12 became substantially finer after staged cooling and a stronger reheat/recool sequence (runner-operation-0152). These interventions are shelved within the tested scope.

## Final decision
Batch 9 is the best completed batch meeting both constraints: crystal recovery about 0.535, purity about 0.984, and fines about 0.459 (runner-operation-0109). Batch 10 had higher measured recovery (~0.578) but is ineligible because fines were ~0.524. Recommend batch 9 while noting the observed particle-quality variability; a future confirmation should replicate its exact thermal history and verify fines before scale-up.
