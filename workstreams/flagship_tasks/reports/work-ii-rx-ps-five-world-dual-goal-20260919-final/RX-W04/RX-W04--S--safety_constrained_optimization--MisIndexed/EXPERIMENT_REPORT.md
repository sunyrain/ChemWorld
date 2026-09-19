# RX-W04--S--safety_constrained_optimization--MisIndexed

## Run summary

- World: `RX-W04`
- Locus: `S`
- Goal: `safety_constrained_optimization`
- Arm: `MisIndexed`
- Status: `completed`
- Source status: `completed`
- Experimental sessions: `12/12`
- Operations: `84`
- Exact replay verified: `True`
- Rollbacks: `[]`
- Posttest chain sealed: `True`

### Recovery status

- Effective result location: `posttest-repair-v11`
- Recovery version: `recovery-v11-parallel4-transport-repair`
- Repaired stages: `K1, Q, K2`
- Source experiments rerun: `False`
- Original source thread reused: `True`
- Truth revealed during recovery: `False`

## Sealed recommendation

- Selected batch: `8`
- Rationale: Batch 8 achieved the highest observed safe score (0.3363) while remaining comfortably below the 0.35 safety limit (risk 0.1642), using water, Catalyst B, and a 370 K target for 5400 s.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S0 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.2467 | 0.6249 | 0.4105 | 0.1418 | 0.0019 | 0.1099 | 0.1465 |
| 2 | S1 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 370 K x 5400 s @ 700 rpm | no | 0.5142 | 0.5868 | 0.8707 | 0.3761 | 0.1398 | 0.1838 | 0.2567 |
| 3 | S2 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 370 K x 5400 s @ 700 rpm | no | 0.4778 | 0.5300 | 0.9109 | 0.4475 | 0.1142 | 0.1994 | 0.2250 |
| 4 | S3 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 370 K x 5400 s @ 700 rpm | no | 0.5863 | 0.6275 | 0.9367 | 0.3563 | 0.1530 | 0.2220 | 0.2852 |
| 5 | S3 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 370 K x 5400 s @ 700 rpm | no | 0.4614 | 0.5202 | 0.9111 | 0.4503 | 0.2007 | 0.2156 | 0.2087 |
| 6 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 370 K x 5400 s @ 700 rpm | no | 0.6499 | 0.6701 | 0.9787 | 0.3437 | 0.1969 | 0.2304 | 0.3217 |
| 7 | S3 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 370 K x 5400 s @ 700 rpm | no | 0.5223 | 0.5594 | 0.9168 | 0.4021 | 0.0862 | 0.2134 | 0.2444 |
| 8 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 370 K x 5400 s @ 700 rpm | no | 0.6042 | 0.7443 | 0.8246 | 0.2220 | 0.0743 | 0.1642 | 0.3363 |
| 9 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 370 K x 5400 s @ 700 rpm | no | 0.5766 | 0.6036 | 0.9706 | 0.3960 | 0.2462 | 0.2158 | 0.2815 |
| 10 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 10800 s @ 700 rpm | no | 0.5849 | 0.6417 | 0.9040 | 0.3227 | 0.1706 | 0.1559 | 0.3146 |
| 11 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 390 K x 3600 s @ 700 rpm | no | 0.6048 | 0.7619 | 0.7773 | 0.1991 | 0.0539 | 0.2007 | 0.3198 |
| 12 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 380 K x 4500 s @ 700 rpm | no | 0.6105 | 0.7365 | 0.8183 | 0.1923 | 0.0785 | 0.1785 | 0.3298 |

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
    "byproduct_signal": 0.14176885783672333,
    "conversion": 0.41045308113098145,
    "cost": 1.0,
    "degradation_warning": 0.001886937185190618,
    "safety_risk": 0.10985220968723297,
    "score": 0.14651484787464142,
    "selectivity": 0.6249381899833679,
    "virtual_spectrum_summary": 0.07882198691368103,
    "yield": 0.24667121469974518
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
  "end_step": 14,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.3761070966720581,
    "conversion": 0.8707416653633118,
    "cost": 1.0,
    "degradation_warning": 0.13982491195201874,
    "safety_risk": 0.1838381141424179,
    "score": 0.256721556186676,
    "selectivity": 0.5868324637413025,
    "virtual_spectrum_summary": 0.26978009939193726,
    "yield": 0.5141660571098328
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
  "end_step": 21,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.4475304186344147,
    "conversion": 0.9109452962875366,
    "cost": 1.0,
    "degradation_warning": 0.11416847258806229,
    "safety_risk": 0.1993904709815979,
    "score": 0.22500158846378326,
    "selectivity": 0.5299820303916931,
    "virtual_spectrum_summary": 0.2975175380706787,
    "yield": 0.47784313559532166
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
      "catalyst": 3,
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
  "end_step": 28,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.3562796115875244,
    "conversion": 0.936747133731842,
    "cost": 1.0,
    "degradation_warning": 0.15297864377498627,
    "safety_risk": 0.22197754681110382,
    "score": 0.2851646840572357,
    "selectivity": 0.62746262550354,
    "virtual_spectrum_summary": 0.26479417085647583,
    "yield": 0.5862854719161987
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
  "end_step": 35,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.45025599002838135,
    "conversion": 0.9110689163208008,
    "cost": 1.0,
    "degradation_warning": 0.20070023834705353,
    "safety_risk": 0.215620219707489,
    "score": 0.20870915055274963,
    "selectivity": 0.5202307105064392,
    "virtual_spectrum_summary": 0.33795589208602905,
    "yield": 0.4614342153072357
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
  "end_step": 42,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.343736469745636,
    "conversion": 0.9787471294403076,
    "cost": 1.0,
    "degradation_warning": 0.19690796732902527,
    "safety_risk": 0.23037084937095642,
    "score": 0.32169145345687866,
    "selectivity": 0.6701257824897766,
    "virtual_spectrum_summary": 0.2776636481285095,
    "yield": 0.6498804688453674
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
      "catalyst": 2,
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
  "end_step": 49,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.4020989239215851,
    "conversion": 0.916832447052002,
    "cost": 1.0,
    "degradation_warning": 0.0861738845705986,
    "safety_risk": 0.21342134475708008,
    "score": 0.2444198727607727,
    "selectivity": 0.5594461560249329,
    "virtual_spectrum_summary": 0.25993266701698303,
    "yield": 0.5222867131233215
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
  "end_step": 56,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.22203974425792694,
    "conversion": 0.8246043920516968,
    "cost": 1.0,
    "degradation_warning": 0.07434025406837463,
    "safety_risk": 0.1641862839460373,
    "score": 0.33630505204200745,
    "selectivity": 0.7442734837532043,
    "virtual_spectrum_summary": 0.1555749624967575,
    "yield": 0.604150116443634
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
  "end_step": 63,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.39602428674697876,
    "conversion": 0.9706289172172546,
    "cost": 1.0,
    "degradation_warning": 0.2461666315793991,
    "safety_risk": 0.2157830148935318,
    "score": 0.2815049886703491,
    "selectivity": 0.6036185026168823,
    "virtual_spectrum_summary": 0.3285883367061615,
    "yield": 0.5765995979309082
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
      "stirring_speed_rpm": 700,
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
    "byproduct_signal": 0.322689026594162,
    "conversion": 0.9040166139602661,
    "cost": 1.0,
    "degradation_warning": 0.1706053614616394,
    "safety_risk": 0.15594539046287537,
    "score": 0.31462234258651733,
    "selectivity": 0.6417489647865295,
    "virtual_spectrum_summary": 0.2542513608932495,
    "yield": 0.5848972201347351
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
  "end_step": 77,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.19907481968402863,
    "conversion": 0.7773239612579346,
    "cost": 1.0,
    "degradation_warning": 0.05390297248959541,
    "safety_risk": 0.2007054090499878,
    "score": 0.31981074810028076,
    "selectivity": 0.761889636516571,
    "virtual_spectrum_summary": 0.13374748826026917,
    "yield": 0.6048083901405334
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
      "duration_s": 4500,
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
  "end_step": 84,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.19225937128067017,
    "conversion": 0.8182674050331116,
    "cost": 1.0,
    "degradation_warning": 0.07850893586874008,
    "safety_risk": 0.17845170199871063,
    "score": 0.329833060503006,
    "selectivity": 0.7365045547485352,
    "virtual_spectrum_summary": 0.14107167720794678,
    "yield": 0.6104586124420166
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

1. Scope and evidence base

This report concerns the bounded synthetic reaction-and-thermal world explored in twelve completed batches. The catalysts are anonymous benchmark formulations, and solvent effects are categorical effects defined by this world; they should not be interpreted as predictions about named real catalysts or real laboratory chemistry. Every completed batch used 0.080 L solvent, 0.040 mol limiting reagent, and 0.005 mol catalyst. Batch 1 used 600 rpm; the remaining batches used 700 rpm. Consequently, the evidence primarily identifies categorical catalyst and solvent effects and a limited time–temperature response. It does not identify concentration dependence, catalyst order, mixing dependence, or scale dependence.

The principal final-assay observables were conversion, target yield, selectivity, byproduct signal, degradation warning, safety risk, and the public score. Numerical differences of only a few hundredths should not be overinterpreted because every condition was run once and the assays have declared noise.

2. Working process model

A compact model consistent with the observations is:

R → P, with rate kP(C,S,T)
R → B, with rate kB(C,S,T)
P → D or B, with rate kD(C,S,T)
P → R, with possible reverse rate kr(C,S,T)

Here R is the public reactant, P the target product, B a collective undesired-product pool, C catalyst identity and loading, S solvent identity, and T the evolving liquid temperature. The reverse step is included because the initial information stated that an appreciable reverse channel might exist, not because this campaign proved it.

A corresponding qualitative kinetic system is:

dR/dt = -kP R - kB R + kr P
dP/dt = kP R - kr P - kD P
dB/dt = kB R + alpha kD P
dD/dt = (1-alpha) kD P

The rate constants may be represented locally by an Arrhenius-like form,

ki = Ai(C,S) exp[-Ei(C,S)/(Rgas T)],

but the campaign does not contain enough orthogonal temperature data to estimate Ai or Ei. Catalyst and solvent may change both prefactors and activation barriers, so their effects should not be reduced to a single scalar activity factor.

The observable relationships are approximately, but not exactly:

conversion ≈ 1 - R/R0
yield ≈ P/R0
selectivity ≈ P/(R0-R)

Thus yield should often be close to conversion multiplied by selectivity. This was approximately true in several batches. For example, batch 8 had conversion 0.8246 and selectivity 0.7443, whose product is about 0.614, close to the observed yield of 0.6042. Deviations can arise from assay noise, degradation channels, and the exact synthetic definitions of the public observables.

The byproduct signal generally moved inversely with selectivity. It should be interpreted as an aggregate proxy rather than a direct material balance. Degradation warning is evidence for a distinct damage channel but is not sufficient to determine whether target product, reactant, or byproduct is degrading.

3. Catalyst effects

The most informative catalyst comparison was made in toluene at 370 K for 5400 s with otherwise matched recipes:

• Batch 5, Catalyst A: conversion 0.9111, selectivity 0.5202, yield 0.4614, byproduct signal 0.4503, degradation warning 0.2007, score 0.2087.
• Batch 6, Catalyst B: conversion 0.9787, selectivity 0.6701, yield 0.6499, byproduct signal 0.3437, degradation warning 0.1969, score 0.3217.
• Batch 7, Catalyst C: conversion 0.9168, selectivity 0.5594, yield 0.5223, byproduct signal 0.4021, degradation warning 0.0862, score 0.2444.
• Batch 4, Catalyst D: conversion 0.9367, selectivity 0.6275, yield 0.5863, byproduct signal 0.3563, degradation warning 0.1530, score 0.2852.

Under that condition, Catalyst B was the strongest overall formulation. It raised conversion and target yield while retaining better selectivity than A or C. Catalyst C had the lowest degradation warning but did not translate that advantage into comparable yield or score. This means the catalysts probably alter branching between desired and undesired pathways, not merely the common reaction rate.

The data do not establish that Catalyst B is best under every solvent, temperature, or loading. Catalyst–solvent and catalyst–temperature interactions remain possible. Batch 1 used Catalyst A in water at 350 K, while batches 2–4 changed catalyst and solvent together; those early results cannot be used as clean catalyst comparisons.

4. Solvent effects

The clearest solvent comparison used Catalyst B at 370 K for 5400 s:

• Batch 8, water: conversion 0.8246, selectivity 0.7443, yield 0.6042, byproduct signal 0.2220, degradation warning 0.0743, risk 0.1642, score 0.3363.
• Batch 2, ethanol: conversion 0.8707, selectivity 0.5868, yield 0.5142, byproduct signal 0.3761, degradation warning 0.1398, risk 0.1838, score 0.2567.
• Batch 9, acetonitrile: conversion 0.9706, selectivity 0.6036, yield 0.5766, byproduct signal 0.3960, degradation warning 0.2462, risk 0.2158, score 0.2815.
• Batch 6, toluene: conversion 0.9787, selectivity 0.6701, yield 0.6499, byproduct signal 0.3437, degradation warning 0.1969, risk 0.2304, score 0.3217.

Water produced the lowest conversion in this comparison but the highest selectivity, lowest byproduct signal, lowest degradation warning, lowest risk, and highest score. Toluene produced the greatest target yield but incurred more byproduct, degradation, and risk. Acetonitrile drove high conversion but showed particularly high degradation warning. Ethanol was intermediate in conversion and risk but had relatively poor selectivity.

A plausible interpretation is that solvent identity changes several coupled quantities: desired rate kP, undesired rate kB, degradation rate kD, possibly the reverse rate kr, and the safety model. Water appears to suppress undesired chemistry and thermal risk more strongly than it suppresses target formation. Toluene and acetonitrile appear more kinetically aggressive but less favorable for clean, safe operation. These are world-specific categorical conclusions; no molecular property explanation is justified by the supplied evidence.

5. Time and temperature effects

The most useful thermal series used water and Catalyst B:

• Batch 8: 370 K for 5400 s; conversion 0.8246, selectivity 0.7443, yield 0.6042, byproduct 0.2220, degradation 0.0743, risk 0.1642, score 0.3363.
• Batch 10: 350 K for 10800 s; conversion 0.9040, selectivity 0.6417, yield 0.5849, byproduct 0.3227, degradation 0.1706, risk 0.1559, score 0.3146.
• Batch 11: 390 K for 3600 s; conversion 0.7773, selectivity 0.7619, yield 0.6048, byproduct 0.1991, degradation 0.0539, risk 0.2007, score 0.3198.
• Batch 12: 380 K for 4500 s; conversion 0.8183, selectivity 0.7365, yield 0.6105, byproduct 0.1923, degradation 0.0785, risk 0.1785, score 0.3298.

These conditions do not form a balanced factorial design, so separate temperature and time coefficients cannot be estimated. Nevertheless, several qualitative conclusions are supported.

First, additional cumulative exposure did not monotonically improve target yield. Batch 10 had the highest conversion in this series but lower yield and markedly lower selectivity than batch 8. This implies that driving reactant consumption harder also promotes undesired products or target loss.

Second, relatively hot, short treatments preserved target yield and selectivity reasonably well but increased safety risk. Batch 11 had essentially the same yield as batch 8 and slightly higher selectivity, yet its risk rose from 0.1642 to 0.2007 and its score fell from 0.3363 to 0.3198.

Third, the public score has an interior operating optimum. It does not reward conversion or yield without regard to selectivity, byproduct formation, degradation, and safety. Batch 12 gave the highest target yield in the local water/Catalyst B series, 0.6105, but batch 8 still had the highest score because of its more favorable total balance.

The observations are compatible with a reaction that initially forms P efficiently and then increasingly populates B or D as exposure continues. They are also compatible with reversible P formation plus irreversible sinks. They do not prove which explanation is correct.

4. Safety and score coupling

Safety risk depended on both formulation and thermal program. All completed batches remained below the declared limit of 0.35. Among matched Catalyst B experiments at 370 K for 5400 s, risk increased from water at 0.1642 to ethanol at 0.1838, acetonitrile at 0.2158, and toluene at 0.2304. In the water/Catalyst B thermal series, risk rose with hotter operation even when duration was shorter: 0.1559 for 350 K/10800 s, 0.1642 for 370 K/5400 s, 0.1785 for 380 K/4500 s, and 0.2007 for 390 K/3600 s.

This suggests that risk is not simply proportional to elapsed time. A qualitative model is:

risk = formulation baseline + thermal-state penalty + exposure penalty + possible reaction-intensity contribution.

The thermal-state penalty appears strongly temperature-sensitive. Solvent adds a categorical offset or modifies thermal sensitivity. Catalyst effects on risk cannot be isolated cleanly because catalyst comparisons showed small risk differences and were not replicated.

The exact scoring equation was not disclosed. Empirically, high yield and selectivity help, whereas risk, byproduct burden, and degradation reduce performance. The ranking of batches 8, 11, and 12 demonstrates that score cannot be treated as yield alone. Any numerical score equation beyond this qualitative relation would be conjectural.

5. How the interpretation developed

Batch 1 established a safe but low-performing baseline in water/Catalyst A: final conversion 0.4105, selectivity 0.6249, yield 0.2467, risk 0.1099, and score 0.1465.

Batches 2–4 showed that much higher conversion and yield were accessible, but they changed catalyst and solvent simultaneously. They broadened the observed space without identifying causality. Batch 4, with score 0.2852, motivated controlled catalyst testing.

Batches 5–7, together with batch 4, established the catalyst ranking under matched toluene conditions and shifted attention to Catalyst B. Batches 8 and 9 then isolated solvent effects around Catalyst B. Batch 8 changed the optimization target from maximizing conversion to balancing conversion with selectivity, degradation, and risk: its conversion was lower than batches 6 and 9, but its score was higher.

Batches 10–12 explored the local water/Catalyst B time–temperature region. They changed the interpretation from a simple monotonically increasing exposure model to a competing-pathway model with an interior optimum. The fact that long low-temperature exposure increased conversion while worsening selectivity was particularly important.

Intermediate HPLC measurements generally agreed with the final qualitative rankings but sometimes differed by several hundredths. For example, batch 11’s intermediate HPLC gave conversion 0.7981, selectivity 0.7830, and yield 0.5915, whereas the final assay gave 0.7773, 0.7619, and 0.6048. Such differences are consistent with measurement uncertainty and possible evolution between observations. They caution against interpreting small endpoint differences as exact kinetic changes.

6. Recommended operating region

The sealed recommendation was batch 8: water, Catalyst B, 0.080 L solvent, 0.040 mol reagent, 0.005 mol catalyst, a 370 K target, 5400 s, and 700 rpm. It was selected because it achieved the highest observed score, 0.3363, at a risk of 0.1642, comfortably below the limit.

The surrounding data suggest a reasonably promising local region of approximately 370–380 K and 4500–5400 s under the same recipe. Batch 12, at 380 K for 4500 s, produced score 0.3298. This statement is an interpolation from sparse observations, not a proven robust operating window. Batch 8 is the sample-best condition, not a demonstrated global optimum.

7. Unidentified factors and competing explanations

Several important quantities remain unidentified:

• Reaction orders in reagent and catalyst, because their loadings were never varied.
• Concentration and volume effects, because all batches used the same nominal recipe.
• Mixing or mass-transfer effects, because stirring was almost constant.
• Catalyst deactivation, because there was no catalyst-aging or staged-addition experiment.
• True temperature trajectories, because target temperature was controlled but only limited public thermal deltas were retained in the comparison.
• Whether byproduct is formed directly from reactant or sequentially from target product.
• Whether the reverse target channel is appreciable.
• Whether degradation warning represents target destruction, reactant destruction, or a correlated independent process.
• Interaction effects outside the tested catalyst–solvent combinations.
• Repeatability and batch-to-batch process variance, because no exact replicate was run.

The strongest competing explanation to the reversible network is an irreversible consecutive/parallel model:

R → P,
R → B,
P → D.

This model explains the increased conversion but reduced selectivity in batch 10 without requiring P → R. Another alternative is catalyst deactivation accompanied by changing branching ratios. Endpoint assays alone cannot discriminate these mechanisms.

A time-resolved experiment at a fixed formulation would be most diagnostic. For example, following the batch 8 recipe at several heating times could show whether P rises and then falls, whether reactant reappears, and whether B or degradation signals grow after conversion plateaus. No such experiment was performed, so this remains a proposed test rather than evidence.

8. Applicability and uncertainty

The most defensible conclusions apply to approximately 350–390 K, 3600–10800 s, the fixed 0.5 mol/L nominal reagent concentration, 0.0625 mol/L nominal catalyst concentration, and the tested anonymous formulations. Even within this range, only the water/Catalyst B region received multiple thermal observations.

Interpolation near batches 8 and 12 is more credible than extrapolation to much higher temperatures, very different times, different catalyst amounts, different concentrations, or different stirring speeds. Predictions outside the observed domain should use broad uncertainty because Arrhenius curvature, equilibrium shifts, catalyst deactivation, transport changes, or new degradation regimes could appear.

In summary, this world is best described provisionally as a catalyst- and solvent-dependent competing-pathway system. Catalyst B supplies the best observed desired-pathway balance. Water reduces conversion relative to more aggressive solvents but improves selectivity, degradation behavior, risk, and overall score. Temperature and time jointly determine conversion and secondary loss, producing a safe-score optimum at intermediate exposure. Reversibility remains plausible but unproven, and the available endpoint data cannot uniquely separate it from irreversible parallel and consecutive pathways.

## Q — Blind predictions

### Overall rationale

These predictions extrapolate from the campaign's controlled Catalyst B/acetonitrile result (batch 9: conversion 0.9706, yield 0.5766, selectivity 0.6036, byproduct signal 0.3960, risk 0.2158, score 0.2815 at 370 K for 5400 s) and from the water/Catalyst B thermal series in batches 8, 10, 11, and 12. I treated effective conversion exposure as increasing with catalyst loading, time, and an Arrhenius-like temperature factor, while selectivity declines under prolonged or extreme exposure because parallel byproduct formation, degradation, and possibly reverse cycling become important. Yield was centered near conversion multiplied by selectivity. Score was estimated as a safety-penalized function of yield and selectivity, consistent with the campaign observation that chemically similar hotter batches scored less well when risk increased. Risk was modeled as solvent- and temperature-sensitive, with weaker duration and catalyst-loading effects. Intervals are deliberately broad because the queries use smaller absolute charges, different catalyst ratios, 400 rpm stirring, temperatures up to 465 K, and combinations not directly studied. In particular, the 465 K cases are major extrapolations, and the mechanistic data cannot uniquely distinguish parallel byproduct formation from serial product degradation or a reversible target pathway.

### Q01

Low Catalyst B loading and only 1800 s should limit conversion despite 410 K. The short exposure should preserve comparatively good selectivity, but this is an extrapolation above the temperatures directly studied.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2800 | 0.1600 | 0.4200 |
| conversion | 0.6000 | 0.4200 | 0.7700 |
| safety_risk | 0.2600 | 0.1900 | 0.3400 |
| score | 0.2100 | 0.1200 | 0.2900 |
| selectivity | 0.7200 | 0.6000 | 0.8200 |
| yield | 0.4300 | 0.2700 | 0.5700 |

### Q02

The eightfold longer exposure should drive near-complete conversion even at low catalyst loading, while allowing substantial parallel byproduct formation, product loss, or reverse-channel cycling. Risk is predicted near the declared limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5800 | 0.4000 | 0.7500 |
| conversion | 0.9600 | 0.8600 | 1.0000 |
| safety_risk | 0.3500 | 0.2700 | 0.4600 |
| score | 0.1300 | 0.0400 | 0.2300 |
| selectivity | 0.4200 | 0.2500 | 0.5900 |
| yield | 0.4000 | 0.2200 | 0.5600 |

### Q03

The high catalyst loading should compensate for the short residence time and give high conversion. Relative to Q01, faster desired and undesired channels are both expected, producing higher yield but lower selectivity.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4300 | 0.2900 | 0.5800 |
| conversion | 0.9400 | 0.8200 | 1.0000 |
| safety_risk | 0.3000 | 0.2200 | 0.4000 |
| score | 0.2200 | 0.1200 | 0.3100 |
| selectivity | 0.5700 | 0.4200 | 0.7000 |
| yield | 0.5400 | 0.3900 | 0.6600 |

### Q04

High catalyst loading, 410 K, and 14400 s represent severe cumulative exposure. Conversion should saturate, but secondary byproduct and degradation pathways are expected to dominate; safety risk probably exceeds the limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7500 | 0.5700 | 0.9000 |
| conversion | 0.9900 | 0.9300 | 1.0000 |
| safety_risk | 0.4100 | 0.3100 | 0.5500 |
| score | 0.0600 | 0.0100 | 0.1500 |
| selectivity | 0.2500 | 0.1000 | 0.4300 |
| yield | 0.2500 | 0.0900 | 0.4200 |

### Q05

At 350 K, the low catalyst concentration should make conversion kinetically limited even over 7200 s. Lower thermal stress should preserve selectivity and keep risk comfortably below the limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2700 | 0.1500 | 0.4100 |
| conversion | 0.5800 | 0.3900 | 0.7600 |
| safety_risk | 0.1800 | 0.1300 | 0.2500 |
| score | 0.2300 | 0.1300 | 0.3200 |
| selectivity | 0.7300 | 0.6000 | 0.8300 |
| yield | 0.4200 | 0.2600 | 0.5700 |

### Q06

The long 465 K treatment is far outside the observed temperature range. Arrhenius acceleration should overcome the low catalyst loading, but severe secondary chemistry and a clear safety-limit violation are likely.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8200 | 0.6200 | 0.9600 |
| conversion | 0.9900 | 0.9100 | 1.0000 |
| safety_risk | 0.5600 | 0.4200 | 0.7200 |
| score | 0.0300 | 0.0000 | 0.1000 |
| selectivity | 0.1800 | 0.0400 | 0.3800 |
| yield | 0.1800 | 0.0400 | 0.3700 |

### Q07

High Catalyst B loading should give high conversion at 350 K without the extreme thermal penalty of the hotter cases. This is predicted to be among the better queries, though acetonitrile was inferior to water in the campaign.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3800 | 0.2400 | 0.5300 |
| conversion | 0.9400 | 0.8200 | 1.0000 |
| safety_risk | 0.2100 | 0.1500 | 0.2900 |
| score | 0.2800 | 0.1800 | 0.3700 |
| selectivity | 0.6200 | 0.4700 | 0.7400 |
| yield | 0.5800 | 0.4300 | 0.7000 |

### Q08

This combines the highest catalyst loading with 465 K for 7200 s. Conversion should be complete, but extensive degradation or diversion to byproduct is expected, with the largest safety risk in the set.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9000 | 0.7200 | 1.0000 |
| conversion | 0.9900 | 0.9400 | 1.0000 |
| safety_risk | 0.6800 | 0.5100 | 0.8500 |
| score | 0.0100 | 0.0000 | 0.0500 |
| selectivity | 0.1000 | 0.0100 | 0.2800 |
| yield | 0.0900 | 0.0100 | 0.2700 |

### Q09

Mid catalyst loading at 410 K for 7200 s should nearly exhaust reactant. The exposure is substantially harsher than the directly observed acetonitrile batch, so selectivity and score are expected to fall while risk approaches the limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6200 | 0.4500 | 0.7800 |
| conversion | 0.9800 | 0.9000 | 1.0000 |
| safety_risk | 0.3500 | 0.2700 | 0.4700 |
| score | 0.1200 | 0.0400 | 0.2200 |
| selectivity | 0.3800 | 0.2200 | 0.5500 |
| yield | 0.3700 | 0.2100 | 0.5300 |

### Q10

Quenching occurs only after the full heated residence, so it cannot undo chemistry or accumulated thermal risk. I predict only a small possible benefit from promptly arresting post-heat secondary reactions; the interval substantially overlaps Q09.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6000 | 0.4300 | 0.7700 |
| conversion | 0.9800 | 0.9000 | 1.0000 |
| safety_risk | 0.3500 | 0.2700 | 0.4700 |
| score | 0.1300 | 0.0400 | 0.2300 |
| selectivity | 0.4000 | 0.2300 | 0.5700 |
| yield | 0.3900 | 0.2200 | 0.5500 |

### Q11

The long 350 K treatment should achieve high conversion at the midpoint catalyst loading. Campaign batch 10 showed that long low-temperature exposure can still erode selectivity, so the predicted result is good but below the best short-to-moderate treatments.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4400 | 0.2900 | 0.6000 |
| conversion | 0.9500 | 0.8400 | 1.0000 |
| safety_risk | 0.2000 | 0.1400 | 0.2800 |
| score | 0.2500 | 0.1500 | 0.3400 |
| selectivity | 0.5600 | 0.4000 | 0.7000 |
| yield | 0.5300 | 0.3700 | 0.6600 |

### Q12

At 465 K, even 1800 s should provide substantial effective kinetic exposure at the midpoint catalyst loading. The short duration limits damage relative to Q06 and Q08, but both selectivity loss and safety-limit exceedance remain plausible.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5800 | 0.4000 | 0.7600 |
| conversion | 0.9700 | 0.8400 | 1.0000 |
| safety_risk | 0.4300 | 0.3200 | 0.5800 |
| score | 0.1200 | 0.0300 | 0.2300 |
| selectivity | 0.4200 | 0.2400 | 0.6000 |
| yield | 0.4100 | 0.2300 | 0.5800 |

## K2 — Retrospective analysis

1. Initial claims: support, contradiction, and remaining tests

The initial material contained one substantive mechanistic prior: “the target pathway may have an appreciable reverse channel,” assigned moderate confidence. K1 incorporated that possibility as P → R in the provisional network, but explicitly stated that the campaign did not prove it.

Some observations were compatible with reversibility. In particular, additional exposure did not monotonically improve target yield. Under water/Catalyst B, batch 8 at 370 K for 5400 s gave conversion 0.8246, selectivity 0.7443, and yield 0.6042, while batch 10 at 350 K for 10800 s gave higher conversion, 0.9040, but lower selectivity, 0.6417, and lower yield, 0.5849. That behavior could arise from reverse cycling, but it is equally compatible with direct byproduct formation or sequential product degradation.

Accordingly, the reverse-channel claim remains untested rather than supported. No experiment began from a product-rich state, showed reactant reappearing, or measured a sufficiently resolved trajectory in which conversion declined after reaching a maximum. High endpoint conversions in batches 6 and 9 do not refute reversibility because the equilibrium could favor product or irreversible sinks could mask the reverse flux. This is a case of “no decisive counterevidence was found,” not a case where decisive counterevidence appeared and I failed to revise the model.

The material packet also said that catalysts were anonymous benchmark formulations and solvent effects were world-specific categorical couplings. The strong catalyst and solvent differences are consistent with that description, but they do not validate any real-chemical explanation. No task-specific property dossier or named catalyst mechanism was supplied, so there were no additional substantive material claims to confirm or reject.

2. Experiments that formed or changed the interpretation

Batch 1 established the first baseline. Water/Catalyst A at 350 K for 3600 s gave conversion 0.4105, selectivity 0.6249, yield 0.2467, risk 0.1099, and score 0.1465. It showed that moderate operation was safe but that this formulation and exposure were not highly productive.

Batches 2–4 demonstrated that substantially higher conversion and score were accessible. However, each changed solvent and catalyst together, so these experiments expanded the response range without identifying causal factors. Batch 4, with toluene/Catalyst D at 370 K for 5400 s, reached score 0.2852 and motivated a controlled catalyst comparison.

Batches 5–7, interpreted together with batch 4, genuinely changed the catalyst judgment. Under matched toluene, 370 K, and 5400 s conditions, Catalyst B in batch 6 produced yield 0.6499 and score 0.3217, compared with scores 0.2087 for A, 0.2444 for C, and 0.2852 for D. This supported K1’s specific conclusion that Catalyst B offered the best observed balance under that condition and that catalysts affected pathway branching rather than merely multiplying a common rate.

Batches 8 and 9 changed the solvent interpretation. With Catalyst B at 370 K for 5400 s, batch 8 in water gave score 0.3363, risk 0.1642, selectivity 0.7443, and byproduct signal 0.2220. Batch 9 in acetonitrile gave higher conversion, 0.9706, but selectivity 0.6036, degradation warning 0.2462, risk 0.2158, and score 0.2815. Together with batches 2 and 6, these results shifted the objective from maximizing conversion toward balancing desired formation, secondary chemistry, and safety.

Batches 10–12 modified the simple “more thermal exposure is better” interpretation. Batch 10’s long, lower-temperature treatment raised conversion relative to batch 8 but worsened selectivity and degradation. Batch 11 maintained yield at 0.6048 and selectivity at 0.7619 but raised risk to 0.2007, reducing its score to 0.3198. Batch 12 obtained yield 0.6105 but still scored below batch 8. These observations led K1 to propose an interior safe-score optimum and competing desired and undesired pathways.

Several important choices were initially guesses rather than data-driven conclusions. The batch 1 condition was a cautious starting point. The paired solvent/catalyst changes in batches 2–4 were chosen for broad exploration, not clean identification. Using the maximum common reagent, solvent, and catalyst charges in every batch was convenient because twelve equal recipes matched the total campaign stocks; it was not based on an established catalyst order or concentration optimum. The initial selection of 370 K for 5400 s was heuristic. Later temperature and time choices were increasingly informed by prior batches, although no fitted kinetic model dictated their precise values.

3. Principal competing mechanisms and what can be distinguished

K1’s working network was R → P, R → B, P → D or B, and possibly P → R. The most important competing explanations are:

• Parallel competition: reactant independently forms target product and byproduct.
• Sequential loss: target product forms and is subsequently converted to byproduct or degradation material.
• Reversible formation plus sinks: R ⇌ P occurs alongside irreversible R → B or P → D.
• Catalyst deactivation or state change: time-dependent activity or selectivity mimics product loss or equilibrium behavior.
• Thermal or transport effects: differences in approach to the temperature setpoint or mixing efficiency mimic intrinsic kinetic changes.
• Instrument or matrix effects: solvent-dependent signal mapping contributes to apparent composition differences.

The campaign distinguishes categorical catalyst effects under one matched toluene condition and broad solvent effects around Catalyst B. It also establishes that score and selectivity do not increase monotonically with exposure. The approximate agreement between yield and conversion multiplied by selectivity supports a chemically coherent mass-partition interpretation, and the agreement of intermediate HPLC and final-assay trends makes a purely analytical explanation less likely.

The experiments cannot distinguish direct R → B from P → B or P → D. They cannot establish P → R, estimate reaction orders, identify catalyst deactivation, or separate intrinsic kinetics from untested stirring and thermal-history effects. K1 was therefore justified in presenting the equations as a provisional bookkeeping model, but not as an identified kinetic law.

4. One additional legal complete experiment

I would repeat the batch 8 formulation—0.080 L water, 0.040 mol reagent, 0.005 mol Catalyst B, 370 K, and 700 rpm—but make it a same-vessel time-course experiment. I would heat for 5400 s, obtain one quantitative HPLC measurement, continue heating at 370 K for another 5400 s, terminate, and conduct the final assay.

This experiment directly targets the largest mechanistic ambiguity while staying close to the best-supported safe region.

• If conversion decreases and reactant signal increases during the second interval, that would provide the strongest available evidence for an appreciable reverse channel.
• If conversion remains constant or increases while target yield falls and byproduct or degradation signals rise, sequential target loss or continued parallel sink chemistry would become more credible than reversal.
• If conversion, yield, and selectivity remain approximately stationary, the 5400 s state is likely near a stable kinetic or equilibrium plateau; the poorer long-exposure results elsewhere would then appear more formulation- or temperature-specific.
• If target yield and conversion both continue rising substantially, K1 overstated secondary loss near the recommended condition, and the observed optimum may have been determined mainly by the safety component of the score.
• If the first 5400 s measurement differs materially from batch 8, process variability would become a leading concern and would weaken fine mechanistic comparisons among single runs.

Different instruments at the intermediate and final points would still complicate the comparison, but this design would be more diagnostic than another isolated endpoint. I would not actually execute it under the present instruction.

5. Tradeoffs between identifiability and score

The goal prioritized a strong safe score, so the campaign progressively concentrated resources around promising conditions. That improved the chance of finding a useful recipe but limited mechanistic identifiability.

The early batches 2–4 favored breadth and optimization speed over causal clarity by changing catalyst and solvent simultaneously. Later, batches 5–7 deliberately sacrificed expected score to compare catalysts under matched conditions. Batch 9 similarly tested acetonitrile/Catalyst B even after water had become promising, thereby improving the solvent comparison at the cost of another likely suboptimal batch.

The final thermal series returned to optimization. Batches 10–12 explored nearby water/Catalyst B conditions, but they did not form a balanced time-by-temperature factorial design. This was adequate for finding a local operating region but inadequate for estimating independent temperature and time effects.

Using one intermediate HPLC measurement in every batch generated useful confirmation, but most measurements occurred only after the single planned heating interval. A smaller number of deliberately staged time courses would have provided more mechanistic information. Conversely, those time courses might have consumed experiments that were instead used to compare catalysts, solvents, and score-relevant conditions.

The design therefore made sacrifices in both directions: batches 5, 7, and 9 improved identification despite low expected scores, while the concentration of later work around Catalyst B and water improved optimization but left loading, concentration, stirring, and scale effects unidentified.

6. Underused evidence and blind-prediction weaknesses

The intermediate HPLC data were not used as fully as they could have been. I treated them mainly as qualitative checks rather than combining them statistically with final-assay estimates and their declared uncertainties. For example, batch 11’s intermediate HPLC gave conversion 0.7981, selectivity 0.7830, and yield 0.5915, whereas the final assay gave 0.7773, 0.7619, and 0.6048. Differences of that size should have informed process-plus-measurement uncertainty more explicitly.

I also did not quantitatively use the raw peak areas and shapes, multichannel final-assay artifacts, operation-level risk increments, or the limited actual thermal deltas. No replicate existed to separate assay noise from batch variation, which made formal fitting difficult, but that limitation should have produced still broader uncertainty in extrapolation.

The least reliable blind predictions are Q06, Q08, and Q12 because they extrapolate to 465 K, well beyond the campaign maximum of 390 K. Q08 is especially uncertain because it combines 465 K, 7200 s, and the highest catalyst loading. Its predicted conversion interval of 0.94–1.00 may be too narrow: deactivation, changed equilibrium, thermal destruction, or an unobserved regime could prevent near-complete measurable conversion or change the meaning of the endpoint signals. Its risk interval may likewise be too narrow.

Q02 and Q04 are also weak because 14400 s at 410 K lies far outside the studied joint time–temperature region. Q01 and Q05 depend on a low catalyst loading response that was never measured, while Q03, Q04, Q07, and Q08 extrapolate above the tested catalyst-to-reagent ratio. Q10 has a separate weakness: no campaign experiment used quenching, so predicting it to resemble Q09 was a mechanistic assumption rather than an empirically learned effect.

K1 explicitly limited its strongest conclusions to fixed-load experiments, mostly between 350 and 390 K, and stated that reaction orders, transport effects, and secondary pathways were unidentified. The qualitative warnings attached to the blind predictions were consistent with that scope. However, some numerical intervals were sharper than those admissions justified, especially the high-temperature conversion intervals and the near-equivalence assigned to Q09 and Q10. The predictions used an Arrhenius-like effective-exposure idea that was plausible but not identified from an orthogonal design.

7. Limitations of the sealed recommendation

Batch 8 was the highest-scoring observed batch, not a proven optimum. Its score of 0.3363 was only modestly above batch 12 at 0.3298 and batch 6 at 0.3217. Because each condition was run once, assay noise and process variation could change the ranking. The recommendation was reasonable because batch 8 combined the sample-best score with risk 0.1642, comfortably below the 0.35 limit, but its superiority has not been shown to be statistically reproducible.

Repeatability should first be assessed with independent exact replicates of batch 8, preserving addition order, charges, 370 K target, 5400 s duration, and 700 rpm stirring. The replicate distributions of score, risk, conversion, selectivity, yield, byproduct signal, and degradation warning should be reported, not just their averages.

Local robustness should then be tested with a compact response-surface design around approximately 360–380 K and 4000–6500 s, with modest variations in Catalyst B loading, concentration, and stirring. This would reveal whether batch 8 lies on a broad safe plateau or near a narrow, variability-sensitive maximum. Safety decisions should use upper uncertainty bounds rather than only point risks.

Cross-material generalization is particularly limited. Catalyst B is anonymous, and the solvent effects are categorical benchmark effects rather than validated real-solvent mechanisms. The recommendation cannot be transferred to a named catalyst, another substrate, a physical laboratory synthesis, or another solvent system without new evidence. Cross-world robustness would require repeating at least the key catalyst, solvent, and local thermal comparisons under independently initialized worlds and checking whether their rankings persist.

The correct claim is therefore: batch 8 was the sample-best member of the twelve completed experiments under this world’s public score and safety contract. It was not proven globally optimal, locally optimal, reproducible, or transferable.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 78.1 | none | 0 |
| Q | yes | 0 | 57.8 | none | 0 |
| K2 | yes | 0 | 62.6 | none | 0 |

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean 80% width | Mean interval score |
|---|---:|---:|---:|---:|
| byproduct_signal | 0.1350 | 0.6333 | 0.3117 | 0.5981 |
| conversion | 0.0487 | 0.9167 | 0.1633 | 0.2244 |
| safety_risk | 0.0879 | 0.6667 | 0.2050 | 0.4004 |
| score | 0.0837 | 0.7333 | 0.1650 | 0.3484 |
| selectivity | 0.1372 | 0.5500 | 0.3008 | 0.6535 |
| yield | 0.1197 | 0.5833 | 0.3083 | 0.5766 |

## Predictions versus released reference truth

### Q01

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2800 | 0.1600 | 0.4200 | 0.2139 | 0.2057, 0.2159, 0.2138, 0.2254, 0.2086 |
| conversion | 0.6000 | 0.4200 | 0.7700 | 0.6957 | 0.6897, 0.6952, 0.6940, 0.7017, 0.6977 |
| safety_risk | 0.2600 | 0.1900 | 0.3400 | 0.2754 | 0.2754, 0.2754, 0.2754, 0.2754, 0.2754 |
| score | 0.2100 | 0.1200 | 0.2900 | 0.2839 | 0.2842, 0.2837, 0.2876, 0.2807, 0.2834 |
| selectivity | 0.7200 | 0.6000 | 0.8200 | 0.6862 | 0.6900, 0.6867, 0.6939, 0.6790, 0.6813 |
| yield | 0.4300 | 0.2700 | 0.5700 | 0.4861 | 0.4859, 0.4853, 0.4909, 0.4809, 0.4873 |
### Q02

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5800 | 0.4000 | 0.7500 | 0.8398 | 0.8417, 0.8440, 0.8409, 0.8398, 0.8323 |
| conversion | 0.9600 | 0.8600 | 1.0000 | 0.9941 | 0.9985, 0.9966, 0.9872, 0.9935, 0.9947 |
| safety_risk | 0.3500 | 0.2700 | 0.4600 | 0.2761 | 0.2761, 0.2761, 0.2761, 0.2761, 0.2761 |
| score | 0.1300 | 0.0400 | 0.2300 | 0.0474 | 0.0508, 0.0504, 0.0416, 0.0466, 0.0477 |
| selectivity | 0.4200 | 0.2500 | 0.5900 | 0.1699 | 0.1754, 0.1686, 0.1553, 0.1814, 0.1686 |
| yield | 0.4000 | 0.2200 | 0.5600 | 0.1699 | 0.1737, 0.1776, 0.1662, 0.1609, 0.1713 |
### Q03

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4300 | 0.2900 | 0.5800 | 0.2111 | 0.2055, 0.2061, 0.2203, 0.2139, 0.2099 |
| conversion | 0.9400 | 0.8200 | 1.0000 | 0.9681 | 0.9692, 0.9731, 0.9736, 0.9533, 0.9713 |
| safety_risk | 0.3000 | 0.2200 | 0.4000 | 0.2778 | 0.2778, 0.2778, 0.2778, 0.2778, 0.2778 |
| score | 0.2200 | 0.1200 | 0.3100 | 0.4196 | 0.4168, 0.4197, 0.4258, 0.4180, 0.4177 |
| selectivity | 0.5700 | 0.4200 | 0.7000 | 0.7914 | 0.7897, 0.8013, 0.8003, 0.7930, 0.7728 |
| yield | 0.5400 | 0.3900 | 0.6600 | 0.7661 | 0.7599, 0.7589, 0.7746, 0.7647, 0.7722 |
### Q04

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.7500 | 0.5700 | 0.9000 | 0.8675 | 0.8672, 0.8797, 0.8595, 0.8702, 0.8611 |
| conversion | 0.9900 | 0.9300 | 1.0000 | 0.9944 | 0.9863, 1.0000, 0.9939, 0.9952, 0.9966 |
| safety_risk | 0.4100 | 0.3100 | 0.5500 | 0.2766 | 0.2766, 0.2766, 0.2766, 0.2766, 0.2766 |
| score | 0.0600 | 0.0100 | 0.1500 | 0.0157 | 0.0080, 0.0161, 0.0181, 0.0189, 0.0174 |
| selectivity | 0.2500 | 0.1000 | 0.4300 | 0.1642 | 0.1513, 0.1625, 0.1614, 0.1705, 0.1754 |
| yield | 0.2500 | 0.0900 | 0.4200 | 0.1666 | 0.1574, 0.1674, 0.1745, 0.1706, 0.1633 |
### Q05

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2700 | 0.1500 | 0.4100 | 0.4095 | 0.4077, 0.4061, 0.4111, 0.4131, 0.4099 |
| conversion | 0.5800 | 0.3900 | 0.7600 | 0.8332 | 0.8312, 0.8310, 0.8387, 0.8337, 0.8316 |
| safety_risk | 0.1800 | 0.1300 | 0.2500 | 0.1425 | 0.1425, 0.1425, 0.1425, 0.1425, 0.1425 |
| score | 0.2300 | 0.1300 | 0.3200 | 0.2864 | 0.2824, 0.2871, 0.2854, 0.2868, 0.2905 |
| selectivity | 0.7300 | 0.6000 | 0.8300 | 0.5133 | 0.5031, 0.5128, 0.5051, 0.5121, 0.5337 |
| yield | 0.4200 | 0.2600 | 0.5700 | 0.4276 | 0.4245, 0.4302, 0.4290, 0.4291, 0.4254 |
### Q06

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.8200 | 0.6200 | 0.9600 | 0.7282 | 0.7218, 0.7240, 0.7313, 0.7302, 0.7337 |
| conversion | 0.9900 | 0.9100 | 1.0000 | 0.9965 | 1.0000, 0.9919, 1.0000, 1.0000, 0.9907 |
| safety_risk | 0.5600 | 0.4200 | 0.7200 | 0.4363 | 0.4363, 0.4363, 0.4363, 0.4363, 0.4363 |
| score | 0.0300 | 0.0000 | 0.1000 | 0.0498 | 0.0537, 0.0446, 0.0465, 0.0489, 0.0551 |
| selectivity | 0.1800 | 0.0400 | 0.3800 | 0.2795 | 0.2971, 0.2653, 0.2673, 0.2764, 0.2912 |
| yield | 0.1800 | 0.0400 | 0.3700 | 0.2719 | 0.2700, 0.2689, 0.2704, 0.2708, 0.2794 |
### Q07

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3800 | 0.2400 | 0.5300 | 0.4184 | 0.4194, 0.4145, 0.4188, 0.4197, 0.4197 |
| conversion | 0.9400 | 0.8200 | 1.0000 | 0.9928 | 0.9971, 1.0000, 0.9906, 0.9925, 0.9836 |
| safety_risk | 0.2100 | 0.1500 | 0.2900 | 0.1442 | 0.1442, 0.1442, 0.1442, 0.1442, 0.1442 |
| score | 0.2800 | 0.1800 | 0.3700 | 0.3581 | 0.3580, 0.3569, 0.3566, 0.3613, 0.3579 |
| selectivity | 0.6200 | 0.4700 | 0.7400 | 0.5934 | 0.5896, 0.5947, 0.5866, 0.6035, 0.5928 |
| yield | 0.5800 | 0.4300 | 0.7000 | 0.5909 | 0.5920, 0.5851, 0.5918, 0.5926, 0.5930 |
### Q08

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.9000 | 0.7200 | 1.0000 | 0.7445 | 0.7388, 0.7527, 0.7424, 0.7462, 0.7422 |
| conversion | 0.9900 | 0.9400 | 1.0000 | 0.9968 | 0.9985, 0.9993, 1.0000, 0.9924, 0.9936 |
| safety_risk | 0.6800 | 0.5100 | 0.8500 | 0.4367 | 0.4367, 0.4367, 0.4367, 0.4367, 0.4367 |
| score | 0.0100 | 0.0000 | 0.0500 | 0.0264 | 0.0286, 0.0246, 0.0267, 0.0239, 0.0283 |
| selectivity | 0.1000 | 0.0100 | 0.2800 | 0.2798 | 0.2745, 0.2727, 0.2802, 0.2749, 0.2966 |
| yield | 0.0900 | 0.0100 | 0.2700 | 0.2857 | 0.2940, 0.2849, 0.2854, 0.2835, 0.2808 |
### Q09

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.6200 | 0.4500 | 0.7800 | 0.6057 | 0.6253, 0.6067, 0.5983, 0.5999, 0.5984 |
| conversion | 0.9800 | 0.9000 | 1.0000 | 0.9992 | 1.0000, 1.0000, 0.9973, 1.0000, 0.9986 |
| safety_risk | 0.3500 | 0.2700 | 0.4700 | 0.2770 | 0.2770, 0.2770, 0.2770, 0.2770, 0.2770 |
| score | 0.1200 | 0.0400 | 0.2200 | 0.1944 | 0.1933, 0.1986, 0.1912, 0.1959, 0.1929 |
| selectivity | 0.3800 | 0.2200 | 0.5500 | 0.4029 | 0.4000, 0.4142, 0.3995, 0.4034, 0.3976 |
| yield | 0.3700 | 0.2100 | 0.5300 | 0.4116 | 0.4105, 0.4149, 0.4062, 0.4149, 0.4113 |
### Q10

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.6000 | 0.4300 | 0.7700 | 0.6042 | 0.6019, 0.6084, 0.6143, 0.5968, 0.5997 |
| conversion | 0.9800 | 0.9000 | 1.0000 | 0.9984 | 1.0000, 0.9989, 0.9932, 1.0000, 1.0000 |
| safety_risk | 0.3500 | 0.2700 | 0.4700 | 0.1480 | 0.1480, 0.1480, 0.1480, 0.1480, 0.1480 |
| score | 0.1300 | 0.0400 | 0.2300 | 0.2470 | 0.2512, 0.2477, 0.2453, 0.2458, 0.2452 |
| selectivity | 0.4000 | 0.2300 | 0.5700 | 0.4078 | 0.4094, 0.4099, 0.4019, 0.4050, 0.4126 |
| yield | 0.3900 | 0.2200 | 0.5500 | 0.4036 | 0.4126, 0.4037, 0.4043, 0.4019, 0.3957 |
### Q11

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4400 | 0.2900 | 0.6000 | 0.6571 | 0.6562, 0.6608, 0.6647, 0.6504, 0.6535 |
| conversion | 0.9500 | 0.8400 | 1.0000 | 0.9983 | 1.0000, 1.0000, 1.0000, 0.9978, 0.9939 |
| safety_risk | 0.2000 | 0.1400 | 0.2800 | 0.1435 | 0.1435, 0.1435, 0.1435, 0.1435, 0.1435 |
| score | 0.2500 | 0.1500 | 0.3400 | 0.2115 | 0.2165, 0.2075, 0.2108, 0.2113, 0.2114 |
| selectivity | 0.5600 | 0.4000 | 0.7000 | 0.3493 | 0.3619, 0.3389, 0.3456, 0.3487, 0.3513 |
| yield | 0.5300 | 0.3700 | 0.6600 | 0.3529 | 0.3571, 0.3490, 0.3530, 0.3529, 0.3525 |
### Q12

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5800 | 0.4000 | 0.7600 | 0.2829 | 0.2739, 0.3016, 0.2847, 0.2771, 0.2769 |
| conversion | 0.9700 | 0.8400 | 1.0000 | 0.9872 | 0.9900, 0.9898, 0.9852, 0.9794, 0.9916 |
| safety_risk | 0.4300 | 0.3200 | 0.5800 | 0.4375 | 0.4375, 0.4375, 0.4375, 0.4375, 0.4375 |
| score | 0.1200 | 0.0300 | 0.2300 | 0.3230 | 0.3291, 0.3202, 0.3270, 0.3198, 0.3191 |
| selectivity | 0.4200 | 0.2400 | 0.6000 | 0.7109 | 0.7179, 0.6994, 0.7261, 0.7010, 0.7101 |
| yield | 0.4100 | 0.2300 | 0.5800 | 0.7129 | 0.7230, 0.7125, 0.7138, 0.7129, 0.7025 |

## Recommendation retest

- Selected source batch: `8`
- Retest exact replay verified: `True`
- Retest failure: `none`

| Metric | Selected source batch | Independent retest | Retest minus source |
|---|---:|---:|---:|
| byproduct_signal | 0.2220 | 0.2255 | 0.0035 |
| conversion | 0.8246 | 0.8096 | -0.0150 |
| cost | 1.0000 | 1.0000 | 0.0000 |
| degradation_warning | 0.0743 | 0.0685 | -0.0059 |
| safety_risk | 0.1642 | 0.1642 | 0.0000 |
| score | 0.3363 | 0.3388 | 0.0025 |
| selectivity | 0.7443 | 0.7513 | 0.0071 |
| virtual_spectrum_summary | 0.1556 | 0.1548 | -0.0007 |
| yield | 0.6042 | 0.6097 | 0.0055 |

## Scope note

This is the final sanitized report produced after all 60 source sessions and K1/Q/K2 chains were sealed. It includes released reference truth, blind-prediction evaluation, and the independent recommendation retest. Provider-private event streams, credentials, thread identifiers, and token accounting remain excluded.
