# EQ-Sol — model-authored source notebook

Development replication. Each version is the model's scientific account, not verified environment truth. Posttest answers are separate in the JSON record.

## Revision 1

Recorded: 2026-10-13T05:21:30.352586+00:00; public operations available: 0; reviewed through: not specified.

# Source-stage hypothesis notebook

## H1 [tentative; pre-experiment]
Within water-only, near-ambient independent batches, equilibrium observables are expected to depend primarily on analytical concentration `C = reagent amount / liquid volume`, not on amount or volume separately. A 3×4 factorial grid (volumes 0.04, 0.06, 0.08 L; matched C values 0.05, 0.15, 0.30, 0.50 mol/L) will test collapse at matched C.

Weak-acid expectation: increasing C should lower pH and lower dissociation fraction; dilution should raise both. Precipitation proxy may rise monotonically or show a threshold with C. Matched-C results that differ reproducibly by volume would oppose concentration-only H1 and suggest finite-amount/geometry or another batch-scale effect.

One pH-meter observation before termination plus the required final assay will provide two independently noisy views per condition; numerical differences smaller than the declared channel noise will not be treated alone as evidence of effects.

---

## Revision 2

Recorded: 2026-10-13T05:23:24.015871+00:00; public operations available: 60; reviewed through: runner-operation-0060.

# Source-stage hypothesis notebook

## H1 [rejected in its directional form; supported only as a null-collapse description]
Pre-experiment, I expected water-only equilibrium responses to be governed mainly by analytical concentration `C=n/V`, with increasing C lowering pH and dissociation and perhaps raising precipitation.

The completed 3×4 factorial grid covered V = 0.04, 0.06, 0.08 L and matched C = 0.05, 0.15, 0.30, 0.50 mol/L (events runner-operation-0001 through runner-operation-0060). Final-assay concentration-group means for (pH_normalized, dissociation, precipitation) were approximately:
- 0.05 M: (0.2557, 0.0723, 0.1562)
- 0.15 M: (0.2532, 0.0707, 0.1542)
- 0.30 M: (0.2536, 0.0760, 0.1568)
- 0.50 M: (0.2528, 0.0678, 0.1547)

Thus a tenfold loading change produced only about -0.0029 normalized pH (-0.040 pH unit), with no monotone dissociation or precipitation change. Matched-C results also showed no consistent volume ordering. The appropriate bounded conclusion is near-invariance over this grid, not proof of exact equality; individual final-assay noise is declared as 0.002, 0.006, and 0.006 for these channels, and only three volume replicates occur at each C.

## H2 [rejected for this operational definition of total loading]
A simple unbuffered monoprotic weak acid in which added-reagent concentration is the acid analytical concentration predicts roughly a -0.5 pH-unit change per decade in the low-dissociation regime and a substantial decline in dissociation with C. The observed decade change is about -0.04 pH unit and dissociation remains near 0.07 (endpoint group means 0.0723 vs 0.0678), so that model is not an adequate identifiable explanation here.

An apparent Henderson-type pKa computed separately from final pH and dissociation averages about 4.67 (range about 4.57–4.74), but this does not rescue the mass-balance model because both measured quantities are nearly invariant while nominal C changes. Equivalent explanations remaining open are an unobserved buffer/support formulation, a fixed activity background, added reagent not equaling the full acid pool, or bounded-channel behavior. The experiment cannot distinguish these.

## H3 [supported as a scoped empirical statement]
At near-ambient conditions, water solvent, immediate measurements, and C=0.05–0.50 M, the precipitation proxy is approximately flat near 0.155 with scatter comparable to measurement noise; no threshold was resolved. A threshold could lie outside the tested interval, or the proxy could report a background/plateau rather than precipitated moles. Testing lower/higher C (if legal), equilibration time, or direct dilution trajectories would distinguish these alternatives.

The pre-termination pH-meter and final assay do not behave as exact replicates: pH broadly agrees, while dissociation and precipitation sometimes differ by more than one channel's stated noise (e.g. events runner-operation-0023/0025 and runner-operation-0033/0035). Because the meter and final assay have different noise models and the meter consumes sample, I treat them as concordance checks rather than pool them as interchangeable replicates.

Equilibrium residual is at/near its nonnegative floor in most final assays and therefore has limited discriminatory power. Equilibrium confidence varied with condition but is explicitly an environment diagnostic, not scientific uncertainty or a target; it is not used to support H1–H3.

## Scope and next decision
Claims apply only to anonymous reagent in water, the tested loading/volume grid, near-ambient immediate snapshots, and these public proxy channels. The strongest next test would independently vary background formulation or perform staged dilution with repeated chemistry measurements. A reproducible pH shift substantially exceeding the declared resolution, with dissociation changing consistently under dilution, would overturn the near-invariance statement.

---
