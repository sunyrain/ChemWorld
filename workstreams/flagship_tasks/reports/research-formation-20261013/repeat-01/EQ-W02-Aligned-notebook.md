# repeat-01 / EQ-W02-Aligned — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T11:16:30.521537+00:00; available public operations: 0; reviewed through: None.

# Equilibrium characterization notebook

## Pre-experiment commitments (before batch 1)

**H1 [tentative].** In water near 298 K and low loading, dilution of a fixed monoprotic-acid total should raise pH and slightly increase dissociation fraction. For 0.001 mol diluted from 0.018 to 0.054 L, the archival local prediction is ΔpH_normalized ≈ +0.00256 and Δfraction ≈ +0.00581 (effective pKa 4.789–4.889). I will test the exact pair; deviations beyond the displayed measurement noise or failure of direction would weaken it.

**H2 [tentative].** At equal nominal concentration, total amount/volume pairs should give similar pH and dissociation if concentration is the principal identifiable variable. Comparisons 0.001/0.018, 0.003/0.054, and 0.004/0.072 mol/L test this; systematic differences would indicate total-loading, volume, or boundary effects.

**H3 [tentative].** The precipitation proxy may show a concentration/loading threshold rather than follow acid dissociation smoothly. A loading series at 0.020 L and a dilution series at 0.040 mol will locate any bounded transition. Because the proxy is normalized and mechanism mapping is hidden, I will not equate it to a physical precipitated fraction.

Planned scope: water, ambient uncontrolled starting temperature, reagent-only batches. One pre-termination pH-meter reading and one required post-termination final assay per batch; selected replication will assess repeatability. Final conclusions will distinguish sensor-scale numerical differences from evidence given the stated channel noise.

## Revision 2

Recorded: 2026-10-13T11:17:47.768647+00:00; available public operations: 60; reviewed through: runner-operation-0060.

# Equilibrium characterization notebook

## Pre-experiment commitments
**H1 [tentative].** The archival local prediction for 0.001 mol water batches diluted 0.018→0.054 L was ΔpH_normalized ≈ +0.00256 and Δdissociation ≈ +0.00581, with effective pKa 4.789–4.889.
**H2 [tentative].** Equal nominal concentration should give similar pH and dissociation if concentration is the principal variable.
**H3 [tentative].** The precipitation proxy might exhibit a loading/concentration threshold.

## Final source-stage interpretation

**H1 [unresolved, directionally compatible only].** Final assays for the exact pair (events runner-operation-0005 and -0010) changed pH_normalized by +0.00424 and dissociation fraction by +0.01106 on dilution, matching the predicted directions but only modestly exceeding the channels' single-reading noise scales. The replicate of the concentrated endpoint (runner-operation-0060 versus -0005) itself differed by +0.00519 in pH_normalized while dissociation differed by only +0.00014. Thus the archival numerical increments are not independently resolved by this campaign; the direction remains plausible. A fixed-0.040 mol dilution sequence (runner-operation-0040, -0045, -0050, -0055) was not monotone in either response, opposing a claim of a large universal dilution effect across the full tested range.

**H2 [supported only as an approximate bounded description].** At nominal 0.0556 mol/L, final assays for different amount/volume pairs (runner-operation-0005, -0015, -0020, plus replicate -0060) cluster within a few channel-noise scales but are not identical. Across all 12 endpoints, exploratory least-squares slopes versus ln(nominal concentration) were very small: -0.00021 for pH_normalized and -0.00181 for dissociation fraction per log unit. This makes a strong concentration-only law unsupported; total loading/volume effects remain observationally equivalent to measurement scatter and hidden bounded-state effects.

**H3 [not supported in tested scope].** Final precipitation_signal stayed about 0.146–0.163 over nominal concentrations 0.0185–2 mol/L (endpoint events runner-operation-0005 through -0060); its exploratory slope versus ln concentration was +0.00102 per log unit. No resolved threshold appeared. Because this is a bounded proxy, this result does not establish absence of physical precipitation outside the tested water/reagent-only domain.

**Cross-instrument confound.** Pre-termination pH-meter and post-termination final-assay values sometimes differ more than either single sensor's nominal noise (for example runner-operation-0003 vs -0005), despite no chemistry-advancing operation between them. Instrument-specific noise/calibration and sample consumption therefore prevent treating the intermediate/final contrast as kinetics or termination chemistry.

**Decision and scope.** Retain only weak, local claims for water at ambient starting conditions, reagent 0.001–0.040 mol, and initial liquid volume 0.018–0.080 L. A denser replicated dilution series would change the H1 decision if it produced a repeatable monotone shift exceeding endpoint repeatability. Batch 2 is the preferred evidentiary anchor because it is the exact dilute endpoint of the supplied archival comparison; batch 1 and replicate batch 12 provide its necessary concentrated controls.
