# RX-W03--P--mechanism_discovery--MisIndexed

## Run summary

- World: `RX-W03`
- Locus: `P`
- Goal: `mechanism_discovery`
- Arm: `MisIndexed`
- Status: `completed`
- Source status: `completed`
- Experimental sessions: `12/12`
- Operations: `97`
- Exact replay verified: `True`
- Rollbacks: `[]`
- Posttest chain sealed: `True`

### Recovery status

- Effective result location: `source-repair-v9`
- Recovery version: `recovery-v9-parallel4`
- Repaired stages: `source`
- Source experiments rerun: `False`
- Original source thread reused: `False`
- Truth revealed during recovery: `False`

## Sealed recommendation

- Selected batch: `12`
- Rationale: Batch 12 combined the informative low-temperature 390 K program with prompt quenching, giving the campaign's strongest observed safe score, high final yield, and substantially reduced safety risk.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000475 mol) | 420 K x 1650 s @ 150 rpm → 420 K x 1650 s @ 150 rpm | no | 0.7748 | 0.7944 | 0.9803 | 0.2073 | 0.1587 | 0.3196 | 0.4008 |
| 2 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000475 mol) | 390 K x 1650 s @ 150 rpm → 390 K x 1650 s @ 150 rpm | no | 0.7445 | 0.8152 | 0.9149 | 0.1794 | 0.1051 | 0.1650 | 0.4569 |
| 3 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000475 mol) | 405 K x 1650 s @ 150 rpm → 405 K x 1650 s @ 150 rpm | no | 0.7687 | 0.8041 | 0.9511 | 0.1866 | 0.1279 | 0.2385 | 0.4343 |
| 4 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000475 mol) | 420 K x 825 s @ 150 rpm → 420 K x 825 s @ 150 rpm | no | 0.7481 | 0.8921 | 0.8446 | 0.1220 | 0.0625 | 0.3189 | 0.4026 |
| 5 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000475 mol) | 390 K x 3000 s @ 150 rpm → 390 K x 3000 s @ 150 rpm | no | 0.7068 | 0.7167 | 0.9842 | 0.2967 | 0.2118 | 0.1653 | 0.4217 |
| 6 | S0 (0.0050 L) | 0.003000 mol | C0 (0.000475 mol) | 390 K x 1650 s @ 150 rpm → 390 K x 1650 s @ 150 rpm | no | 0.4604 | 0.7321 | 0.6245 | 0.1697 | 0.0213 | 0.1624 | 0.3136 |
| 7 | S0 (0.0050 L) | 0.003000 mol | C2 (0.000475 mol) | 390 K x 1650 s @ 150 rpm → 390 K x 1650 s @ 150 rpm | no | 0.6150 | 0.8004 | 0.7890 | 0.1544 | 0.0468 | 0.1638 | 0.4007 |
| 8 | S0 (0.0050 L) | 0.003000 mol | C3 (0.000475 mol) | 390 K x 1650 s @ 150 rpm → 390 K x 1650 s @ 150 rpm | no | 0.6067 | 0.8346 | 0.7246 | 0.1298 | 0.0291 | 0.1636 | 0.3806 |
| 9 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000237 mol) | 390 K x 1650 s @ 150 rpm → 390 K x 1650 s @ 150 rpm | no | 0.5994 | 0.7928 | 0.7683 | 0.1604 | 0.0643 | 0.1637 | 0.3962 |
| 10 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000950 mol) | 390 K x 1650 s @ 150 rpm → 390 K x 1650 s @ 150 rpm | no | 0.8162 | 0.8243 | 0.9840 | 0.1664 | 0.1312 | 0.1657 | 0.4602 |
| 11 | S1 (0.0050 L) | 0.003000 mol | C1 (0.000475 mol) | 390 K x 1650 s @ 150 rpm → 390 K x 1650 s @ 150 rpm | no | 0.7273 | 0.7616 | 0.9555 | 0.2345 | 0.1466 | 0.1886 | 0.4299 |
| 12 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000475 mol) | 390 K x 1650 s @ 150 rpm → 390 K x 1650 s @ 150 rpm | yes | 0.7561 | 0.8420 | 0.9173 | 0.1656 | 0.1116 | 0.1011 | 0.4939 |

## Complete experimental actions and observations

### Batch 1

Lifecycle index: `1`; end step: `8`.

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
      "volume_L": 0.005
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000475,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1650,
      "operation": "heat",
      "stirring_speed_rpm": 150,
      "target_temperature_K": 420
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 1650,
      "operation": "heat",
      "stirring_speed_rpm": 150,
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
  "end_step": 8,
  "lifecycle_index": 1,
  "metrics": {
    "byproduct_signal": 0.2073119878768921,
    "conversion": 0.9802899360656738,
    "cost": 0.619700014591217,
    "degradation_warning": 0.1586628407239914,
    "safety_risk": 0.3195798993110657,
    "score": 0.40075621008872986,
    "selectivity": 0.7943879961967468,
    "virtual_spectrum_summary": 0.18541987240314484,
    "yield": 0.774777889251709
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
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.005
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000475,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1650,
      "operation": "heat",
      "stirring_speed_rpm": 150,
      "target_temperature_K": 390
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 1650,
      "operation": "heat",
      "stirring_speed_rpm": 150,
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
  "end_step": 16,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.17939235270023346,
    "conversion": 0.914915144443512,
    "cost": 0.619700014591217,
    "degradation_warning": 0.10509026795625687,
    "safety_risk": 0.16500824689865112,
    "score": 0.45687681436538696,
    "selectivity": 0.8151780962944031,
    "virtual_spectrum_summary": 0.14595641195774078,
    "yield": 0.7445362210273743
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
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.005
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000475,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1650,
      "operation": "heat",
      "stirring_speed_rpm": 150,
      "target_temperature_K": 405
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 1650,
      "operation": "heat",
      "stirring_speed_rpm": 150,
      "target_temperature_K": 405
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
    "byproduct_signal": 0.18657644093036652,
    "conversion": 0.9510894417762756,
    "cost": 0.619700014591217,
    "degradation_warning": 0.12790387868881226,
    "safety_risk": 0.23851171135902405,
    "score": 0.43430450558662415,
    "selectivity": 0.8041218519210815,
    "virtual_spectrum_summary": 0.16017378866672516,
    "yield": 0.7686634063720703
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
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.005
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000475,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 825,
      "operation": "heat",
      "stirring_speed_rpm": 150,
      "target_temperature_K": 420
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 825,
      "operation": "heat",
      "stirring_speed_rpm": 150,
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
  "end_step": 32,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.12198212742805481,
    "conversion": 0.8445631861686707,
    "cost": 0.6059499979019165,
    "degradation_warning": 0.062485404312610626,
    "safety_risk": 0.3188534677028656,
    "score": 0.4026380181312561,
    "selectivity": 0.892073392868042,
    "virtual_spectrum_summary": 0.09520860016345978,
    "yield": 0.7481060028076172
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
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.005
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000475,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3000,
      "operation": "heat",
      "stirring_speed_rpm": 150,
      "target_temperature_K": 390
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 3000,
      "operation": "heat",
      "stirring_speed_rpm": 150,
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
  "end_step": 40,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.29670801758766174,
    "conversion": 0.9842305183410645,
    "cost": 0.6421999931335449,
    "degradation_warning": 0.21184302866458893,
    "safety_risk": 0.1653326451778412,
    "score": 0.4216859042644501,
    "selectivity": 0.7166813611984253,
    "virtual_spectrum_summary": 0.258518785238266,
    "yield": 0.7067804932594299
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
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.005
    },
    {
      "catalyst": 0,
      "catalyst_amount_mol": 0.000475,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1650,
      "operation": "heat",
      "stirring_speed_rpm": 150,
      "target_temperature_K": 390
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 1650,
      "operation": "heat",
      "stirring_speed_rpm": 150,
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
  "end_step": 48,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.1697341352701187,
    "conversion": 0.6245474219322205,
    "cost": 0.42969998717308044,
    "degradation_warning": 0.021301299333572388,
    "safety_risk": 0.16244681179523468,
    "score": 0.31357768177986145,
    "selectivity": 0.7321256399154663,
    "virtual_spectrum_summary": 0.10293935984373093,
    "yield": 0.46040648221969604
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
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.005
    },
    {
      "catalyst": 2,
      "catalyst_amount_mol": 0.000475,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1650,
      "operation": "heat",
      "stirring_speed_rpm": 150,
      "target_temperature_K": 390
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 1650,
      "operation": "heat",
      "stirring_speed_rpm": 150,
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
  "end_step": 56,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.15440070629119873,
    "conversion": 0.7890176773071289,
    "cost": 0.5056999921798706,
    "degradation_warning": 0.04677863046526909,
    "safety_risk": 0.1637902557849884,
    "score": 0.40074655413627625,
    "selectivity": 0.8004446029663086,
    "virtual_spectrum_summary": 0.10597077012062073,
    "yield": 0.615023136138916
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
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.005
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.000475,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1650,
      "operation": "heat",
      "stirring_speed_rpm": 150,
      "target_temperature_K": 390
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 1650,
      "operation": "heat",
      "stirring_speed_rpm": 150,
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
  "end_step": 64,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.12979993224143982,
    "conversion": 0.7245748043060303,
    "cost": 0.6956999897956848,
    "degradation_warning": 0.029115023091435432,
    "safety_risk": 0.1635943353176117,
    "score": 0.38058194518089294,
    "selectivity": 0.834579586982727,
    "virtual_spectrum_summary": 0.08449172973632812,
    "yield": 0.6066675186157227
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
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.005
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.0002375,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1650,
      "operation": "heat",
      "stirring_speed_rpm": 150,
      "target_temperature_K": 390
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 1650,
      "operation": "heat",
      "stirring_speed_rpm": 150,
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
  "end_step": 72,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.1603829711675644,
    "conversion": 0.7682819366455078,
    "cost": 0.4487000107765198,
    "degradation_warning": 0.0643116757273674,
    "safety_risk": 0.16374526917934418,
    "score": 0.3962130844593048,
    "selectivity": 0.7927516102790833,
    "virtual_spectrum_summary": 0.11715088784694672,
    "yield": 0.5993808507919312
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
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.005
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.00095,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1650,
      "operation": "heat",
      "stirring_speed_rpm": 150,
      "target_temperature_K": 390
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 1650,
      "operation": "heat",
      "stirring_speed_rpm": 150,
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
  "end_step": 80,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.16635416448116302,
    "conversion": 0.9840347170829773,
    "cost": 0.9617000222206116,
    "degradation_warning": 0.13120387494564056,
    "safety_risk": 0.16566042602062225,
    "score": 0.46023571491241455,
    "selectivity": 0.8242760896682739,
    "virtual_spectrum_summary": 0.15053653717041016,
    "yield": 0.8162010312080383
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
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.005
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000475,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1650,
      "operation": "heat",
      "stirring_speed_rpm": 150,
      "target_temperature_K": 390
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 1650,
      "operation": "heat",
      "stirring_speed_rpm": 150,
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
  "end_step": 88,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.23447082936763763,
    "conversion": 0.955487072467804,
    "cost": 0.6216999888420105,
    "degradation_warning": 0.1466052234172821,
    "safety_risk": 0.18856588006019592,
    "score": 0.4298653304576874,
    "selectivity": 0.7616088390350342,
    "virtual_spectrum_summary": 0.19493131339550018,
    "yield": 0.7273476719856262
  },
  "ordinal": 11
}
```

### Batch 12

Lifecycle index: `12`; end step: `97`.

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
      "volume_L": 0.005
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000475,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1650,
      "operation": "heat",
      "stirring_speed_rpm": 150,
      "target_temperature_K": 390
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 1650,
      "operation": "heat",
      "stirring_speed_rpm": 150,
      "target_temperature_K": 390
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
  "end_step": 97,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.16560781002044678,
    "conversion": 0.9173322916030884,
    "cost": 0.6529856324195862,
    "degradation_warning": 0.11156878620386124,
    "safety_risk": 0.10111456364393234,
    "score": 0.49389901757240295,
    "selectivity": 0.8420429229736328,
    "virtual_spectrum_summary": 0.14129024744033813,
    "yield": 0.7561379075050354
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

Scope and evidence base

I completed 12 synthetic benchmark batches. Every batch used 0.003 mol limiting reagent and 0.005 L solvent. Unless stated otherwise, it used water, Catalyst B (catalog index 1), 0.000475 mol catalyst, 150 rpm stirring, and two equal heating segments separated by an HPLC measurement. Final values came from the required post-termination final assay. The reported observables are synthetic public proxies, not identities or measurements of real chemical species.

Core interpretation

The simplest account consistent with the campaign is a catalyzed network with three important processes:

1. Desired conversion of reactant R to target P.
2. Competing conversion of R, and possibly P, to byproduct B.
3. Time- and temperature-dependent degradation of P or related material to D.

A useful minimal model is:

  dR/dt = -(kP + kB) R
  dP/dt = kP R - kD P
  dB/dt = kB R + alpha*kD P
  dD/dt = (1-alpha)*kD P

with rate constants dependent on actual temperature, catalyst identity and loading, solvent, and possibly catalyst activity:

  kj = Aj(catalyst, solvent, loading, activity) * exp[-Ej/(Rgas*Tactual)]
  d(activity)/dt = -kdeact(Tactual, solvent)*activity

The deactivation term is plausible but not uniquely established. Substrate depletion plus product degradation can explain most of the observed late-time slowing and loss of selectivity without invoking deactivation.

The final-assay selectivity is numerically close to yield/conversion. For example, batch 2 gave 0.74454/0.91492 = 0.8138, close to the reported selectivity of 0.81518. The byproduct signal is also approximately 1-selectivity: batch 2 had 0.17939 versus 1-0.81518 = 0.18482, and batch 1 had 0.20731 versus 0.20561. I therefore interpret conversion as total reacted fraction, yield as surviving target fraction, selectivity as the target share of converted material, and byproduct_signal as a complementary competing-product proxy. Degradation_warning supplies additional information not completely represented by byproduct_signal.

Observed experimental matrix

Batch 1 — Catalyst B, water, 0.000475 mol catalyst, commanded 420 K for 3300 s. Midpoint HPLC at 1650 s: conversion 0.82900, yield 0.73498, selectivity 0.91438, byproduct 0.10631. Final assay: conversion 0.98029, yield 0.77478, selectivity 0.79439, byproduct 0.20731, degradation warning 0.15866, risk 0.31958.

Batch 2 — same formulation, 390 K for 3300 s. Midpoint: conversion 0.68350, yield 0.58454, selectivity 0.86074, byproduct 0.09692. Final: conversion 0.91492, yield 0.74454, selectivity 0.81518, byproduct 0.17939, degradation 0.10509, risk 0.16501.

Batch 3 — same formulation, 405 K for 3300 s. Midpoint: conversion 0.76161, yield 0.65689, selectivity 0.89827, byproduct 0.08743. Final: conversion 0.95109, yield 0.76866, selectivity 0.80412, byproduct 0.18658, degradation 0.12790, risk 0.23851.

Batch 4 — same formulation, 420 K for only 1650 s. HPLC at 825 s: conversion 0.58389, yield 0.52971, selectivity 0.92568, byproduct 0.07598. Final: conversion 0.84456, yield 0.74811, selectivity 0.89207, byproduct 0.12198, degradation 0.06249, risk 0.31885.

Batch 5 — same formulation, 390 K for 6000 s. HPLC at 3000 s: conversion 0.89240, yield 0.71962, selectivity 0.83304, byproduct 0.15482. Final: conversion 0.98423, yield 0.70678, selectivity 0.71668, byproduct 0.29671, degradation 0.21184, risk 0.16533.

Batch 6 — Catalyst A, otherwise batch-2 conditions. Midpoint: conversion 0.37522, yield 0.27207, selectivity 0.72503, byproduct 0.09346. Final: conversion 0.62455, yield 0.46041, selectivity 0.73213, byproduct 0.16973, degradation 0.02130, risk 0.16245.

Batch 7 — Catalyst C, otherwise batch-2 conditions. Midpoint: conversion 0.49103, yield 0.43616, selectivity 0.81911, byproduct 0.05638. Final: conversion 0.78902, yield 0.61502, selectivity 0.80044, byproduct 0.15440, degradation 0.04678, risk 0.16379.

Batch 8 — Catalyst D, otherwise batch-2 conditions. Midpoint: conversion 0.42402, yield 0.39095, selectivity 0.85435, byproduct 0.05055. Final: conversion 0.72457, yield 0.60667, selectivity 0.83458, byproduct 0.12980, degradation 0.02912, risk 0.16359.

Batch 9 — Catalyst B at half loading, 0.0002375 mol, otherwise batch-2 conditions. Midpoint: conversion 0.49241, yield 0.41906, selectivity 0.87492, byproduct 0.05794. Final: conversion 0.76828, yield 0.59938, selectivity 0.79275, byproduct 0.16038, degradation 0.06431, risk 0.16375.

Batch 10 — Catalyst B at double loading, 0.00095 mol, otherwise batch-2 conditions. Midpoint: conversion 0.89506, yield 0.77998, selectivity 0.93112, byproduct 0.08907. Final: conversion 0.98403, yield 0.81620, selectivity 0.82428, byproduct 0.16635, degradation 0.13120, risk 0.16566.

Batch 11 — ethanol instead of water, otherwise batch-2 conditions. Midpoint: conversion 0.80177, yield 0.65045, selectivity 0.84948, byproduct 0.11622. Final: conversion 0.95549, yield 0.72735, selectivity 0.76161, byproduct 0.23447, degradation 0.14661, risk 0.18857.

Batch 12 — nominally the batch-2 formulation and thermal program, followed by an explicit quench before termination. Midpoint: conversion 0.67491, yield 0.59723, selectivity 0.87770, byproduct 0.07439. The quench caused a reported temperature change of -45 K over 3.376 s and reduced the reported risk by 0.06389. Final: conversion 0.91733, yield 0.75614, selectivity 0.84204, byproduct 0.16561, degradation 0.11157, risk 0.10111. It also had the largest observed safe score, 0.49390.

How the explanation developed

The initial supplied model suggested that the higher-temperature side of a reference region near 420 K and 3300 s would preserve balanced performance. Batch 1 partly supported the kinetic portion: 420 K produced nearly complete conversion and high yield. It contradicted a simple claim that hotter is unconditionally better, however, because selectivity declined from 0.914 at the midpoint to 0.794 at the end, while byproduct and degradation rose markedly. Its risk, 0.3196, was also close to the 0.35 limit.

Batches 2 and 3 established a temperature-rate tradeoff. At fixed 3300 s, final conversion increased from 0.9149 at 390 K to 0.9511 at 405 K and 0.9803 at 420 K. Yield increased much less, from 0.7445 to 0.7687 to 0.7748. Meanwhile degradation increased from 0.1051 to 0.1279 to 0.1587, and risk rose from 0.1650 to 0.2385 to 0.3196. Thus temperature accelerates desired formation, but it also accelerates competing or secondary loss. The small incremental yield obtained at 420 K is not proportional to its large safety and selectivity penalties.

Batches 1, 4, and 5 clarified the time effect. At 420 K, extending the run from 1650 s (batch 4) to 3300 s (batch 1) increased conversion from 0.8446 to 0.9803 and yield by only 0.0267, while selectivity fell from 0.8921 to 0.7944 and degradation rose from 0.0625 to 0.1587. At 390 K, extending from 3300 s (batch 2) to 6000 s (batch 5) increased conversion from 0.9149 to 0.9842 but actually reduced target yield from 0.7445 to 0.7068; selectivity fell to 0.7167 and degradation doubled to 0.2118. This is strong evidence that P is not a monotonically accumulating endpoint. It reaches a broad maximum and is subsequently lost or diluted by competing products.

The catalyst series showed that Catalyst B is the most active tested catalyst under the 390 K/water conditions. Final yields were 0.4604, 0.7445, 0.6150, and 0.6067 for Catalysts A, B, C, and D, respectively. Catalysts differ in both activity and branching selectivity: Catalyst D was slower than Catalyst C but had higher final selectivity (0.8346 versus 0.8004). Therefore catalyst identity cannot be represented by one scalar activity multiplier alone; catalyst-specific effects on kP/kB are needed.

The loading series provided evidence for a positive, nonlinear Catalyst B dependence. Half loading gave final conversion/yield of 0.7683/0.5994, standard loading gave 0.9149/0.7445, and double loading gave 0.9840/0.8162. The double-loading midpoint was especially informative: conversion 0.8951, yield 0.7800, and selectivity 0.9311. More catalyst therefore greatly accelerates target formation at 390 K. The final selectivity was lower than the midpoint because secondary processes continued after much of R had been consumed. A saturating catalyst-loading function, for example kP proportional to Ccat/(KC+Ccat), is more plausible for extrapolation than indefinite linear scaling, although only three loadings were tested.

The water/ethanol comparison suggests a solvent coupling rather than a purely thermal effect. Ethanol increased midpoint conversion relative to the water batch-2 observation, but its final yield was slightly lower, selectivity substantially lower, byproduct higher, degradation higher, and risk higher. A reasonable representation is solvent-dependent multipliers on kP, kB, kD, and heat/risk response. Only water and ethanol were actually compared; no statement about acetonitrile or toluene is supported.

Thermal history and safety

The commanded setpoint is not an instantaneous actual temperature. The first 1650 s heat segments changed temperature by approximately +83.04 K at a 390 K command, +95.22 K at 405 K, and +107.05 K at 420 K. Repeating an equal segment at the same command still changed temperature by about +6.18, +8.63, and +11.44 K, respectively. This is evidence for finite thermal lag and continuing approach or overshoot, so kinetics should be integrated over Tactual(t), not evaluated only at the requested setpoint.

A minimal process model is:

  dTactual/dt = (Tcommand - Tactual)/tau + Qreaction/Ceff - Qloss(Tactual)/Ceff

with possible controller overshoot or benchmark-specific heating dynamics. The available public observations do not identify tau, heat release, or controller parameters separately.

Risk behaved primarily as a thermal-state metric rather than a simple time integral. The 420 K batches reached risks around 0.319 after both 1650 and 3300 s, whereas the 390 K batches remained near 0.165 even after 6000 s. Explicit quenching in batch 12 lowered risk from its pre-quench level by 0.06389 to 0.10111. Ethanol modestly increased risk at the same commanded thermal program. A qualitative risk model is therefore:

  risk = f(Tactual or peak Tactual, solvent, composition)

with f strongly increasing over the 390-420 K region, plus a reversible contribution that falls on cooling. Calling it purely cumulative would contradict the observed negative risk change during quench.

Predictive qualitative rules within the tested domain

• Raising temperature from 390 toward 420 K accelerates conversion but yields diminishing improvements in surviving target and disproportionately increases degradation and risk.

• Extending reaction time initially increases target yield, but after substantial conversion it decreases selectivity and can reduce yield because degradation/secondary conversion dominates.

• Catalyst B is the most productive of the four catalysts tested at 390 K in water. Catalyst identity affects both overall rate and product branching.

• Increasing Catalyst B loading from 0.0002375 to 0.00095 mol strongly increases conversion and target yield at 3300 s. The effect should not be extrapolated linearly beyond this range.

• Water was more favorable than ethanol for final selectivity, degradation, and risk under the tested conditions.

• Prompt quenching arrests the hot state and substantially lowers reported risk. Batch 12 also showed better final selectivity and yield than batch 2, but the size of the chemical improvement cannot be assigned entirely to quenching because nominal replicate batches displayed process variation and there was no pre-quench final assay in batch 12.

• For maximizing raw final yield among observed batches, batch 10 was best: 390 K, 3300 s, water, Catalyst B at 0.00095 mol, giving yield 0.8162. For balancing observed product performance and safety, batch 12 was best by the public score because explicit quenching reduced risk to 0.1011 while retaining yield 0.7561 and selectivity 0.8420.

Identifiability limits and competing explanations

1. Product degradation versus independent side reaction: declining selectivity and rising degradation_warning are consistent with P -> D, but an independent slow R -> D/B pathway with a larger activation energy could produce similar observables. No experiment started from isolated P, so sequential degradation is not uniquely proven.

2. Catalyst deactivation: late-time slowing could reflect deactivation, substrate depletion, product inhibition, or approach to a reversible limit. The present data cannot distinguish these. The high conversion obtained with double catalyst loading is compatible with deactivation being offset by more active catalyst, but it is not proof.

3. Thermal kinetics versus heat-transfer artifacts: commanded setpoints were varied, but only limited temperature-change summaries were public. Arrhenius parameters and controller dynamics cannot be separately estimated. The reported rates are effective rates along each actual thermal trajectory.

4. Quench chemistry versus cooling: batch 12 establishes the operational effect of the quench on temperature and risk. It does not establish whether quench changes product speciation, merely freezes composition, or affects the final assay response. Its final chemical outcome should be treated as suggestive rather than a clean causal estimate.

5. Measurement and process variation: the instrument noise declarations were small, but nominally comparable batches 2 and 12 differed at their midpoint. This implies batch/process variability or latent trajectory differences beyond analytical noise. Small numerical contrasts should not be overinterpreted.

6. Concentration effects: reagent amount, solvent volume, stirring speed, and sampling protocol were essentially fixed. The proposed equations are therefore local in concentration and mixing. Reaction order in R, mass-transfer limitations, and dilution effects were not identified.

7. Solvent scope: only water and ethanol were experimentally compared. Acetonitrile and toluene effects remain unknown despite being selectable materials.

8. Anonymous identities: catalysts and reaction species are benchmark categories. It would be unjustified to map them to a named real catalyst, reaction, or molecular mechanism.

Overall conclusion

Within the tested domain, this world behaves like a thermally accelerated, catalyst-dependent target-forming reaction coupled to competing product formation and later thermal degradation. Catalyst B increases the desired rate most strongly, and increased Catalyst B loading allows high conversion at the safer 390 K command. Temperature and residence time cannot be optimized independently: hotter or longer operation raises conversion but eventually sacrifices selectivity and surviving target. Actual thermal history matters because the vessel approaches the command dynamically and continues warming during repeated segments. Explicit quenching is an important termination operation because it rapidly lowers temperature and risk and plausibly arrests secondary chemistry. This account is predictive locally, but its rate constants, reaction orders, deactivation law, and exact species-level mechanism remain underdetermined by the 12-batch data.

## Q — Blind predictions

### Overall rationale

Predictions use the campaign-supported parallel target/side-product model with subsequent thermal loss of target. Temperature and time were treated as increasing both desired conversion and secondary degradation; Catalyst B loading was adjusted slightly upward from the standard campaign loading. Quenching was modeled primarily as a reduction in terminal thermal risk, with only a small chemical preservation effect. All queries use acetonitrile and 400 rpm, neither of which was tested in the campaign, so solvent and mixing uncertainty is included explicitly. Intervals are wider for 450–460 K, multistage thermal histories, and long exposures because these require extrapolation beyond the observed 390–420 K range.

### Q01

This is close to batch 1, but uses untested acetonitrile, faster stirring, and 10.5% more Catalyst B. Near-complete conversion is expected at 420 K for 3300 s, while secondary conversion lowers selectivity. The risk estimate is near or slightly above the stated safety limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2100 | 0.1300 | 0.3200 |
| conversion | 0.9850 | 0.9400 | 1.0000 |
| safety_risk | 0.3500 | 0.3000 | 0.4300 |
| score | 0.3800 | 0.2700 | 0.4700 |
| selectivity | 0.7900 | 0.6800 | 0.8700 |
| yield | 0.7800 | 0.6700 | 0.8500 |

### Q02

The pre-quench chemistry should resemble Q01 because quenching occurs after the complete heating period. Based on batch 12, quenching should sharply reduce the terminal thermal risk and may preserve a small additional amount of target, although the chemical benefit of quenching was not cleanly identified.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2000 | 0.1200 | 0.3100 |
| conversion | 0.9850 | 0.9400 | 1.0000 |
| safety_risk | 0.2400 | 0.1700 | 0.3200 |
| score | 0.4300 | 0.3300 | 0.5200 |
| selectivity | 0.8000 | 0.6900 | 0.8800 |
| yield | 0.7900 | 0.6800 | 0.8600 |

### Q03

This is closest to batch 2. The slightly greater Catalyst B loading and faster stirring should modestly raise conversion, but the unknown acetonitrile effect dominates the uncertainty. The lower temperature should keep risk and degradation well below the 420 K cases.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1900 | 0.1100 | 0.2900 |
| conversion | 0.9400 | 0.8400 | 0.9850 |
| safety_risk | 0.1800 | 0.1300 | 0.2400 |
| score | 0.4500 | 0.3500 | 0.5300 |
| selectivity | 0.8100 | 0.7100 | 0.8900 |
| yield | 0.7600 | 0.6500 | 0.8400 |

### Q04

At 450 K for 3300 s, conversion should saturate, but extrapolation from batches 1, 3, and 4 predicts substantially faster secondary loss and a safety-limit violation. This temperature is outside the experimentally tested range, so the intervals are deliberately wide.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3400 | 0.2000 | 0.5300 |
| conversion | 0.9980 | 0.9700 | 1.0000 |
| safety_risk | 0.5200 | 0.4200 | 0.6500 |
| score | 0.2400 | 0.0700 | 0.3900 |
| selectivity | 0.6600 | 0.4700 | 0.7900 |
| yield | 0.6600 | 0.4700 | 0.7900 |

### Q05

This resembles the short 420 K batch 4, where target yield was already high and selectivity remained much better than after 3300 s. The higher catalyst loading may slightly increase conversion. Risk is governed mainly by the high terminal thermal state rather than duration.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1100 | 0.0500 | 0.2000 |
| conversion | 0.8600 | 0.7300 | 0.9400 |
| safety_risk | 0.3500 | 0.2900 | 0.4300 |
| score | 0.4000 | 0.3000 | 0.4900 |
| selectivity | 0.8900 | 0.8000 | 0.9500 |
| yield | 0.7600 | 0.6500 | 0.8400 |

### Q06

The extended 420 K exposure should drive essentially complete conversion but carry the reaction well beyond the target-yield maximum. Batch 5 showed that long residence time can reduce yield despite increasing conversion; at 420 K this loss should be stronger.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3900 | 0.2500 | 0.5700 |
| conversion | 0.9990 | 0.9800 | 1.0000 |
| safety_risk | 0.3500 | 0.3000 | 0.4400 |
| score | 0.2900 | 0.1200 | 0.4200 |
| selectivity | 0.6100 | 0.4300 | 0.7500 |
| yield | 0.6100 | 0.4300 | 0.7500 |

### Q07

The initial 390 K segment should form target with moderate selectivity, after which the 450 K segment rapidly completes conversion and accelerates secondary loss. Because the hot segment is last, terminal risk should remain high. Order-dependent thermal lag adds uncertainty.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2800 | 0.1600 | 0.4400 |
| conversion | 0.9950 | 0.9500 | 1.0000 |
| safety_risk | 0.5100 | 0.4000 | 0.6400 |
| score | 0.2900 | 0.1200 | 0.4300 |
| selectivity | 0.7200 | 0.5600 | 0.8400 |
| yield | 0.7200 | 0.5600 | 0.8300 |

### Q08

A hot first segment should create target rapidly but expose it to secondary conversion during the following segment. Cooling toward 390 K before termination should reduce terminal risk relative to Q07. The amount of cooling and the distinction between peak and current-state risk are not fully identified.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3000 | 0.1700 | 0.4700 |
| conversion | 0.9900 | 0.9300 | 1.0000 |
| safety_risk | 0.2700 | 0.1800 | 0.4000 |
| score | 0.3700 | 0.2100 | 0.4900 |
| selectivity | 0.7000 | 0.5300 | 0.8300 |
| yield | 0.6900 | 0.5200 | 0.8100 |

### Q09

The short 440 K treatment should give more conversion than batch 4 while retaining better selectivity than a long high-temperature run. Its terminal thermal risk is nevertheless expected to exceed the safety limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1600 | 0.0800 | 0.2800 |
| conversion | 0.9300 | 0.8200 | 0.9850 |
| safety_risk | 0.4500 | 0.3700 | 0.5600 |
| score | 0.3400 | 0.2000 | 0.4600 |
| selectivity | 0.8400 | 0.7200 | 0.9200 |
| yield | 0.7800 | 0.6600 | 0.8600 |

### Q10

Chemistry should be close to Q09, but the explicit quench should substantially lower the terminal risk and improve the score. Any direct improvement in chemical yield or selectivity is predicted to be small because the quench follows the entire heat exposure.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1500 | 0.0700 | 0.2700 |
| conversion | 0.9300 | 0.8200 | 0.9850 |
| safety_risk | 0.3000 | 0.2100 | 0.4000 |
| score | 0.4100 | 0.2900 | 0.5100 |
| selectivity | 0.8500 | 0.7300 | 0.9300 |
| yield | 0.7900 | 0.6700 | 0.8700 |

### Q11

The 370 K command should be much safer but kinetically slower. The long duration partly compensates for the lower temperature, while still permitting some secondary conversion. This is a temperature extrapolation below the campaign range, so conversion is relatively uncertain.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1900 | 0.0900 | 0.3200 |
| conversion | 0.8300 | 0.6500 | 0.9400 |
| safety_risk | 0.1100 | 0.0700 | 0.1700 |
| score | 0.4300 | 0.3100 | 0.5300 |
| selectivity | 0.8100 | 0.6800 | 0.9000 |
| yield | 0.6700 | 0.5200 | 0.7800 |

### Q12

This combines the highest temperature and longest duration in the prediction set. Conversion should be complete, but the campaign's time and temperature trends imply extensive destruction or diversion of target, high byproduct signal, and a severe safety penalty. It is a large extrapolation, reflected in the broad intervals.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7200 | 0.4800 | 0.9100 |
| conversion | 1.0000 | 0.9850 | 1.0000 |
| safety_risk | 0.6200 | 0.4800 | 0.7900 |
| score | 0.0700 | 0.0000 | 0.2200 |
| selectivity | 0.2800 | 0.0900 | 0.5200 |
| yield | 0.2800 | 0.0900 | 0.5200 |

## K2 — Retrospective analysis

1. Assessment of the initial information

The initial packet contained one substantive process claim: near the reference region of 420 K and 3300 s, “the higher-temperature side should retain safe balanced performance more reliably than the lower-temperature side.” It also warned that a temperature-bound rollback should count as evidence against an attempted condition rather than as missing output. The remaining material information was mainly structural: catalysts were anonymous categories, solvent effects were categorical benchmark effects, and no task-specific property dossier was supplied.

The kinetic portion of the temperature claim received support. At 3300 s with the reference water/Catalyst B formulation, conversion rose from 0.9149 in batch 2 at 390 K to 0.9511 in batch 3 at 405 K and 0.9803 in batch 1 at 420 K. Thus the higher-temperature side produced faster and more complete conversion.

The stronger claim about retaining “safe balanced performance” was contradicted within the tested range. Over the same series, risk rose from 0.1650 to 0.2385 to 0.3196, selectivity fell overall from 0.8152 at 390 K to 0.7944 at 420 K, and degradation_warning rose from 0.1051 to 0.1587. Yield increased only modestly, from 0.7445 to 0.7748. Batch 4 reinforced the distinction between rapid formation and balanced operation: 420 K for only 1650 s gave yield 0.7481 and selectivity 0.8921, but risk was already 0.3189. In K1 I therefore revised the initial statement into a tradeoff: temperature accelerates desired formation but also increases secondary loss and safety risk.

This is genuine counterevidence that was incorporated, not merely an absence of confirmation. However, I did not test temperatures above 420 K during the campaign, so I did not directly test the packet’s rollback statement. No attempted operation was rolled back. Consequently, the behavior of the system at a hard thermal boundary remained untested; it would be incorrect to say that the lack of a rollback supported safe operation at 450–460 K.

The initial reference formulation also implicitly favored water, Catalyst B, 0.000475 mol catalyst, and 150 rpm. Catalyst B was subsequently supported as the most productive tested catalyst under the common 390 K conditions. Water was better than ethanol for final selectivity, degradation, and risk in the one comparison. Nevertheless, neither of these findings validates the reference choices universally. Acetonitrile, toluene, concentration effects, and stirring-speed effects were not tested.

2. Experiments that formed or changed the account

Batch 1 was chosen primarily from the supplied reference region rather than from campaign evidence. It established that the nominal reference could produce high conversion and yield, but its midpoint-to-final change first suggested that target formation was followed by secondary loss: selectivity fell from 0.9144 to 0.7944 while byproduct_signal rose from 0.1063 to 0.2073.

Batches 2 and 3 were the most important temperature comparisons. They changed my view from the supplied “higher is more reliable” expectation to a rate–selectivity–risk tradeoff. Batch 2 showed that 390 K retained much of the 420 K yield at roughly half the risk. Batch 3 demonstrated a graded response at 405 K rather than a simple threshold.

Batches 4 and 5 were the clearest mechanistic time tests. Batch 4 showed that short exposure at 420 K could give substantial target formation before severe selectivity loss. Batch 5 showed that extending a 390 K run to 6000 s increased conversion to 0.9842 but reduced yield to 0.7068 and selectivity to 0.7167. That observation was central to the K1 statement that the target is “not a monotonically accumulating endpoint.” It strongly motivated a sequential-loss term, although it did not uniquely prove one.

Batches 6–8 were deliberately diagnostic rather than score-seeking. They established that catalyst identity changes both rate and branching: Catalyst B gave the highest final yield, while Catalyst D was slower but more selective than Catalyst C. This prevented me from treating catalyst identity as only a scalar activity multiplier.

Batches 9 and 10 tested Catalyst B loading. Batch 10 materially changed the operational picture: doubling the loading gave midpoint conversion 0.8951, yield 0.7800, and selectivity 0.9311 at 390 K, followed by final yield 0.8162. This showed that catalyst loading could substitute partly for higher temperature. My suggestion of a saturating loading response was an extrapolative modeling choice, not something established by only three loading levels.

Batch 11 was selected to test a solvent effect, but choosing ethanol rather than acetonitrile or toluene was an unvalidated design choice. It showed faster conversion but worse final branching and risk than the water comparator. One solvent contrast was insufficient to map the categorical solvent space.

Batch 12 was motivated by the growing evidence that termination timing and cooling mattered. It established the operational effect of quenching on temperature and reported risk: the quench changed temperature by -45 K and risk by -0.06389. Its favorable final result led to the sealed recommendation. However, attributing its chemical differences from batch 2 entirely to quenching would be unjustified because batch 12 had no final-quality assay immediately before the quench, and the nominally similar batches already differed at the midpoint.

Several choices remained guess-based. I used the same concentration and mostly the same stirring speed throughout, assumed that one midpoint HPLC measurement per batch was a good use of the instrument budget, and did not reserve batches for true replication. I also avoided more extreme temperatures because of the safety objective. Those were defensible operational choices, but they limited mechanism identification.

3. Principal competing mechanisms and what the data distinguish

The K1 working model was a network in which reactant R forms target P and competing byproduct B, followed by thermal loss of P to degradation products. The most important competitor is a purely parallel network in which R independently forms P, B, and D, with no substantial conversion of P after formation.

The evidence favors, but does not prove, sequential target loss. The strongest evidence is batch 5: after long heating, conversion increased while target yield decreased and degradation_warning increased. Likewise, extending 420 K exposure from batch 4 to batch 1 produced only a small yield gain but a large selectivity and degradation penalty. These behaviors are naturally explained by P → D or P → B. A sufficiently slow, high-activation-energy parallel R → D/B channel can nevertheless mimic them as R is consumed, especially because no isolated target was introduced and no species-resolved mass balance was available.

A second competition is catalyst deactivation versus ordinary substrate depletion, product inhibition, or reversible chemistry. Declining incremental conversion at late times does not by itself demonstrate deactivation. The strong response to doubled catalyst loading is compatible with deactivation, but it is equally compatible with normal positive catalyst order. The campaign lacked a catalyst-spike experiment after an observed slowdown, so these alternatives remain unresolved.

A third competition concerns thermal history. The observed temperature changes support a finite-lag thermal process, but they do not distinguish controller inertia, reaction heat, solvent-dependent heat transfer, and benchmark-specific overshoot. Consequently, fitted kinetic effects would be effective effects along actual trajectories, not intrinsic Arrhenius constants.

A fourth competition concerns quenching. It may merely cool the vessel and freeze composition, it may chemically alter intermediates, or it may alter assay-visible speciation. Batch 12 clearly demonstrates cooling and lower terminal risk, but it cannot distinguish these chemical interpretations.

The catalyst data do distinguish a one-dimensional catalyst ranking from a richer branching model: Catalyst C and Catalyst D did not preserve the same rate/selectivity relationship, so identity must affect more than overall rate. The experiments also distinguish a cumulative-only risk model from one having a reversible state component, because risk decreased during quenching. They do not establish whether the remaining risk depends on current temperature, peak temperature, accumulated exposure, or a combination.

4. One additional complete experiment

If only one additional legal complete experiment were available, I would use a path-switch experiment in the well-characterized water/Catalyst B system rather than test another material. I would charge 0.003 mol reagent, 0.005 L water, and 0.00095 mol Catalyst B; heat at 390 K for approximately 1650 s; obtain an HPLC measurement; then heat at 420 K for approximately 1500 s; quench immediately; terminate; and perform the final assay.

The doubled catalyst loading is intentional: batch 10 showed that it can create a high target inventory and high conversion early at 390 K. The subsequent temperature increase would then test what happens to an already target-rich mixture rather than simply asking whether high temperature accelerates initial formation. The quench would define the endpoint and reduce unnecessary post-program thermal ambiguity.

If conversion increased during the second stage while yield stayed constant or increased proportionally and selectivity remained high, I would weaken the sequential-degradation interpretation and favor predominantly parallel formation pathways.

If conversion increased only modestly but yield fell, while byproduct_signal and degradation_warning rose strongly, I would strengthen the P → D/B interpretation. That would show loss after a substantial target inventory had already formed.

If the second stage produced much less change than predicted despite appreciable residual reactant, I would increase the plausibility of catalyst deactivation, product inhibition, or a reversible limit. It would not distinguish those three by itself, but it would show that substrate depletion alone was inadequate.

If the second stage caused an unexpectedly strong conversion jump without corresponding degradation, I would infer that the high-temperature penalty depends more on prolonged exposure than on temperature alone and revise the effective activation-energy ordering.

This single experiment would still not be as decisive as introducing isolated target or running matched order-reversed batches, neither of which was available as one legal campaign batch. It is therefore the best feasible discriminator, not a definitive mechanism test.

5. Tradeoff between identifiability and operational score

The research goal explicitly prioritized explanatory and predictive understanding over the public safe score. I therefore spent multiple batches on conditions expected to underperform operationally. Batches 5–9 are examples: the long-time batch, alternative catalysts, and half-loading condition were valuable for mechanism discrimination but were not plausible score maxima. This sacrificed short-term score in exchange for identifying time dependence, catalyst branching, and loading response.

Conversely, batch 10 moved toward optimization after the catalyst and temperature trends were clearer. It found the highest observed raw yield by combining the safer 390 K command with higher Catalyst B loading. Batch 12 also had an optimization component: it combined the favorable 390 K region with explicit quenching and produced the highest observed public score.

Some choices compromised identifiability to preserve safety. I did not test 450 or 460 K, so the high-temperature curvature, rollback behavior, and catastrophic-degradation regime remained extrapolations. I also retained water for most batches instead of mapping all four solvents, because this maintained comparability and reduced the risk of spending scarce batches on poorly performing categorical conditions.

There were also cases where optimization reduced causal clarity. Batch 12 was the only explicit quench batch, and its favorable result was used for the recommendation even though a clean paired pre-quench endpoint was absent. A stronger mechanism design would have included replicated quenched and unquenched batches under identical trajectories. Similarly, doubling catalyst in batch 10 improved performance but did not by itself distinguish saturation, deactivation compensation, or ordinary catalyst order.

The repeated midpoint HPLC measurements were a productive identifiability choice, because they exposed within-batch evolution. However, using the same midpoint structure in almost every batch meant that I did not allocate measurements to denser time courses or true replicates. The design was broad and exploratory rather than statistically optimal.

6. Underused evidence and weaknesses in the blind predictions

The largest underused evidence source was the raw characterization output. I relied on processed conversion, yield, selectivity, byproduct, and degradation estimates and did not inspect the detailed public spectral artifacts. Peak assignments or mass-balance structure might have helped determine whether degradation and byproduct channels were distinct or merely correlated proxies.

I also did not quantitatively fit the temperature-change observations. K1 noted first-segment changes of about +83.04 K, +95.22 K, and +107.05 K for 390, 405, and 420 K commands, followed by additional changes during the second segments. These observations were used qualitatively but not converted into an estimated thermal time constant or explicit trajectory model. The cost and score observations were likewise not used to identify the exact scoring function, making all blind score predictions less secure than the chemistry predictions.

The midpoint data were informative but difficult to combine rigorously with final assays because HPLC and final_assay had different uncertainty structures. Sampling also removed 0.0002 L before the second segment. That change was small but systematic. I treated midpoint-to-final changes mainly as reaction evolution without explicitly propagating cross-instrument and sampling effects.

The nominal similarity of batches 2 and 12 revealed more process variability than the declared analytical noise alone would suggest. I acknowledged this in K1, but the blind prediction intervals for some near-reference cases were probably still too narrow.

All 12 blind queries used acetonitrile and 400 rpm, whereas the campaign tested neither acetonitrile nor stirring-speed variation. Therefore even Q01–Q03 and Q05, which otherwise resembled observed thermal programs, were not close interpolations. Their conversion, yield, selectivity, byproduct, and risk intervals likely understated categorical solvent and mixing uncertainty. This is in tension with K1’s explicit statement that only water and ethanol had been compared and that the account was local in concentration and mixing.

Q04 and Q12 were especially unreliable because 450 and 460 K were beyond the observed 420 K maximum. Q12 also combined 460 K with 6300 s, outside both the tested temperature and joint temperature–time domain. Although its yield and selectivity intervals were broad, the conversion interval of 0.985–1.0 was too confident. It omitted the initial packet’s possibility of a temperature-bound rollback or other safety-constrained behavior.

Q07 and Q08 were highly uncertain because no order-reversed thermal programs were run. Their differing risk estimates assumed that terminal thermal state mattered substantially, but K1 had not identified the relative roles of peak temperature, current temperature, and accumulated exposure. Those risk intervals may therefore have been too narrow.

Q02 and Q10 were also weak because the chemical effect of quenching had only one confounded precedent. Predicting small yield and selectivity improvements from quenching went beyond what batch 12 cleanly established. The risk direction was well supported; the magnitude at 420–440 K was extrapolative.

Q11 extrapolated below the observed temperature range. Its relatively narrow safety interval was more defensible than its kinetic interval, but the assumed compensation between 370 K and 5700 s depended on an unestimated activation energy.

Finally, every blind score interval inherited uncertainty from an unidentified scoring equation. I used analogies to observed batches rather than a fitted public-score law. Those score ranges should have been wider, particularly where risk might cross the 0.35 constraint or an operation might be rolled back.

7. Limitations of the sealed recommendation

The sealed recommendation selected batch 12 because it had the highest observed safe score, 0.4939, with yield 0.7561, selectivity 0.8420, and risk 0.1011 after quenching. This is a sample-in statement: it was the best of the 12 completed batches under the observed noisy outcomes and the public scoring rule.

It is not proof of global or even local optimality. Batch 12 was only one realization, only one explicit quench experiment was run, and no exact replicate was available. Batch 10 had a materially higher raw yield of 0.8162, so the preferred operation depends on whether the objective emphasizes score, safety, yield, selectivity, cost, or robustness. The batch-12 advantage may also include process variation unrelated to quenching.

Repeatability should first be tested with several exact replicates of batch 12, including identical operation order and quench timing. A matched unquenched control should be interleaved rather than compared retrospectively with a single earlier batch. Pre-quench and post-quench measurements would help separate compositional preservation from a purely thermal-risk effect.

Local robustness should be evaluated around the chosen point with small structured perturbations: for example 385/390/395 K, approximately 3000/3300/3600 s, modestly varied Catalyst B loading, and slightly altered quench timing. The objective should be a response surface with uncertainty, not another isolated maximum. A condition whose mean score is marginally higher but whose risk frequently crosses 0.35 would not be robustly preferable.

Material robustness requires repeating the local design across catalyst identities and solvents. Batch 11 already showed that changing water to ethanol altered both chemistry and risk. Nothing in the campaign established that the recommended thermal and quench policy transfers to acetonitrile or toluene, or even that Catalyst B remains best in those solvents.

Cross-world generalization is still weaker. The catalysts and kinetic effects were anonymous benchmark categories with latent categorical profiles. A recommendation in this world should not be treated as a named real-chemistry recipe or assumed to transfer to another hidden world with different thermal or catalytic parameters.

Accordingly, the correct claim is: batch 12 was the highest-scoring observed member of a sparse 12-point campaign and is a reasonable candidate for confirmatory testing. The unsupported stronger claim would be that 390 K, 3300 s, standard Catalyst B loading, water, and quenching is already proven optimal.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 111.3 | none | 0 |
| Q | yes | 0 | 107.5 | none | 0 |
| K2 | yes | 0 | 129.2 | none | 0 |

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean 80% width | Mean interval score |
|---|---:|---:|---:|---:|
| byproduct_signal | 0.1855 | 0.3167 | 0.2500 | 0.8441 |
| conversion | 0.0415 | 0.6333 | 0.1067 | 0.2022 |
| safety_risk | 0.0805 | 0.5000 | 0.1792 | 0.2934 |
| score | 0.0794 | 0.7833 | 0.2408 | 0.2583 |
| selectivity | 0.1772 | 0.3333 | 0.2483 | 0.7896 |
| yield | 0.1410 | 0.4333 | 0.2525 | 0.5719 |

## Predictions versus released reference truth

### Q01

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2100 | 0.1300 | 0.3200 | 0.4503 | 0.4469, 0.4662, 0.4467, 0.4450, 0.4467 |
| conversion | 0.9850 | 0.9400 | 1.0000 | 0.9938 | 1.0000, 1.0000, 0.9860, 0.9873, 0.9956 |
| safety_risk | 0.3500 | 0.3000 | 0.4300 | 0.2983 | 0.2983, 0.2983, 0.2983, 0.2983, 0.2983 |
| score | 0.3800 | 0.2700 | 0.4700 | 0.2654 | 0.2635, 0.2685, 0.2680, 0.2631, 0.2639 |
| selectivity | 0.7900 | 0.6800 | 0.8700 | 0.5546 | 0.5563, 0.5738, 0.5478, 0.5381, 0.5570 |
| yield | 0.7800 | 0.6700 | 0.8500 | 0.5493 | 0.5420, 0.5435, 0.5619, 0.5554, 0.5436 |
### Q02

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2000 | 0.1200 | 0.3100 | 0.4565 | 0.4617, 0.4629, 0.4545, 0.4442, 0.4594 |
| conversion | 0.9850 | 0.9400 | 1.0000 | 1.0000 | 1.0000, 1.0000, 1.0000, 1.0000, 1.0000 |
| safety_risk | 0.2400 | 0.1700 | 0.3200 | 0.1511 | 0.1511, 0.1511, 0.1511, 0.1511, 0.1511 |
| score | 0.4300 | 0.3300 | 0.5200 | 0.3276 | 0.3307, 0.3368, 0.3227, 0.3239, 0.3239 |
| selectivity | 0.8000 | 0.6900 | 0.8800 | 0.5523 | 0.5540, 0.5733, 0.5405, 0.5400, 0.5537 |
| yield | 0.7900 | 0.6800 | 0.8600 | 0.5474 | 0.5539, 0.5572, 0.5426, 0.5458, 0.5372 |
### Q03

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1900 | 0.1100 | 0.2900 | 0.3766 | 0.3794, 0.3709, 0.3819, 0.3900, 0.3609 |
| conversion | 0.9400 | 0.8400 | 0.9850 | 0.9967 | 1.0000, 1.0000, 0.9889, 1.0000, 0.9944 |
| safety_risk | 0.1800 | 0.1300 | 0.2400 | 0.1857 | 0.1857, 0.1857, 0.1857, 0.1857, 0.1857 |
| score | 0.4500 | 0.3500 | 0.5300 | 0.3684 | 0.3706, 0.3671, 0.3652, 0.3719, 0.3673 |
| selectivity | 0.8100 | 0.7100 | 0.8900 | 0.6293 | 0.6322, 0.6263, 0.6308, 0.6343, 0.6231 |
| yield | 0.7600 | 0.6500 | 0.8400 | 0.6327 | 0.6355, 0.6305, 0.6258, 0.6375, 0.6344 |
### Q04

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3400 | 0.2000 | 0.5300 | 0.5283 | 0.5341, 0.5287, 0.5215, 0.5298, 0.5274 |
| conversion | 0.9980 | 0.9700 | 1.0000 | 0.9965 | 1.0000, 0.9988, 0.9941, 1.0000, 0.9895 |
| safety_risk | 0.5200 | 0.4200 | 0.6500 | 0.4035 | 0.4035, 0.4035, 0.4035, 0.4035, 0.4035 |
| score | 0.2400 | 0.0700 | 0.3900 | 0.1753 | 0.1761, 0.1753, 0.1756, 0.1755, 0.1738 |
| selectivity | 0.6600 | 0.4700 | 0.7900 | 0.4844 | 0.4790, 0.4868, 0.4792, 0.4926, 0.4847 |
| yield | 0.6600 | 0.4700 | 0.7900 | 0.4854 | 0.4900, 0.4836, 0.4902, 0.4801, 0.4833 |
### Q05

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1100 | 0.0500 | 0.2000 | 0.2240 | 0.2127, 0.2190, 0.2346, 0.2243, 0.2295 |
| conversion | 0.8600 | 0.7300 | 0.9400 | 0.9780 | 0.9698, 0.9860, 0.9851, 0.9824, 0.9669 |
| safety_risk | 0.3500 | 0.2900 | 0.4300 | 0.2987 | 0.2987, 0.2987, 0.2987, 0.2987, 0.2987 |
| score | 0.4000 | 0.3000 | 0.4900 | 0.4067 | 0.4069, 0.4023, 0.4073, 0.4084, 0.4085 |
| selectivity | 0.8900 | 0.8000 | 0.9500 | 0.7769 | 0.7760, 0.7624, 0.7815, 0.7800, 0.7844 |
| yield | 0.7600 | 0.6500 | 0.8400 | 0.7642 | 0.7673, 0.7603, 0.7611, 0.7654, 0.7667 |
### Q06

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3900 | 0.2500 | 0.5700 | 0.6220 | 0.6125, 0.6145, 0.6156, 0.6437, 0.6239 |
| conversion | 0.9990 | 0.9800 | 1.0000 | 0.9956 | 0.9990, 1.0000, 0.9906, 0.9940, 0.9944 |
| safety_risk | 0.3500 | 0.3000 | 0.4400 | 0.2979 | 0.2979, 0.2979, 0.2979, 0.2979, 0.2979 |
| score | 0.2900 | 0.1200 | 0.4200 | 0.1604 | 0.1639, 0.1597, 0.1587, 0.1595, 0.1599 |
| selectivity | 0.6100 | 0.4300 | 0.7500 | 0.3931 | 0.3923, 0.3900, 0.3880, 0.4025, 0.3925 |
| yield | 0.6100 | 0.4300 | 0.7500 | 0.3905 | 0.3990, 0.3897, 0.3908, 0.3829, 0.3901 |
### Q07

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2800 | 0.1600 | 0.4400 | 0.4961 | 0.4975, 0.4926, 0.5053, 0.4934, 0.4915 |
| conversion | 0.9950 | 0.9500 | 1.0000 | 0.9933 | 0.9948, 0.9899, 0.9907, 0.9910, 1.0000 |
| safety_risk | 0.5100 | 0.4000 | 0.6400 | 0.4274 | 0.4274, 0.4274, 0.4274, 0.4274, 0.4274 |
| score | 0.2900 | 0.1200 | 0.4300 | 0.1786 | 0.1762, 0.1787, 0.1795, 0.1720, 0.1868 |
| selectivity | 0.7200 | 0.5600 | 0.8400 | 0.5091 | 0.4941, 0.5185, 0.5054, 0.5066, 0.5207 |
| yield | 0.7200 | 0.5600 | 0.8300 | 0.5068 | 0.5097, 0.5018, 0.5120, 0.4923, 0.5182 |
### Q08

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3000 | 0.1700 | 0.4700 | 0.5022 | 0.5042, 0.5091, 0.4928, 0.4979, 0.5072 |
| conversion | 0.9900 | 0.9300 | 1.0000 | 0.9991 | 1.0000, 0.9954, 1.0000, 1.0000, 1.0000 |
| safety_risk | 0.2700 | 0.1800 | 0.4000 | 0.1973 | 0.1973, 0.1973, 0.1973, 0.1973, 0.1973 |
| score | 0.3700 | 0.2100 | 0.4900 | 0.2871 | 0.2870, 0.2882, 0.2802, 0.2860, 0.2941 |
| selectivity | 0.7000 | 0.5300 | 0.8300 | 0.5111 | 0.5264, 0.5157, 0.4835, 0.5021, 0.5279 |
| yield | 0.6900 | 0.5200 | 0.8100 | 0.5163 | 0.5063, 0.5171, 0.5160, 0.5190, 0.5232 |
### Q09

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1600 | 0.0800 | 0.2800 | 0.2551 | 0.2478, 0.2551, 0.2557, 0.2586, 0.2585 |
| conversion | 0.9300 | 0.8200 | 0.9850 | 0.9888 | 0.9803, 0.9874, 0.9938, 0.9911, 0.9914 |
| safety_risk | 0.4500 | 0.3700 | 0.5600 | 0.3780 | 0.3780, 0.3780, 0.3780, 0.3780, 0.3780 |
| score | 0.3400 | 0.2000 | 0.4600 | 0.3587 | 0.3576, 0.3632, 0.3586, 0.3556, 0.3583 |
| selectivity | 0.8400 | 0.7200 | 0.9200 | 0.7559 | 0.7496, 0.7587, 0.7564, 0.7553, 0.7596 |
| yield | 0.7800 | 0.6600 | 0.8600 | 0.7437 | 0.7471, 0.7537, 0.7420, 0.7358, 0.7399 |
### Q10

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1500 | 0.0700 | 0.2700 | 0.2502 | 0.2529, 0.2556, 0.2474, 0.2418, 0.2531 |
| conversion | 0.9300 | 0.8200 | 0.9850 | 0.9895 | 0.9937, 0.9834, 0.9945, 0.9943, 0.9816 |
| safety_risk | 0.3000 | 0.2100 | 0.4000 | 0.1718 | 0.1718, 0.1718, 0.1718, 0.1718, 0.1718 |
| score | 0.4100 | 0.2900 | 0.5100 | 0.4472 | 0.4450, 0.4479, 0.4492, 0.4470, 0.4470 |
| selectivity | 0.8500 | 0.7300 | 0.9300 | 0.7487 | 0.7486, 0.7516, 0.7418, 0.7498, 0.7516 |
| yield | 0.7900 | 0.6700 | 0.8700 | 0.7459 | 0.7395, 0.7473, 0.7538, 0.7433, 0.7454 |
### Q11

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1900 | 0.0900 | 0.3200 | 0.5042 | 0.5026, 0.5049, 0.5110, 0.4947, 0.5079 |
| conversion | 0.8300 | 0.6500 | 0.9400 | 0.9947 | 0.9891, 0.9869, 1.0000, 0.9984, 0.9993 |
| safety_risk | 0.1100 | 0.0700 | 0.1700 | 0.1547 | 0.1547, 0.1547, 0.1547, 0.1547, 0.1547 |
| score | 0.4300 | 0.3100 | 0.5300 | 0.2976 | 0.2974, 0.3007, 0.2905, 0.2975, 0.3018 |
| selectivity | 0.8100 | 0.6800 | 0.9000 | 0.5042 | 0.5154, 0.5160, 0.4770, 0.5024, 0.5103 |
| yield | 0.6700 | 0.5200 | 0.7800 | 0.5044 | 0.4984, 0.5069, 0.5023, 0.5044, 0.5099 |
### Q12

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.7200 | 0.4800 | 0.9100 | 0.8008 | 0.7912, 0.7944, 0.8024, 0.8120, 0.8042 |
| conversion | 1.0000 | 0.9850 | 1.0000 | 0.9991 | 1.0000, 0.9954, 1.0000, 1.0000, 1.0000 |
| safety_risk | 0.6200 | 0.4800 | 0.7900 | 0.4203 | 0.4203, 0.4203, 0.4203, 0.4203, 0.4203 |
| score | 0.0700 | 0.0000 | 0.2200 | 0.0000 | 0.0000, 0.0000, 0.0000, 0.0000, 0.0000 |
| selectivity | 0.2800 | 0.0900 | 0.5200 | 0.2143 | 0.2309, 0.1960, 0.2230, 0.2062, 0.2153 |
| yield | 0.2800 | 0.0900 | 0.5200 | 0.2193 | 0.2180, 0.2146, 0.2252, 0.2157, 0.2233 |

## Recommendation retest

- Selected source batch: `12`
- Retest exact replay verified: `True`
- Retest failure: `none`

| Metric | Selected source batch | Independent retest | Retest minus source |
|---|---:|---:|---:|
| byproduct_signal | 0.1656 | 0.1711 | 0.0055 |
| conversion | 0.9173 | 0.9209 | 0.0036 |
| cost | 0.6530 | 0.6530 | 0.0000 |
| degradation_warning | 0.1116 | 0.1076 | -0.0040 |
| safety_risk | 0.1011 | 0.1011 | 0.0000 |
| score | 0.4939 | 0.4858 | -0.0081 |
| selectivity | 0.8420 | 0.8352 | -0.0068 |
| virtual_spectrum_summary | 0.1413 | 0.1425 | 0.0012 |
| yield | 0.7561 | 0.7392 | -0.0170 |

## Scope note

This is the final sanitized report produced after all 60 source sessions and K1/Q/K2 chains were sealed. It includes released reference truth, blind-prediction evaluation, and the independent recommendation retest. Provider-private event streams, credentials, thread identifiers, and token accounting remain excluded.
