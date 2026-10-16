# repeat-02/EQ-P03-B-Opaque

Status: completed; source assays 12/12; public note versions 3.

Physical differences below describe the selected actions under matched worlds. They do not establish that an agent proposed or tested an explanation. All notebook versions, including terminal revisions, follow verbatim.

| Assay | End event | Prior note | First later note | Mean gap / assay SD: pH, free acid, precipitate |
| --- | --- | --- | --- | --- |
| 1 | 5 | 1 | 2 | 0.034, 0.704, 0.000 |
| 2 | 10 | 1 | 2 | 3.416, 3.936, 0.000 |
| 3 | 15 | 1 | 2 | 13.337, 3.494, 0.000 |
| 4 | 20 | 1 | 2 | 24.242, 2.121, 0.000 |
| 5 | 25 | 1 | 2 | 20.365, 0.582, 2.553 |
| 6 | 30 | 1 | 2 | 11.934, 0.125, 5.488 |
| 7 | 35 | 2 | 3 | 0.000, 0.000, 10.516 |
| 8 | 40 | 2 | 3 | 0.000, 0.000, 8.413 |
| 9 | 45 | 2 | 3 | 11.934, 0.125, 5.488 |
| 10 | 50 | 2 | 3 | 1.054, 0.003, 11.443 |
| 11 | 55 | 2 | 3 | 0.000, 0.000, 8.413 |
| 12 | 60 | 2 | 3 | 20.365, 0.582, 2.553 |

## Revision 1

Available operation events: 0.

# Hypothesis notebook

## Pre-experiment expectations
H1 [tentative]: In water at fixed temperature, increasing total acid loading should lower pH and reduce the free dissociation fraction; dilution should do the reverse. A simple weak-acid relation may describe the non-precipitating regime.

H2 [tentative]: Precipitation should emerge above a loading/concentration boundary and may cap dissolved neutral acid, causing departures from a single homogeneous weak-acid model. I will test loading and volume independently, include matched-concentration pairs and repeats, and treat differences smaller than stated assay noise as unresolved.

Alternative: observed loading effects could depend on absolute moles rather than concentration; matched-concentration batches should distinguish this within the tested aqueous scope.

## Revision 2

Available operation events: 30.

# Hypothesis notebook

## Pre-experiment expectations
H1 [tentative]: In water at fixed temperature, increasing total acid loading should lower pH and reduce the free dissociation fraction; dilution should do the reverse. A simple weak-acid relation may describe the non-precipitating regime.

H2 [tentative]: Precipitation should emerge above a loading/concentration boundary and may cap dissolved neutral acid, causing departures from a single homogeneous weak-acid model. Absolute-moles and concentration explanations remain alternatives.

## Interim interpretation (through batch 6)
H1 [supported in tested aqueous loading series]: Final assays from 7.5e-6 to 0.20 mol/L show a strong monotonic pH decline (pH_normalized about 0.379 to 0.130) and dissociation-fraction decline (about 0.648 to near zero), events runner-operation-0005 through -0030. The trend is much larger than stated assay noise, though individual near-zero dissociation values are resolution-limited.

H2 [unresolved; narrowed]: No final-assay precipitation signal distinguishable from the 0.006 channel SD through 0.20 mol/L (events -0005, -0010, -0015, -0020, -0025, -0030). A threshold may lie above 0.20 mol/L, or this aqueous slice may not precipitate appreciably. Next: test 0.3–1.0 mol/L and matched concentrations at two absolute mole/volume scales. A reproducible signal materially above assay noise would revive the threshold claim.

## Revision 3

Available operation events: 60.

# Hypothesis notebook

## Final source-stage synthesis
H1 [supported in this bounded aqueous scope]: Nominal total concentration is the main effective control observed. Across 7.5e-6 to 1.0 mol/L, final-assay pH falls monotonically from about 5.31 to about 1.02–1.06, while free dissociation falls from about 0.65 to values indistinguishable from zero at high loading (runner-operation-0005 to -0060). The exact dissociation curve near zero is resolution-limited.

Matched-concentration evidence disfavors a large independent absolute-moles/volume effect: 0.10 mol/L at 0.008 mol/0.08 L and 0.004 mol/0.04 L gave pH 2.093 and 2.111 with negligible precipitation (events -0025, -0060); 0.20 mol/L at the two scales gave pH 1.817 and 1.843 with zero final precipitation (events -0030, -0045). These differences are small relative to stated assay resolution; dissociation differences at 0.20 mol/L remain unresolved rather than evidence of a scale effect.

H2 [supported as an onset, model unresolved]: Final precipitation is negligible through 0.60 mol/L (-0005 to -0030, -0045, -0050), marginal at 0.80 mol/L (0.0136, -0035), and clearly positive and repeatable at 1.0 mol/L (0.0369 and 0.0401, -0040 and -0055). Thus an effective onset lies roughly between 0.6 and 1.0 mol/L under these conditions; data do not identify whether this is a sharp solubility threshold, a smooth bounded response, or another equivalent high-loading nonideality.

A single ideal weak-acid constant is not established over the full range: the paired pH and reported free-fraction responses change too strongly across concentration, and precipitation/nonideality appears at the upper boundary. A local dilute weak-acid interpretation remains plausible, but ionic/activity effects, a concentration-dependent effective constant, and hidden coupled equilibria are observationally equivalent here.

Uncertainty/scope: final-assay SDs are 0.002 in pH_normalized, 0.006 in dissociation, and 0.006 in precipitation. Claims concern water near 298 K, nominal 0.04–0.08 L batches, no added component/catalyst, and instantaneous equilibrated simulator states. Intermediate pH-meter readings are secondary because their uncertainties are larger. Further discrimination would require denser 0.6–1.0 mol/L sampling, replicate dilute points, and an intervention on ionic environment or temperature.

## Sealed K1

## Scope and public background

This is a bounded synthetic weak-acid/precipitation world, not a model of general aqueous chemistry or a named real material. The public definitions are: `pH_normalized = pH/14`; acid dissociation fraction is free deprotonated acid divided by total acid feed; precipitation signal is precipitated acid divided by total acid feed. Hidden species identities and mechanism-to-species mappings are not public. Final-assay stated standard deviations are 0.002 for normalized pH, 0.006 for dissociation fraction, and 0.006 for precipitation signal. The reported equilibrium confidence is an environment diagnostic, not my scientific confidence. No explicit archival relationship or prior fitted law was supplied.

All autonomous batches used water near 298.15 K, without added catalyst or component. Concentrations below are nominal loading divided by prepared liquid volume. A preceding pH-meter measurement removed 0.00003 L before each final assay, a negligible but systematic volume change of at most 0.075%.

## Actual observations

Two public preliminary observations used 6e-7 mol in 0.080 and 0.075 L. They reported normalized pH 0.37684 and 0.38124, dissociation fractions 0.65346 and 0.64569, and zero precipitation. These observations alone did not establish a mechanism.

My 12 final assays gave:

| Batch | Feed / volume | Nominal concentration | pH | Dissociation fraction | Precipitation signal |
|---|---:|---:|---:|---:|---:|
| 1 | 6e-7 mol / 0.080 L | 7.5e-6 mol/L | 5.306 | 0.6484 | 0.0021 |
| 2 | 6e-5 mol / 0.080 L | 7.5e-4 mol/L | 4.007 | 0.0908 | 0 |
| 3 | 6e-4 mol / 0.080 L | 0.0075 mol/L | 3.209 | 0.0166 | 0 |
| 4 | 0.003 mol / 0.080 L | 0.0375 mol/L | 2.586 | 0.0149 | 0.0031 |
| 5 | 0.008 mol / 0.080 L | 0.10 mol/L | 2.093 | 0.0060 | 0.0003 |
| 6 | 0.016 mol / 0.080 L | 0.20 mol/L | 1.817 | 0 | 0 |
| 7 | 0.032 mol / 0.040 L | 0.80 mol/L | 1.200 | 0 | 0.0136 |
| 8 | 0.040 mol / 0.040 L | 1.00 mol/L | 1.023 | 0.0045 | 0.0369 |
| 9 | 0.008 mol / 0.040 L | 0.20 mol/L | 1.843 | 0.0096 | 0 |
| 10 | 0.024 mol / 0.040 L | 0.60 mol/L | 1.326 | 0.0025 | 0.0049 |
| 11 | 0.040 mol / 0.040 L | 1.00 mol/L | 1.060 | 0 | 0.0401 |
| 12 | 0.004 mol / 0.040 L | 0.10 mol/L | 2.111 | 0.0028 | 0.0026 |

Batch 1 is consistent with the public dilute preliminary assays within their stated uncertainties. The final equilibrium residuals were 0–0.0073, while equilibrium-confidence diagnostics ranged approximately from 0.45 to 0.85; neither quantity proves that a proposed chemical mechanism is correct.

## Supported effective relationships

### Loading and pH

Across 7.5e-6–1.0 mol/L, increasing concentration caused a large, monotonic fall in pH from about 5.31 to 1.02–1.06. Over roughly 0.0075–1.0 mol/L, a compact empirical summary is

`pH approximately 1.05 - log10(C / (mol/L))`,

with deviations on the order of a few tenths of a pH unit or less in the observed data. This is an interpolation summary, not a mechanistic law, and it fails toward the extremely dilute boundary where pH approaches about 5.3 rather than continuing along the same line.

### Loading and dissociation

The free deprotonated fraction declined strongly with loading: about 0.65 at 7.5e-6 mol/L, 0.091 at 7.5e-4 mol/L, 0.017 at 0.0075 mol/L, and values near the assay resolution above approximately 0.1 mol/L. Individual high-loading estimates between zero and about 0.01 cannot be ordered confidently because the final-assay standard deviation is 0.006. The defensible conclusion is a strong decline followed by a resolution-limited near-zero regime, not a precisely known high-concentration curve.

### Volume and dilution

Matched-concentration pairs support concentration rather than absolute moles as the main control in the tested volume range:

* At 0.10 mol/L, batches 5 and 12 used 0.080 and 0.040 L and produced pH 2.093 and 2.111. Their dissociation and precipitation differences were both smaller than combined assay uncertainty.
* At 0.20 mol/L, batches 6 and 9 produced pH 1.817 and 1.843 and both had zero final precipitation. Their dissociation estimates, 0 and 0.0096, differ by only about 1.1 combined standard deviations and therefore do not establish a scale effect.

Thus dilution raises pH and increases dissociation primarily by lowering concentration. An independent volume or absolute-mole effect is not resolved between 0.04 and 0.08 L, but effects smaller than the measurement precision remain possible.

### Precipitation

Final precipitation was indistinguishable from zero through 0.60 mol/L. Batch 7 at 0.80 mol/L gave 0.0136, about 2.3 single-measurement standard deviations above zero, so it is suggestive rather than a precisely located boundary. The two independent 1.00 mol/L batches gave 0.0369 and 0.0401; their close agreement and size relative to the 0.006 standard deviation provide clear evidence of a reproducible high-loading precipitation response. A practical effective onset therefore lies between about 0.6 and 1.0 mol/L under the tested conditions, with a mean proxy near 0.039 at 1.0 mol/L.

The experiment does not determine whether there is a sharp thermodynamic solubility threshold. A smooth sigmoid response, a broadened transition, or another high-loading nonideality can explain the sparse 0.6, 0.8, and 1.0 mol/L observations equally well.

## Mechanistic assessment and competing explanations

For a single ideal monoprotic acid with no other proton source, one might expect

`Ka = C*alpha^2/(1-alpha)` and `[H+] approximately C*alpha`.

That complete ideal model is not supported over the full range. For example, batch 3 has `C*alpha` about 1.25e-4 mol/L, which would imply pH about 3.90, whereas the measured pH was 3.21. Similar discrepancies occur at higher loading. Therefore the public pH and dissociation channels cannot be reduced globally to a single ideal-acid mass balance using the nominal feed concentration.

Several explanations remain observationally equivalent:

1. a concentration-dependent effective dissociation constant caused by activity coefficients or ionic-strength effects;
2. background or support-electrolyte acid/base contributions to pH;
3. hidden coupled protonation equilibria or ion pairing;
4. a latent benchmark mapping in which pH and free deprotonated fraction are related but not constrained by the simplest one-acid electroneutrality equation;
5. at high loading, removal of some acid into a precipitated pool plus additional nonideality.

The data support an effective concentration-response description but do not identify among these microscopic explanations. At 1.0 mol/L, dissociation plus precipitation accounts for only about 4% of total feed; without public species mapping, the remaining fraction cannot safely be assigned to a unique dissolved species.

## Uncertainty, limitations, and supported domain

The strongest conclusions are the monotonic pH decrease, the large dissociation decrease, concentration dominance over the tested twofold volume change, and reproducible precipitation near 1.0 mol/L. Near-zero dissociation and precipitation values should not be interpreted below channel resolution. Only the 1.0 mol/L condition was exactly replicated; the matched 0.10 and 0.20 mol/L pairs also serve as limited scale checks. Intermediate pH-meter observations had larger uncertainties and were treated as secondary evidence.

The account is supported only for water near 298 K, nominal volumes of 0.04–0.08 L, loading from 7.5e-6 to 1.0 mol/L, no added catalyst/component, and the simulator's instantaneous assay state. Temperature, solvent identity, electrolyte formulation, equilibration time, hysteresis, and precipitate reversibility were not varied. Denser replicated sampling between 0.6 and 1.0 mol/L could distinguish a sharp threshold from a smooth onset; controlled changes in ionic environment or temperature would be required to discriminate activity effects, background acidity, and coupled equilibria.

## Sealed Q

{
  "predictions": [
    {
      "query_id": "Q01",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.262,
          "lower80": 0.253,
          "upper80": 0.271
        },
        "acid_dissociation_fraction": {
          "estimate": 0.044,
          "lower80": 0.025,
          "upper80": 0.068
        },
        "precipitation_signal": {
          "estimate": 0.001,
          "lower80": 0,
          "upper80": 0.012
        }
      },
      "rationale": "At 0.002 mol/L, log-concentration interpolation between observed batches 2 and 3 predicts pH about 3.67 and a rapidly declining but still measurable dissociation fraction. All observed concentrations below 0.6 mol/L had precipitation consistent with zero. The 0.02 L scale is below the studied 0.04–0.08 L range, so intervals include scale uncertainty."
    },
    {
      "query_id": "Q02",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.235,
          "lower80": 0.228,
          "upper80": 0.242
        },
        "acid_dissociation_fraction": {
          "estimate": 0.02,
          "lower80": 0.007,
          "upper80": 0.035
        },
        "precipitation_signal": {
          "estimate": 0.001,
          "lower80": 0,
          "upper80": 0.012
        }
      },
      "rationale": "The 0.006 mol/L concentration lies close to batch 3 at 0.0075 mol/L, where normalized pH was 0.2292 and dissociation was 0.0166. A slightly higher pH and dissociation are expected after dilution. Precipitation should remain negligible."
    },
    {
      "query_id": "Q03",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.202,
          "lower80": 0.196,
          "upper80": 0.208
        },
        "acid_dissociation_fraction": {
          "estimate": 0.015,
          "lower80": 0.004,
          "upper80": 0.028
        },
        "precipitation_signal": {
          "estimate": 0.001,
          "lower80": 0,
          "upper80": 0.012
        }
      },
      "rationale": "At 0.02 mol/L, interpolation between batches 3 and 4 predicts pH about 2.83. Dissociation changed only modestly between those neighboring observations, but its exact value is uncertain because the channel noise is substantial relative to the small fraction. No precipitation is expected."
    },
    {
      "query_id": "Q04",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.168,
          "lower80": 0.162,
          "upper80": 0.174
        },
        "acid_dissociation_fraction": {
          "estimate": 0.008,
          "lower80": 0,
          "upper80": 0.019
        },
        "precipitation_signal": {
          "estimate": 0.001,
          "lower80": 0,
          "upper80": 0.012
        }
      },
      "rationale": "The 0.06 mol/L condition lies between observed 0.0375 and 0.10 mol/L batches. Log-concentration interpolation gives pH about 2.35, while dissociation should be small and close to measurement resolution. This loading is far below the observed precipitation onset."
    },
    {
      "query_id": "Q05",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.131,
          "lower80": 0.125,
          "upper80": 0.137
        },
        "acid_dissociation_fraction": {
          "estimate": 0.005,
          "lower80": 0,
          "upper80": 0.016
        },
        "precipitation_signal": {
          "estimate": 0.001,
          "lower80": 0,
          "upper80": 0.013
        }
      },
      "rationale": "The concentration exactly matches batches 6 and 9, whose normalized pH values were 0.1298 and 0.1317 and whose final precipitation signals were zero. Their dissociation estimates bracketed zero and 0.0096. The point estimate averages that resolution-limited behavior; the smaller 0.02 L scale broadens uncertainty."
    },
    {
      "query_id": "Q06",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.095,
          "lower80": 0.089,
          "upper80": 0.101
        },
        "acid_dissociation_fraction": {
          "estimate": 0.003,
          "lower80": 0,
          "upper80": 0.013
        },
        "precipitation_signal": {
          "estimate": 0.003,
          "lower80": 0,
          "upper80": 0.017
        }
      },
      "rationale": "Batch 10 directly observed 0.6 mol/L at normalized pH 0.0947, dissociation 0.0025, and precipitation 0.0049. Because that precipitation value was below one assay standard deviation, the underlying signal remains consistent with zero. The 0.02 L volume introduces modest scale-extrapolation uncertainty."
    },
    {
      "query_id": "Q07",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.168,
          "lower80": 0.162,
          "upper80": 0.174
        },
        "acid_dissociation_fraction": {
          "estimate": 0.008,
          "lower80": 0,
          "upper80": 0.019
        },
        "precipitation_signal": {
          "estimate": 0.001,
          "lower80": 0,
          "upper80": 0.012
        }
      },
      "rationale": "This 0.06 mol/L batch is compositionally equivalent to Q04 but uses 0.04 L, within the studied volume range. Matched 0.10 and 0.20 mol/L observations showed no resolved independent volume effect, so concentration-based interpolation is used with slightly less scale uncertainty."
    },
    {
      "query_id": "Q08",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.168,
          "lower80": 0.159,
          "upper80": 0.177
        },
        "acid_dissociation_fraction": {
          "estimate": 0.008,
          "lower80": 0,
          "upper80": 0.024
        },
        "precipitation_signal": {
          "estimate": 0.001,
          "lower80": 0,
          "upper80": 0.016
        }
      },
      "rationale": "The same 0.06 mol/L concentration should give essentially the same central response as Q04 and Q07 if concentration controls equilibrium. However, 0.01 L is fourfold below the smallest experimentally tested volume, so the intervals allow an unresolved absolute-scale effect."
    },
    {
      "query_id": "Q09",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.131,
          "lower80": 0.123,
          "upper80": 0.139
        },
        "acid_dissociation_fraction": {
          "estimate": 0.005,
          "lower80": 0,
          "upper80": 0.019
        },
        "precipitation_signal": {
          "estimate": 0.001,
          "lower80": 0,
          "upper80": 0.016
        }
      },
      "rationale": "Its final composition is 0.20 mol/L, matching batches 6 and 9 and Q05. A true equilibrium state should depend mainly on final concentration rather than staged addition, so the same central prediction is used. Addition-path dependence was not experimentally tested, and the 0.02 L scale is extrapolative, so intervals are wider."
    },
    {
      "query_id": "Q10",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.131,
          "lower80": 0.123,
          "upper80": 0.139
        },
        "acid_dissociation_fraction": {
          "estimate": 0.005,
          "lower80": 0,
          "upper80": 0.019
        },
        "precipitation_signal": {
          "estimate": 0.001,
          "lower80": 0,
          "upper80": 0.016
        }
      },
      "rationale": "Q10 has the same final water, reagent, volume, and concentration as Q09, differing only in addition order. With no observed precipitation at 0.20 mol/L and no evidence for hysteresis, path independence is the best prediction, while the wider intervals acknowledge that path effects were untested."
    },
    {
      "query_id": "Q11",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.095,
          "lower80": 0.085,
          "upper80": 0.104
        },
        "acid_dissociation_fraction": {
          "estimate": 0.003,
          "lower80": 0,
          "upper80": 0.02
        },
        "precipitation_signal": {
          "estimate": 0.003,
          "lower80": 0,
          "upper80": 0.022
        }
      },
      "rationale": "The concentration matches observed batch 10, but the 0.01 L volume is well below the tested range. The central values therefore follow the 0.6 mol/L observation, while substantially broader intervals cover possible scale effects. Precipitation remains more likely absent or very small than clearly positive because robust onset was seen only near 1.0 mol/L."
    },
    {
      "query_id": "Q12",
      "metrics": {
        "pH_normalized": {
          "estimate": 0.095,
          "lower80": 0.09,
          "upper80": 0.1
        },
        "acid_dissociation_fraction": {
          "estimate": 0.003,
          "lower80": 0,
          "upper80": 0.012
        },
        "precipitation_signal": {
          "estimate": 0.003,
          "lower80": 0,
          "upper80": 0.016
        }
      },
      "rationale": "This exactly matches batch 10 in nominal concentration and 0.04 L volume, so its final-assay values provide the closest anchor. The precipitation interval includes zero because the observed 0.0049 signal was smaller than the stated 0.006 assay standard deviation."
    }
  ],
  "rationale": "Predictions use nominal concentration as the principal effective variable, consistent with the sealed account's matched-volume comparisons. Normalized pH was interpolated approximately linearly against log concentration. Dissociation was modeled as a decreasing, near-zero high-loading response without imposing the rejected global ideal-acid mass balance. Precipitation was treated as negligible through 0.6 mol/L. Intervals combine stated final-assay noise with interpolation, sparse-replication, small-volume extrapolation, and untested path-dependence uncertainty; bounds respect the public 0–1 metric ranges."
}

## Sealed K2

## 1. Supported, contradicted, and untested relationships

**Supported within the studied aqueous world:**

- Nominal concentration is the dominant observed control. From 7.5e-6 to 1.0 mol/L, increasing concentration monotonically lowered pH from about 5.31 to 1.02–1.06 and reduced the measured free deprotonated fraction from about 0.65 to values near assay resolution.
- Dilution therefore raises pH and generally increases dissociation within this range.
- Matched-concentration comparisons at 0.10 and 0.20 mol/L found no resolved independent effect of changing volume from 0.08 to 0.04 L. This supports concentration control over a large absolute-moles effect, but it does not prove exact scale invariance.
- Precipitation was indistinguishable from zero through 0.60 mol/L, suggestive at 0.80 mol/L, and clearly positive and reproducible at 1.0 mol/L.

**Contradicted or unsupported:**

- A single global ideal-monoprotic-acid model is contradicted as a complete account. The measured pH and dissociation fractions do not satisfy `[H+] = C*alpha` across the series. For example, batch 3 had `C*alpha` about 1.25e-4 mol/L, corresponding to pH about 3.90 under that model, but observed pH was 3.21.
- The evidence does not support assigning every near-zero high-loading dissociation estimate a meaningful numerical order. Values around 0–0.01 are comparable to the 0.006 assay standard deviation.
- A precise precipitation threshold was not established. The data support a high-loading onset region, not a unique solubility constant.

**Untested:**

- Temperature, nonaqueous solvents, added components, catalysts, ionic environment, waiting time, reversibility, and precipitation hysteresis were not varied.
- Addition-order effects were not tested in K1.
- Volumes below 0.04 L were not tested.
- The response above 1.0 mol/L and between the sparse 0.6, 0.8, and 1.0 mol/L points is unknown.

## 2. Observations that changed the account

There were actual observations that changed the account.

- The initial expectation that dilution would raise pH and dissociation was supported by the concentration series.
- The expectation that a simple weak-acid relationship might describe the nonprecipitating regime was narrowed substantially. Batch 3 and subsequent batches showed that pH and reported free dissociation could not be joined by the simplest one-acid mass balance over the full range.
- Early batches through 0.20 mol/L showed no resolved precipitation, temporarily weakening the initial threshold conjecture. Batch 7 at 0.80 mol/L then produced a marginal signal of 0.0136. Batches 8 and 11 at 1.0 mol/L produced 0.0369 and 0.0401, converting the precipitation claim from speculative to supported at the upper boundary.
- Matched pairs changed the interpretation from a generic loading effect to a primarily concentration-based effect: batches 5 and 12 agreed at 0.10 mol/L despite different amounts and volumes, and batches 6 and 9 agreed in pH and precipitation at 0.20 mol/L.

## 3. Competing explanations

Some alternatives are partly distinguishable:

- A large absolute-moles effect is disfavored relative to concentration control by the matched 0.10 and 0.20 mol/L pairs.
- A global ideal single-acid model is disfavored by the incompatibility between pH and `C*alpha`.
- A genuinely positive precipitation response at 1.0 mol/L is favored over pure measurement noise because it was independently repeated.

Important alternatives remain unresolved:

- Concentration-dependent activity coefficients, background electrolyte acidity, ion pairing, hidden coupled protonation equilibria, and a benchmark-specific latent mapping could all produce the observed separation between pH and free dissociation.
- A sharp solubility threshold, a smooth sigmoid precipitation response, and a broadened heterogeneous transition all remain compatible with the sparse high-loading data.
- Small scale effects remain possible because the matched-volume differences were below measurement resolution rather than exactly proven absent.
- Path independence is plausible for an equilibrium endpoint but was not observed directly.

## 4. Best next legal experiment

I would independently repeat batch 7: add 0.040 L water and 0.032 mol reagent, terminate, and measure with the final assay. This is a legal 0.80 mol/L experiment and directly targets the weakest link in the precipitation-onset inference.

Possible outcomes would have distinct interpretations:

- A precipitation signal near zero would imply that the original 0.0136 value was likely noise or an unstable boundary observation, narrowing robust onset to between 0.8 and 1.0 mol/L.
- A repeated signal near 0.014 would establish that precipitation is already present at 0.8 mol/L and support a gradual onset between 0.6 and 1.0 mol/L.
- A signal near the 1.0 mol/L level, around 0.04, would favor a steeper transition beginning below 0.8 mol/L and suggest that the original batch 7 value was a low fluctuation.
- The accompanying pH and dissociation values would also test reproducibility at the only marginal-onset concentration.

One assay would still not identify a complete precipitation curve, but it would resolve whether the current 0.8 mol/L evidence is reproducible.

## 5. Limits of the evidence

The evidence consists of 12 final assays, one exact high-loading replicate, two matched-concentration scale comparisons, and secondary pH-meter measurements. The final-assay standard deviations are 0.002 in normalized pH, 0.006 in dissociation, and 0.006 in precipitation. Consequently, high-loading dissociation and low precipitation values are resolution-limited.

The design is sparse over several orders of magnitude and especially sparse around precipitation onset. Only water near 298 K, 0.04–0.08 L, no catalyst/component, and immediate simulator endpoints were studied. Hidden species mapping prevents a unique material balance or microscopic mechanism. Equilibrium confidence is only an environment diagnostic and cannot be used as epistemic confidence. These limits make the effective concentration-response relationships stronger than any mechanistic interpretation.

## 6. Least reliable Q forecasts

The least reliable forecasts are Q08 and Q11 because their 0.01 L volume is fourfold below the smallest studied volume. Their central estimates assume scale invariance beyond the demonstrated 0.04–0.08 L range.

Q09 and Q10 are also weak because they test staged versus solvent-first paths, while K1 contained no path-control experiment. Giving them identical central estimates was an equilibrium-based inference, not an observed fact.

Q01 is uncertain because both its 0.02 L scale and its dissociation estimate require interpolation across a broad, nonlinear dilute-region gap. Q06 also extrapolates the observed 0.60 mol/L response from 0.04 to 0.02 L.

The precipitation forecasts at 0.60 mol/L should not be read as evidence for a true nonzero signal. Their small positive point estimates reflected bounded observation noise and the single batch-10 value of 0.0049, which was below one assay standard deviation. Q12 is comparatively well anchored because it reproduces batch 10's nominal concentration and volume.

## 7. Limits on generalization

Generalization to new loading is limited by interpolation gaps and the absence of observations above 1.0 mol/L. Generalization to new dilution or volume is limited because scale was checked only between 0.04 and 0.08 L at two concentrations. Generalization to new paths is limited because no K1 experiment changed addition order, equilibration time, or precipitation history. Generalization to other worlds is especially limited: the system is an anonymous bounded synthetic benchmark, and neither real-material identity nor transferable microscopic parameters are available.

Accordingly, the most defensible transferable statement is qualitative and local: in this world and tested aqueous domain, concentration strongly lowers pH and free dissociation, while a reproducible precipitation proxy emerges near the upper concentration boundary. Numerical equations, scale invariance, path independence, and microscopic mechanisms should not be exported beyond that scope.
