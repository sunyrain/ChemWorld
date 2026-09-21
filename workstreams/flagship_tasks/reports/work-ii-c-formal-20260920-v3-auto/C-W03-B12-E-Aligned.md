# C-W03-B12-E-Aligned

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
      "stirring_speed_rpm": 600,
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
      "target_temperature_K": 278
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 278
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
    "byproduct_signal": 0.3717477023601532,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7526236176490784,
    "crystal_fines_fraction": 0.2958814203739166,
    "crystal_purity": 0.9876905083656311,
    "crystal_size": 0.08237281441688538,
    "crystal_yield": 0.42382484674453735,
    "degradation_warning": 0.19315007328987122,
    "safety_risk": 0.17965108156204224,
    "score": 0.5067126750946045,
    "selectivity": 0.5228960514068604,
    "virtual_spectrum_summary": 0.29137876629829407,
    "yield": 0.5207335948944092
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
  "end_step": 22,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.2799225151538849,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5628166794776917,
    "crystal_fines_fraction": 0.7388967871665955,
    "crystal_purity": 0.9790710806846619,
    "crystal_size": 0.09450750797986984,
    "crystal_yield": 0.47379758954048157,
    "degradation_warning": 0.08596953004598618,
    "safety_risk": 0.14236222207546234,
    "score": 0.44837725162506104,
    "selectivity": 0.5803638100624084,
    "virtual_spectrum_summary": 0.1926436722278595,
    "yield": 0.568912923336029
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
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 265
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
  "end_step": 32,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.32185977697372437,
    "conversion": 0.9983178973197937,
    "cost": 1.0,
    "crystal_csd_quality": 0.6690142154693604,
    "crystal_fines_fraction": 0.44648221135139465,
    "crystal_purity": 0.9900803565979004,
    "crystal_size": 0.06690257787704468,
    "crystal_yield": 0.431944340467453,
    "degradation_warning": 0.15746696293354034,
    "safety_risk": 0.16193810105323792,
    "score": 0.4799105226993561,
    "selectivity": 0.5378003716468811,
    "virtual_spectrum_summary": 0.24788300693035126,
    "yield": 0.5369130969047546
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
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 265
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
  "end_step": 42,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.3439888656139374,
    "conversion": 0.9889952540397644,
    "cost": 1.0,
    "crystal_csd_quality": 0.7084944248199463,
    "crystal_fines_fraction": 0.3614634573459625,
    "crystal_purity": 1.0,
    "crystal_size": 0.08414776623249054,
    "crystal_yield": 0.3869529962539673,
    "degradation_warning": 0.10625171661376953,
    "safety_risk": 0.17185179889202118,
    "score": 0.4748392701148987,
    "selectivity": 0.47655123472213745,
    "virtual_spectrum_summary": 0.23700714111328125,
    "yield": 0.46292099356651306
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
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 265
    },
    {
      "instrument": "particle_size",
      "operation": "measure"
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
  "end_step": 54,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.33536505699157715,
    "conversion": 0.996337890625,
    "cost": 1.0,
    "crystal_csd_quality": 0.7271534204483032,
    "crystal_fines_fraction": 0.33495083451271057,
    "crystal_purity": 0.9788765907287598,
    "crystal_size": 0.06573779135942459,
    "crystal_yield": 0.48285409808158875,
    "degradation_warning": 0.15865646302700043,
    "safety_risk": 0.18335027992725372,
    "score": 0.5171906352043152,
    "selectivity": 0.5707331895828247,
    "virtual_spectrum_summary": 0.25584620237350464,
    "yield": 0.5645802617073059
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
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 360
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 265
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
  "end_step": 66,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.39174383878707886,
    "conversion": 0.9924335479736328,
    "cost": 1.0,
    "crystal_csd_quality": 0.694554328918457,
    "crystal_fines_fraction": 0.36966532468795776,
    "crystal_purity": 1.0,
    "crystal_size": 0.05940405651926994,
    "crystal_yield": 0.46064019203186035,
    "degradation_warning": 0.23878854513168335,
    "safety_risk": 0.17928625643253326,
    "score": 0.4959219694137573,
    "selectivity": 0.5148588418960571,
    "virtual_spectrum_summary": 0.3229139447212219,
    "yield": 0.5167444348335266
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
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 360
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 265
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
  "end_step": 78,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.3228565454483032,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7346320152282715,
    "crystal_fines_fraction": 0.3038163483142853,
    "crystal_purity": 0.9805828928947449,
    "crystal_size": 0.09945747256278992,
    "crystal_yield": 0.5009058117866516,
    "degradation_warning": 0.15616446733474731,
    "safety_risk": 0.18283089995384216,
    "score": 0.5238835215568542,
    "selectivity": 0.5154454708099365,
    "virtual_spectrum_summary": 0.2478451132774353,
    "yield": 0.5420926213264465
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
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 360
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.001
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 265
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
  "end_step": 90,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.3151664733886719,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7706459164619446,
    "crystal_fines_fraction": 0.30235233902931213,
    "crystal_purity": 0.9808319211006165,
    "crystal_size": 0.11608128249645233,
    "crystal_yield": 0.5060374140739441,
    "degradation_warning": 0.16273236274719238,
    "safety_risk": 0.18271620571613312,
    "score": 0.5350101590156555,
    "selectivity": 0.5428815484046936,
    "virtual_spectrum_summary": 0.2465711236000061,
    "yield": 0.5345762968063354
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
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 265
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
    "byproduct_signal": 0.3256160616874695,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7459706664085388,
    "crystal_fines_fraction": 0.31661248207092285,
    "crystal_purity": 0.9830358624458313,
    "crystal_size": 0.06655611842870712,
    "crystal_yield": 0.49694451689720154,
    "degradation_warning": 0.15533596277236938,
    "safety_risk": 0.18270350992679596,
    "score": 0.520453155040741,
    "selectivity": 0.5206978917121887,
    "virtual_spectrum_summary": 0.2489900141954422,
    "yield": 0.5343738198280334
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
      "operation": "seed_crystals",
      "seed_mass_g": 0.001
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 265
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
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 285
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
  "end_step": 115,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.328185111284256,
    "conversion": 0.9858242273330688,
    "cost": 1.0,
    "crystal_csd_quality": 0.7029272317886353,
    "crystal_fines_fraction": 0.33322882652282715,
    "crystal_purity": 0.9789730906486511,
    "crystal_size": 0.07999885827302933,
    "crystal_yield": 0.49082428216934204,
    "degradation_warning": 0.17429770529270172,
    "safety_risk": 0.18180684745311737,
    "score": 0.5090315937995911,
    "selectivity": 0.5246397256851196,
    "virtual_spectrum_summary": 0.2589357793331146,
    "yield": 0.5335665345191956
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
      "solvent": 2,
      "volume_L": 0.04
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
      "target_temperature_K": 360
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.001
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 265
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
  "end_step": 127,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.3304983973503113,
    "conversion": 0.9990203976631165,
    "cost": 1.0,
    "crystal_csd_quality": 0.644207775592804,
    "crystal_fines_fraction": 0.5474740266799927,
    "crystal_purity": 0.9955735206604004,
    "crystal_size": 0.07417092472314835,
    "crystal_yield": 0.49803540110588074,
    "degradation_warning": 0.15205533802509308,
    "safety_risk": 0.20959365367889404,
    "score": 0.4793209731578827,
    "selectivity": 0.5453146696090698,
    "virtual_spectrum_summary": 0.25019901990890503,
    "yield": 0.525824785232544
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
      "target_temperature_K": 360
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.001
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 265
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
  "end_step": 140,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.3110092878341675,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7428771257400513,
    "crystal_fines_fraction": 0.3173324465751648,
    "crystal_purity": 0.9951622486114502,
    "crystal_size": 0.10739216953516006,
    "crystal_yield": 0.49197399616241455,
    "degradation_warning": 0.16552074253559113,
    "safety_risk": 0.18271620571613312,
    "score": 0.5254535675048828,
    "selectivity": 0.5287238359451294,
    "virtual_spectrum_summary": 0.24553945660591125,
    "yield": 0.5337658524513245
  },
  "ordinal": 12
}
```

## K1

```json
{
  "payload": {
    "report": "Mechanistic account\n\nObserved process and outcome\nThe recommended batch remains batch 8. It used 0.040 mol reagent in 0.080 L solvent-S2, 0.005 mol catalyst-C0, reaction at 360 K for 3600 s with 600 rpm stirring, 0.001 g seed, staged crystallization at 300 K for 7200 s, 265 K for 14400 s, and 250 K for 14400 s, followed by filtration. Its final assay gave reaction yield 0.535, selectivity 0.543, crystal recovery 0.506, purity 0.981, fines fraction 0.302, normalized crystal size 0.116, and CSD quality 0.771. It therefore met both constraints with substantial margin.\n\nMaterial effects\nThe solvent dossier describes S2 as having relatively low solubility (0.70), low nucleation tendency (0.65), high growth tendency (1.30), and low impurity occlusion (0.65). The observations are consistent with that combination: S2 repeatedly afforded high purity and fines well below 0.50 while permitting recovery near 0.50. For example, S2/C0 batches 5, 7, 8, 9, 10 and 12 had purities of about 0.979\u20130.995 and fines of about 0.302\u20130.335 under the standard 0.080 L charge.\n\nThe contrasting solvent trials support, but do not uniquely prove, this interpretation. S0 has the nominally highest nucleation tendency and impurity occlusion and lower growth tendency. Batch 2, using S0/C0 and direct cooling to 250 K, reached recovery 0.474 and purity 0.979 but produced a fines fraction of 0.739, clearly failing the particle constraint. S1 was intermediate: batch 3 gave recovery 0.432, purity 0.990 and fines 0.446. These trials also changed cooling endpoints, so the solvent attribution is partly confounded with process history.\n\nCatalyst effects appeared mainly in the reaction product pool. Under S2, batch 5 with C0 gave final reaction yield/selectivity of 0.565/0.571 and crystal recovery 0.483. Comparable C2 and C3 trials were weaker: batch 4 gave 0.463/0.477 and recovery 0.387, while batch 6 gave 0.517/0.515 and recovery 0.461. C1 in batch 1 gave 0.521/0.523 and recovery 0.424. Thus C0 was the best empirical choice, although the comparisons include different cooling histories and ordinary batch variability. The nominal catalyst panel alone would not have established this ordering.\n\nReaction\u2013crystallization coupling\nCrystal recovery is a conditional crystallization metric:\n\nR_crystal = n(target recovered as crystals, excluding seed) / n(target present before separation).\n\nIt is not overall yield from charged reagent. A useful approximate overall isolated-target fraction is\n\nY_isolated \u2248 Y_reaction \u00d7 R_crystal,\n\nprovided the two reported quantities share a compatible target basis. For batch 8 this is approximately 0.535 \u00d7 0.506 \u2248 0.271. Reaction selectivity controls the impurity burden presented to crystallization, whereas solvent-dependent solubility, nucleation, growth and occlusion determine how much target is recovered and how clean and coarse the crystals are.\n\nThe S2 process maintained high crystal purity despite final byproduct signals around 0.31\u20130.34 in several C0 batches. I interpret this as preferential target crystallization and low impurity occlusion rather than disappearance of reaction byproducts. This interpretation is supported by S2\u2019s material dossier but was not directly confirmed by separate solid and mother-liquor assays.\n\nProcess-history dependence\nCooling history mattered, not just final temperature. Batch 5 used the staged 300\u2192265\u2192250 K program and achieved recovery 0.483 with fines 0.335. The intermediate particle measurement after the 265 K stage showed fines 0.355, suggesting that the final cooling step increased recovery without triggering a fines excursion. Direct deep cooling can behave differently: batch 2 reached recovery 0.474 but generated fines 0.739 in the more nucleating S0 solvent.\n\nSeed amount showed a non-monotonic effect within the S2/C0 staged process. Reducing seed from 0.050 g in batch 5 to 0.010 g in batch 7 increased observed recovery from 0.483 to 0.501 and reduced fines from 0.335 to 0.304. Batch 8 at 0.001 g gave recovery 0.506, fines 0.302 and the largest observed normalized size, 0.116. Omitting seed entirely in batch 9 gave slightly lower recovery, 0.497, and fines 0.317. My interpretation is that excessive seed created too much growth surface or too many competing crystals, while a very small seed charge provided controlled nucleation without materially contributing to the seed-excluded numerator. Complete omission left nucleation more stochastic. This is an empirical interpretation rather than a demonstrated microscopic mechanism.\n\nThermal cycling did not help. After the standard staged sequence, batch 10 was reheated to 285 K for 3600 s and recooled to 250 K for 14400 s. Recovery fell to 0.491 and fines rose to 0.333 relative to batch 8. Partial dissolution followed by renucleation or loss of favorable crystal history is a plausible explanation. Likewise, simply adding another 14400 s controlled step at 250 K in batch 12 did not improve recovery: it gave 0.492, purity 0.995 and fines 0.317. Therefore the standard three-stage program was preferable to either cycling or extended terminal cooling.\n\nConcentration exposed the unresolved recovery\u2013particle-quality tradeoff. Batch 11 halved solvent volume to 0.040 L while keeping reagent and catalyst charges fixed. Recovery remained high at 0.498 and purity increased to 0.996, but fines rose to 0.547 and violated the limit. Higher supersaturation evidently promoted excessive nucleation. More concentrated operation could conceivably be rescued by slower cooling, different agitation or a tailored seed population, but those alternatives were not tested.\n\nRevisions and uncertainty\nThe campaign progressed from broad material/catalyst screening to staged-cooling and seed-dose refinement. Early batch 1 was feasible but gave only 0.424 recovery. Batch 2 demonstrated that maximizing supersaturation or using a strongly nucleating solvent could raise recovery while failing particle quality. Batches 5\u20139 established S2/C0 staged cooling and then located the low-seed region. Batches 10\u201312 tested thermal cycling, concentration and extended low-temperature treatment; none displaced batch 8.\n\nFinal-assay standard uncertainties were approximately 0.010 for crystal recovery and purity, 0.018 for fines and CSD quality, and 0.025 for normalized size. Consequently, the recovery difference between batches 8 and 7 (0.005) is not individually decisive, and the difference between batches 8 and 12 (0.014) is only modest. Batch 8 is best viewed as the highest observed feasible result, not proof of a sharply resolved optimum. Its constraint margins are much stronger than its ranking margin: purity exceeded the 0.80 threshold by about 0.18 and fines were about 0.20 below the 0.50 limit.\n\nUntested alternatives include finer temperature ramps, agitation changes during crystallization, intermediate seed doses around 0.001\u20130.010 g, and dilution levels between 0.040 and 0.080 L. These might improve recovery while retaining particle quality. The main unresolved tradeoff is that stronger supersaturation can preserve or raise recovery but promotes fines, whereas gentler nucleation and growth control protects CSD quality without guaranteeing additional recovery."
  },
  "failure": null,
  "elapsed_s": 54.296999999991385,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 952960,
    "input_tokens": 1074893,
    "output_tokens": 8518,
    "reasoning_output_tokens": 2570
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
          "estimate": 0.24,
          "lower80": 0.14,
          "upper80": 0.36
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.94,
          "upper80": 1
        },
        "crystal_size": {
          "estimate": 0.2,
          "lower80": 0.12,
          "upper80": 0.3
        },
        "crystal_yield": {
          "estimate": 0.35,
          "lower80": 0.26,
          "upper80": 0.44
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q01"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.4,
          "lower80": 0.27,
          "upper80": 0.55
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
          "estimate": 0.28,
          "lower80": 0.19,
          "upper80": 0.38
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q02"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.36,
          "lower80": 0.23,
          "upper80": 0.5
        },
        "crystal_purity": {
          "estimate": 0.96,
          "lower80": 0.91,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.22,
          "lower80": 0.13,
          "upper80": 0.33
        },
        "crystal_yield": {
          "estimate": 0.26,
          "lower80": 0.17,
          "upper80": 0.36
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q03"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.44,
          "lower80": 0.31,
          "upper80": 0.59
        },
        "crystal_purity": {
          "estimate": 0.95,
          "lower80": 0.9,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.16,
          "lower80": 0.09,
          "upper80": 0.25
        },
        "crystal_yield": {
          "estimate": 0.24,
          "lower80": 0.15,
          "upper80": 0.34
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
          "estimate": 0.95,
          "lower80": 0.9,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.17,
          "lower80": 0.1,
          "upper80": 0.27
        },
        "crystal_yield": {
          "estimate": 0.25,
          "lower80": 0.16,
          "upper80": 0.35
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q05"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.63,
          "lower80": 0.48,
          "upper80": 0.77
        },
        "crystal_purity": {
          "estimate": 0.94,
          "lower80": 0.88,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.11,
          "lower80": 0.05,
          "upper80": 0.2
        },
        "crystal_yield": {
          "estimate": 0.27,
          "lower80": 0.18,
          "upper80": 0.37
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q06"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.39,
          "lower80": 0.27,
          "upper80": 0.53
        },
        "crystal_purity": {
          "estimate": 0.96,
          "lower80": 0.91,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.19,
          "lower80": 0.11,
          "upper80": 0.29
        },
        "crystal_yield": {
          "estimate": 0.26,
          "lower80": 0.17,
          "upper80": 0.36
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q07"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.59,
          "lower80": 0.43,
          "upper80": 0.74
        },
        "crystal_purity": {
          "estimate": 0.96,
          "lower80": 0.9,
          "upper80": 1
        },
        "crystal_size": {
          "estimate": 0.11,
          "lower80": 0.05,
          "upper80": 0.2
        },
        "crystal_yield": {
          "estimate": 0.2,
          "lower80": 0.11,
          "upper80": 0.3
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q08"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.88,
          "lower80": 0.7,
          "upper80": 0.98
        },
        "crystal_purity": {
          "estimate": 0.94,
          "lower80": 0.84,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.03,
          "lower80": 0.005,
          "upper80": 0.08
        },
        "crystal_yield": {
          "estimate": 0.004,
          "lower80": 0,
          "upper80": 0.025
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q09"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.62,
          "lower80": 0.45,
          "upper80": 0.78
        },
        "crystal_purity": {
          "estimate": 0.95,
          "lower80": 0.87,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.08,
          "lower80": 0.03,
          "upper80": 0.16
        },
        "crystal_yield": {
          "estimate": 0.055,
          "lower80": 0.015,
          "upper80": 0.12
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q10"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.43,
          "lower80": 0.3,
          "upper80": 0.57
        },
        "crystal_purity": {
          "estimate": 0.95,
          "lower80": 0.9,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.17,
          "lower80": 0.1,
          "upper80": 0.27
        },
        "crystal_yield": {
          "estimate": 0.25,
          "lower80": 0.16,
          "upper80": 0.35
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q11"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.6,
          "lower80": 0.45,
          "upper80": 0.75
        },
        "crystal_purity": {
          "estimate": 0.93,
          "lower80": 0.86,
          "upper80": 0.98
        },
        "crystal_size": {
          "estimate": 0.12,
          "lower80": 0.06,
          "upper80": 0.21
        },
        "crystal_yield": {
          "estimate": 0.36,
          "lower80": 0.26,
          "upper80": 0.46
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q12"
      }
    ],
    "rationale": "Q01\u2013Q02 isolates solvent: S1's lower nominal solubility, lower nucleation tendency and lower occlusion should give higher recovery, larger particles, fewer fines and slightly higher purity than S3. Q03\u2013Q04 compares seed loading; campaign batches 5, 7 and 8 showed that reducing seed improved recovery, size and fines, although complete omission in batch 9 was slightly worse. Q05\u2013Q06 keeps total crystallization time approximately fixed: gradual cooling should suppress the nucleation burst and fines caused by an immediate drop to 278.15 K, while terminal recovery should be similar. Q07\u2013Q08 compares a final cold hold with reheating and rapid recooling; the latter is expected to dissolve part of the crop and regenerate fines, consistent with the deterioration from campaign batch 8 to thermally cycled batch 10. Q09\u2013Q10 tests residence time at only modest undercooling: seeds ensure particles are present, but 60 seconds should yield almost no seed-excluded product; two hours permits limited growth. Q11\u2013Q12 doubles concentration; it should increase recovery but also supersaturation, occlusion and fines, paralleling the fines failure of concentrated campaign batch 11. Intervals are deliberately broad because these recipes extrapolate to much longer cooling histories, different reaction conditions and S0-dominated solvent space; several fines intervals cross the 0.50 boundary."
  },
  "failure": null,
  "elapsed_s": 79.45300000000861,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 952960,
    "input_tokens": 1137859,
    "output_tokens": 12534,
    "reasoning_output_tokens": 4878
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
    "report": "1. Status of the main claims\n\nSupported by direct observations:\n- S2/C0 with staged cooling was the strongest tested platform. Batches 5, 7, 8, 9, 10 and 12 all used that platform at the standard dilution and produced purity around 0.979\u20130.995 with fines around 0.302\u20130.335. Batch 8 had the highest observed feasible recovery, 0.506.\n- Seed loading had a reproducible directional association under otherwise similar S2/C0 staged conditions. Recovery/fines changed from 0.483/0.335 at 0.050 g seed (batch 5), to 0.501/0.304 at 0.010 g (batch 7), and 0.506/0.302 at 0.001 g (batch 8). Omitting seed in batch 9 gave 0.497/0.317. This supports a low, nonzero seed region, although the recovery differences are comparable to assay uncertainty.\n- Stronger supersaturation created a quality penalty. Halving solvent volume in batch 11 produced recovery 0.498 but fines 0.547, versus fines near 0.30\u20130.34 for the standard-dilution S2/C0 batches.\n- Post-crystallization thermal manipulation did not improve the result. Reheating and recooling in batch 10 reduced recovery to 0.491 and increased fines to 0.333 relative to batch 8. An extra 250 K step in batch 12 also failed to improve recovery, giving 0.492 and fines 0.317.\n\nSupported, but confounded:\n- Solvent choice affected CSD. S0 in batch 2 gave fines 0.739, S1 in batch 3 gave 0.446, and standard-volume S2 trials generally gave 0.30\u20130.37. However, catalyst, seed and cooling programs were not fully matched, so assigning the differences specifically to nominal nucleation, growth and occlusion properties remains an interpretation.\n- C0 appeared preferable among catalysts. Under S2, batch 5 with C0 outperformed C2 in batch 4 and C3 in batch 6 in recovery and reaction metrics. Batch 1 with C1 was also weaker. The histories were not identical, and repeated C0 batches showed substantial variation in final selectivity, so a clean catalyst ranking was not established.\n\nContradicted or qualified:\n- A simple claim that higher concentration necessarily lowers purity is contradicted by batch 11: its purity was 0.996, higher rather than lower. The demonstrated concentration penalty was fines, not purity.\n- A claim that more time at the lowest temperature necessarily increases recovery is contradicted by batch 12. Its additional 250 K residence did not beat batch 8.\n- The proposed microscopic explanation that excessive seed creates too many competing crystals is not directly demonstrated. The dose-response observations support it, but alternative explanations include batch variability, seed-size-distribution effects and nonlinear assay noise.\n\nStill untested:\n- Preferential impurity rejection was inferred from high crystal purity despite appreciable byproduct signals, but separate solid and mother-liquor compositions were not measured.\n- The approximate relationship Y_isolated \u2248 Y_reaction \u00d7 R_crystal was not validated by an independent overall mass balance.\n- Fine temperature ramps, crystallization agitation, seed-size distribution, intermediate dilution, and interactions among solvent, catalyst and cooling history remain untested.\n\n2. One additional experiment\n\nI would repeat batch 8 exactly\u2014S2/C0, 0.001 g seed and the 300\u2192265\u2192250 K staged program\u2014but add nondestructive particle-size measurements after each cooling stage, with HPLC immediately before seeding and the usual final assay after filtration.\n\nThis would distinguish three explanations:\n- Controlled seeded growth: particles should be detectable after the 300 K stage, median size should increase progressively, and fines should remain low as recovery develops. The final result should reproduce roughly 0.50 recovery and 0.30 fines.\n- Delayed spontaneous nucleation: little particle development would be observed at 300 K, followed by a sharp increase in particle count and fines at 265 or 250 K. That would weaken the claim that the 0.001 g seed itself controls the CSD.\n- Apparent superiority caused mainly by batch/assay variability: the intermediate trajectory could look reasonable but the final recovery might not reproduce the batch-8 advantage over batches 5, 7, 9 and 12. A materially lower repeat would show that the optimum is not sharply resolved.\n\nThe pre-seed HPLC result would also determine whether an anomalous reaction product pool, rather than crystallization conditions, contributed to batch 8.\n\n3. Least effectively used observation and least reliable prediction\n\nThe observation used least effectively was the disagreement between the in-situ particle measurement and final assay in batch 6. Before filtration it indicated fines 0.331 and size 0.0658, whereas the final assay gave fines 0.370 and size 0.0594. I treated the final values as definitive without fully using this discrepancy to quantify sampling, filtration and instrument uncertainty. It cautions against overinterpreting small CSD differences among batches 5, 7, 8, 9 and 12.\n\nQ09 is the least reliable held-out prediction. It filters only 60 seconds after a small 300\u2192292 K cooling step, so its recovered target is likely near zero and its measured particles would be dominated by the added seed. The campaign contained no analogous seed-dominated, near-zero-growth batch. Consequently, particles_present is plausible because seed was added, but the predicted seed-excluded recovery and especially the size and fines distribution depend on unobserved seed morphology and how the benchmark reports CSD when almost no new product has crystallized. Q08 is also uncertain because reheating to 315 K is a stronger extrapolation than the 285 K cycle tested in batch 10, but Q09 has the weaker empirical anchor."
  },
  "failure": null,
  "elapsed_s": 61.125,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 1004672,
    "input_tokens": 1204761,
    "output_tokens": 14954,
    "reasoning_output_tokens": 6001
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
    "selection_rationale": "Batch 8 gave the highest observed feasible seed-excluded crystal recovery (0.506), while comfortably meeting purity (0.981 >= 0.80) and fines (0.302 <= 0.50). Its low 0.001 g seed dose and staged 300/265/250 K cooling also produced the best overall score among tested batches."
  },
  "recommendation_recipe": {
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
        "duration_s": 3600,
        "operation": "heat",
        "stirring_speed_rpm": 600,
        "target_temperature_K": 360
      },
      {
        "operation": "seed_crystals",
        "seed_mass_g": 0.001
      },
      {
        "duration_s": 7200,
        "operation": "cool_crystallize",
        "target_temperature_K": 300
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 265
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
    "lifecycle_index": 8,
    "source_attempts": 12
  },
  "prediction_evaluation": {
    "contrasts": [
      {
        "absolute_delta_error": 0.07989151001544348,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_yield",
        "predicted_delta": -0.06999999999999995,
        "resolved": true,
        "true_delta": -0.14989151001544343
      },
      {
        "absolute_delta_error": 0.03064587911515071,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_purity",
        "predicted_delta": -0.030000000000000027,
        "resolved": false,
        "true_delta": 0.0006458791151506826
      },
      {
        "absolute_delta_error": 0.06938040150063503,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_size",
        "predicted_delta": -0.05000000000000002,
        "resolved": true,
        "true_delta": 0.01938040150063501
      },
      {
        "absolute_delta_error": 0.6883138299289018,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.16000000000000003,
        "resolved": true,
        "true_delta": -0.5283138299289017
      },
      {
        "absolute_delta_error": 0.019840782226429515,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_yield",
        "predicted_delta": -0.020000000000000018,
        "resolved": false,
        "true_delta": -0.00015921777357050249
      },
      {
        "absolute_delta_error": 0.019746054635378263,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_purity",
        "predicted_delta": -0.010000000000000009,
        "resolved": false,
        "true_delta": 0.009746054635378254
      },
      {
        "absolute_delta_error": 0.05281442889796413,
        "direction_correct": true,
        "factor": "seed",
        "metric": "crystal_size",
        "predicted_delta": -0.06,
        "resolved": true,
        "true_delta": -0.007185571102035868
      },
      {
        "absolute_delta_error": 0.08426690822029767,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.08000000000000002,
        "resolved": true,
        "true_delta": 0.16426690822029769
      },
      {
        "absolute_delta_error": 0.019547857564826104,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_yield",
        "predicted_delta": 0.020000000000000018,
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
        "absolute_delta_error": 0.01668654733429699,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_size",
        "predicted_delta": -0.06000000000000001,
        "resolved": true,
        "true_delta": -0.04331345266570302
      },
      {
        "absolute_delta_error": 0.41295396285845926,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.21000000000000002,
        "resolved": true,
        "true_delta": 0.6229539628584593
      },
      {
        "absolute_delta_error": 0.10437670725156425,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_yield",
        "predicted_delta": -0.06,
        "resolved": true,
        "true_delta": 0.04437670725156426
      },
      {
        "absolute_delta_error": 0.011056182794199176,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_purity",
        "predicted_delta": 0.0,
        "resolved": true,
        "true_delta": -0.011056182794199176
      },
      {
        "absolute_delta_error": 0.040294418729357004,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_size",
        "predicted_delta": -0.08,
        "resolved": true,
        "true_delta": -0.039705581270643
      },
      {
        "absolute_delta_error": 0.46037028724012596,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.19999999999999996,
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
        "absolute_delta_error": 0.02194368604118524,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_purity",
        "predicted_delta": 0.010000000000000009,
        "resolved": true,
        "true_delta": -0.01194368604118523
      },
      {
        "absolute_delta_error": 0.036101832298345224,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_size",
        "predicted_delta": 0.05,
        "resolved": true,
        "true_delta": 0.013898167701654779
      },
      {
        "absolute_delta_error": 0.32539272978183875,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.26,
        "resolved": false,
        "true_delta": 0.06539272978183874
      },
      {
        "absolute_delta_error": 0.09504321303990107,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_yield",
        "predicted_delta": 0.10999999999999999,
        "resolved": false,
        "true_delta": 0.014956786960098917
      },
      {
        "absolute_delta_error": 0.014828397249087133,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_purity",
        "predicted_delta": -0.019999999999999907,
        "resolved": false,
        "true_delta": -0.005171602750912774
      },
      {
        "absolute_delta_error": 0.02435687395732107,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_size",
        "predicted_delta": -0.05000000000000002,
        "resolved": true,
        "true_delta": -0.025643126042678946
      },
      {
        "absolute_delta_error": 0.4359895667604082,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.16999999999999998,
        "resolved": true,
        "true_delta": 0.6059895667604082
      }
    ],
    "failures": [],
    "metrics": {
      "crystal_fines_fraction": {
        "coverage80": 0.5833333333333334,
        "interval_score80": 1.6077709734475703,
        "interval_width": 0.28,
        "mae": 0.225371182119226,
        "n": 12,
        "planned": 12
      },
      "crystal_purity": {
        "coverage80": 0.8333333333333334,
        "interval_score80": 0.10861721497611228,
        "interval_width": 0.09916666666666667,
        "mae": 0.033762495238254774,
        "n": 12,
        "planned": 12
      },
      "crystal_size": {
        "coverage80": 0.4166666666666667,
        "interval_score80": 0.27893575369828105,
        "interval_width": 0.15625,
        "mae": 0.07401839879782503,
        "n": 12,
        "planned": 12
      },
      "crystal_yield": {
        "coverage80": 0.8333333333333334,
        "interval_score80": 0.1839019350688117,
        "interval_width": 0.16916666666666666,
        "mae": 0.040906950686184086,
        "n": 12,
        "planned": 12
      }
    },
    "quality": {
      "balanced_accuracy": 0.9166666666666667,
      "false_negative": 0,
      "false_positive": 1,
      "true_negative": 5,
      "true_positive": 6
    },
    "resolved_direction_correct": 10,
    "resolved_direction_n": 16,
    "tie_correct": 0,
    "tie_n": 8,
    "valid": true
  },
  "public_baselines": {
    "available": true,
    "mae": {
      "public_mean": {
        "crystal_fines_fraction": 0.3252069018022991,
        "crystal_purity": 0.004499061360382871,
        "crystal_size": 0.019191178217026515,
        "crystal_yield": 0.2606108806553204
      },
      "public_nearest_neighbor": {
        "crystal_fines_fraction": 0.3798734894340074,
        "crystal_purity": 0.004677450946011287,
        "crystal_size": 0.01778733118035024,
        "crystal_yield": 0.2147177281004905
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
        "cached_input": 952960,
        "input": 1022990,
        "output": 5991,
        "stage": "source",
        "uncached_input": 70030
      },
      {
        "cached_input": 0,
        "input": 51903,
        "output": 2527,
        "stage": "K1",
        "uncached_input": 51903
      },
      {
        "cached_input": 0,
        "input": 62966,
        "output": 4016,
        "stage": "Q",
        "uncached_input": 62966
      },
      {
        "cached_input": 51712,
        "input": 66902,
        "output": 2420,
        "stage": "K2",
        "uncached_input": 15190
      }
    ],
    "total": {
      "cached_input": 1004672,
      "input": 1204761,
      "input_plus_output": 1219715,
      "output": 14954,
      "uncached_input": 200089
    },
    "valid": true
  },
  "elapsed_s": 548.2179999999935
}
```
