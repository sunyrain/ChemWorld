# RX-W05--P--safety_constrained_optimization--MisIndexed

## Run summary

- World: `RX-W05`
- Locus: `P`
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

No recovery override was required for this task.

## Sealed recommendation

- Selected batch: `12`
- Rationale: Batch 12 achieved the strongest observed public safe score (0.47356) while remaining well below the 0.35 safety limit (risk 0.10315). Its procedure used 0.003 mol reagent, 0.0075 L water, 0.000525 mol Catalyst D, and one 3300 s heat at a 385 K requested boundary with 600 rpm stirring, followed by termination and final assay.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S0 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 420 K x 3300 s @ 600 rpm | no | 0.7771 | 0.8172 | 0.9454 | 0.1896 | 0.1405 | 0.2264 | 0.4338 |
| 2 | S0 (0.0075 L) | 0.003000 mol | C0 (0.000525 mol) | 420 K x 3300 s @ 600 rpm | no | 0.6923 | 0.8238 | 0.8582 | 0.1639 | 0.0663 | 0.2255 | 0.4306 |
| 3 | S0 (0.0075 L) | 0.003000 mol | C1 (0.000525 mol) | 420 K x 3300 s @ 600 rpm | no | 0.7368 | 0.7878 | 0.9281 | 0.1975 | 0.1025 | 0.2260 | 0.4251 |
| 4 | S0 (0.0075 L) | 0.003000 mol | C2 (0.000525 mol) | 420 K x 3300 s @ 600 rpm | no | 0.5514 | 0.7099 | 0.7825 | 0.2350 | 0.0512 | 0.2245 | 0.3302 |
| 5 | S1 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 420 K x 3300 s @ 600 rpm | no | 0.6781 | 0.6897 | 0.9661 | 0.2950 | 0.2378 | 0.2496 | 0.3616 |
| 6 | S2 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 420 K x 3300 s @ 600 rpm | no | 0.7093 | 0.7201 | 0.9782 | 0.2949 | 0.2461 | 0.2678 | 0.3742 |
| 7 | S3 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 420 K x 3300 s @ 600 rpm | no | 0.5753 | 0.5854 | 0.9515 | 0.4023 | 0.2858 | 0.2798 | 0.2792 |
| 8 | S0 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 410 K x 3300 s @ 600 rpm | no | 0.7722 | 0.8254 | 0.9303 | 0.1812 | 0.1068 | 0.1816 | 0.4605 |
| 9 | S0 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 430 K x 3300 s @ 600 rpm | no | 0.7660 | 0.7883 | 0.9760 | 0.2017 | 0.1460 | 0.2698 | 0.4136 |
| 10 | S0 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 400 K x 3300 s @ 600 rpm | no | 0.7498 | 0.8395 | 0.9043 | 0.1616 | 0.1080 | 0.1428 | 0.4699 |
| 11 | S0 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 390 K x 3300 s @ 600 rpm | no | 0.7393 | 0.8275 | 0.8794 | 0.1441 | 0.0953 | 0.1139 | 0.4733 |
| 12 | S0 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 385 K x 3300 s @ 600 rpm | no | 0.7214 | 0.8487 | 0.8528 | 0.1314 | 0.0792 | 0.1032 | 0.4736 |

## Complete experimental actions and observations

### Batch 1

Lifecycle index: `1`; end step: `7`.

```json
{
  "actions": [
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.0075
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 420
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
    "byproduct_signal": 0.1896010935306549,
    "conversion": 0.9454025030136108,
    "cost": 0.7402999997138977,
    "degradation_warning": 0.1405431181192398,
    "safety_risk": 0.2263662964105606,
    "score": 0.4337889850139618,
    "selectivity": 0.8171907663345337,
    "virtual_spectrum_summary": 0.1675250083208084,
    "yield": 0.7771146893501282
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
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.0075
    },
    {
      "catalyst": 0,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 420
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
    "byproduct_signal": 0.16385798156261444,
    "conversion": 0.8582122325897217,
    "cost": 0.36629998683929443,
    "degradation_warning": 0.06634572148323059,
    "safety_risk": 0.22547794878482819,
    "score": 0.4305991232395172,
    "selectivity": 0.8237939476966858,
    "virtual_spectrum_summary": 0.11997746676206589,
    "yield": 0.6923112273216248
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
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.0075
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 420
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
    "byproduct_signal": 0.19747529923915863,
    "conversion": 0.9280763864517212,
    "cost": 0.5763000249862671,
    "degradation_warning": 0.10252586752176285,
    "safety_risk": 0.2260156273841858,
    "score": 0.42512935400009155,
    "selectivity": 0.787760853767395,
    "virtual_spectrum_summary": 0.15474805235862732,
    "yield": 0.7367963790893555
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
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.0075
    },
    {
      "catalyst": 2,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 420
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
    "byproduct_signal": 0.2350197583436966,
    "conversion": 0.782519519329071,
    "cost": 0.450300008058548,
    "degradation_warning": 0.05119440332055092,
    "safety_risk": 0.22449980676174164,
    "score": 0.33020922541618347,
    "selectivity": 0.7098860740661621,
    "virtual_spectrum_summary": 0.15229834616184235,
    "yield": 0.5513516664505005
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
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.0075
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 420
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
    "byproduct_signal": 0.29496994614601135,
    "conversion": 0.9660854339599609,
    "cost": 0.6632999777793884,
    "degradation_warning": 0.2377644032239914,
    "safety_risk": 0.24958759546279907,
    "score": 0.3616229295730591,
    "selectivity": 0.6896747946739197,
    "virtual_spectrum_summary": 0.26922744512557983,
    "yield": 0.6781002283096313
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
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.0075
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 420
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
    "byproduct_signal": 0.2948897182941437,
    "conversion": 0.9781747460365295,
    "cost": 0.6680999994277954,
    "degradation_warning": 0.24606478214263916,
    "safety_risk": 0.2677887976169586,
    "score": 0.37423932552337646,
    "selectivity": 0.7200990319252014,
    "virtual_spectrum_summary": 0.2729184925556183,
    "yield": 0.7092801332473755
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
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 3,
      "volume_L": 0.0075
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 420
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
    "byproduct_signal": 0.4022729992866516,
    "conversion": 0.9514697790145874,
    "cost": 0.6650999784469604,
    "degradation_warning": 0.28580766916275024,
    "safety_risk": 0.27975013852119446,
    "score": 0.2792060077190399,
    "selectivity": 0.5853658318519592,
    "virtual_spectrum_summary": 0.34986361861228943,
    "yield": 0.5752878785133362
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
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.0075
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 410
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
    "byproduct_signal": 0.18120959401130676,
    "conversion": 0.9302703142166138,
    "cost": 0.6603000164031982,
    "degradation_warning": 0.10682297497987747,
    "safety_risk": 0.18164575099945068,
    "score": 0.4604808986186981,
    "selectivity": 0.8253540992736816,
    "virtual_spectrum_summary": 0.1477356106042862,
    "yield": 0.7722147703170776
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
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.0075
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 430
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
    "byproduct_signal": 0.2017330527305603,
    "conversion": 0.9760265946388245,
    "cost": 0.6603000164031982,
    "degradation_warning": 0.14598922431468964,
    "safety_risk": 0.26984280347824097,
    "score": 0.4135989248752594,
    "selectivity": 0.7882972359657288,
    "virtual_spectrum_summary": 0.1766483187675476,
    "yield": 0.7659530639648438
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
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.0075
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
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
  "end_step": 61,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.1615607887506485,
    "conversion": 0.9042916893959045,
    "cost": 0.6603000164031982,
    "degradation_warning": 0.10799766331911087,
    "safety_risk": 0.1428210735321045,
    "score": 0.4699224829673767,
    "selectivity": 0.839526355266571,
    "virtual_spectrum_summary": 0.13745738565921783,
    "yield": 0.7497780323028564
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
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.0075
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 390
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
    "byproduct_signal": 0.1441289186477661,
    "conversion": 0.8794045448303223,
    "cost": 0.6603000164031982,
    "degradation_warning": 0.09529627859592438,
    "safety_risk": 0.11386619508266449,
    "score": 0.47327861189842224,
    "selectivity": 0.827472448348999,
    "virtual_spectrum_summary": 0.12215422838926315,
    "yield": 0.7393495440483093
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
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.0075
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 385
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
    "byproduct_signal": 0.1314300298690796,
    "conversion": 0.8528467416763306,
    "cost": 0.6603000164031982,
    "degradation_warning": 0.07919991761445999,
    "safety_risk": 0.10315173119306564,
    "score": 0.4735614061355591,
    "selectivity": 0.8486829996109009,
    "virtual_spectrum_summary": 0.10792648047208786,
    "yield": 0.721385657787323
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

1. Scope and evidence base

This interpretation is based only on the 12 completed campaign batches. Every batch used 0.003 mol of anonymous limiting reagent, 0.0075 L solvent, 0.000525 mol catalyst, 600 rpm stirring, and a single 3300 s heat operation. The variables deliberately changed were catalyst identity, solvent identity, and requested heating target. Consequently, the conclusions are local to this composition, loading, mixing rate, and residence time.

The reported temperatures are controller targets, not necessarily instantaneous liquid temperatures. In Batch 1, requesting 420 K for 3300 s produced a recorded temperature change of 107.36 K, demonstrating finite thermal response. I therefore do not equate a requested target directly with an isothermal liquid temperature.

2. Observed batch results

All values below are final-assay observations unless stated otherwise:

- Batch 1: Catalyst D, water, 420 K target. Yield 0.7771, selectivity 0.8172, conversion 0.9454, byproduct signal 0.1896, degradation warning 0.1405, safety risk 0.2264, score 0.4338.
- Batch 2: Catalyst A, water, 420 K. Yield 0.6923, selectivity 0.8238, conversion 0.8582, byproduct 0.1639, degradation 0.0663, risk 0.2255, score 0.4306.
- Batch 3: Catalyst B, water, 420 K. Yield 0.7368, selectivity 0.7878, conversion 0.9281, byproduct 0.1975, degradation 0.1025, risk 0.2260, score 0.4251.
- Batch 4: Catalyst C, water, 420 K. Yield 0.5514, selectivity 0.7099, conversion 0.7825, byproduct 0.2350, degradation 0.0512, risk 0.2245, score 0.3302.
- Batch 5: Catalyst D, ethanol, 420 K. Yield 0.6781, selectivity 0.6897, conversion 0.9661, byproduct 0.2950, degradation 0.2378, risk 0.2496, score 0.3616.
- Batch 6: Catalyst D, acetonitrile, 420 K. Yield 0.7093, selectivity 0.7201, conversion 0.9782, byproduct 0.2949, degradation 0.2461, risk 0.2678, score 0.3742.
- Batch 7: Catalyst D, toluene, 420 K. Yield 0.5753, selectivity 0.5854, conversion 0.9515, byproduct 0.4023, degradation 0.2858, risk 0.2798, score 0.2792.
- Batch 8: Catalyst D, water, 410 K. Yield 0.7722, selectivity 0.8254, conversion 0.9303, byproduct 0.1812, degradation 0.1068, risk 0.1816, score 0.4605.
- Batch 9: Catalyst D, water, 430 K. Yield 0.7660, selectivity 0.7883, conversion 0.9760, byproduct 0.2017, degradation 0.1460, risk 0.2698, score 0.4136.
- Batch 10: Catalyst D, water, 400 K. Yield 0.7498, selectivity 0.8395, conversion 0.9043, byproduct 0.1616, degradation 0.1080, risk 0.1428, score 0.4699.
- Batch 11: Catalyst D, water, 390 K. Yield 0.7393, selectivity 0.8275, conversion 0.8794, byproduct 0.1441, degradation 0.0953, risk 0.1139, score 0.4733.
- Batch 12: Catalyst D, water, 385 K. Yield 0.7214, selectivity 0.8487, conversion 0.8528, byproduct 0.1314, degradation 0.0792, risk 0.1032, score 0.4736.

Batch 1 also had an HPLC measurement immediately after heating: conversion 0.9581, yield 0.7752, selectivity 0.8269, and byproduct signal 0.2059. Its subsequent final assay gave broadly consistent performance, although individual values shifted within the scale expected from distinct noisy synthetic measurements and sample handling.

3. Proposed reaction network

The simplest model consistent with the observations is a desired reaction competing with one or more undesired pathways, followed by possible degradation of desired product:

R --kP--> P
R --kB--> B
P --kD--> D

Here R is the limiting reactant, P is the desired product, B denotes primary side products, and D denotes thermally generated degradation products. A local kinetic representation is:

dR/dt = -(kP + kB)R
dP/dt = kP R - kD P
dB/dt = kB R
dD/dt = kD P

The apparent rate constants plausibly depend on temperature, catalyst, and solvent:

kj = Aj exp(-Ej/RT) × Fj(catalyst) × Gj(solvent),

with possible catalyst-solvent interactions omitted from this minimal expression.

This is an explanatory model, not an identified law. The experiment did not measure concentrations versus time, so the individual rate constants and activation energies cannot be estimated uniquely.

The measurements support the approximate bookkeeping relation

yield ≈ conversion × selectivity.

For example, Batch 12 gives 0.8528 × 0.8487 = approximately 0.724, close to the measured yield of 0.7214. Similar approximate agreement occurs in other batches. Small discrepancies are compatible with assay noise, proxy definitions, degradation, or mass-balance conventions.

4. Temperature and residence-time interpretation

Within Catalyst D/water batches at fixed 3300 s, conversion increased monotonically with requested heating target: 0.8528 at 385 K, 0.8794 at 390 K, 0.9043 at 400 K, 0.9303 at 410 K, 0.9454 at 420 K, and 0.9760 at 430 K. This is strong evidence that higher requested temperature accelerates net reactant consumption.

However, higher conversion did not translate into a higher safe score. Between 385 and 430 K, selectivity generally declined, byproduct signal rose from 0.1314 to 0.2017, degradation rose from 0.0792 to 0.1460, and safety risk rose from 0.1032 to 0.2698. Yield exhibited a broad maximum rather than monotonic growth: it rose from 0.7214 at 385 K to about 0.77 around 410–420 K, then declined slightly at 430 K. This is the expected signature of competing reactions and secondary degradation becoming more important as thermal severity increases.

The score consequently formed a broad optimum on the lower-temperature side: 0.4736 at 385 K and 0.4733 at 390 K, versus 0.4605 at 410 K, 0.4338 at 420 K, and 0.4136 at 430 K. The difference between Batches 11 and 12 is only 0.00028, far smaller than the declared assay uncertainties for individual chemical observables. Thus Batch 12 had the best observed score, but the evidence does not establish that 385 K is intrinsically superior to 390 K. A more defensible conclusion is that a local optimum or plateau exists near the lowest tested region, approximately 385–400 K under this fixed 3300 s protocol.

The supplied initial model suggested that the higher-temperature side of the 420 K reference region would retain safe balanced performance more reliably. The data only partly support that prior: higher temperature reliably increased conversion, but it reduced selectivity, increased degradation and risk, and lowered the overall safe score. I therefore revised the interpretation from “higher is better” to “higher increases rate, while lower thermal severity gives the better balance.”

Because duration was never varied, temperature and thermal dose remain coupled. A lower target with a longer time, or a higher target with a shorter time, might reproduce similar conversion with different degradation. No claim about the optimal duration is justified from this campaign.

5. Catalyst effects

Batches 1–4 isolate catalyst identity at water/420 K. Catalyst D produced the highest conversion and yield: 0.9454 and 0.7771. Catalyst A was less active, with conversion 0.8582 and yield 0.6923, but had lower degradation and slightly higher selectivity; its score of 0.4306 was therefore close to Catalyst D's 0.4338. Catalyst B was intermediate in activity but less selective, giving score 0.4251. Catalyst C was clearly inferior under these conditions, with conversion 0.7825, selectivity 0.7099, yield 0.5514, and score 0.3302.

My interpretation is that the anonymous catalysts alter both desired and undesired activation channels rather than merely multiplying one common rate. Catalyst D strongly promotes productive conversion but also permits appreciable degradation at high thermal severity. Catalyst A may be intrinsically less active yet cleaner. Catalyst C either weakly promotes the desired channel, promotes a side pathway, or is inhibited under the aqueous conditions.

These are categorical benchmark formulations, so assigning real chemical identities, coordination mechanisms, or specific active sites would be speculation. Catalyst ranking may also change with solvent or temperature because those interactions were not factorially tested.

6. Solvent effects

Batches 1 and 5–7 compare solvents with Catalyst D at 420 K. Water gave the best balance despite not giving the highest conversion. Acetonitrile and ethanol increased conversion to 0.9782 and 0.9661, respectively, but decreased selectivity and sharply increased byproduct and degradation signals. Toluene was worst: conversion remained high at 0.9515, while selectivity fell to 0.5854, byproduct rose to 0.4023, and degradation rose to 0.2858.

This indicates that solvent changes relative pathway rates, not just the overall rate. Water appears to favor the productive channel or suppress side-product/degradation channels. Acetonitrile and ethanol accelerate consumption but do not preserve selectivity. Toluene strongly favors undesirable chemistry under the tested conditions.

The physical origin is unidentified. Plausible competing explanations include polarity-dependent stabilization of transition states, altered catalyst speciation, solvation of reactant or product, phase/mass-transfer behavior, or solvent-specific thermal susceptibility. The benchmark documentation explicitly states that solvent effects are categorical calibrations rather than predictions from real solvent-property correlations, so conventional chemical-property explanations should be treated only as hypotheses.

7. Safety model

Observed safety risk was always below the declared 0.35 limit. For water/Catalyst D batches it rose monotonically from 0.1032 at 385 K to 0.2698 at 430 K. In Batch 1, charging reagent and water produced cumulative risk of about 0.0593 before heating; the heat operation added about 0.1670, reaching 0.2264. Catalyst addition itself caused no visible increment in that batch.

A useful empirical representation is:

risk ≈ risk_charge(reagent, solvent, volume) + integral h(T(t), solvent, composition) dt,

where h increases nonlinearly with thermal severity. Solvent also matters: at the same nominal 420 K protocol, risks were 0.2264 for water, 0.2496 for ethanol, 0.2678 for acetonitrile, and 0.2798 for toluene. Since no solvent was tested across multiple temperatures, solvent-dependent kinetics and solvent-dependent hazard cannot be separated.

The risk variable may be an engineered cumulative benchmark index rather than a literal physical probability or measured heat-release quantity. I therefore interpret its monotonic trends operationally and do not translate it into real-world calorimetric units.

8. Coupling and overall operating logic

The major coupling is between conversion, selectivity, degradation, and safety:

- Raising thermal severity increases conversion.
- The same change increases side reactions, degradation, and safety risk.
- Yield initially benefits from increased conversion but eventually plateaus or falls because selectivity declines.
- The safe score rewards the lower-risk, cleaner balance rather than maximum conversion alone.
- Catalyst and solvent shift both the productive and unproductive branches, so activity cannot be optimized independently of selectivity.

A compact qualitative simulator would be:

1. Determine a thermal trajectory from target temperature, duration, volume, and solvent.
2. Evaluate catalyst- and solvent-dependent kP, kB, and kD along that trajectory.
3. Integrate the competing reaction network.
4. Compute conversion and selectivity, with yield approximately their product.
5. Map B and D inventories to byproduct and degradation proxy signals.
6. Accumulate safety risk from charging and thermal exposure.
7. Calculate score from productive outcome minus penalties associated with poor selectivity, byproduct, degradation, risk, and possibly cost.

The exact score formula was not public and cannot be recovered uniquely from 12 points.

9. Limits and competing explanations

Important unidentified factors include reaction order, activation energies, induction periods, catalyst deactivation, reversible equilibrium, product inhibition, phase behavior, heat-transfer coefficients, and mixing dependence. Only one reagent amount, solvent volume, catalyst loading, stirring speed, and duration were used. There were no true replicate batches, so batch-to-batch process variability cannot be separated from measurement noise.

The proposed parallel-plus-degradation network is not unique. A reversible desired reaction with a temperature-dependent equilibrium could also generate a conversion plateau. Consecutive conversion of product into the species reported as “byproduct” could replace the parallel B pathway. Catalyst inhibition or solvent-dependent catalyst activation could mimic changes attributed to intrinsic rate constants. The byproduct and degradation outputs are calibrated proxy signals and should not automatically be treated as exact mole fractions.

Catalyst effects were measured only in water at 420 K, while solvent effects were measured only with Catalyst D at 420 K. Therefore catalyst-solvent interactions are completely unresolved. The lower-temperature optimum was mapped only for Catalyst D in water, so it should not be extrapolated to the other catalysts or solvents.

10. Final interpretation

The most evidence-supported picture is a thermally accelerated desired conversion competing with catalyst- and solvent-dependent side reactions and product degradation. Catalyst D in water provides the best observed productive balance. High requested temperature maximizes conversion but increasingly sacrifices selectivity and safety. At the fixed 3300 s residence time, the best observed safe-score region is approximately 385–390 K, represented by Batches 12 and 11. Batch 12 is the sealed recommendation because it had the highest observed score, 0.47356, with risk 0.10315, but its tiny score advantage over Batch 11 should not be interpreted as a precisely located optimum.

## Q — Blind predictions

### Overall rationale

Predictions use the campaign-supported competing-pathway model: temperature and time increase conversion, but excessive thermal exposure raises byproduct formation, reduces selectivity, and accumulates safety risk. Catalyst B was inferred from its measured difference from Catalyst D in water, while solvent-2 behavior was anchored to the measured Catalyst D/acetonitrile batch. Yield was kept approximately consistent with conversion multiplied by selectivity. Score estimates emphasize yield and selectivity with a safety-risk penalty, as observed across the 12 campaign batches. Intervals include final-assay noise plus larger model uncertainty from the untested catalyst-solvent combination, reduced solvent volume, 400 rpm stirring, duration changes, sequential heating, and extrapolation above 430 K.

### Q01

This is closest to the 420 K solvent-2 experiment, adjusted for Catalyst B rather than D, lower solvent volume, and slower stirring. I expect high conversion but poorer selectivity than the aqueous Catalyst B batch, with substantial solvent-associated byproduct formation.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3100 | 0.2300 | 0.3900 |
| conversion | 0.9600 | 0.9100 | 0.9900 |
| safety_risk | 0.2550 | 0.2000 | 0.3200 |
| score | 0.3500 | 0.2700 | 0.4300 |
| selectivity | 0.6820 | 0.5900 | 0.7700 |
| yield | 0.6550 | 0.5500 | 0.7500 |

### Q02

The quench occurs after the full heat exposure, so it should not reverse accumulated conversion or risk. I assign only a small possible benefit from suppressing residual side chemistry before termination; the interval substantially overlaps Q01.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3050 | 0.2250 | 0.3850 |
| conversion | 0.9600 | 0.9100 | 0.9900 |
| safety_risk | 0.2550 | 0.2000 | 0.3200 |
| score | 0.3520 | 0.2700 | 0.4350 |
| selectivity | 0.6870 | 0.5950 | 0.7750 |
| yield | 0.6600 | 0.5550 | 0.7550 |

### Q03

Lowering the target from 420 to 390 K should reduce conversion moderately while improving selectivity, byproduct burden, and safety. The prediction extrapolates the measured aqueous temperature trend into the untested Catalyst B–acetonitrile combination.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2550 | 0.1700 | 0.3400 |
| conversion | 0.8950 | 0.8000 | 0.9550 |
| safety_risk | 0.1400 | 0.0950 | 0.2000 |
| score | 0.3800 | 0.2900 | 0.4700 |
| selectivity | 0.7050 | 0.6100 | 0.7950 |
| yield | 0.6280 | 0.5100 | 0.7350 |

### Q04

At 450 K, conversion should be nearly saturated, but the observed temperature trends imply markedly greater side reaction and accumulated risk. This is outside the measured temperature range, so the intervals are deliberately wide and include a safety-limit violation.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3900 | 0.2800 | 0.5200 |
| conversion | 0.9950 | 0.9650 | 1.0000 |
| safety_risk | 0.4100 | 0.3200 | 0.5300 |
| score | 0.2300 | 0.1100 | 0.3500 |
| selectivity | 0.5900 | 0.4500 | 0.7100 |
| yield | 0.5800 | 0.4300 | 0.7000 |

### Q05

The shorter 1500 s heat should leave appreciably more reactant but preserve selectivity and limit thermal byproduct generation. Finite heating time makes conversion especially uncertain because the campaign did not vary duration.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2200 | 0.1300 | 0.3200 |
| conversion | 0.7400 | 0.5900 | 0.8600 |
| safety_risk | 0.1500 | 0.1000 | 0.2100 |
| score | 0.3700 | 0.2700 | 0.4600 |
| selectivity | 0.7500 | 0.6500 | 0.8400 |
| yield | 0.5500 | 0.4100 | 0.6800 |

### Q06

Extending the 420 K exposure to 5100 s should push conversion toward completion, while secondary degradation and competing pathways reduce selectivity. Accumulated risk is predicted near or above the 0.35 limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4000 | 0.2900 | 0.5300 |
| conversion | 0.9930 | 0.9600 | 1.0000 |
| safety_risk | 0.3700 | 0.2900 | 0.4800 |
| score | 0.2500 | 0.1200 | 0.3800 |
| selectivity | 0.6000 | 0.4600 | 0.7200 |
| yield | 0.5900 | 0.4400 | 0.7100 |

### Q07

The low-then-high sequence gives 3600 s total exposure but delays the most severe thermal segment. I expect high conversion and intermediate selectivity, with less cumulative hazard than an equally long treatment beginning at 450 K.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3500 | 0.2400 | 0.4700 |
| conversion | 0.9650 | 0.9000 | 0.9950 |
| safety_risk | 0.3000 | 0.2200 | 0.4000 |
| score | 0.3100 | 0.1900 | 0.4200 |
| selectivity | 0.6500 | 0.5200 | 0.7600 |
| yield | 0.6300 | 0.4900 | 0.7400 |

### Q08

Starting at 450 K should create a more severe thermal trajectory than Q07 because cooling toward 390 K is not instantaneous. I therefore predict slightly higher conversion, byproduct formation, and risk, but lower selectivity and score.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4000 | 0.2800 | 0.5400 |
| conversion | 0.9800 | 0.9300 | 1.0000 |
| safety_risk | 0.3400 | 0.2500 | 0.4500 |
| score | 0.2600 | 0.1300 | 0.3900 |
| selectivity | 0.6000 | 0.4600 | 0.7200 |
| yield | 0.5900 | 0.4400 | 0.7100 |

### Q09

A short 440 K treatment trades duration against temperature. I expect substantial but incomplete conversion and more side reaction than the 420 K short-duration case, while remaining less hazardous than a full 3300 s high-temperature exposure.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3300 | 0.2200 | 0.4400 |
| conversion | 0.8700 | 0.7500 | 0.9500 |
| safety_risk | 0.2200 | 0.1600 | 0.3000 |
| score | 0.3250 | 0.2100 | 0.4300 |
| selectivity | 0.6700 | 0.5500 | 0.7800 |
| yield | 0.5800 | 0.4400 | 0.7000 |

### Q10

Post-heat quenching should leave accumulated risk and conversion close to Q09, but may modestly preserve product before final termination. Because the campaign did not directly compare quenched and unquenched batches, this small benefit is highly uncertain.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3200 | 0.2100 | 0.4300 |
| conversion | 0.8700 | 0.7500 | 0.9500 |
| safety_risk | 0.2200 | 0.1600 | 0.3000 |
| score | 0.3350 | 0.2200 | 0.4400 |
| selectivity | 0.6800 | 0.5600 | 0.7900 |
| yield | 0.5900 | 0.4500 | 0.7100 |

### Q11

The long 370 K treatment may recover substantial conversion while avoiding the strongest high-temperature selectivity and safety penalties. This temperature-duration tradeoff was not directly studied, so both conversion and accumulated low-temperature degradation remain important uncertainties.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2300 | 0.1400 | 0.3400 |
| conversion | 0.8900 | 0.7700 | 0.9600 |
| safety_risk | 0.1400 | 0.0900 | 0.2100 |
| score | 0.4050 | 0.3000 | 0.5000 |
| selectivity | 0.7500 | 0.6400 | 0.8400 |
| yield | 0.6700 | 0.5300 | 0.7800 |

### Q12

This combines the highest target and longest duration, far beyond the observed domain. Conversion should be effectively complete, but extensive competing reaction or product degradation is likely, with a clear safety-limit violation and a very low score. The large intervals reflect extreme extrapolation and the possibility of nonlinear thermal behavior.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5800 | 0.4200 | 0.7500 |
| conversion | 0.9980 | 0.9600 | 1.0000 |
| safety_risk | 0.6800 | 0.4800 | 0.8800 |
| score | 0.0600 | 0.0000 | 0.2000 |
| selectivity | 0.4300 | 0.2300 | 0.6100 |
| yield | 0.4000 | 0.1900 | 0.5800 |

## K2 — Retrospective analysis

1. Retrospective on the initial information

The initial packet did contain one substantive directional claim: relative to the 420 K, 3300 s reference region, “the higher-temperature side should retain safe balanced performance more reliably than the lower-temperature side.” It also explicitly described that model as incomplete and said experimental evidence was authoritative.

The conversion component of that claim received support. With Catalyst D in water at fixed 3300 s, conversion rose from 0.8528 in Batch 12 at 385 K to 0.8794 in Batch 11 at 390 K, 0.9043 in Batch 10 at 400 K, 0.9303 in Batch 8 at 410 K, 0.9454 in Batch 1 at 420 K, and 0.9760 in Batch 9 at 430 K. Thus higher requested temperature reliably increased reactant consumption over the tested range.

The broader “safe balanced performance” claim was contradicted. Score declined from 0.4736 in Batch 12 and 0.4733 in Batch 11 to 0.4338 in Batch 1 and 0.4136 in Batch 9. Over the same sequence, safety risk, byproduct signal, and degradation generally increased. This was not merely an absence of supporting evidence: it was positive counterevidence. I did revise the interpretation during the campaign and stated in K1 that the data changed the working view from “higher is better” to “higher increases rate, while lower thermal severity gives the better balance.” I did not continue treating the initial directional claim as authoritative after that evidence appeared.

The initial statement that a temperature-bound rollback should count as evidence against the attempted setting was not tested. No tested heat operation produced a reported rollback or rejected operation. Consequently, there was neither support nor counterevidence for that specific assertion. It would be incorrect to treat the absence of a rollback as proof that rollbacks cannot occur, especially for more extreme conditions.

The supplied 420 K, 3300 s, Catalyst D/water context was useful as a reference point. Batch 1 showed that this recipe was feasible and safely below the 0.35 limit, with risk 0.2264, conversion 0.9454, and score 0.4338. However, its status as a reference did not imply optimality, and the later temperature series demonstrated that it was not the best observed safe-score region.

The material packet did not make real-chemistry claims about the anonymous catalysts or reaction species. It expressly warned that solvent and catalyst effects were calibrated categorical benchmark effects. K1 respected that limitation: explanations involving polarity, catalyst speciation, or transition-state stabilization were labeled hypotheses rather than identified real chemistry.

2. Experiments that formed or changed the interpretation

Batch 1 established the operational baseline and was the only batch with a nonfinal HPLC observation. The post-heat HPLC values—conversion 0.9581, yield 0.7752, selectivity 0.8269, and byproduct 0.2059—were broadly compatible with the final assay. This supported using the final assay as the principal cross-batch comparison, although one paired measurement was insufficient to quantify instrument or sampling bias.

Batches 2–4 genuinely informed the catalyst interpretation. At the same water/420 K conditions, Catalyst A was cleaner but less active than Catalyst D, Catalyst B was intermediate, and Catalyst C was distinctly poor. These results changed the catalyst model from an unspecified categorical effect to a view in which catalysts alter desired and undesired pathways differently. In particular, the near equality of the Batch 1 and Batch 2 scores, despite different conversions and degradation warnings, showed that activity alone did not determine utility.

Batches 5–7 strongly changed the solvent interpretation. Ethanol, acetonitrile, and toluene all maintained high conversion with Catalyst D at 420 K, yet their selectivity and degradation performance were worse than water. Batch 7 was especially diagnostic: conversion remained 0.9515, but selectivity fell to 0.5854 and byproduct signal rose to 0.4023. That result made a simple “faster conversion gives better outcome” explanation untenable.

Batches 8 and 9 were the decisive test of the initial temperature claim. Batch 8 at 410 K improved score to 0.4605 and reduced risk to 0.1816, whereas Batch 9 at 430 K produced greater conversion but reduced score to 0.4136 and raised risk to 0.2698. These two results motivated the subsequent move toward lower temperatures.

Batches 10–12 were primarily local optimization experiments. Scores of 0.4699, 0.4733, and 0.4736 at 400, 390, and 385 K showed a broad lower-temperature plateau. They refined the recommended operating region but added only limited mechanistic identifiability because duration, loading, concentration, and stirring were still held fixed.

Several choices depended mostly on the initial packet rather than prior data. Batch 1 copied the supplied reference context. Holding 3300 s and 600 rpm throughout the campaign also followed that reference and convenience rather than evidence that those settings were optimal. The first catalyst and solvent scans used a conventional one-factor-at-a-time strategy.

Other choices depended on emerging data. The move from 420 K to 410 and 430 K bracketed the reference after the categorical scans. The later choices of 400, 390, and 385 K were direct adaptations to the increasing scores and decreasing risks observed on the lower-temperature side.

Important unverified guesses remained. I assumed that catalyst effects observed in water would remain directionally similar in other solvents, that one 3300 s comparison represented temperature effects adequately, and that requested temperature ordered actual thermal exposure consistently. Those assumptions became especially consequential in the blind predictions, where every query combined Catalyst B with acetonitrile, 0.005 L solvent, and 400 rpm—a combination never tested in the campaign.

3. Principal competing mechanisms and what the data distinguish

K1 proposed a minimal network consisting of parallel desired and undesired conversion plus consecutive product degradation:

R -> P, R -> B, and P -> D.

This model explains the simultaneous increase in conversion and deterioration of selectivity at high thermal severity. It also explains the broad yield maximum: faster formation of P initially helps yield, while increased formation of B and destruction of P eventually offset that benefit.

The strongest competing explanation is a reversible desired reaction combined with temperature-dependent equilibrium and one or more side reactions. Under that model, changes in conversion need not reflect only kinetic acceleration. A second competitor is a purely consecutive network in which most of the reported byproduct originates from P rather than directly from R. A third is catalyst activation, inhibition, or deactivation: apparent catalyst-dependent rate differences might reflect evolving catalyst state rather than fixed rate multipliers. Solvent-dependent heat transfer or phase behavior could also mimic intrinsic solvent effects.

The experiments can distinguish some broad propositions. They show that catalyst and solvent identities affect more than total conversion, because batches with similar conversion had very different selectivity and byproduct signals. They also show that higher requested thermal severity increases conversion and risk while eventually lowering balanced performance.

They cannot determine whether byproduct is formed in parallel from reactant or consecutively from product. There were no time courses across multiple batches, no species-resolved mechanistic assignments, and only one intermediate measurement. They cannot identify reaction order, activation energies, equilibrium constants, catalyst deactivation, or the actual temperature trajectory. They also cannot separate intrinsic solvent chemistry from solvent-dependent thermal or transport behavior. Because catalyst identity was varied only in water and solvent only with Catalyst D, catalyst-solvent interactions are completely confounded with extrapolation.

4. One additional complete experiment I would choose

I would repeat the Batch 12 recipe while adding one intermediate measurement:

- 0.003 mol reagent;
- 0.0075 L water;
- 0.000525 mol Catalyst D;
- heat at a 385 K requested target and 600 rpm for 1650 s;
- measure by HPLC;
- continue heating at 385 K and 600 rpm for another 1650 s;
- terminate;
- perform the required final assay.

This remains one complete experiment, reproduces the nominal total conditions of Batch 12, tests repeatability of the sealed recommendation, and provides a midpoint observation. Splitting the heat command could itself perturb the controller trajectory, so that limitation would need to be recorded.

If the midpoint showed substantially lower conversion than the final assay while selectivity remained nearly constant, that would support gradual productive conversion with relatively stable pathway competition at 385 K. If midpoint product yield were already near the final value but degradation or byproduct rose during the second half, that would support consecutive product loss and suggest shortening the residence time. If conversion and composition were already nearly final at 1650 s, then the 3300 s duration would appear unnecessarily long and the kinetic model used in K1 would need revision. If the replicated final score and risk agreed with Batch 12 within assay uncertainty, confidence in local repeatability would increase. A materially lower score or higher risk would show that the sealed recommendation was an unstable sample maximum rather than a reproducible operating point.

I prefer this experiment over testing another temperature because the largest unresolved weakness of the recommendation is the absence of replication and time resolution. One experiment cannot fully solve both, but this design contributes to both questions.

5. Tradeoff between mechanistic identifiability and score optimization

The early campaign devoted meaningful resources to identifiability. Batches 2–4 tested all catalyst categories at a common condition, and Batches 5–7 tested all solvents with Catalyst D. Some of those experiments were predictably unlikely to beat the reference after early evidence accumulated. Batch 4 with Catalyst C and Batch 7 with toluene ultimately had scores of only 0.3302 and 0.2792. They sacrificed immediate score improvement to establish categorical rankings and expose side-pathway behavior.

Batch 9 at 430 K was also mechanistically valuable despite its poorer score. It tested the higher-temperature side favored by the initial model and supplied direct counterevidence to the safe-balance claim.

The latter campaign shifted toward optimization. Batches 10–12 successively moved from 400 to 390 to 385 K because the score improved. This produced a better recommendation but spent three experiments densely along one axis while leaving duration, stirring, volume, catalyst loading, and catalyst-solvent interactions unidentified. That is a clear case in which optimization displaced broader mechanism learning.

Conversely, the categorical scans sacrificed score opportunities for information. A more aggressive optimization campaign could have moved to lower water temperatures immediately after Batch 1 and used more batches to tune temperature and duration. It might have found a better operating point, but it would have known much less about why water and Catalyst D were favorable.

The safe-score research goal appropriately biased the final choice toward a lower-risk balance rather than maximum conversion. Batch 9 had the highest conversion among the water temperature series but was not recommended. However, the same objective encouraged reliance on the observed scalar score, whose precise formula was not identified. The campaign therefore optimized an observed outcome more successfully than it identified the underlying kinetic system.

6. Underused evidence and weaknesses in the blind predictions

The raw characterization artifacts and spectral peak structures were not inspected beyond the processed summaries. They may have contained useful evidence about peak overlap, missingness, saturation, or consistency of proxy assignments. K1 appropriately avoided inventing hidden species identities, but more careful use of the public raw signals could still have tested whether processed changes were supported by the spectra.

The operation-level risk decomposition was used only explicitly for Batch 1, where reagent and solvent charging contributed about 0.0593 before heating and the heat step added about 0.1670. Comparable operation deltas from later batches were not assembled into a quantitative risk model. This weakened the later extrapolation to different durations, volumes, and multistep heating.

The single Batch 1 HPLC/final-assay pair was acknowledged but not modeled. Its conversion changed from 0.9581 to 0.9454 and byproduct from 0.2059 to 0.1896 between measurements. Those differences could reflect assay noise, destructive sampling, or process evolution, but with only one pair they were difficult to exploit. Instrument budgets were largely left unused, which was a missed opportunity for time-resolved evidence.

The blind predictions least reliable are Q12, Q04, Q07, Q08, Q06, and Q11. Q12 extrapolated simultaneously to 460 K and 6300 s, beyond both the tested temperature and duration ranges, and assigned a detailed degradation-like outcome without any high-severity training point above 430 K. Q04 similarly extrapolated to 450 K. Q07 and Q08 required predictions about thermal history and order effects even though no sequential heat program had been tested. Q06 and Q11 changed duration substantially despite K1 explicitly stating that temperature and thermal dose were confounded and that no optimal-duration claim was justified.

Even Q01 and Q02 were less secure than their presentation suggested. The campaign never tested Catalyst B in acetonitrile, 0.005 L solvent, or 400 rpm. Their conversion interval of 0.91–0.99 may be too narrow if catalyst-solvent interaction, concentration, or mixing has a strong effect. The small predicted quench benefits in Q02 and Q10 were unsupported by any quenched-versus-unquenched comparison.

Several score intervals were also likely too narrow because the score model was inferred informally from only 12 correlated observations. The prediction rationale said that the intervals included model uncertainty, but some numerical ranges conveyed more precision than K1 warranted. This is partially inconsistent with K1’s explicit scope limits: K1 said catalyst-solvent interactions were unresolved, the model applied only locally at one duration and stirring rate, and requested temperatures were not actual liquid temperatures. The sequential-heating predictions nevertheless relied on a specific thermal-inertia narrative, and the duration predictions relied on an assumed kinetic form. Those should have been presented with still wider intervals or stronger caveats.

No prediction truth has been supplied, so these are prospective self-criticisms, not post hoc explanations of prediction errors.

7. Limitations of the sealed recommendation

Batch 12 is the sample-in highest-scoring batch, not a proven global or even precisely located local optimum. Its score of 0.47356 exceeded Batch 11’s 0.47328 by only about 0.00028, far below the scale of the declared assay uncertainties. The defensible conclusion is a favorable region around 385–390 K under the tested recipe, not proof that exactly 385 K is superior.

There were no replicate batches. Therefore the repeatability of Batch 12’s score, safety risk of 0.10315, and final composition is unknown. The recommendation also lies at the lowest tested temperature boundary. Conditions below 385 K were never tested, so the true local maximum could lie below the explored range. Duration was fixed at 3300 s, and a shorter or longer treatment could improve the balance.

Local robustness should be tested with replicated center points and small perturbations around temperature, duration, stirring rate, catalyst loading, and solvent volume. A suitable design would include repeated 385 and 390 K batches, nearby temperatures such as 380 and 395 K, and modest duration changes around 3300 s. Replication is necessary before interpreting differences smaller than assay and process variability.

Cross-material robustness would require testing the lower-temperature strategy with other catalysts and solvents in a factorial or response-surface design. The current data do not show that 385–390 K is favorable for Catalyst A, B, or C, or for ethanol, acetonitrile, or toluene. Catalyst-solvent interactions could reverse the ranking.

Cross-world generalization is even more limited. The catalysts and reaction species are anonymous benchmark entities, and solvent effects are categorical runtime calibrations rather than validated real-solvent property laws. The recommendation should therefore be viewed as specific to this synthetic world and campaign contract. Generalization to another hidden world, simulator parameterization, or real chemical system would require new calibration and independent validation.

In summary, the sealed operation is justified as the best observed member of this 12-batch sample and as a representative of a promising low-temperature region. It has not been demonstrated to be uniquely optimal, reproducible, robust to small operating perturbations, transferable across material choices, or portable beyond this benchmark world.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 104.9 | none | 0 |
| Q | yes | 0 | 154.0 | none | 0 |
| K2 | yes | 0 | 110.2 | none | 0 |

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean 80% width | Mean interval score |
|---|---:|---:|---:|---:|
| byproduct_signal | 0.0640 | 0.8333 | 0.2183 | 0.3226 |
| conversion | 0.0485 | 0.5667 | 0.1212 | 0.1853 |
| safety_risk | 0.0974 | 0.5000 | 0.1696 | 0.4634 |
| score | 0.0674 | 0.7667 | 0.2104 | 0.2700 |
| selectivity | 0.0763 | 0.7500 | 0.2329 | 0.3536 |
| yield | 0.1010 | 0.6833 | 0.2596 | 0.4865 |

## Predictions versus released reference truth

### Q01

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3100 | 0.2300 | 0.3900 | 0.2826 | 0.2852, 0.2894, 0.2712, 0.2806, 0.2868 |
| conversion | 0.9600 | 0.9100 | 0.9900 | 0.9936 | 0.9944, 0.9886, 0.9985, 1.0000, 0.9865 |
| safety_risk | 0.2550 | 0.2000 | 0.3200 | 0.2975 | 0.2975, 0.2975, 0.2975, 0.2975, 0.2975 |
| score | 0.3500 | 0.2700 | 0.4300 | 0.3741 | 0.3745, 0.3704, 0.3762, 0.3731, 0.3761 |
| selectivity | 0.6820 | 0.5900 | 0.7700 | 0.7204 | 0.7250, 0.7175, 0.7148, 0.7117, 0.7328 |
| yield | 0.6550 | 0.5500 | 0.7500 | 0.7164 | 0.7143, 0.7102, 0.7240, 0.7179, 0.7156 |
### Q02

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3050 | 0.2250 | 0.3850 | 0.2861 | 0.2908, 0.2824, 0.2881, 0.2929, 0.2764 |
| conversion | 0.9600 | 0.9100 | 0.9900 | 0.9921 | 0.9993, 1.0000, 0.9838, 0.9912, 0.9863 |
| safety_risk | 0.2550 | 0.2000 | 0.3200 | 0.1512 | 0.1512, 0.1512, 0.1512, 0.1512, 0.1512 |
| score | 0.3520 | 0.2700 | 0.4350 | 0.4400 | 0.4421, 0.4407, 0.4410, 0.4418, 0.4345 |
| selectivity | 0.6870 | 0.5950 | 0.7750 | 0.7247 | 0.7349, 0.7269, 0.7271, 0.7216, 0.7132 |
| yield | 0.6600 | 0.5550 | 0.7550 | 0.7228 | 0.7198, 0.7212, 0.7257, 0.7294, 0.7176 |
### Q03

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2550 | 0.1700 | 0.3400 | 0.2305 | 0.2338, 0.2259, 0.2177, 0.2369, 0.2383 |
| conversion | 0.8950 | 0.8000 | 0.9550 | 0.9608 | 0.9596, 0.9490, 0.9674, 0.9626, 0.9652 |
| safety_risk | 0.1400 | 0.0950 | 0.2000 | 0.1854 | 0.1854, 0.1854, 0.1854, 0.1854, 0.1854 |
| score | 0.3800 | 0.2900 | 0.4700 | 0.4438 | 0.4466, 0.4474, 0.4404, 0.4439, 0.4408 |
| selectivity | 0.7050 | 0.6100 | 0.7950 | 0.7671 | 0.7763, 0.7752, 0.7648, 0.7603, 0.7591 |
| yield | 0.6280 | 0.5100 | 0.7350 | 0.7437 | 0.7453, 0.7506, 0.7349, 0.7477, 0.7399 |
### Q04

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3900 | 0.2800 | 0.5200 | 0.3349 | 0.3411, 0.3290, 0.3394, 0.3241, 0.3407 |
| conversion | 0.9950 | 0.9650 | 1.0000 | 0.9971 | 0.9964, 0.9936, 0.9975, 0.9981, 1.0000 |
| safety_risk | 0.4100 | 0.3200 | 0.5300 | 0.4031 | 0.4031, 0.4031, 0.4031, 0.4031, 0.4031 |
| score | 0.2300 | 0.1100 | 0.3500 | 0.2995 | 0.3030, 0.2973, 0.3051, 0.2950, 0.2974 |
| selectivity | 0.5900 | 0.4500 | 0.7100 | 0.6731 | 0.6859, 0.6698, 0.6734, 0.6614, 0.6750 |
| yield | 0.5800 | 0.4300 | 0.7000 | 0.6776 | 0.6782, 0.6748, 0.6911, 0.6732, 0.6704 |
### Q05

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2200 | 0.1300 | 0.3200 | 0.1390 | 0.1313, 0.1497, 0.1384, 0.1357, 0.1399 |
| conversion | 0.7400 | 0.5900 | 0.8600 | 0.8939 | 0.9038, 0.8951, 0.8931, 0.8821, 0.8954 |
| safety_risk | 0.1500 | 0.1000 | 0.2100 | 0.2972 | 0.2972, 0.2972, 0.2972, 0.2972, 0.2972 |
| score | 0.3700 | 0.2700 | 0.4600 | 0.4181 | 0.4209, 0.4187, 0.4150, 0.4146, 0.4214 |
| selectivity | 0.7500 | 0.6500 | 0.8400 | 0.8564 | 0.8553, 0.8572, 0.8540, 0.8567, 0.8586 |
| yield | 0.5500 | 0.4100 | 0.6800 | 0.7624 | 0.7676, 0.7631, 0.7562, 0.7563, 0.7688 |
### Q06

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4000 | 0.2900 | 0.5300 | 0.4142 | 0.4168, 0.4031, 0.4113, 0.4196, 0.4205 |
| conversion | 0.9930 | 0.9600 | 1.0000 | 0.9945 | 0.9842, 0.9940, 0.9980, 1.0000, 0.9961 |
| safety_risk | 0.3700 | 0.2900 | 0.4800 | 0.2972 | 0.2972, 0.2972, 0.2972, 0.2972, 0.2972 |
| score | 0.2500 | 0.1200 | 0.3800 | 0.2977 | 0.2966, 0.2960, 0.3021, 0.2986, 0.2951 |
| selectivity | 0.6000 | 0.4600 | 0.7200 | 0.6004 | 0.6005, 0.5997, 0.6043, 0.6057, 0.5920 |
| yield | 0.5900 | 0.4400 | 0.7100 | 0.6037 | 0.6035, 0.6000, 0.6114, 0.6014, 0.6020 |
### Q07

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3500 | 0.2400 | 0.4700 | 0.3184 | 0.3152, 0.3252, 0.3252, 0.3153, 0.3110 |
| conversion | 0.9650 | 0.9000 | 0.9950 | 0.9980 | 1.0000, 1.0000, 1.0000, 1.0000, 0.9902 |
| safety_risk | 0.3000 | 0.2200 | 0.4000 | 0.4275 | 0.4275, 0.4275, 0.4275, 0.4275, 0.4275 |
| score | 0.3100 | 0.1900 | 0.4200 | 0.3011 | 0.3054, 0.3035, 0.2994, 0.2993, 0.2978 |
| selectivity | 0.6500 | 0.5200 | 0.7600 | 0.6925 | 0.7058, 0.6881, 0.6972, 0.6796, 0.6920 |
| yield | 0.6300 | 0.4900 | 0.7400 | 0.6972 | 0.6993, 0.7056, 0.6895, 0.7005, 0.6912 |
### Q08

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4000 | 0.2800 | 0.5400 | 0.3216 | 0.3273, 0.3191, 0.3086, 0.3218, 0.3312 |
| conversion | 0.9800 | 0.9300 | 1.0000 | 0.9968 | 0.9991, 1.0000, 0.9973, 0.9961, 0.9914 |
| safety_risk | 0.3400 | 0.2500 | 0.4500 | 0.1975 | 0.1975, 0.1975, 0.1975, 0.1975, 0.1975 |
| score | 0.2600 | 0.1300 | 0.3900 | 0.4075 | 0.4073, 0.4070, 0.4041, 0.4125, 0.4069 |
| selectivity | 0.6000 | 0.4600 | 0.7200 | 0.7016 | 0.7006, 0.7052, 0.6910, 0.7046, 0.7067 |
| yield | 0.5900 | 0.4400 | 0.7100 | 0.6992 | 0.6986, 0.6948, 0.6970, 0.7099, 0.6957 |
### Q09

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3300 | 0.2200 | 0.4400 | 0.1517 | 0.1510, 0.1588, 0.1357, 0.1541, 0.1589 |
| conversion | 0.8700 | 0.7500 | 0.9500 | 0.9456 | 0.9443, 0.9462, 0.9392, 0.9438, 0.9543 |
| safety_risk | 0.2200 | 0.1600 | 0.3000 | 0.3768 | 0.3768, 0.3768, 0.3768, 0.3768, 0.3768 |
| score | 0.3250 | 0.2100 | 0.4300 | 0.3984 | 0.3958, 0.4013, 0.3970, 0.3990, 0.3989 |
| selectivity | 0.6700 | 0.5500 | 0.7800 | 0.8476 | 0.8351, 0.8618, 0.8575, 0.8339, 0.8498 |
| yield | 0.5800 | 0.4400 | 0.7000 | 0.7952 | 0.7969, 0.7935, 0.7871, 0.8057, 0.7929 |
### Q10

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3200 | 0.2100 | 0.4300 | 0.1532 | 0.1524, 0.1604, 0.1493, 0.1485, 0.1556 |
| conversion | 0.8700 | 0.7500 | 0.9500 | 0.9459 | 0.9443, 0.9377, 0.9581, 0.9487, 0.9408 |
| safety_risk | 0.2200 | 0.1600 | 0.3000 | 0.1712 | 0.1712, 0.1712, 0.1712, 0.1712, 0.1712 |
| score | 0.3350 | 0.2200 | 0.4400 | 0.4888 | 0.4881, 0.4857, 0.4916, 0.4910, 0.4875 |
| selectivity | 0.6800 | 0.5600 | 0.7900 | 0.8509 | 0.8547, 0.8603, 0.8394, 0.8540, 0.8458 |
| yield | 0.5900 | 0.4500 | 0.7100 | 0.7961 | 0.7925, 0.7846, 0.8071, 0.7989, 0.7972 |
### Q11

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2300 | 0.1400 | 0.3400 | 0.3207 | 0.3220, 0.3285, 0.3186, 0.3278, 0.3067 |
| conversion | 0.8900 | 0.7700 | 0.9600 | 0.9808 | 0.9709, 0.9777, 0.9940, 0.9742, 0.9873 |
| safety_risk | 0.1400 | 0.0900 | 0.2100 | 0.1548 | 0.1548, 0.1548, 0.1548, 0.1548, 0.1548 |
| score | 0.4050 | 0.3000 | 0.5000 | 0.4068 | 0.4034, 0.4056, 0.4113, 0.4075, 0.4063 |
| selectivity | 0.7500 | 0.6400 | 0.8400 | 0.6769 | 0.6720, 0.6683, 0.6786, 0.6851, 0.6803 |
| yield | 0.6700 | 0.5300 | 0.7800 | 0.6732 | 0.6701, 0.6762, 0.6801, 0.6713, 0.6682 |
### Q12

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5800 | 0.4200 | 0.7500 | 0.5786 | 0.5786, 0.5797, 0.5783, 0.5826, 0.5738 |
| conversion | 0.9980 | 0.9600 | 1.0000 | 0.9966 | 0.9974, 0.9885, 0.9990, 0.9992, 0.9990 |
| safety_risk | 0.6800 | 0.4800 | 0.8800 | 0.4202 | 0.4202, 0.4202, 0.4202, 0.4202, 0.4202 |
| score | 0.0600 | 0.0000 | 0.2000 | 0.1418 | 0.1464, 0.1386, 0.1392, 0.1429, 0.1417 |
| selectivity | 0.4300 | 0.2300 | 0.6100 | 0.4511 | 0.4571, 0.4436, 0.4565, 0.4418, 0.4566 |
| yield | 0.4000 | 0.1900 | 0.5800 | 0.4475 | 0.4551, 0.4464, 0.4372, 0.4555, 0.4432 |

## Recommendation retest

- Selected source batch: `12`
- Retest exact replay verified: `True`
- Retest failure: `none`

| Metric | Selected source batch | Independent retest | Retest minus source |
|---|---:|---:|---:|
| byproduct_signal | 0.1314 | 0.1473 | 0.0159 |
| conversion | 0.8528 | 0.8584 | 0.0055 |
| cost | 0.6603 | 0.6603 | 0.0000 |
| degradation_warning | 0.0792 | 0.0895 | 0.0103 |
| safety_risk | 0.1032 | 0.1032 | 0.0000 |
| score | 0.4736 | 0.4707 | -0.0029 |
| selectivity | 0.8487 | 0.8481 | -0.0005 |
| virtual_spectrum_summary | 0.1079 | 0.1213 | 0.0134 |
| yield | 0.7214 | 0.7132 | -0.0082 |

## Scope note

This is the final sanitized report produced after all 60 source sessions and K1/Q/K2 chains were sealed. It includes released reference truth, blind-prediction evaluation, and the independent recommendation retest. Provider-private event streams, credentials, thread identifiers, and token accounting remain excluded.
