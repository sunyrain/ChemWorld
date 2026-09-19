# RX-W04--P--safety_constrained_optimization--Aligned

## Run summary

- World: `RX-W04`
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

- Selected batch: `12`
- Rationale: Batch 12 achieved the highest completed-batch public safe score (0.4489) while keeping safety risk low (0.170), comfortably below the 0.35 limit.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 420 K x 3300 s @ 350 rpm | no | 0.7778 | 0.8047 | 0.9708 | 0.1876 | 0.1019 | 0.2858 | 0.4152 |
| 2 | S0 (0.0050 L) | 0.003000 mol | C0 (0.000525 mol) | 420 K x 3300 s @ 350 rpm | no | 0.6021 | 0.7059 | 0.8433 | 0.2666 | 0.1215 | 0.2847 | 0.3290 |
| 3 | S0 (0.0050 L) | 0.003000 mol | C2 (0.000525 mol) | 420 K x 3300 s @ 350 rpm | no | 0.6079 | 0.7185 | 0.8572 | 0.2625 | 0.0441 | 0.2845 | 0.3275 |
| 4 | S0 (0.0050 L) | 0.003000 mol | C3 (0.000525 mol) | 420 K x 3300 s @ 350 rpm | no | 0.7084 | 0.7628 | 0.8907 | 0.1884 | 0.0869 | 0.2851 | 0.3609 |
| 5 | S1 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 420 K x 3300 s @ 350 rpm | no | 0.6435 | 0.6592 | 0.9798 | 0.3398 | 0.1889 | 0.3088 | 0.3154 |
| 6 | S2 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 420 K x 3300 s @ 350 rpm | no | 0.6598 | 0.6375 | 0.9947 | 0.3536 | 0.2839 | 0.3271 | 0.3095 |
| 7 | S3 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 420 K x 3300 s @ 350 rpm | no | 0.6941 | 0.6912 | 1.0000 | 0.3136 | 0.2301 | 0.3399 | 0.3316 |
| 8 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 410 K x 3300 s @ 350 rpm | no | 0.7750 | 0.8210 | 0.9408 | 0.1951 | 0.0879 | 0.2362 | 0.4375 |
| 9 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 400 K x 3300 s @ 350 rpm | no | 0.7488 | 0.8198 | 0.9054 | 0.1679 | 0.1010 | 0.1894 | 0.4442 |
| 10 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 430 K x 3300 s @ 350 rpm | no | 0.7866 | 0.7975 | 0.9686 | 0.2217 | 0.1407 | 0.3287 | 0.3974 |
| 11 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 400 K x 4500 s @ 350 rpm | no | 0.7447 | 0.7815 | 0.9675 | 0.2204 | 0.1242 | 0.1896 | 0.4381 |
| 12 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 395 K x 4500 s @ 350 rpm | no | 0.7497 | 0.7913 | 0.9428 | 0.2223 | 0.1219 | 0.1700 | 0.4489 |

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
      "volume_L": 0.005
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 350,
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
    "byproduct_signal": 0.18758054077625275,
    "conversion": 0.9708428382873535,
    "cost": 0.6557000279426575,
    "degradation_warning": 0.10187100619077682,
    "safety_risk": 0.2858142554759979,
    "score": 0.4151908755302429,
    "selectivity": 0.8046835064888,
    "virtual_spectrum_summary": 0.1490112543106079,
    "yield": 0.7778053879737854
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
      "volume_L": 0.005
    },
    {
      "catalyst": 0,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 350,
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
    "byproduct_signal": 0.26659414172172546,
    "conversion": 0.843253493309021,
    "cost": 0.4456999897956848,
    "degradation_warning": 0.12146889418363571,
    "safety_risk": 0.28465357422828674,
    "score": 0.32899361848831177,
    "selectivity": 0.7059487700462341,
    "virtual_spectrum_summary": 0.20128779113292694,
    "yield": 0.6021129488945007
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
      "volume_L": 0.005
    },
    {
      "catalyst": 2,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 350,
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
    "byproduct_signal": 0.26247382164001465,
    "conversion": 0.8572264909744263,
    "cost": 0.529699981212616,
    "degradation_warning": 0.04408959671854973,
    "safety_risk": 0.28448230028152466,
    "score": 0.32753413915634155,
    "selectivity": 0.7185215950012207,
    "virtual_spectrum_summary": 0.16420091688632965,
    "yield": 0.6079202890396118
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
      "solvent": 0,
      "volume_L": 0.005
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 350,
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
    "byproduct_signal": 0.1883627027273178,
    "conversion": 0.8906969428062439,
    "cost": 0.7397000193595886,
    "degradation_warning": 0.08688860386610031,
    "safety_risk": 0.28508272767066956,
    "score": 0.36086422204971313,
    "selectivity": 0.7628098726272583,
    "virtual_spectrum_summary": 0.14269934594631195,
    "yield": 0.7083732485771179
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
      "solvent": 1,
      "volume_L": 0.005
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 350,
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
    "byproduct_signal": 0.33981606364250183,
    "conversion": 0.9798055291175842,
    "cost": 0.6577000021934509,
    "degradation_warning": 0.18894553184509277,
    "safety_risk": 0.30880019068717957,
    "score": 0.3154407739639282,
    "selectivity": 0.6592239141464233,
    "virtual_spectrum_summary": 0.27192431688308716,
    "yield": 0.6434608101844788
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
      "solvent": 2,
      "volume_L": 0.005
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 350,
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
    "byproduct_signal": 0.3535842001438141,
    "conversion": 0.9947171807289124,
    "cost": 0.6608999967575073,
    "degradation_warning": 0.2838536500930786,
    "safety_risk": 0.3271262049674988,
    "score": 0.3094910681247711,
    "selectivity": 0.6375085115432739,
    "virtual_spectrum_summary": 0.32220545411109924,
    "yield": 0.6598474979400635
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
      "solvent": 3,
      "volume_L": 0.005
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 350,
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
    "byproduct_signal": 0.31364569067955017,
    "conversion": 1.0,
    "cost": 0.6589000225067139,
    "degradation_warning": 0.23014354705810547,
    "safety_risk": 0.3398732542991638,
    "score": 0.3315962255001068,
    "selectivity": 0.6911695003509521,
    "virtual_spectrum_summary": 0.2760697305202484,
    "yield": 0.6940920352935791
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
      "volume_L": 0.005
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 350,
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
  "end_step": 56,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.19507922232151031,
    "conversion": 0.9407841563224792,
    "cost": 0.6557000279426575,
    "degradation_warning": 0.08786054700613022,
    "safety_risk": 0.2361977994441986,
    "score": 0.4374576508998871,
    "selectivity": 0.8209930658340454,
    "virtual_spectrum_summary": 0.14683081209659576,
    "yield": 0.7749749422073364
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
      "volume_L": 0.005
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 350,
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
  "end_step": 63,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.1679149717092514,
    "conversion": 0.9054339528083801,
    "cost": 0.6557000279426575,
    "degradation_warning": 0.10095566511154175,
    "safety_risk": 0.1894015669822693,
    "score": 0.44420531392097473,
    "selectivity": 0.8198174834251404,
    "virtual_spectrum_summary": 0.13778327405452728,
    "yield": 0.7487705945968628
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
      "volume_L": 0.005
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 350,
      "target_temperature_K": 430
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
    "byproduct_signal": 0.22170430421829224,
    "conversion": 0.968553364276886,
    "cost": 0.6557000279426575,
    "degradation_warning": 0.1407317966222763,
    "safety_risk": 0.3287447988986969,
    "score": 0.397367388010025,
    "selectivity": 0.7975360751152039,
    "virtual_spectrum_summary": 0.1852666735649109,
    "yield": 0.7865829467773438
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
      "volume_L": 0.005
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 4500,
      "operation": "heat",
      "stirring_speed_rpm": 350,
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
  "end_step": 77,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.22042427957057953,
    "conversion": 0.9674975872039795,
    "cost": 0.6657000184059143,
    "degradation_warning": 0.12422818690538406,
    "safety_risk": 0.18964174389839172,
    "score": 0.4381013810634613,
    "selectivity": 0.7814568877220154,
    "virtual_spectrum_summary": 0.17713603377342224,
    "yield": 0.7447404265403748
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
      "volume_L": 0.005
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 4500,
      "operation": "heat",
      "stirring_speed_rpm": 350,
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
  "end_step": 84,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.2223241776227951,
    "conversion": 0.9428380131721497,
    "cost": 0.6657000184059143,
    "degradation_warning": 0.12194511294364929,
    "safety_risk": 0.1699923276901245,
    "score": 0.4489244520664215,
    "selectivity": 0.7913070917129517,
    "virtual_spectrum_summary": 0.1771536022424698,
    "yield": 0.7497010827064514
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

1. Scope and evidence base

This report describes only the bounded synthetic reaction-and-thermal world explored in the completed 12-batch campaign. It is not a claim about a named real reaction, catalyst, or industrial process. The reagent and catalysts were anonymous benchmark materials, while solvent names identified selectable reference components whose effects were benchmark-specific.

Every batch used 0.003 mol reagent, 0.005 L solvent, 0.000525 mol catalyst, and 350 rpm stirring. Thus, the campaign identifies categorical catalyst and solvent effects plus local temperature/time effects around this single composition; it does not identify concentration-order laws or scale dependence.

Reported endpoint values below are final-assay observations. Intermediate HPLC results were useful diagnostically but differed from final assays because of instrument noise, sampling, and possibly small state differences. The safety limit was 0.35.

2. Proposed reaction network

A minimal interpretation is a parallel/serial network:

R -> P  (desired pathway)
R -> B  (competitive byproduct pathway)
P -> D  (thermal degradation or secondary loss)

One possible local kinetic representation is:

dR/dt = -(kP + kB) R

dP/dt = kP R - kD P

dB/dt = kB R + alpha*kD*P

where kP, kB, and kD depend on catalyst, solvent, and temperature. A conventional local form would be

ki = Ai(catalyst, solvent) * exp[-Ei/(Rgas*T)]

but the experiments do not establish Arrhenius behavior, reaction orders, or whether the hidden simulator literally uses these equations. They are a compact phenomenological explanation of the observed conversion/selectivity tradeoffs.

The measurements support the following qualitative relationships:

- Catalyst identity strongly changes desired-path activity and selectivity.
- Higher temperature generally increases conversion but also increases safety risk and secondary chemistry.
- Longer reaction time can increase conversion while eroding selectivity and increasing byproduct formation.
- Solvent identity affects both intrinsic setup risk and pathway selectivity.
- The public score behaves like a combined utility that rewards yield/selectivity/conversion and penalizes risk, byproduct, degradation, and cost. Its exact equation remains unidentified.

3. Catalyst effects

Batches 1-4 isolated catalyst identity at water, target 420 K, and 3300 s:

- Batch 1, Catalyst B: conversion 0.9708, yield 0.7778, selectivity 0.8047, byproduct 0.1876, degradation warning 0.1019, risk 0.2858, score 0.4152.
- Batch 2, Catalyst A: conversion 0.8433, yield 0.6021, selectivity 0.7059, byproduct 0.2666, degradation warning 0.1215, risk 0.2847, score 0.3290.
- Batch 3, Catalyst C: conversion 0.8572, yield 0.6079, selectivity 0.7185, byproduct 0.2625, degradation warning 0.0441, risk 0.2845, score 0.3275.
- Batch 4, Catalyst D: conversion 0.8907, yield 0.7084, selectivity 0.7628, byproduct 0.1884, degradation warning 0.0869, risk 0.2851, score 0.3609.

Because risk was almost constant across these four batches, the performance differences are chiefly chemical rather than safety-related. Catalyst B was the best catalyst in the tested context. It produced the highest conversion, yield, selectivity, and score. Catalyst D was second best. Catalysts A and C had similar low yields and high byproduct signals, although Catalyst C showed the lowest degradation warning.

My interpretation is that Catalyst B has the largest effective desired-path rate relative to the competitive rate, not merely the highest total activity. Catalyst D appears moderately active and selective. Catalyst C's low degradation warning shows that low degradation alone is insufficient: its initial desired conversion/selectivity performance was poorer.

This catalyst ranking is established only for the tested loading, water, and local thermal region. Catalyst-temperature or catalyst-solvent interactions were not independently mapped.

4. Solvent effects and coupling to safety

Batches 1 and 5-7 compared the four solvents with Catalyst B at target 420 K for 3300 s:

- Batch 1, water: conversion 0.9708, yield 0.7778, selectivity 0.8047, byproduct 0.1876, degradation 0.1019, risk 0.2858, score 0.4152.
- Batch 5, ethanol: conversion 0.9798, yield 0.6435, selectivity 0.6592, byproduct 0.3398, degradation 0.1889, risk 0.3088, score 0.3154.
- Batch 6, acetonitrile: conversion 0.9947, yield 0.6598, selectivity 0.6375, byproduct 0.3536, degradation 0.2839, risk 0.3271, score 0.3095.
- Batch 7, toluene: reported conversion 1.0000, yield 0.6941, selectivity 0.6912, byproduct 0.3136, degradation 0.2301, risk 0.3399, score 0.3316.

The nonaqueous solvents drove high disappearance of reactant but substantially poorer selectivity. This is evidence that conversion alone is not a reliable proxy for productive chemistry. Water gave both the best selectivity and lowest byproduct signal, and therefore the best score.

Solvent identity also changed risk before or during otherwise matched heating. The final risks rose in the order water (0.2858) < ethanol (0.3088) < acetonitrile (0.3271) < toluene (0.3399). The thermal-operation risk increments themselves were similar, approximately 0.196, implying that much of this solvent ranking arose from the formulation/setup term rather than a strongly different heating response. Toluene remained barely below the 0.35 constraint at this setting, so extrapolation to hotter conditions would be unsafe.

A plausible mechanistic interpretation is that solvent changes the ratio kP/kB and the degradation propensity, while also contributing an independent safety-risk offset. However, polarity, boiling point, heat capacity, and other real-solvent properties were not experimentally isolated, so attributing these benchmark effects to a specific physical property would be speculation.

5. Temperature response

With Catalyst B, water, and 3300 s, batches 1, 8, 9, and 10 varied target temperature:

- Batch 9, 400 K: conversion 0.9054, yield 0.7488, selectivity 0.8198, byproduct 0.1679, risk 0.1894, score 0.4442.
- Batch 8, 410 K: conversion 0.9408, yield 0.7750, selectivity 0.8210, byproduct 0.1951, risk 0.2362, score 0.4375.
- Batch 1, 420 K: conversion 0.9708, yield 0.7778, selectivity 0.8047, byproduct 0.1876, risk 0.2858, score 0.4152.
- Batch 10, 430 K: conversion 0.9686, yield 0.7866, selectivity 0.7975, byproduct 0.2217, risk 0.3287, score 0.3974.

The dominant monotonic observation is the rise in risk with target temperature. Risk increased by roughly 0.047-0.050 for each 10 K step over 400-430 K. Conversion generally increased toward a plateau near 0.97, while selectivity weakened at the hotter settings. Yield did not increase enough to compensate for risk and byproduct penalties, so final score peaked on the lower-temperature side.

The heat operation did not instantaneously reach its target. Reported temperature changes were approximately 94.23 K at a 400 K target, 102.91 K at 410 K, 111.47 K at 420 K, and 119.92 K at 430 K. This suggests a first-order or otherwise lagged thermal response rather than perfect setpoint tracking. A plausible process model is

dTvessel/dt = (Ttarget - Tvessel)/tau - Qloss(Tvessel)

with reaction rates depending on Tvessel rather than simply on the entered target. The available data do not reveal the initial absolute temperature, tau, heat-transfer coefficient, or reaction heat.

The byproduct result at 420 K was slightly lower than at 410 K, contrary to a perfectly smooth monotonic curve. I regard this as compatible with assay/process variability and coupled kinetics, not strong evidence for a sharp mechanistic reversal. The broader trend from 400 to 430 K supports increasing side-reaction burden.

6. Time-temperature coupling

Batches 9 and 11 compared 3300 versus 4500 s at a 400 K target:

- Batch 9, 3300 s: conversion 0.9054, yield 0.7488, selectivity 0.8198, byproduct 0.1679, degradation 0.1010, risk 0.1894, score 0.4442.
- Batch 11, 4500 s: conversion 0.9675, yield 0.7447, selectivity 0.7815, byproduct 0.2204, degradation 0.1242, risk 0.1896, score 0.4381.

The extra 1200 s substantially increased conversion but did not improve yield. Instead, selectivity decreased and the byproduct and degradation signals increased. This is strong local evidence for competitive or consecutive secondary chemistry: once most reactant is consumed, additional residence time increasingly benefits B or D rather than net P accumulation.

Risk changed by only 0.00024 between these two batches. Therefore, in this explored region, public risk appears much more sensitive to achieved temperature or peak thermal state than to the additional hold time. A simple local risk model could be

risk approximately setup_risk(reagent, solvent, amounts) + thermal_risk(maximum or terminal temperature)

rather than a pure time integral of thermal exposure. This is an empirical inference, not knowledge of the hidden scoring implementation.

Batch 12 combined a lower target, 395 K, with 4500 s. It gave conversion 0.9428, yield 0.7497, selectivity 0.7913, byproduct 0.2223, degradation 0.1219, risk 0.1700, and the campaign-best final score of 0.4489. Its observed temperature change was about 89.85 K. This condition traded some selectivity and byproduct performance relative to Batch 9 for more conversion while gaining a large safety advantage from the lower temperature.

7. Interpretation of the score optimum

The best final-assay score was Batch 12 at 0.4489, followed by Batch 9 at 0.4442, Batch 11 at 0.4381, and Batch 8 at 0.4375. All were comfortably below the risk limit.

This ranking implies a broad local optimum around 395-400 K using water and Catalyst B, with residence time adjusted to balance conversion against secondary chemistry. The optimum is not simply the maximum-yield condition: Batch 10 had higher yield (0.7866) than Batch 12 (0.7497) but a much lower score because its risk and byproduct burdens were higher. It is also not simply the lowest-risk condition; sufficient conversion remains necessary.

The recommended Batch 12 should therefore be viewed as the best observed compromise, not proof of the exact mathematical optimum. Batch 9 is a credible competing operating point: it had slightly lower score but higher selectivity and lower byproduct, with a shorter residence time.

8. Evolution of the explanation during the campaign

The supplied incomplete prior suggested that the lower-temperature side of the 420 K reference region would retain safer balanced performance. Batch 1 established that the reference recipe was productive but already carried appreciable risk (0.2858).

Batches 2-4 changed the initial explanation by showing that catalyst identity was a major kinetic/selectivity variable, with Catalyst B clearly superior. Batches 5-7 then showed that high conversion could be misleading: all three alternative solvents approached complete conversion but suffered much worse selectivity, byproduct formation, degradation, and risk. This motivated treating productive and nonproductive pathways separately.

Batches 8-10 confirmed the prior temperature direction. Lowering the target to 410 and 400 K improved score, whereas 430 K approached the safety constraint and reduced score. Batches 11-12 then clarified the time coupling: extra time recovered conversion at lower temperature but eventually shifted material toward byproduct/degradation. Batch 12 demonstrated that a lower-temperature/longer-time compromise could outperform the original reference.

9. Limits of identification

Several important factors remain unidentifiable:

- Only one reagent amount, solvent volume, catalyst loading, and stirring rate were studied. Reaction orders, dilution effects, catalyst saturation, and mass-transfer limitations cannot be estimated.
- Catalyst-by-solvent and catalyst-by-temperature interactions were not mapped. The catalyst ranking may change elsewhere.
- The thermal measurements exposed temperature changes, not a full time-resolved temperature trajectory. Heat-transfer constants and exothermicity remain unknown.
- Final assays are noisy synthetic measurements. Small differences, especially the 0.0047 score gap between Batches 12 and 9, should not be overinterpreted without replication.
- No replicate batches were run, so process variance cannot be separated cleanly from assay variance.
- HPLC and final-assay estimates sometimes differed. For example, Batch 12 HPLC reported score 0.4689 before termination, whereas its final score was 0.4489. The final assay is the appropriate basis for completed-batch comparison, but the discrepancy limits fine quantitative inference.
- The exact score and safety-risk equations are hidden. Any proposed formula is phenomenological.
- No species identities were public, so assignments such as P, B, and D denote functional roles only.

10. Reasonable competing explanations

The observations could also be explained without literal consecutive degradation of product. For example:

- Longer time may open a second parallel pathway from a slowly reacting subpopulation of reagent rather than converting P into D.
- The degradation-warning channel may be correlated with temperature or solvent state without representing direct loss of P.
- Solvent effects may alter instrument response factors as well as chemistry, although independent public calibration and the consistency across several output channels make a real process effect more plausible.
- Catalyst B may improve mass transfer or effective heat distribution rather than changing intrinsic chemical selectivity.
- The nearly duration-independent risk may be a peak-state safety metric rather than a mechanistic hazard accumulation model.

The current evidence favors a desired pathway competing with side formation and later secondary loss, but it cannot uniquely distinguish among these alternatives.

11. Final world model

Within the tested composition and local operating region, I would use the following qualitative predictor:

1. Add a solvent-specific setup-risk offset, ordered water < ethanol < acetonitrile < toluene.
2. Use catalyst-specific desired and side-path activity factors, with Catalyst B best, Catalyst D intermediate, and Catalysts A/C poorer under the tested conditions.
3. Increase total conversion with temperature and residence time toward saturation.
4. Decrease marginal selectivity as temperature or post-conversion residence time increases because side and degradation pathways become relatively more important.
5. Compute yield from the balance between conversion and selectivity, not from conversion alone.
6. Make thermal risk rise steeply with achieved/peak temperature and only weakly with additional hold time in this range.
7. Favor approximately 395-400 K in water with Catalyst B; use enough time for useful conversion but avoid unnecessary residence after conversion approaches its plateau.

This model is directly supported only near 395-430 K, 3300-4500 s, 0.003 mol reagent, 0.005 L solvent, 0.000525 mol catalyst, and 350 rpm. Predictions outside that region should be treated as extrapolations rather than established behavior.

## Q — Blind predictions

### Overall rationale

Predictions are anchored primarily to Batch 6, the exact Catalyst B/acetonitrile/420 K/3300 s reference observed during the campaign. Temperature and duration adjustments use the trends from water Batches 1 and 8-12: conversion rises toward saturation with thermal exposure, whereas excessive temperature or post-conversion residence increases side formation and reduces selectivity. Risk is modeled as a solvent-dependent setup contribution plus a strongly temperature-dependent terminal thermal contribution with comparatively weak direct duration dependence. Quenched and multistage procedures have wider intervals because neither quenching nor staged heating was experimentally calibrated. All intervals combine final-assay noise, batch variability, and model/extrapolation uncertainty; they are not confidence intervals for a fitted parametric law.

### Q01

This nearly reproduces Batch 6, apart from 400 rather than 350 rpm and a different addition order. Batch 6 gave conversion 0.9947, yield 0.6598, selectivity 0.6375, byproduct 0.3536, risk 0.3271, and score 0.3095. I expect little stirring effect in this range.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3540 | 0.3000 | 0.4100 |
| conversion | 0.9930 | 0.9600 | 1.0000 |
| safety_risk | 0.3270 | 0.2900 | 0.3600 |
| score | 0.3100 | 0.2600 | 0.3600 |
| selectivity | 0.6400 | 0.5800 | 0.7000 |
| yield | 0.6600 | 0.6000 | 0.7200 |

### Q02

The reaction history through heating matches Q01, so conversion and composition should be similar. I predict that quenching largely removes the terminal thermal-risk contribution while preserving products, but this operation was not tested during the campaign; the risk and score intervals are therefore deliberately wide.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3500 | 0.2900 | 0.4100 |
| conversion | 0.9920 | 0.9550 | 1.0000 |
| safety_risk | 0.1700 | 0.1200 | 0.2400 |
| score | 0.3750 | 0.3000 | 0.4500 |
| selectivity | 0.6420 | 0.5800 | 0.7100 |
| yield | 0.6610 | 0.6000 | 0.7300 |

### Q03

Lowering the target from 420 to 390 K should reduce conversion but improve pathway balance and sharply reduce thermal risk. This extrapolates the water temperature series to acetonitrile, so catalyst-solvent-temperature interaction uncertainty is included.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2850 | 0.2100 | 0.3600 |
| conversion | 0.8950 | 0.8000 | 0.9600 |
| safety_risk | 0.1800 | 0.1400 | 0.2300 |
| score | 0.3700 | 0.3000 | 0.4300 |
| selectivity | 0.7050 | 0.6300 | 0.7800 |
| yield | 0.6400 | 0.5500 | 0.7100 |

### Q04

This is a substantial high-temperature extrapolation. Acetonitrile already produced nearly complete conversion but poor selectivity at 420 K; 450 K should mainly increase side formation, degradation, and risk rather than useful conversion. The predicted risk exceeds the declared 0.35 limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4800 | 0.3800 | 0.5900 |
| conversion | 0.9980 | 0.9700 | 1.0000 |
| safety_risk | 0.4600 | 0.3900 | 0.5400 |
| score | 0.1900 | 0.1000 | 0.2900 |
| selectivity | 0.5300 | 0.4200 | 0.6400 |
| yield | 0.5600 | 0.4500 | 0.6600 |

### Q05

At 1500 s the vessel should spend much less time near the 420 K target than in Batch 6. I therefore expect incomplete conversion, less byproduct formation, better selectivity, and a lower terminal thermal risk, with yield limited by conversion.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2400 | 0.1600 | 0.3200 |
| conversion | 0.7800 | 0.6500 | 0.8800 |
| safety_risk | 0.1800 | 0.1400 | 0.2400 |
| score | 0.3400 | 0.2700 | 0.4100 |
| selectivity | 0.7300 | 0.6500 | 0.8000 |
| yield | 0.5700 | 0.4700 | 0.6600 |

### Q06

The longer hold should saturate conversion while allowing additional competitive or consecutive side chemistry. Batch 9 versus Batch 11 showed that added time increased conversion but reduced selectivity and increased byproduct; the same tendency should be stronger in acetonitrile.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4700 | 0.3800 | 0.5700 |
| conversion | 0.9990 | 0.9800 | 1.0000 |
| safety_risk | 0.3300 | 0.2900 | 0.3700 |
| score | 0.2500 | 0.1700 | 0.3300 |
| selectivity | 0.5400 | 0.4400 | 0.6300 |
| yield | 0.5800 | 0.4800 | 0.6700 |

### Q07

The first low-temperature stage permits some relatively selective conversion, but the second stage ends near a high thermal state and should drive further conversion and side reactions. The final hot stage is expected to give high terminal risk and a constraint-sensitive low score.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4300 | 0.3300 | 0.5400 |
| conversion | 0.9850 | 0.9300 | 1.0000 |
| safety_risk | 0.4300 | 0.3500 | 0.5100 |
| score | 0.2200 | 0.1200 | 0.3200 |
| selectivity | 0.5900 | 0.4900 | 0.6900 |
| yield | 0.6000 | 0.4900 | 0.7000 |

### Q08

Heating to 450 K first should irreversibly create substantial product and byproduct, so the later 390 K stage cannot restore selectivity. However, the second stage should cool the vessel and lower terminal safety risk relative to Q07. The interval allows for uncertainty over whether the public risk emphasizes terminal or peak temperature.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4400 | 0.3400 | 0.5500 |
| conversion | 0.9900 | 0.9400 | 1.0000 |
| safety_risk | 0.2400 | 0.1700 | 0.3200 |
| score | 0.3000 | 0.2100 | 0.3900 |
| selectivity | 0.5800 | 0.4800 | 0.6800 |
| yield | 0.6000 | 0.4900 | 0.7000 |

### Q09

The hotter target partially offsets the short 1500 s duration. Because of thermal lag, this should not resemble a full 440 K hold: I expect substantial but incomplete conversion, intermediate side formation, and terminal risk below the 420 K/3300 s acetonitrile batch.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3000 | 0.2100 | 0.3900 |
| conversion | 0.8700 | 0.7600 | 0.9500 |
| safety_risk | 0.2400 | 0.1800 | 0.3000 |
| score | 0.3500 | 0.2700 | 0.4200 |
| selectivity | 0.6800 | 0.5900 | 0.7600 |
| yield | 0.6100 | 0.5100 | 0.7000 |

### Q10

Chemistry should closely match Q09 because quenching occurs after the programmed heat. The quench is predicted to reduce terminal thermal risk and improve safe score, although its unmeasured effect makes these two predictions less certain than the composition estimates.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2970 | 0.2100 | 0.3900 |
| conversion | 0.8680 | 0.7500 | 0.9500 |
| safety_risk | 0.1600 | 0.1100 | 0.2300 |
| score | 0.3900 | 0.3100 | 0.4700 |
| selectivity | 0.6820 | 0.5900 | 0.7700 |
| yield | 0.6120 | 0.5100 | 0.7100 |

### Q11

The long hold should compensate partly for the low 370 K target while retaining low thermal risk. Conversion remains uncertain because this temperature lies below the investigated range. Acetonitrile's observed tendency toward side formation limits the expected selectivity advantage.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2750 | 0.1900 | 0.3700 |
| conversion | 0.8700 | 0.7300 | 0.9600 |
| safety_risk | 0.1500 | 0.1100 | 0.2100 |
| score | 0.3900 | 0.3100 | 0.4600 |
| selectivity | 0.7150 | 0.6200 | 0.8000 |
| yield | 0.6400 | 0.5300 | 0.7300 |

### Q12

This combines the highest target and longest duration and is far outside the experimentally supported safe region. Conversion should saturate, but extensive competitive and consecutive chemistry should lower selectivity and yield while raising byproduct and risk. The broad intervals reflect the long extrapolation and possible nonlinear thermal or safety behavior.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6400 | 0.4900 | 0.7800 |
| conversion | 1.0000 | 0.9850 | 1.0000 |
| safety_risk | 0.5800 | 0.4600 | 0.7000 |
| score | 0.1000 | 0.0200 | 0.2100 |
| selectivity | 0.3800 | 0.2400 | 0.5200 |
| yield | 0.4300 | 0.2800 | 0.5700 |

## K2 — Retrospective analysis

1. Assessment of the initial information

The initial material supplied one substantive directional claim: relative to the 420 K, 3300 s reference region, the lower-temperature side should retain safe, balanced performance more reliably than the higher-temperature side. It also warned that an observed temperature-bound rollback should count as evidence against the attempted condition rather than as missing output. The rest of the initial information mainly defined a reference context and emphasized that the model was incomplete; it did not provide a detailed kinetic mechanism, catalyst ranking, solvent ranking, or quantitative score law.

The lower-temperature claim was supported within the tested local region. Using Catalyst B and water for 3300 s, lowering the target from Batch 1 at 420 K to Batch 8 at 410 K and Batch 9 at 400 K reduced risk from 0.2858 to 0.2362 and 0.1894. Final score rose from 0.4152 to 0.4375 and 0.4442. Conversely, Batch 10 at 430 K raised risk to 0.3287 and reduced score to 0.3974. Thus the observed 400–430 K series supported both the safety direction and the claim of better balanced performance on the lower side.

This did not establish that score improves indefinitely as temperature decreases. Batch 12 showed that 395 K could work well when paired with 4500 s, but no isolated 395 K versus 400 K comparison at a common duration was made, and temperatures below 395 K were not tested. K1 appropriately described an approximate local preference around 395–400 K rather than a universal monotonic law.

The rollback claim remained untested. None of the campaign heat operations produced an observed temperature-bound rollback. Therefore there was neither support nor counterevidence for how rollback would behave. In the blind predictions, especially Q12 at 460 K for 6300 s, I effectively predicted a continuously evolving endpoint without assigning meaningful probability to rollback or operation failure. That was not a discovered contradiction, but it was an underuse of an explicit initial warning.

The initial model contained no substantive catalyst or solvent claims to confirm or refute. The catalyst and solvent conclusions in K1 came entirely from campaign observations. Likewise, the first-order thermal-response equation and the R-to-P/R-to-B/P-to-D network in K1 were my phenomenological interpretations, not claims supplied initially.

2. Experiments that formed or changed my judgments

Batch 1 established the practical baseline. It showed that the reference recipe was highly converting and productive but already carried appreciable risk: final conversion 0.9708, yield 0.7778, selectivity 0.8047, risk 0.2858, and score 0.4152. This converted the initial qualitative claim into a quantitative local anchor.

Batches 2–4 genuinely changed the catalyst model. At otherwise matched water/420 K/3300 s conditions, Catalyst B in Batch 1 clearly outperformed A, C, and D. The similar risks across Batches 1–4 indicated that the score differences were primarily chemical rather than safety-driven. Before those batches, choosing Catalyst B was mainly reliance on the supplied reference context; afterward, it was evidence-based.

Batches 5–7 produced another important revision. I had not initially established whether alternative solvents might improve conversion or score. Ethanol, acetonitrile, and toluene all gave very high conversion, but their selectivity, byproduct, degradation, risk, and score were worse than water. These experiments caused me to separate total conversion from productive conversion and motivated the competing-pathway interpretation in K1. They also established a solvent-associated risk ordering in the tested context.

Batches 8–10 were the cleanest test of the initial directional temperature claim. Their results shifted the optimization focus from the 420 K reference toward approximately 395–400 K. Batch 10 was particularly useful because it showed that a hotter condition could retain high yield while losing safe-score performance.

Batch 11 changed the time interpretation. Relative to Batch 9 at 400 K, extending the duration from 3300 to 4500 s increased conversion from 0.9054 to 0.9675 but left yield nearly unchanged, decreased selectivity from 0.8198 to 0.7815, and increased byproduct from 0.1679 to 0.2204. That was the strongest evidence behind K1's statement that extra residence after substantial conversion benefits secondary chemistry more than net product accumulation.

Batch 12 was primarily an optimization-driven combination rather than a clean mechanistic contrast: both target temperature and duration differed from Batch 9, and temperature differed from Batch 11. Its score of 0.4489 made it the best observed completed batch, but it did not independently identify the effects of 395 K and 4500 s.

Several experimental choices relied on unverified assumptions. Fixing reagent amount, solvent volume, catalyst loading, and stirring at the supplied reference values assumed that these controls were already reasonable. Testing all four catalysts and solvents was a broad categorical screen rather than a mechanistically optimized design. The choice of 400, 410, 420, and 430 K was strongly informed by the initial temperature claim. The later 4500 s trials relied on the untested guess that lower temperature could be compensated by longer duration. That guess was productive, but only partly isolated by the design.

3. Most important competing mechanisms and explanations

K1 favored a network with desired and competitive formation plus possible consecutive product degradation. The most important competitor is a purely parallel network in which different reactant populations or pathways produce target and byproduct at different rates, without appreciable P-to-D conversion. The Batch 9 versus Batch 11 comparison shows that longer time raises conversion while lowering apparent selectivity, but it cannot determine whether existing product is destroyed or whether the remaining reactant is intrinsically less selective.

A second competing explanation is that the degradation-warning signal is an empirical correlate of temperature, solvent, or byproduct composition rather than a direct measure of P-to-D chemistry. The warning increased in several harsher conditions, but the campaign did not establish mass closure among target, byproduct, and degradation channels.

A third ambiguity concerns solvent action. Water may genuinely favor kP/kB, but the observed solvent differences could combine kinetic effects, phase or transport behavior, and instrument-response differences. Independent synthetic calibration makes a wholly instrumental explanation less attractive, yet the campaign did not isolate solvent physical properties or run orthogonal material balances.

A fourth ambiguity concerns catalyst action. Catalyst B may alter intrinsic pathway rates, but it could instead improve mixing, catalyst availability, or coupling to the thermal state. Because catalyst loading and stirring were fixed, intrinsic kinetics and transport enhancement cannot be separated.

The experiments do distinguish several empirical facts: catalyst identity matters at the reference condition; water outperformed the three alternatives tested; added time at 400 K increased conversion but worsened selectivity/byproduct balance; and hotter targets increased observed risk. They do not distinguish parallel from consecutive side formation, terminal-temperature risk from peak-temperature risk, or intrinsic kinetic effects from transport effects.

K1 stated that risk appeared much more sensitive to achieved temperature than to the extra hold time, based on the near-identical risks of Batches 9 and 11. That conclusion is locally supported. However, the stronger claim that risk is governed by maximum or terminal temperature remains unresolved because the campaign used only single-stage heating and no quench. Q02, Q07, Q08, and Q10 required precisely this untested distinction.

4. One additional complete experiment

If one additional legal complete experiment were available, I would run Catalyst B in water with the established amounts and 350 rpm, heat at 400 K for 3300 s, take one HPLC measurement, continue at 400 K for another 1200 s, terminate, and perform the required final assay.

This design creates a within-vessel time contrast approximating the endpoints of Batches 9 and 11. It would not be perfect because the early observation would be HPLC and the endpoint would be final assay, but the existing paired HPLC/final-assay discrepancies from Batches 9 and 11 could at least inform the likely instrument offset. It would reduce independent-batch variability and directly test whether target signal declines, remains flat, or continues growing during the extra residence.

If conversion rose while absolute target yield or target signal fell and byproduct/degradation rose, the consecutive-loss interpretation would become substantially stronger. If conversion and target both rose but selectivity fell only because byproduct grew faster, a parallel competition model would be favored. If all composition metrics changed little, the Batch 9–11 difference would look more like batch or assay variability than robust time-dependent chemistry. If the within-batch behavior disagreed sharply with both earlier batches, confidence in the assumed reproducibility and in the recommended operating region would decrease.

A replicate of Batch 12 would be more directly valuable for validating the recommendation, and a matched quench experiment would be more valuable for the blind quench predictions. I chose the time-course experiment because it offers the greatest mechanistic discrimination from a single new completed batch.

5. Tradeoff between identifiability and operating score

The campaign deliberately mixed screening, mechanism-oriented comparisons, and optimization. Batches 2–4 and 5–7 sacrificed likely score to identify catalyst and solvent effects. Once Batch 1 showed that Catalyst B/water was promising, testing inferior catalysts and nonaqueous solvents was not score-maximizing, but it was essential for establishing that the reference choices were not arbitrary.

Batch 10 at 430 K likewise sacrificed expected safety margin to test the high-temperature side of the initial claim. It remained below the 0.35 limit, but its main value was directional evidence rather than operational performance.

After Batch 7, the design shifted toward optimization. Batches 8–10 located a better thermal region, and Batches 11–12 pursued temperature/time compensation. This improved the best observed score, but mechanistic identifiability suffered. In particular, Batch 12 changed both temperature and duration relative to Batch 9. A factorial set containing 395 and 400 K at both 3300 and 4500 s would have been more identifiable, but only two batches remained.

The research goal explicitly emphasized strong safe-score performance under the risk limit. That justified reserving later experiments for optimization rather than replication or an exhaustive kinetic design. It also encouraged selection of Batch 12 even though the score advantage over Batch 9 was small. Conversely, the categorical catalyst and solvent screens consumed seven of twelve batches and limited local replication. Thus there were sacrifices in both directions: early mechanistic breadth cost score opportunities, while late optimization cost clean factor isolation and replication.

6. Evidence not fully used and weaknesses in the blind predictions

The campaign obtained characterization artifacts and raw chromatographic information, but I relied almost entirely on processed estimates. Peak areas, widths, retention behavior, calibration metadata, and replicate-signal structure were not analyzed. Those data might have revealed saturation, unresolved peaks, or systematic differences between target and byproduct response.

The HPLC/final-assay pairs were also underused quantitatively. K1 acknowledged discrepancies—for example, Batch 12 had HPLC score 0.4689 and final score 0.4489—but I did not estimate an empirical cross-instrument bias or variance. With twelve pairs, even a rough model could have improved uncertainty calibration.

The observed temperature-change values supported thermal lag, but I did not formally fit a time constant. Such a fit would have been especially useful for the short and staged blind procedures. Similarly, cost and operation-order effects were not modeled. Every campaign batch added reagent before solvent, whereas all blind queries added solvent first. I treated that difference as minor in Q01, but no campaign evidence established order invariance.

The least reliable blind predictions are Q12, Q07, Q08, Q02, and Q10. Q12 combines 460 K and 6300 s, far beyond K1's stated 395–430 K and 3300–4500 s applicability range. Its conversion interval of 0.985–1.000 was probably too narrow because it neglected possible rollback, severe degradation, or other nonlinear behavior explicitly anticipated by the initial information.

Q07 and Q08 use staged heating, while the campaign used only single heat operations. Their predicted risk difference assumed that final temperature substantially controls public risk, but peak-risk retention could make them much more similar. Their risk and score intervals should probably have been wider.

Q02 and Q10 depend on quenching, which was never tested. I predicted large reductions in risk and increases in score while leaving composition almost unchanged. That is a plausible guess, not a campaign-supported relationship. The stated intervals acknowledged uncertainty but were still arguably too narrow, particularly for score.

Q04 at 450 K, Q11 at 370 K, and the short-duration Q05/Q09 cases also extrapolate outside the well-observed region. Q04's intervals were broad, but Q11's score and composition intervals may still understate low-temperature kinetic uncertainty. Q03 at 390 K is only a modest temperature extrapolation, yet it also transfers the water-derived temperature response to acetonitrile without evidence that the interaction is stable.

These weaknesses are consistent with K1's explicit scope restriction, but some numerical intervals did not fully honor that warning. In particular, the staged, quenched, extreme-temperature, and extreme-duration predictions should have included more model-form uncertainty rather than mainly assay-scale uncertainty. No prediction truth has been provided, so these are prospective critiques of calibration, not post hoc explanations of errors.

7. Limitations of the sealed recommendation

Batch 12 was the sample-in highest-scoring completed experiment, not a proven optimum. Its final score was 0.4489 versus 0.4442 for Batch 9, a difference of only 0.0047. That gap is smaller than the stated final-assay noise for several contributing channels and was observed without replication. It therefore does not establish that the Batch 12 procedure has a higher expected score than Batch 9.

The recommendation is also conditional on one composition, Catalyst B, water, the tested addition order, and 350 rpm. Catalyst loading, reagent concentration, solvent volume, stirring, order of addition, quenching, and heat-up profile were not optimized. The 395 K/4500 s combination was tested only once, so process variance and day- or world-level variability are unknown.

Repeatability should first be tested with multiple independent replications of Batch 12, including final assays and preferably matched intermediate HPLC measurements. Batch 9 should be replicated in parallel because it is a statistically credible competing recommendation with shorter processing time, higher observed selectivity, and lower byproduct.

Local robustness should then be tested with a small response-surface design around roughly 392.5–402.5 K and 3900–5100 s. Perturbations in catalyst loading, solvent volume, stirring speed, and addition order would reveal whether Batch 12 lies on a broad plateau or a narrow ridge. Safety robustness should include modest setpoint overshoot and thermal-lag variation while preserving a margin below 0.35.

Cross-material generalization would require repeating the local thermal comparison with at least Catalyst D and possibly another solvent; the present evidence does not show that the same temperature/time optimum applies outside Catalyst B/water. Cross-world generalization would require independent simulator worlds, seeds, or campaign instances because all observations came from one world realization.

Accordingly, the sealed recommendation should be described as the best observed member of a twelve-batch sample, with an attractive safety margin, rather than as a globally or even locally proven optimum.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 93.1 | none | 0 |
| Q | yes | 0 | 104.2 | none | 0 |
| K2 | yes | 0 | 107.5 | none | 0 |

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean 80% width | Mean interval score |
|---|---:|---:|---:|---:|
| byproduct_signal | 0.0494 | 0.8500 | 0.1825 | 0.2149 |
| conversion | 0.0559 | 0.5833 | 0.1075 | 0.2886 |
| safety_risk | 0.0503 | 0.7500 | 0.1250 | 0.3049 |
| score | 0.0339 | 0.9833 | 0.1583 | 0.1584 |
| selectivity | 0.0501 | 0.7000 | 0.1808 | 0.2369 |
| yield | 0.0735 | 0.7500 | 0.1917 | 0.4172 |

## Predictions versus released reference truth

### Q01

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3540 | 0.3000 | 0.4100 | 0.3661 | 0.3711, 0.3582, 0.3829, 0.3546, 0.3637 |
| conversion | 0.9930 | 0.9600 | 1.0000 | 0.9983 | 1.0000, 1.0000, 1.0000, 0.9986, 0.9928 |
| safety_risk | 0.3270 | 0.2900 | 0.3600 | 0.3271 | 0.3271, 0.3271, 0.3271, 0.3271, 0.3271 |
| score | 0.3100 | 0.2600 | 0.3600 | 0.3117 | 0.3089, 0.3133, 0.3128, 0.3125, 0.3110 |
| selectivity | 0.6400 | 0.5800 | 0.7000 | 0.6454 | 0.6395, 0.6416, 0.6482, 0.6527, 0.6453 |
| yield | 0.6600 | 0.6000 | 0.7200 | 0.6395 | 0.6358, 0.6456, 0.6401, 0.6368, 0.6391 |
### Q02

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3500 | 0.2900 | 0.4100 | 0.3678 | 0.3770, 0.3726, 0.3588, 0.3768, 0.3536 |
| conversion | 0.9920 | 0.9550 | 1.0000 | 0.9992 | 1.0000, 1.0000, 0.9960, 1.0000, 1.0000 |
| safety_risk | 0.1700 | 0.1200 | 0.2400 | 0.1558 | 0.1558, 0.1558, 0.1558, 0.1558, 0.1558 |
| score | 0.3750 | 0.3000 | 0.4500 | 0.3843 | 0.3838, 0.3841, 0.3876, 0.3844, 0.3815 |
| selectivity | 0.6420 | 0.5800 | 0.7100 | 0.6378 | 0.6410, 0.6229, 0.6441, 0.6452, 0.6359 |
| yield | 0.6610 | 0.6000 | 0.7300 | 0.6412 | 0.6377, 0.6497, 0.6463, 0.6367, 0.6353 |
### Q03

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2850 | 0.2100 | 0.3600 | 0.3044 | 0.3118, 0.2995, 0.2990, 0.3073, 0.3044 |
| conversion | 0.8950 | 0.8000 | 0.9600 | 0.9949 | 1.0000, 0.9882, 0.9993, 0.9868, 1.0000 |
| safety_risk | 0.1800 | 0.1400 | 0.2300 | 0.1950 | 0.1950, 0.1950, 0.1950, 0.1950, 0.1950 |
| score | 0.3700 | 0.3000 | 0.4300 | 0.4036 | 0.4011, 0.4007, 0.4038, 0.4111, 0.4016 |
| selectivity | 0.7050 | 0.6300 | 0.7800 | 0.6944 | 0.6873, 0.6875, 0.6946, 0.7114, 0.6911 |
| yield | 0.6400 | 0.5500 | 0.7100 | 0.6910 | 0.6879, 0.6895, 0.6901, 0.7010, 0.6867 |
### Q04

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4800 | 0.3800 | 0.5900 | 0.4313 | 0.4386, 0.4318, 0.4285, 0.4243, 0.4336 |
| conversion | 0.9980 | 0.9700 | 1.0000 | 0.9955 | 1.0000, 0.9995, 1.0000, 1.0000, 0.9781 |
| safety_risk | 0.4600 | 0.3900 | 0.5400 | 0.4212 | 0.4212, 0.4212, 0.4212, 0.4212, 0.4212 |
| score | 0.1900 | 0.1000 | 0.2900 | 0.2325 | 0.2360, 0.2291, 0.2318, 0.2346, 0.2309 |
| selectivity | 0.5300 | 0.4200 | 0.6400 | 0.5807 | 0.5940, 0.5696, 0.5798, 0.5793, 0.5809 |
| yield | 0.5600 | 0.4500 | 0.6600 | 0.5884 | 0.5878, 0.5859, 0.5861, 0.5936, 0.5887 |
### Q05

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2400 | 0.1600 | 0.3200 | 0.1919 | 0.1999, 0.1936, 0.1956, 0.1847, 0.1857 |
| conversion | 0.7800 | 0.6500 | 0.8800 | 0.9641 | 0.9653, 0.9636, 0.9659, 0.9650, 0.9609 |
| safety_risk | 0.1800 | 0.1400 | 0.2400 | 0.3273 | 0.3273, 0.3273, 0.3273, 0.3273, 0.3273 |
| score | 0.3400 | 0.2700 | 0.4100 | 0.4064 | 0.4049, 0.4081, 0.4049, 0.4106, 0.4033 |
| selectivity | 0.7300 | 0.6500 | 0.8000 | 0.8032 | 0.8034, 0.8204, 0.7967, 0.8219, 0.7738 |
| yield | 0.5700 | 0.4700 | 0.6600 | 0.7825 | 0.7786, 0.7763, 0.7826, 0.7812, 0.7941 |
### Q06

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4700 | 0.3800 | 0.5700 | 0.5074 | 0.5074, 0.5103, 0.5024, 0.5104, 0.5064 |
| conversion | 0.9990 | 0.9800 | 1.0000 | 0.9997 | 1.0000, 1.0000, 0.9987, 1.0000, 1.0000 |
| safety_risk | 0.3300 | 0.2900 | 0.3700 | 0.3268 | 0.3268, 0.3268, 0.3268, 0.3268, 0.3268 |
| score | 0.2500 | 0.1700 | 0.3300 | 0.2221 | 0.2215, 0.2177, 0.2267, 0.2202, 0.2244 |
| selectivity | 0.5400 | 0.4400 | 0.6300 | 0.5033 | 0.4978, 0.4899, 0.5120, 0.5071, 0.5098 |
| yield | 0.5800 | 0.4800 | 0.6700 | 0.5074 | 0.5094, 0.5047, 0.5138, 0.5001, 0.5090 |
### Q07

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4300 | 0.3300 | 0.5400 | 0.4056 | 0.3992, 0.4027, 0.3978, 0.4203, 0.4080 |
| conversion | 0.9850 | 0.9300 | 1.0000 | 0.9957 | 1.0000, 0.9892, 1.0000, 0.9894, 1.0000 |
| safety_risk | 0.4300 | 0.3500 | 0.5100 | 0.4329 | 0.4329, 0.4329, 0.4329, 0.4329, 0.4329 |
| score | 0.2200 | 0.1200 | 0.3200 | 0.2409 | 0.2417, 0.2395, 0.2409, 0.2380, 0.2446 |
| selectivity | 0.5900 | 0.4900 | 0.6900 | 0.6144 | 0.6243, 0.6129, 0.6092, 0.6034, 0.6225 |
| yield | 0.6000 | 0.4900 | 0.7000 | 0.6023 | 0.5969, 0.6014, 0.6043, 0.6034, 0.6053 |
### Q08

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4400 | 0.3400 | 0.5500 | 0.3999 | 0.4150, 0.4019, 0.3945, 0.4007, 0.3876 |
| conversion | 0.9900 | 0.9400 | 1.0000 | 0.9967 | 1.0000, 0.9900, 0.9935, 1.0000, 1.0000 |
| safety_risk | 0.2400 | 0.1700 | 0.3200 | 0.2015 | 0.2015, 0.2015, 0.2015, 0.2015, 0.2015 |
| score | 0.3000 | 0.2100 | 0.3900 | 0.3495 | 0.3550, 0.3465, 0.3441, 0.3457, 0.3562 |
| selectivity | 0.5800 | 0.4800 | 0.6800 | 0.6174 | 0.6125, 0.6215, 0.6070, 0.6070, 0.6390 |
| yield | 0.6000 | 0.4900 | 0.7000 | 0.6112 | 0.6271, 0.6029, 0.6049, 0.6074, 0.6138 |
### Q09

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3000 | 0.2100 | 0.3900 | 0.2157 | 0.2139, 0.2192, 0.2065, 0.2248, 0.2142 |
| conversion | 0.8700 | 0.7600 | 0.9500 | 0.9822 | 0.9779, 0.9743, 0.9871, 0.9816, 0.9901 |
| safety_risk | 0.2400 | 0.1800 | 0.3000 | 0.4014 | 0.4014, 0.4014, 0.4014, 0.4014, 0.4014 |
| score | 0.3500 | 0.2700 | 0.4200 | 0.3688 | 0.3704, 0.3654, 0.3661, 0.3703, 0.3717 |
| selectivity | 0.6800 | 0.5900 | 0.7600 | 0.7845 | 0.7914, 0.7629, 0.7803, 0.7954, 0.7923 |
| yield | 0.6100 | 0.5100 | 0.7000 | 0.7792 | 0.7799, 0.7863, 0.7739, 0.7764, 0.7795 |
### Q10

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2970 | 0.2100 | 0.3900 | 0.2145 | 0.2078, 0.2005, 0.2088, 0.2291, 0.2264 |
| conversion | 0.8680 | 0.7500 | 0.9500 | 0.9863 | 0.9887, 0.9803, 0.9816, 0.9811, 1.0000 |
| safety_risk | 0.1600 | 0.1100 | 0.2300 | 0.1883 | 0.1883, 0.1883, 0.1883, 0.1883, 0.1883 |
| score | 0.3900 | 0.3100 | 0.4700 | 0.4623 | 0.4647, 0.4590, 0.4625, 0.4649, 0.4606 |
| selectivity | 0.6820 | 0.5900 | 0.7700 | 0.7874 | 0.7957, 0.7843, 0.7856, 0.7886, 0.7828 |
| yield | 0.6120 | 0.5100 | 0.7100 | 0.7789 | 0.7791, 0.7741, 0.7815, 0.7858, 0.7740 |
### Q11

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2750 | 0.1900 | 0.3700 | 0.4056 | 0.3998, 0.4141, 0.4004, 0.4077, 0.4058 |
| conversion | 0.8700 | 0.7300 | 0.9600 | 0.9898 | 0.9902, 0.9783, 0.9875, 1.0000, 0.9929 |
| safety_risk | 0.1500 | 0.1100 | 0.2100 | 0.1568 | 0.1568, 0.1568, 0.1568, 0.1568, 0.1568 |
| score | 0.3900 | 0.3100 | 0.4600 | 0.3583 | 0.3600, 0.3543, 0.3578, 0.3581, 0.3614 |
| selectivity | 0.7150 | 0.6200 | 0.8000 | 0.6037 | 0.6056, 0.6084, 0.6044, 0.5914, 0.6089 |
| yield | 0.6400 | 0.5300 | 0.7300 | 0.5977 | 0.6005, 0.5876, 0.5965, 0.6024, 0.6014 |
### Q12

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.6400 | 0.4900 | 0.7800 | 0.6871 | 0.6912, 0.6734, 0.6842, 0.7000, 0.6867 |
| conversion | 1.0000 | 0.9850 | 1.0000 | 0.9967 | 0.9995, 0.9953, 0.9901, 1.0000, 0.9987 |
| safety_risk | 0.5800 | 0.4600 | 0.7000 | 0.4328 | 0.4328, 0.4328, 0.4328, 0.4328, 0.4328 |
| score | 0.1000 | 0.0200 | 0.2100 | 0.0681 | 0.0730, 0.0656, 0.0644, 0.0697, 0.0677 |
| selectivity | 0.3800 | 0.2400 | 0.5200 | 0.3424 | 0.3558, 0.3442, 0.3324, 0.3403, 0.3390 |
| yield | 0.4300 | 0.2800 | 0.5700 | 0.3454 | 0.3486, 0.3383, 0.3441, 0.3500, 0.3460 |

## Recommendation retest

- Selected source batch: `12`
- Retest exact replay verified: `True`
- Retest failure: `none`

| Metric | Selected source batch | Independent retest | Retest minus source |
|---|---:|---:|---:|
| byproduct_signal | 0.2223 | 0.2206 | -0.0017 |
| conversion | 0.9428 | 0.9570 | 0.0142 |
| cost | 0.6657 | 0.6657 | 0.0000 |
| degradation_warning | 0.1219 | 0.1334 | 0.0115 |
| safety_risk | 0.1700 | 0.1700 | 0.0000 |
| score | 0.4489 | 0.4479 | -0.0011 |
| selectivity | 0.7913 | 0.7837 | -0.0076 |
| virtual_spectrum_summary | 0.1772 | 0.1814 | 0.0042 |
| yield | 0.7497 | 0.7483 | -0.0014 |

## Scope note

This is the final sanitized report produced after all 60 source sessions and K1/Q/K2 chains were sealed. It includes released reference truth, blind-prediction evaluation, and the independent recommendation retest. Provider-private event streams, credentials, thread identifiers, and token accounting remain excluded.
