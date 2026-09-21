# C-W05-B24-E-MisIndexed

Status: completed

## Batch 1

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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 350
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
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 260
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
  "end_step": 13,
  "lifecycle_index": 1,
  "metrics": {
    "byproduct_signal": 0.3583585023880005,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5414952039718628,
    "crystal_fines_fraction": 0.9973161816596985,
    "crystal_purity": 0.9853997826576233,
    "crystal_size": 0.04850234091281891,
    "crystal_yield": 0.36936548352241516,
    "degradation_warning": 0.1365693062543869,
    "safety_risk": 0.1704184114933014,
    "score": 0.3632034361362457,
    "selectivity": 0.44685834646224976,
    "virtual_spectrum_summary": 0.2585533559322357,
    "yield": 0.4446955919265747
  },
  "ordinal": 1
}
```

## Batch 2

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
      "seed_mass_g": 0.001
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
  "end_step": 25,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.2886554002761841,
    "conversion": 0.9863571524620056,
    "cost": 1.0,
    "crystal_csd_quality": 0.5572382211685181,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9752551317214966,
    "crystal_size": 0.07153679430484772,
    "crystal_yield": 0.37202292680740356,
    "degradation_warning": 0.04237132892012596,
    "safety_risk": 0.17218616604804993,
    "score": 0.37337440252304077,
    "selectivity": 0.4942834675312042,
    "virtual_spectrum_summary": 0.17782756686210632,
    "yield": 0.4754103124141693
  },
  "ordinal": 2
}
```

## Batch 3

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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
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
  "end_step": 37,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.30026519298553467,
    "conversion": 0.9916462898254395,
    "cost": 1.0,
    "crystal_csd_quality": 0.5472090840339661,
    "crystal_fines_fraction": 0.9949313998222351,
    "crystal_purity": 0.9875808358192444,
    "crystal_size": 0.033838897943496704,
    "crystal_yield": 0.3427625894546509,
    "degradation_warning": 0.060089386999607086,
    "safety_risk": 0.16896504163742065,
    "score": 0.3578585982322693,
    "selectivity": 0.45374324917793274,
    "virtual_spectrum_summary": 0.19218608736991882,
    "yield": 0.4498353898525238
  },
  "ordinal": 3
}
```

## Batch 4

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
      "seed_mass_g": 0.001
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
  "end_step": 49,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.32228466868400574,
    "conversion": 0.9651637077331543,
    "cost": 1.0,
    "crystal_csd_quality": 0.5458671450614929,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9991623163223267,
    "crystal_size": 0.05051957070827484,
    "crystal_yield": 0.27933308482170105,
    "degradation_warning": 0.010895715095102787,
    "safety_risk": 0.15830546617507935,
    "score": 0.3293219208717346,
    "selectivity": 0.38145244121551514,
    "virtual_spectrum_summary": 0.1821596324443817,
    "yield": 0.35884013772010803
  },
  "ordinal": 4
}
```

## Batch 5

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
      "seed_mass_g": 0.001
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
  "end_step": 61,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.2900198996067047,
    "conversion": 0.9844870567321777,
    "cost": 1.0,
    "crystal_csd_quality": 0.547847330570221,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9759315252304077,
    "crystal_size": 0.020349973812699318,
    "crystal_yield": 0.42502954602241516,
    "degradation_warning": 0.07469727098941803,
    "safety_risk": 0.17792090773582458,
    "score": 0.3894936740398407,
    "selectivity": 0.5440426468849182,
    "virtual_spectrum_summary": 0.1931247115135193,
    "yield": 0.5316058397293091
  },
  "ordinal": 5
}
```

## Batch 6

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
      "seed_mass_g": 0.001
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
  "end_step": 73,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.2657686173915863,
    "conversion": 0.9750926494598389,
    "cost": 1.0,
    "crystal_csd_quality": 0.5003889799118042,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 1.0,
    "crystal_size": 0.021765002980828285,
    "crystal_yield": 0.38296666741371155,
    "degradation_warning": 0.03525756672024727,
    "safety_risk": 0.13047680258750916,
    "score": 0.3722977042198181,
    "selectivity": 0.5145184993743896,
    "virtual_spectrum_summary": 0.1620386391878128,
    "yield": 0.5073744654655457
  },
  "ordinal": 6
}
```

## Batch 7

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
      "seed_mass_g": 0.001
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
  "end_step": 85,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.26529109477996826,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5420905947685242,
    "crystal_fines_fraction": 0.9868552684783936,
    "crystal_purity": 0.9784300923347473,
    "crystal_size": 0.053594738245010376,
    "crystal_yield": 0.434309720993042,
    "degradation_warning": 0.03931410610675812,
    "safety_risk": 0.1591368168592453,
    "score": 0.3931266665458679,
    "selectivity": 0.49659597873687744,
    "virtual_spectrum_summary": 0.16360145807266235,
    "yield": 0.5214397311210632
  },
  "ordinal": 7
}
```

## Batch 8

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
      "seed_mass_g": 0.001
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
  "end_step": 97,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.3087940812110901,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5176419019699097,
    "crystal_fines_fraction": 0.9869726896286011,
    "crystal_purity": 0.9636134505271912,
    "crystal_size": 0.08008227497339249,
    "crystal_yield": 0.3028777241706848,
    "degradation_warning": 0.05264599993824959,
    "safety_risk": 0.17449945211410522,
    "score": 0.33866822719573975,
    "selectivity": 0.43726974725723267,
    "virtual_spectrum_summary": 0.1935274451971054,
    "yield": 0.42770901322364807
  },
  "ordinal": 8
}
```

## Batch 9

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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 310
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
  "end_step": 109,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.3771790564060211,
    "conversion": 0.99974125623703,
    "cost": 1.0,
    "crystal_csd_quality": 0.524911642074585,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.974173367023468,
    "crystal_size": 0.0347684882581234,
    "crystal_yield": 0.24952420592308044,
    "degradation_warning": 0.057167623192071915,
    "safety_risk": 0.15487460792064667,
    "score": 0.3035416901111603,
    "selectivity": 0.3114083707332611,
    "virtual_spectrum_summary": 0.2331739068031311,
    "yield": 0.324719101190567
  },
  "ordinal": 9
}
```

## Batch 10

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
    },
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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
    },
    {
      "operation": "quench"
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
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
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
  "end_step": 172,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.13535407185554504,
    "conversion": 0.4798988401889801,
    "cost": 1.0,
    "crystal_csd_quality": 0.5128105282783508,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.977763831615448,
    "crystal_size": 0.036593787372112274,
    "crystal_yield": 0.2476119101047516,
    "degradation_warning": 0.046854905784130096,
    "safety_risk": 0.18009565770626068,
    "score": 0.29310843348503113,
    "selectivity": 0.5259039402008057,
    "virtual_spectrum_summary": 0.09552944451570511,
    "yield": 0.26656574010849
  },
  "ordinal": 10
}
```

## Batch 11

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
      "catalyst": 3,
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
      "seed_mass_g": 0.001
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
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 292
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
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 292
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
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 292
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
  "end_step": 193,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.2432912439107895,
    "conversion": 0.9925931692123413,
    "cost": 1.0,
    "crystal_csd_quality": 0.5346749424934387,
    "crystal_fines_fraction": 0.9936854839324951,
    "crystal_purity": 0.9919599294662476,
    "crystal_size": 0.03709884360432625,
    "crystal_yield": 0.49425920844078064,
    "degradation_warning": 0.04923702031373978,
    "safety_risk": 0.1684918850660324,
    "score": 0.42166584730148315,
    "selectivity": 0.6110161542892456,
    "virtual_spectrum_summary": 0.1559668481349945,
    "yield": 0.5876811742782593
  },
  "ordinal": 11
}
```

## Batch 12

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.01,
      "operation": "add_reagent"
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.002,
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
      "seed_mass_g": 0.001
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
  "end_step": 207,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.1625165045261383,
    "conversion": 0.7923863530158997,
    "cost": 1.0,
    "crystal_csd_quality": 0.6071947813034058,
    "crystal_fines_fraction": 0.6440631151199341,
    "crystal_purity": 0.9931605458259583,
    "crystal_size": 0.09265611320734024,
    "crystal_yield": 0.40830737352371216,
    "degradation_warning": 0.06639852374792099,
    "safety_risk": 0.095921091735363,
    "score": 0.45070680975914,
    "selectivity": 0.6636311411857605,
    "virtual_spectrum_summary": 0.1192634180188179,
    "yield": 0.5272645354270935
  },
  "ordinal": 12
}
```

## Batch 13

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.003,
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
      "seed_mass_g": 0.001
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
  "end_step": 221,
  "lifecycle_index": 13,
  "metrics": {
    "byproduct_signal": 0.22462497651576996,
    "conversion": 0.915195643901825,
    "cost": 1.0,
    "crystal_csd_quality": 0.5062480568885803,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9769936203956604,
    "crystal_size": 0.06252145767211914,
    "crystal_yield": 0.4597840905189514,
    "degradation_warning": 0.06626787781715393,
    "safety_risk": 0.12412712723016739,
    "score": 0.4001135230064392,
    "selectivity": 0.5957314968109131,
    "virtual_spectrum_summary": 0.15336428582668304,
    "yield": 0.539294958114624
  },
  "ordinal": 13
}
```

## Batch 14

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.03,
      "operation": "add_reagent"
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.004,
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
      "seed_mass_g": 0.001
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
  "end_step": 235,
  "lifecycle_index": 14,
  "metrics": {
    "byproduct_signal": 0.26825159788131714,
    "conversion": 0.9754342436790466,
    "cost": 1.0,
    "crystal_csd_quality": 0.5605947971343994,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9611496925354004,
    "crystal_size": 0.08428648114204407,
    "crystal_yield": 0.4750432074069977,
    "degradation_warning": 0.0755947008728981,
    "safety_risk": 0.15233011543750763,
    "score": 0.4092406928539276,
    "selectivity": 0.5507670640945435,
    "virtual_spectrum_summary": 0.18155598640441895,
    "yield": 0.5273133516311646
  },
  "ordinal": 14
}
```

## Batch 15

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.005,
      "operation": "add_reagent"
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.001,
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
      "seed_mass_g": 0.001
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
  "lifecycle_index": 15,
  "metrics": {
    "byproduct_signal": 0.1090783178806305,
    "conversion": 0.5329506397247314,
    "cost": 1.0,
    "crystal_csd_quality": 0.4408288300037384,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9863744974136353,
    "crystal_size": 0.06046045199036598,
    "crystal_yield": 0.15294042229652405,
    "degradation_warning": 0.03549303859472275,
    "safety_risk": 0.0803571566939354,
    "score": 0.29419997334480286,
    "selectivity": 0.7254990339279175,
    "virtual_spectrum_summary": 0.07596494257450104,
    "yield": 0.3866640627384186
  },
  "ordinal": 15
}
```

## Batch 16

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.0075,
      "operation": "add_reagent"
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.0015,
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
      "seed_mass_g": 0.001
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
  "end_step": 267,
  "lifecycle_index": 16,
  "metrics": {
    "byproduct_signal": 0.1384562849998474,
    "conversion": 0.6716490983963013,
    "cost": 1.0,
    "crystal_csd_quality": 0.4782841205596924,
    "crystal_fines_fraction": 0.8443064093589783,
    "crystal_purity": 0.9763467907905579,
    "crystal_size": 0.06780700385570526,
    "crystal_yield": 0.31030943989753723,
    "degradation_warning": 0.058358483016490936,
    "safety_risk": 0.0878056213259697,
    "score": 0.3660608232021332,
    "selectivity": 0.6887058615684509,
    "virtual_spectrum_summary": 0.10241226851940155,
    "yield": 0.4668777585029602
  },
  "ordinal": 16
}
```

## Batch 17

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.020000000000000004
    },
    {
      "amount_mol": 0.01,
      "operation": "add_reagent"
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.002,
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
      "seed_mass_g": 0.001
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
  "end_step": 284,
  "lifecycle_index": 17,
  "metrics": {
    "byproduct_signal": 0.15852107107639313,
    "conversion": 0.706497073173523,
    "cost": 1.0,
    "crystal_csd_quality": 0.5301943421363831,
    "crystal_fines_fraction": 0.7807846665382385,
    "crystal_purity": 0.99786376953125,
    "crystal_size": 0.06034355238080025,
    "crystal_yield": 0.3423493802547455,
    "degradation_warning": 0.054159604012966156,
    "safety_risk": 0.09289111942052841,
    "score": 0.39679858088493347,
    "selectivity": 0.6804418563842773,
    "virtual_spectrum_summary": 0.11155840754508972,
    "yield": 0.4860750138759613
  },
  "ordinal": 17
}
```

## Batch 18

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.01,
      "operation": "add_reagent"
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.002,
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
      "seed_mass_g": 0.001
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
  "end_step": 296,
  "lifecycle_index": 18,
  "metrics": {
    "byproduct_signal": 0.1556723266839981,
    "conversion": 0.7955814003944397,
    "cost": 1.0,
    "crystal_csd_quality": 0.6065215468406677,
    "crystal_fines_fraction": 0.6836602091789246,
    "crystal_purity": 0.9936212301254272,
    "crystal_size": 0.1145561933517456,
    "crystal_yield": 0.29343855381011963,
    "degradation_warning": 0.05769761651754379,
    "safety_risk": 0.09525511413812637,
    "score": 0.4220684766769409,
    "selectivity": 0.6674923300743103,
    "virtual_spectrum_summary": 0.11158370971679688,
    "yield": 0.5394906401634216
  },
  "ordinal": 18
}
```

## Batch 19

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.01,
      "operation": "add_reagent"
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.002,
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
      "seed_mass_g": 0.001
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
  "end_step": 308,
  "lifecycle_index": 19,
  "metrics": {
    "byproduct_signal": 0.17649321258068085,
    "conversion": 0.780299961566925,
    "cost": 1.0,
    "crystal_csd_quality": 0.6127541661262512,
    "crystal_fines_fraction": 0.6244259476661682,
    "crystal_purity": 0.9723016023635864,
    "crystal_size": 0.054073262959718704,
    "crystal_yield": 0.3636103570461273,
    "degradation_warning": 0.05239839106798172,
    "safety_risk": 0.09574060142040253,
    "score": 0.43473106622695923,
    "selectivity": 0.666968584060669,
    "virtual_spectrum_summary": 0.12065054476261139,
    "yield": 0.5291467308998108
  },
  "ordinal": 19
}
```

## Batch 20

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.01,
      "operation": "add_reagent"
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.002,
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
      "seed_mass_g": 0.001
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 255
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
  "end_step": 320,
  "lifecycle_index": 20,
  "metrics": {
    "byproduct_signal": 0.17419520020484924,
    "conversion": 0.7828619480133057,
    "cost": 1.0,
    "crystal_csd_quality": 0.6039507389068604,
    "crystal_fines_fraction": 0.6272038221359253,
    "crystal_purity": 0.9909360408782959,
    "crystal_size": 0.06825835257768631,
    "crystal_yield": 0.3791041374206543,
    "degradation_warning": 0.05652229115366936,
    "safety_risk": 0.09586379677057266,
    "score": 0.44145432114601135,
    "selectivity": 0.6785691976547241,
    "virtual_spectrum_summary": 0.12124238908290863,
    "yield": 0.520838737487793
  },
  "ordinal": 20
}
```

## Batch 21

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.01,
      "operation": "add_reagent"
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.002,
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
      "seed_mass_g": 0.001
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
  "end_step": 337,
  "lifecycle_index": 21,
  "metrics": {
    "byproduct_signal": 0.15129877626895905,
    "conversion": 0.7788053154945374,
    "cost": 1.0,
    "crystal_csd_quality": 0.8364389538764954,
    "crystal_fines_fraction": 0.196244478225708,
    "crystal_purity": 0.9887010455131531,
    "crystal_size": 0.07488574832677841,
    "crystal_yield": 0.30665045976638794,
    "degradation_warning": 0.0543786995112896,
    "safety_risk": 0.09526555240154266,
    "score": 0.5141956210136414,
    "selectivity": 0.6607535481452942,
    "virtual_spectrum_summary": 0.10768473893404007,
    "yield": 0.5386221408843994
  },
  "ordinal": 21
}
```

## Batch 22

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.015,
      "operation": "add_reagent"
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.0025,
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
      "seed_mass_g": 0.001
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
  "end_step": 356,
  "lifecycle_index": 22,
  "metrics": {
    "byproduct_signal": 0.2110314667224884,
    "conversion": 0.8712871074676514,
    "cost": 1.0,
    "crystal_csd_quality": 0.4769533574581146,
    "crystal_fines_fraction": 0.9987235069274902,
    "crystal_purity": 1.0,
    "crystal_size": 0.062190596014261246,
    "crystal_yield": 0.41476553678512573,
    "degradation_warning": 0.06283995509147644,
    "safety_risk": 0.109703429043293,
    "score": 0.3870052695274353,
    "selectivity": 0.6093955039978027,
    "virtual_spectrum_summary": 0.14434528350830078,
    "yield": 0.5285086035728455
  },
  "ordinal": 22
}
```

## Batch 23

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.01,
      "operation": "add_reagent"
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.002,
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
      "seed_mass_g": 0.001
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
  "end_step": 377,
  "lifecycle_index": 23,
  "metrics": {
    "byproduct_signal": 0.17437012493610382,
    "conversion": 0.7844186425209045,
    "cost": 1.0,
    "crystal_csd_quality": 0.8424734473228455,
    "crystal_fines_fraction": 0.0962587371468544,
    "crystal_purity": 0.9959385991096497,
    "crystal_size": 0.12400925159454346,
    "crystal_yield": 0.39530062675476074,
    "degradation_warning": 0.051214754581451416,
    "safety_risk": 0.09592059254646301,
    "score": 0.5546311736106873,
    "selectivity": 0.6756768226623535,
    "virtual_spectrum_summary": 0.11895020306110382,
    "yield": 0.5360263586044312
  },
  "ordinal": 23
}
```

## Batch 24

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.059999999999999
    },
    {
      "amount_mol": 0.009,
      "operation": "add_reagent"
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.00165,
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
      "seed_mass_g": 0.00075
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
  "end_step": 398,
  "lifecycle_index": 24,
  "metrics": {
    "byproduct_signal": 0.1905374377965927,
    "conversion": 0.8295696973800659,
    "cost": 1.0,
    "crystal_csd_quality": 0.7650676965713501,
    "crystal_fines_fraction": 0.3723537027835846,
    "crystal_purity": 1.0,
    "crystal_size": 0.07491433620452881,
    "crystal_yield": 0.4137585461139679,
    "degradation_warning": 0.056819915771484375,
    "safety_risk": 0.09513464570045471,
    "score": 0.5124745965003967,
    "selectivity": 0.6464473009109497,
    "virtual_spectrum_summary": 0.1303645521402359,
    "yield": 0.5445525050163269
  },
  "ordinal": 24
}
```

## K1

```json
{
  "payload": {
    "report": "## Mechanistic account\n\n### Recommended process and observed outcome\nThe sealed recommendation is **batch 24**. It used solvent S2 (0.060 L), reagent (0.009 mol), catalyst C3 (0.00165 mol), reaction at 330 K for 1,800 s with 500 rpm stirring, quench, 0.00075 g seed, and staged 14,400 s cooling segments through 295, 290, 285, 280, 275, 270, 265, 260, 255 and 250 K, followed by a 14,400 s hold at 100 rpm, filtration and final assay.\n\nObserved final-assay results were crystal recovery 0.414, crystal purity 1.000, fines fraction 0.372, reaction conversion 0.830, selectivity 0.646 and reaction yield 0.545. Thus it met both required quality constraints and had the highest observed recovery among compliant batches.\n\n### Material effects\n**Catalyst:** In the approximately matched S2/high-loading experiments at 330 K, C3 performed best. Batches 2\u20135, using C0\u2013C3 respectively, gave crystal recoveries of 0.372, 0.343, 0.279 and 0.425. Their measured reaction yields were approximately 0.475, 0.450, 0.359 and 0.532. I interpret this as a fixed-world advantage for C3 in productive reaction flux. C2 was clearly unfavorable under these conditions. This is experimental evidence for this benchmark world, not a real-material identity claim.\n\n**Solvent:** At high loading with C1, batches 6\u20138 gave crystal recoveries of 0.383 in S0, 0.434 in S1 and 0.303 in S3, versus 0.343 for the comparable S2 batch 3. S1 therefore supported the best high-loading recovery. However, all of these direct-cooling runs produced nearly all fines. S2 became preferable when morphology was prioritized: its nominal dossier indicated the highest relative growth, lowest nucleation tendency and lowest impurity occlusion, and staged dilute S2 processes eventually gave the only clearly compliant particle distributions. The solvent ranking is therefore response-specific rather than universal: S1 favored high-loading recovery, while S2 offered the best controllability of crystal population.\n\nPurity was robust across most isolated products, generally about 0.96\u20131.00. Solvent and catalyst changes affected reaction selectivity and recovery much more than final crystal purity, suggesting strong rejection of reaction impurities during crystallization.\n\n### Reaction mechanism interpretation\nA useful minimal representation is a parallel/secondary network:\n\nR \u2192 P, R \u2192 B, and P \u2192 D,\n\nwhere P is target product, B is direct byproduct and D denotes thermal degradation. Approximate rate laws could be written as\n\nr_P = k_P(C,S,T) C_R,  r_B = k_B(C,S,T) C_R,  r_D = k_D(T) C_P.\n\nCatalyst and solvent alter the effective rate constants. Longer or hotter exposure can raise conversion but also increase byproduct and degradation. For example, batch 1 at 350 K for 3,600 s reached conversion 1.000 but only 0.447 selectivity, with degradation warning 0.137. At 330 K for 1,800 s, batch 5 retained conversion 0.984 while improving selectivity to 0.544 and lowering degradation warning to 0.075. Batch 9 at 310 K for 3,600 s still approached complete conversion but had only 0.311 selectivity, showing that low temperature was not automatically selective in this realized system; extended residence or the temperature dependence of competing pathways likely mattered.\n\nFor batch 24, the reaction yield relation was approximately\n\nY_rxn \u2248 X \u00d7 S = 0.830 \u00d7 0.646 \u2248 0.54,\n\nconsistent with its measured reaction yield of 0.545. Because reported crystal recovery is normalized to target already present before separation, it does not include reaction yield. A rough overall isolated-target fraction relative to reagent charge is instead\n\nY_overall \u2248 Y_rxn \u00d7 R_crystal.\n\nFor batch 24 this is about 0.545 \u00d7 0.414 \u2248 0.225. This distinction is important: batch 11 had a higher crystallization recovery (0.494) and reaction yield (0.588), but its fines fraction of 0.994 made it unacceptable.\n\n### Crystallization mechanism and reaction\u2013crystallization coupling\nThe results are consistent with competition between nucleation and growth. In classical qualitative form,\n\nJ \u221d exp[-B/(ln S)^2],  G = k_g(S\u22121)^g,\n\nwhere S is supersaturation, J is nucleation rate and G is crystal growth rate. High product concentration or a rapid temperature drop can drive J sharply upward, generating many particles that share the available solute and remain below 20 \u00b5m. Controlled supersaturation allows existing seeds to grow without a large secondary-nucleation burst.\n\nThis explains the main coupling: reaction loading and yield set the product concentration entering crystallization. Conditions that maximize product formation can create excessive supersaturation and poor particle quality. At high reagent loading, direct cooling gave good recovery but nearly complete fines. Batch 11, for example, achieved recovery 0.494 after thermal cycling but had fines 0.994. Diluting the reacting system reduced this nucleation pressure. Batch 12, with 0.010 mol reagent in 0.080 L S2, reduced fines to 0.644 while retaining recovery 0.408. Raising reagent to 0.020 and 0.030 mol in batches 13 and 14 increased recovery to 0.460 and 0.475 but returned fines to about 1.00.\n\nThe loading response was nonlinear. Batch 22 used 0.015 mol reagent with staged cooling and still underwent a fine-particle event: recovery 0.415 but fines 0.999. In contrast, batches 21 and 23 used 0.010 mol and gave fines of 0.196 and 0.096. I interpret this as crossing a nucleation threshold rather than a smooth linear concentration effect.\n\n### Process-history dependence\nCooling history was at least as important as endpoint temperature. Batch 18 cooled directly to 270 K and gave recovery 0.293 with fines 0.684. Batch 21 used the same 0.010 mol loading and the same 270 K endpoint, but approached it in 5 K stages; recovery was similar at 0.307 while fines fell to 0.196 and CSD quality rose to 0.836. This is the strongest matched evidence that staged cooling suppressed uncontrolled nucleation rather than merely changing equilibrium recovery.\n\nSimilarly, direct low-temperature batches 19 and 20 gave fines of 0.624 and 0.627, whereas staged cooling to 250 K in batch 23 gave recovery 0.395 with fines 0.096. Deep final cooling therefore need not cause fines if supersaturation is relieved progressively along the path.\n\nLong holding alone was not sufficient. Batch 12 used direct cooling to 250 K plus several long holds but retained fines of 0.644. Repeated warm/cool cycling in batch 11 raised recovery but left fines near 1.00. I infer that once a large fine population has nucleated, ordinary holding or modest cycling does not reliably eliminate it; preventing the initial burst is more effective than attempting later ripening.\n\nSeed mass was not independently resolved. Reducing it from 0.020 g in batch 1 to about 0.001 g in many later batches did not by itself solve the fines problem. An extremely small seed charge in the exploratory batch 10 did not establish a usable particle population until more seed and deeper cooling were applied. The recommended seed therefore serves as a reproducible nucleation template, while the cooling trajectory controls subsequent population growth.\n\n### Revisions during the campaign\nThe initial strategy emphasized full reagent/catalyst loading, deep direct cooling and long holds. Batch 1 demonstrated acceptable purity and recovery but essentially complete fines. Catalyst and solvent screening then identified C3 as the strongest productive catalyst and showed that S1 could give high recovery, but none of the high-loading direct-cooling batches met the particle constraint.\n\nThe next revision lowered reagent concentration. This improved particle quality but revealed a recovery/quality compromise and considerable nonlinearity. The final revision changed the cooling path rather than merely its endpoint. Staged 5 K ramps produced the decisive improvement in batches 21 and 23. Batch 24 then increased effective concentration modestly while retaining the staged trajectory, improving recovery to 0.414 while remaining compliant.\n\n### Uncertainty and unresolved tradeoff\nAll conclusions are based on single synthetic benchmark batches with noisy assays. Final-assay standard deviations were approximately 0.010 for crystal recovery and purity and 0.018 for fines, so the large differences between staged and direct cooling greatly exceed stated analytical noise. Nevertheless, process stochasticity is plausible, particularly near the apparent nucleation threshold. Batch 22\u2019s abrupt failure and variability among nominally similar low-loading runs show that a narrow safe operating window may exist.\n\nBatch 24\u2019s fines value of 0.372 is compliant but not as conservative as batch 23\u2019s 0.096. Batch 23 therefore provides more morphology margin, whereas batch 24 provides greater observed recovery (0.414 versus 0.395). The recommendation favors the higher-recovery compliant process, but replication would be needed to establish that its fines remain below 0.50 with adequate probability.\n\nThe major unresolved tradeoff is thus recovery versus nucleation risk. Higher loading and aggressive precipitation can raise recovery toward 0.45\u20130.49 but produced unacceptable fines in this campaign. Dilute staged cooling produced a recovery near 0.40\u20130.41 with excellent purity and compliant morphology. Untested alternatives include finer temperature increments, feedback control on supersaturation, different seed-size distributions, longer growth periods at intermediate temperature, or a carefully optimized S1/S2 solvent strategy. These could potentially recover some of the high-loading yield without crossing the nucleation threshold, but the campaign did not test them."
  },
  "failure": null,
  "elapsed_s": 70.53099999998813,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 1501952,
    "input_tokens": 1647576,
    "output_tokens": 13245,
    "reasoning_output_tokens": 4814
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
          "lower80": 0.18,
          "upper80": 0.44
        },
        "crystal_purity": {
          "estimate": 0.955,
          "lower80": 0.91,
          "upper80": 0.985
        },
        "crystal_size": {
          "estimate": 0.13,
          "lower80": 0.09,
          "upper80": 0.18
        },
        "crystal_yield": {
          "estimate": 0.36,
          "lower80": 0.27,
          "upper80": 0.45
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q01"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.18,
          "lower80": 0.08,
          "upper80": 0.32
        },
        "crystal_purity": {
          "estimate": 0.97,
          "lower80": 0.93,
          "upper80": 0.993
        },
        "crystal_size": {
          "estimate": 0.17,
          "lower80": 0.12,
          "upper80": 0.23
        },
        "crystal_yield": {
          "estimate": 0.3,
          "lower80": 0.21,
          "upper80": 0.39
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q02"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.09,
          "lower80": 0.03,
          "upper80": 0.2
        },
        "crystal_purity": {
          "estimate": 0.965,
          "lower80": 0.92,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.24,
          "lower80": 0.16,
          "upper80": 0.34
        },
        "crystal_yield": {
          "estimate": 0.24,
          "lower80": 0.15,
          "upper80": 0.34
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q03"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.36,
          "lower80": 0.22,
          "upper80": 0.53
        },
        "crystal_purity": {
          "estimate": 0.955,
          "lower80": 0.9,
          "upper80": 0.985
        },
        "crystal_size": {
          "estimate": 0.105,
          "lower80": 0.07,
          "upper80": 0.15
        },
        "crystal_yield": {
          "estimate": 0.34,
          "lower80": 0.25,
          "upper80": 0.43
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q04"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.28,
          "lower80": 0.15,
          "upper80": 0.44
        },
        "crystal_purity": {
          "estimate": 0.957,
          "lower80": 0.91,
          "upper80": 0.987
        },
        "crystal_size": {
          "estimate": 0.12,
          "lower80": 0.08,
          "upper80": 0.17
        },
        "crystal_yield": {
          "estimate": 0.35,
          "lower80": 0.27,
          "upper80": 0.43
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q05"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.92,
          "lower80": 0.79,
          "upper80": 0.99
        },
        "crystal_purity": {
          "estimate": 0.935,
          "lower80": 0.86,
          "upper80": 0.978
        },
        "crystal_size": {
          "estimate": 0.045,
          "lower80": 0.02,
          "upper80": 0.08
        },
        "crystal_yield": {
          "estimate": 0.37,
          "lower80": 0.28,
          "upper80": 0.46
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q06"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.24,
          "lower80": 0.12,
          "upper80": 0.39
        },
        "crystal_purity": {
          "estimate": 0.96,
          "lower80": 0.915,
          "upper80": 0.988
        },
        "crystal_size": {
          "estimate": 0.13,
          "lower80": 0.085,
          "upper80": 0.185
        },
        "crystal_yield": {
          "estimate": 0.36,
          "lower80": 0.28,
          "upper80": 0.44
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q07"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.72,
          "lower80": 0.53,
          "upper80": 0.88
        },
        "crystal_purity": {
          "estimate": 0.93,
          "lower80": 0.84,
          "upper80": 0.978
        },
        "crystal_size": {
          "estimate": 0.06,
          "lower80": 0.03,
          "upper80": 0.105
        },
        "crystal_yield": {
          "estimate": 0.29,
          "lower80": 0.19,
          "upper80": 0.39
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q08"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.78,
          "lower80": 0.59,
          "upper80": 0.92
        },
        "crystal_purity": {
          "estimate": 0.985,
          "lower80": 0.94,
          "upper80": 0.999
        },
        "crystal_size": {
          "estimate": 0.058,
          "lower80": 0.03,
          "upper80": 0.095
        },
        "crystal_yield": {
          "estimate": 0.012,
          "lower80": 0.001,
          "upper80": 0.04
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q09"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.48,
          "lower80": 0.31,
          "upper80": 0.66
        },
        "crystal_purity": {
          "estimate": 0.975,
          "lower80": 0.93,
          "upper80": 0.996
        },
        "crystal_size": {
          "estimate": 0.085,
          "lower80": 0.05,
          "upper80": 0.13
        },
        "crystal_yield": {
          "estimate": 0.075,
          "lower80": 0.03,
          "upper80": 0.14
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q10"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.29,
          "lower80": 0.16,
          "upper80": 0.45
        },
        "crystal_purity": {
          "estimate": 0.955,
          "lower80": 0.9,
          "upper80": 0.987
        },
        "crystal_size": {
          "estimate": 0.12,
          "lower80": 0.078,
          "upper80": 0.17
        },
        "crystal_yield": {
          "estimate": 0.34,
          "lower80": 0.25,
          "upper80": 0.43
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q11"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.72,
          "lower80": 0.54,
          "upper80": 0.87
        },
        "crystal_purity": {
          "estimate": 0.91,
          "lower80": 0.82,
          "upper80": 0.965
        },
        "crystal_size": {
          "estimate": 0.06,
          "lower80": 0.03,
          "upper80": 0.1
        },
        "crystal_yield": {
          "estimate": 0.47,
          "lower80": 0.38,
          "upper80": 0.56
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q12"
      }
    ],
    "rationale": "Q01\u2013Q02: S1 is expected to give greater recovery, while lower-solubility/lower-nucleation S3 should give larger particles and fewer fines. Q03\u2013Q04: increasing seed mass raises growth surface and recovery but divides solute among more particles, reducing size and increasing fines. Q05\u2013Q06: gradual cooling should suppress the initial nucleation burst; a rapid crash followed by holding can reach similar recovery but cannot readily repair the resulting fine population. Q07\u2013Q08: the added low-temperature hold is benign, whereas reheating to 315 K followed by rapid recooling risks partial dissolution and renewed nucleation. Q09\u2013Q10: both retain seeded particles, but immediate filtration gives almost no seed-excluded recovery; a 2-hour hold permits limited growth and may only narrowly satisfy the fines limit. Q11\u2013Q12: doubling reagent loading increases supersaturation and recovery but is predicted to cross the nonlinear nucleation threshold, lowering size and purity and producing excessive fines. Intervals are wider for fines and for thermal-shock/short-residence cases because the campaign showed threshold-like, history-dependent crystallization behavior and only single-batch evidence near the quality boundary."
  },
  "failure": null,
  "elapsed_s": 95.81299999999464,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 1505536,
    "input_tokens": 1732965,
    "output_tokens": 18021,
    "reasoning_output_tokens": 7920
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
    "report": "## 1. Status of the main claims\n\n### Supported by direct observations\n- **Staged cooling strongly improves particle quality.** The clearest matched comparison is batch 18 versus batch 21: both used 0.010 mol reagent in S2 and ended at 270 K. Direct cooling in batch 18 gave fines 0.684 and recovery 0.293; staged cooling in batch 21 gave fines 0.196 and recovery 0.307. Batch 23 further showed that staged cooling to 250 K could give recovery 0.395 with fines 0.096. The observation is direct; attributing it specifically to suppression of a nucleation burst is an interpretation.\n- **C3 was the best tested catalyst under the matched high-loading S2 screen.** Batches 2\u20135 used C0\u2013C3 and gave crystal recoveries of 0.372, 0.343, 0.279 and 0.425, respectively. Reaction yield was also highest with C3. This supports the empirical catalyst ranking for those conditions, not a universal catalytic mechanism.\n- **Loading creates a sharp quality/recovery tradeoff.** Batches 12\u201314 increased reagent from 0.010 to 0.020 and 0.030 mol. Recovery rose from 0.408 to 0.460\u20130.475, while fines rose from 0.644 to approximately 1.00. More decisively, staged batch 21 at 0.010 mol had fines 0.196, whereas staged batch 22 at 0.015 mol had fines 0.999. This directly supports nonlinear concentration sensitivity.\n- **Purity was comparatively robust.** Most isolated batches had purity around 0.96\u20131.00 despite large changes in recovery and particle quality. The conclusion that crystallization rejected impurities effectively is a reasonable interpretation of that observation.\n- **High conversion did not guarantee selectivity.** Batch 1 reached conversion 1.000 but selectivity only 0.447 and degradation warning 0.137. Batch 9 also showed that lowering temperature alone did not ensure selectivity. These observations support treating conversion, desired-product formation and degradation as separate processes.\n\n### Contradicted or materially qualified\n- **\u201cDilution improves morphology\u201d is too simple.** Batch 15, at only 0.005 mol reagent, still produced fines near 1.00 and recovery only 0.153. Dilution helped in some regimes but was not sufficient by itself; cooling history, seed population and whether enough product was available for sustained growth also mattered.\n- **Deeper cooling does not necessarily worsen fines.** A simple supersaturation argument would predict more nucleation at lower temperature, yet staged batch 23 at 250 K had better fines than staged batch 21 at 270 K. The cooling path dominated the endpoint effect in these observations.\n- **Long holding or thermal cycling was not a reliable cure for fines.** Batch 12 retained fines 0.644 after direct cooling and long holds, and batch 11 retained fines 0.994 after cycling despite recovery 0.494. This contradicts any strong claim that ripening alone repairs an already fine population.\n- **The solvent ranking is conditional.** S1 gave the highest recovery in the C1 solvent screen (batch 7), while S2 ultimately gave the best controlled morphology in dilute staged runs. Thus the evidence does not support one solvent being globally superior.\n\n### Still untested\n- The proposed parallel reaction network and classical nucleation/growth equations were useful organizing models, but individual rate constants, reaction orders and nucleation barriers were not measured.\n- Seed number, seed-size distribution and seed surface area were not independently varied. Seed-mass effects therefore remain unresolved.\n- No exact replicate established whether batches 21, 23 and 24 represent robust deterministic operation or favorable stochastic nucleation events.\n- Solvent blends, feedback control of supersaturation, finer cooling increments and deliberate intermediate-temperature growth holds were not tested.\n- The approximate overall-yield product, reaction yield \u00d7 crystallization recovery, was a bookkeeping relationship rather than a directly assayed overall mass yield.\n\n## 2. One additional experiment\n\nI would repeat the complete batch-24 recipe, while adding non-destructive particle-size measurements after reaching 280, 270, 260 and 250 K and before filtration. The physical recipe would otherwise be unchanged.\n\nThis single experiment would distinguish two competing explanations:\n1. **Controlled-growth explanation:** staged cooling steadily enlarges a limited seed population and avoids secondary nucleation.\n2. **Threshold/stochastic explanation:** batch 24 happened to avoid a random nucleation event, and the apparent benefit is not robust near its concentration boundary.\n\nUnder controlled growth, d50 should increase progressively, fines should remain below 0.50 or decline during the later stages, and final recovery should reproduce near 0.41 with high purity. Under a threshold event, one cooling interval would show an abrupt rise in fines and deterioration of CSD quality; final fines could resemble batch 22 despite similar handling. If d50 and fines remain almost unchanged until the final stages, the data would instead indicate that most crystallization occurs late and that staged cooling acts mainly by conditioning supersaturation before a final precipitation event.\n\n## 3. Least effectively used observation and least reliable prediction\n\nThe account used **batch 15** least effectively. Its very low loading produced low recovery and fines near 1.00, contrary to a monotonic dilution-improves-quality story. I acknowledged nonlinearity but did not explain this result well. It may indicate insufficient solute growth per seed, a seed-dominated number distribution, or a separate nucleation/growth regime at very low target inventory. Those alternatives cannot be separated from the available measurements.\n\nThe least reliable held-out prediction is **Q10**. Its predicted fines estimate was 0.48, immediately beside the 0.50 feasibility boundary, with an 80% interval spanning 0.31\u20130.66. The campaign contained little matched evidence for a large 0.025 g seed charge followed by only a two-hour hold at 292 K. Consequently, both the extent of seed-excluded growth and whether the seed population crosses the fines threshold are extrapolations. The numerical estimate may be reasonable, but its binary quality-feasible classification is particularly fragile."
  },
  "failure": null,
  "elapsed_s": 47.48399999999674,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 1579008,
    "input_tokens": 1823050,
    "output_tokens": 20026,
    "reasoning_output_tokens": 8573
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
    "selection_rationale": "Batch 24 gave the highest observed crystal recovery among batches meeting both constraints: crystal_yield 0.414, crystal_purity 1.000, and fines fraction 0.372. Its staged slow cooling controlled secondary nucleation while deep final cooling preserved recovery."
  },
  "recommendation_recipe": {
    "actions": [
      {
        "operation": "add_solvent",
        "solvent": 2,
        "volume_L": 0.059999999999999
      },
      {
        "amount_mol": 0.009,
        "operation": "add_reagent"
      },
      {
        "catalyst": 3,
        "catalyst_amount_mol": 0.00165,
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
        "seed_mass_g": 0.00075
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
    "lifecycle_index": 24,
    "rejected_attempts": [
      {
        "action": {
          "operation": "add_solvent",
          "solvent": 2,
          "volume_L": 0.08
        },
        "step": 378,
        "transaction_status": "campaign_resource_rejected"
      }
    ]
  },
  "prediction_evaluation": {
    "contrasts": [
      {
        "absolute_delta_error": 0.1492231216822536,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_yield",
        "predicted_delta": -0.06,
        "resolved": true,
        "true_delta": -0.2092231216822536
      },
      {
        "absolute_delta_error": 0.01514777149572899,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_purity",
        "predicted_delta": 0.015000000000000013,
        "resolved": false,
        "true_delta": -0.00014777149572897663
      },
      {
        "absolute_delta_error": 0.03288280081646157,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_size",
        "predicted_delta": 0.04000000000000001,
        "resolved": true,
        "true_delta": 0.007117199183538439
      },
      {
        "absolute_delta_error": 0.15661623193981455,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.12,
        "resolved": true,
        "true_delta": -0.27661623193981455
      },
      {
        "absolute_delta_error": 0.1001323298090879,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_yield",
        "predicted_delta": 0.10000000000000003,
        "resolved": false,
        "true_delta": -0.00013232980908786662
      },
      {
        "absolute_delta_error": 0.01915639526292434,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_purity",
        "predicted_delta": -0.010000000000000009,
        "resolved": false,
        "true_delta": 0.009156395262924333
      },
      {
        "absolute_delta_error": 0.13002056092012954,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_size",
        "predicted_delta": -0.135,
        "resolved": false,
        "true_delta": -0.004979439079870487
      },
      {
        "absolute_delta_error": 0.13658047462014644,
        "direction_correct": true,
        "factor": "seed",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.27,
        "resolved": true,
        "true_delta": 0.13341952537985358
      },
      {
        "absolute_delta_error": 0.01956647913216955,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_yield",
        "predicted_delta": 0.020000000000000018,
        "resolved": false,
        "true_delta": 0.00043352086783046695
      },
      {
        "absolute_delta_error": 0.018227866825037853,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.02199999999999991,
        "resolved": false,
        "true_delta": -0.0037721331749620557
      },
      {
        "absolute_delta_error": 0.031161131163011314,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_size",
        "predicted_delta": -0.075,
        "resolved": true,
        "true_delta": -0.04383886883698868
      },
      {
        "absolute_delta_error": 0.026184712049767467,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.64,
        "resolved": true,
        "true_delta": 0.6138152879502325
      },
      {
        "absolute_delta_error": 0.11304184008830015,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_yield",
        "predicted_delta": -0.07,
        "resolved": true,
        "true_delta": 0.04304184008830014
      },
      {
        "absolute_delta_error": 0.019622485368849585,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.029999999999999916,
        "resolved": true,
        "true_delta": -0.01037751463115033
      },
      {
        "absolute_delta_error": 0.030144646982690107,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_size",
        "predicted_delta": -0.07,
        "resolved": true,
        "true_delta": -0.0398553530173099
      },
      {
        "absolute_delta_error": 0.1699421779987409,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.48,
        "resolved": true,
        "true_delta": 0.6499421779987409
      },
      {
        "absolute_delta_error": 0.04314975880452933,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_yield",
        "predicted_delta": 0.063,
        "resolved": true,
        "true_delta": 0.10614975880452933
      },
      {
        "absolute_delta_error": 0.0022800208771958097,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_purity",
        "predicted_delta": -0.010000000000000009,
        "resolved": true,
        "true_delta": -0.012280020877195819
      },
      {
        "absolute_delta_error": 0.014274188309425409,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_size",
        "predicted_delta": 0.027000000000000003,
        "resolved": true,
        "true_delta": 0.012725811690574594
      },
      {
        "absolute_delta_error": 0.3425302662574825,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.30000000000000004,
        "resolved": false,
        "true_delta": 0.04253026625748246
      },
      {
        "absolute_delta_error": 0.11506595761778368,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_yield",
        "predicted_delta": 0.12999999999999995,
        "resolved": false,
        "true_delta": 0.014934042382216267
      },
      {
        "absolute_delta_error": 0.03989031320205472,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_purity",
        "predicted_delta": -0.04499999999999993,
        "resolved": false,
        "true_delta": -0.005109686797945212
      },
      {
        "absolute_delta_error": 0.03166160161035516,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_size",
        "predicted_delta": -0.06,
        "resolved": true,
        "true_delta": -0.028338398389644838
      },
      {
        "absolute_delta_error": 0.172412437007269,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.43,
        "resolved": true,
        "true_delta": 0.602412437007269
      }
    ],
    "failures": [],
    "metrics": {
      "crystal_fines_fraction": {
        "coverage80": 0.3333333333333333,
        "interval_score80": 1.6829788335905427,
        "interval_width": 0.28250000000000003,
        "mae": 0.262935839495325,
        "n": 12,
        "planned": 12
      },
      "crystal_purity": {
        "coverage80": 0.5833333333333334,
        "interval_score80": 0.11138653806775715,
        "interval_width": 0.08799999999999997,
        "mae": 0.03133044883320133,
        "n": 12,
        "planned": 12
      },
      "crystal_size": {
        "coverage80": 0.6666666666666666,
        "interval_score80": 0.2185862578296567,
        "interval_width": 0.09100000000000001,
        "mae": 0.043707877671654356,
        "n": 12,
        "planned": 12
      },
      "crystal_yield": {
        "coverage80": 0.4166666666666667,
        "interval_score80": 0.415777016177637,
        "interval_width": 0.16158333333333333,
        "mae": 0.0815442139550638,
        "n": 12,
        "planned": 12
      }
    },
    "quality": {
      "balanced_accuracy": 0.7857142857142857,
      "false_negative": 0,
      "false_positive": 3,
      "true_negative": 4,
      "true_positive": 5
    },
    "resolved_direction_correct": 14,
    "resolved_direction_n": 15,
    "tie_correct": 0,
    "tie_n": 9,
    "valid": true
  },
  "public_baselines": {
    "available": false,
    "failure": "Unknown transaction status at step 378: campaign_resource_rejected"
  },
  "tokens": {
    "basis": "cumulative thread snapshots differenced in source/K1/Q/K2 order",
    "complete": true,
    "monetary_cost_usd": null,
    "stages": [
      {
        "cached_input": 1498496,
        "input": 1573960,
        "output": 10008,
        "stage": "source",
        "uncached_input": 75464
      },
      {
        "cached_input": 3456,
        "input": 73616,
        "output": 3237,
        "stage": "K1",
        "uncached_input": 70160
      },
      {
        "cached_input": 3584,
        "input": 85389,
        "output": 4776,
        "stage": "Q",
        "uncached_input": 81805
      },
      {
        "cached_input": 73472,
        "input": 90085,
        "output": 2005,
        "stage": "K2",
        "uncached_input": 16613
      }
    ],
    "total": {
      "cached_input": 1579008,
      "input": 1823050,
      "input_plus_output": 1843076,
      "output": 20026,
      "uncached_input": 244042
    },
    "valid": true
  },
  "elapsed_s": 632.4689999999828
}
```
