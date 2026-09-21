# C-W04-B12-E-MisIndexed

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
      "duration_s": 10800,
      "operation": "cool_crystallize",
      "target_temperature_K": 275
    },
    {
      "duration_s": 7200,
      "operation": "wait",
      "stirring_speed_rpm": 150
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
    "byproduct_signal": 0.3587149381637573,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5086105465888977,
    "crystal_fines_fraction": 0.9973055124282837,
    "crystal_purity": 0.9871428608894348,
    "crystal_size": 0.054121922701597214,
    "crystal_yield": 0.38145506381988525,
    "degradation_warning": 0.16667954623699188,
    "safety_risk": 0.1738763451576233,
    "score": 0.36629483103752136,
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
      "seed_mass_g": 0.001
    },
    {
      "duration_s": 14400,
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
  "end_step": 24,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.44098320603370667,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5559967756271362,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9711803793907166,
    "crystal_size": 0.07397207617759705,
    "crystal_yield": 0.2263304591178894,
    "degradation_warning": 0.17878149449825287,
    "safety_risk": 0.15715385973453522,
    "score": 0.3115253150463104,
    "selectivity": 0.3512682616710663,
    "virtual_spectrum_summary": 0.3229924440383911,
    "yield": 0.33982324600219727
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
      "duration_s": 5400,
      "operation": "heat",
      "stirring_speed_rpm": 350,
      "target_temperature_K": 350
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
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
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
  "end_step": 38,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.4263468086719513,
    "conversion": 0.9983179569244385,
    "cost": 1.0,
    "crystal_csd_quality": 0.5462138056755066,
    "crystal_fines_fraction": 0.9949296116828918,
    "crystal_purity": 0.9787870049476624,
    "crystal_size": 0.03788679093122482,
    "crystal_yield": 0.22416271269321442,
    "degradation_warning": 0.1928683966398239,
    "safety_risk": 0.15774670243263245,
    "score": 0.30976709723472595,
    "selectivity": 0.3570276200771332,
    "virtual_spectrum_summary": 0.3212815225124359,
    "yield": 0.3561403453350067
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 330
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
      "target_temperature_K": 275
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
  "end_step": 52,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.4370439350605011,
    "conversion": 0.9889965057373047,
    "cost": 1.0,
    "crystal_csd_quality": 0.5370208024978638,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 1.0,
    "crystal_size": 0.04664010554552078,
    "crystal_yield": 0.24818454682826996,
    "degradation_warning": 0.17356029152870178,
    "safety_risk": 0.15729394555091858,
    "score": 0.3145487308502197,
    "selectivity": 0.3453017771244049,
    "virtual_spectrum_summary": 0.31847628951072693,
    "yield": 0.3316721022129059
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
      "stirring_speed_rpm": 300,
      "target_temperature_K": 355
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 325
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.005
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
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.3926814794540405,
    "conversion": 0.996337890625,
    "cost": 1.0,
    "crystal_csd_quality": 0.7666676640510559,
    "crystal_fines_fraction": 0.30307313799858093,
    "crystal_purity": 0.9785652756690979,
    "crystal_size": 0.06639106571674347,
    "crystal_yield": 0.3999786078929901,
    "degradation_warning": 0.17243272066116333,
    "safety_risk": 0.1760730743408203,
    "score": 0.48985743522644043,
    "selectivity": 0.4738648235797882,
    "virtual_spectrum_summary": 0.29356953501701355,
    "yield": 0.467711865901947
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
      "stirring_speed_rpm": 300,
      "target_temperature_K": 355
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 325
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.005
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
  "end_step": 76,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.3831600546836853,
    "conversion": 0.9924335479736328,
    "cost": 1.0,
    "crystal_csd_quality": 0.7524839043617249,
    "crystal_fines_fraction": 0.29423895478248596,
    "crystal_purity": 1.0,
    "crystal_size": 0.06116635724902153,
    "crystal_yield": 0.4277583658695221,
    "degradation_warning": 0.1702493131160736,
    "safety_risk": 0.17770524322986603,
    "score": 0.49693000316619873,
    "selectivity": 0.4605916738510132,
    "virtual_spectrum_summary": 0.28735020756721497,
    "yield": 0.46247726678848267
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
      "stirring_speed_rpm": 300,
      "target_temperature_K": 355
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 325
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
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.36578822135925293,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7608477473258972,
    "crystal_fines_fraction": 0.2539049983024597,
    "crystal_purity": 0.9814656376838684,
    "crystal_size": 0.10110238194465637,
    "crystal_yield": 0.45027199387550354,
    "degradation_warning": 0.15623266994953156,
    "safety_risk": 0.17946480214595795,
    "score": 0.5095404982566833,
    "selectivity": 0.4489373564720154,
    "virtual_spectrum_summary": 0.271488219499588,
    "yield": 0.47558456659317017
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 355
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 325
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
  "end_step": 100,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.35809817910194397,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7945882081985474,
    "crystal_fines_fraction": 0.25406044721603394,
    "crystal_purity": 0.98176109790802,
    "crystal_size": 0.11778657138347626,
    "crystal_yield": 0.455403596162796,
    "degradation_warning": 0.16280055046081543,
    "safety_risk": 0.179418683052063,
    "score": 0.5204518437385559,
    "selectivity": 0.4784550070762634,
    "virtual_spectrum_summary": 0.2702142298221588,
    "yield": 0.4701497554779053
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
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 355
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 325
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
  "end_step": 111,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.3685477375984192,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7697651386260986,
    "crystal_fines_fraction": 0.26850613951683044,
    "crystal_purity": 0.9839649200439453,
    "crystal_size": 0.06827033311128616,
    "crystal_yield": 0.44631069898605347,
    "degradation_warning": 0.15540415048599243,
    "safety_risk": 0.17940717935562134,
    "score": 0.5058475136756897,
    "selectivity": 0.45627132058143616,
    "virtual_spectrum_summary": 0.2726331353187561,
    "yield": 0.46994727849960327
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
      "stirring_speed_rpm": 300,
      "target_temperature_K": 355
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 325
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
  "end_step": 125,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.3941855728626251,
    "conversion": 0.9858242273330688,
    "cost": 1.0,
    "crystal_csd_quality": 0.7351922392845154,
    "crystal_fines_fraction": 0.2784321904182434,
    "crystal_purity": 0.9798502922058105,
    "crystal_size": 0.08219706267118454,
    "crystal_yield": 0.4474277198314667,
    "degradation_warning": 0.1766868382692337,
    "safety_risk": 0.17918850481510162,
    "score": 0.49815890192985535,
    "selectivity": 0.45789220929145813,
    "virtual_spectrum_summary": 0.2963111400604248,
    "yield": 0.46681901812553406
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
      "volume_L": 0.04
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 355
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 325
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
  "end_step": 138,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.37062522768974304,
    "conversion": 0.9990203976631165,
    "cost": 1.0,
    "crystal_csd_quality": 0.5691756010055542,
    "crystal_fines_fraction": 0.7257362008094788,
    "crystal_purity": 1.0,
    "crystal_size": 0.075496606528759,
    "crystal_yield": 0.44588127732276917,
    "degradation_warning": 0.1463293433189392,
    "safety_risk": 0.20028500258922577,
    "score": 0.42372190952301025,
    "selectivity": 0.48490121960639954,
    "virtual_spectrum_summary": 0.269692063331604,
    "yield": 0.46541136503219604
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 355
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 325
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
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.3539409935474396,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.766819417476654,
    "crystal_fines_fraction": 0.2690405547618866,
    "crystal_purity": 0.9960914850234985,
    "crystal_size": 0.10909746587276459,
    "crystal_yield": 0.4413401484489441,
    "degradation_warning": 0.16558893024921417,
    "safety_risk": 0.179418683052063,
    "score": 0.5108952522277832,
    "selectivity": 0.4642972946166992,
    "virtual_spectrum_summary": 0.26918256282806396,
    "yield": 0.4693393111228943
  },
  "ordinal": 12
}
```

## K1

```json
{
  "payload": {
    "report": "Mechanistic account\n\nObserved process behavior\n\nAll batches used solvent-S2, whose public nominal profile combines relatively low solubility (0.70), low nucleation tendency (0.65), high crystal-growth tendency (1.30), and low impurity occlusion (0.65). The experiments therefore establish behavior for S2, but do not experimentally rank it against S0, S1, or S3.\n\nReaction performance was approximately consistent with target yield \u2248 conversion \u00d7 selectivity. For example, batch 1 had conversion 1.000, selectivity 0.487, and reaction yield 0.481. With catalyst-C1, the controlled-cooling batches generally retained reaction yield near 0.47 and selectivity near 0.46\u20130.48. The early, confounded catalyst screen gave lower final-assay selectivity with C0 (batch 2, 0.351), C2 (batch 3, 0.357), and C3 (batch 4, 0.345) than with C1 (batch 1, 0.479). This supports C1 as the best tested catalyst, although temperature, duration, and crystallization history differed across those batches, so it is not a clean catalyst-only comparison.\n\nCrystallization strongly purified the target despite only moderate reaction selectivity. Every completed S2 batch had crystal purity above 0.97. I interpret this as preferential target incorporation and rejection of reaction byproduct from the S2 crystal phase. Thus reaction selectivity controls the amount and composition entering crystallization, while solvent-mediated solid\u2013liquid selectivity largely controls recovered-crystal purity.\n\nProcess-history dependence was the dominant finding. Batches 1\u20134 were quenched before crystallization and all produced extremely high fines fractions: 0.997, 1.000, 0.995, and 1.000, respectively. Their crystal recoveries were 0.381, 0.226, 0.224, and 0.248. Batch 4 included a subsequent heat/cool cycle, but this did not repair the fines problem. My interpretation is that the abrupt quench generated a large primary-nucleation population; later aging or thermal cycling could not sufficiently eliminate that population.\n\nIn contrast, batch 5 omitted the quench and used a controlled descent from the reaction temperature to 325 K, seeding there, followed by slow cooling to 275 K. It achieved recovery 0.400, purity 0.979, and fines 0.303. This large discontinuity relative to batches 1\u20134 indicates that nucleation history, not merely final temperature or aging time, governed particle quality.\n\nWithin the non-quenched family, lowering the final temperature increased recovery without violating the fines constraint. With a 0.005 g seed charge, recovery rose from 0.400 at 275 K in batch 5, to 0.428 at 265 K in batch 6, and 0.450 at 250 K in batch 7. Corresponding fines fractions were 0.303, 0.294, and 0.254, while purity remained 0.979\u20131.000. This is consistent with a larger supersaturation/solubility driving force at lower temperature increasing deposition on an already established, limited crystal population rather than causing catastrophic secondary nucleation under the slow-cooling history.\n\nSeeding had a smaller effect than cooling history. At 250 K, reducing seed from 0.005 g in batch 7 to 0.001 g in batch 8 slightly increased observed recovery from 0.450 to 0.455 while leaving fines essentially unchanged (0.254 in both). Omitting seed in batch 9 gave recovery 0.446 and fines 0.269. This weakly favors a small seed charge: enough to establish growth sites and control induction, but not enough to enlarge the number-weighted particle population unnecessarily. The differences are modest and should not be treated as a precisely located seed optimum.\n\nAdditional aging did not improve the result. Batch 10 repeated the 0.001 g seed/250 K strategy but used three 14,400 s holds; recovery was 0.447 and fines 0.278, versus 0.455 and 0.254 in batch 8 after one hold. This suggests that recovery was already near its practical endpoint after the standard hold, or that any slow additional growth was offset by attrition, secondary nucleation, or ordinary process variability.\n\nConcentration introduced an unresolved recovery\u2013quality tradeoff. Batch 11 halved S2 volume from 0.080 L to 0.040 L and used staged slow cooling. Recovery remained 0.446 and purity was 1.000, but fines rose to 0.726, violating the 0.50 limit. The likely interpretation is that higher concentration increased supersaturation enough to trigger excessive nucleation. It did not deliver a compensating recovery gain.\n\nUseful relationships\n\nThe campaign supports the following conceptual balances:\n\n1. Reaction target yield \u2248 conversion \u00d7 reaction selectivity.\n2. Recovered target from the initial charge is proportional to reaction target yield \u00d7 crystallization-stage recovery.\n3. The reported objective recovery is specifically crystal_yield = seed-excluded recovered target product / target product present immediately before separation; it is not overall yield from the original reagent.\n4. A qualitative crystallization driving force is supersaturation S = C/C*(T), with nucleation increasing steeply above a critical supersaturation while growth is favored when a limited seed population is present. The quench and concentrated batch appear to have crossed the high-nucleation regime; the gradual-cooling batches stayed mainly in a growth-dominated regime.\n5. A useful product-quality constraint is to maximize crystal_yield subject to crystal_purity \u2265 0.80 and fines_number_fraction(<20 \u00b5m) \u2264 0.50. Batch 8 satisfied both with substantial margin.\n\nRecommended-batch interpretation\n\nBatch 8 used 0.040 mol reagent, 0.080 L S2, 0.005 mol C1, reaction heating to 355 K for 3,600 s at 300 rpm, controlled cooling to 325 K over 7,200 s, 0.001 g seed, cooling to 250 K over 14,400 s, and a 14,400 s hold at 100 rpm before filtration. Its final assay gave crystal recovery 0.4554, purity 0.9818, fines 0.2541, CSD quality 0.7946, and normalized crystal-size response 0.1178. It was the highest observed recovery among constraint-compliant batches.\n\nUncertainty and revisions\n\nThe strongest revision was abandoning quench-based crystallization after batches 1\u20134 and adopting controlled cooling before seeding. Subsequent revisions lowered terminal temperature, reduced seed dose, tested no seed and prolonged aging, and challenged the process at higher concentration.\n\nBatch 12 repeated the batch-8 recipe and obtained recovery 0.4413, purity 0.9961, and fines 0.2690. Thus batch 8\u2019s numerical lead is not fully separated from process and assay variability; the repeat nevertheless confirmed that the recipe robustly met both quality constraints. Differences among batches 7\u201310 and 12 are small relative to the reported final-assay noise and process proxy, so the evidence supports a robust operating region more strongly than an exact optimum.\n\nUntested alternatives include other solvents, factorial catalyst comparisons at fixed conditions, intermediate solvent volumes, smaller seed-dose increments, altered seed-addition temperature, gentler multi-stage cooling rates, and controlled partial dissolution before final cooling. These could conceivably improve recovery, but the campaign provides no direct evidence that they would. The remaining practical tradeoff is that stronger supersaturation can maintain or raise recovery but may sharply increase fines, as batch 11 showed. Within the tested region, gradual cooling in 0.080 L S2 to 250 K with a small seed charge provided the best balance."
  },
  "failure": null,
  "elapsed_s": 63.530999999988126,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 634240,
    "input_tokens": 725765,
    "output_tokens": 9117,
    "reasoning_output_tokens": 3313
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
          "estimate": 0.36,
          "lower80": 0.2,
          "upper80": 0.54
        },
        "crystal_purity": {
          "estimate": 0.9,
          "lower80": 0.82,
          "upper80": 0.96
        },
        "crystal_size": {
          "estimate": 0.12,
          "lower80": 0.07,
          "upper80": 0.18
        },
        "crystal_yield": {
          "estimate": 0.24,
          "lower80": 0.15,
          "upper80": 0.34
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q01"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.25,
          "lower80": 0.12,
          "upper80": 0.42
        },
        "crystal_purity": {
          "estimate": 0.95,
          "lower80": 0.89,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.15,
          "lower80": 0.09,
          "upper80": 0.22
        },
        "crystal_yield": {
          "estimate": 0.32,
          "lower80": 0.23,
          "upper80": 0.42
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q02"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.56,
          "lower80": 0.37,
          "upper80": 0.74
        },
        "crystal_purity": {
          "estimate": 0.84,
          "lower80": 0.72,
          "upper80": 0.93
        },
        "crystal_size": {
          "estimate": 0.07,
          "lower80": 0.025,
          "upper80": 0.13
        },
        "crystal_yield": {
          "estimate": 0.16,
          "lower80": 0.08,
          "upper80": 0.25
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q03"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.43,
          "lower80": 0.26,
          "upper80": 0.61
        },
        "crystal_purity": {
          "estimate": 0.87,
          "lower80": 0.76,
          "upper80": 0.95
        },
        "crystal_size": {
          "estimate": 0.1,
          "lower80": 0.05,
          "upper80": 0.16
        },
        "crystal_yield": {
          "estimate": 0.19,
          "lower80": 0.11,
          "upper80": 0.29
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q04"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.4,
          "lower80": 0.24,
          "upper80": 0.58
        },
        "crystal_purity": {
          "estimate": 0.875,
          "lower80": 0.77,
          "upper80": 0.95
        },
        "crystal_size": {
          "estimate": 0.11,
          "lower80": 0.055,
          "upper80": 0.17
        },
        "crystal_yield": {
          "estimate": 0.205,
          "lower80": 0.12,
          "upper80": 0.3
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q05"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.84,
          "lower80": 0.66,
          "upper80": 0.96
        },
        "crystal_purity": {
          "estimate": 0.83,
          "lower80": 0.7,
          "upper80": 0.92
        },
        "crystal_size": {
          "estimate": 0.045,
          "lower80": 0.01,
          "upper80": 0.1
        },
        "crystal_yield": {
          "estimate": 0.22,
          "lower80": 0.13,
          "upper80": 0.32
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q06"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.38,
          "lower80": 0.22,
          "upper80": 0.56
        },
        "crystal_purity": {
          "estimate": 0.88,
          "lower80": 0.77,
          "upper80": 0.95
        },
        "crystal_size": {
          "estimate": 0.12,
          "lower80": 0.06,
          "upper80": 0.18
        },
        "crystal_yield": {
          "estimate": 0.22,
          "lower80": 0.13,
          "upper80": 0.32
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q07"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.3,
          "lower80": 0.14,
          "upper80": 0.5
        },
        "crystal_purity": {
          "estimate": 0.91,
          "lower80": 0.8,
          "upper80": 0.98
        },
        "crystal_size": {
          "estimate": 0.15,
          "lower80": 0.075,
          "upper80": 0.23
        },
        "crystal_yield": {
          "estimate": 0.17,
          "lower80": 0.07,
          "upper80": 0.29
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q08"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.76,
          "lower80": 0.55,
          "upper80": 0.92
        },
        "crystal_purity": {
          "estimate": 0.92,
          "lower80": 0.78,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.035,
          "lower80": 0.01,
          "upper80": 0.08
        },
        "crystal_yield": {
          "estimate": 0.025,
          "lower80": 0,
          "upper80": 0.08
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q09"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.6,
          "lower80": 0.39,
          "upper80": 0.79
        },
        "crystal_purity": {
          "estimate": 0.86,
          "lower80": 0.73,
          "upper80": 0.95
        },
        "crystal_size": {
          "estimate": 0.065,
          "lower80": 0.02,
          "upper80": 0.12
        },
        "crystal_yield": {
          "estimate": 0.075,
          "lower80": 0.02,
          "upper80": 0.15
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q10"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.4,
          "lower80": 0.23,
          "upper80": 0.58
        },
        "crystal_purity": {
          "estimate": 0.88,
          "lower80": 0.77,
          "upper80": 0.95
        },
        "crystal_size": {
          "estimate": 0.11,
          "lower80": 0.055,
          "upper80": 0.18
        },
        "crystal_yield": {
          "estimate": 0.215,
          "lower80": 0.13,
          "upper80": 0.31
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q11"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.68,
          "lower80": 0.47,
          "upper80": 0.85
        },
        "crystal_purity": {
          "estimate": 0.82,
          "lower80": 0.68,
          "upper80": 0.92
        },
        "crystal_size": {
          "estimate": 0.06,
          "lower80": 0.02,
          "upper80": 0.12
        },
        "crystal_yield": {
          "estimate": 0.31,
          "lower80": 0.2,
          "upper80": 0.43
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q12"
      }
    ],
    "rationale": "Q01\u2013Q02: S3 is expected to outperform S1 through lower nominal solubility, nucleation and impurity occlusion, giving greater recovery, purity and size with fewer fines. Q03\u2013Q04: increasing S0 seed loading should provide more controlled growth surface and suppress uncontrolled nucleation, moving fines below 0.50 at a modest recovery gain. Q05\u2013Q06: the gradual 72-hour cooling profile should preserve a growth-dominated history, whereas the 120-second temperature drop should create many persistent fines even after long aging; equilibrium recovery may remain similar. Q07\u2013Q08: the post-growth heat cycle should partially dissolve fines and improve purity/size, but some product remains dissolved or is not fully recovered during the short recool, reducing yield. Q09\u2013Q10: a two-hour hold at 292 K permits additional deposition and growth relative to immediate filtration, but is probably insufficient to repair the fines created by the initial 60-second drop. Q11\u2013Q12: doubling concentration should increase recovered fraction but sharply increase nucleation, impurity occlusion and fines, analogous to the campaign\u2019s concentrated batch. All recipes contain seed, so particles are expected even where seed-excluded product recovery is small. Intervals are widest for S0, thermal cycling, high concentration and short crystallizations because these regimes were not directly calibrated; several feasibility calls near the fines threshold are consequently uncertain."
  },
  "failure": null,
  "elapsed_s": 103.60999999998603,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 685184,
    "input_tokens": 828361,
    "output_tokens": 14041,
    "reasoning_output_tokens": 6497
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
    "report": "1. Support, contradiction, and remaining gaps\n\nSupported by direct observation:\n- Process history strongly tracked particle quality. Quenched batches 1\u20134 all had final fines fractions near unity (0.995\u20131.000), whereas non-quenched, gradually cooled batches 5\u201310 and 12 generally gave about 0.25\u20130.30 fines. This supports the practical claim that gradual cooling was essential. The interpretation that quenching caused excessive primary nucleation is plausible, but not yet isolated causally because the early batches also differed in catalyst, reaction conditions, seed loading, and terminal temperature.\n- Lower terminal temperature improved recovery in the matched C1/S2 series: batch 5 at 275 K gave 0.400 recovery, batch 6 at 265 K gave 0.428, and batch 7 at 250 K gave 0.450. Purity remained at least 0.979 and fines remained below 0.31. This directly supports a solubility-driven recovery benefit within that tested range.\n- S2 crystallization strongly purified the reaction mixture. All final crystals had purity above 0.97 even though reaction selectivity was only about 0.35\u20130.48. Preferential target incorporation is an interpretation; the purity observations themselves are direct.\n- The concentrated batch 11 directly demonstrated a quality penalty: halving solvent volume did not improve recovery materially (0.446) but increased fines to 0.726. This supports a supersaturation\u2013nucleation tradeoff.\n- Batch 12 replicated the batch-8 operating region and again met both constraints, with recovery 0.441, purity 0.996, and fines 0.269. It supports robustness of feasibility, though not the exact superiority of batch 8.\n\nWeakly supported or partly contradicted:\n- A small seed charge appeared preferable, but the effect was weak. Batches 7, 8, and 9 gave recoveries of 0.450, 0.455, and 0.446 for 0.005 g, 0.001 g, and no seed, respectively. Those differences are comparable to assay and process uncertainty, so a precise seed optimum is not established.\n- Extra aging did not produce the expected recovery or coarsening benefit: batch 10, with three long holds, gave lower recovery and higher fines than batch 8. This contradicts a simple model in which residence time alone monotonically improves growth.\n- Thermal cycling did not rescue batch 4 after its quench: fines remained 1.000. That contradicts any general claim that a later heat/cool cycle necessarily erases an adverse nucleation history.\n- Nominally low nucleation tendency for S2 did not prevent severe fines in batches 1\u20134. Thus material tendency alone was insufficient; process history dominated.\n- A simple claim that higher concentration must increase fractional recovery is contradicted by batch 11, which showed little recovery benefit.\n\nStill untested:\n- No experimental comparison among S0, S1, S2, and S3 was made; all solvent rankings in the held-out predictions are extrapolations from nominal properties.\n- Catalyst identity was not varied under otherwise identical conditions. The apparent C1 selectivity advantage over C0, C2, and C3 is confounded by reaction temperature, time, and downstream history.\n- Primary nucleation, secondary nucleation, attrition, agglomeration, and impurity occlusion were not separately measured. Their roles remain mechanistic interpretations.\n- Thermal cycling after an initially well-controlled crystallization, intermediate solvent volumes, seed-addition temperature, and detailed cooling-rate effects remain untested.\n\n2. One additional experiment\n\nI would run a matched quench challenge against batches 8 and 12. I would use their same charges and conditions\u20140.040 mol reagent, 0.080 L S2, 0.005 mol C1, 355 K for 3,600 s at 300 rpm\u2014but insert a quench before restoring/conditioning the slurry near 325 K. I would then add 0.001 g seed, cool to 250 K over 14,400 s, hold for 14,400 s at 100 rpm, filter, and assay. An in-situ particle-size reading immediately after the quench and before seeding would be especially diagnostic.\n\nThis would distinguish two explanations: (a) quenching irreversibly creates a large nuclei population that controls the later CSD, versus (b) the poor particles in batches 1\u20134 arose mainly from their other recipe differences. Under explanation (a), particles or an incipient fine population should appear before seeding, final fines should rise above 0.50\u2014potentially toward the near-unity values of batches 1\u20134\u2014and size/CSD quality should decline. Recovery might rise transiently through nucleation but would not represent an acceptable quality gain. Under explanation (b), the result should remain close to batches 8 and 12: approximately 0.44\u20130.46 recovery, high purity, and roughly 0.25\u20130.27 fines. An intermediate outcome would indicate that quench history matters but interacts with final temperature, seed loading, or growth time.\n\n3. Least-used observation and least-reliable prediction\n\nThe account used the intermediate particle-size observations least effectively. It relied mainly on final assays, despite notable differences between in-process and final readings. For example, batch 8 changed from an intermediate normalized size of 0.0748 to a final value of 0.1178, while batch 5 changed from 0.0938 to 0.0664. These differences could reflect continued evolution, filtration/sampling effects, channel noise, or representative-slurry limitations. Treating them explicitly might have better separated real growth from measurement variability and cautioned against interpreting final size and fines as a deterministic CSD pair.\n\nQ08 is the least reliable held-out prediction. It combines several uncalibrated elements: S0 was never tested, the 0.035 g seed charge is far above the best campaign region, the preceding cooling lasts many stages, and the final 315 K dissolution/recrystallization cycle has no close campaign analogue. Batch 4 is only a weak comparator because its thermal cycle followed an already damaging quench in S2. Consequently, whether Q08\u2019s cycle preferentially dissolves fines, dissolves most recovered product, or creates new fines during the short recool is unresolved. The sealed estimate therefore rests more on general crystallization reasoning than on direct campaign calibration."
  },
  "failure": null,
  "elapsed_s": 92.375,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 724736,
    "input_tokens": 884569,
    "output_tokens": 16529,
    "reasoning_output_tokens": 7591
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
    "selection_rationale": "Batch 8 gave the highest observed crystal recovery among batches meeting both constraints: crystal_yield 0.4554, crystal_purity 0.9818, and fines fraction 0.2541. Its gradual, non-quench cooling with a small seed dose avoided the severe fines seen after quenching."
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
        "duration_s": 3600,
        "operation": "heat",
        "stirring_speed_rpm": 300,
        "target_temperature_K": 355
      },
      {
        "duration_s": 7200,
        "operation": "cool_crystallize",
        "target_temperature_K": 325
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
        "absolute_delta_error": 0.1457115849044418,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_yield",
        "predicted_delta": 0.08000000000000002,
        "resolved": true,
        "true_delta": -0.06571158490444179
      },
      {
        "absolute_delta_error": 0.05287642280938465,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_purity",
        "predicted_delta": 0.04999999999999993,
        "resolved": false,
        "true_delta": -0.0028764228093847155
      },
      {
        "absolute_delta_error": 0.010995063719243692,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_size",
        "predicted_delta": 0.03,
        "resolved": true,
        "true_delta": 0.019004936280756307
      },
      {
        "absolute_delta_error": 0.5976947480077399,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.10999999999999999,
        "resolved": true,
        "true_delta": -0.7076947480077399
      },
      {
        "absolute_delta_error": 0.03008776257407511,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_yield",
        "predicted_delta": 0.03,
        "resolved": false,
        "true_delta": -8.776257407511201e-05
      },
      {
        "absolute_delta_error": 0.02141726419352652,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_purity",
        "predicted_delta": 0.030000000000000027,
        "resolved": false,
        "true_delta": 0.008582735806473507
      },
      {
        "absolute_delta_error": 0.029125123275801176,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_size",
        "predicted_delta": 0.03,
        "resolved": false,
        "true_delta": 0.0008748767241988226
      },
      {
        "absolute_delta_error": 0.16137923157767697,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.13000000000000006,
        "resolved": false,
        "true_delta": 0.031379231577676914
      },
      {
        "absolute_delta_error": 0.014644873190271801,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_yield",
        "predicted_delta": 0.015000000000000013,
        "resolved": false,
        "true_delta": 0.0003551268097282123
      },
      {
        "absolute_delta_error": 0.04079492324721479,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.04500000000000004,
        "resolved": false,
        "true_delta": -0.004205076752785253
      },
      {
        "absolute_delta_error": 0.01845150632552567,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_size",
        "predicted_delta": -0.065,
        "resolved": true,
        "true_delta": -0.046548493674474334
      },
      {
        "absolute_delta_error": 0.3002009392429925,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.43999999999999995,
        "resolved": true,
        "true_delta": 0.7402009392429925
      },
      {
        "absolute_delta_error": 0.09146629297589665,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_yield",
        "predicted_delta": -0.04999999999999999,
        "resolved": true,
        "true_delta": 0.04146629297589666
      },
      {
        "absolute_delta_error": 0.039830577525981625,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_purity",
        "predicted_delta": 0.030000000000000027,
        "resolved": false,
        "true_delta": -0.009830577525981599
      },
      {
        "absolute_delta_error": 0.07063855997202603,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_size",
        "predicted_delta": 0.03,
        "resolved": true,
        "true_delta": -0.04063855997202603
      },
      {
        "absolute_delta_error": 0.8478652105803905,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.08000000000000002,
        "resolved": true,
        "true_delta": 0.7678652105803905
      },
      {
        "absolute_delta_error": 0.07800038962529793,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_yield",
        "predicted_delta": 0.049999999999999996,
        "resolved": true,
        "true_delta": 0.12800038962529792
      },
      {
        "absolute_delta_error": 0.04671725463709986,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_purity",
        "predicted_delta": -0.06000000000000005,
        "resolved": true,
        "true_delta": -0.013282745362900195
      },
      {
        "absolute_delta_error": 0.016534244532482596,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_size",
        "predicted_delta": 0.03,
        "resolved": true,
        "true_delta": 0.013465755467517403
      },
      {
        "absolute_delta_error": 0.18884240834118415,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.16000000000000003,
        "resolved": false,
        "true_delta": 0.028842408341184123
      },
      {
        "absolute_delta_error": 0.062463253168567906,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_yield",
        "predicted_delta": 0.095,
        "resolved": true,
        "true_delta": 0.032536746831432095
      },
      {
        "absolute_delta_error": 0.0541923828551657,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_purity",
        "predicted_delta": -0.06000000000000005,
        "resolved": false,
        "true_delta": -0.005807617144834354
      },
      {
        "absolute_delta_error": 0.015611719188503126,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_size",
        "predicted_delta": -0.05,
        "resolved": true,
        "true_delta": -0.03438828081149688
      },
      {
        "absolute_delta_error": 0.4610258952283488,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.28,
        "resolved": true,
        "true_delta": 0.7410258952283488
      }
    ],
    "failures": [],
    "metrics": {
      "crystal_fines_fraction": {
        "coverage80": 0.4166666666666667,
        "interval_score80": 1.6121549863750078,
        "interval_width": 0.35000000000000003,
        "mae": 0.27782828339773996,
        "n": 12,
        "planned": 12
      },
      "crystal_purity": {
        "coverage80": 0.16666666666666666,
        "interval_score80": 0.5112446958060831,
        "interval_width": 0.1875,
        "mae": 0.1070966103018206,
        "n": 12,
        "planned": 12
      },
      "crystal_size": {
        "coverage80": 0.75,
        "interval_score80": 0.14043672538633714,
        "interval_width": 0.11083333333333334,
        "mae": 0.028771824715285693,
        "n": 12,
        "planned": 12
      },
      "crystal_yield": {
        "coverage80": 0.8333333333333334,
        "interval_score80": 0.21043453953038957,
        "interval_width": 0.1775,
        "mae": 0.0647231885101606,
        "n": 12,
        "planned": 12
      }
    },
    "quality": {
      "balanced_accuracy": 0.75,
      "false_negative": 1,
      "false_positive": 2,
      "true_negative": 4,
      "true_positive": 5
    },
    "resolved_direction_correct": 10,
    "resolved_direction_n": 14,
    "tie_correct": 1,
    "tie_n": 10,
    "valid": true
  },
  "public_baselines": {
    "available": true,
    "mae": {
      "public_mean": {
        "crystal_fines_fraction": 0.3646230122888186,
        "crystal_purity": 0.004156780401248468,
        "crystal_size": 0.019943615088417202,
        "crystal_yield": 0.13835707552167695
      },
      "public_nearest_neighbor": {
        "crystal_fines_fraction": 0.3646230122888186,
        "crystal_purity": 0.014986723031512736,
        "crystal_size": 0.019943615088417202,
        "crystal_yield": 0.20136292027367078
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
        "cached_input": 634240,
        "input": 685972,
        "output": 6264,
        "stage": "source",
        "uncached_input": 51732
      },
      {
        "cached_input": 0,
        "input": 39793,
        "output": 2853,
        "stage": "K1",
        "uncached_input": 39793
      },
      {
        "cached_input": 50944,
        "input": 102596,
        "output": 4924,
        "stage": "Q",
        "uncached_input": 51652
      },
      {
        "cached_input": 39552,
        "input": 56208,
        "output": 2488,
        "stage": "K2",
        "uncached_input": 16656
      }
    ],
    "total": {
      "cached_input": 724736,
      "input": 884569,
      "input_plus_output": 901098,
      "output": 16529,
      "uncached_input": 159833
    },
    "valid": true
  },
  "elapsed_s": 490.0470000000205
}
```
