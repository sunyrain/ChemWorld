# repeat-02 / EQ-W04-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T17:18:32.564530+00:00; available public operations: 0; reviewed through: None.

# Source-stage hypotheses

## H1 [tentative; prospective]
For aqueous weak-acid loading at fixed temperature, greater total concentration should lower pH while the dissociated fraction should fall; dilution should reverse both. The precipitation proxy may rise above a concentration/loading threshold, but whether it tracks total concentration, dissociated species, or absolute amount is unresolved.

## Planned discriminations
Use a concentration series spanning load and volume, matched-concentration pairs with different absolute amounts, and selected replicates. Before observing data, I expect matched concentrations to give similar pH/dissociation; a difference in precipitation at matched concentration would support amount/volume dependence beyond concentration. Final-assay noise means isolated small differences will remain unresolved; replication and broad contrasts will be weighted more strongly.

## Revision 2

Recorded: 2026-10-13T17:19:59.102424+00:00; available public operations: 50; reviewed through: runner-operation-0050.

# Source-stage hypotheses

## H1 [not supported for nominal reagent loading in tested scope]
The prospective weak-acid expectation was not borne out by the broad water/reagent series. Across final assays at nominal concentrations 0.0185–0.60 mol/L, pH_normalized, dissociation fraction, and precipitation proxy remained near ~0.29, ~0.06–0.08, and ~0.15 rather than changing monotonically (events runner-operation-0010 through runner-operation-0050). The archival 0.001 mol dilution contrast (events runner-operation-0005 and -0010) was small and did not reproduce its stated direction for dissociation; given assay noise and lack of replication, the local prior is unresolved rather than decisively falsified.

## H2 [tentative; prospective test]
A labeling/indexing alternative is now plausible: `add_reagent` may not be the effective acid-loading coordinate, while component 0 may carry the bounded equilibrium response. In batches 11–12 I will hold water volume at 0.060 L and vary component 0 from 0.012 to 0.036 mol. A large ordered pH/dissociation or precipitation contrast would support H2; another near-flat contrast would leave an invariant/buffered model or hidden baseline as alternatives.

## Scope and confounds
Final assays are prioritized over noisier intermediate pH-meter values. Absolute amount and concentration are partially confounded in the broad series, although matched nominal concentration batches 1 and 3 showed broadly similar final responses. Temperature and solvent identity were held near 298 K and water, so no generalization beyond that slice is intended.

## Revision 3

Recorded: 2026-10-13T17:20:56.605419+00:00; available public operations: 60; reviewed through: runner-operation-0060.

# Source-stage hypotheses

## H1 [unsupported as a sizeable nominal reagent-loading law in this slice]
At ~298 K in water, ten final assays spanning nominal reagent concentration 0.0185–0.60 mol/L did not show a clear monotonic response (events runner-operation-0005 to -0050). Descriptive linear fits versus concentration were shallow: pH_normalized ≈ 0.29190 − 0.00331 C, dissociation fraction ≈ 0.07577 − 0.01980 C, and precipitation_signal ≈ 0.15425 − 0.00042 C (C in mol/L). These are descriptive, not mechanistic fits or significance claims. The corresponding series means were 0.2911, 0.0710, and 0.1542. Scatter and stated assay noise preclude treating the small slopes as established effects.

The supplied archival dilution estimate at 0.001 mol predicted increases of 0.00256 in pH_normalized and 0.00581 in dissociation fraction from 0.018 to 0.054 L. Final events runner-operation-0005 and -0010 differed by +0.00138 and −0.00141, respectively. Thus the pH contrast had the predicted sign but smaller magnitude, while dissociation had the opposite sign; one noisy pair is insufficient for firm rejection, so the archival local relationship is unresolved and not supported by this campaign.

## H2 [not supported by the tested indexing alternative]
At fixed 0.060 L water, component-0 loads 0.012 and 0.036 mol also produced similar final states (events runner-operation-0055 and -0060): no large ordered shift appeared in pH, dissociation, or precipitation. The prospective indexing alternative therefore lacks support from this two-point test.

## Best current effective description and equivalent explanations
Within the examined water/298 K domain, the most defensible effective description is an approximately buffered/invariant final response near pH_normalized 0.29 (pH ≈ 4.1), dissociation fraction 0.07, and precipitation proxy 0.15. This does **not** identify a unique mechanism. Equivalent explanations include a dominant fixed acid/background buffer, saturation/clipping of the response, nominal additions not coupling to the measured acid pool, or effects smaller than run-to-run/process variability. Intermediate pH-meter observations sometimes differed materially from final assays in the same batch (for example runner-operation-0053 vs -0055 precipitation); destructive sampling, instrument/process proxies, and timing make cross-instrument discrepancies a confound rather than evidence of kinetics.

## Scope, uncertainty, and next tests
Claims apply only to water, near 298 K, immediate equilibrium snapshots, and the tested amount/volume range. No general solvent or temperature law was tested. Replicated archival-anchor dilutions, within-batch staged dilution measured by the same instrument, and independent variation of absolute amount at tightly matched concentration would distinguish a weak true dilution law from run variability. A direct component-plus-reagent factorial would further test indexing/coupling. A reproducible ordered shift exceeding ordinary replicate scatter would change the invariant-description decision.
