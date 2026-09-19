# RX-W05--S--mechanism_discovery--Aligned

## Run summary

- World: `RX-W05`
- Locus: `S`
- Goal: `mechanism_discovery`
- Arm: `Aligned`
- Status: `completed`
- Source status: `completed`
- Experimental sessions: `12/12`
- Operations: `86`
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
- Rationale: Batch 12 gave the highest observed target yield and campaign score while remaining below the safety limit; its prompt quench also tested and limited post-heating thermal exposure.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S0 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.3584 | 0.7768 | 0.4558 | 0.1183 | 0.0110 | 0.1199 | 0.2292 |
| 2 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.4623 | 0.8036 | 0.5730 | 0.1169 | 0.0181 | 0.1309 | 0.2842 |
| 3 | S0 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.2713 | 0.6467 | 0.4399 | 0.1556 | 0.0097 | 0.1107 | 0.1644 |
| 4 | S0 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.5314 | 0.8438 | 0.6418 | 0.1134 | 0.0484 | 0.1385 | 0.3254 |
| 5 | S1 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.5038 | 0.7935 | 0.6446 | 0.1294 | 0.0875 | 0.1629 | 0.2910 |
| 6 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.6075 | 0.8086 | 0.7759 | 0.1672 | 0.0903 | 0.1913 | 0.3367 |
| 7 | S3 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.4422 | 0.6855 | 0.6501 | 0.2092 | 0.0985 | 0.1891 | 0.2282 |
| 8 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 325 K x 3600 s @ 600 rpm | no | 0.4613 | 0.8122 | 0.5627 | 0.1067 | 0.0369 | 0.1687 | 0.2679 |
| 9 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 375 K x 3600 s @ 600 rpm | no | 0.6869 | 0.7676 | 0.8837 | 0.2018 | 0.1379 | 0.2189 | 0.3565 |
| 10 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 900 s @ 600 rpm | no | 0.2445 | 0.9084 | 0.2725 | 0.0299 | 0.0073 | 0.1462 | 0.1864 |
| 11 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 1800 s @ 600 rpm → 350 K x 5400 s @ 600 rpm | no | 0.6308 | 0.6692 | 0.9488 | 0.3160 | 0.2373 | 0.2056 | 0.3220 |
| 12 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 375 K x 3600 s @ 600 rpm | yes | 0.7046 | 0.7801 | 0.8808 | 0.2127 | 0.1235 | 0.1985 | 0.3756 |

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
    "byproduct_signal": 0.11833697557449341,
    "conversion": 0.45584824681282043,
    "cost": 1.0,
    "degradation_warning": 0.011042878963053226,
    "safety_risk": 0.11989310383796692,
    "score": 0.2291993349790573,
    "selectivity": 0.7767558693885803,
    "virtual_spectrum_summary": 0.07005462795495987,
    "yield": 0.35844361782073975
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
    "byproduct_signal": 0.11689881980419159,
    "conversion": 0.5729913115501404,
    "cost": 1.0,
    "degradation_warning": 0.018113380298018456,
    "safety_risk": 0.1309013068675995,
    "score": 0.28422603011131287,
    "selectivity": 0.8036028146743774,
    "virtual_spectrum_summary": 0.07244537025690079,
    "yield": 0.4623294472694397
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
    "byproduct_signal": 0.15559612214565277,
    "conversion": 0.4398760199546814,
    "cost": 1.0,
    "degradation_warning": 0.009722239337861538,
    "safety_risk": 0.11065579950809479,
    "score": 0.16440531611442566,
    "selectivity": 0.6466922760009766,
    "virtual_spectrum_summary": 0.08995287865400314,
    "yield": 0.27134940028190613
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
    "byproduct_signal": 0.11337291449308395,
    "conversion": 0.6417669653892517,
    "cost": 1.0,
    "degradation_warning": 0.048361945897340775,
    "safety_risk": 0.13849443197250366,
    "score": 0.32535696029663086,
    "selectivity": 0.8438451290130615,
    "virtual_spectrum_summary": 0.08411797881126404,
    "yield": 0.5313537120819092
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
    "byproduct_signal": 0.1294461041688919,
    "conversion": 0.6445534229278564,
    "cost": 1.0,
    "degradation_warning": 0.08746542781591415,
    "safety_risk": 0.16294914484024048,
    "score": 0.29101186990737915,
    "selectivity": 0.7934861183166504,
    "virtual_spectrum_summary": 0.11055479943752289,
    "yield": 0.5037803053855896
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
    "byproduct_signal": 0.16718417406082153,
    "conversion": 0.7758628129959106,
    "cost": 1.0,
    "degradation_warning": 0.0902695506811142,
    "safety_risk": 0.19127100706100464,
    "score": 0.3366634249687195,
    "selectivity": 0.8085913062095642,
    "virtual_spectrum_summary": 0.13257259130477905,
    "yield": 0.6075031757354736
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
    "byproduct_signal": 0.20923945307731628,
    "conversion": 0.6500768065452576,
    "cost": 1.0,
    "degradation_warning": 0.09851149469614029,
    "safety_risk": 0.1891244351863861,
    "score": 0.22815044224262238,
    "selectivity": 0.6855480670928955,
    "virtual_spectrum_summary": 0.15941187739372253,
    "yield": 0.4421543478965759
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
      "target_temperature_K": 325
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
    "byproduct_signal": 0.10674566775560379,
    "conversion": 0.5627374649047852,
    "cost": 1.0,
    "degradation_warning": 0.036862388253211975,
    "safety_risk": 0.16868431866168976,
    "score": 0.26793381571769714,
    "selectivity": 0.8122386336326599,
    "virtual_spectrum_summary": 0.07529819011688232,
    "yield": 0.46127083897590637
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
  "end_step": 63,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.20181521773338318,
    "conversion": 0.8837167620658875,
    "cost": 1.0,
    "degradation_warning": 0.13789798319339752,
    "safety_risk": 0.21894864737987518,
    "score": 0.3565032184123993,
    "selectivity": 0.7675544023513794,
    "virtual_spectrum_summary": 0.17305245995521545,
    "yield": 0.6869246363639832
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
      "duration_s": 900,
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
  "end_step": 70,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.029868818819522858,
    "conversion": 0.27246707677841187,
    "cost": 1.0,
    "degradation_warning": 0.007316070608794689,
    "safety_risk": 0.14620189368724823,
    "score": 0.18637122213840485,
    "selectivity": 0.9084110856056213,
    "virtual_spectrum_summary": 0.019720083102583885,
    "yield": 0.24453148245811462
  },
  "ordinal": 10
}
```

### Batch 11

Lifecycle index: `11`; end step: `78`.

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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 350
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 5400,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 350
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 78,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.31604433059692383,
    "conversion": 0.9487720727920532,
    "cost": 1.0,
    "degradation_warning": 0.23727205395698547,
    "safety_risk": 0.20560729503631592,
    "score": 0.3219800889492035,
    "selectivity": 0.6692448258399963,
    "virtual_spectrum_summary": 0.2805967926979065,
    "yield": 0.6307874321937561
  },
  "ordinal": 11
}
```

### Batch 12

Lifecycle index: `12`; end step: `86`.

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
      "operation": "quench"
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
  "end_step": 86,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.21271003782749176,
    "conversion": 0.8807587623596191,
    "cost": 1.0,
    "degradation_warning": 0.1235312968492508,
    "safety_risk": 0.1984744668006897,
    "score": 0.3756158947944641,
    "selectivity": 0.7801063656806946,
    "virtual_spectrum_summary": 0.1725796014070511,
    "yield": 0.7045673727989197
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

1. Scope and experimental basis

This report concerns only the anonymous synthetic benchmark reaction world. It does not assign real chemical identities to the reagent, catalysts, target, byproduct, or degradation product. Each of the 12 batches used 0.040 mol reagent, 0.080 L of one solvent, 0.005 mol catalyst, and 600 rpm stirring. Thus, the campaign identifies effects within that single concentration, catalyst-loading, volume, and mixing regime; it does not independently identify reaction orders in reagent or catalyst.

All reported terminal compositions below are final-assay observations. Yield, conversion, and selectivity are separately calibrated channels, so I treat approximate relations such as yield ≈ conversion × selectivity as useful consistency checks rather than exact accounting identities.

2. Main observations

Catalyst comparison in water at a commanded 350 K for 3600 s:

- Batch 1, Catalyst A: conversion 0.45585, selectivity 0.77676, yield 0.35844, byproduct 0.11834, degradation warning 0.01104, risk 0.11989.
- Batch 2, Catalyst B: conversion 0.57299, selectivity 0.80360, yield 0.46233, byproduct 0.11690, degradation warning 0.01811, risk 0.13090.
- Batch 3, Catalyst C: conversion 0.43988, selectivity 0.64669, yield 0.27135, byproduct 0.15560, degradation warning 0.00972, risk 0.11066.
- Batch 4, Catalyst D: conversion 0.64177, selectivity 0.84385, yield 0.53135, byproduct 0.11337, degradation warning 0.04836, risk 0.13849.

The catalyst ranking is therefore not merely an activity ranking. Catalyst D was both the fastest and most target-selective catalyst under this condition. Catalyst C had conversion similar to A but much poorer selectivity and more byproduct, indicating a catalyst-dependent branching ratio. D also produced a larger degradation warning than A–C, plausibly because it formed more target or other labile material during the same interval.

Solvent comparison with Catalyst D at commanded 350 K for 3600 s:

- Batch 4, water: conversion 0.64177, selectivity 0.84385, yield 0.53135, byproduct 0.11337, degradation 0.04836.
- Batch 5, ethanol: conversion 0.64455, selectivity 0.79349, yield 0.50378, byproduct 0.12945, degradation 0.08747.
- Batch 6, acetonitrile: conversion 0.77586, selectivity 0.80859, yield 0.60750, byproduct 0.16718, degradation 0.09027.
- Batch 7, toluene: conversion 0.65008, selectivity 0.68555, yield 0.44215, byproduct 0.20924, degradation 0.09851.

Acetonitrile gave the greatest conversion and yield. Water gave the best selectivity and lowest degradation among these Catalyst D experiments. Toluene strongly favored non-target material. Consequently, solvent changes affect at least two kinetic quantities: total disappearance of reactant and the partitioning of that disappearance among target and competing pathways. A single solvent multiplier on one overall rate constant cannot explain the full table.

Temperature series with Catalyst D in acetonitrile for 3600 s:

- Batch 8, 325 K command: conversion 0.56274, selectivity 0.81224, yield 0.46127, byproduct 0.10675, degradation 0.03686, risk 0.16868.
- Batch 6, 350 K command: conversion 0.77586, selectivity 0.80859, yield 0.60750, byproduct 0.16718, degradation 0.09027, risk 0.19127.
- Batch 9, 375 K command: conversion 0.88372, selectivity 0.76755, yield 0.68692, byproduct 0.20182, degradation 0.13790, risk 0.21895.

Temperature accelerated conversion, but it accelerated byproduct formation and degradation sufficiently that selectivity fell at the highest temperature. Yield nevertheless continued to increase through 375 K over the tested 3600 s interval because the conversion gain exceeded the selectivity loss.

The thermal state did not instantaneously equal the command. Reported temperature changes after 3600 s were +26.21 K for the 325 K command, about +49.1 K for 350 K commands, and +70.94 K for 375 K commands. These observations are consistent with a finite thermal response from an approximately ambient initial state. They show why commanded temperature should not be treated as the complete thermal history.

Time series with Catalyst D in acetonitrile near 350 K:

- Batch 10, 900 s final assay: conversion 0.27247, selectivity 0.90841, yield 0.24453, byproduct 0.02987, degradation 0.00732.
- Batch 11, 1800 s intermediate HPLC: conversion 0.49477, selectivity 0.85153, yield 0.44097, byproduct 0.05287.
- Batch 6, 3600 s final assay: conversion 0.77586, selectivity 0.80859, yield 0.60750, byproduct 0.16718, degradation 0.09027.
- Batch 11, 7200 s final assay after an additional 5400 s heat segment: conversion 0.94877, selectivity 0.66924, yield 0.63079, byproduct 0.31604, degradation 0.23727.

Longer heating drove conversion toward completion but progressively sacrificed selectivity. Yield rose steeply at first, then only from 0.6075 at 3600 s to 0.6308 at 7200 s while degradation and byproduct signals rose substantially. This is evidence for a finite optimal stopping region for target recovery, rather than a rule that maximum conversion is automatically best.

3. Compact kinetic account

The simplest mechanism consistent with the observations is a branched primary reaction plus secondary loss:

R → P with rate kP a R
R → B with rate kB a R
P → D with rate kD P

Here R is the public reactant, P the target, B a competing byproduct pool, D a degradation pool, and a is the fraction or effectiveness of active catalyst. A useful differential representation is:

dR/dt = -a(kP + kB)R
dP/dt = a kP R - kD P
dB/dt = a kB R
dD/dt = kD P

The rate constants should be indexed by catalyst, solvent, and temperature. For example:

ki = Ai × Fcatalyst,i × Fsolvent,i × exp[-Ei/(RT)]

This factorization is only a convenient local parameterization; the data do not prove that catalyst and solvent effects are separable.

For Catalyst D in acetonitrile near 350 K, treating conversion alone as pseudo-first-order gives kapp = -ln(1-X)/t. The estimates are 3.53×10^-4 s^-1 at 900 s, 3.79×10^-4 s^-1 at 1800 s, 4.15×10^-4 s^-1 at 3600 s, and 4.13×10^-4 s^-1 at 7200 s. Their closeness is notable: reactant disappearance is well approximated by a pseudo-first-order law over the observed time range even though product selectivity is changing.

Using the 325, 350, and 375 K commands with the 3600 s conversions gives descriptive kapp values of 2.30×10^-4, 4.15×10^-4, and 5.98×10^-4 s^-1. A three-point Arrhenius regression against nominal commanded temperature gives an apparent activation energy of approximately 19 kJ mol^-1. This is an empirical local summary, not a transferable molecular activation barrier: actual temperatures lagged the commands, and selectivity-changing pathways are folded into the conversion-derived rate.

The decline in selectivity from 0.908 at 900 s to 0.669 at 7200 s requires either a growing competing branch, secondary destruction of target, or both. The simultaneous increase in degradation warning from 0.0073 to 0.2373 supports secondary target or product-pool degradation. The increasing byproduct signal also supports a direct or delayed competing route. The measurements do not uniquely allocate all lost selectivity between those two processes.

4. Thermal and safety coupling

A plausible thermal state equation is:

Ceff dT/dt = UA(Tset - T) + Qrxn[-dR/dt] - Qloss(T,Tambient)

The finite temperature increments show appreciable thermal lag. Catalyst identity also changed heat-associated risk under otherwise matched water conditions: the heat-step risk increments were approximately 0.0477 for A, 0.0587 for B, 0.0385 for C, and 0.0663 for D. This ordering broadly follows activity better than it follows final selectivity, consistent with reaction-rate or formulation-dependent thermal burden. It does not by itself prove measurable self-heating because the public risk channel can combine several benchmark hazards.

At 375 K, Batch 12's heat step added 0.10536 risk. Quenching then reduced the reported temperature by 45 K over 54.85 s and changed risk by -0.02047. Thus, quench is a dynamic cooling operation rather than a zero-time logical flag. In a predictive process model, the kinetic equations should continue to integrate during those 54.85 s using the falling temperature.

All final observed risks remained below the task limit of 0.35. Risk nevertheless rose with temperature and depended on solvent and catalyst, so safety cannot be inferred from conversion alone.

5. Evidence about termination and quench timing

Batches 9 and 12 were the closest comparison of termination handling. Both used Catalyst D, acetonitrile, a 375 K command, and 3600 s heating. Batch 9 was terminated without an explicit quench; Batch 12 was quenched before post-quench HPLC and termination.

- Batch 9 final assay: conversion 0.88372, selectivity 0.76755, yield 0.68692, degradation 0.13790.
- Batch 12 post-quench HPLC: conversion 0.89567, selectivity 0.78258, yield 0.71052, byproduct 0.19062.
- Batch 12 final assay: conversion 0.88076, selectivity 0.78011, yield 0.70457, degradation 0.12353.

The quenched batch had almost unchanged conversion but modestly higher final yield and selectivity and lower degradation warning. This direction is consistent with quench suppressing continued hot degradation. However, there was only one batch per handling mode, and the differences are modest relative to assay uncertainty. Therefore I regard quench protection as supported but not conclusively quantified. I do not claim that quench chemically changes the branching mechanism; rapid cooling alone is sufficient to explain the result.

Batch 12 produced the highest observed yield, 0.70457, and campaign score, 0.37562, at risk 0.19847. Batch 9, without quench, had score 0.35650. The score was a secondary observation and was not used as a mechanistic species measurement.

6. Catalyst deactivation

A catalyst-deactivation extension would be:

da/dt = -kdeact a,

possibly with kdeact increasing with temperature or product concentration. Strong deactivation is not required to explain reactant disappearance: the nearly constant pseudo-first-order kapp estimates through 7200 s argue against rapid loss of Catalyst D activity under the 350 K/acetonitrile condition. Nevertheless, deactivation remains possible because conversion approaches saturation and no independent active-catalyst measurement was available.

The pronounced selectivity loss at long time is better supported as secondary degradation or changing pathway competition than as simple deactivation. Pure nonselective deactivation would slow both desired and undesired primary routes without necessarily producing the observed increases in byproduct and degradation signals. Selective deactivation of the target-forming catalytic state, leaving a byproduct-forming state active, is a viable but more complex competing explanation.

7. How the explanation developed

The initial Batch 1 observation established moderate conversion and target preference rather than complete or purely selective conversion. Batches 2–4 changed the interpretation from a single universal catalyst rate to catalyst-specific activity and branching, particularly because Catalyst C was both less selective and more byproduct-prone while Catalyst D improved both conversion and selectivity.

Batches 5–7 then showed that solvent affects conversion and branching independently: acetonitrile accelerated conversion, water preserved selectivity, and toluene promoted the competing signal. This required separate solvent dependence for kP, kB, and probably kD.

Batches 8 and 9 established a temperature trade-off: conversion increased monotonically across the tested range, while selectivity and degradation worsened at high temperature. Batches 10 and 11 added time resolution and showed that a simple pseudo-first-order expression describes total conversion surprisingly well, but cannot describe product distribution without secondary or time-dependent terms. Finally, Batch 12 showed the direction and timescale of quench effects and supported explicit integration over real thermal history rather than treating termination as instantaneous.

8. Competing explanations

Several alternatives remain observationally equivalent or partly equivalent:

- Parallel-only model: R forms target and byproduct in parallel, with different temperature dependences. A time-varying apparent branching ratio could arise from thermal transients without P → D. The degradation-warning increase makes this less economical but does not eliminate it.
- Consecutive model: R → P → B or D. This naturally explains high early selectivity and later loss, but the assays do not reveal whether the measured byproduct is formed directly from R, from P, or through both routes.
- Catalyst-state model: active catalyst converts into another state that is more byproduct-selective. This can mimic secondary product degradation.
- Reversible target formation: the supplied structural prior suggested effective irreversibility, and no cooling or waiting experiment demonstrated return to reactant. Reversibility is therefore unnecessary on the tested support, but it was not directly excluded by an equilibrium experiment.
- Instrument/process discrepancy: intermediate HPLC and final assay sometimes differed slightly even without much deliberate reaction time between them. Calibration noise, sampling, termination, and short residual evolution can all contribute. Small cross-instrument differences should not be overinterpreted as kinetics.

9. Identifiability limits and applicability

The account is calibrated only for 0.040 mol reagent, 0.005 mol catalyst, approximately 0.080 L solvent, 600 rpm, commanded temperatures of 325–375 K for the main comparative set, and times of 900–7200 s. It should not be extrapolated confidently to the legal extremes of 250 or 470 K, other catalyst loadings, other reagent concentrations, different stirring, mixed solvents, or larger scale.

There were no catalyst-free, reagent-free, or heat-free controls; no true replicate batches; no independent measurement of catalyst activity; and no direct concentration-resolved mass balance for named molecular species. Consequently, reaction orders, individual elementary constants, activation energies for separate branches, heat of reaction, catalyst-deactivation constants, and the chemical identity of degradation products are not identifiable.

Solvent and catalyst were screened sequentially rather than in a full factorial design. Catalyst rankings demonstrated in water may interact with solvent, and Catalyst D was the only catalyst studied across all solvents and temperatures. The apparent 19 kJ mol^-1 activation energy mixes thermal lag and multiple pathways. Quench benefit is based on a single matched pair and remains provisional.

10. Predictive interpretation within the tested domain

Within the observed domain, my preferred predictive algorithm is:

1. Propagate actual temperature with a first-order thermal response toward the command, including a reaction-associated risk or heat term.
2. At each time step, compute solvent-, catalyst-, and temperature-dependent kP, kB, and kD.
3. Integrate the branched/consecutive kinetic equations for R, P, B, and D.
4. If quench is invoked, integrate through the observed finite cooling trajectory rather than stopping rates instantly.
5. Map the terminal state to noisy assay channels, without forcing exact equality between yield and conversion × selectivity.

Qualitatively, this model predicts that Catalyst D in acetonitrile will maximize rate and target yield over the tested choices; water will preserve somewhat better selectivity; increasing temperature or time will raise conversion but eventually give diminishing or negative returns in target yield because byproduct and degradation pathways accumulate; and prompt quenching after the desired hot residence time will tend to preserve product. Those are interpolation-level conclusions supported by the campaign. Numerical predictions outside the tested loading, temperature, time, and mixing region would be extrapolations rather than established properties of the world.

## Q — Blind predictions

### Overall rationale

Predictions use the campaign-derived branched and consecutive model R to target, R to byproduct, and target to degradation. Catalyst B activity was anchored to Batch 2 and transferred to acetonitrile using the solvent effect measured with Catalyst D. Primary conversion was scaled approximately with catalyst concentration and with the campaign's apparent temperature dependence. Target degradation was assigned a stronger temperature dependence, consistent with Batches 6, 8, 9, 10, and 11. Byproduct signal was estimated mainly as converted material not remaining as target. Quench effects were based on the matched direction of Batches 9 and 12. Intervals are deliberately wide because catalyst-loading dependence, 410–465 K behavior, 0.005 L scale, 400 rpm mixing, and 14400 s residence lie partly or wholly outside the directly observed campaign domain.

### Q01

The low catalyst concentration limits conversion despite 410 K. The elevated temperature causes appreciable secondary loss during 1800 s, so selectivity is predicted below the early-time values observed near 350 K.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1470 | 0.0700 | 0.3000 |
| conversion | 0.4520 | 0.3000 | 0.6100 |
| safety_risk | 0.1400 | 0.0800 | 0.2300 |
| score | 0.2300 | 0.1200 | 0.3500 |
| selectivity | 0.6750 | 0.5200 | 0.8000 |
| yield | 0.3050 | 0.1800 | 0.4400 |

### Q02

Fourteen thousand four hundred seconds at 410 K should nearly exhaust reactant even at low catalyst loading. Extrapolating the observed time-dependent degradation predicts that most initially formed target is subsequently converted into non-target material.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9510 | 0.7000 | 1.0000 |
| conversion | 0.9920 | 0.9300 | 1.0000 |
| safety_risk | 0.2900 | 0.1800 | 0.4300 |
| score | 0.0100 | 0.0000 | 0.0800 |
| selectivity | 0.0410 | 0.0000 | 0.2400 |
| yield | 0.0410 | 0.0000 | 0.2300 |

### Q03

The high catalyst concentration makes primary conversion rapid, allowing high conversion and substantial target formation within 1800 s. Secondary degradation at 410 K still lowers selectivity relative to a cooler short-time batch.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3530 | 0.2000 | 0.5600 |
| conversion | 0.9260 | 0.7800 | 0.9900 |
| safety_risk | 0.2100 | 0.1300 | 0.3200 |
| score | 0.3100 | 0.1600 | 0.4600 |
| selectivity | 0.6190 | 0.4400 | 0.7600 |
| yield | 0.5730 | 0.3900 | 0.7100 |

### Q04

High catalyst loading should complete primary conversion early, after which prolonged residence at 410 K exposes nearly the entire target pool to degradation. This is an extrapolation well beyond the campaign's longest hot high-temperature condition.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9880 | 0.8500 | 1.0000 |
| conversion | 1.0000 | 0.9900 | 1.0000 |
| safety_risk | 0.4200 | 0.2700 | 0.6000 |
| score | 0.0020 | 0.0000 | 0.0400 |
| selectivity | 0.0120 | 0.0000 | 0.1500 |
| yield | 0.0120 | 0.0000 | 0.1400 |

### Q05

At 350 K the low catalyst concentration gives only moderate conversion after 7200 s. Degradation is slower than at 410–465 K, preserving a majority target fraction and keeping safety risk relatively low.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1860 | 0.0900 | 0.3400 |
| conversion | 0.5950 | 0.4200 | 0.7400 |
| safety_risk | 0.1000 | 0.0500 | 0.1800 |
| score | 0.3000 | 0.1700 | 0.4300 |
| selectivity | 0.6880 | 0.5500 | 0.8000 |
| yield | 0.4100 | 0.2700 | 0.5400 |

### Q06

Even low catalyst loading is predicted to give nearly complete conversion over 7200 s at 465 K. The target is expected to be thermally depleted, while the high temperature produces a substantial probability of exceeding the 0.35 safety limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9730 | 0.8000 | 1.0000 |
| conversion | 0.9910 | 0.9400 | 1.0000 |
| safety_risk | 0.4700 | 0.3100 | 0.6800 |
| score | 0.0020 | 0.0000 | 0.0500 |
| selectivity | 0.0180 | 0.0000 | 0.1800 |
| yield | 0.0180 | 0.0000 | 0.1700 |

### Q07

High catalyst loading at 350 K drives conversion close to completion. The cooler temperature preserves considerably more target than the corresponding 410 or 465 K long-duration conditions, although 7200 s still causes meaningful byproduct accumulation.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3700 | 0.2000 | 0.5800 |
| conversion | 0.9800 | 0.9200 | 1.0000 |
| safety_risk | 0.1400 | 0.0800 | 0.2400 |
| score | 0.3500 | 0.2000 | 0.4900 |
| selectivity | 0.6230 | 0.4700 | 0.7500 |
| yield | 0.6100 | 0.4500 | 0.7300 |

### Q08

This combines the fastest primary conversion with the most severe tested temperature-time exposure. Conversion should be complete, but essentially all target is predicted to undergo secondary loss; safety-limit violation is likely.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9980 | 0.9200 | 1.0000 |
| conversion | 1.0000 | 0.9950 | 1.0000 |
| safety_risk | 0.6600 | 0.4500 | 0.8600 |
| score | 0.0000 | 0.0000 | 0.0200 |
| selectivity | 0.0020 | 0.0000 | 0.0800 |
| yield | 0.0020 | 0.0000 | 0.0800 |

### Q09

The middle catalyst concentration should make conversion essentially complete at 410 K over 7200 s. The observed deterioration with residence time is extrapolated to leave only a modest target fraction at termination.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8550 | 0.6300 | 0.9700 |
| conversion | 0.9980 | 0.9800 | 1.0000 |
| safety_risk | 0.2900 | 0.1800 | 0.4300 |
| score | 0.0350 | 0.0000 | 0.1300 |
| selectivity | 0.1440 | 0.0400 | 0.3600 |
| yield | 0.1440 | 0.0400 | 0.3500 |

### Q10

The reaction state at the end of heating should resemble Q09. Quenching cannot reverse degradation already accumulated during 7200 s, but it should modestly preserve the remaining target and reduce post-heating thermal risk.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8400 | 0.6000 | 0.9600 |
| conversion | 0.9980 | 0.9800 | 1.0000 |
| safety_risk | 0.2500 | 0.1500 | 0.3900 |
| score | 0.0450 | 0.0050 | 0.1500 |
| selectivity | 0.1600 | 0.0500 | 0.3900 |
| yield | 0.1600 | 0.0500 | 0.3800 |

### Q11

At 350 K the middle catalyst loading should nearly exhaust reactant over 14400 s. The campaign's 7200 s result already showed substantial selectivity loss, so doubling the duration is predicted to reduce target yield despite the high conversion.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5800 | 0.3600 | 0.7800 |
| conversion | 0.9910 | 0.9500 | 1.0000 |
| safety_risk | 0.1800 | 0.1000 | 0.3000 |
| score | 0.1800 | 0.0700 | 0.3200 |
| selectivity | 0.4150 | 0.2500 | 0.6000 |
| yield | 0.4120 | 0.2500 | 0.5800 |

### Q12

At 465 K, 1800 s is long enough for rapid conversion at the middle catalyst concentration but also for strong target degradation. The short duration prevents the near-total target destruction predicted for the 7200 s cases, while safety risk remains near or above the stated limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6610 | 0.4200 | 0.8600 |
| conversion | 0.9550 | 0.8600 | 0.9900 |
| safety_risk | 0.3800 | 0.2400 | 0.5600 |
| score | 0.1000 | 0.0250 | 0.2300 |
| selectivity | 0.3080 | 0.1600 | 0.5000 |
| yield | 0.2940 | 0.1400 | 0.4700 |

## K2 — Retrospective analysis

1. Assessment of the initial information

The initial material packet contained only one substantive mechanistic prior: target formation might be effectively irreversible on the public support, with moderate confidence. It also explicitly said that catalyst identities were opaque and that solvent effects were categorical benchmark effects rather than real-property predictions.

The campaign found no clear counterevidence to effective irreversibility, but it did not actually test reversibility. None of the batches deliberately approached equilibrium from the product side, used an extended cooled hold to look for reactant regeneration, or began with isolated target. Thus, the correct conclusion is absence of observed counterevidence, not experimental confirmation. In K1 I appropriately wrote that reversibility was unnecessary on the tested support but not directly excluded. There was no observed result that clearly contradicted irreversibility and was then ignored.

The anonymity and categorical-effect warnings remained important. The solvent screen showed large differences among water, ethanol, acetonitrile, and toluene, but those differences cannot legitimately be attributed to familiar real-world polarity, proticity, or boiling-point arguments. I respected that limitation in K1 and treated solvent identity as a categorical kinetic factor.

No task-specific dossier supplied claims about catalyst ranking, reaction order, activation energy, heat of reaction, or degradation chemistry. Those aspects were genuinely open rather than initial claims awaiting confirmation. Consequently, statements in K1 such as the branched/consecutive mechanism and the approximately 19 kJ mol^-1 apparent activation energy were campaign-derived interpretations, not validations of supplied material facts.

2. Experiments that formed or changed the interpretation

Batch 1 was mainly an arbitrary baseline: Catalyst A in water at 350 K for 3600 s. Its moderate conversion and selectivity established that the system was neither inert nor completely selective, but the choice of water, full catalyst loading, and 3600 s was not supported by prior kinetic evidence.

Batches 2–4 genuinely changed the model. Under the same water/350 K/3600 s conditions, Catalyst C gave conversion 0.4399 and selectivity 0.6467, whereas Catalyst D gave conversion 0.6418 and selectivity 0.8438. That contrast ruled out treating catalyst identity as only a scalar multiplier on a universal conversion rate. It motivated catalyst-dependent branching as well as catalyst-dependent activity.

Batches 5–7 were the second decisive block. With Catalyst D at 350 K for 3600 s, acetonitrile increased conversion to 0.7759, water retained selectivity of 0.8438, and toluene produced selectivity of only 0.6855 with byproduct signal 0.2092. This changed the account from a single solvent acceleration factor to separate solvent effects on total conversion, target branching, and degradation or byproduct production.

Batches 8 and 9 established the temperature trade-off. Across 325, 350, and 375 K commands, conversion increased from 0.5627 to 0.7759 to 0.8837, while degradation warning increased from 0.0369 to 0.0903 to 0.1379. This was the main evidence for different temperature sensitivities of productive conversion and product loss.

Batches 10 and 11 most strongly shaped the kinetic interpretation. The conversion observations at 900, 1800, 3600, and 7200 s yielded similar pseudo-first-order disappearance constants, while selectivity fell from 0.9084 at 900 s to 0.6692 at 7200 s. This combination supported approximately first-order reactant disappearance plus a separate time-dependent loss of target. It also weakened, without eliminating, a simple rapid-deactivation account.

Batch 12 addressed quenching. Relative to Batch 9, it gave nearly unchanged conversion but somewhat higher yield and lower degradation warning after an explicit quench. That supported the direction of a protective quench effect, although K1 correctly described the evidence as provisional because the comparison had no replication.

Several choices were less evidence-driven. The initial use of maximum reagent, solvent, and catalyst amounts was an unvalidated design convention. Water as the first solvent, 350 K as the baseline, and 600 rpm were guesses. Choosing Catalyst D for subsequent work was data-driven after Batch 4. Choosing acetonitrile after Batch 6 was also data-driven. The 325/350/375 K temperature series, the 900–7200 s time series, and the final quench comparison were based on emerging evidence and explicit diagnostic goals. No catalyst-free control, catalyst-dose series, reagent-concentration series, stirring-speed series, or true replicate was performed.

3. Current competing mechanisms and what the campaign distinguishes

My preferred account remains the K1 branched/consecutive model: reactant forms target and byproduct in parallel, while target subsequently enters a degradation pool. It economically explains rising conversion together with declining selectivity, the large late-time degradation warning, and the approximate relation between converted material not present as target and the byproduct signal.

The most important competing explanations are:

- A parallel-only mechanism whose branching ratio changes with temperature or reaction progress. It can reproduce declining selectivity without literal target degradation if the later reaction environment increasingly favors byproduct.
- A consecutive mechanism in which most measured byproduct is produced from target rather than directly from reactant.
- Selective catalyst-state evolution: a target-selective catalytic state converts into a byproduct-selective state. This can imitate target degradation in all measured public channels.
- General catalyst deactivation combined with an independent uncatalyzed byproduct route.
- Reversible target formation or approach to equilibrium.
- Thermal or transport transients that make nominally time-dependent chemistry actually reflect evolving temperature or mixing.

The experiments distinguish some coarse features. Catalyst C versus D shows that catalyst identity changes branching, not just speed. The time series shows that one fixed selectivity attached to a first-order conversion law is inadequate. The temperature series shows that productive and nonproductive channels do not share identical temperature dependence. The reported degradation channel makes some form of secondary loss more economical than a purely parallel model.

They do not identify whether the target is chemically converted into the measured byproduct, into a separate degradation species, or merely correlated with a changing catalyst state. They do not separate catalyst deactivation from equilibrium or transport limitations at high conversion. They also do not distinguish true Arrhenius behavior from finite thermal response over such a small temperature set. The apparent activation energy in K1 is therefore descriptive rather than elementary.

4. One additional complete experiment

If exactly one legal complete experiment were available, I would choose a condition centered on the largest unresolved extrapolation rather than simply repeat the current best operation:

- 0.005 L acetonitrile
- 0.003 mol reagent
- Catalyst B, 0.000315 mol
- 400 rpm
- Heat at 410 K for 1800 s
- Take one HPLC measurement
- Continue heating at 410 K for another 5400 s
- Terminate and run the final assay

This is the central condition underlying blind predictions Q09 and Q10, except without a quench. It simultaneously tests transfer from Catalyst D to B, catalyst-concentration scaling, small-volume scaling, 410 K extrapolation, and the predicted decline between 1800 and 7200 s.

If conversion rose toward completion while target yield first became substantial and then fell as byproduct and degradation increased, that would strongly support the consecutive-loss component used in K1 and in the blind predictions. If conversion and yield rose proportionally while selectivity stayed approximately constant, the assumed secondary degradation rate would be too large and the parallel stable-branching model would become preferable. If conversion plateaued well below completion, catalyst deactivation, equilibrium, or transport limitation would require much more weight. If conversion stayed high but selectivity changed without a corresponding degradation increase, catalyst-state-dependent branching would become more plausible than direct target degradation.

This experiment would still not uniquely identify chemistry, but its within-vessel early and late observations would be more discriminating than two independent terminal batches because they share formulation and initial state.

5. Trade-off between identifiability and operational score

The stated research goal emphasized explanatory and predictive understanding, with safe score explicitly secondary. That led to several deliberate score sacrifices. Catalyst C in Batch 3 and toluene in Batch 7 were poor-performing conditions, but they were valuable because they exposed catalyst- and solvent-dependent branching. Batch 8 at 325 K and Batch 10 at 900 s produced lower yields but established temperature and time dependence. Batch 11 continued to 7200 s even though the emerging data suggested diminishing target returns; this was useful for detecting late degradation.

Conversely, the design also sacrificed identifiability for optimization. After Batch 4, most experiments used Catalyst D, and after Batch 6 most used acetonitrile. This concentrated evidence around a promising operating region but left catalyst-by-solvent interactions unidentified. Using the maximum catalyst amount in every campaign batch improved conversion and made high-yield conditions easier to find, but it prevented estimation of catalyst order or saturation. Batch 12 was partly mechanistic, through its quench comparison, and partly an optimization attempt at the best observed catalyst-solvent-temperature region.

The campaign therefore followed a sequential screen-then-refine strategy rather than a balanced mechanistic design. It successfully found a high-performing sample-in operation, but a factorial catalyst-by-solvent design, dose variation, and replication would have supported stronger causal identification. The research objective pushed the campaign toward time, temperature, and quench diagnostics; the limited 12-batch budget and desire to retain useful performance pushed it toward Catalyst D/acetonitrile after the early screens.

6. Underused evidence and weaknesses in the blind predictions

The raw characterization artifacts were not inspected beyond the supplied peak summaries and processed estimates. Peak areas, detailed spectra, calibration metadata, and mass-balance fields might have revealed whether the apparent identity conversion minus yield approximately equals byproduct consistently, whether degradation had a distinct spectral trajectory, and whether any channel approached saturation or detection limits.

Operation-level thermal and risk information was also underused. K1 noted the actual temperature increments and the finite 54.85 s quench, but I did not fit a thermal time constant or a quantitative risk model. Catalyst-dependent heat-step risk increments were interpreted qualitatively rather than incorporated into a joint kinetic-thermal fit. Differences between intermediate HPLC and final-assay readings were not modeled explicitly, and instrument uncertainty was not propagated through the pseudo-first-order or Arrhenius estimates.

Several intermediate measurements added little mechanistic leverage because they were taken immediately before termination. Batch 11 was the main exception because its 1800 s HPLC observation preceded additional heating. The lack of replicates also made it difficult to separate assay noise from genuine differences, especially for the modest Batch 9 versus Batch 12 quench effect.

The least reliable blind predictions are Q04, Q06, and Q08, followed by Q02 and Q12. They combine 410–465 K temperatures, long residence times, or high catalyst loading outside the K1 calibration region. Q08 in particular extrapolates both temperature and degradation so aggressively that its near-zero target prediction is highly model-dependent. Q09 and Q10 are also uncertain because their difference rests on a single unreplicated quench comparison. Even Q05 and Q07, which use 350 K, employ untested catalyst loadings, a smaller volume, Catalyst B in acetonitrile, and 400 rather than 600 rpm.

Some prediction intervals were too narrow relative to the limitations declared in K1. K1 explicitly restricted confident interpolation to approximately 325–375 K, 900–7200 s, the tested loading, and 600 rpm. Nevertheless, predictions such as Q04 conversion 1.000 with an 80% interval of 0.99–1.00, Q08 conversion 1.000 with 0.995–1.00, and Q08 yield 0.002 with 0–0.08 expressed excessive confidence outside that domain. Similar criticism applies to the near-complete-conversion intervals for Q06 and Q11. The bounded nature of conversion mechanically compresses intervals near one, but structural uncertainty about deactivation, equilibrium, thermal lag, and catalyst scaling should have widened them substantially.

The safety-risk intervals at 465 K may also be too narrow because no campaign batch approached that temperature and no quantitative scale dependence was identified. The blind score estimates are particularly fragile: K1 did not identify the exact score mapping, and the prediction rationale relied mainly on kinetic channels plus qualitative penalties. That weakness should have produced wider score intervals throughout.

Thus, the blind predictions were consistent with the qualitative K1 mechanism, but their numerical precision was not always consistent with K1's stated scope and identifiability limits. That is a methodological shortcoming visible even without prediction truth.

7. Limitations of the sealed recommendation

The sealed recommendation selected Batch 12 because it had the highest observed campaign yield, 0.7046, and score, 0.3756, at risk 0.1985. It should be described only as the sample-in highest result among the 12 tested batches.

It was not proven globally optimal. The campaign did not densely optimize temperature, time, catalyst amount, stirring speed, concentration, or quench timing. Batch 12 used maximum catalyst loading, Catalyst D, acetonitrile, a 375 K command, 3600 s, and an immediate quench. Nearby settings such as 365 or 385 K, 2500–5000 s, lower catalyst loading, or earlier quench could produce a better yield-risk-cost trade-off.

The apparent advantage over unquenched Batch 9 was modest: yield differed by about 0.0176, selectivity by about 0.0126, and degradation warning by about 0.0144. With one batch per condition, that is not a definitive reproducibility demonstration. Batch order, process variability, and assay noise remain plausible contributors.

Repeatability should be tested with randomized replicate batches of the exact Batch 12 recipe, reporting distributions for yield, selectivity, degradation, risk, and score. Local robustness should then be tested by bracketing temperature, residence time, catalyst loading, and quench delay around Batch 12. A useful local design would include matched quenched and unquenched replicates rather than relying on the single Batch 9–12 comparison.

Cross-material generality would require repeating the local optimum study with other catalysts and solvents, especially because the campaign did not establish that Catalyst D's advantage persists outside water or that acetonitrile's advantage persists across catalysts. Cross-world generality is even less justified: the catalysts are anonymous benchmark formulations and solvent effects are world-specific categorical couplings. The recommendation therefore cannot be transferred to a real named synthesis or another benchmark world without new evidence.

In summary, Batch 12 is a defensible participant-selected incumbent and the best observed sample, not an established optimum. Its repeatability, neighborhood stability, catalyst-solvent interaction robustness, scale dependence, and cross-world validity all remain unproven.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 132.3 | none | 0 |
| Q | yes | 0 | 182.6 | none | 0 |
| K2 | yes | 0 | 97.6 | none | 0 |

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean 80% width | Mean interval score |
|---|---:|---:|---:|---:|
| byproduct_signal | 0.2238 | 0.4167 | 0.2925 | 1.1560 |
| conversion | 0.0218 | 0.9333 | 0.1071 | 0.1117 |
| safety_risk | 0.0756 | 0.6667 | 0.2500 | 0.3046 |
| score | 0.1278 | 0.4167 | 0.1667 | 0.7519 |
| selectivity | 0.2457 | 0.3333 | 0.2608 | 1.3707 |
| yield | 0.2356 | 0.3333 | 0.2542 | 1.3669 |

## Predictions versus released reference truth

### Q01

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1470 | 0.0700 | 0.3000 | 0.1394 | 0.1397, 0.1462, 0.1413, 0.1384, 0.1316 |
| conversion | 0.4520 | 0.3000 | 0.6100 | 0.5419 | 0.5369, 0.5361, 0.5497, 0.5430, 0.5438 |
| safety_risk | 0.1400 | 0.0800 | 0.2300 | 0.2496 | 0.2496, 0.2496, 0.2496, 0.2496, 0.2496 |
| score | 0.2300 | 0.1200 | 0.3500 | 0.2633 | 0.2655, 0.2652, 0.2643, 0.2587, 0.2626 |
| selectivity | 0.6750 | 0.5200 | 0.8000 | 0.7421 | 0.7503, 0.7451, 0.7464, 0.7401, 0.7288 |
| yield | 0.3050 | 0.1800 | 0.4400 | 0.4090 | 0.4107, 0.4134, 0.4068, 0.3985, 0.4152 |
### Q02

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.9510 | 0.7000 | 1.0000 | 0.7361 | 0.7397, 0.7292, 0.7492, 0.7245, 0.7377 |
| conversion | 0.9920 | 0.9300 | 1.0000 | 0.9894 | 0.9940, 0.9820, 0.9971, 0.9889, 0.9850 |
| safety_risk | 0.2900 | 0.1800 | 0.4300 | 0.2515 | 0.2515, 0.2515, 0.2515, 0.2515, 0.2515 |
| score | 0.0100 | 0.0000 | 0.0800 | 0.1240 | 0.1282, 0.1246, 0.1241, 0.1240, 0.1192 |
| selectivity | 0.0410 | 0.0000 | 0.2400 | 0.2740 | 0.2821, 0.2767, 0.2785, 0.2713, 0.2612 |
| yield | 0.0410 | 0.0000 | 0.2300 | 0.2699 | 0.2741, 0.2715, 0.2653, 0.2716, 0.2669 |
### Q03

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3530 | 0.2000 | 0.5600 | 0.1516 | 0.1469, 0.1490, 0.1465, 0.1682, 0.1471 |
| conversion | 0.9260 | 0.7800 | 0.9900 | 0.9045 | 0.9126, 0.8934, 0.9063, 0.9038, 0.9066 |
| safety_risk | 0.2100 | 0.1300 | 0.3200 | 0.2526 | 0.2526, 0.2526, 0.2526, 0.2526, 0.2526 |
| score | 0.3100 | 0.1600 | 0.4600 | 0.4366 | 0.4406, 0.4357, 0.4386, 0.4338, 0.4345 |
| selectivity | 0.6190 | 0.4400 | 0.7600 | 0.8453 | 0.8629, 0.8401, 0.8425, 0.8499, 0.8314 |
| yield | 0.5730 | 0.3900 | 0.7100 | 0.7624 | 0.7594, 0.7661, 0.7686, 0.7528, 0.7653 |
### Q04

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.9880 | 0.8500 | 1.0000 | 0.7894 | 0.7706, 0.7875, 0.8048, 0.7903, 0.7936 |
| conversion | 1.0000 | 0.9900 | 1.0000 | 0.9959 | 1.0000, 0.9907, 1.0000, 0.9890, 1.0000 |
| safety_risk | 0.4200 | 0.2700 | 0.6000 | 0.2519 | 0.2519, 0.2519, 0.2519, 0.2519, 0.2519 |
| score | 0.0020 | 0.0000 | 0.0400 | 0.0871 | 0.0917, 0.0894, 0.0841, 0.0875, 0.0830 |
| selectivity | 0.0120 | 0.0000 | 0.1500 | 0.2562 | 0.2603, 0.2645, 0.2443, 0.2601, 0.2517 |
| yield | 0.0120 | 0.0000 | 0.1400 | 0.2596 | 0.2675, 0.2614, 0.2583, 0.2597, 0.2510 |
### Q05

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1860 | 0.0900 | 0.3400 | 0.2859 | 0.2874, 0.2976, 0.2794, 0.2754, 0.2894 |
| conversion | 0.5950 | 0.4200 | 0.7400 | 0.7070 | 0.7056, 0.7061, 0.7105, 0.7038, 0.7091 |
| safety_risk | 0.1000 | 0.0500 | 0.1800 | 0.1416 | 0.1416, 0.1416, 0.1416, 0.1416, 0.1416 |
| score | 0.3000 | 0.1700 | 0.4300 | 0.2914 | 0.2937, 0.2855, 0.2896, 0.2953, 0.2931 |
| selectivity | 0.6880 | 0.5500 | 0.8000 | 0.6004 | 0.6055, 0.5865, 0.5961, 0.6143, 0.5996 |
| yield | 0.4100 | 0.2700 | 0.5400 | 0.4163 | 0.4191, 0.4105, 0.4134, 0.4182, 0.4204 |
### Q06

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.9730 | 0.8000 | 1.0000 | 0.6099 | 0.6123, 0.6066, 0.6036, 0.6193, 0.6079 |
| conversion | 0.9910 | 0.9400 | 1.0000 | 0.9947 | 1.0000, 0.9837, 0.9990, 0.9934, 0.9973 |
| safety_risk | 0.4700 | 0.3100 | 0.6800 | 0.4259 | 0.4259, 0.4259, 0.4259, 0.4259, 0.4259 |
| score | 0.0020 | 0.0000 | 0.0500 | 0.1323 | 0.1345, 0.1397, 0.1227, 0.1333, 0.1313 |
| selectivity | 0.0180 | 0.0000 | 0.1800 | 0.3927 | 0.3842, 0.4258, 0.3714, 0.4011, 0.3809 |
| yield | 0.0180 | 0.0000 | 0.1700 | 0.3962 | 0.4056, 0.3968, 0.3843, 0.3939, 0.4005 |
### Q07

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3700 | 0.2000 | 0.5800 | 0.3215 | 0.3256, 0.3232, 0.3132, 0.3178, 0.3278 |
| conversion | 0.9800 | 0.9200 | 1.0000 | 0.9676 | 0.9735, 0.9585, 0.9756, 0.9696, 0.9610 |
| safety_risk | 0.1400 | 0.0800 | 0.2400 | 0.1439 | 0.1439, 0.1439, 0.1439, 0.1439, 0.1439 |
| score | 0.3500 | 0.2000 | 0.4900 | 0.4053 | 0.4066, 0.4069, 0.4029, 0.4048, 0.4054 |
| selectivity | 0.6230 | 0.4700 | 0.7500 | 0.6857 | 0.6945, 0.6952, 0.6796, 0.6717, 0.6874 |
| yield | 0.6100 | 0.4500 | 0.7300 | 0.6572 | 0.6533, 0.6575, 0.6531, 0.6640, 0.6580 |
### Q08

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.9980 | 0.9200 | 1.0000 | 0.6400 | 0.6433, 0.6384, 0.6379, 0.6363, 0.6440 |
| conversion | 1.0000 | 0.9950 | 1.0000 | 0.9930 | 0.9781, 0.9871, 1.0000, 1.0000, 1.0000 |
| safety_risk | 0.6600 | 0.4500 | 0.8600 | 0.4263 | 0.4263, 0.4263, 0.4263, 0.4263, 0.4263 |
| score | 0.0000 | 0.0000 | 0.0200 | 0.1053 | 0.1049, 0.1045, 0.0992, 0.1060, 0.1120 |
| selectivity | 0.0020 | 0.0000 | 0.0800 | 0.4013 | 0.4087, 0.3948, 0.3933, 0.3967, 0.4131 |
| yield | 0.0020 | 0.0000 | 0.0800 | 0.3962 | 0.3944, 0.3998, 0.3842, 0.3991, 0.4038 |
### Q09

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.8550 | 0.6300 | 0.9700 | 0.4912 | 0.4900, 0.4852, 0.4940, 0.4841, 0.5025 |
| conversion | 0.9980 | 0.9800 | 1.0000 | 0.9974 | 1.0000, 0.9923, 1.0000, 1.0000, 0.9946 |
| safety_risk | 0.2900 | 0.1800 | 0.4300 | 0.2523 | 0.2523, 0.2523, 0.2523, 0.2523, 0.2523 |
| score | 0.0350 | 0.0000 | 0.1300 | 0.2752 | 0.2725, 0.2767, 0.2744, 0.2725, 0.2800 |
| selectivity | 0.1440 | 0.0400 | 0.3600 | 0.5164 | 0.5050, 0.5198, 0.5199, 0.5132, 0.5241 |
| yield | 0.1440 | 0.0400 | 0.3500 | 0.5154 | 0.5150, 0.5181, 0.5106, 0.5099, 0.5231 |
### Q10

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.8400 | 0.6000 | 0.9600 | 0.4949 | 0.4892, 0.4966, 0.4999, 0.5047, 0.4842 |
| conversion | 0.9980 | 0.9800 | 1.0000 | 0.9942 | 0.9991, 0.9998, 1.0000, 0.9939, 0.9781 |
| safety_risk | 0.2500 | 0.1500 | 0.3900 | 0.1459 | 0.1459, 0.1459, 0.1459, 0.1459, 0.1459 |
| score | 0.0450 | 0.0050 | 0.1500 | 0.3201 | 0.3218, 0.3178, 0.3232, 0.3200, 0.3179 |
| selectivity | 0.1600 | 0.0500 | 0.3900 | 0.5173 | 0.5167, 0.5191, 0.5235, 0.5115, 0.5160 |
| yield | 0.1600 | 0.0500 | 0.3800 | 0.5165 | 0.5199, 0.5082, 0.5188, 0.5198, 0.5156 |
### Q11

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5800 | 0.3600 | 0.7800 | 0.5489 | 0.5697, 0.5532, 0.5308, 0.5504, 0.5403 |
| conversion | 0.9910 | 0.9500 | 1.0000 | 0.9903 | 0.9833, 0.9865, 0.9912, 0.9955, 0.9949 |
| safety_risk | 0.1800 | 0.1000 | 0.3000 | 0.1434 | 0.1434, 0.1434, 0.1434, 0.1434, 0.1434 |
| score | 0.1800 | 0.0700 | 0.3200 | 0.2810 | 0.2783, 0.2768, 0.2825, 0.2819, 0.2854 |
| selectivity | 0.4150 | 0.2500 | 0.6000 | 0.4585 | 0.4538, 0.4471, 0.4607, 0.4561, 0.4750 |
| yield | 0.4120 | 0.2500 | 0.5800 | 0.4602 | 0.4583, 0.4578, 0.4625, 0.4628, 0.4597 |
### Q12

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.6610 | 0.4200 | 0.8600 | 0.2069 | 0.2063, 0.2058, 0.1964, 0.2129, 0.2132 |
| conversion | 0.9550 | 0.8600 | 0.9900 | 0.9513 | 0.9555, 0.9519, 0.9512, 0.9428, 0.9552 |
| safety_risk | 0.3800 | 0.2400 | 0.5600 | 0.4267 | 0.4267, 0.4267, 0.4267, 0.4267, 0.4267 |
| score | 0.1000 | 0.0250 | 0.2300 | 0.3582 | 0.3619, 0.3582, 0.3617, 0.3502, 0.3588 |
| selectivity | 0.3080 | 0.1600 | 0.5000 | 0.7886 | 0.7934, 0.7801, 0.8111, 0.7735, 0.7849 |
| yield | 0.2940 | 0.1400 | 0.4700 | 0.7491 | 0.7543, 0.7544, 0.7438, 0.7407, 0.7521 |

## Recommendation retest

- Selected source batch: `12`
- Retest exact replay verified: `True`
- Retest failure: `none`

| Metric | Selected source batch | Independent retest | Retest minus source |
|---|---:|---:|---:|
| byproduct_signal | 0.2127 | 0.1925 | -0.0202 |
| conversion | 0.8808 | 0.8933 | 0.0125 |
| cost | 1.0000 | 1.0000 | 0.0000 |
| degradation_warning | 0.1235 | 0.1463 | 0.0227 |
| safety_risk | 0.1985 | 0.1985 | 0.0000 |
| score | 0.3756 | 0.3750 | -0.0006 |
| selectivity | 0.7801 | 0.7860 | 0.0059 |
| virtual_spectrum_summary | 0.1726 | 0.1717 | -0.0009 |
| yield | 0.7046 | 0.6962 | -0.0083 |

## Scope note

This is the final sanitized report produced after all 60 source sessions and K1/Q/K2 chains were sealed. It includes released reference truth, blind-prediction evaluation, and the independent recommendation retest. Provider-private event streams, credentials, thread identifiers, and token accounting remain excluded.
