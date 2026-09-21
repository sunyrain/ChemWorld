# EQ-S-W03--Opaque — final English experiment report

World `EQ-S-W03`; information arm `Opaque`; task `mechanism characterization`; effective status `completed`; result origin `original`.

## Source campaign

The autonomous campaign completed 12/12 batches and 60 recorded operations. Exact replay is `True`; rollbacks: 0.

| Batch | Solvent L | Reagent mol | Measurements | pH normalized | Free dissociation | Precipitation signal | Residual |
|---:|---:|---:|---|---:|---:|---:|---:|
| 1 | 0.03 | 0.008 | ph_meter, final_assay | 0.140163 | 0.0107838 | 0.0417896 | 0.00270388 |
| 2 | 0.05 | 0.008 | ph_meter, final_assay | 0.166863 | 0 | 0.0285179 | 0 |
| 3 | 0.07 | 0.008 | ph_meter, final_assay | 0.18658 | 0 | 0.0254843 | 0.00375843 |
| 4 | 0.08 | 0.008 | ph_meter, final_assay | 0.193518 | 0 | 0.0187393 | 0.00210843 |
| 5 | 0.03 | 0.02 | ph_meter, final_assay | 0.0917918 | 0 | 0.0660676 | 0 |
| 6 | 0.05 | 0.02 | ph_meter, final_assay | 0.121331 | 0.00426938 | 0.0533221 | 0 |
| 7 | 0.07 | 0.02 | ph_meter, final_assay | 0.132096 | 0 | 0.0515989 | 0.000285804 |
| 8 | 0.08 | 0.02 | ph_meter, final_assay | 0.143885 | 0.00347903 | 0.0350597 | 0 |
| 9 | 0.03 | 0.032 | ph_meter, final_assay | 0.0731843 | 0 | 0.0867164 | 0 |
| 10 | 0.05 | 0.032 | ph_meter, final_assay | 0.0941179 | 0 | 0.0912818 | 0.00279016 |
| 11 | 0.07 | 0.032 | ph_meter, final_assay | 0.114919 | 0 | 0.0626802 | 0.00734452 |
| 12 | 0.08 | 0.032 | ph_meter, final_assay | 0.119317 | 0 | 0.0474177 | 0 |

### Sealed evidentiary anchor

Batch `9`: Batch 9 is the high-loading, low-volume corner of the fixed aqueous factorial grid; its low normalized pH and strongest final precipitation signal make it a useful anchor for the coupled loading/dilution interpretation, without implying an optimum.

## K1 — sealed mechanistic report

MECHANISTIC REPORT

1. Scope and experimental basis

I completed 12 independent, terminated aqueous batches. Every batch used water, no catalyst, no heating, and one final assay. The design crossed three reagent loadings (0.008, 0.020, and 0.032 mol) with four initial water volumes (0.030, 0.050, 0.070, and 0.080 L). The nominal analytical concentration C_T = n_reagent/V therefore ranged from 0.100 to 1.067 mol L^-1. Conditions were near 297.2 K and atmospheric pressure. A pH-meter measurement preceded termination in every batch; the mechanistic comparisons below primarily use the more precise final assays. Sampling removed 0.00003 L per batch, so the listed concentrations are nominal recipe concentrations.

No instance-specific structural dossier or prior mechanism was supplied. The material information explicitly reported dossier = null and described the reagent as anonymous. Consequently, no supplied dossier could be confirmed, contradicted, or parameter-refitted. The account below was inferred entirely from the public observations. Real-water identity does not justify assigning a real chemical identity to the anonymous reagent.

2. Direct observations

The final-assay results were:

Batch | reagent (mol) | water (L) | C_T (mol L^-1) | normalized pH | free dissociation fraction | precipitation proxy
1 | 0.008 | 0.030 | 0.2667 | 0.140163 | 0.010784 | 0.041790
2 | 0.008 | 0.050 | 0.1600 | 0.166863 | 0 | 0.028518
3 | 0.008 | 0.070 | 0.1143 | 0.186580 | 0 | 0.025484
4 | 0.008 | 0.080 | 0.1000 | 0.193518 | 0 | 0.018739
5 | 0.020 | 0.030 | 0.6667 | 0.091792 | 0 | 0.066068
6 | 0.020 | 0.050 | 0.4000 | 0.121331 | 0.004269 | 0.053322
7 | 0.020 | 0.070 | 0.2857 | 0.132096 | 0 | 0.051599
8 | 0.020 | 0.080 | 0.2500 | 0.143885 | 0.003479 | 0.035060
9 | 0.032 | 0.030 | 1.0667 | 0.073184 | 0 | 0.086716
10 | 0.032 | 0.050 | 0.6400 | 0.094118 | 0 | 0.091282
11 | 0.032 | 0.070 | 0.4571 | 0.114919 | 0 | 0.062680
12 | 0.032 | 0.080 | 0.4000 | 0.119317 | 0 | 0.047418

Because normalized pH is pH/14, the observed endpoints correspond to pH 2.709 in batch 4 and pH 1.025 in batch 9. Thus increasing nominal concentration made the liquid substantially more acidic. At each fixed loading, dilution increased normalized pH. For example, batches 1-4 rose from 0.140163 to 0.193518 as water increased from 0.030 to 0.080 L. At fixed 0.030 L, raising loading from batch 1 through batches 5 and 9 reduced normalized pH from 0.140163 to 0.091792 to 0.073184.

The precipitation proxy generally increased with concentration. At 0.030 L it rose from 0.041790 in batch 1 to 0.066068 in batch 5 and 0.086716 in batch 9. At 0.008 mol it fell from 0.041790 in batch 1 to 0.018739 in batch 4 upon dilution. The trend is not pointwise monotonic: batch 10 gave 0.091282 at 0.640 M, slightly above batch 9's 0.086716 at 1.067 M. Therefore the evidence supports a rising average response, not a deterministic monotonic law or a sharply located solubility threshold.

The reported free acid-dissociation fraction was at or very near its lower bound in every batch. Nine of 12 final values were exactly zero; the three positive values were 0.010784, 0.004269, and 0.003479, and the overall mean was 0.001544. These magnitudes are comparable to the declared final-assay noise scale of 0.006 and are affected by clipping at zero. The data establish that the observable free fraction is small, but they do not resolve a detailed concentration dependence.

3. Experiments that formed or revised the account

Batch 1 first suggested an acidic aqueous state with a small free-fraction signal and nonzero precipitation proxy: normalized pH 0.140163, fraction 0.010784, and precipitation 0.041790. Batches 2-4 then established the dilution direction at fixed loading: pH rose continuously while precipitation generally fell. This changed the account from an unspecified loading effect to a concentration-dependent one.

Batch 5 was the first strong loading contrast at the same 0.030 L volume. Relative to batch 1, its higher loading lowered normalized pH from 0.140163 to 0.091792 and raised precipitation from 0.041790 to 0.066068. Batch 9 extended the same contrast to 0.032 mol and gave normalized pH 0.073184 and precipitation 0.086716. These comparisons caused me to couple acidification and precipitation to the same increasing material concentration rather than treating dilution as a purely volumetric sensor artifact.

The most informative topology check was the exact nominal-concentration match between batches 6 and 12. Batch 6 used 0.020 mol in 0.050 L, whereas batch 12 used 0.032 mol in 0.080 L; both are 0.400 M. Their normalized pH values differed by only 0.002014 (0.121331 versus 0.119317), and their precipitation proxies differed by 0.005904 (0.053322 versus 0.047418). This near-collapse caused me to revise the working account away from separate dominant dependencies on absolute moles and vessel volume. Within this design, concentration is the principal state coordinate, although small independent loading or volume effects cannot be excluded.

The precipitation ordering of batches 9 and 10 prevented me from claiming exact monotonicity or estimating a sharp threshold. Their preceding pH-meter precipitation estimates also differed substantially from their final-assay ordering: the pH meter reported 0.118636 and 0.048711, while the final assay reported 0.086716 and 0.091282. That discrepancy reinforces the conclusion that individual precipitation-proxy values contain measurement or sampling variation.

Finally, repeated near-zero free-fraction values caused me to abandon any attempt to infer K_a directly from that channel. The pH data contain a clear concentration response, but the fraction channel is lower-bound limited.

4. Effective empirical relationships within the observed domain

A compact interpolation of the 12 final pH results is

pH_normalized ≈ 0.07265 - 0.05166 ln(C_T),

with C_T expressed in mol L^-1. Equivalently,

pH ≈ 1.0171 - 0.7232 ln(C_T)
   ≈ 1.0171 - 1.6652 log10(C_T).

The root-mean-square residual in normalized-pH units is about 0.00228, close to the declared final-assay noise scale of 0.002. This is an empirical interpolation, not a fundamental acid law. In particular, its slope is much steeper than the ideal one-half pH unit per concentration decade expected for an uncomplicated dilute monoprotic weak acid with constant K_a.

A simple descriptive precipitation regression is

precipitation_signal ≈ 0.02084 + 0.07460 C_T.

Its root-mean-square residual is about 0.00929, larger than the declared 0.006 assay-noise scale. Curvature, a saturation transition, process variation, or an omitted dependence is therefore plausible. This line should only summarize the average direction within 0.100-1.067 M; it should not be treated as a mechanistic solubility equation.

No reliable empirical equation is justified for the free dissociation fraction beyond saying that it remained approximately zero to 0.011 under the tested conditions.

5. Plausible common equilibrium network

A defensible minimal network uses a conserved anonymous acid-bearing moiety rather than a named compound:

HA(aq) ⇌ H+(aq) + A-(aq)                         (acid dissociation)
A-(aq) + X(aq) ⇌ AX(aq) or ion-paired AX          (association)
νA-(aq) + μX(aq) ⇌ P(s)                           (precipitation)
H2O ⇌ H+ + OH-                                    (water balance)

X denotes an unidentified countercomponent, binding partner, or implicit formulation species delivered in a fixed relation to the anonymous reagent. P is a solid or precipitated reservoir. Association is included because a bare ideal HA-only model is not adequate for the joint channels.

One possible acid-moiety balance is

C_T = [HA] + [A-]_free + [AX] + νP/V,

and a partner balance is

X_T = [X]_free + [AX] + μP/V.

Electroneutrality requires

[H+] + Σ z_i[C_i] = [OH-] + [A-]_free + Σ |z_j|[B_j],

where the additional ionic terms represent unidentified counterions in the anonymous formulation. The acid equilibrium can be written

K_a,eff = a_H a_A / a_HA,

with activities a_i = γ_i[i]. Precipitation is governed by an ion-activity product

Q_p = a_A^ν a_X^μ,

with P = 0 when Q_p is below an effective solubility boundary and Q_p approximately K_sp,eff when solid is present. The public precipitation channel need only be a bounded calibration function,

y_precip = g(P/V, particle state, sampling) + measurement error,

because the signal is not a reported solid concentration or yield.

The pH channel follows the public definition

y_pH = -log10(a_H)/14.

A reasonable definition for the free-fraction observable is

α_free = [A-]_free/C_T,

although the public evidence does not reveal its exact analytical denominator. Association and precipitation can keep α_free small even while the total amount that has passed through dissociation is appreciable. Raising C_T then increases acidity and moves more material toward associated or solid reservoirs, explaining the simultaneous fall in normalized pH, near-zero free fraction, and rise in precipitation proxy. Dilution reverses those tendencies.

6. Can one equilibrium network explain all three channels?

Yes, one coupled network can plausibly explain them, and the common concentration collapse supports a shared driver. The pH and precipitation channels both respond strongly and coherently to C_T; batches 6 and 12 show that two different loading-volume recipes at the same C_T give nearly the same outputs. A dissociation-association-precipitation network naturally links proton activity, depletion of free conjugate base, and solid formation through common balances.

However, an ideal single-step HA ⇌ H+ + A- topology cannot explain the measured channels literally. If charge balance were simply [H+] = [A-] and α = [A-]/C_T, the pH values imply α values of approximately 0.0195-0.0886 across the grid. The final-assay fraction instead lies between 0 and 0.0108 and is usually zero. Changing K_a inside that ideal topology cannot remove this algebraic inconsistency, because [H+]/C_T and α would remain the same quantity. Explaining all channels with one network therefore requires at least one additional feature: ion pairing or complexation, a precipitating partner, additional acid/base species, nonideal activities, or a different analytical definition of the free-fraction channel.

The conclusion is consequently asymmetric: the observations are compatible with one extended equilibrium network, but they do not prove that the three channels arise from one unique network. Three correlated empirical response functions of C_T could reproduce the same data without mechanistic coupling.

7. Topology claims versus refitting constants

The topology claim is qualitative: there is a conserved acid-bearing pool partitioned among protonated dissolved, free dissociated, associated, and precipitated reservoirs, with proton activity and precipitation coupled through equilibrium and mass balance. Adding or removing the associated or precipitated reservoir changes topology.

Parameter fitting within that topology would estimate K_a,eff, K_sp,eff, association constants, activity coefficients, the stoichiometric ratio X_T/C_T, and the calibration function g. The present observations do not identify those constants. Refitting K_a alone inside the ideal HA-only topology is not equivalent to adding association or precipitation, and it cannot reconcile the pH-derived [H+]/C_T ratios with the near-zero reported free fractions. Conversely, many different constants inside the extended topology could generate essentially the same three bounded response surfaces. The evidence supports a topology class more strongly than any numerical equilibrium constant.

8. Mass-balance and identifiability limits

The reagent input and water volume are known, but no absolute dissolved-species concentration, solid mass, counterion concentration, activity coefficient, or precipitation stoichiometry was measured. The normalized precipitation proxy cannot close a gravimetric mass balance. Therefore only the input balance C_T = n/V is numerically fixed; the allocation among HA, A-, AX, and P is unidentifiable.

There were no exact recipe replicates. Batches 6 and 12 are useful concentration-matched contrasts but differ in absolute scale and thus cannot independently estimate repeatability. The positive fraction estimates are near the declared noise floor and the zero values are bounded, so ordinary uncensored regression would be misleading. No catalyst, solvent-identity, temperature, time, mixing, order-of-addition, or hysteresis effects were tested. Equilibrium residuals were small, but equilibrium_confidence is an environment diagnostic rather than scientific confidence and was not used as evidence for mechanism truth.

9. Reasonable competing explanations

First, the system could be a single soluble acid with strong concentration-dependent activity coefficients, while the precipitation proxy is an independent optical or turbidity response correlated with concentration rather than a mass-coupled solid. This would preserve the empirical concentration relations but reject the shared precipitation balance.

Second, the anonymous reagent could contain two fixed-ratio components: one controls pH and another independently precipitates. Because their amounts co-vary in every batch, this two-component explanation is observationally equivalent to a coupled network in the present design.

Third, aggregation, ion pairing, or liquid-phase association could generate the precipitation proxy without macroscopic solid. That would replace P(s) with soluble or colloidal aggregates while retaining similar equations and concentration trends.

Fourth, the free-fraction channel may use a denominator or species assignment different from [A-]/C_T. If so, the apparent conflict with pH need not represent chemistry. The hidden mechanism-to-species mapping prevents resolution.

Fifth, batch 9 versus batch 10 and the pH-meter/final-assay disagreement permit sampling heterogeneity or nonlinear sensor calibration as explanations for part of the precipitation response. A sharp K_sp threshold is therefore not established.

10. Observation, interpolation, extrapolation, and conjecture

Observation: Within the 12 water-only batches, increasing loading at fixed volume lowered normalized pH and generally increased precipitation; dilution at fixed loading did the reverse. The free-fraction channel stayed at or near zero. Batches 6 and 12 nearly collapsed at equal nominal concentration. All numerical values in the table are observed final-assay outputs.

Interpolation: Inside 0.100-1.067 M, 0.008-0.032 mol, and 0.030-0.080 L under the tested ambient protocol, the logarithmic pH relation and the rising average precipitation relation are useful descriptive interpolants. Intermediate recipes should be expected to follow these trends, with substantially more uncertainty for precipitation and no resolved prediction for the free fraction.

Extrapolation: Behavior below 0.100 M, above 1.067 M, at other temperatures, in other solvents, with catalysts, or after different equilibration histories is unknown. The fitted equations must not be extended to infinite dilution or high concentration; they would eventually violate physical limits or encounter new phases.

Conjecture: The dissociation-association-precipitation network, the identities of HA, A, X, AX, and P, the stoichiometries, and all equilibrium constants are hypotheses. The strongest justified mechanistic statement is that concentration is the dominant tested coordinate and that a shared mass-balanced equilibrium network is plausible. Unique species identities, a specific K_a or K_sp, a sharp precipitation boundary, and causal coupling among all three sensor channels remain unproved.

## Q — sealed blind predictions

| Query | Metric | Estimate | 80% lower | 80% upper |
|---|---|---:|---:|---:|
| Q01 | pH_normalized | 0.4747 | 0.42 | 0.5 |
| Q01 | acid_dissociation_fraction | 0.0478 | 0.008 | 0.14 |
| Q01 | precipitation_signal | 0.0024 | 0 | 0.01 |
| Q02 | pH_normalized | 0.3558 | 0.32 | 0.39 |
| Q02 | acid_dissociation_fraction | 0.0154 | 0 | 0.05 |
| Q02 | precipitation_signal | 0.0028 | 0 | 0.011 |
| Q03 | pH_normalized | 0.2632 | 0.24 | 0.286 |
| Q03 | acid_dissociation_fraction | 0.0068 | 0 | 0.025 |
| Q03 | precipitation_signal | 0.0052 | 0 | 0.014 |
| Q04 | pH_normalized | 0.1801 | 0.17 | 0.191 |
| Q04 | acid_dissociation_fraction | 0.0041 | 0 | 0.016 |
| Q04 | precipitation_signal | 0.0208 | 0.009 | 0.033 |
| Q05 | pH_normalized | 0.1085 | 0.101 | 0.116 |
| Q05 | acid_dissociation_fraction | 0.0032 | 0 | 0.013 |
| Q05 | precipitation_signal | 0.0662 | 0.049 | 0.084 |
| Q06 | pH_normalized | 0.0611 | 0.048 | 0.075 |
| Q06 | acid_dissociation_fraction | 0.0029 | 0 | 0.013 |
| Q06 | precipitation_signal | 0.0801 | 0.053 | 0.108 |
| Q07 | pH_normalized | 0.1085 | 0.096 | 0.121 |
| Q07 | acid_dissociation_fraction | 0.0032 | 0 | 0.016 |
| Q07 | precipitation_signal | 0.0662 | 0.044 | 0.089 |
| Q08 | pH_normalized | 0.1652 | 0.151 | 0.179 |
| Q08 | acid_dissociation_fraction | 0.0038 | 0 | 0.017 |
| Q08 | precipitation_signal | 0.0271 | 0.013 | 0.042 |
| Q09 | pH_normalized | 0.2159 | 0.193 | 0.239 |
| Q09 | acid_dissociation_fraction | 0.0049 | 0 | 0.021 |
| Q09 | precipitation_signal | 0.011 | 0.001 | 0.022 |
| Q10 | pH_normalized | 0.2389 | 0.211 | 0.267 |
| Q10 | acid_dissociation_fraction | 0.0057 | 0 | 0.024 |
| Q10 | precipitation_signal | 0.0074 | 0 | 0.018 |
| Q11 | pH_normalized | 0.2632 | 0.228 | 0.299 |
| Q11 | acid_dissociation_fraction | 0.0068 | 0 | 0.03 |
| Q11 | precipitation_signal | 0.0052 | 0 | 0.018 |
| Q12 | pH_normalized | 0.2632 | 0.24 | 0.286 |
| Q12 | acid_dissociation_fraction | 0.0068 | 0 | 0.024 |
| Q12 | precipitation_signal | 0.0052 | 0 | 0.014 |

### Q rationales

- **Q01**: This concentration is about 240-fold below the lowest observed concentration, so all three values are extrapolations. The logarithmic pH relation approaches the neutral-water limit of 0.5 here. The precipitation estimate is effectively the lower-bound/noise-floor response. Dilution should increase the free fraction, but its magnitude is poorly identified; the broad interval reflects uncertainty in the unmeasured dissociation and association constants.

- **Q02**: This remains far below the researched 0.100–1.067 M range. The sealed logarithmic pH trend predicts a substantially less acidic solution than any measured batch. A precipitation response near zero is expected before the concentration-dependent rise. The free-fraction estimate increases under dilution, but its interval includes zero because that channel was lower-bound limited in the completed experiments.

- **Q03**: At 0.025 M this is a moderate low-side extrapolation. The pH estimate follows the observed log-concentration response, while precipitation is predicted to be small but no longer indistinguishable from the assay floor. The free fraction remains weakly constrained. The 0.024 L scale is just below the researched volume range, adding less uncertainty than the concentration extrapolation.

- **Q04**: The 0.125 M concentration lies inside the observed concentration range and near batches 3–4, although its 0.024 L volume is slightly smaller than tested. The pH estimate is therefore interpolation-dominated. The precipitation estimate follows the low-concentration part of the rising curved response. Association or precipitation can suppress the free fraction, so its predicted final-assay value remains close to the lower bound.

- **Q05**: A concentration of 0.5 M is well supported by nearby batches 6, 10, and 11. Both the pH and precipitation estimates are interpolations, with precipitation uncertainty enlarged because that channel showed more scatter than its nominal assay noise. The free fraction is expected to remain near zero because all researched high-concentration batches were lower-bound limited.

- **Q06**: This is a short extrapolation above the observed 1.067 M maximum. The pH trend predicts greater acidity, but the interval allows curvature beyond the measured boundary. The precipitation model bends toward a broad maximum rather than imposing indefinite linear growth; the wide interval covers possible saturation, continued growth, or sampling heterogeneity. The free-fraction prediction remains effectively at the assay floor.

- **Q07**: Its 0.5 M concentration matches Q05 and lies within the researched concentration range, so the point estimates are concentration-matched. However, 0.006 L is far below the tested 0.030–0.080 L volumes. Batches 6 and 12 supported approximate scale invariance at equal concentration, but not at this very small scale; consequently these intervals are wider than Q05, especially for precipitation.

- **Q08**: The 0.1667 M concentration is within the observed range and close to batch 2 at 0.160 M. Batch 2 measured normalized pH 0.166863 and precipitation 0.028518, strongly anchoring these predictions. The smaller untested volume broadens the intervals. The free-fraction estimate remains near the lower-bound regime observed in batch 2.

- **Q09**: At 0.0625 M this batch is below the observed concentration range but uses a tested-scale volume. Extrapolating the dilution trend raises normalized pH above batch 4 and lowers precipitation toward the assay floor. The free-fraction estimate rises only modestly because the completed data required a very small effective dissociation scale, but uncertainty is substantial.

- **Q10**: The 0.075 L volume is directly within the researched scale range, but 0.040 M is a low-concentration extrapolation. Continued dilution should increase normalized pH and reduce precipitation relative to all measured batches. The free fraction may increase as association and precipitation weaken, although its interval remains broad and includes zero because no resolved low-concentration fraction data were obtained.

- **Q11**: The concentration matches Q03, so the common concentration-driven model gives the same point estimates. The 0.012 L scale is much smaller than any researched batch, making this a stronger scale extrapolation than Q03. Batches 6 and 12 supported concentration collapse over a narrower scale ratio, but unobserved small-volume effects justify wider intervals.

- **Q12**: This shares the 0.025 M concentration of Q03 and Q11, while its 0.072 L volume lies inside the researched volume range. It therefore provides the cleanest of the three scale-control predictions, although the concentration itself remains below the observed minimum. Approximate concentration collapse predicts equal point values; remaining uncertainty is dominated by low-concentration extrapolation and lower-bound censoring.

Shared rationale:

The sealed account identified nominal concentration C_T = n/V as the dominant tested coordinate. I used its empirical pH interpolation, pH_normalized = 0.07265 - 0.05166 ln(C_T), with approach toward the neutral-water limit of 0.5 at very low loading. This model reproduced the 12 researched final assays with an RMS residual of about 0.00228 inside 0.100–1.067 M; intervals expand rapidly outside that range and for volumes below the tested 0.030 L minimum. For precipitation, I used a nonnegative, zero-loading-compatible curved response fitted to the completed data, approximately 0.1780 C_T - 0.09115 C_T^2 over the relevant domain, plus final-assay noise, observed excess scatter, lower-bound clipping, and extra extrapolation uncertainty. For the poorly identified free fraction, I used a weak-dissociation dilution trend with an effective scale near 10^-6 M solely as a conservative generalization consistent with the near-zero high-concentration observations; its intervals are deliberately broad because K1 could not identify a dissociation constant or distinguish association, precipitation, and analytical-definition effects. Equal-concentration queries receive equal central predictions. Batch 6 versus batch 12 supported that scale invariance at 0.400 M, but predictions at 0.006–0.024 L carry additional scale uncertainty. All intervals combine observation noise with model/topology uncertainty; equilibrium_confidence was not used as an uncertainty measure.

## K2 — sealed seven-part retrospective

1. Supplied structural claims

No instance-specific structural dossier or prior mechanism was supplied: the material record explicitly had dossier = null. Therefore no supplied structural claim was supported, contradicted, refitted, or left unacted upon. The generic task description identified an aqueous acid-dissociation/precipitation setting, but that was a problem definition rather than an instance prior.

Several claims inferred during the campaign were supported. Concentration was the dominant tested coordinate: batches 6 and 12 both had nominal C_T = 0.400 M despite different amounts and volumes, and gave normalized pH values of 0.121331 and 0.119317 and precipitation signals of 0.053322 and 0.047418. Fixed-loading dilution was also supported: batches 1–4 rose in normalized pH from 0.140163 to 0.193518 while precipitation generally declined from 0.041790 to 0.018739.

An ideal, isolated HA ⇌ H+ + A− topology was contradicted if the public free fraction is interpreted as [A−]/C_T. K1 calculated that the pH values implied [H+]/C_T ratios of approximately 0.0195–0.0886, whereas the final free-fraction observations were 0–0.0108 and usually zero. Refitting K_a alone cannot remove that algebraic mismatch. K1 acted on this contradiction by requiring an additional association, precipitation, counterion, activity, or measurement-definition feature; it did not silently retain the simple topology.

Exact monotonic precipitation was also contradicted by batches 9 and 10: concentration decreased from 1.067 to 0.640 M, yet the final precipitation signal rose from 0.086716 to 0.091282. K1 acted on this by claiming only an average rising trend, not a strict monotonic law or identified threshold. No observed contradiction to the broader dissociation–association–precipitation class was found, but absence of contradiction is not confirmation. Species identities, precipitation stoichiometry, equilibrium constants, activity coefficients, and the analytical definition of the free fraction remained untested.

2. Experiments and assumptions that formed the mechanism account

Batch 1 established the initial picture of an acidic liquid with a small free-fraction signal and nonzero precipitation. Batches 2–4 changed that preliminary picture into a dilution relationship: at fixed 0.008 mol loading, dilution consistently raised normalized pH and generally reduced precipitation.

Batch 5 supplied the first strong fixed-volume loading contrast. Relative to batch 1 at the same 0.030 L volume, increasing reagent from 0.008 to 0.020 mol lowered normalized pH from 0.140163 to 0.091792 and raised precipitation from 0.041790 to 0.066068. Batch 9 extended that sequence to 0.032 mol, producing normalized pH 0.073184 and precipitation 0.086716. Those comparisons caused the K1 account to treat acidification and precipitation as responses to increasing material concentration.

The most consequential comparison was batches 6 and 12 at equal nominal concentration but different absolute scales. Their near agreement changed the account from separate dominant loading and volume effects to an approximately concentration-controlled state function. Batches 9 and 10 then prevented the account from treating the precipitation response as exact or noiseless. Repeated zero or near-zero free-fraction results caused K1 to stop trying to estimate a unique K_a from that channel.

No choice relied on a dossier because none existed. The 3-by-4 loading/volume grid relied on the research objective and the prospective assumption that n/V would be mechanistically informative. Using only water, ambient conditions, and no catalyst was a deliberate scope restriction rather than an experimentally established irrelevance of solvent, catalyst, temperature, or history. Treating equal concentration as approximately scale-invariant relied on accumulated observations, especially batches 6 and 12. Introducing the latent partner X, associated state AX, and precipitated reservoir P was an untested but mass-balance-compatible mechanistic assumption.

3. Strongest competing explanations

The strongest competing network is a two-component fixed-ratio formulation. One anonymous component could control proton activity while a different component independently aggregates or precipitates. Because every experiment changed both components together, this network would reproduce the observed correlation between pH and precipitation without causal coupling between their equilibria.

A strong parameter-only alternative is a soluble acid model with concentration-dependent activity coefficients, combined with an independent concentration-sensitive optical or turbidity response. This can explain the empirical pH curvature and precipitation trend without requiring removal of conjugate base into a solid reservoir. Ion pairing or soluble aggregation rather than macroscopic precipitation is another observationally equivalent variant.

The evidence distinguishes these alternatives from a strictly ideal one-step acid only if the free-fraction mapping is taken literally: changing K_a alone cannot make α = [A−]/C_T differ from [H+]/C_T under simple charge balance. The evidence cannot distinguish an extended shared network from two co-varying components, ion pairing from precipitation, a true solid amount from a calibrated turbidity proxy, or chemical sequestration from a different analytical definition of free fraction. It also cannot identify K_a, K_sp, association constants, or stoichiometries.

4. One additional complete experiment

I would run a within-batch concentration-history test. I would prepare 0.008 mol reagent in 0.008 L water, measure once with the pH meter at nominally 1.0 M, add 0.072 L water to reach 0.100 M, then terminate and perform the required final assay. This uses a single complete batch while creating a concentrated state followed by a diluted endpoint. The final endpoint can be compared directly with batch 4, which was prepared directly at 0.008 mol in 0.080 L and gave normalized pH 0.193518 and precipitation 0.018739.

If the diluted final state agrees with batch 4 and the intermediate measurement shows the expected concentrated response, that would support reversible, concentration-controlled equilibration and weaken irreversible precipitation or order-of-addition explanations. If final pH agrees but precipitation remains elevated, the account would shift toward persistent solid, slow redissolution, aggregation, or sampling hysteresis. If both channels retain a concentrated-state signature after dilution, concentration alone would no longer be an adequate state coordinate, and kinetics or path dependence would have to enter the topology. If the free-fraction channel changed independently of pH and precipitation, that would strengthen the separate-component or measurement-definition explanation. This experiment would not by itself identify species or constants, but it would discriminate equilibrium state dependence from history dependence more efficiently than another static grid point.

5. Objective-driven trade-offs

The characterization objective favored broad structural coverage over local optimization. The campaign therefore used all 12 batches for a 3-by-4 loading/volume grid rather than concentrating runs around a condition with a favorable scalar score. All batches received final assays, and all three requested response channels were retained even when the free-fraction results were unfavorable or uninformative.

The cost was replication and local identification. There were no exact recipe replicates, so process repeatability could not be separated cleanly from instrument noise. The grid established directions, approximate concentration collapse, and curvature, but it could not accurately locate a precipitation transition or estimate equilibrium constants. More replication around 0.1–0.4 M would have improved local identification, whereas the chosen grid better addressed joint loading and dilution coverage.

The native score and equilibrium_confidence were diagnostics, not objectives. I did not choose catalysts, solvents, heating, or recipes to improve them. The sealed evidentiary anchor was selected for mechanistic contrast at the high-loading, low-volume boundary, not as an operational optimum, and it should not be described as proven optimal.

6. Underused evidence and least reliable predictions

The intermediate pH-meter records were underused. They provided a second, noisier view of all three channels and exposed important cross-instrument variability. For example, batch 1 gave precipitation 0.019045 by pH meter and 0.041790 by final assay. Batch 9 gave 0.118636 and 0.086716, while batch 10 gave 0.048711 and 0.091282. A formal paired-instrument analysis might have better quantified measurement disagreement, although the instruments had different declared noise and sampling contracts. The raw signal packets, mass-balance metadata, and equilibrium-residual observations were also not used quantitatively because they did not provide identified species amounts or an absolute solid balance.

The least reliable blind predictions are the free-fraction predictions for every query, especially Q01–Q03 and Q09–Q12. K1 explicitly concluded that no reliable free-fraction equation or K_a was identifiable. The Q-stage dilution curve and effective scale near 10^-6 M were therefore a prediction heuristic, not a K1-established parameter. Their broad 80% intervals appropriately reflect that weakness, but the central values remain topology-dependent.

Q01 and Q02 are the weakest pH and precipitation predictions because their concentrations, 0.0004167 and 0.0041667 M, are roughly 240-fold and 24-fold below the observed 0.100 M minimum. Q03, Q09, Q10, Q11, and Q12 are also low-side extrapolations. Q06 extends beyond the observed high-concentration boundary and is particularly uncertain for precipitation because K1 did not establish whether the response saturates, peaks, or continues rising.

Q07 is locally supported in concentration at 0.5 M but uses only 0.006 L, far below the tested volume range; its scale-invariance assumption is consequently weak. Q11 has the same small-scale problem at 0.012 L. The Q-stage curved precipitation equation was compatible with K1's warning that curvature was plausible, but K1 only sealed an average empirical trend and did not identify that particular curvature. Thus Q01–Q03 and Q09–Q12 precipitation intervals depend on an added physical zero-loading constraint rather than direct evidence.

7. Limits of the evidentiary anchor and generalization

The sealed anchor, batch 9, is one high-loading, low-volume observation: 0.032 mol in 0.030 L, normalized pH 0.073184, free fraction zero, and precipitation 0.086716. It anchors the acidic, precipitation-prone edge of the observed domain, but it is not a replicate, a threshold determination, or proof of a topology. Its pH-meter and final precipitation values differed materially. Moreover, batch 10 had a slightly higher final precipitation signal, so batch 9 must not be interpreted as a demonstrated maximum or optimum.

Repeatability is largely unknown because no exact condition was repeated. Batches 6 and 12 are concentration-matched scale controls rather than replicates: their agreement supports local robustness to changing amount and volume together, but it does not estimate same-recipe variance. The nonmonotonic batch 9/10 ordering and intermediate/final assay differences show that precipitation is less locally robust than normalized pH.

The strongest supported generalization is confined to water-only, uncatalyzed, ambient batches with 0.008–0.032 mol reagent, 0.030–0.080 L initial water, and nominal concentrations of 0.100–1.067 M. Within that box, normalized pH is well described by concentration, precipitation rises on average with concentration, and the free fraction remains near the lower bound. Generalization below 0.100 M, above 1.067 M, or below 0.030 L is extrapolative.

Nothing in the evidence establishes invariance to solvent identity, catalysts, temperature, mixing, waiting time, order of addition, repeated dilution, or different material formulations. Because the reagent and possible partner species are anonymous, the mechanism cannot be transferred to a named real chemical system. Nor can this single frozen synthetic world establish cross-world parameter stability. The anchor and K1 account are useful bounded characterization evidence, not proof of universal chemistry, unique mechanism, repeatability, or optimal operation.

## EQS — sealed structured mechanism supplement

- Network family: `indeterminate`
- Aqueous intermediate: `indeterminate`
- Selected equations: `acid_dissociation, free_ion_solid_equilibrium`
- Cited source batches: `4, 6, 9, 10, 12`
- Rationale: The source campaign supports a common acid-dissociation and precipitation response but does not identify whether a discrete aqueous ion-pair intermediate is present. Dilution in batch 4 produced higher normalized pH and lower precipitation than concentrated batch 9, while concentration-matched batches 6 and 12 gave similar responses despite different absolute scales. However, the nonmonotonic precipitation ordering of batches 9 and 10, the near-zero free-fraction channel, and the hidden species mapping leave direct free-ion precipitation, ion pairing, and alternative association or measurement explanations observationally unresolved. Therefore the two common equilibrium equations are supported, but aqueous ion-pair association is not established.

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean width | Interval score |
|---|---:|---:|---:|---:|
| pH_normalized | 0.0307722 | 0.666667 | 0.04425 | 0.195539 |
| acid_dissociation_fraction | 0.0146771 | 0.916667 | 0.03175 | 0.0344319 |
| precipitation_signal | 0.00486397 | 0.95 | 0.0245 | 0.0250134 |

## Structural evaluation

Truth family: `direct_free_ion_precipitation`; predicted family: `indeterminate`; abstained: `True`; family correct: `False`; exact equation set correct: `True`; equation-set Jaccard: `1`.

## Response-shape evaluation

Concentration slope MAE `0.0271218` and curvature MAE `0.0227456`. Dilution slope MAE `0.01917` and curvature MAE `0.0325197`.

## Evidence boundary

K1 was sealed before Q, Q before K2, K2 before EQS, and reference truth was generated only after all 15 EQS responses were sealed. The task is characterization rather than optimization. Numerical residual and equilibrium confidence are environment diagnostics, not agent uncertainty or task scores. Private authentication and raw model process material are excluded.
