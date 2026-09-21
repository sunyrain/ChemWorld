# C-W01-B24-E-MisIndexed

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
      "stirring_speed_rpm": 200
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
  "end_step": 12,
  "lifecycle_index": 1,
  "metrics": {
    "byproduct_signal": 0.3558693826198578,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7653630971908569,
    "crystal_fines_fraction": 0.2544594407081604,
    "crystal_purity": 0.988656759262085,
    "crystal_size": 0.08623096346855164,
    "crystal_yield": 0.45209136605262756,
    "degradation_warning": 0.18416446447372437,
    "safety_risk": 0.18061931431293488,
    "score": 0.5230410695075989,
    "selectivity": 0.5338460803031921,
    "virtual_spectrum_summary": 0.2786021828651428,
    "yield": 0.531683623790741
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
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 340
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
    "byproduct_signal": 0.2675972878932953,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6793789267539978,
    "crystal_fines_fraction": 0.49667179584503174,
    "crystal_purity": 0.9830515384674072,
    "crystal_size": 0.11286578327417374,
    "crystal_yield": 0.48336392641067505,
    "degradation_warning": 0.05591294914484024,
    "safety_risk": 0.18429328501224518,
    "score": 0.4974093735218048,
    "selectivity": 0.5756059885025024,
    "virtual_spectrum_summary": 0.1723393350839615,
    "yield": 0.5640468597412109
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
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 340
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
  "end_step": 32,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.3104499280452728,
    "conversion": 0.9980403780937195,
    "cost": 1.0,
    "crystal_csd_quality": 0.7320876121520996,
    "crystal_fines_fraction": 0.3084520101547241,
    "crystal_purity": 0.9903686046600342,
    "crystal_size": 0.07596264034509659,
    "crystal_yield": 0.37148192524909973,
    "degradation_warning": 0.05127779766917229,
    "safety_risk": 0.16955532133579254,
    "score": 0.47585633397102356,
    "selectivity": 0.453420490026474,
    "virtual_spectrum_summary": 0.1938224732875824,
    "yield": 0.4524076581001282
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
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 340
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
  "end_step": 42,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.2670803964138031,
    "conversion": 0.9887611865997314,
    "cost": 1.0,
    "crystal_csd_quality": 0.6785460114479065,
    "crystal_fines_fraction": 0.4914858043193817,
    "crystal_purity": 1.0,
    "crystal_size": 0.08372688293457031,
    "crystal_yield": 0.5043026804924011,
    "degradation_warning": 0.0698307678103447,
    "safety_risk": 0.18534184992313385,
    "score": 0.5035994052886963,
    "selectivity": 0.5796047449111938,
    "virtual_spectrum_summary": 0.1783180683851242,
    "yield": 0.5658397674560547
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
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
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
  "end_step": 52,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.28358641266822815,
    "conversion": 0.9961102604866028,
    "cost": 1.0,
    "crystal_csd_quality": 0.6702467203140259,
    "crystal_fines_fraction": 0.5271331071853638,
    "crystal_purity": 0.9804216623306274,
    "crystal_size": 0.04670894145965576,
    "crystal_yield": 0.4887533187866211,
    "degradation_warning": 0.07375490665435791,
    "safety_risk": 0.18369464576244354,
    "score": 0.4875892102718353,
    "selectivity": 0.5769221782684326,
    "virtual_spectrum_summary": 0.1891622394323349,
    "yield": 0.570641040802002
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
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 340
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
  "end_step": 64,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.30497926473617554,
    "conversion": 0.9881521463394165,
    "cost": 1.0,
    "crystal_csd_quality": 0.5473130941390991,
    "crystal_fines_fraction": 0.7850876450538635,
    "crystal_purity": 0.9938106536865234,
    "crystal_size": 0.04034573957324028,
    "crystal_yield": 0.4282984733581543,
    "degradation_warning": 0.04871954768896103,
    "safety_risk": 0.24235151708126068,
    "score": 0.40045735239982605,
    "selectivity": 0.46716251969337463,
    "virtual_spectrum_summary": 0.1896623820066452,
    "yield": 0.46702152490615845
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
      "catalyst": 3,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 340
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
  "end_step": 74,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.3208724558353424,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6204690337181091,
    "crystal_fines_fraction": 0.5380254983901978,
    "crystal_purity": 0.9712773561477661,
    "crystal_size": 0.08773630112409592,
    "crystal_yield": 0.427823007106781,
    "degradation_warning": 0.08958321809768677,
    "safety_risk": 0.1866072714328766,
    "score": 0.4478234350681305,
    "selectivity": 0.4714408218860626,
    "virtual_spectrum_summary": 0.2167923003435135,
    "yield": 0.49796172976493835
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
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 340
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
  "end_step": 84,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.2669990360736847,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7104638814926147,
    "crystal_fines_fraction": 0.457649290561676,
    "crystal_purity": 0.9800697565078735,
    "crystal_size": 0.11316776275634766,
    "crystal_yield": 0.5119263529777527,
    "degradation_warning": 0.09158220142126083,
    "safety_risk": 0.18493258953094482,
    "score": 0.5155390501022339,
    "selectivity": 0.5813986659049988,
    "virtual_spectrum_summary": 0.18806146085262299,
    "yield": 0.5729581117630005
  },
  "ordinal": 8
}
```

## Batch 9

```json
{
  "actions": [
    {
      "amount_mol": 0.0375,
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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 340
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 255
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
  "end_step": 94,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.2733028531074524,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7392840385437012,
    "crystal_fines_fraction": 0.3438909649848938,
    "crystal_purity": 0.9824389219284058,
    "crystal_size": 0.058132022619247437,
    "crystal_yield": 0.5196489691734314,
    "degradation_warning": 0.08603102713823318,
    "safety_risk": 0.1792227178812027,
    "score": 0.531366765499115,
    "selectivity": 0.5743829011917114,
    "virtual_spectrum_summary": 0.18903052806854248,
    "yield": 0.5879067778587341
  },
  "ordinal": 9
}
```

## Batch 10

```json
{
  "actions": [
    {
      "amount_mol": 0.0375,
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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 340
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 7200,
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
  "end_step": 104,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.2661799490451813,
    "conversion": 0.9855663776397705,
    "cost": 1.0,
    "crystal_csd_quality": 0.6516252756118774,
    "crystal_fines_fraction": 0.471215158700943,
    "crystal_purity": 0.9781301617622375,
    "crystal_size": 0.07149368524551392,
    "crystal_yield": 0.5141957402229309,
    "degradation_warning": 0.09743737429380417,
    "safety_risk": 0.17898838222026825,
    "score": 0.5013515949249268,
    "selectivity": 0.58546382188797,
    "virtual_spectrum_summary": 0.19024579226970673,
    "yield": 0.5942385792732239
  },
  "ordinal": 10
}
```

## Batch 11

```json
{
  "actions": [
    {
      "amount_mol": 0.0375,
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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 340
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
  "end_step": 114,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.274694561958313,
    "conversion": 0.9987625479698181,
    "cost": 1.0,
    "crystal_csd_quality": 0.732297420501709,
    "crystal_fines_fraction": 0.3367457687854767,
    "crystal_purity": 0.9930613040924072,
    "crystal_size": 0.07733708620071411,
    "crystal_yield": 0.5051581263542175,
    "degradation_warning": 0.07445739954710007,
    "safety_risk": 0.17860513925552368,
    "score": 0.5297536253929138,
    "selectivity": 0.5892360806465149,
    "virtual_spectrum_summary": 0.18458783626556396,
    "yield": 0.569597601890564
  },
  "ordinal": 11
}
```

## Batch 12

```json
{
  "actions": [
    {
      "amount_mol": 0.0375,
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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 340
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
  "end_step": 125,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.2586961090564728,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6717776656150818,
    "crystal_fines_fraction": 0.4856484532356262,
    "crystal_purity": 0.9944484233856201,
    "crystal_size": 0.09869137406349182,
    "crystal_yield": 0.5203579068183899,
    "degradation_warning": 0.09621580690145493,
    "safety_risk": 0.17938126623630524,
    "score": 0.5106624960899353,
    "selectivity": 0.5819925665855408,
    "virtual_spectrum_summary": 0.18557997047901154,
    "yield": 0.586882472038269
  },
  "ordinal": 12
}
```

## Batch 13

```json
{
  "actions": [
    {
      "amount_mol": 0.0375,
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
      "target_temperature_K": 340
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
  "end_step": 135,
  "lifecycle_index": 13,
  "metrics": {
    "byproduct_signal": 0.24951176345348358,
    "conversion": 0.9969956874847412,
    "cost": 1.0,
    "crystal_csd_quality": 0.7497886419296265,
    "crystal_fines_fraction": 0.35718613862991333,
    "crystal_purity": 0.9813039302825928,
    "crystal_size": 0.07743736356496811,
    "crystal_yield": 0.4909672439098358,
    "degradation_warning": 0.0588216632604599,
    "safety_risk": 0.17812742292881012,
    "score": 0.5267865657806396,
    "selectivity": 0.5894767642021179,
    "virtual_spectrum_summary": 0.16370122134685516,
    "yield": 0.5813349485397339
  },
  "ordinal": 13
}
```

## Batch 14

```json
{
  "actions": [
    {
      "amount_mol": 0.0375,
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
      "stirring_speed_rpm": 500,
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
  "lifecycle_index": 14,
  "metrics": {
    "byproduct_signal": 0.29033714532852173,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.4833619296550751,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9629822373390198,
    "crystal_size": 0.10854659229516983,
    "crystal_yield": 0.4445759952068329,
    "degradation_warning": 0.06577936559915543,
    "safety_risk": 0.1717483401298523,
    "score": 0.3866097033023834,
    "selectivity": 0.5310227870941162,
    "virtual_spectrum_summary": 0.18928614258766174,
    "yield": 0.5231004357337952
  },
  "ordinal": 14
}
```

## Batch 15

```json
{
  "actions": [
    {
      "amount_mol": 0.0375,
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
      "duration_s": 1200,
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
  "end_step": 155,
  "lifecycle_index": 15,
  "metrics": {
    "byproduct_signal": 0.20403221249580383,
    "conversion": 0.9980490803718567,
    "cost": 1.0,
    "crystal_csd_quality": 0.7277618646621704,
    "crystal_fines_fraction": 0.29291534423828125,
    "crystal_purity": 0.9880712628364563,
    "crystal_size": 0.09937402606010437,
    "crystal_yield": 0.5782238841056824,
    "degradation_warning": 0.04751845821738243,
    "safety_risk": 0.18860618770122528,
    "score": 0.5704345703125,
    "selectivity": 0.6738724708557129,
    "virtual_spectrum_summary": 0.13360102474689484,
    "yield": 0.674285888671875
  },
  "ordinal": 15
}
```

## Batch 16

```json
{
  "actions": [
    {
      "amount_mol": 0.0375,
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
      "duration_s": 4800,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 340
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
  "end_step": 165,
  "lifecycle_index": 16,
  "metrics": {
    "byproduct_signal": 0.3553146719932556,
    "conversion": 0.9885537028312683,
    "cost": 1.0,
    "crystal_csd_quality": 0.7094892263412476,
    "crystal_fines_fraction": 0.28731393814086914,
    "crystal_purity": 0.9782392978668213,
    "crystal_size": 0.08702820539474487,
    "crystal_yield": 0.4140942096710205,
    "degradation_warning": 0.1842864602804184,
    "safety_risk": 0.16930407285690308,
    "score": 0.49053457379341125,
    "selectivity": 0.4963586926460266,
    "virtual_spectrum_summary": 0.2783519923686981,
    "yield": 0.4947132468223572
  },
  "ordinal": 16
}
```

## Batch 17

```json
{
  "actions": [
    {
      "amount_mol": 0.0375,
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
      "duration_s": 1200,
      "operation": "heat",
      "stirring_speed_rpm": 500,
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
  "end_step": 175,
  "lifecycle_index": 17,
  "metrics": {
    "byproduct_signal": 0.21588028967380524,
    "conversion": 0.9916958808898926,
    "cost": 1.0,
    "crystal_csd_quality": 0.7115891575813293,
    "crystal_fines_fraction": 0.3451111614704132,
    "crystal_purity": 0.999424934387207,
    "crystal_size": 0.0765853077173233,
    "crystal_yield": 0.5733206272125244,
    "degradation_warning": 0.0481443889439106,
    "safety_risk": 0.18610747158527374,
    "score": 0.557138204574585,
    "selectivity": 0.6531620621681213,
    "virtual_spectrum_summary": 0.14039912819862366,
    "yield": 0.6557958722114563
  },
  "ordinal": 17
}
```

## Batch 18

```json
{
  "actions": [
    {
      "amount_mol": 0.0375,
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
      "duration_s": 1200,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 370
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
  "end_step": 185,
  "lifecycle_index": 18,
  "metrics": {
    "byproduct_signal": 0.18390001356601715,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7611674070358276,
    "crystal_fines_fraction": 0.2609618604183197,
    "crystal_purity": 0.9953625202178955,
    "crystal_size": 0.13695834577083588,
    "crystal_yield": 0.5917500853538513,
    "degradation_warning": 0.054465919733047485,
    "safety_risk": 0.1902868151664734,
    "score": 0.5920113921165466,
    "selectivity": 0.6835355758666992,
    "virtual_spectrum_summary": 0.1256546676158905,
    "yield": 0.6947213411331177
  },
  "ordinal": 18
}
```

## Batch 19

```json
{
  "actions": [
    {
      "amount_mol": 0.0375,
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
      "duration_s": 600,
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
  "end_step": 195,
  "lifecycle_index": 19,
  "metrics": {
    "byproduct_signal": 0.14791390299797058,
    "conversion": 0.8584883213043213,
    "cost": 1.0,
    "crystal_csd_quality": 0.7486259341239929,
    "crystal_fines_fraction": 0.26574790477752686,
    "crystal_purity": 0.9740859866142273,
    "crystal_size": 0.07211596518754959,
    "crystal_yield": 0.545695960521698,
    "degradation_warning": 0.011489243246614933,
    "safety_risk": 0.17720535397529602,
    "score": 0.5578076839447021,
    "selectivity": 0.7191854119300842,
    "virtual_spectrum_summary": 0.08652280271053314,
    "yield": 0.6269484162330627
  },
  "ordinal": 19
}
```

## Batch 20

```json
{
  "actions": [
    {
      "amount_mol": 0.0375,
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
      "duration_s": 1800,
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
  "end_step": 205,
  "lifecycle_index": 20,
  "metrics": {
    "byproduct_signal": 0.23965007066726685,
    "conversion": 0.9931921362876892,
    "cost": 1.0,
    "crystal_csd_quality": 0.7240934371948242,
    "crystal_fines_fraction": 0.2924696207046509,
    "crystal_purity": 0.9927552342414856,
    "crystal_size": 0.08928439766168594,
    "crystal_yield": 0.5522638559341431,
    "degradation_warning": 0.08080141991376877,
    "safety_risk": 0.18550355732440948,
    "score": 0.556915819644928,
    "selectivity": 0.6513336300849915,
    "virtual_spectrum_summary": 0.16816817224025726,
    "yield": 0.6348357200622559
  },
  "ordinal": 20
}
```

## Batch 21

```json
{
  "actions": [
    {
      "amount_mol": 0.0375,
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
      "duration_s": 1200,
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
  "end_step": 215,
  "lifecycle_index": 21,
  "metrics": {
    "byproduct_signal": 0.18157848715782166,
    "conversion": 0.9833226203918457,
    "cost": 1.0,
    "crystal_csd_quality": 0.7682745456695557,
    "crystal_fines_fraction": 0.2890740931034088,
    "crystal_purity": 0.9900954365730286,
    "crystal_size": 0.0677061602473259,
    "crystal_yield": 0.6048932075500488,
    "degradation_warning": 0.04609701782464981,
    "safety_risk": 0.18905799090862274,
    "score": 0.5828754901885986,
    "selectivity": 0.6664187908172607,
    "virtual_spectrum_summary": 0.12061182409524918,
    "yield": 0.6815748810768127
  },
  "ordinal": 21
}
```

## Batch 22

```json
{
  "actions": [
    {
      "amount_mol": 0.0375,
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
      "duration_s": 1200,
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
  "end_step": 225,
  "lifecycle_index": 22,
  "metrics": {
    "byproduct_signal": 0.20711715519428253,
    "conversion": 0.9971964955329895,
    "cost": 1.0,
    "crystal_csd_quality": 0.7608592510223389,
    "crystal_fines_fraction": 0.22426825761795044,
    "crystal_purity": 1.0,
    "crystal_size": 0.08571068197488785,
    "crystal_yield": 0.5644313097000122,
    "degradation_warning": 0.04975823685526848,
    "safety_risk": 0.18778552114963531,
    "score": 0.5792651772499084,
    "selectivity": 0.6640171408653259,
    "virtual_spectrum_summary": 0.13630564510822296,
    "yield": 0.6611748933792114
  },
  "ordinal": 22
}
```

## Batch 23

```json
{
  "actions": [
    {
      "amount_mol": 0.0375,
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
      "duration_s": 1200,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 370
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
  "end_step": 235,
  "lifecycle_index": 23,
  "metrics": {
    "byproduct_signal": 0.20259779691696167,
    "conversion": 0.9917913675308228,
    "cost": 1.0,
    "crystal_csd_quality": 0.7389504313468933,
    "crystal_fines_fraction": 0.2305540144443512,
    "crystal_purity": 0.9973864555358887,
    "crystal_size": 0.10722733289003372,
    "crystal_yield": 0.599139392375946,
    "degradation_warning": 0.04798305407166481,
    "safety_risk": 0.19074763357639313,
    "score": 0.5897322297096252,
    "selectivity": 0.6917200684547424,
    "virtual_spectrum_summary": 0.13302116096019745,
    "yield": 0.6912570595741272
  },
  "ordinal": 23
}
```

## Batch 24

```json
{
  "actions": [
    {
      "amount_mol": 0.0375,
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
      "duration_s": 1200,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 370
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
  "end_step": 246,
  "lifecycle_index": 24,
  "metrics": {
    "byproduct_signal": 0.20236602425575256,
    "conversion": 0.997706413269043,
    "cost": 1.0,
    "crystal_csd_quality": 0.7110775113105774,
    "crystal_fines_fraction": 0.2970272898674011,
    "crystal_purity": 1.0,
    "crystal_size": 0.0845741555094719,
    "crystal_yield": 0.5932515859603882,
    "degradation_warning": 0.05048414319753647,
    "safety_risk": 0.19074763357639313,
    "score": 0.574187695980072,
    "selectivity": 0.6853606104850769,
    "virtual_spectrum_summary": 0.1340191811323166,
    "yield": 0.6923892498016357
  },
  "ordinal": 24
}
```

## K1

```json
{
  "payload": {
    "report": "## Mechanistic account\n\n### Recommended process and principal observation\nThe sealed recommendation remains batch 21: 0.0375 mol reagent in 0.080 L solvent-S2 with 0.005 mol catalyst-C3; heat at 360 K for 1,200 s with 500 rpm stirring; add 0.050 g seed; cool-crystallize at 250 K for 14,400 s; then filter and terminate. Its final assay gave seed-excluded crystal recovery 0.605, crystal purity 0.990, and fines fraction 0.289, satisfying both constraints with substantial margin.\n\nBatch 21 had the highest observed recovery, but it is not uniquely superior within measurement uncertainty. Batches 18, 23, and 24 gave recoveries of 0.592, 0.599, and 0.593. Thus the recommendation is the observed winner, while the underlying optimum probably lies in a relatively broad region around 360\u2013370 K reaction temperature, approximately 1,200 s reaction time, solvent-S2/catalyst-C3, and a final crystallization temperature near 250 K.\n\n### Material effects\n**Observed catalyst effect.** Under matched solvent-S2, 340 K, 2,400 s reaction and 250 K crystallization conditions, catalyst-C3 performed best among the directly compared catalysts: batch 4 gave recovery 0.504, purity 1.000, and fines 0.491. Catalyst-C0 in batch 2 gave 0.483 recovery and 0.497 fines, whereas catalyst-C2 in batch 3 gave only 0.371 recovery. Their final reaction selectivities were approximately 0.580, 0.576, and 0.453, respectively. This connects the poor C2 crystallization result to lower target formation rather than primarily to crystal purity. Catalyst-C1 was not tested under exactly the same conditions: batch 5 at 330 K gave recovery 0.489 but failed the fines limit at 0.527, while batch 1 used a much longer 360 K treatment and developed substantial degradation.\n\n**Observed solvent effect.** Solvent-S2 was clearly the most useful tested medium. Batch 7 with solvent-S3 gave recovery 0.428 and fines 0.538, compared with batch 8 using solvent-S2 at otherwise similar catalyst and reaction conditions, which gave recovery 0.512 and fines 0.458. The solvent-S1 experiment, batch 6, gave recovery 0.428 and fines 0.785, but it was confounded by an unintended double reagent charge after a rejected solvent-S0 operation. No completed solvent-S0 batch was obtained, so its behavior remains untested.\n\n**Interpretation.** The nominal dossier characterized S2 as having low relative solubility (0.7), low nucleation tendency (0.65), high growth tendency (1.3), and low impurity occlusion (0.65). The experimental pattern is consistent with that combination: strong supersaturation and recovery, but with growth favored over excessive new-particle nucleation, plus high crystal purity. This agreement is mechanistically suggestive rather than proof of the hidden response law.\n\n### Reaction mechanism and kinetic window\nA useful minimal network is\n\nR \u2192 P,  R \u2192 B,  and P \u2192 D,\n\nwhere P is the desired product, B a parallel byproduct, and D a thermally generated degradation product. One corresponding model is\n\ndR/dt = \u2212(kP + kB)R,\n\ndP/dt = kP R \u2212 kD P,\n\nwith catalyst, solvent, and temperature changing all three rate constants. Arrhenius behavior, ki = Ai exp(\u2212Ei/RT), explains why increasing temperature initially improves conversion and target formation but eventually accelerates loss of P.\n\nThe experiments show a finite kinetic optimum rather than a simple \u201chotter or longer is better\u201d response. With C3/S2 and 1,200 s reaction time, batches 17, 15, and 18 at 350, 360, and 370 K gave reaction yields of 0.656, 0.674, and 0.695 and crystal recoveries of 0.573, 0.578, and 0.592. By contrast, batch 14 at 320 K for 2,400 s gave only 0.523 reaction yield and 0.445 crystal recovery. At 360 K, batch 19 stopped after 600 s with conversion only 0.858 and recovery 0.546; batch 15 at 1,200 s reached approximately complete conversion and 0.578 recovery; extending to 1,800 s in batch 20 reduced recovery to 0.552. The particularly long 4,800 s treatment at 340 K in batch 16 increased the degradation warning to 0.184 and reduced recovery to 0.414.\n\nThese results motivated revising the initial long heating strategy toward a shorter, hotter reaction. Batch 18 suggested that 370 K was productive, although batch 21 at 360 K ultimately had the highest observed crystallization recovery. Temperatures above 370 K and a finer time optimization around 900\u20131,300 s were not tested.\n\n### Reaction\u2013crystallization coupling\nA useful approximate overall material relation is\n\nrecovered target \u2248 charged reagent \u00d7 conversion \u00d7 selectivity \u00d7 crystal recovery,\n\nwhere the reported crystal recovery is specifically the seed-excluded fraction of target present before separation that is recovered as crystals. Consequently, crystal recovery alone does not report overall synthesis yield: an excellent crystallization cannot compensate fully for a poorly selective reaction.\n\nThe reaction also sets the impurity and degradation environment in which nucleation and growth occur. Batch 16 illustrates this coupling: prolonged reaction produced high degradation and low target yield, followed by low crystal recovery, even though its fines value was acceptable. Conversely, batch 21 combined good reaction performance\u2014conversion 0.983, selectivity 0.666, reaction yield 0.682, and degradation warning 0.046\u2014with the campaign's best crystallization recovery.\n\nCrystallization nevertheless provided strong purification. Batch 21's reaction selectivity was only about 0.666, yet crystal purity was 0.990. Across the later S2 batches, final crystal purity was generally 0.97\u20131.00. This indicates preferential incorporation of target and rejection of soluble byproducts. Purity was therefore not the active constraint in the optimized region; recovery and fines were more discriminating.\n\n### Supersaturation, seeding, and process history\nThe crystallization can be represented by supersaturation S = C/C*(T,x), with nucleation and growth rates such as\n\nJ = kJ(S\u22121)^n,  G = kG(S\u22121)^g,\n\nand crystal growth over the temperature history proportional to \u222bG dt. Particle number is analogously influenced by \u222bJ dt. High recovery favors low terminal solubility C*, while low fines generally favor a low nucleation-to-growth ratio J/G and effective seeding.\n\nCooling history produced a measurable recovery/quality tradeoff. Under otherwise matched 360 K/1,200 s reaction conditions, batch 21 cooled to 250 K and gave recovery 0.605 with fines 0.289. Batch 22 cooled only to 270 K and gave lower recovery, 0.564, but fewer fines, 0.224, and purity 1.000. Thus deeper cooling extracted more target while moderately increasing the fine-particle population. Both satisfied the constraints, so the recovery benefit justified the 250 K endpoint.\n\nHistory before seeding also mattered. Batch 12 was first cooled to 320 K, then seeded and cooled to 250 K; it gave recovery 0.520 but fines 0.486. Batch 9, seeded before a direct four-hour cool to 255 K, gave similar recovery, 0.520, but much lower fines, 0.344. A plausible interpretation is that the pre-cooling step allowed uncontrolled nuclei to form before the seed population could dominate growth. This was not verified with replicate batches.\n\nSeed amount was only sparsely explored. Batch 11 used 0.020 g seed and produced recovery 0.505 and fines 0.337; nearby batches using 0.050 g seed had similar recovery but variable fines. This does not establish a monotonic seed-dose law. No completed unseeded control was run, and seed size distribution was not varied.\n\nExtending the cold history did not clearly help. Batch 24 used two successive 14,400 s segments at 250 K after the 370 K reaction but gave recovery 0.593, compared with 0.599 for the single-segment batch 23. Its fines also increased from 0.231 to 0.297. This suggests that near-equilibrium recovery was already approached during the first four hours, although ordinary assay variability could account for much of the difference. Batch 1 also showed that an ambient-temperature wait after cooling reheated the slurry to about 297 K, requiring recooling; such a warm excursion can redissolve solids and alter the surviving crystal population.\n\n### Revisions, uncertainty, and unresolved tradeoffs\nThe campaign progressed from a long C1/S2 reaction in batch 1, through catalyst and solvent screening, to C3/S2, then to reaction temperature/time and cooling optimization. The principal revisions were: replacing C1/C2 with C3; retaining S2 after the solvent comparison; shortening the reaction from several thousand seconds to approximately 1,200 s; and lowering the final crystallization temperature from 260\u2013270 K to 250 K when recovery became the primary objective.\n\nFinal-assay standard deviations were approximately 0.010 for crystal recovery, 0.010 for purity, and 0.018 for fines. Therefore the 0.006 recovery difference between batch 21 and batch 23 is not statistically decisive. Independent particle-size and final-assay readings also sometimes differed materially\u2014for example, batch 23 reported fines of 0.280 by the in-process particle measurement and 0.231 by the final assay\u2014so exact particle metrics should not be overinterpreted. In contrast, batch 21's purity and fines margins relative to the limits are much larger than the stated noise.\n\nThe remaining tradeoff is chiefly 250 K recovery versus the lower fines obtained at 270 K. Batch 21 favors recovery while remaining safely compliant; batch 22 represents a more conservative particle-quality alternative but is not the recommendation. Untested alternatives include solvent-S0, matched testing of catalyst-C1, unseeded crystallization, broader seed-dose and agitation studies, temperature ramps between 250 and 270 K, deliberate ripening cycles, reaction temperatures above 370 K, and replicated batches sufficient to resolve the near-tie among batches 18, 21, 23, and 24."
  },
  "failure": null,
  "elapsed_s": 97.625,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 555904,
    "input_tokens": 641644,
    "output_tokens": 11566,
    "reasoning_output_tokens": 5378
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
          "estimate": 0.4,
          "lower80": 0.25,
          "upper80": 0.56
        },
        "crystal_purity": {
          "estimate": 0.9,
          "lower80": 0.82,
          "upper80": 0.96
        },
        "crystal_size": {
          "estimate": 0.24,
          "lower80": 0.13,
          "upper80": 0.38
        },
        "crystal_yield": {
          "estimate": 0.24,
          "lower80": 0.12,
          "upper80": 0.38
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q01"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.3,
          "lower80": 0.17,
          "upper80": 0.45
        },
        "crystal_purity": {
          "estimate": 0.94,
          "lower80": 0.87,
          "upper80": 0.98
        },
        "crystal_size": {
          "estimate": 0.32,
          "lower80": 0.19,
          "upper80": 0.47
        },
        "crystal_yield": {
          "estimate": 0.34,
          "lower80": 0.21,
          "upper80": 0.48
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q02"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.68,
          "lower80": 0.5,
          "upper80": 0.84
        },
        "crystal_purity": {
          "estimate": 0.84,
          "lower80": 0.72,
          "upper80": 0.93
        },
        "crystal_size": {
          "estimate": 0.11,
          "lower80": 0.04,
          "upper80": 0.22
        },
        "crystal_yield": {
          "estimate": 0.14,
          "lower80": 0.05,
          "upper80": 0.26
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q03"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.43,
          "lower80": 0.27,
          "upper80": 0.59
        },
        "crystal_purity": {
          "estimate": 0.88,
          "lower80": 0.78,
          "upper80": 0.95
        },
        "crystal_size": {
          "estimate": 0.25,
          "lower80": 0.13,
          "upper80": 0.39
        },
        "crystal_yield": {
          "estimate": 0.17,
          "lower80": 0.07,
          "upper80": 0.29
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q04"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.39,
          "lower80": 0.24,
          "upper80": 0.55
        },
        "crystal_purity": {
          "estimate": 0.89,
          "lower80": 0.79,
          "upper80": 0.96
        },
        "crystal_size": {
          "estimate": 0.29,
          "lower80": 0.16,
          "upper80": 0.44
        },
        "crystal_yield": {
          "estimate": 0.18,
          "lower80": 0.08,
          "upper80": 0.3
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q05"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.63,
          "lower80": 0.46,
          "upper80": 0.79
        },
        "crystal_purity": {
          "estimate": 0.85,
          "lower80": 0.73,
          "upper80": 0.94
        },
        "crystal_size": {
          "estimate": 0.14,
          "lower80": 0.06,
          "upper80": 0.26
        },
        "crystal_yield": {
          "estimate": 0.19,
          "lower80": 0.08,
          "upper80": 0.31
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q06"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.38,
          "lower80": 0.23,
          "upper80": 0.54
        },
        "crystal_purity": {
          "estimate": 0.89,
          "lower80": 0.79,
          "upper80": 0.96
        },
        "crystal_size": {
          "estimate": 0.3,
          "lower80": 0.17,
          "upper80": 0.45
        },
        "crystal_yield": {
          "estimate": 0.19,
          "lower80": 0.08,
          "upper80": 0.31
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q07"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.26,
          "lower80": 0.13,
          "upper80": 0.43
        },
        "crystal_purity": {
          "estimate": 0.92,
          "lower80": 0.83,
          "upper80": 0.98
        },
        "crystal_size": {
          "estimate": 0.36,
          "lower80": 0.21,
          "upper80": 0.52
        },
        "crystal_yield": {
          "estimate": 0.15,
          "lower80": 0.05,
          "upper80": 0.28
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q08"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.78,
          "lower80": 0.58,
          "upper80": 0.94
        },
        "crystal_purity": {
          "estimate": 0.94,
          "lower80": 0.8,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.075,
          "lower80": 0.02,
          "upper80": 0.16
        },
        "crystal_yield": {
          "estimate": 0.012,
          "lower80": 0,
          "upper80": 0.05
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q09"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.6,
          "lower80": 0.42,
          "upper80": 0.77
        },
        "crystal_purity": {
          "estimate": 0.9,
          "lower80": 0.78,
          "upper80": 0.97
        },
        "crystal_size": {
          "estimate": 0.13,
          "lower80": 0.05,
          "upper80": 0.24
        },
        "crystal_yield": {
          "estimate": 0.07,
          "lower80": 0.02,
          "upper80": 0.15
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q10"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.38,
          "lower80": 0.23,
          "upper80": 0.54
        },
        "crystal_purity": {
          "estimate": 0.89,
          "lower80": 0.79,
          "upper80": 0.96
        },
        "crystal_size": {
          "estimate": 0.3,
          "lower80": 0.17,
          "upper80": 0.45
        },
        "crystal_yield": {
          "estimate": 0.18,
          "lower80": 0.08,
          "upper80": 0.3
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q11"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.56,
          "lower80": 0.38,
          "upper80": 0.72
        },
        "crystal_purity": {
          "estimate": 0.84,
          "lower80": 0.72,
          "upper80": 0.93
        },
        "crystal_size": {
          "estimate": 0.24,
          "lower80": 0.12,
          "upper80": 0.38
        },
        "crystal_yield": {
          "estimate": 0.38,
          "lower80": 0.24,
          "upper80": 0.53
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q12"
      }
    ],
    "rationale": "Q01\u2013Q02: S3's lower nominal solubility, nucleation tendency, and impurity occlusion imply higher recovery, larger crystals, greater purity, and fewer fines than S1. Q03\u2013Q04: increasing seed from 0.001 to 0.045 g should shift material from uncontrolled nucleation toward seeded growth, strongly lowering fines while only modestly changing equilibrium recovery. Q05\u2013Q06: gradual cooling should suppress the nucleation burst produced by the 120 s crash; the long hold makes recoveries similar, but Q06 should retain smaller, finer particles. Q07\u2013Q08: the 315 K anneal should selectively dissolve fines and improve size and purity, at the cost of some recovery because the final 1 h recool may not fully restore crystallized mass. Q09\u2013Q10: a two-hour hold at 292 K permits appreciably more seed-excluded growth than a 60 s excursion, but solvent S0's high solubility and nucleation tendency leave both low-yield and likely above the fines limit. Q11\u2013Q12: doubling reagent concentration raises supersaturation and recovery, while increasing secondary nucleation and impurity occlusion; Q12 is therefore predicted to miss the fines specification. All recipes contain seed, so particles are expected even where seed-excluded recovery is very low. Intervals are deliberately broad because these recipes extrapolate to S0, much lower catalyst loading, 385 K reaction history, and cooling durations far outside the campaign data; feasibility booleans use the central estimates."
  },
  "failure": null,
  "elapsed_s": 92.81200000000536,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 555904,
    "input_tokens": 696197,
    "output_tokens": 16274,
    "reasoning_output_tokens": 8343
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
    "report": "## 1. Status of the main claims\n\n### Supported by direct observations\n- **Catalyst-C3/C0 outperformed C2 under matched conditions.** Batches 2\u20134 used S2 at 340 K for 2,400 s and comparable crystallization. C3 gave recovery 0.504, C0 0.483, and C2 only 0.371; C2 also had distinctly lower final selectivity. This directly supports a catalyst effect, although it does not identify the molecular cause.\n- **There is a finite reaction time/temperature window.** With C3/S2, batches 17, 15, and 18 at 350, 360, and 370 K for 1,200 s gave recoveries 0.573, 0.578, and 0.592. Batch 19 at 360 K for only 600 s retained incomplete conversion (0.858), while batch 20 at 1,800 s fell to 0.552 recovery. Batch 16, held 4,800 s at 340 K, had a high degradation warning (0.184) and only 0.414 recovery. These observations support an intermediate kinetic optimum.\n- **Deeper cooling increased recovery at a fines cost.** The closest direct pair is batches 21 and 22: cooling to 250 K gave recovery 0.605 and fines 0.289, while cooling to 270 K gave recovery 0.564 and fines 0.224. Both met specification.\n- **Crystallization strongly purified the product.** Batch 21 had reaction selectivity only 0.666 but crystal purity 0.990. Similar high crystal purities occurred throughout the later S2 series. Preferential crystallization is therefore an observation; impurity rejection from the lattice is the interpretation.\n- **S2 outperformed S3 in the tested comparison.** Batch 8 with S2 gave recovery 0.512 and fines 0.458, versus batch 7 with S3 at 0.428 and 0.538. This is consistent with the nominal S2 growth/solubility properties.\n\n### Contradicted or substantially qualified\n- **More cold residence does not necessarily improve crystal quality.** Batch 24 added a second four-hour segment at 250 K but gave recovery 0.593, size 0.085, and fines 0.297, versus batch 23 at 0.599, 0.107, and 0.231 after one segment. This contradicts a simple monotonic ripening or growth-with-time account, although the differences could partly be assay variability.\n- **More seed was not shown to reduce fines monotonically.** Batch 11 with 0.020 g seed gave fines 0.337, lower than nearby 0.050 g-seed batches 8 and 10 at 0.458 and 0.471. The comparisons are not perfect replicates, so this qualifies rather than decisively reverses the seeding interpretation.\n- **\u201cS2 is best among all solvents\u201d was too broad.** S2 beat S3 directly, but the S1 batch was confounded by a double reagent charge and no completed S0 batch existed. Only the narrower S2-versus-S3 claim is directly supported.\n\n### Still untested interpretations\nThe sequential R\u2192P\u2192D model, Arrhenius explanation, uncontrolled nucleation before seeding, and selective dissolution of fines are mechanistic interpretations rather than identified laws. Also untested are S0 behavior, matched C1 versus C3 performance, unseeded crystallization, agitation effects, temperatures above 370 K, multi-day cooling, deliberate annealing, and concentration effects. Those omissions are especially important because the held-out recipes use S0, C1, 385 K, low catalyst loading, long cooling histories, and reheating.\n\n## 2. Most informative additional experiment\n\nI would run one **time-resolved S0/C1 experiment using the held-out reaction backbone**: 0.020 L S0, 0.004 mol reagent, 0.00025 mol C1, 385 K for 1,500 s, a 900 s wait, quench, return to 300 K, and add about 0.040 g seed. I would then cool rapidly to 292 K, collect nondestructive particle-size measurements after approximately one minute and two hours, continue slowly to 278 K, measure particles again, and finally filter and assay.\n\nThis single trajectory would distinguish three competing explanations:\n- **Solubility-limited:** seeds shrink or disappear, particle signals remain weak, and final seed-excluded recovery remains near zero even after extended cooling.\n- **Kinetically limited growth/nucleation:** particles persist; early fines are high, but size increases and fines fall during the hold and slow cooling, with moderate final recovery.\n- **Impurity/occlusion limited:** appreciable particles and recovery develop, but purity remains low or fines remain high despite long residence.\n\nIf my sealed S0 predictions are approximately right, I would expect particles to persist, low-to-moderate recovery, initially high fines, and gradual coarsening. Absence of particles would invalidate my assumption that added seeds necessarily survive; rapid attainment of high recovery and low fines would show that I overestimated S0 solubility and nucleation penalties.\n\n## 3. Least effectively used observation and least reliable prediction\n\nThe observation used least effectively was the **batch 23\u201324 comparison**. The extra 250 K segment in batch 24 did not improve recovery or size and actually increased fines. Although the mechanism report noted saturation, the sealed predictions still assigned substantial coarsening benefits to extremely long, repeated cooling histories. The campaign evidence instead argues that crystallization may saturate quickly and that repeated `cool_crystallize` operations are not equivalent to continued ideal ripening.\n\n**Q08 is the least reliable held-out prediction.** It combines every major extrapolation: untested S0, C1 at low loading, a 385 K reaction and quench, a multi-day stepped cooling schedule, then an untested 315 K anneal and rapid recooling. My predicted selective dissolution of fines\u2014larger crystals, fewer fines, higher purity but lower recovery\u2014rests mainly on general crystallization reasoning, not a clean campaign comparison. Batch 1 contained a warm excursion but was confounded by different catalyst, solvent, reaction history, and recooling; batch 24 did not demonstrate beneficial ripening. Therefore both the direction and magnitude of Q08\u2019s annealing effect are unusually uncertain."
  },
  "failure": null,
  "elapsed_s": 75.5,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 596992,
    "input_tokens": 755378,
    "output_tokens": 19680,
    "reasoning_output_tokens": 10342
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
    "selection_rationale": "Highest observed seed-excluded crystal recovery (0.605) among completed batches while comfortably meeting crystal purity (0.990) and fines (0.289) constraints."
  },
  "recommendation_recipe": {
    "actions": [
      {
        "amount_mol": 0.0375,
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
        "duration_s": 1200,
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
    "source_attempts": 10
  },
  "prediction_evaluation": {
    "contrasts": [
      {
        "absolute_delta_error": 0.1729406234377425,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_yield",
        "predicted_delta": 0.10000000000000003,
        "resolved": true,
        "true_delta": -0.07294062343774246
      },
      {
        "absolute_delta_error": 0.041253877452758214,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_purity",
        "predicted_delta": 0.039999999999999925,
        "resolved": false,
        "true_delta": -0.0012538774527582897
      },
      {
        "absolute_delta_error": 0.06434669807169803,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_size",
        "predicted_delta": 0.08000000000000002,
        "resolved": true,
        "true_delta": 0.015653301928301985
      },
      {
        "absolute_delta_error": 0.3432152850558221,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.10000000000000003,
        "resolved": true,
        "true_delta": -0.44321528505582214
      },
      {
        "absolute_delta_error": 0.03004833748776478,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_yield",
        "predicted_delta": 0.03,
        "resolved": false,
        "true_delta": -4.8337487764782416e-05
      },
      {
        "absolute_delta_error": 0.03186752955473671,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_purity",
        "predicted_delta": 0.040000000000000036,
        "resolved": false,
        "true_delta": 0.008132470445263329
      },
      {
        "absolute_delta_error": 0.1395775043925993,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_size",
        "predicted_delta": 0.14,
        "resolved": false,
        "true_delta": 0.0004224956074007219
      },
      {
        "absolute_delta_error": 0.22517376032701975,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.25000000000000006,
        "resolved": false,
        "true_delta": -0.02482623967298031
      },
      {
        "absolute_delta_error": 0.009767182469520963,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_yield",
        "predicted_delta": 0.010000000000000009,
        "resolved": false,
        "true_delta": 0.00023281753047904585
      },
      {
        "absolute_delta_error": 0.035209363860740805,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.040000000000000036,
        "resolved": false,
        "true_delta": -0.00479063613925923
      },
      {
        "absolute_delta_error": 0.11079459063642305,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_size",
        "predicted_delta": -0.14999999999999997,
        "resolved": true,
        "true_delta": -0.03920540936357691
      },
      {
        "absolute_delta_error": 0.4363771602380363,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.24,
        "resolved": true,
        "true_delta": 0.6763771602380363
      },
      {
        "absolute_delta_error": 0.0815617281802011,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_yield",
        "predicted_delta": -0.04000000000000001,
        "resolved": true,
        "true_delta": 0.041561728180201096
      },
      {
        "absolute_delta_error": 0.03926416706539704,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_purity",
        "predicted_delta": 0.030000000000000027,
        "resolved": false,
        "true_delta": -0.009264167065397011
      },
      {
        "absolute_delta_error": 0.09044373211685838,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_size",
        "predicted_delta": 0.06,
        "resolved": true,
        "true_delta": -0.030443732116858392
      },
      {
        "absolute_delta_error": 0.8161786076870267,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.12,
        "resolved": true,
        "true_delta": 0.6961786076870267
      },
      {
        "absolute_delta_error": 0.09272767781178036,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_yield",
        "predicted_delta": 0.05800000000000001,
        "resolved": true,
        "true_delta": 0.15072767781178037
      },
      {
        "absolute_delta_error": 0.025926976280662317,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_purity",
        "predicted_delta": -0.039999999999999925,
        "resolved": true,
        "true_delta": -0.014073023719337607
      },
      {
        "absolute_delta_error": 0.0401242016094624,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_size",
        "predicted_delta": 0.05500000000000001,
        "resolved": true,
        "true_delta": 0.014875798390537605
      },
      {
        "absolute_delta_error": 0.20026443684698092,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.18000000000000005,
        "resolved": false,
        "true_delta": 0.02026443684698087
      },
      {
        "absolute_delta_error": 0.16925974627058055,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_yield",
        "predicted_delta": 0.2,
        "resolved": true,
        "true_delta": 0.030740253729419464
      },
      {
        "absolute_delta_error": 0.043976332586183164,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_purity",
        "predicted_delta": -0.050000000000000044,
        "resolved": false,
        "true_delta": -0.00602366741381688
      },
      {
        "absolute_delta_error": 0.032436293373212806,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_size",
        "predicted_delta": -0.06,
        "resolved": true,
        "true_delta": -0.027563706626787192
      },
      {
        "absolute_delta_error": 0.5085789828624289,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.18000000000000005,
        "resolved": true,
        "true_delta": 0.6885789828624289
      }
    ],
    "failures": [],
    "metrics": {
      "crystal_fines_fraction": {
        "coverage80": 0.4166666666666667,
        "interval_score80": 1.753923708106152,
        "interval_width": 0.3216666666666667,
        "mae": 0.27134491415097983,
        "n": 12,
        "planned": 12
      },
      "crystal_purity": {
        "coverage80": 0.08333333333333333,
        "interval_score80": 0.43594645057242226,
        "interval_width": 0.17416666666666666,
        "mae": 0.09497512239907345,
        "n": 12,
        "planned": 12
      },
      "crystal_size": {
        "coverage80": 0.16666666666666666,
        "interval_score80": 0.8191274975950984,
        "interval_width": 0.24250000000000002,
        "mae": 0.1618279074609256,
        "n": 12,
        "planned": 12
      },
      "crystal_yield": {
        "coverage80": 0.75,
        "interval_score80": 0.2847198189357261,
        "interval_width": 0.21333333333333335,
        "mae": 0.0997612921202151,
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
        "crystal_fines_fraction": 0.31402314041245477,
        "crystal_purity": 0.004964576631598864,
        "crystal_size": 0.018099763499094243,
        "crystal_yield": 0.2579920663824628
      },
      "public_nearest_neighbor": {
        "crystal_fines_fraction": 0.39782563461161935,
        "crystal_purity": 0.005643926058627106,
        "crystal_size": 0.01895377064862336,
        "crystal_yield": 0.19841638449737928
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
        "cached_input": 555904,
        "input": 600392,
        "output": 6801,
        "stage": "source",
        "uncached_input": 44488
      },
      {
        "cached_input": 0,
        "input": 41252,
        "output": 4765,
        "stage": "K1",
        "uncached_input": 41252
      },
      {
        "cached_input": 0,
        "input": 54553,
        "output": 4708,
        "stage": "Q",
        "uncached_input": 54553
      },
      {
        "cached_input": 41088,
        "input": 59181,
        "output": 3406,
        "stage": "K2",
        "uncached_input": 18093
      }
    ],
    "total": {
      "cached_input": 596992,
      "input": 755378,
      "input_plus_output": 775058,
      "output": 19680,
      "uncached_input": 158386
    },
    "valid": true
  },
  "elapsed_s": 491.5469999999914
}
```
