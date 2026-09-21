# C-W02-B12-E-MisIndexed

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
      "seed_mass_g": 0.05
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
  "end_step": 13,
  "lifecycle_index": 1,
  "metrics": {
    "byproduct_signal": 0.32486188411712646,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5323254466056824,
    "crystal_fines_fraction": 0.9972753524780273,
    "crystal_purity": 0.9906907081604004,
    "crystal_size": 0.04411771148443222,
    "crystal_yield": 0.4393865764141083,
    "degradation_warning": 0.14797012507915497,
    "safety_risk": 0.1807757318019867,
    "score": 0.39608651399612427,
    "selectivity": 0.5387797355651855,
    "virtual_spectrum_summary": 0.2452605962753296,
    "yield": 0.5366172790527344
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
      "stirring_speed_rpm": 500,
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
  "end_step": 30,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.22992780804634094,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5592923164367676,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9817609190940857,
    "crystal_size": 0.06037694588303566,
    "crystal_yield": 0.5257439613342285,
    "degradation_warning": 0.04619438201189041,
    "safety_risk": 0.1913294643163681,
    "score": 0.4356194734573364,
    "selectivity": 0.6183687448501587,
    "virtual_spectrum_summary": 0.14724776148796082,
    "yield": 0.6059615015983582
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
      "solvent": 3,
      "volume_L": 0.08
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
      "target_temperature_K": 335
    },
    {
      "instrument": "hplc",
      "operation": "measure"
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 305
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 295
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 265
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
  "end_step": 48,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.29444003105163574,
    "conversion": 0.9944811463356018,
    "cost": 1.0,
    "crystal_csd_quality": 0.5065901279449463,
    "crystal_fines_fraction": 0.9949334263801575,
    "crystal_purity": 0.9862552285194397,
    "crystal_size": 0.0435103215277195,
    "crystal_yield": 0.3591954708099365,
    "degradation_warning": 0.0560014545917511,
    "safety_risk": 0.1824120730161667,
    "score": 0.3553648591041565,
    "selectivity": 0.46138501167297363,
    "virtual_spectrum_summary": 0.18714267015457153,
    "yield": 0.4587312936782837
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
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 335
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
      "seed_mass_g": 0.0001
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
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
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
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
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
  "end_step": 87,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.24036535620689392,
    "conversion": 0.9886753559112549,
    "cost": 1.0,
    "crystal_csd_quality": 0.5528929233551025,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 1.0,
    "crystal_size": 0.03306589648127556,
    "crystal_yield": 0.5243800282478333,
    "degradation_warning": 0.04470647871494293,
    "safety_risk": 0.18813899159431458,
    "score": 0.4283919036388397,
    "selectivity": 0.584962785243988,
    "virtual_spectrum_summary": 0.15231886506080627,
    "yield": 0.5711467266082764
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
      "catalyst": 3,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 400,
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
      "seed_mass_g": 1e-05
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
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 298
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
      "target_temperature_K": 278
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 276
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 274
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 272
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 268
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 266
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 264
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 262
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 260
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 258
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 256
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 254
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 252
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
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.3176838159561157,
    "conversion": 0.9959923028945923,
    "cost": 1.0,
    "crystal_csd_quality": 0.552509605884552,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9780358672142029,
    "crystal_size": 0.016113439574837685,
    "crystal_yield": 0.4314629137516022,
    "degradation_warning": 0.07645183056592941,
    "safety_risk": 0.1756293922662735,
    "score": 0.3837583363056183,
    "selectivity": 0.49354153871536255,
    "virtual_spectrum_summary": 0.2091294229030609,
    "yield": 0.4872227609157562
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
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 400,
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
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
    },
    {
      "duration_s": 14400,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 310
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
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 305
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 280
    },
    {
      "duration_s": 14400,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 295
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
  "end_step": 147,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.24350890517234802,
    "conversion": 0.9873378276824951,
    "cost": 1.0,
    "crystal_csd_quality": 0.47035324573516846,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9997793436050415,
    "crystal_size": 0.02805684506893158,
    "crystal_yield": 0.5427963733673096,
    "degradation_warning": 0.04524747282266617,
    "safety_risk": 0.18871654570102692,
    "score": 0.41991478204727173,
    "selectivity": 0.5981015563011169,
    "virtual_spectrum_summary": 0.15429125726222992,
    "yield": 0.5969078540802002
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
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 335
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
  "end_step": 158,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.2028590589761734,
    "conversion": 0.9931881427764893,
    "cost": 1.0,
    "crystal_csd_quality": 0.5317365527153015,
    "crystal_fines_fraction": 0.9868496060371399,
    "crystal_purity": 0.9728845357894897,
    "crystal_size": 0.059646062552928925,
    "crystal_yield": 0.585323691368103,
    "degradation_warning": 0.03600310906767845,
    "safety_risk": 0.15214020013809204,
    "score": 0.4519768953323364,
    "selectivity": 0.6250907778739929,
    "virtual_spectrum_summary": 0.12777388095855713,
    "yield": 0.6444239020347595
  },
  "ordinal": 7
}
```

## Batch 8

```json
{
  "actions": [
    {
      "amount_mol": 0.01,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "catalyst": 0,
      "catalyst_amount_mol": 0.002,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 335
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
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 280
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
  "end_step": 170,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.1698451042175293,
    "conversion": 0.9360008239746094,
    "cost": 1.0,
    "crystal_csd_quality": 0.5076591372489929,
    "crystal_fines_fraction": 0.909092366695404,
    "crystal_purity": 0.9693173766136169,
    "crystal_size": 0.09243689477443695,
    "crystal_yield": 0.48454469442367554,
    "degradation_warning": 0.05607340484857559,
    "safety_risk": 0.05836517736315727,
    "score": 0.4449935555458069,
    "selectivity": 0.7264585494995117,
    "virtual_spectrum_summary": 0.11864783614873886,
    "yield": 0.6597743034362793
  },
  "ordinal": 8
}
```

## Batch 9

```json
{
  "actions": [
    {
      "amount_mol": 0.002,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "catalyst": 0,
      "catalyst_amount_mol": 0.001,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 335
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
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 275
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
  "end_step": 182,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.23918108642101288,
    "conversion": 0.9097932577133179,
    "cost": 1.0,
    "crystal_csd_quality": 1.0,
    "crystal_fines_fraction": 0.0014134504599496722,
    "crystal_purity": 0.994659960269928,
    "crystal_size": 0.3764515519142151,
    "crystal_yield": 0.007928860373795033,
    "degradation_warning": 0.10175154358148575,
    "safety_risk": 0.03593156486749649,
    "score": 0.5502671599388123,
    "selectivity": 0.7229070067405701,
    "virtual_spectrum_summary": 0.17733779549598694,
    "yield": 0.6693465709686279
  },
  "ordinal": 9
}
```

## Batch 10

```json
{
  "actions": [
    {
      "amount_mol": 0.005,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "catalyst": 0,
      "catalyst_amount_mol": 0.00125,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 5400,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 335
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
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 275
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
  "end_step": 194,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.19939692318439484,
    "conversion": 0.8890493512153625,
    "cost": 1.0,
    "crystal_csd_quality": 0.4375433325767517,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9671863317489624,
    "crystal_size": 0.041449546813964844,
    "crystal_yield": 0.29045888781547546,
    "degradation_warning": 0.08321794867515564,
    "safety_risk": 0.043450288474559784,
    "score": 0.3651387393474579,
    "selectivity": 0.7089908123016357,
    "virtual_spectrum_summary": 0.14711637794971466,
    "yield": 0.6488848924636841
  },
  "ordinal": 10
}
```

## Batch 11

```json
{
  "actions": [
    {
      "amount_mol": 0.003,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "catalyst": 0,
      "catalyst_amount_mol": 0.001,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 335
    },
    {
      "operation": "quench"
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 275
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
  "end_step": 205,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.2424963116645813,
    "conversion": 0.9133614897727966,
    "cost": 1.0,
    "crystal_csd_quality": 0.5183960199356079,
    "crystal_fines_fraction": 0.9936863780021667,
    "crystal_purity": 0.9820498824119568,
    "crystal_size": 0.029866831377148628,
    "crystal_yield": 0.025066621601581573,
    "degradation_warning": 0.08747502416372299,
    "safety_risk": 0.03766728565096855,
    "score": 0.3177473545074463,
    "selectivity": 0.7188834547996521,
    "virtual_spectrum_summary": 0.1727367341518402,
    "yield": 0.6389074921607971
  },
  "ordinal": 11
}
```

## Batch 12

```json
{
  "actions": [
    {
      "amount_mol": 0.002,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "catalyst": 0,
      "catalyst_amount_mol": 0.001,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 335
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
      "target_temperature_K": 305
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 290
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 275
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
  "end_step": 219,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.3155064582824707,
    "conversion": 0.9844428896903992,
    "cost": 1.0,
    "crystal_csd_quality": 0.45501843094825745,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9934307336807251,
    "crystal_size": 0.07531038671731949,
    "crystal_yield": 0.19700053334236145,
    "degradation_warning": 0.19620515406131744,
    "safety_risk": 0.07826320827007294,
    "score": 0.34985896944999695,
    "selectivity": 0.6510160565376282,
    "virtual_spectrum_summary": 0.26182088255882263,
    "yield": 0.6438387036323547
  },
  "ordinal": 12
}
```

## K1

```json
{
  "payload": {
    "report": "Mechanistic account\n\nThe campaign revealed a sharp quality\u2013recovery tradeoff dominated by solution loading and solvent choice. Batch 9 remains the recommended process because it was the only completed batch observed to satisfy both hard constraints: crystal purity 0.9947 and number fraction below 20 \u00b5m of 0.0014. Its seed-excluded crystal recovery was only 0.0079, however, so it did not reach the 0.10 feasibility target.\n\nObserved material effects\n\nCatalyst C0 was the most consistently useful catalyst in the tested region. Under broadly comparable concentrated S2 conditions, changing from C1 in batch 1 to C0 in batch 2 increased selectivity from about 0.539 to 0.618, reduced degradation warning from 0.148 to 0.046, and increased crystal recovery from 0.439 to 0.526. Batch 3, using C1/S3, had lower selectivity (0.461) and recovery (0.359), while batch 5 with C3/S2 gave selectivity 0.494 and recovery 0.431. These comparisons are directionally supportive rather than factorial proofs because temperature, time, and crystallization histories also changed.\n\nSolvent S0 gave the best high-loading recovery. Batch 7, using 0.040 mol reagent in 0.080 L S0 with C0, produced the campaign\u2019s highest crystal recovery, 0.585, with purity 0.973. Its fines fraction was nevertheless 0.987, making it infeasible. S2 could also provide substantial recovery: batches 2, 4, and 6 gave approximately 0.524\u20130.543, but all had fines fractions essentially equal to 1. Thus, the nominally favorable growth characteristics of S2 did not overcome excessive nucleation at high loading.\n\nReaction\u2013crystallization coupling\n\nThe reaction establishes both the target inventory available for crystallization and the impurity environment controlling occlusion. A useful approximate decomposition is\n\n  overall isolated target fraction \u2248 reaction yield \u00d7 crystal recovery.\n\nFor example, batch 7 had reaction yield 0.644 and crystal recovery 0.585, giving an approximate overall isolated fraction of 0.377. Batch 12 had corresponding values 0.644 and 0.197, or about 0.127. Batch 9 had reaction yield 0.669 but recovery 0.0079, or only about 0.0053 overall. Crystal recovery is therefore not reaction yield: it is the fraction of target present before separation that was recovered as seed-excluded crystals.\n\nLower reaction temperature and use of C0 generally retained useful conversion while improving selectivity and degradation relative to the initial hotter process. The initial batch used C1/S2 at 360 K for 3600 s and reached complete conversion, but its selectivity was only 0.539 and degradation warning 0.148. Later C0/S0 dilute batches gave selectivity around 0.71\u20130.73 with reaction yields around 0.64\u20130.67. I interpret this as evidence that forcing conversion at high temperature promoted competing pathways; it does not establish a unique kinetic law.\n\nLoading, nucleation, and growth\n\nUsing the approximate initial loading C_R = n_R/V_S, batches 1\u20137 were run near 0.50 mol/L. Batch 8 used 0.125 mol/L, batch 10 used 0.0625 mol/L, batch 11 used 0.0375 mol/L, and batches 9 and 12 used 0.025 mol/L. Decreasing S0 loading from batch 7 to batch 8 reduced the fines fraction from 0.987 to 0.909 and increased the normalized size metric from 0.060 to 0.092, while recovery fell from 0.585 to 0.485. At 0.025 mol/L in batch 9, the fines fraction collapsed to 0.0014 and normalized size rose to 0.376, but recovery collapsed to 0.0079. At the intermediate 0.0625 mol/L condition in batch 10, recovery was 0.290 but fines returned to 1.0. Batch 11 at 0.0375 mol/L without seed still had fines 0.994 and recovery 0.025.\n\nA conventional supersaturation interpretation is consistent with this discontinuous behavior:\n\n  S = C/C*(T, solvent),\n  J \u2248 k_n exp[-B/(ln S)^2],\n  G \u2248 k_g(S-1)^g,\n\nwhere J is primary nucleation rate and G is growth rate. Because J depends very steeply on supersaturation, a modest increase in loading can cross from a few growing crystals to a large population of fines. At very low loading in S0, supersaturation apparently remained low enough to suppress nucleation and favor a small number of large crystals, but much of the target stayed dissolved, causing poor recovery. This interpretation is plausible rather than directly measured; solubility and nucleation rates were not independently assayed.\n\nThe solvent comparison at equal dilute loading is especially informative. Batch 9 used 0.025 mol/L in S0 and gave recovery 0.0079 with almost no fines. Batch 12 used the same nominal loading in S2 and raised recovery to 0.197, but its fines fraction became 1.0. I interpret S2 as generating substantially greater effective supersaturation at the final temperatures: this improved precipitation but triggered excessive nucleation. Both batches retained high purity (0.995 and 0.993), showing that the unresolved constraint was particle-number distribution rather than chemical purity.\n\nProcess-history dependence\n\nCooling history, seeding, and thermal cycling were varied extensively, but their effects were subordinate to loading in the tested high-concentration regime:\n\n\u2022 Batch 2 used a small seed charge followed by staged cooling and long holds; recovery was 0.526 but fines were 1.0.\n\u2022 Batch 4 used a much smaller seed charge and many long growth holds; recovery remained 0.524 and fines remained 1.0.\n\u2022 Batch 5 used many small 2 K cooling increments, yet produced fines of 1.0 and lower recovery of 0.431.\n\u2022 Batch 6 included a deep cooling shock, reheating, a large seed charge, and repeated heat\u2013cool cycles. Recovery reached 0.543, but fines again remained 1.0.\n\u2022 Batch 3 used no seed and thermal cycling in S3; it still produced fines of 0.995.\n\nThese observations argue against simply extending holds or adding more cooling stages as a sufficient remedy after a dense fine population has formed. Reheating in batch 6 may not have entered a selective-dissolution window: it either failed to dissolve enough fines or redissolved material that renucleated during recooling. Seed charges spanning roughly 10^-5 to 0.05 g also failed to control fines at 0.50 mol/L. However, seed amount was not isolated from loading and thermal history, so seed effectiveness remains uncertain.\n\nThe contrast between batches 9 and 11 also suggests history dependence. Batch 9 used 0.0001 g seed at 0.025 mol/L and produced excellent particle quality, whereas unseeded batch 11 at the somewhat higher 0.0375 mol/L produced almost exclusively fines. Both seed presence and the lower loading could explain the difference; the campaign cannot separate them.\n\nRevision of the working model\n\nThe initial strategy followed the nominal dossier: S2 was expected to combine low nucleation, good growth, and low impurity occlusion. Early batches confirmed high purity and reasonable recovery but falsified the expectation that slow cooling or seeding alone would meet the fines limit. Thermal holds, fine cooling increments, and cycling were then tested and also failed at high loading. Screening S0 in batch 7 improved recovery and reaction performance, after which dilution was treated as the main control variable. Batch 9 exposed a narrow low-supersaturation regime with excellent particle quality but inadequate recovery. The final S2 test in batch 12 deliberately sought more recovery at the same dilute loading; it exceeded the initial 0.10 recovery target but failed the fines constraint completely. The recommendation was therefore revised from maximizing raw recovery to selecting the only empirically quality-feasible batch.\n\nUncertainty and untested alternatives\n\nEach batch had only one final assay, so process variation and assay noise were not estimated by replication. Some comparisons changed catalyst, temperature, loading, seed amount, and cooling history together. Early HPLC and particle-size measurements supported the trends, but later decisions relied mainly on final assays. The reported size and fines channels are separately noisy synthetic measurements and should not be forced into exact distributional consistency.\n\nThe most important unresolved region is between the S0 conditions of batches 9 and 11, approximately 0.025\u20130.0375 mol/L. A finer loading search, with replicated seed amount and identical thermal history, might locate a point with recovery above 0.0079 while retaining fines below 0.50. Also untested are intermediate solvent behavior between S0 and S2, a designed selective-dissolution temperature determined from solubility measurements, controlled seed-size distributions, and independent variation of seed number versus seed mass. Mixed solvents, washing, and classified removal of fines were not available in the tested workflow.\n\nAccordingly, batch 9 is defensible as the only demonstrated feasible process, not as proof of a global optimum. The campaign establishes a strong mechanistic tradeoff: increasing effective supersaturation improves seed-excluded recovery but drives secondary or primary nucleation so strongly that the number-based fines constraint fails well before maximum recovery is reached."
  },
  "failure": null,
  "elapsed_s": 70.76499999998487,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 491008,
    "input_tokens": 558907,
    "output_tokens": 11189,
    "reasoning_output_tokens": 4176
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
          "estimate": 0.27,
          "lower80": 0.08,
          "upper80": 0.55
        },
        "crystal_purity": {
          "estimate": 0.93,
          "lower80": 0.85,
          "upper80": 0.98
        },
        "crystal_size": {
          "estimate": 0.19,
          "lower80": 0.1,
          "upper80": 0.31
        },
        "crystal_yield": {
          "estimate": 0.38,
          "lower80": 0.22,
          "upper80": 0.54
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q01"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.46,
          "lower80": 0.19,
          "upper80": 0.76
        },
        "crystal_purity": {
          "estimate": 0.95,
          "lower80": 0.88,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.13,
          "lower80": 0.06,
          "upper80": 0.24
        },
        "crystal_yield": {
          "estimate": 0.48,
          "lower80": 0.32,
          "upper80": 0.64
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q02"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.68,
          "lower80": 0.37,
          "upper80": 0.91
        },
        "crystal_purity": {
          "estimate": 0.94,
          "lower80": 0.86,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.1,
          "lower80": 0.04,
          "upper80": 0.2
        },
        "crystal_yield": {
          "estimate": 0.5,
          "lower80": 0.34,
          "upper80": 0.65
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q03"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.31,
          "lower80": 0.1,
          "upper80": 0.59
        },
        "crystal_purity": {
          "estimate": 0.94,
          "lower80": 0.87,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.19,
          "lower80": 0.1,
          "upper80": 0.31
        },
        "crystal_yield": {
          "estimate": 0.52,
          "lower80": 0.37,
          "upper80": 0.67
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q04"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.34,
          "lower80": 0.12,
          "upper80": 0.62
        },
        "crystal_purity": {
          "estimate": 0.94,
          "lower80": 0.87,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.18,
          "lower80": 0.09,
          "upper80": 0.3
        },
        "crystal_yield": {
          "estimate": 0.52,
          "lower80": 0.37,
          "upper80": 0.67
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q05"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.64,
          "lower80": 0.34,
          "upper80": 0.88
        },
        "crystal_purity": {
          "estimate": 0.93,
          "lower80": 0.84,
          "upper80": 0.98
        },
        "crystal_size": {
          "estimate": 0.09,
          "lower80": 0.04,
          "upper80": 0.18
        },
        "crystal_yield": {
          "estimate": 0.54,
          "lower80": 0.39,
          "upper80": 0.69
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q06"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.3,
          "lower80": 0.09,
          "upper80": 0.58
        },
        "crystal_purity": {
          "estimate": 0.94,
          "lower80": 0.87,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.2,
          "lower80": 0.1,
          "upper80": 0.32
        },
        "crystal_yield": {
          "estimate": 0.53,
          "lower80": 0.38,
          "upper80": 0.68
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q07"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.18,
          "lower80": 0.04,
          "upper80": 0.43
        },
        "crystal_purity": {
          "estimate": 0.96,
          "lower80": 0.89,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.25,
          "lower80": 0.13,
          "upper80": 0.39
        },
        "crystal_yield": {
          "estimate": 0.47,
          "lower80": 0.3,
          "upper80": 0.64
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q08"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.08,
          "lower80": 0.01,
          "upper80": 0.28
        },
        "crystal_purity": {
          "estimate": 0.97,
          "lower80": 0.9,
          "upper80": 1
        },
        "crystal_size": {
          "estimate": 0.18,
          "lower80": 0.09,
          "upper80": 0.3
        },
        "crystal_yield": {
          "estimate": 0.008,
          "lower80": 0,
          "upper80": 0.035
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q09"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.14,
          "lower80": 0.03,
          "upper80": 0.4
        },
        "crystal_purity": {
          "estimate": 0.96,
          "lower80": 0.88,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.19,
          "lower80": 0.09,
          "upper80": 0.31
        },
        "crystal_yield": {
          "estimate": 0.12,
          "lower80": 0.04,
          "upper80": 0.24
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q10"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.31,
          "lower80": 0.1,
          "upper80": 0.59
        },
        "crystal_purity": {
          "estimate": 0.94,
          "lower80": 0.87,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.19,
          "lower80": 0.1,
          "upper80": 0.31
        },
        "crystal_yield": {
          "estimate": 0.52,
          "lower80": 0.37,
          "upper80": 0.67
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q11"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.79,
          "lower80": 0.52,
          "upper80": 0.96
        },
        "crystal_purity": {
          "estimate": 0.9,
          "lower80": 0.79,
          "upper80": 0.97
        },
        "crystal_size": {
          "estimate": 0.08,
          "lower80": 0.03,
          "upper80": 0.16
        },
        "crystal_yield": {
          "estimate": 0.62,
          "lower80": 0.48,
          "upper80": 0.75
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q12"
      }
    ],
    "rationale": "All recipes contain seed, so particles are expected even where seed-excluded product recovery is negligible. Q01\u2013Q02 isolate solvent: lower effective solubility in S3 should increase recovery but also supersaturation and fines relative to S1. Q03\u2013Q04 isolate seed mass: the larger seed charge should provide much more growth surface and suppress uncontrolled nucleation, with little change in equilibrium recovery. Q05\u2013Q06 compare slow cooling with an initial temperature crash followed by an equal long cold residence; the crash is expected to create substantially more fines, while final recovery remains similar. Q07\u2013Q08 compare continued cold growth with a 315 K anneal and recooling; selective dissolution of small particles should lower fines and increase size, at some recovery cost. Q09\u2013Q10 compare 60 seconds with an additional two-hour hold at 292 K: the hold raises seed-excluded recovery, although both remain seed-dominated and relatively coarse. Q11\u2013Q12 isolate loading: doubling reagent concentration should raise recovery but cross toward the high-nucleation regime observed in the campaign, reducing size and making fines infeasible. Intervals are deliberately broad because these recipes use C1, 0.02 L scale, unusually large seed charges, and cooling histories outside the closest completed batches; feasibility assignments use point estimates and are least secure for Q01, Q02, Q04\u2013Q05, and Q11 near the fines threshold."
  },
  "failure": null,
  "elapsed_s": 61.35899999999674,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 494592,
    "input_tokens": 615400,
    "output_tokens": 14096,
    "reasoning_output_tokens": 5369
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
    "report": "1. Claim audit\n\nSupported by direct observations:\n- A strong quality\u2013recovery tradeoff was observed. In S0, batch 7 gave high recovery (0.585) but fines of 0.987, whereas batch 9 gave only 0.0079 recovery but fines of 0.0014. Both had purity above 0.97.\n- Effective supersaturation depends strongly on solvent. At the same nominal 0.025 mol/L loading, batch 9 in S0 had very low recovery and almost no fines, while batch 12 in S2 reached 0.197 recovery but fines of 1.0. Interpreting this as a solubility/nucleation difference is plausible, although the cooling schedules were not identical.\n- Slow cooling alone did not solve the fines problem at high loading. Batches 2, 4, and 5 used staged or very gradual cooling yet had fines near 1.0. Batch 6 added substantial seeding and thermal cycling but also ended at fines of 1.0.\n- Chemical purity was generally not the limiting constraint: all final crystalline products were about 0.97\u20131.00 pure. Particle-number distribution was the recurring failure.\n\nPartially supported but confounded:\n- C0 appeared better than C1 or C3 for reaction selectivity and degradation. Batch 2 outperformed batch 1, and later C0 batches often had selectivity near 0.60\u20130.73. These were not matched catalyst comparisons: temperature, solvent, concentration, and histories also differed.\n- Lower loading appeared to reduce nucleation, but the response was not smoothly monotonic. Batch 9 at 0.025 mol/L had excellent particle quality, while batch 11 at 0.0375 mol/L and batch 10 at 0.0625 mol/L had fines near 1.0. Batch 11 was unseeded, so loading and seeding cannot be separated.\n- The interpretation that higher reaction temperature promotes competing pathways is consistent with batch 1\u2019s relatively poor selectivity and high degradation warning, but no matched temperature experiment established causality.\n\nContradicted or weakened:\n- A simple claim that more seed or more residence time necessarily suppresses fines is contradicted by batch 6, where 0.05 g seed and repeated heat\u2013cool cycles still gave fines of 1.0. Batches 2 and 4 likewise showed that long holds did not rescue an already fine-rich slurry.\n- The nominal dossier suggestion that S2 should favor growth over nucleation was not realized under the tested conditions: S2 repeatedly produced predominantly fines.\n\nStill untested:\n- Whether batch 9\u2019s success arose mainly from its very low loading or from its small seed charge.\n- Whether a deliberately identified selective-dissolution temperature can remove fines without losing excessive recovery.\n- Mixed solvents, controlled seed-size distributions, replication, and a fine loading scan between 0.025 and 0.0375 mol/L were not tested.\n\n2. One additional experiment\n\nI would repeat batch 9 exactly\u2014S0, 0.002 mol reagent in 0.080 L, C0, the same reaction and 300\u2192275\u2192250 K cooling history\u2014but omit the 0.0001 g seed. This uses batch 9 as a direct control and distinguishes two competing explanations:\n\n- Loading-dominated explanation: low effective supersaturation itself suppresses primary nucleation. The unseeded run should produce few or possibly no recoverable particles; if particles form, fines should remain below 0.50, with similarly very low recovery.\n- Seed-control explanation: the small seed population captured supersaturation and prevented primary nucleation. Omitting it should cause either delayed burst nucleation with fines near 1.0, as in batch 11, or no crystallization within the available time.\n- An intermediate result\u2014some particles with appreciably more fines than batch 9 but less than batch 11\u2014would indicate that both low loading and seed-mediated growth were necessary.\n\nThis experiment would also reveal whether batch 9\u2019s large normalized size and extremely low fines substantially reflected the introduced seed population rather than seed-excluded product growth.\n\n3. Least effectively used evidence and least reliable prediction\n\nThe account used batch 6 least effectively. It correctly noted that a 0.05 g seed charge plus repeated heating and cooling failed to reduce fines, but it did not fully propagate that negative evidence into claims about seed surface and selective dissolution. Batch 6 shows that once high supersaturation creates many nuclei, neither large seed mass nor unspecific thermal cycling guarantees population control.\n\nQ08 is the least reliable held-out prediction. Its predicted improvement over Q07 depends on a one-hour 315 K anneal selectively dissolving fines, followed by only one hour of recooling. No solubility curve or dissolution threshold was measured, and batch 6 provides adverse evidence that thermal cycling may simply redissolve material and permit renewed nucleation. The anneal could therefore improve size and fines as predicted, dissolve too much product and sharply lower recovery, or cause renucleation and leave fines high. Its interval cannot fully represent this potentially multimodal behavior."
  },
  "failure": null,
  "elapsed_s": 47.094000000011874,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 494592,
    "input_tokens": 674720,
    "output_tokens": 16221,
    "reasoning_output_tokens": 6387
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
    "selected_experiment_index": 9,
    "selection_rationale": "Batch 9 was the only completed batch observed to satisfy both quality constraints (crystal purity 0.995 and fines fraction 0.0014); its crystal recovery was low (0.0079), below the 0.10 feasibility target, but it is the highest-recovery quality-feasible completed choice."
  },
  "recommendation_recipe": {
    "actions": [
      {
        "amount_mol": 0.002,
        "operation": "add_reagent"
      },
      {
        "operation": "add_solvent",
        "solvent": 0,
        "volume_L": 0.08
      },
      {
        "catalyst": 0,
        "catalyst_amount_mol": 0.001,
        "operation": "add_catalyst"
      },
      {
        "duration_s": 7200,
        "operation": "heat",
        "stirring_speed_rpm": 400,
        "target_temperature_K": 335
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
    "excluded_rejected_attempts": [
      {
        "action": {
          "duration_s": 14400,
          "operation": "cool_crystallize",
          "target_temperature_K": 300
        },
        "status": "validation_failed",
        "step": 177
      }
    ],
    "lifecycle_index": 9,
    "source_attempts": 12
  },
  "prediction_evaluation": {
    "contrasts": [
      {
        "absolute_delta_error": 0.2931177888119947,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_yield",
        "predicted_delta": 0.09999999999999998,
        "resolved": true,
        "true_delta": -0.19311778881199468
      },
      {
        "absolute_delta_error": 0.02144714403614545,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_purity",
        "predicted_delta": 0.019999999999999907,
        "resolved": false,
        "true_delta": -0.0014471440361455423
      },
      {
        "absolute_delta_error": 0.08902680472663707,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_size",
        "predicted_delta": -0.06,
        "resolved": true,
        "true_delta": 0.02902680472663708
      },
      {
        "absolute_delta_error": 0.7802675737116522,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.19,
        "resolved": true,
        "true_delta": -0.5902675737116523
      },
      {
        "absolute_delta_error": 0.020048436438670436,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_yield",
        "predicted_delta": 0.020000000000000018,
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
        "absolute_delta_error": 0.09022020934805375,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_size",
        "predicted_delta": 0.09,
        "resolved": false,
        "true_delta": -0.00022020934805375147
      },
      {
        "absolute_delta_error": 0.34936854990383653,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.37000000000000005,
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
        "absolute_delta_error": 0.00513214634082948,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.009999999999999898,
        "resolved": false,
        "true_delta": -0.004867853659170418
      },
      {
        "absolute_delta_error": 0.052379301835895474,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_size",
        "predicted_delta": -0.09,
        "resolved": true,
        "true_delta": -0.03762069816410452
      },
      {
        "absolute_delta_error": 0.2781013982893206,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.3,
        "resolved": true,
        "true_delta": 0.5781013982893206
      },
      {
        "absolute_delta_error": 0.1000603832856733,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_yield",
        "predicted_delta": -0.06000000000000005,
        "resolved": true,
        "true_delta": 0.04006038328567324
      },
      {
        "absolute_delta_error": 0.029468661285033892,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_purity",
        "predicted_delta": 0.020000000000000018,
        "resolved": false,
        "true_delta": -0.009468661285033875
      },
      {
        "absolute_delta_error": 0.0801029046475648,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_size",
        "predicted_delta": 0.04999999999999999,
        "resolved": true,
        "true_delta": -0.030102904647564807
      },
      {
        "absolute_delta_error": 0.7223941217008812,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.12,
        "resolved": true,
        "true_delta": 0.6023941217008812
      },
      {
        "absolute_delta_error": 0.04168442210246642,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_yield",
        "predicted_delta": 0.11199999999999999,
        "resolved": true,
        "true_delta": 0.1536844221024664
      },
      {
        "absolute_delta_error": 0.004527106938203129,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_purity",
        "predicted_delta": -0.010000000000000009,
        "resolved": true,
        "true_delta": -0.014527106938203138
      },
      {
        "absolute_delta_error": 0.004182525248908879,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_size",
        "predicted_delta": 0.010000000000000009,
        "resolved": true,
        "true_delta": 0.014182525248908888
      },
      {
        "absolute_delta_error": 0.04091092276400039,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.06000000000000001,
        "resolved": false,
        "true_delta": 0.01908907723599962
      },
      {
        "absolute_delta_error": 0.07103124947311257,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_yield",
        "predicted_delta": 0.09999999999999998,
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
        "absolute_delta_error": 0.08342635283571022,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_size",
        "predicted_delta": -0.11,
        "resolved": true,
        "true_delta": -0.026573647164289782
      },
      {
        "absolute_delta_error": 0.11090822043533582,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.48000000000000004,
        "resolved": true,
        "true_delta": 0.5909082204353359
      }
    ],
    "failures": [],
    "metrics": {
      "crystal_fines_fraction": {
        "coverage80": 0.5,
        "interval_score80": 2.5262914936784315,
        "interval_width": 0.4633333333333334,
        "mae": 0.3794912297993731,
        "n": 12,
        "planned": 12
      },
      "crystal_purity": {
        "coverage80": 0.75,
        "interval_score80": 0.13847309387141227,
        "interval_width": 0.12333333333333334,
        "mae": 0.04265656929239181,
        "n": 12,
        "planned": 12
      },
      "crystal_size": {
        "coverage80": 0.3333333333333333,
        "interval_score80": 0.4352035069225923,
        "interval_width": 0.19666666666666666,
        "mae": 0.09916028660324112,
        "n": 12,
        "planned": 12
      },
      "crystal_yield": {
        "coverage80": 0.3333333333333333,
        "interval_score80": 0.8689351196787851,
        "interval_width": 0.27458333333333335,
        "mae": 0.17649450100584205,
        "n": 12,
        "planned": 12
      }
    },
    "quality": {
      "balanced_accuracy": 0.5833333333333334,
      "false_negative": 1,
      "false_positive": 4,
      "true_negative": 2,
      "true_positive": 5
    },
    "resolved_direction_correct": 8,
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
        "crystal_purity": 0.004158550741177482,
        "crystal_size": 0.017192244486071477,
        "crystal_yield": 0.1061566327281832
      },
      "public_nearest_neighbor": {
        "crystal_fines_fraction": 0.2816153163486672,
        "crystal_purity": 0.00888393072654528,
        "crystal_size": 0.035086005630163945,
        "crystal_yield": 0.1293093022213478
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
        "cached_input": 491008,
        "input": 526863,
        "output": 7760,
        "stage": "source",
        "uncached_input": 35855
      },
      {
        "cached_input": 0,
        "input": 32044,
        "output": 3429,
        "stage": "K1",
        "uncached_input": 32044
      },
      {
        "cached_input": 3584,
        "input": 56493,
        "output": 2907,
        "stage": "Q",
        "uncached_input": 52909
      },
      {
        "cached_input": 0,
        "input": 59320,
        "output": 2125,
        "stage": "K2",
        "uncached_input": 59320
      }
    ],
    "total": {
      "cached_input": 494592,
      "input": 674720,
      "input_plus_output": 690941,
      "output": 16221,
      "uncached_input": 180128
    },
    "valid": true
  },
  "elapsed_s": 695.8910000000033
}
```
