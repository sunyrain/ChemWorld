# RX-W01--S--mechanism_discovery--MisIndexed

## Run summary

- World: `RX-W01`
- Locus: `S`
- Goal: `mechanism_discovery`
- Arm: `MisIndexed`
- Status: `completed`
- Source status: `completed`
- Experimental sessions: `12/12`
- Operations: `85`
- Exact replay: `{'checked_steps': 85, 'max_abs_error': 0.0, 'mismatches': [], 'verified': True}`
- Posttest chain sealed: `True`

### Recovery status

No recovery override was required for this task.

## Sealed recommendation

- Selected batch: `12`
- Rationale: Batch 12 gave the highest observed final yield and campaign score while remaining below the safety limit; immediate quenching after the 400 K boundary-controlled hold also reduced observed risk versus the unquenched comparison.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S0 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 350 K × 3600 s @ 600 rpm | no | 0.1759 | 0.4562 | 0.4148 | 0.2437 | 0.0085 | 0.1036 | 0.0793 |
| 2 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K × 3600 s @ 600 rpm | no | 0.2788 | 0.6641 | 0.4234 | 0.1482 | 0.0314 | 0.1123 | 0.1693 |
| 3 | S0 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 350 K × 3600 s @ 600 rpm | no | 0.1809 | 0.5052 | 0.3533 | 0.1792 | 0.0087 | 0.1030 | 0.0876 |
| 4 | S0 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K × 3600 s @ 600 rpm | no | 0.2496 | 0.5953 | 0.3902 | 0.1466 | 0.0315 | 0.1094 | 0.1385 |
| 5 | S1 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K × 3600 s @ 600 rpm | no | 0.3537 | 0.6295 | 0.5541 | 0.1914 | 0.0348 | 0.1457 | 0.1887 |
| 6 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K × 3600 s @ 600 rpm | no | 0.4744 | 0.7031 | 0.6419 | 0.2002 | 0.0766 | 0.1763 | 0.2504 |
| 7 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K × 3600 s @ 600 rpm | no | 0.4392 | 0.6709 | 0.6571 | 0.2205 | 0.0728 | 0.1862 | 0.2253 |
| 8 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 320 K × 3600 s @ 600 rpm | no | 0.3078 | 0.7042 | 0.4557 | 0.1402 | 0.0317 | 0.1520 | 0.1763 |
| 9 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 400 K × 3600 s @ 600 rpm | no | 0.6033 | 0.6669 | 0.8946 | 0.2943 | 0.1666 | 0.2607 | 0.2802 |
| 10 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K × 900 s @ 600 rpm | no | 0.1589 | 0.7875 | 0.2069 | 0.0399 | 0.0000 | 0.1386 | 0.1188 |
| 11 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K × 10800 s @ 600 rpm | no | 0.4534 | 0.4944 | 0.9432 | 0.5301 | 0.3243 | 0.1959 | 0.2111 |
| 12 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 400 K × 3600 s @ 600 rpm | yes | 0.6105 | 0.6856 | 0.9047 | 0.2907 | 0.1495 | 0.1964 | 0.3177 |

## Complete experimental actions and observations

### Batch 1

Lifecycle index: `1`; end step: `7`.

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
    "byproduct_signal": 0.2436654269695282,
    "conversion": 0.4147995412349701,
    "cost": 1.0,
    "degradation_warning": 0.008490330539643764,
    "safety_risk": 0.103555828332901,
    "score": 0.07928425818681717,
    "selectivity": 0.45618101954460144,
    "virtual_spectrum_summary": 0.13783663511276245,
    "yield": 0.17589794099330902
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
    "byproduct_signal": 0.14815106987953186,
    "conversion": 0.42341485619544983,
    "cost": 1.0,
    "degradation_warning": 0.031411901116371155,
    "safety_risk": 0.11234387010335922,
    "score": 0.16934214532375336,
    "selectivity": 0.6640780568122864,
    "virtual_spectrum_summary": 0.09561844915151596,
    "yield": 0.27883970737457275
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
    "byproduct_signal": 0.17916123569011688,
    "conversion": 0.3532930016517639,
    "cost": 1.0,
    "degradation_warning": 0.008658597245812416,
    "safety_risk": 0.10303283482789993,
    "score": 0.08760999143123627,
    "selectivity": 0.5052096247673035,
    "virtual_spectrum_summary": 0.10243505239486694,
    "yield": 0.18085764348506927
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
    "byproduct_signal": 0.14660054445266724,
    "conversion": 0.3902435898780823,
    "cost": 1.0,
    "degradation_warning": 0.03149493783712387,
    "safety_risk": 0.10939750075340271,
    "score": 0.13845130801200867,
    "selectivity": 0.5952738523483276,
    "virtual_spectrum_summary": 0.09480302035808563,
    "yield": 0.24959340691566467
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
  "end_step": 35,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.19140343368053436,
    "conversion": 0.5541254878044128,
    "cost": 1.0,
    "degradation_warning": 0.034811023622751236,
    "safety_risk": 0.14565342664718628,
    "score": 0.18869534134864807,
    "selectivity": 0.6294551491737366,
    "virtual_spectrum_summary": 0.12093684822320938,
    "yield": 0.35365763306617737
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
  "end_step": 42,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.200170636177063,
    "conversion": 0.6418653130531311,
    "cost": 1.0,
    "degradation_warning": 0.07659883797168732,
    "safety_risk": 0.1762675791978836,
    "score": 0.2504167854785919,
    "selectivity": 0.7030836939811707,
    "virtual_spectrum_summary": 0.14456333220005035,
    "yield": 0.47444936633110046
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
  "end_step": 49,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.22053229808807373,
    "conversion": 0.6570703983306885,
    "cost": 1.0,
    "degradation_warning": 0.07278180122375488,
    "safety_risk": 0.18623198568820953,
    "score": 0.22527951002120972,
    "selectivity": 0.6708603501319885,
    "virtual_spectrum_summary": 0.15404456853866577,
    "yield": 0.4391544461250305
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
      "catalyst": 1,
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
    "byproduct_signal": 0.14016222953796387,
    "conversion": 0.4557262063026428,
    "cost": 1.0,
    "degradation_warning": 0.03165455162525177,
    "safety_risk": 0.15201227366924286,
    "score": 0.1763477623462677,
    "selectivity": 0.7042126655578613,
    "virtual_spectrum_summary": 0.0913337767124176,
    "yield": 0.307818740606308
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
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
  "end_step": 63,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.29425299167633057,
    "conversion": 0.8946253061294556,
    "cost": 1.0,
    "degradation_warning": 0.16663864254951477,
    "safety_risk": 0.2607285976409912,
    "score": 0.2801745533943176,
    "selectivity": 0.666886031627655,
    "virtual_spectrum_summary": 0.23682652413845062,
    "yield": 0.6032959818840027
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 900,
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
  "end_step": 70,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.039878394454717636,
    "conversion": 0.20690423250198364,
    "cost": 1.0,
    "degradation_warning": 0.0,
    "safety_risk": 0.13855686783790588,
    "score": 0.11878383159637451,
    "selectivity": 0.787519633769989,
    "virtual_spectrum_summary": 0.021933116018772125,
    "yield": 0.15891021490097046
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 10800,
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
  "end_step": 77,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.5300671458244324,
    "conversion": 0.943164587020874,
    "cost": 1.0,
    "degradation_warning": 0.32429978251457214,
    "safety_risk": 0.19592007994651794,
    "score": 0.2111091911792755,
    "selectivity": 0.4944467544555664,
    "virtual_spectrum_summary": 0.43747183680534363,
    "yield": 0.45336270332336426
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 400
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
    "byproduct_signal": 0.29065975546836853,
    "conversion": 0.9046606421470642,
    "cost": 1.0,
    "degradation_warning": 0.1495484709739685,
    "safety_risk": 0.19636665284633636,
    "score": 0.3177056908607483,
    "selectivity": 0.685606062412262,
    "virtual_spectrum_summary": 0.22715966403484344,
    "yield": 0.6105077862739563
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

# Mechanistic report

## 1. Scope and evidential basis

This report concerns only the bounded synthetic reaction world that was experimentally observed. The reagent, reaction species, and catalysts are anonymous benchmark entities; therefore, I do not assign them real chemical identities or infer ordinary solvent-property trends beyond the measured categorical effects.

All twelve batches used 0.040 mol reagent in 0.080 L solvent. Every catalyst-containing batch used 0.005 mol catalyst, and all heating used 600 rpm. Each batch received one HPLC measurement followed by termination and a destructive final assay. Consequently, the strongest conclusions concern catalyst identity, solvent category, temperature, residence time, and immediate quenching at this one composition and stirring rate.

## 2. Proposed reaction network

The simplest account consistent with the results is a desired, partly reversible conversion coupled to parallel and consecutive undesired pathways:

R <-> P
R -> B
P -> D
B -> D or additional unresolved material

Here R is the limiting reactant, P is the measured target, B represents competing byproduct, and D represents thermally accumulated degradation. Catalyst and solvent change the rate constants rather than introducing separately observed species.

A useful provisional kinetic form is:

- dR/dt = -k1(T,catalyst,solvent) R + k_minus1(T,catalyst,solvent) P - kb(T,catalyst,solvent) R
- dP/dt = k1 R - k_minus1 P - kd(T,catalyst,solvent,time/history) P
- dB/dt = kb R + kd P - kbd B
- dD/dt = kd P + kbd B

The supplied structural prior stated that the target pathway may have an appreciable reverse channel. The observations are compatible with that claim, particularly the failure of target yield to keep increasing during prolonged heating, but they do not uniquely demonstrate reversibility. Product degradation and catalyst deactivation can produce the same endpoint pattern.

As a practical measurement relationship, target yield was approximately conversion multiplied by selectivity, allowing for assay noise and possibly slightly different operational definitions:

Y approximately X times S.

For example, in batch 9, X = 0.8946 and S = 0.6669, giving X*S = 0.5966 versus measured Y = 0.6033. In batch 10, X*S = 0.1629 versus measured Y = 0.1589.

## 3. Temperature and time behavior

The fixed-time acetonitrile/Catalyst B series provides the clearest evidence for thermally accelerated reaction and competition:

- Batch 8, 320 K for 3600 s: conversion 0.4557, selectivity 0.7042, yield 0.3078, byproduct 0.1402, degradation warning 0.0317.
- Batch 6, 350 K for 3600 s: conversion 0.6419, selectivity 0.7031, yield 0.4744, byproduct 0.2002, degradation warning 0.0766.
- Batch 9, 400 K for 3600 s: conversion 0.8946, selectivity 0.6669, yield 0.6033, byproduct 0.2943, degradation warning 0.1666.

Thus increasing temperature strongly increased conversion and target yield over this range, but it also accelerated byproduct and degradation formation. Selectivity was almost unchanged between 320 and 350 K, then declined at 400 K. This is consistent with desired and undesired channels both being thermally activated, with at least one undesired channel having a stronger temperature dependence at the upper end.

The 350 K residence-time series shows a pronounced conversion/selectivity tradeoff:

- Batch 10, 900 s: conversion 0.2069, selectivity 0.7875, yield 0.1589, byproduct 0.0399, degradation warning 0.0000.
- Batch 6, 3600 s: conversion 0.6419, selectivity 0.7031, yield 0.4744, byproduct 0.2002, degradation warning 0.0766.
- Batch 11, 10800 s: conversion 0.9432, selectivity 0.4944, yield 0.4534, byproduct 0.5301, degradation warning 0.3243.

Conversion continued to rise with time, but target yield passed through a maximum between the measured 3600 and 10800 s conditions. The long hold converted additional material mainly into non-target channels and/or destroyed target already formed. The simultaneous rise in byproduct signal and degradation warning supports a consecutive-loss process rather than a simple one-step irreversible R-to-P reaction.

A minimal pseudocode representation is:

1. Compute temperature-dependent k1, k_minus1, kb, and kd.
2. Modify those rates by catalyst and solvent category.
3. Integrate the coupled material balances along the actual temperature-time path.
4. At short time, P formation dominates and selectivity is high.
5. At greater thermal dose, R depletion, reverse reaction, parallel byproduct formation, and P degradation become increasingly important.
6. Quenching sharply reduces all thermally activated rates by lowering temperature.

The apparatus did not instantaneously attain every temperature. Reported heating increments were approximately +22.55 K in batch 8, +49.84 K in the representative 350 K acetonitrile run, and +91.08 K in the 400 K runs. Therefore, a predictive model should integrate actual temperature history rather than treating the requested setpoint as present for the entire nominal hold. Only endpoint temperature changes were publicly observed, so the exact ramp shape remains unidentified.

## 4. Catalyst effects and possible deactivation

Batches 1-4 screened all four catalysts in water at 350 K for 3600 s:

- Batch 1, Catalyst A: conversion 0.4148, selectivity 0.4562, yield 0.1759, byproduct 0.2437, degradation warning 0.0085.
- Batch 2, Catalyst B: conversion 0.4234, selectivity 0.6641, yield 0.2788, byproduct 0.1482, degradation warning 0.0314.
- Batch 3, Catalyst C: conversion 0.3533, selectivity 0.5052, yield 0.1809, byproduct 0.1792, degradation warning 0.0087.
- Batch 4, Catalyst D: conversion 0.3902, selectivity 0.5953, yield 0.2496, byproduct 0.1466, degradation warning 0.0315.

Catalyst B was the best target-forming catalyst under this comparison. Its conversion was only slightly greater than that of Catalyst A, but its much higher selectivity produced substantially more target. Catalyst D ranked second. This suggests that catalyst identity primarily changes branching among target and competing pathways, although changes in overall rate are also present. The corresponding HPLC yields—0.1891, 0.2893, 0.1968, and 0.2494 for A-D—support the same ordering despite measurement differences.

Catalyst deactivation is plausible but not independently established. Batch 11 showed deteriorating product performance after a long hold, which could arise from catalyst deactivation followed by uncatalyzed side reaction, but it could equally arise from target degradation, reversible approach to equilibrium, or continuing parallel conversion. There was no catalyst-loading series, catalyst-free control, reuse experiment, or direct catalyst-state measurement. Therefore, the data identify a history-dependent loss of effective target productivity, not its microscopic cause.

## 5. Solvent-category effects

Using Catalyst B at 350 K for 3600 s gave:

- Batch 2, water: conversion 0.4234, selectivity 0.6641, yield 0.2788, byproduct 0.1482.
- Batch 5, ethanol: conversion 0.5541, selectivity 0.6295, yield 0.3537, byproduct 0.1914.
- Batch 6, acetonitrile: conversion 0.6419, selectivity 0.7031, yield 0.4744, byproduct 0.2002.
- Batch 7, toluene: conversion 0.6571, selectivity 0.6709, yield 0.4392, byproduct 0.2205.

Toluene gave the greatest measured conversion, but acetonitrile gave the best selectivity and target yield. Water was slowest and lowest-yielding. The most defensible interpretation is that the categorical solvent setting modifies both desired and competing rate constants. Although effects resembling differences in solvation or transport could be imagined, the task explicitly defines these as benchmark categorical effects; no real-world solvent mechanism should be claimed from these data.

## 6. Quench and termination timing

Batch 12 repeated the batch-9 recipe—acetonitrile, Catalyst B, 400 K, 3600 s—but introduced an immediate quench before measurement and termination.

Observed quench effects were:

- Temperature decreased by 45 K over 55.24 s.
- Safety risk decreased from 0.2607 immediately after heating to 0.1964 after quenching.
- Final batch-12 results were conversion 0.9047, selectivity 0.6856, yield 0.6105, byproduct 0.2907, and degradation warning 0.1495.
- The unquenched batch 9 gave conversion 0.8946, selectivity 0.6669, yield 0.6033, byproduct 0.2943, and degradation warning 0.1666.

The directional pattern is consistent with quenching suppressing further target loss during cooling and handling: slightly greater retained yield and selectivity, slightly less byproduct and degradation, and markedly lower instantaneous safety risk. However, batches 9 and 12 were single runs, and the changes in chemical observables were modest relative to instrument and process uncertainty. The large risk reduction is directly attributable to cooling; the smaller apparent chemical advantage should be considered suggestive rather than precisely quantified.

Termination without prior quenching appears to freeze the assay state sufficiently for comparison, but the experiment did not separately resolve reaction during cooling, during termination, or during measurement latency. A mechanistic process model should therefore include a post-hold thermal segment rather than assuming an instantaneous stop unless a quench is used.

## 7. Safety coupling

Observed safety risk depended on formulation, temperature, time, and temperature state rather than simply on conversion:

- At 350 K for 3600 s with Catalyst B, risk rose across the solvent categories from 0.1123 in water to 0.1457 in ethanol, 0.1763 in acetonitrile, and 0.1862 in toluene.
- For the acetonitrile/Catalyst B temperature series, risk was 0.1520 at 320 K, 0.1763 at 350 K, and 0.2607 at 400 K.
- A 10800 s hold at 350 K produced risk 0.1959.
- Quenching the 400 K batch reduced current risk to 0.1964.

A reasonable phenomenological risk model is a formulation-dependent baseline plus an increasing function of temperature and thermal exposure, with a reversible state component that falls on cooling. All completed experiments remained below the stated safety limit of 0.35. Risk should not be interpreted as a species concentration because quenching changed it sharply without comparably large changes in conversion.

## 8. Best-supported operating explanation

Within the measured domain, the most productive strategy is to use the Catalyst B/acetonitrile combination, apply enough thermal dose for high conversion, and then quench promptly before extended hot residence causes additional byproduct and degradation. Batch 12 was the best observed realization: final yield 0.6105, conversion 0.9047, selectivity 0.6856, score 0.3177, and post-quench risk 0.1964.

This is an interpolation-level process recommendation, not proof that 400 K for exactly 3600 s is the mathematical optimum. The data imply a ridge in temperature-time space: higher temperature accelerates useful conversion, while excessive total thermal exposure lowers selectivity. A shorter hold somewhat above 400 K or an intermediate hold between 3600 and 10800 s at a lower temperature might perform better, but those are untested extrapolations.

## 9. Competing explanations

Several mechanisms remain observationally equivalent:

1. Reversible target formation plus irreversible byproduct formation.
2. Irreversible target formation followed by target degradation.
3. Catalyst deactivation that progressively favors an uncatalyzed side pathway.
4. Multiple parallel pathways whose relative rates change as reactant is depleted.
5. Apparent kinetic changes caused by unobserved temperature-ramp or mixing dynamics.

The rise of degradation warning and byproduct signal at high thermal dose most strongly supports some form of secondary loss, but it does not identify whether measured byproduct is formed directly from reactant or consecutively from target. Likewise, the structural prior makes reversibility credible, yet no approach-from-both-sides or product-spiking experiment was performed.

## 10. Limits of identification

The following factors were not identified:

- Reaction orders in reagent, catalyst, target, or byproduct.
- Numerical Arrhenius parameters or equilibrium constants.
- Dependence on catalyst loading, reagent concentration, solvent volume, or stirring speed.
- Catalyst-free behavior and catalyst deactivation kinetics.
- Detailed temperature ramp and cooling curves.
- Whether the degradation-warning channel corresponds to one or several species.
- Exact mass balance, because the public observables are normalized noisy channels rather than direct species inventories.
- Reproducibility, because each designed condition was run only once.

Final-assay and HPLC values sometimes differed beyond simple algebraic consistency, as expected from their stated independent noise and sampling contracts. I therefore base conclusions on large, repeated directional differences rather than small assay-to-assay changes.

In summary, the experimentally supported world is a thermally activated, catalyst- and solvent-dependent network in which target formation competes with parallel byproduct formation and later target loss. Catalyst B most effectively directs conversion toward target, acetonitrile provides the best observed yield/selectivity balance, conversion rises with both temperature and time, and excessive thermal residence erodes selectivity. Prompt quenching preserves the favorable state and lowers active safety risk. Reversibility and catalyst deactivation remain credible but unresolved contributors rather than established facts.

## Q — Blind predictions

### Overall rationale

Predictions were derived from the campaign's Catalyst B/acetonitrile temperature-time series, then adjusted for catalyst concentration relative to the studied approximately 0.0625 mol/L loading. Conversion was treated as a saturating pseudo-first-order process with a strongly temperature-dependent rate. Selectivity and yield were reduced as cumulative thermal and catalytic exposure increased, following the observed progression from high-selectivity short runs to the high-conversion, low-selectivity 10800 s run. Byproduct signal was predicted to rise with secondary conversion and target loss. Quenching was assigned a modest chemical-retention benefit but a larger reduction in active safety risk, consistent with batches 9 and 12. Intervals include assay noise, process variability, uncertain catalyst-order dependence, and much larger extrapolation uncertainty at 410-465 K and at the extreme catalyst loadings.

### Q01

The low catalyst loading should slow conversion relative to the studied loading, while the short 1800 s residence time should retain relatively high selectivity. The 410 K temperature increases both productive conversion and thermal competition.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1300 | 0.0600 | 0.2400 |
| conversion | 0.5400 | 0.3800 | 0.7000 |
| safety_risk | 0.2200 | 0.1600 | 0.2900 |
| score | 0.2400 | 0.1200 | 0.3600 |
| selectivity | 0.7600 | 0.6200 | 0.8600 |
| yield | 0.4000 | 0.2600 | 0.5400 |

### Q02

Four hours at 410 K should bring conversion close to completion even at low catalyst loading. Extrapolation from the long 350 K batch predicts substantial secondary loss and byproduct accumulation, so high conversion is not expected to produce high target yield.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6500 | 0.4500 | 0.8400 |
| conversion | 0.9850 | 0.9400 | 1.0000 |
| safety_risk | 0.3400 | 0.2500 | 0.4600 |
| score | 0.0600 | 0.0100 | 0.1600 |
| selectivity | 0.3000 | 0.1500 | 0.4800 |
| yield | 0.2900 | 0.1400 | 0.4700 |

### Q03

The high Catalyst B loading should give rapid conversion during the short 410 K hold. The residence time is still limited enough that target formation should dominate, although more byproduct is expected than in a cooler short run.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2300 | 0.1200 | 0.3700 |
| conversion | 0.8300 | 0.6900 | 0.9300 |
| safety_risk | 0.2500 | 0.1800 | 0.3400 |
| score | 0.2900 | 0.1600 | 0.4300 |
| selectivity | 0.6900 | 0.5500 | 0.8000 |
| yield | 0.5700 | 0.4100 | 0.7000 |

### Q04

This combines high catalyst loading with the longest 410 K exposure. Conversion should saturate, but the experimental decline in selectivity with thermal dose implies severe target degradation or diversion into competing products. This is a substantial extrapolation, hence the wide intervals.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8300 | 0.6400 | 0.9600 |
| conversion | 0.9950 | 0.9700 | 1.0000 |
| safety_risk | 0.3800 | 0.2800 | 0.5200 |
| score | 0.0200 | 0.0000 | 0.0800 |
| selectivity | 0.1400 | 0.0500 | 0.3000 |
| yield | 0.1400 | 0.0400 | 0.2900 |

### Q05

At 350 K, the low catalyst loading should make 7200 s resemble a moderate effective reaction time at the studied loading. Conversion should be substantial while selectivity remains materially higher than in the observed 10800 s run.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2100 | 0.1100 | 0.3400 |
| conversion | 0.6800 | 0.5000 | 0.8200 |
| safety_risk | 0.1800 | 0.1300 | 0.2400 |
| score | 0.2800 | 0.1600 | 0.4000 |
| selectivity | 0.7100 | 0.5900 | 0.8100 |
| yield | 0.4800 | 0.3300 | 0.6100 |

### Q06

Although catalyst loading is low, 7200 s at 465 K is far beyond the observed temperature range and should produce nearly complete conversion with extensive thermal degradation. The chemical and safety intervals are especially wide because this is a strong extrapolation.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9000 | 0.7000 | 0.9900 |
| conversion | 0.9970 | 0.9600 | 1.0000 |
| safety_risk | 0.5700 | 0.4000 | 0.7500 |
| score | 0.0050 | 0.0000 | 0.0400 |
| selectivity | 0.0900 | 0.0150 | 0.2500 |
| yield | 0.0900 | 0.0100 | 0.2400 |

### Q07

High Catalyst B loading should drive conversion close to completion over 7200 s at 350 K. The increased effective catalytic exposure also permits appreciable secondary loss, giving lower selectivity than the 3600 s reference and a yield near the broad optimum rather than near unity.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4000 | 0.2500 | 0.5800 |
| conversion | 0.9200 | 0.8200 | 0.9800 |
| safety_risk | 0.2100 | 0.1500 | 0.2900 |
| score | 0.2300 | 0.1200 | 0.3500 |
| selectivity | 0.5600 | 0.4200 | 0.6900 |
| yield | 0.5100 | 0.3700 | 0.6400 |

### Q08

The combination of high catalyst loading, 465 K, and a two-hour hold should exhaust reactant rapidly and then expose target to a very large secondary-reaction dose. Almost all converted material is therefore predicted to end as byproduct or degradation material.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9600 | 0.7900 | 1.0000 |
| conversion | 0.9990 | 0.9800 | 1.0000 |
| safety_risk | 0.6500 | 0.4600 | 0.8300 |
| score | 0.0010 | 0.0000 | 0.0200 |
| selectivity | 0.0350 | 0.0050 | 0.1500 |
| yield | 0.0350 | 0.0030 | 0.1400 |

### Q09

The catalyst concentration is close to that used in the campaign, so thermal-time extrapolation dominates. Two hours at 410 K should nearly complete conversion but pass the target-yield maximum, causing marked selectivity loss and byproduct formation.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5500 | 0.3800 | 0.7200 |
| conversion | 0.9900 | 0.9500 | 1.0000 |
| safety_risk | 0.3300 | 0.2400 | 0.4400 |
| score | 0.1200 | 0.0500 | 0.2300 |
| selectivity | 0.4300 | 0.2900 | 0.5700 |
| yield | 0.4200 | 0.2800 | 0.5600 |

### Q10

The pre-quench chemistry should resemble Q09. Immediate quenching is predicted to suppress additional hot-state loss during shutdown, modestly improving retained yield and selectivity while producing a clearer reduction in final safety risk.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5200 | 0.3500 | 0.6900 |
| conversion | 0.9900 | 0.9500 | 1.0000 |
| safety_risk | 0.2400 | 0.1700 | 0.3300 |
| score | 0.1600 | 0.0700 | 0.2800 |
| selectivity | 0.4600 | 0.3200 | 0.6000 |
| yield | 0.4500 | 0.3100 | 0.5900 |

### Q11

This extends the observed 350 K time series from 10800 to 14400 s at approximately the studied catalyst concentration. Conversion should approach completion, while continued target loss should lower selectivity and yield further and raise byproduct signal.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6200 | 0.4500 | 0.7800 |
| conversion | 0.9800 | 0.9300 | 1.0000 |
| safety_risk | 0.2100 | 0.1500 | 0.2900 |
| score | 0.1200 | 0.0500 | 0.2200 |
| selectivity | 0.3900 | 0.2600 | 0.5200 |
| yield | 0.3800 | 0.2500 | 0.5100 |

### Q12

The very high temperature should give rapid conversion during 1800 s, but its stronger acceleration of competing and degradation pathways should substantially reduce selectivity. Uncertainty is large because 465 K lies outside the experimental temperature range.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5800 | 0.3800 | 0.7600 |
| conversion | 0.9600 | 0.8600 | 1.0000 |
| safety_risk | 0.4300 | 0.3000 | 0.5900 |
| score | 0.0800 | 0.0200 | 0.1900 |
| selectivity | 0.4200 | 0.2500 | 0.5900 |
| yield | 0.3900 | 0.2300 | 0.5600 |

## K2 — Retrospective analysis

## 1. Assessment of the initial information

The only substantive mechanistic prior was that “the target pathway may have an appreciable reverse channel,” with moderate confidence. The campaign did not directly test microscopic reversibility. In K1 I therefore described reversibility as “compatible” with the observations, not established.

The strongest relevant observation was the time series with Catalyst B in acetonitrile at 350 K: batch 10 at 900 s had conversion 0.2069 and yield 0.1589; batch 6 at 3600 s had conversion 0.6419 and yield 0.4744; batch 11 at 10800 s had conversion 0.9432 but a lower yield of 0.4534, alongside byproduct 0.5301 and degradation warning 0.3243. This shows that prolonged heating ceases to improve target yield, but it does not specifically demonstrate P → R. Indeed, the large increases in byproduct and degradation provide more direct support for irreversible secondary loss than for reversal. That is not positive counterevidence against a reverse channel, because reversal could coexist with degradation, but it weakens any need to invoke appreciable reversal as the primary explanation.

Thus, the initial reverse-channel claim remains untested rather than supported in a discriminating sense. No observation clearly showed target returning to reactant, an equilibrium plateau approached from two directions, or a change in equilibrium with temperature. I did not overlook clear contrary evidence and fail to revise; rather, I recognized in K1 that degradation and deactivation were competing explanations. My wording that the long-time yield maximum was “compatible” with reversibility was defensible but weak evidence.

The material packet also stated that solvent effects were categorical benchmark effects and should not be interpreted as predictions from real solvent properties. The experiment confirmed strong solvent-category dependence, but it could not validate any real chemical-property account. I adhered to that limitation in K1 by declining to attribute the acetonitrile result to a specific real-world polarity, solvation, or transport mechanism.

No substantive initial claims were supplied about catalyst ranking, reaction order, activation parameters, deactivation, optimal temperature, or quench behavior. Those were empirical questions rather than priors that could be confirmed or refuted.

## 2. Experiments that formed or changed my judgments

Batches 1–4 genuinely established the catalyst judgment. At fixed water/350 K/3600 s conditions, Catalyst B in batch 2 produced final selectivity 0.6641 and yield 0.2788, compared with 0.4562 and 0.1759 for Catalyst A in batch 1. Catalysts C and D were intermediate or inferior. This changed the working design from an initially arbitrary Catalyst A baseline to Catalyst B for subsequent solvent and thermal studies. The important lesson was that catalyst identity affected pathway branching more strongly than conversion alone.

Batches 5–7 formed the solvent judgment. With Catalyst B at 350 K for 3600 s, acetonitrile in batch 6 gave yield 0.4744 and selectivity 0.7031. Toluene in batch 7 gave slightly higher conversion, 0.6571 versus 0.6419, but lower yield, 0.4392, and lower selectivity, 0.6709. This changed the working objective from maximizing conversion to balancing conversion and branching, and it motivated selecting acetonitrile for the temperature and time studies.

Batches 8, 6, and 9 formed the temperature account. At 320, 350, and 400 K for 3600 s, conversion rose from 0.4557 to 0.6419 to 0.8946, while degradation warning rose from 0.0317 to 0.0766 to 0.1666. This supported thermally activated target formation coupled to more strongly increasing competition at high temperature.

Batches 10, 6, and 11 most strongly changed the mechanistic interpretation. At 350 K, increasing residence time from 900 to 3600 to 10800 s raised conversion but caused yield to peak and then decline. That result ruled out an adequate description as a single irreversible R → P reaction. It motivated the consecutive-loss terms in K1 and raised, without resolving, the alternatives of target degradation, reversibility, catalyst deactivation, and time-dependent branching.

Batch 12 was a targeted follow-up to batch 9. It repeated the 400 K/3600 s Catalyst B/acetonitrile condition but added a quench. The quench reduced current safety risk from 0.2607 to 0.1964 and produced slightly better final yield and selectivity than batch 9. This formed the recommendation to quench promptly. However, the chemical improvement was modest and based on one paired comparison, so it should not have been treated as a precise quench effect.

Some choices rested more on unverified assumptions. The initial Catalyst A/water baseline was arbitrary because the packet supplied no ranking. The choice of 350 K and 3600 s as the screening center was a pragmatic middle condition rather than a data-derived optimum. The 320 and 400 K temperature points and the 900 and 10800 s time points were chosen to create contrast, not from a previously fitted rate law. The use of maximum catalyst loading in every campaign batch was convenient and score-oriented, but it left catalyst-order and loading effects entirely unidentified. That omission later became important because the blind questions varied catalyst amount substantially.

## 3. Principal competing mechanisms

The leading explanations are:

1. Parallel formation: R → P and R → B, with temperature, solvent, and catalyst changing the branching ratio.
2. Consecutive target loss: R → P → D or B.
3. Reversible target formation: R ⇌ P, combined with one or more irreversible side reactions.
4. Catalyst deactivation: the catalyst initially favors P but loses activity or selectivity with thermal history.
5. Unresolved thermal-history or transport effects: different heating ramps, mixing behavior, or cooling histories could mimic changes in intrinsic kinetics.

The experiments can distinguish a single irreversible target-only pathway from a network containing competition or secondary loss. Batch 11 is especially decisive: nearly complete conversion did not imply maximal yield, and both byproduct and degradation signals were large. The catalyst screen also distinguishes a model in which catalyst identity changes only a common rate multiplier from one in which it changes branching; Catalyst B and Catalyst A had similar conversion in water but very different selectivity.

The experiments cannot reliably distinguish direct R → B from P → B/D. Cross-batch endpoint time points show that byproduct increases as target productivity eventually declines, but no single-vessel species trajectory was measured at multiple times. They also cannot distinguish target degradation from catalyst deactivation, because there was no catalyst-state observable, catalyst-loading series, or rescue experiment with fresh catalyst. Reversibility remains particularly poorly identified because no product addition was legally available, no approach to equilibrium from the product side occurred, and no deliberate temperature-cycle experiment was performed.

The actual temperature increments showed that requested setpoint alone was an incomplete process descriptor, but only endpoint temperature changes were available. Thus, intrinsic Arrhenius effects cannot be cleanly separated from ramp and residence-time effects.

## 4. One additional complete experiment

If only one legal complete experiment were allowed, I would prioritize discriminating secondary target loss from a purely parallel mechanism and probing the initial reversibility claim.

I would use the established Catalyst B/acetonitrile formulation at the campaign scale: 0.080 L acetonitrile, 0.040 mol reagent, and 0.005 mol Catalyst B. I would heat at 400 K and 600 rpm for 3600 s, take one HPLC measurement, quench immediately, then wait for 10800 s at 600 rpm in the cooled state, terminate, and perform the required final assay.

This is anchored by batch 12, which supplies an immediate-post-quench comparison. The within-batch HPLC point would document the state reached before the long cooled wait, while the final assay and batch-12 endpoint would indicate whether the state continues to change after thermal suppression. The different instruments introduce some uncertainty, but the expected changes under the competing mechanisms are large enough to be informative.

Possible interpretations would be:

- If conversion and yield remain approximately stable and byproduct/degradation remain near batch-12 values, the reverse and consecutive-loss rates at the quenched temperature are small. The long-time deterioration in batch 11 would then be primarily a hot-state process.
- If conversion decreases materially while byproduct and degradation remain nearly unchanged, that would be the most direct available support for appreciable P → R reversal.
- If yield and selectivity decrease while conversion remains high and byproduct or degradation increases, irreversible target degradation would be favored over reversal.
- If the post-quench state changes little but a corresponding future hot hold caused continued deterioration, temperature-dependent degradation or deactivation would remain plausible; catalyst deactivation would still not be uniquely identified.
- If conversion continues increasing at the cooled temperature while selectivity falls, parallel residual conversion and secondary loss would both remain active.

I would choose this mechanistic experiment rather than another nominal optimization point because the largest unresolved issue is the cause of the long-time yield decline, not whether a nearby condition can improve the score by a small amount.

## 5. Tradeoff between identifiability and operational score

The early design favored identifiability. Batches 1–4 isolated catalyst identity at one common condition, and batches 5–7 isolated solvent category using the selected catalyst. Batches 8–11 then varied temperature or duration around the same Catalyst B/acetonitrile reference. Several of these conditions were knowingly unlikely to maximize score: batch 10 was deliberately short, batch 8 was deliberately cool, and batch 11 was deliberately long. These experiments sacrificed immediate performance to reveal rate, selectivity, and degradation trends.

Later design shifted toward performance. Batch 9 used the best observed catalyst/solvent combination at 400 K, and batch 12 repeated it with quenching. Batch 12 became the highest-scoring observed condition and the recommendation. This was a reasonable response to the secondary safe-score objective, but it used the final experiment to improve an operating recipe rather than to test catalyst loading, reversibility, or deactivation.

There were also score-driven design costs. Every batch used the maximum permitted catalyst amount, so the campaign learned catalyst identity but not catalyst order, saturation, or minimum effective loading. There were no catalyst-free controls. No conditions were replicated, because each vessel was allocated to a new contrast. That maximized factor coverage and the chance of finding a better operation, but it prevented direct estimation of process reproducibility.

Conversely, batch 11 illustrates sacrificing score for identifiability: its 10800 s hold produced a lower score than the 3600 s high-temperature conditions, but it was the experiment that most clearly exposed secondary loss. The research goal appropriately led me to retain such diagnostic conditions rather than spending all twelve batches on local optimization.

## 6. Underused evidence and weaknesses in the blind predictions

The campaign generated paired HPLC and final-assay estimates, but K1 mainly used the processed endpoint values and broad directional agreement. The discrepancies between HPLC and final assay could have been analyzed more systematically to estimate cross-instrument variability and determine whether state evolution occurred between sampling and termination. Instead, I mostly treated them qualitatively.

I also did not inspect or exploit the public raw characterization artifacts, spectral assignments, mass-balance fragments, calibration flags, or channel-level uncertainty. Those might not have identified hidden species, but they could have revealed saturation, missingness, peak overlap, or mass-balance limitations. The actual temperature-change and operation-risk increments were recorded, yet only a simple qualitative thermal-history account was constructed. A more disciplined fit could have separated formulation baseline risk, heating risk, and quench-reversible risk.

The blind predictions most at risk are Q06 and Q08: both use 465 K for 7200 s, well outside the observed maximum of 400 K and beyond the observed combined temperature-time dose. Their near-unity conversion, near-zero selectivity, and very high safety-risk estimates depend on extrapolating an assumed Arrhenius-like rate and secondary degradation response. The 80% intervals were wide, but probably still too narrow given the absence of activation parameters and the possibility of saturation, phase changes, catalyst failure, or a different high-temperature regime.

Q04 is also highly unreliable because it combines 410 K, 14400 s, and a catalyst concentration far above the studied concentration. Predicting conversion 0.995 and selectivity 0.14 created an appearance of precision that the campaign did not justify. Q02 has the same long high-temperature extrapolation at low catalyst loading.

Q01, Q03, Q05, and Q07 depend strongly on catalyst-loading effects. K1 explicitly stated that reaction order and catalyst-loading dependence were not identified. Nevertheless, the sealed Q rationale adjusted rates according to catalyst concentration using an implicit assumed loading exponent. That was a necessary predictive choice, but it was not supported by campaign data. The intervals, especially for conversion and selectivity, should therefore have been wider.

Q09–Q10 inherit uncertainty in the chemical effect of quenching. K1 correctly called the batch-9/batch-12 chemical difference “suggestive rather than precisely quantified,” but the blind predictions assigned Q10 a fairly definite improvement over Q09. Their chemical intervals should have overlapped even more strongly, and the rationale should have emphasized that the most defensible quench prediction concerned safety risk, not target retention.

Q11 is closer to the measured 350 K time series, but extrapolating from 10800 to 14400 s still requires choosing among reversal, degradation, and deactivation. Its interval may also be too narrow.

All blind queries used 0.005 L solvent, 0.003 mol reagent, 400 rpm, and catalyst amounts unlike the campaign recipe. K1 explicitly limited applicability to one composition and 600 rpm. The prediction rationale mentioned catalyst concentration and thermal extrapolation but did not adequately propagate uncertainty from scale, reagent concentration, stirring speed, and possible transport effects. The safety-risk and score intervals are particularly vulnerable because their functional forms were not mechanistically identified. The score predictions relied on a heuristic relationship among yield, selectivity, and risk rather than a validated equation.

Thus, the sealed predictions were directionally tied to K1, but some numerical intervals were inconsistent with K1’s stated limits by being too confident outside the measured catalyst-loading, scale, stirring, and temperature domain.

## 7. Limits of the sealed recommendation

Batch 12 was the sample-best experiment, not a proven optimum. It had final yield 0.6105, score 0.3177, and post-quench safety risk 0.1964, the best observed combination among the twelve completed batches. That supports selecting it from the tested set.

However, it was only one realization. There was no exact replicate, so its advantage over batch 9 could partly reflect process and assay noise. The quench comparison changed both thermal history and measurement timing, and the observed chemical improvement was modest. The experiment did not establish whether 400 K, 3600 s, the maximum catalyst loading, or the precise quench timing was individually optimal.

Reproducibility should be tested first with several exact batch-12 replicates, preferably randomized among reference batches, using both HPLC and final assay under a prespecified analysis. This would estimate batch variance and determine whether the apparent gain over batch 9 is larger than normal variability.

Local robustness should then be tested around the recommendation rather than by repeating a broad screen: for example, temperatures near 380, 400, and 420 K; hold times near 2700, 3600, and 4500 s; modestly different Catalyst B loadings; and controlled quench delays. Such a design would show whether batch 12 lies on a broad safe plateau or at a narrow, fragile peak. Actual temperature histories should be recorded rather than relying only on nominal setpoints.

Robustness to composition and transport would require varying reagent concentration, solvent volume, and stirring speed. The blind queries emphasize why this matters: they use a smaller volume, higher reagent concentration, different catalyst loadings, and 400 rpm, none of which was validated in the campaign.

Cross-material generalization is especially limited. Catalyst B and the reaction species are anonymous benchmark entities, and the solvent effects are calibrated categorical effects. The result does not establish that real acetonitrile or any real catalyst would behave similarly in a physical synthesis. Cross-world generalization would require repeating the structured catalyst/solvent/temperature/time study under independently instantiated benchmark worlds and testing whether the same qualitative rankings and kinetic relationships persist.

Accordingly, the defensible claim is: batch 12 was the highest-performing observed batch within this one campaign and remained below the stated safety limit. The indefensible stronger claim would be that it is globally optimal, reproducible without verification, or transferable to other scales, materials, stirring regimes, or worlds.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 97.2 | none | 0 |
| Q | yes | 0 | 118.9 | none | 0 |
| K2 | yes | 0 | 115.1 | none | 0 |

## Scope note

This report contains only information available before truth release. Reference truth, prediction scoring, and recommendation retests are intentionally absent because the full 60-task block has not yet completed.
