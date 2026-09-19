# RX-W04--P--safety_constrained_optimization--Opaque

## Run summary

- World: `RX-W04`
- Locus: `P`
- Goal: `safety_constrained_optimization`
- Arm: `Opaque`
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

- Selected batch: `8`
- Rationale: Batch 8 achieved the highest observed final public score (about 0.352) while its safety risk (about 0.227) remained comfortably below the 0.35 limit; it used Catalyst B in toluene with a 370 K boundary target for 3600 s.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S0 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.2403 | 0.6320 | 0.3980 | 0.1385 | 0.0293 | 0.1099 | 0.1445 |
| 2 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.4162 | 0.7805 | 0.5454 | 0.1163 | 0.0376 | 0.1273 | 0.2589 |
| 3 | S0 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.2425 | 0.5650 | 0.4187 | 0.1869 | 0.0214 | 0.1089 | 0.1311 |
| 4 | S0 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.3021 | 0.7071 | 0.3987 | 0.1223 | 0.0284 | 0.1134 | 0.1865 |
| 5 | S1 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.3874 | 0.6378 | 0.6104 | 0.2219 | 0.0406 | 0.1513 | 0.2073 |
| 6 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.5964 | 0.6996 | 0.8196 | 0.2413 | 0.1163 | 0.1923 | 0.3089 |
| 7 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K x 3600 s @ 600 rpm | no | 0.6177 | 0.7443 | 0.8265 | 0.2181 | 0.0678 | 0.2064 | 0.3229 |
| 8 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 370 K x 3600 s @ 600 rpm | no | 0.6910 | 0.7365 | 0.9376 | 0.2440 | 0.1105 | 0.2273 | 0.3520 |
| 9 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 390 K x 3600 s @ 600 rpm | no | 0.6968 | 0.7108 | 0.9493 | 0.2780 | 0.1554 | 0.2697 | 0.3300 |
| 10 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 370 K x 2400 s @ 600 rpm | no | 0.6282 | 0.7991 | 0.7906 | 0.1730 | 0.0629 | 0.2183 | 0.3319 |
| 11 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 360 K x 3600 s @ 600 rpm | no | 0.6477 | 0.7527 | 0.8782 | 0.2272 | 0.1005 | 0.2157 | 0.3380 |
| 12 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 370 K x 4200 s @ 600 rpm | no | 0.6768 | 0.7232 | 0.9580 | 0.2794 | 0.1574 | 0.2292 | 0.3442 |

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
      "solvent": 0,
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
    "byproduct_signal": 0.13850565254688263,
    "conversion": 0.39803728461265564,
    "cost": 1.0,
    "degradation_warning": 0.029343586415052414,
    "safety_risk": 0.10985220968723297,
    "score": 0.1444782167673111,
    "selectivity": 0.6319801807403564,
    "virtual_spectrum_summary": 0.08938272297382355,
    "yield": 0.2402823567390442
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
      "solvent": 0,
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
    "byproduct_signal": 0.11630663275718689,
    "conversion": 0.5453777313232422,
    "cost": 1.0,
    "degradation_warning": 0.0376095212996006,
    "safety_risk": 0.12729288637638092,
    "score": 0.2588609755039215,
    "selectivity": 0.7805403470993042,
    "virtual_spectrum_summary": 0.08089293539524078,
    "yield": 0.4161747992038727
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
      "solvent": 0,
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
    "byproduct_signal": 0.18689747154712677,
    "conversion": 0.41873088479042053,
    "cost": 1.0,
    "degradation_warning": 0.02143062837421894,
    "safety_risk": 0.10889402776956558,
    "score": 0.13111503422260284,
    "selectivity": 0.5649710893630981,
    "virtual_spectrum_summary": 0.11243738979101181,
    "yield": 0.24250373244285583
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
    "byproduct_signal": 0.12227748334407806,
    "conversion": 0.3987159729003906,
    "cost": 1.0,
    "degradation_warning": 0.028435084968805313,
    "safety_risk": 0.1134122759103775,
    "score": 0.1864556223154068,
    "selectivity": 0.7071050405502319,
    "virtual_spectrum_summary": 0.08004840463399887,
    "yield": 0.3021082282066345
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
      "solvent": 1,
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
    "byproduct_signal": 0.22186976671218872,
    "conversion": 0.6103553771972656,
    "cost": 1.0,
    "degradation_warning": 0.04055459052324295,
    "safety_risk": 0.15130333602428436,
    "score": 0.20734132826328278,
    "selectivity": 0.6377987265586853,
    "virtual_spectrum_summary": 0.1402779370546341,
    "yield": 0.38735654950141907
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
    "byproduct_signal": 0.2412506341934204,
    "conversion": 0.8195526003837585,
    "cost": 1.0,
    "degradation_warning": 0.11628655344247818,
    "safety_risk": 0.1923234462738037,
    "score": 0.30885082483291626,
    "selectivity": 0.6995801329612732,
    "virtual_spectrum_summary": 0.18501679599285126,
    "yield": 0.596365213394165
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
    "byproduct_signal": 0.21810275316238403,
    "conversion": 0.826457679271698,
    "cost": 1.0,
    "degradation_warning": 0.06783322989940643,
    "safety_risk": 0.20643991231918335,
    "score": 0.3229203522205353,
    "selectivity": 0.7443211078643799,
    "virtual_spectrum_summary": 0.1504814624786377,
    "yield": 0.6177306771278381
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
      "solvent": 3,
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
  "end_step": 56,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.24396196007728577,
    "conversion": 0.9376100897789001,
    "cost": 1.0,
    "degradation_warning": 0.11046935617923737,
    "safety_risk": 0.22733795642852783,
    "score": 0.35196933150291443,
    "selectivity": 0.7364510297775269,
    "virtual_spectrum_summary": 0.18389029800891876,
    "yield": 0.690994143486023
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
      "solvent": 3,
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
  "end_step": 63,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.2780230939388275,
    "conversion": 0.9492939114570618,
    "cost": 1.0,
    "degradation_warning": 0.15543706715106964,
    "safety_risk": 0.2696792483329773,
    "score": 0.33001071214675903,
    "selectivity": 0.7108056545257568,
    "virtual_spectrum_summary": 0.22285938262939453,
    "yield": 0.6968389749526978
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
      "solvent": 3,
      "volume_L": 0.08
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 2400,
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
    "byproduct_signal": 0.1729632467031479,
    "conversion": 0.7905616164207458,
    "cost": 1.0,
    "degradation_warning": 0.06291275471448898,
    "safety_risk": 0.2183157354593277,
    "score": 0.331874817609787,
    "selectivity": 0.799106776714325,
    "virtual_spectrum_summary": 0.12344052642583847,
    "yield": 0.6282100677490234
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
      "solvent": 3,
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
    "byproduct_signal": 0.22715111076831818,
    "conversion": 0.8781745433807373,
    "cost": 1.0,
    "degradation_warning": 0.10050339251756668,
    "safety_risk": 0.21569833159446716,
    "score": 0.3380081057548523,
    "selectivity": 0.7526730298995972,
    "virtual_spectrum_summary": 0.17015963792800903,
    "yield": 0.6477165818214417
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 3,
      "volume_L": 0.08
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 4200,
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
  "end_step": 84,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.27938055992126465,
    "conversion": 0.9579775333404541,
    "cost": 1.0,
    "degradation_warning": 0.1573946475982666,
    "safety_risk": 0.22916659712791443,
    "score": 0.3442004323005676,
    "selectivity": 0.7232184410095215,
    "virtual_spectrum_summary": 0.22448690235614777,
    "yield": 0.6768076419830322
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

# Mechanistic report

## 1. Scope and evidentiary basis

I interpret this as an anonymous catalytic reaction network in which a limiting reagent is converted into a desired product while competing reactions form byproduct and, under sufficiently severe thermal conditions, degradation products. The catalyst identities are deliberately opaque, and the named solvents have benchmark categorical effects; therefore, I do not assign a real molecular mechanism or real catalyst identity.

All 12 batches used 0.040 mol reagent, 0.080 L solvent, 0.005 mol catalyst, and 600 rpm stirring. Each batch received one thermal treatment, one intermediate HPLC measurement, termination, and one final assay. Consequently, the evidence identifies effects only within that fixed composition, loading, addition order, mixing rate, and approximately 2400–4200 s thermal window. Each condition was tested only once, so differences near the stated assay noise or ordinary process variability should not be overinterpreted.

## 2. Proposed process model

A minimal model consistent with the observations is a parallel-and-consecutive network:

R -> P  (desired catalytic channel)
R -> B  (parallel undesired channel)
P -> D  (thermal or catalyst-mediated degradation)

A corresponding kinetic representation is

- dR/dt = -(kP + kB)R
- dP/dt = kP R - kD P
- dB/dt = kB R
- dD/dt = kD P

where each effective rate constant depends on catalyst, solvent, and temperature. A useful qualitative parameterization would be

k_j = A_j × f_j(catalyst) × g_j(solvent) × exp[-E_j/(RT)]

for j in {P, B, D}. These are proposed equations, not fitted laws: the campaign did not contain enough independent time points, temperatures, or concentrations to estimate their parameters uniquely.

The data suggest that increasing thermal severity initially improves the desired channel by raising conversion, but eventually increases the competing and degradation channels enough to lower selectivity and the public score. Thus, maximum conversion is not the same as maximum safe score. The observed optimum is a balance among conversion, desired-product yield, selectivity, byproduct formation, degradation, and safety risk.

## 3. Catalyst effect

Batches 1–4 screened all four catalysts in water at a 350 K target for 3600 s.

Final-assay observations were:

- Batch 1, Catalyst A: conversion 0.3980, yield 0.2403, selectivity 0.6320, byproduct 0.1385, degradation 0.0293, score 0.1445, risk 0.1099.
- Batch 2, Catalyst B: conversion 0.5454, yield 0.4162, selectivity 0.7805, byproduct 0.1163, degradation 0.0376, score 0.2589, risk 0.1273.
- Batch 3, Catalyst C: conversion 0.4187, yield 0.2425, selectivity 0.5650, byproduct 0.1869, degradation 0.0214, score 0.1311, risk 0.1089.
- Batch 4, Catalyst D: conversion 0.3987, yield 0.3021, selectivity 0.7071, byproduct 0.1223, degradation 0.0284, score 0.1865, risk 0.1134.

Catalyst B was clearly the strongest candidate under these conditions. Relative to Catalyst A, it increased both conversion and selectivity, rather than merely accelerating all channels equally. This implies that the catalyst changes the ratio kP/kB as well as the overall reaction rate. Catalyst D may also favor the desired channel moderately, while Catalyst C appears comparatively unselective.

Catalyst B caused somewhat higher observed risk in water than the other catalysts. This could reflect a catalyst-specific hazard term, stronger reaction progress or heat generation, or an interaction between catalyst activity and the safety model. Those possibilities cannot be separated from the public observations.

## 4. Solvent effect and catalyst–solvent coupling

Batches 2 and 5–7 compare solvents with Catalyst B at 350 K for 3600 s:

- Batch 2, water: conversion 0.5454, yield 0.4162, selectivity 0.7805, score 0.2589, risk 0.1273.
- Batch 5, ethanol: conversion 0.6104, yield 0.3874, selectivity 0.6378, score 0.2073, risk 0.1513.
- Batch 6, acetonitrile: conversion 0.8196, yield 0.5964, selectivity 0.6996, score 0.3089, risk 0.1923.
- Batch 7, toluene: conversion 0.8265, yield 0.6177, selectivity 0.7443, score 0.3229, risk 0.2064.

The solvent does more than change the total rate. Water gave the highest selectivity but relatively low conversion. Ethanol increased conversion but reduced selectivity enough that its score fell below the water result. Acetonitrile and toluene strongly accelerated conversion; toluene retained better selectivity than acetonitrile and therefore produced the best score at 350 K.

A plausible interpretation is that solvent-specific factors independently modify the desired and undesired activation barriers. In symbolic form, gP(solvent) and gB(solvent) are not proportional. Toluene with Catalyst B appears to provide the best observed balance between kP and kB while still giving rapid conversion. This could represent a genuine catalyst–solvent interaction, but the experiment only screened solvents with Catalyst B, so a full catalyst-by-solvent interaction matrix was not measured.

Risk also followed solvent choice strongly: water < ethanol < acetonitrile < toluene for this catalyst and thermal program. Since the named solvents are benchmark categories rather than a claim about real physical hazards, this ordering should be treated as a property of this world, not generalized to real chemistry.

## 5. Temperature and time dependence

The most informative thermal series used Catalyst B in toluene.

At 3600 s:

- Batch 7, 350 K target: conversion 0.8265, yield 0.6177, selectivity 0.7443, byproduct 0.2181, degradation 0.0678, score 0.3229, risk 0.2064.
- Batch 11, 360 K target: conversion 0.8782, yield 0.6477, selectivity 0.7527, byproduct 0.2272, degradation 0.1005, score 0.3380, risk 0.2157.
- Batch 8, 370 K target: conversion 0.9376, yield 0.6910, selectivity 0.7365, byproduct 0.2440, degradation 0.1105, score 0.3520, risk 0.2273.
- Batch 9, 390 K target: conversion 0.9493, yield 0.6968, selectivity 0.7108, byproduct 0.2780, degradation 0.1554, score 0.3300, risk 0.2697.

Conversion approached a plateau between 370 and 390 K. Yield increased only slightly over that interval, while selectivity deteriorated and both byproduct and degradation signals rose. This is strong evidence for an intermediate optimum rather than a monotonic benefit from temperature. In the kinetic picture, kB and/or kD become increasingly important at high temperature once depletion of R limits further gains in P.

The time series at a 370 K target supports the same interpretation:

- Batch 10, 2400 s: conversion 0.7906, yield 0.6282, selectivity 0.7991, byproduct 0.1730, degradation 0.0629, score 0.3319, risk 0.2183.
- Batch 8, 3600 s: conversion 0.9376, yield 0.6910, selectivity 0.7365, byproduct 0.2440, degradation 0.1105, score 0.3520, risk 0.2273.
- Batch 12, 4200 s: conversion 0.9580, yield 0.6768, selectivity 0.7232, byproduct 0.2794, degradation 0.1574, score 0.3442, risk 0.2292.

From 2400 to 3600 s, the gain in conversion and yield outweighed the loss of selectivity. Beyond 3600 s, conversion rose only modestly, while final yield declined and degradation increased substantially. This is consistent with product degradation or continuing parallel byproduct formation after most useful conversion has occurred. The exact decline in yield between Batches 8 and 12 may include batch and assay variation, but the accompanying changes in selectivity, byproduct, and degradation make the qualitative severity effect persuasive.

Batch 11 at 360 K and 3600 s is also consistent with a smooth severity trend between Batches 7 and 8. The available grid therefore places the score maximum near 370 K and roughly 3600 s, although the exact optimum could lie between the tested settings.

## 6. Safety behavior

Every completed batch remained below the declared safety limit of 0.35. The recommended Batch 8 had risk 0.2273, leaving a margin of approximately 0.123. The highest observed risk was 0.2697 in Batch 9 at 390 K, also below the limit but with less margin and a lower score.

Observed risk appears to contain at least two components:

risk ≈ recipe/categorical contribution + thermal-severity contribution + possible interaction terms.

Catalyst and solvent changed risk before considering the high-temperature comparison, and risk increased with both temperature and, more weakly, duration. In the toluene/Catalyst B series, increasing the target from 350 to 370 to 390 K raised final risk from 0.2064 to 0.2273 to 0.2697. At 370 K, increasing duration from 2400 to 3600 to 4200 s raised risk from 0.2183 to 0.2273 to 0.2292. This suggests a stronger nonlinear temperature term and a weaker, potentially saturating time term over the tested range.

The observations do not reveal whether risk represents peak temperature, accumulated exposure, latent exothermicity, solvent hazard, or a composite benchmark. Therefore, the additive expression above is only an empirical organizational model.

## 7. Relationship to the public score

The score rose with desired yield and favorable selectivity but was reduced when byproduct and degradation became appreciable. It cannot be represented as conversion alone: Batch 9 had higher conversion than Batch 8 but a lower score. Likewise, the short Batch 10 had the best selectivity of the toluene thermal series but insufficient conversion and yield to beat Batch 8.

I did not infer an exact score equation. A qualitative representation is

score = F(yield, selectivity, conversion, byproduct, degradation; safety constraint),

with positive dependence on desired yield/selectivity and negative dependence on undesired signals. Cost was visibly clipped at 1.0 for these full-load recipes, but the declared objective weighted the reaction score, and no evidence established an independent cost penalty in the final leaderboard value.

## 8. Intermediate measurements and uncertainty

Intermediate HPLC and final assays did not agree exactly, as expected from different instrument noise and the timing of termination/final analysis. For example, Batch 8 HPLC reported yield 0.6581, selectivity 0.7253, conversion 0.9279, and score 0.3351, whereas its final assay reported 0.6910, 0.7365, 0.9376, and 0.3520. Batch 12 HPLC reported score 0.3489 versus a final score of 0.3442. These differences warn against treating small score differences as deterministic.

Nevertheless, the main catalyst, solvent, and thermal trends are much larger and internally coherent. The selection of Batch 8 rests on its highest directly observed final score, not on an unmeasured interpolation.

## 9. Recommended mechanistic interpretation of Batch 8

Batch 8 used 0.040 mol reagent, 0.080 L toluene, 0.005 mol Catalyst B, a 370 K target, 3600 s, and 600 rpm. It gave the highest observed final score, 0.3520, at risk 0.2273. Mechanistically, this condition appears to drive the desired channel close to high conversion without spending excessive time in the regime where parallel byproduct formation and product degradation dominate.

The interpretation is not that 370 K is intrinsically special. Rather, under this fixed recipe it is near the point where the marginal gain in desired product from greater severity becomes comparable to the marginal loss from lower selectivity and higher degradation.

## 10. Limits of identification

The following factors remain unidentified:

1. Reaction order and concentration dependence: reagent amount and solvent volume were fixed in every batch.
2. Catalyst-loading dependence: only 0.005 mol was used, so saturation, inhibition, or catalyst decomposition cannot be assessed.
3. Mixing and mass transfer: all batches used 600 rpm.
4. Addition-order effects: reagent, solvent, and catalyst were added in the same order.
5. Detailed time profiles: only one post-heating HPLC point and one final assay were obtained per batch.
6. Replicate variability: no exact condition was deliberately replicated.
7. Full catalyst–solvent interactions: only the catalyst screen in water and solvent screen with Catalyst B were completed.
8. Product degradation identity: degradation_warning is an aggregate signal, not structural identification.
9. Thermal dynamics: the system reported temperature changes, but no continuous internal-temperature or heat-flow trace was measured.
10. Exact score and risk equations: only their outputs were public.

## 11. Reasonable competing explanations

The favored explanation is parallel formation of desired and undesired products plus consecutive degradation of the desired product. However, several alternatives remain compatible with the observations:

- The degradation signal could arise directly from reagent rather than from product, with high severity simply accelerating a third parallel channel.
- Loss of selectivity at high temperature could reflect catalyst-state changes or deactivation rather than a distinct product-degradation reaction.
- Solvent effects could be caused by phase or transport behavior rather than changes in elementary activation barriers.
- The yield decrease at 4200 s could partly be stochastic batch variation or assay noise, although the simultaneous rise in byproduct and degradation favors a real severity effect.
- Conversion and selectivity signals may be nonlinear proxies rather than direct species fractions, so the simple mass-action equations may only be phenomenological.

Within the measured domain, all of these alternatives lead to the same practical conclusion: Catalyst B with toluene performs best among the screened categories, and moderate thermal severity near the Batch 8 program is preferable to either insufficient reaction or more aggressive heating.

## Q — Blind predictions

### Overall rationale

These predictions extend the campaign's Catalyst B results to acetonitrile at smaller scale, a slightly higher reagent concentration, a higher catalyst-to-reagent ratio, lower stirring speed, and mostly higher temperatures. The central model is parallel desired and byproduct formation followed by thermal degradation of desired product. Conversion rises and saturates with thermal severity, while selectivity eventually falls; yield is treated approximately as conversion multiplied by selectivity. Safety risk is modeled as a recipe contribution plus nonlinear temperature, duration, and repeated-heating contributions. Quenching is assumed to occur too late to materially alter composition but to reduce terminal risk. Uncertainty intervals incorporate final-assay noise and, more importantly, extrapolation beyond the campaign's 350–390 K evidence, unmeasured scale and concentration effects, lack of replicates, unknown quench behavior, and possible path dependence in the two-stage programs.

### Q01

The high catalyst-to-reagent ratio and 420 K treatment should drive nearly complete conversion. Extrapolation above the measured temperature range predicts appreciable parallel byproduct formation and degradation, reducing selectivity and yield.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4000 | 0.2700 | 0.5500 |
| conversion | 0.9850 | 0.9300 | 1.0000 |
| safety_risk | 0.2500 | 0.1700 | 0.3600 |
| score | 0.2200 | 0.1000 | 0.3400 |
| selectivity | 0.5500 | 0.4000 | 0.6900 |
| yield | 0.5400 | 0.3900 | 0.6800 |

### Q02

The chemical outcome should be close to Q01 because quenching occurs only after the programmed heat exposure. I predict that quenching chiefly lowers the terminal safety state; this effect was not directly calibrated and therefore has a broad interval.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4000 | 0.2700 | 0.5500 |
| conversion | 0.9850 | 0.9300 | 1.0000 |
| safety_risk | 0.1400 | 0.0700 | 0.2500 |
| score | 0.2200 | 0.1000 | 0.3400 |
| selectivity | 0.5500 | 0.4000 | 0.6900 |
| yield | 0.5400 | 0.3900 | 0.6800 |

### Q03

At 390 K, conversion should be high while thermal damage remains below the 420–450 K cases. The estimate is less selective than the measured toluene result because the acetonitrile batch at 350 K showed poorer selectivity and more degradation.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3300 | 0.2200 | 0.4600 |
| conversion | 0.9650 | 0.9000 | 1.0000 |
| safety_risk | 0.1600 | 0.1000 | 0.2400 |
| score | 0.2800 | 0.1700 | 0.3900 |
| selectivity | 0.6400 | 0.5100 | 0.7600 |
| yield | 0.6200 | 0.4900 | 0.7400 |

### Q04

A 450 K treatment should essentially exhaust the reagent but strongly favor byproduct and degradation channels. Both chemistry and risk are extrapolated well beyond the highest studied temperature, so the intervals are intentionally wide.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5700 | 0.4000 | 0.7300 |
| conversion | 0.9950 | 0.9600 | 1.0000 |
| safety_risk | 0.4000 | 0.2700 | 0.5700 |
| score | 0.0900 | 0.0100 | 0.2200 |
| selectivity | 0.3800 | 0.2200 | 0.5500 |
| yield | 0.3800 | 0.2100 | 0.5400 |

### Q05

The shorter 1500 s exposure should preserve selectivity while the elevated temperature and relatively high catalyst loading still produce substantial conversion. This is predicted to be among the better score conditions in the query set.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2600 | 0.1600 | 0.3900 |
| conversion | 0.8800 | 0.7600 | 0.9600 |
| safety_risk | 0.2000 | 0.1300 | 0.3000 |
| score | 0.3100 | 0.2000 | 0.4200 |
| selectivity | 0.7000 | 0.5700 | 0.8100 |
| yield | 0.6200 | 0.4900 | 0.7400 |

### Q06

The extended 5100 s exposure should add little conversion once depletion is nearly complete but should continue producing byproduct and degradation. This follows the measured decline from 3600 to 4200 s at 370 K, extrapolated to 420 K.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5300 | 0.3700 | 0.6900 |
| conversion | 0.9980 | 0.9700 | 1.0000 |
| safety_risk | 0.2900 | 0.2000 | 0.4200 |
| score | 0.1300 | 0.0300 | 0.2700 |
| selectivity | 0.4200 | 0.2600 | 0.5800 |
| yield | 0.4200 | 0.2600 | 0.5800 |

### Q07

The first 390 K segment should accumulate product, after which the 450 K segment can degrade that product and promote byproduct formation. Two heating operations also plausibly accumulate more risk than one comparable-duration operation.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5200 | 0.3500 | 0.6900 |
| conversion | 0.9950 | 0.9500 | 1.0000 |
| safety_risk | 0.4500 | 0.3000 | 0.6400 |
| score | 0.1000 | 0.0100 | 0.2400 |
| selectivity | 0.4300 | 0.2600 | 0.6000 |
| yield | 0.4300 | 0.2500 | 0.5900 |

### Q08

Compared with Q07, placing the severe segment first leaves the later 390 K segment to complete conversion under less damaging conditions. I therefore predict modestly better selectivity and yield, although the unmeasured path dependence makes this highly uncertain.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4500 | 0.2900 | 0.6200 |
| conversion | 0.9950 | 0.9500 | 1.0000 |
| safety_risk | 0.4500 | 0.3000 | 0.6400 |
| score | 0.1400 | 0.0300 | 0.2900 |
| selectivity | 0.5000 | 0.3300 | 0.6600 |
| yield | 0.5000 | 0.3200 | 0.6500 |

### Q09

A short 440 K pulse should provide high conversion but more thermal loss than Q05. The short duration limits, but does not eliminate, the predicted selectivity and degradation penalties.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3400 | 0.2200 | 0.4900 |
| conversion | 0.9400 | 0.8500 | 0.9900 |
| safety_risk | 0.2900 | 0.1900 | 0.4200 |
| score | 0.2500 | 0.1300 | 0.3700 |
| selectivity | 0.6200 | 0.4700 | 0.7500 |
| yield | 0.5800 | 0.4400 | 0.7100 |

### Q10

The final chemistry should closely match Q09 because the quench follows the complete heat exposure. The predicted distinction is lower terminal safety risk, with substantial uncertainty because no campaign batch directly measured a quench effect.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3400 | 0.2200 | 0.4900 |
| conversion | 0.9400 | 0.8500 | 0.9900 |
| safety_risk | 0.1700 | 0.0800 | 0.2900 |
| score | 0.2500 | 0.1300 | 0.3700 |
| selectivity | 0.6200 | 0.4700 | 0.7500 |
| yield | 0.5800 | 0.4400 | 0.7100 |

### Q11

The relatively mild 370 K temperature should keep risk and instantaneous degradation lower, while 5700 s is long enough for high conversion. The long residence time still causes a predicted selectivity penalty compared with a shorter 370 K treatment.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3200 | 0.2100 | 0.4600 |
| conversion | 0.9700 | 0.9000 | 1.0000 |
| safety_risk | 0.1400 | 0.0800 | 0.2200 |
| score | 0.2900 | 0.1700 | 0.4000 |
| selectivity | 0.6500 | 0.5200 | 0.7700 |
| yield | 0.6300 | 0.5000 | 0.7500 |

### Q12

This is the most extreme extrapolation: 460 K for 6300 s should give effectively complete conversion but severe byproduct formation, degradation, and safety burden. The desired yield and score may approach zero, though the absence of observations in this regime requires very broad intervals.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7700 | 0.5700 | 0.9100 |
| conversion | 0.9990 | 0.9700 | 1.0000 |
| safety_risk | 0.6800 | 0.4600 | 0.9000 |
| score | 0.0150 | 0.0000 | 0.0800 |
| selectivity | 0.1500 | 0.0400 | 0.3400 |
| yield | 0.1500 | 0.0300 | 0.3300 |

## K2 — Retrospective analysis

1. Assessment of the initial information

The initial material packet supplied very few substantive mechanistic claims. It explicitly said that the catalysts were anonymous benchmark formulations, that solvent effects were calibrated categorical benchmark effects rather than real-solvent predictions, that no task-specific property dossier was available, and that experimental evidence should be authoritative. Thus, there was no initial Arrhenius law, reaction network, catalyst ranking, solvent ranking, or nominal optimum to confirm or refute.

Several framework-level claims were supported:

- The statement that catalysts had distinct latent activity profiles was supported by Batches 1–4. Under the common water/350 K/3600 s condition, Catalyst B produced a final score of 0.2589, versus 0.1445, 0.1311, and 0.1865 for A, C, and D. This was a genuine categorical catalyst effect.
- The claim that solvents acted as categorical benchmark variables was supported by Batches 2 and 5–7. With Catalyst B at 350 K for 3600 s, the score ranged from 0.2073 in ethanol to 0.3229 in toluene.
- The declared distinction between instrument noise and process behavior was consistent with observed HPLC/final-assay differences. For example, Batch 8 moved from an HPLC score of 0.3351 to a final-assay score of 0.3520, while Batch 12 moved from 0.3489 to 0.3442.

These observations do not validate real chemical claims about water, ethanol, acetonitrile, or toluene. The initial packet specifically warned against such an interpretation, and I respected that in K1 by stating that I would not assign a real catalyst identity or named synthesis. Claims such as real-solvent polarity, boiling point, or physical flammability effects were never tested.

There was no clear initial mechanistic claim that the campaign refuted. More precisely, the lack of contradiction to the benchmark-description statements is not positive mechanistic validation. The packet's hidden categorical coupling remains compatible with the results, but it is too general to be falsified by the campaign.

Several important matters remained untested: concentration dependence, catalyst-loading dependence, reaction order, mixing limitations, addition-order effects, exact risk composition, and whether the named-solvent categories generalize outside this world. K1 correctly listed these as identification limits. I did not encounter contrary evidence and ignore it; rather, the campaign did not generate evidence capable of resolving them.

2. Experiments that formed or changed my judgments

The first strong update came from Batches 1–4. Before these experiments, choosing among catalysts was essentially a guess because the initial information gave no activity ordering. Batch 2 made Catalyst B the clear working choice: its conversion, yield, and selectivity were all materially better than those of Catalyst A under the matched condition. This led me to use Catalyst B in every subsequent batch.

Batches 5–7 then changed the solvent judgment. Water/Catalyst B in Batch 2 had high selectivity, 0.7805, but only 0.5454 conversion. Ethanol in Batch 5 increased conversion but damaged selectivity and score. Acetonitrile in Batch 6 and toluene in Batch 7 gave much higher conversion, with toluene retaining better selectivity and producing the best score. These results formed the K1 judgment that solvent changed both overall rate and channel balance, rather than merely multiplying all rates equally.

Batches 8 and 9 were the most important tests of thermal severity. Batch 8 at 370 K increased the final score to 0.3520 at risk 0.2273. Batch 9 at 390 K increased conversion slightly, from 0.9376 to 0.9493, but reduced selectivity, increased byproduct and degradation signals, and lowered the score to 0.3300. This was the principal evidence behind the K1 statement that “maximum conversion is not the same as maximum safe score.”

Batches 10–12 refined that judgment. Batch 10 at 370 K for 2400 s retained high selectivity but lacked sufficient conversion. Batch 12 at 370 K for 4200 s reached 0.9580 conversion but showed lower yield and higher degradation than Batch 8. Batch 11 at 360 K for 3600 s fell between the 350 and 370 K results. Together they supported an intermediate-severity optimum and motivated the parallel-plus-consecutive network proposed in K1.

The choice to begin with maximum permitted reagent, solvent, and catalyst amounts was not evidence-based. It was an optimization-oriented guess intended to create measurable product and use a uniform recipe. Likewise, the initial 350 K, 3600 s, and 600 rpm condition was a plausible baseline rather than a conclusion derived from supplied data.

The catalyst screen was driven by initial ignorance. The solvent screen was driven by the Catalyst B result. The later temperature and duration experiments were increasingly data-driven. The final Batch 12 choice of 370 K for 4200 s was specifically motivated by the observed Batch 8 result and the desire to test whether a modestly longer residence time would improve conversion enough to improve the score.

3. Leading competing mechanisms and what can be distinguished

K1 favored the network R -> P, R -> B, and P -> D. It is attractive because increasing severity first raised conversion and desired yield, while still greater severity raised byproduct and degradation signals and eventually reduced yield and score.

The most important competitors are:

- Three parallel channels, R -> P, R -> B, and R -> D, without any degradation of P.
- Catalyst-state change or deactivation at high temperature, causing the desired pathway to lose selectivity.
- A transport or phase effect in which solvent and temperature alter mixing or accessibility rather than elementary reaction barriers.
- Instrument-response effects in which degradation_warning and byproduct_signal are correlated proxies rather than independent species balances.
- A reversible or equilibrium-limited desired pathway combined with an irreversible byproduct pathway.

The existing results distinguish a simple single-channel monotonic conversion model from a model containing at least one severity-dependent competing process. Batch 9's greater conversion but lower score than Batch 8, and Batch 12's higher conversion but lower yield than Batch 8, are inconsistent with the idea that all converted reagent becomes stable desired product.

The campaign does not distinguish P -> D from a parallel R -> D channel. A higher degradation signal after a more severe treatment is compatible with both. It also does not distinguish intrinsic selectivity changes from catalyst deactivation, because catalyst state was not measured. Solvent effects cannot be assigned to kinetics rather than transport because stirring and phase behavior were not varied or characterized. No complete mass-balance model was fitted, and the public signals need not correspond one-to-one with chemical species.

The approximate relationship yield ≈ conversion × selectivity was visible in several batches and supports internal consistency among those observables. It does not identify whether loss of selectivity occurred before or after desired product formation.

4. One additional complete experiment

If exactly one legal complete experiment were available, I would use the Batch 8 composition and operating setup: 0.040 mol reagent, 0.080 L toluene, 0.005 mol Catalyst B, and 600 rpm. I would heat at 370 K for 3600 s, take the allowed HPLC measurement, then continue at 370 K for another 1800 s before termination and final assay.

This is deliberately a diagnostic post-conversion challenge. Batch 8 provides the external reference at 3600 s, while the intermediate measurement would document the state of the new vessel before the extra thermal exposure. I would measure conversion, yield, selectivity, and byproduct by HPLC and then conversion, yield, selectivity, byproduct, degradation_warning, safety risk, and score by final assay.

Possible interpretations would be:

- If conversion changed little while yield and selectivity fell and degradation_warning rose strongly, confidence in consecutive P -> D would increase.
- If conversion continued to rise while yield rose proportionally and degradation stayed nearly constant, the apparent Batch 12 loss would look more like process or assay variability, weakening the consecutive-degradation interpretation.
- If conversion stayed fixed but byproduct increased without a corresponding degradation increase, a continuing parallel or product-to-byproduct pathway would become more plausible.
- If the 3600 s intermediate state differed substantially from Batch 8 before the extra hold, batch variability would be larger than assumed and the mechanistic comparison would be inconclusive.
- If risk rose disproportionately during the second heat step, I would revise the weakly saturating duration model in K1 toward an operation-count or accumulated-exposure model.

This design is not perfect because HPLC and final assay are different instruments. An exact Batch 8 replicate would be better for pure repeatability, but the proposed extension gives more mechanistic information from the single added vessel.

5. Tradeoff between mechanistic identifiability and operating score

The research goal emphasized finding a strong safe-score procedure, and that materially shaped the campaign. After identifying Catalyst B, I rapidly concentrated experiments on that catalyst rather than completing a catalyst-by-solvent factorial design. After identifying toluene as the best screened solvent, I spent the remaining batches refining temperature and duration around that recipe.

This was an optimization-favoring choice. It produced a useful local response surface and found Batch 8, but it sacrificed several forms of identifiability:

- Only catalysts were compared in water; only solvents were compared with Catalyst B. Catalyst–solvent interactions are therefore confounded.
- Reagent amount, solvent volume, catalyst loading, stirring speed, and addition order never varied.
- There were no exact replicates.
- There was no low-catalyst or catalyst-free control.
- There was no deliberate post-reaction hold or quench comparison.

Some early batches sacrificed immediate score to gain information. Batches 1, 3, and 4 tested catalysts that ultimately performed poorly, and Batch 5 tested ethanol despite its lower score. Those were worthwhile screening expenditures. Conversely, Batches 8–12 were primarily local optimization experiments. Batch 12, for example, added only a modest time perturbation around the incumbent and contributed less broad mechanistic information than a new loading or interaction test would have.

The design therefore moved from exploration to exploitation. That was appropriate for the stated score objective but left K1's equations qualitative and non-identifiable. A mechanism-first campaign would have used a factorial or response-surface plan with concentration, catalyst loading, temperature, and time variation, probably at the cost of fewer high-scoring batches.

6. Underused evidence and weaknesses in the blind predictions

Several pieces of evidence were not fully exploited:

- I used processed HPLC and final-assay estimates but did not analyze the underlying public spectra, peak assignments, calibration flags, mass-balance fields, or replicate signals.
- Operation-level risk increments were noticed but not systematically modeled across every addition and heat operation.
- Actual temperature changes were reported for several heats, but I did not build a thermal-dynamics model connecting target temperature, achieved temperature, duration, and risk.
- HPLC-to-final differences were described qualitatively rather than used to estimate an empirical between-instrument or process-variation distribution.
- I did not fit even a simple censored kinetic model to the temperature/time series. Such a fit would still have been weakly identified, but it could have made the extrapolation assumptions more explicit.
- The approximate mass-balance relation among conversion, yield, and selectivity could have been enforced more systematically in the predictions.

The least reliable blind predictions are Q12, Q07, Q08, Q04, Q02, and Q10.

Q12 extrapolated to 460 K for 6300 s, far outside K1's stated domain of approximately 2400–4200 s and at temperatures above the highest studied 390 K condition. Its conversion interval of 0.97–1.00 is probably too narrow because catalyst deactivation, volatility, phase changes, or unmodeled loss could prevent complete conversion. Its risk and score intervals are broad, but even they rest on an unsupported extrapolation.

Q07 and Q08 contain two sequential heat operations and ask about order dependence. The campaign had no multi-stage thermal experiment, so my prediction that high-temperature-first would be less damaging than high-temperature-second was mechanistic speculation. The selectivity, yield, score, and risk intervals may all be too narrow. In particular, I assumed that risk contributions from repeated heating accumulate similarly regardless of order, which was never established.

Q04 at 450 K for 3300 s also extrapolates far beyond the observed thermal range. Its conversion lower bound of 0.96 was overly confident for the same reason as Q12.

Q02 and Q10 are quench comparisons. No campaign batch used a quench. I predicted unchanged chemistry but substantially reduced safety risk. That is a reasonable hypothesis, not a campaign-supported conclusion. The safety intervals may be too narrow, and even the claim of unchanged composition could fail if the quench transforms, dilutes, partitions, or stabilizes measured species.

All 12 blind queries also changed scale, concentration, catalyst-to-reagent ratio, addition order, and stirring speed relative to the campaign. K1 explicitly stated that concentration dependence, catalyst-loading dependence, mixing, and addition-order effects were unidentified. Although the prediction rationale acknowledged these shifts, several numerical intervals—especially the near-unity conversion intervals—did not fully reflect the breadth of that stated uncertainty. That is an inconsistency between the caution of K1 and the quantitative confidence of parts of Q.

The more defensible predictions are the relative comparisons within matched pairs or local groups: Q02 versus Q01, Q10 versus Q09, shorter versus longer heating at 420 K, and the expectation that Q12 is more damaging than Q11. Even there, the directions are more credible than the numerical magnitudes.

7. Limitations of the sealed recommendation

The sealed recommendation selected Batch 8 because it had the highest observed final score, 0.3520, while its safety risk, 0.2273, remained below the 0.35 limit. This is accurately described as the sample-best completed batch.

It has not been proved globally optimal, or even precisely locally optimal. The tested grid was sparse. The true local optimum could lie at, for example, 365–375 K, a duration between 3000 and 3900 s, a different catalyst loading, or a different concentration. Batch 12 scored 0.3442 and Batch 11 scored 0.3380, so the advantage of Batch 8 is meaningful but not enormous relative to plausible batch and assay variation.

Repeatability should be tested with several exact Batch 8 replicates performed in randomized order, reporting both within-batch instrument uncertainty and between-batch variability. The relevant question is not merely whether the mean remains near 0.352, but how often the procedure remains below the safety limit and outperforms neighboring conditions.

Local robustness should be tested with small perturbations around Batch 8: temperature, duration, stirring speed, catalyst loading, reagent concentration, addition order, and solvent volume. A useful robustness criterion would penalize conditions whose score collapses or whose risk approaches 0.35 under modest perturbation, even if their nominal mean score is high.

Cross-material generalization requires at least a partial catalyst-by-solvent matrix. The campaign does not establish that Catalyst B is best in every solvent or that toluene is best with every catalyst. Cross-world generalization is even less justified: the material packet explicitly defines categorical benchmark effects for this world, not transferable real-chemical properties.

Finally, the recommendation is tied to the exact public scoring and safety contracts. A procedure optimized for this reaction score may not be optimal under a different weighting of degradation, cost, solvent burden, or safety margin. Therefore, the strongest warranted statement is: Batch 8 was the highest-scoring observed completed experiment in this campaign and was safely within the declared limit. It is not a demonstrated global optimum, a proven robust optimum, or a generally transferable chemical procedure.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 84.0 | none | 0 |
| Q | yes | 0 | 111.0 | none | 0 |
| K2 | yes | 0 | 110.3 | none | 0 |

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean 80% width | Mean interval score |
|---|---:|---:|---:|---:|
| byproduct_signal | 0.0753 | 0.8833 | 0.2900 | 0.3015 |
| conversion | 0.0214 | 0.8833 | 0.0850 | 0.0901 |
| safety_risk | 0.0811 | 0.7500 | 0.2417 | 0.3692 |
| score | 0.1261 | 0.4833 | 0.2208 | 0.4076 |
| selectivity | 0.1248 | 0.5833 | 0.2917 | 0.3963 |
| yield | 0.1366 | 0.5000 | 0.2908 | 0.5048 |

## Predictions versus released reference truth

### Q01

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4000 | 0.2700 | 0.5500 | 0.3661 | 0.3711, 0.3582, 0.3829, 0.3546, 0.3637 |
| conversion | 0.9850 | 0.9300 | 1.0000 | 0.9983 | 1.0000, 1.0000, 1.0000, 0.9986, 0.9928 |
| safety_risk | 0.2500 | 0.1700 | 0.3600 | 0.3271 | 0.3271, 0.3271, 0.3271, 0.3271, 0.3271 |
| score | 0.2200 | 0.1000 | 0.3400 | 0.3117 | 0.3089, 0.3133, 0.3128, 0.3125, 0.3110 |
| selectivity | 0.5500 | 0.4000 | 0.6900 | 0.6454 | 0.6395, 0.6416, 0.6482, 0.6527, 0.6453 |
| yield | 0.5400 | 0.3900 | 0.6800 | 0.6395 | 0.6358, 0.6456, 0.6401, 0.6368, 0.6391 |
### Q02

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4000 | 0.2700 | 0.5500 | 0.3678 | 0.3770, 0.3726, 0.3588, 0.3768, 0.3536 |
| conversion | 0.9850 | 0.9300 | 1.0000 | 0.9992 | 1.0000, 1.0000, 0.9960, 1.0000, 1.0000 |
| safety_risk | 0.1400 | 0.0700 | 0.2500 | 0.1558 | 0.1558, 0.1558, 0.1558, 0.1558, 0.1558 |
| score | 0.2200 | 0.1000 | 0.3400 | 0.3843 | 0.3838, 0.3841, 0.3876, 0.3844, 0.3815 |
| selectivity | 0.5500 | 0.4000 | 0.6900 | 0.6378 | 0.6410, 0.6229, 0.6441, 0.6452, 0.6359 |
| yield | 0.5400 | 0.3900 | 0.6800 | 0.6412 | 0.6377, 0.6497, 0.6463, 0.6367, 0.6353 |
### Q03

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3300 | 0.2200 | 0.4600 | 0.3044 | 0.3118, 0.2995, 0.2990, 0.3073, 0.3044 |
| conversion | 0.9650 | 0.9000 | 1.0000 | 0.9949 | 1.0000, 0.9882, 0.9993, 0.9868, 1.0000 |
| safety_risk | 0.1600 | 0.1000 | 0.2400 | 0.1950 | 0.1950, 0.1950, 0.1950, 0.1950, 0.1950 |
| score | 0.2800 | 0.1700 | 0.3900 | 0.4036 | 0.4011, 0.4007, 0.4038, 0.4111, 0.4016 |
| selectivity | 0.6400 | 0.5100 | 0.7600 | 0.6944 | 0.6873, 0.6875, 0.6946, 0.7114, 0.6911 |
| yield | 0.6200 | 0.4900 | 0.7400 | 0.6910 | 0.6879, 0.6895, 0.6901, 0.7010, 0.6867 |
### Q04

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5700 | 0.4000 | 0.7300 | 0.4313 | 0.4386, 0.4318, 0.4285, 0.4243, 0.4336 |
| conversion | 0.9950 | 0.9600 | 1.0000 | 0.9955 | 1.0000, 0.9995, 1.0000, 1.0000, 0.9781 |
| safety_risk | 0.4000 | 0.2700 | 0.5700 | 0.4212 | 0.4212, 0.4212, 0.4212, 0.4212, 0.4212 |
| score | 0.0900 | 0.0100 | 0.2200 | 0.2325 | 0.2360, 0.2291, 0.2318, 0.2346, 0.2309 |
| selectivity | 0.3800 | 0.2200 | 0.5500 | 0.5807 | 0.5940, 0.5696, 0.5798, 0.5793, 0.5809 |
| yield | 0.3800 | 0.2100 | 0.5400 | 0.5884 | 0.5878, 0.5859, 0.5861, 0.5936, 0.5887 |
### Q05

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2600 | 0.1600 | 0.3900 | 0.1919 | 0.1999, 0.1936, 0.1956, 0.1847, 0.1857 |
| conversion | 0.8800 | 0.7600 | 0.9600 | 0.9641 | 0.9653, 0.9636, 0.9659, 0.9650, 0.9609 |
| safety_risk | 0.2000 | 0.1300 | 0.3000 | 0.3273 | 0.3273, 0.3273, 0.3273, 0.3273, 0.3273 |
| score | 0.3100 | 0.2000 | 0.4200 | 0.4064 | 0.4049, 0.4081, 0.4049, 0.4106, 0.4033 |
| selectivity | 0.7000 | 0.5700 | 0.8100 | 0.8032 | 0.8034, 0.8204, 0.7967, 0.8219, 0.7738 |
| yield | 0.6200 | 0.4900 | 0.7400 | 0.7825 | 0.7786, 0.7763, 0.7826, 0.7812, 0.7941 |
### Q06

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5300 | 0.3700 | 0.6900 | 0.5074 | 0.5074, 0.5103, 0.5024, 0.5104, 0.5064 |
| conversion | 0.9980 | 0.9700 | 1.0000 | 0.9997 | 1.0000, 1.0000, 0.9987, 1.0000, 1.0000 |
| safety_risk | 0.2900 | 0.2000 | 0.4200 | 0.3268 | 0.3268, 0.3268, 0.3268, 0.3268, 0.3268 |
| score | 0.1300 | 0.0300 | 0.2700 | 0.2221 | 0.2215, 0.2177, 0.2267, 0.2202, 0.2244 |
| selectivity | 0.4200 | 0.2600 | 0.5800 | 0.5033 | 0.4978, 0.4899, 0.5120, 0.5071, 0.5098 |
| yield | 0.4200 | 0.2600 | 0.5800 | 0.5074 | 0.5094, 0.5047, 0.5138, 0.5001, 0.5090 |
### Q07

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5200 | 0.3500 | 0.6900 | 0.4056 | 0.3992, 0.4027, 0.3978, 0.4203, 0.4080 |
| conversion | 0.9950 | 0.9500 | 1.0000 | 0.9957 | 1.0000, 0.9892, 1.0000, 0.9894, 1.0000 |
| safety_risk | 0.4500 | 0.3000 | 0.6400 | 0.4329 | 0.4329, 0.4329, 0.4329, 0.4329, 0.4329 |
| score | 0.1000 | 0.0100 | 0.2400 | 0.2409 | 0.2417, 0.2395, 0.2409, 0.2380, 0.2446 |
| selectivity | 0.4300 | 0.2600 | 0.6000 | 0.6144 | 0.6243, 0.6129, 0.6092, 0.6034, 0.6225 |
| yield | 0.4300 | 0.2500 | 0.5900 | 0.6023 | 0.5969, 0.6014, 0.6043, 0.6034, 0.6053 |
### Q08

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4500 | 0.2900 | 0.6200 | 0.3999 | 0.4150, 0.4019, 0.3945, 0.4007, 0.3876 |
| conversion | 0.9950 | 0.9500 | 1.0000 | 0.9967 | 1.0000, 0.9900, 0.9935, 1.0000, 1.0000 |
| safety_risk | 0.4500 | 0.3000 | 0.6400 | 0.2015 | 0.2015, 0.2015, 0.2015, 0.2015, 0.2015 |
| score | 0.1400 | 0.0300 | 0.2900 | 0.3495 | 0.3550, 0.3465, 0.3441, 0.3457, 0.3562 |
| selectivity | 0.5000 | 0.3300 | 0.6600 | 0.6174 | 0.6125, 0.6215, 0.6070, 0.6070, 0.6390 |
| yield | 0.5000 | 0.3200 | 0.6500 | 0.6112 | 0.6271, 0.6029, 0.6049, 0.6074, 0.6138 |
### Q09

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3400 | 0.2200 | 0.4900 | 0.2157 | 0.2139, 0.2192, 0.2065, 0.2248, 0.2142 |
| conversion | 0.9400 | 0.8500 | 0.9900 | 0.9822 | 0.9779, 0.9743, 0.9871, 0.9816, 0.9901 |
| safety_risk | 0.2900 | 0.1900 | 0.4200 | 0.4014 | 0.4014, 0.4014, 0.4014, 0.4014, 0.4014 |
| score | 0.2500 | 0.1300 | 0.3700 | 0.3688 | 0.3704, 0.3654, 0.3661, 0.3703, 0.3717 |
| selectivity | 0.6200 | 0.4700 | 0.7500 | 0.7845 | 0.7914, 0.7629, 0.7803, 0.7954, 0.7923 |
| yield | 0.5800 | 0.4400 | 0.7100 | 0.7792 | 0.7799, 0.7863, 0.7739, 0.7764, 0.7795 |
### Q10

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3400 | 0.2200 | 0.4900 | 0.2145 | 0.2078, 0.2005, 0.2088, 0.2291, 0.2264 |
| conversion | 0.9400 | 0.8500 | 0.9900 | 0.9863 | 0.9887, 0.9803, 0.9816, 0.9811, 1.0000 |
| safety_risk | 0.1700 | 0.0800 | 0.2900 | 0.1883 | 0.1883, 0.1883, 0.1883, 0.1883, 0.1883 |
| score | 0.2500 | 0.1300 | 0.3700 | 0.4623 | 0.4647, 0.4590, 0.4625, 0.4649, 0.4606 |
| selectivity | 0.6200 | 0.4700 | 0.7500 | 0.7874 | 0.7957, 0.7843, 0.7856, 0.7886, 0.7828 |
| yield | 0.5800 | 0.4400 | 0.7100 | 0.7789 | 0.7791, 0.7741, 0.7815, 0.7858, 0.7740 |
### Q11

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3200 | 0.2100 | 0.4600 | 0.4056 | 0.3998, 0.4141, 0.4004, 0.4077, 0.4058 |
| conversion | 0.9700 | 0.9000 | 1.0000 | 0.9898 | 0.9902, 0.9783, 0.9875, 1.0000, 0.9929 |
| safety_risk | 0.1400 | 0.0800 | 0.2200 | 0.1568 | 0.1568, 0.1568, 0.1568, 0.1568, 0.1568 |
| score | 0.2900 | 0.1700 | 0.4000 | 0.3583 | 0.3600, 0.3543, 0.3578, 0.3581, 0.3614 |
| selectivity | 0.6500 | 0.5200 | 0.7700 | 0.6037 | 0.6056, 0.6084, 0.6044, 0.5914, 0.6089 |
| yield | 0.6300 | 0.5000 | 0.7500 | 0.5977 | 0.6005, 0.5876, 0.5965, 0.6024, 0.6014 |
### Q12

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.7700 | 0.5700 | 0.9100 | 0.6871 | 0.6912, 0.6734, 0.6842, 0.7000, 0.6867 |
| conversion | 0.9990 | 0.9700 | 1.0000 | 0.9967 | 0.9995, 0.9953, 0.9901, 1.0000, 0.9987 |
| safety_risk | 0.6800 | 0.4600 | 0.9000 | 0.4328 | 0.4328, 0.4328, 0.4328, 0.4328, 0.4328 |
| score | 0.0150 | 0.0000 | 0.0800 | 0.0681 | 0.0730, 0.0656, 0.0644, 0.0697, 0.0677 |
| selectivity | 0.1500 | 0.0400 | 0.3400 | 0.3424 | 0.3558, 0.3442, 0.3324, 0.3403, 0.3390 |
| yield | 0.1500 | 0.0300 | 0.3300 | 0.3454 | 0.3486, 0.3383, 0.3441, 0.3500, 0.3460 |

## Recommendation retest

- Selected source batch: `8`
- Retest exact replay verified: `True`
- Retest failure: `none`

| Metric | Selected source batch | Independent retest | Retest minus source |
|---|---:|---:|---:|
| byproduct_signal | 0.2440 | 0.2466 | 0.0026 |
| conversion | 0.9376 | 0.9243 | -0.0133 |
| cost | 1.0000 | 1.0000 | 0.0000 |
| degradation_warning | 0.1105 | 0.1087 | -0.0018 |
| safety_risk | 0.2273 | 0.2273 | 0.0000 |
| score | 0.3520 | 0.3429 | -0.0090 |
| selectivity | 0.7365 | 0.7207 | -0.0158 |
| virtual_spectrum_summary | 0.1839 | 0.1845 | 0.0006 |
| yield | 0.6910 | 0.6816 | -0.0094 |

## Scope note

This is the final sanitized report produced after all 60 source sessions and K1/Q/K2 chains were sealed. It includes released reference truth, blind-prediction evaluation, and the independent recommendation retest. Provider-private event streams, credentials, thread identifiers, and token accounting remain excluded.
