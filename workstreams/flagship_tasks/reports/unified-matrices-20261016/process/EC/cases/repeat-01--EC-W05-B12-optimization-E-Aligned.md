# repeat-01/EC-W05-B12-optimization-E-Aligned

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-01\EC-W05-B12-optimization-E-Aligned\participant\optimization-E-Aligned

## 同期笔记

### v1 · 公开事件 0

# Electrochemical campaign hypotheses

## H1 [tentative]
At fixed loading (planned 0.020 mol reagent in 0.040 L solvent), balanced score should show an interior optimum in potential magnitude and electrolysis duration: inadequate drive limits conversion, while excessive drive/time lowers selectivity and energy efficiency. I will test both signs and short/long durations; a sign reversal in productive conversion would change the favored polarity.

## H2 [tentative]
Nominal properties suggest electrolyte E1 may favor transport (thin diffusion layer, high diffusivity), whereas E0/S0 may favor ohmic efficiency (high conductivity). S1 may trade conductivity for diffusion. Because hidden residuals and interfacial selectivity are authoritative, material ranking remains unresolved pending final assays.

## Decision plan
Use early batches for broad polarity/material/drive screening at identical loading, then refine and replicate the highest public score. Meaningful differences must be judged against assay noise and confounding across conditions.

### v2 · 公开事件 83

# Electrochemical campaign hypotheses

## H1 [supported only in the tested E2/S2 scope]
At fixed loading (0.020 mol reagent in 0.040 L solvent), positive-potential performance has a sharp upper operating boundary. With E2/S2, +1.5 V improved as duration increased from 1200 to 3600, 7200, and 14400 s (final assays runner-operation-0027, -0034, -0048, -0055). At 14400 s, +1.6 V gave the highest observed score, 0.6496 (runner-operation-0076), whereas +1.7 V collapsed to 0.0447 with essentially absent conversion/selectivity/transport signals (runner-operation-0083). The large discontinuity exceeds the stated channel noise, but its exact threshold is unresolved because no replicate or intermediate voltage was run. Testable consequence: at this loading/material pair and 14400 s, voltages just below 1.7 V should outperform voltages at or above the apparent degradation boundary.

## H2 [supported in tested comparisons, interactions unresolved]
Precipitation control and electrolyte identity dominate the material response. E0/S0 showed precipitation signal near 1 and negligible selective yield under +1.0 V/300 s (runner-operation-0007). E2/S2 suppressed precipitation and supported progressively useful positive-potential conversion (runner-operation-0027 through -0076). At +1.5 V/14400 s with S2, E1 collapsed (runner-operation-0062), E3 was intermediate (runner-operation-0069), and E2 was best (runner-operation-0055). These are numerical material differences at one operating point, not isolated main effects; solvent/electrolyte interactions and hidden residuals remain alternatives.

## H3 [polarity effect unresolved across materials]
In E0/S0 at 300 s, +1.0 V gave zero selective yield (runner-operation-0007), while -1.0 V gave a small noisy yield and score 0.1714 (runner-operation-0013); stronger/longer negative operation did not improve it (runner-operation-0020). Positive potential was clearly productive in E2/S2, so polarity cannot be ranked independently of materials and effective potential shifts.

## Recommendation decision
Select batch 11: 0.020 mol reagent, 0.040 L S2, E2, +1.6 V, 100 mA cap, 14400 s. It has the highest public score and strong efficiencies with low precipitation (runner-operation-0076). I would change this choice only if a replicate showed the score advantage over batch 8 was assay noise or if fine mapping below the +1.7 V collapse identified a safer/higher optimum.

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
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 300,
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
    "cost": 0.28271999955177307,
    "electrochemical_conversion": 0.015709586441516876,
    "electrochemical_selectivity": 0.998518168926239,
    "energy_efficiency": 0.9631397724151611,
    "faradaic_efficiency": 1.0,
    "ohmic_efficiency": 0.9602119326591492,
    "pH_normalized": 0.23308512568473816,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.9858177900314331
  }
}
```

### 批次 2 · 终点事件 13

```json
{
  "ordinal": 2,
  "lifecycle_index": 2,
  "end_step": 13,
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
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1
    },
    {
      "duration_s": 300,
      "operation": "electrolyze"
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
    "cost": 0.2577199935913086,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.6434827446937561,
    "energy_efficiency": 0.2848791182041168,
    "faradaic_efficiency": 0.40667814016342163,
    "ohmic_efficiency": 0.9690497517585754,
    "pH_normalized": 0.2303897738456726,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.17142920196056366,
    "selective_product_yield": 0.010983134619891644,
    "transport_efficiency": 0.43293496966362
  }
}
```

### 批次 3 · 终点事件 20

```json
{
  "ordinal": 3,
  "lifecycle_index": 3,
  "end_step": 20,
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
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.5
    },
    {
      "duration_s": 1200,
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
    "cost": 0.28332000970840454,
    "electrochemical_conversion": 0.004547304008156061,
    "electrochemical_selectivity": 0.5527814030647278,
    "energy_efficiency": 0.13559363782405853,
    "faradaic_efficiency": 0.29719653725624084,
    "ohmic_efficiency": 0.9660394787788391,
    "pH_normalized": 0.231104776263237,
    "precipitation_signal": 0.9869203567504883,
    "safety_risk": 0.072194404900074,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.3137534558773041
  }
}
```

### 批次 4 · 终点事件 27

```json
{
  "ordinal": 4,
  "lifecycle_index": 4,
  "end_step": 27,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 1200,
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
    "cost": 0.32468000054359436,
    "electrochemical_conversion": 0.018919389694929123,
    "electrochemical_selectivity": 0.7261874079704285,
    "energy_efficiency": 0.656281054019928,
    "faradaic_efficiency": 0.7584185600280762,
    "ohmic_efficiency": 0.9201669096946716,
    "pH_normalized": 0.17094862461090088,
    "precipitation_signal": 0.0,
    "safety_risk": 0.1135944053530693,
    "score": 0.4051230251789093,
    "selective_product_yield": 0.017927497625350952,
    "transport_efficiency": 0.7269310355186462
  }
}
```

### 批次 5 · 终点事件 34

```json
{
  "ordinal": 5,
  "lifecycle_index": 5,
  "end_step": 34,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": 1.5
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
    "cost": 0.32635998725891113,
    "electrochemical_conversion": 0.08874351531267166,
    "electrochemical_selectivity": 0.8511865735054016,
    "energy_efficiency": 0.7726679444313049,
    "faradaic_efficiency": 0.9254315495491028,
    "ohmic_efficiency": 0.9457553625106812,
    "pH_normalized": 0.17590941488742828,
    "precipitation_signal": 0.0,
    "safety_risk": 0.1135944053530693,
    "score": 0.5548123121261597,
    "selective_product_yield": 0.0805179700255394,
    "transport_efficiency": 0.9149220585823059
  }
}
```

### 批次 6 · 终点事件 41

```json
{
  "ordinal": 6,
  "lifecycle_index": 6,
  "end_step": 41,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 2,
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
    "cost": 0.3299599885940552,
    "electrochemical_conversion": 0.0021511756349354982,
    "electrochemical_selectivity": 0.0042426493018865585,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.02405594103038311,
    "ohmic_efficiency": 0.9606892466545105,
    "pH_normalized": 0.17263348400592804,
    "precipitation_signal": 0.0023995577357709408,
    "safety_risk": 0.1135944053530693,
    "score": 0.04325827211141586,
    "selective_product_yield": 0.010337181389331818,
    "transport_efficiency": 0.0
  }
}
```

### 批次 7 · 终点事件 48

```json
{
  "ordinal": 7,
  "lifecycle_index": 7,
  "end_step": 48,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": 1.5
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
    "cost": 0.3285199999809265,
    "electrochemical_conversion": 0.18094216287136078,
    "electrochemical_selectivity": 0.8425830006599426,
    "energy_efficiency": 0.8006201982498169,
    "faradaic_efficiency": 0.9165647625923157,
    "ohmic_efficiency": 0.9791736602783203,
    "pH_normalized": 0.1716480702161789,
    "precipitation_signal": 0.0,
    "safety_risk": 0.1135944053530693,
    "score": 0.5903120636940002,
    "selective_product_yield": 0.15139730274677277,
    "transport_efficiency": 0.9199650883674622
  }
}
```

### 批次 8 · 终点事件 55

```json
{
  "ordinal": 8,
  "lifecycle_index": 8,
  "end_step": 55,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": 1.5
    },
    {
      "duration_s": 14400,
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
    "cost": 0.3328399956226349,
    "electrochemical_conversion": 0.33616724610328674,
    "electrochemical_selectivity": 0.8392595648765564,
    "energy_efficiency": 0.7959927320480347,
    "faradaic_efficiency": 0.9224587678909302,
    "ohmic_efficiency": 0.9644696116447449,
    "pH_normalized": 0.16995058953762054,
    "precipitation_signal": 0.00031451715040020645,
    "safety_risk": 0.1135944053530693,
    "score": 0.6385688185691833,
    "selective_product_yield": 0.2673843502998352,
    "transport_efficiency": 0.9159634113311768
  }
}
```

### 批次 9 · 终点事件 62

```json
{
  "ordinal": 9,
  "lifecycle_index": 9,
  "end_step": 62,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 1.5
    },
    {
      "duration_s": 14400,
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
    "cost": 0.3328399956226349,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.031468190252780914,
    "faradaic_efficiency": 0.0,
    "ohmic_efficiency": 0.979599118232727,
    "pH_normalized": 0.22095520794391632,
    "precipitation_signal": 0.538132905960083,
    "safety_risk": 0.1135944053530693,
    "score": 0.07706377655267715,
    "selective_product_yield": 0.01722601428627968,
    "transport_efficiency": 0.012177566066384315
  }
}
```

### 批次 10 · 终点事件 69

```json
{
  "ordinal": 10,
  "lifecycle_index": 10,
  "end_step": 69,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": 1.5
    },
    {
      "duration_s": 14400,
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
    "cost": 0.3328399956226349,
    "electrochemical_conversion": 0.22893860936164856,
    "electrochemical_selectivity": 0.7741620540618896,
    "energy_efficiency": 0.5621843338012695,
    "faradaic_efficiency": 0.5814235210418701,
    "ohmic_efficiency": 0.9628942012786865,
    "pH_normalized": 0.2869914472103119,
    "precipitation_signal": 0.0,
    "safety_risk": 0.1135944053530693,
    "score": 0.4760756492614746,
    "selective_product_yield": 0.15883386135101318,
    "transport_efficiency": 0.5827731490135193
  }
}
```

### 批次 11 · 终点事件 76

```json
{
  "ordinal": 11,
  "lifecycle_index": 11,
  "end_step": 76,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": 1.6
    },
    {
      "duration_s": 14400,
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
    "cost": 0.3334159851074219,
    "electrochemical_conversion": 0.3550763428211212,
    "electrochemical_selectivity": 0.8366993069648743,
    "energy_efficiency": 0.8168136477470398,
    "faradaic_efficiency": 0.9178078770637512,
    "ohmic_efficiency": 0.9536089897155762,
    "pH_normalized": 0.17063526809215546,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.1135944053530693,
    "score": 0.6495705842971802,
    "selective_product_yield": 0.2903718054294586,
    "transport_efficiency": 0.9249878525733948
  }
}
```

### 批次 12 · 终点事件 83

```json
{
  "ordinal": 12,
  "lifecycle_index": 12,
  "end_step": 83,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": 1.7
    },
    {
      "duration_s": 14400,
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
    "cost": 0.33399200439453125,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.0,
    "ohmic_efficiency": 0.9698421955108643,
    "pH_normalized": 0.17115558683872223,
    "precipitation_signal": 0.0,
    "safety_risk": 0.1135944053530693,
    "score": 0.044721391052007675,
    "selective_product_yield": 0.011055422015488148,
    "transport_efficiency": 0.0
  }
}
```

## K1 封存报告

Mechanism report

1. Empirical picture

The system appears to contain at least four coupled layers: (i) bulk solution and precipitation chemistry set by solvent and electrolyte, (ii) electrical/ionic transport, (iii) a potential-dependent interfacial conversion pathway, and (iv) a sharply competing unproductive pathway at excessive positive potential. The public score is then calculated from the resulting conversion, selectivity, selective yield, and efficiency channels.

All experiments used 0.020 mol reagent in 0.040 L solvent and a 100 mA current cap. Consequently, my conclusions apply to that loading and current setting; concentration and current effects are not identifiable from this campaign.

2. Relationship between assay variables and score

The reported selective-product yield was approximately conversion × selectivity in the productive experiments. Examples are batch 7 (0.18094 × 0.84258 = 0.15245 versus observed yield 0.15140), batch 8 (0.33617 × 0.83926 = 0.28213 versus 0.26738), and batch 11 (0.35508 × 0.83670 = 0.29712 versus 0.29037). Deviations are compatible with assay noise, process proxies, or a small mass-balance correction.

The observations also reveal the published score calculation. Before gating, it is well described by

B = 0.30Y + 0.15S + 0.10X + 0.15E + 0.12F + 0.10T + 0.08O,

where Y is selective-product yield, S selectivity, X conversion, E energy efficiency, F faradaic efficiency, T transport efficiency, and O ohmic efficiency. The selective-yield gate behaves as

score = B × min(1, Y/0.02).

Thus a process with excellent efficiency but essentially no product can score zero. This explains batch 1: selectivity and efficiency channels were high, but yield was 0 and the score was 0. Batch 4 had Y = 0.01793, just below the gate threshold, so its otherwise approximately 0.452 weighted score was reduced to 0.405. Batch 11 had Y = 0.29037 and therefore received its ungated score of 0.64957.

3. Potential and time response in the productive E2/S2 regime

Electrolyte E2 with solvent S2 established the clearest productive regime. At +1.5 V, increasing electrolysis time raised conversion while selectivity and most efficiencies remained nearly constant:

• Batch 5, 3600 s: conversion 0.08874, selectivity 0.85119, yield 0.08052, score 0.55481.
• Batch 7, 7200 s: conversion 0.18094, selectivity 0.84258, yield 0.15140, score 0.59031.
• Batch 8, 14400 s: conversion 0.33617, selectivity 0.83926, yield 0.26738, score 0.63857.

Faradaic efficiency stayed about 0.917–0.925, transport efficiency about 0.915–0.920, and energy efficiency about 0.773–0.801. This suggests that, inside the good potential window, time mainly controls extent of reaction rather than changing the reaction network.

A simple empirical representation is

X(t) ≈ 1 − exp(−k_eff t).

The three +1.5 V observations imply k_eff values of approximately 2.6–2.9 × 10^-5 s^-1. That consistency supports a pseudo-first-order progress law, although a nearly linear charge-controlled process over the observed conversion range is a plausible alternative because actual current was not measured and the current cap never varied. A useful process model within this narrow scope is therefore

Y(t,V,M) ≈ X(t,V,M) × S(V,M),
X(t,V,M) ≈ 1 − exp[−k(V,M)t],

with material combination M controlling both k and the potential window.

Potential was not monotonic. At 14400 s with E2/S2, raising potential from +1.5 V in batch 8 to +1.6 V in batch 11 increased conversion from 0.33617 to 0.35508, yield from 0.26738 to 0.29037, energy efficiency from 0.79599 to 0.81681, and score from 0.63857 to 0.64957. The selectivity remained similar (0.83926 versus 0.83670). Batch 11 was therefore the best observation.

However, +1.7 V at the same composition and duration caused a discontinuous collapse in batch 12: observed conversion and selectivity were both 0, faradaic, transport, and energy efficiencies were all 0, yield was only 0.01106, and score was 0.04472. A separate +2.0 V/7200 s run, batch 6, behaved similarly: conversion 0.00215, selectivity 0.00424, transport and energy efficiencies 0, and score 0.04326. The large changes are far greater than the declared final-assay noise.

I therefore infer a narrow potential window followed by an interfacial overdrive threshold between +1.6 and +1.7 V under E2/S2 conditions. Below the threshold, charge is directed efficiently to target formation. Above it, a competing side reaction, electrode-state transition, passivation event, or rapid degradation pathway consumes current and destroys faradaic/transport performance. The fact that batch 12 retained high ohmic efficiency (0.96984), essentially unchanged pH-normalized signal (0.17116), and zero precipitation signal argues against bulk resistance, bulk acid change, or precipitation being the immediate cause of this cliff. It instead points toward an interfacial or selectivity/faradaic transition. The exact threshold and whether it is smooth but very steep or truly discontinuous were not resolved.

4. Solvent and electrolyte coupling

The material dossier suggests that solvent S2 has low relative conductivity (0.5), reduced proton activity (0.28), a tenfold relative solubility-product factor, and a +0.20 V nominal potential shift. Electrolyte E2 has modest bulk conductivity (3.8 S m^-1), a thin nominal diffusion layer (0.48 mm), relatively low precipitating-salt concentration (0.001 mol L^-1), and a +0.18 V standard-potential shift. Despite its low nominal conductivity, this combination gave high ohmic efficiency (0.920–0.979) and high transport efficiency in the productive window. Thus nominal bulk conductivity alone did not determine performance.

Solvent S0/electrolyte E0 behaved very differently. Batch 1 at +1.0 V for 300 s had conversion 0.01571, selectivity 0.99852, faradaic efficiency 1.0, transport efficiency 0.98582, and energy efficiency 0.96314, yet selective yield was 0 and precipitation signal was 1.0. Batch 2 at −1.0 V/300 s gave a small yield of 0.01098, precipitation 1.0, and score 0.17143. Stronger negative operation in batch 3 (−1.5 V, 1200 s) did not help: yield was 0 and score 0. E0 has the highest nominal precipitating-salt concentration among the profiles, while S0 lacks S2's enhanced solubility-product factor. The consistent near-unity precipitation signal supports precipitation or loss of soluble product/reactant as an important limitation in E0/S0. Nevertheless, batch 1 also shows that high proxy efficiencies do not prove recoverable target formation.

At +1.5 V/14400 s in S2, changing only the electrolyte caused large changes:

• E2, batch 8: score 0.63857, conversion 0.33617, yield 0.26738, precipitation 0.00031.
• E3, batch 10: score 0.47608, conversion 0.22894, yield 0.15883, precipitation 0, transport efficiency 0.58277, faradaic efficiency 0.58142.
• E1, batch 9: score 0.07706, observed conversion and selectivity 0, yield 0.01723, precipitation 0.53813, transport efficiency 0.01218.

E3/S2 avoided precipitation but was transport- and faradaic-limited relative to E2/S2. Its nominal diffusion layer is much thicker (2.8 mm), providing a plausible explanation for its lower transport efficiency despite high nominal conductivity. E1 has high nominal diffusivity and a thin diffusion layer, so its collapse cannot be explained by those bulk properties alone. Its different potential shift, acid environment, precipitation behavior, and hidden interfacial residuals may move +1.5 V outside its productive window. Batch 9 therefore demonstrates strong electrolyte–potential coupling rather than a universal ranking in which E2 is intrinsically best at every voltage.

One possible effective-potential description is

η_eff = V_applied − V0 − ΔV_solvent − ΔV_electrolyte − iR − ΔV_hidden,

with target formation efficient only for η_low < η_eff < η_high. The signs of the supplied nominal shifts in this equation cannot be established from the experiments, so this expression is conceptual rather than a fitted law. It explains why the same applied voltage can be productive for E2 but destructive for E1, and why material rankings should not be extrapolated without mapping their individual voltage windows.

5. Polarity

The E0/S0 comparison initially suggested that negative polarity might be somewhat more productive: batch 1 at +1.0 V had zero yield, while batch 2 at −1.0 V produced a small yield and nonzero score. However, batch 3 showed that making the negative potential stronger and longer did not improve production, while later E2/S2 experiments established a clearly productive positive-potential pathway. Consequently, polarity is not identifiable as a material-independent factor. The data are more consistent with solvent- and electrolyte-dependent effective potentials, precipitation, and interfacial kinetics than with a simple rule that one polarity is universally correct.

6. pH and precipitation observables

The pH-normalized signal was stable within a given electrolyte/material series: approximately 0.170–0.176 for E2/S2, 0.221 for E1/S2, 0.287 for E3/S2, and 0.230–0.233 for E0/S0. It did not change appreciably across the productive-to-collapsed potential transition in E2/S2, so it appears primarily composition-controlled rather than a direct reaction-progress variable in these runs.

Precipitation was likewise strongly composition-dependent: near 1 for E0/S0, 0.538 for E1/S2, and near 0 for E2/S2 and E3/S2. Avoiding precipitation was apparently necessary for high yield in the tested cases but not sufficient: batches 6 and 12 collapsed despite negligible precipitation. I therefore treat precipitation as one gate on accessible material, alongside a separate interfacial potential gate.

7. Safety and cost

Observed safety risk depended more on composition/loading than on voltage or duration. E0/S0 runs were about 0.0722, while S2 runs were about 0.1136, all well below the public limit of 0.65. This is an observation about the benchmark's reported risk, not evidence that analogous real chemicals would be safe. Costs changed only modestly across the E2/S2 duration and potential series, so the score optimum was driven mainly by chemistry and efficiency rather than cost.

8. Integrated mechanistic proposal

A compact pseudocode representation of my explanation is:

bulk_state = f(solvent, electrolyte, loading)
precipitated_fraction = precipitation_model(bulk_state)
pH_state = acid_base_model(solvent, electrolyte)
eta_eff = potential − material_shift − ohmic_drop − hidden_interface_shift

if eta_eff lies in target_window(material_pair):
    k_target = productive_rate(eta_eff, transport, current)
    conversion = 1 − exp(−k_target × time)
    selectivity ≈ material_and_eta_selectivity
    faradaic_efficiency, transport_efficiency = high
else if eta_eff exceeds upper_boundary:
    side_reaction_or_passivation dominates
    target conversion and selectivity collapse
    faradaic and transport efficiencies collapse

recoverable_yield ≈ conversion × selectivity × (1 − inaccessible_fraction)
score = weighted_efficiency_sum × min(1, recoverable_yield/0.02)

For E2/S2 at 100 mA and the tested loading, +1.5 to +1.6 V is inside the productive window, while +1.7 to +2.0 V is beyond its upper boundary. Longer time inside the window increases conversion approximately pseudo-first-order without materially reducing selectivity. E0/S0 is strongly precipitation-limited, E3/S2 is comparatively transport/faradaic-limited at +1.5 V, and E1/S2 at that voltage appears to combine precipitation with an unfavorable interfacial regime.

9. Evidence that changed the explanation

Batch 1 prevented me from treating high faradaic, transport, and selectivity readings as sufficient for success, because yield and score remained zero in the presence of complete precipitation signal. Batches 2–3 rejected a simple strategy of applying increasingly negative potential. Batch 4 showed that S2/E2 could suppress precipitation and enter a productive positive-potential regime. Batches 5, 7, and 8 established the duration law and stable selectivity/efficiency plateau at +1.5 V. Batch 6 first revealed severe positive overdrive. Batches 9–10 demonstrated that nominal material properties do not transfer independently of voltage and that electrolyte identity strongly couples to transport, precipitation, and interface behavior. Batch 11 showed a modest improvement at +1.6 V. Batch 12 then located the sharp failure boundary between +1.6 and +1.7 V and made the interfacial-threshold explanation central.

10. Scope, unidentified quantities, and alternatives

The mechanism is empirical and benchmark-specific. Solvent and electrolyte labels are anonymous and do not identify real substances. Electrode area, gap, contact resistance, actual current, electrode surface state, temperature trajectory, concentrations after sampling, and identities or quantities of side products were not observed. The hidden material residuals cannot be separated from nominal solvent/electrolyte properties.

Because reagent amount, solvent volume, and current cap were fixed, I cannot distinguish first-order kinetics from charge-limited conversion, estimate reaction order, quantify concentration effects, or determine whether 100 mA was actually reached. Material comparisons were made at a common applied voltage rather than at equal effective overpotential, so they conflate intrinsic kinetics with potential shifts. Most conditions were unreplicated; the small score difference between batches 8 and 11 could contain assay noise, although the batch-12 collapse is too large to attribute plausibly to the stated noise alone.

Plausible alternatives to the inferred overdrive side reaction include electrode passivation, a hidden switching rule based on potential, substrate or product degradation, a transport instability, or synthetic clipping after a latent efficiency becomes negative. The unchanged bulk pH, precipitation, and ohmic channels disfavor—but do not eliminate—bulk precipitation or resistance as the direct cause. Likewise, E0/S0's zero yield could reflect sequestration, product instability, or a measurement/mass-balance rule rather than literal precipitation of the target.

The selected batch 11 procedure is therefore an observed local optimum, not a universal optimum: 0.020 mol reagent, 0.040 L S2, electrolyte E2, +1.6 V, 100 mA cap, and 14400 s. Extrapolation beyond 14400 s is especially uncertain because conversion was still rising but the potential response had a sharp nearby failure boundary.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific prior or hidden-world ranking was supplied. The only supplied prior was the nominal material dossier, which explicitly warned that its properties were incomplete and subject to hidden residuals and coupling.

My pre-experiment claim that performance would have an interior potential optimum was supported in the E2/S2 scope. Batch 11 at +1.6 V and 14,400 s scored 0.6496, whereas otherwise matched batch 12 at +1.7 V collapsed to 0.0447; batch 6 at +2.0 V also performed poorly. The claim that insufficient duration limits conversion was supported by batches 5, 7, and 8: at +1.5 V, conversion rose from 0.0887 to 0.1809 to 0.3362 as time increased from 3,600 to 7,200 to 14,400 s, while selectivity remained near 0.84.

The initial nominal-property expectation that E1 might be transport-favorable was contradicted at the tested S2/+1.5 V/14,400 s condition. Batch 9 had transport efficiency 0.0122 and score 0.0771, versus 0.9160 and 0.6386 for E2 in batch 8. This changed my judgment from a bulk-property ranking to a material-dependent effective-potential and interface model. E3 in batch 10 was intermediate, further showing that conductivity alone was not predictive.

The supplied score law was empirically supported. Across the assays, the weighted metric sum reproduced the reported score when selective yield exceeded 0.02, while batches below that threshold behaved consistently with multiplication by min(1, yield/0.02). The self-developed approximation selective yield ≈ conversion × selectivity was also supported by batches 7, 8, and 11, within assay/process deviations.

A pseudo-first-order time law was compatible with batches 5, 7, and 8, but it was not uniquely established. Retrospectively, those data are also compatible with charge-controlled conversion over the sampled range. Because current, concentration, and electrode configuration were not varied in the campaign, reaction order and charge stoichiometry remain untested.

Batch 1 changed my view that high proxy efficiencies necessarily imply a successful process: despite very high selectivity and efficiency channels, its measured yield and score were zero. Batches 2 and 3 weakened a simple negative-polarity strategy. Batch 4 established E2/S2 as a productive, low-precipitation region. Batches 6 and 12 then made the sharp high-potential failure boundary central to the final explanation.

Untested claims include behavior at other reagent concentrations or solvent volumes, the effect of the current cap, solvent S1 or S3, most solvent–electrolyte interactions, electrode-history effects, and whether addition order matters. A universal polarity rule was neither supported nor adequately testable because polarity was not crossed with all material pairs.

2. Most informative additional experiment

I would run the batch-11 composition and loading—0.020 mol reagent, 0.040 L S2, E2, and a 100 mA cap—but at +1.7 V for only 3,600 s, followed by the final assay. This directly separates an immediate potential-threshold explanation from a cumulative high-potential degradation or passivation explanation.

If conversion, selectivity, faradaic efficiency, and transport efficiency were already near zero, resembling batch 12 despite the shorter exposure, I would strengthen the claim that +1.7 V crosses an immediate interfacial or side-reaction threshold. If the short run resembled productive batch 5, but batch 12 remained collapsed after 14,400 s, I would instead favor cumulative product degradation, electrode passivation, or a charge-dependent state transition. An intermediate result would suggest a steep continuous interaction between potential and exposure rather than a discrete switch. A high yield with low efficiency would point toward accumulated product formation followed by parasitic current, whereas low yield with initially plausible efficiency would suggest a recovery or assay limitation. Replication would ultimately still be needed because this single experiment could not quantify run-to-run variation.

3. Unused evidence, reliability, and goal effects

The raw spectral artifacts, peak shapes, replicate signals, and most intermediate UV–visible traces were not modeled quantitatively. I relied mainly on processed final-assay estimates. Cost was recorded but was not a score component, and safety risk varied little within each material series, so neither contributed much to mechanism discrimination. The nominal acid, capacitance, diffusivity, conductivity, and solubility properties were used qualitatively rather than fitted jointly. No systematic uncertainty propagation or replicate-based process variance estimate was possible.

The least reliable blind predictions are Q11 and Q12 because 500 mA was never tested and may introduce current-density, transport, heating, or depletion effects absent from the campaign. Predictions for E1 and E3 at ±0.8 V, and the E0/S2 cross in Q09–Q10, are also weak because the campaign did not map their potential windows. Negative-potential yields and scores are particularly uncertain because several observed yields were close to the assay's zero boundary and the score gate amplifies small yield errors.

The recommendation of batch 11 is locally evidence-based but its advantage over batch 8 is not highly secure: their scores differed by only about 0.011, there were no replicates, and several noisy channels contribute to the score. The location of the optimum between +1.6 and +1.7 V is consequently less reliable than the conclusion that +1.7 V is hazardous to performance under the tested conditions.

The assigned goal did affect evidence collection. After batch 4 identified a promising region, I concentrated experiments on improving the public score in E2/S2 rather than completing a balanced factorial design. That produced a useful duration series and located the high-potential boundary, but left current, concentration, addition order, two solvents, and many material–potential combinations unexplored. I see no direct conflict between the evidence and the optimization goal; the tradeoff was reduced causal identifiability and wider prediction uncertainty outside the optimized region.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.69,
        "lower80": 0.58,
        "upper80": 0.8
      },
      "energy_efficiency": {
        "estimate": 0.36,
        "lower80": 0.22,
        "upper80": 0.5
      },
      "faradaic_efficiency": {
        "estimate": 0.46,
        "lower80": 0.35,
        "upper80": 0.57
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.14,
        "lower80": 0,
        "upper80": 0.31
      },
      "selective_product_yield": {
        "estimate": 0.008,
        "lower80": 0,
        "upper80": 0.021
      },
      "transport_efficiency": {
        "estimate": 0.49,
        "lower80": 0.36,
        "upper80": 0.62
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.98,
        "lower80": 0.92,
        "upper80": 1
      },
      "energy_efficiency": {
        "estimate": 0.9,
        "lower80": 0.76,
        "upper80": 0.98
      },
      "faradaic_efficiency": {
        "estimate": 0.96,
        "lower80": 0.88,
        "upper80": 1
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.58,
        "lower80": 0.32,
        "upper80": 0.69
      },
      "selective_product_yield": {
        "estimate": 0.024,
        "lower80": 0.006,
        "upper80": 0.045
      },
      "transport_efficiency": {
        "estimate": 0.95,
        "lower80": 0.84,
        "upper80": 1
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.7,
        "lower80": 0.56,
        "upper80": 0.82
      },
      "energy_efficiency": {
        "estimate": 0.36,
        "lower80": 0.2,
        "upper80": 0.52
      },
      "faradaic_efficiency": {
        "estimate": 0.47,
        "lower80": 0.33,
        "upper80": 0.6
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.16,
        "lower80": 0,
        "upper80": 0.35
      },
      "selective_product_yield": {
        "estimate": 0.009,
        "lower80": 0,
        "upper80": 0.024
      },
      "transport_efficiency": {
        "estimate": 0.5,
        "lower80": 0.34,
        "upper80": 0.65
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.98,
        "lower80": 0.92,
        "upper80": 1
      },
      "energy_efficiency": {
        "estimate": 0.89,
        "lower80": 0.77,
        "upper80": 0.98
      },
      "faradaic_efficiency": {
        "estimate": 0.96,
        "lower80": 0.88,
        "upper80": 1
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.684,
        "lower80": 0.61,
        "upper80": 0.75
      },
      "selective_product_yield": {
        "estimate": 0.29,
        "lower80": 0.22,
        "upper80": 0.36
      },
      "transport_efficiency": {
        "estimate": 0.94,
        "lower80": 0.83,
        "upper80": 1
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.72,
        "lower80": 0.51,
        "upper80": 0.88
      },
      "energy_efficiency": {
        "estimate": 0.42,
        "lower80": 0.2,
        "upper80": 0.64
      },
      "faradaic_efficiency": {
        "estimate": 0.52,
        "lower80": 0.31,
        "upper80": 0.71
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.2,
        "lower80": 0,
        "upper80": 0.42
      },
      "selective_product_yield": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.032
      },
      "transport_efficiency": {
        "estimate": 0.64,
        "lower80": 0.39,
        "upper80": 0.83
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.9,
        "lower80": 0.72,
        "upper80": 0.99
      },
      "energy_efficiency": {
        "estimate": 0.8,
        "lower80": 0.6,
        "upper80": 0.94
      },
      "faradaic_efficiency": {
        "estimate": 0.88,
        "lower80": 0.7,
        "upper80": 0.98
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.628,
        "lower80": 0.43,
        "upper80": 0.75
      },
      "selective_product_yield": {
        "estimate": 0.23,
        "lower80": 0.12,
        "upper80": 0.35
      },
      "transport_efficiency": {
        "estimate": 0.94,
        "lower80": 0.78,
        "upper80": 1
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.35,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.16,
        "lower80": 0,
        "upper80": 0.36
      },
      "faradaic_efficiency": {
        "estimate": 0.28,
        "lower80": 0.09,
        "upper80": 0.49
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.07,
        "lower80": 0,
        "upper80": 0.25
      },
      "selective_product_yield": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.021
      },
      "transport_efficiency": {
        "estimate": 0.3,
        "lower80": 0.1,
        "upper80": 0.52
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.85,
        "lower80": 0.63,
        "upper80": 0.97
      },
      "energy_efficiency": {
        "estimate": 0.58,
        "lower80": 0.35,
        "upper80": 0.78
      },
      "faradaic_efficiency": {
        "estimate": 0.65,
        "lower80": 0.42,
        "upper80": 0.84
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.5,
        "lower80": 0.33,
        "upper80": 0.65
      },
      "selective_product_yield": {
        "estimate": 0.17,
        "lower80": 0.08,
        "upper80": 0.28
      },
      "transport_efficiency": {
        "estimate": 0.6,
        "lower80": 0.36,
        "upper80": 0.8
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.64,
        "lower80": 0.43,
        "upper80": 0.81
      },
      "energy_efficiency": {
        "estimate": 0.24,
        "lower80": 0.05,
        "upper80": 0.45
      },
      "faradaic_efficiency": {
        "estimate": 0.37,
        "lower80": 0.18,
        "upper80": 0.57
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.1,
        "lower80": 0,
        "upper80": 0.3
      },
      "selective_product_yield": {
        "estimate": 0.007,
        "lower80": 0,
        "upper80": 0.023
      },
      "transport_efficiency": {
        "estimate": 0.4,
        "lower80": 0.2,
        "upper80": 0.61
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.9,
        "lower80": 0.72,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.7,
        "lower80": 0.48,
        "upper80": 0.86
      },
      "faradaic_efficiency": {
        "estimate": 0.82,
        "lower80": 0.63,
        "upper80": 0.94
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.582,
        "lower80": 0.41,
        "upper80": 0.7
      },
      "selective_product_yield": {
        "estimate": 0.23,
        "lower80": 0.13,
        "upper80": 0.34
      },
      "transport_efficiency": {
        "estimate": 0.75,
        "lower80": 0.54,
        "upper80": 0.9
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.35,
        "upper80": 0.8
      },
      "energy_efficiency": {
        "estimate": 0.16,
        "lower80": 0,
        "upper80": 0.38
      },
      "faradaic_efficiency": {
        "estimate": 0.3,
        "lower80": 0.08,
        "upper80": 0.53
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.1,
        "lower80": 0,
        "upper80": 0.31
      },
      "selective_product_yield": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.032
      },
      "transport_efficiency": {
        "estimate": 0.22,
        "lower80": 0.04,
        "upper80": 0.47
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.9,
        "lower80": 0.72,
        "upper80": 0.99
      },
      "energy_efficiency": {
        "estimate": 0.55,
        "lower80": 0.32,
        "upper80": 0.76
      },
      "faradaic_efficiency": {
        "estimate": 0.75,
        "lower80": 0.5,
        "upper80": 0.92
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.763,
        "lower80": 0.56,
        "upper80": 0.88
      },
      "selective_product_yield": {
        "estimate": 0.85,
        "lower80": 0.55,
        "upper80": 0.98
      },
      "transport_efficiency": {
        "estimate": 0.4,
        "lower80": 0.2,
        "upper80": 0.68
      }
    }
  ],
  "rationale": "The predictions use the campaign's polarity-dependent efficiency response, the approximately charge/time-controlled conversion seen inside the productive positive-potential window, and the inferred score weights with its yield gate. The new concentration is close to the studied loading, while electrolyte, solvent, and especially the untested 500 mA condition receive wider intervals. Negative-potential yields are treated as near-zero with clipping/noise-driven score uncertainty; positive 100 mA batches are projected from observed faradaic and transport behavior. At 500 mA, greater charge is expected to raise conversion strongly but reduce transport and energy efficiency."
}
```
