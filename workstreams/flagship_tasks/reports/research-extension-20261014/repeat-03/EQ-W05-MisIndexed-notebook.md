# repeat-03 / EQ-W05-MisIndexed — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T17:43:10.617523+00:00; available public operations: 0; reviewed through: None.

# Source-stage hypotheses

## H1 [tentative; pre-experiment]
Within the supplied bounded aqueous slice, greater total acid loading at fixed water volume should lower pH and reduce dissociation fraction; dilution at fixed acid amount should raise both pH and dissociation fraction. The archival 0.001 mol, 0.018→0.054 L prediction is ΔpH_normalized ≈ +0.00349 and Δdissociation ≈ +0.00819. I will test this locally and across a wider concentration range.

## H2 [tentative; pre-experiment]
Precipitation proxy may depend mainly on concentration (loading/volume), but a threshold/saturation response versus an independent dependence on total amount remains unresolved. A crossed amount–volume design and selected replicates should distinguish these within measurement resolution.

Decisions: use water only, ambient conditions, crossed loadings/volumes, one nonfinal pH-meter reading per batch, then explicit termination and final assay. Treat final assay as primary quantitative evidence and the earlier reading as a within-batch consistency check.

## Revision 2

Recorded: 2026-10-13T17:44:56.045807+00:00; available public operations: 60; reviewed through: runner-operation-0060.

# Source-stage hypotheses and conclusions

## H1 [partly supported locally; broad law unresolved]
For the archival fixed-loading dilution test, 0.001 mol in nominal 0.018 versus 0.054 L, final assays changed pH_normalized from 0.30270 to 0.30928 and dissociation fraction from 0.06472 to 0.07554 (events runner-operation-0005 and -0010). Directions match the prior; observed deltas (+0.00658, +0.01082) exceed but are of similar order to the archival (+0.00349, +0.00819), with assay standard deviations 0.002 and 0.006 per endpoint. This supports the qualitative local dilution response, not exact agreement.

Across the larger crossed design, pH_normalized remains narrowly clustered (~0.3003–0.3093) and dissociation ~0.0647–0.0781. Same nominal concentrations at different total amounts are often close: 0.1667 mol/L endpoints in batches 3 and 6 are especially concordant (events -0015, -0030), and 0.5 mol/L batches 5, 7, 10 have nearly identical dissociation (~0.0737–0.0741; events -0025, -0035, -0050). Yet replicate batch 11 at 0.1667 mol/L differs from batches 3/6 by ~0.012 in dissociation (event -0055), about two single-assay SD, so concentration-only collapse is plausible but not established precisely.

A Henderson–Hasselbalch-style transformation of final pH and dissociation gives apparent pKa values about 5.30–5.42, not the supplied archival 4.609–4.709 interval. This transformation may be invalid because the two public response channels can be effective observables rather than thermodynamically linked species fractions. Decision: reject the archival pKa interval as a direct joint-channel descriptor in this sampled scope, while retaining its qualitative dilution prediction.

## H2 [weak/approximately flat response; threshold unresolved]
Final precipitation_signal spans ~0.1428–0.1612. Equal-concentration sets are reasonably similar: 0.25 mol/L replicates are 0.1531 and 0.1540 (events -0040, -0060); 0.5 mol/L values are 0.1612, 0.1549, 0.1582. The fixed-0.001 mol dilution difference is only -0.00467, smaller than the combined scale implied by two assay SDs. There is therefore no persuasive monotonic dilution or total-loading effect within this design; an approximately flat/plateau response and a shallow concentration response are equivalent explanations at current resolution. A denser low-concentration series with true replicates would discriminate them.

## Measurement/confound decisions
The pH-meter readings are noisier and sometimes visibly disagree with the final assay, consistent with their larger stated channel noise; use final assays as primary evidence and pH-meter readings only as consistency checks. Sampling slightly changes volume, especially in 0.018 L batches, so quoted concentrations are nominal preparation concentrations. Temperature, solvent identity (water), and preparation timing were held fixed; conclusions do not extend to other solvents, temperatures, or named real acids.
