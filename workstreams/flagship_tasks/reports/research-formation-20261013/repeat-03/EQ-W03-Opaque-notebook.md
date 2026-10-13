# repeat-03 / EQ-W03-Opaque — source notebook

Model-authored scientific records, not evaluator truth. Timestamps establish public statements, not private belief or causal influence.

## Revision 1

Recorded: 2026-10-13T12:38:20.890644+00:00; available public operations: 0; reviewed through: None.

# Aqueous-equilibrium hypotheses

## H1 [tentative; pre-experiment]
At fixed water volume, increasing anonymous reagent loading should lower pH and may increase the bounded precipitation proxy; dilution at fixed loading should raise pH, increase weak-acid dissociation fraction, and suppress precipitation. A concentration-like loading/volume variable may collapse both manipulations, but an independent total-loading term (e.g. finite-capacity precipitation) remains plausible.

**Planned test:** a 4 × 3 grid spanning 0.004–0.036 mol reagent and 0.020–0.080 L water. Each batch will receive one pre-termination pH-meter observation and an independent final assay at the same nominal state. Numerical differences smaller than instrument noise or unsupported by repeats will not be treated as effects.

**Falsifier/narrowing condition:** failure of equal-concentration conditions to agree beyond measurement uncertainty would oppose a concentration-only account and motivate separate amount/volume terms. A nonmonotone response would reject the simple directional expectation.

## Revision 2

Recorded: 2026-10-13T12:39:54.754291+00:00; available public operations: 60; reviewed through: runner-operation-0060.

# Aqueous-equilibrium hypotheses

## H1 [rejected in tested scope]
The pre-experiment directional claim—more reagent lowers pH and raises precipitation, while dilution reverses these changes—was not supported over 0.004–0.036 mol reagent in 0.020–0.080 L water at ambient initial conditions.

Across the 12 final assays (runner-operation-0005 through runner-operation-0060), means were pH_normalized 0.27805 (pH ≈ 3.893), dissociation fraction 0.07049, and precipitation proxy 0.15546. A descriptive linear fit versus amount n (mol) and volume V (L) gave:
- pH_normalized ≈ 0.27862 − 0.0412 n + 0.00442 V;
- dissociation ≈ 0.06181 + 0.213 n + 0.0993 V;
- precipitation ≈ 0.14984 − 0.00179 n + 0.121 V.

Across the tested ranges, these fitted shifts are small relative to single-assay noise and inconsistent with the predicted directions for dissociation/precipitation. They are descriptive, not identified mechanistic coefficients.

## H2 [supported only as a local effective description]
Within this grid, the most defensible model is an approximately invariant acidic state rather than a resolved loading law. Final-assay ranges were 0.27496–0.28154 for pH_normalized, 0.05942–0.08216 for dissociation, and 0.13879–0.16311 for precipitation. Equal-concentration checks did not reveal a separate amount effect: 0.60 mol/L batches 2 and 7 (runner-operation-0010, -0035) nearly matched in pH and precipitation; 0.30 mol/L batches 6 and 11 (runner-operation-0030, -0055) differed modestly but within the combined scale of stated assay noise. However, near-flat responses mean concentration control and independent amount/volume effects are not distinguishable here.

## H3 [unresolved confound]
Pre-termination pH-meter and final-assay estimates at nominally the same state sometimes differed more than their stated channel noise (for example batch 1, runner-operation-0003 vs -0005; batch 12, -0058 vs -0060). Tiny destructive sampling alone is unlikely to explain all discrepancies. Instrument-specific bias, batch heterogeneity, or unmodeled sampling effects remain equivalent explanations; therefore no cross-instrument pooled precision is claimed.

## Scope and next test
These conclusions apply only to water, the anonymous reagent, ambient no-wait preparation, and the stated loading/volume window. Component 0, cosolvents, time, and temperature were not tested. A decisive follow-up would randomize replicated batches at the extremes and at equal concentration, with replicate assays from one well-mixed state; a reproducible shift exceeding predeclared combined measurement uncertainty would overturn the local-invariance description.
