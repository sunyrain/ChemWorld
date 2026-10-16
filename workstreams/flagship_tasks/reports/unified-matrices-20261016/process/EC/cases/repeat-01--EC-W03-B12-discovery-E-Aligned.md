# repeat-01/EC-W03-B12-discovery-E-Aligned

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-01\EC-W03-B12-discovery-E-Aligned\participant\discovery-E-Aligned

## 同期笔记

### v1 · 公开事件 0

# Electrochemical mechanism notebook

## Prior expectations (before physical work)

**H1 [tentative] — signed overpotential controls useful conversion.** The nominal solvent and electrolyte potential shifts should move the effective onset, so equal applied potentials need not be comparable across materials. Moderate signed driving force should raise conversion, while excessive magnitude may reduce selectivity/energy efficiency. Opposite signs may be strongly asymmetric. Test with matched loading, volume, material, current cap and duration across potential sign/magnitude.

**H2 [tentative] — charge/time and current-cap effects separate kinetic from transport limits.** At fixed conditions, longer electrolysis should initially increase conversion/yield and later plateau or degrade selectivity. If current caps below the transport-limited current reduce conversion roughly with cap × time, charge limitation is implicated; weak cap dependence suggests potential/transport limitation.

**H3 [tentative] — materials act through transport, ohmic loss, proton activity, and onset shift.** E0/S0 should favor conductivity but may precipitate; E1 has favorable diffusion; E2 is acidic with positive onset shift; E3 is conductive but thick-layer limited. Solvent changes may trade conductivity against diffusion/solubility. I will use matched comparisons and treat nominal properties only as priors.

Initial design: first establish polarity and potential scale under a common loading, then compare duration/current and selected solvent/electrolyte changes, retaining replication where budget permits. Results will be interpreted against declared instrument noise; isolated small differences will remain unresolved.

### v2 · 公开事件 84

# Electrochemical mechanism notebook

## Scope
All quantitative relationships below are restricted to the tested loading (0.020 mol reagent in 0.040 L solvent), this campaign's fixed cell, and the stated material labels. Final-assay standard deviations are those declared by the instrument; small single-batch differences are not treated as established effects.

## H1 [supported in tested scope] — polarity and a bounded useful potential window
For E1/S0 at 100 mA and 3600 s, moving from -1.0 V to +0.5 V to +1.0 V increased conversion (about 0.026, 0.063, 0.092), selectivity (0.604, 0.804, 0.942), and faradaic efficiency (0.367, 0.749, 0.928): final assays at runner-operation-0014, -0028, and -0007. Thus polarity is mechanistically consequential, not merely an energy sign convention. At +2.0 V all reaction-related efficiencies and conversion were reported as zero (runner-operation-0021), rejecting a monotonic-overpotential law and indicating a sharp destructive/inactive high-potential regime. The exact onset/peak remains unresolved because 1–2 V was not densely sampled.

**Predictive consequence:** within the low-to-moderate positive branch, performance should improve toward roughly +1 V; negative polarity should be poor, and sufficiently high positive potential can collapse useful chemistry. Material standard-potential shifts should translate this window, but that translation was not isolated experimentally.

## H2 [supported] — cap × time controls conversion approximately through saturating charge exposure
At E1/S0 and +1.0 V, conversion was 0.092 at 100 mA × 3600 s, 0.255 at 100 mA × 10800 s, and 0.445 at 500 mA × 3600 s (runner-operation-0007, -0042, -0035). A compact empirical law is

`X ≈ 1 − exp(−k I_cap t)`

with individual `k = −ln(1−X)/(I_cap t)` about 2.7e-7, 2.7e-7, and 3.3e-7 (mA·s)^−1. Agreement of the first two supports time scaling; the high-cap point suggests either modest cap-dependent delivery/kinetics or noise/model incompleteness. Because current_mA is only a cap, this is an empirical cap-exposure law, not proof that delivered current always equals the cap.

Useful yield is approximately conversion times selectivity in this regime. Selectivity and faradaic efficiency stayed high at +1 V across the tested exposures, so no late-time selectivity loss was resolved through 10800 s. Extrapolation should saturate rather than remain linear.

## H3 [supported] — electrolyte changes primarily alter transport/faradaic behavior; precipitation alone is insufficient
At S0, +1 V, 500 mA, 3600 s, E1 and E2 gave high conversion (0.445 and 0.407) and faradaic/transport efficiencies near 0.96/0.95 and 0.89/0.88, whereas E0 and E3 gave conversion near 0.079/0.069 and faradaic/transport efficiencies near 0.15/0.15 (runner-operation-0035, -0056, -0049, -0063). These gaps greatly exceed stated assay noise.

E0 had near-maximal precipitation signal (~0.983) and poor performance, consistent with blockage or loss, but E3 was also poor with almost no precipitation; E2 was strong with almost no precipitation. Therefore precipitation can be a penalty but is not the sole material mechanism. Diffusion-layer/onset/interface effects remain necessary. The pH-normalized ordering also tracked declared acidity differences, supporting that the electrolyte identities were physically expressed, but pH by itself did not rank performance.

## H4 [supported for ranking, mechanism unresolved] — solvent controls selectivity and charge utilization beyond ohmic loss
With E1, +1 V, 500 mA, 3600 s, the performance ranking was S1 > S0 > S2 > S3 by yield/score: selective yields about 0.440, 0.429, 0.336, 0.306 and selectivities about 0.999, 0.960, 0.882, 0.823 (runner-operation-0070, -0035, -0077, -0084). S1 versus S0 yield differs by only ~0.011, comparable to one assay SD, so their yield superiority is unresolved in a strict replicate sense; however S1's selectivity/transport advantages are larger. S2/S3 are clearly worse than S0/S1 on several channels.

Ohmic efficiency does not explain the ranking (S1 had lower ohmic efficiency than S0), favoring a mixed diffusion/solvation/interface-selectivity account. Unmeasured world residuals and the absence of replicate batches prevent attribution to one nominal solvent property.

## Working predictive model and limits
Use a product of: (i) a signed, material-shifted potential-window factor that peaks near the tested +1 V region and collapses by +2 V for E1/S0; (ii) saturating cap-exposure conversion `1−exp(−k I_cap t)`; (iii) material factors for faradaic/transport efficiency; and (iv) selectivity. For tested high-cap conditions, favor E1 with S1 or S0; E2/S0 is a credible lower-precipitation alternative. Do not generalize exact coefficients across solvents/electrolytes without accounting for shifted onset and current delivery.

Unresolved: exact potential-window shape, delivered-current law, short-time double-layer transients, whether very long runs eventually lose selectivity, and material interactions. Repetition was not available after the broad factorial comparisons, so marginal differences remain provisional.

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
    "cost": 0.28404000401496887,
    "electrochemical_conversion": 0.09225108474493027,
    "electrochemical_selectivity": 0.9417526721954346,
    "energy_efficiency": 0.9126999974250793,
    "faradaic_efficiency": 0.9275918006896973,
    "ohmic_efficiency": 0.9651356339454651,
    "pH_normalized": 0.20516636967658997,
    "precipitation_signal": 0.851891279220581,
    "safety_risk": 0.072194404900074,
    "score": 0.585107147693634,
    "selective_product_yield": 0.06434479355812073,
    "transport_efficiency": 0.8988880515098572
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
    "cost": 0.28404000401496887,
    "electrochemical_conversion": 0.026203947141766548,
    "electrochemical_selectivity": 0.6039119362831116,
    "energy_efficiency": 0.2876383662223816,
    "faradaic_efficiency": 0.3670108914375305,
    "ohmic_efficiency": 0.9739734530448914,
    "pH_normalized": 0.2024710327386856,
    "precipitation_signal": 0.854923665523529,
    "safety_risk": 0.072194404900074,
    "score": 0.3064347505569458,
    "selective_product_yield": 0.029319526627659798,
    "transport_efficiency": 0.3932677209377289
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
      "current_mA": 100,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 2
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
    "cost": 0.28547999262809753,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.0,
    "ohmic_efficiency": 0.9736093282699585,
    "pH_normalized": 0.2031860202550888,
    "precipitation_signal": 0.8373757600784302,
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
      "current_mA": 100,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 0.5
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
    "electrochemical_conversion": 0.06348096579313278,
    "electrochemical_selectivity": 0.8036198019981384,
    "energy_efficiency": 0.7501214742660522,
    "faradaic_efficiency": 0.7493657469749451,
    "ohmic_efficiency": 0.9471806883811951,
    "pH_normalized": 0.20249544084072113,
    "precipitation_signal": 0.8381239771842957,
    "safety_risk": 0.072194404900074,
    "score": 0.49392765760421753,
    "selective_product_yield": 0.05677401274442673,
    "transport_efficiency": 0.7178781628608704
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
    "cost": 0.2897999882698059,
    "electrochemical_conversion": 0.4445950388908386,
    "electrochemical_selectivity": 0.9596544504165649,
    "energy_efficiency": 0.8027181029319763,
    "faradaic_efficiency": 0.9568935632705688,
    "ohmic_efficiency": 0.8694413900375366,
    "pH_normalized": 0.20745623111724854,
    "precipitation_signal": 0.837450385093689,
    "safety_risk": 0.072194404900074,
    "score": 0.7165285348892212,
    "selective_product_yield": 0.428973913192749,
    "transport_efficiency": 0.946384072303772
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
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 10800,
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
    "cost": 0.2869200110435486,
    "electrochemical_conversion": 0.25486207008361816,
    "electrochemical_selectivity": 0.935645580291748,
    "energy_efficiency": 0.9021483659744263,
    "faradaic_efficiency": 0.9271261692047119,
    "ohmic_efficiency": 0.974196195602417,
    "pH_normalized": 0.2041803002357483,
    "precipitation_signal": 0.8480806946754456,
    "safety_risk": 0.072194404900074,
    "score": 0.6543042659759521,
    "selective_product_yield": 0.24571286141872406,
    "transport_efficiency": 0.9024428129196167
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
      "potential_V": 1
    },
    {
      "duration_s": 3600,
      "operation": "electrolyze"
    },
    {
      "instrument": "ph_meter",
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
    "cost": 0.28279998898506165,
    "electrochemical_conversion": 0.07906671613454819,
    "electrochemical_selectivity": 0.8269609212875366,
    "energy_efficiency": 0.1419116109609604,
    "faradaic_efficiency": 0.14948731660842896,
    "ohmic_efficiency": 0.9071170091629028,
    "pH_normalized": 0.22834065556526184,
    "precipitation_signal": 0.9828575253486633,
    "safety_risk": 0.072194404900074,
    "score": 0.2783135175704956,
    "selective_product_yield": 0.06426452100276947,
    "transport_efficiency": 0.15288767218589783
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
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 3600,
      "operation": "electrolyze"
    },
    {
      "instrument": "ph_meter",
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
    "cost": 0.28279998898506165,
    "electrochemical_conversion": 0.40690016746520996,
    "electrochemical_selectivity": 0.8757033944129944,
    "energy_efficiency": 0.738067626953125,
    "faradaic_efficiency": 0.8912370800971985,
    "ohmic_efficiency": 0.8595408797264099,
    "pH_normalized": 0.15112711489200592,
    "precipitation_signal": 0.00031451715040020645,
    "safety_risk": 0.072194404900074,
    "score": 0.6495858430862427,
    "selective_product_yield": 0.3421476483345032,
    "transport_efficiency": 0.8847417235374451
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
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 3600,
      "operation": "electrolyze"
    },
    {
      "instrument": "ph_meter",
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
    "cost": 0.28279998898506165,
    "electrochemical_conversion": 0.06941216439008713,
    "electrochemical_selectivity": 0.8296722173690796,
    "energy_efficiency": 0.22823812067508698,
    "faradaic_efficiency": 0.14425131678581238,
    "ohmic_efficiency": 0.9187588095664978,
    "pH_normalized": 0.27438896894454956,
    "precipitation_signal": 0.008188718929886818,
    "safety_risk": 0.072194404900074,
    "score": 0.296060711145401,
    "selective_product_yield": 0.07704611122608185,
    "transport_efficiency": 0.16508258879184723
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
    "cost": 0.3057999908924103,
    "electrochemical_conversion": 0.46738967299461365,
    "electrochemical_selectivity": 0.9985705614089966,
    "energy_efficiency": 0.8159557580947876,
    "faradaic_efficiency": 0.9782118201255798,
    "ohmic_efficiency": 0.8072202205657959,
    "pH_normalized": 0.20839183032512665,
    "precipitation_signal": 0.6566107869148254,
    "safety_risk": 0.09559440612792969,
    "score": 0.7309367060661316,
    "selective_product_yield": 0.4403320252895355,
    "transport_efficiency": 0.9795613884925842
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
      "current_mA": 500,
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
    "cost": 0.3314000070095062,
    "electrochemical_conversion": 0.3895496726036072,
    "electrochemical_selectivity": 0.8816357851028442,
    "energy_efficiency": 0.710285484790802,
    "faradaic_efficiency": 0.8086020946502686,
    "ohmic_efficiency": 0.7859451174736023,
    "pH_normalized": 0.2236795276403427,
    "precipitation_signal": 0.4877839982509613,
    "safety_risk": 0.1135944053530693,
    "score": 0.62015300989151,
    "selective_product_yield": 0.3364126980304718,
    "transport_efficiency": 0.8157820701599121
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
    "cost": 0.31540000438690186,
    "electrochemical_conversion": 0.3343871235847473,
    "electrochemical_selectivity": 0.8225716948509216,
    "energy_efficiency": 0.7065211534500122,
    "faradaic_efficiency": 0.7180341482162476,
    "ohmic_efficiency": 0.867375373840332,
    "pH_normalized": 0.21319545805454254,
    "precipitation_signal": 0.5728781223297119,
    "safety_risk": 0.12619440257549286,
    "score": 0.5839888453483582,
    "selective_product_yield": 0.30568727850914,
    "transport_efficiency": 0.7392591238021851
  }
}
```

## K1 封存报告

Mechanistic account

1. Experimental domain and observations

All 12 batches used 0.020 mol of the anonymous limiting reagent in 0.040 L of one anonymous solvent. The cell fixture was fixed across the campaign. Applied potential, current cap, electrolysis time, solvent, and electrolyte were varied. Every batch received a post-electrolysis intermediate measurement and a final assay. The conclusions below concern this synthetic world and this loading; the anonymous labels do not imply real chemical identities.

The main empirical picture is a polarity-sensitive electrochemical conversion with a bounded useful potential window, charge-exposure-dependent conversion, and strong electrolyte/solvent modulation of transport, faradaic efficiency, and selectivity.

2. Potential dependence

The matched E1/S0 experiments at 100 mA and 3600 s established the potential response:

• Batch 2, −1.0 V: conversion 0.0262, selectivity 0.6039, faradaic efficiency 0.3670, transport efficiency 0.3933, energy efficiency 0.2876, and selective-product yield 0.0293.
• Batch 4, +0.5 V: conversion 0.0635, selectivity 0.8036, faradaic efficiency 0.7494, transport efficiency 0.7179, energy efficiency 0.7501, and yield 0.0568.
• Batch 1, +1.0 V: conversion 0.0923, selectivity 0.9418, faradaic efficiency 0.9276, transport efficiency 0.8989, energy efficiency 0.9127, and yield 0.0643.
• Batch 3, +2.0 V: conversion, selectivity, faradaic efficiency, transport efficiency, energy efficiency, and yield were all reported as zero, while ohmic efficiency remained 0.9736.

Thus, potential is not merely controlling electrical power. Positive polarization up to approximately +1 V progressively activates productive charge transfer and improves selectivity, whereas negative polarization is inefficient and poorly selective. Batch 3 decisively rejected a monotonic “more positive is always better” model. Because its ohmic channel remained high while reaction-related channels collapsed, the +2 V result is more consistent with leaving the useful interfacial reaction window than with simple loss of bulk conductivity.

A useful phenomenological representation is

η = Vapp − V0(E,S)

rateuseful ∝ fwindow(η) × ftransport(E,S,I) × remaining reactant,

where fwindow is small at negative η, rises over a positive activation region, peaks near the tested +1 V region for E1/S0, and collapses at sufficiently large positive η. The collapse might represent an inactive surface state, diversion into an unobserved side process, or destruction of the useful pathway. These alternatives cannot be distinguished because degradation products, electrode state, and delivered current were not directly measured. The exact location and width of the window are also unidentifiable because no potentials between +1 and +2 V were tested.

The nominal standard-potential shifts of both solvent and electrolyte plausibly enter V0(E,S). However, the campaign did not perform a potential scan separately for every material, so a quantitative additive shift law remains conjectural.

3. Charge exposure and conversion kinetics

At E1/S0 and +1.0 V, batches 1, 5, and 6 separated current-cap and time effects:

• Batch 1: 100 mA × 3600 s gave conversion 0.0923.
• Batch 6: 100 mA × 10800 s gave conversion 0.2549.
• Batch 5: 500 mA × 3600 s gave conversion 0.4446.

The threefold time increase from batch 1 to batch 6 produced approximately a 2.76-fold conversion increase. Increasing the cap fivefold at constant time produced approximately a 4.82-fold increase. These observations support accumulated charge exposure as a principal state variable.

A compact empirical model is

X = 1 − exp(−k Icap t),

within a fixed potential/material regime. The inferred k values are approximately 2.69×10⁻⁷, 2.73×10⁻⁷, and 3.27×10⁻⁷ (mA·s)⁻¹ for batches 1, 6, and 5 respectively. The close agreement of batches 1 and 6 is particularly supportive of first-order depletion or another saturating exposure law. Batch 5’s somewhat larger apparent coefficient could reflect cap-dependent interfacial kinetics, different actual current utilization, or ordinary model and assay error.

This is explicitly a current-cap model, not a direct Faraday-law determination. Actual current, electron stoichiometry, electrode area, and current-time traces were unavailable. Consequently, I cannot identify an intrinsic rate constant or electrons transferred per molecule. Linear extrapolation is inappropriate near high conversion; the exponential form predicts saturation as reactant is depleted.

At +1 V, selectivity and faradaic efficiency remained high as exposure increased. Batch 6 at 10800 s retained selectivity 0.9356 and faradaic efficiency 0.9271; batch 5 at the higher cap had selectivity 0.9597 and faradaic efficiency 0.9569. Therefore, no late-time selectivity decay was resolved within the tested range. Longer exposures might eventually encounter depletion or secondary chemistry, but that is extrapolation rather than observation.

Selective-product yield was generally close to conversion multiplied by selectivity in the productive, higher-signal experiments: batch 5 had X×S ≈ 0.427 versus measured yield 0.429, and batch 10 had X×S ≈ 0.467 versus measured yield 0.440. The channels are independently noisy and should not be forced into exact algebraic identity, especially at low signal.

4. Electrolyte effects and transport

Batches 7, 5, 8, and 9 compared E0–E3 in S0 at +1.0 V, 500 mA, and 3600 s:

• E0, batch 7: conversion 0.0791, yield 0.0643, selectivity 0.8270, faradaic efficiency 0.1495, transport efficiency 0.1529, precipitation signal 0.9829, pH-normalized 0.2283.
• E1, batch 5: conversion 0.4446, yield 0.4290, selectivity 0.9597, faradaic efficiency 0.9569, transport efficiency 0.9464, precipitation signal 0.8375, pH-normalized 0.2075.
• E2, batch 8: conversion 0.4069, yield 0.3421, selectivity 0.8757, faradaic efficiency 0.8912, transport efficiency 0.8847, precipitation signal 0.0003, pH-normalized 0.1511.
• E3, batch 9: conversion 0.0694, yield 0.0770, selectivity 0.8297, faradaic efficiency 0.1443, transport efficiency 0.1651, precipitation signal 0.0082, pH-normalized 0.2744.

The large separation between E1/E2 and E0/E3 is much greater than the declared final-assay noise. Faradaic and transport efficiencies move together very strongly, suggesting that inadequate delivery to the productive interface, or transport-driven diversion of current, is a major electrolyte-dependent bottleneck.

The nominal dossier is qualitatively compatible with part of this result: E1 has the largest stated diffusivity and a thin diffusion layer, whereas E3 has the thickest diffusion layer. But no single published property explains all four electrolytes. E0 has high nominal conductivity yet performs poorly, and E2 performs strongly despite lower nominal conductivity. Conductivity therefore is not the controlling variable by itself.

Precipitation is also not a sufficient explanation. E0’s nearly maximal precipitation signal and poor transport are compatible with blocking or loss of active material. However, E1 performs very well despite a high precipitation signal, E2 performs well with almost none, and E3 performs poorly with almost none. Precipitation may impose a penalty in some electrolyte regimes, but onset shifts, diffusivity, double-layer behavior, proton environment, and fixed world-specific interfacial residuals are also required.

The pH-normalized ordering shows that electrolyte acidity is expressed in the final state, but pH alone does not rank performance. I therefore view proton activity as a coupled modifier of kinetics/selectivity rather than a one-dimensional performance predictor.

5. Solvent effects

Batches 5 and 10–12 compared S0–S3 with E1 at +1.0 V, 500 mA, and 3600 s:

• S0, batch 5: conversion 0.4446, yield 0.4290, selectivity 0.9597, faradaic efficiency 0.9569, transport efficiency 0.9464, ohmic efficiency 0.8694, score 0.7165.
• S1, batch 10: conversion 0.4674, yield 0.4403, selectivity 0.9986, faradaic efficiency 0.9782, transport efficiency 0.9796, ohmic efficiency 0.8072, score 0.7309.
• S2, batch 11: conversion 0.3895, yield 0.3364, selectivity 0.8816, faradaic efficiency 0.8086, transport efficiency 0.8158, ohmic efficiency 0.7859, score 0.6202.
• S3, batch 12: conversion 0.3344, yield 0.3057, selectivity 0.8226, faradaic efficiency 0.7180, transport efficiency 0.7393, ohmic efficiency 0.8674, score 0.5840.

The broad ranking is S1≈S0 > S2 > S3. The yield difference between S1 and S0 is only about 0.011, comparable to one stated yield standard deviation, so an intrinsic yield advantage for S1 over S0 is not established without replication. S1’s selectivity and transport estimates are nevertheless higher. The larger multichannel gaps separating S0/S1 from S2/S3 are more persuasive.

The solvent ranking cannot be reduced to ohmic efficiency: S3 had better ohmic efficiency than S1 and S2 but the worst conversion, selectivity, faradaic efficiency, and transport efficiency. Solvent therefore influences solvation, diffusion, proton activity, effective onset, and interfacial selectivity in addition to resistance. The nominal S1 diffusivity advantage is consistent with its strong transport result, but hidden fixed solvent-electrolyte residuals prevent assigning causality to that property alone.

Safety risk remained well below the 0.65 limit in all reported comparisons, although it increased across the solvent series under matched conditions: approximately 0.072 for S0, 0.096 for S1, 0.114 for S2, and 0.126 for S3.

6. Integrated working model

A practical state model for this world is:

η = Vapp − V0(E,S)
Iproductive = Icap × gohmic(E,S,I) × gtransport(E,S,I) × gwindow(η)
dX/dt = kapp(E,S,η) × Iproductive × (1−X)
Yselective ≈ X × Sel(E,S,η,X)

Faradaic efficiency represents the fraction of delivered charge entering productive electrochemistry; transport efficiency represents access of reactant or charge carrier to the productive interface; ohmic efficiency represents the voltage fraction not lost resistively. These factors are coupled rather than strictly independent. Precipitation can lower accessible area or transport, while proton activity and double-layer properties can shift interfacial kinetics and selectivity.

For E1/S0 near +1 V, the data permit the reduced exposure law X≈1−exp(−kIcap t) with k around 3×10⁻⁷ (mA·s)⁻¹. Outside this local regime, k must be multiplied by material and potential-window factors. Applying the same coefficient at −1 V, +2 V, or to E0/E3 would be contradicted by the observations.

7. How the explanation changed

The initial hypothesis was that increasing signed overpotential would raise conversion until selectivity eventually deteriorated. Batches 2, 4, and 1 supported polarity dependence and rising performance toward +1 V. Batch 3 then forced a major revision: the response has a sharp bounded window rather than a monotonic or gently saturating potential law.

Batches 5 and 6 established accumulated cap-time exposure as the simplest conversion coordinate and supported a saturating kinetic law. Batches 7–9 changed the material explanation from a conductivity or precipitation ranking to a coupled transport/interfacial account: precipitation could explain E0 poorly but could not explain E3. Finally, batches 10–12 showed that solvent-dependent selectivity and faradaic/transport utilization matter more than ohmic efficiency alone.

8. Scope, uncertainty, and alternatives

There were no independent replicate batches, so small differences—especially S1 versus S0 yield—remain provisional. Instrument standard deviations quantify synthetic measurement noise but do not cover all model discrepancy. The fixture was constant, making comparisons internally valid but preventing identification of electrode-area, gap, and contact-resistance effects. Anonymous material identities, actual current traces, electrode surface state, electron stoichiometry, temperature evolution, and hidden world residuals were not observable.

Plausible alternative accounts include a homogeneous potential-dependent chemical step following electron transfer, surface passivation at +2 V, competitive solvent or electrolyte oxidation, mass-transfer-limited current with material-dependent limiting values, or a change in product detectability at extreme potential. The current data favor a potential-window plus charge-exposure model but do not uniquely select among those microscopic mechanisms.

The most defensible predictions are therefore local: near the tested loading and E1 with S0/S1, moderate positive potential around +1 V should outperform negative polarization; conversion should initially scale with current-cap × time and then saturate; +2 V should not be treated as an improvement; and E0/E3 are likely to remain transport/faradaic limited unless another potential window or operating regime is found.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific mechanism or solution prior was supplied. The only supplied scientific prior was the public nominal material dossier. It described properties such as conductivity, diffusivity, diffusion-layer thickness, acidity, precipitation tendency, capacitance, and nominal potential shifts, while explicitly warning that hidden fixed residuals and solvent coupling remained. I therefore treated it as mechanistic prior information, not ground truth about performance.

Supported claims and laws:

• Signed potential matters. Under otherwise matched E1/S0, 100 mA, 3600 s conditions, moving from −1.0 V in batch 2 to +0.5 V in batch 4 and +1.0 V in batch 1 raised conversion from 0.026 to 0.063 to 0.092, selectivity from 0.604 to 0.804 to 0.942, and faradaic efficiency from 0.367 to 0.749 to 0.928. This supported the pre-experiment claim that polarity and effective overpotential control productive chemistry.

• Conversion depends approximately on accumulated current-cap × time exposure within the E1/S0, +1 V regime. Batch 1 gave conversion 0.092 at 100 mA for 3600 s; batch 6 gave 0.255 at the same cap for 10800 s; batch 5 gave 0.445 at 500 mA for 3600 s. The first two gave nearly identical coefficients in the empirical law X≈1−exp(−kIcap t), about 2.7×10⁻⁷ (mA·s)⁻¹. Batch 5 was reasonably consistent but implied a somewhat larger coefficient. This supported a saturating exposure model, although not a literal Faraday-law interpretation because actual current was unmeasured.

• Electrolyte effects are strongly associated with transport and faradaic utilization. At S0, +1 V, 500 mA, and 3600 s, E1 and E2 in batches 5 and 8 had transport efficiencies of 0.946 and 0.885 and conversions of 0.445 and 0.407. E0 and E3 in batches 7 and 9 had transport efficiencies of only 0.153 and 0.165 and conversions of 0.079 and 0.069. These differences were much larger than declared assay noise.

• Solvent affects interfacial selectivity and charge utilization, not only resistance. In the matched E1 comparison, batches 5 and 10–12 ranked approximately S1≈S0>S2>S3 in yield, faradaic efficiency, and transport efficiency. Ohmic efficiency did not follow that ranking: for example, S3 in batch 12 had ohmic efficiency 0.867, higher than S1’s 0.807 in batch 10, but substantially worse conversion, selectivity, and yield.

Contradicted or substantially revised claims:

• A monotonic “larger positive potential gives more conversion” law was contradicted by batch 3. At +2.0 V, reaction-related final metrics were reported as zero even though ohmic efficiency remained 0.974. This changed the account from monotonic activation to a bounded productive potential window with a high-potential inactive or destructive regime.

• Bulk conductivity alone did not rank electrolytes. E0 had high nominal conductivity but performed poorly in batch 7, while lower-conductivity E2 performed strongly in batch 8.

• Precipitation alone did not explain electrolyte performance. E0’s poor batch 7 coincided with a precipitation signal of 0.983, but E1 performed well in batch 5 despite a signal of 0.837. E3 was poor in batch 9 with a precipitation signal of only 0.008, while E2 was strong in batch 8 with essentially no precipitation. Precipitation may contribute, but it is neither necessary nor sufficient for poor performance.

• A purely ohmic solvent model was contradicted by batches 5 and 10–12, as noted above.

Untested or only weakly tested claims:

• The nominal solvent and electrolyte standard-potential shifts may translate the useful potential window, but each material was not scanned across potential, so an additive V0(E,S) law was not tested.

• The exponential exposure law was supported only at moderate conversion in one material regime. True high-conversion saturation was not observed.

• Actual delivered current, electron stoichiometry, limiting-current values, electrode area effects, and short-time double-layer transients were not measured.

• Irreversible degradation, reversible surface inactivity, substrate destruction, and diversion into an unobserved side reaction remain observationally confounded at +2 V.

• Long-time selectivity loss was not observed through batch 6 at 10800 s, but longer-time or higher-conversion behavior remains untested.

2. One additional discriminating experiment

I would repeat the batch-1 composition, E1/S0 with 0.020 mol reagent in 0.040 L, but use a two-stage potential sequence: first electrolyze at +2.0 V for 3600 s, then reset to +1.0 V and electrolyze for 3600 s before termination and final assay. An intermediate permitted measurement after the +2 V stage would be useful, but the decisive observation would be the final assay after the +1 V recovery stage.

The leading phenomenological explanation is that +2 V lies outside a bounded productive window. A major alternative is that the +2 V treatment irreversibly destroys substrate, product-forming capacity, or the active interface.

• If the final conversion, yield, and efficiencies recover to approximately the batch-1 neighborhood after the +1 V stage, the +2 V state was mostly reversible or simply nonproductive while applied. I would strengthen the bounded reversible-window interpretation.

• If the final result remains near batch 3’s zero reaction-related response, I would favor irreversible passivation, substrate destruction, or persistent poisoning.

• Partial recovery would imply mixed behavior. Dependence on the duration of the +2 V pre-treatment would then become the next question, but one experiment could not separate substrate loss from electrode damage.

This experiment is more discriminating than another single-potential endpoint because batch 3 alone cannot reveal whether productive capacity survives the extreme-potential exposure.

3. Unused evidence, reliability, and effect of the goal

The raw spectral artifacts were not analyzed in detail; the account relied mainly on calibrated processed estimates and the supplied peak assignments. Most intermediate UV–visible and pH measurements were also underused because they were taken after electrolysis and did not constitute a genuine time course. Batch 1’s intermediate UV–visible efficiencies broadly agreed with its final assay, but intermediate instruments were noisier and did not expose all required outcomes. Nominal capacitance, acid pKa, supporting-electrolyte concentration, Ksp, and solubility factors informed qualitative hypotheses but were not fitted quantitatively. Cost, raw process time, and detailed spectral shapes were not central to the mechanism model.

The least reliable blind predictions are those requiring unobserved material interactions or cap extrapolation: Q09 and Q10 combine E0 with S2, a pairing never tested; Q01–Q04 extrapolate E0 from 500 mA to 100 mA; Q11 and Q12 depend strongly on whether E0 is limiting-current constrained; and Q07–Q08 similarly extrapolate E3 to a lower current cap. Q01 and Q02 are additionally fragile because their predicted yields lie near the score contract’s 0.02 multiplicative gate. The E1 predictions Q05 and Q06 are comparatively better constrained by batches 1, 2, 4–6.

The sealed recommendation of batch 10 is reliable as the highest observed score, but its exact superiority over batch 5 is not strongly established: their selective yields differed by only about 0.011, comparable to one final-assay yield standard deviation, and neither was replicated. The broader conclusion that E1 with S0 or S1 around +1 V is favorable is more reliable than the precise S1>S0 ranking.

The assigned primary goal did affect evidence collection. Because explanation and prediction were prioritized over score optimization, the campaign spent batches on polarity, duration, current, all four electrolytes, and all four solvents rather than repeatedly refining the best recipe. This produced broad mechanistic contrasts but left no independent replication, a sparse potential grid, and incomplete interaction coverage. The public score was still useful as a secondary summary and determined the sealed operating selection, but it did not exclusively drive the experimental design. There was no clear conflict with safety: all tested batches remained below the stated risk limit.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.43,
        "upper80": 0.74
      },
      "energy_efficiency": {
        "estimate": 0.3,
        "lower80": 0.14,
        "upper80": 0.47
      },
      "faradaic_efficiency": {
        "estimate": 0.34,
        "lower80": 0.18,
        "upper80": 0.5
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.1,
        "lower80": 0.01,
        "upper80": 0.27
      },
      "selective_product_yield": {
        "estimate": 0.007,
        "lower80": 0.0,
        "upper80": 0.024
      },
      "transport_efficiency": {
        "estimate": 0.38,
        "lower80": 0.21,
        "upper80": 0.55
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.8,
        "lower80": 0.67,
        "upper80": 0.9
      },
      "energy_efficiency": {
        "estimate": 0.68,
        "lower80": 0.51,
        "upper80": 0.82
      },
      "faradaic_efficiency": {
        "estimate": 0.7,
        "lower80": 0.53,
        "upper80": 0.84
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.44,
        "lower80": 0.18,
        "upper80": 0.57
      },
      "selective_product_yield": {
        "estimate": 0.019,
        "lower80": 0.004,
        "upper80": 0.043
      },
      "transport_efficiency": {
        "estimate": 0.73,
        "lower80": 0.55,
        "upper80": 0.87
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.44,
        "upper80": 0.73
      },
      "energy_efficiency": {
        "estimate": 0.3,
        "lower80": 0.15,
        "upper80": 0.46
      },
      "faradaic_efficiency": {
        "estimate": 0.34,
        "lower80": 0.19,
        "upper80": 0.5
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.33,
        "lower80": 0.21,
        "upper80": 0.45
      },
      "selective_product_yield": {
        "estimate": 0.078,
        "lower80": 0.038,
        "upper80": 0.13
      },
      "transport_efficiency": {
        "estimate": 0.38,
        "lower80": 0.22,
        "upper80": 0.54
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.8,
        "lower80": 0.68,
        "upper80": 0.89
      },
      "energy_efficiency": {
        "estimate": 0.68,
        "lower80": 0.52,
        "upper80": 0.81
      },
      "faradaic_efficiency": {
        "estimate": 0.7,
        "lower80": 0.54,
        "upper80": 0.83
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.54,
        "lower80": 0.43,
        "upper80": 0.64
      },
      "selective_product_yield": {
        "estimate": 0.19,
        "lower80": 0.12,
        "upper80": 0.28
      },
      "transport_efficiency": {
        "estimate": 0.73,
        "lower80": 0.56,
        "upper80": 0.86
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.64,
        "lower80": 0.53,
        "upper80": 0.74
      },
      "energy_efficiency": {
        "estimate": 0.36,
        "lower80": 0.25,
        "upper80": 0.48
      },
      "faradaic_efficiency": {
        "estimate": 0.43,
        "lower80": 0.32,
        "upper80": 0.55
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.36,
        "lower80": 0.28,
        "upper80": 0.44
      },
      "selective_product_yield": {
        "estimate": 0.064,
        "lower80": 0.036,
        "upper80": 0.1
      },
      "transport_efficiency": {
        "estimate": 0.46,
        "lower80": 0.34,
        "upper80": 0.58
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.9,
        "lower80": 0.83,
        "upper80": 0.96
      },
      "energy_efficiency": {
        "estimate": 0.86,
        "lower80": 0.76,
        "upper80": 0.94
      },
      "faradaic_efficiency": {
        "estimate": 0.88,
        "lower80": 0.8,
        "upper80": 0.95
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.62,
        "lower80": 0.55,
        "upper80": 0.69
      },
      "selective_product_yield": {
        "estimate": 0.22,
        "lower80": 0.16,
        "upper80": 0.29
      },
      "transport_efficiency": {
        "estimate": 0.86,
        "lower80": 0.76,
        "upper80": 0.94
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.43,
        "upper80": 0.74
      },
      "energy_efficiency": {
        "estimate": 0.25,
        "lower80": 0.1,
        "upper80": 0.42
      },
      "faradaic_efficiency": {
        "estimate": 0.3,
        "lower80": 0.14,
        "upper80": 0.47
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.3,
        "lower80": 0.19,
        "upper80": 0.42
      },
      "selective_product_yield": {
        "estimate": 0.052,
        "lower80": 0.02,
        "upper80": 0.1
      },
      "transport_efficiency": {
        "estimate": 0.34,
        "lower80": 0.17,
        "upper80": 0.51
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.82,
        "lower80": 0.7,
        "upper80": 0.91
      },
      "energy_efficiency": {
        "estimate": 0.68,
        "lower80": 0.5,
        "upper80": 0.82
      },
      "faradaic_efficiency": {
        "estimate": 0.72,
        "lower80": 0.54,
        "upper80": 0.85
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.53,
        "lower80": 0.4,
        "upper80": 0.64
      },
      "selective_product_yield": {
        "estimate": 0.15,
        "lower80": 0.08,
        "upper80": 0.24
      },
      "transport_efficiency": {
        "estimate": 0.75,
        "lower80": 0.56,
        "upper80": 0.88
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.36,
        "upper80": 0.71
      },
      "energy_efficiency": {
        "estimate": 0.18,
        "lower80": 0.04,
        "upper80": 0.36
      },
      "faradaic_efficiency": {
        "estimate": 0.22,
        "lower80": 0.07,
        "upper80": 0.41
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.26,
        "lower80": 0.13,
        "upper80": 0.39
      },
      "selective_product_yield": {
        "estimate": 0.033,
        "lower80": 0.007,
        "upper80": 0.081
      },
      "transport_efficiency": {
        "estimate": 0.25,
        "lower80": 0.08,
        "upper80": 0.45
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.74,
        "lower80": 0.57,
        "upper80": 0.87
      },
      "energy_efficiency": {
        "estimate": 0.45,
        "lower80": 0.25,
        "upper80": 0.64
      },
      "faradaic_efficiency": {
        "estimate": 0.52,
        "lower80": 0.31,
        "upper80": 0.7
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.42,
        "lower80": 0.29,
        "upper80": 0.55
      },
      "selective_product_yield": {
        "estimate": 0.12,
        "lower80": 0.055,
        "upper80": 0.21
      },
      "transport_efficiency": {
        "estimate": 0.55,
        "lower80": 0.33,
        "upper80": 0.73
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.39,
        "upper80": 0.73
      },
      "energy_efficiency": {
        "estimate": 0.06,
        "lower80": 0.0,
        "upper80": 0.19
      },
      "faradaic_efficiency": {
        "estimate": 0.07,
        "lower80": 0.0,
        "upper80": 0.21
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.2,
        "lower80": 0.1,
        "upper80": 0.32
      },
      "selective_product_yield": {
        "estimate": 0.028,
        "lower80": 0.004,
        "upper80": 0.073
      },
      "transport_efficiency": {
        "estimate": 0.08,
        "lower80": 0.0,
        "upper80": 0.23
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.8,
        "lower80": 0.67,
        "upper80": 0.89
      },
      "energy_efficiency": {
        "estimate": 0.14,
        "lower80": 0.03,
        "upper80": 0.29
      },
      "faradaic_efficiency": {
        "estimate": 0.15,
        "lower80": 0.04,
        "upper80": 0.3
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.32,
        "lower80": 0.23,
        "upper80": 0.43
      },
      "selective_product_yield": {
        "estimate": 0.175,
        "lower80": 0.09,
        "upper80": 0.28
      },
      "transport_efficiency": {
        "estimate": 0.16,
        "lower80": 0.04,
        "upper80": 0.32
      }
    }
  ],
  "rationale": "Predictions use the campaign's signed potential window, a saturating current-cap×time exposure law adjusted for the smaller reagent charge requirement, and electrolyte/solvent-specific transport and faradaic factors. E1 is the best-constrained electrolyte; E0 and E3 require wider intervals because their only matched high-current observations were strongly transport-limited. Negative polarization lowers charge utilization and selectivity, while E0 at 500 mA is predicted to remain limiting-current constrained. Intervals combine assay noise with substantial extrapolation uncertainty; short runs also have score uncertainty from the selective-yield gate near 0.02."
}
```
