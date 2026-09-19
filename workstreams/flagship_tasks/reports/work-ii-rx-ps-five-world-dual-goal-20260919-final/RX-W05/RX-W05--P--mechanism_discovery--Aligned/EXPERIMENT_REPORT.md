# RX-W05--P--mechanism_discovery--Aligned

## Run summary

- World: `RX-W05`
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
- Rationale: The 1800 s heat followed by prompt quench gave the lowest observed final safety risk (0.0793) while retaining strong yield (0.724), selectivity (0.888), and the highest observed final score among the tested batches.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S0 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 420 K x 3300 s @ 600 rpm | no | 0.7677 | 0.7758 | 0.9647 | 0.2139 | 0.1497 | 0.2264 | 0.4216 |
| 2 | S0 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 400 K x 3300 s @ 600 rpm | no | 0.7594 | 0.8312 | 0.9097 | 0.1671 | 0.1291 | 0.1428 | 0.4642 |
| 3 | S0 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 440 K x 3300 s @ 600 rpm | no | 0.7701 | 0.7879 | 0.9890 | 0.2088 | 0.1625 | 0.3059 | 0.3923 |
| 4 | S0 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 420 K x 1800 s @ 600 rpm | no | 0.7279 | 0.8779 | 0.8266 | 0.1101 | 0.0594 | 0.2256 | 0.4190 |
| 5 | S0 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 420 K x 6000 s @ 600 rpm | no | 0.6761 | 0.6869 | 0.9944 | 0.3301 | 0.2755 | 0.2263 | 0.3635 |
| 6 | S0 (0.0075 L) | 0.003000 mol | C0 (0.000525 mol) | 420 K x 3300 s @ 600 rpm | no | 0.7130 | 0.8153 | 0.8601 | 0.1778 | 0.0431 | 0.2255 | 0.4289 |
| 7 | S0 (0.0075 L) | 0.003000 mol | C1 (0.000525 mol) | 420 K x 3300 s @ 600 rpm | no | 0.7430 | 0.7957 | 0.9201 | 0.2176 | 0.1171 | 0.2260 | 0.4208 |
| 8 | S0 (0.0075 L) | 0.003000 mol | C2 (0.000525 mol) | 420 K x 3300 s @ 600 rpm | no | 0.5493 | 0.7080 | 0.7821 | 0.2411 | 0.0607 | 0.2245 | 0.3209 |
| 9 | S1 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 420 K x 3300 s @ 600 rpm | no | 0.6848 | 0.6997 | 0.9632 | 0.2905 | 0.2216 | 0.2496 | 0.3585 |
| 10 | S2 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 420 K x 3300 s @ 600 rpm | no | 0.7053 | 0.6991 | 0.9840 | 0.2871 | 0.2416 | 0.2678 | 0.3600 |
| 11 | S3 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 420 K x 3300 s @ 600 rpm | no | 0.5688 | 0.5944 | 0.9621 | 0.3939 | 0.2763 | 0.2798 | 0.2719 |
| 12 | S0 (0.0075 L) | 0.003000 mol | C3 (0.000525 mol) | 420 K x 1800 s @ 600 rpm | yes | 0.7242 | 0.8884 | 0.8324 | 0.1039 | 0.0447 | 0.0793 | 0.4777 |

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
    "byproduct_signal": 0.21386931836605072,
    "conversion": 0.9647380709648132,
    "cost": 0.7402999997138977,
    "degradation_warning": 0.1496729999780655,
    "safety_risk": 0.2263662964105606,
    "score": 0.42160066962242126,
    "selectivity": 0.775783896446228,
    "virtual_spectrum_summary": 0.18498097360134125,
    "yield": 0.7676892876625061
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
      "catalyst": 3,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
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
    "byproduct_signal": 0.16712957620620728,
    "conversion": 0.9096563458442688,
    "cost": 0.7402999997138977,
    "degradation_warning": 0.12906548380851746,
    "safety_risk": 0.1428210735321045,
    "score": 0.46422895789146423,
    "selectivity": 0.8311810493469238,
    "virtual_spectrum_summary": 0.15000073611736298,
    "yield": 0.7594188451766968
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
      "catalyst": 3,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3300,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 440
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
    "byproduct_signal": 0.20884492993354797,
    "conversion": 0.9889649152755737,
    "cost": 0.7402999997138977,
    "degradation_warning": 0.16254545748233795,
    "safety_risk": 0.3058708906173706,
    "score": 0.3922668695449829,
    "selectivity": 0.7879452705383301,
    "virtual_spectrum_summary": 0.18801017105579376,
    "yield": 0.7701398730278015
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
      "catalyst": 3,
      "catalyst_amount_mol": 0.000525,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1800,
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
    "byproduct_signal": 0.11011146754026413,
    "conversion": 0.8265519738197327,
    "cost": 0.7278000116348267,
    "degradation_warning": 0.059379223734140396,
    "safety_risk": 0.22562961280345917,
    "score": 0.4189663529396057,
    "selectivity": 0.8778594136238098,
    "virtual_spectrum_summary": 0.0872819572687149,
    "yield": 0.7278990745544434
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
  "end_step": 35,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.33007046580314636,
    "conversion": 0.9944266080856323,
    "cost": 0.7627999782562256,
    "degradation_warning": 0.2755080759525299,
    "safety_risk": 0.22633026540279388,
    "score": 0.36346811056137085,
    "selectivity": 0.6868959665298462,
    "virtual_spectrum_summary": 0.30551740527153015,
    "yield": 0.6760751605033875
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
  "end_step": 42,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.17781881988048553,
    "conversion": 0.8600943684577942,
    "cost": 0.4462999999523163,
    "degradation_warning": 0.04309013485908508,
    "safety_risk": 0.22547794878482819,
    "score": 0.42892810702323914,
    "selectivity": 0.8152638077735901,
    "virtual_spectrum_summary": 0.11719091236591339,
    "yield": 0.7129945158958435
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
  "end_step": 49,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.21764923632144928,
    "conversion": 0.9200566411018372,
    "cost": 0.6563000082969666,
    "degradation_warning": 0.11706820130348206,
    "safety_risk": 0.2260156273841858,
    "score": 0.42080047726631165,
    "selectivity": 0.7957425117492676,
    "virtual_spectrum_summary": 0.17238777875900269,
    "yield": 0.7429904937744141
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
  "end_step": 56,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.24107234179973602,
    "conversion": 0.782075822353363,
    "cost": 0.5303000211715698,
    "degradation_warning": 0.06073230877518654,
    "safety_risk": 0.22449980676174164,
    "score": 0.3208656311035156,
    "selectivity": 0.7079821825027466,
    "virtual_spectrum_summary": 0.15991933643817902,
    "yield": 0.5492935180664062
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
  "end_step": 63,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.29050278663635254,
    "conversion": 0.9632046222686768,
    "cost": 0.7433000206947327,
    "degradation_warning": 0.22163806855678558,
    "safety_risk": 0.24958759546279907,
    "score": 0.358505517244339,
    "selectivity": 0.6996774673461914,
    "virtual_spectrum_summary": 0.2595136761665344,
    "yield": 0.6847752928733826
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
  "end_step": 70,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.28712132573127747,
    "conversion": 0.9840459823608398,
    "cost": 0.7480999827384949,
    "degradation_warning": 0.24164393544197083,
    "safety_risk": 0.2677887976169586,
    "score": 0.36000844836235046,
    "selectivity": 0.6991464495658875,
    "virtual_spectrum_summary": 0.2666565179824829,
    "yield": 0.705330491065979
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
  "end_step": 77,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.3939001262187958,
    "conversion": 0.9621285796165466,
    "cost": 0.7451000213623047,
    "degradation_warning": 0.27632322907447815,
    "safety_risk": 0.27975013852119446,
    "score": 0.27192041277885437,
    "selectivity": 0.5943552851676941,
    "virtual_spectrum_summary": 0.34099051356315613,
    "yield": 0.5687907934188843
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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 420
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "operation": "quench"
    },
    {
      "duration_s": 1500,
      "operation": "wait",
      "stirring_speed_rpm": 600
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
    "byproduct_signal": 0.1039484292268753,
    "conversion": 0.8324365019798279,
    "cost": 0.8164260983467102,
    "degradation_warning": 0.044665880501270294,
    "safety_risk": 0.0792868584394455,
    "score": 0.47771576046943665,
    "selectivity": 0.8884096145629883,
    "virtual_spectrum_summary": 0.07727128267288208,
    "yield": 0.7242285013198853
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

1. Scope and evidential basis

I completed 12 closed batches using the same nominal charge unless otherwise stated: 0.003 mol anonymous limiting reagent, 0.000525 mol catalyst, 0.0075 L solvent, and 600 rpm stirring. Each batch received one endpoint HPLC measurement and one post-termination final assay. The factors varied were temperature target, heating duration, catalyst identity, solvent identity, and quench timing.

The species and catalysts are anonymous benchmark entities. Therefore, the account below is a kinetic/process model, not a claim about a named chemical mechanism. Numerical values quoted as observations are processed instrument estimates or public state deltas; equations and rate interpretations are hypotheses.

2. Central mechanistic picture

The simplest model consistent with the campaign is a catalytic network with desired formation, competing conversion, and subsequent loss of accumulated target:

R -> P  (desired catalytic route, rate kP)
R -> B  (parallel undesired route, rate kB)
P -> D  (secondary degradation or conversion, rate kD)

A useful provisional model is:

dR/dt = -a(t)[kP(T,C,S) + kB(T,C,S)]R

dP/dt = a(t)kP(T,C,S)R - kD(T,C,S)P

dB/dt = a(t)kB(T,C,S)R + f kD(T,C,S)P

da/dt = -kdeact(T,C,S)a

Here R is remaining reactant, P is target, B is measured side-product material, D is degraded or otherwise undesirable material, a(t) is effective catalyst activity, C is catalyst identity, and S is solvent identity. The coefficient f allows degraded target to contribute partly to the measured byproduct channel. Arrhenius-like temperature dependence is plausible for each rate constant, but the data do not support unique activation energies.

Observed conversion is approximately 1-R/R0, yield is approximately P/R0, and selectivity reflects the partitioning of converted material into target versus undesirable channels. These definitions need not be exact because the synthetic instrument channels are separately calibrated and their estimates contain noise.

This model explains the most important observation: conversion continues to increase with time, but target yield reaches a maximum and then declines while byproduct and degradation signals rise. Thus maximum conversion is not the same as maximum useful product formation.

3. Time dependence and target loss

Batches 4, 1, and 5 form the main duration series, all using water and Catalyst D at a 420 K target:

- Batch 4, 1800 s: final conversion 0.8266, yield 0.7279, selectivity 0.8779, byproduct 0.1101, degradation warning 0.0594.
- Batch 1, 3300 s: final conversion 0.9647, yield 0.7677, selectivity 0.7758, byproduct 0.2139, degradation warning 0.1497.
- Batch 5, 6000 s: final conversion 0.9944, yield 0.6761, selectivity 0.6869, byproduct 0.3301, degradation warning 0.2755.

The conversion increase from 1800 to 3300 s raises yield only from 0.728 to 0.768 and causes a much larger deterioration in selectivity. Extending to 6000 s barely increases conversion but lowers yield by about 0.092 relative to 3300 s. At the same time, byproduct rises from 0.110 to 0.330 and degradation warning from 0.059 to 0.276.

A crude irreversible first-order conversion estimate, kobs=-ln(1-X)/t, is about 9.7e-4 s^-1 at 1800 s, 1.0e-3 s^-1 at 3300 s, and 8.6e-4 s^-1 at 6000 s. The declining apparent rate at long time could result from reactant depletion, catalyst deactivation, approach to a kinetic ceiling, or some combination. The much clearer conclusion is that P is not stable indefinitely under the reaction conditions.

The yield optimum in the tested interval lies near, but is not proven to be exactly at, 3300 s. A duration between roughly 2000 and 3500 s appears to trade conversion against secondary loss. This range is an interpolation within the tested water/Catalyst D/420 K context, not a universal optimum.

4. Temperature and actual thermal response

Batches 2, 1, and 3 used water, Catalyst D, and 3300 s heating at targets of 400, 420, and 440 K:

- Batch 2, 400 K: conversion 0.9097, yield 0.7594, selectivity 0.8312, byproduct 0.1671, degradation 0.1291, risk 0.1428.
- Batch 1, 420 K: conversion 0.9647, yield 0.7677, selectivity 0.7758, byproduct 0.2139, degradation 0.1497, risk 0.2264.
- Batch 3, 440 K: conversion 0.9890, yield 0.7701, selectivity 0.7879, byproduct 0.2088, degradation 0.1625, risk 0.3059.

Higher target temperature clearly accelerated conversion, but target yield changed very little across this range. Most of the extra conversion at higher temperature was offset by loss of selectivity or degradation. The small selectivity increase from batch 1 to batch 3 is not enough to establish a nonmonotonic temperature effect because it is comparable to assay variation and conflicts with the overall growth in degradation warning.

The public heat-state deltas show that commanded temperature was not identical to realized thermal response. The reported temperature rises were 91.554 K at a 400 K target, 107.358 K at 420 K, and 122.552 K at 440 K. Thus a 20 K target increment produced only about a 15-16 K increment in the reported endpoint rise. Because absolute starting temperature was not explicitly observed, I do not assign exact absolute reactor temperatures. The mechanistic rates should depend on the actual trajectory T(t), not merely the setpoint.

The initial supplied model predicted safer balanced behavior on the lower-temperature side. The experiments supported that directional safety claim: risk rose from 0.1428 to 0.2264 to 0.3059 across the three targets. They also refined it: the lower temperature sacrificed some conversion but almost no final yield, making the 400 K condition attractive when safety and selectivity matter.

5. Catalyst effects

Batches 6, 7, 8, and 1 compared Catalysts A-D in water at 420 K for 3300 s:

- Catalyst A, batch 6: conversion 0.8601, yield 0.7130, selectivity 0.8153, byproduct 0.1778, degradation 0.0431.
- Catalyst B, batch 7: conversion 0.9201, yield 0.7430, selectivity 0.7957, byproduct 0.2176, degradation 0.1171.
- Catalyst C, batch 8: conversion 0.7821, yield 0.5493, selectivity 0.7080, byproduct 0.2411, degradation 0.0607.
- Catalyst D, batch 1: conversion 0.9647, yield 0.7677, selectivity 0.7758, byproduct 0.2139, degradation 0.1497.

Catalyst D was the strongest conversion promoter and produced the highest target yield at this fixed time. Catalyst A was slower but more selective and generated much less degradation signal. Catalyst B was intermediate. Catalyst C was poor in both conversion and selectivity and generated unusually high byproduct relative to its conversion.

This pattern requires at least two catalyst-dependent effects rather than a single scalar activity multiplier. Catalyst identity appears to affect both total conversion rate and branching between target and side products. Catalyst D may also promote secondary target degradation, directly or simply because it forms target earlier and exposes it to hot conditions longer. Catalyst A may be intrinsically cleaner, or its lower apparent degradation may only reflect slower turnover and shorter effective exposure of P.

No catalyst-loading series was performed, so catalyst order, saturation, aggregation, and concentration-dependent deactivation remain unidentified.

6. Solvent effects and coupling to safety

Batches 1 and 9-11 compared solvents with Catalyst D at 420 K for 3300 s:

- Water, batch 1: conversion 0.9647, yield 0.7677, selectivity 0.7758, byproduct 0.2139, degradation 0.1497, risk 0.2264.
- Ethanol, batch 9: conversion 0.9632, yield 0.6848, selectivity 0.6997, byproduct 0.2905, degradation 0.2216, risk 0.2496.
- Acetonitrile, batch 10: conversion 0.9840, yield 0.7053, selectivity 0.6991, byproduct 0.2871, degradation 0.2416, risk 0.2678.
- Toluene, batch 11: conversion 0.9621, yield 0.5688, selectivity 0.5944, byproduct 0.3939, degradation 0.2763, risk 0.2798.

Conversion alone obscures the solvent effect: all four conditions achieved high conversion, but the product distribution differed substantially. Water favored target formation and minimized undesirable signals. Toluene was strongly unfavorable, while ethanol and acetonitrile were intermediate and similar in selectivity.

Solvent therefore modifies kP/kB and probably kD, not merely the overall reaction speed. It also altered safety independently of the nearly identical heat-operation risk increment. The final risk increased in the order water < ethanol < acetonitrile < toluene. This suggests a solvent-specific baseline contribution coupled with thermal hazard, rather than risk being a simple function of conversion.

These are categorical benchmark effects. They should not be generalized from real-world solvent polarity, boiling point, or flammability without additional evidence.

7. Quench and termination timing

Batches 4 and 12 provide the quench comparison. Both used water, Catalyst D, a 420 K target, and 1800 s heating. Their pre-termination HPLC results were close:

- Batch 4 HPLC: conversion 0.8297, yield 0.7298, selectivity 0.8699, byproduct 0.1121.
- Batch 12 pre-quench HPLC: conversion 0.8182, yield 0.7137, selectivity 0.8543, byproduct 0.1164.

Batch 4 was terminated without quenching. Batch 12 was quenched, then held for 1500 s before termination. The quench produced a reported temperature delta of -45 K, reduced safety risk from 0.2256 to 0.0793, and had a reported operation time delta of about 5.0 s. The subsequent 1500 s wait left the displayed composition and risk unchanged.

Final assay results were:

- Batch 4, no quench: conversion 0.8266, yield 0.7279, selectivity 0.8779, byproduct 0.1101, degradation 0.0594, risk 0.2256.
- Batch 12, quenched: conversion 0.8324, yield 0.7242, selectivity 0.8884, byproduct 0.1039, degradation 0.0447, risk 0.0793.

The small chemical differences are within plausible batch and instrument variation, so I do not claim that quenching increased yield or conversion. The strong conclusion is that prompt quenching sharply reduced the hazardous thermal state and effectively arrested further observable chemistry during the 1500 s hold. This supports treating quench time as a genuine kinetic boundary: the relevant reaction duration is time at reactive temperature, not elapsed wall-clock time before assay.

Batch 12 was therefore the sealed recommendation. It combined low final risk with 0.724 yield and 0.888 selectivity. It is the best balanced safe condition tested, although batch 2 had somewhat higher yield at moderate risk.

8. Safety model

A provisional process-risk representation is:

Risk = rsetup(S, charge) + rthermal(Tactual endpoint or maximum, S) - rquench.

At a 420 K target, the heat-associated risk increment was approximately 0.165-0.167 across 1800, 3300, and 6000 s. Final risk was therefore almost independent of heating duration but strongly dependent on temperature target and solvent. This indicates that the public safety metric behaves more like a state or peak-temperature hazard than an integrated thermal dose.

Quenching removes a large part of that thermal-state contribution. The data do not establish whether chemical accumulation, pressure, or some other latent state also contributes. No tested batch exceeded the stated 0.35 safety limit; the highest observed value was 0.3059 in batch 3.

9. Measurement interpretation

Endpoint HPLC and final assay values sometimes differed. For example, batch 2 HPLC estimated conversion 0.9292 and selectivity 0.7903, whereas its final assay estimated 0.9097 and 0.8312. These discrepancies should not be interpreted as reverse reaction during termination because instrument noise, independent calibration, and sampling are sufficient explanations. Mechanistic conclusions above rely on large, repeated trends rather than small cross-instrument differences.

Likewise, selectivity is not exactly yield/conversion in every assay. I treat all three as separately noisy proxies for the same mass-partitioning process rather than imposing an exact algebraic identity.

10. How the explanation changed during the campaign

The supplied prior emphasized a lower-temperature safety advantage near the 420 K, 3300 s reference region. Batch 1 confirmed that the reference condition gave high conversion but revealed substantial side-product and degradation signals. Batches 2 and 3 then showed that increasing temperature mainly increased conversion and risk, with little target-yield benefit. This strengthened the lower-temperature recommendation.

Batch 4 initially suggested that shorter heating could preserve selectivity, while batch 5 decisively showed that prolonged heating destroys accumulated target. That evidence changed the working model from simple parallel formation alone to a network requiring secondary loss of P or time-dependent selectivity.

The catalyst comparison showed that activity and selectivity cannot be represented by one catalyst-strength parameter. The solvent comparison similarly showed nearly constant high conversion with large changes in target yield, requiring solvent-dependent branching or degradation.

Finally, batch 12 demonstrated that quenching is not merely an administrative termination step. It changes the thermal state, greatly lowers risk, and prevents detectable evolution during a subsequent hold.

11. Limits of identifiability

Several important factors remain unresolved:

- Parallel side-product formation and sequential target degradation are partially confounded. The time series strongly supports target loss, but it cannot determine how much byproduct arises directly from R versus from P.
- Catalyst deactivation is plausible from the declining long-time apparent rate, but reagent depletion or approach to a conversion ceiling can explain the same pattern.
- Absolute reactor temperature and the complete heating ramp were not directly measured; only target settings, durations, and public temperature deltas were observed.
- There was no full within-batch concentration-time series. Each batch had only an endpoint HPLC measurement, so detailed rate constants are not identifiable.
- Catalyst amount, reagent concentration, solvent volume, stirring speed, order of addition, and scale were held fixed. Reaction orders and mass-transfer limitations are unknown.
- Catalyst-solvent interactions were not factorially mapped. Catalyst rankings established in water may change in another solvent.
- The chemical meaning of the degradation-warning channel is unknown. It may indicate degraded target, a correlated impurity, or a process-state proxy.
- Batch replication was limited. Batches 4 and 12 provide a partial replicate before their different termination procedures, but most conditions were run only once.
- The risk metric appears state-based, but its hidden components cannot be separated into temperature, solvent, pressure, or composition contributions.

12. Reasonable competing explanations

A purely parallel model, R -> P and R -> B with time-varying branching caused by catalyst-state evolution, could reproduce the falling selectivity without literal P -> D. A reversible desired reaction, R <-> P, combined with irreversible side-product formation could also generate a yield maximum. Catalyst poisoning by product or byproduct could explain the slowing conversion. Apparent target loss might additionally reflect changing analytical response or matrix effects, although the coordinated rise in byproduct and degradation signals makes a real process change more plausible.

The present data favor a desired-product intermediate that becomes vulnerable during prolonged hot exposure, but they do not uniquely prove its microscopic pathway.

13. Predictive use within the studied domain

Within the tested charge, 600 rpm mixing, 0.0075 L scale, and roughly 400-440 K target range, I would predict:

- Raising temperature increases conversion and safety risk more reliably than it increases isolated target yield.
- Extending heating beyond roughly 3300 s drives conversion toward completion but decreases target yield and selectivity.
- Shorter heating followed by immediate quench preserves selectivity and sharply lowers the final hazardous thermal state.
- Catalyst D maximizes conversion and target yield at the reference time, while Catalyst A offers a cleaner but slower regime.
- Water is superior to the other tested solvents for target partitioning and safety.
- Conditions outside the measured temperature, time, catalyst-loading, concentration, or mixing ranges should not be extrapolated quantitatively.

Overall, this world behaves as a thermally accelerated catalytic reaction network in which the desired product is kinetically favored only over a finite processing window. Temperature, catalyst, and solvent affect both total conversion and pathway branching; prolonged hot residence promotes undesirable material; and quenching is the key operation that freezes composition while removing most of the observed thermal risk.

## Q — Blind predictions

### Overall rationale

Predictions were generated from the campaign's observed time, temperature, catalyst, solvent, and quench trends. The central reference was the 420 K, 3300 s series. Catalyst B was treated as slower but slightly cleaner than Catalyst D, while acetonitrile was treated as maintaining high conversion but worsening target partitioning. Temperature and duration were applied through a saturating conversion model with increasing secondary target loss at prolonged or hotter exposure. Safety was modeled mainly from solvent-dependent setup risk and terminal thermal state, with a large reduction after quenching. Intervals combine final-assay noise with larger structural uncertainty for the untested 0.005 L volume, 400 rpm stirring, catalyst-solvent interaction, staged heating, and extrapolated temperature extremes.

### Q01

This is closest to the studied 420 K, 3300 s conditions. Combining the observed Catalyst B effect with the acetonitrile effect predicts high conversion but lower yield and selectivity than the water runs. The reduced solvent volume and lower stirring rate were not independently calibrated, so the intervals include additional model uncertainty.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2910 | 0.2100 | 0.3800 |
| conversion | 0.9400 | 0.8700 | 0.9800 |
| safety_risk | 0.2450 | 0.2000 | 0.3000 |
| score | 0.3660 | 0.3000 | 0.4300 |
| selectivity | 0.7200 | 0.6300 | 0.8000 |
| yield | 0.6800 | 0.6000 | 0.7500 |

### Q02

The chemical estimates are the same as Q01 because batch 12 showed that a prompt quench mainly arrested the state rather than materially changing endpoint composition. The quench is predicted to remove most of the thermal risk, producing a higher score.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2910 | 0.2100 | 0.3800 |
| conversion | 0.9400 | 0.8700 | 0.9800 |
| safety_risk | 0.0900 | 0.0500 | 0.1400 |
| score | 0.4210 | 0.3500 | 0.4900 |
| selectivity | 0.7200 | 0.6300 | 0.8000 |
| yield | 0.6800 | 0.6000 | 0.7500 |

### Q03

Lower temperature should reduce conversion but preserve branching toward target and suppress degradation. This extrapolates 10 K below the lowest temperature used in the direct 3300 s temperature series, so kinetic uncertainty is appreciable.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1850 | 0.1100 | 0.2700 |
| conversion | 0.8400 | 0.7200 | 0.9200 |
| safety_risk | 0.1150 | 0.0700 | 0.1700 |
| score | 0.4280 | 0.3500 | 0.5000 |
| selectivity | 0.8050 | 0.7100 | 0.8800 |
| yield | 0.6650 | 0.5600 | 0.7400 |

### Q04

At 450 K, conversion should be nearly complete, but the added thermal severity is expected to increase competing conversion and target loss. This is a 10 K extrapolation beyond the tested 440 K condition and may cross the nominal safety threshold, hence the wide risk and score intervals.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3450 | 0.2400 | 0.4600 |
| conversion | 0.9920 | 0.9500 | 1.0000 |
| safety_risk | 0.3550 | 0.2900 | 0.4300 |
| score | 0.2980 | 0.2000 | 0.3900 |
| selectivity | 0.6550 | 0.5300 | 0.7500 |
| yield | 0.6500 | 0.5300 | 0.7400 |

### Q05

The shortened residence time should preserve selectivity and suppress byproduct formation, but it should terminate before full conversion. Risk is treated primarily as a thermal-state quantity because it was nearly duration-independent at a fixed temperature in the campaign.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1500 | 0.0800 | 0.2300 |
| conversion | 0.7650 | 0.6300 | 0.8700 |
| safety_risk | 0.2450 | 0.2000 | 0.3000 |
| score | 0.3680 | 0.2900 | 0.4400 |
| selectivity | 0.8200 | 0.7200 | 0.8900 |
| yield | 0.6250 | 0.5100 | 0.7100 |

### Q06

Longer hot residence should bring conversion close to completion while allowing substantial parallel byproduct formation and secondary target loss. The prediction is interpolated between the tested 3300 and 6000 s regimes, with extra uncertainty from the new catalyst-solvent combination.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3750 | 0.2700 | 0.4900 |
| conversion | 0.9750 | 0.9200 | 1.0000 |
| safety_risk | 0.2450 | 0.2000 | 0.3000 |
| score | 0.3260 | 0.2400 | 0.4000 |
| selectivity | 0.6500 | 0.5300 | 0.7500 |
| yield | 0.6200 | 0.5000 | 0.7100 |

### Q07

The low-temperature first stage should build some target before a high-temperature finishing stage drives conversion upward. Ending at 450 K is expected to leave a high final thermal risk, while late high-temperature exposure may accelerate degradation. No two-stage temperature sequence was directly tested.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3200 | 0.2100 | 0.4400 |
| conversion | 0.9500 | 0.8700 | 0.9900 |
| safety_risk | 0.3550 | 0.2700 | 0.4500 |
| score | 0.3130 | 0.2100 | 0.4100 |
| selectivity | 0.6900 | 0.5600 | 0.7900 |
| yield | 0.6650 | 0.5400 | 0.7500 |

### Q08

The same nominal thermal durations as Q07 give a similar integrated kinetic dose, but the final 390 K stage should reduce the terminal thermal state. High temperature occurs earlier, so the subsequent cooler period is predicted to cause less degradation than ending with the high-temperature stage. Whether safety records peak or terminal state is a major uncertainty.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2800 | 0.1800 | 0.4000 |
| conversion | 0.9400 | 0.8500 | 0.9900 |
| safety_risk | 0.1450 | 0.0800 | 0.2400 |
| score | 0.4090 | 0.3000 | 0.5000 |
| selectivity | 0.7300 | 0.6000 | 0.8200 |
| yield | 0.6900 | 0.5700 | 0.7800 |

### Q09

A short 440 K treatment should accelerate conversion relative to a short 420 K run without reaching the severe target loss expected at long duration. Its unquenched terminal thermal state is nevertheless predicted to carry substantial risk.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2200 | 0.1300 | 0.3200 |
| conversion | 0.8500 | 0.7300 | 0.9300 |
| safety_risk | 0.3220 | 0.2600 | 0.3900 |
| score | 0.3330 | 0.2400 | 0.4200 |
| selectivity | 0.7500 | 0.6300 | 0.8400 |
| yield | 0.6500 | 0.5400 | 0.7400 |

### Q10

The chemical estimates match Q09 because quenching occurs after the programmed reaction period. Based on batch 12, the quench should sharply reduce the final safety risk and thereby improve the score, although its effectiveness after a hotter treatment is extrapolated.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2200 | 0.1300 | 0.3200 |
| conversion | 0.8500 | 0.7300 | 0.9300 |
| safety_risk | 0.1000 | 0.0500 | 0.1700 |
| score | 0.4120 | 0.3200 | 0.5000 |
| selectivity | 0.7500 | 0.6300 | 0.8400 |
| yield | 0.6500 | 0.5400 | 0.7400 |

### Q11

The long duration partly compensates for the very low temperature, while the mild thermal state should preserve selectivity and limit degradation. This is the largest low-temperature extrapolation, so conversion and yield have broad intervals despite the predicted low safety risk.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1600 | 0.0800 | 0.2600 |
| conversion | 0.7800 | 0.6100 | 0.9000 |
| safety_risk | 0.0750 | 0.0400 | 0.1300 |
| score | 0.4360 | 0.3400 | 0.5200 |
| selectivity | 0.8200 | 0.7000 | 0.9000 |
| yield | 0.6550 | 0.5100 | 0.7500 |

### Q12

This combines the hottest and longest conditions and is well outside the directly studied joint range. Conversion should be essentially complete, but extensive competing reaction and secondary target degradation are expected to depress yield and selectivity. The run is also likely to exceed the nominal safety limit; rollback or nonlinear hazard behavior is included in the wide interval.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5800 | 0.4200 | 0.7300 |
| conversion | 0.9990 | 0.9700 | 1.0000 |
| safety_risk | 0.4000 | 0.3200 | 0.4900 |
| score | 0.1270 | 0.0300 | 0.2300 |
| selectivity | 0.4000 | 0.2400 | 0.5700 |
| yield | 0.4200 | 0.2500 | 0.5700 |

## K2 — Retrospective analysis

1. Assessment of the initial information

The initial packet contained one substantive directional process claim: relative to the stated reference region near 420 K and 3300 s, the lower-temperature side should retain safe, balanced performance more reliably than the higher-temperature side. It explicitly described that model as incomplete and said experimental evidence was authoritative. It did not provide a substantive molecular mechanism, named catalyst identities, kinetic constants, reaction orders, or a task-specific material-property dossier.

That directional temperature claim was supported within the tested local domain. At 3300 s with water and Catalyst D, batch 2 at 400 K had risk 0.1428, yield 0.7594, and selectivity 0.8312; batch 1 at 420 K had risk 0.2264, yield 0.7677, and selectivity 0.7758; batch 3 at 440 K had risk 0.3059, yield 0.7701, and selectivity 0.7879. Lowering the target from 420 to 400 K therefore reduced risk greatly and preserved nearly all observed yield while improving selectivity. Raising it to 440 K increased conversion and risk but produced almost no yield benefit.

The claim should nevertheless be interpreted locally. Three temperatures under one catalyst-solvent-time combination do not prove it for all catalysts, solvents, concentrations, or schedules. The slight increase in measured selectivity from batch 1 at 420 K to batch 3 at 440 K also prevents a strong claim that selectivity must decrease monotonically with temperature. I treated that difference as measurement or process variation rather than decisive counterevidence, which was reasonable but not proven.

The packet also instructed that a temperature-bound rollback, if observed, should count as evidence rather than missing output. No such rollback occurred in the 12 experiments, so that proposition remained untested. This is a case of no relevant observation, not confirmation. Similarly, the reference catalyst, loading, solvent, and agitation values described a context, not an asserted optimum.

There was no initial mechanistic claim about sequential degradation, catalyst deactivation, solvent branching, or quench efficacy. Those parts of K1 were developed from campaign observations. Consequently, there was no initial mechanistic proposition in those areas that was either refuted or ignored. I do not identify an important initial claim for which clear counterevidence appeared and was knowingly left uncorrected.

2. Experiments that formed or changed the interpretation

Batch 1 was anchored almost entirely by the supplied reference context. It established that the nominal reference gave high conversion but nontrivial byproduct and degradation signals. It did not by itself distinguish parallel side reaction from later product loss.

Batches 2 and 3 were the direct test of the initial temperature claim. Their selection depended strongly on the supplied lower-versus-higher-temperature proposition. They supported the safety direction and showed that additional conversion at higher temperature did not translate into much additional target yield. This was the first reason to reject a simple strategy of maximizing conversion.

Batches 4 and 5 changed the mechanistic interpretation most strongly. With the same nominal water/Catalyst D/420 K formulation, the final results progressed from batch 4 at 1800 s—conversion 0.8266, yield 0.7279, byproduct 0.1101, and degradation warning 0.0594—to batch 1 at 3300 s, and then to batch 5 at 6000 s—conversion 0.9944, yield 0.6761, byproduct 0.3301, and degradation warning 0.2755. The decline in yield between 3300 and 6000 s despite increasing conversion motivated the K1 statement that the target has a finite processing window and is vulnerable during prolonged hot residence. Before batch 5, a purely parallel R-to-P/R-to-B picture remained more plausible; afterward, sequential loss of P or strongly time-varying branching had to be considered.

Batches 6-8 changed my catalyst model. I initially could have treated catalyst identity as a scalar activity factor. The results did not support that simplification. Catalyst A in batch 6 was slower but cleaner, Catalyst D in batch 1 was fastest and highest-yielding at that time, and Catalyst C in batch 8 was poor in both conversion and selectivity. That led K1 to state that catalyst identity affects both total rate and pathway branching.

Batches 9-11 changed the solvent interpretation. Conversion remained high in every solvent, but yield, selectivity, byproduct, degradation, and risk varied substantially. Toluene in batch 11, for example, gave conversion 0.9621 but only 0.5688 yield and 0.5944 selectivity. This showed that conversion alone was an inadequate response variable and supported solvent-dependent branching or target loss.

Batch 12 changed the interpretation of quench from an administrative operation to a process boundary. After 1800 s at a 420 K target, quenching reduced displayed risk from 0.2256 to 0.0793 and the subsequent 1500 s wait produced no displayed compositional evolution. The small final chemical differences from unquenched batch 4 were not enough to prove that quenching improved yield, but the risk reduction and apparent arrest were clear.

Several design choices depended on unverified assumptions. The one-factor-at-a-time catalyst and solvent comparisons assumed that effects would be interpretable around a single reference context. The duration grid assumed that 1800, 3300, and 6000 s would span the useful window. The high-temperature batch and long-duration batch assumed that informative deterioration could be observed without an unsafe outcome. The choice to use one HPLC measurement near each endpoint, rather than a genuine within-batch time course, was primarily a resource-allocation decision rather than a mechanistically justified one.

3. Principal competing mechanisms and what the data distinguish

K1 proposed a network with desired formation R -> P, parallel side formation R -> B, and secondary loss P -> D, optionally coupled to catalyst deactivation. The most important competing explanation is a purely parallel network whose branching ratio changes with time because the catalyst or reaction medium evolves:

R -> P
R -> B

a_active -> a_modified

In that alternative, yield can peak without literal degradation of isolated P if the late reaction increasingly favors B and little R remains. A reversible desired step, R <-> P, combined with irreversible R or P conversion to B is another credible alternative. Product inhibition, catalyst poisoning, equilibrium limitation, and analytical matrix changes can also mimic parts of the observed behavior.

The existing experiments distinguish a constant-selectivity, irreversible single-path model from the broader class of competing-path models. Batch 5 decisively contradicts the idea that more conversion must monotonically produce more retained target. The catalyst and solvent series also distinguish a single universal rate multiplier from a model in which branching depends on catalyst and solvent.

They do not uniquely distinguish direct R -> B from P -> D. Cross-batch endpoint measurements cannot establish whether target concentration actually rose and then fell inside a single vessel. They also cannot separate catalyst deactivation from reagent depletion or approach to equilibrium. The declining crude apparent first-order rate at long time is consistent with all three.

The data weakly favor genuine secondary target loss because yield decreased while byproduct and degradation-warning signals rose substantially from 3300 to 6000 s. However, K1 appropriately called this a favored account rather than a proven microscopic pathway. No isolated-product stability test, catalyst restart test, reversible perturbation, or dense time course was performed.

The safety behavior is also nonunique. The duration-independent risk at a fixed target and its sharp quench response suggest a thermal-state quantity, but the experiments cannot tell whether the latent cause is temperature, pressure, volatile inventory, solvent-specific hazard, or a composite score. The phrase in K1 that risk behaves “more like a state or peak-temperature hazard than an integrated thermal dose” remains a phenomenological inference.

4. One additional complete experiment

If exactly one additional legal complete experiment were allowed, I would run a within-batch time course under the formulation that dominates the sealed prediction questions: 0.003 mol reagent, 0.000525 mol Catalyst B, 0.005 L acetonitrile, and 400 rpm at a 420 K target. I would heat in consecutive segments to cumulative times of 1500, 3300, and 5100 s, taking an HPLC measurement after each segment. I would then quench promptly, terminate, and obtain the required final assay.

This experiment would be more informative than another isolated endpoint for two reasons. First, it would directly anchor the previously untested catalyst-solvent-volume-stirring combination used in Q01-Q12. Second, repeated measurements in one vessel would reduce cross-batch confounding when asking whether target yield peaks and declines.

Possible outcomes would update the account differently:

- If conversion rose throughout, yield peaked near 3300 s and then declined, while byproduct increased, that would strongly support secondary target loss or an equivalent within-vessel time-dependent selectivity change. It would also support the qualitative basis of Q05, Q01, and Q06.
- If yield remained monotonic through 5100 s while selectivity stayed roughly constant, the K1 degradation picture would be too strongly generalized from the water/Catalyst D system. The poor long-time batch 5 result would then look interaction-specific rather than universal.
- If conversion stopped increasing early but yield later declined, reversible target formation or direct P degradation would become more plausible than merely changing parallel branching from remaining R.
- If both conversion and composition plateaued early, catalyst deactivation, equilibrium, or transport limitation would become more important.
- If the quench changed composition materially between the last HPLC result and final assay, my assumption in Q02 and Q10 that quenching primarily changes risk would need revision.

Even this experiment would not prove molecular identities. Multiple HPLC measurements consume small samples and segmented heating is not perfectly identical to uninterrupted heating, so those perturbations would have to be acknowledged.

5. Tradeoff between mechanistic identifiability and operating score

The campaign emphasized mechanistic coverage more than score optimization. Batch 3 at 440 K, batch 5 at 6000 s, batch 8 with Catalyst C, and batch 11 with toluene were knowingly likely to be inferior operating conditions. Their observed scores—approximately 0.392, 0.363, 0.321, and 0.272—were lower than the best batches, but they exposed temperature risk, long-time deterioration, catalyst-dependent branching, and solvent effects. Those experiments sacrificed immediate score for identifiability.

Conversely, batch 12 served both research and operating goals. It tested whether quench timing changes the terminal state and also produced the highest observed score, 0.4777. Selecting it as the recommendation was an optimization-oriented decision made after broad exploration.

The design did not fully optimize either objective. Mechanistic identifiability was limited by one-factor-at-a-time comparisons, sparse time points, lack of replication, and the absence of catalyst-solvent interactions. Score optimization was limited because I did not perform a fine local search around the promising region. For example, a 400 K condition with an optimized duration followed by quench was never tested, even though batch 2 and batch 12 jointly suggest that it could outperform the sealed recommendation.

The stated research goal explicitly made explanatory and predictive understanding primary and the safe score secondary. That justified allocating batches to poor catalysts, poor solvents, and prolonged heating rather than spending all 12 batches refining a local maximum. The cost was that the final recommendation was selected from a coarse design rather than from a dedicated optimization study.

6. Underused evidence and weaknesses in the blind predictions

The paired HPLC and final-assay results were not exploited quantitatively enough. I noted cross-instrument discrepancies but did not estimate a calibration offset, variance component, or condition-dependent bias. The known instrument noise specifications could also have been propagated more formally into the prediction intervals.

The public heat-state deltas were used qualitatively, but I did not reconstruct even a simple thermal-response model. The approximately compressed response to 400, 420, and 440 K targets could have informed staged-temperature predictions more systematically. Likewise, solvent-specific setup risk and heat-associated risk increments could have been fit rather than estimated informally.

I relied mainly on processed estimates and did not analyze the referenced raw spectral artifacts. Raw peak shapes, missingness, replicate signals, or channel covariance might have helped distinguish analytical noise from true process variation. That omission was partly practical, but it reduced the evidential use of measurements already obtained.

Batches 4 and 12 provided a valuable partial replication before their termination procedures. Their pre-quench HPLC differences gave an empirical view of batch-plus-instrument variation, yet the blind intervals were still largely judgmental rather than derived from that replicate contrast.

The least reliable blind predictions are Q07 and Q08 because no staged temperature sequence was tested. Their predictions assumed both kinetic path dependence and a particular interpretation of terminal versus peak safety. The Q08 safety interval of 0.08-0.24 may be too narrow because a prior 450 K exposure could remain encoded in the public risk state even after a lower-temperature stage.

Q12 is also highly unreliable. It combines 460 K and 6300 s, beyond the tested maximum target and duration jointly, and may invoke nonlinear degradation, a constraint response, or rollback. Although its intervals were broad, the conversion interval of 0.97-1.00 and the particular yield/selectivity ranges still express more structural confidence than the evidence warrants.

Q11 extrapolates to 370 K, below the tested range, while using a long duration. Its conversion, yield, and byproduct intervals are likely too narrow because activation-energy uncertainty compounds strongly at the low-temperature extreme.

Q04, Q09, and Q10 extrapolate thermal risk above the directly tested range. Q10 additionally assumes that quench efficacy transfers unchanged from 420 to 440 K and from water/Catalyst D to acetonitrile/Catalyst B. That assumption was not tested, making its risk interval potentially too narrow.

Even Q01 and Q02 are less secure than their intervals imply. Every blind query combines Catalyst B with acetonitrile, 0.005 L solvent, and 400 rpm, whereas the campaign varied catalyst and solvent separately at 0.0075 L and 600 rpm. Catalyst-solvent interaction, concentration effects, and mixing effects were explicitly listed in K1 as unidentified. Additively combining the separate Catalyst B and acetonitrile effects was therefore convenient but unvalidated.

This exposes a tension with K1. K1 correctly limited quantitative use to the tested charge, 600 rpm, 0.0075 L scale, and local temperature range, and warned that catalyst-solvent interactions were unmapped. The blind task necessarily required extrapolation outside that scope, but several Q intervals did not expand enough to reflect the stated limitations. The point predictions were defensible hypotheses; their apparent precision was less defensible.

The score predictions were especially indirect. I inferred score behavior from observed response combinations rather than knowing the evaluator’s complete internal transformation. Correlations among yield, selectivity, byproduct, and risk make such a fitted relationship unstable outside the observed design. Score intervals should therefore have been at least as conservative as the widest underlying process uncertainty.

7. Limitations of the sealed recommendation

Batch 12 was the sample-best observed experiment, not a proven optimum. Its final score of 0.4777 was the highest among the 12 completed batches, and its risk of 0.0793 was the lowest final post-reaction risk because it was quenched. Those statements are sample-in comparisons over the tested set.

The recommendation rests on one execution. Batch 4 is only a partial comparator: it used the same nominal formulation and 1800 s heat but was not quenched and was not a true randomized replicate. Small differences between batches 4 and 12 cannot establish a reproducible chemical advantage from quenching. The clearest demonstrated benefit is the reduction in the displayed terminal risk state.

The recommendation also confounds several choices. It does not prove that 1800 s is the best duration, that 420 K is the best target, or that Catalyst D and water remain best after duration and quench are optimized jointly. Batch 2 suggests that a lower temperature can retain comparable yield at much lower unquenched risk. A 400 K run with an adjusted duration and prompt quench might plausibly outperform batch 12, but it was not tested.

Repeatability should first be assessed with randomized replicate executions of batch 12, including both pre-quench HPLC and final assay. Reporting between-batch variation in yield, selectivity, byproduct, degradation warning, risk, and score would show whether the observed advantage exceeds measurement and process noise.

Local robustness should then be tested with a small response-surface design around the recommendation: for example, 400-420 K, roughly 1500-2400 s, modest perturbations in catalyst amount and stirring, and controlled quench delays. An unquenched control at each center condition would separate chemical optimization from the risk benefit of quenching. The local study should examine both mean performance and sensitivity to deviations, because a slightly lower mean with a flatter response could be operationally preferable.

Cross-material generalization requires factorial tests of catalyst and solvent rather than transferring the water/Catalyst D result by assumption. At minimum, the quench and duration response should be repeated for Catalyst A and B and for the alternative solvents. Cross-scale robustness requires varying volume and concentration while maintaining and then deliberately changing catalyst-to-reagent ratio and mixing intensity.

Finally, cross-world generalization is not established at all. The catalysts and kinetic solvent effects are anonymous benchmark constructs. K1 explicitly warned against inferring a named real synthesis or transferring categorical effects from ordinary solvent properties. Validation in another synthetic world would require re-estimating the catalyst, solvent, thermal-response, and risk relationships; validation in a physical chemical system would require real analytical standards, calorimetry, material identities, and independent safety review.

Thus the sealed recommendation is best described as the highest-scoring tested member of a sparse local campaign, with a well-supported terminal-risk benefit from quenching. It is not a globally optimized recipe, not yet a demonstrated robust optimum, and not evidence of transferability beyond this benchmark world.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 108.8 | none | 0 |
| Q | yes | 0 | 125.0 | none | 0 |
| K2 | yes | 0 | 113.1 | none | 0 |

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean 80% width | Mean interval score |
|---|---:|---:|---:|---:|
| byproduct_signal | 0.0383 | 0.9167 | 0.2008 | 0.2514 |
| conversion | 0.0733 | 0.2500 | 0.1475 | 0.3288 |
| safety_risk | 0.0573 | 0.6667 | 0.1233 | 0.1671 |
| score | 0.0269 | 1.0000 | 0.1717 | 0.1717 |
| selectivity | 0.0476 | 0.8000 | 0.2100 | 0.2466 |
| yield | 0.0598 | 0.7000 | 0.2067 | 0.3470 |

## Predictions versus released reference truth

### Q01

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2910 | 0.2100 | 0.3800 | 0.2826 | 0.2852, 0.2894, 0.2712, 0.2806, 0.2868 |
| conversion | 0.9400 | 0.8700 | 0.9800 | 0.9936 | 0.9944, 0.9886, 0.9985, 1.0000, 0.9865 |
| safety_risk | 0.2450 | 0.2000 | 0.3000 | 0.2975 | 0.2975, 0.2975, 0.2975, 0.2975, 0.2975 |
| score | 0.3660 | 0.3000 | 0.4300 | 0.3741 | 0.3745, 0.3704, 0.3762, 0.3731, 0.3761 |
| selectivity | 0.7200 | 0.6300 | 0.8000 | 0.7204 | 0.7250, 0.7175, 0.7148, 0.7117, 0.7328 |
| yield | 0.6800 | 0.6000 | 0.7500 | 0.7164 | 0.7143, 0.7102, 0.7240, 0.7179, 0.7156 |
### Q02

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2910 | 0.2100 | 0.3800 | 0.2861 | 0.2908, 0.2824, 0.2881, 0.2929, 0.2764 |
| conversion | 0.9400 | 0.8700 | 0.9800 | 0.9921 | 0.9993, 1.0000, 0.9838, 0.9912, 0.9863 |
| safety_risk | 0.0900 | 0.0500 | 0.1400 | 0.1512 | 0.1512, 0.1512, 0.1512, 0.1512, 0.1512 |
| score | 0.4210 | 0.3500 | 0.4900 | 0.4400 | 0.4421, 0.4407, 0.4410, 0.4418, 0.4345 |
| selectivity | 0.7200 | 0.6300 | 0.8000 | 0.7247 | 0.7349, 0.7269, 0.7271, 0.7216, 0.7132 |
| yield | 0.6800 | 0.6000 | 0.7500 | 0.7228 | 0.7198, 0.7212, 0.7257, 0.7294, 0.7176 |
### Q03

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1850 | 0.1100 | 0.2700 | 0.2305 | 0.2338, 0.2259, 0.2177, 0.2369, 0.2383 |
| conversion | 0.8400 | 0.7200 | 0.9200 | 0.9608 | 0.9596, 0.9490, 0.9674, 0.9626, 0.9652 |
| safety_risk | 0.1150 | 0.0700 | 0.1700 | 0.1854 | 0.1854, 0.1854, 0.1854, 0.1854, 0.1854 |
| score | 0.4280 | 0.3500 | 0.5000 | 0.4438 | 0.4466, 0.4474, 0.4404, 0.4439, 0.4408 |
| selectivity | 0.8050 | 0.7100 | 0.8800 | 0.7671 | 0.7763, 0.7752, 0.7648, 0.7603, 0.7591 |
| yield | 0.6650 | 0.5600 | 0.7400 | 0.7437 | 0.7453, 0.7506, 0.7349, 0.7477, 0.7399 |
### Q04

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3450 | 0.2400 | 0.4600 | 0.3349 | 0.3411, 0.3290, 0.3394, 0.3241, 0.3407 |
| conversion | 0.9920 | 0.9500 | 1.0000 | 0.9971 | 0.9964, 0.9936, 0.9975, 0.9981, 1.0000 |
| safety_risk | 0.3550 | 0.2900 | 0.4300 | 0.4031 | 0.4031, 0.4031, 0.4031, 0.4031, 0.4031 |
| score | 0.2980 | 0.2000 | 0.3900 | 0.2995 | 0.3030, 0.2973, 0.3051, 0.2950, 0.2974 |
| selectivity | 0.6550 | 0.5300 | 0.7500 | 0.6731 | 0.6859, 0.6698, 0.6734, 0.6614, 0.6750 |
| yield | 0.6500 | 0.5300 | 0.7400 | 0.6776 | 0.6782, 0.6748, 0.6911, 0.6732, 0.6704 |
### Q05

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1500 | 0.0800 | 0.2300 | 0.1390 | 0.1313, 0.1497, 0.1384, 0.1357, 0.1399 |
| conversion | 0.7650 | 0.6300 | 0.8700 | 0.8939 | 0.9038, 0.8951, 0.8931, 0.8821, 0.8954 |
| safety_risk | 0.2450 | 0.2000 | 0.3000 | 0.2972 | 0.2972, 0.2972, 0.2972, 0.2972, 0.2972 |
| score | 0.3680 | 0.2900 | 0.4400 | 0.4181 | 0.4209, 0.4187, 0.4150, 0.4146, 0.4214 |
| selectivity | 0.8200 | 0.7200 | 0.8900 | 0.8564 | 0.8553, 0.8572, 0.8540, 0.8567, 0.8586 |
| yield | 0.6250 | 0.5100 | 0.7100 | 0.7624 | 0.7676, 0.7631, 0.7562, 0.7563, 0.7688 |
### Q06

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3750 | 0.2700 | 0.4900 | 0.4142 | 0.4168, 0.4031, 0.4113, 0.4196, 0.4205 |
| conversion | 0.9750 | 0.9200 | 1.0000 | 0.9945 | 0.9842, 0.9940, 0.9980, 1.0000, 0.9961 |
| safety_risk | 0.2450 | 0.2000 | 0.3000 | 0.2972 | 0.2972, 0.2972, 0.2972, 0.2972, 0.2972 |
| score | 0.3260 | 0.2400 | 0.4000 | 0.2977 | 0.2966, 0.2960, 0.3021, 0.2986, 0.2951 |
| selectivity | 0.6500 | 0.5300 | 0.7500 | 0.6004 | 0.6005, 0.5997, 0.6043, 0.6057, 0.5920 |
| yield | 0.6200 | 0.5000 | 0.7100 | 0.6037 | 0.6035, 0.6000, 0.6114, 0.6014, 0.6020 |
### Q07

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3200 | 0.2100 | 0.4400 | 0.3184 | 0.3152, 0.3252, 0.3252, 0.3153, 0.3110 |
| conversion | 0.9500 | 0.8700 | 0.9900 | 0.9980 | 1.0000, 1.0000, 1.0000, 1.0000, 0.9902 |
| safety_risk | 0.3550 | 0.2700 | 0.4500 | 0.4275 | 0.4275, 0.4275, 0.4275, 0.4275, 0.4275 |
| score | 0.3130 | 0.2100 | 0.4100 | 0.3011 | 0.3054, 0.3035, 0.2994, 0.2993, 0.2978 |
| selectivity | 0.6900 | 0.5600 | 0.7900 | 0.6925 | 0.7058, 0.6881, 0.6972, 0.6796, 0.6920 |
| yield | 0.6650 | 0.5400 | 0.7500 | 0.6972 | 0.6993, 0.7056, 0.6895, 0.7005, 0.6912 |
### Q08

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2800 | 0.1800 | 0.4000 | 0.3216 | 0.3273, 0.3191, 0.3086, 0.3218, 0.3312 |
| conversion | 0.9400 | 0.8500 | 0.9900 | 0.9968 | 0.9991, 1.0000, 0.9973, 0.9961, 0.9914 |
| safety_risk | 0.1450 | 0.0800 | 0.2400 | 0.1975 | 0.1975, 0.1975, 0.1975, 0.1975, 0.1975 |
| score | 0.4090 | 0.3000 | 0.5000 | 0.4075 | 0.4073, 0.4070, 0.4041, 0.4125, 0.4069 |
| selectivity | 0.7300 | 0.6000 | 0.8200 | 0.7016 | 0.7006, 0.7052, 0.6910, 0.7046, 0.7067 |
| yield | 0.6900 | 0.5700 | 0.7800 | 0.6992 | 0.6986, 0.6948, 0.6970, 0.7099, 0.6957 |
### Q09

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2200 | 0.1300 | 0.3200 | 0.1517 | 0.1510, 0.1588, 0.1357, 0.1541, 0.1589 |
| conversion | 0.8500 | 0.7300 | 0.9300 | 0.9456 | 0.9443, 0.9462, 0.9392, 0.9438, 0.9543 |
| safety_risk | 0.3220 | 0.2600 | 0.3900 | 0.3768 | 0.3768, 0.3768, 0.3768, 0.3768, 0.3768 |
| score | 0.3330 | 0.2400 | 0.4200 | 0.3984 | 0.3958, 0.4013, 0.3970, 0.3990, 0.3989 |
| selectivity | 0.7500 | 0.6300 | 0.8400 | 0.8476 | 0.8351, 0.8618, 0.8575, 0.8339, 0.8498 |
| yield | 0.6500 | 0.5400 | 0.7400 | 0.7952 | 0.7969, 0.7935, 0.7871, 0.8057, 0.7929 |
### Q10

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2200 | 0.1300 | 0.3200 | 0.1532 | 0.1524, 0.1604, 0.1493, 0.1485, 0.1556 |
| conversion | 0.8500 | 0.7300 | 0.9300 | 0.9459 | 0.9443, 0.9377, 0.9581, 0.9487, 0.9408 |
| safety_risk | 0.1000 | 0.0500 | 0.1700 | 0.1712 | 0.1712, 0.1712, 0.1712, 0.1712, 0.1712 |
| score | 0.4120 | 0.3200 | 0.5000 | 0.4888 | 0.4881, 0.4857, 0.4916, 0.4910, 0.4875 |
| selectivity | 0.7500 | 0.6300 | 0.8400 | 0.8509 | 0.8547, 0.8603, 0.8394, 0.8540, 0.8458 |
| yield | 0.6500 | 0.5400 | 0.7400 | 0.7961 | 0.7925, 0.7846, 0.8071, 0.7989, 0.7972 |
### Q11

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1600 | 0.0800 | 0.2600 | 0.3207 | 0.3220, 0.3285, 0.3186, 0.3278, 0.3067 |
| conversion | 0.7800 | 0.6100 | 0.9000 | 0.9808 | 0.9709, 0.9777, 0.9940, 0.9742, 0.9873 |
| safety_risk | 0.0750 | 0.0400 | 0.1300 | 0.1548 | 0.1548, 0.1548, 0.1548, 0.1548, 0.1548 |
| score | 0.4360 | 0.3400 | 0.5200 | 0.4068 | 0.4034, 0.4056, 0.4113, 0.4075, 0.4063 |
| selectivity | 0.8200 | 0.7000 | 0.9000 | 0.6769 | 0.6720, 0.6683, 0.6786, 0.6851, 0.6803 |
| yield | 0.6550 | 0.5100 | 0.7500 | 0.6732 | 0.6701, 0.6762, 0.6801, 0.6713, 0.6682 |
### Q12

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5800 | 0.4200 | 0.7300 | 0.5786 | 0.5786, 0.5797, 0.5783, 0.5826, 0.5738 |
| conversion | 0.9990 | 0.9700 | 1.0000 | 0.9966 | 0.9974, 0.9885, 0.9990, 0.9992, 0.9990 |
| safety_risk | 0.4000 | 0.3200 | 0.4900 | 0.4202 | 0.4202, 0.4202, 0.4202, 0.4202, 0.4202 |
| score | 0.1270 | 0.0300 | 0.2300 | 0.1418 | 0.1464, 0.1386, 0.1392, 0.1429, 0.1417 |
| selectivity | 0.4000 | 0.2400 | 0.5700 | 0.4511 | 0.4571, 0.4436, 0.4565, 0.4418, 0.4566 |
| yield | 0.4200 | 0.2500 | 0.5700 | 0.4475 | 0.4551, 0.4464, 0.4372, 0.4555, 0.4432 |

## Recommendation retest

- Selected source batch: `12`
- Retest exact replay verified: `True`
- Retest failure: `none`

| Metric | Selected source batch | Independent retest | Retest minus source |
|---|---:|---:|---:|
| byproduct_signal | 0.1039 | 0.1094 | 0.0055 |
| conversion | 0.8324 | 0.8178 | -0.0147 |
| cost | 0.8164 | 0.8164 | 0.0000 |
| degradation_warning | 0.0447 | 0.0590 | 0.0143 |
| safety_risk | 0.0793 | 0.0793 | 0.0000 |
| score | 0.4777 | 0.4735 | -0.0042 |
| selectivity | 0.8884 | 0.8907 | 0.0023 |
| virtual_spectrum_summary | 0.0773 | 0.0867 | 0.0094 |
| yield | 0.7242 | 0.7159 | -0.0083 |

## Scope note

This is the final sanitized report produced after all 60 source sessions and K1/Q/K2 chains were sealed. It includes released reference truth, blind-prediction evaluation, and the independent recommendation retest. Provider-private event streams, credentials, thread identifiers, and token accounting remain excluded.
