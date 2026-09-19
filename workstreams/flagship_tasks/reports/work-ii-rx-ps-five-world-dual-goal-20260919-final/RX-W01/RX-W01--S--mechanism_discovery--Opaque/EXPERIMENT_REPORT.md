# RX-W01--S--mechanism_discovery--Opaque

## Run summary

- World: `RX-W01`
- Locus: `S`
- Goal: `mechanism_discovery`
- Arm: `Opaque`
- Status: `completed`
- Source status: `completed`
- Experimental sessions: `12/12`
- Operations: `86`
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

- Selected batch: `9`
- Rationale: Batch 9 gave the strongest final target yield and campaign score while remaining below the safety-risk limit; it used Catalyst B in acetonitrile with a 370 K boundary target for 3600 s.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S0 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.1808 | 0.4194 | 0.4117 | 0.2396 | 0.0000 | 0.1036 | 0.0718 |
| 2 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.2737 | 0.6549 | 0.4208 | 0.1456 | 0.0284 | 0.1123 | 0.1647 |
| 3 | S0 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.1812 | 0.5116 | 0.3739 | 0.1904 | 0.0175 | 0.1030 | 0.0914 |
| 4 | S0 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.2453 | 0.6170 | 0.3974 | 0.1582 | 0.0387 | 0.1094 | 0.1429 |
| 5 | S1 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.3514 | 0.6516 | 0.5528 | 0.1948 | 0.0336 | 0.1457 | 0.1932 |
| 6 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.4498 | 0.7068 | 0.6482 | 0.1811 | 0.0772 | 0.1763 | 0.2421 |
| 7 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.4301 | 0.6572 | 0.6624 | 0.2279 | 0.0505 | 0.1862 | 0.2188 |
| 8 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 330 K x 3600 s @ 600 rpm | no | 0.3651 | 0.6987 | 0.5112 | 0.1466 | 0.0438 | 0.1598 | 0.1999 |
| 9 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 370 K x 3600 s @ 600 rpm | no | 0.5447 | 0.7218 | 0.7692 | 0.2280 | 0.1035 | 0.1969 | 0.2867 |
| 10 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 900 s @ 600 rpm | no | 0.1661 | 0.7876 | 0.2086 | 0.0450 | 0.0000 | 0.1386 | 0.1219 |
| 11 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3600 s @ 600 rpm → 350 K x 3600 s @ 600 rpm | no | 0.5343 | 0.5934 | 0.8800 | 0.3664 | 0.2089 | 0.1938 | 0.2629 |
| 12 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | yes | 0.4680 | 0.7038 | 0.6595 | 0.1774 | 0.0664 | 0.1697 | 0.2528 |

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
    "byproduct_signal": 0.23959116637706757,
    "conversion": 0.4117429256439209,
    "cost": 1.0,
    "degradation_warning": 0.0,
    "safety_risk": 0.103555828332901,
    "score": 0.07176263630390167,
    "selectivity": 0.41944822669029236,
    "virtual_spectrum_summary": 0.1317751407623291,
    "yield": 0.18081603944301605
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
    "byproduct_signal": 0.14556348323822021,
    "conversion": 0.42078667879104614,
    "cost": 1.0,
    "degradation_warning": 0.02838408388197422,
    "safety_risk": 0.11234387010335922,
    "score": 0.16470324993133545,
    "selectivity": 0.6548639535903931,
    "virtual_spectrum_summary": 0.09283275157213211,
    "yield": 0.2736583352088928
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
    "byproduct_signal": 0.19041822850704193,
    "conversion": 0.37391382455825806,
    "cost": 1.0,
    "degradation_warning": 0.017547398805618286,
    "safety_risk": 0.10303283482789993,
    "score": 0.09142643213272095,
    "selectivity": 0.5116189122200012,
    "virtual_spectrum_summary": 0.11262635886669159,
    "yield": 0.18123771250247955
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
    "byproduct_signal": 0.1582133024930954,
    "conversion": 0.39741748571395874,
    "cost": 1.0,
    "degradation_warning": 0.03874771296977997,
    "safety_risk": 0.10939750075340271,
    "score": 0.14288541674613953,
    "selectivity": 0.6170419454574585,
    "virtual_spectrum_summary": 0.10445377975702286,
    "yield": 0.24528014659881592
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
    "byproduct_signal": 0.19484496116638184,
    "conversion": 0.5528305768966675,
    "cost": 1.0,
    "degradation_warning": 0.03360360115766525,
    "safety_risk": 0.14565342664718628,
    "score": 0.19319602847099304,
    "selectivity": 0.6515816450119019,
    "virtual_spectrum_summary": 0.1222863495349884,
    "yield": 0.35140401124954224
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
    "byproduct_signal": 0.18110904097557068,
    "conversion": 0.6482201814651489,
    "cost": 1.0,
    "degradation_warning": 0.07715868949890137,
    "safety_risk": 0.1762675791978836,
    "score": 0.2421162724494934,
    "selectivity": 0.7068390846252441,
    "virtual_spectrum_summary": 0.13433139026165009,
    "yield": 0.4497622549533844
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
    "byproduct_signal": 0.22790879011154175,
    "conversion": 0.6624017357826233,
    "cost": 1.0,
    "degradation_warning": 0.050472840666770935,
    "safety_risk": 0.18623198568820953,
    "score": 0.21876250207424164,
    "selectivity": 0.6571508049964905,
    "virtual_spectrum_summary": 0.14806261658668518,
    "yield": 0.4300975501537323
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
    "byproduct_signal": 0.14656972885131836,
    "conversion": 0.5111568570137024,
    "cost": 1.0,
    "degradation_warning": 0.043759044259786606,
    "safety_risk": 0.15978805720806122,
    "score": 0.19993093609809875,
    "selectivity": 0.6986889839172363,
    "virtual_spectrum_summary": 0.10030492395162582,
    "yield": 0.3651190400123596
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
    "byproduct_signal": 0.22795481979846954,
    "conversion": 0.7692494988441467,
    "cost": 1.0,
    "degradation_warning": 0.10351553559303284,
    "safety_risk": 0.1968512386083603,
    "score": 0.286670446395874,
    "selectivity": 0.7217695116996765,
    "virtual_spectrum_summary": 0.17195715010166168,
    "yield": 0.5447154641151428
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
      "catalyst": 1,
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
    "byproduct_signal": 0.045048560947179794,
    "conversion": 0.20861968398094177,
    "cost": 1.0,
    "degradation_warning": 0.0,
    "safety_risk": 0.13855686783790588,
    "score": 0.12186148762702942,
    "selectivity": 0.7876178622245789,
    "virtual_spectrum_summary": 0.024776708334684372,
    "yield": 0.16611412167549133
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
  "end_step": 78,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.36639973521232605,
    "conversion": 0.8799864053726196,
    "cost": 1.0,
    "degradation_warning": 0.20886510610580444,
    "safety_risk": 0.19378018379211426,
    "score": 0.26287052035331726,
    "selectivity": 0.5933632254600525,
    "virtual_spectrum_summary": 0.2955091595649719,
    "yield": 0.534330427646637
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
  "end_step": 86,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.17736954987049103,
    "conversion": 0.659510612487793,
    "cost": 1.0,
    "degradation_warning": 0.0664229691028595,
    "safety_risk": 0.16965629160404205,
    "score": 0.25276222825050354,
    "selectivity": 0.7038437724113464,
    "virtual_spectrum_summary": 0.1274435818195343,
    "yield": 0.46798890829086304
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

1. Scope and evidence base

I completed 12 batches using a constant initial charge of 0.040 mol limiting reagent, 0.080 L solvent, and 0.005 mol catalyst. Unless otherwise stated, batches were stirred at 600 rpm. Every batch received one intermediate HPLC measurement and a post-termination final assay. The species are anonymous benchmark roles, so the terms reactant, target, byproduct, and degradation product below describe functional roles rather than real chemical identities.

The main controlled factors were catalyst identity, solvent identity, thermal boundary target, residence time, and quenching. Because most factors were changed one at a time around selected baselines, the evidence supports a phenomenological kinetic account but not a unique molecular mechanism.

2. Proposed reaction network

The smallest network consistent with the observations is parallel target/byproduct formation followed by slower deterioration of the desired material:

R -> P, rate kP(T, solvent, catalyst) * fR(R)
R -> B, rate kB(T, solvent, catalyst) * fR(R)
P -> D, rate kD(T, solvent, catalyst) * fP(P)

Additional conversion into B or D may also occur after substantial reactant depletion. Here R is the limiting reactant, P is the measured target, B represents competing products contributing to the byproduct signal, and D represents material contributing to the degradation warning or other unobserved losses.

A useful initial approximation is parallel pseudo-first-order consumption:

dR/dt = -(kP + kB)R
dP/dt = kP R - kD P
dB/dt = kB R + alpha*kD P

with temperature-dependent rate constants such as

ki(T) = Ai * exp[-Ei/(Rgas*T)].

For a non-isothermal operation, the appropriate independent variable is integrated thermal exposure, not merely the requested boundary temperature:

Omega_i = integral ki(Tactual(t)) dt.

Catalyst and solvent can be represented as multipliers on Ai and, importantly, on the branching ratio kP/(kP+kB). This distinction is required because the catalyst screen changed selectivity much more strongly than it changed total conversion.

The measured target yield is approximately, but not exactly, conversion times selectivity. For example, batch 9 gave conversion 0.76925 and selectivity 0.72177, whose product is about 0.555, close to the observed yield of 0.54472. Differences can arise from degradation, calibration definitions, process variation, and independent channel noise.

3. Evidence for approximately first-order reactant consumption

The most informative time series used Catalyst B in acetonitrile at a 350 K boundary target:

- Batch 10, 900 s: final conversion 0.20862, yield 0.16611, selectivity 0.78762, byproduct signal 0.04505, and degradation warning 0.
- Batch 6, 3600 s: final conversion 0.64822, yield 0.44976, selectivity 0.70684, byproduct signal 0.18111, and degradation warning 0.07716.
- Batch 11, 7200 s total: final conversion 0.87999, yield 0.53433, selectivity 0.59336, byproduct signal 0.36640, and degradation warning 0.20887.

Using kobs = -ln(1-conversion)/t gives approximately 2.60e-4 s^-1 at 900 s, 2.90e-4 s^-1 at 3600 s, and 2.94e-4 s^-1 at 7200 s. The lower short-time estimate is plausibly caused by heat-up time. The agreement at 3600 and 7200 s is strong evidence that total disappearance can be approximated by first-order kinetics over this tested range.

The target does not scale proportionally with conversion at long times. From 3600 to 7200 s, conversion increased by about 0.232, but yield increased by only about 0.085. Simultaneously, selectivity fell by about 0.113, the byproduct signal roughly doubled, and the degradation warning rose substantially. Thus continued heating increasingly favors competing conversion and/or degradation.

4. Temperature dependence and actual thermal history

With Catalyst B in acetonitrile for 3600 s:

- Batch 8, 330 K target: conversion 0.51116, yield 0.36512, selectivity 0.69869, byproduct 0.14657, degradation warning 0.04376, risk 0.15979.
- Batch 6, 350 K target: conversion 0.64822, yield 0.44976, selectivity 0.70684, byproduct 0.18111, degradation warning 0.07716, risk 0.17627.
- Batch 9, 370 K target: conversion 0.76925, yield 0.54472, selectivity 0.72177, byproduct 0.22795, degradation warning 0.10352, risk 0.19685.

The corresponding apparent first-order constants are approximately 1.98e-4, 2.90e-4, and 4.07e-4 s^-1. Treating the requested temperatures as rough effective temperatures gives an apparent activation energy near 18 kJ mol^-1. This value is descriptive rather than a uniquely identified elementary-step barrier because the vessels heated transiently and the full temperature trajectories were not observed.

The recorded temperature changes demonstrate why thermal history matters. In batch 6 the first 350 K heating interval raised the reported temperature by 49.84 K. In batch 11, the first 3600 s interval produced the same 49.84 K rise, while the second 3600 s interval raised it by only another 1.85 K. The second hour was therefore spent much closer to the hot operating state than the first hour. A model based only on nominal temperature multiplied by total time would miss this distinction.

Within the tested one-hour window, raising the boundary target from 330 to 370 K accelerated both desired and undesired chemistry, but the target pathway remained competitive: measured selectivity did not decline across these three batches. The deterioration became clearer when exposure was extended to two hours at 350 K.

5. Catalyst effects

Batches 1-4 used water, a 350 K target, and 3600 s, changing only catalyst identity:

- Batch 1, Catalyst A: conversion 0.41174, yield 0.18082, selectivity 0.41945, byproduct 0.23959, degradation warning 0.
- Batch 2, Catalyst B: conversion 0.42079, yield 0.27366, selectivity 0.65486, byproduct 0.14556, degradation warning 0.02838.
- Batch 3, Catalyst C: conversion 0.37391, yield 0.18124, selectivity 0.51162, byproduct 0.19042, degradation warning 0.01755.
- Batch 4, Catalyst D: conversion 0.39742, yield 0.24528, selectivity 0.61704, byproduct 0.15821, degradation warning 0.03875.

Total conversion varied relatively little compared with selectivity and yield. Catalyst B was best in this water screen, followed by Catalyst D. Catalyst A produced similar conversion to Catalyst B but much poorer selectivity and substantially more byproduct. I therefore interpret the main catalyst effect as control of branching between target and competing pathways, not simply acceleration of all reactant consumption.

The experiment does not identify whether this selectivity control arises from different active-site structures, different activation energies, or suppression of a secondary reaction. Because the catalysts are anonymous benchmark formulations, assigning a real chemical identity or detailed catalytic cycle would be unjustified.

6. Solvent effects and coupling with catalyst

Batches 2 and 5-7 used Catalyst B at 350 K for 3600 s:

- Batch 2, water: conversion 0.42079, yield 0.27366, selectivity 0.65486, byproduct 0.14556, risk 0.11234.
- Batch 5, ethanol: conversion 0.55283, yield 0.35140, selectivity 0.65158, byproduct 0.19484, risk 0.14565.
- Batch 6, acetonitrile: conversion 0.64822, yield 0.44976, selectivity 0.70684, byproduct 0.18111, risk 0.17627.
- Batch 7, toluene: conversion 0.66240, yield 0.43010, selectivity 0.65715, byproduct 0.22791, risk 0.18623.

The solvent affects both overall rate and pathway partitioning. Toluene gave slightly more conversion than acetonitrile, but acetonitrile gave higher selectivity, higher target yield, and less byproduct. Thus solvent cannot be modeled solely as a common rate multiplier. In the proposed equations it must influence kP and kB differently, and it may also affect kD.

Only Catalyst B was compared across all solvents, while all catalysts were compared only in water. Consequently, catalyst-solvent interaction terms remain unidentified. It is not established that Catalyst B would be the best catalyst in every solvent.

7. Competing conversion, degradation, and possible catalyst deactivation

The long-time evidence clearly shows deterioration of outcome quality, but it does not uniquely identify its microscopic cause. In batch 11, the second hour increased conversion from an intermediate HPLC value of 0.64982 to a final value of 0.87999, while final selectivity fell to 0.59336 and degradation warning rose to 0.20887. This is consistent with target degradation, increasing formation of byproduct as reactant becomes depleted, or both.

Gross catalyst deactivation is not required to explain the conversion data. The apparent first-order reactant-disappearance constant remained close to 2.9e-4 s^-1 between the one- and two-hour endpoints. However, selective deactivation remains a reasonable competing explanation: a target-selective catalytic state could decay into a less selective state while total reactant consumption continues. The present channels cannot distinguish that scenario from ordinary secondary degradation of P.

A more flexible alternative model would introduce an active catalyst fraction a(t):

da/dt = -kdeact(T)*a

dP/dt = a*kP*R - kD*P

dB/dt = [a*kB + (1-a)*kB,inactive]*R + alpha*kD*P.

The data do not justify estimating kdeact separately, so I retain the simpler parallel-plus-degradation network as the primary account and treat deactivation as unresolved.

8. Quench and termination

Batch 12 repeated the Catalyst B/acetonitrile/350 K/3600 s condition and then applied a quench before termination. Its pre-quench HPLC values were conversion 0.65523, yield 0.48368, selectivity 0.70725, and byproduct 0.17387. The quench lowered the reported temperature by 45 K over 55.11 s and reduced reported risk from 0.17627 to 0.16966. The final assay gave conversion 0.65951, yield 0.46799, selectivity 0.70384, byproduct 0.17737, and degradation warning 0.06642.

The closest unquenched comparison, batch 6, gave final yield 0.44976, degradation warning 0.07716, and risk 0.17627. This is directionally consistent with quenching arresting thermal deterioration and reducing safety risk. However, the apparent yield improvement is small, there was only one quenched batch, and the intermediate HPLC and final assay are different noisy measurement systems. The decrease from batch 12's pre-quench HPLC yield to its final-assay yield must not be interpreted as direct loss during quenching without accounting for cross-instrument uncertainty. The secure conclusion is that quenching rapidly reduced temperature and observed risk; protection of chemical yield is plausible but not conclusively quantified.

Termination without an explicit quench appears to freeze the batch for final assay in the benchmark lifecycle, but the experiments did not provide a continuous post-termination trajectory. I therefore do not infer real-world cooling kinetics from termination itself.

9. Practical predictive interpretation

Within the tested charge and stirring regime, I would predict outcomes using the following pseudocode:

initialize R=1, P=0, B=0, D=0
for each small interval dt:
    read or approximate Tactual(t)
    calculate kP, kB, kD from temperature, solvent, and catalyst factors
    dR = -(kP+kB)*R*dt
    dP = (kP*R-kD*P)*dt
    dB = (kB*R+alpha*kD*P)*dt
    update R, P, B
conversion = 1-R
selectivity approximately P/(P+B plus any other converted material)
yield approximately P, adjusted for assay calibration

For the observed design space, Catalyst B and acetonitrile provide the best demonstrated balance of target formation and competing conversion. Batch 9, with a 370 K target for 3600 s, was the strongest tested endpoint: yield 0.54472, selectivity 0.72177, conversion 0.76925, score 0.28667, and risk 0.19685, below the 0.35 safety limit. It was therefore selected as the final recommendation.

Batch 11 shows that simply extending residence time is not equivalent to raising temperature for one hour. Its yield of 0.53433 was close to batch 9, but its selectivity was much lower, and its byproduct and degradation channels were much larger. I infer that an optimal stopping region exists before prolonged hot exposure causes substantial deterioration. Its exact location was not resolved.

10. Safety coupling

Observed safety risk increased with faster/hotter conditions and with the solvent choice. In the Catalyst B solvent series at 350 K for one hour, risk rose from 0.11234 in water to 0.14565 in ethanol, 0.17627 in acetonitrile, and 0.18623 in toluene. For Catalyst B in acetonitrile, the one-hour risk rose from 0.15979 at the 330 K target to 0.17627 at 350 K and 0.19685 at 370 K. The quench reduced risk by about 0.0066 in batch 12. All completed batches remained below the specified limit of 0.35.

These associations do not reveal whether risk is driven by temperature, accumulated conversion, solvent-specific benchmark penalties, byproduct inventory, or a combination. A predictive safety model should therefore include separate solvent and thermal-exposure terms rather than identifying risk directly with yield or conversion.

11. Limits of identification and competing explanations

Several important factors remain unresolved:

- There were no catalyst-free controls and no catalyst-loading series, so catalytic rate order and uncatalyzed background reaction are unknown.
- Reagent amount, solvent volume, concentration, and stirring were held fixed. Reaction order beyond the pseudo-first-order approximation and possible mass-transfer effects are not identified.
- The full temperature-versus-time trajectory was not measured; only operation-level temperature changes were reported. The apparent activation energy is therefore an effective value.
- Catalyst and solvent effects were not studied in a full factorial design. Their interaction cannot be separated.
- Each final condition was measured once. Batch 12 provides only a near-replicate of batch 6, and it also differs by quenching.
- The byproduct signal and degradation warning are normalized analytical channels, not direct molar inventories. They should not be forced into an exact mass balance.
- Intermediate HPLC and final-assay estimates have different calibration and noise characteristics. Changes between those instruments are not pure kinetic changes.
- Target degradation, conversion to a second byproduct, changing selectivity with reactant depletion, and selective catalyst deactivation can all explain part of the long-time behavior.
- No molecular identities or spectra-to-structure mapping were public, so a named chemical mechanism would be speculation.

A competing purely empirical explanation would treat conversion, selectivity, and degradation warning as independent response surfaces of catalyst, solvent, temperature, and time. Such a model could interpolate the measured region without asserting a reaction network. I prefer the parallel-formation-plus-degradation account because it jointly explains the nearly first-order conversion, catalyst-dependent branching, increasing byproduct, and long-time loss of selectivity. Nevertheless, the empirical response-surface interpretation remains viable, and the present campaign cannot prove that P chemically converts into the measured degradation channel.

12. Overall conclusion

The world is best described, within the explored region, as a thermally accelerated reactant-consumption system with at least two competing formation channels. Catalyst identity primarily controls pathway selectivity, while solvent controls both overall rate and branching. Temperature increases conversion over one hour without destroying selectivity in the tested 330-370 K range, but prolonged hot exposure produces diminishing target-yield returns, increased byproduct, and a strong degradation warning. Conversion is well approximated by pseudo-first-order kinetics after accounting qualitatively for heat-up, whereas target yield requires a parallel-pathway and secondary-deterioration model. Quenching clearly lowers temperature and risk and may modestly preserve the target, but that chemical benefit remains uncertain from one comparison.

## Q — Blind predictions

### Overall rationale

Predictions use the previously reported parallel target/byproduct formation model with secondary target deterioration. Conversion was extrapolated from the approximately first-order time series and its observed temperature dependence; catalyst concentration was treated as an uncertain kinetic multiplier. Yield and selectivity were reduced at long thermal exposure to reflect the deterioration seen between batches 6 and 11, while byproduct signal was tied approximately to converted material not remaining as target. Quench protection was kept modest because batch 12 supplied only one noisy comparison. The intervals include final-assay noise and, more importantly, structural uncertainty from untested catalyst loading, smaller volume, higher concentration, lower stirring speed, temperatures above 370 K, and durations beyond 7200 s.

### Q01

The low catalyst concentration limits conversion during the short 410 K exposure. Extrapolation above the researched temperature range suggests faster conversion than the 350 K short-time batch, while substantial target degradation is not yet expected.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1020 | 0.0300 | 0.3000 |
| conversion | 0.3440 | 0.1800 | 0.5800 |
| safety_risk | 0.1200 | 0.0600 | 0.2200 |
| score | 0.1490 | 0.0500 | 0.2700 |
| selectivity | 0.7020 | 0.4800 | 0.8500 |
| yield | 0.2410 | 0.1000 | 0.4000 |

### Q02

Four hours at 410 K should approach complete conversion even with low catalyst loading, but the long hot residence is predicted to convert or divert most target material into competing and degradation channels. This is a strong extrapolation, so the yield and selectivity intervals are wide.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8740 | 0.5800 | 0.9800 |
| conversion | 0.9860 | 0.8000 | 1.0000 |
| safety_risk | 0.2200 | 0.1100 | 0.3800 |
| score | 0.0100 | 0.0000 | 0.1000 |
| selectivity | 0.1130 | 0.0200 | 0.4000 |
| yield | 0.1120 | 0.0200 | 0.3800 |

### Q03

High Catalyst B concentration combined with a short 410 K exposure is predicted to give rapid target formation before prolonged degradation dominates. The point estimate therefore has high conversion and retains selectivity near the favorable short-to-intermediate-time regime.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2300 | 0.0800 | 0.5000 |
| conversion | 0.8390 | 0.6000 | 0.9700 |
| safety_risk | 0.1400 | 0.0700 | 0.2500 |
| score | 0.3800 | 0.1800 | 0.5500 |
| selectivity | 0.7260 | 0.5200 | 0.8700 |
| yield | 0.6090 | 0.3500 | 0.7800 |

### Q04

The combination of high catalyst loading and four hours at 410 K should exhaust the reactant early, leaving a long period for target deterioration. Conversion is consequently near saturation, but the surviving target fraction is highly uncertain and predicted to be small.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9370 | 0.7000 | 0.9950 |
| conversion | 1.0000 | 0.9600 | 1.0000 |
| safety_risk | 0.2400 | 0.1300 | 0.4200 |
| score | 0.0030 | 0.0000 | 0.0600 |
| selectivity | 0.0630 | 0.0050 | 0.3000 |
| yield | 0.0630 | 0.0050 | 0.3000 |

### Q05

At 350 K, the low catalyst concentration is predicted to offset the long residence time, producing moderate conversion. The extended exposure lowers selectivity relative to a short run, but thermal degradation should be less severe than in the 410–465 K cases.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2030 | 0.0700 | 0.4200 |
| conversion | 0.5520 | 0.3200 | 0.7800 |
| safety_risk | 0.1000 | 0.0500 | 0.1800 |
| score | 0.1980 | 0.0800 | 0.3400 |
| selectivity | 0.6310 | 0.4500 | 0.7800 |
| yield | 0.3480 | 0.1800 | 0.5300 |

### Q06

Despite low catalyst loading, two hours at 465 K is expected to drive nearly complete conversion. Extrapolated thermal deterioration is severe, making byproduct formation dominant and creating large structural uncertainty in yield, selectivity, and risk.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8870 | 0.6200 | 0.9950 |
| conversion | 0.9850 | 0.8200 | 1.0000 |
| safety_risk | 0.3000 | 0.1600 | 0.5000 |
| score | 0.0070 | 0.0000 | 0.0800 |
| selectivity | 0.0990 | 0.0050 | 0.3600 |
| yield | 0.0980 | 0.0050 | 0.3500 |

### Q07

High Catalyst B loading at 350 K should give nearly complete conversion within two hours. The lower temperature moderates target deterioration, although the time dependence observed in batch 11 implies appreciable loss of selectivity and increased byproduct.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3690 | 0.2000 | 0.5800 |
| conversion | 0.9690 | 0.8400 | 1.0000 |
| safety_risk | 0.1300 | 0.0700 | 0.2300 |
| score | 0.3230 | 0.1700 | 0.4600 |
| selectivity | 0.6190 | 0.4300 | 0.7600 |
| yield | 0.6000 | 0.4000 | 0.7300 |

### Q08

This is the most severe combination of catalyst loading, temperature, and duration. Reactant conversion should saturate rapidly, but most initially formed target is predicted to be lost during the remaining hot exposure. The interval is deliberately wide because 465 K is far outside the researched range.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9500 | 0.7400 | 1.0000 |
| conversion | 1.0000 | 0.9800 | 1.0000 |
| safety_risk | 0.3300 | 0.1800 | 0.5500 |
| score | 0.0020 | 0.0000 | 0.0400 |
| selectivity | 0.0500 | 0.0000 | 0.2500 |
| yield | 0.0500 | 0.0000 | 0.2500 |

### Q09

The near-research catalyst concentration and two-hour 410 K exposure should yield almost complete conversion. Based on the long-time decline in batch 11 and extrapolated temperature acceleration, substantial target deterioration is expected before termination.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7120 | 0.4700 | 0.9000 |
| conversion | 0.9960 | 0.9000 | 1.0000 |
| safety_risk | 0.2100 | 0.1100 | 0.3700 |
| score | 0.0640 | 0.0100 | 0.1800 |
| selectivity | 0.2850 | 0.1000 | 0.5300 |
| yield | 0.2830 | 0.1000 | 0.5200 |

### Q10

The reaction state immediately before quenching should resemble Q09. Quenching is predicted to provide only modest chemical protection because it occurs after the full hot residence, but it should slightly reduce subsequent deterioration and safety risk. The Q09 and Q10 intervals intentionally overlap strongly.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6950 | 0.4500 | 0.8900 |
| conversion | 0.9940 | 0.8900 | 1.0000 |
| safety_risk | 0.1900 | 0.0900 | 0.3500 |
| score | 0.0730 | 0.0100 | 0.2000 |
| selectivity | 0.3020 | 0.1100 | 0.5500 |
| yield | 0.3000 | 0.1100 | 0.5400 |

### Q11

Four hours at 350 K should nearly exhaust the reactant at the intermediate catalyst concentration. The lower temperature preserves more target than the long 410–465 K cases, but the duration is twice the longest researched exposure and therefore implies substantial byproduct and degradation uncertainty.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5600 | 0.3400 | 0.7900 |
| conversion | 0.9850 | 0.8600 | 1.0000 |
| safety_risk | 0.1700 | 0.0900 | 0.3000 |
| score | 0.1520 | 0.0500 | 0.2900 |
| selectivity | 0.4310 | 0.2100 | 0.6400 |
| yield | 0.4250 | 0.2000 | 0.6200 |

### Q12

A short 465 K treatment is predicted to give rapid conversion while limiting the time available for secondary deterioration. Its uncertainty remains large because heat-up occupies an important fraction of 1800 s and no research batch approached this temperature.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3200 | 0.1200 | 0.5800 |
| conversion | 0.8410 | 0.6000 | 0.9800 |
| safety_risk | 0.2200 | 0.1100 | 0.3900 |
| score | 0.2510 | 0.1000 | 0.4100 |
| selectivity | 0.6190 | 0.4200 | 0.7900 |
| yield | 0.5210 | 0.2800 | 0.7200 |

## K2 — Retrospective analysis

1. Initial claims and their status

The initial material packet contained almost no substantive kinetic or mechanistic claims. It explicitly withheld a task-specific property dossier, described the catalysts as anonymous benchmark formulations, and warned that the named solvents had categorical benchmark effects rather than reliably inferable real-chemistry behavior. It therefore supplied no initial rate law, catalyst ranking, solvent ranking, degradation mechanism, or optimal operating region to test.

Two broad packet claims were consistent with the campaign. First, catalyst category mattered: in water at nominally 350 K for 3600 s, batches 1–4 had final conversions of 0.412, 0.421, 0.374, and 0.397, but selectivities of 0.419, 0.655, 0.512, and 0.617. This supported a catalyst-dependent latent profile, especially for branching. Second, solvent category mattered: with Catalyst B, batches 2 and 5–7 showed substantial solvent-dependent changes in conversion and selectivity. These observations support categorical coupling, but they do not validate a physical interpretation of the anonymous categories.

The packet’s warning against assigning real identities remained fully applicable. No observation supported a named reaction, molecular intermediate, or real catalytic cycle. This is an untested boundary condition rather than an experimentally verified chemical claim.

K1’s principal data-derived claim was that reactant disappearance was approximately pseudo-first-order over the studied Catalyst B/acetonitrile region. The apparent constants from batches 10, 6, and 11 were roughly 2.60e-4, 2.90e-4, and 2.94e-4 s^-1. That is meaningful support for an effective first-order approximation, not proof of an elementary first-order step.

A constant-selectivity parallel model was contradicted by the time series: selectivity declined from 0.788 in batch 10 at 900 s to 0.707 in batch 6 at 3600 s and 0.593 in batch 11 at 7200 s. K1 did respond to this evidence by adding target deterioration and discussing selective catalyst deactivation. Thus this was counterevidence that caused revision, not counterevidence that was silently ignored.

No clear experimental contradiction to the flexible R -> P, R -> B, P -> D account emerged. However, “no observed contradiction” is weaker than confirmation because that network can accommodate several trends. Catalyst-free background conversion, catalyst-loading dependence, reaction order, concentration effects, transport sensitivity, catalyst–solvent interactions, and the complete thermal trajectory all remained untested.

2. Experiments that formed or changed my judgments

Batch 1 was mainly a baseline. Batches 2–4 produced the first important mechanistic change: Catalyst B gave nearly the same conversion as Catalyst A but much higher selectivity and lower byproduct. That shifted my interpretation away from a single catalyst activity multiplier and toward catalyst-dependent pathway branching.

Batches 5–7 then changed the solvent interpretation. Toluene in batch 7 gave slightly higher conversion than acetonitrile in batch 6, 0.662 versus 0.648, but acetonitrile gave higher yield, 0.450 versus 0.430, higher selectivity, and less byproduct. This showed that solvent could not be ranked by total rate alone and motivated separate solvent effects on productive and competing channels.

Batches 8 and 9 established the observed temperature trend around the selected Catalyst B/acetonitrile condition. The increase from batch 8 at 330 K to batch 9 at 370 K raised final conversion from 0.511 to 0.769 and yield from 0.365 to 0.545. These results motivated K1’s Arrhenius-like interpolation and its approximate effective activation energy near 18 kJ mol^-1. K1 correctly qualified that estimate because nominal targets were being used in place of full temperature histories.

Batch 10 was essential to the time interpretation. Its 900 s endpoint had conversion 0.209, selectivity 0.788, byproduct 0.045, and no reported degradation warning. It established that high early selectivity preceded the poorer long-time outcome.

Batch 11 changed the account most strongly. Extending total heating to 7200 s raised conversion to 0.880 but yield only to 0.534, while selectivity fell to 0.593, byproduct rose to 0.366, and degradation warning rose to 0.209. This was the main basis for adding secondary deterioration or time-dependent selectivity. Its second heating interval also increased temperature by only 1.85 K after a 49.84 K increase in the first interval, proving that two equal-duration segments did not represent equal thermal histories.

Batch 12 shaped the quench interpretation. The quench lowered reported temperature by 45 K over about 55 s and reduced risk by approximately 0.0066. Its chemical protection was only suggestive because the closest unquenched comparator was a separate batch and the pre-quench and final observations came from different instruments.

Several design choices preceded evidence. The initial 350 K, 3600 s baseline, maximum catalyst charge, maximum reagent charge, and 600 rpm stirring rate were practical guesses. The initial catalyst screen was motivated by the categorical options in the packet. Later choices were adaptive: Catalyst B was selected after batches 1–4, and acetonitrile after batches 5–7. That adaptation improved the chance of finding a strong operation but narrowed the design before catalyst–solvent interactions had been studied.

3. Main competing mechanisms

The primary K1 account remains parallel formation followed by deterioration:

R -> P
R -> B
P -> D.

The most important alternatives are:

- Selective catalyst deactivation: a P-selective catalytic state may decay into a less selective state while total reactant consumption continues.
- Composition-dependent branching: selectivity may change as reactant is depleted or products accumulate, without P undergoing secondary degradation.
- Multiple primary byproduct pathways with distinct temperature dependencies.
- Thermal-history confounding: the poorer long-time endpoint may partly reflect the greater fraction of the later interval spent near the hot boundary state.
- A purely empirical response surface in which the observed channels need not correspond to a closed material-balance network.

The campaign can distinguish some coarse claims. The catalyst screen rejects a model in which catalyst identity only multiplies all reaction rates equally. The solvent screen similarly rejects a single common solvent multiplier. The time series establishes that productive selectivity worsens with prolonged exposure in the tested system.

The campaign cannot distinguish P -> D from selective catalyst deactivation or depletion-dependent branching. The degradation-warning channel does not identify its chemical precursor. The nearly constant apparent reactant-disappearance rate argues against severe deactivation of all activity, but it does not rule out loss of only the selective pathway. No catalyst-free control exists, so the uncatalyzed background rate is unknown. The design also cannot determine whether Catalyst B would remain best outside water because the catalyst and solvent screens were not factorial.

4. One additional complete experiment

If one legal complete experiment were allowed, I would run a catalyst-free kinetic control using 0.080 L acetonitrile and 0.040 mol reagent. I would heat toward 350 K at 600 rpm for 900 s, measure once by HPLC, continue heating for another 2700 s, terminate, and run the final assay. I would not actually execute it here.

This condition directly leverages batches 10 and 6, which used the same solvent and nominal temperature with Catalyst B at 900 and 3600 s.

- Very low conversion at both times would establish that Catalyst B is kinetically necessary and would support treating catalyst loading as a rate variable.
- Lower conversion but similar selectivity would indicate that Catalyst B mainly accelerates both productive and competing channels.
- Similar conversion but much lower selectivity would strengthen K1’s judgment that Catalyst B primarily controls branching.
- Similar conversion and selectivity would seriously weaken the catalytic interpretation and suggest that catalyst identity may act mainly as a categorical benchmark offset.
- Strong time-dependent deterioration without catalyst would show that thermal background chemistry can generate the batch-11 pattern, reducing the need to invoke catalyst deactivation.

This experiment would not uniquely distinguish target degradation from all other alternatives, but it would supply the most important missing kinetic anchor.

5. Identifiability versus operational score

Several batches sacrificed score for identification. Batches 3 and 4 tested catalysts that did not outperform Catalyst B. Batch 8 used a cooler condition, batch 10 deliberately stopped early at low conversion, and batch 11 extended heating into a regime likely to worsen selectivity. These experiments were retained because the research goal emphasized explanation rather than merely maximizing the public score.

There were also optimization-driven sacrifices of identifiability. After Catalyst B and acetonitrile appeared favorable, most later experiments used that pair. This led to batch 9, the best observed endpoint, but left catalyst–solvent interactions unresolved. Maximum catalyst loading was used throughout the research campaign; that favored conversion but made catalyst order and saturation unidentified. Concentration and stirring were held fixed, which simplified comparisons but prevented separation of intrinsic kinetics from concentration or transport effects.

The result was a sequential compromise rather than either a pure mechanism study or a pure optimizer. The catalyst and solvent screens emphasized discrimination, while the later thermal series concentrated resources around the empirically promising material pair. A more identification-focused campaign would have included catalyst-free and catalyst-loading controls. A more score-focused campaign would have spent more batches refining conditions near batch 9.

6. Underused evidence and weaknesses in the sealed predictions

The thermal-operation records were underused quantitatively. K1 acknowledged that batch 11’s first and second heating intervals had very different temperature increments, but the fitted effective kinetics still relied heavily on nominal boundary temperatures. No full T(t) trajectory was available, so the apparent activation energy conflated kinetics with heat-up.

The intermediate HPLC measurements were also difficult to exploit. Most batches supplied only one intermediate point, sampling was destructive, and final values came from a different instrument. I used their trends but did not fit separate HPLC and final-assay observation models. In batch 12, for example, the pre-quench HPLC yield and final-assay yield cannot be treated as a direct noiseless kinetic difference.

Safety evidence was not converted into a well-identified model. The campaign showed solvent, temperature, and exposure trends, but did not separate intrinsic solvent risk, material quantity, conversion, byproduct accumulation, and temperature. Consequently, safety predictions in Q were substantially more assumption-dependent than their numerical presentation may imply.

The least reliable blind predictions are the combined extrapolations:

- Q04 and Q08 combined high catalyst loading with very long or very hot exposure. Their conversion estimates were 1.000 with 80% lower bounds of 0.96 and 0.98. Those conversion intervals are probably too narrow because K1 contained no catalyst-loading series and no data above 370 K.
- Q02 predicted conversion 0.986 and yield only 0.112 after four hours at 410 K. Both near-complete conversion and severe target loss depend on extrapolating an unverified degradation equation.
- Q06 predicted conversion 0.985, yield 0.098, and risk 0.30 at 465 K for 7200 s. Q08 made an even more severe yield prediction of 0.050. The campaign did not establish degradation kinetics at anything close to 465 K, so these yield, selectivity, byproduct, and score intervals could be much too narrow.
- Q09 and Q10 predicted nearly complete conversion at 410 K for 7200 s, with modest quench protection in Q10. Batch 12 justified only a small directional quench effect, not a precise magnitude at 410 K.
- Q11 extended duration to 14400 s, twice the longest campaign exposure. Its predicted yield of 0.425 with interval 0.20–0.62 may still understate structural uncertainty about whether target loss continues, saturates, or follows another pathway.
- Q12 used 465 K for only 1800 s. Its prediction is highly sensitive to heat-up, which occupied a significant fraction of short campaign runs and was not modeled from a full trajectory.
- Q03 and Q07 predicted yields near 0.61 and 0.60 under high catalyst loading. These depend directly on an assumed catalyst-concentration multiplier that was never measured.

Every Q batch also changed scale from 0.080 L to 0.005 L, reagent concentration from 0.50 to 0.60 mol L^-1, and stirring from 600 to 400 rpm. K1 explicitly said that concentration, catalyst loading, and mixing were unidentified. Therefore, intervals driven mainly by final-assay noise would be inconsistent with K1’s scope. The sealed Q intervals attempted to include structural uncertainty, but the near-saturation conversion bounds and near-zero score bounds in the most extreme cases likely remained overconfident. This judgment is made without prediction truth and is not a post hoc explanation of observed errors.

7. Limitations of the sealed recommendation

Batch 9 was the sample-best completed batch, not a proven optimum. Its final conversion was 0.769, yield 0.545, selectivity 0.722, score 0.287, and risk 0.197. Those observations justified selecting it among the twelve completed batches, but only one batch was run at that exact condition.

Repeatability was not established. The first test should be several independent exact repetitions of batch 9 using the same measurement sequence. That would estimate process variance and show whether its advantage over batches 11 and 12 is reproducible.

Local robustness was also not established. A compact response-surface study should perturb temperature around 370 K, time around 3600 s, catalyst loading, concentration, and stirring, with replicated center points. A quench/no-quench comparison at the batch-9 condition would test whether its outcome can be preserved while reducing risk.

Material robustness is unknown because the other catalysts were tested only in water. Testing nearby operating conditions with at least one other catalyst in acetonitrile would reveal whether the recommendation depends on an unmeasured catalyst–solvent interaction.

Cross-world and real-material transfer are even less justified. The packet described latent benchmark couplings, so a new world would require recalibration from new observations. Anonymous catalyst categories cannot be assumed to preserve their ranking across worlds, and the benchmark solvent effects should not be interpreted as real synthetic guidance.

The defensible conclusion is limited: batch 9 was the highest-scoring observed member of this campaign and a sensible local starting point. The campaign did not prove that it is globally optimal, repeatable, locally robust, scale-invariant, transferable across material combinations, or transferable to another world.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 122.0 | none | 0 |
| Q | yes | 0 | 147.7 | none | 0 |
| K2 | yes | 0 | 82.4 | none | 0 |

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean 80% width | Mean interval score |
|---|---:|---:|---:|---:|
| byproduct_signal | 0.1161 | 0.9167 | 0.3775 | 0.4247 |
| conversion | 0.0345 | 1.0000 | 0.2133 | 0.2133 |
| safety_risk | 0.0670 | 0.8333 | 0.2425 | 0.2820 |
| score | 0.0838 | 0.6500 | 0.1942 | 0.3561 |
| selectivity | 0.1259 | 0.9167 | 0.3608 | 0.4401 |
| yield | 0.1243 | 0.9167 | 0.3642 | 0.4374 |

## Predictions versus released reference truth

### Q01

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1020 | 0.0300 | 0.3000 | 0.1660 | 0.1755, 0.1675, 0.1685, 0.1634, 0.1550 |
| conversion | 0.3440 | 0.1800 | 0.5800 | 0.4974 | 0.4904, 0.4986, 0.4894, 0.5090, 0.4995 |
| safety_risk | 0.1200 | 0.0600 | 0.2200 | 0.2382 | 0.2382, 0.2382, 0.2382, 0.2382, 0.2382 |
| score | 0.1490 | 0.0500 | 0.2700 | 0.2176 | 0.2177, 0.2151, 0.2192, 0.2149, 0.2213 |
| selectivity | 0.7020 | 0.4800 | 0.8500 | 0.6682 | 0.6668, 0.6747, 0.6838, 0.6463, 0.6693 |
| yield | 0.2410 | 0.1000 | 0.4000 | 0.3393 | 0.3421, 0.3286, 0.3353, 0.3432, 0.3471 |
### Q02

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.8740 | 0.5800 | 0.9800 | 0.7907 | 0.7883, 0.7816, 0.7919, 0.7950, 0.7966 |
| conversion | 0.9860 | 0.8000 | 1.0000 | 0.9955 | 1.0000, 0.9904, 1.0000, 0.9914, 0.9959 |
| safety_risk | 0.2200 | 0.1100 | 0.3800 | 0.2401 | 0.2401, 0.2401, 0.2401, 0.2401, 0.2401 |
| score | 0.0100 | 0.0000 | 0.1000 | 0.0925 | 0.0906, 0.0940, 0.0910, 0.0943, 0.0926 |
| selectivity | 0.1130 | 0.0200 | 0.4000 | 0.2151 | 0.2068, 0.2240, 0.2125, 0.2183, 0.2138 |
| yield | 0.1120 | 0.0200 | 0.3800 | 0.2135 | 0.2128, 0.2130, 0.2102, 0.2171, 0.2144 |
### Q03

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2300 | 0.0800 | 0.5000 | 0.1759 | 0.1879, 0.1765, 0.1652, 0.1758, 0.1740 |
| conversion | 0.8390 | 0.6000 | 0.9700 | 0.8625 | 0.8723, 0.8654, 0.8646, 0.8518, 0.8582 |
| safety_risk | 0.1400 | 0.0700 | 0.2500 | 0.2411 | 0.2411, 0.2411, 0.2411, 0.2411, 0.2411 |
| score | 0.3800 | 0.1800 | 0.5500 | 0.3993 | 0.3998, 0.4060, 0.3982, 0.3925, 0.3999 |
| selectivity | 0.7260 | 0.5200 | 0.8700 | 0.8038 | 0.8083, 0.8175, 0.8050, 0.7813, 0.8070 |
| yield | 0.6090 | 0.3500 | 0.7800 | 0.6927 | 0.6888, 0.7002, 0.6887, 0.6925, 0.6933 |
### Q04

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.9370 | 0.7000 | 0.9950 | 0.8234 | 0.8319, 0.8187, 0.8047, 0.8242, 0.8376 |
| conversion | 1.0000 | 0.9600 | 1.0000 | 0.9961 | 0.9979, 1.0000, 0.9969, 0.9949, 0.9909 |
| safety_risk | 0.2400 | 0.1300 | 0.4200 | 0.2407 | 0.2407, 0.2407, 0.2407, 0.2407, 0.2407 |
| score | 0.0030 | 0.0000 | 0.0600 | 0.0586 | 0.0586, 0.0599, 0.0615, 0.0530, 0.0597 |
| selectivity | 0.0630 | 0.0050 | 0.3000 | 0.2067 | 0.2135, 0.2148, 0.2117, 0.1955, 0.1978 |
| yield | 0.0630 | 0.0050 | 0.3000 | 0.2065 | 0.2020, 0.2039, 0.2104, 0.2000, 0.2162 |
### Q05

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2030 | 0.0700 | 0.4200 | 0.3427 | 0.3570, 0.3472, 0.3373, 0.3320, 0.3400 |
| conversion | 0.5520 | 0.3200 | 0.7800 | 0.6725 | 0.6707, 0.6733, 0.6807, 0.6692, 0.6687 |
| safety_risk | 0.1000 | 0.0500 | 0.1800 | 0.1409 | 0.1409, 0.1409, 0.1409, 0.1409, 0.1409 |
| score | 0.1980 | 0.0800 | 0.3400 | 0.2363 | 0.2352, 0.2416, 0.2340, 0.2391, 0.2316 |
| selectivity | 0.6310 | 0.4500 | 0.7800 | 0.5081 | 0.5123, 0.5200, 0.4998, 0.5115, 0.4971 |
| yield | 0.3480 | 0.1800 | 0.5300 | 0.3440 | 0.3391, 0.3498, 0.3415, 0.3498, 0.3401 |
### Q06

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.8870 | 0.6200 | 0.9950 | 0.6580 | 0.6596, 0.6455, 0.6477, 0.6646, 0.6724 |
| conversion | 0.9850 | 0.8200 | 1.0000 | 0.9970 | 0.9923, 0.9975, 0.9958, 0.9992, 1.0000 |
| safety_risk | 0.3000 | 0.1600 | 0.5000 | 0.4184 | 0.4184, 0.4184, 0.4184, 0.4184, 0.4184 |
| score | 0.0070 | 0.0000 | 0.0800 | 0.0968 | 0.1005, 0.0990, 0.0959, 0.0959, 0.0930 |
| selectivity | 0.0990 | 0.0050 | 0.3600 | 0.3386 | 0.3473, 0.3394, 0.3406, 0.3360, 0.3297 |
| yield | 0.0980 | 0.0050 | 0.3500 | 0.3324 | 0.3371, 0.3371, 0.3291, 0.3310, 0.3275 |
### Q07

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3690 | 0.2000 | 0.5800 | 0.3706 | 0.3709, 0.3574, 0.3671, 0.3773, 0.3805 |
| conversion | 0.9690 | 0.8400 | 1.0000 | 0.9536 | 0.9645, 0.9474, 0.9625, 0.9460, 0.9476 |
| safety_risk | 0.1300 | 0.0700 | 0.2300 | 0.1433 | 0.1433, 0.1433, 0.1433, 0.1433, 0.1433 |
| score | 0.3230 | 0.1700 | 0.4600 | 0.3618 | 0.3636, 0.3575, 0.3639, 0.3586, 0.3653 |
| selectivity | 0.6190 | 0.4300 | 0.7600 | 0.6202 | 0.6227, 0.6081, 0.6355, 0.6026, 0.6321 |
| yield | 0.6000 | 0.4000 | 0.7300 | 0.5921 | 0.5924, 0.5905, 0.5856, 0.5970, 0.5950 |
### Q08

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.9500 | 0.7400 | 1.0000 | 0.6833 | 0.6764, 0.6873, 0.6869, 0.6861, 0.6798 |
| conversion | 1.0000 | 0.9800 | 1.0000 | 0.9969 | 0.9976, 1.0000, 0.9869, 1.0000, 1.0000 |
| safety_risk | 0.3300 | 0.1800 | 0.5500 | 0.4189 | 0.4189, 0.4189, 0.4189, 0.4189, 0.4189 |
| score | 0.0020 | 0.0000 | 0.0400 | 0.0716 | 0.0729, 0.0695, 0.0697, 0.0774, 0.0686 |
| selectivity | 0.0500 | 0.0000 | 0.2500 | 0.3451 | 0.3412, 0.3405, 0.3438, 0.3497, 0.3501 |
| yield | 0.0500 | 0.0000 | 0.2500 | 0.3379 | 0.3433, 0.3348, 0.3364, 0.3487, 0.3264 |
### Q09

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.7120 | 0.4700 | 0.9000 | 0.5497 | 0.5468, 0.5516, 0.5584, 0.5480, 0.5434 |
| conversion | 0.9960 | 0.9000 | 1.0000 | 0.9944 | 0.9970, 0.9902, 1.0000, 0.9955, 0.9895 |
| safety_risk | 0.2100 | 0.1100 | 0.3700 | 0.2411 | 0.2411, 0.2411, 0.2411, 0.2411, 0.2411 |
| score | 0.0640 | 0.0100 | 0.1800 | 0.2421 | 0.2357, 0.2430, 0.2458, 0.2442, 0.2419 |
| selectivity | 0.2850 | 0.1000 | 0.5300 | 0.4571 | 0.4478, 0.4587, 0.4688, 0.4497, 0.4606 |
| yield | 0.2830 | 0.1000 | 0.5200 | 0.4578 | 0.4468, 0.4601, 0.4582, 0.4673, 0.4563 |
### Q10

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.6950 | 0.4500 | 0.8900 | 0.5455 | 0.5591, 0.5398, 0.5426, 0.5369, 0.5491 |
| conversion | 0.9940 | 0.8900 | 1.0000 | 0.9937 | 1.0000, 1.0000, 0.9875, 0.9862, 0.9946 |
| safety_risk | 0.1900 | 0.0900 | 0.3500 | 0.1447 | 0.1447, 0.1447, 0.1447, 0.1447, 0.1447 |
| score | 0.0730 | 0.0100 | 0.2000 | 0.2835 | 0.2828, 0.2939, 0.2808, 0.2830, 0.2771 |
| selectivity | 0.3020 | 0.1100 | 0.5500 | 0.4608 | 0.4589, 0.4903, 0.4415, 0.4667, 0.4468 |
| yield | 0.3000 | 0.1100 | 0.5400 | 0.4590 | 0.4568, 0.4649, 0.4658, 0.4559, 0.4516 |
### Q11

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5600 | 0.3400 | 0.7900 | 0.5995 | 0.6234, 0.5938, 0.5959, 0.5966, 0.5880 |
| conversion | 0.9850 | 0.8600 | 1.0000 | 0.9882 | 0.9840, 0.9870, 0.9883, 0.9952, 0.9867 |
| safety_risk | 0.1700 | 0.0900 | 0.3000 | 0.1429 | 0.1429, 0.1429, 0.1429, 0.1429, 0.1429 |
| score | 0.1520 | 0.0500 | 0.2900 | 0.2369 | 0.2418, 0.2390, 0.2310, 0.2346, 0.2381 |
| selectivity | 0.4310 | 0.2100 | 0.6400 | 0.3913 | 0.3984, 0.4014, 0.3924, 0.3747, 0.3894 |
| yield | 0.4250 | 0.2000 | 0.6200 | 0.3919 | 0.4007, 0.3911, 0.3766, 0.3947, 0.3966 |
### Q12

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3200 | 0.1200 | 0.5800 | 0.2298 | 0.2339, 0.2223, 0.2346, 0.2244, 0.2338 |
| conversion | 0.8410 | 0.6000 | 0.9800 | 0.9087 | 0.9225, 0.9044, 0.9203, 0.8975, 0.8989 |
| safety_risk | 0.2200 | 0.1100 | 0.3900 | 0.4192 | 0.4192, 0.4192, 0.4192, 0.4192, 0.4192 |
| score | 0.2510 | 0.1000 | 0.4100 | 0.3203 | 0.3213, 0.3222, 0.3237, 0.3173, 0.3171 |
| selectivity | 0.6190 | 0.4200 | 0.7900 | 0.7430 | 0.7407, 0.7464, 0.7577, 0.7340, 0.7361 |
| yield | 0.5210 | 0.2800 | 0.7200 | 0.6852 | 0.6855, 0.6889, 0.6816, 0.6860, 0.6839 |

## Recommendation retest

- Selected source batch: `9`
- Retest exact replay verified: `True`
- Retest failure: `none`

| Metric | Selected source batch | Independent retest | Retest minus source |
|---|---:|---:|---:|
| byproduct_signal | 0.2280 | 0.2316 | 0.0037 |
| conversion | 0.7692 | 0.7671 | -0.0022 |
| cost | 1.0000 | 1.0000 | 0.0000 |
| degradation_warning | 0.1035 | 0.1072 | 0.0037 |
| safety_risk | 0.1969 | 0.1969 | 0.0000 |
| score | 0.2867 | 0.2874 | 0.0008 |
| selectivity | 0.7218 | 0.7219 | 0.0001 |
| virtual_spectrum_summary | 0.1720 | 0.1756 | 0.0037 |
| yield | 0.5447 | 0.5471 | 0.0024 |

## Scope note

This is the final sanitized report produced after all 60 source sessions and K1/Q/K2 chains were sealed. It includes released reference truth, blind-prediction evaluation, and the independent recommendation retest. Provider-private event streams, credentials, thread identifiers, and token accounting remain excluded.
