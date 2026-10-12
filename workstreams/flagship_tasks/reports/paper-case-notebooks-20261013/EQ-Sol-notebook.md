# EQ-Sol — model-authored source notebook

Development replication. Each version is the model's scientific account, not verified environment truth. Posttest answers are separate in the JSON record.

## Revision 1

Recorded: 2026-10-12T17:34:04.108761+00:00; public operations available: 0; reviewed through: not specified.

# Source-stage hypotheses

## H1 [tentative; pre-experiment]
In water near ambient conditions, pH and acid dissociation should depend primarily on analytical loading concentration (total reagent amount/liquid volume), while the precipitation proxy may show a threshold-like increase at higher concentration rather than a smooth loading-only trend. Equal-concentration preparations at different absolute scales should be similar within measurement variability; dilution at fixed amount should raise dissociation and may lower precipitation. A concentration mismatch, solvent identity effect, or persistent absolute-amount effect would revise this claim.

## Design decision
Use twelve independent water batches spanning concentration and including equal-concentration scale pairs and local repeats. Spend one nonfinal pH measurement per batch before termination, then all required final assays. Treat final-assay noise as stated and do not use equilibrium diagnostics as epistemic confidence.

---

## Revision 2

Recorded: 2026-10-12T17:35:34.213244+00:00; public operations available: 72; reviewed through: runner-operation-0072.

# Source-stage hypotheses and conclusions

## H1 [not supported as a resolved trend in this scope]
**Pre-experiment claim:** in ambient water, concentration (amount/volume) would systematically shift pH and dissociation, and high concentration might increase precipitation. Across 0.10–0.70 mol/L, the final-assay linear descriptive slopes were only −0.00454 pH_normalized per mol/L, +0.01099 dissociation fraction per mol/L, and −0.00039 precipitation-signal per mol/L. These changes across the tested span are small relative to between-batch scatter and the declared per-assay noise (0.002, 0.006, 0.006 respectively), so they do not establish the predicted effects. Evidence: final assays runner-operation-0006 through runner-operation-0072 at six-operation intervals.

## H2 [supported only as an effective bounded description]
At ambient temperature in water over 0.10–0.70 mol/L, the public chemical channels are approximately flat: pH_normalized is near 0.25 (pH about 3.5), dissociation near 0.07, and precipitation proxy near 0.15–0.16. Group means at 0.20, 0.40, and 0.50 mol/L respectively were: pH_normalized 0.25436, 0.25239, 0.25341; dissociation 0.07031, 0.07232, 0.07025; precipitation 0.15556, 0.15449, 0.15308. This is an empirical local description, not evidence that the quantities are exactly invariant or mechanistically uncoupled.

## H3 [scale equivalence plausible but not proven]
Equal-concentration preparations at different absolute scales did not show a consistent monotonic volume/amount effect. The 0.20 mol/L triplet (runner-operation-0012, -0048, -0054) and 0.40 mol/L triplet (-0018, -0036, -0042) contain scatter, including a low precipitation value at the smallest 0.40 mol/L volume, but the analogous 0.20 mol/L series is nonmonotonic. Thus concentration-only equivalence remains a parsimonious explanation; an absolute-scale effect and batch variability remain observationally equivalent with these data.

## H4 [repeatability limits]
The direct 0.50 mol/L repeat pair (runner-operation-0066 and -0072) differed by 0.00247 in pH_normalized, 0.01484 in dissociation, and 0.00023 in precipitation. Relative to declared single-assay noise, precipitation repeated closely while dissociation showed appreciable batch-to-batch spread. One pair is insufficient to assign a process error bar. The nonfinal pH-meter readings were noisier and sometimes disagreed with final assays; conclusions therefore anchor on required final assays.

## Scope, alternatives, and next test
No solvent, temperature, ionic-strength, or time perturbation was made; conclusions apply only to independently prepared ambient water batches and cannot distinguish a buffered/saturated regime from weak true concentration dependence masked by batch/instrument variation. A follow-up should add replicated dilution trajectories within the same vessel and more independent repeats at 0.20, 0.40, and 0.50 mol/L. A reproducible response larger than stated measurement variability and monotonic across dilution would overturn the approximate-flat effective model. Equilibrium residual/confidence are retained only as environment diagnostics, not scientific certainty.

---
