# RX-W03--P--mechanism_discovery--Aligned

## Run summary

- World: `RX-W03`
- Locus: `P`
- Goal: `mechanism_discovery`
- Arm: `Aligned`
- Status: `completed`
- Source status: `completed`
- Experimental sessions: `12/12`
- Operations: `85`
- Exact replay verified: `True`
- Rollbacks: `[]`
- Posttest chain sealed: `True`

### Recovery status

- Effective result location: `posttest-repair-v9`
- Recovery version: `recovery-v9-parallel4`
- Repaired stages: `Q, K2`
- Source experiments rerun: `False`
- Original source thread reused: `True`
- Truth revealed during recovery: `False`

## Sealed recommendation

- Selected batch: `12`
- Rationale: Batch 12 combined strong conversion and yield with a post-reaction quench that reduced observed safety risk, giving the best balanced final result.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000475 mol) | 420 K x 3300 s @ 150 rpm | no | 0.7729 | 0.7859 | 0.9685 | 0.2162 | 0.1427 | 0.2572 | 0.4248 |
| 2 | S0 (0.0050 L) | 0.003000 mol | C0 (0.000475 mol) | 420 K x 3300 s @ 150 rpm | no | 0.5607 | 0.7649 | 0.7395 | 0.1873 | 0.0473 | 0.2551 | 0.3317 |
| 3 | S0 (0.0050 L) | 0.003000 mol | C2 (0.000475 mol) | 420 K x 3300 s @ 150 rpm | no | 0.7086 | 0.7763 | 0.8973 | 0.1764 | 0.0526 | 0.2564 | 0.4013 |
| 4 | S0 (0.0050 L) | 0.003000 mol | C3 (0.000475 mol) | 420 K x 3300 s @ 150 rpm | no | 0.7108 | 0.8305 | 0.8357 | 0.1330 | 0.0577 | 0.2563 | 0.3906 |
| 5 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000475 mol) | 390 K x 3300 s @ 150 rpm | no | 0.7395 | 0.7984 | 0.9053 | 0.1645 | 0.0912 | 0.1440 | 0.4592 |
| 6 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000475 mol) | 405 K x 3300 s @ 150 rpm | no | 0.7644 | 0.8165 | 0.9433 | 0.1829 | 0.1238 | 0.1916 | 0.4560 |
| 7 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000475 mol) | 435 K x 3300 s @ 150 rpm | no | 0.7602 | 0.7905 | 0.9773 | 0.2306 | 0.1704 | 0.3198 | 0.3936 |
| 8 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000475 mol) | 420 K x 1500 s @ 150 rpm | no | 0.7081 | 0.9033 | 0.7955 | 0.0946 | 0.0521 | 0.2562 | 0.4128 |
| 9 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000475 mol) | 420 K x 6000 s @ 150 rpm | no | 0.6607 | 0.6552 | 1.0000 | 0.3475 | 0.2978 | 0.2571 | 0.3482 |
| 10 | S1 (0.0050 L) | 0.003000 mol | C1 (0.000475 mol) | 390 K x 3300 s @ 150 rpm | no | 0.7357 | 0.7645 | 0.9573 | 0.2337 | 0.1478 | 0.1676 | 0.4435 |
| 11 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000150 mol) | 405 K x 3300 s @ 150 rpm | no | 0.5305 | 0.7755 | 0.6837 | 0.1696 | 0.0732 | 0.1896 | 0.3505 |
| 12 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000475 mol) | 405 K x 3300 s @ 150 rpm | yes | 0.7678 | 0.8093 | 0.9334 | 0.1961 | 0.1278 | 0.1033 | 0.4910 |

## Complete experimental actions and observations

### Batch 1

Lifecycle index: `1`; end step: `7`.

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.005
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000475,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 150,
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
    "byproduct_signal": 0.21624505519866943,
    "conversion": 0.9684633016586304,
    "cost": 0.619700014591217,
    "degradation_warning": 0.14270353317260742,
    "safety_risk": 0.25716689229011536,
    "score": 0.42479199171066284,
    "selectivity": 0.7859150171279907,
    "virtual_spectrum_summary": 0.18315136432647705,
    "yield": 0.7729050517082214
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
      "volume_L": 0.005
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "catalyst": 0,
      "catalyst_amount_mol": 0.000475,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 150,
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
  "end_step": 14,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.1872875839471817,
    "conversion": 0.7394765615463257,
    "cost": 0.42969998717308044,
    "degradation_warning": 0.04732637107372284,
    "safety_risk": 0.25514674186706543,
    "score": 0.3316742777824402,
    "selectivity": 0.7649209499359131,
    "virtual_spectrum_summary": 0.12430503219366074,
    "yield": 0.5607060790061951
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
      "volume_L": 0.005
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "catalyst": 2,
      "catalyst_amount_mol": 0.000475,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 150,
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
  "end_step": 21,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.17635692656040192,
    "conversion": 0.8973170518875122,
    "cost": 0.5056999921798706,
    "degradation_warning": 0.0526396669447422,
    "safety_risk": 0.2563643753528595,
    "score": 0.4013184905052185,
    "selectivity": 0.7762953639030457,
    "virtual_spectrum_summary": 0.12068416178226471,
    "yield": 0.7086173295974731
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
      "volume_L": 0.005
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.000475,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 150,
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
  "end_step": 28,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.13303129374980927,
    "conversion": 0.8356539011001587,
    "cost": 0.6956999897956848,
    "degradation_warning": 0.05771207809448242,
    "safety_risk": 0.2562745213508606,
    "score": 0.3906254768371582,
    "selectivity": 0.8305241465568542,
    "virtual_spectrum_summary": 0.09913764894008636,
    "yield": 0.7108064293861389
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
      "volume_L": 0.005
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000475,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 150,
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
  "end_step": 35,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.16449697315692902,
    "conversion": 0.9052747488021851,
    "cost": 0.619700014591217,
    "degradation_warning": 0.09121209383010864,
    "safety_risk": 0.14401142299175262,
    "score": 0.45915043354034424,
    "selectivity": 0.7983971834182739,
    "virtual_spectrum_summary": 0.13151878118515015,
    "yield": 0.7394970059394836
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
      "solvent": 0,
      "volume_L": 0.005
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000475,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 150,
      "target_temperature_K": 405
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
    "byproduct_signal": 0.1828787475824356,
    "conversion": 0.9433097243309021,
    "cost": 0.619700014591217,
    "degradation_warning": 0.12384270131587982,
    "safety_risk": 0.19163988530635834,
    "score": 0.45602354407310486,
    "selectivity": 0.8165176510810852,
    "virtual_spectrum_summary": 0.15631252527236938,
    "yield": 0.7644277811050415
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
      "solvent": 0,
      "volume_L": 0.005
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000475,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 150,
      "target_temperature_K": 435
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
    "byproduct_signal": 0.2305566966533661,
    "conversion": 0.9773183465003967,
    "cost": 0.619700014591217,
    "degradation_warning": 0.1704399734735489,
    "safety_risk": 0.3197721242904663,
    "score": 0.39358431100845337,
    "selectivity": 0.7905101180076599,
    "virtual_spectrum_summary": 0.20350417494773865,
    "yield": 0.760231077671051
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
      "solvent": 0,
      "volume_L": 0.005
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000475,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1500,
      "operation": "heat",
      "stirring_speed_rpm": 150,
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
  "end_step": 56,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.09463653713464737,
    "conversion": 0.7954972386360168,
    "cost": 0.6047000288963318,
    "degradation_warning": 0.052101898938417435,
    "safety_risk": 0.2562240958213806,
    "score": 0.41283491253852844,
    "selectivity": 0.9033346772193909,
    "virtual_spectrum_summary": 0.07549595087766647,
    "yield": 0.7080559134483337
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
      "solvent": 0,
      "volume_L": 0.005
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000475,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 6000,
      "operation": "heat",
      "stirring_speed_rpm": 150,
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
  "end_step": 63,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.34748125076293945,
    "conversion": 1.0,
    "cost": 0.6421999931335449,
    "degradation_warning": 0.29775577783584595,
    "safety_risk": 0.2570512294769287,
    "score": 0.3481910228729248,
    "selectivity": 0.6551771759986877,
    "virtual_spectrum_summary": 0.3251047730445862,
    "yield": 0.6607244610786438
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
      "solvent": 1,
      "volume_L": 0.005
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000475,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 150,
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
  "end_step": 70,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.23369446396827698,
    "conversion": 0.9573463201522827,
    "cost": 0.6216999888420105,
    "degradation_warning": 0.14784720540046692,
    "safety_risk": 0.16758668422698975,
    "score": 0.4435402452945709,
    "selectivity": 0.7644634246826172,
    "virtual_spectrum_summary": 0.19506320357322693,
    "yield": 0.7356843948364258
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
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.005
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.00015,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 150,
      "target_temperature_K": 405
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
    "byproduct_signal": 0.16964322328567505,
    "conversion": 0.6837369799613953,
    "cost": 0.385699987411499,
    "degradation_warning": 0.07315575331449509,
    "safety_risk": 0.18961802124977112,
    "score": 0.35053932666778564,
    "selectivity": 0.7754589915275574,
    "virtual_spectrum_summary": 0.1262238621711731,
    "yield": 0.5304974317550659
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
      "solvent": 0,
      "volume_L": 0.005
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000475,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 150,
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
  "end_step": 85,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.19609107077121735,
    "conversion": 0.9333982467651367,
    "cost": 0.6529775857925415,
    "degradation_warning": 0.1277981698513031,
    "safety_risk": 0.10326392948627472,
    "score": 0.4910079538822174,
    "selectivity": 0.8092873692512512,
    "virtual_spectrum_summary": 0.1653592735528946,
    "yield": 0.7677819728851318
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report for the completed 12-batch reaction-safety campaign

1. Scope and interpretation

This report describes a bounded synthetic benchmark involving an anonymous limiting reagent, anonymous catalysts A–D, and categorical solvent effects. The real solvent names identify selectable components, but the observed kinetic effects should not be interpreted as predictions about a named real reaction. I use R for the public reactant, P for the desired target, B for competing byproduct, and D for degradation products or processes represented by the degradation-warning channel.

All numerical compositions below are final-assay processed observations unless explicitly identified as pre-termination HPLC observations. Yield, conversion, selectivity, byproduct signal, and degradation warning are dimensionless fractions. Each condition was run only once, so small differences may reflect process variability and assay noise. The final-assay stated noise scales were approximately 0.006 for yield, 0.008 for conversion, byproduct, and degradation warning, and 0.010 for selectivity, but lack of replication leaves additional process variability unidentified.

2. Experimental map and principal observations

Every batch used 0.003 mol reagent and 0.005 L solvent. Except for batch 11, catalyst loading was 0.000475 mol. Stirring was 150 rpm.

Batch 1 — water, Catalyst B, 420 K, 3300 s, no quench: yield 0.7729, conversion 0.9685, selectivity 0.7859, byproduct 0.2162, degradation 0.1427, safety risk 0.2572. This was the supplied reference-region condition.

Batch 2 — water, Catalyst A, 420 K, 3300 s: yield 0.5607, conversion 0.7395, selectivity 0.7649, byproduct 0.1873, degradation 0.0473, risk 0.2551.

Batch 3 — water, Catalyst C, 420 K, 3300 s: yield 0.7086, conversion 0.8973, selectivity 0.7763, byproduct 0.1764, degradation 0.0526, risk 0.2564.

Batch 4 — water, Catalyst D, 420 K, 3300 s: yield 0.7108, conversion 0.8357, selectivity 0.8305, byproduct 0.1330, degradation 0.0577, risk 0.2563.

Batch 5 — water, Catalyst B, 390 K, 3300 s: yield 0.7395, conversion 0.9053, selectivity 0.7984, byproduct 0.1645, degradation 0.0912, risk 0.1440.

Batch 6 — water, Catalyst B, 405 K, 3300 s: yield 0.7644, conversion 0.9433, selectivity 0.8165, byproduct 0.1829, degradation 0.1238, risk 0.1916.

Batch 7 — water, Catalyst B, 435 K, 3300 s: yield 0.7602, conversion 0.9773, selectivity 0.7905, byproduct 0.2306, degradation 0.1704, risk 0.3198.

Batch 8 — water, Catalyst B, 420 K, 1500 s: yield 0.7081, conversion 0.7955, selectivity 0.9033, byproduct 0.0946, degradation 0.0521, risk 0.2562.

Batch 9 — water, Catalyst B, 420 K, 6000 s: yield 0.6607, conversion 1.0000 (clipped at the observable upper bound), selectivity 0.6552, byproduct 0.3475, degradation 0.2978, risk 0.2571.

Batch 10 — ethanol, Catalyst B, 390 K, 3300 s: yield 0.7357, conversion 0.9573, selectivity 0.7645, byproduct 0.2337, degradation 0.1478, risk 0.1676.

Batch 11 — water, Catalyst B, 0.000150 mol catalyst, 405 K, 3300 s: yield 0.5305, conversion 0.6837, selectivity 0.7755, byproduct 0.1696, degradation 0.0732, risk 0.1896.

Batch 12 — water, Catalyst B, 405 K, 3300 s, followed by quench: yield 0.7678, conversion 0.9334, selectivity 0.8093, byproduct 0.1961, degradation 0.1278, risk 0.1033. This was the sealed recommendation because it retained the high target yield of the balanced 405 K condition while the quench sharply lowered the terminal risk.

3. Proposed reaction network

The simplest account consistent with the campaign is a catalytic network containing both parallel and consecutive loss paths:

R --(catalyst, temperature)--> P
R --(catalyst, temperature)--> B
P --(temperature/time, possibly catalyst-assisted)--> D and/or B

A useful provisional kinetic form is:

dR/dt = -a(t,C,c)[kP,c(T) + kB,c(T)]R

dP/dt = a(t,C,c)kP,c(T)R - kD,c(T)P

dB/dt = a(t,C,c)kB,c(T)R + alpha·kD,c(T)P

dD/dt = (1-alpha)·kD,c(T)P

Here c is catalyst identity, C is catalyst loading, and a is effective catalyst activity. Candidate forms are a = C/(KC + C) for loading saturation and a(t) = a0 exp[-kdeact(T)t] for deactivation. The current data establish a strong loading dependence but do not distinguish linear catalysis, saturation, inhibition, or explicit catalyst deactivation.

Temperature dependence can be represented locally by Arrhenius-like terms, ki,c(T) = Ai,c exp[-Ei,c/(RT)]. The data require the competing and degradation channels to become increasingly important as thermal exposure rises. I would not claim that the available four temperatures determine unique activation energies.

A compact observational interpretation is:

conversion ≈ 1 - R/R0

target yield ≈ P/R0

selectivity ≈ P/(P + observable competing products), subject to the benchmark calibration

The measured quantities are noisy calibrated proxies, so identities such as yield = conversion × selectivity should not be imposed exactly. For example, batch 6 had conversion 0.9433 and selectivity 0.8165, whose product is about 0.770, close to but not exactly its measured yield of 0.7644.

4. Evidence for catalyst-dependent activity and branching

Batches 1–4 isolated catalyst identity at the same nominal thermal and recipe conditions. Catalyst B produced the greatest conversion (0.9685) and yield (0.7729), so it has the largest effective productive activity among those tested. Catalyst A was markedly less active: conversion 0.7395 and yield 0.5607. Catalyst C was intermediate at 0.8973 conversion and 0.7086 yield.

Catalyst D is especially informative because it was cleaner but less converting. Its conversion was only 0.8357, yet selectivity was 0.8305 and byproduct signal was 0.1330, both better than Catalyst B at 0.7859 selectivity and 0.2162 byproduct. Thus catalyst identity changes more than a single common rate multiplier: it changes either the productive/competing branching ratio, the degradation rate, or both. A model assigning each catalyst only one scalar activity would miss this result.

The loading comparison reinforces a kinetic role for Catalyst B. Reducing its amount from 0.000475 mol in batch 6 to 0.000150 mol in batch 11 at 405 K and 3300 s lowered conversion from 0.9433 to 0.6837 and yield from 0.7644 to 0.5305. The 68% loading reduction therefore caused a large loss in conversion. This is qualitatively consistent with a catalyst-dependent rate. The low-loading batch also had less degradation warning (0.0732 versus 0.1238), which can arise simply because less product and less total conversion were generated, although catalyst-assisted degradation is a competing explanation.

5. Temperature, time, and the target-yield maximum

The Catalyst B/water temperature series at 3300 s was batches 5, 6, 1, and 7 at 390, 405, 420, and 435 K. Conversion increased monotonically: 0.9053, 0.9433, 0.9685, and 0.9773. In contrast, byproduct signal generally increased from 0.1645 to 0.1829, 0.2162, and 0.2306, while degradation warning increased from 0.0912 to 0.1238, 0.1427, and 0.1704. Target yield rose from 0.7395 at 390 K to 0.7644 at 405 K and 0.7729 at 420 K, then ceased improving at 435 K (0.7602). Given assay noise, the exact yield ordering near the top is uncertain, but the mechanistic pattern is clear: higher temperature accelerates reagent disappearance while increasingly diverting material into competing or degraded states.

The time series at 420 K gives stronger evidence for a consecutive loss process. At 1500 s (batch 8), conversion was 0.7955, selectivity 0.9033, byproduct 0.0946, degradation 0.0521, and yield 0.7081. At 3300 s (batch 1), conversion reached 0.9685 and yield 0.7729, but selectivity had fallen to 0.7859 and degradation risen to 0.1427. At 6000 s (batch 9), conversion was at the reported ceiling of 1.0000, but yield fell to 0.6607, selectivity to 0.6552, while byproduct and degradation rose to 0.3475 and 0.2978. Therefore conversion continues toward completion after target yield has reached a maximum, and prolonged exposure destroys or transforms target material. This behavior cannot be explained adequately by a single irreversible R→P reaction with fixed selectivity.

The local process optimum is consequently a stopping-time problem. Short exposure preserves selectivity but leaves reactant; long exposure maximizes disappearance of reactant but sacrifices accumulated target. Under the tested recipe, approximately 3300 s at 405–420 K lies near the target-yield ridge. This is a local statement, not a globally fitted optimum.

6. Solvent coupling

Batches 5 and 10 compare water and ethanol at 390 K, 3300 s with Catalyst B. Ethanol increased observed conversion from 0.9053 to 0.9573 but did not improve yield: 0.7357 versus 0.7395 in water. It reduced selectivity from 0.7984 to 0.7645 and increased byproduct from 0.1645 to 0.2337 and degradation warning from 0.0912 to 0.1478. Risk also increased from 0.1440 to 0.1676.

Within this benchmark, ethanol therefore appears to accelerate overall conversion while disproportionately accelerating nonproductive or downstream channels. In the equations this could be represented by solvent-specific multipliers on kP, kB, and kD, with the multiplier on competing loss larger than the productive benefit. Because there was only one ethanol condition and no tests of acetonitrile or toluene, this conclusion is local and categorical. No real-solvent physical mechanism, such as polarity or boiling behavior, can be identified from these data.

7. Thermal history and safety coupling

The heat operations reported changes in temperature rather than complete temperature-time traces. Representative reported temperature changes were about +83.02 K for a 390 K command, +95.20 K for 405 K, +107.03 K for 420 K, and +118.52 K for 435 K. These values are consistent with heating from a roughly ambient initial state toward the commanded setpoint, but they do not establish the ramp time, overshoot, or time actually spent isothermally. A thermal submodel such as dT/dt = [Tset - T]/tau is plausible, yet tau cannot be recovered from endpoint deltas alone. Consequently, the kinetic variable should strictly be integrated thermal exposure, ∫ki[T(t)]dt, rather than commanded temperature multiplied by duration.

Safety risk was strongly temperature-dependent but was not simply proportional to conversion. For the Catalyst B/water 3300 s series, terminal risk rose from 0.1440 at 390 K to 0.1916 at 405 K, 0.2572 at 420 K, and 0.3198 at 435 K. The 435 K condition remained below the stated 0.35 limit but approached it closely. Changing duration from 1500 to 6000 s at 420 K barely changed reported terminal risk (0.2562 to 0.2571), suggesting that the public risk metric is dominated by current or peak thermal state and recipe hazards rather than cumulative chemical degradation.

Quenching separates composition from terminal thermal risk. Batch 12 matched batch 6 in recipe and heat command but added a quench after its HPLC measurement. Immediately before quench, batch 12 HPLC reported yield 0.7775, conversion 0.9211, selectivity 0.8154, and byproduct 0.2057. The quench reported a temperature change of -45 K over about 3.38 s and lowered risk by 0.0884, from 0.1916 to 0.1033. Its final assay remained compositionally close to batch 6: yields 0.7678 versus 0.7644, conversions 0.9334 versus 0.9433, and selectivities 0.8093 versus 0.8165. These differences are not compelling evidence of a chemical quench effect because they are comparable to measurement/process variation. The supported conclusion is that quenching promptly arrests thermal exposure and substantially reduces the terminal safety metric without a demonstrated target-yield penalty.

A useful process representation is therefore:

heat until a chosen stopping criterion;
quench rapidly, causing T := T - approximately 45 K under the tested state;
set reaction rates near zero or strongly reduced after quench;
terminate and assay.

Only one quench timing was tested, so the rate of residual chemistry during quench and the benefit of earlier or later quenching remain unknown.

8. Intermediate versus final measurements

In several batches, the pre-termination HPLC and final assay were directionally consistent but not identical. Batch 6 HPLC gave yield 0.7775, conversion 0.9294, selectivity 0.8220, and byproduct 0.1898; its final assay gave 0.7644, 0.9433, 0.8165, and 0.1829. Batch 9 HPLC gave yield 0.6521, conversion 1.0000, selectivity 0.6763, and byproduct 0.3342; the final assay gave 0.6607, 1.0000, 0.6552, and 0.3475. These differences could arise from independent instrument noise, sample removal, calibration differences, or small continuing changes between measurement and termination. They are insufficient to infer a definite hidden reaction during the measurement interval.

9. What changed my interpretation

The initial supplied model suggested that the lower-temperature side of the 420 K reference region would retain safer balanced performance. Batch 5 strongly supported the safety part: 390 K lowered risk from 0.2572 to 0.1440. Initially, the high yield and conversion of batch 1 could have been explained by a largely direct catalytic conversion. The 420 K time series modified that explanation: batch 9 showed complete conversion coupled to much lower yield and much higher degradation, requiring an important time-dependent secondary loss pathway.

The catalyst screen further changed a simple activity-only view. Catalyst D’s combination of lower conversion with higher selectivity and lower byproduct required catalyst-specific branching or degradation effects. The loading experiment supported catalyst-dependent rate control, while the ethanol experiment showed that a condition that increases conversion can simultaneously worsen selectivity. Finally, batch 12 demonstrated that terminal safety can be manipulated through thermal handling independently of most of the achieved composition, making quench timing a separate control variable rather than merely part of the reaction recipe.

10. Predictive implications within the tested region

Supported interpolation: for water, Catalyst B near 390–435 K and 1500–6000 s, conversion should increase with temperature and time; selectivity should generally decrease with excessive thermal exposure; and target yield should have an interior maximum rather than increasing to complete conversion.

Supported process recommendation: around 405 K for about 3300 s, followed promptly by quench, is the best tested balance. Batch 12 gave yield 0.7678 at risk 0.1033 and the highest final reaction score, 0.4910. Batch 1 had a marginally higher point estimate of yield, 0.7729, but much higher risk, 0.2572, and more aggressive thermal conditions.

Reasonable extrapolation: at times substantially beyond 6000 s at 420 K, target yield would probably decline further while degradation/byproduct signals rise or plateau. This is not directly observed beyond 6000 s.

Reasonable extrapolation: a temperature between 405 and 420 K with a stopping time somewhat below or near 3300 s may preserve most of the target yield while improving selectivity and risk. The experiment grid is too sparse to locate that optimum numerically.

Speculation: catalyst deactivation may contribute at long time or high temperature, but the observations can also be explained entirely by target degradation and competing conversion. No experiment directly measured catalyst activity after aging or reused catalyst.

11. Identifiability limits and competing explanations

The network topology is not unique. Rising degradation warning and falling yield could represent P→D, a common precursor branching increasingly toward degradation, reversible target formation followed by equilibrium displacement, or a detector response that changes with matrix composition. The consecutive P→D interpretation is the simplest because yield decreases after conversion reaches completion, but it is not uniquely proven.

Catalyst D’s cleaner profile could reflect intrinsically better selectivity, slower total conversion that simply has not reached the dirty late-time regime, or slower target degradation. A matched-conversion rather than matched-time comparison would be required to separate these explanations.

The catalyst-loading result does not determine reaction order in catalyst. Only two loadings were used, and they were not matched for conversion or exposure. Catalyst saturation, aggregation, induction, inhibition, and deactivation remain possible.

The temperature series does not yield trustworthy activation energies because it lacks replicates and full T(t) trajectories, and because productive and degrading processes overlap. Similarly, the time series contains only three times at one nominal temperature.

Only water and one ethanol condition were tested. No claims can be made about acetonitrile or toluene, and no molecular solvent mechanism should be inferred from categorical benchmark coupling.

Stirring was fixed at 150 rpm, so transport limitation cannot be excluded. Reagent concentration, solvent volume, and reagent/catalyst addition order were also essentially fixed. The model is therefore local to 0.003 mol reagent in 0.005 L solvent, the tested catalyst loadings, and this mixing protocol.

The public channels do not provide chemical identities or a closed mass balance for R, P, B, and D. “Byproduct signal” and “degradation warning” should be treated as calibrated observables rather than literal mole fractions. Conversion was clipped at 1.0000 in batch 9, so its exact proximity to complete conversion is unresolved.

12. Overall account

The observed world is best described as a thermally activated, catalyst-dependent reaction network in which desired target formation competes with direct byproduct formation and with secondary loss of accumulated target. Catalyst identity controls both activity and selectivity. Increasing catalyst loading accelerates conversion. Temperature and time increase conversion but also increase byproduct formation and degradation, producing a finite optimum in target yield. Solvent acts as a categorical modifier of all these rates; ethanol accelerated disappearance of reactant at 390 K but worsened selectivity relative to water. Safety risk is coupled strongly to thermal state and solvent but only weakly to extended time at a fixed setpoint. A rapid post-reaction quench lowers temperature and terminal risk while leaving the achieved composition approximately intact. This model explains the main catalyst, temperature, time, solvent, loading, and quench observations, but its kinetic parameters and detailed topology remain underdetermined by the single-replicate 12-batch design.

## Q — Blind predictions

### Overall rationale

The predictions extend the campaign's empirical catalyst-B temperature and time trends using the provisional network R→P, R→B, and P→degradation/byproduct. Point scores were estimated from the observed joint dependence on yield, selectivity, and terminal safety risk. Intervals include final-assay noise plus much larger structural uncertainty: every query uses untested acetonitrile, 400 rpm stirring, and a catalyst loading slightly above the main campaign value. Quenched and staged-temperature batches receive additional uncertainty because only one quench and no staged thermal histories were studied. Predictions are bounded to the public metric ranges; conversion near unity reflects likely saturation rather than precisely identified complete reaction.

### Q01

This is close to the studied 420 K, 3300 s Catalyst B condition, but acetonitrile, 400 rpm stirring, and the slightly higher catalyst loading were not tested. I expect nearly complete conversion and a yield near the observed local maximum, with wide intervals for the uncalibrated solvent and mixing effects.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2000 | 0.1200 | 0.3000 |
| conversion | 0.9850 | 0.9100 | 1.0000 |
| safety_risk | 0.2700 | 0.2100 | 0.3400 |
| score | 0.4400 | 0.3400 | 0.5200 |
| selectivity | 0.8000 | 0.7000 | 0.8800 |
| yield | 0.7800 | 0.6600 | 0.8600 |

### Q02

The quench should leave composition approximately unchanged from Q01 while lowering terminal thermal risk. The risk reduction is extrapolated from only batch 12, so its interval allows substantial solvent-dependent variation.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2000 | 0.1200 | 0.3000 |
| conversion | 0.9850 | 0.9100 | 1.0000 |
| safety_risk | 0.1500 | 0.0800 | 0.2400 |
| score | 0.4880 | 0.3800 | 0.5800 |
| selectivity | 0.8000 | 0.7000 | 0.8800 |
| yield | 0.7800 | 0.6600 | 0.8600 |

### Q03

Lower temperature should reduce conversion and thermal loss relative to Q01 while improving safety. The estimate is anchored to batch 5, with extra uncertainty because acetonitrile and 400 rpm were outside the research campaign.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1900 | 0.1000 | 0.3000 |
| conversion | 0.9400 | 0.8000 | 0.9900 |
| safety_risk | 0.1550 | 0.1000 | 0.2300 |
| score | 0.4690 | 0.3500 | 0.5600 |
| selectivity | 0.8100 | 0.7000 | 0.9000 |
| yield | 0.7500 | 0.6100 | 0.8400 |

### Q04

At 450 K, conversion should be effectively complete, but competing conversion and target degradation should reduce selectivity and yield. This exceeds the studied 435 K maximum, so both the chemical and safety predictions are extrapolations and the interval includes a safety-limit exceedance.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2800 | 0.1700 | 0.4300 |
| conversion | 0.9950 | 0.9500 | 1.0000 |
| safety_risk | 0.3900 | 0.3100 | 0.4900 |
| score | 0.3420 | 0.2000 | 0.4600 |
| selectivity | 0.7200 | 0.5700 | 0.8300 |
| yield | 0.7100 | 0.5500 | 0.8200 |

### Q05

The short 420 K exposure should preserve high selectivity but leave appreciable reactant, as in batch 8. Higher catalyst loading and mixing may raise conversion modestly, but the unseen solvent makes that adjustment uncertain.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1000 | 0.0400 | 0.2100 |
| conversion | 0.8400 | 0.7000 | 0.9400 |
| safety_risk | 0.2700 | 0.2100 | 0.3400 |
| score | 0.4140 | 0.3000 | 0.5100 |
| selectivity | 0.9000 | 0.7900 | 0.9600 |
| yield | 0.7200 | 0.5900 | 0.8200 |

### Q06

The extended exposure should drive conversion to its observable ceiling while causing substantial byproduct formation and secondary target loss. It is shorter than batch 9 but uses untested acetonitrile and stronger mixing, warranting broad compositional intervals.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3000 | 0.1900 | 0.4400 |
| conversion | 0.9980 | 0.9600 | 1.0000 |
| safety_risk | 0.2700 | 0.2100 | 0.3400 |
| score | 0.3820 | 0.2400 | 0.4900 |
| selectivity | 0.7000 | 0.5600 | 0.8100 |
| yield | 0.7000 | 0.5400 | 0.8100 |

### Q07

The low-temperature first stage should form target before a high-temperature finishing stage drives conversion and degradation. Because the sequence ends at 450 K, terminal risk should resemble a high-temperature batch. No staged-temperature experiment was performed, so order-dependent catalyst aging and target destruction create large uncertainty.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2600 | 0.1500 | 0.4100 |
| conversion | 0.9900 | 0.9100 | 1.0000 |
| safety_risk | 0.3900 | 0.3000 | 0.5000 |
| score | 0.3500 | 0.2000 | 0.4700 |
| selectivity | 0.7400 | 0.5900 | 0.8500 |
| yield | 0.7200 | 0.5500 | 0.8300 |

### Q08

The initial 450 K stage should rapidly create conversion and some irreversible damage, while the subsequent 390 K stage should finish at a lower thermal risk than Q07. I predict slightly better retained yield and selectivity than Q07, but this ordering effect is speculative because the campaign did not test staged histories.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2300 | 0.1300 | 0.3800 |
| conversion | 0.9900 | 0.9100 | 1.0000 |
| safety_risk | 0.1600 | 0.1000 | 0.2500 |
| score | 0.4570 | 0.3100 | 0.5600 |
| selectivity | 0.7700 | 0.6200 | 0.8700 |
| yield | 0.7400 | 0.5700 | 0.8400 |

### Q09

A short 440 K treatment should deliver high but incomplete conversion while retaining more selectivity than a long high-temperature exposure. Safety is near the stated limit because the setpoint exceeds the highest well-supported balanced region.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1400 | 0.0600 | 0.2600 |
| conversion | 0.9100 | 0.7800 | 0.9800 |
| safety_risk | 0.3500 | 0.2700 | 0.4400 |
| score | 0.3960 | 0.2700 | 0.5000 |
| selectivity | 0.8600 | 0.7400 | 0.9400 |
| yield | 0.7500 | 0.6100 | 0.8400 |

### Q10

Composition should remain close to Q09, while quenching should substantially reduce terminal risk. The quench interval is especially wide because its effectiveness was measured only once at 405 K in water, not at 440 K in acetonitrile.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1400 | 0.0600 | 0.2600 |
| conversion | 0.9100 | 0.7800 | 0.9800 |
| safety_risk | 0.2200 | 0.1200 | 0.3300 |
| score | 0.4480 | 0.3100 | 0.5600 |
| selectivity | 0.8600 | 0.7400 | 0.9400 |
| yield | 0.7500 | 0.6100 | 0.8400 |

### Q11

Long exposure at 370 K may eventually give substantial conversion while limiting instantaneous thermal risk, but 370 K lies below the studied range. The balance between slow target formation and long-time degradation is therefore poorly constrained, producing wide conversion and yield intervals.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1800 | 0.0800 | 0.3200 |
| conversion | 0.8800 | 0.6800 | 0.9700 |
| safety_risk | 0.1100 | 0.0700 | 0.1800 |
| score | 0.4640 | 0.3200 | 0.5600 |
| selectivity | 0.8200 | 0.6800 | 0.9200 |
| yield | 0.7100 | 0.5400 | 0.8200 |

### Q12

This combines a temperature above the explored range with a duration beyond the longest campaign exposure. Conversion should saturate, but extensive competing conversion and target degradation are expected. It is the least reliable prediction and may encounter nonlinear safety behavior or operational constraint handling absent from the training campaign.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5800 | 0.3800 | 0.7800 |
| conversion | 1.0000 | 0.9600 | 1.0000 |
| safety_risk | 0.4400 | 0.3000 | 0.6000 |
| score | 0.1180 | 0.0000 | 0.3100 |
| selectivity | 0.4200 | 0.2200 | 0.6200 |
| yield | 0.4200 | 0.2000 | 0.6500 |

## K2 — Retrospective analysis

1. Initial claims: supported, contradicted, or untested

The initial material contained one substantive process claim: near the 420 K, 3300 s reference region, the lower-temperature side should preserve safe, balanced performance more reliably than the higher-temperature side. It also said that any temperature-bound rollback should count as evidence against the attempted setting rather than as missing output. No task-specific molecular mechanism, catalyst ranking, solvent-effect model, or kinetic parameters were supplied.

The directional temperature claim was supported, especially for safety. For Catalyst B in water at 3300 s, risk rose from 0.1440 in batch 5 at 390 K to 0.1916 in batch 6 at 405 K, 0.2572 in batch 1 at 420 K, and 0.3198 in batch 7 at 435 K. Higher temperature also raised degradation warning across that series from 0.0912 to 0.1238, 0.1427, and 0.1704. Batch 7 increased conversion to 0.9773 but did not improve yield over the reference, supporting the warning that higher temperature is not a free performance gain.

The “balanced performance” portion needs qualification. Batch 6 at 405 K preserved most of the reference yield—0.7644 versus 0.7729 in batch 1—while lowering risk substantially. Batch 5 at 390 K was safer still but yielded only 0.7395. The evidence therefore favors a lower-temperature compromise near 405 K, not a universal rule that lower temperature improves every outcome.

No temperature-bound rollback occurred, so the rollback interpretation remained untested. That is absence of a relevant observation, not confirmation. Likewise, acetonitrile, toluene, stirring-rate effects, catalyst reuse, and detailed thermal lag were never tested during the campaign.

I did not observe clear evidence contradicting the supplied temperature-direction claim. The important later development was instead that the claim was incomplete: batches 8 and 9 showed that reaction time and secondary target loss were as important as temperature. K1 accordingly expanded the account into a reaction network rather than retaining only the original directional heuristic.

2. Experiments that formed or changed the interpretation

Batch 1 established the reference phenotype but did not by itself identify a mechanism. Its conversion of 0.9685 and yield of 0.7729 were still compatible with a simple mostly productive conversion.

Batches 2–4 genuinely changed the catalyst interpretation. Under the same nominal recipe and thermal program, Catalyst A gave conversion 0.7395 and yield 0.5607, Catalyst C gave 0.8973 and 0.7086, and Catalyst D gave 0.8357 and 0.7108. Catalyst D was especially informative: its selectivity of 0.8305 and byproduct signal of 0.1330 were cleaner than Catalyst B’s 0.7859 and 0.2162 despite lower conversion. This motivated K1’s specific judgment that catalyst identity changes branching or degradation, not merely a single overall rate constant.

Batches 5–7 were selected largely because of the initial lower-temperature claim and the batch-1 reference. They established a temperature-dependent tradeoff among conversion, degradation, safety, and yield. Batch 7 at 435 K was important because additional conversion no longer translated into additional target yield.

Batches 8 and 9 most strongly changed the mechanistic account. At 420 K, moving from 1500 s to 3300 s and 6000 s increased conversion from 0.7955 to 0.9685 and then the reported ceiling of 1.0000. Yield first rose from 0.7081 to 0.7729 but then fell to 0.6607, while degradation warning rose from 0.0521 to 0.1427 and then 0.2978. This was the direct basis for K1’s statement that prolonged exposure “destroys or transforms target material” and for proposing a consecutive P→D/B process. It was evidence against a single irreversible R→P model with fixed selectivity.

Batch 10 was an exploratory solvent choice rather than a consequence of a validated solvent theory. Relative to water at 390 K, ethanol increased conversion from 0.9053 to 0.9573 but worsened selectivity from 0.7984 to 0.7645 and increased byproduct signal from 0.1645 to 0.2337. That supported categorical solvent coupling, but testing ethanol rather than either remaining solvent was essentially an informed guess.

Batch 11 was chosen after Catalyst B emerged as the most productive tested catalyst. Lowering its loading from 0.000475 mol to 0.000150 mol reduced conversion from 0.9433 in batch 6 to 0.6837 and yield from 0.7644 to 0.5305. This supported catalyst-dependent rate control but did not identify catalyst order, saturation, aggregation, inhibition, or deactivation.

Batch 12 increasingly served both mechanism and optimization. Adding a quench to the batch-6 recipe lowered risk from 0.1916 immediately before quench to 0.1033 at the terminal state, while final composition remained broadly similar to batch 6. This supported K1’s claim that terminal thermal risk can be controlled somewhat independently of achieved composition. Because only one quench was tested, its generality was not established.

Several design choices remained assumptions: fixed reagent amount and volume, fixed addition order, 150 rpm stirring, reliance on nominal setpoint and duration rather than measured T(t), and use of only one non-water solvent. Those assumptions became especially consequential for the blind predictions, all of which used acetonitrile, 400 rpm, and 0.000525 mol Catalyst B.

3. Leading mechanism and competing explanations

K1’s preferred phenomenological network was:

R→P,
R→B,
P→D and/or B,

with catalyst identity, loading, solvent, and temperature affecting the individual rates. This is the simplest account of an interior target-yield maximum combined with continuing conversion and rising degradation.

The strongest competing topology is a common-intermediate model: R first forms an unobserved intermediate I, and temperature or catalyst state controls I’s partition among P, B, and D. It can reproduce the same observed time trends without requiring direct degradation of isolated P. Because I was never observed, the campaign cannot uniquely distinguish these networks.

A second competitor is reversible target formation, R⇌P, followed by irreversible trapping or degradation. The late yield decline could then reflect equilibrium redistribution plus side-reaction capture rather than a simple first-order P→D step. No target-rich perturbation experiment was performed, so reversibility remains unresolved.

A third competitor is catalyst deactivation. Long exposure might reduce productive catalytic activity while competing uncatalyzed reactions continue. K1 correctly labeled this as speculative: no aged-catalyst challenge, reuse experiment, or direct catalyst-state measurement was conducted.

Catalyst D’s clean profile also remains ambiguous. It may possess intrinsically better branching selectivity, or it may simply progress more slowly along the same conversion-dependent degradation trajectory. The matched-time catalyst screen distinguishes observed performance but not intrinsic selectivity at matched conversion.

The data do distinguish broader classes. They disfavor a single fixed-selectivity R→P model; demonstrate catalyst-dependent effective activity; show catalyst-specific performance not captured by conversion alone; and establish that excessive thermal exposure increases competing or degradation signals. They do not determine elementary species, unique rate laws, reaction order, activation energies, catalyst-deactivation constants, or whether mass transport contributes.

4. One additional complete experiment

I would repeat the Catalyst B/water reference recipe—0.005 L water, 0.003 mol reagent, 0.000475 mol catalyst, and 150 rpm—but use a within-vessel time-course challenge: heat at 420 K for 1500 s, measure once by HPLC, continue heating at 420 K for another 4500 s, terminate, and perform the required final assay.

This directly targets the central K1 claim of consecutive target loss. Existing batches 8 and 9 used separate vessels, so their contrast confounds time with between-batch process variation.

Possible interpretations would be:

• If target yield rises initially and then falls substantially while conversion, byproduct, and degradation signals rise, the P→D/B account gains support.

• If target yield remains approximately constant while conversion and byproduct continue increasing, parallel branching through an unobserved intermediate becomes more attractive than direct target destruction.

• If all composition channels plateau after the first measurement, catalyst deactivation or equilibrium limitation becomes more plausible.

• If conversion continues but degradation warning does not rise, the degradation channel or its mechanistic interpretation would need revision.

The experiment would not be decisive because the early observation would be HPLC and the endpoint would be the multichannel final assay. Only changes appreciably larger than combined instrument and process uncertainty should be interpreted mechanistically. I would not execute this proposal now.

5. Identifiability versus operating score

The campaign deliberately spent several batches on mechanistic discrimination rather than expected score. The catalyst screen, the 1500 s and 6000 s time points, and the low-loading batch were scientifically useful even when operationally inferior. Batch 9 in particular produced only a 0.3482 score but supplied the clearest evidence for an interior yield maximum and secondary loss. Batch 11 scored only 0.3505 but established strong catalyst-loading dependence.

Later choices placed more weight on performance. Once batch 6 identified a favorable 405 K compromise, batch 12 repeated that recipe with a quench. This raised the final score to 0.4910 and supplied useful evidence about risk control, but a replicate, matched-conversion catalyst comparison, or extra time point would have improved identifiability more.

The research goal prioritized explanation over the safe score, which justified broad coverage of catalyst, temperature, time, solvent, loading, and quench effects. Nevertheless, the design was not a formal system-identification design: it lacked replication, randomization, factorial crossings, matched-conversion comparisons, and complete thermal trajectories. Covering many factors with only 12 batches produced breadth at the cost of parameter identifiability.

Thus both tradeoffs occurred. Batches 2–4, 8, 9, and 11 sacrificed likely score for information. Batch 12 sacrificed some potential mechanistic information for optimization and validation of a practical control step.

6. Underused evidence and blind-prediction weaknesses

The raw characterization artifacts were not examined in depth. K1 relied mainly on processed estimates rather than fully exploiting peak areas, shapes, baselines, saturation flags, cross-channel discrepancies, or mass-balance structure. GC and UV–visible measurements were never used, so the campaign lacked an independent intermediate modality.

The temperature changes were informative but difficult to use. Reported changes were approximately +83 K, +95 K, +107 K, and +119 K for 390, 405, 420, and 435 K commands, but no full T(t) histories were available. Consequently, nominal setpoint and duration were used as kinetic coordinates even though K1 stated that integrated thermal exposure was the more appropriate variable.

The paired HPLC and final-assay results were discussed qualitatively rather than modeled systematically. They might have supported an estimate of cross-instrument bias or post-sampling evolution, but single observations and differing modalities made those effects hard to separate.

Among the sealed blind predictions, Q12 is least reliable. Its 460 K, 6300 s treatment exceeds both the studied temperature and duration ranges and combines the two directions most associated with degradation and elevated risk. Its predicted interval may still be too narrow because it cannot fully represent nonlinear constraint handling, saturation, or thermal runaway-like benchmark behavior.

Q07 and Q08 are also highly uncertain because they reverse a two-stage 390/450 K history. No staged-temperature experiment was conducted. Their difference depends on path dependence, catalyst aging, irreversible target damage, and whether the public safety metric reflects terminal or peak thermal state. K1 explicitly said these features were not identifiable.

Q11 extrapolates below the studied range to 370 K, where the long-time balance between slow formation and degradation is unknown. Q04 extrapolates to 450 K. Q09 and Q10 combine an untested 440 K point with short exposure; the quench in Q10 is extrapolated from one water experiment at 405 K.

More fundamentally, every blind query uses acetonitrile, 400 rpm, and 0.000525 mol Catalyst B. Acetonitrile was never tested, stirring was fixed at 150 rpm, and the loading response was observed at only two widely separated values. Therefore even Q01–Q06 are not simple interpolations. Their intervals must cover structural uncertainty, not merely final-assay noise.

The sealed prediction rationale did acknowledge these domain shifts, but some numerical intervals—especially those for conversion and composition in Q01, Q02, Q07, Q08, and Q12—could still be overconfident. Near-unity conversion intervals are particularly fragile because batch 9’s 1.0000 result was clipped. If those intervals are read as calibrated probabilities rather than judgmental ranges, they are not fully consistent with K1’s declared local scope and single-replicate uncertainty.

7. Limitations of the sealed recommendation

The sealed recommendation was batch 12: water, Catalyst B, 0.000475 mol catalyst, 405 K for 3300 s at 150 rpm, followed by quench. It produced yield 0.7678, conversion 0.9334, selectivity 0.8093, byproduct signal 0.1961, degradation warning 0.1278, risk 0.1033, and the highest observed score, 0.4910.

This establishes batch 12 as sample-best among the 12 completed batches. It does not establish a global or even precisely located local optimum. Both batch 12 and its unquenched comparator, batch 6, were single runs. Their small compositional differences are compatible with measurement and process variation, while the large risk reduction rests on one quench event.

Repeatability should be tested by independently reproducing the entire batch-12 procedure, including setup, thermal history, quench timing, termination, and assay. Replication should quantify process variation in composition and in the risk decrease, not only analytical noise.

Local robustness should be tested with a small replicated neighborhood around the recommendation: temperatures around 400–410 K, durations bracketing 3300 s, modest catalyst-loading changes, and realistic quench delays. A center-point replicate would distinguish a broad operating plateau from a narrow, noise-sensitive ridge.

Cross-material scope requires repeating the local comparison with other solvents and catalysts. Batch 10 already showed that a solvent can raise conversion while worsening selectivity, so the batch-12 recipe cannot simply be transferred to acetonitrile or another catalyst. Cross-world scope would require independent benchmark-world initializations because the complete evidence base came from one campaign world.

Finally, the recommendation optimizes the public score under this particular contract. Different priorities for yield, degradation, cost, throughput, or peak rather than terminal risk could favor another condition. The defensible claim is that batch 12 was the highest-scoring observed safe compromise in this sample and that quenching was promising. It was not proven uniquely optimal, globally optimal, reproducible, or transferable.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 121.3 | none | 0 |
| Q | yes | 0 | 87.4 | none | 0 |
| K2 | yes | 0 | 92.7 | none | 0 |

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean 80% width | Mean interval score |
|---|---:|---:|---:|---:|
| byproduct_signal | 0.2222 | 0.1667 | 0.2325 | 1.1418 |
| conversion | 0.0424 | 0.6000 | 0.1342 | 0.2075 |
| safety_risk | 0.0288 | 1.0000 | 0.1667 | 0.1667 |
| score | 0.1246 | 0.4167 | 0.2383 | 0.4867 |
| selectivity | 0.2138 | 0.2000 | 0.2325 | 1.0688 |
| yield | 0.1677 | 0.4167 | 0.2617 | 0.7366 |

## Predictions versus released reference truth

### Q01

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2000 | 0.1200 | 0.3000 | 0.4503 | 0.4469, 0.4662, 0.4467, 0.4450, 0.4467 |
| conversion | 0.9850 | 0.9100 | 1.0000 | 0.9938 | 1.0000, 1.0000, 0.9860, 0.9873, 0.9956 |
| safety_risk | 0.2700 | 0.2100 | 0.3400 | 0.2983 | 0.2983, 0.2983, 0.2983, 0.2983, 0.2983 |
| score | 0.4400 | 0.3400 | 0.5200 | 0.2654 | 0.2635, 0.2685, 0.2680, 0.2631, 0.2639 |
| selectivity | 0.8000 | 0.7000 | 0.8800 | 0.5546 | 0.5563, 0.5738, 0.5478, 0.5381, 0.5570 |
| yield | 0.7800 | 0.6600 | 0.8600 | 0.5493 | 0.5420, 0.5435, 0.5619, 0.5554, 0.5436 |
### Q02

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2000 | 0.1200 | 0.3000 | 0.4565 | 0.4617, 0.4629, 0.4545, 0.4442, 0.4594 |
| conversion | 0.9850 | 0.9100 | 1.0000 | 1.0000 | 1.0000, 1.0000, 1.0000, 1.0000, 1.0000 |
| safety_risk | 0.1500 | 0.0800 | 0.2400 | 0.1511 | 0.1511, 0.1511, 0.1511, 0.1511, 0.1511 |
| score | 0.4880 | 0.3800 | 0.5800 | 0.3276 | 0.3307, 0.3368, 0.3227, 0.3239, 0.3239 |
| selectivity | 0.8000 | 0.7000 | 0.8800 | 0.5523 | 0.5540, 0.5733, 0.5405, 0.5400, 0.5537 |
| yield | 0.7800 | 0.6600 | 0.8600 | 0.5474 | 0.5539, 0.5572, 0.5426, 0.5458, 0.5372 |
### Q03

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1900 | 0.1000 | 0.3000 | 0.3766 | 0.3794, 0.3709, 0.3819, 0.3900, 0.3609 |
| conversion | 0.9400 | 0.8000 | 0.9900 | 0.9967 | 1.0000, 1.0000, 0.9889, 1.0000, 0.9944 |
| safety_risk | 0.1550 | 0.1000 | 0.2300 | 0.1857 | 0.1857, 0.1857, 0.1857, 0.1857, 0.1857 |
| score | 0.4690 | 0.3500 | 0.5600 | 0.3684 | 0.3706, 0.3671, 0.3652, 0.3719, 0.3673 |
| selectivity | 0.8100 | 0.7000 | 0.9000 | 0.6293 | 0.6322, 0.6263, 0.6308, 0.6343, 0.6231 |
| yield | 0.7500 | 0.6100 | 0.8400 | 0.6327 | 0.6355, 0.6305, 0.6258, 0.6375, 0.6344 |
### Q04

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2800 | 0.1700 | 0.4300 | 0.5283 | 0.5341, 0.5287, 0.5215, 0.5298, 0.5274 |
| conversion | 0.9950 | 0.9500 | 1.0000 | 0.9965 | 1.0000, 0.9988, 0.9941, 1.0000, 0.9895 |
| safety_risk | 0.3900 | 0.3100 | 0.4900 | 0.4035 | 0.4035, 0.4035, 0.4035, 0.4035, 0.4035 |
| score | 0.3420 | 0.2000 | 0.4600 | 0.1753 | 0.1761, 0.1753, 0.1756, 0.1755, 0.1738 |
| selectivity | 0.7200 | 0.5700 | 0.8300 | 0.4844 | 0.4790, 0.4868, 0.4792, 0.4926, 0.4847 |
| yield | 0.7100 | 0.5500 | 0.8200 | 0.4854 | 0.4900, 0.4836, 0.4902, 0.4801, 0.4833 |
### Q05

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1000 | 0.0400 | 0.2100 | 0.2240 | 0.2127, 0.2190, 0.2346, 0.2243, 0.2295 |
| conversion | 0.8400 | 0.7000 | 0.9400 | 0.9780 | 0.9698, 0.9860, 0.9851, 0.9824, 0.9669 |
| safety_risk | 0.2700 | 0.2100 | 0.3400 | 0.2987 | 0.2987, 0.2987, 0.2987, 0.2987, 0.2987 |
| score | 0.4140 | 0.3000 | 0.5100 | 0.4067 | 0.4069, 0.4023, 0.4073, 0.4084, 0.4085 |
| selectivity | 0.9000 | 0.7900 | 0.9600 | 0.7769 | 0.7760, 0.7624, 0.7815, 0.7800, 0.7844 |
| yield | 0.7200 | 0.5900 | 0.8200 | 0.7642 | 0.7673, 0.7603, 0.7611, 0.7654, 0.7667 |
### Q06

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3000 | 0.1900 | 0.4400 | 0.6220 | 0.6125, 0.6145, 0.6156, 0.6437, 0.6239 |
| conversion | 0.9980 | 0.9600 | 1.0000 | 0.9956 | 0.9990, 1.0000, 0.9906, 0.9940, 0.9944 |
| safety_risk | 0.2700 | 0.2100 | 0.3400 | 0.2979 | 0.2979, 0.2979, 0.2979, 0.2979, 0.2979 |
| score | 0.3820 | 0.2400 | 0.4900 | 0.1604 | 0.1639, 0.1597, 0.1587, 0.1595, 0.1599 |
| selectivity | 0.7000 | 0.5600 | 0.8100 | 0.3931 | 0.3923, 0.3900, 0.3880, 0.4025, 0.3925 |
| yield | 0.7000 | 0.5400 | 0.8100 | 0.3905 | 0.3990, 0.3897, 0.3908, 0.3829, 0.3901 |
### Q07

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2600 | 0.1500 | 0.4100 | 0.4961 | 0.4975, 0.4926, 0.5053, 0.4934, 0.4915 |
| conversion | 0.9900 | 0.9100 | 1.0000 | 0.9933 | 0.9948, 0.9899, 0.9907, 0.9910, 1.0000 |
| safety_risk | 0.3900 | 0.3000 | 0.5000 | 0.4274 | 0.4274, 0.4274, 0.4274, 0.4274, 0.4274 |
| score | 0.3500 | 0.2000 | 0.4700 | 0.1786 | 0.1762, 0.1787, 0.1795, 0.1720, 0.1868 |
| selectivity | 0.7400 | 0.5900 | 0.8500 | 0.5091 | 0.4941, 0.5185, 0.5054, 0.5066, 0.5207 |
| yield | 0.7200 | 0.5500 | 0.8300 | 0.5068 | 0.5097, 0.5018, 0.5120, 0.4923, 0.5182 |
### Q08

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2300 | 0.1300 | 0.3800 | 0.5022 | 0.5042, 0.5091, 0.4928, 0.4979, 0.5072 |
| conversion | 0.9900 | 0.9100 | 1.0000 | 0.9991 | 1.0000, 0.9954, 1.0000, 1.0000, 1.0000 |
| safety_risk | 0.1600 | 0.1000 | 0.2500 | 0.1973 | 0.1973, 0.1973, 0.1973, 0.1973, 0.1973 |
| score | 0.4570 | 0.3100 | 0.5600 | 0.2871 | 0.2870, 0.2882, 0.2802, 0.2860, 0.2941 |
| selectivity | 0.7700 | 0.6200 | 0.8700 | 0.5111 | 0.5264, 0.5157, 0.4835, 0.5021, 0.5279 |
| yield | 0.7400 | 0.5700 | 0.8400 | 0.5163 | 0.5063, 0.5171, 0.5160, 0.5190, 0.5232 |
### Q09

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1400 | 0.0600 | 0.2600 | 0.2551 | 0.2478, 0.2551, 0.2557, 0.2586, 0.2585 |
| conversion | 0.9100 | 0.7800 | 0.9800 | 0.9888 | 0.9803, 0.9874, 0.9938, 0.9911, 0.9914 |
| safety_risk | 0.3500 | 0.2700 | 0.4400 | 0.3780 | 0.3780, 0.3780, 0.3780, 0.3780, 0.3780 |
| score | 0.3960 | 0.2700 | 0.5000 | 0.3587 | 0.3576, 0.3632, 0.3586, 0.3556, 0.3583 |
| selectivity | 0.8600 | 0.7400 | 0.9400 | 0.7559 | 0.7496, 0.7587, 0.7564, 0.7553, 0.7596 |
| yield | 0.7500 | 0.6100 | 0.8400 | 0.7437 | 0.7471, 0.7537, 0.7420, 0.7358, 0.7399 |
### Q10

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1400 | 0.0600 | 0.2600 | 0.2502 | 0.2529, 0.2556, 0.2474, 0.2418, 0.2531 |
| conversion | 0.9100 | 0.7800 | 0.9800 | 0.9895 | 0.9937, 0.9834, 0.9945, 0.9943, 0.9816 |
| safety_risk | 0.2200 | 0.1200 | 0.3300 | 0.1718 | 0.1718, 0.1718, 0.1718, 0.1718, 0.1718 |
| score | 0.4480 | 0.3100 | 0.5600 | 0.4472 | 0.4450, 0.4479, 0.4492, 0.4470, 0.4470 |
| selectivity | 0.8600 | 0.7400 | 0.9400 | 0.7487 | 0.7486, 0.7516, 0.7418, 0.7498, 0.7516 |
| yield | 0.7500 | 0.6100 | 0.8400 | 0.7459 | 0.7395, 0.7473, 0.7538, 0.7433, 0.7454 |
### Q11

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1800 | 0.0800 | 0.3200 | 0.5042 | 0.5026, 0.5049, 0.5110, 0.4947, 0.5079 |
| conversion | 0.8800 | 0.6800 | 0.9700 | 0.9947 | 0.9891, 0.9869, 1.0000, 0.9984, 0.9993 |
| safety_risk | 0.1100 | 0.0700 | 0.1800 | 0.1547 | 0.1547, 0.1547, 0.1547, 0.1547, 0.1547 |
| score | 0.4640 | 0.3200 | 0.5600 | 0.2976 | 0.2974, 0.3007, 0.2905, 0.2975, 0.3018 |
| selectivity | 0.8200 | 0.6800 | 0.9200 | 0.5042 | 0.5154, 0.5160, 0.4770, 0.5024, 0.5103 |
| yield | 0.7100 | 0.5400 | 0.8200 | 0.5044 | 0.4984, 0.5069, 0.5023, 0.5044, 0.5099 |
### Q12

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5800 | 0.3800 | 0.7800 | 0.8008 | 0.7912, 0.7944, 0.8024, 0.8120, 0.8042 |
| conversion | 1.0000 | 0.9600 | 1.0000 | 0.9991 | 1.0000, 0.9954, 1.0000, 1.0000, 1.0000 |
| safety_risk | 0.4400 | 0.3000 | 0.6000 | 0.4203 | 0.4203, 0.4203, 0.4203, 0.4203, 0.4203 |
| score | 0.1180 | 0.0000 | 0.3100 | 0.0000 | 0.0000, 0.0000, 0.0000, 0.0000, 0.0000 |
| selectivity | 0.4200 | 0.2200 | 0.6200 | 0.2143 | 0.2309, 0.1960, 0.2230, 0.2062, 0.2153 |
| yield | 0.4200 | 0.2000 | 0.6500 | 0.2193 | 0.2180, 0.2146, 0.2252, 0.2157, 0.2233 |

## Recommendation retest

- Selected source batch: `12`
- Retest exact replay verified: `True`
- Retest failure: `none`

| Metric | Selected source batch | Independent retest | Retest minus source |
|---|---:|---:|---:|
| byproduct_signal | 0.1961 | 0.1922 | -0.0039 |
| conversion | 0.9334 | 0.9610 | 0.0276 |
| cost | 0.6530 | 0.6530 | 0.0000 |
| degradation_warning | 0.1278 | 0.1178 | -0.0100 |
| safety_risk | 0.1033 | 0.1033 | 0.0000 |
| score | 0.4910 | 0.4897 | -0.0013 |
| selectivity | 0.8093 | 0.8031 | -0.0062 |
| virtual_spectrum_summary | 0.1654 | 0.1587 | -0.0067 |
| yield | 0.7678 | 0.7615 | -0.0063 |

## Scope note

This is the final sanitized report produced after all 60 source sessions and K1/Q/K2 chains were sealed. It includes released reference truth, blind-prediction evaluation, and the independent recommendation retest. Provider-private event streams, credentials, thread identifiers, and token accounting remain excluded.
