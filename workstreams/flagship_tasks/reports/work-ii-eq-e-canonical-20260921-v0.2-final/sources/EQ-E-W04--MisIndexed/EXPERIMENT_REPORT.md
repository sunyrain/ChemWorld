# EQ-E-W04--MisIndexed — final English experiment report

World `EQ-E-W04`; information arm `MisIndexed`; task `entity-conditioned mechanism characterization`; effective status `completed`; result origin `original`.

## Source campaign

The autonomous campaign completed 12/12 batches and 60 recorded operations. Exact replay is `True`; rollbacks: 0.

| Batch | Medium selector | Volume L | Reagent mol | Measurements | pH normalized | Free dissociation | Precipitation signal | Residual |
|---:|---:|---:|---:|---|---:|---:|---:|---:|
| 1 | 0 | 0.04 | 0.004 | ph_meter, final_assay | 0.198406 | 0 | 0.0120032 | 0 |
| 2 | 0 | 0.04 | 0.016 | ph_meter, final_assay | 0.129111 | 0 | 0.0418249 | 0.00351127 |
| 3 | 0 | 0.08 | 0.008 | ph_meter, final_assay | 0.196452 | 0.00315217 | 0.00918265 | 0 |
| 4 | 0 | 0.08 | 0.032 | ph_meter, final_assay | 0.123875 | 0.00195773 | 0.0333399 | 0 |
| 5 | 1 | 0.04 | 0.004 | ph_meter, final_assay | 0.155278 | 0.0012404 | 0.0507848 | 0.00184555 |
| 6 | 1 | 0.04 | 0.016 | ph_meter, final_assay | 0.092322 | 0 | 0.115945 | 0.00744666 |
| 7 | 1 | 0.08 | 0.008 | ph_meter, final_assay | 0.158825 | 0.000714802 | 0.0604933 | 0.00674473 |
| 8 | 1 | 0.08 | 0.032 | ph_meter, final_assay | 0.0912466 | 0.003989 | 0.119569 | 0 |
| 9 | 2 | 0.04 | 0.004 | ph_meter, final_assay | 0.219132 | 0.00209684 | 0.000659129 | 0.00631357 |
| 10 | 2 | 0.04 | 0.016 | ph_meter, final_assay | 0.144319 | 0.00742595 | 0.0244877 | 0 |
| 11 | 2 | 0.08 | 0.008 | ph_meter, final_assay | 0.221205 | 0.0027187 | 0.00910653 | 0.000666545 |
| 12 | 2 | 0.08 | 0.032 | ph_meter, final_assay | 0.141879 | 0 | 0.0233102 | 0 |

### Sealed evidentiary anchor

Batch `8`: Batch 8 is a useful evidentiary anchor because its high-loading, larger-scale medium-1 response directly pairs with batch 6 at the same concentration, supporting a scale-transfer check while retaining clear entity-conditioned precipitation.

Complete sanitized agent-visible scientific I/O: [trajectory](trajectory.jsonl). Every attempted operation is retained in order; private provider events, credentials, session identifiers, usage accounting, and evaluator-only state are excluded.

## K1 — sealed open mechanistic report

# Mechanistic report

## 1. Scope and experimental design

I studied three selectable benchmark media, denoted M0, M1, and M2. Although the public catalog attaches familiar solvent labels to selectors, the task explicitly defines their reaction effects as categorical benchmark effects. I therefore do not infer ordinary real-solvent chemistry from those names.

The 12 completed batches formed a balanced 3 × 2 × 2 design:

- medium: M0, M1, or M2;
- nominal reagent concentration: 0.10 or 0.40 mol L⁻¹;
- liquid volume: 0.040 or 0.080 L.

No catalyst, heating, or deliberate waiting period was used. Each batch received an in-process pH-meter measurement, was terminated, and then received the required final assay. Consequently, concentration and scale effects can be compared directly, but temperature, catalyst, time-to-equilibrium, mixing, and wider concentration effects cannot be identified.

## 2. Direct final-assay observations

The following values are observations, not fitted or inferred hidden states. “pHn” is pH_normalized = pH/14. “Acid fraction” is the reported acid_dissociation_fraction. “Precip.” is precipitation_signal. “Residual” is equilibrium_residual. The diagnostic column is equilibrium_confidence; it is an environment diagnostic and is not my scientific confidence.

| Batch | Medium | Volume (L) | C (mol L⁻¹) | pHn | Acid fraction | Precip. | Residual | Diagnostic |
|---:|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | M0 | 0.040 | 0.10 | 0.198406 | 0.000000 | 0.012003 | 0.000000 | 0.828922 |
| 2 | M0 | 0.040 | 0.40 | 0.129111 | 0.000000 | 0.041825 | 0.003511 | 0.876945 |
| 3 | M0 | 0.080 | 0.10 | 0.196452 | 0.003152 | 0.009183 | 0.000000 | 0.832402 |
| 4 | M0 | 0.080 | 0.40 | 0.123875 | 0.001958 | 0.033340 | 0.000000 | 0.863640 |
| 5 | M1 | 0.040 | 0.10 | 0.155278 | 0.001240 | 0.050785 | 0.001846 | 0.928662 |
| 6 | M1 | 0.040 | 0.40 | 0.092322 | 0.000000 | 0.115945 | 0.007447 | 0.960358 |
| 7 | M1 | 0.080 | 0.10 | 0.158825 | 0.000715 | 0.060493 | 0.006745 | 0.942032 |
| 8 | M1 | 0.080 | 0.40 | 0.091247 | 0.003989 | 0.119569 | 0.000000 | 0.955972 |
| 9 | M2 | 0.040 | 0.10 | 0.219132 | 0.002097 | 0.000659 | 0.006314 | 0.810206 |
| 10 | M2 | 0.040 | 0.40 | 0.144319 | 0.007426 | 0.024488 | 0.000000 | 0.803202 |
| 11 | M2 | 0.080 | 0.10 | 0.221205 | 0.002719 | 0.009107 | 0.000667 | 0.812789 |
| 12 | M2 | 0.080 | 0.40 | 0.141879 | 0.000000 | 0.023310 | 0.000000 | 0.809564 |

The scale-averaged final-assay cell means were:

| Medium | Mean pHn at 0.10 M | Mean pHn at 0.40 M | Mean precip. at 0.10 M | Mean precip. at 0.40 M |
|:---:|---:|---:|---:|---:|
| M0 | 0.197429 | 0.126493 | 0.010593 | 0.037582 |
| M1 | 0.157052 | 0.091784 | 0.055639 | 0.117757 |
| M2 | 0.220168 | 0.143099 | 0.004883 | 0.023899 |

Converted to ordinary pH units, these pH means are respectively:

- M0: pH 2.764 at 0.10 M and 1.771 at 0.40 M;
- M1: pH 2.199 and 1.285;
- M2: pH 3.082 and 2.003.

## 3. Main relationships inferred from the observations

### 3.1 Concentration is the dominant within-medium driver

Increasing nominal concentration fourfold lowered the mean pH by 0.993, 0.914, and 1.079 pH units in M0, M1, and M2, respectively. Equivalently, the hydrogen-ion signal implied by pH increased approximately 9.84-fold, 8.20-fold, and 11.99-fold. All three media therefore share a robust directional rule:

higher reagent concentration → lower pH → larger precipitation signal.

The precipitation signal increased by factors of approximately 3.55 in M0, 2.12 in M1, and 4.89 in M2. Thus the direction transfers across all three media, while the response magnitude is entity-conditioned.

A classical dilute, unbuffered weak acid with constant thermodynamic Ka would have [H+] scaling approximately as the square root of total acid concentration. The observed two-point effective exponents are much larger: about 1.65, 1.52, and 1.79 for M0, M1, and M2 when [H+] is represented as proportional to C^β. These are descriptive exponents over only 0.10–0.40 M, not established laws. Their departure from 0.5 could reflect activity coefficients, a medium acid/background contribution, concentration-dependent effective ionization, precipitation-driven mass-balance shifts, or the fact that the reported reagent concentration is not identical to a simple analytical weak-acid concentration.

### 3.2 Medium identity shifts both acid response and precipitation

At both concentrations, the pH ordering is:

M1 < M0 < M2.

Interpreted through pH alone, M1 produces the greatest hydrogen-ion activity and M2 the least. The precipitation ordering is also stable in the cell means:

M1 > M0 > M2.

M1 is especially distinct. At 0.10 M its mean precipitation signal is 0.05564, compared with 0.01059 for M0 and 0.00488 for M2. At 0.40 M it is 0.11776, compared with 0.03758 and 0.02390. Medium identity therefore changes more than a pH offset: it also changes the amount or observability of the solid-forming response.

The parallel ordering of lower pH and greater precipitation suggests coupling rather than two wholly independent outputs. It does not, however, prove that acidity directly causes precipitation.

### 3.3 Scale transfer is supported within the tested range

Changing volume from 0.040 to 0.080 L while holding concentration fixed produced small and non-systematic changes relative to the concentration and medium effects. The normalized-pH scale differences ranged from approximately −0.00524 to +0.00355. Precipitation differences ranged from approximately −0.00848 to +0.00971.

The known final-assay noise scales are 0.002 for pHn and 0.006 for precipitation_signal. Some individual scale contrasts are therefore not exactly zero, but there is no common direction across media or concentrations. The most economical description is that concentration, rather than total amount or vessel scale, controls the response over 0.040–0.080 L. Batch 8 was selected as the replay anchor because it pairs directly with batch 6 at 0.40 M: their final pHn values were 0.091247 and 0.092322, and their precipitation signals were 0.119569 and 0.115945 despite the twofold volume difference.

This is local scale transfer, not proof of arbitrary scale invariance.

### 3.4 The reported acid-dissociation fraction is not quantitatively resolved

Final acid_dissociation_fraction values ranged from zero to 0.00743 and were frequently clipped at zero. The declared final-assay noise scale for this channel is 0.006, comparable to the entire observed range. Its medium means are consequently dominated by noise and boundary clipping. I do not use that channel to rank intrinsic dissociation tendencies or estimate Ka.

This distinction matters: pH clearly separates media and concentrations, while the reported dissociation fraction does not. Any mechanism claiming precise dissociation fractions from these batches would exceed the evidence.

## 4. Proposed effective mechanism

A chemically interpretable minimal model is a coupled acid-ionization and direct-precipitation system:

HA ⇌ H⁺ + A⁻

M* + νA⁻ ⇌ S(s)

Here HA is the anonymous acid-like reagent, A⁻ is its conjugate/base-like dissolved form, M* denotes an unidentified medium-provided or background solid-forming partner, and S is an effective precipitated phase. For medium m, one could write

Ka,m,eff = a(H⁺)a(A⁻)/a(HA)

Ksp,m,eff = a(M*)a(A⁻)^ν

with total-material balances and electroneutrality closing the system. Medium identity can act through several effective parameters at once:

1. Ka,m,eff or the activity coefficients controlling the measured pH;
2. the available concentration/activity of M*;
3. Ksp,m,eff or nucleation propensity;
4. the mapping from actual solid amount/particle population to the bounded precipitation signal.

Precipitation removes dissolved A⁻. Under a reversible equilibrium interpretation, that removal can pull HA ionization forward, providing a natural coupling between more solid formation and a lower pH. This qualitative feedback is compatible with M1 showing both the lowest pH and the largest precipitation signal.

An equally useful empirical representation, restricted to the measured domain, is:

pHn_m(C) ≈ A_m + B_m log10(C/0.10)

P_m(C) ≈ P0,m (C/0.10)^α_m.

Using scale-averaged observations:

- A = (0.19743, 0.15705, 0.22017) for M0–M2;
- B = (−0.11782, −0.10841, −0.12801);
- P0 = (0.01059, 0.05564, 0.00488);
- α = (0.913, 0.541, 1.146).

These expressions interpolate the two tested concentration levels. They are not mechanistic parameter estimates and should not be extrapolated toward zero concentration, saturation, or substantially higher loading.

## 5. How the experiments changed the interpretation

The supplied qualitative mapping proposed:

- selector 0: higher ionization and higher solid formation;
- selector 1: intermediate ionization and lower solid formation;
- selector 2: lower ionization and intermediate solid formation.

The literal selector-to-property indexing is not supported by the observations.

Batches 1–4 established M0 as an intermediate response: its mean pH lay between M1 and M2, and its high-concentration precipitation signal was also intermediate. Batches 5–8 materially revised the mapping because M1, which had been labeled lower in solid formation, instead produced by far the largest precipitation signals at every matched design point. Its pH was also consistently below M0 and M2. Batches 9–12 supported the “lower ionization” direction for M2 through its higher pH, but its precipitation was lower rather than clearly intermediate.

Thus M1 most closely resembles the supplied qualitative “high ionization/high solid formation” profile, suggesting at least an indexing error between M0 and M1. The remaining M0/M2 assignment cannot be repaired into the supplied three profiles without tension: observed M0 precipitation exceeds M2 at high concentration. A simple permutation may therefore be incomplete; the supplied labels may also compress concentration-dependent or proxy-dependent behavior.

## 6. Instrument and temporal evidence

The in-process pH-meter readings usually supported the same qualitative ordering and concentration effects, but its precipitation channel was noisier. For example, batch 6 reported an in-process precipitation signal of 0.17769 and a final value of 0.11594; batch 8 reported 0.13166 and 0.11957. These differences could reflect larger pH-meter-channel noise, sampling/measurement timing, or real evolution before termination. Because the experiment did not include controlled time points, I cannot distinguish those explanations.

Final equilibrium_residual values were small, ranging from zero to 0.00745, but this does not establish thermodynamic equilibrium independently. Likewise, the mean environment diagnostic differed by medium—approximately 0.850 for M0, 0.947 for M1, and 0.809 for M2—but equilibrium_confidence is explicitly an environment diagnostic, not epistemic confidence and not a mechanistic observable. I therefore do not treat its ranking as evidence that one medium is more scientifically understood or more truly equilibrated.

## 7. Competing explanations

Several mechanisms remain observationally equivalent or nearly so:

1. **Coupled equilibrium:** precipitation consumes an ionization product and thereby drives further acid dissociation.
2. **Common medium control:** medium identity independently changes effective acidity and solubility/nucleation, producing correlated pH and precipitation without strong causal feedback between them.
3. **Background-acidity model:** each medium contributes a different acid/base background; pH ordering then need not equal intrinsic HA dissociation ordering.
4. **Kinetic precipitation:** precipitation_signal may primarily reflect nucleation, particle size, or turbidity at the assay time rather than equilibrium solid amount.
5. **Nonlinear sensor mapping:** the bounded precipitation proxy may have medium-dependent optical sensitivity or saturation, so signal ratios need not equal solid-mass ratios.
6. **Activity-coefficient effects:** at 0.10–0.40 M, nonideality may dominate apparent concentration exponents and prevent a simple constant-Ka interpretation.
7. **Multiple dissolved or solid species:** the anonymous reagent could support more than one ionization step, complex, or precipitated form. The present observables cannot resolve these possibilities.

## 8. Evidence boundaries and uncertainty

Strongly supported within the tested domain:

- Increasing concentration from 0.10 to 0.40 M lowers pH and increases precipitation in every medium.
- Medium identity substantially shifts both responses.
- M1 gives the lowest pH and greatest precipitation; M2 gives the highest pH and generally the least precipitation; M0 is intermediate.
- Responses approximately transfer between 0.040 and 0.080 L at fixed concentration.
- The supplied literal selector mapping is inconsistent with the observed medium labels, especially for M1 precipitation.

Not identifiable from these data:

- thermodynamic Ka, Ksp, activity coefficients, stoichiometry, or solid composition;
- the true dissociated fraction, because its signal lies near the measurement noise floor and is clipped at zero;
- whether precipitation is at equilibrium or kinetically limited;
- causal direction between acidification and precipitation;
- effects of temperature, mixing speed, waiting time, catalyst, or selector 3;
- response outside 0.10–0.40 M and 0.040–0.080 L;
- whether familiar catalog solvent names have ordinary real-world chemical implications in this categorical benchmark.

There were no same-condition replicate batches beyond the matched-concentration scale pairs. Those pairs provide a useful reproducibility/transfer check but do not yield a pure estimate of batch variance because volume changed. Numerical precision in the table should therefore not be mistaken for equivalent mechanistic precision.

## 9. Overall conclusion

The simplest defensible account is an entity-conditioned, concentration-controlled acid/precipitation system. Concentration raises the effective hydrogen-ion response and solid-forming response together. Medium identity changes the baseline acidity and precipitation propensity, most likely through effective ionization, activity, solubility, and/or nucleation parameters. These relationships are largely intensive over the tested twofold scale change. M1 is the strong-acid-response/high-precipitation entity, M0 is intermediate, and M2 is the weak-acid-response/low-precipitation entity in the measured window. This empirical mapping contradicts the supplied literal indexing, but the data do not uniquely determine whether a simple permutation or a more substantive failure of the qualitative profile is responsible.

## Q — sealed blind predictions

| Query | Metric | Estimate | 80% lower | 80% upper |
|---|---|---:|---:|---:|
| Q01 | pH_normalized | 0.351 | 0.3 | 0.402 |
| Q01 | acid_dissociation_fraction | 0.0015 | 0 | 0.018 |
| Q01 | precipitation_signal | 0.003 | 0 | 0.014 |
| Q02 | pH_normalized | 0.298 | 0.247 | 0.349 |
| Q02 | acid_dissociation_fraction | 0.0017 | 0 | 0.018 |
| Q02 | precipitation_signal | 0.011 | 0 | 0.032 |
| Q03 | pH_normalized | 0.387 | 0.336 | 0.438 |
| Q03 | acid_dissociation_fraction | 0.003 | 0 | 0.02 |
| Q03 | precipitation_signal | 0.0025 | 0 | 0.014 |
| Q04 | pH_normalized | 0.209 | 0.197 | 0.221 |
| Q04 | acid_dissociation_fraction | 0.0015 | 0 | 0.012 |
| Q04 | precipitation_signal | 0.0086 | 0 | 0.019 |
| Q05 | pH_normalized | 0.168 | 0.156 | 0.18 |
| Q05 | acid_dissociation_fraction | 0.0017 | 0 | 0.013 |
| Q05 | precipitation_signal | 0.0493 | 0.031 | 0.068 |
| Q06 | pH_normalized | 0.233 | 0.22 | 0.246 |
| Q06 | acid_dissociation_fraction | 0.003 | 0 | 0.015 |
| Q06 | precipitation_signal | 0.005 | 0 | 0.015 |
| Q07 | pH_normalized | 0.106 | 0.088 | 0.124 |
| Q07 | acid_dissociation_fraction | 0.0015 | 0 | 0.015 |
| Q07 | precipitation_signal | 0.0544 | 0.038 | 0.071 |
| Q08 | pH_normalized | 0.073 | 0.055 | 0.091 |
| Q08 | acid_dissociation_fraction | 0.0017 | 0 | 0.016 |
| Q08 | precipitation_signal | 0.1466 | 0.116 | 0.178 |
| Q09 | pH_normalized | 0.121 | 0.102 | 0.14 |
| Q09 | acid_dissociation_fraction | 0.003 | 0 | 0.018 |
| Q09 | precipitation_signal | 0.038 | 0.023 | 0.054 |
| Q10 | pH_normalized | 0.209 | 0.2 | 0.218 |
| Q10 | acid_dissociation_fraction | 0.0015 | 0 | 0.011 |
| Q10 | precipitation_signal | 0.0086 | 0 | 0.018 |
| Q11 | pH_normalized | 0.168 | 0.159 | 0.177 |
| Q11 | acid_dissociation_fraction | 0.0017 | 0 | 0.012 |
| Q11 | precipitation_signal | 0.0493 | 0.033 | 0.066 |
| Q12 | pH_normalized | 0.233 | 0.223 | 0.243 |
| Q12 | acid_dissociation_fraction | 0.003 | 0 | 0.014 |
| Q12 | precipitation_signal | 0.005 | 0 | 0.014 |

### Q rationales

- **Q01**: Selector 0 extrapolation to 0.005 M using the fitted log-concentration pH relationship and a concentration power law for precipitation. The 20-fold extrapolation below the observed range motivates wide intervals, while acid dissociation remains effectively unresolved near the assay floor.

- **Q02**: Selector 1 retains its lower-pH and higher-precipitation identity, but both relationships are extrapolated far below the studied concentration range. The precipitation interval includes zero because the expected signal approaches the assay noise scale.

- **Q03**: Selector 2 is predicted to retain the highest normalized pH and a precipitation response near the measurement floor. Extrapolation uncertainty dominates because 0.005 M is well below the observed 0.10–0.40 M range.

- **Q04**: The concentration is close to the observed 0.10 M boundary. Selector 0 predictions therefore mainly interpolate the established medium response, with modest added uncertainty for the smaller 0.024 L scale.

- **Q05**: Selector 1 showed a reproducible acidic and precipitation-prone response at both studied scales. The estimate is a short extrapolation from 0.10 M, with the interval including instrument noise and uncertainty in the low-concentration curvature.

- **Q06**: Selector 2 is predicted to remain less acidic and weakly precipitating at 0.08 M. Its precipitation estimate is close to the final-assay noise floor, so the lower prediction bound is zero.

- **Q07**: This is a moderate extrapolation above the observed 0.40 M endpoint. The prediction continues selector 0's fitted log-concentration pH decline and near-proportional precipitation increase, with widened intervals for possible high-loading curvature.

- **Q08**: Selector 1 is expected to remain the lowest-pH and most precipitation-prone entity. The interval is wider than an instrumental interval because saturation or sub-power-law curvature above 0.40 M was not tested.

- **Q09**: The estimate extrapolates selector 2's concentration response to 0.60 M while retaining its higher pH and lower precipitation relative to the other selectors. Model uncertainty exceeds assay noise at this untested concentration.

- **Q10**: At fixed concentration, the studied 0.040 and 0.080 L batches showed no consistent scale effect. The 0.048 L prediction therefore uses the selector 0 concentration model with a narrower interval than the 0.024 L counterpart.

- **Q11**: The 0.048 L volume lies between the studied scales, for which selector 1 transferred well. The estimate is governed primarily by concentration and entity identity rather than total reagent amount.

- **Q12**: Scale invariance over 0.040–0.080 L supports applying the selector 2 concentration response at 0.048 L. Precipitation remains near the detection/noise floor, whereas normalized pH is more tightly constrained.

Shared rationale:

Predictions use the sealed campaign's scale-averaged entity-specific relationships. Normalized pH was represented locally as A_m + B_m log10(C/0.10), fitted to the 0.10 and 0.40 M observations. Precipitation was represented as P0_m(C/0.10)^alpha_m, with extra uncertainty for extrapolation and floor clipping. The tested twofold scale change showed no systematic effect, so concentration rather than total amount was used as the primary predictor; intervals are slightly wider at 0.024 L than at the interpolated 0.048 L scale. Acid-dissociation measurements were comparable to the 0.006 final-assay noise, frequently clipped at zero, and showed no reliable concentration trend. Their predictions therefore remain near the empirical selector means with broad, zero-bounded intervals rather than imposing an unsupported mechanistic law. Intervals combine assay noise, between-scale variation, model uncertainty, and substantially increased uncertainty at 0.005 and 0.60 M.

## K2 — sealed seven-part retrospective

## 1. Assessment of the initial claims

The initial material packet did contain substantive qualitative claims. It proposed that selector 0 had higher acid-ionization and solid-formation tendencies, selector 1 had intermediate ionization and lower solid formation, and selector 2 had lower ionization and intermediate solid formation. It also warned that the selectable materials were categorical benchmark formulations rather than a basis for importing ordinary real-solvent chemistry.

The categorical-benchmark warning was respected but was not itself experimentally tested. I consistently interpreted the selectors as M0–M2 rather than attributing their behavior to named real solvents.

The proposed selector mapping was only partly supported and was substantially contradicted:

- The pH evidence supported selector 2 as the least acidic-response entity: its scale-averaged final pH was 3.082 at 0.10 M and 2.003 at 0.40 M, higher than the matched values for selectors 0 and 1.
- The proposed ordering between selectors 0 and 1 was contradicted. Batches 5–8 showed that selector 1 had consistently lower pH than selector 0 in batches 1–4. Thus, if lower pH is used as the operative indicator of stronger acid response, the observed ordering was M1 > M0 > M2 rather than M0 > M1 > M2.
- The solid-formation mapping was more directly contradicted. Selector 1 was initially described as having lower solid-formation tendency, yet it produced the largest precipitation signal at every matched condition. For example, at 0.40 M the final signals were 0.115945 and 0.119569 in batches 6 and 8, versus 0.041825 and 0.033340 for selector 0 in batches 2 and 4.
- Selector 2 did not behave as the clearly intermediate precipitation entity. Its scale-averaged precipitation was 0.004883 at 0.10 M and 0.023899 at 0.40 M, below selector 0 at both concentrations.

K1 therefore explicitly revised rather than silently retained the supplied indexing. It stated that “the literal selector-to-property indexing is not supported” and that M1 most closely resembled the supplied high-ionization/high-solid profile. This was a response to observed counterevidence, not merely an absence of supporting evidence.

There is an important qualification. The final-assay acid_dissociation_fraction channel did not directly establish the ionization ordering: its values were mostly between zero and 0.0074, comparable with the declared 0.006 noise scale and frequently clipped at zero. The ionization interpretation was instead based mainly on pH. K1 acknowledged this by saying that the fraction channel could not support a quantitative ranking. Thus the pH-based disagreement with the prior is genuine, but it does not uniquely identify intrinsic Ka.

The initial packet did not make quantitative claims about concentration exponents, scale transfer, kinetics, thermodynamic equilibrium, or precipitation stoichiometry. Those matters were not confirmations of prior claims. Concentration and local scale behavior were tested; kinetics, true equilibrium, stoichiometry, and named chemical identities remained untested.

## 2. Experiments that formed or changed the interpretation

The 3 × 2 × 2 design was selected before observing outcomes. Its main determinants were the research goal, the twelve-batch budget, and an unvalidated but reasonable assumption that 0.10 and 0.40 M would span an informative response range while 0.040 and 0.080 L would provide a local scale contrast. The initial qualitative mapping motivated testing all three selectors symmetrically, but it did not determine the numerical concentration or volume choices.

Specific experiments had different inferential roles:

- Batches 1 and 2 first established the strong concentration effect in selector 0: pH_normalized fell from 0.198406 to 0.129111 and precipitation rose from 0.012003 to 0.041825 as concentration increased from 0.10 to 0.40 M.
- Batches 3 and 4 were important because they approximately reproduced those concentration effects at twice the volume. They began to support an intensive, concentration-controlled description rather than a total-mole-controlled one.
- Batches 5 and 6 produced the first major revision of the supplied mapping. Selector 1 was not weakly precipitating: its final precipitation signals were 0.050785 and 0.115945, both substantially above the matched selector-0 values. Its pH was also lower.
- Batches 7 and 8 made that revision much more credible by reproducing the selector-1 pattern at 0.080 L. In particular, batches 6 and 8 gave closely matched high-concentration results despite their twofold volume difference.
- Batches 9–12 established selector 2 as the highest-pH and generally lowest-precipitation entity. They also prevented me from interpreting M0 as simply “low precipitation,” because M0 remained above M2 at high concentration.

The most consequential change in belief therefore occurred after batches 5–8. Before those batches, retaining the initial selector ranking would still have been plausible. After them, especially after the scale-paired confirmation in batches 7 and 8, the “selector 1 has lower solid-formation tendency” claim was untenable.

Some choices were based more on design convenience than validated mechanism. I assumed that two concentration levels would be enough to reveal a transferable functional relationship, and I treated the two scale levels partly as replication. Neither assumption was fully justified. Two concentration levels determine a slope but cannot reveal curvature, thresholds, or saturation. The scale pairs are not true replicates because volume changed. I also omitted deliberate waiting, thermal perturbation, dilution history, and repeated final assays, so the design was stronger for mapping response surfaces than for distinguishing equilibrium from kinetic mechanisms.

## 3. Current competing mechanisms and what the experiments discriminate

K1 proposed a minimal coupled picture:

HA ⇌ H+ + A−

M* + νA− ⇌ S(s)

In that picture, precipitation consumes A− and can pull ionization forward, linking lower pH with more solid formation. This remains a plausible mechanism because every selector showed lower pH and higher precipitation at higher concentration, and M1 showed both the lowest pH and the greatest precipitation.

The most important alternatives are:

1. **Coupled reversible equilibrium.** Precipitation removes an ionization product, so acid dissociation and solid formation thermodynamically reinforce one another.
2. **Parallel medium effects.** Each medium independently changes acidity and precipitation propensity. Their correlation need not imply causal feedback.
3. **Background-acidity differences.** The media may contribute different acid/base backgrounds, so pH need not measure intrinsic reagent dissociation.
4. **Kinetic or path-dependent precipitation.** The precipitation signal may reflect nucleation, growth, aggregation, or persistent particles rather than an equilibrium solid amount.
5. **Medium-dependent observation mapping.** Identical solid amounts could produce different normalized precipitation signals because of particle size or optical response.
6. **Nonideal or multi-species acid chemistry.** Activity coefficients, complexation, or multiple ionization steps could explain why the effective pH response was much steeper than the textbook square-root weak-acid relation.

The experiments discriminate some coarse alternatives. They strongly disfavor a medium-independent response, a total-mole-only response over the tested scales, and the supplied literal selector mapping. They also show that a single common precipitation amplitude cannot describe all three selectors.

They do not distinguish reversible coupling from parallel medium control. They do not distinguish thermodynamic solid amount from nucleation or optical effects. Low residuals and high environment diagnostics do not resolve this issue: as K1 emphasized, equilibrium_confidence is an environment diagnostic, not scientific confidence. The in-process/final differences, such as precipitation changing from 0.177686 to 0.115945 in batch 6, raise a temporal or instrument question but cannot separate kinetics from cross-instrument noise.

## 4. One additional complete experiment I would choose

I would perform a dilution-history experiment in selector 1 because M1 generated the largest and clearest precipitation response.

Proposed sequence:

1. Add 0.020 L of selector-1 medium.
2. Add 0.008 mol reagent, initially creating 0.40 M.
3. Measure once with the pH meter to document the concentrated state.
4. Add 0.060 L of the same medium, diluting the batch to 0.10 M at a final volume of 0.080 L.
5. Use a fixed, preregistered wait and stirring condition.
6. Terminate and perform the final assay.

The final concentration and volume would match batch 7, but the preparation history would differ: batch 7 was prepared directly at 0.10 M, whereas this batch would pass through the precipitation-prone 0.40 M state.

Possible outcomes would have different implications:

- If the final pH and precipitation return near batch 7 values—pH_normalized 0.158825 and precipitation 0.060493—that would support reversibility and a state-function-like concentration dependence.
- If pH returns near batch 7 but precipitation remains near the high-concentration batch-8 value of 0.119569, that would favor persistent solid, nucleation hysteresis, or an irreversible optical/particle-memory effect.
- If both pH and precipitation retain high-concentration-like values, the system would show broader compositional or chemical hysteresis, challenging the simple equilibrium model.
- If precipitation drops below batch 7 while pH matches it, redissolution or particle-size effects would need explicit consideration.

This single experiment would still have limitations. The fixed wait would not be matched in the original batch 7, and the pre- and post-dilution measurements would use different instruments. It would not conclusively prove equilibrium, but it would provide a stronger mechanistic discriminator than another static grid point.

## 5. Tradeoff between identifiability and operational score

The design prioritized characterization over score maximization. All twelve available complete experiments were allocated symmetrically across entities, concentrations, and scales. After selector 1 began producing higher diagnostic scores and larger precipitation signals, I did not redirect later batches toward it. Instead, I completed the preregistered-like coverage of selectors 1 and 2.

This choice sacrificed potential operational score. For example, selector-1 batches 6–8 had diagnostic values around 0.94–0.96, whereas selector-2 batches 9–12 were around 0.80–0.81. A score-seeking campaign could have concentrated resources on conditions resembling batch 6 or 8. Doing so would have weakened entity mapping and might never have established that selector 2 was the high-pH, low-precipitation endpoint.

Conversely, the design did not maximize mechanistic identifiability in an absolute sense. It favored broad static coverage over causal perturbations. Two concentrations and two volumes efficiently answered whether entity and concentration effects transferred locally, but they were insufficient for curvature, equilibrium, hysteresis, or kinetic identification. Thus the central tradeoff was not simply “mechanism versus score.” It was broad response-surface identifiability versus deeper causal-mechanism identifiability.

There is no evidence that I sacrificed identifiability to optimize the scalar score during execution. The scalar score was treated as a diagnostic rather than the research objective. There is, however, evidence that I sacrificed deeper mechanistic resolution to preserve balanced coverage and complete all required selector contrasts.

## 6. Underused evidence and weakest blind predictions

Several evidence sources were not fully exploited:

- I relied primarily on processed estimates and did not conduct a detailed analysis of the raw final-assay spectra, mass-balance fields, calibration metadata, or missingness information.
- All twelve pH-meter measurements were collected, but K1 only used selected examples to discuss pre/final differences. A censored hierarchical model of the paired channels could have quantified systematic instrument or timing offsets.
- The acid_dissociation_fraction observations were treated appropriately as unresolved, but I did not fit a censored likelihood that explicitly modeled zero clipping and the declared 0.006 noise.
- The concentration-by-scale data could have supported a formal interaction model. Instead, I used simple paired comparisons and descriptive power laws.
- Process telemetry was nearly invariant by design and therefore offered little leverage. The absence of deliberate time or temperature variation made it impossible to use telemetry mechanistically.

No prediction truth has been disclosed, so I cannot assess realized prediction error. Prospectively, the least reliable sealed predictions are Q01–Q03 at 0.005 M. They extrapolate twentyfold below the lowest studied concentration using a log-linear pH model and a power-law precipitation model determined from only two concentration levels. K1 had explicitly warned that these equations were local interpolations and “should not be extrapolated toward zero concentration.” The prediction task required extrapolation, but the Q01–Q03 pH intervals—roughly ±0.051 in normalized units—may still be too narrow given the range of competing low-concentration limits.

The Q07–Q09 predictions at 0.60 M are also uncertain, especially Q08 precipitation. The sealed estimate of 0.1466 with an 80% interval of 0.116–0.178 assumes that selector 1 continues its fitted power law. Saturation, aggregation, or a bounded-signal ceiling could create appreciable curvature above 0.40 M. Q08's interval may therefore be too narrow.

Q04–Q06 use a concentration close to the observed range but a 0.024 L volume below the tested minimum of 0.040 L. Their pH intervals only modestly exceed the assay-scale uncertainty. If vessel-scale or mixing effects emerge below 0.040 L, those intervals would also be too narrow. Q10–Q12 are the most defensible because 0.08 M is close to the measured 0.10 M boundary and 0.048 L lies between the tested scales.

The acid-dissociation predictions were deliberately broad and zero-bounded, reflecting K1's statement that the channel was unresolved. Their point estimates are weakly informed empirical averages rather than mechanistic predictions. That limitation is consistent with K1, although assigning selector-specific point estimates may imply more entity resolution than the evidence truly supported.

Overall, the sealed Q rationale disclosed the extrapolations and added uncertainty, but the numerical intervals did not fully embody K1's strongest applicability warning. In particular, the low-concentration pH and precipitation intervals assumed much more functional-form stability than K1 had established.

## 7. Limitations of the sealed recommendation

The sealed recommendation selected batch 8: selector 1, 0.40 M, 0.080 L. The stated reason was that it provided an evidentiary anchor for local scale transfer through its pairing with batch 6, not that it was universally optimal.

Its main limitations are:

- It is a single realized batch with no exact replicate.
- Its apparent robustness is inferred from batch 6, which matched concentration and selector but used half the volume; that is a scale comparison, not a same-condition reproducibility test.
- It occupies only one concentration, scale, entity, temperature, and procedural history.
- Its high precipitation could be sensitive to particle history or assay timing.
- The selected condition was not compared with a dense local neighborhood, so it is not established as a local optimum.
- The recommendation says nothing about transfer to different anonymous materials, different benchmark worlds, or real chemical systems.

A proper validation sequence would include exact repeats of batch 8, neighboring concentrations such as 0.30, 0.40, and 0.50 M, neighboring volumes around 0.080 L, controlled waiting and stirring variations, and matched tests in the other selectors. Cross-world validation would require replay under independently instantiated worlds while preserving the same public recipe and scoring contract. Cross-material generalization would require new selectors or formulations, not merely another batch of selector 1.

Finally, “sample-in highest” and “proved optimal” must be separated. Batch 8 had a strong response and served the chosen scientific comparison well, but it was selected from only twelve structured observations. Even if it happened to have the highest observed scalar score, that would make it the sample-in maximum among tested batches, not proof of global or even local optimality. K1 correctly framed it as an evidentiary anchor; interpreting it as a universally recommended optimum would exceed the evidence.

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean width | Interval score |
|---|---:|---:|---:|---:|
| pH_normalized | 0.023131 | 0.716667 | 0.0455 | 0.122385 |
| acid_dissociation_fraction | 0.0141137 | 0.716667 | 0.0151667 | 0.0988467 |
| precipitation_signal | 0.00415533 | 0.983333 | 0.0268333 | 0.028333 |

## Entity-map and scale-transfer evaluation

| Concentration M | Pairwise entity-contrast MAE |
|---:|---:|
| 0.005 | 0.0303128 |
| 0.08 | 0.00331272 |
| 0.6 | 0.00296665 |

| Selector | Same-concentration scale-gap MAE |
|---:|---:|
| 0 | 0.00176991 |
| 1 | 0.0016389 |
| 2 | 0.00178524 |

## Evidence boundary

The participant received exactly K1, Q, and K2, in that order. K1 is the primary open-form entity-mechanism artifact. No candidate property vector, numerical entity constant, hidden truth, or score was shown before K2 sealed. Reference truth was generated only after all 15 K2 responses sealed. The common direct weak-acid/free-ion-precipitation topology was fixed across worlds and arms; the task was entity mapping, not operation optimization.
