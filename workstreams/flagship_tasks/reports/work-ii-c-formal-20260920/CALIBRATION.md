# Crystallization development calibration

All 24 candidates retained. World seed 17 is excluded from formal worlds.

| Candidate | Factor | Variant | Executed | Recovery | Purity | Size index | Fines | Quality |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| D01 | solvent | long | True | 0.286189 | 0.987179 | 0.059143 | 0.998947 | False |
| D02 | solvent | long | True | 0.129975 | 0.985786 | 0.088567 | 0.369921 | True |
| D03 | solvent | short | True | 0.285402 | 0.985502 | 0.057755 | 0.999548 | False |
| D04 | solvent | short | True | 0.122672 | 0.981934 | 0.055283 | 0.998937 | False |
| D05 | seed | transient | True | 0.006126 | 0.980355 | 0.034899 | 0.999819 | False |
| D06 | seed | transient | True | 0.009723 | 0.997290 | 0.034746 | 0.990225 | False |
| D07 | seed | gentle | True | 0.091399 | 0.978224 | 0.072738 | 0.684169 | False |
| D08 | seed | gentle | True | 0.091031 | 0.987691 | 0.068594 | 0.780788 | False |
| D09 | cooling_history | transient | True | 0.106328 | 0.982752 | 0.048077 | 0.999025 | False |
| D10 | cooling_history | transient | True | 0.130470 | 0.980519 | 0.047598 | 0.999322 | False |
| D11 | cooling_history | gentle | True | 0.129553 | 0.985762 | 0.079882 | 0.501113 | False |
| D12 | cooling_history | gentle | True | 0.130471 | 0.983116 | 0.051066 | 0.998834 | False |
| D13 | thermal_history | partial_dissolution | True | 0.118588 | 0.983539 | 0.048333 | 0.998830 | False |
| D14 | thermal_history | partial_dissolution | True | 0.051521 | 0.971227 | 0.039376 | 1.000000 | False |
| D15 | thermal_history | long_memory | True | 0.085907 | 0.988052 | 0.071518 | 0.690403 | False |
| D16 | thermal_history | long_memory | True | 0.118741 | 0.975391 | 0.052812 | 1.000000 | False |
| D17 | continue_growth | early | True | 0.000064 | 0.999962 | 0.032073 | 0.613134 | False |
| D18 | continue_growth | early | True | 0.031001 | 0.989673 | 0.048816 | 0.996909 | False |
| D19 | continue_growth | late | True | 0.062985 | 0.988997 | 0.051855 | 0.995738 | False |
| D20 | continue_growth | late | True | 0.071522 | 0.988283 | 0.054344 | 0.995837 | False |
| D21 | upstream_loading | gentle | True | 0.000000 | 1.000000 | 0.400000 | 0.000000 | True |
| D22 | upstream_loading | gentle | True | 0.103364 | 0.983405 | 0.086239 | 0.324625 | True |
| D23 | upstream_loading | transient | True | 0.000000 | 1.000000 | 0.400000 | 0.000000 | True |
| D24 | upstream_loading | transient | True | 0.037330 | 0.983140 | 0.040609 | 0.999293 | False |

## Development selection

```json
{
  "acceptable": true,
  "coverage": {
    "quality_positive": 3,
    "quality_negative": 9,
    "feasible": 2,
    "resolved_pairs": 6,
    "contrasts": [
      {
        "factor": "solvent",
        "deltas": {
          "crystal_yield": -0.156213311977061,
          "crystal_purity": -0.001392933342861613,
          "crystal_size": 0.029423736845637358,
          "crystal_fines_fraction": -0.6290263713814402
        },
        "resolved": true
      },
      {
        "factor": "seed",
        "deltas": {
          "crystal_yield": 0.0035969014349340077,
          "crystal_purity": 0.01693457584849989,
          "crystal_size": -0.00015303949036007958,
          "crystal_fines_fraction": -0.00959455280907584
        },
        "resolved": true
      },
      {
        "factor": "cooling_history",
        "deltas": {
          "crystal_yield": 0.0009187131634270651,
          "crystal_purity": -0.002646221450656294,
          "crystal_size": -0.028815808257469183,
          "crystal_fines_fraction": 0.4977211991947942
        },
        "resolved": true
      },
      {
        "factor": "thermal_history",
        "deltas": {
          "crystal_yield": 0.03283391134415016,
          "crystal_purity": -0.012660994435080952,
          "crystal_size": -0.018706248421504687,
          "crystal_fines_fraction": 0.30959731507155175
        },
        "resolved": true
      },
      {
        "factor": "continue_growth",
        "deltas": {
          "crystal_yield": 0.030936987554258978,
          "crystal_purity": -0.010288163627643732,
          "crystal_size": 0.01674292993472739,
          "crystal_fines_fraction": 0.38377487508841057
        },
        "resolved": true
      },
      {
        "factor": "upstream_loading",
        "deltas": {
          "crystal_yield": 0.10336370087989104,
          "crystal_purity": -0.01659452281819196,
          "crystal_size": -0.3137612584808862,
          "crystal_fines_fraction": 0.32462455856280903
        },
        "resolved": true
      }
    ]
  },
  "queries": [
    {
      "query_id": "Q01",
      "pair": "solvent",
      "calibration_id": "D01",
      "actions": [
        {
          "operation": "add_solvent",
          "volume_L": 0.028,
          "solvent": 1
        },
        {
          "operation": "add_reagent",
          "amount_mol": 0.01
        },
        {
          "operation": "add_catalyst",
          "catalyst_amount_mol": 0.00025,
          "catalyst": 1
        },
        {
          "operation": "heat",
          "target_temperature_K": 385.0,
          "duration_s": 1500.0,
          "stirring_speed_rpm": 720.0
        },
        {
          "operation": "wait",
          "duration_s": 900.0,
          "stirring_speed_rpm": 720.0
        },
        {
          "operation": "quench"
        },
        {
          "operation": "seed_crystals",
          "seed_mass_g": 0.05
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 298.1791666666667,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 296.35833333333335,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 294.5375,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 292.71666666666664,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 290.8958333333333,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 289.075,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 287.25416666666666,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 285.43333333333334,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 283.61249999999995,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 281.79166666666663,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 279.9708333333333,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 278.15,
          "duration_s": 14400
        },
        {
          "operation": "filter_crystals"
        },
        {
          "operation": "terminate"
        },
        {
          "operation": "measure",
          "instrument": "final_assay"
        }
      ]
    },
    {
      "query_id": "Q02",
      "pair": "solvent",
      "calibration_id": "D02",
      "actions": [
        {
          "operation": "add_solvent",
          "volume_L": 0.028,
          "solvent": 3
        },
        {
          "operation": "add_reagent",
          "amount_mol": 0.01
        },
        {
          "operation": "add_catalyst",
          "catalyst_amount_mol": 0.00025,
          "catalyst": 1
        },
        {
          "operation": "heat",
          "target_temperature_K": 385.0,
          "duration_s": 1500.0,
          "stirring_speed_rpm": 720.0
        },
        {
          "operation": "wait",
          "duration_s": 900.0,
          "stirring_speed_rpm": 720.0
        },
        {
          "operation": "quench"
        },
        {
          "operation": "seed_crystals",
          "seed_mass_g": 0.05
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 298.1791666666667,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 296.35833333333335,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 294.5375,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 292.71666666666664,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 290.8958333333333,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 289.075,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 287.25416666666666,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 285.43333333333334,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 283.61249999999995,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 281.79166666666663,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 279.9708333333333,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 278.15,
          "duration_s": 14400
        },
        {
          "operation": "filter_crystals"
        },
        {
          "operation": "terminate"
        },
        {
          "operation": "measure",
          "instrument": "final_assay"
        }
      ]
    },
    {
      "query_id": "Q03",
      "pair": "seed",
      "calibration_id": "D05",
      "actions": [
        {
          "operation": "add_solvent",
          "volume_L": 0.028,
          "solvent": 3
        },
        {
          "operation": "add_reagent",
          "amount_mol": 0.01
        },
        {
          "operation": "add_catalyst",
          "catalyst_amount_mol": 0.00025,
          "catalyst": 1
        },
        {
          "operation": "heat",
          "target_temperature_K": 385.0,
          "duration_s": 1500.0,
          "stirring_speed_rpm": 720.0
        },
        {
          "operation": "wait",
          "duration_s": 900.0,
          "stirring_speed_rpm": 720.0
        },
        {
          "operation": "quench"
        },
        {
          "operation": "seed_crystals",
          "seed_mass_g": 0.001
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 294,
          "duration_s": 600
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 288,
          "duration_s": 600
        },
        {
          "operation": "filter_crystals"
        },
        {
          "operation": "terminate"
        },
        {
          "operation": "measure",
          "instrument": "final_assay"
        }
      ]
    },
    {
      "query_id": "Q04",
      "pair": "seed",
      "calibration_id": "D06",
      "actions": [
        {
          "operation": "add_solvent",
          "volume_L": 0.028,
          "solvent": 3
        },
        {
          "operation": "add_reagent",
          "amount_mol": 0.01
        },
        {
          "operation": "add_catalyst",
          "catalyst_amount_mol": 0.00025,
          "catalyst": 1
        },
        {
          "operation": "heat",
          "target_temperature_K": 385.0,
          "duration_s": 1500.0,
          "stirring_speed_rpm": 720.0
        },
        {
          "operation": "wait",
          "duration_s": 900.0,
          "stirring_speed_rpm": 720.0
        },
        {
          "operation": "quench"
        },
        {
          "operation": "seed_crystals",
          "seed_mass_g": 0.05
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 294,
          "duration_s": 600
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 288,
          "duration_s": 600
        },
        {
          "operation": "filter_crystals"
        },
        {
          "operation": "terminate"
        },
        {
          "operation": "measure",
          "instrument": "final_assay"
        }
      ]
    },
    {
      "query_id": "Q05",
      "pair": "cooling_history",
      "calibration_id": "D11",
      "actions": [
        {
          "operation": "add_solvent",
          "volume_L": 0.028,
          "solvent": 3
        },
        {
          "operation": "add_reagent",
          "amount_mol": 0.01
        },
        {
          "operation": "add_catalyst",
          "catalyst_amount_mol": 0.00025,
          "catalyst": 1
        },
        {
          "operation": "heat",
          "target_temperature_K": 385.0,
          "duration_s": 1500.0,
          "stirring_speed_rpm": 720.0
        },
        {
          "operation": "wait",
          "duration_s": 900.0,
          "stirring_speed_rpm": 720.0
        },
        {
          "operation": "quench"
        },
        {
          "operation": "seed_crystals",
          "seed_mass_g": 0.05
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 298.1791666666667,
          "duration_s": 7200
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 296.35833333333335,
          "duration_s": 7200
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 294.5375,
          "duration_s": 7200
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 292.71666666666664,
          "duration_s": 7200
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 290.8958333333333,
          "duration_s": 7200
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 289.075,
          "duration_s": 7200
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 287.25416666666666,
          "duration_s": 7200
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 285.43333333333334,
          "duration_s": 7200
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 283.61249999999995,
          "duration_s": 7200
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 281.79166666666663,
          "duration_s": 7200
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 279.9708333333333,
          "duration_s": 7200
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 278.15,
          "duration_s": 7200
        },
        {
          "operation": "filter_crystals"
        },
        {
          "operation": "terminate"
        },
        {
          "operation": "measure",
          "instrument": "final_assay"
        }
      ]
    },
    {
      "query_id": "Q06",
      "pair": "cooling_history",
      "calibration_id": "D12",
      "actions": [
        {
          "operation": "add_solvent",
          "volume_L": 0.028,
          "solvent": 3
        },
        {
          "operation": "add_reagent",
          "amount_mol": 0.01
        },
        {
          "operation": "add_catalyst",
          "catalyst_amount_mol": 0.00025,
          "catalyst": 1
        },
        {
          "operation": "heat",
          "target_temperature_K": 385.0,
          "duration_s": 1500.0,
          "stirring_speed_rpm": 720.0
        },
        {
          "operation": "wait",
          "duration_s": 900.0,
          "stirring_speed_rpm": 720.0
        },
        {
          "operation": "quench"
        },
        {
          "operation": "seed_crystals",
          "seed_mass_g": 0.05
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 278.15,
          "duration_s": 120
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 278.15,
          "duration_s": 14380
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 278.15,
          "duration_s": 14380
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 278.15,
          "duration_s": 14380
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 278.15,
          "duration_s": 14380
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 278.15,
          "duration_s": 14380
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 278.15,
          "duration_s": 14380
        },
        {
          "operation": "filter_crystals"
        },
        {
          "operation": "terminate"
        },
        {
          "operation": "measure",
          "instrument": "final_assay"
        }
      ]
    },
    {
      "query_id": "Q07",
      "pair": "thermal_history",
      "calibration_id": "D15",
      "actions": [
        {
          "operation": "add_solvent",
          "volume_L": 0.028,
          "solvent": 3
        },
        {
          "operation": "add_reagent",
          "amount_mol": 0.01
        },
        {
          "operation": "add_catalyst",
          "catalyst_amount_mol": 0.00025,
          "catalyst": 1
        },
        {
          "operation": "heat",
          "target_temperature_K": 385.0,
          "duration_s": 1500.0,
          "stirring_speed_rpm": 720.0
        },
        {
          "operation": "wait",
          "duration_s": 900.0,
          "stirring_speed_rpm": 720.0
        },
        {
          "operation": "quench"
        },
        {
          "operation": "seed_crystals",
          "seed_mass_g": 0.05
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 297.5,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 295.0,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 292.5,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 290.0,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 287.5,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 285.0,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 285,
          "duration_s": 14400
        },
        {
          "operation": "filter_crystals"
        },
        {
          "operation": "terminate"
        },
        {
          "operation": "measure",
          "instrument": "final_assay"
        }
      ]
    },
    {
      "query_id": "Q08",
      "pair": "thermal_history",
      "calibration_id": "D16",
      "actions": [
        {
          "operation": "add_solvent",
          "volume_L": 0.028,
          "solvent": 3
        },
        {
          "operation": "add_reagent",
          "amount_mol": 0.01
        },
        {
          "operation": "add_catalyst",
          "catalyst_amount_mol": 0.00025,
          "catalyst": 1
        },
        {
          "operation": "heat",
          "target_temperature_K": 385.0,
          "duration_s": 1500.0,
          "stirring_speed_rpm": 720.0
        },
        {
          "operation": "wait",
          "duration_s": 900.0,
          "stirring_speed_rpm": 720.0
        },
        {
          "operation": "quench"
        },
        {
          "operation": "seed_crystals",
          "seed_mass_g": 0.05
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 297.5,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 295.0,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 292.5,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 290.0,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 287.5,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 285.0,
          "duration_s": 14400
        },
        {
          "operation": "heat",
          "target_temperature_K": 325,
          "duration_s": 7200,
          "stirring_speed_rpm": 600.0
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 285,
          "duration_s": 7200
        },
        {
          "operation": "filter_crystals"
        },
        {
          "operation": "terminate"
        },
        {
          "operation": "measure",
          "instrument": "final_assay"
        }
      ]
    },
    {
      "query_id": "Q09",
      "pair": "continue_growth",
      "calibration_id": "D17",
      "actions": [
        {
          "operation": "add_solvent",
          "volume_L": 0.028,
          "solvent": 3
        },
        {
          "operation": "add_reagent",
          "amount_mol": 0.01
        },
        {
          "operation": "add_catalyst",
          "catalyst_amount_mol": 0.00025,
          "catalyst": 1
        },
        {
          "operation": "heat",
          "target_temperature_K": 385.0,
          "duration_s": 1500.0,
          "stirring_speed_rpm": 720.0
        },
        {
          "operation": "wait",
          "duration_s": 900.0,
          "stirring_speed_rpm": 720.0
        },
        {
          "operation": "quench"
        },
        {
          "operation": "seed_crystals",
          "seed_mass_g": 0.025
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 292,
          "duration_s": 60
        },
        {
          "operation": "filter_crystals"
        },
        {
          "operation": "terminate"
        },
        {
          "operation": "measure",
          "instrument": "final_assay"
        }
      ]
    },
    {
      "query_id": "Q10",
      "pair": "continue_growth",
      "calibration_id": "D18",
      "actions": [
        {
          "operation": "add_solvent",
          "volume_L": 0.028,
          "solvent": 3
        },
        {
          "operation": "add_reagent",
          "amount_mol": 0.01
        },
        {
          "operation": "add_catalyst",
          "catalyst_amount_mol": 0.00025,
          "catalyst": 1
        },
        {
          "operation": "heat",
          "target_temperature_K": 385.0,
          "duration_s": 1500.0,
          "stirring_speed_rpm": 720.0
        },
        {
          "operation": "wait",
          "duration_s": 900.0,
          "stirring_speed_rpm": 720.0
        },
        {
          "operation": "quench"
        },
        {
          "operation": "seed_crystals",
          "seed_mass_g": 0.025
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 292,
          "duration_s": 60
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 292,
          "duration_s": 7200
        },
        {
          "operation": "filter_crystals"
        },
        {
          "operation": "terminate"
        },
        {
          "operation": "measure",
          "instrument": "final_assay"
        }
      ]
    },
    {
      "query_id": "Q11",
      "pair": "upstream_loading",
      "calibration_id": "D21",
      "actions": [
        {
          "operation": "add_solvent",
          "volume_L": 0.028,
          "solvent": 3
        },
        {
          "operation": "add_reagent",
          "amount_mol": 0.004
        },
        {
          "operation": "add_catalyst",
          "catalyst_amount_mol": 0.00025,
          "catalyst": 1
        },
        {
          "operation": "heat",
          "target_temperature_K": 385.0,
          "duration_s": 1500.0,
          "stirring_speed_rpm": 720.0
        },
        {
          "operation": "wait",
          "duration_s": 900.0,
          "stirring_speed_rpm": 720.0
        },
        {
          "operation": "quench"
        },
        {
          "operation": "seed_crystals",
          "seed_mass_g": 0.05
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 297.75,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 295.5,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 293.25,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 291.0,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 288.75,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 286.5,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 284.25,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 282.0,
          "duration_s": 14400
        },
        {
          "operation": "filter_crystals"
        },
        {
          "operation": "terminate"
        },
        {
          "operation": "measure",
          "instrument": "final_assay"
        }
      ]
    },
    {
      "query_id": "Q12",
      "pair": "upstream_loading",
      "calibration_id": "D22",
      "actions": [
        {
          "operation": "add_solvent",
          "volume_L": 0.028,
          "solvent": 3
        },
        {
          "operation": "add_reagent",
          "amount_mol": 0.02
        },
        {
          "operation": "add_catalyst",
          "catalyst_amount_mol": 0.00025,
          "catalyst": 1
        },
        {
          "operation": "heat",
          "target_temperature_K": 385.0,
          "duration_s": 1500.0,
          "stirring_speed_rpm": 720.0
        },
        {
          "operation": "wait",
          "duration_s": 900.0,
          "stirring_speed_rpm": 720.0
        },
        {
          "operation": "quench"
        },
        {
          "operation": "seed_crystals",
          "seed_mass_g": 0.05
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 297.75,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 295.5,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 293.25,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 291.0,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 288.75,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 286.5,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 284.25,
          "duration_s": 14400
        },
        {
          "operation": "cool_crystallize",
          "target_temperature_K": 282.0,
          "duration_s": 14400
        },
        {
          "operation": "filter_crystals"
        },
        {
          "operation": "terminate"
        },
        {
          "operation": "measure",
          "instrument": "final_assay"
        }
      ]
    }
  ]
}
```
