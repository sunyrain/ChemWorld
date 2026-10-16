# repeat-01/EC-W03-B12-optimization-E-Aligned

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-01\EC-W03-B12-optimization-E-Aligned\participant\optimization-E-Aligned

## 同期笔记

### v1 · 公开事件 0

# Electrochemical campaign hypotheses

**H1 [tentative]** Balanced performance should favor a moderate effective overpotential rather than the largest magnitude: conversion should rise with magnitude/duration, while selectivity and energy efficiency may fall beyond an optimum. Test across potential signs and magnitudes at fixed loading.

**H2 [tentative]** High-conductivity media (especially solvent-S0 and electrolyte-E3/E0 nominally) should improve ohmic efficiency, but transport may instead favor thinner diffusion layers / higher diffusivity (E1 or E2). A factorial material screen can distinguish these tradeoffs.

**H3 [tentative]** Current cap can limit delivered charge, so durations should be interpreted jointly with current cap. Initial screen will use a common 0.02 mol in 0.04 L loading, then refine potential, cap, and duration around the best observed score.

Predicted testable pattern: either potential sign will be strongly superior; within that sign an intermediate potential and duration will maximize the balanced score. This expectation is recorded before physical experiments.

### v2 · 公开事件 35

# Electrochemical campaign hypotheses

**H1 [supported in tested scope]** Positive potential is strongly superior to the matched negative potential at S0/E0, 1.0 V magnitude, 100 mA cap, 7200 s, and 0.02 mol/0.04 L loading. Batch 1 scored 0.509 versus batch 2 at 0.292, with higher conversion, selectivity, and all efficiency metrics (events runner-operation-0007 and -0014). This does not yet establish the optimum positive magnitude.

**H2 [supported for paired material combinations; interaction unresolved]** The matched S1/E1 combination is currently best: batch 3 scored 0.609, versus S0/E0 0.509, S2/E2 0.511, and S3/E3 0.425 (final assays at events -0007, -0021, -0028, -0035). Its advantage spans selectivity and Faradaic/transport/energy efficiency. Because solvent and electrolyte were changed together, whether S1, E1, or their interaction causes the gain remains unresolved. Next, cross S1 and E1 against alternatives.

**H3 [unresolved]** At fixed materials, longer charge or greater positive potential should increase conversion/yield but may sacrifice selectivity and energy efficiency. Test duration/potential/current cap around S1/E1; prefer the balanced score rather than conversion alone.

Measurement differences substantially exceed the stated final-assay per-channel noise for several metrics, but no replicate has yet been run; world-fixed material residuals and interaction are alternative explanations.

### v3 · 公开事件 73

# Electrochemical campaign hypotheses

**H1 [supported in tested scope]** Positive potential is superior to the matched negative potential (batches 1–2); the claim remains local to tested materials and charge conditions.

**H2 [supported, refined]** Electrolyte-E1 is the dominant favorable choice in the limited crossing: S0/E1 (batch 7, score 0.622) outperformed S0/E0 (batch 1, 0.509), while S1/E0 (batch 6, 0.575) was below S1/E1 (batch 3, 0.609). Solvent-S0 versus S1 is a smaller unresolved contrast because batch 7 exceeded batch 3 by only 0.013 and there are no replicates.

**H3 [supported non-monotonic duration response]** At S0/E1, +1.0 V, 100 mA cap, fixed loading, extending electrolysis from 7200 s (batch 7) to 14400 s (batch 8) and 28800 s (batch 9) raised score 0.622 → 0.674 → 0.852, mainly through conversion/yield while efficiencies stayed high. Extending to 43200 s (batch 10) lowered conversion, selective yield, and score to 0.813 (events runner-operation-0049, -0056, -0064, -0073). Thus useful charge has an optimum or post-formation loss region between roughly 28800 and 43200 s; alternatives include stochastic process variation, but the yield change is large relative to assay noise.

Final tests: probe near 32400 s and independently vary potential near the best duration. A result exceeding batch 9 would move the recommendation; otherwise retain batch 9.

### v4 · 公开事件 90

# Electrochemical campaign hypotheses — final source-stage record

**H1 [supported in tested scope]** Positive polarization is superior to matched negative polarization at S0/E0, ±1.0 V, 100 mA cap, 7200 s (batches 1–2). The campaign did not map the full signed response surface.

**H2 [supported for tested combinations]** Electrolyte-E1 gave the strongest balanced outcomes in the limited material crossing. S0/E1 was slightly better than S1/E1 in the initial matched-condition comparison, but the solvent contrast is not securely resolved without paired replicates; material interactions remain possible.

**H3 [supported non-monotonic duration response]** For 0.02 mol reagent in 0.04 L S0 with E1, +1.0 V and a 100 mA cap, balanced performance improved strongly through 28800 s, then declined at 32400–43200 s. Batch 9 at 28800 s had the maximum observed score 0.852, conversion 0.704, selective yield 0.691, and high efficiency/selectivity. Batch 11 (32400 s) scored 0.837 and batch 10 (43200 s) 0.813 (events runner-operation-0064, -0082, -0073).

**H4 [repeatability qualified]** Exact-condition repetition of the batch-9 procedure in batch 12 scored 0.835 rather than 0.852, while retaining similarly high conversion/yield and efficiency (event runner-operation-0090). Thus the 28800 s region is reproducibly high-performing, but the numerical advantage of batch 9 over batches 11–12 is not established as a deterministic effect given process variation and assay noise.

**Decision.** Recommend completed batch 9 because it is the maximum observed balanced-efficiency score and is supported by a high-performing exact replicate. Operational recipe: 0.02 mol limiting reagent, 0.04 L solvent-S0, electrolyte-E1, +1.0 V, 100 mA magnitude cap, two 14400 s electrolysis segments, then terminate/assay. I would change this decision if replicated neighboring durations or potentials produced a clearly higher mean score; those dimensions remain incompletely mapped.

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
    "cost": 0.28547999262809753,
    "electrochemical_conversion": 0.14071957767009735,
    "electrochemical_selectivity": 0.8394781947135925,
    "energy_efficiency": 0.6901599764823914,
    "faradaic_efficiency": 0.735862135887146,
    "ohmic_efficiency": 0.9659870862960815,
    "pH_normalized": 0.23031213879585266,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.5085907578468323,
    "selective_product_yield": 0.09591609984636307,
    "transport_efficiency": 0.7071583867073059
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
    "cost": 0.28547999262809753,
    "electrochemical_conversion": 0.05967716872692108,
    "electrochemical_selectivity": 0.5403205752372742,
    "energy_efficiency": 0.2102794200181961,
    "faradaic_efficiency": 0.36285680532455444,
    "ohmic_efficiency": 0.9748249650001526,
    "pH_normalized": 0.2276168018579483,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.29246559739112854,
    "selective_product_yield": 0.04489239677786827,
    "transport_efficiency": 0.3891136050224304
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
      "current_mA": 100,
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
    "cost": 0.3014799952507019,
    "electrochemical_conversion": 0.16379068791866302,
    "electrochemical_selectivity": 0.9346990585327148,
    "energy_efficiency": 0.9072447419166565,
    "faradaic_efficiency": 0.8800724744796753,
    "ohmic_efficiency": 0.9500816464424133,
    "pH_normalized": 0.21038080751895905,
    "precipitation_signal": 0.6509549021720886,
    "safety_risk": 0.09559440612792969,
    "score": 0.6088584065437317,
    "selective_product_yield": 0.1496986299753189,
    "transport_efficiency": 0.8966293931007385
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
      "current_mA": 100,
      "electrolyte_profile": 2,
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
    "cost": 0.32708001136779785,
    "electrochemical_conversion": 0.1371329426765442,
    "electrochemical_selectivity": 0.7610573172569275,
    "energy_efficiency": 0.7012686133384705,
    "faradaic_efficiency": 0.7836040258407593,
    "ohmic_efficiency": 0.9364427328109741,
    "pH_normalized": 0.1731279492378235,
    "precipitation_signal": 0.0,
    "safety_risk": 0.1135944053530693,
    "score": 0.5108447670936584,
    "selective_product_yield": 0.11207673698663712,
    "transport_efficiency": 0.7521165013313293
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
      "current_mA": 100,
      "electrolyte_profile": 3,
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
    "cost": 0.3110800087451935,
    "electrochemical_conversion": 0.09911423921585083,
    "electrochemical_selectivity": 0.7280247807502747,
    "energy_efficiency": 0.6026656031608582,
    "faradaic_efficiency": 0.5238180160522461,
    "ohmic_efficiency": 0.9737112522125244,
    "pH_normalized": 0.28910213708877563,
    "precipitation_signal": 0.0,
    "safety_risk": 0.12619440257549286,
    "score": 0.42484980821609497,
    "selective_product_yield": 0.07749635726213455,
    "transport_efficiency": 0.513308584690094
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
      "current_mA": 100,
      "electrolyte_profile": 0,
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
    "cost": 0.3014799952507019,
    "electrochemical_conversion": 0.15035194158554077,
    "electrochemical_selectivity": 0.9133784770965576,
    "energy_efficiency": 0.832826554775238,
    "faradaic_efficiency": 0.8184559345245361,
    "ohmic_efficiency": 0.9655643105506897,
    "pH_normalized": 0.2366265505552292,
    "precipitation_signal": 0.9922776222229004,
    "safety_risk": 0.09559440612792969,
    "score": 0.5753245949745178,
    "selective_product_yield": 0.14507180452346802,
    "transport_efficiency": 0.7937725782394409
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
      "current_mA": 100,
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
    "cost": 0.28547999262809753,
    "electrochemical_conversion": 0.17882715165615082,
    "electrochemical_selectivity": 0.9292353987693787,
    "energy_efficiency": 0.9075004458427429,
    "faradaic_efficiency": 0.9052276611328125,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.20319488644599915,
    "precipitation_signal": 0.8331227898597717,
    "safety_risk": 0.072194404900074,
    "score": 0.6221460103988647,
    "selective_product_yield": 0.16420932114124298,
    "transport_efficiency": 0.908627986907959
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
      "current_mA": 100,
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
    "cost": 0.28835999965667725,
    "electrochemical_conversion": 0.3319372236728668,
    "electrochemical_selectivity": 0.9259119629859924,
    "energy_efficiency": 0.9028729796409607,
    "faradaic_efficiency": 0.911121666431427,
    "ohmic_efficiency": 0.9910537004470825,
    "pH_normalized": 0.2014974057674408,
    "precipitation_signal": 0.8459956645965576,
    "safety_risk": 0.072194404900074,
    "score": 0.67449551820755,
    "selective_product_yield": 0.29300838708877563,
    "transport_efficiency": 0.9046263098716736
  }
}
```

### 批次 9 · 终点事件 64

```json
{
  "ordinal": 9,
  "lifecycle_index": 9,
  "end_step": 64,
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
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 14400,
      "operation": "electrolyze"
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
    "cost": 0.3121199905872345,
    "electrochemical_conversion": 0.7044289112091064,
    "electrochemical_selectivity": 0.9451497197151184,
    "energy_efficiency": 0.960247278213501,
    "faradaic_efficiency": 0.9378814101219177,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.20351119339466095,
    "precipitation_signal": 0.8538698554039001,
    "safety_risk": 0.072194404900074,
    "score": 0.8520542979240417,
    "selective_product_yield": 0.6912827491760254,
    "transport_efficiency": 0.9587126970291138
  }
}
```

### 批次 10 · 终点事件 73

```json
{
  "ordinal": 10,
  "lifecycle_index": 10,
  "end_step": 73,
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
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 14400,
      "operation": "electrolyze"
    },
    {
      "duration_s": 14400,
      "operation": "electrolyze"
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
    "cost": 0.3315488398075104,
    "electrochemical_conversion": 0.6300704479217529,
    "electrochemical_selectivity": 0.9665308594703674,
    "energy_efficiency": 0.9505794644355774,
    "faradaic_efficiency": 0.9603592753410339,
    "ohmic_efficiency": 0.9655799269676208,
    "pH_normalized": 0.2011970430612564,
    "precipitation_signal": 0.8430317044258118,
    "safety_risk": 0.072194404900074,
    "score": 0.8132306933403015,
    "selective_product_yield": 0.5799890160560608,
    "transport_efficiency": 0.9617088437080383
  }
}
```

### 批次 11 · 终点事件 82

```json
{
  "ordinal": 11,
  "lifecycle_index": 11,
  "end_step": 82,
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
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 14400,
      "operation": "electrolyze"
    },
    {
      "duration_s": 14400,
      "operation": "electrolyze"
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
    "cost": 0.33047720789909363,
    "electrochemical_conversion": 0.6968751549720764,
    "electrochemical_selectivity": 0.9441729187965393,
    "energy_efficiency": 0.9436930418014526,
    "faradaic_efficiency": 0.9500468373298645,
    "ohmic_efficiency": 0.9775055050849915,
    "pH_normalized": 0.2021820843219757,
    "precipitation_signal": 0.8509208559989929,
    "safety_risk": 0.072194404900074,
    "score": 0.8366196751594543,
    "selective_product_yield": 0.6527451872825623,
    "transport_efficiency": 0.9572268128395081
  }
}
```

### 批次 12 · 终点事件 90

```json
{
  "ordinal": 12,
  "lifecycle_index": 12,
  "end_step": 90,
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
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 14400,
      "operation": "electrolyze"
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
    "cost": 0.3121199905872345,
    "electrochemical_conversion": 0.6899223923683167,
    "electrochemical_selectivity": 0.9369825124740601,
    "energy_efficiency": 0.9202298521995544,
    "faradaic_efficiency": 0.9124228358268738,
    "ohmic_efficiency": 0.9902722835540771,
    "pH_normalized": 0.20270240306854248,
    "precipitation_signal": 0.8442568182945251,
    "safety_risk": 0.072194404900074,
    "score": 0.8351850509643555,
    "selective_product_yield": 0.6851121783256531,
    "transport_efficiency": 0.9336477518081665
  }
}
```

## K1 封存报告

Mechanistic report

I interpret this world as a charge-driven electrochemical conversion with three coupled layers: (1) potential-dependent interfacial kinetics and reaction direction, (2) electrolyte/solvent control of charge and mass transport, and (3) a finite useful-charge window beyond which additional electrolysis gives little benefit or promotes loss of useful product. This is an empirical explanation of the simulated world, not a claim about any identified real chemical system; all material labels are anonymous benchmark labels.

1. Directly observed operating behavior

All comparisons below used 0.020 mol limiting reagent in 0.040 L solvent. Except for batch 2, the polarity was +1.0 V; every controlled run used a 100 mA current cap.

• Polarity had a large effect. With S0/E0 and 7200 s, batch 1 at +1.0 V scored 0.509, with conversion 0.141, selectivity 0.839, selective yield 0.0959, Faradaic efficiency 0.736, transport efficiency 0.707, and energy efficiency 0.690. The matched batch 2 at −1.0 V scored only 0.292: conversion 0.0597, selectivity 0.540, yield 0.0449, Faradaic efficiency 0.363, transport efficiency 0.389, and energy efficiency 0.210. Ohmic efficiency remained high in both batches (0.966 and 0.975), so the negative-polarity failure was not principally an ohmic-resistance failure. It more likely reflected unfavorable reaction direction, interfacial kinetics, or parasitic charge consumption.

• Materials strongly affected the non-ohmic efficiencies. At +1.0 V and 7200 s, matched pairs gave: batch 1 S0/E0, score 0.509; batch 3 S1/E1, 0.609; batch 4 S2/E2, 0.511; and batch 5 S3/E3, 0.425. Batch 3 combined conversion 0.164, selectivity 0.935, Faradaic efficiency 0.880, transport efficiency 0.897, and energy efficiency 0.907. Batch 5 was weaker in conversion (0.0991), Faradaic efficiency (0.524), and transport efficiency (0.513), despite high ohmic efficiency (0.974). Thus nominal bulk conductivity alone cannot explain performance.

• Limited crossing of S0/S1 and E0/E1 suggests that E1 was the larger favorable factor. Batch 6, S1/E0, scored 0.575, whereas batch 3, S1/E1, scored 0.609. Batch 1, S0/E0, scored 0.509, whereas batch 7, S0/E1, scored 0.622. Batch 7 had conversion 0.179, selectivity 0.929, yield 0.164, Faradaic efficiency 0.905, transport efficiency 0.909, ohmic efficiency reported at 1.000, and energy efficiency 0.908. The S0 versus S1 effect was smaller and less secure: S0/E1 exceeded S1/E1 by only 0.013 score units, and those conditions were not replicated as a paired material comparison.

• At S0/E1, duration—hence accumulated charge exposure—was the most important optimized continuous variable. At 7200 s, batch 7 scored 0.622 with conversion 0.179 and yield 0.164. At 14400 s, batch 8 scored 0.674 with conversion 0.332 and yield 0.293. At 28800 s, batch 9 reached the campaign maximum score of 0.852, conversion 0.704, selectivity 0.945, yield 0.691, Faradaic efficiency 0.938, transport efficiency 0.959, ohmic efficiency 1.000, and energy efficiency 0.960.

• The duration response was non-monotonic across independent batches. Batch 11 at 32400 s scored 0.837, with conversion 0.697 and yield 0.653. Batch 10 at 43200 s scored 0.813, with conversion 0.630 and yield 0.580, although its selectivity and efficiencies remained high: selectivity 0.967, Faradaic efficiency 0.960, transport efficiency 0.962, and energy efficiency 0.951. An exact-condition repeat of the 28800 s recipe, batch 12, scored 0.835, with conversion 0.690 and yield 0.685. Therefore the 28800–32400 s region is reproducibly high-performing, but the exact numerical superiority of batch 9 is not established as a deterministic duration effect.

2. Proposed process model

A useful qualitative current model is

I(t) = min[I_cap, I_kin(E_eff,state), I_transport(state), E_drive/R_ohmic],

where I_cap was 100 mA in the controlled campaign, E_eff is the applied potential corrected for solvent/electrolyte shifts and the instantaneous interfacial state, and I_transport includes diffusion-layer and concentration limitations. The accumulated charge is Q = integral I(t)dt. No current trace was measured, so Q cannot be computed from duration and the cap alone; treating 100 mA × time as delivered charge would be unjustified.

The desired pathway can be represented schematically as

R + charge → P,
R + charge → B,
P + excess charge/time → D,

where R is the limiting reactant, P the desired product, B competing products, and D degraded or otherwise non-useful material. A minimal kinetic description would be

dR/dt = −r_des(E_eff,R,transport) − r_side(E_eff,R,state),
dP/dt = r_des − r_loss(E_eff,P,state),

with instantaneous Faradaic efficiency approximately equal to useful reaction current divided by total current. Selectivity describes partitioning among chemical pathways, while transport and ohmic efficiencies determine how effectively the imposed electrical conditions reach the reactive interface. Selective yield should consequently increase with conversion and selectivity but can be reduced by product loss, incomplete recovery, or state-dependent assay definitions. The measurements roughly support this coupling, although selective yield is not exactly conversion × selectivity in every batch, so I would not impose that identity as a law.

Positive polarization evidently places the interface in the favorable kinetic regime. Negative polarization still passed charge efficiently enough to retain high ohmic efficiency, but much less of that electrical input reached the desired transformation. This explains why batch 2 simultaneously had poor Faradaic, transport, energy, conversion, and selectivity values without an ohmic collapse.

The nominal dossier offers a plausible basis for the E1 result. E1 had the highest declared diffusivity and a relatively thin diffusion layer, properties expected to increase mass-transfer-limited current. Its bulk conductivity was not the highest, yet experimental ohmic efficiency was already near unity; therefore increasing conductivity further could offer little benefit compared with improving interfacial supply and suppressing parasitic chemistry. S0 had favorable relative conductivity, while E1 supplied favorable diffusivity/thin-layer properties, so S0/E1 may combine good ohmic behavior with good transport. This is a mechanistic interpretation, not an identified causal decomposition: hidden, fixed solvent–electrolyte residuals and interface factors were explicitly part of the world.

3. Why duration has an optimum

From 7200 through 28800 s, extra electrolysis mainly increased conversion and selective yield while selectivity and all three electrical efficiencies stayed high. The public score weights selective yield most heavily, so this rise in useful product explains much of the score improvement. Beyond that region, the lower yield in batches 11 and 10 is consistent with one or more of the following:

• depletion of easily converted reactant, causing marginal charge to enter side reactions;
• product oxidation/reduction or other charge-induced degradation;
• electrode passivation or changing interfacial coverage;
• concentration polarization or local composition changes;
• batch-to-batch stochastic process variation.

The evidence does not uniquely select among these mechanisms. Importantly, the 43200 s experiment was a separate batch, not a time-series measurement of batch 9; therefore I did not literally observe conversion decrease within one vessel. The apparent downturn is a cross-batch response. The difference between the two nominally identical 28800 s runs—scores 0.852 and 0.835—also demonstrates meaningful run-to-run and/or measurement variability. Still, both 28800 s runs were strong, and the 43200 s yield deficit was sufficiently large to make a genuine overexposure region plausible.

A compact empirical response could be written as

useful yield(Q) ≈ formation(Q) − loss(Q),

where formation initially rises with Q and saturates as R is depleted, while loss is small at low Q but becomes important after a threshold. A form such as A[1−exp(−kQ)]−B·max(0,Q−Q0)^n would reproduce the observed qualitative shape, but the campaign does not identify its parameters or prove that charge rather than elapsed time is the true independent variable.

4. pH and precipitation coupling

For the high-performing S0/E1 duration series, normalized pH remained close to 0.20: 0.203 in batch 7, 0.201 in batch 8, 0.204 in batch 9, 0.201 in batch 10, 0.202 in batch 11, and 0.203 in batch 12. Precipitation signal was likewise consistently high, approximately 0.833–0.854. Thus the major duration-dependent changes in conversion and yield did not coincide with large changes in these two terminal observables.

Across materials, precipitation varied much more: it was 1.000 in batches 1–2, 0.651 in batch 3, zero in batches 4–5, 0.992 in batch 6, and 0.833 in batch 7. Nevertheless, zero-precipitation batches 4–5 did not outperform the high-precipitation E1 batches. Precipitation is therefore not a simple universally harmful bottleneck in the tested space. It may report electrolyte equilibria or an inactive salt pool rather than direct loss of target. Alternatively, its effects could be offset by superior E1 transport. Because no isolated precipitation intervention was made, causality is unidentifiable.

5. Relation to the balanced score

The score combined selective product yield, conversion, selectivity, Faradaic efficiency, transport efficiency, ohmic efficiency, and energy efficiency, with selective yield carrying the largest stated weight. This explains why batch 9 outranked the very selective batch 10: batch 10 had slightly higher selectivity and Faradaic efficiency but materially lower conversion and selective yield. The optimized world is consequently not one in which maximum selectivity alone is sufficient. It rewards a joint regime where substantial reactant is converted before excess electrical exposure erodes useful output, while electrical and transport losses remain low.

6. What changed the explanation

The initial prior was that moderate positive overpotential would outperform excessive or wrong-signed polarization, and that conductivity and diffusivity might trade off. Batches 1–2 established the strong polarity asymmetry. Batches 3–5 showed that high nominal conductivity or low precipitation alone could not rank the materials. Batches 6–7 changed the material explanation from a vague preference for the matched S1/E1 pair to a more specific, though still provisional, preference for E1 and the S0/E1 combination. Batches 8–9 showed that the early 7200 s screen greatly undercharged the useful reaction. Batch 10 rejected simple monotonic improvement with duration. Batch 11 localized the useful region, while batch 12 showed that batch 9's exact score should not be treated as perfectly repeatable even though the operating region remained strong.

7. Scope and unidentifiable factors

The explanation is local to 0.020 mol reagent, 0.040 L solvent, the tested anonymous materials, ±1.0 V polarity comparison, +1.0 V optimization, a 100 mA cap, and total electrolysis times of 7200–43200 s. Reagent concentration, solvent volume, potential magnitude other than 1.0 V, and current cap were not independently varied. Consequently, duration cannot be cleanly separated from delivered charge, and the optimum cannot be extrapolated safely to another loading, electrode geometry, resistance, or current cap.

Only a subset of solvent/electrolyte crosses was tested. S2 and S3 were confounded with E2 and E3, respectively. The small S0/S1 difference under E1 lacks replicate support. Hidden fixed world residuals, solvent–electrolyte interactions, electrode area/gap/contact resistance, kinetic transfer coefficients, electron stoichiometry, true instantaneous current, reactant/product concentration histories, and identities of side products are all unobserved. Terminal assay noise and process variability prevent fine ranking of batches 9, 11, and 12 as mechanistically distinct regimes.

Plausible alternatives include: E1 may improve intrinsic interfacial selectivity rather than transport; S0/E1 may benefit from a hidden interaction not represented by nominal properties; the long-duration downturn may be process variability rather than product degradation; precipitation may passivate the electrode beneficially rather than merely remove material; or segmentation into repeated 14400 s operations may itself alter state in a way not captured by total duration. The campaign cannot eliminate these alternatives.

Overall, the most defensible account is a polarity-selective desired electron-transfer pathway whose observable productivity is jointly controlled by material-dependent transport/interfacial efficiency and accumulated electrical exposure. S0/E1 at +1.0 V accessed a high-efficiency regime, and roughly 28800 s at the tested loading balanced formation against late-stage loss. Batch 9 was the highest observed instance, while batch 12 supports the robustness of the operating region rather than the exact maximum score.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific mechanism, response law, or ground-truth prior was supplied. The supplied information was a nominal material-property dossier plus the scoring and instrument contracts. The dossier was explicitly incomplete and allowed hidden world-specific residuals, so I treated it as a qualitative prior rather than a predictive law.

Supported claims:
• Reaction polarity matters strongly. At otherwise matched S0/E0 conditions, positive polarization in batch 1 scored 0.509, versus 0.292 for negative polarization in batch 2. Conversion, selectivity, Faradaic efficiency, transport efficiency, and energy efficiency all favored +1.0 V. This was the clearest evidence changing my judgment from an initially generic expectation of a signed response to confidence that the positive direction was preferred.
• Electrolyte E1 is favorable within the tested material subset. Replacing E0 with E1 improved S0 performance from batch 1 (score 0.509) to batch 7 (0.622), while the analogous S1 comparison improved from batch 6 (0.575) to batch 3 (0.609). The crossing changed my initial interpretation: after batch 3 I could not tell whether S1, E1, or their interaction was responsible; batches 6–7 shifted the evidence toward E1 as the larger contribution.
• Useful output has a non-monotonic exposure response near the tested optimum. With S0/E1, score rose from 0.622 at 7200 s in batch 7 to 0.674 at 14400 s in batch 8 and 0.852 at 28800 s in batch 9. It then fell to 0.837 at 32400 s in batch 11 and 0.813 at 43200 s in batch 10. This contradicted a simple monotonic-duration law and motivated the proposed competition between formation and late-stage loss or diminishing returns.
• The 28800 s region is robustly good, although its exact optimum is uncertain. The exact-condition repeat in batch 12 scored 0.835 rather than batch 9’s 0.852, but retained high yield and efficiency. This supported the operating region while weakening any claim that batch 9’s precise score is deterministic.
• Bulk conductivity alone is not an adequate ranking variable. Batch 5 had high ohmic efficiency but weak Faradaic and transport efficiencies and a score of 0.425. Conversely, E1 performed well despite not having the highest nominal bulk conductivity. The evidence favors coupled transport, interfacial kinetics, and selectivity rather than a one-variable conductivity law.

Contradicted or weakened claims:
• A simple “more electrolysis is always better” relationship was contradicted by batches 10–11 relative to batch 9.
• A simple “less precipitation is better” rule was contradicted as a general ranking rule. Batches 4–5 had zero precipitation signal yet did not outperform the high-precipitation S0/E1 batches. This does not prove precipitation is harmless; it shows that its isolated effect was not identifiable and was not dominant over the tested material differences.
• The early apparent preference for the matched S1/E1 pair was weakened by batch 7, where S0/E1 scored higher. The S0–S1 difference remains too small and insufficiently replicated to call a firm solvent law.

Untested claims:
• The separate causal effects of delivered current, current cap, potential magnitude, reagent concentration, and volume were not tested. All optimized batches used +1.0 V and a 100 mA cap.
• The proposed product-loss, passivation, or secondary-electrolysis mechanism was not observed directly. The long-duration downturn occurred across independent batches, not as a time series within one vessel.
• Electron stoichiometry, actual current, accumulated charge, identities of side products, and kinetic rate laws remain unknown.
• Most solvent–electrolyte interactions remain untested. S2 and S3 were confounded with E2 and E3 in batches 4–5.

2. One additional discriminating experiment

I would repeat the complete batch-10 condition: 0.020 mol reagent, 0.040 L S0, E1, +1.0 V, 100 mA cap, and 43200 s total electrolysis, followed by the final assay. This directly tests the leading interpretation that exposure beyond the approximately 28800 s region reproducibly reduces useful yield, against the alternative that batch 10 was mainly an unfavorable stochastic realization.

Before seeing the result, I would interpret another selective yield near or below about 0.62 with a score near or below about 0.82 as support for a reproducible overexposure region, because it would agree with batch 10 and remain below both 28800 s batches 9 and 12. A result around selective yield 0.67 or higher and score 0.84 or higher would weaken the degradation/overexposure explanation and favor substantial run-to-run variability or a broad, flat optimum. A much higher result would contradict the claimed downturn. A repeat low score accompanied by persistently high selectivity and efficiencies would particularly support late-stage loss or reduced recovery rather than a general electrical-efficiency collapse. One repeat would still not distinguish product degradation from passivation, depletion, or another charge-dependent process; that would require time-resolved composition or a designed no-charge hold comparison.

3. Unused evidence, weak predictions, and goal effects

The raw spectral artifacts were not analyzed, and intermediate UV–visible measurements were used mainly as qualitative consistency checks rather than fitted quantitatively. Cost and safety readouts did not become active discriminators because the tested recipes remained within the safety limit. The pH and precipitation observations were summarized but not subjected to targeted interventions. Much of the nominal dossier—especially capacitance, acid properties, solubility-product information, and standard-potential shifts—remained only qualitative because the campaign lacked enough orthogonal material crosses to estimate their separate effects.

The least reliable blind predictions are Q01–Q02 because 600 s lies far outside the duration region characterized during optimization and places selective yield near the score’s multiplicative gate. Q07–Q10 are also weak because they require untested S0/E3 and S2/E0 crosses. Q11–Q12 extrapolate from a 100 mA to a 500 mA cap without measured current, so their assumption that the higher cap is nonbinding is uncertain. Even Q03–Q06 involve +/−0.8 V, a smaller reagent inventory, and a slightly different concentration from the campaign. The polarity ordering is more reliable than their numerical values.

The recommendation of batch 9 is reliable as the highest observed completed batch, but less reliable as a uniquely optimal recipe. Batches 11 and 12 scored only modestly lower, and batch 12 demonstrated appreciable exact-condition variation. The strongest recommendation is therefore the S0/E1, positive-potential, roughly 28800–32400 s region, not the exact score or an infinitely precise duration optimum.

The assigned maximization goal did affect evidence collection. After the material screen identified S0/E1 as promising, most remaining batches exploited duration near that condition. This improved the achieved score and provided one exact repeat, but left potential magnitude, current cap, concentration, and most material interactions poorly identified. There was no clear conflict between maximizing score and learning during the early screen, but later exploitation reduced the breadth and causal identifiability of the final mechanism.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.4,
        "upper80": 0.68
      },
      "energy_efficiency": {
        "estimate": 0.22,
        "lower80": 0.08,
        "upper80": 0.39
      },
      "faradaic_efficiency": {
        "estimate": 0.34,
        "lower80": 0.18,
        "upper80": 0.49
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.07,
        "lower80": 0.015,
        "upper80": 0.16
      },
      "selective_product_yield": {
        "estimate": 0.0045,
        "lower80": 0,
        "upper80": 0.012
      },
      "transport_efficiency": {
        "estimate": 0.37,
        "lower80": 0.2,
        "upper80": 0.54
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.85,
        "lower80": 0.74,
        "upper80": 0.93
      },
      "energy_efficiency": {
        "estimate": 0.7,
        "lower80": 0.56,
        "upper80": 0.83
      },
      "faradaic_efficiency": {
        "estimate": 0.72,
        "lower80": 0.6,
        "upper80": 0.82
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.29,
        "lower80": 0.14,
        "upper80": 0.45
      },
      "selective_product_yield": {
        "estimate": 0.012,
        "lower80": 0.003,
        "upper80": 0.026
      },
      "transport_efficiency": {
        "estimate": 0.7,
        "lower80": 0.56,
        "upper80": 0.82
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.57,
        "lower80": 0.46,
        "upper80": 0.67
      },
      "energy_efficiency": {
        "estimate": 0.25,
        "lower80": 0.15,
        "upper80": 0.36
      },
      "faradaic_efficiency": {
        "estimate": 0.38,
        "lower80": 0.29,
        "upper80": 0.48
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.312,
        "lower80": 0.24,
        "upper80": 0.39
      },
      "selective_product_yield": {
        "estimate": 0.055,
        "lower80": 0.035,
        "upper80": 0.078
      },
      "transport_efficiency": {
        "estimate": 0.41,
        "lower80": 0.3,
        "upper80": 0.53
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.86,
        "lower80": 0.78,
        "upper80": 0.92
      },
      "energy_efficiency": {
        "estimate": 0.72,
        "lower80": 0.61,
        "upper80": 0.82
      },
      "faradaic_efficiency": {
        "estimate": 0.74,
        "lower80": 0.65,
        "upper80": 0.82
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.536,
        "lower80": 0.46,
        "upper80": 0.61
      },
      "selective_product_yield": {
        "estimate": 0.14,
        "lower80": 0.105,
        "upper80": 0.18
      },
      "transport_efficiency": {
        "estimate": 0.72,
        "lower80": 0.62,
        "upper80": 0.81
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.65,
        "lower80": 0.5,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.35,
        "lower80": 0.2,
        "upper80": 0.51
      },
      "faradaic_efficiency": {
        "estimate": 0.5,
        "lower80": 0.35,
        "upper80": 0.65
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.375,
        "lower80": 0.27,
        "upper80": 0.48
      },
      "selective_product_yield": {
        "estimate": 0.07,
        "lower80": 0.035,
        "upper80": 0.11
      },
      "transport_efficiency": {
        "estimate": 0.56,
        "lower80": 0.4,
        "upper80": 0.7
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.94,
        "lower80": 0.87,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.93,
        "lower80": 0.84,
        "upper80": 0.99
      },
      "faradaic_efficiency": {
        "estimate": 0.91,
        "lower80": 0.83,
        "upper80": 0.97
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.65,
        "lower80": 0.57,
        "upper80": 0.72
      },
      "selective_product_yield": {
        "estimate": 0.22,
        "lower80": 0.17,
        "upper80": 0.28
      },
      "transport_efficiency": {
        "estimate": 0.92,
        "lower80": 0.83,
        "upper80": 0.98
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.52,
        "lower80": 0.36,
        "upper80": 0.67
      },
      "energy_efficiency": {
        "estimate": 0.18,
        "lower80": 0.06,
        "upper80": 0.34
      },
      "faradaic_efficiency": {
        "estimate": 0.28,
        "lower80": 0.14,
        "upper80": 0.44
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.266,
        "lower80": 0.17,
        "upper80": 0.37
      },
      "selective_product_yield": {
        "estimate": 0.035,
        "lower80": 0.012,
        "upper80": 0.065
      },
      "transport_efficiency": {
        "estimate": 0.32,
        "lower80": 0.16,
        "upper80": 0.49
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.76,
        "lower80": 0.63,
        "upper80": 0.86
      },
      "energy_efficiency": {
        "estimate": 0.7,
        "lower80": 0.56,
        "upper80": 0.82
      },
      "faradaic_efficiency": {
        "estimate": 0.6,
        "lower80": 0.46,
        "upper80": 0.73
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.472,
        "lower80": 0.37,
        "upper80": 0.57
      },
      "selective_product_yield": {
        "estimate": 0.1,
        "lower80": 0.06,
        "upper80": 0.15
      },
      "transport_efficiency": {
        "estimate": 0.58,
        "lower80": 0.43,
        "upper80": 0.71
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.43,
        "upper80": 0.71
      },
      "energy_efficiency": {
        "estimate": 0.22,
        "lower80": 0.09,
        "upper80": 0.37
      },
      "faradaic_efficiency": {
        "estimate": 0.34,
        "lower80": 0.2,
        "upper80": 0.49
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.291,
        "lower80": 0.19,
        "upper80": 0.4
      },
      "selective_product_yield": {
        "estimate": 0.045,
        "lower80": 0.018,
        "upper80": 0.08
      },
      "transport_efficiency": {
        "estimate": 0.35,
        "lower80": 0.21,
        "upper80": 0.51
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.82,
        "lower80": 0.7,
        "upper80": 0.9
      },
      "energy_efficiency": {
        "estimate": 0.67,
        "lower80": 0.53,
        "upper80": 0.79
      },
      "faradaic_efficiency": {
        "estimate": 0.68,
        "lower80": 0.55,
        "upper80": 0.79
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.494,
        "lower80": 0.39,
        "upper80": 0.59
      },
      "selective_product_yield": {
        "estimate": 0.12,
        "lower80": 0.075,
        "upper80": 0.17
      },
      "transport_efficiency": {
        "estimate": 0.62,
        "lower80": 0.48,
        "upper80": 0.74
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.57,
        "lower80": 0.44,
        "upper80": 0.69
      },
      "energy_efficiency": {
        "estimate": 0.25,
        "lower80": 0.13,
        "upper80": 0.38
      },
      "faradaic_efficiency": {
        "estimate": 0.38,
        "lower80": 0.27,
        "upper80": 0.5
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.31,
        "lower80": 0.22,
        "upper80": 0.41
      },
      "selective_product_yield": {
        "estimate": 0.055,
        "lower80": 0.03,
        "upper80": 0.085
      },
      "transport_efficiency": {
        "estimate": 0.41,
        "lower80": 0.28,
        "upper80": 0.55
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.86,
        "lower80": 0.76,
        "upper80": 0.93
      },
      "energy_efficiency": {
        "estimate": 0.72,
        "lower80": 0.59,
        "upper80": 0.84
      },
      "faradaic_efficiency": {
        "estimate": 0.74,
        "lower80": 0.63,
        "upper80": 0.84
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.535,
        "lower80": 0.44,
        "upper80": 0.63
      },
      "selective_product_yield": {
        "estimate": 0.14,
        "lower80": 0.095,
        "upper80": 0.19
      },
      "transport_efficiency": {
        "estimate": 0.72,
        "lower80": 0.59,
        "upper80": 0.83
      }
    }
  ],
  "rationale": "Predictions are anchored to the campaign’s matched ±1.0 V S0/E0 batches, the S0/E1 material comparison, and the observed duration response. I scaled charge-limited conversion and yield for the slightly lower concentration and smaller reagent inventory, allowed ±0.8 V to reduce driving force, and treated the 500 mA cap as probably nonbinding at 0.8 V. Positive polarity is therefore predicted to retain much higher selectivity and electrical efficiencies than negative polarity, E1 to remain favorable, and 600 s runs to fall near or below the selective-yield score gate. Intervals include assay noise, run-to-run variation, and substantial extrapolation uncertainty for untested potential, cap, and material crosses."
}
```
