# EQ-Sol — model-authored source notebook

Development replication. Each version is the model's scientific account, not verified environment truth. Posttest answers are separate in the JSON record.

## Revision 1

Recorded: 2026-10-13T05:54:38.470775+00:00; public operations available: 0; reviewed through: not specified.

# Pre-experiment commitments

## H1 [tentative]
Within water-only conditions near ambient temperature, equilibrium observables are expected to depend primarily on analytical loading concentration (reagent amount / liquid volume), rather than amount or volume separately. A matched-concentration comparison should therefore agree within measurement variability.

## H2 [tentative]
For a weak acid, increasing analytical concentration is expected to lower pH while lowering the dissociated fraction; dilution should reverse both. A bounded precipitation proxy may rise above a concentration-dependent onset, but its functional form and reversibility are unresolved.

## Planned tests
Use 12 independent aqueous batches spanning roughly 0.06–2 mol/L, including matched concentrations produced from different amount/volume pairs. Use one pre-terminal pH-meter measurement and the mandatory post-termination final assay per batch. Some batches may use staged dilution after the first measurement to test direction/reversibility within a vessel. Numerical differences will not automatically be treated as effects; instrument noise and repeatability will be considered. Temperature and solvent identity will be held near their default/water settings, so conclusions will be scoped accordingly.

---

## Revision 2

Recorded: 2026-10-13T05:56:56.442317+00:00; public operations available: 61; reviewed through: runner-operation-0061.

# Final source-stage interpretation

## H1 [narrowed; supported only as an effective invariance]
Across water-only, near-ambient batches with nominal reagent concentration about 0.0625–2 mol/L, the final-assay channels are effectively flat within the observed scatter. A least-squares descriptive fit versus ln(n/V) gives slopes of about +0.000105 for pH_normalized, +0.000733 for acid_dissociation_fraction, and -0.00165 for precipitation_signal per unit ln concentration. These are small relative to the declared single-assay noise scales and the observed scatter. The 12 final assays (runner-operation-0005, -0010, -0015, -0020, -0025, -0030, -0035, -0040, -0045, -0050, -0055, -0061) average approximately pH 3.55, dissociation fraction 0.0707, and precipitation proxy 0.1556; observed RMS scatter is about 0.00167 normalized pH, 0.00518 fraction, and 0.00505 precipitation.

Matched nominal concentrations made with distinct amount/volume pairs likewise show no reproducible separation in the higher-precision final assay. Thus neither concentration nor amount/volume separately is identifiable as an effect over this tested slice. “Concentration-only control” remains an equivalent parametrization of the null response, not a demonstrated mechanistic law.

## H2 [not supported in this scope]
The preregistered weak-acid expectation that increasing analytical concentration would lower pH and dissociation fraction was not observed over a 32-fold nominal concentration range. The precipitation proxy also showed no resolved onset. This rejects that simple loading-response model for these operations and conditions, but not weak-acid chemistry in untested formulations.

## Measurement and interpretation limits
The pH-meter readings are noisier than final assays as declared, especially for dissociation and precipitation channels, and their numerical excursions were not repeatable in final assays. Batch 12 staged dilution (runner-operation-0058 to -0061) changed both concentration and instrument, so it does not by itself establish reversibility. Plausible observationally equivalent explanations include a fixed/background-buffered equilibrium dominating the public channels, the anonymous limiting reagent not being the acid-active loading variable, or a broad plateau of a bounded response. The experiment cannot distinguish these without changing a chemically active component or measuring the same channel with comparable precision before and after dilution.

## Decision
Use batch 3 (final event runner-operation-0015; 0.020 mol in 0.080 L, nominal 0.25 mol/L) as the evidentiary anchor: its pre-terminal and final measurements closely agree and it lies inside, rather than at the edge of, the tested concentration range. This is an anchor selection, not an optimization claim. A future result showing reproducible changes larger than instrument scatter under matched-instrument staged dilution, or after varying the active anonymous component, would change the effective-invariance conclusion.

---
