# RX-W05--S--safety_constrained_optimization--Aligned

## Run summary

- World: `RX-W05`
- Locus: `S`
- Goal: `safety_constrained_optimization`
- Arm: `Aligned`
- Status: `completed`
- Source status: `completed`
- Experimental sessions: `12/12`
- Operations: `85`
- Exact replay verified: `True`
- Rollbacks: `[]`
- Posttest chain sealed: `True`

### Recovery status

- Effective result location: `source-repair-v11`
- Recovery version: `recovery-v11-parallel4-transport-repair`
- Repaired stages: `source`
- Source experiments rerun: `False`
- Original source thread reused: `False`
- Truth revealed during recovery: `False`

## Sealed recommendation

- Selected batch: `10`
- Rationale: Batch 10 gave the highest observed final safe score (0.3749) while remaining well below the 0.35 safety limit (risk 0.1588).

## Twelve-session experiment table

| Batch | Solvent | Reagent | Catalyst | Heat schedule | Quench | Yield | Selectivity | Conversion | Byproduct | Degradation | Safety | Score |
|---:|---|---|---|---|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S2 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 350 K x 3600 s @ 600 rpm → 370 K x 3600 s @ 600 rpm | no | 0.6481 | 0.7168 | 0.9042 | 0.2651 | 0.1237 | 0.2131 | 0.3330 |
| 2 | S2 (0.0800 L) | 0.040000 mol | C1 (0.005000 mol) | 365 K x 5400 s @ 700 rpm | no | 0.6136 | 0.6897 | 0.9094 | 0.2760 | 0.1832 | 0.2077 | 0.3154 |
| 3 | S2 (0.0800 L) | 0.040000 mol | C2 (0.005000 mol) | 350 K x 5400 s @ 700 rpm | no | 0.4065 | 0.6293 | 0.6693 | 0.2766 | 0.0540 | 0.1724 | 0.2093 |
| 4 | S2 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 5400 s @ 700 rpm | no | 0.6431 | 0.7319 | 0.8772 | 0.2437 | 0.1656 | 0.2015 | 0.3373 |
| 5 | S0 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 5400 s @ 700 rpm | no | 0.6270 | 0.7861 | 0.7989 | 0.1621 | 0.0823 | 0.1519 | 0.3589 |
| 6 | S1 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 5400 s @ 700 rpm | no | 0.5784 | 0.7058 | 0.7940 | 0.2352 | 0.1498 | 0.1751 | 0.3084 |
| 7 | S3 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 5400 s @ 700 rpm | no | 0.4869 | 0.5899 | 0.7905 | 0.3460 | 0.1796 | 0.1998 | 0.2313 |
| 8 | S0 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 340 K x 7200 s @ 700 rpm | no | 0.6282 | 0.7585 | 0.8150 | 0.1793 | 0.1123 | 0.1512 | 0.3544 |
| 9 | S0 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 345 K x 7200 s @ 700 rpm | no | 0.6538 | 0.7664 | 0.8485 | 0.2010 | 0.1112 | 0.1550 | 0.3682 |
| 10 | S0 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 7200 s @ 700 rpm | no | 0.6701 | 0.7608 | 0.8815 | 0.2048 | 0.1222 | 0.1588 | 0.3749 |
| 11 | S0 (0.0800 L) | 0.040000 mol | C0 (0.005000 mol) | 350 K x 7200 s @ 700 rpm | no | 0.5449 | 0.7390 | 0.7425 | 0.1993 | 0.0493 | 0.1417 | 0.3132 |
| 12 | S0 (0.0800 L) | 0.040000 mol | C3 (0.005000 mol) | 350 K x 9000 s @ 700 rpm | no | 0.6595 | 0.7227 | 0.9276 | 0.2605 | 0.1706 | 0.1624 | 0.3642 |

## Complete experimental actions and observations

### Batch 1

Lifecycle index: `1`; end step: `8`.

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
      "target_temperature_K": 350
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 370
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
    "byproduct_signal": 0.2650696933269501,
    "conversion": 0.9042196869850159,
    "cost": 1.0,
    "degradation_warning": 0.12366554141044617,
    "safety_risk": 0.2130700647830963,
    "score": 0.3329787850379944,
    "selectivity": 0.7168188691139221,
    "virtual_spectrum_summary": 0.2014378309249878,
    "yield": 0.6480840444564819
  },
  "ordinal": 1
}
```

### Batch 2

Lifecycle index: `2`; end step: `15`.

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
      "duration_s": 5400,
      "operation": "heat",
      "stirring_speed_rpm": 700,
      "target_temperature_K": 365
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
  "end_step": 15,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.2760384976863861,
    "conversion": 0.9093683958053589,
    "cost": 1.0,
    "degradation_warning": 0.1832190304994583,
    "safety_risk": 0.20766641199588776,
    "score": 0.31535810232162476,
    "selectivity": 0.6897261142730713,
    "virtual_spectrum_summary": 0.23426973819732666,
    "yield": 0.6135990619659424
  },
  "ordinal": 2
}
```

### Batch 3

Lifecycle index: `3`; end step: `22`.

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
      "duration_s": 5400,
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
  "end_step": 22,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.27661818265914917,
    "conversion": 0.6693220138549805,
    "cost": 1.0,
    "degradation_warning": 0.05399000644683838,
    "safety_risk": 0.17242532968521118,
    "score": 0.2092665433883667,
    "selectivity": 0.6292720437049866,
    "virtual_spectrum_summary": 0.17643550038337708,
    "yield": 0.4065193235874176
  },
  "ordinal": 3
}
```

### Batch 4

Lifecycle index: `4`; end step: `29`.

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
      "duration_s": 5400,
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
  "end_step": 29,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.24365878105163574,
    "conversion": 0.8772039413452148,
    "cost": 1.0,
    "degradation_warning": 0.16556739807128906,
    "safety_risk": 0.2014928162097931,
    "score": 0.33727699518203735,
    "selectivity": 0.731928825378418,
    "virtual_spectrum_summary": 0.2085176557302475,
    "yield": 0.6431154012680054
  },
  "ordinal": 4
}
```

### Batch 5

Lifecycle index: `5`; end step: `36`.

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
      "duration_s": 5400,
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
  "end_step": 36,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.16207876801490784,
    "conversion": 0.798904538154602,
    "cost": 1.0,
    "degradation_warning": 0.08228152990341187,
    "safety_risk": 0.15189649164676666,
    "score": 0.35889309644699097,
    "selectivity": 0.7861464619636536,
    "virtual_spectrum_summary": 0.12617000937461853,
    "yield": 0.6270486116409302
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
      "duration_s": 5400,
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
  "end_step": 43,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.23520967364311218,
    "conversion": 0.7939751148223877,
    "cost": 1.0,
    "degradation_warning": 0.14976145327091217,
    "safety_risk": 0.17513203620910645,
    "score": 0.30839547514915466,
    "selectivity": 0.7058190703392029,
    "virtual_spectrum_summary": 0.196757972240448,
    "yield": 0.5783815979957581
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
      "duration_s": 5400,
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
  "end_step": 50,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.3459819257259369,
    "conversion": 0.7904539108276367,
    "cost": 1.0,
    "degradation_warning": 0.17963451147079468,
    "safety_risk": 0.1998373121023178,
    "score": 0.23133806884288788,
    "selectivity": 0.5899159908294678,
    "virtual_spectrum_summary": 0.27112558484077454,
    "yield": 0.48685118556022644
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 700,
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
  "end_step": 57,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.17931585013866425,
    "conversion": 0.8149734735488892,
    "cost": 1.0,
    "degradation_warning": 0.11227329075336456,
    "safety_risk": 0.1511632353067398,
    "score": 0.35439398884773254,
    "selectivity": 0.758526623249054,
    "virtual_spectrum_summary": 0.1491466909646988,
    "yield": 0.6282211542129517
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 700,
      "target_temperature_K": 345
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
    "byproduct_signal": 0.2010088860988617,
    "conversion": 0.8484745025634766,
    "cost": 1.0,
    "degradation_warning": 0.1112145408987999,
    "safety_risk": 0.15504248440265656,
    "score": 0.36822688579559326,
    "selectivity": 0.7664461731910706,
    "virtual_spectrum_summary": 0.1606014370918274,
    "yield": 0.6538425087928772
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
      "duration_s": 7200,
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
  "end_step": 71,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.20479737222194672,
    "conversion": 0.881517767906189,
    "cost": 1.0,
    "degradation_warning": 0.12220508605241776,
    "safety_risk": 0.15883983671665192,
    "score": 0.3749103844165802,
    "selectivity": 0.7607669830322266,
    "virtual_spectrum_summary": 0.16763083636760712,
    "yield": 0.6701119542121887
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
      "duration_s": 7200,
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
  "end_step": 78,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.19932742416858673,
    "conversion": 0.7425422072410583,
    "cost": 1.0,
    "degradation_warning": 0.04928876832127571,
    "safety_risk": 0.14167971909046173,
    "score": 0.31318363547325134,
    "selectivity": 0.738955557346344,
    "virtual_spectrum_summary": 0.1318100392818451,
    "yield": 0.5448659658432007
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
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 9000,
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
  "end_step": 85,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.2605476379394531,
    "conversion": 0.9275909662246704,
    "cost": 1.0,
    "degradation_warning": 0.17058877646923065,
    "safety_risk": 0.16236676275730133,
    "score": 0.3641601800918579,
    "selectivity": 0.7227001190185547,
    "virtual_spectrum_summary": 0.2200661599636078,
    "yield": 0.6594777703285217
  },
  "ordinal": 12
}
```

## K1 — Mechanistic report

Mechanistic report

1. Scope and evidentiary status

This report describes the synthetic benchmark world supported by the completed 12-batch campaign. It is not a claim about a named real reaction. The reagent, reaction species, and catalysts are anonymous, while the named solvents act as calibrated categorical benchmark variables; their behavior should not be extrapolated from real-world solvent properties alone.

All batches used 0.040 mol reagent, 0.080 L solvent, and 0.005 mol catalyst. Except for batch 1, stirring was fixed at 700 rpm; batch 1 used 600 rpm. Consequently, the campaign identifies relative effects of catalyst, solvent, temperature, and time over this narrow recipe, but does not identify concentration, catalyst-loading, addition-order, or mixing laws.

2. Proposed process model

The observations are consistent with an effectively irreversible network containing a desired pathway and at least one competing or subsequent loss pathway:

R → P
R → B
P → D

Here R is the public reactant, P the target product, B a competing byproduct pool, and D a thermally generated degradation pool. A minimal kinetic representation is

dR/dt = −(kP + kB)R,
dP/dt = kP R − kD P,
dB/dt = kB R + φkD P.

The rate constants depend jointly on catalyst c, solvent s, and temperature:

kj(T,c,s) = Aj(c,s) exp[−Ej(c,s)/(RT)].

This is a useful phenomenological model, not an identified molecular mechanism. Catalyst and solvent may alter both prefactors and apparent activation barriers. The product-loss term is motivated by the decline in selectivity and rise in degradation at long residence time, although a conversion-dependent parallel side reaction could also explain those trends.

The measured quantities approximately satisfy

yield ≈ conversion × selectivity.

For example, batch 10 gave conversion 0.8815 and selectivity 0.7608, whose product is 0.6707, close to the measured yield of 0.6701. Batch 5 similarly gave 0.7989 × 0.7861 = 0.6281 versus yield 0.6270. The byproduct signal is also close to, but not exactly, conversion × (1 − selectivity), suggesting that conversion is partitioned primarily between target and byproduct, with degradation, calibration, and mass-balance effects accounting for the residual.

Temperature behaved like a controlled thermal state approaching the set point rather than changing instantaneously. From an approximately ambient starting state, a 350 K set point produced a temperature rise near 49.14 K after 5400–7200 s. Batch 8 at 340 K rose 40.11 K, and batch 9 at 345 K rose 44.65 K. A generic representation is

dT/dt = (Tset − T)/τ + Qreaction/(ρCpV) − Qloss/(ρCpV).

The present experiments do not separate controller dynamics from reaction heat release.

3. Safety-risk behavior

The public safety-risk scalar was path-dependent and accumulated contributions from charging and heating. It should be interpreted as the benchmark constraint variable, not as a calibrated real-world accident probability.

With 0.040 mol reagent, the initial risk was 0.03631. Charging 0.080 L solvent produced strongly solvent-dependent setup risks before heating: approximately 0.07219 for water, 0.09559 for ethanol, 0.11359 for acetonitrile, and 0.12619 for toluene. Catalyst addition itself produced no visible risk increment at this loading.

Heating added risk as a coupled function of temperature, duration, solvent, and catalyst activity. For Catalyst D in water, total final risk rose from 0.15116 at 340 K for 7200 s to 0.15504 at 345 K and 0.15884 at 350 K. Extending the 350 K treatment to 9000 s increased it to 0.16237. Catalyst identity also mattered: at 350 K for 7200 s in water, Catalyst A ended at risk 0.14168, whereas Catalyst D ended at 0.15884. This is consistent with a reaction-rate or heat-release coupling rather than risk being determined solely by the heater set point.

A useful empirical form is

risk = rcharge(reagent, solvent, concentration) + ∫ g[T(t), c, s, reaction rate]dt,

where g increases with thermal severity and, apparently, catalyst activity. Every completed batch remained below the declared limit of 0.35; the largest observed final risk was 0.21307 in batch 1.

4. Catalyst effects

Catalyst D was the strongest tested performer. The cleanest direct comparison was in acetonitrile at 350 K for 5400 s:

• Batch 3, Catalyst C: conversion 0.6693, yield 0.4065, selectivity 0.6293, byproduct 0.2766, degradation 0.0540, risk 0.1724, score 0.2093.
• Batch 4, Catalyst D: conversion 0.8772, yield 0.6431, selectivity 0.7319, byproduct 0.2437, degradation 0.1656, risk 0.2015, score 0.3373.

Thus Catalyst D was much more active and gave both greater yield and selectivity than Catalyst C under that matched condition, although its higher activity coincided with greater thermal risk and degradation.

A matched water comparison at 350 K for 7200 s also favored D:

• Batch 11, Catalyst A: conversion 0.7425, yield 0.5449, selectivity 0.7390, degradation 0.0493, risk 0.1417, score 0.3132.
• Batch 10, Catalyst D: conversion 0.8815, yield 0.6701, selectivity 0.7608, degradation 0.1222, risk 0.1588, score 0.3749.

Catalyst A was milder and generated less degradation, but its lower conversion outweighed that advantage. Catalyst B was examined only in batch 2 under a different, hotter acetonitrile schedule: 365 K for 5400 s gave conversion 0.9094, yield 0.6136, selectivity 0.6897, degradation 0.1832, risk 0.2077, and score 0.3154. Because temperature was not matched, these data establish that B can be active but do not cleanly rank its intrinsic activity against D.

5. Solvent effects

Batches 4–7 provide a matched solvent comparison using Catalyst D at 350 K for 5400 s:

• Water, batch 5: conversion 0.7989, yield 0.6270, selectivity 0.7861, byproduct 0.1621, degradation 0.0823, risk 0.1519, score 0.3589.
• Ethanol, batch 6: conversion 0.7940, yield 0.5784, selectivity 0.7058, byproduct 0.2352, degradation 0.1498, risk 0.1751, score 0.3084.
• Acetonitrile, batch 4: conversion 0.8772, yield 0.6431, selectivity 0.7319, byproduct 0.2437, degradation 0.1656, risk 0.2015, score 0.3373.
• Toluene, batch 7: conversion 0.7905, yield 0.4869, selectivity 0.5899, byproduct 0.3460, degradation 0.1796, risk 0.1998, score 0.2313.

Water was the best selectivity and safety medium. Acetonitrile accelerated conversion and slightly exceeded water in absolute yield under this particular 5400 s condition, but it generated more byproduct and degradation and had substantially higher risk, producing a lower safe score. Ethanol was intermediate. Toluene was poorest, primarily because of low selectivity and high byproduct formation.

These results imply that solvent changes more than the desired rate constant: it changes the relative desired, byproduct, and degradation rates as well as the charging-risk baseline. Because solvent is a categorical benchmark effect, polarity, boiling point, or other real physical properties cannot be asserted as the cause.

6. Temperature and residence-time effects in the best catalyst–solvent pair

Catalyst D in water gave the clearest local response surface.

At a fixed 7200 s duration:

• Batch 8, 340 K: conversion 0.8150, yield 0.6282, selectivity 0.7585, byproduct 0.1793, degradation 0.1123, risk 0.1512, score 0.3544.
• Batch 9, 345 K: conversion 0.8485, yield 0.6538, selectivity 0.7664, byproduct 0.2010, degradation 0.1112, risk 0.1550, score 0.3682.
• Batch 10, 350 K: conversion 0.8815, yield 0.6701, selectivity 0.7608, byproduct 0.2048, degradation 0.1222, risk 0.1588, score 0.3749.

Conversion and yield increased monotonically over 340–350 K. Selectivity was nearly flat within a narrow band, while byproduct and risk increased. In this tested range, the conversion gain dominated, so the safe score peaked at the highest tested temperature.

At a fixed 350 K set point:

• Batch 5, 5400 s: conversion 0.7989, yield 0.6270, selectivity 0.7861, byproduct 0.1621, degradation 0.0823, score 0.3589.
• Batch 10, 7200 s: conversion 0.8815, yield 0.6701, selectivity 0.7608, byproduct 0.2048, degradation 0.1222, score 0.3749.
• Batch 12, 9000 s: conversion 0.9276, yield 0.6595, selectivity 0.7227, byproduct 0.2605, degradation 0.1706, score 0.3642.

This is the strongest evidence for an optimum residence time. Extending from 5400 to 7200 s raised conversion enough to improve yield and score. Extending to 9000 s raised conversion further but lowered selectivity, increased byproduct and degradation, and reduced yield and score. This behavior is naturally explained by product degradation or an increasingly important side pathway at high conversion.

7. Batch 1 and evidence for thermal-history coupling

Batch 1 used Catalyst A in acetonitrile with two sequential heat stages: 350 K for 3600 s followed by 370 K for 3600 s. Its final assay gave conversion 0.9042, yield 0.6481, selectivity 0.7168, byproduct 0.2651, degradation 0.1237, risk 0.2131, and score 0.3330. The first stage alone had an HPLC estimate of conversion 0.5982 and yield 0.4619. The large subsequent conversion increase shows that thermal history and cumulative exposure matter; the final state cannot be represented adequately by set point alone.

Nevertheless, batch 1 cannot determine whether staged heating has a special mechanistic effect because it lacks a matched isothermal control with the same catalyst, solvent, total duration, and integrated temperature exposure.

8. Interpretation of the score

The exact scoring equation was not exposed. Empirically, score increased with target yield and selectivity and decreased with byproduct, degradation, and safety risk. Yield alone was insufficient: batch 12 had conversion 0.9276 and yield 0.6595 but scored below batch 10 because its selectivity and degradation profile were worse. Conversely, very mild conditions sacrificed too much conversion.

All batches used the same maximum reagent, solvent, and catalyst charges, and their displayed cost was saturated at 1. Therefore, this campaign cannot determine whether cost contributes to the score below that saturation point. The recommendation of batch 10 is based on its directly observed final score of 0.3749, the highest of the 12 completed batches, with risk 0.1588, comfortably below 0.35.

9. Measurement limitations

Each batch had one intermediate HPLC measurement followed by termination and a final assay. The two instruments generally agreed on qualitative trends, but they were not perfectly interchangeable. For example, batch 8 reported intermediate HPLC selectivity 0.8200 but final-assay selectivity 0.7585. Batch 12 reported intermediate selectivity 0.6723 and final selectivity 0.7227. Some differences exceed what would be expected from the nominal analytical standard deviations alone, so they may include sampling variation, instrument-specific calibration, process variability, or state changes associated with elapsed measurement and termination steps.

The final recommendations and numerical comparisons above use the final assays unless explicitly identified as intermediate measurements. Small differences, especially a few hundredths, should not be overinterpreted. The repeated temperature/time patterns are more reliable than any single assay fluctuation.

10. What remains unidentified

The following factors were not independently varied and therefore remain unidentified:

• Reaction order in reagent, catalyst, product, or byproduct.
• Catalyst-loading dependence and whether saturation or inhibition occurs.
• Concentration and solvent-volume effects.
• Addition-order effects.
• Mixing or mass-transfer dependence, because stirring was essentially fixed.
• Behavior outside 340–370 K, and especially near the 0.35 safety limit.
• Whether cooling, waiting, or quenching changes selectivity.
• Molecular identities, elementary steps, activation energies, reaction enthalpy, and phase behavior.
• Whether the degradation warning represents conversion of P into one species or a broader correlated damage signal.
• The exact safe-score function and any cost dependence below the displayed saturation.

The initial structural prior suggested effective irreversibility, and monotonic conversion with greater thermal exposure is consistent with that prior. However, no reverse-reaction or equilibrium experiment was conducted, so irreversibility is not proven.

11. Reasonable competing explanations

The preferred explanation is a desired reaction followed by or competing with thermally accelerated degradation. Several alternatives remain viable:

• Two purely parallel irreversible pathways, with selectivity changing as temperature, solvent, catalyst state, or reagent concentration evolves, could mimic apparent P → D behavior.
• Catalyst deactivation could cause diminishing desired production while a noncatalytic side reaction continues.
• Product or byproduct inhibition could alter the apparent rate and selectivity at high conversion.
• The degradation warning may be a correlated spectral proxy rather than a distinct chemical pool.
• Instrument-specific response factors could account for part of the observed selectivity changes.

The campaign does not distinguish these alternatives decisively. The sequential-loss model is favored because, for Catalyst D in water at 350 K, extending residence time from 7200 to 9000 s increased conversion but decreased both yield and selectivity while sharply increasing byproduct and degradation. That is the expected signature of overprocessing, but it is not unique proof of a particular elementary mechanism.

12. Final operating interpretation

Within the experimentally supported domain, the world is best treated as a thermally activated, effectively irreversible selectivity problem with categorical catalyst–solvent coupling and path-dependent safety accumulation. Catalyst D supplies the strongest useful activity; water suppresses charging risk and unwanted pathways; moderate heating improves conversion; and excessive residence time converts the incremental benefit into byproduct and degradation.

The best observed compromise was batch 10: 0.040 mol reagent, 0.080 L water, 0.005 mol Catalyst D, heating at 350 K for 7200 s with 700 rpm stirring, followed by termination and final assay. Its final observed values were yield 0.6701, selectivity 0.7608, conversion 0.8815, byproduct signal 0.2048, degradation warning 0.1222, safety risk 0.1588, and score 0.3749. Claims about behavior between nearby tested conditions are modest interpolation; claims outside the tested recipe, catalyst loading, solvent set, and thermal range would be extrapolation.

## Q — Blind predictions

### Overall rationale

Predictions were extrapolated from the Catalyst B/acetonitrile result in campaign batch 2 and from the broader temperature-time patterns observed across all 12 campaign batches. I treated conversion as an approximately irreversible, thermally activated process whose apparent rate scales with catalyst concentration, and treated yield as approximately conversion multiplied by selectivity. Selectivity was reduced with increasing temperature and cumulative exposure to represent parallel byproduct formation and subsequent product degradation. Safety risk was modeled qualitatively as a charging baseline plus an accumulated term increasing with temperature, time, and catalyst activity. The intervals include final-assay noise but are dominated by structural uncertainty because the queries use much smaller volumes, untested catalyst loadings, 400 rpm stirring, reversed charging order, and temperatures up to 465 K, well beyond the campaign's main 340–370 K range. Values near zero or one are therefore boundary-limited predictions rather than precise determinations.

### Q01

The low catalyst concentration should limit conversion during the short treatment, despite strong thermal acceleration at 410 K. High temperature is expected to reduce selectivity relative to the observed 365 K Catalyst B batch.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2600 | 0.1300 | 0.4300 |
| conversion | 0.6800 | 0.4800 | 0.8400 |
| safety_risk | 0.2000 | 0.1100 | 0.3200 |
| score | 0.2000 | 0.0800 | 0.3200 |
| selectivity | 0.6200 | 0.4500 | 0.7600 |
| yield | 0.4200 | 0.2500 | 0.5900 |

### Q02

Four hours at 410 K should nearly exhaust the reactant even at low catalyst loading. The long, hot exposure is predicted to shift most converted material into byproduct or degradation channels and to exceed the safety limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8200 | 0.6300 | 0.9600 |
| conversion | 0.9900 | 0.9400 | 1.0000 |
| safety_risk | 0.6200 | 0.3800 | 0.8800 |
| score | 0.0050 | 0.0000 | 0.0800 |
| selectivity | 0.1500 | 0.0300 | 0.3200 |
| yield | 0.1400 | 0.0200 | 0.3000 |

### Q03

The high catalyst concentration should drive nearly complete conversion in 1800 s. Short residence time retains appreciable product, but the 410 K temperature likely causes poorer selectivity and higher risk than the observed Catalyst B reference.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.4300 | 0.2700 | 0.6100 |
| conversion | 0.9800 | 0.9000 | 1.0000 |
| safety_risk | 0.3900 | 0.2200 | 0.6200 |
| score | 0.1700 | 0.0400 | 0.3000 |
| selectivity | 0.5500 | 0.3700 | 0.7000 |
| yield | 0.5400 | 0.3600 | 0.6900 |

### Q04

High catalyst loading and four hours at 410 K constitute extreme overprocessing. Conversion should saturate, while secondary chemistry and accumulated thermal risk should dominate the final state.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9300 | 0.8000 | 1.0000 |
| conversion | 1.0000 | 0.9800 | 1.0000 |
| safety_risk | 0.9500 | 0.7000 | 1.0000 |
| score | 0.0010 | 0.0000 | 0.0300 |
| selectivity | 0.0500 | 0.0000 | 0.1600 |
| yield | 0.0400 | 0.0000 | 0.1400 |

### Q05

At 350 K the low catalyst concentration is expected to leave substantial reactant after 7200 s. The material that does react should be relatively selective, with limited byproduct formation and low risk.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.0800 | 0.0300 | 0.1700 |
| conversion | 0.3800 | 0.2200 | 0.5600 |
| safety_risk | 0.1400 | 0.0800 | 0.2300 |
| score | 0.1900 | 0.0900 | 0.3000 |
| selectivity | 0.8000 | 0.6700 | 0.8900 |
| yield | 0.3000 | 0.1600 | 0.4500 |

### Q06

The very high temperature should overwhelm the low catalyst limitation over two hours. Nearly complete conversion is predicted, but with extensive product loss, byproduct formation, and severe safety-limit violation.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9600 | 0.8700 | 1.0000 |
| conversion | 1.0000 | 0.9900 | 1.0000 |
| safety_risk | 0.9200 | 0.6500 | 1.0000 |
| score | 0.0010 | 0.0000 | 0.0300 |
| selectivity | 0.0300 | 0.0000 | 0.1000 |
| yield | 0.0200 | 0.0000 | 0.0800 |

### Q07

High catalyst loading compensates for the moderate temperature and should produce high conversion. Selectivity should remain substantially better than at 410–465 K, making this the strongest predicted batch among the queries, although Catalyst B in acetonitrile remains less favorable than the campaign optimum.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.2300 | 0.1200 | 0.3700 |
| conversion | 0.8700 | 0.7200 | 0.9600 |
| safety_risk | 0.2300 | 0.1300 | 0.3700 |
| score | 0.3250 | 0.2000 | 0.4300 |
| selectivity | 0.7400 | 0.6000 | 0.8400 |
| yield | 0.6400 | 0.4700 | 0.7800 |

### Q08

This combines the highest catalyst concentration with the most severe two-hour temperature. It should give saturated conversion but almost complete diversion or degradation of target product and near-maximal safety risk.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9800 | 0.9100 | 1.0000 |
| conversion | 1.0000 | 0.9900 | 1.0000 |
| safety_risk | 0.9900 | 0.8200 | 1.0000 |
| score | 0.0010 | 0.0000 | 0.0200 |
| selectivity | 0.0100 | 0.0000 | 0.0600 |
| yield | 0.0050 | 0.0000 | 0.0400 |

### Q09

The intermediate catalyst concentration is close to the campaign concentration on a volume basis. At 410 K for 7200 s it should reach essentially complete conversion, followed by substantial overprocessing and a large safety-limit violation.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8000 | 0.6100 | 0.9400 |
| conversion | 0.9950 | 0.9700 | 1.0000 |
| safety_risk | 0.7200 | 0.4800 | 0.9400 |
| score | 0.0100 | 0.0000 | 0.0800 |
| selectivity | 0.1800 | 0.0500 | 0.3500 |
| yield | 0.1800 | 0.0400 | 0.3400 |

### Q10

Quenching occurs only after the full thermal exposure, so I predict little change in conversion or composition relative to Q09. It may add a small operational risk increment; the lack of campaign quench data makes this difference especially uncertain.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.8000 | 0.6100 | 0.9400 |
| conversion | 0.9950 | 0.9700 | 1.0000 |
| safety_risk | 0.7400 | 0.5000 | 0.9600 |
| score | 0.0080 | 0.0000 | 0.0800 |
| selectivity | 0.1800 | 0.0500 | 0.3500 |
| yield | 0.1800 | 0.0400 | 0.3400 |

### Q11

The moderate temperature limits instantaneous side chemistry, while the four-hour duration should produce high conversion. The extended residence time should nevertheless lower selectivity relative to a shorter 350 K run and create appreciable byproduct.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.3200 | 0.1900 | 0.4700 |
| conversion | 0.9100 | 0.7800 | 0.9800 |
| safety_risk | 0.2500 | 0.1400 | 0.4100 |
| score | 0.2760 | 0.1300 | 0.3900 |
| selectivity | 0.6500 | 0.5000 | 0.7700 |
| yield | 0.5900 | 0.4200 | 0.7200 |

### Q12

Even the short 1800 s exposure should give nearly complete conversion at 465 K. Very rapid competing and degradation pathways are expected to leave little target and to drive risk far above the declared limit.

| Metric | Point estimate | 80% lower | 80% upper |
|---|---:|---:|---:|
| byproduct_signal | 0.9000 | 0.7400 | 0.9900 |
| conversion | 0.9950 | 0.9700 | 1.0000 |
| safety_risk | 0.8600 | 0.5700 | 1.0000 |
| score | 0.0030 | 0.0000 | 0.0600 |
| selectivity | 0.0800 | 0.0100 | 0.2200 |
| yield | 0.0800 | 0.0100 | 0.2100 |

## K2 — Retrospective analysis

1. Initial claims: supported, challenged, or untested

The initial material packet contained only one substantive mechanistic prior: the target pathway “may be effectively irreversible on the public support,” with moderate confidence. It supplied no task-specific property dossier and explicitly stated that the named solvents had categorical benchmark effects rather than physically inferred real-solvent behavior.

The campaign found no clear evidence against effective irreversibility. Conversion generally increased with greater thermal exposure: for Catalyst D in water, final conversion rose from 0.7989 in batch 5 at 350 K for 5400 s, to 0.8815 in batch 10 at 7200 s, and to 0.9276 in batch 12 at 9000 s. Batch 1 likewise increased substantially after its second heating stage. This is consistency with irreversibility, not proof of it. No experiment began from isolated product, perturbed an equilibrium, or tested a reverse direction. K1 therefore correctly said that irreversibility was “not proven.”

There was also no evidence that justified assigning real molecular identities or real-solvent property mechanisms to the anonymous system. The strong water/acetonitrile/toluene differences supported the existence of solvent coupling, but not a physical explanation based on polarity or boiling point. That limitation from the initial packet remained fully applicable.

The simple sequential-loss interpretation R → P → D did encounter ambiguous evidence. The between-batch time series supported it, but within batch 12 the intermediate HPLC selectivity was 0.6723 whereas the final assay reported 0.7227. A literal model in which selectivity must only decline with additional elapsed time would not predict that increase. I did not treat it as decisive counterevidence because the measurements came from different instruments and K1 explicitly noted substantial HPLC/final-assay disagreement. Nevertheless, it is an observed tension, not merely an absence of support. K1 appropriately retained parallel reaction, catalyst deactivation, inhibition, and measurement response as competitors rather than presenting sequential degradation as established fact.

2. Experiments that formed or changed the interpretation

Batch 1 formed the first quantitative view of the system. After Catalyst A in acetonitrile was heated at 350 K for 3600 s, HPLC showed conversion 0.5982 and yield 0.4619; after a second 370 K stage, the final values were conversion 0.9042 and yield 0.6481. This established that additional thermal exposure could produce a large conversion gain, but its staged design confounded temperature and time.

Batch 2 became the only direct Catalyst B/acetonitrile anchor and was therefore disproportionately important for the later blind predictions. At 365 K for 5400 s it gave conversion 0.9094, selectivity 0.6897, degradation warning 0.1832, and risk 0.2077. During the campaign it primarily showed that Catalyst B could be active; only during the prediction task did it become the basis for extrapolating Catalyst B across new loadings and much higher temperatures.

The matched comparison between batches 3 and 4 genuinely changed the catalyst ranking. Under acetonitrile at 350 K for 5400 s, Catalyst D greatly exceeded Catalyst C in conversion, yield, selectivity, and score. That result motivated carrying D into the solvent screen.

Batches 4–7 were the most informative matched design. With Catalyst D at 350 K for 5400 s, water improved both safety and selectivity, while toluene produced the highest byproduct signal and lowest score. This established the D–water region as the best exploitation target and replaced the initially arbitrary acetonitrile choice.

Batches 8–10 then mapped a narrow temperature response at 7200 s. Their increasing conversion and score from 340 to 350 K justified moving to 350 K. Batches 5, 10, and 12 supplied the most important mechanistic pattern: at 350 K, extending residence from 5400 to 7200 s improved yield and score, but extending to 9000 s raised conversion while lowering selectivity and score. That observation produced K1’s overprocessing interpretation and selected 7200 s as the local compromise.

Batch 11 tested whether the milder risk profile of Catalyst A could compensate for lower activity. It did not: under matched water/350 K/7200 s conditions, A scored 0.3132 versus D’s 0.3749 in batch 10. This strengthened the D recommendation.

Several early choices rested mainly on unverified guesses. Using the maximum reagent, solvent, and catalyst charges was not supported by the initial dossier. Catalyst A and acetonitrile in batch 1 were starting benchmarks rather than evidence-based choices. Temperatures and durations in the first four batches were broad exploratory guesses. Stirring at 600 or 700 rpm was never validated. Later choices were increasingly data-driven, especially the move to Catalyst D, water, and the 340–350 K local series.

3. Leading competing mechanisms and what the campaign distinguishes

K1’s preferred phenomenology was an irreversible desired pathway plus parallel and sequential loss:

R → P, R → B, and P → D.

The strongest alternative is a purely parallel network in which the instantaneous branching fraction changes with temperature, catalyst state, reagent concentration, or conversion. Both models explain higher byproduct and lower selectivity under severe conditions. The existing endpoint assays do not uniquely distinguish them.

A second alternative is catalyst deactivation. Under that account, desired production slows with time while a background side reaction continues. A third is product or byproduct inhibition, which could make selectivity appear conversion-dependent without requiring direct product destruction. A fourth is that degradation_warning is primarily an analytical correlate rather than the abundance of a distinct degradation pool.

The campaign can distinguish several coarse effects. It clearly shows catalyst dependence, categorical solvent dependence, increasing conversion with thermal severity, and an empirical overprocessing region at 350 K beyond approximately 7200 s. It also shows that risk is path- and formulation-dependent rather than a function of set point alone.

It cannot distinguish elementary reaction order, parallel loss from sequential product destruction, deactivation from inhibition, or kinetic chemistry from some instrument-response effects. Because every batch used essentially one endpoint plus one HPLC sample, there was no common-instrument time course. Because the product was never isolated or re-exposed, direct P → D conversion was not tested.

4. The single additional experiment I would choose

I would repeat the recommended Catalyst D/water formulation with the same charging order and quantities, heat at 350 K and 700 rpm, take an HPLC measurement at 7200 s, continue heating at 350 K for another 1800 s, then terminate and perform the required final assay at 9000 s.

This experiment would be chosen for mechanistic discrimination rather than for seeking a new maximum. It would create a within-vessel trajectory spanning the conditions represented by batches 10 and 12, reducing between-batch variability. It would also serve as a partial replication of both conditions.

If conversion increased while target yield fell and byproduct/degradation rose, that would strengthen the sequential-loss or conversion-dependent late-side-reaction interpretation. If conversion and yield both increased with nearly constant selectivity, the apparent batch-12 overprocessing effect would look more like between-batch or measurement variability. If conversion stopped while byproduct continued to rise, product degradation or catalyst deactivation would become more likely than a stable parallel branching model. If conversion, yield, and byproduct all became nearly stationary, a kinetic plateau, deactivation, or equilibrium-like limitation would become more plausible. If the repeated 7200 s measurement differed substantially from batch 10 before the extension, reproducibility and instrument comparability would become the dominant concern.

The remaining limitation is that the intermediate HPLC and final assay are different instruments. A repeated common-instrument time series would be cleaner, but a legal complete batch still requires the final assay, and the campaign’s nonfinal measurement constraint makes the proposed experiment the most informative available compromise.

5. Tradeoff between identifiability and operating score

The primary research objective emphasized strong safe-score performance under a safety limit, so the campaign progressively shifted from exploration to exploitation. Batches 3–7 sacrificed immediate score to identify catalyst and solvent effects: Catalyst C and toluene were knowingly continued to final assay even after their intermediate evidence looked unfavorable. Those batches improved mechanistic and categorical identifiability at the cost of spending experiments on low-performing regions.

The later campaign made the opposite tradeoff. Batches 8–10 and 12 concentrated on Catalyst D in water near the apparent optimum. This improved local operating performance and revealed a useful temperature/time response, but it left large parts of the system unidentified. Catalyst B was not revisited under water or at matched temperatures; catalyst loading, reagent concentration, solvent volume, addition order, and stirring were never varied. The maximum catalyst charge was used throughout, so the campaign could not determine whether a lower-cost or lower-risk loading would retain most of the performance.

The fixed full charges also saturated the displayed cost metric at 1. This was an optimization weakness as well as an identifiability weakness: the design could neither learn the cost contribution to score nor discover a more material-efficient recipe. Conversely, the four-solvent screen and Catalyst C batch were useful scientifically but did not directly maximize the final score.

Thus the campaign achieved a reasonable exploration-to-exploitation progression, but the research goal pushed the final third toward a narrow local optimum. It did not produce a globally identifiable kinetic model.

6. Underused evidence and weaknesses in the blind predictions

The paired HPLC and final-assay results were not used as fully as they could have been. Their discrepancies could have been modeled explicitly as instrument-specific bias plus process variability. Instead, K1 used them mainly as a qualitative warning. Batch 8’s selectivity changed from 0.8200 by HPLC to 0.7585 by final assay, while batch 12 changed in the opposite direction, from 0.6723 to 0.7227. Those pairs weaken precise claims about small selectivity differences.

The operation receipts also separated charging-risk and heating-risk increments. K1 described these increments, but I did not fit a quantitative risk model. Actual temperature changes could have informed a controller time constant, but the observations were mostly long enough to be near their set points and therefore poorly suited to identifying transient heating behavior. Score variation could have been analyzed more formally, but cost was saturated and the predictors were strongly correlated.

The least reliable blind predictions were Q04, Q06, Q08, and Q12 because they extrapolated to 410–465 K, far beyond the main 340–370 K evidence, and often combined that extrapolation with untested catalyst concentrations. Q02, Q09, and Q10 were also weak because they assumed the form of long-duration degradation and risk accumulation at 410 K. Q10 was uniquely uncertain: K1 explicitly stated that quenching had not been studied, yet the prediction assumed little compositional effect and only a small added risk increment.

Even the nominally moderate-temperature predictions Q05, Q07, and Q11 depended on an unverified proportional relationship between Catalyst B concentration and reaction rate. They also involved 0.005 L batches, 400 rpm stirring, solvent-first charging, and reagent and catalyst concentrations not studied in the campaign. Q11 extended duration to 14400 s, beyond the campaign maximum of 9000 s.

Several prediction intervals were probably too narrow. In particular, the near-boundary conversion intervals and near-zero score intervals for the 465 K cases expressed more confidence in saturation and catastrophic selectivity loss than the evidence justified. The risk intervals for Q04, Q06, Q08, and Q12 may also have been too concentrated near one because no high-temperature risk curve had been measured. Q10’s interval did not fully reflect uncertainty about quench behavior. These weaknesses are consistent with, but more severe than, K1’s declared limitations: K1 explicitly said catalyst-loading dependence, stirring dependence, quenching, and behavior outside 340–370 K were unidentified. The prediction rationale acknowledged extrapolation, but some numerical intervals did not fully honor that structural uncertainty.

No prediction truth has yet been provided, so these are prospective criticisms of support and calibration, not post hoc explanations of prediction error.

7. Limitations of the sealed recommendation

The sealed recommendation selected batch 10 because its final score of 0.3749 was the highest observed score among the 12 completed batches and its risk of 0.1588 was below the 0.35 limit. This establishes only a sample-internal winner.

It does not prove that the procedure is globally optimal, locally optimal in expectation, or even the best of the tested procedures after accounting for assay and process noise. Nearby batches were close: batch 9 scored 0.3682 and batch 12 scored 0.3642. Batch 10’s intermediate HPLC-based visible score was 0.3672, illustrating that measurement realization can affect ranking. Selecting the largest of 12 noisy outcomes also creates a winner’s-curse risk.

Repeatability should first be tested with independent exact replicates of batch 10, reporting the distribution of final score, risk, conversion, yield, selectivity, byproduct, and degradation rather than a single mean. Local robustness should then be tested with small perturbations around 350 K, 7200 s, catalyst amount, stirring rate, and charge quantities. Conditions such as 345–355 K and roughly 6600–7800 s would reveal whether performance lies on a broad plateau or a narrow peak. Addition-order and small controller deviations should also be tested because the recommendation implicitly includes the campaign’s reagent–water–catalyst charging sequence.

Cross-material generalization would require matched tests with other catalysts and solvents near their own optima, not merely comparison at one common condition. Cross-world generalization would require independent benchmark worlds or seeds because all evidence came from one world realization. Since the material packet described categorical latent profiles, the superiority of Catalyst D in water should not be assumed to transfer to a different anonymous reaction system.

Accordingly, the defensible claim is: batch 10 was the highest-scoring observed completed batch in this campaign. The stronger claim that it is the optimal operating procedure has not been demonstrated.

## Posttest validation and execution metadata

| Stage | Valid | Exit code | Elapsed (s) | Failure | Provider errors |
|---|:---:|---:|---:|---|---:|
| K1 | yes | 0 | 114.8 | none | 0 |
| Q | yes | 0 | 165.4 | none | 0 |
| K2 | yes | 0 | 99.4 | none | 0 |

## Blind-prediction evaluation

| Metric | MAE to five-repeat mean | Empirical 80% coverage | Mean 80% width | Mean interval score |
|---|---:|---:|---:|---:|
| byproduct_signal | 0.2622 | 0.2667 | 0.2475 | 1.5990 |
| conversion | 0.0652 | 0.6167 | 0.1192 | 0.2771 |
| safety_risk | 0.3334 | 0.4167 | 0.3292 | 1.9287 |
| score | 0.1575 | 0.3333 | 0.1317 | 1.0974 |
| selectivity | 0.2774 | 0.2500 | 0.2325 | 1.8066 |
| yield | 0.2462 | 0.4167 | 0.2425 | 1.7053 |

## Predictions versus released reference truth

### Q01

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2600 | 0.1300 | 0.4300 | 0.1394 | 0.1397, 0.1462, 0.1413, 0.1384, 0.1316 |
| conversion | 0.6800 | 0.4800 | 0.8400 | 0.5419 | 0.5369, 0.5361, 0.5497, 0.5430, 0.5438 |
| safety_risk | 0.2000 | 0.1100 | 0.3200 | 0.2496 | 0.2496, 0.2496, 0.2496, 0.2496, 0.2496 |
| score | 0.2000 | 0.0800 | 0.3200 | 0.2633 | 0.2655, 0.2652, 0.2643, 0.2587, 0.2626 |
| selectivity | 0.6200 | 0.4500 | 0.7600 | 0.7421 | 0.7503, 0.7451, 0.7464, 0.7401, 0.7288 |
| yield | 0.4200 | 0.2500 | 0.5900 | 0.4090 | 0.4107, 0.4134, 0.4068, 0.3985, 0.4152 |
### Q02

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.8200 | 0.6300 | 0.9600 | 0.7361 | 0.7397, 0.7292, 0.7492, 0.7245, 0.7377 |
| conversion | 0.9900 | 0.9400 | 1.0000 | 0.9894 | 0.9940, 0.9820, 0.9971, 0.9889, 0.9850 |
| safety_risk | 0.6200 | 0.3800 | 0.8800 | 0.2515 | 0.2515, 0.2515, 0.2515, 0.2515, 0.2515 |
| score | 0.0050 | 0.0000 | 0.0800 | 0.1240 | 0.1282, 0.1246, 0.1241, 0.1240, 0.1192 |
| selectivity | 0.1500 | 0.0300 | 0.3200 | 0.2740 | 0.2821, 0.2767, 0.2785, 0.2713, 0.2612 |
| yield | 0.1400 | 0.0200 | 0.3000 | 0.2699 | 0.2741, 0.2715, 0.2653, 0.2716, 0.2669 |
### Q03

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.4300 | 0.2700 | 0.6100 | 0.1516 | 0.1469, 0.1490, 0.1465, 0.1682, 0.1471 |
| conversion | 0.9800 | 0.9000 | 1.0000 | 0.9045 | 0.9126, 0.8934, 0.9063, 0.9038, 0.9066 |
| safety_risk | 0.3900 | 0.2200 | 0.6200 | 0.2526 | 0.2526, 0.2526, 0.2526, 0.2526, 0.2526 |
| score | 0.1700 | 0.0400 | 0.3000 | 0.4366 | 0.4406, 0.4357, 0.4386, 0.4338, 0.4345 |
| selectivity | 0.5500 | 0.3700 | 0.7000 | 0.8453 | 0.8629, 0.8401, 0.8425, 0.8499, 0.8314 |
| yield | 0.5400 | 0.3600 | 0.6900 | 0.7624 | 0.7594, 0.7661, 0.7686, 0.7528, 0.7653 |
### Q04

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.9300 | 0.8000 | 1.0000 | 0.7894 | 0.7706, 0.7875, 0.8048, 0.7903, 0.7936 |
| conversion | 1.0000 | 0.9800 | 1.0000 | 0.9959 | 1.0000, 0.9907, 1.0000, 0.9890, 1.0000 |
| safety_risk | 0.9500 | 0.7000 | 1.0000 | 0.2519 | 0.2519, 0.2519, 0.2519, 0.2519, 0.2519 |
| score | 0.0010 | 0.0000 | 0.0300 | 0.0871 | 0.0917, 0.0894, 0.0841, 0.0875, 0.0830 |
| selectivity | 0.0500 | 0.0000 | 0.1600 | 0.2562 | 0.2603, 0.2645, 0.2443, 0.2601, 0.2517 |
| yield | 0.0400 | 0.0000 | 0.1400 | 0.2596 | 0.2675, 0.2614, 0.2583, 0.2597, 0.2510 |
### Q05

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.0800 | 0.0300 | 0.1700 | 0.2859 | 0.2874, 0.2976, 0.2794, 0.2754, 0.2894 |
| conversion | 0.3800 | 0.2200 | 0.5600 | 0.7070 | 0.7056, 0.7061, 0.7105, 0.7038, 0.7091 |
| safety_risk | 0.1400 | 0.0800 | 0.2300 | 0.1416 | 0.1416, 0.1416, 0.1416, 0.1416, 0.1416 |
| score | 0.1900 | 0.0900 | 0.3000 | 0.2914 | 0.2937, 0.2855, 0.2896, 0.2953, 0.2931 |
| selectivity | 0.8000 | 0.6700 | 0.8900 | 0.6004 | 0.6055, 0.5865, 0.5961, 0.6143, 0.5996 |
| yield | 0.3000 | 0.1600 | 0.4500 | 0.4163 | 0.4191, 0.4105, 0.4134, 0.4182, 0.4204 |
### Q06

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.9600 | 0.8700 | 1.0000 | 0.6099 | 0.6123, 0.6066, 0.6036, 0.6193, 0.6079 |
| conversion | 1.0000 | 0.9900 | 1.0000 | 0.9947 | 1.0000, 0.9837, 0.9990, 0.9934, 0.9973 |
| safety_risk | 0.9200 | 0.6500 | 1.0000 | 0.4259 | 0.4259, 0.4259, 0.4259, 0.4259, 0.4259 |
| score | 0.0010 | 0.0000 | 0.0300 | 0.1323 | 0.1345, 0.1397, 0.1227, 0.1333, 0.1313 |
| selectivity | 0.0300 | 0.0000 | 0.1000 | 0.3927 | 0.3842, 0.4258, 0.3714, 0.4011, 0.3809 |
| yield | 0.0200 | 0.0000 | 0.0800 | 0.3962 | 0.4056, 0.3968, 0.3843, 0.3939, 0.4005 |
### Q07

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.2300 | 0.1200 | 0.3700 | 0.3215 | 0.3256, 0.3232, 0.3132, 0.3178, 0.3278 |
| conversion | 0.8700 | 0.7200 | 0.9600 | 0.9676 | 0.9735, 0.9585, 0.9756, 0.9696, 0.9610 |
| safety_risk | 0.2300 | 0.1300 | 0.3700 | 0.1439 | 0.1439, 0.1439, 0.1439, 0.1439, 0.1439 |
| score | 0.3250 | 0.2000 | 0.4300 | 0.4053 | 0.4066, 0.4069, 0.4029, 0.4048, 0.4054 |
| selectivity | 0.7400 | 0.6000 | 0.8400 | 0.6857 | 0.6945, 0.6952, 0.6796, 0.6717, 0.6874 |
| yield | 0.6400 | 0.4700 | 0.7800 | 0.6572 | 0.6533, 0.6575, 0.6531, 0.6640, 0.6580 |
### Q08

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.9800 | 0.9100 | 1.0000 | 0.6400 | 0.6433, 0.6384, 0.6379, 0.6363, 0.6440 |
| conversion | 1.0000 | 0.9900 | 1.0000 | 0.9930 | 0.9781, 0.9871, 1.0000, 1.0000, 1.0000 |
| safety_risk | 0.9900 | 0.8200 | 1.0000 | 0.4263 | 0.4263, 0.4263, 0.4263, 0.4263, 0.4263 |
| score | 0.0010 | 0.0000 | 0.0200 | 0.1053 | 0.1049, 0.1045, 0.0992, 0.1060, 0.1120 |
| selectivity | 0.0100 | 0.0000 | 0.0600 | 0.4013 | 0.4087, 0.3948, 0.3933, 0.3967, 0.4131 |
| yield | 0.0050 | 0.0000 | 0.0400 | 0.3962 | 0.3944, 0.3998, 0.3842, 0.3991, 0.4038 |
### Q09

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.8000 | 0.6100 | 0.9400 | 0.4912 | 0.4900, 0.4852, 0.4940, 0.4841, 0.5025 |
| conversion | 0.9950 | 0.9700 | 1.0000 | 0.9974 | 1.0000, 0.9923, 1.0000, 1.0000, 0.9946 |
| safety_risk | 0.7200 | 0.4800 | 0.9400 | 0.2523 | 0.2523, 0.2523, 0.2523, 0.2523, 0.2523 |
| score | 0.0100 | 0.0000 | 0.0800 | 0.2752 | 0.2725, 0.2767, 0.2744, 0.2725, 0.2800 |
| selectivity | 0.1800 | 0.0500 | 0.3500 | 0.5164 | 0.5050, 0.5198, 0.5199, 0.5132, 0.5241 |
| yield | 0.1800 | 0.0400 | 0.3400 | 0.5154 | 0.5150, 0.5181, 0.5106, 0.5099, 0.5231 |
### Q10

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.8000 | 0.6100 | 0.9400 | 0.4949 | 0.4892, 0.4966, 0.4999, 0.5047, 0.4842 |
| conversion | 0.9950 | 0.9700 | 1.0000 | 0.9942 | 0.9991, 0.9998, 1.0000, 0.9939, 0.9781 |
| safety_risk | 0.7400 | 0.5000 | 0.9600 | 0.1459 | 0.1459, 0.1459, 0.1459, 0.1459, 0.1459 |
| score | 0.0080 | 0.0000 | 0.0800 | 0.3201 | 0.3218, 0.3178, 0.3232, 0.3200, 0.3179 |
| selectivity | 0.1800 | 0.0500 | 0.3500 | 0.5173 | 0.5167, 0.5191, 0.5235, 0.5115, 0.5160 |
| yield | 0.1800 | 0.0400 | 0.3400 | 0.5165 | 0.5199, 0.5082, 0.5188, 0.5198, 0.5156 |
### Q11

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.3200 | 0.1900 | 0.4700 | 0.5489 | 0.5697, 0.5532, 0.5308, 0.5504, 0.5403 |
| conversion | 0.9100 | 0.7800 | 0.9800 | 0.9903 | 0.9833, 0.9865, 0.9912, 0.9955, 0.9949 |
| safety_risk | 0.2500 | 0.1400 | 0.4100 | 0.1434 | 0.1434, 0.1434, 0.1434, 0.1434, 0.1434 |
| score | 0.2760 | 0.1300 | 0.3900 | 0.2810 | 0.2783, 0.2768, 0.2825, 0.2819, 0.2854 |
| selectivity | 0.6500 | 0.5000 | 0.7700 | 0.4585 | 0.4538, 0.4471, 0.4607, 0.4561, 0.4750 |
| yield | 0.5900 | 0.4200 | 0.7200 | 0.4602 | 0.4583, 0.4578, 0.4625, 0.4628, 0.4597 |
### Q12

| Metric | Prediction | 80% lower | 80% upper | Reference mean | Five reference replicates |
|---|---:|---:|---:|---:|---|
| byproduct_signal | 0.9000 | 0.7400 | 0.9900 | 0.2069 | 0.2063, 0.2058, 0.1964, 0.2129, 0.2132 |
| conversion | 0.9950 | 0.9700 | 1.0000 | 0.9513 | 0.9555, 0.9519, 0.9512, 0.9428, 0.9552 |
| safety_risk | 0.8600 | 0.5700 | 1.0000 | 0.4267 | 0.4267, 0.4267, 0.4267, 0.4267, 0.4267 |
| score | 0.0030 | 0.0000 | 0.0600 | 0.3582 | 0.3619, 0.3582, 0.3617, 0.3502, 0.3588 |
| selectivity | 0.0800 | 0.0100 | 0.2200 | 0.7886 | 0.7934, 0.7801, 0.8111, 0.7735, 0.7849 |
| yield | 0.0800 | 0.0100 | 0.2100 | 0.7491 | 0.7543, 0.7544, 0.7438, 0.7407, 0.7521 |

## Recommendation retest

- Selected source batch: `10`
- Retest exact replay verified: `True`
- Retest failure: `none`

| Metric | Selected source batch | Independent retest | Retest minus source |
|---|---:|---:|---:|
| byproduct_signal | 0.2048 | 0.2064 | 0.0016 |
| conversion | 0.8815 | 0.8711 | -0.0104 |
| cost | 1.0000 | 1.0000 | 0.0000 |
| degradation_warning | 0.1222 | 0.1343 | 0.0121 |
| safety_risk | 0.1588 | 0.1588 | 0.0000 |
| score | 0.3749 | 0.3687 | -0.0062 |
| selectivity | 0.7608 | 0.7582 | -0.0026 |
| virtual_spectrum_summary | 0.1676 | 0.1740 | 0.0063 |
| yield | 0.6701 | 0.6589 | -0.0112 |

## Scope note

This is the final sanitized report produced after all 60 source sessions and K1/Q/K2 chains were sealed. It includes released reference truth, blind-prediction evaluation, and the independent recommendation retest. Provider-private event streams, credentials, thread identifiers, and token accounting remain excluded.
