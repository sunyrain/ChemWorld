# RX-W01--S--safety_constrained_optimization--Aligned

## Run summary

- World: `RX-W01`
- Locus: `S`
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
- Rationale: Batch 12 delivered the highest observed public safe score (0.2846) while its safety risk (0.2172) remained comfortably below the 0.35 limit.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S2 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 340 K x 3600 s @ 600 rpm | no | 0.2826 | 0.5344 | 0.5119 | 0.2259 | 0.0212 | 0.1544 | 0.1283 |
| 2 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 340 K x 3600 s @ 600 rpm | no | 0.4255 | 0.7201 | 0.5927 | 0.1775 | 0.0571 | 0.1678 | 0.2340 |
| 3 | S2 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 340 K x 3600 s @ 600 rpm | no | 0.2956 | 0.6057 | 0.4799 | 0.1926 | 0.0225 | 0.1544 | 0.1482 |
| 4 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 340 K x 3600 s @ 600 rpm | no | 0.3673 | 0.6746 | 0.5557 | 0.1797 | 0.0545 | 0.1637 | 0.1975 |
| 5 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 340 K x 3600 s @ 600 rpm | no | 0.2242 | 0.6349 | 0.3886 | 0.1311 | 0.0330 | 0.1054 | 0.1398 |
| 6 | S1 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 340 K x 3600 s @ 600 rpm | no | 0.3091 | 0.6474 | 0.4764 | 0.1738 | 0.0285 | 0.1380 | 0.1710 |
| 7 | S3 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 340 K x 3600 s @ 600 rpm | no | 0.3940 | 0.6584 | 0.5885 | 0.1979 | 0.0467 | 0.1781 | 0.2009 |
| 8 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 360 K x 3600 s @ 600 rpm | no | 0.5054 | 0.7151 | 0.7246 | 0.1974 | 0.0984 | 0.1856 | 0.2699 |
| 9 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 380 K x 3600 s @ 600 rpm | no | 0.5673 | 0.6841 | 0.8106 | 0.2662 | 0.1258 | 0.2116 | 0.2838 |
| 10 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 400 K x 3600 s @ 600 rpm | no | 0.6004 | 0.6757 | 0.8899 | 0.2891 | 0.1594 | 0.2607 | 0.2808 |
| 11 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 380 K x 2700 s @ 600 rpm | no | 0.5252 | 0.7449 | 0.7037 | 0.2020 | 0.0757 | 0.2035 | 0.2751 |
| 12 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 380 K x 4800 s @ 600 rpm | no | 0.5786 | 0.6449 | 0.8962 | 0.3308 | 0.1890 | 0.2172 | 0.2846 |

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
    "byproduct_signal": 0.2259444147348404,
    "conversion": 0.5118507146835327,
    "cost": 1.0,
    "degradation_warning": 0.0211945828050375,
    "safety_risk": 0.154388427734375,
    "score": 0.12834715843200684,
    "selectivity": 0.5344210267066956,
    "virtual_spectrum_summary": 0.1338069885969162,
    "yield": 0.28257906436920166
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
    "byproduct_signal": 0.17753982543945312,
    "conversion": 0.5926799178123474,
    "cost": 1.0,
    "degradation_warning": 0.05712241306900978,
    "safety_risk": 0.16782106459140778,
    "score": 0.2339859902858734,
    "selectivity": 0.720085084438324,
    "virtual_spectrum_summary": 0.12335199117660522,
    "yield": 0.4255405068397522
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
    "byproduct_signal": 0.19262167811393738,
    "conversion": 0.4798811674118042,
    "cost": 1.0,
    "degradation_warning": 0.022458814084529877,
    "safety_risk": 0.1544008105993271,
    "score": 0.1481645554304123,
    "selectivity": 0.605681836605072,
    "virtual_spectrum_summary": 0.11604838818311691,
    "yield": 0.2955908477306366
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
    "byproduct_signal": 0.1797490268945694,
    "conversion": 0.555738627910614,
    "cost": 1.0,
    "degradation_warning": 0.05445461347699165,
    "safety_risk": 0.1637077033519745,
    "score": 0.197458878159523,
    "selectivity": 0.6745671629905701,
    "virtual_spectrum_summary": 0.12336654216051102,
    "yield": 0.3672792315483093
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
  "end_step": 35,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.13109292089939117,
    "conversion": 0.38857370615005493,
    "cost": 1.0,
    "degradation_warning": 0.0329541377723217,
    "safety_risk": 0.10541493445634842,
    "score": 0.13983696699142456,
    "selectivity": 0.6349001526832581,
    "virtual_spectrum_summary": 0.08693046122789383,
    "yield": 0.2242281585931778
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
  "end_step": 42,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.1738366037607193,
    "conversion": 0.47636282444000244,
    "cost": 1.0,
    "degradation_warning": 0.028476471081376076,
    "safety_risk": 0.13796356320381165,
    "score": 0.17101912200450897,
    "selectivity": 0.6473530530929565,
    "virtual_spectrum_summary": 0.10842454433441162,
    "yield": 0.3090704381465912
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
    "byproduct_signal": 0.19792640209197998,
    "conversion": 0.5884859561920166,
    "cost": 1.0,
    "degradation_warning": 0.04665472358465195,
    "safety_risk": 0.1781449317932129,
    "score": 0.2009088099002838,
    "selectivity": 0.6584457159042358,
    "virtual_spectrum_summary": 0.12985414266586304,
    "yield": 0.3940350115299225
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
    "byproduct_signal": 0.1973646879196167,
    "conversion": 0.7245919108390808,
    "cost": 1.0,
    "degradation_warning": 0.0983758419752121,
    "safety_risk": 0.18561460077762604,
    "score": 0.2698715329170227,
    "selectivity": 0.7150989174842834,
    "virtual_spectrum_summary": 0.1528197079896927,
    "yield": 0.5054104328155518
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
    "byproduct_signal": 0.26619356870651245,
    "conversion": 0.8106022477149963,
    "cost": 1.0,
    "degradation_warning": 0.12580125033855438,
    "safety_risk": 0.21162213385105133,
    "score": 0.28376710414886475,
    "selectivity": 0.6841360330581665,
    "virtual_spectrum_summary": 0.20301702618598938,
    "yield": 0.5672570466995239
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
  "end_step": 70,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.2891279458999634,
    "conversion": 0.8899307250976562,
    "cost": 1.0,
    "degradation_warning": 0.15938666462898254,
    "safety_risk": 0.2607285976409912,
    "score": 0.2807513177394867,
    "selectivity": 0.675662100315094,
    "virtual_spectrum_summary": 0.2307443618774414,
    "yield": 0.6004264950752258
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
      "duration_s": 2700,
      "operation": "heat",
      "stirring_speed_rpm": 600,
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
  "end_step": 77,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.2020142376422882,
    "conversion": 0.7036938667297363,
    "cost": 1.0,
    "degradation_warning": 0.07570718228816986,
    "safety_risk": 0.2034917175769806,
    "score": 0.27511394023895264,
    "selectivity": 0.7448810935020447,
    "virtual_spectrum_summary": 0.14517606794834137,
    "yield": 0.5252388715744019
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
      "duration_s": 4800,
      "operation": "heat",
      "stirring_speed_rpm": 600,
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
    "byproduct_signal": 0.3307906687259674,
    "conversion": 0.8962426781654358,
    "cost": 1.0,
    "degradation_warning": 0.18901239335536957,
    "safety_risk": 0.21715320646762848,
    "score": 0.28457117080688477,
    "selectivity": 0.6449298858642578,
    "virtual_spectrum_summary": 0.26699045300483704,
    "yield": 0.5785834193229675
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

1. Scope and evidential basis

This report describes only the bounded synthetic reaction world explored in the completed 12-batch campaign. It is not a claim about a named real reaction, catalyst, or solvent system. Catalyst identities were opaque benchmark formulations, and the public material packet explicitly stated that solvent effects were categorical benchmark effects rather than predictions from ordinary solvent-property correlations.

Every batch used 0.040 mol reagent, 0.005 mol catalyst, 0.080 L solvent, one programmed heat operation, and 600 rpm stirring. Consequently, the campaign identifies categorical catalyst and solvent effects and a limited temperature–time response, but it does not identify concentration, catalyst-loading, mixing, addition-order, or multistep thermal effects. Each condition was run only once, so small differences must not be treated as replicated effects.

2. Proposed reaction network

The simplest model consistent with the observations is a set of competing, effectively one-way pathways:

R -> P  (desired product)
R -> B  (primary byproduct)
P -> D  (product degradation)

Additional direct formation of degradation material from R cannot be excluded. A useful kinetic representation is:

  dR/dt = -(kP + kB)R
  dP/dt = kP R - kD P
  dB/dt = kB R + alpha*kD P
  dD/dt = (1-alpha)*kD P

where kP, kB, and kD depend on catalyst, solvent, temperature, and possibly changing composition. A plausible local parameterization is

  ki(T,catalyst,solvent) = Ai * FCatalyst(i) * FSolvent(i) * exp[-Ei/(Rgas*T)]

but the campaign does not contain enough independent conditions to estimate unique activation energies or categorical multipliers.

Operationally, conversion reports loss of R, yield reports retained P, selectivity reports partitioning toward P, byproduct_signal tracks B-like material, and degradation_warning tracks D-like material. The measurements broadly support the bookkeeping relationship

  yield approximately conversion * selectivity,

although it is not exact because the channels are independently noisy and may use different normalizations. For example, batch 2 gave conversion 0.59268, selectivity 0.72009, and yield 0.42554; conversion times selectivity is about 0.4268. Batch 9 gave 0.81060, 0.68414, and 0.56726, respectively. The increasing gap between conversion and retained target at severe conditions is consistent with stronger competing and degradation pathways.

The initial public structural prior suggested that the target pathway might be effectively irreversible. The monotonic increase in conversion with thermal severity is compatible with that prior, so an irreversible approximation is reasonable over the tested support. It was not directly proven: I performed no reverse, cooling-hold, product-spike, or equilibrium experiment.

3. Catalyst effects

Batches 1–4 compared catalysts in acetonitrile at a 340 K target for 3600 s. The final-assay results were:

- Batch 1, Catalyst A: conversion 0.51185, yield 0.28258, selectivity 0.53442, byproduct 0.22594, degradation 0.02119, score 0.12835, risk 0.15439.
- Batch 2, Catalyst B: conversion 0.59268, yield 0.42554, selectivity 0.72009, byproduct 0.17754, degradation 0.05712, score 0.23399, risk 0.16782.
- Batch 3, Catalyst C: conversion 0.47988, yield 0.29559, selectivity 0.60568, byproduct 0.19262, degradation 0.02246, score 0.14816, risk 0.15440.
- Batch 4, Catalyst D: conversion 0.55574, yield 0.36728, selectivity 0.67457, byproduct 0.17975, degradation 0.05445, score 0.19746, risk 0.16371.

Thus Catalyst B increased both apparent reaction rate and desired-path partitioning relative to A, C, and D. Its advantage was not merely higher conversion: its selectivity was also highest. Catalyst B also produced more degradation warning than A or C, suggesting that a highly active catalyst may accelerate P degradation as well as P formation. A plausible catalyst ranking on the tested condition is B > D > C > A for target performance, but this ranking need not remain invariant at other temperatures, loadings, or solvents.

4. Solvent effects and coupling

Using Catalyst B at 340 K for 3600 s, batches 2 and 5–7 gave:

- Batch 5, water: conversion 0.38857, yield 0.22423, selectivity 0.63490, byproduct 0.13109, degradation 0.03295, score 0.13984, risk 0.10541.
- Batch 6, ethanol: conversion 0.47636, yield 0.30907, selectivity 0.64735, byproduct 0.17384, degradation 0.02848, score 0.17102, risk 0.13796.
- Batch 2, acetonitrile: conversion 0.59268, yield 0.42554, selectivity 0.72009, byproduct 0.17754, degradation 0.05712, score 0.23399, risk 0.16782.
- Batch 7, toluene: conversion 0.58849, yield 0.39404, selectivity 0.65845, byproduct 0.19793, degradation 0.04665, score 0.20091, risk 0.17814.

The main solvent effect appears to be on reaction progress, with the observed conversion order acetonitrile approximately toluene > ethanol > water. Acetonitrile also improved the desired-path selectivity relative to the other tested solvents, giving it the best score at this condition. Toluene approached its conversion but generated a less favorable selectivity/byproduct balance.

The safety ordering was different: water was safest, followed by ethanol, acetonitrile, and toluene. This establishes a coupled performance–risk tradeoff rather than a single universally best solvent. For example, water reduced risk to 0.10541 but also reduced yield to 0.22423, whereas acetonitrile increased yield to 0.42554 at risk 0.16782. In batch 1, adding 0.080 L acetonitrile alone produced an observed risk of 0.07762, and adding 0.040 mol reagent raised it to 0.11349 before heating. This shows that risk is not generated solely by temperature; formulation and concentration contribute before reaction heating.

Because only Catalyst B was screened across all four solvents, catalyst–solvent interaction is not separately identifiable. The apparent superiority of Catalyst B in acetonitrile cannot be assumed to have the same magnitude in water, ethanol, or toluene.

5. Temperature dependence

With Catalyst B, acetonitrile, and a 3600 s heat operation, batches 2 and 8–10 tested targets of 340, 360, 380, and 400 K:

- Batch 2, 340 K: conversion 0.59268, yield 0.42554, selectivity 0.72009, byproduct 0.17754, degradation 0.05712, score 0.23399, risk 0.16782.
- Batch 8, 360 K: conversion 0.72459, yield 0.50541, selectivity 0.71510, byproduct 0.19736, degradation 0.09838, score 0.26987, risk 0.18561.
- Batch 9, 380 K: conversion 0.81060, yield 0.56726, selectivity 0.68414, byproduct 0.26619, degradation 0.12580, score 0.28377, risk 0.21162.
- Batch 10, 400 K: conversion 0.88993, yield 0.60043, selectivity 0.67566, byproduct 0.28913, degradation 0.15939, score 0.28075, risk 0.26073.

Conversion and absolute yield rose monotonically with programmed temperature, consistent with thermally activated kinetics. Selectivity declined above 340–360 K, while byproduct and degradation signals increased. Therefore the undesired reactions appear at least as temperature-sensitive as the desired reaction, and possibly more temperature-sensitive. The public score consequently peaked locally around the 380 K region rather than at the highest yield: raising the target from 380 to 400 K increased yield by about 0.0332 but slightly reduced score because selectivity, byproduct, degradation, and risk all worsened.

The heat-step telemetry reported temperature changes of approximately 40.97, 58.50, 75.18, and 91.08 K for the respective programmed targets. These values should not be mistaken for direct confirmation that the liquid remained exactly at each target throughout the operation. A more faithful process model would contain thermal lag, for example

  dTvessel/dt = (Ttarget - Tvessel)/tau,

with kinetics integrated over Tvessel(t). The available endpoint telemetry does not identify tau or the full temperature trajectory.

6. Residence-time dependence

At a 380 K target, Catalyst B, and acetonitrile, the final results were:

- Batch 11, 2700 s: conversion 0.70369, yield 0.52524, selectivity 0.74488, byproduct 0.20201, degradation 0.07571, score 0.27511, risk 0.20349.
- Batch 9, 3600 s: conversion 0.81060, yield 0.56726, selectivity 0.68414, byproduct 0.26619, degradation 0.12580, score 0.28377, risk 0.21162.
- Batch 12, 4800 s: conversion 0.89624, yield 0.57858, selectivity 0.64493, byproduct 0.33079, degradation 0.18901, score 0.28457, risk 0.21715.

Longer residence time increased conversion but caused diminishing target-yield returns. From 3600 to 4800 s, conversion increased by about 0.0856, whereas yield increased by only about 0.0113; selectivity fell by about 0.0392 and degradation warning rose by about 0.0632. This is strong evidence for continued consumption into undesired channels and/or degradation of accumulated P.

Batch 12 had the numerically highest observed public score, 0.28457, and was therefore the sealed recommendation. However, its advantage over batch 9 was only about 0.00080, far smaller than a persuasive single-run distinction given the published assay noise and unmeasured process variability. Mechanistically, batch 9 is at least as plausible as the more robust operating region because it achieved almost the same score with substantially lower byproduct, degradation, exposure time, and risk. The campaign establishes a broad score plateau near 380 K and 3600–4800 s, not a precisely identified optimum at 4800 s.

7. Safety model

A phenomenological safety representation consistent with the data is

  Risk = Rformulation(solvent, reagent concentration, catalyst)
         + integral h(Tvessel, composition, solvent, catalyst) dt,

where h rises nonlinearly with temperature and may increase as reactive or degradation species accumulate.

Evidence for separate terms includes the preheating acetonitrile/reagent risk in batch 1, the solvent-dependent risks in batches 2 and 5–7, modest catalyst-dependent differences in batches 1–4, the strong rise from 0.16782 at 340 K to 0.26073 at 400 K, and the smaller time-dependent rise from 0.20349 at 2700 s to 0.21715 at 4800 s at 380 K. Every completed batch remained below the declared safety limit of 0.35. No observation supports extrapolating this safety conclusion above 400 K, beyond 4800 s at 380 K, at higher concentrations, or under different addition and mixing protocols.

8. Intermediate versus final measurements

HPLC was collected after heating and before termination in every batch. It generally agreed with the final assay on qualitative rankings, but individual values shifted because the instruments had independent noise and sample handling occurred between measurements. In batch 1, for example, HPLC reported conversion 0.53186, yield 0.28116, selectivity 0.53323, and byproduct 0.23914; the final assay reported 0.51185, 0.28258, 0.53442, and 0.22594. In batch 12, HPLC reported conversion 0.90674 and yield 0.57258, while the final assay reported 0.89624 and 0.57858. I therefore used final assays as the authoritative batch-comparison evidence and did not interpret small HPLC/final differences as real post-heating chemistry.

9. Factors that remain unidentified

The campaign cannot determine unique elementary rate constants, activation energies, reaction orders, heat-transfer parameters, or whether P degradation is catalyst-mediated. It also cannot distinguish all of the following reasonable alternatives:

- B may form only in parallel from R, only sequentially from P, or by both routes.
- The degradation channel may consume P, arise directly from R, or share signal with multiple minor products.
- Temperature-dependent selectivity may reflect intrinsic activation energies, catalyst-state changes, solvent-state changes, or transport effects.
- Apparent solvent activity may arise from latent categorical calibration rather than recognizable polarity, boiling point, or proticity trends.
- Catalyst B may truly increase intrinsic selectivity, or it may change the time at which maximum P concentration occurs.
- The small difference between batches 9 and 12 may be ordinary instrument/process noise rather than a reproducible time effect on score.
- Stirring and mass transfer may matter, but 600 rpm was never varied.

Reversibility is also not identified. An effectively irreversible model is supported as a practical approximation by the structural prior and the observed severity trends, but no experiment tested whether P can return to R.

10. Consolidated interpretation

Within the tested domain, Catalyst B in acetonitrile provides the largest desired-path rate and favorable selectivity. Increasing temperature or residence time drives R conversion upward, but increasingly exposes material to byproduct formation and degradation. This produces a finite performance plateau rather than unlimited improvement with severity. Solvent, catalyst, and temperature also contribute to safety risk, with temperature giving the clearest nonlinear rise. A suitable control concept for this world is therefore to stop near the onset of diminishing target-yield returns rather than maximize conversion:

  heat until marginal target formation approximately equals marginal loss to B and D,
  subject to Risk < 0.35.

The observed plateau lies near the tested 380 K target and 3600–4800 s window at the fixed recipe and stirring rate. Batch 12 was the highest measured-score member of that window, but batch 9 provides nearly indistinguishable score with a cleaner and safer measured state. Claims outside the fixed composition, 340–400 K main temperature series, and 2700–4800 s local time series are extrapolations rather than observations.

## Q — Blind predictions

### Overall rationale

Predictions use an irreversible competing-pathway model with reactant-to-target, reactant-to-byproduct, and target-degradation channels. Conversion kinetics were extrapolated from the Catalyst B/acetonitrile temperature and time series using an approximately Arrhenius temperature response and catalyst-concentration scaling. Retained yield was estimated with a sequential degradation term; selectivity was tied to retained yield relative to conversion, and byproduct signal was approximated from converted material not retained as target. The campaign data also revealed an essentially exact public-score relationship over the observed batches: score approximately -0.10 + 0.40*yield + 0.25*selectivity + 0.10*conversion - 0.45*safety_risk, bounded at zero. Safety estimates combine formulation risk with temperature-, duration-, and catalyst-dependent exposure. Intervals include final-assay noise but are dominated by structural uncertainty because catalyst amount, 400 rpm stirring, 0.005 L scale, quenching, temperatures above 400 K, and 14400-second residence times were not directly studied.

### Q01

The low catalyst concentration and short residence time should limit conversion despite 410 K. Little accumulated product degradation is expected, so retained-product selectivity should remain high. This extrapolates catalyst-loading and 400 rpm effects that were not directly varied in the campaign.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.0800 | 0.0300 | 0.2500 |
| conversion | 0.3600 | 0.2000 | 0.5800 |
| safety_risk | 0.2200 | 0.1400 | 0.3200 |
| score | 0.1500 | 0.0500 | 0.2600 |
| selectivity | 0.8000 | 0.6200 | 0.9000 |
| yield | 0.2900 | 0.1600 | 0.4400 |

### Q02

Fourteen thousand four hundred seconds at 410 K should bring even the low-catalyst batch close to complete conversion. The long hot exposure is predicted to convert much of the initially formed target into byproduct or degradation channels, sharply lowering retained selectivity and score.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6100 | 0.3700 | 0.8200 |
| conversion | 0.9700 | 0.8200 | 1.0000 |
| safety_risk | 0.3000 | 0.1900 | 0.4400 |
| score | 0.1000 | 0.0000 | 0.2400 |
| selectivity | 0.3700 | 0.1700 | 0.5900 |
| yield | 0.3600 | 0.1600 | 0.5800 |

### Q03

The high catalyst concentration should provide rapid conversion during the short 410 K treatment. Short residence time limits secondary loss, making this one of the stronger predicted conditions, although both catalyst-loading response and the 410 K extrapolation remain uncertain.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2500 | 0.1200 | 0.4300 |
| conversion | 0.8600 | 0.6800 | 0.9700 |
| safety_risk | 0.2900 | 0.1800 | 0.4200 |
| score | 0.2800 | 0.1400 | 0.3900 |
| selectivity | 0.7200 | 0.5700 | 0.8300 |
| yield | 0.6200 | 0.4400 | 0.7500 |

### Q04

High catalyst loading plus 14400 seconds at 410 K is predicted to exhaust the reactant early and then strongly degrade accumulated target. The safety-risk point estimate exceeds the declared 0.35 limit, and the score is expected to be at or near its lower bound.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8900 | 0.6400 | 0.9900 |
| conversion | 1.0000 | 0.9700 | 1.0000 |
| safety_risk | 0.3900 | 0.2500 | 0.5800 |
| score | 0.0000 | 0.0000 | 0.1000 |
| selectivity | 0.1100 | 0.0200 | 0.3500 |
| yield | 0.1100 | 0.0200 | 0.3400 |

### Q05

At 350 K the low catalyst concentration should give only moderate conversion after 7200 seconds. Lower temperature suppresses degradation and thermal risk, leaving a favorable selectivity but a yield limited by incomplete reaction.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1700 | 0.0700 | 0.3400 |
| conversion | 0.5200 | 0.3100 | 0.7200 |
| safety_risk | 0.1400 | 0.0800 | 0.2300 |
| score | 0.2000 | 0.0800 | 0.3100 |
| selectivity | 0.6700 | 0.5200 | 0.8100 |
| yield | 0.3500 | 0.2000 | 0.5200 |

### Q06

The long 465 K exposure should overcome the low catalyst concentration and drive nearly complete conversion. Severe thermal exposure is expected to cause substantial secondary loss and a likely safety-limit violation. This is a large temperature extrapolation, so its intervals are especially broad.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5500 | 0.3000 | 0.8400 |
| conversion | 0.9800 | 0.8500 | 1.0000 |
| safety_risk | 0.4700 | 0.3000 | 0.7000 |
| score | 0.0700 | 0.0000 | 0.2200 |
| selectivity | 0.4400 | 0.1500 | 0.6700 |
| yield | 0.4300 | 0.1400 | 0.6600 |

### Q07

High catalyst concentration should produce near-complete conversion even at 350 K. The long residence time permits appreciable catalyst-associated product loss, so the predicted yield is much lower than conversion despite relatively modest thermal risk.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5000 | 0.3000 | 0.7300 |
| conversion | 0.9600 | 0.8200 | 1.0000 |
| safety_risk | 0.2000 | 0.1100 | 0.3200 |
| score | 0.2100 | 0.0700 | 0.3400 |
| selectivity | 0.4700 | 0.2700 | 0.6700 |
| yield | 0.4600 | 0.2500 | 0.6500 |

### Q08

This combines the highest catalyst concentration, highest temperature, and a long residence time. Conversion should saturate, but extensive target destruction and byproduct formation are predicted. Safety risk is very likely above 0.35, making the expected score effectively zero.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8000 | 0.5000 | 0.9800 |
| conversion | 1.0000 | 0.9800 | 1.0000 |
| safety_risk | 0.6500 | 0.4200 | 0.8800 |
| score | 0.0000 | 0.0000 | 0.0800 |
| selectivity | 0.2000 | 0.0200 | 0.4900 |
| yield | 0.2000 | 0.0200 | 0.4800 |

### Q09

The center catalyst concentration closely matches the catalyst concentration used in the campaign. At 410 K for 7200 seconds, conversion should be nearly complete, but extrapolation from batches 9, 10, and 12 indicates substantial post-formation loss. Safety risk lies near the constraint boundary.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5500 | 0.3300 | 0.7800 |
| conversion | 0.9900 | 0.9100 | 1.0000 |
| safety_risk | 0.3100 | 0.2000 | 0.4600 |
| score | 0.1500 | 0.0000 | 0.2900 |
| selectivity | 0.4500 | 0.2200 | 0.6500 |
| yield | 0.4400 | 0.2000 | 0.6400 |

### Q10

The quench occurs only after the full heat exposure, so it cannot undo degradation already accumulated and should leave the final assay close to Q09. I assign a slight preservation advantage but treat it as uncertain because no quench comparison was performed; its main plausible benefit is suppressing residual chemistry during cooling.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.5400 | 0.3100 | 0.7700 |
| conversion | 0.9900 | 0.9100 | 1.0000 |
| safety_risk | 0.3000 | 0.1900 | 0.4500 |
| score | 0.1600 | 0.0000 | 0.3000 |
| selectivity | 0.4500 | 0.2300 | 0.6600 |
| yield | 0.4500 | 0.2100 | 0.6600 |

### Q11

The lower temperature keeps risk moderate, but the 14400-second duration should still drive conversion close to completion. The sequential-loss model predicts that this very long residence time removes much of the accumulated target, producing high byproduct signal and only moderate-to-low retained yield.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6400 | 0.3900 | 0.8400 |
| conversion | 0.9800 | 0.8500 | 1.0000 |
| safety_risk | 0.2000 | 0.1200 | 0.3300 |
| score | 0.1300 | 0.0000 | 0.2700 |
| selectivity | 0.3400 | 0.1300 | 0.5800 |
| yield | 0.3400 | 0.1300 | 0.5700 |

### Q12

At the center catalyst concentration, 465 K should give rapid conversion within 1800 seconds. The short duration limits degradation relative to Q06 and Q08, so substantial target yield may survive, but the temperature is outside the campaign range and the predicted safety risk is slightly above the declared limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3300 | 0.1500 | 0.5900 |
| conversion | 0.9300 | 0.7500 | 0.9900 |
| safety_risk | 0.3900 | 0.2500 | 0.5800 |
| score | 0.2200 | 0.0500 | 0.3500 |
| selectivity | 0.6400 | 0.4300 | 0.7900 |
| yield | 0.6000 | 0.3500 | 0.7500 |

## K2 — Retrospective analysis

1. Initial claims: supported, contradicted, or untested

The initial material packet contained only one substantive mechanistic prior: “The target pathway may be effectively irreversible on the public support,” with moderate confidence. It also warned that the catalysts were opaque benchmark formulations and that named solvents had categorical benchmark effects rather than transferable real-chemistry property relationships. No task-specific kinetic constants, catalyst ranking, solvent ranking, or nominal optimum was supplied.

The irreversibility prior remained compatible with the observations, but it was not demonstrated. Conversion increased with temperature in batches 2 and 8–10 and with residence time in batches 11, 9, and 12. I observed no obvious return of target to reactant. That is merely an absence of counterevidence: I never performed a cooling hold, reverse-reaction test, target spike, or equilibrium perturbation. K1 correctly described irreversibility as a “reasonable approximation” rather than an established law.

The categorical-material warning was strongly supported operationally. Acetonitrile and Catalyst B performed best in the tested comparisons, but nothing in the data justifies attributing this to ordinary solvent polarity, boiling point, or a real catalyst identity. K1 explicitly preserved this limitation.

There was no clear initial mechanistic claim that was contradicted and then knowingly left unrevised. The more important issue is that several later working assumptions lacked tests. In particular, K1 proposed R→P, R→B, and P→D as the simplest network. Rising degradation warning and diminishing yield gains support it, but they do not uniquely establish P→D. Thus this was not an initial claim refuted by data; it was a later interpretation that remained underidentified.

The declared safety limit of 0.35 was a task constraint, not a mechanistic claim. All 12 observed batches remained below it. This establishes compliance only inside the tested domain, not general safety.

2. Experiments that formed or changed the interpretation

Batch 1 established the first baseline: Catalyst A in acetonitrile at 340 K for 3600 s gave conversion 0.51185, yield 0.28258, selectivity 0.53442, score 0.12835, and risk 0.15439. Its operation-level telemetry also showed that appreciable risk existed before heating: acetonitrile addition produced risk 0.07762, and reagent addition raised it to 0.11349. That directly changed my safety interpretation from a purely thermal hazard model to a formulation-plus-thermal model.

Batch 2 was the largest early update. Replacing Catalyst A with B at otherwise matched conditions increased yield from 0.28258 to 0.42554, selectivity from 0.53442 to 0.72009, and score from 0.12835 to 0.23399. Batches 3 and 4 then showed that Catalysts C and D were intermediate rather than equivalent to B. These four batches generated the local B > D > C > A performance ranking cited in K1.

Batches 5–7, together with batch 2, formed the solvent interpretation. Water lowered risk to 0.10541 but also lowered yield to 0.22423. Toluene approached acetonitrile in conversion but had poorer selectivity and a higher risk of 0.17814. This led to the explicit K1 judgment that solvent selection involved a performance–risk tradeoff and that acetonitrile was best only for the tested Catalyst B condition.

Batches 8–10 changed the strategy from “more thermal severity gives more product” to “there is a score plateau.” Increasing the target from 340 to 400 K monotonically raised conversion and yield, but the score rose only to 0.28377 at 380 K and then fell to 0.28075 at 400 K. Byproduct, degradation warning, and risk all worsened. This was the clearest evidence for competing severity-dependent channels.

Batches 11 and 12 refined that conclusion. At 380 K, increasing duration from 2700 to 4800 s raised conversion from 0.70369 to 0.89624, but yield increased only from 0.52524 to 0.57858 while selectivity fell from 0.74488 to 0.64493. Batch 12 produced the highest numerical score, 0.28457, but exceeded batch 9 by only about 0.00080. This led K1 to describe a broad plateau rather than a precisely located optimum.

Several important choices depended on unverified guesses. The first use of acetonitrile and Catalyst A was essentially arbitrary because the packet provided no ranking. Using maximum reagent, solvent, and catalyst amounts in every batch was driven by the optimization goal and the convenient resource allocation, not by established kinetics. Holding stirring at 600 rpm assumed mixing would not dominate. The later temperature and time choices were data-driven, but catalyst loading, concentration, addition order, quenching, and mixing were never explored.

3. Leading competing mechanisms and what can be distinguished

The K1 network—parallel desired and byproduct formation followed by target degradation—remains my leading compact explanation:

R→P, R→B, and P→D.

Its principal competitor is a model with no literal P degradation. In that alternative, selectivity changes with time because the catalyst changes state, the reaction medium evolves, product inhibits the desired channel, or a late-forming byproduct pathway accelerates. The final increase in degradation_warning could then be a correlated assay channel rather than direct evidence that P was consumed.

A second competitor is a wholly parallel network with several products formed directly from R, each with different temperature dependence. Such a model can also produce increasing conversion, declining target fraction, and rising degradation signal without P→D.

A third explanation is transport or thermal-history control. The heat-step temperature changes were not equal to the programmed target changes, and stirring was fixed. Apparent kinetic effects could partly reflect thermal lag, viscosity, phase behavior, or mass transfer rather than intrinsic activation energies.

A fourth possibility is reversible chemistry or an equilibrium-limited desired pathway accompanied by irreversible side reactions. The current severity series is compatible with effective irreversibility but cannot exclude hidden reversibility because no reverse perturbation was made.

The data distinguish several broad facts: reaction progress accelerates with temperature and time; Catalyst B is locally more effective than A, C, or D in acetonitrile; acetonitrile is locally preferable to the other solvents with Catalyst B; and severe exposure worsens the target-to-nontarget balance. The data do not distinguish sequential degradation from evolving parallel selectivity, intrinsic kinetics from transport, catalyst–solvent interaction from additive categorical effects, or true equilibrium from a slow effectively irreversible process.

4. One additional legal complete experiment

I would repeat the batch-12 formulation—0.080 L acetonitrile, 0.040 mol reagent, and 0.005 mol Catalyst B at 600 rpm—but use a within-vessel time course at a 380 K target. I would heat for 3600 s, collect a small HPLC measurement, heat for another 1200 s, collect a second HPLC measurement if the instrument-use allowance permitted it, then terminate and perform the required final assay. If only one nonfinal measurement were allowed, I would measure at 3600 s and use the final assay after 4800 s, accepting the cross-instrument limitation.

This experiment would both repeat the recommended endpoint and reduce between-batch ambiguity in the batch-9 versus batch-12 comparison.

If target signal rose substantially during the extra 1200 s while reactant fell, the evidence would favor continued net target formation and weaken a strong P→D interpretation. If reactant fell but target remained approximately constant while byproduct and degradation signals rose, it would support simultaneous target formation and target loss near a kinetic plateau. If target signal itself fell while degradation signal rose, sequential P→D would receive much stronger support. If the 4800 s final result failed to reproduce batch 12 within assay and process uncertainty, the sealed recommendation would lose credibility as a stable optimum. If both time points reproduced the previous trend, confidence in the local plateau would increase.

A perfectly discriminating product-degradation experiment would start from isolated P, but that was not a legal material operation in this task. The proposed time course is therefore the most informative legal approximation.

5. Tradeoff between identifiability and operating score

The research goal explicitly prioritized strong safe-score performance. That pushed the campaign toward screening and local optimization rather than balanced mechanistic identification. Seven batches were used to choose catalyst and solvent categories, and the remaining five concentrated on temperature and residence time around the best observed formulation.

There were real sacrifices of identifiability for optimization. I did not replicate conditions, vary catalyst loading, vary stirring, vary reagent concentration, test addition order, use a no-catalyst control, or construct a full catalyst-by-solvent interaction matrix. Once Catalyst B and acetonitrile appeared favorable, I largely committed to them. This improved the chance of finding a high score within 12 batches but made the multiplicative kinetic model in K1 underdetermined.

The maximum material amounts in every batch also favored throughput and consistency over identification of reaction order. Consequently, the later blind predictions had to extrapolate catalyst concentration and scale without direct evidence.

There were smaller sacrifices of score for information. Batches 3–7 tested catalysts and solvents known by then to be less promising than batch 2, but those experiments were necessary to establish categorical rankings and the safety–performance tradeoff. Batch 10 at 400 K knowingly explored a more hazardous severity to locate the score turnover. Batch 11 at 2700 s traded expected conversion for information about the time response.

The intermediate HPLC measurement in every batch improved evidential continuity, although it was not used for within-batch adaptive stopping. A more mechanism-focused program would have used those instrument opportunities for repeated time points or controls instead of one terminal-adjacent measurement per batch.

6. Underused evidence and reliability of the blind predictions

The raw characterization artifacts and full spectra were not inspected. I relied on processed estimates and supplied peak summaries. That left potentially useful information about peak shapes, minor bands, calibration behavior, saturation, and missingness unused.

The paired HPLC and final-assay measurements were also underexploited. K1 noted examples such as batch 1, where HPLC conversion was 0.53186 and final conversion was 0.51185, but I did not build an explicit cross-instrument bias model. Because HPLC sampling preceded termination and the final assay used different synthetic channels, these differences mix instrument noise, sampling, and any intervening chemistry.

The heat-step temperature-change telemetry was acknowledged through a thermal-lag equation in K1 but not quantitatively fitted. Likewise, operation-level risk increments were available most clearly for batch 1, yet the campaign did not repeat them across amount levels. This became especially important in the blind predictions, whose recipes used 0.005 L rather than 0.080 L.

The score relationship inferred for the blind predictions—approximately score = -0.10 + 0.40*yield + 0.25*selectivity + 0.10*conversion - 0.45*safety_risk—fit the observed batches extremely closely. It was useful for internal score consistency, but it could not repair uncertainty in the predicted underlying metrics.

The least reliable blind predictions are Q04, Q06, Q08, and Q12. They involve 465 K or the combination of high catalyst loading and 14400 s, far outside the 340–400 K and 2700–4800 s local support described in K1. Q02 and Q11 are also weak because 14400 s is a threefold extrapolation beyond the longest observed heat. Q10 is structurally uncertain because no quench experiment was performed. All 12 queries changed scale, stirring, reagent concentration, and/or catalyst concentration relative to the campaign.

Several intervals were probably too narrow. In particular, Q04 conversion [0.97, 1.00] and Q08 conversion [0.98, 1.00] expressed excessive confidence in saturation despite unmeasured catalyst-loading and high-temperature behavior. The Q08 safety interval [0.42, 0.88] was broad numerically but still rested on an unidentified intensive-versus-extensive risk scaling. Q03, Q07, and Q12 yield intervals may also understate uncertainty about catalyst concentration and mixing. Q10’s narrow difference from Q09 was an assumption, not evidence.

This overconfidence is in tension with K1’s explicit statement that safety and kinetics should not be extrapolated above 400 K, beyond 4800 s, at different concentrations, or under different mixing protocols. The blind-prediction rationale acknowledged those extrapolations, but some numerical intervals did not fully honor the scope warning.

7. Limitations of the sealed recommendation

Batch 12 was the sample-in highest observed result, not a proven optimum. Its score of 0.28457 exceeded batch 9’s 0.28377 by only about 0.00080. That difference is not compelling relative to assay noise, process variability, and the lack of replicates. Batch 12 also had substantially worse byproduct_signal, 0.33079 versus 0.26619, degradation_warning, 0.18901 versus 0.12580, and risk, 0.21715 versus 0.21162. The sealed choice followed the numerical score objective, but batch 9 may be operationally more robust.

Repeatability should be tested with multiple independent repeats of batches 9 and 12, using the same addition order and calibrated instruments. The appropriate comparison would include distributions of score and safety risk, not only mean yield. A paired or blocked design would help separate day-to-day process variation from the small mean-score difference.

Local robustness should be tested around 380 K and 3600–4800 s with modest perturbations in temperature, duration, catalyst amount, reagent concentration, and stirring. The aim would be to identify a region whose lower prediction bound remains attractive and whose upper risk bound remains below 0.35. A robust optimum could differ from the highest single observed point.

Catalyst–solvent robustness requires at least a partial interaction design, because only Catalyst B was tested across all four solvents. Material robustness would require controlled changes in material lots or explicitly different benchmark formulations. No inference to a real named catalyst or ordinary solvent-property rule is justified.

Finally, cross-world generalization cannot be claimed. The materials were anonymous or categorically coupled to this synthetic benchmark. Validation in another world would require fresh calibration and experiments rather than replaying the batch-12 recipe as if its mechanism were universal. The defensible conclusion is therefore: batch 12 was the highest-scoring member of the 12 observed batches and complied with the observed safety constraint; it was not demonstrated to be uniquely optimal, repeatable, locally robust, or transferable.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 100.5 | none | 0 |
| Q | yes | 0 | 229.5 | none | 0 |
| K2 | yes | 0 | 121.1 | none | 0 |

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean 80% width | Mean interval score |
|---|---:|---:|---:|---:|
| byproduct_signal | 0.0901 | 0.9667 | 0.4042 | 0.4082 |
| conversion | 0.0322 | 1.0000 | 0.1842 | 0.1842 |
| safety_risk | 0.0772 | 0.7500 | 0.2733 | 0.3197 |
| score | 0.0802 | 0.8333 | 0.2300 | 0.2559 |
| selectivity | 0.0998 | 0.9167 | 0.3867 | 0.3966 |
| yield | 0.0752 | 1.0000 | 0.3967 | 0.3967 |

## Predictions versus released reference truth

### Q01

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.0800 | 0.0300 | 0.2500 | 0.1660 | 0.1755, 0.1675, 0.1685, 0.1634, 0.1550 |
| conversion | 0.3600 | 0.2000 | 0.5800 | 0.4974 | 0.4904, 0.4986, 0.4894, 0.5090, 0.4995 |
| safety_risk | 0.2200 | 0.1400 | 0.3200 | 0.2382 | 0.2382, 0.2382, 0.2382, 0.2382, 0.2382 |
| score | 0.1500 | 0.0500 | 0.2600 | 0.2176 | 0.2177, 0.2151, 0.2192, 0.2149, 0.2213 |
| selectivity | 0.8000 | 0.6200 | 0.9000 | 0.6682 | 0.6668, 0.6747, 0.6838, 0.6463, 0.6693 |
| yield | 0.2900 | 0.1600 | 0.4400 | 0.3393 | 0.3421, 0.3286, 0.3353, 0.3432, 0.3471 |
### Q02

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.6100 | 0.3700 | 0.8200 | 0.7907 | 0.7883, 0.7816, 0.7919, 0.7950, 0.7966 |
| conversion | 0.9700 | 0.8200 | 1.0000 | 0.9955 | 1.0000, 0.9904, 1.0000, 0.9914, 0.9959 |
| safety_risk | 0.3000 | 0.1900 | 0.4400 | 0.2401 | 0.2401, 0.2401, 0.2401, 0.2401, 0.2401 |
| score | 0.1000 | 0.0000 | 0.2400 | 0.0925 | 0.0906, 0.0940, 0.0910, 0.0943, 0.0926 |
| selectivity | 0.3700 | 0.1700 | 0.5900 | 0.2151 | 0.2068, 0.2240, 0.2125, 0.2183, 0.2138 |
| yield | 0.3600 | 0.1600 | 0.5800 | 0.2135 | 0.2128, 0.2130, 0.2102, 0.2171, 0.2144 |
### Q03

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2500 | 0.1200 | 0.4300 | 0.1759 | 0.1879, 0.1765, 0.1652, 0.1758, 0.1740 |
| conversion | 0.8600 | 0.6800 | 0.9700 | 0.8625 | 0.8723, 0.8654, 0.8646, 0.8518, 0.8582 |
| safety_risk | 0.2900 | 0.1800 | 0.4200 | 0.2411 | 0.2411, 0.2411, 0.2411, 0.2411, 0.2411 |
| score | 0.2800 | 0.1400 | 0.3900 | 0.3993 | 0.3998, 0.4060, 0.3982, 0.3925, 0.3999 |
| selectivity | 0.7200 | 0.5700 | 0.8300 | 0.8038 | 0.8083, 0.8175, 0.8050, 0.7813, 0.8070 |
| yield | 0.6200 | 0.4400 | 0.7500 | 0.6927 | 0.6888, 0.7002, 0.6887, 0.6925, 0.6933 |
### Q04

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.8900 | 0.6400 | 0.9900 | 0.8234 | 0.8319, 0.8187, 0.8047, 0.8242, 0.8376 |
| conversion | 1.0000 | 0.9700 | 1.0000 | 0.9961 | 0.9979, 1.0000, 0.9969, 0.9949, 0.9909 |
| safety_risk | 0.3900 | 0.2500 | 0.5800 | 0.2407 | 0.2407, 0.2407, 0.2407, 0.2407, 0.2407 |
| score | 0.0000 | 0.0000 | 0.1000 | 0.0586 | 0.0586, 0.0599, 0.0615, 0.0530, 0.0597 |
| selectivity | 0.1100 | 0.0200 | 0.3500 | 0.2067 | 0.2135, 0.2148, 0.2117, 0.1955, 0.1978 |
| yield | 0.1100 | 0.0200 | 0.3400 | 0.2065 | 0.2020, 0.2039, 0.2104, 0.2000, 0.2162 |
### Q05

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.1700 | 0.0700 | 0.3400 | 0.3427 | 0.3570, 0.3472, 0.3373, 0.3320, 0.3400 |
| conversion | 0.5200 | 0.3100 | 0.7200 | 0.6725 | 0.6707, 0.6733, 0.6807, 0.6692, 0.6687 |
| safety_risk | 0.1400 | 0.0800 | 0.2300 | 0.1409 | 0.1409, 0.1409, 0.1409, 0.1409, 0.1409 |
| score | 0.2000 | 0.0800 | 0.3100 | 0.2363 | 0.2352, 0.2416, 0.2340, 0.2391, 0.2316 |
| selectivity | 0.6700 | 0.5200 | 0.8100 | 0.5081 | 0.5123, 0.5200, 0.4998, 0.5115, 0.4971 |
| yield | 0.3500 | 0.2000 | 0.5200 | 0.3440 | 0.3391, 0.3498, 0.3415, 0.3498, 0.3401 |
### Q06

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5500 | 0.3000 | 0.8400 | 0.6580 | 0.6596, 0.6455, 0.6477, 0.6646, 0.6724 |
| conversion | 0.9800 | 0.8500 | 1.0000 | 0.9970 | 0.9923, 0.9975, 0.9958, 0.9992, 1.0000 |
| safety_risk | 0.4700 | 0.3000 | 0.7000 | 0.4184 | 0.4184, 0.4184, 0.4184, 0.4184, 0.4184 |
| score | 0.0700 | 0.0000 | 0.2200 | 0.0968 | 0.1005, 0.0990, 0.0959, 0.0959, 0.0930 |
| selectivity | 0.4400 | 0.1500 | 0.6700 | 0.3386 | 0.3473, 0.3394, 0.3406, 0.3360, 0.3297 |
| yield | 0.4300 | 0.1400 | 0.6600 | 0.3324 | 0.3371, 0.3371, 0.3291, 0.3310, 0.3275 |
### Q07

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5000 | 0.3000 | 0.7300 | 0.3706 | 0.3709, 0.3574, 0.3671, 0.3773, 0.3805 |
| conversion | 0.9600 | 0.8200 | 1.0000 | 0.9536 | 0.9645, 0.9474, 0.9625, 0.9460, 0.9476 |
| safety_risk | 0.2000 | 0.1100 | 0.3200 | 0.1433 | 0.1433, 0.1433, 0.1433, 0.1433, 0.1433 |
| score | 0.2100 | 0.0700 | 0.3400 | 0.3618 | 0.3636, 0.3575, 0.3639, 0.3586, 0.3653 |
| selectivity | 0.4700 | 0.2700 | 0.6700 | 0.6202 | 0.6227, 0.6081, 0.6355, 0.6026, 0.6321 |
| yield | 0.4600 | 0.2500 | 0.6500 | 0.5921 | 0.5924, 0.5905, 0.5856, 0.5970, 0.5950 |
### Q08

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.8000 | 0.5000 | 0.9800 | 0.6833 | 0.6764, 0.6873, 0.6869, 0.6861, 0.6798 |
| conversion | 1.0000 | 0.9800 | 1.0000 | 0.9969 | 0.9976, 1.0000, 0.9869, 1.0000, 1.0000 |
| safety_risk | 0.6500 | 0.4200 | 0.8800 | 0.4189 | 0.4189, 0.4189, 0.4189, 0.4189, 0.4189 |
| score | 0.0000 | 0.0000 | 0.0800 | 0.0716 | 0.0729, 0.0695, 0.0697, 0.0774, 0.0686 |
| selectivity | 0.2000 | 0.0200 | 0.4900 | 0.3451 | 0.3412, 0.3405, 0.3438, 0.3497, 0.3501 |
| yield | 0.2000 | 0.0200 | 0.4800 | 0.3379 | 0.3433, 0.3348, 0.3364, 0.3487, 0.3264 |
### Q09

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5500 | 0.3300 | 0.7800 | 0.5497 | 0.5468, 0.5516, 0.5584, 0.5480, 0.5434 |
| conversion | 0.9900 | 0.9100 | 1.0000 | 0.9944 | 0.9970, 0.9902, 1.0000, 0.9955, 0.9895 |
| safety_risk | 0.3100 | 0.2000 | 0.4600 | 0.2411 | 0.2411, 0.2411, 0.2411, 0.2411, 0.2411 |
| score | 0.1500 | 0.0000 | 0.2900 | 0.2421 | 0.2357, 0.2430, 0.2458, 0.2442, 0.2419 |
| selectivity | 0.4500 | 0.2200 | 0.6500 | 0.4571 | 0.4478, 0.4587, 0.4688, 0.4497, 0.4606 |
| yield | 0.4400 | 0.2000 | 0.6400 | 0.4578 | 0.4468, 0.4601, 0.4582, 0.4673, 0.4563 |
### Q10

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.5400 | 0.3100 | 0.7700 | 0.5455 | 0.5591, 0.5398, 0.5426, 0.5369, 0.5491 |
| conversion | 0.9900 | 0.9100 | 1.0000 | 0.9937 | 1.0000, 1.0000, 0.9875, 0.9862, 0.9946 |
| safety_risk | 0.3000 | 0.1900 | 0.4500 | 0.1447 | 0.1447, 0.1447, 0.1447, 0.1447, 0.1447 |
| score | 0.1600 | 0.0000 | 0.3000 | 0.2835 | 0.2828, 0.2939, 0.2808, 0.2830, 0.2771 |
| selectivity | 0.4500 | 0.2300 | 0.6600 | 0.4608 | 0.4589, 0.4903, 0.4415, 0.4667, 0.4468 |
| yield | 0.4500 | 0.2100 | 0.6600 | 0.4590 | 0.4568, 0.4649, 0.4658, 0.4559, 0.4516 |
### Q11

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.6400 | 0.3900 | 0.8400 | 0.5995 | 0.6234, 0.5938, 0.5959, 0.5966, 0.5880 |
| conversion | 0.9800 | 0.8500 | 1.0000 | 0.9882 | 0.9840, 0.9870, 0.9883, 0.9952, 0.9867 |
| safety_risk | 0.2000 | 0.1200 | 0.3300 | 0.1429 | 0.1429, 0.1429, 0.1429, 0.1429, 0.1429 |
| score | 0.1300 | 0.0000 | 0.2700 | 0.2369 | 0.2418, 0.2390, 0.2310, 0.2346, 0.2381 |
| selectivity | 0.3400 | 0.1300 | 0.5800 | 0.3913 | 0.3984, 0.4014, 0.3924, 0.3747, 0.3894 |
| yield | 0.3400 | 0.1300 | 0.5700 | 0.3919 | 0.4007, 0.3911, 0.3766, 0.3947, 0.3966 |
### Q12

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3300 | 0.1500 | 0.5900 | 0.2298 | 0.2339, 0.2223, 0.2346, 0.2244, 0.2338 |
| conversion | 0.9300 | 0.7500 | 0.9900 | 0.9087 | 0.9225, 0.9044, 0.9203, 0.8975, 0.8989 |
| safety_risk | 0.3900 | 0.2500 | 0.5800 | 0.4192 | 0.4192, 0.4192, 0.4192, 0.4192, 0.4192 |
| score | 0.2200 | 0.0500 | 0.3500 | 0.3203 | 0.3213, 0.3222, 0.3237, 0.3173, 0.3171 |
| selectivity | 0.6400 | 0.4300 | 0.7900 | 0.7430 | 0.7407, 0.7464, 0.7577, 0.7340, 0.7361 |
| yield | 0.6000 | 0.3500 | 0.7500 | 0.6852 | 0.6855, 0.6889, 0.6816, 0.6860, 0.6839 |

## Recommendation retest

- Selected source batch: `12`
- Retest exact replay verified: `True`
- Retest failure: `none`

| Metric | Selected source batch | Independent retest | Retest minus source |
|---|---:|---:|---:|
| byproduct_signal | 0.3308 | 0.3345 | 0.0037 |
| conversion | 0.8962 | 0.8888 | -0.0075 |
| cost | 1.0000 | 1.0000 | 0.0000 |
| degradation_warning | 0.1890 | 0.1929 | 0.0038 |
| safety_risk | 0.2172 | 0.2172 | 0.0000 |
| score | 0.2846 | 0.2867 | 0.0022 |
| selectivity | 0.6449 | 0.6593 | 0.0144 |
| virtual_spectrum_summary | 0.2670 | 0.2708 | 0.0038 |
| yield | 0.5786 | 0.5769 | -0.0017 |

## Scope note

This is the final sanitized report produced after all 60 source sessions and K1/Q/K2 chains were sealed. It includes released reference truth, blind-prediction evaluation, and the independent recommendation retest. Provider-private event streams, credentials, thread identifiers, and token accounting remain excluded.
