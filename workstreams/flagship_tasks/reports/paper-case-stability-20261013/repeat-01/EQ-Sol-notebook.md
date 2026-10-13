# EQ-Sol — model-authored source notebook

Development replication. Each version is the model's scientific account, not verified environment truth. Posttest answers are separate in the JSON record.

## Revision 1

Recorded: 2026-10-13T04:22:31.601353+00:00; public operations available: 0; reviewed through: not specified.

# Source-stage hypothesis notebook

## H1 [tentative; pre-experiment]
Within the water-only, near-ambient scope, equilibrium responses are expected to be governed mainly by analytical loading concentration (C_T=n/V), rather than absolute moles or volume separately. Matched-concentration pairs should therefore agree within measurement noise.

## H2 [tentative; pre-experiment]
For a weak acid, increasing (C_T) should lower pH while decreasing the dissociated fraction; a mass-action-like local consequence is that (C_T\alpha^2/(1-\alpha)) may be approximately constant where precipitation is negligible. The precipitation proxy may introduce a threshold/nonlinearity at higher loading and break that relation.

## Planned discrimination
Use twelve independent water batches spanning (C_T=0.0625) to (1.0) mol/L, including matched-concentration pairs at 0.125, 0.25, and 0.50 mol/L. Each batch gets a pre-termination pH-meter observation and the required post-termination final assay. Agreement of matched concentrations supports concentration control but cannot distinguish activities from a calibrated effective concentration law; systematic absolute-scale differences would oppose H1.

---

## Revision 2

Recorded: 2026-10-13T04:24:11.636840+00:00; public operations available: 63; reviewed through: runner-operation-0063.

# Source-stage hypothesis notebook

## Scope and evidence base
Twelve independent water-only, near-ambient batches were completed with required final assays. Nominal analytical loadings span about 0.0625–1.0 mol/L. Final assays have stated channel standard deviations of 0.002 (pH/14), 0.006 (dissociation fraction), and 0.006 (precipitation proxy). The pre-final pH-meter draw changes volume only slightly. In batch 12 the planned 0.03 mol addition was rejected for stock limits (runner-operation-0057); its pre-termination pH-meter reading was therefore a water blank and is excluded, while its eventual final assay is valid after a 0.01 mol addition (runner-operation-0063).

## H1 [unresolved / narrowed]
The original concentration-control conjecture is not uniquely identified because the public responses are nearly flat over the entire loading range. Matched nominal concentrations give small and non-systematic final-assay differences:
- 0.125 M, batches 1 vs 7 (runner-operation-0005, runner-operation-0035): Δ(pH/14)=0.00168, Δα=0.00953, Δprecip=0.00155.
- 0.25 M, batches 2 vs 8 (runner-operation-0010, runner-operation-0040): differences 0.00097, 0.00203, and 0.00801.
- 0.50 M, batches 3 vs 10 (runner-operation-0015, runner-operation-0050): differences 0.00262, 0.01129, and 0.00126.
These are comparable to the stated single-assay noise scales rather than repeatable absolute-volume effects. Thus there is no resolved separate dependence on moles or volume, but flat saturation/buffering or an effective hidden background is observationally equivalent to concentration-only control here.

## H2 [rejected in its simple mass-action form]
Across final assays, mean (range) is pH/14 0.25345 (0.24988–0.25603), α 0.07084 (0.06125–0.07944), and precipitation proxy 0.15557 (0.14403–0.16193). Least-squares slopes versus ln(C_T) are small: −0.00107, +0.00211, and +0.00266 respectively. The anticipated monotonic fall in pH and dissociation fraction with loading is not observed; α even has a small positive fitted slope. The diagnostic (C_T\alpha^2/(1-\alpha)) spans 3.56e-4 to 6.25e-3 (17.6-fold), so it is not a constant effective dissociation parameter over this scope.

## H3 [supported descriptively in this scope]
A constant-response description is the simplest effective summary over 0.0625–1.0 M water-only loading: pH ≈3.55 (from 14×mean normalized pH), α≈0.071, and precipitation proxy≈0.156. This is descriptive, not a mechanistic claim. The precipitation channel shows no resolved threshold or monotonic onset. Equivalent explanations include strong background buffering/ionic-strength effects, a saturated bounded response mapping, or channels representing effective proxies rather than an ideal single-acid speciation identity.

## Uncertainty and next tests
Reported ranges include measurement noise and between-batch variation; no new error bar is inferred. More replication at fixed loading and points below 0.0625 M (if permitted) would distinguish a genuinely flat plateau from a weak slope or transition. Independent changes to supporting component, solvent identity, or temperature would test the background/saturation alternatives, but those factors were intentionally held fixed here.

---
