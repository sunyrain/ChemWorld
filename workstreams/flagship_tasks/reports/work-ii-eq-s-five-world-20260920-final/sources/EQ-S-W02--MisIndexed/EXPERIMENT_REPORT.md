# EQ-S-W02--MisIndexed — final English experiment report

World `EQ-S-W02`; information arm `MisIndexed`; task `mechanism characterization`; effective status `completed`; result origin `original`.

## Source campaign

The autonomous campaign completed 12/12 batches and 72 recorded operations. Exact replay is `True`; rollbacks: 0.

| Batch | Solvent L | Reagent mol | Measurements | pH normalized | Free dissociation | Precipitation signal | Residual |
|---:|---:|---:|---|---:|---:|---:|---:|
| 1 | 0.04 | 0.005 | ph_meter, final_assay | 0.141503 | 0 | 0.00107888 | 0 |
| 2 | 0.04 | 0.01 | ph_meter, final_assay | 0.125437 | 0 | 0 | 0.00201976 |
| 3 | 0.04 | 0.015 | ph_meter, final_assay | 0.112556 | 0.00239883 | 0.0102555 | 0 |
| 4 | 0.04 | 0.02 | ph_meter, final_assay | 0.102277 | 0.00142731 | 0 | 0 |
| 5 | 0.04 | 0.025 | ph_meter, final_assay | 0.0919949 | 0.000688188 | 0.0136015 | 0 |
| 6 | 0.04 | 0.03 | ph_meter, final_assay | 0.0828646 | 0 | 0.0411161 | 0 |
| 7 | 0.04 | 0.035 | ph_meter, final_assay | 0.0736732 | 0.00269912 | 0.048383 | 0.000206568 |
| 8 | 0.04 | 0.04 | ph_meter, final_assay | 0.0683644 | 0 | 0.0607795 | 0.00424874 |
| 9 | 0.02 | 0.015 | ph_meter, final_assay | 0.0816888 | 0.000422585 | 0.0400128 | 0 |
| 10 | 0.03 | 0.015 | ph_meter, final_assay | 0.0974588 | 0.00234835 | 0 | 0 |
| 11 | 0.06 | 0.015 | ph_meter, final_assay | 0.121143 | 0.00109038 | 0.00817137 | 0 |
| 12 | 0.08 | 0.015 | ph_meter, final_assay | 0.129956 | 0 | 0 | 0 |

### Sealed evidentiary anchor

Batch `8`: Highest aqueous loading in the fixed-catalyst series; it anchors the low-pH, clearly positive precipitation end of the observed loading response and complements the dilution contrasts.

## K1 — sealed mechanistic report

Mechanistic report

1. Experimental basis and scope

The campaign comprised 12 completed, independent aqueous batches. Every batch contained water, 0.003 mol of benchmark Catalyst A, and 0.005–0.040 mol of anonymous reagent. Initial liquid volumes were 0.020–0.080 L, giving nominal reagent loadings C_R = n_R/V from 0.125 to 1.000 mol L^-1. No heating or deliberate aging was applied. Conditions remained near 297.2 K and atmospheric pressure. Each batch received one in-process pH-meter measurement, was terminated, and then received a destructive final assay. Thus, the primary comparisons are equilibrium-like endpoint comparisons, not kinetic measurements.

The final-assay results were:

Batch 1: 0.005 mol in 0.040 L, C_R = 0.125 M; normalized pH 0.141503, free acid-dissociation fraction 0.000000, precipitation proxy 0.001079.
Batch 2: 0.010 mol in 0.040 L, C_R = 0.250 M; normalized pH 0.125437, fraction 0.000000, precipitation 0.000000.
Batch 3: 0.015 mol in 0.040 L, C_R = 0.375 M; normalized pH 0.112556, fraction 0.002399, precipitation 0.010256.
Batch 4: 0.020 mol in 0.040 L, C_R = 0.500 M; normalized pH 0.102277, fraction 0.001427, precipitation 0.000000.
Batch 5: 0.025 mol in 0.040 L, C_R = 0.625 M; normalized pH 0.091995, fraction 0.000688, precipitation 0.013601.
Batch 6: 0.030 mol in 0.040 L, C_R = 0.750 M; normalized pH 0.082865, fraction 0.000000, precipitation 0.041116.
Batch 7: 0.035 mol in 0.040 L, C_R = 0.875 M; normalized pH 0.073673, fraction 0.002699, precipitation 0.048383.
Batch 8: 0.040 mol in 0.040 L, C_R = 1.000 M; normalized pH 0.068364, fraction 0.000000, precipitation 0.060779.
Batch 9: 0.015 mol in 0.020 L, C_R = 0.750 M; normalized pH 0.081689, fraction 0.000423, precipitation 0.040013.
Batch 10: 0.015 mol in 0.030 L, C_R = 0.500 M; normalized pH 0.097459, fraction 0.002348, precipitation 0.000000.
Batch 11: 0.015 mol in 0.060 L, C_R = 0.250 M; normalized pH 0.121143, fraction 0.001090, precipitation 0.008171.
Batch 12: 0.015 mol in 0.080 L, C_R = 0.1875 M; normalized pH 0.129956, fraction 0.000000, precipitation 0.000000.

Batch 8 is the sealed evidentiary anchor. It anchors the high-loading end rather than representing an optimized process condition.

2. Direct observations

Loading and dilution acted primarily through nominal concentration. In the fixed-volume series, batches 1–8, normalized pH decreased monotonically from 0.141503 at 0.125 M to 0.068364 at 1.000 M. Because normalized pH is pH/14, this corresponds to ordinary pH values of approximately 1.98 and 0.96, respectively.

The deliberate concentration matches support concentration, rather than total reagent moles alone, as the principal public predictor. At 0.750 M, batches 6 and 9 used different amounts and volumes but gave normalized pH values of 0.082865 and 0.081689 and precipitation values of 0.041116 and 0.040013. At 0.500 M, batches 4 and 10 gave normalized pH 0.102277 and 0.097459, with both precipitation estimates clipped to zero. At 0.250 M, batches 2 and 11 gave normalized pH 0.125437 and 0.121143; their precipitation values, 0 and 0.008171, differ only modestly relative to the final-assay precipitation noise scale of 0.006 per observation. These pairs do not establish perfect concentration scaling, but they substantially weaken an explanation based only on absolute reagent amount or vessel volume.

The precipitation response showed a concentration-dependent crossover rather than a sharply resolved threshold. It was absent or small below about 0.6 M, apart from noisy low positive values such as 0.010256 in batch 3. It then rose to 0.041116 and 0.040013 in the two 0.750 M batches, 0.048383 at 0.875 M, and 0.060779 at 1.000 M. Batch 4 being zero at 0.500 M while batch 3 was 0.010256 at 0.375 M shows why these data do not justify a strictly monotonic deterministic threshold at low signal.

The final-assay free dissociation fraction was not quantitatively resolved. All 12 values lay between 0 and 0.002699, below the declared final-assay standard uncertainty of 0.006. Several were clipped at zero. The in-process pH meter sometimes returned larger estimates—for example 0.029880 in batch 1 and 0.029206 in batch 5—but its uncertainty for this channel was 0.015, and the corresponding final values were 0 and 0.000688. Consequently, apparent fluctuations in this fraction should not be fitted as a meaningful loading trend.

Final equilibrium residuals were zero in most batches and small in the others, including 0.002020 in batch 2 and 0.004249 in batch 8. These are instrument/environment outputs, not independent proof that a particular molecular topology is correct. Likewise, equilibrium_confidence is an environment diagnostic and is not used here as scientific confidence.

3. Empirical interpolation

Across the observed 0.125–1.000 M range, a simple descriptive regression is

pH_normalized ≈ 0.07270 - 0.03539 ln(C_R / 1 M).

Its root-mean-square residual over the 12 final assays is about 0.00334. This relation compactly describes the measured loading and dilution response, but it is an interpolation, not a fitted acid-dissociation constant. It absorbs activity effects, precipitation coupling, formulation effects, and the unknown mapping from hidden state to the public channel.

For precipitation, a global unconstrained linear regression is physically unattractive because it produces a negative intercept. The observations are better summarized as a bounded, low-signal regime below roughly 0.5–0.6 M followed by a rising regime: approximately 0.04 at 0.75 M and 0.061 at 1.0 M. The transition location and shape are not accurately identified, so I do not assign a numerical solubility product from these proxy values.

No useful empirical interpolation for the dissociation fraction is supported: its full final-assay range is smaller than one stated standard uncertainty.

4. Plausible unified equilibrium network

A parsimonious network consistent with the supplied qualitative structural account is

HA(aq) ⇌ H+(aq) + A-(aq)
M+(aq) + A-(aq) ⇌ MA(s).

Here HA is the anonymous weak-acid-like reagent state, A- is its free conjugate base, M+ is a formal precipitating counterion or formulation component, and MA(s) is a solid or solid-like sink. These names describe roles, not real chemical identities. In particular, the experiment did not establish that benchmark Catalyst A is literally the source of M+.

In activity form,

K_a = a_H a_A / a_HA,
K_sp = a_M a_A when solid is present.

A useful precipitation complementarity condition is

s ≥ 0,
K_sp - a_M a_A ≥ 0,
s(K_sp - a_M a_A) = 0,

where s is the amount of precipitated MA per chosen volume basis. With 1:1 stoichiometry, formal balances would be

C_A,total = [HA] + [A-] + s,
C_M,total = [M+] + s.

A complete implementation would also include water autoionization, spectator ions, electroneutrality, and activity coefficients. A schematic charge balance is

[H+] + [M+] + other cations = [A-] + [OH-] + other anions.

The public pH channel is related to hydrogen activity by

pH_normalized = -log10(a_H)/14.

A plausible definition of the free dissociation channel is

alpha_free = [A-]/([HA] + [A-]),

although the hidden benchmark mapping was not disclosed, so this definition must not be treated as verified. The precipitation channel is explicitly a bounded proxy, and can only safely be represented as

precipitation_signal = clip(g(s, supersaturation, or solid population) + measurement error, 0, 1),

with unknown monotone response function g.

This single network can qualitatively couple all three public responses. Increasing concentration raises hydrogen activity and lowers normalized pH. Once the ion product approaches a solubility boundary, removal of A- into MA(s) can shift acid dissociation and produce a rising solid proxy. The matched-concentration batches show that pH and precipitation can collapse together despite changes in amount and dilution. However, the dissociation-fraction channel is too poorly resolved to demonstrate the expected quantitative third leg of this coupling. Thus one network is sufficient, but the data do not prove that it is unique or fully validate all three species mappings.

5. How the account formed and changed

Batch 1 established the dilute endpoint: normalized pH 0.141503 and essentially no precipitation. Batches 2–5 showed a smooth pH decline but only intermittent near-zero precipitation. At that stage, the evidence supported acidification with loading but did not yet require a precipitation branch.

Batches 6–8 revised that view. The precipitation proxy rose reproducibly from 0.041116 at 0.750 M to 0.060779 at 1.000 M while normalized pH continued downward. This made a coupled precipitation branch plausible.

Batches 9–12 then tested whether the preceding pattern was merely an amount or vessel-size artifact. Batch 9 reproduced batch 6 closely at 0.750 M despite using half the reagent amount and half the volume. Batches 10 and 11 also approximately reproduced the corresponding 0.500 and 0.250 M pH levels. These comparisons caused concentration to replace absolute loading as the primary empirical coordinate, while leaving small secondary volume or formulation effects possible.

The dissociation-fraction account was revised in the opposite direction. Some in-process measurements initially suggested fractions of a few percent, but the more precise final assays repeatedly returned values near zero with uncertainty exceeding their spread. I therefore treat this channel as unresolved rather than forcing it to follow the pH trend.

6. Topology claim versus parameter refitting

The topology claim is that the minimal species graph contains a weak-acid dissociation step and a direct free-ion precipitation step, with no distinct, kinetically or thermodynamically required aqueous MA intermediate. That is a statement about which states and edges exist.

Changing K_a, K_sp, activity coefficients, formal background-ion concentration, or the proxy calibration g while retaining HA ⇌ H+ + A- and M+ + A- ⇌ MA(s) is parameter refitting within the same topology. Such refitting can move the pH curve and precipitation crossover, but it cannot establish that an omitted aqueous complex is absent.

The present observations favor the direct topology only by parsimony: two coupled equilibria can explain the broad pH and precipitation patterns, and no public observation requires an intermediate. They do not identify K_a or K_sp separately, because the activities, M balance, spectator ions, and precipitation-proxy calibration are unknown. They also do not discriminate direct precipitation from a rapid sequence through an unobserved soluble complex.

7. Supplied dossier or prior

No task-specific nominal property dossier was supplied: the material record explicitly reported dossier = null. No instance-specific prior values for K_a, K_sp, activities, or proxy calibration were supplied either.

Separately, a qualitative structural prior was supplied. It proposed the direct network HA ⇌ H+ + A- and M+ + A- ⇌ MA(s), with no distinct aqueous MA species, and predicted a joint three-channel concentration response. The pH and precipitation observations support that prior qualitatively and within the tested local domain. The concentration-matched pairs particularly support a common concentration-controlled account. The proposed absence of aqueous MA was left untested, because no species-resolved public mapping could distinguish direct precipitation from rapid ion pairing. The promised three-channel implication must also be revised: two channels behaved coherently, while the free-dissociation fraction was below useful final-assay resolution.

8. Unidentifiable factors and competing explanations

The following were not identified: the chemical identities of HA, A-, M+, or MA; whether Catalyst A supplies M+ or only changes activities; K_a; K_sp; activity coefficients; ionic strength; spectator-ion concentrations; solid stoichiometry beyond the plausible 1:1 model; the conversion between precipitated amount and public proxy; nucleation or equilibration times; and the cause of the small matched-concentration offsets.

Reasonable competing explanations include:

(a) Soluble-complex pathway: M+ + A- ⇌ MA(aq), followed by MA(aq) ⇌ MA(s). A fast or low-population intermediate would be observationally equivalent here.

(b) Ion pairing without a macroscopic solid: the precipitation proxy could respond to aggregates or supersaturation rather than equilibrium solid mass.

(c) Empirical common-cause response: pH and the precipitation proxy could both be independent functions of nominal concentration. Their correlation alone does not prove that precipitation causally shifts acid dissociation.

(d) Nonideal-solution explanation: concentration-dependent activity coefficients or background electrolyte could generate curvature and an apparent precipitation crossover without constant ideal-solution K values.

(e) Hidden formulation or volume effects: Catalyst A was fixed at 0.003 mol rather than fixed concentration. The approximate concentration collapse argues against a dominant catalyst-concentration effect, but the design cannot eliminate it.

9. Observation, interpolation, extrapolation, and conjecture

Observation: the tabled 12 final assays, the selected in-process comparisons, the monotonic fixed-volume pH decline, the high-loading precipitation rise, and the near-zero unresolved final dissociation fractions are direct observations.

Interpolation: the logarithmic pH equation and the qualitative precipitation crossover summarize only aqueous, Catalyst-A batches at 297.2 K, 0.125–1.000 M reagent loading, 0.020–0.080 L volume, and the tested operation sequence. Predictions between tested concentrations within this domain are interpolations.

Extrapolation: behavior below 0.125 M, above 1.000 M, at other temperatures, after long equilibration, with other solvents or catalysts, without Catalyst A, or under different ionic backgrounds is unsupported. The empirical logarithmic pH relation and rising precipitation trend should not be projected there.

Conjecture: the identities of hidden species, the association of Catalyst A with M+, the exact definition of alpha_free, direct rather than intermediate-mediated precipitation, and any numerical K_a or K_sp are mechanistic conjectures. The direct two-equilibrium network is the most economical current account, not a uniquely identified molecular truth.

## Q — sealed blind predictions

| Query | Metric | Estimate | 80% lower | 80% upper |
|---|---|---:|---:|---:|
| Q01 | pH_normalized | 0.23 | 0.17 | 0.36 |
| Q01 | acid_dissociation_fraction | 0.015 | 0 | 0.12 |
| Q01 | precipitation_signal | 0 | 0 | 0.012 |
| Q02 | pH_normalized | 0.194 | 0.15 | 0.29 |
| Q02 | acid_dissociation_fraction | 0.008 | 0 | 0.06 |
| Q02 | precipitation_signal | 0 | 0 | 0.012 |
| Q03 | pH_normalized | 0.167 | 0.13 | 0.23 |
| Q03 | acid_dissociation_fraction | 0.004 | 0 | 0.03 |
| Q03 | precipitation_signal | 0 | 0 | 0.014 |
| Q04 | pH_normalized | 0.142 | 0.115 | 0.18 |
| Q04 | acid_dissociation_fraction | 0.001 | 0 | 0.015 |
| Q04 | precipitation_signal | 0.001 | 0 | 0.018 |
| Q05 | pH_normalized | 0.1 | 0.075 | 0.13 |
| Q05 | acid_dissociation_fraction | 0.001 | 0 | 0.012 |
| Q05 | precipitation_signal | 0.003 | 0 | 0.03 |
| Q06 | pH_normalized | 0.061 | 0.03 | 0.1 |
| Q06 | acid_dissociation_fraction | 0.001 | 0 | 0.015 |
| Q06 | precipitation_signal | 0.078 | 0.015 | 0.17 |
| Q07 | pH_normalized | 0.1 | 0.06 | 0.15 |
| Q07 | acid_dissociation_fraction | 0.001 | 0 | 0.02 |
| Q07 | precipitation_signal | 0.003 | 0 | 0.045 |
| Q08 | pH_normalized | 0.136 | 0.105 | 0.18 |
| Q08 | acid_dissociation_fraction | 0.001 | 0 | 0.018 |
| Q08 | precipitation_signal | 0.001 | 0 | 0.022 |
| Q09 | pH_normalized | 0.152 | 0.115 | 0.215 |
| Q09 | acid_dissociation_fraction | 0.002 | 0 | 0.025 |
| Q09 | precipitation_signal | 0 | 0 | 0.016 |
| Q10 | pH_normalized | 0.159 | 0.12 | 0.23 |
| Q10 | acid_dissociation_fraction | 0.003 | 0 | 0.035 |
| Q10 | precipitation_signal | 0 | 0 | 0.015 |
| Q11 | pH_normalized | 0.167 | 0.115 | 0.25 |
| Q11 | acid_dissociation_fraction | 0.004 | 0 | 0.045 |
| Q11 | precipitation_signal | 0 | 0 | 0.02 |
| Q12 | pH_normalized | 0.167 | 0.13 | 0.23 |
| Q12 | acid_dissociation_fraction | 0.004 | 0 | 0.035 |
| Q12 | precipitation_signal | 0 | 0 | 0.016 |

### Q rationales

- **Q01**: This concentration is about 300-fold below the lowest completed batch. I therefore replace the observed-range log-linear pH interpolation with a weak-acid low-concentration continuation toward neutral water. Precipitation should be negligible. The dissociation fraction may rise upon dilution, but its public channel was unresolved in K1, so its interval is deliberately broad.

- **Q02**: This remains far below the observed 0.125–1.0 M domain. A weak-acid dilution continuation predicts higher normalized pH than any K1 batch, with no credible precipitation. The dissociation-fraction estimate is only a cautious upward departure from the near-zero K1 assays.

- **Q03**: At 0.025 M this is still a downward concentration extrapolation. The pH estimate uses the low-loading weak-acid continuation anchored at batch 1. The predicted precipitation proxy is zero because every clearly positive K1 precipitation response occurred at much higher concentration.

- **Q04**: The concentration exactly matches batch 1, whose final values were 0.141503 normalized pH, zero dissociation fraction, and 0.001079 precipitation. The new batch has a different scale and omits the fixed Catalyst A used in K1, so the point follows batch 1 but the intervals are substantially wider than assay noise alone.

- **Q05**: Batches 4 and 10 bracket this concentration directly and gave normalized pH values 0.102277 and 0.097459, with both precipitation estimates at zero. Their agreement supports a concentration-based point near 0.100. Uncertainty is enlarged because this catalyst-free 0.024 L scale was not tested.

- **Q06**: This is a modest concentration extrapolation beyond the 1.0 M endpoint in batch 8. Continuing the observed high-loading trends gives slightly lower normalized pH and a precipitation proxy above 0.060779. The interval is wide because the proxy may saturate or change slope and because no catalyst-free high-concentration batch was observed.

- **Q07**: The concentration matches Q05 and K1 batches 4 and 10, so concentration scaling gives the same central pH and near-zero precipitation. The 0.006 L scale is far below the K1 volume range, making scale, surface, and omitted-formulation effects especially uncertain.

- **Q08**: This concentration lies between batches 1 and 12 and is close to their dilute, effectively nonprecipitating regime. A weak-acid interpolation gives normalized pH near 0.136. Any association-sensitive response is not resolved strongly enough to justify a positive precipitation point much above the clipping floor.

- **Q09**: This is below the measured concentration range but not at the extreme asymptote. Dilution should raise normalized pH and suppress precipitation. The unresolved dissociation channel receives a slightly positive point and an asymmetric interval allowing a dilution-induced increase.

- **Q10**: At 0.04 M, the weak-acid continuation predicts a normalized pH above the observed batch-1 value and negligible precipitation. Greater dilution could increase the free dissociation fraction, but K1 did not resolve that channel, so the estimate remains conservative.

- **Q11**: This shares the 0.025 M concentration of Q03, so the concentration-controlled account gives the same central prediction. Its smaller 0.012 L scale is outside K1 coverage and warrants broader intervals, especially because the K1 catalyst amount was fixed in moles rather than concentration.

- **Q12**: This is the large-scale control at the same 0.025 M concentration as Q03 and Q11. K1 concentration-matched pairs favored concentration over absolute amount or volume, so the point estimates are shared. The volume lies inside the K1 range, giving a narrower interval than Q11, although the catalyst omission remains untested.

Shared rationale:

The central pH predictions use two regimes from the sealed K1 account. Within and just above the observed 0.125–1.0 M range, they follow the measured concentration response, including the approximately 0.100 result at 0.5 M and the high-loading continuation beyond batch 8. Below 0.125 M, where the empirical logarithmic fit was explicitly not validated, they use a weak-acid dilution continuation anchored to batch 1 and tending toward neutral water rather than extending the K1 regression without limit. Precipitation points follow the K1 low-signal regime below roughly 0.5–0.6 M and the rising high-loading branch observed in batches 6–8. The free acid-dissociation channel remained below useful final-assay resolution in K1, so its points stay conservative while its intervals allow dilution-dependent increases. All queries omit the 0.003 mol Catalyst A used in every K1 batch. Because K1 had no catalyst-free control and did not establish whether Catalyst A supplied the formal precipitating component or merely altered activities, this is a genuine formulation extrapolation and is a major source of prediction uncertainty. Intervals combine that model uncertainty, concentration or scale extrapolation, proxy clipping, and final-assay observation noise; they do not use equilibrium_confidence as uncertainty.

## K2 — sealed seven-part retrospective

1. Supplied structural claims

No instance-specific property or parameter dossier was supplied: the material record had dossier = null, with no prior values for Ka, Ksp, activities, or sensor calibration. A separate qualitative structural prior proposed HA(aq) ⇌ H+(aq) + A−(aq), direct M+(aq) + A−(aq) ⇌ MA(s), and no distinct aqueous MA intermediate.

The acid-response claim was qualitatively supported. In the fixed-volume series, normalized pH fell from 0.141503 in batch 1 at 0.125 M to 0.068364 in batch 8 at 1.0 M. The concentration-control claim was also supported locally: batches 6 and 9 both represented 0.75 M despite different amounts and volumes, and returned normalized pH values of 0.082865 and 0.081689 and precipitation signals of 0.041116 and 0.040013.

A precipitation branch was supported as a parsimonious effective description. The final precipitation signal increased from essentially zero at low loading to 0.041116 in batch 6, 0.048383 in batch 7, and 0.060779 in batch 8. This supports concentration-coupled formation of a solid or solid-like state, but it does not establish its molecular identity.

The claim that precipitation is direct, with no aqueous MA intermediate, was untested rather than confirmed. None of the public channels was species-resolved in a way that could distinguish direct ion capture from a rapidly equilibrating soluble complex. Likewise, the promised coherent three-channel response was only partly supported: pH and precipitation behaved systematically, whereas every final acid-dissociation estimate was between 0 and 0.002699, below the final-assay uncertainty of 0.006.

There was no clear observed contradiction to the two-equilibrium topology that was knowingly ignored. The irregular dissociation channel and low-level precipitation nonmonotonicity—such as batch 3 giving 0.010256 while batch 4 was clipped to zero—were treated as unresolved near-noise behavior rather than silently overridden. The K1 account was explicitly revised to say that only two channels were informative and that absence of aqueous MA remained untested.

2. Experiments and assumptions that formed the account

Batch 1 established the dilute observed endpoint: normalized pH 0.141503 with precipitation 0.001079. Batches 2–5 established a smooth pH decline but did not yet require a precipitation branch because their precipitation estimates were absent or small and irregular.

Batches 6–8 materially changed the account. At 0.75–1.0 M, precipitation rose reproducibly from 0.041116 to 0.060779 while normalized pH continued to fall. Those observations made a coupled precipitation equilibrium more credible than an acid-only description. Batch 8 was sealed as the evidentiary anchor because it fixed the high-loading, low-pH, positive-precipitation endpoint—not because it was operationally optimal.

Batches 9–12 tested dilution and scale. Batch 9 closely reproduced batch 6 at 0.75 M despite using 0.015 mol in 0.020 L rather than 0.030 mol in 0.040 L. The 0.5 M comparison between batches 4 and 10 and the 0.25 M comparison between batches 2 and 11 were less exact but still supported nominal concentration as the principal public coordinate.

The decision to examine a concentration series was consistent with both the research objective and the qualitative prior. The later interpretation of concentration collapse relied on accumulated observations, especially batches 6/9. By contrast, adding 0.003 mol of Catalyst A to every batch relied on an untested design assumption. No dossier established that Catalyst A was required, inert, or identical to the formal M+ source. Because there was no catalyst-free control, the K1 account correctly left that mapping unidentified.

The initial temptation to interpret positive in-process dissociation estimates was rejected after comparison with the final assays. For example, batch 1 produced an in-process fraction of 0.029880 but a final estimate of zero; batch 5 changed from 0.029206 to 0.000688. This caused the dissociation channel to be downgraded rather than fitted aggressively.

3. Strongest competing explanations

The strongest competing network is

HA ⇌ H+ + A−,
M+ + A− ⇌ MA(aq),
MA(aq) ⇌ MA(s).

If soluble MA is short-lived, low in abundance, or spectrally unassigned, this network can generate the same public pH and precipitation responses as direct M+ + A− ⇌ MA(s). The evidence cannot discriminate those topologies.

An equally important parameter-only alternative retains the direct topology but changes Ka, Ksp, activity coefficients, background-ion concentrations, and the bounded proxy map from solid amount or supersaturation to precipitation_signal. Such refitting can move the apparent crossover and pH curve without changing any reaction edge. K1 did not identify these constants separately.

A nonmechanistic common-cause explanation also remains viable: normalized pH and precipitation_signal may each be empirical functions of analytical concentration, without precipitation measurably controlling proton activity. The concentration-matched pairs distinguish concentration control from a simple total-mole explanation, but they do not establish causal coupling, solid stoichiometry, the identity of M+, or the absence of aggregation and ion pairing.

4. One additional complete experiment

I would run one catalyst-free 0.75 M aqueous batch: add 0.040 L water and 0.030 mol reagent, add no catalyst, acquire one in-process pH-meter measurement, terminate, and acquire the required final assay. This exactly matches the nominal concentration, reagent amount, and volume of batch 6 while changing the most consequential untested factor.

If it reproduced batch 6—approximately 0.082865 normalized pH and 0.041116 precipitation—the account would shift toward an intrinsic reagent/background-ion equilibrium in which Catalyst A is unnecessary over this local range. It would also strengthen the use of concentration-only interpolation for the blind catalyst-free queries.

If pH remained near batch 6 but precipitation collapsed toward zero, Catalyst A would become a plausible source or enabler of the precipitating component, and the acid and precipitation channels would need to be treated as partly separable.

If both pH and precipitation shifted substantially, Catalyst A would likely alter activities or coupled speciation, making the entire K1 response formulation-specific. If the final dissociation fraction also rose above its 0.006 assay uncertainty, the earlier near-zero values could no longer be treated simply as a universal property of the reagent system.

Even this experiment would not, by itself, distinguish direct precipitation from an aqueous-MA pathway; species-resolved evidence would still be required.

5. Effect of the characterization objective

The objective favored coverage of loading and dilution over process-score improvement. Eight batches mapped 0.125–1.0 M at fixed volume, and four added dilution or concentration-scale contrasts. This created broad local structure and three useful matched-concentration comparisons, but it left no exact recipe replicate and no catalyst-free, solvent, temperature, or time control.

That trade-off improved qualitative identification of concentration dependence and the precipitation crossover but weakened repeatability estimates and parameter identification. One in-process measurement per batch was retained to compare channels, although the final assay was the primary endpoint. The scalar score was treated as a diagnostic rather than an objective: no batch was selected because it improved score, and no unfavorable endpoint was replaced. Batch 8 was selected solely as a mechanistically informative boundary anchor.

6. Underused evidence and least reliable predictions

The in-process pH-meter data were underused quantitatively. Their pH values broadly supported the final trend, but their much noisier dissociation estimates could have been analyzed more formally as cross-instrument disagreement. The final spectral artifacts were also underused because the public mapping did not authorize molecular assignments. Small equilibrium residuals were reported but intentionally not converted into confidence in the topology, and equilibrium_confidence was correctly excluded from epistemic uncertainty.

The matched-concentration pairs could have supported a formal hierarchical estimate of volume effects, but three pairs were insufficient to separate volume, catalyst concentration, sampling, and ordinary process variation. Raw low-level precipitation differences likewise did not justify a precise threshold fit.

The least reliable sealed blind predictions are Q01 and Q02, which extrapolate roughly 300-fold and 30-fold below the lowest observed concentration; Q06, which exceeds the 1.0 M upper boundary; and Q07, whose 0.006 L volume is far below the 0.020–0.080 L K1 range. Q11 is also a scale extrapolation at 0.012 L. Q03, Q09, Q10, Q11, and Q12 all lie below the observed concentration range. Their weak-acid low-concentration continuation was therefore conjectural rather than a K1 interpolation.

All 12 predictions are additionally formulation extrapolations because they omit Catalyst A, whereas every K1 batch contained 0.003 mol. Q04 and Q05 have the best concentration anchors—batch 1 for 0.125 M and batches 4/10 for 0.5 M—but even they lack catalyst-free support. The acid-dissociation predictions and their 80% intervals are the least identified metric-wise because K1 never resolved that channel. Broad intervals in the sealed Q response acknowledged these problems, but they cannot substitute for missing controls.

7. Limits of the anchor, repeatability, robustness, and generalization

Batch 8 is a single high-loading observation, not a replicate and not a proven optimum. It anchors normalized pH 0.068364 and precipitation 0.060779 at 1.0 M for one water/Catalyst-A formulation and one operation sequence. It cannot alone establish saturation behavior, threshold location, long-term equilibration, or reproducibility.

Repeatability is supported only indirectly. Batches 6 and 9 gave close results at 0.75 M, but they intentionally differed in amount and volume; they are concentration controls, not exact replicates. Batches 4/10 and 2/11 likewise demonstrate approximate local robustness while leaving small differences that could arise from scale, catalyst concentration, or noise.

The strongest local generalization is therefore limited to water, Catalyst A at 0.003 mol per vessel, about 297.2 K, analytical concentrations of 0.125–1.0 M, and volumes of 0.020–0.080 L. Within that domain, decreasing normalized pH and rising high-loading precipitation are robust qualitative findings. Generalization to catalyst-free batches, other catalyst identities or amounts, other solvents, temperatures, equilibration times, ionic backgrounds, much smaller volumes, or concentrations outside the measured interval is unsupported or extrapolative.

Finally, this is a bounded synthetic world. The anonymous roles and calibrated public proxies do not establish identities or laws for real aqueous chemistry, and the inferred network should not be transferred to another world without new evidence.

## EQS — sealed structured mechanism supplement

- Network family: `indeterminate`
- Aqueous intermediate: `indeterminate`
- Selected equations: `acid_dissociation, free_ion_solid_equilibrium`
- Cited source batches: `1, 6, 8, 9`
- Rationale: Acid dissociation and a free-ion/solid equilibrium are the common parsimonious account: normalized pH decreased from batch 1 to batch 8, while batches 6 and 8 showed clear positive precipitation signals. Batches 6 and 9 also produced closely matched pH and precipitation responses at the same analytical concentration despite different scales. However, no species-resolved source evidence distinguished direct precipitation from rapid formation of an aqueous MA ion pair followed by solid formation. The aqueous intermediate is therefore indeterminate rather than demonstrated absent or present.

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean width | Interval score |
|---|---:|---:|---:|---:|
| pH_normalized | 0.0191603 | 1 | 0.1025 | 0.1025 |
| acid_dissociation_fraction | 0.0157658 | 0.916667 | 0.0358333 | 0.0583266 |
| precipitation_signal | 0.00218232 | 1 | 0.03125 | 0.03125 |

## Structural evaluation

Truth family: `aqueous_ion_pair_intermediate`; predicted family: `indeterminate`; abstained: `True`; family correct: `False`; exact equation set correct: `False`; equation-set Jaccard: `0.666667`.

## Response-shape evaluation

Concentration slope MAE `0.0160158` and curvature MAE `0.0153245`. Dilution slope MAE `0.0148009` and curvature MAE `0.0144209`.

## Evidence boundary

K1 was sealed before Q, Q before K2, K2 before EQS, and reference truth was generated only after all 15 EQS responses were sealed. The task is characterization rather than optimization. Numerical residual and equilibrium confidence are environment diagnostics, not agent uncertainty or task scores. Private authentication and raw model process material are excluded.
