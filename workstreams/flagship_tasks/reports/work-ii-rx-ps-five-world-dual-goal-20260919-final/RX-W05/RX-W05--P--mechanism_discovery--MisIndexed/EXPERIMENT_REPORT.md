# RX-W05--P--mechanism_discovery--MisIndexed

## Run summary

- World: `RX-W05`
- Locus: `P`
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

- Selected batch: `12`
- Rationale: Batch 12 gave the strongest safe final performance and most informative operating balance: catalyst D in water, a 420 K boundary target for 2400 s, then prompt quench. It retained high yield while suppressing byproduct, degradation, and residual safety risk relative to longer or hotter runs.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S0 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 420 K x 3300 s @ 600 rpm | no | 0.7709 | 0.8098 | 0.9604 | 0.2014 | 0.1428 | 0.2264 | 0.4310 |
| 2 | S0 (0.0075 L) | 0.003000 mol | C0 (0.000525 mol) | 420 K x 3300 s @ 600 rpm | no | 0.6884 | 0.8236 | 0.8599 | 0.1768 | 0.0361 | 0.2255 | 0.4212 |
| 3 | S0 (0.0075 L) | 0.003000 mol | C1 (0.000525 mol) | 420 K x 3300 s @ 600 rpm | no | 0.7330 | 0.7789 | 0.9352 | 0.2176 | 0.1074 | 0.2260 | 0.4141 |
| 4 | S0 (0.0075 L) | 0.003000 mol | C2 (0.000525 mol) | 420 K x 3300 s @ 600 rpm | no | 0.5450 | 0.7205 | 0.7945 | 0.2356 | 0.0407 | 0.2245 | 0.3235 |
| 5 | S1 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 420 K x 3300 s @ 600 rpm | no | 0.6731 | 0.6901 | 0.9684 | 0.3009 | 0.2342 | 0.2496 | 0.3519 |
| 6 | S2 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 420 K x 3300 s @ 600 rpm | no | 0.7014 | 0.7159 | 0.9762 | 0.3116 | 0.2421 | 0.2678 | 0.3618 |
| 7 | S3 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 420 K x 3300 s @ 600 rpm | no | 0.5746 | 0.5937 | 0.9460 | 0.4075 | 0.2774 | 0.2798 | 0.2725 |
| 8 | S0 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 390 K x 3300 s @ 600 rpm | no | 0.7317 | 0.8381 | 0.8816 | 0.1455 | 0.0872 | 0.1139 | 0.4651 |
| 9 | S0 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 450 K x 3300 s @ 600 rpm | no | 0.7670 | 0.7809 | 0.9817 | 0.2205 | 0.1792 | 0.3322 | 0.3767 |
| 10 | S0 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 420 K x 1200 s @ 600 rpm | no | 0.6286 | 0.9152 | 0.6952 | 0.0744 | 0.0209 | 0.2247 | 0.3763 |
| 11 | S0 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 420 K x 6000 s @ 600 rpm | no | 0.6780 | 0.6835 | 1.0000 | 0.3382 | 0.2674 | 0.2263 | 0.3639 |
| 12 | S0 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 420 K x 2400 s @ 600 rpm | yes | 0.7665 | 0.8404 | 0.9132 | 0.1442 | 0.0815 | 0.0798 | 0.4953 |

## Complete experimental actions and observations

### Batch 1

Lifecycle index: `1`; end step: `7`.

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.0075
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
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
    "byproduct_signal": 0.2014375627040863,
    "conversion": 0.9604207873344421,
    "cost": 0.7402999997138977,
    "degradation_warning": 0.14282676577568054,
    "safety_risk": 0.2263662964105606,
    "score": 0.43097925186157227,
    "selectivity": 0.8098200559616089,
    "virtual_spectrum_summary": 0.17506271600723267,
    "yield": 0.7709424495697021
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
      "volume_L": 0.0075
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
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
    "byproduct_signal": 0.17681024968624115,
    "conversion": 0.8598582148551941,
    "cost": 0.4462999999523163,
    "degradation_warning": 0.03606726974248886,
    "safety_risk": 0.22547794878482819,
    "score": 0.421156644821167,
    "selectivity": 0.8235987424850464,
    "virtual_spectrum_summary": 0.11347591131925583,
    "yield": 0.68841552734375
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
      "volume_L": 0.0075
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
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
    "byproduct_signal": 0.2176104038953781,
    "conversion": 0.935178816318512,
    "cost": 0.6563000082969666,
    "degradation_warning": 0.10739928483963013,
    "safety_risk": 0.2260156273841858,
    "score": 0.41411659121513367,
    "selectivity": 0.7789120078086853,
    "virtual_spectrum_summary": 0.16801540553569794,
    "yield": 0.7330193519592285
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
      "volume_L": 0.0075
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
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
    "byproduct_signal": 0.23560570180416107,
    "conversion": 0.7944658994674683,
    "cost": 0.5303000211715698,
    "degradation_warning": 0.04072382673621178,
    "safety_risk": 0.22449980676174164,
    "score": 0.32349294424057007,
    "selectivity": 0.7204771637916565,
    "virtual_spectrum_summary": 0.14790885150432587,
    "yield": 0.5449549555778503
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
      "volume_L": 0.0075
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
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
  "end_step": 35,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.300907701253891,
    "conversion": 0.9683600664138794,
    "cost": 0.7433000206947327,
    "degradation_warning": 0.23424729704856873,
    "safety_risk": 0.24958759546279907,
    "score": 0.35192668437957764,
    "selectivity": 0.6900531649589539,
    "virtual_spectrum_summary": 0.2709105312824249,
    "yield": 0.6730545163154602
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
      "volume_L": 0.0075
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
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
  "end_step": 42,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.3115506172180176,
    "conversion": 0.9762222766876221,
    "cost": 0.7480999827384949,
    "degradation_warning": 0.2421017736196518,
    "safety_risk": 0.2677887976169586,
    "score": 0.361835241317749,
    "selectivity": 0.7158970236778259,
    "virtual_spectrum_summary": 0.28029865026474,
    "yield": 0.7013843059539795
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
      "volume_L": 0.0075
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
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
  "end_step": 49,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.40748482942581177,
    "conversion": 0.9460412859916687,
    "cost": 0.7451000213623047,
    "degradation_warning": 0.27738121151924133,
    "safety_risk": 0.27975013852119446,
    "score": 0.2724559009075165,
    "selectivity": 0.5936605334281921,
    "virtual_spectrum_summary": 0.3489381968975067,
    "yield": 0.5745855569839478
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
      "volume_L": 0.0075
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
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
    "byproduct_signal": 0.14547061920166016,
    "conversion": 0.8816473484039307,
    "cost": 0.7402999997138977,
    "degradation_warning": 0.08724123239517212,
    "safety_risk": 0.11386619508266449,
    "score": 0.46508482098579407,
    "selectivity": 0.8380991220474243,
    "virtual_spectrum_summary": 0.11926739662885666,
    "yield": 0.7316627502441406
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
      "volume_L": 0.0075
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
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
      "target_temperature_K": 450
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
    "byproduct_signal": 0.2204769402742386,
    "conversion": 0.9817206859588623,
    "cost": 0.7402999997138977,
    "degradation_warning": 0.17919905483722687,
    "safety_risk": 0.3321538269519806,
    "score": 0.3766978979110718,
    "selectivity": 0.780911386013031,
    "virtual_spectrum_summary": 0.2019018977880478,
    "yield": 0.7669930458068848
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
      "solvent": 0,
      "volume_L": 0.0075
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1200,
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
  "end_step": 70,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.07437805831432343,
    "conversion": 0.6951863765716553,
    "cost": 0.7228000164031982,
    "degradation_warning": 0.02093816176056862,
    "safety_risk": 0.2247406542301178,
    "score": 0.37633660435676575,
    "selectivity": 0.9151976108551025,
    "virtual_spectrum_summary": 0.05033010244369507,
    "yield": 0.6285796165466309
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
      "volume_L": 0.0075
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 6000,
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
  "end_step": 77,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.33817702531814575,
    "conversion": 1.0,
    "cost": 0.7627999782562256,
    "degradation_warning": 0.26737403869628906,
    "safety_risk": 0.22633026540279388,
    "score": 0.36393240094184875,
    "selectivity": 0.6835107803344727,
    "virtual_spectrum_summary": 0.30631569027900696,
    "yield": 0.6779583096504211
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
      "volume_L": 0.0075
    },
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 420
    },
    {
      "operation": "quench"
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
    "byproduct_signal": 0.14419782161712646,
    "conversion": 0.9131654500961304,
    "cost": 0.7677665948867798,
    "degradation_warning": 0.08150726556777954,
    "safety_risk": 0.0797891765832901,
    "score": 0.4953259825706482,
    "selectivity": 0.8404325842857361,
    "virtual_spectrum_summary": 0.11598706990480423,
    "yield": 0.7664576768875122
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

1. Scope and evidential basis

This report concerns only the bounded synthetic reaction world explored in the completed 12-batch campaign. Catalyst identities are anonymous benchmark formulations, and the named solvents have categorical benchmark effects; I do not infer a real chemical synthesis or real catalyst identity.

All batches used 0.003 mol reagent, 0.000525 mol catalyst, 0.0075 L solvent, and 600 rpm stirring. Consequently, the campaign identifies effects of catalyst category, solvent category, temperature, elapsed reaction time, and quenching only near that recipe. It does not identify concentration orders, catalyst-dose dependence, or mixing dependence.

The values below are final-assay observations unless explicitly described otherwise:

- Batch 1: catalyst D, water, 420 K target, 3300 s. Conversion 0.9604, yield 0.7709, selectivity 0.8098, byproduct 0.2014, degradation 0.1428, safety risk 0.2264.
- Batch 2: catalyst A, water, 420 K, 3300 s. Conversion 0.8599, yield 0.6884, selectivity 0.8236, byproduct 0.1768, degradation 0.0361, risk 0.2255.
- Batch 3: catalyst B, water, 420 K, 3300 s. Conversion 0.9352, yield 0.7330, selectivity 0.7789, byproduct 0.2176, degradation 0.1074, risk 0.2260.
- Batch 4: catalyst C, water, 420 K, 3300 s. Conversion 0.7945, yield 0.5450, selectivity 0.7205, byproduct 0.2356, degradation 0.0407, risk 0.2245.
- Batch 5: catalyst D, ethanol, 420 K, 3300 s. Conversion 0.9684, yield 0.6731, selectivity 0.6901, byproduct 0.3009, degradation 0.2342, risk 0.2496.
- Batch 6: catalyst D, acetonitrile, 420 K, 3300 s. Conversion 0.9762, yield 0.7014, selectivity 0.7159, byproduct 0.3116, degradation 0.2421, risk 0.2678.
- Batch 7: catalyst D, toluene, 420 K, 3300 s. Conversion 0.9460, yield 0.5746, selectivity 0.5937, byproduct 0.4075, degradation 0.2774, risk 0.2798.
- Batch 8: catalyst D, water, 390 K target, 3300 s. Conversion 0.8816, yield 0.7317, selectivity 0.8381, byproduct 0.1455, degradation 0.0872, risk 0.1139.
- Batch 9: catalyst D, water, 450 K target, 3300 s. Conversion 0.9817, yield 0.7670, selectivity 0.7809, byproduct 0.2205, degradation 0.1792, risk 0.3322.
- Batch 10: catalyst D, water, 420 K, 1200 s. Conversion 0.6952, yield 0.6286, selectivity 0.9152, byproduct 0.0744, degradation 0.0209, risk 0.2247.
- Batch 11: catalyst D, water, 420 K, 6000 s. Conversion 1.0000, yield 0.6780, selectivity 0.6835, byproduct 0.3382, degradation 0.2674, risk 0.2263.
- Batch 12: catalyst D, water, 420 K, 2400 s, followed promptly by quenching. Conversion 0.9132, yield 0.7665, selectivity 0.8404, byproduct 0.1442, degradation 0.0815, post-quench risk 0.0798.

2. Proposed reaction network

The smallest network consistent with the observations is a desired reaction competing with undesired formation, followed by time- and temperature-dependent deterioration of desired product:

R --kP--> P
R --kB--> B
P --kD--> D and/or additional B-like material

Here R is the limiting reactant, P is the target-product pool, B is a competing byproduct pool, and D is the material responsible for the degradation-warning channel. The public signals are normalized analytical responses rather than demonstrated mole fractions, so B and D should be regarded as observable pools, not necessarily single chemical species.

A useful local kinetic representation is:

  dR/dt = -(kP + kB) R
  dP/dt = kP R - kD P
  dB/dt = kB R + alpha kD P
  dD/dt = (1-alpha) kD P

The rate constants can be represented locally as:

  kj(T,catalyst,solvent,t) = Aj exp[-Ej/(Rgas T)] Fj,catalyst Gj,solvent a(t)

where a(t) is an optional catalyst-activity factor. A simple deactivation law would be da/dt = -kdeact a, although this campaign does not require catalyst deactivation to explain the data. Product degradation or a late-time selectivity shift is more directly supported.

A useful observation relation is:

  target yield approximately equals conversion × selectivity.

This relation works well across the campaign. For example, Batch 1 gives 0.9604 × 0.8098 = about 0.778, close to observed yield 0.7709. Batch 10 gives about 0.636 versus 0.6286, Batch 11 about 0.684 versus 0.6780, and Batch 12 about 0.768 versus 0.7665. Small discrepancies are compatible with independent channel noise and calibration.

3. Evidence for competing and sequential processes

The time series at the common 420 K target is the clearest mechanistic evidence. In Batch 10 at 1200 s, conversion was only 0.695, but selectivity was 0.915, byproduct was 0.074, and degradation was 0.021. Extending to 3300 s in Batch 1 raised conversion to 0.960 and yield to 0.771, but selectivity fell to 0.810 while byproduct and degradation rose to 0.201 and 0.143. At 6000 s in Batch 11, conversion saturated at 1.000, yet yield fell to 0.678, selectivity fell to 0.684, byproduct rose to 0.338, and degradation rose to 0.267.

Thus, elapsed time first increases target formation by consuming R, but later exposure primarily increases undesired material and destroys or transforms P. A purely parallel model R→P and R→B with fixed selectivity would predict relatively constant selectivity as conversion rises. The large decline from 0.915 at 1200 s to 0.684 at 6000 s therefore favors either sequential loss of P or a time-dependent change in catalytic selectivity. The explicit rise in the degradation-warning channel makes sequential deterioration the more direct explanation.

Yield consequently has an interior optimum: insufficient time leaves reactant unconverted, whereas excessive time causes secondary conversion. Within the tested recipe, the useful region is roughly 2400–3300 s at the 420 K setpoint, with prompt termination or quenching.

4. Catalyst effects

Batches 1–4 isolate catalyst identity under otherwise common conditions. Catalyst D produced the highest conversion and yield. Catalyst A preserved selectivity and showed very little degradation, but its lower conversion limited yield. Catalyst B gave fairly high conversion but poorer selectivity and more byproduct. Catalyst C was weak in both conversion and selectivity.

A qualitative ordering at 420 K and 3300 s is:

- Desired conversion activity: D > B > A > C.
- Final yield: D > B > A > C.
- Resistance to the measured degradation channel: A approximately C > B > D.
- Selectivity: A slightly above D, then B, then C.

Catalyst D is therefore not simply universally superior. It raises kP enough to give the best useful yield, but it also appears to increase kD or otherwise permits more late-stage deterioration. Catalyst A may have a lower desired-reaction rate but a lower degradation rate. Catalyst C’s poor selectivity despite low degradation suggests that its main defect is a larger competing-path fraction kB/(kP+kB), not merely deactivation.

Catalyst deactivation remains possible but unproven. No catalyst-loading series, catalyst-reuse experiment, or late catalyst addition was performed. The time-dependent yield decline can be explained without deactivation by P→D, while deactivation alone would more naturally cause a plateau than a decline in target yield.

5. Solvent effects and coupling

Batches 1 and 5–7 compare solvents with catalyst D. Water was decisively best for balanced formation: yield 0.771 and selectivity 0.810, compared with yields of 0.673 in ethanol, 0.701 in acetonitrile, and 0.575 in toluene. The nonaqueous solvents still gave high conversion, so their lower yields primarily reflect poorer partitioning between desired and undesired pathways rather than failure to consume reactant.

Observed byproduct and degradation increased strongly away from water. Toluene was especially unfavorable, with byproduct 0.4075, degradation 0.2774, and selectivity only 0.5937. Ethanol and acetonitrile were intermediate and similar, although acetonitrile gave slightly better yield and selectivity than ethanol while showing slightly more byproduct and degradation.

The solvent also coupled to safety. Under the common 420 K/3300 s treatment, risk increased from 0.226 in water to 0.250 in ethanol, 0.268 in acetonitrile, and 0.280 in toluene. Setup risk before heating was also visibly solvent-dependent. Thus solvent changes both chemistry and the safety state; it is not merely a dilution label.

Because only catalyst D was tested across all four solvents, I cannot identify catalyst-by-solvent interactions separately from solvent main effects. The conclusion that water is best is secure for catalyst D near this recipe, but extrapolating the same solvent ordering to catalysts A–C is an inference.

6. Temperature and actual thermal history

The commanded setpoint was not equal to the public temperature-state change. Starting from approximately ambient state, the reported temperature changes were about +83.4 K for a 390 K target, +107.36 K for a 420 K target, and +129.93 K for a 450 K target. These correspond approximately to final public temperatures of 381, 405, and 428 K. I therefore interpret setpoint as a controller input and the reported state change as the better indication of attained endpoint temperature.

A minimal thermal model would be:

  dT/dt = (Tset - T)/tau + Qreaction/Cp - Qloss/Cp,

or, for an empirical endpoint mapping, Tactual = Tambient + h(Tset, duration, formulation). The campaign does not provide continuous temperature traces, so tau, reaction heat, and heat-loss terms cannot be separated. Interestingly, 1200, 3300, and 6000 s runs at the 420 K target had very similar final temperature changes, near +107.36 K. This indicates that the endpoint temperature was reached relatively early or that the public temperature field represents a controlled terminal state; it does not establish that their complete warm-up trajectories were identical.

At 3300 s, raising the target from 390 K to 420 K increased conversion from 0.882 to 0.960 and yield from 0.732 to 0.771, but decreased selectivity from 0.838 to 0.810 and increased degradation from 0.087 to 0.143. Raising it further to 450 K increased conversion only to 0.982, did not improve yield (0.767), and further worsened selectivity and degradation to 0.781 and 0.179.

Thus kP is temperature-activated, but the undesired rates kB and/or kD are also activated and become dominant after conversion is already high. The yield-temperature curve is locally saturating and possibly peaked around the middle setting, while degradation and safety risk rise monotonically over the tested range.

The supplied incomplete prior suggested that the higher-temperature side might retain balanced safe performance more reliably than the lower-temperature side. The experiments caused me to revise that belief. Batch 9’s higher target produced nearly no yield benefit over Batch 1, but substantially higher risk (0.332 versus 0.226), lower selectivity, and more degradation. Batch 8’s lower target sacrificed some yield but was much safer (risk 0.114) and cleaner. Higher temperature is useful for rate, not reliably better for balance.

7. Quench and termination

Batch 12 provides direct evidence that quenching changes the physical state. After 2400 s at the 420 K target, quenching reduced the public temperature by 45 K and reduced safety risk from 0.2261 immediately before quench to 0.0798 afterward. The reported quench-state transition took about 5.14 s in that outcome. The subsequent final assay gave yield 0.7665, selectivity 0.8404, byproduct 0.1442, and degradation 0.0815.

This is consistent with quenching sharply reducing all temperature-dependent rate constants and effectively preserving an intermediate-time product distribution. Batch 12 retained nearly the Batch 1 yield while showing much less degradation and byproduct, and it avoided the severe late-time deterioration observed in Batch 11.

However, the chemical benefit of quenching is not completely isolated experimentally. Batch 12 differs from Batch 1 in both reaction time (2400 versus 3300 s) and quench treatment, and no unquenched 2400 s batch was run. Therefore, the reduced impurity burden is jointly attributable to earlier stopping and quenching; only the immediate reduction in temperature and safety risk is directly assignable to the quench operation.

The post-quench HPLC in Batch 12 reported conversion 0.8962, yield 0.7727, selectivity 0.8754, and byproduct 0.1291. The final assay later reported 0.9132, 0.7665, 0.8404, and 0.1442. These are directionally consistent but not identical, as expected from independent synthetic channel calibration and noise. I do not interpret the differences as definitive evidence that substantial reaction continued after quenching.

8. Safety model

Safety risk behaved mainly as a function of formulation and attained temperature, and much less as a function of reaction duration. Water runs at the 420 K target had risks around 0.2245–0.2264 across catalysts and across 1200–6000 s. At constant catalyst D and 3300 s, risk rose from 0.1139 at the 390 K target to 0.2264 at 420 K and 0.3322 at 450 K. This suggests a nonlinear monotonic temperature term combined with a solvent-dependent baseline:

  risk before quench approximately equals rsolvent + rT(Tactual) + smaller formulation terms.

A locally quadratic or exponential rT would be plausible, but three temperature settings are insufficient to identify its form. Quench introduces a large negative state change by cooling the vessel. Risk should not be treated as an accumulated toxicological quantity here; it is an observed public process-state metric that can decrease when the vessel is quenched.

9. Compact predictive account

For conditions close to the tested recipe, my working simulator would be:

1. Convert the requested temperature setpoint into an actual temperature history using a first-order thermal response rather than assuming T = Tset.
2. Select catalyst- and solvent-specific multipliers for kP, kB, and kD.
3. Integrate the competing/sequential kinetic equations.
4. Compute conversion = 1 - R/R0.
5. Compute selectivity from target formation relative to converted material.
6. Predict yield approximately as conversion × selectivity.
7. Map B and D pools monotonically to the byproduct and degradation channels.
8. On quench, rapidly lower T, making subsequent kP, kB, and kD small.
9. Predict safety risk from solvent baseline and actual temperature, with a large immediate reduction after quench.

In pseudocode:

  T = thermal_history(Tset, duration, solvent)
  for each short interval dt:
      kp = Arrhenius(T, catalyst, solvent, desired_path)
      kb = Arrhenius(T, catalyst, solvent, competing_path)
      kd = Arrhenius(T, catalyst, solvent, degradation_path)
      R -= (kp + kb)*R*dt
      P += (kp*R - kd*P)*dt
      B += (kb*R + alpha*kd*P)*dt
      D += (1-alpha)*kd*P*dt
  if quenched:
      T -= observed_quench_drop
      rates become small

This is a structural model, not a fitted parameter set. Twelve categorical and one-dimensional experiments are insufficient for reliable numerical Arrhenius parameters.

10. Applicability and unresolved alternatives

The account is strongest for 0.003 mol reagent, 0.000525 mol catalyst, 0.0075 L solvent, 600 rpm, water/catalyst D, actual endpoint temperatures of roughly 381–428 K, and times of 1200–6000 s. Predictions outside that neighborhood are extrapolations.

Important unidentified factors are:

- Reaction orders and concentration effects: reagent, solvent volume, and catalyst loading were fixed.
- Mixing or transport: every heated batch used 600 rpm.
- Full thermal trajectory: only public endpoint changes were observed, not continuous temperature telemetry.
- Catalyst deactivation: plausible but not separated from product degradation.
- Catalyst–solvent interactions: only catalyst D received a solvent screen.
- Exact composition of byproduct and degradation pools: the channels could combine multiple species.
- Quench chemistry versus simple cooling: no matched unquenched 2400 s control was available.
- Replicate variability: no exact batch replicate was run, although intermediate HPLC and final assays provided cross-channel consistency.
- Measurement latency effects: the data do not identify whether any small post-sampling evolution occurred.

A reasonable competing explanation is a purely parallel network whose selectivity changes over time because catalyst state or medium composition changes, without direct P→D conversion. Another is catalyst deactivation accompanied by increasing activity of a background undesired reaction. These models can mimic the falling selectivity. Nevertheless, the simultaneous late-time decline in yield and rise in the degradation-warning channel makes direct or indirect destruction of accumulated target product the most economical explanation.

Overall, this world is best described as a thermally activated, catalyst- and solvent-dependent competition with a secondary overprocessing regime. Catalyst D in water rapidly forms target, but prolonged or hotter exposure shifts the balance toward byproduct and degradation. Actual thermal state, not nominal setpoint alone, controls both kinetics and safety. Timely quenching preserves the high-yield intermediate-time state and sharply reduces residual process risk.

## Q — Blind predictions

### Overall rationale

The predictions use the campaign-supported structure R→P competing with R→B and followed by time- and temperature-dependent P deterioration. Catalyst-B effects were anchored to Batch 3, while the acetonitrile shift was estimated from the water/acetonitrile comparison in Batches 1 and 6. Temperature and time responses were transferred from Batches 8–11, and the quench risk reduction was anchored to Batch 12. All queries change solvent volume and stirring speed from the researched recipe, and catalyst-by-solvent interactions were not directly measured; prediction intervals therefore include substantial structural uncertainty beyond final-assay noise. Scores were estimated jointly from expected yield, selectivity, impurity burden, and safety risk under the public reaction scoring behavior.

### Q01

This combines the observed catalyst-B baseline with the adverse acetonitrile solvent effect. Lower solvent volume and 400 rpm were not tested, so the interval includes concentration and mixing uncertainty.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3300 | 0.2400 | 0.4300 |
| conversion | 0.9500 | 0.8800 | 0.9900 |
| safety_risk | 0.2800 | 0.2300 | 0.3400 |
| score | 0.3300 | 0.2500 | 0.4100 |
| selectivity | 0.6900 | 0.5900 | 0.7700 |
| yield | 0.6500 | 0.5500 | 0.7300 |

### Q02

The quench is predicted to preserve essentially the Q01 composition because it occurs after the reaction interval, while sharply lowering the final thermal safety state. The score consequently rises despite similar chemical metrics.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3300 | 0.2400 | 0.4300 |
| conversion | 0.9500 | 0.8800 | 0.9900 |
| safety_risk | 0.1300 | 0.0800 | 0.2000 |
| score | 0.3700 | 0.2800 | 0.4600 |
| selectivity | 0.6900 | 0.5900 | 0.7700 |
| yield | 0.6500 | 0.5500 | 0.7300 |

### Q03

The lower setpoint should reduce both desired conversion and secondary deterioration. Relative to Q01, the expected result is cleaner and safer but somewhat under-converted.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2700 | 0.1800 | 0.3700 |
| conversion | 0.8700 | 0.7600 | 0.9400 |
| safety_risk | 0.1700 | 0.1200 | 0.2300 |
| score | 0.3600 | 0.2700 | 0.4500 |
| selectivity | 0.7200 | 0.6200 | 0.8000 |
| yield | 0.6200 | 0.5100 | 0.7100 |

### Q04

The high setpoint should nearly complete conversion but accelerate competing formation and degradation. Acetonitrile and the reduced solvent volume make safety extrapolation especially uncertain, with substantial probability of exceeding the nominal 0.35 safety limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3500 | 0.2500 | 0.4700 |
| conversion | 0.9700 | 0.9100 | 1.0000 |
| safety_risk | 0.3800 | 0.3100 | 0.4600 |
| score | 0.2700 | 0.1800 | 0.3600 |
| selectivity | 0.6500 | 0.5300 | 0.7500 |
| yield | 0.6300 | 0.5100 | 0.7200 |

### Q05

The shorter exposure should retain high intrinsic selectivity and low byproduct formation, but incomplete conversion limits yield. This follows the strong time dependence observed between 1200 and 3300 seconds.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1900 | 0.1100 | 0.2900 |
| conversion | 0.7500 | 0.6200 | 0.8500 |
| safety_risk | 0.2800 | 0.2200 | 0.3400 |
| score | 0.3400 | 0.2500 | 0.4300 |
| selectivity | 0.7800 | 0.6800 | 0.8600 |
| yield | 0.5800 | 0.4700 | 0.6800 |

### Q06

Long exposure should exhaust reactant but drive substantial overprocessing. The prediction therefore has nearly complete conversion with lower target yield, lower selectivity, and more byproduct than Q01.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4200 | 0.3100 | 0.5400 |
| conversion | 0.9900 | 0.9500 | 1.0000 |
| safety_risk | 0.2800 | 0.2200 | 0.3400 |
| score | 0.2800 | 0.1900 | 0.3700 |
| selectivity | 0.6000 | 0.4800 | 0.7000 |
| yield | 0.5900 | 0.4700 | 0.6800 |

### Q07

The initial low-temperature stage should form product relatively cleanly, but the final high-temperature stage acts on an accumulated product pool and is expected to promote late degradation. Final safety risk is dominated by the hot second stage.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3800 | 0.2600 | 0.5100 |
| conversion | 0.9700 | 0.8900 | 1.0000 |
| safety_risk | 0.3900 | 0.3100 | 0.4800 |
| score | 0.2600 | 0.1600 | 0.3600 |
| selectivity | 0.6300 | 0.4900 | 0.7400 |
| yield | 0.6100 | 0.4800 | 0.7100 |

### Q08

High temperature first should produce rapid conversion, while the later low-temperature stage reduces the terminal thermal state and slows subsequent deterioration. Irreversible impurity formed during the first stage remains, so the result is not equivalent to an entirely low-temperature run.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3000 | 0.2000 | 0.4200 |
| conversion | 0.9600 | 0.8800 | 0.9900 |
| safety_risk | 0.1800 | 0.1200 | 0.2700 |
| score | 0.3900 | 0.2900 | 0.4800 |
| selectivity | 0.7000 | 0.5800 | 0.7900 |
| yield | 0.6700 | 0.5500 | 0.7600 |

### Q09

The combination of a short duration and high setpoint should give intermediate-to-high conversion before the full long-time degradation regime develops. The hot terminal state creates appreciable safety risk.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2300 | 0.1400 | 0.3400 |
| conversion | 0.8400 | 0.7200 | 0.9200 |
| safety_risk | 0.3500 | 0.2800 | 0.4300 |
| score | 0.3200 | 0.2300 | 0.4100 |
| selectivity | 0.7300 | 0.6200 | 0.8200 |
| yield | 0.6100 | 0.5000 | 0.7100 |

### Q10

The composition is predicted to match Q09 within assay and model uncertainty, while quenching lowers the final thermal risk and improves the safe score.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2300 | 0.1400 | 0.3400 |
| conversion | 0.8400 | 0.7200 | 0.9200 |
| safety_risk | 0.1800 | 0.1100 | 0.2600 |
| score | 0.3700 | 0.2700 | 0.4600 |
| selectivity | 0.7300 | 0.6200 | 0.8200 |
| yield | 0.6100 | 0.5000 | 0.7100 |

### Q11

Long duration compensates partly for the low temperature, giving substantial but not necessarily complete conversion. Low temperature suppresses the secondary pathway and safety risk, although the 5700-second exposure still permits some degradation.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2700 | 0.1700 | 0.3900 |
| conversion | 0.9000 | 0.7900 | 0.9600 |
| safety_risk | 0.1300 | 0.0800 | 0.2000 |
| score | 0.4100 | 0.3100 | 0.5000 |
| selectivity | 0.7400 | 0.6200 | 0.8300 |
| yield | 0.6700 | 0.5500 | 0.7600 |

### Q12

This is the strongest extrapolation: very high temperature and long duration should ensure complete conversion but also severe overprocessing, byproduct formation, and safety burden. Catalyst B may degrade less aggressively than catalyst D, preventing an even lower central yield, but uncertainty is wide.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5000 | 0.3600 | 0.6500 |
| conversion | 1.0000 | 0.9700 | 1.0000 |
| safety_risk | 0.4500 | 0.3600 | 0.5600 |
| score | 0.1800 | 0.0900 | 0.2900 |
| selectivity | 0.5000 | 0.3500 | 0.6300 |
| yield | 0.5000 | 0.3500 | 0.6300 |

## K2 — Retrospective analysis

1. Initial claims: supported, contradicted, or untested

The initial material supplied one substantive local claim: near the reference recipe—catalyst D, water, 0.000525 mol catalyst, 0.003 mol reagent, 0.0075 L solvent, 600 rpm, approximately 420 K for 3300 s—the higher-temperature side was expected to retain safe, balanced performance more reliably than the lower-temperature side. It also warned that the model was incomplete and that experimental evidence was authoritative. No task-specific material-property dossier or named chemical mechanism was supplied.

The reference region itself was reasonably supported. Batch 1 at the reference conditions gave conversion 0.9604 and yield 0.7709, making it one of the strongest unquenched batches. Catalyst D and water also proved favorable in their respective screens. Thus, the reference recipe was a useful starting point, although that does not validate the supplied directional temperature claim.

The higher-temperature directional claim was contradicted rather than merely left unsupported. At 3300 s, Batch 8 at a 390 K target had risk 0.1139, score 0.4651, selectivity 0.8381, and degradation 0.0872. Batch 1 at 420 K had risk 0.2264, score 0.4310, selectivity 0.8098, and degradation 0.1428. Batch 9 at 450 K reached conversion 0.9817 but had risk 0.3322, score 0.3767, selectivity 0.7809, and degradation 0.1792. Higher temperature improved conversion but did not reliably improve balanced performance or safety. K1 explicitly revised the prior on this point, stating that “higher temperature is useful for rate, not reliably better for balance.” This was a genuine correction prompted by evidence, not an absence of contrary evidence.

The instruction to interpret a temperature-bound rollback as evidence was never tested because none of my submitted heating operations was rolled back. Batch 9 approached the safety limit but was accepted. Therefore, I have no evidence about the detailed rollback rule or the resulting physical state. This is a case of no test, not support.

The initial information did not provide substantive claims about catalyst ordering, solvent ordering, reaction order, catalyst deactivation, or product degradation. Those parts of K1 were developed from the campaign rather than inherited from the prior.

2. Experiments that formed or changed the account

Batch 1 established the empirical anchor. It showed that the nominal reference recipe gave high conversion and yield but already had measurable byproduct and degradation. It also revealed that the reported temperature-state change, about +107.36 K, was not identical to simply assigning the vessel the 420 K setpoint. The later K1 distinction between commanded setpoint and actual public thermal state arose from these heat outcomes, although no continuous thermal model was identified.

Batches 2–4 formed the catalyst ranking. Relative to catalyst D in Batch 1, catalyst A in Batch 2 gave lower conversion and yield but much less degradation; catalyst B in Batch 3 was intermediate in conversion but poorer in selectivity; catalyst C in Batch 4 was weak in both conversion and selectivity. These results changed the simple notion that catalyst choice was only an activity multiplier. They suggested separate effects on desired conversion, competing conversion, and degradation.

Batches 5–7 formed the solvent judgment. With catalyst D fixed, ethanol, acetonitrile, and especially toluene retained substantial conversion but lost selectivity and increased both byproduct and degradation relative to water. That observation was central to K1’s conclusion that solvent acts on pathway partitioning and safety, not merely dilution.

Batches 8 and 9 changed the temperature belief inherited from the initial model. They demonstrated a conversion benefit but a safety and selectivity penalty on moving upward in temperature. Batch 9 was particularly diagnostic because its yield, 0.7670, was essentially no better than Batch 1’s 0.7709 despite its higher conversion and risk.

Batches 10 and 11 were the strongest evidence for a time-dependent secondary process. At 1200 s, Batch 10 had conversion 0.6952, selectivity 0.9152, byproduct 0.0744, and degradation 0.0209. At 6000 s, Batch 11 had complete measured conversion but yield only 0.6780, selectivity 0.6835, byproduct 0.3382, and degradation 0.2674. K1’s R→P, R→B, and P→D account was primarily formed from this contrast. The explicit differential equations in K1 were a retrospective compact representation, not a parameterized law established during the experiment sequence.

Batch 12 formed the practical quench judgment. After 2400 s at the 420 K target, quenching reduced the public temperature by 45 K and risk from 0.2261 to 0.0798. Its final yield was 0.7665 with less byproduct and degradation than Batch 1. This supported prompt stopping and cooling, but it did not isolate quenching from the shorter reaction time.

Several choices depended mainly on the initial information: Batch 1 copied the supplied reference recipe, and the initial temperature comparison was centered on its 420 K reference. The catalyst and solvent screens followed the stated research goal rather than a pre-existing mechanistic result. Later use of catalyst D and water was data-driven after Batches 1–7. The choices of 1200, 2400, and 6000 s, and the expectation that 450 K would remain executable, contained unvalidated judgment. Holding reagent amount, catalyst amount, volume, and stirring fixed was also a design assumption rather than a demonstrated statement that those variables were unimportant.

3. Main competing mechanisms and what is distinguishable

K1 proposed the minimal network R→P, R→B, followed by P→D or P→additional byproduct. The strongest support for a sequential loss process is that increasing time from Batch 10 through Batch 1 to Batch 11 raised conversion while eventually lowering yield and sharply increasing degradation. A fixed-selectivity parallel network alone cannot readily explain that pattern.

The most important competing explanation is a time-dependent branching network caused by catalyst-state or medium-state changes. For example, catalyst deactivation could suppress the desired path while an uncatalyzed undesired path persists, or the catalyst could transform into a less selective state. Such a model can produce falling selectivity without direct destruction of P. The campaign distinguishes a fixed parallel network from some time-dependent secondary process, but it does not distinguish direct P degradation from catalyst-state-dependent pathway switching.

A second competition concerns catalyst D. It may directly accelerate P degradation, or it may simply form P earlier, thereby exposing a larger P pool to a catalyst-independent degradation process for longer. The single endpoint at each catalyst cannot separate these explanations. Catalyst-specific time courses would be needed.

A third competition concerns solvent. Water may alter intrinsic pathway rate constants, catalyst state, thermal behavior, or signal response. High conversion but low selectivity in the nonaqueous solvents supports a chemical pathway effect, yet only catalyst D was screened across solvents. Catalyst–solvent interaction remains confounded with the estimated solvent main effect.

A fourth competition concerns quenching. Batch 12 directly proves cooling and risk reduction, but its cleaner final composition could result from stopping at 2400 s, from the quench itself, or from both. Existing experiments cannot assign the compositional improvement uniquely to quenching.

The approximate relation “yield ≈ conversion × selectivity,” cited in K1, is well supported as an observation-level consistency relation. It does not identify the microscopic network because both parallel and sequential mechanisms can satisfy it.

4. One additional complete experiment

I would run a matched, unquenched control for Batch 12: 0.0075 L water, 0.003 mol reagent, 0.000525 mol catalyst D, 600 rpm, a 420 K target for 2400 s, no quench, followed by termination and final assay. If the complete-experiment allowance also included one nonfinal instrument use, I would take HPLC immediately after heating and before termination, while still retaining the required final assay.

This experiment would change only the quench decision relative to Batch 12. It is more informative now than another nominal optimum search because it directly tests the causal basis of the sealed recommendation.

Possible interpretations would be:

- If the unquenched batch had approximately the same conversion, yield, selectivity, byproduct, and degradation as Batch 12 but substantially higher risk, I would conclude that the quench primarily changes thermal safety and preserves an already established composition. K1’s chemical-preservation language would then have been too strong.
- If the unquenched batch had appreciably more byproduct or degradation and lower yield, I would infer meaningful post-heating evolution before or during termination/final handling, strengthening the claim that quenching chemically preserves P.
- If it had lower conversion but similar selectivity, an unexpected quench-associated conversion or measurement effect would need consideration.
- If it reproduced neither Batch 12 nor the surrounding time trend, batch variability or an unmodeled state variable would become more important, weakening confidence in the apparent 2400–3300 s optimum.

A replicate of Batch 12 would be valuable for reproducibility, but the matched no-quench control offers more immediate mechanistic discrimination from a single experiment.

5. Tradeoff between identifiability and operating score

The research goal emphasized explanatory and predictive understanding rather than pure score optimization. I therefore spent several experiments on deliberately nonoptimal conditions. Batches 2–4 tested catalysts that ultimately scored below catalyst D. Batches 5–7 tested solvents that were progressively worse, with Batch 7 scoring only 0.2725. Batch 9 approached the safety limit, and Batch 11 deliberately overprocessed the reaction to expose the late-time regime. Those decisions sacrificed immediate score to identify catalyst, solvent, temperature, and time effects.

Conversely, after the categorical screens, I concentrated all temperature, duration, and quench work on catalyst D in water. That was efficient for locating a good operation and led to Batch 12, but it sacrificed mechanistic identifiability. In particular, it left catalyst-specific time dependence, catalyst–solvent interaction, and whether catalyst D uniquely promotes degradation unresolved. This was an optimization-driven narrowing of the design.

The design was mostly one-factor-at-a-time rather than factorial. That made comparisons easy to interpret locally, but it provided poor coverage of interactions and no independent error estimate. A more identification-oriented design would have included selected catalyst×solvent and catalyst×time combinations plus replicates. A more score-oriented design would have skipped much of the catalyst and solvent screen after early evidence favored catalyst D and water, using those batches instead for a dense time-temperature-quench search.

Batch 12 was both an exploitation step and a mechanistic probe, but its two simultaneous changes relative to Batch 1—shorter time and quenching—made it less identifiable than a matched pair. Thus, the final operation improved score while sacrificing causal separation.

6. Underused evidence and weaknesses in the blind predictions

The characterization artifacts and full raw synthetic spectra were not inspected beyond the public peak summaries and processed estimates. Those artifacts might have helped assess peak overlap, missingness, calibration flags, or whether the degradation and byproduct assignments changed consistently. I also used HPLC in every intermediate measurement and did not use GC or UV–visible measurements. HPLC was well aligned with conversion and yield, but an orthogonal channel could have tested whether the inferred degradation/byproduct trend was instrument-specific.

The paired intermediate HPLC and final-assay observations were not formally modeled. Batch 12, for example, had post-quench HPLC conversion 0.8962, selectivity 0.8754, and byproduct 0.1291, followed by final-assay values of 0.9132, 0.8404, and 0.1442. K1 correctly avoided treating those differences as proof of continued reaction, but a calibration-aware analysis could have quantified systematic channel offsets rather than relying on qualitative agreement.

The thermal state changes were also underused. Endpoint temperature changes were recorded, but no attempt could identify the transient temperature history. K1’s first-order thermal equation was therefore only a plausible process representation. Costs, setup-risk increments, and solvent-specific baseline risk were observed but not fitted systematically.

All blind queries were extrapolations because they combined catalyst B with acetonitrile, 0.005 L solvent, and 400 rpm; that exact combination was never tested. K1 explicitly limited its strongest applicability to 0.0075 L, 600 rpm, and especially catalyst D in water. Consequently, the Q predictions depended on transferring a catalyst effect from water and a solvent effect from catalyst D while assuming manageable interaction. That is directly outside the strongest K1 scope.

The least reliable predictions were:

- Q12, because 460 K and 6300 s exceeded both the tested temperature maximum and nearly the tested time maximum in combination. Its severe-overprocessing point estimate was plausible, but the chemical intervals were probably too narrow for a two-axis extrapolation.
- Q07 and Q08, because no multi-stage temperature-order experiment was conducted. The claimed order effect—high temperature late being worse for accumulated P—came from the proposed sequential model, not direct evidence. Their selectivity, yield, byproduct, score, and safety intervals likely understated model-form uncertainty.
- Q04, Q09, and Q12 for safety risk, because they approached or exceeded the nominal safety boundary under an untested solvent volume. The possibility of a temperature-bound rollback was not included explicitly as a mixture outcome.
- Q02 and Q10, because the quench risk reduction was transferred from one water/catalyst-D batch to catalyst B in concentrated acetonitrile. Their composition intervals also assumed that quenching after the scheduled heat caused little chemical change.
- Q11, because 370 K was below the tested minimum of 390 K and was paired with a long duration. Compensation between temperature and time was not identified quantitatively.

Even Q01 was less secure than its interval suggested: it crossed catalyst, solvent, concentration, and stirring effects. The prediction rationale acknowledged this structural uncertainty, but several 80% intervals—particularly conversion and safety intervals—were still too confident relative to K1’s stated limitations. Score intervals were also fragile because I did not identify the exact nonlinear score mapping; I inferred score jointly from nearby observed outcomes.

7. Limitations of the sealed recommendation

Batch 12 was the highest final-assay score among the twelve observed batches, at 0.4953, and it had an attractive balance of yield 0.7665, selectivity 0.8404, byproduct 0.1442, degradation 0.0815, and post-quench risk 0.0798. It is therefore the sample-best completed batch.

It was not proven globally optimal. The campaign did not densely search temperature, time, catalyst loading, concentration, stirring, solvent volume, or quench timing. The apparent useful time region of roughly 2400–3300 s was supported by only a few points, with the 2400 s point also confounded by quenching. Conditions such as 2100, 2700, or 3000 s with prompt quench might perform better. A slightly different target temperature could also improve the conversion–degradation balance.

Repeatability was not demonstrated because Batch 12 had no exact replicate. I would test repeatability with multiple independently initialized repetitions, using both HPLC and final assay and comparing the full metric vector rather than score alone. The key quantities would be between-batch variability in yield, selectivity, degradation, risk, and actual temperature change.

Local robustness should be tested with a small designed neighborhood around Batch 12, for example 410/420/430 K crossed with approximately 2100/2400/2700 s, all with a standardized prompt quench. Small perturbations in reagent amount, catalyst amount, solvent volume, and stirring would reveal whether the recommendation lies on a broad plateau or a narrow ridge. Quench delay should be varied explicitly because practical execution may not be instantaneous.

Material robustness would require repeating the local design with catalysts A and B and at least one nonaqueous solvent. The present evidence supports Batch 12 only for catalyst D in water; it does not establish a material-independent rule. Cross-world generalization would require repetition under independent world instances or latent parameter draws. The anonymous benchmark categories and synthetic calibration make transfer to a real chemical system especially unjustified.

Finally, the quench operation received a high-cost constraint flag in Batch 12. Depending on how a future objective weights cost against chemistry and safety, the same operation may not remain preferred. The sealed recommendation is therefore best understood as the highest-performing observed compromise in this campaign, not as a proven optimum, universally robust recipe, or validated real-world process.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 106.5 | none | 0 |
| Q | yes | 0 | 116.2 | none | 0 |
| K2 | yes | 0 | 101.8 | none | 0 |

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean 80% width | Mean interval score |
|---|---:|---:|---:|---:|
| byproduct_signal | 0.0475 | 0.9833 | 0.2150 | 0.2157 |
| conversion | 0.0594 | 0.4000 | 0.1325 | 0.2595 |
| safety_risk | 0.0214 | 1.0000 | 0.1392 | 0.1392 |
| score | 0.0517 | 0.9167 | 0.1842 | 0.2082 |
| selectivity | 0.0522 | 0.8333 | 0.2092 | 0.2579 |
| yield | 0.0875 | 0.6667 | 0.2117 | 0.4511 |

## Predictions versus released reference truth

### Q01

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3300 | 0.2400 | 0.4300 | 0.2826 | 0.2852, 0.2894, 0.2712, 0.2806, 0.2868 |
| conversion | 0.9500 | 0.8800 | 0.9900 | 0.9936 | 0.9944, 0.9886, 0.9985, 1.0000, 0.9865 |
| safety_risk | 0.2800 | 0.2300 | 0.3400 | 0.2975 | 0.2975, 0.2975, 0.2975, 0.2975, 0.2975 |
| score | 0.3300 | 0.2500 | 0.4100 | 0.3741 | 0.3745, 0.3704, 0.3762, 0.3731, 0.3761 |
| selectivity | 0.6900 | 0.5900 | 0.7700 | 0.7204 | 0.7250, 0.7175, 0.7148, 0.7117, 0.7328 |
| yield | 0.6500 | 0.5500 | 0.7300 | 0.7164 | 0.7143, 0.7102, 0.7240, 0.7179, 0.7156 |
### Q02

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3300 | 0.2400 | 0.4300 | 0.2861 | 0.2908, 0.2824, 0.2881, 0.2929, 0.2764 |
| conversion | 0.9500 | 0.8800 | 0.9900 | 0.9921 | 0.9993, 1.0000, 0.9838, 0.9912, 0.9863 |
| safety_risk | 0.1300 | 0.0800 | 0.2000 | 0.1512 | 0.1512, 0.1512, 0.1512, 0.1512, 0.1512 |
| score | 0.3700 | 0.2800 | 0.4600 | 0.4400 | 0.4421, 0.4407, 0.4410, 0.4418, 0.4345 |
| selectivity | 0.6900 | 0.5900 | 0.7700 | 0.7247 | 0.7349, 0.7269, 0.7271, 0.7216, 0.7132 |
| yield | 0.6500 | 0.5500 | 0.7300 | 0.7228 | 0.7198, 0.7212, 0.7257, 0.7294, 0.7176 |
### Q03

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2700 | 0.1800 | 0.3700 | 0.2305 | 0.2338, 0.2259, 0.2177, 0.2369, 0.2383 |
| conversion | 0.8700 | 0.7600 | 0.9400 | 0.9608 | 0.9596, 0.9490, 0.9674, 0.9626, 0.9652 |
| safety_risk | 0.1700 | 0.1200 | 0.2300 | 0.1854 | 0.1854, 0.1854, 0.1854, 0.1854, 0.1854 |
| score | 0.3600 | 0.2700 | 0.4500 | 0.4438 | 0.4466, 0.4474, 0.4404, 0.4439, 0.4408 |
| selectivity | 0.7200 | 0.6200 | 0.8000 | 0.7671 | 0.7763, 0.7752, 0.7648, 0.7603, 0.7591 |
| yield | 0.6200 | 0.5100 | 0.7100 | 0.7437 | 0.7453, 0.7506, 0.7349, 0.7477, 0.7399 |
### Q04

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3500 | 0.2500 | 0.4700 | 0.3349 | 0.3411, 0.3290, 0.3394, 0.3241, 0.3407 |
| conversion | 0.9700 | 0.9100 | 1.0000 | 0.9971 | 0.9964, 0.9936, 0.9975, 0.9981, 1.0000 |
| safety_risk | 0.3800 | 0.3100 | 0.4600 | 0.4031 | 0.4031, 0.4031, 0.4031, 0.4031, 0.4031 |
| score | 0.2700 | 0.1800 | 0.3600 | 0.2995 | 0.3030, 0.2973, 0.3051, 0.2950, 0.2974 |
| selectivity | 0.6500 | 0.5300 | 0.7500 | 0.6731 | 0.6859, 0.6698, 0.6734, 0.6614, 0.6750 |
| yield | 0.6300 | 0.5100 | 0.7200 | 0.6776 | 0.6782, 0.6748, 0.6911, 0.6732, 0.6704 |
### Q05

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1900 | 0.1100 | 0.2900 | 0.1390 | 0.1313, 0.1497, 0.1384, 0.1357, 0.1399 |
| conversion | 0.7500 | 0.6200 | 0.8500 | 0.8939 | 0.9038, 0.8951, 0.8931, 0.8821, 0.8954 |
| safety_risk | 0.2800 | 0.2200 | 0.3400 | 0.2972 | 0.2972, 0.2972, 0.2972, 0.2972, 0.2972 |
| score | 0.3400 | 0.2500 | 0.4300 | 0.4181 | 0.4209, 0.4187, 0.4150, 0.4146, 0.4214 |
| selectivity | 0.7800 | 0.6800 | 0.8600 | 0.8564 | 0.8553, 0.8572, 0.8540, 0.8567, 0.8586 |
| yield | 0.5800 | 0.4700 | 0.6800 | 0.7624 | 0.7676, 0.7631, 0.7562, 0.7563, 0.7688 |
### Q06

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4200 | 0.3100 | 0.5400 | 0.4142 | 0.4168, 0.4031, 0.4113, 0.4196, 0.4205 |
| conversion | 0.9900 | 0.9500 | 1.0000 | 0.9945 | 0.9842, 0.9940, 0.9980, 1.0000, 0.9961 |
| safety_risk | 0.2800 | 0.2200 | 0.3400 | 0.2972 | 0.2972, 0.2972, 0.2972, 0.2972, 0.2972 |
| score | 0.2800 | 0.1900 | 0.3700 | 0.2977 | 0.2966, 0.2960, 0.3021, 0.2986, 0.2951 |
| selectivity | 0.6000 | 0.4800 | 0.7000 | 0.6004 | 0.6005, 0.5997, 0.6043, 0.6057, 0.5920 |
| yield | 0.5900 | 0.4700 | 0.6800 | 0.6037 | 0.6035, 0.6000, 0.6114, 0.6014, 0.6020 |
### Q07

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3800 | 0.2600 | 0.5100 | 0.3184 | 0.3152, 0.3252, 0.3252, 0.3153, 0.3110 |
| conversion | 0.9700 | 0.8900 | 1.0000 | 0.9980 | 1.0000, 1.0000, 1.0000, 1.0000, 0.9902 |
| safety_risk | 0.3900 | 0.3100 | 0.4800 | 0.4275 | 0.4275, 0.4275, 0.4275, 0.4275, 0.4275 |
| score | 0.2600 | 0.1600 | 0.3600 | 0.3011 | 0.3054, 0.3035, 0.2994, 0.2993, 0.2978 |
| selectivity | 0.6300 | 0.4900 | 0.7400 | 0.6925 | 0.7058, 0.6881, 0.6972, 0.6796, 0.6920 |
| yield | 0.6100 | 0.4800 | 0.7100 | 0.6972 | 0.6993, 0.7056, 0.6895, 0.7005, 0.6912 |
### Q08

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3000 | 0.2000 | 0.4200 | 0.3216 | 0.3273, 0.3191, 0.3086, 0.3218, 0.3312 |
| conversion | 0.9600 | 0.8800 | 0.9900 | 0.9968 | 0.9991, 1.0000, 0.9973, 0.9961, 0.9914 |
| safety_risk | 0.1800 | 0.1200 | 0.2700 | 0.1975 | 0.1975, 0.1975, 0.1975, 0.1975, 0.1975 |
| score | 0.3900 | 0.2900 | 0.4800 | 0.4075 | 0.4073, 0.4070, 0.4041, 0.4125, 0.4069 |
| selectivity | 0.7000 | 0.5800 | 0.7900 | 0.7016 | 0.7006, 0.7052, 0.6910, 0.7046, 0.7067 |
| yield | 0.6700 | 0.5500 | 0.7600 | 0.6992 | 0.6986, 0.6948, 0.6970, 0.7099, 0.6957 |
### Q09

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2300 | 0.1400 | 0.3400 | 0.1517 | 0.1510, 0.1588, 0.1357, 0.1541, 0.1589 |
| conversion | 0.8400 | 0.7200 | 0.9200 | 0.9456 | 0.9443, 0.9462, 0.9392, 0.9438, 0.9543 |
| safety_risk | 0.3500 | 0.2800 | 0.4300 | 0.3768 | 0.3768, 0.3768, 0.3768, 0.3768, 0.3768 |
| score | 0.3200 | 0.2300 | 0.4100 | 0.3984 | 0.3958, 0.4013, 0.3970, 0.3990, 0.3989 |
| selectivity | 0.7300 | 0.6200 | 0.8200 | 0.8476 | 0.8351, 0.8618, 0.8575, 0.8339, 0.8498 |
| yield | 0.6100 | 0.5000 | 0.7100 | 0.7952 | 0.7969, 0.7935, 0.7871, 0.8057, 0.7929 |
### Q10

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2300 | 0.1400 | 0.3400 | 0.1532 | 0.1524, 0.1604, 0.1493, 0.1485, 0.1556 |
| conversion | 0.8400 | 0.7200 | 0.9200 | 0.9459 | 0.9443, 0.9377, 0.9581, 0.9487, 0.9408 |
| safety_risk | 0.1800 | 0.1100 | 0.2600 | 0.1712 | 0.1712, 0.1712, 0.1712, 0.1712, 0.1712 |
| score | 0.3700 | 0.2700 | 0.4600 | 0.4888 | 0.4881, 0.4857, 0.4916, 0.4910, 0.4875 |
| selectivity | 0.7300 | 0.6200 | 0.8200 | 0.8509 | 0.8547, 0.8603, 0.8394, 0.8540, 0.8458 |
| yield | 0.6100 | 0.5000 | 0.7100 | 0.7961 | 0.7925, 0.7846, 0.8071, 0.7989, 0.7972 |
### Q11

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2700 | 0.1700 | 0.3900 | 0.3207 | 0.3220, 0.3285, 0.3186, 0.3278, 0.3067 |
| conversion | 0.9000 | 0.7900 | 0.9600 | 0.9808 | 0.9709, 0.9777, 0.9940, 0.9742, 0.9873 |
| safety_risk | 0.1300 | 0.0800 | 0.2000 | 0.1548 | 0.1548, 0.1548, 0.1548, 0.1548, 0.1548 |
| score | 0.4100 | 0.3100 | 0.5000 | 0.4068 | 0.4034, 0.4056, 0.4113, 0.4075, 0.4063 |
| selectivity | 0.7400 | 0.6200 | 0.8300 | 0.6769 | 0.6720, 0.6683, 0.6786, 0.6851, 0.6803 |
| yield | 0.6700 | 0.5500 | 0.7600 | 0.6732 | 0.6701, 0.6762, 0.6801, 0.6713, 0.6682 |
### Q12

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5000 | 0.3600 | 0.6500 | 0.5786 | 0.5786, 0.5797, 0.5783, 0.5826, 0.5738 |
| conversion | 1.0000 | 0.9700 | 1.0000 | 0.9966 | 0.9974, 0.9885, 0.9990, 0.9992, 0.9990 |
| safety_risk | 0.4500 | 0.3600 | 0.5600 | 0.4202 | 0.4202, 0.4202, 0.4202, 0.4202, 0.4202 |
| score | 0.1800 | 0.0900 | 0.2900 | 0.1418 | 0.1464, 0.1386, 0.1392, 0.1429, 0.1417 |
| selectivity | 0.5000 | 0.3500 | 0.6300 | 0.4511 | 0.4571, 0.4436, 0.4565, 0.4418, 0.4566 |
| yield | 0.5000 | 0.3500 | 0.6300 | 0.4475 | 0.4551, 0.4464, 0.4372, 0.4555, 0.4432 |

## Recommendation retest

- Selected source batch: `12`
- Retest exact replay verified: `True`
- Retest failure: `none`

| Metric | Selected source batch | Independent retest | Retest minus source |
|---|---:|---:|---:|
| byproduct_signal | 0.1442 | 0.1467 | 0.0025 |
| conversion | 0.9132 | 0.9022 | -0.0109 |
| cost | 0.7678 | 0.7678 | 0.0000 |
| degradation_warning | 0.0815 | 0.0852 | 0.0037 |
| safety_risk | 0.0798 | 0.0798 | 0.0000 |
| score | 0.4953 | 0.4968 | 0.0015 |
| selectivity | 0.8404 | 0.8596 | 0.0192 |
| virtual_spectrum_summary | 0.1160 | 0.1190 | 0.0030 |
| yield | 0.7665 | 0.7609 | -0.0056 |

## Scope note

This is the final sanitized report produced after all 60 source sessions and K1/Q/K2 chains were sealed. It includes released reference truth, blind-prediction evaluation, and the independent recommendation retest. Provider-private event streams, credentials, thread identifiers, and token accounting remain excluded.
