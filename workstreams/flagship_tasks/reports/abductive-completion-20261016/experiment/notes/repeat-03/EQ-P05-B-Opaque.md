# repeat-03/EQ-P05-B-Opaque

Status: completed; source assays 12/12; public note versions 2.

Physical differences below describe the selected actions under matched worlds. They do not establish that an agent proposed or tested an explanation. All notebook versions, including terminal revisions, follow verbatim.

| Assay | End event | Prior note | First later note | Mean gap / assay SD: pH, free acid, precipitate |
| --- | --- | --- | --- | --- |
| 1 | 5 | 1 | 2 | 0.098, 0.720, 0.000 |
| 2 | 10 | 1 | 2 | 0.044, 0.505, 0.000 |
| 3 | 15 | 1 | 2 | 6.194, 2.972, 0.000 |
| 4 | 20 | 1 | 2 | 3.839, 2.830, 0.000 |
| 5 | 25 | 1 | 2 | 22.982, 1.675, 0.000 |
| 6 | 30 | 1 | 2 | 18.082, 2.116, 0.000 |
| 7 | 35 | 1 | 2 | 24.249, 0.381, 1.449 |
| 8 | 40 | 1 | 2 | 29.774, 1.167, 0.000 |
| 9 | 45 | 1 | 2 | 6.411, 0.013, 6.015 |
| 10 | 50 | 1 | 2 | 14.921, 0.082, 3.372 |
| 11 | 55 | 1 | 2 | 0.000, 0.000, 8.413 |
| 12 | 60 | 1 | 2 | 6.411, 0.013, 6.015 |

## Revision 1

Available operation events: 0.

# Source-stage hypothesis notebook

## H1 [tentative; pre-experiment]
In water near ambient conditions, raising total acid concentration (higher reagent loading or smaller liquid volume) should lower pH and the free deprotonated fraction. The two preliminary trace-loading assays R01/R02 are compatible with roughly half dissociation and negligible precipitation, but their small volume difference is not enough to establish a dilution effect.

## H2 [tentative; pre-experiment]
The precipitation proxy should remain near zero at trace loading and increase only after a concentration/loading threshold. A paired 0.04/0.08 L water grid at matched reagent amounts can distinguish a concentration-controlled response from a response dominated by absolute moles, although either may remain observationally equivalent over a limited range.

## Decision rule
Use broad log-spaced loadings plus high-load points. Treat differences cautiously relative to declared assay noise; repeated same-state pH-meter/final-assay readings provide method agreement rather than independent batch replication. Revise if dilution has weak/nonmonotone effects or precipitation tracks absolute loading more closely than concentration.

## Revision 2

Available operation events: 60.

# Source-stage hypothesis notebook

## H1 [supported in tested aqueous scope]
The dominant coordinate is nominal total loading concentration, (C_T=n/V), over (7.5\times10^{-6}) to 1 mol/L in water near 298 K. Final-assay pH falls monotonically with concentration. A descriptive all-point fit is
[
pH_{normalized}\approx 0.1004-0.05862\log_{10}(C_T/\mathrm{mol\,L^{-1}}),
]
or (pH\approx1.406-0.821\log_{10}C_T). This is an empirical summary, not a claimed equilibrium law; curvature/local deviations and lack of batch replication limit precision.

Evidence: paired-volume batches 1–12 (final assays at runner-operation-0005, -0010, -0015, -0020, -0025, -0030, -0035, -0040, -0045, -0050, -0055, -0060). The strongest identifiability check is equal concentration at 0.5 mol/L but different absolute amount and volume: batches 9 and 12 give pH_normalized 0.11067 and 0.11197, indistinguishable at the declared 0.002 assay SD. Thus absolute moles alone are disfavored in this scope, although concentration-dependent activity effects remain equivalent to a simple concentration law.

## H2 [supported qualitatively; high-loading magnitude unresolved]
The free deprotonated fraction decreases sharply with concentration: 0.520 at (7.5\times10^{-6}) M (batch 2), 0.038 at (1.5\times10^{-3}) M (batch 3), and near the lower bound by 0.025 M and above. The trace pair (batches 1/2) also shows a clear dilution response (0.402 vs 0.520). Preliminary R01/R02 agree with the dilute endpoint. At high loading, clipping/noise prevents distinguishing zero from a small positive fraction; a classical single ideal weak-acid model, activity/common-ion modification, and the benchmark's effective response remain alternative explanations.

## H3 [rejected as an observed threshold; bounded scope]
No reproducible precipitation onset was found up to 1 mol/L and 0.04 mol feed. All final signals were 0–0.014, comparable to assay noise; isolated pH-meter excursions (for example runner-operation-0033) were not reproduced by the corresponding final assay (runner-operation-0035). Therefore the evidence supports only an upper/no-detected-effect statement, not absence of precipitation generally. A different component, solvent, temperature, equilibration protocol, or loading beyond this bounded grid could change the conclusion.

## Measurement and uncertainty decisions
Same-state pH-meter readings broadly track final-assay trends but are noisier and are method comparisons, not independent batch replicates. Numerical differences smaller than declared channel noise are not treated as effects. No time/temperature dependence was tested. The water-only, near-ambient results should not be generalized to the named nonaqueous solvents or anonymous additives.

## Sealed K1

Scientific account of the bounded aqueous-equilibrium world

PUBLIC BACKGROUND AND DEFINITIONS
The task defines pH_normalized as pH/14, acid_dissociation_fraction as the free deprotonated-acid fraction relative to total acid feed, and precipitation_signal as the precipitated-acid fraction relative to total acid feed. The system is explicitly a bounded weak-acid/precipitation benchmark, not a model of general aqueous chemistry. Final-assay standard deviations were declared as 0.002 for pH_normalized and 0.006 for both acid dissociation and precipitation. The public preliminary assays used 6×10^-7 mol in 0.080 and 0.075 L water. They reported pH_normalized 0.38657 and 0.38394, dissociation fractions 0.51442 and 0.50256, and precipitation signals 0.00276 and 0.00247.

EXPERIMENTAL SCOPE
I completed 12 water-only batches near 298 K. Each reagent amount was tested at 0.040 and 0.080 L: 6×10^-7, 6×10^-5, 0.001, 0.005, 0.020, and 0.040 mol. Nominal total concentration C_T=n/V therefore spanned 7.5×10^-6 to 1 mol/L. Every batch received an intermediate pH-meter measurement and a final assay. No additive, nonaqueous solvent, temperature, time, or mixing study was performed.

ACTUAL FINAL-ASSAY OBSERVATIONS
Ordered by concentration, the observations were:
• Batch 2, 7.5×10^-6 M: pH_normalized 0.38804, dissociation 0.51954, precipitation 0.01397.
• Batch 1, 1.5×10^-5 M: 0.37064, 0.40195, 0.
• Batch 4, 7.5×10^-4 M: 0.29755, 0.04910, 0.
• Batch 3, 1.5×10^-3 M: 0.28078, 0.03834, 0.00375.
• Batch 6, 0.0125 M: 0.22278, 0, 0.01105.
• Batch 5, 0.025 M: 0.20662, 0.00393, 0.00429.
• Batch 8, 0.0625 M: 0.17632, 0.00423, 0.00039.
• Batch 7, 0.125 M: 0.15295, 0, 0.
• Batch 10, 0.25 M: 0.13377, 0, 0.
• Batch 9, 0.5 M: 0.11067, 0, 0.
• Batch 12, also 0.5 M but with twice the moles and volume of batch 9: 0.11197, 0.00184, 0.
• Batch 11, 1 M: 0.08466, 0, 0.
Here, reported zeros are bounded instrument outputs and should not be interpreted as proof of exact physical zero.

SUPPORTED RELATIONSHIPS
1. pH is primarily concentration-controlled in this range. pH_normalized decreased monotonically as C_T increased. Doubling volume at fixed moles raised pH_normalized in every pair, generally by about 0.016–0.027. An all-point descriptive least-squares fit was
pH_normalized ≈ 0.1004 − 0.05862 log10(C_T/[mol L^-1]),
equivalently pH ≈ 1.406 − 0.821 log10(C_T/[mol L^-1]). This summarizes the measured interval only; it is not asserted as an exact equilibrium law or an extrapolation.

2. Concentration explains the observations better than absolute loading alone. Batches 9 and 12 both had C_T=0.5 M, while batch 12 doubled both amount and volume. Their pH_normalized values, 0.11067 and 0.11197, differed by only 0.00131, below the declared 0.002 single-assay standard deviation. Both had no detected final precipitation, and their dissociation estimates were at the lower bound or noise scale. This comparison disfavors an absolute-moles-only explanation within the tested geometry.

3. Dissociation decreases strongly with concentration. It was about one-half at approximately 8×10^-6 M, about 0.04–0.05 at 7.5×10^-4 to 1.5×10^-3 M, and indistinguishable from a very small value at most concentrations of 0.0125 M or higher. The clearest paired dilution response was batches 1 and 2: doubling volume changed dissociation from 0.40195 to 0.51954, far larger than the declared assay noise. At high loading, channel noise and the zero lower bound prevent resolving the dilution effect quantitatively.

4. A simple ideal monoprotic weak-acid relation is locally plausible only at the dilute end. Using K_a≈C_T α^2/(1−α), batches 1 and 2 imply an apparent K_a of roughly 4×10^-6; the two preliminary reference assays give a similar dilute estimate. At 7.5×10^-4 to 1.5×10^-3 M, the corresponding apparent value is nearer 2×10^-6, and it becomes poorly identifiable once α approaches the measurement floor. Thus a constant ideal K_a is a useful local dilute approximation but is not supported globally across five orders of magnitude.

5. No systematic precipitation transition was observed. All final precipitation signals lay between 0 and 0.01397, approximately at the scale of a few declared standard deviations, with no monotone increase with concentration. In particular, final signals were zero at 0.125, 0.25, both 0.5 M conditions, and 1 M. An isolated intermediate pH-meter precipitation estimate of 0.0312 in batch 7 was followed by a zero final-assay estimate and therefore was not treated as a reproduced event. The supported statement is 'no concentration-dependent precipitation detected under this protocol,' not 'precipitation is impossible.'

INFERENCE VERSUS CONJECTURE
The empirical concentration–pH curve, the decline in dissociation, and the absence of a resolved precipitation trend are direct inferences from the observations. The dilute apparent K_a is derived from an ideal weak-acid equation and is therefore model-dependent. Possible explanations for its loss of constancy include concentration-dependent activities, background ionic or acid-base contributions, a concentration-dependent effective equilibrium, or the benchmark definitions separating free deprotonated acid from other contributors to hydrogen-ion activity. These explanations are observationally equivalent in this dataset. A precipitation-coupled explanation is not supported because the precipitation proxy remained at its noise floor.

UNCERTAINTY AND LIMITATIONS
The final pH trend is much larger than the stated measurement noise and is well supported. The same-concentration comparison provides limited evidence for concentration rather than total moles, but there was no full independent replication of every condition. Intermediate pH-meter readings broadly followed the final trends but have larger declared noise and are method comparisons, not independent batch replicates. Dissociation values near zero are censored by the bounded channel, so only an upper/no-resolved-signal interpretation is justified there. No formal precipitation detection limit or replicated confidence interval was established. The environment's equilibrium_confidence channel is a diagnostic, not my epistemic confidence. Results apply only to water, approximately 298 K, 0.040–0.080 L, 6×10^-7–0.040 mol feed, and 7.5×10^-6–1 mol/L nominal loading under the instantaneous benchmark protocol. Behavior in other solvents, with additives, at other temperatures or times, or outside this concentration range remains conjectural.

## Sealed Q

{
  "predictions": [
    {
      "query_id": "Q01",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.273,
          "lower80": 0.252,
          "upper80": 0.294
        },
        "acid_dissociation_fraction": {
          "estimate": 0.03,
          "lower80": 0.014,
          "upper80": 0.047
        },
        "precipitation_signal": {
          "estimate": 0.003,
          "lower80": 0,
          "upper80": 0.014
        }
      },
      "rationale": "At 0.002 M this interpolates just above batches 3 and 4 in concentration. Their pH and dissociation trends imply pH_normalized near 0.27 and dissociation near 0.03. Precipitation remained at the noise floor. The interval is widened because 0.020 L is below the experimentally studied volumes."
    },
    {
      "query_id": "Q02",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.243,
          "lower80": 0.222,
          "upper80": 0.264
        },
        "acid_dissociation_fraction": {
          "estimate": 0.016,
          "lower80": 0.004,
          "upper80": 0.029
        },
        "precipitation_signal": {
          "estimate": 0.003,
          "lower80": 0,
          "upper80": 0.014
        }
      },
      "rationale": "The 0.006 M concentration lies between the 0.0015 and 0.0125 M observations. Log-concentration interpolation predicts lower pH and dissociation than Q01, while precipitation remains unresolved. Model uncertainty is appreciable because dissociation approaches its measurement floor."
    },
    {
      "query_id": "Q03",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.212,
          "lower80": 0.192,
          "upper80": 0.232
        },
        "acid_dissociation_fraction": {
          "estimate": 0.007,
          "lower80": 0,
          "upper80": 0.017
        },
        "precipitation_signal": {
          "estimate": 0.003,
          "lower80": 0,
          "upper80": 0.014
        }
      },
      "rationale": "At 0.020 M, interpolation between the 0.0125 and 0.025 M batches gives pH_normalized near 0.21. Dissociation should be small and may be reported as zero after observation noise and lower-bound clipping. No concentration-dependent precipitation was observed."
    },
    {
      "query_id": "Q04",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.178,
          "lower80": 0.158,
          "upper80": 0.198
        },
        "acid_dissociation_fraction": {
          "estimate": 0.004,
          "lower80": 0,
          "upper80": 0.013
        },
        "precipitation_signal": {
          "estimate": 0.003,
          "lower80": 0,
          "upper80": 0.014
        }
      },
      "rationale": "The concentration nearly matches the observed 0.0625 M condition, so its pH estimate is anchored near that result. Dissociation and precipitation are expected at the channel noise floor. The smaller 0.020 L scale adds uncertainty beyond final-assay noise."
    },
    {
      "query_id": "Q05",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.14,
          "lower80": 0.118,
          "upper80": 0.162
        },
        "acid_dissociation_fraction": {
          "estimate": 0.002,
          "lower80": 0,
          "upper80": 0.012
        },
        "precipitation_signal": {
          "estimate": 0.003,
          "lower80": 0,
          "upper80": 0.015
        }
      },
      "rationale": "Log-concentration interpolation between 0.125 and 0.25 M supports pH_normalized near 0.14. Dissociation was already indistinguishable from a very small value in this region. Precipitation showed no reproducible rise, but the untested 0.020 L scale warrants a broader interval."
    },
    {
      "query_id": "Q06",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.104,
          "lower80": 0.083,
          "upper80": 0.125
        },
        "acid_dissociation_fraction": {
          "estimate": 0.001,
          "lower80": 0,
          "upper80": 0.01
        },
        "precipitation_signal": {
          "estimate": 0.003,
          "lower80": 0,
          "upper80": 0.015
        }
      },
      "rationale": "The 0.6 M state lies between the replicated 0.5 M response and the 1 M observation, giving pH_normalized near 0.10. Dissociation should be below reliable resolution, and precipitation should remain near zero. Volume extrapolation broadens the interval."
    },
    {
      "query_id": "Q07",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.178,
          "lower80": 0.164,
          "upper80": 0.192
        },
        "acid_dissociation_fraction": {
          "estimate": 0.004,
          "lower80": 0,
          "upper80": 0.012
        },
        "precipitation_signal": {
          "estimate": 0.003,
          "lower80": 0,
          "upper80": 0.012
        }
      },
      "rationale": "This 0.060 M batch uses a studied 0.040 L scale and closely matches the observed 0.0625 M condition. Concentration control therefore gives a relatively narrow pH interval. Dissociation and precipitation remain close to their lower bounds."
    },
    {
      "query_id": "Q08",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.178,
          "lower80": 0.153,
          "upper80": 0.203
        },
        "acid_dissociation_fraction": {
          "estimate": 0.004,
          "lower80": 0,
          "upper80": 0.015
        },
        "precipitation_signal": {
          "estimate": 0.003,
          "lower80": 0,
          "upper80": 0.016
        }
      },
      "rationale": "The point estimate matches Q04 and Q07 because all have the same final concentration. However, 0.010 L is fourfold below the smallest studied volume, so possible scale or geometry effects require wider intervals despite evidence favoring concentration over absolute moles."
    },
    {
      "query_id": "Q09",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.14,
          "lower80": 0.116,
          "upper80": 0.164
        },
        "acid_dissociation_fraction": {
          "estimate": 0.002,
          "lower80": 0,
          "upper80": 0.014
        },
        "precipitation_signal": {
          "estimate": 0.003,
          "lower80": 0,
          "upper80": 0.016
        }
      },
      "rationale": "Its final totals equal Q05, so an equilibrium state-function interpretation predicts the same central outcomes. The staged alternating additions were not tested in the campaign; intervals include possible path dependence or incomplete relaxation. No observed evidence supports a precipitation pulse persisting to the final assay."
    },
    {
      "query_id": "Q10",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.14,
          "lower80": 0.116,
          "upper80": 0.164
        },
        "acid_dissociation_fraction": {
          "estimate": 0.002,
          "lower80": 0,
          "upper80": 0.014
        },
        "precipitation_signal": {
          "estimate": 0.003,
          "lower80": 0,
          "upper80": 0.016
        }
      },
      "rationale": "The final concentration and totals match Q05 and Q09, so the concentration model gives identical central estimates. Solvent-first versus staged ordering is observationally untested; the prediction interval is widened rather than assuming exact path independence."
    },
    {
      "query_id": "Q11",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.104,
          "lower80": 0.079,
          "upper80": 0.129
        },
        "acid_dissociation_fraction": {
          "estimate": 0.001,
          "lower80": 0,
          "upper80": 0.012
        },
        "precipitation_signal": {
          "estimate": 0.003,
          "lower80": 0,
          "upper80": 0.016
        }
      },
      "rationale": "At 0.6 M the point estimate interpolates between the observed 0.5 and 1 M states. The unusually small 0.010 L volume is outside the studied range, so this scale-control prediction has the widest pH interval among the 0.6 M cases."
    },
    {
      "query_id": "Q12",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.104,
          "lower80": 0.089,
          "upper80": 0.119
        },
        "acid_dissociation_fraction": {
          "estimate": 0.001,
          "lower80": 0,
          "upper80": 0.01
        },
        "precipitation_signal": {
          "estimate": 0.003,
          "lower80": 0,
          "upper80": 0.012
        }
      },
      "rationale": "This 0.6 M batch uses the experimentally studied 0.040 L volume and lies between observed 0.5 and 1 M concentrations. It therefore receives narrower intervals than Q06 or Q11. Dissociation and precipitation are expected to be indistinguishable from small positive or clipped-zero signals."
    }
  ],
  "rationale": "Central pH predictions use local interpolation along the sealed concentration-response curve rather than extrapolating the global logarithmic fit. Dissociation estimates follow its steep decline with concentration and explicitly allow lower-bound clipping. Precipitation estimates remain near the observed noise floor because no systematic onset was detected through 1 M. The 80% intervals combine declared final-assay noise, empirical model scatter, sparse replication, and extra uncertainty for volumes below 0.040 L or untested addition paths."
}

## Sealed K2

1. Supported, contradicted, and untested relationships

Supported within the studied water-only domain:
- pH_normalized decreases monotonically as nominal concentration n/V increases from 7.5×10^-6 to 1 mol/L.
- At fixed reagent amount, dilution from 0.040 to 0.080 L raises pH_normalized.
- Acid_dissociation_fraction falls sharply with concentration: approximately 0.4–0.52 at trace concentration, approximately 0.04–0.05 near 10^-3 M, and generally indistinguishable from a small value at higher concentrations.
- Concentration is a better predictor than absolute moles alone. Batches 9 and 12 both had 0.5 M despite twofold differences in amount and volume, and gave pH_normalized 0.11067 and 0.11197.
- A constant ideal weak-acid relationship is locally plausible at the dilute end, where batches 1 and 2 and the preliminary reference assays imply an apparent Ka near 4×10^-6.

Contradicted or disfavored:
- A simple absolute-loading-only account is disfavored by batches 9 and 12.
- A readily detectable monotonic precipitation threshold within 7.5×10^-6–1 M is contradicted by the final assays. Precipitation signals remained between 0 and 0.01397 without increasing systematically.
- A single, concentration-independent ideal Ka over the entire range is not supported. The apparent value changes at intermediate concentration, while high-concentration dissociation estimates approach the measurement floor.

Untested:
- Temperature, equilibration-time, stirring, atmosphere, nonaqueous-solvent, additive, and electrolyte-profile effects.
- Volumes below 0.040 L and above 0.080 L.
- Addition-order and staged-versus-bulk path dependence.
- Reversibility or hysteresis under dilution after concentration.
- Behavior beyond 1 M or below 7.5×10^-6 M.
- Whether equilibrium is reached dynamically rather than merely represented by the final benchmark snapshot.

2. Observations that changed the account

There were actual observations that changed the account.
- Batches 1 and 2 changed the initial qualitative dilution conjecture into quantitative evidence: doubling volume changed pH_normalized from 0.37064 to 0.38804 and dissociation from 0.40195 to 0.51954.
- The full monotonic pH sequence across batches 1–12 supported a concentration-response description rather than an isolated local effect.
- Batches 9 and 12 were especially consequential. Their closely matching pH at the same 0.5 M concentration, despite different amounts and volumes, shifted the account toward concentration control and away from absolute moles.
- Batches 3–8 showed that dissociation fell toward the bounded measurement floor more rapidly than a globally constant ideal weak-acid description could safely establish.
- The absence of increasing final precipitation through batch 11 at 1 M changed the initial precipitation-threshold conjecture into a no-detected-onset conclusion. The isolated intermediate signal in batch 7 was not reproduced by its final assay.

3. Competing explanations

Currently distinguishable:
- Pure absolute-moles control versus concentration control: the former is disfavored by the batch 9/batch 12 comparison.
- A large monotonic precipitation contribution versus no resolved precipitation contribution: the former is disfavored in the tested domain.

Still unresolved:
- A weak acid with concentration-dependent activities, a concentration-dependent effective Ka, background acid/base or ionic contributions, and a synthetic benchmark response can all explain the divergence from a global ideal weak-acid law.
- The pH and dissociation channels may separate at high loading because other species contribute to hydrogen-ion activity, but hidden species information is unavailable.
- Reported zero dissociation or precipitation may mean a true zero or a small positive value hidden by noise and lower-bound clipping.
- Concentration-only control and modest vessel-scale or geometry effects remain unresolved below 0.040 L.
- State-function equilibrium behavior and path-dependent transient behavior remain unresolved because no staged or reverse-path experiment was observed.

4. Single next legal experiment

I would prepare 0.010 mol reagent in 0.020 L water, terminate, and perform the final assay. This gives exactly 0.5 M at half the volume and amount of batch 9 and one quarter those of batch 12.

Possible outcomes:
- If pH_normalized remains near the batch 9/12 value of about 0.111, with dissociation and precipitation near their lower bounds, it would strengthen concentration control across a fourfold scale range.
- A reproducible pH displacement exceeding the combined assay and empirical scatter, roughly several hundredths in pH_normalized, would support an explicit volume, amount, or geometry contribution.
- A substantial precipitation signal at the smaller scale would challenge the current no-detected-precipitation account and suggest scale-sensitive supersaturation or path effects.
- A result close in pH but different only in bounded near-zero dissociation would be weak evidence because that channel is poorly resolved at 0.5 M.

5. Limits for the characterization objective

The campaign provides a broad concentration sweep but only two studied volumes, one solvent, approximately one temperature, and one endpoint protocol. There is little independent batch replication; intermediate and final instruments on the same batch are method comparisons rather than biological or physical replicates. The precipitation and high-loading dissociation channels are bounded at zero and have noise comparable with most observed signals. No formal detection limit for the precipitation proxy was established. Hidden species and mechanism mappings prevent a unique chemical mechanism. The empirical logarithmic pH fit is descriptive and shows local deviations, so extrapolation is not justified. Equilibrium_confidence is an environment diagnostic and does not replace epistemic uncertainty or evidence of equilibration.

6. Least reliable Q forecasts

Q08 and Q11 are least reliable for scale because their 0.010 L volumes are fourfold below the smallest observed volume. Q09 and Q10 are also weak because their staged and solvent-first paths were never tested; assigning them the same central result relied on an unverified state-function assumption. Q01–Q06 use 0.020 L and therefore also extrapolate in physical scale, although their concentrations remain inside the observed concentration range. Q02 is particularly uncertain for dissociation because 0.006 M lies in the sparsely observed transition toward the measurement floor. Q06 and Q11 have additional high-concentration dissociation uncertainty because a small positive fraction cannot be separated reliably from clipping. Q07 and Q12 are comparatively better anchored because they use the observed 0.040 L scale and interpolate in concentration. None of the requested concentrations exceeded the studied concentration range, but all path-control forecasts and all forecasts below 0.040 L extend beyond the strictly demonstrated scope.

7. Limits on generalization

Generalization to new loading is limited by the observed 7.5×10^-6–1 M interval and by increasing censoring of dissociation at high concentration. Generalization to dilution is limited because only 0.040 and 0.080 L were tested and concentration was changed simultaneously within most pairs. Generalization to new paths is unsupported because no order, staging, reversal, or waiting comparison was performed. Generalization to other worlds is especially limited: solvent identities may have benchmark-specific categorical effects, catalysts and species are anonymous, and the public mechanism-to-species mapping is hidden. Consequently, the results characterize this bounded water benchmark under its tested protocol; they are not transferable quantitative constants for real weak acids or general aqueous precipitation.
