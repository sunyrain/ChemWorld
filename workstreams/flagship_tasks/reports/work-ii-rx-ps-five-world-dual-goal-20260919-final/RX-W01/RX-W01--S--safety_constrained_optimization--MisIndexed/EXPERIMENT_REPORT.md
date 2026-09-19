# RX-W01--S--safety_constrained_optimization--MisIndexed

## Run summary

- World: `RX-W01`
- Locus: `S`
- Goal: `safety_constrained_optimization`
- Arm: `MisIndexed`
- Status: `completed`
- Source status: `completed`
- Experimental sessions: `12/12`
- Operations: `73`
- Exact replay verified: `True`
- Rollbacks: `[]`
- Posttest chain sealed: `True`

### Recovery status

- Effective result location: `posttest-repair-v3`
- Recovery version: `unknown`
- Repaired stages: `Q, K2`
- Source experiments rerun: `False`
- Original source thread reused: `True`
- Truth revealed during recovery: `False`

## Sealed recommendation

- Selected batch: `8`
- Rationale: Batch 8 achieved the highest observed public safe score (0.2907) while remaining safely below the 0.35 risk limit (risk 0.2037).

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S0 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.1763 | 0.4445 | 0.4089 | 0.2500 | 0.0000 | 0.1036 | 0.0759 |
| 2 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.2756 | 0.6437 | 0.4168 | 0.1526 | 0.0258 | 0.1123 | 0.1623 |
| 3 | S0 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.1826 | 0.4933 | 0.3660 | 0.1886 | 0.0118 | 0.1030 | 0.0866 |
| 4 | S0 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.2436 | 0.5948 | 0.3942 | 0.1521 | 0.0308 | 0.1094 | 0.1363 |
| 5 | S1 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.3602 | 0.6402 | 0.5616 | 0.1936 | 0.0351 | 0.1457 | 0.1947 |
| 6 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.4610 | 0.7099 | 0.6498 | 0.1937 | 0.0676 | 0.1763 | 0.2475 |
| 7 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.4370 | 0.6568 | 0.6705 | 0.2140 | 0.0490 | 0.1862 | 0.2223 |
| 8 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 375 K x 3600 s @ 600 rpm | no | 0.5655 | 0.7089 | 0.7895 | 0.2463 | 0.1063 | 0.2037 | 0.2907 |
| 9 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 400 K x 3600 s @ 600 rpm | no | 0.6087 | 0.6819 | 0.8735 | 0.2866 | 0.1460 | 0.2607 | 0.2840 |
| 10 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 425 K x 3600 s @ 600 rpm | no | 0.6141 | 0.6612 | 0.9564 | 0.3363 | 0.2056 | 0.3633 | 0.2431 |
| 11 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 380 K x 3600 s @ 600 rpm | no | 0.5782 | 0.6894 | 0.8199 | 0.2532 | 0.1240 | 0.2116 | 0.2904 |
| 12 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 375 K x 5400 s @ 600 rpm | no | 0.5696 | 0.6271 | 0.9013 | 0.3457 | 0.2046 | 0.2114 | 0.2796 |

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
    "byproduct_signal": 0.25002703070640564,
    "conversion": 0.4089481830596924,
    "cost": 1.0,
    "degradation_warning": 0.0,
    "safety_risk": 0.103555828332901,
    "score": 0.0759432390332222,
    "selectivity": 0.4444863498210907,
    "virtual_spectrum_summary": 0.1375148594379425,
    "yield": 0.17631740868091583
  },
  "ordinal": 1
}
```

### Batch 2

Lifecycle index: `2`; end step: `13`.

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
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 13,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.15262620151042938,
    "conversion": 0.4167596399784088,
    "cost": 1.0,
    "degradation_warning": 0.0258448738604784,
    "safety_risk": 0.11234387010335922,
    "score": 0.16230426728725433,
    "selectivity": 0.6437240839004517,
    "virtual_spectrum_summary": 0.09557460248470306,
    "yield": 0.27563005685806274
  },
  "ordinal": 2
}
```

### Batch 3

Lifecycle index: `3`; end step: `19`.

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
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 19,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.18864992260932922,
    "conversion": 0.36604776978492737,
    "cost": 1.0,
    "degradation_warning": 0.011782958172261715,
    "safety_risk": 0.10303283482789993,
    "score": 0.08659831434488297,
    "selectivity": 0.493337482213974,
    "virtual_spectrum_summary": 0.10905979573726654,
    "yield": 0.18255986273288727
  },
  "ordinal": 3
}
```

### Batch 4

Lifecycle index: `4`; end step: `25`.

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
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 25,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.15211795270442963,
    "conversion": 0.3942277729511261,
    "cost": 1.0,
    "degradation_warning": 0.030761001631617546,
    "safety_risk": 0.10939750075340271,
    "score": 0.1363334357738495,
    "selectivity": 0.5947848558425903,
    "virtual_spectrum_summary": 0.09750732779502869,
    "yield": 0.2436082810163498
  },
  "ordinal": 4
}
```

### Batch 5

Lifecycle index: `5`; end step: `31`.

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
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 31,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.1935557872056961,
    "conversion": 0.5616034865379333,
    "cost": 1.0,
    "degradation_warning": 0.0350925475358963,
    "safety_risk": 0.14565342664718628,
    "score": 0.19474686682224274,
    "selectivity": 0.6402418613433838,
    "virtual_spectrum_summary": 0.12224733084440231,
    "yield": 0.360175222158432
  },
  "ordinal": 5
}
```

### Batch 6

Lifecycle index: `6`; end step: `37`.

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
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 37,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.19373688101768494,
    "conversion": 0.6497737169265747,
    "cost": 1.0,
    "degradation_warning": 0.06759834289550781,
    "safety_risk": 0.1762675791978836,
    "score": 0.24753005802631378,
    "selectivity": 0.709940493106842,
    "virtual_spectrum_summary": 0.1369745433330536,
    "yield": 0.4609699249267578
  },
  "ordinal": 6
}
```

### Batch 7

Lifecycle index: `7`; end step: `43`.

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
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 43,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.21399222314357758,
    "conversion": 0.6705098152160645,
    "cost": 1.0,
    "degradation_warning": 0.04896502196788788,
    "safety_risk": 0.18623198568820953,
    "score": 0.2222672700881958,
    "selectivity": 0.6568121910095215,
    "virtual_spectrum_summary": 0.13972999155521393,
    "yield": 0.43704405426979065
  },
  "ordinal": 7
}
```

### Batch 8

Lifecycle index: `8`; end step: `49`.

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
      "target_temperature_K": 375
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
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.24631766974925995,
    "conversion": 0.7895145416259766,
    "cost": 1.0,
    "degradation_warning": 0.1063142642378807,
    "safety_risk": 0.20366504788398743,
    "score": 0.2907131612300873,
    "selectivity": 0.7089053988456726,
    "virtual_spectrum_summary": 0.18331614136695862,
    "yield": 0.5654615759849548
  },
  "ordinal": 8
}
```

### Batch 9

Lifecycle index: `9`; end step: `55`.

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
      "target_temperature_K": 400
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 55,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.2866078317165375,
    "conversion": 0.8734540343284607,
    "cost": 1.0,
    "degradation_warning": 0.14604057371616364,
    "safety_risk": 0.2607285976409912,
    "score": 0.2839561700820923,
    "selectivity": 0.6818814873695374,
    "virtual_spectrum_summary": 0.2233525663614273,
    "yield": 0.6086706519126892
  },
  "ordinal": 9
}
```

### Batch 10

Lifecycle index: `10`; end step: `61`.

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
      "target_temperature_K": 425
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 61,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.33631545305252075,
    "conversion": 0.9563626050949097,
    "cost": 1.0,
    "degradation_warning": 0.20560140907764435,
    "safety_risk": 0.3633401095867157,
    "score": 0.24307987093925476,
    "selectivity": 0.6611962914466858,
    "virtual_spectrum_summary": 0.2774941325187683,
    "yield": 0.6141189932823181
  },
  "ordinal": 10
}
```

### Batch 11

Lifecycle index: `11`; end step: `67`.

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
      "target_temperature_K": 380
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 67,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.2531798183917999,
    "conversion": 0.8198562860488892,
    "cost": 1.0,
    "degradation_warning": 0.1239844560623169,
    "safety_risk": 0.21162213385105133,
    "score": 0.2903722822666168,
    "selectivity": 0.6894009113311768,
    "virtual_spectrum_summary": 0.19504190981388092,
    "yield": 0.5781659483909607
  },
  "ordinal": 11
}
```

### Batch 12

Lifecycle index: `12`; end step: `73`.

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
      "stirring_speed_rpm": 600,
      "target_temperature_K": 375
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 73,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.3456916809082031,
    "conversion": 0.9013042449951172,
    "cost": 1.0,
    "degradation_warning": 0.2045775204896927,
    "safety_risk": 0.21143418550491333,
    "score": 0.2795925438404083,
    "selectivity": 0.6271184682846069,
    "virtual_spectrum_summary": 0.28219032287597656,
    "yield": 0.5695697069168091
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

1. Scope and evidence base

This interpretation is based only on the 12 completed campaign batches and their public measurements. It describes the anonymous synthetic benchmark world, not a real named reaction. Every batch used 0.040 mol reagent, 0.080 L solvent, and 0.005 mol catalyst, corresponding nominally to 0.50 mol/L reagent and 0.0625 mol/L catalyst before sampling. All heated batches used 600 rpm stirring. Consequently, the campaign identifies categorical catalyst and solvent effects and a limited temperature/time response, but it does not identify concentration, catalyst-loading, mixing, or scale laws.

Final-assay values include synthetic measurement noise. Small differences should therefore not be overinterpreted. The reported score was observed directly; I did not infer its exact proprietary formula.

2. Proposed process structure

A minimal mechanism consistent with the observations is:

R ⇌ P
R → B
P → B and/or D

Here R is the public reactant, P the desired target, B a non-target byproduct pool, and D a degradation pool. Catalyst, solvent, and temperature change the effective rate constants and possibly the equilibrium position.

One useful phenomenological model is:

dR/dt = -kP R - kB R + k−P P
dP/dt = kP R - k−P P - kD P
dB/dt = kB R + αkD P
dD/dt = (1-α)kD P

with

ki = Ai(catalyst, solvent) exp[-Ei/(RT)].

This is not claimed as a uniquely identified law. It is a compact way to express four robust features of the data:

• catalysts strongly alter productive selectivity;
• solvents alter both conversion and selectivity;
• heating initially raises target yield;
• excessive temperature or residence time increasingly favors byproduct and degradation channels, causing target yield to plateau while conversion continues upward.

The supplied prior stated that an appreciable reverse channel might exist. The campaign remains compatible with that prior, but does not uniquely demonstrate reversibility. Parallel side reactions plus secondary product degradation explain the observations at least as well.

3. Catalyst effects

Batches 1–4 compared all catalysts in water at 350 K for 3600 s.

• Batch 1, Catalyst A: conversion 0.40895, selectivity 0.44449, yield 0.17632, byproduct 0.25003, degradation 0.00000, risk 0.10356, score 0.07594.
• Batch 2, Catalyst B: conversion 0.41676, selectivity 0.64372, yield 0.27563, byproduct 0.15263, degradation 0.02584, risk 0.11234, score 0.16230.
• Batch 3, Catalyst C: conversion 0.36605, selectivity 0.49334, yield 0.18256, byproduct 0.18865, degradation 0.01178, risk 0.10303, score 0.08660.
• Batch 4, Catalyst D: conversion 0.39423, selectivity 0.59478, yield 0.24361, byproduct 0.15212, degradation 0.03076, risk 0.10940, score 0.13633.

The main advantage of Catalyst B was selectivity rather than a large conversion increase: its conversion was only slightly above Catalyst A, but its selectivity rose from 0.444 to 0.644 and its byproduct signal fell from 0.250 to 0.153. Catalyst D was second best. This suggests that catalyst identity primarily changes the branching ratio kP/(kP+kB), although modest changes in overall rate and degradation are also possible.

Catalyst B was selected for subsequent work. That conclusion is directly supported only in water at one temperature and time. Catalyst–solvent interactions were not mapped, so another catalyst could conceivably outperform B in another solvent.

4. Solvent effects

Batches 2 and 5–7 compared solvents using Catalyst B at 350 K for 3600 s.

• Batch 2, water: conversion 0.41676, selectivity 0.64372, yield 0.27563, risk 0.11234, score 0.16230.
• Batch 5, ethanol: conversion 0.56160, selectivity 0.64024, yield 0.36018, risk 0.14565, score 0.19475.
• Batch 6, acetonitrile: conversion 0.64977, selectivity 0.70994, yield 0.46097, risk 0.17627, score 0.24753.
• Batch 7, toluene: conversion 0.67051, selectivity 0.65681, yield 0.43704, risk 0.18623, score 0.22227.

Acetonitrile gave the best balance. Relative to water, it raised both conversion and selectivity, producing a much larger yield. Toluene gave slightly higher conversion than acetonitrile but lower selectivity, more byproduct signal (0.21399 versus 0.19374), greater risk, and a lower score. Ethanol was intermediate.

In the model, these results can be represented by solvent-dependent rate prefactors and branching ratios. Acetonitrile appears to increase the productive rate relative to the competing pathway. However, because the benchmark explicitly treats solvents as categorical kinetic effects, these results should not be assigned to real-world polarity, boiling point, or other physical properties without additional evidence.

5. Temperature response in the selected catalyst–solvent system

Batches 6 and 8–11 used Catalyst B in acetonitrile for 3600 s:

• 350 K, Batch 6: conversion 0.64977, selectivity 0.70994, yield 0.46097, byproduct 0.19374, degradation 0.06760, risk 0.17627, score 0.24753.
• 375 K, Batch 8: conversion 0.78951, selectivity 0.70891, yield 0.56546, byproduct 0.24632, degradation 0.10631, risk 0.20367, score 0.29071.
• 380 K, Batch 11: conversion 0.81986, selectivity 0.68940, yield 0.57817, byproduct 0.25318, degradation 0.12398, risk 0.21162, score 0.29037.
• 400 K, Batch 9: conversion 0.87345, selectivity 0.68188, yield 0.60867, byproduct 0.28661, degradation 0.14604, risk 0.26073, score 0.28396.
• 425 K, Batch 10: conversion 0.95636, selectivity 0.66120, yield 0.61412, byproduct 0.33632, degradation 0.20560, risk 0.36334, score 0.24308. This batch exceeded the declared 0.35 safety limit.

Conversion increased monotonically with temperature. Target yield also increased, but with sharply diminishing returns above about 380–400 K. Meanwhile, selectivity declined, byproduct and degradation signals rose, and safety risk increased strongly. Thus the side/degradation channels have an effective temperature sensitivity comparable to or greater than the productive channel. The optimum safe score occurred before maximum conversion or maximum yield.

Batch 8 at 375 K had the highest observed score, 0.29071. Batch 11 at 380 K was statistically and practically very close at 0.29037, but had greater observed risk and degradation. Batch 9 generated more target yield, yet its extra yield did not compensate for reduced selectivity, larger byproduct/degradation signals, and higher risk. Batch 10 illustrates the failure of conversion maximization as an operating objective: it had the greatest conversion, but was unsafe and scored poorly relative to Batches 8 and 11.

6. Residence-time effect

Batch 12 repeated the Catalyst B/acetonitrile/375 K condition with 5400 s rather than 3600 s:

• Batch 8, 3600 s: conversion 0.78951, selectivity 0.70891, yield 0.56546, byproduct 0.24632, degradation 0.10631, risk 0.20367, score 0.29071.
• Batch 12, 5400 s: conversion 0.90130, selectivity 0.62712, yield 0.56957, byproduct 0.34569, degradation 0.20458, risk 0.21143, score 0.27959.

The extra 1800 s substantially increased conversion but produced almost no target-yield gain. Instead, selectivity fell and both byproduct and degradation signals increased strongly. This is the clearest evidence for a late-time loss process. Plausible explanations include secondary degradation of P, depletion-induced competition, approach to a reversible equilibrium followed by degradation, or a slow parallel reaction that becomes important at long residence time.

The experiment does not distinguish these alternatives because no time-resolved concentration profile was collected. Nevertheless, it establishes operationally that extending the 375 K hold beyond 3600 s is counterproductive for the public safe score.

7. Safety behavior and coupling to performance

Observed safety risk depended on material choices, temperature, and weakly on residence time. At identical 350 K/3600 s conditions with Catalyst B, risk rose from 0.112 in water to 0.146 in ethanol, 0.176 in acetonitrile, and 0.186 in toluene. Within the selected acetonitrile system it rose from 0.176 at 350 K to 0.204 at 375 K, 0.212 at 380 K, 0.261 at 400 K, and 0.363 at 425 K.

The 375 K time extension raised risk only from 0.204 to 0.211 while markedly changing composition. This suggests that peak temperature and categorical recipe terms dominate the reported risk, with duration or accumulated chemistry contributing less over the tested interval. A simple operational approximation would be

risk ≈ hsolvent + hcatalyst + f(T) + g(T,t,composition),

where f(T) becomes strongly nonlinear at high temperature. The available points do not justify a unique functional form. Interpolation suggests that the safety boundary lies somewhere between 400 and 425 K for this exact recipe and duration, but using an interpolated boundary as an operating target would be poor practice because only 425 K was directly observed to violate the limit.

8. Relation between yield, selectivity, conversion, and score

Across most batches, yield was approximately conversion multiplied by selectivity, allowing for measurement noise and channel-specific calibration. The score was not simply yield: high risk, byproduct, degradation, and/or lower selectivity reduced performance. For example, Batch 9 had a higher yield than Batch 8 (0.60867 versus 0.56546) but a lower score (0.28396 versus 0.29071). Batch 10 increased yield only slightly further while becoming unsafe and falling to a score of 0.24308.

I therefore interpret the practical objective as maximizing productive formation while avoiding excessive side chemistry and thermal hazard, rather than maximizing conversion alone.

9. Measurement consistency

Batch 1 was the only batch with an intermediate HPLC measurement. Immediately after heating it reported conversion 0.40275, selectivity 0.41323, yield 0.19254, and byproduct 0.23269. The final assay later reported conversion 0.40895, selectivity 0.44449, yield 0.17632, and byproduct 0.25003. No further reaction step occurred between those measurements other than termination. The differences are modest and consistent with instrument-specific noise/calibration rather than strong continued chemistry. This comparison supports treating small assay differences cautiously.

10. Recommended operating region

The sealed recommendation was Batch 8:

• 0.080 L acetonitrile
• 0.040 mol reagent
• 0.005 mol Catalyst B
• heat at 375 K for 3600 s
• stir at 600 rpm
• terminate and assay

It achieved the highest observed score, 0.29071, with risk 0.20367, comfortably below the 0.35 limit. Batch 11 at 380 K was nearly tied, but it offered no score advantage and showed greater degradation and risk. The recommendation is therefore based on actual observed performance rather than an extrapolated optimum.

11. Identifiability limits

Several quantities remain unidentified:

• No catalyst-loading or reagent-concentration series was performed, so kinetic order and saturation behavior are unknown.
• Only one solvent was used for the temperature and time studies; temperature responses may differ in other solvents.
• Catalyst–solvent interactions are confounded because the complete 4×4 categorical matrix was not tested.
• Stirring was fixed at 600 rpm, so mass-transfer limitation cannot be excluded.
• There was only one deliberate residence-time comparison and no dense time course, preventing separation of reversibility, parallel byproduct formation, and sequential degradation.
• Each condition had one final assay, so process variability cannot be separated from stated instrument noise.
• The exact safety-risk and score equations are not public and cannot be reconstructed uniquely from 12 observations.
• Because all recipes used the maximum tested catalyst, reagent, and solvent amounts, a lower-cost formulation may exist. Every completed recipe carried a high-cost flag, so cost optimization was not achieved.

12. Reasonable competing explanations

The preferred interpretation invokes productive formation plus parallel and secondary loss pathways. Other explanations remain viable:

• A purely irreversible parallel network R→P and R→B could explain much of the catalyst and solvent behavior; the late-time yield plateau could then arise from reactant depletion rather than reverse reaction.
• A sequential pathway R→P→B/D could explain the time and temperature trends without a reverse channel.
• Temperature-dependent assay response or changing matrix effects could contribute to apparent selectivity changes, although the coordinated rise in byproduct and degradation signals favors genuine process chemistry.
• Catalyst B may not intrinsically be more selective; it may simply place the fixed 3600 s observation closer to its kinetic optimum. Time courses for every catalyst would be needed to distinguish intrinsic branching from different rates.
• Solvent effects may reflect categorical benchmark parameters that simultaneously change kinetics and risk, rather than a single mechanistic solvent property.

13. Overall conclusion

Within the tested domain, the world behaves like a temperature-accelerated reaction network in which catalyst and solvent control both rate and pathway branching. Catalyst B strongly improves productive selectivity, and acetonitrile gives the best observed combination of conversion and selectivity. Raising temperature increases conversion but increasingly activates byproduct formation, degradation, and safety risk. Extending residence time at 375 K similarly drives conversion without materially improving target yield. These coupled effects produce a broad optimum near 375–380 K for a 3600 s hold, with Batch 8 providing the best directly observed safe-score performance. Reversibility is plausible but unproven; secondary degradation or slow parallel chemistry is at least equally consistent with the available evidence.

## Q — Blind predictions

### Overall rationale

Predictions use a phenomenological productive-formation/secondary-loss model anchored to the Catalyst B–acetonitrile campaign data. The query reagent concentration is 0.60 mol/L versus 0.50 mol/L in the campaign; low, middle, and high catalyst concentrations are approximately 0.024, 0.063, and 0.104 mol/L versus 0.0625 mol/L in the campaign. Conversion was projected to accelerate with temperature and catalyst concentration, while target material was allowed to undergo time- and temperature-dependent loss into the byproduct channel. Safety estimates account qualitatively for the much smaller absolute batch size, but their intervals include substantial uncertainty because the campaign did not identify scale, catalyst-loading, stirring, quench, or high-temperature risk laws. Score estimates emphasize yield and selectivity with penalties for risk and extensive side chemistry. The intervals represent structural extrapolation uncertainty in addition to final-assay noise.

### Q01

The low catalyst concentration should limit conversion during the short 410 K hold, while the short exposure should preserve high selectivity. This extrapolates the Catalyst B/acetonitrile temperature trend beyond the tested loading range.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.0720 | 0.0200 | 0.2000 |
| conversion | 0.3610 | 0.2000 | 0.5600 |
| safety_risk | 0.0200 | 0.0050 | 0.0700 |
| score | 0.2250 | 0.0800 | 0.3800 |
| selectivity | 0.7990 | 0.6200 | 0.9100 |
| yield | 0.2880 | 0.1400 | 0.4400 |

### Q02

Four hours at 410 K should drive nearly complete conversion even at low catalyst loading, but Batch 12 indicates that prolonged exposure redirects material toward byproduct or degradation. The long-time extrapolation makes the yield and selectivity intervals especially wide.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7230 | 0.4500 | 0.9000 |
| conversion | 0.9720 | 0.8300 | 1.0000 |
| safety_risk | 0.0550 | 0.0150 | 0.1800 |
| score | 0.0600 | 0.0100 | 0.2000 |
| selectivity | 0.2560 | 0.0800 | 0.4800 |
| yield | 0.2490 | 0.0800 | 0.4700 |

### Q03

The high catalyst concentration should produce rapid conversion during the short hold while avoiding much of the late-time target loss. This is predicted to be the strongest of the 410 K corner conditions, although catalyst-loading behavior was not measured.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1890 | 0.0800 | 0.3800 |
| conversion | 0.8560 | 0.7000 | 0.9600 |
| safety_risk | 0.0250 | 0.0060 | 0.0800 |
| score | 0.5050 | 0.2500 | 0.6800 |
| selectivity | 0.7790 | 0.6200 | 0.8900 |
| yield | 0.6660 | 0.4600 | 0.8000 |

### Q04

High catalyst loading and a four-hour 410 K exposure should exhaust reactant early and leave substantial time for secondary loss. Conversion is therefore predicted near unity, but useful yield and selectivity are highly uncertain and likely poor.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8320 | 0.6100 | 0.9700 |
| conversion | 1.0000 | 0.9600 | 1.0000 |
| safety_risk | 0.0650 | 0.0200 | 0.2000 |
| score | 0.0260 | 0.0000 | 0.1400 |
| selectivity | 0.1680 | 0.0300 | 0.3800 |
| yield | 0.1680 | 0.0300 | 0.3800 |

### Q05

At 350 K, low catalyst loading should make conversion moderate even after two hours. Lower temperature should preserve selectivity better than the long 410 K cases, but prolonged target loss remains possible.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1870 | 0.0700 | 0.3600 |
| conversion | 0.5360 | 0.3200 | 0.7300 |
| safety_risk | 0.0150 | 0.0030 | 0.0600 |
| score | 0.2240 | 0.0800 | 0.3700 |
| selectivity | 0.6510 | 0.4800 | 0.8000 |
| yield | 0.3490 | 0.1900 | 0.5000 |

### Q06

The 465 K condition is well beyond the studied range and should give almost complete conversion despite low catalyst loading. Strong thermal byproduct and degradation channels are expected to leave little target after two hours; both chemical and safety intervals are deliberately broad.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7930 | 0.5500 | 0.9600 |
| conversion | 0.9830 | 0.8800 | 1.0000 |
| safety_risk | 0.0850 | 0.0200 | 0.2800 |
| score | 0.0340 | 0.0000 | 0.1600 |
| selectivity | 0.1940 | 0.0400 | 0.4300 |
| yield | 0.1900 | 0.0400 | 0.4200 |

### Q07

High catalyst concentration at 350 K should reach high conversion within two hours while avoiding the severe temperature-driven loss expected at 410–465 K. Some secondary loss is still expected because the hold exceeds the one-hour campaign baseline.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4010 | 0.2400 | 0.5900 |
| conversion | 0.9640 | 0.8400 | 1.0000 |
| safety_risk | 0.0300 | 0.0060 | 0.0900 |
| score | 0.3190 | 0.1600 | 0.4700 |
| selectivity | 0.5840 | 0.4200 | 0.7200 |
| yield | 0.5630 | 0.3900 | 0.7000 |

### Q08

This combines the highest catalyst concentration with the most severe temperature and a long hold. Reactant disappearance should be complete, but extensive secondary chemistry should dominate. It is among the least reliable predictions because both loading and temperature are outside the observed support.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8750 | 0.6600 | 0.9900 |
| conversion | 1.0000 | 0.9800 | 1.0000 |
| safety_risk | 0.1100 | 0.0250 | 0.3200 |
| score | 0.0140 | 0.0000 | 0.1000 |
| selectivity | 0.1250 | 0.0100 | 0.3400 |
| yield | 0.1250 | 0.0100 | 0.3400 |

### Q09

The catalyst concentration is almost identical to the campaign concentration, making this the most direct loading comparison. At 410 K for two hours, conversion should approach completion, while extended thermal exposure should reduce selectivity and target yield.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5480 | 0.3800 | 0.7300 |
| conversion | 0.9910 | 0.9100 | 1.0000 |
| safety_risk | 0.0400 | 0.0100 | 0.1400 |
| score | 0.1900 | 0.0700 | 0.3300 |
| selectivity | 0.4470 | 0.2600 | 0.6100 |
| yield | 0.4420 | 0.2500 | 0.6000 |

### Q10

Because quenching occurs only after the full heat exposure, I predict composition close to Q09, with at most a small benefit from arresting post-heat chemistry. No paired quench experiment was performed, so its intervals are wider and overlap Q09 strongly.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5400 | 0.3400 | 0.7500 |
| conversion | 0.9910 | 0.9000 | 1.0000 |
| safety_risk | 0.0350 | 0.0050 | 0.1400 |
| score | 0.1950 | 0.0600 | 0.3500 |
| selectivity | 0.4550 | 0.2400 | 0.6500 |
| yield | 0.4500 | 0.2300 | 0.6300 |

### Q11

Four hours at 350 K should eventually produce high conversion at the campaign-like catalyst concentration, but the long residence time should cause appreciable target loss. The lower temperature moderates degradation relative to the long 410 K cases.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6180 | 0.4100 | 0.8200 |
| conversion | 0.9820 | 0.8400 | 1.0000 |
| safety_risk | 0.0250 | 0.0050 | 0.1000 |
| score | 0.1300 | 0.0300 | 0.2800 |
| selectivity | 0.3700 | 0.1800 | 0.5700 |
| yield | 0.3640 | 0.1700 | 0.5600 |

### Q12

At campaign-like catalyst concentration, 465 K should give rapid conversion within 1800 s. The shorter exposure should retain substantially more target than Q06 or Q08, although extrapolation above 425 K makes the thermal-loss and risk estimates uncertain.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3880 | 0.2200 | 0.5700 |
| conversion | 0.9300 | 0.8000 | 0.9900 |
| safety_risk | 0.0450 | 0.0100 | 0.1800 |
| score | 0.3000 | 0.1300 | 0.4800 |
| selectivity | 0.5830 | 0.4200 | 0.7300 |
| yield | 0.5420 | 0.3500 | 0.7000 |

## K2 — Retrospective analysis

1. Initial claims: supported, contradicted, or untested

The initial packet contained only one substantive mechanistic prior: “The target pathway may have an appreciable reverse channel,” with moderate confidence. It supplied no task-specific rate constants, safety law, catalyst-loading model, or nominal solvent ranking.

The reverse-channel claim remained possible but was not established. Batch 12 was the most suggestive observation: extending the Catalyst B/acetonitrile/375 K hold from 3600 s in Batch 8 to 5400 s increased conversion from 0.7895 to 0.9013, while yield changed only from 0.5655 to 0.5696 and selectivity fell from 0.7089 to 0.6271. This is compatible with reversibility, but it is equally compatible with sequential product degradation or a slow parallel side reaction. K1 therefore correctly stated that “Reversibility is plausible but unproven.”

No result clearly contradicted reversibility. That is only an absence of contrary evidence, not positive verification. There was no equilibrium perturbation, product-fed experiment, temperature-reversal experiment, or sufficiently resolved time course. I did not observe a clear refutation and then neglect to revise the model; rather, the experiments never discriminated the claim.

The packet also warned that solvent effects were categorical benchmark effects rather than real-property predictions. K1 respected this by declining to attribute acetonitrile’s performance to polarity or another real solvent property. That policy itself was not experimentally tested.

2. Experiments that genuinely formed or changed my judgments

Batches 1–4 formed the catalyst judgment. Under water/350 K/3600 s conditions, Catalyst B in Batch 2 gave conversion similar to Catalyst A in Batch 1 but much higher selectivity, 0.6437 versus 0.4445, and lower byproduct signal, 0.1526 versus 0.2500. This led to the K1 interpretation that Catalyst B mainly improved pathway branching rather than merely accelerating total conversion.

Batches 5–7 formed the solvent judgment. With Catalyst B at 350 K, acetonitrile in Batch 6 gave yield 0.4610 and score 0.2475, outperforming ethanol, water, and toluene. Batch 7 was particularly informative because toluene gave slightly higher conversion than acetonitrile but worse selectivity, risk, and score. That prevented me from treating conversion alone as the optimization target.

Batches 8–10 changed the thermal interpretation. Raising temperature increased conversion and yield, but also byproduct, degradation, and risk. Batch 10 reached conversion 0.9564 at 425 K but exceeded the 0.35 safety limit with risk 0.3633 and scored only 0.2431. This directly established that the safe-score optimum occurred before maximum conversion.

Batch 11 tested the local region near Batch 8. Its 380 K score of 0.29037 was nearly tied with Batch 8’s 0.29071, supporting a broad favorable region rather than a sharply identified optimum.

Batch 12 most strongly changed the mechanistic interpretation by showing late-time conversion–yield decoupling. It motivated the K1 statement that “extending the 375 K hold beyond 3600 s is counterproductive,” while leaving the cause unresolved.

Several initial choices were guesses: maximum catalyst and reagent amounts, 600 rpm, 350 K, and a 3600 s baseline were not derived from the material packet. The catalyst screen was driven by categorical ignorance. Later solvent and temperature choices were data-driven. The 425 K experiment was chosen to bracket performance and safety, while Batch 12 deliberately traded likely score for information about residence time.

The pseudo-first-order catalyst and temperature extrapolation used for the sealed Q predictions was developed after the campaign; it was not a model I had already established during the experiments. It should not be retroactively presented as having guided the campaign.

3. Leading competing mechanisms

The principal alternatives remain:

• Reversible productive formation with side chemistry: R ⇌ P, R → B, and possibly P → D.
• Irreversible parallel formation: R → P and R → B.
• Sequential target loss: R → P → B/D, potentially alongside R → B.
• State-dependent behavior such as catalyst activation or deactivation, phase effects, or changing assay response.

The campaign distinguishes several coarse facts. Catalyst identity changes observed selectivity. Solvent identity changes both conversion and pathway allocation. Higher temperature accelerates reactant disappearance while making non-target channels and safety risk more important. Longer residence time can raise conversion without materially improving target yield.

It does not distinguish equilibrium limitation from sequential degradation. In Batch 12, constant target yield could represent continued formation balanced by degradation, an equilibrium-limited target pool, or increasing parallel consumption of remaining reactant. The degradation-warning increase favors genuine loss chemistry, but it does not establish that the target is the degradation precursor. Nor can the catalyst screen separate intrinsic branching selectivity from different catalysts merely occupying different positions along their kinetic trajectories.

Consequently, the equations in K1 were a useful phenomenological representation, not an identified reaction law. Kinetic order, activation energies, catalyst saturation, and reverse-rate magnitude remain unknown.

4. One additional complete experiment

I would run one time-resolved batch at the recommended composition: 0.080 L acetonitrile, 0.040 mol reagent, 0.005 mol Catalyst B, 375 K, and 600 rpm. I would collect intermediate HPLC measurements after cumulative heating times of approximately 900, 1800, 3600, 5400, and 7200 s, then terminate and obtain a final assay. The campaign left most nonfinal instrument capacity unused, so such repeated measurements would have been the highest-value use of one additional vessel, subject to accounting for the small destructive sampling volumes.

Interpretation of possible outcomes:

• A target concentration that rises, peaks, and then falls while conversion remains high and degradation rises would strongly favor sequential P → B/D loss.
• Stable nonzero reactant and target proportions with little further degradation would increase confidence in reversible R ⇌ P equilibrium.
• Nearly constant target with continuing reactant loss and increasing byproduct would favor a slow parallel R → B pathway, although balanced production and degradation could still imitate it.
• No meaningful change after 3600 s would suggest that the Batch 8/12 difference contained more process or measurement variation than K1 assumed.
• Abrupt or non-smooth changes would increase the plausibility of catalyst-state or phase-dependent explanations.

This would still not prove reversibility because the legal inputs did not permit starting with added target. It would, however, convert the present two-point residence-time comparison into a trajectory capable of rejecting some alternatives.

5. Identifiability versus operating score

The study increasingly prioritized safe-score optimization. The catalyst and solvent screens served both optimization and interpretation, but they were one-factor slices, not a crossed catalyst-by-solvent design. After Batch 6, most experiments concentrated on Catalyst B/acetonitrile because that was the best observed combination. This improved the recommendation but left catalyst–solvent interactions unidentified.

Batches 8–11 primarily mapped the useful thermal operating region. They were effective for score and safety, but replicates or a balanced response-surface design would have provided better uncertainty estimates. Batch 12 was the clearest deliberate sacrifice of expected score for mechanistic information: the longer hold was unlikely to beat Batch 8, but it tested whether additional conversion still produced useful target.

Conversely, using maximum catalyst in every campaign batch simplified categorical comparison but sacrificed both cost optimization and catalyst-order identification. Every recipe received a high-cost flag. A lower catalyst loading might have improved practical performance, but the campaign never tested it.

Thus optimization reduced identifiability, while the limited mechanistic probe in Batch 12 consumed a batch that could otherwise have refined the score optimum. Those tradeoffs were reasonable for the stated primary goal, but they preclude claims of a fully identified mechanism or global optimum.

6. Underused evidence and weaknesses in the sealed predictions

The raw characterization artifacts were underused. I relied mostly on processed estimates and summary peaks rather than examining full calibration metadata, raw traces, replicate signals, missingness, mass balance, or possible saturation flags. Only Batch 1 had an intermediate HPLC measurement. Most of the nonfinal measurement allowance was unused, and no condition was replicated.

The least reliable sealed predictions are Q06 and Q08, which extrapolate to 465 K for 7200 s; Q02 and Q04, which extrapolate to 14400 s at 410 K; and Q10, whose quench effect had no campaign analogue. Q12 also extrapolates 40 K above the highest tested temperature, despite its shorter hold. Q01–Q08 further depend on unmeasured catalyst-loading effects.

Several sealed intervals may be too narrow:

• Q08 assigned conversion 0.98–1.00 and Q04 assigned 0.96–1.00. Near-complete conversion is plausible, but those narrow intervals assume monotonic catalyst and Arrhenius scaling despite no loading series and no observations above 425 K.
• Q06 and Q08 gave safety-risk upper bounds of 0.28 and 0.32. These exclude the 0.35 limit even though Batch 10 was already unsafe at 425 K. The prediction assumed that the much smaller absolute batch size strongly reduced risk, but K1 explicitly stated that the scale and risk laws were unidentified. The upper bounds should therefore have allowed more possibility of unexpectedly high risk.
• Q12’s safety interval of 0.01–0.18 may likewise be overconfident at 465 K.
• Q01’s selectivity interval of 0.62–0.91 assumes that low catalyst loading mainly slows conversion while preserving pathway selectivity. That separation was never experimentally tested.
• Q10 was predicted very close to Q09, based on the assumption that post-heat quenching would only arrest subsequent chemistry. Since no paired quench comparison existed, a larger compositional or risk effect should have remained plausible.

The yield, selectivity, and score intervals for the long high-temperature cases were broader, appropriately reflecting structural uncertainty, but even they depended on an unverified sequential-loss model. These weaknesses are consistent with the limitations listed in K1—no loading series, no kinetic order, one time comparison, fixed stirring, no replicates, and no public score or safety equation—but any narrow Q intervals are not fully consistent with that caution.

7. Limitations of the sealed recommendation

Batch 8 was the sample-internal winner, not a proven optimum. Its score of 0.29071 exceeded Batch 11’s 0.29037 by only 0.00034, much less than would justify a strong claim that 375 K is intrinsically superior to 380 K. The evidence supports a favorable region around 375–380 K, not an exact optimum.

The recommendation was observed only once. Repeatability should be assessed with independent replicates that estimate the distributions of score, risk, yield, and degradation. Local robustness should be tested by varying temperature around 365–385 K, duration around 3000–4200 s, catalyst loading, and stirring speed. This would show whether normal control errors preserve performance.

Cost robustness is unresolved because catalyst loading was never varied. Safety robustness also requires deliberate margin testing: Batch 8 was comfortably below the limit, but the nonlinear rise culminating in Batch 10 shows that temperature excursions cannot be evaluated from a linear assumption.

Cross-material generalization is weak. Catalyst B was selected from a catalyst screen conducted only in water, while the solvent screen used only Catalyst B. A crossed catalyst-by-solvent design is required before declaring that pairing globally best within this world. Cross-world or real-chemistry generalization is weaker still because the materials were anonymous categorical benchmark formulations.

The defensible conclusion is therefore limited: Batch 8 was the highest-scoring completed batch among the 12 tested and provides a reasonable empirical operating recommendation for this specific benchmark world. It has not been shown to be uniquely optimal, repeatable, locally insensitive, cheapest, or transferable.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 85.9 | none | 0 |
| Q | yes | 0 | 116.2 | none | 0 |
| K2 | yes | 0 | 63.1 | none | 0 |

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean 80% width | Mean interval score |
|---|---:|---:|---:|---:|
| byproduct_signal | 0.0733 | 1.0000 | 0.3492 | 0.3492 |
| conversion | 0.0307 | 1.0000 | 0.1733 | 0.1733 |
| safety_risk | 0.2066 | 0.0000 | 0.1425 | 1.1339 |
| score | 0.0518 | 1.0000 | 0.2558 | 0.2558 |
| selectivity | 0.0813 | 0.8333 | 0.3425 | 0.3575 |
| yield | 0.0614 | 0.9667 | 0.3500 | 0.3520 |

## Predictions versus released reference truth

### Q01

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.0720 | 0.0200 | 0.2000 | 0.1660 | 0.1755, 0.1675, 0.1685, 0.1634, 0.1550 |
| conversion | 0.3610 | 0.2000 | 0.5600 | 0.4974 | 0.4904, 0.4986, 0.4894, 0.5090, 0.4995 |
| safety_risk | 0.0200 | 0.0050 | 0.0700 | 0.2382 | 0.2382, 0.2382, 0.2382, 0.2382, 0.2382 |
| score | 0.2250 | 0.0800 | 0.3800 | 0.2176 | 0.2177, 0.2151, 0.2192, 0.2149, 0.2213 |
| selectivity | 0.7990 | 0.6200 | 0.9100 | 0.6682 | 0.6668, 0.6747, 0.6838, 0.6463, 0.6693 |
| yield | 0.2880 | 0.1400 | 0.4400 | 0.3393 | 0.3421, 0.3286, 0.3353, 0.3432, 0.3471 |
### Q02

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.7230 | 0.4500 | 0.9000 | 0.7907 | 0.7883, 0.7816, 0.7919, 0.7950, 0.7966 |
| conversion | 0.9720 | 0.8300 | 1.0000 | 0.9955 | 1.0000, 0.9904, 1.0000, 0.9914, 0.9959 |
| safety_risk | 0.0550 | 0.0150 | 0.1800 | 0.2401 | 0.2401, 0.2401, 0.2401, 0.2401, 0.2401 |
| score | 0.0600 | 0.0100 | 0.2000 | 0.0925 | 0.0906, 0.0940, 0.0910, 0.0943, 0.0926 |
| selectivity | 0.2560 | 0.0800 | 0.4800 | 0.2151 | 0.2068, 0.2240, 0.2125, 0.2183, 0.2138 |
| yield | 0.2490 | 0.0800 | 0.4700 | 0.2135 | 0.2128, 0.2130, 0.2102, 0.2171, 0.2144 |
### Q03

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1890 | 0.0800 | 0.3800 | 0.1759 | 0.1879, 0.1765, 0.1652, 0.1758, 0.1740 |
| conversion | 0.8560 | 0.7000 | 0.9600 | 0.8625 | 0.8723, 0.8654, 0.8646, 0.8518, 0.8582 |
| safety_risk | 0.0250 | 0.0060 | 0.0800 | 0.2411 | 0.2411, 0.2411, 0.2411, 0.2411, 0.2411 |
| score | 0.5050 | 0.2500 | 0.6800 | 0.3993 | 0.3998, 0.4060, 0.3982, 0.3925, 0.3999 |
| selectivity | 0.7790 | 0.6200 | 0.8900 | 0.8038 | 0.8083, 0.8175, 0.8050, 0.7813, 0.8070 |
| yield | 0.6660 | 0.4600 | 0.8000 | 0.6927 | 0.6888, 0.7002, 0.6887, 0.6925, 0.6933 |
### Q04

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.8320 | 0.6100 | 0.9700 | 0.8234 | 0.8319, 0.8187, 0.8047, 0.8242, 0.8376 |
| conversion | 1.0000 | 0.9600 | 1.0000 | 0.9961 | 0.9979, 1.0000, 0.9969, 0.9949, 0.9909 |
| safety_risk | 0.0650 | 0.0200 | 0.2000 | 0.2407 | 0.2407, 0.2407, 0.2407, 0.2407, 0.2407 |
| score | 0.0260 | 0.0000 | 0.1400 | 0.0586 | 0.0586, 0.0599, 0.0615, 0.0530, 0.0597 |
| selectivity | 0.1680 | 0.0300 | 0.3800 | 0.2067 | 0.2135, 0.2148, 0.2117, 0.1955, 0.1978 |
| yield | 0.1680 | 0.0300 | 0.3800 | 0.2065 | 0.2020, 0.2039, 0.2104, 0.2000, 0.2162 |
### Q05

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1870 | 0.0700 | 0.3600 | 0.3427 | 0.3570, 0.3472, 0.3373, 0.3320, 0.3400 |
| conversion | 0.5360 | 0.3200 | 0.7300 | 0.6725 | 0.6707, 0.6733, 0.6807, 0.6692, 0.6687 |
| safety_risk | 0.0150 | 0.0030 | 0.0600 | 0.1409 | 0.1409, 0.1409, 0.1409, 0.1409, 0.1409 |
| score | 0.2240 | 0.0800 | 0.3700 | 0.2363 | 0.2352, 0.2416, 0.2340, 0.2391, 0.2316 |
| selectivity | 0.6510 | 0.4800 | 0.8000 | 0.5081 | 0.5123, 0.5200, 0.4998, 0.5115, 0.4971 |
| yield | 0.3490 | 0.1900 | 0.5000 | 0.3440 | 0.3391, 0.3498, 0.3415, 0.3498, 0.3401 |
### Q06

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.7930 | 0.5500 | 0.9600 | 0.6580 | 0.6596, 0.6455, 0.6477, 0.6646, 0.6724 |
| conversion | 0.9830 | 0.8800 | 1.0000 | 0.9970 | 0.9923, 0.9975, 0.9958, 0.9992, 1.0000 |
| safety_risk | 0.0850 | 0.0200 | 0.2800 | 0.4184 | 0.4184, 0.4184, 0.4184, 0.4184, 0.4184 |
| score | 0.0340 | 0.0000 | 0.1600 | 0.0968 | 0.1005, 0.0990, 0.0959, 0.0959, 0.0930 |
| selectivity | 0.1940 | 0.0400 | 0.4300 | 0.3386 | 0.3473, 0.3394, 0.3406, 0.3360, 0.3297 |
| yield | 0.1900 | 0.0400 | 0.4200 | 0.3324 | 0.3371, 0.3371, 0.3291, 0.3310, 0.3275 |
### Q07

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4010 | 0.2400 | 0.5900 | 0.3706 | 0.3709, 0.3574, 0.3671, 0.3773, 0.3805 |
| conversion | 0.9640 | 0.8400 | 1.0000 | 0.9536 | 0.9645, 0.9474, 0.9625, 0.9460, 0.9476 |
| safety_risk | 0.0300 | 0.0060 | 0.0900 | 0.1433 | 0.1433, 0.1433, 0.1433, 0.1433, 0.1433 |
| score | 0.3190 | 0.1600 | 0.4700 | 0.3618 | 0.3636, 0.3575, 0.3639, 0.3586, 0.3653 |
| selectivity | 0.5840 | 0.4200 | 0.7200 | 0.6202 | 0.6227, 0.6081, 0.6355, 0.6026, 0.6321 |
| yield | 0.5630 | 0.3900 | 0.7000 | 0.5921 | 0.5924, 0.5905, 0.5856, 0.5970, 0.5950 |
### Q08

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.8750 | 0.6600 | 0.9900 | 0.6833 | 0.6764, 0.6873, 0.6869, 0.6861, 0.6798 |
| conversion | 1.0000 | 0.9800 | 1.0000 | 0.9969 | 0.9976, 1.0000, 0.9869, 1.0000, 1.0000 |
| safety_risk | 0.1100 | 0.0250 | 0.3200 | 0.4189 | 0.4189, 0.4189, 0.4189, 0.4189, 0.4189 |
| score | 0.0140 | 0.0000 | 0.1000 | 0.0716 | 0.0729, 0.0695, 0.0697, 0.0774, 0.0686 |
| selectivity | 0.1250 | 0.0100 | 0.3400 | 0.3451 | 0.3412, 0.3405, 0.3438, 0.3497, 0.3501 |
| yield | 0.1250 | 0.0100 | 0.3400 | 0.3379 | 0.3433, 0.3348, 0.3364, 0.3487, 0.3264 |
### Q09

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5480 | 0.3800 | 0.7300 | 0.5497 | 0.5468, 0.5516, 0.5584, 0.5480, 0.5434 |
| conversion | 0.9910 | 0.9100 | 1.0000 | 0.9944 | 0.9970, 0.9902, 1.0000, 0.9955, 0.9895 |
| safety_risk | 0.0400 | 0.0100 | 0.1400 | 0.2411 | 0.2411, 0.2411, 0.2411, 0.2411, 0.2411 |
| score | 0.1900 | 0.0700 | 0.3300 | 0.2421 | 0.2357, 0.2430, 0.2458, 0.2442, 0.2419 |
| selectivity | 0.4470 | 0.2600 | 0.6100 | 0.4571 | 0.4478, 0.4587, 0.4688, 0.4497, 0.4606 |
| yield | 0.4420 | 0.2500 | 0.6000 | 0.4578 | 0.4468, 0.4601, 0.4582, 0.4673, 0.4563 |
### Q10

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5400 | 0.3400 | 0.7500 | 0.5455 | 0.5591, 0.5398, 0.5426, 0.5369, 0.5491 |
| conversion | 0.9910 | 0.9000 | 1.0000 | 0.9937 | 1.0000, 1.0000, 0.9875, 0.9862, 0.9946 |
| safety_risk | 0.0350 | 0.0050 | 0.1400 | 0.1447 | 0.1447, 0.1447, 0.1447, 0.1447, 0.1447 |
| score | 0.1950 | 0.0600 | 0.3500 | 0.2835 | 0.2828, 0.2939, 0.2808, 0.2830, 0.2771 |
| selectivity | 0.4550 | 0.2400 | 0.6500 | 0.4608 | 0.4589, 0.4903, 0.4415, 0.4667, 0.4468 |
| yield | 0.4500 | 0.2300 | 0.6300 | 0.4590 | 0.4568, 0.4649, 0.4658, 0.4559, 0.4516 |
### Q11

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.6180 | 0.4100 | 0.8200 | 0.5995 | 0.6234, 0.5938, 0.5959, 0.5966, 0.5880 |
| conversion | 0.9820 | 0.8400 | 1.0000 | 0.9882 | 0.9840, 0.9870, 0.9883, 0.9952, 0.9867 |
| safety_risk | 0.0250 | 0.0050 | 0.1000 | 0.1429 | 0.1429, 0.1429, 0.1429, 0.1429, 0.1429 |
| score | 0.1300 | 0.0300 | 0.2800 | 0.2369 | 0.2418, 0.2390, 0.2310, 0.2346, 0.2381 |
| selectivity | 0.3700 | 0.1800 | 0.5700 | 0.3913 | 0.3984, 0.4014, 0.3924, 0.3747, 0.3894 |
| yield | 0.3640 | 0.1700 | 0.5600 | 0.3919 | 0.4007, 0.3911, 0.3766, 0.3947, 0.3966 |
### Q12

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3880 | 0.2200 | 0.5700 | 0.2298 | 0.2339, 0.2223, 0.2346, 0.2244, 0.2338 |
| conversion | 0.9300 | 0.8000 | 0.9900 | 0.9087 | 0.9225, 0.9044, 0.9203, 0.8975, 0.8989 |
| safety_risk | 0.0450 | 0.0100 | 0.1800 | 0.4192 | 0.4192, 0.4192, 0.4192, 0.4192, 0.4192 |
| score | 0.3000 | 0.1300 | 0.4800 | 0.3203 | 0.3213, 0.3222, 0.3237, 0.3173, 0.3171 |
| selectivity | 0.5830 | 0.4200 | 0.7300 | 0.7430 | 0.7407, 0.7464, 0.7577, 0.7340, 0.7361 |
| yield | 0.5420 | 0.3500 | 0.7000 | 0.6852 | 0.6855, 0.6889, 0.6816, 0.6860, 0.6839 |

## Recommendation retest

- Selected source batch: `8`
- Retest exact replay verified: `True`
- Retest failure: `none`

| Metric | Selected source batch | Independent retest | Retest minus source |
|---|---:|---:|---:|
| byproduct_signal | 0.2463 | 0.2242 | -0.0221 |
| conversion | 0.7895 | 0.7972 | 0.0077 |
| cost | 1.0000 | 1.0000 | 0.0000 |
| degradation_warning | 0.1063 | 0.1068 | 0.0004 |
| safety_risk | 0.2037 | 0.2037 | 0.0000 |
| score | 0.2907 | 0.2867 | -0.0040 |
| selectivity | 0.7089 | 0.7081 | -0.0008 |
| virtual_spectrum_summary | 0.1833 | 0.1714 | -0.0119 |
| yield | 0.5655 | 0.5541 | -0.0114 |

## Scope note

This is the final sanitized report produced after all 60 source sessions and K1/Q/K2 chains were sealed. It includes released reference truth, blind-prediction evaluation, and the independent recommendation retest. Provider-private event streams, credentials, thread identifiers, and token accounting remain excluded.
