# C-W03-B24-E-Aligned

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
      "target_temperature_K": 350
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
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
  "end_step": 11,
  "lifecycle_index": 1,
  "metrics": {
    "byproduct_signal": 0.321694016456604,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7047088742256165,
    "crystal_fines_fraction": 0.4532296657562256,
    "crystal_purity": 0.986866295337677,
    "crystal_size": 0.07271242141723633,
    "crystal_yield": 0.44093990325927734,
    "degradation_warning": 0.14845706522464752,
    "safety_risk": 0.18081331253051758,
    "score": 0.48642319440841675,
    "selectivity": 0.5333123207092285,
    "virtual_spectrum_summary": 0.2437373846769333,
    "yield": 0.5311498045921326
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
      "target_temperature_K": 330
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
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
  "end_step": 21,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.3007863759994507,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5737084150314331,
    "crystal_fines_fraction": 0.7447625994682312,
    "crystal_purity": 0.9805697798728943,
    "crystal_size": 0.09606654196977615,
    "crystal_yield": 0.40586140751838684,
    "degradation_warning": 0.05605404078960419,
    "safety_risk": 0.13266214728355408,
    "score": 0.41768497228622437,
    "selectivity": 0.4932042062282562,
    "virtual_spectrum_summary": 0.19065682590007782,
    "yield": 0.48159778118133545
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
      "target_temperature_K": 330
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
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
  "end_step": 31,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.31514930725097656,
    "conversion": 0.9982950091362,
    "cost": 1.0,
    "crystal_csd_quality": 0.5894169211387634,
    "crystal_fines_fraction": 0.7173374891281128,
    "crystal_purity": 0.9890393614768982,
    "crystal_size": 0.06132034212350845,
    "crystal_yield": 0.41496261954307556,
    "degradation_warning": 0.10652072727680206,
    "safety_risk": 0.1570899337530136,
    "score": 0.42197808623313904,
    "selectivity": 0.48331156373023987,
    "virtual_spectrum_summary": 0.22126644849777222,
    "yield": 0.48241323232650757
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
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
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
  "end_step": 41,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.3068101704120636,
    "conversion": 0.9889938831329346,
    "cost": 1.0,
    "crystal_csd_quality": 0.6514327526092529,
    "crystal_fines_fraction": 0.5973577499389648,
    "crystal_purity": 1.0,
    "crystal_size": 0.06952633708715439,
    "crystal_yield": 0.4578215479850769,
    "degradation_warning": 0.0944875180721283,
    "safety_risk": 0.17874380946159363,
    "score": 0.4627741873264313,
    "selectivity": 0.5144848823547363,
    "virtual_spectrum_summary": 0.2112649828195572,
    "yield": 0.5008538961410522
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
      "target_temperature_K": 330
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
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
  "end_step": 51,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.3807065486907959,
    "conversion": 0.9963365197181702,
    "cost": 1.0,
    "crystal_csd_quality": 0.5663659572601318,
    "crystal_fines_fraction": 0.7353423833847046,
    "crystal_purity": 0.9677920341491699,
    "crystal_size": 0.04717081040143967,
    "crystal_yield": 0.3361581861972809,
    "degradation_warning": 0.1109904870390892,
    "safety_risk": 0.17690616846084595,
    "score": 0.3756176233291626,
    "selectivity": 0.41589897871017456,
    "virtual_spectrum_summary": 0.2593343257904053,
    "yield": 0.4097454845905304
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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
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
  "end_step": 61,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.3193899989128113,
    "conversion": 0.9924196004867554,
    "cost": 1.0,
    "crystal_csd_quality": 0.6404561996459961,
    "crystal_fines_fraction": 0.5929272174835205,
    "crystal_purity": 1.0,
    "crystal_size": 0.042757727205753326,
    "crystal_yield": 0.44010743498802185,
    "degradation_warning": 0.10916458815336227,
    "safety_risk": 0.17769959568977356,
    "score": 0.45415499806404114,
    "selectivity": 0.5046120285987854,
    "virtual_spectrum_summary": 0.22478856146335602,
    "yield": 0.5064905881881714
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
      "catalyst": 2,
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
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
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
  "end_step": 71,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.35568079352378845,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7048518061637878,
    "crystal_fines_fraction": 0.42840972542762756,
    "crystal_purity": 0.9804322123527527,
    "crystal_size": 0.09099883586168289,
    "crystal_yield": 0.33772099018096924,
    "degradation_warning": 0.07350511848926544,
    "safety_risk": 0.16379475593566895,
    "score": 0.4383295476436615,
    "selectivity": 0.37334200739860535,
    "virtual_spectrum_summary": 0.22870174050331116,
    "yield": 0.399895042181015
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
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
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
  "end_step": 81,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.3354988396167755,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6777040958404541,
    "crystal_fines_fraction": 0.5787010788917542,
    "crystal_purity": 0.9798785448074341,
    "crystal_size": 0.09922819584608078,
    "crystal_yield": 0.442412406206131,
    "degradation_warning": 0.16246400773525238,
    "safety_risk": 0.176936537027359,
    "score": 0.4648524522781372,
    "selectivity": 0.5081510543823242,
    "virtual_spectrum_summary": 0.25763314962387085,
    "yield": 0.4998336136341095
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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
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
  "end_step": 91,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.3171783685684204,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6588808298110962,
    "crystal_fines_fraction": 0.5781669616699219,
    "crystal_purity": 0.9820166826248169,
    "crystal_size": 0.049085456877946854,
    "crystal_yield": 0.4492303431034088,
    "degradation_warning": 0.10884255170822144,
    "safety_risk": 0.17806898057460785,
    "score": 0.458379864692688,
    "selectivity": 0.4945114552974701,
    "virtual_spectrum_summary": 0.22342725098133087,
    "yield": 0.5081861019134521
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
      "target_temperature_K": 330
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
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
  "end_step": 101,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.3100554943084717,
    "conversion": 0.9858216047286987,
    "cost": 1.0,
    "crystal_csd_quality": 0.6271814703941345,
    "crystal_fines_fraction": 0.5856642127037048,
    "crystal_purity": 0.9778696894645691,
    "crystal_size": 0.06225142255425453,
    "crystal_yield": 0.43304693698883057,
    "degradation_warning": 0.12024889886379242,
    "safety_risk": 0.17716576159000397,
    "score": 0.4489176273345947,
    "selectivity": 0.505592405796051,
    "virtual_spectrum_summary": 0.22464251518249512,
    "yield": 0.5145178437232971
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
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
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
  "end_step": 111,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.318570077419281,
    "conversion": 0.9990177750587463,
    "cost": 1.0,
    "crystal_csd_quality": 0.636588990688324,
    "crystal_fines_fraction": 0.5637628436088562,
    "crystal_purity": 0.9933608770370483,
    "crystal_size": 0.06767202168703079,
    "crystal_yield": 0.4332120716571808,
    "degradation_warning": 0.09726892411708832,
    "safety_risk": 0.17813408374786377,
    "score": 0.45971623063087463,
    "selectivity": 0.5393421649932861,
    "virtual_spectrum_summary": 0.21898455917835236,
    "yield": 0.5198509097099304
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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.025
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
  "end_step": 121,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.3025716245174408,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6545023918151855,
    "crystal_fines_fraction": 0.5754148960113525,
    "crystal_purity": 0.9942939281463623,
    "crystal_size": 0.08948115259408951,
    "crystal_yield": 0.4361620545387268,
    "degradation_warning": 0.11902733892202377,
    "safety_risk": 0.17784073948860168,
    "score": 0.46254003047943115,
    "selectivity": 0.5083656907081604,
    "virtual_spectrum_summary": 0.21997669339179993,
    "yield": 0.5134063959121704
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
      "target_temperature_K": 330
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
  "end_step": 131,
  "lifecycle_index": 13,
  "metrics": {
    "byproduct_signal": 0.30608806014060974,
    "conversion": 0.9972143769264221,
    "cost": 1.0,
    "crystal_csd_quality": 0.6775112748146057,
    "crystal_fines_fraction": 0.5781410336494446,
    "crystal_purity": 0.9807186126708984,
    "crystal_size": 0.06736846268177032,
    "crystal_yield": 0.42444974184036255,
    "degradation_warning": 0.11065581440925598,
    "safety_risk": 0.17756445705890656,
    "score": 0.457925021648407,
    "selectivity": 0.5115361213684082,
    "virtual_spectrum_summary": 0.2181435376405716,
    "yield": 0.5035222768783569
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
      "target_temperature_K": 330
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
  "end_step": 140,
  "lifecycle_index": 14,
  "metrics": {
    "byproduct_signal": 0.3204011023044586,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6819157004356384,
    "crystal_fines_fraction": 0.5951205492019653,
    "crystal_purity": 0.9640650749206543,
    "crystal_size": 0.1029263585805893,
    "crystal_yield": 0.4293786883354187,
    "degradation_warning": 0.1155814379453659,
    "safety_risk": 0.17755305767059326,
    "score": 0.45754802227020264,
    "selectivity": 0.5045187473297119,
    "virtual_spectrum_summary": 0.2282322496175766,
    "yield": 0.4983299970626831
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
      "target_temperature_K": 330
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
  "lifecycle_index": 15,
  "metrics": {
    "byproduct_signal": 0.3138076066970825,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6300348043441772,
    "crystal_fines_fraction": 0.585459291934967,
    "crystal_purity": 0.9877052903175354,
    "crystal_size": 0.0795699954032898,
    "crystal_yield": 0.44145986437797546,
    "degradation_warning": 0.1084289476275444,
    "safety_risk": 0.17885801196098328,
    "score": 0.4583401083946228,
    "selectivity": 0.5233494639396667,
    "virtual_spectrum_summary": 0.22138720750808716,
    "yield": 0.5278826355934143
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
      "target_temperature_K": 330
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
    },
    {
      "duration_s": 1800,
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
  "end_step": 160,
  "lifecycle_index": 16,
  "metrics": {
    "byproduct_signal": 0.3068864345550537,
    "conversion": 0.988551139831543,
    "cost": 1.0,
    "crystal_csd_quality": 0.48927995562553406,
    "crystal_fines_fraction": 0.8194432258605957,
    "crystal_purity": 0.9763738512992859,
    "crystal_size": 0.06879878044128418,
    "crystal_yield": 0.42586931586265564,
    "degradation_warning": 0.11975320428609848,
    "safety_risk": 0.17767934501171112,
    "score": 0.39490827918052673,
    "selectivity": 0.5038489103317261,
    "virtual_spectrum_summary": 0.22267648577690125,
    "yield": 0.5022021532058716
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
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
    },
    {
      "duration_s": 3600,
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
  "end_step": 170,
  "lifecycle_index": 17,
  "metrics": {
    "byproduct_signal": 0.32208743691444397,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5715753436088562,
    "crystal_fines_fraction": 0.7023622989654541,
    "crystal_purity": 0.9985378384590149,
    "crystal_size": 0.06141684576869011,
    "crystal_yield": 0.43877893686294556,
    "degradation_warning": 0.11447189003229141,
    "safety_risk": 0.17767123878002167,
    "score": 0.4311719536781311,
    "selectivity": 0.5007144808769226,
    "virtual_spectrum_summary": 0.2286604344844818,
    "yield": 0.510871410369873
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
      "target_temperature_K": 330
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
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
  "end_step": 180,
  "lifecycle_index": 18,
  "metrics": {
    "byproduct_signal": 0.2957274317741394,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6466853618621826,
    "crystal_fines_fraction": 0.6347230076789856,
    "crystal_purity": 0.9944716691970825,
    "crystal_size": 0.11598362028598785,
    "crystal_yield": 0.4280157685279846,
    "degradation_warning": 0.11032643169164658,
    "safety_risk": 0.17766782641410828,
    "score": 0.45630455017089844,
    "selectivity": 0.5059822797775269,
    "virtual_spectrum_summary": 0.2122969776391983,
    "yield": 0.5193879008293152
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
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
    },
    {
      "duration_s": 10000,
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
  "end_step": 190,
  "lifecycle_index": 19,
  "metrics": {
    "byproduct_signal": 0.31654831767082214,
    "conversion": 0.9909009337425232,
    "cost": 1.0,
    "crystal_csd_quality": 0.6000918745994568,
    "crystal_fines_fraction": 0.6922488212585449,
    "crystal_purity": 0.9732391238212585,
    "crystal_size": 0.05725984275341034,
    "crystal_yield": 0.43709349632263184,
    "degradation_warning": 0.1050272062420845,
    "safety_risk": 0.1776672601699829,
    "score": 0.43183064460754395,
    "selectivity": 0.5054585337638855,
    "virtual_spectrum_summary": 0.221363827586174,
    "yield": 0.5090439915657043
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
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 280
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
  "lifecycle_index": 20,
  "metrics": {
    "byproduct_signal": 0.31425032019615173,
    "conversion": 0.9934629797935486,
    "cost": 1.0,
    "crystal_csd_quality": 0.5379394888877869,
    "crystal_fines_fraction": 0.8085607886314392,
    "crystal_purity": 0.9918423295021057,
    "crystal_size": 0.06712043285369873,
    "crystal_yield": 0.40850770473480225,
    "degradation_warning": 0.10915110260248184,
    "safety_risk": 0.17655719816684723,
    "score": 0.4051492214202881,
    "selectivity": 0.5170591473579407,
    "virtual_spectrum_summary": 0.22195567190647125,
    "yield": 0.5007359981536865
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
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
    },
    {
      "duration_s": 3600,
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
  "end_step": 210,
  "lifecycle_index": 21,
  "metrics": {
    "byproduct_signal": 0.29135388135910034,
    "conversion": 0.9894062876701355,
    "cost": 1.0,
    "crystal_csd_quality": 0.6044248938560486,
    "crystal_fines_fraction": 0.7421517968177795,
    "crystal_purity": 0.9890128374099731,
    "crystal_size": 0.04724786430597305,
    "crystal_yield": 0.4487936794757843,
    "degradation_warning": 0.10700751096010208,
    "safety_risk": 0.17807331681251526,
    "score": 0.43351879715919495,
    "selectivity": 0.49924352765083313,
    "virtual_spectrum_summary": 0.2083980143070221,
    "yield": 0.518519401550293
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
      "seed_mass_g": 0.01
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
  "end_step": 220,
  "lifecycle_index": 22,
  "metrics": {
    "byproduct_signal": 0.32387760281562805,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6733756065368652,
    "crystal_fines_fraction": 0.4545900821685791,
    "crystal_purity": 1.0,
    "crystal_size": 0.0740814208984375,
    "crystal_yield": 0.45180395245552063,
    "degradation_warning": 0.14656007289886475,
    "safety_risk": 0.1808890849351883,
    "score": 0.48360568284988403,
    "selectivity": 0.5209394693374634,
    "virtual_spectrum_summary": 0.2440847009420395,
    "yield": 0.5222183465957642
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
      "seed_mass_g": 0.01
    },
    {
      "duration_s": 7200,
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
  "end_step": 232,
  "lifecycle_index": 23,
  "metrics": {
    "byproduct_signal": 0.33330950140953064,
    "conversion": 0.9950222373008728,
    "cost": 1.0,
    "crystal_csd_quality": 0.6622391939163208,
    "crystal_fines_fraction": 0.4758785367012024,
    "crystal_purity": 0.9973579049110413,
    "crystal_size": 0.09366197884082794,
    "crystal_yield": 0.4383915662765503,
    "degradation_warning": 0.14824499189853668,
    "safety_risk": 0.17988017201423645,
    "score": 0.47897741198539734,
    "selectivity": 0.5297542810440063,
    "virtual_spectrum_summary": 0.2500304579734802,
    "yield": 0.5315124988555908
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
      "seed_mass_g": 0.01
    },
    {
      "duration_s": 7200,
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
  "end_step": 241,
  "lifecycle_index": 24,
  "metrics": {
    "byproduct_signal": 0.32117849588394165,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6631397604942322,
    "crystal_fines_fraction": 0.48510414361953735,
    "crystal_purity": 1.0,
    "crystal_size": 0.0728042721748352,
    "crystal_yield": 0.4485001862049103,
    "degradation_warning": 0.14223599433898926,
    "safety_risk": 0.18130163848400116,
    "score": 0.48058006167411804,
    "selectivity": 0.531904935836792,
    "virtual_spectrum_summary": 0.2406543642282486,
    "yield": 0.5411547422409058
  },
  "ordinal": 24
}
```

## K1

```json
{
  "payload": {
    "report": "Mechanistic account\n\nThe recommended experiment remains batch 22: 0.040 mol reagent, 0.080 L solvent-S2, 0.005 mol catalyst-C1, heating toward 350 K for 3600 s at 500 rpm, addition of 0.010 g seed, cooling to 270 K over 7200 s, and filtration. Its final assay gave crystal recovery 0.4518, purity 1.000, and fines fraction 0.4546. Batch 1 used essentially the same thermal and crystallization conditions and also passed the specifications (recovery 0.4409, purity 0.9869, fines 0.4532), supporting\u2014but not fully establishing\u2014reproducibility.\n\nMaterial effects\n\nObserved: In the controlled solvent screen at 330 K followed by cooling to 250 K over 14400 s (batches 2\u20135), S2 was best overall. Batch 4 (S2) produced recovery 0.4578, purity 1.000, and fines 0.5974, compared with recoveries of 0.4059, 0.4150, and 0.3362 and fines of 0.7448, 0.7173, and 0.7353 for S0, S1, and S3, respectively. The S2 batch still failed the fines constraint under that particular history.\n\nInterpretation: The nominal dossier describes S2 as having relatively low solubility, strong crystal growth, low nucleation tendency, and low impurity occlusion. Its observed combination of higher recovery, fewer fines, and excellent purity is qualitatively consistent with those properties. Lower terminal solubility raises recovery, while a higher growth-to-nucleation ratio and reduced occlusion favor coarser, purer crystals. This agreement is evidence rather than proof because solvent identity was tested under only one common thermal profile and hidden solvent residuals may be important.\n\nObserved: Catalyst choice affected both reaction composition and crystallization. Under comparable S2/330 K/270 K conditions, C2 in batch 7 gave a passing fines value of 0.4284 but only 0.3377 recovery and reaction selectivity 0.3733. C0 and C3 in batches 6 and 8 gave about 0.440\u20130.442 recovery but fines of 0.593 and 0.579. C1 ultimately supported the best feasible recovery in batch 22.\n\nInterpretation: Catalyst effects are not confined to conversion. Different catalysts change target concentration and the impurity mixture entering crystallization; those impurities can promote or suppress nucleation, adsorb on growing faces, or remain in solution. C2 appears to create a lower-target or more nucleation-inhibiting liquor that gives fewer fines at the cost of recovery. This causal attribution is not uniquely identified because catalyst screens were not replicated and their reaction selectivities differed substantially.\n\nReaction\u2013crystallization coupling\n\nAcross the campaign, reaction conversion was generally near unity, so selectivity largely controlled reaction yield. A useful empirical relationship is\n\nY_reaction \u2248 X \u00d7 S_rxn,\n\nwhere X is conversion and S_rxn is reaction selectivity. For batch 22, X = 1.000, S_rxn = 0.5209, and measured reaction yield = 0.5222, consistent with this approximation.\n\nCrystal recovery has a different denominator:\n\nR_crystal = recovered target in crystals / target present before separation,\n\nwith seed mass excluded. It is therefore not the overall reagent-to-isolated-product yield. An approximate overall material yield is Y_reaction \u00d7 R_crystal; for batch 22 this is about 0.5222 \u00d7 0.4518 \u2248 0.236. High crystal purity also does not imply high reaction selectivity: batch 22 had only about 0.52 reaction selectivity but essentially pure recovered crystals. Thus crystallization performed a strong purification while leaving roughly half of the available target unrecovered in the mother liquor or separation losses.\n\nA simple framework is supersaturation S = C/C*(T, solvent, composition). Recovery generally rises as terminal solubility C* falls, approximately as 1 \u2212 C*V/M_target before accounting for kinetic and filtration losses. Nucleation rate is expected to increase very steeply with supersaturation, schematically J \u221d exp[\u2212B/(ln S)^2], whereas crystal growth has a less steep dependence such as G \u221d (S\u22121)^g. Conditions that generate supersaturation too abruptly can therefore increase J/G, producing many particles and a high number fraction below 20 micrometres even when mass recovery rises.\n\nProcess-history dependence\n\nObserved: Thermal history had a larger effect than endpoint temperature alone. With the same S2/C1 charge, 0.010 g seed, 270 K endpoint, and 7200 s cooling period, batch 18 used a 330 K reaction stage and gave fines 0.6347, whereas batch 22 used 350 K and gave 0.4546. Batch 1, also using the 350 K history, gave 0.4532. The two 350 K results are notably consistent.\n\nInterpretation: The 350 K stage may change solution memory before cooling through more complete dissolution, a different reaction/impurity distribution, or destruction of incipient clusters. It may also generate an impurity that inhibits secondary nucleation: degradation warnings were around 0.146\u20130.148 in batches 22\u201323, higher than the roughly 0.11 seen in many 330 K batches. That impurity-inhibition mechanism is plausible but unproven; the higher temperature could instead alter unobserved speciation or the effective supersaturation trajectory.\n\nObserved: Cooling duration was non-monotonic. At a 270 K endpoint after a 330 K reaction, batches 16\u201319 used 1800, 3600, 7200, and 10000 s and gave fines of 0.819, 0.702, 0.635, and 0.692. Longer cooling initially reduced fines, but 10000 s did not continue the trend. Several 14400 s experiments gave fines near 0.56\u20130.60. Recovery remained mostly around 0.43\u20130.44.\n\nInterpretation: Slower cooling can allow growth to consume supersaturation before extensive secondary nucleation, but the scatter indicates competing nucleation, growth, aggregation, and batch variability. Neither endpoint nor nominal duration alone describes the outcome adequately.\n\nObserved: Seed loading from zero to 0.050 g in batches 11\u201314 caused no decisive improvement: recovery remained 0.424\u20130.436 and fines 0.564\u20130.595. The unseeded batch 14 had somewhat lower purity (0.964), but the differences are not large enough to assign a robust seed-dose law.\n\nInterpretation: At the 330 K/270 K history, spontaneous or secondary nucleation probably dominated over the tested seed-mass effect. Seed timing, seed size distribution, and surface condition were not varied, so the result does not show that seeding is intrinsically ineffective.\n\nObserved: A temperature cycle in batch 23\u2014cooling to 260 K, reheating to 285 K, and recooling to 270 K\u2014gave passing fines of 0.4759 and purity 0.9974, but recovery fell to 0.4384 relative to batch 22. The likely benefit from partial dissolution or ripening was insufficient to compensate for target redissolution and incomplete recovery during the second cooling.\n\nRevisions during the campaign\n\nThe initial S2/350 K experiment (batch 1) was feasible. I then explored deeper cooling on the assumption that it would increase recovery, but the 250 K solvent screen showed that strong supersaturation could violate the fines constraint. Catalyst C2 offered a fines solution but imposed a large recovery penalty. Seed-dose studies did not resolve the problem, and cooling-time studies revealed substantial non-monotonicity. Returning to the 350 K history reproduced the low-fines regime in batch 22. Thermal cycling was subsequently tested in batch 23 but did not improve recovery. Batch 24 used a slightly lower 265 K endpoint and passed narrowly (recovery 0.4485, purity 1.000, fines 0.4851), but it neither exceeded batch 22 recovery nor provided as much fines margin, so it did not change the recommendation.\n\nUncertainty and unresolved tradeoff\n\nFinal-assay noise standard deviations were approximately 0.010 for recovery and 0.018 for fines, with additional process variability evident across nominally similar batches. The recovery difference between batches 22 and 24 (0.0033) is therefore not statistically decisive. Batch 22 is preferred because it had the highest observed feasible recovery and a larger fines margin: 0.4546 is about 0.045 below the limit, whereas batch 24 at 0.4851 is only about 0.015 below it. Purity was reported at the upper bound in both, so the exact purity advantage cannot be resolved, though both comfortably exceed 0.80.\n\nThe main unresolved tradeoff is recovery versus particle-number quality. Deeper or more forceful crystallization can retain recovery near 0.45 but often generates excessive fines; gentler histories or C2 can suppress fines but may sacrifice recovery. Batch 22 is a balanced feasible point, not proof of a global optimum. Untested alternatives include optimized multistage cooling without the large reheating used in batch 23, low-temperature aging, different seed size or addition temperature, reduced concentration, catalyst loading changes, quenching before crystallization, and deliberate impurity control. These remain hypotheses and do not alter the selected recommendation."
  },
  "failure": null,
  "elapsed_s": 88.17199999999139,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 428160,
    "input_tokens": 487982,
    "output_tokens": 9088,
    "reasoning_output_tokens": 3844
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
          "estimate": 0.2,
          "lower80": 0.09,
          "upper80": 0.34
        },
        "crystal_purity": {
          "estimate": 0.97,
          "lower80": 0.91,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.23,
          "lower80": 0.14,
          "upper80": 0.32
        },
        "crystal_yield": {
          "estimate": 0.48,
          "lower80": 0.34,
          "upper80": 0.62
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q01"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.34,
          "lower80": 0.2,
          "upper80": 0.49
        },
        "crystal_purity": {
          "estimate": 0.93,
          "lower80": 0.84,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.17,
          "lower80": 0.09,
          "upper80": 0.26
        },
        "crystal_yield": {
          "estimate": 0.37,
          "lower80": 0.24,
          "upper80": 0.51
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q02"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.39,
          "lower80": 0.23,
          "upper80": 0.57
        },
        "crystal_purity": {
          "estimate": 0.89,
          "lower80": 0.78,
          "upper80": 0.97
        },
        "crystal_size": {
          "estimate": 0.18,
          "lower80": 0.09,
          "upper80": 0.28
        },
        "crystal_yield": {
          "estimate": 0.31,
          "lower80": 0.18,
          "upper80": 0.45
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q03"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.27,
          "lower80": 0.14,
          "upper80": 0.43
        },
        "crystal_purity": {
          "estimate": 0.93,
          "lower80": 0.84,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.22,
          "lower80": 0.13,
          "upper80": 0.32
        },
        "crystal_yield": {
          "estimate": 0.34,
          "lower80": 0.21,
          "upper80": 0.48
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q04"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.24,
          "lower80": 0.12,
          "upper80": 0.4
        },
        "crystal_purity": {
          "estimate": 0.93,
          "lower80": 0.84,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.24,
          "lower80": 0.14,
          "upper80": 0.34
        },
        "crystal_yield": {
          "estimate": 0.35,
          "lower80": 0.22,
          "upper80": 0.49
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q05"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.58,
          "lower80": 0.4,
          "upper80": 0.75
        },
        "crystal_purity": {
          "estimate": 0.89,
          "lower80": 0.78,
          "upper80": 0.97
        },
        "crystal_size": {
          "estimate": 0.12,
          "lower80": 0.05,
          "upper80": 0.22
        },
        "crystal_yield": {
          "estimate": 0.37,
          "lower80": 0.23,
          "upper80": 0.52
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q06"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.22,
          "lower80": 0.1,
          "upper80": 0.38
        },
        "crystal_purity": {
          "estimate": 0.94,
          "lower80": 0.86,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.26,
          "lower80": 0.16,
          "upper80": 0.37
        },
        "crystal_yield": {
          "estimate": 0.36,
          "lower80": 0.23,
          "upper80": 0.5
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q07"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.56,
          "lower80": 0.37,
          "upper80": 0.74
        },
        "crystal_purity": {
          "estimate": 0.9,
          "lower80": 0.79,
          "upper80": 0.98
        },
        "crystal_size": {
          "estimate": 0.14,
          "lower80": 0.06,
          "upper80": 0.24
        },
        "crystal_yield": {
          "estimate": 0.22,
          "lower80": 0.1,
          "upper80": 0.37
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q08"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.88,
          "lower80": 0.72,
          "upper80": 0.97
        },
        "crystal_purity": {
          "estimate": 0.91,
          "lower80": 0.75,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.035,
          "lower80": 0.015,
          "upper80": 0.07
        },
        "crystal_yield": {
          "estimate": 0.015,
          "lower80": 0.002,
          "upper80": 0.05
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q09"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.69,
          "lower80": 0.5,
          "upper80": 0.84
        },
        "crystal_purity": {
          "estimate": 0.92,
          "lower80": 0.81,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.075,
          "lower80": 0.03,
          "upper80": 0.14
        },
        "crystal_yield": {
          "estimate": 0.1,
          "lower80": 0.04,
          "upper80": 0.19
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q10"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.23,
          "lower80": 0.11,
          "upper80": 0.39
        },
        "crystal_purity": {
          "estimate": 0.94,
          "lower80": 0.86,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.25,
          "lower80": 0.15,
          "upper80": 0.36
        },
        "crystal_yield": {
          "estimate": 0.36,
          "lower80": 0.23,
          "upper80": 0.5
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q11"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.44,
          "lower80": 0.27,
          "upper80": 0.61
        },
        "crystal_purity": {
          "estimate": 0.9,
          "lower80": 0.79,
          "upper80": 0.97
        },
        "crystal_size": {
          "estimate": 0.18,
          "lower80": 0.1,
          "upper80": 0.28
        },
        "crystal_yield": {
          "estimate": 0.55,
          "lower80": 0.41,
          "upper80": 0.68
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q12"
      }
    ],
    "rationale": "All recipes contain seed, so particles are expected even when seed-excluded product recovery is very small. Q01 versus Q02 reflects the lower nominal solubility, faster growth, lower nucleation tendency and lower occlusion of S1 relative to S3, giving Q01 higher recovery, size and purity with fewer fines. Q03 versus Q04 assigns the larger seed charge a modest kinetic advantage: faster supersaturation consumption, fewer secondary nuclei and slightly higher recovery. Q05 versus Q06 separates gradual cooling from an initial temperature crash; the long low-temperature hold in Q06 preserves or slightly raises recovery, but cannot fully erase the fine population created during rapid cooling. Q07 versus Q08 treats the 315 K excursion as substantial redissolution followed by an overly rapid recooling, lowering recovered product and regenerating fines. Q09 versus Q10 shows that a two-hour hold at 292 K permits measurable deposition and growth, although both remain fines-limited and Q09 has almost no seed-excluded recovery. Q11 versus Q12 assigns the doubled reagent concentration much higher supersaturation and recovery, together with smaller crystals, more fines and slightly lower purity; its point estimate remains feasible but the interval crosses both quality thresholds. Intervals are deliberately broad because these recipes extrapolate beyond the campaign in concentration, 385 K reaction history and multi-day staged cooling; they represent mechanistic predictive uncertainty rather than final-assay noise."
  },
  "failure": null,
  "elapsed_s": 95.01600000000326,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 431744,
    "input_tokens": 531663,
    "output_tokens": 13962,
    "reasoning_output_tokens": 7007
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
    "report": "1. Status of the main claims\n\nSupported by direct observations:\n- Solvent-S2 was the strongest solvent in the matched screen. Under the common batch 2\u20135 history, batch 4 (S2) had the highest crystal recovery (0.458), highest purity (1.000), and lowest fines fraction (0.597), although it still failed the fines limit. This supports the empirical solvent ranking under that history; attributing it to low solubility, low occlusion and favorable growth remains an interpretation.\n- The 350 K history was reproducibly associated with fewer fines. Batches 1 and 22 used essentially the same S2/C1, 350 K, seeded 270 K process and gave fines of 0.453 and 0.455. Batch 18 used the analogous 330 K/270 K/7200 s history and gave 0.635. The association is direct; cluster erasure, altered impurity chemistry and nucleation inhibition are competing interpretations.\n- Crystallization strongly purified a mediocre reaction mixture. Batch 22 had reaction selectivity about 0.521 but crystal purity 1.000; batch 1 similarly combined selectivity 0.533 with purity 0.987. The separation effect is observed directly.\n- Catalyst-C2 exhibited a quality/recovery tradeoff. Batch 7 passed the fines constraint at 0.428 but recovered only 0.338, whereas C0 and C3 in batches 6 and 8 recovered about 0.440\u20130.442 but failed on fines. The catalyst-dependent outcomes are observed, while the proposed impurity-mediated mechanism is not identified.\n- The tested temperature cycle did not improve recovery. Relative to batch 22, batch 23 reduced recovery from 0.452 to 0.438 while retaining acceptable fines. This directly contradicts the tentative expectation that partial redissolution and ripening would necessarily improve the result.\n\nContradicted or substantially weakened:\n- A simple \u201ccolder or longer always improves crystallization\u201d rule was contradicted. Cooling-time batches 16\u201319 gave fines of 0.819, 0.702, 0.635 and 0.692 as duration increased, so the response was non-monotonic. The 250 K solvent screen also produced severe fines despite deep cooling.\n- A strong monotonic seed-mass effect was not supported. Across batches 11\u201314, seed charges from zero to 0.050 g left recovery near 0.424\u20130.436 and fines near 0.564\u20130.595. Small directional differences existed, but they were comparable to process and assay uncertainty.\n- The initial idea that lowering the endpoint from 270 to 265 K would clearly increase feasible recovery was weakened by batch 24: it remained feasible but recovered 0.449, slightly below batch 22, and had less fines margin.\n\nStill untested:\n- Whether the favorable 350 K effect is physical solution memory, destruction of precursor clusters, a changed impurity spectrum, or formation of a nucleation inhibitor.\n- Actual target concentration in the mother liquor and therefore the equilibrium-versus-kinetic contribution to unrecovered product.\n- Seed size, morphology and addition temperature; only seed mass was varied.\n- Quenching effects, staged cooling over many days, low-concentration operation, and reheating a mature slurry above 285 K. These were important extrapolations in the held-out predictions but were not campaign observations.\n- The global optimum remains untested; batch 22 is the best observed feasible point, not proof of optimality.\n\n2. One additional experiment\n\nI would run the batch-22 S2/C1 charge but first react at 330 K for 3600 s, take an HPLC measurement, quench to freeze reaction chemistry, then heat the quenched solution to 350 K for 3600 s before adding 0.010 g seed and cooling to 270 K over 7200 s. I would obtain an in-situ particle-size measurement, filter, terminate and perform the final assay.\n\nThis experiment distinguishes two leading explanations for the 350 K effect. If post-quench thermal conditioning gives fines near 0.45 while the HPLC composition remains characteristic of the 330 K reaction, physical dissolution of clusters or solution-memory erasure is favored. If fines remain near the 330 K result of roughly 0.63, the benefit probably requires reaction or impurity chemistry occurring while the unquenched mixture is at 350 K. An intermediate result around 0.50\u20130.56 would suggest both mechanisms contribute. A large purity or recovery change would additionally show that quench chemistry is a confound, so the interpretation would remain qualified.\n\n3. Least-used observation and least-reliable prediction\n\nThe intermediate HPLC result from batch 1 was used least effectively. It established conversion 1.000, selectivity about 0.546 and byproduct signal about 0.322 before crystallization, but no matched HPLC measurement was collected for a 330 K comparator. Consequently, the account invoked altered impurity chemistry without directly showing that batches 18 and 22 entered crystallization with different liquid compositions. The numerous pre-filtration particle measurements were also secondary to final assays and could have been used more explicitly to quantify filtration or measurement-stage changes\u2014for example, batch 23 changed from an in-situ fines estimate of 0.525 to a final value of 0.476.\n\nQ08 is the least reliable held-out prediction. It reheats a mature, slowly grown S0 slurry to 315 K after roughly 80 hours and then recools it in only one hour. The campaign\u2019s closest cycle was batch 23, which reheated only to 285 K and had a very different solvent, concentration and prior cooling history. Whether 315 K causes slight ripening, selective fines dissolution, or nearly complete redissolution is unknown; those alternatives imply very different recovery, size and fines outcomes. The sealed Q08 estimate therefore depends more heavily on extrapolation than the other paired predictions."
  },
  "failure": null,
  "elapsed_s": 53.10899999999674,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 463104,
    "input_tokens": 580138,
    "output_tokens": 16342,
    "reasoning_output_tokens": 8101
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
    "selected_experiment_index": 22,
    "selection_rationale": "Highest observed seed-excluded crystal recovery among batches meeting both constraints: crystal_yield 0.452, crystal_purity 1.000, fines fraction 0.455."
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
        "stirring_speed_rpm": 500,
        "target_temperature_K": 350
      },
      {
        "operation": "seed_crystals",
        "seed_mass_g": 0.01
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
    "excluded_rejected_attempts": [],
    "lifecycle_index": 22,
    "source_attempts": 10
  },
  "prediction_evaluation": {
    "contrasts": [
      {
        "absolute_delta_error": 0.03989151001544344,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_yield",
        "predicted_delta": -0.10999999999999999,
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
        "absolute_delta_error": 0.07938040150063501,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_size",
        "predicted_delta": -0.06,
        "resolved": true,
        "true_delta": 0.01938040150063501
      },
      {
        "absolute_delta_error": 0.6683138299289018,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.14,
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
        "absolute_delta_error": 0.03025394536462178,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_purity",
        "predicted_delta": 0.040000000000000036,
        "resolved": false,
        "true_delta": 0.009746054635378254
      },
      {
        "absolute_delta_error": 0.047185571102035875,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_size",
        "predicted_delta": 0.04000000000000001,
        "resolved": true,
        "true_delta": -0.007185571102035868
      },
      {
        "absolute_delta_error": 0.28426690822029765,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.12,
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
        "absolute_delta_error": 0.036445289569308814,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.040000000000000036,
        "resolved": false,
        "true_delta": -0.0035547104306912214
      },
      {
        "absolute_delta_error": 0.07668654733429697,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_size",
        "predicted_delta": -0.12,
        "resolved": true,
        "true_delta": -0.04331345266570302
      },
      {
        "absolute_delta_error": 0.2829539628584593,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.33999999999999997,
        "resolved": true,
        "true_delta": 0.6229539628584593
      },
      {
        "absolute_delta_error": 0.18437670725156424,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_yield",
        "predicted_delta": -0.13999999999999999,
        "resolved": true,
        "true_delta": 0.04437670725156426
      },
      {
        "absolute_delta_error": 0.028943817205800748,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.039999999999999925,
        "resolved": true,
        "true_delta": -0.011056182794199176
      },
      {
        "absolute_delta_error": 0.080294418729357,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_size",
        "predicted_delta": -0.12,
        "resolved": true,
        "true_delta": -0.039705581270643
      },
      {
        "absolute_delta_error": 0.32037028724012584,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.3400000000000001,
        "resolved": true,
        "true_delta": 0.6603702872401259
      },
      {
        "absolute_delta_error": 0.00951718430200213,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_yield",
        "predicted_delta": 0.085,
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
        "absolute_delta_error": 0.026101832298345215,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_size",
        "predicted_delta": 0.039999999999999994,
        "resolved": true,
        "true_delta": 0.013898167701654779
      },
      {
        "absolute_delta_error": 0.2553927297818388,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.19000000000000006,
        "resolved": false,
        "true_delta": 0.06539272978183874
      },
      {
        "absolute_delta_error": 0.17504321303990114,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_yield",
        "predicted_delta": 0.19000000000000006,
        "resolved": false,
        "true_delta": 0.014956786960098917
      },
      {
        "absolute_delta_error": 0.03482839724908715,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_purity",
        "predicted_delta": -0.039999999999999925,
        "resolved": false,
        "true_delta": -0.005171602750912774
      },
      {
        "absolute_delta_error": 0.04435687395732106,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_size",
        "predicted_delta": -0.07,
        "resolved": true,
        "true_delta": -0.025643126042678946
      },
      {
        "absolute_delta_error": 0.3959895667604082,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.21,
        "resolved": true,
        "true_delta": 0.6059895667604082
      }
    ],
    "failures": [],
    "metrics": {
      "crystal_fines_fraction": {
        "coverage80": 0.5,
        "interval_score80": 1.734964413406588,
        "interval_width": 0.305,
        "mae": 0.2839914056603944,
        "n": 12,
        "planned": 12
      },
      "crystal_purity": {
        "coverage80": 0.6666666666666666,
        "interval_score80": 0.19827911999545453,
        "interval_width": 0.16416666666666666,
        "mae": 0.06459582857158806,
        "n": 12,
        "planned": 12
      },
      "crystal_size": {
        "coverage80": 0.25,
        "interval_score80": 0.47445264287076117,
        "interval_width": 0.17041666666666666,
        "mae": 0.10615103250145604,
        "n": 12,
        "planned": 12
      },
      "crystal_yield": {
        "coverage80": 0.4166666666666667,
        "interval_score80": 0.4289936036227611,
        "interval_width": 0.24400000000000002,
        "mae": 0.11797692518252424,
        "n": 12,
        "planned": 12
      }
    },
    "quality": {
      "balanced_accuracy": 0.8333333333333333,
      "false_negative": 0,
      "false_positive": 2,
      "true_negative": 4,
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
        "crystal_fines_fraction": 0.3071534143698245,
        "crystal_purity": 0.0043002806978992185,
        "crystal_size": 0.018999905288188203,
        "crystal_yield": 0.21724454035587304
      },
      "public_nearest_neighbor": {
        "crystal_fines_fraction": 0.30865382222454046,
        "crystal_purity": 0.00698818682810845,
        "crystal_size": 0.026239868113748916,
        "crystal_yield": 0.19102749695606225
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
        "cached_input": 424704,
        "input": 456419,
        "output": 5506,
        "stage": "source",
        "uncached_input": 31715
      },
      {
        "cached_input": 3456,
        "input": 31563,
        "output": 3582,
        "stage": "K1",
        "uncached_input": 28107
      },
      {
        "cached_input": 3584,
        "input": 43681,
        "output": 4874,
        "stage": "Q",
        "uncached_input": 40097
      },
      {
        "cached_input": 31360,
        "input": 48475,
        "output": 2380,
        "stage": "K2",
        "uncached_input": 17115
      }
    ],
    "total": {
      "cached_input": 463104,
      "input": 580138,
      "input_plus_output": 596480,
      "output": 16342,
      "uncached_input": 117034
    },
    "valid": true
  },
  "elapsed_s": 527.4070000000065
}
```
