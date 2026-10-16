# repeat-01/EC-W03-B12-optimization-E-MisIndexed

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-01\EC-W03-B12-optimization-E-MisIndexed\participant\optimization-E-MisIndexed

## 同期笔记

### v1 · 公开事件 0

# Electrochemical campaign hypotheses

## H1 [tentative]
At fixed loading (0.020 mol reagent in 0.040 L solvent), balanced score should favor moderate driving potential and duration rather than extremes: conversion should rise with charge, while selectivity and energy efficiency may fall at high overpotential or prolonged electrolysis. A potential-shift-adjusted comparison is needed because solvent/electrolyte nominal shifts differ.

## H2 [tentative]
Transport/ohmic performance should tend to improve with conductivity and diffusivity, but the best balanced score may instead occur in a less proton-active medium if that suppresses competing chemistry. E3 and E1 are plausible starting electrolytes; S1 is a plausible compromise solvent. These are priors only and may be overturned by assays.

## Planned tests
Hold loading and volume fixed. First screen material combinations under common electrical conditions, then vary potential, time, and current cap around the best region; use a replicate or near-replicate if possible. A result favoring an extreme condition will redirect later tests toward that boundary.

### v2 · 公开事件 28

# Electrochemical campaign hypotheses

## H1 [supported in tested S1/E3 scope]
Negative potential accesses the target-forming regime; +1.0 V gave zero selective yield, while -1.0 V produced detectable yield under otherwise matched 600 s, 100 mA-cap conditions (events runner-operation-0007 and -0014). This sign effect is large relative to the assay noise scales, though exact low conversion values remain noisy.

## H2 [supported locally]
Within S1/E3, moderate negative potential is preferable to stronger drive for balanced score. At 3600 s and 200 mA cap, -0.5 V reached score 0.354 versus 0.150 at -1.5 V (events -0028, -0021), with higher selectivity and energy/Faradaic/transport efficiencies. Potential and realized current are confounded, so this does not yet isolate overpotential from delivered charge.

## H3 [unresolved]
Material-dependent conductivity, transport, proton activity, and shifts may dominate the optimum. Next tests will compare solvent/electrolyte combinations near -0.5 V, then tune duration/current. The working expectation is that longer electrolysis can raise yield until efficiency/selectivity losses outweigh conversion gains.

### v3 · 公开事件 63

# Electrochemical campaign hypotheses

## H1 [supported in tested scope]
Negative potential accesses the target-forming regime; the matched 600 s sign comparison strongly favored -1.0 V over +1.0 V (events runner-operation-0007, -0014).

## H2 [supported locally]
Moderate negative potential is better balanced than -1.5 V in S1/E3. Extending -0.5 V electrolysis from 3600 to 14400 s raised yield and score (events -0028, -0035), without the efficiency collapse seen at -1.5 V. Duration remains confounded with accumulated charge.

## H3 [supported among screened combinations]
At -0.5 V, 200 mA cap, 14400 s, S1/E1 was best of tested materials (score 0.474, event -0049) and exceeded S1/E3 (0.427, -0035), S0/E0 (0.379, -0042), S2/E1 (0.418, -0056), and S3/E1 (0.430, -0063). This is evidence for a material-combination effect, but not a complete factorial separation of solvent and electrolyte. High precipitation signal for E1 is a possible non-scoring operational concern, although safety remained below the stated limit.

## Decision
Use the final three batches to tune potential and current cap around S1/E1 at maximum tested duration. A milder potential is expected to trade conversion for selectivity/efficiency; a higher current cap may increase conversion but harm transport/ohmic performance. Recommend the best observed completed batch, not an extrapolation.

### v4 · 公开事件 84

# Electrochemical campaign hypotheses — final source-stage synthesis

## H1 [supported in tested scope]
Target formation requires the negative-potential regime under the tested conditions: the matched short sign comparison favored -1.0 V over +1.0 V (events runner-operation-0007 and -0014). This claim is scoped to the tested loading and S1/E3; material potential shifts mean the numerical boundary should not be assumed universal.

## H2 [supported locally]
A moderate negative setpoint balances yield and electrical efficiencies. In S1/E1 at 14400 s and 200 mA cap, moving from -0.5 to -0.25 V increased the observed score from 0.474 to 0.489 (events -0049 and -0070), whereas 0 V raised yield but collapsed energy and ohmic efficiencies, lowering score to 0.392 (event -0077). The -0.35 V result scored 0.474 (event -0084). Because assay noise and run-to-run process uncertainty are nonzero, the small -0.25 versus -0.5 score difference is a numerical advantage rather than strong evidence of a precisely located optimum.

## H3 [supported among screened combinations]
S1/E1 was the strongest screened material combination at -0.5 V, 200 mA cap, 14400 s (event -0049), outperforming the tested S1/E3, S0/E0, S2/E1, and S3/E1 combinations (events -0035, -0042, -0056, -0063). The partial, non-factorial screen cannot uniquely assign the benefit to solvent or electrolyte. E1 showed substantial precipitation signal, an unresolved operational feature not directly penalizing the public score here.

## Operating decision
Recommend completed batch 10: 0.020 mol reagent, 0.040 L S1, E1 electrolyte, -0.25 V, 200 mA current cap, 14400 s electrolysis. It had the highest observed balanced-efficiency-v2 score (0.489; event -0070). Batch 7 at -0.5 V remains a plausible robust alternative because its score was close and its ohmic efficiency was higher. Further work should replicate both conditions and refine the -0.5 to -0.25 V interval while measuring realized current/charge.

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
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 3,
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
    "cost": 0.2988399863243103,
    "electrochemical_conversion": 0.019761737436056137,
    "electrochemical_selectivity": 0.9132629036903381,
    "energy_efficiency": 0.8829307556152344,
    "faradaic_efficiency": 0.7801703810691833,
    "ohmic_efficiency": 0.9629068970680237,
    "pH_normalized": 0.2834365665912628,
    "precipitation_signal": 0.00621018698439002,
    "safety_risk": 0.09559440612792969,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.7514666318893433
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
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 3,
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
    "cost": 0.2988399863243103,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.5857460498809814,
    "energy_efficiency": 0.25794824957847595,
    "faradaic_efficiency": 0.30707383155822754,
    "ohmic_efficiency": 0.97174471616745,
    "pH_normalized": 0.28074121475219727,
    "precipitation_signal": 0.009242543950676918,
    "safety_risk": 0.09559440612792969,
    "score": 0.16303952038288116,
    "selective_product_yield": 0.011729691177606583,
    "transport_efficiency": 0.3333306610584259
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
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "current_mA": 200,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": -1.5
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
    "cost": 0.30292001366615295,
    "electrochemical_conversion": 0.040792595595121384,
    "electrochemical_selectivity": 0.5044339299201965,
    "energy_efficiency": 0.12524005770683289,
    "faradaic_efficiency": 0.22076629102230072,
    "ohmic_efficiency": 0.9492005705833435,
    "pH_normalized": 0.28145623207092285,
    "precipitation_signal": 0.0,
    "safety_risk": 0.09559440612792969,
    "score": 0.15042522549629211,
    "selective_product_yield": 0.013158363290131092,
    "transport_efficiency": 0.23732319474220276
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
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "current_mA": 200,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": -0.5
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
    "cost": 0.30004000663757324,
    "electrochemical_conversion": 0.06890148669481277,
    "electrochemical_selectivity": 0.6196609735488892,
    "energy_efficiency": 0.5364906787872314,
    "faradaic_efficiency": 0.41786321997642517,
    "ohmic_efficiency": 0.8868166208267212,
    "pH_normalized": 0.2807656526565552,
    "precipitation_signal": 0.0,
    "safety_risk": 0.09559440612792969,
    "score": 0.3544137179851532,
    "selective_product_yield": 0.04791444167494774,
    "transport_efficiency": 0.38637566566467285
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
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "current_mA": 200,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": -0.5
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
    "cost": 0.3043600022792816,
    "electrochemical_conversion": 0.294189453125,
    "electrochemical_selectivity": 0.654776394367218,
    "energy_efficiency": 0.5479525327682495,
    "faradaic_efficiency": 0.4006379246711731,
    "ohmic_efficiency": 0.8862507939338684,
    "pH_normalized": 0.2857264280319214,
    "precipitation_signal": 0.0,
    "safety_risk": 0.09559440612792969,
    "score": 0.4269070029258728,
    "selective_product_yield": 0.19696417450904846,
    "transport_efficiency": 0.3901284635066986
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
      "current_mA": 200,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -0.5
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
    "cost": 0.28835999965667725,
    "electrochemical_conversion": 0.2499513477087021,
    "electrochemical_selectivity": 0.6010141968727112,
    "energy_efficiency": 0.4549599587917328,
    "faradaic_efficiency": 0.3561265170574188,
    "ohmic_efficiency": 0.9004285335540771,
    "pH_normalized": 0.229326069355011,
    "precipitation_signal": 0.9978154301643372,
    "safety_risk": 0.072194404900074,
    "score": 0.37877023220062256,
    "selective_product_yield": 0.15821726620197296,
    "transport_efficiency": 0.331443190574646
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
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "current_mA": 200,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -0.5
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
    "cost": 0.3043600022792816,
    "electrochemical_conversion": 0.3609381318092346,
    "electrochemical_selectivity": 0.6798233985900879,
    "energy_efficiency": 0.5827777981758118,
    "faradaic_efficiency": 0.4719671607017517,
    "ohmic_efficiency": 0.885922372341156,
    "pH_normalized": 0.21038967370986938,
    "precipitation_signal": 0.6467019319534302,
    "safety_risk": 0.09559440612792969,
    "score": 0.47444698214530945,
    "selective_product_yield": 0.24638792872428894,
    "transport_efficiency": 0.4753675162792206
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
      "solvent": 2,
      "volume_L": 0.04
    },
    {
      "current_mA": 200,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -0.5
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
    "cost": 0.3299599885940552,
    "electrochemical_conversion": 0.3200945556163788,
    "electrochemical_selectivity": 0.6114265322685242,
    "energy_efficiency": 0.5053970813751221,
    "faradaic_efficiency": 0.44371649622917175,
    "ohmic_efficiency": 0.8434156775474548,
    "pH_normalized": 0.222994863986969,
    "precipitation_signal": 0.482858806848526,
    "safety_risk": 0.1135944053530693,
    "score": 0.41789549589157104,
    "selective_product_yield": 0.17973722517490387,
    "transport_efficiency": 0.43722113966941833
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
      "solvent": 3,
      "volume_L": 0.04
    },
    {
      "current_mA": 200,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -0.5
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
    "cost": 0.3139599859714508,
    "electrochemical_conversion": 0.31820735335350037,
    "electrochemical_selectivity": 0.5782473683357239,
    "energy_efficiency": 0.5490329265594482,
    "faradaic_efficiency": 0.4203159213066101,
    "ohmic_efficiency": 0.9108219742774963,
    "pH_normalized": 0.21400423347949982,
    "precipitation_signal": 0.5824911594390869,
    "safety_risk": 0.12619440257549286,
    "score": 0.4299090802669525,
    "selective_product_yield": 0.2052597552537918,
    "transport_efficiency": 0.44114717841148376
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
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "current_mA": 200,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -0.25
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
    "cost": 0.3014799952507019,
    "electrochemical_conversion": 0.4076998233795166,
    "electrochemical_selectivity": 0.7404863238334656,
    "energy_efficiency": 0.5260690450668335,
    "faradaic_efficiency": 0.5347790718078613,
    "ohmic_efficiency": 0.698050320148468,
    "pH_normalized": 0.20839183032512665,
    "precipitation_signal": 0.6566107869148254,
    "safety_risk": 0.09559440612792969,
    "score": 0.488566517829895,
    "selective_product_yield": 0.28060948848724365,
    "transport_efficiency": 0.5361286401748657
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
      "current_mA": 200,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 0
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
    "cost": 0.2985999882221222,
    "electrochemical_conversion": 0.4524976313114166,
    "electrochemical_selectivity": 0.7545936107635498,
    "energy_efficiency": 0.012963879853487015,
    "faradaic_efficiency": 0.5905579328536987,
    "ohmic_efficiency": 0.0026482813991606236,
    "pH_normalized": 0.20937687158584595,
    "precipitation_signal": 0.6644999384880066,
    "safety_risk": 0.09559440612792969,
    "score": 0.39223822951316833,
    "selective_product_yield": 0.33667415380477905,
    "transport_efficiency": 0.5977378487586975
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
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "current_mA": 200,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -0.35
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
    "cost": 0.30263200402259827,
    "electrochemical_conversion": 0.3586582839488983,
    "electrochemical_selectivity": 0.6880755424499512,
    "energy_efficiency": 0.5501688122749329,
    "faradaic_efficiency": 0.468504399061203,
    "ohmic_efficiency": 0.8080542087554932,
    "pH_normalized": 0.20989719033241272,
    "precipitation_signal": 0.6578359007835388,
    "safety_risk": 0.09559440612792969,
    "score": 0.4741285443305969,
    "selective_product_yield": 0.27562758326530457,
    "transport_efficiency": 0.4897293448448181
  }
}
```

## K1 封存报告

## Mechanistic account

This is a bounded synthetic electrochemical world involving an anonymous limiting reagent, four anonymous solvents (S0–S3), and four anonymous electrolyte profiles (E0–E3). I interpret the observations using a charge-driven target reaction competing with non-target electrochemistry, coupled to mass transport, solution resistance, proton activity, precipitation, and an instrument-defined energy-efficiency calculation. The public data support this qualitative structure, but they do not identify real chemical species, electron stoichiometry, electrode area, realized current, or individual rate constants.

### 1. Proposed process model

A useful phenomenological model is:

- Applied potential and the solvent/electrolyte potential shifts determine an effective overpotential, η.
- The current cap does not necessarily equal realized current. A plausible relationship is
  `I_real = min(I_cap, I_kinetic(η), I_transport)`.
- Productive charge accumulation drives conversion:
  `dX/dt ≈ (I_real * FE_target)/(n F N0) * f(X)`,
  where X is conversion, N0 is initial reagent amount, n is an unknown electron count, and f(X) accounts for depletion or passivation.
- Target yield is approximately conversion times chemical selectivity:
  `Y_target ≈ X * S_chem`,
  with deviations from assay noise, side reactions, or the fact that the reported channels may not share exactly the same estimator.
- Chemical selectivity and Faradaic efficiency depend differently on η, proton activity, solvent environment, and interfacial state. Thus high conversion need not maximize the balanced score.
- Transport efficiency depends on diffusivity, diffusion-layer thickness, conductivity, concentration, and hidden solvent–electrolyte coupling. Ohmic and energy efficiencies additionally depend on cell resistance and potential/current conventions.
- Precipitation can change free ion concentrations, conductivity, mass transport, or electrode condition, although no decisive causal effect of precipitation was isolated here.

The public score is consistent with the declared weighted combination of conversion, electrochemical selectivity, energy efficiency, Faradaic efficiency, ohmic efficiency, selective-product yield, and transport efficiency. Consequently, a condition that maximizes yield alone can lose to a condition with moderately lower yield but much better electrical efficiencies.

### 2. Charge and duration effects

The clearest within-material duration comparison was between batches 4 and 5. Both used 0.020 mol reagent in 0.040 L S1, E3, −0.5 V, and a 200 mA current cap. Increasing electrolysis time from 3,600 s to 14,400 s increased conversion from 0.0689 to 0.2942 and selective-product yield from 0.0479 to 0.1970. These are roughly fourfold changes for a fourfold duration increase. Meanwhile, selectivity changed only from 0.6197 to 0.6548, Faradaic efficiency from 0.4179 to 0.4006, and energy efficiency from 0.5365 to 0.5480. The score rose from 0.3544 to 0.4269.

This supports approximately charge-proportional product formation over that range, without strong depletion or accelerating degradation. It does not prove strict linearity: there was no intermediate time series, realized current was not measured, and batches were not replicated. Extrapolation beyond 14,400 s would therefore be unjustified.

### 3. Potential dependence and competing objectives

The S1/E1 potential series at 14,400 s and a 200 mA cap illustrates the main coupling:

- Batch 7, −0.50 V: conversion 0.3609, selectivity 0.6798, yield 0.2464, Faradaic efficiency 0.4720, transport efficiency 0.4754, ohmic efficiency 0.8859, energy efficiency 0.5828, score 0.4744.
- Batch 12, −0.35 V: conversion 0.3587, selectivity 0.6881, yield 0.2756, Faradaic efficiency 0.4685, transport efficiency 0.4897, ohmic efficiency 0.8081, energy efficiency 0.5502, score 0.4741.
- Batch 10, −0.25 V: conversion 0.4077, selectivity 0.7405, yield 0.2806, Faradaic efficiency 0.5348, transport efficiency 0.5361, ohmic efficiency 0.6981, energy efficiency 0.5261, score 0.4886.
- Batch 11, 0 V: conversion 0.4525, selectivity 0.7546, yield 0.3367, Faradaic efficiency 0.5906, and transport efficiency 0.5977, but ohmic efficiency fell to 0.00265 and energy efficiency to 0.01296; score fell to 0.3922.

Thus moving from −0.50 toward −0.25 V improved the measured chemical channels and Faradaic/transport efficiencies, while progressively reducing ohmic efficiency. At 0 V the chemical channels were best but the electrical-efficiency channels collapsed. This explains why batch 10, not batch 11, was the operating recommendation.

I would not interpret the near-zero ohmic efficiency at a nominal 0 V as proof that the solution suddenly became highly resistive. The solvent and electrolyte were unchanged. A more plausible explanation is that the benchmark's ohmic/energy metrics depend strongly on applied-potential headroom, cell polarization, or a ratio that becomes unfavorable near the chosen reference potential. That interpretation is conjectural because cell voltage, current, resistance, and the calculation formulas were not exposed.

The ordering is not perfectly smooth: batch 12 at −0.35 V had lower conversion than batch 10 at −0.25 V. The assay noise alone may not explain the entire difference, so fixed hidden nonlinearities, process variability, or differences in realized current are plausible. With no replicates, the 0.014 score advantage of batch 10 over batch 7 is an observed numerical advantage, not strong evidence that −0.25 V is the precisely located optimum.

At stronger negative drive, performance deteriorated. Batch 3 used S1/E3 at −1.5 V, 200 mA, and 3,600 s and produced conversion 0.0408, selectivity 0.5044, yield 0.0132, energy efficiency 0.1252, Faradaic efficiency 0.2208, transport efficiency 0.2373, and score 0.1504. Under the same material, current cap, and duration, batch 4 at −0.5 V scored 0.3544. This is consistent with excessive overpotential favoring parasitic charge transfer or an inefficient interfacial state rather than productive conversion.

### 4. Polarity evidence

Batches 1 and 2 compared +1.0 and −1.0 V using S1/E3, 100 mA, and 600 s. Batch 1 at +1.0 V showed conversion 0.0198 and selectivity 0.9133 but zero reported selective yield and score. Batch 2 at −1.0 V showed selective yield 0.0117 and score 0.1630, although its conversion estimate was clipped at zero and its selectivity was only 0.5857.

The appearance of product only in the negative-potential run is compatible with a cathodic target pathway. However, both runs were near the low-signal regime, the conversion/yield channels were internally noisy there, and +1.0 V may simply have been an excessively strong potential in the opposite direction. I therefore treat cathodic target formation as a plausible explanation rather than a uniquely established reaction mechanism.

### 5. Electrolyte effects

The most direct electrolyte comparison used S1 at −0.5 V, 200 mA, and 14,400 s:

- Batch 5, E3: score 0.4269, conversion 0.2942, yield 0.1970, selectivity 0.6548, Faradaic efficiency 0.4006, transport efficiency 0.3901.
- Batch 7, E1: score 0.4744, conversion 0.3609, yield 0.2464, selectivity 0.6798, Faradaic efficiency 0.4720, transport efficiency 0.4754.

E1 therefore improved every listed chemical, Faradaic, and transport outcome in this comparison, while ohmic efficiency remained almost unchanged (0.8859 versus 0.8863). Nominal E1 has higher bulk conductivity than E3 but also a thicker diffusion layer and lower diffusivity, so conductivity alone cannot explain the transport improvement. The E1 potential shift, acid environment, double-layer properties, and hidden fixed residuals or solvent coupling are all plausible contributors.

E1 also produced substantial precipitation signal in S1: 0.6467 in batch 7 and approximately 0.657–0.664 in batches 10–12. E3 in S1 gave zero precipitation signal in batches 4 and 5. This could indicate electrolyte-specific ion pairing or precipitation coupled to reaction products. It cannot be reconciled from nominal salt concentration and Ksp alone, which shows that the public material dossier is incomplete or that the precipitation channel involves species not represented by those nominal descriptors.

### 6. Solvent effects

With E1, −0.5 V, 200 mA, and 14,400 s, three solvents were compared:

- Batch 7, S1: score 0.4744; conversion 0.3609; yield 0.2464; selectivity 0.6798; energy efficiency 0.5828; transport efficiency 0.4754.
- Batch 8, S2: score 0.4179; conversion 0.3201; yield 0.1797; selectivity 0.6114; energy efficiency 0.5054; transport efficiency 0.4372.
- Batch 9, S3: score 0.4299; conversion 0.3182; yield 0.2053; selectivity 0.5782; energy efficiency 0.5490; transport efficiency 0.4411.

S1 was the strongest overall solvent in that local comparison. S3 had the highest ohmic efficiency, 0.9108, but poorer chemical selectivity and yield. S2 did not convert its nominally low proton activity and favorable solubility-product factor into superior score. These observations support solvent control of both interfacial selectivity and transport, rather than a one-variable ranking by conductivity or proton activity.

Batch 6 used S0/E0 at the same electrical condition and scored 0.3788, with precipitation signal 0.9978. Because both solvent and electrolyte changed relative to batch 7, its poorer performance cannot identify which material caused the difference.

### 7. pH, precipitation, and safety

The pH-normalized channel varied mainly with material choice, not with potential in the S1/E1 series. Batches 7 and 10–12 were all near 0.208–0.210, despite large changes in potential-dependent efficiencies. This suggests that bulk acid state was relatively stable and was not the main cause of the potential optimum.

Precipitation likewise remained near 0.65 across the S1/E1 potential series, while score ranged from 0.392 to 0.489. Precipitation was therefore not sufficient to determine performance within that series. It may still affect electrode aging or reproducibility, neither of which was measured.

Observed safety risk stayed well below the 0.65 limit. Representative values were 0.0722 for S0/E0, 0.0956 for S1 combinations, 0.1136 for S2/E1, and 0.1262 for S3/E1. Because risk followed material choice more clearly than electrolysis condition in these experiments, it appears dominated by the benchmark's solvent/reagent handling terms rather than accumulated electrochemical stress. No claim about real-world safety is warranted for anonymous benchmark materials.

### 8. Scope and identifiability limits

All principal comparisons used 0.020 mol reagent in 0.040 L solvent. Concentration and volume effects were not investigated, so the proposed relationships apply only near that loading. Current cap was mostly 200 mA and was never varied cleanly at otherwise optimal conditions. Therefore current dependence, electron stoichiometry, actual charge passed, and mass-transfer-limited current are unidentifiable.

There were no replicates. Instrument noise was declared, but process variability and hidden world residuals prevent assigning confidence intervals from single runs. The material screen was only partially factorial: E1 versus E3 was compared in S1, and S1/S2/S3 were compared with E1, but most other solvent–electrolyte combinations were untested. Interaction effects cannot be separated comprehensively.

The anonymous IDs do not support claims about real solvent or electrolyte identities. Electrode area, spacing, contact resistance, temperature history, electrode surface state, and product identities were unavailable. The data also cannot distinguish among several alternatives: direct electron transfer to the reagent; electrogeneration of an active mediator; proton-coupled electron transfer; or an interfacial pathway altered by adsorption or precipitation.

### 9. Overall interpretation

My preferred explanation is a target-forming cathodic or effectively negative-overpotential reaction whose rate is approximately charge-controlled at low-to-moderate conversion. Solvent and electrolyte jointly set the effective formal potential, interfacial selectivity, ionic transport, proton environment, and precipitation state. Strong negative drive wastes charge through competing processes, whereas moving too close to the benchmark's zero-potential reference destroys the reported ohmic and energy efficiencies despite improving chemical yield. The public balanced optimum therefore lies at an intermediate potential.

The best observed compromise was batch 10: 0.020 mol reagent, 0.040 L S1, E1, −0.25 V, 200 mA current cap, and 14,400 s. Its score was 0.4886 with conversion 0.4077, selectivity 0.7405, selective yield 0.2806, Faradaic efficiency 0.5348, transport efficiency 0.5361, ohmic efficiency 0.6981, and energy efficiency 0.5261. Batch 7 at −0.5 V is a plausible more electrically robust alternative because it retained much higher ohmic efficiency and scored only 0.014 lower. Replication and finer potential/current mapping would be required to establish whether batch 10 represents a reproducible optimum rather than a favorable single realization.

## K2 封存报告

1. **Claims and laws tested**

No instance-specific prior was supplied. The only supplied prior was the nominal material dossier, explicitly described as incomplete and subject to hidden residuals and solvent–electrolyte coupling.

- My initial law that moderate driving potential would outperform an extreme potential was supported locally. With S1/E3 at 3,600 s and 200 mA, batch 4 at −0.5 V scored 0.354, versus 0.150 for batch 3 at −1.5 V. With S1/E1, batch 10 at −0.25 V scored 0.489, while batch 11 at 0 V fell to 0.392 because its energy and ohmic efficiencies collapsed despite higher yield. This evidence changed the explanation from “more conversion is probably better” to an explicit conversion–electrical-efficiency compromise.

- The proposed approximately charge-controlled duration law was supported over one tested interval. Batches 4 and 5 differed primarily in duration: increasing from 3,600 to 14,400 s raised conversion from 0.0689 to 0.2942 and yield from 0.0479 to 0.1970, close to proportional increases. Saturation, long-time degradation, and the independent effect of current were untested.

- A negative-potential target pathway was weakly supported, not conclusively established. In the matched short runs, batch 2 at −1.0 V produced yield 0.0117, whereas batch 1 at +1.0 V reported zero yield. Both were low-signal measurements, and batch 2’s conversion estimate was clipped at zero, so this does not uniquely establish a cathodic molecular mechanism.

- The initial expectation that E1 or E3 and S1 might be useful was supported empirically. At otherwise matched conditions, S1/E1 in batch 7 scored 0.474 versus 0.427 for S1/E3 in batch 5. Among the E1 solvent comparison, S1 in batch 7 exceeded S2 in batch 8 and S3 in batch 9. However, the broader claim that nominal conductivity or diffusivity alone predicts performance was contradicted: E1 had nominally less favorable diffusion-layer properties than E3 but gave higher observed transport efficiency. Hidden coupling, potential shifts, or interfacial effects were therefore required.

- A simple nominal-Ksp prediction of precipitation was contradicted or at least shown incomplete. Batch 6, S0/E0, had precipitation signal 0.998, while S1/E3 in batches 4–5 had essentially zero and S1/E1 in batches 7 and 10–12 was near 0.65. The nominal salt descriptors alone did not explain that ordering.

- The approximation `selective yield ≈ conversion × selectivity` was broadly supported. For batch 7 the product of 0.3609 and 0.6798 is about 0.245, close to the measured yield of 0.246. Batch 10 showed a larger deviation—about 0.302 from the product versus 0.281 observed—so the relationship is approximate rather than an exact identity.

- The effect of current cap, concentration, volume, repeated cycling, and electrode aging remained untested. Nearly all informative optimization runs used 200 mA, 0.020 mol reagent, and 0.040 L solvent, with no replicates.

The evidence that most changed my judgment was: batches 3–4, which demonstrated the penalty at excessive negative potential; batches 4–5, which established the strong duration response; batches 5 and 7–9, which overturned a simple nominal-property ranking; and batches 10–11, which showed that maximizing chemical yield did not maximize the balanced score.

2. **One additional discriminating experiment**

I would repeat the batch-10 materials, loading, potential, and duration—S1/E1, 0.020 mol in 0.040 L, −0.25 V, 14,400 s—but reduce the current cap from 200 to 100 mA. I would collect the permitted intermediate UV–visible measurement and the final assay.

The leading explanation is that productive conversion is substantially controlled by delivered charge, with the current cap binding at −0.25 V. Relative to batch 10, it predicts materially lower conversion and yield at 100 mA, possibly near one-half before nonlinear corrections, accompanied by improved ohmic efficiency and perhaps higher chemical selectivity.

The main alternative is that current at −0.25 V is already limited by kinetics or transport below 100 mA, or that the batch-10 advantage was primarily a potential-dependent scoring artifact rather than cap-controlled charge delivery. Under that alternative, reducing the cap would leave conversion, yield, and transport efficiency close to batch 10.

- A large yield/conversion decrease with reasonably preserved selectivity would strengthen the charge-controlled model.
- Similar chemical results at both caps would imply that 200 mA was nonbinding and would shift my explanation toward potential-controlled kinetics or transport limitation.
- A disproportionate collapse of Faradaic or transport efficiency would suggest nonlinear interfacial or mass-transfer coupling rather than simple charge scaling.
- A result outside all these patterns would increase concern about batch variability, precipitation-mediated electrode changes, or the lack of reproducibility in the original optimum.

A replicate at exactly the batch-10 condition would estimate reproducibility better, but it would distinguish the competing current-control explanations less effectively.

3. **Unused evidence, weak predictions, and goal effects**

The raw spectral traces and peak-level characterization were not modeled; I relied on processed estimates. Intermediate UV–visible results were used mainly as consistency checks rather than fitted as a time-resolved kinetic series. Cost, detailed pH behavior, and precipitation were not used directly to choose the recommendation except as qualitative cautions. Nominal double-layer capacitance, diffusion-layer thickness, acid pKa, solubility-product factors, and potential shifts were not separable because the material screen was incomplete. No data addressed electrode aging, replicate variance, or realized current.

The least reliable sealed predictions are the positive-potential cases Q02, Q04, Q06, Q08, Q10, and Q12 because only batch 1 directly sampled positive potential, and it was a short, low-signal run. Q11 and Q12 are also weak because no campaign experiment used a 500 mA cap. Predictions for unobserved combinations such as S0/E1, S0/E3, and S2/E0 require extrapolating material interactions. Q01 and Q02 are additionally vulnerable to the selective-yield score gate because small absolute yield errors can cause large score changes.

The batch-10 recommendation is less certain than its rank suggests. Its score of 0.489 was only about 0.014 above batch 7, with no replication, and batch 12 showed non-smooth behavior at an intermediate potential. Batch 7 may therefore be a more electrically robust alternative even though it was not the highest observed score.

The assigned goal did affect evidence collection. Optimizing the public balanced-efficiency score encouraged fixed loading, long-duration exploitation, and local potential refinement after a promising material combination was found. That improved the chance of identifying a high-scoring batch but displaced replication, a full solvent–electrolyte factorial design, independent current variation, and detailed mechanistic measurements. There was no direct conflict between the goal and learning which operating region was favorable, but there was a clear tradeoff between score optimization and identifying a unique mechanism.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.45,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.44,
        "lower80": 0.28,
        "upper80": 0.58
      },
      "faradaic_efficiency": {
        "estimate": 0.35,
        "lower80": 0.22,
        "upper80": 0.47
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.094,
        "lower80": 0.0,
        "upper80": 0.24
      },
      "selective_product_yield": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.018
      },
      "transport_efficiency": {
        "estimate": 0.34,
        "lower80": 0.22,
        "upper80": 0.46
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.82,
        "lower80": 0.65,
        "upper80": 0.94
      },
      "energy_efficiency": {
        "estimate": 0.78,
        "lower80": 0.62,
        "upper80": 0.9
      },
      "faradaic_efficiency": {
        "estimate": 0.7,
        "lower80": 0.55,
        "upper80": 0.82
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.024,
        "lower80": 0.0,
        "upper80": 0.27
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0.0,
        "upper80": 0.012
      },
      "transport_efficiency": {
        "estimate": 0.68,
        "lower80": 0.55,
        "upper80": 0.8
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.59,
        "lower80": 0.47,
        "upper80": 0.7
      },
      "energy_efficiency": {
        "estimate": 0.43,
        "lower80": 0.29,
        "upper80": 0.56
      },
      "faradaic_efficiency": {
        "estimate": 0.33,
        "lower80": 0.22,
        "upper80": 0.45
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.332,
        "lower80": 0.26,
        "upper80": 0.4
      },
      "selective_product_yield": {
        "estimate": 0.07,
        "lower80": 0.035,
        "upper80": 0.12
      },
      "transport_efficiency": {
        "estimate": 0.34,
        "lower80": 0.23,
        "upper80": 0.46
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.78,
        "lower80": 0.62,
        "upper80": 0.91
      },
      "energy_efficiency": {
        "estimate": 0.73,
        "lower80": 0.57,
        "upper80": 0.85
      },
      "faradaic_efficiency": {
        "estimate": 0.68,
        "lower80": 0.52,
        "upper80": 0.8
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.234,
        "lower80": 0.0,
        "upper80": 0.51
      },
      "selective_product_yield": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "transport_efficiency": {
        "estimate": 0.67,
        "lower80": 0.52,
        "upper80": 0.79
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.68,
        "lower80": 0.56,
        "upper80": 0.79
      },
      "energy_efficiency": {
        "estimate": 0.56,
        "lower80": 0.42,
        "upper80": 0.68
      },
      "faradaic_efficiency": {
        "estimate": 0.46,
        "lower80": 0.34,
        "upper80": 0.58
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.411,
        "lower80": 0.34,
        "upper80": 0.48
      },
      "selective_product_yield": {
        "estimate": 0.115,
        "lower80": 0.07,
        "upper80": 0.17
      },
      "transport_efficiency": {
        "estimate": 0.46,
        "lower80": 0.34,
        "upper80": 0.58
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.8,
        "lower80": 0.64,
        "upper80": 0.92
      },
      "energy_efficiency": {
        "estimate": 0.72,
        "lower80": 0.55,
        "upper80": 0.85
      },
      "faradaic_efficiency": {
        "estimate": 0.72,
        "lower80": 0.56,
        "upper80": 0.84
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.096,
        "lower80": 0.0,
        "upper80": 0.48
      },
      "selective_product_yield": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.03
      },
      "transport_efficiency": {
        "estimate": 0.72,
        "lower80": 0.57,
        "upper80": 0.83
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.49,
        "upper80": 0.73
      },
      "energy_efficiency": {
        "estimate": 0.48,
        "lower80": 0.34,
        "upper80": 0.61
      },
      "faradaic_efficiency": {
        "estimate": 0.37,
        "lower80": 0.25,
        "upper80": 0.49
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.357,
        "lower80": 0.28,
        "upper80": 0.43
      },
      "selective_product_yield": {
        "estimate": 0.08,
        "lower80": 0.04,
        "upper80": 0.135
      },
      "transport_efficiency": {
        "estimate": 0.37,
        "lower80": 0.25,
        "upper80": 0.49
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.82,
        "lower80": 0.66,
        "upper80": 0.94
      },
      "energy_efficiency": {
        "estimate": 0.78,
        "lower80": 0.61,
        "upper80": 0.9
      },
      "faradaic_efficiency": {
        "estimate": 0.72,
        "lower80": 0.56,
        "upper80": 0.84
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.171,
        "lower80": 0.0,
        "upper80": 0.5
      },
      "selective_product_yield": {
        "estimate": 0.007,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "transport_efficiency": {
        "estimate": 0.7,
        "lower80": 0.55,
        "upper80": 0.82
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.64,
        "lower80": 0.5,
        "upper80": 0.76
      },
      "energy_efficiency": {
        "estimate": 0.49,
        "lower80": 0.34,
        "upper80": 0.63
      },
      "faradaic_efficiency": {
        "estimate": 0.4,
        "lower80": 0.27,
        "upper80": 0.53
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.363,
        "lower80": 0.28,
        "upper80": 0.45
      },
      "selective_product_yield": {
        "estimate": 0.09,
        "lower80": 0.045,
        "upper80": 0.15
      },
      "transport_efficiency": {
        "estimate": 0.36,
        "lower80": 0.23,
        "upper80": 0.49
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.8,
        "lower80": 0.63,
        "upper80": 0.92
      },
      "energy_efficiency": {
        "estimate": 0.65,
        "lower80": 0.46,
        "upper80": 0.8
      },
      "faradaic_efficiency": {
        "estimate": 0.67,
        "lower80": 0.49,
        "upper80": 0.8
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.267,
        "lower80": 0.0,
        "upper80": 0.49
      },
      "selective_product_yield": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.055
      },
      "transport_efficiency": {
        "estimate": 0.6,
        "lower80": 0.43,
        "upper80": 0.74
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.56,
        "lower80": 0.4,
        "upper80": 0.68
      },
      "energy_efficiency": {
        "estimate": 0.3,
        "lower80": 0.15,
        "upper80": 0.45
      },
      "faradaic_efficiency": {
        "estimate": 0.26,
        "lower80": 0.14,
        "upper80": 0.4
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.346,
        "lower80": 0.25,
        "upper80": 0.43
      },
      "selective_product_yield": {
        "estimate": 0.25,
        "lower80": 0.12,
        "upper80": 0.42
      },
      "transport_efficiency": {
        "estimate": 0.22,
        "lower80": 0.1,
        "upper80": 0.35
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.65,
        "lower80": 0.45,
        "upper80": 0.81
      },
      "energy_efficiency": {
        "estimate": 0.38,
        "lower80": 0.19,
        "upper80": 0.57
      },
      "faradaic_efficiency": {
        "estimate": 0.45,
        "lower80": 0.27,
        "upper80": 0.61
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.256,
        "lower80": 0.0,
        "upper80": 0.43
      },
      "selective_product_yield": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "transport_efficiency": {
        "estimate": 0.38,
        "lower80": 0.21,
        "upper80": 0.54
      }
    }
  ],
  "rationale": "Predictions use the campaign’s near-matched concentration, the approximately charge-proportional duration response in batches 4–5, the polarity evidence from batches 1–2, and material corrections from batches 5–9. The public score weights and selective-yield gate were applied while allowing uncertainty in unreported conversion and ohmic efficiency. Intervals are broad for positive-potential cases and 500 mA cases because these require substantial extrapolation beyond the well-characterized region."
}
```
