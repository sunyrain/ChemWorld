# EQ-E-W01--Opaque — final English experiment report

World `EQ-E-W01`; information arm `Opaque`; task `entity-conditioned mechanism characterization`; effective status `completed`; result origin `original`.

## Source campaign

The autonomous campaign completed 12/12 batches and 60 recorded operations. Exact replay is `True`; rollbacks: 0.

| Batch | Medium selector | Volume L | Reagent mol | Measurements | pH normalized | Free dissociation | Precipitation signal | Residual |
|---:|---:|---:|---:|---|---:|---:|---:|---:|
| 1 | 0 | 0.04 | 0.005 | ph_meter, final_assay | 0.139307 | 0.0241444 | 0.0686443 | 0.00113889 |
| 2 | 0 | 0.04 | 0.01 | ph_meter, final_assay | 0.118355 | 0.000112726 | 0.0796079 | 0.00282557 |
| 3 | 0 | 0.04 | 0.02 | ph_meter, final_assay | 0.0998924 | 0.00472282 | 0.0805738 | 0 |
| 4 | 0 | 0.08 | 0.02 | ph_meter, final_assay | 0.12076 | 0.0118461 | 0.075069 | 0 |
| 5 | 1 | 0.04 | 0.005 | ph_meter, final_assay | 0.161185 | 0 | 0.0444157 | 0.00114421 |
| 6 | 1 | 0.04 | 0.01 | ph_meter, final_assay | 0.122932 | 0.00584894 | 0.0758751 | 0 |
| 7 | 1 | 0.04 | 0.02 | ph_meter, final_assay | 0.0938701 | 0 | 0.100187 | 0 |
| 8 | 1 | 0.08 | 0.02 | ph_meter, final_assay | 0.129312 | 0.000431235 | 0.0543316 | 0.0054806 |
| 9 | 2 | 0.04 | 0.005 | ph_meter, final_assay | 0.223986 | 0.000967255 | 0.0019307 | 0 |
| 10 | 2 | 0.04 | 0.01 | ph_meter, final_assay | 0.178631 | 0.0129083 | 0.00618257 | 0.00891589 |
| 11 | 2 | 0.04 | 0.02 | ph_meter, final_assay | 0.14191 | 0 | 0.00709679 | 0.00110037 |
| 12 | 2 | 0.08 | 0.02 | ph_meter, final_assay | 0.179457 | 0 | 0.0110135 | 0 |

### Sealed evidentiary anchor

Batch `10`: Central 0.25 mol/L loading in medium 2; it anchors both the matched-concentration cross-medium comparison and the twofold-scale transfer check against batch 12.

Complete sanitized agent-visible scientific I/O: [trajectory](trajectory.jsonl). Every attempted operation is retained in order; private provider events, credentials, session identifiers, usage accounting, and evaluator-only state are excluded.

## K1 — sealed open mechanistic report

# Mechanistic report

## 1. Scope and experimental design

I completed 12 closed batches at approximately 297.14 K and ambient pressure. No catalyst, heating, waiting period, or kinetic perturbation was used. Each batch contained one of three medium selectors, anonymous here as M0, M1, and M2. Their public selector labels were Water, Ethanol, and Acetonitrile, respectively, but the material information explicitly states that their runtime effects are categorical benchmark effects. Consequently, this report does not interpret the results as predictions about real water, ethanol, or acetonitrile chemistry.

For each medium I tested nominal reagent concentration C = n/V at 0.125, 0.250, and 0.500 mol L^-1 using 0.040 L batches. I also tested 0.250 mol L^-1 at twice the physical scale, 0.020 mol in 0.080 L. Every batch received one intermediate pH-meter measurement, was terminated, and then received the required final assay. The final assay is my primary quantitative evidence because its declared standard deviations were 0.002 for normalized pH, 0.006 for acid-dissociation fraction, 0.006 for precipitation signal, 0.004 for equilibrium residual, and 0.006 for the environment's equilibrium-confidence diagnostic.

The normalized pH observable is pH/14. Concentrations below are nominal preparation concentrations before the very small measurement samples were removed.

## 2. Final-assay observations

| Batch | Medium | Volume (L) | Reagent (mol) | C (mol L^-1) | pH/14 | Dissociation fraction | Precipitation signal | Equilibrium residual | Environment diagnostic |
|---:|:---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | M0 | 0.040 | 0.005 | 0.125 | 0.139307 | 0.024144 | 0.068644 | 0.001139 | 0.968515 |
| 2 | M0 | 0.040 | 0.010 | 0.250 | 0.118355 | 0.000113 | 0.079608 | 0.002826 | 0.957356 |
| 3 | M0 | 0.040 | 0.020 | 0.500 | 0.099892 | 0.004723 | 0.080574 | 0.000000 | 0.943519 |
| 4 | M0 | 0.080 | 0.020 | 0.250 | 0.120760 | 0.011846 | 0.075069 | 0.000000 | 0.948803 |
| 5 | M1 | 0.040 | 0.005 | 0.125 | 0.161185 | 0.000000 | 0.044416 | 0.001144 | 0.881785 |
| 6 | M1 | 0.040 | 0.010 | 0.250 | 0.122932 | 0.005849 | 0.075875 | 0.000000 | 0.937905 |
| 7 | M1 | 0.040 | 0.020 | 0.500 | 0.093870 | 0.000000 | 0.100187 | 0.000000 | 0.948230 |
| 8 | M1 | 0.080 | 0.020 | 0.250 | 0.129312 | 0.000431 | 0.054332 | 0.005481 | 0.933980 |
| 9 | M2 | 0.040 | 0.005 | 0.125 | 0.223986 | 0.000967 | 0.001931 | 0.000000 | 0.805379 |
| 10 | M2 | 0.040 | 0.010 | 0.250 | 0.178631 | 0.012908 | 0.006183 | 0.008916 | 0.786950 |
| 11 | M2 | 0.040 | 0.020 | 0.500 | 0.141910 | 0.000000 | 0.007097 | 0.001100 | 0.798616 |
| 12 | M2 | 0.080 | 0.020 | 0.250 | 0.179457 | 0.000000 | 0.011013 | 0.000000 | 0.799508 |

The corresponding final-assay pH values were approximately 1.95, 1.66, 1.40, and 1.69 for M0; 2.26, 1.72, 1.31, and 1.81 for M1; and 3.14, 2.50, 1.99, and 2.51 for M2, in increasing batch order within each medium.

The intermediate pH-meter readings generally supported the final pH pattern. For example, its normalized-pH readings for M2 were 0.21934, 0.18531, 0.14071, and 0.17823 in batches 9-12, compared with final values 0.22399, 0.17863, 0.14191, and 0.17946. Intermediate precipitation estimates were substantially noisier, as expected from their declared standard deviation of 0.020, and I therefore do not use them to define the precipitation relationship.

## 3. Empirical mechanism

### 3.1 Medium-conditioned acidity response

The clearest transferable relationship is a medium-specific, approximately log-linear dependence of normalized pH on nominal concentration:

pH_normalized(C, M) approximately equals A_M - s_M log10(C / 0.125).

Using the observed 0.125 and 0.500 mol L^-1 endpoints gives:

- M0: A = 0.13931 and s = 0.06547.
- M1: A = 0.16118 and s = 0.11181.
- M2: A = 0.22399 and s = 0.13633.

This simple endpoint relationship also predicts the central concentration reasonably well. At 0.250 mol L^-1 it predicts approximately 0.11960, 0.12753, and 0.18295 for M0-M2. The averages of the two observed scales at that concentration were 0.11956, 0.12612, and 0.17904, respectively.

Thus, concentration increases acidity in every medium, but it does not do so through one universal curve plus a fixed medium offset. The concentration response itself depends on medium identity. M2 has the highest normalized pH throughout the tested interval, but its curve is also the steepest; its separation from M0 shrinks as concentration increases. The M1 curve is intermediate at low concentration and crosses to slightly lower pH than M0 at 0.500 mol L^-1. This crossing is direct evidence for a medium-by-concentration interaction.

An equivalent purely empirical representation is

[H+]_effective proportional to C^gamma_M,

with gamma approximately 14s: 0.92 for M0, 1.57 for M1, and 1.91 for M2. Here [H+]_effective means the hydrogen activity implied by the pH channel, not a measured stoichiometric hydrogen concentration. These exponents summarize the bounded data; they should not be treated as fundamental reaction orders.

A textbook ideal dilute monoprotic weak acid would give pH = 0.5(pKa - log10 C), corresponding to s = 1/28 = 0.0357 in normalized units. All three observed endpoint slopes are steeper, especially for M1 and M2. Therefore, one constant pKa with ideal activities is not an adequate complete explanation of this world over 0.125-0.500 mol L^-1. Effective activity coefficients, medium buffering, precipitation coupling, concentration-dependent speciation, or benchmark calibration effects must contribute if the pH channel is interpreted chemically.

### 3.2 Direct-precipitation response

Precipitation is even more strongly entity-conditioned:

- M0 produced a moderate and nearly concentration-insensitive final signal: 0.06864 at 0.125 M, 0.07734 averaged across the two 0.250 M scales, and 0.08057 at 0.500 M.
- M1 produced a strongly concentration-dependent signal: 0.04442 at 0.125 M, 0.06510 averaged at 0.250 M, and 0.10019 at 0.500 M.
- M2 remained near the lower boundary throughout: 0.00193 at 0.125 M, 0.00860 averaged at 0.250 M, and 0.00710 at 0.500 M.

A useful qualitative process model is therefore:

1. Medium identity sets both an effective acid-response function and a precipitation propensity.
2. Increasing reagent concentration raises effective hydrogen activity in all three media.
3. In M1, increasing concentration also strongly increases precipitation.
4. M0 has an already appreciable precipitation channel whose additional concentration dependence is weak over this interval.
5. M2 strongly suppresses the observable precipitation channel while retaining a pronounced concentration response in pH.

A compact pseudo-model would be:

pHn = A[M] - s[M] * log10(C/C0) + scale_term[M] + error_pH
precip = clip(u[M] + v[M] * log10(C/C0) + interaction[M,C] + scale_term_P[M] + error_P, 0, 1)

where C0 = 0.125 mol L^-1. The acidity relation is well supported in the tested range. The precipitation expression is only a structural description: four observations per medium are insufficient to identify a unique functional form, and M2 is close to the lower boundary.

### 3.3 Coupling between acidity and precipitation

Across the whole campaign, lower pH often accompanies more precipitation: M2 has both the highest pH and the least precipitation, while increasing concentration in M1 lowers pH and raises precipitation. Nevertheless, precipitation is not a single-valued function of pH. M0 and M1 can have similar pH around 0.25 M while showing different precipitation behavior, and their concentration trends differ.

The supported conclusion is therefore a shared medium-conditioned coupling, not a demonstrated direction of causation. Plausible causal structures include:

- precipitation removes one dissolved form and shifts the acid equilibrium;
- acid state controls formation of the precipitating form;
- medium identity independently changes acid activity and solid formation, creating correlation without direct causal feedback;
- all three effects occur together.

The current interventions changed concentration and medium simultaneously with respect to both responses; they did not selectively manipulate precipitation at fixed chemical activity. Directionality is consequently not identifiable.

### 3.4 Scale transfer

The twofold scale comparisons at fixed nominal concentration provide a limited test of transfer:

- M0, batches 2 and 4: normalized-pH difference +0.00241 and precipitation difference -0.00454 at larger scale.
- M1, batches 6 and 8: normalized-pH difference +0.00638 and precipitation difference -0.02154 at larger scale.
- M2, batches 10 and 12: normalized-pH difference +0.00083 and precipitation difference +0.00483 at larger scale.

M0 and M2 transfer well within the resolution of this single-pair design. M1 shows a possible scale or mixing effect: the larger batch is less acidic and has less precipitation. Relative to final-assay noise alone, those M1 differences are around two combined standard deviations, so they are noteworthy. However, each scale was represented by only one batch, meaning batch variation and scale are confounded. I regard the M1 scale effect as a testable warning rather than an established law.

Batch 10 was selected as the final-recommendation anchor because it is the central 0.250 mol L^-1 M2 condition, participates in both the cross-medium comparison and the twofold-scale comparison with batch 12, and contains nonzero final estimates for both dissociation and precipitation. Selection as an anchor is not an optimization claim.

## 4. How the interpretation developed

Batch 1 established that M0 combined a low pH with a moderate precipitation signal. Batches 2 and 3 then showed a systematic concentration-dependent pH decline but little additional precipitation, arguing against one common concentration response for both observables. Batch 4 showed that the M0 relationship approximately transferred to twice the volume.

Batch 5 initially suggested that M1 was less acidic and less precipitation-prone than M0 at low concentration. Batches 6 and 7 changed that simple offset interpretation: M1's pH fell more steeply and its precipitation rose more strongly, ultimately exceeding M0 precipitation at 0.500 M. This forced the interpretation from a medium ranking to a medium-by-concentration interaction. Batch 8 raised the possibility that the M1 coupling also depends on physical scale.

Batch 9 revealed a qualitatively distinct M2 regime: much higher pH and precipitation close to zero. Batches 10 and 11 confirmed that M2 retained its low-precipitation character across concentration while its pH responded strongly. Batch 12 reproduced the central-concentration pH at twice the scale and kept precipitation near the lower boundary. These observations support treating M2 as a different response class, not merely a shifted version of M0 or M1.

## 5. Acid-dissociation fraction and diagnostics

The reported final acid-dissociation fractions were small, irregular, and frequently exactly zero. Apart from batch 1 at 0.02414, all estimates were at or below 0.01291, close to the assay's declared 0.006 standard deviation and subject to the observable's zero boundary. They did not vary monotonically with concentration or medium.

I therefore do not infer a reliable dissociation-fraction law from this channel. In particular, inserting nominal total reagent concentration and measured pH into a simple alpha = [H+]/C mass-balance formula would not reproduce the reported dissociation values. That mismatch could reflect unobserved stoichiometry, activities, other acid sources or sinks, precipitation, or the benchmark channel definition. It is not legitimate to select one explanation without additional measurements.

All final equilibrium residuals were small, from zero to 0.00892. This is compatible with the environment returning internally settled states, but it does not prove a particular chemical equilibrium model. The reported equilibrium-confidence values are an environment diagnostic, not my epistemic confidence. They were high for M0, generally high but variable for M1, and approximately 0.79-0.81 for M2. I record this entity dependence but do not use the diagnostic as a scientific response or as evidence that one medium is intrinsically better.

## 6. Entity mapping

The experimentally supported mapping within this bounded world is:

- M0: moderate-to-high effective acidity, moderate precipitation already present at low concentration, shallow precipitation response, and comparatively shallow pH response.
- M1: pH and precipitation are highly concentration-sensitive; low concentration gives less acidity and precipitation than M0, whereas high concentration gives slightly greater acidity and more precipitation than M0. Possible scale sensitivity remains unresolved.
- M2: substantially lower effective acidity at a given concentration, a steep pH response to concentration, and precipitation suppressed near the measurement floor.

No task-specific property dossier or qualitative mechanism-to-species mapping was supplied. Thus there was no independent proposed chemical identity map to confirm or falsify. Public selector names alone do not authorize attributing these effects to real-solvent dielectric constants, proticity, or solubility properties.

## 7. Applicability and evidence boundaries

The empirical relationships are supported only for uncatalyzed, unheated, nominally immediate measurements near 297 K, volumes of 0.040-0.080 L, and nominal reagent concentrations of 0.125-0.500 mol L^-1. They should not be extrapolated to dilution below 0.125 M, concentrations above 0.500 M, other temperatures, catalysts, reaction times, or other medium selectors.

The log-linear pH equations interpolate the tested range well, but extrapolation could generate physically incorrect values or miss saturation, buffering transitions, phase changes, or new species. The precipitation model is less certain, especially for M2 because its signal lies near the lower boundary. No conclusion about induction time, nucleation kinetics, crystal identity, particle size, or equilibrium solubility is possible because none was measured.

There were no same-condition independent replicates. The two 0.250 M observations per medium differ in physical scale, so they cannot simultaneously provide a clean replicate variance and an unconfounded scale effect. Instrument standard deviations quantify declared measurement noise, not all batch-to-batch process variability.

## 8. Reasonable competing explanations

Several mechanisms remain observationally equivalent:

1. Medium-specific effective acid constants or activity coefficients, combined with separate medium-specific solubility thresholds.
2. A precipitation-coupled acid equilibrium in which removal of a dissolved species shifts proton release or uptake.
3. Medium-specific buffering or an unobserved acid/base reservoir, with precipitation responding independently to concentration.
4. Concentration-dependent association or multiple acid states that make a one-pKa model inadequate.
5. Transport or mixing effects, particularly for the possible M1 scale difference.
6. Channel-specific benchmark calibration and zero clipping, especially for dissociation fraction and the near-zero M2 precipitation signal.

The data identify reproducible effective input-output relationships, especially the entity-conditioned pH curves and the distinct precipitation patterns. They do not identify molecular species, pKa, Ksp, precipitation stoichiometry, activity coefficients, or the direction of acid-precipitation causality. Those distinctions would require interventions or observables not present in the sealed campaign.

## Q — sealed blind predictions

| Query | Metric | Estimate | 80% lower | 80% upper |
|---|---|---:|---:|---:|
| Q01 | pH_normalized | 0.231 | 0.18 | 0.29 |
| Q01 | acid_dissociation_fraction | 0.04 | 0 | 0.12 |
| Q01 | precipitation_signal | 0.041 | 0.008 | 0.085 |
| Q02 | pH_normalized | 0.317 | 0.235 | 0.405 |
| Q02 | acid_dissociation_fraction | 0.012 | 0 | 0.08 |
| Q02 | precipitation_signal | 0.003 | 0 | 0.04 |
| Q03 | pH_normalized | 0.415 | 0.32 | 0.52 |
| Q03 | acid_dissociation_fraction | 0.012 | 0 | 0.08 |
| Q03 | precipitation_signal | 0.001 | 0 | 0.025 |
| Q04 | pH_normalized | 0.151 | 0.134 | 0.169 |
| Q04 | acid_dissociation_fraction | 0.012 | 0 | 0.045 |
| Q04 | precipitation_signal | 0.067 | 0.043 | 0.092 |
| Q05 | pH_normalized | 0.18 | 0.148 | 0.213 |
| Q05 | acid_dissociation_fraction | 0.004 | 0 | 0.035 |
| Q05 | precipitation_signal | 0.037 | 0.006 | 0.078 |
| Q06 | pH_normalized | 0.25 | 0.227 | 0.275 |
| Q06 | acid_dissociation_fraction | 0.004 | 0 | 0.035 |
| Q06 | precipitation_signal | 0.001 | 0 | 0.022 |
| Q07 | pH_normalized | 0.095 | 0.081 | 0.109 |
| Q07 | acid_dissociation_fraction | 0.004 | 0 | 0.025 |
| Q07 | precipitation_signal | 0.082 | 0.058 | 0.108 |
| Q08 | pH_normalized | 0.085 | 0.068 | 0.103 |
| Q08 | acid_dissociation_fraction | 0.002 | 0 | 0.025 |
| Q08 | precipitation_signal | 0.108 | 0.073 | 0.145 |
| Q09 | pH_normalized | 0.131 | 0.113 | 0.15 |
| Q09 | acid_dissociation_fraction | 0.002 | 0 | 0.025 |
| Q09 | precipitation_signal | 0.008 | 0 | 0.028 |
| Q10 | pH_normalized | 0.153 | 0.136 | 0.171 |
| Q10 | acid_dissociation_fraction | 0.012 | 0 | 0.045 |
| Q10 | precipitation_signal | 0.063 | 0.04 | 0.089 |
| Q11 | pH_normalized | 0.186 | 0.152 | 0.222 |
| Q11 | acid_dissociation_fraction | 0.004 | 0 | 0.035 |
| Q11 | precipitation_signal | 0.016 | 0 | 0.062 |
| Q12 | pH_normalized | 0.251 | 0.228 | 0.276 |
| Q12 | acid_dissociation_fraction | 0.004 | 0 | 0.035 |
| Q12 | precipitation_signal | 0.003 | 0 | 0.024 |

### Q rationales

- **Q01**: This is a 25-fold dilution beyond the lowest observed M0 concentration. The pH estimate extrapolates the M0 log-concentration relationship; precipitation extrapolates M0's shallow trend. Dissociation is weakly identified, so its interval is deliberately broad and allows increased fractional dissociation upon dilution.

- **Q02**: The M1 pH curve is extrapolated far below the observed range. M1 precipitation declined strongly toward lower concentration, so the bounded prediction is near zero. Wide intervals reflect both long extrapolation and the unresolved M1 scale sensitivity.

- **Q03**: M2 had the highest pH and precipitation near the lower boundary throughout the campaign. The pH estimate is a long log-linear extrapolation, while precipitation is clipped near zero. Neither the molecular dissociation law nor behavior at this dilution was directly identified.

- **Q04**: At 0.08 M this is a modest extrapolation below the 0.125 M M0 observation. The estimate follows M0's log-linear pH curve and shallow precipitation curve. The interval includes instrument noise, sparse process variation, and uncertainty from the smaller volume.

- **Q05**: The concentration trend predicts a higher pH and less precipitation than observed for M1 at 0.125 M. The point estimate incorporates half of the observed direction of the twofold M1 scale contrast; the broad interval reflects that scale and batch variation were confounded.

- **Q06**: The M2 log-concentration curve predicts high normalized pH at 0.08 M. M2 precipitation remained near the measurement boundary at every studied concentration, so the prediction remains near zero. The interval allows a small unobserved positive signal.

- **Q07**: This is a short extrapolation above the observed M0 maximum of 0.5 M. M0 showed a systematic pH decline but only a shallow precipitation increase, which is continued here without assuming a new phase transition.

- **Q08**: The prediction continues M1's steep pH and precipitation concentration responses slightly beyond 0.5 M. Its precipitation estimate exceeds the M0 estimate, as already observed at 0.5 M. Extra width covers extrapolation and possible scale sensitivity.

- **Q09**: This modest high-concentration extrapolation preserves M2's steep pH response and strongly suppressed precipitation. Because observed M2 precipitation was close to zero and non-monotonic at that scale, the interval is bounded at zero and wider than assay noise alone.

- **Q10**: This shares concentration with Q04 but doubles volume. The point difference follows the small observed M0 scale contrast: slightly higher pH and slightly lower precipitation at larger scale. The pair should otherwise transfer closely.

- **Q11**: Relative to Q05, the point estimates carry forward the observed M1 twofold-scale direction: higher pH and lower precipitation at larger volume. This effect was based on only one historical scale pair, so the interval also permits weak or absent scale dependence.

- **Q12**: M2 pH transferred closely across the historical twofold scale comparison, so Q12 is predicted close to Q06. The slight upward precipitation adjustment follows the observed scale-pair direction but remains practically near the lower boundary.

Shared rationale:

Predictions use the sealed campaign's medium-specific log-linear relationship between normalized pH and concentration. Precipitation uses separate entity-conditioned trends: shallow for M0, strongly concentration-dependent for M1, and near the lower boundary for M2. Q04-Q12 scale-control differences are informed by the observed twofold-scale pairs, but their intervals recognize that scale was not independently replicated. Acid-dissociation fraction was poorly identified, frequently clipped at zero, and inconsistent with a simple nominal-concentration mass balance; its estimates are therefore conservative and its intervals substantially wider than final-assay noise. The 0.005 M cases are long extrapolations, while 0.08 M and 0.6 M are shorter extrapolations from the tested 0.125-0.500 M range.

## K2 — sealed seven-part retrospective

## 1. Status of claims in the initial information

The initial packet contained very few substantive mechanistic claims. It defined the system as a bounded synthetic weak-acid/direct-precipitation slice, stated that pH_normalized = pH/14, and warned that the public material names were selectors for categorical benchmark effects rather than predictions about real solvents. It supplied no task-specific property dossier, no quantitative pKa or Ksp, no reaction stoichiometry, and no substantive qualitative entity-to-mechanism mapping. The reference to a possible archival estimate was conditional; no usable estimate was actually supplied. Therefore, K1 correctly stated that there was no independent qualitative mapping to confirm or falsify.

What was supported:

- Entity conditioning was strongly supported. Batches 1-4, 5-8, and 9-12 formed visibly different pH and precipitation response families for selectors M0, M1, and M2.
- The direct-precipitation observable was active for M0 and M1. Final precipitation signals ranged from 0.0686 to 0.0806 for M0 and from 0.0444 to 0.1002 for M1. M2 instead remained near the lower boundary, from 0.00193 to 0.0110.
- The warning against interpreting selector names as real-solvent chemistry remained appropriate. Nothing in the experiment identified dielectric constants, proticity, solubility parameters, or any real molecular mechanism associated with the public names.
- The instruction that equilibrium_confidence was an environment diagnostic rather than scientific confidence was respected in K1. Its entity dependence was recorded, but it was not used as epistemic certainty.

What received counterevidence:

- A single ideal dilute monoprotic weak-acid law was not adequate. K1 compared the expected normalized-pH slope of 1/28 = 0.0357 per concentration decade with empirical endpoint slopes of approximately 0.0655, 0.1118, and 0.1363 for M0-M2. This is counterevidence to a common constant-pKa, ideal-activity model, although not to the broad statement that the benchmark concerns weak-acid behavior.
- A simple fixed medium offset was contradicted. M1 was less acidic than M0 at 0.125 M in batches 5 and 1, but slightly more acidic at 0.500 M in batches 7 and 3. K1 explicitly revised the interpretation to a medium-by-concentration interaction.
- Exact scale invariance received possible counterevidence in M1. Batches 6 and 8 differed by 0.00638 in normalized pH and 0.02154 in precipitation at the same nominal 0.250 M concentration. K1 did not ignore this; it called the result a testable warning rather than a law because scale and batch variation were confounded.
- Treating the reported dissociation fraction as alpha = [H+]/C received counterevidence. Its small, irregular, frequently zero values were incompatible with that simple calculation. K1 explicitly declined to force consistency.

What remained untested:

- Molecular identity, pKa, Ksp, precipitation stoichiometry, solid identity, activity coefficients, and the direction of acid-precipitation causality.
- Temperature, catalyst, waiting-time, stirring, and kinetic effects.
- Whether the M1 scale contrast was reproducible.
- Generalization outside 0.125-0.500 M, outside 0.040-0.080 L, or to real materials.

Thus there was no case where clear initial mechanistic counterevidence was silently retained as if supportive. The main limitation was instead that the initial packet lacked a substantive mechanism to test directly.

## 2. Experiments that formed or changed the interpretation

Batch 1 established the initial M0 reference: normalized pH 0.1393 and moderate precipitation 0.0686 at 0.125 M. Batches 2 and 3 were the first decisive concentration series. They lowered normalized pH to 0.1184 and 0.0999 while precipitation changed only to 0.0796 and 0.0806. That separation between a strong acidity response and a shallow precipitation response formed the first important mechanistic judgment.

Batch 4, at the same 0.250 M concentration as batch 2 but twice the nominal scale, supported approximate M0 scale transfer. It did not prove reproducibility because it was not a same-scale replicate.

Batch 5 initially suggested a simple M1 shift toward higher pH and lower precipitation than M0. Batches 6 and 7 materially changed that view. M1's normalized pH fell to 0.1229 and 0.0939, while precipitation rose to 0.0759 and 0.1002. The comparison of batches 7 and 3 produced the crossover that forced the K1 medium-by-concentration interpretation. Batch 8 then introduced the unresolved M1 scale warning.

Batch 9 created the clearest entity contrast: M2 gave normalized pH 0.2240 and precipitation 0.00193 at 0.125 M. Batches 10 and 11 showed that this was not merely one anomalous low-concentration result: M2 retained very low precipitation while its pH responded strongly to concentration. Batch 12 was especially important because its normalized pH of 0.17946 closely matched batch 10's 0.17863 at the same concentration and doubled scale.

The experimental choices themselves came from three different sources:

- The initial research goal directly motivated testing all three specified selectors and testing concentration and scale transfer.
- Existing data motivated later interpretation but did not alter the already chosen four-condition pattern within each selector. In particular, the M0 results did not cause me to redesign M1 or M2 coverage after seeing outcomes.
- The exact levels 0.125, 0.250, and 0.500 M, and the choice of a twofold scale comparison, were unvalidated design judgments. No property dossier justified those values. They were chosen to provide a broad logarithmic concentration span while fitting the material budget.

Other choices were assumptions rather than evidence-based decisions. I used no waiting period and implicitly treated the immediate terminated state as adequate for an equilibrium characterization. I also purchased one intermediate pH measurement in every batch even though the final assay reported the same core processed observables. Those decisions maximized uniform coverage but were not demonstrated to be the most informative design.

## 3. Current competing mechanisms and what can be distinguished

The leading competing explanations are:

1. Medium-specific acid activity plus an independent precipitation law. Each selector changes an effective acidity function and separately changes a precipitation threshold or propensity.
2. Precipitation-coupled acid equilibrium. Removal of one dissolved form shifts proton release or uptake, causing pH and precipitation to influence each other.
3. A hidden buffer or acid/base reservoir. Medium identity changes buffering, while precipitation responds to concentration through a partly independent pathway.
4. Multiple acid states, association, or concentration-dependent activities. These can generate slopes steeper than the ideal one-pKa result without requiring precipitation to drive pH.
5. Kinetic or transport effects. Mixing, nucleation, or finite settling could explain at least part of the M1 scale contrast.
6. Measurement-channel effects. Zero clipping and channel-specific calibration could explain irregular dissociation estimates and some near-boundary precipitation behavior.

The campaign distinguishes several coarse hypotheses. It rejects a universal response curve shared by all selectors. It also rejects a single fixed selector offset, because the M1-M0 difference changes with concentration and crosses sign. It shows that precipitation cannot be represented only as a universal function of observed pH: similar pH values in M0 and M1 can coexist with different concentration responses, while M2 has a distinct low-precipitation regime.

It cannot determine the direction of coupling. No intervention selectively changed precipitation while holding acid activity fixed, or vice versa. It cannot distinguish an activity-coefficient model from a hidden-buffer model, because neither activities nor buffer species were measured. It cannot distinguish equilibrium scale dependence from batch variation or kinetics, because there was one observation at each scale and no waiting-time intervention. Raw processed channels also cannot identify pKa, Ksp, or stoichiometry without a species-resolved mass balance.

The small equilibrium residuals indicate internally settled synthetic outputs, but they do not adjudicate among these chemical explanations. Likewise, the environment diagnostic must not be used to select a mechanism.

## 4. One additional complete experiment I would choose

I would choose an M1 batch at 0.250 M and 0.080 L: 0.020 mol reagent in 0.080 L selector-1 medium. I would measure with the pH meter immediately, wait 3,600 seconds with controlled stirring at 600 rpm, measure again with the pH meter, terminate, and obtain the final assay.

This repeats the condition of batch 8 while adding a within-batch temporal perturbation. It targets the largest unresolved inconsistency in K1: the batch-6 versus batch-8 scale contrast. The two pH-meter observations would provide pH and precipitation estimates before and after waiting, while the final assay would provide the more precise terminal values.

Possible outcomes and their implications would be:

- If the immediate and post-wait measurements remain near batch 8, and the final assay again gives higher pH and lower precipitation than batch 6, the evidence for a reproducible M1 scale-dependent response would strengthen.
- If the immediate state resembles batch 8 but evolves toward batch 6 during waiting, the original contrast would look more like mixing, nucleation, or finite-time relaxation than a true equilibrium scale effect.
- If the new 0.080 L batch resembles batch 6 from the outset, batch 8 would look like batch variability or a measurement fluctuation, weakening the scale-effect interpretation.
- If precipitation changes during waiting without a corresponding pH change, an approximately independent precipitation pathway would gain support.
- If pH and precipitation move together beyond their measurement uncertainties, coupled relaxation would gain support, although that correlation alone still would not establish causal direction.

One experiment cannot fully separate scale, time, and batch variation. A replicated factorial study would be needed for that. This choice is the most useful single experiment because it tests reproducibility and kinetic relaxation in the same complete batch without inventing a new material intervention. It is a proposed experiment only and was not executed.

## 5. Tradeoff between mechanistic identifiability and operational score

The design favored mechanistic coverage over score maximization. All 12 available complete batches were allocated to a structured selector-by-concentration design with a scale check for every selector. I continued studying M2 even though its environment diagnostic was around 0.79-0.81, lower than M0's roughly 0.94-0.97. Because that diagnostic carried a large positive scoring weight, an optimization-oriented campaign might have concentrated on high-diagnostic M0 conditions. Doing so would have sacrificed the strongest entity contrast and the discovery that M2 suppresses precipitation.

Likewise, batches 5-8 were scientifically valuable because they revealed the M1 crossover and possible scale dependence, not because they were guaranteed to improve score. No catalyst, heating, or other optimization operation was screened. This was appropriate because the stated goal was mechanism characterization and entity mapping, not medium ranking or optimization.

There were nevertheless identifiability sacrifices. Four conditions per selector allowed broad coverage but no exact same-condition replicate. The scale observations therefore confounded scale with ordinary batch variation. Uniformly purchasing one intermediate pH measurement per batch consumed all 12 intermediate-measurement opportunities but did not create a time course. A more identifiability-focused design could have omitted some redundant intermediate measurements and devoted them to before-and-after waiting observations in selected batches.

The immediate termination protocol also favored efficient, standardized coverage over kinetic identifiability. It avoided varying time as another factor, but it left the assumption of rapid equilibration untested. Thus the principal compromise was not optimization versus mechanism; it was breadth of mechanistic coverage versus replication and causal discrimination.

## 6. Underused evidence and weakest blind predictions

Several acquired evidence streams were only partially used:

- K1 relied chiefly on final processed estimates. The raw multichannel final-assay artifacts and spectral peak structures were not inspected in detail. They might have supported cross-channel consistency checks, although the hidden mapping would still prevent secure molecular assignments.
- The paired intermediate and final measurements were used qualitatively rather than in an explicit measurement-error or cross-instrument model. Such a model could have quantified systematic offsets and identified unusual pairs, such as the large intermediate-to-final precipitation change in batch 8.
- The 12 equilibrium residuals were reported but not modeled. Their small magnitude limited their discriminating value, while batch 10's relatively large 0.00892 residual might have justified extra caution when choosing it as an anchor.
- The irregular dissociation channel was appropriately treated as weakly identified, but no hierarchical censored model was fitted. Its zero boundary and declared noise make raw averages biased upward and complicate interpretation.
- Cost, risk, and scalar score were not central to the mechanism report. That was appropriate for the research goal, but it means the campaign cannot support an operational utility recommendation.

The least reliable blind predictions are Q01-Q03. They extrapolate from a minimum observed concentration of 0.125 M down to 0.005 M, a 25-fold dilution. K1 explicitly said that its empirical relationships should not be extrapolated below 0.125 M. The prediction task forced an extrapolation, and the Q rationales disclosed that fact, but the numerical form still assumed that the log-linear pH relationship continued without buffering transitions or new regimes.

The pH intervals for Q01-Q03 may be too narrow relative to model-form uncertainty. For example, Q03 predicted 0.415 with an 80% interval of 0.32-0.52. That interval is wide relative to assay noise but may still underrepresent uncertainty from extending an empirical M2 exponent far outside its tested range. Q02 has the same problem because the steep M1 exponent was estimated from only three concentration levels.

The low-concentration dissociation estimates are even less secure. Q01 assigned 0.040 and Q02-Q03 assigned 0.012 despite K1's explicit conclusion that no reliable dissociation-fraction law was identifiable. Those points introduced a plausible dilution heuristic rather than a result supported by the observed channel. The broad intervals acknowledged uncertainty, but the point estimates remain speculative and are the clearest tension with K1.

Q11 is another weak prediction. Its pH estimate of 0.186 and precipitation estimate of 0.016 propagated the direction of the single M1 scale contrast. Because K1 called that contrast only a warning, the point prediction gives it more structural weight than the evidence warrants. The intervals permit weaker scale dependence, but the precipitation interval may still be too narrow if batch 8 was anomalous or if kinetics dominate.

Q08's precipitation prediction of 0.108 is a smaller extrapolation above 0.500 M and is more defensible, but an unobserved precipitation threshold or saturation could invalidate the linear continuation. Q07-Q09 should therefore also include model-form uncertainty beyond instrument noise.

Predictions at 0.08 M were only modest extrapolations and are less problematic than Q01-Q03, but they still fall outside K1's declared applicability range. Overall, the rationales were candid about extrapolation, yet several intervals were closer to parametric confidence intervals than full predictive intervals under uncertain mechanism form.

## 7. Limitations of the sealed recommendation

The sealed recommendation selected batch 10: M2 at 0.250 M, 0.040 L, and 0.010 mol reagent. K1 explicitly described it as an evidentiary anchor, not an optimization claim. It was chosen because it participated in both a matched-concentration cross-selector comparison and the scale comparison with batch 12, and because its processed estimates were nonzero.

That selection has important limitations:

- It is one realization, not a replicated operating point.
- Its dissociation estimate of 0.01291 may be largely noise; batch 12 at the same concentration reported zero.
- Its equilibrium residual, 0.00892, was the largest final residual in the campaign.
- The scale partner, batch 12, reproduced pH closely but differed in dissociation, precipitation, residual, and environment diagnostic.
- It was not selected by an exhaustive optimization over concentration, time, temperature, catalyst, or scale.
- It has no demonstrated relevance to real acetonitrile or any named material because the runtime selector effect is synthetic and categorical.

Repeatability should be tested with several exact batch-10 replicates, preserving order of addition, volume, temperature, termination timing, and assay procedure. Local robustness should be tested with a small neighborhood around 0.250 M, such as approximately 0.20, 0.25, and 0.30 M, together with multiple volumes and replicated center points. A time perturbation should establish whether the terminal state is stable rather than merely immediate.

Cross-material generalization requires repeating the same local design for M0 and M1, not merely comparing one historical condition per selector. Cross-world generalization would require independent benchmark-world instances or seeds under the same public contract. Generalization to physical chemistry would require real materials, empirical calibration, species-resolved assays, and an independently validated mechanism; the current synthetic benchmark cannot supply that evidence.

Finally, sample-in highest and proven optimal are distinct claims. The recommendation was not even asserted to be the sample-in highest-scoring batch; it was selected for evidentiary connectivity. A sample-in highest result would only mean that one of the 12 observed realizations had the largest recorded scalar score. Proven optimality would require an appropriate objective, replicated comparisons, local and global search coverage, and uncertainty-aware validation. None of those conditions was met, so no optimality claim is justified.

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean width | Interval score |
|---|---:|---:|---:|---:|
| pH_normalized | 0.0225961 | 0.916667 | 0.0734167 | 0.111736 |
| acid_dissociation_fraction | 0.0167534 | 0.916667 | 0.04875 | 0.0697744 |
| precipitation_signal | 0.00854511 | 0.883333 | 0.0475 | 0.0533701 |

## Entity-map and scale-transfer evaluation

| Concentration M | Pairwise entity-contrast MAE |
|---:|---:|
| 0.005 | 0.0598965 |
| 0.08 | 0.00846769 |
| 0.6 | 0.00717722 |

| Selector | Same-concentration scale-gap MAE |
|---:|---:|
| 0 | 0.00259975 |
| 1 | 0.00810528 |
| 2 | 0.00178501 |

## Evidence boundary

The participant received exactly K1, Q, and K2, in that order. K1 is the primary open-form entity-mechanism artifact. No candidate property vector, numerical entity constant, hidden truth, or score was shown before K2 sealed. Reference truth was generated only after all 15 K2 responses sealed. The common direct weak-acid/free-ion-precipitation topology was fixed across worlds and arms; the task was entity mapping, not operation optimization.
