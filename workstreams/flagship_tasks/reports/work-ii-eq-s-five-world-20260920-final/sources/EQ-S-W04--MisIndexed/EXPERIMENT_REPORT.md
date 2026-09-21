# EQ-S-W04--MisIndexed — final English experiment report

World `EQ-S-W04`; information arm `MisIndexed`; task `mechanism characterization`; effective status `completed`; result origin `original`.

## Source campaign

The autonomous campaign completed 12/12 batches and 60 recorded operations. Exact replay is `True`; rollbacks: 0.

| Batch | Solvent L | Reagent mol | Measurements | pH normalized | Free dissociation | Precipitation signal | Residual |
|---:|---:|---:|---|---:|---:|---:|---:|
| 1 | 0.04 | 0.005 | ph_meter, final_assay | 0.150966 | 0 | 0.00171093 | 0.00649248 |
| 2 | 0.04 | 0.015 | ph_meter, final_assay | 0.111847 | 0.00326445 | 0.00323649 | 0.00290189 |
| 3 | 0.04 | 0.025 | ph_meter, final_assay | 0.0982722 | 0.00998882 | 0.00318413 | 0.00435527 |
| 4 | 0.04 | 0.035 | ph_meter, final_assay | 0.0862094 | 0.000298357 | 0.00791367 | 0.00109801 |
| 5 | 0.06 | 0.005 | ph_meter, final_assay | 0.163725 | 0 | 0 | 0 |
| 6 | 0.06 | 0.015 | ph_meter, final_assay | 0.129971 | 0 | 0.00753933 | 0 |
| 7 | 0.06 | 0.025 | ph_meter, final_assay | 0.109485 | 0.00142264 | 0 | 0 |
| 8 | 0.06 | 0.035 | ph_meter, final_assay | 0.101998 | 0 | 0 | 0 |
| 9 | 0.08 | 0.005 | ph_meter, final_assay | 0.169127 | 0.00799128 | 0.00416605 | 0 |
| 10 | 0.08 | 0.015 | ph_meter, final_assay | 0.14097 | 0 | 0 | 0.00195261 |
| 11 | 0.08 | 0.025 | ph_meter, final_assay | 0.120884 | 0.00681754 | 0 | 0 |
| 12 | 0.08 | 0.035 | ph_meter, final_assay | 0.11281 | 0.00520561 | 0.00135872 | 0 |

### Sealed evidentiary anchor

Batch `3`: This high-loading, low-volume batch anchors the concentrated end of the loading–dilution series and returned measurable values for all three target observables.

## K1 — sealed mechanistic report

MECHANISTIC REPORT

1. Scope and experimental basis

I completed 12 water-only equilibrium batches spanning reagent amounts of 0.005, 0.015, 0.025, and 0.035 mol and initial water volumes of 0.040, 0.060, and 0.080 L. The resulting nominal loading concentration C0 = n0/V0 ranged from 0.0625 to 0.875 mol L^-1. Every batch received an in-process pH-meter measurement and a post-termination final assay. No catalyst, heating, deliberate waiting period, nonaqueous solvent, or independent metal-ion addition was tested. Accordingly, the report concerns the ambient-temperature aqueous slice actually observed, not the full legal intervention space.

An instance-specific structural prior was supplied; therefore it is not the case that no instance prior was available. The prior proposed the direct-free-ion network

HA(aq) ⇌ H+(aq) + A−(aq)
M+(aq) + A−(aq) ⇌ MA(s),

with no distinct dissolved MA intermediate. No task-specific nominal property dossier or numerical constants were supplied: the material-information dossier itself was null. Thus the experiment could test the proposed topology qualitatively, but it could not compare fitted constants with dossier values.

2. Direct observations

The final-assay results were:

Batch | water (L) | reagent (mol) | C0 (mol L^-1) | normalized pH | free acid-dissociation fraction | precipitation proxy
1 | 0.040 | 0.005 | 0.1250 | 0.150966 | 0.000000 | 0.001711
2 | 0.040 | 0.015 | 0.3750 | 0.111847 | 0.003264 | 0.003236
3 | 0.040 | 0.025 | 0.6250 | 0.098272 | 0.009989 | 0.003184
4 | 0.040 | 0.035 | 0.8750 | 0.086209 | 0.000298 | 0.007914
5 | 0.060 | 0.005 | 0.08333 | 0.163725 | 0.000000 | 0.000000
6 | 0.060 | 0.015 | 0.2500 | 0.129971 | 0.000000 | 0.007539
7 | 0.060 | 0.025 | 0.41667 | 0.109485 | 0.001423 | 0.000000
8 | 0.060 | 0.035 | 0.58333 | 0.101998 | 0.000000 | 0.000000
9 | 0.080 | 0.005 | 0.06250 | 0.169127 | 0.007991 | 0.004166
10 | 0.080 | 0.015 | 0.18750 | 0.140970 | 0.000000 | 0.000000
11 | 0.080 | 0.025 | 0.31250 | 0.120884 | 0.006818 | 0.000000
12 | 0.080 | 0.035 | 0.43750 | 0.112810 | 0.005206 | 0.001359

Batch 3 was sealed as the evidentiary anchor because it sampled the concentrated region and returned nonzero values on all three public response channels. Selection as an anchor does not make it representative of every channel: its acid fraction, 0.009989, was among the largest observed and should not be treated as a universal value.

The pH response was strong and orderly. At fixed 0.040 L, raising loading from 0.005 mol in batch 1 to 0.035 mol in batch 4 lowered normalized pH from 0.150966 to 0.086209. At fixed 0.005 mol, dilution from 0.040 L in batch 1 to 0.080 L in batch 9 raised normalized pH from 0.150966 to 0.169127. Similar monotonic loading effects occurred in the 0.060- and 0.080-L blocks.

The in-process pH measurements independently showed the same broad concentration response. For example, batch 1 gave 0.152871 in process and 0.150966 by final assay; batch 12 gave 0.107993 and 0.112810, respectively. These differences are consistent with measurement variation and do not establish time evolution because only one pre-termination time point was collected per batch.

In contrast, the free-fraction and precipitation channels remained near their lower boundary. Across final assays, their respective means were 0.002916 and 0.002426. Both are below the declared final-assay standard deviation of 0.006 for the corresponding channel, and zero clipping produces an upward bias in such nonnegative averages. The largest free-fraction estimate was 0.009989 in batch 3; the largest precipitation estimate was 0.007914 in batch 4. Neither channel varied monotonically with C0. Linear descriptive slopes against ln(C0) were only about +0.00017 for free fraction and +0.00066 for precipitation proxy, much smaller than the pointwise noise scale.

Final equilibrium residuals ranged from 0 to 0.00649. The reported equilibrium-confidence values ranged from approximately 0.652 to 0.699. Equilibrium confidence is an environment diagnostic, not my scientific confidence, and I do not use it as evidence for topology identification.

3. Empirical loading–dilution relationship

Over the measured range, the simplest descriptive equation for normalized pH y is

y = 0.08362 − 0.03203 ln(C0),

where C0 is in mol L^-1. The root-mean-square residual over the 12 final assays is approximately 0.00216 normalized-pH units, close to the declared assay noise of 0.002.

A fit that allowed amount and volume to enter independently gave

y = 0.09344 − 0.03161 ln(n0) + 0.03486 ln(V0).

For a response determined only by concentration n0/V0, the amount and volume coefficients should have equal magnitude and opposite signs. Their observed near-symmetry supports concentration as the principal coupled variable. The small coefficient mismatch is not sufficient evidence for an independent total-amount or vessel-volume effect.

Because normalized pH equals pH/14, the first equation is equivalent to approximately

pH = 1.171 − 1.032 log10(C0).

The slope is close to −1 rather than the ideal dilute weak-acid limiting slope of −1/2. Equivalently, translating pH directly to hydrogen activity gives a descriptive relationship aH ≈ 0.065 C0; the batchwise inferred ratios ranged approximately from 0.0567 to 0.0725. This is a compact empirical description, not an identified dissociation fraction or a fitted thermodynamic Ka. Activities, sensor-channel definitions, precipitation coupling, and unknown background charge prevent that interpretation.

4. Plausible equilibrium network and balances

A defensible encompassing network retains the supplied acid step and treats precipitation as an optional branch:

HA(aq) ⇌ H+(aq) + A−(aq),     Ka = aH aA/aHA
M+(aq) + A−(aq) ⇌ MA(s),     Ksp = aM aA when solid is present.

If s is the amount of solid MA and no other A-bearing species exist, the A-unit balance is

n0 = nHA + nA− + s.

If the analytical free-dissociation fraction is defined on the total introduced A basis, then fA = nA−/n0. If instead it is normalized only to dissolved acid, then fA = nA−/(nHA+nA−). The public channel name alone does not identify which denominator is used, so I do not choose between them.

For the metal component, a minimal balance would be

nM,0 = nM+ + s,

but nM,0 and even the source of M+ were not independently observed or manipulated. Electroneutrality would require

[H+] + [M+] + Σ positive background charge = [A−] + [OH−] + Σ negative background charge.

The precipitation equilibrium is more accurately written with complementarity conditions:

s ≥ 0,  aM aA ≤ Ksp,  and  s(Ksp − aM aA) = 0.

The measured precipitation signal P is only a bounded proxy. A general observation model is P = g(s/V, supersaturation, particle response), where g is unknown and need not be linear. Consequently, a near-zero P does not quantify a solid mass without calibration.

This one network can explain all three channels in the limited sense that increasing C0 raises hydrogen activity and lowers normalized pH, while either a large effective Ksp, little available M+, or an inactive precipitation branch leaves free A− and the precipitation proxy near their detection boundaries. Thus the channels are not mutually inconsistent with one equilibrium system. However, the evidence does not show that their small fluctuations share a causal precipitation equilibrium: only the pH channel exhibits a resolved concentration response.

5. How the experiments formed and revised the account

Batch 1 established an acidic response at C0 = 0.125 mol L^-1 while both secondary channels were effectively zero. Batches 2–4 then increased loading at fixed 0.040 L. Their systematic pH fall demonstrated a real loading effect, but the absence of corresponding monotonic changes in free fraction or precipitation immediately weakened the expectation that the proposed solid branch would be visibly activated by concentration.

Batches 5–8 repeated the loading series at 0.060 L. The pH values again ordered principally by concentration, whereas the two secondary channels alternated between zero and small positive estimates. Batches 9–12 extended dilution to 0.080 L and confirmed that dilution reverses the loading effect on pH. The near-opposite fitted coefficients for ln(amount) and ln(volume) arose from the complete 3-by-4 design and caused me to prefer concentration coupling over separate amount and volume terms.

The combined series therefore revised the supplied account as follows: the acidification component remains plausible and is strongly supported phenomenologically, but the direct precipitation edge is only an admissible latent branch, not an observed active process. The claim that there is no dissolved MA intermediate was left untested, because no species-resolved measurement distinguished free M+, free A−, dissolved MA, and solid MA. The data neither require nor directly contradict such an intermediate.

6. Topology claim versus refitting constants

A topology claim asks which species and edges exist—for example, whether precipitation is direct from M+ and A−, whether dissolved MA exists, or whether no precipitation chemistry occurs. Refitting constants inside the supplied topology changes Ka, Ksp, activity coefficients, background-ion levels, or the proxy calibration while retaining the same species graph.

The present observations do not identify the topology. Within the supplied topology, one can fit an effectively inactive solid branch by choosing a sufficiently large Ksp, low available M+, or weak proxy response. That is parameter refitting, not evidence that the direct-free-ion edge is correct. Conversely, adding a dissolved MA intermediate and choosing its formation constant so that its abundance is negligible produces essentially the same observables. Removing the precipitation edge entirely also fits the near-zero precipitation series. These models are observationally equivalent under the interventions performed.

Therefore the supported topology claim is deliberately narrower: there is an acid-loading process that couples reagent concentration to hydrogen activity. A separate A-bearing free channel and a possible precipitation channel may coexist, but neither the direct M+ + A− → MA(s) edge nor the absence of dissolved MA is identified.

7. Competing explanations

Reasonable alternatives include:

(a) Effective strong-acid or fixed-yield dissociation. The nearly −1 log-concentration slope and aH/C0 near 0.065 can arise from an approximately concentration-independent proton-releasing fraction over this bounded range, with no active precipitation.

(b) Weak-acid equilibrium with nonideal activities. A conventional HA equilibrium can mimic the observed slope if activity coefficients, background ionic strength, or coupled equilibria vary with loading. Without activity or composition measurements, Ka is not identifiable.

(c) Direct precipitation with an inactive or weakly observed branch. The supplied network may be correct, but the tested ion products may remain below effective saturation, the metal inventory may be small, or the public proxy may have low gain.

(d) Dissolved complexation before precipitation. HA dissociation could be coupled to M+ + A− ⇌ MA(aq), followed optionally by MA(aq) ⇌ MA(s). If dissolved MA were spectroscopically silent to the public channels, this topology would reproduce the observations.

(e) Background buffering or counterion chemistry. An unobserved buffer or spectator-ion balance could control hydrogen activity while leaving the reported free-A and precipitation proxies near zero.

(f) Observation-map ambiguity. The acid-dissociation fraction and precipitation proxy may be nonlinear, differently normalized functions of hidden species. In that case their small values cannot be compared directly with the approximately 0.065 ratio inferred from pH.

The current data favor none of alternatives (b)–(f) uniquely. Alternative (a) is the most parsimonious phenomenological description but should not be elevated to a molecular topology.

8. Identifiable and unidentifiable quantities

Identifiable within the study range are the direction and approximate magnitude of the normalized-pH response to concentration, the near-equivalence of increased volume and reduced amount through C0, and the fact that final free-fraction and precipitation signals were not resolved as systematic concentration responses.

Not identifiable are Ka, Ksp, activities, the M+ inventory, background electrolyte composition, solid mass, the precipitation-proxy calibration, the exact denominator of the free-fraction channel, the existence or absence of dissolved MA, kinetic equilibration time, temperature dependence, catalyst effects, solvent effects, hysteresis, nucleation barriers, and whether small nonzero secondary-channel readings are chemical signal or clipped noise.

9. Supported range and status of claims

Observation: The table above reports measurements at 12 exact amount–volume combinations, all in water under ambient telemetry. Normalized pH covered 0.0862–0.1691, free fraction 0–0.00999, and precipitation proxy 0–0.00791.

Interpolation: Within n0 = 0.005–0.035 mol, V0 = 0.040–0.080 L, and C0 = 0.0625–0.875 mol L^-1, the log-concentration equation is a well-supported descriptive interpolant for normalized pH. Within this rectangle, both secondary channels should be described as near-zero and unresolved rather than assigned a monotonic equation.

Extrapolation: Predictions outside those amount, volume, or concentration bounds are unsupported. In particular, the fitted logarithmic pH equation must not be extended toward zero concentration, extreme concentration, different temperatures, other solvents, catalyst addition, or added metal. A precipitation threshold outside the sampled range remains possible.

Conjecture: The acid equilibrium HA ⇌ H+ + A− is a plausible molecular interpretation of the pH response. The direct-free-ion precipitation edge and absence of aqueous MA are conjectural under this evidence. The numerical relation aH ≈ 0.065 C0 is empirical and must not be interpreted as a universal dissociation constant.

10. Overall conclusion

One encompassing equilibrium network can accommodate all three public channels, but the experiment resolves only its acidification response. Loading and dilution act primarily through nominal concentration: more reagent lowers normalized pH, while dilution raises it, with a nearly log-linear response. The free acid-dissociation and precipitation channels remain at the lower boundary without systematic concentration dependence. The supplied direct-free-ion precipitation topology is therefore not contradicted, because its solid branch can be inactive, but it is not positively supported and is not distinguishable from a no-precipitation model or a model containing dissolved MA. Changing Ka, Ksp, background-ion levels, or sensor gains within the supplied graph would be constant refitting; it would not validate the topology. Species-resolved metal/anion measurements and interventions on metal loading or saturation would be required to discriminate those alternatives.

## Q — sealed blind predictions

| Query | Metric | Estimate | 80% lower | 80% upper |
|---|---|---:|---:|---:|
| Q01 | pH_normalized | 0.333 | 0.27 | 0.4 |
| Q01 | acid_dissociation_fraction | 0.08 | 0 | 0.26 |
| Q01 | precipitation_signal | 0.0024 | 0 | 0.04 |
| Q02 | pH_normalized | 0.259 | 0.225 | 0.295 |
| Q02 | acid_dissociation_fraction | 0.015 | 0 | 0.07 |
| Q02 | precipitation_signal | 0.0024 | 0 | 0.025 |
| Q03 | pH_normalized | 0.202 | 0.183 | 0.222 |
| Q03 | acid_dissociation_fraction | 0.005 | 0 | 0.025 |
| Q03 | precipitation_signal | 0.0024 | 0 | 0.015 |
| Q04 | pH_normalized | 0.15 | 0.14 | 0.16 |
| Q04 | acid_dissociation_fraction | 0.003 | 0 | 0.011 |
| Q04 | precipitation_signal | 0.0024 | 0 | 0.012 |
| Q05 | pH_normalized | 0.106 | 0.096 | 0.116 |
| Q05 | acid_dissociation_fraction | 0.003 | 0 | 0.01 |
| Q05 | precipitation_signal | 0.0024 | 0 | 0.012 |
| Q06 | pH_normalized | 0.076 | 0.06 | 0.092 |
| Q06 | acid_dissociation_fraction | 0.003 | 0 | 0.012 |
| Q06 | precipitation_signal | 0.0024 | 0 | 0.015 |
| Q07 | pH_normalized | 0.106 | 0.093 | 0.119 |
| Q07 | acid_dissociation_fraction | 0.003 | 0 | 0.012 |
| Q07 | precipitation_signal | 0.0024 | 0 | 0.015 |
| Q08 | pH_normalized | 0.141 | 0.131 | 0.151 |
| Q08 | acid_dissociation_fraction | 0.003 | 0 | 0.011 |
| Q08 | precipitation_signal | 0.0024 | 0 | 0.012 |
| Q09 | pH_normalized | 0.172 | 0.163 | 0.182 |
| Q09 | acid_dissociation_fraction | 0.003 | 0 | 0.012 |
| Q09 | precipitation_signal | 0.0024 | 0 | 0.012 |
| Q10 | pH_normalized | 0.187 | 0.172 | 0.202 |
| Q10 | acid_dissociation_fraction | 0.004 | 0 | 0.018 |
| Q10 | precipitation_signal | 0.0024 | 0 | 0.015 |
| Q11 | pH_normalized | 0.202 | 0.178 | 0.225 |
| Q11 | acid_dissociation_fraction | 0.005 | 0 | 0.025 |
| Q11 | precipitation_signal | 0.0024 | 0 | 0.018 |
| Q12 | pH_normalized | 0.202 | 0.184 | 0.221 |
| Q12 | acid_dissociation_fraction | 0.005 | 0 | 0.025 |
| Q12 | precipitation_signal | 0.0024 | 0 | 0.015 |

### Q rationales

- **Q01**: This concentration is 150-fold below the lowest observed concentration. The pH estimate extrapolates the sealed log-concentration relationship, while its wide interval allows low-concentration curvature and approach toward the water limit. Model averaging assigns some probability to increased free dissociation on dilution, although the measured free-fraction channel was boundary-limited. Precipitation is expected to remain negligible.

- **Q02**: This remains well below the experimental concentration range. Log-concentration extrapolation predicts substantially higher normalized pH than in the research batches. A modest free-fraction increase is allowed because dilution could expose a low-concentration dissociation regime, but zero remains plausible. There is no empirical basis for a resolved precipitation response.

- **Q03**: At 0.025 M this is a moderate extrapolation below the observed 0.0625 M boundary. The concentration model gives normalized pH near 0.202. The secondary channels are predicted close to their clipped-noise baseline, with extra upper uncertainty for a possible low-concentration dissociation transition.

- **Q04**: The concentration exactly matches research batch 1, whose final normalized pH was 0.150966 with both secondary responses near zero. The smaller absolute scale is outside the tested volume range, so the interval includes a possible weak scale effect, but concentration remains the dominant predictor.

- **Q05**: A concentration of 0.5 M lies inside the observed concentration range, between several measured high-loading batches. The fitted concentration response gives normalized pH near 0.106. Neither free fraction nor precipitation showed a resolved trend in this region, so both remain near the boundary baseline.

- **Q06**: This is a high-concentration extrapolation beyond the observed maximum of 0.875 M. The log-concentration model predicts further acidification, but nonideality or saturation could bend the response, producing a wider interval. The research supplied no evidence for activation of either secondary channel at high loading.

- **Q07**: This has the same 0.5 M concentration as Q05 but one-quarter of its amount and volume. The sealed account predicts approximately the same response because amount and volume acted mainly through their ratio. The very small volume is outside the research range, so the interval is wider than for Q05.

- **Q08**: The 0.1667 M concentration lies inside the observed range and between the batch-1 and batch-10 concentration anchors. Concentration interpolation gives normalized pH near 0.141. The smaller volume adds modest scale uncertainty, while both secondary channels remain unresolved.

- **Q09**: The concentration equals research batch 9, which returned normalized pH 0.169127, free fraction 0.007991, and precipitation 0.004166; those secondary values were not repeated systematically and were comparable to assay noise. The fitted multi-batch concentration relationship gives 0.172, with the interval covering the direct anchor.

- **Q10**: At 0.04 M this is a limited dilution extrapolation below the measured range. The pH estimate follows the observed logarithmic dilution response. The free-fraction interval allows a small low-concentration increase, but the point estimate remains near the boundary behavior; precipitation remains unsupported.

- **Q11**: This is the small-scale member of the 0.025 M control set. Concentration invariance gives the same central predictions as Q03 and Q12. Its volume and amount are both farther below the research design, so its intervals are widest among the three scale controls.

- **Q12**: This has the same 0.025 M concentration as Q03 and Q11 but a volume inside the experimentally studied 0.040–0.080 L range. The central prediction is therefore concentration-matched, with slightly less scale uncertainty than Q11. The secondary channels remain close to their observed boundary baseline.

Shared rationale:

The shared quantitative model is the sealed K1 concentration relationship pH_normalized = 0.08362 - 0.03203 ln(C), fitted over 0.0625–0.875 M with a residual root-mean-square error of about 0.00216. Separate amount and volume coefficients were nearly equal and opposite, so equal-concentration scale controls receive equal central predictions; intervals widen when absolute scale lies outside the original 0.040–0.080 L and 0.005–0.035 mol design. Final-assay free-fraction and precipitation values had means of 0.00292 and 0.00243, respectively, showed no systematic concentration dependence, and were comparable to the declared 0.006 observation noise with clipping at zero. Their point predictions therefore remain near the boundary baseline except for cautious model-averaged increases in free dissociation at previously unobserved low concentrations. Prediction intervals combine assay noise, fitted-response uncertainty, possible amount/volume scale effects, and substantial topology uncertainty for extrapolation. No equilibrium-confidence value is used as an uncertainty measure.

## K2 — sealed seven-part retrospective

1. Supplied structural claims

An instance-specific structural prior was supplied, but no task-specific numerical property dossier was supplied: the material-information dossier was null. The prior proposed HA(aq) ⇌ H+(aq) + A−(aq), direct precipitation M+(aq) + A−(aq) ⇌ MA(s), no dissolved MA(aq), and a three-channel concentration response.

The acidification part was supported phenomenologically. Increasing concentration consistently lowered normalized pH: at 0.040 L, batch 1 at 0.125 M gave 0.150966, whereas batch 4 at 0.875 M gave 0.086209. Dilution reversed that response; batch 9 at 0.0625 M gave 0.169127. This supports a concentration-coupled proton-generating process, but it does not uniquely establish the stated weak-acid elementary step or identify Ka.

The claim that the three public channels would jointly exhibit the proposed concentration response was contradicted observationally. The free-fraction and precipitation channels stayed at their lower boundary without monotonic concentration dependence. For example, batch 3 at 0.625 M had free fraction 0.009989 and precipitation 0.003184, while batch 4 at the still higher 0.875 M had 0.000298 and 0.007914. Across all batches, the respective means were only 0.002916 and 0.002426, below the declared 0.006 assay noise scale and consistent with clipping near zero.

That contradiction was not acted on during the campaign by changing the experimental matrix: the planned loading–dilution grid was completed rather than replacing later batches with metal-ion or low-concentration interventions. It therefore contradicts an active, resolved three-channel response, not the mere existence of a latent direct-precipitation edge.

The direct M+ + A− precipitation topology was not positively supported, but it also had no decisive logical contradiction: a large effective Ksp, little available M+, or an insensitive proxy could leave the branch inactive. The claimed absence of dissolved MA was untested because no species-resolved measurement separated M+, A−, MA(aq), and MA(s). The proposed dissolved acid balance was likewise not directly verified.

2. Experiments and assumptions that formed the account

Batch 1 established the initial pattern: an acidic response at 0.125 M with essentially boundary-level secondary signals. Batches 2–4 changed the account by showing a strong monotonic pH decline at fixed 0.040 L without a corresponding monotonic free-fraction or precipitation response. That weakened the supplied expectation of a visibly active precipitation branch.

Batches 5–8 repeated the loading series at 0.060 L, and batches 9–12 extended it to 0.080 L. These two blocks established that amount and dilution largely entered through concentration. The fitted coefficients were approximately −0.03161 for ln(amount) and +0.03486 for ln(volume), close to the equal-and-opposite pattern expected for dependence on amount/volume. Batch 9 also supplied the lowest observed concentration anchor, 0.0625 M, with normalized pH 0.169127.

The choice of an all-water 3-by-4 amount–volume grid was driven by the characterization objective and the supplied aqueous scope, not by numerical dossier constants. The decision to interpret pH primarily through concentration came from accumulated observations. Retaining HA ⇌ H+ + A− as a plausible molecular interpretation relied partly on the supplied structural prior and partly on the observed acidification, but remained an untested topology assumption. Treating precipitation as optional rather than active came from the accumulated near-zero proxy results.

Batch 3 was selected as the sealed anchor because its 0.040 L, 0.025 mol condition sampled the concentrated region and produced nonzero readings on all three channels: normalized pH 0.098272, free fraction 0.009989, and precipitation 0.003184. That selection did not imply that its two small secondary values were representative or mechanistically resolved.

3. Strongest competing explanations

The strongest parameter-only explanation retains the supplied topology but makes the solid branch effectively inactive over the tested range. A sufficiently large effective Ksp, low M+ inventory, altered activity coefficients, or weak precipitation-proxy gain can reproduce the pH trend while leaving the other channels near zero. This is refitting parameters inside one topology, not confirmation of that topology.

The strongest competing network is a proton-release system without an observably active precipitate, possibly augmented by dissolved association:

HA ⇌ H+ + A−
M+ + A− ⇌ MA(aq),

with either no solid edge or a subsequent MA(aq) ⇌ MA(s) step that remains inactive. An even simpler effective alternative is concentration-proportional proton release controlled by background ions or buffering. The sealed empirical relationship, normalized pH = 0.08362 − 0.03203 ln(C), is close to pH = 1.171 − 1.032 log10(C), so an approximately fixed proton-releasing fraction is a parsimonious description over the observed range.

The evidence distinguishes a reproducible concentration–pH coupling from the absence of a resolved concentration trend in the other channels. It cannot distinguish direct precipitation from negligible precipitation, dissolved complexation, background buffering, nonideal weak-acid behavior, or an ambiguous observation map. It also cannot determine Ka, Ksp, the M+ inventory, solid mass, or whether dissolved MA exists.

4. One additional legal complete experiment

I would run one low-concentration water batch at 0.080 L with 0.002 mol reagent, giving 0.025 M. I would take one pH-meter measurement, terminate the batch, and obtain the required final assay. This keeps volume inside the characterized range while extending concentration below the observed 0.0625 M boundary. It directly tests the most consequential extrapolation used in the blind predictions without introducing a catalyst whose relation to M+ is unknown.

If normalized pH followed the sealed logarithmic relationship near 0.202 and both secondary channels remained at zero, I would strengthen the effective concentration-response account and further weaken the need for an active precipitation branch. If the free fraction rose clearly above its noise scale while pH showed curvature, I would infer entry into a dilute weak-acid regime and revise the account toward concentration-dependent dissociation. If precipitation became measurable on dilution, the simple monotonic saturation story would fail and an observation-map, nucleation, or association transition would need consideration. If all three channels changed sharply, I would treat 0.025–0.0625 M as a transition region rather than extrapolating one global equation. A single such experiment still would not identify direct versus dissolved association.

5. Characterization trade-offs

The objective was mechanism characterization rather than operational-score improvement. I therefore used all 12 complete batches for a structured loading–dilution matrix instead of searching for a high scalar score. The design gave broad local coverage and separated amount from volume better than repeated optimization at one condition would have done.

The cost of that choice was limited replication. No recipe was repeated exactly, so pure batch-to-batch repeatability cannot be estimated independently of the response surface. The pH meter and final assay supplied partial within-batch measurement comparison, but they are different measurements rather than true independent batch replicates. The grid also favored local identification of concentration dependence over identification of precipitation topology: no metal-source perturbation, catalyst contrast, low-concentration transition series, temperature contrast, or time series was included.

There was a temptation to regard higher equilibrium-confidence or scalar score as desirable, but neither was the research objective. Equilibrium confidence was correctly treated as an environment diagnostic, not scientific certainty, and batch selection was based on evidentiary coverage rather than claimed optimality.

6. Underused evidence and least reliable predictions

The paired pH-meter measurements were underused. They broadly supported the final-assay pH trend—for example, batch 1 gave 0.152871 before termination and 0.150966 finally—but a formal cross-instrument bias analysis was not performed. The small mismatch between the separate amount and volume coefficients was also underused; it could indicate weak scale dependence, although it could equally be sampling noise. Equilibrium residuals, raw spectral structure, mass-balance fields, and zero-clipping behavior were not developed into independent mechanistic tests. In particular, the close agreement between the mean precipitation signal and the expected positive bias from clipping zero-centered noise deserved more explicit treatment.

The least reliable blind predictions are Q01 and Q02. Their concentrations, 0.0004167 and 0.0041667 M, are respectively about 150-fold and 15-fold below the lowest K1 concentration. Their pH estimates came from unsupported logarithmic extrapolation, and their predicted free-fraction increases were model-averaged conjectures rather than K1-identified effects.

Q03, Q11, and Q12 at 0.025 M are also outside the concentration range. Giving them the same central response assumes concentration-only scale invariance beyond where it was established. Q11 is especially uncertain because its 0.012 L volume and 0.0003 mol loading are both below the K1 design.

Q06 at 1.25 M is the least reliable high-concentration prediction because it exceeds the observed 0.875 M maximum and could encounter nonideality or saturation. Q07 inherits concentration support at 0.5 M but uses only 0.006 L, far outside the observed volume range; equating it centrally with Q05 was a strong scale-invariance assumption. Q04 is concentration-matched to batch 1 but uses a smaller volume, so it is safer than the extreme extrapolations but not a direct recipe replication.

The widest conceptual inconsistency with K1 scope is that the blind prediction set necessarily assigned numerical centers to low-concentration free-fraction behavior even though K1 explicitly classified that regime as unsupported extrapolation. The wide intervals acknowledged this, but they did not convert conjecture into identified mechanism.

7. Limits of the anchor, repeatability, robustness, and generalization

The sealed anchor is one batch, not a replicated standard. Batch 3 represents 0.625 M at 0.040 L and cannot establish repeatability, a threshold, or a universal relation. Its free-fraction value of 0.009989 was among the largest observed and should not be generalized as typical. Its precipitation value of 0.003184 remained below the assay noise scale.

Local robustness is strongest for the direction of the pH response. The trend recurred across three volumes and four loadings, and the log-concentration fit had a residual root-mean-square error of about 0.00216. Robustness is much weaker for the exact fitted coefficients because there were no exact recipe replicates and all measurements came from one frozen synthetic world.

Repeatability is only partially addressed by agreement between in-process and final pH readings and by the smooth response across neighboring conditions. It was not established through independent repeated batches. The secondary channels were dominated by boundary censoring and observation noise, so their apparent repeatability at zero is not proof that the corresponding species or processes were absent.

Generalization is defensible only within the water, ambient-condition region bounded approximately by 0.005–0.035 mol reagent, 0.040–0.080 L volume, and 0.0625–0.875 M concentration. Generalization to smaller vessels, lower or higher concentrations, other solvents, catalysts, temperatures, equilibration times, or external metal loading is unsupported. Real solvent names do not make the categorical synthetic effects predictions about real chemistry. Nothing in K1 establishes transfer to another frozen world or to physical samples.

Finally, neither batch 3 nor any other condition was shown to be optimal, and optimality was not the objective. The anchor was chosen for mechanistic coverage and measurable channels, subject to substantial noise and topology ambiguity.

## EQS — sealed structured mechanism supplement

- Network family: `indeterminate`
- Aqueous intermediate: `indeterminate`
- Selected equations: `acid_dissociation, free_ion_solid_equilibrium`
- Cited source batches: `1, 3, 4, 9`
- Rationale: The concentration-dependent acidification supports an acid-dissociation process: normalized pH fell from 0.150966 in batch 1 at 0.125 M to 0.086209 in batch 4 at 0.875 M, while diluted batch 9 at 0.0625 M gave 0.169127. However, the free-fraction and precipitation channels remained near their noise-limited lower boundaries without a systematic concentration response; for example, batch 3 gave free fraction 0.009989 and precipitation signal 0.003184. The evidence therefore cannot distinguish direct free-ion precipitation from a network containing an aqueous MA ion-pair intermediate. The acid-dissociation and free-ion solid-equilibrium equations are retained as the common encompassing equations, but neither absence nor presence of an aqueous intermediate was identified.

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean width | Interval score |
|---|---:|---:|---:|---:|
| pH_normalized | 0.00491189 | 1 | 0.0408333 | 0.0408333 |
| acid_dissociation_fraction | 0.00386745 | 0.883333 | 0.0409167 | 0.0432571 |
| precipitation_signal | 0.00357205 | 0.916667 | 0.0171667 | 0.0323554 |

## Structural evaluation

Truth family: `aqueous_ion_pair_intermediate`; predicted family: `indeterminate`; abstained: `True`; family correct: `False`; exact equation set correct: `False`; equation-set Jaccard: `0.666667`.

## Response-shape evaluation

Concentration slope MAE `0.012423` and curvature MAE `0.0159496`. Dilution slope MAE `0.00743007` and curvature MAE `0.0148561`.

## Evidence boundary

K1 was sealed before Q, Q before K2, K2 before EQS, and reference truth was generated only after all 15 EQS responses were sealed. The task is characterization rather than optimization. Numerical residual and equilibrium confidence are environment diagnostics, not agent uncertainty or task scores. Private authentication and raw model process material are excluded.
