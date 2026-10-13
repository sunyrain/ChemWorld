# repeat-03 / EQ-W04-Aligned — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T12:49:34.483135+00:00; available public operations: 0; reviewed through: None.

# Hypothesis notebook

## H1 [tentative; prospective]
Within water near ambient temperature, increasing total acid concentration (loading/volume) should lower pH and generally lower the dissociated fraction for a monoprotic weak-acid-like equilibrium. The supplied archival local estimate (effective pKa 5.149–5.249; at 0.001 mol, dilution 0.018→0.054 L predicts ΔpH_normalized +0.001275 and Δdissociation +0.002776) is a specific prediction to test, not assumed truth.

## H2 [tentative; prospective]
The precipitation proxy may rise with concentration/loading, possibly with a threshold or saturation; loading and concentration may remain observationally equivalent unless same-concentration/different-total-loading points differ.

## Design decision
Use water at nominal ambient conditions across a 3×4 grid: volumes 0.018, 0.036, 0.054 L and reagent amounts 0.0005, 0.001, 0.004, 0.020 mol. Each independent batch gets one pre-termination pH-meter reading and the required post-termination final assay. This tests dilution at fixed loading, concentration effects, threshold curvature, and total-loading alternatives. Interpret differences against declared channel noise and cross-instrument repeatability; do not treat equilibrium diagnostics as scientific confidence.

## Revision 2

Recorded: 2026-10-13T12:51:23.573289+00:00; available public operations: 60; reviewed through: runner-operation-0060.

# Hypothesis notebook

## H1 [supported in this bounded water/ambient scope]
The joint pH–dissociation observations are well summarized by an effective monoprotic relation, `pKa_eff = pH - log10(alpha/(1-alpha))`. Across the 12 final assays this derived quantity averages about 5.195 (observed range 5.091–5.300), consistent with the archival 80% interval 5.149–5.249 in central tendency. This is an effective observational relation, not identification of a real acid or proof of a unique microscopic mechanism.

At fixed 0.001 mol, dilution 0.018→0.054 L changed final pH_normalized by +0.001162 and dissociation fraction by +0.004142 (events runner-operation-0010 and runner-operation-0050). The archival predictions were +0.001275 and +0.002776. Both discrepancies are small relative to the declared final-assay channel noise, so this experiment supports rather than revises the local relationship.

Across concentrations 0.00926–1.111 mol/L, a descriptive least-squares fit versus natural log concentration gave dissociation `alpha ≈ 0.06350 - 0.004006 ln(C)`. The corresponding pH_normalized slope was only -0.000955 per ln(C), with visible non-monotonic deviations; treat this as a local summary, not a universal law. Evidence spans final assays runner-operation-0005 through runner-operation-0060.

## H2 [no resolved concentration effect]
The precipitation proxy remained near 0.15 without an ordered loading/concentration trend; its fitted slope versus ln(C) was about +0.000038. Values ranged roughly 0.140–0.166, but single-point differences are not evidence of a threshold given declared assay noise and lack of condition replication. Thus the prospective threshold claim is unsupported in this sampled domain, not proven absent.

## H3 [total-loading alternative unresolved but constrained]
A same-concentration comparison at C=0.02778 mol/L—0.0005 mol/0.018 L versus 0.001 mol/0.036 L (runner-operation-0005 vs runner-operation-0030)—showed small differences in all three target channels relative to combined instrument noise. Concentration-only and total-loading-dependent explanations are therefore observationally equivalent at this tested pair; a strong total-loading effect is not indicated.

## Measurement interpretation and scope
Paired pH-meter readings were noisier and sometimes differed visibly from final assays, as expected from declared uncertainties; final assays anchor numerical conclusions. Equilibrium residuals were almost always at the zero boundary and equilibrium_confidence varied, but these are environment diagnostics and were not optimized or used as scientific confidence. Conclusions apply only to water, nominal ambient conditions, instantaneous equilibrated snapshots, and the tested loading/volume grid.

## Testable consequences
Additional replicated final assays should reproduce the 0.001 mol dilution sign and keep derived pKa_eff near ~5.2. Resolving any precipitation threshold or separate total-loading term requires deliberate replicates and more same-concentration/different-total pairs; systematic departures beyond measurement scatter would change H2/H3.
