# repeat-02/EC-W02-B12-optimization-E-MisIndexed

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-02\EC-W02-B12-optimization-E-MisIndexed\participant\optimization-E-MisIndexed

## 同期笔记

### v1 · 公开事件 0

# Hypothesis notebook

## H1 [tentative; pre-experiment]
At fixed loading (0.020 mol reagent in 0.050 L), balanced efficiency should have an interior optimum in potential magnitude and electrolysis duration: conversion rises with charge, while selectivity/energy efficiency eventually fall. Opposite potential signs may be strongly asymmetric. This will be tested across both signs and short/long durations.

## H2 [tentative; pre-experiment]
The best material pair may trade conductivity against mass transport and precipitation. Nominally S0/E0 should conduct well with a thin diffusion layer, while E3 may avoid precipitation but has a thick diffusion layer; E2 may suffer precipitation. A material screen at common electrolysis settings should distinguish these alternatives.

## Design decision
Use all 12 batches as independent fixed-loading assays, first spanning sign, magnitude, duration, solvent, and electrolyte, then refining around the strongest public score. One intermediate UV-vis measurement per batch will use the available 12-use budget and provide efficiency diagnostics before termination.

### v2 · 公开事件 85

# Hypothesis notebook

## H1 [supported in tested negative-potential scope; positive-sign asymmetry supported]
At fixed loading (0.020 mol in 0.050 L), negative potential produced the target response whereas +1.2 V did not: batch 1 at +1.2 V/600 s had zero reported selective yield and score, while batch 2 at -1.2 V/600 s had nonzero yield and score (events runner-operation-0007 and -0014). The result supports sign asymmetry, though only one positive condition was assayed.

Within S0/E2 at a 500 mA cap, lowering magnitude while extending time improved the observed balanced score and yield: -1.0 V/7200 s (batch 8, event -0056), -0.8 V/7200 s (batch 9, -0063), -0.6 V/10000 s (batch 10, -0070), and -0.4 V/14400 s (batch 11, -0077) rose sequentially in score (0.354, 0.408, 0.464, 0.493) and selective yield (0.164, 0.228, 0.333, 0.474). This progression is not a clean one-factor potential experiment because duration also changed.

Extending -0.4 V from 14400 to 19200 s increased observed conversion, yield, and score slightly (batch 12, event -0085: 0.812, 0.550, 0.499) while faradaic and transport efficiencies decreased relative to batch 11. Thus an interior duration optimum remains unresolved; the extra 4800 s produced only a small score gain and clear efficiency tradeoffs. Independent replication is absent, so the small score difference between batches 11 and 12 is numerical rather than firm evidence.

## H2 [partly supported, narrow scope]
At S0, -1.2 V, 100 mA cap, 600 s, E2 gave the highest observed score among E0–E3 (batches 2 and 5–7; events -0014, -0035, -0042, -0049), with negligible precipitation signal versus E0 and E1. Score differences were small and selective yields were near the scoring gate, so electrolyte superiority at short time is tentative. E2 nevertheless enabled the strongest later long-duration results. Solvent effects remain unresolved because later solvent screening was suspended to allocate batches to the unexpectedly important duration/potential regime.

## Operating decision
Recommend batch 12 as the highest observed public score (0.499) and yield, using S0, E2, 0.020 mol/0.050 L, -0.4 V, 500 mA cap, and segmented 14400 + 4800 s electrolysis. Batch 11 is a credible lower-time alternative because its score was nearly equal with better faradaic/transport efficiency. A future result showing reproducibly lower batch-12 score or stronger long-time degradation would switch the recommendation to batch 11.

## 实际批次及公开测量

### 批次 1 · 终点事件 7

```json
{
  "ordinal": 1,
  "lifecycle_index": 1,
  "end_step": 7,
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.05
    },
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1.2
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
    "cost": 0.285288006067276,
    "electrochemical_conversion": 0.008014115504920483,
    "electrochemical_selectivity": 0.01034972071647644,
    "energy_efficiency": 0.005256945732980967,
    "faradaic_efficiency": 0.02452157624065876,
    "ohmic_efficiency": 0.969560444355011,
    "pH_normalized": 0.22897005081176758,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.0
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
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.05
    },
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.2
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
    "cost": 0.285288006067276,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.5511128306388855,
    "energy_efficiency": 0.17957621812820435,
    "faradaic_efficiency": 0.352959543466568,
    "ohmic_efficiency": 0.9783982634544373,
    "pH_normalized": 0.22627469897270203,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.16236650943756104,
    "selective_product_yield": 0.011950265616178513,
    "transport_efficiency": 0.37921637296676636
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
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.05
    },
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "current_mA": 150,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.8
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
    "cost": 0.286296010017395,
    "electrochemical_conversion": 0.007090944796800613,
    "electrochemical_selectivity": 0.46084359288215637,
    "energy_efficiency": 0.08025605976581573,
    "faradaic_efficiency": 0.2434489130973816,
    "ohmic_efficiency": 0.9651718735694885,
    "pH_normalized": 0.22698970139026642,
    "precipitation_signal": 0.9871450662612915,
    "safety_risk": 0.05933958664536476,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.2600058317184448
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
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.05
    },
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "current_mA": 200,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -2.2
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
    "cost": 0.2881680130958557,
    "electrochemical_conversion": 0.017461217939853668,
    "electrochemical_selectivity": 0.4058813750743866,
    "energy_efficiency": 0.015131448395550251,
    "faradaic_efficiency": 0.25600674748420715,
    "ohmic_efficiency": 0.9753937125205994,
    "pH_normalized": 0.22629910707473755,
    "precipitation_signal": 0.987893283367157,
    "safety_risk": 0.05933958664536476,
    "score": 0.09977268427610397,
    "selective_product_yield": 0.01002192310988903,
    "transport_efficiency": 0.22451920807361603
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
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.05
    },
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -1.2
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
    "cost": 0.285288006067276,
    "electrochemical_conversion": 0.008675347082316875,
    "electrochemical_selectivity": 0.5811915993690491,
    "energy_efficiency": 0.1945199966430664,
    "faradaic_efficiency": 0.347199022769928,
    "ohmic_efficiency": 0.972093939781189,
    "pH_normalized": 0.20622022449970245,
    "precipitation_signal": 0.8436887264251709,
    "safety_risk": 0.05933958664536476,
    "score": 0.15699444711208344,
    "selective_product_yield": 0.011469269171357155,
    "transport_efficiency": 0.3366895616054535
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
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.05
    },
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -1.2
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
    "cost": 0.285288006067276,
    "electrochemical_conversion": 0.0068081095814704895,
    "electrochemical_selectivity": 0.5237982869148254,
    "energy_efficiency": 0.1913101226091385,
    "faradaic_efficiency": 0.3236064910888672,
    "ohmic_efficiency": 0.9675301313400269,
    "pH_normalized": 0.15415410697460175,
    "precipitation_signal": 0.0023995577357709408,
    "safety_risk": 0.05933958664536476,
    "score": 0.16449889540672302,
    "selective_product_yield": 0.012756717391312122,
    "transport_efficiency": 0.29892316460609436
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
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.05
    },
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": -1.2
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
    "cost": 0.285288006067276,
    "electrochemical_conversion": 0.014868145808577538,
    "electrochemical_selectivity": 0.5340339541435242,
    "energy_efficiency": 0.22055469453334808,
    "faradaic_efficiency": 0.29257363080978394,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.26957690715789795,
    "precipitation_signal": 0.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.1273851841688156,
    "selective_product_yield": 0.00971311330795288,
    "transport_efficiency": 0.2959739863872528
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
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.05
    },
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 2,
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
    "cost": 0.2994000017642975,
    "electrochemical_conversion": 0.32287517189979553,
    "electrochemical_selectivity": 0.5573267340660095,
    "energy_efficiency": 0.29533398151397705,
    "faradaic_efficiency": 0.35956448316574097,
    "ohmic_efficiency": 0.8224347829818726,
    "pH_normalized": 0.15147122740745544,
    "precipitation_signal": 0.00031451715040020645,
    "safety_risk": 0.05933958664536476,
    "score": 0.3535502851009369,
    "selective_product_yield": 0.16371408104896545,
    "transport_efficiency": 0.35306912660598755
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
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.05
    },
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -0.8
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
    "cost": 0.2965199947357178,
    "electrochemical_conversion": 0.35686272382736206,
    "electrochemical_selectivity": 0.5795647501945496,
    "energy_efficiency": 0.4605322778224945,
    "faradaic_efficiency": 0.3759628236293793,
    "ohmic_efficiency": 0.7867898344993591,
    "pH_normalized": 0.1534850001335144,
    "precipitation_signal": 0.008188718929886818,
    "safety_risk": 0.05933958664536476,
    "score": 0.4079706072807312,
    "selective_product_yield": 0.22843877971172333,
    "transport_efficiency": 0.3967941105365753
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
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.05
    },
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -0.6
    },
    {
      "duration_s": 10000,
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
    "electrochemical_conversion": 0.5605791807174683,
    "electrochemical_selectivity": 0.6348546147346497,
    "energy_efficiency": 0.43099847435951233,
    "faradaic_efficiency": 0.4298655390739441,
    "ohmic_efficiency": 0.6652643084526062,
    "pH_normalized": 0.15117086470127106,
    "precipitation_signal": 0.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.46385636925697327,
    "selective_product_yield": 0.3333132565021515,
    "transport_efficiency": 0.4312151074409485
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
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.05
    },
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -0.4
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
    "cost": 0.2965199947357178,
    "electrochemical_conversion": 0.7468767166137695,
    "electrochemical_selectivity": 0.635562002658844,
    "energy_efficiency": 0.34415608644485474,
    "faradaic_efficiency": 0.39534181356430054,
    "ohmic_efficiency": 0.5167897343635559,
    "pH_normalized": 0.15215590596199036,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.05933958664536476,
    "score": 0.49289458990097046,
    "selective_product_yield": 0.47404274344444275,
    "transport_efficiency": 0.4025217592716217
  }
}
```

### 批次 12 · 终点事件 85

```json
{
  "ordinal": 12,
  "lifecycle_index": 12,
  "end_step": 85,
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.05
    },
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -0.4
    },
    {
      "duration_s": 14400,
      "operation": "electrolyze"
    },
    {
      "duration_s": 4800,
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
    "cost": 0.31836000084877014,
    "electrochemical_conversion": 0.8120276927947998,
    "electrochemical_selectivity": 0.6329028606414795,
    "energy_efficiency": 0.31741246581077576,
    "faradaic_efficiency": 0.29893729090690613,
    "ohmic_efficiency": 0.5301382541656494,
    "pH_normalized": 0.15267622470855713,
    "precipitation_signal": 0.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.4989681541919708,
    "selective_product_yield": 0.549727737903595,
    "transport_efficiency": 0.32016223669052124
  }
}
```

## K1 封存报告

## Mechanistic account

I interpret this world as a potential-driven electrochemical conversion of an anonymous limiting reagent into a desired product, with parallel undesired electron-transfer and degradation pathways. The principal state variables are reagent concentration, applied potential and its sign, elapsed electrolysis time, effective current, electrolyte identity, solvent identity, proton activity, precipitation, and mass/charge transport. The public score combines conversion, selectivity, selective-product yield, faradaic efficiency, transport efficiency, ohmic efficiency, and energy efficiency, with selective-product yield carrying the largest weight and a stated 0.02 multiplicative gate.

All experiments used 0.020 mol reagent in 0.050 L solvent-S0, corresponding to a nominal initial concentration of 0.40 mol/L. Consequently, the conclusions mainly apply to that loading and solvent. Solvent effects were not experimentally identified.

## Proposed process model

A useful qualitative model is:

- The applied potential activates a productive electron-transfer channel only for the negative polarity tested.
- More negative overpotential increases the instantaneous reaction rate but also increases parasitic current, energetic loss, or undesired chemistry.
- Electrolysis time controls accumulated charge and therefore conversion.
- The commanded current is a cap rather than necessarily the realized current. A conceptual relation is

  I_actual = min(I_cap, I_kinetic(E), I_transport),

  where kinetic current depends strongly on potential and electrolyte-dependent standard-potential shifts, while transport current depends on diffusivity, diffusion-layer thickness, concentration, and solvent coupling.
- Product formation can be represented approximately by

  dn_product/dt = FE(E, materials, state) × I_actual/(zF) × S_product,

  where FE is faradaic efficiency and S_product represents product selectivity among faradaic pathways.
- Conversion grows with integrated productive and unproductive reaction, approximately

  X(t) = 1 − exp(−∫k_eff(E, materials, state)dt),

  although the experiments do not identify a specific kinetic order.
- Electrical energy input is proportional to ∫|E I_actual|dt. Energy efficiency should therefore fall if additional charge produces progressively less desired product.
- Ohmic efficiency is controlled by solution conductivity and cell resistance, while transport efficiency reflects the ratio between realized current and a mass-transfer limit.

Selective-product yield should approximately track conversion multiplied by electrochemical selectivity. This is reasonably visible at high signal: batch 11 had conversion 0.747 and selectivity 0.636, whose product is about 0.475, essentially its measured selective yield of 0.474. In batch 12 the corresponding product is about 0.514 versus measured yield 0.550, and in batch 10 it is about 0.356 versus 0.333. These discrepancies are plausible consequences of independent channel noise and process-proxy uncertainty rather than proof of a different mass-balance law.

## Evidence for potential-sign dependence

Batch 1 used S0/E0, +1.2 V, a 100 mA cap, and 600 s. Its final assay reported selective-product yield 0, electrochemical selectivity 0.010, faradaic efficiency 0.0245, transport efficiency 0, and score 0. Batch 2 changed only the sign to −1.2 V under the same declared conditions. It produced selective yield 0.0120, selectivity 0.551, faradaic efficiency 0.353, transport efficiency 0.379, and score 0.162.

This is the strongest evidence for polarity asymmetry. My preferred explanation is that the desired product is formed by the cathodic direction in the public sign convention, whereas positive potential activates essentially no productive pathway. An alternative is that a hidden interfacial or solvent reaction suppresses the target at positive potential. Only one positive-potential condition was tested, so the exact boundary between inactive and active polarity is unknown.

Increasing negative magnitude did not improve performance in the early series. Batch 3 used −1.8 V, 150 mA, and 1200 s with S0/E0 and returned zero measured selective yield and score, with selectivity 0.461, faradaic efficiency 0.243, transport efficiency 0.260, and energy efficiency 0.0803. Batch 4 used −2.2 V, 200 mA, and 1800 s and gave yield 0.0100 and score 0.0998, with selectivity 0.406 and energy efficiency only 0.0151. Compared with batch 2, these stronger negative potentials reduced selectivity and energy efficiency. Although current and time also changed, these outcomes support parasitic reactions or excessive energetic losses at large overpotential.

## Electrolyte coupling

Batches 2 and 5–7 compared electrolytes E0–E3 at S0, −1.2 V, 100 mA, and 600 s:

- Batch 2, E0: score 0.1624, yield 0.0120, selectivity 0.551, precipitation signal 1.000, normalized pH 0.226.
- Batch 5, E1: score 0.1570, yield 0.0115, selectivity 0.581, precipitation 0.844, normalized pH 0.206.
- Batch 6, E2: score 0.1645, yield 0.0128, selectivity 0.524, precipitation 0.0024, normalized pH 0.154.
- Batch 7, E3: score 0.1274, yield 0.0097, selectivity 0.534, precipitation 0, normalized pH 0.270.

The short-time scores were close and yields lay near or below the stated 0.02 scoring gate, so this is weak evidence for an intrinsic E2 advantage. Nevertheless, E2 combined acceptable faradaic and transport efficiencies with negligible observed precipitation and was selected for the longer experiments.

The electrolyte dossier alone does not explain the observed ordering. E2 nominally has conductivity 10.5 S/m, a relatively thick 1.65 mm diffusion layer, low diffusivity of 4.5×10⁻¹⁰ m²/s, and the strongest nominal precipitation tendency. Yet its measured precipitation signal was near zero, whereas E0 and E1 precipitated strongly. Possible explanations include hidden world-specific solvent/electrolyte residuals, potential-dependent availability of the precipitating species, pH coupling, or the low conversion of the short experiments. Because the material dossier explicitly allows bounded latent residuals and solvent coupling, I would not treat nominal precipitation constants as sufficient predictors in this world.

E3 illustrates a separate tradeoff: despite the highest nominal conductivity and no precipitation, it has the thickest nominal diffusion layer, and its batch-7 transport efficiency was only 0.296 with a lower score. Thus bulk conductivity alone is not enough; diffusion-layer and interfacial factors matter.

## Development of the preferred regime

The explanation changed substantially after batch 8. Early 600–1800 s runs produced only trace selective yield, suggesting that accumulated charge and residence time, not merely stronger voltage, were limiting conversion.

Using S0/E2 and a 500 mA cap:

- Batch 8, −1.0 V for 7200 s: conversion 0.323, selectivity 0.557, yield 0.164, faradaic efficiency 0.360, transport efficiency 0.353, ohmic efficiency 0.822, energy efficiency 0.295, score 0.354.
- Batch 9, −0.8 V for 7200 s: conversion 0.357, selectivity 0.580, yield 0.228, faradaic efficiency 0.376, transport efficiency 0.397, ohmic efficiency 0.787, energy efficiency 0.461, score 0.408.
- Batch 10, −0.6 V for 10000 s: conversion 0.561, selectivity 0.635, yield 0.333, faradaic efficiency 0.430, transport efficiency 0.431, ohmic efficiency 0.665, energy efficiency 0.431, score 0.464.
- Batch 11, −0.4 V for 14400 s: conversion 0.747, selectivity 0.636, yield 0.474, faradaic efficiency 0.395, transport efficiency 0.403, ohmic efficiency 0.517, energy efficiency 0.344, score 0.493.
- Batch 12, −0.4 V for 19200 s, applied as 14400 plus 4800 s: conversion 0.812, selectivity 0.633, yield 0.550, faradaic efficiency 0.299, transport efficiency 0.320, ohmic efficiency 0.530, energy efficiency 0.317, score 0.499.

The progression supports a low-overpotential, long-duration strategy. Milder potential preserves selectivity and productive charge efficiency, while additional time supplies enough total charge for substantial conversion. It also shows diminishing returns. Extending −0.4 V from 14400 to 19200 s increased conversion by about 0.065 and yield by about 0.076, but score rose by only 0.006. Faradaic efficiency fell from 0.395 to 0.299 and transport efficiency from 0.403 to 0.320. I therefore infer increasing substrate depletion, product-mediated inhibition, concentration polarization, or a growing fraction of current diverted to background reactions late in electrolysis.

The near-constant selectivity of batches 10–12, approximately 0.63–0.64, suggests that their principal tradeoff was conversion versus electrical/transport efficiency rather than a large change in product branching. The inability to exceed roughly 0.64 selectivity may reflect an intrinsic competing reaction, but the campaign did not identify that pathway.

## Ohmic and transport behavior

Ohmic efficiency decreased as the preferred series moved from −1.0 V to −0.4 V and longer times: 0.822 in batch 8, 0.787 in batch 9, 0.665 in batch 10, and about 0.52 in batches 11–12. This does not necessarily mean physical resistance increased monotonically; at smaller applied voltage a similar absolute ohmic drop consumes a larger fraction of the available voltage. Concentration changes during long electrolysis may also alter conductivity.

Transport efficiency remained around 0.35–0.43 through batch 11 and dropped to 0.320 in batch 12. That pattern is consistent with reactant depletion or a thickening diffusion layer during the extended final segment. The 500 mA setting should therefore be interpreted as a permissive current ceiling. There is no evidence that 500 mA actually flowed throughout the experiments.

Intermediate UV-visible estimates and final-assay estimates were similar in scale but not identical. For example, batch 10 UV-visible values for energy, faradaic, ohmic, and transport efficiency were 0.491, 0.437, 0.676, and 0.396, whereas the final assay reported 0.431, 0.430, 0.665, and 0.431. Batch 12 UV-visible values were 0.293, 0.375, 0.507, and 0.378, versus final values of 0.317, 0.299, 0.530, and 0.320. I regard these differences as measurement/process uncertainty, not resolved temporal trajectories, because both instruments are noisy synthetic snapshots and no replicate time series was performed.

## Proton activity and precipitation

Normalized pH depended strongly on electrolyte identity in the short screen but was stable near 0.151–0.153 for the long E2 series. Precipitation signals were essentially zero throughout batches 8–12. Thus the improved long-duration response cannot be attributed to a visible change in precipitation within E2; instead it appears to arise from accumulated conversion under a stable acid/solubility environment.

Precipitation could nevertheless suppress transport or active area in E0 and E1, where short-run signals were high. This remains conjectural because no electrode-surface measurement or paired long-duration E0/E1 experiment was performed.

## Safety and cost observations

The displayed safety risk was approximately 0.0593 for every completed batch, well below the 0.65 limit. No tested electrolysis condition visibly increased that metric. This only establishes safety within the benchmark’s reported state; it does not show that potential, current, gas formation, or heating would be harmless outside the tested range.

Longer electrolysis increased public cost modestly. Final cost was about 0.297 for batch 11 and 0.318 for batch 12. The small score improvement of batch 12 therefore came with both reduced electrochemical efficiencies and higher cost, making batch 11 a plausible efficiency-oriented alternative even though batch 12 had the highest formal score.

## What is identified and what is not

Reasonably supported within the tested domain:

1. Negative rather than positive potential is required for appreciable target formation.
2. Very negative potentials are inefficient and less selective under the early conditions.
3. At 0.40 mol/L loading in S0/E2, mild negative potential combined with long duration gives far higher conversion and yield than short, high-overpotential operation.
4. Late electrolysis shows diminishing efficiency, especially between batches 11 and 12.
5. Electrolyte selection affects pH, precipitation, transport, and score; E2 was the best tested platform for the subsequent optimization.

Not separately identifiable:

- Potential and duration effects in batches 8–11, because they were changed together except between batches 8 and 9.
- The effect of raising the current cap from 100 to 500 mA, because it coincided with longer times and changed potentials.
- Solvent effects, since only S0 was used.
- Reaction order, electron stoichiometry z, actual current-time traces, kinetic rate constants, exchange currents, electrode area, cell resistance, and diffusion-limited current.
- The identities and yields of individual byproducts.
- Whether declining late-stage efficiency is caused by depletion, product inhibition, electrode fouling, pH gradients, or background electrolysis.
- Repeatability. There were no exact replicate batches, so small differences—especially the 0.006 score difference between batches 11 and 12—are numerical observations rather than firm evidence of an effect.

## Plausible alternative explanations

The apparent improvement from −1.0 to −0.4 V could be driven mainly by longer duration rather than milder potential. A clean factorial design would be needed to separate these variables. Likewise, E2’s slight short-time score advantage may be noise; its importance is supported more by its successful later use than by the electrolyte screen alone. Because no other electrolyte received the same long-duration mild-potential treatment, E0, E1, or E3 could conceivably outperform E2 in that regime.

The zero yields in batches 1 and 3 may partly reflect channel clipping or measurement noise near zero rather than absolute absence of product. Nevertheless, their associated efficiency and selectivity patterns still make them clearly inferior to the long E2 runs.

## Overall interpretation

The world is best described as a cathodic conversion limited initially by delivered charge and later by declining faradaic and mass-transfer efficiency. Large negative overpotential accelerates nonproductive processes and wastes energy; milder negative potential maintains roughly 0.63 product selectivity, but requires long electrolysis to accumulate conversion. Electrolyte-dependent acid, conductivity, interfacial, and precipitation couplings determine how much of the commanded electrical input reaches the desired chemistry. Under the tested fixed-loading conditions, S0/E2 at −0.4 V with a 500 mA cap lies near the observed balance between conversion and efficiency. Batch 12 maximized the public score and yield, while batch 11 appears close to the practical knee of the response because it retained better faradaic and transport efficiency for almost the same score.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific prior or proposed response law was supplied. The supplied material dossier gave nominal conductivity, diffusivity, diffusion-layer, acidity, precipitation, capacitance, and potential-shift properties, but explicitly presented them as incomplete priors subject to hidden residuals. My principal laws were therefore self-developed.

Supported:
- Polarity asymmetry was strongly supported. Batch 1 at +1.2 V produced zero selective yield and score, whereas batch 2 at −1.2 V under otherwise matching conditions produced yield 0.0120, selectivity 0.551, and score 0.162. This changed my judgment from treating potential sign as an exploratory variable to treating negative polarity as necessary for the target pathway.
- Excessive negative overpotential appeared detrimental. Relative to batch 2, batches 3 and 4 at −1.8 and −2.2 V had poorer selectivity and energy efficiency and no score improvement. This supported a productive cathodic pathway accompanied by increasing parasitic loss at large overpotential.
- Accumulated charge/time was much more important than the early experiments suggested. Batch 8, at −1.0 V for 7200 s, increased yield to 0.164 and score to 0.354. That result caused the main revision: the trace yields in batches 1–7 were not simply a material-selection problem but largely reflected insufficient electrolysis time.
- A mild-potential, long-duration operating region was supported empirically. Batches 9–11 progressed from score 0.408 to 0.464 to 0.493 as potential became milder and duration increased. Batch 12 extended −0.4 V electrolysis to 19200 s and reached the highest observed yield, 0.550, and score, 0.499.
- Diminishing late-stage efficiency was supported. Compared with batch 11, batch 12 increased yield and conversion but reduced faradaic efficiency from 0.395 to 0.299 and transport efficiency from 0.403 to 0.320 for only a 0.006 score increase.

Partly supported or contradicted:
- My initial expectation of a clearly identifiable interior duration optimum was not established. Batch 12 still scored slightly higher than batch 11, so the tested range did not show a score decline; it showed diminishing returns and declining component efficiencies instead.
- My initial material expectation that nominal E0 transport properties might make S0/E0 attractive was weakened. In the short matched screen, E2 in batch 6 had the highest score and negligible precipitation, while E0 in batch 2 showed precipitation signal 1.0. However, the score difference was small and near the yield gate.
- The nominal precipitation ordering was not borne out directly. E2 had the strongest nominal precipitation tendency in the dossier but showed almost no precipitation in batches 6 and 8–12, whereas E0 and E1 showed large signals in batches 2 and 5. Hidden solvent coupling, reaction state, or benchmark residuals therefore outweighed a simple nominal-property ranking.

Untested or unresolved:
- Solvent effects were untested because every campaign batch used S0.
- A clean potential law was untested because potential and duration were usually changed together after batch 9.
- The effect of the 100 versus 500 mA cap was not isolated.
- No exact replicate tested repeatability, and no experiment identified kinetic order, electron stoichiometry, actual current, byproduct identity, or the cause of late efficiency loss.
- Other electrolytes were not tested in the successful mild-potential, long-duration regime, so E2 was not proven globally optimal.

2. One discriminating experiment

I would run the same loading and materials as batches 9–12—0.020 mol reagent in 0.050 L S0 with E2 and a 500 mA cap—but use −0.8 V for 14400 s. This would compare directly with batch 11 at −0.4 V for 14400 s, isolating potential at the same duration, while also extending the batch-9 −0.8 V condition from 7200 to 14400 s.

If −0.4 V retained higher selectivity and energy/faradaic efficiency at similar conversion or yield, it would support the leading explanation that mild overpotential intrinsically suppresses parasitic pathways. If −0.8 V produced substantially higher conversion, yield, and score without a major efficiency penalty, the alternative explanation—that duration, rather than milder potential, caused most of the batch 9–11 improvement—would become more credible. If −0.8 V raised conversion but lowered selectivity and efficiency, I would retain the overpotential tradeoff model but revise the optimum according to whether the score favored the extra conversion. A result indistinguishable from batch 11 would leave the potential effect unresolved because there was no exact replication-based noise estimate.

3. Unused evidence, reliability, and goal effects

Unused or underused evidence included the detailed raw UV-visible spectra, calibration traces, and final-assay spectral artifacts; I relied mainly on processed estimates. Intermediate UV-visible measurements were collected in every batch but were used chiefly as qualitative consistency checks rather than to fit a time-dependent model. Cost and safety were recorded, but safety remained near 0.0593 and did not discriminate conditions. I also did not exploit dedicated pH-meter measurements, exact current-time traces were unavailable, and the solvent-property dossier could not be tested because S1–S3 were never used.

The recommendation of batch 12 is less robust than its ranking implies. Its score exceeded batch 11 by only 0.006 without replication, while batch 11 had appreciably better faradaic and transport efficiencies. Thus batch 11 remains a credible alternative if repeatability, cost, or component efficiency matters.

The least reliable blind predictions are Q09 and Q10 because S2 was never experimentally tested. Q11 is also uncertain because it combines a smaller volume and different concentration with the 500 mA cap under E0, a long-duration regime not observed for E0. More generally, all predictions extrapolate from 0.020 mol/0.050 L to 0.012 mol/0.025 L. The near-zero positive-potential predictions are supported by batch 1, but their extension to long durations and other materials remains untested.

The score-maximization goal did affect evidence collection. After batch 8 revealed the importance of long duration, I allocated the remaining batches to exploiting and refining that region rather than completing a balanced solvent screen, exact replicates, or a factorial separation of potential, current, and time. This improved the observed best score but weakened causal identification and prediction reliability outside S0/E2. There was no clear conflict with safety because all observed risks remained far below the stated limit, but there was a tradeoff between maximizing the campaign score and collecting broadly generalizable mechanistic evidence.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.59,
        "lower80": 0.48,
        "upper80": 0.7
      },
      "energy_efficiency": {
        "estimate": 0.38,
        "lower80": 0.26,
        "upper80": 0.5
      },
      "faradaic_efficiency": {
        "estimate": 0.39,
        "lower80": 0.3,
        "upper80": 0.48
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.17,
        "lower80": 0.08,
        "upper80": 0.25
      },
      "selective_product_yield": {
        "estimate": 0.011,
        "lower80": 0,
        "upper80": 0.03
      },
      "transport_efficiency": {
        "estimate": 0.41,
        "lower80": 0.3,
        "upper80": 0.51
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.015,
        "lower80": 0,
        "upper80": 0.055
      },
      "energy_efficiency": {
        "estimate": 0.008,
        "lower80": 0,
        "upper80": 0.035
      },
      "faradaic_efficiency": {
        "estimate": 0.02,
        "lower80": 0,
        "upper80": 0.06
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.003,
        "lower80": 0,
        "upper80": 0.025
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0,
        "upper80": 0.012
      },
      "transport_efficiency": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.05
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.5,
        "upper80": 0.69
      },
      "energy_efficiency": {
        "estimate": 0.42,
        "lower80": 0.3,
        "upper80": 0.55
      },
      "faradaic_efficiency": {
        "estimate": 0.4,
        "lower80": 0.3,
        "upper80": 0.49
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.416,
        "lower80": 0.32,
        "upper80": 0.5
      },
      "selective_product_yield": {
        "estimate": 0.22,
        "lower80": 0.14,
        "upper80": 0.31
      },
      "transport_efficiency": {
        "estimate": 0.4,
        "lower80": 0.28,
        "upper80": 0.5
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.018,
        "lower80": 0,
        "upper80": 0.065
      },
      "energy_efficiency": {
        "estimate": 0.007,
        "lower80": 0,
        "upper80": 0.035
      },
      "faradaic_efficiency": {
        "estimate": 0.019,
        "lower80": 0,
        "upper80": 0.06
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.005,
        "lower80": 0,
        "upper80": 0.03
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.05
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.51,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.44,
        "lower80": 0.31,
        "upper80": 0.57
      },
      "faradaic_efficiency": {
        "estimate": 0.39,
        "lower80": 0.29,
        "upper80": 0.49
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.408,
        "lower80": 0.31,
        "upper80": 0.5
      },
      "selective_product_yield": {
        "estimate": 0.21,
        "lower80": 0.13,
        "upper80": 0.31
      },
      "transport_efficiency": {
        "estimate": 0.36,
        "lower80": 0.25,
        "upper80": 0.47
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.018,
        "lower80": 0,
        "upper80": 0.065
      },
      "energy_efficiency": {
        "estimate": 0.008,
        "lower80": 0,
        "upper80": 0.04
      },
      "faradaic_efficiency": {
        "estimate": 0.02,
        "lower80": 0,
        "upper80": 0.065
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.005,
        "lower80": 0,
        "upper80": 0.032
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0,
        "upper80": 0.016
      },
      "transport_efficiency": {
        "estimate": 0.011,
        "lower80": 0,
        "upper80": 0.055
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.57,
        "lower80": 0.45,
        "upper80": 0.68
      },
      "energy_efficiency": {
        "estimate": 0.46,
        "lower80": 0.32,
        "upper80": 0.59
      },
      "faradaic_efficiency": {
        "estimate": 0.33,
        "lower80": 0.23,
        "upper80": 0.44
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.382,
        "lower80": 0.28,
        "upper80": 0.48
      },
      "selective_product_yield": {
        "estimate": 0.18,
        "lower80": 0.1,
        "upper80": 0.28
      },
      "transport_efficiency": {
        "estimate": 0.33,
        "lower80": 0.22,
        "upper80": 0.44
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.02,
        "lower80": 0,
        "upper80": 0.07
      },
      "energy_efficiency": {
        "estimate": 0.009,
        "lower80": 0,
        "upper80": 0.045
      },
      "faradaic_efficiency": {
        "estimate": 0.02,
        "lower80": 0,
        "upper80": 0.065
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.005,
        "lower80": 0,
        "upper80": 0.035
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0,
        "upper80": 0.017
      },
      "transport_efficiency": {
        "estimate": 0.012,
        "lower80": 0,
        "upper80": 0.06
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.56,
        "lower80": 0.41,
        "upper80": 0.69
      },
      "energy_efficiency": {
        "estimate": 0.31,
        "lower80": 0.17,
        "upper80": 0.46
      },
      "faradaic_efficiency": {
        "estimate": 0.34,
        "lower80": 0.22,
        "upper80": 0.46
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.37,
        "lower80": 0.25,
        "upper80": 0.49
      },
      "selective_product_yield": {
        "estimate": 0.2,
        "lower80": 0.1,
        "upper80": 0.32
      },
      "transport_efficiency": {
        "estimate": 0.43,
        "lower80": 0.28,
        "upper80": 0.57
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.018,
        "lower80": 0,
        "upper80": 0.07
      },
      "energy_efficiency": {
        "estimate": 0.007,
        "lower80": 0,
        "upper80": 0.04
      },
      "faradaic_efficiency": {
        "estimate": 0.018,
        "lower80": 0,
        "upper80": 0.065
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.004,
        "lower80": 0,
        "upper80": 0.035
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0,
        "upper80": 0.017
      },
      "transport_efficiency": {
        "estimate": 0.012,
        "lower80": 0,
        "upper80": 0.06
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.59,
        "lower80": 0.48,
        "upper80": 0.69
      },
      "energy_efficiency": {
        "estimate": 0.39,
        "lower80": 0.26,
        "upper80": 0.52
      },
      "faradaic_efficiency": {
        "estimate": 0.36,
        "lower80": 0.26,
        "upper80": 0.47
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.488,
        "lower80": 0.38,
        "upper80": 0.59
      },
      "selective_product_yield": {
        "estimate": 0.44,
        "lower80": 0.28,
        "upper80": 0.6
      },
      "transport_efficiency": {
        "estimate": 0.36,
        "lower80": 0.24,
        "upper80": 0.48
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.012,
        "lower80": 0,
        "upper80": 0.055
      },
      "energy_efficiency": {
        "estimate": 0.004,
        "lower80": 0,
        "upper80": 0.03
      },
      "faradaic_efficiency": {
        "estimate": 0.015,
        "lower80": 0,
        "upper80": 0.055
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.003,
        "lower80": 0,
        "upper80": 0.03
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.008,
        "lower80": 0,
        "upper80": 0.05
      }
    }
  ],
  "rationale": "Predictions use the campaign’s strong polarity asymmetry: negative potentials produced selective conversion, whereas +1.2 V gave essentially zero target yield, so all positive-potential queries are forecast near zero. Negative 7200 s runs are extrapolated from the observed −0.8 V long-duration regime, adjusted for the smaller 0.012 mol charge basis, the 100 versus 500 mA cap, and electrolyte or solvent transport/precipitation differences. E1 is expected to retain slightly higher selectivity, E3 somewhat lower charge efficiency, and S2 to reduce precipitation but incur poorer conductivity. Intervals are deliberately broad because concentration and solvent are extrapolations, potential/current/time were partly confounded in the campaign, and there were no exact replicates."
}
```
