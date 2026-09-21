# C-W05-B12-E-Aligned

Status: completed

## Batch 1

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
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
      "target_temperature_K": 280
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 200
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
  "end_step": 12,
  "lifecycle_index": 1,
  "metrics": {
    "byproduct_signal": 0.4009212255477905,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7203300595283508,
    "crystal_fines_fraction": 0.38386768102645874,
    "crystal_purity": 0.9851447939872742,
    "crystal_size": 0.07966085523366928,
    "crystal_yield": 0.34699690341949463,
    "degradation_warning": 0.18093393743038177,
    "safety_risk": 0.17092272639274597,
    "score": 0.45456019043922424,
    "selectivity": 0.4298115372657776,
    "virtual_spectrum_summary": 0.30192694067955017,
    "yield": 0.42764905095100403
  },
  "ordinal": 1
}
```

## Batch 2

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 340
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
    "byproduct_signal": 0.4457552433013916,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7251203060150146,
    "crystal_fines_fraction": 0.3756335973739624,
    "crystal_purity": 0.9817309379577637,
    "crystal_size": 0.11178108304738998,
    "crystal_yield": 0.30704450607299805,
    "degradation_warning": 0.2060827612876892,
    "safety_risk": 0.16213490068912506,
    "score": 0.4379936158657074,
    "selectivity": 0.37499478459358215,
    "virtual_spectrum_summary": 0.33790263533592224,
    "yield": 0.3635497987270355
  },
  "ordinal": 2
}
```

## Batch 3

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 2,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 360
    },
    {
      "instrument": "hplc",
      "operation": "measure"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.03
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 280
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 280
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
  "end_step": 34,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.3520383834838867,
    "conversion": 0.9983132481575012,
    "cost": 1.0,
    "crystal_csd_quality": 0.6895998120307922,
    "crystal_fines_fraction": 0.40261566638946533,
    "crystal_purity": 0.9886366724967957,
    "crystal_size": 0.07041870802640915,
    "crystal_yield": 0.31355249881744385,
    "degradation_warning": 0.1099310964345932,
    "safety_risk": 0.1661897748708725,
    "score": 0.4388101100921631,
    "selectivity": 0.4321843683719635,
    "virtual_spectrum_summary": 0.24309010803699493,
    "yield": 0.43129509687423706
  },
  "ordinal": 3
}
```

## Batch 4

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
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
      "target_temperature_K": 280
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
  "end_step": 45,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.4386594891548157,
    "conversion": 0.9889965057373047,
    "cost": 1.0,
    "crystal_csd_quality": 0.7258447408676147,
    "crystal_fines_fraction": 0.3509121835231781,
    "crystal_purity": 1.0,
    "crystal_size": 0.08517390489578247,
    "crystal_yield": 0.3774482309818268,
    "degradation_warning": 0.24866686761379242,
    "safety_risk": 0.1735076904296875,
    "score": 0.470997154712677,
    "selectivity": 0.4446026682853699,
    "virtual_spectrum_summary": 0.35316282510757446,
    "yield": 0.43097299337387085
  },
  "ordinal": 4
}
```

## Batch 5

```json
{
  "actions": [
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
      "catalyst": 3,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 400,
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
      "target_temperature_K": 280
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
  "end_step": 56,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.3519231975078583,
    "conversion": 0.996337890625,
    "cost": 1.0,
    "crystal_csd_quality": 0.5309486389160156,
    "crystal_fines_fraction": 0.8187475800514221,
    "crystal_purity": 0.9781145453453064,
    "crystal_size": 0.044761963188648224,
    "crystal_yield": 0.44762465357780457,
    "degradation_warning": 0.1919184774160385,
    "safety_risk": 0.14251385629177094,
    "score": 0.42149773240089417,
    "selectivity": 0.5730414986610413,
    "virtual_spectrum_summary": 0.2799210846424103,
    "yield": 0.5668885707855225
  },
  "ordinal": 5
}
```

## Batch 6

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
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
      "target_temperature_K": 280
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
  "end_step": 67,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.38752245903015137,
    "conversion": 0.9924335479736328,
    "cost": 1.0,
    "crystal_csd_quality": 0.6814368367195129,
    "crystal_fines_fraction": 0.4214556813240051,
    "crystal_purity": 0.9986737966537476,
    "crystal_size": 0.05413229763507843,
    "crystal_yield": 0.4587174654006958,
    "degradation_warning": 0.2301633507013321,
    "safety_risk": 0.16498076915740967,
    "score": 0.4887000024318695,
    "selectivity": 0.5199764966964722,
    "virtual_spectrum_summary": 0.31671085953712463,
    "yield": 0.5218621492385864
  },
  "ordinal": 6
}
```

## Batch 7

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 3,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
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
      "target_temperature_K": 280
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
  "end_step": 78,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.4932200610637665,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.4956313967704773,
    "crystal_fines_fraction": 0.8506959080696106,
    "crystal_purity": 0.967123806476593,
    "crystal_size": 0.07615172117948532,
    "crystal_yield": 0.3130277991294861,
    "degradation_warning": 0.2949853241443634,
    "safety_risk": 0.1774330735206604,
    "score": 0.34064868092536926,
    "selectivity": 0.360286682844162,
    "virtual_spectrum_summary": 0.4040144085884094,
    "yield": 0.3869338929653168
  },
  "ordinal": 7
}
```

## Batch 8

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
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
      "target_temperature_K": 360
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
  "end_step": 88,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.3604957163333893,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7232673764228821,
    "crystal_fines_fraction": 0.39542046189308167,
    "crystal_purity": 0.9787067174911499,
    "crystal_size": 0.10976199805736542,
    "crystal_yield": 0.4915219843387604,
    "degradation_warning": 0.22046607732772827,
    "safety_risk": 0.16728027164936066,
    "score": 0.5126431584358215,
    "selectivity": 0.5436097979545593,
    "virtual_spectrum_summary": 0.29748237133026123,
    "yield": 0.5353045463562012
  },
  "ordinal": 8
}
```

## Batch 9

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
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
      "target_temperature_K": 360
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
  "end_step": 98,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.3632039725780487,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.6895332932472229,
    "crystal_fines_fraction": 0.4241998493671417,
    "crystal_purity": 0.9813565611839294,
    "crystal_size": 0.060646902769804,
    "crystal_yield": 0.49847468733787537,
    "degradation_warning": 0.20581094920635223,
    "safety_risk": 0.16900452971458435,
    "score": 0.5002945065498352,
    "selectivity": 0.5291011929512024,
    "virtual_spectrum_summary": 0.2923771142959595,
    "yield": 0.5427771210670471
  },
  "ordinal": 9
}
```

## Batch 10

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
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
      "target_temperature_K": 360
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.02
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
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
  "end_step": 108,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.3503577709197998,
    "conversion": 0.9858242273330688,
    "cost": 1.0,
    "crystal_csd_quality": 0.6416688561439514,
    "crystal_fines_fraction": 0.4566554129123688,
    "crystal_purity": 0.9775444865226746,
    "crystal_size": 0.07218696177005768,
    "crystal_yield": 0.5117358565330505,
    "degradation_warning": 0.21196134388446808,
    "safety_risk": 0.17030340433120728,
    "score": 0.4932169020175934,
    "selectivity": 0.5454380512237549,
    "virtual_spectrum_summary": 0.2880793809890747,
    "yield": 0.5543648600578308
  },
  "ordinal": 10
}
```

## Batch 11

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
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
  "end_step": 118,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.3588723838329315,
    "conversion": 0.9990203976631165,
    "cost": 1.0,
    "crystal_csd_quality": 0.6519112586975098,
    "crystal_fines_fraction": 0.44294843077659607,
    "crystal_purity": 0.9928745031356812,
    "crystal_size": 0.07757896929979324,
    "crystal_yield": 0.5026983022689819,
    "degradation_warning": 0.18898136913776398,
    "safety_risk": 0.17070603370666504,
    "score": 0.5002820491790771,
    "selectivity": 0.5750247240066528,
    "virtual_spectrum_summary": 0.28242143988609314,
    "yield": 0.5555348992347717
  },
  "ordinal": 11
}
```

## Batch 12

```json
{
  "actions": [
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
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
      "target_temperature_K": 280
    },
    {
      "instrument": "particle_size",
      "operation": "measure"
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
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 200
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
  "end_step": 133,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.3420012593269348,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7190079689025879,
    "crystal_fines_fraction": 0.36228910088539124,
    "crystal_purity": 0.9937862157821655,
    "crystal_size": 0.10398828238248825,
    "crystal_yield": 0.5043915510177612,
    "degradation_warning": 0.21024160087108612,
    "safety_risk": 0.17022235691547394,
    "score": 0.5216821432113647,
    "selectivity": 0.5406087636947632,
    "virtual_spectrum_summary": 0.28270941972732544,
    "yield": 0.5456507802009583
  },
  "ordinal": 12
}
```

## K1

```json
{
  "payload": {
    "report": "Mechanistic account\n\nThe campaign indicates that reaction selectivity, solvent-controlled supersaturation, and crystallization history jointly determine the isolated crystals. Crystal yield here is the seed-excluded crystallization recovery, R_c = n(target in recovered crystals)/n(target present before separation); it is not overall yield from charged reagent. A useful approximate overall isolated-target fraction is therefore Y_isolated \u2248 Y_reaction \u00d7 R_c. For recommended batch 10, this is approximately 0.554 \u00d7 0.512 \u2248 0.284 of the initial-reagent basis, subject to the benchmark\u2019s measurement definitions and noise.\n\nMaterial effects\n\nSolvent was the strongest observed crystallization factor. With catalyst C3 and otherwise similar 360 K reaction, seeding, cooling, aging, and filtration histories, S0 (batch 5) produced high recovery, 0.448, but an unacceptable fines fraction of 0.819. S1 (batch 6) improved recovery to 0.459 while giving 0.999 purity and acceptable fines of 0.421. S2 (batch 4) gave lower recovery, 0.377, but excellent purity and fewer fines, 0.351. S3 (batch 7) was poor on both recovery, 0.313, and fines, 0.851. Thus recovery did not follow nominal solubility alone. My interpretation is that each solvent changed reaction performance as well as product solubility, nucleation, growth, and impurity occlusion. S0 generated substantial target but excessive primary/secondary nucleation; S1 provided the best balance of target inventory, growth, and nucleation control. S2 favored clean, comparatively coarse crystallization but left more target unrecovered, while S3 combined weak reaction performance with an unfavorable particle population.\n\nA standard supersaturation description is useful: S = C/C*(T,solvent), with nucleation J \u2248 k_n(S\u22121)^m and growth G \u2248 k_g(S\u22121)^g. Solvent changes C*, k_n, k_g, and impurity incorporation. Seeded, gradual cooling should direct supersaturation toward growth rather than uncontrolled nucleation. The solvent results are consistent with this framework, but the individual kinetic constants were not measured.\n\nCatalyst C3 was retained after the early screen. The closest comparison was batch 1 versus batch 4: both used S2, 360 K for one hour, 0.02 g seed, cooling to 280 K, and an aging period. C3 in batch 4 gave recovery 0.377 and fines 0.351, versus 0.347 and 0.384 with C1 in batch 1. The final reaction yields were similar, about 0.431 versus 0.428, although degradation was higher with C3. C0 in batch 2 and C2 in batch 3 were less attractive, but those comparisons were confounded by different reaction temperatures, seed charges, and cooling histories. Therefore C3 is the best observed choice, not a cleanly isolated catalyst optimum.\n\nReaction\u2013crystallization coupling\n\nConversion was generally near unity, so product formation was governed mainly by selectivity and degradation rather than residual reactant. Final reaction selectivity varied substantially across solvent\u2013catalyst combinations: approximately 0.375 in batch 2, 0.573 in batch 5, 0.520 in batch 6, and 0.360 in batch 7. Nevertheless, crystal purity remained 0.967\u20131.000. This shows that crystallization was highly selective and rejected much of the reaction byproduct even when liquid-phase selectivity was only moderate.\n\nThe reaction was not quenched before crystallization. Consequently, catalyst-mediated reaction or degradation could continue during cooling and aging, and HPLC immediately after heating was not always identical to the final assay. For example, batch 4 had post-heating HPLC yield/selectivity of 0.477/0.465 but final values of 0.431/0.445. This may reflect continued chemistry, phase redistribution, sampling differences, and instrument noise. A quenched versus unquenched comparison was not performed, so continued reaction during crystallization remains an interpretation rather than a proven mechanism.\n\nProcess-history dependence and revisions\n\nThe initial strategy favored S2 because its nominal dossier suggested low solubility, strong growth, and low impurity occlusion. Batches 1\u20134 screened catalysts and cooling/seed histories in S2. After C3 performed best in the closest comparison, batches 5\u20137 screened solvents. S1 emerged as the best feasible solvent and was then optimized in batches 8\u201312 by lowering the crystallization endpoint and changing seed/cooling history.\n\nWith S1/C3, 0.02 g seed, four-hour cooling, and four-hour aging, reducing the endpoint from 280 K to 270, 260, and 250 K increased observed recovery from 0.459 in batch 6 to 0.492, 0.498, and 0.512 in batches 8, 9, and 10. At the same time, fines moved from 0.395 at 270 K to 0.424 at 260 K and 0.457 at 250 K. This is the central recovery\u2013quality tradeoff: deeper cooling increased thermodynamic recovery but also increased nucleation and approached the fines limit.\n\nIncreasing seed from 0.02 g in batch 10 to 0.05 g in batch 11 reduced the recovery point estimate from 0.512 to 0.503, while improving purity from 0.978 to 0.993 and fines from 0.457 to 0.443. These differences are modest relative to assay uncertainty, but they are consistent with additional seed surface moderating supersaturation and fines at a small apparent recovery cost.\n\nBatch 12 used staged cooling, first to 280 K and then to 250 K, followed by aging. Its in-process particle measurements showed fines decreasing from 0.406 after the first cooling stage to 0.362 after the second and 0.352 after aging, while normalized crystal size increased from 0.060 to 0.073 and then 0.116. The final assay gave recovery 0.504, purity 0.994, fines 0.362, and size 0.104. Thus staged cooling and aging produced a much more robust particle-quality margin than direct cooling in batch 10, but did not exceed batch 10\u2019s recovery point estimate.\n\nRecommendation and uncertainty\n\nThe sealed recommendation remains batch 10 because it had the highest observed feasible seed-excluded recovery: 0.512, with purity 0.978 and fines 0.457. Purity is comfortably above 0.80, but the fines margin is only 0.043. Final-assay standard deviations were approximately 0.010 for crystal yield, 0.010 for purity, 0.018 for fines, and 0.025 for normalized size. The 0.007 recovery difference between batches 10 and 12 is therefore not statistically resolved by single measurements. Batch 12 may be the more robust quality process, whereas batch 10 remains the correct choice under the stated objective of maximizing the observed recovery subject to the measured constraints.\n\nImportant untested alternatives include replicated batches 10 and 12; a quenched reaction before crystallization; finer multistage or continuous cooling ramps; lower stirring during supersaturation generation; seed-size and seed-timing studies; filtration at controlled low temperature; and a fully matched catalyst/temperature/duration factorial. These could determine whether batch 10\u2019s recovery advantage is reproducible and whether staged cooling can retain its lower fines while matching or exceeding the recovery of direct 250 K cooling."
  },
  "failure": null,
  "elapsed_s": 61.905999999988126,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 855680,
    "input_tokens": 965104,
    "output_tokens": 9413,
    "reasoning_output_tokens": 3471
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
          "lower80": 0.04,
          "upper80": 0.29
        },
        "crystal_purity": {
          "estimate": 0.985,
          "lower80": 0.94,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.23,
          "lower80": 0.12,
          "upper80": 0.36
        },
        "crystal_yield": {
          "estimate": 0.5,
          "lower80": 0.35,
          "upper80": 0.63
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q01"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.32,
          "lower80": 0.15,
          "upper80": 0.52
        },
        "crystal_purity": {
          "estimate": 0.97,
          "lower80": 0.9,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.18,
          "lower80": 0.08,
          "upper80": 0.31
        },
        "crystal_yield": {
          "estimate": 0.34,
          "lower80": 0.2,
          "upper80": 0.49
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q02"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.61,
          "lower80": 0.39,
          "upper80": 0.82
        },
        "crystal_purity": {
          "estimate": 0.96,
          "lower80": 0.87,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.1,
          "lower80": 0.03,
          "upper80": 0.22
        },
        "crystal_yield": {
          "estimate": 0.32,
          "lower80": 0.18,
          "upper80": 0.46
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q03"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.2,
          "lower80": 0.07,
          "upper80": 0.4
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.92,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.2,
          "lower80": 0.1,
          "upper80": 0.34
        },
        "crystal_yield": {
          "estimate": 0.34,
          "lower80": 0.22,
          "upper80": 0.47
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q04"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.18,
          "lower80": 0.06,
          "upper80": 0.36
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.92,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.22,
          "lower80": 0.11,
          "upper80": 0.36
        },
        "crystal_yield": {
          "estimate": 0.35,
          "lower80": 0.23,
          "upper80": 0.48
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q05"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.37,
          "lower80": 0.18,
          "upper80": 0.59
        },
        "crystal_purity": {
          "estimate": 0.97,
          "lower80": 0.9,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.14,
          "lower80": 0.05,
          "upper80": 0.27
        },
        "crystal_yield": {
          "estimate": 0.35,
          "lower80": 0.22,
          "upper80": 0.49
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q06"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.17,
          "lower80": 0.05,
          "upper80": 0.35
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.92,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.23,
          "lower80": 0.12,
          "upper80": 0.37
        },
        "crystal_yield": {
          "estimate": 0.36,
          "lower80": 0.24,
          "upper80": 0.49
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q07"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.12,
          "lower80": 0.03,
          "upper80": 0.3
        },
        "crystal_purity": {
          "estimate": 0.99,
          "lower80": 0.94,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.25,
          "lower80": 0.11,
          "upper80": 0.42
        },
        "crystal_yield": {
          "estimate": 0.25,
          "lower80": 0.1,
          "upper80": 0.4
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q08"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.3,
          "lower80": 0.1,
          "upper80": 0.58
        },
        "crystal_purity": {
          "estimate": 0.99,
          "lower80": 0.91,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.08,
          "lower80": 0.03,
          "upper80": 0.16
        },
        "crystal_yield": {
          "estimate": 0.015,
          "lower80": 0.0,
          "upper80": 0.05
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q09"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.27,
          "lower80": 0.09,
          "upper80": 0.52
        },
        "crystal_purity": {
          "estimate": 0.985,
          "lower80": 0.92,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.1,
          "lower80": 0.04,
          "upper80": 0.19
        },
        "crystal_yield": {
          "estimate": 0.08,
          "lower80": 0.02,
          "upper80": 0.17
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q10"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.19,
          "lower80": 0.06,
          "upper80": 0.38
        },
        "crystal_purity": {
          "estimate": 0.983,
          "lower80": 0.92,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.21,
          "lower80": 0.1,
          "upper80": 0.35
        },
        "crystal_yield": {
          "estimate": 0.35,
          "lower80": 0.23,
          "upper80": 0.48
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q11"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.35,
          "lower80": 0.17,
          "upper80": 0.56
        },
        "crystal_purity": {
          "estimate": 0.95,
          "lower80": 0.85,
          "upper80": 0.995
        },
        "crystal_size": {
          "estimate": 0.23,
          "lower80": 0.11,
          "upper80": 0.39
        },
        "crystal_yield": {
          "estimate": 0.6,
          "lower80": 0.44,
          "upper80": 0.73
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q12"
      }
    ],
    "rationale": "The six pairs isolate solvent (Q01\u2013Q02), seed loading (Q03\u2013Q04), gradual versus crash cooling (Q05\u2013Q06), low-temperature aging versus a heat\u2013recool cycle (Q07\u2013Q08), immediate filtration versus a 2 h hold (Q09\u2013Q10), and reagent concentration (Q11\u2013Q12). I expect S1 to give higher recovery and fewer fines than S3; heavy seeding to suppress primary nucleation relative to the very low-seed case; and gradual cooling to produce larger particles and fewer fines than a rapid initial temperature drop, with similar long-time recovery. The heat cycle should dissolve fines and improve size distribution and purity, but its short recooling period may not restore all dissolved product. At 292 K, seeds ensure particles are present, but immediate filtration should recover almost no seed-excluded product; the hold permits limited growth. Doubling reagent concentration should substantially increase supersaturation and recovery, while increasing impurity occlusion and secondary nucleation. Intervals are deliberately broad because these recipes use much lower catalyst concentration, smaller volume, quenching, and far longer cooling histories than the campaign; uncertainty is greatest for thermal cycling, near-zero recovery, and the concentration extrapolation."
  },
  "failure": null,
  "elapsed_s": 91.39100000000326,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 855680,
    "input_tokens": 1029098,
    "output_tokens": 14135,
    "reasoning_output_tokens": 6514
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
    "report": "1. Status of the main claims\n\nSupported by direct observations:\n- Solvent strongly affected recovery and particle quality. Under closely related C3 conditions, batch 5 (S0) gave crystal yield 0.448 but fines 0.819; batch 6 (S1) gave 0.459 yield with fines 0.421; batch 7 (S3) gave only 0.313 yield with fines 0.851. S1 therefore provided the best feasible balance in that comparison. The explanation in terms of solvent-dependent solubility, nucleation, growth, and occlusion remains an interpretation; those kinetic quantities were not measured separately.\n- Deeper direct cooling in S1 increased recovery while narrowing the fines margin. Batches 8, 9, and 10 ended at 270, 260, and 250 K and gave yields of 0.492, 0.498, and 0.512, while fines rose from 0.395 to 0.424 and 0.457. This directly supports a recovery\u2013quality tradeoff for that process family.\n- Staging and aging changed the particle distribution. In batch 12, particle measurements progressed from size/fines 0.060/0.406 after the 280 K stage to 0.073/0.362 after 250 K and 0.116/0.352 after aging. Its final assay, 0.104/0.362, confirmed a substantially better fines margin than batch 10, although recovery was slightly lower at 0.504 versus 0.512.\n- Crystallization was selective. Even when final reaction selectivity was only about 0.36\u20130.57, crystal purity was 0.967\u20131.000 across the solvent screen. That directly supports impurity rejection during crystallization.\n\nSupported only weakly or with confounding:\n- C3 appeared better than C1 in the closest comparison: batch 4 versus batch 1 gave recovery 0.377 versus 0.347 and fines 0.351 versus 0.384. However, single-batch noise and subtle history differences prevent a strong catalyst ranking. C0 and C2 were tested with different temperatures, seed loads, and cooling histories, so their apparent inferiority is not a clean catalyst effect.\n- Raising seed from 0.02 g in batch 10 to 0.05 g in batch 11 improved purity and fines but reduced the recovery estimate from 0.512 to 0.503. Those changes are comparable to assay uncertainty, so the proposed supersaturation-buffering effect of additional seed is plausible rather than established.\n\nContradicted or revised:\n- The initial expectation that S2\u2019s nominal low solubility, strong growth, and low occlusion would make it optimal was contradicted for the stated recovery objective. S2 produced clean particles in batch 4, but S1 subsequently delivered higher feasible recovery in batches 6 and 8\u201310.\n- A simple claim that lower temperature intrinsically creates more fines is incomplete. The matched endpoint series in batches 8\u201310 showed that trend, but the within-batch measurements in staged batch 12 showed fines falling as cooling and aging proceeded. Cooling rate and history therefore modify, and can overcome, the endpoint-temperature effect.\n- Solubility alone cannot explain the solvent ranking. S0 gave relatively high recovery in batch 5 despite its nominally higher solubility, while also giving extreme fines. Its stronger reaction yield and resulting target concentration probably contributed to supersaturation, but that causal link was not isolated.\n\nStill untested:\n- Continued reaction or degradation during crystallization remains unproven because no campaign batch included an otherwise matched quench/no-quench comparison.\n- The suggested nucleation and growth relationships, J\u2248k_n(S\u22121)^m and G\u2248k_g(S\u22121)^g, are organizing models rather than fitted laws.\n- Whether batch 10 truly has higher recovery than batch 12 is unresolved: their 0.007 difference is smaller than the approximate single-assay crystal-yield standard deviation of 0.010.\n- Effects of seed size distribution, filtration temperature, washing, continuous ramp shape, and matched catalyst-dose or reaction-time changes were not tested.\n\n2. One additional experiment\n\nI would repeat the batch-10 S1/C3 recipe with one deliberate change: take an HPLC measurement immediately after the 360 K reaction, then quench before seeding, cool directly to 250 K over four hours, age for four hours, filter, terminate, and perform the final assay. The reagent, solvent, catalyst, seed, stirring, cooling, aging, and filtration conditions would otherwise match batch 10.\n\nThis would distinguish two explanations for the differences between post-heating HPLC and final reaction metrics:\n- If catalyst-mediated reaction or degradation continued during the unquenched crystallization, the quenched experiment should preserve its post-reaction yield/selectivity. Its final byproduct and degradation signals should differ from batch 10, and altered target/impurity concentrations could change crystal recovery or purity.\n- If those discrepancies arose mainly from instrument noise, phase redistribution, or sampling, quenching should leave the final reaction and crystal outcomes close to batch 10 within uncertainty.\n\nA particularly informative outcome would be unchanged crystal recovery but improved purity after quenching, indicating that continued chemistry mainly generated impurities. Lower recovery after quenching would imply that useful product formation continued during batch 10\u2019s cooling/aging period. Higher recovery with lower degradation would instead indicate that the unquenched catalyst primarily destroyed target during that period.\n\n3. Least effectively used observation and least reliable prediction\n\nThe account used batch 5 least effectively. Its combination of the highest reaction yield in the solvent screen, about 0.567, relatively high crystal recovery, 0.448, and extremely poor fines, 0.819, contains evidence that reaction-generated target concentration and crystallization supersaturation were coupled. I mainly described it as an intrinsic S0 nucleation problem. A better treatment would have separated the solvent\u2019s direct nucleation tendency from its indirect effect through reaction yield and target concentration. The campaign did not provide the matched data needed to quantify those contributions.\n\nQ08 is the least reliable held-out prediction. It reheats an established crystal population to 315 K and then allows only one hour of recooling. No campaign batch tested partial dissolution, seed survival, polymorph/history reset, or recrystallization after such a thermal cycle. Consequently, my sealed estimates for its surviving particles, recovery, size improvement, and reduced fines depend on an unverified assumption that heating preferentially dissolves fines without fully erasing the crystal population. Complete dissolution followed by insufficient renucleation, or rapid secondary nucleation during recooling, could produce qualitatively different outcomes."
  },
  "failure": null,
  "elapsed_s": 55.09299999999348,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 908032,
    "input_tokens": 1097734,
    "output_tokens": 16627,
    "reasoning_output_tokens": 7568
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
    "selection_rationale": "Batch 10 gave the highest observed seed-excluded crystal recovery (0.512) while meeting crystal purity (0.978 >= 0.80) and fines (0.457 <= 0.50) constraints."
  },
  "recommendation_recipe": {
    "actions": [
      {
        "operation": "add_solvent",
        "solvent": 1,
        "volume_L": 0.08
      },
      {
        "amount_mol": 0.04,
        "operation": "add_reagent"
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
        "target_temperature_K": 360
      },
      {
        "operation": "seed_crystals",
        "seed_mass_g": 0.02
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 250
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
    "excluded_rejected_attempts": [],
    "lifecycle_index": 10,
    "source_attempts": 10
  },
  "prediction_evaluation": {
    "contrasts": [
      {
        "absolute_delta_error": 0.04922312168225362,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_yield",
        "predicted_delta": -0.15999999999999998,
        "resolved": true,
        "true_delta": -0.2092231216822536
      },
      {
        "absolute_delta_error": 0.014852228504271037,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_purity",
        "predicted_delta": -0.015000000000000013,
        "resolved": false,
        "true_delta": -0.00014777149572897663
      },
      {
        "absolute_delta_error": 0.057117199183538456,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_size",
        "predicted_delta": -0.05000000000000002,
        "resolved": true,
        "true_delta": 0.007117199183538439
      },
      {
        "absolute_delta_error": 0.46661623193981455,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.19,
        "resolved": true,
        "true_delta": -0.27661623193981455
      },
      {
        "absolute_delta_error": 0.020132329809087884,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_yield",
        "predicted_delta": 0.020000000000000018,
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
        "absolute_delta_error": 0.10497943907987049,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_size",
        "predicted_delta": 0.1,
        "resolved": false,
        "true_delta": -0.004979439079870487
      },
      {
        "absolute_delta_error": 0.5434195253798535,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.41,
        "resolved": true,
        "true_delta": 0.13341952537985358
      },
      {
        "absolute_delta_error": 0.00043352086783046695,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_yield",
        "predicted_delta": 0.0,
        "resolved": false,
        "true_delta": 0.00043352086783046695
      },
      {
        "absolute_delta_error": 0.006227866825037953,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.010000000000000009,
        "resolved": false,
        "true_delta": -0.0037721331749620557
      },
      {
        "absolute_delta_error": 0.036161131163011305,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_size",
        "predicted_delta": -0.07999999999999999,
        "resolved": true,
        "true_delta": -0.04383886883698868
      },
      {
        "absolute_delta_error": 0.42381528795023254,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.19,
        "resolved": true,
        "true_delta": 0.6138152879502325
      },
      {
        "absolute_delta_error": 0.15304184008830013,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_yield",
        "predicted_delta": -0.10999999999999999,
        "resolved": true,
        "true_delta": 0.04304184008830014
      },
      {
        "absolute_delta_error": 0.02037751463115034,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_purity",
        "predicted_delta": 0.010000000000000009,
        "resolved": true,
        "true_delta": -0.01037751463115033
      },
      {
        "absolute_delta_error": 0.05985535301730989,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_size",
        "predicted_delta": 0.01999999999999999,
        "resolved": true,
        "true_delta": -0.0398553530173099
      },
      {
        "absolute_delta_error": 0.6999421779987409,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.05000000000000002,
        "resolved": true,
        "true_delta": 0.6499421779987409
      },
      {
        "absolute_delta_error": 0.04114975880452933,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_yield",
        "predicted_delta": 0.065,
        "resolved": true,
        "true_delta": 0.10614975880452933
      },
      {
        "absolute_delta_error": 0.007280020877195814,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_purity",
        "predicted_delta": -0.0050000000000000044,
        "resolved": true,
        "true_delta": -0.012280020877195819
      },
      {
        "absolute_delta_error": 0.00727418830942541,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_size",
        "predicted_delta": 0.020000000000000004,
        "resolved": true,
        "true_delta": 0.012725811690574594
      },
      {
        "absolute_delta_error": 0.07253026625748243,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.02999999999999997,
        "resolved": false,
        "true_delta": 0.04253026625748246
      },
      {
        "absolute_delta_error": 0.23506595761778373,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_yield",
        "predicted_delta": 0.25,
        "resolved": false,
        "true_delta": 0.014934042382216267
      },
      {
        "absolute_delta_error": 0.027890313202054817,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_purity",
        "predicted_delta": -0.03300000000000003,
        "resolved": false,
        "true_delta": -0.005109686797945212
      },
      {
        "absolute_delta_error": 0.048338398389644856,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_size",
        "predicted_delta": 0.020000000000000018,
        "resolved": true,
        "true_delta": -0.028338398389644838
      },
      {
        "absolute_delta_error": 0.442412437007269,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.15999999999999998,
        "resolved": true,
        "true_delta": 0.602412437007269
      }
    ],
    "failures": [],
    "metrics": {
      "crystal_fines_fraction": {
        "coverage80": 0.0,
        "interval_score80": 3.2537350120091197,
        "interval_width": 0.3566666666666667,
        "mae": 0.49554016786757865,
        "n": 12,
        "planned": 12
      },
      "crystal_purity": {
        "coverage80": 1.0,
        "interval_score80": 0.09041666666666666,
        "interval_width": 0.09041666666666666,
        "mae": 0.011233569860902145,
        "n": 12,
        "planned": 12
      },
      "crystal_size": {
        "coverage80": 0.25,
        "interval_score80": 0.4518373969397358,
        "interval_width": 0.22833333333333336,
        "mae": 0.1142912110049877,
        "n": 12,
        "planned": 12
      },
      "crystal_yield": {
        "coverage80": 0.75,
        "interval_score80": 0.4492315348853848,
        "interval_width": 0.24250000000000002,
        "mae": 0.11527696677893468,
        "n": 12,
        "planned": 12
      }
    },
    "quality": {
      "balanced_accuracy": 0.4,
      "false_negative": 1,
      "false_positive": 7,
      "true_negative": 0,
      "true_positive": 4
    },
    "resolved_direction_correct": 6,
    "resolved_direction_n": 15,
    "tie_correct": 2,
    "tie_n": 9,
    "valid": true
  },
  "public_baselines": {
    "available": true,
    "mae": {
      "public_mean": {
        "crystal_fines_fraction": 0.3232997895729167,
        "crystal_purity": 0.004418502515471573,
        "crystal_size": 0.019529406063888675,
        "crystal_yield": 0.20599170582480753
      },
      "public_nearest_neighbor": {
        "crystal_fines_fraction": 0.34891695852815197,
        "crystal_purity": 0.0044654513267410045,
        "crystal_size": 0.021691227983485536,
        "crystal_yield": 0.14333529330280945
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
        "cached_input": 855680,
        "input": 912544,
        "output": 6515,
        "stage": "source",
        "uncached_input": 56864
      },
      {
        "cached_input": 0,
        "input": 52560,
        "output": 2898,
        "stage": "K1",
        "uncached_input": 52560
      },
      {
        "cached_input": 0,
        "input": 63994,
        "output": 4722,
        "stage": "Q",
        "uncached_input": 63994
      },
      {
        "cached_input": 52352,
        "input": 68636,
        "output": 2492,
        "stage": "K2",
        "uncached_input": 16284
      }
    ],
    "total": {
      "cached_input": 908032,
      "input": 1097734,
      "input_plus_output": 1114361,
      "output": 16627,
      "uncached_input": 189702
    },
    "valid": true
  },
  "elapsed_s": 452.1559999999881
}
```
