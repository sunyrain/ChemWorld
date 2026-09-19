# RX-W04--P--mechanism_discovery--Aligned

## Run summary

- World: `RX-W04`
- Locus: `P`
- Goal: `mechanism_discovery`
- Arm: `Aligned`
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

- Selected batch: `12`
- Rationale: Batch 12 gave the highest observed safe score (0.472), with good yield and selectivity and much lower safety risk after prompt quenching at the lower-temperature condition.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 420 K x 3300 s @ 350 rpm | no | 0.7690 | 0.8067 | 0.9747 | 0.2024 | 0.1080 | 0.2858 | 0.4126 |
| 2 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 390 K x 3300 s @ 350 rpm | no | 0.7267 | 0.8251 | 0.8904 | 0.1571 | 0.0627 | 0.1531 | 0.4515 |
| 3 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 405 K x 3300 s @ 350 rpm | no | 0.7555 | 0.8214 | 0.9261 | 0.1878 | 0.0846 | 0.2118 | 0.4393 |
| 4 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 435 K x 3300 s @ 350 rpm | no | 0.7782 | 0.7884 | 0.9762 | 0.1913 | 0.1307 | 0.3459 | 0.3848 |
| 5 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 420 K x 1800 s @ 350 rpm | no | 0.7370 | 0.8478 | 0.8379 | 0.1160 | 0.0431 | 0.2851 | 0.3979 |
| 6 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 420 K x 1800 s @ 350 rpm → 420 K x 3600 s @ 350 rpm | no | 0.7122 | 0.6878 | 0.9976 | 0.2958 | 0.2146 | 0.3245 | 0.3432 |
| 7 | S0 (0.0050 L) | 0.003000 mol | C0 (0.000525 mol) | 420 K x 3300 s @ 350 rpm | no | 0.5857 | 0.7110 | 0.8418 | 0.2413 | 0.1274 | 0.2847 | 0.3236 |
| 8 | S0 (0.0050 L) | 0.003000 mol | C2 (0.000525 mol) | 420 K x 3300 s @ 350 rpm | no | 0.6221 | 0.6998 | 0.8514 | 0.2325 | 0.0519 | 0.2845 | 0.3280 |
| 9 | S0 (0.0050 L) | 0.003000 mol | C3 (0.000525 mol) | 420 K x 3300 s @ 350 rpm | no | 0.6933 | 0.7716 | 0.8763 | 0.2006 | 0.0797 | 0.2851 | 0.3556 |
| 10 | S1 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 420 K x 3300 s @ 350 rpm | no | 0.6494 | 0.6639 | 0.9672 | 0.3399 | 0.1968 | 0.3088 | 0.3177 |
| 11 | S2 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 420 K x 3300 s @ 350 rpm | no | 0.6444 | 0.6459 | 1.0000 | 0.3598 | 0.2946 | 0.3271 | 0.3059 |
| 12 | S0 (0.0050 L) | 0.003000 mol | C1 (0.000525 mol) | 390 K x 3300 s @ 350 rpm | yes | 0.7250 | 0.8369 | 0.8659 | 0.1691 | 0.0904 | 0.1001 | 0.4719 |

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
    "byproduct_signal": 0.20236510038375854,
    "conversion": 0.9747275114059448,
    "cost": 0.6557000279426575,
    "degradation_warning": 0.10800524801015854,
    "safety_risk": 0.2858142554759979,
    "score": 0.4125736951828003,
    "selectivity": 0.8067219853401184,
    "virtual_spectrum_summary": 0.1599031686782837,
    "yield": 0.769017219543457
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 350,
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
  "end_step": 14,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.15705227851867676,
    "conversion": 0.8903537392616272,
    "cost": 0.6557000279426575,
    "degradation_warning": 0.06270183622837067,
    "safety_risk": 0.1531040370464325,
    "score": 0.45149555802345276,
    "selectivity": 0.8250612616539001,
    "virtual_spectrum_summary": 0.11459457874298096,
    "yield": 0.7266542315483093
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 350,
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
  "end_step": 21,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.18783074617385864,
    "conversion": 0.9260969161987305,
    "cost": 0.6557000279426575,
    "degradation_warning": 0.0845828577876091,
    "safety_risk": 0.21184282004833221,
    "score": 0.4392675459384918,
    "selectivity": 0.821424663066864,
    "virtual_spectrum_summary": 0.14136919379234314,
    "yield": 0.7555023431777954
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 350,
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
  "end_step": 28,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.19129090011119843,
    "conversion": 0.9762145280838013,
    "cost": 0.6557000279426575,
    "degradation_warning": 0.13066916167736053,
    "safety_risk": 0.3458949327468872,
    "score": 0.3847854733467102,
    "selectivity": 0.7884275317192078,
    "virtual_spectrum_summary": 0.1640111207962036,
    "yield": 0.7781996726989746
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
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1800,
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
    "byproduct_signal": 0.11595429480075836,
    "conversion": 0.8378550410270691,
    "cost": 0.6431999802589417,
    "degradation_warning": 0.043104421347379684,
    "safety_risk": 0.2851153016090393,
    "score": 0.3979029357433319,
    "selectivity": 0.8478060364723206,
    "virtual_spectrum_summary": 0.08317185193300247,
    "yield": 0.7369694709777832
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
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 350,
      "target_temperature_K": 420
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 350,
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
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.2957528829574585,
    "conversion": 0.9975747466087341,
    "cost": 0.6732000112533569,
    "degradation_warning": 0.2145981341600418,
    "safety_risk": 0.32453441619873047,
    "score": 0.34323495626449585,
    "selectivity": 0.6878175139427185,
    "virtual_spectrum_summary": 0.2592332363128662,
    "yield": 0.7122089862823486
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
  "end_step": 50,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.24132031202316284,
    "conversion": 0.8418189287185669,
    "cost": 0.4456999897956848,
    "degradation_warning": 0.1273898184299469,
    "safety_risk": 0.28465357422828674,
    "score": 0.3235616385936737,
    "selectivity": 0.7110055685043335,
    "virtual_spectrum_summary": 0.1900515854358673,
    "yield": 0.5857310891151428
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
  "end_step": 57,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.23252345621585846,
    "conversion": 0.8513934016227722,
    "cost": 0.529699981212616,
    "degradation_warning": 0.05193237587809563,
    "safety_risk": 0.28448230028152466,
    "score": 0.3279559016227722,
    "selectivity": 0.6998147964477539,
    "virtual_spectrum_summary": 0.1512574702501297,
    "yield": 0.6221247315406799
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
  "end_step": 64,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.2006252110004425,
    "conversion": 0.8763388395309448,
    "cost": 0.7397000193595886,
    "degradation_warning": 0.07973717898130417,
    "safety_risk": 0.28508272767066956,
    "score": 0.3555912971496582,
    "selectivity": 0.7715994119644165,
    "virtual_spectrum_summary": 0.14622558653354645,
    "yield": 0.6932869553565979
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
  "end_step": 71,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.33987072110176086,
    "conversion": 0.9671955108642578,
    "cost": 0.6577000021934509,
    "degradation_warning": 0.19684012234210968,
    "safety_risk": 0.30880019068717957,
    "score": 0.31773561239242554,
    "selectivity": 0.663922905921936,
    "virtual_spectrum_summary": 0.2755069434642792,
    "yield": 0.649413526058197
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
      "volume_L": 0.005
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
  "end_step": 78,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.35984551906585693,
    "conversion": 1.0,
    "cost": 0.6608999967575073,
    "degradation_warning": 0.29460424184799194,
    "safety_risk": 0.3271262049674988,
    "score": 0.3059138059616089,
    "selectivity": 0.645851194858551,
    "virtual_spectrum_summary": 0.3304869532585144,
    "yield": 0.6443695425987244
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
      "solvent": 0,
      "volume_L": 0.005
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
      "stirring_speed_rpm": 350,
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
  "end_step": 86,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.16913120448589325,
    "conversion": 0.8659136295318604,
    "cost": 0.689125657081604,
    "degradation_warning": 0.09036065638065338,
    "safety_risk": 0.10007365047931671,
    "score": 0.4718634784221649,
    "selectivity": 0.8369078040122986,
    "virtual_spectrum_summary": 0.1336844563484192,
    "yield": 0.7249772548675537
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

1. Scope and evidence base

This account concerns only the bounded synthetic reaction world that was studied. The reagent and catalysts are anonymous benchmark entities, and the documented solvent effects are categorical benchmark effects rather than predictions from ordinary real-solvent properties. I completed 12 batches, each containing 0.003 mol reagent, 0.005 L solvent, and 0.000525 mol catalyst. Unless stated otherwise, the mixture was stirred at 350 rpm. Each batch received one HPLC measurement and a final assay. Final-assay values below are direct observations; mechanistic interpretations and extrapolations are explicitly identified as such.

2. Proposed reaction network

The smallest network consistent with the results is a desired reaction competing with both direct byproduct formation and subsequent product degradation:

R → P                 desired target formation
R → B                 competing conversion
P → D                 secondary degradation or conversion

A useful kinetic representation is:

dR/dt = −[kP(T,C,S,a) + kB(T,C,S,a)]R

dP/dt = kP(T,C,S,a)R − kD(T,C,S,a)P

dB/dt = kB(T,C,S,a)R

dD/dt = kD(T,C,S,a)P

Here T is actual temperature rather than merely the requested set point, C is catalyst identity, S is solvent category, and a is an optional catalyst-activity state. A plausible parameterization is

kj = Aj f_j(C) g_j(S) a_j(t) exp[−Ej/(RTactual)].

This form is not uniquely identified by the data. It is a compact explanation for three robust observations: conversion increases with thermal exposure, selectivity falls at excessive temperature or time, and catalyst and solvent identities affect target and side-product channels differently.

A catalyst-deactivation extension could use da/dt = −kd(T,S)a. However, the campaign did not directly measure catalyst activity or reuse a catalyst. Consequently, deactivation is only a possible contributor. Substrate depletion, product degradation, and a changing product/reactant ratio can explain the late-time behavior without deactivation.

3. Thermal process

The requested temperature is not identical to the realized thermal state. The public heat-operation telemetry reported actual temperature changes. For nominal 3300 s heats, the observed rises were approximately 85.45 K at a 390 K request (batch 2), 98.58 K at 405 K (batch 3), 111.47 K at 420 K (batches 1 and 7–11), and 124.11 K at 435 K (batch 4). Thus the response was systematic but lagged or offset from the set point.

A conceptual thermal equation is

dT/dt = (Tset − T)/τheat − qloss(T),

with operation-dependent stopping and possible discontinuities at a new heat or quench operation. I cannot identify τheat uniquely. In particular, batch 6 showed that operation segmentation matters: its first 1800 s heat at 420 K raised temperature by 111.48 K, while a second 3600 s heat added another 7.53 K. A single smooth first-order fit is therefore not justified from these data alone; the simulator may include staged controller behavior or an operation-specific approach limit.

Safety risk was strongly coupled to thermal state. With the otherwise identical water/Catalyst B/3300 s recipe, final risk rose from 0.1531 at 390 K (batch 2), to 0.2118 at 405 K (batch 3), 0.2858 at 420 K (batch 1), and 0.3459 at 435 K (batch 4). The last result approached the stated 0.35 safety limit. This confirms the supplied prior that the lower-temperature side is safer. It also shows that nominal temperature should not be used without accounting for actual thermal history.

4. Temperature dependence of chemistry

Final assays for the temperature series were:

• Batch 2, 390 K for 3300 s: conversion 0.8904, yield 0.7267, selectivity 0.8251, byproduct 0.1571, degradation warning 0.0627, risk 0.1531, score 0.4515.
• Batch 3, 405 K for 3300 s: conversion 0.9261, yield 0.7555, selectivity 0.8214, byproduct 0.1878, degradation warning 0.0846, risk 0.2118, score 0.4393.
• Batch 1, 420 K for 3300 s: conversion 0.9747, yield 0.7690, selectivity 0.8067, byproduct 0.2024, degradation warning 0.1080, risk 0.2858, score 0.4126.
• Batch 4, 435 K for 3300 s: conversion 0.9762, yield 0.7782, selectivity 0.7884, byproduct 0.1913, degradation warning 0.1307, risk 0.3459, score 0.3848.

Increasing temperature therefore accelerates consumption of R, but conversion nearly saturates by the 420 K condition. Beyond that point, the incremental target yield is small, while selectivity, degradation warning, safety, and the combined score worsen. The monotonic decline in selectivity and rise in degradation warning suggest that the undesired channel has a larger effective temperature sensitivity than the desired channel, or that hotter operation accelerates P → D. The data cannot distinguish these explanations uniquely.

The observed yield is not exactly conversion multiplied by selectivity. These are separately calibrated synthetic channels with stated measurement noise, so exact algebraic mass-balance identities should not be imposed on their point estimates.

5. Time dependence and late-stage loss of target

The time series at nominal 420 K with Catalyst B in water was especially diagnostic:

• Batch 5, 1800 s: conversion 0.8379, yield 0.7370, selectivity 0.8478, byproduct 0.1160, degradation warning 0.0431.
• Batch 1, 3300 s: conversion 0.9747, yield 0.7690, selectivity 0.8067, byproduct 0.2024, degradation warning 0.1080.
• Batch 6, 5400 s total in two heat operations: conversion 0.9976, yield 0.7122, selectivity 0.6878, byproduct 0.2958, degradation warning 0.2146.

The batch 6 HPLC measurement after its first 1800 s segment gave conversion 0.8376, yield 0.7146, selectivity 0.8714, and byproduct 0.1242. This closely reproduces the independent 1800 s batch 5 HPLC result: conversion 0.8330, yield 0.7354, selectivity 0.8682, and byproduct 0.0981. After the additional heat in batch 6, conversion approached completion but final yield fell and both byproduct and degradation signals increased substantially.

This is strong evidence against a simple irreversible R → P model. The target has a finite optimal residence time. Early heating mainly forms P; prolonged heating increasingly converts remaining R through competing pathways and/or consumes P through P → D. A qualitative stopping rule is therefore to stop near the point where

kP R ≈ kD P,

because beyond that point the instantaneous net production rate of P becomes small or negative. The available observations locate that crossover somewhere between the 3300 s and 5400 s exposures under the 420 K water/Catalyst B condition, but they do not determine it precisely.

6. Catalyst effects

At nominal 420 K for 3300 s in water, the final assays were:

• Catalyst A, batch 7: conversion 0.8418, yield 0.5857, selectivity 0.7110, byproduct 0.2413, degradation warning 0.1274.
• Catalyst B, batch 1: conversion 0.9747, yield 0.7690, selectivity 0.8067, byproduct 0.2024, degradation warning 0.1080.
• Catalyst C, batch 8: conversion 0.8514, yield 0.6221, selectivity 0.6998, byproduct 0.2325, degradation warning 0.0519.
• Catalyst D, batch 9: conversion 0.8763, yield 0.6933, selectivity 0.7716, byproduct 0.2006, degradation warning 0.0797.

Catalyst B was clearly the best of the four at this condition: it gave the highest conversion, yield, and selectivity. Catalyst D was second. Catalysts A and C were substantially less productive and less selective. Catalyst C had the lowest degradation warning, but that did not compensate for its poor conversion and selectivity. This pattern implies that catalyst identity changes more than a single common rate multiplier: the relative factors fP(C), fB(C), and possibly fD(C) differ.

No catalyst-free batch or catalyst-loading series was run, so absolute catalytic acceleration, rate order in catalyst, saturation, and catalyst lifetime remain unidentified. The late decline in batch 6 could include Catalyst B deactivation, but it could equally be caused by P degradation or depletion of R. The evidence supports catalyst-specific activity/selectivity, not a uniquely identified molecular catalytic mechanism.

7. Solvent-category coupling

At nominal 420 K for 3300 s with Catalyst B:

• Water, batch 1: conversion 0.9747, yield 0.7690, selectivity 0.8067, byproduct 0.2024, degradation warning 0.1080, risk 0.2858.
• Ethanol, batch 10: conversion 0.9672, yield 0.6494, selectivity 0.6639, byproduct 0.3399, degradation warning 0.1968, risk 0.3088.
• Acetonitrile, batch 11: conversion reported at the upper bound of 1.0000, yield 0.6444, selectivity 0.6459, byproduct 0.3598, degradation warning 0.2946, risk 0.3271.

Water was markedly more selective and productive. Ethanol and acetonitrile maintained or increased overall conversion but diverted much more material toward undesired channels. Acetonitrile was the most severe case; its conversion estimate was clipped at 1.0, so its exact unconstrained value is unavailable. These results support solvent-dependent gP, gB, and gD factors rather than a solvent effect acting only on total reaction speed.

Toluene was not tested, so nothing empirical can be claimed for that category. Because the environment explicitly defines these as categorical benchmark effects, interpreting the trend through real polarity, proticity, boiling point, or named chemical interactions would be speculation.

8. Quench and termination

Batch 12 repeated the lower-temperature water/Catalyst B condition—390 K for 3300 s—but added a quench before termination. Its final assay was conversion 0.8659, yield 0.7250, selectivity 0.8369, byproduct 0.1691, degradation warning 0.0904, risk 0.1001, and score 0.4719. This was the highest score observed.

The direct non-quenched comparator, batch 2, gave conversion 0.8904, yield 0.7267, selectivity 0.8251, byproduct 0.1571, degradation warning 0.0627, risk 0.1531, and score 0.4515. The nearly identical yields and modest differences among chemical channels should not be overinterpreted from one replicate per treatment and different noisy assay realizations. In particular, the higher degradation-warning point estimate in the quenched batch does not establish that quenching caused degradation.

The clear effect was on reported safety risk: prompt quenching reduced it from 0.1531 to 0.1001 under matched nominal reaction conditions. My interpretation is that quenching rapidly removes the hot/reactive state and arrests further evolution. The evidence supports quenching as a safety and state-freezing operation; it does not prove that quenching intrinsically increases chemical yield.

Termination without a preceding quench appears to freeze the chemical state for assay, but HPLC and final-assay differences cannot be treated as time evolution because they are different instruments with independent calibrations and noise. For example, batch 1 HPLC gave conversion 0.9639, yield 0.7489, selectivity 0.8275, and byproduct 0.1918, whereas its final assay gave 0.9747, 0.7690, 0.8067, and 0.2024. Those differences are compatible with measurement variation and channel calibration.

9. How the evidence changed the explanation

The supplied initial model predicted that the lower-temperature side would retain safe balanced performance. Batches 2–4 confirmed the safety direction very strongly. The chemistry results then refined that prior: higher temperature does increase conversion and initially increases target yield, but it simultaneously activates undesired conversion and degradation. Thus the relevant optimum is not maximum conversion or maximum temperature.

The comparison of batches 5, 1, and 6 changed the model from a mainly parallel-pathway account to a parallel-plus-sequential account. The fall in yield from 0.7690 at 3300 s to 0.7122 at 5400 s despite conversion increasing from 0.9747 to 0.9976 is particularly difficult to explain without target loss or an equivalent late-forming impurity pathway.

The catalyst comparison showed that Catalyst B changes both activity and selectivity, rather than merely producing a universal speed-up. The solvent comparison similarly showed that high conversion can coexist with poor yield and selectivity. Finally, batch 12 demonstrated that thermal termination strategy is an independent control lever: reaction conditions determine the chemical state, while quenching strongly influences residual safety risk and likely prevents post-reaction drift.

10. Practical predictive account within the studied domain

Within the tested recipe scale, a reasonable qualitative simulator is:

1. Update actual T from the requested heat operation using a lagged, operation-dependent thermal response.
2. At each time increment, compute catalyst- and solvent-specific desired, byproduct, and degradation rates.
3. Consume R through desired and competing channels.
4. Form P initially, but allow P loss to grow important at long time and high temperature.
5. On quench, rapidly reduce the reactive thermal state and set subsequent kinetic rates near zero.
6. On termination, freeze composition for the final assay.
7. Compute safety chiefly from peak/current thermal-reactive state, with additional solvent and prolonged-exposure contributions.

Qualitative predictions supported by interpolation are: lowering the nominal temperature from 420 K toward 390–405 K should sacrifice some conversion while improving safety and usually selectivity; extending the 420 K process substantially beyond 3300 s should increase conversion but reduce target yield; Catalyst B should outperform the other tested catalysts near the reference recipe; ethanol or acetonitrile should worsen selectivity relative to water; and prompt quenching should reduce terminal safety risk.

These are local predictions. I would not extrapolate them to different concentrations, catalyst loadings, stirring regimes, scales, or untested solvents without new evidence.

11. Remaining uncertainties and competing explanations

The following factors remain unidentifiable from the campaign:

• Direct R → B versus P → B/D: both can lower selectivity, and only aggregate byproduct/degradation channels were observed.
• Catalyst deactivation versus substrate depletion or product degradation: no catalyst-activity measurement, reuse test, or loading series was performed.
• Exact Arrhenius parameters and reaction orders: four temperatures and three principal time exposures are insufficient, especially because actual temperature histories were not constant ideal isotherms.
• Mixing effects: stirring was fixed at 350 rpm, so transport limitation cannot be separated from intrinsic kinetics.
• Concentration and dilution effects: reagent, catalyst, and solvent amounts were held fixed.
• Quench chemistry versus thermal arrest: batch 12 establishes a lower-risk endpoint but not the microscopic cause or a reproducible chemical-composition benefit.
• Instrument offsets: intermediate HPLC and final-assay values are separately calibrated noisy observations, not interchangeable measurements.
• Replicate variability: there was only one final replicate for each designed condition.
• Toluene behavior: unmeasured.

A reasonable competing model is a purely parallel network whose selectivity changes with conversion because catalyst states or medium composition evolve, without literal degradation of P. Another is a catalyst-deactivation model in which the desired pathway loses activity faster than the undesired pathway. Both could reproduce declining late selectivity. I favor explicit P → D because batch 6 showed decreasing target yield during continued conversion, but the evidence does not uniquely prove it.

Overall, the world behaves like a thermally activated, catalyst- and solvent-selective reaction with a finite target-yield window. Excess temperature or residence time pushes the system toward byproduct and degradation channels, while the realized thermal trajectory—not only the programmed set point—controls both chemistry and safety. In the studied region, the most defensible operational pattern is Catalyst B in water, moderate-to-low temperature, limited residence time, and prompt quenching.

## Q — Blind predictions

### Overall rationale

Predictions are based on the observed acetonitrile/Catalyst B result in batch 11, the water temperature series in batches 2, 3, 1, and 4, the time series in batches 5, 1, and 6, and the quench comparison between batches 2 and 12. I treated actual chemistry as a desired pathway competing with direct byproduct formation and late target degradation. Temperature, duration, solvent, operation order, and quenching were propagated qualitatively through that model. Intervals include final-assay noise plus larger structural uncertainty for untested temperatures, staged heating, 400 rpm stirring, and high-temperature quenching. Estimates are bounded to the public metric range [0,1].

### Q01

This closely matches acetonitrile batch 11 at 420 K for 3300 s. The change from 350 to 400 rpm was not experimentally identified, so I predict only a small net effect and include it as model uncertainty.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3570 | 0.3200 | 0.4000 |
| conversion | 0.9950 | 0.9700 | 1.0000 |
| safety_risk | 0.3290 | 0.3000 | 0.3600 |
| score | 0.3080 | 0.2700 | 0.3500 |
| selectivity | 0.6480 | 0.6100 | 0.6900 |
| yield | 0.6480 | 0.6100 | 0.6900 |

### Q02

The chemical endpoint should be similar to Q01, while quenching should substantially lower residual thermal risk. The estimated risk reduction is extrapolated from the matched water comparison between batches 2 and 12.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3550 | 0.3100 | 0.4000 |
| conversion | 0.9950 | 0.9700 | 1.0000 |
| safety_risk | 0.2550 | 0.2100 | 0.3000 |
| score | 0.3420 | 0.3000 | 0.3900 |
| selectivity | 0.6500 | 0.6100 | 0.7000 |
| yield | 0.6500 | 0.6100 | 0.7000 |

### Q03

Lower temperature should reduce conversion relative to Q01 but improve selectivity and suppress byproduct formation. Acetonitrile is still expected to remain less selective than water at the same temperature.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2850 | 0.2300 | 0.3500 |
| conversion | 0.9350 | 0.8800 | 0.9800 |
| safety_risk | 0.1950 | 0.1600 | 0.2300 |
| score | 0.3850 | 0.3300 | 0.4400 |
| selectivity | 0.7150 | 0.6600 | 0.7700 |
| yield | 0.6650 | 0.6000 | 0.7200 |

### Q04

This extrapolates 15 K beyond the highest temperature tested. Conversion should be effectively complete, but the temperature-sensitive competing and degradation channels should reduce yield and selectivity and push risk above the stated safety limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4550 | 0.3600 | 0.5500 |
| conversion | 0.9980 | 0.9700 | 1.0000 |
| safety_risk | 0.4200 | 0.3600 | 0.4900 |
| score | 0.2120 | 0.1200 | 0.3000 |
| selectivity | 0.5550 | 0.4600 | 0.6400 |
| yield | 0.5550 | 0.4500 | 0.6500 |

### Q05

Short exposure should preserve selectivity and limit byproduct formation, while leaving appreciable unconverted reagent. The thermal-risk estimate remains near the 420 K baseline because observed risk was more sensitive to achieved temperature than to moderate changes in duration.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2550 | 0.2000 | 0.3200 |
| conversion | 0.8750 | 0.8000 | 0.9400 |
| safety_risk | 0.3250 | 0.2900 | 0.3600 |
| score | 0.3220 | 0.2700 | 0.3800 |
| selectivity | 0.7450 | 0.6800 | 0.8100 |
| yield | 0.6500 | 0.5900 | 0.7100 |

### Q06

Long exposure should drive conversion to its upper bound while allowing substantial competing conversion and target degradation. This follows the pronounced late-time yield and selectivity loss observed in batch 6, augmented by acetonitrile's adverse solvent effect.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4900 | 0.4000 | 0.5800 |
| conversion | 1.0000 | 0.9800 | 1.0000 |
| safety_risk | 0.3600 | 0.3200 | 0.4100 |
| score | 0.2180 | 0.1300 | 0.3000 |
| selectivity | 0.5150 | 0.4000 | 0.6200 |
| yield | 0.5250 | 0.4200 | 0.6200 |

### Q07

The low-temperature first stage should form target relatively selectively, but the following 450 K stage can consume target and generate byproduct. Ending on the hot stage is also expected to leave high terminal risk.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4250 | 0.3300 | 0.5300 |
| conversion | 0.9950 | 0.9500 | 1.0000 |
| safety_risk | 0.4300 | 0.3600 | 0.5000 |
| score | 0.2250 | 0.1300 | 0.3200 |
| selectivity | 0.5850 | 0.4800 | 0.6800 |
| yield | 0.5900 | 0.4900 | 0.6800 |

### Q08

The early hot stage should cause irreversible side reaction, but the final 390 K stage should produce a substantially safer terminal thermal state than Q07. Chemical ordering effects were not directly tested, so the chemistry intervals are broad.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4000 | 0.3100 | 0.5000 |
| conversion | 0.9900 | 0.9400 | 1.0000 |
| safety_risk | 0.2500 | 0.1900 | 0.3200 |
| score | 0.3180 | 0.2300 | 0.4000 |
| selectivity | 0.6100 | 0.5100 | 0.7000 |
| yield | 0.6150 | 0.5100 | 0.7100 |

### Q09

A short 440 K treatment should give high but not necessarily complete conversion. Short residence time preserves more selectivity than a long hot treatment, although acetonitrile and the high terminal temperature still produce considerable byproduct and risk.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3500 | 0.2700 | 0.4400 |
| conversion | 0.9500 | 0.8800 | 0.9900 |
| safety_risk | 0.3950 | 0.3400 | 0.4600 |
| score | 0.2640 | 0.1800 | 0.3500 |
| selectivity | 0.6500 | 0.5600 | 0.7400 |
| yield | 0.6200 | 0.5300 | 0.7000 |

### Q10

Quenching should leave the chemical outcome close to Q09 while reducing residual thermal risk. The magnitude of this high-temperature quench effect is extrapolated and is therefore assigned a wider interval.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3450 | 0.2600 | 0.4300 |
| conversion | 0.9500 | 0.8800 | 0.9900 |
| safety_risk | 0.3000 | 0.2400 | 0.3600 |
| score | 0.3090 | 0.2300 | 0.3900 |
| selectivity | 0.6550 | 0.5600 | 0.7500 |
| yield | 0.6250 | 0.5300 | 0.7100 |

### Q11

The long duration should compensate substantially for the low temperature, while the cooler condition suppresses the most temperature-sensitive side reactions and risk. This is an extrapolation below the tested 390 K boundary, so kinetic uncertainty is appreciable.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2800 | 0.2000 | 0.3700 |
| conversion | 0.9400 | 0.8500 | 0.9900 |
| safety_risk | 0.1450 | 0.1000 | 0.2000 |
| score | 0.4120 | 0.3500 | 0.4700 |
| selectivity | 0.7200 | 0.6400 | 0.8000 |
| yield | 0.6750 | 0.5800 | 0.7500 |

### Q12

This combines a temperature above the explored range with a duration longer than any single uninterrupted heat studied. Conversion should saturate, while extensive competing conversion and target degradation produce low yield and selectivity, high byproduct signal, and severe safety risk.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6200 | 0.5000 | 0.7800 |
| conversion | 1.0000 | 0.9800 | 1.0000 |
| safety_risk | 0.5200 | 0.4500 | 0.6200 |
| score | 0.0510 | 0.0000 | 0.1600 |
| selectivity | 0.3200 | 0.1500 | 0.4700 |
| yield | 0.3400 | 0.1500 | 0.4800 |

## K2 — Retrospective analysis

1. Assessment of the initial information

The initial information contained one substantive directional claim: relative to the stated 420 K, 3300 s reference region, “the lower-temperature side should retain safe balanced performance more reliably than the higher-temperature side.” It also supplied a reference recipe—Catalyst B, 0.000525 mol catalyst, 0.003 mol reagent, 0.005 L water, and 350 rpm—but explicitly described the model as incomplete and potentially shifted. It did not supply a molecular identity, a rate law, activation parameters, catalyst ranking, solvent ranking, or a detailed mechanism. The material dossier was explicitly absent, so there were no meaningful real-chemical property claims to test.

The temperature claim was strongly supported for safety and overall score. With the otherwise matched reference recipe, batch 2 at 390 K had risk 0.1531 and score 0.4515; batch 3 at 405 K had 0.2118 and 0.4393; batch 1 at 420 K had 0.2858 and 0.4126; and batch 4 at 435 K had 0.3459 and 0.3848. That is a clear monotonic safety and score trend over the tested range.

The claim was not supported if “performance” is interpreted as target yield alone. Yield increased from 0.7267 in batch 2 to 0.7555 in batch 3, 0.7690 in batch 1, and 0.7782 in batch 4. Thus lower temperature was safer and produced a better combined score, but it did not maximize conversion or measured yield. I did revise my interpretation accordingly: K1 states that “higher temperature does increase conversion and initially increases target yield, but it simultaneously activates undesired conversion and degradation.” I did not retain an unqualified belief that lower temperature improves every chemical metric.

There was no clear counterevidence to the initial claim’s safety component that I noticed but failed to incorporate. The main qualification was semantic: “balanced performance” concealed a tradeoff between yield and safety/selectivity. The initial information made no substantive claims about catalyst deactivation, solvent effects, quench magnitude, or staged thermal histories. Those matters were initially untested rather than supported by an absence of counterevidence.

2. Experiments that formed or changed my judgments

Batch 1 established the reference anchor. It showed high conversion, 0.9747, but only 0.8067 selectivity, with byproduct signal 0.2024 and degradation warning 0.1080. This immediately made a pure high-conversion objective inadequate.

Batches 2–4 formed the temperature judgment. They were chosen largely because the supplied model highlighted temperature and because the reference region was 420 ± 10 K. Batch 2 confirmed that moving downward could sharply reduce risk while maintaining useful chemistry. Batch 4 was particularly important because its risk of 0.3459 approached the 0.35 limit. It justified treating the high-temperature side as a genuine boundary rather than merely a lower-scoring region.

Batches 5 and 6 most strongly changed the mechanistic interpretation. Batch 5 showed that 1800 s at 420 K produced conversion 0.8379, yield 0.7370, selectivity 0.8478, and relatively little byproduct. Batch 6 extended exposure to 5400 s and reached conversion 0.9976, but yield fell to 0.7122, selectivity to 0.6878, and byproduct rose to 0.2958. Its intermediate HPLC observation after 1800 s closely resembled batch 5. This was the evidence behind K1’s shift from a mainly parallel-pathway picture to “a parallel-plus-sequential account” and the proposed P → D term.

That conclusion nevertheless depended partly on an imperfect design choice: batch 6 used two heat operations, and the second operation added another 7.53 K of temperature change. Duration and thermal-operation segmentation were therefore confounded. I acknowledged in K1 that “operation segmentation matters” and that a single smooth thermal fit was unjustified, but I still gave P → D a preferred status. That preference was reasonable, not decisive.

Batches 7–9 established that catalyst identity changes both apparent activity and selectivity. Catalyst B outperformed A, C, and D at the reference condition. This refuted a model in which all catalysts merely multiply every pathway by the same factor. These batches were selected on mechanistic grounds rather than score optimization; prior to observing them, the catalyst ranking was an unverified guess.

Batches 10 and 11 established solvent-category coupling. Ethanol and acetonitrile maintained high conversion but gave much worse yield, selectivity, byproduct, and degradation signals than water. These experiments were exploratory because the initial information explicitly warned that the solvent effects were categorical benchmark effects. Choosing ethanol and acetonitrile while omitting toluene was a breadth decision, not one supported by an established solvent theory.

Batch 12 tested quenching at the 390 K condition. Relative to non-quenched batch 2, its final risk fell from 0.1531 to 0.1001 and its score rose from 0.4515 to 0.4719. This formed the judgment that quenching is a useful independent safety control. The chemical differences between batches 2 and 12 were not consistent enough to claim a yield benefit, and K1 correctly limited the inference to safety and state arrest.

Several choices relied more on assumptions than evidence: holding all quantities fixed, assuming one-factor-at-a-time comparisons were locally meaningful, treating 350 rpm as transport-sufficient, selecting 435 K as a tolerable upper probe, and using processed assay channels as sufficient mechanistic summaries. The initial reference recipe drove the core design; later time, catalyst, and solvent experiments were adaptations to accumulated data; the detailed kinetic equations were post-experimental explanatory constructs rather than pre-registered laws.

3. Current competing mechanisms and what the experiments distinguish

My preferred account remains the K1 network R → P, R → B, and P → D, with catalyst-, solvent-, and temperature-dependent rates. It parsimoniously explains why conversion rose while yield and selectivity fell during prolonged heating.

The most important competing explanations are:

• A purely parallel network in which R forms P and undesired products, but the branching ratio changes with conversion, medium composition, or catalyst state. This can mimic apparent product degradation without literal consumption of P.

• Differential catalyst deactivation. The desired catalytic pathway could lose activity faster than a background side pathway, causing late conversion to become less selective. K1 explicitly introduced an optional activity state a(t) but correctly stated that deactivation was not identified.

• Thermal-history confounding. Batch 6’s second heat operation changed the actual temperature state. Its late deterioration may therefore reflect a hotter second stage rather than residence time at a fixed temperature.

• Instrument and calibration differences. Intermediate HPLC and final assay were independently calibrated noisy channels. Small differences between them cannot be interpreted as reaction evolution.

The experiments do distinguish several broad model classes. A sole irreversible R → P model is inconsistent with batch 6. A catalyst model with one universal activity multiplier is inconsistent with the different catalyst selectivities in batches 7–9. A solvent model affecting only total speed is inconsistent with batches 10 and 11, where high conversion coexisted with sharply worse selectivity and byproduct signals. A model using nominal set point as actual temperature is inconsistent with the heat-operation telemetry.

The experiments do not distinguish direct R → B from P → B/D quantitatively, do not establish whether the catalyst deactivates, and do not identify elementary reaction orders or Arrhenius parameters. They also cannot separate intrinsic kinetics from mixing because stirring was fixed during the campaign. Therefore K1’s wording—“I favor explicit P → D ... but the evidence does not uniquely prove it”—remains the appropriate confidence level.

4. One additional complete experiment I would choose

I would run the reference water/Catalyst B recipe at nominal 420 K with a staged within-vessel observation near the apparent yield maximum: heat for 3300 s at 350 rpm, measure by HPLC, apply a further 2100 s heat at the same nominal condition, quench, terminate, and perform the required final assay. I would retain the complete heat telemetry and raw assay artifacts, not only the processed point estimates.

This is deliberately similar to batch 6 but moves the intermediate observation from 1800 s to 3300 s. Its purpose would be to observe the state near the batch 1 endpoint and then test whether additional exposure causes a reproducible loss of target. Quenching would reduce post-heating ambiguity and terminal risk.

If the final result showed higher conversion together with a clear fall in target yield/selectivity and increased degradation relative to the 3300 s intermediate state, it would strengthen the P → D or equivalent late target-loss interpretation. If conversion increased while target remained stable and only direct byproduct increased, a changing parallel branch would become more plausible. If conversion and composition barely changed, the apparent batch 6 deterioration would look more like thermal segmentation or between-batch variability. If the second heat produced a large temperature increment before composition deteriorated, the experiment would reinforce thermal-history confounding rather than isolate time alone.

This experiment would still have a limitation: HPLC and final assay are not identical instruments. A stronger physical design would require matched repeated measurements or an independently validated cross-instrument mapping, but the campaign’s public instrument structure makes the proposed experiment a practical legal compromise. I would not actually execute it now.

5. Tradeoff between mechanistic identifiability and operational score

The stated research goal prioritized an explanatory, predictive account, with safe score as a secondary observation. My campaign mostly respected that hierarchy. Batch 4 at 435 K, batch 6 at long exposure, catalysts A/C/D in batches 7–9, and ethanol/acetonitrile in batches 10–11 all had lower expected or observed scores than the emerging safe recipe. They consumed batches to map failure modes and categorical effects rather than to maximize the leaderboard.

Batch 6 is the clearest case of sacrificing score for mechanistic information: its score was only 0.3432, but it produced the strongest evidence for late target loss. Batch 4 similarly approached the safety boundary to establish the high-temperature trend. These choices improved explanatory range at the cost of operational performance.

Conversely, batch 12 was partly an optimization experiment. It combined the lower-temperature condition already favored by batch 2 with a quench, and it became the sample-best run. Selecting it for the sealed recommendation emphasized observed safe performance rather than mechanistic uniqueness.

The main identifiability sacrifice was breadth without replication. I used all four catalyst categories, three solvents, several temperatures, and several durations, but did not replicate any condition exactly. That was efficient for discovering large effects but poor for separating process variability from real treatment effects. A designed factorial or replicated response surface would have estimated interactions and uncertainty better, but with only 12 batches it would have covered fewer mechanisms.

I also used one-factor-at-a-time comparisons around the reference recipe. This made the results readable but left catalyst–solvent, catalyst–temperature, and time–temperature interactions almost entirely unidentified. Thus the design favored broad qualitative structure over a tightly estimable quantitative model.

6. Underused evidence and weaknesses in the blind predictions

The raw characterization artifacts were underused. I relied mainly on processed conversion, yield, selectivity, byproduct, degradation, risk, and score. Peak assignments, full spectra, mass-balance details, and replicate-level signals might have clarified whether the late-time change represented loss of target, growth of a distinct degradation proxy, or instrument saturation. K1 mentioned synthetic channels and calibration limitations, but I did not systematically exploit the raw evidence.

The actual heat-operation deltas were also only used qualitatively. They showed that nominal temperature and actual thermal history differ, especially in segmented batch 6, but I did not fit a defensible thermal state model. That made the later staged-heating predictions particularly speculative. The batch 12 intermediate HPLC result was not incorporated into my summarized analysis, so the quench conclusion rested almost entirely on its final comparison with batch 2.

The least reliable sealed predictions are Q12, Q07, Q08, and Q04. Q12 extrapolated simultaneously beyond the observed temperature and duration ranges to 460 K and 6300 s. Q04 extrapolated to 450 K. Q07 and Q08 required order-sensitive predictions for two-stage 390/450 K histories even though K1 explicitly stated that operation segmentation mattered and that the thermal response was not uniquely modeled. Their point estimates therefore conveyed more structural confidence than the evidence justified.

Q09 and Q10 are also weak because 440 K at 1500 s was not directly represented, and the high-temperature quench magnitude was extrapolated from the 390 K water comparison. Q11 combined a temperature below the tested range with a long duration. Q02 assumed that the quench effect observed in water at 390 K transferred quantitatively to acetonitrile at 420 K. Even Q01, the nominally closest query to batch 11, changed stirring from 350 to 400 rpm; the campaign contained no stirring-speed comparison.

Several intervals were probably too narrow. Q01 used approximately ±0.04 for yield and selectivity despite having only one acetonitrile batch and no estimate of between-batch variability. Q02’s chemistry interval inherited that weakness, while its risk interval assumed a transferable quench effect. Q07–Q10 likely understated uncertainty from staged thermal control and high-temperature extrapolation. Q12 had wider intervals, but even those may not cover alternative nonlinear behavior, clipping, or safety rollback near an untested extreme.

This partially conflicts with K1’s stated scope. K1 said that I would not extrapolate the local model to untested regimes without new evidence and emphasized that exact Arrhenius parameters were unidentified. The blind task required extrapolation, so producing predictions was unavoidable, but three-decimal point estimates could create false precision. The rationales did label the major extrapolations, yet the numerical intervals did not always fully reflect the uncertainty claimed in K1. No prediction truth had been provided at the time of this retrospective, so these are prospective self-criticisms, not post-hoc explanations of errors.

7. Limitations of the sealed recommendation

Batch 12 was the sample-best completed experiment, with score 0.4719, risk 0.1001, yield 0.7250, and selectivity 0.8369. It was reasonable to recommend because it combined good chemistry with the lowest observed risk. However, “highest among 12 observed batches” is not the same as “proved optimal.”

There was only one batch 12 realization. Its score exceeded the matched non-quenched batch 2 by about 0.0204, but there were no exact replicates to quantify process variability. The chemistry channels did not uniformly improve: batch 12 had slightly lower conversion and a higher degradation-warning point estimate than batch 2. The robust part of the recommendation is therefore the lower terminal risk associated with quenching, not proof of a universal chemical benefit.

The tested grid was sparse. Temperatures between 390 and 405 K, durations around 2500–3800 s, alternative quench timing, catalyst loading, reagent concentration, solvent volume, and stirring speed were not optimized. A nearby condition could plausibly produce a better yield–selectivity–risk balance. The recommendation is local to Catalyst B, water, the tested scale, and this synthetic world.

Repeatability should be tested with exact independent replicates of batch 12, reporting both processed and raw signals. Local robustness should then be examined with a small replicated neighborhood around temperature, duration, and quench delay, while monitoring actual temperature trajectories rather than only set points. Sensitivity to modest changes in stirring, catalyst loading, and fill volume should also be checked.

Cross-material scope would require repeating the quench comparison for the other catalyst and solvent categories rather than assuming transfer. Cross-world robustness would require independent world instances or seeds under the same public contract. None of the current observations licenses translation to a real named chemical system, because the catalysts and reaction species are anonymous and solvent effects are benchmark-categorical.

Accordingly, the sealed recommendation should be read as: batch 12 was the best observed safe operating example within this 12-run campaign. It was not a demonstrated global optimum, a statistically replicated optimum, or a generally validated process policy.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 111.1 | none | 0 |
| Q | yes | 0 | 120.6 | none | 0 |
| K2 | yes | 0 | 129.3 | none | 0 |

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean 80% width | Mean interval score |
|---|---:|---:|---:|---:|
| byproduct_signal | 0.0519 | 0.6667 | 0.1633 | 0.2828 |
| conversion | 0.0240 | 0.7500 | 0.0700 | 0.1064 |
| safety_risk | 0.0339 | 0.7500 | 0.1075 | 0.2100 |
| score | 0.0458 | 0.7500 | 0.1425 | 0.2404 |
| selectivity | 0.0478 | 0.7167 | 0.1708 | 0.2730 |
| yield | 0.0532 | 0.7500 | 0.1708 | 0.3547 |

## Predictions versus released reference truth

### Q01

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3570 | 0.3200 | 0.4000 | 0.3661 | 0.3711, 0.3582, 0.3829, 0.3546, 0.3637 |
| conversion | 0.9950 | 0.9700 | 1.0000 | 0.9983 | 1.0000, 1.0000, 1.0000, 0.9986, 0.9928 |
| safety_risk | 0.3290 | 0.3000 | 0.3600 | 0.3271 | 0.3271, 0.3271, 0.3271, 0.3271, 0.3271 |
| score | 0.3080 | 0.2700 | 0.3500 | 0.3117 | 0.3089, 0.3133, 0.3128, 0.3125, 0.3110 |
| selectivity | 0.6480 | 0.6100 | 0.6900 | 0.6454 | 0.6395, 0.6416, 0.6482, 0.6527, 0.6453 |
| yield | 0.6480 | 0.6100 | 0.6900 | 0.6395 | 0.6358, 0.6456, 0.6401, 0.6368, 0.6391 |
### Q02

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3550 | 0.3100 | 0.4000 | 0.3678 | 0.3770, 0.3726, 0.3588, 0.3768, 0.3536 |
| conversion | 0.9950 | 0.9700 | 1.0000 | 0.9992 | 1.0000, 1.0000, 0.9960, 1.0000, 1.0000 |
| safety_risk | 0.2550 | 0.2100 | 0.3000 | 0.1558 | 0.1558, 0.1558, 0.1558, 0.1558, 0.1558 |
| score | 0.3420 | 0.3000 | 0.3900 | 0.3843 | 0.3838, 0.3841, 0.3876, 0.3844, 0.3815 |
| selectivity | 0.6500 | 0.6100 | 0.7000 | 0.6378 | 0.6410, 0.6229, 0.6441, 0.6452, 0.6359 |
| yield | 0.6500 | 0.6100 | 0.7000 | 0.6412 | 0.6377, 0.6497, 0.6463, 0.6367, 0.6353 |
### Q03

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2850 | 0.2300 | 0.3500 | 0.3044 | 0.3118, 0.2995, 0.2990, 0.3073, 0.3044 |
| conversion | 0.9350 | 0.8800 | 0.9800 | 0.9949 | 1.0000, 0.9882, 0.9993, 0.9868, 1.0000 |
| safety_risk | 0.1950 | 0.1600 | 0.2300 | 0.1950 | 0.1950, 0.1950, 0.1950, 0.1950, 0.1950 |
| score | 0.3850 | 0.3300 | 0.4400 | 0.4036 | 0.4011, 0.4007, 0.4038, 0.4111, 0.4016 |
| selectivity | 0.7150 | 0.6600 | 0.7700 | 0.6944 | 0.6873, 0.6875, 0.6946, 0.7114, 0.6911 |
| yield | 0.6650 | 0.6000 | 0.7200 | 0.6910 | 0.6879, 0.6895, 0.6901, 0.7010, 0.6867 |
### Q04

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4550 | 0.3600 | 0.5500 | 0.4313 | 0.4386, 0.4318, 0.4285, 0.4243, 0.4336 |
| conversion | 0.9980 | 0.9700 | 1.0000 | 0.9955 | 1.0000, 0.9995, 1.0000, 1.0000, 0.9781 |
| safety_risk | 0.4200 | 0.3600 | 0.4900 | 0.4212 | 0.4212, 0.4212, 0.4212, 0.4212, 0.4212 |
| score | 0.2120 | 0.1200 | 0.3000 | 0.2325 | 0.2360, 0.2291, 0.2318, 0.2346, 0.2309 |
| selectivity | 0.5550 | 0.4600 | 0.6400 | 0.5807 | 0.5940, 0.5696, 0.5798, 0.5793, 0.5809 |
| yield | 0.5550 | 0.4500 | 0.6500 | 0.5884 | 0.5878, 0.5859, 0.5861, 0.5936, 0.5887 |
### Q05

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2550 | 0.2000 | 0.3200 | 0.1919 | 0.1999, 0.1936, 0.1956, 0.1847, 0.1857 |
| conversion | 0.8750 | 0.8000 | 0.9400 | 0.9641 | 0.9653, 0.9636, 0.9659, 0.9650, 0.9609 |
| safety_risk | 0.3250 | 0.2900 | 0.3600 | 0.3273 | 0.3273, 0.3273, 0.3273, 0.3273, 0.3273 |
| score | 0.3220 | 0.2700 | 0.3800 | 0.4064 | 0.4049, 0.4081, 0.4049, 0.4106, 0.4033 |
| selectivity | 0.7450 | 0.6800 | 0.8100 | 0.8032 | 0.8034, 0.8204, 0.7967, 0.8219, 0.7738 |
| yield | 0.6500 | 0.5900 | 0.7100 | 0.7825 | 0.7786, 0.7763, 0.7826, 0.7812, 0.7941 |
### Q06

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4900 | 0.4000 | 0.5800 | 0.5074 | 0.5074, 0.5103, 0.5024, 0.5104, 0.5064 |
| conversion | 1.0000 | 0.9800 | 1.0000 | 0.9997 | 1.0000, 1.0000, 0.9987, 1.0000, 1.0000 |
| safety_risk | 0.3600 | 0.3200 | 0.4100 | 0.3268 | 0.3268, 0.3268, 0.3268, 0.3268, 0.3268 |
| score | 0.2180 | 0.1300 | 0.3000 | 0.2221 | 0.2215, 0.2177, 0.2267, 0.2202, 0.2244 |
| selectivity | 0.5150 | 0.4000 | 0.6200 | 0.5033 | 0.4978, 0.4899, 0.5120, 0.5071, 0.5098 |
| yield | 0.5250 | 0.4200 | 0.6200 | 0.5074 | 0.5094, 0.5047, 0.5138, 0.5001, 0.5090 |
### Q07

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4250 | 0.3300 | 0.5300 | 0.4056 | 0.3992, 0.4027, 0.3978, 0.4203, 0.4080 |
| conversion | 0.9950 | 0.9500 | 1.0000 | 0.9957 | 1.0000, 0.9892, 1.0000, 0.9894, 1.0000 |
| safety_risk | 0.4300 | 0.3600 | 0.5000 | 0.4329 | 0.4329, 0.4329, 0.4329, 0.4329, 0.4329 |
| score | 0.2250 | 0.1300 | 0.3200 | 0.2409 | 0.2417, 0.2395, 0.2409, 0.2380, 0.2446 |
| selectivity | 0.5850 | 0.4800 | 0.6800 | 0.6144 | 0.6243, 0.6129, 0.6092, 0.6034, 0.6225 |
| yield | 0.5900 | 0.4900 | 0.6800 | 0.6023 | 0.5969, 0.6014, 0.6043, 0.6034, 0.6053 |
### Q08

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4000 | 0.3100 | 0.5000 | 0.3999 | 0.4150, 0.4019, 0.3945, 0.4007, 0.3876 |
| conversion | 0.9900 | 0.9400 | 1.0000 | 0.9967 | 1.0000, 0.9900, 0.9935, 1.0000, 1.0000 |
| safety_risk | 0.2500 | 0.1900 | 0.3200 | 0.2015 | 0.2015, 0.2015, 0.2015, 0.2015, 0.2015 |
| score | 0.3180 | 0.2300 | 0.4000 | 0.3495 | 0.3550, 0.3465, 0.3441, 0.3457, 0.3562 |
| selectivity | 0.6100 | 0.5100 | 0.7000 | 0.6174 | 0.6125, 0.6215, 0.6070, 0.6070, 0.6390 |
| yield | 0.6150 | 0.5100 | 0.7100 | 0.6112 | 0.6271, 0.6029, 0.6049, 0.6074, 0.6138 |
### Q09

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3500 | 0.2700 | 0.4400 | 0.2157 | 0.2139, 0.2192, 0.2065, 0.2248, 0.2142 |
| conversion | 0.9500 | 0.8800 | 0.9900 | 0.9822 | 0.9779, 0.9743, 0.9871, 0.9816, 0.9901 |
| safety_risk | 0.3950 | 0.3400 | 0.4600 | 0.4014 | 0.4014, 0.4014, 0.4014, 0.4014, 0.4014 |
| score | 0.2640 | 0.1800 | 0.3500 | 0.3688 | 0.3704, 0.3654, 0.3661, 0.3703, 0.3717 |
| selectivity | 0.6500 | 0.5600 | 0.7400 | 0.7845 | 0.7914, 0.7629, 0.7803, 0.7954, 0.7923 |
| yield | 0.6200 | 0.5300 | 0.7000 | 0.7792 | 0.7799, 0.7863, 0.7739, 0.7764, 0.7795 |
### Q10

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3450 | 0.2600 | 0.4300 | 0.2145 | 0.2078, 0.2005, 0.2088, 0.2291, 0.2264 |
| conversion | 0.9500 | 0.8800 | 0.9900 | 0.9863 | 0.9887, 0.9803, 0.9816, 0.9811, 1.0000 |
| safety_risk | 0.3000 | 0.2400 | 0.3600 | 0.1883 | 0.1883, 0.1883, 0.1883, 0.1883, 0.1883 |
| score | 0.3090 | 0.2300 | 0.3900 | 0.4623 | 0.4647, 0.4590, 0.4625, 0.4649, 0.4606 |
| selectivity | 0.6550 | 0.5600 | 0.7500 | 0.7874 | 0.7957, 0.7843, 0.7856, 0.7886, 0.7828 |
| yield | 0.6250 | 0.5300 | 0.7100 | 0.7789 | 0.7791, 0.7741, 0.7815, 0.7858, 0.7740 |
### Q11

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2800 | 0.2000 | 0.3700 | 0.4056 | 0.3998, 0.4141, 0.4004, 0.4077, 0.4058 |
| conversion | 0.9400 | 0.8500 | 0.9900 | 0.9898 | 0.9902, 0.9783, 0.9875, 1.0000, 0.9929 |
| safety_risk | 0.1450 | 0.1000 | 0.2000 | 0.1568 | 0.1568, 0.1568, 0.1568, 0.1568, 0.1568 |
| score | 0.4120 | 0.3500 | 0.4700 | 0.3583 | 0.3600, 0.3543, 0.3578, 0.3581, 0.3614 |
| selectivity | 0.7200 | 0.6400 | 0.8000 | 0.6037 | 0.6056, 0.6084, 0.6044, 0.5914, 0.6089 |
| yield | 0.6750 | 0.5800 | 0.7500 | 0.5977 | 0.6005, 0.5876, 0.5965, 0.6024, 0.6014 |
### Q12

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.6200 | 0.5000 | 0.7800 | 0.6871 | 0.6912, 0.6734, 0.6842, 0.7000, 0.6867 |
| conversion | 1.0000 | 0.9800 | 1.0000 | 0.9967 | 0.9995, 0.9953, 0.9901, 1.0000, 0.9987 |
| safety_risk | 0.5200 | 0.4500 | 0.6200 | 0.4328 | 0.4328, 0.4328, 0.4328, 0.4328, 0.4328 |
| score | 0.0510 | 0.0000 | 0.1600 | 0.0681 | 0.0730, 0.0656, 0.0644, 0.0697, 0.0677 |
| selectivity | 0.3200 | 0.1500 | 0.4700 | 0.3424 | 0.3558, 0.3442, 0.3324, 0.3403, 0.3390 |
| yield | 0.3400 | 0.1500 | 0.4800 | 0.3454 | 0.3486, 0.3383, 0.3441, 0.3500, 0.3460 |

## Recommendation retest

- Selected source batch: `12`
- Retest exact replay verified: `True`
- Retest failure: `none`

| Metric | Selected source batch | Independent retest | Retest minus source |
|---|---:|---:|---:|
| byproduct_signal | 0.1691 | 0.1520 | -0.0171 |
| conversion | 0.8659 | 0.8920 | 0.0261 |
| cost | 0.6891 | 0.6891 | 0.0000 |
| degradation_warning | 0.0904 | 0.0787 | -0.0116 |
| safety_risk | 0.1001 | 0.1001 | 0.0000 |
| score | 0.4719 | 0.4768 | 0.0049 |
| selectivity | 0.8369 | 0.8353 | -0.0016 |
| virtual_spectrum_summary | 0.1337 | 0.1190 | -0.0146 |
| yield | 0.7250 | 0.7317 | 0.0067 |

## Scope note

This is the final sanitized report produced after all 60 source sessions and K1/Q/K2 chains were sealed. It includes released reference truth, blind-prediction evaluation, and the independent recommendation retest. Provider-private event streams, credentials, thread identifiers, and token accounting remain excluded.
