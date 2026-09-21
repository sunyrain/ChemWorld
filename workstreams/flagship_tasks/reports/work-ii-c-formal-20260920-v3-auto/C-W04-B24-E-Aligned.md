# C-W04-B24-E-Aligned

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
      "target_temperature_K": 350
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
    "byproduct_signal": 0.35467949509620667,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.546587347984314,
    "crystal_fines_fraction": 0.997342586517334,
    "crystal_purity": 0.9871459007263184,
    "crystal_size": 0.03917128965258598,
    "crystal_yield": 0.3826180696487427,
    "degradation_warning": 0.15192534029483795,
    "safety_risk": 0.17327705025672913,
    "score": 0.3713361620903015,
    "selectivity": 0.47121208906173706,
    "virtual_spectrum_summary": 0.2634401321411133,
    "yield": 0.4690496027469635
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
    },
    {
      "operation": "quench"
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 290
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
  "end_step": 23,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.29071182012557983,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5617169737815857,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9841654300689697,
    "crystal_size": 0.06694186478853226,
    "crystal_yield": 0.4024072587490082,
    "degradation_warning": 0.0521516315639019,
    "safety_risk": 0.1757815033197403,
    "score": 0.3856002688407898,
    "selectivity": 0.5021020174026489,
    "virtual_spectrum_summary": 0.18335974216461182,
    "yield": 0.48986196517944336
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
    },
    {
      "operation": "quench"
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
  "end_step": 54,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.28427693247795105,
    "conversion": 0.9967114925384521,
    "cost": 1.0,
    "crystal_csd_quality": 0.5516303777694702,
    "crystal_fines_fraction": 0.9949334263801575,
    "crystal_purity": 0.9910105466842651,
    "crystal_size": 0.027932139113545418,
    "crystal_yield": 0.41016221046447754,
    "degradation_warning": 0.0675414651632309,
    "safety_risk": 0.176186665892601,
    "score": 0.38354799151420593,
    "selectivity": 0.4959123432636261,
    "virtual_spectrum_summary": 0.18674597144126892,
    "yield": 0.4942300021648407
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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
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
  "end_step": 69,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.2783251106739044,
    "conversion": 0.9873900413513184,
    "cost": 1.0,
    "crystal_csd_quality": 0.5187692642211914,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 1.0,
    "crystal_size": 0.03865243121981621,
    "crystal_yield": 0.42650818824768066,
    "degradation_warning": 0.03755626082420349,
    "safety_risk": 0.17676015198230743,
    "score": 0.3861355483531952,
    "selectivity": 0.5203170776367188,
    "virtual_spectrum_summary": 0.16997912526130676,
    "yield": 0.505858838558197
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
      "solvent": 0,
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
      "stirring_speed_rpm": 400,
      "target_temperature_K": 320
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
  "end_step": 82,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.2404084950685501,
    "conversion": 0.9484897255897522,
    "cost": 1.0,
    "crystal_csd_quality": 0.5136615037918091,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9767245054244995,
    "crystal_size": 0.030171262100338936,
    "crystal_yield": 0.46638721227645874,
    "degradation_warning": 0.027947083115577698,
    "safety_risk": 0.1367158442735672,
    "score": 0.4000323712825775,
    "selectivity": 0.5804370641708374,
    "virtual_spectrum_summary": 0.14480085670948029,
    "yield": 0.547171413898468
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
      "solvent": 1,
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
      "stirring_speed_rpm": 400,
      "target_temperature_K": 320
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
  "end_step": 95,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.28250107169151306,
    "conversion": 0.9769671559333801,
    "cost": 1.0,
    "crystal_csd_quality": 0.5156729221343994,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9993482232093811,
    "crystal_size": 0.02158702164888382,
    "crystal_yield": 0.4423829913139343,
    "degradation_warning": 0.03720821067690849,
    "safety_risk": 0.1565917283296585,
    "score": 0.3842352032661438,
    "selectivity": 0.49101266264915466,
    "virtual_spectrum_summary": 0.17211928963661194,
    "yield": 0.48520827293395996
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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 320
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
  "end_step": 108,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.29718685150146484,
    "conversion": 0.9988641142845154,
    "cost": 1.0,
    "crystal_csd_quality": 0.5302650928497314,
    "crystal_fines_fraction": 0.9868426322937012,
    "crystal_purity": 0.9808655381202698,
    "crystal_size": 0.054521407932043076,
    "crystal_yield": 0.42617014050483704,
    "degradation_warning": 0.0413345992565155,
    "safety_risk": 0.17206871509552002,
    "score": 0.3772871792316437,
    "selectivity": 0.4374653100967407,
    "virtual_spectrum_summary": 0.1820533275604248,
    "yield": 0.46153393387794495
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 320
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
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.28268197178840637,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5581873059272766,
    "crystal_fines_fraction": 0.9869509935379028,
    "crystal_purity": 0.9716573357582092,
    "crystal_size": 0.08159967511892319,
    "crystal_yield": 0.43601343035697937,
    "degradation_warning": 0.05206652730703354,
    "safety_risk": 0.18552961945533752,
    "score": 0.39025282859802246,
    "selectivity": 0.488452672958374,
    "virtual_spectrum_summary": 0.17890502512454987,
    "yield": 0.4750638008117676
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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 320
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
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.2999463379383087,
    "conversion": 0.9952810406684875,
    "cost": 1.0,
    "crystal_csd_quality": 0.5156477093696594,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9815170764923096,
    "crystal_size": 0.018755469471216202,
    "crystal_yield": 0.34520336985588074,
    "degradation_warning": 0.040506087243556976,
    "safety_risk": 0.1687598079442978,
    "score": 0.3527493476867676,
    "selectivity": 0.4636264443397522,
    "virtual_spectrum_summary": 0.1831982284784317,
    "yield": 0.4746303856372833
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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 320
    },
    {
      "operation": "quench"
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 295
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 295
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 295
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 295
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 295
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 295
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 295
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 295
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 295
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 295
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 295
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 295
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
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.29282346367836,
    "conversion": 0.9802465438842773,
    "cost": 1.0,
    "crystal_csd_quality": 0.5210129618644714,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9766249656677246,
    "crystal_size": 0.03275251388549805,
    "crystal_yield": 0.34632042050361633,
    "degradation_warning": 0.05191243439912796,
    "safety_risk": 0.16827932000160217,
    "score": 0.3517509698867798,
    "selectivity": 0.4537753164768219,
    "virtual_spectrum_summary": 0.18441349267959595,
    "yield": 0.46014687418937683
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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 320
    },
    {
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 1e-06
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 290
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
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 1e-06
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 290
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
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.000999
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 290
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
  "end_step": 174,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.3013380467891693,
    "conversion": 0.993442714214325,
    "cost": 1.0,
    "crystal_csd_quality": 0.5338411927223206,
    "crystal_fines_fraction": 0.9936850070953369,
    "crystal_purity": 0.9935402870178223,
    "crystal_size": 0.04006001353263855,
    "crystal_yield": 0.39031660556793213,
    "degradation_warning": 0.02893245965242386,
    "safety_risk": 0.17122675478458405,
    "score": 0.3699386417865753,
    "selectivity": 0.4712918698787689,
    "virtual_spectrum_summary": 0.17875553667545319,
    "yield": 0.4492444396018982
  },
  "ordinal": 11
}
```

## Batch 12

```json
{
  "actions": [
    {
      "amount_mol": 0.01,
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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 320
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
      "target_temperature_K": 280
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
  "end_step": 185,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.1846584975719452,
    "conversion": 0.8908991813659668,
    "cost": 1.0,
    "crystal_csd_quality": 0.6707282066345215,
    "crystal_fines_fraction": 0.555034339427948,
    "crystal_purity": 0.9937556385993958,
    "crystal_size": 0.09684911370277405,
    "crystal_yield": 0.4494923949241638,
    "degradation_warning": 0.05090538412332535,
    "safety_risk": 0.09818856418132782,
    "score": 0.487234890460968,
    "selectivity": 0.6261336207389832,
    "virtual_spectrum_summary": 0.12446960061788559,
    "yield": 0.5601160526275635
  },
  "ordinal": 12
}
```

## Batch 13

```json
{
  "actions": [
    {
      "amount_mol": 0.02,
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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 320
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
      "target_temperature_K": 280
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
  "end_step": 196,
  "lifecycle_index": 13,
  "metrics": {
    "byproduct_signal": 0.254915326833725,
    "conversion": 0.9126357436180115,
    "cost": 1.0,
    "crystal_csd_quality": 0.5082453489303589,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.978614866733551,
    "crystal_size": 0.06361861526966095,
    "crystal_yield": 0.36971229314804077,
    "degradation_warning": 0.035739533603191376,
    "safety_risk": 0.11855021119117737,
    "score": 0.3597116470336914,
    "selectivity": 0.48939964175224304,
    "virtual_spectrum_summary": 0.15628622472286224,
    "yield": 0.4404454529285431
  },
  "ordinal": 13
}
```

## Batch 14

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
      "catalyst_amount_mol": 0.0025,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 320
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
      "target_temperature_K": 280
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
  "end_step": 207,
  "lifecycle_index": 14,
  "metrics": {
    "byproduct_signal": 0.3125726580619812,
    "conversion": 0.937562882900238,
    "cost": 1.0,
    "crystal_csd_quality": 0.5312744379043579,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9595831632614136,
    "crystal_size": 0.09249236434698105,
    "crystal_yield": 0.314701110124588,
    "degradation_warning": 0.0357728973031044,
    "safety_risk": 0.13600169122219086,
    "score": 0.3325398564338684,
    "selectivity": 0.3901965320110321,
    "virtual_spectrum_summary": 0.1880127638578415,
    "yield": 0.35694050788879395
  },
  "ordinal": 14
}
```

## Batch 15

```json
{
  "actions": [
    {
      "amount_mol": 0.006,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.0015,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 320
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
      "target_temperature_K": 280
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
  "end_step": 218,
  "lifecycle_index": 15,
  "metrics": {
    "byproduct_signal": 0.18692252039909363,
    "conversion": 0.8150604963302612,
    "cost": 1.0,
    "crystal_csd_quality": 0.5333900451660156,
    "crystal_fines_fraction": 0.7711122035980225,
    "crystal_purity": 0.9870068430900574,
    "crystal_size": 0.07679494470357895,
    "crystal_yield": 0.3349475562572479,
    "degradation_warning": 0.045805737376213074,
    "safety_risk": 0.0864729955792427,
    "score": 0.40069854259490967,
    "selectivity": 0.6368129253387451,
    "virtual_spectrum_summary": 0.12341997027397156,
    "yield": 0.520330011844635
  },
  "ordinal": 15
}
```

## Batch 16

```json
{
  "actions": [
    {
      "amount_mol": 0.008,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.0015,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 320
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
      "target_temperature_K": 280
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
  "end_step": 229,
  "lifecycle_index": 16,
  "metrics": {
    "byproduct_signal": 0.20263805985450745,
    "conversion": 0.8130552768707275,
    "cost": 1.0,
    "crystal_csd_quality": 0.6041435599327087,
    "crystal_fines_fraction": 0.5343047976493835,
    "crystal_purity": 0.9770591855049133,
    "crystal_size": 0.07986841350793839,
    "crystal_yield": 0.33643627166748047,
    "degradation_warning": 0.054613299667835236,
    "safety_risk": 0.09053515642881393,
    "score": 0.4271688759326935,
    "selectivity": 0.5764229893684387,
    "virtual_spectrum_summary": 0.13602691888809204,
    "yield": 0.4725481867790222
  },
  "ordinal": 16
}
```

## Batch 17

```json
{
  "actions": [
    {
      "amount_mol": 0.012,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.0015,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 320
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
      "target_temperature_K": 280
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
  "end_step": 240,
  "lifecycle_index": 17,
  "metrics": {
    "byproduct_signal": 0.25519779324531555,
    "conversion": 0.8485113978385925,
    "cost": 1.0,
    "crystal_csd_quality": 0.7137234807014465,
    "crystal_fines_fraction": 0.36713579297065735,
    "crystal_purity": 0.998577892780304,
    "crystal_size": 0.07437296956777573,
    "crystal_yield": 0.3281315863132477,
    "degradation_warning": 0.04502042382955551,
    "safety_risk": 0.09799554198980331,
    "score": 0.45538759231567383,
    "selectivity": 0.4845404624938965,
    "virtual_spectrum_summary": 0.16061797738075256,
    "yield": 0.4183909296989441
  },
  "ordinal": 17
}
```

## Batch 18

```json
{
  "actions": [
    {
      "amount_mol": 0.01,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.002,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 320
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
      "target_temperature_K": 285
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
  "end_step": 251,
  "lifecycle_index": 18,
  "metrics": {
    "byproduct_signal": 0.2137804925441742,
    "conversion": 0.9106025099754333,
    "cost": 1.0,
    "crystal_csd_quality": 0.6845979690551758,
    "crystal_fines_fraction": 0.5515600442886353,
    "crystal_purity": 0.9942390322685242,
    "crystal_size": 0.1205911636352539,
    "crystal_yield": 0.30380114912986755,
    "degradation_warning": 0.05184850096702576,
    "safety_risk": 0.09675629436969757,
    "score": 0.4496726393699646,
    "selectivity": 0.570801317691803,
    "virtual_spectrum_summary": 0.14091110229492188,
    "yield": 0.5292718410491943
  },
  "ordinal": 18
}
```

## Batch 19

```json
{
  "actions": [
    {
      "amount_mol": 0.01,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.002,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 320
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
      "target_temperature_K": 285
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
  "end_step": 262,
  "lifecycle_index": 19,
  "metrics": {
    "byproduct_signal": 0.23460139334201813,
    "conversion": 0.8953210115432739,
    "cost": 1.0,
    "crystal_csd_quality": 0.7280305624008179,
    "crystal_fines_fraction": 0.3903309404850006,
    "crystal_purity": 0.972967267036438,
    "crystal_size": 0.06332111358642578,
    "crystal_yield": 0.36776840686798096,
    "degradation_warning": 0.046549275517463684,
    "safety_risk": 0.0971171110868454,
    "score": 0.4787622392177582,
    "selectivity": 0.5702775716781616,
    "virtual_spectrum_summary": 0.1499779373407364,
    "yield": 0.5189279317855835
  },
  "ordinal": 19
}
```

## Batch 20

```json
{
  "actions": [
    {
      "amount_mol": 0.01,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.002,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 320
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
  "end_step": 273,
  "lifecycle_index": 20,
  "metrics": {
    "byproduct_signal": 0.23230336606502533,
    "conversion": 0.8978830575942993,
    "cost": 1.0,
    "crystal_csd_quality": 0.719599723815918,
    "crystal_fines_fraction": 0.37143465876579285,
    "crystal_purity": 0.9916180372238159,
    "crystal_size": 0.0783950686454773,
    "crystal_yield": 0.4000967741012573,
    "degradation_warning": 0.05067317560315132,
    "safety_risk": 0.09720998257398605,
    "score": 0.4920301139354706,
    "selectivity": 0.5818781852722168,
    "virtual_spectrum_summary": 0.15056978166103363,
    "yield": 0.5106199979782104
  },
  "ordinal": 20
}
```

## Batch 21

```json
{
  "actions": [
    {
      "amount_mol": 0.009,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.002,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 320
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
  "end_step": 284,
  "lifecycle_index": 21,
  "metrics": {
    "byproduct_signal": 0.20027966797351837,
    "conversion": 0.8898858428001404,
    "cost": 1.0,
    "crystal_csd_quality": 0.7441939115524292,
    "crystal_fines_fraction": 0.36878904700279236,
    "crystal_purity": 0.9890995621681213,
    "crystal_size": 0.062286362051963806,
    "crystal_yield": 0.41868487000465393,
    "degradation_warning": 0.04976779222488403,
    "safety_risk": 0.09507377445697784,
    "score": 0.5042739510536194,
    "selectivity": 0.5855867862701416,
    "virtual_spectrum_summary": 0.13254933059215546,
    "yield": 0.5455206036567688
  },
  "ordinal": 21
}
```

## Batch 22

```json
{
  "actions": [
    {
      "amount_mol": 0.011,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.002,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 320
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
  "end_step": 295,
  "lifecycle_index": 22,
  "metrics": {
    "byproduct_signal": 0.24354417622089386,
    "conversion": 0.9113133549690247,
    "cost": 1.0,
    "crystal_csd_quality": 0.7053772211074829,
    "crystal_fines_fraction": 0.433487206697464,
    "crystal_purity": 1.0,
    "crystal_size": 0.07330558449029922,
    "crystal_yield": 0.3937646150588989,
    "degradation_warning": 0.051010746508836746,
    "safety_risk": 0.09929119795560837,
    "score": 0.4779238700866699,
    "selectivity": 0.5416868925094604,
    "virtual_spectrum_summary": 0.15690413117408752,
    "yield": 0.49194300174713135
  },
  "ordinal": 22
}
```

## Batch 23

```json
{
  "actions": [
    {
      "amount_mol": 0.012,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.002,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 320
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
  "end_step": 306,
  "lifecycle_index": 23,
  "metrics": {
    "byproduct_signal": 0.2491808384656906,
    "conversion": 0.9063751101493835,
    "cost": 1.0,
    "crystal_csd_quality": 0.6762254238128662,
    "crystal_fines_fraction": 0.5237010717391968,
    "crystal_purity": 0.9961454272270203,
    "crystal_size": 0.09246367961168289,
    "crystal_yield": 0.3808586001396179,
    "degradation_warning": 0.04305937886238098,
    "safety_risk": 0.10132177919149399,
    "score": 0.46099796891212463,
    "selectivity": 0.540414571762085,
    "virtual_spectrum_summary": 0.15642617642879486,
    "yield": 0.4946417808532715
  },
  "ordinal": 23
}
```

## Batch 24

```json
{
  "actions": [
    {
      "amount_mol": 0.014,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.002,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 320
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
  "end_step": 317,
  "lifecycle_index": 24,
  "metrics": {
    "byproduct_signal": 0.26381176710128784,
    "conversion": 0.9181843400001526,
    "cost": 1.0,
    "crystal_csd_quality": 0.5722769498825073,
    "crystal_fines_fraction": 0.7780020236968994,
    "crystal_purity": 1.0,
    "crystal_size": 0.06381823867559433,
    "crystal_yield": 0.35956260561943054,
    "degradation_warning": 0.043454546481370926,
    "safety_risk": 0.1052461713552475,
    "score": 0.40159183740615845,
    "selectivity": 0.5004249215126038,
    "virtual_spectrum_summary": 0.164651021361351,
    "yield": 0.4680871367454529
  },
  "ordinal": 24
}
```

## K1

```json
{
  "payload": {
    "report": "Recommended process and observed result\n\nBatch 21 used 0.009 mol reagent, 0.080 L solvent-S2, and 0.002 mol catalyst-C1. It was heated at 320 K for 2400 s with 300 rpm stirring, quenched, seeded with 0.001 g, cooled to 285 K for 14,400 s and then to 250 K for 14,400 s, filtered, and assayed. The final assay gave reaction conversion 0.890, selectivity 0.586, reaction yield 0.546, byproduct signal 0.200, degradation warning 0.050, seed-excluded crystal recovery 0.419, crystal purity 0.989, fines fraction 0.369, and CSD quality 0.744. It had the highest observed recovery among batches satisfying purity >=0.80 and fines <=0.50.\n\nMaterial effects\n\nObserved: solvent identity affected both reaction and crystallization, but the solvent screen was performed in a high-loading regime. Under otherwise similar conditions in batches 5\u20138, solvent-S0 gave the highest reaction selectivity and crystal recovery (0.580 and 0.466), whereas S1, S2, and S3 gave recoveries of 0.442, 0.426, and 0.436. However, every member of that screen had an unacceptable fines fraction near 1.0. S3 produced the largest reported size index in that screen, while S0 gave the strongest reaction performance. Thus, high recovery from S0 did not translate into a constraint-feasible process.\n\nInterpretation: solvent-S2\u2019s nominal low solubility, low nucleation tendency, high crystal-growth tendency, and low impurity-occlusion tendency made it a reasonable solvent for developing a lower-concentration crystallization window. The successful S2 result should not be interpreted as proof that S2 is globally superior; S0 was never retested in the final low-loading protocol. The nominal material dossier was useful as a prior but did not predict the high-loading ranking by itself.\n\nCatalyst-C1 was used throughout the main campaign. Consequently, no experimental catalyst ranking was established. Its nominal activity and the achieved conversions support its adequacy, but alternatives C0, C2, and C3 remain untested under the recommended recipe.\n\nReaction\u2013crystallization coupling\n\nThe central empirical effect was reagent concentration. At 0.04 mol reagent in 0.08 L solvent, conversion was usually close to unity, but selectivity was modest and the crystal population was dominated by fines. For example, batch 1 reached conversion 1.000 but had selectivity 0.471, byproduct signal 0.355, recovery 0.383, and fines 0.997. In the matched loading study, batch 12 at 0.010 mol gave recovery 0.449 and fines 0.555, while batches 13 and 14 at 0.020 and 0.030 mol gave recoveries of 0.370 and 0.315 with fines of 1.000. Lower loading therefore created the only observed route toward acceptable number-weighted particle quality.\n\nA useful conceptual description is reaction yield approximately equal to conversion times selectivity, Y_rxn \u2248 X\u00b7S, while the crystallization-stage recovery is R_cryst = n(target recovered as crystals, excluding seed)/n(target present before separation). Overall isolated target per charged reagent would scale approximately as Y_rxn\u00b7R_cryst. Because the campaign objective defined recovery only across crystallization, a lower-concentration batch can have good R_cryst even though it makes less absolute product per vessel.\n\nThe likely coupling variable is supersaturation, which may be represented as \u03c3=(C\u2212C*)/C*. Classical empirical forms J=k_n\u03c3^n for nucleation and G=k_g\u03c3^g for growth are useful here. If nucleation has the stronger supersaturation dependence, increasing concentration creates many nuclei faster than it increases growth, producing a high number fraction below 20 \u03bcm. This interpretation is consistent with the loading studies, but nucleation and growth rates were not directly measured.\n\nProcess-history dependence\n\nReaction history mattered. Batch 1\u2019s relatively severe 350 K, 3600 s treatment gave degradation warning 0.152 and byproduct signal 0.355. Reducing severity lowered degradation: batch 2, treated at 330 K for 1800 s, had degradation warning 0.052. The final 320 K, 2400 s treatment retained about 0.89 conversion while improving the balance between selectivity and crystallization behavior. A generic history model would integrate temperature-dependent rates, such as X=1\u2212exp[\u2212\u222bk_rxn(T)dt], while degradation accumulates through a separate \u222bk_deg(T)C_product dt term. The data support avoiding unnecessary high-temperature residence, though they do not identify activation energies.\n\nCrystallization was strongly path dependent rather than determined solely by final temperature. Unseeded staged cooling in batch 2 produced recovery 0.402 but fines 1.000. Very long stirred aging in batch 3 did not ripen away the fines: after extensive holds it still gave fines 0.995 and a size index of 0.028. Batch 4 combined maximum seed addition with a heat/cool cycle but still produced fines 1.000. Batch 9 stopped at 295 K after adding 0.05 g seed and gave only 0.345 recovery with fines 1.000. Repeated nominally isothermal crystallization at 295 K in batch 10 also failed, giving recovery 0.346 and fines 1.000. These observations argue that prolonged residence, thermal cycling, or more seed alone cannot compensate for excessive initial supersaturation in this system.\n\nWithin the lower-loading regime, the terminal cooling temperature was important. Batches 18\u201320 all used 0.010 mol reagent, 0.002 mol C1, 0.080 L S2, a 285 K first cooling stage, and final stages at 270, 260, and 250 K. Recovery increased from 0.304 to 0.368 to 0.400. Their fines fractions were 0.552, 0.390, and 0.371. Thus, in this observed window, deeper second-stage cooling increased recovery without causing the expected fines penalty. I interpret the initial 285 K stage and small seed charge as establishing a controlled crystal population before the deeper recovery-driving cool. This remains a mechanistic interpretation rather than a directly observed nucleation sequence.\n\nRevisions during the campaign\n\nThe initial strategy emphasized complete reaction, S2\u2019s favorable nominal crystallization properties, extended aging, and thermal manipulation. Batches 1\u201311 showed that those measures did not solve the fines constraint at 0.04 mol loading. The strategy was therefore revised to reduce reagent concentration. Batch 12 nearly met the fines limit at 0.010 mol, and batch 17 first clearly satisfied it at 0.012 mol, although recovery was only 0.328. The cooling endpoint study then identified 250 K as the best tested endpoint. A final local loading search produced batch 21 at 0.009 mol with recovery 0.419 and fines 0.369. Neighboring batches demonstrate a narrow feasible region: batch 22 at 0.011 mol remained feasible with recovery 0.394 and fines 0.433, but batch 23 at 0.012 mol failed slightly at fines 0.524, and batch 24 at 0.014 mol failed clearly at 0.778.\n\nUncertainty and unresolved tradeoffs\n\nPurity was not the limiting attribute: nearly all developed crystallizations had purity around 0.97\u20131.00, far above the 0.80 threshold. The unresolved tradeoff is recovery versus fines. The highest recoveries observed overall were batch 5 at 0.466 and batch 12 at 0.449, but their fines fractions were 1.000 and 0.555. Batch 21 sacrifices some recovery to obtain a substantial fines margin. Its recovery advantage over feasible batch 20 (0.400) and batch 22 (0.394) is modest, so the precise ranking is less certain than the conclusion that all three define a promising operating region.\n\nEach batch received only one final assay, and no exact process replicate was run. Instrument noise, batch variability, and the non-factorial evolution of conditions limit causal inference. Seed amount, catalyst amount, reaction residence, and loading were sometimes changed together. Solvent effects were not rescreened under the final low-loading protocol, catalyst alternatives were not tested, and absolute isolated mass or productivity was not optimized. The fines response was also non-monotonic in some intermediate batches, indicating either nonlinear crystallization dynamics or measurement/process variability. Accordingly, batch 21 is supported as the best observed constrained result, not as proof of a global optimum."
  },
  "failure": null,
  "elapsed_s": 68.73500000001513,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 692608,
    "input_tokens": 773460,
    "output_tokens": 10278,
    "reasoning_output_tokens": 3625
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
          "estimate": 0.985,
          "lower80": 0.95,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.1,
          "lower80": 0.068,
          "upper80": 0.14
        },
        "crystal_yield": {
          "estimate": 0.4,
          "lower80": 0.31,
          "upper80": 0.49
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q01"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.57,
          "lower80": 0.4,
          "upper80": 0.74
        },
        "crystal_purity": {
          "estimate": 0.972,
          "lower80": 0.93,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.074,
          "lower80": 0.046,
          "upper80": 0.11
        },
        "crystal_yield": {
          "estimate": 0.34,
          "lower80": 0.25,
          "upper80": 0.44
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q02"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.24,
          "lower80": 0.1,
          "upper80": 0.43
        },
        "crystal_purity": {
          "estimate": 0.965,
          "lower80": 0.91,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.125,
          "lower80": 0.082,
          "upper80": 0.18
        },
        "crystal_yield": {
          "estimate": 0.29,
          "lower80": 0.2,
          "upper80": 0.39
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q03"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.57,
          "lower80": 0.39,
          "upper80": 0.75
        },
        "crystal_purity": {
          "estimate": 0.968,
          "lower80": 0.92,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.074,
          "lower80": 0.046,
          "upper80": 0.11
        },
        "crystal_yield": {
          "estimate": 0.31,
          "lower80": 0.22,
          "upper80": 0.41
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q04"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.44,
          "lower80": 0.28,
          "upper80": 0.62
        },
        "crystal_purity": {
          "estimate": 0.97,
          "lower80": 0.92,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.09,
          "lower80": 0.058,
          "upper80": 0.132
        },
        "crystal_yield": {
          "estimate": 0.32,
          "lower80": 0.23,
          "upper80": 0.42
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q05"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.78,
          "lower80": 0.61,
          "upper80": 0.92
        },
        "crystal_purity": {
          "estimate": 0.955,
          "lower80": 0.89,
          "upper80": 0.995
        },
        "crystal_size": {
          "estimate": 0.052,
          "lower80": 0.028,
          "upper80": 0.085
        },
        "crystal_yield": {
          "estimate": 0.33,
          "lower80": 0.23,
          "upper80": 0.43
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q06"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.34,
          "lower80": 0.19,
          "upper80": 0.52
        },
        "crystal_purity": {
          "estimate": 0.971,
          "lower80": 0.92,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.105,
          "lower80": 0.068,
          "upper80": 0.153
        },
        "crystal_yield": {
          "estimate": 0.33,
          "lower80": 0.24,
          "upper80": 0.43
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q07"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.58,
          "lower80": 0.39,
          "upper80": 0.76
        },
        "crystal_purity": {
          "estimate": 0.981,
          "lower80": 0.94,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.073,
          "lower80": 0.043,
          "upper80": 0.111
        },
        "crystal_yield": {
          "estimate": 0.24,
          "lower80": 0.14,
          "upper80": 0.35
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q08"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.9,
          "lower80": 0.73,
          "upper80": 1.0
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.92,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.045,
          "lower80": 0.019,
          "upper80": 0.078
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
          "estimate": 0.72,
          "lower80": 0.52,
          "upper80": 0.9
        },
        "crystal_purity": {
          "estimate": 0.975,
          "lower80": 0.92,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.06,
          "lower80": 0.03,
          "upper80": 0.098
        },
        "crystal_yield": {
          "estimate": 0.12,
          "lower80": 0.05,
          "upper80": 0.21
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q10"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.48,
          "lower80": 0.31,
          "upper80": 0.66
        },
        "crystal_purity": {
          "estimate": 0.969,
          "lower80": 0.92,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.084,
          "lower80": 0.053,
          "upper80": 0.125
        },
        "crystal_yield": {
          "estimate": 0.32,
          "lower80": 0.23,
          "upper80": 0.42
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q11"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.82,
          "lower80": 0.66,
          "upper80": 0.95
        },
        "crystal_purity": {
          "estimate": 0.945,
          "lower80": 0.87,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.055,
          "lower80": 0.029,
          "upper80": 0.09
        },
        "crystal_yield": {
          "estimate": 0.41,
          "lower80": 0.31,
          "upper80": 0.51
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q12"
      }
    ],
    "rationale": "These are epistemic intervals for noise-free outcomes, not final-assay noise bands. Q01\u2013Q02: S1's lower nominal solubility, nucleation tendency, and impurity occlusion should give higher recovery, purity, and particle quality than S3. Q03\u2013Q04: reducing seed from 0.045 g to 0.001 g should produce fewer but larger crystals and substantially fewer fines, with only a small recovery change. Q05\u2013Q06: gradual cooling should control supersaturation better than an immediate crash to 278.15 K; the long crash-cool hold may approach similar recovery but is expected to retain many fines. Q07\u2013Q08: continued low-temperature growth should preserve recovery and improve size, whereas reheating to 315 K can redissolve product and the short recooling step may regenerate fines before full recovery. Q09\u2013Q10: both contain seed particles, but the added 7200 s hold should raise seed-excluded recovery and permit growth; 292 K remains too warm and the residence too short for likely feasibility. Q11\u2013Q12: doubling reagent loading should increase supersaturation and recovery but strongly increase secondary nucleation, fines, and impurity occlusion. Uncertainty is broad because these recipes extrapolate to S0/S1/S3, unusually slow ramps, high relative seed charges, and a 385 K reaction history not replicated in the campaign; predictions near the 0.50 fines boundary are especially uncertain."
  },
  "failure": null,
  "elapsed_s": 83.18799999999464,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 692608,
    "input_tokens": 822813,
    "output_tokens": 14386,
    "reasoning_output_tokens": 6004
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
    "report": "1. Status of the main claims\n\nSupported by direct observations:\n- Loading was the clearest control on fines. In the matched series, batch 12 at 0.010 mol reagent gave fines 0.555, whereas batches 13 and 14 at 0.020 and 0.030 mol gave fines 1.000. In the final local series, batches 21\u201324 increased loading from 0.009 to 0.014 mol while fines rose from 0.369 to 0.778 overall; batches 23 and 24 failed the fines constraint. This supports a concentration/supersaturation effect, although the non-monotonic intermediate campaign results preclude a precise response law.\n- Deeper final cooling improved recovery in the tested low-loading path. Batches 18, 19, and 20 ended at 270, 260, and 250 K and gave recoveries 0.304, 0.368, and 0.400. Their fines also fell from 0.552 to 0.390 and 0.371. The numerical trend is observed directly; the proposed explanation\u2014controlled population establishment at 285 K followed by growth and recovery\u2014is interpretive.\n- Extended residence alone did not cure high-loading fines. Batch 3 used extensive aging but ended with fines 0.995. Repeated crystallization holds in batch 10 also left fines at 1.000. Batch 4\u2019s heat/cool cycle and large seed charge likewise gave fines 1.000. Thus, long time, cycling, or high seed was not sufficient under those conditions.\n- Purity was not the active constraint. Developed batches generally had purity near 0.97\u20131.00, including feasible batch 21 at 0.989. Fines, rather than purity, separated feasible from infeasible conditions.\n- Batch 21 was the best observed constrained result: recovery 0.419, purity 0.989, and fines 0.369. This is an empirical campaign ranking, not proof of a global optimum.\n\nPartly supported but still interpretive:\n- Severe reaction history appeared detrimental. Batch 1 at 350 K for 3600 s had degradation warning 0.152 and byproduct signal 0.355, while batch 2 at 330 K for 1800 s had degradation warning 0.052 and byproduct signal 0.291. Temperature and residence changed together, so attributing the difference specifically to temperature-dependent degradation remains tentative.\n- The proposed supersaturation mechanism is consistent with the loading trends: higher concentration plausibly raised nucleation faster than growth and generated more fines. Supersaturation, nucleation rate, and growth rate were not measured directly, so equations such as J=k_n\u03c3^n and G=k_g\u03c3^g are explanatory models rather than fitted laws.\n- The apparent narrow feasible window is supported by batches 20\u201324, but only one final assay was obtained per condition. Batch 17 passed at 0.012 mol with fines 0.367, while batch 23 at the same nominal reagent amount but a different catalyst amount/history gave fines 0.524. This shows both history dependence and unresolved variability.\n\nContradicted or not supported as a general claim:\n- A broad claim that S2 is the best solvent is not supported. In the high-loading solvent screen, batch 5 using S0 had the highest recovery and reaction selectivity, 0.466 and 0.580, compared with batch 7 using S2 at 0.426 and 0.437. All four solvent-screen batches failed the fines constraint, so the screen does not establish the best solvent in the final low-loading regime. S2 was a successful development choice, not a demonstrated global winner.\n- A simple claim that more aging necessarily produces larger, cleaner particles is contradicted by batch 3 and batch 10.\n- A simple claim that reheating necessarily removes fines is contradicted as a sufficient rule by batch 4, although that experiment does not rule out a beneficial cycle in another concentration regime.\n\nStill untested:\n- Catalyst effects remain untested because the developed batches used C1; C0, C2, and C3 were not compared under a matched protocol.\n- The causal effect of seed mass is unresolved. High-seed batches 4 and 9 had poor fines, but low-seed batch 11 also had poor fines at high loading. There was no clean matched seed-dose experiment in the final concentration window.\n- S0, S1, and S3 were not tested using the batch-21 low-loading cooling history. Likewise, productivity, absolute isolated mass, and exact replication variance remain unknown.\n\n2. One additional experiment\n\nI would repeat batch 21 exactly but replace solvent-S2 with solvent-S0: 0.009 mol reagent, 0.080 L S0, 0.002 mol C1, 320 K for 2400 s at 300 rpm, quench, 0.001 g seed, 14,400 s to 285 K, another 14,400 s to 250 K, filter, terminate, and final assay. If permitted within the single experiment, I would also take an intermediate HPLC measurement before crystallization to separate reaction effects from crystallization effects.\n\nThis directly tests two competing explanations. Under the material-property explanation, S2 is important because its lower nominal solubility, lower nucleation tendency, faster growth, and lower occlusion create the feasible particle distribution; S0 should then give lower or similar recovery, more fines, and possibly lower purity. Under the process-dominant explanation, low loading and staged cooling\u2014not S2 identity\u2014create feasibility. If the high-loading solvent ranking generalizes, S0 might retain acceptable fines while improving reaction selectivity or recovery, potentially outperforming batch 21. An intermediate reaction measurement would show whether any final advantage arose from making a better feed or from recovering that feed more effectively as crystals.\n\n3. Least effectively used observation and least reliable prediction\n\nThe least effectively used observation was batch 5. S0 produced the campaign\u2019s highest observed recovery, 0.466, and the strongest reaction selectivity in the solvent screen, yet subsequent optimization remained almost entirely in S2. Its fines fraction of 1.000 justified not recommending batch 5 itself, but it did not justify abandoning S0 before testing whether low loading could solve its fines problem. Consequently, the account relied more heavily on nominal solvent properties than the S0 observation warranted.\n\nThe least reliable held-out prediction is Q08. It combines a long gradual crystallization, reheating to 315 K with stirring, and a short recooling step. Its result depends on unmeasured dissolution kinetics, how much of the crystal population survives reheating, impurity release, attrition, and whether recooling favors growth on survivors or renewed nucleation. Batch 4 is the only remotely analogous campaign observation, but it used materially different loading, seed mass, and thermal history, so it cannot calibrate Q08 cleanly. The sealed Q08 estimate therefore rests on a qualitative redissolution\u2013renucleation interpretation and has greater structural uncertainty than predictions based mainly on the directly observed loading or final-temperature trends."
  },
  "failure": null,
  "elapsed_s": 60.125,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 730368,
    "input_tokens": 876194,
    "output_tokens": 16816,
    "reasoning_output_tokens": 6905
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
    "selection_rationale": "Highest observed seed-excluded crystal recovery among completed batches meeting both constraints: crystal_yield 0.419, crystal_purity 0.989, and fines fraction 0.369."
  },
  "recommendation_recipe": {
    "actions": [
      {
        "amount_mol": 0.009,
        "operation": "add_reagent"
      },
      {
        "operation": "add_solvent",
        "solvent": 2,
        "volume_L": 0.08
      },
      {
        "catalyst": 1,
        "catalyst_amount_mol": 0.002,
        "operation": "add_catalyst"
      },
      {
        "duration_s": 2400,
        "operation": "heat",
        "stirring_speed_rpm": 300,
        "target_temperature_K": 320
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
    "excluded_rejected_attempts": [],
    "lifecycle_index": 21,
    "source_attempts": 11
  },
  "prediction_evaluation": {
    "contrasts": [
      {
        "absolute_delta_error": 0.005711584904441791,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_yield",
        "predicted_delta": -0.06,
        "resolved": true,
        "true_delta": -0.06571158490444179
      },
      {
        "absolute_delta_error": 0.010123577190615296,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_purity",
        "predicted_delta": -0.013000000000000012,
        "resolved": false,
        "true_delta": -0.0028764228093847155
      },
      {
        "absolute_delta_error": 0.045004936280756316,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_size",
        "predicted_delta": -0.02600000000000001,
        "resolved": true,
        "true_delta": 0.019004936280756307
      },
      {
        "absolute_delta_error": 0.8976947480077399,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.18999999999999995,
        "resolved": true,
        "true_delta": -0.7076947480077399
      },
      {
        "absolute_delta_error": 0.02008776257407513,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_yield",
        "predicted_delta": 0.020000000000000018,
        "resolved": false,
        "true_delta": -8.776257407511201e-05
      },
      {
        "absolute_delta_error": 0.005582735806473504,
        "direction_correct": true,
        "factor": "seed",
        "metric": "crystal_purity",
        "predicted_delta": 0.0030000000000000027,
        "resolved": false,
        "true_delta": 0.008582735806473507
      },
      {
        "absolute_delta_error": 0.051874876724198826,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_size",
        "predicted_delta": -0.051000000000000004,
        "resolved": false,
        "true_delta": 0.0008748767241988226
      },
      {
        "absolute_delta_error": 0.29862076842232305,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.32999999999999996,
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
        "absolute_delta_error": 0.01079492324721476,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.015000000000000013,
        "resolved": false,
        "true_delta": -0.004205076752785253
      },
      {
        "absolute_delta_error": 0.008548493674474335,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_size",
        "predicted_delta": -0.038,
        "resolved": true,
        "true_delta": -0.046548493674474334
      },
      {
        "absolute_delta_error": 0.40020093924299244,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.34,
        "resolved": true,
        "true_delta": 0.7402009392429925
      },
      {
        "absolute_delta_error": 0.13146629297589668,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_yield",
        "predicted_delta": -0.09000000000000002,
        "resolved": true,
        "true_delta": 0.04146629297589666
      },
      {
        "absolute_delta_error": 0.019830577525981608,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_purity",
        "predicted_delta": 0.010000000000000009,
        "resolved": false,
        "true_delta": -0.009830577525981599
      },
      {
        "absolute_delta_error": 0.008638559972026026,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_size",
        "predicted_delta": -0.032,
        "resolved": true,
        "true_delta": -0.04063855997202603
      },
      {
        "absolute_delta_error": 0.5278652105803905,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.23999999999999994,
        "resolved": true,
        "true_delta": 0.7678652105803905
      },
      {
        "absolute_delta_error": 0.033000389625297916,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_yield",
        "predicted_delta": 0.095,
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
        "absolute_delta_error": 0.20884240834118417,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.18000000000000005,
        "resolved": false,
        "true_delta": 0.028842408341184123
      },
      {
        "absolute_delta_error": 0.057463253168567874,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_yield",
        "predicted_delta": 0.08999999999999997,
        "resolved": true,
        "true_delta": 0.032536746831432095
      },
      {
        "absolute_delta_error": 0.018192382855165667,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_purity",
        "predicted_delta": -0.02400000000000002,
        "resolved": false,
        "true_delta": -0.005807617144834354
      },
      {
        "absolute_delta_error": 0.005388280811496872,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_size",
        "predicted_delta": -0.029000000000000005,
        "resolved": true,
        "true_delta": -0.03438828081149688
      },
      {
        "absolute_delta_error": 0.40102589522834886,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.33999999999999997,
        "resolved": true,
        "true_delta": 0.7410258952283488
      }
    ],
    "failures": [],
    "metrics": {
      "crystal_fines_fraction": {
        "coverage80": 0.25,
        "interval_score80": 1.329998206720009,
        "interval_width": 0.3325,
        "mae": 0.23950229100791173,
        "n": 12,
        "planned": 12
      },
      "crystal_purity": {
        "coverage80": 1.0,
        "interval_score80": 0.08124999999999998,
        "interval_width": 0.08124999999999998,
        "mae": 0.01630575854052657,
        "n": 12,
        "planned": 12
      },
      "crystal_size": {
        "coverage80": 0.9166666666666666,
        "interval_score80": 0.07268957366546468,
        "interval_width": 0.07016666666666667,
        "mae": 0.014674039167686038,
        "n": 12,
        "planned": 12
      },
      "crystal_yield": {
        "coverage80": 0.9166666666666666,
        "interval_score80": 0.18802121328401264,
        "interval_width": 0.18083333333333332,
        "mae": 0.05520360460569945,
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
    "tie_correct": 2,
    "tie_n": 10,
    "valid": true
  },
  "public_baselines": {
    "available": true,
    "mae": {
      "public_mean": {
        "crystal_fines_fraction": 0.3646230122888186,
        "crystal_purity": 0.004258136444004394,
        "crystal_size": 0.02042290368685602,
        "crystal_yield": 0.14016698173615258
      },
      "public_nearest_neighbor": {
        "crystal_fines_fraction": 0.3706460696280573,
        "crystal_purity": 0.008601697191293556,
        "crystal_size": 0.03648120592255329,
        "crystal_yield": 0.12181319541665836
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
        "cached_input": 692608,
        "input": 735572,
        "output": 7349,
        "stage": "source",
        "uncached_input": 42964
      },
      {
        "cached_input": 0,
        "input": 37888,
        "output": 2929,
        "stage": "K1",
        "uncached_input": 37888
      },
      {
        "cached_input": 0,
        "input": 49353,
        "output": 4108,
        "stage": "Q",
        "uncached_input": 49353
      },
      {
        "cached_input": 37760,
        "input": 53381,
        "output": 2430,
        "stage": "K2",
        "uncached_input": 15621
      }
    ],
    "total": {
      "cached_input": 730368,
      "input": 876194,
      "input_plus_output": 893010,
      "output": 16816,
      "uncached_input": 145826
    },
    "valid": true
  },
  "elapsed_s": 526.9689999999828
}
```
