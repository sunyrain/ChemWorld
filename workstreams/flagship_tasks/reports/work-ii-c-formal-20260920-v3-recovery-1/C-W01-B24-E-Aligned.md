# C-W01-B24-E-Aligned

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
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 3600,
      "operation": "cool_crystallize",
      "target_temperature_K": 320
    },
    {
      "duration_s": 7200,
      "operation": "wait",
      "stirring_speed_rpm": 300
    },
    {
      "duration_s": 7200,
      "operation": "cool_crystallize",
      "target_temperature_K": 270
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
  "end_step": 15,
  "lifecycle_index": 1,
  "metrics": {
    "byproduct_signal": 0.32109472155570984,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5003650784492493,
    "crystal_fines_fraction": 0.9972182512283325,
    "crystal_purity": 0.9883275032043457,
    "crystal_size": 0.05420699715614319,
    "crystal_yield": 0.43854326009750366,
    "degradation_warning": 0.15056051313877106,
    "safety_risk": 0.18101076781749725,
    "score": 0.3916333317756653,
    "selectivity": 0.5474326014518738,
    "virtual_spectrum_summary": 0.24435432255268097,
    "yield": 0.5452700853347778
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 600,
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
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
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
  "end_step": 46,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.421561598777771,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5183612108230591,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9815369248390198,
    "crystal_size": 0.0766599252820015,
    "crystal_yield": 0.3202090561389923,
    "degradation_warning": 0.2087106853723526,
    "safety_risk": 0.16654597222805023,
    "score": 0.34461578726768494,
    "selectivity": 0.4333741068840027,
    "virtual_spectrum_summary": 0.32577869296073914,
    "yield": 0.42192912101745605
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
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
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
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 100
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 295
    },
    {
      "duration_s": 7200,
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
  "end_step": 71,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.32922694087028503,
    "conversion": 0.9983176589012146,
    "cost": 1.0,
    "crystal_csd_quality": 0.5140780210494995,
    "crystal_fines_fraction": 0.9948385953903198,
    "crystal_purity": 0.9866967797279358,
    "crystal_size": 0.03647034615278244,
    "crystal_yield": 0.4282888174057007,
    "degradation_warning": 0.16627717018127441,
    "safety_risk": 0.1798517256975174,
    "score": 0.3885197937488556,
    "selectivity": 0.538790225982666,
    "virtual_spectrum_summary": 0.2558995485305786,
    "yield": 0.5379027724266052
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
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
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
  "end_step": 162,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.3225976526737213,
    "conversion": 0.988996148109436,
    "cost": 1.0,
    "crystal_csd_quality": 0.5085489749908447,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 1.0,
    "crystal_size": 0.05199287459254265,
    "crystal_yield": 0.3428098261356354,
    "degradation_warning": 0.05251839756965637,
    "safety_risk": 0.16805094480514526,
    "score": 0.3537844717502594,
    "selectivity": 0.4594929814338684,
    "virtual_spectrum_summary": 0.20106197893619537,
    "yield": 0.44586315751075745
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
      "duration_s": 1800,
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
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
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
  "end_step": 186,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.2479073703289032,
    "conversion": 0.996147096157074,
    "cost": 1.0,
    "crystal_csd_quality": 0.5138647556304932,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9721836447715759,
    "crystal_size": 0.03184167668223381,
    "crystal_yield": 0.46054357290267944,
    "degradation_warning": 0.057019367814064026,
    "safety_risk": 0.18612252175807953,
    "score": 0.4099161624908447,
    "selectivity": 0.6367966532707214,
    "virtual_spectrum_summary": 0.16200776398181915,
    "yield": 0.6305248737335205
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
      "target_temperature_K": 350
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 330
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
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
  "end_step": 208,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.37853744626045227,
    "conversion": 0.9924335479736328,
    "cost": 1.0,
    "crystal_csd_quality": 0.8123206496238708,
    "crystal_fines_fraction": 0.1673828661441803,
    "crystal_purity": 1.0,
    "crystal_size": 0.069259412586689,
    "crystal_yield": 0.4156251847743988,
    "degradation_warning": 0.1913420706987381,
    "safety_risk": 0.17801012098789215,
    "score": 0.5277241468429565,
    "selectivity": 0.5053074955940247,
    "virtual_spectrum_summary": 0.29429954290390015,
    "yield": 0.5071931481361389
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
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 350
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 340
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
  "end_step": 235,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.34942007064819336,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.8454086184501648,
    "crystal_fines_fraction": 0.09996192157268524,
    "crystal_purity": 0.9817177653312683,
    "crystal_size": 0.11157777160406113,
    "crystal_yield": 0.46582624316215515,
    "degradation_warning": 0.1660037338733673,
    "safety_risk": 0.18266120553016663,
    "score": 0.5571408271789551,
    "selectivity": 0.504974901676178,
    "virtual_spectrum_summary": 0.2668827176094055,
    "yield": 0.5316221117973328
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
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 600,
      "target_temperature_K": 360
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 350
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 340
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
  "end_step": 265,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.24219828844070435,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.8914061784744263,
    "crystal_fines_fraction": 0.05790353938937187,
    "crystal_purity": 0.9809445142745972,
    "crystal_size": 0.1345711648464203,
    "crystal_yield": 0.5693610310554504,
    "degradation_warning": 0.06740178912878036,
    "safety_risk": 0.19460105895996094,
    "score": 0.6155998706817627,
    "selectivity": 0.6230582594871521,
    "virtual_spectrum_summary": 0.16353987157344818,
    "yield": 0.6147529482841492
  },
  "ordinal": 8
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
        "crystal_fines_fraction": 0.31402314041245477,
        "crystal_purity": 0.004522471596611714,
        "crystal_size": 0.017013185815904552,
        "crystal_yield": 0.1764758924038162
      },
      "public_nearest_neighbor": {
        "crystal_fines_fraction": 0.4058902521826895,
        "crystal_purity": 0.004778631917852809,
        "crystal_size": 0.03426054999033374,
        "crystal_yield": 0.20760409776279828
      }
    },
    "training_batches": 8
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
  "elapsed_s": 234.25
}
```
