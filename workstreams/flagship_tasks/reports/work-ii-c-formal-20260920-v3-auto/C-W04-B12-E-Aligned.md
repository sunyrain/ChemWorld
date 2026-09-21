# C-W04-B12-E-Aligned

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
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.02
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 275
    },
    {
      "instrument": "particle_size",
      "operation": "measure"
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
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
    "byproduct_signal": 0.3587149381637573,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.4941159188747406,
    "crystal_fines_fraction": 0.9973059296607971,
    "crystal_purity": 0.9871428608894348,
    "crystal_size": 0.05739297345280647,
    "crystal_yield": 0.38145506381988525,
    "degradation_warning": 0.16667954623699188,
    "safety_risk": 0.1738763451576233,
    "score": 0.36372295022010803,
    "selectivity": 0.47859370708465576,
    "virtual_spectrum_summary": 0.27229902148246765,
    "yield": 0.4764312207698822
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
      "volume_L": 0.08
    },
    {
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 400,
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
      "operation": "seed_crystals",
      "seed_mass_g": 0.001
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 290
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
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
  "end_step": 28,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.29571083188056946,
    "conversion": 0.9990811944007874,
    "cost": 1.0,
    "crystal_csd_quality": 0.5576691031455994,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9780205488204956,
    "crystal_size": 0.06797051429748535,
    "crystal_yield": 0.3932879567146301,
    "degradation_warning": 0.04436740651726723,
    "safety_risk": 0.1739886850118637,
    "score": 0.3781582713127136,
    "selectivity": 0.4846929907798767,
    "virtual_spectrum_summary": 0.1826062947511673,
    "yield": 0.47204193472862244
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
      "stirring_speed_rpm": 400,
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
      "operation": "seed_crystals",
      "seed_mass_g": 1e-06
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 295
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 275
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
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
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 1e-06
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.0001
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 290
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "instrument": "particle_size",
      "operation": "measure"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 280
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 280
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 300
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
  "end_step": 75,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.2812615931034088,
    "conversion": 0.9956625699996948,
    "cost": 1.0,
    "crystal_csd_quality": 0.5504258275032043,
    "crystal_fines_fraction": 0.9949333071708679,
    "crystal_purity": 0.9867324829101562,
    "crystal_size": 0.02677758038043976,
    "crystal_yield": 0.4049491882324219,
    "degradation_warning": 0.07356217503547668,
    "safety_risk": 0.1769455522298813,
    "score": 0.3833923935890198,
    "selectivity": 0.5092594027519226,
    "virtual_spectrum_summary": 0.18779686093330383,
    "yield": 0.507022500038147
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
      "stirring_speed_rpm": 400,
      "target_temperature_K": 340
    },
    {
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.001
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 296
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 294
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 292
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 290
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 288
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 286
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 284
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 282
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 280
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 275
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
  "end_step": 96,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.2760140299797058,
    "conversion": 0.9863344430923462,
    "cost": 1.0,
    "crystal_csd_quality": 0.5495717525482178,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 1.0,
    "crystal_size": 0.03834131732583046,
    "crystal_yield": 0.43872877955436707,
    "degradation_warning": 0.043723367154598236,
    "safety_risk": 0.1779562085866928,
    "score": 0.3940560221672058,
    "selectivity": 0.5144673585891724,
    "virtual_spectrum_summary": 0.17148323357105255,
    "yield": 0.499480277299881
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
      "solvent": 2,
      "volume_L": 0.04
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 340
    },
    {
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.0001
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 296
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 294
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 292
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 290
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 288
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 286
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 284
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 282
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 280
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 275
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
  "end_step": 117,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.30113643407821655,
    "conversion": 0.9963339567184448,
    "cost": 1.0,
    "crystal_csd_quality": 0.5521223545074463,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9826103448867798,
    "crystal_size": 0.008148567751049995,
    "crystal_yield": 0.4541577100753784,
    "degradation_warning": 0.06822966784238815,
    "safety_risk": 0.20147168636322021,
    "score": 0.3924419581890106,
    "selectivity": 0.5178353190422058,
    "virtual_spectrum_summary": 0.19632838666439056,
    "yield": 0.5116803646087646
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
      "stirring_speed_rpm": 400,
      "target_temperature_K": 340
    },
    {
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.001
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 296
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 294
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 292
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 290
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 288
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 286
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 284
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 282
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 280
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 275
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 265
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 260
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 255
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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 285
    },
    {
      "instrument": "particle_size",
      "operation": "measure"
    },
    {
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 295
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
  "end_step": 146,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.29360613226890564,
    "conversion": 0.9897715449333191,
    "cost": 1.0,
    "crystal_csd_quality": 0.5295889377593994,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9984277486801147,
    "crystal_size": 0.010927812196314335,
    "crystal_yield": 0.3938896358013153,
    "degradation_warning": 0.06593479961156845,
    "safety_risk": 0.1748451590538025,
    "score": 0.3759987950325012,
    "selectivity": 0.5037214756011963,
    "virtual_spectrum_summary": 0.19115404784679413,
    "yield": 0.5042496919631958
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
      "stirring_speed_rpm": 400,
      "target_temperature_K": 340
    },
    {
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.0001
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
  "end_step": 157,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.28362271189689636,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.544725239276886,
    "crystal_fines_fraction": 0.9868564605712891,
    "crystal_purity": 0.976726770401001,
    "crystal_size": 0.05120839178562164,
    "crystal_yield": 0.45267629623413086,
    "degradation_warning": 0.0589069128036499,
    "safety_risk": 0.17794576287269592,
    "score": 0.394316166639328,
    "selectivity": 0.4847027659416199,
    "virtual_spectrum_summary": 0.18250060081481934,
    "yield": 0.5099935531616211
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
      "catalyst": 3,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 340
    },
    {
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.0001
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
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
  "end_step": 167,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.24776913225650787,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5760332345962524,
    "crystal_fines_fraction": 0.9869764447212219,
    "crystal_purity": 0.9737152457237244,
    "crystal_size": 0.07260073721408844,
    "crystal_yield": 0.4800635576248169,
    "degradation_warning": 0.04976658523082733,
    "safety_risk": 0.16294489800930023,
    "score": 0.4185294210910797,
    "selectivity": 0.556240439414978,
    "virtual_spectrum_summary": 0.15866798162460327,
    "yield": 0.5433635711669922
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
      "catalyst": 3,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 340
    },
    {
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.0001
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
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
  "end_step": 181,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.2582187056541443,
    "conversion": 0.9925450682640076,
    "cost": 1.0,
    "crystal_csd_quality": 0.5510190725326538,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9759287238121033,
    "crystal_size": 0.02308063581585884,
    "crystal_yield": 0.47097066044807434,
    "degradation_warning": 0.04237018898129463,
    "safety_risk": 0.16294489800930023,
    "score": 0.40392157435417175,
    "selectivity": 0.5344730615615845,
    "virtual_spectrum_summary": 0.16108687222003937,
    "yield": 0.5435773730278015
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
      "solvent": 3,
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
      "stirring_speed_rpm": 400,
      "target_temperature_K": 340
    },
    {
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.0001
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
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
  "end_step": 191,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.2759212851524353,
    "conversion": 0.9804494380950928,
    "cost": 1.0,
    "crystal_csd_quality": 0.5142644047737122,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9613816738128662,
    "crystal_size": 0.04090069234371185,
    "crystal_yield": 0.4410761296749115,
    "degradation_warning": 0.0752299576997757,
    "safety_risk": 0.19024470448493958,
    "score": 0.3834012448787689,
    "selectivity": 0.5228283405303955,
    "virtual_spectrum_summary": 0.18561019003391266,
    "yield": 0.5289217233657837
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
      "solvent": 0,
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
      "stirring_speed_rpm": 400,
      "target_temperature_K": 340
    },
    {
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.0001
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
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
  "end_step": 201,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.21682795882225037,
    "conversion": 0.9697866439819336,
    "cost": 1.0,
    "crystal_csd_quality": 0.5326988101005554,
    "crystal_fines_fraction": 0.9936861991882324,
    "crystal_purity": 0.9869162440299988,
    "crystal_size": 0.0455450713634491,
    "crystal_yield": 0.49159327149391174,
    "degradation_warning": 0.02400088869035244,
    "safety_risk": 0.14305511116981506,
    "score": 0.42340826988220215,
    "selectivity": 0.6308925151824951,
    "virtual_spectrum_summary": 0.130055770277977,
    "yield": 0.5933322310447693
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
      "catalyst": 3,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 340
    },
    {
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.0001
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 275
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
  "end_step": 211,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.24361194670200348,
    "conversion": 0.9946763515472412,
    "cost": 1.0,
    "crystal_csd_quality": 0.5490812063217163,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.987614095211029,
    "crystal_size": 0.06360113620758057,
    "crystal_yield": 0.4553741216659546,
    "degradation_warning": 0.05255497246980667,
    "safety_risk": 0.16229389607906342,
    "score": 0.4064655601978302,
    "selectivity": 0.5420827269554138,
    "virtual_spectrum_summary": 0.15763629972934723,
    "yield": 0.5425531268119812
  },
  "ordinal": 12
}
```

## K1

```json
{
  "payload": {
    "report": "Mechanistic account\n\nThe campaign indicates that the reaction and crystallization stages were strongly coupled through solvent identity, product concentration, impurity generation, and thermal history. All materials were anonymous benchmark identities, so the conclusions apply only to C0\u2013C3 and S0\u2013S3 in this fixed synthetic system.\n\nObserved material effects\n\nCatalyst C3 was the most useful catalyst among those carried into the later comparisons, although catalyst effects were not isolated cleanly from solvent and temperature. Batch 1 used C1/S2 at 360 K for 3600 s and reached complete conversion but gave selectivity 0.479, byproduct signal 0.359, degradation warning 0.167, and crystal recovery 0.381. Later C3 batches at 340 K for 1800 s generally had lower degradation (about 0.02\u20130.08) and better selectivity in favorable solvents. C0 was examined in batch 2, but under a different crystallization history; C2 was not tested. Consequently, C3 is an evidence-supported working choice, not a demonstrated global catalyst optimum.\n\nSolvent identity affected both reaction selectivity and crystallization. Batches 7, 8, 10, and 11 form the closest solvent comparison: each used C3, 0.040 mol reagent, 0.080 L solvent, 340 K for 1800 s, quenching, 0.0001 g seed, a single 14,400 s cooling operation to 270 K, filtration, and final assay.\n\n\u2022 Batch 7, S2: reaction yield 0.510, selectivity 0.485, crystal recovery 0.453, purity 0.977, normalized size 0.051, and fines fraction 0.987.\n\u2022 Batch 8, S1: reaction yield 0.543, selectivity 0.556, crystal recovery 0.480, purity 0.974, normalized size 0.073, and fines fraction 0.987.\n\u2022 Batch 10, S3: reaction yield 0.529, selectivity 0.523, crystal recovery 0.441, purity 0.961, normalized size 0.041, and fines fraction 1.000.\n\u2022 Batch 11, S0: reaction yield 0.593, selectivity 0.631, crystal recovery 0.492, purity 0.987, normalized size 0.046, and fines fraction 0.994.\n\nThus S0 gave the largest observed reaction yield and crystallization-stage recovery, whereas S1 gave the largest particles and best CSD-quality estimate in this matched comparison. Using the instrument definition, normalized size \u00d7 250 \u00b5m, the reported d50 values were approximately 18.2 \u00b5m for batch 8, 12.8 \u00b5m for batch 7, 11.4 \u00b5m for batch 11, and 10.2 \u00b5m for batch 10. This helps explain why all four remained dominated by particles below 20 \u00b5m. The nominal dossier had suggested particularly favorable growth and low nucleation for S2, but the realized campaign favored S1 for size and S0 for recovery; fixed-world residuals or reaction-stage coupling evidently outweighed the nominal prior.\n\nReaction\u2013crystallization coupling\n\nA useful conceptual reaction scheme is parallel desired and undesired conversion:\n\nR \u2192 P, rate rP = kP(C,S,T)\u00b7f(R)\nR \u2192 I, rate rI = kI(C,S,T)\u00b7f(R)\nP \u2192 D, rate rD = kD(S,T)\u00b7f(P).\n\nCatalyst and solvent alter the relative rate constants, while excessive temperature or residence time increases byproduct and degradation exposure. Batch 1 illustrates that complete conversion alone was not sufficient: its high-temperature treatment produced poor selectivity and a strong degradation warning. In contrast, the 340 K/1800 s C3 processes preserved high conversion while improving selectivity in S0 and S1.\n\nThe crystallizer did not receive identical material merely because conversion was similar. Differences in target concentration, impurity concentration, and degradation products could change the saturation concentration, heterogeneous nucleation rate, crystal-face growth, and impurity occlusion. This is consistent with the solvent-dependent reaction and CSD results. High crystal purity throughout most of the campaign\u2014typically about 0.96\u20131.00\u2014suggests that the crystal lattice rejected impurities effectively, even when the mother liquor contained appreciable byproduct. Purity therefore ceased to be the limiting quality attribute; particle number and fines became limiting.\n\nCrystallization interpretation\n\nThe observations are qualitatively described by supersaturation and a population balance:\n\nS = C/C*(T,solvent),\nB = kb(S\u22121)^b for S > 1,\nG = kg(S\u22121)^g,\n\u2202n(L,t)/\u2202t + \u2202[G n(L,t)]/\u2202L = nucleation \u2212 dissolution \u00b1 aggregation/attrition.\n\nHere B is the nucleation rate, G the linear growth rate, and n(L,t) the number distribution. A simple scaling for characteristic size is\n\nd50 \u221d [Msolid/(\u03c1N)]^(1/3),\n\nwhere N is the number of crystals. Recovery can increase Msolid, but if cooling simultaneously creates a very large N through secondary nucleation, d50 remains small and the number fraction below 20 \u00b5m stays high. This appears to have occurred throughout the campaign.\n\nProcess-history dependence\n\nCooling history mattered, but longer or more elaborate processing was not automatically beneficial. Batch 4 used S2/C3, 0.001 g seed, and eleven successive 14,400 s cooling segments down to 270 K. It produced recovery 0.439, purity 1.000, normalized size 0.038, and fines 1.000. Batch 7 instead used 0.0001 g seed and one direct 14,400 s cool to 270 K; recovery increased to 0.453, size to 0.051, and fines decreased slightly to 0.987. Repeated cooling segments therefore did not act as a simple growth hold; they likely maintained or repeatedly regenerated nucleating supersaturation.\n\nBatch 9 tested four additional 14,400 s holds at 270 K after the otherwise batch-8-like S1 process. Relative to batch 8, recovery changed from 0.480 to 0.471, normalized size from 0.073 to 0.023, and fines from 0.987 to 1.000. The direct observation is that the holds worsened the final CSD rather than ripening it. Secondary nucleation, attrition, or measurement variability are plausible explanations, but the campaign did not separately identify them.\n\nConcentration also mattered. Batch 5 halved the S2 solvent volume to 0.040 L and used a small seed with staged cooling. It gave recovery 0.454 but normalized size only 0.008 and fines 1.000. The interpretation is that increased supersaturation raised the number of new nuclei faster than it raised growth per particle. This is consistent with the population-balance scaling, although concentration was confounded with the staged cooling history.\n\nDeep cooling followed by reheating did not successfully remove fines. Batch 6 cooled gradually to 250 K and then reheated the slurry to 285 and 295 K in an attempt to dissolve small crystals selectively. Its final recovery was 0.394, purity 0.998, normalized size 0.011, and fines 1.000. In-process particle readings changed during reheating, but neither reading indicated a decisive fines reduction. The final result suggests substantial product redissolution without a sufficiently selective removal of the fine population.\n\nEndpoint temperature showed a recovery\u2013purity tradeoff but did not solve particle quality. Batch 12 repeated the S1-type direct process with a 275 K endpoint rather than 270 K. Compared with batch 8, recovery fell from 0.480 to 0.455 and purity increased from 0.974 to 0.988, while fines increased to 1.000. Stopping warmer therefore sacrificed recovery without creating a compliant CSD.\n\nRecovery definitions and useful coupling metric\n\nThe reported crystal_yield is crystallization-stage recovery:\n\nYcryst = seed-excluded recovered target product / target product present before separation.\n\nIt is not overall yield from charged reagent. For process reasoning only, an approximate overall recovered-target fraction can be represented as\n\nYoverall \u2248 Yreaction \u00d7 Ycryst.\n\nThis gives roughly 0.26 for batch 8 (0.543 \u00d7 0.480) and 0.29 for batch 11 (0.593 \u00d7 0.492). These products are not official campaign metrics, but they show why a strong reaction solvent such as S0 could have attractive total mass productivity even though its particle quality was poor.\n\nRevisions during the campaign\n\nThe initial approach emphasized S2 because its nominal dossier suggested low solubility, strong growth, low impurity occlusion, and low nucleation. Early batches then showed high purity and reasonable recovery but almost entirely fine particles. The campaign consequently revised seed loading downward, lengthened and staged cooling, tested aging, varied concentration, attempted temperature cycling, and finally compared all four solvents under a common direct-cooling protocol. Those revisions established that prolonged aging, extreme slow staging, concentration increase, and reheat/dissolution were not improvements in the tested forms. The solvent comparison shifted the working preference toward S1 for the best recovery/size compromise, while identifying S0 as the recovery leader.\n\nUncertainty and unresolved tradeoff\n\nFinal-assay standard uncertainties were approximately 0.01 for crystal recovery, 0.01 for purity, 0.025 in normalized crystal size (about 6.25 \u00b5m), and 0.018 for fines fraction. Individual size rankings are therefore uncertain, and some in-process particle measurements differed materially from final-assay size estimates. However, the fines results were approximately 0.987\u20131.000 in every relevant final assay, far from the required maximum of 0.50. Instrument noise cannot plausibly bridge that gap. The campaign therefore found high-purity, moderate-recovery crystallization but no quality-feasible batch.\n\nBatch 8 remains the sealed recommendation because it combined recovery 0.480, purity 0.974, the largest observed normalized size among the matched solvent comparison, and a near-minimum fines result. This does not imply that it satisfied the fines constraint; it did not. The unresolved problem is to reduce crystal number or selectively remove fines while retaining recovery. Untested alternatives include a true controlled supersaturation feed or antisolvent addition, classification or washing that physically removes fines, different seed size distributions rather than seed mass alone, lower-shear mixing during the cooling ramp, continuous fines dissolution with external circulation, testing catalyst C2, and broader catalyst\u2013solvent interaction designs. These mechanisms are plausible but were not demonstrated in the campaign."
  },
  "failure": null,
  "elapsed_s": 73.93700000000536,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 2645888,
    "input_tokens": 2974372,
    "output_tokens": 12859,
    "reasoning_output_tokens": 5444
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
          "estimate": 0.28,
          "lower80": 0.14,
          "upper80": 0.46
        },
        "crystal_purity": {
          "estimate": 0.95,
          "lower80": 0.9,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.17,
          "lower80": 0.11,
          "upper80": 0.23
        },
        "crystal_yield": {
          "estimate": 0.29,
          "lower80": 0.21,
          "upper80": 0.37
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q01"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.44,
          "lower80": 0.27,
          "upper80": 0.63
        },
        "crystal_purity": {
          "estimate": 0.91,
          "lower80": 0.84,
          "upper80": 0.97
        },
        "crystal_size": {
          "estimate": 0.12,
          "lower80": 0.07,
          "upper80": 0.18
        },
        "crystal_yield": {
          "estimate": 0.23,
          "lower80": 0.15,
          "upper80": 0.32
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q02"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.88,
          "lower80": 0.72,
          "upper80": 0.98
        },
        "crystal_purity": {
          "estimate": 0.9,
          "lower80": 0.83,
          "upper80": 0.96
        },
        "crystal_size": {
          "estimate": 0.055,
          "lower80": 0.02,
          "upper80": 0.1
        },
        "crystal_yield": {
          "estimate": 0.31,
          "lower80": 0.23,
          "upper80": 0.39
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q03"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.32,
          "lower80": 0.16,
          "upper80": 0.52
        },
        "crystal_purity": {
          "estimate": 0.91,
          "lower80": 0.84,
          "upper80": 0.97
        },
        "crystal_size": {
          "estimate": 0.15,
          "lower80": 0.09,
          "upper80": 0.21
        },
        "crystal_yield": {
          "estimate": 0.33,
          "lower80": 0.25,
          "upper80": 0.41
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q04"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.3,
          "lower80": 0.15,
          "upper80": 0.49
        },
        "crystal_purity": {
          "estimate": 0.91,
          "lower80": 0.84,
          "upper80": 0.97
        },
        "crystal_size": {
          "estimate": 0.15,
          "lower80": 0.09,
          "upper80": 0.21
        },
        "crystal_yield": {
          "estimate": 0.34,
          "lower80": 0.26,
          "upper80": 0.42
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q05"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.92,
          "lower80": 0.78,
          "upper80": 0.99
        },
        "crystal_purity": {
          "estimate": 0.9,
          "lower80": 0.82,
          "upper80": 0.96
        },
        "crystal_size": {
          "estimate": 0.045,
          "lower80": 0.015,
          "upper80": 0.085
        },
        "crystal_yield": {
          "estimate": 0.35,
          "lower80": 0.27,
          "upper80": 0.43
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q06"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.34,
          "lower80": 0.17,
          "upper80": 0.54
        },
        "crystal_purity": {
          "estimate": 0.91,
          "lower80": 0.84,
          "upper80": 0.97
        },
        "crystal_size": {
          "estimate": 0.145,
          "lower80": 0.085,
          "upper80": 0.21
        },
        "crystal_yield": {
          "estimate": 0.35,
          "lower80": 0.27,
          "upper80": 0.43
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q07"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.78,
          "lower80": 0.57,
          "upper80": 0.94
        },
        "crystal_purity": {
          "estimate": 0.93,
          "lower80": 0.86,
          "upper80": 0.98
        },
        "crystal_size": {
          "estimate": 0.06,
          "lower80": 0.02,
          "upper80": 0.11
        },
        "crystal_yield": {
          "estimate": 0.29,
          "lower80": 0.2,
          "upper80": 0.38
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q08"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.39,
          "lower80": 0.2,
          "upper80": 0.62
        },
        "crystal_purity": {
          "estimate": 0.94,
          "lower80": 0.86,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.11,
          "lower80": 0.055,
          "upper80": 0.17
        },
        "crystal_yield": {
          "estimate": 0.055,
          "lower80": 0.01,
          "upper80": 0.12
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q09"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.32,
          "lower80": 0.16,
          "upper80": 0.53
        },
        "crystal_purity": {
          "estimate": 0.93,
          "lower80": 0.86,
          "upper80": 0.98
        },
        "crystal_size": {
          "estimate": 0.12,
          "lower80": 0.065,
          "upper80": 0.18
        },
        "crystal_yield": {
          "estimate": 0.11,
          "lower80": 0.05,
          "upper80": 0.18
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q10"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.29,
          "lower80": 0.14,
          "upper80": 0.48
        },
        "crystal_purity": {
          "estimate": 0.91,
          "lower80": 0.84,
          "upper80": 0.97
        },
        "crystal_size": {
          "estimate": 0.155,
          "lower80": 0.095,
          "upper80": 0.22
        },
        "crystal_yield": {
          "estimate": 0.34,
          "lower80": 0.26,
          "upper80": 0.42
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q11"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.56,
          "lower80": 0.36,
          "upper80": 0.75
        },
        "crystal_purity": {
          "estimate": 0.88,
          "lower80": 0.8,
          "upper80": 0.95
        },
        "crystal_size": {
          "estimate": 0.11,
          "lower80": 0.06,
          "upper80": 0.17
        },
        "crystal_yield": {
          "estimate": 0.47,
          "lower80": 0.39,
          "upper80": 0.55
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q12"
      }
    ],
    "rationale": "The six pairs isolate: solvent (Q01\u2013Q02), seed loading (Q03\u2013Q04), slow ramp versus crash-cool/hold (Q05\u2013Q06), post-ramp hold versus heat-cycle (Q07\u2013Q08), immediate versus aged shallow crystallization (Q09\u2013Q10), and reagent loading (Q11\u2013Q12). I expect S1 to outperform S3 in growth, purity and recovery; a large seed charge and slow ramp to suppress secondary nucleation relative to the low-seed or crash-cooled cases; the 315 K cycle to redissolve product and create fines on rapid recooling; and aging at 292 K to raise the small seed-excluded recovery. Doubling reagent loading should raise recovery but also supersaturation, occlusion and fines. Every recipe contains an effective seed charge, so particles are expected even where seed-excluded recovery is small. Intervals are deliberately broad because campaign evidence did not directly cover this low catalyst/loading regime, final size measurements were noisy, and the predicted fines compliance of the slow-ramp and shallow-cooling cases remains uncertain."
  },
  "failure": null,
  "elapsed_s": 76.76499999998487,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 2649472,
    "input_tokens": 3142986,
    "output_tokens": 16675,
    "reasoning_output_tokens": 7608
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
    "report": "1. Status of the main claims\n\nSupported by direct observations\n\n\u2022 Solvent identity affected both reaction and crystallization. The closest comparison was batches 7, 8, 10 and 11, which shared C3, reaction charge, heating, seed loading and direct cooling but used S2, S1, S3 and S0, respectively. Batch 11/S0 had the highest reaction yield, selectivity and crystal recovery (0.593, 0.631 and 0.492), whereas batch 8/S1 had the largest normalized crystal size and best CSD quality in that set (0.073 and 0.576). This directly supports a material effect, although the molecular explanation remains interpretive.\n\n\u2022 Purity was not the campaign\u2019s limiting constraint. The cited matched batches had crystal purities of 0.961\u20130.987, and most other completed batches were similarly high. By contrast, final fines fractions were approximately 0.987\u20131.000. The conclusion that particle quality, rather than purity, prevented feasibility is therefore directly supported and robust to stated assay noise.\n\n\u2022 Additional aging did not improve the tested S1 process. Batch 9 added four 14,400 s holds after the otherwise batch-8-like crystallization. Its normalized size fell from 0.073 to 0.023 and fines rose from 0.987 to 1.000, while recovery changed from 0.480 to 0.471. The deterioration is observed; attributing it specifically to secondary nucleation or attrition is interpretation.\n\n\u2022 Elaborate staged cooling was not automatically superior. Batch 4 used eleven slow cooling segments with S2 and gave size 0.038, recovery 0.439 and fines 1.000. Batch 7 used a much simpler direct cooling step and gave size 0.051, recovery 0.453 and fines 0.987. This supports the operational conclusion that longer schedules alone did not solve fines.\n\n\u2022 The tested dissolution/recrystallization strategy failed. Batch 6 underwent deep cooling followed by reheating to 285 and 295 K. Its final recovery was 0.394, size 0.011 and fines 1.000. Product loss without a durable CSD improvement is directly observed. Preferential fines dissolution was the proposed mechanism, but it was contradicted in that implementation.\n\n\u2022 A warmer final temperature traded recovery for purity without solving fines. Batch 12 ended at 275 K and gave recovery 0.455, purity 0.988 and fines 1.000, versus 0.480, 0.974 and 0.987 for batch 8 at 270 K.\n\nContradicted or weakened\n\n\u2022 The nominal prior that S2 should be the best growth solvent was contradicted by the matched empirical comparison: S1 gave larger particles, while S0 gave greater recovery. The dossier was only prior evidence, so this is not an internal inconsistency; it shows that realized residuals and reaction coupling mattered.\n\n\u2022 Simple Ostwald-ripening expectations were contradicted. Neither extended holding in batch 9 nor reheating in batch 6 produced the expected durable reduction in fines.\n\n\u2022 The claim that higher concentration caused more secondary nucleation is plausible but weakly supported. Batch 5 used only 0.040 L S2 and ended with very small particles and fines 1.000, but it also differed in seed loading and cooling history. The observed poor CSD is real; assigning it uniquely to concentration is not justified.\n\nStill untested\n\n\u2022 C3 was never established as a catalyst optimum. It performed adequately in later batches, but catalyst identity was confounded with solvent and temperature. C2 was never tested, and there was no matched C0\u2013C3 catalyst series.\n\n\u2022 The population-balance explanation\u2014excess secondary nucleation increasing particle number faster than crystal mass\u2014is consistent with the results but was not directly demonstrated. No particle-number trajectory, supersaturation measurement or microscopy-based birth-rate estimate was obtained.\n\n\u2022 The prediction that a very large seed charge combined with an extremely slow ramp could suppress fines remains essentially untested. The campaign did not run the 0.035\u20130.045 g seed, low-loading, multi-day schedules used in several held-out recipes. Batch 1 used 0.020 g seed, but under substantially different reaction and cooling conditions.\n\n\u2022 The proposed overall-yield approximation, reaction yield \u00d7 crystallization recovery, is bookkeeping rather than a validated kinetic law.\n\n2. One additional experiment\n\nI would repeat batch 4 exactly\u2014S2/C3, 0.040 mol reagent, 0.080 L solvent, 340 K for 1800 s, quench, and the same eleven-stage slow ramp to 270 K\u2014but increase seed mass from 0.001 g to 0.045 g. I would include non-destructive particle-size measurements after the first crystal-forming stage, midway through the ramp and immediately before filtration, followed by the normal final assay.\n\nThis changes one principal factor relative to an existing completed batch and directly tests the largest unsupported assumption in the held-out predictions.\n\nCompeting explanations and expected outcomes:\n\n\u2022 Seeded-surface control: If campaign fines arose because insufficient seed surface allowed uncontrolled secondary nucleation, the high seed charge should consume supersaturation earlier. Fines should fall markedly, potentially toward or below 0.50, while recovery remains near batch 4\u2019s approximately 0.44 and purity remains high. The particle trajectory should show limited creation of a new fine mode.\n\n\u2022 Growth dilution/particle-number control: If added seed primarily increases the number of particles sharing a fixed product mass, characteristic size should decrease or remain small and fines should remain near 1.00. Recovery may change little because it is seed-excluded.\n\n\u2022 Cooling-history control: If repeated cooling operations themselves continually generate nuclei regardless of seed surface, the high-seed experiment should still end with high fines. Intermediate measurements would show fines increasing during successive stages rather than being fixed at seeding.\n\nA large fines reduction would support the high-seed assumptions used for Q01, Q02, Q04, Q05, Q07, Q11 and Q12. Failure would undermine the predicted feasibility of that whole group.\n\n3. Least effectively used observation and least reliable prediction\n\nThe account used the disagreement between in-process particle measurements and final assays least effectively. For example, batch 4\u2019s prefiltration particle measurement reported normalized size about 0.063, whereas its final assay reported about 0.038. In batch 6, successive readings changed from about 0.020 to 0.037 to 0.025, followed by a final value near 0.011. I largely treated these differences as noise. They could instead indicate real dissolution, filtration/phase-selection effects, or strong sampling variability. Without resolving that issue, mechanistic conclusions based on individual size values are less secure than conclusions based on the consistently extreme fines fractions.\n\nQ09 is the least reliable held-out prediction. It uses a large 0.025 g seed charge, only 0.004 mol reagent, a 60 s cool to 292 K and immediate filtration. The campaign did not examine such a seed-dominated, shallow, extremely short crystallization. It is uncertain whether appreciable seed-excluded product would form, whether the recovered-solid CSD would mostly reflect the original seeds, and how purity would behave when very little new product coats them. Thus my predictions of particles being present, low but nonzero recovery, and feasible fines relied much more on extrapolation than the other estimates."
  },
  "failure": null,
  "elapsed_s": 70.32800000000861,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 2806016,
    "input_tokens": 3315336,
    "output_tokens": 19398,
    "reasoning_output_tokens": 8716
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
    "selected_experiment_index": 8,
    "selection_rationale": "No completed batch met the fines constraint (all final fines fractions were about 0.99-1.00). Batch 8 is the best compromise: crystal_yield 0.480, crystal_purity 0.974, and fines 0.987, with the strongest overall score among near-minimum-fines batches."
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
        "catalyst": 3,
        "catalyst_amount_mol": 0.005,
        "operation": "add_catalyst"
      },
      {
        "duration_s": 1800,
        "operation": "heat",
        "stirring_speed_rpm": 400,
        "target_temperature_K": 340
      },
      {
        "operation": "quench"
      },
      {
        "operation": "seed_crystals",
        "seed_mass_g": 0.0001
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 270
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
    "lifecycle_index": 8,
    "source_attempts": 10
  },
  "prediction_evaluation": {
    "contrasts": [
      {
        "absolute_delta_error": 0.005711584904441819,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_yield",
        "predicted_delta": -0.05999999999999997,
        "resolved": true,
        "true_delta": -0.06571158490444179
      },
      {
        "absolute_delta_error": 0.03712357719061521,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_purity",
        "predicted_delta": -0.039999999999999925,
        "resolved": false,
        "true_delta": -0.0028764228093847155
      },
      {
        "absolute_delta_error": 0.06900493628075632,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_size",
        "predicted_delta": -0.05000000000000002,
        "resolved": true,
        "true_delta": 0.019004936280756307
      },
      {
        "absolute_delta_error": 0.8676947480077399,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.15999999999999998,
        "resolved": true,
        "true_delta": -0.7076947480077399
      },
      {
        "absolute_delta_error": 0.02008776257407513,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_yield",
        "predicted_delta": 0.020000000000000018,
        "resolved": false,
        "true_delta": -8.776257407511201e-05
      },
      {
        "absolute_delta_error": 0.0014172641935265018,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_purity",
        "predicted_delta": 0.010000000000000009,
        "resolved": false,
        "true_delta": 0.008582735806473507
      },
      {
        "absolute_delta_error": 0.09412512327580118,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_size",
        "predicted_delta": 0.095,
        "resolved": false,
        "true_delta": 0.0008748767241988226
      },
      {
        "absolute_delta_error": 0.5913792315776769,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.56,
        "resolved": false,
        "true_delta": 0.031379231577676914
      },
      {
        "absolute_delta_error": 0.009644873190271741,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_yield",
        "predicted_delta": 0.009999999999999953,
        "resolved": false,
        "true_delta": 0.0003551268097282123
      },
      {
        "absolute_delta_error": 0.005794923247214756,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.010000000000000009,
        "resolved": false,
        "true_delta": -0.004205076752785253
      },
      {
        "absolute_delta_error": 0.05845150632552566,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_size",
        "predicted_delta": -0.105,
        "resolved": true,
        "true_delta": -0.046548493674474334
      },
      {
        "absolute_delta_error": 0.12020093924299236,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.6200000000000001,
        "resolved": true,
        "true_delta": 0.7402009392429925
      },
      {
        "absolute_delta_error": 0.10146629297589665,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_yield",
        "predicted_delta": -0.06,
        "resolved": true,
        "true_delta": 0.04146629297589666
      },
      {
        "absolute_delta_error": 0.029830577525981616,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_purity",
        "predicted_delta": 0.020000000000000018,
        "resolved": false,
        "true_delta": -0.009830577525981599
      },
      {
        "absolute_delta_error": 0.044361440027973965,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_size",
        "predicted_delta": -0.08499999999999999,
        "resolved": true,
        "true_delta": -0.04063855997202603
      },
      {
        "absolute_delta_error": 0.3278652105803905,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.44,
        "resolved": true,
        "true_delta": 0.7678652105803905
      },
      {
        "absolute_delta_error": 0.07300038962529792,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_yield",
        "predicted_delta": 0.055,
        "resolved": true,
        "true_delta": 0.12800038962529792
      },
      {
        "absolute_delta_error": 0.0032827453629002967,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_purity",
        "predicted_delta": -0.009999999999999898,
        "resolved": true,
        "true_delta": -0.013282745362900195
      },
      {
        "absolute_delta_error": 0.0034657554675174077,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_size",
        "predicted_delta": 0.009999999999999995,
        "resolved": true,
        "true_delta": 0.013465755467517403
      },
      {
        "absolute_delta_error": 0.09884240834118413,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.07,
        "resolved": false,
        "true_delta": 0.028842408341184123
      },
      {
        "absolute_delta_error": 0.09746325316856785,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_yield",
        "predicted_delta": 0.12999999999999995,
        "resolved": true,
        "true_delta": 0.032536746831432095
      },
      {
        "absolute_delta_error": 0.024192382855165673,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_purity",
        "predicted_delta": -0.030000000000000027,
        "resolved": false,
        "true_delta": -0.005807617144834354
      },
      {
        "absolute_delta_error": 0.010611719188503121,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_size",
        "predicted_delta": -0.045,
        "resolved": true,
        "true_delta": -0.03438828081149688
      },
      {
        "absolute_delta_error": 0.47102589522834876,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.2700000000000001,
        "resolved": true,
        "true_delta": 0.7410258952283488
      }
    ],
    "failures": [],
    "metrics": {
      "crystal_fines_fraction": {
        "coverage80": 0.4166666666666667,
        "interval_score80": 2.1213216530416745,
        "interval_width": 0.34249999999999997,
        "mae": 0.30795634562215196,
        "n": 12,
        "planned": 12
      },
      "crystal_purity": {
        "coverage80": 0.16666666666666666,
        "interval_score80": 0.26551434346492936,
        "interval_width": 0.12749999999999997,
        "mae": 0.07001327696848725,
        "n": 12,
        "planned": 12
      },
      "crystal_size": {
        "coverage80": 0.5,
        "interval_score80": 0.18898194890484485,
        "interval_width": 0.10833333333333334,
        "mae": 0.05252182471528569,
        "n": 12,
        "planned": 12
      },
      "crystal_yield": {
        "coverage80": 0.6666666666666666,
        "interval_score80": 0.23756308971502546,
        "interval_width": 0.15583333333333332,
        "mae": 0.060394215282369317,
        "n": 12,
        "planned": 12
      }
    },
    "quality": {
      "balanced_accuracy": 0.6666666666666667,
      "false_negative": 1,
      "false_positive": 3,
      "true_negative": 3,
      "true_positive": 5
    },
    "resolved_direction_correct": 10,
    "resolved_direction_n": 14,
    "tie_correct": 2,
    "tie_n": 10,
    "valid": true
  },
  "public_baselines": {
    "available": true,
    "mae": {
      "public_mean": {
        "crystal_fines_fraction": 0.3690826401732719,
        "crystal_purity": 0.004835775993945616,
        "crystal_size": 0.028249380614189926,
        "crystal_yield": 0.19366684056255146
      },
      "public_nearest_neighbor": {
        "crystal_fines_fraction": 0.3704345978742514,
        "crystal_purity": 0.010692180876563798,
        "crystal_size": 0.05718294521887338,
        "crystal_yield": 0.16738820817999964
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
        "cached_input": 2642432,
        "input": 2817683,
        "output": 9470,
        "stage": "source",
        "uncached_input": 175251
      },
      {
        "cached_input": 3456,
        "input": 156689,
        "output": 3389,
        "stage": "K1",
        "uncached_input": 153233
      },
      {
        "cached_input": 3584,
        "input": 168614,
        "output": 3816,
        "stage": "Q",
        "uncached_input": 165030
      },
      {
        "cached_input": 156544,
        "input": 172350,
        "output": 2723,
        "stage": "K2",
        "uncached_input": 15806
      }
    ],
    "total": {
      "cached_input": 2806016,
      "input": 3315336,
      "input_plus_output": 3334734,
      "output": 19398,
      "uncached_input": 509320
    },
    "valid": true
  },
  "elapsed_s": 775.1100000000151
}
```
