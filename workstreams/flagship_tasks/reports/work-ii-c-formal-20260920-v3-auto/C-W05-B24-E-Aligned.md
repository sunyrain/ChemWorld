# C-W05-B24-E-Aligned

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
      "target_temperature_K": 370
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
      "target_temperature_K": 260
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
  "end_step": 12,
  "lifecycle_index": 1,
  "metrics": {
    "byproduct_signal": 0.37551313638687134,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6834776997566223,
    "crystal_fines_fraction": 0.5374366044998169,
    "crystal_purity": 0.9860137701034546,
    "crystal_size": 0.05958862602710724,
    "crystal_yield": 0.37520861625671387,
    "degradation_warning": 0.1748649924993515,
    "safety_risk": 0.17172731459140778,
    "score": 0.4436812400817871,
    "selectivity": 0.46543386578559875,
    "virtual_spectrum_summary": 0.2852214574813843,
    "yield": 0.4632713794708252
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
      "duration_s": 3600,
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
      "seed_mass_g": 0.05
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
    "byproduct_signal": 0.34411340951919556,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.523507297039032,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9771736860275269,
    "crystal_size": 0.07437461614608765,
    "crystal_yield": 0.3976650536060333,
    "degradation_warning": 0.11106379330158234,
    "safety_risk": 0.173446387052536,
    "score": 0.3733530640602112,
    "selectivity": 0.48606008291244507,
    "virtual_spectrum_summary": 0.2392410784959793,
    "yield": 0.4745984375476837
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 500,
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
  "end_step": 39,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.4301791191101074,
    "conversion": 0.9983177185058594,
    "cost": 1.0,
    "crystal_csd_quality": 0.48931506276130676,
    "crystal_fines_fraction": 0.994870126247406,
    "crystal_purity": 0.9850836992263794,
    "crystal_size": 0.05089101940393448,
    "crystal_yield": 0.23245182633399963,
    "degradation_warning": 0.12574288249015808,
    "safety_risk": 0.15243828296661377,
    "score": 0.29109710454940796,
    "selectivity": 0.291640967130661,
    "virtual_spectrum_summary": 0.2931828200817108,
    "yield": 0.29075363278388977
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
  "end_step": 51,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.30971500277519226,
    "conversion": 0.9889920949935913,
    "cost": 1.0,
    "crystal_csd_quality": 0.5198434591293335,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 1.0,
    "crystal_size": 0.04052690789103508,
    "crystal_yield": 0.4772065281867981,
    "degradation_warning": 0.13780738413333893,
    "safety_risk": 0.16538913547992706,
    "score": 0.40851882100105286,
    "selectivity": 0.5653965473175049,
    "virtual_spectrum_summary": 0.23235657811164856,
    "yield": 0.5517644286155701
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
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 370
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
  "end_step": 63,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.4256998598575592,
    "conversion": 0.9963378310203552,
    "cost": 1.0,
    "crystal_csd_quality": 0.4600108563899994,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9752860069274902,
    "crystal_size": 0.04131881147623062,
    "crystal_yield": 0.3811340630054474,
    "degradation_warning": 0.2573677599430084,
    "safety_risk": 0.17325171828269958,
    "score": 0.3545405864715576,
    "selectivity": 0.49202510714530945,
    "virtual_spectrum_summary": 0.3499504029750824,
    "yield": 0.48587214946746826
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
      "catalyst": 3,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 370
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
  "end_step": 76,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.42317476868629456,
    "conversion": 0.992433488368988,
    "cost": 1.0,
    "crystal_csd_quality": 0.4407722055912018,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9987807869911194,
    "crystal_size": 0.03719549998641014,
    "crystal_yield": 0.40840089321136475,
    "degradation_warning": 0.26190364360809326,
    "safety_risk": 0.1739194095134735,
    "score": 0.3589130640029907,
    "selectivity": 0.4720326364040375,
    "virtual_spectrum_summary": 0.35060277581214905,
    "yield": 0.47391825914382935
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
      "stirring_speed_rpm": 600,
      "target_temperature_K": 370
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
  "end_step": 88,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.37535789608955383,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6592890620231628,
    "crystal_fines_fraction": 0.5269340872764587,
    "crystal_purity": 0.9794034957885742,
    "crystal_size": 0.07755545526742935,
    "crystal_yield": 0.4023328721523285,
    "degradation_warning": 0.1720365285873413,
    "safety_risk": 0.17179103195667267,
    "score": 0.4461846947669983,
    "selectivity": 0.4411032795906067,
    "virtual_spectrum_summary": 0.28386327624320984,
    "yield": 0.4677504897117615
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
      "stirring_speed_rpm": 600,
      "target_temperature_K": 370
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
      "target_temperature_K": 260
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
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
  "end_step": 103,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.3676678538322449,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6906043291091919,
    "crystal_fines_fraction": 0.5282196998596191,
    "crystal_purity": 0.9797373414039612,
    "crystal_size": 0.0942181646823883,
    "crystal_yield": 0.4084624946117401,
    "degradation_warning": 0.17860440909862518,
    "safety_risk": 0.17179103195667267,
    "score": 0.45706236362457275,
    "selectivity": 0.4722861349582672,
    "virtual_spectrum_summary": 0.28258928656578064,
    "yield": 0.46398088335990906
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 370
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
  "end_step": 115,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.32528263330459595,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.4693974256515503,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9827200174331665,
    "crystal_size": 0.049528732895851135,
    "crystal_yield": 0.4696561396121979,
    "degradation_warning": 0.1450234353542328,
    "safety_risk": 0.16292628645896912,
    "score": 0.39067742228507996,
    "selectivity": 0.5272555947303772,
    "virtual_spectrum_summary": 0.24416600167751312,
    "yield": 0.5409315824508667
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
      "stirring_speed_rpm": 600,
      "target_temperature_K": 370
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
  "end_step": 127,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.370994508266449,
    "conversion": 0.9858242273330688,
    "cost": 1.0,
    "crystal_csd_quality": 0.42679670453071594,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9766750931739807,
    "crystal_size": 0.05684763193130493,
    "crystal_yield": 0.36495479941368103,
    "degradation_warning": 0.18261435627937317,
    "safety_risk": 0.17008498311042786,
    "score": 0.34179890155792236,
    "selectivity": 0.4615996778011322,
    "virtual_spectrum_summary": 0.286223441362381,
    "yield": 0.47052648663520813
  },
  "ordinal": 10
}
```

## Batch 11

```json
{
  "actions": [
    {
      "amount_mol": 0.03,
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
      "target_temperature_K": 370
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
  "end_step": 139,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.3678155243396759,
    "conversion": 0.9990203380584717,
    "cost": 1.0,
    "crystal_csd_quality": 0.5630888938903809,
    "crystal_fines_fraction": 0.7123945355415344,
    "crystal_purity": 0.9935006499290466,
    "crystal_size": 0.07448447495698929,
    "crystal_yield": 0.421330988407135,
    "degradation_warning": 0.17616334557533264,
    "safety_risk": 0.15024924278259277,
    "score": 0.4279972314834595,
    "selectivity": 0.5306074023246765,
    "virtual_spectrum_summary": 0.28157204389572144,
    "yield": 0.5111175179481506
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
      "volume_L": 0.06
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
      "target_temperature_K": 370
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
  "end_step": 151,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.36685627698898315,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.46781572699546814,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9973495602607727,
    "crystal_size": 0.08925485610961914,
    "crystal_yield": 0.39916524291038513,
    "degradation_warning": 0.1857893168926239,
    "safety_risk": 0.176642045378685,
    "score": 0.36406415700912476,
    "selectivity": 0.45452895760536194,
    "virtual_spectrum_summary": 0.2853761315345764,
    "yield": 0.459570974111557
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
      "stirring_speed_rpm": 600,
      "target_temperature_K": 370
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
      "duration_s": 7200,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 280
    },
    {
      "duration_s": 7200,
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
  "end_step": 167,
  "lifecycle_index": 13,
  "metrics": {
    "byproduct_signal": 0.36702707409858704,
    "conversion": 0.9972169399261475,
    "cost": 1.0,
    "crystal_csd_quality": 0.6892602443695068,
    "crystal_fines_fraction": 0.536181628704071,
    "crystal_purity": 0.9807656407356262,
    "crystal_size": 0.06424052268266678,
    "crystal_yield": 0.3816886842250824,
    "degradation_warning": 0.17302127182483673,
    "safety_risk": 0.17179103195667267,
    "score": 0.44629207253456116,
    "selectivity": 0.4712902009487152,
    "virtual_spectrum_summary": 0.27972447872161865,
    "yield": 0.463277667760849
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
      "stirring_speed_rpm": 600,
      "target_temperature_K": 370
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
      "target_temperature_K": 310
    },
    {
      "duration_s": 14400,
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
  "end_step": 184,
  "lifecycle_index": 14,
  "metrics": {
    "byproduct_signal": 0.3813401460647583,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6954194903373718,
    "crystal_fines_fraction": 0.5514177083969116,
    "crystal_purity": 0.9641237854957581,
    "crystal_size": 0.10003940016031265,
    "crystal_yield": 0.38661766052246094,
    "degradation_warning": 0.17794689536094666,
    "safety_risk": 0.17179103195667267,
    "score": 0.4465440809726715,
    "selectivity": 0.46468913555145264,
    "virtual_spectrum_summary": 0.28981319069862366,
    "yield": 0.4585016965866089
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
      "stirring_speed_rpm": 600,
      "target_temperature_K": 370
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
      "target_temperature_K": 260
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
  "end_step": 197,
  "lifecycle_index": 15,
  "metrics": {
    "byproduct_signal": 0.3747466504573822,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6477854251861572,
    "crystal_fines_fraction": 0.5526936054229736,
    "crystal_purity": 0.9872069954872131,
    "crystal_size": 0.07514335215091705,
    "crystal_yield": 0.383515328168869,
    "degradation_warning": 0.17079441249370575,
    "safety_risk": 0.17179103195667267,
    "score": 0.4392092823982239,
    "selectivity": 0.46270450949668884,
    "virtual_spectrum_summary": 0.282968133687973,
    "yield": 0.46723905205726624
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
      "stirring_speed_rpm": 600,
      "target_temperature_K": 370
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
  "end_step": 212,
  "lifecycle_index": 16,
  "metrics": {
    "byproduct_signal": 0.3678254783153534,
    "conversion": 0.9885537624359131,
    "cost": 1.0,
    "crystal_csd_quality": 0.6278790831565857,
    "crystal_fines_fraction": 0.5279213786125183,
    "crystal_purity": 0.9772384166717529,
    "crystal_size": 0.06935235857963562,
    "crystal_yield": 0.3831082880496979,
    "degradation_warning": 0.18211866915225983,
    "safety_risk": 0.17179103195667267,
    "score": 0.43343794345855713,
    "selectivity": 0.45985618233680725,
    "virtual_spectrum_summary": 0.2842574119567871,
    "yield": 0.4582107663154602
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
      "catalyst_amount_mol": 0.0025,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 370
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
  "end_step": 224,
  "lifecycle_index": 17,
  "metrics": {
    "byproduct_signal": 0.4034375846385956,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5659915804862976,
    "crystal_fines_fraction": 0.6997115015983582,
    "crystal_purity": 0.99781334400177,
    "crystal_size": 0.06972881406545639,
    "crystal_yield": 0.3178584575653076,
    "degradation_warning": 0.13904060423374176,
    "safety_risk": 0.16170044243335724,
    "score": 0.37826108932495117,
    "selectivity": 0.3753126859664917,
    "virtual_spectrum_summary": 0.2844589352607727,
    "yield": 0.3854639530181885
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
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 370
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
  "end_step": 236,
  "lifecycle_index": 18,
  "metrics": {
    "byproduct_signal": 0.33952826261520386,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.4723914563655853,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9916101694107056,
    "crystal_size": 0.11935419589281082,
    "crystal_yield": 0.42263302206993103,
    "degradation_warning": 0.16954319179058075,
    "safety_risk": 0.1765892505645752,
    "score": 0.38245654106140137,
    "selectivity": 0.5009253025054932,
    "virtual_spectrum_summary": 0.26303496956825256,
    "yield": 0.5143322348594666
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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 390
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
  "end_step": 248,
  "lifecycle_index": 19,
  "metrics": {
    "byproduct_signal": 0.28806090354919434,
    "conversion": 0.9908943176269531,
    "cost": 1.0,
    "crystal_csd_quality": 0.6556306481361389,
    "crystal_fines_fraction": 0.5284146666526794,
    "crystal_purity": 0.9755874872207642,
    "crystal_size": 0.05931971222162247,
    "crystal_yield": 0.49014490842819214,
    "degradation_warning": 0.09504576027393341,
    "safety_risk": 0.18377801775932312,
    "score": 0.4833434820175171,
    "selectivity": 0.5612756609916687,
    "virtual_spectrum_summary": 0.2012040913105011,
    "yield": 0.5648572444915771
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
      "duration_s": 1200,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 410
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
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 290
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
  "end_step": 261,
  "lifecycle_index": 20,
  "metrics": {
    "byproduct_signal": 0.2435372769832611,
    "conversion": 0.9931780099868774,
    "cost": 1.0,
    "crystal_csd_quality": 0.7887857556343079,
    "crystal_fines_fraction": 0.21497881412506104,
    "crystal_purity": 0.9951504468917847,
    "crystal_size": 0.09121385216712952,
    "crystal_yield": 0.5287037491798401,
    "degradation_warning": 0.06706012040376663,
    "safety_risk": 0.18994399905204773,
    "score": 0.5667136311531067,
    "selectivity": 0.6225672960281372,
    "virtual_spectrum_summary": 0.1641225516796112,
    "yield": 0.60606849193573
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
      "duration_s": 1200,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 410
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
      "target_temperature_K": 320
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
  "end_step": 274,
  "lifecycle_index": 21,
  "metrics": {
    "byproduct_signal": 0.2206408530473709,
    "conversion": 0.9891213178634644,
    "cost": 1.0,
    "crystal_csd_quality": 0.8462613821029663,
    "crystal_fines_fraction": 0.17743830382823944,
    "crystal_purity": 0.992786705493927,
    "crystal_size": 0.0743032768368721,
    "crystal_yield": 0.5526928901672363,
    "degradation_warning": 0.06491652876138687,
    "safety_risk": 0.19036902487277985,
    "score": 0.5867777466773987,
    "selectivity": 0.6047516465187073,
    "virtual_spectrum_summary": 0.15056490898132324,
    "yield": 0.6238518953323364
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
      "duration_s": 900,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 430
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
      "target_temperature_K": 330
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
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
  "end_step": 288,
  "lifecycle_index": 22,
  "metrics": {
    "byproduct_signal": 0.2192467451095581,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.8246056437492371,
    "crystal_fines_fraction": 0.11755625158548355,
    "crystal_purity": 1.0,
    "crystal_size": 0.09603047370910645,
    "crystal_yield": 0.5695856809616089,
    "degradation_warning": 0.048690345138311386,
    "safety_risk": 0.1941055804491043,
    "score": 0.5993583798408508,
    "selectivity": 0.6340466737747192,
    "virtual_spectrum_summary": 0.14249636232852936,
    "yield": 0.6335766315460205
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
      "duration_s": 900,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 450
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
      "target_temperature_K": 280
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
  "end_step": 302,
  "lifecycle_index": 23,
  "metrics": {
    "byproduct_signal": 0.2161017507314682,
    "conversion": 0.9934808611869812,
    "cost": 1.0,
    "crystal_csd_quality": 0.7940953969955444,
    "crystal_fines_fraction": 0.14235346019268036,
    "crystal_purity": 1.0,
    "crystal_size": 0.11497803777456284,
    "crystal_yield": 0.5698866844177246,
    "degradation_warning": 0.04526882991194725,
    "safety_risk": 0.19499032199382782,
    "score": 0.5969259142875671,
    "selectivity": 0.6566852331161499,
    "virtual_spectrum_summary": 0.13922692835330963,
    "yield": 0.657437801361084
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
      "duration_s": 900,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 470
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
      "target_temperature_K": 330
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
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
  "end_step": 316,
  "lifecycle_index": 24,
  "metrics": {
    "byproduct_signal": 0.2156638354063034,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7806451320648193,
    "crystal_fines_fraction": 0.17802177369594574,
    "crystal_purity": 1.0,
    "crystal_size": 0.09673920273780823,
    "crystal_yield": 0.567886471748352,
    "degradation_warning": 0.05067571625113487,
    "safety_risk": 0.19557946920394897,
    "score": 0.5889496207237244,
    "selectivity": 0.6539765000343323,
    "virtual_spectrum_summary": 0.1414191722869873,
    "yield": 0.6626195907592773
  },
  "ordinal": 24
}
```

## K1

```json
{
  "payload": {
    "report": "Mechanistic account\n\nRecommended batch 23 used 0.040 mol reagent, 0.080 L solvent-S2, 0.005 mol catalyst-C1, heating toward 450 K for 900 s at 600 rpm (observed reactor temperature 413.84 K), quenching to 368.84 K, adding 0.050 g seed, staged cooling, a 14,400 s hold at 250 K and 100 rpm, filtration, and final assay. Its observed seed-excluded crystal recovery was 0.5699, purity 1.000, and number fraction below 20 \u00b5m 0.142. The nominal first cooling request toward 340 K produced no recorded temperature change; the effective recorded cooling stages were 310, 280, and 250 K. That non-response should not be treated as evidence for a 340 K crystallization mechanism.\n\nObservations and interpretation\n\n1. Material effects were strongly interactive rather than additive. The public prior characterized S2 as relatively low-solubility (0.70), low-nucleation (0.65), high-growth (1.30), and low-occlusion (0.65). Its empirical performance with C1 is consistent with a solvent that supplies strong crystallization driving force while permitting seed growth, but only when supersaturation is introduced gradually. Catalyst identity also changed the downstream particle distribution, presumably through the target/impurity composition delivered to crystallization. Under broadly similar S2, high-temperature conditions, C1 gave fines near 0.53 in batches 7\u20138, whereas C3 in batch 6 and C0 in batch 18 gave fines near 1.00. C2 in batch 3 also gave poor reaction selectivity (0.292 final assay), recovery (0.232), and fines (0.995). Halving C1 from 0.005 to 0.0025 mol in batch 17 reduced crystal recovery to 0.318 and increased fines to 0.700. These results support a real C1\u2013S2 coupling, not merely selection of the nominally most active catalyst.\n\nS1 could give substantial recovery but failed particle quality: batch 9 (C1/S1) gave recovery 0.470 with fines 1.000, and batch 4 (C3/S1) gave recovery 0.477 with fines 1.000. Thus S1 was rejected despite acceptable purity. Lowering reagent charge to 0.030 mol in batch 11 increased fines to 0.712, while reducing S2 volume to 0.060 L in batch 12 produced fines 1.000. Neither simple dilution nor greater concentration solved the quality problem.\n\n2. Reaction history controlled crystallization through composition and seed-entry temperature. The early 370 K/3,600 s C1/S2 process gave essentially complete conversion but only about 0.44\u20130.47 selectivity, byproduct signal around 0.37, degradation warning around 0.17, crystal recovery around 0.38\u20130.41, and fines around 0.53 (batches 1, 7, 8, 13\u201316). Moving to shorter, hotter reactions improved the reaction packet and downstream recovery: batch 19, heated toward 390 K for 1,800 s (384.0 K observed), gave selectivity 0.561, reaction yield 0.565, degradation 0.095, and crystal recovery 0.490. Batch 20, heated toward 410 K for 1,200 s (397.75 K observed), gave selectivity 0.623, reaction yield 0.606, degradation 0.067, recovery 0.529, and fines 0.215 after staged cooling. Batch 22, heated toward 430 K for 900 s (404.15 K observed), reached reaction yield 0.634, crystal recovery 0.5696, and fines 0.118. Batch 23 reached reaction yield 0.657 and recovery 0.5699. Further heating in batch 24 (422.25 K observed) raised reaction yield slightly to 0.663 but did not improve crystallization-stage recovery (0.5679) and increased fines to 0.178. This suggests a plateau near the batch-22/23 region rather than evidence that ever-higher temperature is beneficial.\n\nA plausible interpretation is that the short, hot treatment favored rapid target formation relative to persistent byproduct/degradation formation and left a mother liquor more favorable to selective seeded growth. It also caused quench temperatures of roughly 353\u2013369 K in batches 20\u201323, much higher than the approximately 321 K seed-entry temperature of the early 370 K experiments. High-temperature seed addition followed by staged cooling may have allowed partial seed conditioning and growth before strong supersaturation developed. This interpretation is consistent with the data but seed survival or partial dissolution was not directly measured.\n\n3. Cooling endpoint alone did not determine quality; the full thermal history mattered. At the earlier reaction condition, direct cooling to 280 K in batch 10 gave fines 1.000 and recovery 0.365. Direct cooling to 260 K followed by one hold gave fines about 0.53 and recovery about 0.40 in batches 7 and 15. Very slow multistage cooling from an approximately 321 K seed-entry point did not by itself solve the problem: batch 14 still gave fines 0.551 and recovery 0.387. Likewise, direct cooling after the hotter reaction in batch 19 left fines at 0.528. In contrast, coupling the short/hot reaction to staged cooling produced fines 0.215 in batch 20; extending the final stage to 250 K raised recovery to 0.553 while reducing fines to 0.177 in batch 21. Batches 22\u201324, using still hotter/shorter reactions and several stages down to 250 K, delivered recoveries of 0.568\u20130.570 with fines of 0.118\u20130.178. Therefore the major revision was not simply \u201ccool more slowly\u201d; it was to combine favorable upstream composition, high-temperature seeding, staged removal of supersaturation, and a final low-temperature growth/ripening hold.\n\nUseful relationships\n\nFor interpretation, reaction target production may be written approximately as\n\nn_target,pre-separation \u2248 n_reagent \u00d7 conversion \u00d7 selectivity,\n\nand recovered target crystal as\n\nn_target,crystal = Y_crystal \u00d7 n_target,pre-separation,\n\nwhere the reported Y_crystal is explicitly seed-excluded crystallization-stage recovery. Thus overall isolated target relative to reagent is approximately reaction yield \u00d7 crystal recovery. For batch 23 this is about 0.657 \u00d7 0.570 \u2248 0.375. This overall figure is useful for mass-balance thinking, but it is not interchangeable with the campaign objective, which was crystallization-stage recovery subject to purity and fines constraints.\n\nA conventional qualitative crystallization model is also useful:\n\nsupersaturation \u03c3 = C/C*(T,solvent) \u2212 1,\nJ \u2248 k_n \u03c3^m,\nG \u2248 k_g \u03c3^g,\n\nwhere J is nucleation rate and G is crystal growth rate. S2\u2019s nominal low solubility increases the possible driving force, while its nominal low nucleation and high growth favor seeded growth. Rapidly imposing large \u03c3 can nevertheless make J dominate, explaining why direct or poorly coupled cooling generated many fines. Staged cooling is interpreted as limiting peak \u03c3 so that growth on existing particles competes successfully with secondary nucleation. Catalyst-dependent impurities can alter C*, k_n, k_g, surface poisoning, agglomeration, or breakage, which provides a plausible route for the observed catalyst\u2013particle-size coupling.\n\nRevisions, uncertainty, and unresolved alternatives\n\nThe campaign began with full-charge C1/S2 at moderate heating and direct cooling. Its purity and recovery were promising, but fines were marginally above specification. Tests of other catalysts, S1, lower reagent loading, lower solvent volume, reduced catalyst dose, extra holds, thermal cycling, and slower cooling showed that none of those changes alone reliably corrected fines. The decisive revision was the short/hot reaction plus high-temperature seeding and staged cooling demonstrated in batches 20\u201324.\n\nFinal-assay noise standard deviations were approximately 0.010 for crystal recovery, 0.010 for purity, and 0.018 for fines. Consequently, the 0.0003 recovery difference between batches 22 and 23 is not statistically meaningful, nor are the small recovery differences among batches 22\u201324. Batch 23 remains the sealed recommendation, but the evidence supports a broad near-optimal plateau rather than a precisely located temperature optimum. Its quality margins are much more convincing: purity was reported as 1.000 and fines 0.142, far from the respective 0.80 minimum and 0.50 maximum, even allowing for instrument noise.\n\nThe remaining recovery/quality tradeoff is unresolved at finer resolution. Cooling to 250 K improved recovery relative to batch 20 without sacrificing fines in batches 21\u201324, but still lower temperatures were unavailable, and longer optimized holds were not replicated under the final reaction condition. Exact replicates of batch 23 were not performed. Untested alternatives include varying seed mass or seed-addition temperature independently, optimizing each cooling-stage duration, changing agitation during crystallization, and using a designed temperature cycle under the final upstream composition. Because catalyst and solvent labels denote anonymous synthetic benchmark materials with fixed hidden residuals, the mechanism should be viewed as a process-level explanation of this campaign, not a claim about transferable real chemical identities."
  },
  "failure": null,
  "elapsed_s": 82.14000000001397,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 1186176,
    "input_tokens": 1297957,
    "output_tokens": 17176,
    "reasoning_output_tokens": 5733
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
          "estimate": 0.32,
          "lower80": 0.17,
          "upper80": 0.5
        },
        "crystal_purity": {
          "estimate": 0.965,
          "lower80": 0.9,
          "upper80": 0.995
        },
        "crystal_size": {
          "estimate": 0.115,
          "lower80": 0.065,
          "upper80": 0.18
        },
        "crystal_yield": {
          "estimate": 0.28,
          "lower80": 0.16,
          "upper80": 0.42
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q01"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.48,
          "lower80": 0.28,
          "upper80": 0.7
        },
        "crystal_purity": {
          "estimate": 0.935,
          "lower80": 0.84,
          "upper80": 0.985
        },
        "crystal_size": {
          "estimate": 0.09,
          "lower80": 0.045,
          "upper80": 0.15
        },
        "crystal_yield": {
          "estimate": 0.2,
          "lower80": 0.09,
          "upper80": 0.34
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q02"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.82,
          "lower80": 0.59,
          "upper80": 0.98
        },
        "crystal_purity": {
          "estimate": 0.9,
          "lower80": 0.78,
          "upper80": 0.97
        },
        "crystal_size": {
          "estimate": 0.045,
          "lower80": 0.015,
          "upper80": 0.095
        },
        "crystal_yield": {
          "estimate": 0.14,
          "lower80": 0.04,
          "upper80": 0.28
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q03"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.46,
          "lower80": 0.25,
          "upper80": 0.69
        },
        "crystal_purity": {
          "estimate": 0.92,
          "lower80": 0.81,
          "upper80": 0.98
        },
        "crystal_size": {
          "estimate": 0.1,
          "lower80": 0.05,
          "upper80": 0.17
        },
        "crystal_yield": {
          "estimate": 0.2,
          "lower80": 0.09,
          "upper80": 0.35
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q04"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.44,
          "lower80": 0.24,
          "upper80": 0.66
        },
        "crystal_purity": {
          "estimate": 0.92,
          "lower80": 0.81,
          "upper80": 0.98
        },
        "crystal_size": {
          "estimate": 0.1,
          "lower80": 0.05,
          "upper80": 0.17
        },
        "crystal_yield": {
          "estimate": 0.2,
          "lower80": 0.09,
          "upper80": 0.35
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q05"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.76,
          "lower80": 0.53,
          "upper80": 0.95
        },
        "crystal_purity": {
          "estimate": 0.89,
          "lower80": 0.75,
          "upper80": 0.97
        },
        "crystal_size": {
          "estimate": 0.06,
          "lower80": 0.025,
          "upper80": 0.12
        },
        "crystal_yield": {
          "estimate": 0.23,
          "lower80": 0.1,
          "upper80": 0.39
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q06"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.49,
          "lower80": 0.28,
          "upper80": 0.71
        },
        "crystal_purity": {
          "estimate": 0.91,
          "lower80": 0.79,
          "upper80": 0.98
        },
        "crystal_size": {
          "estimate": 0.09,
          "lower80": 0.045,
          "upper80": 0.155
        },
        "crystal_yield": {
          "estimate": 0.21,
          "lower80": 0.09,
          "upper80": 0.36
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q07"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.35,
          "lower80": 0.16,
          "upper80": 0.59
        },
        "crystal_purity": {
          "estimate": 0.94,
          "lower80": 0.84,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.12,
          "lower80": 0.06,
          "upper80": 0.2
        },
        "crystal_yield": {
          "estimate": 0.14,
          "lower80": 0.04,
          "upper80": 0.28
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q08"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.6,
          "lower80": 0.34,
          "upper80": 0.86
        },
        "crystal_purity": {
          "estimate": 0.94,
          "lower80": 0.8,
          "upper80": 0.995
        },
        "crystal_size": {
          "estimate": 0.07,
          "lower80": 0.025,
          "upper80": 0.14
        },
        "crystal_yield": {
          "estimate": 0.015,
          "lower80": 0.001,
          "upper80": 0.06
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q09"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.48,
          "lower80": 0.25,
          "upper80": 0.74
        },
        "crystal_purity": {
          "estimate": 0.93,
          "lower80": 0.8,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.085,
          "lower80": 0.035,
          "upper80": 0.16
        },
        "crystal_yield": {
          "estimate": 0.07,
          "lower80": 0.015,
          "upper80": 0.17
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q10"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.44,
          "lower80": 0.24,
          "upper80": 0.67
        },
        "crystal_purity": {
          "estimate": 0.92,
          "lower80": 0.81,
          "upper80": 0.98
        },
        "crystal_size": {
          "estimate": 0.1,
          "lower80": 0.05,
          "upper80": 0.17
        },
        "crystal_yield": {
          "estimate": 0.2,
          "lower80": 0.09,
          "upper80": 0.35
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q11"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.72,
          "lower80": 0.48,
          "upper80": 0.93
        },
        "crystal_purity": {
          "estimate": 0.88,
          "lower80": 0.73,
          "upper80": 0.97
        },
        "crystal_size": {
          "estimate": 0.06,
          "lower80": 0.025,
          "upper80": 0.12
        },
        "crystal_yield": {
          "estimate": 0.36,
          "lower80": 0.2,
          "upper80": 0.54
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q12"
      }
    ],
    "rationale": "All recipes contain seed, so particles are expected even where seed-excluded target recovery is very small. Q01\u2013Q02: S1 is predicted to outperform S3 because its lower nominal solubility and nucleation tendency, faster growth, and lower impurity occlusion favor greater recovery and a coarser, cleaner population. Q03\u2013Q04: increasing S0 seed from 0.001 to 0.045 g should suppress uncontrolled nucleation and provide more growth area, improving yield and fines, although S0 remains intrinsically unfavorable. Q05\u2013Q06: gradual cooling should strongly reduce fines relative to the 120-second crash; the long cold residence in Q06 may slightly increase recovery but is unlikely to erase the initial nucleation burst. Q07\u2013Q08: the 315 K temperature cycle is expected to dissolve preferentially small particles and improve size and fines, at the cost of unrecovered dissolved product after the relatively fast recool. Q09\u2013Q10: two hours at 292 K should increase seed-excluded deposition and modestly improve the particle distribution versus immediate filtration, but both predictions are especially uncertain because recovery is near zero. Q11\u2013Q12: doubling reagent concentration should increase fractional crystallization recovery, while the unchanged catalyst and seed charges raise impurity and nucleation risks, lowering purity and worsening fines. Intervals express epistemic 80% uncertainty for noise-free outcomes and are deliberately broad because these recipes use S0/S1/S3, much lower charge, unusually long cooling histories, and seed-to-product ratios not directly covered by the completed campaign; feasibility labels use the point estimates."
  },
  "failure": null,
  "elapsed_s": 82.59400000001187,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 1186176,
    "input_tokens": 1362288,
    "output_tokens": 21036,
    "reasoning_output_tokens": 7837
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
    "report": "1. Status of the main claims\n\nSupported by direct observations:\n\n- C1/S2 was the strongest observed catalyst\u2013solvent combination for particle quality. With otherwise related conditions, C1/S2 batches 7\u20138 gave fines near 0.53, whereas C3/S2 batch 6 and C0/S2 batch 18 gave fines near 1.00. Reducing C1 to 0.0025 mol in batch 17 also worsened recovery and fines. This directly supports a catalyst-dependent downstream effect, although the proposed impurity-mediated mechanism remains interpretive.\n- Shorter, hotter reaction histories improved the measured reaction packet. From batch 19 through batches 20, 22 and 23, increasing the realized reaction temperature while shortening exposure generally reduced byproduct/degradation signals and increased selectivity and reaction yield. Batch 23 reached selectivity 0.657 and reaction yield 0.657, versus roughly 0.44\u20130.47 selectivity under the earlier 370 K/3,600 s C1/S2 conditions. Batch 24 showed a plateau: greater heating did not improve crystallization-stage recovery.\n- The combined short/hot reaction and staged cooling produced the best observed recovery\u2013quality region. Batches 20\u201324 had recoveries of about 0.529\u20130.570 and fines of 0.118\u20130.215, whereas batches 7\u20138 and 13\u201316 generally had recoveries around 0.38\u20130.41 and fines around 0.53. Batch 21 also directly showed that extending the final cooling endpoint from 260 to 250 K could increase recovery without causing a fines failure under the improved upstream history.\n- Direct or poorly coupled cooling was inadequate in several cases. Batch 10 ended at 280 K with fines 1.00; batch 19 used the hotter reaction but essentially direct cooling and still gave fines 0.528; batch 14 used elaborate slow cooling with the older reaction history and gave fines 0.551. These observations support process-history dependence rather than a simple endpoint-temperature rule.\n- S1 did not deliver acceptable particle quality in the tested histories: batches 4 and 9 both had fines 1.00 despite recoveries near 0.47. Lower reagent loading in batch 11, lower solvent volume in batch 12, and reduced catalyst dose in batch 17 also failed to improve the joint objective.\n\nSupported only as interpretation:\n\n- The explanation that catalyst-dependent impurities altered nucleation, growth, surface poisoning or agglomeration is plausible but was not directly measured. The assays showed catalyst-dependent final behavior, not the microscopic route.\n- The proposal that high-temperature seeding conditioned or partially dissolved seeds before controlled regrowth is also interpretive. No particle measurement was made immediately after seed addition, and seed survival was not assayed.\n- The supersaturation model J\u2248k_n\u03c3^m and G\u2248k_g\u03c3^g is a useful organizing framework, but its parameters were not fitted. It explains the qualitative benefit of staged cooling without proving the operative exponent or rate-limiting event.\n\nContradicted or qualified:\n\n- A simple claim that slower cooling alone suppresses fines is contradicted by batch 14, where very gradual multistage cooling still produced fines 0.551. It must be qualified as an interaction with upstream composition and seed-entry history.\n- A simple claim that additional holding always improves fines is not supported. In batch 15, the intermediate particle readings changed only from 0.563 to 0.540 after a hold, and batch 16 did not show a reliable improvement after several holds.\n- The nominal solvent prior was not sufficient by itself. S1 had favorable nominal nucleation, growth and occlusion properties relative to S3/S0, yet tested S1 batches still had fines 1.00. Experimental history dominated the nominal ranking.\n\nStill untested:\n\n- Exact replication of batch 23 and independent estimation of process variability.\n- Separating reaction-temperature effects from seed-entry-temperature effects.\n- Separating staged cooling from the improved upstream composition without changing both together.\n- Independent seed-mass and seed-addition-temperature response curves.\n- Direct measurements of supersaturation, impurity adsorption, nucleation rate, seed dissolution or polymorph identity.\n- Whether the batch-22/23 plateau persists between the tested temperature points.\n\n2. One additional experiment\n\nI would repeat the batch-23 upstream recipe\u20140.040 mol reagent, 0.080 L S2, 0.005 mol C1, heating toward 450 K for 900 s at 600 rpm, quenching and adding 0.050 g seed\u2014but replace its staged cooling with one direct 14,400 s cool to 250 K followed by the same 14,400 s hold at 100 rpm, filtration and final assay. A pre-filtration particle-size measurement would be the most informative optional measurement.\n\nThis hybrid would use existing batches as controls: batch 23 represents hot/short reaction plus staged cooling, while batch 19 represents a less-hot reaction plus direct cooling. It would distinguish three explanations:\n\n- If the hybrid retained approximately batch-23 performance\u2014recovery around 0.55\u20130.57 and fines well below 0.50\u2014the upstream composition and high seed-entry temperature would be the dominant causes, with staging comparatively unimportant.\n- If recovery remained high but fines rose toward approximately 0.5\u20131.0, staged control of supersaturation would be essential for quality, while the upstream reaction would primarily determine available target and recovery.\n- If both recovery and quality deteriorated, the result would support a genuine interaction: the improved reaction packet would be useful only when coupled to staged cooling.\n\nThis single experiment would not completely separate reaction composition from seed-entry temperature, but it would resolve the largest present ambiguity more efficiently than another incremental temperature optimization.\n\n3. Least effectively used observation and least reliable prediction\n\nThe account used batch 8 least effectively. Batch 8 applied a 285 K heating cycle after crystallization and then recooled, yet its final recovery (0.408) and fines (0.528) were essentially no better than related non-cycled C1/S2 batches. I mentioned this negative result but still treated thermal cycling mainly through the favorable textbook mechanism of preferential fines dissolution. The evidence should have prompted stronger caution that reheating may merely redissolve product, fail to discriminate particle sizes, or generate new fines during recooling.\n\nFor the same reason, Q08 is the least reliable held-out prediction. I predicted that its 315 K cycle would improve size and fines while sacrificing recovery relative to Q07. That direction is mechanistically plausible, but it extrapolates far beyond batch 8: Q08 uses S0, much lower reagent and catalyst charges, a different seed-to-product ratio, an extremely long prior cooling history, a much hotter dissolution step, and a rapid 3,600 s recool. The cycle might instead dissolve most newly deposited target, leave seed-dominated particles, or trigger a fresh nucleation burst. Thus even the sign of its fines change relative to Q07 is uncertain. Q09 is also highly uncertain because its predicted recovery is near zero, but Q08 is less reliable mechanistically because its central directional claim rests on an intervention that did not improve the closest observed campaign batch."
  },
  "failure": null,
  "elapsed_s": 50.5,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 1238400,
    "input_tokens": 1430399,
    "output_tokens": 23001,
    "reasoning_output_tokens": 8244
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
    "selection_rationale": "Highest observed seed-excluded crystal recovery (0.5699) among completed batches while meeting purity (1.000) and fines (0.142) constraints."
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
        "duration_s": 900,
        "operation": "heat",
        "stirring_speed_rpm": 600,
        "target_temperature_K": 450
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
        "target_temperature_K": 310
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
    "excluded_rejected_attempts": [
      {
        "action": {
          "duration_s": 14400,
          "operation": "cool_crystallize",
          "target_temperature_K": 340
        },
        "status": "validation_failed",
        "step": 295
      }
    ],
    "lifecycle_index": 23,
    "source_attempts": 14
  },
  "prediction_evaluation": {
    "contrasts": [
      {
        "absolute_delta_error": 0.12922312168225358,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_yield",
        "predicted_delta": -0.08000000000000002,
        "resolved": true,
        "true_delta": -0.2092231216822536
      },
      {
        "absolute_delta_error": 0.02985222850427094,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_purity",
        "predicted_delta": -0.029999999999999916,
        "resolved": false,
        "true_delta": -0.00014777149572897663
      },
      {
        "absolute_delta_error": 0.03211719918353845,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_size",
        "predicted_delta": -0.02500000000000001,
        "resolved": true,
        "true_delta": 0.007117199183538439
      },
      {
        "absolute_delta_error": 0.4366162319398145,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.15999999999999998,
        "resolved": true,
        "true_delta": -0.27661623193981455
      },
      {
        "absolute_delta_error": 0.060132329809087864,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_yield",
        "predicted_delta": 0.06,
        "resolved": false,
        "true_delta": -0.00013232980908786662
      },
      {
        "absolute_delta_error": 0.010843604737075685,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_purity",
        "predicted_delta": 0.020000000000000018,
        "resolved": false,
        "true_delta": 0.009156395262924333
      },
      {
        "absolute_delta_error": 0.059979439079870495,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_size",
        "predicted_delta": 0.05500000000000001,
        "resolved": false,
        "true_delta": -0.004979439079870487
      },
      {
        "absolute_delta_error": 0.4934195253798535,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.35999999999999993,
        "resolved": true,
        "true_delta": 0.13341952537985358
      },
      {
        "absolute_delta_error": 0.029566479132169532,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_yield",
        "predicted_delta": 0.03,
        "resolved": false,
        "true_delta": 0.00043352086783046695
      },
      {
        "absolute_delta_error": 0.02622786682503797,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.030000000000000027,
        "resolved": false,
        "true_delta": -0.0037721331749620557
      },
      {
        "absolute_delta_error": 0.003838868836988675,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_size",
        "predicted_delta": -0.04000000000000001,
        "resolved": true,
        "true_delta": -0.04383886883698868
      },
      {
        "absolute_delta_error": 0.29381528795023254,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.32,
        "resolved": true,
        "true_delta": 0.6138152879502325
      },
      {
        "absolute_delta_error": 0.11304184008830012,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_yield",
        "predicted_delta": -0.06999999999999998,
        "resolved": true,
        "true_delta": 0.04304184008830014
      },
      {
        "absolute_delta_error": 0.040377514631150246,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_purity",
        "predicted_delta": 0.029999999999999916,
        "resolved": true,
        "true_delta": -0.01037751463115033
      },
      {
        "absolute_delta_error": 0.0698553530173099,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_size",
        "predicted_delta": 0.03,
        "resolved": true,
        "true_delta": -0.0398553530173099
      },
      {
        "absolute_delta_error": 0.7899421779987409,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.14,
        "resolved": true,
        "true_delta": 0.6499421779987409
      },
      {
        "absolute_delta_error": 0.05114975880452932,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_yield",
        "predicted_delta": 0.05500000000000001,
        "resolved": true,
        "true_delta": 0.10614975880452933
      },
      {
        "absolute_delta_error": 0.0022800208771959207,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_purity",
        "predicted_delta": -0.009999999999999898,
        "resolved": true,
        "true_delta": -0.012280020877195819
      },
      {
        "absolute_delta_error": 0.0022741883094254053,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_size",
        "predicted_delta": 0.015,
        "resolved": true,
        "true_delta": 0.012725811690574594
      },
      {
        "absolute_delta_error": 0.16253026625748246,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.12,
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
        "absolute_delta_error": 0.03489031320205482,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_purity",
        "predicted_delta": -0.040000000000000036,
        "resolved": false,
        "true_delta": -0.005109686797945212
      },
      {
        "absolute_delta_error": 0.01166160161035517,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_size",
        "predicted_delta": -0.04000000000000001,
        "resolved": true,
        "true_delta": -0.028338398389644838
      },
      {
        "absolute_delta_error": 0.322412437007269,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.27999999999999997,
        "resolved": true,
        "true_delta": 0.602412437007269
      }
    ],
    "failures": [],
    "metrics": {
      "crystal_fines_fraction": {
        "coverage80": 0.3333333333333333,
        "interval_score80": 1.8490221173130799,
        "interval_width": 0.43083333333333335,
        "mae": 0.313930922261704,
        "n": 12,
        "planned": 12
      },
      "crystal_purity": {
        "coverage80": 0.25,
        "interval_score80": 0.23210965043652965,
        "interval_width": 0.1770833333333333,
        "mae": 0.06483044883320131,
        "n": 12,
        "planned": 12
      },
      "crystal_size": {
        "coverage80": 0.8333333333333334,
        "interval_score80": 0.12211680921830924,
        "interval_width": 0.11166666666666668,
        "mae": 0.027135552619970357,
        "n": 12,
        "planned": 12
      },
      "crystal_yield": {
        "coverage80": 0.9166666666666666,
        "interval_score80": 0.24630985996439955,
        "interval_width": 0.24033333333333337,
        "mae": 0.05933212096072755,
        "n": 12,
        "planned": 12
      }
    },
    "quality": {
      "balanced_accuracy": 0.6142857142857143,
      "false_negative": 1,
      "false_positive": 4,
      "true_negative": 3,
      "true_positive": 4
    },
    "resolved_direction_correct": 7,
    "resolved_direction_n": 15,
    "tie_correct": 0,
    "tie_n": 9,
    "valid": true
  },
  "public_baselines": {
    "available": true,
    "mae": {
      "public_mean": {
        "crystal_fines_fraction": 0.2944410323572612,
        "crystal_purity": 0.004392535203343438,
        "crystal_size": 0.018722049819314687,
        "crystal_yield": 0.21206764188396457
      },
      "public_nearest_neighbor": {
        "crystal_fines_fraction": 0.24654030697952736,
        "crystal_purity": 0.016120474687610548,
        "crystal_size": 0.027213961593126376,
        "crystal_yield": 0.18254525767751062
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
        "cached_input": 1186176,
        "input": 1245539,
        "output": 13799,
        "stage": "source",
        "uncached_input": 59363
      },
      {
        "cached_input": 0,
        "input": 52418,
        "output": 3377,
        "stage": "K1",
        "uncached_input": 52418
      },
      {
        "cached_input": 0,
        "input": 64331,
        "output": 3860,
        "stage": "Q",
        "uncached_input": 64331
      },
      {
        "cached_input": 52224,
        "input": 68111,
        "output": 1965,
        "stage": "K2",
        "uncached_input": 15887
      }
    ],
    "total": {
      "cached_input": 1238400,
      "input": 1430399,
      "input_plus_output": 1453400,
      "output": 23001,
      "uncached_input": 191999
    },
    "valid": true
  },
  "elapsed_s": 741.0310000000172
}
```
