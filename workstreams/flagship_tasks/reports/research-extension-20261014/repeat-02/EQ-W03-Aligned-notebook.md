# repeat-02 / EQ-W03-Aligned — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T11:39:20.334381+00:00; available public operations: 0; reviewed through: None.

# Aqueous equilibrium hypothesis notebook

## Pre-experiment predictions (before batch 1)
**H1 [tentative].** Within water near ambient conditions, pH and acid dissociation should be governed primarily by analytical loading concentration (total reagent mol / liquid L), with amount and volume pairs at matched concentration giving similar responses. A monoprotic weak-acid effective pKa near the supplied 4.97–5.07 interval predicts modestly greater dissociation and higher pH on dilution.

**H2 [tentative].** The archival dilution claim at 0.001 mol, 0.018→0.054 L predicts changes of about +0.00404 in dissociation fraction and +0.001826 in pH_normalized. I will directly bracket this pair. A materially different direction or a change well beyond measurement-scale expectations would reject its local applicability.

**H3 [unresolved].** Precipitation may depend on concentration, absolute loading, or both. Matched-concentration pairs across different amount/volume scales will distinguish these only if differences exceed assay scatter and repeat measurements are coherent.

Design decision: use all 12 batches as an aqueous loading–dilution matrix, including matched-concentration pairs and one direct archival-anchor pair. One pH-meter snapshot per batch will provide within-batch comparison to the required final assay. No claim will be generalized to nonaqueous solvents, additives, or other temperatures.

## Revision 2

Recorded: 2026-10-13T11:40:23.945264+00:00; available public operations: 60; reviewed through: runner-operation-0060.

# Aqueous equilibrium hypothesis notebook

## Final source-stage interpretation

**H1 [supported only as an effective weak-acid description].** Across the 12 ambient aqueous batches, the final assays are mutually compatible with a monoprotic Henderson–Hasselbalch-style relationship
`pKa_eff = pH - log10(alpha/(1-alpha))`.
Derived batch values span 4.93–5.11, mean 5.020 and population scatter about 0.051. This supports the supplied effective-pKa interval as a useful central local description, but the scatter and single final replicate per condition do not establish a universal constant. Evidence: final assays runner-operation-0005 through runner-operation-0060.

**H2 [supported at the specified anchor].** For 0.001 mol diluted from 0.018 L to 0.054 L, final assays changed acid dissociation by +0.00463 and pH_normalized by +0.00151 (runner-operation-0005 vs runner-operation-0010). These are close in sign and magnitude to the archival +0.00404 and +0.001826 predictions. The paired pH-meter snapshots were noisier and gave a larger pH change (runner-operation-0003 vs runner-operation-0008), so the conclusion is limited to compatibility rather than precise validation.

**H3 [unresolved; no detected precipitation law in this matrix].** Final precipitation_signal remained narrowly clustered around roughly 0.15–0.16 across analytical loading 0.0185–1 mol/L. Matched-concentration comparisons at 0.1667 mol/L (batches 3/6) and 0.5 mol/L (batches 7/9/10) do not show a coherent absolute-loading trend relative to assay scatter. The public proxy could be a near-constant background, a saturated/clipped response, or a weak concentration/amount effect hidden by noise; these are observationally equivalent here. Intermediate pH-meter precipitation readings were visibly more variable and do not resolve the alternatives.

**Scope and uncertainty.** Conclusions apply only to water, approximately 298 K, no additives, 0.001–0.04 mol total loading, 0.018–0.08 L, and the public bounded channels. Final-assay noise is nonzero and conditions lack true replicate final assays, so numerical differences outside the direct archival pair are not by themselves evidence of effects. `equilibrium_confidence` was treated only as an environment diagnostic. Residuals were generally near zero and do not supply uncertainty estimates.

**Testable consequence / next decision.** A future replicated dilution series at fixed amount, plus replicated matched-concentration scale pairs, should preserve the weak-acid direction while precipitation remains constant if the background explanation is correct. A reproducible precipitation trend exceeding within-condition replicate scatter would overturn H3's current suspension. Batch 2 is the best single evidentiary anchor because it is the diluted member of the explicitly predicted archival pair and, together with batch 1, directly tests the supplied local relationship.
