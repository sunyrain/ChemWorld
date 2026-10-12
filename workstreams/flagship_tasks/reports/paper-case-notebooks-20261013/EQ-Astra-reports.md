# EQ-Astra — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

# Mechanistic report: bounded aqueous-equilibrium campaign

## 1. Main interpretation

The strongest result is a limitation on the interpretation of the controls: nominal added reagent concentration, n/V, cannot simply be equated with the analytical concentration of an isolated, unbuffered monoprotic acid. Over large changes in loading and liquid volume, the measured pH, acid-dissociation fraction, and precipitation proxy remained in a narrow neighborhood.

A conservative empirical description is therefore a weakly responsive chemical-channel state: pH approximately 3.9–4.0, acid-dissociation fraction approximately 0.07–0.09, and precipitation proxy approximately 0.15. Small dilution responses are plausible, but most observed contrasts are comparable with measurement variability. The observations do not identify why the response is so compressed.

Conditional on interpreting the reported fraction as the usual dissociated fraction of a monoprotic acid, the joint pH–fraction values imply an apparent pKa near 5.02, rather than the supplied archival interval 4.609–4.709. This conditional parameter is more defensible than treating the nominal loading as dissolved acid concentration. However, the narrow range of observed pH and fraction means that even this pKa is principally a consistency summary, not a demonstrated mechanistic law over a substantial titration range.

No solubility product, precipitation threshold, precipitated mass, or kinetic rate constant was identified.

## 2. Public variables and measurement interpretation

The manipulated quantities were added reagent amount n, water volume V, preparation path, and, in one batch, waiting time. All batches used water, no catalyst, and temperatures near 298.15 K. One batch used the public component-0 addition operation instead of add_reagent.

The principal measured channels were:

- q = pH_normalized, with pH = 14q by the published contract.
- alpha = acid_dissociation_fraction, a bounded fraction.
- P = precipitation_signal, a bounded normalized proxy, not a measured amount of solid.
- equilibrium_residual and equilibrium_confidence, which are environment diagnostics. Neither is my uncertainty estimate, and neither establishes a physical mechanism by itself.

Chemical composition was not independently measured. The public labels do not establish that the added limiting reagent is chemically identical to the species underlying alpha. No molecular acid identity or solid identity can be assigned from this campaign.

Each batch had one pH-meter measurement and one final assay. The pH-meter measurement consumed 0.00003 L before the final assay; the final assay consumed 0.0003 L. Accordingly, nominal recipe volume is not exactly the liquid volume at final measurement. Homogeneous sampling would normally preserve concentration while reducing amount and volume together, but that behavior should not be assumed for unidentified phases or internal mappings. The relative pre-final volume removal was largest in batch 8: 1.5% of its initial 0.002 L.

The raw public pH packet for batch 1 reported pH 3.950, hydrogen_mol_L 0.000112289123, and a declared pH standard deviation of 0.02. These fields support the pH interpretation but do not independently identify acid concentration: they are outputs of the same synthetic measurement packet.

## 3. Experimental record

All twelve batches were explicitly terminated and final-assayed. The following table gives final processed estimates, rounded for readability. Volumes are nominal water additions, not sampling-corrected final volumes. pH is calculated as 14 times the reported normalized value.

| Batch | Added amount, mol | Nominal water, L | Distinguishing treatment | q | pH | alpha | P |
|---|---:|---:|---|---:|---:|---:|---:|
| 1 | 0.001 | 0.018 | Initial archival anchor | 0.277216 | 3.8810 | 0.068607 | 0.145044 |
| 2 | 0.001 | 0.054 | Dilute archival anchor | 0.281063 | 3.9349 | 0.074072 | 0.153389 |
| 3 | 0.0001 | 0.018 | Low-loading contrast | 0.285496 | 3.9970 | 0.078831 | 0.142795 |
| 4 | 0.010 | 0.018 | Higher-loading contrast | 0.279167 | 3.9083 | 0.070904 | 0.154927 |
| 5 | 0.040 | 0.018 | Highest-loading contrast | 0.277424 | 3.8839 | 0.078599 | 0.157516 |
| 6 | 0.001 | 0.018 | 60 s wait at 300 rpm | 0.281328 | 3.9386 | 0.075055 | 0.159521 |
| 7 | 0.001 | 0.018 then +0.036 | Component 0; pH measurement before dilution | 0.281407 | 3.9397 | 0.083749 | 0.159733 |
| 8 | 0.001 | 0.002 | Small-volume contrast | 0.280521 | 3.9273 | 0.078199 | 0.159061 |
| 9 | 0.001 | 0.080 | Large-volume contrast | 0.281552 | 3.9417 | 0.087482 | 0.147748 |
| 10 | 0.002 | 0.036 | Doubled scale at batch-1 nominal n/V | 0.280525 | 3.9273 | 0.063528 | 0.153869 |
| 11 | 0.001 | 0.018 | Repeat of batch 1 | 0.279368 | 3.9111 | 0.070222 | 0.152489 |
| 12 | 0.001 | 0.054 | Repeat of batch 2 | 0.279531 | 3.9134 | 0.077393 | 0.166348 |

The corresponding final-assay event numbers were 0005, 0010, 0015, 0020, 0025, 0031, 0037, 0042, 0047, 0052, 0057, and 0062. Event 0062 confirmed twelve completed experiments and campaign termination. Batch 11 was committed as the repeated reference anchor, not as an optimized outcome.

## 4. How the interpretation developed

### 4.1 Initial hypothesis and archival relationship

The supplied archival claim concerned 0.001 mol at 298.15 K diluted from 0.018 to 0.054 L. It predicted:

- delta q = +0.003494987, equivalent to approximately +0.04893 pH units;
- delta alpha = +0.008187416;
- an effective pKa interval of 4.609404789–4.709404789, labeled as an 80% archival interval.

My initial working hypothesis was that dilution would increase both pH and dissociation, and that n/V might organize the response. I treated the archival relationship as a testable local estimate, not as a calibration constraint.

### 4.2 The first dilution pair did not falsify the local increments

Batch 2 minus batch 1 gave:

- delta q = +0.0038470;
- delta pH = +0.05386;
- delta alpha = +0.0054644;
- delta P = +0.0083451.

The first two chemical contrasts had the expected direction and were compatible in magnitude with the archival dilution increments. A single pair, however, was insufficient to distinguish a reproducible response from measurement variation.

### 4.3 The loading sweep challenged the ordinary concentration interpretation

Batches 3, 4, and 5 varied loading at fixed nominal volume 0.018 L. Between batches 3 and 5, added amount increased 400-fold, from 0.0001 to 0.040 mol. Nominal n/V increased from approximately 0.00556 to 2.222 mol/L.

Despite this change, pH fell only from 3.9970 to 3.8839, while alpha was almost unchanged: 0.078831 versus 0.078599. The intermediate batch 4 had alpha 0.070904, so the fraction did not follow a clean monotonic loading trend.

For comparison, an isolated weak acid in its low-dissociation regime would approximately obey pH = (pKa - log10 C)/2. A 400-fold concentration increase would then decrease pH by approximately 1.30 units and substantially decrease the dissociated fraction. That is not what these channels showed. This theoretical contrast is not a fitted prediction of the world; it explains why I stopped treating nominal n/V as ordinary analytical acid concentration.

### 4.4 Waiting did not reveal a large hidden relaxation

Batch 6 repeated the 0.001 mol, 0.018 L recipe but included a 60 s wait at 300 rpm. Relative to batch 1, its final q increased by approximately 0.00411 and alpha by 0.00645. Relative to the later immediate repeat, batch 11, the differences were smaller: approximately 0.00196 and 0.00483.

The wait therefore did not reveal a large transformation toward the strongly concentration-dependent state expected under the simple acid model. It weakens the explanation that all immediate observations merely preceded a large, rapid relaxation. It does not establish instantaneous equilibration, a relaxation time, or absence of slower processes: there was only one waiting treatment and no within-batch chemical time series.

### 4.5 Component substitution and staged dilution remained confounded

Batch 7 used component 0, initially in 0.018 L, measured with the pH meter, and then received another 0.036 L of water before its final assay.

Before dilution, the pH-meter channels were q = 0.279824, alpha = 0.064114, and P = 0.166773. After dilution, the final assay gave q = 0.281407, alpha = 0.083749, and P = 0.159733.

These readings are compatible with increased dissociation after dilution, but they use different instruments at different preparation states. They cannot cleanly quantify the dilution effect. Comparison with batches 2 and 12 also confounds reagent-operation choice with preparation path. The result provides no evidence for a dramatic component-0-specific shift, but it does not prove equivalence of the two addition operations or path independence.

### 4.6 A forty-fold volume contrast still produced only small changes

Batches 8 and 9 used 0.001 mol in 0.002 and 0.080 L respectively, corresponding to nominal concentrations 0.5 and 0.0125 mol/L.

Across this forty-fold dilution:

- q increased by only 0.0010307, or 0.01443 pH units;
- alpha increased by 0.0092829;
- P decreased by 0.0113128.

The fraction change is suggestive in direction but modest relative to assay uncertainty. The pH contrast is much smaller than the approximately 0.801 pH-unit change expected from the elementary square-root weak-acid approximation across a forty-fold dilution. This is a second strong reason not to identify nominal concentration directly with the chemically active acid concentration.

### 4.7 Matched nominal concentration did not uniquely establish concentration control

Batch 10 doubled both amount and volume relative to batch 1: 0.002 mol in 0.036 L instead of 0.001 mol in 0.018 L. Both have nominal n/V = 0.05556 mol/L.

Their final channels were broadly similar, with q differing by +0.003309 and alpha by -0.005079. This is compatible with scale invariance. However, a model in which almost every recipe yields approximately the same chemical state also predicts this agreement. Thus the matched-scale comparison does not uniquely support an n/V-controlled mechanism.

### 4.8 Replication reduced confidence in a precisely specified dilution slope

The repeated anchor pair, batch 12 minus batch 11, gave:

- delta q = +0.0001632;
- delta pH = +0.00228;
- delta alpha = +0.0071707;
- delta P = +0.0138588.

The alpha contrast had the same sign as in the first pair, but the pH contrast was much smaller. Averaging the two direct endpoint pairs gives delta q approximately +0.0020051 and delta alpha approximately +0.0063176. These averages remain compatible with the archival increments at the available precision; they do not validate their exact values.

The dilute final precipitation proxy itself differed by approximately 0.01296 between batches 2 and 12. That repeatability contrast cautions against assigning mechanisms to cross-recipe changes of similar size.

## 5. Candidate equations and what they do—and do not—identify

### 5.1 A conventional acid model is useful as a rejected direct interpretation

For an ideal isolated monoprotic acid HA:

HA <-> H+ + A-

C = [HA] + [A-]

alpha = [A-]/C

Ka = [H+][A-]/[HA]

With no other important proton or charge sources and neglecting water ionization, [H+] approximately equals alpha C, giving:

Ka = C alpha^2/(1-alpha).

The campaign does not support inserting nominal n/V directly for C in these equations. For example, batch 1 had nominal C = 0.05556 mol/L and alpha = 0.068607. Their product is approximately 0.00381 mol/L, whereas its final pH of 3.8810 corresponds to hydrogen activity approximately 0.000132 relative to the standard-state convention. The mismatch is large, not a small rounding effect.

This mismatch does not prove any particular alternative. It shows that the package of assumptions—nominal loading equals dissolved acid concentration, the fraction refers to that same acid pool, ideal activities, and unbuffered charge balance—is untenable as a direct interpretation.

### 5.2 Conditional apparent acidity from the two channels

If alpha is interpreted as the dissociated fraction entering a Henderson–Hasselbalch-type relation, then:

pH = pKa_app + log10(alpha/(1-alpha))

and consequently:

pKa_app = 14q + log10((1-alpha)/alpha).

Applying this transformation to the first ten final assays gave:

| Batch | Derived pKa_app |
|---|---:|
| 1 | 5.0138 |
| 2 | 5.0318 |
| 3 | 5.0646 |
| 4 | 5.0257 |
| 5 | 4.9530 |
| 6 | 5.0293 |
| 7 | 4.9787 |
| 8 | 4.9987 |
| 9 | 4.9601 |
| 10 | 5.0959 |

Their mean is approximately 5.015. The repeated anchors likewise remain near 5.0. The descriptive range above is not a confidence interval.

Under this conditional interpretation, the archival pKa interval is displaced substantially below the observed channel-derived values. I would revise the working apparent pKa toward 5.02 rather than retain 4.66. However, a common pKa near 5.02 has not been shown to predict a broad response curve: q and alpha vary little, and two approximately constant channels naturally generate an approximately constant transformed value. Activity corrections, channel normalization, or mapping differences could also shift this apparent parameter.

### 5.3 Minimal effective process representation

A defensible representation of the available evidence is:

nominal recipe and preparation history
    -> unidentified mapping to effective chemical state
    -> pH, dissociation-fraction channel, and precipitation proxy
    -> instrument noise and bounded processing.

In equations, one could write:

C_eff = g(n, V, background state, preparation history)

q = f_q(C_eff, other effective variables) + measurement error

alpha = f_alpha(C_eff, other effective variables) + measurement error

P = f_P(C_eff, other effective variables) + measurement error.

The functions g and f are not identified. Within the sampled conditions, their composition is weakly responsive. An optional local constraint is the apparent pKa relation above, but it should remain conditional rather than hard-coded as established chemistry.

For interpolation near tested recipes, a near-constant baseline with uncertain small corrections is safer than an elaborate fitted mechanism. It is not evidence that the underlying state is truly constant everywhere.

## 6. Precipitation and coupling

Final precipitation proxies ranged from 0.142795 to 0.166348. The loading sweep at 0.018 L showed a modest increase from batch 3 to batch 5, while the extreme volume comparison showed a decrease on dilution. Conversely, both direct archival endpoint pairs showed an increase in P on dilution.

These observations do not support a single clean monotonic dependence on nominal concentration. They also do not demonstrate a causal dependence of P on alpha or pH. The experiment did not independently vary pH while holding all other effective variables fixed, and the measurement scatter is substantial relative to the contrasts.

Reasonable possibilities include an approximately constant baseline proxy, a weak chemical response obscured by noise, or a nonlinear transformation of an unobserved saturation variable. None permits converting P to solid moles or applying a solubility-product equation without additional calibration and species information.

The final equilibrium_residual values were zero or small, up to approximately 0.00403. Because these are bounded noisy diagnostics, zeros need not mean exact physical closure. The values do not rescue the failed identification of nominal loading with active acid concentration.

## 7. Competing explanations

### A. A buffered or background-dominated chemical state

An unobserved background acid–base pool could hold pH near 3.9 and make added reagent a weak perturbation. This explains response compression qualitatively. No buffer composition, capacity, or independent background concentration was measured, so this is a hypothesis rather than an identified mechanism.

### B. Transformed or bounded effective loading

The world may map nominal amount and volume to a normalized, capped, or otherwise transformed effective concentration. Broad nominal changes would then produce small changes in the acid channels. The observations are compatible with this, but do not reveal the transformation or any cap location.

### C. The added reagent is not the acid pool underlying the fraction

The anonymous limiting reagent may affect a different internal quantity from the dissociation channel. A label or operation-to-state mismatch would make an n/V acid model inappropriate. Component-0 testing did not resolve this because its operation was not independently chemically calibrated and its final comparison also changed preparation path.

### D. Instrument-channel coupling or a nearly fixed proxy state

Both q and alpha may be derived from shared internal benchmark variables rather than independent species determinations. That could generate a stable apparent pKa even without independently verified acid equilibria. The public calibration contract describes synthetic channel measurements but does not supply the hidden chemical mapping needed to exclude this explanation.

### E. Activity effects or solubility limitation

Strong nonideality or a solubility-limited dissolved pool could also compress responses. These explanations are not impossible, but the campaign contains no ionic-strength series, dissolved-versus-total assay, or calibrated solid measurement. Invoking them specifically would go beyond the evidence.

### F. Slow equilibration

Slow equilibration remains possible outside the tested timing. The single 60 s wait did not produce a large change, so a large response occurring within that interval is not supported. Much slower dynamics and effects hidden by the available precision remain unresolved.

These alternatives need not be mutually exclusive. The campaign constrains the overall recipe-to-observable response more strongly than it identifies the internal process.

## 8. Uncertainty

The declared final-assay noise scales were 0.002 for normalized pH and 0.006 for both alpha and P. Treating these as independent per-reading standard deviations gives approximate standard deviations for a two-final-assay difference of:

- 0.00283 in normalized pH, equivalent to 0.0396 pH units;
- 0.00849 in alpha;
- 0.00849 in P.

For the difference between two endpoint means, each based on two final assays, the corresponding nominal scales are 0.002 and 0.006. These are instrument-noise calculations, not comprehensive confidence intervals: process variability, correlations, and interpretation uncertainty are not fully known.

For the apparent pKa transformation near alpha = 0.075, propagation of the declared final-channel noise gives an uncertainty scale of roughly 0.047 pKa units per reading if q and alpha errors are independent. Systematic channel interpretation could produce a larger shift. Thus the repeated displacement from the archival pKa interval is meaningful conditionally, while the mechanistic meaning of that displacement remains uncertain.

The pH-meter fraction and precipitation channels were noisier than the final assay. They should not be pooled with equal weight. Repeated values displayed during termination were retained prior measurements, not new independent observations. Likewise, raw electrode, hydrogen, and processed pH fields from one packet are not separate experimental replicates.

## 9. Supported range and limits of extrapolation

Direct empirical support is limited to the actual sampled recipes:

- water-only preparations without catalyst;
- temperature near 298.15 K, without a designed temperature series;
- added amounts from 0.0001 to 0.040 mol;
- nominal water volumes from 0.002 to 0.080 L;
- mostly immediate observations, one 60 s hold, and one staged-dilution preparation;
- nominal concentrations approximately 0.00556–2.222 mol/L across the sampled combinations.

This was not a complete factorial design over amount and volume. Those endpoint ranges must not be read as validation of every combination inside a rectangle, nor as evidence for behavior outside it.

No claims are supported about other solvents, catalyst effects, broad temperature or pressure dependence, ionic strength, actual acid identity, actual solid identity, long-time behavior, or real aqueous samples. The environment is a bounded synthetic benchmark.

## 10. Conclusions and discriminating implications

The campaign supports three main conclusions:

1. The observed chemical channels are much less sensitive to nominal loading and dilution than an elementary isolated-acid model using C = n/V would predict.
2. A conditional pH–fraction apparent pKa is near 5.02, challenging the supplied archival pKa interval, but the narrow channel range prevents unique identification of an acid-dissociation mechanism.
3. Small dilution effects and precipitation responses remain incompletely resolved. The archival dilution increments are compatible with the data but are not precisely validated; no precipitation law was established.

If the same effective regime persists, additional nearby preparations would be expected to remain near the observed channel neighborhood. That is an interpolation hypothesis, not a verified general law. Distinguishing the competing explanations would require independent calibration of the active acid loading or dissolved species, more replicated dilution contrasts, and broader time or acid–base perturbations. Those measurements were not performed and are not implied by this report.

Batch 11 remains the recommended evidentiary anchor because it repeats the original undiluted recipe and connects the dilution, scale, and waiting comparisons. Its selection does not assert superior yield, superior physical equilibrium, or a higher scientific-confidence score. This report interprets the sealed campaign record without revising its completed handoff.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | acid_dissociation_fraction | 0.078 | 0.067 | 0.089 |
| Q01 | pH_normalized | 0.282 | 0.278 | 0.286 |
| Q01 | precipitation_signal | 0.152 | 0.139 | 0.165 |
| Q02 | acid_dissociation_fraction | 0.078 | 0.067 | 0.089 |
| Q02 | pH_normalized | 0.282 | 0.278 | 0.286 |
| Q02 | precipitation_signal | 0.152 | 0.139 | 0.165 |
| Q03 | acid_dissociation_fraction | 0.079 | 0.059 | 0.104 |
| Q03 | pH_normalized | 0.283 | 0.276 | 0.292 |
| Q03 | precipitation_signal | 0.151 | 0.129 | 0.173 |
| Q04 | acid_dissociation_fraction | 0.077 | 0.058 | 0.099 |
| Q04 | pH_normalized | 0.282 | 0.275 | 0.29 |
| Q04 | precipitation_signal | 0.153 | 0.132 | 0.175 |
| Q05 | acid_dissociation_fraction | 0.075 | 0.061 | 0.089 |
| Q05 | pH_normalized | 0.28 | 0.275 | 0.285 |
| Q05 | precipitation_signal | 0.155 | 0.139 | 0.171 |
| Q06 | acid_dissociation_fraction | 0.075 | 0.061 | 0.089 |
| Q06 | pH_normalized | 0.28 | 0.275 | 0.285 |
| Q06 | precipitation_signal | 0.155 | 0.139 | 0.171 |
| Q07 | acid_dissociation_fraction | 0.075 | 0.061 | 0.089 |
| Q07 | pH_normalized | 0.28 | 0.275 | 0.285 |
| Q07 | precipitation_signal | 0.155 | 0.139 | 0.171 |
| Q08 | acid_dissociation_fraction | 0.079 | 0.047 | 0.122 |
| Q08 | pH_normalized | 0.283 | 0.271 | 0.3 |
| Q08 | precipitation_signal | 0.151 | 0.117 | 0.184 |
| Q09 | acid_dissociation_fraction | 0.077 | 0.047 | 0.117 |
| Q09 | pH_normalized | 0.282 | 0.27 | 0.297 |
| Q09 | precipitation_signal | 0.153 | 0.12 | 0.186 |
| Q10 | acid_dissociation_fraction | 0.075 | 0.057 | 0.094 |
| Q10 | pH_normalized | 0.279 | 0.272 | 0.286 |
| Q10 | precipitation_signal | 0.157 | 0.137 | 0.181 |
| Q11 | acid_dissociation_fraction | 0.076 | 0.063 | 0.089 |
| Q11 | pH_normalized | 0.28 | 0.275 | 0.285 |
| Q11 | precipitation_signal | 0.155 | 0.14 | 0.171 |
| Q12 | acid_dissociation_fraction | 0.075 | 0.064 | 0.086 |
| Q12 | pH_normalized | 0.28 | 0.276 | 0.284 |
| Q12 | precipitation_signal | 0.155 | 0.142 | 0.168 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

These are predictions of the public processed final-assay channels, not latent chemical composition or environment confidence. The twelve completed batches showed q approximately 0.277–0.285, dissociation fraction approximately 0.064–0.087, and precipitation proxy approximately 0.143–0.166 despite large nominal concentration changes. I therefore use a pooled, weak-response baseline with small, strongly shrunk local adjustments. I do not identify added reagent concentration with dissolved acid concentration, enforce the archival pKa, or convert the precipitation proxy into solid mass. The reported lower80 and upper80 values are approximate marginal 80% predictive bounds for each new observation, not confidence intervals for a mean and not simultaneous coverage across metrics or queries. They incorporate the declared final-assay noise scales of 0.002 for normalized pH and 0.006 for each other channel, observed between-batch variation, and additional model uncertainty. Wider bounds are assigned to trace loading, concentration beyond the tested maximum, and unresolved dosing-path effects. Equal central predictions for matched-concentration or matched-total recipes express the absence of evidence for a directional difference; they do not establish mechanistic equivalence. Unlike the research batches, these queries omit a preceding pH-meter sample. I apply no speculative point correction for that omission because its chemical effect was not isolated. The intervals are judgmental extrapolative uncertainty assessments, not empirically validated coverage guarantees. No new experiments or hidden information were used.

**Q01**: This is near the low-loading observations in batches 3 and 9. I predict a slightly higher pH and dissociation fraction than the overall baseline, but shrink those adjustments toward the nearly flat response because the loading trend was weak.

**Q02**: The nominal concentration equals Q01, with twice its amount and volume. The matched-scale comparison in batches 1 and 10 did not resolve an independent scale effect. Equal point predictions express that lack of evidence, not proof that concentration alone controls the response.

**Q03**: The volume is within the sampled range, but the amount is tenfold below the lowest tested loading and nominal concentration is below the tested range. I retain a weak-response baseline with modest upward pH and dissociation adjustments. Wider, slightly asymmetric intervals allow an emerging dilution response without assuming an unverified ideal-acid law.

**Q04**: This shares Q03's extrapolative amount but has substantially less solvent. The fortyfold volume comparison in batches 8 and 9 produced only a small response, so I predict only a small difference from Q03. The intervals accommodate uncertainty about whether trace loading changes the effective regime.

**Q05**: The final totals, 0.002 mol and 0.024 L, are within the explored loading and volume ranges. I use the local baseline rather than extrapolating a strong concentration law. Interleaved dosing was not isolated experimentally, so the intervals include preparation-path uncertainty.

**Q06**: This has the same final totals as Q05 and Q07. No observed result justifies a directional effect of accumulating solvent before reagent. I therefore assign the same central prediction, while retaining uncertainty about operation order and incremental dosing.

**Q07**: Batch 7 supplied limited evidence about adding solvent after reagent, but its component choice and measurement sequence were confounded with preparation path. There is no defensible signed correction relative to Q05 or Q06. Equal predictions are a conservative working assumption rather than an established path-independence law.

**Q08**: The amount is one hundredfold below the minimum tested amount. The campaign does not identify a reliable slope into this trace-loading region, so I hold the central estimate near Q03 rather than impose an ideal-acid extrapolation. Substantially wider intervals represent possible breakdown of the weak-response regime.

**Q09**: This combines trace loading with a small but previously bracketed volume. I retain approximately the Q04 central state because no measured trace-loading law supports a larger adjustment. The broad intervals account for uncertain effective loading, background dominance, and possible changes in the proxy response.

**Q10**: Batch 5 tested this amount at 0.018 L and returned q = 0.277424, alpha = 0.078599, and P = 0.157516. The new nominal concentration, 6.67 mol/L, is threefold above the campaign maximum. I shrink toward the pooled baseline and widen intervals rather than assume a strong acidity shift or an unobserved precipitation threshold.

**Q11**: Amount and volume are individually within the sampled ranges, although their combination was not tested. Its nominal concentration is close to batch 4 and its amount matches batch 5. Those observations support a near-baseline response, with extra uncertainty for separating concentration, amount, and volume effects.

**Q12**: This is an interior interpolation in amount, volume, and nominal concentration. The nearly flat empirical model is better supported here than at the trace-loading or high-concentration boundaries. Intervals cover a new final-assay reading, including measurement variation and uncertainty in the weak recipe response.

## K2

# Retrospective review of the sealed campaign, K1 mechanism report, and Q predictions

I refer to the sealed mechanism report as K1 and the sealed blind predictions as Q. No prediction truth has been disclosed. This review does not revise either submission and uses only the existing public record. Proposed experiments below are hypothetical, not performed.

## 1. Initial claims: supported, challenged, or untested

The initial information did contain substantive scientific claims. The archival relationship specified an effective pKa interval of 4.6094–4.7094 and, for 0.001 mol diluted from 0.018 to 0.054 L at 298.15 K, increments of 0.003494987 in normalized pH and 0.008187416 in dissociation fraction. These claims need separate assessments.

**The small local dilution increments were not decisively contradicted, but were not established.** Batches 1 and 2 produced increments of approximately 0.003847 in normalized pH and 0.005464 in fraction. That initial agreement was encouraging but weak. Repeated endpoints, batches 11 and 12, produced increments of only 0.000163 in normalized pH and 0.007171 in fraction. The two fraction contrasts had the same sign, whereas the pH contrast was poorly reproducible at that precision. K1 therefore said: “The archival dilution increments are compatible with the data but are not precisely validated.” Compatibility here means absence of a sufficiently strong contradiction, not positive validation of the numerical law.

**The archival pKa was challenged, conditional on the channel interpretation.** K1 calculated pKa_app = 14q + log10((1-alpha)/alpha), obtaining 4.953–5.096 across the first ten finals, centered near 5.015. This is substantially above the archival interval. I did not retain 4.66 as the working apparent parameter after recognizing this discrepancy. The qualification is important: the evidence challenges the archival value as interpreted through these public channels; it does not establish a molecular acid constant because the relevant species and activity mapping were not independently identified.

**The simple identification of nominal n/V with isolated-acid concentration was contradicted.** This was my working interpretation, not a complete law supplied by the archive. The 400-fold loading contrast between batches 3 and 5 produced almost identical final fractions, 0.078831 and 0.078599, rather than the substantial decrease expected for an ordinary unbuffered acid. The broad volume contrast in batches 8 and 9 reinforced the problem. I revised this interpretation during the campaign: the notebook after batch 5 already described the loading-as-acid model as challenged and considered operation semantics, background effects, and timing.

The first batch alone contained a warning: its pH and fraction were difficult to reconcile with nominal acid concentration under ideal unbuffered charge balance. I did not immediately quantify that inconsistency. Instead, I initially prioritized the archival endpoint contrast. That was delayed use of a diagnostic, although I subsequently revised the model rather than continuing to assert it as established.

**Much of the broader material information remained untested.** The solvent identities and anonymous catalyst descriptions were not hypotheses that this water-only campaign could validate. No solvent comparison, catalyst comparison, temperature series, or chemical identity determination was performed. The public normalization q = pH/14 was used as a measurement definition, not established experimentally. The interpretation of precipitation as a bounded proxy was respected; it was never calibrated against solid mass.

## 2. Experiments that changed the interpretation, and the basis for choosing them

The decisive experiments were not necessarily those with the largest channel differences.

**Batches 1 and 2 established the reference comparison but did not establish the mechanism.** Their conditions came directly from the archival anchor. They showed that the claimed small increments were plausible at first sight. Their main value was a concrete reference for replication and later perturbations.

**Batches 3–5 caused the principal model revision.** They varied loading at the same 0.018 L volume. The unexpectedly narrow pH and fraction response made ordinary n/V acid chemistry untenable as a direct interpretation. This was stronger evidence than agreement with one small dilution increment because the nominal perturbation was much larger. The choice of a broad loading sweep was based on a general identifiability argument: a mechanism should survive changes large enough to separate its predictions from assay noise. The exact loading levels were exploratory choices, not inferred optimal design points.

**Batch 6 tested a specific rescue explanation suggested by the preceding results.** The 60 s wait was chosen after considering whether immediate measurements might precede a chemical-state update or relaxation. Its final channels remained near the baseline. That weakened a large relaxation within 60 s, but did not identify kinetics. The choice of 60 s was not grounded in a measured timescale; it was an unverified practical probe.

**Batch 7 explored operation identity and preparation history, but confounded them.** It used component 0 and staged dilution, with a pH-meter reading before dilution and a final assay afterward. Its final fraction of 0.083749 was not a dramatic departure from other dilute preparations. However, component choice, dilution path, and instrument changed together. K1 explicitly acknowledged that this could not prove operation equivalence or path independence. The experiment addressed a plausible concern, but its design was weaker than a clean one-factor contrast.

**Batches 8 and 9 reinforced the response-compression conclusion.** A forty-fold volume difference at 0.001 mol gave only approximately 0.01443 pH units of final difference. This was a powerful negative result for the elementary concentration model, even though it could not distinguish background buffering from a transformed input mapping.

**Batch 10 was conceptually useful but weakly discriminating in practice.** Doubling both amount and volume tested nominal concentration equivalence. K1 correctly warned that agreement also follows from a nearly constant response. Once the broad sweeps had shown response compression, this design had less discriminatory power than it would have had in a strongly responsive system.

**Batches 11 and 12 changed my assessment of precision.** They were selected to repeat the archival endpoints rather than expand the chemistry. The repeated pH contrast was much smaller than the first, and the dilute precipitation proxy changed from 0.153389 in batch 2 to 0.166348 in batch 12. These results directly discouraged fitting a precise local slope or interpreting similarly sized proxy differences mechanistically.

The chronology matters: the initial archive motivated the anchor tests; the flat loading response motivated the timing and operation-semantic concerns; later replication motivated caution about small contrasts. I should not present the final list of competing explanations as if each had been fully articulated before the first experiment.

## 3. Current competing explanations and what is distinguishable

The most important distinction is between an identifiable empirical response and an unidentified internal mechanism. K1 summarized the evidence as a “weakly responsive chemical-channel state” and represented the process as an unknown mapping from recipe and history to effective state and then to public channels.

The leading explanations remain:

1. **A background-dominated or buffered acid–base state.** Added material could be a small perturbation to an unobserved pool.
2. **A transformed or bounded effective loading.** Nominal amount and volume might enter a normalized, capped, or otherwise compressed internal variable.
3. **A mismatch between the addition control and the acid pool represented by the fraction.** The anonymous reagent need not be the species assumed by an ordinary acid mass balance.
4. **Shared channel construction or a nearly fixed proxy state.** The apparent pKa could reflect coupled public-channel definitions rather than independently verified species equilibrium.
5. **Physical nonideality, dissolved-pool limitation, or slow dynamics.** These remain possible but were not independently characterized.

The campaign can distinguish the observed response from an ideal isolated monoprotic acid with C = n/V over the tested range. It also weakens the claim that a large missing response would appear simply after waiting 60 s under the batch-6 conditions.

It cannot distinguish buffering from capped loading, identify the input transformation, or separate independent chemistry from channel coupling. A stable transformed pKa is not enough: as K1 noted, nearly constant q and alpha automatically yield a nearly constant transformed value. The observations also cannot establish a precipitation threshold, solid identity, or solubility product.

Some explanations are more elaborate than others. For example, invoking solubility limitation would require explaining why the precipitation proxy barely changes and why the dissolved acid pool behaves as observed. That makes it less directly supported, but not experimentally excluded. Simplicity favors a weak-response empirical model for prediction; it does not make that model a complete mechanism.

## 4. One additional legal complete experiment: hypothetical choice

If one additional complete batch and its required resources were permitted, I would choose **0.000001 mol added reagent in 0.075 L water, near 298.15 K, no catalyst, no deliberate hold**, followed by one pH-meter measurement, explicit termination, and a final assay. These are previously available operation types and legal addition magnitudes. This would be an extension of the campaign, not an action legal under its already exhausted assay budget.

I would measure the same public chemical channels and inspect the raw pH packet as well as the final processed estimates. I would not regard hydrogen and electrode fields from that packet as independent chemical assays.

The rationale is retrospective: after sealing Q, the largest unresolved predictive risk is whether the weak-response regime persists at trace loading. This experiment directly probes that vulnerability while retaining a volume already bracketed by batches 2 and 9. Its preceding pH sample would make it slightly different from Q08, so it would not be an exact replication of that query.

Possible interpretations would be:

- **Channels remain near q approximately 0.28, alpha approximately 0.08, and P approximately 0.15:** this would extend support for a background-dominated, mapped, or nearly fixed response down to much smaller loading. It still would not distinguish those explanations.
- **A large, coherent increase in pH and dissociation:** this would show that the plateau does not extend to trace loading and strengthen an effective-concentration interpretation with a transition between regimes. It would not by itself establish the ideal n/V law or locate the transition.
- **pH changes substantially but alpha does not, or vice versa:** this would challenge extrapolation of the apparent pKa relation and elevate channel-mapping or multicomponent explanations.
- **The precipitation proxy changes strongly while acid channels remain near baseline:** this would favor some decoupling of precipitation from the inferred acid state.
- **The two instruments disagree beyond their expected uncertainty:** the immediate priority would become measurement interpretation or operation-dependent state changes, not fitting a new equilibrium equation.

One batch could reveal a regime change but could not reliably establish a small difference or a new law. This choice sacrifices another baseline replicate in order to address the most consequential extrapolation uncertainty. It is a hypothetical preference made now, not a claim about the original planning.

## 5. Identifiability versus operational score

The research objective, rather than the native score, drove the campaign. I varied loading and volume, repeated anchors, and tested time and path because those changes could challenge an explanation. I did not select catalysts, solvent categories, or control settings to maximize equilibrium_confidence or the scalar score.

This matters because equilibrium_confidence is an environment diagnostic. Treating it as my scientific confidence would have encouraged selecting favorable diagnostic values instead of exposing model failures. The recommendation of batch 11 was explicitly evidentiary, not a declaration that it had the best score.

The main trade-offs were within research design:

- Broad perturbations gave strong power to reject the naive acid model but left few replicates for estimating small slopes.
- Endpoint replication improved uncertainty assessment but consumed batches that could have tested a new regime.
- Using one pH-meter measurement in every batch supplied cross-instrument context but consumed the full intermediate-measurement allowance. It left no multiple-reading trajectory within batch 6.
- Batch 7 attempted to investigate two questions at once and lost identifiability through confounding.
- Batch 10 tested scale invariance, but its value was limited by the already flat response.

There is no evidence that I deliberately sacrificed identifiability to improve score. Conversely, I cannot quantify a score sacrificed for science because I did not run an optimization counterfactual. The defensible statement is that score maximization was not the selection criterion. The campaign also ended after 62 operations because the twelve completed batches and assay allocations were exhausted; unused operations could not substitute for additional chemical observations.

## 6. Underused evidence and weaknesses in the blind predictions

### Evidence not fully exploited

**Raw measurement information was used unevenly.** I inspected the first pH artifact but did not systematically analyze all raw pH packets or final-assay spectra and calibration metadata. The record supplied processed estimates, so this does not invalidate their use. It does mean I did not fully check whether raw signals could clarify cross-instrument differences, clipping, or uncertainty. I cannot now claim what those uninspected details would have shown.

**Intermediate and final readings were not analyzed jointly.** They offered more observations than the twelve final values alone. However, they had different declared noise and sampling states, and batch 7 changed preparation between measurements. Proper use would require explicit weighting and careful separation of comparable and noncomparable pairs. I mostly used them qualitatively rather than fitting a measurement model.

**The charge-balance inconsistency could have been quantified earlier.** K1 eventually contrasted batch 1's alpha times nominal concentration, approximately 0.00381 mol/L, with hydrogen activity implied by pH, approximately 0.000132 relative to the standard state. That discrepancy was available early and could have accelerated the move away from nominal loading as acid concentration.

**No formal comparison of simple empirical models was performed.** A constant model, amount-only model, volume-only model, and log-concentration model could have been compared cautiously using the existing readings. The small, uneven design would still prevent strong conclusions, but it would have made the degree of shrinkage in Q more transparent. Instead, Q used judgmental local adjustments around a pooled baseline.

**The apparent pKa calculation was conditional and partly post hoc.** It was useful for testing compatibility with the archive, but it should not be mistaken for an independently calibrated mechanistic fit. K1 stated that limitation; the remaining weakness is that a narrow response range permits many equally good channel relations.

### Least reliable predictions

**Q08 and Q09 are the least reliable.** Their 0.000001 mol loading is one hundredfold below the lowest tested amount. K1 explicitly limited support to 0.0001–0.040 mol and admitted that the effective loading map was unknown. Although Q widened its intervals, it still concentrated them around the plateau: for Q08, alpha was bounded at 0.047–0.122 and normalized pH at 0.271–0.300. Those bounds do not accommodate a substantial transition toward a dilute-acid regime. Without truth feedback, I cannot say they missed, but they may be too narrow for the structural uncertainty admitted in K1.

**Q03 and Q04 share the same problem to a lesser degree.** Their amounts are tenfold below the tested minimum. The intervals were wider than interior intervals, but remained based primarily on persistence of the flat response. That assumption was not established experimentally.

**Q10 is the principal high-concentration risk.** Its nominal concentration is 6.67 mol/L, threefold above the campaign maximum. The amount and volume were separately familiar, but their combination was not. A threshold or a nonlinear response could occur there, and the precipitation interval of 0.137–0.181 may underrepresent that possibility.

**Q05–Q07 rely on an unverified equivalence assumption.** Equal point predictions are defensible when there is no evidence for the sign of an order effect. They are not evidence that the three paths are equivalent. Their identical, relatively modest intervals may not fully represent the lack of a clean path experiment. Batch 7 does not resolve this because it also changed the addition operation and measurement sequence.

Q01, Q02, Q11, and especially the interior Q12 are better grounded as local empirical predictions. Nevertheless, even their nominal 80% coverage was not calibrated with held-out observations. The twofold scale result does not uniquely prove concentration control, and the high-amount/high-volume combination in Q11 was not directly tested.

### Consistency with K1

Q was verbally consistent with K1: it explicitly used a weak-response baseline, labeled extrapolations, and called the intervals judgmental rather than validated. The possible inconsistency is numerical rather than verbal. K1 allowed major uncertainty in the recipe-to-state mapping; some extrapolative Q intervals may be too concentrated to express that uncertainty fully.

All Q recipes also omit the preceding pH-meter sample used in the research batches. Q acknowledged the omission and applied no speculative correction. That was reasonable, but it remains a systematic preparation difference whose effect was not isolated.

No conclusion about actual predictive accuracy is available until truth is disclosed. These are weaknesses in justification and uncertainty representation, not retrospective claims of observed failure.

## 7. Limits of the sealed recommendation and how it could be evaluated

The sealed recommendation was batch 11: 0.001 mol in 0.018 L water, selected as a repeated archival reference. Its final q was 0.279368, alpha 0.070222, and P 0.152489. K1 described it as an “evidentiary anchor,” not an optimized recipe.

That recommendation has several limitations:

- It is tied to one water-only recipe near 298.15 K.
- It was repeated only once under the same immediate-measurement protocol, in batch 1.
- It does not represent the full volume, loading, time, or preparation-path range.
- Its status as a useful reference does not identify the chemical species or the internal mechanism.
- It is not automatically the best recipe for prediction, diagnostic score, precision, or any physical production objective.

The existing repeat is informative: batch 11 minus batch 1 differed by approximately 0.002151 in normalized pH, 0.001614 in fraction, and 0.007446 in precipitation proxy. These are compatible with the measurement scales, but two realizations cannot characterize repeatability tails, drift, or rare failures.

A future repeatability assessment would use independent repetitions of the exact operation sequence, including measurement configuration and sampling order, with predeclared summaries of bias and spread. Local robustness would require separate, small perturbations of amount, volume, hold time, and temperature rather than changing them together. A preparation with no intermediate sample should be compared directly with the sampled protocol to determine whether the reference transfers to final-assay-only queries.

Cross-material generalization would require new evidence for other solvent categories and addition operations. The named solvent identities do not justify transferring the fitted response because the public contract describes categorical benchmark effects. Cross-world generalization would require independent campaigns with the public controls and calibration checked again; the apparent pKa and plateau must not be presumed invariant.

Finally, “sample-internal highest” and “proven optimal” are different claims. I did not recommend batch 11 because it was the sample-internal maximum of the scalar score or any chemical channel. Even if a batch had the highest observed score among the twelve, noise, sparse coverage, and untested interactions would prevent a claim of optimality. Here the intended value of the recommendation is reproducible scientific reference, not superiority. That narrower claim is useful, but it too would benefit from more replication and explicit local-robustness testing.

## EQS

### dissociation precipitation

**assessment**: indeterminate

**competing explanation**: An approximately constant precipitation-proxy baseline with measurement variability explains the observations without requiring coupling to dissociation. A weak continuous response is also compatible, but neither its slope nor its causal dependence on dissociation is identified. A threshold outside the observed effective-state range, or obscured by the unknown recipe-to-state mapping, cannot be excluded. The direct dilution comparisons increased the precipitation proxy (batches 1 to 2 and 11 to 12), whereas the broader volume comparison decreased it (batches 8 to 9). These inconsistent directions and limited replication do not establish a continuous or threshold-like relationship.

**supported range**: The twelve final assays covered dissociation fractions 0.06353–0.08748, precipitation proxies 0.14280–0.16635, and normalized pH 0.27722–0.28550, corresponding to pH approximately 3.881–3.997. Preparations used water without catalyst near 298.15 K, added amounts 0.0001–0.040 mol, and nominal volumes 0.002–0.080 L across the sampled combinations. These were not a full factorial design. The narrow observed chemical-channel range, despite broad nominal concentration changes, limits inference about transitions. The precipitation signal is not calibrated solid mass.

### effective pka

**estimate**: not estimated

**identifiable**: False

**lower80**: not estimated

**rationale**: I abstain from assigning an identified world-level effective pKa and an 80% interval. Conditional on treating the public dissociation fraction as a monoprotic acid fraction, the transformation pKa_app = 14*pH_normalized + log10((1-alpha)/alpha) gives a descriptive center near 5.02; the first ten final assays yielded 4.953–5.096. That range is not an 80% interval. This conditional channel summary challenges the archival 4.609–4.709 interval under the same interpretation, but does not identify a predictive acid-equilibrium law. Batches 3 and 5 increased nominal loading 400-fold at fixed volume while their fractions remained nearly identical, 0.078831 and 0.078599. Batches 8 and 9 changed volume fortyfold but differed by only about 0.0144 pH units. Principal confounders are the unknown mapping from added reagent to the acid pool, possible background buffering or transformed effective concentration, activity effects, and possible shared construction of the public channels. Nearly constant pH and fraction can generate a nearly constant transformed pKa without demonstrating the proposed relationship. An interval based only on propagated instrument noise would omit these unresolved structural uncertainties.

**upper80**: not estimated

### path dependence

**assessment**: indeterminate

**rationale**: No reproducible staged-addition effect was demonstrated, but final-state dominance was not established either. Batch 7 used component 0 in 0.018 L, underwent a pH-meter measurement, and then received 0.036 L additional water. Its final normalized pH, fraction, and precipitation proxy were 0.281407, 0.083749, and 0.159733. Direct preparations at nominally corresponding totals, batches 2 and 12, gave 0.281063/0.074072/0.153389 and 0.279531/0.077393/0.166348, respectively. These results show no compelling large path effect, but batch 7 confounded addition path with the addition operation and sampled before rather than after final dilution; it also lacked a staged-path replicate. Batch 10's matched-concentration scale comparison and batch 6's 60 s wait supplied useful context but were not controlled staged-order comparisons. Thus final-state-only prediction is a parsimonious working assumption, not an experimentally distinguished mechanism, and small or condition-dependent path effects remain unresolved.
