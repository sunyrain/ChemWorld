# repeat-01 / EQ-W04-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T17:00:39.392964+00:00; available public operations: 0; reviewed through: None.

# Source-stage hypothesis notebook

## Pre-experiment expectations (before batch 1)

**H1 [tentative]** Within the bounded aqueous slice, increasing anonymous reagent loading at fixed water volume will lower pH and may increase the acid-dissociation response; dilution at fixed moles should raise pH and, near the archival anchor (0.001 mol; 0.018 to 0.054 L; about 298 K), increase dissociation by roughly 0.006 and normalized pH by roughly 0.0026. This is a prediction from the supplied archival local fit, not yet evidence.

**H2 [tentative]** The precipitation proxy is primarily concentration/loading dependent and may show a bounded onset rather than a simple linear response. Fixed-concentration, different-scale batches can distinguish concentration control from an absolute-mole/volume contribution, but cannot by themselves identify microscopic species.

Plan: use water-only formulations spanning the archival dilution pair, repeats, a concentration series, and fixed-concentration scale comparisons. Each batch will receive one pre-termination pH-meter measurement and the required post-termination final assay. Numerical differences smaller than instrument noise or lacking repeatability will remain unresolved.

## Revision 2

Recorded: 2026-10-13T17:01:43.790586+00:00; available public operations: 20; reviewed through: runner-operation-0020.

# Source-stage hypothesis notebook

## Pre-experiment expectations

**H1 [revised; pH component supported locally, dissociation component unresolved]** The supplied archival dilution prediction was tested twice at each endpoint: 0.001 mol in 0.018 L (final assays: runner-operation-0005, runner-operation-0015) and 0.054 L (runner-operation-0010, runner-operation-0020). Endpoint-mean normalized pH increased by about 0.00260 on threefold dilution, essentially matching the prior +0.00256. Endpoint-mean acid-dissociation fraction instead changed by about -0.00040 rather than the predicted +0.00581; with final-assay per-reading noise stated as 0.006 and only two replicates per endpoint, this does not establish either a small effect or exact invariance. The archival relationship therefore appears partly mis-indexed or otherwise not jointly portable across channels.

**H2 [tentative]** Precipitation proxy may depend on concentration/loading. The same dilution comparison changed the final-assay endpoint mean by about +0.0081 on dilution, but this small two-versus-two difference is not yet strong relative to the stated 0.006 per-reading noise and could reflect an unmodeled scale effect.

Next test: map a wider fixed-volume concentration series, then compare matched concentration at multiple total scales. A monotonic broad response would support concentration control; divergence at matched concentration would support absolute loading/volume or sampling-scale contributions. Microscopic identity remains non-identifiable from these channels.

## Revision 3

Recorded: 2026-10-13T17:02:19.415653+00:00; available public operations: 40; reviewed through: runner-operation-0040.

# Source-stage hypothesis notebook

## H1 [revised; channel-specific archival validity]
At the archival 0.001 mol dilution pair, replicated final assays support the predicted normalized-pH increment (mean change about +0.00260 versus prior +0.00256; runner-operation-0005/0015 compared with 0010/0020). They do not support the predicted dissociation increment: mean change about -0.00040 versus +0.00581, unresolved at stated assay noise. The supplied relationship is therefore not accepted as a single transferable multichannel law; a channel/index mismatch is a live explanation.

## H2 [simple reagent-concentration control rejected over tested range]
At fixed nominal 0.018 L, increasing reagent from 0.001 to 0.016 mol (final assays runner-operation-0005, 0025, 0030, 0035, 0040, with the 0.001 repeat at 0015) produced no monotonic pH, dissociation, or precipitation trend: all stayed in narrow bands compared with the 16-fold loading change. This opposes the original expectation that these observables are primarily controlled by reagent concentration. Alternatives include: reagent amount is not the effective acid-total input; a latent component or buffering/saturation pins the measured slice; or public channels are indexed to another loading variable.

## H3 [new tentative mapping hypothesis]
The sole anonymous `component 0` may be the chemically active loading coordinate for the acid/precipitation slice, whereas `add_reagent` may be largely spectator with respect to these equilibrium channels. Prediction made before testing: component-only or component-spiked batches should shift at least one of pH, dissociation, or precipitation substantially beyond the near-flat reagent-only series. A null component response would instead favor an internally buffered/invariant world.

Decision: retain two matched-reagent-concentration scale tests for absolute-scale confounding, then use the final two batches to test component 0 alone and as a spike. Microscopic identity remains unassigned.

## Revision 4

Recorded: 2026-10-13T17:03:39.438992+00:00; available public operations: 61; reviewed through: runner-operation-0061.

# Source-stage hypothesis notebook

## H1 [supported only for a local pH contrast; rejected as a joint multichannel relationship]
The archival 0.001 mol, 0.018-to-0.054 L dilution contrast was replicated twice per endpoint (final assays runner-operation-0005/0015 versus 0010/0020). Mean normalized pH rose by about 0.00260, matching the supplied +0.00256. Mean acid-dissociation fraction changed by about -0.00040, not the supplied +0.00581, and is unresolved at the stated 0.006 assay noise. Thus the pH contrast is reproducible in this narrow scope, but treating the supplied pair of channel changes as one law is unwarranted; channel/index mismatch, a coincidentally local pH fit, and unidentified effective loading remain equivalent explanations.

## H2 [reagent concentration has little identifiable effect in this tested aqueous slice]
At nominal 0.018 L, reagent loading from 0.001 to 0.016 mol (runner-operation-0005/0015, 0025, 0030, 0035, 0040) gave a fitted normalized-pH slope of only about +0.000094 per natural-log concentration unit and precipitation slope about -0.000145 per unit, amid nonmonotonic scatter. Dissociation showed a weak fitted decline (~-0.00345 per natural-log unit), but sparse singletons and 0.006 per-reading assay noise prevent a firm functional claim. Fixed nominal concentration at different scales (runner-operation-0005/0015, 0045, 0050) likewise did not establish a systematic scale effect; one dissociation value at the largest scale was low, so scale dependence is not excluded.

## H3 [component-as-active-loading hypothesis rejected in tested form]
Component-only 0.001 mol/0.018 L (runner-operation-0055) resembled reagent-only endpoints. A much larger 0.040 mol component spike added to 0.001 mol reagent in 0.018 L (runner-operation-0061) also left final normalized pH, dissociation, and precipitation within the overall reagent-only bands. This directly opposes the predeclared prediction of a substantial component response. It favors a buffered/invariant response surface or an unobserved/mis-indexed effective loading variable over either public amount alone.

## Effective bounded characterization and uncertainty
Across all 12 room-temperature water batches, final-assay pH_normalized was roughly 0.287-0.295, acid_dissociation_fraction roughly 0.059-0.079, and precipitation_signal roughly 0.148-0.162. These are empirical ranges, not confidence intervals. Assay noise is stated as 0.002, 0.006, and 0.006 respectively; repeats were limited and most design points are singletons. The precipitation proxy showed no credible onset through the tested reagent range or the component spike. No microscopic acid identity, solubility product, or unique mechanistic equation is identifiable. Future discrimination should vary any separately exposed true acid-total coordinate, add more endpoint replicates, and randomize scale/concentration independently; a strong monotonic response outside these ranges would overturn the near-invariance claim.

Decision: use batch 12 as the evidentiary anchor because its extreme component perturbation most directly tests and rejects the alternative public-coordinate mapping, not because it optimizes a score.
