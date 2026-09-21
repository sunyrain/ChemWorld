# C-W03-B24-E-Opaque

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
      "stirring_speed_rpm": 250
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
    "byproduct_signal": 0.2762332856655121,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.4978239834308624,
    "crystal_fines_fraction": 0.9973194003105164,
    "crystal_purity": 0.9805160164833069,
    "crystal_size": 0.05059893801808357,
    "crystal_yield": 0.4347969889640808,
    "degradation_warning": 0.08981538563966751,
    "safety_risk": 0.13940587639808655,
    "score": 0.3934541642665863,
    "selectivity": 0.5612952709197998,
    "virtual_spectrum_summary": 0.1923452466726303,
    "yield": 0.5591270327568054
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
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 285
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 150
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
  "end_step": 27,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.29093337059020996,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5085177421569824,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9807944297790527,
    "crystal_size": 0.0789426937699318,
    "crystal_yield": 0.39520999789237976,
    "degradation_warning": 0.0676366537809372,
    "safety_risk": 0.13471587002277374,
    "score": 0.3838033378124237,
    "selectivity": 0.5418630242347717,
    "virtual_spectrum_summary": 0.19044984877109528,
    "yield": 0.5303794145584106
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
  "end_step": 41,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.3371802866458893,
    "conversion": 0.9961942434310913,
    "cost": 1.0,
    "crystal_csd_quality": 0.49811407923698425,
    "crystal_fines_fraction": 0.9949294924736023,
    "crystal_purity": 0.9744446277618408,
    "crystal_size": 0.04587627947330475,
    "crystal_yield": 0.27430737018585205,
    "degradation_warning": 0.059051912277936935,
    "safety_risk": 0.11892332881689072,
    "score": 0.3211897313594818,
    "selectivity": 0.39065951108932495,
    "virtual_spectrum_summary": 0.21202252805233002,
    "yield": 0.38894471526145935
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
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 285
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
  "end_step": 55,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.28970372676849365,
    "conversion": 0.9886218905448914,
    "cost": 1.0,
    "crystal_csd_quality": 0.5189198851585388,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 1.0,
    "crystal_size": 0.05023853853344917,
    "crystal_yield": 0.4190904200077057,
    "degradation_warning": 0.0829954519867897,
    "safety_risk": 0.1356014758348465,
    "score": 0.39002934098243713,
    "selectivity": 0.5303294062614441,
    "virtual_spectrum_summary": 0.19668500125408173,
    "yield": 0.5165027976036072
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
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 285
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
  "end_step": 69,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.3215392529964447,
    "conversion": 0.9963214993476868,
    "cost": 1.0,
    "crystal_csd_quality": 0.5368121266365051,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.972627580165863,
    "crystal_size": 0.020418772473931313,
    "crystal_yield": 0.42136940360069275,
    "degradation_warning": 0.10377420485019684,
    "safety_risk": 0.15902523696422577,
    "score": 0.3835539221763611,
    "selectivity": 0.5204424262046814,
    "virtual_spectrum_summary": 0.22354497015476227,
    "yield": 0.514281153678894
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
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.02
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 285
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
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 120,
      "target_temperature_K": 300
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
    "byproduct_signal": 0.3245299160480499,
    "conversion": 0.9924304485321045,
    "cost": 1.0,
    "crystal_csd_quality": 0.5111553072929382,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9999901652336121,
    "crystal_size": 0.015673484653234482,
    "crystal_yield": 0.4321829676628113,
    "degradation_warning": 0.11556869745254517,
    "safety_risk": 0.1588924676179886,
    "score": 0.3836776912212372,
    "selectivity": 0.5025067925453186,
    "virtual_spectrum_summary": 0.2304973602294922,
    "yield": 0.5043908357620239
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
      "catalyst": 2,
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
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.005
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 285
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
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 120,
      "target_temperature_K": 300
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
  "end_step": 103,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.3535762131214142,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5304907560348511,
    "crystal_fines_fraction": 0.9868429899215698,
    "crystal_purity": 0.9663133025169373,
    "crystal_size": 0.06115754693746567,
    "crystal_yield": 0.33333662152290344,
    "degradation_warning": 0.07298193871974945,
    "safety_risk": 0.14540833234786987,
    "score": 0.3410641849040985,
    "selectivity": 0.3691098690032959,
    "virtual_spectrum_summary": 0.22730877995491028,
    "yield": 0.39565131068229675
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
      "duration_s": 3600,
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
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 120,
      "target_temperature_K": 300
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
  "end_step": 120,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.3342949151992798,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5732643008232117,
    "crystal_fines_fraction": 0.9869751930236816,
    "crystal_purity": 0.9760639667510986,
    "crystal_size": 0.07139534503221512,
    "crystal_yield": 0.43672704696655273,
    "degradation_warning": 0.1613827645778656,
    "safety_risk": 0.15824708342552185,
    "score": 0.3980087339878082,
    "selectivity": 0.5010645985603333,
    "virtual_spectrum_summary": 0.2564844489097595,
    "yield": 0.49274563789367676
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
      "seed_mass_g": 0.005
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
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
  "end_step": 138,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.46782025694847107,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6883749961853027,
    "crystal_fines_fraction": 0.5149549841880798,
    "crystal_purity": 0.9826671481132507,
    "crystal_size": 0.05334661528468132,
    "crystal_yield": 0.4009922742843628,
    "degradation_warning": 0.22688442468643188,
    "safety_risk": 0.17388540506362915,
    "score": 0.4424395263195038,
    "selectivity": 0.4042784571647644,
    "virtual_spectrum_summary": 0.35939913988113403,
    "yield": 0.41795438528060913
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
      "target_temperature_K": 340
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.001
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
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
  "end_step": 160,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.5121813416481018,
    "conversion": 0.9858242273330688,
    "cost": 1.0,
    "crystal_csd_quality": 0.6510795950889587,
    "crystal_fines_fraction": 0.5342012047767639,
    "crystal_purity": 0.9785189032554626,
    "crystal_size": 0.0678555890917778,
    "crystal_yield": 0.3987453579902649,
    "degradation_warning": 0.2535264492034912,
    "safety_risk": 0.1733131855726242,
    "score": 0.4319751262664795,
    "selectivity": 0.40306273102760315,
    "virtual_spectrum_summary": 0.3957866430282593,
    "yield": 0.4119895398616791
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
      "catalyst": 2,
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
      "target_temperature_K": 310
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
  "end_step": 182,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.5527481436729431,
    "conversion": 0.9990203976631165,
    "cost": 1.0,
    "crystal_csd_quality": 0.728965163230896,
    "crystal_fines_fraction": 0.3241020739078522,
    "crystal_purity": 0.994823694229126,
    "crystal_size": 0.08487559854984283,
    "crystal_yield": 0.2940261662006378,
    "degradation_warning": 0.19099871814250946,
    "safety_risk": 0.1615615338087082,
    "score": 0.4333215057849884,
    "selectivity": 0.3415367305278778,
    "virtual_spectrum_summary": 0.389960914850235,
    "yield": 0.32204684615135193
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
      "solvent": 2,
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
      "target_temperature_K": 340
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
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
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.5448687076568604,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6658568978309631,
    "crystal_fines_fraction": 0.5626621246337891,
    "crystal_purity": 0.9948479533195496,
    "crystal_size": 0.0971953272819519,
    "crystal_yield": 0.3783065676689148,
    "degradation_warning": 0.30634805560112,
    "safety_risk": 0.171791672706604,
    "score": 0.4294374883174896,
    "selectivity": 0.3833240866661072,
    "virtual_spectrum_summary": 0.4375343918800354,
    "yield": 0.38836610317230225
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
      "target_temperature_K": 310
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
      "target_temperature_K": 260
    },
    {
      "duration_s": 14400,
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
  "end_step": 227,
  "lifecycle_index": 13,
  "metrics": {
    "byproduct_signal": 0.4997304677963257,
    "conversion": 0.9972169399261475,
    "cost": 1.0,
    "crystal_csd_quality": 0.6293433308601379,
    "crystal_fines_fraction": 0.5949769020080566,
    "crystal_purity": 0.9709459543228149,
    "crystal_size": 0.07077693194150925,
    "crystal_yield": 0.30934813618659973,
    "degradation_warning": 0.23740944266319275,
    "safety_risk": 0.12369576841592789,
    "score": 0.3921705484390259,
    "selectivity": 0.365321546792984,
    "virtual_spectrum_summary": 0.3816860020160675,
    "yield": 0.3573090136051178
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
      "target_temperature_K": 310
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
      "target_temperature_K": 250
    },
    {
      "duration_s": 14400,
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
  "end_step": 251,
  "lifecycle_index": 14,
  "metrics": {
    "byproduct_signal": 0.5083146095275879,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6325655579566956,
    "crystal_fines_fraction": 0.6131015419960022,
    "crystal_purity": 0.9542868733406067,
    "crystal_size": 0.10686594247817993,
    "crystal_yield": 0.32067999243736267,
    "degradation_warning": 0.23669014871120453,
    "safety_risk": 0.12442391365766525,
    "score": 0.39418551325798035,
    "selectivity": 0.36436542868614197,
    "virtual_spectrum_summary": 0.3860836327075958,
    "yield": 0.35817795991897583
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
      "target_temperature_K": 310
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
      "target_temperature_K": 250
    },
    {
      "duration_s": 14400,
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
  "end_step": 275,
  "lifecycle_index": 15,
  "metrics": {
    "byproduct_signal": 0.49560192227363586,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6492973566055298,
    "crystal_fines_fraction": 0.5429927110671997,
    "crystal_purity": 0.9831746220588684,
    "crystal_size": 0.08313880115747452,
    "crystal_yield": 0.3587599992752075,
    "degradation_warning": 0.22062371671199799,
    "safety_risk": 0.1527058333158493,
    "score": 0.42362380027770996,
    "selectivity": 0.3994778096675873,
    "virtual_spectrum_summary": 0.3718617260456085,
    "yield": 0.4040123522281647
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
      "target_temperature_K": 310
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
      "target_temperature_K": 250
    },
    {
      "duration_s": 14400,
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
  "end_step": 299,
  "lifecycle_index": 16,
  "metrics": {
    "byproduct_signal": 0.6121753454208374,
    "conversion": 0.9885537624359131,
    "cost": 1.0,
    "crystal_csd_quality": 0.5328066945075989,
    "crystal_fines_fraction": 0.6636725664138794,
    "crystal_purity": 0.9695932865142822,
    "crystal_size": 0.07408224791288376,
    "crystal_yield": 0.22159543633460999,
    "degradation_warning": 0.3102332651615143,
    "safety_risk": 0.16692392528057098,
    "score": 0.321021169424057,
    "selectivity": 0.25347164273262024,
    "virtual_spectrum_summary": 0.4763014018535614,
    "yield": 0.2518262267112732
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
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
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
  "end_step": 321,
  "lifecycle_index": 17,
  "metrics": {
    "byproduct_signal": 0.5006263852119446,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6694109439849854,
    "crystal_fines_fraction": 0.47874975204467773,
    "crystal_purity": 1.0,
    "crystal_size": 0.06685725599527359,
    "crystal_yield": 0.39863860607147217,
    "degradation_warning": 0.23934143781661987,
    "safety_risk": 0.17419473826885223,
    "score": 0.4494328796863556,
    "selectivity": 0.4223875105381012,
    "virtual_spectrum_summary": 0.3830481767654419,
    "yield": 0.4325457811355591
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
      "target_temperature_K": 340
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
  "end_step": 343,
  "lifecycle_index": 18,
  "metrics": {
    "byproduct_signal": 0.4978533089160919,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6824326515197754,
    "crystal_fines_fraction": 0.5349382758140564,
    "crystal_purity": 0.9957056641578674,
    "crystal_size": 0.11879680305719376,
    "crystal_yield": 0.3845115005970001,
    "degradation_warning": 0.24360398948192596,
    "safety_risk": 0.1738359034061432,
    "score": 0.4479247033596039,
    "selectivity": 0.4238516092300415,
    "virtual_spectrum_summary": 0.38344112038612366,
    "yield": 0.4372585713863373
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
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
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
  "lifecycle_index": 19,
  "metrics": {
    "byproduct_signal": 0.4671902060508728,
    "conversion": 0.9909035563468933,
    "cost": 1.0,
    "crystal_csd_quality": 0.6824358105659485,
    "crystal_fines_fraction": 0.48423537611961365,
    "crystal_purity": 0.9744015336036682,
    "crystal_size": 0.056587375700473785,
    "crystal_yield": 0.39695316553115845,
    "degradation_warning": 0.22306907176971436,
    "safety_risk": 0.1743694543838501,
    "score": 0.4460311830043793,
    "selectivity": 0.4339592754840851,
    "virtual_spectrum_summary": 0.3573356866836548,
    "yield": 0.4375460743904114
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
      "target_temperature_K": 310
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
  "end_step": 383,
  "lifecycle_index": 20,
  "metrics": {
    "byproduct_signal": 0.42966020107269287,
    "conversion": 0.9934656023979187,
    "cost": 1.0,
    "crystal_csd_quality": 0.5996696352958679,
    "crystal_fines_fraction": 0.6564046144485474,
    "crystal_purity": 0.9925298094749451,
    "crystal_size": 0.07098449021577835,
    "crystal_yield": 0.44770359992980957,
    "degradation_warning": 0.17202523350715637,
    "safety_risk": 0.18153589963912964,
    "score": 0.4397048056125641,
    "selectivity": 0.5009632706642151,
    "virtual_spectrum_summary": 0.31372445821762085,
    "yield": 0.4846414625644684
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
      "target_temperature_K": 320
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
  "end_step": 405,
  "lifecycle_index": 21,
  "metrics": {
    "byproduct_signal": 0.4756994843482971,
    "conversion": 0.9894089102745056,
    "cost": 1.0,
    "crystal_csd_quality": 0.4916962683200836,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.98853600025177,
    "crystal_size": 0.04734257608652115,
    "crystal_yield": 0.35450372099876404,
    "degradation_warning": 0.19606399536132812,
    "safety_risk": 0.16815851628780365,
    "score": 0.33846908807754517,
    "selectivity": 0.3729465901851654,
    "virtual_spectrum_summary": 0.3498634994029999,
    "yield": 0.3922238349914551
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
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1800,
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
      "target_temperature_K": 310
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 290
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
  "end_step": 434,
  "lifecycle_index": 22,
  "metrics": {
    "byproduct_signal": 0.4528898000717163,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6018452048301697,
    "crystal_fines_fraction": 0.6462544798851013,
    "crystal_purity": 1.0,
    "crystal_size": 0.07012181729078293,
    "crystal_yield": 0.4482586681842804,
    "degradation_warning": 0.1747836023569107,
    "safety_risk": 0.18150416016578674,
    "score": 0.44104352593421936,
    "selectivity": 0.4795052707195282,
    "virtual_spectrum_summary": 0.3277420103549957,
    "yield": 0.480784147977829
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
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 2700,
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
      "target_temperature_K": 310
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
  "end_step": 456,
  "lifecycle_index": 23,
  "metrics": {
    "byproduct_signal": 0.46186769008636475,
    "conversion": 0.9950222373008728,
    "cost": 1.0,
    "crystal_csd_quality": 0.7136408686637878,
    "crystal_fines_fraction": 0.39969879388809204,
    "crystal_purity": 0.9974932670593262,
    "crystal_size": 0.09509006142616272,
    "crystal_yield": 0.4123837649822235,
    "degradation_warning": 0.1981266289949417,
    "safety_risk": 0.17777718603610992,
    "score": 0.47880229353904724,
    "selectivity": 0.4664326310157776,
    "virtual_spectrum_summary": 0.343184232711792,
    "yield": 0.46819087862968445
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
      "catalyst": 0,
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
      "target_temperature_K": 310
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
  "lifecycle_index": 24,
  "metrics": {
    "byproduct_signal": 0.4599442183971405,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5761340260505676,
    "crystal_fines_fraction": 0.7107252478599548,
    "crystal_purity": 1.0,
    "crystal_size": 0.07129891216754913,
    "crystal_yield": 0.4166165888309479,
    "degradation_warning": 0.19090226292610168,
    "safety_risk": 0.17900292575359344,
    "score": 0.42099693417549133,
    "selectivity": 0.46981361508369446,
    "virtual_spectrum_summary": 0.33887532353401184,
    "yield": 0.479063481092453
  },
  "ordinal": 24
}
```

## K1

```json
{
  "payload": {
    "report": "Objective and recommendation context\n\nThe campaign optimized crystallization-stage, seed-excluded recovery, R_c, subject to crystal purity P \u2265 0.80 and number fraction below 20 \u00b5m, f_20 \u2264 0.50. Batch 23 remained the recommendation: 0.04 mol reagent, 0.08 L solvent-S2, 0.005 mol catalyst-C0; heat toward 340 K for 2700 s at 500 rpm; do not quench; add 0.05 g seed; cool for 14,400 s to 310 K and then for 14,400 s to 295 K; hold five times for 14,400 s at 100 rpm; cool for 14,400 s to 270 K; hold another five times for 14,400 s at 100 rpm; then filter. Its final assay gave R_c = 0.4124, P = 0.9975, and f_20 = 0.3997. Conversion was 0.9950, selectivity 0.4664, and reaction yield 0.4682.\n\nObserved material effects\n\nCatalyst identity had a substantial reaction effect. Under the early solvent-S0 series, final reaction yields for C0, C1, C2, and C3 were approximately 0.559 (batch 1), 0.530 (batch 2), 0.389 (batch 3), and 0.517 (batch 4), respectively, although batch 1 also used a higher reaction temperature and the crystallization histories were not identical. A similar ranking was apparent with solvent-S1: C0 and C1 gave reaction yields near 0.514 and 0.504 in batches 5 and 6, while C2 was lower at 0.396 in batch 7 and C3 gave 0.493 in batch 8. These observations motivated continued use of C0. The interpretation is that C0/C1 favor target formation relative to C2, but a clean intrinsic catalyst ranking is not proven because residence time, temperature, and downstream aging were confounded with several comparisons.\n\nSolvent-S2 was especially useful for particle-quality control under the later no-quench protocol. With C0 and substantial seeding, batches 17, 19, and 23 achieved f_20 values of 0.479, 0.484, and 0.400 while retaining R_c values of 0.399, 0.397, and 0.412. By contrast, late C0 runs using S0, S1, and S3 gave f_20 = 0.595 in batch 13, 0.543 in batch 15, and 0.664 in batch 16. Those comparisons also differed in final temperature and history, so they support a practical S2 effect rather than establishing an isolated solvent property. Because all identities are anonymous benchmark materials, no real-substance polarity or solubility assignment is justified.\n\nReaction\u2013crystallization coupling\n\nA useful reaction approximation is\n\nY_rxn \u2248 X\u00b7S,\n\nwhere X is conversion and S is selectivity. The measured values followed this relationship within assay/process uncertainty; for batch 23, 0.995\u00d70.466 \u2248 0.464 versus measured reaction yield 0.468. An approximate seed-excluded overall recovery from charged reagent would then scale as Y_rxn\u00b7R_c, about 0.193 for batch 23, although the formal optimization variable was R_c alone: recovered target divided by target present before separation.\n\nReaction history affected crystallization, not merely the amount of target available. With C0/S2, shortening the 340 K reaction period to 1800 s increased R_c to 0.448 in batch 20, but f_20 rose to 0.656. The corresponding byproduct and degradation signals, 0.430 and 0.172, were lower than batch 17\u2019s 0.501 and 0.239 after 3600 s, yet batch 17 passed the fines constraint with f_20 = 0.479 and R_c = 0.399. An intermediate 2700 s treatment in batch 23 produced intermediate byproduct/degradation signals (0.462/0.198) but the best qualifying balance. One interpretation is that reaction composition changes solubility, nucleation, or growth inhibition: maximizing chemical yield alone can create a mother liquor that nucleates too many small crystals. This causal mechanism was not directly measured; an alternative is nonlinear or stochastic nucleation near a threshold.\n\nProcess-history dependence\n\nQuenching was the clearest adverse history variable. Batches 1\u20138 were quenched and then cooled; their final f_20 values were approximately 0.987\u20131.000, despite high purities and sometimes good R_c (for example, batch 1 had P = 0.981 and R_c = 0.435 but f_20 = 0.997). The likely interpretation is that the abrupt temperature decrease generated high supersaturation and extensive primary or secondary nucleation. Removing the quench and using staged cooling immediately improved particle populations: batches 9\u201312 gave f_20 values of 0.515, 0.534, 0.324, and 0.563. The data demonstrate the history effect, while the supersaturation explanation remains mechanistic inference because solution concentration was not measured during cooling.\n\nIncreasing the seed charge to 0.05 g was generally associated with better fines control in the no-quench experiments. Batch 11, using 0.05 g, reached f_20 = 0.324, whereas batches 9 and 10, with 0.005 and 0.001 g, gave 0.515 and 0.534. Catalyst identity differed across those batches, so seed causality was not isolated. Later C0/S2 batches using 0.05 g repeatedly approached or passed the specification. A plausible mechanism is that adequate seed surface consumes supersaturation by growth before widespread spontaneous nucleation. Since the metric is number-weighted, excessive seed numbers could instead increase apparent fines; seed-size distribution was unobserved and remains an alternative explanation.\n\nLong aging was not monotonically beneficial. Batch 19, with fewer low-speed holds, gave R_c = 0.397 and f_20 = 0.484, similar to batch 17\u2019s 0.399 and 0.479 after more holds. Batch 24 used a 2400 s reaction and twelve holds but gave f_20 = 0.711 despite R_c = 0.417. Thus, additional time does not guarantee ripening; continued nucleation, attrition even at 100 rpm, or batch variability may offset growth. Likewise, reheating to 290 K and recooling did not rescue the short-reaction material: batch 22 retained high recovery, R_c = 0.448, but f_20 = 0.646. This argues against assuming a simple Ostwald-ripening correction under the tested anneal.\n\nRevisions made during the campaign\n\nThe initial strategy emphasized conversion and deep cooling after quench. It delivered recovery and purity but almost entirely fine particles. The process was therefore revised to eliminate quenching, introduce staged slow cooling, lower agitation, increase seeding, and add long growth holds. Colder endpoints of 250\u2013260 K in batches 13\u201315 did not improve the balance: R_c was 0.309\u20130.359 and f_20 was 0.543\u20130.613. Attention then shifted to solvent-S2 at 270 K. Shortening reaction time raised recovery but failed the fines constraint (batches 20 and 22); the intermediate 2700 s reaction in batch 23 provided a stronger constraint margin than borderline batches 17 and 19 and therefore became the recommendation.\n\nQuality\u2013recovery tradeoff and uncertainty\n\nPurity was not the active limitation: most filtered products had P around 0.95\u20131.00. The unresolved tradeoff was recovery versus fines. The highest observed recoveries, approximately 0.448 in batches 20 and 22, failed f_20 by a wide margin. The best qualifying recovery was 0.412 in batch 23. Batches 17 and 19 also qualified but only narrowly, with f_20 = 0.479 and 0.484. Given the stated final-assay noise scales (about 0.01 for R_c and 0.018 for f_20, plus process uncertainty), their margins are fragile; batch 23\u2019s roughly 0.10 fines margin is materially more credible.\n\nBatch 23 was still a single realization rather than an exact replicate. Its in-process particle result, f_20 = 0.449, differed from the final assay value of 0.400, indicating measurement noise and/or state/context differences. Batch 24\u2019s poor fines result under a nearby recipe also shows that interpolation in reaction time or total aging is unreliable. The mechanism is therefore best treated as an evidence-supported working model: C0 supplies acceptable target formation; S2 and avoidance of quench enable coarse-particle growth; adequate seed and slow staged cooling control nucleation; and reaction residence changes the liquor composition enough to create a nonmonotonic recovery\u2013fines response. Untested alternatives include finer temperature ramps, controlled antisolvent addition, different seed-size distributions, and exact replication around batch 23."
  },
  "failure": null,
  "elapsed_s": 73.03200000000652,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 436224,
    "input_tokens": 531254,
    "output_tokens": 10579,
    "reasoning_output_tokens": 4117
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
          "estimate": 0.35,
          "lower80": 0.18,
          "upper80": 0.56
        },
        "crystal_purity": {
          "estimate": 0.95,
          "lower80": 0.88,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.11,
          "lower80": 0.065,
          "upper80": 0.17
        },
        "crystal_yield": {
          "estimate": 0.38,
          "lower80": 0.25,
          "upper80": 0.5
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q01"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.66,
          "lower80": 0.45,
          "upper80": 0.86
        },
        "crystal_purity": {
          "estimate": 0.91,
          "lower80": 0.81,
          "upper80": 0.97
        },
        "crystal_size": {
          "estimate": 0.07,
          "lower80": 0.032,
          "upper80": 0.12
        },
        "crystal_yield": {
          "estimate": 0.24,
          "lower80": 0.12,
          "upper80": 0.37
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q02"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.76,
          "lower80": 0.56,
          "upper80": 0.93
        },
        "crystal_purity": {
          "estimate": 0.96,
          "lower80": 0.89,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.055,
          "lower80": 0.023,
          "upper80": 0.1
        },
        "crystal_yield": {
          "estimate": 0.3,
          "lower80": 0.18,
          "upper80": 0.43
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q03"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.4,
          "lower80": 0.21,
          "upper80": 0.61
        },
        "crystal_purity": {
          "estimate": 0.97,
          "lower80": 0.91,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.105,
          "lower80": 0.06,
          "upper80": 0.16
        },
        "crystal_yield": {
          "estimate": 0.33,
          "lower80": 0.21,
          "upper80": 0.46
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q04"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.35,
          "lower80": 0.17,
          "upper80": 0.56
        },
        "crystal_purity": {
          "estimate": 0.97,
          "lower80": 0.91,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.115,
          "lower80": 0.067,
          "upper80": 0.175
        },
        "crystal_yield": {
          "estimate": 0.34,
          "lower80": 0.22,
          "upper80": 0.47
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q05"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.86,
          "lower80": 0.7,
          "upper80": 0.97
        },
        "crystal_purity": {
          "estimate": 0.94,
          "lower80": 0.85,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.045,
          "lower80": 0.018,
          "upper80": 0.085
        },
        "crystal_yield": {
          "estimate": 0.38,
          "lower80": 0.25,
          "upper80": 0.51
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q06"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.32,
          "lower80": 0.15,
          "upper80": 0.53
        },
        "crystal_purity": {
          "estimate": 0.97,
          "lower80": 0.91,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.12,
          "lower80": 0.07,
          "upper80": 0.18
        },
        "crystal_yield": {
          "estimate": 0.35,
          "lower80": 0.23,
          "upper80": 0.48
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q07"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.64,
          "lower80": 0.43,
          "upper80": 0.84
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.92,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.07,
          "lower80": 0.033,
          "upper80": 0.12
        },
        "crystal_yield": {
          "estimate": 0.26,
          "lower80": 0.14,
          "upper80": 0.39
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q08"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.45,
          "lower80": 0.22,
          "upper80": 0.7
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.9,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.09,
          "lower80": 0.045,
          "upper80": 0.15
        },
        "crystal_yield": {
          "estimate": 0.015,
          "lower80": 0.0,
          "upper80": 0.055
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q09"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.34,
          "lower80": 0.16,
          "upper80": 0.57
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.91,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.11,
          "lower80": 0.06,
          "upper80": 0.17
        },
        "crystal_yield": {
          "estimate": 0.11,
          "lower80": 0.045,
          "upper80": 0.21
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q10"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.34,
          "lower80": 0.17,
          "upper80": 0.55
        },
        "crystal_purity": {
          "estimate": 0.97,
          "lower80": 0.91,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.115,
          "lower80": 0.067,
          "upper80": 0.175
        },
        "crystal_yield": {
          "estimate": 0.34,
          "lower80": 0.22,
          "upper80": 0.47
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q11"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.67,
          "lower80": 0.46,
          "upper80": 0.86
        },
        "crystal_purity": {
          "estimate": 0.91,
          "lower80": 0.81,
          "upper80": 0.97
        },
        "crystal_size": {
          "estimate": 0.065,
          "lower80": 0.03,
          "upper80": 0.115
        },
        "crystal_yield": {
          "estimate": 0.49,
          "lower80": 0.35,
          "upper80": 0.62
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q12"
      }
    ],
    "rationale": "Q01\u2013Q02 isolates solvent: I expect S1 to retain more target and support seed growth than S3, which performed poorly in the campaign, so Q01 has higher recovery, larger particles, and fewer fines. Q03\u2013Q04 isolates seed loading: 0.045 g should provide enough growth surface to suppress uncontrolled nucleation, whereas 0.001 g should yield a fine-dominated population. Q05\u2013Q06 compares slow ramping with an immediate temperature crash at equal approximate aging time; the crash may slightly increase recovery but should create many persistent fines. Q07\u2013Q08 tests a late 315 K heat cycle: partial dissolution followed by rapid recooling is expected to sacrifice recovery and regenerate fines rather than produce reliable ripening. Q09\u2013Q10 isolates a 7200 s growth hold at 292 K; seeds ensure particles in both, but Q09 should have almost no seed-excluded recovery, while Q10 permits measurable deposition and coarsening. Q11\u2013Q12 doubles reagent concentration: higher supersaturation should increase fractional recovery but overwhelm the fixed seed area, reducing purity and increasing secondary nucleation. Intervals are deliberately broad because these recipes extrapolate to smaller charge, higher reaction temperature, very long ramps, and unreplicated histories; fines predictions are especially uncertain near the 0.50 feasibility boundary."
  },
  "failure": null,
  "elapsed_s": 97.875,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 436224,
    "input_tokens": 575736,
    "output_tokens": 15170,
    "reasoning_output_tokens": 7009
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
    "report": "1. Status of the main claims\n\nSupported by direct observations:\n- Purity was not the active constraint. Every cited optimized or near-optimized filtered batch had purity well above 0.80; for example, batches 17, 19, and 23 gave 1.000, 0.974, and 0.997. The operative constraint was generally fines.\n- A recovery\u2013fines tradeoff was observed. Batches 20 and 22 reached the largest recoveries, about 0.448, but failed the fines limit at 0.656 and 0.646. Batch 23 sacrificed some recovery, to 0.412, while passing at 0.400.\n- Process history mattered. Quenched batches 1\u20138 all produced extremely fine populations, with final fines around 0.987\u20131.000. Later no-quench, staged-cooling batches could pass: batch 11 gave 0.324, batch 17 gave 0.479, batch 19 gave 0.484, and batch 23 gave 0.400. This is strong observational support for a history effect, although quench removal was bundled with slower cooling, longer aging, and other changes.\n- More aging or colder endpoints were not monotonically beneficial. Batches 13\u201315, ending at 250\u2013260 K, still had fines of 0.543\u20130.613 and recoveries of only 0.309\u20130.359. Batch 19 used fewer holds than batch 17 but gave nearly the same recovery and fines. Batch 24 used a nearby recipe with extensive aging yet gave fines of 0.711.\n- The tested anneal did not rescue a fines-prone process. Batch 22, reheated to 290 K and recooled, retained high recovery but still had fines of 0.646.\n- Reaction residence showed a nonmonotonic association with product quality in the closely related C0/S2 series. At 1800, 2700, and 3600 s, batches 20, 23, and 17 gave recoveries of 0.448, 0.412, and 0.399 and fines of 0.656, 0.400, and 0.479. Thus, the intermediate residence was the best observed compromise rather than an endpoint of a simple monotonic trend.\n\nSupported only provisionally or with confounding:\n- Solvent-S2 appeared useful for fines control, but solvent was not isolated under one identical protocol. The favorable S2 batches 17, 19, and 23 differed historically from S0/S1/S3 comparisons such as batches 13, 15, and 16. The practical association is observed; a solvent-specific solubility mechanism is interpretation.\n- C0/C1 generally outperformed C2 in reaction yield in batches 1\u20138, but temperature and downstream histories were not fully matched. A catalyst effect is plausible, but the intrinsic ranking is not cleanly identified.\n- Heavy seeding appeared compatible with good fines control: batch 11 with 0.05 g seed achieved fines of 0.324, and later qualifying C0/S2 batches also used 0.05 g. However, catalyst and process history were confounded. Unseeded batch 12 still formed particles and had fines of 0.563, only modestly worse than some lightly seeded batches, so the stronger claim that seed amount itself suppressed nucleation was not established.\n\nContradicted or qualified:\n- A simple \u201clonger aging causes ripening and therefore fewer fines\u201d account is contradicted by batches 17 versus 19 and especially batch 24. Time alone was insufficient.\n- A simple \u201cdeeper cooling increases useful recovery\u201d account is contradicted by batches 13\u201315.\n- A generic \u201creheat\u2013recool annealing repairs fines\u201d claim is contradicted for the tested cycle by batch 22.\n- The idea that lower byproduct or degradation signals necessarily improve crystal quality is contradicted by batch 20: its signals were lower than batch 17\u2019s, yet its fines were substantially worse.\n\nStill untested:\n- Supersaturation-driven primary nucleation, growth inhibition by impurities, attrition, and Ostwald ripening were inferred rather than measured. No concentration, supersaturation, nucleation-rate, or seed-size-distribution data were collected.\n- It remains unknown whether batch 23 represents a reproducible residence-time optimum or a favorable stochastic nucleation realization. It was not exactly replicated.\n- The cause of the difference between batch 23\u2019s in-process particle fines estimate of 0.449 and final-assay value of 0.400 is unresolved; instrument noise and physical evolution or sampling context are both possible.\n- Scale and concentration effects in the held-out recipes remain extrapolations because the campaign mainly used 0.04 mol reagent in 0.08 L solvent, whereas the predictions use much smaller charges and volumes.\n\n2. One additional experiment\n\nI would exactly repeat batch 23, while adding a single HPLC measurement immediately before seeding, then complete the same crystallization and final assay. The small analytical sample would be recorded, and no process settings would otherwise change.\n\nThis would distinguish two leading explanations. Under a reproducible residence-time/composition optimum, the pre-seeding reaction profile should be close to batch 23\u2019s final reaction signature and the final material should again have recovery near 0.41, purity near 1, and fines clearly below 0.50. That result would support the interpretation that 2700 s creates a reliably favorable liquor composition for seeded growth.\n\nUnder a stochastic or threshold-nucleation explanation, similar HPLC chemistry could be followed by substantially different fines, potentially resembling batch 20 or 24. That would show that the apparent optimum is dominated by crystallization variability rather than reaction composition. Conversely, if both the HPLC profile and crystal outcome shift together, reaction-stage variability or composition-dependent nucleation would be favored. One experiment cannot fully separate all causes, but this design simultaneously supplies the missing exact replicate and a reaction-state diagnostic.\n\n3. Least effectively used observation and least reliable prediction\n\nThe account used batch 12 least effectively. It was an unseeded staged-cooling experiment that nevertheless formed particles, with recovery 0.378, purity 0.995, and fines 0.563. I emphasized adequate seed surface as a mechanism for suppressing spontaneous nucleation, but batch 12 shows that substantial crystallization occurs without added seed and that its fines penalty was not universally catastrophic. Because its catalyst differed from the principal C0 comparisons, it does not disprove a seed effect, but it should have been given more weight as evidence against a simple seed-controlled mechanism.\n\nQ09 is the least reliable held-out prediction. It allows only 60 s at 292 K after adding seed, far outside the campaign\u2019s crystallization histories. The expected solids may consist almost entirely of introduced seed while the requested yield explicitly excludes seed mass. Consequently, particles_present is plausible, but seed-excluded yield should be near zero and the predicted size and fines depend strongly on the unknown seed-size distribution and on whether negligible new deposition changes the measured number distribution. Calling Q09 quality-feasible is therefore especially fragile. Q12 is also uncertain because it doubles concentration, but Q09 has the weaker empirical analogue and the most ambiguous relationship between visible particles and newly recovered product."
  },
  "failure": null,
  "elapsed_s": 53.51600000000326,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 439680,
    "input_tokens": 617914,
    "output_tokens": 17391,
    "reasoning_output_tokens": 7661
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
    "selection_rationale": "Highest observed seed-excluded crystal recovery among completed batches meeting both constraints: crystal_yield 0.412, crystal_purity 0.997, and fines fraction 0.400. The no-quench, seeded, staged slow-cooling process also gave the strongest qualifying particle-quality result."
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
        "catalyst": 0,
        "catalyst_amount_mol": 0.005,
        "operation": "add_catalyst"
      },
      {
        "duration_s": 2700,
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
        "target_temperature_K": 310
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
    "source_attempts": 22
  },
  "prediction_evaluation": {
    "contrasts": [
      {
        "absolute_delta_error": 0.009891510015443417,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_yield",
        "predicted_delta": -0.14,
        "resolved": true,
        "true_delta": -0.14989151001544343
      },
      {
        "absolute_delta_error": 0.04064587911515061,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_purity",
        "predicted_delta": -0.039999999999999925,
        "resolved": false,
        "true_delta": 0.0006458791151506826
      },
      {
        "absolute_delta_error": 0.059380401500635005,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_size",
        "predicted_delta": -0.039999999999999994,
        "resolved": true,
        "true_delta": 0.01938040150063501
      },
      {
        "absolute_delta_error": 0.8383138299289018,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.31000000000000005,
        "resolved": true,
        "true_delta": -0.5283138299289017
      },
      {
        "absolute_delta_error": 0.03015921777357053,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_yield",
        "predicted_delta": 0.030000000000000027,
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
        "absolute_delta_error": 0.05718557110203586,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_size",
        "predicted_delta": 0.049999999999999996,
        "resolved": true,
        "true_delta": -0.007185571102035868
      },
      {
        "absolute_delta_error": 0.5242669082202976,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.36,
        "resolved": true,
        "true_delta": 0.16426690822029769
      },
      {
        "absolute_delta_error": 0.03954785756482607,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_yield",
        "predicted_delta": 0.03999999999999998,
        "resolved": false,
        "true_delta": 0.0004521424351739134
      },
      {
        "absolute_delta_error": 0.026445289569308805,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.030000000000000027,
        "resolved": false,
        "true_delta": -0.0035547104306912214
      },
      {
        "absolute_delta_error": 0.026686547334296984,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_size",
        "predicted_delta": -0.07,
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
        "absolute_delta_error": 0.13437670725156423,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_yield",
        "predicted_delta": -0.08999999999999997,
        "resolved": true,
        "true_delta": 0.04437670725156426
      },
      {
        "absolute_delta_error": 0.021056182794199185,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_purity",
        "predicted_delta": 0.010000000000000009,
        "resolved": true,
        "true_delta": -0.011056182794199176
      },
      {
        "absolute_delta_error": 0.010294418729356991,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_size",
        "predicted_delta": -0.04999999999999999,
        "resolved": true,
        "true_delta": -0.039705581270643
      },
      {
        "absolute_delta_error": 0.3403702872401259,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.32,
        "resolved": true,
        "true_delta": 0.6603702872401259
      },
      {
        "absolute_delta_error": 0.0004828156979978654,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_yield",
        "predicted_delta": 0.095,
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
        "absolute_delta_error": 0.006101832298345225,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_size",
        "predicted_delta": 0.020000000000000004,
        "resolved": true,
        "true_delta": 0.013898167701654779
      },
      {
        "absolute_delta_error": 0.17539272978183873,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.10999999999999999,
        "resolved": false,
        "true_delta": 0.06539272978183874
      },
      {
        "absolute_delta_error": 0.13504321303990105,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_yield",
        "predicted_delta": 0.14999999999999997,
        "resolved": false,
        "true_delta": 0.014956786960098917
      },
      {
        "absolute_delta_error": 0.05482839724908717,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_purity",
        "predicted_delta": -0.05999999999999994,
        "resolved": false,
        "true_delta": -0.005171602750912774
      },
      {
        "absolute_delta_error": 0.024356873957321057,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_size",
        "predicted_delta": -0.05,
        "resolved": true,
        "true_delta": -0.025643126042678946
      },
      {
        "absolute_delta_error": 0.27598956676040814,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.33,
        "resolved": true,
        "true_delta": 0.6059895667604082
      }
    ],
    "failures": [],
    "metrics": {
      "crystal_fines_fraction": {
        "coverage80": 0.4166666666666667,
        "interval_score80": 1.8373907668177614,
        "interval_width": 0.38999999999999996,
        "mae": 0.28577363791099286,
        "n": 12,
        "planned": 12
      },
      "crystal_purity": {
        "coverage80": 0.8333333333333334,
        "interval_score80": 0.13372972420117354,
        "interval_width": 0.1083333333333333,
        "mae": 0.02887779145776695,
        "n": 12,
        "planned": 12
      },
      "crystal_size": {
        "coverage80": 0.75,
        "interval_score80": 0.1201339145404664,
        "interval_width": 0.09583333333333333,
        "mae": 0.028601302385732028,
        "n": 12,
        "planned": 12
      },
      "crystal_yield": {
        "coverage80": 0.75,
        "interval_score80": 0.3345254270008256,
        "interval_width": 0.22916666666666666,
        "mae": 0.0871435918491909,
        "n": 12,
        "planned": 12
      }
    },
    "quality": {
      "balanced_accuracy": 0.5833333333333333,
      "false_negative": 2,
      "false_positive": 3,
      "true_negative": 3,
      "true_positive": 4
    },
    "resolved_direction_correct": 9,
    "resolved_direction_n": 16,
    "tie_correct": 0,
    "tie_n": 8,
    "valid": true
  },
  "public_baselines": {
    "available": true,
    "mae": {
      "public_mean": {
        "crystal_fines_fraction": 0.3071534143698245,
        "crystal_purity": 0.004672700973418681,
        "crystal_size": 0.018999905288188203,
        "crystal_yield": 0.1689264386418183
      },
      "public_nearest_neighbor": {
        "crystal_fines_fraction": 0.2807277159765969,
        "crystal_purity": 0.006602851709569581,
        "crystal_size": 0.02436344823841231,
        "crystal_yield": 0.18761579414434426
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
        "cached_input": 436224,
        "input": 498598,
        "output": 7289,
        "stage": "source",
        "uncached_input": 62374
      },
      {
        "cached_input": 0,
        "input": 32656,
        "output": 3290,
        "stage": "K1",
        "uncached_input": 32656
      },
      {
        "cached_input": 0,
        "input": 44482,
        "output": 4591,
        "stage": "Q",
        "uncached_input": 44482
      },
      {
        "cached_input": 3456,
        "input": 42178,
        "output": 2221,
        "stage": "K2",
        "uncached_input": 38722
      }
    ],
    "total": {
      "cached_input": 439680,
      "input": 617914,
      "input_plus_output": 635305,
      "output": 17391,
      "uncached_input": 178234
    },
    "valid": true
  },
  "elapsed_s": 942.9230000000098
}
```
