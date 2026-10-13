# repeat-02 / EQ-W03-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T17:11:19.611623+00:00; available public operations: 0; reviewed through: None.

# Pre-experiment hypotheses

**H1 [tentative]** Within the supplied weak-acid scope, increasing dilution at fixed acid total should slightly increase both pH and dissociation fraction. For 0.001 mol diluted from 0.018 to 0.054 L near 298 K, the archival prediction is approximately +0.00349 in pH/14 and +0.00819 in dissociation fraction. A paired test will check this.

**H2 [tentative]** At fixed liquid concentration, changing total moles and volume proportionally should produce similar pH and dissociation; any reproducible departure would indicate a total-loading or precipitation coupling.

**H3 [tentative]** The precipitation proxy should be low at dilute loading and increase nonlinearly above an effective concentration/loading boundary. Concentration and total amount may be observationally confounded, so matched-concentration pairs and a broad concentration series are planned.

Measurement differences will be interpreted against the instruments' declared noise and replication rather than treated automatically as effects.

## Revision 2

Recorded: 2026-10-13T17:12:23.451118+00:00; available public operations: 20; reviewed through: runner-operation-0020.

# Working hypotheses after batches 1–4

**H1 [supported locally, still noisy]** For 0.001 mol acid, dilution from 0.018 to 0.054 L increased final-assay pH/14 by about 0.00385 and dissociation fraction by about 0.00546 (final events runner-operation-0005 and runner-operation-0010). The pH change closely matches the archival +0.00349 prediction; the dissociation change has the predicted sign but is smaller than +0.00819. Given declared single-assay noise, this is consistency evidence rather than precise validation.

**H2 [provisionally supported]** Matched concentration near 0.0333 mol/L at different scale (0.001 mol/0.030 L versus 0.002 mol/0.060 L) gave close final responses: pH/14 0.27952 vs 0.28074 and dissociation 0.06457 vs 0.07429 (runner-operation-0015, runner-operation-0020). The numerical alpha difference is not yet decisive relative to assay noise; a pure concentration-controlled explanation remains viable.

**H3 [unresolved]** Final precipitation proxy remained near 0.145–0.155 across these dilute batches. Higher concentration/loading is required to locate any nonlinear boundary. Intermediate pH-meter readings sometimes differ materially from final assays, so cross-instrument differences are treated as measurement-method/noise confounding, not temporal chemistry.

## Revision 3

Recorded: 2026-10-13T17:14:41.836222+00:00; available public operations: 61; reviewed through: runner-operation-0061.

# Final source-stage interpretation (12 completed batches)

**H1 [supported only as a local delta; supplied pKa interval rejected under the usual fraction mapping]** The 0.001 mol, 0.018→0.054 L cross-batch comparison changed final pH/14 by +0.00385 and dissociation fraction by +0.00546 (runner-operation-0005 vs runner-operation-0010), broadly consistent in sign and scale with the archival +0.00349/+0.00819 local dilution delta. However, applying the ordinary monoprotic relation pKa = pH − log10(alpha/(1−alpha)) to all final measurements gives apparent values 4.954–5.098 (mean 5.015), outside the supplied 80% interval 4.609–4.709. Thus the archival delta can remain locally predictive while its stated pKa interval is not supported by these public channels. Equivalent explanations include nonideal/activity effects or a calibrated dissociation proxy not identical to a thermodynamic species fraction.

**H2 [supported in tested aqueous scope]** Concentration dominates any scale effect that is identifiable here. Matched-concentration pairs at about 0.033, 0.133, and 0.8 mol/L showed final pH/14 pair differences 0.0012, 0.0029, and 0.0012; dissociation differences 0.0097, 0.0057, and 0.0067 (events runner-operation-0015/0020, 0025/0030, 0050/0055). These are comparable to declared assay noise and empirical pair scatter, so no separate total-mole effect is resolved.

**H3 [weak concentration trend, not a universal law]** Across nominal concentrations about 0.0083–0.8 mol/L, an exploratory least-squares fit versus ln(C) gave pH/14 ≈ 0.27787 − 0.000764 ln(C/M) and alpha ≈ 0.06941 − 0.00194 ln(C/M). The endpoints favor higher pH and dissociation on dilution, but replicate scatter and sparse low-concentration coverage preclude a precise law. The conventional ideal weak-acid concentration response is much stronger than observed, reinforcing that these are effective bounded channels.

**H4 [no resolved precipitation boundary]** Final precipitation signals stayed about 0.145–0.167 and an exploratory slope versus ln(C) was only +0.00031. Matched pairs scatter by up to ~0.009, comparable to the declared 0.006 assay noise, so neither concentration nor total amount has a resolved precipitation effect over this design. A threshold outside the tested range, a nearly constant background, and a weak masked dependence remain equivalent explanations.

**Staged dilution caveat.** Batch 12 compared a pre-dilution pH-meter reading at ~0.5 M (runner-operation-0058) with a post-dilution final assay at ~0.167 M (runner-operation-0061); the direction opposed H1. Because instrument and stage changed together, this does not isolate dilution and is not used to overturn the cleaner final-assay anchor pair.

**Scope/next test.** Conclusions apply to water near 298 K, nominal 0.008–0.8 M loading, 0.0005–0.040 mol, and 0.018–0.060 L final volumes. A decisive follow-up would use the same instrument before and after dilution with replicated matched-concentration controls, plus concentrations beyond this range if legal, to separate dilution, total loading, and any precipitation threshold.
