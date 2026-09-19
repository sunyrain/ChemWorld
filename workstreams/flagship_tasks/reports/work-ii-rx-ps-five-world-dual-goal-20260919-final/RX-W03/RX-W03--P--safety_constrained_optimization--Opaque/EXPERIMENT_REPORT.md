# RX-W03--P--safety_constrained_optimization--Opaque

## Run summary

- World: `RX-W03`
- Locus: `P`
- Goal: `safety_constrained_optimization`
- Arm: `Opaque`
- Status: `completed`
- Source status: `completed`
- Experimental sessions: `12/12`
- Operations: `96`
- Exact replay verified: `True`
- Rollbacks: `[]`
- Posttest chain sealed: `True`

### Recovery status

- Effective result location: `source-repair-v9`
- Recovery version: `recovery-v9-parallel4`
- Repaired stages: `source`
- Source experiments rerun: `False`
- Original source thread reused: `False`
- Truth revealed during recovery: `False`

## Sealed recommendation

- Selected batch: `11`
- Rationale: Batch 11 achieved the highest observed final safe score (about 0.338) while keeping safety risk about 0.187, comfortably below the 0.35 limit; it used Catalyst B in acetonitrile with a 360 K boundary target for 2400 s, followed by quench.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S2 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 340 K x 3600 s @ 600 rpm | yes | 0.3300 | 0.6442 | 0.4955 | 0.1601 | 0.0367 | 0.1520 | 0.1742 |
| 2 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 340 K x 3600 s @ 600 rpm | yes | 0.5899 | 0.7302 | 0.7962 | 0.2173 | 0.1541 | 0.1860 | 0.3144 |
| 3 | S2 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 340 K x 3600 s @ 600 rpm | yes | 0.4698 | 0.7261 | 0.6466 | 0.1858 | 0.0675 | 0.1683 | 0.2584 |
| 4 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 340 K x 3600 s @ 600 rpm | yes | 0.4500 | 0.7479 | 0.5780 | 0.1388 | 0.0569 | 0.1651 | 0.2505 |
| 5 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 340 K x 3600 s @ 600 rpm | yes | 0.4514 | 0.8150 | 0.5701 | 0.1200 | 0.0299 | 0.1237 | 0.2856 |
| 6 | S1 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 340 K x 3600 s @ 600 rpm | yes | 0.5278 | 0.7484 | 0.6706 | 0.1681 | 0.0671 | 0.1547 | 0.2957 |
| 7 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 340 K x 3600 s @ 600 rpm | yes | 0.4313 | 0.6309 | 0.7033 | 0.2675 | 0.1074 | 0.1832 | 0.2182 |
| 8 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 360 K x 3600 s @ 600 rpm | yes | 0.6330 | 0.6893 | 0.9039 | 0.2704 | 0.2120 | 0.1961 | 0.3277 |
| 9 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 380 K x 3600 s @ 600 rpm | yes | 0.6252 | 0.6459 | 0.9557 | 0.3454 | 0.2733 | 0.2022 | 0.3161 |
| 10 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 360 K x 7200 s @ 600 rpm | yes | 0.4592 | 0.4773 | 0.9908 | 0.5516 | 0.4542 | 0.1973 | 0.2133 |
| 11 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 360 K x 2400 s @ 600 rpm | yes | 0.6148 | 0.7892 | 0.7877 | 0.1775 | 0.1054 | 0.1871 | 0.3378 |
| 12 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 370 K x 1800 s @ 600 rpm | yes | 0.5934 | 0.8213 | 0.7165 | 0.1390 | 0.0970 | 0.1837 | 0.3316 |

## Complete experimental actions and observations

### Batch 1

Lifecycle index: `1`; end step: `8`.

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
  "end_step": 8,
  "lifecycle_index": 1,
  "metrics": {
    "byproduct_signal": 0.16007480025291443,
    "conversion": 0.49554625153541565,
    "cost": 1.0,
    "degradation_warning": 0.03666546195745468,
    "safety_risk": 0.15200887620449066,
    "score": 0.17420463263988495,
    "selectivity": 0.6441830992698669,
    "virtual_spectrum_summary": 0.10454059392213821,
    "yield": 0.33002057671546936
  },
  "ordinal": 1
}
```

### Batch 2

Lifecycle index: `2`; end step: `16`.

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
  "end_step": 16,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.21734558045864105,
    "conversion": 0.7962155342102051,
    "cost": 1.0,
    "degradation_warning": 0.15414299070835114,
    "safety_risk": 0.18604473769664764,
    "score": 0.31443870067596436,
    "selectivity": 0.7302423715591431,
    "virtual_spectrum_summary": 0.18890441954135895,
    "yield": 0.5899417400360107
  },
  "ordinal": 2
}
```

### Batch 3

Lifecycle index: `3`; end step: `24`.

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
  "end_step": 24,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.18581309914588928,
    "conversion": 0.6465545892715454,
    "cost": 1.0,
    "degradation_warning": 0.06753826141357422,
    "safety_risk": 0.16825157403945923,
    "score": 0.2583675980567932,
    "selectivity": 0.7260504364967346,
    "virtual_spectrum_summary": 0.1325894147157669,
    "yield": 0.4697818458080292
  },
  "ordinal": 3
}
```

### Batch 4

Lifecycle index: `4`; end step: `32`.

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
  "end_step": 32,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.1387704759836197,
    "conversion": 0.5779897570610046,
    "cost": 1.0,
    "degradation_warning": 0.05689626187086105,
    "safety_risk": 0.1650938093662262,
    "score": 0.25048699975013733,
    "selectivity": 0.7478566765785217,
    "virtual_spectrum_summary": 0.10192707926034927,
    "yield": 0.45004022121429443
  },
  "ordinal": 4
}
```

### Batch 5

Lifecycle index: `5`; end step: `40`.

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
      "target_temperature_K": 340
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
  "end_step": 40,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.12004119902849197,
    "conversion": 0.5701084733009338,
    "cost": 1.0,
    "degradation_warning": 0.029894446954131126,
    "safety_risk": 0.12371555715799332,
    "score": 0.2856404781341553,
    "selectivity": 0.8150123953819275,
    "virtual_spectrum_summary": 0.07947515696287155,
    "yield": 0.45137131214141846
  },
  "ordinal": 5
}
```

### Batch 6

Lifecycle index: `6`; end step: `48`.

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
      "target_temperature_K": 340
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
  "end_step": 48,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.16809634864330292,
    "conversion": 0.6706379652023315,
    "cost": 1.0,
    "degradation_warning": 0.06706488877534866,
    "safety_risk": 0.15473076701164246,
    "score": 0.29565730690956116,
    "selectivity": 0.7484396696090698,
    "virtual_spectrum_summary": 0.12263219058513641,
    "yield": 0.527781069278717
  },
  "ordinal": 6
}
```

### Batch 7

Lifecycle index: `7`; end step: `56`.

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
      "target_temperature_K": 340
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
  "end_step": 56,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.26746493577957153,
    "conversion": 0.7032671570777893,
    "cost": 1.0,
    "degradation_warning": 0.10744930803775787,
    "safety_risk": 0.18316683173179626,
    "score": 0.21815964579582214,
    "selectivity": 0.6309133172035217,
    "virtual_spectrum_summary": 0.19545790553092957,
    "yield": 0.43132415413856506
  },
  "ordinal": 7
}
```

### Batch 8

Lifecycle index: `8`; end step: `64`.

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
      "target_temperature_K": 360
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
  "end_step": 64,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.2703862488269806,
    "conversion": 0.903884768486023,
    "cost": 1.0,
    "degradation_warning": 0.2119903266429901,
    "safety_risk": 0.19612641632556915,
    "score": 0.3276544213294983,
    "selectivity": 0.6893018484115601,
    "virtual_spectrum_summary": 0.24410808086395264,
    "yield": 0.6329934597015381
  },
  "ordinal": 8
}
```

### Batch 9

Lifecycle index: `9`; end step: `72`.

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
  "end_step": 72,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.34543514251708984,
    "conversion": 0.9557012915611267,
    "cost": 1.0,
    "degradation_warning": 0.27331435680389404,
    "safety_risk": 0.20220541954040527,
    "score": 0.3161194622516632,
    "selectivity": 0.6458503603935242,
    "virtual_spectrum_summary": 0.3129808008670807,
    "yield": 0.6251979470252991
  },
  "ordinal": 9
}
```

### Batch 10

Lifecycle index: `10`; end step: `80`.

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
      "stirring_speed_rpm": 600,
      "target_temperature_K": 360
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
  "end_step": 80,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.5516233444213867,
    "conversion": 0.9907575845718384,
    "cost": 1.0,
    "degradation_warning": 0.4542219936847687,
    "safety_risk": 0.19731606543064117,
    "score": 0.21329747140407562,
    "selectivity": 0.4772706925868988,
    "virtual_spectrum_summary": 0.5077927708625793,
    "yield": 0.4592406749725342
  },
  "ordinal": 10
}
```

### Batch 11

Lifecycle index: `11`; end step: `88`.

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
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 360
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
  "end_step": 88,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.17747047543525696,
    "conversion": 0.7876509428024292,
    "cost": 1.0,
    "degradation_warning": 0.1054215356707573,
    "safety_risk": 0.18712162971496582,
    "score": 0.3377727270126343,
    "selectivity": 0.789156436920166,
    "virtual_spectrum_summary": 0.14504845440387726,
    "yield": 0.6148081421852112
  },
  "ordinal": 11
}
```

### Batch 12

Lifecycle index: `12`; end step: `96`.

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
  "end_step": 96,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.13898800313472748,
    "conversion": 0.7164773941040039,
    "cost": 1.0,
    "degradation_warning": 0.09704732894897461,
    "safety_risk": 0.18374156951904297,
    "score": 0.33164969086647034,
    "selectivity": 0.8213396668434143,
    "virtual_spectrum_summary": 0.12011469900608063,
    "yield": 0.593376874923706
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

1. Scope and evidence base

This interpretation is based only on the 12 completed campaign batches. Every batch used 0.040 mol reagent, 0.005 mol catalyst, 0.080 L solvent, 600 rpm stirring, one heating operation, an HPLC measurement, quenching, termination, and a final assay. Consequently, the campaign identifies effects of catalyst identity, solvent identity, temperature, and heating time within that fixed recipe; it does not identify concentration, catalyst-loading, mixing, addition-order, or scale effects.

All reported catalysts are anonymous benchmark formulations. The solvent names are real identities, but their effects in this world are categorical benchmark effects rather than claims about real chemical behavior.

2. Proposed reaction network

The observations are consistent with a limiting reactant R forming target product P while competing and secondary pathways produce byproduct B and degradation material D:

R --kP--> P
R --kB--> B
P --kD--> B and/or D

A useful approximate model is:

dR/dt = -(kP + kB)R
dP/dt = kP R - kD P

with each rate constant depending on catalyst, solvent, and temperature. A conventional representation would be

ki = Ai(catalyst, solvent) exp[-Ei/(RT)].

Conversion is X = 1 - R/R0. Selectivity is approximately the fraction of converted material remaining as target, and yield follows approximately

Y ≈ X × S.

This relation is strongly supported by the final assays. For example, batch 11 gave X = 0.7877 and S = 0.7892, whose product is about 0.622, close to the observed yield of 0.6148. Batch 2 gave 0.7962 × 0.7302 ≈ 0.581, close to its observed yield of 0.5899. Deviations of roughly one percentage point are compatible with the independent assay-channel noise and mass-balance proxies.

The important qualitative feature is that the desired and undesired pathways do not respond identically to process severity. Raising temperature or extending time accelerates conversion, but sufficiently severe exposure lowers selectivity and raises both the byproduct and degradation signals. Thus conversion alone is not an adequate optimization target.

3. Catalyst effects

Batches 1-4 compared catalysts A-D under otherwise matched acetonitrile, 340 K target, 3600 s conditions.

- Batch 1, Catalyst A: conversion 0.4955, selectivity 0.6442, yield 0.3300, byproduct 0.1601, degradation 0.0367, final risk 0.1520, score 0.1742.
- Batch 2, Catalyst B: conversion 0.7962, selectivity 0.7302, yield 0.5899, byproduct 0.2173, degradation 0.1541, final risk 0.1860, score 0.3144.
- Batch 3, Catalyst C: conversion 0.6466, selectivity 0.7261, yield 0.4698, byproduct 0.1858, degradation 0.0675, final risk 0.1683, score 0.2584.
- Batch 4, Catalyst D: conversion 0.5780, selectivity 0.7479, yield 0.4500, byproduct 0.1388, degradation 0.0569, final risk 0.1651, score 0.2505.

Catalyst B is therefore the strongest kinetic catalyst in the tested regime. It generated substantially greater conversion and target yield than A, C, or D, although it also generated more heat-associated risk and more degradation than C or D. Catalyst D appears intrinsically more selective or less prone to the main byproduct pathway, but its lower conversion kept its score below that of B. Catalyst A was both slow and relatively unselective.

The heat-operation risk increment also depended on catalyst. At the matched 340 K condition, the risk after heating was approximately 0.1567 for A, 0.1907 for B, 0.1729 for C, and 0.1698 for D. Since catalyst addition itself did not visibly increase risk, this pattern suggests that reaction rate or reaction heat is coupled to the thermal-risk state rather than risk being a static catalyst hazard.

4. Solvent effects and catalyst-solvent coupling

Batches 2 and 5-7 compared solvents using Catalyst B at 340 K for 3600 s.

- Batch 5, water: conversion 0.5701, selectivity 0.8150, yield 0.4514, byproduct 0.1200, degradation 0.0299, final risk 0.1237, score 0.2856.
- Batch 6, ethanol: conversion 0.6706, selectivity 0.7484, yield 0.5278, byproduct 0.1681, degradation 0.0671, final risk 0.1547, score 0.2957.
- Batch 2, acetonitrile: conversion 0.7962, selectivity 0.7302, yield 0.5899, byproduct 0.2173, degradation 0.1541, final risk 0.1860, score 0.3144.
- Batch 7, toluene: conversion 0.7033, selectivity 0.6309, yield 0.4313, byproduct 0.2675, degradation 0.1074, final risk 0.1832, score 0.2182.

Water provided the safest and cleanest chemistry but reduced the rate sufficiently that its yield and score were below those of acetonitrile. Ethanol was intermediate. Acetonitrile gave the best productivity and matched-condition score, despite its larger byproduct, degradation, and risk values. Toluene was unfavorable: conversion was appreciable, but selectivity collapsed and the byproduct signal was the largest in this solvent comparison.

A plausible interpretation is that solvent changes both the productive rate coefficient and the branching ratio between productive and side reactions. A single solvent multiplier on all rates would not explain the data: water and toluene differ strongly in selectivity at comparable moderate conversion, so solvent must influence at least one selectivity-determining step.

5. Temperature and time dependence

Batches 2 and 8-12 explored thermal severity with Catalyst B in acetonitrile.

- Batch 2: 340 K, 3600 s; X 0.7962, S 0.7302, Y 0.5899, degradation 0.1541, score 0.3144.
- Batch 8: 360 K, 3600 s; X 0.9039, S 0.6893, Y 0.6330, degradation 0.2120, score 0.3277.
- Batch 9: 380 K, 3600 s; X 0.9557, S 0.6459, Y 0.6252, degradation 0.2733, score 0.3161.
- Batch 10: 360 K, 7200 s; X 0.9908, S 0.4773, Y 0.4592, degradation 0.4542, score 0.2133.
- Batch 11: 360 K, 2400 s; X 0.7877, S 0.7892, Y 0.6148, degradation 0.1054, score 0.3378.
- Batch 12: 370 K, 1800 s; X 0.7165, S 0.8213, Y 0.5934, degradation 0.0970, score 0.3316.

At 360 K, conversion behaves strikingly like a pseudo-first-order process. Using kobs = -ln(1-X)/t gives approximately 6.5×10^-4 s^-1 for batch 11, batch 8, and batch 10 despite their different durations. This internal consistency supports a first-order or pseudo-first-order reactant-consumption model over this range.

Selectivity does not remain constant at 360 K: it fell from 0.789 at 2400 s to 0.689 at 3600 s and 0.477 at 7200 s. Meanwhile, degradation rose from 0.105 to 0.212 and then 0.454. This is the clearest evidence for a secondary time-dependent loss of target product, although a time-dependent shift in catalyst selectivity is a viable alternative.

Increasing the target from 340 to 360 K increased useful conversion enough to improve score. Increasing it further to 380 K produced only a small yield change while increasing byproduct and degradation. The 7200 s experiment demonstrates that pursuing complete conversion is actively harmful in this world: batch 10 had the highest conversion but one of the poorest optimized-series scores.

Batch 12 shows the other side of the optimum. At 370 K for only 1800 s, selectivity was excellent and degradation remained modest, but conversion and yield were slightly too low to beat batch 11. The best observed compromise was therefore around the batch-11 severity: a 360 K boundary target for 2400 s.

The reported temperatures are control targets rather than proof of uniform instantaneous bulk temperature. Recorded heat-operation temperature rises were about 57.6 K in batch 11, 66.4 K in batch 12, and 74.7 K in batch 9. Thermal ramping and lag can explain why the 370 K/1800 s batch does not follow a simple isothermal Arrhenius extrapolation from the 360 K batches.

6. Safety behavior and quenching

All completed batches respected the safety limit of 0.35. The largest observed pre-quench risk was approximately 0.2288 in batch 9, leaving substantial margin to the limit. Batch 11 had pre-quench risk 0.1971 and final risk 0.1871. Batch 12 had final risk 0.1837. Quenching consistently cooled the system and reduced the reported risk without materially changing the already measured composition.

Risk appears to contain at least three components:

risk ≈ solvent/setup contribution + reaction/thermal contribution - cooling/quench relief.

The solvent/setup contribution was visible before heating, while the heating increment depended on catalyst, solvent, target temperature, and exposure. Risk is therefore coupled to reaction progress and thermal state, not merely to the selected heater setpoint. I did not observe evidence of a sharp runaway threshold within the explored region, but no experiment approached the declared limit closely enough to rule out nonlinear behavior at higher temperatures, concentrations, or scale.

7. Interpretation of the public score

The exact scoring equation was not exposed. Empirically, score increases with useful yield and selectivity and decreases with safety risk, byproduct, degradation, and cost-related penalties. All catalyst-containing batches displayed the same high-cost flag or cost ceiling, so this campaign cannot separate the detailed cost function from catalyst loading.

The score is clearly not a conversion metric. Batch 10 had conversion 0.9908 but score 0.2133, whereas batch 11 had conversion 0.7877 and score 0.3378. The optimization is therefore governed by a balance among target yield, selectivity, degradation, and safety rather than by conversion alone.

8. Measurement consistency

The intermediate HPLC measurements generally agreed with the final assays. For batch 11, HPLC gave conversion 0.7844, selectivity 0.7829, yield 0.6267, and byproduct 0.1913; the final assay gave 0.7877, 0.7892, 0.6148, and 0.1775. These differences are small relative to the campaign-wide effects.

Some batches showed larger channel-to-channel differences. For example, batch 4 had HPLC selectivity 0.8076 but final-assay selectivity 0.7479. I interpret such isolated discrepancies as synthetic instrument noise, channel calibration differences, or process uncertainty rather than evidence of composition changing after quench. There were no replicate batches, so repeatability cannot be estimated independently.

9. Recommended operating interpretation

Within the explored fixed recipe, the best supported operating region is:

- Catalyst B, 0.005 mol;
- acetonitrile, 0.080 L;
- reagent, 0.040 mol;
- 600 rpm;
- 360 K target for about 2400 s;
- prompt quench, then termination.

This is the sealed recommendation corresponding to batch 11. It achieved the highest observed final score, 0.3378, with yield 0.6148, selectivity 0.7892, conversion 0.7877, and final risk 0.1871. Batch 12 is a reasonable competing low-severity condition, with higher selectivity and slightly lower risk but lower yield and score.

10. Limits of identification and competing explanations

The proposed network is not uniquely identified. The decrease in selectivity with time may arise from sequential degradation of P, continued parallel production of B as R becomes depleted, catalyst transformation, or a temperature-dependent analytical response. The simultaneous rise in degradation warning makes secondary product loss the most economical explanation, but it is not proven by species-resolved time-course data.

Catalyst B may possess a larger intrinsic productive rate constant, or it may simply reach a different temperature trajectory through stronger reaction heat. Because temperature histories were not measured continuously, kinetic and thermal feedback effects cannot be fully separated.

Solvent effects may reflect changes in productive kinetics, side-reaction kinetics, catalyst state, heat transfer, or the benchmark's categorical solvent coupling. The experiment set does not isolate these mechanisms.

Only one catalyst loading, reagent concentration, liquid volume, stirring speed, operation order, and quench policy were tested. Extrapolation outside 0.040 mol reagent in 0.080 L solvent, 0.005 mol catalyst, 600 rpm, and approximately 340-380 K targets is speculative. In particular, the safety behavior should not be extrapolated to greater concentration, volume, or thermal severity.

Finally, the numerical measurements are outputs of bounded synthetic benchmark instruments. They support an internally consistent model of this world, not a claim about a named real reaction or real catalyst system.

## Q — Blind predictions

### Overall rationale

Predictions use the campaign-supported pseudo-first-order reactant-consumption model coupled to a slower secondary loss of target product. Catalyst B in acetonitrile is retained across all queries, but these batches use a higher catalyst and reagent concentration than the campaign and temperatures up to 460 K, so extrapolation uncertainty is substantial. Conversion was extrapolated from the observed temperature-dependent rate; selectivity and byproduct were extrapolated from their strong dependence on thermal residence time. Yield was constrained to remain approximately conversion times selectivity. Quenching was treated as changing safety risk and score, not pre-quench composition. Safety intervals are deliberately wide because scale, concentration, 400 rpm mixing, and temperatures above the studied 380 K range were not independently identified.

### Q01

At 420 K for 3300 s, the higher catalyst concentration should drive nearly complete conversion, but extrapolation of the observed secondary-loss trend predicts extensive byproduct formation. Without quenching, the terminal thermal-risk component remains present.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6700 | 0.5100 | 0.8200 |
| conversion | 0.9980 | 0.9600 | 1.0000 |
| safety_risk | 0.2500 | 0.1700 | 0.3500 |
| score | 0.1200 | 0.0300 | 0.2300 |
| selectivity | 0.3200 | 0.1700 | 0.4800 |
| yield | 0.3100 | 0.1600 | 0.4700 |

### Q02

The chemical trajectory is the same as Q01, so conversion and composition are predicted to be essentially unchanged. Quenching should principally remove the reversible hot-state risk component, modestly improving safe score.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6700 | 0.5100 | 0.8200 |
| conversion | 0.9980 | 0.9600 | 1.0000 |
| safety_risk | 0.1700 | 0.1000 | 0.2600 |
| score | 0.1500 | 0.0500 | 0.2700 |
| selectivity | 0.3200 | 0.1700 | 0.4800 |
| yield | 0.3100 | 0.1600 | 0.4700 |

### Q03

The lower 390 K target should suppress secondary loss relative to Q01, while 3300 s and the high catalyst concentration still imply very high conversion. This resembles a more severe version of the long 360 K campaign runs.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5100 | 0.3600 | 0.6700 |
| conversion | 0.9870 | 0.9100 | 1.0000 |
| safety_risk | 0.1800 | 0.1200 | 0.2700 |
| score | 0.2200 | 0.1000 | 0.3300 |
| selectivity | 0.4800 | 0.3200 | 0.6300 |
| yield | 0.4700 | 0.3100 | 0.6200 |

### Q04

A 450 K, 3300 s exposure is well beyond the campaign range. Reactant depletion should be complete, but the product pool is expected to undergo extensive secondary conversion. The safety interval crosses the declared 0.35 limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8200 | 0.6700 | 0.9400 |
| conversion | 1.0000 | 0.9800 | 1.0000 |
| safety_risk | 0.3600 | 0.2500 | 0.4900 |
| score | 0.0500 | 0.0000 | 0.1500 |
| selectivity | 0.1700 | 0.0500 | 0.3200 |
| yield | 0.1700 | 0.0500 | 0.3100 |

### Q05

The short 1500 s exposure should exploit rapid productive conversion at 420 K while limiting the residence time available for product degradation. This is predicted to be the strongest member of the blind set, though it is an extrapolation above the studied temperature range.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2500 | 0.1300 | 0.4000 |
| conversion | 0.9500 | 0.8200 | 0.9950 |
| safety_risk | 0.2000 | 0.1300 | 0.2900 |
| score | 0.3400 | 0.2300 | 0.4300 |
| selectivity | 0.7300 | 0.5800 | 0.8400 |
| yield | 0.6900 | 0.5500 | 0.7900 |

### Q06

Extending the 420 K exposure to 5100 s should add little conversion after early reactant depletion but substantially increase secondary product loss. Risk is also higher, with meaningful probability of approaching or exceeding the safety limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8500 | 0.7000 | 0.9600 |
| conversion | 1.0000 | 0.9850 | 1.0000 |
| safety_risk | 0.2700 | 0.1800 | 0.3800 |
| score | 0.0500 | 0.0000 | 0.1500 |
| selectivity | 0.1400 | 0.0300 | 0.2900 |
| yield | 0.1400 | 0.0300 | 0.2800 |

### Q07

The initial 390 K stage should create a substantial product pool, which is then exposed to 450 K during the second stage. Under the proposed sequential-loss mechanism this ordering is particularly damaging, and the final hot state also raises safety risk.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8100 | 0.6400 | 0.9400 |
| conversion | 1.0000 | 0.9700 | 1.0000 |
| safety_risk | 0.3500 | 0.2400 | 0.4900 |
| score | 0.0500 | 0.0000 | 0.1600 |
| selectivity | 0.1800 | 0.0500 | 0.3500 |
| yield | 0.1800 | 0.0500 | 0.3400 |

### Q08

The 450 K first stage should cause rapid conversion and appreciable damage, but the subsequent 390 K stage is less destructive than ending with the hot stage in Q07. Cooling toward the second target should also lower terminal risk, although accumulated chemical damage remains.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7300 | 0.5500 | 0.8900 |
| conversion | 1.0000 | 0.9700 | 1.0000 |
| safety_risk | 0.2700 | 0.1800 | 0.4000 |
| score | 0.1000 | 0.0100 | 0.2300 |
| selectivity | 0.2600 | 0.1000 | 0.4400 |
| yield | 0.2600 | 0.1000 | 0.4300 |

### Q09

The 1500 s duration limits secondary loss, but 440 K should be less selective and riskier than Q05. Conversion is predicted to be almost complete, with a final profile broadly comparable to campaign batch 9 but at shorter duration and higher catalyst concentration.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3500 | 0.2000 | 0.5200 |
| conversion | 0.9800 | 0.8900 | 1.0000 |
| safety_risk | 0.2500 | 0.1600 | 0.3600 |
| score | 0.2800 | 0.1600 | 0.3900 |
| selectivity | 0.6300 | 0.4600 | 0.7700 |
| yield | 0.6100 | 0.4500 | 0.7300 |

### Q10

Composition should match Q09 because quenching follows the same reaction exposure. Quenching is predicted to reduce the terminal hot-state risk and therefore improve safe score without materially restoring degraded product.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3500 | 0.2000 | 0.5200 |
| conversion | 0.9800 | 0.8900 | 1.0000 |
| safety_risk | 0.1700 | 0.1000 | 0.2700 |
| score | 0.3100 | 0.1900 | 0.4200 |
| selectivity | 0.6300 | 0.4600 | 0.7700 |
| yield | 0.6100 | 0.4500 | 0.7300 |

### Q11

Although 370 K is the mildest target in the blind set, 5700 s is long enough to approach complete conversion and permit substantial secondary loss. The prediction lies between campaign batch 10's severe long hold and the cleaner short batch 12 condition.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6200 | 0.4500 | 0.7800 |
| conversion | 0.9970 | 0.9500 | 1.0000 |
| safety_risk | 0.1800 | 0.1100 | 0.2800 |
| score | 0.1600 | 0.0600 | 0.2800 |
| selectivity | 0.3700 | 0.2100 | 0.5400 |
| yield | 0.3700 | 0.2000 | 0.5300 |

### Q12

This combines the highest temperature with the longest exposure and no quench. Conversion should saturate early, followed by near-complete loss of target to byproduct or degradation channels. A safety-limit violation is more likely than not, so the expected score is near zero.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9600 | 0.8500 | 1.0000 |
| conversion | 1.0000 | 0.9950 | 1.0000 |
| safety_risk | 0.4800 | 0.3400 | 0.6500 |
| score | 0.0050 | 0.0000 | 0.0400 |
| selectivity | 0.0350 | 0.0000 | 0.1400 |
| yield | 0.0350 | 0.0000 | 0.1400 |

## K2 — Retrospective analysis

1. Assessment of the initial information

The initial material packet made almost no substantive kinetic or mechanistic claim. It explicitly said that no task-specific property dossier was available, that the catalysts were anonymous benchmark formulations, and that solvent effects were categorical world-specific effects rather than predictions from real solvent chemistry. Consequently, there was no initial proposed mechanism to confirm or falsify.

Several structural claims in the packet were supported:

- Catalyst identity mattered strongly. Under the matched batch 1-4 comparison, Catalyst B produced much greater conversion and yield than A, C, or D. This is consistent with the stated “latent categorical activity profile,” although that label did not predict which catalyst would be best.
- Solvent identity mattered categorically. Batches 2 and 5-7 produced clearly different conversion, selectivity, byproduct, risk, and score outcomes. Again, the packet predicted that a coupling existed but not its direction.
- The instruments behaved as noisy, non-identical channels. For example, batch 4 had HPLC selectivity 0.8076 and final-assay selectivity 0.7479. The campaign therefore supported the warning that processed estimates have channel-specific uncertainty rather than constituting exact hidden-state readouts.
- The declared safety limit of 0.35 was operationally relevant, but every completed campaign batch stayed below it. The highest observed pre-quench risk was about 0.2288 in batch 9. This is only an absence of a violation in the explored region; it is not evidence that more severe conditions are universally safe.

No evidence contradicted the packet’s warning against interpreting the benchmark as a real named reaction. I did not attempt such an identification.

Several important matters remained untested: whether effects scale with catalyst concentration, reagent concentration, liquid volume, or stirring; whether the risk model is extensive or concentration-based; and whether solvent and catalyst effects transfer between worlds. The campaign also did not test temperatures above 380 K. K1 acknowledged these limitations, but the later blind predictions necessarily extrapolated beyond them.

There is one important distinction between “no counterevidence” and “counterevidence not acted on.” For the proposed pseudo-first-order consumption model, the three 360 K batches were mutually consistent, so there was no clear counterevidence within that slice. For a simple model in which selectivity is fixed by catalyst and solvent, however, batches 8, 10, and 11 were direct counterevidence: selectivity changed greatly with residence time. I did revise the final K1 explanation toward secondary product loss. Earlier in the campaign, before batch 10, I had not yet explicitly made that revision.

2. Experiments that formed or changed the interpretation

Batch 1 established a practical baseline rather than confirming an existing theory. Catalyst A in acetonitrile at 340 K for 3600 s gave only 0.4955 conversion, 0.3300 yield, and score 0.1742. The initial selection of acetonitrile, Catalyst A, 340 K, and 3600 s was largely an unvalidated guess made to obtain a moderate, presumably safe starting point.

Batch 2 was the first major change in belief. Changing only to Catalyst B increased conversion to 0.7962, yield to 0.5899, and score to 0.3144. This caused Catalyst B to become the main platform for later experiments. Batches 3 and 4 showed that C and D were intermediate: D had comparatively favorable selectivity and byproduct but insufficient conversion. Those experiments supported a catalyst-dependent rate/selectivity tradeoff rather than a one-dimensional catalyst ranking.

Batches 5-7 formed the solvent interpretation. Water in batch 5 was safest and cleanest but slower; ethanol in batch 6 was intermediate; acetonitrile retained the best matched-condition score; and toluene in batch 7 produced poor selectivity and a large byproduct signal. These experiments justified continuing with acetonitrile for score optimization.

Batch 8 showed that increasing the target from 340 to 360 K could improve yield and score despite greater degradation. Batch 9 showed diminishing returns at 380 K: conversion rose to 0.9557, but score fell relative to batch 8 as byproduct and degradation increased.

Batch 10 changed the mechanism most decisively. At 360 K for 7200 s, conversion reached 0.9908 while selectivity fell to 0.4773, degradation rose to 0.4542, and score fell to 0.2133. This falsified any working assumption that maximizing conversion would maximize performance. It motivated the sequential-loss term in K1.

Batch 11 was chiefly an optimization experiment informed by batches 8-10. Shortening the 360 K exposure to 2400 s produced the best observed score, 0.3378. Batch 12 then tested a hotter and shorter alternative, 370 K for 1800 s. Its higher selectivity but lower conversion and score supported, but did not prove, a local compromise near batch 11.

Thus, the early catalyst and solvent screens were data-driven identification experiments after an initially guessed baseline. The late temperature/time choices depended on accumulated data. The exact choices of 360 K/2400 s and 370 K/1800 s were still heuristic; no fitted optimizer or predeclared kinetic model selected them.

3. Principal competing mechanisms and what the campaign distinguishes

K1 proposed parallel formation plus secondary target loss:

R → P, R → B, and P → B or D.

The leading competitor is a purely parallel network in which R forms P and B, but the branching fraction itself changes with time because of catalyst transformation, reactant depletion, or a changing thermal state. That model can reproduce declining apparent selectivity without literal degradation of P.

Another competitor is thermal-history heterogeneity. A nominal 360 K operation is not necessarily an isothermal exposure: heating ramps, reaction heat, and controller lag may make the apparent time dependence a temperature-history effect. The recorded temperature increments support the existence of thermal dynamics, but continuous temperature traces were unavailable.

A further possibility is that the “degradation warning” and “byproduct signal” are partially overlapping proxies rather than separate material pools. The final assay does not publicly identify hidden species, so the campaign cannot establish a unique stoichiometric network.

The campaign can distinguish several coarse features:

- Productive conversion is strongly catalyst-, solvent-, temperature-, and time-dependent.
- At 360 K with Catalyst B and acetonitrile, reactant disappearance is compatible with pseudo-first-order behavior across 2400, 3600, and 7200 s.
- Selectivity is not constant over those residence times.
- Severe exposure harms final score even when it increases conversion.

It cannot distinguish uniquely among secondary P degradation, time-varying parallel selectivity, catalyst aging, or thermal-history effects. Nor can it separate intrinsic Catalyst B kinetics from reaction-heat feedback, because catalyst identity and heat generation were not independently controlled. The blind Q07/Q08 order predictions were consequences of the sequential-loss hypothesis, not additional evidence for it; no prediction truth has been revealed.

4. One additional complete experiment

I would run one time-resolved batch at the batch-11 composition: 0.080 L acetonitrile, 0.040 mol reagent, 0.005 mol Catalyst B, and 600 rpm. I would heat at a 360 K target in three successive 1200 s segments, taking an HPLC measurement after each segment, then quench, terminate, and obtain the required final assay. The small HPLC sample consumption would be recorded explicitly.

This experiment is more discriminating than another single endpoint because it would observe the same vessel at approximately 1200, 2400, and 3600 s, reducing between-batch variability.

Possible outcomes would change my judgment as follows:

- If conversion rose approximately exponentially while target amount first rose and then declined, with byproduct or degradation increasing as target declined, that would strongly favor genuine sequential product loss.
- If target amount rose monotonically but target selectivity decreased only because later reactant conversion increasingly favored byproduct, that would favor a time-varying parallel branching mechanism.
- If the first 1200 s already showed most conversion and later segments mainly increased degradation, the batch-11 optimum would be interpreted as being on the descending side of a product maximum, suggesting an even shorter optimum.
- If all three measurements retained nearly constant selectivity and degradation, the cross-batch trend would look more like batch variability, thermal-history variation, or channel bias; confidence in K1’s sequential-loss interpretation would decrease.
- If HPLC time points and the final assay differed systematically beyond their declared uncertainties, I would give greater weight to channel calibration or sampling explanations.

This design still would not prove molecular identities or fully separate thermal and chemical effects, because it lacks a continuous internal-temperature trace and an authentic isolated-product challenge.

5. Tradeoff between mechanistic identifiability and score optimization

The study began with a relatively identifiable one-factor-at-a-time structure. Batches 1-4 held solvent and thermal conditions fixed while screening catalyst, and batches 2 and 5-7 held Catalyst B and thermal conditions fixed while screening solvent. These choices sacrificed some expected score because A, C, D, water, ethanol, and toluene were retained long enough to characterize them after Catalyst B/acetonitrile had begun to look favorable.

Batch 10 was also primarily informative rather than score-seeking. A 7200 s hold was a deliberately severe boundary test; it produced a poor score but revealed that near-complete conversion was undesirable. That information was central to K1.

After batch 7, the design increasingly favored optimization. Batches 8-12 concentrated on Catalyst B/acetonitrile and adjusted temperature and duration. This improved the best score but weakened broad mechanistic identifiability: there were no matched time series for the other catalysts or solvents, no catalyst-loading series, and no replication.

The safe-score research goal strongly encouraged operation below the 0.35 risk limit and favored conditions likely to improve yield without exploring hazardous extremes. That was appropriate operationally but left the shape of the safety response near the constraint unidentified. Similarly, using maximum reagent, solvent, and catalyst allocations in every batch simplified comparisons and supported score, but eliminated dose-response information.

In short, early batches sacrificed score for categorical identification, batch 10 sacrificed score for severity information, and the last two batches sacrificed broader identification for local score improvement.

6. Underused evidence and weaknesses in the blind predictions

The raw characterization artifacts were not fully exploited. I used processed estimates and a few reported peaks, but I did not quantitatively compare complete chromatographic or multichannel spectral shapes across batches. Such comparison might have revealed whether the byproduct and degradation proxies represented distinct evolving features.

The paired HPLC/final-assay observations were also underused. K1 mentioned their general agreement and the batch-4 discrepancy, but I did not fit a channel-bias or measurement-error model. Consequently, the apparent kinetic consistency at 360 K was treated more precisely than the unreplicated data justified.

Risk-operation deltas and realized temperature changes could have supported a quantitative thermal-risk model. Instead, K1 used only a qualitative additive decomposition. The public score likewise was not fitted quantitatively, although the campaign supplied enough endpoints for a provisional empirical relationship.

The least reliable blind predictions are Q12, Q04, Q07, and Q08. They extrapolate to 450-460 K, beyond the campaign maximum of 380 K. Q07 and Q08 additionally require an untested claim about heat-stage ordering and thermal memory. Q12 combines the largest extrapolation in temperature and duration, so its near-zero target prediction and likely safety violation are especially speculative.

Q01/Q02 and Q06 are also weak because 420 K was untested and the scale changed from 0.080 L to 0.005 L. Q01 versus Q02 and Q09 versus Q10 rely on extrapolating how quenching partitions reversible hot-state risk from accumulated risk.

Several intervals were probably too narrow given these limitations. In particular:

- Q01 conversion [0.96, 1.00] and Q04 conversion [0.98, 1.00] express too much confidence in high-temperature kinetic extrapolation.
- Q05 yield [0.55, 0.79] and selectivity [0.58, 0.84] may be too narrow because the prediction combines higher temperature, higher catalyst concentration, smaller volume, and lower stirring speed.
- Q09/Q10 composition intervals may likewise understate uncertainty.
- Safety intervals for nearly every query may be too narrow because K1 never identified whether risk scales with amount, concentration, vessel volume, instantaneous temperature, or accumulated exposure.

This is partly inconsistent with K1’s explicit scope statement that extrapolation outside 0.040 mol reagent, 0.080 L solvent, 0.005 mol catalyst, 600 rpm, and 340-380 K was speculative. The blind-prediction rationale did acknowledge “substantial” extrapolation uncertainty, but some numerical intervals did not fully honor that warning. With no truth feedback, this is a calibration critique, not a claim that any particular point prediction is wrong.

7. Limitations of the sealed recommendation

Batch 11 is the sample-in highest-scoring batch, not a proven optimum. Its score of 0.3378 exceeded batch 12 at 0.3316 and batch 8 at 0.3277, but those differences are modest relative to process variability and assay uncertainty. Each condition was run only once. Ranking noise could therefore change the apparent winner.

The recommendation is conditional on the tested recipe, operation order, vessel model, and benchmark world. It also carries the high-cost flag associated with the chosen catalyst loading. The “360 K” value is a boundary target, not proof that every part of the batch followed a uniform 360 K trajectory.

Repeatability should first be tested with several independent exact replicates of batch 11, reporting the distribution of final score, risk, yield, selectivity, and degradation rather than only their means. The final recommendation should be reconsidered if the lower tail approaches unacceptable performance or if batch-to-batch ranking is unstable.

Local robustness should then be tested with a small designed neighborhood around batch 11, for example 350-370 K, 1800-3000 s, modest changes in stirring, and at least two Catalyst B loadings. The aim would be to determine whether batch 11 lies on a broad plateau or a narrow peak and whether plausible control errors preserve the safety margin.

Robustness to quench timing should also be assessed because prompt quenching was part of the recommended procedure. Delays may reduce selectivity even if the nominal heating program is unchanged.

Cross-material generalization would require repeating the local design with the other catalysts and solvents; the current data do not show that the same time-temperature optimum applies to them. Cross-world generalization is even less justified because the catalysts are anonymous latent benchmark profiles and solvent coupling is world-specific. A procedure should therefore be described as “best observed in this campaign and world,” not as universally optimal.

The correct final claim is limited: batch 11 was the highest observed completed experiment among 12 tested batches and respected the declared safety constraint. The campaign did not prove global optimality, exact local optimality, repeatability, or transferability.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 104.9 | none | 0 |
| Q | yes | 0 | 104.4 | none | 0 |
| K2 | yes | 0 | 113.1 | none | 0 |

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean 80% width | Mean interval score |
|---|---:|---:|---:|---:|
| byproduct_signal | 0.1770 | 0.4167 | 0.2908 | 0.7689 |
| conversion | 0.0067 | 1.0000 | 0.0596 | 0.0596 |
| safety_risk | 0.0507 | 0.8333 | 0.2008 | 0.2230 |
| score | 0.1207 | 0.2500 | 0.1875 | 0.4271 |
| selectivity | 0.1974 | 0.3667 | 0.2875 | 0.8877 |
| yield | 0.2042 | 0.1667 | 0.2775 | 0.9586 |

## Predictions versus released reference truth

### Q01

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.6700 | 0.5100 | 0.8200 | 0.4503 | 0.4469, 0.4662, 0.4467, 0.4450, 0.4467 |
| conversion | 0.9980 | 0.9600 | 1.0000 | 0.9938 | 1.0000, 1.0000, 0.9860, 0.9873, 0.9956 |
| safety_risk | 0.2500 | 0.1700 | 0.3500 | 0.2983 | 0.2983, 0.2983, 0.2983, 0.2983, 0.2983 |
| score | 0.1200 | 0.0300 | 0.2300 | 0.2654 | 0.2635, 0.2685, 0.2680, 0.2631, 0.2639 |
| selectivity | 0.3200 | 0.1700 | 0.4800 | 0.5546 | 0.5563, 0.5738, 0.5478, 0.5381, 0.5570 |
| yield | 0.3100 | 0.1600 | 0.4700 | 0.5493 | 0.5420, 0.5435, 0.5619, 0.5554, 0.5436 |
### Q02

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.6700 | 0.5100 | 0.8200 | 0.4565 | 0.4617, 0.4629, 0.4545, 0.4442, 0.4594 |
| conversion | 0.9980 | 0.9600 | 1.0000 | 1.0000 | 1.0000, 1.0000, 1.0000, 1.0000, 1.0000 |
| safety_risk | 0.1700 | 0.1000 | 0.2600 | 0.1511 | 0.1511, 0.1511, 0.1511, 0.1511, 0.1511 |
| score | 0.1500 | 0.0500 | 0.2700 | 0.3276 | 0.3307, 0.3368, 0.3227, 0.3239, 0.3239 |
| selectivity | 0.3200 | 0.1700 | 0.4800 | 0.5523 | 0.5540, 0.5733, 0.5405, 0.5400, 0.5537 |
| yield | 0.3100 | 0.1600 | 0.4700 | 0.5474 | 0.5539, 0.5572, 0.5426, 0.5458, 0.5372 |
### Q03

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5100 | 0.3600 | 0.6700 | 0.3766 | 0.3794, 0.3709, 0.3819, 0.3900, 0.3609 |
| conversion | 0.9870 | 0.9100 | 1.0000 | 0.9967 | 1.0000, 1.0000, 0.9889, 1.0000, 0.9944 |
| safety_risk | 0.1800 | 0.1200 | 0.2700 | 0.1857 | 0.1857, 0.1857, 0.1857, 0.1857, 0.1857 |
| score | 0.2200 | 0.1000 | 0.3300 | 0.3684 | 0.3706, 0.3671, 0.3652, 0.3719, 0.3673 |
| selectivity | 0.4800 | 0.3200 | 0.6300 | 0.6293 | 0.6322, 0.6263, 0.6308, 0.6343, 0.6231 |
| yield | 0.4700 | 0.3100 | 0.6200 | 0.6327 | 0.6355, 0.6305, 0.6258, 0.6375, 0.6344 |
### Q04

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.8200 | 0.6700 | 0.9400 | 0.5283 | 0.5341, 0.5287, 0.5215, 0.5298, 0.5274 |
| conversion | 1.0000 | 0.9800 | 1.0000 | 0.9965 | 1.0000, 0.9988, 0.9941, 1.0000, 0.9895 |
| safety_risk | 0.3600 | 0.2500 | 0.4900 | 0.4035 | 0.4035, 0.4035, 0.4035, 0.4035, 0.4035 |
| score | 0.0500 | 0.0000 | 0.1500 | 0.1753 | 0.1761, 0.1753, 0.1756, 0.1755, 0.1738 |
| selectivity | 0.1700 | 0.0500 | 0.3200 | 0.4844 | 0.4790, 0.4868, 0.4792, 0.4926, 0.4847 |
| yield | 0.1700 | 0.0500 | 0.3100 | 0.4854 | 0.4900, 0.4836, 0.4902, 0.4801, 0.4833 |
### Q05

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2500 | 0.1300 | 0.4000 | 0.2240 | 0.2127, 0.2190, 0.2346, 0.2243, 0.2295 |
| conversion | 0.9500 | 0.8200 | 0.9950 | 0.9780 | 0.9698, 0.9860, 0.9851, 0.9824, 0.9669 |
| safety_risk | 0.2000 | 0.1300 | 0.2900 | 0.2987 | 0.2987, 0.2987, 0.2987, 0.2987, 0.2987 |
| score | 0.3400 | 0.2300 | 0.4300 | 0.4067 | 0.4069, 0.4023, 0.4073, 0.4084, 0.4085 |
| selectivity | 0.7300 | 0.5800 | 0.8400 | 0.7769 | 0.7760, 0.7624, 0.7815, 0.7800, 0.7844 |
| yield | 0.6900 | 0.5500 | 0.7900 | 0.7642 | 0.7673, 0.7603, 0.7611, 0.7654, 0.7667 |
### Q06

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.8500 | 0.7000 | 0.9600 | 0.6220 | 0.6125, 0.6145, 0.6156, 0.6437, 0.6239 |
| conversion | 1.0000 | 0.9850 | 1.0000 | 0.9956 | 0.9990, 1.0000, 0.9906, 0.9940, 0.9944 |
| safety_risk | 0.2700 | 0.1800 | 0.3800 | 0.2979 | 0.2979, 0.2979, 0.2979, 0.2979, 0.2979 |
| score | 0.0500 | 0.0000 | 0.1500 | 0.1604 | 0.1639, 0.1597, 0.1587, 0.1595, 0.1599 |
| selectivity | 0.1400 | 0.0300 | 0.2900 | 0.3931 | 0.3923, 0.3900, 0.3880, 0.4025, 0.3925 |
| yield | 0.1400 | 0.0300 | 0.2800 | 0.3905 | 0.3990, 0.3897, 0.3908, 0.3829, 0.3901 |
### Q07

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.8100 | 0.6400 | 0.9400 | 0.4961 | 0.4975, 0.4926, 0.5053, 0.4934, 0.4915 |
| conversion | 1.0000 | 0.9700 | 1.0000 | 0.9933 | 0.9948, 0.9899, 0.9907, 0.9910, 1.0000 |
| safety_risk | 0.3500 | 0.2400 | 0.4900 | 0.4274 | 0.4274, 0.4274, 0.4274, 0.4274, 0.4274 |
| score | 0.0500 | 0.0000 | 0.1600 | 0.1786 | 0.1762, 0.1787, 0.1795, 0.1720, 0.1868 |
| selectivity | 0.1800 | 0.0500 | 0.3500 | 0.5091 | 0.4941, 0.5185, 0.5054, 0.5066, 0.5207 |
| yield | 0.1800 | 0.0500 | 0.3400 | 0.5068 | 0.5097, 0.5018, 0.5120, 0.4923, 0.5182 |
### Q08

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.7300 | 0.5500 | 0.8900 | 0.5022 | 0.5042, 0.5091, 0.4928, 0.4979, 0.5072 |
| conversion | 1.0000 | 0.9700 | 1.0000 | 0.9991 | 1.0000, 0.9954, 1.0000, 1.0000, 1.0000 |
| safety_risk | 0.2700 | 0.1800 | 0.4000 | 0.1973 | 0.1973, 0.1973, 0.1973, 0.1973, 0.1973 |
| score | 0.1000 | 0.0100 | 0.2300 | 0.2871 | 0.2870, 0.2882, 0.2802, 0.2860, 0.2941 |
| selectivity | 0.2600 | 0.1000 | 0.4400 | 0.5111 | 0.5264, 0.5157, 0.4835, 0.5021, 0.5279 |
| yield | 0.2600 | 0.1000 | 0.4300 | 0.5163 | 0.5063, 0.5171, 0.5160, 0.5190, 0.5232 |
### Q09

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3500 | 0.2000 | 0.5200 | 0.2551 | 0.2478, 0.2551, 0.2557, 0.2586, 0.2585 |
| conversion | 0.9800 | 0.8900 | 1.0000 | 0.9888 | 0.9803, 0.9874, 0.9938, 0.9911, 0.9914 |
| safety_risk | 0.2500 | 0.1600 | 0.3600 | 0.3780 | 0.3780, 0.3780, 0.3780, 0.3780, 0.3780 |
| score | 0.2800 | 0.1600 | 0.3900 | 0.3587 | 0.3576, 0.3632, 0.3586, 0.3556, 0.3583 |
| selectivity | 0.6300 | 0.4600 | 0.7700 | 0.7559 | 0.7496, 0.7587, 0.7564, 0.7553, 0.7596 |
| yield | 0.6100 | 0.4500 | 0.7300 | 0.7437 | 0.7471, 0.7537, 0.7420, 0.7358, 0.7399 |
### Q10

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3500 | 0.2000 | 0.5200 | 0.2502 | 0.2529, 0.2556, 0.2474, 0.2418, 0.2531 |
| conversion | 0.9800 | 0.8900 | 1.0000 | 0.9895 | 0.9937, 0.9834, 0.9945, 0.9943, 0.9816 |
| safety_risk | 0.1700 | 0.1000 | 0.2700 | 0.1718 | 0.1718, 0.1718, 0.1718, 0.1718, 0.1718 |
| score | 0.3100 | 0.1900 | 0.4200 | 0.4472 | 0.4450, 0.4479, 0.4492, 0.4470, 0.4470 |
| selectivity | 0.6300 | 0.4600 | 0.7700 | 0.7487 | 0.7486, 0.7516, 0.7418, 0.7498, 0.7516 |
| yield | 0.6100 | 0.4500 | 0.7300 | 0.7459 | 0.7395, 0.7473, 0.7538, 0.7433, 0.7454 |
### Q11

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.6200 | 0.4500 | 0.7800 | 0.5042 | 0.5026, 0.5049, 0.5110, 0.4947, 0.5079 |
| conversion | 0.9970 | 0.9500 | 1.0000 | 0.9947 | 0.9891, 0.9869, 1.0000, 0.9984, 0.9993 |
| safety_risk | 0.1800 | 0.1100 | 0.2800 | 0.1547 | 0.1547, 0.1547, 0.1547, 0.1547, 0.1547 |
| score | 0.1600 | 0.0600 | 0.2800 | 0.2976 | 0.2974, 0.3007, 0.2905, 0.2975, 0.3018 |
| selectivity | 0.3700 | 0.2100 | 0.5400 | 0.5042 | 0.5154, 0.5160, 0.4770, 0.5024, 0.5103 |
| yield | 0.3700 | 0.2000 | 0.5300 | 0.5044 | 0.4984, 0.5069, 0.5023, 0.5044, 0.5099 |
### Q12

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.9600 | 0.8500 | 1.0000 | 0.8008 | 0.7912, 0.7944, 0.8024, 0.8120, 0.8042 |
| conversion | 1.0000 | 0.9950 | 1.0000 | 0.9991 | 1.0000, 0.9954, 1.0000, 1.0000, 1.0000 |
| safety_risk | 0.4800 | 0.3400 | 0.6500 | 0.4203 | 0.4203, 0.4203, 0.4203, 0.4203, 0.4203 |
| score | 0.0050 | 0.0000 | 0.0400 | 0.0000 | 0.0000, 0.0000, 0.0000, 0.0000, 0.0000 |
| selectivity | 0.0350 | 0.0000 | 0.1400 | 0.2143 | 0.2309, 0.1960, 0.2230, 0.2062, 0.2153 |
| yield | 0.0350 | 0.0000 | 0.1400 | 0.2193 | 0.2180, 0.2146, 0.2252, 0.2157, 0.2233 |

## Recommendation retest

- Selected source batch: `11`
- Retest exact replay verified: `True`
- Retest failure: `none`

| Metric | Selected source batch | Independent retest | Retest minus source |
|---|---:|---:|---:|
| byproduct_signal | 0.1775 | 0.1797 | 0.0022 |
| conversion | 0.7877 | 0.7815 | -0.0062 |
| cost | 1.0000 | 1.0000 | 0.0000 |
| degradation_warning | 0.1054 | 0.1228 | 0.0173 |
| safety_risk | 0.1871 | 0.1871 | 0.0000 |
| score | 0.3378 | 0.3353 | -0.0025 |
| selectivity | 0.7892 | 0.7779 | -0.0112 |
| virtual_spectrum_summary | 0.1450 | 0.1541 | 0.0090 |
| yield | 0.6148 | 0.6172 | 0.0024 |

## Scope note

This is the final sanitized report produced after all 60 source sessions and K1/Q/K2 chains were sealed. It includes released reference truth, blind-prediction evaluation, and the independent recommendation retest. Provider-private event streams, credentials, thread identifiers, and token accounting remain excluded.
