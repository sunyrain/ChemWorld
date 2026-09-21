# C-W01-B12-E-MisIndexed

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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 365
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
      "stirring_speed_rpm": 150
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
    "byproduct_signal": 0.3303855061531067,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5108351111412048,
    "crystal_fines_fraction": 0.9973329305648804,
    "crystal_purity": 0.987384021282196,
    "crystal_size": 0.05996666103601456,
    "crystal_yield": 0.4121800363063812,
    "degradation_warning": 0.1731489896774292,
    "safety_risk": 0.1794416904449463,
    "score": 0.3854347765445709,
    "selectivity": 0.5358292460441589,
    "virtual_spectrum_summary": 0.2596290707588196,
    "yield": 0.5336667895317078
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
      "duration_s": 3600,
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
      "target_temperature_K": 285
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
  "end_step": 25,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.2996312081813812,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5618268847465515,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9743582010269165,
    "crystal_size": 0.06934945285320282,
    "crystal_yield": 0.39643988013267517,
    "degradation_warning": 0.08633970469236374,
    "safety_risk": 0.17715544998645782,
    "score": 0.3865929841995239,
    "selectivity": 0.5243415832519531,
    "virtual_spectrum_summary": 0.20365002751350403,
    "yield": 0.512895405292511
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
      "catalyst": 3,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 500,
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
      "target_temperature_K": 300
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
      "duration_s": 14400,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 315
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
      "target_temperature_K": 285
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
  "end_step": 45,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.27272993326187134,
    "conversion": 0.9982622265815735,
    "cost": 1.0,
    "crystal_csd_quality": 0.5174514651298523,
    "crystal_fines_fraction": 0.9948591589927673,
    "crystal_purity": 0.9863526225090027,
    "crystal_size": 0.0331808477640152,
    "crystal_yield": 0.4487980306148529,
    "degradation_warning": 0.1129012480378151,
    "safety_risk": 0.1844245195388794,
    "score": 0.4038025438785553,
    "selectivity": 0.5930402874946594,
    "virtual_spectrum_summary": 0.20080702006816864,
    "yield": 0.5921200513839722
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
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "catalyst": 2,
      "catalyst_amount_mol": 0.003,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 300,
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
      "instrument": "particle_size",
      "operation": "measure"
    },
    {
      "duration_s": 14400,
      "operation": "heat",
      "stirring_speed_rpm": 100,
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
      "target_temperature_K": 285
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
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.2770211100578308,
    "conversion": 0.9765859842300415,
    "cost": 1.0,
    "crystal_csd_quality": 0.4834310710430145,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 1.0,
    "crystal_size": 0.06259193271398544,
    "crystal_yield": 0.29507771134376526,
    "degradation_warning": 0.01937314122915268,
    "safety_risk": 0.12011164426803589,
    "score": 0.34645166993141174,
    "selectivity": 0.4948989450931549,
    "virtual_spectrum_summary": 0.1610795259475708,
    "yield": 0.4751838147640228
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
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.004,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 350
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.001
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
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
      "target_temperature_K": 285
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
  "end_step": 94,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.5520535707473755,
    "conversion": 0.996337890625,
    "cost": 1.0,
    "crystal_csd_quality": 0.7332283854484558,
    "crystal_fines_fraction": 0.4030592441558838,
    "crystal_purity": 0.9778274297714233,
    "crystal_size": 0.06392017006874084,
    "crystal_yield": 0.30870112776756287,
    "degradation_warning": 0.2962270975112915,
    "safety_risk": 0.1645546555519104,
    "score": 0.4280411899089813,
    "selectivity": 0.35314127802848816,
    "virtual_spectrum_summary": 0.43693166971206665,
    "yield": 0.346988320350647
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
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "catalyst": 3,
      "catalyst_amount_mol": 0.004,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 350
    },
    {
      "operation": "quench"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 330
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.001
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
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
      "target_temperature_K": 285
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
      "duration_s": 14400,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 292
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
      "target_temperature_K": 285
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
  "end_step": 127,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.2891821563243866,
    "conversion": 0.991939127445221,
    "cost": 1.0,
    "crystal_csd_quality": 0.6659283638000488,
    "crystal_fines_fraction": 0.5464034676551819,
    "crystal_purity": 0.9994372129440308,
    "crystal_size": 0.04166487976908684,
    "crystal_yield": 0.447935551404953,
    "degradation_warning": 0.09207745641469955,
    "safety_risk": 0.1806735247373581,
    "score": 0.47238364815711975,
    "selectivity": 0.541825532913208,
    "virtual_spectrum_summary": 0.20048503577709198,
    "yield": 0.5434402227401733
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
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 350
    },
    {
      "operation": "quench"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 360
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.001
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
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
      "target_temperature_K": 285
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
  "end_step": 149,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.2669704854488373,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.8471264839172363,
    "crystal_fines_fraction": 0.08904736489057541,
    "crystal_purity": 0.9802562594413757,
    "crystal_size": 0.11876086890697479,
    "crystal_yield": 0.48465973138809204,
    "degradation_warning": 0.09227129071950912,
    "safety_risk": 0.18476076424121857,
    "score": 0.5729845762252808,
    "selectivity": 0.5551769733428955,
    "virtual_spectrum_summary": 0.18835584819316864,
    "yield": 0.5817660689353943
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
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 350
    },
    {
      "operation": "quench"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 360
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.001
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
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
  "end_step": 177,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.25928041338920593,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.8902867436408997,
    "crystal_fines_fraction": 0.06215563416481018,
    "crystal_purity": 0.9806123971939087,
    "crystal_size": 0.1399177759885788,
    "crystal_yield": 0.5477375388145447,
    "degradation_warning": 0.098839171230793,
    "safety_risk": 0.1878967136144638,
    "score": 0.6035439372062683,
    "selectivity": 0.5863598585128784,
    "virtual_spectrum_summary": 0.18708185851573944,
    "yield": 0.5779964327812195
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
      "solvent": 2,
      "volume_L": 0.06
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
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 350
    },
    {
      "operation": "quench"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 360
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.001
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
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
  "end_step": 207,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.27232202887535095,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.8425216674804688,
    "crystal_fines_fraction": 0.16137999296188354,
    "crystal_purity": 0.9839603900909424,
    "crystal_size": 0.07771788537502289,
    "crystal_yield": 0.5422261357307434,
    "degradation_warning": 0.09559380263090134,
    "safety_risk": 0.19558720290660858,
    "score": 0.5747697353363037,
    "selectivity": 0.5615890622138977,
    "virtual_spectrum_summary": 0.1927943229675293,
    "yield": 0.5752629637718201
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
      "solvent": 2,
      "volume_L": 0.04
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
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 350
    },
    {
      "operation": "quench"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 360
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.001
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
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
  "end_step": 237,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.267484188079834,
    "conversion": 0.9858242273330688,
    "cost": 1.0,
    "crystal_csd_quality": 0.6424198746681213,
    "crystal_fines_fraction": 0.5390959978103638,
    "crystal_purity": 0.9834335446357727,
    "crystal_size": 0.0696340948343277,
    "crystal_yield": 0.5474953651428223,
    "degradation_warning": 0.11122676730155945,
    "safety_risk": 0.21939383447170258,
    "score": 0.4965817630290985,
    "selectivity": 0.5703151226043701,
    "virtual_spectrum_summary": 0.19716833531856537,
    "yield": 0.579241931438446
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
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 350
    },
    {
      "operation": "quench"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 360
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.0005
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
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
  "end_step": 266,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.27112168073654175,
    "conversion": 0.9989200830459595,
    "cost": 1.0,
    "crystal_csd_quality": 0.8495792150497437,
    "crystal_fines_fraction": 0.06886692345142365,
    "crystal_purity": 0.9937329888343811,
    "crystal_size": 0.10957301408052444,
    "crystal_yield": 0.530724048614502,
    "degradation_warning": 0.07986915111541748,
    "safety_risk": 0.18788982927799225,
    "score": 0.5898059606552124,
    "selectivity": 0.592562735080719,
    "virtual_spectrum_summary": 0.18505804240703583,
    "yield": 0.5730147361755371
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
      "catalyst": 3,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 350
    },
    {
      "operation": "quench"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 360
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.001
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
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
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "duration_s": 2400,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 350
    },
    {
      "operation": "quench"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 300,
      "target_temperature_K": 360
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.001
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
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
  "end_step": 321,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.25512322783470154,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.8625180125236511,
    "crystal_fines_fraction": 0.07713572680950165,
    "crystal_purity": 0.9949427843093872,
    "crystal_size": 0.13122867047786713,
    "crystal_yield": 0.5336740612983704,
    "degradation_warning": 0.10162755846977234,
    "safety_risk": 0.1878967136144638,
    "score": 0.5939872860908508,
    "selectivity": 0.5722021460533142,
    "virtual_spectrum_summary": 0.1860501766204834,
    "yield": 0.5771859884262085
  },
  "ordinal": 12
}
```

## K1

```json
{
  "payload": {
    "report": "Mechanistic account\n\nRecommendation remains batch 8.\n\nObservations. All successful late-stage processes used solvent S2 and catalyst C3. Batch 8 gave seed-excluded crystal recovery 0.548, purity 0.981, fines number fraction 0.062, normalized crystal size 0.140, and CSD quality 0.890. Related batches 11 and 12 reproduced the quality regime (purity 0.994\u20130.995; fines 0.069\u20130.077) with recoveries 0.531\u20130.534. Thus the recommended result is supported by repeat behavior, although the exact 0.548 recovery has assay/process uncertainty.\n\nMaterial effects. The public prior characterized S2 as having relatively low solubility and nucleation tendency, high crystal-growth tendency, and low impurity occlusion. The observations are consistent with that profile: S2 ultimately produced high-purity crystals while permitting large-particle, low-fines operation. This is an interpretation rather than a controlled solvent comparison, because the optimization campaign concentrated on S2 and did not run the final thermal history with S0, S1, or S3. Catalyst C3 appeared favorable for reaction selectivity: batch 3 measured selectivity 0.593, versus 0.536 for C1 in batch 1 and 0.524 for C0 in batch 2; C2 gave 0.495 in batch 4. These comparisons are confounded by temperature, loading, catalyst amount, and residence time, so they support C3 operationally but do not establish an intrinsic catalyst ranking.\n\nReaction model and coupling. A useful inventory approximation is n_target \u2248 n_reagent\u00b7X\u00b7S, where X is conversion and S is reaction selectivity; recovered product is n_recovered \u2248 Yc\u00b7n_target, where Yc is the reported seed-excluded crystallization recovery. Conversion was generally near unity, while selectivity remained only about 0.55\u20130.59 in the better quenched C3 batches. Crystallization nevertheless raised isolated crystal purity to about 0.98\u20130.995, indicating strong impurity rejection by the S2 crystallization. Reaction selectivity therefore controls absolute product mass and impurity burden, whereas Yc measures recovery only from the target already present before separation. High Yc should not be mistaken for high overall yield from reagent.\n\nThe reaction and crystallization could not be optimized independently without controlling history. In batch 5, omitting the quench and directly cooling from the reaction produced acceptable fines (0.403) but only 0.309 crystal recovery, selectivity 0.353, and degradation warning 0.296. I interpret this as continued reaction/degradation during the prolonged cooling schedule. Quenching arrested that chemistry, but quenching alone generated an unfavorable initial supersaturation history. The effective solution was quench followed by a high-temperature dissolution/reset step before controlled crystallization.\n\nCrystallization mechanism. Define relative supersaturation as \u03c3 = C/C*(T) \u2212 1. Nucleation rate J commonly increases much more steeply with \u03c3 than crystal growth rate G. Rapid creation of large \u03c3 therefore generates many sub-20 \u00b5m particles, while small staged changes in \u03c3 favor growth on an existing seed population. This explains the early failures: batch 1, despite purity 0.987 and recovery 0.412, had fines 0.997; batch 2 had fines 1.000; and batch 3, with a large 0.05 g seed charge, had fines 0.995 and very small normalized size 0.033. A larger seed charge evidently supplied excessive particle number and did not suppress the fines population.\n\nProcess-history dependence was pronounced. Late mild annealing did not repair a previously generated fine population: batch 4 changed from an in-process fines estimate of about 0.981 to 1.000 after a 310 K annealing cycle, and its final recovery fell to 0.295. Batch 6 used a quench followed by only a 330 K reset and ended at recovery 0.448 but fines 0.546, just outside specification. In contrast, batch 7 reheated to 360 K after quenching, then cooled slowly to 330 K before adding 0.001 g seed and continued through staged 320, 310, 300, and 285 K holds. It achieved recovery 0.485, purity 0.980, and fines 0.089. I interpret the 360 K step as a substantially more complete dissolution of quench-generated nuclei, effectively resetting the population before seeding.\n\nBatch 8 retained that reaction/quench/360 K reset and staged cooling history, then extended cooling through 270 K to 250 K with long low-agitation holds. Recovery increased from the batch-7 value of 0.485 to 0.548 while fines remained very low at 0.062. In this controlled regime, deeper cooling increased equilibrium driving force and deposited additional target on established crystals rather than causing an uncontrolled nucleation burst.\n\nLoading and quality/recovery tradeoff. Reducing S2 from 0.08 L in batch 8 to 0.06 L in batch 9 produced similar recovery, 0.542, but worsened fines to 0.161 and reduced normalized size to 0.078. At 0.04 L in batch 10, recovery was again similar at 0.547, but fines rose to 0.539 and failed the constraint. Thus concentration did not deliver a convincing recovery benefit but progressively narrowed and finally crossed the fines limit. Batch 11 reduced seed from 0.001 to 0.0005 g; it preserved low fines (0.069) but recovery was 0.531, offering no observed improvement. The unresolved tradeoff is therefore between aggressive concentration/deep supersaturation, which may maintain recovery but raises nucleation and fines, and the more dilute, slower batch-8 history, which gives a robust quality margin.\n\nUncertainty and revisions. The final-assay noise scales are approximately 0.01 for crystal recovery and purity and 0.018 for fines. Consequently, the recovery differences among batches 8, 9, 10, 11, and 12 are small enough that their precise ranking is uncertain. However, batch 8 has large margins to both constraints, while batches 6 and 10 exceeded the fines limit by roughly 0.046 and 0.039, respectively. Replicates 11 and 12 confirm the low-fines mechanism but show recovery variation from 0.531 to 0.534, suggesting both process variability and assay noise. My main revision during the campaign was from trying to anneal fines after formation to preventing their formation through a full high-temperature reset, small seeding dose, staged cooling, and low agitation.\n\nUntested alternatives include a controlled factorial comparison of all catalysts under the exact batch-8 history, other solvents under the same reaction and thermal program, intermediate reset temperatures between 330 and 360 K, finer optimization of seed dose and seeding temperature, and alternative hold durations. These could clarify causal material effects or shorten the process, but no tested alternative exceeded batch 8 while satisfying both purity and fines constraints."
  },
  "failure": null,
  "elapsed_s": 55.703000000008615,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 1485696,
    "input_tokens": 1619317,
    "output_tokens": 16454,
    "reasoning_output_tokens": 6039
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
          "estimate": 0.6,
          "lower80": 0.43,
          "upper80": 0.78
        },
        "crystal_purity": {
          "estimate": 0.9,
          "lower80": 0.83,
          "upper80": 0.96
        },
        "crystal_size": {
          "estimate": 0.075,
          "lower80": 0.04,
          "upper80": 0.11
        },
        "crystal_yield": {
          "estimate": 0.34,
          "lower80": 0.24,
          "upper80": 0.45
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q01"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.37,
          "lower80": 0.22,
          "upper80": 0.52
        },
        "crystal_purity": {
          "estimate": 0.95,
          "lower80": 0.9,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.1,
          "lower80": 0.06,
          "upper80": 0.14
        },
        "crystal_yield": {
          "estimate": 0.43,
          "lower80": 0.32,
          "upper80": 0.54
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q02"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.43,
          "lower80": 0.25,
          "upper80": 0.62
        },
        "crystal_purity": {
          "estimate": 0.87,
          "lower80": 0.79,
          "upper80": 0.94
        },
        "crystal_size": {
          "estimate": 0.105,
          "lower80": 0.06,
          "upper80": 0.16
        },
        "crystal_yield": {
          "estimate": 0.29,
          "lower80": 0.18,
          "upper80": 0.4
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q03"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.78,
          "lower80": 0.61,
          "upper80": 0.94
        },
        "crystal_purity": {
          "estimate": 0.86,
          "lower80": 0.78,
          "upper80": 0.93
        },
        "crystal_size": {
          "estimate": 0.045,
          "lower80": 0.02,
          "upper80": 0.08
        },
        "crystal_yield": {
          "estimate": 0.3,
          "lower80": 0.19,
          "upper80": 0.41
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q04"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.72,
          "lower80": 0.54,
          "upper80": 0.9
        },
        "crystal_purity": {
          "estimate": 0.86,
          "lower80": 0.78,
          "upper80": 0.93
        },
        "crystal_size": {
          "estimate": 0.05,
          "lower80": 0.025,
          "upper80": 0.085
        },
        "crystal_yield": {
          "estimate": 0.31,
          "lower80": 0.2,
          "upper80": 0.42
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q05"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.95,
          "lower80": 0.82,
          "upper80": 1.0
        },
        "crystal_purity": {
          "estimate": 0.85,
          "lower80": 0.76,
          "upper80": 0.93
        },
        "crystal_size": {
          "estimate": 0.025,
          "lower80": 0.01,
          "upper80": 0.055
        },
        "crystal_yield": {
          "estimate": 0.35,
          "lower80": 0.23,
          "upper80": 0.48
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q06"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.68,
          "lower80": 0.49,
          "upper80": 0.87
        },
        "crystal_purity": {
          "estimate": 0.86,
          "lower80": 0.78,
          "upper80": 0.93
        },
        "crystal_size": {
          "estimate": 0.055,
          "lower80": 0.025,
          "upper80": 0.09
        },
        "crystal_yield": {
          "estimate": 0.32,
          "lower80": 0.21,
          "upper80": 0.43
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q07"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.84,
          "lower80": 0.65,
          "upper80": 0.98
        },
        "crystal_purity": {
          "estimate": 0.88,
          "lower80": 0.79,
          "upper80": 0.95
        },
        "crystal_size": {
          "estimate": 0.035,
          "lower80": 0.015,
          "upper80": 0.07
        },
        "crystal_yield": {
          "estimate": 0.22,
          "lower80": 0.11,
          "upper80": 0.34
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q08"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.98,
          "lower80": 0.88,
          "upper80": 1.0
        },
        "crystal_purity": {
          "estimate": 0.94,
          "lower80": 0.85,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.018,
          "lower80": 0.005,
          "upper80": 0.045
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
          "estimate": 0.82,
          "lower80": 0.61,
          "upper80": 0.97
        },
        "crystal_purity": {
          "estimate": 0.91,
          "lower80": 0.82,
          "upper80": 0.97
        },
        "crystal_size": {
          "estimate": 0.03,
          "lower80": 0.01,
          "upper80": 0.065
        },
        "crystal_yield": {
          "estimate": 0.13,
          "lower80": 0.05,
          "upper80": 0.24
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q10"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.72,
          "lower80": 0.53,
          "upper80": 0.9
        },
        "crystal_purity": {
          "estimate": 0.86,
          "lower80": 0.78,
          "upper80": 0.93
        },
        "crystal_size": {
          "estimate": 0.05,
          "lower80": 0.025,
          "upper80": 0.085
        },
        "crystal_yield": {
          "estimate": 0.3,
          "lower80": 0.19,
          "upper80": 0.41
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q11"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.86,
          "lower80": 0.68,
          "upper80": 0.98
        },
        "crystal_purity": {
          "estimate": 0.83,
          "lower80": 0.73,
          "upper80": 0.91
        },
        "crystal_size": {
          "estimate": 0.04,
          "lower80": 0.018,
          "upper80": 0.075
        },
        "crystal_yield": {
          "estimate": 0.44,
          "lower80": 0.32,
          "upper80": 0.56
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q12"
      }
    ],
    "rationale": "All recipes contain seeds, so particles are expected in every batch. Q01/Q02 isolates solvent: S3's lower nominal solubility, lower nucleation tendency, faster growth, and lower impurity occlusion should give Q02 higher recovery, purity and size with fewer fines than S1. Q03/Q04 isolates seed loading in nucleation-prone S0: the small seed charge should leave fewer particles able to grow larger, whereas 0.045 g is expected to produce a seed-dominated fine population; only Q03 is provisionally feasible, with substantial boundary uncertainty. Q05/Q06 contrasts gradual and crash cooling at equal approximate duration: the crash should spend longer at low temperature and slightly raise recovery, but at the cost of severe nucleation and fines. Q07/Q08 contrasts a terminal hold with reheating to 315 K and rapid recooling: the thermal cycle may dissolve product and fines, but the short recooling period is expected to recover less material and renucleate, so it is not credited with a quality improvement. Q09/Q10 tests residence at 292 K: two additional hours should increase seed-excluded deposition and particle growth, yet probably not enough to remove the predominantly fine population. Q11/Q12 doubles reagent loading: higher concentration should increase fractional recovery but also supersaturation, impurity occlusion and secondary nucleation, reducing purity and worsening fines. Intervals are deliberately broad because these recipes extrapolate from the campaign to S0/S1/S3, much larger seed-to-product ratios, and different temperature histories; uncertainty is dominated by mechanism and process-history extrapolation rather than final-assay noise."
  },
  "failure": null,
  "elapsed_s": 112.45300000000861,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 1485696,
    "input_tokens": 1693933,
    "output_tokens": 22404,
    "reasoning_output_tokens": 10232
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
    "report": "1. Status of the main claims\n\nSupported by direct observations:\n- Controlled thermal history strongly affected particle quality. Batch 6, which used only a 330 K post-quench reset, finished with fines 0.546 and normalized size 0.042. Batch 7 used a 360 K reset followed by staged cooling and finished with fines 0.089 and size 0.119. This supports a history effect, although attributing it specifically to complete dissolution is an interpretation because the batches were not otherwise identical.\n- Extending controlled cooling from 285 K to 250 K improved recovery without sacrificing quality. Batch 7 stopped at 285 K and gave recovery 0.485; the closely related batch 8 continued through 270 K to 250 K and gave recovery 0.548, fines 0.062, and purity 0.981. Extra low-temperature residence time is a remaining confounder.\n- Increasing concentration did not produce a clear recovery advantage and worsened particle quality. With otherwise similar late-stage programs, batches 8, 9, and 10 used 0.08, 0.06, and 0.04 L S2. Their recoveries were nearly unchanged at 0.548, 0.542, and 0.547, while fines rose from 0.062 to 0.161 and then 0.539. This directly supports the concentration\u2013fines tradeoff.\n- The successful regime was reproducible qualitatively. Batches 8, 11, and 12 all used dilute S2, a high-temperature reset, staged deep cooling, and small seed charges. They all passed quality, with fines 0.062\u20130.077 and purity 0.981\u20130.995, although recovery varied from 0.531 to 0.548.\n- Crystallization strongly enriched target relative to the reaction mixture. For example, batch 8 had reaction selectivity 0.586 but crystal purity 0.981. Similar high crystal purity appeared across many batches despite only moderate reaction selectivity. Preferential impurity rejection is the most plausible interpretation, but the observations do not identify the microscopic exclusion mechanism.\n\nSupported but confounded:\n- Quenching followed by reheating appeared to decouple reaction termination from crystallization control. Batch 5 omitted quenching and passed the fines limit, but had selectivity 0.353, degradation warning 0.296, and recovery 0.309. Quenched batches 7 and 8 had much lower degradation warnings and higher recovery. Continued reaction or degradation during batch 5\u2019s long cooling is plausible, but catalyst amount, temperature trajectory, and final temperature also differed.\n- Late annealing did not reliably repair an established fine population. Batch 4\u2019s particle estimate changed from fines 0.981 before its annealing sequence to 1.000 afterward; batch 6 also remained above specification after a mild terminal cycle. This supports prevention rather than repair, but neither was a clean annealing control.\n\nContradicted or not supported:\n- A simple expectation that higher concentration should increase fractional crystallization recovery was contradicted over batches 8\u201310: recovery was essentially flat while fines worsened sharply.\n- The data did not support reducing seed from 0.001 to 0.0005 g as an improvement. Batch 11 retained excellent fines but recovered 0.531 versus 0.548 in batch 8. The difference is small enough that no strong adverse seed-dose conclusion is warranted.\n\nStill untested:\n- S2\u2019s superiority over S0, S1, and S3 under the final batch-8 history remains untested. The material dossier supports the proposed low-solubility/high-growth interpretation, but the campaign did not make a controlled solvent comparison.\n- The apparent catalyst ranking is not causal. C3 batches often had better selectivity than the early C0/C1/C2 batches, but reaction conditions and downstream histories differed.\n- The claim that a large seed charge itself caused the poor CSD in batch 3 is weak. Batch 3 used 0.05 g seed and had fines 0.995, but it also had an incomplete thermal reset and a different cooling history.\n\n2. One additional experiment\n\nI would repeat batch 8 exactly, changing only the post-quench reset temperature from 360 K to 330 K. I would retain 0.08 L S2, 0.04 mol reagent, 0.005 mol C3, the 0.001 g seed charge, all staged cooling and holds through 250 K, and the same filtration point.\n\nThis would distinguish two explanations for batches 7\u20138:\n- Full-reset explanation: 360 K dissolves quench-generated nuclei or residual solids, and that population reset is essential.\n- Slow-cooling explanation: the long staged cooling, low agitation, and small seed charge dominate, while 360 K is incidental.\n\nIf the full-reset explanation is correct, the 330 K batch should retain excess nuclei and finish with substantially smaller particles and fines around 0.4\u20130.6, while purity and recovery could remain near 0.98 and 0.52\u20130.55. If slow cooling is sufficient, it should resemble batch 8, with fines below about 0.15, size around 0.10\u20130.14, and recovery around 0.52\u20130.55. A clean result would also clarify whether batch 6 failed because of its reset temperature or because of its different downstream annealing history.\n\n3. Weakest use of evidence and least reliable prediction\n\nThe account used batch 3 least effectively. Its combination of a 0.05 g seed charge, fines 0.995, size 0.033, and recovery 0.449 was cited as evidence that excessive seeding creates a fine population. However, batch 3 also underwent quenching, crystallization before a complete high-temperature reset, and subsequent thermal cycling. Those factors could independently explain its poor CSD. The observation was real, but the seed-dose interpretation was underidentified.\n\nQ08 is the least reliable held-out prediction. It introduces a 315 K reheat only after an extended slow crystallization, followed by rapid recooling. No campaign batch used that exact ordering and timescale. Reheating could partially dissolve only fines and improve the distribution, dissolve most product and reduce recovery, or erase the population and trigger renewed nucleation during rapid recooling. The campaign\u2019s thermal cycles were performed under materially different histories, so Q08\u2019s predicted recovery and fines rely on the most uncertain extrapolation of the sealed set."
  },
  "failure": null,
  "elapsed_s": 52.515999999974156,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 1548928,
    "input_tokens": 1774419,
    "output_tokens": 24931,
    "reasoning_output_tokens": 11352
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
    "selection_rationale": "Batch 8 delivered the highest observed seed-excluded crystal recovery among specification-passing batches (crystal_yield 0.548), with crystal_purity 0.981 and fines fraction 0.062, comfortably meeting both quality constraints."
  },
  "recommendation_recipe": {
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
        "duration_s": 2400,
        "operation": "heat",
        "stirring_speed_rpm": 300,
        "target_temperature_K": 350
      },
      {
        "operation": "quench"
      },
      {
        "duration_s": 7200,
        "operation": "heat",
        "stirring_speed_rpm": 300,
        "target_temperature_K": 360
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 330
      },
      {
        "operation": "seed_crystals",
        "seed_mass_g": 0.001
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 320
      },
      {
        "duration_s": 14400,
        "operation": "wait",
        "stirring_speed_rpm": 100
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
    "lifecycle_index": 8,
    "source_attempts": 28
  },
  "prediction_evaluation": {
    "contrasts": [
      {
        "absolute_delta_error": 0.16294062343774243,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_yield",
        "predicted_delta": 0.08999999999999997,
        "resolved": true,
        "true_delta": -0.07294062343774246
      },
      {
        "absolute_delta_error": 0.05125387745275822,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_purity",
        "predicted_delta": 0.04999999999999993,
        "resolved": false,
        "true_delta": -0.0012538774527582897
      },
      {
        "absolute_delta_error": 0.009346698071698023,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_size",
        "predicted_delta": 0.02500000000000001,
        "resolved": true,
        "true_delta": 0.015653301928301985
      },
      {
        "absolute_delta_error": 0.21321528505582216,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.22999999999999998,
        "resolved": true,
        "true_delta": -0.44321528505582214
      },
      {
        "absolute_delta_error": 0.010048337487764791,
        "direction_correct": true,
        "factor": "seed",
        "metric": "crystal_yield",
        "predicted_delta": 0.010000000000000009,
        "resolved": false,
        "true_delta": -4.8337487764782416e-05
      },
      {
        "absolute_delta_error": 0.018132470445263338,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_purity",
        "predicted_delta": -0.010000000000000009,
        "resolved": false,
        "true_delta": 0.008132470445263329
      },
      {
        "absolute_delta_error": 0.06042249560740072,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_size",
        "predicted_delta": -0.06,
        "resolved": false,
        "true_delta": 0.0004224956074007219
      },
      {
        "absolute_delta_error": 0.37482623967298034,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.35000000000000003,
        "resolved": false,
        "true_delta": -0.02482623967298031
      },
      {
        "absolute_delta_error": 0.039767182469520934,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_yield",
        "predicted_delta": 0.03999999999999998,
        "resolved": false,
        "true_delta": 0.00023281753047904585
      },
      {
        "absolute_delta_error": 0.005209363860740779,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.010000000000000009,
        "resolved": false,
        "true_delta": -0.00479063613925923
      },
      {
        "absolute_delta_error": 0.014205409363576907,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_size",
        "predicted_delta": -0.025,
        "resolved": true,
        "true_delta": -0.03920540936357691
      },
      {
        "absolute_delta_error": 0.4463771602380363,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.22999999999999998,
        "resolved": true,
        "true_delta": 0.6763771602380363
      },
      {
        "absolute_delta_error": 0.1415617281802011,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_yield",
        "predicted_delta": -0.1,
        "resolved": true,
        "true_delta": 0.041561728180201096
      },
      {
        "absolute_delta_error": 0.02926416706539703,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_purity",
        "predicted_delta": 0.020000000000000018,
        "resolved": false,
        "true_delta": -0.009264167065397011
      },
      {
        "absolute_delta_error": 0.010443732116858395,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_size",
        "predicted_delta": -0.019999999999999997,
        "resolved": true,
        "true_delta": -0.030443732116858392
      },
      {
        "absolute_delta_error": 0.5361786076870267,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.15999999999999992,
        "resolved": true,
        "true_delta": 0.6961786076870267
      },
      {
        "absolute_delta_error": 0.04572767781178036,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_yield",
        "predicted_delta": 0.10500000000000001,
        "resolved": true,
        "true_delta": 0.15072767781178037
      },
      {
        "absolute_delta_error": 0.01592697628066231,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_purity",
        "predicted_delta": -0.029999999999999916,
        "resolved": true,
        "true_delta": -0.014073023719337607
      },
      {
        "absolute_delta_error": 0.0028757983905376046,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_size",
        "predicted_delta": 0.012,
        "resolved": true,
        "true_delta": 0.014875798390537605
      },
      {
        "absolute_delta_error": 0.1802644368469809,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.16000000000000003,
        "resolved": false,
        "true_delta": 0.02026443684698087
      },
      {
        "absolute_delta_error": 0.10925974627058055,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_yield",
        "predicted_delta": 0.14,
        "resolved": true,
        "true_delta": 0.030740253729419464
      },
      {
        "absolute_delta_error": 0.023976332586183147,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_purity",
        "predicted_delta": -0.030000000000000027,
        "resolved": false,
        "true_delta": -0.00602366741381688
      },
      {
        "absolute_delta_error": 0.01756370662678719,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_size",
        "predicted_delta": -0.010000000000000002,
        "resolved": true,
        "true_delta": -0.027563706626787192
      },
      {
        "absolute_delta_error": 0.5485789828624289,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.14,
        "resolved": true,
        "true_delta": 0.6885789828624289
      }
    ],
    "failures": [],
    "metrics": {
      "crystal_fines_fraction": {
        "coverage80": 0.3333333333333333,
        "interval_score80": 1.1446535077857343,
        "interval_width": 0.3125,
        "mae": 0.2032516923244607,
        "n": 12,
        "planned": 12
      },
      "crystal_purity": {
        "coverage80": 0.08333333333333333,
        "interval_score80": 0.5317340275570102,
        "interval_width": 0.1475,
        "mae": 0.10414178906574012,
        "n": 12,
        "planned": 12
      },
      "crystal_size": {
        "coverage80": 0.9166666666666666,
        "interval_score80": 0.06479635471865776,
        "interval_width": 0.06225,
        "mae": 0.021225333923483834,
        "n": 12,
        "planned": 12
      },
      "crystal_yield": {
        "coverage80": 0.9166666666666666,
        "interval_score80": 0.3011642718977899,
        "interval_width": 0.21,
        "mae": 0.056852315565230266,
        "n": 12,
        "planned": 12
      }
    },
    "quality": {
      "balanced_accuracy": 0.6666666666666666,
      "false_negative": 4,
      "false_positive": 0,
      "true_negative": 6,
      "true_positive": 2
    },
    "resolved_direction_correct": 12,
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
        "crystal_purity": 0.004738603005620993,
        "crystal_size": 0.016575762692193362,
        "crystal_yield": 0.2042957866580238
      },
      "public_nearest_neighbor": {
        "crystal_fines_fraction": 0.24077925155432953,
        "crystal_purity": 0.004492668700435409,
        "crystal_size": 0.015600017895940954,
        "crystal_yield": 0.27126782878150046
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
        "cached_input": 1485696,
        "input": 1555871,
        "output": 13820,
        "stage": "source",
        "uncached_input": 70175
      },
      {
        "cached_input": 0,
        "input": 63446,
        "output": 2634,
        "stage": "K1",
        "uncached_input": 63446
      },
      {
        "cached_input": 0,
        "input": 74616,
        "output": 5950,
        "stage": "Q",
        "uncached_input": 74616
      },
      {
        "cached_input": 63232,
        "input": 80486,
        "output": 2527,
        "stage": "K2",
        "uncached_input": 17254
      }
    ],
    "total": {
      "cached_input": 1548928,
      "input": 1774419,
      "input_plus_output": 1799350,
      "output": 24931,
      "uncached_input": 225491
    },
    "valid": true
  },
  "elapsed_s": 743.4529999999795
}
```
