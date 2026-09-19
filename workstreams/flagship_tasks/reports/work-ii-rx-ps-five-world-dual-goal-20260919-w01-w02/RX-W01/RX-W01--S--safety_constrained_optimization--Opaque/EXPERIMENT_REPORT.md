# RX-W01--S--safety_constrained_optimization--Opaque

## Run summary

- World: `RX-W01`
- Locus: `S`
- Goal: `safety_constrained_optimization`
- Arm: `Opaque`
- Status: `completed`
- Source status: `completed`
- Experimental sessions: `12/12`
- Operations: `96`
- Exact replay: `{'checked_steps': 96, 'max_abs_error': 0.0, 'mismatches': [], 'verified': True}`
- Posttest chain sealed: `True`

### Recovery status

No recovery override was required for this task.

## Sealed recommendation

- Selected batch: `11`
- Rationale: Batch 11 achieved the highest observed public safe score (0.2454) while remaining comfortably below the 0.35 safety limit (risk 0.1617), and its Catalyst B/ethanol, 355 K, 8000 s procedure was independently repeated in batch 12.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S0 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 340 K × 3600 s @ 500 rpm | yes | 0.1452 | 0.4173 | 0.3608 | 0.2158 | 0.0038 | 0.0930 | 0.0566 |
| 2 | S1 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 360 K × 7200 s @ 700 rpm | yes | 0.4750 | 0.5581 | 0.8514 | 0.3916 | 0.1427 | 0.1623 | 0.2416 |
| 3 | S2 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 380 K × 3600 s @ 700 rpm | yes | 0.4468 | 0.6252 | 0.7306 | 0.2744 | 0.0608 | 0.1724 | 0.2305 |
| 4 | S3 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 360 K × 7200 s @ 700 rpm | yes | 0.4369 | 0.4895 | 0.9148 | 0.4860 | 0.2268 | 0.1951 | 0.2008 |
| 5 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K × 10000 s @ 700 rpm | yes | 0.4828 | 0.5137 | 0.9423 | 0.4892 | 0.3158 | 0.1892 | 0.2306 |
| 6 | S2 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 350 K × 7200 s @ 700 rpm | yes | 0.4423 | 0.5441 | 0.7993 | 0.3571 | 0.1049 | 0.1731 | 0.2150 |
| 7 | S1 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 350 K × 7200 s @ 700 rpm | yes | 0.3334 | 0.4609 | 0.7184 | 0.4036 | 0.0511 | 0.1437 | 0.1558 |
| 8 | S1 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 345 K × 10000 s @ 700 rpm | yes | 0.4490 | 0.5138 | 0.8772 | 0.4326 | 0.1781 | 0.1605 | 0.2236 |
| 9 | S2 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 370 K × 6000 s @ 700 rpm | yes | 0.4785 | 0.5678 | 0.8473 | 0.3662 | 0.1217 | 0.1795 | 0.2373 |
| 10 | S2 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 365 K × 8000 s @ 700 rpm | yes | 0.4762 | 0.5203 | 0.9101 | 0.4587 | 0.1432 | 0.1818 | 0.2297 |
| 11 | S1 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 355 K × 8000 s @ 700 rpm | yes | 0.4859 | 0.5496 | 0.8647 | 0.3950 | 0.1483 | 0.1617 | 0.2454 |
| 12 | S1 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 355 K × 8000 s @ 700 rpm | yes | 0.4653 | 0.5347 | 0.8581 | 0.4017 | 0.1503 | 0.1617 | 0.2328 |

## Complete experimental actions and observations

### Batch 1

Lifecycle index: `1`; end step: `8`.

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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 340
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
  "end_step": 8,
  "lifecycle_index": 1,
  "metrics": {
    "byproduct_signal": 0.21583674848079681,
    "conversion": 0.36080676317214966,
    "cost": 1.0,
    "degradation_warning": 0.003755341749638319,
    "safety_risk": 0.09301621466875076,
    "score": 0.056611623615026474,
    "selectivity": 0.4172804355621338,
    "virtual_spectrum_summary": 0.12040011584758759,
    "yield": 0.14517034590244293
  },
  "ordinal": 1
}
```

### Batch 2

Lifecycle index: `2`; end step: `16`.

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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 700,
      "target_temperature_K": 360
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
  "end_step": 16,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.39160963892936707,
    "conversion": 0.8514305353164673,
    "cost": 1.0,
    "degradation_warning": 0.14267845451831818,
    "safety_risk": 0.1623154729604721,
    "score": 0.2416328638792038,
    "selectivity": 0.558123767375946,
    "virtual_spectrum_summary": 0.2795906066894531,
    "yield": 0.47500208020210266
  },
  "ordinal": 2
}
```

### Batch 3

Lifecycle index: `3`; end step: `24`.

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
      "stirring_speed_rpm": 700,
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
  "end_step": 24,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.2743595838546753,
    "conversion": 0.7305511236190796,
    "cost": 1.0,
    "degradation_warning": 0.06079190596938133,
    "safety_risk": 0.1724267601966858,
    "score": 0.2304832637310028,
    "selectivity": 0.6252168416976929,
    "virtual_spectrum_summary": 0.1782541275024414,
    "yield": 0.44678995013237
  },
  "ordinal": 3
}
```

### Batch 4

Lifecycle index: `4`; end step: `32`.

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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 700,
      "target_temperature_K": 360
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
  "end_step": 32,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.4859863519668579,
    "conversion": 0.9148163199424744,
    "cost": 1.0,
    "degradation_warning": 0.22680312395095825,
    "safety_risk": 0.19511958956718445,
    "score": 0.20082005858421326,
    "selectivity": 0.4894924759864807,
    "virtual_spectrum_summary": 0.36935392022132874,
    "yield": 0.4369227886199951
  },
  "ordinal": 4
}
```

### Batch 5

Lifecycle index: `5`; end step: `40`.

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
      "duration_s": 10000,
      "operation": "heat",
      "stirring_speed_rpm": 700,
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
  "end_step": 40,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.48922404646873474,
    "conversion": 0.9423273801803589,
    "cost": 1.0,
    "degradation_warning": 0.3158077895641327,
    "safety_risk": 0.1891903430223465,
    "score": 0.2306375950574875,
    "selectivity": 0.513745903968811,
    "virtual_spectrum_summary": 0.41118672490119934,
    "yield": 0.48276010155677795
  },
  "ordinal": 5
}
```

### Batch 6

Lifecycle index: `6`; end step: `48`.

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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 700,
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
  "end_step": 48,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.3571164309978485,
    "conversion": 0.7992504239082336,
    "cost": 1.0,
    "degradation_warning": 0.10485626757144928,
    "safety_risk": 0.17309731245040894,
    "score": 0.21498845517635345,
    "selectivity": 0.5441341996192932,
    "virtual_spectrum_summary": 0.24359935522079468,
    "yield": 0.44230911135673523
  },
  "ordinal": 6
}
```

### Batch 7

Lifecycle index: `7`; end step: `56`.

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
      "catalyst": 2,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 700,
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
  "end_step": 56,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.4036218523979187,
    "conversion": 0.7184256911277771,
    "cost": 1.0,
    "degradation_warning": 0.05109858140349388,
    "safety_risk": 0.1436530202627182,
    "score": 0.15581199526786804,
    "selectivity": 0.4609484374523163,
    "virtual_spectrum_summary": 0.2449863851070404,
    "yield": 0.3334404528141022
  },
  "ordinal": 7
}
```

### Batch 8

Lifecycle index: `8`; end step: `64`.

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
      "duration_s": 10000,
      "operation": "heat",
      "stirring_speed_rpm": 700,
      "target_temperature_K": 345
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
  "end_step": 64,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.4325910806655884,
    "conversion": 0.8772395849227905,
    "cost": 1.0,
    "degradation_warning": 0.17814746499061584,
    "safety_risk": 0.1605016589164734,
    "score": 0.22356675565242767,
    "selectivity": 0.513812243938446,
    "virtual_spectrum_summary": 0.3180914521217346,
    "yield": 0.44903871417045593
  },
  "ordinal": 8
}
```

### Batch 9

Lifecycle index: `9`; end step: `72`.

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
      "duration_s": 6000,
      "operation": "heat",
      "stirring_speed_rpm": 700,
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
  "end_step": 72,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.36619365215301514,
    "conversion": 0.8473384380340576,
    "cost": 1.0,
    "degradation_warning": 0.12168056517839432,
    "safety_risk": 0.1794768124818802,
    "score": 0.2373191863298416,
    "selectivity": 0.5677832961082458,
    "virtual_spectrum_summary": 0.25616276264190674,
    "yield": 0.47851020097732544
  },
  "ordinal": 9
}
```

### Batch 10

Lifecycle index: `10`; end step: `80`.

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
      "duration_s": 8000,
      "operation": "heat",
      "stirring_speed_rpm": 700,
      "target_temperature_K": 365
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
  "end_step": 80,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.4587240517139435,
    "conversion": 0.9100666642189026,
    "cost": 1.0,
    "degradation_warning": 0.1432476043701172,
    "safety_risk": 0.18181632459163666,
    "score": 0.2297247350215912,
    "selectivity": 0.5202558636665344,
    "virtual_spectrum_summary": 0.3167596459388733,
    "yield": 0.4761786460876465
  },
  "ordinal": 10
}
```

### Batch 11

Lifecycle index: `11`; end step: `88`.

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
      "duration_s": 8000,
      "operation": "heat",
      "stirring_speed_rpm": 700,
      "target_temperature_K": 355
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
  "end_step": 88,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.39497628808021545,
    "conversion": 0.8646776676177979,
    "cost": 1.0,
    "degradation_warning": 0.1483234167098999,
    "safety_risk": 0.16173361241817474,
    "score": 0.24543975293636322,
    "selectivity": 0.5496124625205994,
    "virtual_spectrum_summary": 0.2839824855327606,
    "yield": 0.4858724772930145
  },
  "ordinal": 11
}
```

### Batch 12

Lifecycle index: `12`; end step: `96`.

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
      "duration_s": 8000,
      "operation": "heat",
      "stirring_speed_rpm": 700,
      "target_temperature_K": 355
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
  "end_step": 96,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.4017002284526825,
    "conversion": 0.8581019043922424,
    "cost": 1.0,
    "degradation_warning": 0.15033812820911407,
    "safety_risk": 0.16173361241817474,
    "score": 0.23282776772975922,
    "selectivity": 0.5346839427947998,
    "virtual_spectrum_summary": 0.2885873019695282,
    "yield": 0.4653168022632599
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

1. Scope and evidence basis

This report describes only the synthetic reaction-and-thermal world explored in the completed 12-batch campaign. The limiting reagent, catalysts, and reaction products are anonymous benchmark entities. Although some solvents have real chemical names, their effects in this world are calibrated categorical effects; I therefore do not interpret Catalyst B or ethanol as implying any real synthesis.

Every batch used 0.040 mol reagent, 0.080 L solvent, and 0.005 mol catalyst. Batch 1 was stirred at 500 rpm; batches 2–12 used 700 rpm. Consequently, the campaign primarily identifies categorical catalyst/solvent effects and temperature–time effects at one concentration, catalyst loading, and mixing regime. It does not establish general kinetic constants.

The HPLC measurement was made after heating but before quenching. The final assay was made after quenching and termination. Numerical comparisons below use final-assay estimates unless explicitly labeled HPLC. The public estimates are noisy synthetic measurements, not exact hidden-state compositions.

2. Empirical picture of how the world operates

The observations are consistent with a thermally activated catalytic network in which reagent is consumed through competing productive and unproductive channels. A minimal plausible scheme is:

R --kP(catalyst, solvent, T)--> P
R --kB(catalyst, solvent, T)--> B
P --kD(catalyst, solvent, T)--> D

Here R is the public reactant, P the desired target, B a primary byproduct pool, and D a degradation pool. A useful qualitative model would be:

dR/dt = -(kP + kB)R
dP/dt = kP R - kD P
dB/dt = kB R + alpha·kD P
dD/dt = (1-alpha)·kD P

with Arrhenius-like rates

ki = Ai(catalyst, solvent)·f(catalyst loading, concentration, mixing)·exp[-Ei/(RT)].

This model is not uniquely proved, but it explains the main observations: heating raises conversion; catalyst and solvent change both activity and branching; excessive thermal exposure raises byproduct and degradation signals; and the best score occurs at an intermediate exposure rather than at maximum conversion.

Yield was broadly consistent with conversion multiplied by selectivity, allowing for assay noise and the fact that the public channels may not be algebraically identical. For example, batch 2 had conversion 0.8514, selectivity 0.5581, and yield 0.4750; 0.8514×0.5581 is approximately 0.475. Batch 11 similarly had 0.8647 conversion and 0.5496 selectivity, whose product is approximately 0.475, close to its measured yield of 0.4859. This supports the interpretation that conversion describes disappearance of R while selectivity describes the productive fraction of converted material.

The byproduct and degradation channels appear related but distinct. A batch can have appreciable byproduct signal while degradation remains small, as in batch 1 (byproduct 0.2158, degradation 0.0038), whereas long or severe exposure produces much larger degradation, as in batch 5 (degradation 0.3158). Thus the byproduct signal is unlikely to be only degraded product.

3. Temperature and time

Thermal exposure was the main continuous driver of conversion. The vessel did not instantaneously reach the requested setpoint. For example, a 360 K, 7200 s heat in batch 2 changed the public temperature by 58.44 K, consistent with an endpoint near 358.44 K from an approximately 300 K start. Batch 3, requested at 380 K for 3600 s, changed temperature by 75.19 K. I therefore interpret each treatment through its full transient thermal history, not merely target temperature multiplied by time.

Batch 1, at 340 K for 3600 s with Catalyst A/water, was under-reacted: conversion 0.3608, yield 0.1452, selectivity 0.4173, and score 0.0566. This result caused me to increase thermal severity and explore other catalyst/solvent categories.

Higher exposure strongly increased conversion, but beyond a moderate region it increasingly favored byproduct formation or secondary degradation. Batch 5, Catalyst B/acetonitrile at 350 K for 10000 s, reached the highest measured conversion, 0.9423, but had selectivity only 0.5137, byproduct 0.4892, degradation 0.3158, and score 0.2306. Batch 10, Catalyst C/acetonitrile at 365 K for 8000 s, likewise reached conversion 0.9101 but gave selectivity 0.5203, byproduct 0.4587, and score 0.2297. These results changed my working objective from “maximize conversion” to “stop near the productive-selectivity optimum.”

For Catalyst C/acetonitrile, the clearest exposure sequence was:

• Batch 6, 350 K for 7200 s: conversion 0.7993, yield 0.4423, selectivity 0.5441, byproduct 0.3571, degradation 0.1049, score 0.2150.
• Batch 9, 370 K for 6000 s: conversion 0.8473, yield 0.4785, selectivity 0.5678, byproduct 0.3662, degradation 0.1217, score 0.2373.
• Batch 10, 365 K for 8000 s: conversion 0.9101, yield 0.4762, selectivity 0.5203, byproduct 0.4587, degradation 0.1432, score 0.2297.

Batch 9 demonstrates a favorable intermediate regime. Extending exposure from that region toward batch 10 increased conversion but did not improve yield and reduced selectivity. This is consistent with exhaustion of the easy productive pathway, increasing competition from R→B, or loss of accumulated P through P→D.

4. Catalyst and solvent effects and their coupling

Catalyst and solvent are not simple independent rate multipliers. Their effects include activity, selectivity, and safety coupling.

Catalyst C/acetonitrile was relatively selective under sufficiently hot, moderate-duration operation. Batch 3, at 380 K for 3600 s, had the highest measured final-assay selectivity, 0.6252, with conversion 0.7306, yield 0.4468, low degradation of 0.0608, and score 0.2305. This led me initially to favor Catalyst C. However, later experiments showed that its advantage depended strongly on solvent and exposure.

The strongest directly controlled solvent contrast was batches 6 and 7. Both used Catalyst C, 350 K, 7200 s, 0.040 mol reagent, 0.005 mol catalyst, 0.080 L solvent, and 700 rpm. Changing acetonitrile in batch 6 to ethanol in batch 7 changed:

• conversion: 0.7993 to 0.7184
• selectivity: 0.5441 to 0.4609
• yield: 0.4423 to 0.3334
• byproduct: 0.3571 to 0.4036
• score: 0.2150 to 0.1558

Thus acetonitrile is clearly the better partner for Catalyst C in the tested regime. The simultaneous changes in conversion and selectivity support a catalyst–solvent interaction rather than a solvent effect on rate alone.

Catalyst B/ethanol produced the best safe-score region. Batch 2 at 360 K for 7200 s gave conversion 0.8514, yield 0.4750, selectivity 0.5581, degradation 0.1427, safety risk 0.1623, and score 0.2416. Batch 11 at 355 K for 8000 s improved the observed score to 0.2454, with conversion 0.8647, yield 0.4859, selectivity 0.5496, byproduct 0.3950, degradation 0.1483, and risk 0.1617. The nearly equal risks but slightly different conversion/selectivity balance indicate a broad local optimum rather than an extremely sharp setpoint.

Catalyst B/acetonitrile did not clearly outperform Catalyst B/ethanol. Batch 5 gave high conversion but severe degradation and a score of 0.2306. Because its duration and temperature differed from the ethanol experiments, the solvent effect for Catalyst B is not cleanly isolated. Nevertheless, the best observed Catalyst B results used ethanol.

Catalyst D/toluene was tested only once and was comparatively unselective. Batch 4 at 360 K for 7200 s gave conversion 0.9148 but selectivity 0.4895, byproduct 0.4860, degradation 0.2268, and score 0.2008. This is another example in which high conversion reflected substantial undesired chemistry.

Catalyst A/water was also tested only once, in the low-severity batch 1. Its low performance is confounded with the mild thermal treatment and lower stirring speed, so I cannot conclude that Catalyst A or water is intrinsically poor.

5. Safety behavior

All completed batches remained below the declared safety limit of 0.35. Final post-quench risks ranged from 0.0930 in batch 1 to 0.1951 in batch 4. The highest-performing batch 11 had risk 0.1617.

Risk had at least two components. First, material addition generated a solvent-dependent baseline. The approximate pre-heating risk inferred from the heat-step readouts was lowest for the water formulation in batch 1, higher for ethanol, higher again for acetonitrile, and highest for the tested toluene batch. Second, heating added a temperature- and duration-dependent increment. For example, the heat step added about 0.0764 risk in batch 2, 0.0836 in batch 3, and 0.0823 in batch 5. Quenching then reduced the displayed risk: batch 2 fell from 0.1719 around the heated/HPLC state to final risk 0.1623; batch 3 fell from 0.1970 to 0.1724.

A qualitative risk model consistent with the data is:

risk_heated ≈ r_material(solvent, reagent concentration) + integral g(T(t), duration, solvent) dt,
risk_after_quench ≈ risk_heated - q(T_before_quench, quench effectiveness).

I cannot determine whether the internal safety rule uses peak risk, instantaneous state risk, accumulated hazard, or a combination. Operationally, both peak and final displayed risks were comfortably compliant in this campaign.

6. Score behavior

The public score favored productive yield and selectivity while penalizing unsafe or poor-quality operation, but I did not identify an exact formula. High conversion alone was insufficient: batch 5 had conversion 0.9423 but scored 0.2306, below batch 11 at conversion 0.8647 and score 0.2454. Similarly, batch 4 converted 0.9148 but scored only 0.2008 because selectivity, byproduct, degradation, and risk were worse.

The best observed scores were:

• Batch 11: 0.2454, risk 0.1617.
• Batch 2: 0.2416, risk 0.1623.
• Batch 9: 0.2373, risk 0.1795.
• Batch 12: 0.2328, risk 0.1617.

This supports an operating principle of moderate-to-high conversion with preserved selectivity, rather than complete reagent disappearance.

7. Repeatability and measurement uncertainty

Batches 11 and 12 were an exact procedural repeat: Catalyst B, ethanol, 355 K for 8000 s, 700 rpm, and identical charges. Their reported final risks were identical at 0.1617, indicating deterministic or highly stable thermal/safety behavior. Their chemical estimates differed:

• Batch 11: conversion 0.8647, yield 0.4859, selectivity 0.5496, byproduct 0.3950, degradation 0.1483, score 0.2454.
• Batch 12: conversion 0.8581, yield 0.4653, selectivity 0.5347, byproduct 0.4017, degradation 0.1503, score 0.2328.

The score spread of 0.0126 is important. It shows that the single best score should not be treated as an exact deterministic property of the recipe. The variation could reflect assay noise, a process-uncertainty proxy, or both. Batch 11 remains the highest observed completed batch, while the pair supports a more conservative expectation in the approximate 0.23–0.25 range.

Pre-quench HPLC and post-quench final-assay estimates also differed. In batch 11, HPLC reported conversion 0.8613, yield 0.4689, selectivity 0.5366, and byproduct 0.3839, compared with final-assay values of 0.8647, 0.4859, 0.5496, and 0.3950. Such differences are generally compatible with separate instrument noise and minor state changes around quenching; they do not demonstrate continued reaction after quench.

8. How the interpretation evolved

Batch 1 established that mild heating with Catalyst A/water was insufficient. Batch 2 showed that a different catalyst/solvent pair plus stronger thermal exposure could raise conversion and yield dramatically without approaching the safety limit. Batch 3 produced unusually high selectivity and motivated focused study of Catalyst C/acetonitrile. Batches 5, 6, 9, and 10 then demonstrated a nonmonotonic exposure optimum: increasing conversion eventually increased byproduct/degradation and reduced selectivity. The controlled batch 6 versus batch 7 comparison revealed a strong Catalyst C–solvent interaction. Batches 8 and 11 refined the Catalyst B/ethanol region, with batch 11 becoming the best observed result. Batch 12 tested reproducibility and made me reduce confidence in interpreting small score differences as deterministic improvements.

9. Limits of identification and competing explanations

Several mechanistic features remain unidentifiable:

• Catalyst and solvent identities are categorical benchmark labels; molecular elementary steps cannot be assigned.
• Catalyst loading, reagent concentration, and solvent volume were fixed, so reaction orders and dilution effects cannot be estimated.
• Nearly all experiments used one stirring rate. Mass-transfer limitation cannot be separated from intrinsic kinetics.
• Temperature and time were changed together in most comparisons. Activation energies and independent time constants cannot be fitted reliably.
• Only endpoint measurements were collected. Parallel byproduct formation cannot be distinguished decisively from consecutive product degradation.
• Catalyst/solvent combinations were incompletely crossed. Some apparent catalyst effects may actually be solvent effects or interactions.
• Catalyst A/water and Catalyst D/toluene each have only one observation, preventing robust ranking.
• The byproduct and degradation observables are signals, not demonstrated mole fractions; they need not close a strict mass balance.
• Quenching occurred between HPLC and final assay, so instrument differences are partly confounded with sampling time and state.

A reasonable competing model is a purely parallel network R→P and R→B in which the apparent degradation warning is an independent thermal damage indicator rather than actual loss of P. Another possibility is catalyst deactivation: longer heating could lower the productive rate while leaving a background byproduct pathway active, producing the same decline in selectivity without P→D. Product inhibition or changing solvent environment as conversion rises could also explain the nonmonotonic optimum. The present endpoint data cannot discriminate among these alternatives.

10. Best current operating interpretation

Within the studied domain, the world appears to reward a catalyst–solvent-specific intermediate thermal dose. The most defensible local regime is Catalyst B with ethanol, 0.040 mol reagent, 0.005 mol catalyst, 0.080 L solvent, 700 rpm, and heating near 355–360 K for roughly 7200–8000 s, followed by prompt quenching. This is an interpolation around batches 2, 11, and 12, not a claim outside the tested range. Batch 11 is the highest observed realization, while batch 12 quantifies meaningful run-to-run or measurement variability.

The principal mechanistic conclusion is therefore not that maximum temperature or maximum conversion is optimal. It is that productive and undesired pathways have different catalyst–solvent and thermal sensitivities; conversion initially generates target product, but additional exposure increasingly generates byproduct or degradation. Safe, high-scoring operation requires stopping near the maximum of productive yield times quality/selectivity while retaining a substantial safety margin.

## Q — Blind predictions

### Overall rationale

Predictions are based on the campaign's inferred competing-pathway model: catalyst and temperature accelerate reagent disappearance, while excessive temperature or residence time increasingly favors byproduct formation and secondary degradation. Yield was treated as approximately conversion multiplied by selectivity, subject to final-assay noise. The closest direct evidence is batch 5, which used Catalyst B with acetonitrile at 350 K for 10000 s and gave conversion 0.9423, selectivity 0.5137, yield 0.4828, byproduct 0.4892, risk 0.1892 after quenching, and score 0.2306. However, the new batches use much smaller absolute charges, different catalyst-to-reagent ratios, 400 rpm stirring, mostly omit quenching, and include temperatures up to 465 K. Prediction intervals are therefore deliberately broad, especially for high-temperature selectivity, byproduct signal, safety risk, and score. Q09 and Q10 are assigned nearly identical chemical outcomes, with Q10 receiving a lower safety-risk estimate because quenching reduced the displayed heated-state risk in the completed campaign.

### Q01

The low catalyst-to-reagent ratio and short 1800 s residence should limit conversion despite the 410 K target. The short exposure should preserve relatively good branching selectivity, so this is predicted to be under-converted rather than severely degraded.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2000 | 0.1000 | 0.3400 |
| conversion | 0.5000 | 0.3100 | 0.7000 |
| safety_risk | 0.1100 | 0.0600 | 0.1800 |
| score | 0.1500 | 0.0700 | 0.2400 |
| selectivity | 0.5800 | 0.4400 | 0.7000 |
| yield | 0.2900 | 0.1600 | 0.4300 |

### Q02

Fourteen thousand four hundred seconds at 410 K should compensate for the low catalyst loading and drive conversion nearly to completion. Extrapolation from the long-exposure campaign batches suggests substantial loss of selectivity and growth of the byproduct/degradation channels.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7000 | 0.5300 | 0.8600 |
| conversion | 0.9900 | 0.9400 | 1.0000 |
| safety_risk | 0.2100 | 0.1300 | 0.3100 |
| score | 0.0700 | 0.0100 | 0.1600 |
| selectivity | 0.3000 | 0.1600 | 0.4500 |
| yield | 0.3000 | 0.1600 | 0.4500 |

### Q03

The high catalyst loading should make the short 410 K treatment substantially more effective than Q01. Because residence time remains short, this condition is expected to approach high conversion while retaining moderate selectivity, making it one of the stronger predicted conditions.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4200 | 0.2700 | 0.5800 |
| conversion | 0.9400 | 0.8200 | 0.9900 |
| safety_risk | 0.1100 | 0.0600 | 0.1800 |
| score | 0.2500 | 0.1500 | 0.3400 |
| selectivity | 0.5500 | 0.4200 | 0.6700 |
| yield | 0.5200 | 0.3900 | 0.6400 |

### Q04

High catalyst loading and the longest 410 K residence should exhaust the reagent early, leaving a long interval in which unproductive or secondary degradation chemistry can dominate. Conversion is therefore predicted to saturate while selectivity and safe score decline sharply.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8000 | 0.6400 | 0.9400 |
| conversion | 1.0000 | 0.9800 | 1.0000 |
| safety_risk | 0.2100 | 0.1300 | 0.3100 |
| score | 0.0300 | 0.0000 | 0.1000 |
| selectivity | 0.2000 | 0.0700 | 0.3600 |
| yield | 0.2000 | 0.0700 | 0.3600 |

### Q05

At 350 K, the low catalyst loading should leave the batch only partly converted after 7200 s. Mild temperature should preserve selectivity and keep safety risk low, but limited conversion constrains yield and score.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1900 | 0.0800 | 0.3300 |
| conversion | 0.4800 | 0.2800 | 0.6800 |
| safety_risk | 0.0700 | 0.0300 | 0.1300 |
| score | 0.1600 | 0.0700 | 0.2500 |
| selectivity | 0.5900 | 0.4500 | 0.7100 |
| yield | 0.2800 | 0.1400 | 0.4200 |

### Q06

The 465 K target is far outside the campaign's directly studied temperature range. Even with low catalyst loading, 7200 s is expected to produce essentially complete conversion but extensive undesired chemistry. The risk interval crosses the 0.35 limit because this is a large thermal extrapolation without a quench.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8800 | 0.7000 | 0.9900 |
| conversion | 1.0000 | 0.9700 | 1.0000 |
| safety_risk | 0.2700 | 0.1700 | 0.3900 |
| score | 0.0100 | 0.0000 | 0.0600 |
| selectivity | 0.1200 | 0.0200 | 0.2900 |
| yield | 0.1200 | 0.0200 | 0.2900 |

### Q07

High catalyst loading should bring the 350 K batch close to completion within 7200 s. This resembles the campaign's productive moderate-temperature regime, although the catalyst concentration and scale are extrapolated. Moderate selectivity and low thermal risk are expected.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4500 | 0.3000 | 0.6100 |
| conversion | 0.9400 | 0.8300 | 0.9900 |
| safety_risk | 0.0700 | 0.0300 | 0.1300 |
| score | 0.2400 | 0.1500 | 0.3300 |
| selectivity | 0.5200 | 0.4000 | 0.6400 |
| yield | 0.4900 | 0.3700 | 0.6100 |

### Q08

This combines the highest catalyst loading with a long 465 K exposure. It is predicted to be the most over-processed batch: conversion saturates, while target material is largely displaced by byproduct or degradation. Thermal risk is highly uncertain and may violate the declared limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9500 | 0.8000 | 1.0000 |
| conversion | 1.0000 | 0.9900 | 1.0000 |
| safety_risk | 0.2700 | 0.1700 | 0.3900 |
| score | 0.0020 | 0.0000 | 0.0300 |
| selectivity | 0.0500 | 0.0000 | 0.1900 |
| yield | 0.0500 | 0.0000 | 0.1900 |

### Q09

The central catalyst loading at 410 K for 7200 s should give nearly complete conversion. Relative to the campaign optimum, the higher temperature and prolonged post-conversion exposure are expected to increase byproduct formation and reduce selectivity. No quench is present, so the final displayed risk should remain near the heated-state value.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6500 | 0.4800 | 0.8100 |
| conversion | 0.9900 | 0.9400 | 1.0000 |
| safety_risk | 0.1800 | 0.1100 | 0.2800 |
| score | 0.1000 | 0.0300 | 0.1900 |
| selectivity | 0.3500 | 0.2100 | 0.5000 |
| yield | 0.3500 | 0.2100 | 0.5000 |

### Q10

The chemical trajectory should closely match Q09 because quenching follows the entire heating period. The quench is predicted mainly to lower the final safety-risk readout and arrest further reaction during closeout; small chemical differences are included within the prediction intervals.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6400 | 0.4700 | 0.8000 |
| conversion | 0.9900 | 0.9400 | 1.0000 |
| safety_risk | 0.1400 | 0.0800 | 0.2300 |
| score | 0.1100 | 0.0300 | 0.2100 |
| selectivity | 0.3600 | 0.2200 | 0.5100 |
| yield | 0.3600 | 0.2200 | 0.5100 |

### Q11

The long 350 K residence should drive the central catalyst loading close to full conversion, but more slowly than the 410 K cases. Lower temperature should retain more selectivity than Q09, although the 14400 s duration still allows appreciable byproduct formation.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5500 | 0.3800 | 0.7100 |
| conversion | 0.9700 | 0.8800 | 1.0000 |
| safety_risk | 0.1300 | 0.0700 | 0.2100 |
| score | 0.1600 | 0.0700 | 0.2600 |
| selectivity | 0.4300 | 0.2900 | 0.5700 |
| yield | 0.4200 | 0.2800 | 0.5500 |

### Q12

At 465 K, even 1800 s may be sufficient for near-complete conversion at the central catalyst loading. The short duration should be less damaging than Q06 or Q08, but the temperature is a major extrapolation and may cause rapid unproductive branching or degradation, producing wide intervals.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5800 | 0.3900 | 0.7600 |
| conversion | 0.9900 | 0.9100 | 1.0000 |
| safety_risk | 0.1800 | 0.1000 | 0.2900 |
| score | 0.1400 | 0.0500 | 0.2500 |
| selectivity | 0.4200 | 0.2700 | 0.5800 |
| yield | 0.4200 | 0.2600 | 0.5700 |

## K2 — Retrospective analysis

1. Initial claims: supported, contradicted, or untested

The initial material packet contained almost no substantive mechanistic or kinetic claims. It explicitly said that no task-specific nominal property dossier was supplied, that the catalysts were anonymous benchmark formulations, and that the named solvents had categorical benchmark effects rather than real-world predictive chemistry. Therefore, there was no initial proposed rate law, catalyst ranking, solvent ranking, activation energy, or reaction network to confirm or refute.

Several contractual claims were consistent with the observations:

• The system behaved as a categorical benchmark rather than as something that could safely be inferred from familiar solvent chemistry. For example, Catalyst C performed much better with acetonitrile in batch 6 than with ethanol in batch 7 under otherwise matched conditions. This supports treating catalyst–solvent combinations empirically, but it does not independently validate the metadata claim about how the world was constructed.
• The declared final-assay uncertainty was qualitatively supported by the exact procedural repeat in batches 11 and 12. Their safety risks were both 0.1617, but their final yields were 0.4859 and 0.4653 and their scores were 0.2454 and 0.2328. That variation is compatible with assay noise or process-proxy uncertainty.
• The 0.35 safety threshold remained unviolated in all completed experiments. This is only an absence of contrary observations; it does not validate the risk model or prove that all explored or predicted conditions are safe.

Important initial claims remained untested. I did not test whether the solvent effects were independent of scale, concentration, catalyst loading, or stirring. I also did not test the stated interpretation that the real solvent identities should not be used predictively; I respected that boundary rather than attempting to validate it.

No initial mechanistic claim was directly contradicted because none was supplied. This distinction matters: the campaign generated a mechanism hypothesis from observations rather than selecting among mechanisms proposed in the initial packet.

There were, however, cases in my own evolving beliefs where contrary evidence appeared before I fully revised the design. After batch 3 gave the highest observed selectivity, 0.6252, I leaned toward Catalyst C/acetonitrile. Batch 6 then gave a lower score of 0.2150, and batch 7 showed that Catalyst C/ethanol was particularly poor, with score 0.1558. I did revise toward a catalyst–solvent interaction model, but I continued allocating several batches to Catalyst C/acetonitrile. Similarly, batches 5 and 10 showed that very high conversion did not maximize score; the later design corrected for this, but the early campaign had implicitly treated increased conversion as more beneficial than the data ultimately supported.

2. Experiments that formed or changed the interpretation

Batch 1 formed the first operational judgment. Catalyst A/water at 340 K for 3600 s produced conversion 0.3608, yield 0.1452, and score 0.0566. It showed that the initial mild condition was under-reacted. The choice itself was not data-driven; it was a baseline guess using one catalyst, one solvent, and a moderate thermal treatment.

Batch 2 caused the largest early update. Catalyst B/ethanol at 360 K for 7200 s raised conversion to 0.8514, yield to 0.4750, and score to 0.2416 while final risk remained 0.1623. It established that strong performance was accessible well below the safety limit and shifted attention toward moderate-to-high conversion rather than the mild batch-1 regime.

Batch 3 changed the selectivity hypothesis. Catalyst C/acetonitrile at 380 K for 3600 s gave selectivity 0.6252, the highest final-assay selectivity observed, despite conversion of only 0.7306. This motivated the later Catalyst C/acetonitrile series. However, catalyst, solvent, and thermal history were all changed relative to batch 2, so the causal attribution to Catalyst C was initially more confident than the design justified.

Batch 4 mainly supplied a negative screening result. Catalyst D/toluene at 360 K for 7200 s achieved conversion 0.9148 but selectivity only 0.4895, degradation 0.2268, and score 0.2008. It helped separate conversion from useful performance. Because Catalyst D and toluene were never tested separately, it did not identify which categorical factor caused the result.

Batch 5 was central to the competing-pathway interpretation. Catalyst B/acetonitrile at 350 K for 10000 s reached conversion 0.9423, but byproduct was 0.4892, degradation was 0.3158, and score was only 0.2306. This was strong evidence against optimizing conversion alone. It motivated the K1 statement that “additional exposure increasingly generates byproduct or degradation.”

Batches 6 and 7 were the cleanest causal comparison. Both used Catalyst C at 350 K for 7200 s and differed in solvent. Acetonitrile in batch 6 gave conversion 0.7993, selectivity 0.5441, yield 0.4423, and score 0.2150; ethanol in batch 7 gave 0.7184, 0.4609, 0.3334, and 0.1558. This genuinely formed the catalyst–solvent coupling judgment rather than merely suggesting it through confounded screening.

Batches 6, 9, and 10 formed the nonmonotonic exposure judgment for Catalyst C/acetonitrile. Batch 9, at 370 K for 6000 s, scored 0.2373, whereas the more converted batch 10, at 365 K for 8000 s, scored 0.2297. The comparison was not a pure time perturbation because temperature also changed, but together with batch 5 it supported an intermediate optimum.

Batch 11 established the sample-best result: Catalyst B/ethanol at 355 K for 8000 s produced score 0.2454 at risk 0.1617. Batch 12 was an exact procedural repeat and reduced confidence in small score differences because it scored only 0.2328. That repeat was specifically chosen from existing data rather than from the initial packet.

Several choices were mainly guesses or resource-driven. Using the maximum reagent, catalyst, and solvent allotment in every campaign batch was convenient and allowed all stock to be divided equally across 12 batches, but it sacrificed dose-response identification. The four initial catalyst/solvent pairs were a sparse, confounded screen rather than a factorial design. Temperatures and durations were selected through qualitative intuition about thermal activation, not an estimated kinetic model. The universal use of one HPLC endpoint per batch was also a design convention rather than a conclusion from evidence.

3. Most important competing mechanisms

K1 proposed a minimal network with parallel productive and unproductive consumption plus possible product degradation:

R → P,
R → B,
P → D.

The main competitor is a purely parallel network:

R → P,
R → B,

with no significant P → D reaction. In that explanation, worsening selectivity at longer exposure arises because the productive catalyst deactivates, the unproductive channel becomes relatively dominant as composition changes, or the public degradation warning is only a correlated damage indicator rather than material lost from P.

A second competitor is catalyst deactivation:

d(active catalyst)/dt < 0,
with productive chemistry depending more strongly on active catalyst than background byproduct formation. This could reproduce the observation that conversion continues to rise while selectivity falls, without requiring direct target degradation.

A third explanation is conversion-dependent inhibition or medium change. As reagent is consumed, product, byproduct, or changing composition could alter the relative rate constants. The categorical solvent effects could then arise from solvation or transport terms rather than different elementary branching chemistry.

A fourth explanation is mass-transfer or heat-transfer limitation. Most experiments used 700 rpm, while batch 1 used 500 rpm, and no systematic stirring study was performed. The public temperature changes showed that the setpoint was approached dynamically. Apparent kinetic differences could therefore include different thermal trajectories rather than only Arrhenius chemistry.

The existing data can distinguish some broad propositions. They reject a model in which score is determined by conversion alone. They also show that solvent is not merely an inert label for Catalyst C: batches 6 and 7 changed both conversion and selectivity. They support a nonconstant effective selectivity over thermal exposure.

The data cannot distinguish direct P → D degradation from catalyst deactivation, changing parallel branching, product inhibition, or a conversion-dependent medium effect. Endpoint measurements provide no direct observation of a rise and subsequent fall in P within one vessel. The degradation warning correlates with severe conditions but is not a demonstrated mole fraction. Incomplete catalyst–solvent crossing also prevents separation of general catalyst effects from pair-specific interactions.

4. One additional complete experiment

If exactly one new legal complete experiment were available, I would run a within-vessel time-course near the recommended regime rather than another isolated endpoint:

• 0.080 L ethanol, solvent 1
• 0.040 mol reagent
• 0.005 mol Catalyst B, catalyst 1
• 700 rpm
• heat at 355 K in three successive 4000 s segments
• obtain HPLC measurements after 4000, 8000, and 12000 cumulative seconds
• then quench, terminate, and perform the required final assay

This uses the batch-11 material system but creates internal temporal information. The segmented thermal history would not be identical to a single 12000 s heat because later segments start from an already warm state, so the actual temperature trajectory would need to be retained in the interpretation. Nevertheless, it would be more discriminating than another endpoint-only batch.

Possible outcomes would have different implications:

• If conversion rose continuously while target yield rose by 4000–8000 s and then fell by 12000 s, with byproduct or degradation increasing, that would provide direct support for secondary target loss or another genuinely time-dependent loss process.
• If target yield plateaued but did not decline while conversion and byproduct continued to rise, a changing parallel branching ratio or catalyst deactivation would become more plausible than P → D.
• If conversion, yield, and selectivity were already nearly stationary by 4000 s, then the apparent temperature–time trends among the original batches would more likely reflect differing thermal ramps, categorical interactions, or measurement variation.
• If all three HPLC measurements varied only within instrument uncertainty, confidence in the proposed exposure optimum would decrease, and the difference between batches 11 and 12 would deserve more weight as noise.
• If the 8000 s measurement reproduced batch 11 closely but the final post-quench assay differed materially, the quench/instrument confounding identified in K1 would become a central issue.

If campaign-style resource constraints allowed only one nonfinal instrument use, I would measure at 4000 s and use the final assay at 8000 s, accepting that this weaker two-point trajectory could not establish a yield maximum.

5. Tradeoff between identifiability and score optimization

The research goal emphasized finding a strong safe-score procedure, and that substantially shaped the campaign. Once batch 2 scored 0.2416 safely, later experiments concentrated around active catalyst/solvent pairs and moderate-to-high thermal exposure. This increased the probability of improving the recommendation but reduced the breadth and orthogonality of the mechanistic design.

The largest sacrifice of identifiability was the initial confounding of catalyst, solvent, temperature, duration, and, for batch 1, stirring speed. A full catalyst-by-solvent screen at fixed thermal conditions would have identified categorical effects much better, but it would have consumed most of the 12 batches and likely included many low-scoring combinations. Likewise, all batches used the same maximum reagent and catalyst quantities, so no catalyst-order or concentration-response information was obtained.

There were some deliberate sacrifices of score for information. Batch 7 tested Catalyst C with ethanol even though batch 6 had already made acetonitrile look more attractive; its score of 0.1558 was poor, but the matched comparison produced the campaign's clearest interaction evidence. Batch 1 was also primarily a baseline and scored very poorly. Batch 3's short, hot condition was useful for identifying a high-selectivity regime rather than merely copying batch 2.

Conversely, batches 9–12 increasingly favored optimization. Batches 9 and 10 refined exposure for Catalyst C/acetonitrile, while batches 11 and 12 concentrated on Catalyst B/ethanol. Batch 12 sacrificed the opportunity to test a new factor in favor of checking repeatability of the sample-best recipe. That was valuable for recommendation confidence but provided little new structural identification.

Intermediate HPLC measurements were also used mainly as endpoint confirmation immediately before quenching. A time-course allocation would have been more mechanistically informative, but one HPLC measurement in every batch supported rapid operational comparison across candidates. Thus the campaign was an optimization-oriented sequential design with a few diagnostic contrasts, not a mechanism-optimal design.

6. Underused evidence and weaknesses in the blind predictions

Several evidence sources were underused. I did not inspect or quantitatively model the full characterization artifacts and raw spectral structures. The final-assay peak assignments could potentially have supported a more explicit mass-balance analysis, although the public mapping remained bounded and synthetic. I also did not fit the actual temperature transients, despite recording heat-step temperature changes. A thermal-response model could have separated requested setpoint from integrated exposure.

The operation-level risk deltas were only used qualitatively. They contained information about solvent addition, reagent addition, heating, and quench contributions. However, because every campaign batch used the same large charge and all final assays followed quenching, those deltas could not identify how risk scales with the much smaller charges and omitted quenches in the blind questions.

The HPLC/final-assay pairs were not modeled jointly. Their differences contain information about instrument noise and possible quench-state changes. Instead, K1 treated them descriptively. The exact batch-11/batch-12 repeat could also have been used to inflate predictive uncertainty more systematically.

The least reliable blind predictions are Q06, Q08, and Q12 because they use 465 K, far above the campaign maximum target of 380 K. Q08 additionally combines that temperature with the high catalyst loading and 7200 s duration. Q04 is also weak because it combines high catalyst loading with 14400 s at 410 K, a much more severe exposure than any completed batch. These predictions depend almost entirely on extrapolating the proposed competing-pathway model.

Q01–Q04 and Q05–Q08 also change the absolute scale from 0.080 L solvent and 0.040 mol reagent to 0.005 L and 0.003 mol, while varying the catalyst-to-reagent ratio. K1 explicitly said that catalyst loading, concentration, dilution, and scale dependence were unidentifiable. Therefore, the point predictions for those cases should be regarded as structural guesses, not calibrated interpolation.

Some prediction intervals were probably too narrow:

• Q06 and Q08 assigned conversion intervals starting at 0.97 and 0.99 and byproduct estimates near saturation. Without any 465 K data, those lower bounds express excessive confidence in monotonic Arrhenius acceleration and the assumed degradation network.
• Q04 similarly placed conversion in [0.98, 1.00], despite having no validated catalyst-loading law.
• Q12 used conversion [0.91, 1.00]; rapid heating dynamics over only 1800 s make that interval particularly questionable.
• Q03 and Q07 treated the high catalyst loading as predictably beneficial, although catalyst loading was never varied in the campaign.
• Q09 and Q10 assumed nearly identical chemistry and attributed the main difference to quench-induced risk reduction. That is reasonable from the observed campaign sequence, but the magnitude of quench effects at the new scale and temperature was not identified.
• The safety-risk intervals may be too narrow across nearly all queries because it was unknown whether risk scales with absolute inventory, concentration, thermal state, peak temperature, or some combination.

These weaknesses are not contradictions of K1's stated scope; K1 explicitly limited its interpretation to one concentration, catalyst loading, and mixing regime and said that the risk rule was not identifiable. However, the numerical Q predictions sometimes failed to propagate those admissions fully. In particular, near-boundary estimates of conversion, selectivity, and byproduct should have had wider intervals, and some intervals should have allowed qualitatively different behavior such as catalyst deactivation or incomplete heating.

No prediction truth has yet been supplied, so none of these criticisms is based on retrospective knowledge of errors. They are an audit of extrapolation distance and internal consistency with K1.

7. Limitations of the sealed recommendation

The sealed recommendation selected batch 11 because it had the highest observed score, 0.2454, at risk 0.1617. This is a sample-maximum statement, not proof of global or even local optimality.

The exact repeat in batch 12 immediately demonstrates the limitation. Under the same stated procedure, batch 12 scored 0.2328. The two-run mean is about 0.2391, which is not clearly superior to batch 2's single observed score of 0.2416 or batch 9's 0.2373 once measurement and process uncertainty are acknowledged. Selecting batch 11 rather than the replicated-condition mean introduces winner's-curse bias.

Local robustness was only sparsely tested. Batches 2, 8, 11, and 12 used Catalyst B/ethanol at different temperature–time combinations, but temperature and duration were not independently varied on a compact grid. A proper local study would replicate the center and test, for example, 350, 355, and 360 K at fixed 8000 s, plus 7000, 8000, and 9000 s at fixed 355 K. It would compare mean score, variance, peak risk, and degradation rather than selecting the largest single realization.

Repeatability would require more than one duplicate pair. At least several independent repeats should estimate process variance and final-assay variance. Intermediate HPLC measurements could determine whether variability originates before quenching or mainly in the final assay. Randomizing run order would help separate recipe effects from any campaign drift, even though the public contract did not reveal a drift mechanism.

Robustness to material quantities was not tested at all. Catalyst loading, reagent concentration, solvent volume, and stirring should be perturbed separately. The blind questions illustrate why this matters: their catalyst-to-reagent ratios and scale lie outside the fitted domain.

Cross-material generalization is especially limited. Catalyst B/ethanol cannot be assumed to transfer to Catalyst B/acetonitrile, as batch 5 already suggests, and Catalyst C showed a strong solvent interaction between batches 6 and 7. No conclusion should be transferred to a real named reaction merely because ethanol or acetonitrile appears in the benchmark.

Cross-world generalization is weaker still. K1's proposed equations were explanatory abstractions for this synthetic world, not validated universal laws. Another world could change categorical activity tables, risk scaling, thermal response, or measurement mapping while preserving the same public action vocabulary.

Accordingly, the defensible conclusion is: batch 11 was the highest observed compliant completed batch in this finite campaign, and its procedure was supported by one lower-scoring exact repeat. It was not proven optimal, its expected score was not established with precision, and its robustness outside the narrow tested catalyst–solvent–loading–temperature region remains unknown.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 97.6 | none | 0 |
| Q | yes | 0 | 95.3 | none | 0 |
| K2 | yes | 0 | 103.0 | none | 0 |

## Scope note

This report contains only information available before truth release. Reference truth, prediction scoring, and recommendation retests are intentionally absent because the full 60-task block has not yet completed.
