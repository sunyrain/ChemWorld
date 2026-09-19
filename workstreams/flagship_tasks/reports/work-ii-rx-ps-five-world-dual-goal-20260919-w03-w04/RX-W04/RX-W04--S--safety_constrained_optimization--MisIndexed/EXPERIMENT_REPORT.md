# RX-W04--S--safety_constrained_optimization--MisIndexed

## Run summary

- World: `RX-W04`
- Locus: `S`
- Goal: `safety_constrained_optimization`
- Arm: `MisIndexed`
- Status: `retained_nonconforming`
- Source status: `completed`
- Experimental sessions: `12/12`
- Operations: `84`
- Exact replay verified: `True`
- Rollbacks: `[]`
- Posttest chain sealed: `False`

### Recovery status

No recovery override was required for this task.

## Sealed recommendation

- Selected batch: `8`
- Rationale: Batch 8 achieved the highest observed safe score (0.3363) while remaining comfortably below the 0.35 safety limit (risk 0.1642), using water, Catalyst B, and a 370 K target for 5400 s.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S0 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.2467 | 0.6249 | 0.4105 | 0.1418 | 0.0019 | 0.1099 | 0.1465 |
| 2 | S1 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 370 K x 5400 s @ 700 rpm | no | 0.5142 | 0.5868 | 0.8707 | 0.3761 | 0.1398 | 0.1838 | 0.2567 |
| 3 | S2 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 370 K x 5400 s @ 700 rpm | no | 0.4778 | 0.5300 | 0.9109 | 0.4475 | 0.1142 | 0.1994 | 0.2250 |
| 4 | S3 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 370 K x 5400 s @ 700 rpm | no | 0.5863 | 0.6275 | 0.9367 | 0.3563 | 0.1530 | 0.2220 | 0.2852 |
| 5 | S3 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 370 K x 5400 s @ 700 rpm | no | 0.4614 | 0.5202 | 0.9111 | 0.4503 | 0.2007 | 0.2156 | 0.2087 |
| 6 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 370 K x 5400 s @ 700 rpm | no | 0.6499 | 0.6701 | 0.9787 | 0.3437 | 0.1969 | 0.2304 | 0.3217 |
| 7 | S3 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 370 K x 5400 s @ 700 rpm | no | 0.5223 | 0.5594 | 0.9168 | 0.4021 | 0.0862 | 0.2134 | 0.2444 |
| 8 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 370 K x 5400 s @ 700 rpm | no | 0.6042 | 0.7443 | 0.8246 | 0.2220 | 0.0743 | 0.1642 | 0.3363 |
| 9 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 370 K x 5400 s @ 700 rpm | no | 0.5766 | 0.6036 | 0.9706 | 0.3960 | 0.2462 | 0.2158 | 0.2815 |
| 10 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 10800 s @ 700 rpm | no | 0.5849 | 0.6417 | 0.9040 | 0.3227 | 0.1706 | 0.1559 | 0.3146 |
| 11 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 390 K x 3600 s @ 700 rpm | no | 0.6048 | 0.7619 | 0.7773 | 0.1991 | 0.0539 | 0.2007 | 0.3198 |
| 12 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 380 K x 4500 s @ 700 rpm | no | 0.6105 | 0.7365 | 0.8183 | 0.1923 | 0.0785 | 0.1785 | 0.3298 |

## Complete experimental actions and observations

### Batch 1

Lifecycle index: `1`; end step: `7`.

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 350
    },
    {
      "instrument": "hplc",
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
  "end_step": 7,
  "lifecycle_index": 1,
  "metrics": {
    "byproduct_signal": 0.14176885783672333,
    "conversion": 0.41045308113098145,
    "cost": 1.0,
    "degradation_warning": 0.001886937185190618,
    "safety_risk": 0.10985220968723297,
    "score": 0.14651484787464142,
    "selectivity": 0.6249381899833679,
    "virtual_spectrum_summary": 0.07882198691368103,
    "yield": 0.24667121469974518
  },
  "ordinal": 1
}
```

### Batch 2

Lifecycle index: `2`; end step: `14`.

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 5400,
      "operation": "heat",
      "stirring_speed_rpm": 700,
      "target_temperature_K": 370
    },
    {
      "instrument": "hplc",
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
  "end_step": 14,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.3761070966720581,
    "conversion": 0.8707416653633118,
    "cost": 1.0,
    "degradation_warning": 0.13982491195201874,
    "safety_risk": 0.1838381141424179,
    "score": 0.256721556186676,
    "selectivity": 0.5868324637413025,
    "virtual_spectrum_summary": 0.26978009939193726,
    "yield": 0.5141660571098328
  },
  "ordinal": 2
}
```

### Batch 3

Lifecycle index: `3`; end step: `21`.

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 2,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 5400,
      "operation": "heat",
      "stirring_speed_rpm": 700,
      "target_temperature_K": 370
    },
    {
      "instrument": "hplc",
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
  "end_step": 21,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.4475304186344147,
    "conversion": 0.9109452962875366,
    "cost": 1.0,
    "degradation_warning": 0.11416847258806229,
    "safety_risk": 0.1993904709815979,
    "score": 0.22500158846378326,
    "selectivity": 0.5299820303916931,
    "virtual_spectrum_summary": 0.2975175380706787,
    "yield": 0.47784313559532166
  },
  "ordinal": 3
}
```

### Batch 4

Lifecycle index: `4`; end step: `28`.

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 3,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 5400,
      "operation": "heat",
      "stirring_speed_rpm": 700,
      "target_temperature_K": 370
    },
    {
      "instrument": "hplc",
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
  "end_step": 28,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.3562796115875244,
    "conversion": 0.936747133731842,
    "cost": 1.0,
    "degradation_warning": 0.15297864377498627,
    "safety_risk": 0.22197754681110382,
    "score": 0.2851646840572357,
    "selectivity": 0.62746262550354,
    "virtual_spectrum_summary": 0.26479417085647583,
    "yield": 0.5862854719161987
  },
  "ordinal": 4
}
```

### Batch 5

Lifecycle index: `5`; end step: `35`.

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 3,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 5400,
      "operation": "heat",
      "stirring_speed_rpm": 700,
      "target_temperature_K": 370
    },
    {
      "instrument": "hplc",
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
  "end_step": 35,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.45025599002838135,
    "conversion": 0.9110689163208008,
    "cost": 1.0,
    "degradation_warning": 0.20070023834705353,
    "safety_risk": 0.215620219707489,
    "score": 0.20870915055274963,
    "selectivity": 0.5202307105064392,
    "virtual_spectrum_summary": 0.33795589208602905,
    "yield": 0.4614342153072357
  },
  "ordinal": 5
}
```

### Batch 6

Lifecycle index: `6`; end step: `42`.

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 3,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 5400,
      "operation": "heat",
      "stirring_speed_rpm": 700,
      "target_temperature_K": 370
    },
    {
      "instrument": "hplc",
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
  "end_step": 42,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.343736469745636,
    "conversion": 0.9787471294403076,
    "cost": 1.0,
    "degradation_warning": 0.19690796732902527,
    "safety_risk": 0.23037084937095642,
    "score": 0.32169145345687866,
    "selectivity": 0.6701257824897766,
    "virtual_spectrum_summary": 0.2776636481285095,
    "yield": 0.6498804688453674
  },
  "ordinal": 6
}
```

### Batch 7

Lifecycle index: `7`; end step: `49`.

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 3,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 2,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 5400,
      "operation": "heat",
      "stirring_speed_rpm": 700,
      "target_temperature_K": 370
    },
    {
      "instrument": "hplc",
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
  "end_step": 49,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.4020989239215851,
    "conversion": 0.916832447052002,
    "cost": 1.0,
    "degradation_warning": 0.0861738845705986,
    "safety_risk": 0.21342134475708008,
    "score": 0.2444198727607727,
    "selectivity": 0.5594461560249329,
    "virtual_spectrum_summary": 0.25993266701698303,
    "yield": 0.5222867131233215
  },
  "ordinal": 7
}
```

### Batch 8

Lifecycle index: `8`; end step: `56`.

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 5400,
      "operation": "heat",
      "stirring_speed_rpm": 700,
      "target_temperature_K": 370
    },
    {
      "instrument": "hplc",
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
  "end_step": 56,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.22203974425792694,
    "conversion": 0.8246043920516968,
    "cost": 1.0,
    "degradation_warning": 0.07434025406837463,
    "safety_risk": 0.1641862839460373,
    "score": 0.33630505204200745,
    "selectivity": 0.7442734837532043,
    "virtual_spectrum_summary": 0.1555749624967575,
    "yield": 0.604150116443634
  },
  "ordinal": 8
}
```

### Batch 9

Lifecycle index: `9`; end step: `63`.

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 5400,
      "operation": "heat",
      "stirring_speed_rpm": 700,
      "target_temperature_K": 370
    },
    {
      "instrument": "hplc",
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
  "end_step": 63,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.39602428674697876,
    "conversion": 0.9706289172172546,
    "cost": 1.0,
    "degradation_warning": 0.2461666315793991,
    "safety_risk": 0.2157830148935318,
    "score": 0.2815049886703491,
    "selectivity": 0.6036185026168823,
    "virtual_spectrum_summary": 0.3285883367061615,
    "yield": 0.5765995979309082
  },
  "ordinal": 9
}
```

### Batch 10

Lifecycle index: `10`; end step: `70`.

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 10800,
      "operation": "heat",
      "stirring_speed_rpm": 700,
      "target_temperature_K": 350
    },
    {
      "instrument": "hplc",
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
  "end_step": 70,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.322689026594162,
    "conversion": 0.9040166139602661,
    "cost": 1.0,
    "degradation_warning": 0.1706053614616394,
    "safety_risk": 0.15594539046287537,
    "score": 0.31462234258651733,
    "selectivity": 0.6417489647865295,
    "virtual_spectrum_summary": 0.2542513608932495,
    "yield": 0.5848972201347351
  },
  "ordinal": 10
}
```

### Batch 11

Lifecycle index: `11`; end step: `77`.

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 700,
      "target_temperature_K": 390
    },
    {
      "instrument": "hplc",
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
  "end_step": 77,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.19907481968402863,
    "conversion": 0.7773239612579346,
    "cost": 1.0,
    "degradation_warning": 0.05390297248959541,
    "safety_risk": 0.2007054090499878,
    "score": 0.31981074810028076,
    "selectivity": 0.761889636516571,
    "virtual_spectrum_summary": 0.13374748826026917,
    "yield": 0.6048083901405334
  },
  "ordinal": 11
}
```

### Batch 12

Lifecycle index: `12`; end step: `84`.

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 4500,
      "operation": "heat",
      "stirring_speed_rpm": 700,
      "target_temperature_K": 380
    },
    {
      "instrument": "hplc",
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
  "end_step": 84,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.19225937128067017,
    "conversion": 0.8182674050331116,
    "cost": 1.0,
    "degradation_warning": 0.07850893586874008,
    "safety_risk": 0.17845170199871063,
    "score": 0.329833060503006,
    "selectivity": 0.7365045547485352,
    "virtual_spectrum_summary": 0.14107167720794678,
    "yield": 0.6104586124420166
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

No valid K1 payload was produced.

Retained failure: `provider_failure`. The missing report is not inferred or reconstructed.

## Q — Blind predictions

### Overall rationale

These predictions extrapolate from the campaign's controlled Catalyst B/acetonitrile result (batch 9: conversion 0.9706, yield 0.5766, selectivity 0.6036, byproduct signal 0.3960, risk 0.2158, score 0.2815 at 370 K for 5400 s) and from the water/Catalyst B thermal series in batches 8, 10, 11, and 12. I treated effective conversion exposure as increasing with catalyst loading, time, and an Arrhenius-like temperature factor, while selectivity declines under prolonged or extreme exposure because parallel byproduct formation, degradation, and possibly reverse cycling become important. Yield was centered near conversion multiplied by selectivity. Score was estimated as a safety-penalized function of yield and selectivity, consistent with the campaign observation that chemically similar hotter batches scored less well when risk increased. Risk was modeled as solvent- and temperature-sensitive, with weaker duration and catalyst-loading effects. Intervals are deliberately broad because the queries use smaller absolute charges, different catalyst ratios, 400 rpm stirring, temperatures up to 465 K, and combinations not directly studied. In particular, the 465 K cases are major extrapolations, and the mechanistic data cannot uniquely distinguish parallel byproduct formation from serial product degradation or a reversible target pathway.

### Q01

Low Catalyst B loading and only 1800 s should limit conversion despite 410 K. The short exposure should preserve comparatively good selectivity, but this is an extrapolation above the temperatures directly studied.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2800 | 0.1600 | 0.4200 |
| conversion | 0.6000 | 0.4200 | 0.7700 |
| safety_risk | 0.2600 | 0.1900 | 0.3400 |
| score | 0.2100 | 0.1200 | 0.2900 |
| selectivity | 0.7200 | 0.6000 | 0.8200 |
| yield | 0.4300 | 0.2700 | 0.5700 |

### Q02

The eightfold longer exposure should drive near-complete conversion even at low catalyst loading, while allowing substantial parallel byproduct formation, product loss, or reverse-channel cycling. Risk is predicted near the declared limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5800 | 0.4000 | 0.7500 |
| conversion | 0.9600 | 0.8600 | 1.0000 |
| safety_risk | 0.3500 | 0.2700 | 0.4600 |
| score | 0.1300 | 0.0400 | 0.2300 |
| selectivity | 0.4200 | 0.2500 | 0.5900 |
| yield | 0.4000 | 0.2200 | 0.5600 |

### Q03

The high catalyst loading should compensate for the short residence time and give high conversion. Relative to Q01, faster desired and undesired channels are both expected, producing higher yield but lower selectivity.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4300 | 0.2900 | 0.5800 |
| conversion | 0.9400 | 0.8200 | 1.0000 |
| safety_risk | 0.3000 | 0.2200 | 0.4000 |
| score | 0.2200 | 0.1200 | 0.3100 |
| selectivity | 0.5700 | 0.4200 | 0.7000 |
| yield | 0.5400 | 0.3900 | 0.6600 |

### Q04

High catalyst loading, 410 K, and 14400 s represent severe cumulative exposure. Conversion should saturate, but secondary byproduct and degradation pathways are expected to dominate; safety risk probably exceeds the limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7500 | 0.5700 | 0.9000 |
| conversion | 0.9900 | 0.9300 | 1.0000 |
| safety_risk | 0.4100 | 0.3100 | 0.5500 |
| score | 0.0600 | 0.0100 | 0.1500 |
| selectivity | 0.2500 | 0.1000 | 0.4300 |
| yield | 0.2500 | 0.0900 | 0.4200 |

### Q05

At 350 K, the low catalyst concentration should make conversion kinetically limited even over 7200 s. Lower thermal stress should preserve selectivity and keep risk comfortably below the limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2700 | 0.1500 | 0.4100 |
| conversion | 0.5800 | 0.3900 | 0.7600 |
| safety_risk | 0.1800 | 0.1300 | 0.2500 |
| score | 0.2300 | 0.1300 | 0.3200 |
| selectivity | 0.7300 | 0.6000 | 0.8300 |
| yield | 0.4200 | 0.2600 | 0.5700 |

### Q06

The long 465 K treatment is far outside the observed temperature range. Arrhenius acceleration should overcome the low catalyst loading, but severe secondary chemistry and a clear safety-limit violation are likely.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8200 | 0.6200 | 0.9600 |
| conversion | 0.9900 | 0.9100 | 1.0000 |
| safety_risk | 0.5600 | 0.4200 | 0.7200 |
| score | 0.0300 | 0.0000 | 0.1000 |
| selectivity | 0.1800 | 0.0400 | 0.3800 |
| yield | 0.1800 | 0.0400 | 0.3700 |

### Q07

High Catalyst B loading should give high conversion at 350 K without the extreme thermal penalty of the hotter cases. This is predicted to be among the better queries, though acetonitrile was inferior to water in the campaign.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3800 | 0.2400 | 0.5300 |
| conversion | 0.9400 | 0.8200 | 1.0000 |
| safety_risk | 0.2100 | 0.1500 | 0.2900 |
| score | 0.2800 | 0.1800 | 0.3700 |
| selectivity | 0.6200 | 0.4700 | 0.7400 |
| yield | 0.5800 | 0.4300 | 0.7000 |

### Q08

This combines the highest catalyst loading with 465 K for 7200 s. Conversion should be complete, but extensive degradation or diversion to byproduct is expected, with the largest safety risk in the set.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9000 | 0.7200 | 1.0000 |
| conversion | 0.9900 | 0.9400 | 1.0000 |
| safety_risk | 0.6800 | 0.5100 | 0.8500 |
| score | 0.0100 | 0.0000 | 0.0500 |
| selectivity | 0.1000 | 0.0100 | 0.2800 |
| yield | 0.0900 | 0.0100 | 0.2700 |

### Q09

Mid catalyst loading at 410 K for 7200 s should nearly exhaust reactant. The exposure is substantially harsher than the directly observed acetonitrile batch, so selectivity and score are expected to fall while risk approaches the limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6200 | 0.4500 | 0.7800 |
| conversion | 0.9800 | 0.9000 | 1.0000 |
| safety_risk | 0.3500 | 0.2700 | 0.4700 |
| score | 0.1200 | 0.0400 | 0.2200 |
| selectivity | 0.3800 | 0.2200 | 0.5500 |
| yield | 0.3700 | 0.2100 | 0.5300 |

### Q10

Quenching occurs only after the full heated residence, so it cannot undo chemistry or accumulated thermal risk. I predict only a small possible benefit from promptly arresting post-heat secondary reactions; the interval substantially overlaps Q09.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6000 | 0.4300 | 0.7700 |
| conversion | 0.9800 | 0.9000 | 1.0000 |
| safety_risk | 0.3500 | 0.2700 | 0.4700 |
| score | 0.1300 | 0.0400 | 0.2300 |
| selectivity | 0.4000 | 0.2300 | 0.5700 |
| yield | 0.3900 | 0.2200 | 0.5500 |

### Q11

The long 350 K treatment should achieve high conversion at the midpoint catalyst loading. Campaign batch 10 showed that long low-temperature exposure can still erode selectivity, so the predicted result is good but below the best short-to-moderate treatments.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4400 | 0.2900 | 0.6000 |
| conversion | 0.9500 | 0.8400 | 1.0000 |
| safety_risk | 0.2000 | 0.1400 | 0.2800 |
| score | 0.2500 | 0.1500 | 0.3400 |
| selectivity | 0.5600 | 0.4000 | 0.7000 |
| yield | 0.5300 | 0.3700 | 0.6600 |

### Q12

At 465 K, even 1800 s should provide substantial effective kinetic exposure at the midpoint catalyst loading. The short duration limits damage relative to Q06 and Q08, but both selectivity loss and safety-limit exceedance remain plausible.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5800 | 0.4000 | 0.7600 |
| conversion | 0.9700 | 0.8400 | 1.0000 |
| safety_risk | 0.4300 | 0.3200 | 0.5800 |
| score | 0.1200 | 0.0300 | 0.2300 |
| selectivity | 0.4200 | 0.2400 | 0.6000 |
| yield | 0.4100 | 0.2300 | 0.5800 |

## K2 — Retrospective analysis

1. Assessment of the initial claims

The only substantive mechanistic claim in the initial information was that “the target pathway may have an appreciable reverse channel,” with moderate confidence. The campaign did not directly test that claim. K1 therefore treated reversibility as one plausible element of a working network rather than as an established result.

Some observations were compatible with reversibility, particularly the failure of longer exposure to produce a monotonic improvement. For example, under water/Catalyst B, batch 8 at 370 K for 5400 s gave conversion 0.8246, selectivity 0.7443, and yield 0.6042, whereas batch 10 at 350 K for 10800 s gave higher conversion, 0.9040, but lower selectivity, 0.6417, and slightly lower yield, 0.5849. However, that pattern is equally consistent with parallel byproduct formation or sequential degradation. It is not affirmative evidence for a reverse reaction.

There was no direct observation of product returning to reactant, no perturbation starting from product-rich material, and no sufficiently resolved time course showing conversion decreasing after a maximum. Thus, the proper retrospective classification is “still untested,” not “supported.” There was also no decisive counterevidence: conversions as high as 0.9787 in batch 6 and 0.9706 in batch 9 do not exclude a reverse channel because the equilibrium could lie strongly toward product or irreversible sinks could mask reversal. I did not encounter clear counterevidence and then fail to revise the claim; rather, the experiments never became diagnostic enough to settle it.

The material packet also stated that catalyst and solvent behavior belonged to anonymous categorical benchmark profiles and that real solvent names should not be interpreted as real-chemistry predictions. The strong catalyst and solvent differences support the existence of categorical effects in this world. They do not identify their physical origin or validate real-world chemical analogies. No task-specific property dossier was supplied, so there were no further substantive property claims to test.

2. Experiments that formed or changed the interpretation

Batch 1 supplied the first baseline: water/Catalyst A at 350 K for 3600 s produced final conversion 0.4105, selectivity 0.6249, yield 0.2467, risk 0.1099, and score 0.1465. It established that moderate heating was safe but that this particular recipe was kinetically or catalytically weak.

Batches 2–4 broadened the observed response range, but they simultaneously changed solvent and catalyst. Their higher conversions and scores showed that substantial improvement was possible, yet they could not identify whether catalyst or solvent caused it. Batch 4, using toluene/Catalyst D at 370 K for 5400 s, reached score 0.2852 and motivated a more controlled catalyst comparison.

Batches 5–7 were the first genuinely diagnostic block because solvent, temperature, time, loading, and stirring were held fixed while catalyst identity changed. In toluene at 370 K for 5400 s, Catalyst B in batch 6 clearly outperformed A, C, and D: batch 6 gave yield 0.6499, selectivity 0.6701, and score 0.3217, compared with scores 0.2087, 0.2444, and 0.2852 in batches 5, 7, and 4. This changed the working view from an undifferentiated categorical catalyst effect to a specific conclusion that Catalyst B was the most promising catalyst under the tested conditions.

Batches 8 and 9 completed a partially controlled solvent comparison around Catalyst B. Batch 8 was especially influential. Water/Catalyst B at 370 K for 5400 s gave conversion 0.8246, selectivity 0.7443, byproduct signal 0.2220, yield 0.6042, risk 0.1642, and score 0.3363. Relative to batch 6 in toluene, it sacrificed conversion and a little yield but sharply improved selectivity, byproduct burden, and risk. Batch 9 showed that acetonitrile/Catalyst B could reach conversion 0.9706 but had selectivity only 0.6036, degradation warning 0.2462, risk 0.2158, and score 0.2815. These results formed K1’s view that solvent affected both kinetic partitioning and safety rather than merely changing overall rate.

Batches 10–12 modified the simplest “more heat or more time is better” interpretation. Under water/Catalyst B, batch 10’s long low-temperature treatment increased conversion but worsened selectivity and degradation relative to batch 8. Batch 11 at 390 K for 3600 s gave yield 0.6048 and selectivity 0.7619 but a higher risk of 0.2007, leaving its score at 0.3198. Batch 12 at 380 K for 4500 s reached the highest observed yield in this local series, 0.6105, but its score of 0.3298 remained below batch 8. These outcomes supported K1’s interpretation that the score reflects a coupled chemical/safety optimum rather than a conversion maximum.

Several choices were not evidence-led at the time they were made. The initial 350 K/3600 s condition was a cautious guess. Batches 2–4 used a confounded catalyst–solvent screen chosen for breadth rather than identifiability. Full reagent, solvent, and catalyst charges were used consistently largely because twelve equal full-charge batches exactly matched the campaign stocks and because higher loading seemed likely to improve conversion; catalyst order and concentration effects had not been established. The selection of 370 K/5400 s and later thermal adjustments was guided by accumulated observations, but the precise values were still heuristic rather than derived from a fitted kinetic model.

3. Principal competing mechanisms and explanations

K1 proposed a minimal network resembling R → P, R → B, P → R, and P → D, with rate constants affected by catalyst, solvent, and temperature. That remains useful as a bookkeeping model, but several alternatives fit the endpoint data:

• Parallel competition: reactant independently forms target product and byproduct. Lower selectivity after long exposure could simply reflect continuing R → B.

• Sequential loss: target product forms first and is later converted to byproduct or degradation products. This would explain why additional exposure can raise conversion without raising surviving target yield.

• Reversible target formation plus irreversible sinks: R ⇌ P accompanied by R → B or P → D. This is the interpretation most closely related to the initial prior, but it was not uniquely selected by the data.

• Catalyst deactivation or state change: apparent time dependence could arise because Catalyst B loses activity or changes selectivity during heating rather than because P is reversible or unstable.

• Solvent-dependent analytical or partition effects: differences in final signals could partly reflect how the public assay maps the virtual state to signals, although the synthetic calibration and the consistency between HPLC and final-assay trends make a wholly analytical explanation less likely.

• Thermal-state and transport effects: target temperature is a setpoint, not necessarily the instantaneous liquid temperature. Stirring was almost fixed, so heat transfer or mass-transfer limitations cannot be separated from intrinsic kinetics.

The controlled toluene block distinguishes catalyst identity effects under one condition, and the Catalyst B solvent block distinguishes broad solvent effects. The thermal series establishes non-monotonic score behavior. The campaign cannot distinguish parallel byproduct formation from serial product degradation or reversibility, cannot estimate reaction orders, and cannot determine whether solvent effects operate through desired rate, undesired rate, equilibrium, thermal risk, or several of these simultaneously.

4. The single additional complete experiment I would choose

I would run the batch 8 recipe again—0.080 L water, 0.040 mol reagent, and 0.005 mol Catalyst B at 370 K and 700 rpm—but as a same-vessel time-course experiment. I would heat for 5400 s, take one quantitative HPLC measurement, continue heating for a further 5400 s at the same setpoint, then terminate and perform the final assay. This keeps the chemistry at the best-supported operating point while introducing the time contrast that the original campaign lacked.

The interpretations would be:

• If conversion falls between 5400 and 10800 s while reactant signal rises, that would be the clearest available support for an appreciable reverse channel.

• If conversion remains constant or rises while target yield falls and byproduct or degradation signal rises, sequential product loss or parallel sink chemistry would become more credible than reversal.

• If conversion, selectivity, and yield remain nearly stationary, the 5400 s state is probably close to a stable equilibrium or kinetic plateau, and the poorer long-exposure results elsewhere would more likely be temperature-, solvent-, or batch-specific.

• If both conversion and target yield continue increasing, K1 overstated the importance of secondary loss near the recommended condition, and the apparent optimum may instead have been produced mainly by the score’s safety penalty.

• If the repeated 5400 s observation differs materially from batch 8 before the second heating period, process variability would become a leading explanation and would weaken most fine mechanistic comparisons.

This would still not perfectly separate reversal from every deactivation model, but it would be more diagnostic than another isolated endpoint.

5. Tradeoff between identifiability and score optimization

The research goal explicitly prioritized a high safe score, so the campaign progressively concentrated resources around promising conditions. That was beneficial operationally but costly mechanistically. After batch 6 identified Catalyst B, four of the last six experiments used water/Catalyst B to refine the thermal operating region. This helped find and validate a useful local region, but it left catalyst loading, reagent concentration, solvent volume, and stirring essentially unvaried.

The early batches 2–4 favored exploration efficiency over clean causal identification by changing catalyst and solvent together. Conversely, batches 5–7 sacrificed expected score to compare inferior catalysts under matched conditions; this was a deliberate identifiability investment. Batch 9 similarly tested acetonitrile/Catalyst B even though water had already looked promising, improving the solvent comparison at the cost of a likely lower score.

Batches 10–12 shifted back toward optimization. They mapped nearby time–temperature alternatives, but not in a balanced factorial design, so separate time and temperature effects remain difficult to estimate. The decision to use one intermediate HPLC measurement in every batch provided useful confirmation of endpoint trends, yet those measurements were generally placed only after the single heating operation. A smaller number of deliberately staged time-course experiments would have been more informative mechanistically.

Thus, there were sacrifices in both directions: batches 5, 7, and 9 improved identification but were unlikely to win; the concentration of later experiments around water/Catalyst B improved the chance of a strong recommendation but narrowed the mechanism that could be inferred.

6. Underused evidence and weaknesses in the blind predictions

The intermediate HPLC observations were underused. I mainly used their processed conversion, yield, selectivity, and byproduct estimates as qualitative checks. I did not formally combine intermediate and final measurements with their stated noise levels, model the systematic differences between instruments, or use the raw peak shapes and areas quantitatively. The raw multichannel final-assay artifacts, actual thermal approach to setpoint, operation-level risk increments, and assay uncertainty fields also were not incorporated into a fitted model.

The discrepancy between intermediate and final estimates could have helped quantify observation and short-delay variability. For example, batch 11’s intermediate HPLC estimated conversion 0.7981, selectivity 0.7830, and yield 0.5915, while its final assay estimated 0.7773, 0.7619, and 0.6048. Treating such differences only descriptively understated the uncertainty in later predictions. No replicate experiment was available to separate instrument noise from batch variability.

The least reliable blind predictions are Q06, Q08, and Q12 because they extrapolate to 465 K, far above the campaign maximum of 390 K. Q08 is particularly weak because it combines 465 K, 7200 s, and the highest catalyst loading. Its narrow conversion interval of 0.94–1.00 assumed that extreme exposure necessarily means nearly complete conversion; catalyst deactivation, altered equilibrium, thermal loss, or other unobserved behavior could invalidate that assumption. Its risk interval may also be too narrow because the campaign never approached that thermal regime.

Q02 and Q04 are also weak because 14400 s at 410 K lies well beyond the studied joint time–temperature domain. Q01 and Q05 depend strongly on a catalyst-loading response that was never measured; their conversion intervals may be too narrow at the low loading. Q03, Q04, Q07, and Q08 likewise extrapolate above the tested catalyst loading relative to substrate. Q10 is uncertain for a different reason: no campaign batch used a quench, so the prediction that it would closely resemble Q09 was a mechanistic guess rather than a learned effect.

K1 explicitly limited its interpretation to the fixed-load, mostly 350–390 K campaign region and acknowledged that reaction order, transport, and the identity of secondary pathways were unidentifiable. The qualitative cautions in the blind-prediction rationale were consistent with that scope. However, some numerical intervals—especially conversion at 465 K and the near-equivalence assigned to Q09 and Q10—were sharper than K1’s admitted uncertainty justified. The point estimates also relied on an Arrhenius-like exposure concept that had not been fitted from a sufficiently orthogonal data set.

7. Limitations of the sealed recommendation

Batch 8 was the sample-best completed experiment, not a proven optimum. Its score of 0.3363 was only modestly above batch 12 at 0.3298 and batch 6 at 0.3217. Given final-assay noise, process variability, and the absence of replicates, the true ranking of nearby conditions is uncertain. The recommendation was justified because batch 8 combined the highest observed score with risk 0.1642, comfortably below the 0.35 limit, but it should not be described as globally or even locally optimal.

Repeatability should first be tested through independent exact replicates of batch 8, including the same addition order, 370 K target, 5400 s duration, and 700 rpm stirring. Replicate distributions should be reported for score, risk, conversion, selectivity, yield, byproduct signal, and degradation warning rather than only their means.

Local robustness should then be examined with a small response-surface design around the recommendation: approximately 360–380 K, 4000–6500 s, modest Catalyst B loading changes, and small changes in reagent concentration and stirring. The purpose would be to identify whether batch 8 lies on a broad safe plateau or at a narrow, variability-sensitive peak. Conditions should be evaluated against the safety limit using upper uncertainty bounds, not merely point risks.

Cross-material scope is especially limited. Catalyst B is an anonymous benchmark formulation, and the solvent effects are categorical runtime effects rather than validated real-solvent mechanistic predictions. The recommendation therefore cannot be transferred to a named catalyst, an empirical synthesis, another substrate, or another solvent system without new evidence. Cross-world generalization would require repeating the catalyst and solvent comparisons under independently initialized worlds or seeds and verifying that the ranking is stable.

In short, the sealed recommendation means: “batch 8 was the best observed member of this twelve-batch campaign under the public score and safety contract.” It does not mean that its parameters have been proven optimal, that its superiority is statistically reproducible, or that its mechanism and performance generalize beyond the tested synthetic world.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | no | 1 | 45.4 | provider_failure | 2 |
| Q | yes | 0 | 136.3 | none | 0 |
| K2 | yes | 0 | 133.6 | none | 0 |

## Retained incomplete-chain notice

This cell is not counted as a complete K1/Q/K2 chain. Its twelve source experiments, recommendation, and any valid posttest payloads are preserved, but the missing stage must be repaired in the frozen order before the cell can enter the effective denominator. No missing text has been synthesized for this export.

## Scope note

This report contains only information available before truth release. Reference truth, prediction scoring, and recommendation retests are intentionally absent because the full 60-task block has not yet completed.
