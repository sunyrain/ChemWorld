# RX-W02--S--safety_constrained_optimization--Aligned

## Run summary

- World: `RX-W02`
- Locus: `S`
- Goal: `safety_constrained_optimization`
- Arm: `Aligned`
- Status: `completed`
- Source status: `completed`
- Experimental sessions: `12/12`
- Operations: `89`
- Exact replay: `{'checked_steps': 89, 'max_abs_error': 0.0, 'mismatches': [], 'verified': True}`
- Posttest chain sealed: `True`

### Recovery status

No recovery override was required for this task.

## Sealed recommendation

- Selected batch: `11`
- Rationale: Batch 11 achieved the highest observed public safe score (0.257) while remaining comfortably below the 0.35 safety limit (risk 0.139), using water, Catalyst A, and a short 410 K heat followed by quench.

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S0 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 350 K × 3600 s @ 600 rpm; 350 K × 7200 s @ 600 rpm | yes | 0.4040 | 0.5315 | 0.7675 | 0.3870 | 0.0725 | 0.1282 | 0.2135 |
| 2 | S0 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 350 K × 10800 s @ 600 rpm | yes | 0.4146 | 0.4925 | 0.7899 | 0.3971 | 0.1613 | 0.1325 | 0.2083 |
| 3 | S0 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 350 K × 10800 s @ 600 rpm | yes | 0.3746 | 0.5127 | 0.7238 | 0.3711 | 0.1466 | 0.1283 | 0.1927 |
| 4 | S0 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K × 10800 s @ 600 rpm | yes | 0.3490 | 0.4792 | 0.7389 | 0.3964 | 0.1368 | 0.1262 | 0.1765 |
| 5 | S1 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 350 K × 10800 s @ 600 rpm | yes | 0.3477 | 0.4096 | 0.8589 | 0.5036 | 0.1015 | 0.1497 | 0.1600 |
| 6 | S2 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 350 K × 10800 s @ 600 rpm | yes | 0.3552 | 0.4028 | 0.8332 | 0.5036 | 0.1446 | 0.1703 | 0.1494 |
| 7 | S3 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 350 K × 10800 s @ 600 rpm | yes | 0.3589 | 0.4166 | 0.8713 | 0.5283 | 0.1256 | 0.1820 | 0.1529 |
| 8 | S0 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 330 K × 14400 s @ 600 rpm; 330 K × 3600 s @ 600 rpm | yes | 0.3695 | 0.4593 | 0.8084 | 0.4419 | 0.1270 | 0.1271 | 0.1863 |
| 9 | S0 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 370 K × 7200 s @ 600 rpm | yes | 0.4355 | 0.5801 | 0.7469 | 0.3193 | 0.0864 | 0.1294 | 0.2357 |
| 10 | S0 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 390 K × 5400 s @ 600 rpm | yes | 0.4540 | 0.6263 | 0.7371 | 0.2815 | 0.0657 | 0.1330 | 0.2520 |
| 11 | S0 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 410 K × 4200 s @ 600 rpm | yes | 0.4737 | 0.6327 | 0.7165 | 0.2678 | 0.0598 | 0.1386 | 0.2570 |
| 12 | S0 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 430 K × 3000 s @ 600 rpm | yes | 0.4421 | 0.6762 | 0.6535 | 0.2079 | 0.0265 | 0.1473 | 0.2450 |

## Complete experimental actions and observations

### Batch 1

Lifecycle index: `1`; end step: `9`.

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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 350
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
  "end_step": 9,
  "lifecycle_index": 1,
  "metrics": {
    "byproduct_signal": 0.38695964217185974,
    "conversion": 0.7675004601478577,
    "cost": 1.0,
    "degradation_warning": 0.0725306048989296,
    "safety_risk": 0.1281982660293579,
    "score": 0.21353130042552948,
    "selectivity": 0.5314829349517822,
    "virtual_spectrum_summary": 0.24546657502651215,
    "yield": 0.40399935841560364
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
      "stirring_speed_rpm": 600,
      "target_temperature_K": 350
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
    "byproduct_signal": 0.3971147835254669,
    "conversion": 0.7899425625801086,
    "cost": 1.0,
    "degradation_warning": 0.16128742694854736,
    "safety_risk": 0.13254092633724213,
    "score": 0.2083061933517456,
    "selectivity": 0.49254077672958374,
    "virtual_spectrum_summary": 0.29099246859550476,
    "yield": 0.41455039381980896
  },
  "ordinal": 2
}
```

### Batch 3

Lifecycle index: `3`; end step: `23`.

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
      "duration_s": 10800,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 350
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
  "end_step": 23,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.37107688188552856,
    "conversion": 0.7238170504570007,
    "cost": 1.0,
    "degradation_warning": 0.14660173654556274,
    "safety_risk": 0.12825144827365875,
    "score": 0.1926773190498352,
    "selectivity": 0.5126926302909851,
    "virtual_spectrum_summary": 0.2700630724430084,
    "yield": 0.37458905577659607
  },
  "ordinal": 3
}
```

### Batch 4

Lifecycle index: `4`; end step: `30`.

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
      "duration_s": 10800,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 350
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
  "end_step": 30,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.39636796712875366,
    "conversion": 0.7388730645179749,
    "cost": 1.0,
    "degradation_warning": 0.13683992624282837,
    "safety_risk": 0.12623724341392517,
    "score": 0.17646558582782745,
    "selectivity": 0.4792105555534363,
    "virtual_spectrum_summary": 0.27958035469055176,
    "yield": 0.34895601868629456
  },
  "ordinal": 4
}
```

### Batch 5

Lifecycle index: `5`; end step: `37`.

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
      "duration_s": 10800,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 350
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
  "end_step": 37,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.5035950541496277,
    "conversion": 0.8589282631874084,
    "cost": 1.0,
    "degradation_warning": 0.1014639288187027,
    "safety_risk": 0.14973729848861694,
    "score": 0.15996110439300537,
    "selectivity": 0.4095532298088074,
    "virtual_spectrum_summary": 0.32263603806495667,
    "yield": 0.3476543724536896
  },
  "ordinal": 5
}
```

### Batch 6

Lifecycle index: `6`; end step: `44`.

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
      "duration_s": 10800,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 350
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
  "end_step": 44,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.503620445728302,
    "conversion": 0.8332204818725586,
    "cost": 1.0,
    "degradation_warning": 0.1446346491575241,
    "safety_risk": 0.17034628987312317,
    "score": 0.14944559335708618,
    "selectivity": 0.40279725193977356,
    "virtual_spectrum_summary": 0.34207683801651,
    "yield": 0.3552001416683197
  },
  "ordinal": 6
}
```

### Batch 7

Lifecycle index: `7`; end step: `51`.

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
      "duration_s": 10800,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 350
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
  "end_step": 51,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.5282992720603943,
    "conversion": 0.8712890148162842,
    "cost": 1.0,
    "degradation_warning": 0.12556862831115723,
    "safety_risk": 0.18201160430908203,
    "score": 0.15292897820472717,
    "selectivity": 0.41664257645606995,
    "virtual_spectrum_summary": 0.34707045555114746,
    "yield": 0.35886162519454956
  },
  "ordinal": 7
}
```

### Batch 8

Lifecycle index: `8`; end step: `60`.

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
      "duration_s": 14400,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 330
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 330
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
  "end_step": 60,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.44194552302360535,
    "conversion": 0.8083832859992981,
    "cost": 1.0,
    "degradation_warning": 0.12698860466480255,
    "safety_risk": 0.12711352109909058,
    "score": 0.1862524449825287,
    "selectivity": 0.45930352807044983,
    "virtual_spectrum_summary": 0.3002149164676666,
    "yield": 0.36947330832481384
  },
  "ordinal": 8
}
```

### Batch 9

Lifecycle index: `9`; end step: `67`.

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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 370
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
  "end_step": 67,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.3193141222000122,
    "conversion": 0.7469068169593811,
    "cost": 1.0,
    "degradation_warning": 0.08643291145563126,
    "safety_risk": 0.12940095365047455,
    "score": 0.2356993407011032,
    "selectivity": 0.5801238417625427,
    "virtual_spectrum_summary": 0.21451757848262787,
    "yield": 0.43552032113075256
  },
  "ordinal": 9
}
```

### Batch 10

Lifecycle index: `10`; end step: `74`.

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
      "duration_s": 5400,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 390
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
  "end_step": 74,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.2814910411834717,
    "conversion": 0.7371008992195129,
    "cost": 1.0,
    "degradation_warning": 0.06573106348514557,
    "safety_risk": 0.13302798569202423,
    "score": 0.2520172894001007,
    "selectivity": 0.6263277530670166,
    "virtual_spectrum_summary": 0.1843990534543991,
    "yield": 0.45396965742111206
  },
  "ordinal": 10
}
```

### Batch 11

Lifecycle index: `11`; end step: `81`.

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
      "duration_s": 4200,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 410
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
  "end_step": 81,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.2678026556968689,
    "conversion": 0.7164536714553833,
    "cost": 1.0,
    "degradation_warning": 0.059811703860759735,
    "safety_risk": 0.13859091699123383,
    "score": 0.25695034861564636,
    "selectivity": 0.6327149868011475,
    "virtual_spectrum_summary": 0.17420673370361328,
    "yield": 0.47373032569885254
  },
  "ordinal": 11
}
```

### Batch 12

Lifecycle index: `12`; end step: `89`.

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
      "duration_s": 3000,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 430
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
  "end_step": 89,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.20787103474140167,
    "conversion": 0.653471827507019,
    "cost": 1.0,
    "degradation_warning": 0.026506463065743446,
    "safety_risk": 0.1472700983285904,
    "score": 0.24498246610164642,
    "selectivity": 0.6762462258338928,
    "virtual_spectrum_summary": 0.12625697255134583,
    "yield": 0.4421131908893585
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

1. Scope and evidence base

This report describes only the bounded synthetic reaction world explored in the completed 12-batch campaign. The reagent and catalysts were anonymous benchmark materials, and the named solvents had categorical benchmark effects. I therefore do not assign a real molecular identity, named reaction, or real-world catalyst mechanism.

Every batch used 0.040 mol reagent, 0.005 mol catalyst, 0.080 L solvent, and 600 rpm stirring. All batches were quenched before termination and final assay. Consequently, the evidence identifies relative effects of catalyst identity, solvent identity, and a coupled temperature–time schedule, but it does not identify concentration, catalyst-loading, mixing, or scale effects.

2. Proposed reaction network

The simplest explanation consistent with the observations is an effectively irreversible target-forming pathway competing with side-product formation and followed by slower loss of target quality:

R --kP(catalyst, solvent, T)--> P
R --kB(catalyst, solvent, T)--> B
P --kD(catalyst, solvent, T)--> D

Here R is the public reactant pool, P is the desired product pool, B represents parallel impurities/byproducts, and D represents degraded or otherwise nonselective material. A minimal kinetic representation would be:

dR/dt = -(kP + kB)R
dP/dt = kP R - kD P
dB/dt = kB R + alpha*kD P

with Arrhenius-like temperature dependence, for example k_i = A_i(catalyst, solvent)*exp[-E_i/(RT)]. The data do not establish that these are literal elementary steps; they are an identifiable phenomenological network.

Conversion reports disappearance of R, whereas yield and selectivity reflect formation and retention of P. Thus high conversion need not imply high target yield. The solvent screen strongly demonstrated this distinction.

3. Time evolution and evidence for secondary loss

Batch 1 used water and Catalyst A at 350 K. After the first 3,600 s, HPLC observed conversion 0.3809, yield 0.2345, selectivity 0.5807, and byproduct signal 0.1514. After another 7,200 s at the same nominal temperature, the final assay observed conversion 0.7675 and yield 0.4040, while selectivity declined to 0.5315 and byproduct signal rose to 0.3870. The desired product therefore accumulated with time, but the marginal chemistry became less selective.

Batch 8 provides stronger evidence for over-processing. With water and Catalyst A at 330 K, HPLC after 14,400 s gave conversion 0.7313, yield 0.3789, selectivity 0.5116, and byproduct signal 0.4056. After a further 3,600 s, the final assay gave higher conversion, 0.8084, but lower yield, 0.3695, lower selectivity, 0.4593, and higher byproduct signal, 0.4419. Because the intermediate and final values came from different instruments and include measurement noise, their exact difference should not be overinterpreted. Nevertheless, the simultaneous rise in conversion and byproduct signal with loss of yield/selectivity is qualitatively consistent with target loss or increasingly dominant side chemistry at long residence time.

These observations caused me to replace an initial simple model, in which longer heating merely approached a fixed product yield, with the sequential/parallel model above. The apparent irreversibility prior supplied for this world remains plausible for reactant consumption, but it does not imply that the target itself is indefinitely stable.

4. Catalyst effects

Batches 1–4 compared all four catalysts in water under an approximately common 350 K, 10,800 s total heat exposure:

- Batch 1, Catalyst A: conversion 0.7675, yield 0.4040, selectivity 0.5315, byproduct 0.3870, degradation warning 0.0725, final risk 0.1282, score 0.2135.
- Batch 2, Catalyst B: conversion 0.7899, yield 0.4146, selectivity 0.4925, byproduct 0.3971, degradation warning 0.1613, risk 0.1325, score 0.2083.
- Batch 3, Catalyst C: conversion 0.7238, yield 0.3746, selectivity 0.5127, byproduct 0.3711, degradation warning 0.1466, risk 0.1283, score 0.1927.
- Batch 4, Catalyst D: conversion 0.7389, yield 0.3490, selectivity 0.4792, byproduct 0.3964, degradation warning 0.1368, risk 0.1262, score 0.1765.

Catalyst B produced slightly higher conversion and nominal yield than Catalyst A, but it had poorer selectivity and a much larger degradation warning. Catalyst A consequently produced the best safe score and was retained. In the proposed equations, Catalyst A appears to provide the most favorable effective kP/(kB+kD) ratio rather than simply the largest total rate constant. Catalyst B may be somewhat more active but less discriminating or less stable.

This conclusion is local to the tested loading and schedules. Catalyst ranking could change at another loading, concentration, or temperature because only one catalyst loading was examined.

5. Solvent effects

Batches 1 and 5–7 compared the four solvents with Catalyst A near 350 K for 10,800 s:

- Batch 1, water: conversion 0.7675, yield 0.4040, selectivity 0.5315, byproduct 0.3870, risk 0.1282, score 0.2135.
- Batch 5, ethanol: conversion 0.8589, yield 0.3477, selectivity 0.4096, byproduct 0.5036, risk 0.1497, score 0.1600.
- Batch 6, acetonitrile: conversion 0.8332, yield 0.3552, selectivity 0.4028, byproduct 0.5036, risk 0.1703, score 0.1494.
- Batch 7, toluene: conversion 0.8713, yield 0.3589, selectivity 0.4166, byproduct 0.5283, risk 0.1820, score 0.1529.

The nonaqueous solvents all accelerated overall reactant disappearance relative to water, but disproportionately promoted non-target chemistry. Their higher conversion was accompanied by lower target yield/selectivity, larger byproduct signals, higher risk, and lower scores. Water therefore does not appear to maximize gross reaction rate; it improves pathway discrimination and safety.

Within the phenomenological model, water reduces kB/kP, kD/kP, or both. Plausible benchmark-level interpretations include differential stabilization of the target-forming transition state, suppression of a side reaction, or improved catalyst-state stability. The experiment cannot distinguish these explanations, and the real solvent names must not be treated as evidence for a particular molecular solvation mechanism.

6. Temperature–time coupling

The later water/Catalyst A experiments deliberately shortened residence time as temperature increased:

- Batch 8: 330 K for 18,000 s; conversion 0.8084, yield 0.3695, selectivity 0.4593, byproduct 0.4419, degradation warning 0.1270, risk 0.1271, score 0.1863.
- Batch 9: 370 K for 7,200 s; conversion 0.7469, yield 0.4355, selectivity 0.5801, byproduct 0.3193, degradation warning 0.0864, risk 0.1294, score 0.2357.
- Batch 10: 390 K for 5,400 s; conversion 0.7371, yield 0.4540, selectivity 0.6263, byproduct 0.2815, degradation warning 0.0657, risk 0.1330, score 0.2520.
- Batch 11: 410 K for 4,200 s; conversion 0.7165, yield 0.4737, selectivity 0.6327, byproduct 0.2678, degradation warning 0.0598, risk 0.1386, score 0.2570.
- Batch 12: 430 K for 3,000 s; conversion 0.6535, yield 0.4421, selectivity 0.6762, byproduct 0.2079, degradation warning 0.0265, final risk 0.1473, score 0.2450.

The 330–410 K sequence indicates that a hotter, shorter treatment was superior to a cooler, longer treatment in this region. Conversion declined modestly with increasingly short schedules, but selectivity rose, byproduct and degradation signals fell, and target yield peaked in Batch 11. This suggests that the desired pathway responds rapidly to temperature, while important losses depend strongly on residence time, accumulated exposure, catalyst aging, or prolonged contact with products. In Arrhenius language, the target-forming process may have a favorable apparent temperature response relative to the dominant low-temperature/time-dependent losses. However, temperature and duration were deliberately confounded, so separate activation energies cannot be estimated.

Batch 12 indicates a turnover rather than unlimited improvement with temperature. Although it had the highest selectivity and lowest byproduct/degradation signals, its conversion and yield were lower than Batch 11, and its final score was lower. The 3,000 s residence time was probably too short to form enough target. It is also possible that 430 K introduced a new limitation such as catalyst deactivation or a rapid thermal transient, but the present measurements cannot distinguish that from under-conversion.

7. Safety behavior and quench coupling

Safety risk contained at least two components: a charge/composition contribution and a thermal-state contribution. In Batch 1, adding 0.080 L water produced risk about 0.0363, and adding 0.040 mol reagent raised it to about 0.0722. Heating at 350 K for the first hour raised it to about 0.1074; after the full heat exposure it reached about 0.1354, and quenching reduced it to about 0.1282.

The thermal term was strongly nonlinear at the upper end. In Batch 12, heating toward 430 K for 3,000 s produced a pre-quench risk of 0.3299, close to the declared 0.35 limit. Quenching then reduced the final observed risk to 0.1473. Thus quench is not merely a bookkeeping step: it appears to remove stored thermal/reactive hazard by cooling or deactivating the mixture. A useful qualitative model is:

risk = charge_risk(solvent, amounts) + hot_state_risk(T, exposure, reactive inventory) - quench_relief

where hot_state_risk increases nonlinearly with temperature. Final risk alone can conceal a much higher transient risk before quench. This is why Batch 11 is the stronger operating point despite the attractive selectivity of Batch 12: Batch 11 achieved the best observed score with a much larger margin from the limit during the tested schedule.

The safe-score evidently rewards target formation/selectivity while penalizing risk and non-target outcomes. I did not infer an exact scoring equation. For example, score did not behave as a simple function of conversion alone: high-conversion nonaqueous batches scored poorly because selectivity, byproduct formation, and risk were unfavorable.

8. Recommended mechanistic interpretation of the best batch

Batch 11—water, Catalyst A, 410 K, 4,200 s, 600 rpm, followed by quench—was the best observed compromise. Its final assay gave yield 0.4737, selectivity 0.6327, conversion 0.7165, byproduct signal 0.2678, degradation warning 0.0598, risk 0.1386, and score 0.2570.

Mechanistically, I interpret this point as a kinetic window: the temperature is high enough for rapid target formation, while the residence time is short enough to limit parallel byproduct accumulation and secondary target loss. Quenching arrests the active/hot state before additional deterioration occurs. Batch 12 moved further toward selectivity but sacrificed too much conversion and approached the safety boundary during heating.

9. Identifiability limits and competing explanations

Several important features remain unidentified:

- Temperature and duration were not varied independently in the optimization series. The apparent benefit of temperature could instead be primarily a benefit of shorter residence time.
- Only one reagent concentration, catalyst loading, solvent volume, and stirring rate were tested. No kinetic orders, transport dependence, or catalyst-loading optimum can be claimed.
- There was no uncatalyzed control, so the magnitude of catalytic acceleration is unknown.
- There was no direct species mapping. Byproduct and degradation channels are aggregate synthetic observables, not identified molecules.
- Most conditions had only one final assay and no replicate batch. Differences near the instrument-noise scale should not be treated as exact.
- Batch 1 and Batch 8 included intermediate HPLC measurements and small sample removal, whereas most other batches did not. This is too small to explain the major trends but prevents a perfectly identical protocol comparison.
- The catalysts may alter separate pathways, may change their active-state population, or may simply have different stability. The current data cannot distinguish these mechanisms.
- The solvent pattern could arise from intrinsic pathway selectivity, catalyst-state effects, phase/transport behavior, or benchmark-specific categorical parameters. Since mixing was fixed and no phase measurement was made, these remain competing explanations.
- The decline in long-time yield could reflect true P-to-D degradation, catalyst deactivation followed by continued background side reaction, or an assay response change as the impurity mixture evolves. The parallel-plus-sequential model is the most economical explanation, not a uniquely proven one.
- The extreme pre-quench risk at 430 K may represent stored heat, an active reactive intermediate, a nonlinear temperature hazard model, or a combination. Only the public risk observable is known.

10. Overall conclusion

Within the explored domain, the world behaves like an irreversible but selectivity-limited catalytic conversion. Catalyst and solvent control the partition between desired and undesired pathways; exposure time permits both additional conversion and accumulating product loss/byproduct formation; temperature can accelerate entry into the useful kinetic window but creates a sharply rising transient safety burden. Water and Catalyst A gave the most favorable pathway partition. A short 410 K treatment followed by prompt quench best balanced formation, selectivity, degradation suppression, and safety. This explanation is well supported locally by Batches 1–12, but it should not be extrapolated to other loadings, concentrations, mixing regimes, or temperatures beyond the tested range without new evidence.

## Q — Blind predictions

### Overall rationale

Predictions use the campaign-supported parallel-plus-sequential model in which catalyst loading and temperature accelerate reactant consumption, while long exposure promotes byproduct formation and target loss. Yield was kept approximately consistent with conversion multiplied by selectivity. Catalyst B and acetonitrile were assigned poorer pathway discrimination than the recommended water–Catalyst A system. Safety estimates include a nonlinear hot-state term and a substantial quench benefit. Intervals are deliberately broad because these batches use a smaller scale, different concentrations and stirring, untested catalyst loadings, mostly omit quench, and extend to 465 K, whereas the campaign varied only full-charge formulations and reached 430 K.

### Q01

A short 410 K exposure with low Catalyst B loading should give partial conversion. The short residence time preserves moderate selectivity despite acetonitrile, while omission of quench leaves some thermal risk.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2500 | 0.1300 | 0.4000 |
| conversion | 0.5200 | 0.3600 | 0.6800 |
| safety_risk | 0.1800 | 0.1100 | 0.2800 |
| score | 0.1250 | 0.0600 | 0.2000 |
| selectivity | 0.5400 | 0.3900 | 0.6700 |
| yield | 0.2800 | 0.1800 | 0.3900 |

### Q02

Four hours at 410 K should nearly exhaust the reactant even at low catalyst loading, but prolonged exposure in acetonitrile is expected to shift most converted material into byproduct or degradation channels. The unquenched hot state may approach or exceed the safety limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7900 | 0.6500 | 0.9200 |
| conversion | 0.9800 | 0.9300 | 1.0000 |
| safety_risk | 0.3800 | 0.2500 | 0.5500 |
| score | 0.0190 | 0.0030 | 0.0600 |
| selectivity | 0.1700 | 0.0700 | 0.3000 |
| yield | 0.1700 | 0.0700 | 0.2900 |

### Q03

The high catalyst loading should produce rapid conversion during the short 410 K treatment. Limited residence time restrains secondary loss, although Catalyst B and acetonitrile are both expected to be less selective than the water–Catalyst A combination.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4900 | 0.3400 | 0.6600 |
| conversion | 0.9300 | 0.8200 | 0.9900 |
| safety_risk | 0.1900 | 0.1200 | 0.2900 |
| score | 0.1600 | 0.0800 | 0.2500 |
| selectivity | 0.4600 | 0.3200 | 0.5900 |
| yield | 0.4300 | 0.2900 | 0.5600 |

### Q04

High catalyst loading combined with four hours at 410 K should drive virtually complete conversion but severe over-processing. The prediction assigns most converted material to aggregate byproducts and gives a low score because both selectivity and unquenched safety are unfavorable.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8800 | 0.7500 | 0.9700 |
| conversion | 0.9980 | 0.9700 | 1.0000 |
| safety_risk | 0.4000 | 0.2700 | 0.5800 |
| score | 0.0060 | 0.0005 | 0.0300 |
| selectivity | 0.1000 | 0.0300 | 0.2100 |
| yield | 0.1000 | 0.0300 | 0.2100 |

### Q05

At 350 K, the low catalyst loading should leave substantial reactant after two hours. Low conversion limits yield, but the relatively mild temperature and incomplete processing should retain better selectivity and low risk.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.1500 | 0.0700 | 0.2700 |
| conversion | 0.3400 | 0.2200 | 0.4800 |
| safety_risk | 0.1200 | 0.0700 | 0.1900 |
| score | 0.0950 | 0.0450 | 0.1600 |
| selectivity | 0.5700 | 0.4300 | 0.6900 |
| yield | 0.1900 | 0.1200 | 0.2900 |

### Q06

Two hours at 465 K is a severe extrapolation beyond the explored optimum. It should overcome the low catalyst loading and give high conversion, but extensive secondary chemistry and a large unquenched thermal hazard are expected to suppress yield and score.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.7600 | 0.5800 | 0.9200 |
| conversion | 0.9000 | 0.7800 | 0.9800 |
| safety_risk | 0.7000 | 0.4800 | 0.9100 |
| score | 0.0060 | 0.0000 | 0.0300 |
| selectivity | 0.1400 | 0.0400 | 0.2900 |
| yield | 0.1300 | 0.0400 | 0.2700 |

### Q07

High catalyst loading should make the 350 K treatment substantially more complete than Q05. The longer effective catalytic exposure also promotes the poor-selectivity behavior observed for Catalyst B and acetonitrile, leaving a moderate yield and byproduct-rich mixture.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4800 | 0.3400 | 0.6300 |
| conversion | 0.8200 | 0.6900 | 0.9200 |
| safety_risk | 0.1300 | 0.0800 | 0.2100 |
| score | 0.1150 | 0.0550 | 0.1900 |
| selectivity | 0.4000 | 0.2700 | 0.5300 |
| yield | 0.3300 | 0.2200 | 0.4500 |

### Q08

This combines the largest catalyst loading with the harshest sustained temperature. Conversion should saturate, while target material is predicted to be largely replaced by byproduct or degradation channels. The unquenched safety risk is expected to be far above the declared limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9400 | 0.8300 | 1.0000 |
| conversion | 0.9950 | 0.9600 | 1.0000 |
| safety_risk | 0.7300 | 0.5200 | 0.9300 |
| score | 0.0007 | 0.0000 | 0.0060 |
| selectivity | 0.0500 | 0.0100 | 0.1400 |
| yield | 0.0500 | 0.0100 | 0.1400 |

### Q09

The central catalyst loading and two-hour 410 K exposure should give high conversion but substantial secondary loss in acetonitrile. Without quench, residual thermal or reactive-state risk materially depresses the predicted score.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6800 | 0.5300 | 0.8200 |
| conversion | 0.9400 | 0.8600 | 0.9900 |
| safety_risk | 0.2900 | 0.1900 | 0.4300 |
| score | 0.0480 | 0.0150 | 0.0950 |
| selectivity | 0.2700 | 0.1500 | 0.4000 |
| yield | 0.2500 | 0.1400 | 0.3800 |

### Q10

The chemical endpoints should closely match Q09 because quench follows the completed heat exposure. Based on the campaign, quench should substantially reduce the final safety risk by collapsing the hot/reactive state, producing a modest score improvement.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6800 | 0.5300 | 0.8200 |
| conversion | 0.9400 | 0.8600 | 0.9900 |
| safety_risk | 0.1400 | 0.0900 | 0.2200 |
| score | 0.0580 | 0.0200 | 0.1150 |
| selectivity | 0.2700 | 0.1500 | 0.4000 |
| yield | 0.2500 | 0.1400 | 0.3800 |

### Q11

Four hours at 350 K should give high conversion at the central catalyst loading, but the long residence time is expected to accumulate byproduct and lower selectivity. Risk remains lower than for the hotter unquenched schedules.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.6100 | 0.4600 | 0.7600 |
| conversion | 0.8800 | 0.7700 | 0.9600 |
| safety_risk | 0.1600 | 0.1000 | 0.2500 |
| score | 0.0660 | 0.0250 | 0.1200 |
| selectivity | 0.3000 | 0.1800 | 0.4300 |
| yield | 0.2600 | 0.1500 | 0.3900 |

### Q12

A short 465 K treatment should rapidly generate product at the central catalyst loading and avoid some long-time degradation, but it remains outside the experimentally supported temperature range and lacks a quench. High transient safety risk therefore limits the predicted score.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4600 | 0.3100 | 0.6300 |
| conversion | 0.8000 | 0.6500 | 0.9100 |
| safety_risk | 0.4300 | 0.2900 | 0.6100 |
| score | 0.0730 | 0.0250 | 0.1400 |
| selectivity | 0.4000 | 0.2600 | 0.5400 |
| yield | 0.3200 | 0.2000 | 0.4500 |

## K2 — Retrospective analysis

1. Assessment of the initial information

The initial material packet contained only one substantive mechanistic prior: “The target pathway may be effectively irreversible on the public support,” with moderate confidence. It otherwise explicitly said that no task-specific nominal property dossier was supplied, that catalysts were anonymous benchmark formulations, and that solvent effects were categorical benchmark effects rather than real-chemistry predictions.

The irreversibility prior received limited support, but it was not proven. In Batch 1, conversion increased from 0.3809 after 3,600 s to 0.7675 after a further 7,200 s at 350 K. In Batch 8, it increased from 0.7313 after 14,400 s to 0.8084 after another 3,600 s at 330 K. Neither sequence showed regeneration of reactant. This is correctly described as an absence of counterevidence, not as a direct demonstration of irreversibility: I did not perform a perturbation, dilution, product-spike, or reverse-condition experiment that could reveal a reversible equilibrium.

The observed decline of yield and selectivity during extended processing does not refute irreversible reactant consumption. It instead motivated the K1 distinction between irreversible disappearance of reactant and imperfect stability of the target. K1 stated that the prior “remains plausible for reactant consumption, but it does not imply that the target itself is indefinitely stable.” That remains the most defensible reading.

The anonymity and categorical-effect warnings were respected. I did not infer a real catalyst identity or named synthesis. The solvent labels were operationally useful, but the data did not validate any real molecular solvation theory. No initial claim supplied catalyst rankings, solvent rankings, kinetic orders, activation energies, or a safety equation, so none of those could be tested against an initial dossier.

I am not aware of an initial substantive claim for which clear counterevidence appeared and was then knowingly ignored. The main danger was weaker: I sometimes treated a convenient phenomenological interpretation as more coherent than the sparse design strictly warranted. That concerns inference strength, not failure to correct a contradicted initial claim.

2. Experiments that formed or changed the interpretation

Batch 1 established the first useful baseline. Choosing water, Catalyst A, 350 K, and a total of 10,800 s was initially a pragmatic guess rather than a conclusion supported by prior material properties. The intermediate HPLC result and final assay were important because they showed increasing conversion and yield together with declining selectivity and rising byproduct signal. This was the first evidence against a model in which time merely moves the system monotonically toward a stable, selectively formed product.

Batches 2–4 genuinely formed the catalyst ranking. Under approximately matched water/350 K/10,800 s conditions, Catalyst A gave the highest observed score, 0.2135. Catalyst B gave slightly higher conversion and nominal yield but lower selectivity, a higher degradation warning, and a lower score of 0.2083. Catalysts C and D scored still lower. This changed the working objective from maximizing gross activity to maximizing effective pathway discrimination.

Batches 5–7 strongly changed my interpretation of solvent effects. Ethanol, acetonitrile, and toluene all gave higher conversion than water, yet lower yield/selectivity, larger byproduct signals, higher risk, and lower scores. These batches supported the K1 claim that water “does not appear to maximize gross reaction rate; it improves pathway discrimination and safety.” They also demonstrated that conversion was an inadequate optimization target.

Batch 8 most directly strengthened the secondary-loss hypothesis. Extending the 330 K treatment from 14,400 to 18,000 s increased conversion but reduced the final measured yield and selectivity while increasing byproduct signal. Because HPLC and final assay were different instruments, this was not a clean kinetic trace, but the joint direction of the changes was influential.

Batches 9–11 drove the shift toward hotter, shorter operation. Scores rose from 0.2357 at 370 K/7,200 s to 0.2520 at 390 K/5,400 s and 0.2570 at 410 K/4,200 s. Batch 12 then prevented an unchecked extrapolation to still higher temperature: 430 K/3,000 s improved selectivity and reduced byproduct signal but lowered conversion, yield, and score relative to Batch 11. Its pre-quench risk of 0.3299 also revealed a narrow transient safety margin.

Several choices were nevertheless based on unverified guesses. The initial baseline, the use of full available charge in every batch, the 20 K temperature increments, and the paired shortening of time as temperature rose were heuristic. The 330–430 K schedule was selected to find a high score efficiently, not to identify separate temperature and duration effects. Likewise, retaining 600 rpm assumed mixing was adequate without testing it.

3. Current competing mechanisms and what the experiments distinguish

K1 proposed a parallel-plus-sequential network: reactant forms target or byproduct, and target may subsequently be lost. This remains economical, but it is not unique.

The most important competing explanation is catalyst deactivation combined with continued uncatalyzed or weakly catalyzed side reaction. Under that model, the target need not undergo a literal P-to-D transformation. The catalyst could lose target-forming activity with time while reactant continues to disappear through a background pathway. The existing experiments distinguish both of these models from a simple one-step, constant-selectivity conversion because long exposure increased conversion while worsening the product distribution. They do not distinguish target degradation from selective-catalyst deactivation.

A second alternative is a changing response or aggregation of multiple impurity channels rather than chemical destruction of target. HPLC and final assay were not repeatedly applied to identical states, and the public signals do not map to identified species. Thus the apparent decline in target yield during Batch 8 could include cross-instrument differences and process noise.

A third competition concerns the hotter-shorter trend. K1 suggested that the desired pathway might have a favorable apparent temperature response, while important losses depend on residence time. Equally plausibly, temperature itself may not improve intrinsic selectivity; the benefit may come almost entirely from shorter residence time. Because temperature and duration were changed together in Batches 8–12, activation-energy differences and residence-time effects are not separately identifiable.

For solvents, intrinsic kinetic selectivity competes with catalyst-state, phase, and mass-transfer explanations. The nonaqueous solvents increased conversion and worsened target selectivity, which establishes a robust operational ranking at the tested formulation. It does not reveal whether solvent changed elementary rate constants, catalyst stability, phase behavior, or transport.

For safety, the data support a hot-state contribution because Batch 12 rose to risk 0.3299 during heating and fell to 0.1473 after quench. However, stored sensible heat, reactive-intermediate inventory, and an abstract nonlinear temperature penalty remain observationally entangled.

4. One additional complete experiment I would choose

I would run the Batch 11 formulation again—0.080 L water, 0.040 mol reagent, 0.005 mol Catalyst A, and 600 rpm—but heat at 410 K for 5,400 s rather than 4,200 s. I would take one HPLC measurement at 4,200 s, continue heating for 1,200 s, quench, terminate, and perform the required final assay.

This single experiment would serve two purposes. The 4,200 s HPLC point would provide a partial replication of the Batch 11 state, while the final assay would test whether modestly extending the recommended schedule improves conversion or crosses into over-processing. It would not be a perfect replication because the instruments differ and sampling slightly perturbs volume, but it would be more informative than another isolated endpoint.

If the 4,200 s measurement resembled Batch 11 and the extra 1,200 s increased conversion and yield without materially reducing selectivity, the recommended duration was probably too short and the optimum would shift later. If conversion increased but yield or selectivity fell and byproduct rose, that would strengthen the sequential-loss or catalyst-deactivation interpretation and support prompt quenching near 4,200 s. If all chemical metrics changed very little, the system likely enters a broad kinetic plateau, making the operation more time-robust than the original data show. If the 4,200 s state differed substantially from Batch 11, batch variability or assay noise would become a dominant concern, and the claim that Batch 11 represented a reproducible optimum would weaken. A substantially higher transient risk at 5,400 s would also show that local time robustness is constrained by safety even if chemical yield improves.

5. Tradeoff between mechanistic identifiability and operational score

The campaign objective explicitly prioritized a strong safe score under a 0.35 risk limit. That objective shaped the design toward categorical screening followed by local optimization.

There was useful investment in identifiability. Batches 1–4 held the principal schedule approximately fixed while screening catalysts, and Batches 1 and 5–7 did the same for solvents. Those blocks isolated categorical effects reasonably well. Intermediate measurements in Batches 1 and 8 exposed time evolution that final assays alone would have hidden. These choices consumed batches that might otherwise have been devoted entirely to exploitation.

The later campaign clearly sacrificed identifiability for optimization. Temperature rose while duration fell, so the attractive trend from Batches 9–11 could be used to improve the score but could not yield separate temperature and time effects. I also did not replicate the best batch, test neighboring durations at exactly 410 K, vary catalyst loading, or include an uncatalyzed control. Those omissions made sense for finding a better operating point within twelve experiments, but they left the kinetic model underdetermined.

There was also some sacrifice of immediate score for learning. Batches 2–4 tested catalysts that proved inferior, and Batches 5–7 tested solvents that produced much lower scores. Batch 8 was deliberately cooler and longer and also scored poorly. These experiments were valuable because they established the operational landscape. By contrast, Batches 9–12 were increasingly exploitative.

The full-charge policy simplified comparisons and used the stock allocation evenly, but it prevented identification of concentration and catalyst-order effects. It also meant the eventual blind questions, which changed scale and catalyst loading, lay outside the well-supported design region.

6. Evidence that was underused and weaknesses in the blind predictions

The raw characterization artifacts and spectra were not inspected in detail. I relied on processed estimates rather than asking whether peak structure, signal saturation, missingness, or mass-balance information supported multiple byproduct channels. That evidence might have helped distinguish a single degradation product from a broad impurity distribution.

The public risk trajectory was also underused. Batch 12 made the quench effect obvious, but I did not systematically record pre-quench versus post-quench risk for every temperature. Consequently, the safety model in K1 remained qualitative. Cost quickly saturated at the displayed value of 1.0 and was not useful for discriminating recipes, but the underlying cost trajectory could still have clarified scaling.

I also did not fit even a simple quantitative kinetic model to all endpoints. Such a model would still have been weakly identifiable, but it could have made the temperature–time confounding and parameter uncertainty explicit rather than relying mainly on verbal trends.

The least reliable blind predictions are Q06, Q08, and Q12 because they use 465 K, above the highest studied 430 K, and omit quench. Q06 and Q08 also combine 7,200 s exposure with that extrapolated temperature. Their predicted risks and severe degradation depend on extending a nonlinear trend beyond direct evidence. The Q08 conversion interval of 0.96–1.00 and Q04 interval of 0.97–1.00 were probably too narrow: catalyst deactivation, a new high-temperature pathway, or scale-dependent heat behavior could prevent saturation. Their very low selectivity intervals may likewise have been overconfident.

Q02 and Q04 are also weak because 14,400 s at 410 K greatly exceeds the locally optimized exposure. Q01 and Q03 depend on extrapolating catalyst-loading effects without having varied loading in the campaign. Q09 and Q10 rely on the assumption that quench mainly changes risk rather than the chemical endpoint; the campaign supported rapid risk relief but did not directly compare quenched and unquenched otherwise identical batches. Q10 therefore deserved wider intervals for both score and chemical metrics.

All twelve blind questions used 0.005 L solvent, 0.003 mol reagent, 400 rpm, Catalyst B, and catalyst amounts not tested during the campaign. Thus even the apparently moderate cases involved simultaneous scale, concentration, mixing, catalyst-loading, catalyst-identity, and solvent changes. K1 explicitly stated that no kinetic orders or transport dependence could be claimed and that the interpretation should not be extrapolated to other loadings, concentrations, mixing regimes, or temperatures without new evidence. The blind rationale acknowledged this, but several numerical intervals did not fully honor that warning. In particular, near-boundary conversion forecasts and the precise quench benefit were more confident than the declared applicability warranted.

7. Limitations of the sealed recommendation

Batch 11 was the sample-best observed experiment, not a proven optimum. Its score of 0.2570 exceeded Batch 10’s 0.2520 by only about 0.005. Given assay noise, process variation, and the absence of replicates, that difference may not represent a reproducible ordering. The recommendation is therefore properly described as “highest observed under the sampled conditions,” not “globally optimal” or even conclusively locally optimal.

Repeatability should first be tested with independent exact replicates of Batch 11, including the same additions, 410 K target, 4,200 s duration, 600 rpm, quench, termination, and final assay. Replicates should record both pre-quench and post-quench risk. The relevant result would be the distribution of score and constraint compliance, not only the mean.

Local robustness should then be tested with a compact neighborhood around Batch 11: temperatures such as 400, 410, and 420 K; durations slightly below and above 4,200 s; and modest changes in catalyst loading and stirring. Temperature and time should be varied independently rather than along one diagonal. This would reveal whether Batch 11 lies on a broad plateau, a sharp optimum, or a safety-sensitive ridge.

Robustness to operational deviations also requires testing delayed quench, incomplete temperature tracking, and small charge variations. Batch 12 showed that transient risk can approach the limit before quench even when final risk looks comfortable, so endpoint safety alone is insufficient.

Cross-material generalization is especially limited. Catalyst A–D are anonymous categorical formulations, and their ranking need not transfer to another catalyst set. Water’s favorable effect is valid for this benchmark world and formulation, not a general claim about aqueous reaction chemistry. Generalization across worlds would require repeating at least the catalyst and solvent screening blocks and recalibrating the thermal-risk relationship.

Finally, the recommendation optimizes the public score contract, which combines measured performance and safety in this synthetic environment. It is not evidence of real process feasibility, real material compatibility, or a universally optimal chemical procedure. Its strongest defensible status is a promising, sample-best operating point within the tested benchmark domain, with good observed safety margin after quench but incomplete evidence for repeatability, transient robustness, and transportability.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 95.1 | none | 0 |
| Q | yes | 0 | 109.8 | none | 0 |
| K2 | yes | 0 | 107.8 | none | 0 |

## Scope note

This report contains only information available before truth release. Reference truth, prediction scoring, and recommendation retests are intentionally absent because the full 60-task block has not yet completed.
