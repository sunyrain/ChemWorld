# EQ-S-W04--Aligned — final English experiment report

World `EQ-S-W04`; information arm `Aligned`; task `mechanism characterization`; effective status `completed`; result origin `original`.

## Source campaign

The autonomous campaign completed 12/12 batches and 84 recorded operations. Exact replay is `True`; rollbacks: 0.

| Batch | Solvent L | Reagent mol | Measurements | pH normalized | Free dissociation | Precipitation signal | Residual |
|---:|---:|---:|---|---:|---:|---:|---:|
| 1 | 0.04 | 0.005 | ph_meter, final_assay | 0.1493 | 0.00290827 | 0 | 0 |
| 2 | 0.04 | 0.015 | ph_meter, final_assay | 0.12095 | 0 | 0 | 0.000887705 |
| 3 | 0.04 | 0.025 | ph_meter, final_assay | 0.100504 | 0 | 0 | 0 |
| 4 | 0.04 | 0.035 | ph_meter, final_assay | 0.0876586 | 0 | 0.0158974 | 0 |
| 5 | 0.06 | 0.005 | ph_meter, final_assay | 0.161309 | 0 | 0 | 0.0123986 |
| 6 | 0.06 | 0.015 | ph_meter, final_assay | 0.131314 | 0.0142926 | 0 | 5.51714e-05 |
| 7 | 0.06 | 0.025 | ph_meter, final_assay | 0.113623 | 0.00807231 | 0 | 0 |
| 8 | 0.06 | 0.035 | ph_meter, final_assay | 0.0984908 | 0 | 0 | 0 |
| 9 | 0.08 | 0.005 | ph_meter, final_assay | 0.169118 | 0.00227418 | 0.00227143 | 0.00464175 |
| 10 | 0.08 | 0.015 | ph_meter, final_assay | 0.137684 | 0.00778388 | 0 | 0 |
| 11 | 0.08 | 0.025 | ph_meter, final_assay | 0.121804 | 0 | 0.0049081 | 0.000695585 |
| 12 | 0.08 | 0.035 | ph_meter, final_assay | 0.110491 | 0.00589335 | 0 | 0 |

### Sealed evidentiary anchor

Batch `4`: Selected as the high-loading, low-volume boundary condition; it anchors the observed pH response and the clearest nonzero final precipitation proxy in the concentration series, without implying optimality.

## K1 — sealed mechanistic report

MECHANISTIC REPORT

1. Scope and evidence

The campaign comprised 12 completed aqueous batches. Every batch used water, anonymous reagent, Catalyst A, 600 s of waiting at 400 rpm, an intermediate pH-meter measurement, termination, and a final assay. Reagent loading covered 0.005–0.035 mol and nominal water volume covered 0.040–0.080 L, corresponding to nominal reagent concentrations C_T = n_reagent/V of 0.0625–0.875 mol L^-1. Catalyst A was 0.002 mol in batches 1–11. In batch 12 it was increased to 0.005 mol; consequently, that corner is not a clean continuation of the loading–dilution grid.

The final-assay observations were:

Batch | reagent (mol) | water (L) | C_T (mol L^-1) | normalized pH | free acid-dissociation fraction | precipitation proxy
1 | 0.005 | 0.040 | 0.1250 | 0.149300 | 0.002908 | 0
2 | 0.015 | 0.040 | 0.3750 | 0.120950 | 0 | 0
3 | 0.025 | 0.040 | 0.6250 | 0.100504 | 0 | 0
4 | 0.035 | 0.040 | 0.8750 | 0.087659 | 0 | 0.015897
5 | 0.005 | 0.060 | 0.08333 | 0.161309 | 0 | 0
6 | 0.015 | 0.060 | 0.2500 | 0.131314 | 0.014293 | 0
7 | 0.025 | 0.060 | 0.41667 | 0.113623 | 0.008072 | 0
8 | 0.035 | 0.060 | 0.58333 | 0.098491 | 0 | 0
9 | 0.005 | 0.080 | 0.0625 | 0.169119 | 0.002274 | 0.002271
10 | 0.015 | 0.080 | 0.1875 | 0.137684 | 0.007784 | 0
11 | 0.025 | 0.080 | 0.3125 | 0.121804 | 0 | 0.004908
12 | 0.035 | 0.080 | 0.4375 | 0.110491 | 0.005893 | 0

The final-assay standard deviations declared for normalized pH, dissociation fraction, and precipitation proxy were respectively 0.002, 0.006, and 0.006. Exact zeros in the last two channels should therefore be treated as bounded or clipped near-floor estimates, not proof of exact chemical absence.

2. Direct observations

The strongest observation is a reproducible concentration-controlled pH response. At every fixed reagent amount, dilution raised normalized pH:

• 0.005 mol: 0.149300 in batch 1, 0.161309 in batch 5, and 0.169119 in batch 9 as water increased from 0.040 to 0.080 L.
• 0.015 mol: 0.120950 in batch 2, 0.131314 in batch 6, and 0.137684 in batch 10.
• 0.025 mol: 0.100504 in batch 3, 0.113623 in batch 7, and 0.121804 in batch 11.
• 0.035 mol: 0.087659 in batch 4, 0.098491 in batch 8, and 0.110491 in batch 12, although batch 12 also changed catalyst amount.

Conversely, at each fixed volume, greater reagent loading lowered normalized pH. Thus loading and dilution act predominantly through their ratio, the analytical concentration, rather than as unrelated effects of total moles and volume.

For the common-catalyst batches 1–11, a descriptive least-squares relation is

pH_normalized ≈ 0.08592 - 0.03068 ln(C_T/[1 mol L^-1])

or, in conventional pH units,

pH ≈ 1.203 - 0.989 log10(C_T/[1 mol L^-1]).

Its normalized-pH root-mean-square residual is about 0.00232, close to the declared final-assay noise of 0.002. This is an empirical summary within the tested domain, not an independently established equilibrium law. It corresponds approximately to [H+] ≈ 0.0627 C_T^0.989 if activities are provisionally replaced by concentrations. Across the measured range, normalized pH ran from 0.087659 to 0.169119, equivalent to pH 1.227–2.368 and nominal [H+] of about 0.0593–0.00429 mol L^-1.

The acid-dissociation-fraction channel did not show an identifiable monotonic loading or dilution trend. Its 12-batch mean was approximately 0.00344; seven final values were exactly zero and the maximum, 0.014293 in batch 6, was only about 2.4 declared standard deviations above zero. For example, the fraction was zero in concentrated batch 4, 0.014293 in batch 6, 0.008072 in batch 7, zero again in batch 8, and 0.002274 in the most dilute batch 9. This pattern is more consistent with a very small true signal observed near a nonnegative floor than with a resolved concentration law.

The precipitation proxy was likewise largely at its floor. Nine of 12 final assays were exactly zero. The nonzero results were batch 4, 0.015897; batch 9, 0.002271; and batch 11, 0.004908. Only batch 4 was clearly more than two final-assay standard deviations above zero. There was no replicated high signal and no monotonic trend across loading or dilution.

Intermediate measurements reinforce the need for caution about the two near-floor channels. In batch 1, the pH meter reported precipitation proxy 0.024495, whereas the final assay reported zero. Batch 7 changed from 0.008519 to zero, batch 9 from 0.037652 to 0.002271, and batch 11 from 0.018949 to 0.004908. These differences are compatible with the pH meter’s larger declared precipitation noise of 0.020. By contrast, normalized pH was much more reproducible: batch 1 gave 0.150071 by pH meter and 0.149300 by final assay, while batch 7 gave 0.112633 and 0.113623.

Equilibrium residuals were zero or small in final assays: zero in many batches, 0.000888 in batch 2, 0.012399 in batch 5, 0.004642 in batch 9, and 0.000696 in batch 11. This indicates numerical or environmental consistency but does not identify a chemical topology. Likewise, equilibrium_confidence is an environment diagnostic and is not used here as scientific confidence or as evidence for a mechanism.

3. Plausible common equilibrium network

The supplied structural account proposed:

HA(aq) ⇌ H+(aq) + A−(aq)
M+(aq) + A−(aq) ⇌ MA(aq)
M+(aq) + A−(aq) ⇌ MA(s).

This is a chemically coherent single-network explanation for all three public channels. The acid equilibrium controls hydrogen activity and the pool of free A−. Association removes A− into dissolved MA. If the free-ion product crosses a solubility boundary, solid MA forms and produces the precipitation response.

A useful equilibrium representation is

K_a = a_H a_A/a_HA,
β_MA = a_MA/(a_M a_A),
K_sp = a_M a_A at saturation,
pH_normalized = -log10(a_H)/14.

Let n_A,T denote total introduced acid-family material and n_M,T total introduced metal-family material. A complete acid-family balance would be

n_A,T = V([HA] + [A−] + [MA]_aq) + n_MA,s,

while the dissolved balance stated in the supplied account is

n_HA + n_A− + n_MA,aq.

The metal-family balance would be

n_M,T = V([M+] + [MA]_aq) + n_MA,s.

A charge balance would include H+, M+, A−, OH−, and any unobserved counterions supplied with the anonymous formulations. Because those counterions and activities were not measured, a numerical charge-balance reconstruction is not possible. The public precipitation signal is only a bounded proxy, so no conversion from its value to n_MA,s is justified.

Within this network, dilution changes several coupled quantities simultaneously. It lowers analytical acid and metal concentrations, changes the acid dissociation ratio through K_a, changes association through β_MA[M+][A−], and changes the ion product a_Ma_A relative to K_sp. Consequently, one network can in principle generate the pH curve, a small free-dissociation fraction, and a threshold-like precipitation channel.

4. What the experiments support about topology

The pH series strongly supports an acid-generating aqueous process whose dominant control variable is reagent concentration. It is compatible with the proposed HA ⇌ H+ + A− step. The nearly unit negative slope of pH against log10(C_T) is closer to a constant effective proton yield than to the textbook infinite-dilution square-root law for an isolated weak acid. That difference need not falsify the acid step: activities, formulation counterions, association, and the anonymous meaning of the reagent can all alter the apparent law. It does mean that a simple ideal weak-acid formula should not be claimed from these data.

The evidence does not uniquely support a distinct dissolved MA intermediate. No instrument reported [MA]_aq, free [M+], free [A−], or a species-specific spectrum that could distinguish MA(aq) from other sequestration. A direct precipitation topology,

M+ + A− ⇌ MA(s),

could reproduce the observed channels without a distinct aqueous intermediate. Conversely, a dissolved ion pair with essentially no solid over this domain could also reproduce them.

The evidence for the solid branch is weak. Batch 4—the sealed evidentiary anchor—was the highest-concentration common-catalyst condition and produced the clearest nonzero final precipitation proxy, 0.015897. That is qualitatively consistent with an ion-product threshold. However, batches 8 and 12 had substantial nominal concentrations and zero final proxy, while dilute batch 9 and intermediate batch 11 had small nonzero values. Intermediate-to-final discrepancies further show that much of the apparent precipitation variation is measurement noise. Thus batch 4 is a useful boundary observation, not proof of a precipitation law.

After predominantly zero precipitation results in batches 1–11, batch 12 used 0.005 mol rather than 0.002 mol Catalyst A to probe whether more of the catalyst-associated component would reveal the branch. Its final precipitation proxy remained zero. This revised the account away from any simple claim that increasing Catalyst A necessarily increases precipitation. The test is nevertheless confounded: batch 12 simultaneously occupied a new reagent/volume condition, and the chemical role of Catalyst A is opaque. It cannot estimate a catalyst coefficient or falsify every metal-coupled precipitation model.

5. One network versus three unrelated response models

A single equilibrium network is sufficient to explain the qualitative meanings of all three response channels: proton production gives pH, speciation gives the free dissociation fraction, and the same free A− pool participates in an ion product that can generate precipitation. The observations do not contradict that joint account because the latter two channels are mostly below their effective resolution.

Sufficiency is not identification. The experiment strongly constrains only the pH surface. It does not demonstrate that changes in the measured fraction or precipitation proxy covary with the pH according to shared fitted constants. Therefore the defensible topology claim is limited to “an acid-producing aqueous equilibrium, possibly coupled to association and precipitation.” It is not defensible to claim that the distinct MA(aq) node or the solid edge has been uniquely recovered.

Changing K_a, β_MA, K_sp, activity coefficients, proxy scaling, or effective component inventories while retaining the same three-edge topology is parameter refitting. Such refitting could move the precipitation threshold or keep the dissociation channel near zero, but it would not test whether MA(aq) exists as a distinct node. A topology test would require observations that discriminate the three-edge graph from alternatives—for example, species-specific evidence for MA(aq), independent metal loading at fixed acid concentration, or reversible appearance of solid at a predicted ion-product boundary. Those observations were not obtained.

6. Status of the supplied dossier and priors

No task-specific nominal property dossier was supplied: the material information explicitly reported dossier = null. No instance prior was supplied: prior_record was null. Therefore no numerical prior constants, solubility limit, pK_a, or prior response surface were available to confirm or refit.

A structural initial-world-model account was supplied separately from an instance prior. Its HA dissociation step is supported qualitatively by the systematic pH response. Its proposal that dissolved MA is a distinct intermediate remains untested and unidentifiable. Its solid MA branch receives only weak qualitative support from batch 4 and is not established by the campaign. Its stated dissolved acid-family balance is chemically consistent, but the necessary species amounts were not observed, so the balance was not quantitatively verified. The dossier should therefore be revised from a relatively specific three-edge mechanism to a partially supported family: a well-supported acid-producing concentration response plus unresolved association and precipitation branches.

7. Supported interpolation

Interpolation is supported only for water, Catalyst A, the stated preparation and 600 s wait, reagent amounts of 0.005–0.035 mol, volumes of 0.040–0.080 L, and nominal concentrations of 0.0625–0.875 mol L^-1. Within that rectangle, the empirical log-concentration relation is a defensible interpolator for normalized pH, with an observed residual scale around 0.0023.

Interpolation of the dissociation fraction should instead be reported as “near the nonnegative detection floor,” not as the irregular individual values. Interpolation of precipitation should be conservative: the proxy was generally zero or very small, with one isolated value of 0.015897 at the high-concentration boundary. A sharp threshold location cannot be inferred.

8. Extrapolation

No quantitative extrapolation is supported outside the tested loading, volume, solvent, catalyst identity, catalyst amount, temperature, mixing, or 600 s equilibration conditions. In particular, the empirical pH equation should not be extended toward infinite dilution, beyond 0.875 mol L^-1, or to nonaqueous solvents. The campaign does not establish whether precipitation rises above the tested concentration range, redissolves under other conditions, or changes with longer waiting. It also does not justify predictions for Catalysts B–D.

9. Conjectures and competing explanations

The preferred conjecture is the supplied coupled network with acid dissociation, reversible aqueous association, and a precipitation boundary. It is parsimonious because one A-containing pool links all three channels, but the association and solid nodes remain provisional.

Reasonable competitors are:

• An acid-only model plus measurement-floor precipitation noise. This explains the strong pH curve and the lack of reproducible precipitation without invoking MA(aq) or MA(s).
• Direct precipitation without a distinct aqueous MA intermediate. This has the same observable acid and solid endpoints but a different topology.
• A buffered or counterion-controlled formulation in which proton activity is approximately proportional to reagent concentration, while the reported dissociation fraction measures a different small free-species pool. This would explain the near-unit pH/log-concentration slope and the apparent mismatch between substantial [H+] and a near-zero public fraction.
• Concentration-dependent activity coefficients or ion pairing that deform an otherwise ordinary weak-acid equilibrium. These effects are observationally equivalent to changing effective K_a over this limited range.
• A kinetic or particulate-detection explanation for the precipitation proxy. The inconsistent intermediate and final values could arise from noisy detection of transient or heterogeneous material rather than a stable equilibrium solid.

10. Overall conclusion

This world exhibits a clear, concentration-dominated aqueous acidity response: more reagent or less water lowers normalized pH, and a single log-concentration curve describes batches 1–11 to approximately the assay-noise scale. A shared acid/association/precipitation network can explain all three public channels, and the supplied HA dissociation step is qualitatively supported. However, the free-dissociation and precipitation channels remained mostly at their measurement floors. The campaign therefore does not identify a distinct aqueous MA intermediate, a numerical solubility product, or even a uniquely necessary solid branch. Batch 4 supplies a useful high-concentration precipitation hint, while batch 12 and the intermediate/final discrepancies prevent a strong monotonic precipitation claim. The defensible result is a constrained mechanism family, not a uniquely fitted reaction graph.

## Q — sealed blind predictions

| Query | Metric | Estimate | 80% lower | 80% upper |
|---|---|---:|---:|---:|
| Q01 | pH_normalized | 0.325 | 0.27 | 0.38 |
| Q01 | acid_dissociation_fraction | 0.088 | 0.02 | 0.2 |
| Q01 | precipitation_signal | 0.001 | 0 | 0.012 |
| Q02 | pH_normalized | 0.254 | 0.22 | 0.29 |
| Q02 | acid_dissociation_fraction | 0.029 | 0.005 | 0.075 |
| Q02 | precipitation_signal | 0.001 | 0 | 0.012 |
| Q03 | pH_normalized | 0.199 | 0.17 | 0.23 |
| Q03 | acid_dissociation_fraction | 0.012 | 0 | 0.035 |
| Q03 | precipitation_signal | 0.001 | 0 | 0.013 |
| Q04 | pH_normalized | 0.15 | 0.135 | 0.165 |
| Q04 | acid_dissociation_fraction | 0.0053 | 0 | 0.02 |
| Q04 | precipitation_signal | 0.0015 | 0 | 0.015 |
| Q05 | pH_normalized | 0.107 | 0.092 | 0.122 |
| Q05 | acid_dissociation_fraction | 0.0026 | 0 | 0.015 |
| Q05 | precipitation_signal | 0.003 | 0 | 0.02 |
| Q06 | pH_normalized | 0.079 | 0.055 | 0.102 |
| Q06 | acid_dissociation_fraction | 0.0017 | 0 | 0.015 |
| Q06 | precipitation_signal | 0.01 | 0 | 0.04 |
| Q07 | pH_normalized | 0.107 | 0.08 | 0.135 |
| Q07 | acid_dissociation_fraction | 0.0026 | 0 | 0.025 |
| Q07 | precipitation_signal | 0.003 | 0 | 0.025 |
| Q08 | pH_normalized | 0.141 | 0.126 | 0.156 |
| Q08 | acid_dissociation_fraction | 0.0046 | 0 | 0.02 |
| Q08 | precipitation_signal | 0.002 | 0 | 0.016 |
| Q09 | pH_normalized | 0.171 | 0.158 | 0.184 |
| Q09 | acid_dissociation_fraction | 0.0075 | 0 | 0.026 |
| Q09 | precipitation_signal | 0.001 | 0 | 0.013 |
| Q10 | pH_normalized | 0.185 | 0.17 | 0.199 |
| Q10 | acid_dissociation_fraction | 0.0093 | 0 | 0.03 |
| Q10 | precipitation_signal | 0.001 | 0 | 0.013 |
| Q11 | pH_normalized | 0.199 | 0.165 | 0.235 |
| Q11 | acid_dissociation_fraction | 0.012 | 0 | 0.05 |
| Q11 | precipitation_signal | 0.001 | 0 | 0.016 |
| Q12 | pH_normalized | 0.199 | 0.181 | 0.216 |
| Q12 | acid_dissociation_fraction | 0.012 | 0 | 0.035 |
| Q12 | precipitation_signal | 0.001 | 0 | 0.013 |

### Q rationales

- **Q01**: This concentration is about 150-fold below the lowest studied concentration, so the pH estimate is a long extrapolation of the observed log-concentration relation. A weak-acid dilution asymptote could raise the free dissociation fraction substantially. With no added Catalyst A and extremely low ion loading, precipitation should remain at the measurement floor.

- **Q02**: The concentration remains well below the experimental range, but less extremely than Q01. The fitted acidity relation predicts normalized pH near 0.254, while weak-acid speciation suggests a larger free fraction than in the completed batches. Precipitation is unlikely without added Catalyst A at this dilute condition.

- **Q03**: At 0.025 M this is a moderate extrapolation below the studied range and also a scale-control condition. Concentration-based acidity predicts normalized pH near 0.199. The dissociation estimate follows the plausible weak-acid dilution trend, but its interval is broad because the measured fraction was unresolved near zero and this batch omits Catalyst A.

- **Q04**: The analytical concentration exactly matches batch 1, whose final normalized pH was 0.149300, so the acidity prediction is anchored despite the smaller absolute scale. Batch 1 had a near-floor dissociation fraction and zero final precipitation. Omission of Catalyst A prevents an exact recipe match and is reflected in the intervals.

- **Q05**: A concentration of 0.5 M lies within the studied concentration range, where the empirical pH curve is well supported. The free-fraction signal should remain close to its lower bound. A small precipitation response is possible at this loading, but the absence of Catalyst A and the lack of a reproducible precipitation trend make zero entirely plausible.

- **Q06**: This is the only query above the studied upper concentration of 0.875 M. Log-concentration extrapolation predicts normalized pH near 0.079. High concentration raises the possibility of crossing an association or precipitation boundary, but batch 4 supplied only one weak positive precipitation observation and the present recipe has no Catalyst A, so both model and observation uncertainty are large.

- **Q07**: The concentration matches Q05, so a concentration-controlled model gives the same central predictions. However, the 0.006 L scale is far below the studied volumes, making this a strong test of whether concentration alone is sufficient. Wider intervals allow for absolute-scale, mixing, and omitted-catalyst effects.

- **Q08**: At 0.1667 M, the predicted pH is interpolated between the low-loading campaign conditions, although the volume is below the studied range. The dissociation fraction is expected to remain small. This condition is below the only persuasive precipitation hint, so a floor-level proxy is most likely.

- **Q09**: The concentration exactly matches batch 9, whose final normalized pH was 0.169119, dissociation fraction was 0.002274, and precipitation proxy was 0.002271. The present batch has a different absolute scale and no Catalyst A, but the campaign’s concentration collapse supports a similar pH and a near-floor precipitation response.

- **Q10**: This concentration is modestly below the studied range, so the pH prediction is a short extrapolation toward greater dilution. Weak-acid reasoning permits a somewhat larger free fraction, although that channel was poorly resolved experimentally. The low ion loading and absence of Catalyst A favor negligible precipitation.

- **Q11**: The concentration matches Q03 and therefore receives the same central concentration-based prediction. Its smaller 0.012 L scale is farther from the completed experiments, so its intervals are wider. Any precipitation should remain close to zero, while the free-fraction prediction is particularly uncertain because the campaign did not identify that channel’s law.

- **Q12**: This large-scale control has the same 0.025 M concentration as Q03 and Q11, and its 0.072 L volume lies within the campaign’s volume range. It should therefore be the cleanest of the three scale controls for the concentration-only pH model. The other two channels are predicted near their lower bounds because no robust association or precipitation response was established.

Shared rationale:

The central pH predictions use the sealed K1 empirical relation pH_normalized = 0.08592 - 0.03068 ln(C/M), which summarized common-catalyst batches 1–11 with a residual near the final-assay noise. Intervals widen outside the studied concentration range of 0.0625–0.875 M, outside the studied volume range of 0.040–0.080 L, and because these new recipes omit Catalyst A and the 600 s wait used during research. Free acid-dissociation predictions use a cautious weak-acid dilution trend calibrated only to the campaign’s near-floor values; this is a conjectural extrapolation because K1 could not identify that channel’s constants. Precipitation is predicted near zero because nine of 12 final assays were zero, positive observations were small and inconsistent, and no Catalyst A is added here. A modest high-concentration increase is retained to represent the unresolved possibility of an ion-product threshold. All intervals combine final-assay noise with larger structural uncertainty; they do not use equilibrium_confidence as an uncertainty measure.

## K2 — sealed seven-part retrospective

1. Status of the supplied structural claims

No instance-specific numerical dossier was supplied: the material record had dossier = null, and no instance prior was supplied because prior_record was null. What was supplied was a qualitative structural proposal: HA(aq) ⇌ H+(aq) + A−(aq), a distinct dissolved association M+ + A− ⇌ MA(aq), and precipitation M+ + A− ⇌ MA(s), together with an acid-family balance.

The acid-producing step was supported qualitatively. In every fixed-volume series, increasing reagent lowered normalized pH, and in every fixed-loading series, dilution raised it. For example, at 0.005 mol reagent, normalized pH rose from 0.149300 in batch 1 to 0.161309 in batch 5 and 0.169119 in batch 9 as water increased. The batches with a common catalyst condition were summarized well by a log-concentration relation.

The distinct MA(aq) intermediate was untested rather than supported. No measurement identified MA(aq), free M+, or free A− separately. The proposed acid-family balance was chemically coherent but not quantitatively tested because its individual species inventories were unavailable.

The solid branch received only weak, non-replicated support. Batch 4, the highest-concentration common-catalyst condition, gave precipitation_signal = 0.015897, but nine of 12 final assays were zero and other nonzero values were small. This was not a decisive contradiction of precipitation, because a threshold could lie near or beyond the sampled domain and the signal was noisy. It did contradict any simple, strong monotonic claim that the sampled loading series necessarily produced progressively more precipitation.

Increasing Catalyst A from 0.002 mol to 0.005 mol in batch 12 did not produce precipitation_signal above zero. That observation argued against the simple claim “more Catalyst A necessarily gives more precipitate,” and the K1 account explicitly revised away from that claim. It did not falsify every metal-coupled topology because batch 12 also changed reagent concentration and volume relative to earlier batches.

There was also a structural tension that was recognized only in the sealed interpretation, not acted on during the campaign: the empirical conventional-pH slope was approximately −0.989 per decade of analytical concentration, whereas an isolated ideal weak acid would ordinarily show a different asymptotic dependence. K1 treated this as a warning against claiming a textbook weak-acid equation, not as decisive falsification of the HA step.

2. Experiments and choices that formed or changed the account

Batches 1–11 formed the main concentration account. Their reagent/volume grid established that analytical concentration was the leading predictor of pH. Batch 1 also showed good cross-instrument pH agreement—0.150071 by the intermediate meter and 0.149300 by final assay—while its precipitation proxy changed from 0.024495 to zero. That contrast helped separate the robust pH channel from the noisy precipitation channel.

Batches 4, 8, 9, and 11 shaped the precipitation judgment. Batch 4 supplied the clearest positive final value, 0.015897. However, batch 8 was zero at another high concentration, while dilute batch 9 and intermediate batch 11 gave only 0.002271 and 0.004908. The intermediate-to-final changes in batches 7, 9, and 11 further reduced confidence in treating small precipitation values as stable solids. In batch 9, for example, the proxy fell from 0.037652 at the intermediate measurement to 0.002271 at final assay.

Batch 12 was the explicit mechanism probe prompted by accumulated near-zero precipitation observations: Catalyst A was raised to 0.005 mol. Its zero final precipitation result changed the account by weakening a simple catalyst-dose explanation. Because that choice was made after earlier observations and was confounded with a new reagent/volume condition, it was correctly treated as exploratory rather than a clean causal test.

The dossier influenced the decision to include Catalyst A and to think in terms of an M/A association–precipitation branch. The specific assumption that Catalyst A operationalized the proposed M-containing component was never measured and remained untested. Using 0.002 mol Catalyst A in batches 1–11, using only water, and allowing 600 s at 400 rpm were design choices, not conclusions forced by the observations. The 4-by-3 loading/dilution coverage was chosen to identify concentration dependence rather than to maximize a process score. The late catalyst change sacrificed a fully uniform factorial corner for an exploratory branch probe.

3. Strongest competing explanation and identifiability

The strongest topology-level competitor is an acid-only aqueous model, HA ⇌ H+ + A−, with the precipitation channel dominated by a nonnegative measurement floor or occasional particulate noise. It explains the reproducible pH surface without requiring either MA(aq) or MA(s). A second strong competitor is direct precipitation, M+ + A− ⇌ MA(s), without a distinct dissolved MA intermediate.

A parameter-only alternative retains the supplied three-edge topology but changes effective K_a, the association constant, K_sp, activity coefficients, component inventories, and proxy calibration so that association and precipitation remain mostly below resolution. That is refitting constants inside one topology; it is not evidence that the distinct MA(aq) node exists.

The evidence can distinguish a robust concentration-dependent acidity response from the two poorly resolved channels. It cannot distinguish an aqueous MA intermediate from direct precipitation, establish which added material supplies M+, estimate a unique K_a or K_sp, or decide whether small precipitation signals represent stable solid, transient particles, or observation noise. Near-zero residual diagnostics do not resolve these alternatives.

4. One additional legal complete experiment

I would run a matched catalyst-omission version of batch 4: add 0.040 L water and 0.035 mol reagent, add no catalyst, wait 600 s at 400 rpm, measure once with the pH meter, terminate, and obtain the final assay. This retains batch 4’s 0.875 M analytical concentration and process history while changing the most uncertain mechanistic factor. I would measure normalized pH, acid_dissociation_fraction, precipitation_signal, and the residual channel, using the final assay as primary evidence and the intermediate measurement only as a repeatability check.

If precipitation fell reproducibly from batch 4’s 0.015897 to the floor while pH or free fraction shifted, that would support a catalyst-coupled M/A branch. If pH remained the same and precipitation remained near the floor, batch 4 would look more like a noisy isolated positive. If precipitation remained near 0.0159 without catalyst, Catalyst A would be unnecessary for that response, favoring an intrinsic reagent component, direct precipitation, or a proxy unrelated to the proposed M source. If precipitation increased without catalyst, inhibition or complexation by Catalyst A would become a serious alternative. One batch would still not provide replication, so every outcome would remain provisional.

5. Effect of the characterization objective on design trade-offs

The objective favored broad structural coverage over local precision. The campaign used loading and volume levels spanning 0.0625–0.875 M rather than repeating a few conditions. That choice strongly identified the pH concentration trend but left no true batch replication for the dissociation or precipitation channels.

Coverage also competed with topology identification. Holding Catalyst A fixed in batches 1–11 made the loading/dilution surface interpretable, but it did not independently vary the proposed M component. Changing the catalyst amount only in batch 12 created one exploratory contrast at the cost of a completely clean factorial grid.

No experiment was selected to improve the scalar operational score, and equilibrium_confidence was not treated as scientific confidence. The sealed anchor, batch 4, was chosen because it was an informative boundary condition with the clearest nonzero precipitation proxy, not because it was optimal. Cost, score, and operational desirability were subordinate to mechanistic coverage.

6. Underused evidence and weak blind predictions

The raw final-assay artifacts and their multichannel peak summaries were underused. K1 relied mainly on processed equilibrium metrics because the supplied peak assignments were generic proxies and did not identify MA(aq) or MA(s). Temperature, pressure, and the precise intermediate-to-final timing information were also not used to test equilibration. Intermediate pH-meter results were used qualitatively, but a formal paired instrument analysis was not performed.

The weakest blind predictions are Q01 and Q02. Their concentrations, 0.0004167 and 0.004167 M, were far below K1’s lower boundary of 0.0625 M. Their acid-fraction point estimates of 0.088 and 0.029 relied on a conjectural weak-acid dilution asymptote even though K1 explicitly said that the acid-fraction law was unidentified. Q06 was also weak because 1.25 M exceeded the upper boundary and its precipitation estimate of 0.010 assumed a possible threshold that K1 had not localized.

Q07 and Q11 were weak scale generalizations because their 0.006 and 0.012 L volumes were far below the studied 0.040–0.080 L range. The equal central predictions assigned to constant-concentration controls were a concentration-only hypothesis, not a demonstrated invariance. Q03 and Q12 were also below the studied concentration range at 0.025 M, although Q12’s volume lay within the studied volume range.

All 12 blind batches omitted Catalyst A and the 600 s wait used in K1. Consequently, even apparently anchored predictions such as Q04 at 0.125 M and Q09 at 0.0625 M were not exact recipe interpolations. Their pH estimates were more defensible than their fraction or precipitation estimates, but their intervals may still have been too narrow for this intervention change. The precipitation intervals were especially model-dependent because K1 had not established whether Catalyst A supplied the M-containing branch.

7. Limits of the anchor, repeatability, robustness, and generalization

The sealed anchor, batch 4, is one unreplicated boundary observation. Its normalized pH is consistent with the broader concentration curve, but its precipitation_signal of 0.015897 is only one modest positive against a declared final-assay standard deviation of 0.006. It cannot establish a threshold, a solid mass, or a repeatable precipitation state, and it must not be described as proven optimal.

Intermediate and final measurements are not independent batch replicates. Their pH agreement in batches such as 1 and 7 supports local measurement consistency, but their precipitation disagreement shows that small proxy values are not locally robust. No condition was remade from a fresh vessel, so between-batch repeatability at identical settings is unknown.

The pH relation is locally robust only for water, Catalyst A at 0.002 mol, 600 s at 400 rpm, reagent amounts of 0.005–0.035 mol, volumes of 0.040–0.080 L, and analytical concentrations of 0.0625–0.875 M. Batch 12 does not extend that common-condition domain cleanly because its catalyst amount changed.

Generalization beyond that domain is limited. The campaign did not test Catalysts B–D, catalyst omission, ethanol, acetonitrile, toluene, alternative temperatures, longer equilibration, or independently controlled metal and acid inventories. It did not establish scale invariance at constant concentration. Anonymous benchmark identities prevent translation to named real chemistry. Finally, the inferred relationships describe this bounded synthetic world only; neither the structural topology nor its fitted concentration curve should be treated as a universal aqueous-chemistry law or transferred to another world without new evidence.

## EQS — sealed structured mechanism supplement

- Network family: `indeterminate`
- Aqueous intermediate: `indeterminate`
- Selected equations: `acid_dissociation, free_ion_solid_equilibrium`
- Cited source batches: `1, 4, 8, 9, 11, 12`
- Rationale: The source campaign supports acid dissociation and permits a free-ion solid equilibrium, but it cannot determine whether a distinct aqueous MA intermediate exists. The systematic pH response, including batch 1, supports an acid-producing equilibrium. Batch 4 supplied the clearest nonzero final precipitation proxy (0.015897), while batches 8 and 12 were zero and batches 9 and 11 were only weakly positive. These results leave both direct free-ion precipitation and precipitation preceded by aqueous ion pairing observationally viable. No measurement identified MA(aq), so aqueous ion-pair association is not selected as an established equation.

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean width | Interval score |
|---|---:|---:|---:|---:|
| pH_normalized | 0.00338102 | 1 | 0.0493333 | 0.0493333 |
| acid_dissociation_fraction | 0.00478694 | 0.983333 | 0.0434167 | 0.0435802 |
| precipitation_signal | 0.00296792 | 0.95 | 0.0173333 | 0.0192169 |

## Structural evaluation

Truth family: `aqueous_ion_pair_intermediate`; predicted family: `indeterminate`; abstained: `True`; family correct: `False`; exact equation set correct: `False`; equation-set Jaccard: `0.666667`.

## Response-shape evaluation

Concentration slope MAE `0.0114322` and curvature MAE `0.0156382`. Dilution slope MAE `0.00741369` and curvature MAE `0.0134811`.

## Evidence boundary

K1 was sealed before Q, Q before K2, K2 before EQS, and reference truth was generated only after all 15 EQS responses were sealed. The task is characterization rather than optimization. Numerical residual and equilibrium confidence are environment diagnostics, not agent uncertainty or task scores. Private authentication and raw model process material are excluded.
