# repeat-03/EC-W01-B12-optimization-E-Opaque

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-03\EC-W01-B12-optimization-E-Opaque\participant\optimization-E-Opaque

## 同期笔记

### v1 · 公开事件 0

# Electrochemical campaign hypotheses

## H1 [tentative]
Balanced efficiency will have an interior optimum in potential magnitude and electrolysis duration: weak/short conditions under-convert, while strong/long conditions reduce selectivity and energy efficiency. This should appear as a score maximum rather than monotonic improvement.

## H2 [tentative]
Solvent and electrolyte identities may strongly control transport and ohmic efficiency. Initial batches will screen both potential signs and material combinations at a fixed loading, then later batches will refine the best region.

## H3 [tentative]
The current setting is only a cap; once above the cell's delivered-current regime, increasing the cap may have little benefit. Comparison at otherwise matched conditions can distinguish cap limitation from potential/time limitation.

Planned interpretation rule: treat final-assay differences as provisional when comparable to declared channel noise; prioritize replicated or large multimetric improvements. Evidence that the best point lies on a tested boundary will trigger expansion toward that boundary rather than immediate replication.

### v2 · 公开事件 49

# Electrochemical campaign hypotheses

## H1 [supported qualitatively; optimum unresolved]
Negative potential is the productive sign in the tested S0/E0 system: at ±1.2 V, 100 mA, 600 s, the negative-sign batch produced measurable yield and a 0.171 score whereas the positive-sign batch scored zero (events runner-operation-0007 and -0014). Moving simultaneously to -1.5 V and 3600 s did not improve S0/E0 (event -0021), so stronger/longer is not automatically better. Potential and duration remain confounded.

## H2 [supported for paired formulations; components unresolved]
At -1.2 V, 100 mA, 3600 s, paired S3/E3 gave the highest observed score (0.258; event -0042), exceeding paired S1/E1 and S2/E2 (~0.222–0.224; events -0028, -0035). Since solvent and electrolyte changed together, their individual effects and cross-combinations remain unresolved. Low precipitation in S2/E2 and S3/E3, versus strong precipitation in S0/E0, is associated with the better scores but is not established as causal.

## H3 [supported in tested high-cap contrast]
For S3/E3 at -1.2 V and 3600 s, raising the current cap from 100 to 500 mA increased measured conversion/yield modestly but sharply lowered faradaic, transport and energy efficiencies, reducing score from 0.258 to 0.196 (events -0042, -0049). Thus 500 mA is not preferred in this scope. A moderate cap below or near 100 mA should be refined.

## Next tests
Use S3/E3 as the provisional platform. Separate time, potential and moderate current-cap effects, then replicate/refine the best condition. A cross-combination is lower priority unless remaining results suggest the paired-material advantage is weak.

### v3 · 公开事件 84

# Electrochemical campaign hypotheses — final source-stage record

## H1 [supported in tested scope]
Negative potential is required for productive behavior in the direct ±1.2 V comparison (events runner-operation-0007 and -0014). Within S3/E3, -0.8 V improved energy efficiency and selectivity relative to -1.2 V while retaining useful conversion (events -0070 and -0084 versus -0042). Thus the best tested potential region is near -0.8 V, not the magnitude boundary. The exact optimum is unresolved because only sparse potentials were tested.

## H2 [supported for paired formulations; component attribution unresolved]
At -1.2 V, 100 mA, 3600 s, paired S3/E3 had the strongest observed result among the four same-index solvent/electrolyte pairs (events -0021, -0028, -0035, -0042). S3/E3 also showed negligible precipitation. Solvent and electrolyte effects were not separated by cross-combinations, so recommendation applies to the pair rather than either component individually.

## H3 [supported in tested contrasts]
A 500 mA cap at S3/E3, -1.2 V, 3600 s reduced faradaic, transport, and energy efficiencies despite modestly greater conversion/yield, lowering score (event -0049 versus -0042). At -0.8 V, 50 mA gave lower conversion and score than 100 mA (event -0077 versus -0070). The preferred tested cap is therefore 100 mA; values between 50 and 100 mA remain untested.

## H4 [duration optimum unresolved, long duration disfavored]
At S3/E3 and -1.2 V, 1800 and 3600 s produced similar scores (~0.259), while 7200 s was substantially worse (events -0063, -0042, -0056). Channel noise, especially the 0.01 selective-yield noise and yield gating, prevents strong discrimination between 1800 and 3600 s. The 3600 s setting is retained because it was used in two independent -0.8 V batches.

## Recommended operating region
Fixed tested loading: 0.020 mol limiting reagent in 0.050 L solvent-S3; electrolyte-E3; -0.8 V; current cap 100 mA; electrolyze 3600 s. Independent batches 10 and 12 support similar selectivity and efficiency profiles (events -0070 and -0084), although their conversion and selective-yield estimates differ beyond what a simple deterministic relation would imply. This discrepancy is treated as measurement/process variability, not as evidence that one replicate is mechanistically superior. Batch 12 has the highest observed public score (0.295), while batch 10 provides the stronger measured conversion; the repeated procedure is preferred over selecting an isolated noisy endpoint.

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
      "volume_L": 0.05
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
    "ohmic_efficiency": 0.9730915427207947,
    "pH_normalized": 0.23218974471092224,
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
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.05
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
    "electrochemical_selectivity": 0.5988643765449524,
    "energy_efficiency": 0.17134326696395874,
    "faradaic_efficiency": 0.3593781888484955,
    "ohmic_efficiency": 0.981929361820221,
    "pH_normalized": 0.2294943928718567,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.1714622974395752,
    "selective_product_yield": 0.012271160259842873,
    "transport_efficiency": 0.38563501834869385
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
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
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
    "cost": 0.2871600091457367,
    "electrochemical_conversion": 0.02374766394495964,
    "electrochemical_selectivity": 0.5371297597885132,
    "energy_efficiency": 0.11437976360321045,
    "faradaic_efficiency": 0.2864631712436676,
    "ohmic_efficiency": 0.9722567200660706,
    "pH_normalized": 0.23020939528942108,
    "precipitation_signal": 0.9868234395980835,
    "safety_risk": 0.05933958664536476,
    "score": 0.06460190564393997,
    "selective_product_yield": 0.00529205147176981,
    "transport_efficiency": 0.30302008986473083
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
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 1,
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
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "metrics": {
    "cost": 0.3067280054092407,
    "electrochemical_conversion": 0.02518150582909584,
    "electrochemical_selectivity": 0.5257735252380371,
    "energy_efficiency": 0.1846659630537033,
    "faradaic_efficiency": 0.33877280354499817,
    "ohmic_efficiency": 0.9695844650268555,
    "pH_normalized": 0.20294250547885895,
    "precipitation_signal": 0.7142676115036011,
    "safety_risk": 0.08273958414793015,
    "score": 0.2216448187828064,
    "selective_product_yield": 0.016849547624588013,
    "transport_efficiency": 0.30728524923324585
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
      "solvent": 2,
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
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
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "metrics": {
    "cost": 0.33872801065444946,
    "electrochemical_conversion": 0.027518093585968018,
    "electrochemical_selectivity": 0.45006775856018066,
    "energy_efficiency": 0.1548732966184616,
    "faradaic_efficiency": 0.2690587639808655,
    "ohmic_efficiency": 0.9525505900382996,
    "pH_normalized": 0.17220906913280487,
    "precipitation_signal": 0.0,
    "safety_risk": 0.10073958337306976,
    "score": 0.22357548773288727,
    "selective_product_yield": 0.01914321631193161,
    "transport_efficiency": 0.258549302816391
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
      "solvent": 3,
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
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
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "metrics": {
    "cost": 0.3187279999256134,
    "electrochemical_conversion": 0.02658137120306492,
    "electrochemical_selectivity": 0.5347115397453308,
    "energy_efficiency": 0.1966504007577896,
    "faradaic_efficiency": 0.2859621047973633,
    "ohmic_efficiency": 0.9822806119918823,
    "pH_normalized": 0.28623321652412415,
    "precipitation_signal": 0.0023995577357709408,
    "safety_risk": 0.11333958804607391,
    "score": 0.25837719440460205,
    "selective_product_yield": 0.023296641185879707,
    "transport_efficiency": 0.26127877831459045
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
      "solvent": 3,
      "volume_L": 0.05
    },
    {
      "current_mA": 500,
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
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "metrics": {
    "cost": 0.3256399929523468,
    "electrochemical_conversion": 0.046843547374010086,
    "electrochemical_selectivity": 0.5385043621063232,
    "energy_efficiency": 0.06154502183198929,
    "faradaic_efficiency": 0.08039701730012894,
    "ohmic_efficiency": 0.9432819485664368,
    "pH_normalized": 0.285247802734375,
    "precipitation_signal": 0.0,
    "safety_risk": 0.11333958804607391,
    "score": 0.19628813862800598,
    "selective_product_yield": 0.02702149748802185,
    "transport_efficiency": 0.08379737287759781
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
      "solvent": 3,
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
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
    "cost": 0.32045599818229675,
    "electrochemical_conversion": 0.04384973645210266,
    "electrochemical_selectivity": 0.5249779224395752,
    "energy_efficiency": 0.19737501442432404,
    "faradaic_efficiency": 0.26995760202407837,
    "ohmic_efficiency": 0.9991381168365479,
    "pH_normalized": 0.28355032205581665,
    "precipitation_signal": 0.00031451715040020645,
    "safety_risk": 0.11333958804607391,
    "score": 0.0644112229347229,
    "selective_product_yield": 0.005093044135719538,
    "transport_efficiency": 0.26346224546432495
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
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 3,
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
    "cost": 0.31786400079727173,
    "electrochemical_conversion": 0.010313562117516994,
    "electrochemical_selectivity": 0.5213106870651245,
    "energy_efficiency": 0.23341329395771027,
    "faradaic_efficiency": 0.25325247645378113,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.2855640947818756,
    "precipitation_signal": 0.008188718929886818,
    "safety_risk": 0.11333958804607391,
    "score": 0.25915035605430603,
    "selective_product_yield": 0.02370574325323105,
    "transport_efficiency": 0.2740837335586548
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
      "solvent": 3,
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": -0.8
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
    "cost": 0.3181520104408264,
    "electrochemical_conversion": 0.04461824148893356,
    "electrochemical_selectivity": 0.5994594097137451,
    "energy_efficiency": 0.41145703196525574,
    "faradaic_efficiency": 0.32258662581443787,
    "ohmic_efficiency": 0.962709903717041,
    "pH_normalized": 0.28324997425079346,
    "precipitation_signal": 0.0,
    "safety_risk": 0.11333958804607391,
    "score": 0.224317729473114,
    "selective_product_yield": 0.014538628980517387,
    "transport_efficiency": 0.32393622398376465
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
      "solvent": 3,
      "volume_L": 0.05
    },
    {
      "current_mA": 50,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": -0.8
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
    "cost": 0.31757599115371704,
    "electrochemical_conversion": 0.028006823733448982,
    "electrochemical_selectivity": 0.5704413056373596,
    "energy_efficiency": 0.406950443983078,
    "faradaic_efficiency": 0.31427326798439026,
    "ohmic_efficiency": 0.9894182085990906,
    "pH_normalized": 0.28423500061035156,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.11333958804607391,
    "score": 0.15107154846191406,
    "selective_product_yield": 0.010023719631135464,
    "transport_efficiency": 0.3214532136917114
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
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": -0.8
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
    "cost": 0.3181520104408264,
    "electrochemical_conversion": 0.012840207666158676,
    "electrochemical_selectivity": 0.5630999803543091,
    "energy_efficiency": 0.3882621228694916,
    "faradaic_efficiency": 0.2794463336467743,
    "ohmic_efficiency": 0.989536702632904,
    "pH_normalized": 0.28475531935691833,
    "precipitation_signal": 0.0,
    "safety_risk": 0.11333958804607391,
    "score": 0.29516151547431946,
    "selective_product_yield": 0.0280318520963192,
    "transport_efficiency": 0.3006712794303894
  }
}
```

## K1 封存报告

## Mechanistic account

I interpret this benchmark as a polarity-dependent electrochemical conversion in which applied potential establishes whether the target pathway is accessible, while delivered charge, electrolyte/solvent transport, and parasitic current determine conversion and the various efficiency channels. The identities S0–S3 and E0–E3 are anonymous, so this is a phenomenological mechanism rather than a claim about real molecular identities.

All completed batches used 0.020 mol limiting reagent in 0.050 L solvent. The recommended tested procedure was batch 12: solvent-S3, electrolyte-E3, −0.8 V, a 100 mA current cap, and 3600 s electrolysis.

### 1. Productive polarity and potential

The clearest mechanistic result is that the productive electrode reaction requires negative potential. Batches 1 and 2 were a direct sign comparison in S0/E0 at 100 mA and 600 s:

- Batch 1, +1.2 V: conversion 0.0080, selectivity 0.0103, selective-product yield 0, faradaic efficiency 0.0245, transport efficiency 0, energy efficiency 0.0053, and score 0.
- Batch 2, −1.2 V: selectivity 0.5989, selective-product yield 0.0123, faradaic efficiency 0.3594, transport efficiency 0.3856, energy efficiency 0.1713, and score 0.1715. Its conversion estimate was clipped at zero, despite other channels indicating some productive chemistry.

Thus the positive-potential result is not merely a modest kinetic loss: almost every productive channel collapsed. My leading interpretation is a cathodic target transformation. Positive potential either leaves the limiting reagent unreacted or drives an unproductive oxidative process.

Potential magnitude does not appear to obey a simple “more negative is better” rule. In S0/E0, changing from −1.2 V for 600 s in batch 2 to −1.5 V for 3600 s in batch 3 did not improve the outcome: batch 3 scored only 0.0646, with conversion 0.0237, selectivity 0.5371, yield 0.0053, and energy efficiency 0.1144. Potential and time changed together, so this comparison cannot separately identify their effects, but it rejects a broadly monotonic strong-potential/long-time benefit.

The most informative S3/E3 comparison was between −1.2 and −0.8 V. At 100 mA and 3600 s:

- Batch 6 at −1.2 V had conversion 0.0266, selectivity 0.5347, energy efficiency 0.1967, faradaic efficiency 0.2860, transport efficiency 0.2613, and score 0.2584.
- Batch 10 at −0.8 V had conversion 0.0446, selectivity 0.5995, energy efficiency 0.4115, faradaic efficiency 0.3226, transport efficiency 0.3239, and score 0.2243.
- The batch-12 replicate at −0.8 V had conversion 0.0128, selectivity 0.5631, energy efficiency 0.3883, faradaic efficiency 0.2794, transport efficiency 0.3007, and score 0.2952.

Although conversion and selective-yield estimates varied substantially between batches 10 and 12, both −0.8 V runs showed much higher energy efficiency than batch 6 and retained similar or better selectivity and charge/transport efficiencies. I therefore infer that −0.8 V is nearer the balanced operating window: it supplies enough cathodic overpotential for the target reaction without the extra electrical work or parasitic reactions associated with −1.2 to −1.5 V. The exact optimum is not identifiable because potentials between −0.8 and −1.2 V, and milder negative potentials, were not tested.

A plausible potential dependence is

`i_target = i0,target × f(η)`

with target current increasing once a cathodic threshold is crossed, while a competing current grows more steeply at large negative overpotential. Then

`faradaic efficiency ≈ i_target / (i_target + i_side)`

and

`energy efficiency ≈ useful chemical energy / integral(|V i| dt)`.

This form explains why sufficient negative bias is essential, yet a stronger negative bias need not maximize the balanced score.

### 2. Current cap, charge delivery, and transport

The configured current appears to behave as a cap rather than a guaranteed constant current. A useful conceptual model is

`i_delivered(t) = min(i_cap, i_kinetic(V,state), i_transport(solvent,electrolyte,state))`,

`Q = integral i_delivered(t) dt`,

`conversion ≈ 1 − exp(−k_Q Q / n0)`

before degradation or depletion becomes important. Product formation would then be approximately conversion times chemical selectivity, with additional process and measurement variability.

The comparison of batches 6 and 7 strongly shows that simply raising the cap is undesirable. Both used S3/E3, −1.2 V, and 3600 s:

- At 100 mA, batch 6 gave conversion 0.0266, yield 0.0233, faradaic efficiency 0.2860, transport efficiency 0.2613, energy efficiency 0.1967, and score 0.2584.
- At 500 mA, batch 7 gave higher conversion (0.0468) and yield (0.0270), but faradaic efficiency fell to 0.0804, transport efficiency to 0.0838, energy efficiency to 0.0615, and score to 0.1963.

This pattern is consistent with severe polarization, ohmic loss, or side-current dominance at the high cap. The conversion gain was small relative to the fivefold cap increase, suggesting that kinetic or mass-transfer limitations prevent useful utilization of the additional nominal current.

At −0.8 V, batches 10 and 11 compared 100 and 50 mA at 3600 s. Batch 11 at 50 mA had conversion 0.0280, selectivity 0.5704, faradaic efficiency 0.3143, transport efficiency 0.3215, energy efficiency 0.4070, and score 0.1511. Its energy and transport metrics were similar to the 100 mA runs, but its conversion and measured yield were lower than batch 10. This suggests that 50 mA can constrain productive charge throughput, whereas 500 mA produces inefficient excess current. The best tested cap is therefore 100 mA, although the optimum could lie anywhere between 50 and 100 mA because that interval was not sampled.

Ohmic efficiency remained unusually high in all conditions—generally about 0.94–1.00—even when faradaic and transport efficiency deteriorated. For example, batch 7 retained an ohmic efficiency of 0.9433 while its faradaic and transport efficiencies fell below 0.09. Thus I do not think simple series resistance alone explains the current-cap penalty. Interfacial polarization, transport to the electrode, and parasitic electrochemistry are more plausible dominant losses.

### 3. Solvent/electrolyte medium and precipitation

Batches 3–6 screened same-index solvent/electrolyte pairs at 100 mA and 3600 s. Batch 3 used −1.5 V, whereas batches 4–6 used −1.2 V, so S0/E0 is not a perfectly controlled member of the material comparison. The results were:

- Batch 3, S0/E0: score 0.0646; precipitation signal 0.9868.
- Batch 4, S1/E1: score 0.2216; precipitation 0.7143.
- Batch 5, S2/E2: score 0.2236; precipitation 0.
- Batch 6, S3/E3: score 0.2584; precipitation 0.0024.

S3/E3 was the best tested pair and was carried forward. My interpretation is that the medium affects at least three coupled properties: solubility/phase behavior, ionic transport, and electrode interfacial kinetics. Strong precipitation in S0/E0 and S1/E1 could remove reagent or product from the electrochemically active liquid phase, foul an electrode, or distort transport. The near-zero precipitation signals of S2/E2 and S3/E3 accompanied better scores, although the dataset does not establish precipitation as the cause.

The normalized pH also depended strongly on the paired medium: representative final values were about 0.23 for S0/E0, 0.203 for S1/E1, 0.172 for S2/E2, and 0.283–0.286 for S3/E3. Because solvent and electrolyte were always changed together in this screen, I cannot attribute these changes to either component, nor can I determine whether pH is causal, a consequence of formulation, or only correlated with the favorable medium.

A phenomenological coupling could be written as

`k_transport = g(solvent, electrolyte, precipitation, concentration)`,

`i_transport ∝ k_transport × available dissolved reactant`,

where precipitation reduces the available dissolved fraction or electrode area. However, cross-combinations such as S3/E0 or S2/E3 were not tested. Consequently, the evidence supports the S3/E3 pair only; it does not show that S3 and E3 are independently optimal or that their effects are additive.

### 4. Time dependence and competing processes

At S3/E3, −1.2 V, and 100 mA, duration was explored at 1800, 3600, and 7200 s:

- Batch 9, 1800 s: conversion 0.0103, selectivity 0.5213, yield 0.0237, energy efficiency 0.2334, score 0.2592.
- Batch 6, 3600 s: conversion 0.0266, selectivity 0.5347, yield 0.0233, energy efficiency 0.1967, score 0.2584.
- Batch 8, 7200 s: conversion 0.0438, selectivity 0.5250, yield 0.0051, energy efficiency 0.1974, score 0.0644.

Conversion generally increased with time, as expected from accumulated charge. The very poor 7200 s score, despite its higher conversion, indicates that conversion alone is not the objective. A long run may permit product degradation, depletion of the readily accessible reagent, electrode passivation, or increasing diversion of current to side reactions. The approximately unchanged selectivity and efficiency channels make the exact cause ambiguous, and the especially low yield estimate may also contain substantial measurement/process noise.

A useful extended model is

`dR/dt = −r_target − r_side,R`,

`dP/dt = r_target − k_deg(V,medium) P`,

with passivation or transport deterioration represented by a declining active-area or mass-transfer term. This naturally creates an interior duration optimum: early time is charge-limited, while late time adds less target product and may destroy or divert it. The 1800 and 3600 s batches were practically indistinguishable by observed score, so the data do not resolve the optimum within that interval. I retained 3600 s because it was the duration replicated at the preferred −0.8 V condition, not because the data prove it superior to 1800 s.

### 5. Score behavior and measurement variability

The public balanced-efficiency score is a weighted combination of conversion, selectivity, selective-product yield, faradaic efficiency, transport efficiency, ohmic efficiency, and energy efficiency. It also applies a multiplicative selective-yield gate at 0.02. Operationally, the reported results are consistent with

`score = weighted_component_sum × min(selective_product_yield / 0.02, 1)`.

This gate explains why small changes in the selective-yield channel caused large score changes. Batch 10 had excellent conversion, selectivity, and energy efficiency but yield 0.0145, so its weighted result was penalized to 0.2243. Batch 12 used the same procedure and had a lower measured conversion but yield 0.0280, above the gate, producing the campaign-high score of 0.2952.

The final-assay selective-yield noise standard was publicly declared as 0.01. This is large relative to yields in the 0.005–0.028 range. Conversion also had a declared noise scale of 0.01. The divergent batch-10 and batch-12 conversion/yield estimates therefore should not be read as two different deterministic mechanisms. Their selectivity and efficiency profiles were much more consistent: selectivity 0.5995 versus 0.5631, energy efficiency 0.4115 versus 0.3883, faradaic efficiency 0.3226 versus 0.2794, and transport efficiency 0.3239 versus 0.3007. I interpret the replicated procedure as robustly occupying the best efficiency region, while its exact conversion and yield remain uncertain.

The selective-yield channel also did not always numerically equal measured conversion times measured selectivity. That can arise because the channels are independently calibrated/noisy synthetic observables or because “selective product yield” contains additional recovery/process factors. I therefore do not force exact algebraic identity among these three measured channels.

### 6. Safety and operating constraints

Observed safety risk remained well below the stated limit of 0.65 in every batch. It was about 0.059 for S0, 0.083 for S1, 0.101 for S2, and 0.113 for S3. The preferred S3 procedure therefore carries a somewhat higher observed risk than the other tested solvents, but its risk of 0.113 is still far from the constraint. In the tested domain, performance—not the safety ceiling—determined the recommendation. Extrapolation to stronger potentials, longer times, different concentrations, or larger scale would not be justified from these risk observations.

### 7. Overall proposed process

My best compact account is:

1. A negative potential activates a cathodic target pathway; positive potential is essentially nonproductive.
2. The delivered current is jointly limited by the current cap, electrode kinetics, and mass transport.
3. Productive conversion grows with integrated useful charge, but faradaic efficiency falls when excessive current or overpotential drives side reactions.
4. The solvent/electrolyte pair controls solubility, precipitation, interfacial kinetics, and transport. S3/E3 provides the best tested compromise and avoids the strong precipitation seen in S0/E0 and S1/E1.
5. Stronger potential, higher current, or longer time can raise conversion without raising balanced performance because energy consumption, parasitic current, transport limitation, or product loss becomes dominant.
6. The score’s yield gate amplifies assay variability near a selective yield of 0.02, so replicated multichannel behavior is more mechanistically informative than the rank order of isolated scores.

Within the sampled space, this leads to an interior operating region near S3/E3, −0.8 V, 100 mA, and 1800–3600 s. The sealed recommendation uses 3600 s because that exact procedure was replicated in batches 10 and 12, and batch 12 achieved the highest observed score.

### 8. Scope, unidentified factors, and alternatives

This account is limited to 0.020 mol reagent in 0.050 L solvent and to the sparse potential/current/time grid that was tested. Concentration and volume effects were never varied. Solvent and electrolyte effects are confounded because only matched pairs were screened. Potential and duration were also confounded in the S0 comparisons. No direct current–time trace, electrode potential loss, temperature trajectory, species-resolved concentration, or degradation measurement was available.

Plausible alternatives remain:

- The apparent S3/E3 advantage could be dominated entirely by S3 or entirely by E3 rather than by a pairwise interaction.
- Low precipitation may be a benign marker of the favorable formulation rather than the causal reason for better transport.
- The 500 mA penalty could arise mainly from a benchmark-specific current-utilization law rather than a physical mass-transfer limit.
- The long-time decline could be product degradation, electrode passivation, reagent depletion, or primarily noisy selective-yield measurement; the existing channels do not distinguish these explanations.
- The true best potential could lie between −0.8 and −1.2 V, or slightly milder than −0.8 V. The current optimum could lie between 50 and 100 mA.

Accordingly, the strongest claims are the productive negative polarity, the failure of the 500 mA strategy, the superiority of the tested S3/E3 pair, and the favorable replicated efficiency profile at −0.8 V and 100 mA. Detailed molecular identities and a unique microscopic mechanism are not identifiable from the public evidence.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific prior, nominal material dossier, or supplied mechanistic law was provided. The only supplied structure was the public workflow, instrument, and scoring contracts. All chemical/process hypotheses were therefore self-developed from the campaign.

Supported claims:
- Productive polarity is negative. The direct comparison between batch 1 (+1.2 V) and batch 2 (−1.2 V), both S0/E0, 100 mA, and 600 s, changed the interpretation decisively. Batch 1 had zero yield and score, whereas batch 2 showed selectivity 0.599, measurable yield, useful faradaic/transport efficiency, and score 0.171.
- More aggressive operation does not monotonically improve balanced performance. Batch 3 (S0/E0, −1.5 V, 3600 s) scored only 0.065, contradicting any simple expectation that stronger potential plus longer duration must help relative to batch 2.
- The tested medium matters. Among the same-index formulation screen, batch 6 using S3/E3 scored 0.258, above batches 3–5. Batches 5 and 6 also had negligible precipitation compared with batches 3 and 4. This supports a formulation effect, but not attribution to a particular component.
- A 500 mA cap is detrimental to balanced efficiency in the tested S3/E3 system. Relative to batch 6 at 100 mA, batch 7 at 500 mA raised conversion modestly but collapsed faradaic, transport, and energy efficiencies and reduced the score to 0.196.
- Very long electrolysis is disfavored under the tested −1.2 V S3/E3 conditions. Batch 8 at 7200 s had greater conversion but a score of only 0.064, whereas batches 9 and 6 at 1800 and 3600 s scored about 0.259 and 0.258.
- The −0.8 V region offers a better energy/selectivity compromise than −1.2 V. Batches 10 and 12 at −0.8 V both had energy efficiencies near 0.39–0.41, much higher than batch 6 at −1.2 V. Batch 12 produced the campaign-high score of 0.295.

Contradicted or narrowed claims:
- The initial conjecture that greater duration would first improve performance was narrowed substantially. Conversion tended to rise, but batch 8 showed that this did not translate into yield or score at 7200 s.
- The idea that the current was merely a harmless cap above the delivered-current regime was contradicted in its strong form. Batch 7 showed a conversion response to 500 mA, but with severe efficiency penalties. The cap affected the state even if useful current did not scale proportionally.
- A simple deterministic identity `selective yield = measured conversion × measured selectivity` was not supported by the final-assay channels. Batches 10 and 12 used the same procedure yet had markedly different conversion and yield estimates. Independent channel noise or an additional recovery/process factor is required.

Untested or unresolved claims:
- Whether S3, E3, or their interaction caused the batch-6 advantage remains untested because only matched pairs were screened.
- The suggestion that precipitation causes poor performance remains unresolved; it may merely correlate with formulation identity.
- Product degradation, electrode passivation, and reagent depletion are plausible explanations for batch 8, but no measurement distinguished them.
- The precise potential optimum, the optimum between 50 and 100 mA, and the distinction between 1800 and 3600 s remain unresolved.
- Batch 11 supported 100 mA over 50 mA at −0.8 V, but one comparison cannot establish a smooth current-response law.

The evidence that most changed my judgment was, sequentially, the batch-1/2 polarity reversal, batch 3's failure under stronger/longer conditions, the paired-medium ranking in batches 4–6, the high-current efficiency collapse in batch 7, the long-duration failure in batch 8, and the combination of improved efficiency but large assay variability in batches 10 and 12.

2. One additional discriminating experiment

I would run one cross-combination batch at the campaign loading: 0.020 mol reagent in 0.050 L solvent-S0, electrolyte-E3, −0.8 V, 100 mA, and 3600 s, with the same UV–vis and final-assay workflow.

This would distinguish the leading explanation—that solvent-controlled phase behavior/precipitation is an important part of the S3/E3 advantage—from the alternative that electrolyte-E3 alone largely controls the favorable electrochemical efficiencies.

- If S0/E3 showed strong precipitation and S0-like low performance despite E3, I would increase confidence that solvent/phase behavior is causally important.
- If it retained S3/E3-like selectivity, faradaic, transport, and energy efficiencies even with substantial precipitation, I would favor electrolyte identity as the main driver and reinterpret precipitation as a correlated marker rather than a cause.
- If it gave intermediate or internally mixed results—for example, good faradaic efficiency but poor transport or yield—I would favor a solvent–electrolyte interaction rather than a single-component explanation.
- A result differing only in selective yield would be weak evidence because that channel was noisy and controls the nonlinear score gate. I would base the judgment primarily on the joint efficiency profile and precipitation signal.

One experiment would not fully identify both main effects and their interaction, but this cross-combination is more discriminating than another matched-pair replicate.

3. Unused evidence, reliability, and goal effects

Evidence not fully used included the raw UV–vis traces and spectral structure; interpretation relied mainly on processed estimates. The intermediate UV–vis measurements were used qualitatively but were not fitted jointly with final assays. Final-assay pH values were noted, but no dedicated pH-meter experiments were performed. Cost was not modeled beyond recognizing that it contributed to the operating context. Safety observations were used only to verify that all batches remained far below the 0.65 limit. No concentration, volume, or reagent-loading series was collected, and no cross-combination separated solvent from electrolyte effects.

The least reliable blind predictions are Q05, Q07, and Q09 because they use solvent/electrolyte combinations absent from the campaign. Q03–Q12 also change both concentration and charge exposure relative to the core data, and most use 7200 s, where only one campaign batch existed and its yield was anomalously poor. Q11 is especially uncertain because it combines long duration, reduced reagent amount, changed concentration, and the poorly performing 500 mA regime. Exact score predictions are less reliable than polarity or efficiency-direction predictions because the 0.02 selective-yield gate greatly amplifies assay and process variation. The near-zero positive-potential predictions are directionally more secure, although their exact small values remain uncertain.

The recommendation is most reliable at the level of negative polarity, moderate current, and the tested S3/E3 pair. It is less reliable as a claim that −0.8 V is the exact optimum, that 3600 s is superior to 1800 s, or that S3 and E3 are independently optimal.

The assigned goal did affect evidence collection. Maximizing the public balanced score encouraged exploitation after batch 6: later work concentrated on S3/E3, moderate current, and the favorable negative-potential region. That choice produced a replicated recommendation in batches 10 and 12, but it displaced mechanistically cleaner cross-combinations, concentration studies, dedicated pH measurements, and replicated duration controls. Thus there was a real but ordinary tension between score optimization and mechanism identification; no evidence indicates a stronger hidden conflict.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.61,
        "lower80": 0.48,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.42,
        "lower80": 0.3,
        "upper80": 0.54
      },
      "faradaic_efficiency": {
        "estimate": 0.36,
        "lower80": 0.25,
        "upper80": 0.47
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.144,
        "lower80": 0.03,
        "upper80": 0.27
      },
      "selective_product_yield": {
        "estimate": 0.009,
        "lower80": 0.0,
        "upper80": 0.025
      },
      "transport_efficiency": {
        "estimate": 0.39,
        "lower80": 0.27,
        "upper80": 0.5
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "energy_efficiency": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "faradaic_efficiency": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "selective_product_yield": {
        "estimate": 0.0015,
        "lower80": 0.0,
        "upper80": 0.012
      },
      "transport_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.04
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.57,
        "lower80": 0.43,
        "upper80": 0.69
      },
      "energy_efficiency": {
        "estimate": 0.38,
        "lower80": 0.25,
        "upper80": 0.5
      },
      "faradaic_efficiency": {
        "estimate": 0.31,
        "lower80": 0.2,
        "upper80": 0.42
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.303,
        "lower80": 0.05,
        "upper80": 0.39
      },
      "selective_product_yield": {
        "estimate": 0.02,
        "lower80": 0.003,
        "upper80": 0.04
      },
      "transport_efficiency": {
        "estimate": 0.33,
        "lower80": 0.2,
        "upper80": 0.45
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.12
      },
      "energy_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "faradaic_efficiency": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.009,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.05
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.57,
        "lower80": 0.4,
        "upper80": 0.7
      },
      "energy_efficiency": {
        "estimate": 0.39,
        "lower80": 0.24,
        "upper80": 0.53
      },
      "faradaic_efficiency": {
        "estimate": 0.34,
        "lower80": 0.2,
        "upper80": 0.47
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.308,
        "lower80": 0.04,
        "upper80": 0.41
      },
      "selective_product_yield": {
        "estimate": 0.022,
        "lower80": 0.002,
        "upper80": 0.045
      },
      "transport_efficiency": {
        "estimate": 0.32,
        "lower80": 0.18,
        "upper80": 0.45
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.14
      },
      "energy_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "faradaic_efficiency": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.009,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.016
      },
      "transport_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.06
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.4,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.39,
        "lower80": 0.23,
        "upper80": 0.54
      },
      "faradaic_efficiency": {
        "estimate": 0.3,
        "lower80": 0.17,
        "upper80": 0.43
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.302,
        "lower80": 0.04,
        "upper80": 0.41
      },
      "selective_product_yield": {
        "estimate": 0.022,
        "lower80": 0.002,
        "upper80": 0.046
      },
      "transport_efficiency": {
        "estimate": 0.29,
        "lower80": 0.15,
        "upper80": 0.43
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.14
      },
      "energy_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "faradaic_efficiency": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.009,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.016
      },
      "transport_efficiency": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.06
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.38,
        "upper80": 0.69
      },
      "energy_efficiency": {
        "estimate": 0.39,
        "lower80": 0.23,
        "upper80": 0.54
      },
      "faradaic_efficiency": {
        "estimate": 0.32,
        "lower80": 0.18,
        "upper80": 0.46
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.307,
        "lower80": 0.07,
        "upper80": 0.42
      },
      "selective_product_yield": {
        "estimate": 0.028,
        "lower80": 0.005,
        "upper80": 0.055
      },
      "transport_efficiency": {
        "estimate": 0.35,
        "lower80": 0.2,
        "upper80": 0.5
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.14
      },
      "energy_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "faradaic_efficiency": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.009,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.016
      },
      "transport_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.06
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.54,
        "lower80": 0.38,
        "upper80": 0.68
      },
      "energy_efficiency": {
        "estimate": 0.11,
        "lower80": 0.03,
        "upper80": 0.22
      },
      "faradaic_efficiency": {
        "estimate": 0.09,
        "lower80": 0.02,
        "upper80": 0.19
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.21,
        "lower80": 0.08,
        "upper80": 0.32
      },
      "selective_product_yield": {
        "estimate": 0.025,
        "lower80": 0.004,
        "upper80": 0.055
      },
      "transport_efficiency": {
        "estimate": 0.09,
        "lower80": 0.02,
        "upper80": 0.2
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.12
      },
      "energy_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "faradaic_efficiency": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.016
      },
      "transport_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.05
      }
    }
  ],
  "rationale": "The direct polarity comparison made positive potential essentially nonproductive, so all +0.8 V predictions remain near zero. Negative-potential estimates extrapolate from the observed −0.8 to −1.5 V results, with longer electrolysis increasing charge exposure but also allowing overprocessing. E0 is assigned relatively strong transport, while cross-combinations receive wide intervals because solvent and electrolyte effects were confounded during the campaign. The 500 mA case reflects the observed collapse of faradaic, transport, and energy efficiencies at high current. Intervals also account for the new concentration, untested material combinations, process variation, assay noise, and the score's highly nonlinear 0.02 selective-yield gate."
}
```
