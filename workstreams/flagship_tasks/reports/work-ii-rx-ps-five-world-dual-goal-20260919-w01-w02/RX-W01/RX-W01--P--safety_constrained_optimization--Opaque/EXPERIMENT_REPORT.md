# RX-W01--P--safety_constrained_optimization--Opaque

## Run summary

- World: `RX-W01`
- Locus: `P`
- Goal: `safety_constrained_optimization`
- Arm: `Opaque`
- Status: `completed`
- Source status: `completed`
- Experimental sessions: `12/12`
- Operations: `84`
- Exact replay: `{'checked_steps': 84, 'max_abs_error': 0.0, 'mismatches': [], 'verified': True}`
- Posttest chain sealed: `True`

### Recovery status

No recovery override was required for this task.

## Sealed recommendation

- Selected batch: `12`
- Rationale: Batch 12 achieved the strongest observed public safe-score (about 0.284) while remaining comfortably below the 0.35 safety limit (risk about 0.197), using solvent 2, catalyst 1, a 370 K target, and 3600 s heating.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S0 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 330 K × 3600 s @ 600 rpm | no | 0.1235 | 0.3705 | 0.3143 | 0.1994 | 0.0063 | 0.0932 | 0.0315 |
| 2 | S1 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 360 K × 5400 s @ 700 rpm | no | 0.4691 | 0.6042 | 0.7658 | 0.2983 | 0.1035 | 0.1660 | 0.2406 |
| 3 | S2 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 360 K × 5400 s @ 700 rpm | no | 0.4362 | 0.5356 | 0.7883 | 0.3853 | 0.0628 | 0.1805 | 0.2060 |
| 4 | S3 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 360 K × 5400 s @ 700 rpm | no | 0.3831 | 0.4576 | 0.8228 | 0.4749 | 0.0433 | 0.1892 | 0.1647 |
| 5 | S1 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 360 K × 5400 s @ 700 rpm | no | 0.3284 | 0.4185 | 0.7280 | 0.4299 | 0.0125 | 0.1513 | 0.1407 |
| 6 | S1 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 360 K × 5400 s @ 700 rpm | no | 0.3492 | 0.5065 | 0.6923 | 0.3557 | 0.0507 | 0.1521 | 0.1671 |
| 7 | S1 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 360 K × 5400 s @ 700 rpm | no | 0.3941 | 0.5520 | 0.7378 | 0.3318 | 0.1022 | 0.1617 | 0.1966 |
| 8 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 360 K × 5400 s @ 700 rpm | no | 0.5418 | 0.6392 | 0.8473 | 0.3108 | 0.1672 | 0.1959 | 0.2731 |
| 9 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 380 K × 5400 s @ 700 rpm | no | 0.5616 | 0.5968 | 0.9417 | 0.3624 | 0.2134 | 0.2187 | 0.2696 |
| 10 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 370 K × 5400 s @ 700 rpm | no | 0.5699 | 0.6201 | 0.8866 | 0.3396 | 0.1835 | 0.2056 | 0.2791 |
| 11 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 360 K × 7200 s @ 700 rpm | no | 0.5282 | 0.5515 | 0.9290 | 0.4082 | 0.2470 | 0.1998 | 0.2521 |
| 12 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 370 K × 3600 s @ 700 rpm | no | 0.5483 | 0.7037 | 0.7756 | 0.2323 | 0.0954 | 0.1973 | 0.2840 |

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
      "target_temperature_K": 330
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
    "byproduct_signal": 0.1994362771511078,
    "conversion": 0.3143315315246582,
    "cost": 1.0,
    "degradation_warning": 0.006325569003820419,
    "safety_risk": 0.09323185682296753,
    "score": 0.03149053826928139,
    "selectivity": 0.3705081343650818,
    "virtual_spectrum_summary": 0.1125364601612091,
    "yield": 0.12346171587705612
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
      "duration_s": 5400,
      "operation": "heat",
      "stirring_speed_rpm": 700,
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
  "end_step": 14,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.29830965399742126,
    "conversion": 0.7658418416976929,
    "cost": 1.0,
    "degradation_warning": 0.10348665714263916,
    "safety_risk": 0.16596156358718872,
    "score": 0.2405608743429184,
    "selectivity": 0.6041542887687683,
    "virtual_spectrum_summary": 0.21063931286334991,
    "yield": 0.4690520763397217
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
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 5400,
      "operation": "heat",
      "stirring_speed_rpm": 700,
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
  "end_step": 21,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.38532349467277527,
    "conversion": 0.7882547974586487,
    "cost": 1.0,
    "degradation_warning": 0.06283895671367645,
    "safety_risk": 0.1805284470319748,
    "score": 0.2059507668018341,
    "selectivity": 0.535567581653595,
    "virtual_spectrum_summary": 0.24020545184612274,
    "yield": 0.4361779987812042
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
      "solvent": 3,
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
      "duration_s": 5400,
      "operation": "heat",
      "stirring_speed_rpm": 700,
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
  "end_step": 28,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.47487568855285645,
    "conversion": 0.8227769732475281,
    "cost": 1.0,
    "degradation_warning": 0.04331798106431961,
    "safety_risk": 0.18923169374465942,
    "score": 0.16474059224128723,
    "selectivity": 0.4575570523738861,
    "virtual_spectrum_summary": 0.2806747257709503,
    "yield": 0.3830697238445282
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
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 5400,
      "operation": "heat",
      "stirring_speed_rpm": 700,
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
  "end_step": 35,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.4299001097679138,
    "conversion": 0.7279731035232544,
    "cost": 1.0,
    "degradation_warning": 0.01253537368029356,
    "safety_risk": 0.15131689608097076,
    "score": 0.14068229496479034,
    "selectivity": 0.4184707999229431,
    "virtual_spectrum_summary": 0.24208597838878632,
    "yield": 0.3283997178077698
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
      "catalyst": 2,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 5400,
      "operation": "heat",
      "stirring_speed_rpm": 700,
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
  "end_step": 42,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.35568520426750183,
    "conversion": 0.6922869086265564,
    "cost": 1.0,
    "degradation_warning": 0.05067327246069908,
    "safety_risk": 0.152068093419075,
    "score": 0.1671188473701477,
    "selectivity": 0.5065211057662964,
    "virtual_spectrum_summary": 0.218429833650589,
    "yield": 0.34922632575035095
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
      "duration_s": 5400,
      "operation": "heat",
      "stirring_speed_rpm": 700,
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
  "end_step": 49,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.3318217098712921,
    "conversion": 0.7377511262893677,
    "cost": 1.0,
    "degradation_warning": 0.10218572616577148,
    "safety_risk": 0.16167297959327698,
    "score": 0.19664861261844635,
    "selectivity": 0.5519569516181946,
    "virtual_spectrum_summary": 0.22848550975322723,
    "yield": 0.39409276843070984
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
      "duration_s": 5400,
      "operation": "heat",
      "stirring_speed_rpm": 700,
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
  "end_step": 56,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.3107711374759674,
    "conversion": 0.8472900390625,
    "cost": 1.0,
    "degradation_warning": 0.1672334372997284,
    "safety_risk": 0.19589613378047943,
    "score": 0.27308952808380127,
    "selectivity": 0.6392186284065247,
    "virtual_spectrum_summary": 0.24617917835712433,
    "yield": 0.5417728424072266
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
      "duration_s": 5400,
      "operation": "heat",
      "stirring_speed_rpm": 700,
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
    "byproduct_signal": 0.3623760938644409,
    "conversion": 0.941650927066803,
    "cost": 1.0,
    "degradation_warning": 0.21337898075580597,
    "safety_risk": 0.21867680549621582,
    "score": 0.26958176493644714,
    "selectivity": 0.5967738628387451,
    "virtual_spectrum_summary": 0.29532739520072937,
    "yield": 0.5615693926811218
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
      "duration_s": 5400,
      "operation": "heat",
      "stirring_speed_rpm": 700,
      "target_temperature_K": 370
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
    "byproduct_signal": 0.33957988023757935,
    "conversion": 0.8866485357284546,
    "cost": 1.0,
    "degradation_warning": 0.18350671231746674,
    "safety_risk": 0.20564338564872742,
    "score": 0.27910611033439636,
    "selectivity": 0.6201465725898743,
    "virtual_spectrum_summary": 0.2693469524383545,
    "yield": 0.5698603391647339
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 700,
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
  "end_step": 77,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.40823325514793396,
    "conversion": 0.9290223717689514,
    "cost": 1.0,
    "degradation_warning": 0.24696584045886993,
    "safety_risk": 0.19982652366161346,
    "score": 0.25214412808418274,
    "selectivity": 0.5515089631080627,
    "virtual_spectrum_summary": 0.33566293120384216,
    "yield": 0.5282164812088013
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
      "stirring_speed_rpm": 700,
      "target_temperature_K": 370
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
    "byproduct_signal": 0.23228389024734497,
    "conversion": 0.7755561470985413,
    "cost": 1.0,
    "degradation_warning": 0.09541952610015869,
    "safety_risk": 0.19725921750068665,
    "score": 0.28404366970062256,
    "selectivity": 0.7037234306335449,
    "virtual_spectrum_summary": 0.17069491744041443,
    "yield": 0.5483096241950989
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

1. Scope and evidence base

This interpretation is based only on the 12 completed campaign batches and their public HPLC/final-assay outputs. The selectable catalysts are anonymous benchmark formulations, and the solvent effects are categorical benchmark effects; therefore, I do not assign real chemical identities to the catalyst or reaction species. All batches remained below the declared safety-risk limit of 0.35. The highest observed risk was about 0.219 in Batch 9.

All batches used 0.040 mol reagent, 0.080 L solvent, and 0.005 mol catalyst. Most used 700 rpm stirring; Batch 1 used 600 rpm. Consequently, the campaign principally identifies categorical solvent/catalyst effects and temperature-time effects, not concentration, loading, or mixing laws.

2. Proposed reaction network

The simplest model consistent with the data is a desired reaction competing with byproduct formation and followed by thermal loss of desired product:

R -> P                 rate k1(T, catalyst, solvent)
R -> B                 rate k2(T, catalyst, solvent)
P -> B and/or D         rate k3(T, catalyst, solvent)

Here R is the public reactant, P is the target product, B is an ordinary byproduct pool, and D is a more strongly degraded material reflected by the degradation-warning channel. A minimal kinetic representation is:

dR/dt = -(k1 + k2)R

dP/dt = k1 R - k3 P

dB/dt = k2 R + alpha k3 P

dD/dt = (1-alpha) k3 P

The temperature dependence could be represented locally by Arrhenius-like terms,

ki(T) = Ai(catalyst, solvent) exp[-Ei/(RT)],

but the data do not determine Ai or Ei separately. Catalyst and solvent should be treated as modifying both activity and pathway partitioning, rather than merely multiplying all rates by a common factor.

The observables are approximately related by:

conversion = 1 - R/R0

selectivity = P/(R0-R)

yield = P/R0 approximately conversion x selectivity.

This relationship is directly supported by the results. For example, Batch 8 gave conversion 0.8473 and selectivity 0.6392; their product is about 0.5416, close to the observed yield of 0.5418. Batch 12 gave 0.7756 x 0.7037 = about 0.5458, close to its measured yield of 0.5483. Small mismatches are consistent with the declared measurement noise.

3. Catalyst and solvent effects

The clearest solvent comparison at a common nominal thermal program is among the Catalyst A batches at 360 K for 5400 s:

- Batch 5, ethanol: conversion 0.7280, selectivity 0.4185, yield 0.3284, byproduct 0.4299, score 0.1407.
- Batch 3, acetonitrile: conversion 0.7883, selectivity 0.5356, yield 0.4362, byproduct 0.3853, score 0.2060.
- Batch 4, toluene: conversion 0.8228, selectivity 0.4576, yield 0.3831, byproduct 0.4749, score 0.1647.

Thus, solvent effects cannot be described solely as faster or slower reaction. Toluene produced the highest conversion of these three but also the largest byproduct signal and poorer selectivity. Acetonitrile gave the best balance, suggesting that it favors k1 relative to k2 and/or suppresses k3. Ethanol was both less productive and less selective with Catalyst A.

The clearest catalyst comparison uses ethanol at 360 K for 5400 s:

- Batch 5, Catalyst A: conversion 0.7280, selectivity 0.4185, yield 0.3284, byproduct 0.4299.
- Batch 2, Catalyst B: conversion 0.7658, selectivity 0.6042, yield 0.4691, byproduct 0.2983.
- Batch 6, Catalyst C: conversion 0.6923, selectivity 0.5065, yield 0.3492, byproduct 0.3557.
- Batch 7, Catalyst D: conversion 0.7378, selectivity 0.5520, yield 0.3941, byproduct 0.3318.

Catalyst B was the strongest formulation in this comparison because it increased target selectivity while keeping byproduct formation relatively low. Catalyst D was second, Catalyst C intermediate, and Catalyst A worst. The catalyst ranking is therefore primarily a selectivity ranking rather than simply an activity ranking.

Batch 8 combined the two favorable categories, acetonitrile and Catalyst B, at 360 K for 5400 s. It produced conversion 0.8473, selectivity 0.6392, yield 0.5418, byproduct 0.3108, degradation warning 0.1672, risk 0.1959, and score 0.2731. This exceeded either Catalyst A in acetonitrile (Batch 3) or Catalyst B in ethanol (Batch 2), supporting beneficial catalyst-solvent coupling. However, because the full 4 x 4 categorical matrix was not measured, the interaction cannot be quantitatively separated from additive catalyst and solvent effects.

4. Temperature and residence-time behavior

Batches 8-10 isolate temperature reasonably well with Catalyst B, acetonitrile, and 5400 s heating:

- Batch 8, 360 K: conversion 0.8473, selectivity 0.6392, yield 0.5418, byproduct 0.3108, degradation 0.1672, risk 0.1959, score 0.2731.
- Batch 10, 370 K: conversion 0.8866, selectivity 0.6201, yield 0.5699, byproduct 0.3396, degradation 0.1835, risk 0.2056, score 0.2791.
- Batch 9, 380 K: conversion 0.9417, selectivity 0.5968, yield 0.5616, byproduct 0.3624, degradation 0.2134, risk 0.2187, score 0.2696.

Increasing temperature clearly increased conversion, but it also reduced selectivity and increased both byproduct and degradation channels. Yield peaked near 370 K in this small series, while the public score also peaked near 370 K and then declined. This suggests that undesired pathways have equal or greater effective temperature sensitivity than the desired pathway once substantial product has accumulated.

Residence time shows the same conversion-selectivity tradeoff. At 360 K, extending the run from 5400 s in Batch 8 to 7200 s in Batch 11 raised conversion from 0.8473 to 0.9290, but selectivity fell from 0.6392 to 0.5515. Yield decreased from 0.5418 to 0.5282, byproduct rose from 0.3108 to 0.4082, degradation rose from 0.1672 to 0.2470, and score fell from 0.2731 to 0.2521. This is strong evidence that continued heating after high conversion causes overreaction or product degradation rather than simply completing the desired transformation.

At 370 K, shortening the duration from 5400 s in Batch 10 to 3600 s in Batch 12 reduced conversion from 0.8866 to 0.7756 but improved selectivity from 0.6201 to 0.7037. The yield changed only modestly, from 0.5699 to 0.5483, while byproduct fell from 0.3396 to 0.2323 and degradation fell from 0.1835 to 0.0954. The score consequently increased from 0.2791 to the campaign maximum of 0.2840. This observation caused me to revise the optimization target away from maximum conversion or maximum isolated yield and toward stopping earlier, before secondary chemistry erodes selectivity.

5. Interpretation of the score and safety behavior

The score is not simply conversion or yield. Batch 10 had a slightly larger yield than Batch 12, yet Batch 12 had the better score because it had substantially better selectivity and smaller byproduct/degradation signals. I infer that the score rewards productive, selective conversion while penalizing undesirable products and possibly risk. I did not identify the exact hidden score equation.

Observed risk increased with thermal severity but stayed well inside the 0.35 constraint in every batch. In the optimized catalyst-solvent series it rose from about 0.196 in Batch 8 at 360 K/5400 s, to 0.206 in Batch 10 at 370 K/5400 s, and to 0.219 in Batch 9 at 380 K/5400 s. Batch 12 at 370 K/3600 s had risk about 0.197. The likely public-level model is a base contribution from charging materials plus an accumulated thermal contribution depending on temperature, duration, and solvent category. The data do not justify a more precise risk equation.

The visible cost channel saturated at 1 after catalyst charging, so this campaign cannot distinguish economic differences among the complete recipes. The repeated high-cost flag therefore provides little mechanistic discrimination.

6. Experiments that most shaped the explanation

Batch 1 was an initial low-severity reference using water, Catalyst A, 330 K, and 3600 s. It produced only 0.3143 conversion, 0.3705 selectivity, 0.1235 yield, and score 0.0315 at risk 0.0932. This established that mild conditions with that formulation were safe but kinetically inadequate.

Batches 3-5 showed that higher conversion is not automatically beneficial: toluene in Batch 4 gave more conversion than acetonitrile in Batch 3, but worse selectivity, byproduct, yield, and score. This prompted a pathway-partitioning interpretation of solvent effects.

Batches 2 and 5-7 identified Catalyst B as a strong selectivity-promoting category in ethanol. Batch 8 then showed that Catalyst B and acetonitrile work particularly well together.

Batches 8-10 established the rising-temperature tradeoff: conversion increased monotonically, whereas selectivity declined and byproduct/degradation rose. The optimum was therefore internal rather than located at the hottest tested condition.

Batch 11 provided the clearest evidence for time-dependent overreaction because longer heating increased conversion while decreasing both yield and score.

Batch 12 was decisive for the recommended stopping policy. Its 370 K/3600 s program deliberately accepted incomplete conversion and achieved the best score through high selectivity and low degradation.

7. Measurement uncertainty and assay consistency

The intermediate HPLC and final assay did not always agree exactly. In Batch 1, HPLC estimated yield 0.1319 and selectivity 0.4078, whereas the final assay gave yield 0.1235 and selectivity 0.3705. In Batch 2, HPLC gave yield 0.4563 and the final assay 0.4691. In Batch 9, HPLC gave yield 0.5819 while the final assay gave 0.5616. These differences are directionally inconsistent and are reasonably attributed to instrument noise, sampling, and process-proxy uncertainty rather than systematic reaction progress after termination. Therefore, small numerical differences between neighboring batches should not be overinterpreted. The broad temperature, time, catalyst, and solvent trends are larger and chemically coherent, but there were no true recipe replicates to quantify batch-to-batch variance.

8. Applicability and unresolved factors

The proposed model applies locally to the measured domain: 0.040 mol reagent in 0.080 L solvent with 0.005 mol catalyst, nominal temperatures of 330-380 K, durations of 3600-7200 s, and stirring near 700 rpm. Extrapolation outside that domain is speculative. In particular, no evidence establishes behavior at lower catalyst loading, altered concentration, staged addition, quenching before termination, temperatures above 380 K, or very short reaction times.

Reaction orders cannot be identified because reagent, solvent volume, and catalyst loading were not varied. Stirring dependence and mass-transfer limitation are also unidentifiable. Actual temperature trajectories were not fully observed, so nominal setpoint effects combine heat-up dynamics with intrinsic kinetics. The campaign cannot distinguish whether the degradation-warning signal arises directly from P, from B, or from an independent thermolysis pathway. Nor can it distinguish catalyst deactivation from substrate depletion or product inhibition.

9. Reasonable competing explanations

The preferred sequential-loss explanation, R -> P -> degradation, is supported by the worsening selectivity and increasing degradation warning at longer time and higher temperature. However, a purely parallel model remains plausible: R could react through desired and undesired channels, with the undesired channel having a larger activation energy. That model would also produce increasing conversion and decreasing selectivity as temperature rises. The time-series evidence in Batch 11 favors secondary product loss but does not prove it.

A second alternative is catalyst deactivation combined with a persistent noncatalytic side reaction. Early in the batch, active Catalyst B could produce P selectively; after deactivation, residual R might be consumed less selectively. This would mimic the observed late-time decline in selectivity without requiring direct P destruction.

A third alternative is that the degradation-warning channel is not a conserved chemical pool but a spectroscopic proxy correlated with thermal history. If so, its rise would still predict poorer operating performance but would not map one-to-one onto degraded product mass.

10. Working operational model

For prediction within the observed region, I would use the following qualitative pseudocode:

1. Select catalyst-solvent-specific k1, k2, and k3 values; Catalyst B plus acetonitrile has the most favorable k1/(k2+k3) balance observed.
2. Increase all rates with temperature, but increase undesired-pathway importance more rapidly above approximately 370 K.
3. Integrate R -> P with competing and secondary loss over the residence time.
4. Compute conversion from R depletion, yield from remaining P, and selectivity as yield/conversion.
5. Increase byproduct and degradation proxies with integrated undesired flux and thermal exposure.
6. Compute risk from charging plus a monotonic temperature-time severity term.
7. Prefer the stopping time that maximizes selective product performance, not the time that maximizes conversion.

Within the tested space, the best supported operating region is therefore Catalyst B in acetonitrile near a 370 K target with a comparatively short 3600 s heating period. This statement is an interpolation from observed batches, especially Batch 12, not a claim about real named chemistry or untested operating conditions.

## Q — Blind predictions

### Overall rationale

Predictions use the campaign-supported network of desired conversion competing with byproduct formation and subsequent thermal loss of target product. Yield was kept approximately consistent with conversion multiplied by selectivity, and byproduct signal approximately consistent with conversion minus yield. Catalyst B with acetonitrile was treated as the most favorable measured categorical combination. Temperature and time were modeled as increasing conversion while progressively lowering selectivity, with undesired chemistry accelerating particularly above the 370–380 K experimental range. The larger catalyst-to-reagent ratio in the queries was assumed to accelerate conversion, whereas the reduction from 700 to 400 rpm was assigned a smaller opposing effect. Quenching after a completed heat program was not assumed to reverse prior reaction. Prediction intervals include final-assay noise, unknown effects of the changed scale and stirring rate, and substantial model uncertainty for temperatures up to 460 K.

### Q01

The favorable Catalyst B–acetonitrile pairing should give nearly complete conversion at 420 K. However, this temperature is well above the studied optimum, so accelerated competing and secondary reactions are expected to lower selectivity and raise byproduct formation. The interval is wide because this is a temperature extrapolation and the lower stirring rate was not calibrated.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5800 | 0.4200 | 0.7400 |
| conversion | 0.9700 | 0.9000 | 1.0000 |
| safety_risk | 0.2900 | 0.2200 | 0.3800 |
| score | 0.1500 | 0.0700 | 0.2300 |
| selectivity | 0.4000 | 0.2700 | 0.5400 |
| yield | 0.3900 | 0.2600 | 0.5200 |

### Q02

Quenching occurs only after the full heating period, so I expect essentially the same final conversion and pathway partitioning as Q01. It should prevent further chemistry during handling, but termination already follows immediately; therefore, any chemical benefit is predicted to be smaller than the extrapolation uncertainty. Quenching may add a small operational-risk contribution rather than erase accumulated thermal risk.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5800 | 0.4200 | 0.7400 |
| conversion | 0.9700 | 0.9000 | 1.0000 |
| safety_risk | 0.2900 | 0.2200 | 0.3900 |
| score | 0.1500 | 0.0700 | 0.2300 |
| selectivity | 0.4000 | 0.2700 | 0.5400 |
| yield | 0.3900 | 0.2600 | 0.5200 |

### Q03

At 390 K for 3300 s, the increased catalyst-to-reagent ratio should provide high conversion despite 400 rpm stirring. This condition is only moderately beyond the campaign temperature range, so selectivity should remain appreciably better than at 420–450 K. It is predicted to be among the stronger-scoring queries.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3700 | 0.2400 | 0.5000 |
| conversion | 0.9000 | 0.8000 | 0.9700 |
| safety_risk | 0.2400 | 0.1800 | 0.3100 |
| score | 0.2600 | 0.1800 | 0.3300 |
| selectivity | 0.5900 | 0.4700 | 0.7000 |
| yield | 0.5300 | 0.4100 | 0.6400 |

### Q04

At 450 K, conversion should saturate, but the campaign trend indicates that undesired-pathway importance rises faster than desired production as temperature increases. I therefore predict severe selectivity loss, a dominant byproduct signal, and risk near or above the declared 0.35 limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8100 | 0.6500 | 0.9400 |
| conversion | 0.9950 | 0.9600 | 1.0000 |
| safety_risk | 0.3700 | 0.2700 | 0.5000 |
| score | 0.0350 | 0.0000 | 0.1100 |
| selectivity | 0.1800 | 0.0600 | 0.3300 |
| yield | 0.1800 | 0.0600 | 0.3300 |

### Q05

The short 1500 s residence time should limit overreaction even at 420 K. Conversion is predicted to be lower than Q01, but selectivity and yield retention should be much better. This mirrors the campaign observation that deliberately stopping earlier improved score despite incomplete conversion.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3000 | 0.1700 | 0.4400 |
| conversion | 0.8000 | 0.6500 | 0.9100 |
| safety_risk | 0.2100 | 0.1500 | 0.2800 |
| score | 0.2500 | 0.1600 | 0.3300 |
| selectivity | 0.6300 | 0.5000 | 0.7500 |
| yield | 0.5000 | 0.3800 | 0.6200 |

### Q06

The long 5100 s exposure at 420 K should drive conversion to saturation while allowing extensive secondary or competing chemistry. The expected result is much poorer selectivity than Q01 or Q05, a large byproduct fraction, low score, and a material chance of exceeding the safety limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7900 | 0.6200 | 0.9300 |
| conversion | 0.9950 | 0.9500 | 1.0000 |
| safety_risk | 0.3600 | 0.2700 | 0.4800 |
| score | 0.0450 | 0.0000 | 0.1300 |
| selectivity | 0.2100 | 0.0700 | 0.3700 |
| yield | 0.2100 | 0.0700 | 0.3700 |

### Q07

The first 390 K stage should accumulate target product, after which the 450 K stage can rapidly consume remaining reactant and degrade or divert accumulated product. This ordering is therefore predicted to be especially unfavorable for selectivity, although total conversion should be nearly complete.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7800 | 0.6000 | 0.9200 |
| conversion | 0.9950 | 0.9500 | 1.0000 |
| safety_risk | 0.3200 | 0.2300 | 0.4300 |
| score | 0.0500 | 0.0000 | 0.1400 |
| selectivity | 0.2200 | 0.0800 | 0.3900 |
| yield | 0.2200 | 0.0800 | 0.3900 |

### Q08

The initial 450 K stage should produce rapid conversion and substantial byproduct formation. Cooling to 390 K for the second stage cannot reverse that loss, but it should be less destructive to accumulated product than ending with the 450 K stage in Q07. I therefore predict modestly higher retained selectivity than Q07, with similarly high conversion and thermal risk.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7100 | 0.5200 | 0.8800 |
| conversion | 0.9900 | 0.9300 | 1.0000 |
| safety_risk | 0.3200 | 0.2300 | 0.4300 |
| score | 0.0850 | 0.0100 | 0.1800 |
| selectivity | 0.2800 | 0.1300 | 0.4500 |
| yield | 0.2800 | 0.1300 | 0.4500 |

### Q09

The 440 K temperature is strongly unfavorable to selectivity, but the 1500 s exposure limits the time available for secondary loss. The result should retain substantially more product than the longer high-temperature batches while giving high, though not necessarily complete, conversion.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4300 | 0.2800 | 0.5900 |
| conversion | 0.8900 | 0.7700 | 0.9700 |
| safety_risk | 0.2400 | 0.1700 | 0.3200 |
| score | 0.2100 | 0.1200 | 0.3000 |
| selectivity | 0.5200 | 0.3800 | 0.6500 |
| yield | 0.4600 | 0.3400 | 0.5900 |

### Q10

Because quenching follows the complete 1500 s heat treatment and is immediately followed by termination, the principal chemical metrics are predicted to match Q09 within assay and model uncertainty. The quench may stabilize the sample but is not expected to recover product already diverted during heating.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4300 | 0.2800 | 0.5900 |
| conversion | 0.8900 | 0.7700 | 0.9700 |
| safety_risk | 0.2450 | 0.1800 | 0.3300 |
| score | 0.2100 | 0.1200 | 0.3000 |
| selectivity | 0.5200 | 0.3800 | 0.6500 |
| yield | 0.4600 | 0.3400 | 0.5900 |

### Q11

This is closest to the studied temperature region. The longer 5700 s duration and higher catalyst-to-reagent ratio should raise conversion beyond campaign Batch 10, but the campaign's time trend predicts declining selectivity and increasing byproduct formation. Its score should remain moderate rather than improve with conversion alone.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4350 | 0.3000 | 0.5700 |
| conversion | 0.9450 | 0.8600 | 0.9900 |
| safety_risk | 0.2200 | 0.1700 | 0.2900 |
| score | 0.2300 | 0.1500 | 0.3100 |
| selectivity | 0.5400 | 0.4200 | 0.6500 |
| yield | 0.5100 | 0.3900 | 0.6200 |

### Q12

This condition combines the highest temperature with the longest duration and lies far outside the experimentally supported thermal region. Conversion should be effectively complete, but extensive competing reaction and product degradation are expected to leave little target product. It is also predicted to exceed the safety limit clearly. The intervals are especially broad because this is the most extreme extrapolation.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9500 | 0.7900 | 1.0000 |
| conversion | 0.9990 | 0.9700 | 1.0000 |
| safety_risk | 0.5600 | 0.3900 | 0.7600 |
| score | 0.0080 | 0.0000 | 0.0600 |
| selectivity | 0.0500 | 0.0000 | 0.1900 |
| yield | 0.0500 | 0.0000 | 0.1900 |

## K2 — Retrospective analysis

1. Assessment of the initial information

The initial packet made very few substantive kinetic or mechanistic claims. It explicitly said that no task-specific property dossier was available, that the catalyst identities were anonymous, and that solvent effects were calibrated categorical benchmark effects rather than predictions from ordinary solvent properties. Accordingly, there was no supplied rate law, catalyst ranking, solvent ranking, optimum temperature, or degradation mechanism to confirm or refute. Experimental evidence was designated as authoritative.

Several structural claims were supported operationally:

- The catalyst and solvent categories had reproducible-looking consequences large enough to exceed nominal assay noise. For example, under the common ethanol/360 K/5400 s setting, Catalyst B in Batch 2 gave final selectivity 0.6042 and yield 0.4691, whereas Catalyst A in Batch 5 gave 0.4185 and 0.3284. This supports the claim that the anonymous categories are meaningfully coupled to the simulated reaction.
- The public observables were mutually coherent. As noted in K1, yield was approximately conversion multiplied by selectivity: Batch 8 gave 0.8473 × 0.6392 ≈ 0.5416 versus observed yield 0.5418. That supports use of the public channels as a chemically interpretable mass-partition summary.
- The declared safety constraint was operationally meaningful and was respected: all observed campaign risks were below 0.35, with the largest around 0.219 in Batch 9.
- Differences between intermediate HPLC and final assay were of plausible instrumental magnitude and inconsistent direction, as K1 discussed for Batches 1, 2, and 9. This is compatible with, but does not independently validate, the stated synthetic noise contracts.

Nothing in the campaign contradicted the packet's warning not to infer real catalyst identities or real-solvent property mechanisms. That is an absence of counterevidence, not positive evidence that the benchmark categories reproduce real acetonitrile, ethanol, or toluene chemistry.

Important initial claims that remained untested include the detailed calibration, detection-limit, baseline-drift, and saturation contracts; I used processed estimates and did not systematically audit raw traces against those claims. The campaign also did not test whether changing scale, concentration, catalyst loading, or stirring follows any ordinary physical law.

There was no clear initial mechanistic claim that was directly refuted. A more relevant distinction concerns my own evolving assumptions. Early optimization implicitly treated increased conversion as likely beneficial. Batch 4 already supplied counterevidence: it had greater conversion than Batch 3, 0.8228 versus 0.7883, but worse yield, selectivity, byproduct, and score. I did correct that assumption in later choices and in K1. By contrast, the possibility that score differences as small as those between Batches 10 and 12 were dominated by run and assay noise was recognized in K1 but not fully reflected in the confidence of the sealed recommendation.

2. Experiments that formed or changed my judgments

Batch 1 was primarily a conservative baseline based on unverified intuition rather than prior task data: water, Catalyst A, 330 K, and 3600 s appeared likely to be safe. Its low conversion of 0.3143, yield of 0.1235, and score of 0.0315 established that this mild recipe was inadequate, but it did not isolate which of solvent, catalyst, temperature, or time was responsible.

Batch 2 was another broad exploratory jump—ethanol, Catalyst B, 360 K, and 5400 s—again relying substantially on guesswork. Its score of 0.2406 showed that large improvement was possible, but because four factors changed relative to Batch 1, it initially provided poor mechanistic attribution.

Batches 3–5 were the first deliberately comparative set. Holding Catalyst A and the 360 K/5400 s program fixed while changing solvent allowed the conclusion that solvent affected pathway partitioning rather than only rate. Batch 4 in toluene had the highest conversion of that subset but the worst byproduct signal, while Batch 3 in acetonitrile had the best yield and score. This comparison materially changed the search toward acetonitrile.

Batches 5–7, together with Batch 2, supplied the catalyst comparison in ethanol. Catalyst B in Batch 2 was clearly better than A, C, or D on the observed balance of selectivity and yield. This was a data-driven shift, although it assumed that catalyst rankings would transfer across solvents.

Batch 8 tested that transfer by pairing Catalyst B with acetonitrile. Its score of 0.2731 supported the combination and justified making it the platform for thermal optimization. This was one of the most consequential experiments because it converted two separate categorical observations into evidence for a useful combined recipe. It did not, however, identify whether the improvement was additive or a true catalyst–solvent interaction.

Batches 9 and 10 explored 380 and 370 K at 5400 s. Their results established a local temperature tradeoff: conversion increased from Batch 8 through Batch 9, while selectivity deteriorated and score peaked around the middle. Batch 9 was especially important because 0.9417 conversion did not produce the best yield or score.

Batch 11 extended the 360 K run to 7200 s. Relative to Batch 8, conversion increased from 0.8473 to 0.9290, but yield fell from 0.5418 to 0.5282, selectivity fell to 0.5515, and byproduct and degradation increased. This was the strongest evidence for overreaction or secondary loss and was central to the sequential-loss interpretation in K1.

Batch 12 shortened the 370 K program to 3600 s. Its conversion was only 0.7756, but selectivity was 0.7037, degradation warning 0.0954, and score 0.2840. It changed the operational judgment from “maximize conversion near 370 K” to “stop earlier to preserve selectivity.”

The later experimental choices therefore became increasingly data-driven, but important assumptions remained unverified: that categorical rankings transferred between conditions, that 700 rpm was adequate and comparable across batches, that a single intermediate measurement represented the batch, and that observed score differences larger than a few thousandths were actionable without replication.

3. Principal competing mechanisms and what the experiments distinguish

K1 preferred a network with parallel desired and undesired conversion plus secondary target loss:

R → P, R → B, and P → B/D.

The most important competing explanation is a purely parallel network in which R → P and R → B have different temperature dependencies, with no actual destruction of P. Higher temperature could then increase the undesired branching fraction and reproduce the decline in selectivity.

The campaign distinguishes these explanations only partially. Batch 11 provides evidence favoring secondary loss because extending the 360 K residence time increased conversion but decreased absolute yield, not merely selectivity. If the comparison were noise-free and perfectly matched, a decline in P while reaction continued would be difficult to explain by parallel consumption of residual R alone. However, Batches 8 and 11 were independent batches without replication, and the yield difference was only about 0.014. Thus, it is suggestive rather than decisive.

A second competitor is catalyst deactivation followed by a less-selective background reaction. Early active Catalyst B could produce P selectively; after deactivation, residual R could form B. This can cause declining cumulative selectivity without requiring P degradation. Existing endpoint data do not separate this from P → B/D.

A third competitor is product inhibition or equilibrium limitation. Accumulated P could slow the desired channel while leaving an undesired channel active. Again, endpoint conversion, yield, and selectivity alone cannot distinguish this from deactivation.

A fourth explanation concerns the degradation-warning channel itself. It may represent a genuine degraded material pool, but it could instead be a thermal-history-correlated spectroscopic proxy. Its monotonic association with severe conditions supports its predictive value but does not prove a mass-balanced degradation route.

The solvent comparisons demonstrate that categorical solvent choice changes more than the overall rate, because conversion and selectivity rankings differ. They do not identify whether the cause is stabilization of a transition state, catalyst speciation, solubility, or a benchmark-specific categorical parameter. Similarly, catalyst comparisons identify performance rankings only within the tested context; they do not reveal molecular catalytic cycles.

The approximate relation yield ≈ conversion × selectivity and byproduct ≈ conversion − yield supports a partition model, but it does not prove that the byproduct signal is a single species or that degradation is separate from the byproduct pool.

4. The single additional experiment I would choose

I would choose one within-batch time-course experiment designed to reduce batch-to-batch confounding:

- Add 0.080 L acetonitrile, 0.040 mol reagent, and 0.005 mol Catalyst B.
- Heat at 360 K and 700 rpm for 5400 s.
- Measure by HPLC immediately.
- Continue heating at 360 K and 700 rpm for another 1800 s.
- Terminate and perform the required final assay.

This directly revisits the Batch 8 versus Batch 11 comparison in a single vessel. I would record conversion, yield, selectivity, byproduct signal, degradation warning, and risk. Although HPLC and final assay have different noise models, the within-vessel design would remove much of the recipe and batch variation.

Possible outcomes would affect the interpretation as follows:

- If target yield clearly decreases while conversion, byproduct, and degradation warning increase, that would substantially strengthen the P → B/D secondary-loss mechanism.
- If target yield stays approximately constant while conversion and byproduct rise, the result would favor residual R being consumed through an increasingly undesired parallel pathway, catalyst deactivation, or product inhibition rather than direct P destruction.
- If target yield continues to rise but selectivity falls, the parallel-pathway model would become more compelling; longer time would still be operationally unfavorable, but “product degradation” would be too strong a description.
- If both measurements resemble one another within uncertainty, then the Batch 8/11 difference would look less secure and possibly dominated by between-batch or assay variation.
- If degradation warning rises without a corresponding decrease in target yield, it would support treating that channel as a thermal proxy rather than a direct measure of destroyed P.

A true isotopic or isolated-product challenge would distinguish mechanisms better, but it was not among the legal operations. The proposed experiment is therefore the strongest available test within the public action set.

5. Tradeoff between mechanistic identifiability and score optimization

The campaign increasingly prioritized operating score after the broad categorical screen. That was appropriate to the stated primary goal, but it reduced identifiability.

The main sacrifices of identifiability for optimization were:

- After Batch 8, four of the remaining batches concentrated on Catalyst B in acetonitrile. This efficiently optimized a promising region but left most of the 4 × 4 catalyst–solvent matrix unmeasured.
- Temperature and time were not explored in a balanced factorial design. Batch 9, Batch 10, Batch 11, and Batch 12 supplied useful local contrasts, but temperature, duration, and independent-batch noise were not fully separable.
- No exact recipe was replicated. Consequently, the variance of a completed batch and the statistical significance of the apparent optimum remain unknown.
- Catalyst loading, reagent concentration, solvent volume, and stirring speed were kept almost fixed. This improved comparability for optimization but made kinetic orders and transport effects unidentifiable.
- Intermediate measurements were generally taken only once near the endpoint, rather than at multiple time points. This conserved the limited nonfinal-instrument budget but left the kinetic network underdetermined.

There were also experiments that sacrificed immediate score for information. Batch 4 tested toluene with Catalyst A despite no evidence that it would be best. Batches 6 and 7 tested Catalysts C and D after Catalyst B already looked promising. Batch 9 deliberately increased temperature to 380 K and obtained a worse score, but it established that conversion saturation and thermal severity were not beneficial. Batch 11 likewise used a longer duration that was expected to test completion rather than maximize score; its inferior result was mechanistically informative.

The research goal shaped the compromise: I first screened categories, then exploited the best combination and used the remaining runs for local optimization. A more mechanism-centered program would have used replicates, a balanced catalyst–solvent design, and within-batch time courses. A pure optimization program might have abandoned inferior catalysts sooner and spent more batches refining 365–375 K and 3000–4500 s.

6. Underused evidence and weaknesses in the sealed blind predictions

The raw characterization artifacts were underused. I relied mainly on processed estimates and a few peak summaries rather than inspecting chromatographic shapes, minor peaks, baselines, saturation flags, missingness metadata, or replicate-level signals. Such evidence might have helped determine whether the byproduct proxy was one stable peak, whether new degradation peaks appeared at high severity, and whether assay discrepancies reflected noise or changing composition.

The operation-level risk deltas were also underexploited. They could have been organized into charging, solvent, temperature, and duration contributions. Instead, K1 gave only a qualitative risk model. That weakness became important in the blind predictions, where scale, concentration, and much higher temperatures changed simultaneously.

Actual thermal response was not fully used. Batch 1 showed that the vessel approached its target during heating, but I did not reconstruct or compare temperature trajectories across scale and solvent. The blind batches used only 0.005 L rather than 0.080 L, so assuming a similar effective temperature exposure was particularly uncertain.

The sealed predictions for Q04, Q06, and Q12 are the least reliable single-stage predictions because they extrapolate to 450–460 K and, for Q12, to 6300 s. K1 explicitly restricted its local applicability to approximately 330–380 K, 3600–7200 s, fixed charge amounts, and stirring near 700 rpm. Q12 is far outside the temperature range and combines that extrapolation with a new scale, concentration, catalyst fraction, and 400 rpm stirring.

Q07 and Q08 are also highly unreliable because they require path-dependent predictions for two-stage heating. The campaign contained no reversed-order thermal sequences. My claim that ending with the 450 K stage in Q07 would be more destructive than beginning with it in Q08 follows the proposed secondary-loss mechanism, but it was not established experimentally.

Q02 and Q10 are uncertain for a different reason: no campaign batch used quenching. The sealed prediction treated quenching after the heat program as chemically almost neutral and allowed only a small risk effect. That is an unsupported assumption about the simulator's quench semantics.

Even Q03, Q05, Q09, and Q11 contain major extrapolations. The blind batches changed reagent concentration from 0.5 to 0.6 mol/L, catalyst-to-reagent ratio from 12.5% to 17.5%, total volume from 0.080 L to 0.005 L, and stirring from mostly 700 to 400 rpm. K1 expressly said that loading, concentration, scale, and stirring laws were unidentified. Nevertheless, the sealed rationale assumed that the higher catalyst fraction accelerated conversion and that reduced stirring supplied a smaller opposing effect. Those were guesses, not campaign-derived relationships.

Several prediction intervals were probably too narrow. In particular:

- The Q04 conversion interval of 0.96–1.00 and Q12 conversion interval of 0.97–1.00 express excessive confidence in saturation despite unmeasured high-temperature behavior and possible catalyst deactivation.
- The Q12 selectivity and yield intervals of 0–0.19 acknowledge severe uncertainty but may still be too narrow if the benchmark clips, deactivates, or changes regimes at extreme temperature.
- Safety intervals for Q01–Q11 may be too narrow because the risk dependence on absolute charge, concentration, small volume, and quenching was never identified.
- Score intervals are vulnerable because I never recovered the public score equation. I used an empirical association between yield, byproduct, and observed scores, then extrapolated it into regions with possible safety violations and severe degradation.
- The paired predictions Q01/Q02 and Q09/Q10 may be overconfidently similar because quench behavior was entirely untested.

These weaknesses are partly consistent with K1, which explicitly labeled extrapolation beyond the measured domain as speculative. However, the numerical precision of the sealed Q predictions does not fully reflect that warning. Giving point estimates to two or three decimal places can imply more calibration than the evidence supports. No truth feedback has been supplied, so this is a prospective critique of evidential support, not a post hoc reaction to prediction errors.

7. Limitations of the sealed recommendation

Batch 12 was the sample-in highest observed score, not a proven optimum. Its final score was about 0.2840, compared with about 0.2791 for Batch 10 and 0.2731 for Batch 8. The Batch 12–Batch 10 difference was only about 0.005, smaller than several observed HPLC/final-assay discrepancies and comparable to plausible batch noise. Without replication, it is not established that Batch 12 has the highest expected score.

The recommendation is also conditional on the exact tested recipe: 0.040 mol reagent, 0.080 L acetonitrile, 0.005 mol Catalyst B, a 370 K target, 3600 s, and 700 rpm. K1 correctly described it as the best supported region rather than a universal chemical optimum, but the sealed selection necessarily chose one batch.

Repeatability should be tested by several exact replicates of Batch 12, with the distribution of final score, yield, selectivity, byproduct, degradation warning, and safety risk reported. Replication should also include intermediate HPLC to assess whether assay discrepancies are random and whether the product distribution is stable at termination.

Local robustness should be tested with a compact response-surface design around the recommendation, for example temperatures near 365, 370, and 375 K and durations near 3000, 3600, and 4200 s. Small perturbations in stirring and charge amounts would reveal whether the apparent optimum is broad and operationally forgiving or narrow and fragile. Robust optimization should consider the lower confidence bound on score and the upper confidence bound on safety risk, not only mean score.

Material robustness requires testing nearby catalyst and solvent categories under the same local thermal design. Batch 8 supported Catalyst B with acetonitrile, but the incomplete categorical matrix means another interaction could have been missed. Transfer to different catalyst lots or real materials cannot be claimed because the benchmark catalysts are anonymous and the solvent effects are simulator-specific categories.

Cross-world generalization would require repeating the design in independently initialized worlds or benchmark instances. The present campaign observed one world realization. A recipe can be sample-in best because it exploited that realization's latent categorical parameters without being best elsewhere.

Finally, optimality would require either a sufficiently dense local/global search with replication or a validated response model covering all legal variables. Neither was obtained. The defensible statement is therefore: Batch 12 was the highest-scoring completed batch observed in this campaign and remained comfortably below the safety limit. It was not demonstrated to be uniquely optimal, globally optimal, statistically superior to Batch 10, or transferable beyond the tested benchmark world.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 85.8 | none | 0 |
| Q | yes | 0 | 118.4 | none | 0 |
| K2 | yes | 0 | 96.9 | none | 0 |

## Scope note

This report contains only information available before truth release. Reference truth, prediction scoring, and recommendation retests are intentionally absent because the full 60-task block has not yet completed.
