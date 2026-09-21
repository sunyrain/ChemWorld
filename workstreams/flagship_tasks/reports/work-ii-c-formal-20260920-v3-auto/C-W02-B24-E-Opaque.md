# C-W02-B24-E-Opaque

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
      "target_temperature_K": 360
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 7200,
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
  "end_step": 10,
  "lifecycle_index": 1,
  "metrics": {
    "byproduct_signal": 0.22398467361927032,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.518471896648407,
    "crystal_fines_fraction": 0.8830021619796753,
    "crystal_purity": 0.9790710806846619,
    "crystal_size": 0.05531816557049751,
    "crystal_yield": 0.5406267642974854,
    "degradation_warning": 0.09098739176988602,
    "safety_risk": 0.15342745184898376,
    "score": 0.45450910925865173,
    "selectivity": 0.6665233969688416,
    "virtual_spectrum_summary": 0.1641358882188797,
    "yield": 0.6643497943878174
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
      "target_temperature_K": 340
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
      "stirring_speed_rpm": 200
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 150
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
  "end_step": 23,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.31660717725753784,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6002417802810669,
    "crystal_fines_fraction": 0.7202679514884949,
    "crystal_purity": 0.9794086217880249,
    "crystal_size": 0.10005781054496765,
    "crystal_yield": 0.4889584481716156,
    "degradation_warning": 0.12317172437906265,
    "safety_risk": 0.17160147428512573,
    "score": 0.46406400203704834,
    "selectivity": 0.6003788113594055,
    "virtual_spectrum_summary": 0.2295612245798111,
    "yield": 0.5889338254928589
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
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 340
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
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 150
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 290
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 120
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 120
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 120
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 120
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 120
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 120
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
  "end_step": 51,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.46096304059028625,
    "conversion": 0.9983179569244385,
    "cost": 1.0,
    "crystal_csd_quality": 0.45760977268218994,
    "crystal_fines_fraction": 0.9946458339691162,
    "crystal_purity": 0.9866682887077332,
    "crystal_size": 0.06512456387281418,
    "crystal_yield": 0.39590024948120117,
    "degradation_warning": 0.23346374928951263,
    "safety_risk": 0.1770145446062088,
    "score": 0.3578220009803772,
    "selectivity": 0.46218571066856384,
    "virtual_spectrum_summary": 0.3585883677005768,
    "yield": 0.4612984359264374
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
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 340
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
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
  "end_step": 66,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.5488171577453613,
    "conversion": 0.9889965057373047,
    "cost": 1.0,
    "crystal_csd_quality": 0.5507425665855408,
    "crystal_fines_fraction": 0.7079606652259827,
    "crystal_purity": 1.0,
    "crystal_size": 0.06854479759931564,
    "crystal_yield": 0.1830451637506485,
    "degradation_warning": 0.27795737981796265,
    "safety_risk": 0.16405069828033447,
    "score": 0.32272255420684814,
    "selectivity": 0.29592689871788025,
    "virtual_spectrum_summary": 0.4269302487373352,
    "yield": 0.2822972238063812
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
      "target_temperature_K": 340
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 315
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
      "target_temperature_K": 300
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
  "end_step": 88,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.6333808302879333,
    "conversion": 0.996337890625,
    "cost": 1.0,
    "crystal_csd_quality": 0.5108875632286072,
    "crystal_fines_fraction": 0.8215884566307068,
    "crystal_purity": 0.9697780609130859,
    "crystal_size": 0.044177692383527756,
    "crystal_yield": 0.2559312582015991,
    "degradation_warning": 0.37483838200569153,
    "safety_risk": 0.11814527958631516,
    "score": 0.3234214186668396,
    "selectivity": 0.32955360412597656,
    "virtual_spectrum_summary": 0.5170367360115051,
    "yield": 0.3234006464481354
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
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "catalyst": 2,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 350
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
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
      "target_temperature_K": 300
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
      "target_temperature_K": 280
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
  "end_step": 115,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.7669835686683655,
    "conversion": 0.9924335479736328,
    "cost": 1.0,
    "crystal_csd_quality": 0.4202967584133148,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9900245070457458,
    "crystal_size": 0.019574973732233047,
    "crystal_yield": 0.08558762818574905,
    "degradation_warning": 0.41742628812789917,
    "safety_risk": 0.09610413759946823,
    "score": 0.2054186463356018,
    "selectivity": 0.09129734337329865,
    "virtual_spectrum_summary": 0.6096827983856201,
    "yield": 0.09318296611309052
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
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 340
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 315
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
      "operation": "cool_crystallize",
      "target_temperature_K": 280
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
  "end_step": 140,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.6605169773101807,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.503978431224823,
    "crystal_fines_fraction": 0.7937592267990112,
    "crystal_purity": 0.9702805876731873,
    "crystal_size": 0.07732200622558594,
    "crystal_yield": 0.26212722063064575,
    "degradation_warning": 0.37669727206230164,
    "safety_risk": 0.11612512171268463,
    "score": 0.32105323672294617,
    "selectivity": 0.2599480450153351,
    "virtual_spectrum_summary": 0.5327981114387512,
    "yield": 0.28659525513648987
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
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 350
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 290
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 320
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
      "target_temperature_K": 305
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
  "end_step": 168,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.617360532283783,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.4405219852924347,
    "crystal_fines_fraction": 0.9867806434631348,
    "crystal_purity": 0.9712150692939758,
    "crystal_size": 0.08150225877761841,
    "crystal_yield": 0.3395020067691803,
    "degradation_warning": 0.39883744716644287,
    "safety_risk": 0.12443681806325912,
    "score": 0.3241941034793854,
    "selectivity": 0.36701059341430664,
    "virtual_spectrum_summary": 0.5190251469612122,
    "yield": 0.3587053120136261
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
      "solvent": 0,
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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
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
  "end_step": 196,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.19290854036808014,
    "conversion": 0.954730212688446,
    "cost": 1.0,
    "crystal_csd_quality": 0.5476334095001221,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9734294414520264,
    "crystal_size": 0.02709902450442314,
    "crystal_yield": 0.5128852725028992,
    "degradation_warning": 0.022359659895300865,
    "safety_risk": 0.14406552910804749,
    "score": 0.42836645245552063,
    "selectivity": 0.6285998225212097,
    "virtual_spectrum_summary": 0.1161615401506424,
    "yield": 0.6125680208206177
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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
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
  "end_step": 216,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.20055605471134186,
    "conversion": 0.966876745223999,
    "cost": 1.0,
    "crystal_csd_quality": 0.9713567495346069,
    "crystal_fines_fraction": 0.011348346248269081,
    "crystal_purity": 0.9905356764793396,
    "crystal_size": 0.39038214087486267,
    "crystal_yield": 0.009045898914337158,
    "degradation_warning": 0.0394643098115921,
    "safety_risk": 0.12696774303913116,
    "score": 0.5325042605400085,
    "selectivity": 0.6488299369812012,
    "virtual_spectrum_summary": 0.12806476652622223,
    "yield": 0.6453807950019836
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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
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
      "target_temperature_K": 292
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
  "end_step": 237,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.20907065272331238,
    "conversion": 0.9800728559494019,
    "cost": 1.0,
    "crystal_csd_quality": 0.5079666972160339,
    "crystal_fines_fraction": 0.9936485886573792,
    "crystal_purity": 0.986129641532898,
    "crystal_size": 0.034510910511016846,
    "crystal_yield": 0.4865204989910126,
    "degradation_warning": 0.01648433692753315,
    "safety_risk": 0.16938477754592896,
    "score": 0.42182907462120056,
    "selectivity": 0.6659274697303772,
    "virtual_spectrum_summary": 0.12240681052207947,
    "yield": 0.6340616345405579
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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
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
      "target_temperature_K": 296
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
  "end_step": 260,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.19307219982147217,
    "conversion": 0.9840424656867981,
    "cost": 1.0,
    "crystal_csd_quality": 0.5207071900367737,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9868411421775818,
    "crystal_size": 0.055855438113212585,
    "crystal_yield": 0.4766741394996643,
    "degradation_warning": 0.03824274614453316,
    "safety_risk": 0.16842930018901825,
    "score": 0.4229259788990021,
    "selectivity": 0.645358681678772,
    "virtual_spectrum_summary": 0.12339894473552704,
    "yield": 0.6380247473716736
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
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
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
  "end_step": 283,
  "lifecycle_index": 13,
  "metrics": {
    "byproduct_signal": 0.19658862054347992,
    "conversion": 0.9782694578170776,
    "cost": 1.0,
    "crystal_csd_quality": 0.5384986996650696,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9732659459114075,
    "crystal_size": 0.03342832624912262,
    "crystal_yield": 0.45815300941467285,
    "degradation_warning": 0.029871223494410515,
    "safety_risk": 0.1679171472787857,
    "score": 0.4176199436187744,
    "selectivity": 0.6585204601287842,
    "virtual_spectrum_summary": 0.1215657889842987,
    "yield": 0.6381319761276245
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
      "solvent": 1,
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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
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
  "end_step": 318,
  "lifecycle_index": 14,
  "metrics": {
    "byproduct_signal": 0.21090167760849,
    "conversion": 0.9877650141716003,
    "cost": 1.0,
    "crystal_csd_quality": 0.5426833033561707,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9566240906715393,
    "crystal_size": 0.06898024678230286,
    "crystal_yield": 0.4630819857120514,
    "degradation_warning": 0.03479684889316559,
    "safety_risk": 0.1679171472787857,
    "score": 0.41914376616477966,
    "selectivity": 0.651919424533844,
    "virtual_spectrum_summary": 0.1316545009613037,
    "yield": 0.633355975151062
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
      "solvent": 1,
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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
    },
    {
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 1,
      "operation": "cool_crystallize",
      "target_temperature_K": 298
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
  "end_step": 329,
  "lifecycle_index": 15,
  "metrics": {
    "byproduct_signal": 0.2043081820011139,
    "conversion": 0.9851879477500916,
    "cost": 1.0,
    "crystal_csd_quality": 0.13621847331523895,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9955223202705383,
    "crystal_size": 0.039047982543706894,
    "crystal_yield": 0.0,
    "degradation_warning": 0.027644362300634384,
    "safety_risk": 0.12714006006717682,
    "score": 0.23031899333000183,
    "selectivity": 0.6499347686767578,
    "virtual_spectrum_summary": 0.12480946630239487,
    "yield": 0.6420933604240417
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
      "solvent": 1,
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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
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
      "target_temperature_K": 292
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 296
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
  "end_step": 351,
  "lifecycle_index": 16,
  "metrics": {
    "byproduct_signal": 0.19738702476024628,
    "conversion": 0.9696062803268433,
    "cost": 1.0,
    "crystal_csd_quality": 0.4840969741344452,
    "crystal_fines_fraction": 0.9878060221672058,
    "crystal_purity": 0.9705057740211487,
    "crystal_size": 0.039643123745918274,
    "crystal_yield": 0.4668862521648407,
    "degradation_warning": 0.03896861523389816,
    "safety_risk": 0.16842108964920044,
    "score": 0.40861567854881287,
    "selectivity": 0.6470864415168762,
    "virtual_spectrum_summary": 0.12609873712062836,
    "yield": 0.6330650448799133
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
      "solvent": 1,
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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
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
      "target_temperature_K": 292
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 310
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
  "end_step": 369,
  "lifecycle_index": 17,
  "metrics": {
    "byproduct_signal": 0.21258799731731415,
    "conversion": 0.9841080904006958,
    "cost": 1.0,
    "crystal_csd_quality": 0.5138474702835083,
    "crystal_fines_fraction": 0.9720020890235901,
    "crystal_purity": 0.9920418858528137,
    "crystal_size": 0.027286067605018616,
    "crystal_yield": 0.428062379360199,
    "degradation_warning": 0.033687300980091095,
    "safety_risk": 0.1643214076757431,
    "score": 0.4110182821750641,
    "selectivity": 0.6439520120620728,
    "virtual_spectrum_summary": 0.13208268582820892,
    "yield": 0.6417343020439148
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
      "solvent": 1,
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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
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
      "target_temperature_K": 292
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 325
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
  "end_step": 381,
  "lifecycle_index": 18,
  "metrics": {
    "byproduct_signal": 0.18622800707817078,
    "conversion": 0.9872375130653381,
    "cost": 1.0,
    "crystal_csd_quality": 0.5286559462547302,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9877114295959473,
    "crystal_size": 0.07631774246692657,
    "crystal_yield": 0.34477415680885315,
    "degradation_warning": 0.02954183891415596,
    "safety_risk": 0.15876051783561707,
    "score": 0.3962147831916809,
    "selectivity": 0.6492198705673218,
    "virtual_spectrum_summary": 0.11571923643350601,
    "yield": 0.6502508521080017
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
      "solvent": 1,
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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
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
  "end_step": 491,
  "lifecycle_index": 19,
  "metrics": {
    "byproduct_signal": 0.2070489078760147,
    "conversion": 0.9719560742378235,
    "cost": 1.0,
    "crystal_csd_quality": 1.0,
    "crystal_fines_fraction": 0.0,
    "crystal_purity": 0.9858769178390503,
    "crystal_size": 0.3799891471862793,
    "crystal_yield": 0.003889756742864847,
    "degradation_warning": 0.024242615327239037,
    "safety_risk": 0.12696774303913116,
    "score": 0.5355420112609863,
    "selectivity": 0.6486961245536804,
    "virtual_spectrum_summary": 0.12478607147932053,
    "yield": 0.6399069428443909
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
      "solvent": 1,
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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
    },
    {
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 3000,
      "operation": "cool_crystallize",
      "target_temperature_K": 298
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
  "end_step": 502,
  "lifecycle_index": 20,
  "metrics": {
    "byproduct_signal": 0.2047508805990219,
    "conversion": 0.9745181202888489,
    "cost": 1.0,
    "crystal_csd_quality": 0.4616546034812927,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9843227863311768,
    "crystal_size": 0.048205628991127014,
    "crystal_yield": 0.46181225776672363,
    "degradation_warning": 0.028366511687636375,
    "safety_risk": 0.1679166555404663,
    "score": 0.4060556888580322,
    "selectivity": 0.6602967381477356,
    "virtual_spectrum_summary": 0.12537792325019836,
    "yield": 0.631598949432373
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
      "solvent": 1,
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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 315
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
  "end_step": 517,
  "lifecycle_index": 21,
  "metrics": {
    "byproduct_signal": 0.397862046957016,
    "conversion": 0.9894089102745056,
    "cost": 1.0,
    "crystal_csd_quality": 0.49058839678764343,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9838792085647583,
    "crystal_size": 0.043837063014507294,
    "crystal_yield": 0.4043174684047699,
    "degradation_warning": 0.18772371113300323,
    "safety_risk": 0.158280611038208,
    "score": 0.3703747093677521,
    "selectivity": 0.4814175069332123,
    "virtual_spectrum_summary": 0.30329978466033936,
    "yield": 0.500694751739502
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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
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
  "end_step": 530,
  "lifecycle_index": 22,
  "metrics": {
    "byproduct_signal": 0.19309446215629578,
    "conversion": 0.9570387005805969,
    "cost": 1.0,
    "crystal_csd_quality": 0.6217201948165894,
    "crystal_fines_fraction": 0.6307635307312012,
    "crystal_purity": 0.9961443543434143,
    "crystal_size": 0.06888142973184586,
    "crystal_yield": 0.5448063015937805,
    "degradation_warning": 0.024243077263236046,
    "safety_risk": 0.14773255586624146,
    "score": 0.49970942735671997,
    "selectivity": 0.6540095806121826,
    "virtual_spectrum_summary": 0.11711133271455765,
    "yield": 0.6244389414787292
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
      "stirring_speed_rpm": 500,
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
      "target_temperature_K": 295
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 290
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 285
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
  "end_step": 555,
  "lifecycle_index": 23,
  "metrics": {
    "byproduct_signal": 0.19062714278697968,
    "conversion": 0.9487781524658203,
    "cost": 1.0,
    "crystal_csd_quality": 0.7066512107849121,
    "crystal_fines_fraction": 0.46784666180610657,
    "crystal_purity": 0.9902835488319397,
    "crystal_size": 0.09238635748624802,
    "crystal_yield": 0.5392926335334778,
    "degradation_warning": 0.01741791144013405,
    "safety_risk": 0.14773255586624146,
    "score": 0.5358890295028687,
    "selectivity": 0.671334445476532,
    "virtual_spectrum_summary": 0.11268298327922821,
    "yield": 0.6422432065010071
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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 327.5
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 325
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 322.5
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 317.5
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 315
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 312.5
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 307.5
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 305
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 302.5
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 297.5
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 295
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 292.5
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 290
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 287.5
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 285
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 282.5
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 280
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 277.5
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 275
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 272.5
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 267.5
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 265
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 262.5
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 260
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 257.5
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 255
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 252.5
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
  "end_step": 595,
  "lifecycle_index": 24,
  "metrics": {
    "byproduct_signal": 0.19039535522460938,
    "conversion": 0.9546932578086853,
    "cost": 1.0,
    "crystal_csd_quality": 0.6836092472076416,
    "crystal_fines_fraction": 0.5284395217895508,
    "crystal_purity": 0.9991211295127869,
    "crystal_size": 0.07253067195415497,
    "crystal_yield": 0.5334048271179199,
    "degradation_warning": 0.019919002428650856,
    "safety_risk": 0.14773255586624146,
    "score": 0.5234233140945435,
    "selectivity": 0.6649750471115112,
    "virtual_spectrum_summary": 0.11368099600076675,
    "yield": 0.6433753371238708
  },
  "ordinal": 24
}
```

## K1

```json
{
  "payload": {
    "report": "Mechanistic account\n\nThe campaign indicates two coupled but distinguishable stages: catalyst/solvent/thermal history sets the amount and quality of target available in solution, while the cooling trajectory controls how that target is partitioned between a small number of grown crystals and a large population of fines. The recommended process remains batch 23.\n\nObserved material effects\n\n\u2022 Catalyst C0 was clearly preferred. With solvent S0, alternatives C1, C2, and C3 gave final reaction yields of about 0.323, 0.093, and 0.287 in batches 5\u20137, compared with roughly 0.62\u20130.66 for successful C0 histories. Their crystal recoveries were also lower: 0.256, 0.086, and 0.262, respectively. I interpret this as inferior target-forming selectivity, not merely poorer crystallization, because these batches also had high byproduct signals and low reaction selectivity. The exact molecular cause is hidden and therefore untested.\n\n\u2022 Solvent S0 gave the strongest recovery. In the initial C0 solvent survey, batches 1\u20134 gave crystal yields of 0.541 (S0), 0.489 (S1), 0.396 (S2), and 0.183 (S3). S2 and S3 also showed poorer reaction selectivity and more byproduct. Because their crystallization schedules were not perfectly identical, this ranking is strong empirical evidence rather than a clean estimate of an isolated solvent coefficient.\n\nReaction behavior\n\nA useful empirical decomposition is\n\nreaction yield \u2248 conversion \u00d7 selectivity,\n\nwhich was broadly consistent with the assays. For example, batch 1 reached conversion near 1 and selectivity about 0.67\u20130.68, giving reaction yield about 0.66\u20130.68. In batch 23, conversion was 0.949, selectivity 0.671, and reaction yield 0.642.\n\nHigher temperature or prolonged warm residence accelerated conversion but also promoted byproduct formation and degradation. Batch 1, heated near 360 K for one hour, reached full conversion but showed byproduct near 0.224 and degradation near 0.091. The adopted milder C0/S0 reaction near 330 K for 1800 s retained reaction yield around 0.64 while batch 23 showed byproduct 0.191 and degradation only 0.017. Batch 8 illustrates cumulative thermal damage: a heat/cool/reheat history without quenching produced degradation about 0.399, reaction yield about 0.359, and crystal yield only 0.340.\n\nCrystallization mechanism and coupling\n\nThe reported crystal-yield quantity is\n\nYcrystal = seed-excluded recovered target product / target product present before separation.\n\nIt is therefore a crystallization-stage recovery, not overall yield from charged reagent. A useful overall-product proxy would be\n\nYoverall \u2248 Yreaction \u00d7 Ycrystal,\n\nalthough the campaign objective explicitly optimized Ycrystal subject to purity and fines constraints.\n\nThe results support competition between growth on existing crystals and secondary nucleation. Cooling generated high recovery, but abrupt or coarse cooling generated many sub-20 \u00b5m particles. Holding seeded quenched liquor without a cooling operation produced large, clean particles but almost no seed-excluded recovery: batch 10 had fines 0.011 and crystal yield 0.009; batch 19, even after 100 long holds, had fines effectively zero but yield only 0.0039. Thus ordinary holds at about 298 K did not create enough supersaturation for material transfer onto the seeds.\n\nConversely, once a cooling/crystallization operation was applied, recovery rose sharply but fines often approached unity. Batches 11\u201314 gave crystal yields around 0.46\u20130.49 but fines around 0.99\u20131.00. Increasing seed from 0.05 g to about 1 g in batch 14 did not suppress this response, so seed mass alone was not the controlling variable over the tested range. A very short cooling operation in batch 15 gave essentially zero recovery and still poor particle statistics, while a 3000 s operation in batch 20 already gave recovery 0.462 and fines 1.00. This suggests a history-dependent nucleation threshold rather than smooth proportional control by cooling duration.\n\nThe successful intervention was to distribute the temperature change over repeated long, small cooling stages. Batch 22 used roughly 20 K stages down to 250 K and achieved the highest observed recovery, 0.545, but fines remained 0.631 and failed the specification. Batch 23 used 5 K stages from approximately 325 K to 250 K. It retained recovery of 0.539 while reducing fines to 0.468, with purity 0.990. My interpretation is that each small supersaturation increment allowed existing particles to consume solute before the next increment, limiting secondary nucleation while still reaching the low-temperature recovery plateau.\n\nProcess-history dependence\n\nFinal temperature alone was insufficient to predict quality. Batch 1 reached 270 K and recovered 0.541 but had fines 0.883. Batch 22 reached 250 K in four coarse stages and had fines 0.631. Batch 23 reached 250 K through 5 K stages and passed at 0.468. The sequence and spacing of the cooling operations therefore mattered at least as much as the endpoint.\n\nQuenching also changed the subsequent regime. It arrested reaction degradation, but immediate crystallization from quenched liquor repeatedly produced very high fines. Avoiding quench during the staged-cooling sequence in batch 23 preserved low degradation because the initial reaction was mild, while enabling the successful particle-history trajectory. This is an empirical coupling; possibilities such as quench-induced mixing, a discontinuous supersaturation jump, or altered nucleation kinetics remain untested.\n\nAttempts to remove fines by post-crystallization reheating were unsuccessful. Reheating to 296\u2013310 K in batches 16\u201317 reduced recovery somewhat but left fines near 0.97\u20130.99; reheating to 325 K in batch 18 lowered recovery to 0.345 without improving fines. Thus the observed distribution was not readily repaired after nucleation; it had to be controlled during its formation.\n\nPurity and tradeoff\n\nCrystal purity was robustly high in most productive batches, generally about 0.97\u20131.00, so the active constraint was particle-size distribution rather than purity. The unresolved tradeoff is between maximum recovery and reliable fines compliance. Batch 22 recovered 0.545 but failed the fines limit. Batch 23 recovered 0.539 and passed both constraints. Batch 24 used still finer 2.5 K stages and gave recovery 0.533, purity 0.999, but fines 0.528, narrowly failing. Therefore finer staging was not monotonically better.\n\nUncertainty and revisions\n\nThe strategy evolved from material screening, through quench/seed/hold and reheating tests, to explicit cooling-path control. Early interpretation overemphasized seed loading and long holds; batches 10, 14, and 19 falsified the idea that those variables alone would produce useful seed-excluded recovery. Reheating experiments then showed that post hoc ripening was ineffective under the tested conditions. The final revision focused on limiting supersaturation increments during initial crystal formation.\n\nInstrument noise and process variability are important near the fines threshold. Batch 23 had a particle-size reading of 0.517 before its final assay reported 0.468, while batch 24 reported 0.528 in the final assay. These differences imply that a nominal value close to 0.50 is not a large safety margin. Replicates of the batch-23 schedule, intermediate step sizes between 5 and 20 K, altered stage residence times, and independent tests separating quench from cooling-rate effects remain untested. Nevertheless, batch 23 is the strongest completed evidence because it uniquely combined high seed-excluded recovery with observed purity and fines compliance."
  },
  "failure": null,
  "elapsed_s": 59.671999999991385,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 976768,
    "input_tokens": 1091802,
    "output_tokens": 13934,
    "reasoning_output_tokens": 3668
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
          "estimate": 0.42,
          "lower80": 0.25,
          "upper80": 0.61
        },
        "crystal_purity": {
          "estimate": 0.95,
          "lower80": 0.89,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.12,
          "lower80": 0.06,
          "upper80": 0.21
        },
        "crystal_yield": {
          "estimate": 0.38,
          "lower80": 0.25,
          "upper80": 0.51
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q01"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.45,
          "lower80": 0.27,
          "upper80": 0.65
        },
        "crystal_purity": {
          "estimate": 0.97,
          "lower80": 0.91,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.11,
          "lower80": 0.05,
          "upper80": 0.2
        },
        "crystal_yield": {
          "estimate": 0.22,
          "lower80": 0.1,
          "upper80": 0.37
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q02"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.56,
          "lower80": 0.36,
          "upper80": 0.75
        },
        "crystal_purity": {
          "estimate": 0.95,
          "lower80": 0.89,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.09,
          "lower80": 0.04,
          "upper80": 0.17
        },
        "crystal_yield": {
          "estimate": 0.41,
          "lower80": 0.28,
          "upper80": 0.53
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q03"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.4,
          "lower80": 0.23,
          "upper80": 0.59
        },
        "crystal_purity": {
          "estimate": 0.95,
          "lower80": 0.89,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.13,
          "lower80": 0.07,
          "upper80": 0.22
        },
        "crystal_yield": {
          "estimate": 0.42,
          "lower80": 0.3,
          "upper80": 0.54
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q04"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.36,
          "lower80": 0.2,
          "upper80": 0.54
        },
        "crystal_purity": {
          "estimate": 0.95,
          "lower80": 0.89,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.14,
          "lower80": 0.08,
          "upper80": 0.23
        },
        "crystal_yield": {
          "estimate": 0.43,
          "lower80": 0.31,
          "upper80": 0.55
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q05"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.91,
          "lower80": 0.77,
          "upper80": 1.0
        },
        "crystal_purity": {
          "estimate": 0.96,
          "lower80": 0.9,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.04,
          "lower80": 0.01,
          "upper80": 0.09
        },
        "crystal_yield": {
          "estimate": 0.45,
          "lower80": 0.33,
          "upper80": 0.57
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q06"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.32,
          "lower80": 0.17,
          "upper80": 0.5
        },
        "crystal_purity": {
          "estimate": 0.95,
          "lower80": 0.89,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.15,
          "lower80": 0.08,
          "upper80": 0.24
        },
        "crystal_yield": {
          "estimate": 0.44,
          "lower80": 0.32,
          "upper80": 0.56
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q07"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.76,
          "lower80": 0.56,
          "upper80": 0.93
        },
        "crystal_purity": {
          "estimate": 0.96,
          "lower80": 0.9,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.06,
          "lower80": 0.02,
          "upper80": 0.12
        },
        "crystal_yield": {
          "estimate": 0.4,
          "lower80": 0.27,
          "upper80": 0.53
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q08"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.96,
          "lower80": 0.82,
          "upper80": 1.0
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.92,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.03,
          "lower80": 0.0,
          "upper80": 0.08
        },
        "crystal_yield": {
          "estimate": 0.03,
          "lower80": 0.0,
          "upper80": 0.12
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q09"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.98,
          "lower80": 0.87,
          "upper80": 1.0
        },
        "crystal_purity": {
          "estimate": 0.96,
          "lower80": 0.9,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.04,
          "lower80": 0.01,
          "upper80": 0.09
        },
        "crystal_yield": {
          "estimate": 0.4,
          "lower80": 0.27,
          "upper80": 0.53
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q10"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.35,
          "lower80": 0.19,
          "upper80": 0.53
        },
        "crystal_purity": {
          "estimate": 0.95,
          "lower80": 0.89,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.14,
          "lower80": 0.08,
          "upper80": 0.23
        },
        "crystal_yield": {
          "estimate": 0.43,
          "lower80": 0.31,
          "upper80": 0.55
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q11"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.7,
          "lower80": 0.5,
          "upper80": 0.88
        },
        "crystal_purity": {
          "estimate": 0.92,
          "lower80": 0.83,
          "upper80": 0.98
        },
        "crystal_size": {
          "estimate": 0.07,
          "lower80": 0.03,
          "upper80": 0.14
        },
        "crystal_yield": {
          "estimate": 0.55,
          "lower80": 0.41,
          "upper80": 0.68
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q12"
      }
    ],
    "rationale": "Q01\u2013Q02 isolates solvent: I expect S1 to recover substantially more target than S3, while both retain high crystal purity; the particle-quality difference is less certain. Q03\u2013Q04 isolates seed loading: 0.045 g should provide enough growth surface to suppress some secondary nucleation, whereas 0.001 g is more likely to leave fines above specification, with little change in normalized recovery. Q05\u2013Q06 holds endpoint and total crystallization time approximately fixed: gradual cooling should favor growth and larger particles, while the initial rapid drop in Q06 should create persistent fines despite comparable or slightly higher recovery. Q07\u2013Q08 tests annealing followed by rapid recooling: prior reheating attempts did not reliably repair an established fine population, and the final fast recooling is expected to renucleate fines, so Q08 is worse than the continued staged history in Q07. Q09\u2013Q10 tests residence at 292 K after a fast drop: immediate filtration should give very little seed-excluded recovery, whereas the additional 7200 s crystallization should raise recovery sharply but leave a fine-rich population. Q11\u2013Q12 doubles reagent concentration at fixed solvent and catalyst: greater supersaturation should increase fractional recovery but also secondary nucleation and impurity risk, making Q12 less likely to satisfy the fines limit. Intervals are deliberately broad because the campaign did not exactly reproduce this concentration, C1 loading, 385 K reaction, or these fine temperature increments; uncertainty is greatest near the fines threshold and for the solvent and concentration extrapolations."
  },
  "failure": null,
  "elapsed_s": 81.42199999999139,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 976768,
    "input_tokens": 1138925,
    "output_tokens": 17426,
    "reasoning_output_tokens": 5416
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
    "report": "1. Status of the main claims\n\nSupported by direct observations:\n\n\u2022 C0 was the best tested catalyst. With S0, batches 5\u20137 using C1\u2013C3 had reaction yields of about 0.323, 0.093, and 0.287 and crystal yields of 0.256, 0.086, and 0.262. C0 batches commonly reached reaction yields near 0.64 and crystal recovery near 0.54. The interpretation that C0 has intrinsically better target selectivity is plausible, although the crystallization histories were not perfectly matched.\n\n\u2022 Excess warm residence caused deterioration. Batch 8\u2019s extended heat/reheat history produced degradation near 0.399 and crystal yield 0.340, whereas the milder reaction in batch 23 had degradation near 0.017 and crystal yield 0.539. This directly supports thermal-history dependence; assignment to a particular chemical degradation pathway remains interpretive.\n\n\u2022 Recovery and fines were strongly coupled. Seeded liquor held without cooling gave excellent particle quality but negligible seed-excluded recovery: batches 10 and 19 had yields of only 0.009 and 0.004 with fines near zero. Cooling raised recovery to roughly 0.4\u20130.5 in batches 11\u201314 and 20 but produced fines near unity. This tradeoff is directly observed.\n\n\u2022 Cooling history mattered beyond final temperature. Batch 1 reached 270 K with yield 0.541 but fines 0.883; batch 22 reached 250 K in coarse stages with yield 0.545 and fines 0.631; batch 23 reached 250 K in 5 K stages with yield 0.539 and fines 0.468. These observations support a path-dependent crystallization process.\n\n\u2022 Post-crystallization reheating was not an effective repair under the tested conditions. Batches 16\u201318 retained fines around 0.97\u20131.00 while recovery decreased. The interpretation that the fine population becomes difficult to reverse is supported within that limited reheating range.\n\nContradicted or weakened:\n\n\u2022 A simple monotonic rule that ever-finer cooling increments always reduce fines is contradicted by batch 24. Its 2.5 K staging gave fines 0.528, worse than batch 23\u2019s 0.468 with 5 K staging, while recovery decreased from 0.539 to 0.533. Process variability may contribute, but the direct observations do not justify monotonic extrapolation.\n\n\u2022 Seed loading alone as a strong control of fines is weakly contradicted by batch 14: increasing total seed to approximately 1 g did not prevent fines near 1.00. Differences among histories prevent a clean seed coefficient, but the result argues against a simple \u201cmore seed means fewer fines\u201d mechanism.\n\n\u2022 The solvent ranking is only partly supported. Batches 1\u20134 suggested recovery S0 > S1 > S2 > S3, but their crystallization histories differed. Thus the empirical ranking is observed, while attributing it entirely to solvent-dependent solubility is unproven.\n\nStill untested:\n\n\u2022 Whether quenching itself changes nucleation behavior, rather than merely changing temperature and stopping reaction.\n\n\u2022 Whether batch 23\u2019s fines result is reproducible or partly stochastic/instrumental. Its intermediate particle reading was 0.517, whereas the final assay reported 0.468.\n\n\u2022 The separate effects of cooling-step size, total cooling time, number of operation segments, and final temperature.\n\n\u2022 Molecular explanations for catalyst and solvent effects, which remain inaccessible for the anonymous materials.\n\n\u2022 Concentration effects and scale invariance; the campaign did not systematically vary reagent concentration.\n\n2. Most informative additional experiment\n\nI would repeat the batch-23 C0/S0 charge and reaction\u20140.04 mol reagent, 0.08 L solvent, 0.005 mol catalyst, 330 K for 1800 s\u2014but quench immediately after reaction, reheat to approximately 325 K, add 0.05 g seed, and then apply exactly the same 5 K, 14,400 s staged cooling schedule to 250 K before filtration and final assay.\n\nBatch 23 supplies the unquenched comparator, so one additional batch would distinguish two competing explanations:\n\n\u2022 Cooling-path explanation: particle quality is governed mainly by incremental supersaturation. After restoring the same crystallization starting temperature, the quenched batch should resemble batch 23\u2014yield around 0.53\u20130.54, purity above 0.98, and fines near or below 0.50.\n\n\u2022 Quench/state-history explanation: quenching creates a persistent nucleation-prone state through abrupt supersaturation, mixing, or another hidden state variable. Reheating would then fail to restore batch-23 behavior; fines would remain substantially above 0.50, potentially near the high values seen in quenched cooling batches 11\u201314, even if recovery remained high.\n\nA mixed outcome\u2014lower degradation or improved reaction quality but worse fines\u2014would show that quenching benefits the reaction while harming crystallization. Measuring particles immediately before filtration would also help separate final-assay noise from true process variability.\n\n3. Least effectively used observation and least reliable prediction\n\nThe observation used least effectively was batch 24\u2019s reversal relative to batch 23. I acknowledged it as nonmonotonicity or uncertainty, but much of the subsequent prediction rationale still treated finer staged cooling as reliably favorable. Batch 24 shows that step size alone is insufficient and that unmodelled segmentation, stochastic nucleation, or assay variation can move fines across the 0.50 boundary.\n\nThe least reliable held-out prediction is Q12. It doubles reagent concentration while holding solvent and catalyst fixed, a perturbation never isolated in the campaign. It can simultaneously alter reaction conversion, catalyst-to-reagent ratio, impurity production, supersaturation, recovered fraction, nucleation rate, and particle size. My prediction that Q12 would have higher crystal recovery but worse fines than Q11 is mechanistically plausible, but it is a multi-effect extrapolation rather than a relationship established by matched batches. The Q03\u2013Q04 seed comparison is also fragile because batch 14 did not support a strong monotonic seed-mass benefit, but Q12 involves the larger unsupported extrapolation."
  },
  "failure": null,
  "elapsed_s": 54.390999999974156,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 1012992,
    "input_tokens": 1189460,
    "output_tokens": 19269,
    "reasoning_output_tokens": 5913
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
    "selected_experiment_index": 23,
    "selection_rationale": "Batch 23 delivered the highest observed seed-excluded crystal recovery among completed batches meeting both quality constraints: crystal_yield 0.5393, crystal_purity 0.9903, and fines fraction 0.4678. Fine 5 K staged cooling to 250 K preserved recovery while suppressing fines."
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
        "stirring_speed_rpm": 500,
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
        "target_temperature_K": 295
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 290
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 285
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
    "lifecycle_index": 23,
    "source_attempts": 25
  },
  "prediction_evaluation": {
    "contrasts": [
      {
        "absolute_delta_error": 0.033117788811994675,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_yield",
        "predicted_delta": -0.16,
        "resolved": true,
        "true_delta": -0.19311778881199468
      },
      {
        "absolute_delta_error": 0.02144714403614556,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_purity",
        "predicted_delta": 0.020000000000000018,
        "resolved": false,
        "true_delta": -0.0014471440361455423
      },
      {
        "absolute_delta_error": 0.039026804726637075,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_size",
        "predicted_delta": -0.009999999999999995,
        "resolved": true,
        "true_delta": 0.02902680472663708
      },
      {
        "absolute_delta_error": 0.6202675737116523,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.030000000000000027,
        "resolved": true,
        "true_delta": -0.5902675737116523
      },
      {
        "absolute_delta_error": 0.010048436438670427,
        "direction_correct": true,
        "factor": "seed",
        "metric": "crystal_yield",
        "predicted_delta": 0.010000000000000009,
        "resolved": false,
        "true_delta": -4.843643867041836e-05
      },
      {
        "absolute_delta_error": 0.008235561540249181,
        "direction_correct": true,
        "factor": "seed",
        "metric": "crystal_purity",
        "predicted_delta": 0.0,
        "resolved": false,
        "true_delta": 0.008235561540249181
      },
      {
        "absolute_delta_error": 0.04022020934805376,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_size",
        "predicted_delta": 0.04000000000000001,
        "resolved": false,
        "true_delta": -0.00022020934805375147
      },
      {
        "absolute_delta_error": 0.1393685499038365,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.16000000000000003,
        "resolved": false,
        "true_delta": -0.020631450096163517
      },
      {
        "absolute_delta_error": 0.019739549297168146,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_yield",
        "predicted_delta": 0.020000000000000018,
        "resolved": false,
        "true_delta": 0.00026045070283187144
      },
      {
        "absolute_delta_error": 0.014867853659170427,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_purity",
        "predicted_delta": 0.010000000000000009,
        "resolved": false,
        "true_delta": -0.004867853659170418
      },
      {
        "absolute_delta_error": 0.06237930183589548,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_size",
        "predicted_delta": -0.1,
        "resolved": true,
        "true_delta": -0.03762069816410452
      },
      {
        "absolute_delta_error": 0.028101398289320567,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.55,
        "resolved": true,
        "true_delta": 0.5781013982893206
      },
      {
        "absolute_delta_error": 0.08006038328567322,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_yield",
        "predicted_delta": -0.03999999999999998,
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
        "absolute_delta_error": 0.05989709535243519,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_size",
        "predicted_delta": -0.09,
        "resolved": true,
        "true_delta": -0.030102904647564807
      },
      {
        "absolute_delta_error": 0.16239412170088124,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.44,
        "resolved": true,
        "true_delta": 0.6023941217008812
      },
      {
        "absolute_delta_error": 0.21631557789753358,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_yield",
        "predicted_delta": 0.37,
        "resolved": true,
        "true_delta": 0.1536844221024664
      },
      {
        "absolute_delta_error": 0.00547289306179688,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_purity",
        "predicted_delta": -0.020000000000000018,
        "resolved": true,
        "true_delta": -0.014527106938203138
      },
      {
        "absolute_delta_error": 0.004182525248908886,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_size",
        "predicted_delta": 0.010000000000000002,
        "resolved": true,
        "true_delta": 0.014182525248908888
      },
      {
        "absolute_delta_error": 0.0009109227640003992,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.020000000000000018,
        "resolved": false,
        "true_delta": 0.01908907723599962
      },
      {
        "absolute_delta_error": 0.09103124947311264,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_yield",
        "predicted_delta": 0.12000000000000005,
        "resolved": true,
        "true_delta": 0.02896875052688741
      },
      {
        "absolute_delta_error": 0.023942953078098683,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_purity",
        "predicted_delta": -0.029999999999999916,
        "resolved": false,
        "true_delta": -0.006057046921901232
      },
      {
        "absolute_delta_error": 0.043426352835710225,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_size",
        "predicted_delta": -0.07,
        "resolved": true,
        "true_delta": -0.026573647164289782
      },
      {
        "absolute_delta_error": 0.24090822043533588,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.35,
        "resolved": true,
        "true_delta": 0.5909082204353359
      }
    ],
    "failures": [],
    "metrics": {
      "crystal_fines_fraction": {
        "coverage80": 0.75,
        "interval_score80": 0.7971011005122404,
        "interval_width": 0.31583333333333335,
        "mae": 0.13532456313270644,
        "n": 12,
        "planned": 12
      },
      "crystal_purity": {
        "coverage80": 1.0,
        "interval_score80": 0.10166666666666664,
        "interval_width": 0.10166666666666664,
        "mae": 0.030156569292391817,
        "n": 12,
        "planned": 12
      },
      "crystal_size": {
        "coverage80": 0.9166666666666666,
        "interval_score80": 0.12637551329063945,
        "interval_width": 0.12416666666666666,
        "mae": 0.03042999945291951,
        "n": 12,
        "planned": 12
      },
      "crystal_yield": {
        "coverage80": 0.4166666666666667,
        "interval_score80": 0.48111150100781136,
        "interval_width": 0.24083333333333334,
        "mae": 0.11634492350248803,
        "n": 12,
        "planned": 12
      }
    },
    "quality": {
      "balanced_accuracy": 0.8333333333333334,
      "false_negative": 1,
      "false_positive": 1,
      "true_negative": 5,
      "true_positive": 5
    },
    "resolved_direction_correct": 11,
    "resolved_direction_n": 14,
    "tie_correct": 3,
    "tie_n": 10,
    "valid": true
  },
  "public_baselines": {
    "available": true,
    "mae": {
      "public_mean": {
        "crystal_fines_fraction": 0.28539295852396884,
        "crystal_purity": 0.004563360779943931,
        "crystal_size": 0.019181442040776143,
        "crystal_yield": 0.10125067273916134
      },
      "public_nearest_neighbor": {
        "crystal_fines_fraction": 0.22649062911403642,
        "crystal_purity": 0.009919998701238062,
        "crystal_size": 0.019737062284267186,
        "crystal_yield": 0.22520546589929039
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
        "cached_input": 976768,
        "input": 1055436,
        "output": 11713,
        "stage": "source",
        "uncached_input": 78668
      },
      {
        "cached_input": 0,
        "input": 36366,
        "output": 2221,
        "stage": "K1",
        "uncached_input": 36366
      },
      {
        "cached_input": 0,
        "input": 47123,
        "output": 3492,
        "stage": "Q",
        "uncached_input": 47123
      },
      {
        "cached_input": 36224,
        "input": 50535,
        "output": 1843,
        "stage": "K2",
        "uncached_input": 14311
      }
    ],
    "total": {
      "cached_input": 1012992,
      "input": 1189460,
      "input_plus_output": 1208729,
      "output": 19269,
      "uncached_input": 176468
    },
    "valid": true
  },
  "elapsed_s": 1009.9839999999967
}
```
