# RX-W03--S--mechanism_discovery--Opaque

## Run summary

- World: `RX-W03`
- Locus: `S`
- Goal: `mechanism_discovery`
- Arm: `Opaque`
- Status: `completed`
- Source status: `completed`
- Experimental sessions: `12/12`
- Operations: `85`
- Exact replay verified: `True`
- Rollbacks: `[]`
- Posttest chain sealed: `True`

### Recovery status

- Effective result location: `posttest-repair-v10`
- Recovery version: `recovery-v10-parallel4-continue`
- Repaired stages: `Q, K2`
- Source experiments rerun: `False`
- Original source thread reused: `True`
- Truth revealed during recovery: `False`

## Sealed recommendation

- Selected batch: `12`
- Rationale: Best balanced operating point: Catalyst D in acetonitrile, 370 K boundary heating for 3600 s followed by quench gave 0.573 yield, 0.762 selectivity, low 0.085 degradation warning, and 0.185 safety risk. It also provided a direct quench comparison to the otherwise matched unquenched batch 4.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S2 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 370 K x 3600 s @ 600 rpm | no | 0.4526 | 0.6830 | 0.6735 | 0.2202 | 0.0538 | 0.1861 | 0.2354 |
| 2 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 370 K x 3600 s @ 600 rpm | no | 0.6308 | 0.6774 | 0.9408 | 0.3158 | 0.2333 | 0.2155 | 0.3187 |
| 3 | S2 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 370 K x 3600 s @ 600 rpm | no | 0.5827 | 0.6974 | 0.8378 | 0.2471 | 0.1044 | 0.2027 | 0.3000 |
| 4 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 370 K x 3600 s @ 600 rpm | no | 0.5893 | 0.7582 | 0.7598 | 0.1947 | 0.0940 | 0.2009 | 0.3109 |
| 5 | S0 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 370 K x 3600 s @ 600 rpm | no | 0.4255 | 0.7890 | 0.5556 | 0.1272 | 0.0211 | 0.1381 | 0.2609 |
| 6 | S1 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 370 K x 3600 s @ 600 rpm | no | 0.4724 | 0.7395 | 0.6506 | 0.1746 | 0.0393 | 0.1689 | 0.2629 |
| 7 | S3 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 370 K x 3600 s @ 600 rpm | no | 0.4232 | 0.5961 | 0.6991 | 0.2894 | 0.0612 | 0.1976 | 0.1993 |
| 8 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 340 K x 7200 s @ 600 rpm | no | 0.5552 | 0.6597 | 0.8277 | 0.2853 | 0.1563 | 0.1892 | 0.2846 |
| 9 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 400 K x 1800 s @ 600 rpm | no | 0.5209 | 0.8144 | 0.6364 | 0.1147 | 0.0421 | 0.2503 | 0.2630 |
| 10 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 370 K x 1800 s @ 600 rpm | no | 0.4172 | 0.8286 | 0.5005 | 0.0820 | 0.0190 | 0.1775 | 0.2442 |
| 11 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 370 K x 7200 s @ 600 rpm | no | 0.5775 | 0.6341 | 0.9468 | 0.3920 | 0.2646 | 0.2128 | 0.2884 |
| 12 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 370 K x 3600 s @ 600 rpm | yes | 0.5734 | 0.7616 | 0.7905 | 0.2032 | 0.0846 | 0.1849 | 0.3156 |

## Complete experimental actions and observations

### Batch 1

Lifecycle index: `1`; end step: `7`.

```json
{
  "actions": [
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
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
  "end_step": 7,
  "lifecycle_index": 1,
  "metrics": {
    "byproduct_signal": 0.22022517025470734,
    "conversion": 0.6735041737556458,
    "cost": 1.0,
    "degradation_warning": 0.05377498269081116,
    "safety_risk": 0.18605010211467743,
    "score": 0.23539786040782928,
    "selectivity": 0.6829794645309448,
    "virtual_spectrum_summary": 0.14532257616519928,
    "yield": 0.4525628089904785
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
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
    "byproduct_signal": 0.3157874345779419,
    "conversion": 0.9407682418823242,
    "cost": 1.0,
    "degradation_warning": 0.23327074944972992,
    "safety_risk": 0.21553504467010498,
    "score": 0.3187483251094818,
    "selectivity": 0.6774080991744995,
    "virtual_spectrum_summary": 0.27865493297576904,
    "yield": 0.6307756304740906
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
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
    "byproduct_signal": 0.2470770627260208,
    "conversion": 0.8377828001976013,
    "cost": 1.0,
    "degradation_warning": 0.10442141443490982,
    "safety_risk": 0.20271287858486176,
    "score": 0.29996445775032043,
    "selectivity": 0.6973757147789001,
    "virtual_spectrum_summary": 0.18288202583789825,
    "yield": 0.5826576352119446
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
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
    "byproduct_signal": 0.1946539282798767,
    "conversion": 0.7597655653953552,
    "cost": 1.0,
    "degradation_warning": 0.09397058933973312,
    "safety_risk": 0.20087462663650513,
    "score": 0.31087467074394226,
    "selectivity": 0.7582142353057861,
    "virtual_spectrum_summary": 0.14934642612934113,
    "yield": 0.5893453359603882
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
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
    "byproduct_signal": 0.12723137438297272,
    "conversion": 0.5555971264839172,
    "cost": 1.0,
    "degradation_warning": 0.02110070362687111,
    "safety_risk": 0.1381237804889679,
    "score": 0.26085689663887024,
    "selectivity": 0.7889774441719055,
    "virtual_spectrum_summary": 0.07947257161140442,
    "yield": 0.42552128434181213
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.08
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
    "byproduct_signal": 0.17461545765399933,
    "conversion": 0.6505774855613708,
    "cost": 1.0,
    "degradation_warning": 0.039266228675842285,
    "safety_risk": 0.16887862980365753,
    "score": 0.2628955543041229,
    "selectivity": 0.7394509315490723,
    "virtual_spectrum_summary": 0.11370830237865448,
    "yield": 0.4724261164665222
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 3,
      "volume_L": 0.08
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
    "byproduct_signal": 0.2893810570240021,
    "conversion": 0.6990902423858643,
    "cost": 1.0,
    "degradation_warning": 0.06121421977877617,
    "safety_risk": 0.19758416712284088,
    "score": 0.19930499792099,
    "selectivity": 0.5960568785667419,
    "virtual_spectrum_summary": 0.18670599162578583,
    "yield": 0.42323657870292664
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
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
  "end_step": 56,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.2852846384048462,
    "conversion": 0.8277415633201599,
    "cost": 1.0,
    "degradation_warning": 0.1562759429216385,
    "safety_risk": 0.18920719623565674,
    "score": 0.28464755415916443,
    "selectivity": 0.6596953272819519,
    "virtual_spectrum_summary": 0.2272307127714157,
    "yield": 0.555232048034668
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
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
    "byproduct_signal": 0.11466934531927109,
    "conversion": 0.6364141702651978,
    "cost": 1.0,
    "degradation_warning": 0.04209503158926964,
    "safety_risk": 0.2502940893173218,
    "score": 0.26297664642333984,
    "selectivity": 0.8144156336784363,
    "virtual_spectrum_summary": 0.0820109024643898,
    "yield": 0.5209091305732727
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
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
    "byproduct_signal": 0.08199546486139297,
    "conversion": 0.5005097985267639,
    "cost": 1.0,
    "degradation_warning": 0.018964676186442375,
    "safety_risk": 0.17747145891189575,
    "score": 0.24423116445541382,
    "selectivity": 0.8286420702934265,
    "virtual_spectrum_summary": 0.053631607443094254,
    "yield": 0.4172045588493347
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
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
  "end_step": 77,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.39197343587875366,
    "conversion": 0.9467801451683044,
    "cost": 1.0,
    "degradation_warning": 0.26463982462882996,
    "safety_risk": 0.21284019947052002,
    "score": 0.2884095311164856,
    "selectivity": 0.6340625286102295,
    "virtual_spectrum_summary": 0.33467331528663635,
    "yield": 0.5774849653244019
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
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
      "target_temperature_K": 370
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
    "byproduct_signal": 0.2032492607831955,
    "conversion": 0.7905266284942627,
    "cost": 1.0,
    "degradation_warning": 0.0845905989408493,
    "safety_risk": 0.18487150967121124,
    "score": 0.3156053125858307,
    "selectivity": 0.7616022825241089,
    "virtual_spectrum_summary": 0.14985285699367523,
    "yield": 0.5733606219291687
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

1. Scope and evidence

This report concerns an anonymous benchmark reaction, not an identified real synthesis. All twelve vessels used 0.040 mol limiting reagent, 0.080 L solvent, 0.005 mol catalyst, and 600 rpm stirring. Therefore, the evidence identifies categorical catalyst and solvent effects plus temperature, time, and quench effects, but it does not identify concentration orders, catalyst-loading dependence, or a real molecular mechanism.

The measured final quantities are dimensionless public assay estimates. “Conversion” describes disappearance of reactant proxy, “yield” target formation, “selectivity” allocation toward target rather than competing material, “byproduct signal” competing conversion, and “degradation warning” accumulated damage. Instrument uncertainty and uncontrolled synthetic process variation mean that small differences should not be overinterpreted.

2. Proposed operating mechanism

The simplest account consistent with the campaign is a catalytic network containing both parallel and consecutive reactions:

R --kP(T,S,C)·a(t)--> P
R --kB(T,S,C)·a(t)--> B
P --kD(T,S,C)--> D

R is the limiting reactant, P the desired target, B a directly competing byproduct, D degraded target or other late impurity, S solvent, C catalyst identity, and a(t) the fraction of active catalyst.

A useful provisional rate model is:

dR/dt = -a(t)[kP(T,S,C)+kB(T,S,C)]R

dP/dt = a(t)kP(T,S,C)R - kD(T,S,C)P

dB/dt = a(t)kB(T,S,C)R + fB kD(T,S,C)P

da/dt = -kdeact(T,S,C)a

with Arrhenius-like temperature dependence, ki(T)=Ai exp[-Ei/(RT)]. The observations do not establish literal first-order kinetics; these equations are a compact phenomenological hypothesis.

The measured yield is approximately, but not exactly, conversion multiplied by selectivity. For example, batch 4 gave conversion 0.7598 and selectivity 0.7582, whose product is about 0.576, close to its measured yield of 0.5893. Similar approximate agreement occurs elsewhere. Deviations are compatible with assay noise, distinct channel calibrations, degradation accounting, or a selectivity definition that is not exactly P/(all converted material).

The model implies three coupled regimes:

• Early reaction: target formation dominates; conversion and yield rise while selectivity is high.
• Intermediate reaction: target yield approaches a maximum as unreacted material remains available but competing conversion grows.
• Excess thermal exposure: conversion continues toward completion, but byproduct and degradation channels increasingly consume material or target, lowering selectivity and eventually lowering target yield.

Catalyst and solvent change both the productive rate and the ratio kP/kB; they cannot be represented only as uniform rate multipliers. Temperature and duration determine integrated thermal exposure, while quenching ends or sharply suppresses the kinetic network. Safety risk is additionally coupled to solvent identity, requested temperature, heating duration, and thermal history rather than being determined by chemical yield alone.

3. Evidence for catalyst effects

Batches 1–4 held solvent, nominal temperature, duration, amounts, and stirring constant: acetonitrile, 370 K, 3600 s, 0.040 mol reagent, 0.005 mol catalyst, and 600 rpm.

• Batch 1, Catalyst A: conversion 0.6735, yield 0.4526, selectivity 0.6830, byproduct 0.2202, degradation 0.0538, risk 0.1861.
• Batch 2, Catalyst B: conversion 0.9408, yield 0.6308, selectivity 0.6774, byproduct 0.3158, degradation 0.2333, risk 0.2155.
• Batch 3, Catalyst C: conversion 0.8378, yield 0.5827, selectivity 0.6974, byproduct 0.2471, degradation 0.1044, risk 0.2027.
• Batch 4, Catalyst D: conversion 0.7598, yield 0.5893, selectivity 0.7582, byproduct 0.1947, degradation 0.0940, risk 0.2009.

Catalyst B was the strongest conversion promoter and produced the largest observed yield in this screen, but it also produced the largest byproduct and degradation signals. Catalyst D produced less conversion than B or C yet had the best selectivity and almost the same yield as C. Thus catalyst identity changes selectivity and damage propensity, not merely total reaction speed. This evidence caused me to reject a single “catalyst activity factor” model and instead assign catalyst-specific productive, competing, and possibly deactivation constants.

The data do not distinguish whether Catalyst B directly accelerates degradation, simply reaches high conversion earlier and leaves more time for secondary damage, or undergoes deactivation that releases a species favoring byproducts. Those are competing explanations.

4. Evidence for solvent effects

Batches 4–7 used Catalyst D at nominally 370 K for 3600 s.

• Batch 5, water: conversion 0.5556, yield 0.4255, selectivity 0.7890, byproduct 0.1272, degradation 0.0211, risk 0.1381.
• Batch 6, ethanol: conversion 0.6506, yield 0.4724, selectivity 0.7395, byproduct 0.1746, degradation 0.0393, risk 0.1689.
• Batch 4, acetonitrile: conversion 0.7598, yield 0.5893, selectivity 0.7582, byproduct 0.1947, degradation 0.0940, risk 0.2009.
• Batch 7, toluene: conversion 0.6991, yield 0.4232, selectivity 0.5961, byproduct 0.2894, degradation 0.0612, risk 0.1976.

Water suppressed total conversion but strongly suppressed byproduct and degradation, giving the highest selectivity and lowest risk. Ethanol was intermediate. Acetonitrile gave the best target yield among these four solvents. Toluene gave substantial conversion but poor target allocation: its yield was essentially the same as water despite much greater conversion, and its byproduct signal was highest.

This pattern supports solvent-specific branching: acetonitrile favors productive turnover, water slows most chemistry and especially damage, while toluene disproportionately favors the competing pathway. A reasonable alternative is that the solvents change catalyst activation or deactivation rather than the elementary branching step. Because solvent effects are categorical benchmark effects and no catalyst-state measurement was available, these interpretations cannot be separated.

5. Time dependence and the yield maximum

Batches 10, 4, and 11 form the most informative approximate time series for Catalyst D in acetonitrile at nominally 370 K:

• Batch 10, 1800 s: conversion 0.5005, yield 0.4172, selectivity 0.8286, byproduct 0.0820, degradation 0.0190.
• Batch 4, 3600 s: conversion 0.7598, yield 0.5893, selectivity 0.7582, byproduct 0.1947, degradation 0.0940.
• Batch 11, 7200 s: conversion 0.9468, yield 0.5775, selectivity 0.6341, byproduct 0.3920, degradation 0.2646.

Conversion rose monotonically with time, but yield did not. Doubling from 1800 to 3600 s strongly increased yield; doubling again to 7200 s increased conversion by about 0.187 but slightly reduced yield, while selectivity fell by about 0.124 and degradation nearly tripled relative to batch 4. This is the clearest evidence for consecutive loss of product, increasing competing conversion, or both. It rules out a simple irreversible R→P model over the full tested time range.

The data place the target-yield maximum broadly near intermediate exposure, around the 3600 s condition at nominal 370 K for Catalyst D in acetonitrile. This location is an interpolation from sparse endpoints, not a fitted optimum.

Catalyst deactivation remains possible but is not uniquely demonstrated. Deactivation alone would cause conversion to plateau, whereas the concurrent rise in byproduct and degradation signals indicates that selectivity loss is also important. A model containing both declining productive activity and continuing side chemistry is plausible.

6. Temperature and actual thermal history

Requested setpoint is not identical to actual liquid temperature. The recorded temperature increases during heating were about 66.27 K in batch 1 at a 370 K command, 66.37 K in batch 10 at the same command, 91.23 K in batch 9 at a 400 K command, 39.63 K in batch 8 at a 340 K command, and 66.20 K in batch 11 at a 370 K command. These readings show repeatable but finite thermal approach behavior. Kinetic interpretation should therefore use the actual time–temperature trajectory or an exposure integral, not only the requested setpoint.

A minimal thermal model is:

dT/dt = [Tset-T]/τheat - qloss(T,S,V)

and an effective exposure for pathway i is:

Θi = ∫ exp[-Ei/(RT(t))]dt.

The campaign did not provide enough time-resolved temperature samples to estimate τheat or activation energies, but it clearly shows that command temperature and elapsed time are imperfect substitutes for Θi.

At equal 1800 s duration, raising the nominal temperature from 370 K in batch 10 to 400 K in batch 9 changed conversion from 0.5005 to 0.6364 and yield from 0.4172 to 0.5209. Selectivity remained fairly high but declined from 0.8286 to 0.8144, degradation rose from 0.0190 to 0.0421, and safety risk rose sharply from 0.1775 to 0.2503. Higher temperature therefore accelerates productive reaction, side reaction, and operational risk.

At 7200 s, raising nominal temperature from 340 K in batch 8 to 370 K in batch 11 changed conversion from 0.8277 to 0.9468 and yield from 0.5552 to 0.5775, but selectivity fell from 0.6597 to 0.6341, byproduct rose from 0.2853 to 0.3920, degradation rose from 0.1563 to 0.2646, and risk rose from 0.1892 to 0.2128. The relatively small yield gain despite much larger damage supports differing activation sensitivities and an exposure-dependent yield maximum.

Batch 8 also shows that low temperature is not intrinsically protective if duration is long: nominal 340 K for 7200 s accumulated degradation of 0.1563. Time and temperature must be treated jointly.

7. Termination and quench

Batch 12 replicated the central Catalyst D/acetonitrile/370 K/3600 s design but inserted a quench before endpoint HPLC and termination. Its final assay was conversion 0.7905, yield 0.5734, selectivity 0.7616, byproduct 0.2032, degradation 0.0846, and safety risk 0.1849.

The closest unquenched comparison, batch 4, gave conversion 0.7598, yield 0.5893, selectivity 0.7582, byproduct 0.1947, degradation 0.0940, and risk 0.2009. The differences are modest: quenching was associated with slightly lower degradation and risk, essentially unchanged selectivity, and slightly lower yield. Given one vessel per condition and assay/process variability, this is evidence that quenching is compatible with preserving the intermediate-exposure state, but it is not strong evidence for a large chemical yield benefit. It does support the process interpretation that prompt cooling is useful for limiting further exposure and improving the safety profile.

I selected batch 12 as the sealed operating recommendation because it balanced yield 0.5734, selectivity 0.7616, low degradation 0.0846, and risk 0.1849. This was a robustness and safety choice rather than the single highest observed yield. Batch 2 had the highest observed yield, 0.6308, but substantially worse degradation, byproduct, and risk.

8. Prediction rules within the studied domain

For conditions close to 0.040 mol reagent, 0.080 L solvent, 0.005 mol catalyst, and 600 rpm, I would use the following qualitative simulator:

1. Propagate actual temperature with a first-order thermal-lag model.
2. Integrate temperature-dependent productive, competing, degradation, and deactivation rates.
3. Give Catalyst B the highest overall turnover but a high damage/side-reaction coefficient.
4. Give Catalyst D the highest productive selectivity and use it for balanced operation.
5. Assign acetonitrile high productive rate, water low overall rate and low damage, ethanol intermediate behavior, and toluene a high competing-branch fraction.
6. Predict rising conversion with exposure, initially rising yield, and declining selectivity after intermediate exposure.
7. Treat quench as rapidly reducing all subsequent rate constants, while acknowledging that the observed quench effect was small.

Local directional predictions are more defensible than exact numerical predictions. For Catalyst D in acetonitrile, extending a 370 K run from 1800 toward 3600 s should raise conversion and yield; extending it much beyond 3600 s toward 7200 s should mainly raise conversion, byproduct, and degradation while lowering selectivity. Raising temperature at fixed short time should raise conversion and yield but also risk and degradation.

9. Limits, non-identifiability, and competing explanations

The following factors remain unidentified:

• No catalyst-loading, reagent-loading, volume, or stirring-speed variation was performed, so kinetic orders, mass-transfer dependence, saturation, and catalyst efficiency cannot be estimated.
• Each condition had only one final vessel. Apparent differences include instrument noise and synthetic process variability.
• Measurements were endpoint or near-endpoint observations, not dense kinetic traces. Many distinct rate networks can reproduce them.
• Catalyst identities are anonymous. No claims about real catalytic species, coordination states, or named chemistry are justified.
• Solvent identities are real labels, but their reaction effects are benchmark categorical effects; ordinary physical-property arguments cannot be assumed to explain them.
• Byproduct and degradation signals do not prove separate molecular species. They could be partially overlapping assay proxies.
• The data cannot decide whether selectivity loss arises from direct parallel R→B conversion, consecutive P→D conversion, catalyst deactivation that changes selectivity, or combinations of these processes.
• Temperature was not recorded as a complete time series. Activation energies and thermal time constants are therefore not identifiable.
• The quench comparison is unreplicated, so its small apparent benefit may reflect run variation.

Reasonable competing models include: (i) two purely parallel reactions whose relative rates change with catalyst age; (ii) reversible target formation followed by an equilibrium shift and irreversible degradation; (iii) catalyst activation followed by deactivation, with inactive catalyst promoting byproduct; or (iv) transport-limited productive reaction plus homogeneous degradation. The observed time-dependent yield maximum favors inclusion of a secondary loss or changing selectivity, but it does not uniquely choose among these models.

Overall, the most economical explanation is a thermally activated catalytic branching network with secondary target degradation, catalyst-specific activity/selectivity tradeoffs, solvent-dependent branching, finite thermal lag, and a yield maximum at intermediate integrated thermal exposure.

## Q — Blind predictions

### Overall rationale

Predictions extrapolate the campaign's Catalyst B result and the Catalyst D temperature/time series using a saturating conversion model with catalyst-loading and temperature-dependent exposure. Yield and selectivity are reduced at long or severe exposure to represent competing conversion and secondary target loss. Byproduct signal is constrained to remain broadly complementary to target yield at high conversion. Safety risk increases with temperature, duration, and catalyst loading, with a small reduction for quenching. Score estimates use the empirical campaign relationship score ≈ max(0, -0.10 + 0.40·yield + 0.25·selectivity + 0.10·conversion - 0.45·safety_risk). Intervals are intentionally broad because catalyst loading, 400 rpm stirring, small batch scale, and most queried temperature-time combinations were not directly studied.

### Q01

Low Catalyst B loading and short residence time should limit conversion despite 410 K. I expect high early-time selectivity and modest byproduct formation; uncertainty is dominated by the untested loading and scale.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1100 | 0.0400 | 0.2500 |
| conversion | 0.6100 | 0.3500 | 0.8200 |
| safety_risk | 0.1200 | 0.0700 | 0.2000 |
| score | 0.3120 | 0.1700 | 0.4300 |
| selectivity | 0.8200 | 0.6800 | 0.9100 |
| yield | 0.5000 | 0.3000 | 0.6700 |

### Q02

The long 410 K exposure should overcome the low catalyst loading and nearly exhaust reactant, but the campaign's time series implies substantial late byproduct formation and target loss.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6300 | 0.3800 | 0.8400 |
| conversion | 0.9900 | 0.9300 | 1.0000 |
| safety_risk | 0.2000 | 0.1200 | 0.3200 |
| score | 0.1390 | 0.0000 | 0.3000 |
| selectivity | 0.3600 | 0.1500 | 0.5800 |
| yield | 0.3500 | 0.1200 | 0.5800 |

### Q03

High Catalyst B loading at 410 K should produce rapid, nearly complete conversion within 1800 s. Short exposure should preserve more target than the long-duration cases, although Catalyst B's observed side-reaction tendency lowers selectivity.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2900 | 0.1500 | 0.4900 |
| conversion | 0.9800 | 0.8400 | 1.0000 |
| safety_risk | 0.1900 | 0.1100 | 0.2900 |
| score | 0.3640 | 0.2000 | 0.4800 |
| selectivity | 0.7000 | 0.5100 | 0.8200 |
| yield | 0.6900 | 0.4900 | 0.8200 |

### Q04

This combines high Catalyst B loading with the longest 410 K exposure. Conversion should saturate, while accumulated competing conversion and degradation make yield and selectivity highly uncertain and probably poor.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8100 | 0.5600 | 0.9500 |
| conversion | 0.9950 | 0.9700 | 1.0000 |
| safety_risk | 0.2900 | 0.1700 | 0.4400 |
| score | 0.0100 | 0.0000 | 0.1700 |
| selectivity | 0.1800 | 0.0400 | 0.4200 |
| yield | 0.1700 | 0.0300 | 0.4200 |

### Q05

At 350 K, low catalyst loading should give slower but relatively selective conversion. The 7200 s duration should raise conversion substantially without the severe thermal damage expected at 410–465 K.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1800 | 0.0700 | 0.3500 |
| conversion | 0.8000 | 0.5500 | 0.9400 |
| safety_risk | 0.1000 | 0.0600 | 0.1700 |
| score | 0.3760 | 0.2300 | 0.4900 |
| selectivity | 0.7700 | 0.6100 | 0.8800 |
| yield | 0.6200 | 0.4200 | 0.7600 |

### Q06

Even at low catalyst loading, 465 K for 7200 s should drive near-complete conversion. This is a strong extrapolation beyond the campaign and is expected to produce extensive byproduct formation, target damage, and elevated risk.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6700 | 0.4200 | 0.9100 |
| conversion | 0.9950 | 0.9200 | 1.0000 |
| safety_risk | 0.3100 | 0.1800 | 0.4800 |
| score | 0.0640 | 0.0000 | 0.2400 |
| selectivity | 0.3200 | 0.0900 | 0.5600 |
| yield | 0.3100 | 0.0800 | 0.5500 |

### Q07

High loading should make conversion nearly complete even at 350 K. The long exposure is expected to erode selectivity, though less severely than the corresponding high-temperature cases.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4400 | 0.2500 | 0.6900 |
| conversion | 0.9950 | 0.9200 | 1.0000 |
| safety_risk | 0.1400 | 0.0800 | 0.2300 |
| score | 0.2940 | 0.1200 | 0.4300 |
| selectivity | 0.5500 | 0.3100 | 0.7300 |
| yield | 0.5500 | 0.3000 | 0.7200 |

### Q08

High Catalyst B loading, 465 K, and 7200 s form the most severe condition. I expect saturated conversion but extensive diversion or destruction of target, with a substantial chance of exceeding the declared safety limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8700 | 0.6400 | 0.9800 |
| conversion | 0.9980 | 0.9700 | 1.0000 |
| safety_risk | 0.4400 | 0.2600 | 0.6500 |
| score | 0.0000 | 0.0000 | 0.1200 |
| selectivity | 0.1200 | 0.0200 | 0.3500 |
| yield | 0.1100 | 0.0100 | 0.3400 |

### Q09

The intermediate loading at 410 K for 7200 s should produce nearly complete conversion but substantial late-stage selectivity loss. This is outside the observed Catalyst B time range, so the yield interval is broad.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6000 | 0.3700 | 0.8200 |
| conversion | 0.9950 | 0.9500 | 1.0000 |
| safety_risk | 0.2400 | 0.1400 | 0.3700 |
| score | 0.1410 | 0.0000 | 0.3000 |
| selectivity | 0.3900 | 0.1700 | 0.6100 |
| yield | 0.3800 | 0.1600 | 0.6000 |

### Q10

Because quench occurs only after the full 7200 s heat period, I predict only a modest improvement relative to Q09, mainly through limiting post-heating exposure and slightly reducing risk. The campaign did not establish a large quench effect.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5800 | 0.3400 | 0.8100 |
| conversion | 0.9950 | 0.9500 | 1.0000 |
| safety_risk | 0.2200 | 0.1200 | 0.3500 |
| score | 0.1630 | 0.0100 | 0.3300 |
| selectivity | 0.4100 | 0.1800 | 0.6400 |
| yield | 0.4000 | 0.1700 | 0.6300 |

### Q11

Four hours at 350 K should allow intermediate Catalyst B loading to approach complete conversion. Lower temperature should restrain damage relative to Q02, but the very long duration is still expected to reduce selectivity materially.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5500 | 0.3300 | 0.7800 |
| conversion | 0.9950 | 0.9400 | 1.0000 |
| safety_risk | 0.1500 | 0.0900 | 0.2500 |
| score | 0.2210 | 0.0500 | 0.3700 |
| selectivity | 0.4500 | 0.2100 | 0.6600 |
| yield | 0.4400 | 0.2000 | 0.6400 |

### Q12

At 465 K, intermediate loading should achieve nearly complete conversion within 1800 s. The short exposure should preserve appreciable target, but high temperature creates considerable uncertainty in selectivity, degradation, and risk.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3400 | 0.1800 | 0.5800 |
| conversion | 0.9900 | 0.8800 | 1.0000 |
| safety_risk | 0.3000 | 0.1700 | 0.4600 |
| score | 0.2890 | 0.1000 | 0.4500 |
| selectivity | 0.6600 | 0.4200 | 0.8100 |
| yield | 0.6500 | 0.4000 | 0.8000 |

## K2 — Retrospective analysis

1. Initial claims: supported, contradicted, or untested

The initial material packet contained almost no substantive, task-specific chemical claims. It supplied anonymous catalyst labels, real solvent names coupled to categorical benchmark effects, operating bounds, instrument contracts, and the instruction that experimental evidence was authoritative. It did not supply a kinetic law, activation energy, catalyst ranking, solvent ranking, deactivation model, or expected optimum. Therefore, there was no initial chemical mechanism that could properly be called confirmed or refuted.

The statement that catalyst identity represented a latent categorical activity profile was consistent with batches 1–4. Under the same acetonitrile/370 K/3600 s program, Catalyst B gave conversion 0.9408 and degradation warning 0.2333, whereas Catalyst D gave conversion 0.7598 and degradation warning 0.0940. This supports the practical importance of catalyst identity, but it does not independently prove how the latent profile is implemented.

The warning that named solvents should be treated as categorical benchmark effects rather than as predictions from ordinary solvent properties remained appropriate. Batches 4–7 showed large solvent-dependent changes, especially the contrast between acetonitrile and toluene, but those observations cannot validate a real physical-property explanation. No counterevidence to the benchmark interpretation was found; that is weaker than proving it.

The declared safety limit of 0.35 was not violated by any completed campaign batch. This supports only the statement that the tested conditions stayed inside the constraint. It does not validate safety at the blind-query extremes, particularly Q08, for which I predicted risk 0.44 with an 80% interval of 0.26–0.65.

A simple irreversible R→P account did encounter clear counterevidence. In the Catalyst D/acetonitrile time series, conversion rose from 0.5005 in batch 10 to 0.7598 in batch 4 and 0.9468 in batch 11, while selectivity fell from 0.8286 to 0.7582 and 0.6341. Yield rose and then slightly declined. K1 responded to this evidence by introducing parallel byproduct formation and consecutive target loss. Thus this was counterevidence that produced a revision, not counterevidence that was ignored.

I do not identify a comparably direct contradiction that K1 recognized but deliberately left unrevised. The larger problem was underdetermination: K1 retained catalyst deactivation, equilibrium, transport, and thermal-lag possibilities without evidence sufficient to choose among them. Those were explicitly labeled as unresolved rather than silently treated as established.

2. Experiments that actually formed or changed the account

Batch 1 was a guessed central condition. Acetonitrile, Catalyst A, 370 K, 3600 s, 600 rpm, and maximum permitted charges were selected before relevant performance data existed. The initial packet supplied legal ranges but did not justify this particular center point.

Batches 2–4 genuinely changed the catalyst interpretation. Catalyst B was the activity leader and gave the campaign’s highest observed yield, 0.6308, but also much greater byproduct and degradation. Catalyst D gave a better selectivity/damage balance. This caused me to reject a model in which catalyst identity merely multiplies one universal rate constant. K1 instead assigned catalyst-specific productive, competing, and possibly deactivation constants.

Batches 5–7 formed the solvent account. Water gave conversion 0.5556, selectivity 0.7890, and degradation 0.0211; acetonitrile with Catalyst D gave substantially higher yield; toluene gave conversion 0.6991 but selectivity only 0.5961 and byproduct 0.2894. These results supported solvent-dependent branching rather than a uniform solvent acceleration factor.

Batches 8–11 produced the strongest kinetic evidence. In particular, batches 10, 4, and 11 revealed a yield maximum at intermediate exposure and showed that conversion could continue increasing while selectivity deteriorated. Batch 9 versus batch 10 showed that increasing nominal temperature from 370 to 400 K at 1800 s increased conversion and yield but also degradation and risk. Those observations motivated K1’s exposure-dependent network and its statement that “time and temperature must be treated jointly.”

Batch 12 was more influential for the operating recommendation than for mechanism discrimination. Relative to nominally matched batch 4, the quenched batch had slightly lower degradation and risk but also slightly lower yield. K1 therefore treated quenching as a modest, uncertain benefit rather than a major mechanistic intervention.

Several key choices remained only partly evidence-based. Continuing with Catalyst D after batch 4 used existing data and enabled a coherent local time/temperature study. In contrast, fixing catalyst amount, reagent amount, solvent volume, and stirring at one level was a convenience rather than an evidence-based conclusion. The later blind predictions then had to extrapolate precisely across those untested dimensions. The Q rationale’s “saturating conversion model with catalyst-loading and temperature-dependent exposure” was a modeling assumption, not a relationship measured in the campaign.

3. Most important competing explanations

K1’s leading phenomenological model was R→P and R→B in parallel, with P→D as a consecutive loss and a possible time-dependent catalyst activity a(t). The principal competitors are:

• Pure parallel branching with time- or temperature-dependent selectivity, without appreciable destruction of P.
• Consecutive target loss after formation, as represented by P→D.
• Catalyst activation or deactivation that changes both rate and branching over time.
• Reversible target formation or an approach to equilibrium, followed by irreversible side chemistry.
• Thermal or transport limitation, where heat-up, mixing, or phase behavior creates the apparent kinetics.

The campaign distinguishes all of these from a single irreversible R→P pathway. It also distinguishes solvent-dependent branching from a model in which solvent only applies one common rate multiplier: toluene’s substantial conversion and poor target allocation are difficult to explain with a universal multiplier.

The campaign cannot reliably separate direct R→B formation from P→D loss. Batch 11’s high conversion, lower selectivity, large byproduct signal, and degradation warning are compatible with both. Because measurements came from different vessels at different endpoints, the data do not directly show P forming and then disappearing in one vessel.

Likewise, catalyst deactivation cannot be separated from equilibrium or transport limitation. No catalyst-loading series, stirring series, or same-vessel kinetic trajectory was obtained. Solvent effects could act through elementary branching, catalyst speciation, deactivation, phase behavior, or heat transfer. Catalyst and solvent interaction was also not mapped because the solvent screen used only Catalyst D.

The blind-query conditions increase these ambiguities. For example, Q01 and Q03 differ in Catalyst B amount at otherwise identical conditions, but the campaign did not establish whether rates scale with catalyst concentration, catalyst-to-reagent ratio, or neither. My Q predictions assumed a strong loading response; that assumption was necessary for numerical prediction but remains unverified.

4. The single additional complete experiment I would choose

I would run 0.040 mol reagent, 0.080 L acetonitrile, and 0.005 mol Catalyst B at 600 rpm. I would heat to nominally 370 K for 1800 s, take an HPLC measurement, continue heating the same vessel for another 5400 s, quench, terminate, and obtain the required final assay.

This condition brackets the only Catalyst B result, batch 2 at 3600 s, while producing a same-vessel trajectory from 1800 to 7200 s. I would retain conversion, yield, selectivity, and byproduct at 1800 s; the final assay would add degradation warning. Actual thermal changes would also be retained.

Different outcomes would alter the account as follows:

• Rising conversion accompanied by a rise and then fall in yield, plus increasing degradation, would support consecutive target loss.
• Rising conversion and yield with a declining yield/conversion ratio and increasing byproduct would favor changing parallel branching without requiring substantial P destruction.
• Little change after 1800 s would favor deactivation, equilibrium, or transport limitation.
• Stalled conversion combined with falling yield and rising degradation would favor productive catalyst deactivation plus continuing nonproductive target decay.
• Large disagreement with batch 2 at the intermediate time would show that process variability is larger than assumed and would force wider prediction intervals throughout.

This experiment would not identify a molecular catalyst state, but it would address the most consequential ambiguity using the catalyst that dominates the blind queries.

5. Tradeoff between identifiability and operating score

The design spent meaningful resources on mechanism identification. The four-catalyst comparison, four-solvent comparison, time series, temperature contrasts, and quench comparison were more informative than repeatedly exploiting the first high-scoring condition. Batch 11, for example, was not selected to maximize score; its long exposure revealed the conversion/selectivity tradeoff and the onset of severe degradation.

There was nevertheless an optimization-driven concentration of effort. After batch 4, Catalyst D and acetonitrile became the main platform. This made the local time/temperature comparisons coherent and led to a balanced recommendation, but it left Catalyst B with only one observed time point. That omission was costly because all twelve blind queries used Catalyst B.

Conversely, some identifiability was sacrificed for operational comparability. Every campaign batch used maximum permitted charges and 600 rpm. This reduced nuisance variation but prevented estimation of catalyst order, concentration effects, or mixing dependence. The blind cases used a much smaller volume, 0.003 mol reagent, variable catalyst amounts, and 400 rpm, so the extrapolation burden was large.

Batch 12 was mainly an operating refinement. It tested a quench near the preferred Catalyst D condition and became the sealed recommendation. A replicate or Catalyst B time point would probably have contributed more to mechanism identifiability. Thus the final batch sacrificed some mechanistic information for a potentially safer operating recommendation.

If score maximization alone had governed the campaign, batch 2 should have been replicated and locally optimized because it had the highest observed score, approximately 0.3187. If identifiability alone had governed it, I would have added replicates, a Catalyst B time series, and catalyst-loading variation. The actual design occupied a middle ground.

6. Underused evidence and weaknesses in the blind predictions

The raw characterization artifacts were not fully exploited. Reasoning relied mostly on processed estimates and compact peak lists. Spectral baselines, channel disagreements, calibration flags, missingness, and mass-balance fields might have revealed measurement limitations even if they could not resolve the mechanism.

Near-endpoint HPLC/final-assay pairs were also underused as an empirical source of uncertainty. In batch 8, HPLC estimated conversion 0.8377 and selectivity 0.6949, whereas the final assay gave 0.8277 and 0.6597. Systematically analyzing such discrepancies could have supported a more defensible process-plus-instrument uncertainty model.

Thermal evidence was difficult to use. Recorded temperature changes demonstrated finite thermal lag, but complete T(t) trajectories were unavailable. K1 therefore introduced the exposure integral Θi=∫exp[-Ei/(RT(t))]dt conceptually but could not estimate it. The Q predictions nevertheless used an approximate temperature-dependent exposure model; that was an extrapolative convenience rather than a fitted law.

The public campaign scores were informative enough to reconstruct the empirical scoring relationship used in Q: score ≈ max(0, −0.10 + 0.40·yield + 0.25·selectivity + 0.10·conversion − 0.45·risk). Once the component predictions are accepted, score is therefore less structurally independent. Its uncertainty remains strongly correlated with the component uncertainties, something the marginal intervals do not fully express.

The least reliable blind predictions are Q04, Q06, and Q08. Q04 combines high Catalyst B loading with 14400 s at 410 K. Q06 uses 465 K for 7200 s, and Q08 combines that severe thermal program with high loading. The point predictions—Q04 yield 0.17, Q06 yield 0.31, and Q08 yield 0.11—depend heavily on unvalidated assumptions about late target destruction. Their qualitative direction is defensible, but their numerical placement is weak.

Q02 and Q11 are also uncertain because 14400 s is twice the longest campaign duration. Q01 and Q03 probe loading at 410 K, while catalyst-loading dependence was never measured. Q09 and Q10 depend on a quench effect inferred from only batches 4 and 12; their small predicted differences, such as yields 0.38 versus 0.40, should not be interpreted as resolved.

Several conversion intervals may be too narrow. I assigned Q04 0.995 with an interval of 0.97–1.00, Q08 0.998 with 0.97–1.00, and Q09/Q10 0.995 with 0.95–1.00. Those intervals express saturation under the assumed exposure model but inadequately cover strong deactivation, equilibrium, scale-dependent heat transfer, or transport limitation. The corresponding risk intervals may also underrepresent uncertainty in how absolute amount and small volume enter the public risk calculation.

This weakness is directly connected to K1’s stated limits. K1 said that catalyst-loading, reagent-loading, volume, and stirring effects were unidentified and that “local directional predictions are more defensible than exact numerical predictions.” The blind set deliberately probes those omitted dimensions. The wide yield and selectivity intervals acknowledge part of the problem, but the near-unity conversion predictions are more confident than K1’s applicability statement warrants. This is a prospective self-critique made without access to prediction truth, not a post hoc adjustment.

7. Limitations of the sealed recommendation

Batch 12 was not the sample’s highest observed result. Batch 2 had the highest observed yield, 0.6308, and the highest score, approximately 0.3187. Batch 12 gave yield 0.5734 and score approximately 0.3156. It was selected because it combined selectivity 0.7616, degradation warning 0.0846, and risk 0.1849 more favorably than the high-activity Catalyst B condition.

The recommendation is therefore a balanced preference within the sampled set, not proof of an optimum. It is based on one vessel. The comparison with unquenched batch 4 was not a clean replicated estimate: batch 12 had slightly lower yield, slightly higher conversion and byproduct, and only modestly lower degradation and risk. Random process and assay variation could account for part of the apparent advantage.

Repeatability should be assessed with multiple independent replicates of batch 12 interleaved with replicates of batch 4. That would estimate both ordinary run variance and the quench effect without time-order confounding.

Local robustness should be tested with neighboring temperatures, durations, and Catalyst D loadings rather than a single nominal point. A compact response-surface design around 370 K and 3600 s, with actual thermal histories recorded, would show whether batch 12 lies on a broad plateau or a narrow ridge. Modest variation in stirring and concentration would test sensitivity to transport and scale.

Cross-material transfer requires repeating the local design with other catalysts and solvents. Current evidence does not justify assuming that Catalyst D’s balance transfers to Catalyst B or that acetonitrile remains preferred under a different catalyst. Cross-world transfer is still less defensible: catalyst identities are anonymous and solvent effects were explicitly described as world-specific categorical benchmark couplings.

Accordingly, batch 12 should be described as a promising, safety-balanced member of the sampled design. It has not been shown to be repeatable, locally optimal, globally optimal, material-general, or world-general.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 95.5 | none | 0 |
| Q | yes | 0 | 114.4 | none | 0 |
| K2 | yes | 0 | 85.9 | none | 0 |

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean 80% width | Mean interval score |
|---|---:|---:|---:|---:|
| byproduct_signal | 0.1268 | 0.7000 | 0.3933 | 0.5151 |
| conversion | 0.0143 | 1.0000 | 0.1325 | 0.1325 |
| safety_risk | 0.0569 | 0.9167 | 0.2200 | 0.2631 |
| score | 0.0391 | 1.0000 | 0.2692 | 0.2692 |
| selectivity | 0.1180 | 0.8167 | 0.3817 | 0.5088 |
| yield | 0.1061 | 0.9167 | 0.4042 | 0.4299 |

## Predictions versus released reference truth

### Q01

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1100 | 0.0400 | 0.2500 | 0.1848 | 0.1918, 0.1819, 0.1704, 0.1891, 0.1908 |
| conversion | 0.6100 | 0.3500 | 0.8200 | 0.7137 | 0.7023, 0.7224, 0.7188, 0.7145, 0.7107 |
| safety_risk | 0.1200 | 0.0700 | 0.2000 | 0.2518 | 0.2518, 0.2518, 0.2518, 0.2518, 0.2518 |
| score | 0.3120 | 0.1700 | 0.4300 | 0.3274 | 0.3246, 0.3325, 0.3231, 0.3272, 0.3293 |
| selectivity | 0.8200 | 0.6800 | 0.9100 | 0.7446 | 0.7346, 0.7507, 0.7388, 0.7478, 0.7514 |
| yield | 0.5000 | 0.3000 | 0.6700 | 0.5270 | 0.5292, 0.5340, 0.5188, 0.5246, 0.5285 |
### Q02

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.6300 | 0.3800 | 0.8400 | 0.9165 | 0.9241, 0.9159, 0.9222, 0.9177, 0.9027 |
| conversion | 0.9900 | 0.9300 | 1.0000 | 0.9982 | 1.0000, 1.0000, 1.0000, 1.0000, 0.9911 |
| safety_risk | 0.2000 | 0.1200 | 0.3200 | 0.2522 | 0.2522, 0.2522, 0.2522, 0.2522, 0.2522 |
| score | 0.1390 | 0.0000 | 0.3000 | 0.0065 | 0.0068, 0.0060, 0.0124, 0.0037, 0.0034 |
| selectivity | 0.3600 | 0.1500 | 0.5800 | 0.0907 | 0.0810, 0.0943, 0.1061, 0.0782, 0.0938 |
| yield | 0.3500 | 0.1200 | 0.5800 | 0.0891 | 0.0956, 0.0852, 0.0939, 0.0896, 0.0814 |
### Q03

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2900 | 0.1500 | 0.4900 | 0.2439 | 0.2551, 0.2405, 0.2456, 0.2377, 0.2404 |
| conversion | 0.9800 | 0.8400 | 1.0000 | 0.9840 | 0.9910, 0.9798, 0.9883, 0.9778, 0.9833 |
| safety_risk | 0.1900 | 0.1100 | 0.2900 | 0.2538 | 0.2538, 0.2538, 0.2538, 0.2538, 0.2538 |
| score | 0.3640 | 0.2000 | 0.4800 | 0.4127 | 0.4149, 0.4118, 0.4145, 0.4127, 0.4096 |
| selectivity | 0.7000 | 0.5100 | 0.8200 | 0.7564 | 0.7525, 0.7577, 0.7556, 0.7640, 0.7520 |
| yield | 0.6900 | 0.4900 | 0.8200 | 0.7398 | 0.7460, 0.7376, 0.7438, 0.7366, 0.7348 |
### Q04

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.8100 | 0.5600 | 0.9500 | 0.9599 | 0.9591, 0.9620, 0.9651, 0.9593, 0.9539 |
| conversion | 0.9950 | 0.9700 | 1.0000 | 0.9956 | 1.0000, 0.9911, 1.0000, 0.9919, 0.9949 |
| safety_risk | 0.2900 | 0.1700 | 0.4400 | 0.2525 | 0.2525, 0.2525, 0.2525, 0.2525, 0.2525 |
| score | 0.0100 | 0.0000 | 0.1700 | 0.0000 | 0.0000, 0.0000, 0.0000, 0.0000, 0.0000 |
| selectivity | 0.1800 | 0.0400 | 0.4200 | 0.0756 | 0.0716, 0.0733, 0.0668, 0.0853, 0.0810 |
| yield | 0.1700 | 0.0300 | 0.4200 | 0.0734 | 0.0697, 0.0765, 0.0699, 0.0811, 0.0700 |
### Q05

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1800 | 0.0700 | 0.3500 | 0.4087 | 0.4217, 0.4103, 0.4022, 0.3956, 0.4138 |
| conversion | 0.8000 | 0.5500 | 0.9400 | 0.8430 | 0.8392, 0.8436, 0.8392, 0.8386, 0.8545 |
| safety_risk | 0.1000 | 0.0600 | 0.1700 | 0.1426 | 0.1426, 0.1426, 0.1426, 0.1426, 0.1426 |
| score | 0.3760 | 0.2300 | 0.4900 | 0.2913 | 0.2939, 0.2886, 0.2971, 0.2898, 0.2871 |
| selectivity | 0.7700 | 0.6100 | 0.8800 | 0.5173 | 0.5216, 0.5049, 0.5338, 0.5106, 0.5157 |
| yield | 0.6200 | 0.4200 | 0.7600 | 0.4350 | 0.4399, 0.4358, 0.4401, 0.4365, 0.4227 |
### Q06

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.6700 | 0.4200 | 0.9100 | 0.8233 | 0.8278, 0.8247, 0.8136, 0.8315, 0.8191 |
| conversion | 0.9950 | 0.9200 | 1.0000 | 0.9952 | 0.9988, 0.9901, 0.9926, 0.9947, 1.0000 |
| safety_risk | 0.3100 | 0.1800 | 0.4800 | 0.4261 | 0.4261, 0.4261, 0.4261, 0.4261, 0.4261 |
| score | 0.0640 | 0.0000 | 0.2400 | 0.0000 | 0.0000, 0.0000, 0.0000, 0.0000, 0.0000 |
| selectivity | 0.3200 | 0.0900 | 0.5600 | 0.1871 | 0.1941, 0.1683, 0.1953, 0.1894, 0.1884 |
| yield | 0.3100 | 0.0800 | 0.5500 | 0.1849 | 0.1885, 0.1877, 0.1865, 0.1781, 0.1839 |
### Q07

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4400 | 0.2500 | 0.6900 | 0.5161 | 0.5192, 0.5183, 0.5198, 0.5114, 0.5117 |
| conversion | 0.9950 | 0.9200 | 1.0000 | 0.9945 | 0.9933, 1.0000, 0.9913, 0.9970, 0.9911 |
| safety_risk | 0.1400 | 0.0800 | 0.2300 | 0.1438 | 0.1438, 0.1438, 0.1438, 0.1438, 0.1438 |
| score | 0.2940 | 0.1200 | 0.4300 | 0.2970 | 0.2948, 0.2939, 0.2935, 0.3014, 0.3012 |
| selectivity | 0.5500 | 0.3100 | 0.7300 | 0.4950 | 0.4950, 0.4901, 0.4932, 0.4948, 0.5021 |
| yield | 0.5500 | 0.3000 | 0.7200 | 0.4986 | 0.4935, 0.4928, 0.4919, 0.5092, 0.5058 |
### Q08

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.8700 | 0.6400 | 0.9800 | 0.8563 | 0.8570, 0.8322, 0.8629, 0.8565, 0.8729 |
| conversion | 0.9980 | 0.9700 | 1.0000 | 0.9973 | 1.0000, 0.9919, 1.0000, 1.0000, 0.9945 |
| safety_risk | 0.4400 | 0.2600 | 0.6500 | 0.4263 | 0.4263, 0.4263, 0.4263, 0.4263, 0.4263 |
| score | 0.0000 | 0.0000 | 0.1200 | 0.0000 | 0.0000, 0.0000, 0.0000, 0.0000, 0.0000 |
| selectivity | 0.1200 | 0.0200 | 0.3500 | 0.1701 | 0.1633, 0.1704, 0.1715, 0.1742, 0.1709 |
| yield | 0.1100 | 0.0100 | 0.3400 | 0.1738 | 0.1784, 0.1766, 0.1728, 0.1716, 0.1699 |
### Q09

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.6000 | 0.3700 | 0.8200 | 0.7196 | 0.7083, 0.7133, 0.7299, 0.7153, 0.7310 |
| conversion | 0.9950 | 0.9500 | 1.0000 | 0.9933 | 1.0000, 0.9804, 1.0000, 0.9986, 0.9875 |
| safety_risk | 0.2400 | 0.1400 | 0.3700 | 0.2529 | 0.2529, 0.2529, 0.2529, 0.2529, 0.2529 |
| score | 0.1410 | 0.0000 | 0.3000 | 0.1314 | 0.1360, 0.1316, 0.1277, 0.1341, 0.1277 |
| selectivity | 0.3900 | 0.1700 | 0.6100 | 0.3006 | 0.3108, 0.3002, 0.2918, 0.3038, 0.2963 |
| yield | 0.3800 | 0.1600 | 0.6000 | 0.2924 | 0.2957, 0.2963, 0.2868, 0.2958, 0.2873 |
### Q10

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5800 | 0.3400 | 0.8100 | 0.7130 | 0.7267, 0.7023, 0.7206, 0.7129, 0.7025 |
| conversion | 0.9950 | 0.9500 | 1.0000 | 0.9922 | 1.0000, 0.9941, 0.9958, 0.9831, 0.9878 |
| safety_risk | 0.2200 | 0.1200 | 0.3500 | 0.1456 | 0.1456, 0.1456, 0.1456, 0.1456, 0.1456 |
| score | 0.1630 | 0.0100 | 0.3300 | 0.1737 | 0.1786, 0.1673, 0.1736, 0.1726, 0.1762 |
| selectivity | 0.4100 | 0.1800 | 0.6400 | 0.2959 | 0.3124, 0.2771, 0.2873, 0.3050, 0.2977 |
| yield | 0.4000 | 0.1700 | 0.6300 | 0.2889 | 0.2891, 0.2842, 0.2933, 0.2828, 0.2953 |
### Q11

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5500 | 0.3300 | 0.7800 | 0.7775 | 0.7826, 0.7700, 0.7824, 0.7723, 0.7800 |
| conversion | 0.9950 | 0.9400 | 1.0000 | 0.9975 | 1.0000, 1.0000, 1.0000, 1.0000, 0.9875 |
| safety_risk | 0.1500 | 0.0900 | 0.2500 | 0.1432 | 0.1432, 0.1432, 0.1432, 0.1432, 0.1432 |
| score | 0.2210 | 0.0500 | 0.3700 | 0.1414 | 0.1452, 0.1394, 0.1458, 0.1449, 0.1317 |
| selectivity | 0.4500 | 0.2100 | 0.6600 | 0.2451 | 0.2573, 0.2426, 0.2622, 0.2561, 0.2075 |
| yield | 0.4400 | 0.2000 | 0.6400 | 0.2426 | 0.2439, 0.2387, 0.2423, 0.2439, 0.2444 |
### Q12

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3400 | 0.1800 | 0.5800 | 0.3277 | 0.3364, 0.3157, 0.3327, 0.3236, 0.3300 |
| conversion | 0.9900 | 0.8800 | 1.0000 | 0.9933 | 0.9929, 0.9900, 1.0000, 0.9984, 0.9854 |
| safety_risk | 0.3000 | 0.1700 | 0.4600 | 0.4273 | 0.4273, 0.4273, 0.4273, 0.4273, 0.4273 |
| score | 0.2890 | 0.1000 | 0.4500 | 0.3000 | 0.3025, 0.2997, 0.3014, 0.2990, 0.2971 |
| selectivity | 0.6600 | 0.4200 | 0.8100 | 0.6713 | 0.6755, 0.6797, 0.6646, 0.6644, 0.6722 |
| yield | 0.6500 | 0.4000 | 0.8000 | 0.6671 | 0.6710, 0.6621, 0.6732, 0.6677, 0.6612 |

## Recommendation retest

- Selected source batch: `12`
- Retest exact replay verified: `True`
- Retest failure: `none`

| Metric | Selected source batch | Independent retest | Retest minus source |
|---|---:|---:|---:|
| byproduct_signal | 0.2032 | 0.1873 | -0.0160 |
| conversion | 0.7905 | 0.7598 | -0.0308 |
| cost | 1.0000 | 1.0000 | 0.0000 |
| degradation_warning | 0.0846 | 0.0990 | 0.0144 |
| safety_risk | 0.1849 | 0.1849 | 0.0000 |
| score | 0.3156 | 0.3166 | 0.0009 |
| selectivity | 0.7616 | 0.7467 | -0.0149 |
| virtual_spectrum_summary | 0.1499 | 0.1475 | -0.0023 |
| yield | 0.5734 | 0.5928 | 0.0194 |

## Scope note

This is the final sanitized report produced after all 60 source sessions and K1/Q/K2 chains were sealed. It includes released reference truth, blind-prediction evaluation, and the independent recommendation retest. Provider-private event streams, credentials, thread identifiers, and token accounting remain excluded.
