# EQ-W03--Opaque — final public report

World `EQ-W03`; prior arm `Opaque`; status `completed`. The effective result came from `attempt-01`.

## Source campaign

The campaign contains 12/12 completed batches and 60 recorded operations. Exact replay: `True`.

| Batch | pH normalized | Acid dissociation | Precipitation signal | Residual |
|---:|---:|---:|---:|---:|
| 1 | 0.278419 | 0.0691395 | 0.138775 | 0.00740432 |
| 2 | 0.27673 | 0.0676593 | 0.154874 | 0.00164676 |
| 3 | 0.280012 | 0.0745743 | 0.157113 | 0 |
| 4 | 0.28017 | 0.0708781 | 0.1494 | 0.000940216 |
| 5 | 0.27707 | 0.0594161 | 0.163109 | 0.00247906 |
| 6 | 0.278402 | 0.0707086 | 0.155014 | 0 |
| 7 | 0.27652 | 0.0618293 | 0.155749 | 0.00309748 |
| 8 | 0.274979 | 0.0717164 | 0.157798 | 0 |
| 9 | 0.281322 | 0.0698297 | 0.159713 | 0 |
| 10 | 0.277008 | 0.0763263 | 0.158363 | 0.00123332 |
| 11 | 0.280334 | 0.0716861 | 0.162807 | 0 |
| 12 | 0.275628 | 0.0821678 | 0.152765 | 0.00182736 |

## Sealed scientific account

### K1 report

Mechanistic report

1. Experimental basis

I completed 12 independent water-only batches spanning a crossed loading–volume design. Total reagent loading n was 0.0050, 0.0125, 0.0225, or 0.0350 mol; liquid volume V was 0.030, 0.050, or 0.080 L. Thus the nominal total concentration C_T = n/V covered 0.0625–1.1667 mol L^-1, an 18.67-fold range. Every batch received one pre-termination pH-meter measurement and one post-termination final assay. No catalyst, heating, waiting, pH titration, or nonaqueous solvent was tested.

The following are the final-assay observations. pH is calculated from the public definition pH = 14 pH_normalized.

Batch | V (L) | n (mol) | C_T (mol L^-1) | pH | dissociated fraction α | precipitation proxy P | equilibrium residual
1 | 0.030 | 0.0050 | 0.1667 | 3.8979 | 0.06914 | 0.13877 | 0.00740
2 | 0.030 | 0.0125 | 0.4167 | 3.8742 | 0.06766 | 0.15487 | 0.00165
3 | 0.030 | 0.0225 | 0.7500 | 3.9202 | 0.07457 | 0.15711 | 0
4 | 0.030 | 0.0350 | 1.1667 | 3.9224 | 0.07088 | 0.14940 | 0.00094
5 | 0.050 | 0.0050 | 0.1000 | 3.8790 | 0.05942 | 0.16311 | 0.00248
6 | 0.050 | 0.0125 | 0.2500 | 3.8976 | 0.07071 | 0.15501 | 0
7 | 0.050 | 0.0225 | 0.4500 | 3.8713 | 0.06183 | 0.15575 | 0.00310
8 | 0.050 | 0.0350 | 0.7000 | 3.8497 | 0.07172 | 0.15780 | 0
9 | 0.080 | 0.0050 | 0.0625 | 3.9385 | 0.06983 | 0.15971 | 0
10 | 0.080 | 0.0125 | 0.1563 | 3.8781 | 0.07633 | 0.15836 | 0.00123
11 | 0.080 | 0.0225 | 0.2813 | 3.9247 | 0.07169 | 0.16281 | 0
12 | 0.080 | 0.0350 | 0.4375 | 3.8588 | 0.08217 | 0.15276 | 0.00183

Batch 6 was selected before this report as the replay/recommendation anchor because it is a central design point and has paired pH-meter and final-assay observations. It was not selected because it maximized a chemical outcome.

2. Principal effective mechanism

The strongest identifiable relationship is consistent with a monoprotic acid-dissociation coordinate:

HA ⇌ H+ + A−

α = [A−]/([HA] + [A−])

For this coordinate, the Henderson–Hasselbalch form gives

α = 1/(1 + 10^(pKa_eff − pH)),

or equivalently

pKa_eff = pH + log10((1 − α)/α).

Applying this transformation independently to the 12 final assays gives pKa_eff values from 4.907 to 5.078, with mean 5.014 and empirical standard deviation 0.049. The corresponding effective dissociation constant is approximately

Ka_eff = 10^−5.014 ≈ 9.68 × 10^−6.

This batch-by-batch invariance is substantially clearer than any direct dependence on loading or volume. I therefore regard an effective pKa near 5.01 as the main supported local relationship. “Effective” is essential: the experiment does not establish a named acid, ideal activities, a unique microscopic species, or even that the two reported channels are analytically independent.

A compact empirical description over the tested region is therefore:

C_T = n/V,
pH ≈ 3.893 + ε_pH,
α ≈ 1/(1 + 10^(5.014 − pH)) + ε_α,
P ≈ 0.1555 + ε_P.

Here ε denotes measurement variation and any unresolved recipe dependence. This is a bounded local model, not a general aqueous-chemistry law.

3. Loading, dilution, and buffering behavior

The final-assay pH_normalized mean was 0.27805, corresponding to pH 3.8927. Its complete observed range was only pH 3.8497–3.9385, or 0.089 pH unit, despite the 18.67-fold concentration range. The dissociated fraction had mean 0.07049 and range 0.05942–0.08217.

That behavior is not what a simple, isolated, unbuffered weak acid at analytical concentration C_T would predict. In the usual dilute limiting approximation,

[H+] ≈ sqrt(Ka C_T),
α ≈ sqrt(Ka/C_T).

Across an 18.67-fold change in C_T, that model predicts about 0.636 pH unit of change and a 4.32-fold change in α. The actual spans were 0.089 pH unit and a 1.38-fold α ratio. Consequently, I reject the isolated-unbuffered-weak-acid model as a sufficient explanation within this world.

The data instead support a pH-clamped or background-dominated equilibrium regime. Plausible realizations include an unreported buffer reservoir, a counterion/background acid-base pool much larger than the variable free contribution, or an environment-defined latent pH setpoint. Under any of these realizations, loading changes total material while pH remains near 3.9; α then follows the approximately constant pH through the effective pKa relation.

A purely descriptive least-squares fit to pH_normalized using n and V was

pH_normalized ≈ 0.27890 − 0.0452 n + 0.0000317 V,

with n in mol and V in L. Across the complete tested loading interval, the fitted loading term represents only about −0.019 pH unit; the fitted volume contribution is negligible. This fit is descriptive only: there are no exact recipe replicates, only 12 points, and the small coefficient should not be interpreted as a separately identified physical constant.

The batches that most changed the interpretation were 2–4. After batch 1 suggested pH 3.898, α = 0.0691, and pKa_eff = 5.027, raising C_T at the same 0.030 L volume to 0.4167, 0.7500, and 1.1667 mol L^-1 did not cause the large pH decrease or dissociation decrease expected for an isolated weak acid. Batches 5–12 then reproduced the near-constant pH/α regime at larger volumes and lower concentrations. In particular, batch 9 at the lowest concentration, 0.0625 mol L^-1, still gave pH 3.939 and α = 0.0698, while batch 4 at the highest concentration, 1.1667 mol L^-1, gave pH 3.922 and α = 0.0709.

4. Precipitation proxy

The final precipitation proxy had mean 0.15546 and range 0.13877–0.16311. No reproducible monotonic dependence on C_T, n, V, pH, or α was resolved.

Volume-group means were 0.1500 at 0.030 L, 0.1579 at 0.050 L, and 0.1584 at 0.080 L. The apparently lower 0.030 L mean is largely driven by batch 1. Loading-group means for increasing n were 0.1539, 0.1561, 0.1586, and 0.1533, which is shallow and nonmonotonic.

Specific contrasts argue against a simple concentration-triggered precipitation rule. At the same 0.005 mol loading, dilution from batch 1 (0.030 L, C_T = 0.1667 mol L^-1) to batch 9 (0.080 L, C_T = 0.0625 mol L^-1) increased P from 0.1388 to 0.1597, opposite to the simplest expectation that concentration alone promotes precipitation. At 0.035 mol loading, batches 4 and 12 changed C_T from 1.1667 to 0.4375 mol L^-1 but gave similar P values of 0.1494 and 0.1528.

Moreover, the approximate ionized-material coordinate αC_T varies by roughly an order of magnitude and more across the grid, while P remains near 0.155. Thus P is not identified as a direct linear proxy for dissolved A− concentration. Reasonable interpretations are:

• a nearly constant background precipitation/turbidity signal;
• a proxy already on a broad plateau or saturated region;
• precipitation controlled by an unobserved counter-species whose availability is effectively fixed;
• a nonlinear threshold lying outside the tested range;
• a readout dominated by baseline or matrix effects rather than precipitated amount.

Because P is explicitly a bounded normalized proxy, I do not equate it with solid mass, solubility, or yield. No physical solid was isolated or quantified, so a solubility product cannot be estimated from these data.

5. Measurement coupling and uncertainty

The final-assay instrument has lower declared noise for these channels than the pH meter, so the numerical model above uses the final assays as the principal evidence. The intermediate readings broadly occupied the same regime but sometimes differed substantially from their final values. For example, batch 6 gave pH_normalized = 0.28832, α = 0.08497, and P = 0.15666 by pH meter, versus 0.27840, 0.07071, and 0.15501 in the final assay. Batch 12 gave α = 0.04015 by pH meter and 0.08217 by final assay. With no waiting or kinetic intervention between these measurements, such differences are more safely treated as instrument/readout variability than as demonstrated chemical evolution.

The final equilibrium residual was between 0 and 0.00740. This supports internal numerical consistency but does not establish that the proposed microscopic mechanism is unique. Likewise, equilibrium_confidence is an environment diagnostic, not my epistemic confidence, and I do not use it as evidence strength or optimize the explanation around it.

Uncertainty in pKa_eff is summarized by the empirical batch spread, approximately 5.014 ± 0.049 standard deviation, rather than by an overly narrow standard error. Systematic calibration, correlated channel construction, activity effects, and design-point dependence are not removed by averaging. The precipitation data justify only a local baseline estimate near 0.155, with individual values spanning approximately ±0.012 around it; they do not justify a fitted precipitation law.

6. Identifiability and competing explanations

The following explanations are observationally equivalent or nearly equivalent in this campaign:

A. Buffered weak acid: a real HA/A− equilibrium with pKa near 5.01 is embedded in a stronger background buffer that holds pH near 3.9.

B. Background-ion or activity-controlled equilibrium: the reagent participates in acid dissociation, but fixed counterions, ionic strength, or nonideal activities dominate the proton balance. The fitted pKa is then conditional rather than thermodynamic.

C. Shared latent-coordinate readout: pH and α are two calibrated outputs of the same hidden equilibrium variable. Their Henderson–Hasselbalch consistency may therefore reflect sensor/model construction rather than two independent chemical measurements.

D. Multispecies equivalence: several acids, protonation sites, complexes, or soluble/insoluble forms could collectively produce the same apparent single-pKa response over this narrow pH window.

For precipitation, a constant background, a saturated response, and an unobserved limiting counter-species are all compatible with the observations. The present grid cannot distinguish them.

7. Scope and unsupported extrapolations

The supported domain is water, ambient telemetry near 297 K and atmospheric pressure, n = 0.005–0.035 mol, V = 0.030–0.080 L, and C_T = 0.0625–1.1667 mol L^-1, using the specified bounded synthetic instruments. Within that domain, pH near 3.9, α near 0.07, effective pKa near 5.01, and an approximately flat precipitation proxy near 0.155 are supported.

Outside that domain, constancy is an extrapolation. I cannot infer behavior at very low loading, beyond 1.17 mol L^-1, at other temperatures, after long equilibration, under titration, with catalysts, or in ethanol, acetonitrile, or toluene. I also cannot identify kinetic rates, actual dissolved concentrations, solid composition, activity coefficients, buffer capacity, molecular identity, stoichiometry beyond the effective one-proton coordinate, or a thermodynamic solubility product.

The clearest discriminating future tests—stated only as predictions, not performed here—would be exact recipe replicates; controlled acid/base titration at fixed C_T; extension to much lower C_T; independent quantification of dissolved and solid material; and perturbation of background ionic composition. An isolated weak-acid model predicts substantial pH and α changes upon large dilution, whereas the favored clamped-background model predicts continued near-constant pH until buffer capacity or the latent setpoint regime is exceeded.

Overall conclusion: this bounded world is best described locally as a pH-clamped aqueous acid-dissociation coordinate with pKa_eff ≈ 5.01. Total loading and dilution strongly change nominal concentration but have little resolved effect on pH or dissociation over the tested window. The precipitation channel is approximately constant and cannot yet be assigned a unique concentration, ionization, or solubility mechanism.

### Blind Q predictions

| Query | Metric | Estimate | 80% lower | 80% upper |
|---|---|---:|---:|---:|
| Q01 | acid_dissociation_fraction | 0.071 | 0.056 | 0.086 |
| Q01 | pH_normalized | 0.278 | 0.273 | 0.283 |
| Q01 | precipitation_signal | 0.137 | 0.115 | 0.154 |
| Q02 | acid_dissociation_fraction | 0.071 | 0.056 | 0.086 |
| Q02 | pH_normalized | 0.278 | 0.273 | 0.283 |
| Q02 | precipitation_signal | 0.137 | 0.115 | 0.154 |
| Q03 | acid_dissociation_fraction | 0.236 | 0.18 | 0.3 |
| Q03 | pH_normalized | 0.322 | 0.312 | 0.334 |
| Q03 | precipitation_signal | 0.003 | 0 | 0.025 |
| Q04 | acid_dissociation_fraction | 0.073 | 0.058 | 0.091 |
| Q04 | pH_normalized | 0.2795 | 0.274 | 0.285 |
| Q04 | precipitation_signal | 0.005 | 0 | 0.055 |
| Q05 | acid_dissociation_fraction | 0.071 | 0.059 | 0.082 |
| Q05 | pH_normalized | 0.278 | 0.274 | 0.282 |
| Q05 | precipitation_signal | 0.152 | 0.14 | 0.164 |
| Q06 | acid_dissociation_fraction | 0.071 | 0.059 | 0.082 |
| Q06 | pH_normalized | 0.278 | 0.274 | 0.282 |
| Q06 | precipitation_signal | 0.152 | 0.14 | 0.164 |
| Q07 | acid_dissociation_fraction | 0.071 | 0.059 | 0.082 |
| Q07 | pH_normalized | 0.278 | 0.274 | 0.282 |
| Q07 | precipitation_signal | 0.152 | 0.14 | 0.164 |
| Q08 | acid_dissociation_fraction | 0.563 | 0.43 | 0.7 |
| Q08 | pH_normalized | 0.366 | 0.348 | 0.385 |
| Q08 | precipitation_signal | 0.002 | 0 | 0.02 |
| Q09 | acid_dissociation_fraction | 0.214 | 0.16 | 0.27 |
| Q09 | pH_normalized | 0.318 | 0.308 | 0.329 |
| Q09 | precipitation_signal | 0.003 | 0 | 0.025 |
| Q10 | acid_dissociation_fraction | 0.071 | 0.045 | 0.1 |
| Q10 | pH_normalized | 0.278 | 0.268 | 0.289 |
| Q10 | precipitation_signal | 0.155 | 0.125 | 0.18 |
| Q11 | acid_dissociation_fraction | 0.071 | 0.059 | 0.083 |
| Q11 | pH_normalized | 0.278 | 0.274 | 0.282 |
| Q11 | precipitation_signal | 0.155 | 0.143 | 0.167 |
| Q12 | acid_dissociation_fraction | 0.07 | 0.061 | 0.079 |
| Q12 | pH_normalized | 0.278 | 0.275 | 0.281 |
| Q12 | precipitation_signal | 0.153 | 0.141 | 0.165 |

Predictions use the previously sealed interpretation without further experimentation. For unsaturated trace batches I applied a monoprotic weak-acid relation with effective pKa 5.014. The observed plateau implies an approximate dissolved concentration cap of 0.0018 mol L^-1 from [H+]/alpha; above it, pH_normalized and dissociation were held near their empirical final-assay means of 0.27805 and 0.07049. Precipitation is the least identified channel: I treated it as negligible below the inferred cap and approaching the observed mean of 0.15546 as excess loading grows. Intervals combine observed final-assay scatter with additional extrapolation and threshold uncertainty. Equivalent final totals receive equivalent predictions because the completed campaign supplied no evidence for addition-order memory.

### K2 retrospective

1. Initial claims: supported, challenged, or untested

The initial packet contained almost no substantive chemical mechanism to confirm. It explicitly said that no task-specific property dossier was supplied, `prior_record` was null, and experimental evidence was authoritative. Thus there was no numerical archival pKa, solubility threshold, buffer capacity, or precipitation law against which the campaign could be adjudicated.

Several definitional claims were respected rather than experimentally established: pH_normalized = pH/14; acid dissociation is a fraction; precipitation_signal is a bounded proxy; and equilibrium_confidence is an environment diagnostic rather than epistemic confidence. K1 followed these distinctions, especially by refusing to interpret precipitation_signal as solid mass and by not treating equilibrium_confidence as evidence strength.

The initial description of the world as a weak-acid/precipitation slice received qualitative support. Across the final assays, pH and dissociation were consistent with the effective relation

α = 1/(1 + 10^(pKa_eff − pH)),

with K1 estimating pKa_eff = 5.014 and an empirical batch standard deviation of 0.049. This supports an acid-dissociation coordinate, but it does not verify a unique molecular acid or independent measurement of both variables.

The campaign produced direct counterevidence to a simple isolated, unbuffered weak-acid model. As K1 stated, the 18.67-fold nominal concentration range should have produced about 0.636 pH unit of change and a 4.32-fold change in α under that model, whereas the observed spans were only 0.089 pH unit and 1.38-fold. K1 did revise the interpretation accordingly, favoring a “pH-clamped or background-dominated equilibrium regime.” This was not merely an absence of counterevidence: it was affirmative evidence against the unbuffered model within the tested domain.

No initial substantive claim was contradicted and then knowingly retained without revision, because no such quantitative initial mechanism was supplied. However, several possibilities remained entirely untested: nonaqueous solvents, catalyst effects, temperature dependence, kinetic equilibration, addition-order memory, true solid formation, and behavior below 0.0625 mol L^-1. The absence of evidence against these effects must not be confused with evidence that they are absent.

2. Experiments that formed or changed the interpretation

Batch 1 supplied the first local anchor: pH 3.8979, α = 0.06914, and an implied pKa_eff of 5.027. On its own, that batch could not distinguish a weak acid, a buffered system, or a shared latent readout.

Batches 2–4 were the most consequential experimental block. At fixed V = 0.030 L, nominal concentration rose from 0.1667 mol L^-1 in batch 1 to 1.1667 mol L^-1 in batch 4, but pH and α remained near the same regime. This caused the decisive rejection of the isolated-unbuffered interpretation.

Batches 5–12 extended the plateau across larger volumes. The most persuasive contrast was between batch 9, the lowest tested concentration at 0.0625 mol L^-1, and batch 4, the highest at 1.1667 mol L^-1. They gave pH values of 3.9385 and 3.9224 and α values of 0.06983 and 0.07088, respectively. That comparison strongly supported a plateau but did not identify its physical cause.

The precipitation interpretation was shaped by contrasts such as batches 1 and 9. They used the same 0.005 mol loading but gave precipitation signals of 0.1388 and 0.1597 after dilution from 0.030 to 0.080 L. This ran opposite to a simple “higher nominal concentration gives more precipitation” rule. Batches 4 and 12 likewise had substantially different concentrations but similar precipitation signals, 0.1494 and 0.1528. These observations motivated K1’s conclusion that no monotonic precipitation law was resolved.

The overall 3 × 4 loading–volume grid was chosen principally from the research goal and resource limits, not from prior data. Water was selected because the task concerned an aqueous equilibrium. The crossed design was intended to separate amount and volume, while one pH-meter measurement per batch provided a second readout before the required final assay. The precise grid, the assumption that ambient no-wait operation was sufficient, and the decision not to test trace loading were design guesses rather than conclusions established by initial evidence.

An important weakness is that the design was not adapted after batches 2–4 revealed an early plateau. A stronger adaptive campaign would have moved some later batches several orders of magnitude lower in concentration. Instead, all 12 batches remained at or above 0.0625 mol L^-1. That produced good confirmation of the plateau but poor identification of what creates it.

3. Current competing mechanisms and what can be distinguished

The leading explanations remain:

A. Background-buffer or pH-setpoint mechanism. A fixed acid/base reservoir holds pH near 3.9; the reported α then follows from an effective pKa near 5.01.

B. Solubility or precipitation cap. Excess reagent precipitates, pinning dissolved analytical concentration and therefore pH and α. This explanation became prominent only during the blind-prediction reasoning, when the combination [H+]/α was noted to be about 0.0018 mol L^-1. It was not an established conclusion in K1, and invoking it for Q predictions was an extrapolative hypothesis.

C. Shared latent-coordinate readout. pH and α may be calibrated outputs of the same hidden equilibrium coordinate. Their Henderson–Hasselbalch consistency would then not constitute two independent confirmations of a molecular mechanism.

D. Nonideal or multispecies equilibrium. Fixed counterions, ionic strength, complexes, multiple protonation sites, or several acid pools could produce an apparently constant conditional pKa over the observed window.

The experiment distinguishes these candidates from the simple isolated-unbuffered weak-acid model because the expected concentration response is absent. It also disfavors a simple monotonic dependence of precipitation_signal on nominal concentration within the tested range.

It cannot distinguish A from B because every tested concentration may lie on the same plateau. It cannot distinguish a genuine HA/A− equilibrium from C because no independent species concentration was measured. It cannot separate buffering, nonideal activities, or multispecies behavior because ionic composition and pH were never independently perturbed. It also cannot establish whether precipitation_signal reports precipitated amount, saturation state, turbidity, or a calibrated latent proxy.

4. One additional complete experiment

If exactly one additional legal experiment were allowed, I would use 0.075 L water and 0.000010 mol reagent, giving C_T = 1.33 × 10^-4 mol L^-1. I would measure once with the pH meter before termination, then terminate and obtain the required final assay. This is the same condition later presented as blind query Q03, but no truth for Q03 has been supplied; proposing it here does not use outcome feedback.

This condition is more than two orders of magnitude below the lowest experimental concentration and approximately an order of magnitude below the hypothesized 0.0018 mol L^-1 cap. Its possible outcomes would be highly discriminating:

• If pH_normalized rose toward approximately 0.322, α rose toward approximately 0.24, and precipitation_signal collapsed toward zero, that would support an unsaturated weak-acid regime connected to a solubility-limited plateau.

• If pH_normalized remained near 0.278 and α near 0.07, the precipitation-cap explanation would be weakened. A background buffer, fixed latent setpoint, or shared readout would become more plausible.

• If pH and α shifted as expected for dilution but precipitation_signal remained near 0.155, the acid equilibrium and precipitation proxy would likely be governed by different latent variables or the latter would contain a substantial baseline.

• If the pH meter and final assay disagreed strongly, as they did for α in batch 12, the main update would concern measurement coupling rather than chemistry. It would strengthen the need for replication and independent calibration before choosing among mechanisms.

A single experiment still could not estimate a complete transition curve, but it would provide more discrimination than another point on the already well-sampled plateau.

5. Tradeoff between identifiability and operational score

The research objective explicitly concerned characterization rather than yield or process optimization. The campaign therefore used a structured loading–volume matrix rather than searching for the largest native score. No catalyst, heating schedule, or solvent screen was used to improve equilibrium_confidence, and K1 correctly treated that quantity as a diagnostic rather than scientific confidence.

This choice likely sacrificed operational score in favor of mechanistic coverage. Conversely, there is no evidence that a high-scoring recipe was selected at the expense of identifiability. Batch 6 was recommended because it was a central comparison point with paired measurements, not because it was claimed to optimize an outcome.

Nevertheless, the design did not maximize mechanistic identifiability as well as it could have. Once a plateau was apparent, continuing a balanced grid of relatively high concentrations produced redundant confirmation. Exact replicates, trace-loading points, a blank-like condition, or an independently imposed pH would have been more diagnostic. Thus the main tradeoff was not optimization versus science; it was orderly factorial coverage versus adaptive regime discovery. The campaign favored the former.

6. Underused evidence and reliability of the blind predictions

The paired pH-meter and final-assay measurements were not fully exploited. K1 cited batch 6 and batch 12 to show discrepancies, but it did not fit instrument-specific bias or variance. Batch 12 was especially important: α changed from 0.04015 by pH meter to 0.08217 by final assay without a deliberate kinetic treatment. That observation limits how confidently either channel can be treated as an independent chemical state variable.

The precipitation observations were also difficult to use. They were nearly constant and lacked a monotonic loading response. K1 appropriately left several explanations open. In the later Q predictions, however, I adopted a more specific precipitation-cap model and estimated near-zero precipitation below an inferred threshold. That step went beyond what K1 had established.

The derived quantity [H+]/α ≈ 0.0018 mol L^-1 was not discussed in K1. It is suggestive of a capped dissolved concentration only if charge balance gives [A−] ≈ [H+] and α refers to the same analytical pool. Neither assumption was independently established. Treating 0.0018 mol L^-1 as a physical threshold in the Q rationale was therefore speculative.

The least reliable blind predictions are Q03, Q08, and Q09 because they lie far below the observed concentration domain. Their intervals were probably too narrow. For example, Q03 predicted pH_normalized 0.312–0.334, excluding the near-0.278 plateau favored in K1’s background-clamp explanation. Q08 and Q09 similarly excluded or nearly excluded that competing regime. This conflicts with K1’s explicit statement that behavior below 0.0625 mol L^-1 was unsupported.

Q04 is also structurally uncertain because it was placed near the inferred threshold. Its precipitation interval of 0–0.055 excluded the approximately 0.155 background plateau, even though K1 explicitly retained a constant-background explanation. Q01 and Q02 likewise relied on an unverified formula for the amount above the cap; their precipitation intervals may be too narrow.

Q10 is the most extreme high-side extrapolation at 6.67 mol L^-1. Its intervals, especially 0.125–0.180 for precipitation_signal, likely understate uncertainty about capacity limits, nonideality, clipping, and whether such a concentrated state obeys the same mechanism.

Q05–Q07 assumed exact order invariance because their final totals match. That is reasonable for a true equilibrium, but addition-order memory was never tested. Their identical, relatively narrow intervals omit this structural uncertainty. Q11 and Q12 are comparatively better supported because their concentrations lie within or near the observed plateau domain.

Thus several Q intervals were inconsistent with the scope and competing explanations stated in K1. A better calibrated prediction would have used mixture-like or much wider intervals that retained both the background-clamped and unsaturated weak-acid possibilities. This assessment is based solely on internal consistency; no prediction truths have been revealed.

7. Limitations of the sealed recommendation

The sealed recommendation selected batch 6: 0.0125 mol reagent in 0.050 L water. Its value is that it is a central, interpretable anchor, not that it is proven optimal. It was observed once, has no exact replicate, and its pre-termination and final measurements were not identical. Its pH-meter α was 0.08497, whereas its final-assay α was 0.07071. That alone prevents treating the recipe as a precisely reproducible standard without further evidence.

Repeatability should be tested with multiple exact repetitions of batch 6, preserving operation order and timing and comparing both instruments. Local robustness should be tested by small independent perturbations around 0.0125 mol and 0.050 L, plus equivalent-concentration recipes at different amounts and volumes. Addition-order variants like Q05–Q07 would test whether only final totals matter.

Cross-material generalization would require repeating the local design with the other allowed solvents and, if scientifically relevant, catalysts. The initial material packet warned that these are categorical benchmark effects; water-only evidence cannot establish transfer to ethanol, acetonitrile, or toluene. Cross-world generalization would require the same preregistered local design across independently instantiated worlds or seeds, with all failures retained.

Finally, “sample-internal highest” and “proven optimal” are different claims. Batch 6 was not sealed as an optimizer at all. Even if it happened to have the largest value of a diagnostic or scalar score among the 12 observed batches, that would only be an in-sample maximum over a sparse grid. It would not demonstrate global optimality, causal superiority, repeatability, or transfer. The defensible claim is narrower: batch 6 is a convenient central completed experiment for replay and comparison.

### EQ-specific supplement

Effective pKa identifiable: `True`; estimate `5.014`; 80% interval `[4.95, 5.08]`.

A local effective pKa is identifiable from the paired final-assay pH and dissociation values using pKa_eff = pH + log10((1-alpha)/alpha). The 12 batch estimates had mean 5.014, empirical standard deviation 0.049, and range 4.907–5.078. The interval is deliberately based on batch-level spread rather than a narrow standard error because calibration coupling, activity effects, and shared latent readout remain possible. This is a conditional effective pKa, not an identified thermodynamic constant or molecular identity.

Path-dependence assessment: `indeterminate`.

All source batches used the same simple order: water addition followed by one reagent addition, termination, and final assay. No source experiment varied staged-addition order while holding final amount and volume fixed, so reproducible path dependence was not tested. Endpoint comparisons such as batch 6 (0.0125 mol in 0.050 L) and batch 11 (0.0225 mol in 0.080 L) are broadly consistent with a final-state plateau, but they are not path-matched experiments. Final-state dominance is therefore plausible but not established.

Dissociation-precipitation assessment: `indeterminate`.

Supported range: Water-only batches with 0.005–0.035 mol reagent, 0.030–0.080 L volume, and 0.0625–1.1667 mol L^-1 nominal concentration; observed pH was 3.850–3.939, dissociation fraction 0.0594–0.0822, and precipitation signal 0.1388–0.1631. Within this range neither a continuous trend nor a threshold crossing was resolved.

Competing explanation: The precipitation proxy may be a nearly constant background or an already saturated readout rather than a response coupled directly to dissociation. A solubility-limited dissolved pool is also compatible with the plateau, but no transition was observed.
## Blind-prediction evaluation

| Metric | MAE | Empirical 80% coverage | Mean width | Interval score |
|---|---:|---:|---:|---:|
| acid_dissociation_fraction | 0.0123254 | 0.9 | 0.06325 | 0.0832972 |
| pH_normalized | 0.00318294 | 0.816667 | 0.0141667 | 0.0228781 |
| precipitation_signal | 0.0157441 | 0.833333 | 0.0315 | 0.104175 |

## Scope and privacy

Reference truth was released only after every EQS response was sealed. The environment-derived equilibrium-confidence field is neither an agent uncertainty estimate nor a score. Authentication material, raw model events, session identifiers, and usage accounting are excluded.
