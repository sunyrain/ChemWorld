# EQ-Astra — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

# Mechanistic report: bounded aqueous acid-dissociation and precipitation response

## 1. Main interpretation

The experiments support a concentration-dependent, bounded response rather than an ideal weak acid whose analytical concentration is simply the amount of added reagent divided by liquid volume.

My preferred working description has three parts:

1. Nominal reagent concentration is a useful input coordinate. Dilution raises pH and the reported acid-dissociation fraction, while reducing the precipitation proxy, especially at low loadings. Matched-concentration experiments at different absolute amounts and volumes give similar responses.
2. pH and dissociation fraction are approximately consistent with a common effective monoprotic acidity near pKa = 5.0. This is a conditional cross-channel relationship, not identification of a real acid or proof that the channels independently measure physical species.
3. The connection between nominal loading and effective acidity is strongly compressed at higher loading. The precipitation signal also approaches an apparent plateau around 0.15 over much of the sampled range. These features could arise from bounded internal concentration mappings, limited dissolved availability, activity effects, or synthetic response transformations. The experiments do not uniquely separate those possibilities.

The simplest useful representation is therefore a latent effective-concentration model coupled to a weak-acid-like speciation relationship and an empirical bounded precipitation response. I would not interpret the precipitation signal as precipitated mass or claim a solubility product from these data.

## 2. Experimental scope and measurement basis

Twelve batches were completed, explicitly terminated, and measured by final assay. Each also had one intermediate pH-meter measurement. All used water and the anonymous limiting reagent, with no catalyst or other solvent. Temperature telemetry was approximately 298.15 K. Batch 7 alone included an explicit 600 s wait at 400 rpm; its reported temperature increase was only about 0.00048 K. The other measurements were made without an explicit waiting interval.

The campaign used 63 operations, 12 intermediate pH-meter measurements, and 12 final assays. The selection of batch 8 as the recommended completed experiment was an evidentiary choice: it supplies a direct low-concentration reference, with a scale comparison in batch 9 and a staged-dilution comparison in batch 10. It was not selected as a yield or diagnostic-score optimum.

The principal observed quantities are:

- q = pH_normalized, with pH = 14q by the public measurement contract;
- alpha = acid_dissociation_fraction;
- P = precipitation_signal, a bounded normalized proxy;
- equilibrium_residual and equilibrium_confidence, which are environmental diagnostics.

The pH-meter sampling step consumes 0.00003 L. The final assay consumes 0.0003 L. Consequently, nominal preparation volumes are not exactly the final sample-basis volumes. In a homogeneous proportional withdrawal, concentration would be preserved by sampling; however, the actual dissolved chemical inventories and phase-specific removal were not independently measured. I therefore distinguish nominal preparation concentration from an independently verified dissolved-acid concentration.

Nominal final-assay noise standard deviations were 0.002 for q and 0.006 for alpha and P. The corresponding pH-meter processed-channel values were 0.004, 0.015, and 0.02. The raw pH packet inspected for the intermediate measurement in batch 6 separately declared a pH standard deviation of 0.02. Those different uncertainty statements refer to different parts of the measurement output and should not be silently conflated. I use the processed-channel noise scales when comparing the processed quantities below.

## 3. Final-assay evidence

Values below are rounded actual final-assay observations. Amounts and volumes are nominal preparation quantities, before accounting for measurement withdrawals.

| Batch | Preparation and path | Nominal endpoint n/V, mol/L | q | alpha | P |
|---|---|---:|---:|---:|---:|
| 1 | 0.001 mol in 0.018 L | 0.055556 | 0.277216 | 0.068607 | 0.145044 |
| 2 | 0.001 mol in 0.054 L | 0.018519 | 0.281063 | 0.074072 | 0.153389 |
| 3 | 0.0001 mol in 0.018 L | 0.005556 | 0.285496 | 0.078831 | 0.142795 |
| 4 | 0.01 mol in 0.018 L | 0.555556 | 0.279167 | 0.070904 | 0.154927 |
| 5 | 0.03 mol in 0.054 L | 0.555556 | 0.277505 | 0.078770 | 0.157501 |
| 6 | 0.0001 mol in 0.054 L | 0.001852 | 0.296069 | 0.114097 | 0.147961 |
| 7 | 0.001 mol in 0.018 L; 600 s wait after intermediate measurement | 0.055556 | 0.279578 | 0.079698 | 0.160383 |
| 8 | 0.00001 mol in 0.054 L | 0.00018519 | 0.324306 | 0.244555 | 0.035567 |
| 9 | 0.00000333333 mol in 0.018 L | 0.00018519 | 0.321434 | 0.245163 | 0.025651 |
| 10 | 0.00001 mol in 0.018 L, intermediate measurement, then add 0.036 L water | approximately 0.00018519 | 0.323408 | 0.228022 | 0.030450 |
| 11 | 0.00001 mol in 0.054 L, intermediate measurement, then add 0.00009 mol reagent | approximately 0.001852 | 0.294104 | 0.109249 | 0.140935 |
| 12 | 0.000001 mol in 0.054 L | 0.000018519 | 0.360542 | 0.530390 | 0.012832 |

Final-assay event identifiers for batches 1–12 were respectively 0005, 0010, 0015, 0020, 0025, 0030, 0036, 0041, 0046, 0052, 0058, and 0063, each with the prefix runner-operation-.

## 4. What concentration and dilution do

### 4.1 A clearly resolved dilute regime

The strongest evidence comes from the direct-preparation sequence at 0.054 L:

- Batch 6: 0.0001 mol, q = 0.296069, alpha = 0.114097, P = 0.147961.
- Batch 8: 0.00001 mol, q = 0.324306, alpha = 0.244555, P = 0.035567.
- Batch 12: 0.000001 mol, q = 0.360542, alpha = 0.530390, P = 0.012832.

The corresponding pH values are approximately 4.1450, 4.5403, and 5.0476. Thus two successive tenfold reductions in nominal concentration increase dissociation substantially and decrease the precipitation proxy. These changes are much larger than the declared final-assay noise scales.

This behavior is qualitatively compatible with a weak-acid-like response: dilution increases the fraction dissociated while decreasing hydrogen activity. The precipitation trend suggests a common dependence on loading or availability, but it does not establish that acid dissociation directly causes precipitation or vice versa.

### 4.2 Strong compression at higher concentration

Batch 3 and batch 4 differ by a factor of 100 in nominal concentration at the same preparation volume. Yet q changes only from 0.285496 to 0.279167, and alpha from 0.078831 to 0.070904. The precipitation signal remains near 0.15.

The small individual differences should not be overinterpreted, but the absence of the large concentration response expected for an ideal unbuffered acid is informative. Across batches 1–5, nominal concentrations span approximately 0.00556–0.556 mol/L, while alpha remains roughly 0.069–0.079 and q roughly 0.277–0.285.

A literal weak-acid model using the full nominal loading as analytical acid concentration cannot naturally explain this high-loading compression with a fixed dissociation constant. An additional loading-to-effective-state relationship is required.

### 4.3 Matched concentration supports a concentration coordinate

Batches 4 and 5 have the same nominal concentration but differ threefold in both amount and volume. Their final differences are approximately:

- q: −0.001662;
- alpha: +0.007866;
- P: +0.002574.

Those differences do not establish a scale effect at the stated measurement precision.

The more informative low-concentration comparison is batches 8 and 9. Their nominal concentrations are also equal despite a threefold scale difference. Their alpha values, 0.244555 and 0.245163, are nearly identical. Their q values differ by −0.002872 and P by −0.009916, modest differences relative to independent two-assay noise scales of approximately 0.00283 and 0.00849, respectively.

These comparisons favor concentration over absolute reagent amount as a first-order explanatory variable. They do not prove exact scale invariance or exclude smaller volume, geometry, or sampling effects.

## 5. The pH–dissociation coupling

If alpha can be interpreted as the fraction of a monoprotic acid present in its dissociated form, the usual activity-based ratio motivates the effective relation

pH = pKa_eff + log10[alpha/(1 − alpha)].

Equivalently,

pKa_eff = 14q − log10[alpha/(1 − alpha)].

This equation can be tested as a cross-channel relationship without first assuming that nominal reagent concentration equals total acid concentration.

Applying it to final assays gives:

| Batch | Derived pKa_eff |
|---|---:|
| 1 | 5.014 |
| 2 | 5.032 |
| 6 | 5.035 |
| 8 | 5.030 |
| 9 | 4.988 |
| 12 | 4.995 |

The agreement near 5.0 spans a wide change in reported dissociation fraction, from about 0.069 to 0.530. It is stronger evidence for an effective pH–fraction relation than for any particular loading-to-concentration law.

The derived values are not independent direct measurements of a molecular pKa. They use two public output channels, which might themselves be generated from shared synthetic state variables. They also require the interpretation of alpha as a monoprotic speciation fraction. Activity-coefficient ratios or a transformed fraction could change the physical meaning of the intercept.

For approximate uncertainty propagation, assuming independent small errors,

sigma(pKa_eff)^2 ≈ (14 sigma_q)^2 + [sigma_alpha / (ln(10) alpha(1 − alpha))]^2.

With the declared final-assay noise, this gives a per-assay uncertainty scale around 0.05 pKa units near alpha = 0.07 and around 0.03–0.04 at the more dissociated conditions. This is only an illustrative propagation: it excludes unknown cross-channel correlations and model discrepancy. Nevertheless, it shows why the clustering near 5.0 is meaningful while small differences among the estimates are not evidence of a changing dissociation constant.

## 6. Revision of the archival relationship

The public archival claim contained two distinct elements:

1. An 80% interval for effective pKa of 4.6094–4.7094.
2. For 0.001 mol at 298.15 K, dilution from 0.018 to 0.054 L was predicted to increase q by 0.003494987 and alpha by 0.008187416.

Batches 1 and 2 directly tested the preparation endpoints. Their final-assay differences were:

- observed delta q = +0.003847015;
- observed delta alpha = +0.005464413.

Both are compatible with the archival local increments at the nominal assay precision. In particular, the alpha increment is smaller than the approximate two-assay standard-deviation scale of 0.00849. The endpoint pair therefore neither precisely validates the local dilution slope nor warrants rejecting it.

The pKa claim fares differently. Under the monoprotic interpretation of the measured fraction, the observed pH–fraction combinations imply approximately 5.0, not 4.61–4.71. I would revise the effective cross-channel acidity estimate upward and reject the archival interval for that specific interpretation of the public outputs.

This distinction is important: a local dilution increment can remain approximately right even when its associated mechanistic parameter or indexing is wrong. The experiments do not establish why the archival estimate differs. Possible explanations include a different effective parameter definition, a scope mismatch, or a different mapping between reported fraction and physical speciation. I cannot identify the cause from the public evidence.

## 7. A candidate effective-state model

A compact phenomenological model is:

C_nom = n_nom / V_liquid

C_eff = f(C_nom; conditions)

Ka_eff ≈ 10^(−5)

h = [sqrt(Ka_eff^2 + 4 Ka_eff C_eff) − Ka_eff] / 2

alpha = h / C_eff

q = −log10(h) / 14

P = g(C_nom, C_eff, possibly other state variables)

Here h is a hydrogen concentration-like quantity relative to the usual standard state. The quadratic form assumes an ideal unbuffered monoprotic balance at the effective-state level, neglecting water autoionization and other charge sources. It is a candidate representation, not an established microscopic mechanism.

The crucial freedom is f. The evidence does not support setting f(C_nom) = C_nom over the entire tested range. Instead, f must strongly compress increasing nominal concentration at higher loading, or some other part of the ideal balance must fail.

One way to illustrate this mismatch is to calculate the conditional quantity

C_eff* = 10^(−14q) / alpha.

If hydrogen concentration equals dissociated-acid concentration, this is the implied analytical acid concentration. The actual derived values include:

| Batch | Nominal concentration, mol/L | Conditional C_eff*, mol/L |
|---|---:|---:|
| 12 | 0.00001852 | 0.00001690 |
| 8 | 0.0001852 | 0.0001179 |
| 6 | 0.001852 | 0.0006277 |
| 3 | 0.005556 | 0.001277 |
| 2 | 0.01852 | 0.001568 |
| 1 | 0.05556 | 0.001917 |
| 4 | 0.5556 | 0.001742 |
| 5 | 0.5556 | 0.001654 |

These are arithmetic transformations of observed channels, not measured chemical inventories. The high-loading values suggest an effective scale of order 0.0015–0.002 mol/L despite much larger nominal concentrations. The apparent nonmonotonic details at the upper end should not be fitted as physical features; they are sensitive to measurement noise and to the assumptions used in this transformation.

A smooth saturating f, a hard bound, or a dissolution-limited mapping could each reproduce this broad behavior. The campaign does not identify their exact functional form or parameters. I therefore prefer an unspecified bounded mapping to a precisely parameterized equation unsupported by sufficient transition-region measurements.

## 8. Precipitation: supported response, unidentified mechanism

The precipitation proxy has a substantial concentration response:

- At approximately 0.0000185 mol/L, batch 12 gives P = 0.012832.
- Around 0.000185 mol/L, batches 8–10 give P = 0.025651–0.035567.
- Around 0.00185 mol/L, batches 6 and 11 give P = 0.140935–0.147961.
- At higher nominal concentrations, most final assays remain near 0.14–0.16.

Thus the sampled points locate a strong rise between roughly 0.000185 and 0.00185 mol/L, followed by an apparent plateau. They do not locate a unique sharp onset concentration. The intermediate observation in batch 10, at nominally 0.00001 mol/0.018 L = 0.000556 mol/L, gave P = 0.133066, but that pH-meter proxy has a larger noise scale and is not a densely sampled onset study.

The apparent plateau is around 0.15, not at the public channel's upper numerical limit of 1. It could therefore reflect a bounded internal response rather than clipping at the displayed channel boundary.

Several interpretations remain reasonable:

- Genuine loss of dissolved availability through precipitation could help explain the compressed acidity response.
- The proxy could be a smooth concentration-driven synthetic signal rather than a mass balance on solids.
- Both precipitation and acidity could respond to a shared effective state without directly constraining one another.
- Background composition or activity effects could limit the acidity response while precipitation is generated through a separate relationship.

No solid identity, dissolved species inventory, precipitated amount, ion product, or independent solubility measurement was obtained. A precipitation-mediated cap on dissolved acid is therefore plausible but unproven. In particular, the inverse association between alpha and P during dilution is not evidence that changing alpha alone would change precipitation.

## 9. Path and waiting-time evidence

### 9.1 Staged dilution

Batch 10 began with 0.00001 mol in 0.018 L. Its intermediate measurement gave:

q = 0.309811, alpha = 0.165178, P = 0.133066.

After adding 0.036 L water, its final assay gave:

q = 0.323408, alpha = 0.228022, P = 0.030450.

The directions agree with the dilution prediction recorded before this batch: increased pH and dissociation, decreased precipitation.

Its endpoint pH and precipitation are close to the direct low-concentration preparations in batches 8 and 9. Its fraction is about 0.0165–0.0171 lower than theirs. That is about two nominal two-assay standard deviations, so exact path equivalence should not be declared. It is a reason for replication, not by itself a compelling discovery of hysteresis. The endpoint inventory also differs slightly because sampling preceded dilution.

### 9.2 Staged loading

Batch 11 began with 0.00001 mol in 0.054 L. Its intermediate measurement gave q = 0.323166, alpha = 0.250387, and P = 0.076247. Adding 0.00009 mol reagent led to final values q = 0.294104, alpha = 0.109249, and P = 0.140935.

The endpoint is close to batch 6, prepared directly at the corresponding nominal loading. Their final differences are approximately −0.001965 in q, −0.004848 in alpha, and −0.007026 in P. These differences do not resolve a path effect at the nominal noise level.

The intermediate P in batch 11 is higher than the final proxy measured at similar low concentration in batches 8 and 9. This illustrates why individual pH-meter proxy values should not be treated as exact chemical states; the processed pH-meter precipitation noise is appreciably larger than the final-assay noise.

### 9.3 Waiting

Batch 7 repeated the batch 1 preparation but added a 600 s wait after the intermediate measurement. Before waiting, q was 0.279824; the final value was 0.279578. No large pH change was apparent.

Compared with the no-wait batch 1 final assay, batch 7 differed by +0.002362 in q, +0.011091 in alpha, and +0.015339 in P. The latter differences are not negligible relative to nominal noise, but one comparison cannot separate waiting from batch/readout variation. Within-batch before/after comparisons also change instrument and include sampling.

The defensible conclusion is that a large slow pH relaxation was not demonstrated at this anchor condition. It is not that kinetics are absent everywhere or that 600 s has no effect on any response.

## 10. Competing explanations and identifiability

### Effective monoprotic speciation with a bounded availability mapping

This is my preferred compact representation. It explains the approximate constant pKa_eff, the dilute response, and the high-loading compression. It leaves the origin of the availability mapping unresolved.

### Real solution chemistry with activities, buffering, or background species

Hydrogen activity need not equal hydrogen concentration, and electroneutrality need not be satisfied solely by the reported acid's conjugate base. Such effects could invalidate C_eff* as an inventory while preserving an approximately Henderson–Hasselbalch-like output relationship. The campaign lacked independent ionic-strength, counterion, or background-acidity interventions to distinguish these effects.

### Dissolution or precipitation-limited dissolved concentration

A ceiling in dissolved availability could explain why very different high nominal loadings produce similar pH and alpha. The precipitation trend makes this plausible, but the proxy is not a phase-resolved mass measurement. No quantitative equilibrium solid–liquid mechanism is identified.

### Shared synthetic latent-variable or reporting transformation

Because these are benchmark channels, q and alpha may be related by construction, and P may be another bounded transformation of the same loading coordinate. That would explain the cross-channel regularity without requiring a uniquely recoverable physical acid mechanism. Numerical relationships among public outputs remain useful even under this interpretation.

### Kinetic or preparation-history effects

The zero-explicit-wait measurements, one wait comparison, and two staged paths do not exclude smaller kinetic or history effects. The current data favor a predominantly endpoint-controlled response over the tested paths, but do not establish a path-independent thermodynamic equilibrium throughout the world.

These explanations are not all mutually exclusive. The important unresolved distinction is whether the bounded behavior lies in dissolved chemical availability, activity/speciation, or the observation transformation itself.

## 11. Uncertainty and supported range

Direct support is restricted to:

- water with the anonymous reagent;
- preparation volumes of 0.018 and 0.054 L, including one staged dilution;
- total added reagent amounts from 0.000001 to 0.03 mol;
- nominal endpoint concentrations approximately 0.0000185–0.556 mol/L, sampled sparsely rather than continuously;
- approximately 298.15 K;
- immediate-readout preparations and one 600 s waiting comparison.

Within that scope, the strongest findings are the dilute concentration dependence, approximate scale agreement, high-loading compression, and conditional pKa_eff near 5.0. The exact concentration mapping, precipitation onset and shape, small path effects, and time dependence remain weakly identified.

No conclusion is established for other solvents, catalysts, substantial temperature or pressure changes, other reagents, extremely dilute behavior approaching water autoionization, or concentrations beyond the sampled range. The approximate pKa clustering is not a fitted confidence interval; the environmental equilibrium_confidence is neither my uncertainty nor a research score. Similarly, near-zero equilibrium_residual outputs cannot substitute for an independent chemical mass or charge balance.

## 12. Testable consequences, explicitly separated from observations

The following are model implications, not additional measured results:

- At untested intermediate concentrations within the dilute range, I expect higher dilution to increase q and alpha and reduce P, with a stronger response than on the high-loading plateau.
- Under the conditional speciation interpretation, new pH–fraction pairs should remain close to pH − log10[alpha/(1 − alpha)] ≈ 5.0. A systematic departure larger than measurement uncertainty would challenge this representation.
- Matched-concentration preparations at modestly different scales should give similar endpoints if concentration remains the dominant coordinate.
- A precipitation-controlled availability cap should be accompanied by a reproducible relationship between independently measured dissolved inventory and solid formation. The present proxy alone cannot test that consequence.
- Reproducible path or waiting-time offsets exceeding measurement and sampling uncertainty would require adding history or kinetics to the endpoint model.

I would not extrapolate the observed precipitation plateau indefinitely or predict alpha approaching one at arbitrarily low nominal loading without accounting for background chemistry and water autoionization.

## 13. Overall conclusion

This world is best described, at the resolution of the public evidence, by a weak-acid-like pH–dissociation coupling embedded in a bounded loading response. Nominal concentration organizes the observations better than absolute amount alone. Dilution has a strong and coherent effect in the dilute regime; high nominal loading produces much smaller changes, and the precipitation proxy approaches an apparent plateau.

The archival local dilution increment remains compatible with the direct endpoint test, but its effective pKa interval is not supported under the monoprotic interpretation of the observed fraction. A revised conditional value near 5.0 describes the public pH–fraction relationship much better.

The central limitation is not simply numerical uncertainty in pKa. It is the unobserved mapping from added reagent to chemically effective concentration, and the uncertain physical meaning of the precipitation proxy. The campaign identifies useful effective relationships while leaving several microscopic and reporting-level mechanisms observationally equivalent.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | acid_dissociation_fraction | 0.077 | 0.064 | 0.09 |
| Q01 | pH_normalized | 0.281 | 0.276 | 0.286 |
| Q01 | precipitation_signal | 0.151 | 0.138 | 0.165 |
| Q02 | acid_dissociation_fraction | 0.077 | 0.064 | 0.09 |
| Q02 | pH_normalized | 0.281 | 0.276 | 0.286 |
| Q02 | precipitation_signal | 0.151 | 0.138 | 0.165 |
| Q03 | acid_dissociation_fraction | 0.273 | 0.247 | 0.301 |
| Q03 | pH_normalized | 0.328 | 0.322 | 0.334 |
| Q03 | precipitation_signal | 0.022 | 0 | 0.049 |
| Q04 | acid_dissociation_fraction | 0.12 | 0.098 | 0.143 |
| Q04 | pH_normalized | 0.296 | 0.289 | 0.303 |
| Q04 | precipitation_signal | 0.142 | 0.117 | 0.164 |
| Q05 | acid_dissociation_fraction | 0.075 | 0.059 | 0.091 |
| Q05 | pH_normalized | 0.279 | 0.273 | 0.285 |
| Q05 | precipitation_signal | 0.153 | 0.136 | 0.171 |
| Q06 | acid_dissociation_fraction | 0.075 | 0.059 | 0.091 |
| Q06 | pH_normalized | 0.279 | 0.273 | 0.285 |
| Q06 | precipitation_signal | 0.153 | 0.136 | 0.171 |
| Q07 | acid_dissociation_fraction | 0.075 | 0.059 | 0.091 |
| Q07 | pH_normalized | 0.279 | 0.273 | 0.285 |
| Q07 | precipitation_signal | 0.153 | 0.136 | 0.171 |
| Q08 | acid_dissociation_fraction | 0.572 | 0.52 | 0.628 |
| Q08 | pH_normalized | 0.367 | 0.359 | 0.375 |
| Q08 | precipitation_signal | 0.006 | 0 | 0.024 |
| Q09 | acid_dissociation_fraction | 0.252 | 0.223 | 0.282 |
| Q09 | pH_normalized | 0.324 | 0.317 | 0.331 |
| Q09 | precipitation_signal | 0.028 | 0.003 | 0.058 |
| Q10 | acid_dissociation_fraction | 0.074 | 0.045 | 0.106 |
| Q10 | pH_normalized | 0.279 | 0.267 | 0.291 |
| Q10 | precipitation_signal | 0.154 | 0.112 | 0.198 |
| Q11 | acid_dissociation_fraction | 0.075 | 0.06 | 0.091 |
| Q11 | pH_normalized | 0.279 | 0.273 | 0.285 |
| Q11 | precipitation_signal | 0.154 | 0.137 | 0.172 |
| Q12 | acid_dissociation_fraction | 0.075 | 0.063 | 0.087 |
| Q12 | pH_normalized | 0.279 | 0.275 | 0.283 |
| Q12 | precipitation_signal | 0.153 | 0.141 | 0.166 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

These are blind predictions for the three requested final-assay outputs, based only on the completed public campaign. Nominal concentration is total added reagent divided by total added water. The queries contain no intermediate measurement withdrawals, and no adjustment is made that treats the final assay's sample consumption as a prior dilution or concentration step. Central predictions use concentration-dependent interpolation in the dilute regime and pooled plateau behavior at higher loading. The approximate pH–fraction relationship with effective pKa near 5.0 provides a consistency constraint, not proof of a physical species identity or an ideal nominal-loading mass balance. Matched endpoint recipes receive equal central estimates because the campaign did not identify a reliable dosing-order correction. Precipitation is predicted as an empirical bounded proxy, not solid mass. The stated intervals are approximate marginal 80% predictive intervals for individual future assay outcomes, not simultaneous intervals for all metrics or queries. They incorporate declared final-assay noise, limited replication, interpolation or extrapolation uncertainty, and unresolved scale or path effects; their coverage has not been independently validated. Bounds respect the public zero-to-one measurement range. Environmental equilibrium_confidence is not used as epistemic confidence or as a task score. No new laboratory evidence was obtained, and the sealed report is unchanged.

**Q01**: The nominal concentration is 0.015 mol/L, between batches 3 and 2 and within the observed compressed-response regime. The prediction is anchored mainly to batch 2, with uncertainty for interpolation, preparation-volume differences, and final-assay noise.

**Q02**: This preparation has the same nominal concentration as Q01. Matched-concentration comparisons in batches 4 versus 5 and 8 versus 9 support equal central predictions despite different absolute amounts and volumes. These are predictions for independent assay outcomes, not an assertion that the measured outcomes will be identical.

**Q03**: The nominal concentration is 0.0001333 mol/L, moderately below the matched low-concentration preparations in batches 8 and 9. Interpolation toward batch 12 predicts higher dissociation and pH and a smaller precipitation proxy. The liquid volume exceeds the studied preparation volumes, and the precipitation response is only sparsely constrained here.

**Q04**: The nominal concentration is 0.001667 mol/L, close to batches 6 and 11. Slightly greater dilution predicts a modest increase in dissociation relative to those endpoints. The 0.006 L volume is below the studied range, so the intervals include additional uncertainty about scale dependence and the precipitation transition.

**Q05**: The accumulated endpoint is 0.002 mol in 0.024 L, or 0.08333 mol/L, within the high-loading plateau supported by batches 1, 4, 5, and 7. Staged experiments provided no compelling evidence for a large path effect, so the central prediction depends on the endpoint. The intervals allow unresolved dosing-history effects.

**Q06**: This sequence reaches the same nominal endpoint as Q05. The working model does not assign a systematic effect to solvent-first accumulation or splitting the reagent dose. Equal central estimates reflect that unresolved distinction, while predictive intervals retain room for history dependence and assay variation.

**Q07**: The final amount and volume equal those of Q05 and Q06. Batch 10 broadly supported approaching a direct-preparation response by dilution, although exact path equivalence was not established. No directional path correction is justified for this high-loading endpoint.

**Q08**: At 0.00001333 mol/L, this condition is modestly more dilute than batch 12 and lies below the tested concentration range. Extending the dilute weak-acid-like response predicts increased dissociation and pH, with precipitation near its lower boundary. Wider intervals account for extrapolation, uncertain background chemistry, and the larger volume.

**Q09**: The nominal concentration is 0.0001667 mol/L, close to the low-concentration endpoints of batches 8 through 10. Slightly greater dilution predicts a modest increase in dissociation. Although concentration is well supported as a coordinate, the substantially smaller volume and observed endpoint variation justify broader intervals than assay noise alone.

**Q10**: The nominal concentration is 6.667 mol/L, twelve times the highest studied concentration, and the amount and volume also extend beyond the studied preparation range. The central prediction extends the observed high-loading plateau rather than applying an unsupported ideal nominal-concentration acid law. This is the least secure extrapolation; the wider intervals allow changes in effective availability, scale response, and precipitation behavior.

**Q11**: The nominal concentration is 0.5333 mol/L, close to the matched high-concentration batches 4 and 5. Their final observations anchor the plateau prediction. Absolute amount and volume exceed those studied, so uncertainty is larger than a simple replicate prediction but substantially smaller than for Q10.

**Q12**: The nominal concentration is 0.13636 mol/L, inside the sampled high-loading regime, and both preparation amount and volume are within the studied ranges. Pooling plateau observations is more defensible than fitting a small concentration slope to noisy differences. The intervals include assay noise and uncertainty in the plateau level.

## K2

Retained failure: provider_failure
