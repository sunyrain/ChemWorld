# repeat-02/EC-W05-B12-discovery-E-MisIndexed

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-02\EC-W05-B12-discovery-E-MisIndexed\participant\discovery-E-MisIndexed

## 同期笔记

### v1 · 公开事件 0

# Electrochemical hypothesis notebook

## H1 [tentative]
At fixed loading, conversion should increase with passed charge until depletion, whereas selectivity/faradaic efficiency may peak at intermediate overpotential and decline at stronger forcing because competing pathways increase. Current is a cap, so delivered charge may be transport/ohmic limited rather than cap-proportional.

## H2 [tentative]
Material effects should separate into transport and interfacial terms: higher conductivity should favor ohmic efficiency, while thinner diffusion layers/higher diffusivity should favor transport efficiency. Nominal shifts in solvent and electrolyte standard potential may translate the response along the applied-potential axis.

## H3 [tentative]
Both potential signs must be tested: one sign may support target formation while the reverse sign yields little target or a distinct low-selectivity branch. Longer electrolysis should improve conversion only until degradation or selectivity loss dominates.

Plan: use constant reagent/solvent volume loading across 12 independent batches, spanning sign, magnitude, duration, current cap, solvents, and electrolytes. Use intermediate UV-vis snapshots to distinguish efficiency changes from final-assay noise. Replicate at least one central condition. Material dossiers are priors only; observations will control revisions.

### v2 · 公开事件 63

# Electrochemical hypothesis notebook

## H1 [supported qualitatively; quantitative law unresolved]
At 0.02 mol in 0.04 L, target output is charge-limited at low current but efficiency falls at high current. At +1 V/E3/3600 s, raising the cap from 20 to 50 to 100 mA increased final conversion/yield from 0.009/0 to 0.034/0.049 to 0.055/0.057 (events runner-operation-0056, -0063, -0042), while final faradaic/transport efficiency decreased from about 0.78/0.77 at 20–50 mA to 0.59/0.57 at 100 mA. The yield difference between 50 and 100 mA is small relative to single-run uncertainty and remains unresolved; conversion differs more clearly. A 500 mA cap at shorter exposure had poor efficiencies (runner-operation-0028, -0035), but duration is a confound.

## H2 [partly supported]
E3 suppresses precipitation relative to E0: E0 final assays showed precipitation near 0.99–1 (runner-operation-0007, -0028), while E3 at comparable loading showed near-zero precipitation (runner-operation-0035, -0042, -0049, -0056, -0063). This is directionally consistent with the nominal salt dossier. E3 does not automatically maximize efficiency; current and potential dominate. Electrolyte and solvent effects on target kinetics are not yet separated.

## H3 [supported for sign asymmetry; mechanism unresolved]
The response is strongly polarity-dependent. At ±1 V, 100 mA, 300 s in S0/E0, +1 V retained near-unity efficiency but only 0.016 conversion and zero measured yield (runner-operation-0007), whereas −1 V produced much lower energy/faradaic/transport efficiencies and essentially no conversion (runner-operation-0014). The small nonzero negative-polarity yield is compatible with assay noise because conversion was clipped at zero. Thus the productive branch is provisionally positive-potential.

## H4 [tentative response shape]
At E3/100 mA/3600 s, +1.0 and +1.4 V gave similar yield (~0.057–0.058) and conversion (~0.055–0.063), but +1.0 had higher energy efficiency and score (runner-operation-0042 vs -0049). This suggests a broad product plateau with energy penalty at excess potential, not evidence for a sharp kinetic optimum.

Next tests: isolate solvent changes at +1 V/50 mA/3600 s, then one electrolyte change. A repeatable solvent effect should shift efficiency and/or conversion beyond the scatter visible between UV-vis and final assay. Recommendation currently favors the 50 mA E3 condition (batch 9) for balanced efficiency, subject to material-screen results.

### v3 · 公开事件 84

# Electrochemical hypothesis notebook

## H1 [supported in tested positive-potential scope]
At 0.02 mol reagent in 0.04 L solvent, target formation is charge-limited at low current while transport/faradaic efficiency falls as forcing increases. For S0/E3, +1 V, 3600 s, caps of 20, 50, and 100 mA gave final conversion/yield 0.009/0, 0.034/0.049, and 0.055/0.057, respectively (runner-operation-0056, -0063, -0042); faradaic/transport efficiency was ~0.78/0.77, ~0.76/0.78, and ~0.59/0.57. Thus 50 mA provides the best tested compromise, while 100 mA increases conversion only modestly at a sizable efficiency cost. Single batches and assay uncertainty limit claims about small differences.

## H2 [supported for precipitation; material tradeoffs unresolved]
Electrolyte strongly controls precipitation. E3 produced near-zero precipitation in all tested S0 positive-potential runs (runner-operation-0035, -0042, -0049, -0056, -0063), consistent with its low nominal precipitating-salt level. At the matched S0/+1 V/50 mA/3600 s condition, E1 raised faradaic/transport efficiency from ~0.76/0.78 (E3, runner-operation-0063) to ~0.83/0.86 (runner-operation-0084) and preserved yield (~0.048), but precipitation rose from 0.008 to 0.849. This is a genuine operating tradeoff, not an overall electrolyte ranking.

## H3 [supported for sign asymmetry]
The productive branch is positive-potential. At ±1 V, 100 mA, 300 s in S0/E0, +1 V retained near-unity efficiencies with 0.016 conversion (runner-operation-0007); −1 V gave much lower energy/faradaic/transport efficiencies and conversion clipped at zero (runner-operation-0014). Its small reported yield is compatible with assay noise. No evidence supports a productive negative-potential branch in this tested regime.

## H4 [supported broad plateau, not sharp optimum]
For S0/E3 at 100 mA/3600 s, +1.0 and +1.4 V gave similar yield (~0.057–0.058) and conversion (~0.055–0.063), but +1.0 V had higher energy efficiency and score (runner-operation-0042 vs -0049). Strong +2 V/500 mA/1200 s collapsed efficiencies and target output (runner-operation-0021). A parsimonious response is activation followed by an efficiency plateau/decline under excess overpotential or current, with duration controlling accumulated conversion.

## H5 [supported solvent ordering at one operating point]
At E3/+1 V/50 mA/3600 s, S0 outperformed S1 and S2 in final selectivity and yield: 0.865/0.049 versus 0.777/0.020 and 0.663/0.021 (runner-operation-0063, -0070, -0077). S0 also had the highest faradaic/transport efficiencies among these three. Because there are no replicates, exact magnitudes remain uncertain, but the yield gap is much larger than the stated assay noise and is consistent across both alternative solvents.

## Predictive working model
Use potential polarity as a branch selector; within the positive branch, treat conversion as increasing with effective delivered charge until saturation/degradation, and treat faradaic/transport efficiency as decreasing when current demand exceeds transport. Material shifts alter both potential alignment and transport; precipitation is a separate electrolyte-dependent sink/operability constraint. This qualitative model predicts that longer time at moderate cap can outperform short high-cap operation, and that E1 can look electrically efficient yet be operationally inferior when precipitation matters.

## Decision
Recommend batch 9 (S0/E3, +1 V, 50 mA cap, 3600 s) as the balanced operating point: near-best score, near-zero precipitation, good efficiency, and essentially the same selective yield as higher-scoring but strongly precipitating E1. I would change this decision if replicated E1 operation showed manageable precipitation or substantially higher target yield, or if a finer 50–100 mA/time grid demonstrated a reproducible yield advantage without efficiency loss.

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
      "current_mA": 500,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 2
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
    "cost": 0.2874000072479248,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.0,
    "ohmic_efficiency": 0.90985107421875,
    "pH_normalized": 0.231104776263237,
    "precipitation_signal": 0.9869203567504883,
    "safety_risk": 0.072194404900074,
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
      "potential_V": 0.5
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
    "cost": 0.28380000591278076,
    "electrochemical_conversion": 0.026964066550135612,
    "electrochemical_selectivity": 0.8839040994644165,
    "energy_efficiency": 0.37826335430145264,
    "faradaic_efficiency": 0.22602954506874084,
    "ohmic_efficiency": 0.6921476721763611,
    "pH_normalized": 0.23041419684886932,
    "precipitation_signal": 0.9876685738563538,
    "safety_risk": 0.072194404900074,
    "score": 0.30262595415115356,
    "selective_product_yield": 0.028849579393863678,
    "transport_efficiency": 0.19454200565814972
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
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": 0.5
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
    "cost": 0.28380000591278076,
    "electrochemical_conversion": 0.021441498771309853,
    "electrochemical_selectivity": 0.8117727041244507,
    "energy_efficiency": 0.2921908497810364,
    "faradaic_efficiency": 0.1267581284046173,
    "ohmic_efficiency": 0.6989051699638367,
    "pH_normalized": 0.2749584913253784,
    "precipitation_signal": 0.0,
    "safety_risk": 0.072194404900074,
    "score": 0.257373571395874,
    "selective_product_yield": 0.022955406457185745,
    "transport_efficiency": 0.11624865978956223
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
      "current_mA": 100,
      "electrolyte_profile": 3,
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
    "cost": 0.28404000401496887,
    "electrochemical_conversion": 0.055163197219371796,
    "electrochemical_selectivity": 0.8815313577651978,
    "energy_efficiency": 0.8457491397857666,
    "faradaic_efficiency": 0.5923762321472168,
    "ohmic_efficiency": 0.9700047969818115,
    "pH_normalized": 0.2716825306415558,
    "precipitation_signal": 0.0023995577357709408,
    "safety_risk": 0.072194404900074,
    "score": 0.48711642622947693,
    "selective_product_yield": 0.05684402957558632,
    "transport_efficiency": 0.5676928758621216
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
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": 1.4
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
    "cost": 0.28461599349975586,
    "electrochemical_conversion": 0.06336523592472076,
    "electrochemical_selectivity": 0.9577391743659973,
    "energy_efficiency": 0.6691595315933228,
    "faradaic_efficiency": 0.5704777240753174,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.27069711685180664,
    "precipitation_signal": 0.0,
    "safety_risk": 0.072194404900074,
    "score": 0.473670095205307,
    "selective_product_yield": 0.058178797364234924,
    "transport_efficiency": 0.5738780498504639
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
      "current_mA": 20,
      "electrolyte_profile": 3,
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
    "cost": 0.2828879952430725,
    "electrochemical_conversion": 0.00933709554374218,
    "electrochemical_selectivity": 0.8670863509178162,
    "energy_efficiency": 0.8627864718437195,
    "faradaic_efficiency": 0.7771334648132324,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.2689996659755707,
    "precipitation_signal": 0.00031451715040020645,
    "safety_risk": 0.072194404900074,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.770638108253479
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
      "current_mA": 50,
      "electrolyte_profile": 3,
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
    "cost": 0.28332000970840454,
    "electrochemical_conversion": 0.03411300107836723,
    "electrochemical_selectivity": 0.8651828765869141,
    "energy_efficiency": 0.8927309513092041,
    "faradaic_efficiency": 0.7635406255722046,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.27101343870162964,
    "precipitation_signal": 0.008188718929886818,
    "safety_risk": 0.072194404900074,
    "score": 0.5317749381065369,
    "selective_product_yield": 0.048715002834796906,
    "transport_efficiency": 0.7843719124794006
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
      "current_mA": 50,
      "electrolyte_profile": 3,
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
    "cost": 0.2993200123310089,
    "electrochemical_conversion": 0.04532070830464363,
    "electrochemical_selectivity": 0.7768545746803284,
    "energy_efficiency": 0.759039580821991,
    "faradaic_efficiency": 0.6512070298194885,
    "ohmic_efficiency": 0.9714524745941162,
    "pH_normalized": 0.2704644799232483,
    "precipitation_signal": 0.0,
    "safety_risk": 0.09559440612792969,
    "score": 0.4621107280254364,
    "selective_product_yield": 0.020259473472833633,
    "transport_efficiency": 0.6525565981864929
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
      "solvent": 2,
      "volume_L": 0.04
    },
    {
      "current_mA": 50,
      "electrolyte_profile": 3,
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
    "cost": 0.32491999864578247,
    "electrochemical_conversion": 0.041594501584768295,
    "electrochemical_selectivity": 0.663191556930542,
    "energy_efficiency": 0.6715199947357178,
    "faradaic_efficiency": 0.6056091785430908,
    "ohmic_efficiency": 0.9829414486885071,
    "pH_normalized": 0.28797647356987,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.1135944053530693,
    "score": 0.42310404777526855,
    "selective_product_yield": 0.020501799881458282,
    "transport_efficiency": 0.6127890944480896
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
      "solvent": 0,
      "volume_L": 0.04
    },
    {
      "current_mA": 50,
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
    "cost": 0.28332000970840454,
    "electrochemical_conversion": 0.02407446689903736,
    "electrochemical_selectivity": 0.9023391604423523,
    "energy_efficiency": 0.8907610774040222,
    "faradaic_efficiency": 0.8338807821273804,
    "ohmic_efficiency": 0.9938645362854004,
    "pH_normalized": 0.20225173234939575,
    "precipitation_signal": 0.8490318655967712,
    "safety_risk": 0.072194404900074,
    "score": 0.5509436726570129,
    "selective_product_yield": 0.04828575626015663,
    "transport_efficiency": 0.8551057577133179
  }
}
```

## K1 封存报告

Mechanistic account

1. Empirical scope

All 12 batches used 0.020 mol of limiting reagent in 0.040 L of solvent, so the nominal starting concentration was 0.50 mol L⁻¹. Consequently, the campaign identifies behavior only at this loading and volume. Applied potential ranged from −1.0 to +2.0 V, current caps from 20 to 500 mA, and electrolysis times from 300 to 3600 s. Solvents S0–S2 and electrolytes E0, E1, and E3 were tested; S3 and E2 were not tested. There were no exact independent replicates, so small numerical differences should not be treated as precisely resolved effects.

2. Proposed process structure

I think the world contains at least four coupled processes:

(a) A polarity- and overpotential-dependent electron-transfer branch. Define an effective overpotential schematically as

η = V_applied − [E* + ΔE_solvent + ΔE_electrolyte + ΔE_interface],

where E* and the interface term are unknown. Positive applied potential accesses the target-forming branch in the tested conditions; negative potential does not. The nominal solvent and electrolyte standard-potential shifts are useful priors, but an unknown, campaign-fixed interfacial residual prevents calculation of absolute η.

(b) Charge accumulation. A useful qualitative conversion law is

X_true ≈ X_max[1 − exp(−k(η, materials) Q_product/n₀)],
Q_product = ∫ I_delivered(t)·FE(t) dt.

The programmed current is a cap, not necessarily the delivered current. Thus current cap × time is only a forcing proxy. At low current, product formation is charge-limited. At high demand, transport and side reactions reduce the fraction of charge reaching target product.

(c) Coupled ohmic, transport, and faradaic losses. I would represent delivered current and efficiency schematically as

I_delivered = min[I_cap, I_kinetic(η), I_transport],
I_transport ∝ D_eff C/δ_eff,
FE = f(η, I_delivered/I_transport, solvent, electrolyte),
Energy efficiency ≈ FE × ohmic factor × voltage-utilization factor.

This is not claimed as an identified equation; it summarizes the observed couplings. Conductivity principally affects ohmic loss, while diffusivity and diffusion-layer thickness influence the transport ceiling. Once current demand approaches that ceiling, concentration polarization or related interfacial depletion lowers transport and faradaic efficiency. Excess overpotential can additionally open competing reactions or degradation.

(d) Electrolyte-dependent precipitation. A separate sink or operability process depends on salt concentration, solubility product, solvent, pH, and electrolysis-generated species. In schematic form,

P_precip ≈ sigmoid[log₁₀(Q_ionic/Ksp_eff)].

Precipitation need not be identical to loss of target product, but it can alter accessible species, transport, and assay response. The data show that electrical efficiency and precipitation can trade off rather than move together.

3. Evidence that shaped the account

Polarity: Batch 1 (S0/E0, +1.0 V, 100 mA, 300 s) showed very high final faradaic, transport, and ohmic efficiencies—1.000, 0.986, and 0.960—but only 0.0157 conversion and zero reported selective-product yield. Batch 2 changed only the potential sign to −1.0 V. Its conversion was clipped at zero and its faradaic, transport, and energy efficiencies fell to 0.407, 0.433, and 0.285. The reported yield of 0.0110 despite zero conversion is too small and internally inconsistent to establish productive negative-potential chemistry; assay noise or independent metric processing is a plausible explanation. These two batches established a positive-potential productive branch and rejected a sign-symmetric response.

Excess forcing: Batch 3 (S0/E0, +2.0 V, 500 mA, 1200 s) collapsed to zero reported conversion, selectivity, yield, faradaic efficiency, transport efficiency, and energy efficiency, although ohmic efficiency remained 0.910. Batch 4 used +0.5 V at the same 500 mA and 1200 s and recovered 0.0270 conversion, 0.0288 yield, 0.884 selectivity, 0.226 faradaic efficiency, and 0.195 transport efficiency. This changed the initial simple ‘more positive potential gives more reaction’ idea into a peaked or plateauing response: strong forcing can favor nonproductive reactions or create severe transport limitation. Because potential and actual delivered current interact, Batch 3 alone cannot distinguish direct high-potential degradation from current-driven depletion.

Precipitation and electrolyte: E0 produced precipitation signals near unity in Batches 1–4 (1.000, 1.000, 0.987, and 0.988). Batch 5 changed Batch 4’s electrolyte from E0 to E3 while retaining S0, +0.5 V, 500 mA, and 1200 s. Precipitation fell from 0.988 to zero. Its yield changed only from 0.0288 to 0.0230, while faradaic and transport efficiencies changed from 0.226/0.195 to 0.127/0.116. Thus suppressing precipitation did not automatically improve electrical performance. The precipitation contrast is consistent with the dossier: E0 has 0.012 mol L⁻¹ nominal precipitating salt and log₁₀Ksp = −8.523, whereas E3 has only 0.0002 mol L⁻¹ and log₁₀Ksp = −4.699.

Time and moderate current: Batch 6 (S0/E3, +1.0 V, 100 mA, 3600 s) produced 0.0552 conversion and 0.0568 yield, with 0.882 selectivity, 0.592 faradaic efficiency, 0.568 transport efficiency, 0.970 ohmic efficiency, and precipitation 0.0024. Relative to the short positive-potential run, this established that accumulated electrolysis time/charge is important. It also showed that useful target formation is possible without precipitation.

Potential plateau: Batch 7 differed from Batch 6 only by using +1.4 rather than +1.0 V. Conversion rose modestly from 0.0552 to 0.0634 and selectivity from 0.882 to 0.958, but yield was essentially unchanged within single-assay uncertainty (0.0568 versus 0.0582). Energy efficiency declined from 0.846 to 0.669, and the score declined from 0.487 to 0.474. I therefore infer a broad product plateau between approximately +1.0 and +1.4 V under these conditions, with an energy penalty at the higher potential. The experiment does not locate a sharp optimum.

Current/charge tradeoff: Batches 8, 9, and 6 used S0/E3, +1.0 V, and 3600 s with current caps of 20, 50, and 100 mA. Their final conversion values were 0.0093, 0.0341, and 0.0552, showing increasing accumulated reaction with cap. Their faradaic efficiencies were 0.777, 0.764, and 0.592, and transport efficiencies were 0.771, 0.784, and 0.568. Thus the 20–50 mA regime was electrically efficient but charge-limited; at 100 mA conversion increased while faradaic and transport efficiency deteriorated. Selective yields were 0, 0.0487, and 0.0568. The small yield increment from 50 to 100 mA is not secure without replication, but the efficiency loss is large. This current series most strongly supports a transport-limited charge model.

Solvent coupling: Batches 9–11 held E3, +1.0 V, 50 mA, and 3600 s constant while changing S0, S1, and S2. Final conversion was 0.0341, 0.0453, and 0.0416, respectively, so conversion alone did not favor S0. However, selectivity was 0.865, 0.777, and 0.663, producing yields of 0.0487, 0.0203, and 0.0205. Faradaic/transport efficiencies also declined from 0.764/0.784 for S0 to 0.651/0.653 for S1 and 0.606/0.613 for S2. Hence the solvent changes product partitioning or interfacial selectivity, not merely bulk conversion. The superior S0 result is not predicted by diffusivity alone: S1 has the largest nominal relative diffusivity. Conductivity, double-layer capacitance, proton activity, potential shift, solvation, and hidden residuals are therefore coupled.

Electrical efficiency versus precipitation: Batch 12 changed Batch 9’s electrolyte from E3 to E1 while retaining S0, +1.0 V, 50 mA, and 3600 s. E1 increased faradaic and transport efficiency from 0.764/0.784 to 0.834/0.855 and produced the highest public score, 0.551 versus 0.532. Its yield was essentially unchanged (0.0483 versus 0.0487), but precipitation increased from 0.0082 to 0.849 and normalized pH fell from 0.271 to 0.202. This is decisive evidence for two partially independent axes: E1 is electrically favorable at this operating point, probably through transport or potential alignment, while E3 is much more resistant to precipitation. That tradeoff explains why Batch 9 was the sealed balanced recommendation despite Batch 12’s slightly higher score.

4. Interpretation of the measured metrics

Selective-product yield is not numerically equal to measured conversion multiplied by selectivity in several batches. For example, Batch 9 reports conversion 0.0341, selectivity 0.865, and yield 0.0487. Batch 2 reports zero conversion but nonzero yield. I therefore do not impose the identity Y = X·S on the processed outputs. Possible explanations include independent calibrated channels, clipping near zero, different normalizations, and assay noise. The metrics should be treated as correlated observations of a latent state, not exact mass-balance identities.

Intermediate UV–visible and final-assay efficiency estimates were generally directionally consistent but not identical. For Batch 9, UV–visible versus final values were 0.777 versus 0.764 for faradaic efficiency and 0.780 versus 0.784 for transport efficiency. Larger discrepancies occurred in some material tests: Batch 10 energy efficiency was 0.819 by UV–visible and 0.759 by final assay; Batch 12 faradaic efficiency was 0.910 versus 0.834. Since both instruments are defined as instantaneous snapshots and measurement does not advance chemistry, these differences should be attributed to separate calibration/noise/process proxies rather than post-measurement reaction.

The normalized pH data primarily followed electrolyte/solvent selection: approximately 0.23 for E0, 0.269–0.275 for S0/E3, 0.288 for S2/E3, and 0.202 for S0/E1. The campaign does not identify whether proton activity directly controls target kinetics or merely covaries with formulation. Safety risk was approximately 0.072 for the standard recipes and did not provide a discriminating response within the tested set.

5. Predictive implications

Within S0/E3 at 0.50 mol L⁻¹ and around +1.0 V, increasing electrolysis time or current from a charge-starved condition should initially raise conversion. Increasing current substantially beyond the moderate regime should yield diminishing target gains because faradaic and transport efficiencies decline. Extending time at a moderate cap is therefore conjectured to be preferable to reaching the same nominal charge through a very high cap, although the campaign did not perform an equal-charge comparison.

Potentials modestly above +1.0 V may increase conversion or selectivity slightly but should reduce energy efficiency; much stronger positive forcing combined with high current may collapse target formation. Negative potential is predicted to remain nonproductive near the tested regime.

At the Batch 9 condition, replacing E3 with E1 should preserve target yield and improve electrical efficiencies but produce substantial precipitation and lower normalized pH. Replacing S0 with S1 or S2 should reduce target selectivity and yield even if gross conversion remains similar or rises slightly. These are interpolations within the observed condition, not claims about all potentials or concentrations.

6. Unidentifiable factors and alternatives

The campaign cannot separately identify intrinsic kinetic rate constants, electrode area, electrode gap, actual current trajectories, electron stoichiometry, mass-transfer coefficients, or the hidden material/interface residuals. Electrode fixture properties were fixed across the world, so their absolute effects are inseparable from kinetic constants. No time course within a single batch was measured, preventing discrimination among first-order saturation, reagent depletion, electrode passivation, and time-dependent degradation.

The failure at +2.0 V could reflect direct product degradation, solvent/electrolyte oxidation, depletion at the electrode, passivation, or another competitive current sink. The design confounded very high potential with a 500 mA cap, so these alternatives remain unresolved. Likewise, E0’s poor precipitation behavior could reduce dissolved active species, foul the interface, or merely create an assay-visible solid without causing the electrical changes; Batch 5 shows that precipitation suppression alone does not guarantee better efficiency.

Solvent effects could arise from conductivity, diffusivity, proton activity, double-layer capacitance, potential shifts, target solvation, or fixed latent formulation residuals. With only one matched batch per solvent and no S3 test, a unique solvent mechanism is not identifiable. E2 and S3 behavior should not be inferred from their nominal dossier alone.

Finally, the absence of exact replicates limits estimates of process variability. Differences much larger than the stated final-assay noise—such as the S0 versus S1/S2 yield gap or E1 versus E3 precipitation gap—are persuasive. Differences of only a few thousandths, such as the yields of Batches 6 and 7 or Batches 9 and 12, are numerical observations but not strong evidence of distinct true means.

Overall, the simplest account consistent with the campaign is a positive-potential target pathway whose accumulated conversion depends on effective faradaic charge, coupled to a transport ceiling that penalizes high current and excess potential. Solvent and electrolyte shift interfacial selectivity and transport, while electrolyte chemistry independently governs precipitation. The best balanced observed regime used moderate positive potential and current for a long duration, with S0 supporting target selectivity and E3 preventing precipitation.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific mechanism or response law was supplied. The only supplied scientific prior was the nominal material dossier; it explicitly warned that hidden, fixed residuals and solvent–electrolyte coupling could modify those properties.

Supported claims:
- The self-developed polarity hypothesis was supported. Batch 1 (+1.0 V) retained near-unity faradaic and transport efficiencies, whereas Batch 2 (−1.0 V) gave much lower efficiencies and conversion clipped at zero under otherwise matched conditions. This changed my judgment from treating both signs as plausible to favoring a positive-potential target branch.
- The proposed charge/transport tradeoff was supported by Batches 8, 9, and 6 at 20, 50, and 100 mA. Conversion increased from 0.009 to 0.034 to 0.055, while faradaic and transport efficiencies deteriorated at 100 mA. Batch 9 therefore looked like a better efficiency–output compromise than simply maximizing current.
- The expectation that excessive forcing can become nonproductive was supported by Batch 3: +2.0 V and 500 mA collapsed conversion, selectivity, yield, and most efficiencies. Batch 4, at +0.5 V with the same current cap, recovered measurable product.
- A broad potential plateau was supported by Batches 6 and 7. Raising potential from +1.0 to +1.4 V changed yield only from 0.0568 to 0.0582 while lowering energy efficiency from 0.846 to 0.669.
- The dossier-based precipitation prior was strongly supported. E0 gave precipitation near unity in Batches 1–4, while changing E0 to E3 in the matched Batches 4 and 5 reduced precipitation from 0.988 to zero. E3 also remained near zero in Batches 6–11.
- Solvent-dependent selectivity was supported by matched Batches 9–11. S0, S1, and S2 gave selectivities of 0.865, 0.777, and 0.663 and yields of 0.0487, 0.0203, and 0.0205.

Contradicted or narrowed claims:
- A simple “more potential/current gives more product” law was contradicted by Batch 3 and narrowed by Batches 6–9. Forcing must be represented jointly with transport and faradaic losses.
- A simple “less precipitation means better electrochemical performance” claim was contradicted by Batches 4 and 5: E3 removed precipitation but did not improve yield or efficiency at +0.5 V/500 mA. Batch 12 likewise showed that E1 could be electrically efficient while strongly precipitating.
- Nominal diffusivity alone did not rank solvents. S1 had higher nominal relative diffusivity than S0, yet Batch 10 had lower transport efficiency and much lower yield than Batch 9. Conductivity, interfacial selectivity, proton activity, potential shifts, and hidden residuals must remain coupled alternatives.
- Exact identities such as selective yield = conversion × selectivity were contradicted at the processed-measurement level. Batch 9, for example, reported 0.034 conversion, 0.865 selectivity, and 0.0487 yield. The channels therefore cannot be treated as exact noiseless mass-balance quantities.

Untested or unresolved claims:
- The suggested exponential conversion law and two-electron effective-charge interpretation were only approximate organizing models, not identified laws.
- Time-dependent degradation, passivation, and true saturation were not isolated because no equal-charge comparison or within-batch time course was performed.
- Translation of the potential-response curve by the nominal material potential shifts was not tested with matched potential sweeps across electrolytes.
- The separate causal effects of conductivity, diffusion coefficient, diffusion-layer thickness, capacitance, and proton activity remain unidentifiable.
- S3 and E2 were never tested, and concentration dependence was untested because every batch used the same loading.

The most consequential judgment changes came from Batch 2 establishing polarity asymmetry, Batch 3 rejecting monotonic forcing, Batch 5 separating precipitation from performance, Batches 8–9 revealing the current-efficiency compromise, and Batch 12 revealing the electrical-efficiency/precipitation tradeoff.

2. One additional discriminating experiment

I would run S0/E3 at the established loading and +1.0 V, using a 25 mA cap for 7200 s. Its nominal charge, 180 C, matches Batch 9 at 50 mA for 3600 s.

The leading explanation is that product formation mainly follows effective faradaic charge, while higher instantaneous current causes transport polarization. It predicts that the new batch should have similar or greater yield than Batch 9, with transport and faradaic efficiencies at least as high, because the same nominal charge is delivered more gently.

A plausible alternative is that elapsed time causes passivation, product degradation, or another slow loss independent of nominal charge. It predicts that doubling the exposure time could lower yield or efficiency despite the lower current.

Interpretation would be pre-specified as follows:
- Similar yield with higher efficiencies would strengthen the effective-charge plus current-dependent transport account.
- Lower yield together with lower efficiencies would strengthen slow passivation or degradation.
- Much lower conversion but preserved efficiencies would imply that the current cap is not the delivered current and that low-current kinetics, rather than charge bookkeeping, dominate.
- Higher yield but unexpectedly lower selectivity would suggest that long exposure opens a separate secondary pathway.

One batch would still not establish repeatability, but this comparison would remove the largest current–time confounding present in the campaign.

3. Unused evidence, reliability, and goal effects

The raw UV–visible spectra and final-assay artifacts were not inspected; the analysis used processed estimates. Spectral band shapes, baselines, and mass-balance details were therefore unused. Intermediate UV–visible measurements were used mainly as consistency checks rather than quantitatively modeled. No intermediate pH measurements were taken, so the final pH differences could not be connected to a time course. Cost and safety changed little across the fixed recipes and provided little discrimination. S3, E2, concentration variation, exact replicates, equal-charge comparisons, and repeated time points were also absent.

The least reliable blind predictions are Q11 and Q12 because 500 mA for 7200 s jointly extrapolates beyond both the campaign’s longest high-current exposure and its longest duration. Q03, Q05, Q07, and Q09 are also weak because the only observed negative-potential batch was Batch 2 at 300 s. Q05–Q10 additionally require material interactions not observed in the exact requested combinations. Q01 and Q02 are comparatively more reliable because they remain near the matched short E0 polarity pair, although even they change potential, duration, volume, and loading.

The operating recommendation is also not a claim that Batch 9 has the highest true mean score. Batch 12 had a slightly higher observed score, and neither condition was replicated. The recommendation is more reliable as a precipitation-aware choice because the precipitation contrast—0.008 in Batch 9 versus 0.849 in Batch 12—was much larger than the score difference.

The assigned explanatory goal materially affected evidence collection. I spent batches on reverse polarity, extreme forcing, current variation, and material contrasts rather than concentrating all 12 batches around the apparent optimum. That breadth enabled the mechanism distinctions above but reduced replication and local optimization precision. I also used every intermediate allocation for UV–visible efficiency information instead of reserving some for pH trajectories. There was no unavoidable conflict with the goal, but the choice favored explanatory coverage over narrow score maximization.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.65,
        "lower80": 0.45,
        "upper80": 0.8
      },
      "energy_efficiency": {
        "estimate": 0.32,
        "lower80": 0.17,
        "upper80": 0.47
      },
      "faradaic_efficiency": {
        "estimate": 0.42,
        "lower80": 0.25,
        "upper80": 0.58
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.11,
        "lower80": 0.0,
        "upper80": 0.3
      },
      "selective_product_yield": {
        "estimate": 0.007,
        "lower80": 0.0,
        "upper80": 0.025
      },
      "transport_efficiency": {
        "estimate": 0.45,
        "lower80": 0.28,
        "upper80": 0.6
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.98,
        "lower80": 0.85,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.94,
        "lower80": 0.82,
        "upper80": 1.0
      },
      "faradaic_efficiency": {
        "estimate": 0.95,
        "lower80": 0.82,
        "upper80": 1.0
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.58,
        "lower80": 0.38,
        "upper80": 0.72
      },
      "selective_product_yield": {
        "estimate": 0.024,
        "lower80": 0.008,
        "upper80": 0.05
      },
      "transport_efficiency": {
        "estimate": 0.94,
        "lower80": 0.82,
        "upper80": 1.0
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.42,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.28,
        "lower80": 0.12,
        "upper80": 0.45
      },
      "faradaic_efficiency": {
        "estimate": 0.4,
        "lower80": 0.22,
        "upper80": 0.58
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.34,
        "lower80": 0.18,
        "upper80": 0.5
      },
      "selective_product_yield": {
        "estimate": 0.077,
        "lower80": 0.03,
        "upper80": 0.15
      },
      "transport_efficiency": {
        "estimate": 0.42,
        "lower80": 0.24,
        "upper80": 0.6
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.92,
        "lower80": 0.78,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.88,
        "lower80": 0.72,
        "upper80": 0.98
      },
      "faradaic_efficiency": {
        "estimate": 0.75,
        "lower80": 0.55,
        "upper80": 0.9
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.6,
        "lower80": 0.43,
        "upper80": 0.74
      },
      "selective_product_yield": {
        "estimate": 0.215,
        "lower80": 0.09,
        "upper80": 0.35
      },
      "transport_efficiency": {
        "estimate": 0.72,
        "lower80": 0.52,
        "upper80": 0.88
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.65,
        "lower80": 0.45,
        "upper80": 0.8
      },
      "energy_efficiency": {
        "estimate": 0.38,
        "lower80": 0.18,
        "upper80": 0.58
      },
      "faradaic_efficiency": {
        "estimate": 0.5,
        "lower80": 0.3,
        "upper80": 0.7
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.39,
        "lower80": 0.22,
        "upper80": 0.55
      },
      "selective_product_yield": {
        "estimate": 0.101,
        "lower80": 0.04,
        "upper80": 0.2
      },
      "transport_efficiency": {
        "estimate": 0.55,
        "lower80": 0.35,
        "upper80": 0.75
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.9,
        "lower80": 0.75,
        "upper80": 0.99
      },
      "energy_efficiency": {
        "estimate": 0.84,
        "lower80": 0.68,
        "upper80": 0.97
      },
      "faradaic_efficiency": {
        "estimate": 0.7,
        "lower80": 0.52,
        "upper80": 0.86
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.58,
        "lower80": 0.4,
        "upper80": 0.72
      },
      "selective_product_yield": {
        "estimate": 0.196,
        "lower80": 0.08,
        "upper80": 0.35
      },
      "transport_efficiency": {
        "estimate": 0.72,
        "lower80": 0.54,
        "upper80": 0.88
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.35,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.3,
        "lower80": 0.12,
        "upper80": 0.48
      },
      "faradaic_efficiency": {
        "estimate": 0.35,
        "lower80": 0.18,
        "upper80": 0.52
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.32,
        "lower80": 0.15,
        "upper80": 0.48
      },
      "selective_product_yield": {
        "estimate": 0.06,
        "lower80": 0.02,
        "upper80": 0.14
      },
      "transport_efficiency": {
        "estimate": 0.4,
        "lower80": 0.22,
        "upper80": 0.58
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.86,
        "lower80": 0.7,
        "upper80": 0.97
      },
      "energy_efficiency": {
        "estimate": 0.86,
        "lower80": 0.7,
        "upper80": 0.98
      },
      "faradaic_efficiency": {
        "estimate": 0.64,
        "lower80": 0.45,
        "upper80": 0.81
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.55,
        "lower80": 0.37,
        "upper80": 0.7
      },
      "selective_product_yield": {
        "estimate": 0.171,
        "lower80": 0.07,
        "upper80": 0.32
      },
      "transport_efficiency": {
        "estimate": 0.61,
        "lower80": 0.42,
        "upper80": 0.78
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.45,
        "lower80": 0.25,
        "upper80": 0.65
      },
      "energy_efficiency": {
        "estimate": 0.22,
        "lower80": 0.08,
        "upper80": 0.4
      },
      "faradaic_efficiency": {
        "estimate": 0.3,
        "lower80": 0.14,
        "upper80": 0.48
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.26,
        "lower80": 0.1,
        "upper80": 0.43
      },
      "selective_product_yield": {
        "estimate": 0.042,
        "lower80": 0.01,
        "upper80": 0.11
      },
      "transport_efficiency": {
        "estimate": 0.33,
        "lower80": 0.17,
        "upper80": 0.5
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.7,
        "lower80": 0.5,
        "upper80": 0.86
      },
      "energy_efficiency": {
        "estimate": 0.72,
        "lower80": 0.54,
        "upper80": 0.88
      },
      "faradaic_efficiency": {
        "estimate": 0.6,
        "lower80": 0.42,
        "upper80": 0.76
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.48,
        "lower80": 0.31,
        "upper80": 0.64
      },
      "selective_product_yield": {
        "estimate": 0.131,
        "lower80": 0.05,
        "upper80": 0.26
      },
      "transport_efficiency": {
        "estimate": 0.58,
        "lower80": 0.4,
        "upper80": 0.74
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.45,
        "lower80": 0.2,
        "upper80": 0.68
      },
      "energy_efficiency": {
        "estimate": 0.12,
        "lower80": 0.02,
        "upper80": 0.3
      },
      "faradaic_efficiency": {
        "estimate": 0.15,
        "lower80": 0.05,
        "upper80": 0.32
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.25,
        "lower80": 0.08,
        "upper80": 0.48
      },
      "selective_product_yield": {
        "estimate": 0.105,
        "lower80": 0.02,
        "upper80": 0.3
      },
      "transport_efficiency": {
        "estimate": 0.18,
        "lower80": 0.05,
        "upper80": 0.38
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.88,
        "lower80": 0.65,
        "upper80": 0.99
      },
      "energy_efficiency": {
        "estimate": 0.5,
        "lower80": 0.3,
        "upper80": 0.7
      },
      "faradaic_efficiency": {
        "estimate": 0.35,
        "lower80": 0.18,
        "upper80": 0.55
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.55,
        "lower80": 0.35,
        "upper80": 0.72
      },
      "selective_product_yield": {
        "estimate": 0.42,
        "lower80": 0.18,
        "upper80": 0.75
      },
      "transport_efficiency": {
        "estimate": 0.3,
        "lower80": 0.14,
        "upper80": 0.5
      }
    }
  ],
  "rationale": "Predictions interpolate the observed polarity asymmetry, material effects, and current-dependent transport/faradaic losses. Yield was scaled approximately with passed charge, faradaic efficiency, and selectivity, with saturation/degradation uncertainty. Intervals are wider for 7200 s and 500 mA because both extrapolate beyond the campaign; the short E0 runs are closest to observed batches. Scores incorporate the published weighted components and the strong low-yield gate."
}
```
