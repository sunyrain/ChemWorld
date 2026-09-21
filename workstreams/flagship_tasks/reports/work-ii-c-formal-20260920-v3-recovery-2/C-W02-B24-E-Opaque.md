# C-W02-B24-E-Opaque

Status: failed

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
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.02
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
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
  "end_step": 12,
  "lifecycle_index": 1,
  "metrics": {
    "byproduct_signal": 0.22398467361927032,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5005732774734497,
    "crystal_fines_fraction": 0.9973341822624207,
    "crystal_purity": 0.9793447256088257,
    "crystal_size": 0.047295305877923965,
    "crystal_yield": 0.5406267642974854,
    "degradation_warning": 0.09098739176988602,
    "safety_risk": 0.15372173488140106,
    "score": 0.4402913749217987,
    "selectivity": 0.6748496294021606,
    "virtual_spectrum_summary": 0.1641358882188797,
    "yield": 0.6726759076118469
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
      "target_temperature_K": 340
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
      "target_temperature_K": 295
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
  "end_step": 26,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.2560060918331146,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5401357412338257,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9835423827171326,
    "crystal_size": 0.0764043852686882,
    "crystal_yield": 0.46742916107177734,
    "degradation_warning": 0.07429186254739761,
    "safety_risk": 0.14370350539684296,
    "score": 0.4191308915615082,
    "selectivity": 0.6016806960105896,
    "virtual_spectrum_summary": 0.17423468828201294,
    "yield": 0.5901917815208435
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
      "target_temperature_K": 340
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
      "target_temperature_K": 300
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 295
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
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 1e-06
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
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.005
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
  "end_step": 58,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.32952386140823364,
    "conversion": 0.9972810745239258,
    "cost": 1.0,
    "crystal_csd_quality": 0.501045823097229,
    "crystal_fines_fraction": 0.9949183464050293,
    "crystal_purity": 0.9730884432792664,
    "crystal_size": 0.04122631251811981,
    "crystal_yield": 0.2989717423915863,
    "degradation_warning": 0.06086380407214165,
    "safety_risk": 0.12207712978124619,
    "score": 0.3327643573284149,
    "selectivity": 0.4209434390068054,
    "virtual_spectrum_summary": 0.20862682163715363,
    "yield": 0.41962072253227234
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
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.001
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 300
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.004
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
  "end_step": 75,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.23450398445129395,
    "conversion": 0.9889438152313232,
    "cost": 1.0,
    "crystal_csd_quality": 0.5446196794509888,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 1.0,
    "crystal_size": 0.03591123968362808,
    "crystal_yield": 0.5159333944320679,
    "degradation_warning": 0.06182042509317398,
    "safety_risk": 0.1721990555524826,
    "score": 0.4335825443267822,
    "selectivity": 0.6257641911506653,
    "virtual_spectrum_summary": 0.1567963808774948,
    "yield": 0.6121017932891846
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
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.005
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
  "end_step": 90,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.2943885028362274,
    "conversion": 0.9963361620903015,
    "cost": 1.0,
    "crystal_csd_quality": 0.5435212254524231,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9745715856552124,
    "crystal_size": 0.012191628105938435,
    "crystal_yield": 0.4714337885379791,
    "degradation_warning": 0.10227798670530319,
    "safety_risk": 0.18436290323734283,
    "score": 0.4056496024131775,
    "selectivity": 0.5751303434371948,
    "virtual_spectrum_summary": 0.2079387754201889,
    "yield": 0.5689764618873596
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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 340
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
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 1200
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 1200
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 1200
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 1200
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
  "end_step": 105,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.3282785713672638,
    "conversion": 0.9923936128616333,
    "cost": 1.0,
    "crystal_csd_quality": 0.4924090504646301,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.983095645904541,
    "crystal_size": 0.026966994628310204,
    "crystal_yield": 0.3884717524051666,
    "degradation_warning": 0.09341390430927277,
    "safety_risk": 0.18449601531028748,
    "score": 0.35965409874916077,
    "selectivity": 0.4732072353363037,
    "virtual_spectrum_summary": 0.22258947789669037,
    "yield": 0.4750737249851227
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
  "end_step": 118,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.22118514776229858,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.47578978538513184,
    "crystal_fines_fraction": 0.9867444038391113,
    "crystal_purity": 0.9732197523117065,
    "crystal_size": 0.07203049957752228,
    "crystal_yield": 0.5705484747886658,
    "degradation_warning": 0.0861365869641304,
    "safety_risk": 0.15457890927791595,
    "score": 0.44701987504959106,
    "selectivity": 0.6660497188568115,
    "virtual_spectrum_summary": 0.16041329503059387,
    "yield": 0.6926825046539307
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
      "operation": "quench"
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
  "end_step": 137,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.21349509060382843,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5188275575637817,
    "crystal_fines_fraction": 0.9869743585586548,
    "crystal_purity": 0.9729047417640686,
    "crystal_size": 0.0888029932975769,
    "crystal_yield": 0.5756800770759583,
    "degradation_warning": 0.09270446747541428,
    "safety_risk": 0.15384817123413086,
    "score": 0.45620012283325195,
    "selectivity": 0.6768332123756409,
    "virtual_spectrum_summary": 0.15913930535316467,
    "yield": 0.6685138940811157
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
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.005
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 278
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
  "end_step": 153,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.22394466400146484,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.4928493797779083,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9751728177070618,
    "crystal_size": 0.03927380591630936,
    "crystal_yield": 0.5666553378105164,
    "degradation_warning": 0.08530807495117188,
    "safety_risk": 0.15390683710575104,
    "score": 0.44192129373550415,
    "selectivity": 0.6567310690879822,
    "virtual_spectrum_summary": 0.16155819594860077,
    "yield": 0.6703929901123047
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
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.02
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
  "end_step": 171,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.2158219814300537,
    "conversion": 0.9856159090995789,
    "cost": 1.0,
    "crystal_csd_quality": 0.4584887623786926,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9667094349861145,
    "crystal_size": 0.05350305140018463,
    "crystal_yield": 0.5785233378410339,
    "degradation_warning": 0.0933159738779068,
    "safety_risk": 0.15036769211292267,
    "score": 0.43903952836990356,
    "selectivity": 0.6676158905029297,
    "virtual_spectrum_summary": 0.16069427132606506,
    "yield": 0.6764026880264282
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
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.005
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 305
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
  "end_step": 182,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.22533637285232544,
    "conversion": 0.9989994764328003,
    "cost": 1.0,
    "crystal_csd_quality": 0.47314345836639404,
    "crystal_fines_fraction": 0.9936748743057251,
    "crystal_purity": 0.9791083335876465,
    "crystal_size": 0.05298520252108574,
    "crystal_yield": 0.4079335033893585,
    "degradation_warning": 0.07373444736003876,
    "safety_risk": 0.1417759507894516,
    "score": 0.40296128392219543,
    "selectivity": 0.6849095225334167,
    "virtual_spectrum_summary": 0.15711550414562225,
    "yield": 0.6654055714607239
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
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 360
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
      "target_temperature_K": 310
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
      "operation": "cool_crystallize",
      "target_temperature_K": 288
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 286
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 284
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 282
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 280
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 278
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 276
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 274
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 272
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
  "end_step": 213,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.20276589691638947,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.49414893984794617,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9875063300132751,
    "crystal_size": 0.08043839037418365,
    "crystal_yield": 0.5685256123542786,
    "degradation_warning": 0.0902305543422699,
    "safety_risk": 0.15475867688655853,
    "score": 0.45056426525115967,
    "selectivity": 0.6698854565620422,
    "virtual_spectrum_summary": 0.15212498605251312,
    "yield": 0.6749003529548645
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
      "solvent": 0,
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
      "stirring_speed_rpm": 300,
      "target_temperature_K": 330
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.005
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
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
      "target_temperature_K": 285
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
  "lifecycle_index": 13,
  "metrics": {
    "byproduct_signal": 0.3071674704551697,
    "conversion": 0.9972169399261475,
    "cost": 1.0,
    "crystal_csd_quality": 0.7509474754333496,
    "crystal_fines_fraction": 0.4372459650039673,
    "crystal_purity": 0.9703015685081482,
    "crystal_size": 0.07742402702569962,
    "crystal_yield": 0.4393378496170044,
    "degradation_warning": 0.12288350611925125,
    "safety_risk": 0.14093512296676636,
    "score": 0.49822837114334106,
    "selectivity": 0.5466980338096619,
    "virtual_spectrum_summary": 0.22423969209194183,
    "yield": 0.5386855006217957
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
      "stirring_speed_rpm": 300,
      "target_temperature_K": 360
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.005
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
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
      "target_temperature_K": 285
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
  "end_step": 245,
  "lifecycle_index": 14,
  "metrics": {
    "byproduct_signal": 0.23549118638038635,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.790020763874054,
    "crystal_fines_fraction": 0.3235032558441162,
    "crystal_purity": 0.9589482545852661,
    "crystal_size": 0.11918137967586517,
    "crystal_yield": 0.6048612594604492,
    "degradation_warning": 0.09378677606582642,
    "safety_risk": 0.16113775968551636,
    "score": 0.5830658078193665,
    "selectivity": 0.6711117625236511,
    "virtual_spectrum_summary": 0.17172420024871826,
    "yield": 0.6649240255355835
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
      "solvent": 0,
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
      "stirring_speed_rpm": 300,
      "target_temperature_K": 360
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.005
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
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
      "target_temperature_K": 285
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
  "lifecycle_index": 15,
  "metrics": {
    "byproduct_signal": 0.2286268174648285,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7745200395584106,
    "crystal_fines_fraction": 0.2692260444164276,
    "crystal_purity": 0.9866251945495605,
    "crystal_size": 0.09810223430395126,
    "crystal_yield": 0.6109620928764343,
    "degradation_warning": 0.08853281289339066,
    "safety_risk": 0.1724957823753357,
    "score": 0.5906471014022827,
    "selectivity": 0.6693552136421204,
    "virtual_spectrum_summary": 0.1655845195055008,
    "yield": 0.6738897562026978
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
      "solvent": 0,
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
      "stirring_speed_rpm": 300,
      "target_temperature_K": 360
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.005
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
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
      "target_temperature_K": 285
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
  "end_step": 279,
  "lifecycle_index": 16,
  "metrics": {
    "byproduct_signal": 0.22111432254314423,
    "conversion": 0.9885537624359131,
    "cost": 1.0,
    "crystal_csd_quality": 0.6046911478042603,
    "crystal_fines_fraction": 0.6164702773094177,
    "crystal_purity": 0.9811757206916809,
    "crystal_size": 0.07966496795415878,
    "crystal_yield": 0.620178759098053,
    "degradation_warning": 0.10165401548147202,
    "safety_risk": 0.20746710896492004,
    "score": 0.5177092552185059,
    "selectivity": 0.6673612594604492,
    "virtual_spectrum_summary": 0.1673571765422821,
    "yield": 0.6657158136367798
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
      "solvent": 0,
      "volume_L": 0.05
    },
    {
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 360
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.005
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
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
      "target_temperature_K": 285
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
  "end_step": 296,
  "lifecycle_index": 17,
  "metrics": {
    "byproduct_signal": 0.23667018115520477,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7533339262008667,
    "crystal_fines_fraction": 0.3316528797149658,
    "crystal_purity": 1.0,
    "crystal_size": 0.07569016516208649,
    "crystal_yield": 0.6281880140304565,
    "degradation_warning": 0.09548545628786087,
    "safety_risk": 0.18437649309635162,
    "score": 0.5838044881820679,
    "selectivity": 0.6636837124824524,
    "virtual_spectrum_summary": 0.17313705384731293,
    "yield": 0.6738420128822327
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
      "solvent": 0,
      "volume_L": 0.045
    },
    {
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 360
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.005
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
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
      "target_temperature_K": 285
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
  "end_step": 313,
  "lifecycle_index": 18,
  "metrics": {
    "byproduct_signal": 0.21015143394470215,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7111994028091431,
    "crystal_fines_fraction": 0.5170272588729858,
    "crystal_purity": 0.9972585439682007,
    "crystal_size": 0.1239050105214119,
    "crystal_yield": 0.619845449924469,
    "degradation_warning": 0.09178570657968521,
    "safety_risk": 0.19386865198612213,
    "score": 0.5598722100257874,
    "selectivity": 0.6691860556602478,
    "virtual_spectrum_summary": 0.15688686072826385,
    "yield": 0.6825929880142212
  },
  "ordinal": 18
}
```

## K1

```json
null
```

## Q

```json
null
```

## K2

```json
null
```

## Evaluation and accounting

```json
{
  "failure": {
    "message": "Codex session crossed a frozen operational limit before the next executable operation; no fallback action was emitted: max_provider_error_events",
    "stage": "source",
    "type": "InteractiveCodexExperimentError"
  },
  "recommendation": null,
  "recommendation_recipe": null,
  "prediction_evaluation": {
    "failure": "missing/duplicate/unknown query IDs",
    "valid": false
  },
  "public_baselines": {
    "available": true,
    "mae": {
      "public_mean": {
        "crystal_fines_fraction": 0.28539295852396884,
        "crystal_purity": 0.005609616612781837,
        "crystal_size": 0.017192244486071477,
        "crystal_yield": 0.2594789711101668
      },
      "public_nearest_neighbor": {
        "crystal_fines_fraction": 0.28946799312161586,
        "crystal_purity": 0.0054665585652763264,
        "crystal_size": 0.016519910301822236,
        "crystal_yield": 0.28481593206165406
      }
    },
    "training_batches": 18
  },
  "tokens": {
    "basis": "cumulative thread snapshots differenced in source/K1/Q/K2 order",
    "complete": false,
    "monetary_cost_usd": null,
    "stages": [],
    "total": {
      "cached_input": 0,
      "input": 0,
      "input_plus_output": 0,
      "output": 0,
      "uncached_input": 0
    },
    "valid": false
  },
  "elapsed_s": 516.25
}
```
