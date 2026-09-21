# C-W03-B12-E-Opaque

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
      "stirring_speed_rpm": 600,
      "target_temperature_K": 350
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
  "end_step": 11,
  "lifecycle_index": 1,
  "metrics": {
    "byproduct_signal": 0.2794296443462372,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.4947561025619507,
    "crystal_fines_fraction": 0.9068863391876221,
    "crystal_purity": 0.9788811802864075,
    "crystal_size": 0.05577081814408302,
    "crystal_yield": 0.3859858214855194,
    "degradation_warning": 0.07880985736846924,
    "safety_risk": 0.13519255816936493,
    "score": 0.3891395926475525,
    "selectivity": 0.5560029149055481,
    "virtual_spectrum_summary": 0.18915073573589325,
    "yield": 0.5538126230239868
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
      "target_temperature_K": 350
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
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
  "end_step": 24,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.3610501289367676,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.797075629234314,
    "crystal_fines_fraction": 0.27404502034187317,
    "crystal_purity": 0.9819624423980713,
    "crystal_size": 0.11480680853128433,
    "crystal_yield": 0.39826884865760803,
    "degradation_warning": 0.1526973843574524,
    "safety_risk": 0.15970297157764435,
    "score": 0.5085377097129822,
    "selectivity": 0.495993435382843,
    "virtual_spectrum_summary": 0.267291396856308,
    "yield": 0.4845484495162964
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
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
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
  "end_step": 39,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.3693290948867798,
    "conversion": 0.9983178973197937,
    "cost": 1.0,
    "crystal_csd_quality": 0.8425471782684326,
    "crystal_fines_fraction": 0.1051725223660469,
    "crystal_purity": 0.9908929467201233,
    "crystal_size": 0.0920901745557785,
    "crystal_yield": 0.3792218565940857,
    "degradation_warning": 0.1294340342283249,
    "safety_risk": 0.17385150492191315,
    "score": 0.5185473561286926,
    "selectivity": 0.4366975724697113,
    "virtual_spectrum_summary": 0.2613763213157654,
    "yield": 0.43581029772758484
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 500,
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
  "end_step": 54,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.403872549533844,
    "conversion": 0.9889965057373047,
    "cost": 1.0,
    "crystal_csd_quality": 0.7397685050964355,
    "crystal_fines_fraction": 0.4367452561855316,
    "crystal_purity": 1.0,
    "crystal_size": 0.07945001125335693,
    "crystal_yield": 0.3526574671268463,
    "degradation_warning": 0.1582813262939453,
    "safety_risk": 0.1510951817035675,
    "score": 0.45071130990982056,
    "selectivity": 0.3959733247756958,
    "virtual_spectrum_summary": 0.2933565080165863,
    "yield": 0.3823436498641968
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
      "catalyst": 2,
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
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
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
  "end_step": 69,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.38071078062057495,
    "conversion": 0.9963378310203552,
    "cost": 1.0,
    "crystal_csd_quality": 0.775142252445221,
    "crystal_fines_fraction": 0.27474266290664673,
    "crystal_purity": 0.9732014536857605,
    "crystal_size": 0.06751121580600739,
    "crystal_yield": 0.392801433801651,
    "degradation_warning": 0.12633419036865234,
    "safety_risk": 0.15638914704322815,
    "score": 0.48908862471580505,
    "selectivity": 0.45374760031700134,
    "virtual_spectrum_summary": 0.26624131202697754,
    "yield": 0.44759464263916016
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
      "operation": "seed_crystals",
      "seed_mass_g": 0.02
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
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
  "end_step": 84,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.3859623372554779,
    "conversion": 0.9924335479736328,
    "cost": 1.0,
    "crystal_csd_quality": 0.7942126393318176,
    "crystal_fines_fraction": 0.2181798368692398,
    "crystal_purity": 0.9980853199958801,
    "crystal_size": 0.06666383892297745,
    "crystal_yield": 0.45724600553512573,
    "degradation_warning": 0.1989990472793579,
    "safety_risk": 0.16358047723770142,
    "score": 0.5266010761260986,
    "selectivity": 0.488847017288208,
    "virtual_spectrum_summary": 0.30182886123657227,
    "yield": 0.4907326102256775
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
      "operation": "seed_crystals",
      "seed_mass_g": 0.02
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
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
  "end_step": 99,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.318631649017334,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7324855327606201,
    "crystal_fines_fraction": 0.3377838432788849,
    "crystal_purity": 0.9763315916061401,
    "crystal_size": 0.09648876637220383,
    "crystal_yield": 0.4898928105831146,
    "degradation_warning": 0.1286635547876358,
    "safety_risk": 0.1437220722436905,
    "score": 0.5178059935569763,
    "selectivity": 0.511203408241272,
    "virtual_spectrum_summary": 0.23314601182937622,
    "yield": 0.5378504395484924
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
      "operation": "seed_crystals",
      "seed_mass_g": 0.02
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
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
  "end_step": 114,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.4475930333137512,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7815721035003662,
    "crystal_fines_fraction": 0.3006436228752136,
    "crystal_purity": 0.971072793006897,
    "crystal_size": 0.11391901969909668,
    "crystal_yield": 0.3637511134147644,
    "degradation_warning": 0.23992501199245453,
    "safety_risk": 0.18126556277275085,
    "score": 0.47227802872657776,
    "selectivity": 0.3965385854244232,
    "virtual_spectrum_summary": 0.354142427444458,
    "yield": 0.3882333040237427
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
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
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
  "end_step": 131,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.35337790846824646,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7446430325508118,
    "crystal_fines_fraction": 0.3492872714996338,
    "crystal_purity": 0.9787501096725464,
    "crystal_size": 0.06352189183235168,
    "crystal_yield": 0.48593148589134216,
    "degradation_warning": 0.14412331581115723,
    "safety_risk": 0.1432444453239441,
    "score": 0.5116231441497803,
    "selectivity": 0.500167727470398,
    "virtual_spectrum_summary": 0.2592133581638336,
    "yield": 0.5138436555862427
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
      "volume_L": 0.04
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
      "operation": "seed_crystals",
      "seed_mass_g": 0.02
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
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
  "end_step": 146,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.3149121403694153,
    "conversion": 0.9858242273330688,
    "cost": 1.0,
    "crystal_csd_quality": 0.6312236189842224,
    "crystal_fines_fraction": 0.5866310596466064,
    "crystal_purity": 0.9827975630760193,
    "crystal_size": 0.0656835287809372,
    "crystal_yield": 0.5005894899368286,
    "degradation_warning": 0.1423274278640747,
    "safety_risk": 0.1710706502199173,
    "score": 0.47288456559181213,
    "selectivity": 0.5304437279701233,
    "virtual_spectrum_summary": 0.23724901676177979,
    "yield": 0.5393705368041992
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
      "volume_L": 0.06
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
      "operation": "seed_crystals",
      "seed_mass_g": 0.02
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
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
  "end_step": 161,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.32331547141075134,
    "conversion": 0.9990203380584717,
    "cost": 1.0,
    "crystal_csd_quality": 0.7587338089942932,
    "crystal_fines_fraction": 0.2810078561306,
    "crystal_purity": 0.9938440918922424,
    "crystal_size": 0.08544766157865524,
    "crystal_yield": 0.4845549464225769,
    "degradation_warning": 0.1178772822022438,
    "safety_risk": 0.15058796107769012,
    "score": 0.5304400324821472,
    "selectivity": 0.5478091239929199,
    "virtual_spectrum_summary": 0.23086827993392944,
    "yield": 0.528319239616394
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
      "operation": "seed_crystals",
      "seed_mass_g": 0.02
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
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
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 200,
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
      "target_temperature_K": 260
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
  "end_step": 179,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.3224838674068451,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7308259010314941,
    "crystal_fines_fraction": 0.3577042818069458,
    "crystal_purity": 0.990563154220581,
    "crystal_size": 0.10361018031835556,
    "crystal_yield": 0.46835052967071533,
    "degradation_warning": 0.15172183513641357,
    "safety_risk": 0.14208294451236725,
    "score": 0.5116761326789856,
    "selectivity": 0.5145068764686584,
    "virtual_spectrum_summary": 0.24564094841480255,
    "yield": 0.5195488333702087
  },
  "ordinal": 12
}
```

## K1

```json
{
  "payload": {
    "report": "Mechanistic account\n\nThe campaign indicates that crystallization history, solvent identity, and concentration controlled the constrained objective more strongly than the native composite score. The recommended process remains batch 7: 0.040 mol reagent, 0.080 L solvent-S0, 0.005 mol catalyst-C3, reaction heating toward 350 K for 3600 s at 600 rpm, 0.020 g seed, staged 14,400 s cooling holds at 320, 300, 280, 260, and 250 K, a final 14,400 s hold at 250 K and 100 rpm, followed by filtration. Its final assay gave crystal recovery 0.4899, purity 0.9763, and fines fraction 0.3378, satisfying both constraints.\n\nObservations and material effects\n\nThe clearest approximately matched solvent comparison used catalyst-C3 and the same 0.020 g seed/staged-cooling program. Batch 7 (S0) gave recovery 0.4899, purity 0.9763, and fines 0.3378. Batch 6 (S1) gave lower recovery, 0.4572, but higher purity, 0.9981, and fewer fines, 0.2182. Batch 8 (S3) was inferior in recovery at 0.3638, with purity 0.9711 and fines 0.3006. I interpret S0 as providing the most favorable low-temperature solubility or supersaturation for recovery, while S1 favored a cleaner and narrower crystallization regime. S3 apparently retained more product or otherwise reduced recoverable solid. These are benchmark-specific effects; the anonymous solvent labels do not justify claims about real chemical properties.\n\nCatalyst conclusions are less secure because catalyst changes were confounded with temperature or cooling endpoints. Nevertheless, C3-containing batches 6, 7, 9, 11, and 12 repeatedly produced qualifying solids and recoveries of 0.457\u20130.490, whereas batch 4 using C0 under a lower-temperature reaction schedule gave recovery 0.3527. Batch 2 used C1 and gave 0.3983 recovery, and batch 5 used C2 and gave 0.3928. This supports C3 operationally, but does not isolate a molecular catalytic mechanism.\n\nReaction\u2013crystallization coupling\n\nThe assay defines crystallization recovery as\n\nY_cryst = n(target recovered in crystals, excluding seed) / n(target present before separation).\n\nIt is therefore not an overall yield from charged reagent. Reaction conversion and selectivity determine how much target and impurity enter crystallization, but Y_cryst measures the fraction of that target recovered. For example, batch 7 had conversion 1.000, reaction yield 0.5379, selectivity 0.5112, and byproduct signal 0.3186, yet crystal purity remained 0.9763. Batch 11 similarly had conversion 0.9990, reaction yield 0.5283, selectivity 0.5478, and purity 0.9938. Thus the crystallization rejected much of the reaction impurity, and reaction selectivity alone did not predict crystal purity or recovery.\n\nA useful qualitative coupling is\n\nR_cryst \u2248 1 \u2212 C*(T_f, solvent)V_liquid / n_target,pre,\n\nsubject to kinetic trapping and filtration losses, where C* is target solubility. Lower final temperature or liquid volume should increase recovery, but the resulting supersaturation also changes nucleation. In classical qualitative form, S = C/C*, nucleation may scale as J \u221d exp[\u2212B/(ln S)^2], while growth may scale as G \u221d (S\u22121)^g. Increasing S can therefore improve recovery while creating many small crystals faster than existing crystals can grow.\n\nThat tradeoff appeared directly in the concentration experiments. Batch 10 reduced S0 volume to 0.040 L and achieved the campaign\u2019s highest numerical recovery, 0.5006, but its fines fraction was 0.5866 and therefore failed the \u22640.50 requirement. At 0.060 L, batch 11 recovered 0.4846 with fines 0.2810; at 0.080 L, batch 7 recovered 0.4899 with fines 0.3378. The nonmonotonic difference between batches 7 and 11 is small relative to uncertainty, but the failure at 0.040 L is consistent with excessive supersaturation and secondary nucleation.\n\nProcess-history dependence\n\nBatch 1 established that reaching a low temperature was insufficient without a controlled trajectory. A single 7200 s cooling step to 280 K after 0.050 g seeding produced recovery 0.3860 but fines 0.9069, crystal-size index 0.0558, and CSD quality 0.4948. Batch 2 replaced this with slow stages at 320, 300, and 280 K plus a long low-agitation hold; recovery was similar at 0.3983, but fines fell to 0.2740 and CSD quality rose to 0.7971. I interpret gradual cooling as keeping supersaturation within a growth-dominated zone and limiting burst nucleation and attrition.\n\nCooling farther to 250 K generally preserved acceptable fines when done gradually. Batch 7 combined this history with S0/C3 and gave the best observed qualifying recovery. Extending the final hold was not beneficial: batch 9 used lower seed (0.010 g) and three final holds, but gave recovery 0.4859 and fines 0.3493, essentially no improvement over batch 7. A thermal-cycle alternative was tested in batch 12 by reheating the slurry to 290 K and slowly recooling. It gave recovery 0.4684 and fines 0.3577, so partial redissolution/ripening did not outperform the simpler batch-7 history.\n\nThe seed results do not establish a monotonic seed-loading law. Batch 1\u2019s 0.050 g seed coincided with severe fines, whereas the 0.010\u20130.020 g programs were much better, but cooling history changed simultaneously. The plausible interpretation is that excessive nuclei plus rapid cooling increased the particle number and reduced size; an untested alternative is that batch 1\u2019s fines arose primarily from its cooling rate rather than seed loading.\n\nRevisions during the campaign\n\nThe initial strategy emphasized reaction completion and direct cooling. Batch 1 showed that purity and recovery alone were misleading because the fines constraint failed badly. The program was revised to staged, slow cooling and low-speed aging in batch 2. Subsequent batches screened anonymous solvent/catalyst combinations and lower final temperature, identifying C3 with S0 as the strongest recovery combination. Batch 10 then deliberately increased concentration; its recovery rose but fines crossed the constraint. Batch 11 backed away to 0.060 L and restored quality, while batch 12 tested thermal cycling without improvement. These results led to retaining batch 7 rather than selecting the higher-recovery but noncompliant batch 10.\n\nUncertainty and unresolved tradeoff\n\nEach condition was run once. Final-assay nominal noise scales were about 0.010 for crystal recovery and purity and 0.018 for fines and CSD quality, with additional process uncertainty possible. Consequently, the recovery difference between batch 7 (0.4899) and batch 11 (0.4846) is not statistically resolved, although both are safely above the purity threshold and below the fines limit. By contrast, batch 10\u2019s fines result of 0.5866 is far enough above 0.50 to be a meaningful failure under the observed assay.\n\nThe principal unresolved issue is the recovery\u2013particle-quality boundary between 0.040 and 0.080 L S0. Intermediate solvent volumes, replicated batch-7 and batch-11 runs, alternative seed timings, gentler agitation, and narrower cooling ramps were not tested. Catalyst effects were not isolated in a factorial design, and no direct solubility, supersaturation, nucleation-rate, or species-concentration measurements were available. Accordingly, the proposed mechanism is a process-level interpretation of the observations, not a demonstrated molecular mechanism. The sealed recommendation remains batch 7 because it had the highest observed recovery among batches meeting both stated constraints, while maintaining a useful fines margin."
  },
  "failure": null,
  "elapsed_s": 60.937000000005355,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 532736,
    "input_tokens": 606207,
    "output_tokens": 9630,
    "reasoning_output_tokens": 2615
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
          "estimate": 0.13,
          "lower80": 0.05,
          "upper80": 0.27
        },
        "crystal_purity": {
          "estimate": 0.988,
          "lower80": 0.958,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.18,
          "lower80": 0.11,
          "upper80": 0.27
        },
        "crystal_yield": {
          "estimate": 0.27,
          "lower80": 0.19,
          "upper80": 0.36
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q01"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.2,
          "lower80": 0.08,
          "upper80": 0.38
        },
        "crystal_purity": {
          "estimate": 0.97,
          "lower80": 0.92,
          "upper80": 0.995
        },
        "crystal_size": {
          "estimate": 0.15,
          "lower80": 0.08,
          "upper80": 0.24
        },
        "crystal_yield": {
          "estimate": 0.18,
          "lower80": 0.1,
          "upper80": 0.28
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q02"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.05,
          "lower80": 0.01,
          "upper80": 0.15
        },
        "crystal_purity": {
          "estimate": 0.984,
          "lower80": 0.948,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.3,
          "lower80": 0.18,
          "upper80": 0.44
        },
        "crystal_yield": {
          "estimate": 0.29,
          "lower80": 0.19,
          "upper80": 0.39
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q03"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.14,
          "lower80": 0.05,
          "upper80": 0.29
        },
        "crystal_purity": {
          "estimate": 0.982,
          "lower80": 0.946,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.17,
          "lower80": 0.1,
          "upper80": 0.27
        },
        "crystal_yield": {
          "estimate": 0.3,
          "lower80": 0.21,
          "upper80": 0.4
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q04"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.14,
          "lower80": 0.05,
          "upper80": 0.29
        },
        "crystal_purity": {
          "estimate": 0.982,
          "lower80": 0.946,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.18,
          "lower80": 0.1,
          "upper80": 0.28
        },
        "crystal_yield": {
          "estimate": 0.3,
          "lower80": 0.21,
          "upper80": 0.4
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q05"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.58,
          "lower80": 0.39,
          "upper80": 0.77
        },
        "crystal_purity": {
          "estimate": 0.978,
          "lower80": 0.936,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.08,
          "lower80": 0.03,
          "upper80": 0.15
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
          "estimate": 0.1,
          "lower80": 0.03,
          "upper80": 0.23
        },
        "crystal_purity": {
          "estimate": 0.984,
          "lower80": 0.948,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.2,
          "lower80": 0.11,
          "upper80": 0.31
        },
        "crystal_yield": {
          "estimate": 0.31,
          "lower80": 0.22,
          "upper80": 0.41
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q07"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.58,
          "lower80": 0.37,
          "upper80": 0.79
        },
        "crystal_purity": {
          "estimate": 0.975,
          "lower80": 0.93,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.1,
          "lower80": 0.04,
          "upper80": 0.19
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
          "estimate": 0.18,
          "lower80": 0.05,
          "upper80": 0.39
        },
        "crystal_purity": {
          "estimate": 0.993,
          "lower80": 0.96,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.14,
          "lower80": 0.07,
          "upper80": 0.23
        },
        "crystal_yield": {
          "estimate": 0.01,
          "lower80": 0.0,
          "upper80": 0.035
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q09"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.16,
          "lower80": 0.05,
          "upper80": 0.34
        },
        "crystal_purity": {
          "estimate": 0.989,
          "lower80": 0.953,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.15,
          "lower80": 0.08,
          "upper80": 0.25
        },
        "crystal_yield": {
          "estimate": 0.075,
          "lower80": 0.025,
          "upper80": 0.15
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q10"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.14,
          "lower80": 0.05,
          "upper80": 0.29
        },
        "crystal_purity": {
          "estimate": 0.982,
          "lower80": 0.946,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.18,
          "lower80": 0.1,
          "upper80": 0.28
        },
        "crystal_yield": {
          "estimate": 0.3,
          "lower80": 0.21,
          "upper80": 0.4
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q11"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.28,
          "lower80": 0.13,
          "upper80": 0.48
        },
        "crystal_purity": {
          "estimate": 0.965,
          "lower80": 0.91,
          "upper80": 0.995
        },
        "crystal_size": {
          "estimate": 0.13,
          "lower80": 0.06,
          "upper80": 0.22
        },
        "crystal_yield": {
          "estimate": 0.39,
          "lower80": 0.29,
          "upper80": 0.5
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q12"
      }
    ],
    "rationale": "Pairwise interpretation: Q01\u2013Q02 isolates solvent identity; prior evidence favors S1 over S3 for recovery and purity, while both very slow ramps should suppress fines. Q03\u2013Q04 isolates seed loading: sparse seeding should produce fewer, larger particles, with only a small kinetic recovery penalty after the exceptionally long ramp. Q05\u2013Q06 contrasts gradual cooling with a temperature crash at equal approximate residence time; the crash should raise recovery slightly but lock in many fines. Q07\u2013Q08 tests a terminal hold against reheating to 315 K and rapid recooling; substantial redissolution followed by fast supersaturation is expected to reduce retained recovery and regenerate fines. Q09\u2013Q10 tests residence at 292 K: seed ensures particles are present in both, but 60 seconds gives almost no seed-excluded recovery, whereas two hours permits measurable growth. Q11\u2013Q12 doubles reagent concentration at fixed solvent and catalyst; higher supersaturation should increase recovery but decrease size and raise fines, while remaining nominally feasible under the slow ramp. Intervals are deliberately broad because the campaign did not replicate these dilute, long-duration C1 recipes; solvent, seed, thermal-history, and concentration effects are extrapolated, and intervals near the fines threshold indicate unresolved feasibility risk."
  },
  "failure": null,
  "elapsed_s": 78.57799999997951,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 532736,
    "input_tokens": 652131,
    "output_tokens": 13684,
    "reasoning_output_tokens": 4985
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
    "report": "1. Claim status\n\nSupported by observation:\n- A recovery\u2013fines tradeoff with concentration is the strongest near-matched result. Using S0/C3 and the same seed and staged-cooling program, batch 10 at 0.040 L gave the highest recovery (0.5006) but failed on fines (0.5866); batches 11 at 0.060 L and 7 at 0.080 L gave recoveries of 0.4846 and 0.4899 with fines of 0.2810 and 0.3378. Directly observed: concentrating to 0.040 L crossed the fines limit. Interpretation: excessive supersaturation caused secondary nucleation.\n- Slow staged cooling was operationally associated with better particle quality. Batch 1\u2019s short, single cooling step produced fines 0.9069 and CSD quality 0.4948, whereas batch 2\u2019s staged cooling and aging produced fines 0.2740 and CSD quality 0.7971. This comparison is supportive, not definitive, because solvent, catalyst and seed loading also changed.\n- S0/C3 was the best observed qualifying combination. Under closely similar histories, batch 7 (S0/C3) recovered 0.4899 versus 0.4572 for batch 6 (S1/C3) and 0.3638 for batch 8 (S3/C3). S1 gave better purity and fewer fines than S0, so the solvent effect was a recovery-versus-quality shift rather than universal superiority.\n- Crystallization strongly purified imperfect reaction mixtures. Batch 7 had reaction selectivity 0.5112 and byproduct signal 0.3186 but crystal purity 0.9763; batch 11 had selectivity 0.5478 and purity 0.9938. The assay directly supports impurity rejection, although it does not identify the molecular mechanism.\n- The tested thermal cycle did not improve the objective. Batch 12, which reheated to 290 K and recooled, gave recovery 0.4684 and fines 0.3577, versus 0.4899 and 0.3378 for the otherwise similar batch 7.\n\nContradicted or weakened:\n- A simple monotonic rule that less solvent always creates more fines is weakened by batch 11: 0.060 L produced fewer fines than batch 7 at 0.080 L. Only the extreme 0.040 L case clearly behaved as predicted. Noise and nonlinear nucleation thresholds are plausible alternatives.\n- A general benefit from extra aging was not observed. Batch 9 added two extra long terminal holds and used less seed, yet recovery (0.4859) and fines (0.3493) did not improve over batch 7. Because two factors changed, this does not separately falsify either longer aging or lower seed loading.\n- The proposed ripening benefit of reheating was contradicted under the single tested cycle in batch 12. Different reheating temperatures or slower recooling remain possible.\n\nStill untested:\n- Catalyst-C3 superiority was not established causally because the catalyst comparisons also changed reaction temperature, solvent or cooling endpoint.\n- The claim that batch 1\u2019s fines arose from its 0.050 g seed loading remains untested; rapid cooling is an equally credible cause.\n- No direct solubility, supersaturation, nucleation-rate or growth-rate data tested the proposed equations. The forms involving S=C/C*, J and G were interpretive organizing models.\n- Replicates, a complete solvent\u2013catalyst factorial design, seed-timing effects and the narrow solvent-volume boundary between acceptable and excessive fines were not tested.\n\n2. One additional experiment\n\nI would repeat batch 7 exactly but increase only the seed charge from 0.020 g to 0.050 g. This is preferable to another broad optimization because it directly separates two competing explanations for batch 1: excessive seed population versus rapid, unstaged cooling.\n\nIf seed loading is the dominant cause, the matched high-seed experiment should retain approximately similar recovery but show a distinctly smaller crystal-size index and a large increase in fines, potentially toward or beyond 0.50. If cooling history is dominant, the slow staged trajectory should keep fines near batch 7\u2019s approximately 0.34 despite the larger seed charge, perhaps with only a modest size decrease. An intermediate result would support an interaction: slow cooling mitigates, but does not eliminate, the effect of excessive nuclei. Purity should remain high in all three cases because solvent, catalyst and reaction history would be unchanged.\n\n3. Least-used observation and least-reliable prediction\n\nThe account used batch 3 least effectively. Its final assay showed exceptionally low fines (0.1052) and high CSD quality (0.8425), despite recovery of only 0.3792. Because both S2 and C2 differed from the principal S0/C3 series, I treated it mainly as confounded evidence. It nevertheless warns that material identity can control particle population as strongly as cooling history and that low fines need not imply high recovery.\n\nQ09 is the least reliable held-out prediction. It filters only 60 seconds after cooling to 292 K, a regime with no campaign analogue. I predicted that the introduced seed would make particles present while seed-excluded recovery remained near zero, but the campaign did not establish how the benchmark counts seed-only solids in particle size, fines or purity immediately after seeding. Thus its particle metrics and even the operational significance of a 0.01 recovery estimate depend on an extrapolation far outside the observed residence-time range."
  },
  "failure": null,
  "elapsed_s": 49.375,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 567168,
    "input_tokens": 702029,
    "output_tokens": 15720,
    "reasoning_output_tokens": 5826
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
    "selected_experiment_index": 7,
    "selection_rationale": "Batch 7 delivered the highest observed seed-excluded crystal recovery among batches meeting both constraints: crystal_yield 0.4899, crystal_purity 0.9763, and fines fraction 0.3378. Its slow staged cooling to 250 K with 0.02 g seed in solvent-S0/catalyst-C3 also provided a comfortable quality margin."
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
        "operation": "seed_crystals",
        "seed_mass_g": 0.02
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 320
      },
      {
        "duration_s": 14400,
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
    "lifecycle_index": 7,
    "source_attempts": 15
  },
  "prediction_evaluation": {
    "contrasts": [
      {
        "absolute_delta_error": 0.059891510015443405,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_yield",
        "predicted_delta": -0.09000000000000002,
        "resolved": true,
        "true_delta": -0.14989151001544343
      },
      {
        "absolute_delta_error": 0.0186458791151507,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_purity",
        "predicted_delta": -0.018000000000000016,
        "resolved": false,
        "true_delta": 0.0006458791151506826
      },
      {
        "absolute_delta_error": 0.04938040150063501,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_size",
        "predicted_delta": -0.03,
        "resolved": true,
        "true_delta": 0.01938040150063501
      },
      {
        "absolute_delta_error": 0.5983138299289017,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.07,
        "resolved": true,
        "true_delta": -0.5283138299289017
      },
      {
        "absolute_delta_error": 0.010159217773570511,
        "direction_correct": true,
        "factor": "seed",
        "metric": "crystal_yield",
        "predicted_delta": 0.010000000000000009,
        "resolved": false,
        "true_delta": -0.00015921777357050249
      },
      {
        "absolute_delta_error": 0.011746054635378256,
        "direction_correct": true,
        "factor": "seed",
        "metric": "crystal_purity",
        "predicted_delta": -0.0020000000000000018,
        "resolved": false,
        "true_delta": 0.009746054635378254
      },
      {
        "absolute_delta_error": 0.12281442889796411,
        "direction_correct": true,
        "factor": "seed",
        "metric": "crystal_size",
        "predicted_delta": -0.12999999999999998,
        "resolved": true,
        "true_delta": -0.007185571102035868
      },
      {
        "absolute_delta_error": 0.07426690822029768,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.09000000000000001,
        "resolved": true,
        "true_delta": 0.16426690822029769
      },
      {
        "absolute_delta_error": 0.029547857564826113,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_yield",
        "predicted_delta": 0.030000000000000027,
        "resolved": false,
        "true_delta": 0.0004521424351739134
      },
      {
        "absolute_delta_error": 0.00044528956930878216,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.0040000000000000036,
        "resolved": false,
        "true_delta": -0.0035547104306912214
      },
      {
        "absolute_delta_error": 0.05668654733429697,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_size",
        "predicted_delta": -0.09999999999999999,
        "resolved": true,
        "true_delta": -0.04331345266570302
      },
      {
        "absolute_delta_error": 0.18295396285845933,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.43999999999999995,
        "resolved": true,
        "true_delta": 0.6229539628584593
      },
      {
        "absolute_delta_error": 0.11437670725156426,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_yield",
        "predicted_delta": -0.07,
        "resolved": true,
        "true_delta": 0.04437670725156426
      },
      {
        "absolute_delta_error": 0.0020561827941991684,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.009000000000000008,
        "resolved": true,
        "true_delta": -0.011056182794199176
      },
      {
        "absolute_delta_error": 0.06029441872935701,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_size",
        "predicted_delta": -0.1,
        "resolved": true,
        "true_delta": -0.039705581270643
      },
      {
        "absolute_delta_error": 0.18037028724012594,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.48,
        "resolved": true,
        "true_delta": 0.6603702872401259
      },
      {
        "absolute_delta_error": 0.029517184302002134,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_yield",
        "predicted_delta": 0.065,
        "resolved": true,
        "true_delta": 0.09451718430200214
      },
      {
        "absolute_delta_error": 0.007943686041185227,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_purity",
        "predicted_delta": -0.0040000000000000036,
        "resolved": true,
        "true_delta": -0.01194368604118523
      },
      {
        "absolute_delta_error": 0.0038981677016547978,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_size",
        "predicted_delta": 0.009999999999999981,
        "resolved": true,
        "true_delta": 0.013898167701654779
      },
      {
        "absolute_delta_error": 0.08539272978183873,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.01999999999999999,
        "resolved": false,
        "true_delta": 0.06539272978183874
      },
      {
        "absolute_delta_error": 0.07504321303990111,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_yield",
        "predicted_delta": 0.09000000000000002,
        "resolved": false,
        "true_delta": 0.014956786960098917
      },
      {
        "absolute_delta_error": 0.011828397249087241,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_purity",
        "predicted_delta": -0.017000000000000015,
        "resolved": false,
        "true_delta": -0.005171602750912774
      },
      {
        "absolute_delta_error": 0.024356873957321043,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_size",
        "predicted_delta": -0.04999999999999999,
        "resolved": true,
        "true_delta": -0.025643126042678946
      },
      {
        "absolute_delta_error": 0.46598956676040815,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.14,
        "resolved": true,
        "true_delta": 0.6059895667604082
      }
    ],
    "failures": [],
    "metrics": {
      "crystal_fines_fraction": {
        "coverage80": 0.0,
        "interval_score80": 3.1935047367457443,
        "interval_width": 0.27999999999999997,
        "mae": 0.4571838070079078,
        "n": 12,
        "planned": 12
      },
      "crystal_purity": {
        "coverage80": 1.0,
        "interval_score80": 0.05741666666666668,
        "interval_width": 0.05741666666666668,
        "mae": 0.00590793581992959,
        "n": 12,
        "planned": 12
      },
      "crystal_size": {
        "coverage80": 0.3333333333333333,
        "interval_score80": 0.3924838346017996,
        "interval_width": 0.17250000000000001,
        "mae": 0.09448436583478936,
        "n": 12,
        "planned": 12
      },
      "crystal_yield": {
        "coverage80": 0.8333333333333334,
        "interval_score80": 0.2125981791419257,
        "interval_width": 0.17416666666666666,
        "mae": 0.06159647514240799,
        "n": 12,
        "planned": 12
      }
    },
    "quality": {
      "balanced_accuracy": 0.6666666666666666,
      "false_negative": 0,
      "false_positive": 4,
      "true_negative": 2,
      "true_positive": 6
    },
    "resolved_direction_correct": 10,
    "resolved_direction_n": 16,
    "tie_correct": 4,
    "tie_n": 8,
    "valid": true
  },
  "public_baselines": {
    "available": true,
    "mae": {
      "public_mean": {
        "crystal_fines_fraction": 0.3363403661395907,
        "crystal_purity": 0.004610332991084108,
        "crystal_size": 0.019305547319676732,
        "crystal_yield": 0.22015390763905837
      },
      "public_nearest_neighbor": {
        "crystal_fines_fraction": 0.31748912938890844,
        "crystal_purity": 0.009158687579390562,
        "crystal_size": 0.030232226529714357,
        "crystal_yield": 0.2493831884883562
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
        "cached_input": 532736,
        "input": 571548,
        "output": 6901,
        "stage": "source",
        "uncached_input": 38812
      },
      {
        "cached_input": 0,
        "input": 34659,
        "output": 2729,
        "stage": "K1",
        "uncached_input": 34659
      },
      {
        "cached_input": 0,
        "input": 45924,
        "output": 4054,
        "stage": "Q",
        "uncached_input": 45924
      },
      {
        "cached_input": 34432,
        "input": 49898,
        "output": 2036,
        "stage": "K2",
        "uncached_input": 15466
      }
    ],
    "total": {
      "cached_input": 567168,
      "input": 702029,
      "input_plus_output": 717749,
      "output": 15720,
      "uncached_input": 134861
    },
    "valid": true
  },
  "elapsed_s": 525.5310000000172
}
```
