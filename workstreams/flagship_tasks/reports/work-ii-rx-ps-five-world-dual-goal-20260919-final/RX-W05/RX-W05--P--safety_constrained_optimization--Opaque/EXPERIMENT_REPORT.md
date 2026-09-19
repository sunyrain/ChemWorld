# RX-W05--P--safety_constrained_optimization--Opaque

## Run summary

- World: `RX-W05`
- Locus: `P`
- Goal: `safety_constrained_optimization`
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

- Selected batch: `11`
- Rationale: Batch 11 achieved the highest observed safe score (0.3352) while keeping safety risk (0.2178) comfortably below the 0.35 limit; it used Catalyst A, acetonitrile, and a 375 K target for 7200 s.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S2 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 330 K x 3600 s @ 600 rpm → 330 K x 3600 s @ 600 rpm | no | 0.5052 | 0.7289 | 0.6914 | 0.1990 | 0.0630 | 0.1760 | 0.2742 |
| 2 | S2 (0.0800 L) | 0.040000 mol | C1 (0.002000 mol) | 330 K x 7200 s @ 600 rpm | no | 0.3480 | 0.6163 | 0.5569 | 0.2378 | 0.0682 | 0.1617 | 0.1762 |
| 3 | S2 (0.0800 L) | 0.040000 mol | C2 (0.002000 mol) | 330 K x 7200 s @ 600 rpm | no | 0.2050 | 0.4084 | 0.4715 | 0.2681 | 0.0202 | 0.1452 | 0.0659 |
| 4 | S2 (0.0800 L) | 0.040000 mol | C3 (0.002000 mol) | 330 K x 7200 s @ 600 rpm | no | 0.4089 | 0.6821 | 0.6029 | 0.2093 | 0.1017 | 0.1685 | 0.2185 |
| 5 | S0 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 330 K x 7200 s @ 600 rpm | no | 0.4253 | 0.7343 | 0.5735 | 0.1550 | 0.0074 | 0.1237 | 0.2554 |
| 6 | S1 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 330 K x 7200 s @ 600 rpm | no | 0.4044 | 0.6888 | 0.5967 | 0.1871 | 0.0592 | 0.1482 | 0.2269 |
| 7 | S3 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 330 K x 7200 s @ 600 rpm | no | 0.3351 | 0.5251 | 0.6372 | 0.3004 | 0.0618 | 0.1750 | 0.1503 |
| 8 | S2 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 350 K x 7200 s @ 600 rpm | no | 0.5937 | 0.7330 | 0.8267 | 0.2205 | 0.0879 | 0.1925 | 0.3168 |
| 9 | S2 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 370 K x 7200 s @ 600 rpm | no | 0.6506 | 0.7046 | 0.9321 | 0.2731 | 0.1178 | 0.2114 | 0.3345 |
| 10 | S2 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 390 K x 7200 s @ 600 rpm | no | 0.6689 | 0.6748 | 0.9609 | 0.3114 | 0.1718 | 0.2461 | 0.3216 |
| 11 | S2 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 375 K x 7200 s @ 600 rpm | no | 0.6562 | 0.7090 | 0.9349 | 0.2929 | 0.1522 | 0.2178 | 0.3352 |
| 12 | S2 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 375 K x 6000 s @ 600 rpm | no | 0.6497 | 0.7162 | 0.8906 | 0.2426 | 0.1177 | 0.2153 | 0.3311 |

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
      "target_temperature_K": 330
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 3600,
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
  "end_step": 8,
  "lifecycle_index": 1,
  "metrics": {
    "byproduct_signal": 0.19899745285511017,
    "conversion": 0.6914206147193909,
    "cost": 1.0,
    "degradation_warning": 0.06297165900468826,
    "safety_risk": 0.17602519690990448,
    "score": 0.274245023727417,
    "selectivity": 0.7288694977760315,
    "virtual_spectrum_summary": 0.13778585195541382,
    "yield": 0.5052423477172852
  },
  "ordinal": 1
}
```

### Batch 2

Lifecycle index: `2`; end step: `15`.

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
      "catalyst_amount_mol": 0.002,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
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
  "end_step": 15,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.23782461881637573,
    "conversion": 0.5568577647209167,
    "cost": 1.0,
    "degradation_warning": 0.06822730600833893,
    "safety_risk": 0.16168709099292755,
    "score": 0.1762031763792038,
    "selectivity": 0.6163221001625061,
    "virtual_spectrum_summary": 0.1615058332681656,
    "yield": 0.3479901850223541
  },
  "ordinal": 2
}
```

### Batch 3

Lifecycle index: `3`; end step: `22`.

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
      "catalyst_amount_mol": 0.002,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
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
  "end_step": 22,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.26808902621269226,
    "conversion": 0.47151169180870056,
    "cost": 1.0,
    "degradation_warning": 0.020247433334589005,
    "safety_risk": 0.14518937468528748,
    "score": 0.06593098491430283,
    "selectivity": 0.40840911865234375,
    "virtual_spectrum_summary": 0.15656031668186188,
    "yield": 0.20503190159797668
  },
  "ordinal": 3
}
```

### Batch 4

Lifecycle index: `4`; end step: `29`.

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
      "catalyst_amount_mol": 0.002,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
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
  "end_step": 29,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.20930318534374237,
    "conversion": 0.6029397249221802,
    "cost": 1.0,
    "degradation_warning": 0.10172585397958755,
    "safety_risk": 0.16851434111595154,
    "score": 0.2185262143611908,
    "selectivity": 0.6820734739303589,
    "virtual_spectrum_summary": 0.16089339554309845,
    "yield": 0.4088633060455322
  },
  "ordinal": 4
}
```

### Batch 5

Lifecycle index: `5`; end step: `36`.

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
      "duration_s": 7200,
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
  "end_step": 36,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.15496724843978882,
    "conversion": 0.5735086798667908,
    "cost": 1.0,
    "degradation_warning": 0.00743728457018733,
    "safety_risk": 0.12368606775999069,
    "score": 0.2553759515285492,
    "selectivity": 0.7342727184295654,
    "virtual_spectrum_summary": 0.08857876807451248,
    "yield": 0.4252890944480896
  },
  "ordinal": 5
}
```

### Batch 6

Lifecycle index: `6`; end step: `43`.

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
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
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
  "end_step": 43,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.18708069622516632,
    "conversion": 0.596733808517456,
    "cost": 1.0,
    "degradation_warning": 0.05921078100800514,
    "safety_risk": 0.14823275804519653,
    "score": 0.2269100844860077,
    "selectivity": 0.6887590289115906,
    "virtual_spectrum_summary": 0.12953923642635345,
    "yield": 0.4043792486190796
  },
  "ordinal": 6
}
```

### Batch 7

Lifecycle index: `7`; end step: `50`.

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
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
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
  "end_step": 50,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.3004002273082733,
    "conversion": 0.6371973752975464,
    "cost": 1.0,
    "degradation_warning": 0.06178240850567818,
    "safety_risk": 0.1749965399503708,
    "score": 0.15026800334453583,
    "selectivity": 0.525051474571228,
    "virtual_spectrum_summary": 0.1930222064256668,
    "yield": 0.33508458733558655
  },
  "ordinal": 7
}
```

### Batch 8

Lifecycle index: `8`; end step: `57`.

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
      "duration_s": 7200,
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
  "end_step": 57,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.22050172090530396,
    "conversion": 0.8267324566841125,
    "cost": 1.0,
    "degradation_warning": 0.08789075165987015,
    "safety_risk": 0.19252704083919525,
    "score": 0.3167512118816376,
    "selectivity": 0.7330142259597778,
    "virtual_spectrum_summary": 0.16082678735256195,
    "yield": 0.5936539173126221
  },
  "ordinal": 8
}
```

### Batch 9

Lifecycle index: `9`; end step: `64`.

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
  "end_step": 64,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.2730625569820404,
    "conversion": 0.9321143627166748,
    "cost": 1.0,
    "degradation_warning": 0.11775889247655869,
    "safety_risk": 0.21144285798072815,
    "score": 0.33446189761161804,
    "selectivity": 0.7045834064483643,
    "virtual_spectrum_summary": 0.20317591726779938,
    "yield": 0.650634765625
  },
  "ordinal": 9
}
```

### Batch 10

Lifecycle index: `10`; end step: `71`.

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
      "duration_s": 7200,
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
  "end_step": 71,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.311391144990921,
    "conversion": 0.9609010815620422,
    "cost": 1.0,
    "degradation_warning": 0.17183949053287506,
    "safety_risk": 0.24613870680332184,
    "score": 0.32158541679382324,
    "selectivity": 0.6747515797615051,
    "virtual_spectrum_summary": 0.24859291315078735,
    "yield": 0.6689245700836182
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
  "end_step": 78,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.2928936183452606,
    "conversion": 0.9349231123924255,
    "cost": 1.0,
    "degradation_warning": 0.15215183794498444,
    "safety_risk": 0.21784749627113342,
    "score": 0.3351925015449524,
    "selectivity": 0.7089573740959167,
    "virtual_spectrum_summary": 0.22955982387065887,
    "yield": 0.6562305688858032
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
      "duration_s": 6000,
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
  "end_step": 85,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.2425777018070221,
    "conversion": 0.8906371593475342,
    "cost": 1.0,
    "degradation_warning": 0.11765868216753006,
    "safety_risk": 0.21527314186096191,
    "score": 0.33110225200653076,
    "selectivity": 0.7162056565284729,
    "virtual_spectrum_summary": 0.18636414408683777,
    "yield": 0.6496500968933105
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

Scope and evidence basis

This report describes only the bounded synthetic reaction-and-thermal world explored in 12 completed batches. Catalyst identities are anonymous benchmark categories, and the named solvents have calibrated categorical effects; therefore, none of the conclusions should be interpreted as a claim about a particular real catalyst or real synthesis. All numerical results below are final-assay observations unless explicitly identified as intermediate HPLC measurements.

Observed operating map

All batches used 0.040 mol reagent and 0.080 L solvent. Catalyst A was normally used at 0.005 mol. Batches 2–4 used 0.002 mol of Catalysts B–D, so those catalyst comparisons are partly confounded by catalyst loading.

• Batch 1: Catalyst A, acetonitrile, 330 K target, 7200 s total heating delivered in two 3600 s segments. Yield 0.5052, conversion 0.6914, selectivity 0.7289, byproduct signal 0.1990, degradation warning 0.0630, safety risk 0.1760, score 0.27425.
• Batch 2: Catalyst B, acetonitrile, 330 K, 7200 s. Yield 0.3480, conversion 0.5569, selectivity 0.6163, byproduct 0.2378, degradation 0.0682, risk 0.1617, score 0.17620.
• Batch 3: Catalyst C, acetonitrile, 330 K, 7200 s. Yield 0.2050, conversion 0.4715, selectivity 0.4084, byproduct 0.2681, degradation 0.0202, risk 0.1452, score 0.06593.
• Batch 4: Catalyst D, acetonitrile, 330 K, 7200 s. Yield 0.4089, conversion 0.6029, selectivity 0.6821, byproduct 0.2093, degradation 0.1017, risk 0.1685, score 0.21853.
• Batch 5: Catalyst A, water, 330 K, 7200 s. Yield 0.4253, conversion 0.5735, selectivity 0.7343, byproduct 0.1550, degradation 0.0074, risk 0.1237, score 0.25538.
• Batch 6: Catalyst A, ethanol, 330 K, 7200 s. Yield 0.4044, conversion 0.5967, selectivity 0.6888, byproduct 0.1871, degradation 0.0592, risk 0.1482, score 0.22691.
• Batch 7: Catalyst A, toluene, 330 K, 7200 s. Yield 0.3351, conversion 0.6372, selectivity 0.5251, byproduct 0.3004, degradation 0.0618, risk 0.1750, score 0.15027.
• Batch 8: Catalyst A, acetonitrile, 350 K, 7200 s. Yield 0.5937, conversion 0.8267, selectivity 0.7330, byproduct 0.2205, degradation 0.0879, risk 0.1925, score 0.31675.
• Batch 9: Catalyst A, acetonitrile, 370 K, 7200 s. Yield 0.6506, conversion 0.9321, selectivity 0.7046, byproduct 0.2731, degradation 0.1178, risk 0.2114, score 0.33446.
• Batch 10: Catalyst A, acetonitrile, 390 K, 7200 s. Yield 0.6689, conversion 0.9609, selectivity 0.6748, byproduct 0.3114, degradation 0.1718, risk 0.2461, score 0.32159.
• Batch 11: Catalyst A, acetonitrile, 375 K, 7200 s. Yield 0.6562, conversion 0.9349, selectivity 0.7090, byproduct 0.2929, degradation 0.1522, risk 0.2178, score 0.33519.
• Batch 12: Catalyst A, acetonitrile, 375 K, 6000 s. Yield 0.6497, conversion 0.8906, selectivity 0.7162, byproduct 0.2426, degradation 0.1177, risk 0.2153, score 0.33110.

Proposed process mechanism

The observations are consistent with a catalytic conversion of limiting reactant R into desired product P, competing with formation of undesired material B and with temperature-dependent degradation of either P or a productive intermediate. A minimal phenomenological model would be:

  dR/dt = -k_rxn(T, catalyst, solvent, loading) R
  dP/dt = s(T, catalyst, solvent) k_rxn R - k_deg(T, catalyst, solvent) P
  dB/dt = [1-s(T, catalyst, solvent)] k_rxn R + alpha k_deg P

Here k_rxn is an effective conversion rate, s is the instantaneous productive branching fraction, and k_deg represents secondary loss or degradation. An Arrhenius-like temperature dependence is plausible for both productive and destructive pathways:

  k_rxn = A_rxn f_cat f_solv exp[-E_rxn/(RT)]
  k_deg = A_deg g_cat g_solv exp[-E_deg/(RT)].

The data suggest that increasing temperature accelerates productive conversion strongly at first, but also accelerates byproduct formation, degradation, and safety risk. If the destructive pathway has a stronger temperature dependence than the productive pathway, an intermediate-temperature optimum naturally results.

Yield is approximately, but not exactly, conversion multiplied by selectivity. For example, in Batch 11, 0.9349 × 0.7090 = approximately 0.663, close to the observed yield of 0.6562. Deviations are compatible with independent measurement noise, operational definitions of the assay channels, and secondary loss. Thus, conversion and selectivity should not be treated as independent objectives: a condition can consume more reactant while diverting a larger fraction away from the desired product.

Temperature and time effects

The cleanest trend is the Catalyst A/acetonitrile series. Raising the target from 330 K in Batch 1 to 350, 370, and 390 K in Batches 8–10 raised conversion from 0.691 to 0.827, 0.932, and 0.961. Yield rose from 0.505 to 0.594, 0.651, and 0.669. However, selectivity fell from roughly 0.733 at 350 K to 0.705 at 370 K and 0.675 at 390 K; byproduct signal rose from 0.221 to 0.273 and 0.311, and degradation warning rose from 0.088 to 0.118 and 0.172. Safety risk simultaneously rose from 0.1925 to 0.2114 and 0.2461.

This explains why score did not maximize at the condition with the highest conversion or yield. Score increased from 0.3168 at 350 K to 0.3345 at 370 K, then decreased to 0.3216 at 390 K. Batch 11 at 375 K gave the highest observed score, 0.3352, but its advantage over Batch 9 at 370 K was only 0.00073 and is too small to establish a sharply resolved optimum given assay noise. The supported conclusion is a broad optimum around 370–375 K for approximately two hours, not an exact optimum at 375 K.

The duration comparison at 375 K also supports a conversion-versus-damage tradeoff. Extending heating from 6000 s in Batch 12 to 7200 s in Batch 11 increased conversion from 0.8906 to 0.9349 and yield from 0.6497 to 0.6562, while selectivity decreased from 0.7162 to 0.7090. Byproduct increased from 0.2426 to 0.2929, degradation warning from 0.1177 to 0.1522, and risk from 0.2153 to 0.2178. The longer run produced only a modest score increase, from 0.3311 to 0.3352. This is consistent with diminishing productive return once most reactant has been consumed, followed by continuing side reaction or product degradation.

The vessel temperature did not instantly equal its target. For 7200 s heat operations, the observed temperature increases were about 30.9 K at a 330 K target, 49.1 K at 350 K, 66.6 K at 370 K, 83.4 K at 390 K, and 70.9 K at 375 K. This is consistent with a first-order thermal approach such as dT/dt = (T_target-T)/tau, possibly with reaction-dependent heat terms. Consequently, target temperature, actual temperature history, and time are coupled rather than interchangeable controls.

Catalyst effects

At 330 K in acetonitrile, the measured performance order was A > D > B > C by score. Catalyst A in Batch 1 gave score 0.2743, compared with 0.2185 for D, 0.1762 for B, and 0.0659 for C. The same qualitative order appeared in yield and selectivity: A gave yield/selectivity 0.505/0.729; D, 0.409/0.682; B, 0.348/0.616; and C, 0.205/0.408.

This suggests distinct categorical catalyst activity and branching profiles. Catalyst C appears particularly poor at directing converted material toward the desired channel, whereas Catalyst D is intermediate. However, this is not a clean intrinsic-catalyst ranking: Catalyst A was charged at 0.005 mol, while B–D were charged at 0.002 mol. Lower loading can reduce conversion and could also alter apparent selectivity through residence-time or concentration effects. The experiments therefore support the practical claim that the tested A procedure outperformed the tested B–D procedures, but they do not determine whether 0.005 mol of B, C, or D would remain inferior or whether Catalyst A could perform similarly at 0.002 mol.

Solvent effects

Batches 1 and 5–7 show that solvent affects activity, selectivity, side-product formation, and setup-associated safety. With Catalyst A near 330 K, acetonitrile gave the highest yield and score: yield 0.505 and score 0.274. Water gave the best selectivity, lowest byproduct and degradation signals, and lowest risk: selectivity 0.734, byproduct 0.155, degradation 0.007, risk 0.124. Its lower conversion, 0.574, limited yield to 0.425 and score to 0.255. Ethanol was intermediate, with conversion 0.597, selectivity 0.689, yield 0.404, and score 0.227. Toluene showed relatively high conversion, 0.637, but poor selectivity, 0.525, and high byproduct, 0.300, producing the lowest solvent-series score, 0.150.

This pattern implies that solvent is not merely changing a single reaction rate. Water appears to suppress unproductive or degrading channels but also slows productive conversion. Toluene permits conversion yet biases the network toward byproduct. Acetonitrile provides the best observed balance between rate and productive branching. Plausible latent causes include differential stabilization of catalytic states or transition states, changes in effective reagent/catalyst availability, and solvent-specific coupling to thermal or side-reaction pathways. The benchmark does not expose enough species-level information to distinguish these possibilities.

Safety model

All observed final risks were below the declared 0.35 limit; the maximum was 0.2461 in Batch 10. Risk appears path-dependent and approximately accumulative across charging and heating rather than being a simple function of final yield. A useful descriptive model is:

  risk_total ≈ risk_charge(reagent amount, solvent, volume) + integral h(T(t), catalyst, mixture) dt,

with h increasing nonlinearly with temperature. For Catalyst A/acetonitrile, the observed thermal risk increments over 7200 s were approximately 0.079 at 350 K, 0.098 at 370 K, 0.104 at 375 K, and 0.133 at 390 K. The increase above 375 K was disproportionately large. Solvent also changed the pre-thermal or total risk baseline: at the common 330 K procedure, final risk was 0.124 for water, 0.148 for ethanol, 0.176 for acetonitrile, and 0.175 for toluene.

The reaction score evidently rewards productive performance while penalizing some combination of risk, byproduct, degradation, and possibly cost. The exact score equation is not identifiable from 12 observations. All completed procedures displayed normalized cost 1.0 at final assay, so this campaign cannot identify the marginal cost penalty or determine whether lower catalyst or reagent charges could improve the score through cost reduction.

Evidence that changed the interpretation

The initial Batch 1 result established that Catalyst A/acetonitrile at moderate temperature was productive but incomplete. Batches 2–4 then showed large categorical differences among the tested catalyst procedures, leading me to retain A rather than assuming that all catalysts differed only in rate.

Batches 5–7 changed the solvent interpretation from a simple rate effect to a rate/selectivity tradeoff. Toluene had higher conversion than water but substantially worse yield and score because selectivity collapsed and byproduct increased. Water showed that low-risk, clean chemistry was possible but with slower conversion.

Batches 8–10 established the temperature tradeoff. The 390 K condition had the largest yield and conversion but scored worse than 370 K because selectivity, byproduct, degradation, and risk deteriorated. This ruled out a monotonic “hotter is better” explanation.

Batches 11 and 12 refined the local optimum and showed diminishing returns with longer residence time. They led to the final interpretation of a broad 370–375 K, 6000–7200 s operating region rather than a single precisely identified optimum. Batch 11 was selected because it had the highest observed score while retaining substantial safety margin.

Intermediate-measurement consistency

The HPLC measurements generally supported the final-assay trends but were not identical. For example, Batch 8 HPLC reported conversion 0.8457, selectivity 0.7508, and yield 0.5840, versus final values 0.8267, 0.7330, and 0.5937. Batch 11 HPLC reported conversion 0.9401, selectivity 0.6852, and yield 0.6848, versus final values 0.9349, 0.7090, and 0.6562. Since termination followed the intermediate measurement without another deliberate heating step, these differences are best treated as instrument/channel noise, sampling variability, or small termination effects, rather than strong evidence of rapid chemical change. They also reinforce that the tiny score difference between Batches 9 and 11 should not be overinterpreted.

Limits of identification

The campaign cannot identify molecular species, elementary steps, reaction orders, activation energies, or whether the degradation warning represents product decomposition, catalyst decomposition, or formation of a separate impurity. Only one reagent amount and one solvent volume were studied, so concentration effects and reaction order are unidentified. Stirring was fixed at 600 rpm, leaving mass-transfer limitations untested. Catalyst loading was not independently varied within each catalyst category. No unheated controls, time courses with multiple measurements in one vessel, or replicate batches at identical settings were run. Batch 1 used two heat segments whereas most comparisons used one continuous segment, so exact equivalence of its thermal history is assumed rather than demonstrated.

The final assays contain known synthetic measurement noise, and each condition was run only once. Consequently, fine differences—especially Batch 11 versus Batch 9—may be noise. The observations constrain an effective reaction network but do not uniquely identify it.

Reasonable competing explanations

1. Parallel pathways: reactant partitions directly into target and byproduct, with temperature and solvent changing the branching ratio. This is the primary interpretation above.
2. Consecutive degradation: target forms with high initial selectivity and is subsequently degraded at high temperature or long time. The increase in degradation warning and the duration comparison support this, but the data do not prove that the lost target itself becomes the measured byproduct.
3. Catalyst deactivation: high temperature or particular solvents may deactivate Catalyst A, limiting productive turnover while leaving background side reactions active. This could mimic product degradation.
4. Instrument-channel coupling: yield, selectivity, byproduct, and degradation estimates may share latent spectral information. Correlated assay errors could create some apparent mechanistic relationships.
5. Thermal-history effects: the observed trends may depend on ramping and heat accumulation rather than only on nominal target temperature. A model based on an integral such as integral k[T(t)]dt may fit better than one using target temperature directly.

Overall interpretation and supported recommendation region

Within the studied domain, the world behaves like a temperature-accelerated catalytic network with competing productive, byproduct, and degradation channels. Catalyst and solvent alter both effective rate and pathway selectivity. Higher temperature initially improves conversion and yield, but eventually increases byproduct, degradation, and risk enough to reduce the safe score. The best supported region is Catalyst A at 0.005 mol, 0.040 mol reagent, 0.080 L acetonitrile, 600 rpm, a target near 370–375 K, and a residence time near 6000–7200 s. Batch 11 is the best observed completed procedure, but Batch 9 and Batch 12 demonstrate that the optimum is broad and uncertain. Statements outside the tested ranges—especially above 390 K, beyond 7200 s, at other concentrations or catalyst loadings, or for real chemical identities—are extrapolations and should not be treated as established.

## Q — Blind predictions

### Overall rationale

Predictions use the campaign's effective parallel/consecutive reaction model, explicit thermal lag, Catalyst B's observed lower selectivity, and concentration-adjusted catalytic exposure. The score estimates apply the relationship identified exactly across the completed batches: score = -0.10 + 0.40×yield + 0.25×selectivity + 0.10×conversion - 0.45×safety_risk, subject to the public score bounds. Uncertainty is wider than final-assay noise because every query uses a Catalyst B concentration and reaction scale not directly studied, several temperatures exceed the 390 K campaign maximum, stirring is lower, and no campaign batch tested quenching. Intervals represent combined process, extrapolation, and assay uncertainty rather than independent channel errors.

### Q01

The high catalyst-to-reagent ratio should give nearly complete conversion despite the 3300 s thermal ramp. The late high-temperature exposure is expected to reduce Catalyst B selectivity and increase byproduct formation. The small physical scale should keep accumulated risk modest.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4400 | 0.3100 | 0.5700 |
| conversion | 0.9400 | 0.8400 | 0.9900 |
| safety_risk | 0.0750 | 0.0450 | 0.1300 |
| score | 0.3060 | 0.2200 | 0.3900 |
| selectivity | 0.5500 | 0.4500 | 0.6400 |
| yield | 0.5200 | 0.4000 | 0.6200 |

### Q02

Quenching immediately before termination is predicted to cause little change because no further deliberate reaction period follows. I allow a small possible benefit from faster stabilization, but the interval substantially overlaps Q01 because the quench effect was not measured in the campaign.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4350 | 0.3050 | 0.5650 |
| conversion | 0.9400 | 0.8400 | 0.9900 |
| safety_risk | 0.0740 | 0.0400 | 0.1300 |
| score | 0.3080 | 0.2200 | 0.3950 |
| selectivity | 0.5550 | 0.4550 | 0.6450 |
| yield | 0.5250 | 0.4050 | 0.6250 |

### Q03

The lower target temperature reduces both productive exposure and thermal damage relative to Q01. Conversion should remain high because the catalyst concentration is greater than in the studied Catalyst B batch, while selectivity should be somewhat better than at 420 K.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3800 | 0.2700 | 0.5000 |
| conversion | 0.8500 | 0.7000 | 0.9400 |
| safety_risk | 0.0550 | 0.0350 | 0.1000 |
| score | 0.3010 | 0.2150 | 0.3800 |
| selectivity | 0.5800 | 0.4900 | 0.6700 |
| yield | 0.4900 | 0.3700 | 0.5900 |

### Q04

The 450 K target should drive conversion close to saturation, but the late portion of the ramp extends beyond the campaign's measured temperature range. Stronger side reaction and degradation are therefore expected, with correspondingly broad selectivity, yield, and risk intervals.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5400 | 0.3900 | 0.6800 |
| conversion | 0.9880 | 0.9300 | 1.0000 |
| safety_risk | 0.1050 | 0.0650 | 0.1800 |
| score | 0.2600 | 0.1500 | 0.3500 |
| selectivity | 0.4800 | 0.3500 | 0.5900 |
| yield | 0.4700 | 0.3200 | 0.5800 |

### Q05

With only 1500 s of heating, thermal lag should prevent the vessel from spending much time near 420 K. This gives incomplete conversion but preserves selectivity and limits accumulated risk and byproduct formation.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1900 | 0.1000 | 0.3100 |
| conversion | 0.4600 | 0.3000 | 0.6500 |
| safety_risk | 0.0250 | 0.0120 | 0.0550 |
| score | 0.2080 | 0.1250 | 0.3000 |
| selectivity | 0.6300 | 0.5400 | 0.7100 |
| yield | 0.2900 | 0.1800 | 0.4200 |

### Q06

The longer 420 K treatment should exhaust nearly all reactant. Once conversion saturates, continued hot residence is expected mainly to increase secondary loss and byproduct formation, so the score need not exceed the shorter Q01 procedure.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5900 | 0.4500 | 0.7200 |
| conversion | 0.9990 | 0.9800 | 1.0000 |
| safety_risk | 0.1300 | 0.0800 | 0.2100 |
| score | 0.2170 | 0.1000 | 0.3200 |
| selectivity | 0.4300 | 0.2900 | 0.5600 |
| yield | 0.4200 | 0.2800 | 0.5500 |

### Q07

Heating first toward 390 K and then toward 450 K produces a gradual ramp, with the highest temperatures reached only late. This should give high conversion but less total severe-temperature exposure than a constant 450 K treatment.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4300 | 0.3000 | 0.5700 |
| conversion | 0.9000 | 0.7600 | 0.9800 |
| safety_risk | 0.0750 | 0.0450 | 0.1350 |
| score | 0.2830 | 0.1900 | 0.3700 |
| selectivity | 0.5400 | 0.4300 | 0.6400 |
| yield | 0.4800 | 0.3500 | 0.5900 |

### Q08

Starting with the 450 K target raises the early temperature faster than Q07, and the later 390 K segment does not reverse accumulated conversion or damage. I therefore predict slightly greater conversion, byproduct formation, and risk, with slightly poorer productive selectivity.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4700 | 0.3300 | 0.6100 |
| conversion | 0.9200 | 0.7900 | 0.9900 |
| safety_risk | 0.0800 | 0.0480 | 0.1450 |
| score | 0.2740 | 0.1750 | 0.3650 |
| selectivity | 0.5200 | 0.4000 | 0.6300 |
| yield | 0.4700 | 0.3300 | 0.5900 |

### Q09

Although the target is 440 K, the 1500 s duration is short relative to the observed thermal response time. The mixture should remain mostly in the ramp regime, giving moderate conversion with relatively preserved selectivity and low accumulated risk.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2200 | 0.1200 | 0.3400 |
| conversion | 0.5200 | 0.3400 | 0.7100 |
| safety_risk | 0.0300 | 0.0150 | 0.0650 |
| score | 0.2220 | 0.1300 | 0.3150 |
| selectivity | 0.6200 | 0.5200 | 0.7100 |
| yield | 0.3200 | 0.2000 | 0.4500 |

### Q10

As in Q02, the immediate quench is expected to have only a small stabilization effect because termination follows directly. The estimate is therefore nearly identical to Q09, with uncertainty explicitly covering no quench benefit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2150 | 0.1150 | 0.3350 |
| conversion | 0.5200 | 0.3400 | 0.7100 |
| safety_risk | 0.0290 | 0.0140 | 0.0650 |
| score | 0.2240 | 0.1300 | 0.3200 |
| selectivity | 0.6250 | 0.5250 | 0.7150 |
| yield | 0.3230 | 0.2000 | 0.4550 |

### Q11

The long 370 K treatment combines substantial residence time with a moderate target. High Catalyst B concentration should drive conversion close to completion, while the lower thermal severity should preserve more selectivity than the 420–450 K cases. This is predicted to be among the strongest scores in the query set.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4300 | 0.3100 | 0.5500 |
| conversion | 0.9680 | 0.8900 | 0.9950 |
| safety_risk | 0.0750 | 0.0450 | 0.1300 |
| score | 0.3350 | 0.2500 | 0.4050 |
| selectivity | 0.5900 | 0.5000 | 0.6700 |
| yield | 0.5600 | 0.4500 | 0.6500 |

### Q12

This condition is a large extrapolation beyond the measured thermal range and combines the highest target with the longest query duration. Conversion should saturate, but prolonged high-temperature exposure is expected to divert or degrade much of the desired product. The safety interval crosses the 0.35 limit because both thermal-risk curvature and Catalyst B behavior are poorly constrained here.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8200 | 0.6100 | 0.9600 |
| conversion | 1.0000 | 0.9900 | 1.0000 |
| safety_risk | 0.2400 | 0.1500 | 0.3800 |
| score | 0.0300 | 0.0000 | 0.1800 |
| selectivity | 0.2000 | 0.0500 | 0.3800 |
| yield | 0.1800 | 0.0300 | 0.3500 |

## K2 — Retrospective analysis

1. Initial claims: supported, contradicted, or untested

The initial material packet did not provide a substantive task-specific kinetic or mechanistic dossier. It explicitly said that the catalyst identities were opaque, that the named solvents acted through calibrated categorical benchmark effects, and that experimental evidence was authoritative. Thus, there was no initial claim such as “Catalyst A is best,” “acetonitrile is optimal,” or “the reaction follows a particular rate law” to confirm or refute.

Several framework-level claims were supported:

• Categorical material effects were clearly present. Under the tested 330 K/acetonitrile procedures, Batches 1–4 differed strongly in yield, selectivity, and score across catalyst choices. Likewise, Batches 1 and 5–7 showed large solvent effects that could not be described as a simple physical-property correction.
• The stated safety limit of 0.35 was respected in all completed experiments. The largest observed risk was 0.2461 in Batch 10.
• The declared measurement uncertainty was qualitatively consistent with differences between intermediate HPLC and final assay. For example, Batch 11 changed from HPLC yield 0.6848 and selectivity 0.6852 to final-assay yield 0.6562 and selectivity 0.7090. However, without replicate measurements I could not quantitatively validate the supplied noise model.

Important matters remained untested: reaction order, catalyst-loading dependence, concentration dependence, stirring or transport effects, quench effects, reproducibility, and the real meaning of the degradation channel. The campaign also did not test whether named-solvent physical properties have any predictive value beyond their categorical labels; the initial packet warned against making that inference.

It is important to distinguish absence of disconfirmation from positive support. Nothing in the campaign contradicted the claim that this is a bounded synthetic benchmark rather than a real named synthesis, but the experiments could not independently prove that claim. Similarly, no experiment contradicted the public final-assay calibration contract, but the study was not designed as an instrument-validation exercise.

One judgment deserved earlier correction. During exploration I treated the poor B–D results as evidence favoring Catalyst A. Yet Batches 2–4 used 0.002 mol catalyst, whereas Batch 1 used 0.005 mol. That was already direct evidence that the catalyst ranking was confounded. The sealed K1 report eventually stated this limitation explicitly, but the experimental policy had already committed to A for the remaining optimization batches. Thus, the practical ranking “the tested A procedure was best” was supported, while an intrinsic catalyst ranking was not.

2. Experiments that formed or changed the interpretation

Batch 1 established the first productive reference condition: Catalyst A/acetonitrile at a 330 K target gave conversion 0.6914, yield 0.5052, selectivity 0.7289, and score 0.27425. This result formed the initial view that moderate heating produced incomplete but reasonably selective conversion.

Batches 2–4 materially changed the catalyst view. Their scores were 0.17620 for B, 0.06593 for C, and 0.21853 for D, compared with 0.27425 for A. In particular, Catalyst C produced conversion 0.4715 but selectivity only 0.4084. This suggested that catalyst categories influence branching as well as rate. Nevertheless, choosing lower catalyst loading for B–D was an unvalidated design decision, not something justified by the initial packet or prior observations.

Batches 5–7 were genuinely diagnostic because they varied solvent while retaining Catalyst A, catalyst loading, reagent amount, solvent volume, nominal temperature, duration, and stirring. They changed my interpretation from “solvent mainly alters rate” to “solvent changes both rate and productive branching.” Toluene in Batch 7 gave conversion 0.6372, higher than water’s 0.5735 in Batch 5, but its selectivity was only 0.5251 versus 0.7343 for water. This was strong evidence against a one-dimensional solvent-rate explanation. Acetonitrile remained the best score compromise, while water offered cleaner and safer but slower behavior.

Batches 8–10 produced the clearest change in the thermal interpretation. Increasing the target from 350 to 370 to 390 K raised conversion from 0.8267 to 0.9321 to 0.9609, but score rose only from 0.31675 to 0.33446 and then fell to 0.32159. The simultaneous deterioration in selectivity, byproduct signal, degradation warning, and safety risk refuted a monotonic “hotter is better” optimization rule.

Batches 11 and 12 refined rather than transformed the model. At 375 K, increasing duration from 6000 to 7200 s raised conversion from 0.8906 to 0.9349 and yield from 0.6497 to 0.6562, while byproduct and degradation signals also rose. This supported diminishing productive returns and continuing secondary damage. It led to K1’s judgment that the optimum was a broad 370–375 K, 6000–7200 s region rather than a sharply identified point.

The main experiment choices driven by existing data were the solvent series and the later temperature series. The initial selection of acetonitrile and Catalyst A was largely exploratory. The lower B–D catalyst loading was an unsupported guess. Reusing 600 rpm, full reagent charge, and full solvent volume was mainly a standardization choice rather than a conclusion from evidence. The final emphasis on 370–375 K was data-driven, but the exact 375 K/7200 s selection depended on a very small observed score difference.

3. Current competing mechanisms and what the data distinguish

The leading effective explanation remains the network stated in K1: productive conversion competes with direct byproduct formation, while desired product or a productive intermediate may undergo secondary thermal degradation. Temperature, catalyst, solvent, and time affect both the overall rate and the branching fractions.

The most important alternatives are:

• Parallel branching only: reactant forms target and byproduct directly, with no appreciable destruction of formed target.
• Consecutive degradation: target forms first and is subsequently converted into degradation products or assay-visible byproduct.
• Catalyst deactivation: high temperature or certain solvents deactivate productive Catalyst A while background side reactions continue.
• Transport or mixing limitation: catalyst concentration, stirring, or phase behavior changes the apparent rate and selectivity without changing elementary chemistry.
• Assay-channel coupling: yield, selectivity, byproduct, and degradation estimates may share latent spectral information, producing correlations that resemble a reaction network.
• Thermal-history control: outcomes may depend on the full temperature trajectory rather than nominal target temperature and total duration alone.

The data distinguish some coarse alternatives. Toluene’s combination of relatively high conversion and poor selectivity shows that conversion and productive branching are separable. The 350–390 K series shows that increasing conversion can coincide with declining selectivity and score. The 6000 versus 7200 s comparison at 375 K is consistent with continued damage after most conversion has occurred.

The data do not distinguish direct side-product formation from degradation of already formed product. A single final assay after each batch cannot establish species chronology. The duration comparison is suggestive but not decisive because it lacks replication and uses separate vessels. The experiments also cannot distinguish product degradation from catalyst deactivation: both can yield a plateau in desired product and rising impurity channels. Stirring was fixed at 600 rpm, so mass-transfer explanations remain open. No raw spectral assignments were mapped to hidden species, preventing structural discrimination among these mechanisms.

4. One additional complete experiment

I would run a catalyst-loading discrimination experiment matching Batch 2 except for the Catalyst B amount:

• 0.040 mol reagent
• 0.080 L acetonitrile
• Catalyst B at 0.005 mol rather than 0.002 mol
• 330 K target for 7200 s at 600 rpm
• HPLC immediately before termination
• terminate
• final assay

This is preferable to another local temperature optimization because it changes exactly one major confounded factor relative to Batch 2 and makes the result directly comparable with Batch 1’s Catalyst A loading.

Possible outcomes would change the interpretation as follows:

• If conversion rose to or above Batch 1 while selectivity remained near Batch 2’s 0.616, Catalyst B would appear intrinsically active but intrinsically less product-selective. That would strengthen the parallel-branching interpretation and invalidate any simple activity ranking based on the original screen.
• If both conversion and selectivity rose toward Batch 1, much of the apparent catalyst difference would be attributable to loading or conversion regime. The fixed catalyst-specific branching assumption in K1 would need to be weakened.
• If conversion changed little, Catalyst B would appear loading-saturated or limited by another factor. The strong concentration acceleration assumed in several blind predictions, especially Q01–Q06 and Q11–Q12, would become doubtful.
• If higher loading raised byproduct and reduced yield, Catalyst B would likely promote an additional catalyst-dependent side pathway.
• A large HPLC-to-final decline would favor post-formation degradation or termination-related change; close agreement would favor direct branching or stable products.

This one experiment would not completely separate concentration effects from absolute catalyst amount, but it would resolve the campaign’s largest deliberate design confound.

5. Tradeoff between identifiability and operating-score improvement

The campaign increasingly prioritized score optimization after the first seven batches. That choice was consistent with the stated primary goal of finding a strong safe operating procedure, but it reduced mechanistic identifiability.

The early catalyst and solvent screens sacrificed score for breadth. Batch 3, with score 0.06593, was particularly costly from an optimization perspective but informative in showing that a catalyst procedure could have both low activity and poor selectivity. Batches 5–7 also spent three batches mapping solvents instead of immediately increasing temperature in acetonitrile. Those were reasonable sacrifices for identifying categorical effects.

Conversely, Batches 8–12 concentrated heavily on Catalyst A/acetonitrile temperature and time. This was effective for raising the best score from 0.27425 to 0.33519, but five closely related batches left no capacity for exact replicates, catalyst-loading controls, stirring tests, concentration tests, or quench tests. Batches 9, 11, and 12 occupied a narrow local region and therefore improved local operating knowledge more than global mechanism knowledge.

The largest avoidable identifiability loss was using different catalyst amounts in Batches 1–4. A balanced catalyst screen at one loading would have been more interpretable. The largest optimization-driven compromise was the absence of replication near the apparent optimum. Once Batch 9 achieved 0.33446, replicating it might have been more scientifically valuable than treating Batch 11’s 0.33519 as a meaningful improvement.

There was also a score-versus-safety tradeoff. Water in Batch 5 had the lowest risk and cleanest impurity profile but a lower score than acetonitrile because of reduced conversion. The chosen program favored the higher-scoring acetonitrile path while still retaining a substantial margin below the 0.35 risk limit.

6. Underused evidence and weaknesses in the blind predictions

Several evidence streams were underused:

• The full characterization artifacts and raw synthetic spectra were not inspected. Only processed estimates were used, so peak shapes, saturation flags, missingness, or correlated channel behavior did not inform the model.
• Actual temperature increments and risk increments were observed after heat operations, but they were not fitted with a formal thermal-response model during the campaign. K1 proposed a first-order thermal lag qualitatively, yet its time constant and dependence on volume or composition remained unestimated.
• Intermediate HPLC and final-assay differences were noted but not modeled across batches. A joint observation model could have separated instrument noise from post-sampling process change.
• Cost saturated at 1.0 in every completed final assay, making cost variation unidentifiable. No low-charge experiment tested whether score could improve through reduced material use.
• No replicate was available to estimate process variance separately from instrument noise.

The sealed K1 report stated that the exact score equation was not identifiable from the 12 observations. In preparing the blind predictions, however, I found that all completed scores were consistent to numerical precision with:

score = -0.10 + 0.40×yield + 0.25×selectivity + 0.10×conversion - 0.45×safety_risk.

That later arithmetic observation could not modify the already sealed K1 report, but it shows that the scoring evidence had not been fully exploited at the reporting stage. It does not resolve the chemical mechanism; it only improves propagation from predicted assay channels and risk to score.

The least reliable blind prediction is Q12. It combines a 460 K target, 6300 s duration, a different Catalyst B concentration, much smaller vessel charge, and 400 rpm stirring. K1 explicitly said that claims above 390 K, beyond the studied catalyst loadings, at other concentrations, or at other stirring conditions were extrapolations. Although Q12 received broad intervals, the point estimates—conversion 1.0, selectivity 0.20, yield 0.18, and risk 0.24—depend heavily on an unvalidated thermal-degradation model. Even its safety interval of 0.15–0.38 may be too narrow if the high-temperature risk function has a threshold or runaway-like curvature.

Q04 and Q06 are also weak because they infer Catalyst B behavior during substantial exposure near 420–450 K from one Catalyst B experiment at 330 K. Their conversion intervals may be too narrow: Q04 used 0.93–1.00 and Q06 used 0.98–1.00 despite uncertain catalyst-loading scaling and thermal lag.

Q07 and Q08 are uncertain because no campaign experiment tested ordered multistep temperature histories. The prediction that the 450→390 K sequence would be slightly more damaging than 390→450 K was a model-based guess, not a demonstrated hysteresis law. Their relative ordering is less reliable than their individual intervals imply.

Q02 and Q10 are similarly weak because the campaign never used quench. Predicting them as nearly identical to Q01 and Q09 assumed that immediate termination already halted the relevant chemistry and that quenching did not change accumulated risk or assay recovery. That assumption was explicitly acknowledged in the prediction rationale, but the narrow differences between paired point estimates create a false impression of precision.

Q01, Q03, Q05, Q09, and Q11 also rely on an assumed acceleration from the higher Catalyst B concentration. Because catalyst-loading dependence was never measured, their conversion intervals could all be wider. This is consistent with K1’s declared limits, but the numerical prediction intervals did not always fully reflect those limits.

7. Limitations of the sealed recommendation

Batch 11 was the sample-internal maximum, not a proven optimum. Its observed score was 0.3351925, only about 0.00073 above Batch 9’s 0.3344619. That difference is far smaller than the observed HPLC-to-final variation and the declared assay noise scales. It is therefore inappropriate to claim that 375 K is demonstrably superior to 370 K.

The recommendation is limited by single observations per condition, one catalyst loading, one reagent amount, one solvent volume, one stirring speed, and one campaign world. Batch 11’s final risk of 0.2178 was safely below 0.35, but this does not establish the same risk margin under scale-up, altered thermal response, or another latent world realization.

Repeatability should be tested first with multiple exact replicates of Batch 11, including independent final assays and, ideally, the same intermediate HPLC timing. The relevant outputs would be the distribution of score, risk, conversion, yield, and selectivity—not merely the mean.

Local robustness should be tested with a small neighborhood around the recommendation: approximately 365, 370, 375, and 380 K; 6000, 6600, and 7200 s; and modest stirring perturbations. The goal would be to determine whether the broad plateau inferred from Batches 9, 11, and 12 is real and whether the risk response remains smooth.

Material robustness requires independent checks across catalyst loading and solvent identity. Water’s favorable safety and impurity behavior suggests that an optimized water procedure could potentially compete after adjusting time or temperature. Catalyst B–D should be retested at matched loading before declaring Catalyst A generally superior.

Cross-world generalization would require repeating the response-surface study in independently initialized benchmark worlds or seeds. Because the public materials are categorical latent profiles, success in this world does not prove that the same category ordering persists elsewhere.

The defensible conclusion is therefore: Batch 11 was the highest-scoring completed sample and is a reasonable representative of a promising 370–375 K operating region. It was not replicated, its advantage over Batch 9 was negligible relative to uncertainty, and neither global optimality nor transferability has been demonstrated.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 99.4 | none | 0 |
| Q | yes | 0 | 198.8 | none | 0 |
| K2 | yes | 0 | 104.0 | none | 0 |

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean 80% width | Mean interval score |
|---|---:|---:|---:|---:|
| byproduct_signal | 0.1357 | 0.4167 | 0.2583 | 0.4394 |
| conversion | 0.1422 | 0.3833 | 0.1879 | 0.8295 |
| safety_risk | 0.1989 | 0.0000 | 0.0943 | 1.4730 |
| score | 0.1208 | 0.4333 | 0.1821 | 0.6186 |
| selectivity | 0.1869 | 0.0167 | 0.2133 | 1.0493 |
| yield | 0.2739 | 0.0000 | 0.2462 | 1.8002 |

## Predictions versus released reference truth

### Q01

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4400 | 0.3100 | 0.5700 | 0.2826 | 0.2852, 0.2894, 0.2712, 0.2806, 0.2868 |
| conversion | 0.9400 | 0.8400 | 0.9900 | 0.9936 | 0.9944, 0.9886, 0.9985, 1.0000, 0.9865 |
| safety_risk | 0.0750 | 0.0450 | 0.1300 | 0.2975 | 0.2975, 0.2975, 0.2975, 0.2975, 0.2975 |
| score | 0.3060 | 0.2200 | 0.3900 | 0.3741 | 0.3745, 0.3704, 0.3762, 0.3731, 0.3761 |
| selectivity | 0.5500 | 0.4500 | 0.6400 | 0.7204 | 0.7250, 0.7175, 0.7148, 0.7117, 0.7328 |
| yield | 0.5200 | 0.4000 | 0.6200 | 0.7164 | 0.7143, 0.7102, 0.7240, 0.7179, 0.7156 |
### Q02

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4350 | 0.3050 | 0.5650 | 0.2861 | 0.2908, 0.2824, 0.2881, 0.2929, 0.2764 |
| conversion | 0.9400 | 0.8400 | 0.9900 | 0.9921 | 0.9993, 1.0000, 0.9838, 0.9912, 0.9863 |
| safety_risk | 0.0740 | 0.0400 | 0.1300 | 0.1512 | 0.1512, 0.1512, 0.1512, 0.1512, 0.1512 |
| score | 0.3080 | 0.2200 | 0.3950 | 0.4400 | 0.4421, 0.4407, 0.4410, 0.4418, 0.4345 |
| selectivity | 0.5550 | 0.4550 | 0.6450 | 0.7247 | 0.7349, 0.7269, 0.7271, 0.7216, 0.7132 |
| yield | 0.5250 | 0.4050 | 0.6250 | 0.7228 | 0.7198, 0.7212, 0.7257, 0.7294, 0.7176 |
### Q03

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3800 | 0.2700 | 0.5000 | 0.2305 | 0.2338, 0.2259, 0.2177, 0.2369, 0.2383 |
| conversion | 0.8500 | 0.7000 | 0.9400 | 0.9608 | 0.9596, 0.9490, 0.9674, 0.9626, 0.9652 |
| safety_risk | 0.0550 | 0.0350 | 0.1000 | 0.1854 | 0.1854, 0.1854, 0.1854, 0.1854, 0.1854 |
| score | 0.3010 | 0.2150 | 0.3800 | 0.4438 | 0.4466, 0.4474, 0.4404, 0.4439, 0.4408 |
| selectivity | 0.5800 | 0.4900 | 0.6700 | 0.7671 | 0.7763, 0.7752, 0.7648, 0.7603, 0.7591 |
| yield | 0.4900 | 0.3700 | 0.5900 | 0.7437 | 0.7453, 0.7506, 0.7349, 0.7477, 0.7399 |
### Q04

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5400 | 0.3900 | 0.6800 | 0.3349 | 0.3411, 0.3290, 0.3394, 0.3241, 0.3407 |
| conversion | 0.9880 | 0.9300 | 1.0000 | 0.9971 | 0.9964, 0.9936, 0.9975, 0.9981, 1.0000 |
| safety_risk | 0.1050 | 0.0650 | 0.1800 | 0.4031 | 0.4031, 0.4031, 0.4031, 0.4031, 0.4031 |
| score | 0.2600 | 0.1500 | 0.3500 | 0.2995 | 0.3030, 0.2973, 0.3051, 0.2950, 0.2974 |
| selectivity | 0.4800 | 0.3500 | 0.5900 | 0.6731 | 0.6859, 0.6698, 0.6734, 0.6614, 0.6750 |
| yield | 0.4700 | 0.3200 | 0.5800 | 0.6776 | 0.6782, 0.6748, 0.6911, 0.6732, 0.6704 |
### Q05

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1900 | 0.1000 | 0.3100 | 0.1390 | 0.1313, 0.1497, 0.1384, 0.1357, 0.1399 |
| conversion | 0.4600 | 0.3000 | 0.6500 | 0.8939 | 0.9038, 0.8951, 0.8931, 0.8821, 0.8954 |
| safety_risk | 0.0250 | 0.0120 | 0.0550 | 0.2972 | 0.2972, 0.2972, 0.2972, 0.2972, 0.2972 |
| score | 0.2080 | 0.1250 | 0.3000 | 0.4181 | 0.4209, 0.4187, 0.4150, 0.4146, 0.4214 |
| selectivity | 0.6300 | 0.5400 | 0.7100 | 0.8564 | 0.8553, 0.8572, 0.8540, 0.8567, 0.8586 |
| yield | 0.2900 | 0.1800 | 0.4200 | 0.7624 | 0.7676, 0.7631, 0.7562, 0.7563, 0.7688 |
### Q06

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5900 | 0.4500 | 0.7200 | 0.4142 | 0.4168, 0.4031, 0.4113, 0.4196, 0.4205 |
| conversion | 0.9990 | 0.9800 | 1.0000 | 0.9945 | 0.9842, 0.9940, 0.9980, 1.0000, 0.9961 |
| safety_risk | 0.1300 | 0.0800 | 0.2100 | 0.2972 | 0.2972, 0.2972, 0.2972, 0.2972, 0.2972 |
| score | 0.2170 | 0.1000 | 0.3200 | 0.2977 | 0.2966, 0.2960, 0.3021, 0.2986, 0.2951 |
| selectivity | 0.4300 | 0.2900 | 0.5600 | 0.6004 | 0.6005, 0.5997, 0.6043, 0.6057, 0.5920 |
| yield | 0.4200 | 0.2800 | 0.5500 | 0.6037 | 0.6035, 0.6000, 0.6114, 0.6014, 0.6020 |
### Q07

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4300 | 0.3000 | 0.5700 | 0.3184 | 0.3152, 0.3252, 0.3252, 0.3153, 0.3110 |
| conversion | 0.9000 | 0.7600 | 0.9800 | 0.9980 | 1.0000, 1.0000, 1.0000, 1.0000, 0.9902 |
| safety_risk | 0.0750 | 0.0450 | 0.1350 | 0.4275 | 0.4275, 0.4275, 0.4275, 0.4275, 0.4275 |
| score | 0.2830 | 0.1900 | 0.3700 | 0.3011 | 0.3054, 0.3035, 0.2994, 0.2993, 0.2978 |
| selectivity | 0.5400 | 0.4300 | 0.6400 | 0.6925 | 0.7058, 0.6881, 0.6972, 0.6796, 0.6920 |
| yield | 0.4800 | 0.3500 | 0.5900 | 0.6972 | 0.6993, 0.7056, 0.6895, 0.7005, 0.6912 |
### Q08

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4700 | 0.3300 | 0.6100 | 0.3216 | 0.3273, 0.3191, 0.3086, 0.3218, 0.3312 |
| conversion | 0.9200 | 0.7900 | 0.9900 | 0.9968 | 0.9991, 1.0000, 0.9973, 0.9961, 0.9914 |
| safety_risk | 0.0800 | 0.0480 | 0.1450 | 0.1975 | 0.1975, 0.1975, 0.1975, 0.1975, 0.1975 |
| score | 0.2740 | 0.1750 | 0.3650 | 0.4075 | 0.4073, 0.4070, 0.4041, 0.4125, 0.4069 |
| selectivity | 0.5200 | 0.4000 | 0.6300 | 0.7016 | 0.7006, 0.7052, 0.6910, 0.7046, 0.7067 |
| yield | 0.4700 | 0.3300 | 0.5900 | 0.6992 | 0.6986, 0.6948, 0.6970, 0.7099, 0.6957 |
### Q09

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2200 | 0.1200 | 0.3400 | 0.1517 | 0.1510, 0.1588, 0.1357, 0.1541, 0.1589 |
| conversion | 0.5200 | 0.3400 | 0.7100 | 0.9456 | 0.9443, 0.9462, 0.9392, 0.9438, 0.9543 |
| safety_risk | 0.0300 | 0.0150 | 0.0650 | 0.3768 | 0.3768, 0.3768, 0.3768, 0.3768, 0.3768 |
| score | 0.2220 | 0.1300 | 0.3150 | 0.3984 | 0.3958, 0.4013, 0.3970, 0.3990, 0.3989 |
| selectivity | 0.6200 | 0.5200 | 0.7100 | 0.8476 | 0.8351, 0.8618, 0.8575, 0.8339, 0.8498 |
| yield | 0.3200 | 0.2000 | 0.4500 | 0.7952 | 0.7969, 0.7935, 0.7871, 0.8057, 0.7929 |
### Q10

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2150 | 0.1150 | 0.3350 | 0.1532 | 0.1524, 0.1604, 0.1493, 0.1485, 0.1556 |
| conversion | 0.5200 | 0.3400 | 0.7100 | 0.9459 | 0.9443, 0.9377, 0.9581, 0.9487, 0.9408 |
| safety_risk | 0.0290 | 0.0140 | 0.0650 | 0.1712 | 0.1712, 0.1712, 0.1712, 0.1712, 0.1712 |
| score | 0.2240 | 0.1300 | 0.3200 | 0.4888 | 0.4881, 0.4857, 0.4916, 0.4910, 0.4875 |
| selectivity | 0.6250 | 0.5250 | 0.7150 | 0.8509 | 0.8547, 0.8603, 0.8394, 0.8540, 0.8458 |
| yield | 0.3230 | 0.2000 | 0.4550 | 0.7961 | 0.7925, 0.7846, 0.8071, 0.7989, 0.7972 |
### Q11

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4300 | 0.3100 | 0.5500 | 0.3207 | 0.3220, 0.3285, 0.3186, 0.3278, 0.3067 |
| conversion | 0.9680 | 0.8900 | 0.9950 | 0.9808 | 0.9709, 0.9777, 0.9940, 0.9742, 0.9873 |
| safety_risk | 0.0750 | 0.0450 | 0.1300 | 0.1548 | 0.1548, 0.1548, 0.1548, 0.1548, 0.1548 |
| score | 0.3350 | 0.2500 | 0.4050 | 0.4068 | 0.4034, 0.4056, 0.4113, 0.4075, 0.4063 |
| selectivity | 0.5900 | 0.5000 | 0.6700 | 0.6769 | 0.6720, 0.6683, 0.6786, 0.6851, 0.6803 |
| yield | 0.5600 | 0.4500 | 0.6500 | 0.6732 | 0.6701, 0.6762, 0.6801, 0.6713, 0.6682 |
### Q12

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.8200 | 0.6100 | 0.9600 | 0.5786 | 0.5786, 0.5797, 0.5783, 0.5826, 0.5738 |
| conversion | 1.0000 | 0.9900 | 1.0000 | 0.9966 | 0.9974, 0.9885, 0.9990, 0.9992, 0.9990 |
| safety_risk | 0.2400 | 0.1500 | 0.3800 | 0.4202 | 0.4202, 0.4202, 0.4202, 0.4202, 0.4202 |
| score | 0.0300 | 0.0000 | 0.1800 | 0.1418 | 0.1464, 0.1386, 0.1392, 0.1429, 0.1417 |
| selectivity | 0.2000 | 0.0500 | 0.3800 | 0.4511 | 0.4571, 0.4436, 0.4565, 0.4418, 0.4566 |
| yield | 0.1800 | 0.0300 | 0.3500 | 0.4475 | 0.4551, 0.4464, 0.4372, 0.4555, 0.4432 |

## Recommendation retest

- Selected source batch: `11`
- Retest exact replay verified: `True`
- Retest failure: `none`

| Metric | Selected source batch | Independent retest | Retest minus source |
|---|---:|---:|---:|
| byproduct_signal | 0.2929 | 0.2891 | -0.0038 |
| conversion | 0.9349 | 0.9437 | 0.0088 |
| cost | 1.0000 | 1.0000 | 0.0000 |
| degradation_warning | 0.1522 | 0.1460 | -0.0062 |
| safety_risk | 0.2178 | 0.2178 | 0.0000 |
| score | 0.3352 | 0.3326 | -0.0026 |
| selectivity | 0.7090 | 0.7011 | -0.0078 |
| virtual_spectrum_summary | 0.2296 | 0.2247 | -0.0048 |
| yield | 0.6562 | 0.6525 | -0.0037 |

## Scope note

This is the final sanitized report produced after all 60 source sessions and K1/Q/K2 chains were sealed. It includes released reference truth, blind-prediction evaluation, and the independent recommendation retest. Provider-private event streams, credentials, thread identifiers, and token accounting remain excluded.
