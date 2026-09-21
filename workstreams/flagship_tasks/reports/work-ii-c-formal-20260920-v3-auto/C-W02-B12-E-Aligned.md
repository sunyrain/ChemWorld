# C-W02-B12-E-Aligned

Status: completed

## Batch 1

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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 360
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 280
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 200
    },
    {
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 280
    },
    {
      "instrument": "particle_size",
      "operation": "measure"
    },
    {
      "operation": "filter_crystals"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 13,
  "lifecycle_index": 1,
  "metrics": {
    "byproduct_signal": 0.35507774353027344,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7584236264228821,
    "crystal_fines_fraction": 0.3150453269481659,
    "crystal_purity": 0.9904793500900269,
    "crystal_size": 0.08346505463123322,
    "crystal_yield": 0.4268858730792999,
    "degradation_warning": 0.1663038283586502,
    "safety_risk": 0.17988814413547516,
    "score": 0.5071477293968201,
    "selectivity": 0.5216906070709229,
    "virtual_spectrum_summary": 0.2701294720172882,
    "yield": 0.5195280909538269
  },
  "ordinal": 1
}
```

## Batch 2

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
      "volume_L": 0.04
    },
    {
      "catalyst": 2,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 350
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
    },
    {
      "instrument": "particle_size",
      "operation": "measure"
    },
    {
      "operation": "filter_crystals"
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
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.37299415469169617,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7043850421905518,
    "crystal_fines_fraction": 0.45296135544776917,
    "crystal_purity": 0.9797956347465515,
    "crystal_size": 0.10985670983791351,
    "crystal_yield": 0.32845452427864075,
    "degradation_warning": 0.08384674787521362,
    "safety_risk": 0.17731274664402008,
    "score": 0.43434464931488037,
    "selectivity": 0.3984960615634918,
    "virtual_spectrum_summary": 0.24287782609462738,
    "yield": 0.3870510756969452
  },
  "ordinal": 2
}
```

## Batch 3

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
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 350
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "instrument": "particle_size",
      "operation": "measure"
    },
    {
      "operation": "filter_crystals"
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
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.2381504327058792,
    "conversion": 0.998309314250946,
    "cost": 1.0,
    "crystal_csd_quality": 0.643096387386322,
    "crystal_fines_fraction": 0.5650448799133301,
    "crystal_purity": 0.9865560531616211,
    "crystal_size": 0.06406747549772263,
    "crystal_yield": 0.5383102893829346,
    "degradation_warning": 0.10365533083677292,
    "safety_risk": 0.1765216588973999,
    "score": 0.5101527571678162,
    "selectivity": 0.6582874655723572,
    "virtual_spectrum_summary": 0.17762763798236847,
    "yield": 0.657394528388977
  },
  "ordinal": 3
}
```

## Batch 4

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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 350
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 280
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 280
    },
    {
      "instrument": "particle_size",
      "operation": "measure"
    },
    {
      "operation": "filter_crystals"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 46,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.27551841735839844,
    "conversion": 0.9889556169509888,
    "cost": 1.0,
    "crystal_csd_quality": 0.5336463451385498,
    "crystal_fines_fraction": 0.7999892234802246,
    "crystal_purity": 1.0,
    "crystal_size": 0.06673238426446915,
    "crystal_yield": 0.4261769652366638,
    "degradation_warning": 0.09236329048871994,
    "safety_risk": 0.13902993500232697,
    "score": 0.4278886914253235,
    "selectivity": 0.5926029682159424,
    "virtual_spectrum_summary": 0.19309861958026886,
    "yield": 0.5789492726325989
  },
  "ordinal": 4
}
```

## Batch 5

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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 350
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 280
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 280
    },
    {
      "instrument": "particle_size",
      "operation": "measure"
    },
    {
      "operation": "filter_crystals"
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
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.35771602392196655,
    "conversion": 0.9963374137878418,
    "cost": 1.0,
    "crystal_csd_quality": 0.5656770467758179,
    "crystal_fines_fraction": 0.7053613662719727,
    "crystal_purity": 0.9726399183273315,
    "crystal_size": 0.046875372529029846,
    "crystal_yield": 0.31611159443855286,
    "degradation_warning": 0.11376858502626419,
    "safety_risk": 0.17920763790607452,
    "score": 0.386068731546402,
    "selectivity": 0.47886523604393005,
    "virtual_spectrum_summary": 0.24793967604637146,
    "yield": 0.47271206974983215
  },
  "ordinal": 5
}
```

## Batch 6

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
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 350
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 280
    },
    {
      "instrument": "particle_size",
      "operation": "measure"
    },
    {
      "operation": "filter_crystals"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 68,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.2497907280921936,
    "conversion": 0.9924249649047852,
    "cost": 1.0,
    "crystal_csd_quality": 0.7070592641830444,
    "crystal_fines_fraction": 0.44844919443130493,
    "crystal_purity": 0.9973778128623962,
    "crystal_size": 0.05178571864962578,
    "crystal_yield": 0.5407395362854004,
    "degradation_warning": 0.09588155895471573,
    "safety_risk": 0.17453670501708984,
    "score": 0.5320015549659729,
    "selectivity": 0.6344451904296875,
    "virtual_spectrum_summary": 0.1805316060781479,
    "yield": 0.6363252997398376
  },
  "ordinal": 6
}
```

## Batch 7

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
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 350
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "instrument": "particle_size",
      "operation": "measure"
    },
    {
      "operation": "filter_crystals"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 79,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.23980730772018433,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7170670032501221,
    "crystal_fines_fraction": 0.4186914563179016,
    "crystal_purity": 0.9764911532402039,
    "crystal_size": 0.09157321602106094,
    "crystal_yield": 0.5673647522926331,
    "degradation_warning": 0.08885367214679718,
    "safety_risk": 0.17592284083366394,
    "score": 0.5431389212608337,
    "selectivity": 0.6158021092414856,
    "virtual_spectrum_summary": 0.1718781739473343,
    "yield": 0.642443835735321
  },
  "ordinal": 7
}
```

## Batch 8

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
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 350
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.005
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 260
    },
    {
      "instrument": "particle_size",
      "operation": "measure"
    },
    {
      "operation": "filter_crystals"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 90,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.23211723566055298,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7465425133705139,
    "crystal_fines_fraction": 0.42229077219963074,
    "crystal_purity": 0.9767842888832092,
    "crystal_size": 0.10904361307621002,
    "crystal_yield": 0.5886090993881226,
    "degradation_warning": 0.09542155265808105,
    "safety_risk": 0.1767766773700714,
    "score": 0.5568249225616455,
    "selectivity": 0.6449034810066223,
    "virtual_spectrum_summary": 0.1706041842699051,
    "yield": 0.6365926861763
  },
  "ordinal": 8
}
```

## Batch 9

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
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 350
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.005
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
    },
    {
      "instrument": "particle_size",
      "operation": "measure"
    },
    {
      "operation": "filter_crystals"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 101,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.2425668090581894,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7153515815734863,
    "crystal_fines_fraction": 0.4412806034088135,
    "crystal_purity": 0.9790056347846985,
    "crystal_size": 0.06010761857032776,
    "crystal_yield": 0.591711163520813,
    "degradation_warning": 0.08802516013383865,
    "safety_risk": 0.1773100346326828,
    "score": 0.5436468720436096,
    "selectivity": 0.6231361031532288,
    "virtual_spectrum_summary": 0.17302305996418,
    "yield": 0.6368065476417542
  },
  "ordinal": 9
}
```

## Batch 10

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
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 350
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.001
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
    },
    {
      "instrument": "particle_size",
      "operation": "measure"
    },
    {
      "operation": "filter_crystals"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 112,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.23544391989707947,
    "conversion": 0.9858156442642212,
    "cost": 1.0,
    "crystal_csd_quality": 0.6816248297691345,
    "crystal_fines_fraction": 0.4512297809123993,
    "crystal_purity": 0.9748392105102539,
    "crystal_size": 0.07404479384422302,
    "crystal_yield": 0.5928282141685486,
    "degradation_warning": 0.09943150728940964,
    "safety_risk": 0.17724882066249847,
    "score": 0.5375673174858093,
    "selectivity": 0.6325517892837524,
    "virtual_spectrum_summary": 0.17423833906650543,
    "yield": 0.641473114490509
  },
  "ordinal": 10
}
```

## Batch 11

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
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 350
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.001
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
    },
    {
      "instrument": "particle_size",
      "operation": "measure"
    },
    {
      "operation": "filter_crystals"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 124,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.24395851790905,
    "conversion": 0.999011754989624,
    "cost": 1.0,
    "crystal_csd_quality": 0.7002164125442505,
    "crystal_fines_fraction": 0.4335678219795227,
    "crystal_purity": 0.9898749589920044,
    "crystal_size": 0.07928697764873505,
    "crystal_yield": 0.58379065990448,
    "degradation_warning": 0.07645153254270554,
    "safety_risk": 0.17724882066249847,
    "score": 0.5443074107170105,
    "selectivity": 0.6496492624282837,
    "virtual_spectrum_summary": 0.16858036816120148,
    "yield": 0.6301539540290833
  },
  "ordinal": 11
}
```

## Batch 12

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
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 350
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.001
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
    },
    {
      "operation": "filter_crystals"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "end_step": 134,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.22796005010604858,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7132520079612732,
    "crystal_fines_fraction": 0.4418381452560425,
    "crystal_purity": 0.9910804033279419,
    "crystal_size": 0.10094519704580307,
    "crystal_yield": 0.5867406725883484,
    "degradation_warning": 0.0982099398970604,
    "safety_risk": 0.17724882066249847,
    "score": 0.5484664440155029,
    "selectivity": 0.6290804743766785,
    "virtual_spectrum_summary": 0.16957250237464905,
    "yield": 0.634117066860199
  },
  "ordinal": 12
}
```

## K1

```json
{
  "payload": {
    "report": "Mechanistic account\n\nObservations\n\nThe campaign separated into an early material screen and a later process-history optimization. Batch 10 remained the selected recommendation and is not changed here.\n\n\u2022 Solvent-S1 produced the strongest recovery potential. With catalyst-C0 and otherwise similar reaction conditions, batch 3 reached crystal yield 0.5383, while early solvent screens gave 0.4262 for S0 (batch 4), 0.4269 for S2 (batch 1), and 0.3161 for S3 (batch 5). These comparisons are not a clean solvent-only factorial because catalyst and crystallization history also differed.\n\u2022 The solvents strongly affected particle quality. Final fines fractions were 0.8000 for S0 in batch 4, 0.7054 for S3 in batch 5, and 0.3150 for S2 in batch 1. S1 offered higher recovery but initially excessive fines: batch 3 had yield 0.5383 and fines 0.5650, failing the \u22640.50 requirement.\n\u2022 S2 therefore behaved as a conservative quality solvent, whereas S1 supplied the best recoverable-product opportunity but required controlled crystallization.\n\u2022 Among the later S1 experiments, catalyst-C0 at 350 K generally gave essentially complete conversion, reaction selectivity around 0.62\u20130.65, and reaction yield around 0.63\u20130.64. Early catalyst comparisons were confounded by solvent and crystallization changes, but C1 in batch 1 gave final selectivity 0.5217, C2 in batch 2 gave 0.3985, and C3 in batch 4 gave 0.5926. This evidence favored C0, although it does not establish an isolated catalyst ranking.\n\u2022 Lowering the reaction temperature from the batch-1 condition of 360 K to 350 K retained near-complete conversion while reducing the degradation warning. Batch 1 reported 0.1663 degradation warning, whereas the later 350 K S1/C0 batches were generally about 0.08\u20130.10.\n\nInterpretation of reaction\u2013crystallization coupling\n\nThe reaction generates target product and byproduct in the same solvent subsequently used for crystallization. Catalyst, temperature, and solvent therefore set both the amount of target available and the impurity environment entering the cooling sequence. C0/S1 at 350 K appears to provide a useful compromise: high conversion, better selectivity than the other screened combinations, and a mother liquor from which high-purity crystals can be recovered.\n\nThe important distinction is that crystal recovery was defined as\n\n  Y_crystal = recovered seed-excluded target in crystals / target present before separation.\n\nIt is not overall yield from charged reagent. A useful overall mass-yield approximation would be\n\n  Y_overall \u2248 Y_reaction \u00d7 Y_crystal.\n\nThus catalyst selectivity still matters economically even if the reported crystal-yield objective is normalized to target already formed. Byproducts can also alter nucleation, occlusion, and growth. Nevertheless, final crystal purity stayed high in the optimized S1 batches (0.9748\u20130.9974), suggesting strong impurity rejection by the solid phase despite only moderate reaction selectivity.\n\nThe solvent trends are consistent with competing solubility, nucleation, and growth effects. In qualitative terms, supersaturation may be written as\n\n  S = C/C*(T, solvent),\n\nwith nucleation increasing steeply above a critical supersaturation while growth usually responds less steeply. Recovery can be approximated by\n\n  Y_crystal \u2248 1 \u2212 n_target,liquor(final)/n_target(pre-separation).\n\nCooling farther lowers C*, improving recovery, but it can also create many new nuclei and hence fines. S1 exposed this tradeoff clearly; S2 suppressed fines more effectively but did not reach the same recovery.\n\nProcess-history dependence\n\nThe final state was not determined only by the terminal temperature. The path to that temperature and the seeding point were important.\n\n\u2022 Batch 3 used S1/C0, seeded 0.05 g at the hot post-reaction state, and cooled directly to 270 K twice. It achieved yield 0.5383 but fines 0.5650.\n\u2022 Batch 6 first cooled slowly to 320 K over 14,400 s, then added only 0.01 g seed, and cooled to 280 K over another 14,400 s. Recovery was similar at 0.5407, but fines fell to 0.4484 and purity was 0.9974. The staged path converted an infeasible S1 process into a feasible one without sacrificing recovery.\n\u2022 Lowering the second-stage endpoint then progressively increased recovery: batch 7 at 270 K gave 0.5674 yield and 0.4187 fines; batch 8 at 260 K with 0.005 g seed gave 0.5886 yield and 0.4223 fines; batch 9 at 250 K gave 0.5917 yield and 0.4413 fines.\n\u2022 Batch 10 reduced the seed mass to 0.001 g at 320 K and retained the 250 K endpoint. It gave the highest observed feasible recovery, 0.5928, with purity 0.9748 and fines 0.4512.\n\u2022 Batch 11 added another 14,400 s cooling operation at 250 K but did not improve recovery: yield was 0.5838, with purity 0.9899 and fines 0.4336. This suggests that most recoverable material had crystallized during the first low-temperature stage, although the difference is comparable with assay variation.\n\u2022 Batch 12 repeated the essential batch-10 path without an intermediate particle-size measurement and gave yield 0.5867, purity 0.9911, and fines 0.4418. This supports reproducibility of the feasible region but not a statistically significant superiority of the exact batch-10 seed amount.\n\nA plausible interpretation is that the 320 K stage establishes moderate supersaturation before seeding. The small seed charge supplies a controlled number of growth surfaces, after which the slow 320\u2192250 K cooling directs solute primarily onto existing particles. Hot seeding in batch 3 may have been less effective because seeds could dissolve or because subsequent direct deep cooling generated excessive secondary nuclei. This dissolution explanation is mechanistic inference rather than a directly measured event.\n\nRevisions made during the study\n\nThe initial strategy favored S2 because its nominal low solubility, high growth tendency, and low impurity occlusion suggested good crystals. Batch 1 confirmed excellent purity and fines but only 0.4269 recovery. Reducing S2 solvent volume and cooling to 250 K in batch 2 did not help: recovery fell to 0.3285 and fines rose to 0.4530. The study therefore shifted from a conservative S2 process to the higher-recovery S1 system.\n\nThe first S1 trial revealed the unresolved fines problem. The working model was revised from \u201ccool deeply and seed heavily\u201d to \u201cstage the cooling, seed near the onset region, and use a small seed charge.\u201d Batches 6\u201310 then traced the endpoint and seed-mass response, raising feasible recovery from about 0.54 to about 0.59.\n\nUncertainty and unresolved tradeoffs\n\nThe recovery differences among batches 8\u201310 and 12 are small relative to the final-assay crystal-yield noise scale of approximately 0.01. Batch 10 exceeded batch 9 by only 0.0011 and batch 12 by 0.0061, so these runs describe a recovery plateau rather than a sharply proven optimum. Batch 10 was selected because it had the highest observed feasible recovery, not because its superiority over nearby recipes was statistically resolved.\n\nFines are closer to the constraint than purity. Batch 10 had a fines margin of about 0.049 below the 0.50 limit, while its purity margin was about 0.175 above 0.80. Particle-size readings also varied between the in-process and final assays: batch 10 changed from 0.4298 before filtration to 0.4512 in the final assay. This may reflect measurement noise, sampling, or filtration-associated population differences. Consequently, deeper cooling or other recovery-increasing changes could consume the remaining fines margin.\n\nSeveral alternatives remain untested: a fully crossed catalyst-by-solvent design; endpoints between 250 and 260 K; intermediate seed masses between 0.001 and 0.005 g; seeding-temperature optimization around 320 K; different agitation during crystallization; controlled isothermal aging without ambient warming; washing; and replicate batches sufficient to estimate process variance. Catalyst rankings independent of solvent are unresolved, as are the exact contributions of seed dissolution, primary nucleation, secondary nucleation, and impurity-mediated growth.\n\nOverall, the evidence supports a coupled mechanism in which C0/S1 at 350 K produces a sufficiently clean, target-rich liquor, while staged cooling to 320 K, low seed loading, and slow deep cooling to 250 K shift the crystallization from uncontrolled nucleation toward seeded growth. The remaining optimization problem is to increase recovery beyond the observed ~0.59 plateau without pushing the number fraction of sub-20 \u00b5m particles above 0.50."
  },
  "failure": null,
  "elapsed_s": 87.90600000001723,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 1041024,
    "input_tokens": 1163364,
    "output_tokens": 9778,
    "reasoning_output_tokens": 2807
  },
  "numerics_budget": {
    "limit": 128,
    "on_exhaustion": "continue_answer",
    "version": "public-numerics-budget-v1"
  },
  "numerics_attempts": 0
}
```

## Q

```json
{
  "payload": {
    "predictions": [
      {
        "crystal_fines_fraction": {
          "estimate": 0.3,
          "lower80": 0.2,
          "upper80": 0.42
        },
        "crystal_purity": {
          "estimate": 0.97,
          "lower80": 0.92,
          "upper80": 1
        },
        "crystal_size": {
          "estimate": 0.14,
          "lower80": 0.09,
          "upper80": 0.2
        },
        "crystal_yield": {
          "estimate": 0.42,
          "lower80": 0.26,
          "upper80": 0.56
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q01"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.54,
          "lower80": 0.4,
          "upper80": 0.68
        },
        "crystal_purity": {
          "estimate": 0.94,
          "lower80": 0.87,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.1,
          "lower80": 0.05,
          "upper80": 0.16
        },
        "crystal_yield": {
          "estimate": 0.29,
          "lower80": 0.15,
          "upper80": 0.43
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q02"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.56,
          "lower80": 0.41,
          "upper80": 0.71
        },
        "crystal_purity": {
          "estimate": 0.95,
          "lower80": 0.88,
          "upper80": 1
        },
        "crystal_size": {
          "estimate": 0.13,
          "lower80": 0.07,
          "upper80": 0.2
        },
        "crystal_yield": {
          "estimate": 0.27,
          "lower80": 0.12,
          "upper80": 0.42
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q03"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.44,
          "lower80": 0.31,
          "upper80": 0.58
        },
        "crystal_purity": {
          "estimate": 0.96,
          "lower80": 0.9,
          "upper80": 1
        },
        "crystal_size": {
          "estimate": 0.11,
          "lower80": 0.06,
          "upper80": 0.17
        },
        "crystal_yield": {
          "estimate": 0.3,
          "lower80": 0.16,
          "upper80": 0.44
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q04"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.42,
          "lower80": 0.29,
          "upper80": 0.56
        },
        "crystal_purity": {
          "estimate": 0.96,
          "lower80": 0.9,
          "upper80": 1
        },
        "crystal_size": {
          "estimate": 0.12,
          "lower80": 0.07,
          "upper80": 0.18
        },
        "crystal_yield": {
          "estimate": 0.31,
          "lower80": 0.17,
          "upper80": 0.45
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q05"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.69,
          "lower80": 0.54,
          "upper80": 0.82
        },
        "crystal_purity": {
          "estimate": 0.94,
          "lower80": 0.86,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.07,
          "lower80": 0.03,
          "upper80": 0.12
        },
        "crystal_yield": {
          "estimate": 0.32,
          "lower80": 0.18,
          "upper80": 0.46
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q06"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.4,
          "lower80": 0.27,
          "upper80": 0.54
        },
        "crystal_purity": {
          "estimate": 0.96,
          "lower80": 0.9,
          "upper80": 1
        },
        "crystal_size": {
          "estimate": 0.12,
          "lower80": 0.07,
          "upper80": 0.19
        },
        "crystal_yield": {
          "estimate": 0.32,
          "lower80": 0.18,
          "upper80": 0.46
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q07"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.3,
          "lower80": 0.18,
          "upper80": 0.44
        },
        "crystal_purity": {
          "estimate": 0.97,
          "lower80": 0.91,
          "upper80": 1
        },
        "crystal_size": {
          "estimate": 0.16,
          "lower80": 0.09,
          "upper80": 0.23
        },
        "crystal_yield": {
          "estimate": 0.3,
          "lower80": 0.15,
          "upper80": 0.45
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q08"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.72,
          "lower80": 0.56,
          "upper80": 0.86
        },
        "crystal_purity": {
          "estimate": 0.92,
          "lower80": 0.83,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.05,
          "lower80": 0.02,
          "upper80": 0.1
        },
        "crystal_yield": {
          "estimate": 0.06,
          "lower80": 0,
          "upper80": 0.16
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q09"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.6,
          "lower80": 0.44,
          "upper80": 0.75
        },
        "crystal_purity": {
          "estimate": 0.94,
          "lower80": 0.86,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.07,
          "lower80": 0.03,
          "upper80": 0.13
        },
        "crystal_yield": {
          "estimate": 0.16,
          "lower80": 0.05,
          "upper80": 0.29
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q10"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.41,
          "lower80": 0.28,
          "upper80": 0.55
        },
        "crystal_purity": {
          "estimate": 0.96,
          "lower80": 0.9,
          "upper80": 1
        },
        "crystal_size": {
          "estimate": 0.12,
          "lower80": 0.07,
          "upper80": 0.18
        },
        "crystal_yield": {
          "estimate": 0.32,
          "lower80": 0.18,
          "upper80": 0.46
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q11"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.57,
          "lower80": 0.42,
          "upper80": 0.71
        },
        "crystal_purity": {
          "estimate": 0.92,
          "lower80": 0.84,
          "upper80": 0.98
        },
        "crystal_size": {
          "estimate": 0.09,
          "lower80": 0.04,
          "upper80": 0.15
        },
        "crystal_yield": {
          "estimate": 0.49,
          "lower80": 0.34,
          "upper80": 0.63
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q12"
      }
    ],
    "rationale": "These are extrapolations from the sealed campaign, so the intervals include process-model uncertainty as well as expected batch variability. Q01\u2013Q02 assigns S1 higher recovery, growth and feasibility than S3. Q03\u2013Q04 predicts that the larger seed charge suppresses uncontrolled S0 nucleation, lowering fines, although it slightly reduces size. Q05\u2013Q06 contrasts gradual cooling with a temperature crash: similar terminal recovery is expected, but the crash should generate substantially more fines. Q07\u2013Q08 treats the 315 K cycle as an annealing step that partially dissolves fines and promotes regrowth, improving size and fines at a small possible recovery cost. Q09\u2013Q10 predicts that an additional 292 K hold permits limited growth and recovery, but remains too warm and short for a reliably feasible S0 product. Q11\u2013Q12 predicts that doubling reagent loading raises recovery but also supersaturation, impurity burden and secondary nucleation, creating a recovery\u2013fines tradeoff. Purity is predicted to remain above 0.80 throughout because the campaign showed strong impurity rejection; fines near 0.50 are much less certain. Seed ensures particles are expected in every query, even where seed-excluded product recovery is low."
  },
  "failure": null,
  "elapsed_s": 126.34299999999348,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 1044608,
    "input_tokens": 1235246,
    "output_tokens": 14493,
    "reasoning_output_tokens": 5859
  },
  "numerics_budget": {
    "limit": 128,
    "on_exhaustion": "continue_answer",
    "version": "public-numerics-budget-v1"
  },
  "numerics_attempts": 0
}
```

## K2

```json
{
  "payload": {
    "report": "1. Status of the main claims\n\nSupported by direct observations:\n\n\u2022 S1 offered the highest recovery potential among the screened solvents, but required particle-control measures. Batch 3 (S1) produced crystal yield 0.5383, versus 0.4269 in batch 1 (S2), 0.4262 in batch 4 (S0), and 0.3161 in batch 5 (S3). This is observational support, not an isolated solvent effect, because catalyst and crystallization histories differed.\n\n\u2022 S2 gave conservative particle quality. Batch 1 had fines 0.3150 and purity 0.9905, whereas the initial S1 process in batch 3 had fines 0.5650. Again, the solvent attribution is interpretive because the histories were not matched.\n\n\u2022 The revised staged S1 process reached the required quality region. Batch 6, cooled first to 320 K, seeded with 0.01 g, and then cooled to 280 K, gave yield 0.5407, purity 0.9974, and fines 0.4484. Batch 3, with hot addition of 0.05 g seed and a different cooling path, had similar recovery but infeasible fines. The performance change is directly observed; attributing it specifically to seed survival or nucleation control remains an interpretation because seed mass, timing, and cooling profile all changed together.\n\n\u2022 Deeper second-stage cooling raised recovery across the later S1 series. Batches 6\u20139 gave yields of 0.5407, 0.5674, 0.5886, and 0.5917 at respective endpoints of 280, 270, 260, and 250 K. Their final fines remained below 0.50. The endpoint trend is strong, although the seed charge also changed from 0.01 to 0.005 g between batches 7 and 8.\n\n\u2022 The process reached a recovery plateau near 0.59. Batch 10 gave 0.5928, batch 11 gave 0.5838 despite an extra 14,400 s operation at 250 K, and batch 12 gave 0.5867. Thus the claim that another cold operation would materially increase recovery was contradicted by batch 11, subject to roughly 0.01 assay-scale uncertainty.\n\n\u2022 Purity was not the active optimized-process constraint. Batches 6\u201312 all had purity around 0.975\u20130.997, comfortably above 0.80. Fines, at roughly 0.42\u20130.45 in the best batches, remained the closer constraint.\n\nContradicted or revised claims:\n\n\u2022 The initial prior that S2 would be the best overall solvent was contradicted for recovery. It produced good particles in batch 1 but only 0.4269 recovery. Reducing its volume and cooling more deeply in batch 2 lowered recovery further to 0.3285.\n\n\u2022 A simple claim that deeper cooling must monotonically worsen fines was not supported. Final fines were 0.4484, 0.4187, 0.4223, and 0.4413 in batches 6\u20139. The data instead suggest that cooling history and seeding can contain the fines penalty over this range.\n\n\u2022 Prolonged residence at the final temperature was not automatically beneficial: batch 11 did not outperform batches 9, 10, or 12.\n\nStill untested:\n\n\u2022 A causal catalyst ranking remains untested. C0 looked favorable in the later S1 batches, but early C1\u2013C3 comparisons were confounded by solvent and process changes.\n\n\u2022 Seed dissolution at the hot seeding point, suppression of primary nucleation at 320 K, secondary nucleation, and impurity-mediated growth were not directly observed. They are competing interpretations of the batch 3 versus batch 6 change.\n\n\u2022 The proposed supersaturation and equilibrium-recovery equations were useful organizing relationships, not fitted or validated laws for this benchmark.\n\n\u2022 Heat-cycle annealing, washing, crystallization agitation effects, and behavior over the much longer multistep cooling histories in the held-out recipes were not tested directly.\n\n2. One additional experiment\n\nI would repeat the batch-10 chemistry and thermal profile but add the same 0.001 g seed immediately after the 350 K reaction, rather than after cooling to 320 K. The remaining sequence would be unchanged: S1, C0, 0.04 mol reagent in 0.08 L solvent, 350 K for 3,600 s, slow cooling to 320 K for 14,400 s, slow cooling to 250 K for 14,400 s, particle-size measurement, filtration, termination, and final assay.\n\nThis single matched experiment would separate two explanations that the campaign confounded:\n\n\u2022 Seeding-window explanation: the success of batch 10 depended on adding seed near 320 K, where it survived and directed growth. Hot-added seed would partly dissolve or lose control of the later nucleation event. Expected outcome: recovery might remain near 0.58\u20130.59, but size/CSD would worsen and fines would rise, potentially toward or above 0.50.\n\n\u2022 Low-seed/deep-cooling explanation: seed timing was secondary; the important factors were the small seed charge, slow staged cooling, and 250 K endpoint. Expected outcome: results would remain close to batch 10\u2014approximately 0.59 recovery, about 0.97\u20130.99 purity, and fines in the low-to-mid 0.40s.\n\nA large difference in particle metrics with little change in recovery would support the seeding-window mechanism. Similar results would reject seed survival as the main explanation and shift attention to cooling rate and terminal supersaturation.\n\n3. Least effectively used observation and least reliable prediction\n\nThe account used batch 1\u2019s unintended thermal history least effectively. After cooling to 280 K, its ordinary 14,400 s wait allowed the slurry to warm to about 297 K before it was recooled to 280 K. Batch 1 ultimately had excellent fines of 0.3150. I treated it mainly as evidence for S2, rather than as a weak observation about dissolution\u2013regrowth or thermal cycling. Because solvent, catalyst, seed loading, and reaction conditions were all different, it cannot establish an annealing effect, but it deserved explicit discussion.\n\nQ08 is the least reliable held-out prediction. It intentionally reheats an established S0 slurry to 315 K and then cools it rapidly back to 278.15 K. My prediction assumed that this would dissolve fines and promote regrowth, but the campaign contained no matched reheating experiment. Batch 1\u2019s milder passive warming only reached about 297 K and occurred in S2, so it is an inadequate analogue. At 315 K, Q08 could instead dissolve a substantial part of the product, lose recovery, generate a fresh nucleation burst on recooling, or cause agglomeration. Consequently, both the predicted improvement in fines and the small predicted recovery penalty for Q08 are substantially more speculative than the interpolation-based predictions."
  },
  "failure": null,
  "elapsed_s": 72.31299999999464,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 1104896,
    "input_tokens": 1311763,
    "output_tokens": 16954,
    "reasoning_output_tokens": 6791
  },
  "numerics_budget": {
    "limit": 128,
    "on_exhaustion": "continue_answer",
    "version": "public-numerics-budget-v1"
  },
  "numerics_attempts": 0
}
```

## Evaluation and accounting

```json
{
  "failure": null,
  "recommendation": {
    "selected_experiment_index": 10,
    "selection_rationale": "Batch 10 gave the highest observed seed-excluded crystal recovery among specification-passing batches (crystal_yield 0.5928), with crystal_purity 0.9748 and fines fraction 0.4512, both within the required limits."
  },
  "recommendation_recipe": {
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
        "catalyst": 0,
        "catalyst_amount_mol": 0.005,
        "operation": "add_catalyst"
      },
      {
        "duration_s": 3600,
        "operation": "heat",
        "stirring_speed_rpm": 500,
        "target_temperature_K": 350
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 320
      },
      {
        "operation": "seed_crystals",
        "seed_mass_g": 0.001
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 250
      },
      {
        "instrument": "particle_size",
        "operation": "measure"
      },
      {
        "operation": "filter_crystals"
      },
      {
        "operation": "terminate"
      },
      {
        "instrument": "final_assay",
        "operation": "measure"
      }
    ],
    "excluded_rejected_attempts": [],
    "lifecycle_index": 10,
    "source_attempts": 11
  },
  "prediction_evaluation": {
    "contrasts": [
      {
        "absolute_delta_error": 0.06311778881199467,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_yield",
        "predicted_delta": -0.13,
        "resolved": true,
        "true_delta": -0.19311778881199468
      },
      {
        "absolute_delta_error": 0.028552855963854484,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_purity",
        "predicted_delta": -0.030000000000000027,
        "resolved": false,
        "true_delta": -0.0014471440361455423
      },
      {
        "absolute_delta_error": 0.06902680472663708,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_size",
        "predicted_delta": -0.04000000000000001,
        "resolved": true,
        "true_delta": 0.02902680472663708
      },
      {
        "absolute_delta_error": 0.8302675737116523,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.24000000000000005,
        "resolved": true,
        "true_delta": -0.5902675737116523
      },
      {
        "absolute_delta_error": 0.03004843643867039,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_yield",
        "predicted_delta": 0.02999999999999997,
        "resolved": false,
        "true_delta": -4.843643867041836e-05
      },
      {
        "absolute_delta_error": 0.0017644384597508278,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_purity",
        "predicted_delta": 0.010000000000000009,
        "resolved": false,
        "true_delta": 0.008235561540249181
      },
      {
        "absolute_delta_error": 0.019779790651946252,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_size",
        "predicted_delta": -0.020000000000000004,
        "resolved": false,
        "true_delta": -0.00022020934805375147
      },
      {
        "absolute_delta_error": 0.09936854990383653,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.12000000000000005,
        "resolved": false,
        "true_delta": -0.020631450096163517
      },
      {
        "absolute_delta_error": 0.009739549297168137,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_yield",
        "predicted_delta": 0.010000000000000009,
        "resolved": false,
        "true_delta": 0.00026045070283187144
      },
      {
        "absolute_delta_error": 0.0151321463408296,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.020000000000000018,
        "resolved": false,
        "true_delta": -0.004867853659170418
      },
      {
        "absolute_delta_error": 0.012379301835895466,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_size",
        "predicted_delta": -0.04999999999999999,
        "resolved": true,
        "true_delta": -0.03762069816410452
      },
      {
        "absolute_delta_error": 0.30810139828932065,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.26999999999999996,
        "resolved": true,
        "true_delta": 0.5781013982893206
      },
      {
        "absolute_delta_error": 0.06006038328567326,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_yield",
        "predicted_delta": -0.020000000000000018,
        "resolved": true,
        "true_delta": 0.04006038328567324
      },
      {
        "absolute_delta_error": 0.019468661285033884,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_purity",
        "predicted_delta": 0.010000000000000009,
        "resolved": false,
        "true_delta": -0.009468661285033875
      },
      {
        "absolute_delta_error": 0.07010290464756481,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_size",
        "predicted_delta": 0.04000000000000001,
        "resolved": true,
        "true_delta": -0.030102904647564807
      },
      {
        "absolute_delta_error": 0.7023941217008813,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.10000000000000003,
        "resolved": true,
        "true_delta": 0.6023941217008812
      },
      {
        "absolute_delta_error": 0.053684422102466406,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_yield",
        "predicted_delta": 0.1,
        "resolved": true,
        "true_delta": 0.1536844221024664
      },
      {
        "absolute_delta_error": 0.034527106938203045,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_purity",
        "predicted_delta": 0.019999999999999907,
        "resolved": true,
        "true_delta": -0.014527106938203138
      },
      {
        "absolute_delta_error": 0.005817474751091116,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_size",
        "predicted_delta": 0.020000000000000004,
        "resolved": true,
        "true_delta": 0.014182525248908888
      },
      {
        "absolute_delta_error": 0.13908907723599961,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.12,
        "resolved": false,
        "true_delta": 0.01908907723599962
      },
      {
        "absolute_delta_error": 0.14103124947311257,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_yield",
        "predicted_delta": 0.16999999999999998,
        "resolved": true,
        "true_delta": 0.02896875052688741
      },
      {
        "absolute_delta_error": 0.03394295307809869,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_purity",
        "predicted_delta": -0.039999999999999925,
        "resolved": false,
        "true_delta": -0.006057046921901232
      },
      {
        "absolute_delta_error": 0.003426352835710217,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_size",
        "predicted_delta": -0.03,
        "resolved": true,
        "true_delta": -0.026573647164289782
      },
      {
        "absolute_delta_error": 0.4309082204353359,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.15999999999999998,
        "resolved": true,
        "true_delta": 0.5909082204353359
      }
    ],
    "failures": [],
    "metrics": {
      "crystal_fines_fraction": {
        "coverage80": 0.5,
        "interval_score80": 1.9229581603450983,
        "interval_width": 0.27666666666666667,
        "mae": 0.25267769272206225,
        "n": 12,
        "planned": 12
      },
      "crystal_purity": {
        "coverage80": 0.9166666666666666,
        "interval_score80": 0.1218111798555707,
        "interval_width": 0.11416666666666665,
        "mae": 0.03515656929239181,
        "n": 12,
        "planned": 12
      },
      "crystal_size": {
        "coverage80": 0.8333333333333334,
        "interval_score80": 0.16907985551460603,
        "interval_width": 0.11,
        "mae": 0.041660286603241135,
        "n": 12,
        "planned": 12
      },
      "crystal_yield": {
        "coverage80": 0.9166666666666666,
        "interval_score80": 0.28511641420557604,
        "interval_width": 0.2725,
        "mae": 0.04015630576676812,
        "n": 12,
        "planned": 12
      }
    },
    "quality": {
      "balanced_accuracy": 0.6666666666666666,
      "false_negative": 2,
      "false_positive": 2,
      "true_negative": 4,
      "true_positive": 4
    },
    "resolved_direction_correct": 8,
    "resolved_direction_n": 14,
    "tie_correct": 1,
    "tie_n": 10,
    "valid": true
  },
  "public_baselines": {
    "available": true,
    "mae": {
      "public_mean": {
        "crystal_fines_fraction": 0.28539295852396884,
        "crystal_purity": 0.004170096404171107,
        "crystal_size": 0.017192244486071477,
        "crystal_yield": 0.2404500069681622
      },
      "public_nearest_neighbor": {
        "crystal_fines_fraction": 0.3662169412793119,
        "crystal_purity": 0.016003191316434212,
        "crystal_size": 0.021726691467565954,
        "crystal_yield": 0.15494387917348054
      }
    },
    "training_batches": 12
  },
  "tokens": {
    "basis": "cumulative thread snapshots differenced in source/K1/Q/K2 order",
    "complete": true,
    "monetary_cost_usd": null,
    "stages": [
      {
        "cached_input": 1041024,
        "input": 1102900,
        "output": 6896,
        "stage": "source",
        "uncached_input": 61876
      },
      {
        "cached_input": 0,
        "input": 60464,
        "output": 2882,
        "stage": "K1",
        "uncached_input": 60464
      },
      {
        "cached_input": 3584,
        "input": 71882,
        "output": 4715,
        "stage": "Q",
        "uncached_input": 68298
      },
      {
        "cached_input": 60288,
        "input": 76517,
        "output": 2461,
        "stage": "K2",
        "uncached_input": 16229
      }
    ],
    "total": {
      "cached_input": 1104896,
      "input": 1311763,
      "input_plus_output": 1328717,
      "output": 16954,
      "uncached_input": 206867
    },
    "valid": true
  },
  "elapsed_s": 627.5309999999881
}
```
