# RX-W04--P--mechanism_discovery--Opaque

## Run summary

- World: `RX-W04`
- Locus: `P`
- Goal: `mechanism_discovery`
- Arm: `Opaque`
- Status: `completed`
- Source status: `completed`
- Experimental sessions: `12/12`
- Operations: `85`
- Exact replay verified: `True`
- Rollbacks: `[]`
- Posttest chain sealed: `True`

### Recovery status

No recovery override was required for this task.

## Sealed recommendation

- Selected batch: `12`
- Rationale: Batch 12 gave the highest observed safe score while combining high conversion and yield with prompt quenching; it also remained below the 0.35 safety-risk limit.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S0 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.2517 | 0.6378 | 0.3882 | 0.1576 | 0.0157 | 0.1099 | 0.1495 |
| 2 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.4270 | 0.7735 | 0.5532 | 0.1204 | 0.0231 | 0.1273 | 0.2622 |
| 3 | S0 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.2365 | 0.5669 | 0.4231 | 0.1931 | 0.0000 | 0.1089 | 0.1296 |
| 4 | S0 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.2949 | 0.6953 | 0.4074 | 0.1167 | 0.0278 | 0.1134 | 0.1815 |
| 5 | S1 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.3970 | 0.6327 | 0.6129 | 0.2335 | 0.0622 | 0.1513 | 0.2102 |
| 6 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.6065 | 0.7026 | 0.8271 | 0.2487 | 0.1099 | 0.1923 | 0.3144 |
| 7 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.6250 | 0.7529 | 0.8150 | 0.2205 | 0.0875 | 0.2064 | 0.3268 |
| 8 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 330 K x 3600 s @ 600 rpm | no | 0.5246 | 0.7393 | 0.6827 | 0.1757 | 0.0343 | 0.1893 | 0.2778 |
| 9 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 370 K x 3600 s @ 600 rpm | no | 0.6754 | 0.7463 | 0.9218 | 0.2470 | 0.1174 | 0.2273 | 0.3466 |
| 10 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 390 K x 3600 s @ 600 rpm | no | 0.6919 | 0.7188 | 0.9560 | 0.2717 | 0.1576 | 0.2697 | 0.3307 |
| 11 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 370 K x 7200 s @ 600 rpm | no | 0.5747 | 0.5832 | 0.9937 | 0.4300 | 0.2785 | 0.2296 | 0.2717 |
| 12 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 370 K x 3600 s @ 600 rpm | yes | 0.6765 | 0.7285 | 0.9276 | 0.2337 | 0.1308 | 0.2095 | 0.3512 |

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
    "byproduct_signal": 0.1575903594493866,
    "conversion": 0.3881981074810028,
    "cost": 1.0,
    "degradation_warning": 0.015726471319794655,
    "safety_risk": 0.10985220968723297,
    "score": 0.14952272176742554,
    "selectivity": 0.6377594470977783,
    "virtual_spectrum_summary": 0.09375160932540894,
    "yield": 0.2517413794994354
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
    "byproduct_signal": 0.1204213872551918,
    "conversion": 0.5531877875328064,
    "cost": 1.0,
    "degradation_warning": 0.02308971807360649,
    "safety_risk": 0.12729288637638092,
    "score": 0.2622109353542328,
    "selectivity": 0.7735079526901245,
    "virtual_spectrum_summary": 0.0766221359372139,
    "yield": 0.42699241638183594
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
      "solvent": 0,
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
    "byproduct_signal": 0.19308032095432281,
    "conversion": 0.42313340306282043,
    "cost": 1.0,
    "degradation_warning": 0.0,
    "safety_risk": 0.10889402776956558,
    "score": 0.1296273022890091,
    "selectivity": 0.5668966174125671,
    "virtual_spectrum_summary": 0.10619417577981949,
    "yield": 0.23648031055927277
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
  "end_step": 28,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.11665486544370651,
    "conversion": 0.407381147146225,
    "cost": 1.0,
    "degradation_warning": 0.027758967131376266,
    "safety_risk": 0.1134122759103775,
    "score": 0.18147705495357513,
    "selectivity": 0.6952978372573853,
    "virtual_spectrum_summary": 0.07665171474218369,
    "yield": 0.29487502574920654
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
    "byproduct_signal": 0.23351053893566132,
    "conversion": 0.6128522753715515,
    "cost": 1.0,
    "degradation_warning": 0.06218765676021576,
    "safety_risk": 0.15130333602428436,
    "score": 0.2101639062166214,
    "selectivity": 0.6327002644538879,
    "virtual_spectrum_summary": 0.15641523897647858,
    "yield": 0.39697524905204773
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
  "end_step": 42,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.24869301915168762,
    "conversion": 0.8271124362945557,
    "cost": 1.0,
    "degradation_warning": 0.10993129760026932,
    "safety_risk": 0.1923234462738037,
    "score": 0.31442394852638245,
    "selectivity": 0.7025766968727112,
    "virtual_spectrum_summary": 0.186250239610672,
    "yield": 0.6065352559089661
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
  "end_step": 49,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.22050008177757263,
    "conversion": 0.8150115013122559,
    "cost": 1.0,
    "degradation_warning": 0.08751863241195679,
    "safety_risk": 0.20643991231918335,
    "score": 0.3268202543258667,
    "selectivity": 0.7529040575027466,
    "virtual_spectrum_summary": 0.16065843403339386,
    "yield": 0.6249775886535645
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
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 330
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
    "byproduct_signal": 0.17566454410552979,
    "conversion": 0.6827033162117004,
    "cost": 1.0,
    "degradation_warning": 0.03430338576436043,
    "safety_risk": 0.189253032207489,
    "score": 0.27777668833732605,
    "selectivity": 0.7392930388450623,
    "virtual_spectrum_summary": 0.11205202341079712,
    "yield": 0.5246173739433289
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
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
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
    "byproduct_signal": 0.2470460832118988,
    "conversion": 0.9217622876167297,
    "cost": 1.0,
    "degradation_warning": 0.117387555539608,
    "safety_risk": 0.22733795642852783,
    "score": 0.34661075472831726,
    "selectivity": 0.7463311553001404,
    "virtual_spectrum_summary": 0.18869973719120026,
    "yield": 0.675384521484375
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
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
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
  "end_step": 70,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.271688848733902,
    "conversion": 0.9560245275497437,
    "cost": 1.0,
    "degradation_warning": 0.15757165849208832,
    "safety_risk": 0.2696792483329773,
    "score": 0.3307076394557953,
    "selectivity": 0.718839704990387,
    "virtual_spectrum_summary": 0.22033610939979553,
    "yield": 0.6918773055076599
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 600,
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
  "end_step": 77,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.4299514889717102,
    "conversion": 0.9936544895172119,
    "cost": 1.0,
    "degradation_warning": 0.27853208780288696,
    "safety_risk": 0.22961531579494476,
    "score": 0.2716999351978302,
    "selectivity": 0.5831671357154846,
    "virtual_spectrum_summary": 0.3618127703666687,
    "yield": 0.5746740102767944
  },
  "ordinal": 11
}
```

### Batch 12

Lifecycle index: `12`; end step: `85`.

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
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 370
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "operation": "quench"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 85,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.23365040123462677,
    "conversion": 0.9275929927825928,
    "cost": 1.0,
    "degradation_warning": 0.13080398738384247,
    "safety_risk": 0.20949068665504456,
    "score": 0.351211816072464,
    "selectivity": 0.7284557223320007,
    "virtual_spectrum_summary": 0.18736951053142548,
    "yield": 0.6765235066413879
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

1. Experimental domain

All 12 batches used 0.040 mol of the anonymous limiting reagent, 0.005 mol of catalyst, 0.080 L of one solvent, and 600 rpm stirring. Thus, before sampling, the nominal reagent concentration was 0.50 mol/L and the catalyst/reagent ratio was 0.125. Each batch received an intermediate HPLC measurement after heating and a final assay after termination. Batch 12 additionally received a quench between HPLC and termination. The reported species are anonymous proxies, so this report does not assign them real chemical identities.

The main controlled variables were catalyst category, solvent category, heating target, heating duration, and quenching. The studied region was limited to four catalysts, four solvents, heating targets of 330–390 K, and durations of 3600 or 7200 s. No catalyst-free, concentration, catalyst-loading, or stirring-rate series was performed.

2. Direct observations

Catalyst comparison

Batches 1–4 compared the four catalysts in water at a 350 K target for 3600 s:

- Batch 1, Catalyst A: conversion 0.3882, yield 0.2517, selectivity 0.6378, byproduct signal 0.1576, degradation warning 0.0157, safety risk 0.1099.
- Batch 2, Catalyst B: conversion 0.5532, yield 0.4270, selectivity 0.7735, byproduct signal 0.1204, degradation warning 0.0231, safety risk 0.1273.
- Batch 3, Catalyst C: conversion 0.4231, yield 0.2365, selectivity 0.5669, byproduct signal 0.1931, degradation warning reported at 0, safety risk 0.1089.
- Batch 4, Catalyst D: conversion 0.4074, yield 0.2949, selectivity 0.6953, byproduct signal 0.1167, degradation warning 0.0278, safety risk 0.1134.

Catalyst B was therefore the best of the tested catalysts under the common water condition. It increased both conversion and the fraction directed toward target relative to A, C, and D. Catalyst C was particularly unfavorable for selectivity. The zero degradation value in Batch 3 should be treated as a noisy, floor-clipped observation rather than proof that degradation was absent.

Solvent comparison

Batches 2 and 5–7 used Catalyst B at 350 K for 3600 s:

- Batch 2, water: conversion 0.5532, yield 0.4270, selectivity 0.7735, byproduct 0.1204, degradation 0.0231, risk 0.1273.
- Batch 5, ethanol: conversion 0.6129, yield 0.3970, selectivity 0.6327, byproduct 0.2335, degradation 0.0622, risk 0.1513.
- Batch 6, acetonitrile: conversion 0.8271, yield 0.6065, selectivity 0.7026, byproduct 0.2487, degradation 0.1099, risk 0.1923.
- Batch 7, toluene: conversion 0.8150, yield 0.6250, selectivity 0.7529, byproduct 0.2205, degradation 0.0875, risk 0.2064.

The solvent category strongly affected both rate and pathway partitioning. Water with Catalyst B gave the highest measured selectivity but only moderate conversion. Ethanol increased conversion slightly while sharply worsening selectivity. Acetonitrile and toluene greatly accelerated disappearance of reactant. Toluene gave slightly lower conversion than acetonitrile but higher yield and selectivity, making it the best observed solvent for target formation at this setting. These are benchmark categorical effects and should not be rationalized from real-solvent properties without additional evidence.

Temperature comparison

Batches 8, 7, 9, and 10 used Catalyst B and toluene for 3600 s at successively higher targets:

- Batch 8, 330 K: conversion 0.6827, yield 0.5246, selectivity 0.7393, byproduct 0.1757, degradation 0.0343, risk 0.1893. The heating operation reported a 30.25 K temperature rise.
- Batch 7, 350 K: conversion 0.8150, yield 0.6250, selectivity 0.7529, byproduct 0.2205, degradation 0.0875, risk 0.2064. The reported rise was 49.17 K.
- Batch 9, 370 K: conversion 0.9218, yield 0.6754, selectivity 0.7463, byproduct 0.2470, degradation 0.1174, risk 0.2273. The reported rise was 67.57 K.
- Batch 10, 390 K: conversion 0.9560, yield 0.6919, selectivity 0.7188, byproduct 0.2717, degradation 0.1576, risk 0.2697. The reported rise was 85.48 K.

Conversion and target yield rose monotonically over this tested range, but selectivity stopped improving and declined at 390 K. Both byproduct and degradation signals rose with temperature. Thus temperature accelerates desired formation and competing chemistry simultaneously. The highest observed final chemical yield was in Batch 10, but its selectivity and safe score were worse than at 370 K.

Time comparison and evidence for secondary loss

Batch 11 repeated the Catalyst B/toluene/370 K condition for 7200 rather than 3600 s. Compared with Batch 9:

- Conversion increased from 0.9218 to 0.9937.
- Yield fell from 0.6754 to 0.5747.
- Selectivity fell from 0.7463 to 0.5832.
- Byproduct signal rose from 0.2470 to 0.4300.
- Degradation warning rose from 0.1174 to 0.2785.
- Risk remained similar, 0.2273 versus 0.2296.

This is the clearest evidence that the target is not simply a stable terminal product. Continued hot residence consumes the remaining reactant but also destroys target or diverts late conversion into byproduct/degradation channels. A model containing only irreversible parallel formation of stable target and stable byproduct cannot readily explain the substantial decline in target yield at longer time. A sequential target-to-degradation pathway, or a time-dependent change in catalytic selectivity, is needed.

Quench comparison

Batch 12 repeated the nominal Batch 9 recipe and added a quench. Its pre-quench HPLC values were conversion 0.9318, yield 0.6659, selectivity 0.7278, and byproduct 0.2424. The quench lowered temperature by 45 K over 57.9 s and reduced reported risk by 0.01785. Its final assay gave conversion 0.9276, yield 0.6765, selectivity 0.7285, byproduct 0.2337, degradation 0.1308, risk 0.2095, and score 0.3512.

The corresponding unquenched Batch 9 final values were conversion 0.9218, yield 0.6754, selectivity 0.7463, byproduct 0.2470, degradation 0.1174, risk 0.2273, and score 0.3466. The chemical differences between these single batches are small relative to assay uncertainty and between-instrument differences; therefore I do not claim that quenching measurably increased yield. The robust observed effect was rapid cooling and lower reported safety risk. Batch 12 achieved the highest overall safe score, primarily because it retained the high-yield 370 K state while reducing risk promptly.

3. Proposed reaction and thermal mechanism

A minimal explanatory network is:

R --kP--> P
R --kB--> B
P --kD--> D

Here R is the limiting reactant proxy, P is target product, B is competing byproduct, and D represents degradation products. Catalyst identity and solvent category modify all three effective rates. A more flexible version allows B also to arise from P and allows catalyst activity to change with time.

One useful set of differential equations is:

dR/dt = -a(t)[kP(T,S,C) + kB(T,S,C)]R

dP/dt = a(t)kP(T,S,C)R - kD(T,S,C)P

dB/dt = a(t)kB(T,S,C)R + kPB(T,S,C)P

dD/dt = kD(T,S,C)P

da/dt = -kdeact(T,S,C)a

C and S denote catalyst and solvent categories. The catalyst activity a(t) permits deactivation, although the present data do not require strong deactivation to explain reactant conversion. The rate coefficients may be represented locally as k_i = A_i(C,S) exp[-E_i(C,S)/(RT)], but this is only a phenomenological form for the synthetic world.

Measured quantities are approximately related by conversion X = 1 - R/R0, yield Y = P/R0, and selectivity S_P approximately Y/X. The reported yield, conversion, and selectivity were independently noisy, so this identity is approximate rather than exact in individual assays.

For stable, pseudo-first-order disappearance under a constant effective condition, X(t) = 1 - exp(-k_app t). Applying this expression to the final conversions in Batches 8, 7, 9, and 10 gives apparent rate constants of approximately 3.19e-4, 4.69e-4, 7.08e-4, and 8.68e-4 s^-1 at target settings of 330, 350, 370, and 390 K. Batch 11 independently gives 7.03e-4 s^-1 from its 7200 s conversion at 370 K, almost identical to Batch 9's 7.08e-4 s^-1. This agreement is strong evidence that reactant disappearance is approximately first order over the 370 K, one-to-two-hour interval.

A linear fit of ln(k_app) against 1/T using the target settings gives a slope near -2207 K, corresponding formally to about 18 kJ/mol. I regard that number only as an empirical interpolation descriptor. The vessel experienced a heating trajectory rather than an instantaneous constant target temperature, and the absolute temperature history was not directly observed.

For the simple sequential model, target concentration has the form

P/R0 = [kP/(kR-kD)] [exp(-kD t) - exp(-kR t)],

where kR = kP + kB. This expression naturally produces a target-yield maximum followed by decline. Batch 11 provides qualitative evidence for that shape. Higher temperature increases kR and therefore early target formation, but it also increases kD and competing formation enough to lower selectivity and eventually reduce useful yield.

4. Thermal and safety coupling

The reported temperature rises show that commanded target temperature is not identical to instantaneous material temperature. A reasonable process description is a first-order heating response,

dT/dt = [Tset - T]/tau_heat + Qreaction/(mCp),

followed during quench by a much larger negative heat-removal term. Only net temperature changes were exposed, so tau_heat and reaction heat cannot be separately identified. The nearly equal endpoint temperature rises in Batches 9 and 11, 67.57 and 67.51 K despite different durations, suggest that the vessel approached a thermal plateau well before 7200 s.

Safety risk coupled to formulation and temperature. At the common 350 K setting, risk increased from 0.1273 in water to 0.2064 in toluene. Within the Catalyst B/toluene series it increased from 0.1893 at 330 K to 0.2697 at 390 K. Extending 370 K residence from 3600 to 7200 s barely changed final risk, suggesting that the displayed risk is dominated more by formulation and thermal state than by a simple time integral. Quenching reduced risk directly. Every completed batch remained below the specified 0.35 limit.

5. How the explanation changed during the campaign

Batch 1 initially showed only moderate conversion and substantial competing product. Batches 2–4 demonstrated that catalyst identity changes both rate and selectivity, not merely overall speed; this led to selecting Catalyst B as the active and comparatively selective category.

Batches 5–7 then showed that solvent is also mechanistically coupled to both disappearance and pathway partitioning. The high conversion in acetonitrile and toluene, together with their larger byproduct/degradation signals, rejected a simple interpretation in which solvent changes only target formation.

Batches 8–10 established a monotonic temperature dependence of conversion but a nonmonotonic selectivity response. This changed the working account from one desired Arrhenius reaction to at least two thermally activated channels with different temperature sensitivities.

Batch 11 was decisive for adding secondary target loss or time-dependent selectivity: conversion approached completion while target yield fell and degradation/byproduct signals rose sharply. The close agreement of the apparent conversion rate constants from Batches 9 and 11 argues against severe catalyst deactivation controlling reactant disappearance, although deactivation or catalyst-state evolution could still alter selectivity.

Batch 12 showed that quenching chiefly affects the thermal/safety state under the conditions tested. It did not supply statistically compelling evidence for a chemical yield increase over the unquenched Batch 9, but it is consistent with arresting further hot degradation and is operationally preferable.

6. Scope, unidentified factors, and competing explanations

This account is supported only within the tested categorical materials, fixed concentrations and loading, 600 rpm stirring, and the stated temperature/time range. Extrapolation to lower catalyst loading, different concentration, different mixing, or temperatures outside 330–390 K is speculative.

There were no replicate batches. HPLC and final-assay uncertainties were approximately 0.012 and 0.006–0.010 for several principal channels, with larger selectivity uncertainty for HPLC. Small differences, especially the Batch 9 versus Batch 12 chemical differences and the toluene versus acetonitrile comparison, should not be overinterpreted.

The experiment did not directly observe catalyst concentration, catalyst state, true molecular species, absolute temperature traces, reaction heat, or mass-transfer coefficients. Consequently, intrinsic kinetic constants, reaction orders, activation energies, and catalyst-deactivation constants are not uniquely identifiable.

Several competing interpretations remain reasonable:

- The late yield loss may be direct degradation of target P, conversion of P into the measured byproduct, or a catalyst-state change that makes late reactant conversion less selective.
- The solvent effects may reflect intrinsic kinetics, catalyst activation, heat transfer, phase behavior, or measurement response. Because solvents are categorical benchmark couplings, real-world polarity or boiling-point explanations are unsupported.
- The apparent first-order behavior could arise from true first-order kinetics, pseudo-first-order catalysis at fixed loading, or a combination of heat-up and saturation effects that happens to mimic first-order conversion over this range.
- Increasing degradation warning and byproduct signal need not represent the same physical species or pathway; they are independent public channels.
- Similar endpoint temperatures do not prove identical full thermal histories.

Within those limitations, the most economical predictive account is competing pseudo-first-order reactant consumption combined with secondary target loss. Catalyst B and toluene raise the effective desired rate enough to obtain high conversion, but hotter or longer operation increasingly activates byproduct and degradation channels. Near a 370 K target and 3600 s, target formation is close to its useful maximum before severe late loss. Prompt quenching then lowers thermal risk and plausibly freezes that product distribution, even though the single quench comparison did not resolve a chemical preservation effect beyond measurement uncertainty.

## Q — Blind predictions

### Overall rationale

Predictions use the campaign-derived competing pseudo-first-order model: catalyst and temperature accelerate reactant disappearance, while hotter or longer residence increasingly converts target into byproduct or degradation channels. The acetonitrile baseline comes from Batch 6; temperature and time responses are transferred primarily from Batches 7–11, and quench effects from Batch 12 versus Batch 9. The blind batches have a higher catalyst concentration, slightly higher reagent concentration, lower stirring rate, much smaller total inventory, and mostly exceed the measured temperature range. Intervals therefore include instrument noise, model uncertainty, categorical solvent transfer uncertainty, and especially uncertainty in extrapolated degradation and quantity-dependent safety risk.

### Q01

At 420 K, the higher catalyst concentration should drive nearly complete conversion within 3300 s, but extrapolated secondary target loss should reduce yield and selectivity. Risk is uncertain because the temperature exceeds my measured range while the batch inventory is much smaller.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3600 | 0.2500 | 0.4800 |
| conversion | 0.9940 | 0.9650 | 1.0000 |
| safety_risk | 0.1500 | 0.0700 | 0.2700 |
| score | 0.2700 | 0.1600 | 0.3900 |
| selectivity | 0.5700 | 0.4500 | 0.6800 |
| yield | 0.5600 | 0.4300 | 0.6800 |

### Q02

The chemical state should be close to Q01 because quenching follows the only hot reaction period. I predict only a small chemical preservation effect but a clearer reduction in terminal safety risk, analogous to the Batch 9 versus Batch 12 comparison.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3500 | 0.2400 | 0.4700 |
| conversion | 0.9940 | 0.9650 | 1.0000 |
| safety_risk | 0.1200 | 0.0500 | 0.2300 |
| score | 0.2900 | 0.1800 | 0.4200 |
| selectivity | 0.5800 | 0.4600 | 0.6900 |
| yield | 0.5700 | 0.4400 | 0.6900 |

### Q03

Lowering the target to 390 K should retain high conversion while suppressing secondary degradation relative to 420 K. This is an extrapolation from the observed 370–390 K trend, adjusted for the larger catalyst concentration and lower stirring rate.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2900 | 0.1900 | 0.4000 |
| conversion | 0.9850 | 0.9400 | 1.0000 |
| safety_risk | 0.1100 | 0.0500 | 0.2000 |
| score | 0.3700 | 0.2500 | 0.4900 |
| selectivity | 0.6600 | 0.5500 | 0.7600 |
| yield | 0.6400 | 0.5200 | 0.7500 |

### Q04

At 450 K, reactant disappearance should be essentially complete, but the temperature is well beyond the measured range and should strongly accelerate target-to-degradation and byproduct pathways. The wide intervals reflect that extrapolation.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4900 | 0.3500 | 0.6400 |
| conversion | 0.9990 | 0.9850 | 1.0000 |
| safety_risk | 0.2300 | 0.1100 | 0.3900 |
| score | 0.1500 | 0.0600 | 0.2800 |
| selectivity | 0.4400 | 0.3000 | 0.5800 |
| yield | 0.4300 | 0.2800 | 0.5800 |

### Q05

The shorter 1500 s exposure should stop closer to the target-yield maximum: conversion may not be fully complete, but substantially less target should undergo secondary loss. This is predicted to be among the best chemical outcomes in the query set.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2400 | 0.1400 | 0.3500 |
| conversion | 0.9510 | 0.8600 | 0.9950 |
| safety_risk | 0.1300 | 0.0600 | 0.2400 |
| score | 0.4200 | 0.2900 | 0.5500 |
| selectivity | 0.7200 | 0.6100 | 0.8100 |
| yield | 0.6800 | 0.5500 | 0.7900 |

### Q06

The additional hot residence should add almost no useful conversion after reactant depletion but should continue destroying target and increasing byproduct signal, following the strong Batch 9 to Batch 11 time effect.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5200 | 0.3800 | 0.6700 |
| conversion | 0.9990 | 0.9870 | 1.0000 |
| safety_risk | 0.1700 | 0.0800 | 0.3000 |
| score | 0.1400 | 0.0500 | 0.2700 |
| selectivity | 0.4200 | 0.2800 | 0.5600 |
| yield | 0.4100 | 0.2600 | 0.5600 |

### Q07

The 390 K stage should form substantial target before the subsequent 450 K stage completes conversion and accelerates target loss. Ending at the higher target also supports a relatively high terminal risk estimate.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4200 | 0.2900 | 0.5600 |
| conversion | 0.9970 | 0.9700 | 1.0000 |
| safety_risk | 0.2000 | 0.0900 | 0.3500 |
| score | 0.2000 | 0.0900 | 0.3400 |
| selectivity | 0.5100 | 0.3700 | 0.6400 |
| yield | 0.5000 | 0.3500 | 0.6400 |

### Q08

The integrated chemical exposure is similar to Q07, so the chemical prediction is close. Cooling toward 390 K in the second stage should lower terminal risk and may modestly preserve target, although order effects are poorly identified by my experiments.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4000 | 0.2700 | 0.5400 |
| conversion | 0.9970 | 0.9700 | 1.0000 |
| safety_risk | 0.1400 | 0.0600 | 0.2700 |
| score | 0.2500 | 0.1300 | 0.3900 |
| selectivity | 0.5400 | 0.4000 | 0.6700 |
| yield | 0.5300 | 0.3800 | 0.6700 |

### Q09

A short 440 K treatment should deliver high conversion rapidly while limiting, but not avoiding, secondary degradation. Its temperature makes it less selective and riskier than Q05.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3100 | 0.2000 | 0.4400 |
| conversion | 0.9790 | 0.9100 | 1.0000 |
| safety_risk | 0.1800 | 0.0800 | 0.3200 |
| score | 0.3200 | 0.1900 | 0.4600 |
| selectivity | 0.6400 | 0.5100 | 0.7500 |
| yield | 0.6100 | 0.4700 | 0.7400 |

### Q10

Quenching should leave conversion close to Q09 and may produce only a small yield difference, but it should reduce terminal thermal risk. The score estimate is therefore slightly higher than Q09.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3000 | 0.1900 | 0.4300 |
| conversion | 0.9790 | 0.9100 | 1.0000 |
| safety_risk | 0.1400 | 0.0600 | 0.2700 |
| score | 0.3500 | 0.2200 | 0.4900 |
| selectivity | 0.6500 | 0.5200 | 0.7600 |
| yield | 0.6200 | 0.4800 | 0.7500 |

### Q11

At 370 K, conversion should approach completion during 5700 s, especially at the higher catalyst concentration. However, the long residence should cause substantial target loss, as observed in the 3600 versus 7200 s comparison at 370 K.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4000 | 0.2800 | 0.5400 |
| conversion | 0.9950 | 0.9600 | 1.0000 |
| safety_risk | 0.1200 | 0.0500 | 0.2300 |
| score | 0.2700 | 0.1500 | 0.4000 |
| selectivity | 0.5600 | 0.4300 | 0.6800 |
| yield | 0.5500 | 0.4100 | 0.6800 |

### Q12

This combines the highest temperature with the longest residence. Conversion should be complete, but extensive post-formation degradation is expected to leave little target and a large byproduct signal. This is the most uncertain extrapolation and has the widest risk and composition intervals.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6600 | 0.4900 | 0.8400 |
| conversion | 1.0000 | 0.9930 | 1.0000 |
| safety_risk | 0.3000 | 0.1500 | 0.5000 |
| score | 0.0200 | 0.0000 | 0.0900 |
| selectivity | 0.1600 | 0.0400 | 0.3100 |
| yield | 0.1600 | 0.0300 | 0.3200 |

## K2 — Retrospective analysis

1. Initial information: supported, contradicted, or untested claims

The initial material packet did not provide a substantive reaction mechanism, kinetic law, nominal catalyst ranking, or solvent-performance claim. It explicitly said that no task-specific property dossier was supplied and that experimental evidence was authoritative. It also warned that catalyst identities were anonymous and that the named solvents entered this reaction world through categorical benchmark effects rather than validated real-solvent property correlations. Consequently, there was no detailed initial mechanistic theory to confirm or refute.

Several framing claims were respected but not independently tested. The campaign did show large catalyst and solvent category effects, consistent with the packet's statement that these selections have latent categorical activity profiles. However, observing such effects does not validate the hidden mapping or prove that the supplied category descriptions are complete. Similarly, I found no evidence contradicting the synthetic-instrument calibration contract, but I did not perform standards, blanks, or independent calibration experiments; this is absence of detected contradiction, not experimental validation.

The warning against importing ordinary real-solvent intuition remained important. For example, Batches 2, 5, 6, and 7 established empirical differences among water, ethanol, acetonitrile, and toluene, but nothing in those results identifies polarity, boiling point, phase behavior, or another real-world solvent property as the cause. K1 correctly retained the effects as categorical.

All completed batches stayed below the stated safety limit of 0.35, but that only demonstrates feasibility for the 12 tested recipes. It does not establish that the untested operating space is safe. No initial claim about global safety was tested.

I do not identify an initial mechanistic claim for which clear counterevidence appeared and was consciously left uncorrected. Instead, the mechanism was constructed during the campaign. There were, however, early implicit assumptions—especially that one hour of heating would be a useful baseline, that maximum allowed catalyst and reagent loading would be informative, and that 600 rpm would avoid transport limitations—that were never directly tested. Their survival should be understood as lack of a test, not support.

2. Experiments that formed or changed the judgments

Batch 1 established the first baseline: Catalyst A in water at a 350 K target for 3600 s gave only 0.388 conversion and 0.252 yield. The condition itself was a largely unvalidated design choice rather than a conclusion from prior data.

Batches 2–4 genuinely changed the catalyst judgment because they held solvent, target temperature, duration, loading, and stirring fixed. Batch 2 showed that Catalyst B raised conversion to 0.553 and yield to 0.427 while retaining 0.774 selectivity. Catalysts C and D did not match that combination. This was the basis for K1's restricted statement that “Catalyst B was therefore the best of the tested catalysts under the common water condition.” It did not demonstrate that B is best in every solvent or temperature because catalyst–solvent and catalyst–temperature interactions were not crossed.

Batches 5–7 changed the solvent judgment. With Catalyst B at the common 350 K/3600 s setting, acetonitrile and toluene produced much higher conversion than water, while ethanol produced worse selectivity. Batch 7 gave 0.625 yield and 0.753 selectivity, leading to the data-driven choice of the Catalyst B/toluene combination for the temperature series. This was an optimization-guided pivot, although the one-factor design also supplied mechanistic evidence that solvent affects pathway partitioning rather than only overall rate.

Batches 8–10 established the temperature trend. From 330 to 390 K, conversion increased from 0.683 to 0.956 and yield from 0.525 to 0.692, while degradation warning increased from 0.034 to 0.158 and selectivity fell at 390 K. These observations changed the account from a single desired thermally accelerated reaction to competing thermally activated processes.

Batch 11 was the most important mechanism-changing experiment. Extending the 370 K condition from 3600 s in Batch 9 to 7200 s increased conversion from 0.922 to 0.994 but reduced yield from 0.675 to 0.575 and selectivity from 0.746 to 0.583. Byproduct and degradation signals rose substantially. This drove K1's central judgment that a stable-target parallel-reaction model was inadequate and that secondary target loss or a time-dependent selectivity change was needed.

Batch 12 principally changed the operational, not chemical, judgment. Its quench lowered temperature by 45 K and risk by about 0.0178, while its final chemical values were close to those of unquenched Batch 9. This supported K1's cautious statement that quenching “chiefly affects the thermal/safety state” and did not justify a confident claim of improved chemical yield.

Several important design choices remained guess-based. These included using the maximum permitted reagent, catalyst, and solvent quantities; fixing 600 rpm; always adding solvent, reagent, and catalyst in the same order; using only one intermediate measurement per batch; and treating one-hour heating as the initial reference duration. The later selection of 330, 370, and 390 K was informed by prior results, but the exact spacing was still a design judgment rather than an estimated optimum.

3. Principal competing mechanisms and what can be distinguished

K1's preferred explanation was “competing pseudo-first-order reactant consumption combined with secondary target loss.” In its simplest form, reactant R forms target P or byproduct B, and P subsequently enters a degradation channel D. That explanation remains economical because it accounts for increasing conversion together with declining target yield during prolonged heating.

The main competing explanations are:

- Direct target degradation: R forms P and B in parallel, followed by P converting to D or B.
- Time-dependent branching: the catalyst or reaction medium evolves so that early conversion favors P and late conversion favors B, without necessarily consuming previously formed P.
- Catalyst deactivation or transformation: total catalyst activity or catalytic selectivity changes with time. Pure activity loss alone does not readily explain a falling accumulated target yield, but selective deactivation combined with another pathway could.
- Reversible target formation or thermal equilibration: P could return to R or another pool and then be converted to byproduct.
- Thermal-history effects: nominal target temperature may be an incomplete descriptor, and different heat-up trajectories could change both conversion and degradation.
- Transport or phase effects: solvent category and stirring might alter effective rates through mixing, mass transfer, or phase behavior rather than intrinsic kinetics.
- Observation-model effects: byproduct and degradation channels are proxies with independent calibration and noise; changes in their signals need not correspond to a single conserved chemical network.

The experiments do distinguish some broad classes. Batch 11 provides evidence against a model in which P is a stable terminal product and all selectivity is fixed at the moment R reacts. The nearly identical apparent reactant-disappearance constants inferred from Batches 9 and 11 support approximately first-order disappearance over that interval and provide no strong evidence that gross conversion was stopped by severe deactivation.

They do not distinguish P-to-D from P-to-B, late selective conversion of residual R, reversible chemistry, or a catalyst-state change. The endpoint measurements also cannot separate intrinsic temperature dependence from integrated heat-up history. Catalyst–solvent interactions, reaction order, catalyst saturation, and mass-transfer limitation remain unidentified because the campaign did not vary loading, concentration, or stirring.

4. The single additional complete experiment I would choose

I would run Catalyst B in toluene with the campaign-standard quantities—0.080 L solvent, 0.040 mol reagent, and 0.005 mol catalyst—at 600 rpm. I would heat to a 370 K target for 3600 s, take the single allowed intermediate HPLC measurement, then heat for another 3600 s at the same target, terminate, and obtain the required final assay.

This is deliberately a within-vessel time-course test corresponding to the separate Batch 9 and Batch 11 conditions. It would reduce batch-to-batch formulation variability and directly ask whether already accumulated target declines during the second hot interval. The HPLC and final assay would still be different instruments, so the test would not eliminate all measurement-model uncertainty, but the existing cross-instrument behavior could be used when judging whether a change is materially larger than noise.

Possible outcomes would change the interpretation as follows:

- If target yield clearly fell while byproduct or degradation rose, secondary loss of accumulated P would receive substantially stronger support.
- If conversion rose but target amount stayed approximately constant while byproduct rose, late residual-reactant conversion into B would become more plausible than extensive destruction of P.
- If conversion and target both rose proportionally, the Batch 9/11 yield decline would look more like batch variability or an inadequately controlled thermal-history effect, weakening K1's sequential-loss conclusion.
- If conversion, target, and byproduct all changed very little during the second interval, catalyst deactivation, reactant exhaustion, or rapid approach to a stationary state would become more important.
- If the result depended strongly on the second heat operation's temperature response, that would emphasize thermal path dependence and show that nominally concatenating two heat operations is not equivalent to one continuous 7200 s operation.

I would not use this one opportunity merely to repeat the highest-scoring recipe, because the unresolved distinction between product destruction and time-dependent branching is more consequential for a predictive mechanism.

5. Tradeoff between identifiability and operational score

The early catalyst and solvent sweeps favored identifiability: Batches 1–4 and 2/5–7 changed one categorical factor at a time under otherwise common conditions. Their limitation is that they sampled only main effects and gave no catalyst–solvent interaction matrix.

After Batch 7, the design shifted toward the empirically promising Catalyst B/toluene region. Batches 8–10 served both purposes: they mapped a temperature trend while also searching for better yield and score. This was efficient, but it meant that temperature dependence was characterized only for one catalyst–solvent combination.

Batch 11 sacrificed operational score for mechanistic information. Its score was about 0.272, below the roughly 0.347 score of Batch 9, but the long residence exposed the late-yield-loss phenomenon that became central to K1. This was the clearest instance in which the research goal overrode short-term optimization.

Batch 12 moved back toward operational optimization and safety. It tested quenching at the strong 370 K condition and produced the sample-in highest score of 0.351. It also formed a useful, though unreplicated, comparison with Batch 9. Thus it was not purely exploitative.

Optimization did reduce identifiability in several ways. I repeatedly used maximum catalyst loading despite the visible high-cost flag, did not include a catalyst-free blank, did not vary catalyst dosage, and did not test whether 600 rpm was transport-independent. Once Catalyst B and toluene looked favorable, most remaining resources were concentrated there rather than allocated to interaction tests or replicates. Conversely, Batch 11 knowingly accepted a worse score to investigate time dependence.

The stated research goal appropriately pushed the campaign beyond simply maximizing the public score. Nevertheless, the final design still reflects a compromise: it identified a useful operating neighborhood and a plausible dynamic mechanism, but not a uniquely estimable kinetic model.

6. Underused evidence and weaknesses in the blind predictions

The processed estimates were used much more heavily than the raw characterization artifacts. Peak assignments and spectral shapes could potentially have been compared across time and temperature for evidence of whether the same byproduct/degradation features grew consistently. I did not perform that systematic comparison.

The full set of paired intermediate HPLC and final-assay results was also underused. A hierarchical comparison across all 12 batches might have estimated systematic instrument offsets, termination effects, and within-recipe process variability. Instead, K1 discussed selected pairs qualitatively. That limitation is especially important for the quench conclusion and for interpreting whether small HPLC-to-final changes were chemical or instrumental.

The operation-level risk and temperature deltas contained more information than was incorporated into a quantitative model. In particular, the blind queries used much smaller material inventories than the campaign. I had not measured how safety risk scales with solvent volume, reagent amount, catalyst amount, or concentration. Therefore, the safety predictions relied on an uncertain compromise between amount scaling and formulation/temperature scaling.

The apparent first-order conversion constants were useful, but I did not fit a joint kinetic model with parameter uncertainty, solvent-specific temperature dependence, catalyst-loading dependence, or thermal lag. The blind predictions nevertheless transferred the toluene temperature trend to acetonitrile and assumed that the higher catalyst concentration would accelerate conversion. Those assumptions were explicitly untested.

The least reliable blind prediction was Q12: 460 K for 6300 s was far outside K1's tested 330–390 K temperature range and beyond the tested duration at such a high temperature. Although its yield, selectivity, byproduct, safety, and score intervals were wide, the conversion interval of 0.993–1.000 was probably too narrow given possible deactivation, phase changes, transport effects, or unmodeled thermal behavior.

Q04 at 450 K for 3300 s and Q06 at 420 K for 5100 s were also highly extrapolative. Q07 and Q08 were particularly uncertain because the campaign never reversed two-stage temperature programs; their predicted order effects and terminal-risk difference depended on guessed thermal memory. Q01/Q02 and Q09/Q10 depended on the assumption that quenching changes risk much more than chemistry, supported only by the single Batch 9/12 comparison.

The Q03 and Q05 chemical intervals may also have been too narrow. They transferred a temperature law obtained mainly in Catalyst B/toluene to Catalyst B/acetonitrile, changed catalyst concentration, changed reagent concentration, and reduced stirring from 600 to 400 rpm simultaneously. K1 had explicitly said that extrapolation outside fixed loading, concentration, mixing, and 330–390 K was speculative. The rationales acknowledged those changes, but several high-conversion intervals conveyed more confidence than that scope statement warranted.

Score predictions were additionally fragile because the exact reaction-score mapping was not identified from the campaign. Predicting score from yield, selectivity, byproduct, and risk was therefore a secondary model layered on top of the chemical extrapolation. Safety-risk and score intervals across almost all queries could reasonably have been wider.

7. Limitations of the sealed recommendation

Batch 12 was the sample-in highest-scoring completed experiment, not a proven optimum. Its score of 0.3512 exceeded Batch 9's 0.3466 by only about 0.0046. With no replicate batches and known assay/process uncertainty, that difference is not persuasive evidence that the quench recipe has a higher expected score rather than a favorable realization.

The recommendation was also objective-dependent. Batch 10 had the highest observed chemical yield, approximately 0.692, whereas Batch 12 was recommended because it combined high yield with prompt risk reduction and the highest observed safe score. A user prioritizing maximum chemical yield, selectivity, cost, or minimum degradation could choose differently.

Repeatability should be tested by randomized replicated executions of Batch 12 and the unquenched Batch 9 condition, ideally enough replicates to estimate process variance and the distribution of their score difference. The quench should be characterized by actual timing and temperature trajectory rather than only the nominal operation.

Local robustness should be evaluated with a compact response-surface design around the recommendation: approximately ±10 K, shorter and longer residence times around 3600 s, modest catalyst-loading changes, and controlled quench delays. Stirring should also be varied to check transport independence. A robust recommendation would retain acceptable yield, selectivity, and risk under these perturbations rather than depend on a narrow point optimum.

Material robustness would require crossing Catalyst B with both toluene and acetonitrile near the proposed operating region and checking at least one alternative catalyst. Because the materials are anonymous categorical formulations, success with Catalyst B/toluene cannot be generalized through ordinary chemical identity arguments.

Cross-world generalization is even less established. The recommendation is tied to this synthetic world's hidden categorical couplings, instrument contracts, scoring rule, and thermal response. It should not be presented as a transferable real-chemistry recipe or assumed optimal in another benchmark world without new calibration.

Accordingly, the strongest defensible statement is: Batch 12 was the best observed safe-score realization among the 12 sampled conditions and is a reasonable candidate for replication. It has not been proven globally optimal, locally optimal in expectation, statistically superior to Batch 9, or transferable across materials or worlds.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 139.6 | none | 0 |
| Q | yes | 0 | 159.2 | none | 0 |
| K2 | yes | 0 | 124.4 | none | 0 |

## Scope note

This report contains only information available before truth release. Reference truth, prediction scoring, and recommendation retests are intentionally absent because the full 60-task block has not yet completed.
