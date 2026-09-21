# C-W03-B24-E-MisIndexed

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
  "end_step": 12,
  "lifecycle_index": 1,
  "metrics": {
    "byproduct_signal": 0.33314529061317444,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.49266156554222107,
    "crystal_fines_fraction": 0.997306764125824,
    "crystal_purity": 0.9827007055282593,
    "crystal_size": 0.060059837996959686,
    "crystal_yield": 0.4390811026096344,
    "degradation_warning": 0.16801783442497253,
    "safety_risk": 0.18087826669216156,
    "score": 0.38745641708374023,
    "selectivity": 0.5355391502380371,
    "virtual_spectrum_summary": 0.2588379383087158,
    "yield": 0.5333766341209412
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 340
    },
    {
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.005
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 285
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
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
  "end_step": 27,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.4251951277256012,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5037093162536621,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9776714444160461,
    "crystal_size": 0.08681293576955795,
    "crystal_yield": 0.3598504364490509,
    "degradation_warning": 0.22582779824733734,
    "safety_risk": 0.16876953840255737,
    "score": 0.35072553157806396,
    "selectivity": 0.4281823933124542,
    "virtual_spectrum_summary": 0.33547982573509216,
    "yield": 0.4167374074459076
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
      "catalyst": 2,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 500,
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
      "target_temperature_K": 285
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 290
    },
    {
      "duration_s": 7200,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
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
  "end_step": 44,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.43660542368888855,
    "conversion": 0.9983179569244385,
    "cost": 1.0,
    "crystal_csd_quality": 0.5303604602813721,
    "crystal_fines_fraction": 0.9949293732643127,
    "crystal_purity": 0.9861199259757996,
    "crystal_size": 0.043344222009181976,
    "crystal_yield": 0.2841762602329254,
    "degradation_warning": 0.1855655461549759,
    "safety_risk": 0.15898068249225616,
    "score": 0.3207193911075592,
    "selectivity": 0.3420107364654541,
    "virtual_spectrum_summary": 0.3236374855041504,
    "yield": 0.34112346172332764
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
      "solvent": 3,
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
      "stirring_speed_rpm": 400,
      "target_temperature_K": 340
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
      "target_temperature_K": 300
    },
    {
      "duration_s": 7200,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 285
    },
    {
      "duration_s": 7200,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 7200,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
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
  "end_step": 62,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.5350819230079651,
    "conversion": 0.9889965057373047,
    "cost": 1.0,
    "crystal_csd_quality": 0.46380266547203064,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 1.0,
    "crystal_size": 0.06712351739406586,
    "crystal_yield": 0.22068855166435242,
    "degradation_warning": 0.29909536242485046,
    "safety_risk": 0.16393782198429108,
    "score": 0.2859353721141815,
    "selectivity": 0.2987480163574219,
    "virtual_spectrum_summary": 0.4288879930973053,
    "yield": 0.28511834144592285
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 340
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
      "target_temperature_K": 300
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
  "end_step": 74,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.4407261610031128,
    "conversion": 0.996337890625,
    "cost": 1.0,
    "crystal_csd_quality": 1.0,
    "crystal_fines_fraction": 0.01108784880489111,
    "crystal_purity": 0.9900436997413635,
    "crystal_size": 0.3753965198993683,
    "crystal_yield": 0.0,
    "degradation_warning": 0.2366151213645935,
    "safety_risk": 0.14071060717105865,
    "score": 0.49690061807632446,
    "selectivity": 0.45128583908081055,
    "virtual_spectrum_summary": 0.3488762080669403,
    "yield": 0.44513288140296936
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 340
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
  "end_step": 86,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.43820106983184814,
    "conversion": 0.9924335479736328,
    "cost": 1.0,
    "crystal_csd_quality": 0.4893966317176819,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.991421103477478,
    "crystal_size": 0.01733691245317459,
    "crystal_yield": 0.29472729563713074,
    "degradation_warning": 0.24115101993083954,
    "safety_risk": 0.16465574502944946,
    "score": 0.32970210909843445,
    "selectivity": 0.4312933683395386,
    "virtual_spectrum_summary": 0.34952855110168457,
    "yield": 0.43317899107933044
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 340
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
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 600,
      "operation": "cool_crystallize",
      "target_temperature_K": 295
    },
    {
      "duration_s": 1800,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 298
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
  "end_step": 102,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.42821764945983887,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.45202675461769104,
    "crystal_fines_fraction": 0.9866795539855957,
    "crystal_purity": 0.975277841091156,
    "crystal_size": 0.06394025683403015,
    "crystal_yield": 0.2915956676006317,
    "degradation_warning": 0.2341231256723404,
    "safety_risk": 0.1640125811100006,
    "score": 0.32403793931007385,
    "selectivity": 0.41265028715133667,
    "virtual_spectrum_summary": 0.34087511897087097,
    "yield": 0.43929749727249146
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 340
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
      "target_temperature_K": 300
    },
    {
      "duration_s": 7200,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 290
    },
    {
      "duration_s": 7200,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 280
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
  "end_step": 118,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.4047388732433319,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5358296036720276,
    "crystal_fines_fraction": 0.9868560433387756,
    "crystal_purity": 0.9757205843925476,
    "crystal_size": 0.07545057684183121,
    "crystal_yield": 0.3333260118961334,
    "degradation_warning": 0.20822058618068695,
    "safety_risk": 0.14748252928256989,
    "score": 0.35334041714668274,
    "selectivity": 0.4351746141910553,
    "virtual_spectrum_summary": 0.31630563735961914,
    "yield": 0.42686936259269714
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 340
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
  "end_step": 137,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.4309771656990051,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5101260542869568,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9730604887008667,
    "crystal_size": 0.023217331618070602,
    "crystal_yield": 0.29658499360084534,
    "degradation_warning": 0.23329460620880127,
    "safety_risk": 0.16465574502944946,
    "score": 0.33116114139556885,
    "selectivity": 0.422065794467926,
    "virtual_spectrum_summary": 0.3420200049877167,
    "yield": 0.43574172258377075
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 340
    },
    {
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 295
    },
    {
      "duration_s": 7200,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 305
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
  "end_step": 150,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.423854261636734,
    "conversion": 0.9858242273330688,
    "cost": 1.0,
    "crystal_csd_quality": 0.5000929236412048,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9677831530570984,
    "crystal_size": 0.035322967916727066,
    "crystal_yield": 0.2640399932861328,
    "degradation_warning": 0.24470095336437225,
    "safety_risk": 0.16211698949337006,
    "score": 0.3193393647670746,
    "selectivity": 0.4164944887161255,
    "virtual_spectrum_summary": 0.3432352840900421,
    "yield": 0.4254212975502014
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 340
    },
    {
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 295
    },
    {
      "duration_s": 7200,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 315
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
  "end_step": 163,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.4323688745498657,
    "conversion": 0.9990203976631165,
    "cost": 1.0,
    "crystal_csd_quality": 0.5173889398574829,
    "crystal_fines_fraction": 0.9936640858650208,
    "crystal_purity": 0.9828189015388489,
    "crystal_size": 0.03798487409949303,
    "crystal_yield": 0.21417853236198425,
    "degradation_warning": 0.22172097861766815,
    "safety_risk": 0.15944144129753113,
    "score": 0.31439095735549927,
    "selectivity": 0.4335919916629791,
    "virtual_spectrum_summary": 0.33757731318473816,
    "yield": 0.41410213708877563
  },
  "ordinal": 11
}
```

## Batch 12

```json
{
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.0025,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 340
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
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 285
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
  "end_step": 177,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.412248820066452,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.4527305066585541,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9957852363586426,
    "crystal_size": 0.08845705538988113,
    "crystal_yield": 0.3123106360435486,
    "degradation_warning": 0.24185392260551453,
    "safety_risk": 0.11992353200912476,
    "score": 0.3444662392139435,
    "selectivity": 0.46509191393852234,
    "virtual_spectrum_summary": 0.3355711102485657,
    "yield": 0.4701337218284607
  },
  "ordinal": 12
}
```

## Batch 13

```json
{
  "actions": [
    {
      "amount_mol": 0.005,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.000625,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 340
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
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
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
  "end_step": 191,
  "lifecycle_index": 13,
  "metrics": {
    "byproduct_signal": 0.3941349685192108,
    "conversion": 0.9719383120536804,
    "cost": 1.0,
    "crystal_csd_quality": 0.34423479437828064,
    "crystal_fines_fraction": 0.9784001111984253,
    "crystal_purity": 0.9868173599243164,
    "crystal_size": 0.0592431016266346,
    "crystal_yield": 0.2208402156829834,
    "degradation_warning": 0.19318422675132751,
    "safety_risk": 0.08432967960834503,
    "score": 0.3283870220184326,
    "selectivity": 0.6419602036476135,
    "virtual_spectrum_summary": 0.30370715260505676,
    "yield": 0.6178550124168396
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 340
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
      "target_temperature_K": 300
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
  "end_step": 203,
  "lifecycle_index": 14,
  "metrics": {
    "byproduct_signal": 0.4823850691318512,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 1.0,
    "crystal_fines_fraction": 0.018301552161574364,
    "crystal_purity": 0.976832926273346,
    "crystal_size": 0.43057796359062195,
    "crystal_yield": 0.0,
    "degradation_warning": 0.23467044532299042,
    "safety_risk": 0.15003302693367004,
    "score": 0.47679829597473145,
    "selectivity": 0.33522433042526245,
    "virtual_spectrum_summary": 0.3709135055541992,
    "yield": 0.3290368616580963
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
      "solvent": 3,
      "volume_L": 0.08
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 340
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
  "end_step": 215,
  "lifecycle_index": 15,
  "metrics": {
    "byproduct_signal": 0.4757915735244751,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.43614983558654785,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.978415310382843,
    "crystal_size": 0.05941459536552429,
    "crystal_yield": 0.12361492216587067,
    "degradation_warning": 0.2275179624557495,
    "safety_risk": 0.16035999357700348,
    "score": 0.260284960269928,
    "selectivity": 0.33323967456817627,
    "virtual_spectrum_summary": 0.3640684485435486,
    "yield": 0.33777421712875366
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
      "solvent": 3,
      "volume_L": 0.08
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 340
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
      "target_temperature_K": 298
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
  "end_step": 227,
  "lifecycle_index": 16,
  "metrics": {
    "byproduct_signal": 0.4688704311847687,
    "conversion": 0.9885537624359131,
    "cost": 1.0,
    "crystal_csd_quality": 0.4124683439731598,
    "crystal_fines_fraction": 0.987494707107544,
    "crystal_purity": 0.9684877395629883,
    "crystal_size": 0.051666513085365295,
    "crystal_yield": 0.1086699366569519,
    "degradation_warning": 0.2388422191143036,
    "safety_risk": 0.15939511358737946,
    "score": 0.24877023696899414,
    "selectivity": 0.33039137721061707,
    "virtual_spectrum_summary": 0.36535772681236267,
    "yield": 0.32874596118927
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
      "solvent": 3,
      "volume_L": 0.08
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 340
    },
    {
      "operation": "quench"
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 298
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
  "end_step": 238,
  "lifecycle_index": 17,
  "metrics": {
    "byproduct_signal": 0.48407140374183655,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.4774453341960907,
    "crystal_fines_fraction": 0.9720399379730225,
    "crystal_purity": 0.9864258766174316,
    "crystal_size": 0.04118245095014572,
    "crystal_yield": 0.1215796247124672,
    "degradation_warning": 0.23356090486049652,
    "safety_risk": 0.15909038484096527,
    "score": 0.2663678526878357,
    "selectivity": 0.30644163489341736,
    "virtual_spectrum_summary": 0.37134167551994324,
    "yield": 0.31659990549087524
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
      "solvent": 3,
      "volume_L": 0.08
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 340
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
      "target_temperature_K": 298
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 1200
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 1200
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 1200
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 1200
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 1200
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 1200
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 1200
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 1200
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
  "end_step": 257,
  "lifecycle_index": 18,
  "metrics": {
    "byproduct_signal": 0.457711398601532,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.46063587069511414,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9856934547424316,
    "crystal_size": 0.09221764653921127,
    "crystal_yield": 0.11081639677286148,
    "degradation_warning": 0.22941544651985168,
    "safety_risk": 0.15939511358737946,
    "score": 0.2677537798881531,
    "selectivity": 0.33252474665641785,
    "virtual_spectrum_summary": 0.3549782335758209,
    "yield": 0.3459317088127136
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
      "volume_L": 0.08
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 340
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
      "target_temperature_K": 300
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
  "lifecycle_index": 19,
  "metrics": {
    "byproduct_signal": 0.35586312413215637,
    "conversion": 0.9909035563468933,
    "cost": 1.0,
    "crystal_csd_quality": 0.48764145374298096,
    "crystal_fines_fraction": 0.9773752093315125,
    "crystal_purity": 0.965092658996582,
    "crystal_size": 0.03348575904965401,
    "crystal_yield": 0.28541502356529236,
    "degradation_warning": 0.12790928781032562,
    "safety_risk": 0.12265192717313766,
    "score": 0.3350205719470978,
    "selectivity": 0.4664199948310852,
    "virtual_spectrum_summary": 0.25328388810157776,
    "yield": 0.4700067639350891
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
      "solvent": 3,
      "volume_L": 0.08
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 340
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
      "target_temperature_K": 305
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 298
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
  "end_step": 286,
  "lifecycle_index": 20,
  "metrics": {
    "byproduct_signal": 0.5754839777946472,
    "conversion": 0.9934656023979187,
    "cost": 1.0,
    "crystal_csd_quality": 0.5335900187492371,
    "crystal_fines_fraction": 0.7022149562835693,
    "crystal_purity": 0.9858921766281128,
    "crystal_size": 0.06671229749917984,
    "crystal_yield": 0.11058550328016281,
    "degradation_warning": 0.31404128670692444,
    "safety_risk": 0.15717573463916779,
    "score": 0.2918030619621277,
    "selectivity": 0.25780045986175537,
    "virtual_spectrum_summary": 0.45783478021621704,
    "yield": 0.24147865176200867
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
      "solvent": 3,
      "volume_L": 0.08
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 340
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 325
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 315
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 307
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 304
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 302
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 299
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 298
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
    }
  ],
  "end_step": 310,
  "lifecycle_index": 21,
  "metrics": {
    "byproduct_signal": 0.6739827394485474,
    "conversion": 0.9894089102745056,
    "cost": 1.0,
    "crystal_csd_quality": 0.6634871363639832,
    "crystal_fines_fraction": 0.4949876666069031,
    "crystal_purity": 0.9834369421005249,
    "crystal_size": 0.05674905702471733,
    "crystal_yield": 0.12331599742174149,
    "degradation_warning": 0.4019011855125427,
    "safety_risk": 0.15488502383232117,
    "score": 0.3244760036468506,
    "selectivity": 0.14998136460781097,
    "virtual_spectrum_summary": 0.551546037197113,
    "yield": 0.16925859451293945
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
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 340
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 325
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 315
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 307
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 304
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 302
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 299
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 298
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
    }
  ],
  "end_step": 334,
  "lifecycle_index": 22,
  "metrics": {
    "byproduct_signal": 0.5831118226051331,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7922179698944092,
    "crystal_fines_fraction": 0.22369711101055145,
    "crystal_purity": 1.0,
    "crystal_size": 0.08630895614624023,
    "crystal_yield": 0.2745952308177948,
    "degradation_warning": 0.3422287404537201,
    "safety_risk": 0.16124066710472107,
    "score": 0.45042744278907776,
    "selectivity": 0.31728824973106384,
    "virtual_spectrum_summary": 0.474714457988739,
    "yield": 0.3185671269893646
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
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 340
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 325
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 315
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 307
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 304
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 302
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 299
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 298
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 297
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 296
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
  "end_step": 361,
  "lifecycle_index": 23,
  "metrics": {
    "byproduct_signal": 0.5720372200012207,
    "conversion": 0.9950222373008728,
    "cost": 1.0,
    "crystal_csd_quality": 0.8099828362464905,
    "crystal_fines_fraction": 0.19115081429481506,
    "crystal_purity": 0.9986124634742737,
    "crystal_size": 0.10901390761137009,
    "crystal_yield": 0.2786077558994293,
    "degradation_warning": 0.3268730044364929,
    "safety_risk": 0.1623058170080185,
    "score": 0.46494796872138977,
    "selectivity": 0.3431437015533447,
    "virtual_spectrum_summary": 0.46171334385871887,
    "yield": 0.3449019491672516
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
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 340
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 325
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 315
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 312
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 308
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 306
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 304
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 302
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 301
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 299
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 298
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 297
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 296
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 295
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 294
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 293
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 292
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 291
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 290
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 289
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 288
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 287
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 286
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
    }
  ],
  "end_step": 401,
  "lifecycle_index": 24,
  "metrics": {
    "byproduct_signal": 0.5468053221702576,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.8227990865707397,
    "crystal_fines_fraction": 0.17406506836414337,
    "crystal_purity": 1.0,
    "crystal_size": 0.08928339183330536,
    "crystal_yield": 0.3004259169101715,
    "degradation_warning": 0.3046257197856903,
    "safety_risk": 0.16542598605155945,
    "score": 0.47729259729385376,
    "selectivity": 0.36153262853622437,
    "virtual_spectrum_summary": 0.4378244876861572,
    "yield": 0.3707824945449829
  },
  "ordinal": 24
}
```

## K1

```json
{
  "payload": {
    "report": "Mechanistic account\n\nRecommended process (unchanged): Batch 24. It used 0.040 mol reagent, 0.080 L solvent-S2, 0.005 mol catalyst-C1, reaction at 340 K for 7200 s with 400 rpm stirring, followed by an unquenched staged crystallization. The mixture was cooled first to 330 K, seeded with 0.050 g, then cooled through many 14,400 s stages from 325 to 285 K, followed by four 14,400 s holds at 100 rpm before filtration. Its final assay gave seed-excluded crystal recovery 0.3004, purity 1.000, fines fraction 0.1741, normalized crystal size 0.0893, and CSD quality 0.8228.\n\nObservations\n\n1. Recovery and particle quality were strongly history-dependent. A rapid, deep cool produced substantial recovery but almost exclusively fine particles: Batch 1, quenched and cooled to 270 K, gave recovery 0.4391 but fines 0.9973. Batch 6, cooled directly to 295 K, gave recovery 0.2947 and fines 1.000. Merely extending an isothermal hold did not solve this: Batch 9 remained at recovery 0.2966 and fines 1.000.\n\n2. Very mild crystallization could generate large, clean particles without recovering new product. Batch 5 (S2, seeded at 0.050 g, cooled to 300 K) had normalized size 0.3754, CSD quality 1.000, fines 0.0111, and purity 0.9900, but seed-excluded recovery was zero. Batch 14 showed the same phenomenon with S3: size 0.4306 and fines 0.0183, but zero seed-excluded recovery. These results are important because the assay excludes the seed mass: excellent particle measurements can describe surviving or grown seeds while net recovery of target product remains negligible.\n\n3. Gradual cooling reconciled recovery and fines. Batch 20 used a shorter staged, unquenched S3 trajectory and reached recovery 0.1106 with fines 0.7022. Batch 21 used a much finer cooling schedule and reached recovery 0.1233 with fines 0.4950, just satisfying the fines limit. Transferring that history to S2 produced a large improvement: Batch 22 gave recovery 0.2746 and fines 0.2237. Extending the S2 ramp further gave Batch 23 recovery 0.2786 and fines 0.1912, and Batch 24 recovery 0.3004 and fines 0.1741. Thus the improvement was systematic across the final three experiments, not inferred from score alone.\n\n4. Purity was comparatively insensitive once crystals were recovered. Representative final purities were 0.9827 in Batch 1, 0.9914 in Batch 6, 1.000 in Batch 22, 0.9986 in Batch 23, and 1.000 in Batch 24. Even poorer particle-size experiments generally exceeded 0.96. Purity therefore was not the active constraint in this campaign; fines were.\n\nMaterial effects\n\nSolvent-S2 was the best demonstrated compromise. Its nominal dossier suggested low relative solubility, low nucleation tendency, high growth propensity, and low impurity occlusion. The comparison between the similarly staged final experiments supports that prior: S3 in Batch 21 produced recovery 0.1233 and fines 0.4950, whereas S2 in Batch 22 produced recovery 0.2746 and fines 0.2237. This is consistent with S2 providing both a stronger crystallization driving force and more growth-dominated use of supersaturation. It is not a clean one-factor comparison because the histories were not perfectly identical, so a hidden solvent-specific reaction effect remains possible.\n\nS0 and S1 did not solve the fines problem under the tested direct-cooling schedules. Batch 19 with S0 gave recovery 0.2854 but fines 0.9774; Batch 8 with S1 gave recovery 0.3333 but fines 0.9869. These results do not prove those solvents would fail under Batch 24\u2019s detailed ramp, which was not tested.\n\nCatalyst-C1 was retained after screening because it supported full or near-full conversion and the strongest overall development path. Catalyst comparisons were confounded: Batch 2 with C0 gave recovery 0.3599 and fines 1.000; Batch 3 with C2 gave 0.2842 and 0.9949; the C3 experiment, Batch 4, also changed solvent and gave 0.2207 and 1.000. Consequently, the data establish C1 as the best validated catalyst in the optimized workflow, not necessarily the intrinsic optimum among all catalysts.\n\nReaction\u2013crystallization coupling\n\nThe reaction usually reached near-complete conversion, but selectivity varied materially with solvent and prolonged thermal history. Batch 1\u2019s reaction HPLC showed conversion 1.000, yield about 0.538, selectivity about 0.544, and byproduct signal about 0.333. In the final long-ramp S2 experiments, conversion remained approximately 1.0, while final selectivity was lower: 0.317 in Batch 22, 0.343 in Batch 23, and 0.362 in Batch 24. Their degradation warnings and byproduct signals were also elevated. This suggests that the long warm-to-moderate-temperature residence needed for controlled crystal growth allows continuing side reaction or degradation.\n\nA useful conceptual decomposition is:\n\ncrystallization recovery = recovered target product excluding seed / target product present immediately before separation.\n\nOverall isolated target from reagent would instead scale approximately as:\n\nY_overall \u2248 Y_reaction \u00d7 R_crystallization,\n\nwhere Y_reaction includes conversion and selectivity. Maximizing the reported crystallization recovery alone can therefore tolerate deterioration of the upstream product pool. Batch 24 met the stated objective, but its long cycle may not maximize overall isolated product from the original reagent.\n\nThe crystallization behavior can be described with supersaturation S = C/C*(T,solvent). Nucleation rate J commonly rises much more steeply with supersaturation than growth rate G. A rapid quench creates a large supersaturation spike, so the integrated number of nuclei, N \u221d \u222bJ(S,T)dt, becomes large and available solute is divided among many fine particles. A slow ramp limits the peak supersaturation while allowing cumulative growth, approximately \u0394L \u221d \u222bG(S,T)dt. This accounts for the contrast between Batch 1 and Batches 22\u201324. The pre-seed move to 330 K in the final workflow may also have positioned the solution near metastable supersaturation before seeds were introduced, letting the seeds consume supersaturation before uncontrolled nucleation accelerated.\n\nProcess-history dependence and revisions\n\nThe early working assumption was that deep cooling and long aging would increase recovery. Batches 1\u20134 supported the recovery side but revealed catastrophic fines. The next revision emphasized high seed loading and mild cooling. Batches 5 and 14 showed that this could produce excellent apparent particles but no seed-excluded recovery, exposing a false optimum caused by measuring seeds rather than newly recovered product. Moving only slightly below 300 K caused an abrupt return of nucleation and fines in Batches 6, 7, 9, 15, and 16, suggesting a narrow metastable-zone boundary rather than a smooth response.\n\nAnnealing, prolonged holds, and high agitation were then explored. Long holding in Batch 9, heating/annealing in Batches 10\u201311, and aggressive stirring in Batch 18 did not appreciably reduce fines. The successful revision was not simply \u2018more time\u2019 but distributing the temperature change across many small stages before reaching lower temperature. Batches 20\u201324 demonstrate that path dependence directly. Extending the lower end of the S2 ramp from about 298 K in Batch 22 to 295 K in Batch 23 and finally 285 K in Batch 24 increased recovery while maintaining or improving the fines fraction.\n\nUncertainty and unresolved tradeoffs\n\nFinal-assay noise is small relative to the main contrasts (nominal standard deviations about 0.010 for recovery and purity and 0.018 for fines), but no optimized batch was replicated, so batch-to-batch process variability is unresolved. The apparent monotonic improvement from Batches 22\u201324 is encouraging, yet it combines endpoint, number of cooling stages, and residence time. Their separate causal contributions were not isolated.\n\nThe normalized size in Batch 24 corresponds to a number-weighted d50 of roughly 22 micrometres, only modestly above the 20 micrometre fines threshold, despite a measured fines fraction of 0.174. Batch 23 had a somewhat larger normalized size but slightly lower recovery. These differences may partly reflect measurement noise or distribution shape.\n\nA real quality/recovery tradeoff remains. The highest observed recovery, Batch 1 at 0.4391, failed the fines constraint severely. Batch 24 sacrificed some recovery to obtain compliant particles. Conversely, the best-looking particle populations in Batches 5 and 14 had no seed-excluded recovery. Further extension below 285 K might raise recovery, but could trigger secondary nucleation and increase fines; longer warm residence might improve growth but further damage reaction selectivity. Neither alternative was tested.\n\nOther untested alternatives include applying Batch 24\u2019s exact ramp to S0 or S1, changing seed size distribution rather than seed mass, varying agitation during each individual cooling segment, shortening the initial reaction once conversion is complete, and decoupling reaction and crystallization residence through an earlier transfer or quench. These are plausible improvement routes, not conclusions supported by the present campaign."
  },
  "failure": null,
  "elapsed_s": 65.125,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 1414656,
    "input_tokens": 1518283,
    "output_tokens": 16710,
    "reasoning_output_tokens": 5044
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
          "lower80": 0.12,
          "upper80": 0.48
        },
        "crystal_purity": {
          "estimate": 0.97,
          "lower80": 0.92,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.14,
          "lower80": 0.07,
          "upper80": 0.25
        },
        "crystal_yield": {
          "estimate": 0.27,
          "lower80": 0.14,
          "upper80": 0.41
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q01"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.18,
          "lower80": 0.06,
          "upper80": 0.36
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.93,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.17,
          "lower80": 0.09,
          "upper80": 0.29
        },
        "crystal_yield": {
          "estimate": 0.35,
          "lower80": 0.2,
          "upper80": 0.51
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q02"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.76,
          "lower80": 0.52,
          "upper80": 0.94
        },
        "crystal_purity": {
          "estimate": 0.97,
          "lower80": 0.91,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.055,
          "lower80": 0.02,
          "upper80": 0.12
        },
        "crystal_yield": {
          "estimate": 0.21,
          "lower80": 0.09,
          "upper80": 0.36
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q03"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.39,
          "lower80": 0.19,
          "upper80": 0.62
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.93,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.12,
          "lower80": 0.055,
          "upper80": 0.22
        },
        "crystal_yield": {
          "estimate": 0.25,
          "lower80": 0.12,
          "upper80": 0.4
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q04"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.4,
          "lower80": 0.2,
          "upper80": 0.63
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.93,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.115,
          "lower80": 0.05,
          "upper80": 0.21
        },
        "crystal_yield": {
          "estimate": 0.25,
          "lower80": 0.12,
          "upper80": 0.4
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q05"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.91,
          "lower80": 0.73,
          "upper80": 1.0
        },
        "crystal_purity": {
          "estimate": 0.97,
          "lower80": 0.91,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.04,
          "lower80": 0.012,
          "upper80": 0.09
        },
        "crystal_yield": {
          "estimate": 0.32,
          "lower80": 0.17,
          "upper80": 0.48
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q06"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.43,
          "lower80": 0.22,
          "upper80": 0.66
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.93,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.105,
          "lower80": 0.045,
          "upper80": 0.2
        },
        "crystal_yield": {
          "estimate": 0.26,
          "lower80": 0.13,
          "upper80": 0.41
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q07"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.61,
          "lower80": 0.36,
          "upper80": 0.84
        },
        "crystal_purity": {
          "estimate": 0.97,
          "lower80": 0.91,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.075,
          "lower80": 0.028,
          "upper80": 0.16
        },
        "crystal_yield": {
          "estimate": 0.19,
          "lower80": 0.07,
          "upper80": 0.34
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q08"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.04,
          "lower80": 0.0,
          "upper80": 0.16
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.92,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.32,
          "lower80": 0.17,
          "upper80": 0.49
        },
        "crystal_yield": {
          "estimate": 0.004,
          "lower80": 0.0,
          "upper80": 0.025
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q09"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.12,
          "lower80": 0.02,
          "upper80": 0.32
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.92,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.25,
          "lower80": 0.12,
          "upper80": 0.42
        },
        "crystal_yield": {
          "estimate": 0.055,
          "lower80": 0.01,
          "upper80": 0.14
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q10"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.38,
          "lower80": 0.18,
          "upper80": 0.61
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.93,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.12,
          "lower80": 0.055,
          "upper80": 0.22
        },
        "crystal_yield": {
          "estimate": 0.25,
          "lower80": 0.12,
          "upper80": 0.4
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q11"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.67,
          "lower80": 0.43,
          "upper80": 0.88
        },
        "crystal_purity": {
          "estimate": 0.97,
          "lower80": 0.91,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.07,
          "lower80": 0.027,
          "upper80": 0.15
        },
        "crystal_yield": {
          "estimate": 0.41,
          "lower80": 0.25,
          "upper80": 0.57
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q12"
      }
    ],
    "rationale": "All recipes contain seed, so particles are expected even when seed-excluded recovery is nearly zero. Q01\u2013Q02: S3 is predicted to give greater recovery and fewer fines than S1 because of its lower nominal solubility and nucleation tendency. Q03\u2013Q04: raising seed mass should provide much more growth area and suppress secondary nucleation, improving size and fines with only a modest recovery change. Q05\u2013Q06: the gradual ramp should limit peak supersaturation; the equal-duration temperature crash should recover somewhat more product but generate predominantly fines. Q07\u2013Q08: the extra cold hold should preserve the controlled population, whereas reheating to 315 K likely dissolves product and the rapid recool partly renucleates it. Q09\u2013Q10: after only 60 seconds, measured particles should be mostly seed and seed-excluded recovery almost zero; a two-hour hold permits limited growth. Q11\u2013Q12: doubling reagent concentration should increase thermodynamic recovery but also supersaturation and secondary nucleation, likely violating the fines limit. Purity is predicted to remain above 0.80 throughout, as in the campaign. Intervals are deliberately broad because these recipes use lower charge, higher reaction temperature, S0/S1 conditions, and cooling histories not closely replicated in the sealed experiments; process-model uncertainty is much larger than final-assay noise."
  },
  "failure": null,
  "elapsed_s": 54.139999999984866,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 1414656,
    "input_tokens": 1575709,
    "output_tokens": 19448,
    "reasoning_output_tokens": 6078
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
    "report": "1. Status of the main claims\n\nSupported by direct observations:\n- Process history controls the recovery\u2013fines balance. Rapid/deep cooling gave high recovery with unacceptable fines: Batch 1 had crystal yield 0.4391 and fines 0.9973. Direct cooling in Batch 6 similarly gave yield 0.2947 and fines 1.000. In contrast, increasingly fine staged cooling in Batches 22\u201324 gave yields of 0.2746, 0.2786 and 0.3004 while fines fell to 0.2237, 0.1912 and 0.1741. Interpreting this as suppression of a supersaturation-driven nucleation burst is mechanistic inference, but the history dependence itself is directly observed.\n- Excellent particle measurements do not imply seed-excluded recovery. Batch 5 had CSD quality 1.000, fines 0.0111 and normalized size 0.3754, but zero crystal yield. Batch 14 reproduced the pattern with fines 0.0183, size 0.4306 and zero yield. The direct conclusion is that the recovered particles can largely represent seed; the proposed explanation of seed growth below the threshold for appreciable new-product crystallization is interpretive.\n- Long residence alone was insufficient. Batch 9 remained at fines 1.000 after extensive holding, while Batch 18 combined long residence with high agitation and still had fines 1.000. This contradicts a simple \u201cmore aging produces coarser crystals\u201d rule and supports the importance of the temperature path.\n- Purity was not the active constraint. Relevant batches consistently exceeded 0.96 purity, including Batches 1, 6 and 22\u201324. Fines, not purity, separated feasible from infeasible processes.\n- Solvent-S2 was the strongest demonstrated material in the optimized history. Batch 21 using S3 gave yield 0.1233 and fines 0.4950; the related S2 trajectories in Batches 22\u201324 gave much higher recovery and lower fines. The numerical advantage is observed, although attributing it specifically to solubility, growth and nucleation properties is not fully identified because the schedules were not identical.\n\nContradicted or revised claims:\n- The early assumption that deeper cooling and longer aging would jointly maximize useful recovery was contradicted by Batches 1, 6 and 9: recovery increased, but nearly all particles were fines.\n- The idea that high seed loading alone would deliver both quality and recovery was contradicted by Batches 5 and 14. It delivered excellent apparent particle quality but no seed-excluded recovery.\n- A simple monotonic temperature response was contradicted by the sharp contrast around 295\u2013300 K: Batch 5 at 300 K had zero yield and very few fines, whereas Batch 6 at 295 K had substantial yield and essentially all fines. This suggests a threshold or metastable-zone transition rather than a smooth response.\n- Annealing or vigorous agitation as general remedies for fines was not supported: Batches 10\u201311 and 18 remained fine-rich.\n\nStill untested or only partially supported:\n- Catalyst-C1 was the best validated catalyst in the developed workflow, but intrinsic catalyst ranking remains untested because Batches 2\u20134 changed other conditions.\n- S0 or S1 under the exact Batch 24 cooling schedule was never tested. Their poor fines results in Batches 8 and 19 used less controlled cooling histories.\n- The claim that prolonged warm residence caused the lower selectivity and larger degradation signals in Batches 20\u201324 is plausible but not causal evidence. Reaction continued during crystallization, and temperature, solvent and total time changed together.\n- The separate effects of cooling-step size, total residence time and final temperature were not identified. All three changed across Batches 22\u201324.\n- Seed size distribution, seed surface area, stage-specific agitation, and the benefit of stopping the reaction earlier remain untested.\n\n2. One additional experiment\n\nI would repeat Batch 24\u2019s composition, reaction, seed mass, final temperature and total crystallization time, but replace its many small cooling steps with a matched-duration history that holds near 298 K for most of the cycle and then cools rapidly to 285 K near the end. I would include non-destructive particle-size measurements immediately before and after the final drop, then filter and assay normally.\n\nThis would distinguish two principal explanations:\n- Supersaturation-management explanation: Batch 24 succeeded because small temperature increments let seeded growth consume supersaturation before the next increment. The matched hold/late-drop experiment should then show a sharp increase in fines after the final drop, a smaller size or poorer CSD, and possibly similar or greater recovery than Batch 24.\n- Endpoint/residence explanation: success depended mainly on spending a long time in the crystallization regime and eventually reaching 285 K, rather than on the detailed path. The alternative experiment should then approach Batch 24 in yield and fines despite the late temperature drop.\n\nA third possible outcome would be low recovery with acceptable fines. That would imply that productive growth requires cumulative residence across the intermediate temperatures, rather than merely avoiding nucleation or reaching the final equilibrium temperature.\n\n3. Least effectively used evidence and least reliable prediction\n\nThe account used the charge-loading evidence from Batches 12 and 13 least effectively. Batch 12 used 0.020 mol reagent and gave recovery 0.3123, whereas Batch 13 used 0.005 mol and gave 0.2208, with different selectivity and particle outcomes. Those batches were confounded by seed loading and cooling details, so they do not establish a concentration law, but they were the campaign\u2019s most relevant evidence that product concentration can alter recovery and nucleation. The mechanism report emphasized temperature history and solvents and did not integrate this evidence quantitatively.\n\nQ12 is therefore the least reliable held-out prediction. It doubles reagent charge relative to Q11 in S0, a solvent for which no matched concentration series or Batch-24-style ramp was run. Its predicted increase in recovery and fines rests on a general supersaturation argument, while the actual target-product concentration also depends on reaction conversion, selectivity, degradation, solubility and seed uptake. The available loading experiments do not isolate those effects, so both the magnitude of the recovery increase and whether fines cross 0.50 are especially uncertain. No prediction truth has been used, and the sealed prediction is unchanged."
  },
  "failure": null,
  "elapsed_s": 57.719000000011874,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 1460608,
    "input_tokens": 1635793,
    "output_tokens": 21493,
    "reasoning_output_tokens": 6754
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
    "selected_experiment_index": 24,
    "selection_rationale": "Batch 24 achieved the highest observed seed-excluded crystal recovery among specification-compliant batches (crystal_yield 0.3004), with crystal_purity 1.000 and crystal_fines_fraction 0.1741. Its very gradual seeded cooling without quench materially suppressed fines while improving recovery."
  },
  "recommendation_recipe": {
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
        "duration_s": 7200,
        "operation": "heat",
        "stirring_speed_rpm": 400,
        "target_temperature_K": 340
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 330
      },
      {
        "operation": "seed_crystals",
        "seed_mass_g": 0.05
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 325
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 320
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 315
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 312
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 310
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 308
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 306
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 304
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 302
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 301
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 300
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 299
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 298
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 297
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 296
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 295
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 294
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 293
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 292
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 291
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 290
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 289
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 288
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 287
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 286
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
      }
    ],
    "excluded_rejected_attempts": [],
    "lifecycle_index": 24,
    "source_attempts": 40
  },
  "prediction_evaluation": {
    "contrasts": [
      {
        "absolute_delta_error": 0.2298915100154434,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_yield",
        "predicted_delta": 0.07999999999999996,
        "resolved": true,
        "true_delta": -0.14989151001544343
      },
      {
        "absolute_delta_error": 0.009354120884849326,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_purity",
        "predicted_delta": 0.010000000000000009,
        "resolved": false,
        "true_delta": 0.0006458791151506826
      },
      {
        "absolute_delta_error": 0.010619598499364988,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_size",
        "predicted_delta": 0.03,
        "resolved": true,
        "true_delta": 0.01938040150063501
      },
      {
        "absolute_delta_error": 0.4283138299289017,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.10000000000000003,
        "resolved": true,
        "true_delta": -0.5283138299289017
      },
      {
        "absolute_delta_error": 0.04015921777357051,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_yield",
        "predicted_delta": 0.04000000000000001,
        "resolved": false,
        "true_delta": -0.00015921777357050249
      },
      {
        "absolute_delta_error": 0.0002539453646217549,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_purity",
        "predicted_delta": 0.010000000000000009,
        "resolved": false,
        "true_delta": 0.009746054635378254
      },
      {
        "absolute_delta_error": 0.07218557110203587,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_size",
        "predicted_delta": 0.065,
        "resolved": true,
        "true_delta": -0.007185571102035868
      },
      {
        "absolute_delta_error": 0.5342669082202977,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.37,
        "resolved": true,
        "true_delta": 0.16426690822029769
      },
      {
        "absolute_delta_error": 0.0695478575648261,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_yield",
        "predicted_delta": 0.07,
        "resolved": false,
        "true_delta": 0.0004521424351739134
      },
      {
        "absolute_delta_error": 0.0064452895693087875,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.010000000000000009,
        "resolved": false,
        "true_delta": -0.0035547104306912214
      },
      {
        "absolute_delta_error": 0.03168654733429699,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_size",
        "predicted_delta": -0.07500000000000001,
        "resolved": true,
        "true_delta": -0.04331345266570302
      },
      {
        "absolute_delta_error": 0.11295396285845927,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.51,
        "resolved": true,
        "true_delta": 0.6229539628584593
      },
      {
        "absolute_delta_error": 0.11437670725156426,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_yield",
        "predicted_delta": -0.07,
        "resolved": true,
        "true_delta": 0.04437670725156426
      },
      {
        "absolute_delta_error": 0.0010561827941991675,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.010000000000000009,
        "resolved": true,
        "true_delta": -0.011056182794199176
      },
      {
        "absolute_delta_error": 0.009705581270642999,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_size",
        "predicted_delta": -0.03,
        "resolved": true,
        "true_delta": -0.039705581270643
      },
      {
        "absolute_delta_error": 0.4803702872401259,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.18,
        "resolved": true,
        "true_delta": 0.6603702872401259
      },
      {
        "absolute_delta_error": 0.04351718430200213,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_yield",
        "predicted_delta": 0.051000000000000004,
        "resolved": true,
        "true_delta": 0.09451718430200214
      },
      {
        "absolute_delta_error": 0.01194368604118523,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_purity",
        "predicted_delta": 0.0,
        "resolved": true,
        "true_delta": -0.01194368604118523
      },
      {
        "absolute_delta_error": 0.08389816770165479,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_size",
        "predicted_delta": -0.07,
        "resolved": true,
        "true_delta": 0.013898167701654779
      },
      {
        "absolute_delta_error": 0.014607270218161245,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.07999999999999999,
        "resolved": false,
        "true_delta": 0.06539272978183874
      },
      {
        "absolute_delta_error": 0.14504321303990106,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_yield",
        "predicted_delta": 0.15999999999999998,
        "resolved": false,
        "true_delta": 0.014956786960098917
      },
      {
        "absolute_delta_error": 0.004828397249087235,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_purity",
        "predicted_delta": -0.010000000000000009,
        "resolved": false,
        "true_delta": -0.005171602750912774
      },
      {
        "absolute_delta_error": 0.024356873957321043,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_size",
        "predicted_delta": -0.04999999999999999,
        "resolved": true,
        "true_delta": -0.025643126042678946
      },
      {
        "absolute_delta_error": 0.3159895667604081,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.29000000000000004,
        "resolved": true,
        "true_delta": 0.6059895667604082
      }
    ],
    "failures": [],
    "metrics": {
      "crystal_fines_fraction": {
        "coverage80": 0.4166666666666667,
        "interval_score80": 2.5618194829902716,
        "interval_width": 0.3725,
        "mae": 0.35388008949525923,
        "n": 12,
        "planned": 12
      },
      "crystal_purity": {
        "coverage80": 1.0,
        "interval_score80": 0.07916666666666662,
        "interval_width": 0.07916666666666662,
        "mae": 0.009595828571588092,
        "n": 12,
        "planned": 12
      },
      "crystal_size": {
        "coverage80": 0.6666666666666666,
        "interval_score80": 0.3625396305454724,
        "interval_width": 0.17316666666666666,
        "mae": 0.0699491122533999,
        "n": 12,
        "planned": 12
      },
      "crystal_yield": {
        "coverage80": 0.8333333333333334,
        "interval_score80": 0.2668186017354784,
        "interval_width": 0.2520833333333333,
        "mae": 0.0604657648898729,
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
    "resolved_direction_n": 16,
    "tie_correct": 1,
    "tie_n": 8,
    "valid": true
  },
  "public_baselines": {
    "available": true,
    "mae": {
      "public_mean": {
        "crystal_fines_fraction": 0.3071534143698245,
        "crystal_purity": 0.004869434381922731,
        "crystal_size": 0.021546874201482696,
        "crystal_yield": 0.050468044660726796
      },
      "public_nearest_neighbor": {
        "crystal_fines_fraction": 0.347583165054864,
        "crystal_purity": 0.017021791429358862,
        "crystal_size": 0.026560484447241763,
        "crystal_yield": 0.08135616992079515
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
        "cached_input": 1414656,
        "input": 1472195,
        "output": 13908,
        "stage": "source",
        "uncached_input": 57539
      },
      {
        "cached_input": 0,
        "input": 46088,
        "output": 2802,
        "stage": "K1",
        "uncached_input": 46088
      },
      {
        "cached_input": 0,
        "input": 57426,
        "output": 2738,
        "stage": "Q",
        "uncached_input": 57426
      },
      {
        "cached_input": 45952,
        "input": 60084,
        "output": 2045,
        "stage": "K2",
        "uncached_input": 14132
      }
    ],
    "total": {
      "cached_input": 1460608,
      "input": 1635793,
      "input_plus_output": 1657286,
      "output": 21493,
      "uncached_input": 175185
    },
    "valid": true
  },
  "elapsed_s": 1093.7190000000119
}
```
