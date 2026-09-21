# C-W04-B12-E-Opaque

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
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 200
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
    "byproduct_signal": 0.264827698469162,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5061086416244507,
    "crystal_fines_fraction": 0.99732506275177,
    "crystal_purity": 0.9783403277397156,
    "crystal_size": 0.054275032132864,
    "crystal_yield": 0.4602310359477997,
    "degradation_warning": 0.09229610860347748,
    "safety_risk": 0.14288730919361115,
    "score": 0.4067418575286865,
    "selectivity": 0.5909451246261597,
    "virtual_spectrum_summary": 0.18718849122524261,
    "yield": 0.5887653827667236
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
    "byproduct_signal": 0.2659852206707001,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.4972986876964569,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9807055592536926,
    "crystal_size": 0.08395954966545105,
    "crystal_yield": 0.41161417961120605,
    "degradation_warning": 0.11342775821685791,
    "safety_risk": 0.14086468517780304,
    "score": 0.40112975239753723,
    "selectivity": 0.6238094568252563,
    "virtual_spectrum_summary": 0.19733434915542603,
    "yield": 0.6123629212379456
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
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.2876814305782318,
    "conversion": 0.9982717037200928,
    "cost": 1.0,
    "crystal_csd_quality": 0.4913843274116516,
    "crystal_fines_fraction": 0.9949303865432739,
    "crystal_purity": 0.9759774804115295,
    "crystal_size": 0.039806876331567764,
    "crystal_yield": 0.35240864753723145,
    "degradation_warning": 0.11695154011249542,
    "safety_risk": 0.13312816619873047,
    "score": 0.367951899766922,
    "selectivity": 0.548626720905304,
    "virtual_spectrum_summary": 0.2108529806137085,
    "yield": 0.5477141737937927
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
  "end_step": 68,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.2620021104812622,
    "conversion": 0.9889658093452454,
    "cost": 1.0,
    "crystal_csd_quality": 0.48046261072158813,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 1.0,
    "crystal_size": 0.05588045343756676,
    "crystal_yield": 0.41437503695487976,
    "degradation_warning": 0.09797202050685883,
    "safety_risk": 0.13973264396190643,
    "score": 0.39856380224227905,
    "selectivity": 0.6213582754135132,
    "virtual_spectrum_summary": 0.1881885677576065,
    "yield": 0.6077097058296204
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
      "seed_mass_g": 0.05
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
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
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
  "end_step": 92,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.31985506415367126,
    "conversion": 0.9963378310203552,
    "cost": 1.0,
    "crystal_csd_quality": 0.4829712510108948,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9758486151695251,
    "crystal_size": 0.036252524703741074,
    "crystal_yield": 0.3962593674659729,
    "degradation_warning": 0.1293867826461792,
    "safety_risk": 0.15987925231456757,
    "score": 0.3779522776603699,
    "selectivity": 0.5698737502098083,
    "virtual_spectrum_summary": 0.23414433002471924,
    "yield": 0.5637207627296448
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
      "target_temperature_K": 360
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
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
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
  "end_step": 111,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.36850103735923767,
    "conversion": 0.9924335479736328,
    "cost": 1.0,
    "crystal_csd_quality": 0.4890308380126953,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9999276995658875,
    "crystal_size": 0.02582947164773941,
    "crystal_yield": 0.3434458374977112,
    "degradation_warning": 0.1708584576845169,
    "safety_risk": 0.1707114428281784,
    "score": 0.3541368544101715,
    "selectivity": 0.4854596257209778,
    "virtual_spectrum_summary": 0.2795618772506714,
    "yield": 0.48734524846076965
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
  "end_step": 130,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.3658328354358673,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.46240055561065674,
    "crystal_fines_fraction": 0.9866482019424438,
    "crystal_purity": 0.9657517075538635,
    "crystal_size": 0.07304713129997253,
    "crystal_yield": 0.31941255927085876,
    "degradation_warning": 0.18171653151512146,
    "safety_risk": 0.18061463534832,
    "score": 0.34260064363479614,
    "selectivity": 0.474318265914917,
    "virtual_spectrum_summary": 0.2829805016517639,
    "yield": 0.5009654760360718
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
  "end_step": 164,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.25416696071624756,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.507318913936615,
    "crystal_fines_fraction": 0.9868534207344055,
    "crystal_purity": 0.9781343936920166,
    "crystal_size": 0.08529546111822128,
    "crystal_yield": 0.44635850191116333,
    "degradation_warning": 0.12086869776248932,
    "safety_risk": 0.1412852257490158,
    "score": 0.41559019684791565,
    "selectivity": 0.6369833946228027,
    "virtual_spectrum_summary": 0.19418273866176605,
    "yield": 0.6286765933036804
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
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 500
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
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.2646165192127228,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.48230472207069397,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9803478717803955,
    "crystal_size": 0.035775355994701385,
    "crystal_yield": 0.4372656047344208,
    "degradation_warning": 0.11347229778766632,
    "safety_risk": 0.1412852257490158,
    "score": 0.4011564254760742,
    "selectivity": 0.6152160167694092,
    "virtual_spectrum_summary": 0.19660161435604095,
    "yield": 0.6288903951644897
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
      "target_temperature_K": 360
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
  "end_step": 230,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.25749364495277405,
    "conversion": 0.9858217835426331,
    "cost": 1.0,
    "crystal_csd_quality": 0.4435993432998657,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.973232090473175,
    "crystal_size": 0.046243101358413696,
    "crystal_yield": 0.35957467555999756,
    "degradation_warning": 0.1248786449432373,
    "safety_risk": 0.13508827984333038,
    "score": 0.37513312697410583,
    "selectivity": 0.6262969374656677,
    "virtual_spectrum_summary": 0.1978168934583664,
    "yield": 0.6352221965789795
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
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
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
  "end_step": 248,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.2660082280635834,
    "conversion": 0.9990178942680359,
    "cost": 1.0,
    "crystal_csd_quality": 0.46135395765304565,
    "crystal_fines_fraction": 0.993565559387207,
    "crystal_purity": 0.9932034611701965,
    "crystal_size": 0.052435941994190216,
    "crystal_yield": 0.38428613543510437,
    "degradation_warning": 0.1018986701965332,
    "safety_risk": 0.13732804358005524,
    "score": 0.3899625241756439,
    "selectivity": 0.6433944702148438,
    "virtual_spectrum_summary": 0.19215892255306244,
    "yield": 0.6239030361175537
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
      "target_temperature_K": 360
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
  "end_step": 265,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.3791425824165344,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6809293627738953,
    "crystal_fines_fraction": 0.4679346978664398,
    "crystal_purity": 0.993095874786377,
    "crystal_size": 0.09907977283000946,
    "crystal_yield": 0.45332348346710205,
    "degradation_warning": 0.22441741824150085,
    "safety_risk": 0.14138618111610413,
    "score": 0.48843127489089966,
    "selectivity": 0.5220651626586914,
    "virtual_spectrum_summary": 0.3095162510871887,
    "yield": 0.5271071791648865
  },
  "ordinal": 12
}
```

## K1

```json
{
  "payload": {
    "report": "Mechanistic account\n\nThe campaign indicates that reaction conversion was generally easy to achieve, whereas selectivity and crystal population control were the important limitations. The recommended batch remains batch 12.\n\nObservations on material effects\n\nWith solvent S0 at nominally common reaction conditions, the catalyst screen gave HPLC selectivity/yield values of about 0.600/0.593 for C0 (batch 1), 0.611/0.582 for C1 (batch 2), 0.524/0.525 for C2 (batch 3), and 0.592/0.603 for C3 (batch 4). Conversion was approximately quantitative. Thus C2 was observably inferior, while differences among C0, C1, and C3 were modest and may partly reflect measurement and process variability. C1 was retained as a reasonable, reproducible choice rather than as a uniquely proven optimum.\n\nThe C1 solvent comparison favored S0. Representative final reaction selectivities were approximately 0.624 in S0 (batch 2), 0.570 in S1 (batch 5), 0.485 in S2 (batch 6), and 0.474 in S3 (batch 7). Byproduct signal increased from roughly 0.26 in typical quenched S0 batches to 0.32\u20130.37 in S1\u2013S3. Crystal recovery also declined across these nonidentical protocols: 0.412 in batch 2, 0.396 in batch 5, 0.343 in batch 6, and 0.319 in batch 7. This supports an S0 advantage, although cooling endpoints differed, so reaction and crystallization solvent effects were not cleanly separated.\n\nInterpretation: catalyst identity primarily changed the competition between target and byproduct formation rather than total conversion. Solvent identity affected both reaction selectivity and the crystallization environment\u2014probably through relative solubilities and nucleation behavior. These are benchmark identities, so no real-molecule structural explanation is warranted.\n\nReaction\u2013crystallization coupling\n\nA useful bookkeeping relationship is\n\nY_crystal = n(target recovered as crystals, excluding seed) / n(target present before separation).\n\nIt is a crystallization-stage recovery, not an overall yield from charged reagent. If reaction yield and crystallization recovery share compatible bases, their product is only an approximate overall target recovery. For batch 12, 0.527 \u00d7 0.453 is about 0.239, illustrating why high crystallization recovery does not erase reaction selectivity losses.\n\nMost quenched S0 batches had favorable reaction selectivity around 0.62\u20130.64 and byproduct signal around 0.25\u20130.27. Batch 12 deliberately avoided the abrupt quench and instead remained chemically active during a long staged cooling history. Its final selectivity was only 0.522, byproduct signal 0.379, and degradation warning 0.224. Nevertheless, crystallization rejected impurities effectively: crystal purity was 0.993. The interpretation is that the history that controlled nucleation also prolonged reaction/degradation exposure. Product purity and reaction selectivity therefore need not move together.\n\nProcess-history dependence\n\nThe decisive observation is the contrast between batches 1\u201311 and batch 12. Batches 1\u201311 were quenched from the reaction temperature before seeding. Their final fines fractions were approximately 0.987\u20131.000, despite large variations in subsequent treatment:\n\n\u2022 Batch 3 used only 0.001 g seed plus a heat\u2013cool cycle; fines were 0.995.\n\u2022 Batch 8 used twenty 0.05 g seed additions, 1.0 g total; fines were still 0.987.\n\u2022 Batch 9 added forty four-hour aging periods; fines remained 1.000.\n\u2022 Batch 10 crystallized only to 305 K; fines remained 1.000.\n\u2022 Batch 11 cooled to 270 K and reheated to 300 K to try to dissolve fines; fines remained 0.994.\n\nThus seed amount, prolonged holding, warmer isolation, and one thermal-digestion cycle did not repair the particle population after the quench.\n\nBatch 12 changed the ordering: after reaction at a nominal 360 K, 0.05 g seed was added before any quench, and the batch was cooled in four-hour stages to 330, 315, 300, and 285 K, followed by four four-hour holds at 100 rpm. Its in-process particle measurement gave fines 0.470, and the final assay gave fines 0.468, CSD quality 0.681, purity 0.993, and seed-excluded crystal recovery 0.453. Both independent fines readings were below the 0.50 constraint.\n\nMy mechanistic interpretation is that abrupt quenching generated a large burst of unseeded primary nuclei before added seeds could control the population. Once that very numerous fine population existed, additional seed, aging, or modest reheating could not substantially reduce its number fraction. In batch 12, early seed addition established a growth surface before supersaturation was developed, while staged cooling metered supersaturation and favored growth over primary nucleation. This interpretation is strongly consistent with the history contrast, but the experiment changed hot seeding, quench omission, and cooling schedule together; their individual contributions were not isolated.\n\nRevisions during the campaign\n\nThe initial working approach emphasized catalyst/solvent screening and conventional post-quench changes in endpoint temperature, seed loading, aging time, and thermal cycling. Those revisions repeatedly failed to address fines. The working mechanism was then revised from \u201cinsufficient growth time or seed mass\u201d to \u201cirreversible population formation during the quench.\u201d Batch 12 tested that revised ordering and was the only batch to satisfy the fines constraint while retaining high recovery and purity.\n\nUncertainty and unresolved tradeoffs\n\nBatch 12 exceeded the purity requirement by a large margin, but its fines margin was only about 0.032. The stated final-assay noise scale for fines is 0.018, so compliance is supported by two consistent measurements but is not extremely robust. Its particle-size index differed between the in-process and final readings, while the fines estimates agreed; consequently, the fines fraction is the more reliable morphology criterion here.\n\nBatch 1 had a slightly higher observed recovery, 0.460 versus 0.453 for batch 12, but failed badly on fines at 0.997. The recovery difference is smaller than, or comparable to, assay uncertainty and does not outweigh feasibility. Deeper cooling may raise recovery, but it may also create new nuclei and push fines above 0.50. Conversely, a warmer endpoint could provide a larger fines margin at the cost of recovery. Only one no-quench, pre-seeded staged-cooling sequence was tested, so the feasible frontier remains poorly mapped.\n\nUntested alternatives include independently varying the hot-seed temperature, seed dose, staged cooling rate, final temperature, and agitation without an initial quench; repeating the no-quench protocol with C0 or C3; and shortening or lowering the reaction-temperature exposure to reduce degradation before controlled crystallization. These alternatives could clarify causality or improve robustness, but they were not demonstrated and do not alter the batch 12 recommendation."
  },
  "failure": null,
  "elapsed_s": 61.312999999994645,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 500096,
    "input_tokens": 560324,
    "output_tokens": 11221,
    "reasoning_output_tokens": 4226
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
          "estimate": 0.45,
          "lower80": 0.3,
          "upper80": 0.62
        },
        "crystal_purity": {
          "estimate": 0.975,
          "lower80": 0.94,
          "upper80": 0.995
        },
        "crystal_size": {
          "estimate": 0.1,
          "lower80": 0.06,
          "upper80": 0.15
        },
        "crystal_yield": {
          "estimate": 0.39,
          "lower80": 0.31,
          "upper80": 0.47
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q01"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.6,
          "lower80": 0.43,
          "upper80": 0.77
        },
        "crystal_purity": {
          "estimate": 0.965,
          "lower80": 0.92,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.08,
          "lower80": 0.04,
          "upper80": 0.13
        },
        "crystal_yield": {
          "estimate": 0.32,
          "lower80": 0.24,
          "upper80": 0.4
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q02"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.65,
          "lower80": 0.46,
          "upper80": 0.82
        },
        "crystal_purity": {
          "estimate": 0.985,
          "lower80": 0.95,
          "upper80": 0.999
        },
        "crystal_size": {
          "estimate": 0.07,
          "lower80": 0.03,
          "upper80": 0.12
        },
        "crystal_yield": {
          "estimate": 0.4,
          "lower80": 0.31,
          "upper80": 0.49
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q03"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.36,
          "lower80": 0.22,
          "upper80": 0.52
        },
        "crystal_purity": {
          "estimate": 0.985,
          "lower80": 0.955,
          "upper80": 0.999
        },
        "crystal_size": {
          "estimate": 0.12,
          "lower80": 0.07,
          "upper80": 0.18
        },
        "crystal_yield": {
          "estimate": 0.44,
          "lower80": 0.36,
          "upper80": 0.52
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q04"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.32,
          "lower80": 0.19,
          "upper80": 0.47
        },
        "crystal_purity": {
          "estimate": 0.987,
          "lower80": 0.96,
          "upper80": 0.999
        },
        "crystal_size": {
          "estimate": 0.13,
          "lower80": 0.08,
          "upper80": 0.19
        },
        "crystal_yield": {
          "estimate": 0.45,
          "lower80": 0.37,
          "upper80": 0.53
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q05"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.88,
          "lower80": 0.72,
          "upper80": 0.98
        },
        "crystal_purity": {
          "estimate": 0.975,
          "lower80": 0.93,
          "upper80": 0.995
        },
        "crystal_size": {
          "estimate": 0.055,
          "lower80": 0.02,
          "upper80": 0.1
        },
        "crystal_yield": {
          "estimate": 0.46,
          "lower80": 0.38,
          "upper80": 0.54
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q06"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.28,
          "lower80": 0.16,
          "upper80": 0.43
        },
        "crystal_purity": {
          "estimate": 0.988,
          "lower80": 0.96,
          "upper80": 0.999
        },
        "crystal_size": {
          "estimate": 0.14,
          "lower80": 0.09,
          "upper80": 0.2
        },
        "crystal_yield": {
          "estimate": 0.46,
          "lower80": 0.38,
          "upper80": 0.54
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q07"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.6,
          "lower80": 0.42,
          "upper80": 0.76
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.945,
          "upper80": 0.998
        },
        "crystal_size": {
          "estimate": 0.085,
          "lower80": 0.04,
          "upper80": 0.14
        },
        "crystal_yield": {
          "estimate": 0.42,
          "lower80": 0.32,
          "upper80": 0.52
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q08"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.82,
          "lower80": 0.64,
          "upper80": 0.96
        },
        "crystal_purity": {
          "estimate": 0.99,
          "lower80": 0.95,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.065,
          "lower80": 0.025,
          "upper80": 0.11
        },
        "crystal_yield": {
          "estimate": 0.06,
          "lower80": 0.01,
          "upper80": 0.13
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q09"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.72,
          "lower80": 0.52,
          "upper80": 0.88
        },
        "crystal_purity": {
          "estimate": 0.985,
          "lower80": 0.95,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.08,
          "lower80": 0.035,
          "upper80": 0.13
        },
        "crystal_yield": {
          "estimate": 0.2,
          "lower80": 0.1,
          "upper80": 0.32
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q10"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.27,
          "lower80": 0.15,
          "upper80": 0.42
        },
        "crystal_purity": {
          "estimate": 0.988,
          "lower80": 0.96,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.14,
          "lower80": 0.09,
          "upper80": 0.21
        },
        "crystal_yield": {
          "estimate": 0.46,
          "lower80": 0.38,
          "upper80": 0.54
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q11"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.58,
          "lower80": 0.4,
          "upper80": 0.75
        },
        "crystal_purity": {
          "estimate": 0.965,
          "lower80": 0.91,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.095,
          "lower80": 0.05,
          "upper80": 0.15
        },
        "crystal_yield": {
          "estimate": 0.55,
          "lower80": 0.46,
          "upper80": 0.64
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q12"
      }
    ],
    "rationale": "Q01\u2013Q02: S1 is predicted to give better recovery and population control than S3, consistent with the observed solvent ranking, though Q01 is close to the fines boundary. Q03\u2013Q04: increasing seed from 0.001 to 0.045 g should suppress uncontrolled nucleation, increase size and recovery, and lower fines. Q05\u2013Q06: gradual cooling should preserve similar equilibrium recovery while producing much fewer fines than an immediate crash followed by an equally long cold residence. Q07\u2013Q08: the 315 K excursion followed by rapid recooling is expected to redissolve some product and then regenerate fines, so Q08 loses recovery and morphology quality. Q09\u2013Q10: two hours at 292 K should raise seed-excluded recovery and permit some growth, but both rapid-cooling cases likely remain fines-limited. Q11\u2013Q12: doubling reagent concentration raises recovery through greater supersaturation but also increases secondary nucleation and impurity occlusion, making Q12 likely infeasible on fines. All batches contain added seed, so particles are expected even where seed-excluded recovery is small. Intervals are wider for fines and size because the campaign tested only one clearly feasible population-control history; threshold classifications for Q01, Q03, Q04 and Q12 are consequently less secure than their point estimates suggest."
  },
  "failure": null,
  "elapsed_s": 88.98399999999674,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 500096,
    "input_tokens": 603273,
    "output_tokens": 15996,
    "reasoning_output_tokens": 7301
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
    "report": "1. Status of the main claims\n\nSupported by direct observation:\n- Process history strongly affected particle quality. Batches 1\u201311, all quenched before seeding, had final fines fractions of about 0.987\u20131.000. Batch 12, seeded before cooling and never abruptly quenched, gave 0.470 by particle measurement and 0.468 by final assay. Its CSD quality was also higher, 0.681. This directly supports history dependence, although not one unique mechanism.\n- Post-quench remediation was ineffective in the tested range. Low seed in batch 3, 1.0 g total seed in batch 8, forty aging periods in batch 9, warmer isolation in batch 10, and a 270\u2192300 K digestion treatment in batch 11 all left fines near unity. This contradicts the early ideas that seed quantity, aging alone, or modest thermal cycling could repair an already formed fine population.\n- Reaction conversion was generally near unity while selectivity varied. For the S0 catalyst screen, C2 was worse than C0, C1, and C3; batches 1\u20134 gave HPLC selectivities near 0.600, 0.611, 0.524, and 0.592, respectively. Thus competitive byproduct formation, rather than incomplete conversion, was the principal reaction limitation.\n- S0 performed better than S1\u2013S3 with C1 in the tested recipes. Final selectivity fell from about 0.624 in batch 2 to 0.570, 0.485, and 0.474 in batches 5\u20137, while recovery also declined. The observation is real, but the crystallization comparison is confounded by different temperature histories.\n- Crystallization rejected impurities effectively. Even batches with poorer reaction selectivity generally produced crystals of purity 0.966\u20131.000. Batch 12 combined only 0.522 reaction selectivity with 0.993 crystal purity.\n\nInterpretations supported but not proven:\n- The proposed explanation is that quenching created an uncontrolled primary-nucleation population before seed control, whereas batch 12 developed supersaturation in the presence of seed. The batch contrast supports this, but quench omission, hot seeding, staged cooling, and a longer chemically active history changed together.\n- The interpretation that S0 changes both reaction selectivity and solubility/nucleation behavior is plausible, but only its net process advantage was observed.\n- The claim that batch 12 sacrificed reaction selectivity because the unquenched reaction remained active is consistent with its byproduct signal of 0.379 and degradation warning of 0.224, but residence time and temperature were not independently varied.\n\nContradicted or weakened:\n- \u201cSlower cooling by itself is sufficient\u201d is weakened by batch 5: extensive staged cooling after a quench still produced a fines fraction of 1.000. Solvent and concentration confounding prevent a definitive contradiction.\n- \u201cMore seed necessarily prevents fines\u201d is contradicted under post-quench conditions by batch 8, where 1.0 g total seed still gave fines of 0.987.\n- C1 was not shown to be a uniquely optimal catalyst; C0 and C3 were broadly competitive in batches 1 and 4.\n\nStill untested:\n- The separate causal contributions of avoiding the quench, seeding while hot, and staged cooling.\n- Seed-dose, endpoint-temperature, agitation, and cooling-rate effects within the successful no-quench regime.\n- Whether a reaction-arrest strategy could preserve the morphology of batch 12 while avoiding its selectivity/degradation penalty.\n- Controlled concentration effects and fully matched solvent comparisons.\n\n2. One additional experiment\n\nI would repeat batch 12 as closely as possible but insert a transient quench immediately after reaction, reheat rapidly to the original pre-cooling temperature, then add 0.05 g seed and use the same 330\u2192315\u2192300\u2192285 K staged cooling and four final holds. This uses batch 12 as the existing control while changing principally whether the liquid experiences an unseeded quench.\n\nIt would distinguish two explanations:\n- Irreversible quench-nucleation explanation: the transient quench creates many nuclei that survive reheating. Expected outcome: fines return toward roughly 0.9\u20131.0, crystal size and CSD quality fall, while purity remains high and recovery remains around the previously observed 0.4\u20130.46 range.\n- Staged-cooling-dominant explanation: reheating removes any transient nuclei, and the subsequent seeded staged cooling controls the population. Expected outcome: fines remain near the batch-12 region, roughly 0.45\u20130.55, with size and CSD quality also similar to batch 12.\n\nAn intermediate result would indicate that both irreversible quench history and the later cooling program contribute. Reheating also changes reaction exposure slightly, so reaction selectivity would be a secondary diagnostic rather than the primary causal endpoint.\n\n3. Least effectively used observation and least reliable prediction\n\nThe account used the paired in-process and final crystal-size readings least effectively. In batch 12, crystal size changed from 0.058 in-process to 0.099 in the final assay even though fines agreed closely. Batch 8 similarly changed from 0.042 to 0.085. Because filtration should not be assumed to cause this much genuine growth, these discrepancies could reflect measurement basis, sampling, or noise. I relied primarily on fines and did not fully incorporate this repeated size inconsistency into the morphology mechanism.\n\nQ12 is the least reliable held-out prediction. Its doubled reagent charge tests a concentration effect that was never isolated experimentally. Concentration can alter reaction composition, supersaturation, nucleation, growth, impurity occlusion, and recovery nonlinearly. The campaign\u2019s concentrated quenched batches generally produced almost all fines, whereas the one feasible batch also changed quench and seeding history. Therefore the sealed Q12 estimates\u2014especially fines near the 0.50 boundary and the resulting feasibility classification\u2014depend on extrapolation rather than a controlled campaign comparison."
  },
  "failure": null,
  "elapsed_s": 57.51500000001397,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 531328,
    "input_tokens": 650917,
    "output_tokens": 18623,
    "reasoning_output_tokens": 8628
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
    "selection_rationale": "Batch 12 gave the highest observed seed-excluded crystal recovery among batches meeting both constraints: crystal_yield 0.453, crystal_purity 0.993, and fines fraction 0.468. Seeding before any abrupt quench and staged cooling was decisive."
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
    "lifecycle_index": 12,
    "source_attempts": 17
  },
  "prediction_evaluation": {
    "contrasts": [
      {
        "absolute_delta_error": 0.004288415095558218,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_yield",
        "predicted_delta": -0.07,
        "resolved": true,
        "true_delta": -0.06571158490444179
      },
      {
        "absolute_delta_error": 0.007123577190615293,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_purity",
        "predicted_delta": -0.010000000000000009,
        "resolved": false,
        "true_delta": -0.0028764228093847155
      },
      {
        "absolute_delta_error": 0.03900493628075631,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_size",
        "predicted_delta": -0.020000000000000004,
        "resolved": true,
        "true_delta": 0.019004936280756307
      },
      {
        "absolute_delta_error": 0.8576947480077399,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.14999999999999997,
        "resolved": true,
        "true_delta": -0.7076947480077399
      },
      {
        "absolute_delta_error": 0.04008776257407509,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_yield",
        "predicted_delta": 0.03999999999999998,
        "resolved": false,
        "true_delta": -8.776257407511201e-05
      },
      {
        "absolute_delta_error": 0.008582735806473507,
        "direction_correct": true,
        "factor": "seed",
        "metric": "crystal_purity",
        "predicted_delta": 0.0,
        "resolved": false,
        "true_delta": 0.008582735806473507
      },
      {
        "absolute_delta_error": 0.049125123275801166,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_size",
        "predicted_delta": 0.04999999999999999,
        "resolved": false,
        "true_delta": 0.0008748767241988226
      },
      {
        "absolute_delta_error": 0.32137923157767695,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.29000000000000004,
        "resolved": false,
        "true_delta": 0.031379231577676914
      },
      {
        "absolute_delta_error": 0.009644873190271797,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_yield",
        "predicted_delta": 0.010000000000000009,
        "resolved": false,
        "true_delta": 0.0003551268097282123
      },
      {
        "absolute_delta_error": 0.007794923247214758,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.01200000000000001,
        "resolved": false,
        "true_delta": -0.004205076752785253
      },
      {
        "absolute_delta_error": 0.028451506325525677,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_size",
        "predicted_delta": -0.07500000000000001,
        "resolved": true,
        "true_delta": -0.046548493674474334
      },
      {
        "absolute_delta_error": 0.1802009392429924,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.56,
        "resolved": true,
        "true_delta": 0.7402009392429925
      },
      {
        "absolute_delta_error": 0.08146629297589669,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_yield",
        "predicted_delta": -0.040000000000000036,
        "resolved": true,
        "true_delta": 0.04146629297589666
      },
      {
        "absolute_delta_error": 0.0018305775259815915,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.008000000000000007,
        "resolved": false,
        "true_delta": -0.009830577525981599
      },
      {
        "absolute_delta_error": 0.01436144002797398,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_size",
        "predicted_delta": -0.05500000000000001,
        "resolved": true,
        "true_delta": -0.04063855997202603
      },
      {
        "absolute_delta_error": 0.4478652105803905,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.31999999999999995,
        "resolved": true,
        "true_delta": 0.7678652105803905
      },
      {
        "absolute_delta_error": 0.011999610374702097,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_yield",
        "predicted_delta": 0.14,
        "resolved": true,
        "true_delta": 0.12800038962529792
      },
      {
        "absolute_delta_error": 0.00828274536290019,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_purity",
        "predicted_delta": -0.0050000000000000044,
        "resolved": true,
        "true_delta": -0.013282745362900195
      },
      {
        "absolute_delta_error": 0.0015342445324825968,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_size",
        "predicted_delta": 0.015,
        "resolved": true,
        "true_delta": 0.013465755467517403
      },
      {
        "absolute_delta_error": 0.1288424083411841,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.09999999999999998,
        "resolved": false,
        "true_delta": 0.028842408341184123
      },
      {
        "absolute_delta_error": 0.05746325316856793,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_yield",
        "predicted_delta": 0.09000000000000002,
        "resolved": true,
        "true_delta": 0.032536746831432095
      },
      {
        "absolute_delta_error": 0.017192382855165667,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_purity",
        "predicted_delta": -0.02300000000000002,
        "resolved": false,
        "true_delta": -0.005807617144834354
      },
      {
        "absolute_delta_error": 0.010611719188503135,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_size",
        "predicted_delta": -0.04500000000000001,
        "resolved": true,
        "true_delta": -0.03438828081149688
      },
      {
        "absolute_delta_error": 0.4310258952283489,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.30999999999999994,
        "resolved": true,
        "true_delta": 0.7410258952283488
      }
    ],
    "failures": [],
    "metrics": {
      "crystal_fines_fraction": {
        "coverage80": 0.3333333333333333,
        "interval_score80": 1.4436286308304016,
        "interval_width": 0.31416666666666665,
        "mae": 0.2337896789554853,
        "n": 12,
        "planned": 12
      },
      "crystal_purity": {
        "coverage80": 1.0,
        "interval_score80": 0.05283333333333335,
        "interval_width": 0.05283333333333335,
        "mae": 0.007299288416987589,
        "n": 12,
        "planned": 12
      },
      "crystal_size": {
        "coverage80": 1.0,
        "interval_score80": 0.09833333333333333,
        "interval_width": 0.09833333333333333,
        "mae": 0.031518066028985485,
        "n": 12,
        "planned": 12
      },
      "crystal_yield": {
        "coverage80": 0.25,
        "interval_score80": 0.7867534972439915,
        "interval_width": 0.16833333333333333,
        "mae": 0.1396483096175683,
        "n": 12,
        "planned": 12
      }
    },
    "quality": {
      "balanced_accuracy": 0.75,
      "false_negative": 2,
      "false_positive": 1,
      "true_negative": 5,
      "true_positive": 4
    },
    "resolved_direction_correct": 10,
    "resolved_direction_n": 14,
    "tie_correct": 4,
    "tie_n": 10,
    "valid": true
  },
  "public_baselines": {
    "available": true,
    "mae": {
      "public_mean": {
        "crystal_fines_fraction": 0.3646230122888186,
        "crystal_purity": 0.004853877593426999,
        "crystal_size": 0.021218468792623735,
        "crystal_yield": 0.15369456506702225
      },
      "public_nearest_neighbor": {
        "crystal_fines_fraction": 0.28183662686302924,
        "crystal_purity": 0.009517288337172894,
        "crystal_size": 0.03292789570571389,
        "crystal_yield": 0.17332151777478977
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
        "cached_input": 496640,
        "input": 528918,
        "output": 8214,
        "stage": "source",
        "uncached_input": 32278
      },
      {
        "cached_input": 3456,
        "input": 31406,
        "output": 3007,
        "stage": "K1",
        "uncached_input": 27950
      },
      {
        "cached_input": 0,
        "input": 42949,
        "output": 4775,
        "stage": "Q",
        "uncached_input": 42949
      },
      {
        "cached_input": 31232,
        "input": 47644,
        "output": 2627,
        "stage": "K2",
        "uncached_input": 16412
      }
    ],
    "total": {
      "cached_input": 531328,
      "input": 650917,
      "input_plus_output": 669540,
      "output": 18623,
      "uncached_input": 119589
    },
    "valid": true
  },
  "elapsed_s": 500.3279999999795
}
```
