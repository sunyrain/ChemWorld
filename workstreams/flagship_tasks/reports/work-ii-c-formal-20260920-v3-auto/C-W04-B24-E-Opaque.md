# C-W04-B24-E-Opaque

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
    "byproduct_signal": 0.26710912585258484,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5060065984725952,
    "crystal_fines_fraction": 0.9973246455192566,
    "crystal_purity": 0.9782281517982483,
    "crystal_size": 0.05436402186751366,
    "crystal_yield": 0.4577977657318115,
    "degradation_warning": 0.0941338762640953,
    "safety_risk": 0.14257879555225372,
    "score": 0.40564343333244324,
    "selectivity": 0.588407039642334,
    "virtual_spectrum_summary": 0.1892702728509903,
    "yield": 0.5862307548522949
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
  "end_step": 27,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.27146026492118835,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.49287480115890503,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9753977656364441,
    "crystal_size": 0.08801805227994919,
    "crystal_yield": 0.45658960938453674,
    "degradation_warning": 0.0905148983001709,
    "safety_risk": 0.14303986728191376,
    "score": 0.40790536999702454,
    "selectivity": 0.6089280843734741,
    "virtual_spectrum_summary": 0.19003485143184662,
    "yield": 0.5974689722061157
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
      "operation": "quench"
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
  "end_step": 42,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.2650253474712372,
    "conversion": 0.9982944130897522,
    "cost": 1.0,
    "crystal_csd_quality": 0.4960997998714447,
    "crystal_fines_fraction": 0.9949334263801575,
    "crystal_purity": 0.981200635433197,
    "crystal_size": 0.04885406047105789,
    "crystal_yield": 0.4560745358467102,
    "degradation_warning": 0.10590473562479019,
    "safety_risk": 0.1424066722393036,
    "score": 0.402425616979599,
    "selectivity": 0.5819226503372192,
    "virtual_spectrum_summary": 0.19342108070850372,
    "yield": 0.5810216665267944
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
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 100,
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
  "end_step": 58,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.25907352566719055,
    "conversion": 0.9889729619026184,
    "cost": 1.0,
    "crystal_csd_quality": 0.4917896091938019,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 1.0,
    "crystal_size": 0.059278454631567,
    "crystal_yield": 0.47139087319374084,
    "degradation_warning": 0.07591953128576279,
    "safety_risk": 0.1424688994884491,
    "score": 0.40891560912132263,
    "selectivity": 0.5875601768493652,
    "virtual_spectrum_summary": 0.17665423452854156,
    "yield": 0.5739167928695679
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
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.001
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
  "end_step": 72,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.32373711466789246,
    "conversion": 0.9963371157646179,
    "cost": 1.0,
    "crystal_csd_quality": 0.49325892329216003,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9685777425765991,
    "crystal_size": 0.040178634226322174,
    "crystal_yield": 0.42091235518455505,
    "degradation_warning": 0.10339445620775223,
    "safety_risk": 0.15907980501651764,
    "score": 0.3761906623840332,
    "selectivity": 0.5220299363136292,
    "virtual_spectrum_summary": 0.22458291053771973,
    "yield": 0.5158765912055969
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
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
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
  "end_step": 86,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.321138858795166,
    "conversion": 0.992433488368988,
    "cost": 1.0,
    "crystal_csd_quality": 0.4794580936431885,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9996981024742126,
    "crystal_size": 0.034056007862091064,
    "crystal_yield": 0.457518994808197,
    "degradation_warning": 0.13660714030265808,
    "safety_risk": 0.162346750497818,
    "score": 0.38990896940231323,
    "selectivity": 0.5274266600608826,
    "virtual_spectrum_summary": 0.2380995899438858,
    "yield": 0.529312252998352
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
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.001
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
  "end_step": 100,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.33788642287254333,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.4835057556629181,
    "crystal_fines_fraction": 0.9868525862693787,
    "crystal_purity": 0.9717432856559753,
    "crystal_size": 0.07598736137151718,
    "crystal_yield": 0.4038693308830261,
    "degradation_warning": 0.11491415649652481,
    "safety_risk": 0.1546315997838974,
    "score": 0.36587902903556824,
    "selectivity": 0.4468376636505127,
    "virtual_spectrum_summary": 0.23754890263080597,
    "yield": 0.47348421812057495
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
  "end_step": 114,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.31271225214004517,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5227375030517578,
    "crystal_fines_fraction": 0.9869732856750488,
    "crystal_purity": 0.9727449417114258,
    "crystal_size": 0.09007052332162857,
    "crystal_yield": 0.4569131135940552,
    "degradation_warning": 0.13569273054599762,
    "safety_risk": 0.16090098023414612,
    "score": 0.39902663230895996,
    "selectivity": 0.52792888879776,
    "virtual_spectrum_summary": 0.23305347561836243,
    "yield": 0.5196231603622437
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
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.001
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
  "end_step": 128,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.35688653588294983,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5400579571723938,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9760684370994568,
    "crystal_size": 0.037107937037944794,
    "crystal_yield": 0.3920506238937378,
    "degradation_warning": 0.12954393029212952,
    "safety_risk": 0.17132379114627838,
    "score": 0.3648463189601898,
    "selectivity": 0.43411117792129517,
    "virtual_spectrum_summary": 0.25458237528800964,
    "yield": 0.4477871060371399
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
  "end_step": 142,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.3577243685722351,
    "conversion": 0.9858242273330688,
    "cost": 1.0,
    "crystal_csd_quality": 0.5101879239082336,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9788604378700256,
    "crystal_size": 0.049570392817258835,
    "crystal_yield": 0.4101768434047699,
    "degradation_warning": 0.17722520232200623,
    "safety_risk": 0.17366497218608856,
    "score": 0.36951392889022827,
    "selectivity": 0.4629099667072296,
    "virtual_spectrum_summary": 0.27649974822998047,
    "yield": 0.47183677554130554
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
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.001
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
  "end_step": 156,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.3873378038406372,
    "conversion": 0.9990202784538269,
    "cost": 1.0,
    "crystal_csd_quality": 0.49132341146469116,
    "crystal_fines_fraction": 0.9936819672584534,
    "crystal_purity": 0.987194836139679,
    "crystal_size": 0.059439755976200104,
    "crystal_yield": 0.34652179479599,
    "degradation_warning": 0.13492009043693542,
    "safety_risk": 0.1666848063468933,
    "score": 0.3428652882575989,
    "selectivity": 0.4231142997741699,
    "virtual_spectrum_summary": 0.27374982833862305,
    "yield": 0.40362441539764404
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
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.001
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
  "end_step": 170,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.3587617576122284,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5413239598274231,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9894875884056091,
    "crystal_size": 0.07736630737781525,
    "crystal_yield": 0.3936067819595337,
    "degradation_warning": 0.17590351402759552,
    "safety_risk": 0.17237234115600586,
    "score": 0.37375500798225403,
    "selectivity": 0.4485194683074951,
    "virtual_spectrum_summary": 0.27647554874420166,
    "yield": 0.4535614550113678
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
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.001
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
  "end_step": 184,
  "lifecycle_index": 13,
  "metrics": {
    "byproduct_signal": 0.3512422442436218,
    "conversion": 0.9972167015075684,
    "cost": 1.0,
    "crystal_csd_quality": 0.505246102809906,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9670558571815491,
    "crystal_size": 0.05556628480553627,
    "crystal_yield": 0.3613066077232361,
    "degradation_warning": 0.14619189500808716,
    "safety_risk": 0.18306373059749603,
    "score": 0.3526138663291931,
    "selectivity": 0.46550852060317993,
    "virtual_spectrum_summary": 0.25896957516670227,
    "yield": 0.45749586820602417
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
      "stirring_speed_rpm": 600,
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
  "end_step": 198,
  "lifecycle_index": 14,
  "metrics": {
    "byproduct_signal": 0.37565866112709045,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5097880959510803,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9540799856185913,
    "crystal_size": 0.09955178201198578,
    "crystal_yield": 0.3800339996814728,
    "degradation_warning": 0.1907738447189331,
    "safety_risk": 0.1850740909576416,
    "score": 0.3616368770599365,
    "selectivity": 0.47328075766563416,
    "virtual_spectrum_summary": 0.29246050119400024,
    "yield": 0.467093288898468
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
      "solvent": 3,
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
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.001
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
  "end_step": 212,
  "lifecycle_index": 15,
  "metrics": {
    "byproduct_signal": 0.39113906025886536,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.4698828458786011,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9745053052902222,
    "crystal_size": 0.07186691462993622,
    "crystal_yield": 0.32345837354660034,
    "degradation_warning": 0.16266924142837524,
    "safety_risk": 0.17816494405269623,
    "score": 0.3317844271659851,
    "selectivity": 0.4155949056148529,
    "virtual_spectrum_summary": 0.2883276343345642,
    "yield": 0.42012926936149597
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
  "end_step": 226,
  "lifecycle_index": 16,
  "metrics": {
    "byproduct_signal": 0.37174758315086365,
    "conversion": 0.9885534644126892,
    "cost": 1.0,
    "crystal_csd_quality": 0.4507356584072113,
    "crystal_fines_fraction": 0.9878394603729248,
    "crystal_purity": 0.9634560942649841,
    "crystal_size": 0.07073962688446045,
    "crystal_yield": 0.36535945534706116,
    "degradation_warning": 0.1943366825580597,
    "safety_risk": 0.18365468084812164,
    "score": 0.3436512351036072,
    "selectivity": 0.45681750774383545,
    "virtual_spectrum_summary": 0.29191267490386963,
    "yield": 0.45517194271087646
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
  "end_step": 247,
  "lifecycle_index": 17,
  "metrics": {
    "byproduct_signal": 0.2743507921695709,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.48369506001472473,
    "crystal_fines_fraction": 0.9720371961593628,
    "crystal_purity": 0.9836775064468384,
    "crystal_size": 0.04822144657373428,
    "crystal_yield": 0.35721075534820557,
    "degradation_warning": 0.0959038957953453,
    "safety_risk": 0.1332625150680542,
    "score": 0.37810811400413513,
    "selectivity": 0.5721244812011719,
    "virtual_spectrum_summary": 0.1940496861934662,
    "yield": 0.5822690725326538
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
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.001
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 295
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 285
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
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
  "end_step": 263,
  "lifecycle_index": 18,
  "metrics": {
    "byproduct_signal": 0.18383260071277618,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.4999179542064667,
    "crystal_fines_fraction": 0.9168923497200012,
    "crystal_purity": 0.9844737648963928,
    "crystal_size": 0.10846848785877228,
    "crystal_yield": 0.3859010338783264,
    "degradation_warning": 0.11695507913827896,
    "safety_risk": 0.06023073196411133,
    "score": 0.44035136699676514,
    "selectivity": 0.759677529335022,
    "virtual_spectrum_summary": 0.15373770892620087,
    "yield": 0.7729976773262024
  },
  "ordinal": 18
}
```

## Batch 19

```json
{
  "actions": [
    {
      "amount_mol": 0.002,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "catalyst": 0,
      "catalyst_amount_mol": 0.001,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 360
    },
    {
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.0002
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 295
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 285
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
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
  "lifecycle_index": 19,
  "metrics": {
    "byproduct_signal": 0.17334787547588348,
    "conversion": 0.8323285579681396,
    "cost": 1.0,
    "crystal_csd_quality": 1.0,
    "crystal_fines_fraction": 0.0,
    "crystal_purity": 0.9858769178390503,
    "crystal_size": 0.3799891471862793,
    "crystal_yield": 0.003889756742864847,
    "degradation_warning": 0.06661796569824219,
    "safety_risk": 0.03723476827144623,
    "score": 0.5480135083198547,
    "selectivity": 0.7784323692321777,
    "virtual_spectrum_summary": 0.12531942129135132,
    "yield": 0.6578694581985474
  },
  "ordinal": 19
}
```

## Batch 20

```json
{
  "actions": [
    {
      "amount_mol": 0.005,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "catalyst": 0,
      "catalyst_amount_mol": 0.0025,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 360
    },
    {
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.0005
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 295
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 285
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
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
  "end_step": 295,
  "lifecycle_index": 20,
  "metrics": {
    "byproduct_signal": 0.19433030486106873,
    "conversion": 0.9828803539276123,
    "cost": 1.0,
    "crystal_csd_quality": 0.48293864727020264,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9837321639060974,
    "crystal_size": 0.027873938903212547,
    "crystal_yield": 0.00934124831110239,
    "degradation_warning": 0.10236886143684387,
    "safety_risk": 0.04335939884185791,
    "score": 0.3264479339122772,
    "selectivity": 0.7823733687400818,
    "virtual_spectrum_summary": 0.15294766426086426,
    "yield": 0.757845401763916
  },
  "ordinal": 20
}
```

## Batch 21

```json
{
  "actions": [
    {
      "amount_mol": 0.0075,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "catalyst": 0,
      "catalyst_amount_mol": 0.00375,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 360
    },
    {
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.00075
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 295
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 285
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
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
  "end_step": 311,
  "lifecycle_index": 21,
  "metrics": {
    "byproduct_signal": 0.1764964461326599,
    "conversion": 0.9883114695549011,
    "cost": 1.0,
    "crystal_csd_quality": 0.48590758442878723,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9791706204414368,
    "crystal_size": 0.031417496502399445,
    "crystal_yield": 0.28647688031196594,
    "degradation_warning": 0.1092250868678093,
    "safety_risk": 0.05200573429465294,
    "score": 0.3961819112300873,
    "selectivity": 0.7580996751785278,
    "virtual_spectrum_summary": 0.14622433483600616,
    "yield": 0.7765331864356995
  },
  "ordinal": 21
}
```

## Batch 22

```json
{
  "actions": [
    {
      "amount_mol": 0.0075,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "catalyst": 0,
      "catalyst_amount_mol": 0.00375,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 360
    },
    {
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.00075
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
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 295
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 285
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
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
  "end_step": 332,
  "lifecycle_index": 22,
  "metrics": {
    "byproduct_signal": 0.2020351141691208,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.4464675486087799,
    "crystal_fines_fraction": 0.9987368583679199,
    "crystal_purity": 0.9921442866325378,
    "crystal_size": 0.04792504012584686,
    "crystal_yield": 0.27548202872276306,
    "degradation_warning": 0.11288630217313766,
    "safety_risk": 0.05200645327568054,
    "score": 0.3875090479850769,
    "selectivity": 0.755698025226593,
    "virtual_spectrum_summary": 0.16191814839839935,
    "yield": 0.7561331987380981
  },
  "ordinal": 22
}
```

## Batch 23

```json
{
  "actions": [
    {
      "amount_mol": 0.0075,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "catalyst": 0,
      "catalyst_amount_mol": 0.00375,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 360
    },
    {
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.00075
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 295
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
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
  "end_step": 348,
  "lifecycle_index": 23,
  "metrics": {
    "byproduct_signal": 0.1995677947998047,
    "conversion": 0.9939247965812683,
    "cost": 1.0,
    "crystal_csd_quality": 1.0,
    "crystal_fines_fraction": 0.0,
    "crystal_purity": 1.0,
    "crystal_size": 0.41436320543289185,
    "crystal_yield": 0.0,
    "degradation_warning": 0.10606113821268082,
    "safety_risk": 0.04976757615804672,
    "score": 0.5707300901412964,
    "selectivity": 0.7730229496955872,
    "virtual_spectrum_summary": 0.15748979151248932,
    "yield": 0.773937463760376
  },
  "ordinal": 23
}
```

## Batch 24

```json
{
  "actions": [
    {
      "amount_mol": 0.0075,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "catalyst": 0,
      "catalyst_amount_mol": 0.00375,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 360
    },
    {
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.00075
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 295
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 285
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 300
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
  "end_step": 366,
  "lifecycle_index": 24,
  "metrics": {
    "byproduct_signal": 0.1993360072374344,
    "conversion": 0.9998398423194885,
    "cost": 1.0,
    "crystal_csd_quality": 0.21265549957752228,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 1.0,
    "crystal_size": 0.02400132827460766,
    "crystal_yield": 0.0,
    "degradation_warning": 0.10856223106384277,
    "safety_risk": 0.04899671673774719,
    "score": 0.2741650938987732,
    "selectivity": 0.7666634917259216,
    "virtual_spectrum_summary": 0.15848781168460846,
    "yield": 0.7750695943832397
  },
  "ordinal": 24
}
```

## K1

```json
{
  "payload": {
    "report": "## Mechanistic account\n\n### 1. Main observations\n\nThe campaign revealed a strong, unresolved conflict between crystal recovery and particle-number quality. Concentrated batches readily recovered target product, but nearly all particles were counted below 20 \u00b5m. Dilute batches could produce a coarse, low-fines population, but little seed-excluded product crystallized.\n\nThe clearest comparison used solvent S0 and catalyst C0:\n\n- **Batch 1:** 0.040 mol reagent, 0.080 L S0, 0.005 mol C0; reaction at 360 K for 3600 s; 0.020 g seed; cooling to 270 K. Reaction yield was 0.586 and crystal yield 0.458, with purity 0.978, but fines fraction was 0.997.\n- **Batch 18:** reagent reduced to 0.010 mol, followed by staged cooling through 295, 285 and 270 K. Reaction yield rose to 0.773 and selectivity to 0.760; crystal yield remained substantial at 0.386. Purity was 0.984, but fines remained excessive at 0.917.\n- **Batch 19 (recommended):** 0.002 mol reagent, 0.080 L S0, 0.001 mol C0, 0.0002 g seed, and the same staged cooling/holding scheme. It gave purity 0.986 and final-assay fines 0.000, independently supported by the particle measurement of 0.0158. However, seed-excluded crystal yield was only 0.00389.\n- **Batch 21:** at the intermediate 0.0075 mol loading, crystal yield recovered to 0.286, but fines returned to 1.000.\n\nThus, batch 19 is not a high-throughput solution; it is the highest-recovery completed batch that actually met both specified quality constraints.\n\n### 2. Material effects\n\n**Observed solvent effect.** Under the common high-loading protocol used in batches 5\u201316, S0 was generally superior to the other solvents for reaction selectivity and crystallization recovery. The S1 series (batches 5\u20138) gave crystal yields of about 0.404\u20130.458; S2 (batches 9\u201312) gave 0.347\u20130.410; and S3 (batches 13\u201316) gave 0.323\u20130.380. Representative reaction selectivities were about 0.58\u20130.61 for the early S0 runs, versus roughly 0.45\u20130.53 for S1 and 0.42\u20130.47 for S2/S3.\n\n**Interpretation.** S0 appears to favor target formation and/or suppress competing-product formation. It may also provide a more favorable target solubility difference between the quenched and cold states. Because solvent identity is anonymous, this is an empirical benchmark-material effect rather than a claim about polarity, hydrogen bonding, or any real solvent property.\n\n**Observed catalyst effect.** Across S1\u2013S3, C2 was usually poorest: batches 7, 11 and 15 gave crystal yields 0.404, 0.347 and 0.323. C1 or C3 often gave higher recovery within the same solvent. Nevertheless, C0/S0 was the most developed combination and supported the best high-recovery results.\n\n**Uncertainty.** A complete C0\u2013C3 screen in S0 was not performed, so the superiority of C0 within S0 is not established. Catalyst amount was also reduced with reagent loading in later batches, meaning the concentration effect and catalyst-dose effect are partly confounded.\n\n### 3. Reaction\u2013crystallization coupling\n\nA useful approximate material-balance relation is\n\n`overall recovered target fraction \u2248 reaction yield \u00d7 crystal yield`,\n\nwhere crystal yield is specifically the seed-excluded recovery of target already present before separation.\n\nFor illustration, batch 1 gives approximately 0.586 \u00d7 0.458 \u2248 0.27 overall recovered target per reagent-yield basis, while batch 18 gives about 0.773 \u00d7 0.386 \u2248 0.30. Batch 19 gives only about 0.658 \u00d7 0.00389 \u2248 0.0026 despite its excellent particle quality. These products are approximate because the two reported yields have different formal stage definitions and independent measurement noise.\n\nReaction yield also approximately followed\n\n`reaction yield \u2248 conversion \u00d7 selectivity`.\n\nFor example, batch 19 had conversion 0.832 and selectivity 0.778, consistent with its measured reaction yield of 0.658. Batch 18 was essentially fully converted and had selectivity 0.760, consistent with its 0.773 yield within assay uncertainty.\n\nDilution improved reaction selectivity: it rose from roughly 0.59 in batch 1 to 0.760 in batch 18 and 0.778 in batch 19. A plausible interpretation is that lower instantaneous reactant/product concentration suppresses a bimolecular or concentration-sensitive byproduct pathway. This remains an interpretation because reaction order was not independently measured.\n\nThe same dilution also shifted crystallization behavior. At high loading, strong supersaturation apparently caused extensive primary or secondary nucleation, generating a large number of fines. At very low loading, the visible particle population was dominated by a small number of large seed-derived crystals, while almost no new target mass was recovered. This accounts qualitatively for batch 19\u2019s large normalized crystal size (0.380), excellent CSD quality (1.000), and near-zero fines together with negligible seed-excluded recovery.\n\n### 4. Process-history dependence\n\nSeveral history changes were tested rather than assuming that final temperature alone controlled the outcome:\n\n- Increasing seed from 0.020 g in batch 1 to 0.050 g with slow staged cooling in batch 2 did not improve fines: final fines remained 1.000 and crystal yield stayed near 0.457.\n- Removing seed in batch 3 also failed; crystal yield was 0.456 and fines 0.995.\n- A dissolution/recrystallization cycle in batch 4\u2014cooling to 270 K, reheating to 300 K, holding, and recooling\u2014gave crystal yield 0.471 but fines 1.000.\n- Batch 17 stopped at the milder 300 K endpoint and used ten long holds. Fines improved only to 0.972, while crystal yield fell to 0.357.\n- Batch 22 applied a thermal recycle to the 0.0075 mol formulation. Crystal yield remained 0.275, purity was 0.992, and fines were still 0.999.\n- Batch 23 stopped at 295 K after long holds. It produced coarse, low-fines particles but zero seed-excluded recovery, indicating that the solids were effectively seed dominated.\n- Batch 24 proceeded to 285 K but likewise reported zero seed-excluded yield and a fine particle population, suggesting entry into a nucleation regime without measurable recovered target beyond the seed basis.\n\nThese observations show hysteresis-like regime behavior: mild conditions preserve or enlarge seeds but do not precipitate appreciable product; stronger cooling produces product but triggers many new particles. Longer aging, more seed, no seed, and one thermal recycle did not bridge that gap.\n\n### 5. Apparent threshold and non-monotonic behavior\n\nThe loading series was not smoothly monotonic:\n\n- 0.002 mol, batch 19: crystal yield 0.00389, fines 0.000.\n- 0.005 mol, batch 20: crystal yield 0.00934, fines 1.000.\n- 0.0075 mol, batch 21: crystal yield 0.286, fines 1.000.\n- 0.010 mol, batch 18: crystal yield 0.386, fines 0.917.\n\nThis resembles a supersaturation/nucleation threshold rather than a gradual size response. Below the threshold, seed growth is limited by very little crystallizable excess. Above it, primary nucleation or seed-induced secondary nucleation rapidly raises particle number. The abruptness could also reflect nonlinear benchmark rules, so a literal classical-nucleation model should not be overclaimed.\n\nA conceptual relationship useful for interpreting the data is\n\n`supersaturation ratio S = C/C*`,\n\nwith growth becoming possible for `S > 1` and nucleation rate increasing steeply with supersaturation. A classical qualitative form is\n\n`J \u221d exp[-B/(ln S)^2]`,\n\nwhich explains why small concentration or temperature changes can cause an abrupt transition from almost no new particles to an abundance of fines. The experiments support the qualitative steep-threshold idea, but they do not identify B, solubility C*, or an actual nucleation law.\n\n### 6. Measurement uncertainty and revisions\n\nThe final assay uncertainties were approximately 0.010 for crystal yield and purity and 0.018 for fines and CSD quality. Particle-size measurements had approximately 0.015 uncertainty. Batch 19\u2019s measured recovery, 0.00389, is therefore not clearly distinguishable from zero on a one-standard-deviation basis. Its quality conclusion is much stronger: both the in-process particle result (fines 0.0158) and final assay (clipped at 0.000) are far below the 0.50 limit, while purity 0.986 is far above 0.80.\n\nThe particle-size and final-assay channels sometimes differed numerically, but usually agreed on the regime. For example, batch 18 gave fines 0.897 by particle measurement and 0.917 by final assay; batch 22 gave 1.000 and 0.999. Direct fines measurements were treated as authoritative rather than inferring fines from the separately noisy normalized size channel.\n\nThe working strategy was revised in stages: initial high-loading recovery optimization; slower and staged cooling; seed-dose and no-seed comparisons; solvent/catalyst screening; thermal cycling; and finally concentration reduction. Early revisions improved neither fines nor recovery materially. Concentration reduction was the only intervention that crossed the fines constraint, but it exposed the severe recovery penalty.\n\n### 7. Untested alternatives\n\nSeveral explanations and remedies remain untested:\n\n1. A much finer concentration search between 0.002 and 0.005 mol might locate a narrow window with nonzero recovery and fines below 0.50.\n2. Continuous, feedback-controlled cooling could hold supersaturation in a metastable growth zone more effectively than the discrete temperature steps tested.\n3. Seeding at a different temperature, using a narrower seed-size distribution, or delaying seed addition until a calibrated supersaturation was reached might reduce secondary nucleation.\n4. Alternative C catalysts in S0 could improve reaction selectivity or change the impurity profile enough to affect nucleation.\n5. Catalyst loading, reagent concentration, temperature, and reaction time should be varied independently; the late experiments scaled catalyst with reagent and therefore do not isolate their effects.\n6. Selective removal of fines, classified filtration, or crystal washing could potentially satisfy final product specifications, but those operations were unavailable and were not demonstrated.\n\n### 8. Unresolved tradeoff\n\nThe central unresolved tradeoff is robust: batches with useful crystal recovery\u2014approximately 0.28\u20130.47\u2014failed the fines limit badly, whereas the clearly conforming batch 19 had recovery near zero. Purity was generally not limiting; most crystallized products were around 0.95\u20131.00 purity. The campaign therefore identified purity control and material selection reasonably well, but did not discover a process that simultaneously delivers substantial seed-excluded recovery and an acceptable number fraction of fines."
  },
  "failure": null,
  "elapsed_s": 85.15700000000652,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 865536,
    "input_tokens": 988150,
    "output_tokens": 11512,
    "reasoning_output_tokens": 3854
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
          "estimate": 0.28,
          "lower80": 0.1,
          "upper80": 0.52
        },
        "crystal_purity": {
          "estimate": 0.97,
          "lower80": 0.9,
          "upper80": 0.999
        },
        "crystal_size": {
          "estimate": 0.25,
          "lower80": 0.13,
          "upper80": 0.39
        },
        "crystal_yield": {
          "estimate": 0.32,
          "lower80": 0.19,
          "upper80": 0.44
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q01"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.22,
          "lower80": 0.07,
          "upper80": 0.47
        },
        "crystal_purity": {
          "estimate": 0.95,
          "lower80": 0.86,
          "upper80": 0.995
        },
        "crystal_size": {
          "estimate": 0.28,
          "lower80": 0.15,
          "upper80": 0.43
        },
        "crystal_yield": {
          "estimate": 0.26,
          "lower80": 0.13,
          "upper80": 0.39
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q02"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.58,
          "lower80": 0.32,
          "upper80": 0.82
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.92,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.14,
          "lower80": 0.06,
          "upper80": 0.27
        },
        "crystal_yield": {
          "estimate": 0.31,
          "lower80": 0.17,
          "upper80": 0.44
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q03"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.24,
          "lower80": 0.08,
          "upper80": 0.48
        },
        "crystal_purity": {
          "estimate": 0.985,
          "lower80": 0.94,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.26,
          "lower80": 0.14,
          "upper80": 0.4
        },
        "crystal_yield": {
          "estimate": 0.36,
          "lower80": 0.23,
          "upper80": 0.47
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q04"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.2,
          "lower80": 0.06,
          "upper80": 0.43
        },
        "crystal_purity": {
          "estimate": 0.986,
          "lower80": 0.94,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.29,
          "lower80": 0.16,
          "upper80": 0.44
        },
        "crystal_yield": {
          "estimate": 0.37,
          "lower80": 0.24,
          "upper80": 0.48
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q05"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.78,
          "lower80": 0.55,
          "upper80": 0.96
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.92,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.08,
          "lower80": 0.025,
          "upper80": 0.18
        },
        "crystal_yield": {
          "estimate": 0.41,
          "lower80": 0.28,
          "upper80": 0.52
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q06"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.15,
          "lower80": 0.035,
          "upper80": 0.36
        },
        "crystal_purity": {
          "estimate": 0.987,
          "lower80": 0.945,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.32,
          "lower80": 0.19,
          "upper80": 0.48
        },
        "crystal_yield": {
          "estimate": 0.38,
          "lower80": 0.25,
          "upper80": 0.49
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q07"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.67,
          "lower80": 0.39,
          "upper80": 0.9
        },
        "crystal_purity": {
          "estimate": 0.991,
          "lower80": 0.95,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.12,
          "lower80": 0.045,
          "upper80": 0.25
        },
        "crystal_yield": {
          "estimate": 0.3,
          "lower80": 0.16,
          "upper80": 0.44
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q08"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.03,
          "lower80": 0.0,
          "upper80": 0.14
        },
        "crystal_purity": {
          "estimate": 0.995,
          "lower80": 0.96,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.38,
          "lower80": 0.23,
          "upper80": 0.55
        },
        "crystal_yield": {
          "estimate": 0.004,
          "lower80": 0.0,
          "upper80": 0.025
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q09"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.07,
          "lower80": 0.0,
          "upper80": 0.23
        },
        "crystal_purity": {
          "estimate": 0.992,
          "lower80": 0.95,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.4,
          "lower80": 0.24,
          "upper80": 0.58
        },
        "crystal_yield": {
          "estimate": 0.055,
          "lower80": 0.012,
          "upper80": 0.13
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q10"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.17,
          "lower80": 0.045,
          "upper80": 0.39
        },
        "crystal_purity": {
          "estimate": 0.988,
          "lower80": 0.945,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.3,
          "lower80": 0.17,
          "upper80": 0.46
        },
        "crystal_yield": {
          "estimate": 0.37,
          "lower80": 0.24,
          "upper80": 0.49
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q11"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.82,
          "lower80": 0.58,
          "upper80": 0.98
        },
        "crystal_purity": {
          "estimate": 0.94,
          "lower80": 0.84,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.075,
          "lower80": 0.02,
          "upper80": 0.17
        },
        "crystal_yield": {
          "estimate": 0.46,
          "lower80": 0.33,
          "upper80": 0.57
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q12"
      }
    ],
    "rationale": "All recipes add seed, so particles are expected even where seed-excluded recovery is nearly zero. Q01/Q02 isolate solvent: prior batches showed S1 giving more recovery than S3, while the lower target inventory expected with S3 should modestly reduce nucleation and fines. Q03/Q04 isolate seed loading: the larger seed charge provides much more growth area and is predicted to suppress secondary nucleation; the low-seed case is consequently near or above the fines limit. Q05/Q06 compare slow cooling with an initial crash: the slow ramp should favor growth, whereas the rapid 300-to-278 K drop should create persistent fines despite long aging and slightly higher recovery. Q07/Q08 compare continued cold aging with a 315 K thermal excursion and rapid recooling; campaign thermal cycling did not remove fines, so the excursion is predicted to dissolve some product and regenerate fines during recooling. Q09/Q10 compare immediate filtration with a two-hour hold at 292 K: both are seed-dominated and coarse, but the hold permits a small amount of seed-excluded growth. Q11/Q12 isolate reagent loading: doubling the charge should raise recovery but cross into the high-supersaturation, fines-rich regime observed during the campaign. Purity is predicted to remain above 0.80 throughout; feasibility failures are driven by fines. Intervals are deliberately broad because the campaign did not test these exact low-volume, very slow ramps, and the observed transition between seed-dominated coarse particles and product-rich fines was sharp and non-monotonic."
  },
  "failure": null,
  "elapsed_s": 88.40599999998813,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 865536,
    "input_tokens": 1059991,
    "output_tokens": 15500,
    "reasoning_output_tokens": 6103
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
    "report": "## 1. Status of the main claims\n\n### Supported by direct observations\n\n- **A severe recovery\u2013fines tradeoff was observed.** High-recovery batches such as 1, 2, 4, 18, 21 and 22 delivered seed-excluded crystal yields of roughly 0.28\u20130.47 but fines fractions around 0.92\u20131.00. Batch 19 met both quality limits, with purity 0.986 and fines near zero, but its crystal yield was only 0.00389. This tradeoff is direct evidence, not merely mechanistic interpretation.\n- **Purity was generally not the active constraint.** Final crystal purities were normally about 0.95\u20131.00 across batches 1\u201324, including both high- and low-recovery regimes. Failures were overwhelmingly caused by fines.\n- **S1 outperformed S3 for recovery under the common screening protocol.** Batches 5\u20138 using S1 gave crystal yields of 0.404\u20130.458, whereas batches 13\u201316 using S3 gave 0.323\u20130.380. The associated reaction selectivities were also generally higher for S1. This comparison is reasonably direct because those batches shared the same broad protocol.\n- **C2 was usually unfavorable in the screened solvents.** Batches 7, 11 and 15 were the lowest or among the lowest-recovery members of their respective S1, S2 and S3 catalyst groups.\n- **Dilution coincided with better reaction selectivity.** Selectivity increased from about 0.59 in batch 1 to 0.760 in batch 18 and 0.778 in batch 19. This is observationally supported, although causal attribution to concentration alone is weaker because catalyst dose and other details also changed.\n- **Simple history changes did not solve the fines problem at productive loading.** More seed in batch 2, no seed in batch 3, a 300 K recycle in batch 4, prolonged mild aging in batch 17, and another recycle in batch 22 all left fines close to one.\n\n### Contradicted or substantially weakened\n\n- **The intuitive claim that more seed necessarily suppresses fines was contradicted.** Increasing seed from 0.020 g in batch 1 to 0.050 g in batch 2 did not improve fines; both were essentially all fines. Removing seed in batch 3 also failed, showing that seed amount alone was not the governing variable in that regime.\n- **The expectation that a single dissolution\u2013recrystallization cycle would anneal the distribution was contradicted under the tested conditions.** Batches 4 and 22 retained fines near one after cycling.\n- **A smooth, monotonic concentration response was contradicted.** Batch 19 at 0.002 mol had almost no recovery and almost no fines; batch 20 at 0.005 mol still had very low recovery but fines of 1.00; batch 21 at 0.0075 mol abruptly reached 0.286 recovery while retaining fines of 1.00. The behavior was threshold-like and non-monotonic.\n- **Using reported crystal size alone as a surrogate for the fines constraint was weakened by internal tension in the observations.** For example, batch 14 reported normalized size 0.0996, corresponding nominally to about 24.9 \u00b5m, while reporting fines of 1.00. Batch 18 similarly reported size 0.108, nominally about 27.1 \u00b5m, with fines 0.917. Those channels cannot be treated as a perfectly coherent reconstructed number distribution.\n\n### Still interpretations or untested alternatives\n\n- The attribution of the sharp transition to classical supersaturation-dependent primary or secondary nucleation remains an interpretation. No solubility curve, metastable-zone width or nucleation rate was measured.\n- The proposed concentration-sensitive byproduct pathway is untested. Improved selectivity upon dilution could instead reflect catalyst loading, residence-time effects or another coupled variable.\n- S0 appeared strongest overall, but a complete C0\u2013C3 comparison in S0 under one common protocol was not performed.\n- Continuous supersaturation control, a characterized seed-size distribution, delayed seeding, fines classification and washing were not tested.\n- None of the campaign batches directly tested the held-out recipes\u2019 385 K reaction, 0.020 L solvent volume and extremely slow multi-day cooling ramps. Predictions for those conditions therefore remain extrapolations.\n\n## 2. One additional experiment\n\nI would repeat the batch-20 crystallization formulation while holding catalyst at the batch-19 absolute dose:\n\n- 0.005 mol reagent, 0.080 L S0 and 0.001 mol C0;\n- 360 K for 3600 s, then quench;\n- 0.0005 g seed;\n- staged 295, 285 and 270 K cooling, each for 14,400 s with matched 300 rpm holds;\n- HPLC immediately before crystallization, particle-size measurements after the 285 and 270 K stages, then filtration and final assay.\n\nThis changes only the major unresolved confounding direction: batch 20 used 0.005 mol reagent with 0.0025 mol catalyst, whereas batch 19 used 0.002 mol reagent with 0.001 mol catalyst.\n\nExpected discriminating outcomes:\n\n1. **Concentration/supersaturation threshold explanation:** If the new batch still develops fines near one despite the lower catalyst dose, while HPLC shows acceptable target formation, the batch-19/batch-20 transition is primarily caused by product concentration and nucleation. Intermediate particle measurements should show an abrupt rise in fines at one cooling stage.\n2. **Catalyst or impurity-mediated nucleation explanation:** If lowering catalyst produces a coarse, low-fines population resembling batch 19, the original batch-20 failure was substantially driven by catalyst-associated reaction composition or impurities rather than concentration alone. HPLC should show a corresponding change in byproduct signal or selectivity.\n3. **Smooth seed-growth explanation:** If recovery and particle number increase gradually across the two particle measurements while fines remain below 0.50, the apparent discontinuity was partly an artifact of sparse endpoint sampling rather than a genuinely sharp threshold.\n4. **Insufficient target formation:** If HPLC shows low conversion or little target, a low final recovery would not diagnose crystallization. That result would instead establish that the reduced catalyst dose made the upstream reaction limiting.\n\n## 3. Least effectively used observation and least reliable prediction\n\nThe account used the **discordance between crystal_size and crystal_fines_fraction** least effectively. Batches 14 and 18 are the clearest examples: their reported normalized sizes imply number-weighted medians near or above 20 \u00b5m, yet their reported fractions below 20 \u00b5m were almost one. I noted that the channels were separately noisy, but did not fully propagate this inconsistency into the mechanistic claims. It should have prompted still greater caution about interpreting either channel as a literal reconstructed particle-size distribution and broader uncertainty for predictions of fines from cooling history.\n\nAmong the sealed held-out predictions, **Q08 is least reliable**. It reheats an established crystal population to 315 K and then rapidly returns to 278.15 K. The campaign only tested lower-temperature recycle operations near 300 K in batches 4 and 22, and those occurred at different concentrations and histories. At 315 K, the solids might partially anneal, nearly completely dissolve, or expose a residual seed population; the subsequent rapid cooling could therefore improve the distribution, regenerate many fines, or substantially reduce recovered mass. These alternatives have opposite directional consequences, so Q08 requires the largest mechanistic extrapolation even though its sealed interval was broad."
  },
  "failure": null,
  "elapsed_s": 74.14100000000326,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 924928,
    "input_tokens": 1135740,
    "output_tokens": 18597,
    "reasoning_output_tokens": 7544
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
    "selected_experiment_index": 19,
    "selection_rationale": "Batch 19 was the highest-recovery completed batch satisfying both required quality constraints: crystal purity 0.986 and fines fraction 0.000, with seed-excluded crystal yield 0.0039. Higher-yield batches failed the fines limit."
  },
  "recommendation_recipe": {
    "actions": [
      {
        "amount_mol": 0.002,
        "operation": "add_reagent"
      },
      {
        "operation": "add_solvent",
        "solvent": 0,
        "volume_L": 0.08
      },
      {
        "catalyst": 0,
        "catalyst_amount_mol": 0.001,
        "operation": "add_catalyst"
      },
      {
        "duration_s": 3600,
        "operation": "heat",
        "stirring_speed_rpm": 600,
        "target_temperature_K": 360
      },
      {
        "operation": "quench"
      },
      {
        "operation": "seed_crystals",
        "seed_mass_g": 0.0002
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 295
      },
      {
        "duration_s": 14400,
        "operation": "wait",
        "stirring_speed_rpm": 300
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 285
      },
      {
        "duration_s": 14400,
        "operation": "wait",
        "stirring_speed_rpm": 300
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 270
      },
      {
        "duration_s": 14400,
        "operation": "wait",
        "stirring_speed_rpm": 300
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
    "lifecycle_index": 19,
    "source_attempts": 16
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
        "absolute_delta_error": 0.017123577190615302,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_purity",
        "predicted_delta": -0.020000000000000018,
        "resolved": false,
        "true_delta": -0.0028764228093847155
      },
      {
        "absolute_delta_error": 0.01099506371924372,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_size",
        "predicted_delta": 0.030000000000000027,
        "resolved": true,
        "true_delta": 0.019004936280756307
      },
      {
        "absolute_delta_error": 0.6476947480077399,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.060000000000000026,
        "resolved": true,
        "true_delta": -0.7076947480077399
      },
      {
        "absolute_delta_error": 0.0500877625740751,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_yield",
        "predicted_delta": 0.04999999999999999,
        "resolved": false,
        "true_delta": -8.776257407511201e-05
      },
      {
        "absolute_delta_error": 0.0035827358064735026,
        "direction_correct": true,
        "factor": "seed",
        "metric": "crystal_purity",
        "predicted_delta": 0.0050000000000000044,
        "resolved": false,
        "true_delta": 0.008582735806473507
      },
      {
        "absolute_delta_error": 0.11912512327580117,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_size",
        "predicted_delta": 0.12,
        "resolved": false,
        "true_delta": 0.0008748767241988226
      },
      {
        "absolute_delta_error": 0.3713792315776769,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.33999999999999997,
        "resolved": false,
        "true_delta": 0.031379231577676914
      },
      {
        "absolute_delta_error": 0.03964487319027177,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_yield",
        "predicted_delta": 0.03999999999999998,
        "resolved": false,
        "true_delta": 0.0003551268097282123
      },
      {
        "absolute_delta_error": 0.0017949232472147525,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.006000000000000005,
        "resolved": false,
        "true_delta": -0.004205076752785253
      },
      {
        "absolute_delta_error": 0.16345150632552563,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_size",
        "predicted_delta": -0.20999999999999996,
        "resolved": true,
        "true_delta": -0.046548493674474334
      },
      {
        "absolute_delta_error": 0.1602009392429924,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.5800000000000001,
        "resolved": true,
        "true_delta": 0.7402009392429925
      },
      {
        "absolute_delta_error": 0.12146629297589667,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_yield",
        "predicted_delta": -0.08000000000000002,
        "resolved": true,
        "true_delta": 0.04146629297589666
      },
      {
        "absolute_delta_error": 0.013830577525981602,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_purity",
        "predicted_delta": 0.0040000000000000036,
        "resolved": false,
        "true_delta": -0.009830577525981599
      },
      {
        "absolute_delta_error": 0.15936144002797398,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_size",
        "predicted_delta": -0.2,
        "resolved": true,
        "true_delta": -0.04063855997202603
      },
      {
        "absolute_delta_error": 0.24786521058039046,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.52,
        "resolved": true,
        "true_delta": 0.7678652105803905
      },
      {
        "absolute_delta_error": 0.07700038962529791,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_yield",
        "predicted_delta": 0.051000000000000004,
        "resolved": true,
        "true_delta": 0.12800038962529792
      },
      {
        "absolute_delta_error": 0.010282745362900192,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_purity",
        "predicted_delta": -0.0030000000000000027,
        "resolved": true,
        "true_delta": -0.013282745362900195
      },
      {
        "absolute_delta_error": 0.006534244532482615,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_size",
        "predicted_delta": 0.020000000000000018,
        "resolved": true,
        "true_delta": 0.013465755467517403
      },
      {
        "absolute_delta_error": 0.011157591658815885,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.04000000000000001,
        "resolved": false,
        "true_delta": 0.028842408341184123
      },
      {
        "absolute_delta_error": 0.05746325316856793,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_yield",
        "predicted_delta": 0.09000000000000002,
        "resolved": true,
        "true_delta": 0.032536746831432095
      },
      {
        "absolute_delta_error": 0.04219238285516569,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_purity",
        "predicted_delta": -0.04800000000000004,
        "resolved": false,
        "true_delta": -0.005807617144834354
      },
      {
        "absolute_delta_error": 0.19061171918850311,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_size",
        "predicted_delta": -0.22499999999999998,
        "resolved": true,
        "true_delta": -0.03438828081149688
      },
      {
        "absolute_delta_error": 0.09102589522834892,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.6499999999999999,
        "resolved": true,
        "true_delta": 0.7410258952283488
      }
    ],
    "failures": [],
    "metrics": {
      "crystal_fines_fraction": {
        "coverage80": 0.4166666666666667,
        "interval_score80": 2.2829883197083416,
        "interval_width": 0.37083333333333335,
        "mae": 0.3319746516528496,
        "n": 12,
        "planned": 12
      },
      "crystal_purity": {
        "coverage80": 1.0,
        "interval_score80": 0.07616666666666669,
        "interval_width": 0.07616666666666669,
        "mae": 0.010937463966099589,
        "n": 12,
        "planned": 12
      },
      "crystal_size": {
        "coverage80": 0.3333333333333333,
        "interval_score80": 0.9387174575400804,
        "interval_width": 0.25333333333333335,
        "mae": 0.17244648882280852,
        "n": 12,
        "planned": 12
      },
      "crystal_yield": {
        "coverage80": 0.75,
        "interval_score80": 0.25410134350631153,
        "interval_width": 0.22108333333333333,
        "mae": 0.06985820868607119,
        "n": 12,
        "planned": 12
      }
    },
    "quality": {
      "balanced_accuracy": 0.6666666666666667,
      "false_negative": 1,
      "false_positive": 3,
      "true_negative": 3,
      "true_positive": 5
    },
    "resolved_direction_correct": 11,
    "resolved_direction_n": 14,
    "tie_correct": 4,
    "tie_n": 10,
    "valid": true
  },
  "public_baselines": {
    "available": true,
    "mae": {
      "public_mean": {
        "crystal_fines_fraction": 0.3646230122888186,
        "crystal_purity": 0.005503742389969572,
        "crystal_size": 0.020490958555484978,
        "crystal_yield": 0.08347675804649589
      },
      "public_nearest_neighbor": {
        "crystal_fines_fraction": 0.44846956466039983,
        "crystal_purity": 0.011287853538970272,
        "crystal_size": 0.056181049287316875,
        "crystal_yield": 0.04116952566339927
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
        "cached_input": 865536,
        "input": 928632,
        "output": 7725,
        "stage": "source",
        "uncached_input": 63096
      },
      {
        "cached_input": 0,
        "input": 59518,
        "output": 3787,
        "stage": "K1",
        "uncached_input": 59518
      },
      {
        "cached_input": 0,
        "input": 71841,
        "output": 3988,
        "stage": "Q",
        "uncached_input": 71841
      },
      {
        "cached_input": 59392,
        "input": 75749,
        "output": 3097,
        "stage": "K2",
        "uncached_input": 16357
      }
    ],
    "total": {
      "cached_input": 924928,
      "input": 1135740,
      "input_plus_output": 1154337,
      "output": 18597,
      "uncached_input": 210812
    },
    "valid": true
  },
  "elapsed_s": 566.75
}
```
