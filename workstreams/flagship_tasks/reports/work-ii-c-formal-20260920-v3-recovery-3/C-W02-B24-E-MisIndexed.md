# C-W02-B24-E-MisIndexed

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
      "operation": "seed_crystals",
      "seed_mass_g": 0.02
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 7200,
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
  "end_step": 11,
  "lifecycle_index": 1,
  "metrics": {
    "byproduct_signal": 0.34614425897598267,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7570005655288696,
    "crystal_fines_fraction": 0.29242759943008423,
    "crystal_purity": 0.9904960989952087,
    "crystal_size": 0.08346983045339584,
    "crystal_yield": 0.4389331638813019,
    "degradation_warning": 0.1701538860797882,
    "safety_risk": 0.18189206719398499,
    "score": 0.5114104151725769,
    "selectivity": 0.5184647440910339,
    "virtual_spectrum_summary": 0.2669485807418823,
    "yield": 0.516302227973938
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
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 7200,
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
  "end_step": 22,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.3015795350074768,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7170988917350769,
    "crystal_fines_fraction": 0.44527146220207214,
    "crystal_purity": 0.9809387922286987,
    "crystal_size": 0.10881602019071579,
    "crystal_yield": 0.48537400364875793,
    "degradation_warning": 0.1220536157488823,
    "safety_risk": 0.18815824389457703,
    "score": 0.509800910949707,
    "selectivity": 0.5769917368888855,
    "virtual_spectrum_summary": 0.22079285979270935,
    "yield": 0.5655467510223389
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
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 7200,
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
  "end_step": 33,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.3798066973686218,
    "conversion": 0.9983178973197937,
    "cost": 1.0,
    "crystal_csd_quality": 0.7184330821037292,
    "crystal_fines_fraction": 0.34715789556503296,
    "crystal_purity": 0.9886212348937988,
    "crystal_size": 0.07365093380212784,
    "crystal_yield": 0.2940409481525421,
    "degradation_warning": 0.10278643667697906,
    "safety_risk": 0.16336530447006226,
    "score": 0.43438801169395447,
    "selectivity": 0.371631383895874,
    "virtual_spectrum_summary": 0.2551475763320923,
    "yield": 0.37074410915374756
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
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 7200,
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
  "end_step": 44,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.3697880506515503,
    "conversion": 0.9889965057373047,
    "cost": 1.0,
    "crystal_csd_quality": 0.743460476398468,
    "crystal_fines_fraction": 0.35580217838287354,
    "crystal_purity": 1.0,
    "crystal_size": 0.08331621438264847,
    "crystal_yield": 0.39735808968544006,
    "degradation_warning": 0.1524174064397812,
    "safety_risk": 0.17493167519569397,
    "score": 0.4824256896972656,
    "selectivity": 0.46429169178009033,
    "virtual_spectrum_summary": 0.2719712555408478,
    "yield": 0.4506620466709137
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 340
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
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 7200,
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
  "end_step": 55,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.4446716904640198,
    "conversion": 0.996337890625,
    "cost": 1.0,
    "crystal_csd_quality": 0.7066253423690796,
    "crystal_fines_fraction": 0.4469389021396637,
    "crystal_purity": 0.9792458415031433,
    "crystal_size": 0.05839570239186287,
    "crystal_yield": 0.33900097012519836,
    "degradation_warning": 0.22212180495262146,
    "safety_risk": 0.16848179697990417,
    "score": 0.4377656877040863,
    "selectivity": 0.41912704706192017,
    "virtual_spectrum_summary": 0.34452423453330994,
    "yield": 0.412974089384079
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
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 7200,
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
  "end_step": 66,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.24613340198993683,
    "conversion": 0.9924279451370239,
    "cost": 1.0,
    "crystal_csd_quality": 0.5537129640579224,
    "crystal_fines_fraction": 0.7301525473594666,
    "crystal_purity": 0.9930415153503418,
    "crystal_size": 0.043241120874881744,
    "crystal_yield": 0.5482345223426819,
    "degradation_warning": 0.09217434376478195,
    "safety_risk": 0.15335224568843842,
    "score": 0.47697168588638306,
    "selectivity": 0.6468899250030518,
    "virtual_spectrum_summary": 0.17685182392597198,
    "yield": 0.6487718820571899
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
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 7200,
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
  "end_step": 77,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.2529957890510559,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6390756964683533,
    "crystal_fines_fraction": 0.5653017163276672,
    "crystal_purity": 0.9763221740722656,
    "crystal_size": 0.08850008994340897,
    "crystal_yield": 0.5636159777641296,
    "degradation_warning": 0.09651566296815872,
    "safety_risk": 0.1771533340215683,
    "score": 0.5104129910469055,
    "selectivity": 0.609870970249176,
    "virtual_spectrum_summary": 0.18257972598075867,
    "yield": 0.6365180015563965
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
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 7200,
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
  "end_step": 88,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.32647913694381714,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6378244161605835,
    "crystal_fines_fraction": 0.6034401655197144,
    "crystal_purity": 0.9677114486694336,
    "crystal_size": 0.10016191750764847,
    "crystal_yield": 0.4152308702468872,
    "degradation_warning": 0.1207229346036911,
    "safety_risk": 0.18813195824623108,
    "score": 0.44245535135269165,
    "selectivity": 0.496878445148468,
    "virtual_spectrum_summary": 0.23388884961605072,
    "yield": 0.4885731041431427
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
      "target_temperature_K": 350
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
  "end_step": 99,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.2739136815071106,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.646166205406189,
    "crystal_fines_fraction": 0.5726507902145386,
    "crystal_purity": 0.9792384505271912,
    "crystal_size": 0.0551312193274498,
    "crystal_yield": 0.5402312278747559,
    "degradation_warning": 0.10731726139783859,
    "safety_risk": 0.17568424344062805,
    "score": 0.5032328367233276,
    "selectivity": 0.6219562888145447,
    "virtual_spectrum_summary": 0.1989452838897705,
    "yield": 0.6356322169303894
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
      "target_temperature_K": 350
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 280
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
  "end_step": 110,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.2667907774448395,
    "conversion": 0.9858242273330688,
    "cost": 1.0,
    "crystal_csd_quality": 0.6188141107559204,
    "crystal_fines_fraction": 0.5861778259277344,
    "crystal_purity": 0.9746589660644531,
    "crystal_size": 0.06920958310365677,
    "crystal_yield": 0.5413482785224915,
    "degradation_warning": 0.11872360855340958,
    "safety_risk": 0.17511670291423798,
    "score": 0.4952237010002136,
    "selectivity": 0.6163849830627441,
    "virtual_spectrum_summary": 0.20016056299209595,
    "yield": 0.6253117918968201
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
      "target_temperature_K": 350
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
  "end_step": 121,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.2652326226234436,
    "conversion": 0.9990203380584717,
    "cost": 1.0,
    "crystal_csd_quality": 0.6214467287063599,
    "crystal_fines_fraction": 0.5742367506027222,
    "crystal_purity": 0.9900637865066528,
    "crystal_size": 0.07488115131855011,
    "crystal_yield": 0.5692296624183655,
    "degradation_warning": 0.0865478441119194,
    "safety_risk": 0.17968985438346863,
    "score": 0.5121071338653564,
    "selectivity": 0.6593309044837952,
    "virtual_spectrum_summary": 0.18482446670532227,
    "yield": 0.6398410201072693
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
      "target_temperature_K": 350
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
  "end_step": 132,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.2668226957321167,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6523122787475586,
    "crystal_fines_fraction": 0.5712400078773499,
    "crystal_purity": 0.991040050983429,
    "crystal_size": 0.09535031020641327,
    "crystal_yield": 0.5089378356933594,
    "degradation_warning": 0.12456001341342926,
    "safety_risk": 0.1724483221769333,
    "score": 0.5000466704368591,
    "selectivity": 0.6100186705589294,
    "virtual_spectrum_summary": 0.20280449092388153,
    "yield": 0.6150606870651245
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
      "catalyst": 0,
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
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
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
  "end_step": 143,
  "lifecycle_index": 13,
  "metrics": {
    "byproduct_signal": 0.2932060956954956,
    "conversion": 0.9972169399261475,
    "cost": 1.0,
    "crystal_csd_quality": 0.7087475061416626,
    "crystal_fines_fraction": 0.4474799931049347,
    "crystal_purity": 0.9798984527587891,
    "crystal_size": 0.07967458665370941,
    "crystal_yield": 0.5165097713470459,
    "degradation_warning": 0.12320584803819656,
    "safety_risk": 0.1912059783935547,
    "score": 0.5151382684707642,
    "selectivity": 0.5897796154022217,
    "virtual_spectrum_summary": 0.21670597791671753,
    "yield": 0.5817670822143555
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
      "catalyst": 0,
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
      "seed_mass_g": 0.01
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
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
  "end_step": 154,
  "lifecycle_index": 14,
  "metrics": {
    "byproduct_signal": 0.30751916766166687,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7192337512969971,
    "crystal_fines_fraction": 0.46892642974853516,
    "crystal_purity": 0.9628522396087646,
    "crystal_size": 0.11546608805656433,
    "crystal_yield": 0.521438717842102,
    "degradation_warning": 0.12813147902488708,
    "safety_risk": 0.19064706563949585,
    "score": 0.5124656558036804,
    "selectivity": 0.5665262937545776,
    "virtual_spectrum_summary": 0.22679470479488373,
    "yield": 0.5603388547897339
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
      "catalyst": 0,
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
  "end_step": 165,
  "lifecycle_index": 15,
  "metrics": {
    "byproduct_signal": 0.3041728138923645,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6800788044929504,
    "crystal_fines_fraction": 0.453657865524292,
    "crystal_purity": 0.9861031770706177,
    "crystal_size": 0.09133598208427429,
    "crystal_yield": 0.5088664293289185,
    "degradation_warning": 0.12381856143474579,
    "safety_risk": 0.19021493196487427,
    "score": 0.5088406205177307,
    "selectivity": 0.5783542990684509,
    "virtual_spectrum_summary": 0.22301340103149414,
    "yield": 0.5828889012336731
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
      "catalyst": 0,
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
      "seed_mass_g": 0.01
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 280
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
  "end_step": 176,
  "lifecycle_index": 16,
  "metrics": {
    "byproduct_signal": 0.30740076303482056,
    "conversion": 0.9885537624359131,
    "cost": 1.0,
    "crystal_csd_quality": 0.675674319267273,
    "crystal_fines_fraction": 0.4262295067310333,
    "crystal_purity": 0.9753075242042542,
    "crystal_size": 0.08481423556804657,
    "crystal_yield": 0.47978997230529785,
    "degradation_warning": 0.14443644881248474,
    "safety_risk": 0.18665854632854462,
    "score": 0.4943868815898895,
    "selectivity": 0.5495601296424866,
    "virtual_spectrum_summary": 0.23406681418418884,
    "yield": 0.5479147434234619
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
      "target_temperature_K": 350
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
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 150,
      "target_temperature_K": 290
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
    },
    {
      "duration_s": 7200,
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
  "end_step": 189,
  "lifecycle_index": 17,
  "metrics": {
    "byproduct_signal": 0.26575276255607605,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6288235187530518,
    "crystal_fines_fraction": 0.5582799315452576,
    "crystal_purity": 0.9957635998725891,
    "crystal_size": 0.06989819556474686,
    "crystal_yield": 0.5813448429107666,
    "degradation_warning": 0.10408451408147812,
    "safety_risk": 0.1791490614414215,
    "score": 0.5160881876945496,
    "selectivity": 0.6245319843292236,
    "virtual_spectrum_summary": 0.19300204515457153,
    "yield": 0.6346901655197144
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
      "target_temperature_K": 350
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
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 150,
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
    },
    {
      "duration_s": 7200,
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
  "end_step": 202,
  "lifecycle_index": 18,
  "metrics": {
    "byproduct_signal": 0.24285897612571716,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6434878706932068,
    "crystal_fines_fraction": 0.6073343753814697,
    "crystal_purity": 0.9914769530296326,
    "crystal_size": 0.1211392804980278,
    "crystal_yield": 0.5676143169403076,
    "degradation_warning": 0.10307163745164871,
    "safety_risk": 0.17875094711780548,
    "score": 0.515781044960022,
    "selectivity": 0.6266670823097229,
    "virtual_spectrum_summary": 0.1799546778202057,
    "yield": 0.6400740146636963
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
      "target_temperature_K": 350
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
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 150,
      "target_temperature_K": 310
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
    },
    {
      "duration_s": 7200,
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
  "end_step": 215,
  "lifecycle_index": 19,
  "metrics": {
    "byproduct_signal": 0.26832789182662964,
    "conversion": 0.9909035563468933,
    "cost": 1.0,
    "crystal_csd_quality": 0.6368340849876404,
    "crystal_fines_fraction": 0.5669126510620117,
    "crystal_purity": 0.9702534079551697,
    "crystal_size": 0.05927049368619919,
    "crystal_yield": 0.5725839734077454,
    "degradation_warning": 0.10208265483379364,
    "safety_risk": 0.17820441722869873,
    "score": 0.5069761276245117,
    "selectivity": 0.6218330264091492,
    "virtual_spectrum_summary": 0.1935175359249115,
    "yield": 0.6254197955131531
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
      "target_temperature_K": 350
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
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 150,
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
    },
    {
      "duration_s": 7200,
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
  "end_step": 228,
  "lifecycle_index": 20,
  "metrics": {
    "byproduct_signal": 0.27214890718460083,
    "conversion": 0.9934655427932739,
    "cost": 1.0,
    "crystal_csd_quality": 0.611929178237915,
    "crystal_fines_fraction": 0.6002426743507385,
    "crystal_purity": 0.988970160484314,
    "crystal_size": 0.07256991416215897,
    "crystal_yield": 0.5580793023109436,
    "degradation_warning": 0.1119857132434845,
    "safety_risk": 0.177473783493042,
    "score": 0.4988219141960144,
    "selectivity": 0.6276543140411377,
    "virtual_spectrum_summary": 0.20007547736167908,
    "yield": 0.6113325357437134
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
      "volume_L": 0.04
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
      "target_temperature_K": 350
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
  "end_step": 239,
  "lifecycle_index": 21,
  "metrics": {
    "byproduct_signal": 0.27934592962265015,
    "conversion": 0.9894089102745056,
    "cost": 1.0,
    "crystal_csd_quality": 0.5307031273841858,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9952429533004761,
    "crystal_size": 0.046147070825099945,
    "crystal_yield": 0.5408695936203003,
    "degradation_warning": 0.12321607023477554,
    "safety_risk": 0.22497348487377167,
    "score": 0.42816707491874695,
    "selectivity": 0.573662519454956,
    "virtual_spectrum_summary": 0.20908749103546143,
    "yield": 0.5929397344589233
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
      "volume_L": 0.06
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
      "target_temperature_K": 350
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
  "end_step": 250,
  "lifecycle_index": 22,
  "metrics": {
    "byproduct_signal": 0.3046058118343353,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6963832974433899,
    "crystal_fines_fraction": 0.4273470938205719,
    "crystal_purity": 1.0,
    "crystal_size": 0.07746142148971558,
    "crystal_yield": 0.5244851112365723,
    "degradation_warning": 0.12504765391349792,
    "safety_risk": 0.19950012862682343,
    "score": 0.5176488757133484,
    "selectivity": 0.5709248185157776,
    "virtual_spectrum_summary": 0.22380463778972626,
    "yield": 0.5722036957740784
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
      "volume_L": 0.04
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
      "target_temperature_K": 350
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
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
  "end_step": 262,
  "lifecycle_index": 23,
  "metrics": {
    "byproduct_signal": 0.3024172782897949,
    "conversion": 0.9950222373008728,
    "cost": 1.0,
    "crystal_csd_quality": 0.7019369006156921,
    "crystal_fines_fraction": 0.42463818192481995,
    "crystal_purity": 1.0,
    "crystal_size": 0.09490804374217987,
    "crystal_yield": 0.5233290195465088,
    "degradation_warning": 0.12005212157964706,
    "safety_risk": 0.22497348487377167,
    "score": 0.5221409201622009,
    "selectivity": 0.5885857343673706,
    "virtual_spectrum_summary": 0.22035296261310577,
    "yield": 0.5903440117835999
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
      "volume_L": 0.06
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
      "target_temperature_K": 350
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
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
  "end_step": 274,
  "lifecycle_index": 24,
  "metrics": {
    "byproduct_signal": 0.3019067049026489,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6649328470230103,
    "crystal_fines_fraction": 0.5203348398208618,
    "crystal_purity": 1.0,
    "crystal_size": 0.07238145917654037,
    "crystal_yield": 0.5130835771560669,
    "degradation_warning": 0.12072357535362244,
    "safety_risk": 0.1984623372554779,
    "score": 0.49869659543037415,
    "selectivity": 0.5652379989624023,
    "virtual_spectrum_summary": 0.22037430107593536,
    "yield": 0.5744878649711609
  },
  "ordinal": 24
}
```

## K1

```json
{
  "payload": {
    "report": "Mechanistic account\n\nRecommended process (sealed batch 22)\nCharge 0.040 mol reagent in 0.060 L solvent-S2 with 0.005 mol catalyst-C0. Heat at 350 K for 3,600 s with 600 rpm stirring, add 0.050 g seed, cool to 250 K over 14,400 s, age for 14,400 s at 150 rpm, and filter. Its final assay gave seed-excluded crystal recovery 0.5245, crystal purity 1.000, and fines number fraction 0.4273. The preceding particle-size measurement independently reported fines 0.4387. Thus both observed fines values were below the 0.50 limit.\n\nMaterial effects\n\nObservation: In the approximate catalyst screen using S2, C0 was superior. Batch 2 (C0, 350 K) gave reaction yield 0.5655 and crystal recovery 0.4854. C2 in batch 3 gave 0.3707 and 0.2940, while C3 in batch 4 gave 0.4507 and 0.3974. C1 gave recovery 0.4389 in batch 1 at 370 K and 0.3390 in batch 5 at 340 K with a longer reaction. These are not perfectly matched comparisons, but they motivated the revision from the initially selected C1 to C0.\n\nInterpretation: The fixed-world activity/selectivity residual for C0 appears favorable despite its less impressive nominal activity dossier. C2 especially promoted conversion without corresponding target selectivity: batch 3 had conversion about 0.998 but selectivity only about 0.372. Conversion alone was therefore a poor optimization signal.\n\nObservation: Solvent strongly separated recovery from particle quality. With C0 and otherwise similar processing, S0 in batch 6 and S1 in batch 7 gave high crystal recoveries, 0.5482 and 0.5636, but failed the fines constraint at 0.7302 and 0.5653. S3 in batch 8 gave lower recovery, 0.4152, and also failed on fines at 0.6034. S2 in batch 2 gave lower recovery than S0/S1 but was compliant: 0.4854 recovery and 0.4453 fines.\n\nInterpretation: This agrees qualitatively with the nominal material dossier. S2 has relatively low solubility and nucleation tendency, high crystal-growth tendency, and low impurity occlusion. It therefore appears to create fewer new particles while directing supersaturation into growth on existing crystals. S0 and S1 produced more target in the reaction\u2014final reaction yields were about 0.649 and 0.637 in batches 6 and 7\u2014but their crystallization histories produced too many sub-20-micrometre particles.\n\nReaction\u2013crystallization coupling\n\nA useful mass-balance decomposition is\n\nn(target before separation) = n(reagent charged) X S,\n\nn(seed-excluded recovered target) = Yc n(target before separation),\n\nso the approximate overall recovered target relative to charge is X S Yc. Here X is conversion, S is reaction selectivity, and Yc is the reported crystal recovery. Importantly, the campaign objective used Yc, not X S Yc. A process may therefore have excellent crystallization recovery while making relatively little target overall.\n\nThe experiments also show purification during crystallization. Reaction selectivities were only roughly 0.37\u20130.66, yet final crystal purities were generally 0.96\u20131.00. For example, batch 3 had final reaction selectivity about 0.372 but crystal purity 0.989. I interpret this as preferential incorporation of target into the S2 crystal phase and rejection of much of the reaction impurity into mother liquor. Purity was consequently much less restrictive than particle quality in this campaign.\n\nA qualitative crystallization model is useful:\n\nsigma = (C - C*)/C*,   nucleation rate B proportional to sigma^b,   growth rate G proportional to sigma^g.\n\nSolvent identity, liquid volume, cooling trajectory, and temperature history change C*, sigma, and the balance B/G. High instantaneous supersaturation can raise recovery but create excessive nuclei and fines; slower or staged generation of supersaturation can preserve recovery while allowing growth on existing particles.\n\nProcess-history dependence\n\nThe strongest history effect was observed at low S2 volume. Batch 21 used 0.040 L S2 and direct cooling to 250 K. It achieved recovery 0.5409 but a fines fraction of 1.000, consistent with a supersaturation burst. Batch 23 used the same 0.040 L volume but inserted a 7,200 s stage at 310 K before cooling to 250 K. It gave nearly the same recovery, 0.5233, while reducing final fines to 0.4246. Thus composition alone did not determine the result; the path through temperature\u2013supersaturation space mattered substantially.\n\nAt 0.060 L S2, batch 22 achieved 0.5245 recovery and 0.4273 fines without the intermediate cooling stage. This suggests that modest dilution itself moderated the supersaturation trajectory sufficiently. At 0.080 L S2, batches 13\u201315 were also compliant but had recoveries of 0.5165, 0.5214, and 0.5089. The observed optimum therefore lay near 0.04\u20130.06 L, provided nucleation was controlled by either dilution or staging.\n\nSeed amount had a weaker, unresolved effect. At 0.080 L S2 and 250 K, batch 13 used 0.050 g seed and gave 0.5165 recovery/0.4475 fines; batch 14 used 0.010 g and gave 0.5214/0.4689. The differences are small relative to assay noise and do not establish a monotonic seed law. Batch 24 combined 0.010 g seed with staged cooling at 0.060 L and narrowly failed at 0.5203 fines, but this comparison changes both seed and cooling history.\n\nRevisions during the study\n\nThe initial process used the nominally active C1 with S2 (batch 1). Catalyst screening redirected the work toward C0. Solvent screening then showed that the highest-recovery S0/S1 experiments violated the fines limit, so optimization shifted from reaction yield toward particle-population control. Changes in S1 seed dose and final temperature in batches 9\u201312 did not solve the problem: fines remained about 0.571\u20130.586. Reheat/recool or ripening trials in batches 17\u201320 raised recovery as high as 0.5813 but still left fines at 0.558\u20130.607. The program therefore returned to S2, where batches 13\u201316 established a robust compliant region, and finally varied solvent volume and cooling history in batches 21\u201324. Batch 22 was selected as the highest observed compliant recovery.\n\nQuality/recovery tradeoff and uncertainty\n\nThe unresolved tradeoff is clear: S0/S1 and several S1 recycle histories reached recovery of roughly 0.55\u20130.58, but their fines fractions exceeded 0.50. S2 reduced fines reliably, at the cost of some recovery. Low-volume S2 can recover more material but becomes highly sensitive to cooling history, as batch 21 demonstrates.\n\nBatch 22 and batch 23 are effectively tied in recovery: 0.5245 versus 0.5233, a difference far below the final-assay crystal-yield noise scale of about 0.01. Batch 22 nevertheless has the highest compliant point estimate and two fines observations below the limit. Its final fines margin is about 0.073, appreciably larger than the instrument noise scale of 0.018; purity has a large margin, although the reported value was clipped at 1.000. Exact recipes were not replicated, so process variability cannot be separated from measurement noise. Several comparisons also confound temperature, seed, or reaction conditions.\n\nUntested alternatives include a replicated factorial study around 0.050\u20130.070 L S2, seed loads between 0.02 and 0.05 g, and staged cooling near 300\u2013315 K; continuous cooling-rate control; and systematic agitation/aging optimization. These might determine whether batch 23's staged low-volume route truly matches batch 22 or merely benefited from random variation. They are plausible hypotheses rather than demonstrated improvements, and they do not alter the sealed recommendation."
  },
  "failure": null,
  "elapsed_s": 65.14100000000326,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 469632,
    "input_tokens": 533994,
    "output_tokens": 8073,
    "reasoning_output_tokens": 2808
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
          "estimate": 0.38,
          "lower80": 0.23,
          "upper80": 0.55
        },
        "crystal_purity": {
          "estimate": 0.965,
          "lower80": 0.91,
          "upper80": 0.995
        },
        "crystal_size": {
          "estimate": 0.2,
          "lower80": 0.1,
          "upper80": 0.32
        },
        "crystal_yield": {
          "estimate": 0.36,
          "lower80": 0.22,
          "upper80": 0.5
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q01"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.28,
          "lower80": 0.15,
          "upper80": 0.44
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.94,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.25,
          "lower80": 0.13,
          "upper80": 0.39
        },
        "crystal_yield": {
          "estimate": 0.32,
          "lower80": 0.18,
          "upper80": 0.46
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q02"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.62,
          "lower80": 0.45,
          "upper80": 0.79
        },
        "crystal_purity": {
          "estimate": 0.94,
          "lower80": 0.86,
          "upper80": 0.985
        },
        "crystal_size": {
          "estimate": 0.11,
          "lower80": 0.04,
          "upper80": 0.22
        },
        "crystal_yield": {
          "estimate": 0.38,
          "lower80": 0.23,
          "upper80": 0.53
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q03"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.4,
          "lower80": 0.24,
          "upper80": 0.57
        },
        "crystal_purity": {
          "estimate": 0.95,
          "lower80": 0.88,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.22,
          "lower80": 0.11,
          "upper80": 0.35
        },
        "crystal_yield": {
          "estimate": 0.4,
          "lower80": 0.26,
          "upper80": 0.54
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q04"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.36,
          "lower80": 0.21,
          "upper80": 0.53
        },
        "crystal_purity": {
          "estimate": 0.95,
          "lower80": 0.88,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.24,
          "lower80": 0.12,
          "upper80": 0.38
        },
        "crystal_yield": {
          "estimate": 0.41,
          "lower80": 0.27,
          "upper80": 0.55
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q05"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.55,
          "lower80": 0.38,
          "upper80": 0.72
        },
        "crystal_purity": {
          "estimate": 0.94,
          "lower80": 0.86,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.16,
          "lower80": 0.07,
          "upper80": 0.29
        },
        "crystal_yield": {
          "estimate": 0.42,
          "lower80": 0.28,
          "upper80": 0.56
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q06"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.34,
          "lower80": 0.19,
          "upper80": 0.51
        },
        "crystal_purity": {
          "estimate": 0.95,
          "lower80": 0.88,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.25,
          "lower80": 0.13,
          "upper80": 0.4
        },
        "crystal_yield": {
          "estimate": 0.42,
          "lower80": 0.28,
          "upper80": 0.56
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q07"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.3,
          "lower80": 0.16,
          "upper80": 0.48
        },
        "crystal_purity": {
          "estimate": 0.97,
          "lower80": 0.91,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.28,
          "lower80": 0.14,
          "upper80": 0.45
        },
        "crystal_yield": {
          "estimate": 0.34,
          "lower80": 0.19,
          "upper80": 0.49
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q08"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.7,
          "lower80": 0.5,
          "upper80": 0.87
        },
        "crystal_purity": {
          "estimate": 0.92,
          "lower80": 0.8,
          "upper80": 0.98
        },
        "crystal_size": {
          "estimate": 0.1,
          "lower80": 0.03,
          "upper80": 0.2
        },
        "crystal_yield": {
          "estimate": 0.025,
          "lower80": 0.005,
          "upper80": 0.06
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q09"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.58,
          "lower80": 0.39,
          "upper80": 0.76
        },
        "crystal_purity": {
          "estimate": 0.93,
          "lower80": 0.82,
          "upper80": 0.98
        },
        "crystal_size": {
          "estimate": 0.14,
          "lower80": 0.05,
          "upper80": 0.26
        },
        "crystal_yield": {
          "estimate": 0.16,
          "lower80": 0.07,
          "upper80": 0.27
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q10"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.35,
          "lower80": 0.2,
          "upper80": 0.52
        },
        "crystal_purity": {
          "estimate": 0.95,
          "lower80": 0.88,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.25,
          "lower80": 0.13,
          "upper80": 0.4
        },
        "crystal_yield": {
          "estimate": 0.41,
          "lower80": 0.27,
          "upper80": 0.55
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q11"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.53,
          "lower80": 0.35,
          "upper80": 0.7
        },
        "crystal_purity": {
          "estimate": 0.91,
          "lower80": 0.82,
          "upper80": 0.97
        },
        "crystal_size": {
          "estimate": 0.18,
          "lower80": 0.08,
          "upper80": 0.32
        },
        "crystal_yield": {
          "estimate": 0.57,
          "lower80": 0.44,
          "upper80": 0.7
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q12"
      }
    ],
    "rationale": "All recipes contain seed and reach a cooling step, so particles are expected throughout. Q01\u2013Q02 isolates solvent: S3 is predicted to sacrifice some recovery relative to S1 but give larger, cleaner crystals and fewer fines because its nominal growth/occlusion profile is more favorable. Q03\u2013Q04 isolates seed loading: the larger seed charge should provide substantially more growth surface, suppress secondary nucleation, and reduce fines, with little effect on equilibrium recovery. Q05\u2013Q06 contrasts gradual cooling with a temperature crash followed by a long hold; final recovery should be similar, but the crash is expected to establish a persistent population of fines. Q07\u2013Q08 tests annealing: heating to 315 K should dissolve smaller particles and improve size and fines, but the short recooling period may leave less target recovered. Q09\u2013Q10 shows residence-time dependence at 292 K: two hours should raise recovery and permit growth, although both remain fines-limited. Q11\u2013Q12 doubles reagent concentration: this should markedly increase supersaturation and recovery but also secondary nucleation, impurity occlusion, and the risk of exceeding the fines limit. Purity is predicted to remain above 0.80 because the campaign consistently showed strong crystallization purification. Intervals are deliberately broad because these recipes extrapolate to much lower volume/loading, much longer multistage cooling, and a C1/S0-centered regime not directly replicated in the campaign; feasibility labels use the point estimates, so cases whose fines intervals cross 0.50 remain uncertain."
  },
  "failure": null,
  "elapsed_s": 127.125,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 518272,
    "input_tokens": 628371,
    "output_tokens": 13934,
    "reasoning_output_tokens": 6794
  },
  "numerics_budget": {
    "limit": 128,
    "on_exhaustion": "continue_answer",
    "version": "public-numerics-budget-v1"
  },
  "numerics_attempts": 1
}
```

## K2

```json
{
  "payload": {
    "report": "1. Status of the main claims\n\nSupported by direct observations:\n\n- Catalyst choice mattered, and C0 was the best catalyst observed in the approximate S2 screen. Batch 2 (C0) gave crystal recovery 0.485, versus 0.294 for C2 in batch 3 and 0.397 for C3 in batch 4. C1 gave 0.439 in batch 1 and 0.339 in batch 5, although those C1 runs used different temperature/time conditions. Thus C0 superiority is supported locally, not established as a universal catalyst ranking.\n- Solvent identity created a recovery\u2013particle-quality tradeoff. Under similar C0 processing, S0 and S1 gave higher recoveries in batches 6 and 7\u20140.548 and 0.564\u2014but failed the fines constraint at 0.730 and 0.565. S2 in batch 2 gave lower recovery, 0.485, but compliant fines of 0.445. Further S2 runs, especially batches 13\u201316 and 22\u201323, repeatedly produced compliant fines.\n- Crystallization strongly purified the reaction mixture. Batch 3 directly showed final reaction selectivity near 0.372 but crystal purity near 0.989. Across the campaign, crystal purity was generally 0.96\u20131.00 despite much lower reaction selectivity. Preferential target crystallization is an interpretation, but the separation between reaction selectivity and crystal purity is directly observed.\n- Process history mattered. Batches 21 and 23 are the clearest comparison: both used 0.040 L S2 with the same charge, catalyst, seed, final temperature, and aging conditions, but batch 23 inserted a 310 K cooling stage. Batch 21 had fines of 1.000, whereas batch 23 had fines of 0.425, with similar recoveries of 0.541 and 0.523. This directly supports a strong thermal-path effect.\n- The attempted S1 remedies did not solve the fines problem. Changes in seed and final temperature in batches 9\u201312 left fines around 0.571\u20130.586. Reheat/recool treatments in batches 17\u201320 left fines around 0.558\u20130.607. That directly supports abandoning those tested S1 routes.\n\nSupported mainly as interpretation:\n\n- The explanation that S2 suppresses nucleation while favoring growth and reducing impurity occlusion is consistent with its nominal dossier and observed compliant CSDs, but nucleation and growth rates were not measured directly.\n- The supersaturation explanation for batches 21 and 23 is plausible and parsimonious, but concentration, solubility, and nucleation rate were not measured. The data establish history dependence, not the unique microscopic cause.\n- Treating crystal recovery through a relation such as recovered target = charged reagent \u00d7 conversion \u00d7 selectivity \u00d7 crystallization recovery is a useful mass-balance framework. Only the separate reported quantities were observed; the proposed coupling law was not independently validated.\n\nContradicted or weakened:\n\n- A simple claim that reheating necessarily dissolves fines and improves the distribution is weakened by batches 17\u201320. None produced a compliant S1 fines result, and fines did not improve monotonically with reheat temperature. This is particularly relevant to my favorable annealing interpretation for held-out Q08.\n- A strong monotonic seed-mass effect is not supported. At otherwise similar S2 conditions, batch 13 with 0.050 g seed gave 0.447 fines, while batch 14 with 0.010 g gave 0.469; the difference was small relative to uncertainty. Batch 24 cannot resolve the issue because both seed and cooling history differed.\n- Nominal solvent properties alone do not predict outcomes. S3 nominally has lower nucleation tendency than S0/S1, yet batch 8 still failed with fines of 0.603. Reaction composition and process history must also matter.\n\nStill untested:\n\n- The very long, multistage cooling schedules in Q01\u2013Q08 and Q11\u2013Q12 were never run.\n- The queried 0.020 L scale, 0.004 mol reagent loading, low C1 catalyst charge, quench, and 385 K reaction form a regime well outside the completed campaign.\n- Whether low target concentration crosses a solubility threshold, rather than merely lowering recovery smoothly, remains unknown.\n- Exact reproducibility and process variance remain unknown because no recipe was exactly replicated.\n\n2. One additional experiment\n\nI would run a concentration-perturbation experiment matched to batch 22: 0.020 mol reagent, 0.060 L S2, 0.0025 mol C0 to preserve the catalyst/reagent ratio, the same 350 K/3,600 s reaction, 0.050 g seed, cooling to 250 K over 14,400 s, and 14,400 s aging at 150 rpm. I would add HPLC immediately before crystallization, particle sizing before filtration, and the final assay after termination.\n\nCompared with batch 22, this changes target concentration while retaining solvent identity, catalyst ratio, seed surface, and thermal history. It would distinguish three explanations:\n\n- Concentration/supersaturation control: recovery should fall substantially below batch 22's 0.524, while secondary nucleation and fines should decrease. The HPLC target estimate would connect the change to pre-crystallization concentration.\n- A largely solvent- and temperature-controlled fractional-recovery law: crystal recovery should remain near 0.5 and fines near batch 22's 0.43 despite the lower charge.\n- Seed-dominated population control: fines would remain low because the absolute seed charge is unchanged, while crystal size or recovered mass per seed would shift more strongly than the fines fraction.\n\nA result with little or no seed-excluded product would reveal a solubility threshold and would materially revise the basis for the low-loading held-out predictions. Conversely, recovery near batch 22 would support using fractional recovery across scale.\n\n3. Least-used observation and least-reliable prediction\n\nThe observation used least effectively was batch 1's exceptionally low final fines fraction, 0.292, together with recovery 0.439. I mainly used batch 1 as evidence that C1 was inferior to C0, but its particle result was the best fines result in the campaign. It could indicate that reaction composition, higher reaction temperature, or C1-specific impurities altered nucleation more strongly than the solvent-only account allowed. Because batch 1 differed in catalyst and reaction conditions and had no matched replicate, I could not identify the cause, but the report should have emphasized this counterexample more clearly.\n\nQ08 is the least reliable held-out prediction. I predicted that reheating to 315 K after a long slow ramp would lower fines and increase size, at the cost of recovery. That direction relies on an Ostwald-ripening interpretation, yet batches 17\u201320 provided no convincing evidence that reheat/recool treatment improved fines. Q08 also combines an untested multi-day S0 ramp, a 315 K excursion, and only one hour of recooling, so dissolution, incomplete recovery, and renewed nucleation could dominate in different directions. Its interval was broad, but even the sign of the CSD change relative to Q07 is less secure than the sealed point estimates imply."
  },
  "failure": null,
  "elapsed_s": 65.0,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 551936,
    "input_tokens": 679693,
    "output_tokens": 16777,
    "reasoning_output_tokens": 8065
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
    "selection_rationale": "Highest observed seed-excluded crystal recovery among completed batches meeting both constraints: crystal_yield 0.5245, crystal_purity 1.000, and fines fraction 0.4273. The S2/C0 process at 0.06 L solvent also showed confirmatory particle sizing with fines below 0.50."
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
        "volume_L": 0.06
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
        "target_temperature_K": 350
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
    "excluded_rejected_attempts": [],
    "lifecycle_index": 22,
    "source_attempts": 11
  },
  "prediction_evaluation": {
    "contrasts": [
      {
        "absolute_delta_error": 0.1531177888119947,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_yield",
        "predicted_delta": -0.03999999999999998,
        "resolved": true,
        "true_delta": -0.19311778881199468
      },
      {
        "absolute_delta_error": 0.016447144036145556,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_purity",
        "predicted_delta": 0.015000000000000013,
        "resolved": false,
        "true_delta": -0.0014471440361455423
      },
      {
        "absolute_delta_error": 0.02097319527336291,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_size",
        "predicted_delta": 0.04999999999999999,
        "resolved": true,
        "true_delta": 0.02902680472663708
      },
      {
        "absolute_delta_error": 0.4902675737116523,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.09999999999999998,
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
        "absolute_delta_error": 0.0017644384597508278,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_purity",
        "predicted_delta": 0.010000000000000009,
        "resolved": false,
        "true_delta": 0.008235561540249181
      },
      {
        "absolute_delta_error": 0.11022020934805375,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_size",
        "predicted_delta": 0.11,
        "resolved": false,
        "true_delta": -0.00022020934805375147
      },
      {
        "absolute_delta_error": 0.19936854990383646,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.21999999999999997,
        "resolved": false,
        "true_delta": -0.020631450096163517
      },
      {
        "absolute_delta_error": 0.009739549297168137,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_yield",
        "predicted_delta": 0.010000000000000009,
        "resolved": false,
        "true_delta": 0.00026045070283187144
      },
      {
        "absolute_delta_error": 0.005132146340829591,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.010000000000000009,
        "resolved": false,
        "true_delta": -0.004867853659170418
      },
      {
        "absolute_delta_error": 0.042379301835895465,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_size",
        "predicted_delta": -0.07999999999999999,
        "resolved": true,
        "true_delta": -0.03762069816410452
      },
      {
        "absolute_delta_error": 0.38810139828932055,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.19000000000000006,
        "resolved": true,
        "true_delta": 0.5781013982893206
      },
      {
        "absolute_delta_error": 0.1200603832856732,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_yield",
        "predicted_delta": -0.07999999999999996,
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
        "absolute_delta_error": 0.060102904647564834,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_size",
        "predicted_delta": 0.030000000000000027,
        "resolved": true,
        "true_delta": -0.030102904647564807
      },
      {
        "absolute_delta_error": 0.6423941217008813,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.040000000000000036,
        "resolved": true,
        "true_delta": 0.6023941217008812
      },
      {
        "absolute_delta_error": 0.018684422102466403,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_yield",
        "predicted_delta": 0.135,
        "resolved": true,
        "true_delta": 0.1536844221024664
      },
      {
        "absolute_delta_error": 0.024527106938203147,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_purity",
        "predicted_delta": 0.010000000000000009,
        "resolved": true,
        "true_delta": -0.014527106938203138
      },
      {
        "absolute_delta_error": 0.02581747475109112,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_size",
        "predicted_delta": 0.04000000000000001,
        "resolved": true,
        "true_delta": 0.014182525248908888
      },
      {
        "absolute_delta_error": 0.13908907723599961,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.12,
        "resolved": false,
        "true_delta": 0.01908907723599962
      },
      {
        "absolute_delta_error": 0.13103124947311257,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_yield",
        "predicted_delta": 0.15999999999999998,
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
        "absolute_delta_error": 0.043426352835710225,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_size",
        "predicted_delta": -0.07,
        "resolved": true,
        "true_delta": -0.026573647164289782
      },
      {
        "absolute_delta_error": 0.4109082204353358,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.18000000000000005,
        "resolved": true,
        "true_delta": 0.5909082204353359
      }
    ],
    "failures": [],
    "metrics": {
      "crystal_fines_fraction": {
        "coverage80": 0.5,
        "interval_score80": 1.912124827011765,
        "interval_width": 0.3325,
        "mae": 0.28666959351653204,
        "n": 12,
        "planned": 12
      },
      "crystal_purity": {
        "coverage80": 0.75,
        "interval_score80": 0.1461680642393667,
        "interval_width": 0.11833333333333333,
        "mae": 0.038073235959058475,
        "n": 12,
        "planned": 12
      },
      "crystal_size": {
        "coverage80": 0.16666666666666666,
        "interval_score80": 0.5652574407621004,
        "interval_width": 0.23750000000000002,
        "mae": 0.13332695326990782,
        "n": 12,
        "planned": 12
      },
      "crystal_yield": {
        "coverage80": 0.8333333333333334,
        "interval_score80": 0.35368887844086117,
        "interval_width": 0.25625000000000003,
        "mae": 0.09092825683582134,
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
    "resolved_direction_correct": 9,
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
        "crystal_purity": 0.004302486622639943,
        "crystal_size": 0.017192244486071477,
        "crystal_yield": 0.2352034856839793
      },
      "public_nearest_neighbor": {
        "crystal_fines_fraction": 0.3959500464387022,
        "crystal_purity": 0.008058040914511335,
        "crystal_size": 0.017816873869995205,
        "crystal_yield": 0.183940532054883
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
        "cached_input": 466176,
        "input": 500171,
        "output": 5204,
        "stage": "source",
        "uncached_input": 33995
      },
      {
        "cached_input": 3456,
        "input": 33823,
        "output": 2869,
        "stage": "K1",
        "uncached_input": 30367
      },
      {
        "cached_input": 48640,
        "input": 94377,
        "output": 5861,
        "stage": "Q",
        "uncached_input": 45737
      },
      {
        "cached_input": 33664,
        "input": 51322,
        "output": 2843,
        "stage": "K2",
        "uncached_input": 17658
      }
    ],
    "total": {
      "cached_input": 551936,
      "input": 679693,
      "input_plus_output": 696470,
      "output": 16777,
      "uncached_input": 127757
    },
    "valid": true
  },
  "elapsed_s": 471.01500000001397
}
```
