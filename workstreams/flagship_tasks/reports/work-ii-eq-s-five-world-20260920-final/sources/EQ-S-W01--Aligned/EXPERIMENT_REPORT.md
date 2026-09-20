# EQ-S-W01--Aligned — final English experiment report

World `EQ-S-W01`; information arm `Aligned`; task `mechanism characterization`; effective status `completed`; result origin `recovery_attempt_01`.

## Source campaign

The autonomous campaign completed 12/12 batches and 60 recorded operations. Exact replay is `True`; rollbacks: 0.

| Batch | Solvent L | Reagent mol | Measurements | pH normalized | Free dissociation | Precipitation signal | Residual |
|---:|---:|---:|---|---:|---:|---:|---:|
| 1 | 0.04 | 0.002 | ph_meter, final_assay | 0.210401 | 0.0075606 | 0.00565321 | 0.00218399 |
| 2 | 0.04 | 0.006 | ph_meter, final_assay | 0.153189 | 0.0032824 | 0.0446647 | 0.00240471 |
| 3 | 0.04 | 0.012 | ph_meter, final_assay | 0.120946 | 0 | 0.078102 | 0 |
| 4 | 0.04 | 0.02 | ph_meter, final_assay | 0.0959 | 0.00694772 | 0.0943135 | 0.00429805 |
| 5 | 0.04 | 0.032 | ph_meter, final_assay | 0.0789375 | 0.00697443 | 0.0978819 | 0.00182283 |
| 6 | 0.04 | 0.04 | ph_meter, final_assay | 0.0670202 | 0 | 0.107982 | 0 |
| 7 | 0.08 | 0.002 | ph_meter, final_assay | 0.224661 | 0.0272655 | 0 | 0.00405403 |
| 8 | 0.08 | 0.006 | ph_meter, final_assay | 0.190016 | 0.00917633 | 0.0302765 | 0 |
| 9 | 0.08 | 0.012 | ph_meter, final_assay | 0.150819 | 0 | 0.0423798 | 0 |
| 10 | 0.08 | 0.02 | ph_meter, final_assay | 0.127657 | 0.00770042 | 0.0586952 | 9.47556e-05 |
| 11 | 0.08 | 0.032 | ph_meter, final_assay | 0.106746 | 0.0136618 | 0.0810537 | 0.00908356 |
| 12 | 0.08 | 0.04 | ph_meter, final_assay | 0.0945001 | 0 | 0.0969685 | 0.00694946 |

### Sealed evidentiary anchor

Batch `7`: Batch 7 is the clearest dilute-regime anchor: the final assay shows the highest resolved free-base fraction, high normalized pH, and no detectable precipitation, providing a strong contrast to the concentrated batches.

## K1 — sealed mechanistic report

MECHANISTIC REPORT

1. Scope and evidence base

The campaign comprised 12 completed aqueous batches. Every batch used water, no added catalyst, and a final assay after termination. Reagent amounts were 0.002–0.040 mol, aqueous volumes were 0.040 or 0.080 L, and nominal reagent concentrations C0 = n0/V therefore covered 0.025–1.00 mol L^-1. Conditions were approximately ambient temperature (297 K) and pressure. Temperature, solvent identity, catalyst identity, added metal concentration, equilibration time, and mixing rate were not varied. Conclusions are consequently local to this bounded synthetic aqueous world and this concentration range.

The final-assay channels used here are normalized pH, acid-dissociation fraction, and precipitation signal. The precipitation signal is a bounded proxy, not a measured solid concentration. The reported equilibrium_confidence is an environment diagnostic, not my confidence in the mechanism. Final equilibrium residuals were small, 0–0.0091, but that also does not prove a unique mechanism.

2. Direct observations

The dominant experimental variable was nominal concentration rather than reagent amount or volume separately.

At the dilute end, batch 7 contained 0.002 mol in 0.080 L (0.025 M). Its final normalized pH was 0.22466, acid-dissociation fraction was 0.02727, and precipitation signal was 0.00000. This was selected as the sealed evidentiary anchor because it clearly resolves the dilute, relatively dissociated, non-precipitating regime.

Increasing concentration lowered normalized pH and generally increased precipitation. Examples are:
- Batch 1, 0.002 mol in 0.040 L (0.050 M): pH 0.21040, dissociation 0.00756, precipitation 0.00565.
- Batch 8, 0.006 mol in 0.080 L (0.075 M): pH 0.19002, dissociation 0.00918, precipitation 0.03028.
- Batch 10, 0.020 mol in 0.080 L (0.250 M): pH 0.12766, dissociation 0.00770, precipitation 0.05870.
- Batch 3, 0.012 mol in 0.040 L (0.300 M): pH 0.12095, dissociation reported at the zero boundary, precipitation 0.07810.
- Batch 11, 0.032 mol in 0.080 L (0.400 M): pH 0.10675, dissociation 0.01366, precipitation 0.08105.
- Batch 6, 0.040 mol in 0.040 L (1.00 M): pH 0.06702, dissociation at the zero boundary, precipitation 0.10798.

Two same-concentration comparisons directly separate concentration from absolute loading and dilution:
- Batches 2 and 9 were both 0.150 M, made respectively from 0.006 mol/0.040 L and 0.012 mol/0.080 L. Their normalized pH values were 0.15319 and 0.15082, while precipitation signals were 0.04466 and 0.04238.
- Batches 4 and 12 were both 0.500 M, made respectively from 0.020 mol/0.040 L and 0.040 mol/0.080 L. Their normalized pH values were 0.09590 and 0.09450, while precipitation signals were 0.09431 and 0.09697.

Thus doubling both amount and volume caused only small changes: 0.0014–0.0024 in normalized pH and 0.0023–0.0027 in precipitation signal for these pairs. No independent volume effect is resolved by those comparisons.

The acid-dissociation channel was much less precise as a quantitative trend. The largest final value was 0.02727 in dilute batch 7, and most concentrated batches returned small values or the zero boundary. However, batch 11 returned 0.01366, and same-concentration pairs differed between small positive and zero-boundary estimates. Intermediate pH-meter measurements also sometimes disagreed materially with final estimates; for example, batch 1 gave an intermediate dissociation estimate of 0.03218 but a final value of 0.00756. I therefore interpret this channel qualitatively: free dissociation is most clearly resolved under dilution, while a precise concentration law is not identifiable.

3. Empirical relationships and interpolation

Across all 12 final assays, normalized pH is closely represented within the tested range by the descriptive interpolation

pH_normalized = 0.06635 - 0.04534 ln(C0),

where C0 is in mol L^-1. Equivalently, the decline is about 0.1044 normalized-pH unit per tenfold concentration increase. The in-sample root-mean-square residual is 0.00422 and R^2 is 0.993. This is an empirical summary, not an inferred universal acid law and not evidence that concentration is ideal activity.

Precipitation rises from zero at 0.025 M to approximately 0.108 at 1.00 M, with an increasingly shallow response at high concentration. The data support a monotone, bounded, threshold-like or saturating interpolation, but they do not identify a unique threshold, solubility product, or calibration from signal to precipitated moles.

The resolved part of the dissociation relationship is inverse: the dilute endpoint has the largest fraction, while many higher-concentration estimates are near or at zero. Because assay noise, non-negativity clipping, and precipitation all matter at this scale, fitting a detailed dissociation equation would be unjustified.

4. Plausible common equilibrium network

The simplest chemically coherent topology is the supplied direct-free-ion network:

HA(aq) <=> H+(aq) + A-(aq)
M+(aq) + A-(aq) <=> MA(s)

Here HA is a weak-acid-like dissolved form, A- is its free dissociated form, and M+ is a precipitation partner present in the bounded world. No real chemical identities are implied.

Using activities, the equilibrium relations would be

Ka = a_H a_A / a_HA
Ksp = a_M a_A

when solid MA is present. In an idealized concentration approximation, activities may be replaced by activity coefficients times concentrations. Water additionally supplies

Kw = a_H a_OH.

If s is the number of moles precipitated and n0 is the analytical acid-forming loading, a minimal acid-moiety balance is

n0 = V[HA] + V[A-] + s,

or, for the dissolved-only balance stated in the supplied structural account,

n_dissolved = n_HA + n_A-.

A corresponding metal balance is

n_M,0 = V[M+] + s.

Charge balance requires all charged species, including any undisclosed supporting ions, to balance; schematically,

[H+] + [M+] + other cations = [A-] + [OH-] + other anions.

An operational free-dissociation fraction can plausibly be represented as

alpha_free = [A-]/([HA] + [A-]),

although the public instrument contract does not expose enough species mapping to prove that this is its exact internal definition. The normalized pH channel obeys the public scaling pH_normalized = pH/14, with pH = -log10(a_H). The precipitation observation can be written only generically as

precipitation_signal = g(s/V),

where g is nonnegative, monotone, bounded, and uncalibrated.

This one network can qualitatively couple all three public responses. Increasing C0 increases acid activity and therefore H+, lowering normalized pH. It also increases the available A- and the ion product a_M a_A, which promotes MA(s) and raises the precipitation proxy. Removal of A- into solid can pull further HA dissociation while nevertheless keeping the measured free A- fraction small. Thus low free dissociation and increasing precipitation are not contradictory: free A- can be continuously generated and then sequestered.

5. How the account was formed and revised

Batch 1 initially established that a low-loading solution was acidic and had little precipitation, but its intermediate and final dissociation estimates disagreed enough to discourage reliance on a single alpha measurement. Batches 2–6 then showed a consistent pH decline and precipitation increase as concentration rose from 0.15 to 1.00 M. Batch 7 supplied the decisive dilute contrast: the highest resolved dissociation fraction and no precipitation at 0.025 M. Batches 8–12 filled the intermediate range.

Most importantly, the matched-concentration comparisons 2 versus 9 and 4 versus 12 caused me to revise the description from an ambiguous dependence on total loading or water volume to a concentration-dominated account. They show that amount and dilution act jointly through n0/V to the resolution of these data. Batch 11 prevented an overstrong claim that dissociation must decrease monotonically point by point, because its value was higher than several neighboring estimates. I therefore retain only the qualitative inverse tendency for dissociation.

6. Assessment of the supplied structural information

A structural prior was supplied: a local direct-free-ion precipitation family at locus S, with HA dissociation, direct M+ + A- precipitation, and no distinct aqueous MA intermediate. No task-specific nominal-property dossier was supplied, and no instance-specific prior record was supplied.

The observed common concentration response supports the supplied topology as a parsimonious explanation. In particular, dilute batch 7 is compatible with dissolved dissociation without precipitation, while increasingly concentrated batches show lower pH and greater precipitation. Nothing observed contradicts the proposed HA/H+/A-/MA(s) graph.

However, the claimed absence of aqueous MA could not be directly tested. The public channels provide aggregate pH, a free-dissociation fraction, and a precipitation proxy, not species-resolved detection of MA(aq). The experiments also did not independently vary or measure M+, so its source, inventory, and activity are unidentifiable. The structural account is therefore supported as a viable local network but not verified as unique.

7. Topology claim versus parameter refitting

There are two distinct inferential levels.

Topology claim: the data are consistent with one acid dissociation node coupled through free A- to a precipitation node, without needing separate unrelated mechanisms for the three channels.

Parameter fitting inside that topology: Ka, Ksp, activity coefficients, total M inventory, and the proxy response g could be adjusted to reproduce different quantitative curves while leaving the same reaction graph unchanged. The present observations do not identify those constants separately. The empirical log-concentration pH fit is not a determination of Ka, and the precipitation curve is not a determination of Ksp.

Moreover, successful refitting of the direct network would not prove its topology. A network containing HA <=> H+ + A-, followed by M+ + A- <=> MA(aq) and MA(aq) <=> MA(s), could generate almost identical aggregate channels after its constants were refitted. Distinguishing those alternatives requires an observable specific to dissolved MA or an independent perturbation of M activity.

8. Competing explanations

Reasonable alternatives include:

- A hidden aqueous ion-pair or MA complex preceding precipitation. This is observationally equivalent to direct precipitation if the intermediate is not measured.
- Concentration-dependent activity coefficients or ionic-strength effects. These could produce the steep pH-versus-log-concentration relationship without changing reaction stoichiometry.
- An empirical solubility or aggregation transition rather than an ideal Ksp-controlled crystalline phase. The bounded precipitation proxy cannot distinguish nucleation, amorphous aggregation, or true equilibrium solid formation.
- A heterogeneous binding or sequestration process that removes A- and produces the same inverse dissociation/positive precipitation pattern.
- A latent supporting-ion or finite-M inventory whose concentration co-varies with the prepared state. Because M was neither dosed nor assayed independently, this cannot be separated from Ksp or proxy calibration.
- Two unrelated concentration-response functions for acid and precipitation. This less parsimonious account is not required by the data, but aggregate observations cannot formally exclude it.

A distinct volume-controlled mechanism is disfavored within 0.040–0.080 L by the matched-concentration batches, although very small effects below current resolution remain possible.

9. Identifiability and uncertainty

Identifiable or well supported:
- Nominal concentration n0/V is the principal control variable over the tested design.
- Normalized pH decreases smoothly with concentration.
- The precipitation proxy generally increases and begins to flatten at higher concentration.
- The dilute endpoint has the clearest resolved free-dissociation fraction and no detectable precipitation.
- One coupled equilibrium network is sufficient to organize all three channels.

Not identifiable:
- Numerical Ka or Ksp.
- Activities and activity coefficients.
- Total or free M concentration and the origin of M.
- Conversion from precipitation signal to solid amount.
- Presence or absence of aqueous MA.
- Solid structure, nucleation kinetics, or reversibility.
- Exact internal definition of the reported dissociation fraction.
- Separate effects of temperature, time, mixing, solvent, or catalyst.

There were no independent replicate batches at every condition. The same-concentration pairs provide limited reproducibility evidence for pH and precipitation, but the dissociation values are close to the assay noise scale and often clipped at zero. Consequently, the smooth pH relationship is much more secure than any fitted alpha relationship.

10. Observation, interpolation, extrapolation, and conjecture

Observation: the cited batch values, including the paired-concentration agreements and the dilute-to-concentrated trends, are direct public measurements.

Interpolation: the logarithmic pH equation and a monotone bounded precipitation curve summarize behavior only between 0.025 and 1.00 M in water near 297 K. They are descriptive fits, not fundamental laws.

Extrapolation: behavior below 0.025 M, above 1.00 M, at volumes outside 0.040–0.080 L, or under different temperatures, solvents, catalysts, metal inventories, mixing, or waiting times is unsupported. The fitted pH equation and apparent precipitation plateau should not be extended into those regions.

Conjecture: the direct HA dissociation/free-ion precipitation network, precipitation-driven sequestration of A-, activity effects, and the functional form g(s/V) are mechanistic interpretations. They are chemically coherent and consistent with all three channels, but species-resolved evidence was not available to establish them uniquely.

Overall conclusion: within the tested aqueous range, loading and dilution act primarily through nominal concentration. A single coupled weak-acid/free-ion precipitation network parsimoniously explains the decreasing normalized pH, weak and noisy free-dissociation fraction, and increasing bounded precipitation proxy. The experiment supports this topology as a defensible local account, but it does not distinguish direct precipitation from a hidden dissolved-complex route or identify equilibrium constants by parameter refitting alone.

## Q — sealed blind predictions

| Query | Metric | Estimate | 80% lower | 80% upper |
|---|---|---:|---:|---:|
| Q01 | pH_normalized | 0.292 | 0.265 | 0.325 |
| Q01 | acid_dissociation_fraction | 0.196 | 0.13 | 0.28 |
| Q01 | precipitation_signal | 0.001 | 0 | 0.012 |
| Q02 | pH_normalized | 0.254 | 0.238 | 0.272 |
| Q02 | acid_dissociation_fraction | 0.067 | 0.035 | 0.11 |
| Q02 | precipitation_signal | 0.002 | 0 | 0.015 |
| Q03 | pH_normalized | 0.225 | 0.216 | 0.234 |
| Q03 | acid_dissociation_fraction | 0.028 | 0.012 | 0.047 |
| Q03 | precipitation_signal | 0.005 | 0 | 0.018 |
| Q04 | pH_normalized | 0.161 | 0.152 | 0.169 |
| Q04 | acid_dissociation_fraction | 0.008 | 0 | 0.021 |
| Q04 | precipitation_signal | 0.038 | 0.024 | 0.053 |
| Q05 | pH_normalized | 0.095 | 0.089 | 0.102 |
| Q05 | acid_dissociation_fraction | 0.004 | 0 | 0.014 |
| Q05 | precipitation_signal | 0.096 | 0.083 | 0.108 |
| Q06 | pH_normalized | 0.056 | 0.045 | 0.068 |
| Q06 | acid_dissociation_fraction | 0.002 | 0 | 0.013 |
| Q06 | precipitation_signal | 0.114 | 0.098 | 0.131 |
| Q07 | pH_normalized | 0.095 | 0.086 | 0.104 |
| Q07 | acid_dissociation_fraction | 0.004 | 0 | 0.016 |
| Q07 | precipitation_signal | 0.096 | 0.08 | 0.111 |
| Q08 | pH_normalized | 0.148 | 0.139 | 0.156 |
| Q08 | acid_dissociation_fraction | 0.007 | 0 | 0.02 |
| Q08 | precipitation_signal | 0.047 | 0.033 | 0.062 |
| Q09 | pH_normalized | 0.2 | 0.19 | 0.209 |
| Q09 | acid_dissociation_fraction | 0.014 | 0.002 | 0.029 |
| Q09 | precipitation_signal | 0.02 | 0.007 | 0.034 |
| Q10 | pH_normalized | 0.217 | 0.208 | 0.226 |
| Q10 | acid_dissociation_fraction | 0.022 | 0.007 | 0.041 |
| Q10 | precipitation_signal | 0.012 | 0 | 0.026 |
| Q11 | pH_normalized | 0.225 | 0.213 | 0.237 |
| Q11 | acid_dissociation_fraction | 0.028 | 0.01 | 0.051 |
| Q11 | precipitation_signal | 0.005 | 0 | 0.02 |
| Q12 | pH_normalized | 0.225 | 0.217 | 0.233 |
| Q12 | acid_dissociation_fraction | 0.028 | 0.013 | 0.046 |
| Q12 | precipitation_signal | 0.005 | 0 | 0.017 |

### Q rationales

- **Q01**: This concentration is sixtyfold below the lowest measured concentration, so this is a genuine low-concentration extrapolation. I used the dilute weak-acid branch anchored by batch 7 rather than extending the empirical logarithmic pH fit, which would be physically implausible here. Extensive dilution should raise the free dissociation fraction and leave precipitation effectively absent; the wide intervals reflect uncertainty in the low-concentration asymptote.

- **Q02**: At 0.00417 M this batch remains sixfold below the measured range but is closer to batch 7 than Q01 is. A dilute weak-acid calculation gives a substantially higher free dissociation fraction than observed in the campaign range, while the precipitation ion product should remain too small to generate more than a near-zero, noise-limited proxy.

- **Q03**: The analytical concentration exactly matches sealed anchor batch 7, which returned 0.22466 normalized pH, 0.02727 dissociation, and zero precipitation at a larger volume. The point predictions stay close to that observation, with a small positive expected precipitation signal because a bounded noisy measurement near zero can be clipped. The smaller absolute scale adds uncertainty but no resolved scale correction.

- **Q04**: At 0.125 M this condition interpolates between batches 8 at 0.075 M and the matched 0.150 M batches 2 and 9. The concentration-dominated account predicts lower pH and more precipitation than batch 8, but slightly higher pH and less precipitation than the 0.150 M pair. Free dissociation is expected to be small and is only weakly resolved relative to assay noise.

- **Q05**: The concentration exactly matches batches 4 and 12, whose normalized pH values were 0.09590 and 0.09450 and whose precipitation signals were 0.09431 and 0.09697. Their agreement supports a concentration-based prediction despite Q05's different absolute volume. The dissociation estimate remains near the lower measurement boundary.

- **Q06**: This is a modest extrapolation above the measured 1.00 M endpoint, where batch 6 returned 0.06702 normalized pH and 0.10798 precipitation. Continuing the observed concentration trend gives a lower pH and a slightly larger precipitation proxy, but the proxy is expected to flatten rather than rise linearly. The intervals are widened because neither the high-concentration activity corrections nor the saturation level were identified.

- **Q07**: This is another 0.500 M scale control, so the central predictions follow batches 4 and 12 and match Q05. Its 0.006 L volume is well below the campaign's 0.040–0.080 L range, so the intervals are wider to allow an unresolved small-scale effect even though the measured same-concentration pairs showed no independent volume dependence.

- **Q08**: At 0.1667 M this condition lies just above the replicated 0.150 M state. Batches 2 and 9 averaged about 0.1520 normalized pH and 0.0435 precipitation, so a small downward pH shift and upward precipitation shift are expected. The free-dissociation channel remains close to its detection boundary and receives a correspondingly asymmetric interval.

- **Q09**: The 0.0625 M concentration interpolates between batch 1 at 0.050 M and batch 8 at 0.075 M. Their final pH and precipitation observations bracket the prediction, while their dissociation measurements indicate a small but nonzero fraction with substantial noise. The volume lies inside the studied volume range, so little additional scale uncertainty is required.

- **Q10**: At 0.040 M this condition lies between anchor batch 7 at 0.025 M and batch 1 at 0.050 M. Dilution should increase free dissociation and normalized pH relative to batch 1 while reducing precipitation toward the near-zero dilute regime. The 0.075 L volume is within the studied range.

- **Q11**: This has the same 0.025 M concentration as batch 7 and Q03, so it receives the same central response. Its much smaller 0.012 L scale was not experimentally covered, and therefore its intervals are wider than those for the anchor rather than applying an unsupported deterministic volume correction.

- **Q12**: This 0.025 M condition closely reproduces the concentration of batch 7 at a volume inside the studied range. The concentration-sufficiency evidence from batches 2 versus 9 and 4 versus 12 supports using the same central values as Q03 and Q11. Its scale is better supported than Q11's, so its prediction intervals are narrower.

Shared rationale:

Predictions use only the sealed campaign and K1 mechanism. Within 0.025–1.00 M, normalized pH was modeled by the observed smooth concentration response, with direct anchors and interpolation taking precedence over a global fit. The precipitation proxy was treated as a monotone bounded response that rises from near zero and progressively flattens. Free dissociation was treated as a noisy, nonnegative weak-acid response that increases upon dilution; its intervals are wider because many campaign estimates were comparable to the 0.006 final-assay noise or were clipped at zero. Same-concentration pairs—batches 2 and 9 at 0.150 M and batches 4 and 12 at 0.500 M—showed no resolved independent amount or volume effect, so equal-concentration queries share central predictions. Extra uncertainty was added for volumes below the studied 0.040–0.080 L range. Q01 and Q02 use the dilute HA dissociation branch, approximately anchored by an effective Ka near 2×10^-5 M from batch 7, rather than an unjustified extrapolation of the empirical log-concentration pH curve. Q06 is a high-concentration extrapolation with widened intervals. All intervals include both model uncertainty and final-assay observation noise and are bounded to the public 0–1 metric ranges.

## K2 — sealed seven-part retrospective

1. Supplied structural claims

A structural prior was supplied, but no instance-specific property dossier or instance prior record was supplied. The prior proposed the local network HA(aq) ⇌ H+(aq) + A−(aq), followed by direct M+(aq) + A−(aq) ⇌ MA(s), with no distinct aqueous MA intermediate.

The acid-dissociation claim was supported qualitatively. Increasing nominal concentration lowered normalized pH, while the dilute anchor, batch 7 at 0.025 M, had the highest resolved final dissociation fraction (0.02727) and normalized pH of 0.22466. The precipitation branch was also supported qualitatively: precipitation signal rose from 0 in batch 7 to 0.10798 in batch 6 at 1.00 M.

The claim that one coupled network can organize all three response channels was supported as a parsimonious account. Removal of free A− into a precipitated branch can reconcile increasing precipitation with small measured free-dissociation fractions.

The specifically direct nature of M+ + A− precipitation was not established. The absence of an aqueous MA intermediate was untested because no species-resolved observable for MA(aq) was available. The source, amount, and activity of M+ were likewise untested. No observation directly contradicted the supplied graph, but “no observed contradiction” is weaker than verification.

There were observations that complicated a simple parameterization but were not treated as topological contradictions. Batch 11 had a dissociation estimate of 0.01366 despite being more concentrated than several zero-boundary batches, and batch 1 changed from 0.03218 on the intermediate pH-meter measurement to 0.00756 on final assay. These discrepancies were acknowledged as evidence that the dissociation channel was noisy and clipped; they were not ignored in order to preserve a monotone law. They did not, by themselves, contradict the reaction graph.

2. Experiments that formed or changed the account

Batch 1 first established a low-concentration, low-precipitation acidic state, but its instrument disagreement discouraged reliance on a single dissociation estimate. Batches 2–6 then established the broad progression toward lower normalized pH and greater precipitation as concentration increased. Batch 6, at 1.00 M, provided the measured high-concentration endpoint: normalized pH 0.06702 and precipitation 0.10798.

Batch 7 changed the account most strongly. At 0.025 M it gave normalized pH 0.22466, dissociation 0.02727, and zero precipitation. It established the dilute regime and became the sealed anchor.

The matched-concentration comparisons changed the causal summary from possible separate loading and dilution effects to a concentration-dominated account. Batches 2 and 9 were both 0.150 M despite twofold differences in amount and volume; their pH values were 0.15319 and 0.15082, and precipitation signals were 0.04466 and 0.04238. Batches 4 and 12 were both 0.500 M; their pH values were 0.09590 and 0.09450, and precipitation signals were 0.09431 and 0.09697. These comparisons supplied the main evidence for using n/V as the shared predictor.

The choice to use water without catalyst and to interpret the responses through acid dissociation and precipitation relied partly on the supplied structural prior. The concentration grid and matched-concentration controls relied on the characterization objective and accumulated observations. Treating nominal concentration as sufficient outside the observed 0.040–0.080 L volume range remained an untested assumption. So did equilibrium attainment without a controlled waiting-time study and the assumption that the precipitation proxy was monotone in precipitated material.

3. Strongest competing explanations

The strongest competing topology is

HA ⇌ H+ + A−,
M+ + A− ⇌ MA(aq),
MA(aq) ⇌ MA(s).

A hidden aqueous ion pair or complex could reproduce the same pH, free-dissociation, and precipitation channels after refitting its association and precipitation constants. The acquired instruments did not expose a species-specific MA(aq) measurement, so this topology cannot be distinguished from direct free-ion precipitation.

The strongest parameter-only alternative retains the supplied topology but permits concentration-dependent activity coefficients, a finite latent M inventory, and a nonlinear proxy calibration. Adjusting Ka, Ksp, activity coefficients, total M, and the mapping from solid amount to precipitation signal could reproduce substantially different quantitative curves without changing any reaction edge.

The evidence distinguishes a concentration-coupled response from a large independent volume effect within the tested range. It does not identify numerical Ka or Ksp, the M balance, activity coefficients, solid amount, the proxy calibration, or whether aqueous MA exists. It also cannot decisively separate true equilibrium precipitation from a slowly forming aggregate that gives the same bounded signal.

4. One additional legal complete experiment

I would prepare 0.0006 mol reagent in 0.024 L water, giving 0.025 M at an intermediate absolute scale not used in the campaign. I would obtain a pH-meter measurement before termination and then terminate and obtain the required final assay. I would not add catalyst, heat, or change solvent, because those interventions would introduce new categorical effects rather than isolate the concentration-sufficiency claim.

This experiment would directly challenge the sealed anchor’s transfer across scale. Agreement with batch 7—approximately 0.225 normalized pH, a resolved dilute dissociation fraction, and near-zero precipitation—would strengthen the claim that concentration, rather than absolute amount or volume, governs this local regime. A reproducible pH or precipitation shift would require adding an absolute-scale, background-inventory, surface, or finite-M term to the account. Agreement in pH and precipitation but disagreement only in dissociation would reinforce the judgment that the dissociation channel is noise-limited. A positive precipitation response well above the near-zero expectation would weaken the proposed dilute non-precipitating regime, although it would still not identify direct versus intermediate precipitation.

No single legal experiment using only the available aggregate instruments could conclusively demonstrate the absence of MA(aq). The proposed experiment is therefore aimed at the most important testable assumption rather than pretending to resolve an unobservable species.

5. Effect of the characterization objective

The objective favored broad mechanistic coverage over operational optimization. The 12 batches spanned 0.025–1.00 M and included two matched-concentration scale comparisons. Every batch received a final assay, and every nonfinal measurement allocation was used for a pH-meter reading. This provided coverage of the dilute, transition, and concentrated regimes.

The main cost was limited replication. There were no exact independent repeats at every condition. Batches 2 versus 9 and 4 versus 12 supplied scale controls and limited repeatability evidence, but they were not exact recipe replicates. More exact replication would have improved local uncertainty estimates, especially for dissociation, at the expense of concentration coverage.

Local identification of Ka, Ksp, or an MA intermediate was not feasible with the available channels, so resources were not concentrated on fitting those constants. No experiments were chosen to improve the native scalar score. In particular, equilibrium_confidence was treated as an environment diagnostic rather than an optimization target or an expression of scientific certainty. Solvent and catalyst screening was also avoided because it would have diluted the loading–dilution characterization and introduced categorical effects that could not be identified with only 12 completed batches.

6. Underused evidence and weak blind predictions

The intermediate pH-meter data were underused. They were collected in every batch, but the sealed account used them mainly as qualitative checks and highlighted only discrepancies such as batch 1. A hierarchical treatment combining intermediate and final measurements could have better separated instrument noise from batch variation. The raw final-assay spectral packets, replicate pH readings, and residual diagnostics were also not fully modeled. They did not reveal the hidden species mapping, but they could have improved observation-error estimates.

The weakest blind predictions are Q01 and Q02. Their concentrations, 0.0004167 and 0.004167 M, are far below the measured 0.025 M lower boundary. Their estimates relied on a conjectural dilute weak-acid branch with an effective Ka near 2×10^-5 M, even though K1 explicitly judged numerical Ka unidentifiable. Their dissociation and pH intervals may therefore be too narrow for the degree of structural extrapolation.

Q06 is also weak because 1.25 M lies above the 1.00 M measured endpoint, and the assumed flattening of precipitation was not independently identified. Q07 and Q11 are weak scale extrapolations because their volumes, 0.006 and 0.012 L, are below the studied 0.040–0.080 L range. Q03 and Q05 also use 0.024 L, so their concentration-matched central estimates depend on extending scale invariance beyond its observed domain.

The common central predictions for Q03, Q11, and Q12, and for Q05 and Q07, faithfully reflected the K1 concentration-sufficiency judgment but understated the possibility of finite background inventory or small-volume effects. Dissociation intervals are generally less reliable than pH intervals because many final dissociation values were near the 0.006 assay-noise scale or clipped at zero. Low precipitation intervals are similarly sensitive to nonnegative clipping.

7. Limits of the anchor, repeatability, robustness, and generalization

Batch 7 is a useful contrastive anchor, not a proven optimum or a complete representation of the world. It is a single 0.025 M batch at 0.080 L. Its zero precipitation value is a bounded noisy observation and does not prove exact absence of solid. Its dissociation value was the largest final value observed, but no exact replicate established its repeatability.

Repeatability is strongest for pH and precipitation at the two matched concentrations. Batches 2 and 9 agreed closely at 0.150 M, and batches 4 and 12 agreed closely at 0.500 M. Acid-dissociation repeatability was substantially poorer: matched conditions could differ between a small positive estimate and the zero boundary. Thus local robustness is channel-specific.

The concentration-dominated account is supported only from 0.025 to 1.00 M, volumes of 0.040–0.080 L, water, no added catalyst, and approximately 297 K. It was not tested across other solvents, catalysts, temperatures, waiting times, mixing conditions, or independently controlled M inventories. It should not be generalized to named real chemicals because the reagent, catalyst formulations, and reaction species were anonymous benchmark entities.

Finally, this is evidence about one frozen bounded synthetic world. The close pH relationship and matched-concentration controls support local interpolation, not universality across worlds. Different hidden constants, activity models, M inventories, or proxy mappings could preserve the same topology while changing all numerical responses. Different worlds could also contain an aqueous complex or a non-equilibrium aggregation pathway. The sealed anchor and K1 account are therefore defensible local evidence, not proof of a unique mechanism, optimal condition, or universal aqueous law.

## EQS — sealed structured mechanism supplement

- Network family: `indeterminate`
- Aqueous intermediate: `indeterminate`
- Selected equations: `acid_dissociation, free_ion_solid_equilibrium`
- Cited source batches: `2, 4, 6, 7, 9, 12`
- Rationale: The source campaign supports acid dissociation coupled to precipitation but does not resolve whether precipitation is direct or proceeds through an aqueous ion pair. Batch 7 at 0.025 M showed relatively high free dissociation (0.02727) and zero precipitation signal, whereas batch 6 at 1.00 M showed low resolved dissociation and a precipitation signal of 0.10798. Same-concentration pairs 2/9 at 0.150 M and 4/12 at 0.500 M also supported a concentration-controlled equilibrium response. These observations are consistent with the common acid-dissociation and free-ion/solid equilibrium equations. However, no species-resolved measurement tested for MA(aq), so the supplied claim that an aqueous intermediate is absent had no observed contradiction but remained unverified. A direct route and a route containing a hidden aqueous ion pair could both reproduce the aggregate channels after parameter refitting.

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean width | Interval score |
|---|---:|---:|---:|---:|
| pH_normalized | 0.00163417 | 1 | 0.0230833 | 0.0230833 |
| acid_dissociation_fraction | 0.00278502 | 1 | 0.0399167 | 0.0399167 |
| precipitation_signal | 0.00432806 | 0.983333 | 0.0235 | 0.0242351 |

## Structural evaluation

Truth family: `direct_free_ion_precipitation`; predicted family: `indeterminate`; abstained: `True`; family correct: `False`; exact equation set correct: `True`; equation-set Jaccard: `1`.

## Response-shape evaluation

Concentration slope MAE `0.00460755` and curvature MAE `0.00714164`. Dilution slope MAE `0.0143483` and curvature MAE `0.0253689`.

## Evidence boundary

K1 was sealed before Q, Q before K2, K2 before EQS, and reference truth was generated only after all 15 EQS responses were sealed. The task is characterization rather than optimization. Numerical residual and equilibrium confidence are environment diagnostics, not agent uncertainty or task scores. Private authentication and raw model process material are excluded.
