# repeat-01/EC-W01-B12-optimization-E-Aligned

既有科学公开材料；非provider内部推理。

来源：D:\Projects\ChemWorld-local-research\20261016-unified-matrices\attempt-01\repeat-01\EC-W01-B12-optimization-E-Aligned\participant\optimization-E-Aligned

## 同期笔记

### v1 · 公开事件 0

# Electrochemical campaign hypotheses

## H1 [tentative]
At fixed loading, electrolyte E1 with solvent S1 may offer the best balanced score because their relatively high diffusivity and thinner diffusion layer should improve transport while retaining adequate conductivity. E0/S0 may instead maximize ohmic efficiency but could be transport-limited.

## H2 [tentative]
There should be a moderate absolute potential and duration optimum: insufficient driving force gives low conversion/yield, whereas excessive potential or time lowers selectivity, faradaic efficiency, energy efficiency, and possibly safety. Potential sign could reverse productive direction, so both signs must be tested.

## H3 [tentative]
Current caps above the transport-supported current may not increase delivered conversion and could reduce efficiency; a moderate cap should outperform the highest cap.

Testable plan: begin with a broad factorial-style screen across solvent/electrolyte, potential sign/magnitude, time, and current cap, then use later batches to refine and replicate the best region. A UV-vis intermediate measurement may diagnose efficiency but final assay remains authoritative.

### v2 · 公开事件 84

# Electrochemical campaign hypotheses

## H1 [supported in tested scope]
E1/S1 is the strongest tested material pair for balanced performance. At long electrolysis and a high current cap it outperformed the matched E0/S0, E2/S2, E3/S3, and E1/S2 tests (final-assay events runner-operation-0042, -0049, -0056, -0063, and -0070). The comparison is not a complete cross-factorial survey, so solvent/electrolyte interactions remain unresolved. E0/S0 also showed severe precipitation and transport loss (event -0049).

## H2 [supported locally; global optimum unresolved]
For E1/S1 at a 500 mA cap, extending electrolysis from 7200 to 12000 to 14400 s increased score and selective-product yield across events runner-operation-0028, -0035, and -0042. At 14400 s, raising potential from 1.0 to 1.1 and 1.2 V further improved observed score from 0.7957 to 0.8079 and 0.8117 (events -0042, -0077, -0084). However, 1.5 V at 14400 s collapsed all productive metrics (event -0021), supporting a sharp high-potential degradation/inefficiency region. The optimum between 1.2 and 1.5 V was not resolved.

## H3 [partially supported]
The negative-potential control was weak (event runner-operation-0014) relative to the positive-potential baseline (event -0007), establishing productive polarity in the tested E1/S1 conditions. The campaign did not independently isolate the current-cap response because duration and cap changed together in early tests; any claim of a cap optimum is therefore suspended.

## Decision
Recommend completed batch 12: 0.04 mol reagent, 0.08 L S1, E1, +1.2 V, 500 mA cap, 14400 s. It had the highest observed balanced score (0.8117) and selective-product yield (0.753), with high selectivity (0.964), while remaining well below the safety limit. Batch 11 was close, so the small numerical advantage over 1.1 V should not be treated as definitive beyond this campaign's assay noise.

## 实际批次及公开测量

### 批次 1 · 终点事件 7

```json
{
  "ordinal": 1,
  "lifecycle_index": 1,
  "end_step": 7,
  "actions": [
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.08
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 1,
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
    "cost": 0.3856399953365326,
    "electrochemical_conversion": 0.04693983867764473,
    "electrochemical_selectivity": 0.9193423390388489,
    "energy_efficiency": 0.8825672268867493,
    "faradaic_efficiency": 0.8591352701187134,
    "ohmic_efficiency": 0.9560058116912842,
    "pH_normalized": 0.20561343431472778,
    "precipitation_signal": 0.7280349135398865,
    "safety_risk": 0.09559440612792969,
    "score": 0.5439810752868652,
    "selective_product_yield": 0.0212694238871336,
    "transport_efficiency": 0.8304314613342285
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.08
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 1,
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
    "cost": 0.3856399953365326,
    "electrochemical_conversion": 0.007781770545989275,
    "electrochemical_selectivity": 0.589622437953949,
    "energy_efficiency": 0.2943866550922394,
    "faradaic_efficiency": 0.33917853236198425,
    "ohmic_efficiency": 0.9648436307907104,
    "pH_normalized": 0.20291808247566223,
    "precipitation_signal": 0.7310672998428345,
    "safety_risk": 0.09559440612792969,
    "score": 0.2661704123020172,
    "selective_product_yield": 0.01815265789628029,
    "transport_efficiency": 0.3654353618621826
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
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
    "cost": 0.42739999294281006,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.0,
    "ohmic_efficiency": 0.8702905774116516,
    "pH_normalized": 0.20363308489322662,
    "precipitation_signal": 0.7135193943977356,
    "safety_risk": 0.09559440612792969,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.0
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 1
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
    "cost": 0.3986000120639801,
    "electrochemical_conversion": 0.41067710518836975,
    "electrochemical_selectivity": 0.9092791676521301,
    "energy_efficiency": 0.7351423501968384,
    "faradaic_efficiency": 0.9169024229049683,
    "ohmic_efficiency": 0.8243581652641296,
    "pH_normalized": 0.20294250547885895,
    "precipitation_signal": 0.7142676115036011,
    "safety_risk": 0.09559440612792969,
    "score": 0.6691104173660278,
    "selective_product_yield": 0.3895367383956909,
    "transport_efficiency": 0.8854148387908936
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 12000,
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
    "cost": 0.4081999957561493,
    "electrochemical_conversion": 0.6864871382713318,
    "electrochemical_selectivity": 0.944394588470459,
    "energy_efficiency": 0.7466042041778564,
    "faradaic_efficiency": 0.8897330164909363,
    "ohmic_efficiency": 0.8237923979759216,
    "pH_normalized": 0.20790329575538635,
    "precipitation_signal": 0.7135940194129944,
    "safety_risk": 0.09559440612792969,
    "score": 0.7776303291320801,
    "selective_product_yield": 0.6491268873214722,
    "transport_efficiency": 0.8792235851287842
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 1
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
    "cost": 0.4129999876022339,
    "electrochemical_conversion": 0.7584835290908813,
    "electrochemical_selectivity": 0.9422012567520142,
    "energy_efficiency": 0.7692043781280518,
    "faradaic_efficiency": 0.8348889946937561,
    "ohmic_efficiency": 0.8256491422653198,
    "pH_normalized": 0.20462734997272491,
    "precipitation_signal": 0.7242242693901062,
    "safety_risk": 0.09559440612792969,
    "score": 0.7957420945167542,
    "selective_product_yield": 0.7197456359863281,
    "transport_efficiency": 0.8102056980133057
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 0.8
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
    "cost": 0.3752399981021881,
    "electrochemical_conversion": 0.15102747082710266,
    "electrochemical_selectivity": 0.9370536208152771,
    "energy_efficiency": 0.18583811819553375,
    "faradaic_efficiency": 0.15296855568885803,
    "ohmic_efficiency": 0.8982177376747131,
    "pH_normalized": 0.23021826148033142,
    "precipitation_signal": 0.982570469379425,
    "safety_risk": 0.072194404900074,
    "score": 0.33121198415756226,
    "selective_product_yield": 0.13941644132137299,
    "transport_efficiency": 0.1563689261674881
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": 1.38
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
    "cost": 0.47514399886131287,
    "electrochemical_conversion": 0.6933988928794861,
    "electrochemical_selectivity": 0.826651930809021,
    "energy_efficiency": 0.6629050970077515,
    "faradaic_efficiency": 0.7567878365516663,
    "ohmic_efficiency": 0.8188942670822144,
    "pH_normalized": 0.16625024378299713,
    "precipitation_signal": 0.00031451715040020645,
    "safety_risk": 0.1135944053530693,
    "score": 0.6922339797019958,
    "selective_product_yield": 0.5603506565093994,
    "transport_efficiency": 0.7502924799919128
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 3,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": 1.38
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
    "cost": 0.4431439936161041,
    "electrochemical_conversion": 0.08684289455413818,
    "electrochemical_selectivity": 0.9563625454902649,
    "energy_efficiency": 0.14776411652565002,
    "faradaic_efficiency": 0.08648558706045151,
    "ohmic_efficiency": 0.9530231952667236,
    "pH_normalized": 0.2855640947818756,
    "precipitation_signal": 0.008188718929886818,
    "safety_risk": 0.12619440257549286,
    "score": 0.3025282919406891,
    "selective_product_yield": 0.1029106080532074,
    "transport_efficiency": 0.10731685906648636
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 1.2
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
    "cost": 0.4699600040912628,
    "electrochemical_conversion": 0.6559622287750244,
    "electrochemical_selectivity": 0.8878943920135498,
    "energy_efficiency": 0.7336404323577881,
    "faradaic_efficiency": 0.695780873298645,
    "ohmic_efficiency": 0.8166846632957458,
    "pH_normalized": 0.2139255702495575,
    "precipitation_signal": 0.5786512494087219,
    "safety_risk": 0.1135944053530693,
    "score": 0.6936122179031372,
    "selective_product_yield": 0.554147481918335,
    "transport_efficiency": 0.6971304416656494
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 1.1
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
    "cost": 0.4158799946308136,
    "electrochemical_conversion": 0.7697845101356506,
    "electrochemical_selectivity": 0.9506983757019043,
    "energy_efficiency": 0.8202848434448242,
    "faradaic_efficiency": 0.8130375742912292,
    "ohmic_efficiency": 0.8442196249961853,
    "pH_normalized": 0.20262913405895233,
    "precipitation_signal": 0.7270644307136536,
    "safety_risk": 0.09559440612792969,
    "score": 0.8078938722610474,
    "selective_product_yield": 0.7271469831466675,
    "transport_efficiency": 0.8202175498008728
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 1.2
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
    "cost": 0.4187600016593933,
    "electrochemical_conversion": 0.7399243116378784,
    "electrochemical_selectivity": 0.9638054370880127,
    "energy_efficiency": 0.8300955891609192,
    "faradaic_efficiency": 0.7767208218574524,
    "ohmic_efficiency": 0.8707705140113831,
    "pH_normalized": 0.2031494528055191,
    "precipitation_signal": 0.7204003930091858,
    "safety_risk": 0.09559440612792969,
    "score": 0.8116751909255981,
    "selective_product_yield": 0.7531164288520813,
    "transport_efficiency": 0.7979457378387451
  }
}
```

## K1 封存报告

Mechanistic report

1. Proposed picture of the system

I interpret this world as a charge-driven electrochemical conversion with four coupled layers: electrode kinetics, mass transport, ohmic loss, and competing reactions or degradation. The observed selective-product yield is controlled not only by conversion, but also by electrochemical selectivity and faradaic efficiency. The public balanced score then rewards yield most strongly while also rewarding conversion, selectivity, faradaic efficiency, transport efficiency, ohmic efficiency, and energy efficiency.

A useful qualitative decomposition is:

I_delivered = min(I_cap, I_kinetic(V - V_eq), I_transport)

Q = integral(I_delivered dt)

conversion ≈ f(Q / n_reagent),

productive rate ≈ I_delivered × FE × selectivity,

while side-reaction or degradation rates rise strongly beyond a favorable potential window. Ohmic loss depends on conductivity and cell resistance; transport limitation depends on diffusivity, diffusion-layer thickness, concentration, and solvent factors. This is a conceptual model, not a fitted law.

The material dossier supports such a decomposition. E1 has relatively high nominal diffusivity (1.25×10^-9 m²/s) and a thin diffusion layer (0.95 mm), but only moderate conductivity (5.8 S/m). S1 multiplies diffusivity by 1.25 while multiplying conductivity by 0.7. Thus E1/S1 plausibly favors transport at the cost of some resistance. In contrast, E0/S0 has higher nominal conductivity but lower effective diffusivity, a thicker E0 diffusion layer, and a much stronger precipitation tendency. E3 has high conductivity but a very thick nominal diffusion layer (2.8 mm), which predicts good ohmic behavior but poor mass transport. These nominal properties are only priors because fixed hidden solvent–electrolyte and world-specific residuals were declared to exist.

2. Productive polarity and potential dependence

The reaction clearly favored positive potential under the tested E1/S1 conditions. Batch 1 used +1.0 V, a 100 mA current cap, and 3600 s. Its final assay gave conversion 0.0469, selectivity 0.9193, selective-product yield 0.0213, and score 0.5440. Batch 2 changed the potential to -1.0 V while retaining the same material pair, cap, and duration. It gave conversion 0.00778, selectivity 0.5896, yield 0.0182, and score 0.2662. This supports a productive anodic-versus-cathodic polarity in the benchmark coordinates. It does not identify a real oxidation state or molecular reaction.

Potential was not monotonically beneficial. Batch 3 used E1/S1 at +1.5 V, 500 mA, and 14400 s. Its final assay reported zero conversion, yield, selectivity, faradaic efficiency, transport efficiency, and energy efficiency, although ohmic efficiency remained 0.8703. This is strong evidence that excessive potential and long exposure enter an unproductive regime. Plausible mechanisms include substrate or product degradation, dominant solvent/electrolyte side reactions, electrode passivation, or a benchmark-level selectivity collapse. Because no degradation-specific observable was exposed in the final result, these alternatives cannot be distinguished.

At 14400 s with E1/S1 and a 500 mA cap, the observed potential series was:

• Batch 6, +1.0 V: score 0.7957, conversion 0.7585, selectivity 0.9422, yield 0.7197, FE 0.8349, transport efficiency 0.8102, energy efficiency 0.7692.
• Batch 11, +1.1 V: score 0.8079, conversion 0.7698, selectivity 0.9507, yield 0.7271, FE 0.8130, transport efficiency 0.8202, energy efficiency 0.8203.
• Batch 12, +1.2 V: score 0.8117, conversion 0.7399, selectivity 0.9638, yield 0.7531, FE 0.7767, transport efficiency 0.7979, energy efficiency 0.8301.
• Batch 3, +1.5 V: score and productive metrics 0.

The local data therefore suggest a broad useful region around +1.0 to +1.2 V followed by a severe collapse before or at +1.5 V. Increasing potential from 1.0 to 1.2 V improved selectivity, energy efficiency, ohmic efficiency, and the measured yield/score, while measured conversion and FE peaked earlier. This tradeoff explains why +1.2 V won the balanced objective even though it did not maximize every component.

The exact optimum between 1.2 and 1.5 V is unidentifiable. No batch tested 1.25–1.4 V in E1/S1, and the small score difference between batches 11 and 12 is not decisive relative to the stated measurement noise. Batch 12’s yield (0.7531) was also slightly larger than its independently calibrated conversion estimate (0.7399). I treat that as assay noise or channel-calibration inconsistency rather than literal stoichiometry; a strict identity such as yield = conversion × selectivity is not supported exactly by these noisy synthetic channels.

3. Charge, duration, and current-cap effects

For E1/S1 at +1.0 V and a 500 mA cap, increasing duration produced a strong monotonic rise in conversion and yield over the sampled range:

• Batch 4, 7200 s: conversion 0.4107, yield 0.3895, score 0.6691.
• Batch 5, 12000 s: conversion 0.6865, yield 0.6491, score 0.7776.
• Batch 6, 14400 s: conversion 0.7585, yield 0.7197, score 0.7957.

The increments diminished at longer time, consistent with reactant depletion, decreasing concentration at the interface, product inhibition, transport limitation, or an approach to a kinetic ceiling. A saturating form such as conversion = 1 - exp(-k_eff t) could describe the trend locally, but three points are insufficient to select that equation over alternatives.

Faradaic efficiency decreased from 0.9169 in batch 4 to 0.8897 in batch 5 and 0.8349 in batch 6. Transport efficiency also fell from 0.8854 to 0.8792 to 0.8102. Thus later charge was progressively less productive, even though total yield continued to increase. This supports a process in which depletion strengthens transport limitation and/or side reactions late in electrolysis.

The campaign did not independently identify the current-cap law. Batch 1 used 100 mA for 3600 s, whereas the duration series used 500 mA for longer times. Therefore, the improvement cannot be assigned solely to the higher cap. The 500 mA setting may merely have stopped being limiting while the actual current was set by kinetics, resistance, or transport. An independent cap sweep at fixed potential and duration would have been required to estimate I_delivered(I_cap).

4. Material and solvent couplings

E1/S1 was the best tested pair, but the material screen was deliberately sparse and partially confounded by potential matching.

Batch 7 tested E0/S0 at +0.8 V, 500 mA, and 14400 s. It produced score 0.3312, conversion 0.1510, yield 0.1394, FE 0.1530, transport efficiency 0.1564, and ohmic efficiency 0.8982. Its precipitation signal was extremely high at 0.9826. This combination of good ohmic efficiency with poor transport and FE is consistent with an electrically conductive system whose accessible electrode process is blocked or mass-transfer-limited, plausibly by precipitation. The high precipitation signal is correlated with the failure but does not prove causality.

Batch 8 tested E2/S2 at +1.38 V, 500 mA, and 14400 s. It gave score 0.6922, conversion 0.6934, yield 0.5604, selectivity 0.8267, FE 0.7568, transport efficiency 0.7503, and precipitation signal only 0.000315. This pair avoided precipitation and converted substantial reactant, but lower selectivity and efficiencies kept it behind E1/S1.

Batch 9 tested E3/S3 at +1.38 V, 500 mA, and 14400 s. It retained high selectivity (0.9564) and ohmic efficiency (0.9530), but conversion was only 0.0868, yield 0.1029, FE 0.0865, and transport efficiency 0.1073; score was 0.3025. This is the cleanest support for a transport bottleneck largely independent of bulk resistance: E3’s high nominal conductivity can explain good ohmic efficiency, while its thick diffusion layer and the low S3 diffusivity factor can explain poor transport and current utilization.

Batch 10 isolated part of the solvent effect by combining E1 with S2 at +1.2 V, 500 mA, and 14400 s. It achieved conversion 0.6560, yield 0.5541, selectivity 0.8879, FE 0.6958, transport efficiency 0.6971, and score 0.6936. Under otherwise similar settings, batch 12’s E1/S1 combination gave higher values for all of these performance measures. This directly supports a beneficial S1–E1 coupling or, more simply, the higher nominal diffusivity of S1. However, solvent effects on formal potential, proton activity, conductivity, solvation, and hidden residuals changed simultaneously, so diffusivity cannot be identified as the sole cause.

The potentials for batches 7–9 were chosen with the nominal material potential shifts in mind, but the assumption that these shifts add linearly to a single equilibrium potential was not experimentally validated. Consequently, comparisons across E0/S0, E2/S2, E3/S3, and E1/S1 include a possible mismatch in true overpotential.

5. Acid/base state and precipitation

Final normalized pH values depended on material pair: approximately 0.203 for E1/S1 in batch 12, 0.230 for E0/S0 in batch 7, 0.166 for E2/S2 in batch 8, and 0.286 for E3/S3 in batch 9. This is qualitatively compatible with the declared differences in acid concentration, pKa, and solvent proton activity. However, the campaign did not vary pH independently, so its causal effect on kinetics or selectivity is not identifiable.

Precipitation also varied strongly: about 0.72 for E1/S1, 0.983 for E0/S0, 0.0003 for E2/S2, and 0.0082 for E3/S3. Complete suppression of precipitation was not sufficient for high score, as shown by batches 8 and 9. Conversely, E1/S1 performed best despite a substantial precipitation signal. I therefore infer that precipitation is one constraint among several, not a universal proxy for performance. Moderate precipitation may be tolerated, spatially separated from the active interface, or partly an equilibrium indicator rather than direct electrode blockage.

6. Efficiency relationships and score behavior

The score behaves consistently with the published weighted objective. Yield dominated the ranking: the rise from batch 4 to batches 5–6 substantially increased score, even as some efficiency terms fell. Batch 12 then obtained the highest score by combining high measured yield and selectivity with strong energy and ohmic efficiency. The selective-product-yield gate also explains why batch 1, with yield barely above 0.02, scored much lower despite several high efficiency estimates.

Ohmic efficiency alone was a poor predictor. Batch 9 had the highest observed ohmic efficiency among the material-screen examples (0.9530) but a low score because FE and transport were near 0.1. Likewise, batch 3 retained ohmic efficiency of 0.8703 after productive metrics collapsed. Transport and faradaic efficiencies were more diagnostic of whether charge was reaching the desired pathway, while conversion and yield integrated those efficiencies over time.

A plausible pseudocode representation is:

eta_ohm = g(conductivity, solvent factor, fixed cell resistance, current)
I_transport = h(diffusivity, diffusion-layer thickness, concentration, precipitation, hidden coupling)
overpotential = applied potential - material-dependent equilibrium potential - I×R
I_product = min(I_cap, I_kinetic(overpotential), I_transport) × FE(overpotential, composition, time)
d(product)/dt = I_product × selectivity / (nF)
d(reactant)/dt = -total electrochemical consumption
side reactions and degradation increase at excessive overpotential and with exposure

This representation explains the principal observations, but it is not uniquely established.

7. Safety and cost scope

All tested batches remained below the public safety limit of 0.65. Representative risks were 0.0956 for S1-containing batches, 0.0722 for E0/S0, 0.1136 for S2-containing batches, and 0.1262 for E3/S3. Since no experiment approached the limit, I cannot infer the form of any high-risk penalty or whether risk would rise nonlinearly at potentials beyond those tested. Potential and electrolysis did not visibly raise the reported risk in these experiments; composition additions appeared to dominate the public risk measure.

Cost varied with solvent, potential, time, and measurement, but the score was the stated primary objective and cost was not a weighted score component in the supplied scoring contract. No economic optimum was identified.

8. What changed the explanation

The initial expectation that E1/S1 might balance transport and conductivity was supported by batches 4–6 and the material comparisons. Batch 2 established productive potential polarity. Batch 3 decisively rejected a simple monotonic “more potential and more time is better” model and introduced the high-potential failure region. Batches 4–6 established a saturating time/charge response and declining marginal FE/transport performance. Batches 7 and 9 separated ohmic quality from transport/productivity, showing that conductivity alone is insufficient. Batch 8 showed that suppressing precipitation alone is also insufficient. Batch 10 provided the most direct evidence favoring S1 over S2 with E1. Batches 11 and 12 narrowed the favorable E1/S1 potential region toward 1.1–1.2 V.

9. Limits and plausible alternatives

The principal unidentifiable quantities are actual current versus time, electron stoichiometry, true equilibrium potential, kinetic transfer coefficients, electrode area, cell resistance, concentration profiles, product stability, and the declared fixed latent material residuals. Intermediate UV-visible measurements reported efficiency proxies but did not provide direct current or concentration trajectories. Final assay noise and independent calibration prevent exact mass-action identities from being enforced.

The collapse at batch 3 could result from chemical degradation, electrochemical side reactions, passivation, gas evolution, or a synthetic benchmark threshold. The poor E0/S0 and E3/S3 outcomes could be caused by transport limits, unfavorable hidden interface kinetics, or overpotential mismatch rather than nominal properties alone. E1/S1 may be best intrinsically, or it may simply have received the most thorough local optimization. Since the screen did not cross every solvent with every electrolyte or replicate the leading batches, global material optimality and small differences such as batch 12 versus batch 11 remain uncertain.

Within the tested scope, the strongest defensible conclusion is that productive conversion requires positive polarization, sufficient charge, and a transport-capable medium, but excessive potential destroys efficiency. E1/S1 at approximately +1.1 to +1.2 V and long electrolysis occupied the best observed balance; batch 12 was the highest observed point, not proof of the exact global optimum.

## K2 封存报告

1. Claims, tests, and evidence that changed the assessment

No instance-specific prior, expected optimum, or supplied response law was provided. The material dossier supplied only nominal mechanistic priors—conductivity, diffusivity, diffusion-layer thickness, acid/base properties, precipitation tendency, capacitance, and potential shifts—plus a warning that hidden fixed residuals and solvent–electrolyte couplings existed.

Supported claims:
• Productive polarity was positive in the tested region. Batch 1 (+1.0 V, E1/S1) substantially outperformed batch 2 (-1.0 V) in conversion, selectivity, efficiencies, and score. This was the clearest polarity evidence.
• Conversion and yield increase with electrolysis duration over a local range. At E1/S1, +1.0 V, and a 500 mA cap, batches 4, 5, and 6 increased from 7200 to 12000 to 14400 s; conversion rose from 0.411 to 0.686 to 0.758 and yield from 0.390 to 0.649 to 0.720.
• Marginal charge utilization deteriorates late in a run. Across batches 4–6, faradaic efficiency fell from 0.917 to 0.890 to 0.835, while transport efficiency ultimately fell from 0.885 to 0.810. This supported depletion, increasing transport limitation, or growing side reactions.
• Conductivity alone does not determine performance. Batch 9 had high ohmic efficiency (0.953) but very low transport efficiency (0.107), FE (0.086), conversion (0.087), and score (0.303). This was consistent with the nominally thick E3 diffusion layer.
• Avoiding precipitation alone is insufficient. Batch 8 had essentially zero precipitation signal but scored only 0.692, below the optimized E1/S1 batches. Conversely, batches 11–12 performed best despite precipitation signals near 0.72.
• In the tested scope, E1/S1 was superior to E1/S2. Batch 12 (E1/S1, +1.2 V) exceeded batch 10 (E1/S2, +1.2 V) in yield, selectivity, FE, transport efficiency, and score.

Contradicted or narrowed claims:
• A monotonic “more potential and longer electrolysis are better” law was decisively contradicted by batch 3. At +1.5 V for 14400 s, productive metrics collapsed to zero even though ohmic efficiency remained 0.870. This changed the explanation from a simple charge-limited model to one with a high-potential failure region.
• A simple “highest conductivity wins” expectation was contradicted by batches 7 and 9. Both retained respectable ohmic efficiency but performed poorly because other limitations dominated.
• A simple exact identity such as measured yield = measured conversion × measured selectivity was not supported. For example, batch 12 reported yield 0.753 and conversion 0.740. Independent noisy assay channels make these estimates useful but not algebraically exact.
• The original conjecture that a moderate current cap would outperform the highest cap was neither confirmed nor rejected. Current cap and duration were changed together in the early campaign, so their effects were not independently identifiable.

Untested claims:
• The exact optimum between +1.2 and +1.5 V was not tested.
• Additivity of solvent and electrolyte potential shifts was assumed when choosing some material-screen potentials but never validated.
• The individual causal roles of precipitation, proton activity, interfacial kinetics, and hidden material residuals remain untested because these variables were not independently manipulated.
• No full solvent-by-electrolyte factorial, concentration study, current-cap sweep, or replication study was performed.

Retrospectively, the evidence that most changed the interpretation was batch 3’s collapse, the duration series in batches 4–6, the separation of ohmic and transport behavior in batch 9, and the direct E1 solvent comparison between batches 10 and 12. These statements describe the evidential record rather than claiming unrecorded contemporaneous thoughts.

2. Most informative additional experiment

I would repeat the batch-7 E0/S0 condition—0.04 mol reagent, 0.08 L S0, +0.8 V, E0, and 14400 s—but lower the current cap from 500 to 100 mA. I would retain the same intermediate UV-visible measurement and final assay.

This experiment distinguishes the leading transport/precipitation-limited explanation from an alternative in which E0/S0 mainly suffers from unfavorable interfacial kinetics or an incorrectly matched potential.

• If lowering the cap substantially raised FE, transport efficiency, and energy efficiency while maintaining a meaningful fraction of batch 7’s conversion, I would strengthen the transport-limited interpretation: the 500 mA setting was demanding current faster than E0/S0 could productively support.
• If efficiencies remained near batch 7’s low values and conversion fell roughly with supplied charge, I would favor unfavorable interface kinetics, persistent precipitation/passivation, or potential mismatch rather than current-driven mass-transfer overload.
• If precipitation decreased markedly together with improved efficiencies, I would regard precipitation/passivation as a stronger causal mediator.
• If precipitation stayed near 0.98 but efficiencies improved, precipitation would look more like a correlated equilibrium signal than the direct bottleneck.
• A null difference would not uniquely identify the alternative, but it would weaken the claim that excessive current demand was the main cause.

A replicate of batch 12 would be better for verifying the recommendation’s score, but the proposed cap intervention has greater mechanistic discrimination.

3. Unused evidence, reliability, and effect of the goal

Important evidence was unused or only lightly used. I did not inspect the complete raw spectral artifacts or fit UV-visible band shapes. Intermediate UV-visible efficiency estimates were observed but not modeled quantitatively against final assays. The final pH and precipitation channels were interpreted comparatively, but no intermediate pH measurements were made. Cost, small temperature changes, capacitance, detailed acid dissociation properties, and raw mass-balance metadata were not incorporated into a fitted law. Actual current-versus-time traces, electrode potentials after ohmic correction, and concentration trajectories were unavailable. There were also no technical replicates, so fixed process behavior could not be separated cleanly from assay noise.

The least reliable predictions are those for negative potential at -0.8 V, because only one negative-potential campaign batch existed and it used E1/S1 at -1.0 V. Predictions for the untested S0/E1, S0/E3, and S2/E0 crosses are also weak because hidden solvent–electrolyte interactions were explicitly possible. The new prediction set additionally used a much smaller volume and reagent amount than the campaign; extrapolating charge per mole assumes electrode geometry and transport scale in ways that were not identified. Predictions involving the difference between 100 and 500 mA are particularly uncertain because the campaign did not isolate current cap.

The recommendation of batch 12 is reliable as the highest observed score, but not as proof of a global optimum. Its score of 0.8117 was only slightly above batch 11’s 0.8079, a difference too small to establish a true +1.2 V advantage without replication. The severe gap between +1.2 and +1.5 V also leaves the intervening optimum unresolved.

The assigned goal did affect evidence collection. Maximizing balanced score led to adaptive concentration on E1/S1 and the promising +1.0 to +1.2 V region. That was appropriate for optimization, but it produced a sparse, nonorthogonal material screen and sacrificed independent identification of current, material, solvent, potential, and duration effects. There was no fundamental conflict between the goal and mechanistic learning, but the optimization emphasis made the final recommendation better supported than the general response law.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.52,
        "lower80": 0.25,
        "upper80": 0.76
      },
      "energy_efficiency": {
        "estimate": 0.18,
        "lower80": 0.03,
        "upper80": 0.38
      },
      "faradaic_efficiency": {
        "estimate": 0.16,
        "lower80": 0.03,
        "upper80": 0.34
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.04,
        "lower80": 0.0,
        "upper80": 0.14
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.016
      },
      "transport_efficiency": {
        "estimate": 0.18,
        "lower80": 0.04,
        "upper80": 0.37
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.9,
        "lower80": 0.72,
        "upper80": 0.99
      },
      "energy_efficiency": {
        "estimate": 0.32,
        "lower80": 0.1,
        "upper80": 0.55
      },
      "faradaic_efficiency": {
        "estimate": 0.3,
        "lower80": 0.12,
        "upper80": 0.5
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.13,
        "lower80": 0.01,
        "upper80": 0.3
      },
      "selective_product_yield": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.023
      },
      "transport_efficiency": {
        "estimate": 0.3,
        "lower80": 0.12,
        "upper80": 0.5
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.34,
        "upper80": 0.74
      },
      "energy_efficiency": {
        "estimate": 0.18,
        "lower80": 0.06,
        "upper80": 0.34
      },
      "faradaic_efficiency": {
        "estimate": 0.18,
        "lower80": 0.07,
        "upper80": 0.34
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.14,
        "lower80": 0.03,
        "upper80": 0.28
      },
      "selective_product_yield": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.032
      },
      "transport_efficiency": {
        "estimate": 0.2,
        "lower80": 0.08,
        "upper80": 0.37
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.93,
        "lower80": 0.86,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.35,
        "lower80": 0.18,
        "upper80": 0.53
      },
      "faradaic_efficiency": {
        "estimate": 0.3,
        "lower80": 0.15,
        "upper80": 0.48
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.36,
        "lower80": 0.25,
        "upper80": 0.49
      },
      "selective_product_yield": {
        "estimate": 0.05,
        "lower80": 0.025,
        "upper80": 0.085
      },
      "transport_efficiency": {
        "estimate": 0.3,
        "lower80": 0.15,
        "upper80": 0.48
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.39,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.3,
        "lower80": 0.15,
        "upper80": 0.48
      },
      "faradaic_efficiency": {
        "estimate": 0.32,
        "lower80": 0.17,
        "upper80": 0.5
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.22,
        "lower80": 0.07,
        "upper80": 0.38
      },
      "selective_product_yield": {
        "estimate": 0.015,
        "lower80": 0.001,
        "upper80": 0.04
      },
      "transport_efficiency": {
        "estimate": 0.36,
        "lower80": 0.19,
        "upper80": 0.55
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.92,
        "lower80": 0.84,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.72,
        "lower80": 0.57,
        "upper80": 0.84
      },
      "faradaic_efficiency": {
        "estimate": 0.72,
        "lower80": 0.58,
        "upper80": 0.84
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.55,
        "lower80": 0.44,
        "upper80": 0.67
      },
      "selective_product_yield": {
        "estimate": 0.19,
        "lower80": 0.12,
        "upper80": 0.28
      },
      "transport_efficiency": {
        "estimate": 0.68,
        "lower80": 0.53,
        "upper80": 0.81
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.37,
        "upper80": 0.8
      },
      "energy_efficiency": {
        "estimate": 0.18,
        "lower80": 0.06,
        "upper80": 0.35
      },
      "faradaic_efficiency": {
        "estimate": 0.15,
        "lower80": 0.04,
        "upper80": 0.31
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.12,
        "lower80": 0.02,
        "upper80": 0.27
      },
      "selective_product_yield": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.03
      },
      "transport_efficiency": {
        "estimate": 0.17,
        "lower80": 0.05,
        "upper80": 0.34
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.95,
        "lower80": 0.88,
        "upper80": 0.99
      },
      "energy_efficiency": {
        "estimate": 0.28,
        "lower80": 0.12,
        "upper80": 0.46
      },
      "faradaic_efficiency": {
        "estimate": 0.22,
        "lower80": 0.1,
        "upper80": 0.38
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.34,
        "lower80": 0.24,
        "upper80": 0.47
      },
      "selective_product_yield": {
        "estimate": 0.075,
        "lower80": 0.035,
        "upper80": 0.13
      },
      "transport_efficiency": {
        "estimate": 0.23,
        "lower80": 0.1,
        "upper80": 0.4
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.32,
        "upper80": 0.76
      },
      "energy_efficiency": {
        "estimate": 0.2,
        "lower80": 0.06,
        "upper80": 0.39
      },
      "faradaic_efficiency": {
        "estimate": 0.18,
        "lower80": 0.05,
        "upper80": 0.36
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.11,
        "lower80": 0.02,
        "upper80": 0.26
      },
      "selective_product_yield": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.031
      },
      "transport_efficiency": {
        "estimate": 0.18,
        "lower80": 0.05,
        "upper80": 0.36
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.9,
        "lower80": 0.8,
        "upper80": 0.97
      },
      "energy_efficiency": {
        "estimate": 0.37,
        "lower80": 0.19,
        "upper80": 0.56
      },
      "faradaic_efficiency": {
        "estimate": 0.34,
        "lower80": 0.18,
        "upper80": 0.52
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.36,
        "lower80": 0.25,
        "upper80": 0.5
      },
      "selective_product_yield": {
        "estimate": 0.085,
        "lower80": 0.04,
        "upper80": 0.15
      },
      "transport_efficiency": {
        "estimate": 0.3,
        "lower80": 0.15,
        "upper80": 0.48
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.5,
        "lower80": 0.26,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.1,
        "lower80": 0.01,
        "upper80": 0.25
      },
      "faradaic_efficiency": {
        "estimate": 0.08,
        "lower80": 0.0,
        "upper80": 0.21
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.11,
        "lower80": 0.01,
        "upper80": 0.25
      },
      "selective_product_yield": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.037
      },
      "transport_efficiency": {
        "estimate": 0.1,
        "lower80": 0.01,
        "upper80": 0.25
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.94,
        "lower80": 0.88,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.19,
        "lower80": 0.08,
        "upper80": 0.33
      },
      "faradaic_efficiency": {
        "estimate": 0.15,
        "lower80": 0.06,
        "upper80": 0.28
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.38,
        "lower80": 0.3,
        "upper80": 0.48
      },
      "selective_product_yield": {
        "estimate": 0.22,
        "lower80": 0.15,
        "upper80": 0.3
      },
      "transport_efficiency": {
        "estimate": 0.16,
        "lower80": 0.07,
        "upper80": 0.29
      }
    }
  ],
  "rationale": "Predictions anchor to the campaign’s S0/E0 positive-potential batch and E1/S1 polarity control, then scale cautiously for charge per mole, duration, current cap, and nominal transport/conductivity differences. Positive polarity is expected to preserve high selectivity; negative polarity should produce little target and activate the yield gate. E1 should improve S0 transport, whereas E3 remains diffusion-limited. S2 may reduce E0 precipitation but sacrifices conductivity. Intervals include final-assay noise and substantial model uncertainty from the lower batch volume, sparse cross-material coverage, unmeasured delivered current, and extrapolation away from tested conditions."
}
```
