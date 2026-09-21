# C-W04-B24-E-MisIndexed

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
      "duration_s": 7200,
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
  "end_step": 13,
  "lifecycle_index": 1,
  "metrics": {
    "byproduct_signal": 0.37146347761154175,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.4894246757030487,
    "crystal_fines_fraction": 0.9971484541893005,
    "crystal_purity": 0.9875875115394592,
    "crystal_size": 0.06103474646806717,
    "crystal_yield": 0.38512375950813293,
    "degradation_warning": 0.18609242141246796,
    "safety_risk": 0.17414447665214539,
    "score": 0.3656010627746582,
    "selectivity": 0.4863113760948181,
    "virtual_spectrum_summary": 0.2880464792251587,
    "yield": 0.48414888978004456
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
      "operation": "quench"
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
      "target_temperature_K": 280
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
  "end_step": 26,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.3548147678375244,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5597193241119385,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9753855466842651,
    "crystal_size": 0.07338196784257889,
    "crystal_yield": 0.3394943177700043,
    "degradation_warning": 0.1142137423157692,
    "safety_risk": 0.1691054403781891,
    "score": 0.35823485255241394,
    "selectivity": 0.44534310698509216,
    "virtual_spectrum_summary": 0.24654430150985718,
    "yield": 0.4338979721069336
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
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 305
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
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
    "byproduct_signal": 0.3319219946861267,
    "conversion": 0.9979740977287292,
    "cost": 1.0,
    "crystal_csd_quality": 0.5349627733230591,
    "crystal_fines_fraction": 0.994916558265686,
    "crystal_purity": 0.9762024879455566,
    "crystal_size": 0.029490556567907333,
    "crystal_yield": 0.30433595180511475,
    "degradation_warning": 0.08708194643259048,
    "safety_risk": 0.16607765853405,
    "score": 0.3393551707267761,
    "selectivity": 0.4300830662250519,
    "virtual_spectrum_summary": 0.22174397110939026,
    "yield": 0.4290482699871063
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
      "stirring_speed_rpm": 400,
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
    "byproduct_signal": 0.3444027006626129,
    "conversion": 0.9889605641365051,
    "cost": 1.0,
    "crystal_csd_quality": 1.0,
    "crystal_fines_fraction": 0.015941284596920013,
    "crystal_purity": 1.0,
    "crystal_size": 0.3962223529815674,
    "crystal_yield": 0.0,
    "degradation_warning": 0.08794837445020676,
    "safety_risk": 0.14010073244571686,
    "score": 0.49877220392227173,
    "selectivity": 0.44790446758270264,
    "virtual_spectrum_summary": 0.22899825870990753,
    "yield": 0.4342588782310486
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
      "stirring_speed_rpm": 400,
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
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 305
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
  "end_step": 66,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.3162895441055298,
    "conversion": 0.9961230158805847,
    "cost": 1.0,
    "crystal_csd_quality": 1.0,
    "crystal_fines_fraction": 0.01108784880489111,
    "crystal_purity": 0.9900436997413635,
    "crystal_size": 0.3753965198993683,
    "crystal_yield": 0.0,
    "degradation_warning": 0.0725225955247879,
    "safety_risk": 0.14163130521774292,
    "score": 0.5080471634864807,
    "selectivity": 0.5111409425735474,
    "virtual_spectrum_summary": 0.20659440755844116,
    "yield": 0.5048811435699463
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
      "stirring_speed_rpm": 400,
      "target_temperature_K": 320
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
  "end_step": 79,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.3560710549354553,
    "conversion": 0.9924069046974182,
    "cost": 1.0,
    "crystal_csd_quality": 0.9850090742111206,
    "crystal_fines_fraction": 0.019179346039891243,
    "crystal_purity": 1.0,
    "crystal_size": 0.3705711364746094,
    "crystal_yield": 0.006071155890822411,
    "degradation_warning": 0.09323716908693314,
    "safety_risk": 0.13964854180812836,
    "score": 0.49230021238327026,
    "selectivity": 0.42573344707489014,
    "virtual_spectrum_summary": 0.23779581487178802,
    "yield": 0.42760753631591797
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
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 400,
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
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 296
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
  "end_step": 92,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.30378100275993347,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5091496706008911,
    "crystal_fines_fraction": 0.9867942333221436,
    "crystal_purity": 0.9795829057693481,
    "crystal_size": 0.05062216892838478,
    "crystal_yield": 0.3666521906852722,
    "degradation_warning": 0.07003060728311539,
    "safety_risk": 0.17161357402801514,
    "score": 0.36447882652282715,
    "selectivity": 0.4725054204463959,
    "virtual_spectrum_summary": 0.19859333336353302,
    "yield": 0.4990457594394684
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
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 400,
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
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 298.5
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
  "end_step": 105,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.2960909605026245,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 1.0,
    "crystal_fines_fraction": 0.0,
    "crystal_purity": 0.9924464821815491,
    "crystal_size": 0.425971657037735,
    "crystal_yield": 0.017021771520376205,
    "degradation_warning": 0.07659848779439926,
    "safety_risk": 0.14163130521774292,
    "score": 0.5173799991607666,
    "selectivity": 0.5036882758140564,
    "virtual_spectrum_summary": 0.19731934368610382,
    "yield": 0.49527615308761597
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
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 400,
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
      "target_temperature_K": 297.5
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
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.3072970509529114,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5170013308525085,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9819852113723755,
    "crystal_size": 0.017616141587495804,
    "crystal_yield": 0.3592778742313385,
    "degradation_warning": 0.06937672942876816,
    "safety_risk": 0.1713958978652954,
    "score": 0.36044636368751526,
    "selectivity": 0.48311546444892883,
    "virtual_spectrum_summary": 0.20023290812969208,
    "yield": 0.4966840147972107
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
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 400,
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
      "target_temperature_K": 298
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
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.30017417669296265,
    "conversion": 0.9856088161468506,
    "cost": 1.0,
    "crystal_csd_quality": 0.482563853263855,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9778113961219788,
    "crystal_size": 0.031493645161390305,
    "crystal_yield": 0.35893121361732483,
    "degradation_warning": 0.08078307658433914,
    "safety_risk": 0.1713017076253891,
    "score": 0.3551553189754486,
    "selectivity": 0.4941963851451874,
    "virtual_spectrum_summary": 0.20144817233085632,
    "yield": 0.5030158162117004
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
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 400,
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
      "target_temperature_K": 298.5
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
  "end_step": 146,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.308688759803772,
    "conversion": 0.9988049268722534,
    "cost": 1.0,
    "crystal_csd_quality": 0.9899483323097229,
    "crystal_fines_fraction": 0.0,
    "crystal_purity": 1.0,
    "crystal_size": 0.3956243097782135,
    "crystal_yield": 8.322816029249225e-06,
    "degradation_warning": 0.05780310556292534,
    "safety_risk": 0.14163069427013397,
    "score": 0.5095903277397156,
    "selectivity": 0.511293888092041,
    "virtual_spectrum_summary": 0.19579021632671356,
    "yield": 0.49169665575027466
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
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 400,
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
      "target_temperature_K": 296
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
      "target_temperature_K": 299
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
  "end_step": 160,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.29269030690193176,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.514087975025177,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9942454695701599,
    "crystal_size": 0.058261457830667496,
    "crystal_yield": 0.3503360152244568,
    "degradation_warning": 0.0795615166425705,
    "safety_risk": 0.17110709846019745,
    "score": 0.3645104169845581,
    "selectivity": 0.4907251298427582,
    "virtual_spectrum_summary": 0.19678235054016113,
    "yield": 0.495659738779068
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
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 400,
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
      "target_temperature_K": 296
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 600,
      "operation": "heat",
      "stirring_speed_rpm": 100,
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
  "end_step": 173,
  "lifecycle_index": 13,
  "metrics": {
    "byproduct_signal": 0.2962067425251007,
    "conversion": 0.9970015287399292,
    "cost": 1.0,
    "crystal_csd_quality": 0.5313003063201904,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9809433817863464,
    "crystal_size": 0.03523899242281914,
    "crystal_yield": 0.3205055594444275,
    "degradation_warning": 0.0711899921298027,
    "safety_risk": 0.16985349357128143,
    "score": 0.35637202858924866,
    "selectivity": 0.503886878490448,
    "virtual_spectrum_summary": 0.1949491947889328,
    "yield": 0.4957669675350189
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
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 400,
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
      "target_temperature_K": 296
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
  "end_step": 186,
  "lifecycle_index": 14,
  "metrics": {
    "byproduct_signal": 0.3105197846889496,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5354848504066467,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9643015265464783,
    "crystal_size": 0.07079091668128967,
    "crystal_yield": 0.32543450593948364,
    "degradation_warning": 0.07611561566591263,
    "safety_risk": 0.16985349357128143,
    "score": 0.3577333986759186,
    "selectivity": 0.4972858726978302,
    "virtual_spectrum_summary": 0.2050379067659378,
    "yield": 0.4909909963607788
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
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 400,
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
      "target_temperature_K": 310
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 305
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
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
      "target_temperature_K": 296
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
  "end_step": 204,
  "lifecycle_index": 15,
  "metrics": {
    "byproduct_signal": 0.3039262890815735,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.4976944029331207,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9873847365379333,
    "crystal_size": 0.048210207372903824,
    "crystal_yield": 0.34872376918792725,
    "degradation_warning": 0.06896313279867172,
    "safety_risk": 0.17167158424854279,
    "score": 0.35921069979667664,
    "selectivity": 0.495301216840744,
    "virtual_spectrum_summary": 0.19819286465644836,
    "yield": 0.49972835183143616
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
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 400,
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
      "target_temperature_K": 298.3
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
  "end_step": 217,
  "lifecycle_index": 16,
  "metrics": {
    "byproduct_signal": 0.2970051169395447,
    "conversion": 0.98833829164505,
    "cost": 1.0,
    "crystal_csd_quality": 0.9663634896278381,
    "crystal_fines_fraction": 0.0,
    "crystal_purity": 0.9899475574493408,
    "crystal_size": 0.4010998010635376,
    "crystal_yield": 0.0,
    "degradation_warning": 0.0802873820066452,
    "safety_risk": 0.14163069427013397,
    "score": 0.5018445253372192,
    "selectivity": 0.4924528896808624,
    "virtual_spectrum_summary": 0.19948214292526245,
    "yield": 0.4907000958919525
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
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 400,
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
      "target_temperature_K": 298.2
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
  "end_step": 230,
  "lifecycle_index": 17,
  "metrics": {
    "byproduct_signal": 0.31220611929893494,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.9974355101585388,
    "crystal_fines_fraction": 0.0,
    "crystal_purity": 1.0,
    "crystal_size": 0.3902590572834015,
    "crystal_yield": 0.005575196817517281,
    "degradation_warning": 0.07500606775283813,
    "safety_risk": 0.14163069427013397,
    "score": 0.511558473110199,
    "selectivity": 0.48931846022605896,
    "virtual_spectrum_summary": 0.20546609163284302,
    "yield": 0.499369353055954
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
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 400,
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
      "target_temperature_K": 298.1
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
  "end_step": 243,
  "lifecycle_index": 18,
  "metrics": {
    "byproduct_signal": 0.28584611415863037,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5257267951965332,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9944189786911011,
    "crystal_size": 0.08275173604488373,
    "crystal_yield": 0.3444027900695801,
    "degradation_warning": 0.0708606094121933,
    "safety_risk": 0.17128273844718933,
    "score": 0.3695972263813019,
    "selectivity": 0.4945862889289856,
    "virtual_spectrum_summary": 0.1891026347875595,
    "yield": 0.5078858733177185
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
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 400,
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
      "target_temperature_K": 298.15
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
  "end_step": 256,
  "lifecycle_index": 19,
  "metrics": {
    "byproduct_signal": 0.3066670000553131,
    "conversion": 0.990688145160675,
    "cost": 1.0,
    "crystal_csd_quality": 0.5216505527496338,
    "crystal_fines_fraction": 0.9774632453918457,
    "crystal_purity": 0.973137617111206,
    "crystal_size": 0.02108459547162056,
    "crystal_yield": 0.3533330261707306,
    "degradation_warning": 0.06556138396263123,
    "safety_risk": 0.17127323150634766,
    "score": 0.36128729581832886,
    "selectivity": 0.49406254291534424,
    "virtual_spectrum_summary": 0.19816948473453522,
    "yield": 0.4975419342517853
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
      "solvent": 3,
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
      "stirring_speed_rpm": 400,
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
      "target_temperature_K": 295
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
  "end_step": 269,
  "lifecycle_index": 20,
  "metrics": {
    "byproduct_signal": 0.3023028075695038,
    "conversion": 0.9928737878799438,
    "cost": 1.0,
    "crystal_csd_quality": 0.4943294823169708,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9788310527801514,
    "crystal_size": 0.04240924119949341,
    "crystal_yield": 0.3168651759624481,
    "degradation_warning": 0.07723534107208252,
    "safety_risk": 0.1817082166671753,
    "score": 0.3497798442840576,
    "selectivity": 0.5216198563575745,
    "virtual_spectrum_summary": 0.2010224461555481,
    "yield": 0.5049935579299927
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
      "solvent": 3,
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
      "stirring_speed_rpm": 400,
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
  "end_step": 282,
  "lifecycle_index": 21,
  "metrics": {
    "byproduct_signal": 0.2794063985347748,
    "conversion": 0.9888170957565308,
    "cost": 1.0,
    "crystal_csd_quality": 1.0,
    "crystal_fines_fraction": 0.010206208564341068,
    "crystal_purity": 1.0,
    "crystal_size": 0.37595558166503906,
    "crystal_yield": 0.007492193952202797,
    "degradation_warning": 0.07509174942970276,
    "safety_risk": 0.15472087264060974,
    "score": 0.5128332376480103,
    "selectivity": 0.5038042068481445,
    "virtual_spectrum_summary": 0.18746480345726013,
    "yield": 0.5227769613265991
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
      "solvent": 3,
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
      "stirring_speed_rpm": 400,
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
      "target_temperature_K": 298
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
  "end_step": 295,
  "lifecycle_index": 22,
  "metrics": {
    "byproduct_signal": 0.30494505167007446,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.4958867132663727,
    "crystal_fines_fraction": 0.998622715473175,
    "crystal_purity": 0.9883933663368225,
    "crystal_size": 0.040914639830589294,
    "crystal_yield": 0.304443359375,
    "degradation_warning": 0.07875296473503113,
    "safety_risk": 0.18077558279037476,
    "score": 0.34753236174583435,
    "selectivity": 0.5014025568962097,
    "virtual_spectrum_summary": 0.20315861701965332,
    "yield": 0.5023769736289978
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
      "solvent": 3,
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
      "stirring_speed_rpm": 400,
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
      "target_temperature_K": 299
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
  "end_step": 308,
  "lifecycle_index": 23,
  "metrics": {
    "byproduct_signal": 0.30247771739959717,
    "conversion": 0.9944304823875427,
    "cost": 1.0,
    "crystal_csd_quality": 1.0,
    "crystal_fines_fraction": 0.0,
    "crystal_purity": 1.0,
    "crystal_size": 0.41436320543289185,
    "crystal_yield": 0.0,
    "degradation_warning": 0.07192780077457428,
    "safety_risk": 0.15472087264060974,
    "score": 0.5165701508522034,
    "selectivity": 0.5187274813652039,
    "virtual_spectrum_summary": 0.1987302601337433,
    "yield": 0.5201812386512756
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
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 400,
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
      "target_temperature_K": 298.2
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
  "end_step": 364,
  "lifecycle_index": 24,
  "metrics": {
    "byproduct_signal": 0.304312139749527,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.9794595837593079,
    "crystal_fines_fraction": 0.03264205902814865,
    "crystal_purity": 1.0,
    "crystal_size": 0.3917100429534912,
    "crystal_yield": 0.0,
    "degradation_warning": 0.06687883287668228,
    "safety_risk": 0.14163069427013397,
    "score": 0.5046667456626892,
    "selectivity": 0.4964113235473633,
    "virtual_spectrum_summary": 0.1974671483039856,
    "yield": 0.5055537819862366
  },
  "ordinal": 24
}
```

## K1

```json
{
  "payload": {
    "report": "Mechanistic account\n\nRecommended process (unchanged): batch 8 used 0.040 mol reagent, 0.080 L solvent S2, and 0.005 mol catalyst C1; it was heated toward 330 K for 2,400 s at 400 rpm, quenched, seeded with 0.050 g, cooled to 298.5 K over 14,400 s, aged twice for 14,400 s at 100 rpm, filtered, and assayed. The observed seed-excluded crystal recovery was 0.0170, purity 0.992, fines number fraction 0.000, and normalized crystal size 0.426 (approximately 106 micrometres d50). It remains the selected batch because it had the highest observed recovery among batches satisfying purity >=0.80 and fines <=0.50.\n\nMaterial and reaction effects\n\nObservation: C1/S2 at about 330 K generally gave complete or nearly complete conversion and final reaction selectivity around 0.47\u20130.51. Batch 5, for example, gave conversion 0.996, selectivity 0.511 and degradation warning 0.073. In contrast, batch 1 used the same materials at 370 K and gave selectivity 0.486, byproduct signal 0.371 and degradation warning 0.186. The isolated C0, C2 and C3 tests were less selective: batch 2 (C0/S2, 350 K) gave selectivity 0.445; batch 3 (C2/S2, 340 K) gave 0.430; and batch 4 (C3/S2, 330 K) gave 0.448.\n\nInterpretation: C1 was the best-supported catalyst in the tested region, while excessive temperature promoted degradation and byproduct formation without improving conversion. A useful approximate decomposition is reaction yield \u2248 conversion \u00d7 selectivity, with additional loss represented by degradation/byproduct channels. Catalyst comparisons are not a clean factorial result because C0\u2013C3 were tested at different temperatures and mostly only once.\n\nS3 with C1 at 330 K produced reaction yields and selectivities comparable to, and sometimes slightly above, S2: batches 20, 21 and 23 had selectivities of 0.522, 0.504 and 0.519. Those differences overlap experimental and process variability, so superiority of S3 for reaction chemistry is not established. S0 and S1 were not tested and remain genuine alternatives.\n\nCrystallization mechanism and coupling\n\nThe principal coupling was that reaction conditions determined the amount and impurity composition of target entering crystallization, while solvent and thermal history controlled whether that target remained dissolved, grew on seed, or underwent a nucleation burst. Crystal purity was consistently high, usually 0.97\u20131.00, even when reaction selectivity was only about 0.5. This indicates strong phase selectivity: much of the byproduct stayed in the mother liquor rather than being incorporated into the recovered solid. Thus reaction selectivity and crystal purity were not interchangeable measures.\n\nThe results are consistent with supersaturation S=C/C*(T,solvent), growth G\u2248kg(S\u22121)^g, and a sharply nonlinear nucleation rate such as J\u2248kn exp[\u2212B/(ln S)^2]. Above the metastable boundary, little target crystallized and the measured particles were predominantly large seed crystals. Just below it, rapid secondary or homogeneous nucleation created many fine product crystals. Because fines are number-weighted, even a modest mass of newly nucleated particles can drive the fines fraction close to one.\n\nFor S2, the boundary was exceptionally sharp near 298.1\u2013298.3 K. Batch 16 at 298.3 K had zero observed recovery, fines 0.000 and normalized size 0.401. Batch 17 at 298.2 K had recovery 0.0056, fines 0.000 and size 0.390. Batch 19 at 298.15 K instead had recovery 0.353, fines 0.977 and size 0.021; batch 18 at 298.1 K similarly had recovery 0.344 and fines 1.000. Batch 8 at 298.5 K lay on the low-supersaturation side, retaining large particles and giving the highest observed qualifying recovery, 0.017.\n\nDeeper cooling increased recovery but violated the fines constraint. Batch 1, cooled to 270 K, recovered 0.385 but had fines 0.997. Batch 7 at 296 K recovered 0.367 with fines 0.987. Batches 9 and 10 at 297.5 and 298.0 K recovered about 0.359 but had fines essentially 1. This establishes the unresolved Pareto tradeoff: approximately 0.30\u20130.39 recovery was accessible only with overwhelming fines, whereas low-fines batches generally had recovery indistinguishable from zero to about 0.017.\n\nS3 showed the same qualitative transition at a different temperature. Batch 20 at 295 K recovered 0.317 with fines 1.000; batch 22 at 298 K recovered 0.304 with fines 0.999; batch 23 at 299 K had zero recovery and zero fines; and batch 21 at 300 K recovered 0.0075 with fines 0.010. The shift is consistent with solvent-dependent solubility and nucleation kinetics. The nominal material dossier predicted lower solubility, faster growth and lower nucleation/occlusion for S2 than S3; high purity agrees with low occlusion, but the hoped-for selective seeded growth was overwhelmed by a nucleation cliff.\n\nProcess-history dependence\n\nSlow or staged cooling did not eliminate the fines burst once the critical temperature was crossed. Batch 15 used successive long stages at 310, 305, 300 and 296 K, yet recovered 0.349 with fines 1.000. Batch 2 used staged cooling to 300 and then 280 K without seed and likewise recovered 0.339 with fines 1.000. This suggests final supersaturation dominated the tested cooling-rate effect.\n\nPost-nucleation heating also failed to selectively remove fines. Batch 12 crystallized at 296 K and was reheated to 299 K; it still gave recovery 0.350 and fines 1.000. Batches 13 and 14 reheated similar slurries toward 305 K for 600 and 3,600 s and retained recovery around 0.32 with fines 1.000. Either the reheating was insufficient for size-selective dissolution, or the benchmark dynamics did not provide appreciable Ostwald ripening on those timescales.\n\nLong aging on the non-nucleating side was also ineffective. Batch 24 was cooled to 298.2 K and held for 45 four-hour periods (180 h total aging), but final recovery remained zero while fines were 0.033. Batch 11 at 298.5 K with four aging periods likewise had essentially zero recovery. Therefore simply extending residence time did not convert the seed-only regime into useful seed-excluded recovery.\n\nRevisions and uncertainty\n\nThe initial strategy emphasized deep cooling for recovery; batches 1\u20133 showed useful recovery but unacceptable fines. The program then moved upward in temperature, locating a low-fines regime in batches 4\u20136, followed by a finer search around the S2 transition in batches 7\u201319. Reheating, staged cooling and prolonged aging were tested after the apparent tradeoff emerged, but none resolved it. S3 was then examined in batches 20\u201323 and showed the same basic discontinuity.\n\nFinal-assay standard deviations were approximately 0.010 for crystal yield and purity and 0.018 for fines. Consequently batch 8\u2019s recovery of 0.017 is only modestly above assay-scale uncertainty and was not robustly reproduced: batch 11 used the same nominal 298.5 K endpoint with longer aging and measured essentially zero recovery. In contrast, batch 8\u2019s purity and fines margins relative to the constraints were large. Near-boundary stochasticity, temperature sensitivity, and measurement noise therefore make the precise recovery ranking uncertain, although the separation between low-fines/low-recovery and high-recovery/high-fines regimes is clear.\n\nUntested alternatives include S0 and S1, a systematic catalyst-by-temperature factorial study, different seed size distributions or seed surface areas, antisolvent or concentration changes, controlled seed addition below the saturation temperature, wet milling/agglomeration control, and finer thermal cycling around the metastable boundary. These could potentially decouple growth from nucleation, but the present data do not establish that they would succeed. No tested process achieved the 0.10 initial recovery target while satisfying both quality constraints."
  },
  "failure": null,
  "elapsed_s": 69.93799999999464,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 1303808,
    "input_tokens": 1407497,
    "output_tokens": 14260,
    "reasoning_output_tokens": 4162
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
          "estimate": 0.64,
          "lower80": 0.42,
          "upper80": 0.84
        },
        "crystal_purity": {
          "estimate": 0.91,
          "lower80": 0.82,
          "upper80": 0.97
        },
        "crystal_size": {
          "estimate": 0.14,
          "lower80": 0.06,
          "upper80": 0.24
        },
        "crystal_yield": {
          "estimate": 0.27,
          "lower80": 0.15,
          "upper80": 0.39
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q01"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.36,
          "lower80": 0.18,
          "upper80": 0.56
        },
        "crystal_purity": {
          "estimate": 0.95,
          "lower80": 0.88,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.22,
          "lower80": 0.12,
          "upper80": 0.34
        },
        "crystal_yield": {
          "estimate": 0.35,
          "lower80": 0.23,
          "upper80": 0.47
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q02"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.91,
          "lower80": 0.72,
          "upper80": 1.0
        },
        "crystal_purity": {
          "estimate": 0.87,
          "lower80": 0.77,
          "upper80": 0.95
        },
        "crystal_size": {
          "estimate": 0.05,
          "lower80": 0.015,
          "upper80": 0.12
        },
        "crystal_yield": {
          "estimate": 0.2,
          "lower80": 0.08,
          "upper80": 0.34
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q03"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.58,
          "lower80": 0.34,
          "upper80": 0.8
        },
        "crystal_purity": {
          "estimate": 0.89,
          "lower80": 0.8,
          "upper80": 0.96
        },
        "crystal_size": {
          "estimate": 0.13,
          "lower80": 0.05,
          "upper80": 0.24
        },
        "crystal_yield": {
          "estimate": 0.24,
          "lower80": 0.12,
          "upper80": 0.37
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q04"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.46,
          "lower80": 0.24,
          "upper80": 0.68
        },
        "crystal_purity": {
          "estimate": 0.9,
          "lower80": 0.81,
          "upper80": 0.96
        },
        "crystal_size": {
          "estimate": 0.17,
          "lower80": 0.07,
          "upper80": 0.29
        },
        "crystal_yield": {
          "estimate": 0.25,
          "lower80": 0.13,
          "upper80": 0.38
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q05"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.93,
          "lower80": 0.76,
          "upper80": 1.0
        },
        "crystal_purity": {
          "estimate": 0.86,
          "lower80": 0.75,
          "upper80": 0.94
        },
        "crystal_size": {
          "estimate": 0.05,
          "lower80": 0.015,
          "upper80": 0.11
        },
        "crystal_yield": {
          "estimate": 0.29,
          "lower80": 0.17,
          "upper80": 0.42
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q06"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.41,
          "lower80": 0.2,
          "upper80": 0.64
        },
        "crystal_purity": {
          "estimate": 0.9,
          "lower80": 0.81,
          "upper80": 0.97
        },
        "crystal_size": {
          "estimate": 0.19,
          "lower80": 0.08,
          "upper80": 0.32
        },
        "crystal_yield": {
          "estimate": 0.26,
          "lower80": 0.14,
          "upper80": 0.39
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q07"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.79,
          "lower80": 0.55,
          "upper80": 0.96
        },
        "crystal_purity": {
          "estimate": 0.91,
          "lower80": 0.81,
          "upper80": 0.98
        },
        "crystal_size": {
          "estimate": 0.08,
          "lower80": 0.02,
          "upper80": 0.18
        },
        "crystal_yield": {
          "estimate": 0.18,
          "lower80": 0.06,
          "upper80": 0.32
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q08"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.04,
          "lower80": 0.0,
          "upper80": 0.15
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.91,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.38,
          "lower80": 0.26,
          "upper80": 0.5
        },
        "crystal_yield": {
          "estimate": 0.002,
          "lower80": 0.0,
          "upper80": 0.025
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q09"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.12,
          "lower80": 0.02,
          "upper80": 0.32
        },
        "crystal_purity": {
          "estimate": 0.97,
          "lower80": 0.88,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.34,
          "lower80": 0.2,
          "upper80": 0.48
        },
        "crystal_yield": {
          "estimate": 0.015,
          "lower80": 0.0,
          "upper80": 0.06
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q10"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.48,
          "lower80": 0.25,
          "upper80": 0.71
        },
        "crystal_purity": {
          "estimate": 0.89,
          "lower80": 0.79,
          "upper80": 0.96
        },
        "crystal_size": {
          "estimate": 0.17,
          "lower80": 0.07,
          "upper80": 0.29
        },
        "crystal_yield": {
          "estimate": 0.24,
          "lower80": 0.11,
          "upper80": 0.38
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q11"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.88,
          "lower80": 0.67,
          "upper80": 0.99
        },
        "crystal_purity": {
          "estimate": 0.83,
          "lower80": 0.7,
          "upper80": 0.92
        },
        "crystal_size": {
          "estimate": 0.06,
          "lower80": 0.02,
          "upper80": 0.14
        },
        "crystal_yield": {
          "estimate": 0.46,
          "lower80": 0.32,
          "upper80": 0.59
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q12"
      }
    ],
    "rationale": "All recipes contain seed, so particles are expected even where seed-excluded product recovery is nearly zero. Q01/Q02 compares solvents: S3's lower nominal solubility, nucleation tendency and impurity occlusion should give higher recovery, larger particles, fewer fines and higher purity than S1. Q03/Q04 compares seed loading in S0: the 0.001 g charge is unlikely to provide enough growth surface to suppress a nucleation burst, whereas 0.045 g should improve size and fines, though the predicted fines remain marginal. Q05/Q06 compares slow cooling with a rapid quench followed by an equal-duration cold hold: the rapid route should recover at least as much product but generate many more fines. Q07/Q08 tests a thermal excursion; prior campaign reheating did not reliably remove fines, and the rapid recool from 315 K is expected to sacrifice recovery and renucleate fines rather than produce robust ripening. Q09/Q10 compares immediate filtration with a two-hour hold at 292 K: both should be dominated by large seed particles, with the hold allowing only limited seed-excluded deposition. Q11/Q12 doubles reagent concentration: greater supersaturation should markedly increase recovery but also nucleation, impurity occlusion and fines. Uncertainty is wide because S0 and S1 were not tested in the campaign, these charges are more dilute than the campaign recipes, and the observed crystallization response had a sharp, history-sensitive nucleation boundary."
  },
  "failure": null,
  "elapsed_s": 109.82800000000861,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 1365632,
    "input_tokens": 1531701,
    "output_tokens": 19024,
    "reasoning_output_tokens": 7171
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
    "report": "1. Status of the main claims\n\nSupported by direct observations:\n- A sharp recovery\u2013fines transition existed for S2 near 298.1\u2013298.3 K. Batch 16 at 298.3 K produced zero measured seed-excluded recovery with fines 0.000, and batch 17 at 298.2 K produced only 0.0056 recovery with fines 0.000. In contrast, batches 18 and 19 at 298.1 and 298.15 K produced 0.344\u20130.353 recovery with fines 0.977\u20131.000. Interpreting this as a nucleation threshold is mechanistic inference, but the discontinuous outcome itself is directly observed.\n- High recovery and acceptable fines were unresolved competing objectives. Batches 1, 7, 9, 10, 12\u201315, 18 and 19 recovered roughly 0.32\u20130.39 but had fines near one. Low-fines batches 4\u20136, 8, 11, 16, 17, 21, 23 and 24 had only 0\u20130.017 recovery. This empirical separation is stronger than any particular nucleation equation used to explain it.\n- Slow staged cooling did not prevent fines after crossing the transition. Batch 15 used four long cooling stages and still gave 0.349 recovery with fines 1.000; batch 2 also used staged cooling and gave 0.339 recovery with fines 1.000.\n- Prolonged aging above the apparent nucleation boundary did not generate useful seed-excluded recovery. Batch 24 remained at 298.2 K for 180 h and finished with zero recovery and fines 0.033. Batch 11 at 298.5 K likewise remained effectively at zero recovery.\n- Reheating the fine slurry did not produce demonstrated fines removal. Batches 12\u201314 were first crystallized deeply and then reheated toward 299\u2013305 K; all retained about 0.32\u20130.35 recovery and fines near one.\n- Solvent S3 displayed a qualitatively similar transition at a shifted temperature. Batch 22 at 298 K gave 0.304 recovery and fines 0.999, whereas batch 23 at 299 K gave zero recovery and zero fines. This supports solvent-dependent placement of the boundary.\n\nSupported, but only weakly or with confounding:\n- C1 appeared preferable for reaction selectivity. C1/S2 batches near 330 K generally gave selectivity around 0.47\u20130.51, while the isolated C0, C2 and C3 cases gave about 0.43\u20130.45. However, those catalyst comparisons also changed temperature and lacked replication, so a catalyst effect is an interpretation rather than a clean direct comparison.\n- Higher reaction temperature appeared to increase degradation. Batch 1 at 370 K had degradation warning 0.186, compared with approximately 0.06\u20130.09 in many 320\u2013330 K batches. The direction is supported, but solvent, residence time and batch variation were not fully controlled.\n- Crystal purity was much higher than reaction selectivity. Most recovered solids assayed at roughly 0.97\u20131.00 purity even when reaction selectivity was near 0.5. Selective rejection of byproduct into the mother liquor is a plausible interpretation, but separate solid and mother-liquor compositions were not measured directly.\n\nContradicted or revised:\n- The initial expectation that S2\u2019s nominal low nucleation tendency and high growth tendency would enable substantial seed-driven recovery with few fines was contradicted over the tested conditions. Once appreciable recovery occurred, batches such as 7, 9, 10 and 15 nucleated overwhelming numbers of fines despite seeding and slow cooling.\n- A simple \u201cmore aging gives more recovery\u201d explanation was contradicted by batches 11 and 24.\n- Selective Ostwald ripening or fines dissolution during the tested reheating programs was not supported by batches 12\u201314. Stronger or differently timed cycling remains possible, but the tested version failed.\n- Batch 8\u2019s observed recovery advantage was not robustly replicated: it gave 0.017 recovery at 298.5 K, while batch 11 at the same nominal endpoint with longer aging gave essentially zero. That difference is comparable to final-assay yield uncertainty, so the exact ranking is less secure than the quality classification.\n\nStill untested:\n- S0 and S1 were never used in the campaign; all held-out claims for them rest on nominal material properties and extrapolation.\n- Catalyst identity was not studied in a temperature-controlled factorial design.\n- Seed number, size distribution and surface area were not varied independently of seed mass.\n- Antisolvent addition, wet milling, agglomeration control and feedback-controlled cooling were not tested.\n- The proposed mother-liquor rejection mechanism was not verified with phase-specific concentration measurements.\n- No experiment densely monitored dissolved target concentration and particle population while crossing the 298.1\u2013298.3 K boundary.\n\n2. One additional experiment\n\nI would perform a within-batch, instrumented threshold-crossing experiment using the established C1/S2 reaction conditions and 0.050 g seed. After quenching, I would hold at 298.3 K, collect repeated particle-size and liquid HPLC measurements, step to 298.2 K and repeat, then step to 298.15 K with more frequent measurements. After any fines appear, I would reheat slowly to approximately 300\u2013302 K while continuing both measurements, then complete filtration and final assay.\n\nThis single trajectory would distinguish three explanations:\n- Seed-limited growth: dissolved target should decline gradually, seed-excluded solid recovery should rise continuously, d50 should increase, and fines should remain below 0.5. A sufficiently long hold near 298.2 K would then be expected eventually to exceed about 0.1 recovery.\n- A kinetic nucleation threshold: little change should occur at 298.3\u2013298.2 K, followed by an abrupt decrease in dissolved target and simultaneous jump in fines near 298.15 K. Recovery would move rapidly toward roughly 0.3 while number-weighted size collapsed. This is the explanation most consistent with batches 16\u201319.\n- A smooth equilibrium-solubility boundary or measurement artifact: concentration and solid amount should change smoothly with temperature and substantially reverse during reheating. If particle readings mainly reflected seed rather than deposited target, particle size could remain large while HPLC and the final seed-excluded balance showed negligible deposition.\n\nReheating provides an additional discriminator. Reversible dissolution with preferential loss of small particles would lower fines and increase d50; persistence of fines, as in batches 12\u201314, would instead support kinetic trapping or insufficient size-selective dissolution.\n\n3. Underused observation and least reliable prediction\n\nThe prefiltration particle-size measurements were used least effectively. In several batches they already reproduced the later final-assay classification: batch 9 measured fines 1.000 before filtration and 1.000 finally, while batch 16 measured fines 0.0247 and normalized size 0.399 before filtration versus final values of 0.000 and 0.401. This agreement is important because it indicates that the sharp transition existed in the slurry before filtration and was not created by filtration or final-assay sampling. Using those paired observations explicitly would have strengthened the process-history argument and narrowed uncertainty about measurement artifacts.\n\nQ12 is the least reliable held-out prediction. It combines an untested solvent, S0, with a doubled reagent concentration relative to its paired case and asks for nonlinear consequences in recovery, impurity occlusion and nucleation. The campaign supplied no S0 observations and no controlled concentration series. Its predicted high recovery and high fines therefore depend on extrapolating the supersaturation model and nominal S0 properties beyond the evidence. Q08 is also highly uncertain because its 315 K thermal excursion is stronger than the unsuccessful 299\u2013305 K reheating tested in batches 12\u201314, so either dissolution/ripening or destructive renucleation could dominate."
  },
  "failure": null,
  "elapsed_s": 72.13999999998487,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 1415808,
    "input_tokens": 1598552,
    "output_tokens": 22059,
    "reasoning_output_tokens": 8483
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
    "selection_rationale": "Batch 8 had the highest observed crystal recovery among completed batches meeting both hard quality constraints (crystal purity 0.992 >= 0.80; fines fraction 0.000 <= 0.50). Its seed-excluded crystal yield was 0.0170. No tested batch achieved the initial 0.10 recovery target while also controlling fines."
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
        "duration_s": 2400,
        "operation": "heat",
        "stirring_speed_rpm": 400,
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
        "seed_mass_g": 0.05
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
    "excluded_rejected_attempts": [
      {
        "action": {
          "duration_s": 14400,
          "operation": "cool_crystallize",
          "target_temperature_K": 298.5
        },
        "status": "validation_failed",
        "step": 100
      }
    ],
    "lifecycle_index": 8,
    "source_attempts": 13
  },
  "prediction_evaluation": {
    "contrasts": [
      {
        "absolute_delta_error": 0.14571158490444175,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_yield",
        "predicted_delta": 0.07999999999999996,
        "resolved": true,
        "true_delta": -0.06571158490444179
      },
      {
        "absolute_delta_error": 0.04287642280938464,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_purity",
        "predicted_delta": 0.039999999999999925,
        "resolved": false,
        "true_delta": -0.0028764228093847155
      },
      {
        "absolute_delta_error": 0.06099506371924368,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_size",
        "predicted_delta": 0.07999999999999999,
        "resolved": true,
        "true_delta": 0.019004936280756307
      },
      {
        "absolute_delta_error": 0.4276947480077399,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.28,
        "resolved": true,
        "true_delta": -0.7076947480077399
      },
      {
        "absolute_delta_error": 0.04008776257407509,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_yield",
        "predicted_delta": 0.03999999999999998,
        "resolved": false,
        "true_delta": -8.776257407511201e-05
      },
      {
        "absolute_delta_error": 0.01141726419352651,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_purity",
        "predicted_delta": 0.020000000000000018,
        "resolved": false,
        "true_delta": 0.008582735806473507
      },
      {
        "absolute_delta_error": 0.07912512327580118,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_size",
        "predicted_delta": 0.08,
        "resolved": false,
        "true_delta": 0.0008748767241988226
      },
      {
        "absolute_delta_error": 0.361379231577677,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.33000000000000007,
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
        "absolute_delta_error": 0.03579492324721478,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.040000000000000036,
        "resolved": false,
        "true_delta": -0.004205076752785253
      },
      {
        "absolute_delta_error": 0.07345150632552568,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_size",
        "predicted_delta": -0.12000000000000001,
        "resolved": true,
        "true_delta": -0.046548493674474334
      },
      {
        "absolute_delta_error": 0.27020093924299243,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.47000000000000003,
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
        "absolute_delta_error": 0.019830577525981608,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_purity",
        "predicted_delta": 0.010000000000000009,
        "resolved": false,
        "true_delta": -0.009830577525981599
      },
      {
        "absolute_delta_error": 0.06936144002797398,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_size",
        "predicted_delta": -0.11,
        "resolved": true,
        "true_delta": -0.04063855997202603
      },
      {
        "absolute_delta_error": 0.3878652105803904,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.38000000000000006,
        "resolved": true,
        "true_delta": 0.7678652105803905
      },
      {
        "absolute_delta_error": 0.11500038962529792,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_yield",
        "predicted_delta": 0.013,
        "resolved": true,
        "true_delta": 0.12800038962529792
      },
      {
        "absolute_delta_error": 0.0032827453629001857,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_purity",
        "predicted_delta": -0.010000000000000009,
        "resolved": true,
        "true_delta": -0.013282745362900195
      },
      {
        "absolute_delta_error": 0.05346575546751738,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_size",
        "predicted_delta": -0.03999999999999998,
        "resolved": true,
        "true_delta": 0.013465755467517403
      },
      {
        "absolute_delta_error": 0.051157591658815865,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.07999999999999999,
        "resolved": false,
        "true_delta": 0.028842408341184123
      },
      {
        "absolute_delta_error": 0.18746325316856793,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_yield",
        "predicted_delta": 0.22000000000000003,
        "resolved": true,
        "true_delta": 0.032536746831432095
      },
      {
        "absolute_delta_error": 0.0541923828551657,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_purity",
        "predicted_delta": -0.06000000000000005,
        "resolved": false,
        "true_delta": -0.005807617144834354
      },
      {
        "absolute_delta_error": 0.07561171918850314,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_size",
        "predicted_delta": -0.11000000000000001,
        "resolved": true,
        "true_delta": -0.03438828081149688
      },
      {
        "absolute_delta_error": 0.3410258952283488,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.4,
        "resolved": true,
        "true_delta": 0.7410258952283488
      }
    ],
    "failures": [],
    "metrics": {
      "crystal_fines_fraction": {
        "coverage80": 0.4166666666666667,
        "interval_score80": 2.2039353618453186,
        "interval_width": 0.35833333333333334,
        "mae": 0.34795634562215194,
        "n": 12,
        "planned": 12
      },
      "crystal_purity": {
        "coverage80": 0.3333333333333333,
        "interval_score80": 0.3582241634947864,
        "interval_width": 0.1558333333333333,
        "mae": 0.08001327696848727,
        "n": 12,
        "planned": 12
      },
      "crystal_size": {
        "coverage80": 0.75,
        "interval_score80": 0.5374889625051077,
        "interval_width": 0.18916666666666668,
        "mae": 0.1025218247152857,
        "n": 12,
        "planned": 12
      },
      "crystal_yield": {
        "coverage80": 0.8333333333333334,
        "interval_score80": 0.2927552276356385,
        "interval_width": 0.21875,
        "mae": 0.060472482950404055,
        "n": 12,
        "planned": 12
      }
    },
    "quality": {
      "balanced_accuracy": 0.6666666666666666,
      "false_negative": 2,
      "false_positive": 2,
      "true_negative": 4,
      "true_positive": 4
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
        "crystal_fines_fraction": 0.3646230122888186,
        "crystal_purity": 0.005129864307951944,
        "crystal_size": 0.12288293373863961,
        "crystal_yield": 0.08873514541299243
      },
      "public_nearest_neighbor": {
        "crystal_fines_fraction": 0.3704345978742514,
        "crystal_purity": 0.005344228063511258,
        "crystal_size": 0.03642148573606854,
        "crystal_yield": 0.0869346268300036
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
        "cached_input": 1303808,
        "input": 1357145,
        "output": 11163,
        "stage": "source",
        "uncached_input": 53337
      },
      {
        "cached_input": 0,
        "input": 50352,
        "output": 3097,
        "stage": "K1",
        "uncached_input": 50352
      },
      {
        "cached_input": 61824,
        "input": 124204,
        "output": 4764,
        "stage": "Q",
        "uncached_input": 62380
      },
      {
        "cached_input": 50176,
        "input": 66851,
        "output": 3035,
        "stage": "K2",
        "uncached_input": 16675
      }
    ],
    "total": {
      "cached_input": 1415808,
      "input": 1598552,
      "input_plus_output": 1620611,
      "output": 22059,
      "uncached_input": 182744
    },
    "valid": true
  },
  "elapsed_s": 722.0620000000054
}
```
