# C-W01-B12-E-Opaque

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
      "target_temperature_K": 360
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
  "end_step": 10,
  "lifecycle_index": 1,
  "metrics": {
    "byproduct_signal": 0.24448901414871216,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6100332140922546,
    "crystal_fines_fraction": 0.6607979536056519,
    "crystal_purity": 0.9783586263656616,
    "crystal_size": 0.06360379606485367,
    "crystal_yield": 0.4885803759098053,
    "degradation_warning": 0.07959907501935959,
    "safety_risk": 0.1465299278497696,
    "score": 0.474202424287796,
    "selectivity": 0.618820071220398,
    "virtual_spectrum_summary": 0.170288547873497,
    "yield": 0.6166420578956604
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
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
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
  "end_step": 23,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.30906808376312256,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6735982298851013,
    "crystal_fines_fraction": 0.5104971528053284,
    "crystal_purity": 0.9755948781967163,
    "crystal_size": 0.10395786166191101,
    "crystal_yield": 0.4901142120361328,
    "degradation_warning": 0.12377981841564178,
    "safety_risk": 0.14802485704421997,
    "score": 0.49945157766342163,
    "selectivity": 0.5915761590003967,
    "virtual_spectrum_summary": 0.22568835318088531,
    "yield": 0.5801311731338501
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
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
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
  "end_step": 38,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.4907468855381012,
    "conversion": 0.9983179569244385,
    "cost": 1.0,
    "crystal_csd_quality": 0.648032546043396,
    "crystal_fines_fraction": 0.5100752711296082,
    "crystal_purity": 0.9863284230232239,
    "crystal_size": 0.0649314597249031,
    "crystal_yield": 0.2953364849090576,
    "degradation_warning": 0.25581860542297363,
    "safety_risk": 0.14725059270858765,
    "score": 0.4068268835544586,
    "selectivity": 0.3866190016269684,
    "virtual_spectrum_summary": 0.3850291669368744,
    "yield": 0.3857317268848419
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
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
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
  "end_step": 51,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.3536103367805481,
    "conversion": 0.9889965057373047,
    "cost": 1.0,
    "crystal_csd_quality": 0.7870411276817322,
    "crystal_fines_fraction": 0.2073058933019638,
    "crystal_purity": 1.0,
    "crystal_size": 0.09663272649049759,
    "crystal_yield": 0.45468825101852417,
    "degradation_warning": 0.14530925452709198,
    "safety_risk": 0.18237976729869843,
    "score": 0.5319308042526245,
    "selectivity": 0.5215754508972168,
    "virtual_spectrum_summary": 0.2598748505115509,
    "yield": 0.5079457759857178
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
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
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
  "end_step": 64,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.46807536482810974,
    "conversion": 0.996337890625,
    "cost": 1.0,
    "crystal_csd_quality": 0.6980047225952148,
    "crystal_fines_fraction": 0.39016029238700867,
    "crystal_purity": 0.9698945879936218,
    "crystal_size": 0.0610148124396801,
    "crystal_yield": 0.32856908440589905,
    "degradation_warning": 0.20744232833385468,
    "safety_risk": 0.18001754581928253,
    "score": 0.4357876181602478,
    "selectivity": 0.4138229489326477,
    "virtual_spectrum_summary": 0.35079050064086914,
    "yield": 0.4076699912548065
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
      "stirring_speed_rpm": 600,
      "target_temperature_K": 360
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
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
  "end_step": 77,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.4175972640514374,
    "conversion": 0.9924335479736328,
    "cost": 1.0,
    "crystal_csd_quality": 0.7574855089187622,
    "crystal_fines_fraction": 0.22868801653385162,
    "crystal_purity": 1.0,
    "crystal_size": 0.06977060437202454,
    "crystal_yield": 0.44002586603164673,
    "degradation_warning": 0.23045890033245087,
    "safety_risk": 0.17977002263069153,
    "score": 0.5128730535507202,
    "selectivity": 0.4850682020187378,
    "virtual_spectrum_summary": 0.33338499069213867,
    "yield": 0.48695382475852966
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
      "stirring_speed_rpm": 600,
      "target_temperature_K": 360
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
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
  "end_step": 90,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.38504043221473694,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7664691209793091,
    "crystal_fines_fraction": 0.20058013498783112,
    "crystal_purity": 0.980758011341095,
    "crystal_size": 0.10661684721708298,
    "crystal_yield": 0.38718122243881226,
    "degradation_warning": 0.11541087180376053,
    "safety_risk": 0.1715969294309616,
    "score": 0.4935154914855957,
    "selectivity": 0.40834665298461914,
    "virtual_spectrum_summary": 0.26370713114738464,
    "yield": 0.4349938631057739
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
      "stirring_speed_rpm": 600,
      "target_temperature_K": 360
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
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
  "end_step": 103,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.41666126251220703,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.8043287396430969,
    "crystal_fines_fraction": 0.19159859418869019,
    "crystal_purity": 0.9810075163841248,
    "crystal_size": 0.12524692714214325,
    "crystal_yield": 0.4401494264602661,
    "degradation_warning": 0.23731285333633423,
    "safety_risk": 0.17838110029697418,
    "score": 0.5269025564193726,
    "selectivity": 0.48597386479377747,
    "virtual_spectrum_summary": 0.335954487323761,
    "yield": 0.4776686131954193
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
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
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
  "end_step": 120,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.3997141718864441,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7881776690483093,
    "crystal_fines_fraction": 0.1927780658006668,
    "crystal_purity": 0.9831787347793579,
    "crystal_size": 0.0768619179725647,
    "crystal_yield": 0.4646744430065155,
    "degradation_warning": 0.17267145216464996,
    "safety_risk": 0.1822604089975357,
    "score": 0.5282780528068542,
    "selectivity": 0.48859483003616333,
    "virtual_spectrum_summary": 0.2975449562072754,
    "yield": 0.5022707581520081
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
      "target_temperature_K": 360
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
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
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.35818660259246826,
    "conversion": 0.9858242273330688,
    "cost": 1.0,
    "crystal_csd_quality": 0.6906047463417053,
    "crystal_fines_fraction": 0.3947072923183441,
    "crystal_purity": 0.981847882270813,
    "crystal_size": 0.07204918563365936,
    "crystal_yield": 0.4947732090950012,
    "degradation_warning": 0.16037389636039734,
    "safety_risk": 0.2127082496881485,
    "score": 0.49978333711624146,
    "selectivity": 0.5274567604064941,
    "virtual_spectrum_summary": 0.269170880317688,
    "yield": 0.5363835692405701
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
      "stirring_speed_rpm": 600,
      "target_temperature_K": 360
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
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
  "end_step": 154,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.39304280281066895,
    "conversion": 0.9990203976631165,
    "cost": 1.0,
    "crystal_csd_quality": 0.500590443611145,
    "crystal_fines_fraction": 0.9934753179550171,
    "crystal_purity": 1.0,
    "crystal_size": 0.06450099498033524,
    "crystal_yield": 0.48319360613822937,
    "degradation_warning": 0.14854039251804352,
    "safety_risk": 0.31484904885292053,
    "score": 0.3945084810256958,
    "selectivity": 0.5393504500389099,
    "virtual_spectrum_summary": 0.28301671147346497,
    "yield": 0.5198606252670288
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
      "target_temperature_K": 360
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
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
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 315
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
  "end_step": 173,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.388639360666275,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7199689149856567,
    "crystal_fines_fraction": 0.3854697346687317,
    "crystal_purity": 0.9975873827934265,
    "crystal_size": 0.09728261083364487,
    "crystal_yield": 0.46127063035964966,
    "degradation_warning": 0.18816342949867249,
    "safety_risk": 0.20603536069393158,
    "score": 0.49807095527648926,
    "selectivity": 0.49497437477111816,
    "virtual_spectrum_summary": 0.29842519760131836,
    "yield": 0.5000163912773132
  },
  "ordinal": 12
}
```

## K1

```json
{
  "payload": {
    "report": "Mechanistic account\n\nScope and material identity\nThe reagent, catalysts C0\u2013C3, and solvents S0\u2013S3 are anonymous benchmark materials, so the evidence supports only operational effects, not claims about real molecular identities or specific functional groups.\n\nObserved material effects\n\u2022 Solvent was the dominant morphology variable. With C0 and 0.08 L solvent, batch 4 using S2 gave crystal recovery 0.4547, purity 1.000, and fines fraction 0.2073. Comparable screens gave poorer combinations: S0 in batch 2 produced recovery 0.4901 but fines 0.5105, just outside specification; S1 in batch 3 gave recovery 0.2953 and fines 0.5101; S3 in batch 5 gave recovery 0.3286 and fines 0.3902. Batch 3 used a somewhat different aging endpoint, so its recovery is not a clean solvent-only comparison. Nevertheless, the large fines advantage of S2 was reproducible across later S2 batches.\n\u2022 In the controlled S2/0.08 L catalyst screen, C0 (batch 4) gave the highest recovery, 0.4547. C1, C2, and C3 in batches 6\u20138 gave 0.4400, 0.3872, and 0.4401, respectively. All met the purity and fines constraints. C3 gave slightly better morphology than C0\u2014fines 0.1916 and CSD quality 0.8043\u2014but lower recovery. Thus C0 was preferred for the stated recovery objective, not because it dominated every quality measure.\n\nInterpretation of material effects\nS2 likely provides a favorable balance between target solubility and supersaturation generation. This is an operational interpretation only; its anonymous identity prevents a molecular explanation. C0 appears to generate a reaction mixture whose target/impurity composition is more favorable for recovery than C1\u2013C3. Catalyst choice also changed reaction selectivity, byproduct signal, and degradation warning, so its crystallization effect may be indirect through the composition entering crystallization rather than a direct action on crystal surfaces.\n\nReaction\u2013crystallization coupling\nReaction metrics and crystallization recovery describe different denominators. The relevant definition is\n\nY_crystal = n(target recovered as crystals, excluding seed) / n(target present before separation).\n\nAn approximate overall yield from charged reagent would scale as\n\nY_overall \u2248 Y_reaction \u00d7 Y_crystal,\n\nalthough that product is only a useful bookkeeping approximation here. For batch 10 it is about 0.5364 \u00d7 0.4948 \u2248 0.265, while the campaign objective was specifically the second factor.\n\nThe crystals purified the moderately selective reaction mixtures strongly. In batch 10, reaction yield was 0.5364, selectivity 0.5275, and byproduct signal 0.3582, yet crystal purity was 0.9818. Batch 4 similarly combined reaction yield 0.5079 with crystal purity 1.000. This observation is consistent with preferential incorporation of target and rejection of impurities into mother liquor. A useful conceptual parameter is an impurity distribution coefficient, k_i = x_i,solid/x_i,liquid; the results suggest k_i below unity, but liquid/solid compositions were not measured separately, so that interpretation remains unverified.\n\nCrystallization mechanism and process-history dependence\nA useful description is supersaturation S = C/C*(T, solvent), with chemical driving force \u0394\u03bc = RT ln S. Qualitatively, classical nucleation gives J proportional to exp[-B/(ln S)^2], whereas crystal growth can be represented as G = k_g(S\u22121)^g. Because nucleation responds very sharply to supersaturation, increasing concentration may raise recovery while disproportionately increasing the number of sub-20 \u00b5m particles. Crystal size retains the entire time history through approximately \u0394L = \u222bG(S(t),T(t))dt. The number-based fines fraction is the integral of the particle-number distribution below 20 \u00b5m divided by total particle number.\n\nThe initial S0 process illustrates this history effect. Batch 1 used only 0.02 g seed and direct cooling to 270 K; it gave recovery 0.4886 but fines 0.6608. Batch 2 used 0.05 g seed, staged cooling, long low-speed aging, and a 250 K endpoint; crystal size increased from 0.0636 to 0.1040 on the normalized assay scale and fines fell to 0.5105. Because seed dose, cooling path, and endpoint all changed together, this does not isolate a pure seed effect, but it motivated subsequent staged cooling and maximum tested seeding.\n\nWithin S2, longer low-temperature aging produced only modest gains. Batch 4 gave recovery 0.4547 and fines 0.2073. Batch 9 added several 250 K aging periods and gave recovery 0.4647 and fines 0.1928. These changes are comparable to the stated final-assay noise (about 0.01 for recovery and 0.018 for fines), so extended aging is at most weakly supported as beneficial.\n\nSolvent volume exposed the central tradeoff. At 0.08 L S2, batch 9 had recovery 0.4647 and fines 0.1928. Reducing S2 to 0.04 L in batch 10 raised measured recovery to 0.4948 but also raised fines to 0.3947. At 0.02 L, despite a much slower multistage history, batch 11 produced fines 0.9935 and recovery only 0.4832. This strongly suggests excessive supersaturation and secondary nucleation at the lowest volume. The relationship is nonlinear: concentration improved recovery only modestly before morphology collapsed.\n\nA thermal-cycle alternative was tested in batch 12 at 0.04 L S2. Reheating the seeded slurry to 315 K before final cooling gave recovery 0.4613 and fines 0.3855, versus 0.4948 and 0.3947 in batch 10. The cycle did not materially improve fines and apparently sacrificed recovery. It may have partially dissolved product that was not fully regrown, although one experiment cannot distinguish this from process variation.\n\nDevelopment revisions\nThe campaign began with S0, where recovery was already near 0.49 but fines failed. Seeding and staged cooling improved size but did not bring S0 clearly within specification. Solvent screening identified S2 as the reliable low-fines medium. Catalyst screening then favored C0 for recovery. Longer aging was explored, followed by solvent-volume reduction to increase recovery. The 0.04 L condition in batch 10 gave the best feasible balance; further reduction to 0.02 L caused catastrophic fines, and thermal cycling did not improve the balance.\n\nRecommended sealed batch and uncertainty\nBatch 10 remains the recommendation: 0.040 mol reagent, 0.040 L S2, and 0.005 mol C0; heat at 360 K for 3600 s with 600 rpm stirring; cool to 330 K over 7200 s; add 0.050 g seed; cool to 300 K over 14400 s; age 14400 s at 100 rpm; cool to 250 K over 14400 s; age for three further 14400 s periods at 100 rpm; then filter, terminate, and assay. Its measured recovery was 0.4948, purity 0.9818, and fines fraction 0.3947. Safety risk was 0.2127, below the 0.65 limit.\n\nThe final-assay standard-noise scales were approximately 0.01 for recovery and purity and 0.018 for fines. Batch 10 therefore has substantial observed margins to both constraints: +0.1818 in purity and \u22120.1053 in fines. Its recovery advantage over some nearby S2 processes is less decisive because most conditions were run only once. Batch 2 had a similar recovery, 0.4901, but its fines value of 0.5105 is too close to the boundary to recommend under measurement and process uncertainty.\n\nUnresolved alternatives\nThe most promising untested region is an S2 volume between 0.04 and 0.08 L, combined with independently varied seeding temperature, seed dose, and cooling rate. That region may preserve more of batch 10\u2019s recovery while approaching the robust low-fines behavior of batches 4 and 9. Replication of batch 10 is also needed to quantify process variance. No unseeded control, systematic catalyst-loading study, quench study, or full catalyst-by-solvent interaction matrix was performed. Consequently, the evidence supports a practical supersaturation/nucleation interpretation, but not a unique microscopic mechanism."
  },
  "failure": null,
  "elapsed_s": 75.90600000000268,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 849792,
    "input_tokens": 959804,
    "output_tokens": 11501,
    "reasoning_output_tokens": 3914
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
          "estimate": 0.48,
          "lower80": 0.32,
          "upper80": 0.64
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.93,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.105,
          "lower80": 0.06,
          "upper80": 0.16
        },
        "crystal_yield": {
          "estimate": 0.29,
          "lower80": 0.17,
          "upper80": 0.41
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q01"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.35,
          "lower80": 0.22,
          "upper80": 0.5
        },
        "crystal_purity": {
          "estimate": 0.96,
          "lower80": 0.9,
          "upper80": 0.995
        },
        "crystal_size": {
          "estimate": 0.115,
          "lower80": 0.07,
          "upper80": 0.17
        },
        "crystal_yield": {
          "estimate": 0.33,
          "lower80": 0.21,
          "upper80": 0.45
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q02"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.72,
          "lower80": 0.53,
          "upper80": 0.88
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.93,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.06,
          "lower80": 0.025,
          "upper80": 0.11
        },
        "crystal_yield": {
          "estimate": 0.38,
          "lower80": 0.25,
          "upper80": 0.5
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q03"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.47,
          "lower80": 0.32,
          "upper80": 0.62
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.94,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.12,
          "lower80": 0.075,
          "upper80": 0.18
        },
        "crystal_yield": {
          "estimate": 0.4,
          "lower80": 0.28,
          "upper80": 0.52
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q04"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.42,
          "lower80": 0.28,
          "upper80": 0.57
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.94,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.125,
          "lower80": 0.08,
          "upper80": 0.185
        },
        "crystal_yield": {
          "estimate": 0.4,
          "lower80": 0.28,
          "upper80": 0.52
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
          "estimate": 0.95,
          "lower80": 0.87,
          "upper80": 0.995
        },
        "crystal_size": {
          "estimate": 0.055,
          "lower80": 0.02,
          "upper80": 0.1
        },
        "crystal_yield": {
          "estimate": 0.42,
          "lower80": 0.3,
          "upper80": 0.54
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q06"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.43,
          "lower80": 0.29,
          "upper80": 0.58
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.94,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.12,
          "lower80": 0.075,
          "upper80": 0.18
        },
        "crystal_yield": {
          "estimate": 0.4,
          "lower80": 0.28,
          "upper80": 0.52
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q07"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.4,
          "lower80": 0.26,
          "upper80": 0.56
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.93,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.135,
          "lower80": 0.08,
          "upper80": 0.2
        },
        "crystal_yield": {
          "estimate": 0.34,
          "lower80": 0.21,
          "upper80": 0.47
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q08"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.86,
          "lower80": 0.68,
          "upper80": 0.97
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.9,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.035,
          "lower80": 0.01,
          "upper80": 0.075
        },
        "crystal_yield": {
          "estimate": 0.015,
          "lower80": 0.0,
          "upper80": 0.07
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q09"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.66,
          "lower80": 0.47,
          "upper80": 0.84
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.91,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.05,
          "lower80": 0.02,
          "upper80": 0.095
        },
        "crystal_yield": {
          "estimate": 0.11,
          "lower80": 0.035,
          "upper80": 0.21
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q10"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.45,
          "lower80": 0.3,
          "upper80": 0.61
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.94,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.12,
          "lower80": 0.075,
          "upper80": 0.18
        },
        "crystal_yield": {
          "estimate": 0.4,
          "lower80": 0.28,
          "upper80": 0.52
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q11"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.67,
          "lower80": 0.49,
          "upper80": 0.83
        },
        "crystal_purity": {
          "estimate": 0.94,
          "lower80": 0.85,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.075,
          "lower80": 0.035,
          "upper80": 0.13
        },
        "crystal_yield": {
          "estimate": 0.49,
          "lower80": 0.36,
          "upper80": 0.61
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q12"
      }
    ],
    "rationale": "All recipes deliberately add seed, so particles are expected even when little seed-excluded product has grown. Q01\u2013Q02: S3 is predicted to suppress fines better and recover slightly more target than S1, consistent with the solvent screen, although Q01 lies near the fines boundary. Q03\u2013Q04: increasing seed from 0.001 to 0.045 g should provide much more growth surface, limiting supersaturation accumulation and secondary nucleation; the small-seed case is therefore predicted to fail on fines. Q05\u2013Q06: the slow ramp should produce larger, less fine particles than the 120 s temperature drop; the long final hold makes their recoveries similar but is not expected to erase the rapid-cooling nucleation history. Q07\u2013Q08: the 315 K thermal cycle may dissolve smaller particles and increase mean size, but prior evidence indicates incomplete recovery after reheating, so Q08 has lower predicted yield without a decisive fines advantage. Q09\u2013Q10: two hours at 292 K allows measurable growth relative to immediate filtration, but both retain a high-fines history and Q09 has almost no seed-excluded recovery. Q11\u2013Q12: doubling reagent concentration should increase recovery, but also supersaturation, impurity loading, and secondary nucleation, creating a recovery\u2013fines tradeoff. Intervals represent epistemic and process-history uncertainty in these extrapolated noise-free outcomes, especially for boundary cases and the very rapid cooling recipes."
  },
  "failure": null,
  "elapsed_s": 111.70300000000861,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 849792,
    "input_tokens": 1024574,
    "output_tokens": 16712,
    "reasoning_output_tokens": 7399
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
    "report": "1. Status of the main claims\n\nSupported by direct observations:\n\n- **S2 gave the most robust morphology in the tested solvent screen.** With C0 and 0.08 L solvent, batch 4 (S2) had recovery 0.4547, purity 1.000, and fines 0.2073. Batch 2 (S0) had comparable recovery, 0.4901, but fines 0.5105; batch 5 (S3) had lower recovery, 0.3286, and fines 0.3902. Batch 3 (S1) had recovery 0.2953 and fines 0.5101, although its aging history differed. The observation supports an operational S2 effect; the proposed solubility/supersaturation explanation remains interpretive because the solvents are anonymous and solubility was not measured.\n\n- **C0 was the best tested catalyst for recovery under the matched S2 schedule.** Batches 4, 6, 7, and 8 compared C0\u2013C3. Their recoveries were 0.4547, 0.4400, 0.3872, and 0.4401. C3 had somewhat better morphology than C0, so the direct conclusion is only that C0 best served the recovery objective under those conditions\u2014not that it was universally superior.\n\n- **The reaction mixture underwent strong crystallization-stage purification.** Batch 10 had reaction yield 0.5364, selectivity 0.5275, and byproduct signal 0.3582, but crystal purity 0.9818. Batch 4 showed the same pattern. Preferential impurity rejection is a reasonable interpretation, but no separate mother-liquor composition or solid/liquid distribution coefficient was measured.\n\n- **There was a recovery\u2013fines tradeoff with solvent volume.** Batch 9 at 0.08 L S2 gave recovery 0.4647 and fines 0.1928; batch 10 at 0.04 L gave recovery 0.4948 and fines 0.3947. At 0.02 L, batch 11 gave recovery 0.4832 but fines 0.9935. The severe fines increase at 0.02 L directly contradicts any simple claim that concentration can be increased indefinitely to improve recovery without a morphology penalty.\n\n- **The tested thermal cycle was not beneficial.** Relative to batch 10, batch 12\u2019s reheating cycle gave lower recovery, 0.4613 versus 0.4948, with essentially no convincing fines improvement, 0.3855 versus 0.3947. This contradicts a strong claim that the cycle would solve the quality\u2013recovery tradeoff, although it does not exclude a differently designed cycle.\n\nWeakly supported or confounded:\n\n- **More seed and staged cooling probably reduced fines**, but batches 1 and 2 changed seed mass, cooling path, endpoint, and aging time simultaneously. Fines fell from 0.6608 to 0.5105 and normalized size rose from 0.0636 to 0.1040, but the specific causal contribution of seed mass was not isolated.\n\n- **Long low-temperature aging may slightly improve recovery and morphology.** Batch 4 versus batch 9 changed recovery from 0.4547 to 0.4647 and fines from 0.2073 to 0.1928. Those differences are comparable to assay uncertainty, so a large aging effect is not supported.\n\nStill untested:\n\n- Catalyst-by-solvent interactions, an unseeded control, systematic seed-temperature and seed-dose effects, catalyst loading, quench dependence, and direct solubility curves were not tested. The proposed nucleation and growth equations are useful organizing models, not identified kinetic laws for these anonymous materials.\n\n2. One additional experiment\n\nI would run an intermediate-volume experiment: reproduce batch 10 exactly, but use 0.060 L S2 instead of 0.040 L. I would add nondestructive particle-size measurements after the 300 K aging period, immediately after reaching 250 K, and after the final 250 K aging period, followed by the normal filtration and final assay.\n\nThis would distinguish two explanations for the contrast among batches 9\u201311:\n\n- **Smooth supersaturation tradeoff:** recovery and fines should both fall between the batch-9 and batch-10 values. A plausible result would be recovery around 0.47\u20130.49 and fines around 0.25\u20130.32.\n- **Threshold nucleation:** the 0.060 L condition could retain the low-fines behavior of batch 9 while approaching batch 10\u2019s recovery, indicating that the morphology failure begins only after crossing a concentration threshold. Conversely, fines similar to batch 10 would imply that the threshold lies above 0.08 L but below or near 0.06 L.\n\nThe trajectory measurements would further separate a nucleation burst during cooling from continued secondary nucleation or ripening during aging. An abrupt increase in fines on reaching 250 K would support cooling-driven primary nucleation; rising fines during holds would support continuing secondary nucleation; falling fines with increasing size would support ripening. Repeating the full batch-10 recipe would better quantify reproducibility, but the 0.060 L experiment provides more discrimination and optimization value in a single run.\n\n3. Least-used observation and least-reliable held-out prediction\n\nThe account used the batch-9 in-process particle-size measurement least effectively. Before filtration it reported size 0.0919 and fines 0.2024, whereas the final assay reported size 0.0769 and fines 0.1928. That paired observation could have been used more explicitly to discuss instrument/process-context differences: fines agreed reasonably well, but size differed materially relative to its scale. It cautions against interpreting small size changes across batches as mechanistic without matched measurements.\n\nQ09 is the least reliable held-out prediction. It filters only 60 seconds after cooling to 292 K, far outside the histories explored experimentally. No campaign batch assayed a slurry immediately after seeding and such a short crystallization interval. Its outcome depends sensitively on unmeasured induction time, how much seed-derived particle population persists, and whether any detectable seed-excluded target deposits before filtration. Thus the sealed estimates for its very low recovery, small size, and high fines rely much more on extrapolation than those for the long-ramp recipes. No prediction is revised here."
  },
  "failure": null,
  "elapsed_s": 59.96899999999732,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 902272,
    "input_tokens": 1094475,
    "output_tokens": 19194,
    "reasoning_output_tokens": 8488
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
    "selected_experiment_index": 10,
    "selection_rationale": "Batch 10 had the highest measured seed-excluded crystal recovery among batches meeting both quality constraints: crystal_yield 0.4948, crystal_purity 0.9818, and fines fraction 0.3947."
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
        "target_temperature_K": 360
      },
      {
        "duration_s": 7200,
        "operation": "cool_crystallize",
        "target_temperature_K": 330
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
    "lifecycle_index": 10,
    "source_attempts": 15
  },
  "prediction_evaluation": {
    "contrasts": [
      {
        "absolute_delta_error": 0.1129406234377425,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_yield",
        "predicted_delta": 0.040000000000000036,
        "resolved": true,
        "true_delta": -0.07294062343774246
      },
      {
        "absolute_delta_error": 0.018746122547241728,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_purity",
        "predicted_delta": -0.020000000000000018,
        "resolved": false,
        "true_delta": -0.0012538774527582897
      },
      {
        "absolute_delta_error": 0.005653301928301976,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_size",
        "predicted_delta": 0.010000000000000009,
        "resolved": true,
        "true_delta": 0.015653301928301985
      },
      {
        "absolute_delta_error": 0.31321528505582213,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.13,
        "resolved": true,
        "true_delta": -0.44321528505582214
      },
      {
        "absolute_delta_error": 0.0200483374877648,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_yield",
        "predicted_delta": 0.020000000000000018,
        "resolved": false,
        "true_delta": -4.8337487764782416e-05
      },
      {
        "absolute_delta_error": 0.008132470445263329,
        "direction_correct": true,
        "factor": "seed",
        "metric": "crystal_purity",
        "predicted_delta": 0.0,
        "resolved": false,
        "true_delta": 0.008132470445263329
      },
      {
        "absolute_delta_error": 0.059577504392599276,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_size",
        "predicted_delta": 0.06,
        "resolved": false,
        "true_delta": 0.0004224956074007219
      },
      {
        "absolute_delta_error": 0.2251737603270197,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.25,
        "resolved": false,
        "true_delta": -0.02482623967298031
      },
      {
        "absolute_delta_error": 0.019767182469520916,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_yield",
        "predicted_delta": 0.019999999999999962,
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
        "absolute_delta_error": 0.0307945906364231,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_size",
        "predicted_delta": -0.07,
        "resolved": true,
        "true_delta": -0.03920540936357691
      },
      {
        "absolute_delta_error": 0.31637716023803625,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.36000000000000004,
        "resolved": true,
        "true_delta": 0.6763771602380363
      },
      {
        "absolute_delta_error": 0.1015617281802011,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_yield",
        "predicted_delta": -0.06,
        "resolved": true,
        "true_delta": 0.041561728180201096
      },
      {
        "absolute_delta_error": 0.009264167065397011,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_purity",
        "predicted_delta": 0.0,
        "resolved": false,
        "true_delta": -0.009264167065397011
      },
      {
        "absolute_delta_error": 0.045443732116858405,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_size",
        "predicted_delta": 0.015000000000000013,
        "resolved": true,
        "true_delta": -0.030443732116858392
      },
      {
        "absolute_delta_error": 0.7261786076870267,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.02999999999999997,
        "resolved": true,
        "true_delta": 0.6961786076870267
      },
      {
        "absolute_delta_error": 0.05572767781178037,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_yield",
        "predicted_delta": 0.095,
        "resolved": true,
        "true_delta": 0.15072767781178037
      },
      {
        "absolute_delta_error": 0.014073023719337607,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_purity",
        "predicted_delta": 0.0,
        "resolved": true,
        "true_delta": -0.014073023719337607
      },
      {
        "absolute_delta_error": 0.0001242016094623946,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_size",
        "predicted_delta": 0.015,
        "resolved": true,
        "true_delta": 0.014875798390537605
      },
      {
        "absolute_delta_error": 0.22026443684698083,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.19999999999999996,
        "resolved": false,
        "true_delta": 0.02026443684698087
      },
      {
        "absolute_delta_error": 0.059259746270580504,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_yield",
        "predicted_delta": 0.08999999999999997,
        "resolved": true,
        "true_delta": 0.030740253729419464
      },
      {
        "absolute_delta_error": 0.033976332586183156,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_purity",
        "predicted_delta": -0.040000000000000036,
        "resolved": false,
        "true_delta": -0.00602366741381688
      },
      {
        "absolute_delta_error": 0.017436293373212806,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_size",
        "predicted_delta": -0.045,
        "resolved": true,
        "true_delta": -0.027563706626787192
      },
      {
        "absolute_delta_error": 0.4685789828624289,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.22000000000000003,
        "resolved": true,
        "true_delta": 0.6885789828624289
      }
    ],
    "failures": [],
    "metrics": {
      "crystal_fines_fraction": {
        "coverage80": 0.4166666666666667,
        "interval_score80": 1.3114237081061522,
        "interval_width": 0.3125,
        "mae": 0.23467824748431318,
        "n": 12,
        "planned": 12
      },
      "crystal_purity": {
        "coverage80": 1.0,
        "interval_score80": 0.08333333333333333,
        "interval_width": 0.08333333333333333,
        "mae": 0.01355258253847443,
        "n": 12,
        "planned": 12
      },
      "crystal_size": {
        "coverage80": 0.9166666666666666,
        "interval_score80": 0.11690442232604244,
        "interval_width": 0.09499999999999999,
        "mae": 0.028933429136757043,
        "n": 12,
        "planned": 12
      },
      "crystal_yield": {
        "coverage80": 0.8333333333333334,
        "interval_score80": 0.26460972621923545,
        "interval_width": 0.22375,
        "mae": 0.08488591451837886,
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
    "tie_correct": 3,
    "tie_n": 10,
    "valid": true
  },
  "public_baselines": {
    "available": true,
    "mae": {
      "public_mean": {
        "crystal_fines_fraction": 0.31402314041245477,
        "crystal_purity": 0.004416027635150348,
        "crystal_size": 0.016829786605029148,
        "crystal_yield": 0.1820380860955467
      },
      "public_nearest_neighbor": {
        "crystal_fines_fraction": 0.29150515878387784,
        "crystal_purity": 0.008339580174633673,
        "crystal_size": 0.02855487903765346,
        "crystal_yield": 0.2063622002195269
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
        "cached_input": 849792,
        "input": 907120,
        "output": 7951,
        "stage": "source",
        "uncached_input": 57328
      },
      {
        "cached_input": 0,
        "input": 52684,
        "output": 3550,
        "stage": "K1",
        "uncached_input": 52684
      },
      {
        "cached_input": 0,
        "input": 64770,
        "output": 5211,
        "stage": "Q",
        "uncached_input": 64770
      },
      {
        "cached_input": 52480,
        "input": 69901,
        "output": 2482,
        "stage": "K2",
        "uncached_input": 17421
      }
    ],
    "total": {
      "cached_input": 902272,
      "input": 1094475,
      "input_plus_output": 1113669,
      "output": 19194,
      "uncached_input": 192203
    },
    "valid": true
  },
  "elapsed_s": 572.8129999999946
}
```
