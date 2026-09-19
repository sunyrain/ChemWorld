# RX-W05--P--safety_constrained_optimization--Aligned

## Run summary

- World: `RX-W05`
- Locus: `P`
- Goal: `safety_constrained_optimization`
- Arm: `Aligned`
- Status: `completed`
- Source status: `completed`
- Experimental sessions: `12/12`
- Operations: `84`
- Exact replay verified: `True`
- Rollbacks: `[]`
- Posttest chain sealed: `True`

### Recovery status

No recovery override was required for this task.

## Sealed recommendation

- Selected batch: `11`
- Rationale: Experiment 11 achieved the highest completed-batch public safe score (0.4598) while keeping safety risk (0.1273) well below the 0.35 limit.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S0 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 410 K x 3300 s @ 600 rpm | no | 0.7655 | 0.8202 | 0.9335 | 0.1628 | 0.1259 | 0.1816 | 0.4488 |
| 2 | S0 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 400 K x 4200 s @ 600 rpm | no | 0.7459 | 0.7913 | 0.9661 | 0.2061 | 0.1408 | 0.1430 | 0.4536 |
| 3 | S0 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 390 K x 5000 s @ 600 rpm | no | 0.7348 | 0.7723 | 0.9655 | 0.2214 | 0.1482 | 0.1143 | 0.4567 |
| 4 | S1 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 390 K x 5000 s @ 600 rpm | no | 0.6254 | 0.6609 | 0.9827 | 0.3417 | 0.2739 | 0.1375 | 0.3760 |
| 5 | S2 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 390 K x 5000 s @ 600 rpm | no | 0.6467 | 0.6428 | 0.9797 | 0.3472 | 0.2903 | 0.1557 | 0.3710 |
| 6 | S3 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 390 K x 5000 s @ 600 rpm | no | 0.5245 | 0.5516 | 0.9668 | 0.4665 | 0.3138 | 0.1676 | 0.2930 |
| 7 | S0 (0.0075 L) | 0.003000 mol | C0 (0.000525 mol) | 390 K x 5000 s @ 600 rpm | no | 0.6716 | 0.7793 | 0.8538 | 0.1878 | 0.0668 | 0.1134 | 0.4518 |
| 8 | S0 (0.0075 L) | 0.003000 mol | C1 (0.000525 mol) | 390 K x 5000 s @ 600 rpm | no | 0.6953 | 0.7414 | 0.9399 | 0.2587 | 0.1415 | 0.1139 | 0.4391 |
| 9 | S0 (0.0075 L) | 0.003000 mol | C2 (0.000525 mol) | 390 K x 5000 s @ 600 rpm | no | 0.5266 | 0.6595 | 0.7852 | 0.2715 | 0.0607 | 0.1124 | 0.3490 |
| 10 | S0 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 385 K x 5500 s @ 600 rpm | no | 0.7236 | 0.7502 | 0.9792 | 0.2282 | 0.1578 | 0.1037 | 0.4524 |
| 11 | S0 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 395 K x 4500 s @ 600 rpm | no | 0.7556 | 0.7855 | 0.9349 | 0.2185 | 0.1573 | 0.1273 | 0.4598 |
| 12 | S0 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 390 K x 5000 s @ 600 rpm | no | 0.7444 | 0.7631 | 0.9609 | 0.2368 | 0.1595 | 0.1143 | 0.4577 |

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
  "end_step": 7,
  "lifecycle_index": 1,
  "metrics": {
    "byproduct_signal": 0.16281838715076447,
    "conversion": 0.9335241913795471,
    "cost": 0.7402999997138977,
    "degradation_warning": 0.1259336769580841,
    "safety_risk": 0.18164575099945068,
    "score": 0.4488096237182617,
    "selectivity": 0.8201581835746765,
    "virtual_spectrum_summary": 0.14622026681900024,
    "yield": 0.7654706239700317
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
      "duration_s": 4200,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 400
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
    "byproduct_signal": 0.20613372325897217,
    "conversion": 0.9660835266113281,
    "cost": 0.7477999925613403,
    "degradation_warning": 0.14080122113227844,
    "safety_risk": 0.14303058385849,
    "score": 0.453639954328537,
    "selectivity": 0.791328489780426,
    "virtual_spectrum_summary": 0.1767341047525406,
    "yield": 0.7458581328392029
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
      "duration_s": 5000,
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
  "end_step": 21,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.2214145064353943,
    "conversion": 0.9654608964920044,
    "cost": 0.7544666528701782,
    "degradation_warning": 0.1481904834508896,
    "safety_risk": 0.11429161578416824,
    "score": 0.4566790461540222,
    "selectivity": 0.7723033428192139,
    "virtual_spectrum_summary": 0.1884637027978897,
    "yield": 0.734837532043457
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
      "duration_s": 5000,
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
  "end_step": 28,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.34167441725730896,
    "conversion": 0.9827331304550171,
    "cost": 0.7574666738510132,
    "degradation_warning": 0.27388453483581543,
    "safety_risk": 0.13748665153980255,
    "score": 0.3760302662849426,
    "selectivity": 0.6609194874763489,
    "virtual_spectrum_summary": 0.31116896867752075,
    "yield": 0.6253568530082703
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
      "duration_s": 5000,
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
  "end_step": 35,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.34720364212989807,
    "conversion": 0.9797009229660034,
    "cost": 0.7622666954994202,
    "degradation_warning": 0.2902730107307434,
    "safety_risk": 0.15570469200611115,
    "score": 0.37104806303977966,
    "selectivity": 0.6428369283676147,
    "virtual_spectrum_summary": 0.32158488035202026,
    "yield": 0.646656334400177
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
      "duration_s": 5000,
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
  "end_step": 42,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.4664548933506012,
    "conversion": 0.9668210744857788,
    "cost": 0.7592666745185852,
    "degradation_warning": 0.31383174657821655,
    "safety_risk": 0.1676076203584671,
    "score": 0.29303663969039917,
    "selectivity": 0.5516300201416016,
    "virtual_spectrum_summary": 0.39777448773384094,
    "yield": 0.5244928002357483
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
      "duration_s": 5000,
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
  "end_step": 49,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.18781958520412445,
    "conversion": 0.8538059592247009,
    "cost": 0.4604666531085968,
    "degradation_warning": 0.06678997725248337,
    "safety_risk": 0.11338657885789871,
    "score": 0.45177698135375977,
    "selectivity": 0.7792811393737793,
    "virtual_spectrum_summary": 0.1333562582731247,
    "yield": 0.6716168522834778
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
      "duration_s": 5000,
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
  "end_step": 56,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.2587454617023468,
    "conversion": 0.9399181604385376,
    "cost": 0.6704666614532471,
    "degradation_warning": 0.14145995676517487,
    "safety_risk": 0.11391819268465042,
    "score": 0.4391462206840515,
    "selectivity": 0.7413570284843445,
    "virtual_spectrum_summary": 0.205966979265213,
    "yield": 0.6953125596046448
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
      "duration_s": 5000,
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
  "end_step": 63,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.27146250009536743,
    "conversion": 0.7851651310920715,
    "cost": 0.5444666743278503,
    "degradation_warning": 0.06074513494968414,
    "safety_risk": 0.11239862442016602,
    "score": 0.34901106357574463,
    "selectivity": 0.6594569087028503,
    "virtual_spectrum_summary": 0.17663967609405518,
    "yield": 0.5266409516334534
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
      "duration_s": 5500,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 385
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
    "byproduct_signal": 0.22820696234703064,
    "conversion": 0.9791596531867981,
    "cost": 0.7586333155632019,
    "degradation_warning": 0.15777680277824402,
    "safety_risk": 0.10371098667383194,
    "score": 0.4523639976978302,
    "selectivity": 0.7501609325408936,
    "virtual_spectrum_summary": 0.19651339948177338,
    "yield": 0.7236027121543884
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
      "duration_s": 4500,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 395
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
    "byproduct_signal": 0.2184724658727646,
    "conversion": 0.9349283576011658,
    "cost": 0.7502999901771545,
    "degradation_warning": 0.1573326736688614,
    "safety_risk": 0.1273394376039505,
    "score": 0.4597662687301636,
    "selectivity": 0.7855303287506104,
    "virtual_spectrum_summary": 0.19095955789089203,
    "yield": 0.755558967590332
  },
  "ordinal": 11
}
```

### Batch 12

Lifecycle index: `12`; end step: `84`.

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
      "duration_s": 5000,
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
  "end_step": 84,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.2368130087852478,
    "conversion": 0.9609412550926208,
    "cost": 0.7544666528701782,
    "degradation_warning": 0.15950478613376617,
    "safety_risk": 0.11429161578416824,
    "score": 0.45774346590042114,
    "selectivity": 0.763104259967804,
    "virtual_spectrum_summary": 0.20202431082725525,
    "yield": 0.7443779110908508
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

1. Scope and evidence base

This report describes only the bounded synthetic reaction world explored in the completed 12-batch campaign. The limiting reagent, target, impurities, and catalysts are anonymous benchmark entities. Although the selectable solvents have familiar names, the public material packet explicitly states that their reaction effects are categorical benchmark effects, not predictions derived from real solvent properties. I therefore do not assign a real chemical identity or named mechanism to this system.

Every completed batch used 0.003 mol reagent, 0.0075 L solvent, 0.000525 mol catalyst, one heating operation, and 600 rpm stirring. Consequently, the evidence identifies effects of catalyst category, solvent category, and coupled temperature-duration schedules near the supplied reference region. It does not identify reaction orders, concentration dependence, catalyst-loading dependence, mixing dependence, or behavior under a different operation sequence.

2. Proposed operating picture

The simplest model consistent with the observations is a catalytic network containing a desired pathway and at least one competing pathway:

R --kP(T,C,S)--> P
R --kB(T,C,S)--> B
P --kD(T,C,S)--> D
B --kBD(T,C,S)--> D or additional unobserved material

Here R is the public reactant proxy, P is the target-product proxy, B is the byproduct proxy, D represents degradation material, C is catalyst category, S is solvent category, and T is temperature. A minimal kinetic representation would be

dR/dt = -[kP(T,C,S) + kB(T,C,S)]R,
dP/dt = kP(T,C,S)R - kD(T,C,S)P,
dB/dt = kB(T,C,S)R - kBD(T,C,S)B.

An Arrhenius-like temperature dependence is plausible,

ki(T,C,S) = Ai(C,S) exp[-Ei(C,S)/(RT)],

but the campaign cannot estimate Ai or Ei separately. Temperature and duration were deliberately changed together, and only endpoint measurements were collected. The equations should therefore be treated as a qualitative process model rather than an identified rate law.

The principal implication is that conversion alone is insufficient. Several conditions produced conversion near 0.97-0.98 while having substantially different yield, selectivity, byproduct, and degradation signals. Material can leave the reactant channel without entering or remaining in the desired-product channel. The endpoint likely reflects both primary competition between P and B formation and secondary degradation during prolonged thermal exposure.

3. Thermal severity and safety

For Catalyst D in water, I tested a sequence of coupled temperature-duration schedules:

- Batch 1: 410 K for 3300 s; safety risk 0.18165; yield 0.76547; selectivity 0.82016; conversion 0.93352; byproduct 0.16282; degradation 0.12593; score 0.44881.
- Batch 2: 400 K for 4200 s; risk 0.14303; yield 0.74586; selectivity 0.79133; conversion 0.96608; byproduct 0.20613; degradation 0.14080; score 0.45364.
- Batch 3: 390 K for 5000 s; risk 0.11429; yield 0.73484; selectivity 0.77230; conversion 0.96546; byproduct 0.22141; degradation 0.14819; score 0.45668.
- Batch 10: 385 K for 5500 s; risk 0.10371; yield 0.72360; selectivity 0.75016; conversion 0.97916; byproduct 0.22821; degradation 0.15778; score 0.45236.
- Batch 11: 395 K for 4500 s; risk 0.12734; yield 0.75556; selectivity 0.78553; conversion 0.93493; byproduct 0.21847; degradation 0.15733; score 0.45977.
- Batch 12: 390 K for 5000 s; risk 0.11429; yield 0.74438; selectivity 0.76310; conversion 0.96094; byproduct 0.23681; degradation 0.15950; score 0.45774.

The observed safety risk decreased monotonically as the nominal temperature was reduced along this coupled schedule series: about 0.182 at 410 K, 0.143 at 400 K, 0.127 at 395 K, 0.114 at 390 K, and 0.104 at 385 K. All were below the declared 0.35 limit. This strongly supports a temperature-sensitive hazard or thermal-stress integral. A generic representation is

H = Hsetup + integral h[T(t),S,inventory(t)] dt,

with h increasing strongly with temperature. Because duration increased as temperature fell, the monotonic decline implies that temperature had a stronger hazard effect than the compensating increase in time over this tested region.

The productive chemistry showed a compromise rather than a monotonic optimum. The hottest schedule gave the largest final yield and selectivity but also the largest risk. At the coolest schedule, conversion remained high, yet yield and selectivity fell while byproduct and degradation signals rose. This is consistent with longer residence time allowing competing or secondary pathways to accumulate, although temperature and duration cannot be separated experimentally here. The best measured safe score occurred at the intermediate schedule of 395 K for 4500 s in Batch 11.

The initial supplied model suggested that the lower-temperature side of 420 K would preserve balanced safe performance more reliably. The data supported the safety direction but refined the performance interpretation: simply moving as low as possible was not optimal. The evidence favors an interior compromise around 390-395 K and 4500-5000 s under the tested recipe.

4. Solvent-category effects

Batches 3-6 held Catalyst D, 390 K, 5000 s, loading, volume, and stirring constant while changing solvent category:

- Batch 3, water: risk 0.11429; yield 0.73484; selectivity 0.77230; conversion 0.96546; byproduct 0.22141; degradation 0.14819; score 0.45668.
- Batch 4, ethanol: risk 0.13749; yield 0.62536; selectivity 0.66092; conversion 0.98273; byproduct 0.34167; degradation 0.27388; score 0.37603.
- Batch 5, acetonitrile: risk 0.15570; yield 0.64666; selectivity 0.64284; conversion 0.97970; byproduct 0.34720; degradation 0.29027; score 0.37105.
- Batch 6, toluene: risk 0.16761; yield 0.52449; selectivity 0.55163; conversion 0.96682; byproduct 0.46645; degradation 0.31383; score 0.29304.

Water was clearly superior in this benchmark world. The other solvents did not fail to consume reactant: all had conversion around 0.967-0.983. Instead, they redirected converted material toward byproduct and degradation channels. Toluene was the clearest example, combining conversion 0.96682 with only 0.52449 target yield, 0.55163 selectivity, and a 0.46645 byproduct signal.

This pattern supports a solvent dependence in pathway partitioning rather than merely in overall reaction speed. In the proposed equations, water increases kP relative to kB and/or suppresses kD. The solvent also affected public safety risk under an otherwise identical schedule, rising from 0.11429 in water to 0.13749, 0.15570, and 0.16761 for ethanol, acetonitrile, and toluene. Thus the runtime appears to include a solvent-category contribution to hazard as well as kinetics.

These statements are internal to the synthetic benchmark. It would be unjustified to infer that polarity, boiling point, proticity, or another real physical property caused the ranking.

5. Catalyst-category effects

Batches 3 and 7-9 compared all catalysts in water at 390 K for 5000 s:

- Batch 7, Catalyst A: risk 0.11339; yield 0.67162; selectivity 0.77928; conversion 0.85381; byproduct 0.18782; degradation 0.06679; score 0.45178.
- Batch 8, Catalyst B: risk 0.11392; yield 0.69531; selectivity 0.74136; conversion 0.93992; byproduct 0.25875; degradation 0.14146; score 0.43915.
- Batch 9, Catalyst C: risk 0.11240; yield 0.52664; selectivity 0.65946; conversion 0.78517; byproduct 0.27146; degradation 0.06075; score 0.34901.
- Batch 3, Catalyst D: risk 0.11429; yield 0.73484; selectivity 0.77230; conversion 0.96546; byproduct 0.22141; degradation 0.14819; score 0.45668.

Catalyst D gave the best observed balance and the highest conversion and yield in this comparison. Catalyst A was slower or less active, as indicated by conversion 0.85381, but was comparatively clean: its selectivity was slightly higher than Catalyst D's in these particular assay results, and its degradation signal was much lower. Catalyst B gave relatively high conversion but poorer partitioning to target. Catalyst C was weakest overall, with both low conversion and low selectivity.

Safety risks differed by less than 0.002 across these four water/catalyst batches. Within the observed resolution, catalyst identity strongly affected reaction-channel rates but barely affected the public risk metric under this schedule. This contrasts with the larger solvent and temperature effects on risk.

A reasonable latent interpretation is:

- Catalyst D: high kP and high total turnover, with some secondary degradation liability.
- Catalyst A: lower total rate but favorable primary selectivity and reduced degradation.
- Catalyst B: moderate-to-high activity with a larger competing-pathway fraction.
- Catalyst C: low desired activity and an unfavorable byproduct fraction.

Only one loading and one temperature-duration schedule were used for the catalyst screen, so catalyst ordering could change elsewhere through catalyst-temperature or catalyst-solvent interactions.

6. Repeatability and instrument interpretation

Batches 3 and 12 were nominal repeats of Catalyst D in water at 390 K for 5000 s. Their risks were identical at 0.11429, while their final assays differed modestly:

- Yield: 0.73484 versus 0.74438.
- Selectivity: 0.77230 versus 0.76310.
- Conversion: 0.96546 versus 0.96094.
- Byproduct: 0.22141 versus 0.23681.
- Degradation: 0.14819 versus 0.15950.
- Score: 0.45668 versus 0.45774.

This repeat indicates that small differences of roughly 0.005-0.015 in individual channels can arise from assay noise or bounded process variability, while the composite score is more stable here. Therefore, the approximately 0.0031 score advantage of Batch 11 over Batch 3 and the approximately 0.0020 advantage over Batch 12 are evidence for a local optimum but not proof of a sharply resolved optimum.

Intermediate HPLC and final assays also sometimes disagreed without an intervening heat period. For example, Batch 11 HPLC reported conversion 0.96289, yield 0.74330, selectivity 0.77302, and byproduct 0.20518, whereas its final assay reported 0.93493, 0.75556, 0.78553, and 0.21847. Batch 10 similarly had HPLC yield 0.70884 versus final yield 0.72360. These differences should not be interpreted as kinetic evolution after termination. They are more plausibly consequences of independent instrument noise, channel calibration, sampling, or bounded process-proxy uncertainty.

7. Interpretation of the score

The public score moved in the expected direction when target yield and selectivity improved and when byproduct, degradation, or safety burden decreased. However, the 12 endpoints are insufficient to recover the evaluator's exact composite equation. I therefore treat the score as an observed objective rather than claiming a specific analytical formula.

Batch 11 was selected because it had the highest actual completed-batch score, 0.45977, while its risk of 0.12734 remained far below 0.35. The selected operating procedure was 0.003 mol reagent, 0.0075 L water, 0.000525 mol Catalyst D, heating at 395 K for 4500 s with 600 rpm stirring, followed by termination and final assay.

8. Identifiable conclusions

The campaign provides direct evidence for the following conclusions within the tested region:

- Temperature is a major determinant of the safety metric.
- A moderate rather than maximal thermal schedule gives the best safe-score compromise.
- Water is the best of the four solvent categories for both selectivity and risk under the tested Catalyst D schedule.
- Solvent effects primarily alter pathway partitioning and degradation, because conversion remains high even when target yield collapses.
- Catalyst D provides the strongest overall performance in water; Catalyst A is a plausible cleaner but less active alternative.
- High conversion is not a sufficient optimization target.
- Replicate and cross-instrument variability are large enough that fine distinctions of a few thousandths in score should not be overinterpreted.

9. Unidentified factors and limits of extrapolation

The following remain unidentifiable from this campaign:

- Separate effects of temperature and duration, because they were co-varied in the thermal series.
- Reaction orders in reagent or catalyst and the effects of dilution, because amounts and volume were fixed.
- Whether degradation originates from product, byproduct, catalyst, or a parallel reactant pathway.
- Whether mixing or transport limits any condition, because stirring was always 600 rpm.
- Catalyst-solvent and catalyst-temperature interaction surfaces beyond the single categorical screens.
- Absolute mass balance into chemically distinct species; the public signals are normalized proxies.
- The exact score function and the exact functional form of safety accumulation.
- Real chemical identities or applicability to physical laboratory chemistry.

The recommendation should therefore be extrapolated only locally: approximately the tested amounts, water, Catalyst D, 600 rpm, and a single heating period around 390-395 K for roughly 4500-5000 s. Predictions far outside this region would be conjectural.

10. Reasonable competing explanations

Several alternatives remain compatible with the evidence:

First, the endpoint could arise from parallel primary pathways only, R to P and R to B/D, without meaningful secondary product degradation. The increasing degradation signal at longer, cooler schedules suggests residence-time-dependent secondary chemistry, but endpoint data cannot prove the precursor of D.

Second, solvent and catalyst categories could change analytical response factors or matrix effects rather than only true chemical partitioning. The public instruments are independently calibrated synthetic channels, making a real kinetic effect the more useful working interpretation, but category-dependent proxy response cannot be completely excluded from endpoint values alone.

Third, the apparent thermal optimum may be a severity optimum rather than a true temperature optimum. A different duration at 385 K or 410 K might reproduce or surpass Batch 11. Because the tested schedules trace only one diagonal through temperature-time space, no two-dimensional optimum is identified.

Fourth, Catalyst A might outperform Catalyst D after additional time. Its lower conversion, relatively favorable selectivity, and low degradation are consistent with a slower but cleaner route. No extended-time Catalyst A experiment was performed, so this remains a credible alternative operating strategy rather than an observed result.

Overall, the most economical explanation is a catalyzed desired reaction competing with byproduct formation and time-dependent degradation, with strong categorical modulation by solvent and catalyst and a temperature-dominated safety burden. The data support this model locally, while leaving the detailed kinetic topology and causal physical chemistry unresolved.

## Q — Blind predictions

### Overall rationale

Predictions use the campaign's observed catalyst, solvent, and coupled temperature-duration trends. The central model treats conversion as catalytic reactant loss partitioned between target and byproduct channels, with secondary target degradation and a strongly temperature-dependent accumulated safety burden. Catalyst B was observed only in water at 390 K for 5000 s, while acetonitrile was screened only with Catalyst D; therefore all queries require an uncertain catalyst-solvent interaction extrapolation. The smaller volume and lower stirring speed were not experimentally varied and are represented by wider intervals rather than strong deterministic corrections. Score estimates use the empirical campaign relationship in which yield and selectivity contribute positively and safety risk contributes negatively, with very hazardous extrapolations bounded near zero. Quench and heat-order effects are mechanistic forecasts rather than directly observed effects.

### Q01

This is an extrapolation from the Catalyst B water result and the observed acetonitrile penalty with Catalyst D. At 420 K, conversion should be high, but acetonitrile and the concentrated, slower-stirred recipe are expected to increase byproduct formation and safety burden.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3700 | 0.2500 | 0.5000 |
| conversion | 0.9600 | 0.8800 | 0.9950 |
| safety_risk | 0.3400 | 0.2700 | 0.4400 |
| score | 0.2500 | 0.1100 | 0.3800 |
| selectivity | 0.6100 | 0.4800 | 0.7300 |
| yield | 0.6000 | 0.4600 | 0.7200 |

### Q02

The quench is predicted to preserve slightly more target and suppress post-heating byproduct formation, but it cannot remove thermal risk already accumulated during the 420 K exposure. Its effect is uncertain because no campaign batch used a quench.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3400 | 0.2200 | 0.4800 |
| conversion | 0.9600 | 0.8800 | 0.9950 |
| safety_risk | 0.3500 | 0.2800 | 0.4500 |
| score | 0.2600 | 0.1200 | 0.4000 |
| selectivity | 0.6400 | 0.5000 | 0.7600 |
| yield | 0.6200 | 0.4800 | 0.7400 |

### Q03

Lower temperature sharply reduces predicted risk and degradation, but 3300 s at 390 K is probably insufficient for the near-complete conversion observed after 5000 s. Acetonitrile is still expected to partition more converted material into byproduct than water.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3000 | 0.1900 | 0.4300 |
| conversion | 0.8500 | 0.7100 | 0.9400 |
| safety_risk | 0.1400 | 0.1000 | 0.2000 |
| score | 0.3500 | 0.2400 | 0.4400 |
| selectivity | 0.6400 | 0.5100 | 0.7500 |
| yield | 0.5500 | 0.4200 | 0.6700 |

### Q04

The 450 K exposure lies far above the studied thermal region. The extrapolated hazard rate rises steeply with temperature; conversion should saturate while competing and degradation pathways substantially erode target yield and selectivity.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6100 | 0.4300 | 0.7800 |
| conversion | 0.9900 | 0.9500 | 1.0000 |
| safety_risk | 0.8600 | 0.6500 | 1.0000 |
| score | 0.0000 | 0.0000 | 0.1000 |
| selectivity | 0.3200 | 0.1600 | 0.5000 |
| yield | 0.2800 | 0.1200 | 0.4700 |

### Q05

The short 420 K treatment should limit both conversion and accumulated degradation. Relative to Q01, lower conversion reduces yield, but selectivity and safety should benefit from the shorter residence time.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2700 | 0.1600 | 0.4000 |
| conversion | 0.7700 | 0.6000 | 0.8900 |
| safety_risk | 0.2000 | 0.1500 | 0.2700 |
| score | 0.3000 | 0.2000 | 0.4000 |
| selectivity | 0.6500 | 0.5200 | 0.7600 |
| yield | 0.5000 | 0.3700 | 0.6200 |

### Q06

A 5100 s residence at 420 K should drive almost complete reactant consumption but also accumulate substantial byproduct, degradation, and risk. The predicted risk exceeds the declared safety limit, lowering the safe score.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4900 | 0.3400 | 0.6500 |
| conversion | 0.9900 | 0.9500 | 1.0000 |
| safety_risk | 0.4500 | 0.3500 | 0.5800 |
| score | 0.1300 | 0.0000 | 0.2700 |
| selectivity | 0.5200 | 0.3700 | 0.6600 |
| yield | 0.5000 | 0.3500 | 0.6400 |

### Q07

The final 1800 s at 450 K is expected to dominate conversion and hazard. Performing the lower-temperature segment first should leave less time for newly formed product to degrade after the high-temperature segment, so this order is predicted to outperform Q08 chemically, although both are unsafe.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5700 | 0.4000 | 0.7400 |
| conversion | 0.9900 | 0.9400 | 1.0000 |
| safety_risk | 0.8700 | 0.6600 | 1.0000 |
| score | 0.0000 | 0.0000 | 0.0900 |
| selectivity | 0.4500 | 0.2700 | 0.6200 |
| yield | 0.4200 | 0.2400 | 0.5900 |

### Q08

The high-temperature-first sequence should rapidly form both target and byproduct, after which the 390 K hold can continue slower secondary degradation. Integrated hazard is similar to Q07, but the reversed order is predicted to give poorer target retention.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6400 | 0.4600 | 0.8100 |
| conversion | 0.9900 | 0.9500 | 1.0000 |
| safety_risk | 0.8700 | 0.6600 | 1.0000 |
| score | 0.0000 | 0.0000 | 0.0700 |
| selectivity | 0.3800 | 0.2100 | 0.5600 |
| yield | 0.3400 | 0.1700 | 0.5200 |

### Q09

A short 440 K pulse should give high but not necessarily complete conversion. Its steep temperature-dependent hazard and increased side-pathway rate are expected to push risk beyond the safety limit despite the 1500 s duration.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3900 | 0.2500 | 0.5500 |
| conversion | 0.9000 | 0.7800 | 0.9700 |
| safety_risk | 0.4500 | 0.3400 | 0.5900 |
| score | 0.1500 | 0.0200 | 0.2900 |
| selectivity | 0.5700 | 0.4200 | 0.7000 |
| yield | 0.5100 | 0.3600 | 0.6500 |

### Q10

Quenching is predicted to modestly preserve target and reduce subsequent byproduct formation relative to Q09. Accumulated thermal risk remains approximately unchanged, and the untested quench effect is included in the broad intervals.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3500 | 0.2200 | 0.5000 |
| conversion | 0.9000 | 0.7800 | 0.9700 |
| safety_risk | 0.4500 | 0.3400 | 0.6000 |
| score | 0.1700 | 0.0300 | 0.3200 |
| selectivity | 0.6100 | 0.4600 | 0.7300 |
| yield | 0.5400 | 0.3900 | 0.6800 |

### Q11

At 370 K, risk and degradation should remain low even during the long hold, but Catalyst B is unlikely to reach the high conversion seen near 390-420 K. The expected result is cleaner but conversion-limited.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2000 | 0.1100 | 0.3200 |
| conversion | 0.6300 | 0.4500 | 0.7900 |
| safety_risk | 0.1200 | 0.0800 | 0.1700 |
| score | 0.3300 | 0.2200 | 0.4200 |
| selectivity | 0.6700 | 0.5400 | 0.7800 |
| yield | 0.4400 | 0.3100 | 0.5700 |

### Q12

This is an extreme extrapolation: 460 K for 6300 s should saturate conversion and the bounded risk scale while extensively destroying or diverting target product. The interval is widest for chemical partitioning because no campaign batch approached this thermal severity.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7200 | 0.4800 | 0.9000 |
| conversion | 0.9950 | 0.9700 | 1.0000 |
| safety_risk | 0.9900 | 0.9000 | 1.0000 |
| score | 0.0000 | 0.0000 | 0.0300 |
| selectivity | 0.1200 | 0.0200 | 0.3000 |
| yield | 0.0500 | 0.0000 | 0.1800 |

## K2 — Retrospective analysis

1. Assessment of the initial information

The initial packet contained one substantive scientific claim: relative to the stated 420 K, 3300 s reference region, the lower-temperature side was expected to retain safe, balanced performance more reliably than the higher-temperature side. It also explicitly described that model as incomplete and potentially shifted.

That directional claim received meaningful support. In the Catalyst D/water series, observed risk decreased from 0.18165 in Batch 1 at 410 K for 3300 s to 0.14303 in Batch 2 at 400 K for 4200 s, approximately 0.11429 in Batches 3 and 12 at 390 K for 5000 s, and 0.10371 in Batch 10 at 385 K for 5500 s. The best observed score was also obtained below 420 K: Batch 11 at 395 K for 4500 s scored 0.45977, compared with 0.44881 for Batch 1.

The evidence did not support a stronger claim that progressively lower temperature is always better. Batch 10 at 385 K scored only 0.45236 and had lower yield and selectivity than Batch 11. K1 accordingly revised the picture to an interior compromise around 390–395 K rather than a monotonic “colder is better” rule. This was a refinement of the initial claim, not a clear refutation of its stated lower-versus-higher directional comparison.

The initial packet also warned that a temperature-bound rollback should be treated as evidence against an attempted setting. No tested campaign operation produced such a rollback. That proposition therefore remained untested; there was merely no observed counterexample. It would be incorrect to describe the absence of a rollback as confirmation that the rule was false or irrelevant.

The supplied reference recipe—Catalyst D, water, 0.000525 mol catalyst, 0.003 mol reagent, 0.0075 L solvent, and 600 rpm—proved to be a strong local starting point. Water and Catalyst D gave the best measured scores in their respective screens. However, the packet did not claim that this recipe was globally optimal, and the campaign did not establish that stronger proposition.

The material packet’s categorical-boundary claims were respected rather than experimentally tested: catalysts were anonymous, and named solvents had benchmark categorical effects rather than guaranteed real-property correlations. K1 explicitly declined to infer a real catalyst, named synthesis, or solvent-property mechanism. Nothing in the observations contradicted that boundary, but the experiment could not independently validate it.

2. Experiments that formed or changed the interpretation

Batch 1 established the first empirical anchor. It showed that Catalyst D in water at 410 K for 3300 s gave strong conversion, yield, and selectivity while remaining below the 0.35 safety limit. Batches 2 and 3 then changed the interpretation from “use the supplied reference neighborhood” to “trade temperature against residence time.” They showed decreasing risk and slightly improving score as the schedule moved to lower temperature and longer duration, even though byproduct and degradation signals increased.

The solvent screen in Batches 4–6 caused the largest mechanistic update. Relative to Batch 3, ethanol, acetonitrile, and especially toluene retained very high conversion but sharply reduced target yield and selectivity while increasing byproduct and degradation signals. This was the main evidence behind K1’s judgment that solvent category altered pathway partitioning, not merely total reaction speed. Batch 6 was particularly diagnostic: conversion was 0.96682, but yield was only 0.52449 and byproduct signal was 0.46645.

The catalyst screen in Batches 7–9 changed the catalyst interpretation. Catalyst A appeared slower but cleaner; Catalyst B was active but less selective; Catalyst C was weak overall; and Catalyst D gave the best observed balance. The near-equality of risk across these four batches also led to the judgment that, at 390 K in water, catalyst identity affected reaction outcomes much more strongly than the public safety metric.

Batches 10 and 11 refined the local thermal optimum. Batch 10 showed that going down to 385 K did not continue improving score, while Batch 11 at 395 K for 4500 s produced the campaign maximum of 0.45977. Batch 12 was especially important because it repeated Batch 3 nominally. The close scores but noticeable differences in individual assay channels provided direct evidence of process or assay variability and should temper the apparent precision of the Batch 11 advantage.

The choice of Batch 1 depended strongly on the initial packet. The coupled lower-temperature/longer-duration sequence also inherited the packet’s emphasis on temperature, while the exact compensating durations were heuristic rather than derived from identified kinetics. The solvent and catalyst screens were driven by accumulated campaign evidence and the need to test categorical effects. The final local trials were optimization-driven responses to the observed score surface.

Several choices rested on unverified assumptions. I assumed that increasing duration would approximately compensate for decreasing temperature, but never identified an equivalence law. I also assumed that a one-factor categorical screen at 390 K could meaningfully rank catalysts and solvents more generally. Catalyst-by-solvent and catalyst-by-temperature interactions remained untested.

3. Most important competing mechanisms and explanations

The principal mechanistic competition is between a purely parallel network and one containing important secondary degradation.

In the parallel explanation, reactant is consumed through competing channels, R to P and R to B or D. Solvent and catalyst primarily change the branching fractions. In the sequential explanation used in K1, product or primary byproduct can degrade during continued heating, such as R to P followed by P to D. Both explanations account for high conversion with incomplete target yield.

The solvent screen distinguishes both of those models from a simple “poor conditions merely slow the desired reaction” model. Conversion remained near unity in Batches 4–6 even as target performance deteriorated, so incomplete reaction alone is not adequate. However, endpoint assays cannot determine whether the missing target arose from direct parallel formation of undesirable material or from secondary destruction of initially formed product.

The thermal series weakly favors a residence-time-dependent secondary process because cooler but longer schedules showed increased byproduct and degradation signals. Nevertheless, temperature and duration were co-varied, so this is not decisive. Different activation energies for parallel pathways could produce the same pattern without product degradation.

A second competition is between genuine kinetic effects and category-dependent measurement or matrix effects. The consistency of multiple public channels makes a kinetic interpretation useful, but the campaign did not independently calibrate response factors across solvent and catalyst matrices. Thus some apparent differences in partitioning could be amplified by proxy-response effects.

A third competition concerns Catalyst A versus Catalyst D. Catalyst A may represent a genuinely cleaner but slower route that could surpass Catalyst D at a longer optimized duration. Alternatively, it may simply approach a lower final yield ceiling. Only one Catalyst A schedule was tested, so these explanations cannot be distinguished.

A fourth unresolved issue is whether safety risk is governed mainly by a cumulative thermal integral, a peak-temperature term, or a more complicated state-dependent hazard. The observed monotonic thermal trend supports strong temperature dependence. It does not identify whether order matters in multistep heating or whether solvent changes a setup hazard, the heat-dependent hazard rate, or both.

Finally, concentration and mixing effects remain plausible competitors. Every research batch used 0.0075 L and 600 rpm. Therefore, K1 could not distinguish intrinsic kinetics from transport-limited behavior, nor establish how risk or selectivity changes with concentration.

4. The single additional experiment I would choose

I would run the established Catalyst D/water recipe at 395 K for 3300 s and 600 rpm, using the same reagent, solvent, and catalyst amounts as Batch 11. I would take the permitted intermediate HPLC measurement immediately after heating, then terminate and obtain the required final assay.

This condition fills a particularly informative missing cell. It shares temperature with Batch 11 but has a shorter duration, isolating a duration contrast. It also shares duration with Batch 1 but uses a lower temperature, providing a temperature contrast. This is substantially more identifiable than adding another point along the original diagonal in which lower temperatures always received longer times.

If 395 K for 3300 s retained yield and selectivity close to Batch 11 but had lower conversion, byproduct, degradation, and risk, I would infer that the final part of the 4500 s hold mainly completes reaction and adds some side chemistry. That would support a time-dependent trade-off and motivate duration optimization near 3300–4500 s.

If conversion and yield dropped strongly while selectivity stayed similar, the evidence would favor a mostly parallel network in which duration controls extent more than branching. If conversion remained high but yield and selectivity were substantially better than Batch 11, that would be stronger evidence that the additional 1200 s principally causes secondary degradation.

If the result resembled Batch 1 despite the 15 K temperature difference, duration or total severity would appear more important than temperature itself over this local region. Conversely, a large risk reduction or major change in branching relative to Batch 1 would strengthen the conclusion that temperature has an independent effect.

A large disagreement between the intermediate HPLC and final assay would not by itself demonstrate chemical change, because K1 already noted cross-instrument discrepancies without intervening heating. The final assay would remain the principal endpoint, while HPLC would provide qualified supporting evidence.

5. Trade-off between mechanistic identifiability and operating score

The campaign favored finding a good safe operating point over identifying a complete mechanism. That priority followed the stated goal and explains why much of the work remained near the supplied Catalyst D/water reference recipe.

Optimization sacrificed identifiability in the thermal series. Temperature was lowered while duration was increased, so the experiments traced one severity-like path rather than a factorial temperature-by-time design. This was efficient for searching for a balanced operating point but prevented separate estimation of temperature and residence-time effects. The recommendation benefited from this choice; the kinetic interpretation did not.

The fixed reagent amount, catalyst loading, solvent volume, and stirring speed were another optimization-oriented simplification. They preserved comparability and avoided spending batches on variables that might not improve score, but they left reaction orders, dilution effects, transport behavior, and loading dependence unidentified.

There were also deliberate sacrifices of expected score for information. Batches 4–6 tested three alternative solvents even after water looked promising, and Batch 6 produced a low score of 0.29304. Batches 7–9 likewise tested all alternative catalysts, including Catalyst C, which scored 0.34901. Those batches were scientifically valuable because they revealed that high conversion did not guarantee high target performance and helped establish the catalyst and solvent rankings.

The last three batches shifted back toward optimization. Batches 10 and 11 probed the local temperature-duration region, and Batch 12 repeated a promising condition. The repeat improved uncertainty awareness but used a batch that could instead have supplied a factorial contrast. Overall, the campaign struck a defensible goal-driven balance, but the resulting mechanism is qualitative and locally constrained.

6. Underused evidence and weaknesses in the blind predictions

The intermediate HPLC measurements were not exploited as fully as they could have been. K1 mentioned selected HPLC/final discrepancies, but I did not construct a systematic instrument-bias model across all batches or inspect the public raw artifacts in detail. Peak shapes, assignments, and channel-specific residuals might have helped distinguish stable calibration offsets from process variability, although they still would not reveal hidden species identities.

The operation-level risk increments observed during setup were also underused. Batch 1 showed appreciable risk before heating, but the later analysis concentrated on final risk. A decomposition into reagent, solvent, concentration-independent setup risk, and thermal risk might have improved the blind safety forecasts.

Cost was observed but not incorporated deeply into the mechanistic analysis or the empirical score model. Likewise, only one nominal replicate pair—Batches 3 and 12—was available. It was enough to warn against overprecision but not enough to estimate condition-dependent variance.

The least reliable blind predictions are Q12, Q04, Q07, and Q08. They involve 450–460 K, well outside the campaign’s 385–410 K observations, and Q12 combines 460 K with 6300 s. The predicted near-saturation risks and severe loss of target are mechanistically plausible extrapolations, but their numerical values are weakly supported. Q07 and Q08 additionally rely on a speculative heat-order effect that was never tested.

Q02 and Q10 are also unreliable because no campaign batch used a quench. The predicted small improvements in yield and selectivity were guesses based on a presumed arrest of post-heating chemistry. Termination may already stop relevant evolution in this world, or quenching may have its own matrix effects. Their intervals were probably too narrow for an entirely unobserved operation effect.

All 12 blind queries used Catalyst B in acetonitrile, 0.005 L solvent, and 400 rpm, whereas the campaign separately observed Catalyst B only in water and acetonitrile only with Catalyst D, always at 0.0075 L and 600 rpm. My blind predictions effectively combined main effects and allowed broad uncertainty, but they could not account reliably for catalyst-solvent, concentration, or mixing interactions. Even Q03 and Q11, which are thermally less extreme, remain cross-material extrapolations.

The safety intervals for Q01 and Q02 may also be too narrow because their point estimates lie near the 0.35 limit and were obtained by extrapolating an approximate exponential temperature trend. A peak-temperature rule or rollback threshold could produce discontinuous behavior that those intervals do not capture. Score intervals for the high-risk cases may be too narrow because the exact treatment of constraint violations was never identified; predicting scores near zero assumed effective lower bounding or a strong safety penalty.

These weaknesses are consistent with K1’s explicit statement that extrapolation should be local to water, Catalyst D, 600 rpm, and approximately 390–395 K for 4500–5000 s. The blind queries were almost all outside that scope. Where the prediction intervals appeared numerically confident despite this, the predictions were less conservative than K1’s stated uncertainty warranted.

7. Limitations of the sealed recommendation

Batch 11 is the sample-internal winner, not a proven optimum. Its score of 0.45977 exceeded Batch 12 by only about 0.0020 and Batch 3 by about 0.0031. Those differences are small relative to the observed changes in individual assay channels between the nominally repeated Batches 3 and 12. Thus the evidence supports selecting Batch 11 among the completed batches, but it does not establish that 395 K and 4500 s is uniquely or statistically superior.

Repeatability should be tested by running several independently prepared replicates of the exact Batch 11 procedure, preferably in randomized order among neighboring conditions. The resulting distribution of final score, risk, yield, selectivity, and byproduct would show whether its apparent advantage is reproducible rather than an assay fluctuation.

Local robustness should be tested with a small factorial neighborhood rather than another diagonal sequence: for example, temperatures around 390, 395, and 400 K crossed with durations around 3900, 4500, and 5100 s. Small perturbations in stirring speed, solvent volume, and catalyst loading should follow. A robust operating point should retain acceptable score and remain comfortably below the 0.35 risk limit throughout plausible execution error, not merely at one nominal setting.

The recommendation’s safety margin is encouraging—Batch 11 risk was 0.12734—but robustness against temperature overshoot was not tested. Given the strong observed temperature dependence of risk, controller error or a higher peak temperature could matter disproportionately.

Cross-material generalization requires separate validation. The campaign showed that changing solvent or catalyst could substantially alter pathway partitioning, so Batch 11 cannot be transferred directly to another catalyst-solvent combination. Catalyst A in particular deserves a duration-optimized comparison because it appeared cleaner but slower. Cross-world generalization is even less justified: the catalysts are latent categorical formulations, and the initial packet warned that the supplied model could be shifted. A new world could change category rankings or kinetic parameters while preserving the same public labels.

Accordingly, the sealed recommendation should be described precisely as follows: it was the highest-scoring completed batch in this 12-batch campaign and satisfied the observed safety constraint. It was not proven globally optimal, uniquely locally optimal, universally repeatable, or transferable to different materials, concentrations, mixing conditions, or latent worlds.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 100.1 | none | 0 |
| Q | yes | 0 | 123.4 | none | 0 |
| K2 | yes | 0 | 91.8 | none | 0 |

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean 80% width | Mean interval score |
|---|---:|---:|---:|---:|
| byproduct_signal | 0.1633 | 0.4500 | 0.2958 | 0.7166 |
| conversion | 0.0642 | 0.7000 | 0.1425 | 0.3263 |
| safety_risk | 0.2554 | 0.3333 | 0.2100 | 1.7093 |
| score | 0.2065 | 0.1667 | 0.1892 | 1.2115 |
| selectivity | 0.1986 | 0.3167 | 0.2825 | 1.0499 |
| yield | 0.2487 | 0.2333 | 0.2817 | 1.4006 |

## Predictions versus released reference truth

### Q01

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3700 | 0.2500 | 0.5000 | 0.2826 | 0.2852, 0.2894, 0.2712, 0.2806, 0.2868 |
| conversion | 0.9600 | 0.8800 | 0.9950 | 0.9936 | 0.9944, 0.9886, 0.9985, 1.0000, 0.9865 |
| safety_risk | 0.3400 | 0.2700 | 0.4400 | 0.2975 | 0.2975, 0.2975, 0.2975, 0.2975, 0.2975 |
| score | 0.2500 | 0.1100 | 0.3800 | 0.3741 | 0.3745, 0.3704, 0.3762, 0.3731, 0.3761 |
| selectivity | 0.6100 | 0.4800 | 0.7300 | 0.7204 | 0.7250, 0.7175, 0.7148, 0.7117, 0.7328 |
| yield | 0.6000 | 0.4600 | 0.7200 | 0.7164 | 0.7143, 0.7102, 0.7240, 0.7179, 0.7156 |
### Q02

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3400 | 0.2200 | 0.4800 | 0.2861 | 0.2908, 0.2824, 0.2881, 0.2929, 0.2764 |
| conversion | 0.9600 | 0.8800 | 0.9950 | 0.9921 | 0.9993, 1.0000, 0.9838, 0.9912, 0.9863 |
| safety_risk | 0.3500 | 0.2800 | 0.4500 | 0.1512 | 0.1512, 0.1512, 0.1512, 0.1512, 0.1512 |
| score | 0.2600 | 0.1200 | 0.4000 | 0.4400 | 0.4421, 0.4407, 0.4410, 0.4418, 0.4345 |
| selectivity | 0.6400 | 0.5000 | 0.7600 | 0.7247 | 0.7349, 0.7269, 0.7271, 0.7216, 0.7132 |
| yield | 0.6200 | 0.4800 | 0.7400 | 0.7228 | 0.7198, 0.7212, 0.7257, 0.7294, 0.7176 |
### Q03

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3000 | 0.1900 | 0.4300 | 0.2305 | 0.2338, 0.2259, 0.2177, 0.2369, 0.2383 |
| conversion | 0.8500 | 0.7100 | 0.9400 | 0.9608 | 0.9596, 0.9490, 0.9674, 0.9626, 0.9652 |
| safety_risk | 0.1400 | 0.1000 | 0.2000 | 0.1854 | 0.1854, 0.1854, 0.1854, 0.1854, 0.1854 |
| score | 0.3500 | 0.2400 | 0.4400 | 0.4438 | 0.4466, 0.4474, 0.4404, 0.4439, 0.4408 |
| selectivity | 0.6400 | 0.5100 | 0.7500 | 0.7671 | 0.7763, 0.7752, 0.7648, 0.7603, 0.7591 |
| yield | 0.5500 | 0.4200 | 0.6700 | 0.7437 | 0.7453, 0.7506, 0.7349, 0.7477, 0.7399 |
### Q04

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.6100 | 0.4300 | 0.7800 | 0.3349 | 0.3411, 0.3290, 0.3394, 0.3241, 0.3407 |
| conversion | 0.9900 | 0.9500 | 1.0000 | 0.9971 | 0.9964, 0.9936, 0.9975, 0.9981, 1.0000 |
| safety_risk | 0.8600 | 0.6500 | 1.0000 | 0.4031 | 0.4031, 0.4031, 0.4031, 0.4031, 0.4031 |
| score | 0.0000 | 0.0000 | 0.1000 | 0.2995 | 0.3030, 0.2973, 0.3051, 0.2950, 0.2974 |
| selectivity | 0.3200 | 0.1600 | 0.5000 | 0.6731 | 0.6859, 0.6698, 0.6734, 0.6614, 0.6750 |
| yield | 0.2800 | 0.1200 | 0.4700 | 0.6776 | 0.6782, 0.6748, 0.6911, 0.6732, 0.6704 |
### Q05

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2700 | 0.1600 | 0.4000 | 0.1390 | 0.1313, 0.1497, 0.1384, 0.1357, 0.1399 |
| conversion | 0.7700 | 0.6000 | 0.8900 | 0.8939 | 0.9038, 0.8951, 0.8931, 0.8821, 0.8954 |
| safety_risk | 0.2000 | 0.1500 | 0.2700 | 0.2972 | 0.2972, 0.2972, 0.2972, 0.2972, 0.2972 |
| score | 0.3000 | 0.2000 | 0.4000 | 0.4181 | 0.4209, 0.4187, 0.4150, 0.4146, 0.4214 |
| selectivity | 0.6500 | 0.5200 | 0.7600 | 0.8564 | 0.8553, 0.8572, 0.8540, 0.8567, 0.8586 |
| yield | 0.5000 | 0.3700 | 0.6200 | 0.7624 | 0.7676, 0.7631, 0.7562, 0.7563, 0.7688 |
### Q06

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4900 | 0.3400 | 0.6500 | 0.4142 | 0.4168, 0.4031, 0.4113, 0.4196, 0.4205 |
| conversion | 0.9900 | 0.9500 | 1.0000 | 0.9945 | 0.9842, 0.9940, 0.9980, 1.0000, 0.9961 |
| safety_risk | 0.4500 | 0.3500 | 0.5800 | 0.2972 | 0.2972, 0.2972, 0.2972, 0.2972, 0.2972 |
| score | 0.1300 | 0.0000 | 0.2700 | 0.2977 | 0.2966, 0.2960, 0.3021, 0.2986, 0.2951 |
| selectivity | 0.5200 | 0.3700 | 0.6600 | 0.6004 | 0.6005, 0.5997, 0.6043, 0.6057, 0.5920 |
| yield | 0.5000 | 0.3500 | 0.6400 | 0.6037 | 0.6035, 0.6000, 0.6114, 0.6014, 0.6020 |
### Q07

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5700 | 0.4000 | 0.7400 | 0.3184 | 0.3152, 0.3252, 0.3252, 0.3153, 0.3110 |
| conversion | 0.9900 | 0.9400 | 1.0000 | 0.9980 | 1.0000, 1.0000, 1.0000, 1.0000, 0.9902 |
| safety_risk | 0.8700 | 0.6600 | 1.0000 | 0.4275 | 0.4275, 0.4275, 0.4275, 0.4275, 0.4275 |
| score | 0.0000 | 0.0000 | 0.0900 | 0.3011 | 0.3054, 0.3035, 0.2994, 0.2993, 0.2978 |
| selectivity | 0.4500 | 0.2700 | 0.6200 | 0.6925 | 0.7058, 0.6881, 0.6972, 0.6796, 0.6920 |
| yield | 0.4200 | 0.2400 | 0.5900 | 0.6972 | 0.6993, 0.7056, 0.6895, 0.7005, 0.6912 |
### Q08

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.6400 | 0.4600 | 0.8100 | 0.3216 | 0.3273, 0.3191, 0.3086, 0.3218, 0.3312 |
| conversion | 0.9900 | 0.9500 | 1.0000 | 0.9968 | 0.9991, 1.0000, 0.9973, 0.9961, 0.9914 |
| safety_risk | 0.8700 | 0.6600 | 1.0000 | 0.1975 | 0.1975, 0.1975, 0.1975, 0.1975, 0.1975 |
| score | 0.0000 | 0.0000 | 0.0700 | 0.4075 | 0.4073, 0.4070, 0.4041, 0.4125, 0.4069 |
| selectivity | 0.3800 | 0.2100 | 0.5600 | 0.7016 | 0.7006, 0.7052, 0.6910, 0.7046, 0.7067 |
| yield | 0.3400 | 0.1700 | 0.5200 | 0.6992 | 0.6986, 0.6948, 0.6970, 0.7099, 0.6957 |
### Q09

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3900 | 0.2500 | 0.5500 | 0.1517 | 0.1510, 0.1588, 0.1357, 0.1541, 0.1589 |
| conversion | 0.9000 | 0.7800 | 0.9700 | 0.9456 | 0.9443, 0.9462, 0.9392, 0.9438, 0.9543 |
| safety_risk | 0.4500 | 0.3400 | 0.5900 | 0.3768 | 0.3768, 0.3768, 0.3768, 0.3768, 0.3768 |
| score | 0.1500 | 0.0200 | 0.2900 | 0.3984 | 0.3958, 0.4013, 0.3970, 0.3990, 0.3989 |
| selectivity | 0.5700 | 0.4200 | 0.7000 | 0.8476 | 0.8351, 0.8618, 0.8575, 0.8339, 0.8498 |
| yield | 0.5100 | 0.3600 | 0.6500 | 0.7952 | 0.7969, 0.7935, 0.7871, 0.8057, 0.7929 |
### Q10

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3500 | 0.2200 | 0.5000 | 0.1532 | 0.1524, 0.1604, 0.1493, 0.1485, 0.1556 |
| conversion | 0.9000 | 0.7800 | 0.9700 | 0.9459 | 0.9443, 0.9377, 0.9581, 0.9487, 0.9408 |
| safety_risk | 0.4500 | 0.3400 | 0.6000 | 0.1712 | 0.1712, 0.1712, 0.1712, 0.1712, 0.1712 |
| score | 0.1700 | 0.0300 | 0.3200 | 0.4888 | 0.4881, 0.4857, 0.4916, 0.4910, 0.4875 |
| selectivity | 0.6100 | 0.4600 | 0.7300 | 0.8509 | 0.8547, 0.8603, 0.8394, 0.8540, 0.8458 |
| yield | 0.5400 | 0.3900 | 0.6800 | 0.7961 | 0.7925, 0.7846, 0.8071, 0.7989, 0.7972 |
### Q11

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2000 | 0.1100 | 0.3200 | 0.3207 | 0.3220, 0.3285, 0.3186, 0.3278, 0.3067 |
| conversion | 0.6300 | 0.4500 | 0.7900 | 0.9808 | 0.9709, 0.9777, 0.9940, 0.9742, 0.9873 |
| safety_risk | 0.1200 | 0.0800 | 0.1700 | 0.1548 | 0.1548, 0.1548, 0.1548, 0.1548, 0.1548 |
| score | 0.3300 | 0.2200 | 0.4200 | 0.4068 | 0.4034, 0.4056, 0.4113, 0.4075, 0.4063 |
| selectivity | 0.6700 | 0.5400 | 0.7800 | 0.6769 | 0.6720, 0.6683, 0.6786, 0.6851, 0.6803 |
| yield | 0.4400 | 0.3100 | 0.5700 | 0.6732 | 0.6701, 0.6762, 0.6801, 0.6713, 0.6682 |
### Q12

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.7200 | 0.4800 | 0.9000 | 0.5786 | 0.5786, 0.5797, 0.5783, 0.5826, 0.5738 |
| conversion | 0.9950 | 0.9700 | 1.0000 | 0.9966 | 0.9974, 0.9885, 0.9990, 0.9992, 0.9990 |
| safety_risk | 0.9900 | 0.9000 | 1.0000 | 0.4202 | 0.4202, 0.4202, 0.4202, 0.4202, 0.4202 |
| score | 0.0000 | 0.0000 | 0.0300 | 0.1418 | 0.1464, 0.1386, 0.1392, 0.1429, 0.1417 |
| selectivity | 0.1200 | 0.0200 | 0.3000 | 0.4511 | 0.4571, 0.4436, 0.4565, 0.4418, 0.4566 |
| yield | 0.0500 | 0.0000 | 0.1800 | 0.4475 | 0.4551, 0.4464, 0.4372, 0.4555, 0.4432 |

## Recommendation retest

- Selected source batch: `11`
- Retest exact replay verified: `True`
- Retest failure: `none`

| Metric | Selected source batch | Independent retest | Retest minus source |
|---|---:|---:|---:|
| byproduct_signal | 0.2185 | 0.2227 | 0.0043 |
| conversion | 0.9349 | 0.9392 | 0.0042 |
| cost | 0.7503 | 0.7503 | 0.0000 |
| degradation_warning | 0.1573 | 0.1413 | -0.0161 |
| safety_risk | 0.1273 | 0.1273 | 0.0000 |
| score | 0.4598 | 0.4541 | -0.0057 |
| selectivity | 0.7855 | 0.7690 | -0.0165 |
| virtual_spectrum_summary | 0.1910 | 0.1861 | -0.0049 |
| yield | 0.7556 | 0.7507 | -0.0049 |

## Scope note

This is the final sanitized report produced after all 60 source sessions and K1/Q/K2 chains were sealed. It includes released reference truth, blind-prediction evaluation, and the independent recommendation retest. Provider-private event streams, credentials, thread identifiers, and token accounting remain excluded.
