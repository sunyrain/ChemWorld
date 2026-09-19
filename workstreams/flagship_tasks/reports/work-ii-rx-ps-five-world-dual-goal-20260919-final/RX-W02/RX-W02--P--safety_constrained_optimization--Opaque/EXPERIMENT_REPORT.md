# RX-W02--P--safety_constrained_optimization--Opaque

## Run summary

- World: `RX-W02`
- Locus: `P`
- Goal: `safety_constrained_optimization`
- Arm: `Opaque`
- Status: `completed`
- Source status: `completed`
- Experimental sessions: `12/12`
- Operations: `75`
- Exact replay verified: `True`
- Rollbacks: `[]`
- Posttest chain sealed: `True`

### Recovery status

- Effective result location: `source-repair-v3`
- Recovery version: `unknown`
- Repaired stages: `source`
- Source experiments rerun: `False`
- Original source thread reused: `False`
- Truth revealed during recovery: `False`

## Sealed recommendation

- Selected batch: `9`
- Rationale: Batch 9 achieved the highest observed safe score (0.2287) while keeping safety risk at 0.139, comfortably below the 0.35 limit.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S0 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 340 K x 3600 s @ 600 rpm → 340 K x 7200 s @ 600 rpm | no | 0.3792 | 0.5193 | 0.7106 | 0.3342 | 0.0690 | 0.1271 | 0.1954 |
| 2 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 340 K x 10800 s @ 600 rpm | no | 0.3885 | 0.5225 | 0.7340 | 0.3456 | 0.1380 | 0.1317 | 0.2002 |
| 3 | S0 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 340 K x 10800 s @ 600 rpm | no | 0.3514 | 0.5466 | 0.6529 | 0.3224 | 0.1193 | 0.1271 | 0.1853 |
| 4 | S0 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 340 K x 10800 s @ 600 rpm | no | 0.3287 | 0.4889 | 0.6866 | 0.3741 | 0.1259 | 0.1255 | 0.1659 |
| 5 | S1 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 340 K x 10800 s @ 600 rpm | no | 0.3262 | 0.4125 | 0.8144 | 0.4846 | 0.1766 | 0.1545 | 0.1455 |
| 6 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 340 K x 10800 s @ 600 rpm | no | 0.3001 | 0.3815 | 0.8022 | 0.5252 | 0.2462 | 0.1744 | 0.1172 |
| 7 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 340 K x 10800 s @ 600 rpm | no | 0.3302 | 0.4098 | 0.8200 | 0.5146 | 0.1948 | 0.1866 | 0.1326 |
| 8 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 320 K x 14400 s @ 600 rpm | no | 0.3449 | 0.5125 | 0.6843 | 0.3522 | 0.1234 | 0.1234 | 0.1790 |
| 9 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 360 K x 7200 s @ 600 rpm | no | 0.4248 | 0.5994 | 0.7156 | 0.3110 | 0.1145 | 0.1392 | 0.2287 |
| 10 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 330 K x 14400 s @ 600 rpm | no | 0.3753 | 0.4820 | 0.7605 | 0.4037 | 0.1629 | 0.1306 | 0.1879 |
| 11 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 9000 s @ 600 rpm | no | 0.3934 | 0.5468 | 0.7257 | 0.3260 | 0.1352 | 0.1354 | 0.2057 |
| 12 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 370 K x 6000 s @ 600 rpm | no | 0.4285 | 0.6057 | 0.6916 | 0.2881 | 0.1174 | 0.1463 | 0.2262 |

## Complete experimental actions and observations

### Batch 1

Lifecycle index: `1`; end step: `8`.

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
      "catalyst": 0,
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 340
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 8,
  "lifecycle_index": 1,
  "metrics": {
    "byproduct_signal": 0.334224671125412,
    "conversion": 0.7105699181556702,
    "cost": 1.0,
    "degradation_warning": 0.06898661702871323,
    "safety_risk": 0.12710973620414734,
    "score": 0.19538351893424988,
    "selectivity": 0.5193461179733276,
    "virtual_spectrum_summary": 0.21486754715442657,
    "yield": 0.37922346591949463
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
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 10800,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 340
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
    "byproduct_signal": 0.34558606147766113,
    "conversion": 0.7339506149291992,
    "cost": 1.0,
    "degradation_warning": 0.13795435428619385,
    "safety_risk": 0.13171806931495667,
    "score": 0.20016613602638245,
    "selectivity": 0.5225404500961304,
    "virtual_spectrum_summary": 0.2521517872810364,
    "yield": 0.3885227143764496
  },
  "ordinal": 2
}
```

### Batch 3

Lifecycle index: `3`; end step: `20`.

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
      "catalyst": 2,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 10800,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 340
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 20,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.32235679030418396,
    "conversion": 0.652940034866333,
    "cost": 1.0,
    "degradation_warning": 0.11926344037055969,
    "safety_risk": 0.12713778018951416,
    "score": 0.18527865409851074,
    "selectivity": 0.5466194152832031,
    "virtual_spectrum_summary": 0.230964794754982,
    "yield": 0.3513545095920563
  },
  "ordinal": 3
}
```

### Batch 4

Lifecycle index: `4`; end step: `26`.

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
      "catalyst": 3,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 10800,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 340
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 26,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.3741457164287567,
    "conversion": 0.6865763068199158,
    "cost": 1.0,
    "degradation_warning": 0.12594850361347198,
    "safety_risk": 0.1254574954509735,
    "score": 0.16588202118873596,
    "selectivity": 0.48885127902030945,
    "virtual_spectrum_summary": 0.2624569535255432,
    "yield": 0.32866859436035156
  },
  "ordinal": 4
}
```

### Batch 5

Lifecycle index: `5`; end step: `32`.

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
      "duration_s": 10800,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 340
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 32,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.48455941677093506,
    "conversion": 0.8144264221191406,
    "cost": 1.0,
    "degradation_warning": 0.1766452193260193,
    "safety_risk": 0.15449833869934082,
    "score": 0.1455305814743042,
    "selectivity": 0.41248849034309387,
    "virtual_spectrum_summary": 0.34599804878234863,
    "yield": 0.3262251913547516
  },
  "ordinal": 5
}
```

### Batch 6

Lifecycle index: `6`; end step: `38`.

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
      "duration_s": 10800,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 340
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 38,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.5252323150634766,
    "conversion": 0.802190899848938,
    "cost": 1.0,
    "degradation_warning": 0.24617743492126465,
    "safety_risk": 0.17440274357795715,
    "score": 0.1171729564666748,
    "selectivity": 0.3815041184425354,
    "virtual_spectrum_summary": 0.39965760707855225,
    "yield": 0.30014768242836
  },
  "ordinal": 6
}
```

### Batch 7

Lifecycle index: `7`; end step: `44`.

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
      "duration_s": 10800,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 340
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 44,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.5145618915557861,
    "conversion": 0.8199864029884338,
    "cost": 1.0,
    "degradation_warning": 0.19484518468379974,
    "safety_risk": 0.18662424385547638,
    "score": 0.13255469501018524,
    "selectivity": 0.4097822606563568,
    "virtual_spectrum_summary": 0.37068936228752136,
    "yield": 0.3302285075187683
  },
  "ordinal": 7
}
```

### Batch 8

Lifecycle index: `8`; end step: `50`.

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
      "duration_s": 14400,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 320
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 50,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.352242112159729,
    "conversion": 0.6842505931854248,
    "cost": 1.0,
    "degradation_warning": 0.12344589829444885,
    "safety_risk": 0.12335024029016495,
    "score": 0.17900492250919342,
    "selectivity": 0.5125463604927063,
    "virtual_spectrum_summary": 0.2492838054895401,
    "yield": 0.3448772132396698
  },
  "ordinal": 8
}
```

### Batch 9

Lifecycle index: `9`; end step: `56`.

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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 360
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
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.311046838760376,
    "conversion": 0.7155691385269165,
    "cost": 1.0,
    "degradation_warning": 0.11448966711759567,
    "safety_risk": 0.13918258249759674,
    "score": 0.22869804501533508,
    "selectivity": 0.5993695855140686,
    "virtual_spectrum_summary": 0.22259610891342163,
    "yield": 0.4248272776603699
  },
  "ordinal": 9
}
```

### Batch 10

Lifecycle index: `10`; end step: `62`.

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
      "duration_s": 14400,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 330
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 62,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.4037269353866577,
    "conversion": 0.7605406045913696,
    "cost": 1.0,
    "degradation_warning": 0.162934809923172,
    "safety_risk": 0.1305992603302002,
    "score": 0.18791861832141876,
    "selectivity": 0.48200416564941406,
    "virtual_spectrum_summary": 0.295370489358902,
    "yield": 0.37533295154571533
  },
  "ordinal": 10
}
```

### Batch 11

Lifecycle index: `11`; end step: `68`.

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
      "duration_s": 9000,
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
  "end_step": 68,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.32596927881240845,
    "conversion": 0.7257109880447388,
    "cost": 1.0,
    "degradation_warning": 0.1351863443851471,
    "safety_risk": 0.13539886474609375,
    "score": 0.20570996403694153,
    "selectivity": 0.5468462109565735,
    "virtual_spectrum_summary": 0.24011696875095367,
    "yield": 0.39339202642440796
  },
  "ordinal": 11
}
```

### Batch 12

Lifecycle index: `12`; end step: `75`.

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
      "duration_s": 6000,
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
  "end_step": 75,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.2881069779396057,
    "conversion": 0.6915733218193054,
    "cost": 1.0,
    "degradation_warning": 0.11735647916793823,
    "safety_risk": 0.146257683634758,
    "score": 0.22619260847568512,
    "selectivity": 0.6057479381561279,
    "virtual_spectrum_summary": 0.21126925945281982,
    "yield": 0.4285356402397156
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

1. Scope and evidentiary basis

This report describes a bounded synthetic reaction-and-thermal benchmark, not a named real chemical synthesis. The reagent and catalysts were anonymous benchmark materials, and solvent effects were categorical benchmark effects. Consequently, the terms “product,” “byproduct,” and “degradation” below denote public assay channels rather than identified molecular species.

I completed 12 batches. Every batch used 0.040 mol reagent, 0.080 L solvent, 0.005 mol catalyst, and 600 rpm stirring. Therefore, the campaign identifies relative catalyst, solvent, and temperature–time effects only near those fixed quantities and that mixing condition. All quoted endpoint values are final-assay observations unless explicitly labeled as an intermediate HPLC result.

2. Proposed process model

A compact explanation is a temperature-dependent network of competing reactions:

R -> P       desired route, rate kP(T,catalyst,solvent)
R -> B       parallel byproduct route, rate kB(T,catalyst,solvent)
P -> D       product degradation, rate kPD(T,solvent)
B -> D or other impurities, rate kBD(T,solvent)

A minimal kinetic representation would be:

dR/dt = -(kP + kB)R
dP/dt = kP R - kPD P
dB/dt = kB R - kBD B
dD/dt = kPD P + kBD B

The measured conversion primarily reflects loss of R, whereas yield and selectivity depend on how much reacted material follows and remains on the P branch. Thus, high conversion alone is not evidence of a good process. Temperature, catalyst, solvent, and exposure time affect both the rate of disappearance of R and the branching or degradation rates.

The endpoint behavior suggests that water plus Catalyst B provides the best balance of kP against kB and degradation in the tested domain. Several non-water solvents apparently increase overall reaction rate but increase the undesired branch still more strongly. Shorter, hotter water runs around 360–370 K appear to exploit a favorable kinetic window: rapid formation of P with less cumulative time for side reactions than longer, cooler runs.

This interpretation does not require a literal elementary mechanism. The same equations can represent effective pathways involving intermediates, catalyst activation, solvent-dependent catalyst states, or mass-transfer effects.

3. Catalyst effects

Batches 1–4 compared all four catalysts in water at 340 K and 10,800 s.

Batch 1, Catalyst A: conversion 0.7106, yield 0.3792, selectivity 0.5193, byproduct 0.3342, degradation warning 0.0690, risk 0.1271, score 0.1954.

Batch 2, Catalyst B: conversion 0.7340, yield 0.3885, selectivity 0.5225, byproduct 0.3456, degradation warning 0.1380, risk 0.1317, score 0.2002.

Batch 3, Catalyst C: conversion 0.6529, yield 0.3514, selectivity 0.5466, byproduct 0.3224, degradation warning 0.1193, risk 0.1271, score 0.1853.

Batch 4, Catalyst D: conversion 0.6866, yield 0.3287, selectivity 0.4889, byproduct 0.3741, degradation warning 0.1259, risk 0.1255, score 0.1659.

These observations led me to use Catalyst B for subsequent optimization. Catalyst B was not overwhelmingly superior in intrinsic selectivity: Catalyst C actually gave the highest measured selectivity in this four-batch comparison. Catalyst B instead gave the best observed combination of conversion and yield, and therefore the best score. Catalyst D was least favorable because it combined relatively low yield with low selectivity and high byproduct signal.

The catalyst ranking should be treated as local. Only one catalyst loading was tested, and each catalyst-condition combination had one final assay. It remains possible that Catalyst C would outperform Catalyst B at a different temperature, residence time, or loading.

4. Solvent coupling

Batches 2 and 5–7 compared solvents with Catalyst B at 340 K for 10,800 s.

Batch 2, water: conversion 0.7340, yield 0.3885, selectivity 0.5225, byproduct 0.3456, degradation 0.1380, risk 0.1317, score 0.2002.

Batch 5, ethanol: conversion 0.8144, yield 0.3262, selectivity 0.4125, byproduct 0.4846, degradation 0.1766, risk 0.1545, score 0.1455.

Batch 6, acetonitrile: conversion 0.8022, yield 0.3001, selectivity 0.3815, byproduct 0.5252, degradation 0.2462, risk 0.1744, score 0.1172.

Batch 7, toluene: conversion 0.8200, yield 0.3302, selectivity 0.4098, byproduct 0.5146, degradation 0.1948, risk 0.1866, score 0.1326.

This comparison was the clearest evidence that conversion is not the optimization target by itself. Every non-water solvent produced higher conversion than water, yet all produced lower yield, selectivity, and score, with substantially larger byproduct and degradation signals. I therefore infer that ethanol, acetonitrile, and toluene increase effective reaction rate but disproportionately favor kB and/or degradation. Water suppresses total conversion somewhat while preserving more productive branching.

A competing explanation is that solvent-dependent assay response or phase behavior changes the public channels rather than altering chemical branching. Because only final multichannel estimates were available and the benchmark explicitly uses categorical solvent coupling, those possibilities cannot be separated. Operationally, however, water was robustly superior under the tested conditions.

5. Temperature–time behavior in water with Catalyst B

Batches 2 and 8–12 map a limited temperature–time surface:

Batch 8: 320 K, 14,400 s; conversion 0.6843, yield 0.3449, selectivity 0.5125, byproduct 0.3522, degradation 0.1234, risk 0.1234, score 0.1790.

Batch 10: 330 K, 14,400 s; conversion 0.7605, yield 0.3753, selectivity 0.4820, byproduct 0.4037, degradation 0.1629, risk 0.1306, score 0.1879.

Batch 2: 340 K, 10,800 s; conversion 0.7340, yield 0.3885, selectivity 0.5225, byproduct 0.3456, degradation 0.1380, risk 0.1317, score 0.2002.

Batch 11: 350 K, 9,000 s; conversion 0.7257, yield 0.3934, selectivity 0.5468, byproduct 0.3260, degradation 0.1352, risk 0.1354, score 0.2057.

Batch 9: 360 K, 7,200 s; conversion 0.7156, yield 0.4248, selectivity 0.5994, byproduct 0.3110, degradation 0.1145, risk 0.1392, score 0.2287.

Batch 12: 370 K, 6,000 s; conversion 0.6916, yield 0.4285, selectivity 0.6057, byproduct 0.2881, degradation 0.1174, risk 0.1463, score 0.2262.

Across this deliberately coupled sequence, increasing temperature while shortening time improved yield and selectivity through 360–370 K despite similar or somewhat lower conversion. Byproduct signal declined from 0.4037 in the long 330 K run to 0.3110 at 360 K and 0.2881 at 370 K. This supports a residence-time explanation: long exposure allows parallel or sequential side chemistry to accumulate, whereas a hotter, shorter pulse generates product rapidly and terminates before as much undesired material forms.

The data do not establish that temperature itself intrinsically increases selectivity. Temperature and time changed together, so the apparent improvement could be due chiefly to shorter exposure, to a temperature-dependent change in branching, or to both. The non-monotonic outcomes also argue against fitting a simple single-variable temperature law from these data.

Batch 9 had the highest final safe score, 0.2287, and was consequently selected as the recommendation. Batch 12 had a slightly higher yield and selectivity but also higher risk and a slightly lower final score, 0.2262. This suggests a shallow optimum or ridge near 360–370 K and 6,000–7,200 s rather than a sharply identified optimum.

6. Time-course evidence and measurement variability

Batch 1 included an intermediate HPLC measurement after the first 3,600 s at 340 K. It reported conversion 0.3375, yield 0.1897, selectivity 0.5822, and byproduct signal 0.1436. After another 7,200 s, the final assay reported conversion 0.7106, yield 0.3792, selectivity 0.5193, and byproduct 0.3342. Although the two instruments have different calibrations and noise, the direction is consistent with continuing conversion and product formation accompanied by accumulating byproduct and declining selectivity over extended exposure. This observation helped motivate shorter high-temperature runs.

Batch 12 also had a pre-termination HPLC measurement. It reported conversion 0.7116, yield 0.4316, selectivity 0.6165, byproduct 0.2944, and a contemporaneous displayed score of 0.2321. The final assay then reported conversion 0.6916, yield 0.4285, selectivity 0.6057, byproduct 0.2881, and score 0.2262. No intervening reaction step occurred. This difference is direct evidence of instrument/channel noise and calibration differences, not reaction dynamics. Consequently, distinctions of only a few thousandths in score or a few percentage points in an assay channel should not be overinterpreted. Batch 9’s advantage over Batch 12 is real as an observed leaderboard result but is not sufficient to claim a precisely located mechanistic optimum.

7. Safety and score coupling

All completed batches respected the declared safety limit of 0.35. Observed endpoint risks ranged from 0.1234 to 0.1866. In water, risk generally increased as the chosen temperature rose, even when time fell: 0.1234 at 320 K/14,400 s, 0.1392 at 360 K/7,200 s, and 0.1463 at 370 K/6,000 s. Non-water solvents also showed greater risk, reaching 0.1545 for ethanol, 0.1744 for acetonitrile, and 0.1866 for toluene at 340 K.

Risk behaved as a path-dependent operational quantity rather than merely an endpoint impurity measurement. For example, adding 0.040 mol reagent contributed about 0.0363 risk and adding 0.080 L water brought the early batch risk to about 0.0722 before heating. Heating then added condition-dependent risk. The catalyst addition did not visibly increase risk in the tested setup. A useful conceptual model is therefore:

risk_total = risk_charge(reagent, solvent, quantities) + integral hazard(T(t), solvent, composition) dt

This is descriptive rather than an identified equation. The exact hazard function is unknown.

The score rose with productive yield and selectivity and fell with safety burden and undesired chemistry, but I did not identify an exact scoring equation. The ranking makes clear that neither conversion nor yield alone determines it. For example, Batch 7 had the campaign’s highest conversion, 0.8200, but scored only 0.1326 because selectivity, byproduct, and risk were unfavorable. Batch 9 converted less material, 0.7156, yet scored 0.2287 because its yield/selectivity/risk balance was much better.

8. Recommended operating interpretation

Within the tested domain, the strongest supported procedure is the exact Batch 9 recipe:

- 0.040 mol anonymous limiting reagent
- 0.080 L water
- 0.005 mol Catalyst B
- heat at a target of 360 K for 7,200 s
- stir at 600 rpm
- terminate, then assay

Its final observed results were yield 0.4248, selectivity 0.5994, conversion 0.7156, byproduct signal 0.3110, degradation warning 0.1145, safety risk 0.1392, and score 0.2287. These are observations from a single synthetic benchmark batch, not guaranteed future values.

Batch 12, 370 K for 6,000 s, is a plausible neighboring alternative. Its final score was slightly lower, but its yield, selectivity, and byproduct values were competitive. I would describe the supported region as a short, moderately hot water/Catalyst B process rather than claiming that exactly 360 K is a fundamental optimum.

9. Unidentified factors and competing explanations

Several important effects remain unidentified:

- Catalyst loading: all batches used 0.005 mol. Activity, selectivity, cost, and risk at lower loading are unknown.
- Reagent concentration and solvent volume: all batches used 0.040 mol reagent and 0.080 L solvent. Concentration-order effects cannot be estimated.
- Stirring and transport: all heated batches used 600 rpm. A mass-transfer-controlled explanation cannot be excluded.
- Addition order: reagent, solvent, and catalyst were charged in the same order. Activation or mixing transients were not tested.
- Thermal trajectory: only target temperature and duration were controlled publicly. Heat-up dynamics may contribute to effective exposure.
- Quenching: no batch used an explicit quench. Post-heating stabilization effects remain unknown.
- Replication: there were no exact final-assay replicates, so process variability cannot be separated cleanly from instrument noise.
- Catalyst–solvent interactions: all solvent comparisons used Catalyst B, while all catalyst comparisons used water. A full interaction matrix was not measured.
- Species identity: no molecular assignments or real catalyst identities were public. Any molecular-level mechanism would be speculation.

Reasonable competing models include: a purely parallel R-to-P/R-to-B network; consecutive formation and destruction of P; solvent-dependent catalyst activation/deactivation; phase or transport effects that change apparent rates; and solvent-dependent analytical response. The data favor an effective branching-plus-degradation model because selectivity declines with prolonged exposure and non-water solvents raise conversion while lowering product quality, but they do not uniquely distinguish these microscopic explanations.

10. Final confidence statement

I have high confidence in the local empirical conclusions that water outperformed the other three solvents, Catalyst B gave the best observed score among catalysts at 340 K, all tested procedures stayed below the 0.35 safety limit, and the best observed region was 360–370 K with shorter residence times. I have moderate confidence in the proposed competition between desired formation, byproduct formation, and degradation. I have low confidence in any extrapolation outside the tested quantities, loading, mixing rate, solvent–catalyst combinations, or 320–370 K optimization series. The proposed equations should therefore be read as a compact causal hypothesis consistent with the campaign, not as a uniquely identified kinetic law.

## Q — Blind predictions

### Overall rationale

Predictions are based only on the completed campaign. The main anchors were the acetonitrile/Catalyst B batch at 340 K for 10800 s, which showed high conversion but poor selectivity and substantial byproduct, and the water/Catalyst B temperature–time series, which showed that shorter hot treatments could improve product retention. All queries use much smaller charges, a slightly higher catalyst-to-reagent ratio, 400 rpm rather than 600 rpm, and temperatures extending to 460 K; these are material extrapolations. The intervals therefore include assay noise, uncertain concentration and mixing effects, uncertain high-temperature kinetics, and unmeasured quench behavior. I treated conversion as reactant disappearance, yield as retained target product, selectivity as productive branching, byproduct signal as accumulated undesired material, and safety risk as a path-dependent charge-plus-thermal hazard. Score intervals reflect joint uncertainty in productive metrics and safety rather than an asserted exact scoring equation.

### Q01

The 420 K pulse should give high conversion despite its shorter duration, but acetonitrile is expected to favor the byproduct branch. This is a substantial temperature extrapolation beyond the directly observed acetonitrile batch, so the intervals are broad.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4700 | 0.3100 | 0.6400 |
| conversion | 0.8600 | 0.6900 | 0.9700 |
| safety_risk | 0.2300 | 0.1500 | 0.3400 |
| score | 0.1700 | 0.0800 | 0.2500 |
| selectivity | 0.4600 | 0.3100 | 0.6100 |
| yield | 0.3900 | 0.2500 | 0.5200 |

### Q02

The chemistry should be close to Q01 because quenching occurs only after the specified heating period. I predict a modest safety benefit and slightly better retained product, while recognizing that the effect of quenching was not identified experimentally.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4700 | 0.3100 | 0.6400 |
| conversion | 0.8600 | 0.6900 | 0.9700 |
| safety_risk | 0.2000 | 0.1200 | 0.3100 |
| score | 0.1800 | 0.0900 | 0.2700 |
| selectivity | 0.4700 | 0.3200 | 0.6200 |
| yield | 0.4000 | 0.2500 | 0.5300 |

### Q03

At 390 K for 3300 s, conversion should be lower than at 420 K, while the shorter and cooler exposure should preserve selectivity. The estimate interpolates between the favorable short hot water runs and the less selective acetonitrile observation.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4200 | 0.2700 | 0.5800 |
| conversion | 0.7200 | 0.5300 | 0.8700 |
| safety_risk | 0.1700 | 0.1000 | 0.2700 |
| score | 0.1700 | 0.0900 | 0.2500 |
| selectivity | 0.5000 | 0.3500 | 0.6400 |
| yield | 0.3600 | 0.2300 | 0.4900 |

### Q04

The 450 K treatment should nearly exhaust the reactant but is expected to accelerate side-product formation and degradation strongly in acetonitrile. It lies well outside the experimentally optimized temperature range and may approach the safety limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6100 | 0.4200 | 0.7900 |
| conversion | 0.9500 | 0.8200 | 1.0000 |
| safety_risk | 0.3400 | 0.2200 | 0.4900 |
| score | 0.0850 | 0.0150 | 0.1800 |
| selectivity | 0.3200 | 0.1700 | 0.4900 |
| yield | 0.3000 | 0.1500 | 0.4500 |

### Q05

The short 1500 s exposure should limit conversion but also suppress cumulative byproduct formation. I therefore expect better selectivity than Q01 and a comparable score despite the lower conversion.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3000 | 0.1700 | 0.4500 |
| conversion | 0.5800 | 0.3900 | 0.7500 |
| safety_risk | 0.1500 | 0.0800 | 0.2400 |
| score | 0.1800 | 0.0900 | 0.2700 |
| selectivity | 0.5800 | 0.4200 | 0.7100 |
| yield | 0.3400 | 0.2100 | 0.4700 |

### Q06

Longer exposure at 420 K should drive conversion close to completion, but the campaign showed that prolonged reaction can reduce selectivity and accumulate byproduct. The predicted score is consequently below that of the 3300 s treatment.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6200 | 0.4400 | 0.7900 |
| conversion | 0.9500 | 0.8300 | 1.0000 |
| safety_risk | 0.3000 | 0.2000 | 0.4300 |
| score | 0.0900 | 0.0200 | 0.1800 |
| selectivity | 0.3400 | 0.1900 | 0.5000 |
| yield | 0.3100 | 0.1600 | 0.4500 |

### Q07

The initial 390 K stage should form product and intermediates before the 450 K stage. I expect the final hot stage to convert much of the remainder but also degrade or divert some previously formed product, giving high conversion and moderate-to-low selectivity.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5500 | 0.3700 | 0.7200 |
| conversion | 0.9100 | 0.7500 | 0.9900 |
| safety_risk | 0.2900 | 0.1900 | 0.4200 |
| score | 0.1200 | 0.0400 | 0.2100 |
| selectivity | 0.3900 | 0.2300 | 0.5500 |
| yield | 0.3500 | 0.2000 | 0.4900 |

### Q08

Total thermal exposure matches Q07, but placing the cooler stage last may permit additional productive conversion without ending at the most degrading condition. I therefore predict similar conversion and risk but modestly better selectivity and yield; this ordering effect is speculative.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5000 | 0.3200 | 0.6800 |
| conversion | 0.9100 | 0.7500 | 0.9900 |
| safety_risk | 0.2900 | 0.1900 | 0.4200 |
| score | 0.1400 | 0.0500 | 0.2300 |
| selectivity | 0.4400 | 0.2800 | 0.5900 |
| yield | 0.3900 | 0.2300 | 0.5300 |

### Q09

A brief 440 K pulse should produce moderate-to-high conversion while limiting residence-time-driven degradation. Its higher temperature makes both risk and side reaction more uncertain than for the campaign's 360–370 K runs.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3500 | 0.2000 | 0.5100 |
| conversion | 0.7000 | 0.5000 | 0.8600 |
| safety_risk | 0.2000 | 0.1200 | 0.3100 |
| score | 0.1800 | 0.0800 | 0.2800 |
| selectivity | 0.5400 | 0.3700 | 0.6800 |
| yield | 0.3800 | 0.2300 | 0.5100 |

### Q10

The final composition should remain close to Q09 because quenching follows the full heating period. I assign a modest risk reduction and small product-retention benefit, but quench behavior was unmeasured and is a major source of uncertainty.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3500 | 0.2000 | 0.5100 |
| conversion | 0.7000 | 0.5000 | 0.8600 |
| safety_risk | 0.1700 | 0.0900 | 0.2800 |
| score | 0.1900 | 0.0900 | 0.2900 |
| selectivity | 0.5500 | 0.3800 | 0.6900 |
| yield | 0.3900 | 0.2400 | 0.5200 |

### Q11

This condition is closest in temperature and duration to the campaign's short hot runs, but it uses acetonitrile, which previously raised conversion while depressing selectivity. I therefore predict respectable conversion but appreciably more byproduct than the analogous water process.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4600 | 0.3000 | 0.6200 |
| conversion | 0.7800 | 0.6100 | 0.9100 |
| safety_risk | 0.1600 | 0.0900 | 0.2500 |
| score | 0.1500 | 0.0700 | 0.2300 |
| selectivity | 0.4500 | 0.3000 | 0.6000 |
| yield | 0.3500 | 0.2200 | 0.4800 |

### Q12

The combination of 460 K, 6300 s, and acetonitrile is an extreme extrapolation. I expect nearly complete reactant disappearance but extensive byproduct formation, degradation, and a likely safety-limit violation, leaving little retained target product and a near-zero safe score.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8200 | 0.6200 | 0.9600 |
| conversion | 0.9950 | 0.9400 | 1.0000 |
| safety_risk | 0.5800 | 0.4000 | 0.7800 |
| score | 0.0100 | 0.0000 | 0.0600 |
| selectivity | 0.1000 | 0.0200 | 0.2400 |
| yield | 0.0800 | 0.0100 | 0.2000 |

## K2 — Retrospective analysis

1. Assessment of claims available at the outset

The initial material packet contained almost no substantive, task-specific mechanistic claims. It explicitly said that no nominal property dossier was supplied, that the catalysts were anonymous benchmark formulations, and that solvent effects were categorical benchmark effects rather than predictions from ordinary real-solvent chemistry. Those boundary statements were respected and remain supported: nothing in the campaign justifies assigning a molecular identity to the reagent, product, catalyst, or mechanism, or interpreting the solvent ranking as a general claim about real water, ethanol, acetonitrile, and toluene.

The initial task contract did make operational claims: final assays were required, the safety limit was 0.35, and the public observables included conversion, yield, selectivity, byproduct, degradation warning, risk, and score. All 12 completed batches stayed below that declared safety limit, with observed endpoint risks from 0.1234 to 0.1866. This supports feasibility under the explored conditions, not universal safety.

Most scientific propositions in K1 were generated from the campaign rather than inherited from the initial information. In particular, K1 proposed competing desired, byproduct, and degradation pathways and concluded that “water plus Catalyst B provides the best balance” locally. The local performance data support that operational statement, but they do not establish its molecular cause.

Several claims remained untested rather than merely free of counterevidence. These include effects of catalyst loading, reagent concentration, solvent volume, stirring speed, addition order, quenching, and catalyst–solvent interactions outside water/Catalyst B. K1 expressly listed these limitations. It would be incorrect to say that the campaign supported invariance to those factors; they were held fixed or absent.

There was also evidence that should temper some language in K1. The report described the shorter, hotter water runs as exploiting a favorable kinetic window and suggested that long exposure allows side chemistry to accumulate. That interpretation is plausible, but temperature and time were deliberately changed together in Batches 8–12. Thus, there was already a confounding problem when K1 was written. I acknowledged it later in the same report, but phrases such as “long exposure allows” were stronger than the identification warranted. This is not undiscovered counterevidence; it is a limitation visible at the time that should have been given more weight.

Likewise, Catalyst B was called the best balance, but Batch 3 with Catalyst C had higher selectivity than Batch 2 with Catalyst B: 0.5466 versus 0.5225. Catalyst B was selected because its conversion, yield, and score were higher, not because every chemical-quality channel was superior. Batch 1 with Catalyst A also had a much lower final degradation warning than Batch 2, 0.0690 versus 0.1380. These observations were reported rather than hidden, but they contradict any broad claim that Catalyst B dominates all other catalysts mechanistically.

2. Experiments that formed or changed the interpretation

The initial Batch 1 condition—water, Catalyst A, 340 K, and a total of 10,800 s—was mainly an unvalidated starting guess. There was no task-specific dossier from which to derive 340 K, 600 rpm, full reagent charge, full solvent volume, or full catalyst loading. The symmetric campaign stock limits encouraged using 0.040 mol reagent, 0.080 L solvent, and 0.005 mol catalyst per batch, but that was a resource-allocation convenience rather than a scientific conclusion.

Batch 1’s intermediate HPLC measurement genuinely shaped the subsequent interpretation. After 3,600 s it reported conversion 0.3375, yield 0.1897, selectivity 0.5822, and byproduct 0.1436. The final assay after another 7,200 s reported conversion 0.7106, yield 0.3792, selectivity 0.5193, and byproduct 0.3342. This suggested continuing conversion accompanied by accumulating byproduct and declining selectivity. However, the comparison crossed instruments and sampling times, so it was suggestive rather than a clean kinetic measurement.

Batches 2–4 were the first deliberate mechanistic screen. At fixed water, 340 K, and 10,800 s, they compared Catalysts B, C, and D against Batch 1’s Catalyst A. They established that catalyst category mattered and led me to choose Catalyst B for subsequent work. This choice was data-driven in terms of score, but the screen consisted of only one observation per catalyst.

Batches 5–7 most strongly changed my optimization logic. Ethanol, acetonitrile, and toluene with Catalyst B all produced higher conversion than water but markedly worse selectivity, byproduct, degradation, risk, and score. For example, Batch 7 reached conversion 0.8200 but scored only 0.1326, whereas water Batch 2 converted 0.7340 and scored 0.2002. This directly overturned any simple conversion-maximization strategy and caused me to treat branching and product retention as central.

Batches 8–12 formed the apparent temperature–time ridge. The progression from Batch 8 at 320 K for 14,400 s to Batch 9 at 360 K for 7,200 s and Batch 12 at 370 K for 6,000 s showed improved yield and selectivity in the shorter, hotter region. Batch 9’s score of 0.2287 became the highest final score; Batch 12 was close at 0.2262. These experiments changed the preferred operating region, but they were primarily adaptive optimization rather than a balanced kinetic design.

The second intermediate measurement, in Batch 12, was scientifically important but arrived too late to influence another experiment. HPLC immediately before termination gave conversion 0.7116, yield 0.4316, selectivity 0.6165, and displayed score 0.2321, while the final assay without an intervening reaction step gave 0.6916, 0.4285, 0.6057, and 0.2262. This demonstrated instrument or channel variability on approximately the same scale as the score difference between Batches 9 and 12.

The exact temperature choices after Batch 7—320, 360, 330, 350, and 370 K with different durations—were guided by emerging data but still contained unvalidated assumptions. In particular, I assumed that coupling increasing temperature to decreasing duration was a sensible way to search for a productive ridge. That was useful for optimization but prevented clean attribution of the effect to temperature or time.

3. Principal competing mechanisms and explanations

K1’s effective reaction network remains one reasonable explanation:

R -> P, R -> B, followed by possible P -> D and B -> D processes.

It accounts qualitatively for conversion increasing while selectivity falls and for high-conversion non-water batches having poor yield. The evidence distinguishes this general class from a model in which all converted reagent becomes stable target product: Batches 5–7 clearly contradict that simpler model.

The campaign does not distinguish several more specific explanations:

- Parallel branching versus sequential degradation: low selectivity may arise because R is diverted directly to B, because initially formed P later degrades, or through both processes.
- Temperature-dependent selectivity versus residence-time damage: Batches 8–12 changed temperature and duration together.
- Solvent-dependent kinetics versus analytical or phase effects: non-water solvents may alter the actual reaction network, the effective catalyst state, phase partitioning, or public assay response.
- Homogeneous kinetic control versus transport control: stirring was fixed at 600 rpm, so the effect of mass transfer is unidentified.
- Catalyst identity effects versus catalyst activation or deactivation: one loading and one addition protocol were used.
- True process variability versus measurement variability: there were no exact final-assay replicates.

Existing experiments can distinguish operational rankings under the tested recipes. They show, for example, that water/Catalyst B at 360–370 K with short exposure was better than the tested acetonitrile/Catalyst B condition at 340 K for 10,800 s. They cannot establish molecular causation or predict how the ranking changes at the much smaller charges, different stirring rate, and 390–460 K conditions used in the sealed blind questions.

A particularly important competitive interpretation is that the apparent hot/short advantage is mostly an exposure-time effect rather than a favorable high-temperature branching ratio. Another is the opposite: higher temperature intrinsically favors productive branching, while the shorter duration merely prevents later degradation. The current design cannot separate these.

4. One additional complete experiment I would choose

If restricted to one legal complete experiment, I would run the established water/Catalyst B formulation—0.040 mol reagent, 0.080 L water, 0.005 mol Catalyst B, and 600 rpm—at 330 K for 7,200 s, followed by termination and a final assay. I would prefer a pre-termination HPLC measurement as well if one nonfinal measurement were permitted within that complete experiment, but the final assay would remain the decisive comparable endpoint.

This condition fills the most useful missing cell in the existing temperature–time design. It can be compared at fixed temperature with Batch 10, which used 330 K for 14,400 s, and at fixed duration with Batch 9, which used 360 K for 7,200 s.

Possible interpretations would be:

- If the 330 K/7,200 s batch had low conversion but materially higher selectivity and lower byproduct than Batch 10, that would support cumulative residence-time damage at 330 K.
- If it retained Batch 10’s poor selectivity despite the shorter duration, that would support an intrinsically less favorable branching ratio at 330 K.
- If it approached Batch 9 in yield and selectivity but with lower risk, then time would appear more important than temperature, and the recommendation might shift downward in temperature.
- If it had much lower conversion and yield while preserving selectivity, the data would support an activation-rate limitation at 330 K and strengthen the case for the hotter process.
- If results were inconsistent with both comparisons beyond assay uncertainty, process variability, heat-up history, or an inadequately specified kinetic network would become more credible.

An exact replicate of Batch 9 would be preferable for estimating repeatability, but the 330 K/7,200 s experiment offers greater mechanistic discrimination from a single additional batch. This choice explicitly prioritizes identifiability over merely attempting another high score.

5. Tradeoff between mechanistic identifiability and score improvement

The campaign began with a meaningful amount of identification work. Batches 1–4 screened catalysts, and Batches 5–7 screened all solvents with the selected catalyst. Those batches consumed seven of the twelve available vessels, including conditions that were unlikely to beat the current score after early evidence emerged. In particular, continuing through acetonitrile and toluene after ethanol had already shown a conversion/selectivity tradeoff sacrificed near-term score optimization to establish that the solvent effect was systematic rather than isolated.

After Batch 7, the balance shifted strongly toward optimization. Batches 8–12 searched the water/Catalyst B temperature–time region. Coupling higher temperature with shorter duration was efficient for finding a good procedure, but it sacrificed factorial identifiability. No exact replicate was run, no catalyst loading was varied, and no stirring comparison was performed.

The safe-score objective also encouraged conservative thermal exploration. All experimental endpoint risks remained far below 0.35, so in retrospect the campaign may have been overly cautious in its optimization range. Conversely, avoiding very high temperatures reduced the ability to locate the onset of thermal degradation or the safety boundary. That was a rational safety-oriented choice but limited model extrapolation.

Using the full per-batch share of all stocks simplified the campaign and maximized the chance of measurable outcomes, yet it made the cost channel nearly constant and prevented learning about catalyst efficiency. This was optimization by standardization rather than mechanistic design.

Only two of the twelve available nonfinal measurements were used. More time-course measurements could have improved kinetic identifiability without consuming additional vessels, although they would have consumed sample and potentially perturbed volumes. The limited use of this resource was a design weakness.

6. Evidence that was underused and weaknesses in the blind predictions

The raw characterization artifacts were not examined in depth. I relied mostly on processed estimates and peak summaries rather than analyzing peak shapes, assignments, mass-balance metadata, or cross-channel discrepancies. Given that the instruments were synthetic and independently calibrated, raw spectra might not have resolved the hidden mechanism, but they could have exposed saturation, missingness, or systematic disagreement.

Operation-level safety increments were also underused. The logs showed approximately 0.0363 risk from the full reagent charge and an early total near 0.0722 after adding water. A more formal decomposition of charge risk and thermal risk could have improved the later safety predictions. Instead, the blind predictions used a qualitative path-dependent risk model.

The Batch 12 HPLC/final-assay discrepancy was acknowledged but not propagated rigorously into every blind interval. It demonstrated that a few hundredths in conversion or selectivity and several thousandths in score can arise without further reaction. The final prediction intervals included broad extrapolation uncertainty, but their point-to-point distinctions—especially the claimed small benefits of quenching—were more precise than the evidence justified.

The least reliable sealed predictions are Q12, Q04, and Q06. Q12 extrapolated to 460 K for 6,300 s and assigned conversion 0.995, risk 0.58, and score 0.01. No campaign experiment exceeded 370 K, so all three quantities depend heavily on an assumed acceleration of conversion, degradation, and hazard. Q04 at 450 K for 3,300 s and Q06 at 420 K for 5,100 s have the same problem, though less severely.

Q02 and Q10 are also highly uncertain because K1 explicitly stated that quenching was untested. The predictions assigned modest safety and product-retention benefits relative to Q01 and Q09. That direction was speculative; quenching could have no effect after termination-equivalent stopping, could add operational risk, or could affect public state in a benchmark-specific way.

Q07 and Q08 are unreliable because they infer an ordering effect between 390 K and 450 K stages. The campaign did not test temperature sequencing. The prediction that the high-then-low order would preserve more product was mechanistically plausible but unsupported by direct evidence.

All twelve blind questions used 0.003 mol reagent, 0.005 L solvent, 0.000525 mol catalyst, and 400 rpm. These differ sharply from the campaign’s 0.040 mol, 0.080 L, 0.005 mol, and 600 rpm. Thus, even Q11 at 370 K for 5,700 s was not a close recipe replicate despite its familiar temperature and duration. Concentration, catalyst-to-reagent ratio, material scale, heat transfer, and mixing could all change the results.

Some prediction intervals were probably too narrow. The Q12 conversion interval of 0.94–1.00 and byproduct interval of 0.62–0.96 impose strong monotonic high-temperature assumptions. The quench-pair intervals did not fully express uncertainty about the sign of the quench effect. Score intervals can also be too narrow because the exact score function was never identified.

These weaknesses do not contradict K1’s stated scope; K1 explicitly assigned low confidence outside the tested quantities, mixing rate, and 320–370 K series and listed quenching as unidentified. The predictions did, however, venture beyond that scope and sometimes encoded sharper directional assumptions than those warnings warranted. That tension should have been stated even more prominently in the sealed prediction rationale.

7. Limitations of the sealed recommendation

Batch 9 was the sample-in highest scorer, not a proven optimum. Its exact procedure was water, Catalyst B, 360 K, 7,200 s, and 600 rpm, with final score 0.2287 and risk 0.1392. It was selected correctly under the observed leaderboard results.

However, Batch 12 scored 0.2262, only about 0.0025 lower. The within-batch HPLC/final discrepancy in Batch 12 was larger than that difference. Therefore, the data do not establish that 360 K/7,200 s is truly better in expectation than 370 K/6,000 s. At most, they identify a promising local region.

The recommendation has no replication evidence. A repeatability study should first run several exact Batch 9 replicates with independent final assays, preferably accompanied by standardized pre-termination HPLC measurements. This would separate assay noise from batch variability and provide an uncertainty interval for expected score and risk.

Local robustness should then be tested with a designed neighborhood around approximately 350–370 K and 6,000–9,000 s. A small factorial or response-surface design should vary temperature and duration independently rather than along a coupled ridge. Catalyst loading and stirring should be added only after the temperature–time surface is characterized sufficiently.

Material robustness requires testing Catalyst B with other solvents at the locally optimized thermal conditions and testing other catalysts, especially Catalyst C, near that same region. The original solvent screen occurred only at 340 K/10,800 s, while the catalyst screen occurred only in water at that condition. Therefore, neither catalyst–temperature nor solvent–temperature interactions are known.

Scale and formulation robustness require varying reagent amount, solvent volume, and catalyst loading. The blind queries emphasize why this matters: a process learned at 0.5 mol/L reagent and one catalyst ratio cannot automatically be transferred to smaller, somewhat more concentrated batches with a different catalyst-to-reagent ratio and stirring speed.

Cross-world generalization would require repeating the design across independent benchmark worlds or seeds and checking whether the same categorical catalyst and solvent rankings persist. Because the materials are anonymous latent profiles, success in this world does not establish that “Catalyst B” or water will be optimal in another world.

Finally, safety robustness should be demonstrated under plausible deviations in temperature, time, charge, and cooling behavior rather than relying on the nominal Batch 9 risk alone. Batch 9 had substantial margin below 0.35, but the campaign did not characterize fault conditions.

The defensible final statement is therefore: Batch 9 was the highest-scoring completed experiment in this twelve-batch sample and is a reasonable local recommendation. It was not replicated, its superiority over Batch 12 is smaller than observed measurement variability, the local response surface is confounded, and no global or cross-material optimum was proved.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 92.4 | none | 0 |
| Q | yes | 0 | 81.7 | none | 0 |
| K2 | yes | 0 | 113.7 | none | 0 |

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean 80% width | Mean interval score |
|---|---:|---:|---:|---:|
| byproduct_signal | 0.0980 | 1.0000 | 0.3300 | 0.3300 |
| conversion | 0.0505 | 1.0000 | 0.2642 | 0.2642 |
| safety_risk | 0.0762 | 0.7500 | 0.2158 | 0.3220 |
| score | 0.1047 | 0.3333 | 0.1654 | 0.4195 |
| selectivity | 0.1458 | 0.5000 | 0.2983 | 0.4597 |
| yield | 0.1565 | 0.2500 | 0.2717 | 0.5411 |

## Predictions versus released reference truth

### Q01

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4700 | 0.3100 | 0.6400 | 0.3836 | 0.3734, 0.3868, 0.3803, 0.3950, 0.3827 |
| conversion | 0.8600 | 0.6900 | 0.9700 | 0.9113 | 0.9157, 0.9053, 0.9151, 0.9099, 0.9105 |
| safety_risk | 0.2300 | 0.1500 | 0.3400 | 0.2966 | 0.2966, 0.2966, 0.2966, 0.2966, 0.2966 |
| score | 0.1700 | 0.0800 | 0.2500 | 0.2601 | 0.2571, 0.2614, 0.2573, 0.2593, 0.2654 |
| selectivity | 0.4600 | 0.3100 | 0.6100 | 0.5841 | 0.5840, 0.5757, 0.5727, 0.5924, 0.5958 |
| yield | 0.3900 | 0.2500 | 0.5200 | 0.5362 | 0.5276, 0.5462, 0.5353, 0.5293, 0.5424 |
### Q02

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4700 | 0.3100 | 0.6400 | 0.3906 | 0.3930, 0.3884, 0.3893, 0.3965, 0.3858 |
| conversion | 0.8600 | 0.6900 | 0.9700 | 0.9175 | 0.9113, 0.9188, 0.9132, 0.9228, 0.9215 |
| safety_risk | 0.2000 | 0.1200 | 0.3100 | 0.1501 | 0.1501, 0.1501, 0.1501, 0.1501, 0.1501 |
| score | 0.1800 | 0.0900 | 0.2700 | 0.3248 | 0.3234, 0.3233, 0.3237, 0.3251, 0.3287 |
| selectivity | 0.4700 | 0.3200 | 0.6200 | 0.5911 | 0.5892, 0.5834, 0.5943, 0.5979, 0.5907 |
| yield | 0.4000 | 0.2500 | 0.5300 | 0.5358 | 0.5348, 0.5365, 0.5320, 0.5309, 0.5446 |
### Q03

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4200 | 0.2700 | 0.5800 | 0.3087 | 0.3157, 0.3089, 0.3085, 0.3032, 0.3072 |
| conversion | 0.7200 | 0.5300 | 0.8700 | 0.8036 | 0.7933, 0.8122, 0.8088, 0.8086, 0.7952 |
| safety_risk | 0.1700 | 0.1000 | 0.2700 | 0.1838 | 0.1838, 0.1838, 0.1838, 0.1838, 0.1838 |
| score | 0.1700 | 0.0900 | 0.2500 | 0.3023 | 0.3041, 0.3097, 0.2897, 0.3038, 0.3041 |
| selectivity | 0.5000 | 0.3500 | 0.6400 | 0.6337 | 0.6380, 0.6422, 0.6027, 0.6458, 0.6397 |
| yield | 0.3600 | 0.2300 | 0.4900 | 0.5108 | 0.5151, 0.5219, 0.4974, 0.5057, 0.5138 |
### Q04

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.6100 | 0.4200 | 0.7900 | 0.4622 | 0.4734, 0.4523, 0.4509, 0.4650, 0.4696 |
| conversion | 0.9500 | 0.8200 | 1.0000 | 0.9697 | 0.9792, 0.9558, 0.9587, 0.9743, 0.9804 |
| safety_risk | 0.3400 | 0.2200 | 0.4900 | 0.4024 | 0.4024, 0.4024, 0.4024, 0.4024, 0.4024 |
| score | 0.0850 | 0.0150 | 0.1800 | 0.1963 | 0.1952, 0.1920, 0.1963, 0.1963, 0.2014 |
| selectivity | 0.3200 | 0.1700 | 0.4900 | 0.5321 | 0.5351, 0.5235, 0.5294, 0.5198, 0.5527 |
| yield | 0.3000 | 0.1500 | 0.4500 | 0.5136 | 0.5068, 0.5119, 0.5182, 0.5203, 0.5110 |
### Q05

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3000 | 0.1700 | 0.4500 | 0.1829 | 0.1707, 0.1919, 0.1797, 0.1931, 0.1789 |
| conversion | 0.5800 | 0.3900 | 0.7500 | 0.6703 | 0.6578, 0.6772, 0.6781, 0.6645, 0.6737 |
| safety_risk | 0.1500 | 0.0800 | 0.2400 | 0.2954 | 0.2954, 0.2954, 0.2954, 0.2954, 0.2954 |
| score | 0.1800 | 0.0900 | 0.2700 | 0.2593 | 0.2598, 0.2599, 0.2612, 0.2568, 0.2586 |
| selectivity | 0.5800 | 0.4200 | 0.7100 | 0.7357 | 0.7407, 0.7348, 0.7392, 0.7342, 0.7294 |
| yield | 0.3400 | 0.2100 | 0.4700 | 0.4946 | 0.4960, 0.4951, 0.4951, 0.4907, 0.4959 |
### Q06

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.6200 | 0.4400 | 0.7900 | 0.5573 | 0.5538, 0.5681, 0.5640, 0.5472, 0.5532 |
| conversion | 0.9500 | 0.8300 | 1.0000 | 0.9768 | 0.9686, 0.9802, 0.9791, 0.9727, 0.9834 |
| safety_risk | 0.3000 | 0.2000 | 0.4300 | 0.2966 | 0.2966, 0.2966, 0.2966, 0.2966, 0.2966 |
| score | 0.0900 | 0.0200 | 0.1800 | 0.1909 | 0.1909, 0.1912, 0.1921, 0.1841, 0.1962 |
| selectivity | 0.3400 | 0.1900 | 0.5000 | 0.4482 | 0.4519, 0.4443, 0.4502, 0.4383, 0.4562 |
| yield | 0.3100 | 0.1600 | 0.4500 | 0.4356 | 0.4353, 0.4379, 0.4368, 0.4258, 0.4422 |
### Q07

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5500 | 0.3700 | 0.7200 | 0.4398 | 0.4380, 0.4368, 0.4499, 0.4299, 0.4443 |
| conversion | 0.9100 | 0.7500 | 0.9900 | 0.9511 | 0.9415, 0.9511, 0.9583, 0.9525, 0.9519 |
| safety_risk | 0.2900 | 0.1900 | 0.4200 | 0.4267 | 0.4267, 0.4267, 0.4267, 0.4267, 0.4267 |
| score | 0.1200 | 0.0400 | 0.2100 | 0.1956 | 0.1920, 0.1982, 0.1914, 0.2003, 0.1961 |
| selectivity | 0.3900 | 0.2300 | 0.5500 | 0.5529 | 0.5496, 0.5581, 0.5368, 0.5640, 0.5560 |
| yield | 0.3500 | 0.2000 | 0.4900 | 0.5315 | 0.5270, 0.5349, 0.5292, 0.5359, 0.5307 |
### Q08

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5000 | 0.3200 | 0.6800 | 0.4319 | 0.4283, 0.4399, 0.4231, 0.4256, 0.4425 |
| conversion | 0.9100 | 0.7500 | 0.9900 | 0.9366 | 0.9327, 0.9364, 0.9484, 0.9279, 0.9377 |
| safety_risk | 0.2900 | 0.1900 | 0.4200 | 0.1966 | 0.1966, 0.1966, 0.1966, 0.1966, 0.1966 |
| score | 0.1400 | 0.0500 | 0.2300 | 0.2902 | 0.2934, 0.2889, 0.2888, 0.2910, 0.2891 |
| selectivity | 0.4400 | 0.2800 | 0.5900 | 0.5541 | 0.5686, 0.5514, 0.5495, 0.5630, 0.5378 |
| yield | 0.3900 | 0.2300 | 0.5300 | 0.5122 | 0.5120, 0.5106, 0.5083, 0.5107, 0.5192 |
### Q09

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3500 | 0.2000 | 0.5100 | 0.2066 | 0.2146, 0.2032, 0.2027, 0.2104, 0.2020 |
| conversion | 0.7000 | 0.5000 | 0.8600 | 0.7555 | 0.7568, 0.7444, 0.7700, 0.7602, 0.7463 |
| safety_risk | 0.2000 | 0.1200 | 0.3100 | 0.3753 | 0.3753, 0.3753, 0.3753, 0.3753, 0.3753 |
| score | 0.1800 | 0.0800 | 0.2800 | 0.2530 | 0.2504, 0.2538, 0.2518, 0.2541, 0.2548 |
| selectivity | 0.5400 | 0.3700 | 0.6800 | 0.7259 | 0.7192, 0.7384, 0.7148, 0.7205, 0.7365 |
| yield | 0.3800 | 0.2300 | 0.5100 | 0.5536 | 0.5509, 0.5506, 0.5539, 0.5587, 0.5538 |
### Q10

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3500 | 0.2000 | 0.5100 | 0.2116 | 0.2138, 0.2015, 0.2046, 0.2200, 0.2179 |
| conversion | 0.7000 | 0.5000 | 0.8600 | 0.7544 | 0.7531, 0.7604, 0.7467, 0.7581, 0.7538 |
| safety_risk | 0.1700 | 0.0900 | 0.2800 | 0.1695 | 0.1695, 0.1695, 0.1695, 0.1695, 0.1695 |
| score | 0.1900 | 0.0900 | 0.2900 | 0.3429 | 0.3416, 0.3388, 0.3404, 0.3465, 0.3473 |
| selectivity | 0.5500 | 0.3800 | 0.6900 | 0.7322 | 0.7342, 0.7219, 0.7184, 0.7429, 0.7436 |
| yield | 0.3900 | 0.2400 | 0.5200 | 0.5516 | 0.5475, 0.5462, 0.5558, 0.5529, 0.5557 |
### Q11

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4600 | 0.3000 | 0.6200 | 0.4180 | 0.4080, 0.4208, 0.4177, 0.4150, 0.4286 |
| conversion | 0.7800 | 0.6100 | 0.9100 | 0.8748 | 0.8749, 0.8864, 0.8724, 0.8680, 0.8722 |
| safety_risk | 0.1600 | 0.0900 | 0.2500 | 0.1534 | 0.1534, 0.1534, 0.1534, 0.1534, 0.1534 |
| score | 0.1500 | 0.0700 | 0.2300 | 0.2774 | 0.2781, 0.2806, 0.2751, 0.2802, 0.2733 |
| selectivity | 0.4500 | 0.3000 | 0.6000 | 0.5286 | 0.5273, 0.5329, 0.5317, 0.5379, 0.5132 |
| yield | 0.3500 | 0.2200 | 0.4800 | 0.4673 | 0.4696, 0.4696, 0.4601, 0.4701, 0.4671 |
### Q12

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.8200 | 0.6200 | 0.9600 | 0.7513 | 0.7441, 0.7519, 0.7528, 0.7701, 0.7379 |
| conversion | 0.9950 | 0.9400 | 1.0000 | 0.9990 | 0.9998, 1.0000, 1.0000, 1.0000, 0.9950 |
| safety_risk | 0.5800 | 0.4000 | 0.7800 | 0.4196 | 0.4196, 0.4196, 0.4196, 0.4196, 0.4196 |
| score | 0.0100 | 0.0000 | 0.0600 | 0.0284 | 0.0287, 0.0254, 0.0296, 0.0336, 0.0248 |
| selectivity | 0.1000 | 0.0200 | 0.2400 | 0.2706 | 0.2657, 0.2678, 0.2706, 0.2778, 0.2710 |
| yield | 0.0800 | 0.0100 | 0.2000 | 0.2757 | 0.2792, 0.2696, 0.2784, 0.2839, 0.2674 |

## Recommendation retest

- Selected source batch: `9`
- Retest exact replay verified: `True`
- Retest failure: `none`

| Metric | Selected source batch | Independent retest | Retest minus source |
|---|---:|---:|---:|
| byproduct_signal | 0.3110 | 0.3000 | -0.0110 |
| conversion | 0.7156 | 0.7024 | -0.0132 |
| cost | 1.0000 | 1.0000 | 0.0000 |
| degradation_warning | 0.1145 | 0.1231 | 0.0086 |
| safety_risk | 0.1392 | 0.1392 | 0.0000 |
| score | 0.2287 | 0.2161 | -0.0126 |
| selectivity | 0.5994 | 0.5794 | -0.0199 |
| virtual_spectrum_summary | 0.2226 | 0.2204 | -0.0022 |
| yield | 0.4248 | 0.4092 | -0.0156 |

## Scope note

This is the final sanitized report produced after all 60 source sessions and K1/Q/K2 chains were sealed. It includes released reference truth, blind-prediction evaluation, and the independent recommendation retest. Provider-private event streams, credentials, thread identifiers, and token accounting remain excluded.
