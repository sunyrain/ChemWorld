# EQ-W01--Opaque — final public report

World `EQ-W01`; prior arm `Opaque`; status `completed`. The effective result came from `attempt-04`.

## Source campaign

The campaign contains 12/12 completed batches and 60 recorded operations. Exact replay: `True`.

| Batch | pH normalized | Acid dissociation | Precipitation signal | Residual |
|---:|---:|---:|---:|---:|
| 1 | 0.254575 | 0.0617887 | 0.159566 | 0 |
| 2 | 0.255079 | 0.0754151 | 0.161661 | 0.00055434 |
| 3 | 0.252084 | 0.0833798 | 0.157376 | 0 |
| 4 | 0.25357 | 0.0695466 | 0.15899 | 0 |
| 5 | 0.251444 | 0.0771497 | 0.159154 | 0.0042543 |
| 6 | 0.252475 | 0.0701585 | 0.144262 | 0 |
| 7 | 0.25518 | 0.0690095 | 0.16132 | 0.0077023 |
| 8 | 0.252546 | 0.0699998 | 0.153958 | 0 |
| 9 | 0.256123 | 0.0670157 | 0.150918 | 0.000708153 |
| 10 | 0.252368 | 0.0670013 | 0.156581 | 0.00195114 |
| 11 | 0.255029 | 0.0790135 | 0.151474 | 0 |
| 12 | 0.252625 | 0.064317 | 0.151232 | 0.00195465 |

Complete sanitized agent-visible scientific I/O: [trajectory](trajectory.jsonl). Every attempted operation is retained in order; private provider events, credentials, session identifiers, usage accounting, and evaluator-only state are excluded.

## Sealed scientific account

### K1 report

## Mechanistic report

### 1. Scope of the evidence

I completed 12 water-only batches spanning a structured loading–volume matrix:

- Total reagent loading: 0.004, 0.012, 0.024, or 0.040 mol.
- Liquid volume: 0.040, 0.060, or 0.080 L.
- Nominal concentration, defined as total added reagent divided by liquid volume: 0.050–1.000 mol/L.
- Temperature was approximately 297.2 K and pressure was near ambient.
- No catalyst, heating, waiting period, alternate solvent, or deliberate pH adjustment was used.
- Every batch received one in-process pH-meter measurement and one post-termination final assay.

Thus, the report describes only this bounded, aqueous, near-ambient, effectively immediate-response regime. It is not a general model of aqueous chemistry.

### 2. Final-assay observations

The principal final-assay data were:

| Batch | Reagent (mol) | Volume (L) | Nominal loading (mol/L) | pH/14 | Dissociation fraction | Precipitation proxy | Equilibrium residual |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.004 | 0.040 | 0.100 | 0.25457 | 0.06179 | 0.15957 | 0.00000 |
| 2 | 0.004 | 0.060 | 0.0667 | 0.25508 | 0.07542 | 0.16166 | 0.00055 |
| 3 | 0.004 | 0.080 | 0.050 | 0.25208 | 0.08338 | 0.15738 | 0.00000 |
| 4 | 0.012 | 0.040 | 0.300 | 0.25357 | 0.06955 | 0.15899 | 0.00000 |
| 5 | 0.012 | 0.060 | 0.200 | 0.25144 | 0.07715 | 0.15915 | 0.00425 |
| 6 | 0.012 | 0.080 | 0.150 | 0.25248 | 0.07016 | 0.14426 | 0.00000 |
| 7 | 0.024 | 0.040 | 0.600 | 0.25518 | 0.06901 | 0.16132 | 0.00770 |
| 8 | 0.024 | 0.060 | 0.400 | 0.25255 | 0.07000 | 0.15396 | 0.00000 |
| 9 | 0.024 | 0.080 | 0.300 | 0.25612 | 0.06702 | 0.15092 | 0.00071 |
| 10 | 0.040 | 0.040 | 1.000 | 0.25237 | 0.06700 | 0.15658 | 0.00195 |
| 11 | 0.040 | 0.060 | 0.6667 | 0.25503 | 0.07901 | 0.15147 | 0.00000 |
| 12 | 0.040 | 0.080 | 0.500 | 0.25263 | 0.06432 | 0.15123 | 0.00195 |

Across these batches:

- Mean normalized pH was 0.25359, corresponding to pH 3.550.
- The observed final pH range was only 3.520–3.586.
- Mean dissociation fraction was 0.07115, with a range of 0.06179–0.08338.
- Mean precipitation proxy was 0.15554, with a range of 0.14426–0.16166.
- Final equilibrium residuals were zero or very small; the largest was 0.00770 in batch 7.

These are actual final-assay observations. The transformations and equations below are interpretations of them.

### 3. Primary effective relationship: a strongly clamped aqueous state

The dominant empirical feature is insensitivity to total loading and dilution. A twenty-fold change in nominal concentration, from 0.050 mol/L in batch 3 to 1.000 mol/L in batch 10, produced only a 0.00471 change in normalized pH, or about 0.066 pH unit. Dissociation and precipitation likewise remained in narrow bands without a consistent monotonic ordering.

Simple concentration-only descriptive fits to the final assays were:

pH_normalized ≈ 0.25357 + 0.000071 C_nom

alpha ≈ 0.07305 − 0.00525 C_nom

P ≈ 0.15610 − 0.00155 C_nom

where C_nom is the nominal added-reagent concentration in mol/L, alpha is the reported acid-dissociation fraction, and P is the precipitation proxy. These slopes are extremely small over the tested domain and should not be treated as established mechanistic coefficients. A constant-response description is more defensible than a meaningful linear concentration law.

The matched-concentration comparison was especially informative. Batches 4 and 9 both had C_nom = 0.300 mol/L but differed twofold in both total amount and volume:

- Batch 4: 0.012 mol in 0.040 L; pH/14 = 0.25357, alpha = 0.06955, P = 0.15899.
- Batch 9: 0.024 mol in 0.080 L; pH/14 = 0.25612, alpha = 0.06702, P = 0.15092.

Their differences are modest relative to the cross-instrument scatter seen in this campaign. This comparison does not demonstrate a total-amount effect independent of concentration. It was the reason I selected batch 9 as the recommended replay experiment: together with batch 4, it provides the cleanest available test of concentration equivalence.

At the lowest total loading, batches 1–3 showed an apparent increase in alpha with dilution: 0.06179, 0.07542, and 0.08338 as volume rose from 0.040 to 0.080 L. However, this pattern did not reproduce consistently at the other loadings. For example, batches 4–6 gave 0.06955, 0.07715, and 0.07016. I therefore regard the low-loading sequence as suggestive but insufficient to establish a dilution law.

### 4. Weak-acid interpretation

A useful local interpretation is a monoprotic weak-acid-like equilibrium:

HA ⇌ H+ + A−

K_a,app = [H+] alpha / (1 − alpha)

with

[H+] = 10^(−14 pH_normalized).

Applying this transformation separately to the 12 final assays gives apparent K_a values from approximately 1.80×10^−5 to 2.69×10^−5, with a mean of 2.16×10^−5 and an apparent pK_a of about 4.66.

This is the clearest internally coherent coupling in the observations: the narrow pH and alpha ranges are jointly compatible with a nearly constant local weak-acid parameter. I would use the following as an effective interpolation rule inside the observed state window:

alpha ≈ K_a,app / (K_a,app + 10^(−pH)),

with K_a,app approximately 2.2×10^−5 and pH = 14 pH_normalized.

This equation is not proof that the anonymous added reagent is literally a single monoprotic acid. It is an effective relationship among public observables.

If one additionally assumes that the measured hydrogen ion arises solely from dissociation of that acid, then an active dissolved-acid scale can be estimated as

C_active ≈ [H+]/alpha.

The inferred values are approximately 0.00340–0.00452 mol/L, with a mean near 0.00399 mol/L. This is far below every nominal loading tested, including the lowest nominal concentration of 0.050 mol/L. Consequently, a simple model in which all added reagent remains dissolved and directly participates as the measured weak acid is not supported.

### 5. Proposed process picture

My preferred effective picture is:

1. Added material enters an aqueous environment containing, or rapidly establishing, a limited acid-active pool.
2. That pool is locally governed by a weak-acid-like equilibrium with apparent pK_a near 4.66.
3. Over the tested additions, the acid-active dissolved concentration is strongly buffered, capped, partitioned, or otherwise decoupled from the total nominal reagent loading.
4. The public precipitation channel remains near a baseline of about 0.156. It may report a saturated or weakly responsive phase-partitioning state rather than the amount of precipitate on an absolute mass basis.
5. Because the active dissolved state changes little, pH and dissociation also change little as total loading or water volume changes.

A compact phenomenological representation is:

C_nom = n_added / V

C_active ≈ C_cap ≈ 0.004 mol/L

[H+] = alpha C_active

K_a,app = [H+] alpha/(1−alpha) ≈ 2.2×10^−5

P ≈ P_0 + epsilon_P, with P_0 ≈ 0.156

Here epsilon_P represents a small unresolved dependence on loading, volume, phase state, or measurement variation. This is an interpolation model, not a verified microscopic mechanism.

### 6. Precipitation coupling

The precipitation proxy did not show the threshold or monotonic rise one would expect if it directly measured total precipitated mass across the full loading range. For example:

- Batch 2, at only 0.0667 mol/L nominal loading, had the highest final proxy, 0.16166.
- Batch 6, at 0.150 mol/L, had the lowest proxy, 0.14426.
- Batch 10, at the maximum 1.000 mol/L loading, had an intermediate proxy of 0.15658.

Therefore, I reject a simple law of the form P increasing directly with n_added or C_nom over this range. Plausible alternatives are that all tested conditions lie on a plateau beyond an unobserved precipitation threshold, that P is a normalized indicator rather than a mass fraction, or that its small variations reflect another latent state variable.

The nearly constant inferred C_active and nearly constant P are compatible with solubility-limited clamping: excess material could be inactive, sequestered, or precipitated while the dissolved acid-active pool remains fixed. However, because no phase mass, turbidity, solid composition, or dissolved concentration was measured directly, that explanation remains a hypothesis rather than an observation.

### 7. Intermediate measurements and measurement uncertainty

The pH-meter measurements and final assays agreed on the broad state but not point-for-point. Across all 12 batches, final minus intermediate values had:

- Mean alpha difference: +0.00646; RMS difference: 0.01473.
- Mean precipitation-proxy difference: −0.00835; RMS difference: 0.02041.
- Mean normalized-pH difference: −0.000069; RMS difference: 0.00341, equivalent to about 0.048 pH unit.

Examples include batch 7, where alpha changed from 0.09545 on the pH meter to 0.06901 in the final assay, and batch 9, where it changed from 0.04318 to 0.06702. Precipitation differences could also be substantial: batch 6 changed from 0.18649 to 0.14426.

I do not interpret these paired differences as verified reaction kinetics. There was no designed time-course intervention, and the two instruments have different uncertainty characteristics. They instead establish that fine distinctions smaller than roughly 0.01–0.02 in alpha or precipitation proxy are not robustly resolved by this campaign. The much better pH agreement supports the conclusion that pH is genuinely clamped near 3.55.

### 8. How the experiments changed the interpretation

The initial design treated total amount, water volume, and their ratio as potentially separable drivers. The full matrix changed that interpretation in three ways:

1. Batches 1–3 initially suggested that dilution might increase the dissociation fraction at low total loading. The absence of the same ordering in batches 4–12 weakened that explanation.
2. The batch 4 versus batch 9 matched-concentration comparison showed no compelling independent total-amount or volume effect.
3. The extremes—batch 3 at 0.050 mol/L and batch 10 at 1.000 mol/L—showed nearly the same pH and broadly similar alpha and precipitation values. This led me away from an ordinary nominal-concentration-controlled weak-acid model and toward a clamped active-pool model.

The low residuals indicate that the environment regarded most final states as close to its equilibrium manifold, but they do not identify which microscopic mechanism generated that manifold.

The reported equilibrium_confidence values ranged broadly and non-monotonically. They were descriptively highest around some intermediate-loading batches, such as 0.54359 in batch 5, and lower in several high-loading batches, such as 0.37511 in batch 10. Per the task contract, equilibrium_confidence is an environment diagnostic, not my epistemic confidence, so I do not use it as evidence that one mechanistic explanation is more certain than another.

### 9. Competing explanations

Several explanations remain observationally equivalent or nearly so:

**A. Solubility-limited dissolved acid.** A dissolved weak-acid pool is capped near 0.004 mol/L, with excess added material entering a solid or inactive phase. This naturally explains the loading-independent pH and the apparent constant K_a.

**B. Strong background buffering.** The aqueous environment could contain an implicit buffer that fixes pH near 3.55. The reported alpha could then be a calibrated response to that pH rather than a mass-balance fraction of the added reagent.

**C. Small acid-active fraction of the added material.** Only a few percent of nominal reagent may be acid-active, with the remainder remaining neutral, complexed, aggregated, or assigned to another hidden species. A loading-dependent active fraction could conspire to keep C_active approximately constant.

**D. Phenomenological sensor mapping.** The public alpha and precipitation channels may be locally calibrated proxies sharing latent inputs rather than direct measurements of chemically conserved species. In that case the apparent pK_a is a useful empirical invariant but not a literal molecular constant.

**E. Weak true loading effects hidden by noise.** With one batch per matrix cell and appreciable intermediate/final disagreement, small nonlinear loading or volume effects could be present but unresolved. The data reject large effects, not all effects.

### 10. Limits of identification

This campaign cannot identify:

- The molecular identity of the acid-active species or precipitated material.
- Whether precipitate actually formed, its amount, or its composition.
- Whether the inferred active concentration is a solubility limit, buffer capacity, complexation limit, or calibration artifact.
- Independent kinetic or equilibration timescales, because no waits or time series were performed.
- Temperature dependence, pressure dependence, catalyst effects, or solvent effects.
- Behavior below 0.050 mol/L nominal loading, where a saturation or buffering plateau might end.
- Behavior above 1.000 mol/L or outside 0.040–0.080 L.
- Exact separation of total-loading and volume effects beyond the single matched-concentration pair.
- Whether repeated batches at one condition would reproduce the small observed differences.

### 11. Supported conclusions and extrapolations

**Directly supported within the tested domain:**

- The final aqueous state is acidic, near pH 3.55.
- pH is nearly invariant across 0.004–0.040 mol reagent and 0.040–0.080 L water.
- The dissociation fraction is approximately 0.07 and the precipitation proxy approximately 0.156.
- No strong monotonic dependence on nominal loading, total amount, or dilution is visible.
- The pH and dissociation fraction admit a local weak-acid-like relationship with apparent K_a around 2.2×10^−5.

**Reasonable but unverified interpretation:**

- A capped or buffered acid-active pool near 0.004 mol/L controls the public equilibrium observables.
- The precipitation proxy may be on a plateau associated with that clamping.

**Extrapolation or speculation:**

- At nominal concentrations below the tested 0.050 mol/L, the clamp may fail and pH, alpha, and precipitation may become concentration-dependent.
- A precipitation threshold may lie below the tested range.
- Excess reagent may reside in a hidden solid, complexed, or inactive reservoir.

The most defensible final model is therefore a bounded effective equilibrium model: a nearly constant acid-active aqueous state, weak-acid-like coupling between pH and dissociation, and an approximately constant precipitation proxy. It should not be promoted to a unique microscopic mechanism without direct dissolved-species, phase, and below-threshold measurements.

### Blind Q predictions

| Query | Metric | Estimate | 80% lower | 80% upper |
|---|---|---:|---:|---:|
| Q01 | acid_dissociation_fraction | 0.071 | 0.045 | 0.1 |
| Q01 | pH_normalized | 0.2535 | 0.247 | 0.26 |
| Q01 | precipitation_signal | 0.155 | 0.12 | 0.18 |
| Q02 | acid_dissociation_fraction | 0.071 | 0.045 | 0.1 |
| Q02 | pH_normalized | 0.2535 | 0.247 | 0.26 |
| Q02 | precipitation_signal | 0.155 | 0.12 | 0.18 |
| Q03 | acid_dissociation_fraction | 0.33 | 0.12 | 0.48 |
| Q03 | pH_normalized | 0.311 | 0.27 | 0.34 |
| Q03 | precipitation_signal | 0.112 | 0.06 | 0.16 |
| Q04 | acid_dissociation_fraction | 0.108 | 0.06 | 0.19 |
| Q04 | pH_normalized | 0.268 | 0.252 | 0.288 |
| Q04 | precipitation_signal | 0.149 | 0.115 | 0.17 |
| Q05 | acid_dissociation_fraction | 0.071 | 0.05 | 0.095 |
| Q05 | pH_normalized | 0.2535 | 0.248 | 0.259 |
| Q05 | precipitation_signal | 0.156 | 0.13 | 0.18 |
| Q06 | acid_dissociation_fraction | 0.071 | 0.05 | 0.095 |
| Q06 | pH_normalized | 0.2535 | 0.248 | 0.259 |
| Q06 | precipitation_signal | 0.156 | 0.13 | 0.18 |
| Q07 | acid_dissociation_fraction | 0.071 | 0.05 | 0.095 |
| Q07 | pH_normalized | 0.2535 | 0.248 | 0.259 |
| Q07 | precipitation_signal | 0.156 | 0.13 | 0.18 |
| Q08 | acid_dissociation_fraction | 0.699 | 0.25 | 0.9 |
| Q08 | pH_normalized | 0.359 | 0.28 | 0.4 |
| Q08 | precipitation_signal | 0.05 | 0.01 | 0.16 |
| Q09 | acid_dissociation_fraction | 0.301 | 0.12 | 0.45 |
| Q09 | pH_normalized | 0.307 | 0.27 | 0.34 |
| Q09 | precipitation_signal | 0.117 | 0.06 | 0.16 |
| Q10 | acid_dissociation_fraction | 0.071 | 0.045 | 0.1 |
| Q10 | pH_normalized | 0.2535 | 0.247 | 0.261 |
| Q10 | precipitation_signal | 0.164 | 0.11 | 0.23 |
| Q11 | acid_dissociation_fraction | 0.069 | 0.055 | 0.085 |
| Q11 | pH_normalized | 0.2537 | 0.249 | 0.258 |
| Q11 | precipitation_signal | 0.151 | 0.14 | 0.163 |
| Q12 | acid_dissociation_fraction | 0.071 | 0.055 | 0.089 |
| Q12 | pH_normalized | 0.254 | 0.2495 | 0.2585 |
| Q12 | precipitation_signal | 0.16 | 0.148 | 0.171 |

Predictions use the sealed report's effective model: a monoprotic weak-acid-like active pool with apparent Ka about 2.2e-5 and an inferred dissolved-cap scale near 0.004 mol/L. Above that cap, pH_normalized is predicted near 0.2535 and the dissociation fraction near 0.071, largely independent of nominal loading. Below the cap, the estimates use alpha = (-Ka + sqrt(Ka^2 + 4 Ka C))/(2 C) and pH_normalized = -log10(alpha C)/14. The precipitation estimates use a cautious competition extrapolation, decreasing as dissociation dominates, while retaining broad intervals because the public precipitation channel was nearly flat in the observed campaign. Q05-Q07 share point predictions because the available evidence supports an equilibrium state function rather than dosing-order memory. Intervals combine final-assay variability, disagreement between intermediate and final instruments, parameter uncertainty, and additional extrapolation uncertainty; the widest intervals occur for trace-load and extreme-volume cases.

### K2 retrospective

## 1. Initial claims: supported, contradicted, or untested

The initial material packet supplied almost no substantive task-specific chemical claim. It explicitly said that the reagent was anonymous, that no nominal property dossier was available, and that experimental evidence was authoritative. It also described the task as a bounded weak-acid/precipitation slice, defined `pH_normalized = pH/14`, and warned that `equilibrium_confidence` was an environment diagnostic rather than epistemic confidence. Those statements were framing and measurement contracts, not a proposed mechanism.

Several structural claims were respected or supported:

- The observed state was indeed acidic: final pH values were approximately 3.52–3.59.
- The acid-dissociation and precipitation channels were responsive, bounded observables.
- Treating `equilibrium_confidence` as a diagnostic rather than as my confidence was appropriate. In K1 I explicitly avoided using its high values in batches 4, 5, and 9 as proof of a mechanism.
- The weak-acid framing was compatible with the empirical transformation used in K1. Combining pH and dissociation fraction gave an apparent Ka of roughly 1.8–2.7e-5.

However, compatibility is not validation of a literal molecular weak acid. The packet did not claim that all added reagent was a single dissolved monoprotic acid, and the experiments would have contradicted that interpretation. In K1 I noted that the apparent active concentration inferred as `[H+]/alpha` was about 0.0034–0.0045 mol/L, far below every nominal concentration tested. Thus, a model in which all nominal reagent remained dissolved and directly supplied the measured acid equilibrium had positive counterevidence and was explicitly rejected rather than merely lacking support.

The precipitation label did not establish that the signal was proportional to precipitated mass. The non-monotonic observations—such as 0.16166 in low-loading batch 2 versus 0.15658 in maximum-concentration batch 10—were counterevidence to a simple monotonic mass-proxy interpretation. K1 corrected for this by treating the channel as a bounded proxy and describing a plateau only as a possible explanation.

Important issues remained completely untested: molecular identity, actual solid formation, buffer composition, kinetics, temperature dependence, non-water solvents, catalysts, and dosing-order hysteresis. The absence of evidence against these possibilities must not be described as support for their absence.

There was no archival numerical relationship in the supplied material packet for me to validate. The phrase that a local archival estimate might exist did not supply one. Therefore, the apparent Ka and active-pool cap in K1 were derived interpretations, not confirmations of an initial quantitative claim.

## 2. Experiments that formed or changed the judgment

The 4-by-3 amount–volume matrix was chosen before outcome inspection. It used four reagent amounts and three water volumes, giving nominal concentrations from 0.05 to 1.0 mol/L. This choice came mainly from the research question—separating amount, volume, and concentration—not from prior chemical data. The choice to allocate every batch to water, with no catalyst and no waiting period, was an unverified simplification.

The experiments that genuinely affected the interpretation were:

- **Batch 1** established the first local anchor: pH/14 = 0.25457, alpha = 0.06179, and precipitation proxy = 0.15957 at 0.004 mol in 0.040 L.
- **Batches 2 and 3** initially suggested a dilution effect at fixed 0.004 mol: alpha rose from 0.06179 in batch 1 to 0.07542 and 0.08338 as volume increased. At that stage, a conventional dilution-enhanced dissociation account looked plausible.
- **Batches 4–6** weakened that account. At fixed 0.012 mol, alpha was 0.06955, 0.07715, and 0.07016 rather than increasing consistently with volume. This was an actual failure to reproduce the initial ordering, not merely an absence of additional support.
- **Batches 4 and 9** were the most informative concentration-matched pair. Both had 0.300 mol/L nominal concentration, but batch 9 doubled both amount and volume. Their final pH and alpha were close: 0.25357 versus 0.25612 and 0.06955 versus 0.06702. This weakened large independent total-amount or volume effects, although one noisy pair could not prove concentration-only control.
- **Batches 3 and 10** spanned the nominal-concentration extremes, 0.050 and 1.000 mol/L. Their pH values remained close, and neither alpha nor precipitation exhibited the large change expected from a simple all-dissolved weak-acid model. This comparison was central to the clamped-state interpretation.
- **Batch 6** produced the lowest final precipitation signal, 0.14426, at an intermediate nominal concentration. It was important counterevidence to a simple monotonic precipitation law.
- **Batch 7** had the largest final equilibrium residual, 0.00770, and a large intermediate-to-final alpha shift, from 0.09545 to 0.06901. It emphasized measurement and process variability.
- **Batch 9** was selected for the sealed recommendation because it completed the matched-concentration comparison with batch 4, not because it proved an optimum.
- **Batches 11 and 12** supplied useful high-amount anchors for the later predictions, particularly Q11, but did not change the central mechanism much.

The broad matrix itself was a reasonable design for linear amount-versus-volume effects. Its most consequential weakness was that every nominal concentration was above 0.05 mol/L. The inferred active-pool scale emerged near 0.004 mol/L, so the entire campaign may have sampled only one plateau. That limitation was not known when the matrix was fixed, but the choice of minimum loading was nevertheless based on an unverified guess about the informative scale.

Using one intermediate pH measurement per batch was motivated by the instrument allowance and the desire for cross-instrument comparison. Using exactly one final realization per condition, rather than replicating a few mechanistically decisive conditions, was a design choice that favored broad coverage over variance estimation.

## 3. Principal competing mechanisms and current distinguishability

The leading explanations remain:

1. **Solubility-limited active weak acid.** A dissolved acid-active pool is capped near 0.004 mol/L, and excess material is sequestered into a solid, aggregate, complex, or inactive reservoir. The dissolved pool follows an apparent monoprotic equilibrium with pKa near 4.66.
2. **Background buffering.** An implicit aqueous buffer fixes pH near 3.55. The dissociation channel then follows pH or another latent variable without requiring the nominal reagent itself to form a capped dissolved pool.
3. **Loading-dependent active fraction.** The reagent remains present, but only a decreasing fraction becomes acid-active as nominal loading increases. This can reproduce an approximately constant inferred active concentration without literal precipitation.
4. **Phenomenological shared sensor mapping.** The public pH, alpha, and precipitation channels may be calibrated transformations of one or more latent state variables rather than direct, stoichiometrically linked species measurements.
5. **A weak continuous amount–volume response obscured by noise.** The system may not possess a sharp cap at all. The observed flatness could combine shallow trends, nonlinearities, and one-realization measurement variation.

The experiments distinguish these explanations only partially. They disfavor a large direct dependence on nominal concentration within 0.05–1.0 mol/L and disfavor a simple monotonically increasing precipitation signal over that range. They also show that pH and alpha can be summarized by an approximately constant apparent Ka.

They do not distinguish solubility limitation from buffering, complexation, active-fraction adjustment, or a shared proxy mapping. No dissolved concentration or solid mass was measured. The campaign also cannot distinguish a sharp cap from a smooth saturation curve because it never crossed the inferred transition region.

The batch 4–9 pair weakens large independent amount and volume effects at 0.300 mol/L, but it cannot establish global concentration equivalence. The dosing-order equivalence assumed for Q05–Q07 was not experimentally tested at all. Likewise, the sealed prediction that low trace loading would reveal classical weak-acid behavior was a prospective extrapolation, not an observation already obtained during the campaign.

## 4. One additional complete experiment

If allowed exactly one additional legal complete experiment, I would add 0.075 L water and 1e-5 mol reagent, perform an in-process pH-meter measurement, terminate, and obtain the required final assay. I would not execute it now.

This gives a nominal concentration of approximately 1.33e-4 mol/L, far below the inferred 0.004 mol/L cap but still large enough for meaningful bounded measurements. It is the same condition later posed as Q03, but no truth for Q03 has been supplied.

The result patterns would have different consequences:

- **If pH_normalized were near 0.31 and alpha near 0.33**, close to the sealed Q03 prediction, that would strongly support a below-cap weak-acid regime and a saturation or active-pool transition between approximately 1.3e-4 and 0.05 mol/L. A reduced precipitation signal would further support dissociation–precipitation competition.
- **If pH_normalized remained near 0.254 and alpha near 0.07**, the concentration-cap model would be seriously weakened. Background buffering or a concentration-independent proxy mapping would become the leading explanations.
- **If pH increased but alpha did not follow the apparent Ka relationship**, the constant-Ka coupling inferred in K1 would fail outside the original plateau. Separate control of the two public channels would become more likely.
- **If alpha increased but precipitation remained near 0.156**, the proposed inverse dissociation–precipitation coupling used in the blind predictions would be weakened, while a weak-acid or buffer interpretation might survive.
- **If the intermediate pH meter and final assay disagreed much more than in the original campaign**, equilibration time, sampling, or instrument mapping would become a primary concern; a single endpoint would then be insufficient for mechanism selection.

This experiment is preferable to another plateau replicate for mechanism discrimination because the leading models make widely separated predictions there. Its main limitation is that one observation still would not locate a threshold or establish repeatability.

## 5. Tradeoff between identifiability and operational score

The research objective explicitly prioritized characterization rather than yield or process optimization. I therefore did not adapt recipes toward the native scalar score or toward high `equilibrium_confidence`. The matrix deliberately included low- and high-loading corners even though some, such as batches 7, 10, 11, and 12, had lower environment diagnostic values than several intermediate-loading batches.

This favored identifiability over score exploitation in several respects:

- The amount–volume grid was intended to separate total loading, dilution, and concentration.
- Batch 9 was recommended because of its relationship to batch 4, not because it had been demonstrated to maximize the scoring function.
- I did not abandon low-diagnostic regions after observing them.
- I used all intermediate measurement opportunities for comparative evidence rather than selecting only apparently favorable recipes.

There was little evidence of sacrificing identifiability to optimize score. The more important problem was sacrificing some identifiability to obtain broad coverage: twelve distinct conditions with no exact replicates left process variance poorly identified. In addition, spending the entire matrix above the eventual inferred cap was inefficient for mechanism identification, even though it provided broad nominal-concentration coverage.

Conversely, the design may have sacrificed operational score by sampling extremes and by not concentrating runs around batch 5-like conditions, where the diagnostic happened to be high. That was appropriate because `equilibrium_confidence` was not the scientific objective.

The study also did not compare solvents or catalysts, but this was not primarily score optimization. It was a scope decision to isolate the stated aqueous equilibrium. Introducing categorical materials would have consumed scarce batches and confounded the amount–volume question.

## 6. Underused evidence and weaknesses in the blind predictions

Several forms of acquired evidence were underused:

- The analysis relied mainly on processed estimates. Raw final-assay spectral features, peak assignments, and mass-balance fields were not developed into an independent phase or species analysis.
- The pH-meter packets contained electrode-level and replicate information, but I summarized them chiefly through processed pH and derived metrics. A formal replicate-level measurement model was not fitted.
- The known instrument noise scales were discussed qualitatively but were not integrated into a hierarchical fit separating process variation, instrument variation, and model lack of fit.
- The equilibrium residuals and diagnostic values were listed but not modeled as functions of condition. This was prudent regarding `equilibrium_confidence`, but residual structure might still have helped identify problematic regions.
- The paired intermediate and final readings showed large alpha and precipitation discrepancies. I computed aggregate RMS differences for K1, but the condition-specific discrepancy pattern was not fully exploited.
- No exact replicate prevented empirical calibration of batch-to-batch variance, so the later 80% intervals were necessarily judgmental rather than validated coverage intervals.

The least reliable blind predictions are Q08, Q03, Q09, Q04, and Q10.

- **Q08** is the longest trace-loading extrapolation. Its point prediction of alpha = 0.699 and pH_normalized = 0.359 depends almost completely on treating the apparent Ka and inferred cap as literal below-domain physics. Although its interval was broad, even the lower pH bound of 0.28 may insufficiently represent a fully persistent pH clamp near 0.254.
- **Q03 and Q09** have the same structural weakness. Their centers express a sharp transition to ordinary weak-acid behavior that was never observed. Q03's alpha interval of 0.12–0.48 excludes the original plateau value near 0.07 and may therefore be too narrow relative to the buffered-world alternative explicitly retained in K1.
- **Q04** is closer to the inferred cap, but its pH interval of 0.252–0.288 and alpha interval of 0.06–0.19 still presume more knowledge of the transition shape than the campaign provided.
- **Q10** extrapolates to 6.67 mol/L and a 0.006 L volume. Its precipitation interval was wide, but the pH and alpha intervals remained close to the plateau. If extreme concentration changes activity coefficients or the proxy mapping, those intervals could be too narrow.

Q01 and Q02 also deserve caution. Their shared point predictions were a clean test of concentration equivalence, but both total amounts and Q01's volume were below the experimental domain. Assigning identical centers may understate independent amount effects.

Q05–Q07 were assigned identical centers because the preferred model was a reversible state function. The original campaign contained no dosing-order experiment, so those intervals may be too narrow for unobserved hysteresis or transient precipitation. This is particularly important for Q07, which temporarily passes through a more concentrated state before dilution.

Q11 and Q12 are comparatively reliable because they are close to observed conditions. Even there, the nominal 80% coverage is not empirically calibrated.

These weaknesses are partly consistent with K1, which explicitly restricted support to 0.05–1.0 mol/L, stated that below-threshold behavior was speculative, and listed buffering and proxy mapping as competing explanations. The inconsistency is that some sealed prediction intervals—especially Q03's alpha interval—did not fully propagate those stated alternatives. The rationales acknowledged extrapolation, but several numerical bounds conveyed more precision than K1 justified.

## 7. Limitations of the sealed recommendation

The sealed recommendation selected completed batch 9: 0.024 mol reagent in 0.080 L water, followed by termination and final assay. Its purpose was evidentiary. At 0.300 mol/L, it was the high-volume member of the concentration-matched pair with batch 4.

Its limitations are substantial:

- It is based on one realization, with no repeatability estimate.
- It was selected after observing the campaign and therefore benefits from sample-specific information.
- Its scientific value depends on comparison with batch 4; in isolation, it does not uniquely identify concentration control.
- Batch 4 and batch 9 differed modestly in precipitation proxy, 0.15899 versus 0.15092, so the pair is not exact evidence of invariance.
- It does not probe the inferred cap transition and therefore cannot distinguish solubility limitation from buffering.
- It uses only water, one temperature, one pressure region, and an anonymous reagent in one synthetic world.
- It was not demonstrated to maximize the native score, nor was score maximization the selection criterion.

Repeatability should be tested with exact independent repeats of batch 9, retaining every final result rather than replacing unfavorable runs. Local robustness should then be tested with small, symmetric perturbations of amount and volume: one pair holding concentration at 0.300 mol/L while changing scale, and another pair changing concentration around 0.300 mol/L at approximately fixed volume. This would separate repeat noise from local gradients.

To test the mechanistic value of the recommendation, the paired batch 4 condition should also be repeated. Repeating only batch 9 would estimate precision at one point but would not validate the claimed concentration-equivalence comparison.

Cross-material robustness would require repeating the local design with other allowed solvents or material categories, but conclusions should not be transferred automatically because the initial catalog described categorical benchmark couplings rather than real-material predictive chemistry. Cross-world robustness would require independently generated worlds or seeds with the same public contract and a preregistered analysis of whether the same apparent Ka, cap, and precipitation behavior recur.

Finally, a distinction must be maintained between a sample-in winner and a proven optimum. Batch 9 was not even selected as a sample-in score winner; it was selected as a useful evidence anchor. Even if it had happened to have the highest observed scalar score, one noisy maximum among twelve recipes would not establish optimality. Proving a local optimum would require replication, neighboring conditions, and a prespecified objective; proving a global optimum would require substantially broader coverage. None of those claims is warranted by the sealed recommendation.

### EQ-specific supplement

Effective pKa identifiable: `True`; estimate `4.665`; 80% interval `[4.57, 4.76]`.

This is a local effective pKa, not an identified molecular constant. For each final assay I used pH = 14 times pH_normalized and Ka,app = 10^(-pH) times alpha/(1-alpha). The 12 batches gave apparent Ka values of approximately 1.80e-5 to 2.69e-5, centered near 2.16e-5, corresponding to pKa about 4.665. The interval reflects observed dispersion and instrument-scale uncertainty. Buffering, an unknown active-species fraction, and phenomenological sensor coupling remain structurally confounded.

Path-dependence assessment: `indeterminate`.

Every source-campaign batch used the same order: water addition, reagent addition, measurement, termination, and final assay. Therefore no staged-addition paths were experimentally compared. Endpoint regularity is supported—for example, batches 4 and 9 shared 0.300 mol/L nominal concentration despite twofold differences in amount and volume and had similar pH and dissociation—but that comparison tests scale or concentration equivalence, not path dependence. Final-state dominance is a plausible conjecture, while reproducible path dependence remains untested.

Dissociation-precipitation assessment: `indeterminate`.

Supported range: Water-only batches at approximately 297.2 K, with 0.004–0.040 mol reagent, 0.040–0.080 L volume, and 0.050–1.000 mol/L nominal loading. Within this range, dissociation was 0.0618–0.0834 and precipitation signal was 0.1443–0.1617, with no reproducible monotonic or threshold transition.

Competing explanation: The nearly constant precipitation proxy may reflect a saturated plateau, an independent baseline or latent sensor mapping, or measurement variability rather than direct competition with dissociation. A threshold could lie below the tested concentration range, but it was not observed.
## Blind-prediction evaluation

| Metric | MAE | Empirical 80% coverage | Mean width | Interval score |
|---|---:|---:|---:|---:|
| acid_dissociation_fraction | 0.0134561 | 1 | 0.152833 | 0.152833 |
| pH_normalized | 0.00312016 | 0.9 | 0.03225 | 0.0335457 |
| precipitation_signal | 0.0248606 | 0.716667 | 0.0700833 | 0.16166 |

## Scope and privacy

Reference truth was released only after every EQS response was sealed. The environment-derived equilibrium-confidence field is neither an agent uncertainty estimate nor a score. Authentication material, raw model events, session identifiers, and usage accounting are excluded.
