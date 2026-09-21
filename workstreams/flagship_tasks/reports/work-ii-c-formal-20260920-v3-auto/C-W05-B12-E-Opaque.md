# C-W05-B12-E-Opaque

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
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
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
      "target_temperature_K": 278
    },
    {
      "duration_s": 7200,
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
  "end_step": 15,
  "lifecycle_index": 1,
  "metrics": {
    "byproduct_signal": 0.2882522642612457,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.49849259853363037,
    "crystal_fines_fraction": 0.9465445876121521,
    "crystal_purity": 0.9834206104278564,
    "crystal_size": 0.055346276611089706,
    "crystal_yield": 0.4375591278076172,
    "degradation_warning": 0.1159106120467186,
    "safety_risk": 0.1424834281206131,
    "score": 0.40549466013908386,
    "selectivity": 0.5894272923469543,
    "virtual_spectrum_summary": 0.21069853007793427,
    "yield": 0.5872647166252136
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
      "stirring_speed_rpm": 600,
      "target_temperature_K": 360
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 260
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
  "end_step": 26,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.28994110226631165,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.501655101776123,
    "crystal_fines_fraction": 0.9272621273994446,
    "crystal_purity": 0.9855473637580872,
    "crystal_size": 0.09054459631443024,
    "crystal_yield": 0.4494520127773285,
    "degradation_warning": 0.10184779763221741,
    "safety_risk": 0.14053423702716827,
    "score": 0.4111648201942444,
    "selectivity": 0.5746513605117798,
    "virtual_spectrum_summary": 0.20529910922050476,
    "yield": 0.5632059574127197
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
      "target_temperature_K": 310
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 260
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 300
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
  "end_step": 39,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.3084188997745514,
    "conversion": 0.9983165264129639,
    "cost": 1.0,
    "crystal_csd_quality": 0.4799211025238037,
    "crystal_fines_fraction": 0.9144781827926636,
    "crystal_purity": 0.9792885780334473,
    "crystal_size": 0.05026957765221596,
    "crystal_yield": 0.3709058463573456,
    "degradation_warning": 0.09320305287837982,
    "safety_risk": 0.13150130212306976,
    "score": 0.3727545738220215,
    "selectivity": 0.5092211365699768,
    "virtual_spectrum_summary": 0.21157178282737732,
    "yield": 0.508333146572113
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
      "target_temperature_K": 310
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
      "operation": "heat",
      "stirring_speed_rpm": 150,
      "target_temperature_K": 285
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
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.33983898162841797,
    "conversion": 0.9889965057373047,
    "cost": 1.0,
    "crystal_csd_quality": 0.48824000358581543,
    "crystal_fines_fraction": 0.9033674597740173,
    "crystal_purity": 1.0,
    "crystal_size": 0.060835134238004684,
    "crystal_yield": 0.428437203168869,
    "degradation_warning": 0.18230560421943665,
    "safety_risk": 0.13907712697982788,
    "score": 0.40353959798812866,
    "selectivity": 0.5664355158805847,
    "virtual_spectrum_summary": 0.2689489424228668,
    "yield": 0.5528058409690857
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
      "stirring_speed_rpm": 600,
      "target_temperature_K": 360
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
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
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.3112281560897827,
    "conversion": 0.9963377714157104,
    "cost": 1.0,
    "crystal_csd_quality": 0.6391382813453674,
    "crystal_fines_fraction": 0.5499668121337891,
    "crystal_purity": 0.9750174283981323,
    "crystal_size": 0.052847720682621,
    "crystal_yield": 0.4709751605987549,
    "degradation_warning": 0.12982377409934998,
    "safety_risk": 0.16623301804065704,
    "score": 0.47756853699684143,
    "selectivity": 0.5890973806381226,
    "virtual_spectrum_summary": 0.22959618270397186,
    "yield": 0.5829443335533142
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
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
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
    "byproduct_signal": 0.35956063866615295,
    "conversion": 0.9924328923225403,
    "cost": 1.0,
    "crystal_csd_quality": 0.6412249803543091,
    "crystal_fines_fraction": 0.5010508298873901,
    "crystal_purity": 0.9994930624961853,
    "crystal_size": 0.05158684775233269,
    "crystal_yield": 0.4147011339664459,
    "degradation_warning": 0.15796835720539093,
    "safety_risk": 0.17528745532035828,
    "score": 0.456136554479599,
    "selectivity": 0.49425622820854187,
    "virtual_spectrum_summary": 0.2688441276550293,
    "yield": 0.4961415231227875
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
      "stirring_speed_rpm": 600,
      "target_temperature_K": 360
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
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
  "end_step": 84,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.3656485080718994,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5758109092712402,
    "crystal_fines_fraction": 0.6683025360107422,
    "crystal_purity": 0.9682705998420715,
    "crystal_size": 0.08261433988809586,
    "crystal_yield": 0.3565952479839325,
    "degradation_warning": 0.15045525133609772,
    "safety_risk": 0.1811237335205078,
    "score": 0.4033612608909607,
    "selectivity": 0.4504229724407196,
    "virtual_spectrum_summary": 0.26881155371665955,
    "yield": 0.477070152759552
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
      "stirring_speed_rpm": 600,
      "target_temperature_K": 360
    },
    {
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 325
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 275
    },
    {
      "instrument": "particle_size",
      "operation": "measure"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 150,
      "target_temperature_K": 283
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
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.3006262481212616,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6657015681266785,
    "crystal_fines_fraction": 0.5243647694587708,
    "crystal_purity": 0.9775294065475464,
    "crystal_size": 0.10364099591970444,
    "crystal_yield": 0.4681321978569031,
    "degradation_warning": 0.14040380716323853,
    "safety_risk": 0.16439346969127655,
    "score": 0.48795321583747864,
    "selectivity": 0.5768485069274902,
    "virtual_spectrum_summary": 0.22852614521980286,
    "yield": 0.5685431957244873
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
      "stirring_speed_rpm": 600,
      "target_temperature_K": 360
    },
    {
      "duration_s": 3600,
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
      "target_temperature_K": 285
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
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.30222299695014954,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6611803770065308,
    "crystal_fines_fraction": 0.49759605526924133,
    "crystal_purity": 0.9798609614372253,
    "crystal_size": 0.056482285261154175,
    "crystal_yield": 0.4531748592853546,
    "degradation_warning": 0.12682153284549713,
    "safety_risk": 0.16418489813804626,
    "score": 0.4815761148929596,
    "selectivity": 0.5612670183181763,
    "virtual_spectrum_summary": 0.22329233586788177,
    "yield": 0.5749428868293762
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
      "stirring_speed_rpm": 600,
      "target_temperature_K": 360
    },
    {
      "duration_s": 3600,
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
      "target_temperature_K": 310
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 282
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
  "end_step": 119,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.2951001226902008,
    "conversion": 0.9858241677284241,
    "cost": 1.0,
    "crystal_csd_quality": 0.6321064829826355,
    "crystal_fines_fraction": 0.5029678344726562,
    "crystal_purity": 0.975762665271759,
    "crystal_size": 0.07093025743961334,
    "crystal_yield": 0.4618827998638153,
    "degradation_warning": 0.13822788000106812,
    "safety_risk": 0.16469702124595642,
    "score": 0.47912389039993286,
    "selectivity": 0.5723479390144348,
    "virtual_spectrum_summary": 0.22450760006904602,
    "yield": 0.581274688243866
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
      "stirring_speed_rpm": 600,
      "target_temperature_K": 360
    },
    {
      "duration_s": 3600,
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
      "target_temperature_K": 315
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 284
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
  "end_step": 132,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.30361470580101013,
    "conversion": 0.9990202784538269,
    "cost": 1.0,
    "crystal_csd_quality": 0.6522238850593567,
    "crystal_fines_fraction": 0.48357370495796204,
    "crystal_purity": 0.9908049702644348,
    "crystal_size": 0.07586567848920822,
    "crystal_yield": 0.44784262776374817,
    "degradation_warning": 0.11524789780378342,
    "safety_risk": 0.1643603891134262,
    "score": 0.4850834012031555,
    "selectivity": 0.5894454121589661,
    "virtual_spectrum_summary": 0.21884964406490326,
    "yield": 0.5699555277824402
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
      "stirring_speed_rpm": 600,
      "target_temperature_K": 360
    },
    {
      "duration_s": 3600,
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
      "target_temperature_K": 315
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 283
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
  "end_step": 145,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.2876162528991699,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6653733253479004,
    "crystal_fines_fraction": 0.4919326603412628,
    "crystal_purity": 0.9920109510421753,
    "crystal_size": 0.0976843312382698,
    "crystal_yield": 0.4533226490020752,
    "degradation_warning": 0.13700631260871887,
    "safety_risk": 0.16453120112419128,
    "score": 0.4898940920829773,
    "selectivity": 0.5688766837120056,
    "virtual_spectrum_summary": 0.21984177827835083,
    "yield": 0.5739186406135559
  },
  "ordinal": 12
}
```

## K1

```json
{
  "payload": {
    "report": "Mechanistic account\n\nRecommended process (unchanged): batch 12 used 0.040 mol limiting reagent, 0.080 L solvent-S1, and 0.005 mol catalyst-C0. The reaction was held at 360 K for 3,600 s with 600 rpm stirring. It was cooled to 330 K over 3,600 s, seeded with 0.050 g, and then cooled in three 14,400 s stages to 315, 300, and 283 K. The crystals were filtered immediately, without a warm hold. The final assay gave reaction yield 0.5739, selectivity 0.5689, crystal recovery 0.4533, purity 0.9920, fines fraction 0.4919, and normalized crystal size 0.0977 (approximately 24 \u00b5m by the published normalization). Thus it met purity \u22650.80 and fines \u22640.50.\n\nMaterial effects\n\nObservation: In the solvent-S0 catalyst screen, catalyst-C0 gave HPLC yield/selectivity of 0.593/0.599 in batch 1. C1 gave 0.520/0.549 in batch 2, and C2 gave 0.478/0.477 in batch 3. C3 was closer to C0 at 0.590/0.579 in batch 4. Interpretation: C0 and C3 better direct the reacted material toward target than C1 or C2 under the tested 360 K condition. C0 was retained because its performance was at least as strong and its downstream results showed less degradation than the thermally cycled C3 batch, although crystallization histories confound that latter comparison.\n\nObservation: With C0 fixed, solvent identity strongly changed both reaction and crystallization behavior. S1 in batch 5 produced crystal recovery 0.4710 with fines 0.5500; S2 in batch 6 gave lower recovery, 0.4147, but fines near the limit at 0.5011; S3 in batch 7 was inferior on both recovery and fines, 0.3566 and 0.6683. S0 batches had very high fines, approximately 0.90\u20130.95, despite several thermal histories. Interpretation: solvent-dependent target solubility and nucleation kinetics dominate the particle population. S1 offered the best recovery/fines compromise and became the optimization solvent. S2 may intrinsically suppress fines somewhat more, but at a substantial recovery and upstream-yield penalty.\n\nAn important untested alternative is a catalyst\u2013solvent interaction. Catalysts were screened only in S0 and solvents only with C0, so combinations such as C3/S1 were not tested. Accordingly, the catalyst and solvent effects should not be assumed perfectly separable.\n\nReaction\u2013crystallization coupling\n\nThe upstream reaction controls how much target and impurity enter crystallization, while crystallization determines what fraction of the available target is recovered and how much impurity is rejected. A useful approximate material-balance relation is\n\n  isolated target relative to charged reagent \u2248 reaction yield \u00d7 crystal recovery.\n\nFor batch 12 this is about 0.5739 \u00d7 0.4533 \u2248 0.260. Crystal recovery is specifically seed-excluded recovered target divided by target present before separation; it is not overall reaction yield.\n\nAll final crystal purities were high, roughly 0.968\u20131.000, even when reaction selectivity was only about 0.45\u20130.59. Observation: crystallization therefore rejected much of the soluble impurity under all tested conditions. Interpretation: the binding optimization constraint was particle number distribution, not chemical purity. However, lower upstream selectivity still reduces overall isolated target and may alter supersaturation or impurity-mediated nucleation.\n\nA conventional qualitative representation is\n\n  S = C/C*(T, solvent),\n  J \u2248 J0 exp[-B/(ln S)^2],\n  G \u2248 kg(S \u2212 1)^g,\n\nwhere S is supersaturation, J nucleation rate, and G crystal growth rate. Deep or rapid cooling raises S and recovery but can make J rise disproportionately, creating many particles below 20 \u00b5m. Controlled staging keeps supersaturation in a region favoring growth on introduced seeds rather than uncontrolled primary or secondary nucleation.\n\nProcess-history dependence\n\nObservation: Endpoint temperature alone did not determine the result. In S1, batch 5 was cooled from a 320 K seed point to 270 K and gave high recovery (0.4710) but excessive fines (0.5500). Batch 9 was seeded at 330 K and cooled to 285 K in one long stage; recovery fell to 0.4532 while final fines reached 0.4976. This was the first clearly specification-compliant batch.\n\nStaged cooling was then introduced. Batch 10 used stages to 310 and 282 K. Its in-process particle measurement reported fines 0.4816, but the final assay reported 0.5030, with recovery 0.4619. Batch 11 used 315, 300, and 284 K stages and finished at recovery 0.4478 and fines 0.4836. Batch 12 used the same staging but ended at 283 K, giving 0.4533 recovery and 0.4919 fines. Interpretation: gradual staged cooling reduced the kinetic overshoot into uncontrolled nucleation and allowed a slightly colder endpoint, and hence slightly more recovery, while remaining below the fines threshold.\n\nThermal cycling was not consistently beneficial. Batch 3 cooled to 260 K, reheated to 300 K, and recooled to 270 K, yet had only 0.3709 recovery and 0.9145 fines in S0. Batch 4 cooled to 250 K and annealed at 285 K but still had 0.9034 fines. In S1, batch 8 was measured at 275 K with fines 0.5190, then reheated to 283 K; its final normalized size increased, but fines remained about 0.5244 and recovery was 0.4681. Interpretation: mild reheating may dissolve some small particles and promote ripening, but the tested anneal did not reduce their number fraction enough. Once extensive secondary nucleation has occurred, reheating short of substantial dissolution may not reset the particle population.\n\nBatch 1 also illustrates why elapsed history matters: after cooling to 278 K, a nominal wait allowed the vessel to warm toward 293 K before filtration. Its recovery was 0.4376, so an uncontrolled warm hold can surrender product through redissolution. The recommended process therefore filters immediately at the final controlled temperature.\n\nRevisions during the campaign\n\nThe initial strategy emphasized reaction screening and deep cooling for recovery. Batches 1\u20134 showed that this created unacceptable fines in S0 regardless of catalyst or simple thermal cycling. Solvent screening in batches 5\u20137 identified S1/S2 as much more favorable particle environments. Optimization then moved from deep cooling and post-nucleation annealing (batch 8) to a warmer endpoint (batch 9), followed by deliberately staged cooling (batches 10\u201312). The final revision selected 283 K rather than 284\u2013285 K to recover slightly more target while retaining a measured fines value below 0.50.\n\nUncertainty and unresolved tradeoff\n\nEach process was run once, so material effects are not replicated. The declared final-assay noise scales are about 0.010 for crystal recovery and purity and 0.018 for fines; particle imaging has about 0.015 fines uncertainty. Consequently, recovery differences among batches 9, 11, and 12 are not statistically resolved. Batch 12 exceeds batch 9 in measured recovery by only 0.00015. It was preferred because its fines value, 0.4919, had a somewhat better nominal margin and agreed with its pre-filtration particle result of 0.4940, while purity was higher at 0.9920.\n\nThe fines constraint nevertheless remains marginal: batch 12 is only 0.0081 below the limit, less than one stated noise standard deviation. Batch 10 demonstrates this uncertainty directly\u2014particle imaging suggested 0.4816, whereas its final assay gave 0.5030. Instrument noise, sampling differences, and continued slurry evolution can all contribute. Thus batch 12 is the best observed feasible operating point, not proof of robust compliance in every repeat.\n\nThe unresolved tradeoff is that colder endpoints increase recovery but raise the number fraction of fines, whereas warmer endpoints provide a safer fines margin at lower recovery. A confirmation program would replicate batches 11 and 12 and test endpoints around 283\u2013286 K, preferably targeting a true fines fraction nearer 0.47 rather than operating directly at 0.50. Other untested alternatives include varying seed mass or seed-size distribution, applying controlled agitation during cooling, exploring longer growth-dominant holds without ambient warming, and testing C3/S1. These are hypotheses for future work, not conclusions from the sealed campaign."
  },
  "failure": null,
  "elapsed_s": 79.15600000001723,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 677120,
    "input_tokens": 746171,
    "output_tokens": 10984,
    "reasoning_output_tokens": 3723
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
          "lower80": 0.12,
          "upper80": 0.38
        },
        "crystal_purity": {
          "estimate": 0.985,
          "lower80": 0.95,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.165,
          "lower80": 0.11,
          "upper80": 0.22
        },
        "crystal_yield": {
          "estimate": 0.42,
          "lower80": 0.32,
          "upper80": 0.52
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q01"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.38,
          "lower80": 0.22,
          "upper80": 0.55
        },
        "crystal_purity": {
          "estimate": 0.97,
          "lower80": 0.92,
          "upper80": 0.995
        },
        "crystal_size": {
          "estimate": 0.125,
          "lower80": 0.07,
          "upper80": 0.18
        },
        "crystal_yield": {
          "estimate": 0.3,
          "lower80": 0.18,
          "upper80": 0.42
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q02"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.68,
          "lower80": 0.48,
          "upper80": 0.84
        },
        "crystal_purity": {
          "estimate": 0.976,
          "lower80": 0.93,
          "upper80": 0.998
        },
        "crystal_size": {
          "estimate": 0.06,
          "lower80": 0.025,
          "upper80": 0.105
        },
        "crystal_yield": {
          "estimate": 0.41,
          "lower80": 0.3,
          "upper80": 0.52
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q03"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.27,
          "lower80": 0.14,
          "upper80": 0.42
        },
        "crystal_purity": {
          "estimate": 0.982,
          "lower80": 0.95,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.155,
          "lower80": 0.1,
          "upper80": 0.21
        },
        "crystal_yield": {
          "estimate": 0.43,
          "lower80": 0.33,
          "upper80": 0.53
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q04"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.29,
          "lower80": 0.15,
          "upper80": 0.44
        },
        "crystal_purity": {
          "estimate": 0.982,
          "lower80": 0.95,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.15,
          "lower80": 0.095,
          "upper80": 0.21
        },
        "crystal_yield": {
          "estimate": 0.42,
          "lower80": 0.32,
          "upper80": 0.52
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q05"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.58,
          "lower80": 0.38,
          "upper80": 0.76
        },
        "crystal_purity": {
          "estimate": 0.979,
          "lower80": 0.94,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.075,
          "lower80": 0.035,
          "upper80": 0.12
        },
        "crystal_yield": {
          "estimate": 0.44,
          "lower80": 0.34,
          "upper80": 0.54
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q06"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.31,
          "lower80": 0.16,
          "upper80": 0.47
        },
        "crystal_purity": {
          "estimate": 0.981,
          "lower80": 0.945,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.145,
          "lower80": 0.09,
          "upper80": 0.205
        },
        "crystal_yield": {
          "estimate": 0.43,
          "lower80": 0.33,
          "upper80": 0.53
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q07"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.47,
          "lower80": 0.27,
          "upper80": 0.67
        },
        "crystal_purity": {
          "estimate": 0.982,
          "lower80": 0.945,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.12,
          "lower80": 0.065,
          "upper80": 0.18
        },
        "crystal_yield": {
          "estimate": 0.36,
          "lower80": 0.23,
          "upper80": 0.49
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q08"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.72,
          "lower80": 0.48,
          "upper80": 0.9
        },
        "crystal_purity": {
          "estimate": 0.995,
          "lower80": 0.94,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.07,
          "lower80": 0.025,
          "upper80": 0.115
        },
        "crystal_yield": {
          "estimate": 0.035,
          "lower80": 0.0,
          "upper80": 0.1
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q09"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.54,
          "lower80": 0.32,
          "upper80": 0.73
        },
        "crystal_purity": {
          "estimate": 0.991,
          "lower80": 0.95,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.095,
          "lower80": 0.045,
          "upper80": 0.15
        },
        "crystal_yield": {
          "estimate": 0.12,
          "lower80": 0.04,
          "upper80": 0.22
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q10"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.27,
          "lower80": 0.14,
          "upper80": 0.42
        },
        "crystal_purity": {
          "estimate": 0.983,
          "lower80": 0.95,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.155,
          "lower80": 0.1,
          "upper80": 0.215
        },
        "crystal_yield": {
          "estimate": 0.43,
          "lower80": 0.33,
          "upper80": 0.53
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q11"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.52,
          "lower80": 0.33,
          "upper80": 0.7
        },
        "crystal_purity": {
          "estimate": 0.965,
          "lower80": 0.91,
          "upper80": 0.995
        },
        "crystal_size": {
          "estimate": 0.105,
          "lower80": 0.06,
          "upper80": 0.16
        },
        "crystal_yield": {
          "estimate": 0.59,
          "lower80": 0.48,
          "upper80": 0.7
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q12"
      }
    ],
    "rationale": "Q01\u2013Q02 isolates solvent identity: prior evidence favored S1 over S3 for recovery and fines, although both benefit from the exceptionally slow cooling. Q03\u2013Q04 isolates seed charge; the larger seed population should redirect supersaturation into seeded growth, producing larger particles and fewer fines with little change in equilibrium recovery. Q05\u2013Q06 contrasts gradual cooling with a rapid temperature shock followed by a long cold hold: the hold can recover similar mass, but it cannot reliably erase the large population created during the initial supersaturation spike. Q07\u2013Q08 tests a late thermal cycle; heating to 315 K should redissolve part of the crop, and the rapid recooling leaves less time to recover mass and may regenerate fines, making Q08 marginal. Q09\u2013Q10 tests residence time at 292 K: particles remain present because seed was added, but immediate filtration gives very little seed-excluded recovery; the two-hour hold increases growth and recovery without confidently meeting the fines limit. Q11\u2013Q12 doubles reagent concentration. Higher loading raises attainable recovery but also supersaturation, secondary nucleation, impurity incorporation, and fines, so Q12 is predicted to cross the fines threshold. Intervals are deliberately broad because these recipes extrapolate to much lower catalyst/solute charge, much longer cooling histories, and unreplicated conditions; classifications near fines=0.50 are correspondingly uncertain."
  },
  "failure": null,
  "elapsed_s": 91.60899999999674,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 677120,
    "input_tokens": 789576,
    "output_tokens": 15188,
    "reasoning_output_tokens": 6218
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
    "report": "1. Status of the main claims\n\nSupported by direct observations:\n- Solvent identity materially affected recovery and particle quality. Under the common C0 reaction and similar crystallization program, batch 5 (S1) gave recovery 0.4710 and fines 0.5500, batch 6 (S2) gave 0.4147 and 0.5011, and batch 7 (S3) gave 0.3566 and 0.6683. Thus S1 had the best observed recovery and S3 was inferior. Interpreting this as a solvent-dependent solubility/nucleation effect is plausible, but those physical properties were not measured directly.\n- Catalyst identity affected the upstream reaction. In the S0 HPLC screen, C0/C3 gave yields of 0.593/0.590 in batches 1/4, versus 0.520 for C1 in batch 2 and 0.478 for C2 in batch 3. This directly supports a catalyst effect on reaction performance. It does not establish a universal C0 ranking because only S0 was used.\n- Chemical purity was not the binding constraint. Final crystal purities across batches 1\u201312 were approximately 0.968\u20131.000, while fines frequently exceeded 0.50. That is a direct observation.\n- A feasible recovery\u2013fines boundary was found in S1. Batches 9, 11, and 12 all met the stated limits, with recoveries of 0.4532, 0.4478, and 0.4533 and fines of 0.4976, 0.4836, and 0.4919, respectively.\n\nSupported only conditionally or contradicted by some observations:\n- The interpretation that staged cooling itself suppresses fines is suggestive, not cleanly demonstrated. Staged batches 11 and 12 passed, but the single-stage batch 9 also passed, while staged batch 10 failed narrowly at fines 0.5030. Endpoint temperature, elapsed time, process noise, and assay noise were not independently controlled.\n- Post-nucleation reheating did not reliably remove fines. In batch 8, fines were 0.5190 before reheating and 0.5244 by final assay. Thermally cycled S0 batches 3 and 4 also remained highly fines-rich at 0.9145 and 0.9034. This contradicts any strong claim that the tested anneals were sufficient to repair an already nucleated population.\n- A simple monotonic relation between colder endpoint and higher recovery is not resolved. The broad trend is physically plausible, but batch-to-batch differences near the boundary were comparable to measurement noise and involved different histories.\n- C0 was not proven superior to C3. Their HPLC results were very close, and their downstream batches had different crystallization histories. Selecting C0 was operationally reasonable but not a clean mechanistic conclusion.\n\nStill untested:\n- Catalyst\u2013solvent interactions, including C3/S1.\n- Seed-mass and seed-size effects; campaign batches all received essentially the same effective 0.050 g seed charge.\n- Whether staged ramps outperform a direct ramp when endpoint and total elapsed time are exactly matched.\n- Effects of quenching, large concentration changes, very short crystallization, multi-day cold holds, and controlled crystallization agitation. These appear in the held-out recipes but were outside the campaign evidence.\n- Repeatability and robust compliance. Batch 12\u2019s fines margin was smaller than one declared assay standard deviation.\n\n2. One additional experiment\n\nI would repeat the batch-12 chemistry exactly, including S1, C0, charge, reaction, 330 K seed point, and 0.050 g seed, but replace the three-stage 330\u2192315\u2192300\u2192283 K cooling path with a direct 330\u2192283 K ramp over 14,400 s followed by two 14,400 s isothermal cool-crystallize holds at 283 K. I would make one particle-size measurement immediately before filtration and then perform the final assay.\n\nThis keeps final temperature and total post-seeding time approximately matched while changing when high supersaturation is encountered. It distinguishes two explanations:\n- Supersaturation-history explanation: gradual staging prevents an early nucleation burst. The direct-ramp experiment should then have smaller crystals and fines above batch 12, potentially above 0.50, while recovery remains similar or slightly higher.\n- Endpoint/aging explanation: final temperature and total residence dominate, and extended low-temperature aging erases the earlier path. The experiment should then converge toward batch 12 in recovery, size, and fines, or even show fewer fines if low-temperature ripening dominates.\n\nA result with initially high fines that subsequently fall during the holds would support ripening; persistent high fines would support irreversible early nucleation. One experiment cannot establish reproducibility, but this comparison would address the principal mechanistic ambiguity more directly than another unconstrained optimization run.\n\n3. Weakest use of evidence and least reliable prediction\n\nThe observation used least effectively was batch 1\u2019s warming during the post-cooling wait. The vessel warmed from 278 K toward 293 K before filtration, and I interpreted its 0.4376 recovery as evidence of redissolution during an uncontrolled warm hold. The warming was directly observed, but the causal conclusion was weak because there was no otherwise identical immediate-filtration control. Catalyst identity, cooling history, and assay variability also differed from the most relevant comparison batches.\n\nQ09 is the least reliable held-out prediction. It has only a 60 s cooling step to 292 K followed by immediate filtration, with a large seed charge relative to the small reagent charge. The campaign never sampled this seed-dominated, extremely short kinetic regime. Particles should be present because seed was deliberately added, but seed-excluded recovery could remain near zero while measured size and fines are governed mainly by the unknown initial seed distribution rather than newly crystallized product. Consequently, my numerical Q09 yield, size, fines, and its infeasible classification rely on extrapolation rather than a close campaign analogue."
  },
  "failure": null,
  "elapsed_s": 64.93799999999464,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 708736,
    "input_tokens": 837105,
    "output_tokens": 17630,
    "reasoning_output_tokens": 7363
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
    "selected_experiment_index": 12,
    "selection_rationale": "Batch 12 delivered the highest measured crystal recovery among batches meeting both specifications: crystal_yield 0.4533, crystal_purity 0.9920, and fines fraction 0.4919. Its staged slow cooling also gave a more robust fines margin than batch 9 at essentially the same recovery."
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
        "stirring_speed_rpm": 600,
        "target_temperature_K": 360
      },
      {
        "duration_s": 3600,
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
        "target_temperature_K": 315
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 300
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 283
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
    "lifecycle_index": 12,
    "source_attempts": 13
  },
  "prediction_evaluation": {
    "contrasts": [
      {
        "absolute_delta_error": 0.0892231216822536,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_yield",
        "predicted_delta": -0.12,
        "resolved": true,
        "true_delta": -0.2092231216822536
      },
      {
        "absolute_delta_error": 0.014852228504271037,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_purity",
        "predicted_delta": -0.015000000000000013,
        "resolved": false,
        "true_delta": -0.00014777149572897663
      },
      {
        "absolute_delta_error": 0.04711719918353845,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_size",
        "predicted_delta": -0.04000000000000001,
        "resolved": true,
        "true_delta": 0.007117199183538439
      },
      {
        "absolute_delta_error": 0.41661623193981456,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.14,
        "resolved": true,
        "true_delta": -0.27661623193981455
      },
      {
        "absolute_delta_error": 0.020132329809087884,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_yield",
        "predicted_delta": 0.020000000000000018,
        "resolved": false,
        "true_delta": -0.00013232980908786662
      },
      {
        "absolute_delta_error": 0.0031563952629243275,
        "direction_correct": true,
        "factor": "seed",
        "metric": "crystal_purity",
        "predicted_delta": 0.006000000000000005,
        "resolved": false,
        "true_delta": 0.009156395262924333
      },
      {
        "absolute_delta_error": 0.09997943907987049,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_size",
        "predicted_delta": 0.095,
        "resolved": false,
        "true_delta": -0.004979439079870487
      },
      {
        "absolute_delta_error": 0.5434195253798536,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.41000000000000003,
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
        "absolute_delta_error": 0.000772133174962053,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.0030000000000000027,
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
        "absolute_delta_error": 0.32381528795023257,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.29,
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
        "absolute_delta_error": 0.011377514631150332,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_purity",
        "predicted_delta": 0.0010000000000000009,
        "resolved": true,
        "true_delta": -0.01037751463115033
      },
      {
        "absolute_delta_error": 0.014855353017309905,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_size",
        "predicted_delta": -0.024999999999999994,
        "resolved": true,
        "true_delta": -0.0398553530173099
      },
      {
        "absolute_delta_error": 0.4899421779987409,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.15999999999999998,
        "resolved": true,
        "true_delta": 0.6499421779987409
      },
      {
        "absolute_delta_error": 0.021149758804529337,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_yield",
        "predicted_delta": 0.08499999999999999,
        "resolved": true,
        "true_delta": 0.10614975880452933
      },
      {
        "absolute_delta_error": 0.008280020877195815,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_purity",
        "predicted_delta": -0.0040000000000000036,
        "resolved": true,
        "true_delta": -0.012280020877195819
      },
      {
        "absolute_delta_error": 0.0122741883094254,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_size",
        "predicted_delta": 0.024999999999999994,
        "resolved": true,
        "true_delta": 0.012725811690574594
      },
      {
        "absolute_delta_error": 0.2225302662574824,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.17999999999999994,
        "resolved": false,
        "true_delta": 0.04253026625748246
      },
      {
        "absolute_delta_error": 0.1450659576177837,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_yield",
        "predicted_delta": 0.15999999999999998,
        "resolved": false,
        "true_delta": 0.014934042382216267
      },
      {
        "absolute_delta_error": 0.012890313202054804,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_purity",
        "predicted_delta": -0.018000000000000016,
        "resolved": false,
        "true_delta": -0.005109686797945212
      },
      {
        "absolute_delta_error": 0.021661601610355165,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_size",
        "predicted_delta": -0.05,
        "resolved": true,
        "true_delta": -0.028338398389644838
      },
      {
        "absolute_delta_error": 0.352412437007269,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.25,
        "resolved": true,
        "true_delta": 0.602412437007269
      }
    ],
    "failures": [],
    "metrics": {
      "crystal_fines_fraction": {
        "coverage80": 0.25,
        "interval_score80": 2.1530167466016894,
        "interval_width": 0.3408333333333333,
        "mae": 0.3355401678675787,
        "n": 12,
        "planned": 12
      },
      "crystal_purity": {
        "coverage80": 1.0,
        "interval_score80": 0.059000000000000025,
        "interval_width": 0.059000000000000025,
        "mae": 0.006509769623227117,
        "n": 12,
        "planned": 12
      },
      "crystal_size": {
        "coverage80": 0.25,
        "interval_score80": 0.18880990383269128,
        "interval_width": 0.10416666666666667,
        "mae": 0.05671888595330369,
        "n": 12,
        "planned": 12
      },
      "crystal_yield": {
        "coverage80": 0.3333333333333333,
        "interval_score80": 0.8277142536659251,
        "interval_width": 0.20166666666666666,
        "mae": 0.14863883591679258,
        "n": 12,
        "planned": 12
      }
    },
    "quality": {
      "balanced_accuracy": 0.6857142857142857,
      "false_negative": 1,
      "false_positive": 3,
      "true_negative": 4,
      "true_positive": 4
    },
    "resolved_direction_correct": 9,
    "resolved_direction_n": 15,
    "tie_correct": 2,
    "tie_n": 9,
    "valid": true
  },
  "public_baselines": {
    "available": true,
    "mae": {
      "public_mean": {
        "crystal_fines_fraction": 0.2923835950379527,
        "crystal_purity": 0.0048820147241982565,
        "crystal_size": 0.018173911536121575,
        "crystal_yield": 0.2176372414528084
      },
      "public_nearest_neighbor": {
        "crystal_fines_fraction": 0.3055779892323702,
        "crystal_purity": 0.005671363030896816,
        "crystal_size": 0.023936597194210027,
        "crystal_yield": 0.2252586713134003
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
        "cached_input": 677120,
        "input": 714428,
        "output": 7858,
        "stage": "source",
        "uncached_input": 37308
      },
      {
        "cached_input": 0,
        "input": 31743,
        "output": 3126,
        "stage": "K1",
        "uncached_input": 31743
      },
      {
        "cached_input": 0,
        "input": 43405,
        "output": 4204,
        "stage": "Q",
        "uncached_input": 43405
      },
      {
        "cached_input": 31616,
        "input": 47529,
        "output": 2442,
        "stage": "K2",
        "uncached_input": 15913
      }
    ],
    "total": {
      "cached_input": 708736,
      "input": 837105,
      "input_plus_output": 854735,
      "output": 17630,
      "uncached_input": 128369
    },
    "valid": true
  },
  "elapsed_s": 550.6100000000151
}
```
