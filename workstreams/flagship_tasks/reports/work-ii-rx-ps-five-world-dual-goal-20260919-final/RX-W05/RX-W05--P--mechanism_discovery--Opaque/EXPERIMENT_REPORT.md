# RX-W05--P--mechanism_discovery--Opaque

## Run summary

- World: `RX-W05`
- Locus: `P`
- Goal: `mechanism_discovery`
- Arm: `Opaque`
- Status: `completed`
- Source status: `completed`
- Experimental sessions: `12/12`
- Operations: `86`
- Exact replay verified: `True`
- Rollbacks: `[]`
- Posttest chain sealed: `True`

### Recovery status

No recovery override was required for this task.

## Sealed recommendation

- Selected batch: `9`
- Rationale: Batch 9 gave the highest final safe score and yield observed, with Catalyst D in acetonitrile at a 380 K boundary target for 3600 s; its measured safety risk remained below the 0.35 limit.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S2 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.4562 | 0.7891 | 0.5899 | 0.1100 | 0.0267 | 0.1722 | 0.2613 |
| 2 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.5400 | 0.7593 | 0.6901 | 0.1670 | 0.0846 | 0.1835 | 0.2923 |
| 3 | S2 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.3392 | 0.6564 | 0.5016 | 0.1789 | 0.0185 | 0.1609 | 0.1776 |
| 4 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.6134 | 0.7978 | 0.7659 | 0.1396 | 0.0918 | 0.1913 | 0.3353 |
| 5 | S0 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.5306 | 0.8324 | 0.6370 | 0.1093 | 0.0463 | 0.1385 | 0.3217 |
| 6 | S1 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.5177 | 0.7996 | 0.6523 | 0.1372 | 0.0929 | 0.1629 | 0.2989 |
| 7 | S3 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.4482 | 0.6823 | 0.6671 | 0.2282 | 0.0826 | 0.1891 | 0.2315 |
| 8 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 320 K x 3600 s @ 600 rpm | no | 0.4252 | 0.8186 | 0.5231 | 0.0929 | 0.0477 | 0.1641 | 0.2532 |
| 9 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 380 K x 3600 s @ 600 rpm | no | 0.7054 | 0.7744 | 0.9143 | 0.2294 | 0.1346 | 0.2271 | 0.3650 |
| 10 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 380 K x 900 s @ 600 rpm | no | 0.3359 | 0.9137 | 0.3553 | 0.0357 | 0.0000 | 0.1749 | 0.2196 |
| 11 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 380 K x 7200 s @ 600 rpm | yes | 0.5652 | 0.5956 | 0.9859 | 0.4243 | 0.3419 | 0.2033 | 0.2821 |
| 12 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 380 K x 1800 s @ 600 rpm → 380 K x 1800 s @ 600 rpm | no | 0.7020 | 0.7650 | 0.9146 | 0.2397 | 0.1617 | 0.2378 | 0.3565 |

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
    "byproduct_signal": 0.11001566797494888,
    "conversion": 0.5899218320846558,
    "cost": 1.0,
    "degradation_warning": 0.026732292026281357,
    "safety_risk": 0.1721860021352768,
    "score": 0.2612607479095459,
    "selectivity": 0.789099931716919,
    "virtual_spectrum_summary": 0.07253815233707428,
    "yield": 0.456193208694458
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
    "byproduct_signal": 0.16696740686893463,
    "conversion": 0.6901318430900574,
    "cost": 1.0,
    "degradation_warning": 0.08457121253013611,
    "safety_risk": 0.18354207277297974,
    "score": 0.29225286841392517,
    "selectivity": 0.7593082189559937,
    "virtual_spectrum_summary": 0.129889115691185,
    "yield": 0.5400164127349854
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
    "byproduct_signal": 0.17888358235359192,
    "conversion": 0.5016093254089355,
    "cost": 1.0,
    "degradation_warning": 0.018501153215765953,
    "safety_risk": 0.16085678339004517,
    "score": 0.17757673561573029,
    "selectivity": 0.656446099281311,
    "virtual_spectrum_summary": 0.1067114844918251,
    "yield": 0.33922457695007324
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
    "byproduct_signal": 0.13963569700717926,
    "conversion": 0.7659003734588623,
    "cost": 1.0,
    "degradation_warning": 0.09178891777992249,
    "safety_risk": 0.19127100706100464,
    "score": 0.3353252410888672,
    "selectivity": 0.7977863550186157,
    "virtual_spectrum_summary": 0.11810465157032013,
    "yield": 0.613401472568512
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
  "end_step": 35,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.10927671939134598,
    "conversion": 0.637036144733429,
    "cost": 1.0,
    "degradation_warning": 0.046320151537656784,
    "safety_risk": 0.13849443197250366,
    "score": 0.32172656059265137,
    "selectivity": 0.8323798775672913,
    "virtual_spectrum_summary": 0.08094625920057297,
    "yield": 0.5306262373924255
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
  "end_step": 42,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.13720594346523285,
    "conversion": 0.6523333191871643,
    "cost": 1.0,
    "degradation_warning": 0.09291156381368637,
    "safety_risk": 0.16294914484024048,
    "score": 0.29888617992401123,
    "selectivity": 0.7995569109916687,
    "virtual_spectrum_summary": 0.1172734797000885,
    "yield": 0.5177268385887146
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
  "end_step": 49,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.22822341322898865,
    "conversion": 0.6671411991119385,
    "cost": 1.0,
    "degradation_warning": 0.08256519585847855,
    "safety_risk": 0.1891244351863861,
    "score": 0.23146595060825348,
    "selectivity": 0.6823187470436096,
    "virtual_spectrum_summary": 0.16267721354961395,
    "yield": 0.44819533824920654
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
    "byproduct_signal": 0.09290929138660431,
    "conversion": 0.5231240391731262,
    "cost": 1.0,
    "degradation_warning": 0.04768185690045357,
    "safety_risk": 0.16405753791332245,
    "score": 0.25320592522621155,
    "selectivity": 0.8186131119728088,
    "virtual_spectrum_summary": 0.07255694270133972,
    "yield": 0.4251653254032135
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
    "byproduct_signal": 0.22939935326576233,
    "conversion": 0.9143123626708984,
    "cost": 1.0,
    "degradation_warning": 0.13463914394378662,
    "safety_risk": 0.22708351910114288,
    "score": 0.3649818003177643,
    "selectivity": 0.774368941783905,
    "virtual_spectrum_summary": 0.18675725162029266,
    "yield": 0.7053647637367249
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
      "duration_s": 900,
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
  "end_step": 70,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.0356522761285305,
    "conversion": 0.35526925325393677,
    "cost": 1.0,
    "degradation_warning": 0.0,
    "safety_risk": 0.1748797446489334,
    "score": 0.21961678564548492,
    "selectivity": 0.9136809706687927,
    "virtual_spectrum_summary": 0.0196087509393692,
    "yield": 0.335913747549057
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
    "byproduct_signal": 0.4242929518222809,
    "conversion": 0.9858879446983337,
    "cost": 1.0,
    "degradation_warning": 0.34194472432136536,
    "safety_risk": 0.20325224101543427,
    "score": 0.2821158170700073,
    "selectivity": 0.5956110954284668,
    "virtual_spectrum_summary": 0.38723623752593994,
    "yield": 0.5652194023132324
  },
  "ordinal": 11
}
```

### Batch 12

Lifecycle index: `12`; end step: `86`.

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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 380
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 380
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 86,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.23969492316246033,
    "conversion": 0.9146039485931396,
    "cost": 1.0,
    "degradation_warning": 0.16166041791439056,
    "safety_risk": 0.23780791461467743,
    "score": 0.35649725794792175,
    "selectivity": 0.7649689316749573,
    "virtual_spectrum_summary": 0.2045793980360031,
    "yield": 0.7020204663276672
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

Scope and evidence basis

This report concerns only the anonymous synthetic benchmark world that was experimentally observed. The real solvent names identify selectable materials, but the catalyst identities and reacting species are opaque, and the solvent effects are categorical benchmark effects. I therefore do not infer a named real reaction or catalyst. All numerical results below are actual public observations unless explicitly labeled as an inference, extrapolation, or hypothesis.

All twelve experiments used 0.040 mol of limiting reagent, 0.005 mol of catalyst, 0.080 L of solvent, and 600 rpm stirring. Thus, the campaign identified categorical catalyst and solvent effects and temperature/time effects at one composition and catalyst loading; it did not determine concentration or catalyst-order laws.

Proposed process picture

The simplest account consistent with the observations is a temperature-dependent network containing desired formation, competing conversion, and destruction of already formed target:

R --kP--> P
R --kB--> B
P --kD--> D

Here R is the limiting reactant, P the target, B a directly formed byproduct pool, and D a degradation pool. The measured byproduct signal may combine B and some degradation products, while degradation_warning appears to be a more specific indicator of the destructive branch.

A useful provisional model is:

dR/dt = -a(t)[kP(T,c,s) + kB(T,c,s)]R

dP/dt = a(t)kP(T,c,s)R - kD(T,c,s)P

dB/dt = a(t)kB(T,c,s)R + alpha*kD(T,c,s)P

da/dt = -kd(T,c,s)a

where c denotes catalyst category, s denotes solvent category, and a(t) is an optional active-catalyst fraction. Each rate constant could be represented locally by

ki(T,c,s) = Ai * fc,i(c) * fs,i(s) * exp[-Ei/(Rgas*T)].

This is a mechanistic hypothesis, not a uniquely fitted law. The data clearly require at least one desired and one undesired channel. Catalyst deactivation is plausible but not required: substrate depletion plus P degradation can also explain the time course.

Temperature should be treated as a dynamic state rather than equated with the requested boundary temperature. A minimal thermal model would be

dT/dt = (Tset - T)/tau + Qreaction/C,

with the simulator’s observed thermal lag and possible reaction heat absorbed into effective parameters. A single 3600 s heat operation requested at 350 K produced temperature rises of about 49.17–49.18 K, whereas a single 3600 s operation requested at 380 K produced a 75.16 K rise. In batch 12, the first 1800 s operation at 380 K raised temperature by 75.32 K, and the second raised it by another 4.65 K. Thus two recipes with the same nominal setpoint and total duration need not have identical thermal trajectories.

Catalyst effects

Batches 1–4 screened the four catalysts in acetonitrile at a 350 K requested temperature for 3600 s:

- Batch 1, Catalyst A: final conversion 0.5899, yield 0.4562, selectivity 0.7891, byproduct signal 0.1100, degradation warning 0.0267, safety risk 0.1722.
- Batch 2, Catalyst B: conversion 0.6901, yield 0.5400, selectivity 0.7593, byproduct 0.1670, degradation 0.0846, risk 0.1835.
- Batch 3, Catalyst C: conversion 0.5016, yield 0.3392, selectivity 0.6564, byproduct 0.1789, degradation 0.0185, risk 0.1609.
- Batch 4, Catalyst D: conversion 0.7659, yield 0.6134, selectivity 0.7978, byproduct 0.1396, degradation 0.0918, risk 0.1913.

These experiments changed my initial catalyst-agnostic explanation. Catalyst D is not merely a generic acceleration factor: it produced both the greatest conversion and greatest target yield, while retaining better selectivity than B or C. Catalyst C was poor in both activity and selectivity. Catalyst-dependent multipliers should therefore be allowed to differ between kP and kB rather than multiplying every reaction equally. Catalyst D also carried greater observed thermal/safety risk than A or C under this condition, suggesting coupling among catalyst identity, reaction rate, heat generation, and the risk metric.

Solvent effects

Batches 4–7 held Catalyst D and the 350 K/3600 s program constant while changing solvent:

- Batch 4, acetonitrile: conversion 0.7659, yield 0.6134, selectivity 0.7978, byproduct 0.1396, degradation 0.0918, risk 0.1913.
- Batch 5, water: conversion 0.6370, yield 0.5306, selectivity 0.8324, byproduct 0.1093, degradation 0.0463, risk 0.1385.
- Batch 6, ethanol: conversion 0.6523, yield 0.5177, selectivity 0.7996, byproduct 0.1372, degradation 0.0929, risk 0.1629.
- Batch 7, toluene: conversion 0.6671, yield 0.4482, selectivity 0.6823, byproduct 0.2282, degradation 0.0826, risk 0.1891.

Acetonitrile gave the greatest conversion and yield. Water reduced the apparent reaction rate but improved selectivity, lowered both undesirable signals, and had the lowest risk. Toluene maintained moderate conversion but strongly redirected converted material away from target. This supports solvent-specific effects on the ratio kP/kB and possibly kD, not only on the overall rate. In this benchmark, water is the conservative selective medium, acetonitrile is the productive medium, and toluene favors the competing channel.

Temperature effects

With Catalyst D and acetonitrile for 3600 s, batches 8, 4, and 9 form a temperature series:

- Batch 8, requested 320 K: conversion 0.5231, yield 0.4252, selectivity 0.8186, byproduct 0.0929, degradation 0.0477, risk 0.1641.
- Batch 4, requested 350 K: conversion 0.7659, yield 0.6134, selectivity 0.7978, byproduct 0.1396, degradation 0.0918, risk 0.1913.
- Batch 9, requested 380 K: conversion 0.9143, yield 0.7054, selectivity 0.7744, byproduct 0.2294, degradation 0.1346, risk 0.2271.

Increasing requested temperature accelerated conversion and raised target yield over this one-hour window, but selectivity fell and both byproduct and degradation signals rose. The undesired pathways therefore have substantial temperature dependence. The 380 K condition was still productive at 3600 s, but the trend warns against assuming that still higher temperature would improve yield.

Time dependence and the yield maximum

The 380 K experiments provide the clearest evidence for sequential degradation and a finite optimum time:

- Batch 10, 900 s: conversion 0.3553, yield 0.3359, selectivity 0.9137, byproduct 0.0357, degradation warning reported as 0, risk 0.1749.
- Batch 12, after its first 1800 s segment, HPLC: conversion 0.6769, yield 0.5974, selectivity 0.8780, byproduct 0.0935, risk 0.2066.
- Batch 9, 3600 s final assay: conversion 0.9143, yield 0.7054, selectivity 0.7744, byproduct 0.2294, degradation 0.1346, risk 0.2271.
- Batch 11, 7200 s and then quenched: final conversion 0.9859, yield 0.5652, selectivity 0.5956, byproduct 0.4243, degradation 0.3419, post-quench risk 0.2033. Immediately before quenching, HPLC gave conversion 0.9986, yield 0.5848, selectivity 0.5590, and byproduct 0.4228.

A simple pseudo-first-order calculation, used only as a diagnostic, gives -ln(1-X)/t values of approximately 4.88e-4, 6.28e-4, 6.83e-4, and 5.92e-4 s^-1 at 900, 1800, 3600, and 7200 s respectively. Their imperfect constancy is unsurprising because the batches had different thermal histories and instruments and may include catalyst-state changes. Nevertheless, conversion approaches completion in a roughly saturating manner.

The more important observation is that target yield peaks near 3600 s and then declines even while conversion increases from 0.914 to 0.986. Selectivity simultaneously falls from 0.774 to 0.596, byproduct approximately doubles, and degradation warning rises from 0.135 to 0.342. A purely parallel model R→P and R→B can make selectivity change as conditions evolve, but it does not naturally explain loss of target after near-complete conversion. The P→D step is therefore strongly supported.

Thermal-history coupling

Batch 12 divided the nominal 3600 s at 380 K into two 1800 s heat operations. Its final conversion was 0.9146, yield 0.7020, selectivity 0.7650, byproduct 0.2397, degradation 0.1617, and risk 0.2378. Batch 9 used one continuous 3600 s operation and gave conversion 0.9143, yield 0.7054, selectivity 0.7744, byproduct 0.2294, degradation 0.1346, and risk 0.2271.

The conversion and yield agree closely, supporting cumulative exposure as the principal driver. However, the segmented run acquired an additional 4.65 K temperature rise during its second segment and had somewhat greater degradation and risk. This is evidence that actual temperature history matters beyond the nominal setpoint-duration pair. Because there was only one batch of each type and no replicate, the smaller differences could also be process or measurement noise.

Termination and quench

Only batch 11 included an explicit quench before termination. Quenching lowered temperature by 45 K in 54.7 s and reduced the displayed risk by 0.0264, from 0.2296 to 0.2033. Thus quench has a clear physical cooling and risk-control role.

The pre-quench HPLC and post-quench final assay differed, but they are different instruments with different uncertainties. Their byproduct signals were almost identical (0.4228 versus 0.4243), while conversion, yield, and selectivity shifted modestly. These data do not establish whether quenching chemically changes product distribution. The defensible conclusion is that prompt termination around the yield maximum avoids further hot aging; the chemical efficacy of the quench itself remains unidentified.

Safety coupling

All observed batches remained below the stated safety limit of 0.35. Risk increased with more aggressive catalyst/solvent/temperature combinations and with thermal exposure, while quenching reduced it. At 380 K, risks were 0.1749 after 900 s, 0.2066 after the first 1800 s segment, and 0.2271 after a continuous 3600 s. The long batch reached 0.2296 before quench. The risk metric is therefore coupled to formulation, temperature, and history rather than being a simple function of final conversion.

The public score was treated as secondary. Batch 9 nevertheless gave the highest observed final score, 0.3650, and was selected as the sealed recommendation. Batch 12 scored 0.3565. The recommendation is empirical within the tested grid, not proof of a global optimum.

How the explanation developed

1. Batch 1 established that appreciable target and byproduct form under the initial Catalyst A/acetonitrile/350 K condition.
2. Batches 2–4 showed large catalyst-specific changes. This rejected a model in which catalyst identity merely changes cost or risk and motivated separate catalyst effects on desired and competing rates. Catalyst D became the basis for subsequent studies.
3. Batches 5–7 showed that solvent controls activity, selectivity, and risk independently. Toluene in particular revealed strong diversion into byproduct, while water revealed a slower but cleaner regime.
4. Batches 8 and 9 established that temperature raises conversion and yield over 3600 s but erodes selectivity and increases degradation.
5. Batch 10 and the midpoint of batch 12 showed a clean, highly selective early-time regime.
6. Batch 11 demonstrated that prolonged heating beyond high conversion destroys yield and strongly raises byproduct and degradation signals. This was the main reason for adding the sequential P→D pathway.
7. Batch 12 showed that nominally equal total setpoint time can have a different detailed thermal history, although cumulative exposure still predicted conversion and yield reasonably well.

Applicability and predictive use

Within the measured domain—0.040 mol reagent, 0.005 mol catalyst, 0.080 L solvent, 600 rpm, requested temperatures of 320–380 K, and heating times of 900–7200 s—the model predicts:

- Catalyst D in acetonitrile gives the greatest target productivity among tested categories.
- At fixed time, higher temperature increases conversion but decreases selectivity.
- At 380 K, extending time initially raises yield, but heating much beyond about 3600 s causes net target loss through degradation.
- Water should give a safer and more selective but lower-yield process near the tested condition.
- Toluene should give inferior target selectivity.
- Quenching or otherwise cooling promptly after the desired exposure should reduce physical risk and may prevent further degradation, though a chemical quench benefit was not independently demonstrated.

Interpolation near the tested points is more credible than extrapolation. Predictions above 380 K, below 320 K, beyond 7200 s, at different loadings, or for mixed solvents would be speculative.

Unidentified factors and competing explanations

- No replicate batches were performed, so process variability cannot be separated from small mechanistic effects.
- HPLC and final assay have different noise models and were sometimes used at different process stages. Small pre/post differences should not be treated as reaction changes.
- Only one catalyst loading, reagent loading, solvent volume, stirring rate, and addition protocol was tested. Reaction orders, mass-transfer limitation, catalyst saturation, and concentration effects are unidentified.
- Catalyst deactivation is plausible from the modest decline in apparent conversion rate at long time, but substrate depletion, thermal lag, or reversible catalyst inhibition could explain the same pattern.
- The falling target yield at long time supports target degradation, but another viable explanation is a reversible target/byproduct network whose equilibrium shifts with temperature. Distinguishing irreversible P→D from P⇌B would require cooling/reheating or time-resolved measurements not available here.
- The degradation warning may track a species different from the byproduct signal. Their correlation does not prove that all byproduct is formed from target.
- Absolute internal temperature, reaction heat release, heat-transfer coefficient, and spatial gradients were not directly identified. Only operation-level temperature changes were observed.
- The quench experiment was confounded with the longest heat treatment and a change of analytical instrument. Quench chemistry remains uncertain.
- Sampling slightly changed volume, although the effect is small relative to 0.080 L.
- The real identities of R, P, B, D, and the catalysts are intentionally hidden. Assigning a real chemical mechanism would be unjustified.

Overall conclusion

The most defensible account is a thermally activated catalytic network in which desired target formation competes with direct byproduct formation and is followed by target degradation at prolonged high-temperature exposure. Catalyst and solvent categories independently alter both total activity and pathway partitioning. Catalyst D/acetonitrile is the most productive tested combination, while water provides a cleaner, lower-risk regime. Actual thermal history matters: the vessel approaches the requested temperature dynamically, and continued heating after conversion is high drives the system away from target. The observed optimum is therefore a kinetic stopping point near the batch-9 exposure, not an equilibrium maximum and not necessarily a global optimum outside the tested domain.

## Q — Blind predictions

### Overall rationale

The predictions use the campaign-supported network of desired formation competing with direct byproduct formation, followed by temperature- and time-dependent target degradation. Catalyst B/acetonitrile data at 350 K anchor the catalyst-specific response; the Catalyst D temperature and time series supplies the qualitative thermal scaling and the existence of a finite yield maximum. Actual temperature is treated as lagging the requested boundary temperature, so short high-temperature operations are less severe than their nominal setpoints alone imply. The new batches have higher reagent and catalyst concentrations but much smaller absolute charges than the research batches; I expect somewhat faster chemistry and lower absolute cost/risk contributions from charging. Quench pairs are assigned nearly identical composition but reduced terminal risk. Prediction intervals include final-assay noise, batch variability, uncertainty in concentration and stirring effects, and large structural uncertainty for 420–460 K extrapolation.

### Q01

Catalyst B in acetonitrile should approach high conversion at 420 K and 3300 s, but the temperature is outside the studied range and should accelerate both competing formation and target degradation. The smaller absolute charge should moderate cost and risk relative to the research batches.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3300 | 0.2100 | 0.4700 |
| conversion | 0.9400 | 0.8400 | 0.9900 |
| safety_risk | 0.2200 | 0.1400 | 0.3200 |
| score | 0.2900 | 0.1600 | 0.4300 |
| selectivity | 0.6400 | 0.5000 | 0.7600 |
| yield | 0.6000 | 0.4700 | 0.7000 |

### Q02

The chemical exposure is identical to Q01, so I predict essentially the same composition. The quench should primarily lower terminal temperature and displayed safety risk; the campaign did not establish a reproducible quench-induced composition change.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3300 | 0.2100 | 0.4700 |
| conversion | 0.9400 | 0.8400 | 0.9900 |
| safety_risk | 0.1700 | 0.0900 | 0.2600 |
| score | 0.3100 | 0.1700 | 0.4600 |
| selectivity | 0.6400 | 0.5000 | 0.7600 |
| yield | 0.6000 | 0.4700 | 0.7000 |

### Q03

At 390 K the batch should be slower and cleaner than Q01. Extrapolation from the 350–380 K series suggests substantial conversion after 3300 s, with less degradation and slightly greater selectivity than at 420 K.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2300 | 0.1400 | 0.3500 |
| conversion | 0.8500 | 0.7300 | 0.9400 |
| safety_risk | 0.1500 | 0.0900 | 0.2300 |
| score | 0.3600 | 0.2300 | 0.4900 |
| selectivity | 0.7200 | 0.6000 | 0.8200 |
| yield | 0.6100 | 0.4900 | 0.7100 |

### Q04

A 450 K request for 3300 s should drive nearly complete conversion but also strongly accelerate direct byproduct formation and secondary target degradation. This is a substantial temperature extrapolation, so the composition and risk intervals are wide.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5000 | 0.3400 | 0.6700 |
| conversion | 0.9900 | 0.9300 | 1.0000 |
| safety_risk | 0.3100 | 0.2000 | 0.4400 |
| score | 0.1500 | 0.0500 | 0.2900 |
| selectivity | 0.4800 | 0.3200 | 0.6400 |
| yield | 0.4700 | 0.3100 | 0.6100 |

### Q05

The shorter 1500 s exposure should preserve the high early-time selectivity seen in the research while attaining moderate conversion at 420 K. It is predicted to outperform the longer 420 K batches in score because less target has time to degrade.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1300 | 0.0600 | 0.2300 |
| conversion | 0.7000 | 0.5600 | 0.8200 |
| safety_risk | 0.1800 | 0.1100 | 0.2700 |
| score | 0.3800 | 0.2500 | 0.5100 |
| selectivity | 0.8300 | 0.7200 | 0.9100 |
| yield | 0.5800 | 0.4600 | 0.6800 |

### Q06

At 420 K and 5100 s, reactant conversion should be essentially complete, but prolonged hot aging should move a large fraction of target into the degradation/byproduct pool. The prediction follows the yield maximum and subsequent decline observed between 3600 and 7200 s.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5300 | 0.3700 | 0.7000 |
| conversion | 0.9950 | 0.9600 | 1.0000 |
| safety_risk | 0.2400 | 0.1500 | 0.3500 |
| score | 0.1500 | 0.0500 | 0.2900 |
| selectivity | 0.4600 | 0.3000 | 0.6100 |
| yield | 0.4500 | 0.2900 | 0.5900 |

### Q07

The first 390 K segment should form appreciable target, after which the terminal 450 K segment should complete conversion but degrade part of that accumulated target. Because the hottest segment occurs last and begins from an already warm vessel, this ordering is expected to be relatively damaging.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5100 | 0.3400 | 0.6900 |
| conversion | 0.9900 | 0.9300 | 1.0000 |
| safety_risk | 0.3200 | 0.2100 | 0.4500 |
| score | 0.1500 | 0.0500 | 0.2900 |
| selectivity | 0.4800 | 0.3100 | 0.6400 |
| yield | 0.4700 | 0.3000 | 0.6100 |

### Q08

The initial 450 K segment is partly attenuated by thermal ramp-up, and the following 390 K segment should cool or limit further high-temperature damage. I therefore predict less degradation and greater selectivity than for the reverse ordering in Q07, while retaining high conversion.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3700 | 0.2300 | 0.5300 |
| conversion | 0.9600 | 0.8600 | 1.0000 |
| safety_risk | 0.2700 | 0.1700 | 0.3900 |
| score | 0.2500 | 0.1200 | 0.4000 |
| selectivity | 0.6100 | 0.4600 | 0.7400 |
| yield | 0.5800 | 0.4300 | 0.6900 |

### Q09

The 440 K setpoint supplies rapid conversion during a short 1500 s exposure. Thermal lag should prevent the full severity implied by the nominal setpoint, but selectivity should still be lower and risk higher than for the shorter 420 K case.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2100 | 0.1100 | 0.3400 |
| conversion | 0.8200 | 0.6800 | 0.9200 |
| safety_risk | 0.2400 | 0.1500 | 0.3500 |
| score | 0.3400 | 0.2000 | 0.4800 |
| selectivity | 0.7500 | 0.6200 | 0.8500 |
| yield | 0.6100 | 0.4800 | 0.7100 |

### Q10

Composition is predicted to match Q09 within assay and process uncertainty. Quenching should reduce terminal safety risk and consequently improve the public safe score modestly, without a confidently identifiable chemical redistribution.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2100 | 0.1100 | 0.3400 |
| conversion | 0.8200 | 0.6800 | 0.9200 |
| safety_risk | 0.1800 | 0.0900 | 0.2800 |
| score | 0.3600 | 0.2100 | 0.5100 |
| selectivity | 0.7500 | 0.6200 | 0.8500 |
| yield | 0.6100 | 0.4800 | 0.7100 |

### Q11

The lower 370 K request should limit instantaneous degradation, but 5700 s is long enough for high conversion and appreciable cumulative loss of selectivity. This condition should be safer than the high-temperature queries while giving a moderate final yield.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3100 | 0.1900 | 0.4600 |
| conversion | 0.9100 | 0.8000 | 0.9700 |
| safety_risk | 0.1300 | 0.0700 | 0.2100 |
| score | 0.3300 | 0.1900 | 0.4600 |
| selectivity | 0.6600 | 0.5200 | 0.7800 |
| yield | 0.5900 | 0.4500 | 0.7000 |

### Q12

This is the strongest extrapolation: 460 K for 6300 s should exhaust the reactant and then extensively degrade the target. I predict very high byproduct signal, low surviving target yield and selectivity, elevated safety risk, and a correspondingly low score.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7800 | 0.5800 | 0.9200 |
| conversion | 0.9990 | 0.9800 | 1.0000 |
| safety_risk | 0.4200 | 0.2700 | 0.5900 |
| score | 0.0200 | 0.0000 | 0.0900 |
| selectivity | 0.2000 | 0.0700 | 0.3900 |
| yield | 0.1900 | 0.0600 | 0.3700 |

## K2 — Retrospective analysis

1. Initial claims: supported, contradicted, or untested

The initial material packet contained almost no substantive mechanistic claim. It explicitly said that no task-specific nominal property dossier was supplied, that catalyst and reacting-species identities were opaque, and that experimental evidence was authoritative. It also warned that the named solvents had categorical benchmark effects rather than validated real-chemical property correlations. Consequently, there was no initial kinetic law, catalyst ranking, solvent ranking, activation energy, deactivation model, or recommended temperature to confirm or refute.

The broad claim that catalyst and solvent categories matter was supported. Batches 1–4 showed large catalyst-dependent differences under nominally common conditions, and batches 4–7 showed large solvent-dependent differences with Catalyst D. The warning not to infer a named real mechanism also remains appropriate: none of the observations identifies the anonymous reactant, product, side products, or catalysts.

Several matters remained untested: whether the reaction is homogeneous, whether mixing limits it, whether catalyst loading changes rate proportionally, whether solvents interact with catalyst identity, and whether any real solvent property explains the categorical ordering. The campaign did not test different reagent concentrations, catalyst loadings, or stirring speeds.

There was no direct contradiction of an initial quantitative claim because none was provided. It is important not to confuse that absence with positive validation. Likewise, the absence of a real-material dossier was not evidence that solvent effects must be arbitrary; it merely prevented justified real-chemical interpretation.

There were, however, tensions within my later account. For example, conversion multiplied by selectivity did not always equal reported yield, and HPLC and final-assay estimates sometimes shifted appreciably. That is evidence against treating the processed channels as exact algebraic state variables. K1 partly addressed this by treating the proposed equations as provisional and by noting instrument differences, but it still used conversion, selectivity, and yield rather directly in mechanistic reasoning. The evidence supported qualitative pathway competition more strongly than it supported the exact state definitions in those equations.

2. Experiments that formed or changed my judgments

Batch 1 was mainly an arbitrary baseline: Catalyst A, acetonitrile, 350 K requested temperature, and 3600 s. Acetonitrile, the middle temperature, the one-hour duration, and maximum available charge sizes were not selected from prior kinetic evidence. They were plausible exploratory guesses constrained by the public action ranges.

Batches 2–4 genuinely changed the picture. Holding the other settings fixed while screening Catalysts B, C, and D revealed that Catalyst D gave the greatest final conversion and yield, whereas Catalyst C was poor in both conversion and selectivity. This caused me to reject a catalyst-independent model and to allow catalyst-specific effects on desired and undesired rates. The decision to use Catalyst D thereafter was data-driven.

Batches 5–7 were also strongly informative. They used the batch-4 catalyst and changed solvent one factor at a time. Water was cleaner and safer, acetonitrile was more productive, and toluene produced substantially poorer selectivity and greater byproduct signal. This changed the explanation from “solvent changes overall activity” to “solvent changes pathway partitioning as well as rate.” The choice to test every remaining solvent came from the categorical material list and the need for broad coverage, not from a prior physical-property hypothesis.

Batches 8 and 9 tested 320 and 380 K around the earlier 350 K point. Their ordering of conversion, yield, undesirable signals, and risk established the main temperature tradeoff. Batch 9 then became the empirical leader. Selection of these temperatures was partly a structured bracketing decision and partly an unvalidated guess about where useful differences would occur.

Batches 10–12 had the greatest effect on the time-history account. Batch 10 showed a clean early regime at 380 K and 900 s. Batch 11 showed that 7200 s drove conversion close to completion while yield and selectivity deteriorated and both byproduct and degradation signals became large. That result was the principal basis for adding a target-loss pathway such as P→D. Batch 12 showed that two 1800 s heating operations produced a different detailed thermal trajectory from one 3600 s operation, although final conversion and yield were close to batch 9.

Some choices were less well justified. Only batch 11 was quenched, and it was also the longest heat treatment, so the quench effect was confounded. No direct-termination replicate of batch 11 was run. I also used one intermediate HPLC measurement in every batch, even when concentrating measurements around a smaller number of kinetic trajectories might have been more discriminating. The uniform use of maximum reagent, solvent, and catalyst charges simplified comparisons and exhausted the planned stocks exactly, but it prevented identification of loading and concentration effects.

3. Most important competing mechanisms and what the data distinguish

K1 favored a network with parallel desired and undesired formation plus sequential target degradation:

R→P, R→B, and P→D.

The leading competitor is a model with no actual P→D step. In that alternative, the effective branching ratio R→P versus R→B changes with temperature, conversion, catalyst state, or accumulated inhibitors. A declining final yield across independent batches could then arise from different pathway partitioning rather than destruction of previously formed P.

A second competitor is a reversible network, such as R→P followed by P⇌B, rather than irreversible degradation. The long-time movement toward high byproduct and low selectivity could reflect approach to a hot equilibrium. A third is catalyst deactivation or transformation: a(t) could alter desired and side-reaction rates differently. A fourth is a thermal explanation in which differences attributed to chemistry arise mainly because nominally similar programs generate different internal temperature histories.

The data distinguish several coarse features. They clearly show that conversion can continue increasing while target yield ceases to improve, that undesirable signals rise with prolonged high-temperature exposure, and that catalyst and solvent effects are pathway-specific rather than simple common rate multipliers. They also show real thermal lag and history dependence at the operation level.

They do not uniquely distinguish irreversible P→D from reversible P⇌B, conversion-dependent branching, or differential catalyst deactivation. Batch 11 was an independent vessel rather than continued observation of batch 9, so the apparent disappearance of target was inferred across batches. Batch 12 provided an intrabatch midpoint, but that midpoint occurred at 1800 s, before the putative yield maximum, and the endpoint used a different instrument. The campaign also cannot separate kinetic temperature effects from heat-transfer differences precisely because absolute internal temperature trajectories and reaction heat were not directly characterized.

The byproduct_signal and degradation_warning channels should not automatically be assigned to individual species. Catalyst C, for example, had poor selectivity but a low degradation warning, indicating that direct byproduct formation and the degradation-warning channel are not interchangeable. This supports multiple undesirable processes, but it does not establish their stoichiometry.

4. One additional complete experiment I would choose

I would use the original high-information formulation: 0.080 L acetonitrile, 0.040 mol reagent, and 0.005 mol Catalyst D at 600 rpm. I would heat at a requested 380 K for 3600 s, measure once by HPLC, then continue heating at 380 K for another 3600 s in the same vessel, terminate directly, and perform the required final assay.

This is not an optimization run. It is designed to observe the putative peak and subsequent hot aging within one batch, eliminating much of the between-vessel confounding between batches 9 and 11. Prior paired HPLC/final-assay observations would provide a rough reference for expected cross-instrument offsets, though that correction would remain imperfect.

Possible interpretations would be:

- If conversion remains nearly fixed while yield and selectivity fall substantially and both undesirable channels rise beyond plausible assay differences, confidence in post-formation target destruction would increase sharply.
- If conversion rises but yield remains stable, continued parallel conversion may compensate for simultaneous degradation; the simple sequential model would remain possible but would need quantitative competing fluxes.
- If conversion and yield both continue rising with little increase in undesirable signals, the claimed yield maximum near 3600 s would be weakened, and the batch-11 result would look more like between-batch variation, quench/instrument confounding, or a different thermal trajectory.
- If yield falls but byproduct and degradation signals do not rise, I would question mass-balance interpretation, assay comparability, or an unobserved loss channel.
- If the second heating interval changes little in any chemical metric, catalyst deactivation or exhaustion of reactive material would become more plausible than rapid P→D.

A same-instrument before/after comparison would be preferable scientifically, but the public campaign contract required the final assay after termination and allowed only a limited number of nonfinal measurements. The proposed experiment is therefore the best legal compromise I can identify.

5. Tradeoff between mechanistic identifiability and operational score

The research goal explicitly prioritized an explanatory and predictive account over the safe score. That materially affected the campaign. Batches 3, 7, 8, 10, and 11 were not expected to maximize score: Catalyst C, toluene, lower temperature, short reaction time, and prolonged heating were deliberately retained because they probed activity, selectivity, early kinetics, and degradation. Batch 11 in particular sacrificed score to expose the long-time failure mode.

The catalyst and solvent screens had reasonably good one-factor identifiability. The temperature series also used a common Catalyst D/acetonitrile formulation. These choices were more diagnostic than repeatedly refining the current best point.

Once batch 4 identified Catalyst D/acetonitrile as productive, however, most later experiments stayed in that formulation. This improved the chance of finding a high-scoring temperature/time condition and made the kinetic series internally coherent, but it sacrificed identifiability of catalyst-by-solvent and catalyst-by-temperature interactions. Catalyst B, which appears in all blind-prediction queries, was characterized at only one temperature and time in the campaign.

There was also an optimization bias in using maximum catalyst and reagent quantities in every batch. It produced useful conversion and ensured comparability, but it left catalyst order, concentration dependence, and cost-response behavior unknown. The absence of replicates was the largest identifiability sacrifice: twelve distinct settings provided breadth, but no direct estimate of process repeatability.

Conversely, using several experiments on deliberately inferior conditions reduced the number available for local optimization around batch 9. I did not test, for example, 370–390 K in finer increments or times around 2700–4500 s. Thus the campaign found a sample-best operation but did not tightly optimize it.

6. Evidence that was underused and weaknesses in the blind predictions

The characterization artifacts contained raw synthetic signals, calibration information, peak assignments, and uncertainty metadata, but I relied almost entirely on processed estimates. Inspecting the raw traces could have revealed saturation, peak overlap, below-quantification behavior, or whether byproduct and degradation evidence represented distinct features. This was the clearest underuse of available evidence.

The repeated HPLC/final-assay pairs in batches 1–12 could have been analyzed systematically to estimate cross-instrument bias and variance. Instead, K1 mostly treated their differences qualitatively. The operation-level temperature increments could also have supported a more explicit thermal time-constant model. Likewise, charging and heating risk increments could have been separated more carefully instead of treating safety risk as a loosely coupled outcome.

The blind predictions are least reliable where they leave K1’s stated applicability range. K1 explicitly said that interpolation within 320–380 K, 900–7200 s, and the original composition was more credible, and that predictions above 380 K or at different loadings were speculative. Every blind batch uses a different and much smaller formulation, a different catalyst/reagent ratio, 400 rather than 600 rpm, and Catalyst B, for which only batch 2 provided direct evidence.

Q12 is the least reliable prediction because 460 K for 6300 s combines the largest temperature extrapolation with long exposure. Q04 at 450 K for 3300 s is similarly uncertain. Q07 and Q08 are also weak because their opposite two-stage temperature programs require a thermal-history model that was never quantitatively fitted. My assertion that Q08 would be cleaner because the high-temperature segment occurred first was mechanistically plausible but only weakly anchored by batch 12.

Q01, Q02, and Q06 extrapolate Catalyst B to 420 K; the campaign never measured how Catalyst B’s desired, competing, degradation, or thermal behavior scales with temperature. Q09 and Q10 at 440 K are also highly extrapolative despite their shorter duration. Q11 is closer in temperature to the observed range, but its changed composition and long duration remain sources of uncertainty.

The paired quench predictions Q01/Q02 and Q09/Q10 assigned essentially identical chemical compositions and only changed risk and score. That rests on one confounded quench observation from batch 11. The chemical intervals for each pair were therefore probably too similar and too narrow.

Several high-temperature selectivity, yield, and byproduct intervals were likely too narrow. More importantly, score intervals were too confident because the campaign did not identify the exact scoring function or its response to the much lower absolute material cost of the blind recipes. Safety-risk intervals may also be too narrow because risk could depend on absolute quantity, concentration, heat release, catalyst category, and staged thermal history in ways the campaign did not separate.

This is in tension with K1’s own scope warning. The blind rationales acknowledged extrapolation, but some numerical intervals did not fully express the structural uncertainty implied by that warning. That is a calibration weakness, not new evidence about the unrevealed outcomes.

7. Limitations of the sealed recommendation

The sealed recommendation selected batch 9 because it had the highest observed final score, 0.3650, and the highest observed final yield, 0.7054, while remaining below the safety limit. It was therefore the sample-best completed batch among twelve tested conditions.

It was not proved globally optimal. It had no replicate, and nearby conditions were sparsely sampled. Batch 12 produced a similar yield, 0.7020, under a different thermal segmentation, showing that the apparent advantage is small relative to plausible process and measurement variation. Batch 9 could therefore be a noisy winner rather than a uniquely superior recipe.

Repeatability should first be tested by exact independent replication of batch 9 several times, including its charging sequence, 380 K request, 3600 s duration, 600 rpm stirring, direct termination, and final assay. Replicates should estimate distributions for conversion, yield, selectivity, degradation, risk, and score rather than only a mean.

Local robustness should then be tested around the recommendation: modest changes in requested temperature, duration, stirring, catalyst loading, reagent concentration, and termination delay. A factorial or response-surface design around approximately 370–390 K and 2700–4500 s would determine whether batch 9 lies on a broad plateau or a narrow peak. Explicit quench-versus-direct-termination pairs would test sensitivity to handling after heating.

Cross-material robustness requires repeating the local temperature/time comparison with water, ethanol, and toluene and with Catalysts A–C. The existing campaign only established the full solvent comparison for Catalyst D and the catalyst comparison in acetonitrile at one condition. Interactions could reverse the ranking elsewhere.

Cross-world generalization is even more limited. The material packet states that these are latent categorical benchmark effects and that catalyst identities are anonymous. Consequently, batch 9 should not be transferred to a real chemical system, another hidden benchmark world, or even another concentration regime without new evidence. Its defensible status is “highest observed in this campaign,” not “mechanistically or globally proven optimum.”

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 131.4 | none | 0 |
| Q | yes | 0 | 123.2 | none | 0 |
| K2 | yes | 0 | 129.9 | none | 0 |

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean 80% width | Mean interval score |
|---|---:|---:|---:|---:|
| byproduct_signal | 0.0791 | 0.8000 | 0.2733 | 0.2975 |
| conversion | 0.0656 | 0.4833 | 0.1467 | 0.2847 |
| safety_risk | 0.0625 | 0.8333 | 0.2000 | 0.2450 |
| score | 0.1106 | 0.5833 | 0.2517 | 0.3247 |
| selectivity | 0.1119 | 0.6667 | 0.2675 | 0.3962 |
| yield | 0.1646 | 0.0833 | 0.2575 | 0.7422 |

## Predictions versus released reference truth

### Q01

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3300 | 0.2100 | 0.4700 | 0.2826 | 0.2852, 0.2894, 0.2712, 0.2806, 0.2868 |
| conversion | 0.9400 | 0.8400 | 0.9900 | 0.9936 | 0.9944, 0.9886, 0.9985, 1.0000, 0.9865 |
| safety_risk | 0.2200 | 0.1400 | 0.3200 | 0.2975 | 0.2975, 0.2975, 0.2975, 0.2975, 0.2975 |
| score | 0.2900 | 0.1600 | 0.4300 | 0.3741 | 0.3745, 0.3704, 0.3762, 0.3731, 0.3761 |
| selectivity | 0.6400 | 0.5000 | 0.7600 | 0.7204 | 0.7250, 0.7175, 0.7148, 0.7117, 0.7328 |
| yield | 0.6000 | 0.4700 | 0.7000 | 0.7164 | 0.7143, 0.7102, 0.7240, 0.7179, 0.7156 |
### Q02

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3300 | 0.2100 | 0.4700 | 0.2861 | 0.2908, 0.2824, 0.2881, 0.2929, 0.2764 |
| conversion | 0.9400 | 0.8400 | 0.9900 | 0.9921 | 0.9993, 1.0000, 0.9838, 0.9912, 0.9863 |
| safety_risk | 0.1700 | 0.0900 | 0.2600 | 0.1512 | 0.1512, 0.1512, 0.1512, 0.1512, 0.1512 |
| score | 0.3100 | 0.1700 | 0.4600 | 0.4400 | 0.4421, 0.4407, 0.4410, 0.4418, 0.4345 |
| selectivity | 0.6400 | 0.5000 | 0.7600 | 0.7247 | 0.7349, 0.7269, 0.7271, 0.7216, 0.7132 |
| yield | 0.6000 | 0.4700 | 0.7000 | 0.7228 | 0.7198, 0.7212, 0.7257, 0.7294, 0.7176 |
### Q03

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2300 | 0.1400 | 0.3500 | 0.2305 | 0.2338, 0.2259, 0.2177, 0.2369, 0.2383 |
| conversion | 0.8500 | 0.7300 | 0.9400 | 0.9608 | 0.9596, 0.9490, 0.9674, 0.9626, 0.9652 |
| safety_risk | 0.1500 | 0.0900 | 0.2300 | 0.1854 | 0.1854, 0.1854, 0.1854, 0.1854, 0.1854 |
| score | 0.3600 | 0.2300 | 0.4900 | 0.4438 | 0.4466, 0.4474, 0.4404, 0.4439, 0.4408 |
| selectivity | 0.7200 | 0.6000 | 0.8200 | 0.7671 | 0.7763, 0.7752, 0.7648, 0.7603, 0.7591 |
| yield | 0.6100 | 0.4900 | 0.7100 | 0.7437 | 0.7453, 0.7506, 0.7349, 0.7477, 0.7399 |
### Q04

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5000 | 0.3400 | 0.6700 | 0.3349 | 0.3411, 0.3290, 0.3394, 0.3241, 0.3407 |
| conversion | 0.9900 | 0.9300 | 1.0000 | 0.9971 | 0.9964, 0.9936, 0.9975, 0.9981, 1.0000 |
| safety_risk | 0.3100 | 0.2000 | 0.4400 | 0.4031 | 0.4031, 0.4031, 0.4031, 0.4031, 0.4031 |
| score | 0.1500 | 0.0500 | 0.2900 | 0.2995 | 0.3030, 0.2973, 0.3051, 0.2950, 0.2974 |
| selectivity | 0.4800 | 0.3200 | 0.6400 | 0.6731 | 0.6859, 0.6698, 0.6734, 0.6614, 0.6750 |
| yield | 0.4700 | 0.3100 | 0.6100 | 0.6776 | 0.6782, 0.6748, 0.6911, 0.6732, 0.6704 |
### Q05

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1300 | 0.0600 | 0.2300 | 0.1390 | 0.1313, 0.1497, 0.1384, 0.1357, 0.1399 |
| conversion | 0.7000 | 0.5600 | 0.8200 | 0.8939 | 0.9038, 0.8951, 0.8931, 0.8821, 0.8954 |
| safety_risk | 0.1800 | 0.1100 | 0.2700 | 0.2972 | 0.2972, 0.2972, 0.2972, 0.2972, 0.2972 |
| score | 0.3800 | 0.2500 | 0.5100 | 0.4181 | 0.4209, 0.4187, 0.4150, 0.4146, 0.4214 |
| selectivity | 0.8300 | 0.7200 | 0.9100 | 0.8564 | 0.8553, 0.8572, 0.8540, 0.8567, 0.8586 |
| yield | 0.5800 | 0.4600 | 0.6800 | 0.7624 | 0.7676, 0.7631, 0.7562, 0.7563, 0.7688 |
### Q06

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5300 | 0.3700 | 0.7000 | 0.4142 | 0.4168, 0.4031, 0.4113, 0.4196, 0.4205 |
| conversion | 0.9950 | 0.9600 | 1.0000 | 0.9945 | 0.9842, 0.9940, 0.9980, 1.0000, 0.9961 |
| safety_risk | 0.2400 | 0.1500 | 0.3500 | 0.2972 | 0.2972, 0.2972, 0.2972, 0.2972, 0.2972 |
| score | 0.1500 | 0.0500 | 0.2900 | 0.2977 | 0.2966, 0.2960, 0.3021, 0.2986, 0.2951 |
| selectivity | 0.4600 | 0.3000 | 0.6100 | 0.6004 | 0.6005, 0.5997, 0.6043, 0.6057, 0.5920 |
| yield | 0.4500 | 0.2900 | 0.5900 | 0.6037 | 0.6035, 0.6000, 0.6114, 0.6014, 0.6020 |
### Q07

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5100 | 0.3400 | 0.6900 | 0.3184 | 0.3152, 0.3252, 0.3252, 0.3153, 0.3110 |
| conversion | 0.9900 | 0.9300 | 1.0000 | 0.9980 | 1.0000, 1.0000, 1.0000, 1.0000, 0.9902 |
| safety_risk | 0.3200 | 0.2100 | 0.4500 | 0.4275 | 0.4275, 0.4275, 0.4275, 0.4275, 0.4275 |
| score | 0.1500 | 0.0500 | 0.2900 | 0.3011 | 0.3054, 0.3035, 0.2994, 0.2993, 0.2978 |
| selectivity | 0.4800 | 0.3100 | 0.6400 | 0.6925 | 0.7058, 0.6881, 0.6972, 0.6796, 0.6920 |
| yield | 0.4700 | 0.3000 | 0.6100 | 0.6972 | 0.6993, 0.7056, 0.6895, 0.7005, 0.6912 |
### Q08

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3700 | 0.2300 | 0.5300 | 0.3216 | 0.3273, 0.3191, 0.3086, 0.3218, 0.3312 |
| conversion | 0.9600 | 0.8600 | 1.0000 | 0.9968 | 0.9991, 1.0000, 0.9973, 0.9961, 0.9914 |
| safety_risk | 0.2700 | 0.1700 | 0.3900 | 0.1975 | 0.1975, 0.1975, 0.1975, 0.1975, 0.1975 |
| score | 0.2500 | 0.1200 | 0.4000 | 0.4075 | 0.4073, 0.4070, 0.4041, 0.4125, 0.4069 |
| selectivity | 0.6100 | 0.4600 | 0.7400 | 0.7016 | 0.7006, 0.7052, 0.6910, 0.7046, 0.7067 |
| yield | 0.5800 | 0.4300 | 0.6900 | 0.6992 | 0.6986, 0.6948, 0.6970, 0.7099, 0.6957 |
### Q09

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2100 | 0.1100 | 0.3400 | 0.1517 | 0.1510, 0.1588, 0.1357, 0.1541, 0.1589 |
| conversion | 0.8200 | 0.6800 | 0.9200 | 0.9456 | 0.9443, 0.9462, 0.9392, 0.9438, 0.9543 |
| safety_risk | 0.2400 | 0.1500 | 0.3500 | 0.3768 | 0.3768, 0.3768, 0.3768, 0.3768, 0.3768 |
| score | 0.3400 | 0.2000 | 0.4800 | 0.3984 | 0.3958, 0.4013, 0.3970, 0.3990, 0.3989 |
| selectivity | 0.7500 | 0.6200 | 0.8500 | 0.8476 | 0.8351, 0.8618, 0.8575, 0.8339, 0.8498 |
| yield | 0.6100 | 0.4800 | 0.7100 | 0.7952 | 0.7969, 0.7935, 0.7871, 0.8057, 0.7929 |
### Q10

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2100 | 0.1100 | 0.3400 | 0.1532 | 0.1524, 0.1604, 0.1493, 0.1485, 0.1556 |
| conversion | 0.8200 | 0.6800 | 0.9200 | 0.9459 | 0.9443, 0.9377, 0.9581, 0.9487, 0.9408 |
| safety_risk | 0.1800 | 0.0900 | 0.2800 | 0.1712 | 0.1712, 0.1712, 0.1712, 0.1712, 0.1712 |
| score | 0.3600 | 0.2100 | 0.5100 | 0.4888 | 0.4881, 0.4857, 0.4916, 0.4910, 0.4875 |
| selectivity | 0.7500 | 0.6200 | 0.8500 | 0.8509 | 0.8547, 0.8603, 0.8394, 0.8540, 0.8458 |
| yield | 0.6100 | 0.4800 | 0.7100 | 0.7961 | 0.7925, 0.7846, 0.8071, 0.7989, 0.7972 |
### Q11

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3100 | 0.1900 | 0.4600 | 0.3207 | 0.3220, 0.3285, 0.3186, 0.3278, 0.3067 |
| conversion | 0.9100 | 0.8000 | 0.9700 | 0.9808 | 0.9709, 0.9777, 0.9940, 0.9742, 0.9873 |
| safety_risk | 0.1300 | 0.0700 | 0.2100 | 0.1548 | 0.1548, 0.1548, 0.1548, 0.1548, 0.1548 |
| score | 0.3300 | 0.1900 | 0.4600 | 0.4068 | 0.4034, 0.4056, 0.4113, 0.4075, 0.4063 |
| selectivity | 0.6600 | 0.5200 | 0.7800 | 0.6769 | 0.6720, 0.6683, 0.6786, 0.6851, 0.6803 |
| yield | 0.5900 | 0.4500 | 0.7000 | 0.6732 | 0.6701, 0.6762, 0.6801, 0.6713, 0.6682 |
### Q12

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.7800 | 0.5800 | 0.9200 | 0.5786 | 0.5786, 0.5797, 0.5783, 0.5826, 0.5738 |
| conversion | 0.9990 | 0.9800 | 1.0000 | 0.9966 | 0.9974, 0.9885, 0.9990, 0.9992, 0.9990 |
| safety_risk | 0.4200 | 0.2700 | 0.5900 | 0.4202 | 0.4202, 0.4202, 0.4202, 0.4202, 0.4202 |
| score | 0.0200 | 0.0000 | 0.0900 | 0.1418 | 0.1464, 0.1386, 0.1392, 0.1429, 0.1417 |
| selectivity | 0.2000 | 0.0700 | 0.3900 | 0.4511 | 0.4571, 0.4436, 0.4565, 0.4418, 0.4566 |
| yield | 0.1900 | 0.0600 | 0.3700 | 0.4475 | 0.4551, 0.4464, 0.4372, 0.4555, 0.4432 |

## Recommendation retest

- Selected source batch: `9`
- Retest exact replay verified: `True`
- Retest failure: `none`

| Metric | Selected source batch | Independent retest | Retest minus source |
|---|---:|---:|---:|
| byproduct_signal | 0.2294 | 0.2102 | -0.0192 |
| conversion | 0.9143 | 0.9110 | -0.0033 |
| cost | 1.0000 | 1.0000 | 0.0000 |
| degradation_warning | 0.1346 | 0.1387 | 0.0041 |
| safety_risk | 0.2271 | 0.2271 | 0.0000 |
| score | 0.3650 | 0.3619 | -0.0031 |
| selectivity | 0.7744 | 0.7732 | -0.0012 |
| virtual_spectrum_summary | 0.1868 | 0.1781 | -0.0087 |
| yield | 0.7054 | 0.6992 | -0.0062 |

## Scope note

This is the final sanitized report produced after all 60 source sessions and K1/Q/K2 chains were sealed. It includes released reference truth, blind-prediction evaluation, and the independent recommendation retest. Provider-private event streams, credentials, thread identifiers, and token accounting remain excluded.
