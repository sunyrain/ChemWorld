# repeat-02/EQ-P04-B-Opaque

Status: completed; source assays 12/12; public note versions 2.

Physical differences below describe the selected actions under matched worlds. They do not establish that an agent proposed or tested an explanation. All notebook versions, including terminal revisions, follow verbatim.

| Assay | End event | Prior note | First later note | Mean gap / assay SD: pH, free acid, precipitate |
| --- | --- | --- | --- | --- |
| 1 | 5 | 1 | 2 | 0.056, 0.702, 0.000 |
| 2 | 10 | 1 | 2 | 0.662, 1.983, 0.000 |
| 3 | 15 | 1 | 2 | 4.470, 3.452, 0.000 |
| 4 | 20 | 1 | 2 | 15.903, 2.721, 0.000 |
| 5 | 25 | 1 | 2 | 27.300, 1.560, 0.000 |
| 6 | 30 | 1 | 2 | 23.803, 0.595, 1.566 |
| 7 | 35 | 1 | 2 | 14.790, 0.131, 3.911 |
| 8 | 40 | 1 | 2 | 6.640, 0.022, 6.891 |
| 9 | 45 | 1 | 2 | 23.803, 0.595, 1.566 |
| 10 | 50 | 1 | 2 | 23.803, 0.595, 1.566 |
| 11 | 56 | 1 | 2 | 14.797, 0.131, 3.910 |
| 12 | 62 | 1 | 2 | 6.645, 0.022, 6.888 |

## Revision 1

Available operation events: 0.

# Source-stage hypotheses

**H1 [tentative].** In water near room temperature, increasing total acid concentration should lower pH and the free deprotonated fraction; a solubility boundary may cause precipitation to rise nonlinearly at higher loading. The two supplied microloading references (R01/R02) are broadly compatible with strong dilution-dependent dissociation but differ by amounts comparable to a few stated standard deviations.

**Predictions fixed before autonomous experiments.** At a common water volume, raising feed concentration across a wide range will lower pH_normalized and acid_dissociation_fraction. Precipitation will remain near zero below a threshold and then increase. At common moles, dilution will reverse those trends. Replicate conditions will assess noise/repeatability. Equivalent explanations (activity effects versus precipitation-removal coupled to dissociation) remain unresolved unless contrasts separate them.

**Design.** Use 12 water-only batches spanning concentration with concentration-matched load/volume pairs and replicates; use one pH-meter reading per batch before termination, followed by required final assay.

## Revision 2

Available operation events: 62.

# Source-stage hypotheses and conclusions

**H1 [supported in tested aqueous scope].** Total concentration (C=n/V), rather than absolute scale, is the main identifiable control of pH at 298 K in water. Across (10^{-5})–0.4 M final assays (events runner-operation-0005 through -0040), pH fell monotonically from 5.293 to 1.564. A descriptive least-squares relation is
[
pH approx 1.390-0.805log_{10}(C/mathrm{M}),
]
with in-sample RMS residual about 0.10 pH unit; this is an empirical summary, not a general law. Concentration-matched 0.1 M batches at different scales and a replicate (events -0030, -0045, -0050) were close in pH, and matched 0.2/0.4 M direct-versus-diluted endpoints (-0035 vs -0056; -0040 vs -0062) differed by less than the quadrature of the stated final-assay SDs. Thus no resolvable independent total-volume or history effect was found.

**H2 [supported locally; censored at high loading].** For final assays from (10^{-5}) to (10^{-2}) M, the free deprotonated fraction decreased approximately as
[
alpha approx 0.00189,C^{-0.499},
]
(log-RMS residual 0.094), consistent with a square-root weak-acid asymptote and an effective scale (Ksim3.6	imes10^{-6}) M. This does not uniquely identify an ideal monoprotic equilibrium: activity corrections or simulator-specific coupled equilibria are equivalent over this slice. Above about 0.01 M, (alpha) is comparable to the 0.006 final-assay SD and bounded at zero, so the exponent should not be extrapolated or inferred from those censored readings (events -0025 to -0062).

**H3 [predicted precipitation threshold not supported].** Final precipitation signals were 0–0.017 across the entire range and were non-monotone (events -0005 to -0062). Given the stated 0.006 final-assay SD, only isolated elevations occurred and they did not reproduce at concentration-matched conditions. The pH-meter precipitation channel has still larger SD (0.02). Therefore precipitation is unresolved at/near the response floor; evidence does not establish a loading threshold in this tested water-only, instantaneous-equilibrium protocol.

**Causal dilution check.** In staged batches, doubling water increased pH_normalized by 0.0196 at 0.4→0.2 M (events -0053 to -0056) and by 0.0227 at 0.8→0.4 M (-0059 to -0062), much larger than the combined stated instrument SDs. This supports dilution as the cause of the pH shift. Dissociation and precipitation changes in these cross-instrument comparisons remain unresolved because of floor clipping and unequal sensor noise.

**Scope and remaining alternatives.** Conclusions apply to water, near 298 K, immediate measurements, (10^{-5})–0.8 M. No solvent, temperature, ionic-support, or time dependence was tested. A future decisive test would use repeated final-quality assays around 0.05–0.4 M to distinguish a true small precipitation response from zero plus bounded noise, and paired same-instrument measurements before/after dilution to avoid instrument confounding.

## Sealed K1

PUBLIC BACKGROUND
This is a bounded synthetic weak-acid/precipitation benchmark, not a model of general aqueous chemistry. Public definitions are: pH_normalized = pH/14; acid_dissociation_fraction is the free deprotonated-acid fraction relative to total acid feed; precipitation_signal is the precipitated-acid fraction relative to total feed. No material-specific property dossier or real acid identity was supplied. Water was used throughout my campaign near 298 K. Final-assay standard deviations were 0.002 for pH_normalized, 0.006 for dissociation and 0.006 for precipitation; corresponding pH-meter values were 0.004, 0.015 and 0.020. The supplied preliminary assays used 6×10^-7 mol in 0.080 and 0.075 L and respectively reported (pH_normalized, dissociation, precipitation) = (0.38205, 0.5850, 0.00393) and (0.38076, 0.5706, 0). Those are public observations, not mechanistic laws.

ACTUAL CAMPAIGN OBSERVATIONS
I completed 12 water-only batches, each with an intermediate pH-meter measurement and a final assay. Batches 1–8 used 0.060 L and nominal concentrations of 10^-5, 10^-4, 10^-3, 0.010, 0.050, 0.100, 0.200 and 0.400 mol/L. Their final (pH_normalized, dissociation, precipitation) values were:
B1: (0.37805, 0.53660, 0)
B2: (0.32817, 0.21055, 0.00771)
B3: (0.28040, 0.06399, 0.00158)
B4: (0.22588, 0.01731, 0)
B5: (0.17692, 0, 0)
B6: (0.15810, 0, 0.01726)
B7: (0.13499, 0, 0.00649)
B8: (0.11169, 0.00597, 0.00502).
Thus final pH decreased monotonically from about 5.293 to 1.564 as loading concentration rose from 10^-5 to 0.4 M. Dissociation declined rapidly and became comparable to its uncertainty and lower bound above roughly 0.01 M.

Batches 6, 9 and 10 all targeted 0.100 M but used 0.006 mol/0.060 L, 0.003 mol/0.030 L and a repeat of 0.006 mol/0.060 L. Their final pH_normalized values were 0.15810, 0.15405 and 0.15468. Their precipitation signals were 0.01726, 0 and 0.00204, while all final dissociation estimates were zero. The pH agreement is substantially better than the variation across concentration and gives no clear evidence for an independent absolute-volume effect. The precipitation disagreement instead indicates poor reproducibility near a bounded response floor.

Batches 11 and 12 tested dilution within a batch. In B11, nominal dilution from 0.4 to 0.2 M changed pH_normalized from 0.11297 by pH meter to 0.13256 by final assay. In B12, nominal dilution from 0.8 to 0.4 M changed it from 0.09131 to 0.11405. These increases, 0.0196 and 0.0227 normalized units, exceed the combined stated pH-channel noise scales. Independently prepared versus diluted final endpoints were also close: B7 versus B11 at about 0.2 M differed by 0.00243, and B8 versus B12 at about 0.4 M differed by 0.00237, both below the quadrature of two final-assay standard deviations. These results support concentration/dilution rather than absolute moles, volume, or preparation history as the primary pH control in this design.

INFERRED EFFECTIVE RELATIONSHIPS
For B1–B8, a descriptive least-squares fit was
pH ≈ 1.390 − 0.805 log10(C/1 M),
where C is total nominal loading divided by liquid volume. Its in-sample RMS residual was about 0.10 pH unit. This compactly summarizes the monotonic response over 10^-5–0.4 M but is empirical, shows some curvature, and should not be treated as a thermodynamic law or extrapolated.

For B1–B4, where dissociation remained quantifiable, a log-log fit gave
alpha ≈ 0.00189 C^-0.499,
with C in mol/L and log-RMS residual 0.094. The exponent is close to the square-root asymptote expected for a weak acid, and the coefficient corresponds heuristically to an effective scale near 3.6×10^-6 M if interpreted as sqrt(K). This interpretation is only local. At the lowest point alpha is not asymptotically small, and at higher concentration the assay is censored by noise and the zero bound.

PRECIPITATION
The predicted monotonic precipitation threshold was not observed. Final signals ranged only from 0 to 0.0173, were non-monotonic, and did not reproduce at matched concentration. For example, the three nominal 0.1 M batches gave 0.0173, 0 and 0.0020. The pH-meter precipitation channel was still noisier; its isolated value of 0.031 in concentrated B12 is only about 1.5 of that instrument's stated standard deviations above zero and fell to zero in the final diluted assay. The supported conclusion is therefore that precipitation was absent or too small to resolve reliably under these conditions—not that its true fraction is exactly zero and not that a threshold was identified.

UNCERTAINTY AND IDENTIFIABILITY
All conditions were single final assays, with only limited repeats. Zero-valued dissociation and precipitation estimates are bounded/censored observations. Concentration-matched comparisons constrain large volume or history effects but cannot exclude effects of a few thousandths in pH_normalized. The staged dilution contrasts used different instrument classes before and after dilution, although their size is much larger than the combined pH noise. Equilibrium residuals were generally near zero, while the reported equilibrium_confidence varied with condition; by contract, that quantity is an environment diagnostic and is not my epistemic confidence.

A single ideal monoprotic-acid mechanism is not uniquely established. The local alpha ∝ C^-1/2 behavior is compatible with such a model, but activity-coefficient changes, background ions, coupled acid/solid equilibria, or benchmark-specific calibration can produce similar trends. Moreover, the full-range pH slope and near-zero high-loading dissociation channel are not sufficient to demonstrate strict ideal mass-action consistency. Because precipitation was unresolved, precipitation-driven removal cannot be distinguished from an ordinary activity effect, but it is not required to explain the observed pH trend.

SUPPORTED SCOPE AND CONJECTURES
The supported scope is water near 298 K, immediate measurements, nominal concentrations from 10^-5 to 0.8 M for pH trends, and approximately 10^-5 to 10^-2 M for the fitted dissociation relationship. No evidence was collected about other solvents, temperature, ionic-support formulation, or equilibration time. It is conjecture—not an observation—that replicated high-precision assays around 0.05–0.4 M could reveal a small precipitation onset. Same-instrument paired measurements before and after dilution, plus replicated concentration-matched volumes, would better separate concentration, absolute-scale, path, activity and precipitation explanations.

## Sealed Q

{
  "predictions": [
    {
      "query_id": "Q01",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.264,
          "lower80": 0.257,
          "upper80": 0.271
        },
        "acid_dissociation_fraction": {
          "estimate": 0.042,
          "lower80": 0.03,
          "upper80": 0.055
        },
        "precipitation_signal": {
          "estimate": 0.003,
          "lower80": 0,
          "upper80": 0.014
        }
      },
      "rationale": "At 0.002 M this interpolates between observed B3 (0.001 M) and B4 (0.01 M). The locally supported inverse-square-root dissociation relation predicts about 0.042. Precipitation was unresolved near zero, so its interval is one-sided and model-dominated."
    },
    {
      "query_id": "Q02",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.238,
          "lower80": 0.231,
          "upper80": 0.245
        },
        "acid_dissociation_fraction": {
          "estimate": 0.024,
          "lower80": 0.014,
          "upper80": 0.036
        },
        "precipitation_signal": {
          "estimate": 0.003,
          "lower80": 0,
          "upper80": 0.015
        }
      },
      "rationale": "The 0.006 M concentration lies within the well-observed B3–B4 interval. Log-concentration interpolation determines pH, while the fitted dissociation relation gives about 0.024. No reproducible precipitation trend supports a nonzero threshold response."
    },
    {
      "query_id": "Q03",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.205,
          "lower80": 0.197,
          "upper80": 0.212
        },
        "acid_dissociation_fraction": {
          "estimate": 0.013,
          "lower80": 0.003,
          "upper80": 0.024
        },
        "precipitation_signal": {
          "estimate": 0.003,
          "lower80": 0,
          "upper80": 0.016
        }
      },
      "rationale": "At 0.02 M, pH is interpolated between B4 and B5. Dissociation is near the transition to floor-censored measurements, so its interval is asymmetric and includes values close to zero. Precipitation remains unresolved."
    },
    {
      "query_id": "Q04",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.171,
          "lower80": 0.164,
          "upper80": 0.179
        },
        "acid_dissociation_fraction": {
          "estimate": 0.008,
          "lower80": 0,
          "upper80": 0.018
        },
        "precipitation_signal": {
          "estimate": 0.004,
          "lower80": 0,
          "upper80": 0.018
        }
      },
      "rationale": "The 0.06 M state is interpolated between observed B5 at 0.05 M and the replicated 0.1 M conditions. Dissociation is expected to be small and frequently clipped at zero. The precipitation estimate represents a near-floor predictive center, not evidence of precipitation."
    },
    {
      "query_id": "Q05",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.134,
          "lower80": 0.127,
          "upper80": 0.141
        },
        "acid_dissociation_fraction": {
          "estimate": 0.004,
          "lower80": 0,
          "upper80": 0.014
        },
        "precipitation_signal": {
          "estimate": 0.004,
          "lower80": 0,
          "upper80": 0.019
        }
      },
      "rationale": "This directly matches the nominal concentration of B7 and the diluted endpoint of B11, whose pH_normalized values were 0.13499 and 0.13256. Their agreement supports concentration control. Dissociation and precipitation were both near their lower bounds."
    },
    {
      "query_id": "Q06",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.101,
          "lower80": 0.091,
          "upper80": 0.111
        },
        "acid_dissociation_fraction": {
          "estimate": 0.002,
          "lower80": 0,
          "upper80": 0.012
        },
        "precipitation_signal": {
          "estimate": 0.006,
          "lower80": 0,
          "upper80": 0.025
        }
      },
      "rationale": "The 0.6 M condition lies between the observed 0.4 M final endpoints and the 0.8 M intermediate state, so local high-loading interpolation gives about 0.101. Dissociation should be near the assay floor. Precipitation uncertainty is widened because this range lacked reproducible final-assay evidence for or against a small onset."
    },
    {
      "query_id": "Q07",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.171,
          "lower80": 0.164,
          "upper80": 0.179
        },
        "acid_dissociation_fraction": {
          "estimate": 0.008,
          "lower80": 0,
          "upper80": 0.018
        },
        "precipitation_signal": {
          "estimate": 0.004,
          "lower80": 0,
          "upper80": 0.018
        }
      },
      "rationale": "This is a 0.06 M scale control. Concentration-matched campaign batches showed no resolvable independent volume effect, so the central prediction equals Q04. The interval retains model and final-assay uncertainty."
    },
    {
      "query_id": "Q08",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.171,
          "lower80": 0.163,
          "upper80": 0.18
        },
        "acid_dissociation_fraction": {
          "estimate": 0.008,
          "lower80": 0,
          "upper80": 0.019
        },
        "precipitation_signal": {
          "estimate": 0.004,
          "lower80": 0,
          "upper80": 0.019
        }
      },
      "rationale": "The final concentration again equals 0.06 M. No independent scale effect was identified, but 0.01 L is slightly outside the directly compared campaign volumes, so the intervals are marginally wider than for Q04 and Q07."
    },
    {
      "query_id": "Q09",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.134,
          "lower80": 0.126,
          "upper80": 0.142
        },
        "acid_dissociation_fraction": {
          "estimate": 0.004,
          "lower80": 0,
          "upper80": 0.015
        },
        "precipitation_signal": {
          "estimate": 0.004,
          "lower80": 0,
          "upper80": 0.02
        }
      },
      "rationale": "The staged additions end at the same 0.2 M composition as Q05. Direct-versus-diluted campaign endpoints showed no resolvable preparation-history effect, so final concentration governs the point estimates. Intervals are slightly widened for an unexcluded small path effect."
    },
    {
      "query_id": "Q10",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.134,
          "lower80": 0.126,
          "upper80": 0.142
        },
        "acid_dissociation_fraction": {
          "estimate": 0.004,
          "lower80": 0,
          "upper80": 0.015
        },
        "precipitation_signal": {
          "estimate": 0.004,
          "lower80": 0,
          "upper80": 0.02
        }
      },
      "rationale": "Combining solvent additions before reagent additions produces the same final loading and volume as Q05 and Q09. Available observations support endpoint concentration control rather than order dependence, although a small unmeasured path effect remains within the interval."
    },
    {
      "query_id": "Q11",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.101,
          "lower80": 0.089,
          "upper80": 0.113
        },
        "acid_dissociation_fraction": {
          "estimate": 0.002,
          "lower80": 0,
          "upper80": 0.013
        },
        "precipitation_signal": {
          "estimate": 0.006,
          "lower80": 0,
          "upper80": 0.027
        }
      },
      "rationale": "This shares Q06's 0.6 M concentration but uses only 0.01 L. No scale effect was resolved at lower concentrations, so the central estimates are unchanged. The intervals are wider because both concentration and this small absolute volume extend beyond directly replicated final endpoints."
    },
    {
      "query_id": "Q12",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.101,
          "lower80": 0.09,
          "upper80": 0.112
        },
        "acid_dissociation_fraction": {
          "estimate": 0.002,
          "lower80": 0,
          "upper80": 0.013
        },
        "precipitation_signal": {
          "estimate": 0.006,
          "lower80": 0,
          "upper80": 0.026
        }
      },
      "rationale": "At 0.6 M and 0.04 L, concentration-based interpolation gives the same center as Q06 and Q11. The volume is closer to tested scales, but high-loading dissociation remains floor-censored and precipitation remains structurally uncertain."
    }
  ],
  "rationale": "Predictions use log-concentration interpolation of the sealed pH account, the locally supported relation alpha approximately 0.00189 times C to the power -0.499, and the observed absence of a reproducible volume or preparation-path effect. Intervals combine final-assay noise with interpolation, extrapolation, floor clipping and model uncertainty. Precipitation intervals are deliberately broad and bounded at zero because campaign signals were small, non-monotonic and poorly reproducible."
}

## Sealed K2

1. SUPPORTED, CONTRADICTED, AND UNTESTED RELATIONSHIPS

Supported within the studied water-only, near-298 K domain: total nominal concentration C = n/V is the principal identifiable control of pH. Across B1–B8, increasing C from 10^-5 to 0.4 mol/L monotonically reduced pH_normalized from 0.37805 to 0.11169. The concentration-matched batches B6, B9 and B10, and the matched direct-versus-diluted endpoints B7/B11 and B8/B12, gave no resolvable independent volume or preparation-history effect on final pH. The staged dilutions in B11 and B12 raised pH_normalized by 0.0196 and 0.0227, supporting a causal dilution response.

Also supported locally is decreasing free dissociation with increasing concentration. From B1 through B4, acid_dissociation_fraction fell from 0.53660 to 0.01731 and was summarized by the empirical relation alpha approximately 0.00189 C^-0.499. This square-root-like behavior is supported only over approximately 10^-5–10^-2 M. At greater loading, the values approached the assay noise and zero bound.

The initial expectation of a detectable monotonic precipitation threshold was not supported. Final precipitation signals were small, non-monotonic and not reproducible at matched concentration. For example, nominally 0.1 M B6, B9 and B10 produced 0.01726, 0 and 0.00204. This contradicts a simple, clearly resolved increasing precipitation curve, but it does not prove that the true precipitated fraction is exactly zero.

Untested relationships include solvent identity, temperature, atmosphere, ionic-support formulation, waiting time, equilibration kinetics and repeated reagent-addition order. Absolute-volume effects smaller than the achieved resolution also remain untested. The campaign did not test other aqueous-equilibrium worlds or real named acids.

2. OBSERVATIONS THAT CHANGED THE ACCOUNT

There were actual observations that changed my account. Before experimentation I expected increasing loading to lower pH and dissociation, but also expected precipitation to rise beyond a threshold. B1–B8 confirmed the first two qualitative predictions. The small and non-monotonic final precipitation values, especially the disagreement among B6, B9 and B10, caused me to withdraw the precipitation-threshold claim and classify precipitation as unresolved near the response floor.

The concentration-matched scale comparisons changed the account from a general loading-and-volume description to the narrower inference that concentration is the dominant identifiable variable. The staged B11 and B12 dilution shifts strengthened that conclusion. Conversely, the zero-clipped high-loading dissociation results narrowed the supported range of the fitted dissociation law; I did not treat those zeros as evidence for literally zero dissociation.

3. COMPETING EXPLANATIONS

Concentration and absolute volume were partly distinguishable because the campaign included concentration-matched conditions at different scales. Within available precision, those observations favor concentration control, although small volume effects remain possible.

A local ideal weak-acid interpretation, concentration-dependent activities, background ionic effects and other coupled aqueous equilibria remain unresolved alternatives. The approximately -1/2 dissociation exponent is compatible with a weak-acid asymptote but does not uniquely identify it. The full-range pH trend and the near-floor high-loading dissociation channel do not establish strict ideal monoprotic mass-action consistency.

True precipitation below a few percent and zero precipitation plus bounded observation noise are also unresolved. Coupling between precipitation and acid dissociation cannot be identified because precipitation was not reproducibly resolved. Likewise, the agreement of direct and diluted endpoints constrains large history effects, but it does not prove complete reversibility or exclude rapid path-dependent processes that relax before measurement.

4. NEXT SINGLE LEGAL EXPERIMENT

I would exactly replicate B6: add 0.060 L water, add 0.006 mol reagent to obtain 0.1 M, take the permitted intermediate pH-meter measurement, terminate, and perform the required final assay. This targets the most consequential internal discrepancy: B6 reported precipitation_signal 0.01726, whereas the two other 0.1 M endpoints were 0 and 0.00204.

A repeated final precipitation signal around or above 0.012–0.018 would corroborate a small real response at 0.1 M and weaken the explanation that B6 was merely a positive fluctuation. A result near 0–0.006 would favor a floor-plus-noise explanation and further reject a reproducible threshold at that concentration. An intermediate result would remain ambiguous. Concurrent pH agreement near the previous 0.1 M results would show that any precipitation disagreement is not simply caused by a gross concentration error. One additional batch would still not be decisive because the final-assay precipitation standard deviation is 0.006.

5. LIMITS OF THE AVAILABLE EVIDENCE

Each condition had only one final assay, with limited exact replication. Measurement errors were supplied by the benchmark, but no independent estimate of between-batch process variability was available. Dissociation and precipitation were bounded at zero, making ordinary symmetric-error interpretations inappropriate near the floor. Intermediate and final dilution measurements used different instruments with different noise, so those causal contrasts include an instrument-class confound.

The empirical pH equation is a descriptive fit with about 0.10 pH-unit in-sample RMS residual, not a validated thermodynamic law. The dissociation power law uses only four quantifiable final points. The precipitation observations do not support estimating a threshold or slope. No time course established whether measurements represented a unique thermodynamic equilibrium rather than a rapidly attained benchmark state. The environment's equilibrium_confidence is only a diagnostic and cannot substitute for scientific confidence.

6. LEAST RELIABLE Q FORECASTS

Q06, Q11 and Q12 are least reliable overall. Their 0.6 M final concentration exceeds the greatest concentration measured by a final assay in the campaign, 0.4 M. The only 0.8 M evidence was an intermediate pH-meter observation, so their pH forecasts require cross-instrument interpolation and their dissociation and precipitation forecasts rely heavily on extrapolation and floor behavior.

Q11 is additionally weak because its 0.010 L scale is below the campaign's smallest directly tested batch volume of 0.030 L. Q08 has the same small-volume limitation even though its 0.06 M concentration is well bracketed. Q09 and Q10 are compositionally within scope, but their specific staged-reagent and solvent-first ordering was not tested; the campaign examined dilution history rather than those exact addition-order paths.

For every Q batch, precipitation is the least reliable metric because no stable concentration-response relation was identified. High-loading dissociation predictions are also weak because campaign measurements were noise-limited and clipped at zero. The most defensible forecasts are the pH predictions for Q01–Q05 and Q07–Q10, whose concentrations lie inside the final-assay range, subject to the scale and path qualifications above.

7. GENERALIZATION LIMITS

Interpolation to new loading is most defensible within 10^-5–0.4 M, whereas extrapolation beyond 0.4 M may miss curvature, activity changes or precipitation onset. Dilution predictions assume that only final concentration matters; this was supported for twofold dilution and tested scales but not for arbitrarily large dilution ratios or extremely small volumes. Path generalization is limited because measurements were immediate and only two staged dilution paths were studied. Addition order, waiting, mixing and hysteresis were not systematically varied.

Finally, this is an anonymous bounded synthetic benchmark. Its fitted coefficients, response floors and diagnostic channels cannot be transferred to a different hidden world, a named acid, another solvent, or real laboratory chemistry without new evidence.
