# C-W02-B12-E-Opaque

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
      "stirring_speed_rpm": 500,
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
    "byproduct_signal": 0.22172580659389496,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.4999799132347107,
    "crystal_fines_fraction": 0.9972646832466125,
    "crystal_purity": 0.9798300862312317,
    "crystal_size": 0.054064154624938965,
    "crystal_yield": 0.5430036783218384,
    "degradation_warning": 0.08917980641126633,
    "safety_risk": 0.15448768436908722,
    "score": 0.4443061351776123,
    "selectivity": 0.6898179054260254,
    "virtual_spectrum_summary": 0.16208010911941528,
    "yield": 0.6876410841941833
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
      "target_temperature_K": 300
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
  "end_step": 25,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.2748641073703766,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5247033834457397,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9859204888343811,
    "crystal_size": 0.08165127784013748,
    "crystal_yield": 0.5016425251960754,
    "degradation_warning": 0.11304253339767456,
    "safety_risk": 0.1715254783630371,
    "score": 0.4283757209777832,
    "selectivity": 0.6257394552230835,
    "virtual_spectrum_summary": 0.20204439759254456,
    "yield": 0.6142944097518921
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 305
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
  "end_step": 40,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.366210013628006,
    "conversion": 0.9983178377151489,
    "cost": 1.0,
    "crystal_csd_quality": 0.49586740136146545,
    "crystal_fines_fraction": 0.9946938753128052,
    "crystal_purity": 0.984548807144165,
    "crystal_size": 0.048463013023138046,
    "crystal_yield": 0.3132544159889221,
    "degradation_warning": 0.10721562057733536,
    "safety_risk": 0.1644301861524582,
    "score": 0.33358269929885864,
    "selectivity": 0.4092736542224884,
    "virtual_spectrum_summary": 0.24966253340244293,
    "yield": 0.40838631987571716
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
      "stirring_speed_rpm": 500,
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
  "end_step": 53,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.38284769654273987,
    "conversion": 0.9889962077140808,
    "cost": 1.0,
    "crystal_csd_quality": 0.48903578519821167,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9972078204154968,
    "crystal_size": 0.0654030367732048,
    "crystal_yield": 0.30908408761024475,
    "degradation_warning": 0.13840962946414948,
    "safety_risk": 0.1759677678346634,
    "score": 0.33201277256011963,
    "selectivity": 0.4076242446899414,
    "virtual_spectrum_summary": 0.27285057306289673,
    "yield": 0.3939944803714752
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
      "volume_L": 0.06
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
      "target_temperature_K": 350
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
  "end_step": 74,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.3082895874977112,
    "conversion": 0.996337890625,
    "cost": 1.0,
    "crystal_csd_quality": 0.5169304013252258,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9733715057373047,
    "crystal_size": 0.02433392032980919,
    "crystal_yield": 0.4707477390766144,
    "degradation_warning": 0.1504136174917221,
    "safety_risk": 0.1511184722185135,
    "score": 0.41204598546028137,
    "selectivity": 0.622244656085968,
    "virtual_spectrum_summary": 0.23724539577960968,
    "yield": 0.6160916686058044
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 350
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
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.30473166704177856,
    "conversion": 0.9924325346946716,
    "cost": 1.0,
    "crystal_csd_quality": 0.9850090742111206,
    "crystal_fines_fraction": 0.019179346039891243,
    "crystal_purity": 1.0,
    "crystal_size": 0.3705711364746094,
    "crystal_yield": 0.006071155890822411,
    "degradation_warning": 0.14909665286540985,
    "safety_risk": 0.104550801217556,
    "score": 0.5280028581619263,
    "selectivity": 0.6044377684593201,
    "virtual_spectrum_summary": 0.2346959114074707,
    "yield": 0.6063227653503418
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 350
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
  "end_step": 102,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.2947482466697693,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.4693250060081482,
    "crystal_fines_fraction": 0.9867264032363892,
    "crystal_purity": 0.9648008942604065,
    "crystal_size": 0.06378219276666641,
    "crystal_yield": 0.3201926052570343,
    "degradation_warning": 0.1420687586069107,
    "safety_risk": 0.12888163328170776,
    "score": 0.3671911358833313,
    "selectivity": 0.5857946872711182,
    "virtual_spectrum_summary": 0.2260424792766571,
    "yield": 0.6124413013458252
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 350
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
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 303
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
  "end_step": 116,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.28705817461013794,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.500374972820282,
    "crystal_fines_fraction": 0.9868464469909668,
    "crystal_purity": 0.9651346802711487,
    "crystal_size": 0.07925891131162643,
    "crystal_yield": 0.3054938018321991,
    "degradation_warning": 0.14863663911819458,
    "safety_risk": 0.12737338244915009,
    "score": 0.3729008734226227,
    "selectivity": 0.6169775724411011,
    "virtual_spectrum_summary": 0.2247684895992279,
    "yield": 0.6086717247962952
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 350
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
      "target_temperature_K": 303.5
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
  "end_step": 129,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.29750776290893555,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 1.0,
    "crystal_fines_fraction": 0.0014134504599496722,
    "crystal_purity": 0.994659960269928,
    "crystal_size": 0.3764515519142151,
    "crystal_yield": 0.007928860373795033,
    "degradation_warning": 0.14124023914337158,
    "safety_risk": 0.104550801217556,
    "score": 0.532694935798645,
    "selectivity": 0.5952101945877075,
    "virtual_spectrum_summary": 0.227187380194664,
    "yield": 0.6088855266571045
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 350
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
      "target_temperature_K": 302.09590415089957
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
    "byproduct_signal": 0.29038485884666443,
    "conversion": 0.9858232140541077,
    "cost": 1.0,
    "crystal_csd_quality": 0.44170933961868286,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9630375504493713,
    "crystal_size": 0.04407206550240517,
    "crystal_yield": 0.3027123510837555,
    "degradation_warning": 0.15264658629894257,
    "safety_risk": 0.1278366595506668,
    "score": 0.3549858331680298,
    "selectivity": 0.6062911152839661,
    "virtual_spectrum_summary": 0.22840264439582825,
    "yield": 0.6152173280715942
  },
  "ordinal": 10
}
```

## Batch 11

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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 350
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
  "end_step": 155,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.2743247151374817,
    "conversion": 0.9990200996398926,
    "cost": 1.0,
    "crystal_csd_quality": 0.38619065284729004,
    "crystal_fines_fraction": 0.9928115010261536,
    "crystal_purity": 0.9881896376609802,
    "crystal_size": 0.04622126370668411,
    "crystal_yield": 0.21982814371585846,
    "degradation_warning": 0.16439466178417206,
    "safety_risk": 0.05761180818080902,
    "score": 0.37103360891342163,
    "selectivity": 0.8235788345336914,
    "virtual_spectrum_summary": 0.2248561978340149,
    "yield": 0.8040887713432312
  },
  "ordinal": 11
}
```

## K1

```json
{
  "payload": {
    "report": "Mechanistic account\n\nThe campaign revealed two coupled but partly separable problems: forming target product in solution and recovering it as acceptable crystals. I interpret reaction yield approximately as X\u00b7S, where X is conversion and S is selectivity, while crystallization recovery was measured independently as Yc = (seed-excluded target product recovered in solids)/(target product present before separation). Thus a batch could form substantial product yet recover only a small fraction as crystals.\n\nMaterial effects\n\nThe solvent/catalyst identities are anonymous, so only empirical combination effects can be claimed. Under broadly similar high-loading conditions, solvent-S0/catalyst-C0 was the strongest tested combination. Batch 1 gave reaction yield 0.688, selectivity 0.690 and crystal recovery 0.543. Batch 2 (S1/C1) gave 0.614, 0.626 and 0.502, respectively. Batches 3 and 4, involving S2/C2 and S3/C3, had substantially lower reaction yields (about 0.408 and 0.394) and crystal recoveries (about 0.313 and 0.309). These comparisons support choosing S0/C0, but catalyst and solvent were changed together and some crystallization histories also differed; separate catalyst and solvent effects therefore remain unresolved.\n\nLower reactant loading affected reaction chemistry but did not solve morphology. Batch 11 used 0.010 mol reagent rather than 0.040 mol and showed reaction yield 0.804 and selectivity 0.824, higher than the corresponding high-load S0/C0 runs. Its crystallization recovery was 0.220, purity 0.988, but fines remained 0.993. This is consistent with concentration-dependent side reactions or catalyst-to-substrate ratio effects, although neither interpretation was independently tested.\n\nReaction\u2013crystallization coupling\n\nThe solution product inventory entering crystallization can be represented schematically as nP,0 \u2248 nR,0XS. Cooling then establishes supersaturation, \u03c3 = C/C*(T) \u2212 1, or chemical driving force \u0394\u03bc = RT ln(C/C*). Classical qualitative relationships are useful: nucleation rises sharply as supersaturation increases, J \u221d exp[\u2212A/(ln(C/C*))\u00b2], whereas crystal growth is often approximated by G = kg(C \u2212 C*)^g. The observations suggest that accepted cooling crossed a narrow metastable-zone boundary, producing many new particles faster than existing seeds could consume solute.\n\nThis explains the central tradeoff. Strong cooling produced useful recovery but nearly all particles were fines by number. Batch 1, cooled to 270 K, achieved recovery 0.543 and purity 0.980, but fines were 0.997 and normalized size was 0.054 (roughly 14 \u00b5m d50). Batch 7, cooled to 300 K in the higher-solvent process, recovered 0.320 but had fines 0.987 and size about 16 \u00b5m. Batch 10 is especially diagnostic: cooling only 1 K below the post-quench temperature gave recovery 0.303, yet fines were 1.000 and d50 was roughly 11 \u00b5m.\n\nConversely, batches that remained near the post-quench temperature formed few but much larger crystals. Batch 9 underwent no accepted cooling because its requested 303.5 K target exceeded the actual post-quench temperature of about 303.10 K. After seeding and holding, it gave purity 0.9947, fines 0.0014, normalized size 0.376 (about 94 \u00b5m d50), and excellent CSD quality, but recovery was only 0.00793. Batch 6 followed a similar effectively uncooled history and gave recovery 0.00607, purity 1.000, fines 0.019, and about 93 \u00b5m d50. These outcomes imply growth on a small surviving crystal population under weak supersaturation, with most product remaining dissolved.\n\nProcess-history dependence\n\nThe response was not determined by final temperature alone. Seeding before cooling established an initial crystal population, but subsequent cooling apparently caused extensive primary or secondary nucleation. Once that fine population formed, later residence time did not repair it: Batch 5 received ten long low-agitation holds after cooling, yet fines remained 1.000 and size fell to about 6 \u00b5m while recovery was 0.471. Likewise, Batch 8 was cooled to 300 K and then reheated to 303 K; it still ended with fines 0.987 and recovery 0.305. The chosen reheating treatment therefore did not dissolve fines selectively or create effective Ostwald ripening. A no-seed staged-cooling route also failed: Batch 4 had fines reported as 1.000, showing that spontaneous nucleation was not preferable under those conditions.\n\nThe revisions consequently moved from aggressive cooling, to staged cooling and long aging, to increased solvent volume and near-isothermal seeded holding. Staging and aging did not control the number distribution. Higher solvent loading combined with no effective cooling did control morphology, but at the cost of leaving nearly all product in solution. A very small accepted cooling step then returned the system abruptly to the high-recovery/high-fines regime. This apparent threshold is the main process-history result.\n\nRecommendation and uncertainty\n\nBatch 9 remains the sealed recommendation because it clearly satisfied both formal quality constraints and had the highest observed qualifying recovery. Its purity and fines margins are much larger than the stated final-assay noise scales (approximately 0.01 for purity and 0.018 for fines). However, its recovery advantage over Batch 6 is much smaller than the recovery noise scale of about 0.01, so those two low-recovery outcomes are not meaningfully distinguishable statistically. More importantly, no batch combined the required morphology with the 0.10 recovery feasibility target. The campaign therefore established feasibility for crystal quality, not for quality-constrained recovery.\n\nObserved facts should be separated from interpretation: the sharp contrast between effectively uncooled batches 6/9 and cooled batches 7/10 is observed; attribution to a metastable-zone boundary and nucleation burst is mechanistic interpretation. Untested alternatives include sub-kelvin or continuous cooling control near that boundary, a different seed size distribution or larger effective seed surface, selective warm ripening before isolation, and a factorial study separating solvent from catalyst effects. Such strategies might occupy the unresolved middle ground between roughly 0.008 recovery with excellent morphology and roughly 0.30\u20130.54 recovery with unacceptable fines, but the present experiments do not demonstrate that this middle ground is attainable."
  },
  "failure": null,
  "elapsed_s": 60.875,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 866048,
    "input_tokens": 984487,
    "output_tokens": 9848,
    "reasoning_output_tokens": 4112
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
          "estimate": 0.2,
          "lower80": 0.08,
          "upper80": 0.4
        },
        "crystal_purity": {
          "estimate": 0.97,
          "lower80": 0.92,
          "upper80": 0.995
        },
        "crystal_size": {
          "estimate": 0.29,
          "lower80": 0.18,
          "upper80": 0.43
        },
        "crystal_yield": {
          "estimate": 0.74,
          "lower80": 0.58,
          "upper80": 0.86
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q01"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.31,
          "lower80": 0.13,
          "upper80": 0.55
        },
        "crystal_purity": {
          "estimate": 0.94,
          "lower80": 0.86,
          "upper80": 0.985
        },
        "crystal_size": {
          "estimate": 0.23,
          "lower80": 0.12,
          "upper80": 0.38
        },
        "crystal_yield": {
          "estimate": 0.6,
          "lower80": 0.4,
          "upper80": 0.77
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q02"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.58,
          "lower80": 0.32,
          "upper80": 0.81
        },
        "crystal_purity": {
          "estimate": 0.96,
          "lower80": 0.89,
          "upper80": 0.995
        },
        "crystal_size": {
          "estimate": 0.15,
          "lower80": 0.07,
          "upper80": 0.3
        },
        "crystal_yield": {
          "estimate": 0.76,
          "lower80": 0.59,
          "upper80": 0.88
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q03"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.17,
          "lower80": 0.06,
          "upper80": 0.36
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.93,
          "upper80": 0.998
        },
        "crystal_size": {
          "estimate": 0.31,
          "lower80": 0.2,
          "upper80": 0.46
        },
        "crystal_yield": {
          "estimate": 0.78,
          "lower80": 0.63,
          "upper80": 0.89
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q04"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.19,
          "lower80": 0.07,
          "upper80": 0.39
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.93,
          "upper80": 0.998
        },
        "crystal_size": {
          "estimate": 0.3,
          "lower80": 0.19,
          "upper80": 0.45
        },
        "crystal_yield": {
          "estimate": 0.78,
          "lower80": 0.63,
          "upper80": 0.89
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q05"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.88,
          "lower80": 0.68,
          "upper80": 0.98
        },
        "crystal_purity": {
          "estimate": 0.96,
          "lower80": 0.88,
          "upper80": 0.995
        },
        "crystal_size": {
          "estimate": 0.08,
          "lower80": 0.03,
          "upper80": 0.18
        },
        "crystal_yield": {
          "estimate": 0.8,
          "lower80": 0.65,
          "upper80": 0.91
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q06"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.22,
          "lower80": 0.08,
          "upper80": 0.43
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.93,
          "upper80": 0.998
        },
        "crystal_size": {
          "estimate": 0.28,
          "lower80": 0.17,
          "upper80": 0.43
        },
        "crystal_yield": {
          "estimate": 0.79,
          "lower80": 0.64,
          "upper80": 0.9
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q07"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.76,
          "lower80": 0.48,
          "upper80": 0.94
        },
        "crystal_purity": {
          "estimate": 0.97,
          "lower80": 0.9,
          "upper80": 0.997
        },
        "crystal_size": {
          "estimate": 0.12,
          "lower80": 0.05,
          "upper80": 0.27
        },
        "crystal_yield": {
          "estimate": 0.7,
          "lower80": 0.49,
          "upper80": 0.85
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q08"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.05,
          "lower80": 0.01,
          "upper80": 0.18
        },
        "crystal_purity": {
          "estimate": 0.99,
          "lower80": 0.94,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.37,
          "lower80": 0.25,
          "upper80": 0.52
        },
        "crystal_yield": {
          "estimate": 0.018,
          "lower80": 0.002,
          "upper80": 0.06
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q09"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.24,
          "lower80": 0.08,
          "upper80": 0.5
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.92,
          "upper80": 0.998
        },
        "crystal_size": {
          "estimate": 0.27,
          "lower80": 0.14,
          "upper80": 0.43
        },
        "crystal_yield": {
          "estimate": 0.16,
          "lower80": 0.07,
          "upper80": 0.3
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q10"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.18,
          "lower80": 0.06,
          "upper80": 0.37
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.93,
          "upper80": 0.998
        },
        "crystal_size": {
          "estimate": 0.31,
          "lower80": 0.2,
          "upper80": 0.46
        },
        "crystal_yield": {
          "estimate": 0.78,
          "lower80": 0.63,
          "upper80": 0.89
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q11"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.43,
          "lower80": 0.2,
          "upper80": 0.69
        },
        "crystal_purity": {
          "estimate": 0.95,
          "lower80": 0.86,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.19,
          "lower80": 0.09,
          "upper80": 0.34
        },
        "crystal_yield": {
          "estimate": 0.87,
          "lower80": 0.73,
          "upper80": 0.95
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q12"
      }
    ],
    "rationale": "Q01\u2013Q02 isolates solvent identity: I expect S1 to give better recovery and morphology than S3, but this extrapolation is uncertain because campaign solvent and catalyst effects were confounded. Q03\u2013Q04 isolates seed loading: 0.045 g provides much more growth surface and should suppress secondary nucleation relative to 0.001 g, with only a modest recovery change. Q05\u2013Q06 contrasts gradual and crash cooling at equal approximate residence time: both should approach high recovery, but the crash is expected to create predominantly fines. Q07\u2013Q08 compares continued cold aging with a 315 K reheat followed by rapid recooling; reheating may dissolve crystals, while the final rapid descent is expected to renucleate fines and reduce net recovery. Q09\u2013Q10 isolates a two-hour hold at 292 K: immediate filtration should recover almost no seed-excluded product, whereas the hold permits growth but may begin generating new particles. Q11\u2013Q12 doubles concentration: the higher charge should increase fractional recovery through greater supersaturation, while reducing size and increasing fines and impurity risk. Intervals are epistemic and intentionally broad because the campaign did not directly cover this dilute, very slow-ramp regime; morphology near the fines threshold is especially uncertain."
  },
  "failure": null,
  "elapsed_s": 50.73399999999674,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 866048,
    "input_tokens": 1067164,
    "output_tokens": 12268,
    "reasoning_output_tokens": 4848
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
    "report": "1. Status of the main claims\n\nSupported by direct observations:\n- A strong recovery\u2013morphology tradeoff was observed. Batches 1, 5, 7, 8 and 10 recovered about 0.30\u20130.54 of the available target product but had fines fractions near 0.99\u20131.00. By contrast, batches 6 and 9 had excellent morphology\u2014fines 0.019 and 0.0014, respectively, with normalized size about 0.37\u2014but only 0.006\u20130.008 recovery.\n- Once fines formed, simple aging did not repair them. Batch 5 received ten long low-agitation holds after cooling but still had fines of 1.00 and very small particles.\n- The tested mild reheating did not produce effective ripening. Batch 8 was reheated from 300 to 303 K, yet ended with fines near 0.987 and recovery near 0.305.\n- Seeding alone did not prevent nucleation during appreciable cooling. Several batches used 0.05 g seed but still produced almost exclusively fines. Conversely, seed-free staged cooling in batch 4 also produced fines near 1.00.\n- Lower reactant loading altered the reaction outcome but did not resolve crystal quality. Batch 11 showed higher reaction selectivity and yield than the high-load S0/C0 runs, while its fines remained about 0.993.\n\nInterpretations consistent with, but not proved by, those observations:\n- The sharp contrast between effectively uncooled batches 6/9 and cooled batches 7/10 is consistent with crossing a metastable-zone or nucleation threshold. It is not a direct measurement of supersaturation or nucleation rate.\n- The large particles in batches 6 and 9 were interpreted as growth on a small seed population under weak supersaturation. Their very low seed-excluded recovery also permits an alternative interpretation that the measured population remained predominantly seed material.\n- Concentration-dependent side reactions were proposed to explain batch 11\u2019s improved selectivity, but catalyst-to-substrate ratio and solvent-volume effects were not separated.\n\nContradicted or weakened:\n- A simple claim that staged or very slow cooling necessarily suppresses fines is contradicted by batches 2\u20134 and 7, which used staged histories but still produced nearly all fines.\n- A simple claim that more residence time causes useful coarsening is contradicted by batch 5.\n- A simple claim that a large seed charge guarantees acceptable morphology is contradicted by the cooled, heavily seeded batches.\n\nStill untested:\n- Independent solvent and catalyst effects; the material comparisons changed both together.\n- Sub-kelvin cooling increments around the apparent transition.\n- Seed size distribution and seed surface area independently of seed mass.\n- A sufficiently warm, long selective-dissolution/ripening treatment.\n- Direct concentration or supersaturation measurements during crystallization.\n\n2. One additional experiment\n\nI would repeat the S0/C0, 0.04 mol reagent, 0.10 L solvent, 0.05 g seed process used around batches 6\u201310, but after quenching I would cool in 0.25 K increments from approximately 303.1 K. Each increment would be followed by a fixed hold and a non-destructive particle-size measurement. Cooling would stop after the first substantial rise in fines or after enough cumulative cooling to establish whether recovery can exceed 0.10; the batch would then be filtered and finally assayed.\n\nThis single trajectory would distinguish three explanations:\n- Threshold nucleation: particle size and fines should remain seed-like through early steps, then fines should rise abruptly over one narrow temperature interval. Final recovery may improve, but likely only by violating the fines constraint.\n- Rate-controlled seeded growth: gradual cooling with holds should increase size and recovery progressively while fines remain below 0.50, potentially revealing the missing quality-feasible middle ground.\n- Predominantly seed-only particles: particle measurements would remain almost unchanged and the final seed-excluded recovery would stay very low despite modest cooling.\n\nThe experiment would not fully estimate equilibrium solubility, but it would directly test the most consequential process-history interpretation using morphology measurements along one controlled path.\n\n3. Least effectively used observation and least reliable prediction\n\nThe observation used least effectively was batch 11. It provided the clearest evidence that reaction selectivity changed at lower reagent loading, but the campaign altered concentration, effective catalyst ratio and available solvent conditions together. My account mentioned concentration-dependent side reactions without extracting or testing those competing explanations, and it did not integrate the improved reaction selectivity quantitatively with the poor crystallization outcome.\n\nThe least reliable held-out prediction is Q02. It predicts solvent-S3 with catalyst-C1, whereas the campaign\u2019s S3 evidence came from a batch using catalyst-C3 and a different crystallization history. Therefore the predicted S1-versus-S3 difference in Q01\u2013Q02 depends on extrapolating a solvent effect from a confounded solvent/catalyst comparison. Q08 is also highly uncertain because its 315 K reheat is much stronger than the tested 303 K reheating, but Q02 has the weakest direct material basis."
  },
  "failure": null,
  "elapsed_s": 49.312999999994645,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 866048,
    "input_tokens": 1152181,
    "output_tokens": 14141,
    "reasoning_output_tokens": 5613
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
    "selected_experiment_index": 9,
    "selection_rationale": "Best completed batch satisfying both quality constraints: crystal purity 0.9947 and fines fraction 0.0014; it also had the highest qualifying seed-excluded recovery observed (0.00793), although this remained below the 0.10 feasibility target."
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
        "duration_s": 7200,
        "operation": "heat",
        "stirring_speed_rpm": 300,
        "target_temperature_K": 350
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
    "excluded_rejected_attempts": [
      {
        "action": {
          "duration_s": 14400,
          "operation": "cool_crystallize",
          "target_temperature_K": 303.5
        },
        "status": "validation_failed",
        "step": 124
      }
    ],
    "lifecycle_index": 9,
    "source_attempts": 13
  },
  "prediction_evaluation": {
    "contrasts": [
      {
        "absolute_delta_error": 0.053117788811994665,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_yield",
        "predicted_delta": -0.14,
        "resolved": true,
        "true_delta": -0.19311778881199468
      },
      {
        "absolute_delta_error": 0.028552855963854484,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_purity",
        "predicted_delta": -0.030000000000000027,
        "resolved": false,
        "true_delta": -0.0014471440361455423
      },
      {
        "absolute_delta_error": 0.08902680472663704,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_size",
        "predicted_delta": -0.05999999999999997,
        "resolved": true,
        "true_delta": 0.02902680472663708
      },
      {
        "absolute_delta_error": 0.7002675737116523,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.10999999999999999,
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
        "absolute_delta_error": 0.011764438459750837,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_purity",
        "predicted_delta": 0.020000000000000018,
        "resolved": false,
        "true_delta": 0.008235561540249181
      },
      {
        "absolute_delta_error": 0.16022020934805375,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_size",
        "predicted_delta": 0.16,
        "resolved": false,
        "true_delta": -0.00022020934805375147
      },
      {
        "absolute_delta_error": 0.3893685499038364,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.4099999999999999,
        "resolved": false,
        "true_delta": -0.020631450096163517
      },
      {
        "absolute_delta_error": 0.019739549297168146,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_yield",
        "predicted_delta": 0.020000000000000018,
        "resolved": false,
        "true_delta": 0.00026045070283187144
      },
      {
        "absolute_delta_error": 0.0151321463408296,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.020000000000000018,
        "resolved": false,
        "true_delta": -0.004867853659170418
      },
      {
        "absolute_delta_error": 0.18237930183589546,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_size",
        "predicted_delta": -0.21999999999999997,
        "resolved": true,
        "true_delta": -0.03762069816410452
      },
      {
        "absolute_delta_error": 0.11189860171067934,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.69,
        "resolved": true,
        "true_delta": 0.5781013982893206
      },
      {
        "absolute_delta_error": 0.13006038328567332,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_yield",
        "predicted_delta": -0.09000000000000008,
        "resolved": true,
        "true_delta": 0.04006038328567324
      },
      {
        "absolute_delta_error": 0.0005313387149661342,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.010000000000000009,
        "resolved": false,
        "true_delta": -0.009468661285033875
      },
      {
        "absolute_delta_error": 0.1298970953524352,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_size",
        "predicted_delta": -0.16000000000000003,
        "resolved": true,
        "true_delta": -0.030102904647564807
      },
      {
        "absolute_delta_error": 0.06239412170088121,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.54,
        "resolved": true,
        "true_delta": 0.6023941217008812
      },
      {
        "absolute_delta_error": 0.011684422102466396,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_yield",
        "predicted_delta": 0.14200000000000002,
        "resolved": true,
        "true_delta": 0.1536844221024664
      },
      {
        "absolute_delta_error": 0.004527106938203129,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_purity",
        "predicted_delta": -0.010000000000000009,
        "resolved": true,
        "true_delta": -0.014527106938203138
      },
      {
        "absolute_delta_error": 0.11418252524890887,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_size",
        "predicted_delta": -0.09999999999999998,
        "resolved": true,
        "true_delta": 0.014182525248908888
      },
      {
        "absolute_delta_error": 0.17091092276400038,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.19,
        "resolved": false,
        "true_delta": 0.01908907723599962
      },
      {
        "absolute_delta_error": 0.06103124947311256,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_yield",
        "predicted_delta": 0.08999999999999997,
        "resolved": true,
        "true_delta": 0.02896875052688741
      },
      {
        "absolute_delta_error": 0.023942953078098794,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_purity",
        "predicted_delta": -0.030000000000000027,
        "resolved": false,
        "true_delta": -0.006057046921901232
      },
      {
        "absolute_delta_error": 0.09342635283571021,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_size",
        "predicted_delta": -0.12,
        "resolved": true,
        "true_delta": -0.026573647164289782
      },
      {
        "absolute_delta_error": 0.34090822043533586,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.25,
        "resolved": true,
        "true_delta": 0.5909082204353359
      }
    ],
    "failures": [],
    "metrics": {
      "crystal_fines_fraction": {
        "coverage80": 0.25,
        "interval_score80": 2.3979446181395208,
        "interval_width": 0.3625,
        "mae": 0.37833626018319877,
        "n": 12,
        "planned": 12
      },
      "crystal_purity": {
        "coverage80": 0.9166666666666666,
        "interval_score80": 0.0897408008822738,
        "interval_width": 0.0880833333333333,
        "mae": 0.01432323595905848,
        "n": 12,
        "planned": 12
      },
      "crystal_size": {
        "coverage80": 0.25,
        "interval_score80": 1.0270503715640833,
        "interval_width": 0.24666666666666667,
        "mae": 0.17666028660324115,
        "n": 12,
        "planned": 12
      },
      "crystal_yield": {
        "coverage80": 0.16666666666666666,
        "interval_score80": 2.698822705826075,
        "interval_width": 0.259,
        "mae": 0.3813063949211257,
        "n": 12,
        "planned": 12
      }
    },
    "quality": {
      "balanced_accuracy": 0.5833333333333334,
      "false_negative": 1,
      "false_positive": 4,
      "true_negative": 2,
      "true_positive": 5
    },
    "resolved_direction_correct": 10,
    "resolved_direction_n": 14,
    "tie_correct": 0,
    "tie_n": 10,
    "valid": true
  },
  "public_baselines": {
    "available": false,
    "failure": "Unknown transaction status at step 145: campaign_resource_rejected"
  },
  "tokens": {
    "basis": "cumulative thread snapshots differenced in source/K1/Q/K2 order",
    "complete": true,
    "monetary_cost_usd": null,
    "stages": [
      {
        "cached_input": 866048,
        "input": 925325,
        "output": 7413,
        "stage": "source",
        "uncached_input": 59277
      },
      {
        "cached_input": 0,
        "input": 59162,
        "output": 2435,
        "stage": "K1",
        "uncached_input": 59162
      },
      {
        "cached_input": 0,
        "input": 82677,
        "output": 2420,
        "stage": "Q",
        "uncached_input": 82677
      },
      {
        "cached_input": 0,
        "input": 85017,
        "output": 1873,
        "stage": "K2",
        "uncached_input": 85017
      }
    ],
    "total": {
      "cached_input": 866048,
      "input": 1152181,
      "input_plus_output": 1166322,
      "output": 14141,
      "uncached_input": 286133
    },
    "valid": true
  },
  "elapsed_s": 804.4530000000086
}
```
