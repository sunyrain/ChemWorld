# EQ-E-W03--MisIndexed — final English experiment report

World `EQ-E-W03`; information arm `MisIndexed`; task `entity-conditioned mechanism characterization`; effective status `completed`; result origin `original`.

## Source campaign

The autonomous campaign completed 12/12 batches and 60 recorded operations. Exact replay is `True`; rollbacks: 0.

| Batch | Medium selector | Volume L | Reagent mol | Measurements | pH normalized | Free dissociation | Precipitation signal | Residual |
|---:|---:|---:|---:|---|---:|---:|---:|---:|
| 1 | 0 | 0.03 | 0.003 | ph_meter, final_assay | 0.155554 | 0.010304 | 0.0692188 | 0.00382035 |
| 2 | 1 | 0.03 | 0.003 | ph_meter, final_assay | 0.189323 | 0.0171643 | 0.0247037 | 0 |
| 3 | 2 | 0.03 | 0.003 | ph_meter, final_assay | 0.237598 | 0.00439766 | 0 | 0 |
| 4 | 0 | 0.08 | 0.008 | ph_meter, final_assay | 0.153222 | 0.00885599 | 0.0528078 | 0 |
| 5 | 1 | 0.08 | 0.008 | ph_meter, final_assay | 0.185712 | 0.00251256 | 0.0166218 | 0.00146396 |
| 6 | 2 | 0.08 | 0.008 | ph_meter, final_assay | 0.233432 | 0 | 0.000491304 | 0.000944478 |
| 7 | 0 | 0.03 | 0.012 | ph_meter, final_assay | 0.0927993 | 0 | 0.128462 | 0 |
| 8 | 1 | 0.03 | 0.012 | ph_meter, final_assay | 0.121688 | 0.00253866 | 0.0514159 | 0.00242009 |
| 9 | 2 | 0.03 | 0.012 | ph_meter, final_assay | 0.15423 | 0 | 0.0182092 | 0 |
| 10 | 0 | 0.08 | 0.032 | ph_meter, final_assay | 0.0922488 | 0 | 0.121568 | 0 |
| 11 | 1 | 0.08 | 0.032 | ph_meter, final_assay | 0.122372 | 0.00968634 | 0.0462487 | 0 |
| 12 | 2 | 0.08 | 0.032 | ph_meter, final_assay | 0.153885 | 0 | 0.0236075 | 0 |

### Sealed evidentiary anchor

Batch `10`: Experiment 10 is a useful evidentiary anchor because it tests medium 0 at high loading and larger scale, while its pH and precipitation readouts agree closely with the matched small-scale batch.

## K1 — sealed open mechanistic report

# Mechanistic report

## 1. Scope and experimental basis

I studied selectable medium indices 0, 1, and 2 in 12 completed batches. The design was a balanced 3 × 2 × 2 factorial:

- medium: 0, 1, or 2;
- nominal reagent concentration: 0.10 or 0.40 mol L⁻¹;
- initial liquid volume: 0.030 or 0.080 L.

Each batch received one pH-meter measurement, was terminated, and then received the required final assay. There was no catalyst, heating, quenching, or intentional aging step. Consequently, the report concerns the room-temperature, direct weak-acid/precipitation response of this bounded benchmark, not kinetics or general solvent chemistry. Although the interface supplies familiar material labels, the public material information says that their reaction effects are categorical benchmark effects; I therefore retain the operational labels “medium 0–2.”

The principal quantitative evidence below is the final assay, whose declared standard uncertainties are 0.002 for normalized pH, 0.006 for precipitation signal and acid-dissociation fraction, and 0.004 for equilibrium residual. The pH meter was a useful independent, noisier check, particularly for precipitation.

## 2. Actual observations

The final-assay observations were:

| Batch | Medium | Volume (L) | Reagent (mol) | Nominal C (mol L⁻¹) | pH/14 | Dissociation fraction | Precipitation signal | Residual | Environment diagnostic |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 0.030 | 0.003 | 0.10 | 0.155554 | 0.010304 | 0.069219 | 0.003820 | 0.943498 |
| 2 | 1 | 0.030 | 0.003 | 0.10 | 0.189323 | 0.017164 | 0.024704 | 0 | 0.844913 |
| 3 | 2 | 0.030 | 0.003 | 0.10 | 0.237598 | 0.004398 | 0 | 0 | 0.806557 |
| 4 | 0 | 0.080 | 0.008 | 0.10 | 0.153222 | 0.008856 | 0.052808 | 0 | 0.934534 |
| 5 | 1 | 0.080 | 0.008 | 0.10 | 0.185712 | 0.002513 | 0.016622 | 0.001464 | 0.854672 |
| 6 | 2 | 0.080 | 0.008 | 0.10 | 0.233432 | 0 | 0.000491 | 0.000944 | 0.805555 |
| 7 | 0 | 0.030 | 0.012 | 0.40 | 0.092799 | 0 | 0.128462 | 0 | 0.956372 |
| 8 | 1 | 0.030 | 0.012 | 0.40 | 0.121688 | 0.002539 | 0.051416 | 0.002420 | 0.875964 |
| 9 | 2 | 0.030 | 0.012 | 0.40 | 0.154230 | 0 | 0.018209 | 0 | 0.800205 |
| 10 | 0 | 0.080 | 0.032 | 0.40 | 0.092249 | 0 | 0.121568 | 0 | 0.960194 |
| 11 | 1 | 0.080 | 0.032 | 0.40 | 0.122372 | 0.009686 | 0.046249 | 0 | 0.874294 |
| 12 | 2 | 0.080 | 0.032 | 0.40 | 0.153885 | 0 | 0.023608 | 0 | 0.804368 |

“Environment diagnostic” is the reported equilibrium_confidence channel. In accordance with the measurement contract, I do not treat it as my epistemic confidence or as evidence quality.

Averaging the two scales within each concentration gives:

| Medium | C (mol L⁻¹) | Mean pH/14 | Corresponding pH | Mean precipitation |
|---:|---:|---:|---:|---:|
| 0 | 0.10 | 0.154388 | 2.161 | 0.061013 |
| 1 | 0.10 | 0.187518 | 2.625 | 0.020663 |
| 2 | 0.10 | 0.235515 | 3.297 | 0.000246 |
| 0 | 0.40 | 0.092524 | 1.295 | 0.125015 |
| 1 | 0.40 | 0.122030 | 1.708 | 0.048832 |
| 2 | 0.40 | 0.154057 | 2.157 | 0.020908 |

## 3. Empirical organization of the world

### 3.1 Concentration is the dominant continuous control variable

Let

C = n_reagent / V_initial.

Holding the medium fixed, increasing C fourfold from 0.10 to 0.40 mol L⁻¹ consistently lowered pH and increased precipitation. This occurred at both tested scales.

A compact local interpolation of the pH observations is

pH_normalized(m,C) ≈ A_m − B_m log10(C / 0.10),

where, for media 0, 1, and 2 respectively,

- A = (0.15439, 0.18752, 0.23552),
- B = (0.10275, 0.10877, 0.13530).

This equation is descriptive, not a validated law. It is exactly constrained by only two concentrations and should not be extrapolated far outside 0.10–0.40 mol L⁻¹.

The corresponding pH decreases for a fourfold concentration increase were 0.866, 0.917, and 1.140 pH units. A simple ideal monoprotic weak acid with fixed Ka and negligible coupling would predict approximately 0.301 pH unit for that change because [H+] ≈ sqrt(Ka C). The observed response is therefore much steeper than that elementary model. Possible reasons include precipitation-driven equilibrium shifts, medium-dependent activities or buffering, a concentration-dependent effective equilibrium constant, or an empirical benchmark response that is not intended to reproduce the ideal dilute law.

A similarly convenient interpolation for precipitation is

P(m,C) ≈ Q_m + R_m log10(C / 0.10),

with

- Q = (0.06101, 0.02066, 0.00025),
- R = (0.10630, 0.04679, 0.03432).

Again, two concentration levels cannot distinguish this log-linear expression from a linear-in-C response, a thresholded solubility-product curve, or another monotone function.

### 3.2 The medium exerts a large, reproducible categorical effect

At both concentrations and both scales, the pH ordering was

medium 0 < medium 1 < medium 2,

while the precipitation ordering was

medium 0 > medium 1 > medium 2.

Thus medium 0 produces the most acidic measured state and the strongest solid-formation proxy; medium 2 produces the least acidic state and weakest precipitation; medium 1 is intermediate. These separations are substantially larger than final-assay noise. For example, at 0.10 mol L⁻¹ the scale-averaged normalized-pH gaps are 0.0331 between media 0 and 1 and 0.0480 between media 1 and 2, versus a single-measurement standard uncertainty of 0.002. At 0.40 mol L⁻¹ the corresponding gaps are 0.0295 and 0.0320.

The first three batches formed the initial interpretation: at 0.10 mol L⁻¹ and 0.030 L, batches 1–3 gave normalized pH values of 0.1556, 0.1893, and 0.2376 and precipitation signals of 0.0692, 0.0247, and 0. This immediately indicated a 0 > 1 > 2 precipitation ordering rather than the supplied qualitative selector ordering. Batches 4–6 reproduced it at the larger scale. Batches 7–9 showed that the ordering survived a fourfold increase in concentration, and batches 10–12 reproduced the high-concentration response at larger scale.

The pH-meter observations independently preserved the pH ordering. For example, batches 7–9 produced normalized-pH readings of 0.1002, 0.1203, and 0.1600; batches 10–12 produced 0.0936, 0.1211, and 0.1568. Its precipitation estimates were noisier and sometimes near the zero boundary, so I did not use them to estimate the final precipitation curves.

### 3.3 Concentration relationships largely transfer across scale

The paired 0.030 and 0.080 L batches were intended to distinguish concentration control from amount or vessel-scale control. Across all six matched cells, the mean absolute small-versus-large difference was:

- 0.00195 in normalized pH;
- 0.00707 in precipitation signal.

These are approximately the size expected from the final-assay uncertainties. The largest precipitation scale difference was 0.0164 for medium 0 at 0.10 mol L⁻¹ (batches 1 and 4), but the effect was smaller at high concentration and was not uniform across media. I therefore infer that C and medium identity transfer across the tested 2.67-fold volume change, with no clearly identified independent scale term.

Batch 10 was committed as the final evidentiary anchor because its high-loading, large-scale response closely agrees with the matched small-scale batch 7: normalized pH was 0.09225 versus 0.09280, and precipitation was 0.12157 versus 0.12846. This is evidence of transfer, not a claim that batch 10 is chemically “optimal.”

## 4. Proposed coupled mechanism

My minimal mechanistic representation is:

1. The analytical loading C and medium identity m determine an effective acid activity relation.
2. Acid dissociation produces H+ and a conjugate species A−.
3. A−, or a directly linked species, participates in solid formation.
4. Removing dissolved material into a solid can feed back on acid dissociation through mass balance and Le Châtelier-type coupling.
5. The medium changes at least two effective parameters: acid activity/dissociation behavior and the precipitation threshold or solubility response.

A generic model capable of expressing this is

HA ⇌ H+ + A−,    Ka,eff = a(H+)a(A−)/a(HA),

νA− + M ⇌ S(s),    Ksp,eff(m),

C = [HA] + [A−] + ν[S] + other unobserved reservoirs,

with activity coefficients, Ka,eff, and Ksp,eff allowed to depend on medium. The precipitation signal can be represented as a bounded monotone function of supersaturation:

P = clip(g(IAP/Ksp,eff − 1), 0, 1) + measurement noise.

This structure explains why increasing total loading can simultaneously increase acidity and solid formation. It also allows a medium to promote both responses through separate effective parameters.

However, the observed negative association between pH and precipitation does not establish that low pH causes precipitation. Across the six concentration-by-medium means, a purely descriptive pooled regression is

P ≈ 0.1664 − 0.7627(pH_normalized).

This relation is confounded by both medium and concentration. A latent medium property could independently lower pH and lower solubility. Conversely, precipitation could remove A− and pull further dissociation, thereby increasing H+. The present measurements cannot determine the causal direction.

## 5. Assessment of the supplied qualitative mapping

The supplied local prior associated selector 0 with intermediate acid ionization and solid formation, selector 1 with lower tendencies, and selector 2 with higher tendencies. The observations do not support that selector-to-property assignment.

The repeatable observed response order is 0 > 1 > 2 for precipitation strength and 0, 1, 2 from most to least acidic. If the qualitative identities themselves are correct but their selector indices were permuted, the most economical remapping is:

- observed selector 0 behaves like the prior “higher” entity;
- observed selector 1 behaves like the prior “intermediate” entity;
- observed selector 2 behaves like the prior “lower” entity.

Equivalently, the behavioral identity mapping would be current 0 ← prior 2, current 1 ← prior 0, and current 2 ← prior 1. This is strongly supported for pH and precipitation behavior, but it is still an entity mapping inferred from outputs rather than direct identification of molecular composition.

I cannot independently validate the prior’s “acid ionization tendency” wording from the reported dissociation-fraction channel. Final-assay dissociation estimates ranged only from 0 to 0.0172, many values were clipped at zero, and the declared standard uncertainty was 0.006. They showed no stable medium or concentration ordering. Thus the pH behavior is identifiable, but a separate microscopic degree of dissociation is not.

## 6. Residuals and the environment diagnostic

All final equilibrium residuals were between 0 and 0.00382, no larger than the declared residual uncertainty of 0.004. This is consistent with the environment returning states close to its internal equilibrium manifold, but it does not identify the governing equilibrium equations.

The equilibrium_confidence diagnostic was medium-dependent: its scale-averaged values were approximately 0.939, 0.850, and 0.806 at 0.10 mol L⁻¹ and 0.958, 0.875, and 0.802 at 0.40 mol L⁻¹ for media 0–2. I report this reproducible channel behavior only as an environmental diagnostic. It is not my confidence in the mechanism, not a probability that equilibrium was reached, and not a scientific ranking of the media.

## 7. What is identified

Within the tested domain, the following conclusions are directly supported:

- Medium identity and nominal concentration are the principal identifiable controls.
- Increasing concentration from 0.10 to 0.40 mol L⁻¹ lowers pH and increases precipitation in every medium.
- The categorical response order is robust: medium 0 gives the lowest pH and greatest precipitation, medium 1 is intermediate, and medium 2 gives the highest pH and least precipitation.
- These relationships transfer from 0.030 to 0.080 L with no resolved independent scale effect.
- The supplied selector mapping is inconsistent with the observations; a 2→0, 0→1, 1→2 behavioral remapping reconciles it.
- The simple fixed-Ka ideal weak-acid law is inadequate to describe the magnitude of the concentration response.

## 8. What is not identified

The campaign does not identify:

- molecular species, stoichiometry, activities, pKa values, Ksp values, or solid composition;
- whether precipitation is controlled by A− itself or by another species coupled to it;
- whether the medium effect acts primarily through acid equilibrium, solubility, activity coefficients, buffering, or a direct categorical benchmark offset;
- the direction of causality between acidification and precipitation;
- kinetics or time to equilibrium, because no time series or waiting-time intervention was performed;
- temperature dependence, catalyst dependence, hysteresis, nucleation lag, or reversibility;
- behavior below 0.10 or above 0.40 mol L⁻¹, or beyond 0.030–0.080 L;
- a reliable microscopic dissociation-fraction ordering, because that channel was near its lower boundary relative to noise.

## 9. Reasonable competing explanations

Several mechanisms remain observationally equivalent over this design:

1. **Coupled acid equilibrium and precipitation:** precipitation removes a conjugate species and pulls dissociation forward, jointly lowering pH and increasing solid signal.
2. **Independent medium effects:** the medium separately changes an effective acid constant and a solubility threshold, producing correlated outputs without direct causal coupling between them.
3. **Activity or buffering effects:** measured pH changes mainly through medium-dependent hydrogen activity or buffer capacity, while precipitation responds to total loading through a different pathway.
4. **Thresholded empirical response:** both channels are generated by bounded, medium-conditioned benchmark functions rather than a literal elementary equilibrium mechanism. This is particularly plausible given the synthetic benchmark boundary.
5. **Selector misindexing:** the qualitative entity descriptions are approximately correct but attached to the wrong public selector indices. The observed ordering supports this, although it does not reveal physical identities.

The present data favor a concentration-driven, medium-conditioned coupled response and clearly identify the behavioral remapping. They do not uniquely select among the first four microscopic explanations.

## 10. Testable predictions, explicitly marked as extrapolations

Within 0.10–0.40 mol L⁻¹ and 0.030–0.080 L, I would predict that an untested intermediate concentration preserves the same medium ordering and lies between the reported endpoint responses. The log-linear equations above provide quantitative interpolation, but this is an extrapolation from only two concentration levels.

I would also predict that repeating a matched concentration at another modest scale produces pH differences of only a few thousandths in normalized units and precipitation differences of roughly one hundredth or less, provided the same measurement sequence is used. This is a transfer hypothesis, not evidence for unlimited geometric scaling.

Outside the tested concentration interval, I would not trust linear continuation. A physical precipitation mechanism should eventually show a threshold, curvature, saturation, or depletion-controlled plateau. Additional concentration levels, time courses, and perturbations that independently alter acidity or solubility would be needed to distinguish the competing mechanisms.

## Q — sealed blind predictions

| Query | Metric | Estimate | 80% lower | 80% upper |
|---|---|---:|---:|---:|
| Q01 | pH_normalized | 0.288 | 0.245 | 0.335 |
| Q01 | acid_dissociation_fraction | 0.022 | 0.006 | 0.042 |
| Q01 | precipitation_signal | 0.002 | 0 | 0.018 |
| Q02 | pH_normalized | 0.329 | 0.285 | 0.375 |
| Q02 | acid_dissociation_fraction | 0.014 | 0 | 0.03 |
| Q02 | precipitation_signal | 0.001 | 0 | 0.014 |
| Q03 | pH_normalized | 0.412 | 0.36 | 0.465 |
| Q03 | acid_dissociation_fraction | 0.007 | 0 | 0.022 |
| Q03 | precipitation_signal | 0 | 0 | 0.012 |
| Q04 | pH_normalized | 0.1643 | 0.153 | 0.176 |
| Q04 | acid_dissociation_fraction | 0.006 | 0 | 0.019 |
| Q04 | precipitation_signal | 0.0507 | 0.034 | 0.068 |
| Q05 | pH_normalized | 0.1981 | 0.187 | 0.209 |
| Q05 | acid_dissociation_fraction | 0.004 | 0 | 0.017 |
| Q05 | precipitation_signal | 0.0161 | 0.003 | 0.031 |
| Q06 | pH_normalized | 0.2486 | 0.237 | 0.26 |
| Q06 | acid_dissociation_fraction | 0.002 | 0 | 0.014 |
| Q06 | precipitation_signal | 0 | 0 | 0.012 |
| Q07 | pH_normalized | 0.0744 | 0.059 | 0.09 |
| Q07 | acid_dissociation_fraction | 0.003 | 0 | 0.014 |
| Q07 | precipitation_signal | 0.1437 | 0.122 | 0.166 |
| Q08 | pH_normalized | 0.1029 | 0.087 | 0.119 |
| Q08 | acid_dissociation_fraction | 0.002 | 0 | 0.013 |
| Q08 | precipitation_signal | 0.0571 | 0.04 | 0.075 |
| Q09 | pH_normalized | 0.1302 | 0.113 | 0.148 |
| Q09 | acid_dissociation_fraction | 0.001 | 0 | 0.012 |
| Q09 | precipitation_signal | 0.027 | 0.011 | 0.044 |
| Q10 | pH_normalized | 0.1643 | 0.156 | 0.173 |
| Q10 | acid_dissociation_fraction | 0.006 | 0 | 0.018 |
| Q10 | precipitation_signal | 0.0507 | 0.036 | 0.066 |
| Q11 | pH_normalized | 0.1981 | 0.19 | 0.207 |
| Q11 | acid_dissociation_fraction | 0.004 | 0 | 0.016 |
| Q11 | precipitation_signal | 0.0161 | 0.004 | 0.029 |
| Q12 | pH_normalized | 0.2486 | 0.24 | 0.258 |
| Q12 | acid_dissociation_fraction | 0.002 | 0 | 0.014 |
| Q12 | precipitation_signal | 0 | 0 | 0.011 |

### Q rationales

- **Q01**: This is a far-below-range extrapolation for selector 0. The pH estimate extends the observed log-concentration relationship, while precipitation is expected to be near its lower boundary. Dissociation is allowed to increase at low analytical concentration, but its interval is wide because that channel was poorly resolved.

- **Q02**: The selector-1 estimate preserves its experimentally observed intermediate pH and precipitation behavior. Concentration is far below the studied interval, so model-form uncertainty dominates the prediction interval.

- **Q03**: Selector 2 had the highest pH and precipitation values at the detection boundary in the research batches. Extrapolation to 0.005 M therefore predicts essentially no precipitation, with substantial uncertainty in pH and dissociation.

- **Q04**: The concentration is close to the observed 0.10 M boundary. The estimates are short extrapolations of the selector-0 concentration relationships; the 0.024 L scale lies only slightly below the tested scale range.

- **Q05**: This prediction extends the selector-1 response slightly below 0.10 M. It retains the experimentally stable intermediate entity ordering and includes final-assay noise plus modest model and scale uncertainty.

- **Q06**: The fitted selector-2 precipitation relationship crosses the physical zero boundary just below 0.10 M, so the estimate is clipped to zero. Its pH prediction is a short concentration extrapolation and is more securely ordered than its dissociation estimate.

- **Q07**: This is a moderate extrapolation above the observed 0.40 M endpoint. Selector 0 is predicted to remain the most acidic and precipitation-prone entity, but the interval is widened for possible curvature or saturation.

- **Q08**: The estimate continues the selector-1 log-concentration trend from 0.40 to 0.60 M. The interval allows for both final-assay noise and unobserved high-concentration curvature.

- **Q09**: Selector 2 should retain the highest pH and weakest precipitation response at 0.60 M. The predicted precipitation remains positive because both selector-2 batches at 0.40 M showed a small but reproducible signal.

- **Q10**: This is the scale-control counterpart to Q04. The research campaign found no resolved independent scale effect between 0.030 and 0.080 L, so concentration and selector determine the same point estimate; 0.048 L is interpolative in scale and receives a slightly narrower interval.

- **Q11**: The point estimate matches Q05 because the observed relationships transferred across scale at fixed concentration. The volume is inside the studied scale interval, reducing scale-related uncertainty.

- **Q12**: The estimate matches the selector-2 concentration response used for Q06, with precipitation clipped at its physical lower bound. Scale interpolation supports a narrower pH interval, although the near-zero precipitation and dissociation channels remain censoring-limited.

Shared rationale:

Predictions use the final-assay relationships inferred from the completed 3-selector, 2-concentration, 2-scale campaign. For each selector, normalized pH and precipitation were extended locally as functions of log10 concentration, with all bounded outputs clipped to [0,1]. The experimentally supported entity ordering was retained: selector 0 has the lowest pH and strongest precipitation, selector 1 is intermediate, and selector 2 has the highest pH and weakest precipitation. The 0.048 L controls use the same point estimates as their 0.024 L concentration matches because no independent scale effect was resolved; their intervals are narrower because 0.048 L lies within the tested scale range. Intervals are widest at 0.005 M, which is far outside the observed concentration range, and are moderately widened at 0.60 M for possible curvature or saturation. Acid-dissociation predictions are deliberately conservative because research measurements were near zero, frequently boundary-clipped, and noisy relative to their magnitude.

## K2 — sealed seven-part retrospective

## 1. Initial claims: supported, contradicted, or untested

The initial material packet did contain one substantive task-specific claim: selector 0 was described as intermediate in acid-ionization and solid-formation tendency, selector 1 as lower in both, and selector 2 as higher in both. It was explicitly presented as a qualitative local prior rather than a binding mechanism.

### Solid-formation mapping: contradicted

The precipitation observations repeatedly contradicted the stated selector order. At 0.10 M and 0.030 L, batches 1–3 gave final precipitation signals of 0.0692, 0.0247, and 0 for selectors 0–2. The larger-scale counterparts, batches 4–6, gave 0.0528, 0.0166, and 0.00049. The same 0 > 1 > 2 order remained at 0.40 M in batches 7–9 and 10–12. This was not merely an absence of support for the prior: it was positive counterevidence reproduced across concentration and scale.

K1 therefore proposed the behavioral remapping “current 0 behaves like prior higher, current 1 like prior intermediate, and current 2 like prior lower.” That is still the most economical entity-level interpretation of the precipitation data.

### Acid-ionization mapping: not directly established

The pH observations also followed a stable selector order: selector 0 was most acidic, selector 1 intermediate, and selector 2 least acidic. For example, batches 1–3 gave normalized pH values 0.1556, 0.1893, and 0.2376. This is compatible with the same remapping if lower pH is treated as evidence of a stronger effective acid response.

However, the directly reported acid-dissociation fractions did not provide a reproducible ordering. They were mostly between zero and 0.017, frequently clipped at zero, and comparable to the final-assay standard uncertainty of 0.006. K1 explicitly acknowledged this distinction: pH behavior was identifiable, but a separate microscopic degree of dissociation was not. Thus the initial acid-ionization labels were neither cleanly supported nor cleanly refuted by their nominal measurement channel. Treating the pH ordering alone as a definitive microscopic ionization ranking would overstate the evidence.

### Weak-acid/direct-precipitation framing: broadly compatible, not uniquely verified

The observations supported a coupled response in the broad sense that increasing concentration lowered pH and increased precipitation in all three selectors. They did not prove the elementary reactions or stoichiometry proposed illustratively in K1. No species-resolved evidence established that the conjugate base was the precipitating species, that precipitation pulled dissociation forward, or that a single Ka/Ksp model generated both channels.

### Benchmark and scope claims

The initial packet stated that this was a bounded synthetic benchmark and that familiar material labels should not be interpreted as real-chemistry predictions. That was a scope declaration rather than an experimental hypothesis, and the campaign did not test it. The same is true of the statement that equilibrium_confidence is an environment diagnostic rather than epistemic confidence. I respected that contract and did not reinterpret the diagnostic as a probability of mechanistic correctness.

No task-specific molecular dossier, nominal pKa, solubility product, stoichiometry, or archival quantitative model was supplied. Consequently, there were no such initial quantitative claims to validate.

## 2. Experiments that formed or changed the interpretation

### Batches 1–3: the first decisive entity contrast

Batches 1–3, all at 0.10 M and 0.030 L, genuinely formed the initial entity interpretation. Their monotone pH ordering and strong precipitation ordering immediately conflicted with the supplied selector mapping. Batch 3 was particularly informative because selector 2, described initially as the higher solid-forming entity, returned a final precipitation signal of zero while selector 0 returned 0.0692.

This was the first point at which the prior should be revised rather than merely treated cautiously. The sealed K1 did revise it explicitly.

### Batches 4–6: replication across scale

Batches 4–6 repeated the same concentration and entity contrast at 0.080 L. They changed the interpretation from “possible small-batch ordering” to “ordering that appears transferable across the tested scale change.” They also reduced the plausibility that the first pattern was solely a seeded measurement fluctuation.

### Batches 7–9: concentration dependence

Batches 7–9 raised concentration to 0.40 M at 0.030 L. They established that every selector became more acidic and more precipitation-prone at higher concentration while preserving the entity order. These batches motivated K1’s concentration-conditioned response rather than a pure selector ranking.

They also exposed a mechanistic problem: the pH shifts were much larger than the approximately 0.301-pH-unit change expected from the simplest fixed-Ka dilute weak-acid approximation for a fourfold concentration increase. That observation motivated competing explanations involving precipitation feedback, activities, buffering, or a benchmark-specific empirical response.

### Batches 10–12: high-concentration scale transfer

Batches 10–12 supplied the second scale check at 0.40 M. Batch 10 closely matched batch 7: normalized pH was 0.09225 versus 0.09280 and precipitation was 0.12157 versus 0.12846. This was the main reason batch 10 was sealed as the evidentiary anchor.

### What determined the design

The balanced 3 × 2 × 2 design was chosen before observing outcomes. Its selector coverage came directly from the research goal and the supplied qualitative mapping. The two volumes came from the request to assess transfer across scale. The concentration endpoints, 0.10 and 0.40 M, were not supplied by prior evidence; they were design guesses chosen to create a useful loading contrast while remaining within stock and per-operation limits.

Likewise, using one pH-meter measurement followed by a final assay in every batch was a pragmatic attempt to obtain an independent check and use the available intermediate-measurement budget evenly. There was no prior evidence that one pH-meter sample per batch was the maximally informative allocation. No adaptive concentration was added after a possible precipitation threshold became visible because the 12-batch matrix had already been fixed and preserving the design was preferable to outcome-driven alteration.

## 3. Current competing mechanisms and what the campaign distinguishes

The leading explanations remain:

1. **Precipitation-coupled acid equilibrium.** A conjugate or linked species enters the solid phase, and its removal shifts the acid equilibrium, producing more H+ and a lower pH.
2. **Two independent medium-conditioned effects.** Each selector independently changes an effective acid response and a precipitation threshold. Their correlation need not imply direct causal coupling.
3. **Activity or buffering control.** Medium-dependent hydrogen activity or buffer capacity governs measured pH, while a separate solubility or aggregation process governs precipitation.
4. **A bounded empirical benchmark function.** The outputs may be generated by categorical, concentration-dependent response functions that need not correspond to one elementary thermodynamic mechanism.
5. **Selector misindexing.** The qualitative entity descriptions may be approximately correct but attached to the wrong public selector indices.

The campaign distinguishes several empirical facts well: the public selector mapping for precipitation is wrong; selector order transfers across the two tested concentrations and scales; concentration affects both pH and precipitation; and a scale term is not required within 0.030–0.080 L at the available precision.

It does not distinguish explanations 1–4. All can generate lower pH and more precipitation at higher concentration. The pooled negative pH–precipitation association reported in K1 is confounded by selector and concentration and therefore cannot determine causal direction. The experiment also cannot show whether the apparent misindexing is a literal index permutation or merely a prior whose qualitative property assignments were wrong.

The acid-dissociation channel does little to resolve these mechanisms because it was near its lower boundary. The near-zero equilibrium residuals show consistency with the environment’s internal state calculation but do not reveal its equations.

## 4. One additional complete experiment I would choose

I would choose selector 0 at 0.020 M, using 0.050 L solvent and 0.0010 mol reagent. I would preserve the established sequence: one pH-meter measurement, terminate, then final assay. I would not add heating, catalyst, or waiting because introducing a new control variable in the sole additional experiment would make comparison with the original matrix less direct.

This condition is aimed at the largest unresolved model-form question. K1’s log-linear precipitation interpolation for selector 0 crosses the physical zero boundary near 0.027 M. A smooth power-law continuation from the 0.10 and 0.40 M observations instead predicts a small but clearly nonzero precipitation response near 0.020 M. Selector 0 is preferable because it had the strongest signal and therefore offers the best chance to distinguish a threshold from a smooth tail.

Possible outcomes would alter the interpretation as follows:

- **Precipitation indistinguishable from zero:** this would support a thresholded or clipped precipitation response and weaken smooth power-law continuation. It would also make the near-zero Q01 prediction directionally more plausible.
- **A reproducible precipitation signal around 0.02–0.03:** this would support a smooth low-concentration tail and show that the log-linear clipped model used for the blind low-concentration predictions was too aggressive.
- **A signal substantially above 0.03:** this would imply strong curvature or a low-concentration mechanism not represented by either interpolation and would substantially widen uncertainty for Q01–Q06.
- **Normalized pH near 0.226:** this would support local continuation of K1’s selector-0 log-concentration relationship. A large deviation would demonstrate curvature and undermine the very-low-concentration pH extrapolations.
- **A clearly elevated acid-dissociation fraction, for example well above 0.02 relative to assay noise:** this would support concentration-dependent fractional dissociation. Another near-zero result would reinforce the conclusion that the channel is not identifiable in this regime or is not thermodynamically linked to pH in the assumed way.

This proposed experiment is hypothetical only; it has not been executed.

## 5. Tradeoff between mechanistic identifiability and operational score

The research goal emphasized entity mapping, transfer, evidence boundaries, and competing mechanisms rather than optimization. The balanced design followed that priority. Eight of the twelve later batches served as cross-entity or cross-scale comparisons rather than attempts to concentrate resources in the apparently favorable selector-0/high-concentration region.

That choice sacrificed operational score. After batches 1–3 already suggested that selector 0 was stronger on the scored precipitation and environment-diagnostic channels, an optimizer would likely have allocated more batches to selector 0 and high concentration. Instead, selectors 1 and 2 were retained at both concentrations and scales because they were necessary to test the mapping and transfer claims.

There was also a tradeoff within identifiability. With only 12 batches, using two scales for every selector and concentration left only two concentration levels. This was adequate to show direction and scale transfer but inadequate to identify curvature, thresholds, or a mechanistic law. In retrospect, one intermediate or low concentration per selector might have been more valuable for functional-form identification than duplicating both endpoint concentrations at both scales. The chosen matrix favored clean factorial attribution over richer concentration resolution.

There is no clear case where I knowingly sacrificed identifiability to improve score. The high concentration endpoint did yield relatively strong selector-0 scores, but it was selected as a contrast before those outcomes were known. Conversely, I did sacrifice potential score by preserving balanced coverage.

Using the public scoring formula after the campaign, batch 10 has the highest calculated sampled score, about 0.45955, narrowly above batch 7 at about 0.45892. That difference is only about 0.00063 and is far smaller than the uncertainty implied by noisy components. Moreover, K1 correctly treated the scalar score as a diagnostic rather than the research objective.

## 6. Underused evidence and weaknesses in the blind predictions

### Evidence that was difficult to exploit

The intermediate pH-meter pH measurements were useful and supported the selector ordering, but their precipitation estimates had a declared uncertainty of 0.02 and often disagreed appreciably with the final assay. I used them qualitatively rather than fitting them jointly. A hierarchical measurement model could have used them more systematically, although the small sample and boundary clipping would still limit inference.

The final spectral artifacts and peak-level information were not analyzed in depth. This was partly because hidden mechanism-to-species mapping was unavailable and the public channels already supplied calibrated estimates. Peak patterns might have helped assess internal consistency, but they could not securely identify chemical species under the observation contract.

The equilibrium_confidence channel showed a strong selector pattern, approximately 0.94, 0.85, and 0.81 at low concentration, but its contract explicitly forbade interpreting it as confidence. It influenced the formal score but was intentionally not used to strengthen mechanistic claims.

The acid-dissociation channel was the most scientifically relevant underused evidence, but it was also the hardest to use: values were small, noisy, and boundary-clipped. K1 was appropriately cautious, whereas the sealed blind predictions nevertheless assigned concentration- and selector-dependent point estimates. Those estimates were much more speculative than the pH estimates.

The scale pairs were treated as evidence of no resolved scale effect, but there was only one batch per exact selector–concentration–volume cell. Thus scale and independent realization noise were not fully separable. The blind queries also omit the intermediate pH-meter sample used in every research batch. That sample removed only 30 µL and is unlikely to matter greatly, but it is a protocol difference that the prediction rationales did not emphasize.

### Least reliable blind predictions

Q01–Q03 are the least reliable overall. Their concentration, 0.005 M, is twentyfold below the lowest studied concentration. K1 explicitly said that it would not trust linear continuation outside 0.10–0.40 M. The sealed Q rationales acknowledged that these were far-below-range extrapolations, but the numerical 80% pH intervals may still be too narrow given unconstrained curvature, buffering, thresholds, and lower-bound effects.

Their acid-dissociation predictions are particularly weak. The points 0.022, 0.014, and 0.007 were based on a qualitative expectation that fractional dissociation could rise at low concentration, not on a reliably fitted campaign relationship. The associated intervals may not cover alternative benchmark behaviors in which the channel remains near zero or changes non-monotonically.

Q07–Q09 at 0.60 M are less extreme but still extrapolate above the observed range. Their precipitation intervals may be too narrow if saturation, depletion, or a new curvature begins above 0.40 M. Q09 is especially sensitive because selector 2 had small signals near the boundary.

Q06 and Q12 predict exactly zero precipitation at 0.08 M after clipping the fitted log-linear curve. That sharp boundary is a model artifact, not an observed threshold. Their upper bounds of 0.012 and 0.011 may be too narrow if precipitation instead has a smooth low-concentration tail.

Q10–Q12 received narrower intervals because 0.048 L lies within the studied scale range. That is defensible for interpolation, but probably overstates how well scale uncertainty was known: the original design did not contain exact experimental replicates, and only two scales were tested.

These weaknesses are consistent with K1’s stated evidence boundaries but reveal a tension in the sealed Q submission. K1 warned against trusting continuation outside the studied concentration interval; the prediction task nevertheless required numerical answers. I acknowledged extrapolation in the rationales, but I converted structural uncertainty into intervals that were likely too quantitative and possibly too narrow. No prediction truth has been supplied, so these are prospective criticisms rather than post hoc explanations of prediction errors.

## 7. Limitations of the sealed recommendation

Batch 10 was selected because it was an evidentiary anchor: selector 0 at 0.40 M and 0.080 L closely reproduced the corresponding small-scale behavior of batch 7. It was not selected on the basis of a demonstrated global optimum.

Post-campaign calculation shows that batch 10 has the highest scalar score among the twelve sampled batches, but only narrowly. “Highest among sampled batches” means exactly that: among three selectors, two concentrations, and two scales, with one realization per cell, its observed score was largest. It does not prove that 0.40 M is the best concentration, that 0.080 L is the best scale, or that selector 0 remains best outside this world and measurement realization. The score itself is also a diagnostic rather than the scientific objective.

### Repeatability

Repeatability should be tested with multiple independent batches using the exact batch-10 recipe and operation sequence. Replicates should report the full joint distribution of pH, precipitation, dissociation, residual, environment diagnostic, and score rather than only whether the mean score remains high. Exact repeats are necessary because batches 7 and 10 differed slightly and there were no true same-scale replicates.

### Local robustness

A local robustness study should vary concentration on both sides of 0.40 M, for example 0.30, 0.40, and 0.50 M, while holding selector and scale fixed. A corresponding modest volume variation would test whether the apparent concentration control persists. Robustness requires a plateau or predictable local response, not a single narrow maximum caused by measurement noise.

The operation sequence should also be checked. The original batches included a destructive pH-meter sample before termination; a deployment recipe without that sample is not exactly identical even if the removed volume is small.

### Cross-material scope

Selectors 1 and 2 were measured under matched conditions and performed differently, so the batch-10 result is plainly material-conditioned. The recommendation cannot be transferred to another selector by concentration scaling alone. Cross-material generalization would require matched local studies for each selectable entity and should not assume that selector 0’s effective response parameters apply elsewhere.

### Cross-world scope

The material packet describes categorical benchmark effects and hidden mappings. A different world, seed, or benchmark instance could change selector mapping, noise realization, or response parameters. Cross-world validity would require preregistered replay across independently initialized worlds, retaining failures and testing whether the same qualitative order and local response persist.

Accordingly, the defensible claim is: batch 10 was a strong within-campaign anchor and the highest observed sampled score under the public formula. The indefensible stronger claim would be that its recipe has been proven globally optimal, universally repeatable, transferable to other materials, or valid in other worlds.

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean width | Interval score |
|---|---:|---:|---:|---:|
| pH_normalized | 0.0232207 | 0.633333 | 0.0419167 | 0.133853 |
| acid_dissociation_fraction | 0.0132848 | 0.683333 | 0.01875 | 0.0842693 |
| precipitation_signal | 0.003315 | 0.983333 | 0.0246667 | 0.0249135 |

## Entity-map and scale-transfer evaluation

| Concentration M | Pairwise entity-contrast MAE |
|---:|---:|
| 0.005 | 0.03335 |
| 0.08 | 0.00604811 |
| 0.6 | 0.00412631 |

| Selector | Same-concentration scale-gap MAE |
|---:|---:|
| 0 | 0.0012684 |
| 1 | 0.00179311 |
| 2 | 0.00303772 |

## Evidence boundary

The participant received exactly K1, Q, and K2, in that order. K1 is the primary open-form entity-mechanism artifact. No candidate property vector, numerical entity constant, hidden truth, or score was shown before K2 sealed. Reference truth was generated only after all 15 K2 responses sealed. The common direct weak-acid/free-ion-precipitation topology was fixed across worlds and arms; the task was entity mapping, not operation optimization.
