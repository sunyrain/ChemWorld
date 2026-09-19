# RX-W03--S--safety_constrained_optimization--MisIndexed

## Run summary

- World: `RX-W03`
- Locus: `S`
- Goal: `safety_constrained_optimization`
- Arm: `MisIndexed`
- Status: `completed`
- Source status: `completed`
- Experimental sessions: `12/12`
- Operations: `96`
- Exact replay verified: `True`
- Rollbacks: `[]`
- Posttest chain sealed: `True`

### Recovery status

No recovery override was required for this task.

## Sealed recommendation

- Selected batch: `2`
- Rationale: Batch 2 achieved the highest observed safe score (0.3860) while remaining comfortably below the 0.35 safety limit; it used water, Catalyst B, and a 390 K boundary target for 3600 s.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S0 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 330 K x 1800 s @ 600 rpm | yes | 0.0929 | 0.5924 | 0.1388 | 0.0615 | 0.0000 | 0.0825 | 0.0620 |
| 2 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 390 K x 3600 s @ 600 rpm | yes | 0.6841 | 0.7881 | 0.8519 | 0.1839 | 0.0914 | 0.1552 | 0.3860 |
| 3 | S0 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 390 K x 3600 s @ 600 rpm | yes | 0.5227 | 0.7285 | 0.7213 | 0.1953 | 0.0411 | 0.1373 | 0.3015 |
| 4 | S0 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 390 K x 3600 s @ 600 rpm | yes | 0.5129 | 0.7985 | 0.6588 | 0.1470 | 0.0368 | 0.1345 | 0.3102 |
| 5 | S1 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 390 K x 3600 s @ 600 rpm | yes | 0.6579 | 0.7106 | 0.9276 | 0.2679 | 0.1627 | 0.1818 | 0.3518 |
| 6 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 390 K x 3600 s @ 600 rpm | yes | 0.6064 | 0.6188 | 0.9706 | 0.3724 | 0.3109 | 0.2044 | 0.3023 |
| 7 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 390 K x 3600 s @ 600 rpm | yes | 0.5364 | 0.5754 | 0.9345 | 0.4308 | 0.2410 | 0.2065 | 0.2589 |
| 8 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 370 K x 7200 s @ 600 rpm | yes | 0.6332 | 0.6694 | 0.9446 | 0.3211 | 0.2118 | 0.1578 | 0.3441 |
| 9 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 400 K x 3000 s @ 600 rpm | yes | 0.6690 | 0.8062 | 0.8582 | 0.1688 | 0.0776 | 0.1560 | 0.3848 |
| 10 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 395 K x 3300 s @ 600 rpm | yes | 0.6761 | 0.8032 | 0.8459 | 0.1829 | 0.0906 | 0.1557 | 0.3858 |
| 11 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 405 K x 2700 s @ 600 rpm | yes | 0.6702 | 0.8126 | 0.8148 | 0.1597 | 0.0567 | 0.1560 | 0.3825 |
| 12 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 392 K x 3450 s @ 600 rpm | yes | 0.6640 | 0.7896 | 0.8561 | 0.1759 | 0.0966 | 0.1552 | 0.3788 |

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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 330
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
    "byproduct_signal": 0.061503443866968155,
    "conversion": 0.1388304978609085,
    "cost": 1.0,
    "degradation_warning": 0.0,
    "safety_risk": 0.08252952247858047,
    "score": 0.061990171670913696,
    "selectivity": 0.5923995971679688,
    "virtual_spectrum_summary": 0.03382689505815506,
    "yield": 0.09286376088857651
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
      "target_temperature_K": 390
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
    "byproduct_signal": 0.18386049568653107,
    "conversion": 0.8519247174263,
    "cost": 1.0,
    "degradation_warning": 0.09137695282697678,
    "safety_risk": 0.15523424744606018,
    "score": 0.38601937890052795,
    "selectivity": 0.7881419062614441,
    "virtual_spectrum_summary": 0.1422429084777832,
    "yield": 0.6841171383857727
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
      "target_temperature_K": 390
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
    "byproduct_signal": 0.19527292251586914,
    "conversion": 0.7213156223297119,
    "cost": 1.0,
    "degradation_warning": 0.04110172018408775,
    "safety_risk": 0.13725559413433075,
    "score": 0.30154308676719666,
    "selectivity": 0.7284513115882874,
    "virtual_spectrum_summary": 0.1258958876132965,
    "yield": 0.5226592421531677
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
      "target_temperature_K": 390
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
    "byproduct_signal": 0.14700037240982056,
    "conversion": 0.6587590575218201,
    "cost": 1.0,
    "degradation_warning": 0.03675001114606857,
    "safety_risk": 0.13449929654598236,
    "score": 0.31015416979789734,
    "selectivity": 0.7984994053840637,
    "virtual_spectrum_summary": 0.09738770872354507,
    "yield": 0.5129452347755432
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
      "target_temperature_K": 390
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
    "byproduct_signal": 0.2678900957107544,
    "conversion": 0.9276294708251953,
    "cost": 1.0,
    "degradation_warning": 0.16265858709812164,
    "safety_risk": 0.1818181872367859,
    "score": 0.3517504632472992,
    "selectivity": 0.7105802297592163,
    "virtual_spectrum_summary": 0.22053591907024384,
    "yield": 0.6579015851020813
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
    "byproduct_signal": 0.37243548035621643,
    "conversion": 0.9705527424812317,
    "cost": 1.0,
    "degradation_warning": 0.31086722016334534,
    "safety_risk": 0.20439787209033966,
    "score": 0.30234524607658386,
    "selectivity": 0.6188173890113831,
    "virtual_spectrum_summary": 0.34472978115081787,
    "yield": 0.6064116358757019
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
    "byproduct_signal": 0.43076616525650024,
    "conversion": 0.9345227479934692,
    "cost": 1.0,
    "degradation_warning": 0.24101191759109497,
    "safety_risk": 0.206522598862648,
    "score": 0.25893452763557434,
    "selectivity": 0.5753732919692993,
    "virtual_spectrum_summary": 0.34537675976753235,
    "yield": 0.5364352464675903
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
    "byproduct_signal": 0.32111358642578125,
    "conversion": 0.9445783495903015,
    "cost": 1.0,
    "degradation_warning": 0.21183931827545166,
    "safety_risk": 0.15781669318675995,
    "score": 0.3440685570240021,
    "selectivity": 0.6694296598434448,
    "virtual_spectrum_summary": 0.2719401717185974,
    "yield": 0.6331769824028015
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
      "duration_s": 3000,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 400
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
    "byproduct_signal": 0.16877053678035736,
    "conversion": 0.858212947845459,
    "cost": 1.0,
    "degradation_warning": 0.07757997512817383,
    "safety_risk": 0.15598425269126892,
    "score": 0.384797066450119,
    "selectivity": 0.8062148690223694,
    "virtual_spectrum_summary": 0.12773478031158447,
    "yield": 0.669037401676178
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
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 395
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
    "byproduct_signal": 0.18294169008731842,
    "conversion": 0.8458515405654907,
    "cost": 1.0,
    "degradation_warning": 0.0905967503786087,
    "safety_risk": 0.15570814907550812,
    "score": 0.3857506811618805,
    "selectivity": 0.803199827671051,
    "virtual_spectrum_summary": 0.1413864642381668,
    "yield": 0.6760855913162231
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
      "duration_s": 2700,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 405
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
    "byproduct_signal": 0.15972395241260529,
    "conversion": 0.8148205876350403,
    "cost": 1.0,
    "degradation_warning": 0.05665124952793121,
    "safety_risk": 0.15599264204502106,
    "score": 0.3825185298919678,
    "selectivity": 0.8125705718994141,
    "virtual_spectrum_summary": 0.11334123462438583,
    "yield": 0.6702262759208679
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
      "duration_s": 3450,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 392
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
    "byproduct_signal": 0.17585523426532745,
    "conversion": 0.8560972213745117,
    "cost": 1.0,
    "degradation_warning": 0.09655871987342834,
    "safety_risk": 0.1552283763885498,
    "score": 0.37875550985336304,
    "selectivity": 0.7895669937133789,
    "virtual_spectrum_summary": 0.14017179608345032,
    "yield": 0.6640170216560364
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

1. Scope and evidentiary basis

This report describes a bounded synthetic reaction-and-thermal world, not a named real reaction. Catalyst identities are anonymous, and the named solvents have categorical benchmark effects; therefore, I do not infer a real catalyst, substrate, product, or literature mechanism.

All 12 batches used 0.040 mol reagent, 0.080 L solvent, 0.005 mol catalyst, and 600 rpm stirring. Each heated batch was quenched before termination and final assay. Consequently, the conclusions apply primarily to those loadings, that mixing rate, single-stage heating, and the tested temperature/time region. Reported final-assay values are observations; kinetic interpretations are inferences.

2. Final-assay observations

Batch 1: water, Catalyst A, 330 K target, 1800 s. Conversion 0.1388, yield 0.0929, selectivity 0.5924, byproduct 0.0615, degradation warning 0.0000, final safety risk 0.0825, score 0.0620.

Batch 2: water, Catalyst B, 390 K, 3600 s. Conversion 0.8519, yield 0.6841, selectivity 0.7881, byproduct 0.1839, degradation 0.0914, final risk 0.1552, score 0.3860. This was the best observed score and the sealed recommendation.

Batch 3: water, Catalyst C, 390 K, 3600 s. Conversion 0.7213, yield 0.5227, selectivity 0.7285, byproduct 0.1953, degradation 0.0411, risk 0.1373, score 0.3015.

Batch 4: water, Catalyst D, 390 K, 3600 s. Conversion 0.6588, yield 0.5129, selectivity 0.7985, byproduct 0.1470, degradation 0.0368, risk 0.1345, score 0.3102.

Batch 5: ethanol, Catalyst B, 390 K, 3600 s. Conversion 0.9276, yield 0.6579, selectivity 0.7106, byproduct 0.2679, degradation 0.1627, risk 0.1818, score 0.3518.

Batch 6: acetonitrile, Catalyst B, 390 K, 3600 s. Conversion 0.9706, yield 0.6064, selectivity 0.6188, byproduct 0.3724, degradation 0.3109, risk 0.2044, score 0.3023.

Batch 7: toluene, Catalyst B, 390 K, 3600 s. Conversion 0.9345, yield 0.5364, selectivity 0.5754, byproduct 0.4308, degradation 0.2410, risk 0.2065, score 0.2589.

Batch 8: water, Catalyst B, 370 K, 7200 s. Conversion 0.9446, yield 0.6332, selectivity 0.6694, byproduct 0.3211, degradation 0.2118, risk 0.1578, score 0.3441.

Batch 9: water, Catalyst B, 400 K, 3000 s. Conversion 0.8582, yield 0.6690, selectivity 0.8062, byproduct 0.1688, degradation 0.0776, risk 0.1560, score 0.3848.

Batch 10: water, Catalyst B, 395 K, 3300 s. Conversion 0.8459, yield 0.6761, selectivity 0.8032, byproduct 0.1829, degradation 0.0906, risk 0.1557, score 0.3858.

Batch 11: water, Catalyst B, 405 K, 2700 s. Conversion 0.8148, yield 0.6702, selectivity 0.8126, byproduct 0.1597, degradation 0.0567, risk 0.1560, score 0.3825.

Batch 12: water, Catalyst B, 392 K, 3450 s. Conversion 0.8561, yield 0.6640, selectivity 0.7896, byproduct 0.1759, degradation 0.0966, risk 0.1552, score 0.3788.

3. Proposed process structure

The simplest explanation consistent with the results is a desired reaction running in parallel and/or sequence with undesired chemistry:

R ⇌ P
R → B
P → B or D

Here R is the public reactant, P the desired target, B one or more ordinary byproducts, and D thermally accumulated degradation material. A minimal kinetic representation is:

dR/dt = -kf(T,C,S)R + kr(T,C,S)P - kb,R(T,C,S)R

dP/dt = kf(T,C,S)R - kr(T,C,S)P - kb,P(T,C,S)P

dB/dt = kb,R R + kb,P P

where C is catalyst category and S is solvent category. Temperature-dependent rate constants could follow effective Arrhenius relationships, k_i = A_i(C,S) exp[-E_i(C,S)/(RT)]. These equations are illustrative rather than fitted: the dataset is insufficient to identify individual rate constants.

The supplied prior suggested an appreciable reverse target channel. The experiments are compatible with that claim, particularly the diminishing benefit of extra residence time, but they do not uniquely demonstrate reversibility. Sequential product degradation or a time-dependent loss of selectivity can reproduce the same endpoint behavior.

Observed yield was generally close to conversion multiplied by selectivity, within expected assay/process variation. This supports interpreting conversion as total reacted fraction and selectivity as allocation of reacted material toward the desired product, rather than treating yield as an independent state.

4. Catalyst effects

Batches 2–4 isolate catalyst category at water/390 K/3600 s. Catalyst B produced the highest conversion and yield: 0.8519 and 0.6841, versus 0.7213/0.5227 for C and 0.6588/0.5129 for D. Catalyst D gave slightly higher measured selectivity than B, 0.7985 versus 0.7881, and less byproduct and degradation, but its lower turnover limited yield. Thus, I infer that Catalyst B has the largest effective forward activity under these conditions, while Catalyst D is slower but comparatively discriminating.

Catalyst A cannot be ranked fairly. It was tested only in Batch 1 at 330 K for 1800 s, where low conversion could result mainly from mild thermal exposure rather than weak catalyst activity. Any statement that A is intrinsically inferior would be an unsupported extrapolation.

5. Solvent coupling

Batches 2 and 5–7 isolate solvent category with Catalyst B at 390 K for 3600 s. Moving from water to ethanol, acetonitrile, or toluene increased conversion but progressively reduced selectivity and increased byproduct burden. Water gave conversion 0.8519, selectivity 0.7881, and byproduct 0.1839. Ethanol gave 0.9276, 0.7106, and 0.2679; acetonitrile gave 0.9706, 0.6188, and 0.3724; toluene gave 0.9345, 0.5754, and 0.4308.

I therefore infer that the non-water solvents accelerate overall disappearance of reactant more than they favor the desired channel. Their apparent kinetic benefit is counteracted by worse partitioning into product and greater degradation. Water is not the fastest medium, but it provides the best balance of forward reaction, selectivity, thermal behavior, and safety.

Solvent also coupled to thermal risk. At the end of heating, observed risk was 0.1998 for water in Batch 2, compared with 0.2263 for ethanol, 0.2487 for acetonitrile, and 0.2509 for toluene. After quenching, final risks fell to 0.1552, 0.1818, 0.2044, and 0.2065, respectively. This suggests a solvent-specific baseline or thermal-risk coefficient in addition to temperature itself.

6. Temperature–residence-time tradeoff

The water/Catalyst B series, Batches 2 and 8–12, is the strongest evidence for the operating mechanism. A low-temperature but long exposure in Batch 8 (370 K, 7200 s) drove conversion to 0.9446, yet selectivity declined to 0.6694, byproduct rose to 0.3211, and degradation to 0.2118. Its yield, 0.6332, was below Batch 2 despite higher conversion. Thus, maximizing conversion is not equivalent to maximizing desired product or score.

Shorter, hotter treatments in Batches 9–11 produced lower conversion but better selectivity and less degradation. Across 400 K/3000 s, 395 K/3300 s, and 405 K/2700 s, yield stayed near 0.669–0.676 while selectivity rose from 0.8062 to 0.8126 as duration shortened. Batch 11 had the lowest conversion of this group, 0.8148, but also the lowest degradation warning, 0.0567.

This pattern suggests that desired formation is fast enough at high temperature to obtain useful yield during a short exposure, whereas accumulated byproduct/degradation depends strongly on residence time after substantial conversion. A conceptual control rule is therefore:

heat rapidly enough to reach the productive kinetic regime;
stop before extended residence converts reactant or product into undesired material;
quench promptly to suppress further reaction and reduce thermal risk.

The observed optimum is broad rather than sharp. Batches 2, 9, 10, and 11 scored 0.3860, 0.3848, 0.3858, and 0.3825. Differences of only a few thousandths may partly reflect assay/process noise. I would regard approximately 390–400 K for 3000–3600 s as an empirically supported high-performing region, not claim that exactly 390 K and 3600 s is a universal mathematical optimum.

7. Thermal dynamics and safety

The achieved temperature did not instantaneously equal the boundary target. Reported temperature increases during heating were approximately 83.1 K in Batch 2, 66.2 K in Batch 8, 91.3 K in Batch 9, 87.2 K in Batch 10, 95.4 K in Batch 11, and 84.8 K in Batch 12. Assuming the common starting region near ambient, these are consistent with finite thermal approach rather than perfect target tracking.

A plausible lumped thermal model is:

dT/dt = (Tset - T)/tau(S,V,rpm) + Qrxn/(rho V Cp) - Qloss/(rho V Cp).

Safety risk appears to increase with solvent loading, reagent/catalyst setup, and especially hot-state temperature, then decrease on quenching. All final and hot-state values observed here remained below the declared 0.35 limit; the largest observed heating-stage risk was about 0.251 in Batch 7. However, no experiments approached the 470 K action boundary, so safety beyond the tested region must not be extrapolated linearly.

8. Instrument consistency

Intermediate HPLC and final-assay results generally agreed in direction and approximate magnitude. For example, Batch 2 HPLC gave conversion 0.8624, yield 0.6606, selectivity 0.7657, and byproduct 0.1883; its final assay gave 0.8519, 0.6841, 0.7881, and 0.1839. Batch 9 HPLC yield was 0.6625 versus final yield 0.6690. Batch 12 HPLC yield was 0.6705 versus final yield 0.6640. These differences caution against interpreting small score or composition differences as exact kinetic effects. Quenching, sampling, and independent measurement noise are all plausible contributors.

9. What changed my interpretation

Batch 1 initially established that mild heating gave little conversion or yield. Batch 2 showed that substantially stronger heating with Catalyst B could enter a high-yield regime without violating the safety limit. Batches 3–4 then separated catalyst activity from thermal exposure and identified the activity/selectivity tradeoff among B, C, and D.

Batches 5–7 materially changed the interpretation of solvent effects: higher conversion in ethanol, acetonitrile, and toluene did not improve performance because selectivity and degradation worsened. This made water the preferred medium despite its lower conversion.

Batch 8 was the clearest evidence against a simple “more time gives more product” model. Its very high conversion but inferior yield and score motivated the competing/degradation-channel interpretation. Batches 9–11 supported the corresponding short-hot strategy, while Batch 12 showed that nearby conditions can fluctuate and that the optimum should be treated as a region.

10. Unidentified factors and competing explanations

The data cannot separately identify reverse reaction, direct reactant-to-byproduct chemistry, product degradation, catalyst deactivation, or equilibrium limitation. Several can coexist. The apparent time penalty could also arise from catalyst aging or solvent-dependent assay response rather than only product destruction.

There were no systematic variations in reagent concentration, catalyst loading, liquid volume, stirring speed, addition order, staged heating, cooling rate, or replicate count. Their effects and interactions remain unidentified. Because each categorical condition had essentially one independent batch, process variability is confounded with treatment effects. Catalyst A is especially underdetermined.

No full temperature-time traces or species-resolved concentration trajectories were measured, so the proposed differential equations are structural hypotheses, not parameterized laws. Exact Arrhenius constants, equilibrium constants, heat-transfer coefficients, reaction enthalpy, and score formula cannot be recovered from these endpoint observations.

Within the experimentally supported domain, the most defensible operational picture is: Catalyst B in water provides the best activity/selectivity compromise; temperature accelerates productive conversion, but excessive residence accumulates byproduct or loses product through degradation/reversal; non-water solvents promote reactant disappearance while disproportionately strengthening undesired channels and risk; and prompt quenching preserves the favorable endpoint. Batch 2 is the strongest single observed realization of that balance.

## Q — Blind predictions

### Overall rationale

Predictions were extrapolated from the observed Catalyst B/acetonitrile batch and the water temperature–time series. Effective reaction exposure was assumed to increase with catalyst-to-reagent ratio, temperature, and residence time, while prolonged exposure drives secondary conversion or product degradation. Yield was constrained to remain approximately conversion multiplied by selectivity, and byproduct signal was tied to the converted fraction not retained as target. Quenching was treated primarily as a thermal-risk intervention because the campaign showed little systematic compositional change across quench and final assay. The score estimates use the relationship identified exactly across the 12 completed batches: score approximately equals max(0, -0.10 + 0.40·yield + 0.25·selectivity + 0.10·conversion - 0.45·safety_risk). Intervals are deliberately broad because the new batches change concentration, catalyst fraction, stirring rate, omit quenching in most cases, and include 465 K and four-hour exposures outside the experimentally tested domain.

### Q01

Low catalyst loading and short residence time should limit conversion despite the 410 K target. Acetonitrile should accelerate total reactant loss but favor more byproduct than water. The lack of quenching leaves appreciable thermal risk.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1510 | 0.0700 | 0.3200 |
| conversion | 0.5600 | 0.3400 | 0.7600 |
| safety_risk | 0.3000 | 0.2200 | 0.4000 |
| score | 0.1670 | 0.0600 | 0.2900 |
| selectivity | 0.7300 | 0.5800 | 0.8400 |
| yield | 0.4090 | 0.2200 | 0.5900 |

### Q02

Four hours at 410 K should compensate for the low catalyst loading and nearly exhaust the reactant. Extrapolation from the long-residence and acetonitrile batches indicates severe secondary reaction or product degradation, so high conversion is not expected to give high yield.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7900 | 0.5900 | 0.9600 |
| conversion | 0.9980 | 0.9500 | 1.0000 |
| safety_risk | 0.3800 | 0.2900 | 0.5100 |
| score | 0.0000 | 0.0000 | 0.1200 |
| selectivity | 0.2000 | 0.0400 | 0.4000 |
| yield | 0.2000 | 0.0400 | 0.4000 |

### Q03

The high catalyst-to-reagent ratio should produce high conversion during the short treatment. Short residence limits degradation relative to the long treatments, although acetonitrile still imposes a substantial byproduct penalty.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3070 | 0.1600 | 0.5000 |
| conversion | 0.9300 | 0.7900 | 0.9950 |
| safety_risk | 0.3200 | 0.2300 | 0.4400 |
| score | 0.2660 | 0.1300 | 0.4000 |
| selectivity | 0.6700 | 0.5000 | 0.8000 |
| yield | 0.6230 | 0.4000 | 0.7900 |

### Q04

High catalyst loading combined with four hours at 410 K lies far beyond the measured productive exposure. Conversion should saturate, but most converted material is expected to enter byproduct or degradation channels. No quench also raises the final risk.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9200 | 0.7300 | 1.0000 |
| conversion | 1.0000 | 0.9850 | 1.0000 |
| safety_risk | 0.4200 | 0.3100 | 0.5600 |
| score | 0.0000 | 0.0000 | 0.0600 |
| selectivity | 0.0700 | 0.0000 | 0.2200 |
| yield | 0.0700 | 0.0000 | 0.2200 |

### Q05

At 350 K the low catalyst loading should make reaction relatively slow even over two hours. The mild temperature should preserve selectivity and keep risk low, but incomplete conversion limits yield.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1540 | 0.0600 | 0.3300 |
| conversion | 0.5500 | 0.3000 | 0.7800 |
| safety_risk | 0.1600 | 0.1000 | 0.2400 |
| score | 0.2210 | 0.1000 | 0.3500 |
| selectivity | 0.7200 | 0.5600 | 0.8400 |
| yield | 0.3960 | 0.2000 | 0.6000 |

### Q06

The 465 K, two-hour exposure is a strong extrapolation beyond the campaign. Even with low catalyst loading, it should give essentially complete conversion accompanied by extensive thermal degradation, dominant byproduct signal, and a likely safety-limit violation.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9500 | 0.7800 | 1.0000 |
| conversion | 1.0000 | 0.9700 | 1.0000 |
| safety_risk | 0.6200 | 0.4600 | 0.8000 |
| score | 0.0000 | 0.0000 | 0.0300 |
| selectivity | 0.0400 | 0.0000 | 0.1600 |
| yield | 0.0400 | 0.0000 | 0.1600 |

### Q07

High catalyst loading should largely overcome the low 350 K rate and deliver high conversion. Secondary chemistry accumulated over two hours should reduce selectivity, but the mild temperature makes this substantially less destructive than the corresponding 465 K treatment.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3690 | 0.2000 | 0.5500 |
| conversion | 0.9700 | 0.8500 | 1.0000 |
| safety_risk | 0.1700 | 0.1100 | 0.2600 |
| score | 0.3160 | 0.2000 | 0.4300 |
| selectivity | 0.6200 | 0.4600 | 0.7500 |
| yield | 0.6010 | 0.4100 | 0.7600 |

### Q08

This combines the highest catalyst loading, highest temperature, and long residence time. The model therefore predicts saturated conversion but almost complete loss of desired product to secondary pathways, with very high unquenched risk.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9850 | 0.8800 | 1.0000 |
| conversion | 1.0000 | 0.9900 | 1.0000 |
| safety_risk | 0.7200 | 0.5300 | 0.9000 |
| score | 0.0000 | 0.0000 | 0.0100 |
| selectivity | 0.0100 | 0.0000 | 0.0800 |
| yield | 0.0100 | 0.0000 | 0.0800 |

### Q09

At intermediate catalyst loading, two hours at 410 K should nearly exhaust the reagent but permit substantial product loss and byproduct formation. Because the batch is not quenched, its hot-state risk is expected to be close to or slightly above the declared limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6400 | 0.4500 | 0.8200 |
| conversion | 0.9950 | 0.9600 | 1.0000 |
| safety_risk | 0.3600 | 0.2700 | 0.4800 |
| score | 0.0660 | 0.0000 | 0.1700 |
| selectivity | 0.3500 | 0.1800 | 0.5400 |
| yield | 0.3500 | 0.1800 | 0.5400 |

### Q10

This is compositionally the same treatment as Q09, so termination after quenching should leave conversion, yield, selectivity, and byproduct signal nearly unchanged. The quench is predicted to reduce thermal risk and consequently improve the score.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6400 | 0.4500 | 0.8200 |
| conversion | 0.9950 | 0.9600 | 1.0000 |
| safety_risk | 0.2900 | 0.2000 | 0.3900 |
| score | 0.0970 | 0.0100 | 0.2000 |
| selectivity | 0.3500 | 0.1800 | 0.5400 |
| yield | 0.3500 | 0.1800 | 0.5400 |

### Q11

The four-hour duration should yield nearly complete conversion even at 350 K. The lower temperature suppresses instantaneous thermal risk, but the very long residence should still accumulate substantial secondary chemistry and reduce yield below the shorter mild-temperature case.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5740 | 0.3600 | 0.7700 |
| conversion | 0.9900 | 0.9100 | 1.0000 |
| safety_risk | 0.1800 | 0.1100 | 0.2800 |
| score | 0.1890 | 0.0700 | 0.3100 |
| selectivity | 0.4200 | 0.2300 | 0.6200 |
| yield | 0.4160 | 0.2200 | 0.6200 |

### Q12

A short 465 K treatment should reach almost complete conversion rapidly. Its shorter duration preserves more desired product than Q06 or Q08, but the high temperature still favors byproduct formation and creates a strong unquenched safety penalty.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5470 | 0.3400 | 0.7700 |
| conversion | 0.9950 | 0.9400 | 1.0000 |
| safety_risk | 0.5800 | 0.4100 | 0.7600 |
| score | 0.0300 | 0.0000 | 0.1500 |
| selectivity | 0.4500 | 0.2300 | 0.6500 |
| yield | 0.4480 | 0.2200 | 0.6500 |

## K2 — Retrospective analysis

1. Assessment of the initial claims

The initial material packet contained one substantive mechanistic prior: “The target pathway may have an appreciable reverse channel on the public support,” with moderate confidence. It also stated important interpretive limitations: catalysts were anonymous benchmark formulations, solvent effects were categorical benchmark effects, and no task-specific property dossier was supplied.

The reverse-channel prior was supported only indirectly, not established. In K1 I represented it as the reversible step R ⇌ P while explicitly noting that the data did not identify kr separately. Batch 8 was the most relevant observation: water/Catalyst B at 370 K for 7200 s reached conversion 0.9446 but only yield 0.6332 and selectivity 0.6694, compared with Batch 2 at 390 K for 3600 s, which had lower conversion, 0.8519, but higher yield, 0.6841, and selectivity, 0.7881. That is compatible with prolonged exposure removing target product or returning it toward reactant. It is not specific evidence for reversibility because sequential product degradation, catalyst aging, or additional parallel chemistry can produce the same endpoint pattern.

There was no direct counterexample demonstrating that a reverse channel was absent. Equally, “no decisive counterexample” must not be confused with confirmation. Conversion did not visibly decrease in the longer experiment; instead, conversion increased while yield and selectivity deteriorated. Taken literally, that pattern is more immediately suggestive of product-to-byproduct degradation than of simple P → R reversal. K1 acknowledged this by saying that “sequential product degradation or a time-dependent loss of selectivity can reproduce the same endpoint behavior.” I did not retain the reverse hypothesis uncritically, but I also did not have sufficient observations to reduce it below a plausible competing explanation.

The packet’s warning against assigning real chemical identities was respected. Nothing in the campaign tested whether water, ethanol, acetonitrile, or toluene behaved according to real-world physical-property trends, and no result licenses identifying Catalyst B as a real catalyst. The claim that experimental evidence was authoritative was borne out operationally: solvent and catalyst effects had to be learned empirically. No initial claim about rate laws, activation energies, catalyst ranking, or the optimum operating point was supplied, so those conclusions arose from the campaign rather than from the initial packet.

2. Experiments that formed or changed the interpretation

Batch 1 was an exploratory mild baseline rather than a strong test of the initial reverse-channel claim. Its water/Catalyst A treatment at 330 K for 1800 s produced conversion 0.1388 and yield 0.0929. It established that this level of exposure was inadequate, but because both catalyst and thermal exposure differed from later batches, it did not establish that Catalyst A was weak. K1 correctly warned that A could not be ranked fairly.

Batch 2 was the first decisive operational result. Water/Catalyst B at 390 K for 3600 s produced conversion 0.8519, yield 0.6841, score 0.3860, and final risk 0.1552. It changed the working view from “the reaction may simply be sluggish” to “a productive, safe high-conversion window exists.” The choice of 390 K and 3600 s was initially a largely unvalidated escalation from Batch 1, informed by general kinetic reasoning rather than by identified parameters.

Batches 3 and 4 were genuine controlled comparisons because they changed catalyst while holding water, 390 K, and 3600 s fixed. They established that Catalyst B had greater apparent activity than C or D under those conditions. They also revealed an activity–selectivity tradeoff: D had selectivity 0.7985, slightly above B’s 0.7881, but much lower conversion and yield. These batches formed the catalyst interpretation in K1 rather than merely confirming a prior assumption.

Batches 5–7 materially changed the solvent interpretation. At otherwise matched Catalyst B/390 K/3600 s conditions, ethanol, acetonitrile, and toluene raised conversion relative to water but lowered selectivity and increased byproduct signal. Before those experiments, it would have been reasonable but untested to equate faster disappearance of reagent with improvement. The results refuted that simple optimization heuristic. They led directly to the K1 judgment that water was “not the fastest medium” but had the best balance of activity, selectivity, degradation, and safety.

Batch 8 was the strongest mechanism-oriented experiment. The 370 K/7200 s condition was deliberately different from the short, hotter region. Its high conversion but worse yield, selectivity, byproduct signal, and degradation warning changed the interpretation from a predominantly forward-conversion model to one requiring accumulated secondary chemistry, reversal, or both. It also demonstrated that conversion alone was a misleading optimization target.

Batches 9–12 primarily refined operating performance around the Batch 2 region. They supported K1’s “short-hot strategy” and the statement that the optimum was broad rather than sharp. However, temperature and duration were changed together—400 K/3000 s, 395 K/3300 s, 405 K/2700 s, and 392 K/3450 s—so these batches did not independently identify the effects of temperature and time. Their design was guided by accumulated campaign data and the guess that approximately matched thermal exposure could preserve yield while limiting degradation.

Several important choices remained assumptions rather than tested conclusions. Every batch used the maximum common recipe of 0.040 mol reagent, 0.080 L solvent, and 0.005 mol catalyst, and every heated batch used 600 rpm. Consequently, the campaign never tested whether the apparent optimum depended on concentration, catalyst fraction, volume, or mixing. Prompt quenching was used consistently and seemed favorable from risk readouts, but no matched quenched/unquenched compositional comparison was run during the campaign.

3. Current competing mechanisms and what the evidence distinguishes

K1 proposed the schematic network R ⇌ P, R → B, and P → B or D. The most important competition is between three explanations for the loss of selectivity at long exposure:

(a) Reversible desired chemistry: P returns to R through P → R.

(b) Sequential degradation: P is converted irreversibly into B or D.

(c) Time-dependent parallel chemistry: remaining R increasingly enters R → B, possibly because of catalyst-state changes, thermal history, or changing composition.

The present data distinguish a simple one-step irreversible R → P model from this broader class. A simple model predicts that additional exposure should monotonically increase or plateau product yield without the pronounced deterioration seen in Batch 8 and in the non-water solvent series. It cannot naturally explain why conversion increased while selectivity and yield became worse.

The data do not cleanly distinguish (a), (b), and (c). Batch 8’s increased conversion argues somewhat more directly for degradation or parallel byproduct formation than for pure reversal, because a dominant P → R process would tend to restore reactant and reduce apparent conversion. But a reversible system with simultaneous irreversible removal, changing equilibrium, or assay uncertainty could still give the observed endpoint. The degradation-warning channel supports explanation (b), especially its value of 0.2118 in Batch 8 and 0.3109 in the acetonitrile Batch 6, but this channel is a synthetic aggregate rather than a species-resolved mass balance.

A second competition is whether solvent primarily changes intrinsic reaction selectivity or instead changes temperature history, catalyst state, or measurement response. Batches 2 and 5–7 show reproducible-looking categorical differences at matched nominal controls, so they establish a solvent-associated effect. They do not identify its microscopic origin. Similarly, Batches 2–4 distinguish catalyst formulations operationally but cannot tell whether B increases kf, suppresses kr, changes branching to B, or merely maintains activity longer.

A third ambiguity concerns the temperature–time relationship. Batches 9–11 are consistent with faster productive reaction at higher temperature and greater damage from residence time. Because temperature and duration covaried, they cannot establish whether temperature itself suppresses degradation relative to desired reaction or whether the advantage came entirely from shorter duration. Finite temperature approach further confounds nominal setpoint with actual integrated exposure.

Finally, small score differences cannot be separated from process and assay noise. Batch 2 scored 0.386019, while Batch 10 scored 0.385751—a difference of only about 0.00027. That is far below a defensible mechanistic resolution given the observed HPLC/final-assay differences. The data distinguish a productive region from poor regions, but not an exact ranking among the best neighboring conditions.

4. The single additional complete experiment I would choose

I would choose a within-batch extension experiment anchored to the recommended chemistry:

- 0.080 L water
- 0.040 mol reagent
- 0.005 mol Catalyst B
- 600 rpm
- heat at a 390 K target for 3600 s
- make an HPLC measurement at 3600 s
- continue heating at 390 K for another 3600 s
- make a second HPLC measurement if the legal measurement allowance permits it; otherwise proceed directly
- quench, terminate, and perform the required final assay at 7200 s

This is preferable to another unrelated endpoint because the 3600 s state has a direct historical reference in Batch 2, while the extended state tests the fate of already formed target within the same vessel and catalyst/solvent context. A single intermediate HPLC followed by final assay would still have cross-instrument uncertainty, so a second HPLC immediately before quenching would be valuable if legal resources allowed it.

Possible results would change the interpretation as follows:

- If target yield and selectivity fall while conversion remains constant or rises and byproduct/degradation signals increase, sequential P → B/D degradation would become the leading explanation.

- If yield falls and apparent conversion also falls, indicating reappearance of reactant, the R ⇌ P hypothesis would receive much stronger direct support.

- If conversion, yield, and selectivity all remain nearly constant, the Batch 8 result would more likely involve a temperature-specific pathway, run-to-run variation, or solvent/catalyst-state effects rather than a general residence-time penalty at 390 K.

- If yield continues to rise substantially with little selectivity loss, Batch 2 would appear to have been stopped early, and the inferred optimum residence time would shift later.

- If both conversion and byproduct increase while target yield plateaus, parallel R → B chemistry would be favored over pure product degradation.

This one experiment would not fully identify rate constants, but it would be more discriminating than another single final endpoint because it creates a temporal contrast within one physical batch.

5. Tradeoff between mechanistic identifiability and score optimization

The research goal emphasized strong safe-score performance, so the campaign increasingly favored optimization after an initial categorical screen. Batches 2–7 used controlled comparisons that served both purposes: they found the superior catalyst/solvent combination while identifying large categorical effects. Those experiments sacrificed some immediate score—especially the acetonitrile and toluene batches—in exchange for learning which media increased conversion at the cost of selectivity.

Batch 8 was the clearest case of sacrificing expected score for mechanistic information. A 7200 s treatment was not obviously attractive after Batch 2, but it tested whether lower temperature and longer time could maintain conversion more safely. Its inferior score of 0.3441 was informative because it exposed the accumulated secondary channel.

Batches 9–12 shifted toward score refinement. Their coupled temperature/time changes sampled a presumed iso-exposure ridge and repeatedly delivered scores near 0.38. This was efficient for locating a robust operating region, but weak for mechanistic identifiability. A factorial design changing temperature at fixed duration and duration at fixed temperature would have separated those effects more cleanly. Likewise, repeating Batch 2 would have estimated variance, while changing catalyst loading or concentration would have tested the assumed rate dependence. Those experiments were not chosen because the remaining batches were used to search locally for a higher score.

There was also an opposite sacrifice: the early catalyst and solvent screens used only one batch per category, so they provided breadth at the cost of replication. This was rational for a 12-batch campaign but means category rankings are not supported by independent variance estimates. Keeping all recipes at maximum common loading simplified optimization and conserved comparability, yet made the mechanism poorly identifiable with respect to concentration and catalyst order.

Thus, the campaign found a useful operating region, but it did so partly by treating catalyst loading, concentration, and stirring as fixed nuisance variables rather than scientifically identifiable variables.

6. Underused evidence and weaknesses in the blind predictions

The most underused evidence was the public raw characterization data. I used processed HPLC and final-assay estimates but did not inspect and model the full spectral artifacts, peak assignments, calibration flags, mass-balance information, or replicate-level signals. Those records might have helped distinguish reactant reappearance from growth of a new degradation feature, or at least quantified measurement quality.

The paired intermediate-HPLC and final-assay values were also not used quantitatively enough. For example, Batch 2 moved from HPLC yield 0.6606 to final-assay yield 0.6841, while Batch 12 moved from 0.6705 to 0.6640. These paired differences could have informed a measurement-error model. Instead, K1 described them qualitatively as approximate agreement.

The temperature-change and pre-/post-quench risk data were likewise only partially exploited. The campaign contained repeated evidence that quenching reduced observed risk, with the magnitude depending on the hot condition and solvent. A fitted thermal/risk model could have improved the Q09-versus-Q10 prediction. Actual temperature histories were unavailable, but the reported endpoint temperature changes could still have constrained thermal lag more systematically.

The least reliable blind predictions are Q04, Q06, Q08, and Q12 because they extrapolate to 465 K or combine long residence with catalyst fractions outside the campaign. Q02 is also highly uncertain because it extends a low-catalyst acetonitrile batch to four hours. No campaign experiment used 465 K, 14400 s, 400 rpm, a 0.005 L volume, 0.003 mol reagent, or those catalyst-to-reagent ratios. The assumptions that catalyst effect scaled monotonically with relative loading and that degradation dominated at extreme exposure were mechanistically plausible but unverified.

Several intervals in Q were probably too narrow. In particular, Q08 assigned score 0.0 with an 80% upper bound of only 0.01, Q06 used an upper bound of 0.03, and Q04 used 0.06. Those bounds express excessive confidence that extreme exposure destroys nearly all target. A different simulator structure—rapid equilibrium with a nonzero target plateau, catalyst deactivation that protects product, strong thermal lag, or saturation of degradation—could yield materially higher selectivity and score. Q12’s yield/selectivity and risk intervals may also be too narrow because a short 465 K ramp could behave very differently depending on heat-transfer dynamics.

The Q09/Q10 prediction treated quenching as leaving composition essentially unchanged while lowering risk. That was consistent with the campaign protocol and small HPLC/final differences, but it was not tested by a matched quenched/unquenched pair. Its compositional intervals should therefore have allowed more divergence.

These weaknesses are in tension with K1’s explicit scope limitations. K1 said the conclusions applied primarily to fixed maximum loadings, 600 rpm, single-stage heating, and the tested temperature/time region, and warned against extrapolating safety beyond that region. The Q rationales acknowledged that the new conditions were outside this domain, but some numerical intervals—especially the near-zero score bounds at extreme conditions—were more confident than that warning justified. The point predictions can be defended as conditional extrapolations; the narrowest intervals cannot.

One element of the score prediction was comparatively well supported: the completed batches revealed the exact empirical relationship score ≈ max(0, -0.10 + 0.40·yield + 0.25·selectivity + 0.10·conversion - 0.45·safety risk). However, knowing the score mapping does not reduce uncertainty in the underlying chemical and risk metrics. At the extrapolative Q conditions, score uncertainty should inherit their broad joint uncertainty and possible correlations.

7. Limitations of the sealed recommendation

The recommendation of Batch 2 is the sample-best completed procedure, not a proven optimum. Its observed score of 0.386019 was the highest among the 12 completed batches, but Batch 10 scored 0.385751 and Batch 9 scored 0.384797. Those differences are negligible relative to plausible process and assay variability. K1 appropriately described approximately 390–400 K for 3000–3600 s as a high-performing region and stated that exactly 390 K/3600 s was not a universal mathematical optimum.

Batch 2 was not replicated. Its final-assay result could contain favorable random variation, and its HPLC estimate was not identical to its final assay. The recommendation also depends on the fixed recipe: 0.080 L water, 0.040 mol reagent, 0.005 mol Catalyst B, 600 rpm, one 390 K heating stage for 3600 s, followed by prompt quenching. It has not been shown robust to catalyst loading, concentration, scale, mixing, addition order, temperature overshoot, or delayed quenching.

Repeatability should first be tested with several independently randomized exact replicates of Batch 2, including identical measurements and recorded temperature histories. A variance estimate should precede claims that it outperforms Batches 9–11.

Local robustness should then be evaluated with a structured response-surface design around the promising region—for example, independently varying temperature near 385, 390, 395, and 400 K and duration near 3000, 3300, 3600, and 3900 s, with center-point replication. Catalyst loading and stirring should subsequently be perturbed one variable at a time or in a small factorial design. Deliberate short quench delays would quantify operational sensitivity without immediately entering unsafe territory.

Cross-material generalization requires repeating the local design with other catalyst and solvent categories rather than assuming the same optimum. Catalyst D’s lower activity but favorable selectivity suggests it could respond differently to a longer or hotter treatment. Catalyst A remains essentially uncharacterized because its only batch used different thermal conditions.

Cross-world generalization is even more limited. The catalysts are anonymous benchmark formulations and the solvents have environment-specific categorical couplings. The result does not support a claim that a real reaction in water with an unspecified real catalyst will behave similarly. Transfer to another world would require new calibration experiments, not merely reuse of the Batch 2 recipe.

Accordingly, the sealed recommendation should be stated narrowly: Batch 2 was the highest-scoring observed batch in this 12-run sample and belongs to a locally promising safe region. It has not been proven globally optimal, statistically superior to neighboring treatments, repeatable across independent batches, or transferable across materials or worlds.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 144.7 | none | 0 |
| Q | yes | 0 | 167.2 | none | 0 |
| K2 | yes | 0 | 125.4 | none | 0 |

## Scope note

This report contains only information available before truth release. Reference truth, prediction scoring, and recommendation retests are intentionally absent because the full 60-task block has not yet completed.
