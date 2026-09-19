# RX-W05--S--mechanism_discovery--MisIndexed

## Run summary

- World: `RX-W05`
- Locus: `S`
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

- Effective result location: `source-repair-v11`
- Recovery version: `recovery-v11-parallel4-transport-repair`
- Repaired stages: `source`
- Source experiments rerun: `False`
- Original source thread reused: `False`
- Truth revealed during recovery: `False`

## Sealed recommendation

- Selected batch: `12`
- Rationale: Batch 12 gave the best observed safe score and preserved the high target yield of the 360 K condition while prompt quenching reduced risk and limited continued competing conversion.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S2 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 340 K x 3600 s @ 600 rpm | no | 0.4172 | 0.7725 | 0.5165 | 0.1117 | 0.0245 | 0.1634 | 0.2382 |
| 2 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 340 K x 3600 s @ 600 rpm | no | 0.4867 | 0.7880 | 0.6275 | 0.1525 | 0.0412 | 0.1746 | 0.2759 |
| 3 | S2 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 340 K x 3600 s @ 600 rpm | no | 0.2961 | 0.6423 | 0.4343 | 0.1658 | 0.0266 | 0.1532 | 0.1535 |
| 4 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 340 K x 3600 s @ 600 rpm | no | 0.5618 | 0.8197 | 0.6840 | 0.1164 | 0.0733 | 0.1823 | 0.3160 |
| 5 | S0 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 340 K x 3600 s @ 600 rpm | no | 0.4677 | 0.8442 | 0.5555 | 0.0963 | 0.0340 | 0.1292 | 0.2955 |
| 6 | S1 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 340 K x 3600 s @ 600 rpm | no | 0.4716 | 0.8045 | 0.5848 | 0.1267 | 0.0546 | 0.1538 | 0.2790 |
| 7 | S3 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 340 K x 3600 s @ 600 rpm | no | 0.3981 | 0.6756 | 0.5801 | 0.1969 | 0.0737 | 0.1806 | 0.2049 |
| 8 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 320 K x 3600 s @ 600 rpm | no | 0.4267 | 0.8259 | 0.5178 | 0.1037 | 0.0412 | 0.1641 | 0.2551 |
| 9 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 360 K x 3600 s @ 600 rpm | no | 0.6437 | 0.7897 | 0.7974 | 0.1805 | 0.1054 | 0.2008 | 0.3443 |
| 10 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 340 K x 900 s @ 600 rpm | no | 0.2070 | 0.8872 | 0.2418 | 0.0305 | 0.0094 | 0.1405 | 0.1655 |
| 11 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 340 K x 7200 s @ 600 rpm | no | 0.6285 | 0.6988 | 0.9081 | 0.2848 | 0.2006 | 0.1993 | 0.3272 |
| 12 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 360 K x 3600 s @ 600 rpm | yes | 0.6442 | 0.7967 | 0.8277 | 0.1661 | 0.1079 | 0.1908 | 0.3537 |

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
      "target_temperature_K": 340
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
    "byproduct_signal": 0.11166086047887802,
    "conversion": 0.5164546966552734,
    "cost": 1.0,
    "degradation_warning": 0.024487420916557312,
    "safety_risk": 0.16337274014949799,
    "score": 0.238163024187088,
    "selectivity": 0.772541344165802,
    "virtual_spectrum_summary": 0.07243280857801437,
    "yield": 0.4172499179840088
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
      "target_temperature_K": 340
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
    "byproduct_signal": 0.15247073769569397,
    "conversion": 0.6275460720062256,
    "cost": 1.0,
    "degradation_warning": 0.04121781513094902,
    "safety_risk": 0.17456720769405365,
    "score": 0.27589747309684753,
    "selectivity": 0.7879949808120728,
    "virtual_spectrum_summary": 0.10240692645311356,
    "yield": 0.4867483973503113
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
      "target_temperature_K": 340
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
    "byproduct_signal": 0.1658138781785965,
    "conversion": 0.4343256652355194,
    "cost": 1.0,
    "degradation_warning": 0.026638256385922432,
    "safety_risk": 0.1531612128019333,
    "score": 0.153520867228508,
    "selectivity": 0.6423134803771973,
    "virtual_spectrum_summary": 0.10318484902381897,
    "yield": 0.29608121514320374
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
      "target_temperature_K": 340
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
    "byproduct_signal": 0.1164437085390091,
    "conversion": 0.6840150952339172,
    "cost": 1.0,
    "degradation_warning": 0.07331623136997223,
    "safety_risk": 0.18228019773960114,
    "score": 0.3160233795642853,
    "selectivity": 0.8196679949760437,
    "virtual_spectrum_summary": 0.09703633934259415,
    "yield": 0.5618273615837097
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
      "target_temperature_K": 340
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
    "byproduct_signal": 0.09633932262659073,
    "conversion": 0.5555161833763123,
    "cost": 1.0,
    "degradation_warning": 0.03399549052119255,
    "safety_risk": 0.12917596101760864,
    "score": 0.29553693532943726,
    "selectivity": 0.8441853523254395,
    "virtual_spectrum_summary": 0.06828460097312927,
    "yield": 0.46767038106918335
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
      "target_temperature_K": 340
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
    "byproduct_signal": 0.12674489617347717,
    "conversion": 0.5847806334495544,
    "cost": 1.0,
    "degradation_warning": 0.054619964212179184,
    "safety_risk": 0.15382419526576996,
    "score": 0.27900606393814087,
    "selectivity": 0.8044649362564087,
    "virtual_spectrum_summary": 0.09428867697715759,
    "yield": 0.4715816378593445
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
      "target_temperature_K": 340
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
    "byproduct_signal": 0.19685816764831543,
    "conversion": 0.5800691843032837,
    "cost": 1.0,
    "degradation_warning": 0.07371652126312256,
    "safety_risk": 0.18059197068214417,
    "score": 0.20488344132900238,
    "selectivity": 0.6756014823913574,
    "virtual_spectrum_summary": 0.14144442975521088,
    "yield": 0.3981063663959503
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
    "byproduct_signal": 0.10374019294977188,
    "conversion": 0.5177952647209167,
    "cost": 1.0,
    "degradation_warning": 0.04123827442526817,
    "safety_risk": 0.16405753791332245,
    "score": 0.25511693954467773,
    "selectivity": 0.8258580565452576,
    "virtual_spectrum_summary": 0.075614333152771,
    "yield": 0.4267469644546509
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
      "target_temperature_K": 360
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
    "byproduct_signal": 0.18050681054592133,
    "conversion": 0.7973911166191101,
    "cost": 1.0,
    "degradation_warning": 0.10543311387300491,
    "safety_risk": 0.20079894363880157,
    "score": 0.3442898690700531,
    "selectivity": 0.7896597981452942,
    "virtual_spectrum_summary": 0.1467236429452896,
    "yield": 0.643738329410553
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
      "target_temperature_K": 340
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
    "byproduct_signal": 0.030505791306495667,
    "conversion": 0.2417922168970108,
    "cost": 1.0,
    "degradation_warning": 0.009375139139592648,
    "safety_risk": 0.14049771428108215,
    "score": 0.16553866863250732,
    "selectivity": 0.8871626853942871,
    "virtual_spectrum_summary": 0.020996997132897377,
    "yield": 0.2069818675518036
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
      "target_temperature_K": 340
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
    "byproduct_signal": 0.284840852022171,
    "conversion": 0.9081088900566101,
    "cost": 1.0,
    "degradation_warning": 0.20056390762329102,
    "safety_risk": 0.19934792816638947,
    "score": 0.327187180519104,
    "selectivity": 0.698797345161438,
    "virtual_spectrum_summary": 0.24691621959209442,
    "yield": 0.6284588575363159
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
      "target_temperature_K": 360
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
    "byproduct_signal": 0.16613949835300446,
    "conversion": 0.8277427554130554,
    "cost": 1.0,
    "degradation_warning": 0.10786562412977219,
    "safety_risk": 0.19084054231643677,
    "score": 0.35374438762664795,
    "selectivity": 0.7966945171356201,
    "virtual_spectrum_summary": 0.13991625607013702,
    "yield": 0.644186794757843
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

1. Scope and experimental basis

I completed 12 batches using the same nominal charge in every vessel: 0.040 mol limiting reagent, 0.080 L solvent, and 0.005 mol catalyst, corresponding approximately to 0.50 M reagent and 0.0625 M catalyst before analytical sampling. Heating used 600 rpm stirring. Consequently, the campaign identifies effects of catalyst identity, solvent identity, temperature, time, and quenching at one loading regime; it does not identify concentration or catalyst-order effects.

The reported yields, conversions, selectivities, byproduct signals, and degradation warnings are synthetic instrument observables rather than direct hidden-species inventories. Final-assay values are the principal basis of the comparisons below. HPLC values are useful as intermediate observations, but small HPLC/final-assay differences should not automatically be interpreted as chemical changes because the two instruments have different noise and calibration models.

2. Main observations

Catalyst screen in acetonitrile, nominally 340 K for 3600 s:

- Batch 1, Catalyst A: conversion 0.5165, yield 0.4172, selectivity 0.7725, byproduct signal 0.1117, degradation warning 0.0245, safety risk 0.1634.
- Batch 2, Catalyst B: conversion 0.6275, yield 0.4867, selectivity 0.7880, byproduct signal 0.1525, degradation warning 0.0412, risk 0.1746.
- Batch 3, Catalyst C: conversion 0.4343, yield 0.2961, selectivity 0.6423, byproduct signal 0.1658, degradation warning 0.0266, risk 0.1532.
- Batch 4, Catalyst D: conversion 0.6840, yield 0.5618, selectivity 0.8197, byproduct signal 0.1164, degradation warning 0.0733, risk 0.1823.

Catalyst D therefore increased both total conversion and useful target formation relative to the other catalysts under this condition. Catalyst identity did not merely rescale one common reaction rate: Catalyst C had both low conversion and poor selectivity, while Catalyst B had appreciable conversion but a relatively high byproduct signal. Catalyst D also produced more degradation warning than A-C, suggesting that its activity accelerates desired formation but does not exclusively accelerate that pathway.

Solvent screen with Catalyst D, nominally 340 K for 3600 s:

- Batch 5, water: conversion 0.5555, yield 0.4677, selectivity 0.8442, byproduct 0.0963, degradation 0.0340, risk 0.1292.
- Batch 6, ethanol: conversion 0.5848, yield 0.4716, selectivity 0.8045, byproduct 0.1267, degradation 0.0546, risk 0.1538.
- Batch 4, acetonitrile: conversion 0.6840, yield 0.5618, selectivity 0.8197, byproduct 0.1164, degradation 0.0733, risk 0.1823.
- Batch 7, toluene: conversion 0.5801, yield 0.3981, selectivity 0.6756, byproduct 0.1969, degradation 0.0737, risk 0.1806.

Thus solvent changes both rate and branching. Acetonitrile gave the greatest target yield and conversion. Water gave the best selectivity, lowest byproduct signal, and lowest safety risk, but slower conversion. Toluene was especially unfavorable for product partitioning: conversion was similar to ethanol, yet target yield and selectivity were much lower and byproduct signal was much higher. These results cannot be explained by a solvent-dependent rate multiplier alone.

Time series with Catalyst D in acetonitrile near 340 K:

- Batch 10, 900 s: actual final temperature about 340.17 K; conversion 0.2418, yield 0.2070, selectivity 0.8872, byproduct 0.0305, degradation 0.0094, risk 0.1405.
- Batch 4, 3600 s: actual final temperature about 340.14 K; conversion 0.6840, yield 0.5618, selectivity 0.8197, byproduct 0.1164, degradation 0.0733, risk 0.1823.
- Batch 11, 7200 s: actual final temperature about 340.10 K; conversion 0.9081, yield 0.6285, selectivity 0.6988, byproduct 0.2848, degradation 0.2006, risk 0.1993.

Conversion continued to rise throughout the measured interval, but target yield showed diminishing returns and selectivity deteriorated substantially. The extra hour from 3600 to 7200 s increased conversion by about 0.224 but yield by only about 0.067, while byproduct and degradation signals rose sharply. This is strong evidence that prolonged reaction does not simply convert remaining reagent into target. Competing conversion and/or secondary loss increasingly dominate late in the batch.

Temperature series with Catalyst D in acetonitrile for 3600 s:

- Batch 8, requested 320 K, actual final temperature about 321.45 K: conversion 0.5178, yield 0.4267, selectivity 0.8259, byproduct 0.1037, degradation 0.0412, risk 0.1641.
- Batch 4, requested 340 K, actual about 340.14 K: conversion 0.6840, yield 0.5618, selectivity 0.8197, byproduct 0.1164, degradation 0.0733, risk 0.1823.
- Batch 9, requested 360 K, actual about 358.02 K: conversion 0.7974, yield 0.6437, selectivity 0.7897, byproduct 0.1805, degradation 0.1054, risk 0.2008.

Higher temperature accelerated conversion and increased the one-hour target yield, but selectivity decreased and both byproduct and degradation signals increased. The requested temperature should not be treated as the actual thermal state: the 360 K experiment ended near 358.0 K, whereas the 320 K experiment slightly overshot to about 321.5 K. A predictive model should use actual temperature history when available, not just the controller set point.

Quench comparison:

Batches 9 and 12 used Catalyst D in acetonitrile with the same nominal 360 K, 3600 s heat treatment and reached the same reported pre-quench temperature, about 358.02 K. Batch 9 was terminated without an explicit quench. Batch 12 was quenched, producing a reported temperature change of -45 K, then analyzed and terminated.

Final assay results were:

- Batch 9, no explicit quench: conversion 0.7974, yield 0.6437, selectivity 0.7897, byproduct 0.1805, degradation 0.1054, risk 0.2008.
- Batch 12, prompt quench: conversion 0.8277, yield 0.6442, selectivity 0.7967, byproduct 0.1661, degradation 0.1079, risk 0.1908.

The target yields were essentially identical. The quenched batch had modestly higher conversion and selectivity, lower byproduct signal and risk, and nearly unchanged degradation warning. With only one matched pair, these differences cannot uniquely establish a quench mechanism. The defensible conclusion is that prompt quenching preserved the high target yield while lowering thermal risk; it may also have allowed some residual conversion during cooling while suppressing later hot competing chemistry. Batch 12 had the best observed safe score, 0.3537, and was therefore the sealed recommendation.

3. Proposed reaction network

The smallest network consistent with the data is a desired pathway in parallel with competing conversion, plus secondary target loss:

R -> P        rate kP R
R -> B        rate kB R
P -> D        rate kD P
P -> R        possible reverse rate kminus P

Here R is the public reactant, P the target, B a primary competing product or product family, and D a degradation product or family. A useful working set of equations is:

dR/dt = -(kP + kB) R + kminus P

dP/dt = kP R - (kD + kminus) P

dB/dt = kB R

dD/dt = kD P

The measured conversion is approximately 1 - R/R0. Yield is approximately P/R0, while measured selectivity, byproduct signal, and degradation warning are noisy calibrated proxies rather than exact stoichiometric fractions. Therefore, these equations should be fitted to latent species and linked to observations through separate calibration functions; exact identities such as yield = conversion times reported selectivity should not be imposed without allowing measurement error and proxy mismatch.

Catalyst and solvent should enter as separate modifiers of the individual rate constants, not as one common activity factor. One possible parameterization is:

ki(T,catalyst,solvent) = Ai * fcatalyst,i * fsolvent,i * exp(-Ei/(Rgas T))

for i in {P, B, D, minus}. The data specifically require pathway-dependent factors: water appears to reduce the total rate while favoring P over B, whereas toluene strongly favors competing conversion. Catalyst D increases the desired rate but also raises secondary-degradation evidence.

4. Approximate conversion kinetics

Ignoring reversal for the limited purpose of summarizing total disappearance of reactant, the Catalyst D/acetonitrile conversion data are surprisingly consistent with pseudo-first-order behavior:

X(t) = 1 - exp(-kobs t).

At about 340 K, final-assay conversions from batches 10, 4, and 11 give individual kobs estimates of approximately 3.08e-4, 3.20e-4, and 3.32e-4 s^-1, respectively. Their mean is about 3.20e-4 s^-1. The small upward trend is not evidence of deactivation; within the limited data it suggests that strong catalyst deactivation is unnecessary to explain total conversion. Any deactivation that exists is confounded with thermal transients, measurement noise, and reversible or secondary chemistry.

Using the 3600 s final conversions at actual endpoint temperatures of 321.45, 340.14, and 358.02 K gives approximate kobs values of 2.03e-4, 3.20e-4, and 4.44e-4 s^-1. A three-point Arrhenius regression gives:

ln(kobs/s^-1) approximately -0.807 - 2471/T,

corresponding to an apparent activation energy of about 20.5 kJ mol^-1. This is an empirical local descriptor, not a uniquely identified elementary activation barrier. It folds together catalyst activity, thermal history, parallel channels, possible reversibility, and the conversion observation model. It should only be used near the tested 321-358 K range, at the tested composition and Catalyst D/acetonitrile formulation.

A single first-order equation describes total conversion much better than it describes target yield. For prediction of P, the parallel/secondary network is necessary. Increasing time from 3600 to 7200 s at 340 K produced considerably less additional P than expected if every newly converted unit became target, while B and D signals increased. Likewise, temperature accelerated undesirable signals along with target formation.

5. Thermal and safety coupling

The reactor has finite thermal response: actual temperature approached but did not always equal the set point. Chemistry and risk should therefore be integrated over actual temperature:

for each small interval dt:
  update T from the vessel/controller thermal response;
  calculate kP, kB, kD, and possibly kminus at T;
  integrate R, P, B, and D;
  accumulate a thermal/material risk rate;
  if quenched, rapidly lower T and reduce all temperature-dependent rates.

Observed safety risk increased with hotter or longer processing and depended strongly on solvent and catalyst. For example, with Catalyst D at 340 K and 3600 s, water gave risk 0.1292 versus 0.1823 for acetonitrile. In acetonitrile, shortening the run to 900 s reduced risk to 0.1405, while 7200 s raised it to 0.1993. Heating near 358 K for 3600 s gave risk 0.2008 without explicit quench and 0.1908 with quench. All completed batches remained below the stated 0.35 safety limit.

The visible cost reached its capped value of 1.0 after catalyst charging in these experiments, so it provided little mechanistic information. The reaction score was treated only as a secondary operational metric and was not used as a substitute for chemical observables.

6. How the explanation changed during the campaign

The initial structural prior allowed an appreciable reverse target channel. Batch 1 established that meaningful target formation and competing conversion occurred under moderate heating. The catalyst screen then showed that catalyst identity changes both conversion and branching, leading me away from a one-rate description. Catalyst D was selected for mechanistic studies because it gave the highest conversion and target yield.

The solvent screen further rejected a single catalyst-activity explanation: water improved selectivity despite lowering conversion, and toluene produced much more competing product at similar conversion to ethanol. This motivated pathway-specific catalyst and solvent factors.

The 900/3600/7200 s series showed nearly pseudo-first-order total conversion but progressive selectivity loss and strong growth of byproduct and degradation signals. I therefore added secondary target loss or late competing chemistry to the model. Strong catalyst deactivation was not needed to explain total conversion over this interval.

The temperature series supported thermally activated conversion and showed that undesirable channels also accelerate with temperature. The matched quench comparison showed that fast cooling can preserve the high-temperature target yield and reduce risk, but it did not uniquely distinguish arrest of degradation from continued conversion during cooling.

The original reverse-channel hypothesis remains possible but was not decisively demonstrated. No experiment began with isolated target, and no deliberate hot-to-cold hold was conducted while tracking target and reactant with the same instrument. The decline from the batch-9 HPLC yield of 0.6765 before termination to final-assay yield 0.6437 could reflect real target loss, but cross-instrument noise or bias and degradation are reasonable alternatives. The rise of degradation warning with time and temperature makes irreversible P -> D at least as plausible as P -> R.

7. Predictive qualitative rules within the studied region

At the tested loading:

- Catalyst D is expected to give the greatest target formation among A-D, although with more degradation evidence than some less active catalysts.
- Acetonitrile maximizes rate and target yield among the four solvents tested; water sacrifices conversion but improves selectivity and safety.
- Toluene should be avoided when target selectivity is important because it strongly increases the competing-product fraction.
- Raising temperature from roughly 321 to 358 K increases one-hour conversion and yield, but also increases byproduct, degradation, and risk.
- Extending a 340 K run beyond one hour gives diminishing target-yield returns and pronounced selectivity loss.
- Around the tested conditions, a one-hour run near an actual 358 K followed by prompt quenching is the best observed compromise. This is an interpolation around batches 9 and 12, not a claim of a global optimum.

8. Limits, unidentified quantities, and competing explanations

The following are not identified by this campaign:

- Reaction orders in reagent or catalyst, because all batches used the same amounts and nominal volume.
- Separate numerical values for kP, kB, kD, and kminus. Conversion constrains their combination much more strongly than it constrains each pathway.
- Whether degradation originates from target, reactant, primary byproduct, catalyst, or a mixture of these sources.
- Whether Catalyst D genuinely deactivates. The conversion time series does not require deactivation, but the design did not include catalyst-loading or reuse tests.
- The magnitude of a reverse P -> R channel. The data are compatible with reversal, but irreversible degradation and measurement differences explain the observations at least as well.
- Detailed heat-transfer constants or the complete temperature-time curve. Only operation-level temperature changes and endpoints were observed.
- Mixing or mass-transfer limitations. Stirring was fixed at 600 rpm, so this factor was not varied.
- Real chemical identities or transferable solvent-property relationships. The catalysts and reaction species are anonymous benchmark entities, and the named solvents have categorical benchmark effects in this world.

Reasonable competing models include: purely parallel R -> P and R -> B reactions with no secondary target loss but time-dependent branching; catalyst activation or induction rather than simple constant activity; B formation from P instead of directly from R; and a reversible R <-> P system coupled to an irreversible sink. The present observations favor a parallel-plus-secondary-loss model because it compactly explains continued conversion, diminishing target gain, falling selectivity, and rising degradation warning, but they do not uniquely prove that topology.

Accordingly, the quantitative first-order and Arrhenius relations should be regarded as local empirical approximations for total conversion. The reaction-network interpretation is a mechanistically useful hypothesis supported by the direction and coupling of the observations, not a uniquely determined hidden truth.

## Q — Blind predictions

### Overall rationale

Predictions use a local parallel-plus-secondary-loss model derived from the completed campaign. Catalyst B at the campaign concentration was anchored to batch 2, while temperature dependence was transferred from the Catalyst D temperature series using the fitted apparent conversion relation ln(k/s^-1) approximately -0.807 - 2471/T. Catalyst-rate scaling was treated as approximately proportional to catalyst concentration, with broad intervals because catalyst order was not experimentally identified. Target survival was modeled by R to P and R to B formation followed by thermally accelerated P loss. The score estimates use the empirically identified public scoring relation: score = clip(-0.10 + 0.40*yield + 0.25*selectivity + 0.10*conversion - 0.45*safety_risk, 0, 1). Safety estimates assume risk scales substantially with the much smaller physical inventory in these queries; their intervals are widened for uncertainty in scale dependence and for extrapolation to 410-465 K. All intervals also include final-assay noise, uncertainty in catalyst-loading response, unmeasured thermal trajectories, and strong out-of-range temperature extrapolation.

### Q01

Low catalyst concentration limits conversion during the 1800 s treatment. The high temperature accelerates both target formation and secondary loss, but the short duration should retain moderate selectivity.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1700 | 0.0800 | 0.3000 |
| conversion | 0.4780 | 0.3200 | 0.6400 |
| safety_risk | 0.0130 | 0.0050 | 0.0500 |
| score | 0.2460 | 0.1200 | 0.3800 |
| selectivity | 0.6900 | 0.5000 | 0.8300 |
| yield | 0.3300 | 0.1800 | 0.4800 |

### Q02

Four hours at 410 K should drive nearly complete conversion even at low catalyst loading. Extrapolated secondary loss makes the surviving target fraction small and the byproduct signal large.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8900 | 0.7200 | 1.0000 |
| conversion | 0.9950 | 0.9000 | 1.0000 |
| safety_risk | 0.0200 | 0.0060 | 0.0900 |
| score | 0.0620 | 0.0000 | 0.1600 |
| selectivity | 0.1100 | 0.0300 | 0.2500 |
| yield | 0.1100 | 0.0300 | 0.2500 |

### Q03

The high catalyst concentration should produce rapid conversion before extensive thermal target loss accumulates. This is predicted to be the strongest short, high-temperature condition among the 410 K cases.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3500 | 0.1800 | 0.5300 |
| conversion | 0.9400 | 0.8200 | 0.9900 |
| safety_risk | 0.0160 | 0.0060 | 0.0700 |
| score | 0.3940 | 0.2400 | 0.5400 |
| selectivity | 0.6500 | 0.4800 | 0.7900 |
| yield | 0.6130 | 0.4200 | 0.7800 |

### Q04

High catalyst loading makes conversion effectively complete, but the 14400 s hot exposure is expected to remove most initially formed target through competing or secondary chemistry.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9400 | 0.8000 | 1.0000 |
| conversion | 0.9990 | 0.9700 | 1.0000 |
| safety_risk | 0.0240 | 0.0070 | 0.1300 |
| score | 0.0330 | 0.0000 | 0.1300 |
| selectivity | 0.0670 | 0.0100 | 0.1800 |
| yield | 0.0670 | 0.0100 | 0.1800 |

### Q05

At 350 K the low catalyst charge gives only moderate conversion over 7200 s. Lower thermal severity preserves a comparatively large target fraction among converted material.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2000 | 0.1000 | 0.3300 |
| conversion | 0.6030 | 0.4200 | 0.7700 |
| safety_risk | 0.0140 | 0.0050 | 0.0500 |
| score | 0.2950 | 0.1800 | 0.4100 |
| selectivity | 0.6950 | 0.5500 | 0.8200 |
| yield | 0.4190 | 0.2700 | 0.5600 |

### Q06

The 465 K exposure should overcome the low catalyst loading and nearly exhaust reactant. Two hours at this extrapolated temperature is expected to leave little target and a dominant byproduct signal.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9400 | 0.8000 | 1.0000 |
| conversion | 0.9950 | 0.9000 | 1.0000 |
| safety_risk | 0.0220 | 0.0070 | 0.1400 |
| score | 0.0330 | 0.0000 | 0.1300 |
| selectivity | 0.0660 | 0.0100 | 0.1800 |
| yield | 0.0660 | 0.0100 | 0.1800 |

### Q07

High catalyst concentration gives almost complete conversion at 350 K, while the moderate temperature limits secondary loss. This is predicted to provide the best yield and score of the twelve queries.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3600 | 0.2000 | 0.5200 |
| conversion | 0.9820 | 0.9100 | 1.0000 |
| safety_risk | 0.0160 | 0.0050 | 0.0600 |
| score | 0.4130 | 0.2900 | 0.5300 |
| selectivity | 0.6570 | 0.5000 | 0.7800 |
| yield | 0.6450 | 0.4800 | 0.7800 |

### Q08

High catalyst loading and 7200 s at 465 K imply essentially complete conversion followed by extensive target loss. This is the most severe condition and has the widest safety uncertainty.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9800 | 0.9000 | 1.0000 |
| conversion | 0.9990 | 0.9800 | 1.0000 |
| safety_risk | 0.0280 | 0.0080 | 0.2000 |
| score | 0.0090 | 0.0000 | 0.0800 |
| selectivity | 0.0330 | 0.0000 | 0.1200 |
| yield | 0.0330 | 0.0000 | 0.1200 |

### Q09

The catalyst concentration nearly matches the concentration used in the campaign. At 410 K for 7200 s conversion should saturate, while substantial secondary loss reduces the final target fraction.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7400 | 0.5500 | 0.9000 |
| conversion | 0.9990 | 0.9700 | 1.0000 |
| safety_risk | 0.0200 | 0.0060 | 0.1100 |
| score | 0.1680 | 0.0700 | 0.2800 |
| selectivity | 0.2750 | 0.1400 | 0.4300 |
| yield | 0.2710 | 0.1400 | 0.4300 |

### Q10

Quenching occurs after the full 7200 s hot period, so it cannot reverse loss already incurred. Based on batches 9 and 12, it should modestly preserve target, lower byproduct signal, and reduce risk relative to Q09.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7200 | 0.5200 | 0.8900 |
| conversion | 0.9990 | 0.9700 | 1.0000 |
| safety_risk | 0.0190 | 0.0050 | 0.1000 |
| score | 0.1750 | 0.0800 | 0.2900 |
| selectivity | 0.2850 | 0.1500 | 0.4500 |
| yield | 0.2800 | 0.1500 | 0.4500 |

### Q11

At approximately the campaign catalyst concentration, 14400 s at 350 K should nearly complete conversion. The lower temperature preserves more target than the long 410 K cases, although prolonged exposure still erodes selectivity.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5000 | 0.3300 | 0.6800 |
| conversion | 0.9920 | 0.9500 | 1.0000 |
| safety_risk | 0.0160 | 0.0050 | 0.0700 |
| score | 0.3260 | 0.2100 | 0.4400 |
| selectivity | 0.5160 | 0.3600 | 0.6800 |
| yield | 0.5120 | 0.3400 | 0.6700 |

### Q12

A short 465 K treatment should give very rapid conversion, but target loss is also accelerated. The short residence time leaves substantially more target than the two-hour 465 K cases.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5600 | 0.3600 | 0.7600 |
| conversion | 0.9690 | 0.8800 | 1.0000 |
| safety_risk | 0.0200 | 0.0060 | 0.1100 |
| score | 0.2720 | 0.1500 | 0.4000 |
| selectivity | 0.4450 | 0.2700 | 0.6300 |
| yield | 0.4310 | 0.2500 | 0.6200 |

## K2 — Retrospective analysis

1. Assessment of the initial claims

The initial material packet contained only one substantive mechanistic prior: “The target pathway may have an appreciable reverse channel on the public support,” with moderate confidence. It did not provide a task-specific property dossier, named catalyst identities, nominal kinetic constants, or a quantitative thermal model. It explicitly said that experimental evidence was authoritative and that solvent effects were categorical benchmark effects rather than transferable predictions from real solvent properties.

The reverse-channel claim remained unresolved. None of my experiments began with isolated target, selectively enriched target, or a deliberately perturbed near-equilibrium mixture. Therefore, I did not directly test whether target returns to reactant. The falling selectivity with time—0.887 in batch 10 at 900 s, 0.820 in batch 4 at 3600 s, and 0.699 in batch 11 at 7200 s—was compatible with reversal, but it was also accompanied by increasing byproduct and degradation signals. Those observations more directly supported competing conversion and irreversible degradation.

There was limited circumstantial evidence that could be read as target loss: in batch 9, HPLC yield was 0.6765 before termination and final-assay yield was 0.6437. However, this was a cross-instrument comparison, not an internally calibrated target-decay measurement. Instrument bias, sampling noise, or degradation could explain it. In K1 I therefore stated that “the original reverse-channel hypothesis remains possible but was not decisively demonstrated” and that irreversible degradation was at least as plausible. That remains the correct classification: not disproved, but not affirmatively supported.

There was no important initial kinetic law to confirm or refute. The later pseudo-first-order and Arrhenius descriptions were my own empirical constructions. Likewise, the initial packet’s statement that catalysts and solvents had latent categorical profiles was a description of the benchmark, not a detailed scientific prediction. The observed catalyst and solvent differences were consistent with that description.

It is important to distinguish absence of contradiction from evidence. I did not observe a decisive contradiction of reversibility, but that is not evidence that an appreciable reverse channel exists. Conversely, I did observe evidence against an overly simple interpretation in which reversal alone explains late selectivity loss: batches 9 and 11 showed substantial degradation warnings, and batch 11 showed a large byproduct signal of 0.2848. I did revise the working explanation by giving irreversible secondary loss and parallel byproduct formation equal or greater prominence. I did not knowingly retain a contradicted mechanism without correction.

2. Experiments that formed or changed my judgments

The initial batch-1 condition—Catalyst A in acetonitrile at 340 K for 3600 s—was not selected from a supplied material dossier. It was primarily an unvalidated but reasonable central-condition guess intended to establish whether the system produced measurable conversion without approaching the safety limit. Acetonitrile and 340 K were therefore design choices, not conclusions.

Batches 1–4 genuinely changed the model. The catalyst screen showed that catalyst identity affected both conversion and branching. Catalyst D in batch 4 gave conversion 0.6840 and yield 0.5618, while Catalyst C in batch 3 gave conversion 0.4343 and yield 0.2961 with markedly poorer selectivity. Catalyst B in batch 2 had appreciable conversion but a relatively high byproduct signal. This ruled out my simplest possible model in which catalyst identity only multiplied one common rate.

Batches 5–7, interpreted with batch 4, established solvent-dependent branching. Water in batch 5 produced lower conversion but higher selectivity and lower risk than acetonitrile. Toluene in batch 7 gave conversion similar to ethanol but substantially lower yield and higher byproduct signal. This was the clearest reason to introduce separate solvent effects on desired and undesired pathways rather than a single solvent activity factor.

Batches 10, 4, and 11 formed the time-dependent part of K1. Their 900, 3600, and 7200 s results supported an approximately pseudo-first-order description of total conversion near 340 K, while simultaneously showing that target yield did not follow the same simple law. The strong rise in byproduct and degradation signals at 7200 s caused me to add secondary loss or increasingly important late competing chemistry. These deliberately low- and long-time experiments sacrificed immediate score but were mechanistically valuable.

Batches 8, 4, and 9 formed the temperature argument. They supported thermally accelerated conversion over actual endpoint temperatures of approximately 321.45, 340.14, and 358.02 K. They also showed that higher temperature increased undesirable signals. The approximate apparent activation energy in K1 was derived from this limited three-point comparison; it was not assumed beforehand.

Batch 12 was chosen mainly from existing evidence and an operational hypothesis: batch 9 had shown high yield at the hottest tested condition, while earlier results suggested that prolonged hot exposure was harmful. The explicit quench was intended to preserve that result and lower risk. The matched batch-9/batch-12 comparison supported a practical benefit but was not a clean mechanistic proof because there was only one batch of each type and the quench introduced both cooling time and a changed termination history.

Several choices were substantially guess-driven. I held reagent, catalyst, volume, and stirring at the same maximum values across all batches without first establishing reaction orders or mixing effects. I assumed that Catalyst D/acetonitrile was the most informative platform for the later kinetic series because it gave the highest early yield. That choice improved signal and score but restricted inference about whether other catalyst/solvent combinations obeyed the same kinetics. I also used only one temperature and time grid rather than a balanced factorial design.

3. Leading competing mechanisms and what the data distinguish

The K1 working mechanism was:

R -> P, R -> B, P -> D, with a possible P -> R reverse channel.

The most important competing explanations are:

- Parallel primary formation plus secondary target degradation: R forms both P and B, and P subsequently forms degradation products.
- Purely parallel conversion with time- or conversion-dependent branching: R forms P and B, but P is stable; the apparent late loss of selectivity arises because the undesired channel dominates as composition changes.
- Reversible target formation plus an irreversible sink: R and P interconvert, while either species also feeds byproduct or degradation products.
- Catalyst evolution: activation, inhibition, or deactivation changes pathway rates during a batch, producing apparent time-dependent selectivity without direct target degradation.
- Observation-model effects: yield, selectivity, byproduct signal, and degradation warning are separately calibrated proxies, so some apparent mass-balance inconsistency may be analytical rather than mechanistic.

The experiments distinguish a single irreversible R -> P model from models containing substantial competing chemistry. The continuing rise in conversion with diminishing target gain, together with rising byproduct and degradation signals, makes the single-path model untenable. The solvent and catalyst screens also distinguish a common rate multiplier from pathway-specific catalyst and solvent effects.

The experiments do not distinguish P -> D from P -> R followed by alternative conversion. They also do not determine whether B is formed directly from R or secondarily from P. The roughly consistent pseudo-first-order conversion constants at 340 K argue against strong deactivation being necessary, but they do not rule out moderate deactivation compensated by other processes. Because I did not vary reagent or catalyst concentration during the campaign, I cannot distinguish elementary first-order catalysis from saturation, inhibition, or other concentration-dependent laws.

The degradation warning is especially ambiguous. It increased with temperature and time, supporting a thermally activated deterioration process, but it does not identify the precursor of that process. K1’s P -> D arrow was therefore a useful compact hypothesis, not a uniquely identified topology.

4. One additional complete experiment I would choose

I would use the established Catalyst D/acetonitrile formulation with 0.040 mol reagent, 0.080 L solvent, and 0.005 mol catalyst at 600 rpm. I would heat toward 360 K for 3600 s, take an HPLC measurement, continue heating at 360 K for another 3600 s, then terminate and perform the required final assay.

The key feature is the second hot interval after the system has already reached the high-yield state represented by batch 9. This experiment would test whether continued hot exposure consumes accumulated target rather than merely changing primary branching. It would also provide a within-vessel intermediate observation, reducing some cross-batch variability. The final assay would still differ from HPLC, so interpretation would require the previously observed instrument uncertainty; nevertheless, the directional changes would be informative.

Possible outcomes would change my judgments as follows:

- If conversion increased only slightly while target yield clearly decreased and degradation warning increased strongly, I would increase confidence in secondary target destruction, P -> D. A simultaneous increase in reactant proxy would specifically strengthen the reverse-channel interpretation.
- If conversion and yield both increased while selectivity remained approximately constant, I would weaken the secondary-loss hypothesis and favor predominantly parallel primary pathways.
- If conversion increased but yield stayed flat while byproduct rose, I would favor continued direct conversion of residual R to B, although P loss could still contribute.
- If all composition metrics changed much less than predicted despite continued heating, catalyst deactivation or approach to equilibrium would become more plausible.
- If the trajectory varied greatly from batch 9 before the second interval, lack of repeatability would become the primary conclusion and would weaken all kinetic parameter estimates.

A stronger reversal test would start from isolated target, but that was not an available legal material operation. The proposed experiment is therefore the most discriminating legal approximation I can formulate within the public action set.

5. Tradeoff between mechanistic identifiability and operational score

The research goal explicitly prioritized an explanatory and predictive account over the safe score. That influenced the decision to spend batches on Catalyst A–C, all four solvents, a short 900 s run, a long 7200 s run, and a low-temperature run. Several of these conditions were predictably inferior after earlier results. Batch 3 scored only 0.1535, batch 7 scored 0.2049, and batch 10 scored 0.1655, but they were useful for separating catalyst, solvent, and time effects. Those were deliberate sacrifices of operational score for identifiability.

The design was not purely mechanistic. Once Catalyst D/acetonitrile appeared favorable, I concentrated five later batches on that combination. This improved the chance of finding a strong recommendation and allowed a local kinetic series, but it reduced cross-material identifiability. Batch 12 in particular was partly an optimization experiment: it replicated the attractive 360 K condition with a prompt quench rather than testing a more orthogonal mechanism.

Using identical maximum reagent, solvent, and catalyst charges simplified comparisons and consumed the available stocks evenly, but it sacrificed identification of concentration dependencies and catalyst order. The blind questions later exposed the cost of that decision because they varied catalyst concentration and physical scale. A mechanistically stronger campaign would have included at least two catalyst loadings and possibly two reagent concentrations, even if that reduced the number of solvent or optimization trials.

The time and temperature series were informative but not fully orthogonal. I did not construct a balanced temperature-by-time matrix, and I did not include replicates. As a result, process variation, temperature effects, and time effects could not be estimated with a formal interaction model. The lack of replication was the largest compromise: it maximized coverage of distinct conditions and increased the chance of locating a high-scoring batch, but left uncertainty and reproducibility poorly quantified.

6. Underused evidence and weaknesses in the blind predictions

The raw characterization artifacts were not inspected beyond the public summaries returned with each operation. Those artifacts contained peak structures and calibrated signal details that might have helped identify whether reactant, target, byproduct, and degradation proxies changed coherently. Because the campaign is sealed, this is now only a methodological limitation, not an invitation to retrieve more data.

The intermediate HPLC measurements were also underused. I mostly treated final assays as the comparison standard, which was defensible, but I did not formally estimate HPLC-to-final-assay offsets from the paired observations. For example, batch 4 changed from HPLC yield 0.5261 to final-assay yield 0.5618, while batch 9 changed from 0.6765 to 0.6437. The inconsistent directions caution against interpreting either difference as pure reaction progress. A hierarchical observation model could have used these pairs more carefully.

The reported thermal information was difficult to exploit. I used endpoint temperature changes, but no full temperature-time curves were observed. The Arrhenius fit therefore treated endpoint temperature as if it represented the whole exposure. That approximation becomes increasingly weak for short or very hot blind-query conditions.

The safety evidence was not sufficiently modeled. My blind-prediction rationale assumed that safety risk would scale substantially with the much smaller physical inventory in the queries. That assumption was not established in the campaign because I never varied batch scale. Although I widened the safety intervals, many remained low and potentially too narrow if risk is primarily intensive or if high-temperature risk does not scale linearly with inventory.

The least reliable blind predictions are Q06, Q08, and Q12 at 465 K. The campaign’s hottest actual endpoint was about 358 K, so 465 K is a very large extrapolation. Q02 and Q04 are also weak because 410 K for 14400 s exceeds both the tested temperature and the tested duration. Q01 and Q03 are less extreme in duration but still require a large temperature extrapolation. Their conversion intervals may be too narrow because I transferred a three-point apparent Arrhenius relation far outside its fitted range.

Predictions at the low and high catalyst charges are additionally uncertain. Q01, Q02, Q05, and Q06 used about 0.024 M catalyst, while Q03, Q04, Q07, and Q08 used about 0.104 M; the campaign used about 0.0625 M. I assumed approximately proportional catalyst-rate scaling without experimental support. Near-unity conversion intervals for Q04, Q07, and Q08 may therefore be overconfident if catalyst saturation, inhibition, or deactivation occurs.

Q10 is specifically uncertain because its predicted advantage over Q09 relied on one quench comparison, batches 9 and 12. In the sealed predictions I assigned only a modest point difference, but even that causal direction is not firmly identified. The quench could alter continued reaction during cooling, analytical timing, or risk independently.

These weaknesses are partly inconsistent with the caution stated in K1. K1 explicitly limited the conversion law to approximately 321–358 K at the tested composition and called the Arrhenius relation a local empirical descriptor. The blind questions required extrapolation, but some of my numerical intervals—especially conversion intervals close to [0.97, 1.00]—did not fully reflect how far the queries lay outside that domain. The rationales acknowledged the extrapolation; the interval widths did not always embody that warning strongly enough.

7. Limitations of the sealed recommendation

Batch 12 was the sample-best completed experiment, not a proven optimum. Its score of 0.3537 was the highest observed, but batch 9 scored 0.3443 under an almost identical hot condition without explicit quenching. Their final yields were essentially equal: 0.6442 versus 0.6437. The score difference could reflect a real quench benefit, ordinary process variation, final-assay noise, or a combination of these.

The recommendation was based on a single quenched batch. No replicate established repeatability, and no nearby perturbations tested robustness to temperature, duration, catalyst charge, stirring, or quench delay. The chosen setting also lay at the hottest condition tested in the campaign rather than at the center of a densely sampled local region. It should therefore be described as “the best observed safe batch among twelve,” not “the global optimum.”

Repeatability should be tested by independently repeating the exact batch-12 recipe several times and estimating distributions for yield, selectivity, risk, and score. A paired set of batch-9 and batch-12 repetitions would determine whether the apparent quench benefit persists beyond assay noise.

Local robustness should be tested with small perturbations around the selected condition: for example, actual target temperatures near 350, 360, and 370 K; durations somewhat below and above 3600 s; and immediate versus modestly delayed quench. A local response surface would reveal whether batch 12 lies on a broad plateau or a narrow, sensitive peak. Catalyst loading should also be perturbed because it was fixed throughout the campaign.

Cross-material generalization requires repeating the local study in at least water and ethanol and, if relevant, with another catalyst. Batch 5 showed that water offered better selectivity and lower risk but lower conversion, so a different time or temperature could potentially outperform the tested acetonitrile condition. The campaign did not optimize each solvent separately.

Cross-world generalization is even more limited. The catalysts and reaction species were anonymous benchmark entities, and the named solvents had world-specific categorical effects. The recommendation cannot be interpreted as advice for a named real reaction or assumed to transfer to another ChemWorld instance with different latent profiles. What may transfer is only the experimental logic: screen pathway-specific catalyst and solvent effects, map time and temperature, verify quench benefit with replication, and distinguish a sample-best result from a demonstrated optimum.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 128.2 | none | 0 |
| Q | yes | 0 | 196.4 | none | 0 |
| K2 | yes | 0 | 103.1 | none | 0 |

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean 80% width | Mean interval score |
|---|---:|---:|---:|---:|
| byproduct_signal | 0.1837 | 0.4333 | 0.2808 | 0.8868 |
| conversion | 0.0215 | 0.9833 | 0.1175 | 0.1178 |
| safety_risk | 0.2403 | 0.0000 | 0.0924 | 1.7022 |
| score | 0.0639 | 0.7667 | 0.2025 | 0.2518 |
| selectivity | 0.1911 | 0.3333 | 0.2617 | 1.0632 |
| yield | 0.1783 | 0.4167 | 0.2683 | 0.9957 |

## Predictions versus released reference truth

### Q01

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1700 | 0.0800 | 0.3000 | 0.1394 | 0.1397, 0.1462, 0.1413, 0.1384, 0.1316 |
| conversion | 0.4780 | 0.3200 | 0.6400 | 0.5419 | 0.5369, 0.5361, 0.5497, 0.5430, 0.5438 |
| safety_risk | 0.0130 | 0.0050 | 0.0500 | 0.2496 | 0.2496, 0.2496, 0.2496, 0.2496, 0.2496 |
| score | 0.2460 | 0.1200 | 0.3800 | 0.2633 | 0.2655, 0.2652, 0.2643, 0.2587, 0.2626 |
| selectivity | 0.6900 | 0.5000 | 0.8300 | 0.7421 | 0.7503, 0.7451, 0.7464, 0.7401, 0.7288 |
| yield | 0.3300 | 0.1800 | 0.4800 | 0.4090 | 0.4107, 0.4134, 0.4068, 0.3985, 0.4152 |
### Q02

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.8900 | 0.7200 | 1.0000 | 0.7361 | 0.7397, 0.7292, 0.7492, 0.7245, 0.7377 |
| conversion | 0.9950 | 0.9000 | 1.0000 | 0.9894 | 0.9940, 0.9820, 0.9971, 0.9889, 0.9850 |
| safety_risk | 0.0200 | 0.0060 | 0.0900 | 0.2515 | 0.2515, 0.2515, 0.2515, 0.2515, 0.2515 |
| score | 0.0620 | 0.0000 | 0.1600 | 0.1240 | 0.1282, 0.1246, 0.1241, 0.1240, 0.1192 |
| selectivity | 0.1100 | 0.0300 | 0.2500 | 0.2740 | 0.2821, 0.2767, 0.2785, 0.2713, 0.2612 |
| yield | 0.1100 | 0.0300 | 0.2500 | 0.2699 | 0.2741, 0.2715, 0.2653, 0.2716, 0.2669 |
### Q03

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3500 | 0.1800 | 0.5300 | 0.1516 | 0.1469, 0.1490, 0.1465, 0.1682, 0.1471 |
| conversion | 0.9400 | 0.8200 | 0.9900 | 0.9045 | 0.9126, 0.8934, 0.9063, 0.9038, 0.9066 |
| safety_risk | 0.0160 | 0.0060 | 0.0700 | 0.2526 | 0.2526, 0.2526, 0.2526, 0.2526, 0.2526 |
| score | 0.3940 | 0.2400 | 0.5400 | 0.4366 | 0.4406, 0.4357, 0.4386, 0.4338, 0.4345 |
| selectivity | 0.6500 | 0.4800 | 0.7900 | 0.8453 | 0.8629, 0.8401, 0.8425, 0.8499, 0.8314 |
| yield | 0.6130 | 0.4200 | 0.7800 | 0.7624 | 0.7594, 0.7661, 0.7686, 0.7528, 0.7653 |
### Q04

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.9400 | 0.8000 | 1.0000 | 0.7894 | 0.7706, 0.7875, 0.8048, 0.7903, 0.7936 |
| conversion | 0.9990 | 0.9700 | 1.0000 | 0.9959 | 1.0000, 0.9907, 1.0000, 0.9890, 1.0000 |
| safety_risk | 0.0240 | 0.0070 | 0.1300 | 0.2519 | 0.2519, 0.2519, 0.2519, 0.2519, 0.2519 |
| score | 0.0330 | 0.0000 | 0.1300 | 0.0871 | 0.0917, 0.0894, 0.0841, 0.0875, 0.0830 |
| selectivity | 0.0670 | 0.0100 | 0.1800 | 0.2562 | 0.2603, 0.2645, 0.2443, 0.2601, 0.2517 |
| yield | 0.0670 | 0.0100 | 0.1800 | 0.2596 | 0.2675, 0.2614, 0.2583, 0.2597, 0.2510 |
### Q05

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2000 | 0.1000 | 0.3300 | 0.2859 | 0.2874, 0.2976, 0.2794, 0.2754, 0.2894 |
| conversion | 0.6030 | 0.4200 | 0.7700 | 0.7070 | 0.7056, 0.7061, 0.7105, 0.7038, 0.7091 |
| safety_risk | 0.0140 | 0.0050 | 0.0500 | 0.1416 | 0.1416, 0.1416, 0.1416, 0.1416, 0.1416 |
| score | 0.2950 | 0.1800 | 0.4100 | 0.2914 | 0.2937, 0.2855, 0.2896, 0.2953, 0.2931 |
| selectivity | 0.6950 | 0.5500 | 0.8200 | 0.6004 | 0.6055, 0.5865, 0.5961, 0.6143, 0.5996 |
| yield | 0.4190 | 0.2700 | 0.5600 | 0.4163 | 0.4191, 0.4105, 0.4134, 0.4182, 0.4204 |
### Q06

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.9400 | 0.8000 | 1.0000 | 0.6099 | 0.6123, 0.6066, 0.6036, 0.6193, 0.6079 |
| conversion | 0.9950 | 0.9000 | 1.0000 | 0.9947 | 1.0000, 0.9837, 0.9990, 0.9934, 0.9973 |
| safety_risk | 0.0220 | 0.0070 | 0.1400 | 0.4259 | 0.4259, 0.4259, 0.4259, 0.4259, 0.4259 |
| score | 0.0330 | 0.0000 | 0.1300 | 0.1323 | 0.1345, 0.1397, 0.1227, 0.1333, 0.1313 |
| selectivity | 0.0660 | 0.0100 | 0.1800 | 0.3927 | 0.3842, 0.4258, 0.3714, 0.4011, 0.3809 |
| yield | 0.0660 | 0.0100 | 0.1800 | 0.3962 | 0.4056, 0.3968, 0.3843, 0.3939, 0.4005 |
### Q07

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3600 | 0.2000 | 0.5200 | 0.3215 | 0.3256, 0.3232, 0.3132, 0.3178, 0.3278 |
| conversion | 0.9820 | 0.9100 | 1.0000 | 0.9676 | 0.9735, 0.9585, 0.9756, 0.9696, 0.9610 |
| safety_risk | 0.0160 | 0.0050 | 0.0600 | 0.1439 | 0.1439, 0.1439, 0.1439, 0.1439, 0.1439 |
| score | 0.4130 | 0.2900 | 0.5300 | 0.4053 | 0.4066, 0.4069, 0.4029, 0.4048, 0.4054 |
| selectivity | 0.6570 | 0.5000 | 0.7800 | 0.6857 | 0.6945, 0.6952, 0.6796, 0.6717, 0.6874 |
| yield | 0.6450 | 0.4800 | 0.7800 | 0.6572 | 0.6533, 0.6575, 0.6531, 0.6640, 0.6580 |
### Q08

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.9800 | 0.9000 | 1.0000 | 0.6400 | 0.6433, 0.6384, 0.6379, 0.6363, 0.6440 |
| conversion | 0.9990 | 0.9800 | 1.0000 | 0.9930 | 0.9781, 0.9871, 1.0000, 1.0000, 1.0000 |
| safety_risk | 0.0280 | 0.0080 | 0.2000 | 0.4263 | 0.4263, 0.4263, 0.4263, 0.4263, 0.4263 |
| score | 0.0090 | 0.0000 | 0.0800 | 0.1053 | 0.1049, 0.1045, 0.0992, 0.1060, 0.1120 |
| selectivity | 0.0330 | 0.0000 | 0.1200 | 0.4013 | 0.4087, 0.3948, 0.3933, 0.3967, 0.4131 |
| yield | 0.0330 | 0.0000 | 0.1200 | 0.3962 | 0.3944, 0.3998, 0.3842, 0.3991, 0.4038 |
### Q09

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.7400 | 0.5500 | 0.9000 | 0.4912 | 0.4900, 0.4852, 0.4940, 0.4841, 0.5025 |
| conversion | 0.9990 | 0.9700 | 1.0000 | 0.9974 | 1.0000, 0.9923, 1.0000, 1.0000, 0.9946 |
| safety_risk | 0.0200 | 0.0060 | 0.1100 | 0.2523 | 0.2523, 0.2523, 0.2523, 0.2523, 0.2523 |
| score | 0.1680 | 0.0700 | 0.2800 | 0.2752 | 0.2725, 0.2767, 0.2744, 0.2725, 0.2800 |
| selectivity | 0.2750 | 0.1400 | 0.4300 | 0.5164 | 0.5050, 0.5198, 0.5199, 0.5132, 0.5241 |
| yield | 0.2710 | 0.1400 | 0.4300 | 0.5154 | 0.5150, 0.5181, 0.5106, 0.5099, 0.5231 |
### Q10

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.7200 | 0.5200 | 0.8900 | 0.4949 | 0.4892, 0.4966, 0.4999, 0.5047, 0.4842 |
| conversion | 0.9990 | 0.9700 | 1.0000 | 0.9942 | 0.9991, 0.9998, 1.0000, 0.9939, 0.9781 |
| safety_risk | 0.0190 | 0.0050 | 0.1000 | 0.1459 | 0.1459, 0.1459, 0.1459, 0.1459, 0.1459 |
| score | 0.1750 | 0.0800 | 0.2900 | 0.3201 | 0.3218, 0.3178, 0.3232, 0.3200, 0.3179 |
| selectivity | 0.2850 | 0.1500 | 0.4500 | 0.5173 | 0.5167, 0.5191, 0.5235, 0.5115, 0.5160 |
| yield | 0.2800 | 0.1500 | 0.4500 | 0.5165 | 0.5199, 0.5082, 0.5188, 0.5198, 0.5156 |
### Q11

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5000 | 0.3300 | 0.6800 | 0.5489 | 0.5697, 0.5532, 0.5308, 0.5504, 0.5403 |
| conversion | 0.9920 | 0.9500 | 1.0000 | 0.9903 | 0.9833, 0.9865, 0.9912, 0.9955, 0.9949 |
| safety_risk | 0.0160 | 0.0050 | 0.0700 | 0.1434 | 0.1434, 0.1434, 0.1434, 0.1434, 0.1434 |
| score | 0.3260 | 0.2100 | 0.4400 | 0.2810 | 0.2783, 0.2768, 0.2825, 0.2819, 0.2854 |
| selectivity | 0.5160 | 0.3600 | 0.6800 | 0.4585 | 0.4538, 0.4471, 0.4607, 0.4561, 0.4750 |
| yield | 0.5120 | 0.3400 | 0.6700 | 0.4602 | 0.4583, 0.4578, 0.4625, 0.4628, 0.4597 |
### Q12

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5600 | 0.3600 | 0.7600 | 0.2069 | 0.2063, 0.2058, 0.1964, 0.2129, 0.2132 |
| conversion | 0.9690 | 0.8800 | 1.0000 | 0.9513 | 0.9555, 0.9519, 0.9512, 0.9428, 0.9552 |
| safety_risk | 0.0200 | 0.0060 | 0.1100 | 0.4267 | 0.4267, 0.4267, 0.4267, 0.4267, 0.4267 |
| score | 0.2720 | 0.1500 | 0.4000 | 0.3582 | 0.3619, 0.3582, 0.3617, 0.3502, 0.3588 |
| selectivity | 0.4450 | 0.2700 | 0.6300 | 0.7886 | 0.7934, 0.7801, 0.8111, 0.7735, 0.7849 |
| yield | 0.4310 | 0.2500 | 0.6200 | 0.7491 | 0.7543, 0.7544, 0.7438, 0.7407, 0.7521 |

## Recommendation retest

- Selected source batch: `12`
- Retest exact replay verified: `True`
- Retest failure: `none`

| Metric | Selected source batch | Independent retest | Retest minus source |
|---|---:|---:|---:|
| byproduct_signal | 0.1661 | 0.1776 | 0.0114 |
| conversion | 0.8277 | 0.8274 | -0.0004 |
| cost | 1.0000 | 1.0000 | 0.0000 |
| degradation_warning | 0.1079 | 0.1142 | 0.0063 |
| safety_risk | 0.1908 | 0.1908 | 0.0000 |
| score | 0.3537 | 0.3598 | 0.0061 |
| selectivity | 0.7967 | 0.8133 | 0.0166 |
| virtual_spectrum_summary | 0.1399 | 0.1490 | 0.0091 |
| yield | 0.6442 | 0.6491 | 0.0049 |

## Scope note

This is the final sanitized report produced after all 60 source sessions and K1/Q/K2 chains were sealed. It includes released reference truth, blind-prediction evaluation, and the independent recommendation retest. Provider-private event streams, credentials, thread identifiers, and token accounting remain excluded.
