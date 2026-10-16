# repeat-01/EQ-P01-B-Opaque

Status: completed; source assays 12/12; public note versions 3.

Physical differences below describe the selected actions under matched worlds. They do not establish that an agent proposed or tested an explanation. All notebook versions, including terminal revisions, follow verbatim.

| Assay | End event | Prior note | First later note | Mean gap / assay SD: pH, free acid, precipitate |
| --- | --- | --- | --- | --- |
| 1 | 6 | 1 | 2 | 0.147, 2.032, 0.000 |
| 2 | 12 | 1 | 2 | 0.062, 1.417, 0.000 |
| 3 | 18 | 1 | 2 | 0.035, 1.113, 0.000 |
| 4 | 24 | 1 | 2 | 0.023, 0.924, 0.000 |
| 5 | 30 | 2 | 3 | 3.793, 0.036, 12.201 |
| 6 | 36 | 2 | 3 | 9.809, 0.226, 7.968 |
| 7 | 42 | 2 | 3 | 13.954, 0.557, 5.580 |
| 8 | 48 | 2 | 3 | 17.065, 1.015, 3.857 |
| 9 | 54 | 2 | 3 | 0.000, 0.000, 5.604 |
| 10 | 60 | 2 | 3 | 0.000, 0.000, 11.213 |
| 11 | 66 | 2 | 3 | 0.400, 0.002, 15.270 |
| 12 | 72 | 2 | 3 | 2.203, 0.016, 13.563 |

## Revision 1

Available operation events: 0.

# Source-stage hypothesis notebook

## H1 [tentative; prediction before autonomous experiments]
For water-only batches near ambient conditions, increasing total acid loading at fixed liquid volume should lower pH and the free deprotonated fraction. Dilution at fixed acid amount should raise both. A precipitation proxy may remain near zero at low concentration and appear nonlinearly above a concentration/loading threshold. Equivalent effective explanations include concentration-dependent weak-acid mass action, activity-coefficient changes, and removal of neutral/deprotonated material by a solubility limit; these are not yet distinguishable.

**Planned test.** Use a 3 x 4 endpoint grid of acid amount (approximately 6e-7, 0.006, 0.030 mol) and water volume (0.02, 0.04, 0.06, 0.08 L), with a pH-meter observation at half the endpoint loading and a final assay after the second addition. Replicate-like overlap and supplied references R01/R02 will help assess noise. I will treat differences cautiously relative to stated channel noise and will revise the grid interpretation if staged addition shows unexpected directionality.

**Scope.** Anonymous acid in the bounded benchmark, water, near initial ambient temperature; no claim yet about named chemistry or other solvents.

## Revision 2

Available operation events: 24.

# Source-stage hypothesis notebook

## H1 [supported in the low-loading water scope]
At total acid feed 6e-7 mol, dilution from 0.02 to 0.08 L raises pH_normalized and free dissociation. Final assays span pH_normalized about 0.342 to 0.375 and dissociation about 0.545 to 0.790 (runner-operation-0006, -0012, -0018, -0024). The 0.08 L endpoint agrees closely with supplied R01/R02, while staged half-load pH-meter readings have the same directional pattern (runner-operation-0003, -0009, -0015, -0021). This supports concentration dependence rather than total moles alone in this range.

Small nonzero precipitation readings at very low loading are inconsistent across instruments/endpoints and comparable to stated measurement noise, so precipitation is treated as zero/unresolved here rather than evidence of a physical precipitate.

## H2 [tentative; prediction before higher-load tests]
If a simple weak-acid concentration relationship dominates before precipitation, raising feed concentration should lower pH and dissociation smoothly. If a solubility constraint appears, precipitation should rise nonlinearly and may decouple pH/dissociation from nominal total feed. The upcoming 0.006 and 0.030 mol grids test this; repeated concentrations created by different amount-volume combinations can distinguish concentration control from an independent total-loading or volume effect.

**Scope and alternatives.** Water-only, near ambient temperature. Effective concentration dependence could represent mass action, activities, or concentration-dependent association. Precipitation mechanism and solid identity remain unidentifiable from these channels alone.

## Revision 3

Available operation events: 72.

# Source-stage hypothesis notebook

## H1 [supported in tested water/ambient scope]
Nominal analytical concentration C = total acid feed / liquid volume is the dominant effective coordinate for pH across the tested endpoint grid. At each fixed feed, dilution raises pH_normalized (runner-operation-0006 to -0024; -0030 to -0048; -0054 to -0072). Descriptive least-squares fits of pH_normalized versus ln(C) have slopes -0.0236 at 7.5e-6 to 3e-5 M, -0.0247 at 0.075 to 0.30 M, and -0.0399 at 0.375 to 1.5 M. These are summaries, not a claimed universal law; the high-concentration segment is steeper and there is a large unsampled concentration gap.

The free deprotonated fraction likewise decreases strongly with concentration: final-assay values are about 0.545-0.790 in the micromolar grid (runner-operation-0006, -0012, -0018, -0024), but are at or near the zero boundary in the 0.075-1.5 M grids (runner-operation-0030 through -0072). Because many readings are clipped/noise-scale near zero, the data identify a collapse in free fraction, not its precise functional form.

## H2 [supported threshold-like precipitation proxy; mechanism unresolved]
Endpoint precipitation is indistinguishable from zero through 0.50 M, then rises to 0.034 at 0.75 M and 0.080 at 1.5 M (runner-operation-0066, -0060, -0054; final-assay channel SD 0.006). Thus a threshold-like onset between roughly 0.5 and 0.75 M is supported for these endpoint conditions. The staged pH-meter precipitation values have SD 0.02 and mostly remain noise-scale, so they do not finely locate onset.

A solubility limit is a parsimonious effective explanation, but precipitation_signal alone cannot identify which acid form precipitates, solid stoichiometry, nucleation kinetics, or whether high-concentration nonideality/association produces an equivalent bounded response. The concurrent steeper pH-concentration slope above 0.5 M is consistent with coupling but does not establish causation.

## H3 [unresolved total-loading/volume effects]
The grid strongly establishes dilution trends, but exact concentration-matched comparisons often use different instruments/stages (for example 0.75 M at runner-operation-0057 versus -0060). Instrument noise and staged-history differences confound a strict proof that C alone is sufficient. A future decisive test would use final assays at the same C with several total amounts/volumes and replication near 0.5-0.8 M.

## Decision and scope
Use batch 9 (0.030 mol in 0.020 L; runner-operation-0054) as the evidentiary anchor because it cleanly demonstrates the high-concentration regime and the strongest precipitation signal, while the rest of the grid supplies its contrast. Claims apply only to this anonymous bounded acid in water near ambient initial conditions; they do not establish named chemistry, temperature effects, or behavior in other solvents. Supplied R01/R02 and batch 4 agree at 6e-7 mol in 0.08 L, supporting repeatability at the dilute endpoint.

## Sealed K1

## 1. Public background

This is a bounded synthetic weak-acid/precipitation benchmark, not a model of general aqueous chemistry or an identified real acid. The reagent and mechanism-to-species mapping are anonymous, and no task-specific material dossier or prior local law was supplied. Water was the only solvent tested. The public definitions are: pH_normalized = pH/14; acid_dissociation_fraction = free deprotonated acid divided by total acid feed; precipitation_signal = precipitated acid divided by total acid feed. The stated final-assay standard deviations are 0.002 for pH_normalized, 0.006 for dissociation, and 0.006 for precipitation. Corresponding pH-meter standard deviations are 0.004, 0.015, and 0.020. Equilibrium_confidence is an environment diagnostic, not scientific confidence.

Two supplied preliminary final assays were actual public observations: 6e-7 mol in 0.080 L gave pH_normalized 0.374645, dissociation 0.774900, and precipitation 0; 6e-7 mol in 0.075 L gave 0.374918, 0.777236, and 0.

## 2. Experiments and actual observations

I completed 12 water batches near ambient temperature. Endpoint feed amounts were 6e-7, 0.006, or 0.030 mol, each crossed with liquid volumes of 0.020, 0.040, 0.060, and 0.080 L. In every batch, a pH-meter measurement was taken after half of the final feed had been added, followed by the second addition, termination, and a final assay. The final-assay endpoints are the primary comparable dataset:

| Batch | Feed (mol) | Volume (L) | Nominal C (mol/L) | pH_normalized | pH | Dissociation fraction | Precipitation signal |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 6e-7 | 0.020 | 3.0e-5 | 0.341788 | 4.785 | 0.544694 | 0.000643 |
| 2 | 6e-7 | 0.040 | 1.5e-5 | 0.356810 | 4.995 | 0.663268 | 0 |
| 3 | 6e-7 | 0.060 | 1.0e-5 | 0.366780 | 5.135 | 0.747505 | 0 |
| 4 | 6e-7 | 0.080 | 7.5e-6 | 0.374690 | 5.246 | 0.790026 | 0.003290 |
| 5 | 0.006 | 0.020 | 0.300 | 0.114640 | 1.605 | 0.000395 | 0.002269 |
| 6 | 0.006 | 0.040 | 0.150 | 0.131966 | 1.848 | 0.006344 | 0 |
| 7 | 0.006 | 0.060 | 0.100 | 0.139855 | 1.958 | 0 | 0.000441 |
| 8 | 0.006 | 0.080 | 0.075 | 0.149990 | 2.100 | 0.012572 | 0 |
| 9 | 0.030 | 0.020 | 1.500 | 0.051536 | 0.722 | 0.007898 | 0.080351 |
| 10 | 0.030 | 0.040 | 0.750 | 0.074664 | 1.045 | 0 | 0.034245 |
| 11 | 0.030 | 0.060 | 0.500 | 0.096772 | 1.355 | 0.001252 | 0.000232 |
| 12 | 0.030 | 0.080 | 0.375 | 0.105443 | 1.476 | 0 | 0.002823 |

Batch 4 closely reproduced the supplied dilute reference pH and broadly reproduced its dissociation fraction. The intermediate half-loading measurements independently showed the same dilution direction for pH. For example, batches 1–4 at half loading ranged from pH_normalized 0.3503 at 0.020 L to 0.3939 at 0.080 L, while dissociation rose from 0.662 to 0.883. Intermediate precipitation estimates were mostly noise-scale under the less precise pH-meter channel.

## 3. Supported empirical relationships

**Loading, volume, and pH.** At every fixed final amount, increasing water volume raised pH; equivalently, increasing nominal concentration lowered pH. Thus concentration or dilution is a strongly supported effective coordinate. Descriptive least-squares fits of pH_normalized against ln(C) had slopes of -0.0236 over 7.5e-6–3.0e-5 M, -0.0247 over 0.075–0.300 M, and -0.0399 over 0.375–1.50 M. These correspond to approximate pH changes of -0.76, -0.80, and -1.29 per tenfold concentration increase. The steeper high-concentration segment suggests curvature or a regime change; these fits are summaries rather than universal laws. There is a large unmeasured gap between 3e-5 and 0.075 M.

**Acid dissociation.** In the dilute final-assay range, dissociation increased monotonically with dilution, from 0.545 at 3e-5 M to 0.790 at 7.5e-6 M. In the 0.075–1.50 M endpoints it was at or very near the zero boundary, with all values no greater than 0.0126. This supports a large concentration-dependent collapse in the reported free deprotonated fraction. It does not resolve the detailed functional form because most concentrated results are comparable to the 0.006 final-assay uncertainty and some are clipped at zero.

**Precipitation.** Final-assay precipitation was indistinguishable from zero through 0.50 M. It then rose to 0.0342 at 0.75 M and 0.0804 at 1.50 M, well above the 0.006 channel standard deviation. Under these endpoint conditions, the observations therefore support a threshold-like onset between approximately 0.50 and 0.75 M, followed by a larger response with concentration. Batch 9 provides the clearest high-concentration anchor. The threshold is a statement about the normalized public proxy, not proof of a particular solid phase.

## 4. Inference versus conjecture

The inference most directly supported by the grid is that nominal concentration, rather than total moles alone, organizes pH and dilute dissociation behavior. However, concentration was produced by varying volume at fixed amount within each four-batch block. Exact concentration-matched final assays using independently varied amount and volume were not performed, so an additional total-loading or volume effect is not excluded.

A weak-acid mass-action picture is qualitatively compatible with higher dissociation on dilution. A simple ideal monoprotic model with one fixed dissociation constant is not established across the whole range: the reported dissociation nearly vanishes at moderate and high loading while pH remains strongly acidic, and the pH-concentration slope steepens in the highest range. Plausible competing effective explanations include concentration-dependent activity coefficients, association or oligomerization, an unobserved background electrolyte/proton reservoir, or coupling to precipitation. The public channels cannot distinguish these explanations or identify species.

A solubility-limit interpretation is a parsimonious conjecture for the precipitation onset. Alternatives include a bounded proxy responding to high-concentration association, nonideal phase behavior, or a nucleation/history effect. The coincidence of stronger precipitation and a steeper pH trend above roughly 0.5 M is consistent with coupling, but does not prove that precipitation causes the pH change or identify whether neutral or ionized acid precipitates.

## 5. Uncertainty, limitations, and scope

All autonomous endpoints were single final assays; the supplied dilute references provide only limited repeatability evidence. With the stated final-assay uncertainties, precipitation values below about 0.003 in batches 1–8 and 11–12 should be treated as zero/noise-scale, whereas batches 9 and 10 are clear positive signals. Concentrated dissociation values are poorly resolved because they lie near the lower bound. pH trends are much larger than the stated 0.002 normalized uncertainty and are consequently the most robust relationship.

No temperature series, equilibration-time series, other solvents, catalysts, electrolyte profiles, solid characterization, or direct species measurements were performed. The equilibrium diagnostic residuals were generally near zero, but that is an environment diagnostic and does not validate a chemical mechanism. Conclusions apply only to this anonymous bounded acid in water, near the tested ambient conditions, over the sampled concentration ranges. The most informative future tests would replicate final assays around 0.5–0.8 M, test several amount-volume pairs at identical concentration, and fill the wide 3e-5–0.075 M gap.

## Sealed Q

{
  "predictions": [
    {
      "query_id": "Q01",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.245,
          "lower80": 0.225,
          "upper80": 0.265
        },
        "acid_dissociation_fraction": {
          "estimate": 0.097,
          "lower80": 0.065,
          "upper80": 0.135
        },
        "precipitation_signal": {
          "estimate": 0.001,
          "lower80": 0,
          "upper80": 0.012
        }
      },
      "rationale": "At 0.002 M this batch lies in the large unsampled gap between the dilute and bulk observations. A concentration-based weak-acid interpolation predicts partial dissociation and pH between the two observed regimes. It is far below the observed precipitation onset, so the precipitation estimate is effectively zero; the interval is widened for interpolation uncertainty."
    },
    {
      "query_id": "Q02",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.218,
          "lower80": 0.198,
          "upper80": 0.238
        },
        "acid_dissociation_fraction": {
          "estimate": 0.057,
          "lower80": 0.033,
          "upper80": 0.085
        },
        "precipitation_signal": {
          "estimate": 0.001,
          "lower80": 0,
          "upper80": 0.012
        }
      },
      "rationale": "At 0.006 M, increased concentration should lower both pH and free dissociation relative to Q01. The point estimate follows the effective concentration relationship inferred from the dilute dissociation data and the transition toward the 0.075 M observations. No precipitation was supported anywhere near this concentration."
    },
    {
      "query_id": "Q03",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.187,
          "lower80": 0.17,
          "upper80": 0.203
        },
        "acid_dissociation_fraction": {
          "estimate": 0.032,
          "lower80": 0.012,
          "upper80": 0.054
        },
        "precipitation_signal": {
          "estimate": 0.001,
          "lower80": 0,
          "upper80": 0.012
        }
      },
      "rationale": "The 0.020 M endpoint remains in the unmeasured concentration gap, so model uncertainty dominates instrumental uncertainty. The inferred weak-acid relationship gives a small but resolved free fraction, while the pH trend continues downward approximately with log concentration. Precipitation remains effectively absent."
    },
    {
      "query_id": "Q04",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.156,
          "lower80": 0.147,
          "upper80": 0.165
        },
        "acid_dissociation_fraction": {
          "estimate": 0.018,
          "lower80": 0,
          "upper80": 0.039
        },
        "precipitation_signal": {
          "estimate": 0.001,
          "lower80": 0,
          "upper80": 0.012
        }
      },
      "rationale": "At 0.060 M this condition is close to the lowest observed bulk concentration, 0.075 M, making the pH interpolation comparatively well constrained. Dissociation should be small and is difficult to resolve against assay noise. This concentration is well below the supported precipitation threshold."
    },
    {
      "query_id": "Q05",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.121,
          "lower80": 0.113,
          "upper80": 0.13
        },
        "acid_dissociation_fraction": {
          "estimate": 0.01,
          "lower80": 0,
          "upper80": 0.025
        },
        "precipitation_signal": {
          "estimate": 0.001,
          "lower80": 0,
          "upper80": 0.013
        }
      },
      "rationale": "The 0.20 M condition is interpolated within the observed 0.075–0.30 M bulk range. The endpoint data support low pH, a dissociation fraction near the lower measurement boundary, and no meaningful precipitation. Model and assay uncertainty permit a small positive precipitation reading without implying a precipitated phase."
    },
    {
      "query_id": "Q06",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.089,
          "lower80": 0.078,
          "upper80": 0.099
        },
        "acid_dissociation_fraction": {
          "estimate": 0.006,
          "lower80": 0,
          "upper80": 0.019
        },
        "precipitation_signal": {
          "estimate": 0.012,
          "lower80": 0,
          "upper80": 0.035
        }
      },
      "rationale": "At 0.60 M this batch lies between the nonprecipitating 0.50 M endpoint and the positive 0.75 M endpoint. The pH and dissociation estimates are therefore local interpolations, while precipitation is the principal uncertainty: a small positive signal is expected, but zero remains plausible because the onset was only bounded to roughly 0.50–0.75 M."
    },
    {
      "query_id": "Q07",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.156,
          "lower80": 0.146,
          "upper80": 0.167
        },
        "acid_dissociation_fraction": {
          "estimate": 0.018,
          "lower80": 0,
          "upper80": 0.04
        },
        "precipitation_signal": {
          "estimate": 0.001,
          "lower80": 0,
          "upper80": 0.013
        }
      },
      "rationale": "This is a scale-control realization of the same 0.060 M endpoint as Q04. Concentration was the dominant supported coordinate, so the point estimates are nearly identical. The intervals are slightly wider because the sealed account could not exclude independent total-loading or volume effects."
    },
    {
      "query_id": "Q08",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.156,
          "lower80": 0.144,
          "upper80": 0.169
        },
        "acid_dissociation_fraction": {
          "estimate": 0.018,
          "lower80": 0,
          "upper80": 0.042
        },
        "precipitation_signal": {
          "estimate": 0.001,
          "lower80": 0,
          "upper80": 0.014
        }
      },
      "rationale": "This smaller-scale batch also ends at 0.060 M. Endpoint equilibrium is predicted to depend mainly on concentration, but 0.010 L is outside the autonomous endpoint-volume range, so the interval allows additional scale uncertainty. Precipitation should remain absent at this concentration."
    },
    {
      "query_id": "Q09",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.121,
          "lower80": 0.111,
          "upper80": 0.132
        },
        "acid_dissociation_fraction": {
          "estimate": 0.01,
          "lower80": 0,
          "upper80": 0.027
        },
        "precipitation_signal": {
          "estimate": 0.001,
          "lower80": 0,
          "upper80": 0.015
        }
      },
      "rationale": "The staged additions end at the same 0.20 M state as Q05. For a reversible equilibrium, the endpoint should be path-independent, so the same central prediction is used. The intervals are widened modestly because the experiments did not directly test whether staging affects equilibration or nucleation history."
    },
    {
      "query_id": "Q10",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.121,
          "lower80": 0.112,
          "upper80": 0.131
        },
        "acid_dissociation_fraction": {
          "estimate": 0.01,
          "lower80": 0,
          "upper80": 0.026
        },
        "precipitation_signal": {
          "estimate": 0.001,
          "lower80": 0,
          "upper80": 0.014
        }
      },
      "rationale": "The solvent-first sequence has the same final amount, volume, and concentration as Q05 and Q09. Concentration-based equilibrium predicts the same endpoint. This path avoids the transient concentrated state in Q09, so only modest untested path uncertainty is added."
    },
    {
      "query_id": "Q11",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.089,
          "lower80": 0.076,
          "upper80": 0.101
        },
        "acid_dissociation_fraction": {
          "estimate": 0.006,
          "lower80": 0,
          "upper80": 0.021
        },
        "precipitation_signal": {
          "estimate": 0.012,
          "lower80": 0,
          "upper80": 0.039
        }
      },
      "rationale": "This small-scale control shares the 0.60 M concentration of Q06. The concentration model gives the same center, but the 0.010 L volume is outside the observed endpoint range. Scale uncertainty and proximity to the precipitation onset broaden all intervals, especially that for precipitation."
    },
    {
      "query_id": "Q12",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.089,
          "lower80": 0.077,
          "upper80": 0.1
        },
        "acid_dissociation_fraction": {
          "estimate": 0.006,
          "lower80": 0,
          "upper80": 0.02
        },
        "precipitation_signal": {
          "estimate": 0.012,
          "lower80": 0,
          "upper80": 0.037
        }
      },
      "rationale": "This larger-scale control also ends at 0.60 M. Its volume is within the tested range, so concentration-based interpolation is favored, although its total loading differs from the nearest observations. A weak positive precipitation response is predicted, with an interval spanning zero because the threshold location remains uncertain."
    }
  ],
  "rationale": "Predictions use nominal concentration as the primary effective coordinate because all three observed loading series showed higher pH on dilution. Dissociation estimates follow the concentration-dependent weak-acid relationship supported by the dilute data, with wide bounded intervals where observed values approached zero. Precipitation is treated as absent below 0.5 M and as an uncertain onset process between 0.5 and 0.75 M. Intervals combine final-assay noise with larger model uncertainty in the unsampled concentration gap, near the precipitation threshold, and for untested scale or addition-path effects."
}

## Sealed K2

## 1. Supported, contradicted, and untested relationships

**Supported:** In the 12 observed water batches, dilution at fixed total feed consistently increased pH and, in the dilute series, increased the free deprotonated fraction. Nominal concentration therefore organizes much of the response. Final-assay precipitation was noise-scale through 0.50 M but clearly positive at 0.75 M and 1.50 M, supporting a threshold-like high-concentration regime. The dilute 6e-7 mol, 0.080 L result also broadly agreed with the two supplied reference assays.

**Contradicted or inadequate:** A concentration-independent response is contradicted. Total loading alone is inadequate because changing volume at fixed feed changed pH and dissociation. A single straight pH-versus-log-concentration law is also inadequate as an exact account because the high-concentration slope was steeper. A simple ideal monoprotic-acid model, without additional nonideality, charge balance, or coupled processes, does not simultaneously explain the strongly acidic pH and near-zero reported free dissociation at moderate and high loading. The hypothesis of zero precipitation throughout the domain is contradicted by batches 9 and 10.

**Untested:** Exact sufficiency of concentration, separate effects of total amount and volume, equilibrium path independence, equilibration time, temperature dependence, solvent dependence, reversibility of precipitation, hysteresis, and solid identity remain untested. No exact concentration-matched final-assay scale controls were observed.

## 2. Observations that changed the account

There were actual observations that changed the account. The low-loading series, batches 1–4, confirmed the anticipated dilution direction and established approximate reproducibility against the supplied references. Batches 5–8 changed the account more substantially: dissociation collapsed to values near the assay floor while pH became strongly acidic, so a smooth ideal weak-acid description alone was no longer sufficient. Batches 9 and 10 then produced precipitation signals of 0.0804 at 1.50 M and 0.0342 at 0.75 M, whereas batches 11 and 12 at 0.50 and 0.375 M remained noise-scale. This narrowed the observed precipitation onset to roughly 0.50–0.75 M and motivated a threshold-like rather than globally smooth precipitation account.

No observations were supplied after K1 was sealed. The Q conditions are forecast targets, not experimental outcomes, so they did not change the scientific account.

## 3. Competing explanations

Several explanations remain unresolved. Dilute dissociation is qualitatively compatible with weak-acid mass action, but activity-coefficient changes, association, or another concentration-dependent equilibrium could produce similar trends. The disagreement between pH acidity and the reported free deprotonated fraction at higher loading could reflect nonideal activities, an unobserved proton or charge-balance reservoir, association, or coupling to species not exposed by the public mapping.

The precipitation proxy is consistent with a solubility limit, but high-concentration association, phase-transition behavior, or nucleation/history dependence could produce an equivalent bounded signal. The available channels do not identify the precipitating form or solid stoichiometry. Concentration control also remains distinguishable from independent scale, volume, or total-loading effects because matched-concentration final assays were not observed. Finally, equilibrium path independence and kinetic history remain distinguishable in principle but unresolved experimentally.

## 4. Single next experiment

I would run one scale-control final assay at 0.75 M using 0.015 mol reagent in 0.020 L water: add 0.020 L water, add 0.015 mol reagent, terminate, and measure with the final assay. This is legal and directly compares with batch 10, which reached 0.75 M using 0.030 mol in 0.040 L.

If pH, dissociation, and precipitation reproduce batch 10 within measurement and process uncertainty, that would strengthen concentration as the sufficient endpoint coordinate and support a reproducible precipitation onset. If pH and dissociation agree but precipitation differs materially, nucleation, scale, or total amount would be implicated specifically in the phase response. If all channels differ, concentration alone would be rejected as a sufficient description. A near-zero precipitation result would weaken the claimed 0.50–0.75 M threshold and suggest either stochastic nucleation or a scale/loading dependence.

## 5. Evidential limits

The account rests on 12 single final-assay endpoints plus 12 less precise intermediate pH-meter measurements and two supplied dilute references. There were no autonomous endpoint replicates. A very large concentration gap exists between 3e-5 and 0.075 M. Many dissociation and precipitation estimates were near or clipped at zero, limiting functional identification. Intermediate and endpoint comparisons used instruments with different uncertainties and occurred at different stages, so they are not clean matched replicates.

Only water and near-ambient starting conditions were studied. There were no temperature, time, solvent, catalyst, electrolyte, reversibility, or solid-characterization studies. The precipitation measurement is a normalized public proxy rather than direct phase composition. Equilibrium_confidence and equilibrium_residual are environment diagnostics and cannot validate a proposed mechanism or substitute for scientific uncertainty.

## 6. Least reliable Q forecasts

Q01–Q03 are among the least reliable because their concentrations lie in the large unobserved gap; their pH and dissociation forecasts depend on interpolation across a possible regime change. Q06, Q11, and Q12 at 0.60 M are also weak because they fall directly inside the unresolved precipitation-onset interval, making their precipitation forecasts particularly uncertain.

Q08 and Q11 use 0.010 L, outside the autonomous endpoint-volume range, so their scale extrapolation is weak. Q09 and Q10 test addition-path effects that were not isolated in the observations; assigning them the same central endpoint as Q05 assumes equilibrium path independence. The replicated-concentration logic behind Q04/Q07/Q08 and Q06/Q11/Q12 is scientifically reasonable but stronger than the direct evidence because concentration sufficiency was not proven.

## 7. Limits on generalization

Generalization to new loading is limited by sparse sampling, especially across the concentration gap and near precipitation onset. Generalization across dilution or physical scale is limited because amount and volume were not independently resolved at identical final concentration. Generalization across paths is limited because staging can alter transient concentration, nucleation, and equilibration history even when the final nominal state is identical.

Generalization to other worlds is especially restricted: the acid, species mapping, electrolyte context, and precipitation mechanism are anonymous and benchmark-specific. The observed empirical relationships should not be transferred to a named acid, another solvent, another temperature, or real laboratory chemistry without new evidence.
