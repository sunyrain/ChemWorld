# repeat-01/EC-W05-B12-discovery-E-Opaque

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-01\EC-W05-B12-discovery-E-Opaque\participant\discovery-E-Opaque

## 同期笔记

### v1 · 公开事件 0

# Pre-experiment hypotheses

H1 [tentative] — Product formation is polarity-selective: one potential sign will enable target conversion while the opposite sign gives little target or more degradation. Test with matched ± potential batches.

H2 [tentative] — Conversion should rise with delivered charge/time and current cap until reagent depletion, while selectivity and energy efficiency may decline at excessive magnitude or duration. Test magnitude, current-cap, and duration contrasts at fixed loading.

H3 [tentative] — Solvent and electrolyte identities independently modulate transport/ohmic efficiency and possibly the preferred potential window. Screen all four levels while retaining interpretable matched controls.

Initial design decision: use 0.020 mol in 0.040 L as a common loading for most batches, with UV–vis snapshots to test kinetics; include polarity, time, magnitude, current-cap, solvent, electrolyte, and at least one repeat. Numerical differences will be treated cautiously given stated assay noise.

### v2 · 公开事件 28

# Working hypotheses after batches 1–4

H1 [supported for efficiency; target direction unresolved] — Potential sign strongly changes the efficiency suite in solvent-S0/electrolyte-E0: +1 V gives near-unity faradaic/transport/energy efficiencies, whereas −1 V gives roughly 0.25–0.43 energy/faradaic/transport efficiency (events runner-operation-0005, -0012, -0019, -0026 and final assays -0007, -0014, -0021, -0028). Yet target yield is at/near zero for both signs, so polarity-selective target formation is not established.

H2 [revised] — The first tests were severely charge-limited rather than informative about attainable conversion: 20 mA for 60–600 s corresponds to only 1.2–12 C relative to 0.020 mol reagent. The absence of meaningful yield at these settings does not reject electroconversion. Next tests raise current cap and duration by orders of magnitude and compare charge levels.

H3 [unresolved] — Solvent/electrolyte effects remain untested. Material screening will follow identification of an active polarity/time regime.

Prediction before batches 5–8: if charge limitation dominates, high-cap long electrolysis will materially increase conversion/yield; +1 V should remain more energy-efficient, but either sign may be target-forming. A very long run may expose selectivity/degradation loss.

### v3 · 公开事件 56

# Working hypotheses after batches 1–8

H1 [supported, sign-dependent trade-off in S0/E0] — Positive +1 V produces much higher efficiency/selectivity but much lower conversion than −1 V at the same nominal cap and time. At 500 mA, 3600 s, +1 V gave conversion 0.030, selectivity 0.983 and near-unity efficiencies (event runner-operation-0056), versus −1 V conversion 0.092, selectivity 0.655 and energy/faradaic/transport efficiencies near 0.14/0.22/0.19 (event -0042). Thus current_mA is indeed only a cap; delivered reaction rate depends strongly on potential sign.

H2 [supported in tested negative regime] — At −1 V, 500 mA cap, conversion is approximately proportional to time from 1800–7200 s: about 0.049, 0.092, 0.181 (events -0035, -0042, -0049). Selectivity remains near 0.65, so yield scales correspondingly. No saturation/degradation downturn is visible yet. Prediction: doubling duration beyond 7200 s, if allowed, would roughly double conversion until depletion; increasing negative magnitude may raise delivered rate.

H3 [unresolved] — Material effects remain a major gap. Final batches will combine a ±2 V magnitude contrast in S0/E0 with two alternative solvent/electrolyte combinations at −2 V. Because each alternative is unreplicated and jointly changes solvent/electrolyte, any material attribution will remain provisional.

Decision: optimize explanatory range rather than leaderboard score; retain +1 V batch 8 as the current high-score/efficiency candidate but seek higher negative-magnitude yield.

### v4 · 公开事件 84

# Final source-stage interpretation (12 batches)

H1 [supported within tested loading/material] — Response to potential is asymmetric and non-monotone. In S0/E0 at 500 mA and 7200 s, −1 V gives conversion 0.181, selectivity 0.649 and yield 0.119 (runner-operation-0049); −2 V does not improve conversion (0.169) and lowers selectivity/yield to 0.511/0.106 (runner-operation-0063). At the positive sign, +1 V at 3600 s has low conversion but excellent selectivity and efficiency (runner-operation-0056), whereas +2 V at 7200 s collapses selectivity, faradaic/transport efficiency, and yield (runner-operation-0070). A simple monotone |V| law is rejected; sign-specific potential windows or competing pathways are required.

H2 [supported locally, extrapolation limited] — At −1 V/S0/E0/500 mA, conversion is approximately linear with duration from 1800–7200 s (runner-operation-0035, -0042, -0049), with selectivity near 0.65. The near-zero 20 mA results are consistent with charge/current limitation, but because delivered current is unobserved, a quantitative Faraday-law coefficient cannot be identified from the cap alone. Saturation beyond conversion 0.18 was not tested.

H3 [supported that material matters; components unresolved] — Joint solvent/electrolyte changes substantially alter rate, pH, precipitation and efficiencies at −2 V/7200 s. S1/E2 increases conversion to 0.223 and nearly removes the precipitation signal while lowering pH_normalized to 0.155 (runner-operation-0077), whereas S3/E3 gives conversion 0.050, pH 0.284 and zero precipitation signal (runner-operation-0084), compared with S0/E0 conversion 0.169 and precipitation near 1 (runner-operation-0063). Solvent and electrolyte effects are confounded and unreplicated, so separate causal coefficients are unresolved.

Predictive account: conversion rate is a function of signed potential, current cap, and material-dependent transport; target yield is conversion × a sign/magnitude/material-dependent selectivity, while energy efficiency additionally penalizes large magnitude and inefficient polarity. Duration acts approximately linearly only in the demonstrated low-conversion −1 V regime. A +1 V window in S0/E0 is the best tested balanced-efficiency operating region; −1 V favors throughput/yield.

Recommendation decision: select batch 8 for the secondary balanced score because it achieved the campaign-high score with near-unity selectivity and efficiency, despite low conversion. Batch 7 is preferable only if target yield/throughput is prioritized over the stated balanced metric.

## 实际批次及公开测量

### 批次 1 · 终点事件 7

```json
{
  "ordinal": 1,
  "lifecycle_index": 1,
  "end_step": 7,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.04
    },
    {
      "current_mA": 20,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 60,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "metrics": {
    "cost": 0.28260481357574463,
    "electrochemical_conversion": 0.00832182727754116,
    "electrochemical_selectivity": 0.9983465671539307,
    "energy_efficiency": 0.987197756767273,
    "faradaic_efficiency": 1.0,
    "ohmic_efficiency": 0.9847304821014404,
    "pH_normalized": 0.23308512568473816,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.9854740500450134
  }
}
```

### 批次 2 · 终点事件 14

```json
{
  "ordinal": 2,
  "lifecycle_index": 2,
  "end_step": 14,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.04
    },
    {
      "current_mA": 20,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1
    },
    {
      "duration_s": 60,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "metrics": {
    "cost": 0.28260481357574463,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.6399977803230286,
    "energy_efficiency": 0.2799854278564453,
    "faradaic_efficiency": 0.4022141396999359,
    "ohmic_efficiency": 0.9935683012008667,
    "pH_normalized": 0.2303897738456726,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.14100505411624908,
    "selective_product_yield": 0.009058722294867039,
    "transport_efficiency": 0.4284709692001343
  }
}
```

### 批次 3 · 终点事件 21

```json
{
  "ordinal": 3,
  "lifecycle_index": 3,
  "end_step": 21,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.04
    },
    {
      "current_mA": 20,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 600,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "metrics": {
    "cost": 0.2826479971408844,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.9747204780578613,
    "energy_efficiency": 0.9757068753242493,
    "faradaic_efficiency": 0.9619938731193542,
    "ohmic_efficiency": 0.9803419709205627,
    "pH_normalized": 0.231104776263237,
    "precipitation_signal": 0.9869203567504883,
    "safety_risk": 0.072194404900074,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.9785507321357727
  }
}
```

### 批次 4 · 终点事件 28

```json
{
  "ordinal": 4,
  "lifecycle_index": 4,
  "end_step": 28,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.04
    },
    {
      "current_mA": 20,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1
    },
    {
      "duration_s": 600,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "metrics": {
    "cost": 0.2826479971408844,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.6012951731681824,
    "energy_efficiency": 0.2538937032222748,
    "faradaic_efficiency": 0.4306136965751648,
    "ohmic_efficiency": 0.9925001263618469,
    "pH_normalized": 0.23041419684886932,
    "precipitation_signal": 0.9876685738563538,
    "safety_risk": 0.072194404900074,
    "score": 0.023647649213671684,
    "selective_product_yield": 0.001577888149768114,
    "transport_efficiency": 0.39912617206573486
  }
}
```

### 批次 5 · 终点事件 35

```json
{
  "ordinal": 5,
  "lifecycle_index": 5,
  "end_step": 35,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.04
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1
    },
    {
      "duration_s": 1800,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "metrics": {
    "cost": 0.28619998693466187,
    "electrochemical_conversion": 0.0492141917347908,
    "electrochemical_selectivity": 0.6576117873191833,
    "energy_efficiency": 0.11995066702365875,
    "faradaic_efficiency": 0.20727604627609253,
    "ohmic_efficiency": 0.844822883605957,
    "pH_normalized": 0.23537498712539673,
    "precipitation_signal": 0.9869949817657471,
    "safety_risk": 0.072194404900074,
    "score": 0.24517136812210083,
    "selective_product_yield": 0.03826657682657242,
    "transport_efficiency": 0.19676658511161804
  }
}
```

### 批次 6 · 终点事件 42

```json
{
  "ordinal": 6,
  "lifecycle_index": 6,
  "end_step": 42,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.04
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1
    },
    {
      "duration_s": 3600,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "metrics": {
    "cost": 0.2897999882698059,
    "electrochemical_conversion": 0.09158703684806824,
    "electrochemical_selectivity": 0.6554183959960938,
    "energy_efficiency": 0.13916777074337006,
    "faradaic_efficiency": 0.21581701934337616,
    "ohmic_efficiency": 0.8466796278953552,
    "pH_normalized": 0.2320990413427353,
    "precipitation_signal": 0.9976252913475037,
    "safety_risk": 0.072194404900074,
    "score": 0.26166510581970215,
    "selective_product_yield": 0.06857564300298691,
    "transport_efficiency": 0.19113369286060333
  }
}
```

### 批次 7 · 终点事件 49

```json
{
  "ordinal": 7,
  "lifecycle_index": 7,
  "end_step": 49,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.04
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1
    },
    {
      "duration_s": 7200,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "metrics": {
    "cost": 0.296999990940094,
    "electrochemical_conversion": 0.18122616410255432,
    "electrochemical_selectivity": 0.6490082144737244,
    "energy_efficiency": 0.13805976510047913,
    "faradaic_efficiency": 0.18534335494041443,
    "ohmic_efficiency": 0.8782411813735962,
    "pH_normalized": 0.23111364245414734,
    "precipitation_signal": 0.9826673865318298,
    "safety_risk": 0.072194404900074,
    "score": 0.2831258475780487,
    "selective_product_yield": 0.11856052279472351,
    "transport_efficiency": 0.1887437105178833
  }
}
```

### 批次 8 · 终点事件 56

```json
{
  "ordinal": 8,
  "lifecycle_index": 8,
  "end_step": 56,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.04
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 3600,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "metrics": {
    "cost": 0.28315263986587524,
    "electrochemical_conversion": 0.030430041253566742,
    "electrochemical_selectivity": 0.9826774597167969,
    "energy_efficiency": 0.9719752669334412,
    "faradaic_efficiency": 0.9980514645576477,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.229416161775589,
    "precipitation_signal": 0.995540201663971,
    "safety_risk": 0.072194404900074,
    "score": 0.42545440793037415,
    "selective_product_yield": 0.014195503666996956,
    "transport_efficiency": 0.9915561079978943
  }
}
```

### 批次 9 · 终点事件 63

```json
{
  "ordinal": 9,
  "lifecycle_index": 9,
  "end_step": 63,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.04
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -2
    },
    {
      "duration_s": 7200,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "metrics": {
    "cost": 0.31139999628067017,
    "electrochemical_conversion": 0.16897141933441162,
    "electrochemical_selectivity": 0.5108161568641663,
    "energy_efficiency": 0.08656676858663559,
    "faradaic_efficiency": 0.1745322197675705,
    "ohmic_efficiency": 0.9530985951423645,
    "pH_normalized": 0.23142993450164795,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.25505536794662476,
    "selective_product_yield": 0.10607556998729706,
    "transport_efficiency": 0.19536349177360535
  }
}
```

### 批次 10 · 终点事件 70

```json
{
  "ordinal": 10,
  "lifecycle_index": 10,
  "end_step": 70,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.04
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 2
    },
    {
      "duration_s": 7200,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "metrics": {
    "cost": 0.31139999628067017,
    "electrochemical_conversion": 0.015369986183941364,
    "electrochemical_selectivity": 0.019033947959542274,
    "energy_efficiency": 0.014645654708147049,
    "faradaic_efficiency": 0.009028017520904541,
    "ohmic_efficiency": 0.9125494956970215,
    "pH_normalized": 0.2291157990694046,
    "precipitation_signal": 0.9925763010978699,
    "safety_risk": 0.072194404900074,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.010377603583037853
  }
}
```

### 批次 11 · 终点事件 77

```json
{
  "ordinal": 11,
  "lifecycle_index": 11,
  "end_step": 77,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -2
    },
    {
      "duration_s": 7200,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "metrics": {
    "cost": 0.32739999890327454,
    "electrochemical_conversion": 0.22345860302448273,
    "electrochemical_selectivity": 0.4497390389442444,
    "energy_efficiency": 0.09987672418355942,
    "faradaic_efficiency": 0.2273438423871994,
    "ohmic_efficiency": 0.8409258723258972,
    "pH_normalized": 0.15479108691215515,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.09559440612792969,
    "score": 0.2521511912345886,
    "selective_product_yield": 0.09785080701112747,
    "transport_efficiency": 0.23452378809452057
  }
}
```

### 批次 12 · 终点事件 84

```json
{
  "ordinal": 12,
  "lifecycle_index": 12,
  "end_step": 84,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 3,
      "volume_L": 0.04
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": -2
    },
    {
      "duration_s": 7200,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "metrics": {
    "cost": 0.3370000123977661,
    "electrochemical_conversion": 0.050143051892519,
    "electrochemical_selectivity": 0.3659329414367676,
    "energy_efficiency": 0.015696262940764427,
    "faradaic_efficiency": 0.03723444417119026,
    "ohmic_efficiency": 0.934518575668335,
    "pH_normalized": 0.28434595465660095,
    "precipitation_signal": 0.0,
    "safety_risk": 0.12619440257549286,
    "score": 0.15830275416374207,
    "selective_product_yield": 0.03656168654561043,
    "transport_efficiency": 0.058459389954805374
  }
}
```

## K1 封存报告

Mechanism report

1. Empirical picture

The system is governed by a strong interaction among signed potential, the current cap, electrolysis duration, solvent/electrolyte identity, and competing selectivity/efficiency pathways. Potential magnitude alone is not an adequate reaction coordinate: +1 V, −1 V, +2 V, and −2 V produced qualitatively different regimes.

All batches used 0.020 mol limiting reagent in 0.040 L solvent. Batches 1–10 used solvent-S0/electrolyte-E0. The principal observations were:

• Batch 1 (+1 V, 20 mA, 60 s): conversion 0.0083, selectivity 0.9983, reported selective-product yield 0, and approximately 0.99 efficiencies.
• Batch 2 (−1 V, 20 mA, 60 s): conversion was clipped at 0, selectivity 0.6400, yield 0.0091, energy efficiency 0.2800, faradaic efficiency 0.4022, transport efficiency 0.4285, and ohmic efficiency 0.9936.
• Batch 3 (+1 V, 20 mA, 600 s): conversion and yield were 0; selectivity was 0.9747, with high efficiencies.
• Batch 4 (−1 V, 20 mA, 600 s): conversion was clipped at 0, yield 0.0016, selectivity 0.6013, and energy/faradaic/transport efficiencies were 0.2539/0.4306/0.3991.
• Batches 5–7 used −1 V and a 500 mA cap for 1800, 3600, and 7200 s. Conversion increased from 0.0492 to 0.0916 to 0.1812, while selectivity stayed approximately constant at 0.6576, 0.6554, and 0.6490. Selective-product yield rose from 0.0383 to 0.0686 to 0.1186. Faradaic and transport efficiencies remained low, near 0.19–0.22, while ohmic efficiency was 0.845–0.878.
• Batch 8 (+1 V, 500 mA, 3600 s): conversion was only 0.0304 and yield 0.0142, but selectivity was 0.9827 and energy/faradaic/transport/ohmic efficiencies were 0.9720/0.9981/0.9916/1.0000. This was the highest balanced score, 0.4255.
• Batch 9 (−2 V, 500 mA, 7200 s): conversion 0.1690, selectivity 0.5108, yield 0.1061, and energy/faradaic/transport efficiencies 0.0866/0.1745/0.1954. Thus making the negative potential more extreme did not improve conversion over batch 7 and reduced selectivity.
• Batch 10 (+2 V, 500 mA, 7200 s): conversion 0.0154, selectivity 0.0190, yield 0, faradaic efficiency 0.0090, and transport efficiency 0.0104. The beneficial +1 V regime therefore collapses at +2 V.
• Batch 11 used solvent-S1/electrolyte-E2 at −2 V, 500 mA, 7200 s. It gave conversion 0.2235, selectivity 0.4497, yield 0.0979, pH_normalized 0.1548, precipitation signal 0.0052, faradaic efficiency 0.2273, transport efficiency 0.2345, and ohmic efficiency 0.8409.
• Batch 12 used solvent-S3/electrolyte-E3 under the same electrical conditions. It gave conversion 0.0501, selectivity 0.3659, yield 0.0366, pH_normalized 0.2843, precipitation signal 0, faradaic efficiency 0.0372, transport efficiency 0.0585, and ohmic efficiency 0.9345.

2. Proposed process model

A useful phenomenological decomposition is

r_target = r_electrolysis(V, I_cap, S, E, state) × s(V, S, E, state),

dC/dt ≈ k(V, I_cap, S, E, state) × (1 − C),

Y_target ≈ C × s + measurement/process discrepancy,

where C is conversion, s is pathway selectivity, S and E denote solvent and electrolyte, and “state” may include concentration, electrode condition, pH, precipitation, and accumulated products. In the low-conversion −1 V/S0/E0 regime, (1 − C) is close to one, so the model reduces locally to C ≈ k t.

For batches 5–7, C/t was about 2.5–2.7 × 10⁻⁵ s⁻¹. This local proportionality explains the near-doubling of conversion when time doubled. It is an interpolation over 1800–7200 s and C ≤ 0.18, not evidence that conversion would grow linearly indefinitely. Reagent depletion, passivation, mass transport, or degradation should eventually bend the curve.

The nominal current is best interpreted as a cap rather than measured delivered current. The data do not support calculating charge from I_cap × t as though 500 mA necessarily flowed continuously. Batch 8, for example, had much lower conversion than batch 6 despite the same current cap and duration. A plausible effective-current relation is

I_eff = I_cap × g(V,S,E,state),

with 0 ≤ g ≤ 1, followed by a Faraday-like rate proportional to I_eff times a pathway-specific faradaic utilization. Neither I_eff nor electron stoichiometry was measured, so they cannot be separately identified.

3. Signed-potential mechanism

The potential dependence appears to contain distinct electrochemical windows rather than a monotone dependence on |V|.

At +1 V, the system occupies a highly selective, highly efficient but slow-conversion window. This could correspond to a target-forming electrode process with little parasitic current but limited kinetic driving force or limited current delivery. At −1 V, target formation is faster, but only about 65% selective and is accompanied by poor faradaic and transport metrics. A plausible interpretation is that the negative-potential route activates both target formation and a parallel consumption pathway:

R + e⁻ → P_target,
R + e⁻ → P_side,

with the target branch fraction near 0.65 in S0/E0 over the tested duration range.

Moving from −1 to −2 V does not raise conversion at 7200 s and lowers selectivity from 0.649 to 0.511. This is consistent with a competing reaction, electrode passivation, transport limitation, or wasted charge becoming more important at excessive negative driving force.

The +2 V result is more dramatic: selectivity and faradaic/transport efficiency all approach zero. One possible mechanism is activation of a destructive or non-target oxidation pathway, such as

P_target or R → degradation/impurity products,

or passivation that suppresses productive transport. However, no byproduct identities or degradation products were measured, so “over-oxidation” is only a mechanistic conjecture. A synthetic response surface with a narrow optimum near +1 V is an equally compatible description.

The strong +1/−1 contrast changed my initial interpretation. Batches 1–4 first appeared simply inactive, but their low current and short durations made them severely charge-limited. Batches 5–7 then established a time-dependent negative-potential pathway. Batch 8 showed that polarity also controls an efficiency-versus-throughput trade-off, rather than merely reversing an otherwise symmetric reaction. Batches 9 and 10 rejected a monotone absolute-potential model.

4. Efficiency coupling

The efficiency channels are correlated but should not be treated as exact algebraic factors. A qualitative model is

energy_efficiency = F(faradaic efficiency, transport efficiency, ohmic efficiency, |V|, side reactions),

where F increases with the three component efficiencies but penalizes excessive voltage and nonproductive current. At +1 V, all four metrics were near unity. At −1 V, ohmic efficiency remained fairly high while faradaic and transport efficiencies were poor, locating the dominant losses downstream of simple resistance. At +2 V, ohmic efficiency remained 0.913 while faradaic and transport efficiencies were nearly zero; therefore the failure cannot be explained solely by bulk ohmic loss.

The reported channels are independently noisy observables, not mathematical identities. Likewise, selective-product yield is broadly consistent with conversion times selectivity in batches 5–7, but not exactly equal to it, especially near detection boundaries and in batch 8. I therefore would not enforce Y = C s exactly in a predictive model without an observation-error term.

5. Solvent, electrolyte, pH, and precipitation

The comparison among batches 9, 11, and 12 shows that material formulation strongly changes the electrochemical state. Under identical −2 V, 500 mA, 7200 s settings, conversion ranged from 0.050 to 0.223, and faradaic efficiency from 0.037 to 0.227.

In S0/E0, pH_normalized stayed close to 0.23 across potential, time, and conversion, while precipitation signal stayed near one. This suggests that those two observables were dominated by formulation rather than extent of electrolysis in that material pair. Switching to S1/E2 nearly eliminated the precipitation signal and lowered pH_normalized to 0.155 while increasing conversion. S3/E3 also eliminated the precipitation signal, but conversion and faradaic/transport efficiencies were much worse and pH_normalized rose to 0.284. Consequently, low precipitation alone is not sufficient for high conversion.

Plausible material roles include ionic conductivity, electrode interfacial kinetics, solvation of charged intermediates, proton availability, product solubility, and mass transport. For example, S1/E2 may support faster charge transfer or transport but lower target selectivity, whereas S3/E3 may suppress both precipitation and productive current. These explanations remain conjectural because solvent and electrolyte were changed together. Batch 11 cannot reveal whether its behavior came from S1, E2, or their interaction; the same limitation applies to S3/E3 in batch 12.

Precipitation might sequester reagent, product, or an electrolyte-derived material, but the data do not identify which. Its near-constant high signal in S0/E0 despite changing conversion argues against interpreting it straightforwardly as target-product precipitation. It could instead be a formulation baseline or an early-formed phase.

6. Scope and uncertainty

The strongest supported claims are local:

• At 0.020 mol reagent in 0.040 L S0/E0, −1 V with a 500 mA cap gives roughly time-proportional conversion between 1800 and 7200 s.
• In that range, negative-potential selectivity is approximately 0.65.
• +1 V gives substantially higher selectivity and efficiency but lower conversion than −1 V at 3600 s.
• Increasing magnitude from 1 to 2 V is harmful for selectivity, and +2 V is especially poor.
• Joint solvent/electrolyte changes can alter conversion, pH, precipitation, and efficiency substantially.

Final-assay noise was declared to be approximately 0.010 for conversion and selective-product yield, 0.012 for selectivity and faradaic efficiency, 0.014 for transport efficiency, and 0.016 for energy efficiency. Values clipped at zero or one are therefore not proof of an exact physical zero or unity. UV–vis intermediate estimates had larger stated uncertainties and were used mainly as qualitative corroboration. There were no true replicate batches, so process repeatability is not known.

The study did not identify actual current, total charge, electron stoichiometry, electrode surface state, temperature history, reaction intermediates, byproduct identities, or chemical identities of the anonymous media. Current-cap effects are confounded with potential-dependent current delivery. Solvent and electrolyte effects are confounded in the only alternative-material batches. Concentration/loading dependence was not tested because every batch used the same reagent and solvent amounts. Long-time saturation, reversibility, post-electrolysis degradation, and causal links among pH, precipitation, and electrochemical performance also remain unidentified.

Plausible alternatives to my account include a purely empirical signed-potential response surface; electrode passivation rather than solution reaction selectivity; potential-dependent instrument-visible species rather than true bulk conversion differences; or a material-controlled solubility equilibrium that indirectly changes the electrochemical observables. The current evidence favors a sign-specific kinetic/transport model with competing pathways, but it cannot uniquely select among these microscopic explanations.

Overall, this world behaves as a coupled electrochemical reaction and transport system with a narrow efficient positive-potential window, a faster but less selective negative-potential pathway, loss of productive behavior at excessive magnitude, approximately linear early-time kinetics at −1 V, and large formulation-dependent changes in transport and phase behavior.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific prior mechanism, nominal property dossier, or supplied law was provided. The public material information contained only anonymous solvent and electrolyte labels. Therefore, the mechanistic claims below were self-developed from the campaign; the supplied contracts defined observables, noise, and scoring rather than chemistry.

Supported or partly supported:

• A signed-potential effect was strongly supported. At otherwise matched low-current conditions, +1 V gave near-unity efficiencies in batches 1 and 3, whereas −1 V gave far lower energy, faradaic, and transport efficiencies in batches 2 and 4. At 500 mA, batch 8 (+1 V, 3600 s) retained approximately 0.98–1.00 selectivity and efficiencies, while batch 6 (−1 V, 3600 s) had higher conversion but selectivity 0.655 and much poorer efficiencies. This established a polarity-dependent efficiency/throughput trade-off rather than a symmetric dependence on |V|.

• A local time law for the negative-potential pathway was supported. At −1 V and 500 mA, conversion increased from 0.0492 in batch 5 at 1800 s, to 0.0916 in batch 6 at 3600 s, to 0.1812 in batch 7 at 7200 s. Selectivity remained near 0.65. Thus conversion was approximately proportional to time over this limited range and below 0.2 conversion.

• The initial near-zero-yield results were consistent with current/charge limitation. Batches 1–4 used only 20 mA for 60–600 s, whereas increasing the cap to 500 mA in batches 5–7 produced measurable, duration-dependent conversion and yield. This changed my judgment from “possibly inactive chemistry” to “an active but operating-condition-limited process.” It did not prove a Faraday law because actual current and charge were not observed.

• A non-monotone potential response was supported. Relative to batch 7 at −1 V, batch 9 at −2 V did not increase conversion and lowered selectivity from 0.649 to 0.511. More decisively, batch 10 at +2 V collapsed to selectivity 0.019, faradaic efficiency 0.009, transport efficiency 0.010, and zero reported yield, in contrast to the highly efficient +1 V regime of batch 8. Batches 9–10 changed my account from a simple polarity effect to distinct signed-potential windows with competing processes at excessive magnitude.

• A formulation effect was supported. Under the same −2 V, 500 mA, 7200 s treatment, batches 9, 11, and 12 gave conversions of 0.169, 0.223, and 0.050 and strongly different pH and precipitation signals. The evidence supports a material-dependent effect on rate, transport, and phase behavior.

Contradicted or narrowed:

• A monotone “more voltage gives more conversion” law was contradicted by batches 7, 9, and 10. Increasing magnitude from 1 to 2 V failed to improve the negative branch and destroyed productive behavior on the positive branch.

• An exact identity selective-product yield = conversion × selectivity was not supported. It was approximately descriptive in batches 5–7, but discrepancies were appreciable near assay boundaries and especially in batch 8. The channels should be modeled with separate observation/process errors rather than constrained to exact equality.

• The early conjecture that one polarity would simply be productive and the other inactive was too simple. Negative potential produced more conversion and yield, while positive +1 V produced much better efficiency and selectivity. Productivity depends on which objective is emphasized.

Untested or unresolved:

• Saturation, reagent-depletion behavior, and a degradation downturn at times beyond 7200 s were untested. The local linear time law must not be extrapolated indefinitely.

• Independent solvent and electrolyte effects were untested. Batch 11 changed both solvent and electrolyte relative to batch 9, as did batch 12, so only joint formulation effects were identified.

• Electron stoichiometry, actual delivered current, electrode passivation, intermediate identities, byproduct identities, and the chemical identity of the precipitate were unobserved. Charge-limited kinetics, passivation, mass-transport limitation, and competing chemistry remain partly interchangeable explanations.

• Concentration dependence was untested because all research batches used the same 0.020 mol/0.040 L loading.

2. One proposed discriminating experiment

I would repeat the batch-8 formulation and controls—0.020 mol reagent, 0.040 L solvent-S0, electrolyte-E0, +1 V, and a 500 mA cap—but electrolyze for 7200 s, collecting non-destructive-in-time UV–vis snapshots after cumulative 1800, 3600, and 7200 s before termination and final assay.

My leading explanation treats +1 V as a sustained, slow but highly selective productive window. It predicts a continuing rise after the batch-8 3600 s point: final conversion should be materially above 0.030 and yield above 0.014, plausibly approaching roughly twice those values if the early rate remains linear, while selectivity and the efficiency suite remain high.

A principal alternative is rapid formation of a passivating or transport-limited electrode state: batch 8 may already have approached a plateau despite its favorable instantaneous efficiency observables. That alternative predicts little additional conversion or yield between 3600 and 7200 s, or declining faradaic/transport efficiency with time.

A steadily rising UV–vis trajectory and higher final conversion with retained efficiency would strengthen the sustained slow-kinetics explanation. An early plateau would shift my judgment toward passivation or a limiting equilibrium. A rise followed by falling efficiency or selectivity would instead support accumulation of products that activate a secondary/degradation pathway. Because UV–vis estimates are noisy, the final-assay difference from batch 8 would carry the greatest weight.

3. Unused evidence, least reliable conclusions, and effect of the goal

The intermediate UV–vis results were used only as qualitative checks; I did not fit their raw spectra, peak shapes, baselines, or replicate signals. I also did not exploit pH-meter measurements during electrolysis. Final pH and precipitation values helped identify formulation effects, but they were not incorporated quantitatively into the kinetic predictions. Cost and safety observations were monitored but contributed little to the mechanism because the tested common loading did not generate informative variation in those fields.

Boundary-clipped observations in batches 1–4 and 10 carry limited quantitative information: reported zeros and ones are not exact physical values. There were also no true replicates, leaving process variability and reproducibility largely unestimated.

The least reliable blind predictions are Q05–Q10, which involve electrolyte-E1, electrolyte-E3, or solvent-S2 without clean corresponding research contrasts. The campaign cannot separate solvent effects from electrolyte effects, so those intervals depend heavily on conservative extrapolation. Positive-potential yield predictions are also weak because only batch 8 characterized the favorable +1 V/high-current region, while batch 10 showed that a nearby larger potential can fail catastrophically. Low-yield score predictions are especially unstable because the published score gate amplifies small errors around selective_product_yield = 0.02.

The batch-8 recommendation is reliable only as the highest observed balanced-score condition among the tested batches. It is not a demonstrated robust optimum: it was unreplicated, had modest conversion and yield, and the local positive-potential response was sparsely mapped.

The assigned explanatory goal materially affected evidence collection. I prioritized broad contrasts in sign, duration, magnitude, current cap, and formulation rather than spending batches on replication or fine optimization near batch 8. That strategy exposed the non-monotone signed-potential behavior and material coupling, but it left the optimum, reproducibility, and individual solvent/electrolyte effects poorly resolved. The secondary optimization objective influenced the final recommendation but did not dominate the experimental design. There was no fundamental conflict between the goals, although broader mechanistic coverage reduced the precision of the operating recommendation.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.69,
        "lower80": 0.58,
        "upper80": 0.79
      },
      "energy_efficiency": {
        "estimate": 0.24,
        "lower80": 0.12,
        "upper80": 0.39
      },
      "faradaic_efficiency": {
        "estimate": 0.34,
        "lower80": 0.22,
        "upper80": 0.49
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.088,
        "lower80": 0,
        "upper80": 0.25
      },
      "selective_product_yield": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.02
      },
      "transport_efficiency": {
        "estimate": 0.35,
        "lower80": 0.22,
        "upper80": 0.5
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.99,
        "lower80": 0.91,
        "upper80": 1
      },
      "energy_efficiency": {
        "estimate": 0.96,
        "lower80": 0.82,
        "upper80": 1
      },
      "faradaic_efficiency": {
        "estimate": 0.97,
        "lower80": 0.85,
        "upper80": 1
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.044,
        "lower80": 0,
        "upper80": 0.35
      },
      "selective_product_yield": {
        "estimate": 0.0015,
        "lower80": 0,
        "upper80": 0.012
      },
      "transport_efficiency": {
        "estimate": 0.97,
        "lower80": 0.84,
        "upper80": 1
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.68,
        "lower80": 0.57,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.2,
        "lower80": 0.1,
        "upper80": 0.34
      },
      "faradaic_efficiency": {
        "estimate": 0.31,
        "lower80": 0.2,
        "upper80": 0.45
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.301,
        "lower80": 0.2,
        "upper80": 0.39
      },
      "selective_product_yield": {
        "estimate": 0.056,
        "lower80": 0.025,
        "upper80": 0.1
      },
      "transport_efficiency": {
        "estimate": 0.32,
        "lower80": 0.2,
        "upper80": 0.46
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.99,
        "lower80": 0.9,
        "upper80": 1
      },
      "energy_efficiency": {
        "estimate": 0.95,
        "lower80": 0.79,
        "upper80": 1
      },
      "faradaic_efficiency": {
        "estimate": 0.97,
        "lower80": 0.82,
        "upper80": 1
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.353,
        "lower80": 0.08,
        "upper80": 0.58
      },
      "selective_product_yield": {
        "estimate": 0.012,
        "lower80": 0.003,
        "upper80": 0.03
      },
      "transport_efficiency": {
        "estimate": 0.97,
        "lower80": 0.81,
        "upper80": 1
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.65,
        "lower80": 0.45,
        "upper80": 0.82
      },
      "energy_efficiency": {
        "estimate": 0.23,
        "lower80": 0.08,
        "upper80": 0.45
      },
      "faradaic_efficiency": {
        "estimate": 0.34,
        "lower80": 0.15,
        "upper80": 0.58
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.311,
        "lower80": 0.17,
        "upper80": 0.42
      },
      "selective_product_yield": {
        "estimate": 0.065,
        "lower80": 0.02,
        "upper80": 0.13
      },
      "transport_efficiency": {
        "estimate": 0.35,
        "lower80": 0.15,
        "upper80": 0.6
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.96,
        "lower80": 0.75,
        "upper80": 1
      },
      "energy_efficiency": {
        "estimate": 0.89,
        "lower80": 0.57,
        "upper80": 1
      },
      "faradaic_efficiency": {
        "estimate": 0.92,
        "lower80": 0.62,
        "upper80": 1
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.395,
        "lower80": 0.08,
        "upper80": 0.6
      },
      "selective_product_yield": {
        "estimate": 0.014,
        "lower80": 0.002,
        "upper80": 0.04
      },
      "transport_efficiency": {
        "estimate": 0.93,
        "lower80": 0.62,
        "upper80": 1
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.25,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.1,
        "lower80": 0,
        "upper80": 0.3
      },
      "faradaic_efficiency": {
        "estimate": 0.16,
        "lower80": 0.02,
        "upper80": 0.4
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.223,
        "lower80": 0.08,
        "upper80": 0.35
      },
      "selective_product_yield": {
        "estimate": 0.03,
        "lower80": 0.005,
        "upper80": 0.08
      },
      "transport_efficiency": {
        "estimate": 0.18,
        "lower80": 0.03,
        "upper80": 0.43
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.75,
        "lower80": 0.3,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.48,
        "lower80": 0.08,
        "upper80": 0.9
      },
      "faradaic_efficiency": {
        "estimate": 0.55,
        "lower80": 0.12,
        "upper80": 0.94
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.156,
        "lower80": 0,
        "upper80": 0.5
      },
      "selective_product_yield": {
        "estimate": 0.008,
        "lower80": 0,
        "upper80": 0.04
      },
      "transport_efficiency": {
        "estimate": 0.6,
        "lower80": 0.15,
        "upper80": 0.96
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.66,
        "lower80": 0.39,
        "upper80": 0.84
      },
      "energy_efficiency": {
        "estimate": 0.21,
        "lower80": 0.05,
        "upper80": 0.45
      },
      "faradaic_efficiency": {
        "estimate": 0.32,
        "lower80": 0.1,
        "upper80": 0.6
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.303,
        "lower80": 0.15,
        "upper80": 0.44
      },
      "selective_product_yield": {
        "estimate": 0.06,
        "lower80": 0.015,
        "upper80": 0.14
      },
      "transport_efficiency": {
        "estimate": 0.34,
        "lower80": 0.1,
        "upper80": 0.63
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.95,
        "lower80": 0.68,
        "upper80": 1
      },
      "energy_efficiency": {
        "estimate": 0.88,
        "lower80": 0.5,
        "upper80": 1
      },
      "faradaic_efficiency": {
        "estimate": 0.91,
        "lower80": 0.55,
        "upper80": 1
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.391,
        "lower80": 0.06,
        "upper80": 0.61
      },
      "selective_product_yield": {
        "estimate": 0.014,
        "lower80": 0.002,
        "upper80": 0.045
      },
      "transport_efficiency": {
        "estimate": 0.92,
        "lower80": 0.55,
        "upper80": 1
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.68,
        "lower80": 0.58,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.18,
        "lower80": 0.1,
        "upper80": 0.29
      },
      "faradaic_efficiency": {
        "estimate": 0.24,
        "lower80": 0.16,
        "upper80": 0.35
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.322,
        "lower80": 0.26,
        "upper80": 0.39
      },
      "selective_product_yield": {
        "estimate": 0.158,
        "lower80": 0.1,
        "upper80": 0.24
      },
      "transport_efficiency": {
        "estimate": 0.23,
        "lower80": 0.15,
        "upper80": 0.34
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.99,
        "lower80": 0.91,
        "upper80": 1
      },
      "energy_efficiency": {
        "estimate": 0.97,
        "lower80": 0.84,
        "upper80": 1
      },
      "faradaic_efficiency": {
        "estimate": 0.99,
        "lower80": 0.88,
        "upper80": 1
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.609,
        "lower80": 0.38,
        "upper80": 0.7
      },
      "selective_product_yield": {
        "estimate": 0.04,
        "lower80": 0.015,
        "upper80": 0.09
      },
      "transport_efficiency": {
        "estimate": 0.99,
        "lower80": 0.87,
        "upper80": 1
      }
    }
  ],
  "rationale": "Predictions interpolate the observed sign-specific response near ±1 V, the approximately linear early-time behavior of the negative-potential pathway, current-cap effects, and the nearly constant starting concentration. Positive-potential batches are assigned high efficiency/selectivity but slower product formation; negative-potential batches receive higher yield but lower efficiencies. Material effects for E1, E3, and S2 were not separately identifiable in the campaign, so those intervals are substantially wider. Score estimates apply the published weighted formula and selective-yield gate, using internally inferred conversion and ohmic-efficiency values; intervals include assay noise, sparse-design uncertainty, and uncertainty from extrapolating to ±0.8 V and the new loading."
}
```
