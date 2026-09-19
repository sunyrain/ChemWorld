# RX-W04--S--mechanism_discovery--MisIndexed

## Run summary

- World: `RX-W04`
- Locus: `S`
- Goal: `mechanism_discovery`
- Arm: `MisIndexed`
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

- Selected batch: `9`
- Rationale: Batch 9 gave the strongest safe operating result observed: high conversion and yield at the 380 K boundary-control condition with Catalyst B in toluene, while measured safety risk remained below the 0.35 limit; the hotter and longer runs increased degradation/byproduct burden.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S2 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.3690 | 0.5668 | 0.6666 | 0.2863 | 0.0935 | 0.1715 | 0.1788 |
| 2 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.5786 | 0.7253 | 0.8137 | 0.2402 | 0.1053 | 0.1923 | 0.3076 |
| 3 | S2 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.3824 | 0.5603 | 0.6664 | 0.3101 | 0.0361 | 0.1699 | 0.1832 |
| 4 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.4527 | 0.6542 | 0.6859 | 0.2206 | 0.0718 | 0.1771 | 0.2335 |
| 5 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.4312 | 0.7845 | 0.5405 | 0.1219 | 0.0435 | 0.1273 | 0.2654 |
| 6 | S1 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.3806 | 0.6446 | 0.6125 | 0.2295 | 0.0579 | 0.1513 | 0.2066 |
| 7 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.6226 | 0.7547 | 0.8368 | 0.2143 | 0.0945 | 0.2064 | 0.3285 |
| 8 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 320 K x 3600 s @ 600 rpm | no | 0.4462 | 0.7554 | 0.5965 | 0.1499 | 0.0375 | 0.1802 | 0.2459 |
| 9 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 380 K x 3600 s @ 600 rpm | no | 0.6915 | 0.7186 | 0.9482 | 0.2681 | 0.1363 | 0.2441 | 0.3412 |
| 10 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 410 K x 3600 s @ 600 rpm | no | 0.6857 | 0.6843 | 0.9959 | 0.3170 | 0.1866 | 0.3539 | 0.2857 |
| 11 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 380 K x 1200 s @ 600 rpm | yes | 0.4561 | 0.8250 | 0.5694 | 0.0963 | 0.0160 | 0.1803 | 0.2645 |
| 12 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 380 K x 7200 s @ 600 rpm | no | 0.5625 | 0.5675 | 1.0000 | 0.4598 | 0.3189 | 0.2437 | 0.2572 |

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
    "byproduct_signal": 0.2862565517425537,
    "conversion": 0.6666099429130554,
    "cost": 1.0,
    "degradation_warning": 0.09348317980766296,
    "safety_risk": 0.1714741587638855,
    "score": 0.17881320416927338,
    "selectivity": 0.5667968988418579,
    "virtual_spectrum_summary": 0.19950853288173676,
    "yield": 0.3690408766269684
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
    "byproduct_signal": 0.24021592736244202,
    "conversion": 0.8137246966362,
    "cost": 1.0,
    "degradation_warning": 0.10531789809465408,
    "safety_risk": 0.1923234462738037,
    "score": 0.3075859546661377,
    "selectivity": 0.7252835631370544,
    "virtual_spectrum_summary": 0.17951181530952454,
    "yield": 0.5785953402519226
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
    "byproduct_signal": 0.31009921431541443,
    "conversion": 0.6663975715637207,
    "cost": 1.0,
    "degradation_warning": 0.03614324331283569,
    "safety_risk": 0.1698695868253708,
    "score": 0.18323589861392975,
    "selectivity": 0.5603269338607788,
    "virtual_spectrum_summary": 0.18681901693344116,
    "yield": 0.38238927721977234
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
    "byproduct_signal": 0.22059312462806702,
    "conversion": 0.6858632564544678,
    "cost": 1.0,
    "degradation_warning": 0.07180564850568771,
    "safety_risk": 0.17711316049098969,
    "score": 0.23348453640937805,
    "selectivity": 0.65415358543396,
    "virtual_spectrum_summary": 0.15363876521587372,
    "yield": 0.45265182852745056
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
    "byproduct_signal": 0.12193919718265533,
    "conversion": 0.5404548048973083,
    "cost": 1.0,
    "degradation_warning": 0.04345834627747536,
    "safety_risk": 0.12729288637638092,
    "score": 0.2653874456882477,
    "selectivity": 0.7844969034194946,
    "virtual_spectrum_summary": 0.08662281185388565,
    "yield": 0.43124884366989136
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
    "byproduct_signal": 0.22945542633533478,
    "conversion": 0.6124523282051086,
    "cost": 1.0,
    "degradation_warning": 0.05787482485175133,
    "safety_risk": 0.15130333602428436,
    "score": 0.2065548598766327,
    "selectivity": 0.6445600986480713,
    "virtual_spectrum_summary": 0.15224415063858032,
    "yield": 0.38064026832580566
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
    "byproduct_signal": 0.21428821980953217,
    "conversion": 0.8367507457733154,
    "cost": 1.0,
    "degradation_warning": 0.09449998289346695,
    "safety_risk": 0.20643991231918335,
    "score": 0.3284851312637329,
    "selectivity": 0.7547271847724915,
    "virtual_spectrum_summary": 0.16038352251052856,
    "yield": 0.6225655674934387
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
  "end_step": 56,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.14994727075099945,
    "conversion": 0.5964669585227966,
    "cost": 1.0,
    "degradation_warning": 0.03745806962251663,
    "safety_risk": 0.18022137880325317,
    "score": 0.24587929248809814,
    "selectivity": 0.7553626894950867,
    "virtual_spectrum_summary": 0.09932712465524673,
    "yield": 0.44622883200645447
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
  "end_step": 63,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.2680585980415344,
    "conversion": 0.9481740593910217,
    "cost": 1.0,
    "degradation_warning": 0.13631369173526764,
    "safety_risk": 0.24412548542022705,
    "score": 0.3411795198917389,
    "selectivity": 0.718553364276886,
    "virtual_spectrum_summary": 0.2087733894586563,
    "yield": 0.6914505958557129
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
      "target_temperature_K": 410
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
    "byproduct_signal": 0.3170151114463806,
    "conversion": 0.9958776831626892,
    "cost": 1.0,
    "degradation_warning": 0.18663860857486725,
    "safety_risk": 0.35388612747192383,
    "score": 0.28569796681404114,
    "selectivity": 0.6842916011810303,
    "virtual_spectrum_summary": 0.25834569334983826,
    "yield": 0.6857151389122009
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
      "duration_s": 1200,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 380
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
  "end_step": 78,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.09626420587301254,
    "conversion": 0.5694180130958557,
    "cost": 1.0,
    "degradation_warning": 0.016046352684497833,
    "safety_risk": 0.18031615018844604,
    "score": 0.26450440287590027,
    "selectivity": 0.8250453472137451,
    "virtual_spectrum_summary": 0.06016617268323898,
    "yield": 0.45610886812210083
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
      "duration_s": 7200,
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
  "end_step": 85,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.4598161578178406,
    "conversion": 1.0,
    "cost": 1.0,
    "degradation_warning": 0.3189176023006439,
    "safety_risk": 0.24371913075447083,
    "score": 0.2572057247161865,
    "selectivity": 0.5674628019332886,
    "virtual_spectrum_summary": 0.39641180634498596,
    "yield": 0.5625340342521667
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

## Mechanistic report

### 1. Scope and evidential basis

This report describes the bounded synthetic reaction world explored in twelve completed batches. The limiting reagent, target, impurities, degradation products, and catalysts are anonymous benchmark entities. The solvent names are real material labels, but their kinetic effects here are categorical benchmark effects; therefore, I do not infer a real named reaction or catalyst identity.

Every batch used 0.040 mol reagent, 0.080 L solvent, 0.005 mol catalyst, and 600 rpm stirring. Unless noted otherwise, the programmed heating duration was 3600 s. Each batch received an endpoint HPLC measurement, termination, and a final assay. Values below are final-assay processed estimates unless explicitly identified as HPLC observations.

### 2. Main empirical findings

#### Catalyst dependence in acetonitrile at a 350 K target

The four catalysts gave materially different outcomes:

- Batch 1, Catalyst A: conversion 0.667, yield 0.369, selectivity 0.567, byproduct signal 0.286, degradation warning 0.093, safety risk 0.171.
- Batch 2, Catalyst B: conversion 0.814, yield 0.579, selectivity 0.725, byproduct 0.240, degradation 0.105, risk 0.192.
- Batch 3, Catalyst C: conversion 0.666, yield 0.382, selectivity 0.560, byproduct 0.310, degradation 0.036, risk 0.170.
- Batch 4, Catalyst D: conversion 0.686, yield 0.453, selectivity 0.654, byproduct 0.221, degradation 0.072, risk 0.177.

Catalyst B was the most effective of the four under this condition, improving both conversion and target selectivity. The catalyst effect is consequently not just a uniform acceleration of every reaction channel. A purely common rate multiplier would change conversion but leave selectivity approximately unchanged; the observed selectivity spread from about 0.56 to 0.73 instead implies catalyst-dependent relative rates for target and competing pathways.

The ordering supported by these data is approximately B > D > A ≈ C for target formation, although A and C cannot be cleanly ordered because their conversion and yield are close and the final-assay values contain measurement noise.

#### Solvent dependence with Catalyst B at a 350 K target

- Batch 5, water: conversion 0.540, yield 0.431, selectivity 0.784, byproduct 0.122, degradation 0.043, risk 0.127.
- Batch 6, ethanol: conversion 0.612, yield 0.381, selectivity 0.645, byproduct 0.229, degradation 0.058, risk 0.151.
- Batch 2, acetonitrile: conversion 0.814, yield 0.579, selectivity 0.725, byproduct 0.240, degradation 0.105, risk 0.192.
- Batch 7, toluene: conversion 0.837, yield 0.623, selectivity 0.755, byproduct 0.214, degradation 0.094, risk 0.206.

The solvent therefore affects at least three coupled properties: productive rate, selectivity, and safety burden. Water was slow but relatively selective and clean. Toluene gave the largest target yield and conversion at this temperature but also the largest safety risk of the four. Ethanol was inferior to water in final target yield despite somewhat greater conversion, indicating a larger fraction of converted material entering non-target channels. Acetonitrile was productive, but less productive than toluene under the tested condition.

These are categorical empirical effects. They should not be interpreted as established consequences of real-world solvent polarity, boiling point, or other physical properties because the benchmark explicitly does not provide that mechanistic mapping.

#### Temperature dependence with Catalyst B in toluene

At 3600 s:

- Batch 8, 320 K target: conversion 0.596, yield 0.446, selectivity 0.755, byproduct 0.150, degradation 0.037, risk 0.180.
- Batch 7, 350 K target: conversion 0.837, yield 0.623, selectivity 0.755, byproduct 0.214, degradation 0.094, risk 0.206.
- Batch 9, 380 K target: conversion 0.948, yield 0.691, selectivity 0.719, byproduct 0.268, degradation 0.136, risk 0.244.
- Batch 10, 410 K target: conversion 0.996, yield 0.686, selectivity 0.684, byproduct 0.317, degradation 0.187, risk 0.354.

Increasing temperature strongly increased conversion, but its benefit to target yield saturated between 380 and 410 K. The slight yield change from 0.691 to 0.686 is much smaller than the changes in conversion, selectivity, byproduct, degradation, and risk. Thus, above approximately the 380 K tested condition, extra thermal severity primarily accelerates undesirable chemistry and raises safety burden rather than increasing isolated target formation.

Batch 10 marginally exceeded the stated safety limit of 0.35, with observed risk 0.3539. It is empirical evidence about the system but is not a safe recommended operating point.

The recorded temperature rises during the one-hour heat operations were approximately +20.57 K in Batch 8, +49.17 K in Batch 7, +76.58 K in Batch 9, and +102.91 K in Batch 10. These are observed changes, not direct proof that the liquid remained exactly at the programmed set point for the full hour. They show that actual thermal history follows the requested temperature in a finite-response manner. I did not obtain a continuous temperature trace, so warm-up lag and any reaction-generated heat cannot be separately estimated.

#### Time dependence at a 380 K target with Catalyst B in toluene

- Batch 11, 1200 s followed by quench: final conversion 0.569, yield 0.456, selectivity 0.825, byproduct 0.096, degradation 0.016. The pre-quench HPLC estimates were conversion 0.556, yield 0.474, selectivity 0.843, and byproduct 0.096.
- Batch 9, 3600 s without quench: conversion 0.948, yield 0.691, selectivity 0.719, byproduct 0.268, degradation 0.136.
- Batch 12, 7200 s without quench: conversion 1.000, yield 0.563, selectivity 0.567, byproduct 0.460, degradation 0.319.

The target first accumulates and then declines under prolonged heating. Between 1200 and 3600 s, target yield rose substantially as reagent conversion advanced. Between 3600 and 7200 s, conversion approached unity but target yield fell from 0.691 to 0.563, while byproduct and degradation signals rose sharply. This is the clearest evidence that the target is not a stable terminal sink under severe conditions.

The approximate relation

`target yield ≈ conversion × selectivity`

is supported across the campaign. For example, Batch 9 gives 0.948 × 0.719 = 0.681, close to the measured yield of 0.691; Batch 12 gives 1.000 × 0.567 = 0.567, close to 0.563. Small discrepancies are consistent with independent channel noise and the benchmark's processed definitions.

### 3. Proposed process and equations

A minimal explanatory network is:

`R ⇌ P`

`R → B`

`P → D`

where R is the limiting reagent, P is the desired target, B represents primary competing products, and D represents secondary degradation products. A direct `R → D` route may also exist but was not separately identifiable.

One useful kinetic representation is:

`dR/dt = -a(t)[kP R + kB R] + k−P P`

`dP/dt = a(t) kP R - k−P P - kD P`

`dB/dt = a(t) kB R`

`dD/dt = kD P`

Here, each rate coefficient depends on catalyst, solvent, and temperature. A conventional local parameterization would be

`kj(cat,sol,T) = Aj(cat,sol) exp[-Ej/(RT)]`

for `j ∈ {P, −P, B, D}`. The observations require the categorical catalyst and solvent multipliers to differ by pathway; a single common multiplier is inadequate.

The supplied structural prior stated that the target pathway may possess an appreciable reverse channel. The campaign does not disprove that prior, and the reversible term is retained in the model. However, the observed loss of target during extended heating can also be explained by irreversible target degradation. Because Batch 12 simultaneously showed large degradation and byproduct signals, these data more directly support `P → D` than they support reversal. A reverse rate constant cannot be uniquely estimated without a product-spiking, relaxation, or matched composition experiment.

Catalyst activity could be represented as

`da/dt = -kd(cat,sol,T) a`, with `a(0)=1`.

Catalyst deactivation is plausible at high temperature or long duration, but it was not identified independently. The slowing of productive accumulation could instead arise from reagent depletion, approach to reversible equilibrium, or increasing competition and target destruction. I therefore treat `a(t)` as an optional latent term rather than an established fact.

A minimal thermal model is

`Ceff dT/dt = UA(Tset - T) + Qrxn(t)`

or, if reaction heat is negligible,

`dT/dt = (Tset - T)/τT`.

The observed temperature changes are compatible with finite thermal relaxation toward the set point, but the measurements are insufficient to determine `τT`, `UA`, or `Qrxn` separately. Reaction rates should formally be integrated over actual `T(t)`, not calculated as though the set point were reached instantaneously.

### 4. Coupling between conversion, selectivity, degradation, and safety

The system exhibits a severity tradeoff rather than a single monotonic optimum:

1. Higher temperature or longer time increases conversion.
2. Increasing severity also increases primary byproduct formation and the degradation of accumulated target.
3. Target yield therefore has an interior maximum in time and a shallow maximum in temperature within the explored region.
4. Safety risk rises with solvent choice and thermal severity. The best chemical conversion is not automatically the safest or highest-scoring condition.

A useful qualitative controller would be:

```
while target is still accumulating rapidly and risk is acceptable:
    continue controlled heating
if marginal conversion gain is small or degradation rises rapidly:
    terminate and cool/quench
```

The experiment most consistent with that rule was Batch 9: Catalyst B in toluene, a 380 K target, and 3600 s heating. It gave the campaign's highest observed safe score, with conversion 0.948, yield 0.691, and risk 0.244. Batch 10 demonstrated why further temperature escalation is unattractive, and Batch 12 demonstrated why prolonged residence is unattractive.

### 5. Interpretation of quench and termination

In Batch 11, quenching reduced temperature by 45 K over approximately 57.87 s and reduced displayed safety risk from 0.2102 after heating to 0.1803, a change of about -0.0298. This directly supports a physical cooling/risk-mitigation role.

The pre-quench HPLC and post-termination final assay were broadly similar, but they are different instruments with independent noise: yield changed from 0.474 to 0.456, conversion from 0.556 to 0.569, and selectivity from 0.843 to 0.825. Those differences are not sufficient to claim that quenching chemically destroyed target or created extra conversion. The most defensible interpretation is that quench rapidly lowers thermal exposure and approximately freezes the reacting state.

There was no matched unquenched 1200 s batch, so the chemical benefit of quenching relative to immediate termination is not separately identified. Likewise, termination appeared to preserve the last visible composition, but the experiment did not directly compare different delays between termination and assay.

### 6. How the explanation changed during the campaign

The early catalyst comparison altered a simple initial hypothesis that catalyst identity would merely scale reaction speed. Batch 2's simultaneous gains in conversion and selectivity instead required pathway-specific catalyst effects.

The solvent comparison further rejected a one-dimensional “faster is always better” account. Water in Batch 5 was slower but cleaner and more selective, whereas ethanol in Batch 6 converted more reagent without producing more target. Toluene in Batch 7 combined rapid target formation with a higher safety burden.

The temperature series established that conversion and useful target yield separate at high severity. Batch 10 nearly completed conversion but did not improve yield over Batch 9 and produced more byproduct and degradation.

Finally, the time series changed the explanation from simple parallel formation alone to a consecutive or reversible network. The decline in yield between Batches 9 and 12, despite conversion increasing toward unity, requires loss of target or redistribution away from it. The large degradation warning in Batch 12 makes secondary target degradation the leading explanation, while an appreciable reverse reaction remains a reasonable competing contribution.

### 7. Identifiability limits and competing explanations

Several factors remain unresolved:

- **Reverse reaction versus target degradation:** Both can reduce target at long residence time. The degradation channel is directly suggested by its warning signal, but the reverse flux cannot be quantified.
- **Parallel versus consecutive byproduct formation:** The byproduct signal may include material formed directly from R, from P, or both. The available aggregate channel does not distinguish them.
- **Catalyst deactivation:** No catalyst-loading series, catalyst-reuse test, or dense within-batch time series was performed. Deactivation cannot be separated from depletion, equilibrium, or product inhibition.
- **Temperature kinetics:** Four temperature endpoints are insufficient for trustworthy Arrhenius parameters, especially because actual transient temperatures rather than complete continuous traces were observed.
- **Solvent–catalyst interactions:** Only Catalyst B was compared across all four solvents. Catalyst rankings could change in another solvent; the current model should include possible interaction terms rather than assuming separability.
- **Mixing:** Stirring was fixed at 600 rpm, so mass-transfer limitations and stirring-rate effects remain unknown.
- **Concentration and loading:** Reagent, solvent volume, and catalyst loading were fixed across all batches. Reaction orders and catalyst saturation cannot be inferred.
- **Instrument differences:** HPLC and final-assay values were usually close but not identical. Small endpoint differences should be treated as measurement variability unless they greatly exceed the stated channel noise and are reproduced.
- **Safety composition:** Displayed safety risk is an aggregate benchmark metric. This campaign establishes empirical dependence on solvent and thermal severity but not a physical hazard decomposition.

### 8. Applicability

The explanation is best supported near the tested recipe: 0.040 mol reagent, 0.080 L solvent, 0.005 mol catalyst, 600 rpm, temperature targets of 320–410 K, and residence times of 1200–7200 s. Quantitative extrapolation beyond those ranges is speculative. In particular, behavior above 410 K, at much longer times, at other concentrations, or with mixed solvents is unknown.

Within that domain, the most defensible predictive account is that Catalyst B preferentially promotes the target pathway; solvent changes both productive and competing rates; temperature and time accelerate conversion but increasingly favor byproduct formation and target degradation; and cooling or quenching limits further thermal exposure. The target yield is therefore maximized at intermediate severity rather than at maximum conversion.

## Q — Blind predictions

### Overall rationale

Predictions use the campaign-supported network in which Catalyst B accelerates target and competing formation, while accumulated target undergoes thermally accelerated secondary loss. Conversion was projected from an Arrhenius-like exposure combining catalyst loading, temperature, and time; selectivity was reduced according to cumulative degradation exposure; yield was constrained to remain approximately conversion multiplied by selectivity; and byproduct signal was tied to the converted non-target fraction. The estimates are anchored to Catalyst B in acetonitrile from Batch 2 and use the temperature and residence-time trends from Batches 7–12. Uncertainty intervals widen for 465 K, four-hour residence, and high catalyst loading because those combinations lie beyond the directly studied domain. Quenching is treated as a thermal and safety intervention rather than as a source of a large instantaneous composition change.

### Q01

The low catalyst loading and 1800 s residence should limit conversion despite 410 K. Short exposure should preserve comparatively high selectivity and keep degradation and byproduct formation moderate.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1270 | 0.0600 | 0.2300 |
| conversion | 0.6230 | 0.4800 | 0.7600 |
| safety_risk | 0.1660 | 0.1100 | 0.2500 |
| score | 0.3290 | 0.2000 | 0.4500 |
| selectivity | 0.7960 | 0.6900 | 0.8800 |
| yield | 0.4960 | 0.3600 | 0.6200 |

### Q02

Four hours at 410 K should drive almost complete conversion even at low catalyst loading, but prolonged thermal exposure is predicted to destroy substantial target and divert material to byproducts.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6090 | 0.4300 | 0.7900 |
| conversion | 0.9980 | 0.9600 | 1.0000 |
| safety_risk | 0.2400 | 0.1600 | 0.3500 |
| score | 0.1160 | 0.0400 | 0.2300 |
| selectivity | 0.3910 | 0.2100 | 0.5600 |
| yield | 0.3900 | 0.2000 | 0.5600 |

### Q03

The high catalyst loading should achieve near-complete conversion during the short 410 K treatment. Because residence time is limited, this is predicted to retain much more target than the corresponding four-hour batch.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2810 | 0.1700 | 0.4100 |
| conversion | 0.9820 | 0.9100 | 1.0000 |
| safety_risk | 0.1880 | 0.1200 | 0.2800 |
| score | 0.4060 | 0.2700 | 0.5200 |
| selectivity | 0.7140 | 0.5900 | 0.8100 |
| yield | 0.7010 | 0.5700 | 0.8000 |

### Q04

High catalyst loading combined with four hours at 410 K is a severe extrapolation. Conversion should be complete, but catalyzed secondary loss is expected to leave little target and a very large byproduct signal.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9000 | 0.7000 | 0.9900 |
| conversion | 1.0000 | 0.9800 | 1.0000 |
| safety_risk | 0.2710 | 0.1800 | 0.3900 |
| score | 0.0070 | 0.0000 | 0.0600 |
| selectivity | 0.1000 | 0.0200 | 0.3000 |
| yield | 0.1000 | 0.0200 | 0.3000 |

### Q05

At 350 K, the low catalyst loading should give only moderate conversion after two hours. Lower thermal severity should preserve selectivity, giving a moderate yield with relatively low safety risk.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1790 | 0.0900 | 0.3000 |
| conversion | 0.6920 | 0.5500 | 0.8100 |
| safety_risk | 0.0840 | 0.0500 | 0.1400 |
| score | 0.3480 | 0.2300 | 0.4600 |
| selectivity | 0.7410 | 0.6400 | 0.8300 |
| yield | 0.5130 | 0.3900 | 0.6300 |

### Q06

The 465 K, two-hour treatment is far outside the studied safe temperature range. Complete conversion is likely, but secondary degradation should substantially reduce target yield; both chemical and safety intervals are wide because of this extrapolation.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5390 | 0.3100 | 0.7700 |
| conversion | 1.0000 | 0.9600 | 1.0000 |
| safety_risk | 0.4900 | 0.3200 | 0.7000 |
| score | 0.1080 | 0.0200 | 0.2500 |
| selectivity | 0.4610 | 0.2300 | 0.6600 |
| yield | 0.4610 | 0.2200 | 0.6600 |

### Q07

High catalyst loading should bring conversion close to completion at 350 K, but two hours allows appreciable secondary target loss. This produces more byproduct and lower selectivity than a short high-loading run, while thermal safety remains comparatively favorable.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4700 | 0.3100 | 0.6400 |
| conversion | 0.9920 | 0.9300 | 1.0000 |
| safety_risk | 0.0940 | 0.0600 | 0.1600 |
| score | 0.2490 | 0.1300 | 0.3700 |
| selectivity | 0.5260 | 0.3600 | 0.6700 |
| yield | 0.5220 | 0.3500 | 0.6700 |

### Q08

This is the most severe catalyst-temperature-time combination. The mechanistic extrapolation predicts essentially complete reagent conversion followed by extensive target destruction, with very high byproduct burden and safety risk.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9500 | 0.7400 | 1.0000 |
| conversion | 1.0000 | 0.9900 | 1.0000 |
| safety_risk | 0.5550 | 0.3500 | 0.7900 |
| score | 0.0010 | 0.0000 | 0.0400 |
| selectivity | 0.0500 | 0.0000 | 0.2600 |
| yield | 0.0500 | 0.0000 | 0.2600 |

### Q09

At the central catalyst loading, two hours at 410 K should complete conversion but pass the target-yield maximum, allowing substantial consecutive degradation and byproduct accumulation.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5830 | 0.4000 | 0.7600 |
| conversion | 0.9990 | 0.9600 | 1.0000 |
| safety_risk | 0.2470 | 0.1600 | 0.3600 |
| score | 0.1310 | 0.0500 | 0.2500 |
| selectivity | 0.4170 | 0.2400 | 0.5800 |
| yield | 0.4170 | 0.2300 | 0.5800 |

### Q10

The chemical state immediately after heating should closely match Q09. Quenching is predicted mainly to lower temperature and aggregate safety risk, with no confidently resolvable change in final conversion, yield, selectivity, or byproduct signal.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5830 | 0.4000 | 0.7600 |
| conversion | 0.9990 | 0.9600 | 1.0000 |
| safety_risk | 0.2220 | 0.1300 | 0.3300 |
| score | 0.1350 | 0.0500 | 0.2600 |
| selectivity | 0.4170 | 0.2400 | 0.5800 |
| yield | 0.4170 | 0.2300 | 0.5800 |

### Q11

Although 350 K is relatively mild, four hours at the central catalyst loading should nearly exhaust the reagent and provide enough residence time for substantial target degradation. Safety risk remains lower than in the high-temperature cases.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6320 | 0.4400 | 0.8000 |
| conversion | 0.9970 | 0.9400 | 1.0000 |
| safety_risk | 0.0940 | 0.0600 | 0.1600 |
| score | 0.1210 | 0.0400 | 0.2400 |
| selectivity | 0.3660 | 0.1900 | 0.5500 |
| yield | 0.3650 | 0.1800 | 0.5500 |

### Q12

At 465 K the central catalyst loading should produce nearly complete conversion within 1800 s. The short duration limits, but does not eliminate, secondary target loss; the safety estimate is above the nominal limit and carries substantial extrapolation uncertainty.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3170 | 0.1600 | 0.5100 |
| conversion | 0.9990 | 0.9400 | 1.0000 |
| safety_risk | 0.3790 | 0.2400 | 0.5800 |
| score | 0.2900 | 0.1400 | 0.4300 |
| selectivity | 0.6830 | 0.5000 | 0.8100 |
| yield | 0.6820 | 0.4900 | 0.8100 |

## K2 — Retrospective analysis

## 1. Reassessment of the initial information

The initial material packet contained only one substantive mechanistic prior: “The target pathway may have an appreciable reverse channel on the public support,” with moderate confidence. It did not provide a nominal kinetic law, activation energies, reaction orders, catalyst identities, or a task-specific material dossier. It also explicitly warned that solvent effects were categorical benchmark effects rather than real-property predictions.

The reversibility claim was not directly tested. The decline in target yield between Batch 9 at 3600 s and Batch 12 at 7200 s is compatible with a reverse channel, but it is also—and more directly—compatible with target degradation because the degradation warning rose from 0.136 to 0.319 while yield fell from 0.691 to 0.563. Accordingly, K1 retained `R ⇌ P` but stated that the observations “more directly support `P → D` than they support reversal.” That remains the correct evidential status: absence of a decisive contradiction is not positive confirmation of reversibility.

There was no experiment in which product was introduced into a reagent-poor mixture, nor a relaxation experiment that could show conversion moving backward. Thus the reverse rate was unidentified. No direct counterevidence emerged that was ignored without revision; rather, a broad initial possibility remained unresolved. The long-time data did cause the explanation to shift away from treating reversibility as the sole or leading reason for target loss.

The categorical nature of catalyst and solvent effects was supported operationally. Catalyst identity changed both conversion and selectivity in Batches 1–4, and solvent identity changed conversion, selectivity, byproduct burden, and risk in Batches 2 and 5–7. Nothing supports assigning these effects to real molecular properties or named catalyst chemistry. K1 appropriately avoided doing so.

Catalyst deactivation was not an initial factual claim and remained untested. K1 introduced `da/dt = -k_d a` only as an optional latent term, explicitly noting that depletion, equilibrium, product inhibition, and degradation could mimic it. Reaction-generated heat was similarly not established: the temperature changes showed finite thermal response, but not whether `Q_rxn` was appreciable.

## 2. Experiments that formed or changed the account

The first genuinely model-changing block was the catalyst screen in acetonitrile at a 350 K target. Batch 2 with Catalyst B produced conversion 0.814 and selectivity 0.725, compared with 0.667/0.567 for Catalyst A in Batch 1, 0.666/0.560 for Catalyst C in Batch 3, and 0.686/0.654 for Catalyst D in Batch 4. This rejected a simple account in which catalyst identity only multiplied a common rate. It motivated the K1 statement that catalyst multipliers must be pathway-specific.

The solvent screen changed the account again. Water in Batch 5 was slow but clean and selective, whereas ethanol in Batch 6 converted more reagent without producing more target. Toluene in Batch 7 gave the best target yield of that screen, 0.623, but also greater risk, 0.206. These results established that solvent affected productive rate, competing conversion, and safety jointly. They also motivated moving subsequent experiments to Catalyst B in toluene.

The temperature series in Batches 8, 7, 9, and 10 was the clearest evidence for an interior operating optimum. Raising the target from 320 to 380 K increased yield from 0.446 to 0.691, but raising it further to 410 K did not improve yield: Batch 10 gave 0.686 while selectivity fell, degradation rose, and risk reached 0.3539. This changed the working goal from maximizing conversion to stopping before thermal severity mainly produced damage.

The residence-time comparison was the most important mechanistic result. Batch 11 at 1200 s, Batch 9 at 3600 s, and Batch 12 at 7200 s showed conversion increasing toward unity while yield first increased and then fell. The rise in byproduct signal from 0.096 to 0.268 to 0.460 and in degradation warning from 0.016 to 0.136 to 0.319 forced the addition of a consecutive target-loss process to the explanation.

Some experimental choices were less strongly grounded. Acetonitrile, 350 K, and 3600 s were chosen as a reasonable starting condition rather than from task-specific data. The decision to transfer Catalyst B’s acetonitrile ranking to all solvent tests was an unverified extrapolation. Choosing toluene for the temperature and time studies was supported by Batch 7’s yield, but it sacrificed information about whether temperature responses differed by solvent. The 410 K point was deliberately diagnostic but approached the safety boundary. The 7200 s point was chosen to expose late-time behavior rather than to maximize score.

The quench in Batch 11 was only partially informative because there was no matched unquenched 1200 s batch. It demonstrated a 45 K temperature reduction and a risk decrease of about 0.0298, but it did not isolate a chemical quench effect.

## 3. Leading competing mechanisms and what can be distinguished

The leading account remains a mixed parallel–consecutive network:

`R ⇌ P`, `R → B`, and `P → D`.

The existing data distinguish several coarse features:

- A single irreversible `R → P` process is inadequate because target yield declines during prolonged heating.
- A common catalyst multiplier for all pathways is inadequate because catalyst identity changes selectivity.
- Conversion alone is not a sufficient process objective because nearly complete conversion can coexist with declining yield and increasing degradation.
- Thermal severity affects productive and destructive channels differently.

The data do not distinguish the following important alternatives:

1. **Reversal versus irreversible degradation.** Both can lower P. The degradation-warning increase favors `P → D`, but no observation directly showed P returning to R.
2. **Direct versus consecutive byproduct formation.** The aggregate byproduct channel cannot establish whether it is primarily `R → B`, `P → B`, or a mixture.
3. **Catalyst deactivation versus substrate depletion or product inhibition.** Endpoint comparisons do not separately identify activity loss.
4. **True kinetic temperature dependence versus thermal-history effects.** Only endpoint temperature changes were retained; no continuous trace was used to estimate warm-up or heat-generation parameters.
5. **Intrinsic chemistry versus transport.** Stirring was fixed at 600 rpm, leaving mass-transfer effects unidentified.
6. **Separable versus interacting solvent and catalyst effects.** Only Catalyst B was screened across solvents, so the catalyst ranking may be solvent-specific.

K1’s equation set was therefore a structural scaffold rather than an identified quantitative model. Its optional activity term and reversible term should not be read as experimentally measured components.

## 4. One additional complete experiment I would choose

I would run the established formulation from Batches 7–12: 0.080 L toluene, 0.040 mol reagent, and 0.005 mol Catalyst B at 600 rpm. I would heat toward 380 K for 3600 s, obtain one HPLC measurement, quench, wait for 7200 s at the post-quench thermal state, terminate, and obtain the required final assay.

This uses the same productive state as Batch 9 but then observes low-temperature relaxation rather than continued hot aging as in Batch 12. The pre-quench HPLC and final assay would measure conversion, yield, selectivity, byproduct signal, and degradation warning on either side of the relaxation period.

Possible outcomes would change the account as follows:

- If target yield fell and measured conversion also fell, with little increase in degradation warning, that would be comparatively strong evidence for a reverse `P → R` channel.
- If target yield fell while conversion remained high and degradation warning increased, that would strengthen the irreversible `P → D` explanation.
- If composition remained stable after quenching, it would indicate that the late loss in Batch 12 required sustained high temperature and that quench effectively arrested both reversal and degradation on this timescale.
- If target or conversion continued changing substantially despite cooling, the assumed “quench freezes composition” interpretation would need revision.
- If the pre-quench HPLC failed to reproduce Batch 9, batch-to-batch variability would become a larger concern and mechanistic interpretation of the unreplicated time series would weaken.

This experiment would still not deliver unique elementary rate constants, but it would target the most consequential unresolved distinction using an internal before/after comparison.

## 5. Tradeoff between identifiability and operating score

The campaign deliberately mixed screening, mechanism-oriented stress tests, and operating optimization. The catalyst and solvent screens improved both understanding and the chance of finding a productive recipe. Once Catalyst B and toluene looked favorable, however, the design concentrated later experiments in that region. That increased the probability of a strong recommendation but reduced coverage of catalyst–solvent interactions.

Batches 8–10 traded score for temperature-response information. Batch 10 at 410 K was especially diagnostic: it showed that conversion could increase without improving yield and that risk could exceed the limit. It was not a sensible recommended operating condition. Batch 12 similarly sacrificed score to reveal late target loss and degradation.

Conversely, selecting Catalyst B in toluene for five later batches was partly optimization-driven. A more identification-focused design would have replicated key conditions, crossed at least two catalysts with two solvents, varied catalyst loading, or varied stirring. Those experiments might have produced lower scores but would have made the equations more identifiable.

The research goal prioritized an explanatory and predictive account over the public score, so the temperature and time stress tests were appropriate. Nevertheless, the final design still leaned too heavily on endpoint optimization: every intermediate measurement was essentially an endpoint HPLC check, rather than a deliberately staggered within-batch kinetic series. This limited the ability to estimate rates or distinguish consecutive from reversible behavior.

## 6. Underused evidence and weaknesses in the blind predictions

Several acquired evidence streams were underused:

- The repeated HPLC/final-assay pairs could have been analyzed jointly to estimate cross-instrument discrepancy and process variability. Instead, K1 mainly treated their differences qualitatively as noise.
- Raw spectral artifacts were not inspected or compared for changes in peak assignments. Only processed estimates were used.
- Temperature-response evidence was reduced to total temperature changes. A continuous thermal trace, if available in the public artifact, was not used.
- Risk changes during setup, heating, quenching, and termination were not decomposed quantitatively. This became important because every blind query used a much smaller inventory and 400 rpm rather than the studied 600 rpm.
- The campaign had no exact replicate, so instrument noise could not be separated from batch variability.
- The near relation `yield ≈ conversion × selectivity` was recognized, but it was not formally propagated into a calibrated multivariate uncertainty model.

The least reliable blind predictions are Q08, Q04, and Q06. Q08 combines 465 K, two hours, and the high catalyst loading; Q04 combines the high catalyst loading with four hours at 410 K; Q06 uses 465 K for two hours. Q12 is also highly uncertain because 465 K was never studied, even though its duration is shorter. Q02 and Q11 extrapolate to four hours, twice the longest campaign residence time. Q01, Q03, Q05, and Q07 extrapolate catalyst loading and scale even when their temperatures are closer to the studied domain.

The most fragile predicted quantity across all twelve queries is safety risk. The campaign varied solvent and thermal severity at one inventory scale, whereas the blind batches use 0.005 L solvent and 0.003 mol reagent. I lacked evidence about whether risk scales with total inventory, concentration, peak temperature, reaction rate, or a nonlinear combination. The Q safety intervals should therefore have been wider.

The intervals for saturated conversion were also likely too narrow. For example, Q08 was assigned conversion 1.000 with an 80% interval of 0.99–1.00, and Q04 received 0.98–1.00. Those ranges express excessive confidence in an Arrhenius-like extrapolation beyond the studied catalyst-loading and temperature domain. High temperature could instead cause catalyst deactivation, reagent loss into unobserved channels, or altered thermal behavior.

The Q03 yield interval of 0.57–0.80 and Q12 interval of 0.49–0.81 may also be too narrow because both depend on an untested assumption that greater catalyst loading rapidly raises conversion without proportionally accelerating destructive chemistry. Q10 assumed quench would leave chemical metrics essentially identical to Q09; Batch 11 supported thermal risk reduction, but did not establish that chemical equivalence at 410 K after 7200 s.

These weaknesses are partly inconsistent with K1’s stated applicability. K1 limited quantitative support to 0.005 mol catalyst, 600 rpm, 320–410 K, and 1200–7200 s. Every blind query changed scale, catalyst loading, and stirring; Q02, Q04, and Q11 exceeded the time range, and Q06, Q08, and Q12 exceeded the temperature range. The prediction rationale acknowledged wider extrapolation uncertainty, but several numerical intervals did not fully honor that warning. No truth values had been supplied at the time of this retrospective, so this criticism is based on design and extrapolation logic rather than outcome knowledge.

## 7. Limitations of the sealed recommendation

The sealed recommendation selected Batch 9 because it had the highest observed safe score, 0.341, with conversion 0.948, yield 0.691, and risk 0.244. The wording “strongest safe operating result observed” was appropriate. It did not establish global or even local optimality.

Batch 9 was only one noisy realization. Batch 7 had a score of 0.328 at 350 K and lower risk, 0.206. The score difference is small enough that replicate variability could reverse their ordering. No replicate of Batch 9 was performed, and the 380 K/3600 s point was not bracketed densely in either temperature or time.

Repeatability should be tested with multiple independent replicates of Batch 9, using the same addition order, inventory, stirring, heat program, termination timing, and final assay. Both chemical metrics and actual thermal histories should be compared. The analysis should report the distribution of yield, selectivity, degradation, risk, and score rather than only their means.

Local robustness should be tested with a compact neighborhood around Batch 9—for example, temperature targets near 370, 380, and 390 K and residence times near 2400, 3600, and 4800 s—while including a few catalyst-loading perturbations. This would reveal whether Batch 9 lies on a broad plateau or a narrow ridge and whether modest control errors push risk or degradation sharply upward.

Cross-material robustness requires repeating the neighborhood in at least one other solvent and with another catalyst. Because only Catalyst B was screened across solvents, the current recommendation cannot establish that the catalyst–solvent combination is jointly optimal. Cross-world generalization is even weaker: the anonymous catalyst and categorical solvent couplings are benchmark-specific, and K1 explicitly disclaimed translation to a named real reaction.

Thus Batch 9 is the sample-best completed experiment under the observed campaign, not a proven optimum. Its recommendation is a defensible candidate for replication and local response-surface study, not a universal recipe.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 100.7 | none | 0 |
| Q | yes | 0 | 167.6 | none | 0 |
| K2 | yes | 0 | 133.9 | none | 0 |

## Scope note

This report contains only information available before truth release. Reference truth, prediction scoring, and recommendation retests are intentionally absent because the full 60-task block has not yet completed.
