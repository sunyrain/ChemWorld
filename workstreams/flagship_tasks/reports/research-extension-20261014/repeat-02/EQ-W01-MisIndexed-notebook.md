# repeat-02 / EQ-W01-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T17:29:46.366830+00:00; available public operations: 0; reviewed through: None.

# Aqueous-equilibrium hypotheses

## H1 [tentative; pre-experiment]
For water-only batches near 298 K, increasing anonymous reagent loading at fixed liquid volume should lower pH and reduce the acid dissociation fraction if it behaves as a bounded weak monoprotic acid. At fixed total loading, dilution from 0.018 to 0.054 L should slightly raise both pH and dissociation; the archival expectation for 0.001 mol is ΔpH_normalized ≈ +0.000876 and Δfraction ≈ +0.001885.

## H2 [tentative; pre-experiment]
If concentration is the principal state variable, batches with proportional total loading and volume should agree in pH and dissociation within measurement variability. Persistent differences would support an amount-, volume-, or path-dependent alternative.

## H3 [tentative; pre-experiment]
The precipitation proxy may show a concentration-dependent onset or saturation; paired equal-concentration conditions at different absolute scales and repeats will test whether that interpretation is distinguishable from total-amount or measurement-noise explanations.

Planned scope: water-only, ambient uncontrolled conditions, reagent 0.001–0.036 mol, liquid volume 0.018–0.054 L. Final assays are authoritative; one pH-meter snapshot per batch provides a noisier cross-check. Claims will remain bounded to this domain.

## Revision 2

Recorded: 2026-10-13T17:31:08.766834+00:00; available public operations: 45; reviewed through: runner-operation-0045.

# Aqueous-equilibrium hypotheses

## H1 [unresolved / narrowed]
Across water-only final assays spanning 0.001–0.018 mol and 0.018–0.054 L, pH_normalized remains near 0.251–0.258 and acid dissociation near 0.062–0.089 (final-assay events runner-operation-0005 through runner-operation-0045). The numerical shifts are not monotone in loading and are comparable to cross-batch scatter, so the predicted weak-acid loading trend is not established. The archival 0.001-mol dilution change is much smaller than observed assay scatter: the endpoint difference between 0.018 and 0.054 L is opposite in sign for pH_normalized and only +0.0041 for fraction (runner-operation-0005 vs runner-operation-0015). This does not cleanly reject such a tiny local effect because batches are independent and measurement noise is nonzero, but it does reject treating the archival point estimate as resolved by this design.

## H2 [provisionally supported only as invariance]
Equal-concentration pairs at 0.0556, 0.1667, and 0.5 mol/L do not show a consistent absolute-scale dependence in the final channels (runner-operation-0005 vs -0030; -0020 vs -0035; -0025 vs -0040). However, broad response invariance also fits a weakly coupled or misidentified loading variable, so concentration control is not uniquely identified.

## H3 [not supported over sampled range]
Final precipitation_signal stays narrowly near 0.146–0.158 without monotone concentration response through 1 mol/L (runner-operation-0005 to -0045). No onset is resolved. A bounded constant-background/noise explanation remains equivalent to precipitation below an unresolved threshold.

## Measurement confound
Single pH-meter readings are noisier and sometimes disagree materially with the final assay (e.g. runner-operation-0033 vs -0035), so final assays anchor comparisons. Remaining batches will include a high-concentration scale match and exact repeats to estimate cross-batch repeatability. Claims remain limited to water-only, ambient, immediate snapshots.
