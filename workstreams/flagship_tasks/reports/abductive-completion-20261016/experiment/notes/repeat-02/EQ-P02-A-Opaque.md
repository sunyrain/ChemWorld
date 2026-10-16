# repeat-02/EQ-P02-A-Opaque

Status: completed; source assays 12/12; public note versions 2.

Physical differences below describe the selected actions under matched worlds. They do not establish that an agent proposed or tested an explanation. All notebook versions, including terminal revisions, follow verbatim.

| Assay | End event | Prior note | First later note | Mean gap / assay SD: pH, free acid, precipitate |
| --- | --- | --- | --- | --- |
| 1 | 6 | 1 | 2 | 0.029, 0.814, 0.000 |
| 2 | 12 | 1 | 2 | 0.072, 1.217, 0.000 |
| 3 | 18 | 1 | 2 | 0.717, 3.035, 0.000 |
| 4 | 24 | 1 | 2 | 1.333, 3.722, 0.000 |
| 5 | 30 | 1 | 2 | 4.534, 4.796, 0.000 |
| 6 | 36 | 1 | 2 | 7.015, 4.792, 0.000 |
| 7 | 42 | 1 | 2 | 15.631, 3.663, 0.000 |
| 8 | 48 | 1 | 2 | 20.281, 2.960, 0.000 |
| 9 | 54 | 1 | 2 | 14.475, 0.352, 4.988 |
| 10 | 60 | 1 | 2 | 7.137, 0.067, 8.689 |
| 11 | 66 | 1 | 2 | 1.290, 0.005, 12.827 |
| 12 | 72 | 1 | 2 | 0.000, 0.000, 8.410 |

## Revision 1

Available operation events: 0.

# Aqueous equilibrium hypotheses

## H1 [tentative; prediction before autonomous experiments]
In water near ambient conditions, increasing total acid concentration will lower pH and usually lower the free dissociation fraction, consistent with an effective weak-acid mass-action response. At matched total concentration, changing volume alone should have little effect; at matched moles, dilution should increase dissociation.

## H2 [tentative; prediction before autonomous experiments]
The precipitation proxy will remain near zero at low concentration but may turn on above a finite loading/concentration threshold, potentially breaking a simple homogeneous weak-acid relationship. A concentration series spanning the supplied micromolar reference through concentrated conditions, paired at two volumes, will distinguish concentration control from an independent amount/volume effect.

Final-assay uncertainty scales supplied publicly are about 0.002 in normalized pH and 0.006 in each fraction; isolated differences comparable to those scales will not be treated as established effects. Equivalent explanations (activity corrections, self-association, or precipitation removing neutral acid) will remain unresolved without discriminating evidence.

## Revision 2

Available operation events: 72.

# Aqueous equilibrium hypotheses — source-stage final

## H1 [supported within the dilute aqueous scope]
Across the final assays, raising analytical concentration from about 7.5×10⁻⁶ to 2.5×10⁻² mol L⁻¹ lowered pH and lowered the free dissociation fraction (events runner-operation-0006 through runner-operation-0048). In this range, the effective monoprotic expression
`K_eff = [H+] alpha/(1-alpha-P)`, with `[H+]=10^(-14 pH_normalized)` and precipitation fraction `P`, gives roughly 1.2–1.6×10⁻⁵ mol L⁻¹ from individual final assays. This is an empirical collapse, not an identity assignment.

The 0.08 L, 6×10⁻⁷ mol repeat (runner-operation-0006) is close to supplied R01 relative to the declared assay noise, supporting local repeatability. Doubling concentration by halving volume produces the predicted lower pH/lower dissociation trend throughout the dilute series.

## H2 [supported qualitatively; threshold shape unresolved]
Precipitation is indistinguishable from the zero floor through approximately 0.025 mol L⁻¹ in the precise final assays, then rises at 0.125, 0.25, 0.5, and 1.0 mol L⁻¹ (runner-operation-0054, -0060, -0066, -0072), reaching about 0.095 at the highest tested concentration. Because isolated low-level positive readings are comparable to measurement noise, they are not evidence of precipitation below this region. The onset may be smooth rather than a sharp solubility threshold; the grid is too coarse to decide.

## H3 [concentration control supported; independent volume effect unresolved but constrained]
Same-concentration cross-links were created by comparing a final assay at 0.08 L with the half-loading pH-meter observation at 0.04 L in the paired next batch (for example runner-operation-0054 versus -0057, and -0066 versus -0069). Their pH, dissociation, and precipitation responses broadly agree within the different instruments' stated noise scales. This favors total concentration/loading per liquid volume as the main control rather than volume or absolute moles separately. A small independent volume effect is not excluded because these are single cross-instrument comparisons and the intermediate measurement slightly consumes sample.

## H4 [simple homogeneous model rejected outside dilute scope]
At ≥0.125 mol L⁻¹, the measured hydrogen concentration is no longer compatible with `[H+] ≈ alpha C_total`, and the apparent `K_eff` derived above rises strongly (to order 10⁻⁴–10⁻³ mol L⁻¹ by the highest points). Since alpha is near its assay noise floor there and precipitation is nonzero, a single ideal weak-acid equation should not be extrapolated into the concentrated region. Equivalent explanations still include activity/concentration-scale effects, additional acid-bearing equilibria, and a precipitation-coupled response; these data do not uniquely distinguish them.

## Decisions and future discriminators
Use the dilute `K_eff` only as a local empirical relationship, with uncertainty dominated by assay noise, sparse replication, and ideal-concentration assumptions rather than a fitted formal error bar. Treat the high-loading relationship as phenomenological and monotone. Replicated points around 0.03–0.15 mol L⁻¹, all on the final assay, would distinguish a true precipitation threshold from a smooth proxy response; matched concentration at several independent volumes would more sharply test residual volume effects.

## Sealed K1

## 1. Public background and definitions

This is a bounded synthetic aqueous weak-acid/precipitation world, not a model of general aqueous chemistry. The anonymous reagent has no public real-material identity. All autonomous experiments used water near 298 K; temperature, solvent identity, pressure, and time were not varied.

Public definitions are:
- `pH_normalized = pH/14`.
- Acid dissociation fraction, alpha, is the free deprotonated-acid fraction relative to total acid feed.
- Precipitation signal, P, is the precipitated-acid fraction relative to total acid feed.
- Equilibrium confidence is an environment diagnostic, not my scientific confidence.

Declared one-standard-deviation measurement noise was approximately 0.002, 0.006, and 0.006 for final-assay normalized pH, alpha, and P, respectively. Corresponding pH-meter values were 0.004, 0.015, and 0.020. Values clipped at zero therefore cannot establish very small precipitation signals. No archival local law or material dossier was supplied.

Two preliminary final-assay observations were public. R01 used 6.0e-7 mol in 0.080 L and returned normalized pH 0.37602, alpha 0.73706, and P 0.00425. R02 used the same amount in 0.075 L and returned 0.37660, 0.71974, and 0. These observations alone did not determine a mechanism.

## 2. Autonomous observations

Twelve completed aqueous batches covered nominal final analytical concentrations from 7.5e-6 to 1.0 mol/L. Each batch also had a pH-meter observation after half of its final reagent loading, followed by the final assay after the remaining reagent was added. Nominal concentration below means total added moles divided by initial water volume; the intermediate meter removed 3e-5 L, making actual final concentrations only about 0.04–0.08% higher.

Final-assay endpoints were:

| Batch | Water (L) | Total loading (mol) | Nominal C (mol/L) | Normalized pH | pH | Alpha | P |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.080 | 6.0e-7 | 7.5e-6 | 0.37283 | 5.220 | 0.73228 | 0 |
| 2 | 0.040 | 6.0e-7 | 1.5e-5 | 0.35706 | 4.999 | 0.61545 | 0.00601 |
| 3 | 0.080 | 1.0e-5 | 1.25e-4 | 0.31729 | 4.442 | 0.29297 | 0.00418 |
| 4 | 0.040 | 1.0e-5 | 2.5e-4 | 0.30474 | 4.266 | 0.21730 | 0.00546 |
| 5 | 0.080 | 1.0e-4 | 1.25e-3 | 0.27917 | 3.908 | 0.09405 | 0 |
| 6 | 0.040 | 1.0e-4 | 2.5e-3 | 0.26286 | 3.680 | 0.06197 | 0.00445 |
| 7 | 0.080 | 1.0e-3 | 1.25e-2 | 0.24072 | 3.370 | 0.03489 | 0 |
| 8 | 0.040 | 1.0e-3 | 2.5e-2 | 0.23164 | 3.243 | 0.01995 | 0 |
| 9 | 0.080 | 1.0e-2 | 0.125 | 0.16964 | 2.375 | 0.00633 | 0.02646 |
| 10 | 0.040 | 1.0e-2 | 0.250 | 0.13602 | 1.904 | 0.01221 | 0.05211 |
| 11 | 0.080 | 4.0e-2 | 0.500 | 0.10209 | 1.429 | 0.00712 | 0.07515 |
| 12 | 0.040 | 4.0e-2 | 1.000 | 0.07097 | 0.994 | 0.00651 | 0.09488 |

Batch 1 locally reproduced R01: its normalized-pH difference was 0.0032, alpha difference 0.0048, and precipitation results were both at the noise/floor scale.

The intermediate observations supplied useful same-concentration cross-links. For example, batch 3 final and batch 4 half-loading both had nominal C = 1.25e-4 mol/L. Their normalized pH values were 0.31729 and 0.31313, alpha values 0.29297 and 0.28197, and P values 0.00418 and 0.00062. Batch 9 final and batch 10 half-loading both represented 0.125 mol/L: normalized pH was 0.16964 versus 0.16307, alpha 0.00633 versus 0.00821, and P 0.02646 versus 0.02885. Batch 11 final and batch 12 half-loading both represented 0.5 mol/L: normalized pH was 0.10209 versus 0.10368, alpha 0.00712 versus a zero-floor reading, and P 0.07515 versus 0.05523. These comparisons used different instruments and are single observations, so small differences are not resolved effects.

Final equilibrium residuals were between zero and 0.00644. Final environment-diagnostic equilibrium confidence rose from about 0.45 in the most dilute batches to a maximum of about 0.87 in batch 6, then declined to about 0.65 at the highest loading. I do not interpret this diagnostic as a confidence interval or mechanistic probability.

## 3. Supported empirical relationships

### Loading, dilution, and pH

Increasing total concentration strongly and monotonically lowered pH over the tested range: approximately pH 5.22 at 7.5e-6 mol/L, 3.24 at 0.025 mol/L, and 0.99 at 1.0 mol/L. For a fixed number of moles, halving water volume approximately doubled concentration and produced lower pH. The same-concentration cross-links at different volumes broadly agreed within the stated cross-instrument noise. Thus concentration, total loading divided by liquid volume, is the principal supported control variable. An additional small effect of absolute volume or absolute moles remains possible but was not resolved.

Dilution therefore raises pH and increases the free dissociation fraction within this experimental slice. Conversely, concentration lowers both pH and alpha.

### Dilute acid dissociation

From about 7.5e-6 through 0.025 mol/L, alpha fell from approximately 0.73 to 0.020 as concentration increased. A useful local monoprotic empirical representation is

`K_eff = [H+] alpha / (1 - alpha - P)`, where `[H+] = 10^(-pH)`.

Applied individually to the final assays through 0.025 mol/L, this gives roughly 1.2e-5 to 1.65e-5 mol/L, centered near 1.5e-5 mol/L. In much of that dilute range, `[H+]` is also broadly consistent with `alpha*C_total`, as expected when the measured deprotonated fraction provides the dominant hydrogen-ion countercharge.

This is a supported local effective relationship, not proof of a unique molecular mechanism or a formal thermodynamic dissociation constant. I did not fit a statistically justified confidence interval, and the endpoints are sparse single measurements.

### Precipitation

Precise final assays from 7.5e-6 through 0.025 mol/L returned P between zero and 0.006. Those values are at or below the declared 0.006 assay noise and do not establish precipitation in that range. Clear positive precipitation was observed by 0.125 mol/L: P was 0.0265 in batch 9, then 0.0521, 0.0752, and 0.0949 at 0.25, 0.5, and 1.0 mol/L. The data therefore bracket a transition region above 0.025 mol/L and clearly active by 0.125 mol/L. The single intermediate observation at 0.0625 mol/L was at the zero floor, but its pH-meter precipitation noise was 0.020, so it does not tightly locate the onset.

The observed high-concentration response is monotone, but the grid is too coarse to determine whether it represents a sharp solubility threshold, a smooth saturation curve, or another bounded response.

## 4. Model limitation and competing explanations

A single ideal homogeneous weak-acid equation should be rejected as a global model. At 0.125 mol/L and above, alpha lies near its approximately 0.006 final-assay noise scale, precipitation is nonzero, and measured `[H+]` is no longer compatible with the simple dilute approximation `[H+] = alpha*C_total`. The apparent `K_eff` consequently rises from order 1e-5 in the dilute region to order 1e-4–1e-3 at the highest concentrations. That change is evidence of model breakdown, not evidence that one intrinsic constant literally changes by that amount.

Observationally equivalent or partly equivalent explanations include:
1. Strong activity-coefficient effects, so analytical concentrations cannot substitute for activities at high loading.
2. Additional acid-bearing equilibria, association, or more than one effective dissociation channel.
3. Precipitation removing or redistributing acid-bearing material and coupling to the measured aqueous response.
4. A combination of precipitation and nonideal activity effects.
5. Instrument-floor effects in alpha at high loading, which make ratios involving alpha unstable.

The present measurements cannot uniquely distinguish these explanations. The anonymous material identity and hidden species mapping preclude a justified named-species mechanism.

## 5. Uncertainty and scope

The strongest conclusions are directional: concentration lowers pH and alpha, dilution reverses those trends, and precipitation becomes appreciable at high concentration. The approximate dilute `K_eff` is supported only over the water/ambient-condition range tested, especially up to about 0.025 mol/L. It should not be extrapolated into the precipitation-bearing concentrated regime.

Important limitations are one final replicate per autonomous endpoint, different noise levels for intermediate and final instruments, zero clipping of small precipitation values, sparse coverage between 0.025 and 0.125 mol/L, and no independent variation of temperature, electrolyte profile, solvent composition, or equilibration time. The same-concentration comparisons constrain a large independent volume effect but do not exclude a subtle one.

A discriminating follow-up, if laboratory access were available, would use replicated final assays at several concentrations between about 0.03 and 0.15 mol/L and reproduce each concentration using multiple independently chosen amount/volume combinations. That would test threshold versus smooth precipitation, quantify any residual absolute-volume effect, and determine whether the dilute effective relationship fails before or only after precipitation becomes detectable.

## Sealed Q

{
  "predictions": [
    {
      "query_id": "Q01",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.2681,
          "lower80": 0.258,
          "upper80": 0.278
        },
        "acid_dissociation_fraction": {
          "estimate": 0.0723,
          "lower80": 0.052,
          "upper80": 0.093
        },
        "precipitation_signal": {
          "estimate": 0.002,
          "lower80": 0,
          "upper80": 0.014
        }
      },
      "rationale": "At 0.002 mol/L, log-concentration interpolation between batches 5 and 6 predicts lower pH and dissociation than batch 5 but little detectable precipitation. The 0.02 L scale is below the experimentally tested final volumes, so the intervals include extra scale uncertainty."
    },
    {
      "query_id": "Q02",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.2508,
          "lower80": 0.24,
          "upper80": 0.262
        },
        "acid_dissociation_fraction": {
          "estimate": 0.0472,
          "lower80": 0.03,
          "upper80": 0.065
        },
        "precipitation_signal": {
          "estimate": 0.001,
          "lower80": 0,
          "upper80": 0.014
        }
      },
      "rationale": "The concentration lies between batches 6 and 7, where normalized pH and dissociation declined smoothly and precise final assays showed no resolved precipitation. Uncertainty covers assay noise, interpolation, and the untested 0.02 L scale."
    },
    {
      "query_id": "Q03",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.2346,
          "lower80": 0.224,
          "upper80": 0.245
        },
        "acid_dissociation_fraction": {
          "estimate": 0.0248,
          "lower80": 0.01,
          "upper80": 0.041
        },
        "precipitation_signal": {
          "estimate": 0.001,
          "lower80": 0,
          "upper80": 0.015
        }
      },
      "rationale": "This point is bracketed closely by batches 7 and 8 at 0.0125 and 0.025 mol/L. Both had precipitation at the zero floor, while pH and dissociation followed the dilute concentration trend."
    },
    {
      "query_id": "Q04",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.1979,
          "lower80": 0.181,
          "upper80": 0.215
        },
        "acid_dissociation_fraction": {
          "estimate": 0.0125,
          "lower80": 0,
          "upper80": 0.028
        },
        "precipitation_signal": {
          "estimate": 0.014,
          "lower80": 0,
          "upper80": 0.033
        }
      },
      "rationale": "At 0.06 mol/L, the batch lies in the sparsely sampled transition between batch 8 at 0.025 mol/L and batch 9 at 0.125 mol/L. The central values interpolate those observations, but the precipitation interval is wide because a sharp threshold and a smooth onset remain observationally equivalent."
    },
    {
      "query_id": "Q05",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.1468,
          "lower80": 0.134,
          "upper80": 0.16
        },
        "acid_dissociation_fraction": {
          "estimate": 0.0103,
          "lower80": 0,
          "upper80": 0.023
        },
        "precipitation_signal": {
          "estimate": 0.044,
          "lower80": 0.025,
          "upper80": 0.064
        }
      },
      "rationale": "The concentration is directly bracketed by batches 9 and 10 at 0.125 and 0.25 mol/L. Their results support appreciable precipitation and a concentrated-regime departure from the simple dilute weak-acid relationship; alpha is near its assay noise scale."
    },
    {
      "query_id": "Q06",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.0939,
          "lower80": 0.08,
          "upper80": 0.108
        },
        "acid_dissociation_fraction": {
          "estimate": 0.007,
          "lower80": 0,
          "upper80": 0.017
        },
        "precipitation_signal": {
          "estimate": 0.08,
          "lower80": 0.06,
          "upper80": 0.101
        }
      },
      "rationale": "Interpolation between batches 11 and 12 at 0.5 and 1.0 mol/L predicts strongly acidic conditions, alpha near the measurement floor, and substantial precipitation. The interval also reflects uncertainty in the nonideal high-loading response and the smaller 0.02 L scale."
    },
    {
      "query_id": "Q07",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.1979,
          "lower80": 0.184,
          "upper80": 0.212
        },
        "acid_dissociation_fraction": {
          "estimate": 0.0125,
          "lower80": 0.001,
          "upper80": 0.026
        },
        "precipitation_signal": {
          "estimate": 0.014,
          "lower80": 0,
          "upper80": 0.033
        }
      },
      "rationale": "The predicted response is concentration-controlled and therefore matches Q04 centrally. A 0.04 L volume lies within the tested volume range, so its interval is slightly narrower, although uncertainty about precipitation onset around 0.06 mol/L remains."
    },
    {
      "query_id": "Q08",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.1979,
          "lower80": 0.177,
          "upper80": 0.219
        },
        "acid_dissociation_fraction": {
          "estimate": 0.0125,
          "lower80": 0,
          "upper80": 0.03
        },
        "precipitation_signal": {
          "estimate": 0.014,
          "lower80": 0,
          "upper80": 0.037
        }
      },
      "rationale": "Concentration collapse predicts the same center as Q04 and Q07. Because 0.01 L is below all tested final volumes, the interval is widened to allow an unresolved absolute-volume or finite-scale effect."
    },
    {
      "query_id": "Q09",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.1468,
          "lower80": 0.132,
          "upper80": 0.162
        },
        "acid_dissociation_fraction": {
          "estimate": 0.0103,
          "lower80": 0,
          "upper80": 0.025
        },
        "precipitation_signal": {
          "estimate": 0.044,
          "lower80": 0.022,
          "upper80": 0.068
        }
      },
      "rationale": "Its final concentration equals Q05, so an equilibrium, state-variable interpretation predicts the same center. The staged addition path was not tested directly in K1; intervals are widened to cover possible precipitation-path or mixing history effects."
    },
    {
      "query_id": "Q10",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.1468,
          "lower80": 0.132,
          "upper80": 0.162
        },
        "acid_dissociation_fraction": {
          "estimate": 0.0103,
          "lower80": 0,
          "upper80": 0.025
        },
        "precipitation_signal": {
          "estimate": 0.044,
          "lower80": 0.022,
          "upper80": 0.068
        }
      },
      "rationale": "The final amount, volume, and concentration match Q05 and Q09. No observed evidence supported order dependence, so the central prediction is unchanged, while the interval allows for the untested split-addition path."
    },
    {
      "query_id": "Q11",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.0939,
          "lower80": 0.076,
          "upper80": 0.112
        },
        "acid_dissociation_fraction": {
          "estimate": 0.007,
          "lower80": 0,
          "upper80": 0.02
        },
        "precipitation_signal": {
          "estimate": 0.08,
          "lower80": 0.055,
          "upper80": 0.106
        }
      },
      "rationale": "The 0.6 mol/L concentration is bracketed by batches 11 and 12 and should give the same central equilibrium response as Q06 and Q12. The 0.01 L volume is outside the tested scale, so this prediction receives the widest scale-control intervals."
    },
    {
      "query_id": "Q12",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.0939,
          "lower80": 0.081,
          "upper80": 0.107
        },
        "acid_dissociation_fraction": {
          "estimate": 0.007,
          "lower80": 0,
          "upper80": 0.017
        },
        "precipitation_signal": {
          "estimate": 0.08,
          "lower80": 0.06,
          "upper80": 0.101
        }
      },
      "rationale": "At 0.6 mol/L and 0.04 L, this is an interpolation within both the tested concentration and volume ranges. Batches 11 and 12 support high precipitation, very low dissociation, and low normalized pH; alpha uncertainty remains large relative to its near-floor estimate."
    }
  ],
  "rationale": "Point estimates use interpolation in log concentration through the sealed K1 final-assay observations, with concentration treated as the principal state variable. The intervals combine declared final-assay observation noise with sparse-grid and model uncertainty. They are widened near the unresolved precipitation onset, for 0.01–0.02 L volumes outside the tested 0.04–0.08 L final-volume range, and for untested addition paths. No equilibrium-confidence values were used as epistemic uncertainty."
}

## Sealed K2

## 1. Supported, contradicted, and untested relationships

**Supported in this bounded world:** Increasing analytical loading per liquid volume lowers pH and generally lowers the free acid-dissociation fraction. Dilution produces the opposite response. Same-concentration cross-links at different amount/volume combinations broadly agreed within cross-instrument uncertainty, so concentration is the principal observed control variable. From approximately 7.5e-6 to 0.025 mol/L, the results are compatible with a local effective monoprotic relationship having `K_eff` of roughly 1.2e-5 to 1.65e-5 mol/L. Precipitation was not resolved above the measurement floor through 0.025 mol/L, but was clearly positive at 0.125 mol/L and increased through 1.0 mol/L.

**Contradicted:** A single ideal, homogeneous weak-acid equation is contradicted as a global description. At 0.125 mol/L and above, measured hydrogen concentration, alpha, and total concentration no longer satisfy the dilute approximation `[H+] ≈ alpha*C_total`; precipitation is also nonzero. The observations likewise contradict a globally negligible-precipitation account.

**Untested or only weakly tested:** Independent absolute-volume effects were constrained but not eliminated. Addition-order and staging effects, hysteresis, equilibration-time dependence, temperature dependence, other solvents, electrolyte effects, and reversibility of precipitation were not tested. A sharp precipitation threshold was not distinguished from a smooth onset. No molecular identity or unique hidden-species mechanism was established.

## 2. Observations that changed the account

There were actual observations, and several materially changed the account.

The dilute sequence from batches 1–8 confirmed the anticipated direction of the weak-acid response and supported a local effective dissociation relationship. Batch 1 also agreed locally with preliminary assay R01, increasing confidence that the dilute behavior was repeatable at the available resolution.

The most consequential changes came from batches 9–12. At 0.125, 0.25, 0.5, and 1.0 mol/L, precipitation signals were about 0.0265, 0.0521, 0.0752, and 0.0949. These observations converted precipitation from a tentative possibility into a supported high-loading feature. Simultaneously, alpha approached its assay noise floor while pH continued falling strongly. That combination forced rejection of the initial simple weak-acid representation outside the dilute range.

Same-concentration cross-links—such as batch 3 final versus batch 4 half-loading at 1.25e-4 mol/L, and batch 9 final versus batch 10 half-loading at 0.125 mol/L—shifted the account toward concentration as the principal control rather than independent dependence on total moles or volume. Because these comparisons used different instruments and were not replicated, they did not eliminate smaller scale effects.

## 3. Competing explanations

Some explanations are partly distinguishable. An ideal dilute weak-acid model is adequate locally but distinguishable from, and inferior to, a nonideal or coupled model at high loading. A large independent volume effect is disfavored by the same-concentration cross-links.

Several high-loading explanations remain unresolved: activity-coefficient changes; acid association or additional dissociation channels; precipitation removing or redistributing acid-bearing material; and combinations of these processes. Near-floor alpha measurements make apparent dissociation constants especially unstable at high concentration. The data also cannot distinguish a true solubility threshold from a smooth saturating precipitation proxy. Hidden species mapping and anonymous material identity prevent assigning a unique named chemical mechanism.

## 4. Best single next legal experiment

I would prepare one aqueous batch with 0.080 L water and 0.0048 mol reagent, giving 0.060 mol/L, then terminate and measure it with the final assay. This lies inside the allowed per-operation ranges and targets the largest evidentiary gap between the precise final assays at 0.025 and 0.125 mol/L.

If precipitation were at the zero/noise floor, approximately 0–0.006, it would support an onset above 0.060 mol/L and make my Q04/Q07/Q08 central precipitation estimates too high. A result around 0.01–0.02 would support a smooth onset and the interpolation used in Q. A result near or above 0.025 would support an earlier or steeper transition and would contradict the assumed gradual interpolation. Its pH and alpha would simultaneously test whether the concentration trend remains smooth before clearly established precipitation. One batch would not establish repeatability, but it would provide the greatest discrimination per final assay.

## 5. Limits of the characterization evidence

There was only one autonomous final assay per endpoint, with sparse concentration coverage and no independent final-assay replicates. Small precipitation readings are difficult to interpret because the signal is bounded at zero and final-assay noise is about 0.006. High-loading alpha values are comparable to their own noise scale. Intermediate and final observations used instruments with different uncertainties, and intermediate sampling slightly changed volume.

All experiments used water near ambient temperature. No temperature, pressure, solvent-composition, electrolyte, mixing, or time series was studied. The nominal concentration range was broad, but the critical 0.025–0.125 mol/L precipitation region was poorly resolved. Consequently, the work supports an empirical map and a dilute local relationship, not a complete thermodynamic model, kinetic account, or unique mechanism.

## 6. Least reliable Q forecasts

Q04, Q07, and Q08 are least reliable for precipitation because all are at 0.060 mol/L, directly inside the unresolved onset region. Q08 is additionally weak because its 0.010 L scale is below the 0.040–0.080 L final-volume range tested.

Q11 is also comparatively weak because it combines a 0.600 mol/L nonideal regime with an untested 0.010 L scale. Q06 and Q12 are better scale matches but still rely on interpolation within a regime where the dilute law has failed and alpha is near the assay floor.

Q09 and Q10 are uncertain with respect to path because staged versus solvent-first split addition was never experimentally compared. Their shared central prediction follows an equilibrium state-function assumption rather than direct evidence of path independence.

The pH forecasts are generally more reliable than the alpha forecasts at high concentration. Predictions for high-loading alpha can easily shift within their intervals because the expected signal is comparable to assay noise. None of these forecasts directly violates the sealed scope, but their point-estimate precision should not be mistaken for equivalent evidentiary precision.

## 7. Limits on generalization

Generalization to new loadings is strongest for interpolation inside the observed concentration range and weakest across the precipitation transition or beyond 1.0 mol/L. Generalization under dilution assumes that concentration remains the governing variable; it becomes weaker at volumes below 0.040 L or above 0.080 L because independent scale effects were not decisively excluded.

Generalization across preparation paths assumes rapid equilibration and no persistent nucleation, aggregation, or mixing history. Those assumptions were not tested. Generalization to other solvents, temperatures, electrolyte environments, identities, or real chemical systems is unsupported. Finally, because this is a bounded synthetic world with anonymous species and hidden mechanism mapping, even a successful empirical relationship here should not be treated as a universal acid-dissociation or precipitation law, nor transferred to another world without new calibration evidence.
