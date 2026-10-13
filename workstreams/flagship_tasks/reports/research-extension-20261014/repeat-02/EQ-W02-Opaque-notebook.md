# repeat-02 / EQ-W02-Opaque — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T12:13:18.056476+00:00; available public operations: 0; reviewed through: None.

# Pre-experiment hypotheses

**H1 [tentative].** In water at fixed temperature, pH and dissociation should depend primarily on analytical loading concentration (total reagent moles/liquid volume), while the precipitation proxy may rise nonlinearly above a concentration threshold. Equal-concentration batches at different total volume should therefore agree within measurement noise; dilution at fixed moles should increase dissociation and may reduce precipitation.

**Plan/decision rule.** Map a concentration series, include equal-concentration volume pairs and replicates, and use one intermediate pH measurement per batch when useful. A systematic volume effect among concentration-matched batches would reject concentration-only H1; large replicate scatter would limit claims. Anonymous component/catalyst effects are outside the primary scope unless needed to distinguish alternatives.

## Revision 2

Recorded: 2026-10-13T12:14:23.014950+00:00; available public operations: 35; reviewed through: runner-operation-0035.

# Working hypotheses after batches 1–7

**H1 [narrowed].** Across nominal water loadings 0.10–0.60 mol/L, pH shows at most a shallow decrease with loading (final pH_normalized about 0.269 near 0.2–0.4 M versus about 0.264 at 0.5–0.6 M), not a large weak-acid dilution response. Final acid-dissociation fraction (~0.066–0.078) and precipitation proxy (~0.147–0.162) have no resolved monotonic trend relative to their declared final-assay noise. Evidence: final assays runner-operation-0005, -0010, -0015, -0020, -0025, -0030.

**H2 [supported locally, provisional].** Concentration, rather than total volume, is sufficient for the tested 0.20 M condition: 0.010 mol/0.050 L and 0.016 mol/0.080 L give similar final channels (runner-operation-0010 and -0035). One comparison is not repeatability evidence, and the acid-fraction difference could be noise.

**Measurement confound.** Within-batch pH-meter versus final-assay acid fraction differences are sometimes larger than the final instrument noise alone; instruments have different stated noise and independent draws, so cross-instrument deltas are not interpreted as time effects.

**Next tests.** Add a second 0.20 M volume condition, a 0.40 M replicate, and extend to 0.05 and 0.8–1.0 M. A reproducible sharp precipitation rise or pH curvature at the extremes would revise the near-flat local description.

## Revision 3

Recorded: 2026-10-13T12:15:19.353081+00:00; available public operations: 60; reviewed through: runner-operation-0060.

# Source-stage synthesis (12 completed water batches)

**H1 [rejected in strong form; weak trend unresolved].** Over nominal analytical loading 0.05–1.0 mol/L, there is no strong loading response in the three chemical channels. Final pH_normalized spans 0.2637–0.2691 (mean 0.2664; pH about 3.73), acid fraction spans 0.0614–0.0862, and precipitation proxy spans 0.1469–0.1630 (final assays runner-operation-0005 through -0060). Descriptive least-squares slopes versus ln(C/M) are −0.00047 for pH_normalized, −0.00414 for acid fraction, and +0.00227 for precipitation proxy. These are not asserted effects: replicate scatter and declared assay noise are of similar scale, and no uncertainty interval was fitted.

**H2 [supported in tested scope, not uniquely mechanistic].** Total volume is not separately identifiable from concentration within the 0.20 M matched set: 0.010/0.050, 0.016/0.080, and 0.008/0.040 mol/L batches (runner-operation-0010, -0035, -0040) overlap broadly, although the 0.080 L acid-fraction result is higher and its precipitation result lower. This could be independent measurement noise or an unmodeled volume effect; more replicate matched sets would distinguish them.

**H3 [supported locally].** The 0.40 M repeat (runner-operation-0020 and -0045) agrees to ~0.0031 pH_normalized, ~0.0029 acid fraction, and ~0.0049 precipitation signal, consistent with a nearly flat response and modest stochastic scatter at the center of the range.

**Equivalent explanations / limits.** The data support only an effective near-constant mapping under immediate, ambient, pure-water preparation. They do not distinguish buffered chemistry, saturation/solubility pinning, a fixed-background weak-acid equilibrium, or a benchmark response dominated by a hidden background. No time, temperature, nonaqueous-solvent, or electrolyte-profile dependence was tested. pH-meter/final-assay differences are cross-instrument noise, not kinetics. Equilibrium diagnostics were recorded but not optimized or treated as scientific confidence.

**Prediction in scope.** A new ambient water batch between 0.1 and 0.8 M should have final pH_normalized near 0.266, acid fraction near 0.07, and precipitation proxy near 0.155, with uncertainty at least comparable to the observed spreads and declared sensor noise. A replicated shift much larger than those spreads, or a consistent matched-concentration volume trend, would overturn the near-flat/volume-independent description.

**Recommendation decision.** Use batch 9 (0.020 mol in 0.050 L, 0.40 M) as the evidentiary anchor because it is a central-range direct repeat of batch 4 and therefore connects the inferred mapping to an internal repeatability check; this is not an optimization claim.
