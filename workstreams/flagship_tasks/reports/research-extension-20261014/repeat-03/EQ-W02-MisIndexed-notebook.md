# repeat-03 / EQ-W02-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T17:52:40.285541+00:00; available public operations: 0; reviewed through: None.

# Equilibrium characterization notebook

## Prospective expectations (before physical work)

**H1 [tentative].** In water near 298 K, the supplied local acidity prior is approximately valid at 0.001 mol: increasing liquid volume from 0.018 to 0.054 L should raise pH_normalized by about 0.00127 and acid_dissociation_fraction by about 0.00278. Because these changes are comparable to one final-assay noise scale, independent endpoint comparison plus a staged-dilution batch will be treated as suggestive unless mutually consistent.

**H2 [tentative].** Across a broad loading/concentration grid, pH and dissociation should primarily track analytical concentration (total loading / liquid volume), whereas precipitation_signal may show a nonlinear increase at high concentration or total loading. Competing explanations are dependence on total moles, on volume itself, or on both.

Planned test: twelve independent water batches spanning 0.001–0.040 mol and 0.018–0.054 L, including one replicate and one within-batch staged dilution. Final assays are the principal quantitative evidence; pH-meter readings provide cross-instrument or pre-dilution context. I will revise the grid if early observations show clipping or a sharp transition.

## Revision 2

Recorded: 2026-10-13T17:54:36.886918+00:00; available public operations: 30; reviewed through: runner-operation-0030.

# Equilibrium characterization notebook

## Prospective expectations (written before experiments)

**H1 [tentative].** The supplied local prior predicts, at 0.001 mol, that increasing water from 0.018 to 0.054 L raises pH_normalized by about 0.00127 and dissociation by about 0.00278. These are near one final-assay noise scale.

**H2 [initially tentative; now challenged].** I expected pH and dissociation to track analytical concentration and precipitation to rise nonlinearly at high concentration.

## Interim interpretation through batch 6

Endpoint comparisons span 0.001, 0.004, and 0.012 mol at both nominal 0.018 and 0.054 L (final-assay events runner-operation-0005, -0010, -0015, -0020, -0025, -0030). The 0.001-mol dissociation difference is +0.00275 on dilution, numerically matching the archival increment, but pH_normalized changes -0.00193 rather than +0.00127; each pH difference is comparable to assay noise. At 0.004 and 0.012 mol, dissociation differences are only +0.00105 and +0.00211, while pH differences change sign. Thus the tiny local dilution relationship is not rejected for dissociation, but is not independently resolved; the pH component is not supported by this single pair.

More importantly, increasing loading twelvefold at fixed nominal volume has not produced the large monotonic pH/dissociation shift expected from a simple ideal weak-acid concentration model. Final pH_normalized remains roughly 0.264–0.268 and dissociation roughly 0.066–0.077. Precipitation_signal likewise remains near 0.148–0.173. This challenges H2 and raises alternatives: (A) observables depend weakly on this selectable loading over the tested range, (B) another effective total/component controls acidity, or (C) reported channels are indexed/coupled differently than assumed. The remaining high-loading points and replicate/staged dilution will test whether there is a threshold or reproducible local response. A clear monotonic shift larger than assay noise would restore a loading-response claim.

## Revision 3

Recorded: 2026-10-13T17:57:03.788513+00:00; available public operations: 61; reviewed through: runner-operation-0061.

# Equilibrium characterization notebook

## Prospective expectations (written before experiments)

**H1.** The archival local prior predicts, at 0.001 mol, that dilution from 0.018 to 0.054 L raises pH_normalized by about 0.00127 and dissociation by about 0.00278.

**H2.** I initially expected pH and dissociation to depend primarily on analytical concentration, with precipitation increasing nonlinearly at high concentration.

## Final source-stage interpretation

**H1 [partly numerically reproduced once, but unresolved/revised].** In the first independent 0.001-mol pair, dilution changed dissociation by +0.00275, essentially the archival increment, but pH_normalized by -0.00193, opposite in sign and comparable to assay noise (runner-operation-0005 versus -0010). A second low-loading comparison changed dissociation by -0.00131 and pH_normalized by +0.00164 (runner-operation-0055 versus staged-dilution endpoint -0061). Thus no reproducible directional dilution effect is resolved at the claimed scale. The within-batch staged experiment is useful context because its pre-dilution pH-meter reading is at runner-operation-0058 and its diluted final assay is -0061, but instrument change prevents interpreting that numerical contrast as a pure dilution effect.

**H2 [rejected in its strong form for this bounded selection space].** Reagent batches covered 0.001–0.040 mol, nominal water volumes 0.018 and 0.054 L, and approximate concentrations 0.0185–2.23 mol/L. Across reagent final assays (runner-operation-0005, -0010, -0015, -0020, -0025, -0030, -0045, -0050, -0055, -0061), log-concentration least-squares slopes were only +0.000143 for pH_normalized, -0.00199 for dissociation fraction, and -0.000552 for precipitation_signal per natural-log concentration unit. These are descriptive, not claimed significant effects. Endpoint values remain approximately pH_normalized 0.264–0.269, dissociation 0.066–0.081, and precipitation 0.146–0.173; no monotonic precipitation threshold is evident. Paired volume effects change sign across loading levels.

**H3 [supported as an effective channel relationship, not a molecular mechanism].** Reagent-batch means are pH_normalized 0.26663 (pH about 3.733) and dissociation 0.07293. If the two channels are interpreted with a monoprotic Henderson–Hasselbalch identity, individual endpoint-implied effective pKa values span about 4.775–4.889 with mean 4.838, outside the supplied 5.149–5.249 interval. This discrepancy can mean the archival pKa is inaccurate here, but equivalent explanations remain: public dissociation is an effective bounded response rather than a thermodynamic species fraction; activity/precipitation coupling invalidates the ideal identity; or selectable loading is not the acid-total coordinate assumed by the prior.

**Component/index check [unresolved].** Replacing add_reagent with the sole add_component choice at 0.001 mol gave endpoints in the same broad region (runner-operation-0035 and -0040), without a decisive signature. This neither proves equivalence nor identifies which operation maps to acid total.

**Uncertainty and scope.** Conclusions apply only to water near 298 K, immediate equilibrated snapshots, the tested amounts/volumes, and these public channels. Final-assay stated noise scales are 0.002 (pH_normalized), 0.006 (dissociation and precipitation); observed small differences and sparse replication preclude strong claims below those scales. pH-meter/final-assay contrasts are not interchangeable replicates. equilibrium_confidence is retained only as an environment diagnostic and was not optimized.

**Decision.** Report near-flat empirical responses over the explored grid rather than force the archival dilution law or an ideal weak-acid concentration model. This decision would change with replicated same-instrument dilution differences consistently exceeding measurement noise, or with an independent mapping of the acid-total input coordinate.
