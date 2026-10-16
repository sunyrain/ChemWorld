# repeat-02/EC-W04-B12-optimization-E-MisIndexed

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-02\EC-W04-B12-optimization-E-MisIndexed\participant\optimization-E-MisIndexed

## 同期笔记

### v1 · 公开事件 0

# Electrochemical campaign hypotheses

## H1 [tentative; pre-experiment]
At fixed 0.02 mol reagent in 0.04 L solvent, the balanced score should have an interior optimum in potential magnitude and electrolysis time: insufficient charge limits conversion, whereas excessive driving force/time reduces selectivity and energy efficiency. A first-pass material screen will use both potential signs and UV–vis after a short segment; if conversion is low without degradation evidence, a second segment should improve yield.

## H2 [tentative; pre-experiment]
Transport and ohmic efficiency should favor high nominal conductivity, but selectivity may instead favor lower proton activity and capacitance. Thus solvent S0/electrolyte E2 is the nominal transport benchmark, while S2 or S3 may outperform on selectivity. Material effects remain unresolved until final assays.

Decision: screen broad material/polarity/current/time combinations, then allocate later batches to local refinement and repeatability. A large score reversal by polarity or strong precipitation will supersede nominal-property expectations.

### v2 · 公开事件 16

# Electrochemical campaign hypotheses

## H1 [revised; early evidence]
At fixed 0.02 mol/0.04 L, both ±1.0 V for 1200 s gave very low conversion. Positive polarity produced no detected selective yield (event runner-operation-0008), whereas negative polarity produced a small yield and score ~0.304 (runner-operation-0016). The numerical polarity difference supports screening negative potentials more strongly, but both are near the low-yield/gating region and one run each cannot establish repeatability.

## H2 [unresolved]
Nominal conductivity may improve ohmic efficiency, while solvent proton activity/capacitance may control selectivity. E0/S0 showed precipitation signal at its upper bound in both polarity tests, a likely material confound and reason to prioritize lower-precipitating E1–E3.

## H3 [tentative]
Charge/time is the immediate limiting factor at ±1 V and 100 mA. Raising negative overpotential and extending time should increase conversion and selective yield, with an interior optimum once efficiency/selectivity losses dominate. I will next screen E1–E3 and solvents S1–S3 at stronger negative bias; a positive-polarity rescue would reopen the sign hypothesis.

### v3 · 公开事件 80

# Electrochemical campaign hypotheses

## H1 [supported in tested scope]
Negative polarity is productive; positive +1.5 V was essentially inactive (runner-operation-0032). Under E2/S0, extending electrolysis to 14,400 s at a 500 mA cap raised conversion and yield substantially. At -0.8 V the score was ~0.572 (runner-operation-0072), and at -0.6 V ~0.584 (runner-operation-0080). The latter improved selectivity and yield numerically despite lower ohmic efficiency. This supports an interior optimum at moderate negative potential rather than maximum overpotential.

## H2 [supported in tested scope, material interaction unresolved]
E2 avoids the saturated precipitation seen with E0 and is the best electrolyte tested so far. At -1.2 V and 7200 s, S0/E2 scored ~0.352 (runner-operation-0056), exceeding S1/E2 (~0.328; runner-operation-0064) and S2/E2 (~0.318; runner-operation-0040). S0/E2 is therefore the refinement platform, though comparisons are single runs and solvent/E2 residual interaction may matter.

## H3 [refined]
Long duration is needed at the fixed loading. Between -0.8 and -0.6 V for 14,400 s, the balance shifts toward better selectivity/energy at milder bias without losing conversion. Test -0.4 to -0.7 V and duration near or above 14,400 s; if conversion collapses at -0.4 V, concentrate remaining runs around -0.55 to -0.65 V. Current cap remains a confound because delivered current is unobserved.

### v4 · 公开事件 96

# Electrochemical campaign hypotheses

## H1 [supported in tested scope]
Productive operation requires negative polarity. Positive controls were inactive or yielded no target (runner-operation-0008; runner-operation-0032), while negative conditions gave measurable selective yield. This sign conclusion is strong within the tested materials and loading, though the exact onset depends on material potential shifts.

## H2 [supported in tested scope]
S0/E2 is the best tested material pair. E2 avoided the saturated precipitation observed with E0, and S0/E2 outscored S1/E2 and S2/E2 under the matched -1.2 V, 7200 s comparison (runner-operation-0056 versus runner-operation-0064 and runner-operation-0040). Single-run material comparisons leave residual interaction and run noise unresolved.

## H3 [supported operating window; precise optimum unresolved]
At 0.02 mol reagent in 0.04 L S0 with E2 and a 500 mA cap, 14,400 s total electrolysis produced the highest scores in the moderate-bias region. Observed scores were ~0.572 at -0.8 V (runner-operation-0072), ~0.584 at -0.6 V (runner-operation-0080), ~0.570 at -0.4 V (runner-operation-0088), and ~0.569 at -0.5 V (runner-operation-0096). Thus -0.6 V is the best observed procedure, balancing yield/selectivity against ohmic and energy efficiency. The small differences among -0.4 to -0.8 V are not a replicated proof of a sharp optimum, especially given declared assay noise.

## Recommendation decision
Select lifecycle batch 10: S0, 0.02 mol in 0.04 L; E2; -0.6 V; 500 mA cap; two 7200 s segments (14,400 s total). It has the highest observed balanced score (~0.584), high conversion (~0.819) and the best observed balance rather than the maximum yield alone. I would change this decision if replicated neighboring potentials showed a reliably higher mean score or if the delivered-current response at a lower cap improved ohmic efficiency without sacrificing conversion.

## 实际批次及公开测量

### 批次 1 · 终点事件 8

```json
{
  "ordinal": 1,
  "lifecycle_index": 1,
  "end_step": 8,
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.04
    },
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "current_mA": 100,
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
      "duration_s": 600,
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
    "cost": 0.30107998847961426,
    "electrochemical_conversion": 0.019269946962594986,
    "electrochemical_selectivity": 1.0,
    "energy_efficiency": 0.34582966566085815,
    "faradaic_efficiency": 0.3532553017139435,
    "ohmic_efficiency": 0.9572166204452515,
    "pH_normalized": 0.23440778255462646,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.3245515525341034
  }
}
```

### 批次 2 · 终点事件 16

```json
{
  "ordinal": 2,
  "lifecycle_index": 2,
  "end_step": 16,
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.04
    },
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "current_mA": 100,
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
      "duration_s": 600,
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
    "cost": 0.30107998847961426,
    "electrochemical_conversion": 0.007372461259365082,
    "electrochemical_selectivity": 0.6828215718269348,
    "energy_efficiency": 0.262262225151062,
    "faradaic_efficiency": 0.4557437598705292,
    "ohmic_efficiency": 0.9660544395446777,
    "pH_normalized": 0.2317124307155609,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.30379441380500793,
    "selective_product_yield": 0.018511246889829636,
    "transport_efficiency": 0.48200055956840515
  }
}
```

### 批次 3 · 终点事件 24

```json
{
  "ordinal": 3,
  "lifecycle_index": 3,
  "end_step": 24,
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "current_mA": 300,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -1.5
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
      "duration_s": 1800,
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
    "cost": 0.32308000326156616,
    "electrochemical_conversion": 0.07378650456666946,
    "electrochemical_selectivity": 0.4613584578037262,
    "energy_efficiency": 0.10701547563076019,
    "faradaic_efficiency": 0.2515575587749481,
    "ohmic_efficiency": 0.8830609917640686,
    "pH_normalized": 0.2056807428598404,
    "precipitation_signal": 0.7100405097007751,
    "safety_risk": 0.09559440612792969,
    "score": 0.22814659774303436,
    "selective_product_yield": 0.02622874826192856,
    "transport_efficiency": 0.26811447739601135
  }
}
```

### 批次 4 · 终点事件 32

```json
{
  "ordinal": 4,
  "lifecycle_index": 4,
  "end_step": 32,
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "current_mA": 300,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 1.5
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
      "duration_s": 1800,
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
    "cost": 0.32308000326156616,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.02824951522052288,
    "ohmic_efficiency": 0.8952191472053528,
    "pH_normalized": 0.20499014854431152,
    "precipitation_signal": 0.7107887864112854,
    "safety_risk": 0.09559440612792969,
    "score": 0.002971213310956955,
    "selective_product_yield": 0.0007897500181570649,
    "transport_efficiency": 0.0
  }
}
```

### 批次 5 · 终点事件 40

```json
{
  "ordinal": 5,
  "lifecycle_index": 5,
  "end_step": 40,
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.04
    },
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "current_mA": 300,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -1.2
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
      "duration_s": 3600,
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
    "cost": 0.35256800055503845,
    "electrochemical_conversion": 0.1940883845090866,
    "electrochemical_selectivity": 0.5864611864089966,
    "energy_efficiency": 0.2237996608018875,
    "faradaic_efficiency": 0.34961551427841187,
    "ohmic_efficiency": 0.8194314241409302,
    "pH_normalized": 0.17906564474105835,
    "precipitation_signal": 0.0,
    "safety_risk": 0.1135944053530693,
    "score": 0.31786176562309265,
    "selective_product_yield": 0.11831600964069366,
    "transport_efficiency": 0.3391060531139374
  }
}
```

### 批次 6 · 终点事件 48

```json
{
  "ordinal": 6,
  "lifecycle_index": 6,
  "end_step": 48,
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 3,
      "volume_L": 0.04
    },
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "current_mA": 300,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": -1.2
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
      "duration_s": 3600,
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
    "cost": 0.3365679979324341,
    "electrochemical_conversion": 0.0774138867855072,
    "electrochemical_selectivity": 0.48432809114456177,
    "energy_efficiency": 0.089149609208107,
    "faradaic_efficiency": 0.15638358891010284,
    "ohmic_efficiency": 0.915895938873291,
    "pH_normalized": 0.27974098920822144,
    "precipitation_signal": 0.0023995577357709408,
    "safety_risk": 0.12619440257549286,
    "score": 0.21273165941238403,
    "selective_product_yield": 0.045869603753089905,
    "transport_efficiency": 0.13170024752616882
  }
}
```

### 批次 7 · 终点事件 56

```json
{
  "ordinal": 7,
  "lifecycle_index": 7,
  "end_step": 56,
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.04
    },
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "current_mA": 300,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -1.2
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
      "duration_s": 3600,
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
    "cost": 0.3109680116176605,
    "electrochemical_conversion": 0.22718724608421326,
    "electrochemical_selectivity": 0.6166902184486389,
    "energy_efficiency": 0.23100033402442932,
    "faradaic_efficiency": 0.3875795602798462,
    "ohmic_efficiency": 0.9261735081672668,
    "pH_normalized": 0.15906445682048798,
    "precipitation_signal": 0.0,
    "safety_risk": 0.072194404900074,
    "score": 0.35178613662719727,
    "selective_product_yield": 0.1407080441713333,
    "transport_efficiency": 0.39097991585731506
  }
}
```

### 批次 8 · 终点事件 64

```json
{
  "ordinal": 8,
  "lifecycle_index": 8,
  "end_step": 64,
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "current_mA": 300,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -1.2
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
      "duration_s": 3600,
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
    "cost": 0.3269680142402649,
    "electrochemical_conversion": 0.20154458284378052,
    "electrochemical_selectivity": 0.6035888195037842,
    "energy_efficiency": 0.2361549437046051,
    "faradaic_efficiency": 0.3750971555709839,
    "ohmic_efficiency": 0.8619128465652466,
    "pH_normalized": 0.16059842705726624,
    "precipitation_signal": 0.00031451715040020645,
    "safety_risk": 0.09559440612792969,
    "score": 0.3282073140144348,
    "selective_product_yield": 0.1042214035987854,
    "transport_efficiency": 0.36860179901123047
  }
}
```

### 批次 9 · 终点事件 72

```json
{
  "ordinal": 9,
  "lifecycle_index": 9,
  "end_step": 72,
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.04
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
      "duration_s": 7200,
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
    "cost": 0.32363998889923096,
    "electrochemical_conversion": 0.7878259420394897,
    "electrochemical_selectivity": 0.6798715591430664,
    "energy_efficiency": 0.45487886667251587,
    "faradaic_efficiency": 0.41427215933799744,
    "ohmic_efficiency": 0.7664473056793213,
    "pH_normalized": 0.15938076376914978,
    "precipitation_signal": 0.008188718929886818,
    "safety_risk": 0.072194404900074,
    "score": 0.5716871023178101,
    "selective_product_yield": 0.5605104565620422,
    "transport_efficiency": 0.4351034462451935
  }
}
```

### 批次 10 · 终点事件 80

```json
{
  "ordinal": 10,
  "lifecycle_index": 10,
  "end_step": 80,
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.04
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
      "duration_s": 7200,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "duration_s": 7200,
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
    "cost": 0.3178800046443939,
    "electrochemical_conversion": 0.8191913366317749,
    "electrochemical_selectivity": 0.7378131747245789,
    "energy_efficiency": 0.4721837639808655,
    "faradaic_efficiency": 0.43953487277030945,
    "ohmic_efficiency": 0.6381409168243408,
    "pH_normalized": 0.15706662833690643,
    "precipitation_signal": 0.0,
    "safety_risk": 0.072194404900074,
    "score": 0.5836327075958252,
    "selective_product_yield": 0.5744338035583496,
    "transport_efficiency": 0.44088447093963623
  }
}
```

### 批次 11 · 终点事件 88

```json
{
  "ordinal": 11,
  "lifecycle_index": 11,
  "end_step": 88,
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.04
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
      "duration_s": 7200,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "duration_s": 7200,
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
    "cost": 0.3121199905872345,
    "electrochemical_conversion": 0.8326947093009949,
    "electrochemical_selectivity": 0.7410532236099243,
    "energy_efficiency": 0.37085965275764465,
    "faradaic_efficiency": 0.44100630283355713,
    "ohmic_efficiency": 0.4761046767234802,
    "pH_normalized": 0.15805165469646454,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.072194404900074,
    "score": 0.5703270435333252,
    "selective_product_yield": 0.6148095726966858,
    "transport_efficiency": 0.4481862485408783
  }
}
```

### 批次 12 · 终点事件 96

```json
{
  "ordinal": 12,
  "lifecycle_index": 12,
  "end_step": 96,
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.04
    },
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -0.5
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
      "duration_s": 7200,
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
    "cost": 0.3149999976158142,
    "electrochemical_conversion": 0.7949504256248474,
    "electrochemical_selectivity": 0.7167497277259827,
    "energy_efficiency": 0.4191470742225647,
    "faradaic_efficiency": 0.400448739528656,
    "ohmic_efficiency": 0.5947619080543518,
    "pH_normalized": 0.1585719734430313,
    "precipitation_signal": 0.0,
    "safety_risk": 0.072194404900074,
    "score": 0.5694025158882141,
    "selective_product_yield": 0.6057358980178833,
    "transport_efficiency": 0.4216736853122711
  }
}
```

## K1 封存报告

Mechanistic account

I interpret this world as a cathodic electrochemical conversion whose outcome is jointly controlled by effective overpotential, charge passed, interfacial selectivity, mass transport, solution resistance, proton activity, and precipitation. The public score is not simply yield: its declared weighted components are selective-product yield (0.30), selectivity (0.15), energy efficiency (0.15), faradaic efficiency (0.12), conversion (0.10), transport efficiency (0.10), and ohmic efficiency (0.08), with a low-yield gate. Consequently, a condition that maximizes conversion or yield can lose to a milder condition with better electrical efficiencies.

A useful conceptual model is

η_eff = E_applied − E_eq(materials, pH) − iR,

rate_target ≈ k_target(η_eff, medium) × available reactant × transport,

rate_side ≈ k_side(η_eff, medium) + degradation/precipitation terms,

conversion ≈ f(integral of delivered current over time, electron stoichiometry, mass transport),

selective yield ≈ conversion × selectivity,

with faradaic efficiency representing the share of charge producing desired chemistry, transport efficiency representing delivery of reactant to the interface, and ohmic efficiency decreasing as resistive loss increases. The exact functions, actual delivered current, electron stoichiometry, and hidden material residuals were not observable.

Polarity and activation

Negative potential is the productive polarity in the tested domain. The clearest matched polarity comparison used S1/E1, 300 mA, and 3,600 s total electrolysis. Batch 3 at −1.5 V produced conversion 0.0738, selectivity 0.461, selective yield 0.0262, and score 0.228. Batch 4 at +1.5 V produced conversion 0, selectivity 0, selective yield 0.00079, and score 0.00297. The earlier S0/E0 tests were consistent with this: batch 1 at +1.0 V had selective yield 0 and score 0, whereas batch 2 at −1.0 V had a small selective yield of 0.0185 and score 0.304, although both were close to the low-signal region and heavily affected by precipitation. I therefore infer a cathodic target transformation rather than a symmetric potential response.

Potential magnitude has competing effects. More negative bias can activate conversion, but it also appears to worsen energy efficiency and can promote non-target charge consumption. In the refined S0/E2 series, the best balance occurred at moderate rather than extreme negative bias. With 0.02 mol reagent in 0.04 L solvent, a 500 mA current cap, and 14,400 s total electrolysis, batch 9 at −0.8 V gave conversion 0.788, selectivity 0.680, yield 0.561, energy efficiency 0.455, and score 0.572. Batch 10 at −0.6 V improved the observed score to 0.584, with conversion 0.819, selectivity 0.738, yield 0.574, energy efficiency 0.472, faradaic efficiency 0.440, transport efficiency 0.441, and ohmic efficiency 0.638. Milder conditions did not improve the balanced score: batch 11 at −0.4 V had the highest observed yield in this local series, 0.615, but lower energy and ohmic efficiencies of 0.371 and 0.476, giving score 0.570. Batch 12 at −0.5 V gave yield 0.606 and score 0.569. Thus the evidence favors a broad compromise near −0.6 V, not a proven sharp optimum. Assay noise and the absence of replicates make differences of roughly 0.01–0.02 in score suggestive rather than definitive.

Charge and time

The early 1,200–3,600 s experiments generally had low conversion, while the 14,400 s experiments reached about 0.79–0.83 conversion. This supports charge throughput or slow transport as an important limitation. For example, batch 7 used S0/E2 at −1.2 V, a 300 mA cap, and 7,200 s total time and reached conversion 0.227 and yield 0.141. The later S0/E2 batches used both a larger current cap and twice the time and reached much higher conversion. However, time, current cap, and potential were changed together between those stages, so their individual causal contributions are not identifiable.

The current setting should be interpreted as a cap rather than proof that 500 mA was continuously delivered. Actual current traces were not observed. The decline in ohmic efficiency toward milder potentials in batches 10–11 is not the behavior of a simple fixed-resistance circuit alone, suggesting that hidden current regulation, kinetic limitation, or the benchmark’s coupled efficiency definitions matter. A plausible alternative is that the cap changes interfacial operating state while the potential determines the actual current. Future work would need delivered-current measurements or matched current-cap experiments to distinguish these possibilities.

Electrolyte and precipitation

Electrolyte E2 was the strongest tested platform. Its nominal dossier reports high bulk conductivity (15 S/m), very low precipitating-salt concentration (0.0002 mol/L), and a +0.28 V standard-potential shift. Those properties are consistent with the experimental combination of low precipitation and usable electrical performance, although the dossier is only a prior and includes hidden world-specific residuals.

E0 was clearly precipitation-prone in S0: batches 1 and 2 both returned precipitation signal 1.0. Their pH-normalized values were about 0.23 and their useful yields were negligible. E1/S1 still showed substantial precipitation, approximately 0.710 in batches 3 and 4. By contrast, E2 combinations had precipitation at or very near zero: batch 5 was 0, batch 7 was 0, batch 8 was 0.000315, batch 10 was 0, and batch 12 was 0. This is mechanistically consistent with precipitation removing active ionic material, obstructing the interface, or otherwise lowering transport and productive charge use. It also explains why nominal conductivity alone is insufficient: E0 had respectable nominal conductivity but poor observed behavior because precipitation dominated.

The E3/S3 result shows that avoiding precipitation is necessary but not sufficient. Batch 6 had precipitation only 0.0024, yet at −1.2 V, 300 mA, and 7,200 s it gave conversion 0.0774, yield 0.0459, faradaic efficiency 0.156, transport efficiency 0.132, and score 0.213. This could reflect E3’s lower nominal conductivity, solvent coupling, proton activity, or hidden interfacial kinetics.

Solvent effects

The most informative solvent comparison held E2, −1.2 V, 300 mA, 7,200 s, loading, and volume constant. Batch 7 with S0 scored 0.352, compared with batch 8 using S1 at 0.328 and batch 5 using S2 at 0.318. S0 also had the strongest observed conversion, selectivity, yield, faradaic efficiency, transport efficiency, and ohmic efficiency in that matched set: respectively 0.227, 0.617, 0.141, 0.388, 0.391, and 0.926. The corresponding S1 values were 0.202, 0.604, 0.104, 0.375, 0.369, and 0.862; S2 gave 0.194, 0.586, 0.118, 0.350, 0.339, and 0.819.

This ordering is broadly compatible with S0’s nominally high relative conductivity of 1.2. It is not explained by diffusivity alone, because S1 has higher nominal relative diffusivity (1.25 versus 0.78) but performed worse overall. I infer a coupled solvent effect involving resistance, solvation, double-layer structure, proton activity, and electrolyte-specific residuals. The data do not support assigning the difference to any one property.

Acid/base state and precipitation are also coupled to materials. The refined S0/E2 batches had pH-normalized values tightly clustered near 0.157–0.159 and essentially no precipitation, while S1/E1 was near 0.205 with precipitation about 0.71 and S0/E0 was near 0.23 with precipitation 1. These observations show association, not proof that pH directly caused precipitation, because electrolyte identity, solvent identity, salt loading, and equilibrium constants changed simultaneously.

Intermediate measurements

UV–visible measurements after the first electrolysis segment indicated that electrical efficiencies were established before final termination but could change after the second segment. In batch 10, the halfway UV–visible estimates were energy efficiency 0.526, faradaic efficiency 0.504, transport efficiency 0.463, and ohmic efficiency 0.649; the final assay after the second 7,200 s segment gave 0.472, 0.440, 0.441, and 0.638. Batch 9 similarly moved from halfway values of 0.516, 0.450, 0.454, and 0.738 to final values of 0.455, 0.414, 0.435, and 0.766. These changes are consistent with evolving composition, substrate depletion, or accumulating side products, but direct comparison is limited because UV–visible and final assay have different declared noise levels and the second electrolysis segment changed the state.

Relationship between conversion, selectivity, and yield

Across productive batches, selective yield broadly followed conversion multiplied by selectivity, as expected for a desired-product fraction, but it was not numerically identical. For batch 10, conversion 0.819 and selectivity 0.738 would imply a product near 0.60, compared with measured yield 0.574. Batch 11 similarly had conversion 0.833, selectivity 0.741, and yield 0.615. Deviations are compatible with independent assay noise, recovery or mass-balance effects hidden from the public observables, or a benchmark definition that is not exactly the simple product. I regard the multiplicative relation as a useful approximation rather than an identified law.

Safety and cost

All tested conditions remained below the public safety limit of 0.65. Observed risk was largely associated with the solvent/loading setup and remained constant during electrolysis: approximately 0.072 for S0, 0.096 for S1, 0.114 for S2, and 0.126 for S3 at the standard loading. This suggests that, within the tested potential and time range, chemical inventory and solvent identity dominated the public risk metric more than electrolysis duration. That inference should not be extrapolated beyond the tested range.

Scope and unresolved alternatives

The conclusions apply to this fixed campaign world and primarily to 0.02 mol reagent in 0.04 L solvent, or a nominal initial concentration of 0.5 mol/L. Concentration, volume, electrode geometry, electrode gap, and temperature were not independently varied. The fixture was fixed within the world, so its resistance and area are confounded with every kinetic and transport estimate. No replicate batches were performed, preventing separation of assay noise from true run variation.

The identities are anonymous benchmark materials; no claim about real solvents or electrolytes is warranted. Hidden, fixed material residuals could explain some rankings that nominal properties cannot. The species-level mechanism, electron count, elementary reaction sequence, actual current, electrode surface state, local pH, and identities of side products were unobserved. Plausible alternatives include direct cathodic reduction of the limiting reagent, proton-coupled electron transfer with electrolyte-dependent onset, an adsorption-limited surface reaction, and a transport-limited process whose apparent selectivity changes as substrate is depleted. Precipitation might remove reagent, poison the electrode, increase local resistance, or merely correlate with another unfavorable electrolyte property; the campaign cannot distinguish these mechanisms.

Overall, the most economical explanation is a cathodic, charge-limited conversion with an intermediate-overpotential optimum. E2 suppresses precipitation and provides a favorable potential/conductivity environment; S0 supplies the best tested coupled transport and resistance behavior. Long electrolysis is needed for conversion, while excessive negative bias sacrifices selectivity and energy performance. Within the observed domain, batch 10—S0, E2, −0.6 V, 500 mA cap, and 14,400 s total electrolysis—best expresses that balance, but the exact optimum and the underlying elementary mechanism remain only partially identified.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific prior or proposed mechanism was supplied. The supplied material dossier contained nominal properties and explicitly warned that hidden, world-specific residuals and solvent coupling could alter their implications. The scoring weights, yield gate, safety limit, and instrument noise models were contracts rather than mechanistic claims.

My initial law that useful conversion would have an interior potential/time optimum was supported qualitatively, but not fully identified. In the S0/E2 refinement series, batch 10 at −0.6 V scored 0.584, compared with 0.572 at −0.8 V in batch 9, 0.570 at −0.4 V in batch 11, and 0.569 at −0.5 V in batch 12. This supports a moderate-bias operating region, but the differences were small, unreplicated, and comparable to plausible measurement/process variation; it does not establish a sharp optimum.

The proposed cathodic polarity law was strongly supported. The matched S1/E1 comparison changed my judgment most clearly: batch 3 at −1.5 V produced conversion 0.0738, yield 0.0262, and score 0.228, whereas batch 4 at +1.5 V produced zero reported conversion, yield 0.00079, and score 0.00297. Batches 1 and 2 had already suggested the same direction, but both lay near the yield gate and had saturated precipitation, so I initially treated that evidence cautiously.

The claim that insufficient charge or time limited early experiments was supported. The 1,200–7,200 s batches generally had low conversion, while batches 9–12, run for 14,400 s at a 500 mA cap, reached conversion of about 0.79–0.83. However, time, current cap, potential, and electrolyte were not varied independently, so a pure charge law remains unproven.

The expectation that nominal conductivity would help was supported in the matched E2 solvent comparison. Batch 7 using S0/E2 outperformed batches 8 and 5 using S1/E2 and S2/E2 under the same −1.2 V, 300 mA, 7,200 s protocol. Its score was 0.352 versus 0.328 and 0.318, and it also had higher ohmic and transport efficiencies. Conversely, my initial suggestion that lower-proton-activity S2 or S3 might win through selectivity was not supported: S2 did not exceed S0 in batch 5, and S3/E3 in batch 6 performed poorly. Because batch 6 changed both solvent and electrolyte, it cannot isolate the S3 effect.

The precipitation hypothesis was supported as an association. E0/S0 produced precipitation signal 1.0 in batches 1 and 2, E1/S1 produced about 0.71 in batches 3 and 4, while E2 conditions were essentially precipitation-free in batches 5, 7–12. E2-based batches were generally more useful. Nevertheless, batch 6 showed that low precipitation alone was insufficient, and the data could not distinguish electrode fouling, reagent removal, resistive effects, or a correlated electrolyte property.

The approximate law ‘selective yield ≈ conversion × selectivity’ was broadly supported in productive batches, including batches 10 and 11, but not exactly. Independent assay noise, recovery effects, or a different internal definition could explain the deviations.

Untested or unidentified claims include the elementary reaction sequence, electron stoichiometry, actual delivered current, current–potential curve, concentration dependence, electrode-area dependence, local rather than bulk pH, temperature effects, surface deactivation, and whether performance depends only on integrated charge. The fixed fixture claim supplied in the dossier could not be tested within this campaign. Repeatability was also untested because no exact replicate was run.

2. One discriminating experiment

I would repeat the batch-10 composition and potential—0.02 mol reagent in 0.04 L S0, E2, and −0.6 V—but use a 250 mA current cap for 28,800 s, divided into four 7,200 s electrolysis segments. This gives the same nominal current-time product as batch 10’s 500 mA for 14,400 s. I would take one UV–visible measurement after 14,400 s and perform the final assay after termination.

The leading charge-controlled explanation predicts approximately similar final conversion and selective yield to batch 10, with improved ohmic efficiency and possibly improved energy efficiency at the lower current density. That result would strengthen the view that integrated charge controls conversion while current density mainly controls resistive losses.

A substantially lower conversion at equal nominal charge would indicate that the current cap is not the delivered current, that −0.6 V is kinetically limiting at the lower cap, or that long exposure causes deactivation. Similar conversion but lower selectivity or yield would favor a time-dependent degradation or surface-aging alternative. Higher conversion or yield together with substantially improved efficiency would show that batch 10 was current-density limited and that the recommendation was not yet optimal. A markedly different halfway UV–visible profile would also support a current-density-dependent interface or transport process rather than a simple accumulated-charge law. Without direct current measurement, this experiment would not completely separate current regulation from kinetics, but it would be the most informative single comparison available.

3. Unused evidence, weak predictions, and goal effects

No pH-meter measurements were collected, so electrolyte acid properties were inferred only indirectly from final-assay pH-normalized values. Raw spectral shapes were not analyzed; only processed UV–visible estimates were used. The intermediate measurements were mostly descriptive because every batch continued through its planned second segment rather than using a predeclared stopping rule. Cost and safety data were checked against feasibility but were not modeled in detail because the objective score did not include cost and all observed risks remained well below 0.65. Nominal capacitance, diffusivity, acid dissociation, and solubility-product data were not isolated experimentally. The campaign also left substantial operation budget unused because the lifecycle limited the study to 12 completed batches.

The least reliable blind predictions are the positive-polarity cases Q02, Q04, Q06, Q08, Q10, and Q12. Their target yields were predicted near zero, where assay clipping and the score’s selective-yield gate make both selectivity and score highly nonlinear; batches 1 and 4 also gave inconsistent-looking selectivity values near the no-product limit. Q11 is also weak because 500 mA with E0 was never tested, so it extrapolates both current-cap behavior and severe precipitation. Q09 relies on an untested S2/E0 interaction. Predictions for E1 and E3 with S0 are uncertain because those electrolytes were observed only with different solvents. Even Q01 and Q03 inherit uncertainty from having only two E0/S0 campaign batches, both at ±1.0 V and with saturated precipitation.

The batch-10 recommendation is the best observed choice but not a high-confidence estimate of a unique optimum. Its score exceeded the neighboring batches by only about 0.012–0.014, and there were no replicates. The recommendation is more reliable as a broad region—S0/E2, moderate negative bias, long electrolysis—than as an exact claim that −0.6 V is superior to −0.5 or −0.4 V.

The assigned goal did affect evidence collection. Maximizing the balanced score favored broad material screening followed by local optimization, rather than exact replicates, orthogonal current/time experiments, pH measurements, or a full factorial design. Using one intermediate measurement in every batch consumed the complete intermediate-instrument allowance but provided limited adaptive value. There was no clear conflict with the scientific objective, because the campaign still identified polarity, precipitation, material, and potential effects, but the optimization emphasis reduced causal identifiability and uncertainty calibration.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.72,
        "lower80": 0.5,
        "upper80": 0.9
      },
      "energy_efficiency": {
        "estimate": 0.35,
        "lower80": 0.23,
        "upper80": 0.48
      },
      "faradaic_efficiency": {
        "estimate": 0.48,
        "lower80": 0.36,
        "upper80": 0.6
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.14,
        "lower80": 0.0,
        "upper80": 0.36
      },
      "selective_product_yield": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.025
      },
      "transport_efficiency": {
        "estimate": 0.5,
        "lower80": 0.36,
        "upper80": 0.64
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.88,
        "lower80": 0.45,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.37,
        "lower80": 0.23,
        "upper80": 0.51
      },
      "faradaic_efficiency": {
        "estimate": 0.38,
        "lower80": 0.25,
        "upper80": 0.52
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.03,
        "lower80": 0.0,
        "upper80": 0.28
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.016
      },
      "transport_efficiency": {
        "estimate": 0.34,
        "lower80": 0.2,
        "upper80": 0.49
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.72,
        "lower80": 0.57,
        "upper80": 0.86
      },
      "energy_efficiency": {
        "estimate": 0.34,
        "lower80": 0.22,
        "upper80": 0.47
      },
      "faradaic_efficiency": {
        "estimate": 0.47,
        "lower80": 0.34,
        "upper80": 0.6
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.38,
        "lower80": 0.29,
        "upper80": 0.47
      },
      "selective_product_yield": {
        "estimate": 0.09,
        "lower80": 0.035,
        "upper80": 0.17
      },
      "transport_efficiency": {
        "estimate": 0.49,
        "lower80": 0.34,
        "upper80": 0.63
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.88,
        "lower80": 0.45,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.35,
        "lower80": 0.21,
        "upper80": 0.49
      },
      "faradaic_efficiency": {
        "estimate": 0.36,
        "lower80": 0.22,
        "upper80": 0.5
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.05,
        "lower80": 0.0,
        "upper80": 0.31
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.018
      },
      "transport_efficiency": {
        "estimate": 0.32,
        "lower80": 0.18,
        "upper80": 0.47
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.69,
        "lower80": 0.5,
        "upper80": 0.84
      },
      "energy_efficiency": {
        "estimate": 0.31,
        "lower80": 0.18,
        "upper80": 0.44
      },
      "faradaic_efficiency": {
        "estimate": 0.43,
        "lower80": 0.28,
        "upper80": 0.57
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.36,
        "lower80": 0.23,
        "upper80": 0.45
      },
      "selective_product_yield": {
        "estimate": 0.095,
        "lower80": 0.03,
        "upper80": 0.19
      },
      "transport_efficiency": {
        "estimate": 0.43,
        "lower80": 0.27,
        "upper80": 0.58
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.65,
        "lower80": 0.15,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.12,
        "lower80": 0.0,
        "upper80": 0.32
      },
      "faradaic_efficiency": {
        "estimate": 0.18,
        "lower80": 0.05,
        "upper80": 0.35
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.2
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.017
      },
      "transport_efficiency": {
        "estimate": 0.15,
        "lower80": 0.0,
        "upper80": 0.35
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.38,
        "upper80": 0.77
      },
      "energy_efficiency": {
        "estimate": 0.23,
        "lower80": 0.1,
        "upper80": 0.37
      },
      "faradaic_efficiency": {
        "estimate": 0.29,
        "lower80": 0.15,
        "upper80": 0.44
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.28,
        "lower80": 0.16,
        "upper80": 0.39
      },
      "selective_product_yield": {
        "estimate": 0.055,
        "lower80": 0.01,
        "upper80": 0.14
      },
      "transport_efficiency": {
        "estimate": 0.29,
        "lower80": 0.14,
        "upper80": 0.45
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.5,
        "lower80": 0.05,
        "upper80": 0.95
      },
      "energy_efficiency": {
        "estimate": 0.05,
        "lower80": 0.0,
        "upper80": 0.18
      },
      "faradaic_efficiency": {
        "estimate": 0.08,
        "lower80": 0.0,
        "upper80": 0.22
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.14
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.017
      },
      "transport_efficiency": {
        "estimate": 0.07,
        "lower80": 0.0,
        "upper80": 0.22
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.75,
        "lower80": 0.57,
        "upper80": 0.89
      },
      "energy_efficiency": {
        "estimate": 0.29,
        "lower80": 0.17,
        "upper80": 0.42
      },
      "faradaic_efficiency": {
        "estimate": 0.44,
        "lower80": 0.29,
        "upper80": 0.57
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.36,
        "lower80": 0.24,
        "upper80": 0.47
      },
      "selective_product_yield": {
        "estimate": 0.1,
        "lower80": 0.03,
        "upper80": 0.21
      },
      "transport_efficiency": {
        "estimate": 0.38,
        "lower80": 0.23,
        "upper80": 0.53
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.8,
        "lower80": 0.3,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.24,
        "lower80": 0.09,
        "upper80": 0.4
      },
      "faradaic_efficiency": {
        "estimate": 0.27,
        "lower80": 0.1,
        "upper80": 0.44
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.027,
        "lower80": 0.0,
        "upper80": 0.24
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.018
      },
      "transport_efficiency": {
        "estimate": 0.24,
        "lower80": 0.07,
        "upper80": 0.42
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.68,
        "lower80": 0.53,
        "upper80": 0.81
      },
      "energy_efficiency": {
        "estimate": 0.29,
        "lower80": 0.17,
        "upper80": 0.42
      },
      "faradaic_efficiency": {
        "estimate": 0.39,
        "lower80": 0.25,
        "upper80": 0.52
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.46,
        "lower80": 0.36,
        "upper80": 0.58
      },
      "selective_product_yield": {
        "estimate": 0.38,
        "lower80": 0.2,
        "upper80": 0.58
      },
      "transport_efficiency": {
        "estimate": 0.41,
        "lower80": 0.27,
        "upper80": 0.55
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.82,
        "lower80": 0.35,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.28,
        "lower80": 0.11,
        "upper80": 0.45
      },
      "faradaic_efficiency": {
        "estimate": 0.3,
        "lower80": 0.12,
        "upper80": 0.47
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.045,
        "lower80": 0.0,
        "upper80": 0.28
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.02
      },
      "transport_efficiency": {
        "estimate": 0.28,
        "lower80": 0.09,
        "upper80": 0.46
      }
    }
  ],
  "rationale": "Predictions anchor to the campaign’s matched polarity results, E0/S0 assays, material-property dossier, and the approximately charge-limited behavior seen at long duration. Negative bias is treated as productive; positive-bias yields remain near the assay floor, making their scores highly uncertain because of the public low-yield gate. Long duration raises conversion and yield, while a 500 mA cap raises throughput but lowers expected electrical efficiency. Intervals are widened for untested solvent–electrolyte combinations, current-cap extrapolation, precipitation effects, hidden fixed material residuals, and the absence of replicates."
}
```
