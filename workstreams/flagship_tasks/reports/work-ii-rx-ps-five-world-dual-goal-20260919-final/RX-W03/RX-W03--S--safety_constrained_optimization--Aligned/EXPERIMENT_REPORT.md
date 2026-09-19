# RX-W03--S--safety_constrained_optimization--Aligned

## Run summary

- World: `RX-W03`
- Locus: `S`
- Goal: `safety_constrained_optimization`
- Arm: `Aligned`
- Status: `completed`
- Source status: `completed`
- Experimental sessions: `12/12`
- Operations: `84`
- Exact replay verified: `True`
- Rollbacks: `[]`
- Posttest chain sealed: `True`

### Recovery status

- Effective result location: `source-repair-v9`
- Recovery version: `recovery-v10-parallel4-continue`
- Repaired stages: `source`
- Source experiments rerun: `False`
- Original source thread reused: `False`
- Truth revealed during recovery: `False`

## Sealed recommendation

- Selected batch: `12`
- Rationale: Highest observed public safe score (0.3265) while remaining comfortably below the 0.35 safety limit (risk 0.1911).

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S2 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 320 K x 3600 s @ 600 rpm | no | 0.2260 | 0.6102 | 0.3710 | 0.1461 | 0.0083 | 0.1428 | 0.1158 |
| 2 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 340 K x 3600 s @ 600 rpm | no | 0.5868 | 0.7437 | 0.7888 | 0.2134 | 0.1323 | 0.1907 | 0.3137 |
| 3 | S2 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 340 K x 3600 s @ 600 rpm | no | 0.4684 | 0.7336 | 0.6415 | 0.1930 | 0.0685 | 0.1729 | 0.2571 |
| 4 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 340 K x 3600 s @ 600 rpm | no | 0.4463 | 0.7621 | 0.5837 | 0.1253 | 0.0562 | 0.1698 | 0.2510 |
| 5 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 340 K x 3600 s @ 600 rpm | no | 0.4570 | 0.8055 | 0.5664 | 0.1041 | 0.0497 | 0.1284 | 0.2831 |
| 6 | S1 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 340 K x 3600 s @ 600 rpm | no | 0.5111 | 0.7507 | 0.6648 | 0.1633 | 0.0655 | 0.1594 | 0.2869 |
| 7 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 340 K x 3600 s @ 600 rpm | no | 0.4298 | 0.6128 | 0.7057 | 0.2692 | 0.1122 | 0.1878 | 0.2112 |
| 8 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 360 K x 3600 s @ 600 rpm | no | 0.6171 | 0.6731 | 0.8968 | 0.2879 | 0.2131 | 0.2061 | 0.3121 |
| 9 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.6091 | 0.7141 | 0.8530 | 0.2461 | 0.1765 | 0.1983 | 0.3182 |
| 10 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 345 K x 4500 s @ 600 rpm | no | 0.6040 | 0.6904 | 0.9024 | 0.2988 | 0.2351 | 0.1988 | 0.3150 |
| 11 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3000 s @ 600 rpm | no | 0.6028 | 0.7540 | 0.8048 | 0.1953 | 0.1410 | 0.1941 | 0.3228 |
| 12 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 2700 s @ 600 rpm | no | 0.6044 | 0.7757 | 0.7681 | 0.1838 | 0.1157 | 0.1911 | 0.3265 |

## Complete experimental actions and observations

### Batch 1

Lifecycle index: `1`; end step: `7`.

```json
{
  "actions": [
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
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
      "target_temperature_K": 320
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
    "byproduct_signal": 0.1460677981376648,
    "conversion": 0.37095242738723755,
    "cost": 1.0,
    "degradation_warning": 0.008320258930325508,
    "safety_risk": 0.14284548163414001,
    "score": 0.11575301736593246,
    "selectivity": 0.610232949256897,
    "virtual_spectrum_summary": 0.08408140391111374,
    "yield": 0.22595003247261047
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
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
      "target_temperature_K": 340
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
    "byproduct_signal": 0.21340709924697876,
    "conversion": 0.7887619733810425,
    "cost": 1.0,
    "degradation_warning": 0.1322792023420334,
    "safety_risk": 0.19072236120700836,
    "score": 0.3136666715145111,
    "selectivity": 0.7436563968658447,
    "virtual_spectrum_summary": 0.17689955234527588,
    "yield": 0.5867536067962646
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
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
      "target_temperature_K": 340
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
    "byproduct_signal": 0.19300521910190582,
    "conversion": 0.6414508819580078,
    "cost": 1.0,
    "degradation_warning": 0.06850219517946243,
    "safety_risk": 0.1729304939508438,
    "score": 0.2570810914039612,
    "selectivity": 0.7336073517799377,
    "virtual_spectrum_summary": 0.1369788646697998,
    "yield": 0.46838220953941345
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
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
      "target_temperature_K": 340
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
    "byproduct_signal": 0.12525461614131927,
    "conversion": 0.5837136507034302,
    "cost": 1.0,
    "degradation_warning": 0.05620907247066498,
    "safety_risk": 0.16977310180664062,
    "score": 0.25103020668029785,
    "selectivity": 0.7621331810951233,
    "virtual_spectrum_summary": 0.09418412297964096,
    "yield": 0.4463086426258087
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
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
      "target_temperature_K": 340
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
    "byproduct_signal": 0.10407175868749619,
    "conversion": 0.5664288997650146,
    "cost": 1.0,
    "degradation_warning": 0.04974159598350525,
    "safety_risk": 0.1283951848745346,
    "score": 0.28306055068969727,
    "selectivity": 0.8055499196052551,
    "virtual_spectrum_summary": 0.07962318509817123,
    "yield": 0.4570200741291046
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.08
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
      "target_temperature_K": 340
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
    "byproduct_signal": 0.16326409578323364,
    "conversion": 0.6647717356681824,
    "cost": 1.0,
    "degradation_warning": 0.065495565533638,
    "safety_risk": 0.15940997004508972,
    "score": 0.2868533730506897,
    "selectivity": 0.750740110874176,
    "virtual_spectrum_summary": 0.1192682534456253,
    "yield": 0.5110641717910767
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 3,
      "volume_L": 0.08
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
      "target_temperature_K": 340
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
    "byproduct_signal": 0.26919975876808167,
    "conversion": 0.705700695514679,
    "cost": 1.0,
    "degradation_warning": 0.1121780276298523,
    "safety_risk": 0.18784457445144653,
    "score": 0.2111584097146988,
    "selectivity": 0.6127832531929016,
    "virtual_spectrum_summary": 0.19853997230529785,
    "yield": 0.4298064410686493
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
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
      "target_temperature_K": 360
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
    "byproduct_signal": 0.287878155708313,
    "conversion": 0.8967655897140503,
    "cost": 1.0,
    "degradation_warning": 0.21310199797153473,
    "safety_risk": 0.20610564947128296,
    "score": 0.31206759810447693,
    "selectivity": 0.6731238961219788,
    "virtual_spectrum_summary": 0.2542288899421692,
    "yield": 0.6171440482139587
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
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
  "end_step": 63,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.24607305228710175,
    "conversion": 0.8530345559120178,
    "cost": 1.0,
    "degradation_warning": 0.17645251750946045,
    "safety_risk": 0.1983037292957306,
    "score": 0.3182162344455719,
    "selectivity": 0.7140907645225525,
    "virtual_spectrum_summary": 0.21474380791187286,
    "yield": 0.609066903591156
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 4500,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 345
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
    "byproduct_signal": 0.29876577854156494,
    "conversion": 0.9024020433425903,
    "cost": 1.0,
    "degradation_warning": 0.23505567014217377,
    "safety_risk": 0.19878442585468292,
    "score": 0.31498169898986816,
    "selectivity": 0.6904454827308655,
    "virtual_spectrum_summary": 0.2700962424278259,
    "yield": 0.6039577722549438
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3000,
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
  "end_step": 77,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.1952817738056183,
    "conversion": 0.804818868637085,
    "cost": 1.0,
    "degradation_warning": 0.14099574089050293,
    "safety_risk": 0.19406135380268097,
    "score": 0.32275545597076416,
    "selectivity": 0.7539929151535034,
    "virtual_spectrum_summary": 0.17085306346416473,
    "yield": 0.6027573347091675
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 2700,
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
  "end_step": 84,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.18380235135555267,
    "conversion": 0.7680866718292236,
    "cost": 1.0,
    "degradation_warning": 0.11565868556499481,
    "safety_risk": 0.19114436209201813,
    "score": 0.3264589309692383,
    "selectivity": 0.7756762504577637,
    "virtual_spectrum_summary": 0.1531376987695694,
    "yield": 0.6043654084205627
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

1. Scope and evidence base

This report concerns only the bounded synthetic reaction-and-thermal benchmark studied in the completed 12-batch campaign. The reagent and catalysts are anonymous benchmark materials. Although the selectable solvents have familiar names, their reaction effects are categorical benchmark effects, so I do not interpret them as evidence for a particular real chemical synthesis.

Every batch used 0.040 mol reagent, 0.080 L solvent, 0.005 mol catalyst, and 600 rpm stirring. Thus, the campaign identifies relative effects of catalyst, solvent, temperature, and heating time at one reagent concentration, one catalyst loading, and one mixing rate. Final assays were acquired after termination. One HPLC measurement was also made immediately before termination in every batch.

2. Proposed operating mechanism

The observations are consistent with a thermally activated, effectively irreversible conversion of reactant into a desired target, accompanied by competing formation of byproduct and degradation products:

R --k_target(T,catalyst,solvent)--> P
R --k_side(T,catalyst,solvent)--> B
P --k_deg(T,solvent)--> D

A minimal kinetic representation would be:

dR/dt = -(k_target + k_side)R
dP/dt = k_target R - k_deg P
dB/dt = k_side R + alpha*k_deg P

with Arrhenius-like temperature dependence,

k_j(T) = A_j(catalyst,solvent) * exp[-E_j/(R_gas*T)].

The catalyst and solvent indices probably modify the effective prefactors and possibly activation energies rather than acting as simple additive score bonuses. The final target yield depends on both conversion and selectivity. Heating accelerates target formation, but excessive thermal exposure increasingly favors byproduct generation or target degradation. Consequently, score has an interior optimum in temperature-time space rather than increasing monotonically with conversion.

A useful empirical control variable is thermal exposure rather than nominal setpoint alone:

thermal_exposure = integral f(T_actual(t)) dt,

where f rises steeply with temperature. The reactor did not instantaneously reach its setpoint. For example, the reported temperature increments were about 39.66 K at a 340 K/3600 s treatment, 48.70 K at 350 K/3600 s, and 57.55 K at 360 K/3600 s. Therefore, nominal temperature and duration jointly encode heating transients as well as reaction time.

3. Catalyst effects

Batches 2-4 isolated catalyst identity at acetonitrile, 340 K, and 3600 s.

Batch 2, Catalyst B: final conversion 0.7888, yield 0.5868, selectivity 0.7437, byproduct signal 0.2134, degradation warning 0.1323, safety risk 0.1907, score 0.3137.

Batch 3, Catalyst C: conversion 0.6415, yield 0.4684, selectivity 0.7336, byproduct 0.1930, degradation 0.0685, risk 0.1729, score 0.2571.

Batch 4, Catalyst D: conversion 0.5837, yield 0.4463, selectivity 0.7621, byproduct 0.1253, degradation 0.0562, risk 0.1698, score 0.2510.

Catalyst B gave the strongest productive rate and highest score. Catalyst D was slower but somewhat cleaner: it had the highest observed selectivity and lowest byproduct signal in this controlled comparison. Catalyst C was intermediate in rate. This is evidence that catalyst choice changes more than a single global rate constant. A plausible ordering is:

productive activity: B > C > D
intrinsic cleanliness under these conditions: D > C approximately B

Catalyst A was tested only in Batch 1, at 320 K rather than 340 K. Batch 1 gave conversion 0.3710, yield 0.2260, selectivity 0.6102, byproduct 0.1461, degradation 0.0083, risk 0.1428, and score 0.1158. Because temperature was confounded with catalyst identity, this does not prove Catalyst A is intrinsically poor. It establishes only that the Catalyst A/320 K procedure was too slow and/or insufficiently selective over 3600 s.

4. Solvent effects

Batches 2 and 5-7 compared solvents with Catalyst B at 340 K for 3600 s.

Batch 5, water: conversion 0.5664, yield 0.4570, selectivity 0.8055, byproduct 0.1041, degradation 0.0497, risk 0.1284, score 0.2831.

Batch 6, ethanol: conversion 0.6648, yield 0.5111, selectivity 0.7507, byproduct 0.1633, degradation 0.0655, risk 0.1594, score 0.2869.

Batch 2, acetonitrile: conversion 0.7888, yield 0.5868, selectivity 0.7437, byproduct 0.2134, degradation 0.1323, risk 0.1907, score 0.3137.

Batch 7, toluene: conversion 0.7057, yield 0.4298, selectivity 0.6128, byproduct 0.2692, degradation 0.1122, risk 0.1878, score 0.2112.

These data indicate a solvent-controlled activity/selectivity tradeoff. Water was the cleanest and safest but slower. Acetonitrile provided the largest conversion and yield and therefore the best score despite more byproduct and degradation. Ethanol was intermediate. Toluene was unfavorable because it combined substantial conversion with poor selectivity and the largest byproduct signal.

A reasonable empirical interpretation is that solvent modifies at least two quantities independently:

k_target: acetonitrile > toluene approximately ethanol > water
k_target/k_side: water > ethanol approximately acetonitrile > toluene

The first ordering is approximate because conversion also includes side conversion. The second is supported by selectivity and byproduct measurements. No molecular explanation such as polarity, solvation, or phase behavior can be established from these categorical benchmark observations alone.

5. Temperature and time coupling

Catalyst B/acetonitrile was studied over the most useful temperature-time region.

Batch 2: 340 K, 3600 s; conversion 0.7888, yield 0.5868, selectivity 0.7437, byproduct 0.2134, degradation 0.1323, score 0.3137, risk 0.1907.

Batch 8: 360 K, 3600 s; conversion 0.8968, yield 0.6171, selectivity 0.6731, byproduct 0.2879, degradation 0.2131, score 0.3121, risk 0.2061.

Batch 9: 350 K, 3600 s; conversion 0.8530, yield 0.6091, selectivity 0.7141, byproduct 0.2461, degradation 0.1765, score 0.3182, risk 0.1983.

Raising temperature from 340 to 350-360 K increased conversion and yield, but it also reduced selectivity and increased byproduct and degradation. At 360 K, the conversion gain no longer improved score because adverse pathways offset it. This strongly supports parallel and/or sequential thermal side reactions with temperature sensitivity comparable to or greater than that of productive conversion.

Time variation near 350 K refined the optimum:

Batch 10: 345 K, 4500 s; conversion 0.9024, yield 0.6040, selectivity 0.6904, byproduct 0.2988, degradation 0.2351, score 0.3150, risk 0.1988.

Batch 11: 350 K, 3000 s; conversion 0.8048, yield 0.6028, selectivity 0.7540, byproduct 0.1953, degradation 0.1410, score 0.3228, risk 0.1941.

Batch 12: 350 K, 2700 s; conversion 0.7681, yield 0.6044, selectivity 0.7757, byproduct 0.1838, degradation 0.1157, score 0.3265, risk 0.1911.

The 4500 s run reached high conversion but accumulated much more byproduct and degradation. Shortening the 350 K exposure from 3600 to 3000 and then 2700 s preserved approximately 0.60-0.61 yield while improving selectivity and suppressing degradation. The observed best score was therefore Batch 12, not the highest-conversion batch.

The near-constant yields in Batches 9, 11, and 12, despite conversion decreasing from 0.8530 to 0.8048 to 0.7681, are consistent with a product-yield plateau: additional conversion at longer exposure is increasingly directed toward side products, while some accumulated product may degrade. Because measurement noise is present, the small yield differences should not be overinterpreted, but the accompanying systematic changes in selectivity, byproduct, and degradation support this explanation.

6. Relation between intermediate and final measurements

The pre-termination HPLC and final assay usually agreed qualitatively but not exactly. For example:

Batch 12 HPLC: conversion 0.7514, yield 0.5960, selectivity 0.7448, byproduct 0.2122.
Batch 12 final assay: conversion 0.7681, yield 0.6044, selectivity 0.7757, byproduct 0.1838.

Batch 11 HPLC: conversion 0.8134, yield 0.5857, selectivity 0.7649, byproduct 0.1775.
Batch 11 final assay: conversion 0.8048, yield 0.6028, selectivity 0.7540, byproduct 0.1953.

Batch 2 HPLC: conversion 0.7885, yield 0.5635, selectivity 0.7037, byproduct 0.2067.
Batch 2 final assay: conversion 0.7888, yield 0.5868, selectivity 0.7437, byproduct 0.2134.

I interpret these discrepancies primarily as instrument-specific noise and processing differences, possibly with a small contribution from state evolution around termination. The final assay is the appropriate basis for comparing completed batches. There is not enough evidence to infer a reproducible termination-induced chemical transformation.

7. Safety model

All completed batches remained below the declared safety limit of 0.35. Observed final risks ranged from 0.1284 in Batch 5 to 0.2061 in Batch 8. Within the Catalyst B/acetonitrile series, risk rose with thermal severity: 0.1907 at 340 K/3600 s, 0.1983 at 350 K/3600 s, and 0.2061 at 360 K/3600 s. Shorter 350 K runs reduced risk to 0.1941 at 3000 s and 0.1911 at 2700 s.

Risk was also coupled to formulation. At otherwise fixed 340 K/3600 s Catalyst B conditions, water had risk 0.1284, ethanol 0.1594, acetonitrile 0.1907, and toluene 0.1878. Thus, a conceptual risk model is:

risk = risk_of_charging(reagent,catalyst,solvent) + integral heat_hazard(T,state) dt,

with solvent- and catalyst-dependent charging terms and a thermal term that grows with temperature and duration. This is an empirical benchmark interpretation, not a physical calorimetry model. The accumulated campaign risk should not be confused with the per-batch safety constraint.

8. Why the recommended procedure works

The sealed recommendation was Batch 12:

0.040 mol reagent; 0.080 L acetonitrile; 0.005 mol Catalyst B; heat at a 350 K setpoint for 2700 s with 600 rpm stirring; terminate; final assay.

It occupies the compromise region where Catalyst B and acetonitrile provide fast target formation, while the shortened residence time prevents the later, less selective portion of conversion from dominating. Its observed final performance was conversion 0.7681, yield 0.6044, selectivity 0.7757, byproduct signal 0.1838, degradation warning 0.1157, risk 0.1911, and score 0.3265. This was the highest observed score and remained 0.1589 below the safety limit.

9. Applicability limits and unidentified factors

The proposed mechanism is supported only over the tested domain: 0.040 mol reagent in 0.080 L solvent, 0.005 mol catalyst, 600 rpm, nominal temperatures of 320-360 K for the principal comparisons, and heating times of 2700-4500 s. It should not be assumed to extrapolate quantitatively to different concentration, catalyst loading, stirring speed, vessel scale, staged addition, temperatures outside the tested interval, or very short or very long runs.

Catalyst loading was never varied, so catalyst order and saturation cannot be identified. Reagent concentration and solvent volume were fixed, so concentration order and dilution effects are unknown. Stirring was fixed, so mass-transfer limitation cannot be excluded. Each exact condition was run once; consequently, process variation cannot be separated fully from instrument noise. The 350 K time series used separate batches rather than repeated sampling of one batch.

The data do not identify whether the degradation-warning channel represents decomposition of target, decomposition of reactant, formation of an independent impurity, or a composite signal. Likewise, byproduct signal is not a calibrated material balance fraction. The apparent loss of selectivity with thermal exposure could arise from parallel R-to-B chemistry, sequential P-to-D chemistry, or both. The three-channel scheme above is therefore a useful operational model rather than a uniquely identified molecular mechanism.

10. Reasonable competing explanations

First, a purely parallel-reaction model could explain most trends if the side reaction has a larger activation energy than the target reaction. Under that model, product does not degrade; longer or hotter operation simply directs more remaining reactant into byproduct. The degradation-warning channel would then report a correlated impurity rather than actual product decay.

Second, a sequential model R to P to D could explain the yield plateau and the increasing degradation warning. It would predict that yield eventually declines at still longer exposure. The campaign did not extend far enough at fixed conditions to demonstrate an unambiguous decline beyond measurement noise.

Third, catalyst or product deactivation could create the apparent plateau. Productive conversion might slow with time while an uncatalyzed side pathway continues. No catalyst-state measurement was available to distinguish this from product degradation.

Fourth, solvent effects could reflect benchmark-specific activity coefficients, heat-transfer differences, or effective phase behavior rather than elementary chemical kinetics. Since solvent identity is categorical in this world, a molecular solvent-property explanation would be speculative.

11. Confidence assessment

High confidence: Catalyst B/acetonitrile around 350 K with a shortened 2700-3000 s exposure was the best observed region; Batch 12 had the highest measured safe score; all tested batches respected the safety limit; excessive temperature or duration increased byproduct and degradation indicators.

Moderate confidence: the system contains productive and adverse thermally activated pathways, and the best score arises from balancing conversion against selectivity and degradation rather than maximizing conversion.

Low-to-moderate confidence: actual target product undergoes sequential degradation. This is plausible and parsimonious but is not uniquely distinguished from parallel side reaction, catalyst deactivation, or composite detector behavior.

The most defensible world model is therefore an irreversible productive pathway coupled to one or more increasingly important thermal side pathways, with catalyst and solvent independently controlling both rate and selectivity. It is an operationally predictive model within the sampled neighborhood, not a uniquely established molecular mechanism.

## Q — Blind predictions

### Overall rationale

Predictions were extrapolated from the completed Catalyst B/acetonitrile series. In that series, conversion behaved approximately like a saturating first-order response, while increasing temperature or residence time systematically reduced selectivity and increased adverse-product signals. Catalyst loading was treated as an uncertain positive multiplier on productive and side-reaction rates. Yield was constrained to remain broadly consistent with conversion multiplied by selectivity. Safety risk was modeled as a formulation contribution plus a thermal contribution increasing with temperature and time. Score estimates use the observed public relationship: positive contributions from yield, selectivity, and conversion, opposed by safety risk and operating cost. Intervals include final-assay noise, batch variation, uncertainty from untested catalyst loadings and concentration, and especially broad extrapolation uncertainty at 410-465 K. No new experiments were performed.

### Q01

The low Catalyst B loading should limit conversion during the 1800 s exposure, although 410 K is far above the studied optimum and accelerates both productive and side pathways. This temperature is an extrapolation, so the intervals are wide.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2800 | 0.1200 | 0.4800 |
| conversion | 0.6200 | 0.3800 | 0.8200 |
| safety_risk | 0.1400 | 0.0900 | 0.2200 |
| score | 0.2700 | 0.1600 | 0.3800 |
| selectivity | 0.5500 | 0.3800 | 0.7000 |
| yield | 0.3400 | 0.2000 | 0.5000 |

### Q02

At 410 K for four hours, even the low catalyst loading should approach complete conversion. Extrapolation from the observed deterioration with thermal exposure predicts extensive side reaction or product degradation, low selectivity, and substantially increased risk.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7600 | 0.5200 | 0.9400 |
| conversion | 0.9900 | 0.9400 | 1.0000 |
| safety_risk | 0.3000 | 0.2000 | 0.4300 |
| score | 0.0600 | 0.0000 | 0.1700 |
| selectivity | 0.1500 | 0.0400 | 0.3100 |
| yield | 0.1200 | 0.0200 | 0.2700 |

### Q03

The higher Catalyst B loading should drive rapid conversion during the short 410 K treatment. Higher activity improves yield relative to Q01, but the elevated temperature is expected to erode selectivity and increase byproduct formation.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4300 | 0.2200 | 0.6500 |
| conversion | 0.9100 | 0.7600 | 0.9800 |
| safety_risk | 0.1500 | 0.1000 | 0.2300 |
| score | 0.3200 | 0.2000 | 0.4300 |
| selectivity | 0.5000 | 0.3400 | 0.6500 |
| yield | 0.4600 | 0.3000 | 0.6100 |

### Q04

High catalyst loading, 410 K, and 14400 s constitute severe overprocessing. Conversion should saturate, while sequential degradation and/or thermally favored parallel reaction should leave little desired product.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8400 | 0.6300 | 0.9800 |
| conversion | 1.0000 | 0.9700 | 1.0000 |
| safety_risk | 0.3100 | 0.2100 | 0.4500 |
| score | 0.0200 | 0.0000 | 0.1000 |
| selectivity | 0.0900 | 0.0100 | 0.2200 |
| yield | 0.0600 | 0.0000 | 0.1800 |

### Q05

This temperature lies inside the studied region, but the catalyst loading is much lower and the time is longer. The lower activity should prevent immediate saturation, while 7200 s permits useful conversion with less thermal damage than the 410-465 K cases.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2400 | 0.1100 | 0.4100 |
| conversion | 0.7100 | 0.5100 | 0.8600 |
| safety_risk | 0.1400 | 0.0900 | 0.2100 |
| score | 0.3500 | 0.2400 | 0.4500 |
| selectivity | 0.6800 | 0.5300 | 0.8100 |
| yield | 0.4800 | 0.3300 | 0.6200 |

### Q06

The 465 K, 7200 s treatment is a major extrapolation beyond the campaign and should overwhelm the benefit of low catalyst loading. Near-complete conversion, severe degradation or side reaction, and possible violation of the 0.35 safety limit are expected.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9400 | 0.7600 | 1.0000 |
| conversion | 1.0000 | 0.9700 | 1.0000 |
| safety_risk | 0.4300 | 0.2800 | 0.6200 |
| score | 0.0100 | 0.0000 | 0.0700 |
| selectivity | 0.0300 | 0.0000 | 0.1200 |
| yield | 0.0100 | 0.0000 | 0.0800 |

### Q07

At 350 K the higher catalyst loading should bring conversion close to completion over 7200 s. The long exposure should reduce selectivity compared with the campaign optimum, but the smaller absolute batch cost may preserve a relatively strong score.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4200 | 0.2400 | 0.6200 |
| conversion | 0.9900 | 0.9300 | 1.0000 |
| safety_risk | 0.1500 | 0.1000 | 0.2300 |
| score | 0.3700 | 0.2500 | 0.4700 |
| selectivity | 0.5600 | 0.4200 | 0.6900 |
| yield | 0.5500 | 0.4000 | 0.6800 |

### Q08

High catalyst loading combined with 465 K for 7200 s should give complete conversion but almost entirely adverse thermal chemistry. The safety risk is likely above the declared limit, although uncertainty is large because this region was not experimentally sampled.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9600 | 0.8100 | 1.0000 |
| conversion | 1.0000 | 0.9900 | 1.0000 |
| safety_risk | 0.4500 | 0.3000 | 0.6400 |
| score | 0.0000 | 0.0000 | 0.0400 |
| selectivity | 0.0200 | 0.0000 | 0.0900 |
| yield | 0.0100 | 0.0000 | 0.0600 |

### Q09

The intermediate catalyst loading and 7200 s at 410 K should nearly exhaust reactant. Based on the observed decline in selectivity with thermal exposure, most additional conversion is predicted to appear as byproduct or degraded material.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7200 | 0.4900 | 0.9000 |
| conversion | 0.9900 | 0.9400 | 1.0000 |
| safety_risk | 0.2300 | 0.1500 | 0.3400 |
| score | 0.1000 | 0.0200 | 0.2200 |
| selectivity | 0.2100 | 0.0800 | 0.3800 |
| yield | 0.1800 | 0.0600 | 0.3400 |

### Q10

Quenching occurs only after the full thermal exposure, so it cannot reverse chemistry already accumulated. I predict results close to Q09, with a small possible preservation benefit during closeout offset by a small additional operational risk; the difference is not strongly identifiable from the campaign.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7000 | 0.4700 | 0.8900 |
| conversion | 0.9900 | 0.9400 | 1.0000 |
| safety_risk | 0.2400 | 0.1600 | 0.3500 |
| score | 0.1100 | 0.0200 | 0.2300 |
| selectivity | 0.2200 | 0.0900 | 0.3900 |
| yield | 0.1900 | 0.0700 | 0.3500 |

### Q11

Although 350 K is within the investigated temperature range, the four-hour residence time is much longer than any favorable campaign run. Conversion should be nearly complete, but prolonged side reaction or product degradation should substantially lower selectivity and yield.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5900 | 0.3800 | 0.7800 |
| conversion | 0.9800 | 0.8900 | 1.0000 |
| safety_risk | 0.2000 | 0.1300 | 0.3000 |
| score | 0.2100 | 0.1000 | 0.3300 |
| selectivity | 0.3600 | 0.2000 | 0.5300 |
| yield | 0.3300 | 0.1800 | 0.4900 |

### Q12

At 465 K, even 1800 s should produce very rapid conversion at the intermediate catalyst loading. The shorter exposure makes this less destructive than Q06 or Q08, but selectivity and yield remain highly uncertain because the temperature is far outside the observed range.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7300 | 0.4800 | 0.9200 |
| conversion | 0.9900 | 0.9100 | 1.0000 |
| safety_risk | 0.2200 | 0.1400 | 0.3400 |
| score | 0.1400 | 0.0400 | 0.2700 |
| selectivity | 0.2400 | 0.0900 | 0.4300 |
| yield | 0.2200 | 0.0700 | 0.4000 |

## K2 — Retrospective analysis

1. Assessment of the initial information

The initial packet contained only one substantive mechanistic prior: “The target pathway may be effectively irreversible on the public support,” with moderate confidence. It also stated that no task-specific material dossier was supplied and that catalyst and solvent effects were latent categorical benchmark effects rather than claims about a named real reaction.

The irreversibility prior received limited, indirect support. In the Catalyst B/acetonitrile sequence, conversion generally increased with thermal exposure: Batch 12 at 350 K for 2700 s gave 0.7681 conversion, Batch 11 at 350 K for 3000 s gave 0.8048, and Batch 9 at 350 K for 3600 s gave 0.8530. Batch 10 at 345 K for 4500 s reached 0.9024. I saw no clear recovery of reactant at longer exposure. This is consistent with an effectively irreversible disappearance of reactant.

However, “consistent with” is not the same as “demonstrated.” I never performed a temperature-reversal, product-spike, equilibrium-relaxation, or repeated time-course experiment capable of testing reversibility directly. The modest non-monotonic differences among separate batches could be explained by temperature, noise, or process variation. Thus, K1 correctly treated irreversibility as a working model, but the campaign did not elevate it beyond moderate confidence.

There was no observed result that clearly contradicted the irreversibility prior and was then ignored. This is a case of “no identified counterevidence,” not a case where counterevidence appeared but I failed to revise the model.

The packet’s warning that solvent identities should not be given literal molecular interpretations was supported methodologically rather than experimentally. I honored it in K1 by describing the solvents as categorical kinetic modifiers and explicitly declining to attribute the effects to polarity or a named synthesis. The campaign could not test that metadata claim.

The absence of a nominal property dossier was important. It meant that my initial choices—maximum reagent, solvent, and catalyst charges, acetonitrile, and moderate heating—were not derived from material properties. They were exploratory assumptions. No initial claim was supplied about the best catalyst, solvent, temperature, time, catalyst order, degradation route, or safety equation.

2. Experiments that formed or changed my judgments

Batch 1 was the first empirical anchor. Catalyst A/acetonitrile at 320 K for 3600 s produced only 0.3710 conversion, 0.2260 yield, 0.6102 selectivity, and a 0.1158 score. It showed that a mild treatment could be safe but unproductive. Because catalyst and temperature were confounded, it did not establish that Catalyst A itself was weak. My subsequent move to 340 K and Catalyst B was partly an optimization guess rather than a conclusion compelled by Batch 1.

Batches 2-4 genuinely formed the catalyst ranking used later. Under common acetonitrile, 340 K, and 3600 s conditions, Catalyst B in Batch 2 gave the highest score, 0.3137, versus 0.2571 for Catalyst C in Batch 3 and 0.2510 for Catalyst D in Batch 4. Catalyst D nevertheless had lower byproduct signal and slightly higher selectivity than Catalyst B. These batches caused me to distinguish productive activity from cleanliness rather than treating catalyst quality as one scalar property.

Batches 5-7 established the solvent tradeoff. With Catalyst B at 340 K for 3600 s, water in Batch 5 was clean and relatively safe but slower; ethanol in Batch 6 was intermediate; acetonitrile in Batch 2 gave the best score; and toluene in Batch 7 combined substantial conversion with poor selectivity and a high byproduct signal. These results made acetonitrile the rational solvent for the optimization phase. The solvent choice was therefore data-driven after Batch 7, even though the original use of acetonitrile in Batch 1 was an unvalidated starting guess.

Batches 8 and 9 altered the temperature interpretation. Batch 8 at 360 K raised conversion to 0.8968 but reduced selectivity to 0.6731 and did not improve score over Batch 2. Batch 9 at 350 K produced a slightly higher score of 0.3182. These results were the clearest evidence that maximizing conversion was not equivalent to maximizing the public objective.

Batch 10 at 345 K for 4500 s was especially influential mechanistically. Its conversion was high, 0.9024, but byproduct signal and degradation warning increased to 0.2988 and 0.2351, while score remained only 0.3150. This strengthened the thermal-exposure interpretation and motivated shorter runs.

Batches 11 and 12 then shifted the operational recommendation toward shorter residence time. At 350 K, reducing duration from 3600 s in Batch 9 to 3000 s in Batch 11 and 2700 s in Batch 12 preserved about 0.60 yield while improving selectivity and score. Batch 12 reached the sample-best score of 0.3265.

Several choices still rested on guesses. Maximum catalyst loading was used in every campaign batch, so the supposedly favorable catalyst loading was never established. Reagent concentration, solvent volume, and stirring were fixed without validation. The exact sequence 3600, 4500, 3000, and 2700 s was local manual search rather than a predeclared design. The decision to use one HPLC measurement immediately before termination in every batch produced useful paired observations, but it was driven partly by the instrument budget and did not constitute a structured kinetic sampling plan.

3. Most important competing mechanisms and what can be distinguished

K1 proposed an operational network with productive conversion, parallel byproduct formation, and possible sequential product degradation:

R → P; R → B; P → D.

The strongest competitor is a purely parallel model in which R forms P and B, with the side pathway having greater temperature sensitivity. In that account, the increasing degradation-warning channel is a correlated impurity signal rather than evidence that P itself decays.

A second competitor is catalyst deactivation or substrate-dependent rate change. Productive formation could slow late in the run while a background side reaction continues. That would create a yield plateau without requiring P → D.

A third competitor is a composite measurement explanation: the apparent yield plateau and changes in selectivity could partly reflect final-assay processing, batch variation, or different response factors as the mixture composition changes. The close qualitative agreement between HPLC and final assay makes a wholly instrumental explanation less likely, but it does not remove it.

The experiments can distinguish a simple single-pathway model from a model containing adverse chemistry. Batch 8 versus Batch 2 and Batch 10 versus Batches 11-12 show that more severe exposure raises conversion while worsening selectivity, byproduct, and degradation indicators. A model in which all converted reactant becomes stable target is therefore contradicted.

The experiments also show that catalyst and solvent cannot be represented solely as global speed multipliers. Catalyst D in Batch 4 was slower but cleaner than Catalyst B in Batch 2, and water in Batch 5 was slower but more selective than acetonitrile. At least two effective parameters—productive activity and adverse-pathway propensity—are needed.

The experiments cannot distinguish parallel R → B from sequential P → D with confidence. They also cannot identify whether “degradation warning” maps to loss of P, loss of R, or a separate impurity. Separate batches at different durations do not provide the same evidential strength as a within-batch trajectory. No catalyst-state or species-resolved material balance was observed. K1’s statement that sequential degradation was “plausible and parsimonious but not uniquely distinguished” remains the appropriate conclusion.

4. One additional complete experiment

If exactly one legal complete experiment were available, I would prioritize mechanism discrimination while retaining direct relevance to the recommended region:

- Charge 0.040 mol reagent, 0.080 L acetonitrile, and 0.005 mol Catalyst B.
- Heat at 350 K and 600 rpm for 2700 s.
- Take the permitted intermediate HPLC measurement.
- Continue heating at 350 K and 600 rpm for a further 4500 s, giving 7200 s total exposure.
- Terminate and obtain the required final assay.

This staged experiment uses the Batch 12 condition as an internal early-time anchor and then deliberately extends exposure. It is preferable to another unrelated endpoint because it asks whether already accumulated target survives continued heating.

If the final conversion increased but final yield fell materially below the intermediate HPLC yield, with a large degradation warning, my confidence in sequential P → D would rise substantially. If conversion increased while target yield merely plateaued and byproduct increased without a convincing target decline, I would favor parallel R → B or catalyst deactivation. If both conversion and yield continued to rise with roughly stable selectivity, then the apparent campaign optimum would look more like noise or batch-to-batch variation, weakening K1’s thermal-damage interpretation. If little changed after the second heating segment, catalyst deactivation or reactant depletion would become more plausible.

The limitation is that the early and final measurements would still come from different instruments. Historical HPLC/final-assay pairs give some estimate of that discrepancy, but they do not eliminate it. If resource rules allowed the same analytical instrument at both stages in addition to the mandatory final assay, matched HPLC measurements would be preferable.

An exact replicate of Batch 12 would be the best single experiment for validating the recommendation, but it would be less discriminating mechanistically. I would choose the staged experiment because the question asks for the most informative addition to the completed research, while acknowledging the tradeoff.

5. Tradeoff between mechanistic identifiability and score optimization

The research objective explicitly prioritized strong safe-score performance under a safety limit. That objective shaped the campaign toward sequential local optimization rather than a balanced factorial or kinetic design.

I did devote early batches to identification. Batches 2-4 compared three catalysts under common conditions, and Batches 2 and 5-7 compared all four solvents under common Catalyst B conditions. Those seven batches sacrificed some immediate optimization opportunity in exchange for categorical effect estimates. In particular, Batch 7’s low score of 0.2112 was useful because it revealed the unfavorable toluene selectivity profile.

After Batch 7, the design became predominantly exploitative. Batches 8-12 all used Catalyst B/acetonitrile and adjusted temperature or duration near the improving region. This produced the best observed score but left catalyst loading, concentration, mixing, and reproducibility unidentified. Batches 11 and 12 differed by only 300 s, which was sensible for local score improvement but not maximally informative about broad kinetics.

There was also an optimization-driven sacrifice in using maximum catalyst loading throughout. It was a plausible way to obtain high conversion within a limited batch count, but it prevented estimation of catalyst order or saturation. Likewise, fixed maximum reagent and solvent charges simplified comparisons but gave no information about concentration effects.

Conversely, Batches 3-7 represent cases where I accepted lower anticipated scores to obtain catalyst and solvent contrasts. The campaign therefore was not pure exploitation. Its main weakness is that the identification phase covered categorical choices but not continuous process variables in a structured way.

6. Underused evidence and weaknesses in the blind predictions

The paired HPLC and final-assay observations were underused quantitatively. K1 noted examples from Batches 2, 11, and 12 and treated discrepancies as mainly instrument noise or processing differences, but I did not estimate an empirical cross-instrument bias or variance. Such an estimate could have better calibrated uncertainty in the apparent yield plateau.

The charging-stage safety observations were also underused. Risk was already nonzero before heating and varied with formulation. I described a charging term plus a thermal term, but I did not fit those contributions separately. This matters for the blind queries, whose absolute volumes and catalyst amounts were much smaller than those in the campaign.

The campaign ledger contained process-time, charging-risk, and heat-risk increments that could have supported a more explicit thermal-risk model. My blind predictions instead used a qualitative extrapolation. Similarly, I inferred an approximate public score relationship from the campaign outcomes, but the blind-query cost scaling was not experimentally validated at those smaller charges.

The least reliable blind predictions are Q06 and Q08, both at 465 K for 7200 s. They extrapolate 105 K above the highest studied setpoint and twice the longest principal 3600 s comparison, into a regime where bounded metrics may saturate and safety behavior may change qualitatively. Q04 at 410 K for 14400 s is also highly uncertain because both temperature and duration are far outside the useful campaign neighborhood. Q12 at 465 K for 1800 s remains unreliable despite its shorter duration because no high-temperature transient data were collected.

Q10 is uniquely uncertain because the campaign never used quench. My prediction that it would resemble Q09 with only a small preservation benefit was an explicit guess. The effect of quench on final chemistry, risk accounting, and score was not identified.

Q01-Q08 also changed catalyst loading substantially, while every campaign batch used 0.005 mol catalyst with 0.040 mol reagent. Treating catalyst loading as an approximately monotonic rate multiplier was unsupported. Q05 and Q07 lie at a familiar temperature but still extrapolate in catalyst-to-reagent ratio, concentration, volume, stirring speed, and duration.

Several intervals were probably too narrow relative to those extrapolations. In particular, Q03’s conversion interval of 0.76-0.98 and score interval of 0.20-0.43 may understate uncertainty about catalyst-order behavior at 410 K. Q07’s score interval of 0.25-0.47 is likely too confident given the untested higher catalyst ratio and doubled exposure. Q12’s conversion interval of 0.91-1.00 assumes near saturation too strongly. The safety intervals for Q06 and Q08 may also be too narrow because no evidence established how the risk model behaves near 465 K.

This overconfidence is partly inconsistent with K1’s explicit applicability limit to 320-360 K, 2700-4500 s, fixed loading, fixed volume, and 600 rpm. The prediction rationales acknowledged extrapolation, but some numeric intervals did not fully reflect the breadth of the uncertainty declared in K1. That is a calibration weakness, not new evidence about the hidden outcomes.

7. Limitations of the sealed recommendation

Batch 12 is the sample-best observed procedure, not a proven global optimum. Its score of 0.3265 was the highest among twelve noisy, adaptively selected batches. It exceeded Batch 11 by only about 0.0037 and Batch 9 by about 0.0082. Those differences may be comparable to combined process and assay variability. No exact replicate was run.

The recommendation is local to one formulation and scale: 0.040 mol reagent, 0.080 L acetonitrile, 0.005 mol Catalyst B, 350 K, 2700 s, and 600 rpm. It does not establish that 2700 s is better than nearby untested times such as 2400, 2550, 2850, or 3000 s in repeated trials. Nor does it establish that maximum catalyst loading, the chosen concentration, or 600 rpm is optimal.

Repeatability should first be tested with several exact independent replicates of Batch 12, reporting distributions of final score, safety risk, conversion, yield, selectivity, byproduct signal, and degradation warning. Replication should precede claims based on the small score advantage.

Local robustness should then be tested with a compact response-surface design around the recommendation—for example, 345, 350, and 355 K crossed with approximately 2400, 2700, and 3000 s—while including center-point replicates. Small perturbations in catalyst loading, solvent volume, and stirring should be added to determine whether performance sits on a broad plateau or a narrow ridge. Safety should be evaluated using upper predictive bounds, not only mean observed risk.

Cross-material generalization would require repeating the local comparison with other catalysts and solvents. The campaign showed that catalyst and solvent altered both rate and selectivity, so the Batch 12 time-temperature optimum should not be transferred unchanged even to Catalyst C, Catalyst D, water, or ethanol. Catalyst A is especially unresolved because it was confounded with the 320 K condition.

Cross-world generalization is weaker still. The materials are anonymous benchmark categories, and the solvent coupling is explicitly synthetic. The procedure should not be presented as a real-chemistry recipe or as transferable to another latent world without new calibration experiments.

Accordingly, the defensible claim is: Batch 12 was the highest-scoring observed batch in this campaign and was comfortably within the stated safety limit. The indefensible stronger claim would be: Batch 12 has been proven reproducible, globally optimal, or transferable across materials, scales, or worlds.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 80.5 | none | 0 |
| Q | yes | 0 | 118.3 | none | 0 |
| K2 | yes | 0 | 103.0 | none | 0 |

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean 80% width | Mean interval score |
|---|---:|---:|---:|---:|
| byproduct_signal | 0.1372 | 0.8167 | 0.3617 | 0.4921 |
| conversion | 0.0293 | 0.9500 | 0.1275 | 0.1313 |
| safety_risk | 0.0615 | 0.6667 | 0.2008 | 0.3319 |
| score | 0.0574 | 0.9167 | 0.1775 | 0.2025 |
| selectivity | 0.1477 | 0.5167 | 0.2617 | 0.7224 |
| yield | 0.1410 | 0.5833 | 0.2458 | 0.7814 |

## Predictions versus released reference truth

### Q01

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2800 | 0.1200 | 0.4800 | 0.1848 | 0.1918, 0.1819, 0.1704, 0.1891, 0.1908 |
| conversion | 0.6200 | 0.3800 | 0.8200 | 0.7137 | 0.7023, 0.7224, 0.7188, 0.7145, 0.7107 |
| safety_risk | 0.1400 | 0.0900 | 0.2200 | 0.2518 | 0.2518, 0.2518, 0.2518, 0.2518, 0.2518 |
| score | 0.2700 | 0.1600 | 0.3800 | 0.3274 | 0.3246, 0.3325, 0.3231, 0.3272, 0.3293 |
| selectivity | 0.5500 | 0.3800 | 0.7000 | 0.7446 | 0.7346, 0.7507, 0.7388, 0.7478, 0.7514 |
| yield | 0.3400 | 0.2000 | 0.5000 | 0.5270 | 0.5292, 0.5340, 0.5188, 0.5246, 0.5285 |
### Q02

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.7600 | 0.5200 | 0.9400 | 0.9165 | 0.9241, 0.9159, 0.9222, 0.9177, 0.9027 |
| conversion | 0.9900 | 0.9400 | 1.0000 | 0.9982 | 1.0000, 1.0000, 1.0000, 1.0000, 0.9911 |
| safety_risk | 0.3000 | 0.2000 | 0.4300 | 0.2522 | 0.2522, 0.2522, 0.2522, 0.2522, 0.2522 |
| score | 0.0600 | 0.0000 | 0.1700 | 0.0065 | 0.0068, 0.0060, 0.0124, 0.0037, 0.0034 |
| selectivity | 0.1500 | 0.0400 | 0.3100 | 0.0907 | 0.0810, 0.0943, 0.1061, 0.0782, 0.0938 |
| yield | 0.1200 | 0.0200 | 0.2700 | 0.0891 | 0.0956, 0.0852, 0.0939, 0.0896, 0.0814 |
### Q03

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4300 | 0.2200 | 0.6500 | 0.2439 | 0.2551, 0.2405, 0.2456, 0.2377, 0.2404 |
| conversion | 0.9100 | 0.7600 | 0.9800 | 0.9840 | 0.9910, 0.9798, 0.9883, 0.9778, 0.9833 |
| safety_risk | 0.1500 | 0.1000 | 0.2300 | 0.2538 | 0.2538, 0.2538, 0.2538, 0.2538, 0.2538 |
| score | 0.3200 | 0.2000 | 0.4300 | 0.4127 | 0.4149, 0.4118, 0.4145, 0.4127, 0.4096 |
| selectivity | 0.5000 | 0.3400 | 0.6500 | 0.7564 | 0.7525, 0.7577, 0.7556, 0.7640, 0.7520 |
| yield | 0.4600 | 0.3000 | 0.6100 | 0.7398 | 0.7460, 0.7376, 0.7438, 0.7366, 0.7348 |
### Q04

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.8400 | 0.6300 | 0.9800 | 0.9599 | 0.9591, 0.9620, 0.9651, 0.9593, 0.9539 |
| conversion | 1.0000 | 0.9700 | 1.0000 | 0.9956 | 1.0000, 0.9911, 1.0000, 0.9919, 0.9949 |
| safety_risk | 0.3100 | 0.2100 | 0.4500 | 0.2525 | 0.2525, 0.2525, 0.2525, 0.2525, 0.2525 |
| score | 0.0200 | 0.0000 | 0.1000 | 0.0000 | 0.0000, 0.0000, 0.0000, 0.0000, 0.0000 |
| selectivity | 0.0900 | 0.0100 | 0.2200 | 0.0756 | 0.0716, 0.0733, 0.0668, 0.0853, 0.0810 |
| yield | 0.0600 | 0.0000 | 0.1800 | 0.0734 | 0.0697, 0.0765, 0.0699, 0.0811, 0.0700 |
### Q05

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2400 | 0.1100 | 0.4100 | 0.4087 | 0.4217, 0.4103, 0.4022, 0.3956, 0.4138 |
| conversion | 0.7100 | 0.5100 | 0.8600 | 0.8430 | 0.8392, 0.8436, 0.8392, 0.8386, 0.8545 |
| safety_risk | 0.1400 | 0.0900 | 0.2100 | 0.1426 | 0.1426, 0.1426, 0.1426, 0.1426, 0.1426 |
| score | 0.3500 | 0.2400 | 0.4500 | 0.2913 | 0.2939, 0.2886, 0.2971, 0.2898, 0.2871 |
| selectivity | 0.6800 | 0.5300 | 0.8100 | 0.5173 | 0.5216, 0.5049, 0.5338, 0.5106, 0.5157 |
| yield | 0.4800 | 0.3300 | 0.6200 | 0.4350 | 0.4399, 0.4358, 0.4401, 0.4365, 0.4227 |
### Q06

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.9400 | 0.7600 | 1.0000 | 0.8233 | 0.8278, 0.8247, 0.8136, 0.8315, 0.8191 |
| conversion | 1.0000 | 0.9700 | 1.0000 | 0.9952 | 0.9988, 0.9901, 0.9926, 0.9947, 1.0000 |
| safety_risk | 0.4300 | 0.2800 | 0.6200 | 0.4261 | 0.4261, 0.4261, 0.4261, 0.4261, 0.4261 |
| score | 0.0100 | 0.0000 | 0.0700 | 0.0000 | 0.0000, 0.0000, 0.0000, 0.0000, 0.0000 |
| selectivity | 0.0300 | 0.0000 | 0.1200 | 0.1871 | 0.1941, 0.1683, 0.1953, 0.1894, 0.1884 |
| yield | 0.0100 | 0.0000 | 0.0800 | 0.1849 | 0.1885, 0.1877, 0.1865, 0.1781, 0.1839 |
### Q07

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4200 | 0.2400 | 0.6200 | 0.5161 | 0.5192, 0.5183, 0.5198, 0.5114, 0.5117 |
| conversion | 0.9900 | 0.9300 | 1.0000 | 0.9945 | 0.9933, 1.0000, 0.9913, 0.9970, 0.9911 |
| safety_risk | 0.1500 | 0.1000 | 0.2300 | 0.1438 | 0.1438, 0.1438, 0.1438, 0.1438, 0.1438 |
| score | 0.3700 | 0.2500 | 0.4700 | 0.2970 | 0.2948, 0.2939, 0.2935, 0.3014, 0.3012 |
| selectivity | 0.5600 | 0.4200 | 0.6900 | 0.4950 | 0.4950, 0.4901, 0.4932, 0.4948, 0.5021 |
| yield | 0.5500 | 0.4000 | 0.6800 | 0.4986 | 0.4935, 0.4928, 0.4919, 0.5092, 0.5058 |
### Q08

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.9600 | 0.8100 | 1.0000 | 0.8563 | 0.8570, 0.8322, 0.8629, 0.8565, 0.8729 |
| conversion | 1.0000 | 0.9900 | 1.0000 | 0.9973 | 1.0000, 0.9919, 1.0000, 1.0000, 0.9945 |
| safety_risk | 0.4500 | 0.3000 | 0.6400 | 0.4263 | 0.4263, 0.4263, 0.4263, 0.4263, 0.4263 |
| score | 0.0000 | 0.0000 | 0.0400 | 0.0000 | 0.0000, 0.0000, 0.0000, 0.0000, 0.0000 |
| selectivity | 0.0200 | 0.0000 | 0.0900 | 0.1701 | 0.1633, 0.1704, 0.1715, 0.1742, 0.1709 |
| yield | 0.0100 | 0.0000 | 0.0600 | 0.1738 | 0.1784, 0.1766, 0.1728, 0.1716, 0.1699 |
### Q09

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.7200 | 0.4900 | 0.9000 | 0.7196 | 0.7083, 0.7133, 0.7299, 0.7153, 0.7310 |
| conversion | 0.9900 | 0.9400 | 1.0000 | 0.9933 | 1.0000, 0.9804, 1.0000, 0.9986, 0.9875 |
| safety_risk | 0.2300 | 0.1500 | 0.3400 | 0.2529 | 0.2529, 0.2529, 0.2529, 0.2529, 0.2529 |
| score | 0.1000 | 0.0200 | 0.2200 | 0.1314 | 0.1360, 0.1316, 0.1277, 0.1341, 0.1277 |
| selectivity | 0.2100 | 0.0800 | 0.3800 | 0.3006 | 0.3108, 0.3002, 0.2918, 0.3038, 0.2963 |
| yield | 0.1800 | 0.0600 | 0.3400 | 0.2924 | 0.2957, 0.2963, 0.2868, 0.2958, 0.2873 |
### Q10

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.7000 | 0.4700 | 0.8900 | 0.7130 | 0.7267, 0.7023, 0.7206, 0.7129, 0.7025 |
| conversion | 0.9900 | 0.9400 | 1.0000 | 0.9922 | 1.0000, 0.9941, 0.9958, 0.9831, 0.9878 |
| safety_risk | 0.2400 | 0.1600 | 0.3500 | 0.1456 | 0.1456, 0.1456, 0.1456, 0.1456, 0.1456 |
| score | 0.1100 | 0.0200 | 0.2300 | 0.1737 | 0.1786, 0.1673, 0.1736, 0.1726, 0.1762 |
| selectivity | 0.2200 | 0.0900 | 0.3900 | 0.2959 | 0.3124, 0.2771, 0.2873, 0.3050, 0.2977 |
| yield | 0.1900 | 0.0700 | 0.3500 | 0.2889 | 0.2891, 0.2842, 0.2933, 0.2828, 0.2953 |
### Q11

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5900 | 0.3800 | 0.7800 | 0.7775 | 0.7826, 0.7700, 0.7824, 0.7723, 0.7800 |
| conversion | 0.9800 | 0.8900 | 1.0000 | 0.9975 | 1.0000, 1.0000, 1.0000, 1.0000, 0.9875 |
| safety_risk | 0.2000 | 0.1300 | 0.3000 | 0.1432 | 0.1432, 0.1432, 0.1432, 0.1432, 0.1432 |
| score | 0.2100 | 0.1000 | 0.3300 | 0.1414 | 0.1452, 0.1394, 0.1458, 0.1449, 0.1317 |
| selectivity | 0.3600 | 0.2000 | 0.5300 | 0.2451 | 0.2573, 0.2426, 0.2622, 0.2561, 0.2075 |
| yield | 0.3300 | 0.1800 | 0.4900 | 0.2426 | 0.2439, 0.2387, 0.2423, 0.2439, 0.2444 |
### Q12

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.7300 | 0.4800 | 0.9200 | 0.3277 | 0.3364, 0.3157, 0.3327, 0.3236, 0.3300 |
| conversion | 0.9900 | 0.9100 | 1.0000 | 0.9933 | 0.9929, 0.9900, 1.0000, 0.9984, 0.9854 |
| safety_risk | 0.2200 | 0.1400 | 0.3400 | 0.4273 | 0.4273, 0.4273, 0.4273, 0.4273, 0.4273 |
| score | 0.1400 | 0.0400 | 0.2700 | 0.3000 | 0.3025, 0.2997, 0.3014, 0.2990, 0.2971 |
| selectivity | 0.2400 | 0.0900 | 0.4300 | 0.6713 | 0.6755, 0.6797, 0.6646, 0.6644, 0.6722 |
| yield | 0.2200 | 0.0700 | 0.4000 | 0.6671 | 0.6710, 0.6621, 0.6732, 0.6677, 0.6612 |

## Recommendation retest

- Selected source batch: `12`
- Retest exact replay verified: `True`
- Retest failure: `none`

| Metric | Selected source batch | Independent retest | Retest minus source |
|---|---:|---:|---:|
| byproduct_signal | 0.1838 | 0.1713 | -0.0125 |
| conversion | 0.7681 | 0.7620 | -0.0061 |
| cost | 1.0000 | 1.0000 | 0.0000 |
| degradation_warning | 0.1157 | 0.0988 | -0.0168 |
| safety_risk | 0.1911 | 0.1911 | 0.0000 |
| score | 0.3265 | 0.3201 | -0.0063 |
| selectivity | 0.7757 | 0.7860 | 0.0103 |
| virtual_spectrum_summary | 0.1531 | 0.1387 | -0.0144 |
| yield | 0.6044 | 0.5836 | -0.0207 |

## Scope note

This is the final sanitized report produced after all 60 source sessions and K1/Q/K2 chains were sealed. It includes released reference truth, blind-prediction evaluation, and the independent recommendation retest. Provider-private event streams, credentials, thread identifiers, and token accounting remain excluded.
