# repeat-02/EC-W01-B12-optimization-E-MisIndexed

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-02\EC-W01-B12-optimization-E-MisIndexed\participant\optimization-E-MisIndexed

## 同期笔记

### v1 · 公开事件 0

# Electrochemical campaign hypotheses

## H1 [tentative]
At fixed loading, moderate absolute driving force should maximize the balanced score: increasing duration or potential magnitude should initially raise conversion/yield, but excessive charge or overpotential should reduce selectivity and energy efficiency. Testable consequence: a middle potential-duration combination will beat both weak and aggressive conditions within a material pair.

## H2 [tentative]
Transport and ohmic terms should favor conductive media, while selectivity may favor lower proton activity and double-layer capacitance. The nominal dossier therefore gives no unambiguous best material: S0/E0 is a conductivity baseline, S1 may improve diffusion, and S2/S3 may suppress proton-linked side reactions. I will screen material pairs before local refinement.

## H3 [tentative]
Potential sign is mechanism-critical and unknown. Matched positive/negative trials should show a large directional asymmetry if the target is predominantly anodic or cathodic.

Decision: use a common 0.020 mol reagent in 0.040 L solvent for comparability, screen signs/materials and charge severity, then spend later batches around the best observed region. Intermediate UV-vis measurements will be used diagnostically, not as substitutes for final assays. I will revise these claims after consequential contrasts.

### v2 · 公开事件 42

# Electrochemical campaign hypotheses

## H1 [supported qualitatively, optimum unresolved]
For negative electrolysis, balanced performance depends strongly on driving force and exposure. At S1/E1 and 7200 s, -0.8 V outperformed -1.2 V (final assays experiment 6 versus 3), with higher score, yield, selectivity, Faradaic and energy efficiency. This supports an overpotential penalty at more-negative voltage, but duration and current-response optima remain unresolved.

## H2 [material ranking provisional]
Under the matched -1.2 V, 200 mA cap, 7200 s screen, S1/E1 scored above S2/E2 and S3/E3 (experiments 3–5). This is evidence for the pair as a package, not attribution to solvent or electrolyte separately; crossed combinations were not tested. E0/S0 also showed complete precipitation signal and is not currently preferred.

## H3 [supported strongly in tested scope]
The target pathway is favored at negative potential. The matched S0/E0 sign contrast at ±1.2 V and 1800 s gave zero score at positive potential and a positive score at negative potential (experiments 1–2), far larger than assay uncertainty. This does not imply all positive potentials are inert under every material.

Decision: retain 0.020 mol/0.040 L and S1/E1, then explore duration/current cap and voltages near -0.8 V. A result reversing the -0.8 versus -1.2 ranking under replication would weaken H1.

### v3 · 公开事件 84

# Electrochemical campaign hypotheses

## H1 [supported in tested S1/E1 scope]
Balanced performance is non-monotonic in negative potential. At 500 mA cap and 14400 s, scores at -0.6, -0.5, -0.4, and -0.3 V were approximately 0.553, 0.582, 0.587, and 0.582 (experiments 8–11). A simple quadratic descriptive fit places the vertex near -0.40 V, but this is interpolation rather than a mechanistic law. The independent -0.4 V repeat scored 0.573 (experiment 12), confirming a strong-performing region while showing meaningful run-to-run/process variation beyond any single reported instrument uncertainty.

## H2 [material ranking provisional]
S1/E1 is the best tested pair. In the matched -1.2 V, 200 mA, 7200 s screen it exceeded S2/E2 and S3/E3 (experiments 3–5). Because solvent and electrolyte were changed together, their individual contributions and crossed combinations remain unresolved. Precipitation signal remained around 0.72 in the best region, so eliminating precipitation might offer further improvement, but no tested low-precipitation pair compensated in the balanced score.

## H3 [supported strongly in tested scope]
Negative potential favors target formation: the S0/E0 ±1.2 V contrast at 1800 s separated zero from positive score (experiments 1–2). Scope is limited to the tested loading/material and does not establish that every positive-potential condition is inactive.

## H4 [supported, current-cap mechanism partly confounded]
Long exposure and a permissive current cap enable high conversion at moderate negative potential. Moving from experiment 7 (-0.8 V, 200 mA cap, 14400 s) toward experiment 8 (-0.6 V, 500 mA cap, 14400 s) greatly increased conversion and yield, but potential and cap changed together. The cap is a ceiling rather than delivered-current evidence; its causal contribution is unresolved.

## Operating decision
Recommend the completed experiment 10 procedure: 0.020 mol limiting reagent, 0.040 L S1, E1, -0.40 V, 500 mA cap, 14400 s. It had the highest observed score and was supported by experiment 12 as a repeat of the same operating point, though the repeat score was lower. Neighboring -0.5 and -0.3 V results make -0.4 V a locally supported compromise between yield and energy/ohmic efficiency. This recommendation would change if replicated crossed-material tests or a denser potential scan showed a reliably higher mean score.

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
      "potential_V": 1.2
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
    "cost": 0.2834640145301819,
    "electrochemical_conversion": 0.008014115504920483,
    "electrochemical_selectivity": 0.01034972071647644,
    "energy_efficiency": 0.005256945732980967,
    "faradaic_efficiency": 0.02452157624065876,
    "ohmic_efficiency": 0.9730915427207947,
    "pH_normalized": 0.23218974471092224,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
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
      "potential_V": -1.2
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
    "cost": 0.2834640145301819,
    "electrochemical_conversion": 0.008702250197529793,
    "electrochemical_selectivity": 0.5984846949577332,
    "energy_efficiency": 0.17149116098880768,
    "faradaic_efficiency": 0.35891470313072205,
    "ohmic_efficiency": 0.981929361820221,
    "pH_normalized": 0.2294943928718567,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.2657165825366974,
    "selective_product_yield": 0.01883457787334919,
    "transport_efficiency": 0.3851715326309204
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
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -1.2
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
    "cost": 0.305512011051178,
    "electrochemical_conversion": 0.11198683828115463,
    "electrochemical_selectivity": 0.5451814532279968,
    "energy_efficiency": 0.22309868037700653,
    "faradaic_efficiency": 0.28736308217048645,
    "ohmic_efficiency": 0.928381085395813,
    "pH_normalized": 0.20363308489322662,
    "precipitation_signal": 0.7135193943977356,
    "safety_risk": 0.09559440612792969,
    "score": 0.2820284962654114,
    "selective_product_yield": 0.05480583384633064,
    "transport_efficiency": 0.3039199709892273
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
      "solvent": 2,
      "volume_L": 0.04
    },
    {
      "current_mA": 200,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -1.2
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
    "cost": 0.33111199736595154,
    "electrochemical_conversion": 0.09476092457771301,
    "electrochemical_selectivity": 0.42014798521995544,
    "energy_efficiency": 0.15019164979457855,
    "faradaic_efficiency": 0.2923634946346283,
    "ohmic_efficiency": 0.9076031446456909,
    "pH_normalized": 0.16724827885627747,
    "precipitation_signal": 0.0,
    "safety_risk": 0.1135944053530693,
    "score": 0.2423122674226761,
    "selective_product_yield": 0.0450192391872406,
    "transport_efficiency": 0.260875940322876
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
      "solvent": 3,
      "volume_L": 0.04
    },
    {
      "current_mA": 200,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": -1.2
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
    "cost": 0.31511199474334717,
    "electrochemical_conversion": 0.09219346940517426,
    "electrochemical_selectivity": 0.5390937924385071,
    "energy_efficiency": 0.1565595120191574,
    "faradaic_efficiency": 0.24887244403362274,
    "ohmic_efficiency": 0.9627838134765625,
    "pH_normalized": 0.2895091474056244,
    "precipitation_signal": 0.0,
    "safety_risk": 0.12619440257549286,
    "score": 0.2610117793083191,
    "selective_product_yield": 0.05573583021759987,
    "transport_efficiency": 0.23836298286914825
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
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "current_mA": 200,
      "electrolyte_profile": 1,
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
    "cost": 0.30320799350738525,
    "electrochemical_conversion": 0.14287246763706207,
    "electrochemical_selectivity": 0.6152929067611694,
    "energy_efficiency": 0.4453316926956177,
    "faradaic_efficiency": 0.40120986104011536,
    "ohmic_efficiency": 0.9127849340438843,
    "pH_normalized": 0.20462734997272491,
    "precipitation_signal": 0.7242242693901062,
    "safety_risk": 0.09559440612792969,
    "score": 0.3610990345478058,
    "selective_product_yield": 0.09632496535778046,
    "transport_efficiency": 0.37652653455734253
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
      "potential_V": -0.8
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
    "cost": 0.3078159987926483,
    "electrochemical_conversion": 0.2917958199977875,
    "electrochemical_selectivity": 0.6088826656341553,
    "energy_efficiency": 0.45068374276161194,
    "faradaic_efficiency": 0.37931135296821594,
    "ohmic_efficiency": 0.9443464279174805,
    "pH_normalized": 0.20364195108413696,
    "precipitation_signal": 0.7092664241790771,
    "safety_risk": 0.09559440612792969,
    "score": 0.4012311100959778,
    "selective_product_yield": 0.1792677640914917,
    "transport_efficiency": 0.3827117085456848
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
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -0.6
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
    "cost": 0.3158800005912781,
    "electrochemical_conversion": 0.801948070526123,
    "electrochemical_selectivity": 0.6489005088806152,
    "energy_efficiency": 0.4597517251968384,
    "faradaic_efficiency": 0.4406052231788635,
    "ohmic_efficiency": 0.7263256311416626,
    "pH_normalized": 0.2019444704055786,
    "precipitation_signal": 0.7221392393112183,
    "safety_risk": 0.09559440612792969,
    "score": 0.5530546307563782,
    "selective_product_yield": 0.5072410702705383,
    "transport_efficiency": 0.4341098964214325
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
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "current_mA": 500,
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
    "cost": 0.31299999356269836,
    "electrochemical_conversion": 0.8421998023986816,
    "electrochemical_selectivity": 0.6601240038871765,
    "energy_efficiency": 0.4674766957759857,
    "faradaic_efficiency": 0.4438096284866333,
    "ohmic_efficiency": 0.6811760067939758,
    "pH_normalized": 0.20395824313163757,
    "precipitation_signal": 0.7300134301185608,
    "safety_risk": 0.09559440612792969,
    "score": 0.5822257995605469,
    "selective_product_yield": 0.5821680426597595,
    "transport_efficiency": 0.46464088559150696
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
      "current_mA": 500,
      "electrolyte_profile": 1,
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
    "cost": 0.31011998653411865,
    "electrochemical_conversion": 0.8983234763145447,
    "electrochemical_selectivity": 0.7035456895828247,
    "energy_efficiency": 0.40093010663986206,
    "faradaic_efficiency": 0.4823172688484192,
    "ohmic_efficiency": 0.5534911155700684,
    "pH_normalized": 0.20164410769939423,
    "precipitation_signal": 0.7191752791404724,
    "safety_risk": 0.09559440612792969,
    "score": 0.5866140723228455,
    "selective_product_yield": 0.6019542813301086,
    "transport_efficiency": 0.4836668372154236
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
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -0.3
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
    "cost": 0.30724000930786133,
    "electrochemical_conversion": 0.9370461702346802,
    "electrochemical_selectivity": 0.6914843320846558,
    "energy_efficiency": 0.30636706948280334,
    "faradaic_efficiency": 0.49727824330329895,
    "ohmic_efficiency": 0.42174312472343445,
    "pH_normalized": 0.20262913405895233,
    "precipitation_signal": 0.7270644307136536,
    "safety_risk": 0.09559440612792969,
    "score": 0.5816988348960876,
    "selective_product_yield": 0.648192822933197,
    "transport_efficiency": 0.5044581890106201
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
      "current_mA": 500,
      "electrolyte_profile": 1,
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
    "cost": 0.31011998653411865,
    "electrochemical_conversion": 0.8665454387664795,
    "electrochemical_selectivity": 0.6671863198280334,
    "energy_efficiency": 0.3777351975440979,
    "faradaic_efficiency": 0.4391769766807556,
    "ohmic_efficiency": 0.5803179144859314,
    "pH_normalized": 0.2031494528055191,
    "precipitation_signal": 0.7204003930091858,
    "safety_risk": 0.09559440612792969,
    "score": 0.5731939077377319,
    "selective_product_yield": 0.615447461605072,
    "transport_efficiency": 0.4604019224643707
  }
}
```

## K1 封存报告

Mechanism report

1. Empirical operating map

The system behaves like a cathodic conversion with a finite useful potential window, charge/exposure dependence, and strong coupling among solvent, electrolyte, potential, current ceiling, and duration. The best observed operating region used 0.020 mol limiting reagent in 0.040 L solvent-S1, electrolyte-E1, a negative potential near -0.4 V, a 500 mA current ceiling, and 14,400 s electrolysis. Batch 10 at that point had the highest observed balanced-efficiency-v2 score, 0.5866. Batch 12 repeated the same recipe and scored 0.5732, supporting the region while showing appreciable run-to-run variation.

The score can be understood from the published weighted components:

S_raw = 0.30Y + 0.15Sel + 0.10X + 0.15Eta_E + 0.12Eta_F + 0.10Eta_T + 0.08Eta_O,

where Y is selective-product yield, Sel is electrochemical selectivity, X is conversion, and the remaining terms are energy, Faradaic, transport, and ohmic efficiencies. The published yield gate is consistent with multiplying this raw score by min(Y/0.02,1). Thus conditions with essentially no product are strongly suppressed even if, for example, their ohmic efficiency is high. This explains why batch 1 scored zero despite an observed ohmic efficiency of 0.973.

2. Direction of the target reaction

The clearest mechanistic result is the potential-sign contrast. Batches 1 and 2 used the same S0/E0 medium, 100 mA ceiling, and 1,800 s duration, differing primarily in potential sign:

• Batch 1, +1.2 V: score 0.000; conversion 0.0080; selectivity 0.0103; selective yield 0; energy efficiency 0.0053; Faradaic efficiency 0.0245; transport efficiency 0; precipitation signal 1.000.
• Batch 2, -1.2 V: score 0.2657; conversion 0.0087; selectivity 0.5985; selective yield 0.0188; energy efficiency 0.1715; Faradaic efficiency 0.3589; transport efficiency 0.3852; precipitation signal 1.000.

Conversion was near the assay resolution in both cases, so its small numerical difference should not be overinterpreted. The large changes in selectivity and efficiency, however, indicate that the target-forming electron-transfer pathway is favored under cathodic polarization. Positive polarization in this tested medium mostly generated nonproductive current or negligible target formation. I infer a reduction-like target step, although the anonymous benchmark species prevent assigning a real chemical identity or electron count.

This sign conclusion is secure only for the tested S0/E0 recipe. I did not test positive potentials in S1/E1, so claiming that all positive-potential conditions are inactive would be an extrapolation.

3. Proposed kinetic and transport picture

A useful phenomenological model is:

E_eff = E_applied - DeltaE_solvent - DeltaE_electrolyte - E0_hidden - iR,

i = min(I_ceiling, i_kin(E_eff, medium), i_transport(medium, concentration)),

dX/dt = k_target(E_eff, medium)(1-X) - k_loss(E_eff, medium)X,

Y approximately equals X times intrinsic target selectivity, with assay/process noise, while Faradaic efficiency is the fraction of charge entering productive chemistry. A simple conversion approximation in a restricted regime would be X = 1-exp[-k_app(E_eff, medium,I_ceiling)t], but the data do not justify treating k_app as constant across all potentials because current limitation, mass transport, and side reactions change simultaneously.

The nominal dossier suggests that transport depends on electrolyte diffusivity and diffusion-layer thickness and on the solvent diffusivity factor. Ohmic behavior depends on electrolyte bulk conductivity, solvent conductivity factor, fixture resistance, and actual current. Interface kinetics can also depend on double-layer capacitance, proton activity, and the solvent/electrolyte potential shifts. Fixed hidden world residuals modify all of these relationships.

In this interpretation, the imposed current is a ceiling, not proof that the stated current was continuously delivered. Near a potential-dependent kinetic or transport limit, raising the ceiling permits more current but does not guarantee it. This matters because no direct current trace or passed charge was observed.

4. Material effects and precipitation coupling

Batches 3–5 screened three matched solvent/electrolyte pairs at -1.2 V, 200 mA, and 7,200 s:

• Batch 3, S1/E1: score 0.2820; conversion 0.1120; selectivity 0.5452; yield 0.0548; energy efficiency 0.2231; Faradaic efficiency 0.2874; transport efficiency 0.3039; ohmic efficiency 0.9284; precipitation 0.7135.
• Batch 4, S2/E2: score 0.2423; conversion 0.0948; selectivity 0.4201; yield 0.0450; energy efficiency 0.1502; Faradaic efficiency 0.2924; transport efficiency 0.2609; ohmic efficiency 0.9076; precipitation 0.
• Batch 5, S3/E3: score 0.2610; conversion 0.0922; selectivity 0.5391; yield 0.0557; energy efficiency 0.1566; Faradaic efficiency 0.2489; transport efficiency 0.2384; ohmic efficiency 0.9628; precipitation 0.

S1/E1 was therefore the best tested pair under the matched screen, especially in conversion, energy efficiency, and transport efficiency. This is qualitatively compatible with the high nominal diffusivity of E1, its thin diffusion layer, and the 1.25 relative diffusivity of S1. Its nominal conductivity is lower than E0, so the result is not a simple conductivity ranking.

S2/E2 and S3/E3 suppressed the precipitation signal but did not produce a higher balanced score. Precipitation therefore appears coupled to the medium rather than being an absolute blocker: the best S1/E1 batches retained precipitation signals around 0.71–0.73 yet still performed well. It could represent an electrolyte salt equilibrium largely orthogonal to the target pathway, or it could modestly reduce available transport without overwhelming the favorable kinetics. These alternatives cannot be separated from the present observations.

S0/E0 had precipitation signal 1.000 in batches 1 and 2. Although it gave very high ohmic efficiency, its nominal thick diffusion layer and lower diffusivity provide a plausible explanation for its weak transport/product formation at short exposure. That explanation remains tentative because S0/E0 was not tested at the later high-current, long-duration optimum.

The material screen changed solvent and electrolyte together. Consequently, individual solvent effects, individual electrolyte effects, and solvent-electrolyte interactions are not identifiable. S1/E1 is supported as a package, not as proof that S1 and E1 are separately optimal.

5. Potential, current ceiling, and time

Changing S1/E1 from -1.2 V to -0.8 V at the same 200 mA ceiling and 7,200 s substantially improved performance:

• Batch 3, -1.2 V: score 0.2820; conversion 0.1120; selectivity 0.5452; yield 0.0548; energy efficiency 0.2231.
• Batch 6, -0.8 V: score 0.3611; conversion 0.1429; selectivity 0.6153; yield 0.0963; energy efficiency 0.4453.

Thus, making the electrode less negative improved rather than impaired the target process over this interval. I infer that -1.2 V imposes excessive overpotential, increasing parasitic charge consumption or otherwise lowering target selectivity and energy efficiency.

Duration had a positive effect in the directly comparable batches 6 and 7. Both used S1/E1, -0.8 V, and 200 mA; duration increased from 7,200 to 14,400 s:

• Batch 6: score 0.3611; conversion 0.1429; yield 0.0963.
• Batch 7: score 0.4012; conversion 0.2918; yield 0.1793.

Selectivity and the efficiency terms changed much less than conversion and yield. This supports accumulation of product with exposure rather than a fundamentally different pathway, at least up to 14,400 s. Since 14,400 s was the permitted maximum, the duration optimum was not bracketed. Longer exposure could increase conversion further, reach a plateau, or eventually increase degradation; the campaign cannot decide among these extrapolations.

The transition from batch 7 to batch 8 produced a much larger improvement, but both potential and current ceiling changed:

• Batch 7: -0.8 V, 200 mA, 14,400 s; score 0.4012; conversion 0.2918; yield 0.1793.
• Batch 8: -0.6 V, 500 mA, 14,400 s; score 0.5531; conversion 0.8019; yield 0.5072.

This result is consistent with a restrictive 200 mA ceiling in batch 7 and a more favorable potential in batch 8, but their separate contributions are not identifiable because there was no matched current-only comparison.

6. Local potential window in the optimized regime

Batches 8–11 held S1/E1, the 500 mA ceiling, and 14,400 s constant while stepping potential from -0.6 to -0.3 V:

• Batch 8, -0.6 V: score 0.5531; conversion 0.8019; selectivity 0.6489; yield 0.5072; energy efficiency 0.4598; Faradaic efficiency 0.4406; transport efficiency 0.4341; ohmic efficiency 0.7263.
• Batch 9, -0.5 V: score 0.5822; conversion 0.8422; selectivity 0.6601; yield 0.5822; energy efficiency 0.4675; Faradaic efficiency 0.4438; transport efficiency 0.4646; ohmic efficiency 0.6812.
• Batch 10, -0.4 V: score 0.5866; conversion 0.8983; selectivity 0.7035; yield 0.6020; energy efficiency 0.4009; Faradaic efficiency 0.4823; transport efficiency 0.4837; ohmic efficiency 0.5535.
• Batch 11, -0.3 V: score 0.5817; conversion 0.9370; selectivity 0.6915; yield 0.6482; energy efficiency 0.3064; Faradaic efficiency 0.4973; transport efficiency 0.5045; ohmic efficiency 0.4217.

As potential became less negative, conversion, selective yield, Faradaic efficiency, and transport efficiency generally rose. In contrast, energy efficiency peaked near -0.5 V and then declined, while ohmic efficiency declined strongly. Selectivity was highest in batch 10, although the difference between batches 10 and 11 is comparable to the stated selectivity noise scale and should not be treated as definitive by itself.

The balanced score consequently formed a broad plateau near -0.5 to -0.3 V. A descriptive quadratic fit to the four scores has a vertex near -0.40 V. This fit is an interpolation aid, not a fundamental electrochemical equation. Its apparent optimum results from the scoring tradeoff: moving toward -0.3 V raises conversion and yield but sacrifices energy and ohmic efficiency, whereas moving toward -0.6 V preserves those efficiency terms but leaves more reactant unconverted.

The falling ohmic-efficiency metric at less-negative potential may seem counterintuitive if it is interpreted only as bulk conductivity. It likely represents a system-level ratio involving useful electrical work, actual current, and fixed/contact losses, rather than a material conductivity measurement alone. Another plausible explanation is that the high current ceiling allows larger current as the productive pathway becomes kinetically accessible, increasing iR losses. Without delivered-current or voltage-loss traces, these alternatives remain unidentifiable.

7. Repeatability and process variation

Batch 12 repeated batch 10 exactly. Its result was:

• Batch 12, -0.4 V: score 0.5732; conversion 0.8665; selectivity 0.6672; yield 0.6154; energy efficiency 0.3777; Faradaic efficiency 0.4392; transport efficiency 0.4604; ohmic efficiency 0.5803.

The repeat remained strong but did not reproduce every component. The score difference, about 0.0134, and several component differences are too large to regard batch 10 as a perfectly deterministic optimum. They are compatible with process variation plus independent assay noise. The appropriate inference is that -0.4 V lies in a robust high-performing region, not that its true mean score is exactly 0.5866 or necessarily greater than -0.5 V by the observed 0.0044 margin.

The repeat also shows why the batch-10 selectivity maximum should be treated cautiously. Batch 12 selectivity was 0.6672 rather than 0.7035, while its selective yield was slightly higher. A latent process variable affecting current history, interface state, or product partitioning could change the component balance without changing the recipe.

8. Acid-base and precipitation observations

Within S1/E1, normalized pH stayed close to 0.20 across batches 3 and 6–12 despite large changes in conversion. This suggests that the bulk acid-base state is buffered or controlled primarily by the material formulation rather than by target conversion. It does not rule out local interfacial pH gradients, which could still affect selectivity and precipitation.

Material pairs produced clearly different normalized pH values in the matched screen: approximately 0.204 for S1/E1, 0.167 for S2/E2, and 0.290 for S3/E3. Because both materials changed, these values cannot be assigned solely to electrolyte acid concentration, pKa, or solvent proton activity.

The precipitation signal in optimized S1/E1 runs was nearly constant while conversion changed from about 0.14 to 0.94. That weak empirical coupling favors the hypothesis that precipitation is governed mainly by medium equilibrium rather than by product formation. However, only endpoint snapshots were measured; transient precipitation or electrode fouling could still influence current and efficiency.

9. Scope and unidentifiable quantities

The report applies to the anonymous synthetic benchmark world and does not identify real chemicals or establish a transferable real-world recipe. The following factors remain unidentifiable:

• Molecular identities, stoichiometric electron count, and elementary reaction intermediates.
• The hidden formal potential and fixed world-specific kinetic, solvation, transport, and interface residuals.
• Delivered-current histories, passed charge, electrode area, electrode gap, and contact resistance. The fixture was fixed within the campaign, so its effects are confounded with all experiments.
• Separate solvent and electrolyte main effects, because the material screen used paired combinations rather than a crossed design.
• The isolated effect of the 500 mA ceiling, because potential changed when the ceiling was raised.
• Loading and concentration laws, because every completed batch used 0.020 mol reagent and 0.040 L starting solvent.
• Behavior beyond 14,400 s and the location of any long-time degradation maximum.
• Whether precipitation directly causes efficiency loss, is an inert reporter of medium composition, or both.
• Exact replicate means and variances; only the -0.4 V operating point was repeated.

10. Plausible alternatives

One alternative to the overpotential explanation is that potential chiefly controls how much of the current ceiling is reached, while intrinsic selectivity is mostly material-controlled. Under that model, the apparent potential optimum arises from current-dependent iR and transport penalties rather than a change in elementary pathway selectivity. The data cannot fully separate these mechanisms.

A second alternative is that the target forms through a coupled chemical step after electron transfer. Potential would control generation of a reactive intermediate, while acid-base state, solvent stabilization, or precipitation controls its subsequent partition between target and side product. The nearly stable bulk pH does not exclude this because the relevant chemistry may occur in the interfacial layer.

A third alternative is electrode conditioning: long electrolysis or particular potentials may change the synthetic interface state, producing batch-to-batch differences such as those between batches 10 and 12. No surface-sensitive measurement was available to test this.

11. Final mechanistic synthesis

My best explanation is a cathodic target pathway with a hidden formal potential located such that moderate negative polarization is favorable. Strongly negative potentials, exemplified by -1.2 V, waste energy and reduce selectivity. Long exposure and a sufficiently permissive current ceiling are required to approach high conversion. S1/E1 supplies the best observed combination of mass transport and interfacial selectivity, even though it permits substantial precipitation and does not maximize the ohmic metric. In the 500 mA, 14,400 s regime, moving from -0.6 toward -0.3 V progressively increases conversion and selective yield, but energy and ohmic efficiencies deteriorate; the public weighted objective therefore peaks broadly around -0.4 to -0.5 V.

Batch 10 is the highest observed realization, while batch 12 establishes that the same operating point remains strong but variable. The sealed recommendation should therefore be interpreted as a locally supported operating region centered near -0.4 V—not as proof of a unique global mechanistic optimum.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific prior, hidden response law, or ground-truth outcome was supplied. The only supplied prior information was the nominal material-property dossier plus the instrument and scoring contracts.

Supported claims:
• The target pathway is cathodically favored. The strongest evidence was the matched S0/E0 sign comparison: batch 1 at +1.2 V scored 0 with zero selective yield, whereas batch 2 at -1.2 V scored 0.2657 and showed substantial selectivity and efficiency.
• Moderate negative potential is preferable to excessive negative polarization. In S1/E1, batch 6 at -0.8 V outperformed batch 3 at -1.2 V under otherwise matched 200 mA, 7,200 s conditions. The later fixed-condition scan, batches 8–11, placed the broad score maximum around -0.5 to -0.3 V rather than at the most negative voltage.
• Longer exposure increases conversion and yield in the tested regime. Doubling duration from 7,200 to 14,400 s in batches 6 and 7 increased conversion from 0.143 to 0.292 and selective yield from 0.096 to 0.179.
• S1/E1 was the best tested material package. In the matched -1.2 V screen, batch 3 exceeded S2/E2 in batch 4 and S3/E3 in batch 5. This supported the prior suspicion that favorable diffusion could matter, but not a separable solvent or electrolyte law.
• The optimum is a tradeoff rather than a maximum of every component. From batches 8–11, conversion and yield rose toward -0.3 V while energy and ohmic efficiencies fell, leaving the balanced score nearly flat near -0.4 V.

Contradicted or weakened claims:
• A simple “highest conductivity is best” rule was contradicted. S0/E0 gave high ohmic efficiency but was not the best productive medium; S1/E1 ultimately performed much better.
• The conjecture that suppressing precipitation would necessarily improve the objective was not supported. Batches 4 and 5 had zero precipitation signal yet scored below batch 3, while the best batches retained precipitation signals near 0.72.
• Any claim that batch 10 represented a sharply determined unique optimum was weakened by batch 12. The exact repeat scored 0.5732 rather than 0.5866 and shifted several component metrics. The evidence supports a strong region near -0.4 V, not a noise-free optimum.
• A monotonic “more negative gives more conversion” law was contradicted by batches 8–11: conversion increased as potential moved from -0.6 toward -0.3 V.

Untested or unresolved claims:
• Solvent and electrolyte main effects remain untested because batches 3–5 changed them as matched pairs rather than independently.
• The isolated effect of raising the current ceiling is unresolved. The major change from batch 7 to batch 8 altered both potential and current ceiling.
• Loading, concentration, durations beyond 14,400 s, and most positive-potential material combinations were untested.
• The proposed roles of local pH, interfacial conditioning, precipitation-induced fouling, and fixed fixture resistance remain plausible but unverified because no current trace or surface measurement was available.

The principal judgment changes were sequential: batches 1–2 established polarity; batches 3–5 selected S1/E1; batch 6 shifted attention away from -1.2 V; batch 7 established the value of longer duration; batch 8 revealed a much higher-performing high-current/moderate-potential regime but introduced a current–potential confound; batches 9–11 localized the score plateau; and batch 12 changed the interpretation from a precise optimum to a variable high-performing region.

2. One additional discriminating experiment

I would run the batch-7 recipe again but change only the current ceiling from 200 to 500 mA: 0.020 mol reagent, 0.040 L S1, E1, -0.8 V, 500 mA ceiling, and 14,400 s. This would directly address the confound between batches 7 (-0.8 V, 200 mA) and 8 (-0.6 V, 500 mA).

If conversion and yield rose substantially toward batch 8 while selectivity and energy efficiency remained characteristic of -0.8 V, I would conclude that the higher current ceiling was chiefly responsible for the throughput jump, while potential mainly controls the efficiency/selectivity balance. If the result remained close to batch 7 despite the higher ceiling, I would infer that -0.6 V itself activates a substantially more productive kinetic window and that 200 mA was not the dominant restriction. If conversion increased but Faradaic, energy, or ohmic efficiency deteriorated sharply, I would favor a mixed explanation in which higher current increases throughput while simultaneously introducing transport or iR penalties. A result with large unexplained divergence from all three neighboring batches would increase my belief in interface conditioning or other latent process variation.

3. Unused evidence, reliability, and goal effects

The largest unused evidence source was the detailed raw characterization artifacts. I relied mainly on processed endpoint estimates and did not quantitatively model chromatographic, UV–visible, IR, or NMR proxy peak shapes and areas. Intermediate UV–visible measurements were collected in every batch but were used mostly as qualitative diagnostics; they were not fitted as time-course data. Cost and safety observations were also not used in the mechanistic model because all tested risks stayed well below the public limit and the objective was the balanced-efficiency score. The nominal capacitance, acid, pKa, solubility-product, and potential-shift descriptors informed qualitative reasoning but were not independently identifiable from the paired design.

The least reliable predictions are Q05–Q10, which involve solvent/electrolyte combinations or positive-potential combinations not directly tested, and Q11, which extrapolates S0/E0 to a 500 mA ceiling and much greater exposure. Q01 is also uncertain because its selective yield lies near the 0.02 score-gate threshold, so small process or assay deviations can cause a large proportional score change. For the positive-potential cases, the prediction that target formation remains very low is more reliable than the exact small numerical estimates near the assay floor.

The recommendation’s least reliable aspect is the assertion that -0.40 V is better than -0.50 or -0.30 V in mean performance. Their observed scores were close, and the batch-10/12 repeat difference exceeded the margin between neighboring potentials. The recommendation of the broader S1/E1, 500 mA, long-duration, moderate-negative-potential region is more reliable than the exact voltage ranking.

The assigned optimization goal materially affected evidence collection. I first screened polarity and several material packages, then concentrated batches on improving the public score. That exploitation produced a useful local optimum but left solvent/electrolyte effects crossed, current and potential partly confounded, loading fixed, and only one exact repeat. A mechanism-identification goal would have favored a factorial design, current-only contrasts, multiple repeats, and fewer intermediate measurements. I see no clear conflict beyond this ordinary exploration-versus-optimization tradeoff.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.61,
        "lower80": 0.53,
        "upper80": 0.69
      },
      "energy_efficiency": {
        "estimate": 0.39,
        "lower80": 0.29,
        "upper80": 0.48
      },
      "faradaic_efficiency": {
        "estimate": 0.39,
        "lower80": 0.32,
        "upper80": 0.46
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.21,
        "lower80": 0.04,
        "upper80": 0.34
      },
      "selective_product_yield": {
        "estimate": 0.013,
        "lower80": 0.0,
        "upper80": 0.031
      },
      "transport_efficiency": {
        "estimate": 0.37,
        "lower80": 0.28,
        "upper80": 0.46
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.038
      },
      "energy_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.03
      },
      "faradaic_efficiency": {
        "estimate": 0.014,
        "lower80": 0.0,
        "upper80": 0.038
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.017
      },
      "transport_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.031
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.61,
        "lower80": 0.53,
        "upper80": 0.69
      },
      "energy_efficiency": {
        "estimate": 0.38,
        "lower80": 0.29,
        "upper80": 0.47
      },
      "faradaic_efficiency": {
        "estimate": 0.39,
        "lower80": 0.32,
        "upper80": 0.46
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.38,
        "lower80": 0.31,
        "upper80": 0.45
      },
      "selective_product_yield": {
        "estimate": 0.15,
        "lower80": 0.095,
        "upper80": 0.215
      },
      "transport_efficiency": {
        "estimate": 0.37,
        "lower80": 0.28,
        "upper80": 0.46
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.031
      },
      "faradaic_efficiency": {
        "estimate": 0.013,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.007,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.018
      },
      "transport_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.033
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.64,
        "lower80": 0.53,
        "upper80": 0.73
      },
      "energy_efficiency": {
        "estimate": 0.46,
        "lower80": 0.34,
        "upper80": 0.56
      },
      "faradaic_efficiency": {
        "estimate": 0.42,
        "lower80": 0.33,
        "upper80": 0.5
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.405,
        "lower80": 0.31,
        "upper80": 0.49
      },
      "selective_product_yield": {
        "estimate": 0.16,
        "lower80": 0.09,
        "upper80": 0.24
      },
      "transport_efficiency": {
        "estimate": 0.43,
        "lower80": 0.31,
        "upper80": 0.54
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.013,
        "lower80": 0.0,
        "upper80": 0.043
      },
      "energy_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.033
      },
      "faradaic_efficiency": {
        "estimate": 0.014,
        "lower80": 0.0,
        "upper80": 0.042
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.065
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.019
      },
      "transport_efficiency": {
        "estimate": 0.007,
        "lower80": 0.0,
        "upper80": 0.035
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.48,
        "upper80": 0.7
      },
      "energy_efficiency": {
        "estimate": 0.38,
        "lower80": 0.26,
        "upper80": 0.49
      },
      "faradaic_efficiency": {
        "estimate": 0.34,
        "lower80": 0.25,
        "upper80": 0.43
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.35,
        "lower80": 0.26,
        "upper80": 0.44
      },
      "selective_product_yield": {
        "estimate": 0.127,
        "lower80": 0.065,
        "upper80": 0.205
      },
      "transport_efficiency": {
        "estimate": 0.3,
        "lower80": 0.19,
        "upper80": 0.42
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.042
      },
      "energy_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.034
      },
      "faradaic_efficiency": {
        "estimate": 0.013,
        "lower80": 0.0,
        "upper80": 0.041
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.065
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.019
      },
      "transport_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.034
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.5,
        "lower80": 0.37,
        "upper80": 0.62
      },
      "energy_efficiency": {
        "estimate": 0.27,
        "lower80": 0.16,
        "upper80": 0.39
      },
      "faradaic_efficiency": {
        "estimate": 0.34,
        "lower80": 0.24,
        "upper80": 0.44
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.31,
        "lower80": 0.22,
        "upper80": 0.4
      },
      "selective_product_yield": {
        "estimate": 0.106,
        "lower80": 0.05,
        "upper80": 0.18
      },
      "transport_efficiency": {
        "estimate": 0.32,
        "lower80": 0.2,
        "upper80": 0.44
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.011,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.032
      },
      "faradaic_efficiency": {
        "estimate": 0.013,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.007,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.018
      },
      "transport_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.033
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.49,
        "upper80": 0.69
      },
      "energy_efficiency": {
        "estimate": 0.32,
        "lower80": 0.21,
        "upper80": 0.43
      },
      "faradaic_efficiency": {
        "estimate": 0.36,
        "lower80": 0.27,
        "upper80": 0.45
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.52,
        "lower80": 0.42,
        "upper80": 0.61
      },
      "selective_product_yield": {
        "estimate": 0.54,
        "lower80": 0.39,
        "upper80": 0.68
      },
      "transport_efficiency": {
        "estimate": 0.35,
        "lower80": 0.24,
        "upper80": 0.46
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "energy_efficiency": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.032
      },
      "faradaic_efficiency": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.018
      },
      "transport_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.034
      }
    }
  ],
  "rationale": "The sign-matched campaign contrast showed that negative polarization supports the target pathway whereas positive polarization leaves target yield near the assay floor, so all positive-potential predictions remain close to zero and are yield-gated. Negative-potential estimates scale exposure approximately by charge per mole, with saturation at high exposure, and use the observed -0.8 V efficiencies as anchors. Intervals are wider for short runs, untested crossed solvent/electrolyte pairs, and the 500 mA extrapolation; they include assay noise, the batch-10/12 process variability, and uncertainty about delivered current, precipitation, and material interactions."
}
```
