# repeat-03/EQ-P02-A-Opaque

Status: completed; source assays 12/12; public note versions 3.

Physical differences below describe the selected actions under matched worlds. They do not establish that an agent proposed or tested an explanation. All notebook versions, including terminal revisions, follow verbatim.

| Assay | End event | Prior note | First later note | Mean gap / assay SD: pH, free acid, precipitate |
| --- | --- | --- | --- | --- |
| 1 | 5 | 1 | 2 | 0.029, 0.814, 0.000 |
| 2 | 10 | 1 | 2 | 3.173, 4.591, 0.000 |
| 3 | 15 | 1 | 2 | 12.507, 4.143, 0.000 |
| 4 | 20 | 1 | 2 | 25.210, 2.292, 0.012 |
| 5 | 25 | 1 | 2 | 12.431, 0.234, 5.911 |
| 6 | 30 | 1 | 2 | 3.517, 0.019, 11.081 |
| 7 | 35 | 2 | 3 | 25.210, 2.292, 0.012 |
| 8 | 40 | 2 | 3 | 25.210, 2.292, 0.012 |
| 9 | 45 | 2 | 3 | 12.431, 0.234, 5.911 |
| 10 | 50 | 2 | 3 | 12.431, 0.234, 5.911 |
| 11 | 56 | 2 | 3 | 23.146, 2.565, 0.000 |
| 12 | 61 | 2 | 3 | 25.210, 2.292, 0.012 |

## Revision 1

Available operation events: 0.

# Hypothesis notebook

## H1 [tentative; pre-experiment]
For water-only batches at ambient conditions, increasing total acid loading at fixed liquid volume should lower pH and the free dissociation fraction; sufficiently high loading may increase the precipitation proxy. At fixed loading, dilution should reverse those trends. The preliminary R01/R02 pair is too close and noisy to establish a volume effect.

**Planned discriminating tests.** Use a crossed water-only design spanning loading and volume, including matched concentrations at different total scale to distinguish concentration control from independent amount/volume effects. Use intermediate pH-meter readings primarily to assess equilibration/repeatability; final assays are authoritative. A material deviation between matched-concentration batches would challenge a concentration-only relationship. Solvent/catalyst additions are outside the primary aqueous scope and will be avoided unless needed.

## Revision 2

Available operation events: 30.

# Hypothesis notebook

## H1 [supported in tested water-only loading series]
At 0.08 L water and ambient conditions, greater total loading strongly lowers pH and the free dissociation fraction. Final assays progress from approximately pH 5.22 and dissociation 0.73 at 6e-7 mol (event runner-operation-0005) to pH 1.54 and a floor-level dissociation estimate at 0.03 mol (runner-operation-0030). This monotonic effect is much larger than stated final-assay channel noise.

## H2 [tentative threshold/nonlinear precipitation response]
The precipitation proxy remains near its noise floor through 0.004 mol/0.08 L, rises to about 0.035 at 0.012 mol/0.08 L, and about 0.071 at 0.03 mol/0.08 L (events runner-operation-0020, -0025, -0030). This supports a nonlinear loading or concentration response, but amount and concentration are confounded in this series. Intermediate/final discrepancies at low signals caution against interpreting individual near-zero values.

## H3 [test planned before matched-concentration experiments]
If concentration is the principal state variable, batches at 0.05 M (0.001/0.02, 0.002/0.04, 0.004/0.08 L) and at 0.15 M (0.003/0.02, 0.006/0.04, 0.012/0.08 L) should agree within measurement/process scatter despite different total amounts. Consistent scale-dependent shifts would instead support independent amount or volume effects. A staged dilution of 0.003 mol from 0.02 to 0.08 L should move pH upward, dissociation upward, and precipitation downward if concentration control is causal.

## Revision 3

Available operation events: 61.

# Hypothesis notebook

## H1 [supported in tested water-only, ambient scope]
The dominant control variable is nominal total concentration, C = feed moles / liquid volume, rather than total moles or volume independently. At matched C = 0.05 M, final normalized pH values are 0.2189, 0.2207, 0.2190, and 0.2194 across scales/replicate (events runner-operation-0035, -0040, -0020, -0061). At matched C = 0.15 M they are 0.1600, 0.1624, and 0.1614 (events -0045, -0050, -0025). Dissociation and precipitation channels also cluster by concentration, although dissociation is near its lower measurement boundary at high C.

A within-batch intervention supports dilution rather than batch-scale confounding: diluting 0.003 mol from 0.02 L (0.15 M) to 0.08 L (0.0375 M) changed normalized pH from 0.1525 before dilution to 0.2253 afterward, increased dissociation from a floor-level reading to 0.0262, and decreased precipitation from 0.0354 to zero (events runner-operation-0053 and -0056). Instruments differ and measurements are not simultaneous replicates, so exact deltas include method noise; directions and magnitudes align with the cross-batch pattern.

## H2 [supported local effective weak-acid relationship; bounded scope]
For non/weakly precipitating observations through roughly C = 0.05 M, the public pH and dissociation fractions are consistent with an effective monoprotic relation K_eff = [H+] * alpha / (1 - precipitation - alpha), giving values mostly around 1.6e-5 to 2.0e-5 (effective pKa about 4.7-4.8) for events -0005, -0010, -0015, -0020, -0035, -0056, and -0061. One 0.05 M replicate gives about 1.1e-5 (-0040), illustrating finite assay/process scatter. This is an identifiable effective relationship, not proof of microscopic species or ideal activities. At C >= 0.15 M, alpha is close to zero/noise and this transformed estimate becomes unstable, so the relation is not claimed quantitatively there.

## H3 [supported empirical precipitation onset; mechanism unresolved]
The precipitation proxy is at/near its noise floor at C <= 0.05 M, clusters near 0.032-0.035 at C = 0.15 M, and is about 0.071 at C = 0.375 M (events -0020, -0035, -0040, -0061; -0025, -0045, -0050; -0030). A descriptive censored-linear approximation over 0.05-0.375 M is P approximately max(0, 0.223*C - 0.006), with C in mol/L, but the sparse range does not distinguish a true solubility threshold from a smooth saturating proxy, activity effects, or coupled dissociation/precipitation equilibria. More points around 0.03-0.12 M and independent solids evidence would discriminate these alternatives.

## Uncertainty and decisions
Final-assay nominal standard deviations are 0.002 in normalized pH and 0.006 in each fraction. Near-zero alpha/P values are therefore censored/noise-sensitive; qualitative ordering and replicated matched-concentration agreement are stronger than individual floor values. Intermediate pH-meter estimates have larger channel noise and are used as corroboration/intervention evidence, not pooled as equal-precision replicates. Scope is water-only, ambient, anonymous acid feed, C about 7.5e-6 to 0.375 M; solvent identity, temperature, ionic support, and microscopic solid identity remain untested.

**Anchor decision.** Batch 11 is the most useful evidentiary anchor because its staged fourfold dilution supplies a within-vessel directional test while ending at a condition consistent with independent concentration-matched batches. This is an evidentiary choice, not an optimization claim.

## Sealed K1

PUBLIC BACKGROUND
The system defines pH_normalized as pH/14, acid_dissociation_fraction as the free deprotonated-acid fraction relative to total acid feed, and precipitation_signal as the precipitated-acid fraction relative to total feed. The material is an anonymous weak-acid benchmark in water; no chemical identity or microscopic mechanism is public. Final-assay nominal standard deviations are 0.002 for normalized pH and 0.006 for each fraction. The pH-meter uncertainties are larger: 0.004, 0.015, and 0.020, respectively. The public preliminary assays at 6e-7 mol in 0.080 and 0.075 L gave normalized pH 0.3760 and 0.3766, dissociation 0.7371 and 0.7197, and precipitation 0.00425 and 0. No archival law was supplied.

ACTUAL OBSERVATIONS
Twelve completed water-only, ambient-condition batches were obtained. At fixed volume 0.080 L, increasing feed produced a strong monotonic response:
- Batch 1: 6e-7 mol, C = 7.5e-6 M; final normalized pH 0.37283 (pH 5.220), dissociation 0.7323, precipitation 0.
- Batch 2: 6e-5 mol, C = 0.00075 M; 0.28386 (pH 3.974), 0.1332, 0.00601.
- Batch 3: 0.0006 mol, C = 0.0075 M; 0.24921 (pH 3.489), 0.04869, 0.00418.
- Batch 4: 0.004 mol, C = 0.050 M; 0.21905 (pH 3.067), 0.02076, 0.00553.
- Batch 5: 0.012 mol, C = 0.150 M; 0.16135 (pH 2.259), dissociation reported at the zero boundary, precipitation 0.03485.
- Batch 6: 0.030 mol, C = 0.375 M; 0.11019 (pH 1.543), dissociation at the zero boundary, precipitation 0.07094.

Matched-concentration experiments separated concentration from total scale. At C = 0.050 M, Batches 4, 7, 8, and 12 used respectively 0.004/0.080, 0.001/0.020, 0.002/0.040, and 0.002/0.040 mol/L combinations. Their final normalized pH values were 0.21905, 0.21889, 0.22072, and 0.21939; dissociation fractions were 0.02076, 0.01827, 0.01302, and 0.02321; precipitation signals were 0.00553, 0, 0, and 0. At C = 0.150 M, Batches 5, 9, and 10 gave normalized pH 0.16135, 0.15995, and 0.16237; dissociation 0, 0.00541, and 0.01363; precipitation 0.03485, 0.03200, and 0.03545.

Batch 11 supplied a within-vessel dilution test. Before dilution, 0.003 mol in 0.020 L (0.150 M) gave a pH-meter normalized pH of 0.15248, dissociation at zero, and precipitation 0.03545. After adding 0.060 L water, making C = 0.0375 M, the final assay gave normalized pH 0.22526, dissociation 0.02624, and precipitation 0. The two readings used different instruments, but the changes are much larger than their stated channel noise and agree directionally with the independent batches.

INFERENCE
Nominal concentration C = total feed/liquid volume is the principal identifiable control variable over the tested scales. Increasing loading at fixed volume lowers pH and the free dissociation fraction; dilution raises both. Matched concentrations gave nearly identical pH despite fourfold differences in total amount and volume, so strong independent amount or vessel-volume effects are not supported. Small scale effects remain below the resolution of this design.

Below approximately 0.05 M, the observations are consistent with an effective monoprotic weak-acid relationship. If the unprecipitated protonated fraction is approximated by 1-alpha-P, then
K_eff = [H+] alpha/(1-alpha-P), with [H+] = 10^(-pH).
For the usable low-to-moderate-concentration final assays, K_eff is mostly about 1.6e-5 to 2.0e-5, with one 0.05 M replicate near 1.1e-5. Thus a compact local description is K_eff approximately 1.7e-5, or effective pKa approximately 4.77. This relationship explains both declining pH and declining fractional dissociation as concentration increases. It is an effective relationship, not proof of ideal activities or a particular molecular acid.

Precipitation is indistinguishable from the assay noise floor at or below 0.05 M, clusters around 0.032-0.035 at 0.15 M, and reaches about 0.071 at 0.375 M. A purely descriptive fit over 0.05-0.375 M is P approximately max(0, 0.223C - 0.006), with C in mol/L. This fit is only an interpolation summary: its apparent onset near 0.03 M is not established as a physical solubility threshold, especially because values around 0.05 M are censored near zero.

UNCERTAINTY AND LIMITS
Normalized-pH uncertainty of 0.002 corresponds to about 0.028 pH unit for final assays. Dissociation and precipitation values at or below roughly 0.006 should not be interpreted as resolved positive quantities, and reported zeros are boundary-clipped/noise-sensitive rather than proof of exact absence. At 0.15-0.375 M, dissociation is sufficiently close to zero that transformed K_eff estimates become unstable; the quantitative weak-acid law is therefore supported only through roughly 0.05 M. Replication was concentrated at 0.05 and 0.15 M, so uncertainty includes unmeasured batch variability in addition to declared instrument noise. Final equilibrium residuals were small, but equilibrium_confidence is an environment diagnostic and is not treated as scientific confidence.

COMPETING EXPLANATIONS AND CONJECTURE
The matched-scale and staged-dilution evidence favors concentration control over independent total-amount or volume control. It does not distinguish ideal mass-action behavior from a nonideal activity-based equilibrium that happens to have a nearly constant effective Ka in this range. The rising precipitation proxy could represent a genuine solubility boundary, a smooth saturation response, activity-coefficient changes, or coupled dissociation/precipitation equilibria. The low high-concentration dissociation readings may reflect genuine suppression, removal into precipitate, or lower-bound measurement censoring. No independent solid identification was available, so the precipitated species and stoichiometry are conjectural.

SCOPE
The supported domain is water-only, near ambient conditions, anonymous acid feed, nominal concentration approximately 7.5e-6 to 0.375 M, and liquid volumes 0.020-0.080 L. Temperature, solvent identity, ionic support, catalysts, kinetics, hysteresis, and solid-phase identity were not tested. Results should not be generalized to arbitrary aqueous chemistry. Additional measurements densely spanning about 0.03-0.12 M, with replicate final assays and independent solids evidence, would best distinguish a sharp precipitation threshold from a smooth or activity-driven response.

## Sealed Q

{
  "predictions": [
    {
      "query_id": "Q01",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.269,
          "lower80": 0.263,
          "upper80": 0.275
        },
        "acid_dissociation_fraction": {
          "estimate": 0.088,
          "lower80": 0.075,
          "upper80": 0.102
        },
        "precipitation_signal": {
          "estimate": 0.003,
          "lower80": 0,
          "upper80": 0.012
        }
      },
      "rationale": "At 0.002 M, interpolation between observed low-concentration batches and the effective weak-acid relation predicts moderately acidic pH and about 9% free dissociation. Precipitation should remain at the assay noise floor."
    },
    {
      "query_id": "Q02",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.253,
          "lower80": 0.247,
          "upper80": 0.258
        },
        "acid_dissociation_fraction": {
          "estimate": 0.052,
          "lower80": 0.041,
          "upper80": 0.064
        },
        "precipitation_signal": {
          "estimate": 0.003,
          "lower80": 0,
          "upper80": 0.012
        }
      },
      "rationale": "The 0.006 M concentration lies close to the observed 0.0075 M condition. The effective weak-acid model gives about 5% dissociation, while precipitation remains unresolved from zero."
    },
    {
      "query_id": "Q03",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.235,
          "lower80": 0.228,
          "upper80": 0.241
        },
        "acid_dissociation_fraction": {
          "estimate": 0.029,
          "lower80": 0.019,
          "upper80": 0.039
        },
        "precipitation_signal": {
          "estimate": 0.003,
          "lower80": 0,
          "upper80": 0.013
        }
      },
      "rationale": "At 0.020 M, log-concentration interpolation predicts normalized pH near 0.235 and dissociation near 0.029. This remains below the empirically apparent precipitation region, although small positive assay readings are possible."
    },
    {
      "query_id": "Q04",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.21,
          "lower80": 0.201,
          "upper80": 0.218
        },
        "acid_dissociation_fraction": {
          "estimate": 0.017,
          "lower80": 0.006,
          "upper80": 0.027
        },
        "precipitation_signal": {
          "estimate": 0.006,
          "lower80": 0,
          "upper80": 0.02
        }
      },
      "rationale": "At 0.060 M, the batch is just above the replicated 0.050 M conditions and below the 0.150 M precipitation-positive conditions. The interval allows uncertainty in the onset and shape of precipitation."
    },
    {
      "query_id": "Q05",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.145,
          "lower80": 0.132,
          "upper80": 0.158
        },
        "acid_dissociation_fraction": {
          "estimate": 0.008,
          "lower80": 0,
          "upper80": 0.02
        },
        "precipitation_signal": {
          "estimate": 0.043,
          "lower80": 0.026,
          "upper80": 0.061
        }
      },
      "rationale": "The 0.200 M concentration interpolates between observed 0.150 and 0.375 M batches. It should have low, noise-sensitive free dissociation and clearly positive precipitation; uncertainty includes the unresolved curvature of the precipitation response."
    },
    {
      "query_id": "Q06",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.084,
          "lower80": 0.06,
          "upper80": 0.108
        },
        "acid_dissociation_fraction": {
          "estimate": 0.004,
          "lower80": 0,
          "upper80": 0.016
        },
        "precipitation_signal": {
          "estimate": 0.1,
          "lower80": 0.06,
          "upper80": 0.145
        }
      },
      "rationale": "The 0.600 M concentration extrapolates beyond the observed maximum of 0.375 M. Continued acidification and increased precipitation are expected, but intervals are wide because saturation, nonideal activity, and precipitation curvature were not identified."
    },
    {
      "query_id": "Q07",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.21,
          "lower80": 0.202,
          "upper80": 0.217
        },
        "acid_dissociation_fraction": {
          "estimate": 0.017,
          "lower80": 0.006,
          "upper80": 0.027
        },
        "precipitation_signal": {
          "estimate": 0.006,
          "lower80": 0,
          "upper80": 0.019
        }
      },
      "rationale": "This 0.060 M scale control is predicted to match Q04 because matched-concentration observations supported concentration rather than total amount or volume as the dominant control. Its 0.040 L volume is within the studied range."
    },
    {
      "query_id": "Q08",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.21,
          "lower80": 0.198,
          "upper80": 0.221
        },
        "acid_dissociation_fraction": {
          "estimate": 0.017,
          "lower80": 0.004,
          "upper80": 0.03
        },
        "precipitation_signal": {
          "estimate": 0.006,
          "lower80": 0,
          "upper80": 0.023
        }
      },
      "rationale": "Concentration control predicts the same center as the other 0.060 M batches. The interval is wider because 0.010 L is below the experimentally studied 0.020–0.080 L volume range, so a small independent scale effect cannot be excluded."
    },
    {
      "query_id": "Q09",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.145,
          "lower80": 0.128,
          "upper80": 0.162
        },
        "acid_dissociation_fraction": {
          "estimate": 0.008,
          "lower80": 0,
          "upper80": 0.022
        },
        "precipitation_signal": {
          "estimate": 0.043,
          "lower80": 0.02,
          "upper80": 0.068
        }
      },
      "rationale": "The final state is 0.200 M, so the concentration model predicts the same equilibrium center as Q05. Batch 11 supported substantial equilibration after staged dilution, but this exact staged loading path was not tested; the wider interval allows possible path dependence or precipitation hysteresis."
    },
    {
      "query_id": "Q10",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.145,
          "lower80": 0.131,
          "upper80": 0.159
        },
        "acid_dissociation_fraction": {
          "estimate": 0.008,
          "lower80": 0,
          "upper80": 0.021
        },
        "precipitation_signal": {
          "estimate": 0.043,
          "lower80": 0.024,
          "upper80": 0.064
        }
      },
      "rationale": "Adding all solvent before the staged reagent additions reaches the same 0.200 M final composition as Q05 and Q09. No path effect was established, so the center is unchanged, with modest allowance for untested precipitation history."
    },
    {
      "query_id": "Q11",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.084,
          "lower80": 0.05,
          "upper80": 0.118
        },
        "acid_dissociation_fraction": {
          "estimate": 0.004,
          "lower80": 0,
          "upper80": 0.018
        },
        "precipitation_signal": {
          "estimate": 0.1,
          "lower80": 0.045,
          "upper80": 0.16
        }
      },
      "rationale": "The center follows the 0.600 M extrapolation. This case combines concentration above the observed range with a 0.010 L volume below the studied range, so its interval is the widest among the scale controls."
    },
    {
      "query_id": "Q12",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.084,
          "lower80": 0.061,
          "upper80": 0.108
        },
        "acid_dissociation_fraction": {
          "estimate": 0.004,
          "lower80": 0,
          "upper80": 0.016
        },
        "precipitation_signal": {
          "estimate": 0.1,
          "lower80": 0.06,
          "upper80": 0.145
        }
      },
      "rationale": "At 0.600 M and 0.040 L, concentration dominance predicts the same center as Q06 and Q11. The volume is within the studied range, but substantial uncertainty remains because the concentration requires extrapolation beyond 0.375 M."
    }
  ],
  "rationale": "Predictions use the sealed concentration-dominant account: log-concentration interpolation for normalized pH, the effective weak-acid relationship with K_eff near 1.7e-5 where supported, and an empirical precipitation onset above roughly 0.05 M. Intervals include declared final-assay noise, replicate scatter, uncertainty in precipitation onset, lower-bound clipping of fractional signals, extrapolation beyond 0.375 M, and extra scale or path uncertainty where applicable."
}

## Sealed K2

1. SUPPORTED, CONTRADICTED, AND UNTESTED RELATIONSHIPS

Supported within this bounded water-only world:
- Nominal concentration, C = feed moles/liquid volume, is the dominant observed control variable. At fixed 0.080 L, increasing loading lowered pH and the free dissociation fraction. Matched 0.050 M and 0.150 M batches produced similar outcomes across different amounts and volumes.
- Dilution raises pH and dissociation and lowers precipitation. Batch 11 provided the strongest directional evidence: dilution from 0.150 to 0.0375 M changed normalized pH from 0.1525 to 0.2253, dissociation from a boundary-zero reading to 0.0262, and precipitation from 0.0354 to zero.
- Through roughly 0.05 M, pH and dissociation are consistent with an effective weak-acid relationship having K_eff around 1.7e-5, or effective pKa around 4.7–4.8.
- The precipitation proxy was at or near its measurement floor through 0.05 M, about 0.032–0.035 at 0.15 M, and about 0.071 at 0.375 M.

Contradicted or disfavored:
- A strong independent dependence on total moles or volume is disfavored by the matched-concentration batches. Small scale effects remain possible.
- A single ideal weak-acid equation without precipitation, activity, or censoring qualifications is not adequate across the entire range. At 0.15 M and above, dissociation estimates approach the measurement boundary and the pH behavior cannot be interpreted reliably with the low-concentration model alone.
- A claim of exactly zero precipitation at low concentration is not supported; the assay uncertainty is comparable to the observed near-zero values.

Untested:
- Temperature, pressure, waiting time, equilibration kinetics, alternative solvents, electrolyte/support composition, catalysts, and named chemical identity.
- Reversibility, hysteresis, and most order-of-addition effects.
- Solid composition, stoichiometry, particle formation, and whether the public precipitation signal corresponds to a sharp phase boundary.

2. OBSERVATIONS THAT CHANGED THE ACCOUNT

There were actual experimental observations, and several changed the account. The preliminary R01/R02 pair was too narrowly spaced to establish a volume effect. Batches 1–6 established the large monotonic loading response at fixed volume. Batches 4, 7, 8, and 12 at 0.050 M, and Batches 5, 9, and 10 at 0.150 M, changed the interpretation from a generic loading/volume hypothesis to a concentration-dominant account. Batch 11 then supplied within-vessel dilution evidence in the predicted direction. The positive precipitation results at 0.150 and 0.375 M narrowed the initial hypothesis from merely “possible precipitation at high loading” to a supported concentration-associated rise, while leaving its mathematical form unresolved.

3. COMPETING EXPLANATIONS

Still distinguishable in principle but unresolved by the available data:
- Ideal monoprotic mass action versus a nonideal activity-based equilibrium with a similar local effective Ka.
- A sharp solubility threshold versus a smooth, saturating precipitation response.
- Precipitation-driven removal of one acid form versus a separate concentration-dependent change in dissociation or activity.
- Genuine near-zero dissociation at high concentration versus a small positive fraction obscured by noise and lower-bound clipping.
- Complete final-state control versus modest path dependence or precipitation hysteresis. Batch 11 supports response to dilution but does not test reverse concentration, repeated cycles, or all orderings.
- Exact concentration-only behavior versus small independent effects of volume, interfacial area, or total material that were below this design’s resolution.

4. NEXT SINGLE LEGAL EXPERIMENT

I would prepare one water-only batch at 0.100 M using 0.040 L water and 0.004 mol reagent, terminate it, and obtain a final assay. This lies inside the tested volume range but fills the largest decision-relevant gap between 0.050 and 0.150 M.

Possible results would differ substantively:
- Precipitation near zero, with pH and dissociation close to a continuation of the low-concentration weak-acid trend, would support a relatively sharp onset above 0.10 M.
- An intermediate precipitation signal around 0.015–0.025 would support a smooth concentration response.
- A signal already near the 0.15 M level of approximately 0.033 would support an onset below 0.10 M followed by early saturation or a steep transition.
- A large departure in pH or dissociation without corresponding precipitation would favor nonideal acid-base activity effects rather than precipitation alone.
A single point would narrow the onset but would not identify solid composition or prove a microscopic mechanism.

5. EVIDENCE LIMITS

The account rests on twelve batches, all in water and near ambient conditions. Replication was concentrated at 0.050 and 0.150 M; 0.375 M had only one final assay. Concentrations between 0.05 and 0.15 M were not directly sampled. The only staged dilution used a noisier pH-meter before dilution and a final assay afterward, so its large directional result is persuasive but not a same-instrument paired estimate. Near-zero fractional signals are censored and noise-sensitive. There was no independent solids measurement, activity measurement, species identification, kinetic series, or direct equilibrium-constant determination. The environment’s equilibrium_confidence is only a diagnostic and does not quantify confidence in these scientific conclusions.

6. LEAST RELIABLE Q FORECASTS

Q06, Q11, and Q12 are least reliable because 0.600 M exceeds the observed maximum of 0.375 M. Their precipitation forecasts require extrapolating an unidentified response shape, while their dissociation forecasts lie near the measurement boundary. Q11 is additionally outside the studied volume range at 0.010 L.

Q08 is also outside the studied volume range at 0.010 L, although its 0.060 M concentration is close to observed conditions. Q09 and Q10 rely on unverified path independence; Q09’s alternating staged additions are particularly weakly supported. Q04, Q07, and Q08 lie near the poorly resolved precipitation onset, so their precipitation intervals are more model-dependent than their pH forecasts. Q01–Q03 are interpolation forecasts within the low-concentration relationship and are comparatively more reliable. Q05 is concentration interpolation, but its dissociation estimate remains boundary-sensitive.

7. GENERALIZATION LIMITS

Generalization to new loadings is limited by sparse sampling and by the transition from a low-concentration weak-acid regime to a precipitation-associated regime. Generalization to dilution paths is limited by one staged experiment and no reverse-concentration or cycling tests. Generalization to new addition paths assumes that final equilibrium erases history, which was not established. Volumes below 0.020 L and concentrations above 0.375 M are outside the observed domain. Different solvents, temperatures, support electrolytes, or anonymous material categories could alter effective activities, dissociation, and precipitation. Most importantly, this is a bounded synthetic world with anonymous chemistry: its fitted effective Ka and precipitation response are world-specific and should not be transferred to a named acid, a real laboratory system, or another benchmark world without new evidence.
