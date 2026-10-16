# repeat-02/EQ-P02-B-Opaque

Status: completed; source assays 12/12; public note versions 2.

Physical differences below describe the selected actions under matched worlds. They do not establish that an agent proposed or tested an explanation. All notebook versions, including terminal revisions, follow verbatim.

| Assay | End event | Prior note | First later note | Mean gap / assay SD: pH, free acid, precipitate |
| --- | --- | --- | --- | --- |
| 1 | 5 | 1 | 2 | 0.029, 0.814, 0.000 |
| 2 | 10 | 1 | 2 | 14.228, 3.880, 0.000 |
| 3 | 15 | 1 | 2 | 25.210, 2.292, 0.012 |
| 4 | 20 | 1 | 2 | 17.060, 0.570, 3.879 |
| 5 | 25 | 1 | 2 | 9.362, 0.119, 7.437 |
| 6 | 30 | 1 | 2 | 2.993, 0.015, 11.472 |
| 7 | 35 | 1 | 2 | 17.060, 0.570, 3.879 |
| 8 | 40 | 1 | 2 | 9.362, 0.119, 7.437 |
| 9 | 45 | 1 | 2 | 2.993, 0.015, 11.472 |
| 10 | 50 | 1 | 2 | 14.228, 3.880, 0.000 |
| 11 | 55 | 1 | 2 | 0.000, 0.000, 8.413 |
| 12 | 60 | 1 | 2 | 0.000, 0.000, 8.413 |

## Revision 1

Available operation events: 0.

# Hypothesis notebook

## H1 [tentative]
In water near room temperature, increasing total acid loading at fixed liquid volume should lower pH and reduce the free dissociation fraction; sufficiently high loading may increase the precipitation proxy. Dilution at fixed feed should reverse these responses. The preliminary R01/R02 pair is too noisy and narrow to establish the small volume effect.

**Prospective tests.** Use a concentration grid spanning dilute to concentrated conditions, with matched concentrations created from different amount/volume pairs to distinguish concentration control from separate amount or volume effects. A conventional weak-acid picture predicts approximately concentration-dependent pH and dissociation before precipitation, while precipitation could break simple similarity at high loading. Include repeats to assess measurement scatter. These claims will be revised if matched-concentration outcomes differ beyond assay variation or if trends are non-monotone.

## Revision 2

Available operation events: 60.

# Hypothesis notebook

## H1 [supported within tested aqueous scope]
For water at about 298 K and feeds from 0.01 to 1.0 mol L⁻¹, final pH is governed mainly by nominal loading concentration (C=n/V), not by amount or volume separately. Final-assay matched-concentration pairs at 0.01, 0.10, 0.20, and 0.40 M (events runner-operation-0010/0050, 0020/0035, 0025/0040, 0030/0045) differed by only 0.009–0.042 pH unit after converting pH_normalized ×14, small relative to the broad concentration trend. Across this range an empirical summary is pH_normalized ≈ 0.0769 − 0.0308 ln(C/M), equivalently pH ≈ 1.08 − 0.99 log10(C/M). This is descriptive, not a mechanistic law or an extrapolation outside the tested range.

The ultra-dilute 7.5×10⁻⁶ M condition (runner-operation-0005; pH ≈5.28) lies outside that fitted range and has a large dissociation fraction (~0.716), consistent with a transition toward extensive weak-acid dissociation. It should not be forced onto the concentrated empirical line.

## H2 [supported qualitatively; threshold shape unresolved]
The free deprotonated-acid fraction falls steeply with loading: it was ~0.716 at 7.5×10⁻⁶ M (runner-operation-0005), ~0.006–0.013 at 0.01 M (runner-operation-0010/0050), and assay-floor-like at ≥0.05 M. Clipping at zero and stated assay noise prevent identifying the exact concentrated dependence. A conventional weak-acid equilibrium with activity effects, a buffered/ionic background, or another effective concentration-dependent equilibrium remain observationally equivalent here; pH and the public fraction alone do not identify microscopic species.

## H3 [supported onset, unresolved functional form]
The precipitation proxy is near its noise floor from dilute conditions through 0.40 M, but becomes reproducibly positive at 1.0 M: 0.0435 and 0.0560 in duplicate final assays (runner-operation-0055 and runner-operation-0060). The duplicate numerical difference is not by itself evidence of a batch effect. These results support a high-loading precipitation onset between 0.4 and 1.0 M, but the sparse bracket cannot distinguish a sharp solubility threshold from a smooth bounded response or concentration-dependent activity.

## Measurement and scope decisions
Final assays carry the lower stated noise and are the primary comparisons; same-batch pH-meter readings broadly track them but show larger scatter, especially in small precipitation signals. All autonomous batches used water near ambient temperature, so solvent identity, temperature, kinetics, and electrolyte/catalyst alternatives remain untested. No time series was performed; the explicit termination assay is treated as the operational equilibrium endpoint, not proof of a unique thermodynamic mechanism.

**Testable consequences.** Additional water points between 0.4 and 1.0 M should localize precipitation onset; matched (C) with wider amount/volume separation should continue to agree if concentration similarity is exact. Measurements below 0.01 M should show rising dissociation and departure from the concentrated pH line. A systematic matched-(C) discrepancy beyond repeatability would overturn the concentration-only simplification.

## Sealed K1

## Scope and evidence classes

**Public background.** This is a bounded synthetic weak-acid/precipitation world. The reported quantities are pH_normalized = pH/14, acid_dissociation_fraction = free deprotonated acid divided by total acid feed, and precipitation_signal = precipitated acid divided by total acid feed. Species identities and the hidden mechanism-to-species mapping are not public. Final-assay stated one-standard-deviation noise is 0.002 for pH_normalized (0.028 pH unit), 0.006 for dissociation fraction, and 0.006 for precipitation signal. Equilibrium_confidence is an environment diagnostic, not my scientific confidence.

**Experimental scope.** I completed 12 water batches near 298 K. Nominal concentration was calculated as total reagent loading divided by initial liquid volume. Every batch was terminated and then measured by final assay; a noisier pH-meter measurement was also made before termination. No solvent, temperature, time, catalyst, or electrolyte-profile comparison was performed. Consequently, the conclusions below apply only to this ambient aqueous slice.

## Actual observations

The final-assay observations were:

| Batch | Volume (L) | Loading (mol) | Nominal C (mol L⁻¹) | pH_normalized | pH | Dissociation fraction | Precipitation signal |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.080 | 0.0000006 | 0.0000075 | 0.37737 | 5.283 | 0.71590 | 0.00000 |
| 2 | 0.080 | 0.0008 | 0.010 | 0.21546 | 3.016 | 0.00565 | 0.00224 |
| 3 | 0.080 | 0.004 | 0.050 | 0.17211 | 2.410 | 0.00000 | 0.00383 |
| 4 | 0.080 | 0.008 | 0.100 | 0.14808 | 2.073 | 0.00000 | 0.00000 |
| 5 | 0.080 | 0.016 | 0.200 | 0.12688 | 1.776 | 0.00304 | 0.00538 |
| 6 | 0.080 | 0.032 | 0.400 | 0.10489 | 1.468 | 0.00000 | 0.00101 |
| 7 | 0.040 | 0.004 | 0.100 | 0.14922 | 2.089 | 0.00532 | 0.01001 |
| 8 | 0.040 | 0.008 | 0.200 | 0.12794 | 1.791 | 0.00257 | 0.01337 |
| 9 | 0.040 | 0.016 | 0.400 | 0.10551 | 1.477 | 0.00143 | 0.00000 |
| 10 | 0.040 | 0.0004 | 0.010 | 0.21846 | 3.058 | 0.01317 | 0.00000 |
| 11 | 0.040 | 0.040 | 1.000 | 0.07461 | 1.044 | 0.00000 | 0.04350 |
| 12 | 0.040 | 0.040 | 1.000 | 0.07605 | 1.065 | 0.00000 | 0.05596 |

Two supplied standardized preliminary assays are also actual public observations. R01 used 0.080 L and 0.0000006 mol and gave pH_normalized 0.37597, dissociation 0.73218, and precipitation 0.00425. R02 used 0.075 L and the same loading and gave 0.37654, 0.71465, and 0.00000, respectively. These agree with autonomous Batch 1 within the expected measurement variation.

## Supported effective relationships

### Loading, dilution, and pH

At fixed volume, increasing loading produced a strong, monotonic decrease in pH. From 0.01 to 1.0 M, pH fell from approximately 3.0 to 1.05. An empirical least-squares summary over the observed 0.01–1.0 M data is

pH_normalized ≈ 0.0769 − 0.0308 ln(C/1 M),

or equivalently

pH ≈ 1.08 − 0.99 log10(C/1 M).

Thus, in that bounded interval, hydrogen-ion activity behaves approximately as a power law proportional to C^0.99, with an effective proportionality near 0.084. This is an empirical description, not an identified mass-action mechanism.

The formula must not be extrapolated to the ultra-dilute regime. At 7.5×10⁻⁶ M it would predict a substantially higher pH than the observed 5.28. The ultra-dilute data therefore establish curvature or a regime transition somewhere below 0.01 M.

### Concentration versus separate volume or amount effects

Matched nominal concentrations were prepared at both 0.080 and 0.040 L. The pH differences were only 0.042 pH unit at 0.01 M, 0.016 at 0.10 M, 0.015 at 0.20 M, and 0.009 at 0.40 M. These are small compared with the multi-unit loading trend and comparable to combined assay uncertainty. The duplicate 1.0 M batches differed by 0.020 pH unit.

The supported simplification is therefore that pH depends predominantly on n/V, rather than independently on n or V, over 0.01–1.0 M and volumes of 0.040–0.080 L. Dilution at fixed loading should raise pH, while concentration should lower it. The data do not prove exact concentration similarity, and they cannot exclude smaller volume effects.

### Acid dissociation

The dissociation response is strongly loading-dependent. At approximately 7.5–8.0×10⁻⁶ M, the three available assays gave fractions of about 0.715–0.732. At 0.01 M, Batches 2 and 10 gave 0.0057 and 0.0132. At 0.05–1.0 M, all final-assay values were between zero and 0.0053, comparable to the stated 0.006 assay noise and often clipped at the zero boundary.

It is therefore well supported that free dissociation is extensive in the measured ultra-dilute regime and much smaller by 0.01 M. Its detailed functional form above 0.01 M is not identifiable because the signal is near the measurement floor. The apparent small differences among concentrated batches should not be interpreted as a resolved non-monotonic law.

Under a conventional Henderson–Hasselbalch interpretation, the ultra-dilute pH and dissociation fraction imply an effective pKa around 4.8–4.9. In Batch 1, the independently implied hydrogen concentration and alpha times total concentration are also similar. This makes a monoprotic weak-acid equilibrium a plausible local explanation for the dilute regime. However, a single ideal weak-acid model does not straightforwardly reproduce both the concentrated pH values and the near-zero reported free-deprotonated fractions. Activity corrections, an ionic or acidic background, coupled equilibria, or a distinction between the proton-controlling pool and the reported free fraction would be required. Because hidden species are unavailable, these alternatives cannot be separated.

### Precipitation

From the ultra-dilute condition through 0.40 M, precipitation signals were generally at or near the assay floor. The largest isolated values below 1.0 M were 0.0100 in Batch 7 and 0.0134 in Batch 8; their matched-concentration partners were smaller, and there was no coherent monotonic progression across 0.01–0.40 M.

At 1.0 M, duplicate Batches 11 and 12 gave 0.0435 and 0.0560. Both are many individual assay standard deviations above zero, while their difference is modest relative to combined measurement variation. This supports a reproducible high-loading precipitation response of roughly 0.05 of total feed at 1.0 M. The onset is bracketed only between 0.40 and 1.0 M. The data cannot distinguish a sharp solubility threshold, a smooth activity-dependent rise, or another bounded proxy response.

There is no compelling evidence here for an independent absolute-volume effect on precipitation. At matched 0.10 and 0.20 M, the smaller-volume batches had somewhat larger numerical signals, but those values were near the noise floor, and the direction did not persist at 0.40 M. This question remains unresolved rather than disproved.

## Uncertainty and diagnostic limitations

The final assay is the primary basis for inference because its stated noise is lower than that of the intermediate pH meter. Same-batch intermediate readings broadly followed the final trends but sometimes differed visibly in near-zero dissociation or precipitation channels, as expected when bounded noisy estimates are close to zero. Zero readings should be treated as floor-limited estimates, not proof of an exactly absent species or process.

The pH concentration relation is supported by several matched-concentration pairs and two 1.0 M replicates, but the experimental design contains few exact replicates elsewhere. The precipitation threshold is only coarsely bracketed. No kinetic series was collected, so termination defines the operational endpoint but does not demonstrate a unique thermodynamic mechanism. The observed final equilibrium residuals were small, while equilibrium_confidence was an environment diagnostic; neither substitutes for mechanistic validation.

## Competing explanations and conjectures

1. **Ideal weak acid at low concentration with non-ideal concentrated behavior:** supported locally by the ultra-dilute pH and dissociation fraction; concentrated behavior would require strong activity corrections or additional equilibria.
2. **Buffered, ionic, or acidic background:** could explain why concentrated pH is nearly proportional to total loading while the reported free-deprotonated fraction is near zero.
3. **Multiple acid pools or coupled association:** could decouple the pH-controlling proton balance from the specifically defined free deprotonated fraction.
4. **Precipitation-coupled speciation:** may contribute near 1.0 M, but a roughly 5% precipitation proxy alone does not uniquely explain the entire concentrated pH trend.
5. **Smooth versus threshold precipitation:** both remain viable because no observations were made between 0.40 and 1.0 M.

These are competing conjectures, not identified mechanisms. The public measurements constrain effective relationships but do not reveal microscopic species.

## Bounded conclusions and testable predictions

Within water near 298 K, nominal concentration is the dominant observed control variable. From 0.01 to 1.0 M, pH follows an approximately unit-slope inverse logarithmic relation with concentration. Free dissociation changes from about 0.72 at roughly 8×10⁻⁶ M to assay-floor levels by 0.01 M. Precipitation remains near its floor through 0.40 M and becomes reproducibly positive, around 0.05, at 1.0 M.

Further points between 0.40 and 1.0 M would localize the precipitation onset. Points between 8×10⁻⁶ and 0.01 M would map the dissociation transition and the departure from the concentrated pH law. More widely separated matched-volume preparations at fixed n/V would test the concentration-only simplification. Any reproducible matched-concentration difference substantially exceeding assay and batch variation would require adding an independent volume or total-amount term.

## Sealed Q

{
  "predictions": [
    {
      "query_id": "Q01",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.256,
          "lower80": 0.242,
          "upper80": 0.27
        },
        "acid_dissociation_fraction": {
          "estimate": 0.05,
          "lower80": 0.022,
          "upper80": 0.09
        },
        "precipitation_signal": {
          "estimate": 0.002,
          "lower80": 0,
          "upper80": 0.015
        }
      },
      "rationale": "At 0.002 M this lies between the observed ultra-dilute, highly dissociated regime and the 0.01 M low-dissociation regime. A weak-acid transition plus the concentrated empirical pH trend predicts partial dissociation and pH_normalized near 0.256. The interval is widened because this concentration and 0.020 L scale were not directly tested. Precipitation should remain at the bounded assay floor."
    },
    {
      "query_id": "Q02",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.229,
          "lower80": 0.219,
          "upper80": 0.239
        },
        "acid_dissociation_fraction": {
          "estimate": 0.022,
          "lower80": 0.006,
          "upper80": 0.043
        },
        "precipitation_signal": {
          "estimate": 0.002,
          "lower80": 0,
          "upper80": 0.015
        }
      },
      "rationale": "At 0.006 M the batch approaches the observed 0.01 M regime but should retain somewhat greater dissociation. The pH estimate blends the dilute weak-acid interpretation with the empirical concentration relationship. Precipitation is expected to be indistinguishable from zero; intervals include assay noise and uncertainty in the unmeasured transition."
    },
    {
      "query_id": "Q03",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.196,
          "lower80": 0.189,
          "upper80": 0.203
        },
        "acid_dissociation_fraction": {
          "estimate": 0.0076,
          "lower80": 0,
          "upper80": 0.02
        },
        "precipitation_signal": {
          "estimate": 0.002,
          "lower80": 0,
          "upper80": 0.016
        }
      },
      "rationale": "The 0.02 M concentration is inside the interpolation region between observed 0.01 and 0.05 M batches. The fitted inverse-logarithmic pH relationship gives about 0.196, while dissociation is predicted to be small and close to assay resolution. No precipitation trend was resolved at such low loading."
    },
    {
      "query_id": "Q04",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.164,
          "lower80": 0.157,
          "upper80": 0.17
        },
        "acid_dissociation_fraction": {
          "estimate": 0.0027,
          "lower80": 0,
          "upper80": 0.013
        },
        "precipitation_signal": {
          "estimate": 0.002,
          "lower80": 0,
          "upper80": 0.016
        }
      },
      "rationale": "At 0.06 M this interpolates closely between observed 0.05 and 0.10 M behavior. Concentration control predicts pH_normalized near 0.164 and a dissociation fraction near the lower measurement boundary. Precipitation should remain near zero; the 0.020 L scale adds modest uncertainty."
    },
    {
      "query_id": "Q05",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.127,
          "lower80": 0.12,
          "upper80": 0.134
        },
        "acid_dissociation_fraction": {
          "estimate": 0.0008,
          "lower80": 0,
          "upper80": 0.012
        },
        "precipitation_signal": {
          "estimate": 0.004,
          "lower80": 0,
          "upper80": 0.025
        }
      },
      "rationale": "The final concentration exactly matches observed 0.20 M batches, whose pH_normalized values were about 0.127. Their dissociation estimates were at the assay floor and their small precipitation signals were inconsistent with a resolved monotonic effect. The smaller 0.020 L volume is extrapolative, so the precipitation interval allows a possible scale effect without asserting one."
    },
    {
      "query_id": "Q06",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.093,
          "lower80": 0.085,
          "upper80": 0.101
        },
        "acid_dissociation_fraction": {
          "estimate": 0.0003,
          "lower80": 0,
          "upper80": 0.01
        },
        "precipitation_signal": {
          "estimate": 0.003,
          "lower80": 0,
          "upper80": 0.03
        }
      },
      "rationale": "At 0.60 M, logarithmic interpolation between observed 0.40 and 1.0 M results gives pH_normalized near 0.093 and essentially floor-level free dissociation. Precipitation was near zero at 0.40 M and about 0.05 at 1.0 M. A solubility-threshold interpretation predicts little at 0.60 M, but the broad interval also admits a smoother onset."
    },
    {
      "query_id": "Q07",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.164,
          "lower80": 0.158,
          "upper80": 0.17
        },
        "acid_dissociation_fraction": {
          "estimate": 0.0027,
          "lower80": 0,
          "upper80": 0.013
        },
        "precipitation_signal": {
          "estimate": 0.002,
          "lower80": 0,
          "upper80": 0.015
        }
      },
      "rationale": "This 0.040 L scale is within the observed volume range. The supported concentration-similarity relationship therefore gives the same central prediction as Q04 at 0.06 M: pH_normalized near 0.164, floor-level dissociation, and no resolved precipitation."
    },
    {
      "query_id": "Q08",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.164,
          "lower80": 0.153,
          "upper80": 0.174
        },
        "acid_dissociation_fraction": {
          "estimate": 0.0027,
          "lower80": 0,
          "upper80": 0.016
        },
        "precipitation_signal": {
          "estimate": 0.002,
          "lower80": 0,
          "upper80": 0.022
        }
      },
      "rationale": "The final concentration is again 0.06 M, so concentration control gives the same point estimates as Q04 and Q07. However, 0.010 L is below the tested 0.040–0.080 L range; intervals are widened to account for an unresolved independent scale effect."
    },
    {
      "query_id": "Q09",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.127,
          "lower80": 0.119,
          "upper80": 0.135
        },
        "acid_dissociation_fraction": {
          "estimate": 0.0008,
          "lower80": 0,
          "upper80": 0.013
        },
        "precipitation_signal": {
          "estimate": 0.004,
          "lower80": 0,
          "upper80": 0.028
        }
      },
      "rationale": "Its final state is 0.20 M, matching Q05 and the observed 0.20 M batches. No experimental evidence established path dependence, so the staged additions are predicted to converge to the same endpoint. The interval is widened because the campaign did not directly test staging or transient precipitation."
    },
    {
      "query_id": "Q10",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.127,
          "lower80": 0.119,
          "upper80": 0.135
        },
        "acid_dissociation_fraction": {
          "estimate": 0.0008,
          "lower80": 0,
          "upper80": 0.013
        },
        "precipitation_signal": {
          "estimate": 0.004,
          "lower80": 0,
          "upper80": 0.028
        }
      },
      "rationale": "The final amount, volume, and concentration equal those of Q09 and Q05. Under the operational equilibrium interpretation, solvent-first ordering should not change the final observables. Because addition-order effects were not measured, model uncertainty is retained, particularly for precipitation."
    },
    {
      "query_id": "Q11",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.093,
          "lower80": 0.082,
          "upper80": 0.104
        },
        "acid_dissociation_fraction": {
          "estimate": 0.0003,
          "lower80": 0,
          "upper80": 0.013
        },
        "precipitation_signal": {
          "estimate": 0.003,
          "lower80": 0,
          "upper80": 0.035
        }
      },
      "rationale": "The 0.60 M concentration implies the same central equilibrium response as Q06. The 0.010 L scale is outside the tested range, so the pH, dissociation, and especially precipitation intervals are wider. The central precipitation prediction remains near zero because the observed onset occurred only between 0.40 and 1.0 M."
    },
    {
      "query_id": "Q12",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.093,
          "lower80": 0.086,
          "upper80": 0.1
        },
        "acid_dissociation_fraction": {
          "estimate": 0.0003,
          "lower80": 0,
          "upper80": 0.01
        },
        "precipitation_signal": {
          "estimate": 0.003,
          "lower80": 0,
          "upper80": 0.03
        }
      },
      "rationale": "At 0.040 L this lies within the tested scale and has the same 0.60 M concentration as Q06 and Q11. The concentration-based model predicts pH_normalized near 0.093, negligible resolved dissociation, and little precipitation. The precipitation interval remains asymmetric and broad because only the 0.40 M near-zero and 1.0 M positive endpoints bracket this concentration."
    }
  ],
  "rationale": "Predictions use the sealed K1 conclusions: concentration is the dominant endpoint variable; pH follows an approximately inverse-logarithmic concentration relationship in the concentrated regime; dissociation rises strongly on dilution; and precipitation is near its floor through 0.40 M but approximately 0.05 at 1.0 M. A weak-acid transition was used below 0.01 M rather than blindly extrapolating the concentrated linear fit. Equal-concentration scale and path controls share central estimates because no scale or ordering effect was established, while their intervals widen outside the tested 0.040–0.080 L range or for untested staging. Intervals combine final-assay noise, empirical-model uncertainty, bounded zero clipping, sparse replication, and uncertainty about whether precipitation begins sharply or smoothly between 0.40 and 1.0 M."
}

## Sealed K2

1. **Supported, contradicted, and untested relationships**

**Supported within the measured aqueous scope:** Nominal concentration, n/V, is the dominant predictor of pH. From 0.01 to 1.0 mol L⁻¹, pH decreased approximately linearly with log concentration. Matched-concentration pairs at 0.01, 0.10, 0.20, and 0.40 mol L⁻¹ produced similar pH values despite twofold changes in volume and amount. Free dissociation was high near 8×10⁻⁶ mol L⁻¹ and at or near the assay floor by 0.01 mol L⁻¹. Precipitation remained near its measurement floor through 0.40 mol L⁻¹ but was reproducibly about 0.05 at 1.0 mol L⁻¹.

**Contradicted or inadequate:** A single inverse-logarithmic pH relationship extending across the entire loading range is contradicted by the ultra-dilute observations, which depart substantially from the 0.01–1.0 mol L⁻¹ fit. An unmodified ideal monoprotic-acid model is inadequate across the complete range because it does not simultaneously explain the concentrated pH and near-zero free-deprotonated fraction. The observations also contradict any large, monotonic precipitation response below 0.40 mol L⁻¹. They do not contradict smaller precipitation signals hidden by noise.

**Untested:** Exact concentration similarity outside 0.040–0.080 L; behavior at intermediate concentrations between 8×10⁻⁶ and 0.01 mol L⁻¹; the precipitation curve between 0.40 and 1.0 mol L⁻¹; addition-order effects; equilibration time and hysteresis; other temperatures, solvents, atmospheres, catalysts, or electrolyte profiles; and microscopic species identities.

2. **Observations that changed the account**

Actual campaign observations did change the initial tentative account. The matched-concentration pairs shifted the account toward concentration control rather than independent amount or volume control. Batch 1 and preliminary assays R01/R02 established an ultra-dilute, highly dissociated regime and showed that the concentrated pH fit could not be globally extrapolated. Batches 2–10 established the steep decrease in pH and dissociation with loading. The duplicate 1.0 mol L⁻¹ results in Batches 11 and 12 changed precipitation from an unresolved near-zero response into a supported high-loading onset.

No observations occurred after K1 and Q were sealed, and no prediction truth or scores were supplied. Therefore, nothing after sealing changed the account or validated the forecasts.

3. **Competing explanations**

A conventional weak-acid equilibrium is plausible locally in the ultra-dilute regime and gives an effective pKa near 4.8–4.9. Across the full range, it remains unresolved whether departures arise from activity corrections, an acidic or ionic background, multiple coupled acid pools, association, or a distinction between the proton-controlling pool and the reported free-deprotonated fraction. Hidden species prevent resolving these alternatives from pH and fraction measurements alone.

For precipitation, a sharp solubility threshold near the upper end of 0.40–1.0 mol L⁻¹ and a smooth concentration-dependent rise remain distinguishable in principle but unresolved by the existing bracket. A small absolute-volume effect is also unresolved because some low-level precipitation readings were numerically higher at 0.040 L, but the pattern was inconsistent and close to assay noise. Final-state equilibrium and path-dependent trapping are likewise unresolved because no staged or reordered preparation was measured.

4. **Single next legal experiment**

I would prepare 0.040 L of water with 0.032 mol reagent, giving 0.80 mol L⁻¹, then terminate and perform the final assay. This uses the same water and a tested volume while placing one point inside the precipitation gap.

A precipitation signal near zero would support a comparatively sharp threshold closer to 1.0 mol L⁻¹. A signal around 0.03 would support a smooth rise between 0.40 and 1.0 mol L⁻¹. A signal near or above 0.05 would imply an earlier or steeper onset than inferred. Its pH and dissociation measurements would also test interpolation of the concentrated relationships, but precipitation would be the primary discriminator. One result would still not identify a unique functional form; replication would subsequently be required.

5. **Limits of the evidence**

Only 12 autonomous batches were completed, with few exact replicates and only two high-loading replicates. All used water near 298 K and immediate operational termination. The final assay has finite noise, and bounded clipping makes zero values especially difficult to interpret. Dissociation above 0.01 mol L⁻¹ was mostly below effective resolution. The precipitation onset was bracketed by only 0.40 and 1.0 mol L⁻¹. No time series established equilibration kinetics or reversibility. No hidden species, activities, charge balance, or microscopic phase composition were observable. Consequently, the evidence supports effective input-output relationships, not a unique thermodynamic mechanism.

6. **Least reliable Q forecasts**

Q01 and Q02 are among the least reliable because they lie in the sparsely observed transition below 0.01 mol L⁻¹ and use 0.020 L, outside the experimentally matched 0.040–0.080 L range. Their dissociation forecasts depend strongly on the conjectured weak-acid transition.

Q06, Q11, and Q12 are also weak, specifically for precipitation, because 0.60 mol L⁻¹ lies inside the unmeasured 0.40–1.0 mol L⁻¹ onset interval. Q11 adds extrapolation to 0.010 L. Q08 is less reliable than Q04 and Q07 because its 0.010 L scale is untested. Q09 and Q10 are structurally uncertain because staging and solvent-first ordering were never tested; their equality was an assumption based on an operational equilibrium endpoint, not an observation. Thus, Q08–Q11 extend beyond the stated scale or path scope even where their central estimates are internally consistent with concentration control.

7. **Limits on generalization**

Interpolation within water, near ambient temperature, at tested volumes and concentrations is better supported than extrapolation. New loadings below 0.01 mol L⁻¹ cross a regime transition; new loadings between 0.40 and 1.0 mol L⁻¹ encounter unresolved precipitation behavior; and concentrations above 1.0 mol L⁻¹ are wholly extrapolative. Dilution predictions assume n/V similarity, which was tested only over a twofold volume change. New paths may introduce transient precipitation or hysteresis that final-state data cannot exclude. Most importantly, this is an anonymous bounded benchmark world. Its empirical coefficients, effective pKa, precipitation onset, and possible background contribution must not be generalized to real named acids, other solvents, other temperatures, or other synthetic worlds without new evidence.
