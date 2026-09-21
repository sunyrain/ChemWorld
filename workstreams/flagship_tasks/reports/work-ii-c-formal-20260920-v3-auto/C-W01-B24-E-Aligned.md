# C-W01-B24-E-Aligned

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
      "operation": "seed_crystals",
      "seed_mass_g": 0.02
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 7200,
      "operation": "wait",
      "stirring_speed_rpm": 200
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
    "byproduct_signal": 0.3293435871601105,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.48854905366897583,
    "crystal_fines_fraction": 0.9972988367080688,
    "crystal_purity": 0.9881334900856018,
    "crystal_size": 0.06328985095024109,
    "crystal_yield": 0.44008734822273254,
    "degradation_warning": 0.16778242588043213,
    "safety_risk": 0.1809559166431427,
    "score": 0.3884808421134949,
    "selectivity": 0.536551833152771,
    "virtual_spectrum_summary": 0.25664106011390686,
    "yield": 0.534389317035675
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 345
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
      "target_temperature_K": 305
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
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
      "operation": "cool_crystallize",
      "target_temperature_K": 285
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
  "end_step": 31,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.32234466075897217,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5577437281608582,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9844785928726196,
    "crystal_size": 0.07049662619829178,
    "crystal_yield": 0.4345051050186157,
    "degradation_warning": 0.1381588876247406,
    "safety_risk": 0.18007516860961914,
    "score": 0.3986913561820984,
    "selectivity": 0.5320335030555725,
    "virtual_spectrum_summary": 0.23946106433868408,
    "yield": 0.5205885171890259
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 345
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
      "target_temperature_K": 285
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 285
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
  "end_step": 50,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.3128148317337036,
    "conversion": 0.9983178377151489,
    "cost": 1.0,
    "crystal_csd_quality": 0.5503503084182739,
    "crystal_fines_fraction": 0.9949332475662231,
    "crystal_purity": 0.9911827445030212,
    "crystal_size": 0.030970720574259758,
    "crystal_yield": 0.4372482895851135,
    "degradation_warning": 0.15099571645259857,
    "safety_risk": 0.18047018349170685,
    "score": 0.39645159244537354,
    "selectivity": 0.528861403465271,
    "virtual_spectrum_summary": 0.23999622464179993,
    "yield": 0.5279740691184998
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 345
    },
    {
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
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
  "end_step": 64,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.306863009929657,
    "conversion": 0.9889963865280151,
    "cost": 1.0,
    "crystal_csd_quality": 0.5185962915420532,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 1.0,
    "crystal_size": 0.04188845679163933,
    "crystal_yield": 0.4523535370826721,
    "degradation_warning": 0.12101050466299057,
    "safety_risk": 0.18107371032238007,
    "score": 0.3989239037036896,
    "selectivity": 0.553191065788269,
    "virtual_spectrum_summary": 0.22322939336299896,
    "yield": 0.5395613312721252
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
      "target_temperature_K": 345
    },
    {
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
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
  "end_step": 77,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.32698023319244385,
    "conversion": 0.9963377714157104,
    "cost": 1.0,
    "crystal_csd_quality": 0.5158641934394836,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9781853556632996,
    "crystal_size": 0.019041581079363823,
    "crystal_yield": 0.3892729580402374,
    "degradation_warning": 0.13868604600429535,
    "safety_risk": 0.1773403137922287,
    "score": 0.37904492020606995,
    "selectivity": 0.5624376535415649,
    "virtual_spectrum_summary": 0.24224784970283508,
    "yield": 0.5562846064567566
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 345
    },
    {
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 297
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 400
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 294
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 400
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 291
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 400
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 288
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 400
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 285
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 400
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 282
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 400
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 279
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 400
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 276
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 400
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 273
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 400
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 400
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
  "end_step": 107,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.3244551420211792,
    "conversion": 0.992433488368988,
    "cost": 1.0,
    "crystal_csd_quality": 0.49907752871513367,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 1.0,
    "crystal_size": 0.01630181446671486,
    "crystal_yield": 0.46048203110694885,
    "degradation_warning": 0.14322194457054138,
    "safety_risk": 0.18107371032238007,
    "score": 0.3945041000843048,
    "selectivity": 0.542445182800293,
    "virtual_spectrum_summary": 0.24290020763874054,
    "yield": 0.5443307161331177
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 345
    },
    {
      "operation": "quench"
    },
    {
      "duration_s": 1,
      "operation": "cool_crystallize",
      "target_temperature_K": 285
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 1,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
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
      "duration_s": 600,
      "operation": "cool_crystallize",
      "target_temperature_K": 285
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 600,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
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
  "end_step": 128,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.3144717216491699,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.46921631693840027,
    "crystal_fines_fraction": 0.9868565201759338,
    "crystal_purity": 0.9812608361244202,
    "crystal_size": 0.0648275762796402,
    "crystal_yield": 0.4663010537624359,
    "degradation_warning": 0.13619405031204224,
    "safety_risk": 0.18046899139881134,
    "score": 0.388329416513443,
    "selectivity": 0.5029867887496948,
    "virtual_spectrum_summary": 0.23424676060676575,
    "yield": 0.5296339988708496
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
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.02
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
      "target_temperature_K": 345
    },
    {
      "operation": "quench"
    },
    {
      "duration_s": 1200,
      "operation": "cool_crystallize",
      "target_temperature_K": 290
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "instrument": "particle_size",
      "operation": "measure"
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
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
  "end_step": 151,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.30457833409309387,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.49949321150779724,
    "crystal_fines_fraction": 0.9869766235351562,
    "crystal_purity": 0.9766295552253723,
    "crystal_size": 0.08187712728977203,
    "crystal_yield": 0.4048303961753845,
    "degradation_warning": 0.13963216543197632,
    "safety_risk": 0.1738753765821457,
    "score": 0.3821561336517334,
    "selectivity": 0.5367437601089478,
    "virtual_spectrum_summary": 0.23035255074501038,
    "yield": 0.5284372568130493
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
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.02
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
      "target_temperature_K": 345
    },
    {
      "operation": "quench"
    },
    {
      "duration_s": 1200,
      "operation": "cool_crystallize",
      "target_temperature_K": 290
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 600
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
  "end_step": 212,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.3150278925895691,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.4744790196418762,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9788430333137512,
    "crystal_size": 0.03235702961683273,
    "crystal_yield": 0.3957374691963196,
    "degradation_warning": 0.13223576545715332,
    "safety_risk": 0.1738753765821457,
    "score": 0.3677346706390381,
    "selectivity": 0.5149763822555542,
    "virtual_spectrum_summary": 0.23277144134044647,
    "yield": 0.5286511182785034
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
      "target_temperature_K": 345
    },
    {
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 290
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
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
  "end_step": 247,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.31010833382606506,
    "conversion": 0.9858241677284241,
    "cost": 1.0,
    "crystal_csd_quality": 0.43527770042419434,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9801362156867981,
    "crystal_size": 0.05497993528842926,
    "crystal_yield": 0.46345677971839905,
    "degradation_warning": 0.1467718929052353,
    "safety_risk": 0.18107371032238007,
    "score": 0.38344529271125793,
    "selectivity": 0.544298529624939,
    "virtual_spectrum_summary": 0.2366069257259369,
    "yield": 0.5532252788543701
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
      "target_temperature_K": 345
    },
    {
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 600,
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
  "end_step": 258,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.3186229169368744,
    "conversion": 0.9990202784538269,
    "cost": 1.0,
    "crystal_csd_quality": 0.45043617486953735,
    "crystal_fines_fraction": 0.9935539960861206,
    "crystal_purity": 0.9951719641685486,
    "crystal_size": 0.050028759986162186,
    "crystal_yield": 0.45441919565200806,
    "degradation_warning": 0.12379191070795059,
    "safety_risk": 0.18107371032238007,
    "score": 0.38735783100128174,
    "selectivity": 0.5613960027694702,
    "virtual_spectrum_summary": 0.23094896972179413,
    "yield": 0.5419061183929443
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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 345
    },
    {
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
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
  "end_step": 270,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.242761492729187,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.47790566086769104,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9951460957527161,
    "crystal_size": 0.06893045455217361,
    "crystal_yield": 0.494229257106781,
    "degradation_warning": 0.09871899336576462,
    "safety_risk": 0.14528828859329224,
    "score": 0.41875195503234863,
    "selectivity": 0.6114495992660522,
    "virtual_spectrum_summary": 0.17794236540794373,
    "yield": 0.6164493560791016
  },
  "ordinal": 12
}
```

## Batch 13

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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 345
    },
    {
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
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
  "end_step": 282,
  "lifecycle_index": 13,
  "metrics": {
    "byproduct_signal": 0.33273571729660034,
    "conversion": 0.9972154498100281,
    "cost": 1.0,
    "crystal_csd_quality": 0.4863705039024353,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9811129570007324,
    "crystal_size": 0.053376879543066025,
    "crystal_yield": 0.3828636407852173,
    "degradation_warning": 0.13499124348163605,
    "safety_risk": 0.15538987517356873,
    "score": 0.3653987944126129,
    "selectivity": 0.5020354390144348,
    "virtual_spectrum_summary": 0.2437507063150406,
    "yield": 0.4940221607685089
  },
  "ordinal": 13
}
```

## Batch 14

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
      "target_temperature_K": 345
    },
    {
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
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
  "end_step": 294,
  "lifecycle_index": 14,
  "metrics": {
    "byproduct_signal": 0.36811625957489014,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.48885378241539,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9577596783638,
    "crystal_size": 0.08677804470062256,
    "crystal_yield": 0.34379842877388,
    "degradation_warning": 0.1491505652666092,
    "safety_risk": 0.18112343549728394,
    "score": 0.34714624285697937,
    "selectivity": 0.4682122766971588,
    "virtual_spectrum_summary": 0.26958170533180237,
    "yield": 0.4620247781276703
  },
  "ordinal": 14
}
```

## Batch 15

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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 345
    },
    {
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 280
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
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
  "end_step": 319,
  "lifecycle_index": 15,
  "metrics": {
    "byproduct_signal": 0.25399747490882874,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.4611462950706482,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9882932901382446,
    "crystal_size": 0.05855051055550575,
    "crystal_yield": 0.48556697368621826,
    "degradation_warning": 0.08812060952186584,
    "safety_risk": 0.14532332122325897,
    "score": 0.41161835193634033,
    "selectivity": 0.6160256862640381,
    "virtual_spectrum_summary": 0.17935289442539215,
    "yield": 0.620517909526825
  },
  "ordinal": 15
}
```

## Batch 16

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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 345
    },
    {
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 1200,
      "operation": "cool_crystallize",
      "target_temperature_K": 290
    },
    {
      "instrument": "particle_size",
      "operation": "measure"
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "instrument": "particle_size",
      "operation": "measure"
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "instrument": "particle_size",
      "operation": "measure"
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "instrument": "particle_size",
      "operation": "measure"
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "instrument": "particle_size",
      "operation": "measure"
    },
    {
      "duration_s": 1200,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
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
  "end_step": 352,
  "lifecycle_index": 16,
  "metrics": {
    "byproduct_signal": 0.24707633256912231,
    "conversion": 0.9884854555130005,
    "cost": 1.0,
    "crystal_csd_quality": 0.4409802258014679,
    "crystal_fines_fraction": 0.9877496957778931,
    "crystal_purity": 0.9783076047897339,
    "crystal_size": 0.05279213562607765,
    "crystal_yield": 0.4835275411605835,
    "degradation_warning": 0.09944485872983932,
    "safety_risk": 0.1452474743127823,
    "score": 0.40413767099380493,
    "selectivity": 0.6131773591041565,
    "virtual_spectrum_summary": 0.18064217269420624,
    "yield": 0.6114896535873413
  },
  "ordinal": 16
}
```

## Batch 17

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
      "volume_L": 0.075
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
      "target_temperature_K": 345
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 290
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 280
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
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
  "end_step": 368,
  "lifecycle_index": 17,
  "metrics": {
    "byproduct_signal": 0.29175400733947754,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.8095347881317139,
    "crystal_fines_fraction": 0.14523553848266602,
    "crystal_purity": 1.0,
    "crystal_size": 0.08747423440217972,
    "crystal_yield": 0.5017808675765991,
    "degradation_warning": 0.11553090810775757,
    "safety_risk": 0.1485082358121872,
    "score": 0.5714733600616455,
    "selectivity": 0.5888494849205017,
    "virtual_spectrum_summary": 0.21245360374450684,
    "yield": 0.5990077257156372
  },
  "ordinal": 17
}
```

## Batch 18

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
      "volume_L": 0.075
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
      "target_temperature_K": 345
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 290
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 280
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 260
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
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
  "end_step": 386,
  "lifecycle_index": 18,
  "metrics": {
    "byproduct_signal": 0.2535502016544342,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.8397201299667358,
    "crystal_fines_fraction": 0.16555045545101166,
    "crystal_purity": 0.997106671333313,
    "crystal_size": 0.14148734509944916,
    "crystal_yield": 0.5306053757667542,
    "degradation_warning": 0.10014333575963974,
    "safety_risk": 0.15293283760547638,
    "score": 0.590733528137207,
    "selectivity": 0.6053629517555237,
    "virtual_spectrum_summary": 0.18451711535453796,
    "yield": 0.6187698841094971
  },
  "ordinal": 18
}
```

## Batch 19

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
      "volume_L": 0.075
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
      "target_temperature_K": 345
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 290
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 280
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 260
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
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
  "end_step": 404,
  "lifecycle_index": 19,
  "metrics": {
    "byproduct_signal": 0.26543310284614563,
    "conversion": 0.9909029006958008,
    "cost": 1.0,
    "crystal_csd_quality": 0.8316301107406616,
    "crystal_fines_fraction": 0.12345990538597107,
    "crystal_purity": 0.9676246643066406,
    "crystal_size": 0.0801239088177681,
    "crystal_yield": 0.5251975655555725,
    "degradation_warning": 0.0634501725435257,
    "safety_risk": 0.15090413391590118,
    "score": 0.5761398673057556,
    "selectivity": 0.5921799540519714,
    "virtual_spectrum_summary": 0.17454078793525696,
    "yield": 0.5957663655281067
  },
  "ordinal": 19
}
```

## Batch 20

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
      "volume_L": 0.075
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
      "target_temperature_K": 345
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 290
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 280
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 260
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
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
  "end_step": 422,
  "lifecycle_index": 20,
  "metrics": {
    "byproduct_signal": 0.31073105335235596,
    "conversion": 0.9934642910957336,
    "cost": 1.0,
    "crystal_csd_quality": 0.7973810434341431,
    "crystal_fines_fraction": 0.16951166093349457,
    "crystal_purity": 0.983150064945221,
    "crystal_size": 0.0924495980143547,
    "crystal_yield": 0.40767499804496765,
    "degradation_warning": 0.045594461262226105,
    "safety_risk": 0.1359642595052719,
    "score": 0.5193430185317993,
    "selectivity": 0.4918704032897949,
    "virtual_spectrum_summary": 0.1914195865392685,
    "yield": 0.4755479693412781
  },
  "ordinal": 20
}
```

## Batch 21

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
      "volume_L": 0.075
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
      "target_temperature_K": 345
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 290
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 280
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 260
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
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
  "end_step": 440,
  "lifecycle_index": 21,
  "metrics": {
    "byproduct_signal": 0.26066088676452637,
    "conversion": 0.989408016204834,
    "cost": 1.0,
    "crystal_csd_quality": 0.8525293469429016,
    "crystal_fines_fraction": 0.157626673579216,
    "crystal_purity": 0.9861482977867126,
    "crystal_size": 0.07613570243120193,
    "crystal_yield": 0.5319129824638367,
    "degradation_warning": 0.09856788069009781,
    "safety_risk": 0.15142568945884705,
    "score": 0.5827029943466187,
    "selectivity": 0.5864408016204834,
    "virtual_spectrum_summary": 0.18771903216838837,
    "yield": 0.6057174801826477
  },
  "ordinal": 21
}
```

## Batch 22

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
      "volume_L": 0.075
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
      "target_temperature_K": 345
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 290
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 280
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 260
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
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
  "end_step": 462,
  "lifecycle_index": 22,
  "metrics": {
    "byproduct_signal": 0.3451787531375885,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.8119483590126038,
    "crystal_fines_fraction": 0.14615735411643982,
    "crystal_purity": 0.999248743057251,
    "crystal_size": 0.09288587421178818,
    "crystal_yield": 0.5198860168457031,
    "degradation_warning": 0.12487073987722397,
    "safety_risk": 0.15102282166481018,
    "score": 0.5703667998313904,
    "selectivity": 0.5613977909088135,
    "virtual_spectrum_summary": 0.24604015052318573,
    "yield": 0.5626766681671143
  },
  "ordinal": 22
}
```

## Batch 23

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
      "volume_L": 0.075
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
      "target_temperature_K": 345
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 290
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 280
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 260
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
  "end_step": 479,
  "lifecycle_index": 23,
  "metrics": {
    "byproduct_signal": 0.2643667757511139,
    "conversion": 0.9948381781578064,
    "cost": 1.0,
    "crystal_csd_quality": 0.8286324739456177,
    "crystal_fines_fraction": 0.11358926445245743,
    "crystal_purity": 0.9933879375457764,
    "crystal_size": 0.11454331874847412,
    "crystal_yield": 0.5143724083900452,
    "degradation_warning": 0.08564898371696472,
    "safety_risk": 0.14816386997699738,
    "score": 0.5859902501106262,
    "selectivity": 0.6110994219779968,
    "virtual_spectrum_summary": 0.1839437633752823,
    "yield": 0.6127459406852722
  },
  "ordinal": 23
}
```

## Batch 24

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
      "volume_L": 0.075
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
      "target_temperature_K": 345
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 290
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 280
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 260
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
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
  "end_step": 497,
  "lifecycle_index": 24,
  "metrics": {
    "byproduct_signal": 0.28350043296813965,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.8007595539093018,
    "crystal_fines_fraction": 0.18006253242492676,
    "crystal_purity": 1.0,
    "crystal_size": 0.09189014136791229,
    "crystal_yield": 0.5084845423698425,
    "degradation_warning": 0.09790502488613129,
    "safety_risk": 0.15142568945884705,
    "score": 0.5692112445831299,
    "selectivity": 0.5950046181678772,
    "virtual_spectrum_summary": 0.19998249411582947,
    "yield": 0.6042539477348328
  },
  "ordinal": 24
}
```

## K1

```json
{
  "payload": {
    "report": "Mechanistic account\n\nThe campaign indicates that reaction chemistry and crystal quality were strongly coupled through solvent/catalyst choice, but process history\u2014especially whether the reaction mixture was quenched before controlled cooling\u2014was the dominant determinant of the fines population.\n\nMaterial effects\n\nObservation: Solvent S0 gave the best reaction and recovery results among the quenched comparison batches. Batch 12 (S0/C1) produced reaction yield 0.616, selectivity 0.611, byproduct signal 0.243, crystal recovery 0.494, and purity 0.995. Comparable batches with S1 and S3 gave lower recoveries: 0.383 in batch 13 and 0.344 in batch 14. Representative S2 processes gave recoveries of 0.440\u20130.466 in batches 1 and 7. All of these quenched batches nevertheless had fines fractions near 1.\n\nInterpretation: S0 improved the amount and cleanliness of target entering crystallization, despite its nominal dossier suggesting relatively high solubility, nucleation tendency, and impurity occlusion. The empirical result therefore overrode that prior. Its benefit probably arose partly from reaction selectivity and reduced byproduct loading, not simply equilibrium solubility.\n\nObservation: Catalyst choice remained important under the successful unquenched protocol. With otherwise similar S0 staged-cooling recipes, C0 gave recovery 0.525, purity 0.968, and fines 0.123 in batch 19; C2 gave only 0.408 recovery, selectivity 0.492, and fines 0.170 in batch 20; C3 gave 0.532 recovery, purity 0.986, selectivity 0.586, and fines 0.158 in recommended batch 21. C1 reached 0.531 recovery, 0.997 purity, and 0.166 fines in batch 18.\n\nInterpretation: Catalyst effects propagated into crystallization through target concentration and impurity composition. C2\u2019s low selectivity plausibly reduced recoverable target or interfered with growth. C1 and C3 were much better choices. The small observed recovery difference between them is not mechanistically decisive because it is comparable to assay and batch variability.\n\nReaction\u2013crystallization coupling\n\nA useful bookkeeping distinction is\n\nX = reacted reagent / initial reagent,\nS = target formed / reacted reagent,\nY_rxn \u2248 X\u00b7S,\nR_c = seed-excluded target recovered as crystals / target present before separation.\n\nThus R_c is a crystallization-stage recovery, not an overall yield from charged reagent. A rough overall isolated-target fraction is Y_rxn\u00b7R_c. For batch 21 this is approximately 0.606 \u00d7 0.532 = 0.322. This distinction explains why nearly complete conversion alone was insufficient: batch 1 had conversion 1.000 but selectivity only 0.545, byproduct signal 0.329, reaction yield 0.539, and crystal recovery 0.440.\n\nThe impurity burden affected both the target available for crystallization and the crystal environment. Nevertheless, high final crystal purity was common even in mediocre reaction mixtures, showing that crystallization provided strong purification. Recovery and reaction yield should therefore be optimized jointly rather than treating conversion as the sole reaction endpoint.\n\nProcess-history dependence\n\nObservation: Every evaluated protocol that quenched before crystallization produced an unacceptable fines fraction, generally 0.98\u20131.00. Changing seed charge did not repair this: batches 2\u20134 used seed charges from 0.0001 to 0.05 g yet finished with fines near 1. Batch 7 omitted seed and still had fines 0.987. Very long aging was also ineffective: batch 9 used 50 long holds but ended at recovery 0.396 and fines 1.00. A mild 280 K thermal-aging cycle in batch 15 similarly retained fines 1.00.\n\nInterpretation: The abrupt quench probably established a large, irreversible primary or secondary nucleus population before controlled seed-mediated growth could dominate. Once that number population existed, later holding or mild thermal cycling did not dissolve enough fines to reset the distribution. Seed amount was therefore secondary to when supersaturation was created.\n\nThe decisive revision was to omit the quench, seed while the mixture remained hot, and cool slowly in stages. Batch 17 used this strategy with stages from 330 to 270 K and immediately changed the fines fraction from approximately 1 to 0.145, while giving recovery 0.502, purity 1.000, and CSD quality 0.810. Extending the staged profile to 250 K in batch 18 raised recovery to 0.531 while maintaining purity 0.997 and fines 0.166. This abrupt improvement supports a history-dependent nucleation mechanism rather than a simple equilibrium-solubility explanation.\n\nUnder the interpretation above, hot seeding provided a controlled population of growth sites before large supersaturation developed. Gradual cooling then favored deposition on existing crystals over uncontrolled nucleation. The final low temperature increased crystallization driving force and recovery. The successful CSD quality values of about 0.80\u20130.85 in batches 17\u201324, compared with roughly 0.44\u20130.56 in the quenched experiments, reinforce this account.\n\nRecommended operating history\n\nRecommended batch 21 used S0, C3, full reagent and catalyst charges, reaction heating near 345 K for 3600 s with stirring, no quench, a 0.05 g hot seed charge, staged 14,400 s cooling steps through 330, 320, 310, 300, 290, 280, 270, 260, and 250 K, followed by one 14,400 s growth hold at 300 rpm, filtration, and assay. It delivered the highest observed qualifying recovery, 0.5319, with purity 0.9861, fines 0.1576, CSD quality 0.8525, and conversion 0.9894.\n\nRevisions and uncertainty\n\nThe research strategy was revised substantially. Early work focused on seed loading, cooling rate, aging time, solvent volume, and thermal cycling after quench. Those interventions failed because they acted after the fines population had apparently been established. The later revision moved nucleation control upstream by eliminating the quench and seeding before staged cooling; this produced the key quality improvement.\n\nReplicates show meaningful variability. With closely related C3/S0 staged-cooling histories, recoveries were 0.532 in batch 21, 0.520 after five terminal holds in batch 22, 0.514 without a terminal hold in batch 23, and 0.508 with one hold in batch 24. Their fines fractions ranged from 0.114 to 0.180. Consequently, neither the exact benefit of one final hold nor the small C1-versus-C3 difference is resolved. Batch 21 is the best observed qualifying experiment, not proof of a unique global optimum.\n\nA modest quality/recovery tradeoff remains. Extending cooling from 270 K in batch 17 to 250 K in batch 18 increased recovery from 0.502 to 0.531 while fines rose from 0.145 to 0.166; both remained comfortably within specification. Immediate filtration in batch 23 gave especially low fines (0.114) but lower recovery (0.514), whereas extra holds did not reproducibly increase recovery. Thus continued growth may improve or degrade recovery depending on batch realization, and the terminal hold effect needs replication.\n\nUntested alternatives include seeding immediately before a deliberately milder quench, narrower cooling increments above 330 K, different seed size distributions, controlled slurry classification, and replicated C1/C3 comparisons. These remain hypotheses rather than conclusions. Within the tested domain, the most defensible mechanism is that solvent and catalyst determine target/impurity loading, while the absence of an abrupt quench and preservation of a controlled seeded growth history determine whether the fines constraint is met."
  },
  "failure": null,
  "elapsed_s": 74.82800000000861,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 1352320,
    "input_tokens": 1473241,
    "output_tokens": 16110,
    "reasoning_output_tokens": 6588
  },
  "numerics_budget": {
    "limit": 128,
    "on_exhaustion": "continue_answer",
    "version": "public-numerics-budget-v1"
  },
  "numerics_attempts": 1
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
          "estimate": 0.98,
          "lower80": 0.93,
          "upper80": 1
        },
        "crystal_size": {
          "estimate": 0.18,
          "lower80": 0.1,
          "upper80": 0.28
        },
        "crystal_yield": {
          "estimate": 0.34,
          "lower80": 0.22,
          "upper80": 0.46
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q01"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.46,
          "lower80": 0.27,
          "upper80": 0.67
        },
        "crystal_purity": {
          "estimate": 0.95,
          "lower80": 0.87,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.13,
          "lower80": 0.06,
          "upper80": 0.22
        },
        "crystal_yield": {
          "estimate": 0.27,
          "lower80": 0.16,
          "upper80": 0.4
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q02"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.6,
          "lower80": 0.39,
          "upper80": 0.81
        },
        "crystal_purity": {
          "estimate": 0.97,
          "lower80": 0.91,
          "upper80": 1
        },
        "crystal_size": {
          "estimate": 0.09,
          "lower80": 0.035,
          "upper80": 0.17
        },
        "crystal_yield": {
          "estimate": 0.28,
          "lower80": 0.17,
          "upper80": 0.4
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q03"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.4,
          "lower80": 0.22,
          "upper80": 0.61
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.93,
          "upper80": 1
        },
        "crystal_size": {
          "estimate": 0.16,
          "lower80": 0.08,
          "upper80": 0.25
        },
        "crystal_yield": {
          "estimate": 0.34,
          "lower80": 0.23,
          "upper80": 0.46
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q04"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.4,
          "lower80": 0.22,
          "upper80": 0.6
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.93,
          "upper80": 1
        },
        "crystal_size": {
          "estimate": 0.17,
          "lower80": 0.09,
          "upper80": 0.26
        },
        "crystal_yield": {
          "estimate": 0.34,
          "lower80": 0.23,
          "upper80": 0.46
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q05"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.8,
          "lower80": 0.61,
          "upper80": 0.96
        },
        "crystal_purity": {
          "estimate": 0.96,
          "lower80": 0.89,
          "upper80": 1
        },
        "crystal_size": {
          "estimate": 0.065,
          "lower80": 0.02,
          "upper80": 0.13
        },
        "crystal_yield": {
          "estimate": 0.36,
          "lower80": 0.24,
          "upper80": 0.49
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q06"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.38,
          "lower80": 0.2,
          "upper80": 0.58
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.93,
          "upper80": 1
        },
        "crystal_size": {
          "estimate": 0.18,
          "lower80": 0.1,
          "upper80": 0.28
        },
        "crystal_yield": {
          "estimate": 0.35,
          "lower80": 0.24,
          "upper80": 0.47
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q07"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.74,
          "lower80": 0.53,
          "upper80": 0.92
        },
        "crystal_purity": {
          "estimate": 0.96,
          "lower80": 0.89,
          "upper80": 1
        },
        "crystal_size": {
          "estimate": 0.08,
          "lower80": 0.025,
          "upper80": 0.15
        },
        "crystal_yield": {
          "estimate": 0.31,
          "lower80": 0.19,
          "upper80": 0.44
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q08"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.31,
          "lower80": 0.14,
          "upper80": 0.54
        },
        "crystal_purity": {
          "estimate": 0.99,
          "lower80": 0.94,
          "upper80": 1
        },
        "crystal_size": {
          "estimate": 0.055,
          "lower80": 0.02,
          "upper80": 0.11
        },
        "crystal_yield": {
          "estimate": 0.045,
          "lower80": 0.01,
          "upper80": 0.1
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q09"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.27,
          "lower80": 0.12,
          "upper80": 0.48
        },
        "crystal_purity": {
          "estimate": 0.99,
          "lower80": 0.94,
          "upper80": 1
        },
        "crystal_size": {
          "estimate": 0.1,
          "lower80": 0.045,
          "upper80": 0.18
        },
        "crystal_yield": {
          "estimate": 0.14,
          "lower80": 0.07,
          "upper80": 0.23
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q10"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.39,
          "lower80": 0.21,
          "upper80": 0.59
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.93,
          "upper80": 1
        },
        "crystal_size": {
          "estimate": 0.17,
          "lower80": 0.09,
          "upper80": 0.26
        },
        "crystal_yield": {
          "estimate": 0.34,
          "lower80": 0.23,
          "upper80": 0.46
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q11"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.64,
          "lower80": 0.43,
          "upper80": 0.83
        },
        "crystal_purity": {
          "estimate": 0.93,
          "lower80": 0.84,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.1,
          "lower80": 0.04,
          "upper80": 0.18
        },
        "crystal_yield": {
          "estimate": 0.5,
          "lower80": 0.38,
          "upper80": 0.62
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q12"
      }
    ],
    "rationale": "Q01\u2013Q02: S1 is expected to outperform S3 through lower nominal solubility, nucleation tendency, and impurity occlusion, giving higher recovery and cleaner, coarser crystals. Q03\u2013Q04: increasing seed from 0.001 to 0.045 g should provide enough controlled growth area to suppress secondary nucleation; the low-seed case is therefore predicted to fail the fines limit. Q05\u2013Q06: a gradual ramp should favor seed growth, whereas the initial rapid plunge to 278.15 K should create a nucleation burst; prolonged holding afterward may increase recovery but cannot fully erase those fines. Q07\u2013Q08: continued low-temperature growth is preferable to reheating to 315 K and rapidly recooling, which likely dissolves small crystals and then generates a fresh fine population. Q09\u2013Q10: both contain seed particles, but immediate isolation at 292 K gives very little seed-excluded recovery; the extra 7200 s permits appreciable growth and modest coarsening. Q11\u2013Q12: doubling reagent concentration should strongly increase recovery, but also supersaturation, impurity loading, and secondary nucleation, making Q12 likely to violate the fines constraint. Intervals are deliberately broad because these recipes use lower concentration, higher reaction temperature, and a quench/reconditioning sequence outside the best-tested campaign region; feasibility booleans use the point estimates, even where an interval crosses a specification boundary."
  },
  "failure": null,
  "elapsed_s": 104.68799999999464,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 1352320,
    "input_tokens": 1533741,
    "output_tokens": 20920,
    "reasoning_output_tokens": 9694
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
    "report": "1. Claim status\n\nSupported by direct observation:\n- Process history dominated fines control. Every quenched campaign batch examined before batch 17 had an unacceptable fines fraction, generally 0.98\u20131.00. Examples include batches 1\u20137, the 50-hold experiment in batch 9, and the mild thermal-cycle experiment in batch 15. By contrast, unquenched, hot-seeded staged cooling gave fines of 0.145 in batch 17 and 0.166 in batch 18; batches 19\u201324 remained at 0.114\u20130.180. This directly supports a strong history effect. The interpretation that quenching creates an early nucleus population is plausible, but was not directly measured.\n- S0 performed best in the quenched solvent comparison. Batch 12 gave recovery 0.494, reaction yield 0.616 and selectivity 0.611, compared with recovery 0.383 for S1 in batch 13 and 0.344 for S3 in batch 14. This is an observation. Attribution to better reaction composition plus crystallization behavior is interpretive because solvent identity changed both stages simultaneously.\n- Catalyst affected the coupled process. Under similar successful staged cooling, C0, C2 and C3 gave recoveries of 0.525, 0.408 and 0.532 in batches 19\u201321. C2 also had the lowest selectivity, 0.492. This supports catalyst-dependent feed quality, although it does not prove that selectivity caused the recovery difference.\n- Cooling to 250 K could raise recovery without violating quality limits. Batch 17 stopped at 270 K and gave recovery 0.502; batch 18 extended to 250 K and gave 0.531. Both met purity and fines requirements.\n\nContradicted or weakened:\n- A simple ranking from nominal solvent properties was contradicted. S0\u2019s nominal high solubility, nucleation tendency and impurity occlusion suggested inferior crystallization, yet it was empirically strongest in batches 12\u201316 and 17\u201324.\n- Seed amount alone was not an effective cure for quenched batches. Tiny, moderate and 0.05 g seed charges in batches 2\u20134 all left fines near 1; omitting seed in batch 7 did not help. This contradicts a seed-dose-only explanation.\n- Long aging or mild thermal ripening did not reliably repair a fine population. Batch 9 used 50 long holds and still had fines 1.00; batch 15\u2019s 280 K cycle also ended at 1.00. Among successful batches, five terminal holds in batch 22 did not outperform one hold in batch 21, and immediate filtration in batch 23 actually produced fewer fines.\n- Unique superiority of C3 is not established. Batch 21 was the highest observed qualifying result, but C1 batch 18 differed in recovery by only about 0.0013, while nominally repeated C3 batches 22\u201324 ranged from 0.508 to 0.520.\n\nStill untested:\n- Whether quenching itself irreversibly creates nuclei, or whether the successful result instead came from hot seeding and inclusion of high-temperature cooling stages.\n- Whether S0\u2019s advantage is primarily a reaction effect, an intrinsic crystallization effect, or an interaction between the two.\n- Whether catalyst-dependent impurities causally alter nucleation rather than merely correlating with recovery.\n- Seed-size distribution, operation below 250 K, classification/washing strategies, and replicated catalyst comparisons were not tested.\n\n2. One additional experiment\n\nI would repeat the recommended batch-21 recipe exactly, but insert a quench after reaction and then reheat sufficiently to the original approximately 345 K state before adding the same 0.05 g seed. I would then use the identical 330-to-250 K staged cooling profile, final hold, filtration and assay.\n\nThis creates the closest available comparison with batch 21 and distinguishes two explanations:\n- Irreversible-quench hypothesis: the quench creates persistent nuclei or microcrystals that survive reheating. Expected result: fines rise substantially, potentially above 0.50, CSD quality and size decline, while purity probably remains high and recovery stays roughly in the 0.45\u20130.53 region.\n- Reversible-state/path hypothesis: reheating fully dissolves the quench-generated population, and the important factors are hot seeding and subsequent gradual cooling. Expected result: fines remain near the batch-21 family, approximately 0.11\u20130.20, with recovery around 0.51\u20130.53 and high purity.\n\nAn intermediate fines result would imply incomplete redissolution and would quantify how much process memory survives the thermal reset. This experiment is more discriminating than another seed-dose or hold-time study because those explanations were already weakened by batches 2\u20139 and 22\u201323.\n\n3. Least effectively used evidence and least reliable prediction\n\nThe observation used least effectively in my held-out predictions was the nearly categorical separation between quenched and unquenched campaign batches. All batches 1\u201316 with quench histories had fines near 1, whereas all successful batches 17\u201324 omitted quench and had fines below 0.20. I allowed several held-out quenched recipes to be feasible because they used lower concentration, reheating/reconditioning near 300 K and extremely slow cooling. That extrapolation is chemically plausible, but the campaign supplied no direct evidence that a 300 K reconditioning step erases the quench history. My feasibility probabilities should therefore be treated as less secure than their numerical presentation suggests.\n\nQ06 is the least reliable held-out prediction. Its approximately 22 K initial cooling jump in 120 seconds is far outside the cooling histories that generated the successful campaign batches and is followed by many nominal crystallization holds at the same temperature. The prediction must extrapolate both burst nucleation and subsequent aging, while campaign evidence showed that aging after fines formation was highly variable and usually ineffective. Its predicted high fines fraction is directionally defensible, but the exact yield, size and fines intervals are weakly calibrated. Q09 is also uncertain because it approaches a seed-only, near-zero seed-excluded-yield boundary, but Q06 combines more severe kinetic and process-history extrapolations."
  },
  "failure": null,
  "elapsed_s": 58.780999999988126,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 1402368,
    "input_tokens": 1598971,
    "output_tokens": 23247,
    "reasoning_output_tokens": 10688
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
    "selected_experiment_index": 21,
    "selection_rationale": "Highest observed seed-excluded crystal recovery (0.5319) among completed batches meeting both crystal purity (0.986) and fines (0.158) constraints; controlled unquenched staged cooling also gave strong CSD quality."
  },
  "recommendation_recipe": {
    "actions": [
      {
        "amount_mol": 0.04,
        "operation": "add_reagent"
      },
      {
        "operation": "add_solvent",
        "solvent": 0,
        "volume_L": 0.075
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
        "target_temperature_K": 345
      },
      {
        "operation": "seed_crystals",
        "seed_mass_g": 0.05
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 330
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 320
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 310
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 300
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 290
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 280
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 270
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 260
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 250
      },
      {
        "duration_s": 14400,
        "operation": "wait",
        "stirring_speed_rpm": 300
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
    "lifecycle_index": 21,
    "source_attempts": 18
  },
  "prediction_evaluation": {
    "contrasts": [
      {
        "absolute_delta_error": 0.0029406234377424567,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_yield",
        "predicted_delta": -0.07,
        "resolved": true,
        "true_delta": -0.07294062343774246
      },
      {
        "absolute_delta_error": 0.028746122547241737,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_purity",
        "predicted_delta": -0.030000000000000027,
        "resolved": false,
        "true_delta": -0.0012538774527582897
      },
      {
        "absolute_delta_error": 0.06565330192830197,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_size",
        "predicted_delta": -0.04999999999999999,
        "resolved": true,
        "true_delta": 0.015653301928301985
      },
      {
        "absolute_delta_error": 0.6232152850558221,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.18,
        "resolved": true,
        "true_delta": -0.44321528505582214
      },
      {
        "absolute_delta_error": 0.06004833748776478,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_yield",
        "predicted_delta": 0.06,
        "resolved": false,
        "true_delta": -4.8337487764782416e-05
      },
      {
        "absolute_delta_error": 0.00186752955473668,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_purity",
        "predicted_delta": 0.010000000000000009,
        "resolved": false,
        "true_delta": 0.008132470445263329
      },
      {
        "absolute_delta_error": 0.06957750439259928,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_size",
        "predicted_delta": 0.07,
        "resolved": false,
        "true_delta": 0.0004224956074007219
      },
      {
        "absolute_delta_error": 0.17517376032701965,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.19999999999999996,
        "resolved": false,
        "true_delta": -0.02482623967298031
      },
      {
        "absolute_delta_error": 0.019767182469520916,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_yield",
        "predicted_delta": 0.019999999999999962,
        "resolved": false,
        "true_delta": 0.00023281753047904585
      },
      {
        "absolute_delta_error": 0.015209363860740788,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.020000000000000018,
        "resolved": false,
        "true_delta": -0.00479063613925923
      },
      {
        "absolute_delta_error": 0.0657945906364231,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_size",
        "predicted_delta": -0.10500000000000001,
        "resolved": true,
        "true_delta": -0.03920540936357691
      },
      {
        "absolute_delta_error": 0.27637716023803627,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.4,
        "resolved": true,
        "true_delta": 0.6763771602380363
      },
      {
        "absolute_delta_error": 0.08156172818020108,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_yield",
        "predicted_delta": -0.03999999999999998,
        "resolved": true,
        "true_delta": 0.041561728180201096
      },
      {
        "absolute_delta_error": 0.010735832934603007,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.020000000000000018,
        "resolved": false,
        "true_delta": -0.009264167065397011
      },
      {
        "absolute_delta_error": 0.06955626788314159,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_size",
        "predicted_delta": -0.09999999999999999,
        "resolved": true,
        "true_delta": -0.030443732116858392
      },
      {
        "absolute_delta_error": 0.3361786076870267,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.36,
        "resolved": true,
        "true_delta": 0.6961786076870267
      },
      {
        "absolute_delta_error": 0.055727677811780355,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_yield",
        "predicted_delta": 0.09500000000000001,
        "resolved": true,
        "true_delta": 0.15072767781178037
      },
      {
        "absolute_delta_error": 0.014073023719337607,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_purity",
        "predicted_delta": 0.0,
        "resolved": true,
        "true_delta": -0.014073023719337607
      },
      {
        "absolute_delta_error": 0.0301242016094624,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_size",
        "predicted_delta": 0.045000000000000005,
        "resolved": true,
        "true_delta": 0.014875798390537605
      },
      {
        "absolute_delta_error": 0.06026443684698085,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.03999999999999998,
        "resolved": false,
        "true_delta": 0.02026443684698087
      },
      {
        "absolute_delta_error": 0.1292597462705805,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_yield",
        "predicted_delta": 0.15999999999999998,
        "resolved": true,
        "true_delta": 0.030740253729419464
      },
      {
        "absolute_delta_error": 0.04397633258618305,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_purity",
        "predicted_delta": -0.04999999999999993,
        "resolved": false,
        "true_delta": -0.00602366741381688
      },
      {
        "absolute_delta_error": 0.042436293373212815,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_size",
        "predicted_delta": -0.07,
        "resolved": true,
        "true_delta": -0.027563706626787192
      },
      {
        "absolute_delta_error": 0.4385789828624289,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.25,
        "resolved": true,
        "true_delta": 0.6885789828624289
      }
    ],
    "failures": [],
    "metrics": {
      "crystal_fines_fraction": {
        "coverage80": 0.4166666666666667,
        "interval_score80": 1.7380903747728187,
        "interval_width": 0.38083333333333336,
        "mae": 0.2798564737457881,
        "n": 12,
        "planned": 12
      },
      "crystal_purity": {
        "coverage80": 1.0,
        "interval_score80": 0.08749999999999998,
        "interval_width": 0.08749999999999998,
        "mae": 0.01495183626485703,
        "n": 12,
        "planned": 12
      },
      "crystal_size": {
        "coverage80": 0.6666666666666666,
        "interval_score80": 0.19321243854839446,
        "interval_width": 0.14708333333333334,
        "mae": 0.05557790746092561,
        "n": 12,
        "planned": 12
      },
      "crystal_yield": {
        "coverage80": 0.8333333333333334,
        "interval_score80": 0.27343394759371076,
        "interval_width": 0.21833333333333335,
        "mae": 0.055185648898563595,
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
        "crystal_fines_fraction": 0.31402314041245477,
        "crystal_purity": 0.00467010485113976,
        "crystal_size": 0.01754278915004831,
        "crystal_yield": 0.20584980019837118
      },
      "public_nearest_neighbor": {
        "crystal_fines_fraction": 0.344487301553374,
        "crystal_purity": 0.013796922356283806,
        "crystal_size": 0.060222292570996976,
        "crystal_yield": 0.2575668170443128
      }
    },
    "training_batches": 24
  },
  "tokens": {
    "basis": "cumulative thread snapshots differenced in source/K1/Q/K2 order",
    "complete": true,
    "monetary_cost_usd": null,
    "stages": [
      {
        "cached_input": 1303680,
        "input": 1374176,
        "output": 13114,
        "stage": "source",
        "uncached_input": 70496
      },
      {
        "cached_input": 48640,
        "input": 99065,
        "output": 2996,
        "stage": "K1",
        "uncached_input": 50425
      },
      {
        "cached_input": 0,
        "input": 60500,
        "output": 4810,
        "stage": "Q",
        "uncached_input": 60500
      },
      {
        "cached_input": 50048,
        "input": 65230,
        "output": 2327,
        "stage": "K2",
        "uncached_input": 15182
      }
    ],
    "total": {
      "cached_input": 1402368,
      "input": 1598971,
      "input_plus_output": 1622218,
      "output": 23247,
      "uncached_input": 196603
    },
    "valid": true
  },
  "elapsed_s": 829.2190000000119
}
```
