# EQ-W02--Opaque — final public report

World `EQ-W02`; prior arm `Opaque`; status `completed`. The effective result came from `attempt-02`.

## Source campaign

The campaign contains 12/12 completed batches and 60 recorded operations. Exact replay: `True`.

| Batch | pH normalized | Acid dissociation | Precipitation signal | Residual |
|---:|---:|---:|---:|---:|
| 1 | 0.265518 | 0.0780608 | 0.146919 | 0 |
| 2 | 0.269308 | 0.0691622 | 0.162225 | 0 |
| 3 | 0.269245 | 0.0704721 | 0.150558 | 0.00379401 |
| 4 | 0.269341 | 0.066716 | 0.148029 | 0.00316911 |
| 5 | 0.264727 | 0.071738 | 0.162372 | 0.00447836 |
| 6 | 0.264233 | 0.0692495 | 0.15337 | 0 |
| 7 | 0.266004 | 0.0857305 | 0.147809 | 0 |
| 8 | 0.263758 | 0.0682462 | 0.163022 | 0.00485442 |
| 9 | 0.266662 | 0.0647091 | 0.152798 | 0.000211424 |
| 10 | 0.26606 | 0.0701289 | 0.15588 | 0 |
| 11 | 0.268479 | 0.0688071 | 0.162417 | 0 |
| 12 | 0.26384 | 0.0616994 | 0.160524 | 0.000529324 |

## Sealed scientific account

### K1 report

# Mechanistic report: bounded aqueous acid dissociation and precipitation

## 1. Experimental scope

I completed 12 independent water-only batches at approximately 297.2 K. The design crossed four nominal analytical loadings, C_T = n_reagent/V_liquid = 0.10, 0.20, 0.30, and 0.40 mol/L, with three liquid volumes at every loading: 0.040, 0.060, and 0.080 L. Thus, concentration was varied while total reagent and vessel scale were independently changed. No catalyst, heating, deliberate waiting period, nonaqueous solvent, or pH-adjusting material was used.

Each batch was measured once with the pH meter before termination and once with the more precise final assay after termination. The pH-meter sample removed 0.000030 L, so final-assay concentrations were only about 0.04–0.08% above their nominal values. I treat that perturbation as negligible for the present resolution.

The final-assay observations were:

| Batch | Volume (L) | Reagent (mol) | Nominal C_T (mol/L) | pH | Dissociation fraction alpha | Precipitation proxy P | Equilibrium residual | Environment diagnostic |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.040 | 0.004 | 0.10 | 3.7173 | 0.07806 | 0.14692 | 0.000000 | 0.47220 |
| 2 | 0.080 | 0.008 | 0.10 | 3.7703 | 0.06916 | 0.16223 | 0.000000 | 0.45369 |
| 9 | 0.060 | 0.006 | 0.10 | 3.7333 | 0.06471 | 0.15280 | 0.000211 | 0.45886 |
| 3 | 0.040 | 0.008 | 0.20 | 3.7694 | 0.07047 | 0.15056 | 0.003794 | 0.53558 |
| 4 | 0.080 | 0.016 | 0.20 | 3.7708 | 0.06672 | 0.14803 | 0.003169 | 0.53195 |
| 10 | 0.060 | 0.012 | 0.20 | 3.7248 | 0.07013 | 0.15588 | 0.000000 | 0.52827 |
| 5 | 0.040 | 0.012 | 0.30 | 3.7062 | 0.07174 | 0.16237 | 0.004478 | 0.52450 |
| 6 | 0.080 | 0.024 | 0.30 | 3.6993 | 0.06925 | 0.15337 | 0.000000 | 0.53344 |
| 11 | 0.060 | 0.018 | 0.30 | 3.7587 | 0.06881 | 0.16242 | 0.000000 | 0.53248 |
| 7 | 0.040 | 0.016 | 0.40 | 3.7241 | 0.08573 | 0.14781 | 0.000000 | 0.45014 |
| 8 | 0.080 | 0.032 | 0.40 | 3.6926 | 0.06825 | 0.16302 | 0.004854 | 0.44430 |
| 12 | 0.060 | 0.024 | 0.40 | 3.6938 | 0.06170 | 0.16052 | 0.000529 | 0.45349 |

The stated one-standard-deviation final-assay noise levels were 0.002 in normalized pH, equivalent to 0.028 pH unit, 0.006 in alpha, 0.006 in P, and 0.004 in the equilibrium residual.

## 2. Main empirical relationships

### 2.1 Loading and volume have only weak resolved effects on pH

Mean final pH values at 0.10, 0.20, 0.30, and 0.40 mol/L were respectively 3.740, 3.755, 3.721, and 3.703. All twelve results occupied the narrow interval 3.693–3.771. There is a possible shallow maximum near 0.20 mol/L followed by mild acidification at higher loading, but the total change is small and the sequence is not strictly monotonic.

At fixed concentration, changing volume from 0.040 to 0.080 L did not produce a consistent direction of change. For example, at 0.20 mol/L batches 3 and 4 gave nearly identical pH values of 3.769 and 3.771 despite a twofold change in both volume and total reagent. At 0.30 mol/L, batches 5 and 6 similarly gave 3.706 and 3.699. Other matched pairs fluctuated in both directions. The supported conclusion is therefore that intensive loading is at most a weak pH control over this range, while an independent extensive-volume effect is unresolved.

### 2.2 Dissociation is approximately constant, but is strongly coherent with pH

Mean final dissociation fractions at increasing concentration were 0.07064, 0.06911, 0.06993, and 0.07189. Thus alpha remained near 0.07 rather than decreasing strongly with analytical concentration. The individual range, 0.06170–0.08573, is only a few assay standard deviations wide and has no reproducible monotonic dependence on either concentration or volume.

A much clearer relationship appears when pH and alpha are considered together. For an effective one-step equilibrium

HA_eff <=> H+ + A-_eff,

an empirical Henderson–Hasselbalch representation is

alpha = 1/[1 + 10^(pKa_eff - pH)],

or equivalently

pKa_eff = pH + log10[(1-alpha)/alpha].

Applying this transformation to each final assay gives pKa_eff values from 4.752 to 4.917, with mean 4.852 and root-mean-square scatter 0.048 pKa unit. The concentration-level estimates were 4.859, 4.884, 4.845, and 4.814. This is substantially more stable than a model in which alpha is predicted directly from total concentration alone.

My preferred effective description is therefore:

1. the environment establishes a relatively narrow acidic pH window near 3.7–3.8;
2. an acid-like population partitions according to an effective pKa near 4.85;
3. because pH itself moves little, the measured dissociation fraction also stays near 7%.

This relationship is an empirical coupling between two public observables. It does not by itself identify a real chemical species or prove an elementary monoprotic mechanism.

### 2.3 A simple unbuffered weak-acid model is inconsistent with the observations

If the added reagent were the only acid and alpha were its literal degree of ionization, an ideal dilute monoprotic model would give

Ka = alpha^2 C_T/(1-alpha)

and approximately [H+] = alpha C_T. Using the concentration-group means, the apparent Ka from the first expression rises from 5.37e-4 at 0.10 mol/L to 2.23e-3 at 0.40 mol/L, a factor of about four rather than a constant. Moreover, alpha C_T would be roughly 0.007–0.029 mol/L, whereas pH 3.7 corresponds to hydrogen-ion activity of only about 2e-4 in molar units. The discrepancy is far larger than instrumental noise.

Consequently, I reject the simplest interpretation “one isolated weak acid in pure water, with charge balance supplied only by its own dissociation.” At least one of the following must instead be true:

- the bounded world contains an unobserved buffering or counterion background;
- alpha is an effective population proxy rather than a stoichiometric ionized fraction;
- activity coefficients or coupled association strongly depart from the ideal dilute model;
- multiple latent acid/base states collapse into the reported two-state fraction.

The first two explanations are the most economical, but the experiment cannot distinguish them.

### 2.4 No precipitation threshold was resolved

The final precipitation proxy stayed between 0.14692 and 0.16302. Concentration-group means were 0.15398, 0.15149, 0.15939, and 0.15712. The endpoint change from 0.10 to 0.40 mol/L was only about 0.0031, smaller than a single final-assay standard deviation. Neither concentration nor total reagent amount produced a monotonic response.

Matched-scale contrasts also changed sign. At 0.10 mol/L, increasing volume from 0.040 to 0.080 L raised P from 0.1469 to 0.1622, whereas at 0.30 mol/L it lowered P from 0.1624 to 0.1534. These mixed directions argue against a resolved independent vessel-volume effect.

A generic bounded precipitation mechanism could be written as

S = IAP/Ksp_eff,
P = P0 + A f(S),

where f is a clipped or sigmoidal supersaturation response. The data identify only a baseline-like P near 0.15. They do not identify Ksp_eff, the composition of the ion-activity product, a nucleation threshold, or the amplitude A. Plausible explanations include operation below a precipitation transition, a nearly saturated background whose response is dominated by latent composition, or cancellation between increased analytical loading and shifts in ionization/activity. A broad or noisy proxy floor is also observationally equivalent here.

## 3. Measurements that shaped the interpretation

The most important comparisons were the constant-concentration scale pairs:

- Batches 1 and 2 at 0.10 mol/L;
- batches 3 and 4 at 0.20 mol/L;
- batches 5 and 6 at 0.30 mol/L;
- batches 7 and 8 at 0.40 mol/L.

These comparisons showed that doubling both liquid volume and reagent amount did not create a reproducible extensive-scale response. The intermediate-volume batches 9–12 then filled each concentration level and confirmed that neither pH, alpha, nor P followed a simple volume ordering.

Batch 10 was selected as the final replay recommendation because it is the middle-volume member of the replicated 0.20 mol/L series, not because it maximized a scalar score. Its pH of 3.7248, alpha of 0.07013, and P of 0.15588 are representative of the observed regime.

The paired pH-meter and final-assay measurements also affected my interpretation. Across the 12 batches, their root-mean-square differences were approximately 0.00407 in normalized pH, 0.01697 in alpha, and 0.01653 in P. These are compatible with the instruments' combined stated noise scales. Mean pH-channel disagreement was essentially zero; the pH meter read alpha about 0.0098 higher on average and P about 0.0035 lower, but these offsets are not securely separable from measurement variability with only one pair per batch. I therefore used the final assay for numerical characterization and did not interpret pre/post termination differences as chemical evolution.

## 4. Equilibrium diagnostics

Final equilibrium residuals ranged from zero to 0.004854. Six batches reported exactly zero; the remaining positive values were small relative to the full 0–1 observable scale and near the stated 0.004 residual-noise level. Nothing in these measurements indicates a gross failure to reach the bounded world's equilibrium-like state.

The channel named equilibrium_confidence was approximately 0.45–0.47 at 0.10 and 0.40 mol/L and approximately 0.53 at 0.20 and 0.30 mol/L. I report this only as an environment diagnostic. It is not my scientific confidence, not a probability that the mechanism is correct, and not evidence by itself for a chemical species or law.

## 5. Preferred effective mechanism

Within the tested slice, my compact working model is:

```
C_T = n_reagent / V_liquid
pH = approximately 3.7–3.8, with only weak unresolved dependence on C_T
alpha = 1 / (1 + 10^(4.85 - pH)) + measurement/process deviation
P = approximately 0.155 + weak unresolved function(C_T, V, alpha, latent activities)
```

Mechanistically, I interpret this as a pH-regulated or background-coupled acid equilibrium. Total loading changes the amount of acid-like material but does not proportionally create free hydrogen ion. The reported dissociation fraction follows the regulated pH through an effective pKa-like coupling. The precipitation observable either remains in a shallow part of its response curve or depends on latent activities that are not changed enough by the tested loading/dilution range.

This model explains three otherwise awkward facts simultaneously: the nearly invariant pH, the nearly invariant alpha, and the stable pKa_eff derived from their ratio. It also explains why a conventional concentration-only weak-acid square-root law fails.

## 6. Identifiability limits and competing explanations

The following are not identifiable from this campaign:

- The identity, stoichiometry, and number of acid/base species.
- Whether the pH plateau comes from a buffer, a fixed counterion inventory, nonideal activities, or the benchmark's observable mapping.
- Whether alpha is a literal molecular fraction or an effective assay channel.
- The precipitating species, Ksp, nucleation kinetics, particle inventory, or mapping from precipitated amount to P.
- Temperature dependence, time to equilibrium, hysteresis, mixing effects, catalyst effects, or solvent dependence.
- Behavior below 0.10 or above 0.40 mol/L, outside 0.040–0.080 L, or away from approximately 297 K.

Reasonable competing explanations include:

1. **Buffered single-site acid:** a background buffer fixes pH and a single acid site with pKa near 4.85 sets alpha.
2. **Multi-state effective acid:** several microscopic states produce a two-channel aggregate that happens to follow a Henderson–Hasselbalch-like curve locally.
3. **Activity-controlled equilibrium:** alpha is thermodynamic, but concentration-dependent activity coefficients and counterions invalidate the ideal charge-balance calculation.
4. **Correlated observation mapping:** pH and alpha may be generated from a shared latent equilibrium coordinate, so the stable pKa_eff is an effective sensor-level invariant rather than a molecular constant.
5. **Latent precipitation floor:** P may primarily reflect a fixed background precipitate or baseline, with reagent-dependent precipitation too small to resolve.

The present data favor a pH-coupled description over a concentration-only dissociation law, but they do not discriminate among explanations 1–4. Likewise, they do not establish whether the small variations in P are chemical or instrumental.

## 7. Supported range, extrapolation, and speculation

**Directly supported:** water-only batches at approximately 297.2 K; nominal C_T of 0.10–0.40 mol/L; volumes of 0.040–0.080 L; immediate measurements under the executed protocol. In this range, pH is about 3.69–3.77, alpha about 0.062–0.086, P about 0.147–0.163, and pKa_eff about 4.85 with 0.048 RMS scatter.

**Limited interpolation:** the Henderson–Hasselbalch-like alpha–pH relationship is a reasonable local interpolator inside the observed pH window. A constant or weakly varying P near 0.155 is a safer interpolator than a threshold law.

**Unsupported extrapolation:** predictions at substantially different concentration, dilution, temperature, solvent, residence time, or added catalyst/base/acid are not justified. In particular, no claim is made that pKa_eff remains constant outside this narrow slice or that precipitation remains flat beyond 0.40 mol/L.

**Speculation:** a hidden buffer/background electrolyte and a shallow supersaturation response are plausible mechanistic stories, but neither was directly measured. They should be treated as hypotheses rather than observations.

Overall, the strongest finding is not a loading-driven precipitation law but an effective acid-equilibrium invariant: pH and dissociation are mutually consistent with pKa_eff approximately 4.85 while being inconsistent with the charge balance of an isolated ideal weak acid. The precipitation channel remains essentially unresolved beyond a bounded baseline in the studied domain.

### Blind Q predictions

| Query | Metric | Estimate | 80% lower | 80% upper |
|---|---|---:|---:|---:|
| Q01 | acid_dissociation_fraction | 0.071 | 0.04 | 0.13 |
| Q01 | pH_normalized | 0.267 | 0.257 | 0.283 |
| Q01 | precipitation_signal | 0.132 | 0.08 | 0.17 |
| Q02 | acid_dissociation_fraction | 0.071 | 0.04 | 0.13 |
| Q02 | pH_normalized | 0.267 | 0.257 | 0.283 |
| Q02 | precipitation_signal | 0.132 | 0.08 | 0.17 |
| Q03 | acid_dissociation_fraction | 0.277 | 0.18 | 0.4 |
| Q03 | pH_normalized | 0.317 | 0.298 | 0.338 |
| Q03 | precipitation_signal | 0.004 | 0 | 0.05 |
| Q04 | acid_dissociation_fraction | 0.088 | 0.055 | 0.15 |
| Q04 | pH_normalized | 0.274 | 0.263 | 0.289 |
| Q04 | precipitation_signal | 0.006 | 0 | 0.1 |
| Q05 | acid_dissociation_fraction | 0.071 | 0.05 | 0.095 |
| Q05 | pH_normalized | 0.266 | 0.26 | 0.274 |
| Q05 | precipitation_signal | 0.155 | 0.13 | 0.175 |
| Q06 | acid_dissociation_fraction | 0.071 | 0.05 | 0.095 |
| Q06 | pH_normalized | 0.266 | 0.26 | 0.274 |
| Q06 | precipitation_signal | 0.155 | 0.13 | 0.175 |
| Q07 | acid_dissociation_fraction | 0.071 | 0.05 | 0.095 |
| Q07 | pH_normalized | 0.266 | 0.26 | 0.274 |
| Q07 | precipitation_signal | 0.155 | 0.13 | 0.175 |
| Q08 | acid_dissociation_fraction | 0.629 | 0.45 | 0.8 |
| Q08 | pH_normalized | 0.363 | 0.335 | 0.39 |
| Q08 | precipitation_signal | 0.002 | 0 | 0.04 |
| Q09 | acid_dissociation_fraction | 0.252 | 0.16 | 0.37 |
| Q09 | pH_normalized | 0.313 | 0.294 | 0.334 |
| Q09 | precipitation_signal | 0.004 | 0 | 0.05 |
| Q10 | acid_dissociation_fraction | 0.071 | 0.005 | 0.16 |
| Q10 | pH_normalized | 0.265 | 0.18 | 0.29 |
| Q10 | precipitation_signal | 0.16 | 0.1 | 0.65 |
| Q11 | acid_dissociation_fraction | 0.069 | 0.04 | 0.1 |
| Q11 | pH_normalized | 0.264 | 0.255 | 0.274 |
| Q11 | precipitation_signal | 0.159 | 0.135 | 0.19 |
| Q12 | acid_dissociation_fraction | 0.07 | 0.052 | 0.091 |
| Q12 | pH_normalized | 0.267 | 0.261 | 0.274 |
| Q12 | precipitation_signal | 0.157 | 0.135 | 0.175 |

The predictions use total analytical concentration as the main state variable and treat dosing order as irrelevant at final equilibrium. For extrapolation, I used a competition model suggested by the campaign's nearly invariant pH and dissociation despite changing analytical loading: an effective dissolved concentration saturates near 0.0026 mol/L, while the dissolved fraction follows a weak-acid relation with Ka approximately 1.4e-5. Above that effective plateau, pH_normalized and dissociation remain near 0.266 and 0.071, and the bounded precipitation proxy approaches about 0.16. Below it, the weak-acid quadratic predicts increasing dissociation and pH with dilution and little precipitation. This dissolved-loading interpretation was not uniquely identified by the completed campaign, so intervals are widened for trace concentrations and especially for the extreme 6.67 mol/L batch. Instrument noise, between-batch variation, uncertainty in the plateau location, and model-form uncertainty are all included qualitatively in the 80% ranges.

### K2 retrospective

## 1. Status of claims in the initial information

The initial packet supplied almost no substantive mechanistic claim to test. It identified the task as a bounded aqueous weak-acid/precipitation slice, defined the observable channels, and stated that `pH_normalized = pH/14`. It explicitly showed `prior_record: null`; therefore, there was no numerical archival relationship, pKa, solubility law, or precipitation threshold against which the results could be directly compared. The anonymous material catalogue also did not justify importing properties of any real acid or precipitate.

Several broad framing claims were consistent with the results but were not stringent tests:

- The description as an equilibrium-like acid-dissociation problem was compatible with the small final equilibrium residuals: six batches reported zero and the maximum was 0.004854 in batch 8. This is an absence of evidence for gross nonequilibrium, not proof of thermodynamic equilibrium or path independence.
- The pH and dissociation channels behaved coherently enough to admit the K1 effective Henderson–Hasselbalch representation. K1 reported an effective pKa mean of 4.852 with RMS scatter 0.048.
- The description as a precipitation slice was compatible with a persistent precipitation proxy near 0.15, but no threshold or precipitation law was supplied initially, and none was identified experimentally.

The campaign produced direct counterevidence against a simple interpretation that was not actually asserted by the initial packet: an isolated ideal monoprotic acid whose own dissociation supplies charge balance. K1 explicitly noted that alpha*C_T would be about 0.007–0.029 mol/L, while the observed pH implied hydrogen activity around 2e-4 in molar units. It also showed that alpha²C_T/(1-alpha) changed by roughly a factor of four across the concentration groups. K1 therefore rejected that simple model rather than silently retaining it.

A distinction is important here. The lack of a systematic volume effect is only “no resolved counterevidence” to an intensive-state description; it is not proof that volume never matters. Some matched pairs differed by more than the nominal noise of one reading—for example, precipitation was 0.14692 in batch 1 and 0.16223 in batch 2—but the direction reversed elsewhere, such as batches 5 and 6. I treated those differences as inconsistent fluctuations rather than evidence for a reproducible scale law. No clear initial claim was contradicted and then knowingly left unrevised.

## 2. Experiments that formed the interpretation, and assumptions behind the design

The fixed-concentration scale comparisons were the experiments that most directly shaped K1:

- Batches 1 and 2 held nominal concentration at 0.10 mol/L while doubling volume and reagent.
- Batches 3 and 4 did the same at 0.20 mol/L.
- Batches 5 and 6 did the same at 0.30 mol/L.
- Batches 7 and 8 did the same at 0.40 mol/L.

Batches 9–12 supplied the intermediate 0.060 L member of each concentration series. Together, these comparisons undermined a simple extensive-amount explanation: there was no consistent ordering by 0.040, 0.060, and 0.080 L at fixed concentration. Batches 3 and 4 were particularly influential because their pH values were nearly identical, 3.7694 and 3.7708, despite a twofold change in scale. Batches 5 and 6 provided a similar comparison at 0.30 mol/L.

The aggregate behavior across all four concentration levels formed the acid-equilibrium judgment. Mean dissociation stayed near 0.07 while mean pH stayed near 3.7–3.8. Transforming each final result through pKa_eff = pH + log10[(1-alpha)/alpha] produced the compact K1 relationship near pKa_eff = 4.85. This relationship was discovered from the completed observations; it was not supplied in the initial materials.

The precipitation conclusion was shaped mainly by the absence of an ordered response across all 12 batches. Concentration-group means varied only from approximately 0.1515 to 0.1594, and neither the concentration series nor the scale pairs revealed a threshold. This supported K1’s deliberately weak conclusion that only a baseline-like proxy near 0.15 was identified.

The paired pH-meter and final-assay results were useful as a cross-instrument consistency check. Their discrepancies were broadly compatible with their stated combined noise. They did not provide clean time-course information because there was no controlled waiting interval, and termination versus instrument identity was confounded.

Several design choices rested on assumptions rather than evidence:

- The 0.10–0.40 mol/L range was an unvalidated guess about where informative behavior would occur. It proved useful for scale comparisons but failed to bracket a clear dissociation or precipitation transition.
- Restricting all batches to water followed the aqueous research goal, but it left solvent dependence completely untested.
- Using four concentrations at three scales emphasized concentration/volume decoupling. It consumed all 12 complete experiments and left no exact process replicates or very-low-loading points.
- The assumption that immediate measurements represented the relevant equilibrium-like state relied on the environment framing and small residuals; equilibration time was not tested.
- The later solubility-limited interpretation used in the blind-prediction rationale was not an experiment-time conclusion and was not established in K1. It was a post-report forecasting hypothesis introduced to extrapolate into the trace-loading questions.

## 3. Principal competing mechanisms and what the campaign distinguishes

The leading explanations remain:

1. **Buffered single-site acid.** A latent background fixes pH near 3.7–3.8, while an acid-like site with effective pKa near 4.85 determines alpha.
2. **Multiple microscopic states.** Several acid/base, association, or ion-pair states collapse into public observables that locally resemble a one-site Henderson–Hasselbalch curve.
3. **Strong activity or counterion effects.** Alpha may be thermodynamic, but analytical concentration is not the relevant activity and ideal charge balance fails.
4. **Correlated observable mapping.** The pH and alpha channels may be derived from a common latent equilibrium coordinate. In that case, the stable pKa_eff is a sensor-level invariant rather than a molecular constant.
5. **Precipitation-limited dissolved loading.** Most added material may enter an unobserved precipitated or otherwise inactive pool, leaving an approximately fixed dissolved concentration. This could reconcile the nearly constant pH and alpha with increasing analytical loading.
6. **A bounded precipitation baseline or floor.** The approximately 0.15 precipitation signal could reflect a fixed background, an offset in the public proxy, or a shallow region of a response curve rather than increasing precipitated mass.

The data distinguish the ideal isolated-acid model from this broader family: the charge-balance and constant-Ka failures are too large to explain by final-assay noise alone. The data also make a large, monotonic extensive-volume effect unlikely within the tested range.

The data do not distinguish mechanisms 1–4. They also do not distinguish mechanism 5 from a buffered plateau because every tested analytical concentration was at least 0.10 mol/L. If a dissolved-loading ceiling lies far below that, all 12 batches sampled only the same saturated regime. Nor can the campaign decide whether the precipitation proxy measures precipitated fraction, solid amount, nucleation propensity, or a transformed latent state.

The blind predictions committed more strongly to mechanism 5 than K1 warranted. In particular, their common rationale posited an effective dissolved concentration near 0.0026 mol/L and Ka near 1.4e-5. The Ka-like value was motivated by K1’s pH–alpha relationship, but the 0.0026 mol/L ceiling was inferred indirectly from the charge-balance discrepancy. It was not independently measured. That forecast model must therefore be treated as one competitive extrapolation, not as a finding retroactively present during the campaign.

## 4. One additional complete experiment

If exactly one complete experiment were allowed, I would choose a water batch with 0.060 L solvent and 0.000006 mol reagent, giving C_T = 0.00010 mol/L. I would make one pH-meter measurement, terminate, and then perform the required final assay. I would not actually run it here.

This condition is deliberately far below the campaign range and below the hypothesized 0.0026 mol/L dissolved-loading ceiling. It maximizes discrimination among the leading explanations:

- **If pH_normalized remained near 0.266, alpha near 0.07, and precipitation near 0.15**, the background-buffer or correlated-observable explanation would gain substantial support. A concentration-independent precipitation floor would also become more plausible. The trace weak-acid extrapolation used for Q03, Q08, and Q09 would be weakened.
- **If pH rose toward approximately 4.4–4.6, alpha rose to roughly 0.3, and precipitation approached zero**, an unsaturated weak-acid regime below a loading ceiling would gain support. This would support the qualitative basis of the trace blind predictions, although it would still not prove that high-loading invariance is caused by precipitation rather than another saturation mechanism.
- **If pH and alpha changed as expected for dilution but precipitation stayed near 0.15**, acid speciation and the precipitation proxy would appear partly decoupled; a precipitation baseline or sensor offset would be favored.
- **If precipitation fell but pH and alpha stayed on their old plateau**, removal of a precipitating population would be indicated without evidence that it controlled acid speciation.
- **If the pH-meter and final assay disagreed beyond their combined noise**, instrument-specific mapping or a termination/time effect would need renewed attention.

One exact replicate of a campaign condition would better estimate repeatability, but it would provide less discrimination among the present mechanisms. The trace-loading experiment is therefore the better single mechanistic test.

## 5. Tradeoff between identifiability and operational score

The design primarily pursued identifiability rather than scalar-score maximization. The research brief explicitly said that the native score was diagnostic rather than the research objective, so I used repeated concentration levels across different volumes to separate intensive loading from extensive amount. That choice sacrificed broader exploration and exact replication in exchange for a structured factorial comparison.

The score happened to be highest around 0.20–0.30 mol/L because the environment diagnostic was higher there. Nevertheless, I retained 0.10 and 0.40 mol/L batches and all three volumes rather than concentrating the campaign in the apparently favorable region. This is a concrete case of sacrificing possible score improvement for mechanistic coverage.

There was no clear instance in which I knowingly sacrificed identifiability to optimize score. Indeed, the sealed recommendation was batch 10, with score about 0.30174, even though batch 11 had the largest observed score, about 0.30459. Batch 10 was selected because it was the middle-volume member of the 0.20 mol/L series and thus a representative replay anchor.

However, the design did make a different unfavorable tradeoff: it overinvested in scale comparisons inside one apparently flat regime. After early batches suggested weak effects, the campaign still completed the preselected matrix rather than allocating later batches to trace or boundary concentrations. Preserving a coherent, non-outcome-adaptive design has scientific value, but it meant that the most important transition was never bracketed. This was not score optimization; it was a rigidity cost of the chosen identifiability strategy.

## 6. Underused evidence and weaknesses in the blind predictions

Several evidence sources were underused or intrinsically difficult to use:

- The public final-assay artifacts contained raw multichannel spectra and peak summaries, but the analysis relied almost entirely on processed equilibrium channels. Without a public mechanism-to-species mapping, the peaks could not safely be assigned to dissolved acid, conjugate base, or solid. Still, systematic peak-area scaling might have helped test whether dissolved material plateaued.
- The pH-meter/final-assay pairs were reduced to aggregate differences. They could not cleanly identify termination or time effects because instrument and sequence were confounded.
- The equilibrium residual was useful only as a diagnostic. Its frequent clipping at zero limited quantitative comparison.
- The environment diagnostic displayed a reproducible-looking maximum near 0.20–0.30 mol/L, but the contract explicitly prohibited treating it as scientific confidence. Its mechanistic meaning remained unspecified.
- There were no exact replicate recipes, so observed scatter mixed instrument noise, process variability, and possible scale effects.

The least reliable blind prediction is Q10 at 6.67 mol/L. It lies more than an order of magnitude beyond the tested concentration ceiling. Its point estimate assumed continuation of a dissolved-state plateau, while new activity, precipitation, or clipping regimes were entirely plausible. Even its stated intervals—pH_normalized 0.18–0.29, alpha 0.005–0.16, and precipitation 0.10–0.65—may be too narrow because the observables are bounded on 0–1 and K1 provided no validated high-concentration law.

Q08, Q03, and Q09 are also highly uncertain. Their intervals committed to the unsaturated weak-acid extrapolation:

- Q08 predicted pH_normalized 0.335–0.390, alpha 0.45–0.80, and precipitation 0–0.04.
- Q03 predicted pH_normalized 0.298–0.338, alpha 0.18–0.40, and precipitation 0–0.05.
- Q09 predicted pH_normalized 0.294–0.334, alpha 0.16–0.37, and precipitation 0–0.05.

Those precipitation intervals exclude the approximately 0.15 baseline observed in every campaign batch. They are too narrow if the K1 competing explanation of a latent precipitation floor is taken seriously. Their pH intervals also exclude the campaign plateau, even though K1 explicitly said that a buffer, multiple states, activity effects, and correlated observation mapping could not be distinguished. This is a genuine inconsistency between K1’s uncertainty statement and the later predictive calibration: the forecast selected one extrapolative mechanism but did not widen the intervals enough to cover the equally plausible plateau mechanism.

Q04 is somewhat better calibrated because its pH and alpha intervals nearly include the plateau, but its precipitation interval of 0–0.10 may still be too narrow. Q01 and Q02 are less extreme but remain outside the supported concentration range; their shared prediction appropriately encoded concentration invariance, yet the precipitation lower bound of 0.08 may exclude a sharp unsaturated transition. Q11 is only moderately beyond the tested range, while Q12 is the most defensible interpolation. Q05–Q07 are compositionally near the observed domain, but their identical predictions depend on untested path independence; no staged-dosing experiment was performed in the campaign.

Thus, the blind predictions correctly labeled the solubility-ceiling model as uncertain in their global rationale, but several numerical 80% intervals did not fully propagate the model-form uncertainty already acknowledged in K1.

## 7. Limitations of the sealed recommendation

Batch 10 was a representative evidentiary anchor, not a demonstrated optimum. It used 0.060 L water and 0.012 mol reagent, giving 0.20 mol/L. Its final values—pH_normalized 0.26606, alpha 0.07013, precipitation 0.15588, and zero reported residual—made it useful as the central-volume member of a fixed-concentration comparison.

Its limitations are substantial:

- It was observed only once, so repeatability was not measured.
- Its apparent zero residual may partly reflect clipping or measurement noise.
- It was not the sample with the highest scalar score; batch 11 was higher.
- The 0.20 mol/L region was not shown to be uniquely stable or mechanistically privileged.
- All evidence came from water, one anonymous reagent, one temperature, immediate processing, and one bounded world.

Repeatability should first be tested with exact independent repetitions of batch 10, reporting the full distribution of all five public equilibrium channels rather than replacing an unfavorable repeat. Local robustness should then be tested with a small neighborhood in concentration and volume—for example, concentrations around 0.15, 0.20, and 0.25 mol/L at 0.040, 0.060, and 0.080 L—while preserving total-composition and scale contrasts. Deliberate waiting or staged-dosing variants would test path independence separately.

Cross-material scope would require repeating the design with other publicly selectable solvents or material categories, without assuming that anonymous benchmark effects correspond to real-solvent chemistry. Cross-world generalization would require independently instantiated worlds and a preregistered analysis of whether the same pKa-like invariant, plateau, and lack of scale dependence recur.

Finally, “sample-highest” and “optimal” must remain separate. Batch 11 was sample-highest on the diagnostic score, but that does not prove it maximizes expected score even within this world. Batch 10 was not sample-highest and was never claimed to be. It was selected for representativeness and replay value. Neither batch has been proven optimal for score, mechanistic informativeness, robustness, or transfer.

### EQ-specific supplement

Effective pKa identifiable: `True`; estimate `4.85`; 80% interval `[4.82, 4.89]`.

Within the studied domain, the final-assay pH and dissociation fraction support the effective relation pKa_eff = pH + log10[(1-alpha)/alpha]. The 12 batchwise values had mean 4.852, RMS scatter 0.048, and range 4.752–4.917. The interval includes sampling and assay variability but applies only to this observable-level local relationship; it does not identify an intrinsic molecular pKa because buffering, activity effects, multiple states, and correlated observable mapping remain confounded.

Path-dependence assessment: `indeterminate`.

The evidence is consistent with final-state dominance but does not directly test staged-addition path. Fixed-concentration scale pairs gave broadly similar final responses despite twofold changes in amount and volume: batches 3 and 4 at 0.20 mol/L had pH 3.7694 and 3.7708, while batches 5 and 6 at 0.30 mol/L had pH 3.7062 and 3.6993. However, every source batch used the same solvent-then-reagent order, and no two batches reached identical final amount and volume through different staged paths. Therefore there is no observed reproducible path effect, but path independence remains conjectural rather than demonstrated.

Dissociation-precipitation assessment: `indeterminate`.

Supported range: Water-only batches at approximately 297.2 K, nominal analytical loading 0.10–0.40 mol/L, and final liquid volume 0.040–0.080 L. Across this range, acid dissociation was 0.0617–0.0857 and precipitation signal was 0.1469–0.1630, with no resolved monotonic coupling or abrupt transition.

Competing explanation: All tested loadings may lie above an unobserved precipitation or dissolved-loading threshold, so a threshold-like mechanism followed by saturation would appear as the observed flat response. A concentration-independent proxy baseline is also observationally equivalent within this dataset.
## Blind-prediction evaluation

| Metric | MAE | Empirical 80% coverage | Mean width | Interval score |
|---|---:|---:|---:|---:|
| acid_dissociation_fraction | 0.0135743 | 1 | 0.120333 | 0.120333 |
| pH_normalized | 0.00307885 | 1 | 0.0330833 | 0.0330833 |
| precipitation_signal | 0.0178468 | 0.916667 | 0.1 | 0.133604 |

## Scope and privacy

Reference truth was released only after every EQS response was sealed. The environment-derived equilibrium-confidence field is neither an agent uncertainty estimate nor a score. Authentication material, raw model events, session identifiers, and usage accounting are excluded.
