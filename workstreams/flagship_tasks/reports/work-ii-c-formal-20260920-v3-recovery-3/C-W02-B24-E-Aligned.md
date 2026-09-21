# C-W02-B24-E-Aligned

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
      "target_temperature_K": 380
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "duration_s": 1800,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
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
  "end_step": 14,
  "lifecycle_index": 1,
  "metrics": {
    "byproduct_signal": 0.35537949204444885,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6078317165374756,
    "crystal_fines_fraction": 0.6378909349441528,
    "crystal_purity": 0.9906670451164246,
    "crystal_size": 0.06500610709190369,
    "crystal_yield": 0.4357644319534302,
    "degradation_warning": 0.18438784778118134,
    "safety_risk": 0.18029959499835968,
    "score": 0.44624829292297363,
    "selectivity": 0.527653157711029,
    "virtual_spectrum_summary": 0.27843326330184937,
    "yield": 0.5254906415939331
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
      "catalyst": 1,
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
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 7200,
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
  "end_step": 29,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.421042799949646,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6902841329574585,
    "crystal_fines_fraction": 0.49666833877563477,
    "crystal_purity": 0.9850707054138184,
    "crystal_size": 0.106058269739151,
    "crystal_yield": 0.33336564898490906,
    "degradation_warning": 0.2087850421667099,
    "safety_risk": 0.16786594688892365,
    "score": 0.43696483969688416,
    "selectivity": 0.437523752450943,
    "virtual_spectrum_summary": 0.32552680373191833,
    "yield": 0.42607876658439636
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
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
    },
    {
      "duration_s": 1800,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
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
      "target_temperature_K": 280
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 260
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 200,
      "target_temperature_K": 285
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
  "end_step": 45,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.32049795985221863,
    "conversion": 0.9983178973197937,
    "cost": 1.0,
    "crystal_csd_quality": 0.5244284272193909,
    "crystal_fines_fraction": 0.848816454410553,
    "crystal_purity": 0.9937123656272888,
    "crystal_size": 0.057311829179525375,
    "crystal_yield": 0.4250226616859436,
    "degradation_warning": 0.11567201465368271,
    "safety_risk": 0.1766202598810196,
    "score": 0.4015159606933594,
    "selectivity": 0.5038632154464722,
    "virtual_spectrum_summary": 0.22832629084587097,
    "yield": 0.5029758810997009
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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
    },
    {
      "duration_s": 1800,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 7200,
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
  "end_step": 60,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.2658352851867676,
    "conversion": 0.9889561533927917,
    "cost": 1.0,
    "crystal_csd_quality": 0.5058400630950928,
    "crystal_fines_fraction": 0.9278719425201416,
    "crystal_purity": 1.0,
    "crystal_size": 0.06379591673612595,
    "crystal_yield": 0.46878141164779663,
    "degradation_warning": 0.05882728472352028,
    "safety_risk": 0.16494472324848175,
    "score": 0.4147324860095978,
    "selectivity": 0.5736984014511108,
    "virtual_spectrum_summary": 0.17268168926239014,
    "yield": 0.5600457787513733
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
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
    },
    {
      "duration_s": 1800,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 7200,
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
  "end_step": 75,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.2715888023376465,
    "conversion": 0.9959814548492432,
    "cost": 1.0,
    "crystal_csd_quality": 0.5370773673057556,
    "crystal_fines_fraction": 0.8431285619735718,
    "crystal_purity": 0.9778615236282349,
    "crystal_size": 0.04553816840052605,
    "crystal_yield": 0.45019346475601196,
    "degradation_warning": 0.0652637779712677,
    "safety_risk": 0.14053602516651154,
    "score": 0.4257817268371582,
    "selectivity": 0.5983132719993591,
    "virtual_spectrum_summary": 0.17874254286289215,
    "yield": 0.5919519662857056
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
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
    },
    {
      "duration_s": 1800,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 7200,
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
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.3598284423351288,
    "conversion": 0.9924048781394958,
    "cost": 1.0,
    "crystal_csd_quality": 0.6110848188400269,
    "crystal_fines_fraction": 0.6143476963043213,
    "crystal_purity": 0.9949021935462952,
    "crystal_size": 0.04774856194853783,
    "crystal_yield": 0.3150484561920166,
    "degradation_warning": 0.08614901453256607,
    "safety_risk": 0.17565606534481049,
    "score": 0.3977625370025635,
    "selectivity": 0.4154513478279114,
    "virtual_spectrum_summary": 0.23667269945144653,
    "yield": 0.41732487082481384
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
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
  "end_step": 112,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.31283316016197205,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5225600600242615,
    "crystal_fines_fraction": 0.8380551338195801,
    "crystal_purity": 0.9837294220924377,
    "crystal_size": 0.08155955374240875,
    "crystal_yield": 0.45007428526878357,
    "degradation_warning": 0.09458953887224197,
    "safety_risk": 0.1771966964006424,
    "score": 0.4086912274360657,
    "selectivity": 0.48431092500686646,
    "virtual_spectrum_summary": 0.21462354063987732,
    "yield": 0.5109575390815735
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
    },
    {
      "duration_s": 1800,
      "operation": "cool_crystallize",
      "target_temperature_K": 315
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 305
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 295
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 285
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 275
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 265
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
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.3051431179046631,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.550997257232666,
    "crystal_fines_fraction": 0.8421375155448914,
    "crystal_purity": 0.9839559197425842,
    "crystal_size": 0.09709794819355011,
    "crystal_yield": 0.44936665892601013,
    "degradation_warning": 0.10115741938352585,
    "safety_risk": 0.17700912058353424,
    "score": 0.41688212752342224,
    "selectivity": 0.5154938101768494,
    "virtual_spectrum_summary": 0.21334955096244812,
    "yield": 0.5071879625320435
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 340
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
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 7200,
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
  "end_step": 142,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.4190242886543274,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6825714707374573,
    "crystal_fines_fraction": 0.4933629333972931,
    "crystal_purity": 0.9843270778656006,
    "crystal_size": 0.057944606989622116,
    "crystal_yield": 0.35794374346733093,
    "degradation_warning": 0.20854470133781433,
    "safety_risk": 0.16786594688892365,
    "score": 0.4358385503292084,
    "selectivity": 0.4149165749549866,
    "virtual_spectrum_summary": 0.32430848479270935,
    "yield": 0.4285925328731537
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
      "catalyst": 1,
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
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
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
      "target_temperature_K": 280
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 260
    },
    {
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 275
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
  "end_step": 156,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.41496801376342773,
    "conversion": 0.9858242273330688,
    "cost": 1.0,
    "crystal_csd_quality": 0.6445817351341248,
    "crystal_fines_fraction": 0.5052676200866699,
    "crystal_purity": 0.9805374145507812,
    "crystal_size": 0.07126512378454208,
    "crystal_yield": 0.35252687335014343,
    "degradation_warning": 0.22183452546596527,
    "safety_risk": 0.1675238013267517,
    "score": 0.42706790566444397,
    "selectivity": 0.42411401867866516,
    "virtual_spectrum_summary": 0.3280579447746277,
    "yield": 0.4330408275127411
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 340
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
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 7200,
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
  "end_step": 171,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.38408777117729187,
    "conversion": 0.9990203976631165,
    "cost": 1.0,
    "crystal_csd_quality": 0.6324558258056641,
    "crystal_fines_fraction": 0.5700771808624268,
    "crystal_purity": 0.9916724562644958,
    "crystal_size": 0.07287661731243134,
    "crystal_yield": 0.4049835205078125,
    "degradation_warning": 0.17986096441745758,
    "safety_risk": 0.17473043501377106,
    "score": 0.4442848563194275,
    "selectivity": 0.5003453493118286,
    "virtual_spectrum_summary": 0.2921857237815857,
    "yield": 0.4808554947376251
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 340
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
      "duration_s": 7200,
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
      "target_temperature_K": 260
    },
    {
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 278
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
  "end_step": 185,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.37202978134155273,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6424725651741028,
    "crystal_fines_fraction": 0.5795286893844604,
    "crystal_purity": 0.9928922653198242,
    "crystal_size": 0.09369603544473648,
    "crystal_yield": 0.39647695422172546,
    "degradation_warning": 0.20405836403369904,
    "safety_risk": 0.17410241067409515,
    "score": 0.44435858726501465,
    "selectivity": 0.4773375689983368,
    "virtual_spectrum_summary": 0.2964426577091217,
    "yield": 0.48237961530685425
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
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
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 7200,
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
  "end_step": 200,
  "lifecycle_index": 13,
  "metrics": {
    "byproduct_signal": 0.431435227394104,
    "conversion": 0.9972169399261475,
    "cost": 1.0,
    "crystal_csd_quality": 0.7235825657844543,
    "crystal_fines_fraction": 0.3908766210079193,
    "crystal_purity": 0.980874240398407,
    "crystal_size": 0.07996022701263428,
    "crystal_yield": 0.225163534283638,
    "degradation_warning": 0.1298966258764267,
    "safety_risk": 0.1530250757932663,
    "score": 0.40197163820266724,
    "selectivity": 0.31475329399108887,
    "virtual_spectrum_summary": 0.29574286937713623,
    "yield": 0.30674076080322266
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
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
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 7200,
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
  "lifecycle_index": 14,
  "metrics": {
    "byproduct_signal": 0.44574829936027527,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7417283654212952,
    "crystal_fines_fraction": 0.3800778388977051,
    "crystal_purity": 0.9642019271850586,
    "crystal_size": 0.11707546561956406,
    "crystal_yield": 0.24260485172271729,
    "degradation_warning": 0.13482224941253662,
    "safety_risk": 0.15336500108242035,
    "score": 0.4104568362236023,
    "selectivity": 0.3081522583961487,
    "virtual_spectrum_summary": 0.30583158135414124,
    "yield": 0.30196478962898254
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 3,
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
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 7200,
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
  "end_step": 231,
  "lifecycle_index": 15,
  "metrics": {
    "byproduct_signal": 0.4719747304916382,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6970936059951782,
    "crystal_fines_fraction": 0.40590789914131165,
    "crystal_purity": 0.987014651298523,
    "crystal_size": 0.09236575663089752,
    "crystal_yield": 0.28015467524528503,
    "degradation_warning": 0.24758704006671906,
    "safety_risk": 0.16032955050468445,
    "score": 0.4213424324989319,
    "selectivity": 0.3615472614765167,
    "virtual_spectrum_summary": 0.3710002899169922,
    "yield": 0.3660818338394165
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 3,
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
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 7200,
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
  "lifecycle_index": 16,
  "metrics": {
    "byproduct_signal": 0.46505358815193176,
    "conversion": 0.9885537624359131,
    "cost": 1.0,
    "crystal_csd_quality": 0.7037613391876221,
    "crystal_fines_fraction": 0.3255758583545685,
    "crystal_purity": 0.9770228862762451,
    "crystal_size": 0.0887569785118103,
    "crystal_yield": 0.3017299771308899,
    "degradation_warning": 0.2589113116264343,
    "safety_risk": 0.1608027219772339,
    "score": 0.43212151527404785,
    "selectivity": 0.3586989641189575,
    "virtual_spectrum_summary": 0.3722895681858063,
    "yield": 0.3570535480976105
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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
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
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 7200,
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
  "lifecycle_index": 17,
  "metrics": {
    "byproduct_signal": 0.357372522354126,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6089425086975098,
    "crystal_fines_fraction": 0.6296520829200745,
    "crystal_purity": 0.9989623427391052,
    "crystal_size": 0.06453745812177658,
    "crystal_yield": 0.40640243887901306,
    "degradation_warning": 0.11983180046081543,
    "safety_risk": 0.1714790165424347,
    "score": 0.4293133616447449,
    "selectivity": 0.4511529207229614,
    "virtual_spectrum_summary": 0.25047919154167175,
    "yield": 0.4613091051578522
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 5400,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 335
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
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 7200,
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
  "lifecycle_index": 18,
  "metrics": {
    "byproduct_signal": 0.3918219208717346,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7049919366836548,
    "crystal_fines_fraction": 0.49239909648895264,
    "crystal_purity": 0.9936994314193726,
    "crystal_size": 0.12191345542669296,
    "crystal_yield": 0.3509044647216797,
    "degradation_warning": 0.18270093202590942,
    "safety_risk": 0.16623903810977936,
    "score": 0.4460429847240448,
    "selectivity": 0.40981990098953247,
    "virtual_spectrum_summary": 0.29771748185157776,
    "yield": 0.42322686314582825
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 9000,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 345
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
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 7200,
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
  "lifecycle_index": 19,
  "metrics": {
    "byproduct_signal": 0.4337581992149353,
    "conversion": 0.9909035563468933,
    "cost": 1.0,
    "crystal_csd_quality": 0.7215122580528259,
    "crystal_fines_fraction": 0.38550320267677307,
    "crystal_purity": 0.9725356698036194,
    "crystal_size": 0.06395988166332245,
    "crystal_yield": 0.39147353172302246,
    "degradation_warning": 0.24348664283752441,
    "safety_risk": 0.17062528431415558,
    "score": 0.4644741714000702,
    "selectivity": 0.4420996606349945,
    "virtual_spectrum_summary": 0.3481360077857971,
    "yield": 0.4456864297389984
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 8000,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 343
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
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 7200,
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
  "end_step": 316,
  "lifecycle_index": 20,
  "metrics": {
    "byproduct_signal": 0.4037071764469147,
    "conversion": 0.9934656023979187,
    "cost": 1.0,
    "crystal_csd_quality": 0.683058500289917,
    "crystal_fines_fraction": 0.463992178440094,
    "crystal_purity": 0.9909637570381165,
    "crystal_size": 0.07650886476039886,
    "crystal_yield": 0.4047354459762573,
    "degradation_warning": 0.218765527009964,
    "safety_risk": 0.17329208552837372,
    "score": 0.4611184895038605,
    "selectivity": 0.47686848044395447,
    "virtual_spectrum_summary": 0.32048341631889343,
    "yield": 0.46054667234420776
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7600,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 342
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
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 7200,
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
  "end_step": 333,
  "lifecycle_index": 21,
  "metrics": {
    "byproduct_signal": 0.36941197514533997,
    "conversion": 0.9894089102745056,
    "cost": 1.0,
    "crystal_csd_quality": 0.7135125398635864,
    "crystal_fines_fraction": 0.4961737394332886,
    "crystal_purity": 0.9882955551147461,
    "crystal_size": 0.05735240504145622,
    "crystal_yield": 0.42615360021591187,
    "degradation_warning": 0.20444928109645844,
    "safety_risk": 0.17435522377490997,
    "score": 0.4695637822151184,
    "selectivity": 0.4682571589946747,
    "virtual_spectrum_summary": 0.29517877101898193,
    "yield": 0.48753437399864197
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7400,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 341.5
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
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 7200,
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
  "end_step": 350,
  "lifecycle_index": 22,
  "metrics": {
    "byproduct_signal": 0.3892713487148285,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6628174781799316,
    "crystal_fines_fraction": 0.5086941719055176,
    "crystal_purity": 1.0,
    "crystal_size": 0.07247857749462128,
    "crystal_yield": 0.41851162910461426,
    "degradation_warning": 0.2020251601934433,
    "safety_risk": 0.17488431930541992,
    "score": 0.458503782749176,
    "selectivity": 0.4704231917858124,
    "virtual_spectrum_summary": 0.3050105571746826,
    "yield": 0.47170206904411316
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7600,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 342
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
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 7200,
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
  "end_step": 367,
  "lifecycle_index": 23,
  "metrics": {
    "byproduct_signal": 0.39248332381248474,
    "conversion": 0.9950222373008728,
    "cost": 1.0,
    "crystal_csd_quality": 0.6896156668663025,
    "crystal_fines_fraction": 0.4521363377571106,
    "crystal_purity": 0.9955351948738098,
    "crystal_size": 0.09576002508401871,
    "crystal_yield": 0.408612996339798,
    "degradation_warning": 0.20128533244132996,
    "safety_risk": 0.17435522377490997,
    "score": 0.4708402454853058,
    "selectivity": 0.48318037390708923,
    "virtual_spectrum_summary": 0.3064442276954651,
    "yield": 0.4849386215209961
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
      "volume_L": 0.079999999999999
    },
    {
      "amount_mol": 0.039999999999999,
      "operation": "add_reagent"
    },
    {
      "catalyst": 0,
      "catalyst_amount_mol": 0.004999999999999,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7800,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 342.5
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
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 7200,
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
  "end_step": 383,
  "lifecycle_index": 24,
  "metrics": {
    "byproduct_signal": 0.39794477820396423,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6691397428512573,
    "crystal_fines_fraction": 0.500497043132782,
    "crystal_purity": 1.0,
    "crystal_size": 0.07290384918451309,
    "crystal_yield": 0.3983175456523895,
    "degradation_warning": 0.20987293124198914,
    "safety_risk": 0.17382441461086273,
    "score": 0.4569832980632782,
    "selectivity": 0.4722296893596649,
    "virtual_spectrum_summary": 0.31331244111061096,
    "yield": 0.4814795255661011
  },
  "ordinal": 24
}
```

## K1

```json
{
  "payload": {
    "report": "Mechanistic account\n\nRecommended process (sealed batch 21): charge 0.080 L solvent-S2, 0.040 mol limiting reagent, and 0.005 mol catalyst-C0. Heat at 342 K for 7,600 s with 500 rpm stirring. Cool to 320 K over 3,600 s, add 0.050 g seed, then cool sequentially to 310 K for 3,600 s, 300 K for 7,200 s, and 290, 280, 270, 260, and 250 K for 14,400 s at each step. Filter, terminate, and assay. The final assay gave conversion 0.9894, reaction yield 0.4875, selectivity 0.4683, crystal recovery 0.4262, purity 0.9883, and number-fines fraction 0.4962. It was the highest observed recovery satisfying purity >=0.80 and fines <=0.50.\n\nObserved material effects\n\nSolvent identity strongly affected crystallization. Under broadly comparable C1, 330 K reaction studies, S1 (batch 4) and S0 (batch 5) gave high recovery, 0.4688 and 0.4502, but unacceptable fines of 0.9279 and 0.8431. S3 (batch 6) improved fines to 0.6143 but lowered recovery to 0.3150. S2 supported the best eventual recovery/fines compromise. This is directionally consistent with its nominal low solubility, high growth, low nucleation, and low impurity-occlusion descriptors, although the experiments did not independently measure those properties and the comparisons are partly confounded by process history.\n\nCatalyst identity altered both reaction composition and downstream particle behavior. With S2, a 340 K/7,200 s reaction, and the same seeded cooling schedule to 270 K, C1 in batch 9 gave recovery 0.3579 and fines 0.4934; C0 in batch 11 gave higher recovery, 0.4050, but fines 0.5701; C2 in batch 13 gave only 0.2252 recovery but fines 0.3909; and C3 in batch 15 gave 0.2802 recovery and fines 0.4059. Thus catalysts cannot be ranked solely by conversion or nominal activity: their reaction mixtures had materially different crystallization behavior.\n\nReaction\u2013crystallization coupling\n\nNearly complete conversion did not ensure a good isolated product. Many batches had conversion near 1 while showing very different crystal recovery and fines. The data suggest that the catalyst and thermal reaction history changed concentrations of target, byproduct, and degradation species, which then changed target solubility, nucleation, growth, or impurity adsorption during cooling. This modifier hypothesis is an interpretation rather than a directly identified mechanism.\n\nFor C0, increasing reaction severity moved the system toward fewer fines. Batch 11 at 340 K for 7,200 s gave fines 0.5701 and recovery 0.4050. A more severe 345 K/9,000 s history in batch 19 gave fines 0.3855 and recovery 0.3915. Intermediate conditions produced the useful boundary: batch 20 at 343 K/8,000 s gave recovery 0.4047 and fines 0.4640; batch 21 at 342 K/7,600 s gave recovery 0.4262 and fines 0.4962. Slightly milder batch 22, 341.5 K/7,400 s, crossed the constraint at fines 0.5087. This narrow transition motivated the final C0 operating point.\n\nA plausible explanation is adsorption of reaction-derived impurities on high-curvature nuclei or active crystal faces, suppressing secondary nucleation relative to growth. An alternative is that reaction history changes effective product concentration or solvent activity rather than nucleation kinetics directly. No species-specific or surface measurement distinguished these possibilities.\n\nProcess-history dependence\n\nThe endpoint temperature alone was insufficient to predict the solid. Batch 2 used C1 at 340 K/7,200 s and a staged seeded descent to 270 K, producing recovery 0.3334 and fines 0.4967. With milder reaction histories, prolonged or deeper cooling raised recovery but generated many fines: batches 7 and 8 gave recoveries near 0.45 but fines near 0.84. Batch 3, which included a 260 K crystallization, reheating to 285 K, and recooling, still gave fines 0.8488. Batch 10 used a smaller reheating treatment and ended near the boundary, with recovery 0.3525 and fines 0.5053. Reheating therefore did not reliably erase prior nucleation.\n\nThe effect also depended on catalyst. Extending the C3 schedule from 270 K in batch 15 to 250 K in batch 16 increased recovery from 0.2802 to 0.3017 while decreasing measured fines from 0.4059 to 0.3256. This contrasts with the C1 results and reinforces that cooling time and temperature interact with mixture composition.\n\nUseful relationships\n\nLet P_pre be target product present immediately before separation and P_rec the seed-excluded recovered target. The reported crystallization recovery is Yc = P_rec/P_pre; it is not the overall yield from charged reagent. A simple overall target balance is approximately P_rec = n_R\u00b7X\u00b7S_rxn\u00b7Yc, where n_R is reagent charge, X conversion, and S_rxn effective reaction selectivity. This explains why high crystal recovery cannot compensate indefinitely for poor reaction selectivity.\n\nFor crystallization, supersaturation may be represented as sigma(t) = C(t)/C*(T, solvent, impurities) - 1. Qualitatively, nucleation and growth can be written J = k_n sigma^m and G = k_g sigma^g. The number-fines metric is F20 = N(d < 20 micrometres)/N_total. Cooling to lower temperature reduces equilibrium solubility and tends to raise recovery, approximately Yc \u2248 1 - C*(Tf)V/P_pre - separation losses, but a large or persistent sigma increases J and therefore F20. Seeds provide growth area that can consume supersaturation, whereas excessive residence under supersaturated conditions can accumulate secondary nuclei. Catalyst- and degradation-derived species may alter C*, k_n, or k_g.\n\nRevisions and uncertainty\n\nThe campaign began with C1/S2 and high-temperature or simple cooling protocols. Batch 1 achieved recovery 0.4358 but failed the fines constraint at 0.6379. Slower seeded cooling in batches 2 and 9 established feasibility near 0.50 fines, after which catalyst screening revealed the recovery/fines tradeoff. C2 and C3 offered comfortable fines margins but low recovery; C0 offered higher recovery and was tuned through batches 19\u201324. The recommendation was consequently revised to batch 21.\n\nPurity was not the limiting uncertainty: batch 21 measured 0.9883, far above 0.80. Fines were limiting. Batch 21's 0.4962 is only 0.0038 below the threshold and smaller than the declared final-assay fines noise scale of about 0.018. Its direct repeat, batch 23, supported the process with fines 0.4521 and recovery 0.4086, but demonstrated run-to-run or measurement variability. Batch 24 gave 0.5005 fines, effectively on the boundary. In-situ particle and final-assay values also sometimes differed; for batch 23 they were 0.5013 and 0.4521, respectively. The final assay was used for formal selection, but these discrepancies argue for operating margin in deployment.\n\nThe unresolved tradeoff is that the highest recoveries occurred near or above the fines boundary. Milder reaction histories often recovered about 0.42\u20130.47 but produced excessive fines, whereas conditions providing a wide fines margin generally recovered about 0.23\u20130.39. Untested alternatives include optimizing seed size distribution or dose, adding a controlled antisolvent, selective fines dissolution followed by immediate hot filtration, changing solids concentration or solvent volume, and closed-loop cooling based on supersaturation. No polymorph analysis, direct solubility curve, impurity identification, or scale-up study was performed, so the proposed inhibition/growth mechanism remains provisional."
  },
  "failure": null,
  "elapsed_s": 70.125,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 928768,
    "input_tokens": 1030454,
    "output_tokens": 16649,
    "reasoning_output_tokens": 5352
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
          "estimate": 0.56,
          "lower80": 0.41,
          "upper80": 0.71
        },
        "crystal_purity": {
          "estimate": 0.96,
          "lower80": 0.91,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.075,
          "lower80": 0.035,
          "upper80": 0.125
        },
        "crystal_yield": {
          "estimate": 0.38,
          "lower80": 0.28,
          "upper80": 0.48
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q01"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.47,
          "lower80": 0.32,
          "upper80": 0.62
        },
        "crystal_purity": {
          "estimate": 0.94,
          "lower80": 0.87,
          "upper80": 0.98
        },
        "crystal_size": {
          "estimate": 0.085,
          "lower80": 0.04,
          "upper80": 0.14
        },
        "crystal_yield": {
          "estimate": 0.27,
          "lower80": 0.18,
          "upper80": 0.37
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q02"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.78,
          "lower80": 0.63,
          "upper80": 0.9
        },
        "crystal_purity": {
          "estimate": 0.93,
          "lower80": 0.85,
          "upper80": 0.98
        },
        "crystal_size": {
          "estimate": 0.045,
          "lower80": 0.018,
          "upper80": 0.085
        },
        "crystal_yield": {
          "estimate": 0.28,
          "lower80": 0.18,
          "upper80": 0.39
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q03"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.48,
          "lower80": 0.33,
          "upper80": 0.64
        },
        "crystal_purity": {
          "estimate": 0.95,
          "lower80": 0.89,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.085,
          "lower80": 0.04,
          "upper80": 0.14
        },
        "crystal_yield": {
          "estimate": 0.33,
          "lower80": 0.23,
          "upper80": 0.44
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q04"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.46,
          "lower80": 0.31,
          "upper80": 0.62
        },
        "crystal_purity": {
          "estimate": 0.95,
          "lower80": 0.89,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.09,
          "lower80": 0.045,
          "upper80": 0.145
        },
        "crystal_yield": {
          "estimate": 0.32,
          "lower80": 0.22,
          "upper80": 0.43
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q05"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.72,
          "lower80": 0.57,
          "upper80": 0.85
        },
        "crystal_purity": {
          "estimate": 0.92,
          "lower80": 0.83,
          "upper80": 0.97
        },
        "crystal_size": {
          "estimate": 0.052,
          "lower80": 0.022,
          "upper80": 0.095
        },
        "crystal_yield": {
          "estimate": 0.37,
          "lower80": 0.27,
          "upper80": 0.48
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q06"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.49,
          "lower80": 0.34,
          "upper80": 0.65
        },
        "crystal_purity": {
          "estimate": 0.95,
          "lower80": 0.88,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.085,
          "lower80": 0.04,
          "upper80": 0.14
        },
        "crystal_yield": {
          "estimate": 0.34,
          "lower80": 0.24,
          "upper80": 0.45
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q07"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.63,
          "lower80": 0.45,
          "upper80": 0.78
        },
        "crystal_purity": {
          "estimate": 0.96,
          "lower80": 0.9,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.062,
          "lower80": 0.025,
          "upper80": 0.115
        },
        "crystal_yield": {
          "estimate": 0.25,
          "lower80": 0.14,
          "upper80": 0.37
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q08"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.42,
          "lower80": 0.25,
          "upper80": 0.61
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.92,
          "upper80": 1
        },
        "crystal_size": {
          "estimate": 0.075,
          "lower80": 0.035,
          "upper80": 0.13
        },
        "crystal_yield": {
          "estimate": 0.012,
          "lower80": 0,
          "upper80": 0.045
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q09"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.35,
          "lower80": 0.2,
          "upper80": 0.53
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.92,
          "upper80": 1
        },
        "crystal_size": {
          "estimate": 0.1,
          "lower80": 0.05,
          "upper80": 0.165
        },
        "crystal_yield": {
          "estimate": 0.085,
          "lower80": 0.035,
          "upper80": 0.16
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q10"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.48,
          "lower80": 0.33,
          "upper80": 0.64
        },
        "crystal_purity": {
          "estimate": 0.95,
          "lower80": 0.88,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.087,
          "lower80": 0.042,
          "upper80": 0.142
        },
        "crystal_yield": {
          "estimate": 0.34,
          "lower80": 0.24,
          "upper80": 0.45
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q11"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.67,
          "lower80": 0.51,
          "upper80": 0.81
        },
        "crystal_purity": {
          "estimate": 0.88,
          "lower80": 0.78,
          "upper80": 0.95
        },
        "crystal_size": {
          "estimate": 0.06,
          "lower80": 0.025,
          "upper80": 0.105
        },
        "crystal_yield": {
          "estimate": 0.49,
          "lower80": 0.37,
          "upper80": 0.61
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q12"
      }
    ],
    "rationale": "All recipes contain explicit seed, so particles are expected even where seed-excluded recovery is very low. Q01/Q02 isolates solvent: prior batches indicated higher recovery but more fines with S1 than S3, making Q01 likely fail narrowly while Q02 trades recovery for feasibility. Q03/Q04 isolates seed loading: 0.045 g seed should provide enough growth area to suppress spontaneous nucleation relative to 0.001 g. Q05/Q06 contrasts gradual cooling with an immediate crash; the crash should raise recovery modestly but generate substantially more fines. Q07/Q08 tests thermal cycling: reheating to 315 K can dissolve product, while the rapid one-hour recooling may renucleate it; earlier campaign cycles did not reliably remove fines, so Q08 is assigned lower recovery and worse fines. Q09/Q10 isolates residence at 292 K: after only 60 s, recovered material is mostly seed and seed-excluded yield is near zero; a two-hour hold permits measurable growth and larger, less-fine particles. Q11/Q12 isolates reagent loading: doubling loading should increase fractional recovery by reducing the relative dissolved-product loss, but also increases supersaturation, impurity burden, and fines. Intervals are deliberately broad because these recipes extrapolate to lower volume, lower catalyst loading, much longer cooling histories, and different seed-to-product ratios than the campaign; classifications near fines=0.50 are therefore uncertain."
  },
  "failure": null,
  "elapsed_s": 115.42199999999139,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 979840,
    "input_tokens": 1133181,
    "output_tokens": 22195,
    "reasoning_output_tokens": 9155
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
    "report": "1. Status of the main claims\n\nSupported by direct observations:\n- Material identity affects downstream crystallization independently of conversion. Under matched C1/S2 reaction and cooling conditions, catalyst screening gave distinct recovery/fines outcomes: batch 9 (C1) 0.3579/0.4934, batch 11 (C0) 0.4050/0.5701, batch 13 (C2) 0.2252/0.3909, and batch 15 (C3) 0.2802/0.4059. Solvent changes also produced large differences: batches 4\u20136 gave fines of 0.9279 for S1, 0.8431 for S0, and 0.6143 for S3.\n- Reaction and crystallization are coupled. Nearly complete conversion occurred in many batches despite substantially different crystal recoveries and fines. In the C0 series, moving from batch 11 to batches 19\u201321 changed fines from 0.5701 to 0.3855\u20130.4962 without a comparable conversion change.\n- Process history matters, not merely final temperature. Batch 2 reached 270 K with recovery 0.3334 and fines 0.4967, whereas the longer histories in batches 7 and 8 produced recoveries near 0.45 but fines near 0.84. Thermal cycling in batches 3 and 10 did not reliably eliminate fines.\n- Purity was not the active constraint in the optimized region. Batches 19\u201324 all retained high purity, while feasibility changed chiefly with fines.\n- A narrow recovery/fines boundary exists for C0. Batch 20 gave 0.4047 recovery and 0.4640 fines; batch 21 gave 0.4262 and 0.4962; the slightly milder batch 22 gave 0.4185 and 0.5087. Batch 23 replicated the batch-21 recipe with 0.4086 recovery and 0.4521 fines.\n\nContradicted or qualified:\n- \u201cSlower cooling always improves particle quality\u201d is contradicted by batches 7 and 8, where excessive residence generated many fines.\n- \u201cReheating preferentially removes fines\u201d is not supported by batches 3 and 10. Any dissolution benefit was either weak or offset by subsequent renucleation.\n- The nominal solvent descriptors were not sufficient predictors. In particular, S1\u2019s nominally favorable nucleation and occlusion properties did not prevent the very high fines observed in batch 4.\n- A simple monotonic relationship between measured byproduct signal and fines is not supported. Reaction severity correlated with improved C0 particle quality overall, but individual final-assay byproduct values were noisy and not strictly ordered.\n\nStill untested interpretations:\n- Adsorption of reaction-derived impurities on nuclei or crystal faces remains a hypothesis. No impurity was identified or deliberately added.\n- The alternative explanation\u2014that severe reaction histories merely lower effective target supersaturation or change equilibrium solubility\u2014also remains viable.\n- The proposed J = k_n sigma^m and G = k_g sigma^g relationships are useful organizing equations, but their parameters and even their applicable regimes were not measured.\n- Polymorphism, agglomeration, attrition, seed-size distribution, and scale effects were not characterized.\n\n2. One additional experiment\n\nI would run a concentration-matched mild-history C0 experiment against historical batch 19. Use S2 and the same seed and cooling schedule as batch 19, including cooling to 250 K, but use the milder 340 K/7,200 s reaction history. Reduce the reagent charge to approximately 0.037 mol in 0.080 L so that the expected pre-crystallization target amount is close to that of the more degraded batch-19 mixture. Perform one HPLC measurement immediately before cooling to verify target concentration, conversion, and byproduct signal, then perform particle sizing before filtration and a final assay.\n\nThis would distinguish two leading explanations:\n- Supersaturation/concentration explanation: if lower target concentration alone caused the reduced nucleation, the concentration-matched mild mixture should approach batch 19\u2019s low fines, about 0.39, even though its byproduct profile is milder.\n- Impurity-modifier explanation: if reaction-derived degradation/byproduct species inhibit nucleation or alter growth, the mild mixture should retain substantially higher fines\u2014potentially above 0.50\u2014despite matching target concentration. Its particle-size trajectory should also differ from batch 19.\n\nAn intermediate result would imply contributions from both concentration and modifier chemistry. HPLC would not identify the modifier, but it would prevent target-concentration differences from being mistaken for a chemical inhibition effect.\n\n3. Least effectively used observation and least reliable prediction\n\nThe observation used least effectively was the C3 endpoint comparison between batches 15 and 16. Extending cooling from 270 to 250 K increased recovery from 0.2802 to 0.3017 while decreasing fines from 0.4059 to 0.3256. That behavior runs against the simplest claim that deeper cooling necessarily raises nucleation and fines. I acknowledged it as a catalyst\u2013history interaction but lacked replicate or time-resolved particle data to determine whether it reflected growth, agglomeration, selective dissolution, measurement variation, or a genuinely different C3 impurity effect. It therefore remained an exception rather than an integrated part of the mechanism.\n\nThe least reliable held-out prediction is Q08. It extrapolates from a very long S0 ramp to a large reheating pulse from 278.15 to 315 K followed by only one hour of recooling. The campaign\u2019s thermal cycles were smaller and confounded by different reaction histories. Q08 could plausibly show dissolution and reduced fines, incomplete recrystallization and low recovery, or rapid renucleation with increased fines. My sealed estimate chose the last two effects, but the direction of the fines change is weakly constrained. Q09 is also uncertain because its assay would be dominated by the properties of the added seed after only 60 seconds of cooling, a regime not directly studied."
  },
  "failure": null,
  "elapsed_s": 61.234000000025844,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 1019008,
    "input_tokens": 1190047,
    "output_tokens": 24688,
    "reasoning_output_tokens": 10343
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
    "selection_rationale": "Batch 21 had the highest observed seed-excluded crystal recovery among completed batches meeting both quality constraints: crystal_yield 0.4262, crystal_purity 0.9883, and crystal_fines_fraction 0.4962."
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
        "duration_s": 7600,
        "operation": "heat",
        "stirring_speed_rpm": 500,
        "target_temperature_K": 342
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
        "duration_s": 3600,
        "operation": "cool_crystallize",
        "target_temperature_K": 310
      },
      {
        "duration_s": 7200,
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
    "lifecycle_index": 21,
    "source_attempts": 17
  },
  "prediction_evaluation": {
    "contrasts": [
      {
        "absolute_delta_error": 0.08311778881199469,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_yield",
        "predicted_delta": -0.10999999999999999,
        "resolved": true,
        "true_delta": -0.19311778881199468
      },
      {
        "absolute_delta_error": 0.018552855963854475,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_purity",
        "predicted_delta": -0.020000000000000018,
        "resolved": false,
        "true_delta": -0.0014471440361455423
      },
      {
        "absolute_delta_error": 0.01902680472663707,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_size",
        "predicted_delta": 0.010000000000000009,
        "resolved": true,
        "true_delta": 0.02902680472663708
      },
      {
        "absolute_delta_error": 0.5002675737116522,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.09000000000000008,
        "resolved": true,
        "true_delta": -0.5902675737116523
      },
      {
        "absolute_delta_error": 0.05004843643867041,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_yield",
        "predicted_delta": 0.04999999999999999,
        "resolved": false,
        "true_delta": -4.843643867041836e-05
      },
      {
        "absolute_delta_error": 0.011764438459750726,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_purity",
        "predicted_delta": 0.019999999999999907,
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
        "absolute_delta_error": 0.2793685499038365,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.30000000000000004,
        "resolved": false,
        "true_delta": -0.020631450096163517
      },
      {
        "absolute_delta_error": 0.04973954929716812,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_yield",
        "predicted_delta": 0.04999999999999999,
        "resolved": false,
        "true_delta": 0.00026045070283187144
      },
      {
        "absolute_delta_error": 0.025132146340829498,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.029999999999999916,
        "resolved": false,
        "true_delta": -0.004867853659170418
      },
      {
        "absolute_delta_error": 0.0003793018358954764,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_size",
        "predicted_delta": -0.038,
        "resolved": true,
        "true_delta": -0.03762069816410452
      },
      {
        "absolute_delta_error": 0.31810139828932066,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.25999999999999995,
        "resolved": true,
        "true_delta": 0.5781013982893206
      },
      {
        "absolute_delta_error": 0.13006038328567326,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_yield",
        "predicted_delta": -0.09000000000000002,
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
        "absolute_delta_error": 0.0071029046475648006,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_size",
        "predicted_delta": -0.023000000000000007,
        "resolved": true,
        "true_delta": -0.030102904647564807
      },
      {
        "absolute_delta_error": 0.46239412170088123,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.14,
        "resolved": true,
        "true_delta": 0.6023941217008812
      },
      {
        "absolute_delta_error": 0.0806844221024664,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_yield",
        "predicted_delta": 0.07300000000000001,
        "resolved": true,
        "true_delta": 0.1536844221024664
      },
      {
        "absolute_delta_error": 0.014527106938203138,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_purity",
        "predicted_delta": 0.0,
        "resolved": true,
        "true_delta": -0.014527106938203138
      },
      {
        "absolute_delta_error": 0.01081747475109112,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_size",
        "predicted_delta": 0.02500000000000001,
        "resolved": true,
        "true_delta": 0.014182525248908888
      },
      {
        "absolute_delta_error": 0.08908907723599963,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.07,
        "resolved": false,
        "true_delta": 0.01908907723599962
      },
      {
        "absolute_delta_error": 0.12103124947311256,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_yield",
        "predicted_delta": 0.14999999999999997,
        "resolved": true,
        "true_delta": 0.02896875052688741
      },
      {
        "absolute_delta_error": 0.06394295307809872,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_purity",
        "predicted_delta": -0.06999999999999995,
        "resolved": false,
        "true_delta": -0.006057046921901232
      },
      {
        "absolute_delta_error": 0.0004263528357102142,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_size",
        "predicted_delta": -0.026999999999999996,
        "resolved": true,
        "true_delta": -0.026573647164289782
      },
      {
        "absolute_delta_error": 0.4009082204353358,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.19000000000000006,
        "resolved": true,
        "true_delta": 0.5909082204353359
      }
    ],
    "failures": [],
    "metrics": {
      "crystal_fines_fraction": {
        "coverage80": 0.4166666666666667,
        "interval_score80": 1.848646093535838,
        "interval_width": 0.30916666666666665,
        "mae": 0.26955962519063553,
        "n": 12,
        "planned": 12
      },
      "crystal_purity": {
        "coverage80": 0.75,
        "interval_score80": 0.14726714050795764,
        "interval_width": 0.10833333333333332,
        "mae": 0.03848990262572514,
        "n": 12,
        "planned": 12
      },
      "crystal_size": {
        "coverage80": 0.8333333333333334,
        "interval_score80": 0.09760399328256365,
        "interval_width": 0.09249999999999999,
        "mae": 0.01631284277782266,
        "n": 12,
        "planned": 12
      },
      "crystal_yield": {
        "coverage80": 0.9166666666666666,
        "interval_score80": 0.22844974753890931,
        "interval_width": 0.19083333333333333,
        "mae": 0.05426107851815112,
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
    "resolved_direction_correct": 11,
    "resolved_direction_n": 14,
    "tie_correct": 1,
    "tie_n": 10,
    "valid": true
  },
  "public_baselines": {
    "available": true,
    "mae": {
      "public_mean": {
        "crystal_fines_fraction": 0.28539295852396884,
        "crystal_purity": 0.005512629897723285,
        "crystal_size": 0.017192244486071477,
        "crystal_yield": 0.11545300690377724
      },
      "public_nearest_neighbor": {
        "crystal_fines_fraction": 0.2592659380059838,
        "crystal_purity": 0.006350244021478667,
        "crystal_size": 0.018727271517628447,
        "crystal_yield": 0.1735605147941726
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
        "cached_input": 928768,
        "input": 991088,
        "output": 13333,
        "stage": "source",
        "uncached_input": 62320
      },
      {
        "cached_input": 0,
        "input": 39366,
        "output": 3316,
        "stage": "K1",
        "uncached_input": 39366
      },
      {
        "cached_input": 51072,
        "input": 102727,
        "output": 5546,
        "stage": "Q",
        "uncached_input": 51655
      },
      {
        "cached_input": 39168,
        "input": 56866,
        "output": 2493,
        "stage": "K2",
        "uncached_input": 17698
      }
    ],
    "total": {
      "cached_input": 1019008,
      "input": 1190047,
      "input_plus_output": 1214735,
      "output": 24688,
      "uncached_input": 171039
    },
    "valid": true
  },
  "elapsed_s": 910.8589999999967
}
```
