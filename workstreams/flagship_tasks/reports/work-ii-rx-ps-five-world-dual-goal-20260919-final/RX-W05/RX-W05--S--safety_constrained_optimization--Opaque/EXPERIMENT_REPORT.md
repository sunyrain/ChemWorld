# RX-W05--S--safety_constrained_optimization--Opaque

## Run summary

- World: `RX-W05`
- Locus: `S`
- Goal: `safety_constrained_optimization`
- Arm: `Opaque`
- Status: `completed`
- Source status: `completed`
- Experimental sessions: `12/12`
- Operations: `84`
- Exact replay verified: `True`
- Rollbacks: `[]`
- Posttest chain sealed: `True`

### Recovery status

- Effective result location: `source-repair-v11`
- Recovery version: `recovery-v11-parallel4-transport-repair`
- Repaired stages: `source`
- Source experiments rerun: `False`
- Original source thread reused: `False`
- Truth revealed during recovery: `False`

## Sealed recommendation

- Selected batch: `12`
- Rationale: Highest observed final safe-score (0.3615) while remaining comfortably below the 0.35 safety-risk limit (0.2255); it balanced high conversion and yield against degradation better than hotter or longer runs.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S2 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.4615 | 0.7681 | 0.5840 | 0.1330 | 0.0309 | 0.1722 | 0.2576 |
| 2 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.5408 | 0.7906 | 0.7224 | 0.1591 | 0.0674 | 0.1835 | 0.3036 |
| 3 | S2 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.3379 | 0.6590 | 0.5026 | 0.1907 | 0.0404 | 0.1609 | 0.1778 |
| 4 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.6055 | 0.7957 | 0.7582 | 0.1699 | 0.0877 | 0.1913 | 0.3309 |
| 5 | S0 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.5374 | 0.8438 | 0.6237 | 0.0996 | 0.0425 | 0.1385 | 0.3260 |
| 6 | S1 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.5200 | 0.7932 | 0.6591 | 0.1415 | 0.0745 | 0.1629 | 0.2989 |
| 7 | S3 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.4517 | 0.6834 | 0.6707 | 0.2013 | 0.1040 | 0.1891 | 0.2335 |
| 8 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 375 K x 3600 s @ 600 rpm | no | 0.6869 | 0.7757 | 0.8828 | 0.2012 | 0.1344 | 0.2189 | 0.3584 |
| 9 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 400 K x 3600 s @ 600 rpm | no | 0.7201 | 0.7427 | 0.9483 | 0.2370 | 0.1895 | 0.2790 | 0.3430 |
| 10 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 375 K x 7200 s @ 600 rpm | no | 0.5872 | 0.6094 | 0.9883 | 0.3901 | 0.3276 | 0.2231 | 0.2857 |
| 11 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 382 K x 3000 s @ 600 rpm | no | 0.6861 | 0.7964 | 0.8572 | 0.1831 | 0.1207 | 0.2272 | 0.3570 |
| 12 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 380 K x 3300 s @ 600 rpm | no | 0.6973 | 0.7819 | 0.8858 | 0.1929 | 0.1241 | 0.2255 | 0.3615 |

## Complete experimental actions and observations

### Batch 1

Lifecycle index: `1`; end step: `7`.

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
    "byproduct_signal": 0.13297206163406372,
    "conversion": 0.5840432643890381,
    "cost": 1.0,
    "degradation_warning": 0.030880233272910118,
    "safety_risk": 0.1721860021352768,
    "score": 0.2575576603412628,
    "selectivity": 0.7681353092193604,
    "virtual_spectrum_summary": 0.08703073859214783,
    "yield": 0.46150800585746765
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
  "end_step": 14,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.15910035371780396,
    "conversion": 0.722449004650116,
    "cost": 1.0,
    "degradation_warning": 0.06738866865634918,
    "safety_risk": 0.18354207277297974,
    "score": 0.30363577604293823,
    "selectivity": 0.7906439900398254,
    "virtual_spectrum_summary": 0.11783009767532349,
    "yield": 0.5408095717430115
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
  "end_step": 21,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.1906598061323166,
    "conversion": 0.5026132464408875,
    "cost": 1.0,
    "degradation_warning": 0.04044961556792259,
    "safety_risk": 0.16085678339004517,
    "score": 0.17780452966690063,
    "selectivity": 0.6590409874916077,
    "virtual_spectrum_summary": 0.12306522578001022,
    "yield": 0.33792126178741455
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
      "solvent": 2,
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
  "end_step": 28,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.16992710530757904,
    "conversion": 0.7581726908683777,
    "cost": 1.0,
    "degradation_warning": 0.08769377321004868,
    "safety_risk": 0.19127100706100464,
    "score": 0.33087483048439026,
    "selectivity": 0.7957031726837158,
    "virtual_spectrum_summary": 0.13292211294174194,
    "yield": 0.6055092811584473
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
      "solvent": 0,
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
  "end_step": 35,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.09964016079902649,
    "conversion": 0.6237221360206604,
    "cost": 1.0,
    "degradation_warning": 0.042510081082582474,
    "safety_risk": 0.13849443197250366,
    "score": 0.325959175825119,
    "selectivity": 0.8438096046447754,
    "virtual_spectrum_summary": 0.07393162697553635,
    "yield": 0.5373926162719727
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
      "solvent": 1,
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
  "end_step": 42,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.14152197539806366,
    "conversion": 0.6591309309005737,
    "cost": 1.0,
    "degradation_warning": 0.07454122602939606,
    "safety_risk": 0.16294914484024048,
    "score": 0.2988780736923218,
    "selectivity": 0.7932187914848328,
    "virtual_spectrum_summary": 0.11138064414262772,
    "yield": 0.5199685096740723
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
      "catalyst": 3,
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
  "end_step": 49,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.2012903094291687,
    "conversion": 0.6706622838973999,
    "cost": 1.0,
    "degradation_warning": 0.10404842346906662,
    "safety_risk": 0.1891244351863861,
    "score": 0.23346230387687683,
    "selectivity": 0.6833649277687073,
    "virtual_spectrum_summary": 0.1575314700603485,
    "yield": 0.4516521096229553
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
      "solvent": 2,
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
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 375
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
    "byproduct_signal": 0.20118069648742676,
    "conversion": 0.8827829360961914,
    "cost": 1.0,
    "degradation_warning": 0.13444256782531738,
    "safety_risk": 0.21894864737987518,
    "score": 0.35843461751937866,
    "selectivity": 0.7756767272949219,
    "virtual_spectrum_summary": 0.17114853858947754,
    "yield": 0.6869100332260132
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
      "catalyst": 3,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 400
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
    "byproduct_signal": 0.23700030148029327,
    "conversion": 0.9483168125152588,
    "cost": 1.0,
    "degradation_warning": 0.18945041298866272,
    "safety_risk": 0.27900266647338867,
    "score": 0.34299081563949585,
    "selectivity": 0.7426689267158508,
    "virtual_spectrum_summary": 0.215602844953537,
    "yield": 0.7201077342033386
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
      "solvent": 2,
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 375
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
    "byproduct_signal": 0.3900606036186218,
    "conversion": 0.9883244633674622,
    "cost": 1.0,
    "degradation_warning": 0.3275735378265381,
    "safety_risk": 0.223127081990242,
    "score": 0.2856684625148773,
    "selectivity": 0.609394907951355,
    "virtual_spectrum_summary": 0.3619414269924164,
    "yield": 0.587236225605011
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
      "solvent": 2,
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
      "duration_s": 3000,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 382
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
    "byproduct_signal": 0.1830597072839737,
    "conversion": 0.8572368621826172,
    "cost": 1.0,
    "degradation_warning": 0.1206747516989708,
    "safety_risk": 0.22721873223781586,
    "score": 0.35699662566185,
    "selectivity": 0.7963639497756958,
    "virtual_spectrum_summary": 0.15498647093772888,
    "yield": 0.6860759854316711
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
      "solvent": 2,
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
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 600,
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
    "byproduct_signal": 0.1929018199443817,
    "conversion": 0.8858361840248108,
    "cost": 1.0,
    "degradation_warning": 0.1240510493516922,
    "safety_risk": 0.22547218203544617,
    "score": 0.3615153133869171,
    "selectivity": 0.7818882465362549,
    "virtual_spectrum_summary": 0.16191896796226501,
    "yield": 0.6973053216934204
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

1. Scope and evidence base

This report concerns only the anonymous synthetic benchmark world that was experimentally observed. It does not identify a real catalyst, real reaction, or named synthesis. Catalyst labels A–D and the reagent/product roles should therefore be treated as latent benchmark categories. Although the solvents have real names, their effects here are calibrated categorical effects rather than transferable physical-property predictions.

All 12 completed batches used 0.040 mol limiting reagent, 0.005 mol catalyst, 0.080 L solvent, and 600 rpm stirring. Each batch received one HPLC measurement before termination and one final assay after termination. The factors changed were catalyst, solvent, temperature, and heating duration. No experiment varied reagent concentration, catalyst loading, solvent volume, or stirring speed, so their quantitative roles are not identifiable from this campaign.

The safety limit was 0.35. Every completed batch remained below it; observed terminal risks ranged from 0.1385 to 0.2790. Batch 12 was selected because it had the highest observed final score, 0.3615, at risk 0.2255.

2. Principal empirical observations

Catalyst screen in acetonitrile at a 350 K set point for 3600 s:

- Batch 1, Catalyst A: final conversion 0.5840, yield 0.4615, selectivity 0.7681, byproduct signal 0.1330, degradation warning 0.0309, score 0.2576, risk 0.1722.
- Batch 2, Catalyst B: conversion 0.7224, yield 0.5408, selectivity 0.7906, byproduct 0.1591, degradation 0.0674, score 0.3036, risk 0.1835.
- Batch 3, Catalyst C: conversion 0.5026, yield 0.3379, selectivity 0.6590, byproduct 0.1907, degradation 0.0404, score 0.1778, risk 0.1609.
- Batch 4, Catalyst D: conversion 0.7582, yield 0.6055, selectivity 0.7957, byproduct 0.1699, degradation 0.0877, score 0.3309, risk 0.1913.

Under that tested condition, Catalyst D gave the best overall productive performance, Catalyst B was second, Catalyst A was intermediate, and Catalyst C was least effective. Catalyst C was not merely slower: it also had the lowest selectivity and relatively high byproduct signal. Thus a single scalar “activity” parameter is probably insufficient to describe catalyst identity; catalyst choice appears to affect both productive and competing pathways.

Solvent screen with Catalyst D at 350 K for 3600 s:

- Batch 5, water: conversion 0.6237, yield 0.5374, selectivity 0.8438, byproduct 0.0996, degradation 0.0425, score 0.3260, risk 0.1385.
- Batch 6, ethanol: conversion 0.6591, yield 0.5200, selectivity 0.7932, byproduct 0.1415, degradation 0.0745, score 0.2989, risk 0.1629.
- Batch 4, acetonitrile: conversion 0.7582, yield 0.6055, selectivity 0.7957, byproduct 0.1699, degradation 0.0877, score 0.3309, risk 0.1913.
- Batch 7, toluene: conversion 0.6707, yield 0.4517, selectivity 0.6834, byproduct 0.2013, degradation 0.1040, score 0.2335, risk 0.1891.

Water favored selectivity, suppressed byproduct and degradation signals, and produced the lowest risk, but its conversion was lower than acetonitrile’s. Acetonitrile provided the best conversion and yield and a slightly higher score than water, despite worse byproduct, degradation, and risk values. Ethanol was intermediate. Toluene produced moderate conversion but the poorest selectivity and largest byproduct/degradation signals in this solvent comparison. The solvent effect therefore couples kinetics, pathway selectivity, degradation, and safety rather than acting only as a rate multiplier.

Temperature and time studies with Catalyst D in acetonitrile:

- Batch 4, 350 K for 3600 s: conversion 0.7582, yield 0.6055, selectivity 0.7957, degradation 0.0877, score 0.3309, risk 0.1913.
- Batch 8, 375 K for 3600 s: conversion 0.8828, yield 0.6869, selectivity 0.7757, byproduct 0.2012, degradation 0.1344, score 0.3584, risk 0.2189.
- Batch 9, 400 K for 3600 s: conversion 0.9483, yield 0.7201, selectivity 0.7427, byproduct 0.2370, degradation 0.1895, score 0.3430, risk 0.2790.
- Batch 10, 375 K for 7200 s: conversion 0.9883, yield 0.5872, selectivity 0.6094, byproduct 0.3901, degradation 0.3276, score 0.2857, risk 0.2231.
- Batch 11, 382 K for 3000 s: conversion 0.8572, yield 0.6861, selectivity 0.7964, byproduct 0.1831, degradation 0.1207, score 0.3570, risk 0.2272.
- Batch 12, 380 K for 3300 s: conversion 0.8858, yield 0.6973, selectivity 0.7819, byproduct 0.1929, degradation 0.1241, score 0.3615, risk 0.2255.

Increasing temperature from 350 to 375 K substantially raised conversion and yield, enough to improve the score despite modest selectivity loss and more degradation. Raising the set point to 400 K increased conversion and yield further, but selectivity and degradation worsened enough that the score fell. Extending the 375 K treatment from 3600 to 7200 s was clearly harmful: conversion approached completion, but yield and selectivity fell sharply while byproduct and degradation signals approximately doubled or more. This is strong evidence for sequential loss of desired product and/or increasingly important competing chemistry at high exposure.

The best region was broad rather than sharply resolved: batches 8, 11, and 12 scored 0.3584, 0.3570, and 0.3615, respectively. Their differences are comparable to the stated final-assay channel noise, so batch 12 is the best observed instance, not proof of a uniquely optimal point.

3. Proposed reaction-process model

A minimal explanatory network is:

R -> P       productive reaction
R -> B       primary competing reaction
P -> D       secondary degradation or conversion of desired product
B -> D or additional side products may also occur

Here R is the public reactant role, P the target-product role, B the byproduct role, and D the degradation role. A useful phenomenological model is:

 dR/dt = -(kP + kB) R
 dP/dt = kP R - kD P
 dB/dt = kB R + alpha*kD*P
 dD/dt = (1-alpha)*kD*P

The observed conversion primarily reflects depletion of R; yield reflects accumulated P; selectivity reflects partitioning toward P rather than B/D; byproduct and degradation channels report different portions of undesired material. Exact mass closure cannot be asserted because these are calibrated synthetic observables, and the final yield, conversion, and selectivity channels do not obey a demonstrated exact algebraic identity.

Each rate constant can be represented as a condition-dependent term:

 k_j = A_j * exp[-E_j/(R_gas*T)] * C_j(catalyst) * S_j(solvent) * f_j(concentration, mixing)

for j in {P, B, D}. Catalyst and solvent require pathway-specific modifiers rather than one common multiplier. For example, Catalyst D in acetonitrile increases the productive rate strongly, whereas water appears to reduce overall conversion but suppress undesired pathways even more. The worsening selectivity at higher temperature and long duration implies that the undesired pathways have different temperature/time dependence from productive formation—plausibly a larger apparent activation energy for degradation or simply progressive exposure of accumulated P to kD.

For constant conditions and negligible product degradation, conversion would approximately follow:

 X(t) = 1 - exp[-(kP+kB)t].

The batch 10 result shows why that simpler expression is insufficient for optimization: maximizing X did not maximize retained P. Once kD is appreciable, P rises and then can pass through a maximum. The optimum is therefore an exposure window, not complete conversion.

A practical pseudocode representation is:

 initialize R, P, B, D
 for each small time interval:
     calculate temperature-dependent kP, kB, kD
     modify each rate by catalyst and solvent category
     consume R through productive and competing branches
     form P from the productive branch
     degrade a fraction of accumulated P
 calculate noisy instrument channels from R, P, B, D
 calculate safety risk from formulation and thermal exposure
 calculate score from productive and adverse observables

4. Thermal dynamics and safety coupling

The reactor did not instantly reach its set point. Reported temperature increases during 3600 s heating were approximately 49.2 K at the 350 K set point, 70.9 K at 375 K, and 91.6 K at 400 K, consistent with finite thermal relaxation from an initial temperature near ambient. A simple model is:

 dT/dt = (T_set - T)/tau + q_rxn/(m*Cp),

although the campaign does not separate heater response from reaction heat. The nearly reproducible temperature rises at matched settings suggest that externally imposed heating dominated the terminal temperature response, but unobserved reaction heat cannot be ruled out.

Observed safety risk depended on formulation and heating. At identical 350 K/3600 s Catalyst D conditions, terminal risk changed from 0.1385 in water to 0.1629 in ethanol, 0.1913 in acetonitrile, and 0.1891 in toluene. In Catalyst D/acetonitrile batches, risk rose from 0.1913 at 350 K to 0.2189 at 375 K and 0.2790 at 400 K. Doubling duration at 375 K only raised risk from 0.2189 to 0.2231, much less than the chemical degradation increased. This suggests that the reported safety-risk function is dominated by categorical formulation terms and peak thermal severity, with a weaker duration term over the tested range.

One possible empirical form is:

 risk = r0(solvent,catalyst,loading,concentration) + rT(T_peak) + rt(time) + rint(condition interactions),

with rT convex at high temperature. This is an interpretation, not an identified equation. Risk was reported as a bounded public metric; no calorimetry, pressure, or direct hazard channel was measured.

5. Relationship between observables and score

The score generally increased with retained target yield and favorable selectivity, and decreased with byproduct, degradation, and perhaps safety risk. It was not simply yield or conversion. Batch 9 had the campaign’s highest final yield among the listed runs, 0.7201, but scored below batch 12 because it had lower selectivity and higher byproduct, degradation, and risk. Batch 10 nearly exhausted reactant but scored poorly because desired material was lost to secondary chemistry.

A generic representation consistent with the results is:

 score = F(yield, selectivity, conversion, byproduct, degradation, risk),

where F increases with yield/selectivity and decreases with adverse channels. I cannot identify the exact functional form from these observations, and I did not assume one when choosing the final recommendation.

6. Measurements that changed the interpretation

The initial batch, batch 1, established that moderate heating produced only partial conversion and moderate yield at low-to-moderate degradation. The catalyst screen then changed the interpretation from a purely temperature-controlled reaction to a catalyst-dependent branching problem: Catalyst D improved both conversion and target yield, while Catalyst C had poor selectivity as well as poor conversion.

The solvent screen added a second trade-off. Batch 5 showed that water strongly suppressed adverse channels and risk but also reduced conversion relative to acetonitrile. Batch 7 showed that similar conversion can coexist with much poorer target retention, proving that solvent cannot be modeled solely through total reaction rate.

Batch 8 showed that additional thermal activation was beneficial up to approximately the 375–380 K region. Batch 9 demonstrated the onset of a high-temperature penalty. Batch 10 was the clearest mechanistic discriminator: prolonged reaction increased conversion to 0.9883 while reducing yield to 0.5872 and selectivity to 0.6094. That observation strongly favors a sequential degradation/product-loss mechanism over a model in which undesired material is formed only in a fixed parallel branch from reactant.

Batches 11 and 12 refined the exposure window. Shorter, slightly hotter treatments retained high yield and selectivity, and batch 12 provided the best measured balance.

There were some differences between pre-termination HPLC and final assay values. For example, batch 12 HPLC reported conversion 0.8852, yield 0.7066, selectivity 0.8017, and byproduct 0.2033; the final assay reported 0.8858, 0.6973, 0.7819, and 0.1929. Batch 11 HPLC yield was 0.7171 versus final 0.6861. These differences could arise from instrument noise, channel-specific calibration, sampling, or minor evolution between measurements. Because termination itself reported no process-time increment and the final assay has declared noise, I do not treat these differences as firm evidence of post-termination chemistry.

7. Recommended operating interpretation

Within the studied domain, the most favorable observed regime was:

- 0.040 mol limiting reagent
- 0.005 mol Catalyst D
- 0.080 L acetonitrile
- 600 rpm
- 380 K set point
- 3300 s heating
- terminate, then final assay

This is batch 12, with final score 0.3615 and safety risk 0.2255. The terminal temperature rise during the batch was not retained in the final history output available to this report, so I do not invent that value. Based on neighboring batches, the regime belongs to the same approximately 375–382 K, 3000–3600 s exposure window.

The recommendation is empirical and local. Given assay noise, batches 8 and 11 are credible near-equivalent alternatives. Water with Catalyst D, as in batch 5, is an attractive lower-risk alternative when safety margin is prioritized over maximum observed score.

8. Applicability limits and unidentified factors

The proposed model is supported only for the tested batch scale, fixed reagent/catalyst/solvent amounts, 600 rpm, four solvent categories, four catalyst categories, set points from 350 to 400 K in the optimization series, and durations from 3000 to 7200 s. It should not be extrapolated confidently to different concentrations, catalyst loadings, volumes, mixing rates, reactor geometries, pressure regimes, or temperatures outside the tested interval.

Catalyst and solvent effects may interact. The solvent screen used only Catalyst D, so the solvent ranking cannot automatically be transferred to Catalysts A–C. Likewise, the temperature/time study used only Catalyst D in acetonitrile. A different catalyst might have a different optimum or degradation sensitivity.

Temperature was observed only through aggregate state changes, not a time-resolved temperature trace. Thus Arrhenius parameters, heat-transfer time constants, and any reaction exotherm cannot be separately identified. The campaign also did not measure concentrations over multiple time points within one batch, so individual kP, kB, and kD values cannot be uniquely fitted.

The public channels are proxies. “Byproduct signal” and “degradation warning” need not correspond to single chemical species. Several hidden species or pathways could map into each signal. The exact score function and risk function are also unidentified.

9. Reasonable competing explanations

A reversible reaction or equilibrium limitation could mimic some conversion-time behavior, although the pronounced loss of yield and selectivity with longer heating favors degradation over simple equilibrium alone.

Catalyst deactivation followed by noncatalytic side reaction could also explain why long exposure becomes unfavorable. The data do not distinguish product degradation from catalyst deactivation plus continuing side chemistry.

The apparent sequential loss of P might instead be a parallel pathway whose rate grows disproportionately with temperature or with a changing medium composition. Without time-resolved speciation, those models are observationally similar.

Solvent effects might arise from latent categorical calibration of solubility, phase behavior, catalyst state, or instrument response rather than molecular solvent properties. The benchmark explicitly warns against interpreting these effects as real-world solvent-property predictions.

Finally, small score differences among batches 8, 11, and 12 may be stochastic measurement variation rather than genuine mechanistic differences. The robust conclusion is a favorable intermediate thermal-exposure region with Catalyst D/acetonitrile—not an exactly determined optimum at 380 K and 3300 s.

## Q — Blind predictions

### Overall rationale

These blind predictions use the campaign's Catalyst B result at 350 K as the catalyst-specific anchor and the Catalyst D temperature/time series to estimate thermal scaling and sequential product loss. Conversion was treated approximately as saturating first-order exposure, while selectivity was reduced with cumulative catalyst–temperature–time exposure; yield was constrained to remain broadly consistent with conversion multiplied by selectivity. Safety risk was modeled as a formulation baseline plus a strongly temperature-dependent thermal component and a weaker duration component. The queries change catalyst-to-reagent ratio, concentration, stirring speed, and in several cases exceed the studied temperature or exposure range, so the 80% intervals include model-form uncertainty in addition to final-assay noise. Predictions near 465 K and predictions of extreme degradation are the least certain.

### Q01

The low Catalyst B loading and short treatment should limit conversion despite 410 K. Short exposure should preserve selectivity and restrain byproduct formation. The loading, concentration, and stirring rate are outside the directly studied combination, so the interval includes substantial kinetic uncertainty.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1500 | 0.0700 | 0.2900 |
| conversion | 0.3800 | 0.2200 | 0.5600 |
| safety_risk | 0.2500 | 0.1700 | 0.3400 |
| score | 0.1800 | 0.0900 | 0.2800 |
| selectivity | 0.8400 | 0.7200 | 0.9200 |
| yield | 0.3200 | 0.1900 | 0.4700 |

### Q02

The eightfold longer exposure than Q01 should drive nearly complete conversion even at low catalyst loading. Based on the severe time penalty observed in batch 10, accumulated product is expected to undergo substantial secondary loss, lowering selectivity and increasing byproduct signal.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4200 | 0.2500 | 0.6200 |
| conversion | 0.9700 | 0.9000 | 1.0000 |
| safety_risk | 0.2600 | 0.1800 | 0.3600 |
| score | 0.2700 | 0.1500 | 0.3800 |
| selectivity | 0.5800 | 0.3800 | 0.7400 |
| yield | 0.5600 | 0.3600 | 0.7200 |

### Q03

The high Catalyst B loading should give rapid productive conversion during the short 410 K treatment. Some high-temperature competing chemistry is expected, but the 1800 s duration should retain much more product than the long-exposure cases.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2400 | 0.1200 | 0.3900 |
| conversion | 0.8600 | 0.7200 | 0.9500 |
| safety_risk | 0.3000 | 0.2000 | 0.4100 |
| score | 0.3400 | 0.2200 | 0.4500 |
| selectivity | 0.7600 | 0.6200 | 0.8700 |
| yield | 0.6500 | 0.4700 | 0.7800 |

### Q04

High catalyst loading, 410 K, and 14400 s represent extreme cumulative exposure. Reactant conversion should saturate, but the sequential-product-loss interpretation predicts extensive conversion of target material into byproduct or degradation channels. This is a strong extrapolation beyond the longest high-loading condition studied.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8600 | 0.6700 | 0.9700 |
| conversion | 1.0000 | 0.9700 | 1.0000 |
| safety_risk | 0.3200 | 0.2200 | 0.4500 |
| score | 0.0400 | 0.0000 | 0.1300 |
| selectivity | 0.1200 | 0.0300 | 0.3000 |
| yield | 0.1200 | 0.0300 | 0.2900 |

### Q05

At 350 K, the low catalyst loading should make the 7200 s exposure kinetically moderate rather than extreme. Conversion is predicted to remain incomplete, while selectivity stays favorable and risk remains comfortably below the declared limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1500 | 0.0700 | 0.2800 |
| conversion | 0.5500 | 0.3900 | 0.7000 |
| safety_risk | 0.1800 | 0.1200 | 0.2500 |
| score | 0.2600 | 0.1600 | 0.3600 |
| selectivity | 0.8300 | 0.7200 | 0.9100 |
| yield | 0.4600 | 0.3200 | 0.6000 |

### Q06

Even with low catalyst loading, 465 K for 7200 s should nearly exhaust reactant and strongly activate secondary chemistry. The temperature is well above the campaign range, so both degradation and safety-risk extrapolations are uncertain; exceeding the 0.35 safety limit is more likely than not.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6400 | 0.4300 | 0.8200 |
| conversion | 0.9800 | 0.9100 | 1.0000 |
| safety_risk | 0.5200 | 0.3700 | 0.7000 |
| score | 0.1200 | 0.0300 | 0.2400 |
| selectivity | 0.3600 | 0.1800 | 0.5600 |
| yield | 0.3500 | 0.1700 | 0.5400 |

### Q07

High Catalyst B loading at 350 K should produce high conversion over 7200 s. The long exposure should cause appreciable secondary loss, but the lower temperature should preserve substantially more selectivity and yield than the corresponding 410 or 465 K treatments.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3600 | 0.2200 | 0.5200 |
| conversion | 0.9600 | 0.8900 | 0.9900 |
| safety_risk | 0.2100 | 0.1400 | 0.2900 |
| score | 0.3100 | 0.2000 | 0.4200 |
| selectivity | 0.6400 | 0.4900 | 0.7700 |
| yield | 0.6100 | 0.4600 | 0.7400 |

### Q08

This combines the highest catalyst loading, highest temperature, and a long duration. Conversion should be effectively complete, but the proposed sequential-loss network predicts near-total destruction or diversion of target product. A major safety-limit violation is expected, though the exact magnitude is poorly identified beyond the studied temperature range.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9400 | 0.8000 | 1.0000 |
| conversion | 1.0000 | 0.9900 | 1.0000 |
| safety_risk | 0.6800 | 0.5000 | 0.8500 |
| score | 0.0100 | 0.0000 | 0.0600 |
| selectivity | 0.0600 | 0.0000 | 0.1800 |
| yield | 0.0600 | 0.0000 | 0.1800 |

### Q09

The intermediate catalyst loading and 7200 s at 410 K should drive conversion to saturation. Relative to the favorable 3000–3600 s campaign window, the doubled duration and higher temperature should substantially reduce retained selectivity and yield while increasing byproduct formation.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5500 | 0.3800 | 0.7100 |
| conversion | 0.9900 | 0.9500 | 1.0000 |
| safety_risk | 0.2900 | 0.2000 | 0.4000 |
| score | 0.1900 | 0.0900 | 0.3000 |
| selectivity | 0.4500 | 0.2900 | 0.6100 |
| yield | 0.4400 | 0.2800 | 0.6000 |

### Q10

The chemistry before quenching is identical to Q09. Because quench occurs only after the full heat exposure, it cannot recover already degraded product; I therefore predict only a small improvement from suppressing any residual post-heating evolution and a modest reduction in terminal risk. The campaign did not directly quantify this quench effect.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5400 | 0.3700 | 0.7000 |
| conversion | 0.9900 | 0.9500 | 1.0000 |
| safety_risk | 0.2700 | 0.1800 | 0.3800 |
| score | 0.2000 | 0.1000 | 0.3100 |
| selectivity | 0.4600 | 0.3000 | 0.6200 |
| yield | 0.4500 | 0.2900 | 0.6100 |

### Q11

At 350 K the intermediate catalyst loading should eventually give nearly complete conversion over 14400 s. Long residence time is expected to erode selectivity, but lower temperature should make secondary loss less severe than in Q02, Q04, or Q09.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4400 | 0.2900 | 0.6000 |
| conversion | 0.9800 | 0.9200 | 1.0000 |
| safety_risk | 0.2000 | 0.1400 | 0.2800 |
| score | 0.2700 | 0.1600 | 0.3800 |
| selectivity | 0.5600 | 0.4000 | 0.7000 |
| yield | 0.5500 | 0.3900 | 0.6900 |

### Q12

The brief 465 K treatment should create high conversion without the cumulative destruction expected for Q06 or Q08, but high-temperature competing pathways should still lower selectivity. Safety risk is predicted to exceed the limit despite the short duration because campaign observations indicated a strong peak-temperature contribution.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4200 | 0.2500 | 0.6200 |
| conversion | 0.9400 | 0.8400 | 0.9900 |
| safety_risk | 0.5400 | 0.3800 | 0.7000 |
| score | 0.1800 | 0.0600 | 0.3000 |
| selectivity | 0.5800 | 0.3800 | 0.7400 |
| yield | 0.5400 | 0.3400 | 0.7000 |

## K2 — Retrospective analysis

1. Initial claims: supported, contradicted, or untested

The initial material packet contained almost no substantive mechanistic claim to test. It explicitly said that no task-specific property dossier was supplied, that the catalysts were anonymous benchmark formulations, and that the named solvents had categorical benchmark effects rather than physically transferable solvent-property correlations. Consequently, the campaign began without a proposed rate law, catalyst ranking, solvent ranking, activation energy, or reaction network.

The warning against assigning real chemical identities remains supported in the limited sense that nothing observed required or justified such an assignment. Strong categorical differences appeared among catalysts and solvents, but those differences do not validate any real-world chemical interpretation. Likewise, the observation that water gave lower risk and byproduct signal than acetonitrile is not evidence for a general physical-solvent rule; it is only evidence about this benchmark world.

The public safety limit of 0.35 and the instrument-observation contracts were operational specifications, not mechanistic hypotheses. All 12 completed experiments remained below the safety limit, so the campaign did not test behavior after a safety-limit violation. The declared assay noise and partial-observation structure were consistent with differences between HPLC and final-assay estimates, but I did not formally test their calibration.

No important initial mechanistic claim was directly refuted because essentially none was supplied. It is therefore important not to describe the absence of conflict as positive confirmation. Similarly, I did not encounter clear counterevidence to the packet’s statement that experimental evidence was authoritative and then ignore it. The more relevant issue is that I formed several new interpretations from sparse data and sometimes treated them more quantitatively than the design justified.

2. Experiments that formed or changed my judgments

Batch 1 was an intentionally conservative baseline rather than a condition selected from prior chemical knowledge. The choices of acetonitrile, Catalyst A, 350 K, and 3600 s were largely unvalidated guesses intended to produce an observable but safe response. Its final conversion of 0.5840 and score of 0.2576 established that the system reacted appreciably without approaching the safety limit.

Batches 2–4 genuinely changed the catalyst judgment. Under the same nominal solvent and thermal conditions, Catalyst D in batch 4 produced conversion 0.7582 and score 0.3309, compared with 0.7224 and 0.3036 for Catalyst B in batch 2, 0.5840 and 0.2576 for Catalyst A in batch 1, and 0.5026 and 0.1778 for Catalyst C in batch 3. This was the basis for carrying Catalyst D into later experiments. It also motivated the K1 judgment that catalyst identity affects pathway partitioning as well as total activity, because Catalyst C combined low conversion with poor selectivity rather than behaving merely as a uniformly slower version of Catalyst D.

Batches 5–7 formed the solvent interpretation. Batch 5 showed that water could retain high selectivity, 0.8438, with low byproduct signal, 0.0996, and risk, 0.1385, although conversion was only 0.6237. Batch 7 showed that toluene could give moderate conversion, 0.6707, while selectivity fell to 0.6834 and byproduct signal rose to 0.2013. These results changed the model from a simple solvent-dependent rate multiplier to pathway-specific solvent effects. Acetonitrile was retained for optimization because batch 4 had the best score in that comparison, not because the initial packet recommended it.

Batch 8 was the first strong optimization step: raising the set point from 350 to 375 K increased conversion and yield and raised the score from batch 4’s 0.3309 to 0.3584. Batch 9 then showed a downturn at 400 K: conversion and yield increased, but selectivity and degradation worsened and the score fell to 0.3430. That observation created the working belief in an intermediate thermal optimum.

Batch 10 most strongly changed the mechanistic interpretation. At 375 K for 7200 s, conversion reached 0.9883, while yield fell to 0.5872, selectivity to 0.6094, and byproduct and degradation signals rose to 0.3901 and 0.3276. This was the central evidence behind K1’s sequential product-loss model. It was more diagnostic than the small differences among the near-optimal batches.

Batches 11 and 12 were predominantly local optimization rather than mechanism identification. Their conditions were selected from the already observed peak region. Batch 12 produced the highest observed final score, 0.3615, at risk 0.2255, but its advantage over batch 8 at 0.3584 and batch 11 at 0.3570 was small relative to plausible measurement and process variation.

Several design choices rested mainly on expedience or unverified assumptions. I used the maximum reagent, solvent, and catalyst amounts in every campaign batch, partly because the available stocks exactly supported 12 such batches and partly to obtain strong signals. I never tested whether those maxima were score-optimal. The initial 350 K and 3600 s baseline, the use of 600 rpm, and the exact refinement points at 382 K/3000 s and 380 K/3300 s were pragmatic guesses. They became data-informed only after earlier batches had been observed.

3. Most important competing mechanisms and what can be distinguished

K1 proposed a network with productive formation R→P, parallel byproduct formation R→B, and secondary target loss P→D or P→B. This remains the most economical explanation of batch 10: conversion increased toward completion while retained yield and selectivity deteriorated.

The most important competing explanations are:

- A time- or composition-dependent parallel pathway from reactant, rather than degradation of already formed product. As reactant composition, catalyst state, or medium composition changes, R→B could become progressively favored.
- Catalyst deactivation followed by continued noncatalytic side chemistry. Product need not itself degrade if the productive catalyst state disappears while an undesired pathway remains active.
- Reversible target formation or an equilibrium shift, combined with irreversible trapping into byproducts.
- Multiple hidden products being compressed into the public byproduct and degradation proxy channels. Apparent P→D behavior could partly be a change in instrument mapping rather than a single chemical step.
- Temperature-dependent phase, transport, or catalyst-state changes. The solvent and catalyst categories could alter these latent processes, and the campaign did not directly observe them.

The existing experiments distinguish a fixed, condition-independent parallel-branching model from models with evolving selectivity: batch 10 cannot be explained well by a constant branching fraction that remains unchanged throughout the reaction. They also distinguish a conversion-only optimization rule from a retained-product rule, because the highest conversion did not give the highest score.

They do not uniquely distinguish product degradation from catalyst deactivation, evolving parallel selectivity, reversibility, or hidden phase behavior. Separate batches at 3600 and 7200 s provide suggestive time dependence but not a within-vessel trajectory. Catalyst and solvent effects are also confounded with interactions: the solvent screen used only Catalyst D, and the temperature series used only Catalyst D in acetonitrile. The experiments therefore cannot establish that the observed catalyst ranking persists across solvents or that the thermal optimum persists across catalyst identities.

The safety model is similarly underidentified. K1 inferred a formulation baseline plus a strong peak-temperature term and a weaker duration term. That is consistent with batches 8–10, but the data cannot distinguish peak temperature from temperature-dependent reaction rate, heat release, or other latent categorical contributions.

4. One additional complete experiment I would choose

If permitted exactly one additional legal complete experiment, I would use the batch 8/10 formulation—0.040 mol reagent, 0.005 mol Catalyst D, and 0.080 L acetonitrile at 600 rpm—but run it as an internal two-stage time-course experiment:

- Heat at 375 K for 3600 s.
- Measure once by HPLC.
- Continue heating at 375 K for another 3600 s.
- Terminate and perform the required final assay.

This is not being executed; it is a proposed experiment. Its purpose would be mechanistic discrimination rather than maximizing the expected score. It would reproduce, within one vessel, the transition represented separately by batches 8 and 10 and reduce between-batch variation in the initial state.

If the intermediate measurement resembled batch 8 and the final assay then showed higher conversion but substantially lower yield and selectivity with higher adverse signals, confidence in genuine post-formation loss or evolving side chemistry would increase. It would still not alone distinguish P→D from catalyst deactivation, but it would strengthen the conclusion that longer exposure damages retained target after a favorable intermediate state has been reached.

If conversion, yield, and selectivity all continued to rise during the second interval, the batch 10 result would look less like a reproducible sequential-loss phenomenon and more like batch variation, instrument variation, or a condition-dependent anomaly.

If conversion stayed almost constant while yield fell and degradation rose, that would be particularly strong evidence for target loss after reactant depletion. Conversely, if conversion rose while yield stayed approximately constant and only byproduct increased, an evolving parallel pathway would become more competitive.

A limitation is that the first point would be measured by HPLC and the second by final assay. The observed HPLC/final-assay differences in batches 11 and 12 mean that cross-instrument calibration would remain a confounder. With only one additional complete experiment, however, this design provides more mechanistic information than simply repeating another endpoint.

5. Trade-off between identifiability and operational score

The campaign had two partially conflicting aims: learn enough to choose conditions and produce a strong safe score. The research objective emphasized score under a safety limit, so the design progressively shifted toward optimization.

Batches 1–7 sacrificed some immediate score to identify catalyst and solvent categories. In particular, batches 3 and 7 were poor-scoring but useful because they exposed low-selectivity regimes. Batch 10 also sacrificed expected score for information: doubling the time at 375 K tested whether conversion gains would persist or whether degradation would dominate. Its score of 0.2857 was substantially below the neighboring optimum, but it supplied the strongest mechanistic evidence in the campaign.

By contrast, batches 8, 9, 11, and 12 increasingly concentrated around the promising Catalyst D/acetonitrile region. Batches 11 and 12 were principally optimization refinements. Using two final batches to probe nearby temperature–time combinations improved the chance of a high observed score but did little to identify catalyst-loading response, concentration effects, mixing effects, or catalyst–solvent interactions.

The decision to hold reagent amount, catalyst amount, solvent volume, and stirring speed fixed was the largest optimization-driven loss of identifiability. It preserved a simple comparison and used the available stocks efficiently, but it prevented estimation of reaction orders, catalyst-loading saturation, concentration-dependent safety, and mass-transfer sensitivity. The one-factor-at-a-time progression also made the results easy to interpret locally while leaving interactions almost completely unresolved.

No replicate was reserved. That increased condition coverage and the opportunity to locate a high score, but it sacrificed direct estimation of process repeatability. In retrospect, the score difference among batches 8, 11, and 12 was sufficiently small that one replicate near the apparent optimum could have been more valuable than one of the two fine-grid refinements.

6. Evidence that was underused and weaknesses in the blind predictions

The raw public characterization artifacts were not inspected in detail. I relied on processed estimates rather than examining peak assignments, raw traces, saturation flags, missingness, or replicate structure. Those artifacts might have clarified whether adverse channels changed in a way consistent with distinct products or merely with calibration noise, although their public proxy nature would still limit chemical interpretation.

The operation-level thermal and risk deltas were also underused. I noted terminal temperature changes and the weak additional risk from extending 375 K heating, but I did not fit a quantitative thermal-relaxation or risk model. Setup-stage risk increments across formulations could have been analyzed more systematically. Likewise, the HPLC-to-final-assay differences were discussed qualitatively but not incorporated into a hierarchical instrument-bias model.

The score function remained opaque. I observed that score was not determined by conversion alone, but I did not reliably identify how yield, selectivity, adverse signals, and risk were combined. This matters for the blind score predictions because I effectively extrapolated an empirical score-to-yield relationship rather than a validated scoring equation.

Without any prediction truth now available, the least reliable sealed predictions are Q04, Q06, Q08, and Q12. Q06, Q08, and Q12 use 465 K, well above the highest studied set point of 400 K. Q04 and Q08 combine long exposure with high Catalyst B loading in regimes where conversion was predicted to saturate and target material to be extensively destroyed. The exact lower tail of selectivity and yield in such regimes is governed by an unvalidated extrapolation and possible clipping at zero.

Q10 is also especially uncertain for a different reason: no campaign batch used quench. The sealed prediction assigned Q10 a small improvement over the otherwise identical Q09, but that was conjectural. Quench could affect temperature, risk accounting, residual reaction, or neither in ways not identified by the campaign.

All blind queries used a smaller volume, a somewhat different reagent concentration, 400 rpm rather than 600 rpm, and Catalyst B loadings spanning well below and above the campaign’s fixed catalyst-to-reagent ratio. Thus even the nominally lower-temperature predictions, such as Q05, Q07, and Q11, extrapolated catalyst-loading and concentration effects that were never measured.

Several intervals were probably too narrow for that degree of model-form uncertainty. In particular, Q04’s selectivity interval of 0.03–0.30, Q08’s 0.00–0.18, and the 465 K safety-risk intervals may convey more quantitative confidence than the evidence supports. Q01 and Q03 may also have underrepresented uncertainty in how catalyst loading changes both productive and adverse rates. The intervals accounted for assay noise and some extrapolation uncertainty, but not the full range of plausible alternative mechanisms.

This numerical overconfidence is in tension with, though not a direct contradiction of, K1. K1 explicitly limited applicability to the tested loadings, volume, mixing rate, and 350–400 K region and stated that rate constants and interactions were not identifiable. The prediction rationale also labeled 465 K and extreme degradation cases as least certain. Nevertheless, some sealed numerical intervals were narrower than those qualitative caveats warranted.

7. Limits of the sealed recommendation

Batch 12 is the sample-wise winner, not a proven optimum. Its score of 0.3615 exceeded batch 8’s 0.3584 and batch 11’s 0.3570 by only 0.0031 and 0.0045. Those differences are small relative to the declared measurement noise and unmeasured process variability. With one observation per condition, there is no basis for claiming that 380 K for 3300 s has a higher expected score than all neighboring settings.

The recommendation is also local to Catalyst D, acetonitrile, the fixed amounts, 600 rpm, and this benchmark world. It does not establish optimal catalyst loading, concentration, solvent volume, or mixing. It does not establish that Catalyst D remains best in water or ethanol, nor that acetonitrile remains best with other catalysts. The high-cost flag was present throughout the max-loading campaign, so the procedure may also be unattractive under a different objective that weights cost more strongly.

Repeatability should first be tested by independent exact replicates of batch 12, including the same final assay and preferably the same intermediate HPLC measurement. Replication would estimate process variance, instrument variance, the probability of remaining below the safety limit, and the expected rather than maximum observed score.

Local robustness should then be tested with a small designed neighborhood around the recommendation—for example modest independent perturbations of temperature, duration, catalyst loading, and stirring speed. A robust plateau would be preferable to a sharp maximum whose apparent superiority arose from noise. The existing similarity of batches 8, 11, and 12 suggests a plateau around approximately 375–382 K and 3000–3600 s, but it does not prove one.

Cross-material generalization requires explicit catalyst–solvent interaction experiments rather than transferring the current ranking. Cross-scale or cross-process generalization requires varying concentration, volume, and mixing. Cross-world generalization would require repeating the design in independently initialized benchmark worlds or scenarios, because the material packet explicitly describes latent categorical activity profiles rather than universal properties.

Accordingly, the strongest defensible statement is: batch 12 had the highest observed score among the 12 sampled procedures and remained below the declared safety limit. It has not been shown to be uniquely optimal, statistically superior to neighboring batches, reproducible, robust to perturbations, or transferable beyond the studied benchmark conditions.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 89.6 | none | 0 |
| Q | yes | 0 | 120.4 | none | 0 |
| K2 | yes | 0 | 92.8 | none | 0 |

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean 80% width | Mean interval score |
|---|---:|---:|---:|---:|
| byproduct_signal | 0.1180 | 0.7000 | 0.3000 | 0.5717 |
| conversion | 0.0374 | 0.8833 | 0.1283 | 0.1367 |
| safety_risk | 0.0757 | 0.8333 | 0.2175 | 0.3073 |
| score | 0.0835 | 0.6667 | 0.1958 | 0.3121 |
| selectivity | 0.1424 | 0.6667 | 0.2842 | 0.6971 |
| yield | 0.1288 | 0.7500 | 0.3017 | 0.5979 |

## Predictions versus released reference truth

### Q01

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1500 | 0.0700 | 0.2900 | 0.1394 | 0.1397, 0.1462, 0.1413, 0.1384, 0.1316 |
| conversion | 0.3800 | 0.2200 | 0.5600 | 0.5419 | 0.5369, 0.5361, 0.5497, 0.5430, 0.5438 |
| safety_risk | 0.2500 | 0.1700 | 0.3400 | 0.2496 | 0.2496, 0.2496, 0.2496, 0.2496, 0.2496 |
| score | 0.1800 | 0.0900 | 0.2800 | 0.2633 | 0.2655, 0.2652, 0.2643, 0.2587, 0.2626 |
| selectivity | 0.8400 | 0.7200 | 0.9200 | 0.7421 | 0.7503, 0.7451, 0.7464, 0.7401, 0.7288 |
| yield | 0.3200 | 0.1900 | 0.4700 | 0.4090 | 0.4107, 0.4134, 0.4068, 0.3985, 0.4152 |
### Q02

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4200 | 0.2500 | 0.6200 | 0.7361 | 0.7397, 0.7292, 0.7492, 0.7245, 0.7377 |
| conversion | 0.9700 | 0.9000 | 1.0000 | 0.9894 | 0.9940, 0.9820, 0.9971, 0.9889, 0.9850 |
| safety_risk | 0.2600 | 0.1800 | 0.3600 | 0.2515 | 0.2515, 0.2515, 0.2515, 0.2515, 0.2515 |
| score | 0.2700 | 0.1500 | 0.3800 | 0.1240 | 0.1282, 0.1246, 0.1241, 0.1240, 0.1192 |
| selectivity | 0.5800 | 0.3800 | 0.7400 | 0.2740 | 0.2821, 0.2767, 0.2785, 0.2713, 0.2612 |
| yield | 0.5600 | 0.3600 | 0.7200 | 0.2699 | 0.2741, 0.2715, 0.2653, 0.2716, 0.2669 |
### Q03

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2400 | 0.1200 | 0.3900 | 0.1516 | 0.1469, 0.1490, 0.1465, 0.1682, 0.1471 |
| conversion | 0.8600 | 0.7200 | 0.9500 | 0.9045 | 0.9126, 0.8934, 0.9063, 0.9038, 0.9066 |
| safety_risk | 0.3000 | 0.2000 | 0.4100 | 0.2526 | 0.2526, 0.2526, 0.2526, 0.2526, 0.2526 |
| score | 0.3400 | 0.2200 | 0.4500 | 0.4366 | 0.4406, 0.4357, 0.4386, 0.4338, 0.4345 |
| selectivity | 0.7600 | 0.6200 | 0.8700 | 0.8453 | 0.8629, 0.8401, 0.8425, 0.8499, 0.8314 |
| yield | 0.6500 | 0.4700 | 0.7800 | 0.7624 | 0.7594, 0.7661, 0.7686, 0.7528, 0.7653 |
### Q04

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.8600 | 0.6700 | 0.9700 | 0.7894 | 0.7706, 0.7875, 0.8048, 0.7903, 0.7936 |
| conversion | 1.0000 | 0.9700 | 1.0000 | 0.9959 | 1.0000, 0.9907, 1.0000, 0.9890, 1.0000 |
| safety_risk | 0.3200 | 0.2200 | 0.4500 | 0.2519 | 0.2519, 0.2519, 0.2519, 0.2519, 0.2519 |
| score | 0.0400 | 0.0000 | 0.1300 | 0.0871 | 0.0917, 0.0894, 0.0841, 0.0875, 0.0830 |
| selectivity | 0.1200 | 0.0300 | 0.3000 | 0.2562 | 0.2603, 0.2645, 0.2443, 0.2601, 0.2517 |
| yield | 0.1200 | 0.0300 | 0.2900 | 0.2596 | 0.2675, 0.2614, 0.2583, 0.2597, 0.2510 |
### Q05

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1500 | 0.0700 | 0.2800 | 0.2859 | 0.2874, 0.2976, 0.2794, 0.2754, 0.2894 |
| conversion | 0.5500 | 0.3900 | 0.7000 | 0.7070 | 0.7056, 0.7061, 0.7105, 0.7038, 0.7091 |
| safety_risk | 0.1800 | 0.1200 | 0.2500 | 0.1416 | 0.1416, 0.1416, 0.1416, 0.1416, 0.1416 |
| score | 0.2600 | 0.1600 | 0.3600 | 0.2914 | 0.2937, 0.2855, 0.2896, 0.2953, 0.2931 |
| selectivity | 0.8300 | 0.7200 | 0.9100 | 0.6004 | 0.6055, 0.5865, 0.5961, 0.6143, 0.5996 |
| yield | 0.4600 | 0.3200 | 0.6000 | 0.4163 | 0.4191, 0.4105, 0.4134, 0.4182, 0.4204 |
### Q06

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.6400 | 0.4300 | 0.8200 | 0.6099 | 0.6123, 0.6066, 0.6036, 0.6193, 0.6079 |
| conversion | 0.9800 | 0.9100 | 1.0000 | 0.9947 | 1.0000, 0.9837, 0.9990, 0.9934, 0.9973 |
| safety_risk | 0.5200 | 0.3700 | 0.7000 | 0.4259 | 0.4259, 0.4259, 0.4259, 0.4259, 0.4259 |
| score | 0.1200 | 0.0300 | 0.2400 | 0.1323 | 0.1345, 0.1397, 0.1227, 0.1333, 0.1313 |
| selectivity | 0.3600 | 0.1800 | 0.5600 | 0.3927 | 0.3842, 0.4258, 0.3714, 0.4011, 0.3809 |
| yield | 0.3500 | 0.1700 | 0.5400 | 0.3962 | 0.4056, 0.3968, 0.3843, 0.3939, 0.4005 |
### Q07

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3600 | 0.2200 | 0.5200 | 0.3215 | 0.3256, 0.3232, 0.3132, 0.3178, 0.3278 |
| conversion | 0.9600 | 0.8900 | 0.9900 | 0.9676 | 0.9735, 0.9585, 0.9756, 0.9696, 0.9610 |
| safety_risk | 0.2100 | 0.1400 | 0.2900 | 0.1439 | 0.1439, 0.1439, 0.1439, 0.1439, 0.1439 |
| score | 0.3100 | 0.2000 | 0.4200 | 0.4053 | 0.4066, 0.4069, 0.4029, 0.4048, 0.4054 |
| selectivity | 0.6400 | 0.4900 | 0.7700 | 0.6857 | 0.6945, 0.6952, 0.6796, 0.6717, 0.6874 |
| yield | 0.6100 | 0.4600 | 0.7400 | 0.6572 | 0.6533, 0.6575, 0.6531, 0.6640, 0.6580 |
### Q08

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.9400 | 0.8000 | 1.0000 | 0.6400 | 0.6433, 0.6384, 0.6379, 0.6363, 0.6440 |
| conversion | 1.0000 | 0.9900 | 1.0000 | 0.9930 | 0.9781, 0.9871, 1.0000, 1.0000, 1.0000 |
| safety_risk | 0.6800 | 0.5000 | 0.8500 | 0.4263 | 0.4263, 0.4263, 0.4263, 0.4263, 0.4263 |
| score | 0.0100 | 0.0000 | 0.0600 | 0.1053 | 0.1049, 0.1045, 0.0992, 0.1060, 0.1120 |
| selectivity | 0.0600 | 0.0000 | 0.1800 | 0.4013 | 0.4087, 0.3948, 0.3933, 0.3967, 0.4131 |
| yield | 0.0600 | 0.0000 | 0.1800 | 0.3962 | 0.3944, 0.3998, 0.3842, 0.3991, 0.4038 |
### Q09

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5500 | 0.3800 | 0.7100 | 0.4912 | 0.4900, 0.4852, 0.4940, 0.4841, 0.5025 |
| conversion | 0.9900 | 0.9500 | 1.0000 | 0.9974 | 1.0000, 0.9923, 1.0000, 1.0000, 0.9946 |
| safety_risk | 0.2900 | 0.2000 | 0.4000 | 0.2523 | 0.2523, 0.2523, 0.2523, 0.2523, 0.2523 |
| score | 0.1900 | 0.0900 | 0.3000 | 0.2752 | 0.2725, 0.2767, 0.2744, 0.2725, 0.2800 |
| selectivity | 0.4500 | 0.2900 | 0.6100 | 0.5164 | 0.5050, 0.5198, 0.5199, 0.5132, 0.5241 |
| yield | 0.4400 | 0.2800 | 0.6000 | 0.5154 | 0.5150, 0.5181, 0.5106, 0.5099, 0.5231 |
### Q10

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5400 | 0.3700 | 0.7000 | 0.4949 | 0.4892, 0.4966, 0.4999, 0.5047, 0.4842 |
| conversion | 0.9900 | 0.9500 | 1.0000 | 0.9942 | 0.9991, 0.9998, 1.0000, 0.9939, 0.9781 |
| safety_risk | 0.2700 | 0.1800 | 0.3800 | 0.1459 | 0.1459, 0.1459, 0.1459, 0.1459, 0.1459 |
| score | 0.2000 | 0.1000 | 0.3100 | 0.3201 | 0.3218, 0.3178, 0.3232, 0.3200, 0.3179 |
| selectivity | 0.4600 | 0.3000 | 0.6200 | 0.5173 | 0.5167, 0.5191, 0.5235, 0.5115, 0.5160 |
| yield | 0.4500 | 0.2900 | 0.6100 | 0.5165 | 0.5199, 0.5082, 0.5188, 0.5198, 0.5156 |
### Q11

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4400 | 0.2900 | 0.6000 | 0.5489 | 0.5697, 0.5532, 0.5308, 0.5504, 0.5403 |
| conversion | 0.9800 | 0.9200 | 1.0000 | 0.9903 | 0.9833, 0.9865, 0.9912, 0.9955, 0.9949 |
| safety_risk | 0.2000 | 0.1400 | 0.2800 | 0.1434 | 0.1434, 0.1434, 0.1434, 0.1434, 0.1434 |
| score | 0.2700 | 0.1600 | 0.3800 | 0.2810 | 0.2783, 0.2768, 0.2825, 0.2819, 0.2854 |
| selectivity | 0.5600 | 0.4000 | 0.7000 | 0.4585 | 0.4538, 0.4471, 0.4607, 0.4561, 0.4750 |
| yield | 0.5500 | 0.3900 | 0.6900 | 0.4602 | 0.4583, 0.4578, 0.4625, 0.4628, 0.4597 |
### Q12

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4200 | 0.2500 | 0.6200 | 0.2069 | 0.2063, 0.2058, 0.1964, 0.2129, 0.2132 |
| conversion | 0.9400 | 0.8400 | 0.9900 | 0.9513 | 0.9555, 0.9519, 0.9512, 0.9428, 0.9552 |
| safety_risk | 0.5400 | 0.3800 | 0.7000 | 0.4267 | 0.4267, 0.4267, 0.4267, 0.4267, 0.4267 |
| score | 0.1800 | 0.0600 | 0.3000 | 0.3582 | 0.3619, 0.3582, 0.3617, 0.3502, 0.3588 |
| selectivity | 0.5800 | 0.3800 | 0.7400 | 0.7886 | 0.7934, 0.7801, 0.8111, 0.7735, 0.7849 |
| yield | 0.5400 | 0.3400 | 0.7000 | 0.7491 | 0.7543, 0.7544, 0.7438, 0.7407, 0.7521 |

## Recommendation retest

- Selected source batch: `12`
- Retest exact replay verified: `True`
- Retest failure: `none`

| Metric | Selected source batch | Independent retest | Retest minus source |
|---|---:|---:|---:|
| byproduct_signal | 0.1929 | 0.1752 | -0.0177 |
| conversion | 0.8858 | 0.8718 | -0.0141 |
| cost | 1.0000 | 1.0000 | 0.0000 |
| degradation_warning | 0.1241 | 0.1295 | 0.0055 |
| safety_risk | 0.2255 | 0.2255 | 0.0000 |
| score | 0.3615 | 0.3562 | -0.0053 |
| selectivity | 0.7819 | 0.7835 | 0.0016 |
| virtual_spectrum_summary | 0.1619 | 0.1547 | -0.0073 |
| yield | 0.6973 | 0.6866 | -0.0107 |

## Scope note

This is the final sanitized report produced after all 60 source sessions and K1/Q/K2 chains were sealed. It includes released reference truth, blind-prediction evaluation, and the independent recommendation retest. Provider-private event streams, credentials, thread identifiers, and token accounting remain excluded.
