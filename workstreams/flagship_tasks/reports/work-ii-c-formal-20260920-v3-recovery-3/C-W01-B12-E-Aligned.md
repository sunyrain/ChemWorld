# C-W01-B12-E-Aligned

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
      "target_temperature_K": 350
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.02
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 275
    },
    {
      "duration_s": 7200,
      "operation": "wait",
      "stirring_speed_rpm": 200
    },
    {
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 275
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
    "byproduct_signal": 0.33845067024230957,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7614429593086243,
    "crystal_fines_fraction": 0.32630664110183716,
    "crystal_purity": 0.987845778465271,
    "crystal_size": 0.07998025417327881,
    "crystal_yield": 0.42936956882476807,
    "degradation_warning": 0.1625525951385498,
    "safety_risk": 0.17982865869998932,
    "score": 0.5066112875938416,
    "selectivity": 0.5229513049125671,
    "virtual_spectrum_summary": 0.2592965364456177,
    "yield": 0.520788848400116
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
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 330
    },
    {
      "instrument": "hplc",
      "operation": "measure"
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
  "end_step": 24,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.30678051710128784,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7025934457778931,
    "crystal_fines_fraction": 0.4954153895378113,
    "crystal_purity": 0.9824151992797852,
    "crystal_size": 0.10551143437623978,
    "crystal_yield": 0.41679275035858154,
    "degradation_warning": 0.07411655783653259,
    "safety_risk": 0.1762179434299469,
    "score": 0.47089308500289917,
    "selectivity": 0.49935322999954224,
    "virtual_spectrum_summary": 0.20208173990249634,
    "yield": 0.48790085315704346
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
      "volume_L": 0.04
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
      "target_temperature_K": 350
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.02
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 275
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
  "end_step": 34,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.32346341013908386,
    "conversion": 0.9983179569244385,
    "cost": 1.0,
    "crystal_csd_quality": 0.59870445728302,
    "crystal_fines_fraction": 0.6727116107940674,
    "crystal_purity": 0.9968726634979248,
    "crystal_size": 0.06452759355306625,
    "crystal_yield": 0.45427390933036804,
    "degradation_warning": 0.1694525182247162,
    "safety_risk": 0.20626482367515564,
    "score": 0.4461520314216614,
    "selectivity": 0.5324322581291199,
    "virtual_spectrum_summary": 0.25415849685668945,
    "yield": 0.5315449833869934
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
      "volume_L": 0.06
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
      "target_temperature_K": 350
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.02
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 290
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 275
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
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.31547752022743225,
    "conversion": 0.9889965057373047,
    "cost": 1.0,
    "crystal_csd_quality": 0.7368574738502502,
    "crystal_fines_fraction": 0.3894697427749634,
    "crystal_purity": 1.0,
    "crystal_size": 0.08224877715110779,
    "crystal_yield": 0.45571205019950867,
    "degradation_warning": 0.13589373230934143,
    "safety_risk": 0.18689917027950287,
    "score": 0.5052483677864075,
    "selectivity": 0.5377650260925293,
    "virtual_spectrum_summary": 0.23466481268405914,
    "yield": 0.5241353511810303
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
      "volume_L": 0.05
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
      "operation": "seed_crystals",
      "seed_mass_g": 0.03
    },
    {
      "duration_s": 10000,
      "operation": "cool_crystallize",
      "target_temperature_K": 315
    },
    {
      "duration_s": 10000,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 10000,
      "operation": "cool_crystallize",
      "target_temperature_K": 285
    },
    {
      "duration_s": 10000,
      "operation": "cool_crystallize",
      "target_temperature_K": 275
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
  "end_step": 57,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.333372563123703,
    "conversion": 0.996337890625,
    "cost": 1.0,
    "crystal_csd_quality": 0.7122492790222168,
    "crystal_fines_fraction": 0.43805164098739624,
    "crystal_purity": 0.9836091995239258,
    "crystal_size": 0.05945776402950287,
    "crystal_yield": 0.4618074595928192,
    "degradation_warning": 0.15263791382312775,
    "safety_risk": 0.19446782767772675,
    "score": 0.495085209608078,
    "selectivity": 0.5537917017936707,
    "virtual_spectrum_summary": 0.2520419657230377,
    "yield": 0.5476387739181519
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
      "volume_L": 0.045
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
      "stirring_speed_rpm": 400,
      "target_temperature_K": 350
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 12000,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 12000,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 12000,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 12000,
      "operation": "cool_crystallize",
      "target_temperature_K": 287.5
    },
    {
      "duration_s": 12000,
      "operation": "cool_crystallize",
      "target_temperature_K": 275
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
  "end_step": 70,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.32713520526885986,
    "conversion": 0.9924335479736328,
    "cost": 1.0,
    "crystal_csd_quality": 0.644008457660675,
    "crystal_fines_fraction": 0.5516359210014343,
    "crystal_purity": 1.0,
    "crystal_size": 0.04497065395116806,
    "crystal_yield": 0.48194822669029236,
    "degradation_warning": 0.15462790429592133,
    "safety_risk": 0.2016488015651703,
    "score": 0.4760080575942993,
    "selectivity": 0.546359121799469,
    "virtual_spectrum_summary": 0.24950692057609558,
    "yield": 0.5482447743415833
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
      "volume_L": 0.0475
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
      "stirring_speed_rpm": 400,
      "target_temperature_K": 350
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.03
    },
    {
      "duration_s": 12000,
      "operation": "cool_crystallize",
      "target_temperature_K": 315
    },
    {
      "duration_s": 12000,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 12000,
      "operation": "cool_crystallize",
      "target_temperature_K": 285
    },
    {
      "duration_s": 12000,
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
      "stirring_speed_rpm": 200,
      "target_temperature_K": 305
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.02
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 295
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 285
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
  "end_step": 89,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.3318496644496918,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6345565915107727,
    "crystal_fines_fraction": 0.5671785473823547,
    "crystal_purity": 0.9860414862632751,
    "crystal_size": 0.08619081974029541,
    "crystal_yield": 0.4755668640136719,
    "degradation_warning": 0.15868310630321503,
    "safety_risk": 0.19645418226718903,
    "score": 0.47028788924217224,
    "selectivity": 0.5163883566856384,
    "virtual_spectrum_summary": 0.25392472743988037,
    "yield": 0.5430355668067932
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
      "volume_L": 0.05
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
      "operation": "seed_crystals",
      "seed_mass_g": 0.03
    },
    {
      "duration_s": 10000,
      "operation": "cool_crystallize",
      "target_temperature_K": 315
    },
    {
      "duration_s": 10000,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 10000,
      "operation": "cool_crystallize",
      "target_temperature_K": 285
    },
    {
      "duration_s": 10000,
      "operation": "cool_crystallize",
      "target_temperature_K": 275
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
  "end_step": 102,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.31317397952079773,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7400162816047668,
    "crystal_fines_fraction": 0.4143752455711365,
    "crystal_purity": 0.9862086176872253,
    "crystal_size": 0.11094049364328384,
    "crystal_yield": 0.5002222061157227,
    "degradation_warning": 0.1567138135433197,
    "safety_risk": 0.1956539899110794,
    "score": 0.5166290998458862,
    "selectivity": 0.5463390350341797,
    "virtual_spectrum_summary": 0.24276690185070038,
    "yield": 0.5380337834358215
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
      "volume_L": 0.05
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
      "operation": "seed_crystals",
      "seed_mass_g": 0.03
    },
    {
      "duration_s": 10000,
      "operation": "cool_crystallize",
      "target_temperature_K": 315
    },
    {
      "duration_s": 10000,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 10000,
      "operation": "cool_crystallize",
      "target_temperature_K": 285
    },
    {
      "duration_s": 10000,
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
  "end_step": 116,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.32362353801727295,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7151720523834229,
    "crystal_fines_fraction": 0.42904528975486755,
    "crystal_purity": 0.9885106682777405,
    "crystal_size": 0.061841219663619995,
    "crystal_yield": 0.49830690026283264,
    "degradation_warning": 0.1493174135684967,
    "safety_risk": 0.19601351022720337,
    "score": 0.5039086937904358,
    "selectivity": 0.5245716571807861,
    "virtual_spectrum_summary": 0.24518577754497528,
    "yield": 0.5382475852966309
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
      "volume_L": 0.048
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
      "operation": "seed_crystals",
      "seed_mass_g": 0.03
    },
    {
      "duration_s": 10000,
      "operation": "cool_crystallize",
      "target_temperature_K": 315
    },
    {
      "duration_s": 10000,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 10000,
      "operation": "cool_crystallize",
      "target_temperature_K": 285
    },
    {
      "duration_s": 10000,
      "operation": "cool_crystallize",
      "target_temperature_K": 275
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
  "end_step": 129,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.3167031705379486,
    "conversion": 0.9858242273330688,
    "cost": 1.0,
    "crystal_csd_quality": 0.699244499206543,
    "crystal_fines_fraction": 0.3973061740398407,
    "crystal_purity": 0.9845552444458008,
    "crystal_size": 0.07323906570672989,
    "crystal_yield": 0.4930039346218109,
    "degradation_warning": 0.16107937693595886,
    "safety_risk": 0.19762372970581055,
    "score": 0.5039157271385193,
    "selectivity": 0.5354748368263245,
    "virtual_spectrum_summary": 0.24667246639728546,
    "yield": 0.5444016456604004
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
      "volume_L": 0.05
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
      "operation": "seed_crystals",
      "seed_mass_g": 0.02
    },
    {
      "duration_s": 10000,
      "operation": "cool_crystallize",
      "target_temperature_K": 315
    },
    {
      "duration_s": 10000,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 10000,
      "operation": "cool_crystallize",
      "target_temperature_K": 285
    },
    {
      "duration_s": 10000,
      "operation": "cool_crystallize",
      "target_temperature_K": 275
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
  "end_step": 142,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.32501524686813354,
    "conversion": 0.9990203976631165,
    "cost": 1.0,
    "crystal_csd_quality": 0.7010716795921326,
    "crystal_fines_fraction": 0.4224066436290741,
    "crystal_purity": 0.9992831349372864,
    "crystal_size": 0.08066954463720322,
    "crystal_yield": 0.4832087755203247,
    "degradation_warning": 0.1377437859773636,
    "safety_risk": 0.19530701637268066,
    "score": 0.5023921132087708,
    "selectivity": 0.5485870242118835,
    "virtual_spectrum_summary": 0.24074308574199677,
    "yield": 0.5290971994400024
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
      "volume_L": 0.05
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
      "operation": "seed_crystals",
      "seed_mass_g": 0.04
    },
    {
      "duration_s": 10000,
      "operation": "cool_crystallize",
      "target_temperature_K": 315
    },
    {
      "duration_s": 10000,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 10000,
      "operation": "cool_crystallize",
      "target_temperature_K": 285
    },
    {
      "duration_s": 10000,
      "operation": "cool_crystallize",
      "target_temperature_K": 275
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
  "end_step": 155,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.30901679396629333,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7104334235191345,
    "crystal_fines_fraction": 0.42803114652633667,
    "crystal_purity": 1.0,
    "crystal_size": 0.10217476636171341,
    "crystal_yield": 0.4861587882041931,
    "degradation_warning": 0.15950219333171844,
    "safety_risk": 0.19600459933280945,
    "score": 0.5074852705001831,
    "selectivity": 0.5363444089889526,
    "virtual_spectrum_summary": 0.24173521995544434,
    "yield": 0.5413864254951477
  },
  "ordinal": 12
}
```

## K1

```json
{
  "payload": {
    "report": "Mechanistic account\n\nRecommended completed experiment: batch 8. It used 0.040 mol reagent, 0.050 L solvent-S2, 0.005 mol catalyst-C1, reaction at 350 K for 3600 s with 500 rpm stirring, 0.030 g seed, staged cooling to 315, 300, 285, and 275 K for 10,000 s per stage, then to 260 K for 14,400 s, followed by filtration. Its final assay gave seed-excluded crystal recovery 0.5002, purity 0.9862, fines number fraction 0.4144, normalized crystal size 0.1109, and CSD quality 0.7400. It therefore met both constraints with the highest observed feasible recovery.\n\nMaterial effects\n\nThe public material dossier characterized solvent-S2 as relatively low-solubility (0.70), low-nucleation (0.65), high-growth (1.30), and low-impurity-occlusion (0.65). Those properties provide a coherent interpretation of the generally high crystal purities and useful recoveries obtained with S2: cooling strongly reduces dissolved-product capacity, while growth can compete with secondary nucleation and impurity trapping. However, every completed batch used S2, so its superiority over S0, S1, or S3 remains a prior-based, untested alternative rather than an experimental conclusion.\n\nCatalyst-C1 has higher nominal reference-panel activity than C0. Batch 1 with C1 at 350 K reached conversion 1.000 and reaction yield 0.5208, whereas batch 2 with C0 at 330 K gave conversion 1.000 and yield 0.4879. Selectivities were 0.5230 and 0.4994, respectively. This weakly supports C1, but catalyst identity, temperature, seed charge, and cooling history were changed together; it is not a clean catalyst comparison. Hidden world-specific material residuals also remain possible.\n\nReaction and crystallization coupling\n\nThe reaction generated target together with a substantial byproduct signal. Across the later C1/350 K batches, reaction yield was roughly 0.53\u20130.55 and selectivity roughly 0.52\u20130.55, while final crystal purity was usually 0.98\u20131.00. I interpret this as selective partitioning during crystallization: much of the reaction impurity stayed in the mother liquor even though reaction selectivity was only moderate. Thus high crystal purity did not imply a highly selective reaction.\n\nCrystal recovery is a stage-specific quantity,\n\nR_c = n(target recovered in crystals, excluding seed) / n(target present before separation).\n\nIt is not overall yield from charged reagent. If the reported reaction yield and crystallization recovery are treated as sequential fractions, an approximate overall isolated-target fraction is Y_isolated \u2248 Y_reaction \u00d7 R_c. For batch 8 this is approximately 0.5380 \u00d7 0.5002 \u2248 0.269. This product is useful for process interpretation but was not the optimization target.\n\nThe particle constraint is number-weighted,\n\nF_20 = N(d < 20 micrometres) / N_total,\n\nand therefore responds strongly to the creation of many small secondary crystals even when their mass is modest. The reported normalized size is min(d50/250 micrometres, 1), so batch 8's value 0.1109 corresponds approximately to a number-weighted d50 of 27.7 micrometres.\n\nConcentration and supersaturation\n\nReducing solvent volume increased supersaturation and generally raised recovery, but excessive concentration produced too many fines. Batch 1, with 0.080 L solvent, recovered 0.4294 with fines 0.3263. Batch 3, with only 0.040 L and a relatively short two-stage cooling history, raised recovery to 0.4543 but produced fines of 0.6727 and failed the particle constraint. Batch 4 at 0.060 L achieved recovery 0.4557 with fines 0.3895. Batch 5 at 0.050 L achieved recovery 0.4618 with fines 0.4381. These observations motivated operation near 0.050 L rather than maximizing concentration.\n\nI interpret this as a supersaturation competition: lowering solvent volume increases the crystallization driving force and recoverable fraction, but beyond a threshold nucleation outpaces growth, sharply increasing the number fraction below 20 micrometres. The exact threshold is history-dependent rather than a single concentration limit.\n\nCooling endpoint and staging\n\nAdding a final slow cooling stage from 275 to 260 K was the most successful revision. Batch 5 stopped at 275 K and recovered 0.4618; batch 8 used the same main recipe plus 14,400 s at 260 K and recovered 0.5002 while retaining fines of 0.4144. Cooling further to 250 K in batch 9 did not improve the observed recovery: it was 0.4983, with fines 0.4290 and markedly lower normalized size, 0.0618. Thus the extra 250 K stage apparently added little recoverable product and may have promoted small-particle formation or otherwise worsened size quality.\n\nThe useful qualitative relationship is\n\ndC*/dT > 0, and crystallization driving force \u0394C = C \u2212 C*(T),\n\nwhere C*(T) is target solubility. Lowering T increases \u0394C and equilibrium recovery, but nucleation typically rises nonlinearly with supersaturation. Staged cooling limits instantaneous \u0394C and gives existing crystals time to grow. Batch 8 appears to balance this kinetic penalty against the thermodynamic benefit of cooling.\n\nSeed effects\n\nAt the batch-8 conditions, 0.030 g seed performed better in observed recovery than the tested neighboring charges. Batch 11 used 0.020 g and gave recovery 0.4832, purity 0.9993, and fines 0.4224. Batch 12 used 0.040 g and gave recovery 0.4862, purity 1.000, and fines 0.4280. Batch 8 used 0.030 g and gave recovery 0.5002 with fines 0.4144. This suggests an intermediate seed charge supplied enough growth surface to manage supersaturation without excessively increasing seed-associated particle count. Nevertheless, the recovery differences are close to assay uncertainty, so a sharp mechanistic optimum at exactly 0.030 g is not established.\n\nProcess-history dependence\n\nBatch 7 provides the clearest evidence that final temperature and composition alone do not determine particle quality. After its initial staged cooling, particle imaging reported fines 0.5819. The slurry was reheated to 305 K, given an additional 0.020 g seed, and slowly recooled through 295, 285, and 275 K. A second particle measurement still reported fines 0.5820; normalized size decreased from 0.0745 to 0.0394 in those in-process measurements. Its final assay remained infeasible, with recovery 0.4756 and fines 0.5672. Partial reheating and reseeding therefore did not erase the initial nucleation history and may have generated or preserved additional small particles.\n\nBatch 1 also illustrates thermal-history effects: after cooling to 275 K, an uncooled wait allowed the slurry to warm toward ambient temperature, requiring recooling before filtration. It nevertheless produced low fines (0.3263), but only 0.4294 recovery. This is consistent with partial dissolution or ripening reducing particle number while sacrificing recovered product, although that mechanism was not directly measured.\n\nRevisions during the campaign\n\nThe study began with a dilute 0.080 L process. It then tested a lower-temperature/C0 reaction and smaller seed charge in batch 2, followed by aggressive concentration in batch 3. Batch 3's fines failure led to intermediate solvent volumes and more gradual cooling in batches 4 and 5. Batch 6 deliberately pushed concentration and seed charge; it reached recovery 0.4819 but failed with fines 0.5516. Batch 7 tested whether reheating and reseeding could rescue such a fine-rich history, but it did not. Batch 8 therefore returned to the feasible 0.050 L/0.030 g regime and extended cooling only to 260 K, yielding the best constrained result. Batches 9\u201312 tested colder cooling, slightly lower solvent volume, and neighboring seed charges; none surpassed batch 8.\n\nUncertainty and unresolved tradeoff\n\nFinal-assay nominal standard deviations were approximately 0.010 for crystal recovery, 0.010 for purity, 0.018 for fines fraction, and 0.025 for normalized size. Consequently, small differences among batches 8\u201312 should not be overinterpreted. Batch 8's purity and fines have comfortable margins relative to 0.80 and 0.50, but its recovery advantage over batches 9 and 10 is comparable to assay noise. No exact replicate series was performed.\n\nThe main unresolved tradeoff is that higher supersaturation can raise recovery but risks crossing the fines constraint. Batch 6 reached the highest raw observed recovery, 0.4819 at that stage of development, but failed on fines; later batch 8 achieved both higher recovery and feasible fines through a better concentration/cooling combination. More aggressive concentration may still yield recovery above 0.5002 if nucleation can be controlled, but the attempted slow cooling, larger seed charge, and reheat/reseed rescue did not demonstrate such control. Alternative solvents, mixed-solvent strategies, deliberate ripening holds under temperature control, and a factorial catalyst/temperature study were not tested and remain hypotheses rather than supported recommendations."
  },
  "failure": null,
  "elapsed_s": 61.828000000008615,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 1233280,
    "input_tokens": 1466790,
    "output_tokens": 9371,
    "reasoning_output_tokens": 3416
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
          "upper80": 0.39
        },
        "crystal_purity": {
          "estimate": 0.96,
          "lower80": 0.89,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.15,
          "lower80": 0.08,
          "upper80": 0.24
        },
        "crystal_yield": {
          "estimate": 0.38,
          "lower80": 0.24,
          "upper80": 0.53
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q01"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.38,
          "lower80": 0.22,
          "upper80": 0.56
        },
        "crystal_purity": {
          "estimate": 0.91,
          "lower80": 0.8,
          "upper80": 0.98
        },
        "crystal_size": {
          "estimate": 0.11,
          "lower80": 0.05,
          "upper80": 0.19
        },
        "crystal_yield": {
          "estimate": 0.29,
          "lower80": 0.16,
          "upper80": 0.44
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q02"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.66,
          "lower80": 0.46,
          "upper80": 0.83
        },
        "crystal_purity": {
          "estimate": 0.86,
          "lower80": 0.72,
          "upper80": 0.96
        },
        "crystal_size": {
          "estimate": 0.055,
          "lower80": 0.015,
          "upper80": 0.13
        },
        "crystal_yield": {
          "estimate": 0.27,
          "lower80": 0.12,
          "upper80": 0.43
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q03"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.4,
          "lower80": 0.24,
          "upper80": 0.58
        },
        "crystal_purity": {
          "estimate": 0.89,
          "lower80": 0.77,
          "upper80": 0.97
        },
        "crystal_size": {
          "estimate": 0.11,
          "lower80": 0.05,
          "upper80": 0.19
        },
        "crystal_yield": {
          "estimate": 0.31,
          "lower80": 0.16,
          "upper80": 0.47
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q04"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.38,
          "lower80": 0.23,
          "upper80": 0.55
        },
        "crystal_purity": {
          "estimate": 0.9,
          "lower80": 0.78,
          "upper80": 0.98
        },
        "crystal_size": {
          "estimate": 0.115,
          "lower80": 0.055,
          "upper80": 0.2
        },
        "crystal_yield": {
          "estimate": 0.31,
          "lower80": 0.16,
          "upper80": 0.47
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q05"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.59,
          "lower80": 0.4,
          "upper80": 0.76
        },
        "crystal_purity": {
          "estimate": 0.87,
          "lower80": 0.73,
          "upper80": 0.96
        },
        "crystal_size": {
          "estimate": 0.065,
          "lower80": 0.02,
          "upper80": 0.14
        },
        "crystal_yield": {
          "estimate": 0.33,
          "lower80": 0.18,
          "upper80": 0.49
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q06"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.37,
          "lower80": 0.22,
          "upper80": 0.54
        },
        "crystal_purity": {
          "estimate": 0.9,
          "lower80": 0.78,
          "upper80": 0.98
        },
        "crystal_size": {
          "estimate": 0.12,
          "lower80": 0.06,
          "upper80": 0.21
        },
        "crystal_yield": {
          "estimate": 0.33,
          "lower80": 0.18,
          "upper80": 0.49
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q07"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.55,
          "lower80": 0.35,
          "upper80": 0.73
        },
        "crystal_purity": {
          "estimate": 0.88,
          "lower80": 0.74,
          "upper80": 0.97
        },
        "crystal_size": {
          "estimate": 0.075,
          "lower80": 0.025,
          "upper80": 0.16
        },
        "crystal_yield": {
          "estimate": 0.24,
          "lower80": 0.1,
          "upper80": 0.41
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q08"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.7,
          "lower80": 0.48,
          "upper80": 0.87
        },
        "crystal_purity": {
          "estimate": 0.83,
          "lower80": 0.63,
          "upper80": 0.95
        },
        "crystal_size": {
          "estimate": 0.035,
          "lower80": 0.005,
          "upper80": 0.1
        },
        "crystal_yield": {
          "estimate": 0.025,
          "lower80": 0.0,
          "upper80": 0.08
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q09"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.47,
          "lower80": 0.29,
          "upper80": 0.66
        },
        "crystal_purity": {
          "estimate": 0.87,
          "lower80": 0.71,
          "upper80": 0.96
        },
        "crystal_size": {
          "estimate": 0.065,
          "lower80": 0.02,
          "upper80": 0.14
        },
        "crystal_yield": {
          "estimate": 0.13,
          "lower80": 0.04,
          "upper80": 0.27
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q10"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.34,
          "lower80": 0.19,
          "upper80": 0.51
        },
        "crystal_purity": {
          "estimate": 0.9,
          "lower80": 0.78,
          "upper80": 0.98
        },
        "crystal_size": {
          "estimate": 0.13,
          "lower80": 0.065,
          "upper80": 0.22
        },
        "crystal_yield": {
          "estimate": 0.32,
          "lower80": 0.17,
          "upper80": 0.48
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q11"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.55,
          "lower80": 0.36,
          "upper80": 0.73
        },
        "crystal_purity": {
          "estimate": 0.87,
          "lower80": 0.73,
          "upper80": 0.96
        },
        "crystal_size": {
          "estimate": 0.08,
          "lower80": 0.03,
          "upper80": 0.16
        },
        "crystal_yield": {
          "estimate": 0.39,
          "lower80": 0.23,
          "upper80": 0.55
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q12"
      }
    ],
    "rationale": "All recipes contain seed crystals, so particles are expected even when little new product deposits. Q01 versus Q02 reflects the material prior: S1 has lower solubility, lower nucleation tendency, faster growth and less impurity occlusion than S3, so I predict higher recovery, purity and size with fewer fines for Q01. Q03 versus Q04 isolates seed charge in nucleation-prone S0; very low seeding is expected to permit secondary nucleation and a fine-rich distribution, while 0.045 g seed provides growth surface and restores point-estimate feasibility. Q05 versus Q06 contrasts gradual cooling with a temperature crash: their eventual recoveries may be similar, but the crash should create more fines and impurity occlusion despite the long hold. Q07 versus Q08 tests thermal-history erasure; the 315 K reheat followed by rapid recooling is predicted to dissolve some deposited product and then regenerate fines, consistent with the unsuccessful reheat/reseed rescue observed in batch 7. Q09 versus Q10 shows residence-time dependence at 292 K: 60 seconds should deposit almost no seed-excluded product, whereas the additional two-hour hold increases recovery and allows growth enough for marginal point-estimate feasibility. Q11 versus Q12 doubles concentration; greater supersaturation should increase recovery but also secondary nucleation and occlusion, producing a recovery/fines tradeoff. Uncertainty is broad because the campaign directly tested only S2 and different concentration, temperature and reaction regimes; several feasibility calls, especially Q02, Q04, Q05, Q07, Q10 and Q11, remain close enough to the fines or purity limits that their intervals cross a constraint."
  },
  "failure": null,
  "elapsed_s": 79.57800000000861,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 1233280,
    "input_tokens": 1592890,
    "output_tokens": 13517,
    "reasoning_output_tokens": 5795
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
    "report": "1. Status of the main claims\n\nSupported by direct observations:\n\n- A feasible recovery\u2013fines operating window existed near the batch-8 conditions. Batch 8 directly delivered crystal yield 0.5002, purity 0.9862 and fines 0.4144. Batches 4 and 5 also met both quality limits, with recoveries 0.4557 and 0.4618.\n- Excessive concentration was associated with a fines penalty. Batch 3 used 0.040 L S2 and produced higher recovery than batch 1, but fines rose to 0.6727. Batch 6 at 0.045 L reached recovery 0.4819 but fines 0.5516. This supports a recovery\u2013fines tradeoff, although concentration and cooling history were not varied independently in those comparisons.\n- Extending the batch-5 cooling sequence to 260 K was beneficial in the observed data. Batch 5 stopped at 275 K and gave recovery 0.4618 with fines 0.4381; otherwise closely related batch 8 added a 260 K stage and gave recovery 0.5002 with fines 0.4144.\n- Cooling further was not automatically beneficial. Batch 9 added a 250 K stage to the batch-8 sequence but gave recovery 0.4983 rather than an increase, and normalized size fell from 0.1109 to 0.0618.\n- Reheating did not rescue a fine-rich history. In batch 7, particle measurements gave fines 0.5819 before reheating and 0.5820 after reheating, reseeding and recooling; the final assay remained infeasible at 0.5672 fines.\n- Moderate reaction selectivity coexisted with high crystal purity. For example, batch 8 had reaction selectivity 0.5463 but crystal purity 0.9862. Similar behavior occurred in batches 1, 5 and 12. The coexistence is directly observed; selective rejection of impurity into the mother liquor is the interpretation.\n\nSupported only weakly or with important confounding:\n\n- An intermediate seed charge appeared best. Under the otherwise matched batch-8 process, 0.030 g seed gave recovery 0.5002, versus 0.4832 for 0.020 g in batch 11 and 0.4862 for 0.040 g in batch 12. The ordering is observationally supported, but the differences are comparable to the approximately 0.01 recovery uncertainty and lack replication.\n- Catalyst-C1 appeared somewhat better than C0 for reaction yield, but batch 1 versus batch 2 also changed temperature, seed charge and crystallization history. Thus the catalyst attribution is not established.\n- The concentration\u2013fines explanation is consistent with batches 3\u20136, but differing cooling schedules prevent a clean causal estimate of concentration alone.\n\nContradicted or revised:\n\n- A simple \u201clower final temperature always raises recovery\u201d account is contradicted by batch 9 versus batch 8.\n- A monotonic benefit from increasing seed mass is contradicted by batches 8, 11 and 12; 0.040 g did not outperform 0.030 g.\n- The proposed possibility that reheating could dissolve fines and reset the particle population was contradicted under the batch-7 rework conditions.\n- Maximizing supersaturation without regard to particle history was contradicted as a viable constrained strategy by batches 3 and 6, which failed the fines limit.\n\nStill untested:\n\n- No experiment compared S2 with S0, S1 or S3. Claims that S2\u2019s nominal low solubility, high growth tendency and low impurity occlusion caused its performance remain dossier-based interpretations.\n- Catalyst identity was never isolated from temperature and downstream changes.\n- The inferred mother-liquor impurity rejection mechanism was not verified by separate solid and liquor assays.\n- The approximate overall relation Y_isolated \u2248 Y_reaction \u00d7 R_crystallization was useful bookkeeping, not an independently validated mass balance.\n- Whether the apparent 0.030 g seed optimum is real, and whether recovery above 0.50 can be achieved while maintaining fines below 0.50, remain unresolved.\n\n2. One additional experiment\n\nI would repeat the complete batch-8 recipe with only one change: replace solvent-S2 with solvent-S1. I would keep charge concentration, C1 amount, reaction conditions, 0.030 g seed, all five cooling stages, filtration and assay identical. A nondestructive particle-size measurement immediately before filtration could be added without changing the thermal history.\n\nThis experiment would distinguish three explanations:\n\n- If S2\u2019s lower nominal solubility is the main cause of recovery, S1 should give lower recovery than batch 8, while possibly retaining high purity and acceptable fines.\n- If growth and low impurity occlusion dominate, S1 could approach batch-8 recovery while producing comparable or better purity and particle quality.\n- If hidden world-specific solvent residuals or misindexing dominate the nominal dossier, S1 could behave anomalously\u2014for example, matching or exceeding S2 recovery or producing unexpectedly poor purity or fines.\n\nA result around recovery 0.35\u20130.45 with high purity and low fines would support the solubility-dominant account. Recovery near 0.50 with improved CSD would favor the growth/occlusion account. A large reversal, especially worse purity or much higher fines than nominal properties suggest, would undermine reliance on the material dossier.\n\n3. Least-used observation and least-reliable prediction\n\nThe observation used least effectively was the degradation contrast in the early reaction data. Batch 2 had degradation warning 0.0741, much lower than batch 1 at 0.1626 and batch 8 at 0.1567. I focused on crystallization recovery and treated batch 1 versus batch 2 mainly as a confounded catalyst comparison. The low degradation signal could instead indicate a meaningful lower-temperature reaction advantage, even though batch 2 had lower reaction yield and selectivity. A dedicated temperature study might therefore improve overall isolated product production without materially changing the stage-specific recovery objective.\n\nThe least reliable held-out prediction is Q09. It combines an untested solvent, S0, with only 60 seconds of cooling at 292 K and a seed-dominated solid population. Nothing in the campaign directly sampled such a short transient: campaign crystallizations lasted hours, generally used S2, and allowed substantial target deposition. Although particles should be present because seed was explicitly added, the predicted seed-excluded yield, fines fraction and purity depend sensitively on unobserved cooling dynamics, initial seed-size distribution and how little product must deposit before the recovered-solid metrics stabilize. Q01\u2013Q02 also carry major solvent-extrapolation uncertainty, but Q09 adds the largest kinetic extrapolation."
  },
  "failure": null,
  "elapsed_s": 57.65600000001723,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 1233280,
    "input_tokens": 1723056,
    "output_tokens": 16220,
    "reasoning_output_tokens": 7033
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
    "selection_rationale": "Highest observed seed-excluded crystal recovery among completed batches meeting both constraints: crystal_yield 0.5002, crystal_purity 0.9862, and fines fraction 0.4144."
  },
  "recommendation_recipe": {
    "actions": [
      {
        "operation": "add_solvent",
        "solvent": 2,
        "volume_L": 0.05
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
        "operation": "seed_crystals",
        "seed_mass_g": 0.03
      },
      {
        "duration_s": 10000,
        "operation": "cool_crystallize",
        "target_temperature_K": 315
      },
      {
        "duration_s": 10000,
        "operation": "cool_crystallize",
        "target_temperature_K": 300
      },
      {
        "duration_s": 10000,
        "operation": "cool_crystallize",
        "target_temperature_K": 285
      },
      {
        "duration_s": 10000,
        "operation": "cool_crystallize",
        "target_temperature_K": 275
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
    "excluded_rejected_attempts": [],
    "lifecycle_index": 8,
    "source_attempts": 13
  },
  "prediction_evaluation": {
    "contrasts": [
      {
        "absolute_delta_error": 0.01705937656225756,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_yield",
        "predicted_delta": -0.09000000000000002,
        "resolved": true,
        "true_delta": -0.07294062343774246
      },
      {
        "absolute_delta_error": 0.048746122547241644,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_purity",
        "predicted_delta": -0.04999999999999993,
        "resolved": false,
        "true_delta": -0.0012538774527582897
      },
      {
        "absolute_delta_error": 0.05565330192830198,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_size",
        "predicted_delta": -0.039999999999999994,
        "resolved": true,
        "true_delta": 0.015653301928301985
      },
      {
        "absolute_delta_error": 0.5832152850558221,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.14,
        "resolved": true,
        "true_delta": -0.44321528505582214
      },
      {
        "absolute_delta_error": 0.04004833748776476,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_yield",
        "predicted_delta": 0.03999999999999998,
        "resolved": false,
        "true_delta": -4.8337487764782416e-05
      },
      {
        "absolute_delta_error": 0.021867529554736698,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_purity",
        "predicted_delta": 0.030000000000000027,
        "resolved": false,
        "true_delta": 0.008132470445263329
      },
      {
        "absolute_delta_error": 0.05457750439259928,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_size",
        "predicted_delta": 0.055,
        "resolved": false,
        "true_delta": 0.0004224956074007219
      },
      {
        "absolute_delta_error": 0.2351737603270197,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.26,
        "resolved": false,
        "true_delta": -0.02482623967298031
      },
      {
        "absolute_delta_error": 0.019767182469520972,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_yield",
        "predicted_delta": 0.020000000000000018,
        "resolved": false,
        "true_delta": 0.00023281753047904585
      },
      {
        "absolute_delta_error": 0.025209363860740797,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.030000000000000027,
        "resolved": false,
        "true_delta": -0.00479063613925923
      },
      {
        "absolute_delta_error": 0.010794590636423095,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_size",
        "predicted_delta": -0.05,
        "resolved": true,
        "true_delta": -0.03920540936357691
      },
      {
        "absolute_delta_error": 0.4663771602380363,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.20999999999999996,
        "resolved": true,
        "true_delta": 0.6763771602380363
      },
      {
        "absolute_delta_error": 0.13156172818020112,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_yield",
        "predicted_delta": -0.09000000000000002,
        "resolved": true,
        "true_delta": 0.041561728180201096
      },
      {
        "absolute_delta_error": 0.010735832934603007,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.020000000000000018,
        "resolved": false,
        "true_delta": -0.009264167065397011
      },
      {
        "absolute_delta_error": 0.014556267883141606,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_size",
        "predicted_delta": -0.045,
        "resolved": true,
        "true_delta": -0.030443732116858392
      },
      {
        "absolute_delta_error": 0.5161786076870266,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.18000000000000005,
        "resolved": true,
        "true_delta": 0.6961786076870267
      },
      {
        "absolute_delta_error": 0.04572767781178036,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_yield",
        "predicted_delta": 0.10500000000000001,
        "resolved": true,
        "true_delta": 0.15072767781178037
      },
      {
        "absolute_delta_error": 0.05407302371933764,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_purity",
        "predicted_delta": 0.040000000000000036,
        "resolved": true,
        "true_delta": -0.014073023719337607
      },
      {
        "absolute_delta_error": 0.015124201609462394,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_size",
        "predicted_delta": 0.03,
        "resolved": true,
        "true_delta": 0.014875798390537605
      },
      {
        "absolute_delta_error": 0.25026443684698085,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.22999999999999998,
        "resolved": false,
        "true_delta": 0.02026443684698087
      },
      {
        "absolute_delta_error": 0.03925974627058054,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_yield",
        "predicted_delta": 0.07,
        "resolved": true,
        "true_delta": 0.030740253729419464
      },
      {
        "absolute_delta_error": 0.023976332586183147,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_purity",
        "predicted_delta": -0.030000000000000027,
        "resolved": false,
        "true_delta": -0.00602366741381688
      },
      {
        "absolute_delta_error": 0.02243629337321281,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_size",
        "predicted_delta": -0.05,
        "resolved": true,
        "true_delta": -0.027563706626787192
      },
      {
        "absolute_delta_error": 0.4785789828624289,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.21000000000000002,
        "resolved": true,
        "true_delta": 0.6885789828624289
      }
    ],
    "failures": [],
    "metrics": {
      "crystal_fines_fraction": {
        "coverage80": 0.4166666666666667,
        "interval_score80": 1.8030903747728189,
        "interval_width": 0.3458333333333334,
        "mae": 0.2665231404124548,
        "n": 12,
        "planned": 12
      },
      "crystal_purity": {
        "coverage80": 0.08333333333333333,
        "interval_score80": 0.36568912967971184,
        "interval_width": 0.21583333333333332,
        "mae": 0.09830845573240676,
        "n": 12,
        "planned": 12
      },
      "crystal_size": {
        "coverage80": 0.9166666666666666,
        "interval_score80": 0.13921078345406135,
        "interval_width": 0.13375,
        "mae": 0.029350095803423706,
        "n": 12,
        "planned": 12
      },
      "crystal_yield": {
        "coverage80": 1.0,
        "interval_score80": 0.2808333333333333,
        "interval_width": 0.2808333333333333,
        "mae": 0.04601898223189693,
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
    "tie_correct": 0,
    "tie_n": 10,
    "valid": true
  },
  "public_baselines": {
    "available": true,
    "mae": {
      "public_mean": {
        "crystal_fines_fraction": 0.31402314041245477,
        "crystal_purity": 0.007625750492410007,
        "crystal_size": 0.016575762692193362,
        "crystal_yield": 0.21602263792265952
      },
      "public_nearest_neighbor": {
        "crystal_fines_fraction": 0.28492319170821206,
        "crystal_purity": 0.004556697983910914,
        "crystal_size": 0.01674596490271013,
        "crystal_yield": 0.22023805969863633
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
        "cached_input": 1233280,
        "input": 1352278,
        "output": 6319,
        "stage": "source",
        "uncached_input": 118998
      },
      {
        "cached_input": 0,
        "input": 114512,
        "output": 3052,
        "stage": "K1",
        "uncached_input": 114512
      },
      {
        "cached_input": 0,
        "input": 126100,
        "output": 4146,
        "stage": "Q",
        "uncached_input": 126100
      },
      {
        "cached_input": 0,
        "input": 130166,
        "output": 2703,
        "stage": "K2",
        "uncached_input": 130166
      }
    ],
    "total": {
      "cached_input": 1233280,
      "input": 1723056,
      "input_plus_output": 1739276,
      "output": 16220,
      "uncached_input": 489776
    },
    "valid": true
  },
  "elapsed_s": 488.00000000001455
}
```
