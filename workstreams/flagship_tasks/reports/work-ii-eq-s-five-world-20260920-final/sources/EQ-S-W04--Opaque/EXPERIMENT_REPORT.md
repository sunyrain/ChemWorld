# EQ-S-W04--Opaque — final English experiment report

World `EQ-S-W04`; information arm `Opaque`; task `mechanism characterization`; effective status `completed`; result origin `original`.

## Source campaign

The autonomous campaign completed 12/12 batches and 60 recorded operations. Exact replay is `True`; rollbacks: 0.

| Batch | Solvent L | Reagent mol | Measurements | pH normalized | Free dissociation | Precipitation signal | Residual |
|---:|---:|---:|---|---:|---:|---:|---:|
| 1 | 0.02 | 0.035 | ph_meter, final_assay | 0.0597295 | 0.00349512 | 0.0627256 | 0.00205979 |
| 2 | 0.08 | 0.005 | ph_meter, final_assay | 0.17103 | 0 | 0 | 0 |
| 3 | 0.05 | 0.025 | ph_meter, final_assay | 0.110517 | 0 | 0.000123808 | 0.00252511 |
| 4 | 0.02 | 0.015 | ph_meter, final_assay | 0.0949426 | 0 | 0 | 0 |
| 5 | 0.08 | 0.035 | ph_meter, final_assay | 0.110025 | 0 | 0 | 0 |
| 6 | 0.05 | 0.005 | ph_meter, final_assay | 0.159525 | 0.00614736 | 0 | 0.00285055 |
| 7 | 0.02 | 0.025 | ph_meter, final_assay | 0.0726679 | 0 | 0.0360759 | 5.2803e-05 |
| 8 | 0.08 | 0.015 | ph_meter, final_assay | 0.136471 | 0.00437465 | 0 | 0.0101543 |
| 9 | 0.05 | 0.035 | ph_meter, final_assay | 0.0951608 | 0 | 0.00952714 | 6.42783e-05 |
| 10 | 0.02 | 0.005 | ph_meter, final_assay | 0.125354 | 0 | 0.0024222 | 0 |
| 11 | 0.08 | 0.025 | ph_meter, final_assay | 0.121514 | 0.00478719 | 0.00102453 | 0 |
| 12 | 0.05 | 0.015 | ph_meter, final_assay | 0.123862 | 0.0013783 | 0.0127966 | 4.58323e-05 |

### Sealed evidentiary anchor

Batch `1`: Batch 1 is the clearest evidentiary anchor: the high-loading, low-dilution boundary produced the largest final precipitation proxy while also anchoring the lowest-pH end of the factorial grid, making it especially useful for discriminating concentration-coupled precipitation from loading-only explanations. This is an evidence-selection rationale, not an optimum claim.

## K1 — sealed mechanistic report

MECHANISTIC REPORT

1. Scope and experimental design

I completed 12 independent water-only batches spanning a 4 × 3 loading–dilution grid. Reagent amounts were 0.005, 0.015, 0.025, and 0.035 mol; liquid volumes were 0.020, 0.050, and 0.080 L. Thus the analytical loading C_T = n_R/V ranged from 0.0625 to 1.75 mol L^-1. Every batch received a pre-termination pH-meter measurement and a post-termination final assay. No catalyst, temperature, time, solvent-identity, ionic-strength, or order-of-addition intervention was performed. The report therefore concerns this bounded, approximately room-temperature aqueous slice only.

No instance-specific prior or structural dossier was supplied. The material packet explicitly said that task-specific nominal properties were unavailable and that experimental evidence was authoritative. Consequently, there was no dossier claim to confirm or contradict; catalyst and species identities remain opaque.

2. Direct observations

Final-assay results, listed as batch: amount/volume, C_T, normalized pH, acid-dissociation fraction, precipitation proxy, were:

1: 0.035 mol/0.020 L, 1.75 M, 0.05973, 0.00350, 0.06273.
2: 0.005/0.080, 0.0625 M, 0.17103, 0, 0.
3: 0.025/0.050, 0.500 M, 0.11052, 0, 0.000124.
4: 0.015/0.020, 0.750 M, 0.09494, 0, 0.
5: 0.035/0.080, 0.4375 M, 0.11002, 0, 0.
6: 0.005/0.050, 0.100 M, 0.15953, 0.00615, 0.
7: 0.025/0.020, 1.25 M, 0.07267, 0, 0.03608.
8: 0.015/0.080, 0.1875 M, 0.13647, 0.00437, 0.
9: 0.035/0.050, 0.700 M, 0.09516, 0, 0.00953.
10: 0.005/0.020, 0.250 M, 0.12535, 0, 0.00242.
11: 0.025/0.080, 0.3125 M, 0.12151, 0.00479, 0.00102.
12: 0.015/0.050, 0.300 M, 0.12386, 0.00138, 0.01280.

Because normalized pH is pH/14, the observed final pH range was approximately 0.836 to 2.394. The pH-meter and final-assay normalized-pH results agreed with an RMS difference of 0.00350 and mean absolute difference of 0.00297. This cross-instrument agreement makes the principal pH trend substantially more credible than any isolated channel value.

Seven of twelve final acid-fraction estimates were exactly zero. The five positive estimates ranged only from 0.00138 to 0.00615; their all-batch mean, including zeros, was 0.00168. These values are comparable to the final assay's stated noise scale of 0.006 and are affected by the zero boundary. They support only the conclusion that the reported free dissociation fraction is very small or unresolved, not a precise dissociation law.

The precipitation proxy was also boundary-heavy. Its all-batch mean was 0.01039. The four batches at C_T >= 0.70 M had a mean proxy of 0.02708, compared with 0.00205 for the other eight batches. Nevertheless, the response was not deterministically monotone: batch 4 at 0.75 M returned zero, whereas batch 12 at 0.30 M returned 0.01280.

Final equilibrium residuals were small, from zero to 0.01015. The reported equilibrium-confidence channel ranged approximately 0.628–0.697, but that channel is an environment diagnostic and is not used here as my epistemic confidence or as evidence for a specific topology.

3. Empirical relationships

The strongest identifiable relationship is a concentration collapse for pH. A least-squares fit over all 12 final assays gives

pH_normalized = 0.08239 - 0.03300 ln(C_T / 1 M).

The fit has R^2 = 0.99275, RMS residual 0.00264, and maximum absolute residual 0.00526 in normalized-pH units. Equivalently, within the tested range,

pH = 1.1534 - 0.4620 ln(C_T / 1 M),

or

[H+]_effective ≈ 0.0702 (C_T / 1 M)^1.064 mol L^-1.

This last expression is an empirical re-expression of the pH fit, not proof that ideal concentration equals hydrogen-ion activity.

A separate fit using amount and volume gives

pH_normalized = 0.08863 - 0.03233 ln(n_R) + 0.03410 ln(V),

with the intercept dependent on the chosen units. The loading and volume coefficients have nearly equal magnitudes and opposite signs. This is the expected signature of dependence primarily on n_R/V rather than independent dependence on total moles and vessel volume.

Several actual comparisons caused this account to solidify. Batch 1, the high-loading/low-volume corner, gave the lowest normalized pH and largest precipitation proxy. Batch 2, the opposite corner, gave the highest normalized pH and no precipitation. Batches 3 and 5 had different amounts and volumes but similar concentrations, 0.500 and 0.4375 M, and nearly identical normalized pH values, 0.11052 and 0.11002. Batches 10–12 clustered at 0.250–0.3125 M and likewise clustered at normalized pH 0.12151–0.12535. These observations shifted the interpretation from separate amount and dilution effects to a predominantly concentration-controlled pH law.

Precipitation evidence initially suggested a simple concentration threshold after batches 1 and 2. Batches 7 and 9 strengthened the qualitative association: their 1.25 and 0.70 M conditions produced proxies of 0.03608 and 0.00953. However, batch 4's zero at 0.75 M and batch 12's 0.01280 at 0.30 M forced revision from a sharp deterministic threshold to a noisy, bounded onset or nucleation-like process. The experiment does not identify a unique threshold constant.

4. Plausible equilibrium network and balances

A defensible minimal topology contains proton transfer plus precipitation:

HA ⇌ H+ + A-, with K_a = a_H a_A / a_HA,

and a precipitation association such as

u A- + mu M^(z+) ⇌ P(s),

with an ion-activity product Q and saturation condition Q ≷ K_sp. M denotes an unidentified counter-species or co-formulated ion; its existence and stoichiometry are not directly observed. Water autoionization, H2O ⇌ H+ + OH-, closes the acid–base system but should be negligible at the observed acidity.

An illustrative acid-family balance is

C_A,T = [HA] + [A-] + nu P_V,

where P_V is precipitated formula units per liquid volume. A charge balance has the generic form

[H+] + sum(z_i[C_i+]) = [OH-] + [A-] + sum(|z_j|[C_j-]).

If precipitation removes an anionic or conjugate-base species, acid dissociation and precipitation are thermodynamically coupled through the shared free-ion activity. Dilution changes both proton activity and the precipitation ion-activity product. The public precipitation channel is only a bounded normalized proxy, so an additional observation map is required, for example

precipitation_signal = g(P_V, particle state, nucleation history) + measurement error,

where g is unknown and need not be linear in precipitated mass.

This topology can qualitatively explain all three channels: increasing analytical concentration increases proton activity and lowers pH; the tagged free dissociation fraction can remain small under common-ion or high-acidity suppression; and sufficiently high free-ion activities can activate precipitation. Precipitation can then feed back on dissociation by removing one free species.

However, the simplest ideal monoprotic-acid version of that topology is contradicted quantitatively. If the anonymous reagent were solely HA and its dissociation were the sole source of H+, then alpha would approximately equal [H+]/C_T. The pH fit implies ratios of order 0.06–0.08 across this range, whereas the reported acid-fraction channel is 0–0.00615. Instrument noise cannot bridge an order-of-magnitude discrepancy. Therefore at least one assumption must change: the reported fraction may refer to a tagged subset rather than total proton production; a separate co-loaded acid or background proton reservoir may dominate pH; activity coefficients may be very nonideal; precipitation or complexation may alter the reporting basis; or the public channels may be generated by coupled but non-identical latent pools.

A slightly richer one-network explanation is therefore preferred: a feed-coupled proton-active pool HX establishes most of the pH response, while a tagged weak-acid pool HA has a small measurable free-dissociation fraction, and A- or another coupled ion participates in precipitation. HX and HA can still belong to one equilibrium network through shared H+ and charge balance. This makes joint explanation possible, but the extra pool is conjectural and not structurally identified.

5. Topology versus refitting constants

The data support the broad topology claim that dilution enters through concentrations or activities, proton transfer controls pH, and a concentration-sensitive precipitation branch is coupled to the same aqueous state. They do not uniquely establish the number or identity of acid pools, precipitation stoichiometry, activity model, or proxy transfer function.

Changing K_a, K_sp, activity coefficients, or sensor-scale constants inside a single ideal monoprotic topology is parameter refitting, not a new topology. Such refitting cannot by itself reconcile pH-implied dissociation near several percent with an observed tagged fraction below about 0.6 percent if both quantities are required to describe the same species and hydrogen is produced only by that dissociation. Adding a second proton reservoir, a second acid step, a complexed pool, or a distinct reporting basis changes the topology or observation model. The present evidence favors one of those structural extensions over constant-only refitting, but it cannot select among them.

Likewise, threshold, sigmoid, and nucleation-hysteresis maps for the precipitation proxy may all fit these sparse, near-zero values after constants are adjusted. The data support a precipitation branch but not one unique functional form.

6. Supported interpolation

Within water, approximately room temperature, reagent amounts 0.005–0.035 mol, volumes 0.020–0.080 L, and C_T = 0.0625–1.75 M, interpolation of normalized pH with the logarithmic concentration equation is supported. Its residual scale is close to the final assay's declared normalized-pH noise. Interpolation should use concentration rather than amount alone.

Within that same domain, it is supported only qualitatively that precipitation propensity is greater in the upper concentration region. A probabilistic or soft-onset interpretation is warranted; exact zero should not automatically be interpreted as proof of no solid. The acid-fraction channel should be represented as near the lower measurement boundary, with censoring or clipping acknowledged, rather than fit to a detailed trend.

7. Extrapolation

No quantitative claim is supported below 0.0625 M or above 1.75 M, outside 0.020–0.080 L, or for different temperatures, solvents, catalysts, ionic strengths, or equilibration histories. The logarithmic pH fit must not be extended indefinitely: it would eventually violate physical bounds and ignores activity-coefficient changes at high concentration. The apparent precipitation enrichment above roughly 0.7 M is not a validated solubility threshold. Extrapolation to real acids or real salts is specifically unjustified because the species are anonymous benchmark entities.

8. Conjectures and reasonable competing explanations

Conjecture A, preferred but unproven: one coupled multi-pool network contains a dominant feed-linked proton reservoir, a weakly dissociated tagged acid pool, and an ion-pair/solid branch. It explains the tight pH concentration collapse, near-zero tagged dissociation estimates, and high-concentration precipitation tendency.

Competing explanation B: a single acid undergoes multiple dissociation or association steps, while the public acid-fraction channel reports only one free state. This can mimic a second acid pool without a literal mixture.

Competing explanation C: strong nonideal activities and ion pairing cause concentration-based mass-action calculations to misstate the relationship between pH and the reported fraction. This is plausible at up to 1.75 M, but the experiment contains no ionic-strength intervention capable of identifying it.

Competing explanation D: the pH and acid-fraction channels correspond to partly separate latent quantities linked only through the benchmark observation model. This would reproduce the data but is less chemically informative.

Competing explanation E: the precipitation proxy includes stochastic nucleation or particle-detection effects rather than equilibrium solid amount alone. The batch-4/batch-12 nonmonotonicity is consistent with this, measurement noise, or both.

9. Unidentifiable factors and conclusion

Unidentifiable factors include species identity, acid stoichiometry, intrinsic pKa values, Ksp, activity coefficients, counterion abundance, whether the feed is a mixture, solid stoichiometry, solid mass, nucleation kinetics, equilibration time, and the precipitation proxy's transfer function. Temperature dependence, solvent effects, catalyst effects, reversibility, and path dependence were not tested. Because there were no within-condition final-assay replicates, process variability cannot be separated cleanly from measurement noise.

The most secure conclusion is empirical: in this bounded aqueous world, normalized pH is governed predominantly by the amount-to-volume ratio and follows a highly reproducible logarithmic concentration relation. The reported free acid-dissociation fraction remains at or near its measurement floor. Precipitation is weak and noisy but enriched at high concentration. A single coupled equilibrium network can explain the three responses only if it contains an additional pool, reporting distinction, or strong nonideality beyond the simplest ideal monoprotic-acid model. Thus a broad proton-transfer/precipitation topology is supported, while its constants and several structurally distinct refinements remain unidentifiable.

## Q — sealed blind predictions

| Query | Metric | Estimate | 80% lower | 80% upper |
|---|---|---:|---:|---:|
| Q01 | pH_normalized | 0.339 | 0.285 | 0.395 |
| Q01 | acid_dissociation_fraction | 0.041 | 0.012 | 0.1 |
| Q01 | precipitation_signal | 0.001 | 0 | 0.009 |
| Q02 | pH_normalized | 0.263 | 0.232 | 0.296 |
| Q02 | acid_dissociation_fraction | 0.013 | 0 | 0.035 |
| Q02 | precipitation_signal | 0.001 | 0 | 0.01 |
| Q03 | pH_normalized | 0.204 | 0.188 | 0.222 |
| Q03 | acid_dissociation_fraction | 0.006 | 0 | 0.021 |
| Q03 | precipitation_signal | 0.002 | 0 | 0.011 |
| Q04 | pH_normalized | 0.151 | 0.142 | 0.16 |
| Q04 | acid_dissociation_fraction | 0.003 | 0 | 0.015 |
| Q04 | precipitation_signal | 0.002 | 0 | 0.011 |
| Q05 | pH_normalized | 0.105 | 0.098 | 0.113 |
| Q05 | acid_dissociation_fraction | 0.003 | 0 | 0.013 |
| Q05 | precipitation_signal | 0.003 | 0 | 0.016 |
| Q06 | pH_normalized | 0.075 | 0.067 | 0.083 |
| Q06 | acid_dissociation_fraction | 0.002 | 0 | 0.012 |
| Q06 | precipitation_signal | 0.036 | 0.022 | 0.051 |
| Q07 | pH_normalized | 0.105 | 0.093 | 0.119 |
| Q07 | acid_dissociation_fraction | 0.003 | 0 | 0.014 |
| Q07 | precipitation_signal | 0.003 | 0 | 0.02 |
| Q08 | pH_normalized | 0.142 | 0.132 | 0.152 |
| Q08 | acid_dissociation_fraction | 0.003 | 0 | 0.016 |
| Q08 | precipitation_signal | 0.002 | 0 | 0.011 |
| Q09 | pH_normalized | 0.174 | 0.165 | 0.182 |
| Q09 | acid_dissociation_fraction | 0.004 | 0 | 0.018 |
| Q09 | precipitation_signal | 0.002 | 0 | 0.01 |
| Q10 | pH_normalized | 0.189 | 0.177 | 0.201 |
| Q10 | acid_dissociation_fraction | 0.005 | 0 | 0.022 |
| Q10 | precipitation_signal | 0.001 | 0 | 0.01 |
| Q11 | pH_normalized | 0.204 | 0.185 | 0.225 |
| Q11 | acid_dissociation_fraction | 0.006 | 0 | 0.023 |
| Q11 | precipitation_signal | 0.002 | 0 | 0.013 |
| Q12 | pH_normalized | 0.204 | 0.189 | 0.221 |
| Q12 | acid_dissociation_fraction | 0.006 | 0 | 0.021 |
| Q12 | precipitation_signal | 0.002 | 0 | 0.011 |

### Q rationales

- **Q01**: This concentration is 150-fold below the lowest tested concentration, so the pH estimate extrapolates the sealed logarithmic concentration law and has a wide interval. A weak-acid-like low-concentration rise is allowed for the otherwise unresolved dissociation channel. Precipitation should remain at the clipped-noise floor.

- **Q02**: The pH prediction is a one-decade extrapolation step below Q03 under the fitted log-concentration response. Dissociation may begin to become detectable on dilution, but K1 did not identify its law, so the interval includes zero and appreciably larger values. No precipitation onset is expected.

- **Q03**: This is below the observed concentration range but close enough for a moderate extrapolation of the pH law. The acid fraction is predicted near the assay resolution, with uncertainty dominated by the unidentified acid-pool topology. The concentration is far below the inferred precipitation-onset region.

- **Q04**: This condition lies between K1 batches 6 and 8 in concentration, whose final normalized pH values were 0.15953 at 0.10 M and 0.13647 at 0.1875 M. The dissociation channel remains near its lower boundary, and precipitation is expected to be only a clipped-noise-level result.

- **Q05**: The pH estimate is anchored directly by K1 batch 3 at 0.50 M, which returned 0.11052, and by batch 5 at 0.4375 M, which returned 0.11002; the regression smooths these to 0.105. Batch 3's precipitation proxy was 0.000124, but proximity to the uncertain onset warrants an asymmetric upper range.

- **Q06**: K1 batch 7 tested the same 1.25 M concentration at 0.020 L and returned normalized pH 0.07267 and precipitation proxy 0.03608, providing a close anchor for this 0.024 L query. The acid fraction remains unresolved near zero. The precipitation interval includes assay noise and uncertainty in the soft-onset model.

- **Q07**: The concentration matches Q05 and K1 batch 3, so the concentration-collapse topology predicts the same central pH and near-floor chemistry. However, 0.006 L is below K1's minimum volume of 0.020 L; the intervals are widened for possible absolute-scale, sampling, or nucleation effects that K1 could not identify.

- **Q08**: The predicted pH interpolates between K1 batch 6 at 0.10 M and batch 8 at 0.1875 M. The 0.018 L volume is only slightly outside the studied volume range, and K1 supported concentration rather than absolute amount as the main pH variable. Both other channels should remain near their measurement floors.

- **Q09**: This exactly matches the concentration of K1 batch 2, whose final normalized pH was 0.17103 and whose precipitation and acid-fraction estimates were both zero. The different absolute scale produces only modest additional uncertainty under the concentration-collapse account.

- **Q10**: This is a modest dilution extrapolation below K1's 0.0625 M boundary. The pH estimate follows the sealed logarithmic trend, while the acid fraction is allowed to rise slightly but remains poorly identified. Precipitation is not mechanistically expected at this loading.

- **Q11**: The central values equal Q03 because both have 0.025 M analytical concentration. The smaller 0.012 L scale is outside K1's tested volume range, so the intervals are wider to cover unmeasured scale dependence even though the fitted amount and volume coefficients supported their ratio as the dominant pH control.

- **Q12**: This shares the 0.025 M concentration of Q03 and Q11, while its 0.072 L volume lies inside K1's tested range. The concentration-collapse model therefore gives the same central predictions with a narrower scale-related interval than Q11. Precipitation remains far below the observed high-concentration onset.

Shared rationale:

The sealed K1 account identified analytical concentration C_T = n_R/V as the dominant variable. Final normalized pH over 0.0625–1.75 M followed pH_normalized = 0.08239 - 0.03300 ln(C_T/1 M), with R^2 0.99275 and RMS residual 0.00264; that relation supplies the pH centers. Intervals are narrow for interpolation or direct concentration matches and expand for low-concentration or sub-0.020-L extrapolation. The final acid-dissociation measurements were boundary-censored—seven zeros, mean 0.00168, and maximum 0.00615—so their centers use a weak-acid-like dilution rise only as a cautious continuation, while broad intervals cover the competing zero-pool, tagged-pool, and nonideal-activity explanations retained in K1. Precipitation was near zero below roughly 0.5–0.7 M but increased at high concentration: K1 batch 7 gave 0.03608 at 1.25 M and batch 1 gave 0.06273 at 1.75 M. Predictions therefore use a soft concentration onset, retain a small positive point at the clipped observation floor, and use asymmetric bounded intervals. Equal-concentration scale controls receive equal central values because K1 found nearly equal and opposite logarithmic amount and volume coefficients; their intervals still allow unidentified absolute-scale and nucleation effects. All intervals include final-assay observation noise plus model and extrapolation uncertainty.

## K2 — sealed seven-part retrospective

1. Supplied structural claims

No instance-specific structural dossier or prior was supplied. The material packet explicitly reported that task-specific nominal properties were unavailable, so there were no dossier constants, species assignments, or reaction equations to validate.

The broad public framing—a bounded aqueous acid-dissociation/precipitation slice—was supported at a phenomenological level. Normalized pH collapsed strongly with analytical concentration, and precipitation was enriched at high concentration: batch 7 gave 0.03608 at 1.25 M and batch 1 gave 0.06273 at 1.75 M, whereas batch 2 gave zero at 0.0625 M.

The simplest one-to-one ideal monoprotic interpretation was contradicted by the joint channels. The observed pH implied an effective proton concentration corresponding to roughly 6–8% of analytical loading, while final reported dissociation fractions were only 0–0.00615. Refitting only Ka cannot reconcile those quantities if the same acid is the sole proton source and the reported fraction has its ordinary stoichiometric meaning.

That contradiction was recognized in K1 but was not acted on experimentally: the factorial campaign continued as planned rather than adding a low-concentration, ionic-strength, or species-selective diagnostic. It would therefore be wrong to say that no contradiction was observed. What remained untested were the proposed resolutions: a second proton-active pool, a polyprotic or associated species, a tagged reporting basis, strong activity effects, or an observation-model scaling.

2. Experiments that formed or changed the account

Batch 1, the 1.75 M high-loading/low-volume corner, initially established the low-pH/high-precipitation end: normalized pH 0.05973 and precipitation proxy 0.06273. Batch 2, the opposite 0.0625 M corner, gave normalized pH 0.17103 and zero precipitation. Together they first suggested concentration control.

Batches 3 and 5 made that inference substantially stronger. Although their amounts and volumes differed, their concentrations were close—0.500 and 0.4375 M—and their normalized pH values were nearly identical, 0.11052 and 0.11002. Batches 10–12 similarly clustered near 0.25–0.3125 M and returned normalized pH values of 0.12151–0.12535. Those accumulated observations changed the working account from separate amount and dilution effects to a dominant n/V relationship.

The precipitation account also changed. Batches 1 and 2 initially suggested a clean threshold. Batch 7 at 1.25 M and 0.03608 precipitation, and batch 9 at 0.70 M and 0.00953, supported a high-concentration onset. But batch 4 returned zero at 0.75 M, while batch 12 returned 0.01280 at only 0.30 M. K1 therefore revised the claim to a noisy soft onset or nucleation-sensitive proxy rather than a deterministic threshold.

The repeated near-zero dissociation measurements caused rejection of the simplest shared-pool monoprotic account. Seven final results were exactly zero, and even the largest was only 0.00615 in batch 6. This was an accumulated-observation judgment, not a dossier-derived conclusion.

No experimental choice relied on an instance dossier. The 4 × 3 water-only grid was a coverage choice. The assumptions that water was the appropriate common medium, concentration would be the principal coordinate, and one intermediate pH measurement per batch was sufficient were design assumptions. The later multi-pool or altered-reporting-basis interpretation was an untested mechanistic assumption introduced to reconcile the channels.

3. Strongest competing explanation

The strongest competing reaction network is a single polyprotic or association-capable reagent rather than two chemically distinct acid pools. In that alternative, an initial proton-release step controls pH, the public dissociation fraction reports a later, tagged, or uncomplexed state, and a conjugate ion participates in precipitation. It can reproduce the apparent separation between pH and the reported fraction without requiring a literal feed mixture.

The strongest parameter/observation-only alternative retains one acid/precipitation topology but introduces nonideal activities and an unknown scale or basis for the dissociation readout. That could make the reported fraction much smaller than [H+]/C_T. If the fraction must instead be the ordinary stoichiometric fraction of the sole proton-producing species, constant refitting alone is insufficient.

The evidence distinguishes concentration control from independent amount-only control for pH and supports some high-concentration precipitation branch. It cannot distinguish two acid pools from multiple steps within one molecule, determine whether activity or reporting conventions caused the channel mismatch, identify precipitation stoichiometry, or separate equilibrium solid amount from nucleation and proxy noise.

4. One additional experiment

I would prepare 0.00032 mol reagent in 0.080 L water, giving C_T = 0.0040 M, measure once with the pH meter, terminate, and perform the required final assay. This is legal and targets the largest structural uncertainty while retaining the largest available volume.

If normalized pH continued the K1 logarithmic trend and the dissociation fraction rose clearly above approximately 0.02, that would support a dilution-sensitive weak-acid or association branch. If pH followed the trend while the fraction remained at the zero boundary, the separate/tagged proton-pool interpretation would become more credible. If pH flattened, a background-acidity or low-concentration asymptote would be required. If both pH and fraction departed together, the K1 logarithmic law would be recognized as local rather than mechanistic. Any precipitation signal substantially above its noise-scale floor would contradict the proposed high-concentration onset and favor scale, contamination-like latent structure, or a nonmonotone proxy. This experiment would still not uniquely identify species or constants, but it would discriminate the most consequential competing accounts.

5. Objective-driven trade-offs

The objective was characterization rather than process optimization. I therefore used all 12 completed batches for a structured 4 × 3 amount–volume grid rather than concentrating runs at a favorable score. Each batch received one intermediate pH measurement and one final assay, exhausting the available measurement opportunities while preserving broad coverage.

That decision favored global coverage and identification of the n/V coordinate over replication and precise local parameter estimation. It also meant that catalyst, temperature, solvent identity, time, and order effects were left untested. No batch was selected or repeated to improve the native operational score; that score was explicitly treated as diagnostically irrelevant. Batch 1 was selected as the sealed anchor because it was structurally discriminating—the strongest precipitation response and lowest-pH boundary—not because it was claimed to be optimal.

6. Underused evidence and least-reliable predictions

The pre-termination pH-meter record was underused beyond its aggregate agreement with the final assay. Pairwise examination could have better quantified state-change versus instrument disagreement. Its acid-fraction and precipitation estimates were noisier but could also have informed a hierarchical censored-channel analysis. The small equilibrium residuals were noted but not exploited, appropriately, because they do not identify topology. The nonmonotone precipitation evidence in batches 4 and 12 deserved more weight in uncertainty modeling than a simple onset curve provided.

The least reliable blind predictions are Q01 and Q02, whose concentrations were respectively about 150-fold and 15-fold below the lowest K1 concentration. Their pH estimates extrapolated the logarithmic law, and their dissociation estimates depended on a weak-acid-like continuation that K1 explicitly classified as conjectural. Q01's dissociation interval of 0.012–0.100 is especially inconsistent with the full K1 uncertainty because it excludes zero even though K1 could not rule out a persistently boundary-level tagged fraction.

Q03, Q10, Q11, and Q12 also extrapolated below the concentration range. Q11 additionally used 0.012 L, below the tested volume range. Q07, at 0.006 L, is the most severe volume extrapolation; equal-concentration central values were defensible under the concentration-collapse judgment, but its pH and precipitation intervals may not fully cover scale or sampling effects. Precipitation predictions for Q05 and Q07 at 0.50 M are sensitive to the poorly identified onset. Q06 is comparatively stronger because batch 7 directly tested 1.25 M at a nearby volume.

All acid-fraction predictions are less reliable than the pH predictions because K1 measurements were dominated by clipping and instrument noise. No prediction truth or score has been observed, so these criticisms concern contemporaneous evidential scope rather than hindsight.

7. Limits of the sealed anchor and generalization

The sealed anchor, batch 1, is a single high-concentration boundary observation: 0.035 mol in 0.020 L, normalized pH 0.05973, dissociation fraction 0.00350, and precipitation proxy 0.06273. It was not replicated and cannot establish repeatability, a precise variance, a solubility threshold, or optimality. Its value is that it anchors the extreme response and discriminates concentration-sensitive accounts.

Local robustness is strongest for pH because two instruments agreed across the campaign and the concentration regression had small residuals. Even there, the pre-termination and final measurements were not true independent replicates of one unchanged assay state. Repeatability of dissociation and precipitation is unknown because there were no same-condition final-assay replicates, and both channels were bounded near zero.

Generalization is best supported only for water, approximately room-temperature operation, 0.005–0.035 mol reagent, 0.020–0.080 L volume, and 0.0625–1.75 M concentration. Generalization below that concentration range is extrapolation; generalization below 0.020 L is additionally a scale extrapolation. Nothing in K1 supports transfer to other solvents, catalysts, temperatures, ionic strengths, named real acids, named precipitates, or independently frozen worlds with different latent parameters.

The evidence supports a local empirical concentration law and a broad proton-transfer/precipitation topology. It does not prove a unique network, unique constants, universal scaling, repeatability of the anchor, or an optimal operating condition.

## EQS — sealed structured mechanism supplement

- Network family: `indeterminate`
- Aqueous intermediate: `indeterminate`
- Selected equations: `acid_dissociation, free_ion_solid_equilibrium`
- Cited source batches: `1, 2, 4, 7, 12`
- Rationale: The source campaign supports acid dissociation coupled to a free-ion/solid equilibrium: batch 1 at 1.75 M had normalized pH 0.05973 and precipitation signal 0.06273, while batch 2 at 0.0625 M had normalized pH 0.17103 and zero precipitation; batch 7 at 1.25 M also showed precipitation signal 0.03608. However, batches 4 and 12 showed nonmonotone precipitation responses, and the near-zero dissociation channel could not distinguish direct free-ion precipitation from an aqueous ion-pair intermediate. The sealed account therefore supports the two common equations but leaves the intermediate topology unresolved.

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean width | Interval score |
|---|---:|---:|---:|---:|
| pH_normalized | 0.00652754 | 1 | 0.0346667 | 0.0346667 |
| acid_dissociation_fraction | 0.00745079 | 0.966667 | 0.0248333 | 0.0266806 |
| precipitation_signal | 0.00128062 | 0.966667 | 0.0134167 | 0.0150508 |

## Structural evaluation

Truth family: `aqueous_ion_pair_intermediate`; predicted family: `indeterminate`; abstained: `True`; family correct: `False`; exact equation set correct: `False`; equation-set Jaccard: `0.666667`.

## Response-shape evaluation

Concentration slope MAE `0.0103625` and curvature MAE `0.0124052`. Dilution slope MAE `0.00893765` and curvature MAE `0.0168662`.

## Evidence boundary

K1 was sealed before Q, Q before K2, K2 before EQS, and reference truth was generated only after all 15 EQS responses were sealed. The task is characterization rather than optimization. Numerical residual and equilibrium confidence are environment diagnostics, not agent uncertainty or task scores. Private authentication and raw model process material are excluded.
