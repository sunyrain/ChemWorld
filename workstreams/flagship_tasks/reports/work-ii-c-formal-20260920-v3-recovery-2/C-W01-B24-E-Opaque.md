# C-W01-B24-E-Opaque

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
      "operation": "quench"
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 7200,
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
  "end_step": 11,
  "lifecycle_index": 1,
  "metrics": {
    "byproduct_signal": 0.2484493851661682,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.4969777464866638,
    "crystal_fines_fraction": 0.9972668886184692,
    "crystal_purity": 0.9780269265174866,
    "crystal_size": 0.045833274722099304,
    "crystal_yield": 0.4710766673088074,
    "degradation_warning": 0.06985117495059967,
    "safety_risk": 0.14452829957008362,
    "score": 0.41077667474746704,
    "selectivity": 0.6131309866905212,
    "virtual_spectrum_summary": 0.1680801957845688,
    "yield": 0.6108981966972351
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
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 350
    },
    {
      "operation": "quench"
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 290
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
  "end_step": 23,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.3232932388782501,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5216390490531921,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9740626215934753,
    "crystal_size": 0.08560611307621002,
    "crystal_yield": 0.40280142426490784,
    "degradation_warning": 0.09553435444831848,
    "safety_risk": 0.15683190524578094,
    "score": 0.37696418166160583,
    "selectivity": 0.49224433302879333,
    "virtual_spectrum_summary": 0.22080174088478088,
    "yield": 0.48079684376716614
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
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 350
    },
    {
      "operation": "quench"
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 290
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
  "end_step": 35,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.28966474533081055,
    "conversion": 0.9983175992965698,
    "cost": 1.0,
    "crystal_csd_quality": 0.5473505258560181,
    "crystal_fines_fraction": 0.9949334263801575,
    "crystal_purity": 0.9838823676109314,
    "crystal_size": 0.03632403910160065,
    "crystal_yield": 0.4625895619392395,
    "degradation_warning": 0.11293269693851471,
    "safety_risk": 0.18235482275485992,
    "score": 0.40312281250953674,
    "selectivity": 0.5394130349159241,
    "virtual_spectrum_summary": 0.2101353108882904,
    "yield": 0.5385255813598633
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
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 350
    },
    {
      "operation": "quench"
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 290
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
  "end_step": 47,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.3305935859680176,
    "conversion": 0.9889960289001465,
    "cost": 1.0,
    "crystal_csd_quality": 0.4917382001876831,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.998077929019928,
    "crystal_size": 0.06424416601657867,
    "crystal_yield": 0.3802262246608734,
    "degradation_warning": 0.08773123472929001,
    "safety_risk": 0.18314893543720245,
    "score": 0.36048707365989685,
    "selectivity": 0.4638321101665497,
    "virtual_spectrum_summary": 0.22130551934242249,
    "yield": 0.45020225644111633
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 350
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
      "target_temperature_K": 290
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
  "end_step": 60,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.35195860266685486,
    "conversion": 0.9963371753692627,
    "cost": 1.0,
    "crystal_csd_quality": 0.5113844275474548,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9779541492462158,
    "crystal_size": 0.03641466796398163,
    "crystal_yield": 0.413534015417099,
    "degradation_warning": 0.1425546556711197,
    "safety_risk": 0.15708602964878082,
    "score": 0.37537530064582825,
    "selectivity": 0.4995265007019043,
    "virtual_spectrum_summary": 0.2577268183231354,
    "yield": 0.49337318539619446
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
      "catalyst": 2,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 350
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
      "target_temperature_K": 290
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
  "end_step": 73,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.33595290780067444,
    "conversion": 0.9924328923225403,
    "cost": 1.0,
    "crystal_csd_quality": 0.5229239463806152,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9927335381507874,
    "crystal_size": 0.02807026542723179,
    "crystal_yield": 0.39051681756973267,
    "degradation_warning": 0.07183682173490524,
    "safety_risk": 0.16985063254833221,
    "score": 0.36175358295440674,
    "selectivity": 0.43336018919944763,
    "virtual_spectrum_summary": 0.21710067987442017,
    "yield": 0.4352455139160156
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
      "stirring_speed_rpm": 400,
      "target_temperature_K": 350
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
      "target_temperature_K": 290
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
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.3727124333381653,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.4839577078819275,
    "crystal_fines_fraction": 0.9868521094322205,
    "crystal_purity": 0.9677659869194031,
    "crystal_size": 0.0781613364815712,
    "crystal_yield": 0.38134312629699707,
    "degradation_warning": 0.15272986888885498,
    "safety_risk": 0.18187034130096436,
    "score": 0.3533056080341339,
    "selectivity": 0.42149436473846436,
    "virtual_spectrum_summary": 0.27372029423713684,
    "yield": 0.44814127683639526
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 350
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
  "end_step": 99,
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.24316105246543884,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5355715155601501,
    "crystal_fines_fraction": 0.9869766235351562,
    "crystal_purity": 0.9806713461875916,
    "crystal_size": 0.08318790048360825,
    "crystal_yield": 0.519834041595459,
    "degradation_warning": 0.09997788816690445,
    "safety_risk": 0.1461797058582306,
    "score": 0.43573153018951416,
    "selectivity": 0.6164305210113525,
    "virtual_spectrum_summary": 0.1787286251783371,
    "yield": 0.6081011891365051
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 350
    },
    {
      "operation": "quench"
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
  "end_step": 113,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.25361061096191406,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5096614360809326,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9828848242759705,
    "crystal_size": 0.03334314748644829,
    "crystal_yield": 0.510741114616394,
    "degradation_warning": 0.09258149564266205,
    "safety_risk": 0.1461797058582306,
    "score": 0.4210984408855438,
    "selectivity": 0.594663143157959,
    "virtual_spectrum_summary": 0.1811475157737732,
    "yield": 0.6083149909973145
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 350
    },
    {
      "operation": "quench"
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 290
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
  "end_step": 127,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.24648773670196533,
    "conversion": 0.9857847094535828,
    "cost": 1.0,
    "crystal_csd_quality": 0.47322019934654236,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9792916774749756,
    "crystal_size": 0.04791948199272156,
    "crystal_yield": 0.5358936786651611,
    "degradation_warning": 0.10398784279823303,
    "safety_risk": 0.14783336222171783,
    "score": 0.4218626320362091,
    "selectivity": 0.6057440638542175,
    "virtual_spectrum_summary": 0.18236277997493744,
    "yield": 0.6146467924118042
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 350
    },
    {
      "operation": "quench"
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
      "target_temperature_K": 295
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 275
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 295
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
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.25500231981277466,
    "conversion": 0.9989808797836304,
    "cost": 1.0,
    "crystal_csd_quality": 0.4934369623661041,
    "crystal_fines_fraction": 0.9936863780021667,
    "crystal_purity": 0.9937962889671326,
    "crystal_size": 0.05251210927963257,
    "crystal_yield": 0.5028205513954163,
    "degradation_warning": 0.08100786805152893,
    "safety_risk": 0.1461797058582306,
    "score": 0.42171621322631836,
    "selectivity": 0.6228415966033936,
    "virtual_spectrum_summary": 0.17670482397079468,
    "yield": 0.6033276319503784
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 400,
      "target_temperature_K": 350
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
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.23900386691093445,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5059124231338501,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9931138753890991,
    "crystal_size": 0.07175098359584808,
    "crystal_yield": 0.43546783924102783,
    "degradation_warning": 0.10276627540588379,
    "safety_risk": 0.14087149500846863,
    "score": 0.40809622406959534,
    "selectivity": 0.6022728085517883,
    "virtual_spectrum_summary": 0.17769694328308105,
    "yield": 0.6072907447814941
  },
  "ordinal": 12
}
```

## Batch 13

```json
{
  "actions": [
    {
      "amount_mol": 0.02,
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
      "stirring_speed_rpm": 400,
      "target_temperature_K": 350
    },
    {
      "operation": "quench"
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
  "end_step": 169,
  "lifecycle_index": 13,
  "metrics": {
    "byproduct_signal": 0.20312802493572235,
    "conversion": 0.9971218705177307,
    "cost": 1.0,
    "crystal_csd_quality": 0.5098481178283691,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9812830090522766,
    "crystal_size": 0.06066616252064705,
    "crystal_yield": 0.5085164308547974,
    "degradation_warning": 0.10822458565235138,
    "safety_risk": 0.09114354103803635,
    "score": 0.4465506374835968,
    "selectivity": 0.7168381214141846,
    "virtual_spectrum_summary": 0.1604214757680893,
    "yield": 0.7087579965591431
  },
  "ordinal": 13
}
```

## Batch 14

```json
{
  "actions": [
    {
      "amount_mol": 0.03,
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
      "stirring_speed_rpm": 400,
      "target_temperature_K": 350
    },
    {
      "operation": "quench"
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
  "end_step": 182,
  "lifecycle_index": 14,
  "metrics": {
    "byproduct_signal": 0.2384112924337387,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.5172263979911804,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9650946855545044,
    "crystal_size": 0.0923738181591034,
    "crystal_yield": 0.5156939029693604,
    "degradation_warning": 0.10567911714315414,
    "safety_risk": 0.11940418928861618,
    "score": 0.4366998076438904,
    "selectivity": 0.6550177931785583,
    "virtual_spectrum_summary": 0.17868180572986603,
    "yield": 0.6487912535667419
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
      "volume_L": 0.08
    },
    {
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 14400,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 330
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
  "lifecycle_index": 15,
  "metrics": {
    "byproduct_signal": 0.38234755396842957,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.47892412543296814,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9719948768615723,
    "crystal_size": 0.06482553482055664,
    "crystal_yield": 0.28744155168533325,
    "degradation_warning": 0.1547209918498993,
    "safety_risk": 0.12193913012742996,
    "score": 0.3281022906303406,
    "selectivity": 0.42202621698379517,
    "virtual_spectrum_summary": 0.27991560101509094,
    "yield": 0.42656075954437256
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
      "volume_L": 0.08
    },
    {
      "catalyst": 2,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 350
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
  "lifecycle_index": 16,
  "metrics": {
    "byproduct_signal": 0.31747180223464966,
    "conversion": 0.9885532855987549,
    "cost": 1.0,
    "crystal_csd_quality": 0.45629096031188965,
    "crystal_fines_fraction": 0.9878438711166382,
    "crystal_purity": 0.9633278250694275,
    "crystal_size": 0.06288802623748779,
    "crystal_yield": 0.3177620470523834,
    "degradation_warning": 0.08617354929447174,
    "safety_risk": 0.12518347799777985,
    "score": 0.3346502184867859,
    "selectivity": 0.4511859714984894,
    "virtual_spectrum_summary": 0.213387593626976,
    "yield": 0.4495403468608856
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
      "catalyst": 3,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 350
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
  "lifecycle_index": 17,
  "metrics": {
    "byproduct_signal": 0.34128671884536743,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.49069130420684814,
    "crystal_fines_fraction": 0.9720399379730225,
    "crystal_purity": 0.9885940551757812,
    "crystal_size": 0.04914303123950958,
    "crystal_yield": 0.4012448191642761,
    "degradation_warning": 0.17127910256385803,
    "safety_risk": 0.13461922109127045,
    "score": 0.38202813267707825,
    "selectivity": 0.5215652585029602,
    "virtual_spectrum_summary": 0.2647832930088043,
    "yield": 0.5317233204841614
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
      "stirring_speed_rpm": 100,
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
    "byproduct_signal": 0.30288639664649963,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.49482154846191406,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9934183359146118,
    "crystal_size": 0.09991294890642166,
    "crystal_yield": 0.40348392724990845,
    "degradation_warning": 0.16369570791721344,
    "safety_risk": 0.1367478221654892,
    "score": 0.3943629264831543,
    "selectivity": 0.5611922144889832,
    "virtual_spectrum_summary": 0.2402505874633789,
    "yield": 0.5745991468429565
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
      "solvent": 0,
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
      "stirring_speed_rpm": 100,
      "target_temperature_K": 350
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
  "end_step": 259,
  "lifecycle_index": 19,
  "metrics": {
    "byproduct_signal": 0.32370731234550476,
    "conversion": 0.9909035563468933,
    "cost": 1.0,
    "crystal_csd_quality": 0.5017421841621399,
    "crystal_fines_fraction": 0.9774991869926453,
    "crystal_purity": 0.971617579460144,
    "crystal_size": 0.03835631534457207,
    "crystal_yield": 0.41256165504455566,
    "degradation_warning": 0.15839648246765137,
    "safety_risk": 0.13630253076553345,
    "score": 0.38510313630104065,
    "selectivity": 0.5440162420272827,
    "virtual_spectrum_summary": 0.24931743741035461,
    "yield": 0.5476030111312866
  },
  "ordinal": 19
}
```

## Batch 20

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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 100,
      "target_temperature_K": 350
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
  "end_step": 275,
  "lifecycle_index": 20,
  "metrics": {
    "byproduct_signal": 0.2899327576160431,
    "conversion": 0.9934653639793396,
    "cost": 1.0,
    "crystal_csd_quality": 0.4395931661128998,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9818012118339539,
    "crystal_size": 0.04687775298953056,
    "crystal_yield": 0.19328229129314423,
    "degradation_warning": 0.2038801908493042,
    "safety_risk": 0.05670064687728882,
    "score": 0.3505677282810211,
    "selectivity": 0.7014821767807007,
    "virtual_spectrum_summary": 0.2512091100215912,
    "yield": 0.6851601600646973
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
      "solvent": 0,
      "volume_L": 0.06
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 100,
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
  "end_step": 290,
  "lifecycle_index": 21,
  "metrics": {
    "byproduct_signal": 0.3003174662590027,
    "conversion": 0.9894089102745056,
    "cost": 1.0,
    "crystal_csd_quality": 0.5419859290122986,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9922380447387695,
    "crystal_size": 0.02740977331995964,
    "crystal_yield": 0.4425583481788635,
    "degradation_warning": 0.16340386867523193,
    "safety_risk": 0.14447353780269623,
    "score": 0.40439504384994507,
    "selectivity": 0.552290141582489,
    "virtual_spectrum_summary": 0.23870635032653809,
    "yield": 0.5715673565864563
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
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.020000000000000004
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 100,
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
  "end_step": 306,
  "lifecycle_index": 22,
  "metrics": {
    "byproduct_signal": 0.32217079401016235,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.46544429659843445,
    "crystal_fines_fraction": 0.998578667640686,
    "crystal_purity": 0.9968773126602173,
    "crystal_size": 0.048030588775873184,
    "crystal_yield": 0.37791115045547485,
    "degradation_warning": 0.16103537380695343,
    "safety_risk": 0.1323174685239792,
    "score": 0.3752255439758301,
    "selectivity": 0.5543907880783081,
    "virtual_spectrum_summary": 0.24965985119342804,
    "yield": 0.5556692481040955
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
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 14400,
      "operation": "heat",
      "stirring_speed_rpm": 100,
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
  "end_step": 323,
  "lifecycle_index": 23,
  "metrics": {
    "byproduct_signal": 0.4243772327899933,
    "conversion": 0.9950222373008728,
    "cost": 1.0,
    "crystal_csd_quality": 0.48263517022132874,
    "crystal_fines_fraction": 0.9659817814826965,
    "crystal_purity": 0.9911158084869385,
    "crystal_size": 0.07491874694824219,
    "crystal_yield": 0.2991332709789276,
    "degradation_warning": 0.2172486037015915,
    "safety_risk": 0.12283851951360703,
    "score": 0.34160974621772766,
    "selectivity": 0.4334111511707306,
    "virtual_spectrum_summary": 0.33116936683654785,
    "yield": 0.43516936898231506
  },
  "ordinal": 23
}
```

## Batch 24

```json
{
  "actions": [
    {
      "amount_mol": 0.02,
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
      "duration_s": 14400,
      "operation": "heat",
      "stirring_speed_rpm": 100,
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
  "end_step": 341,
  "lifecycle_index": 24,
  "metrics": {
    "byproduct_signal": 0.4153490960597992,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.42184242606163025,
    "crystal_fines_fraction": 1.0,
    "crystal_purity": 0.9996579885482788,
    "crystal_size": 0.06000741198658943,
    "crystal_yield": 0.2941463887691498,
    "degradation_warning": 0.26535630226135254,
    "safety_risk": 0.07977209240198135,
    "score": 0.3479200303554535,
    "selectivity": 0.5355314612388611,
    "virtual_spectrum_summary": 0.34785234928131104,
    "yield": 0.5447812676429749
  },
  "ordinal": 24
}
```

## K1

```json
{
  "payload": {
    "report": "## Mechanistic account\n\n### Scope and material identities\nThe catalyst and solvent labels are anonymous benchmark identities, so conclusions apply only to C0\u2013C3 and S0\u2013S3 within this campaign. They should not be mapped onto real chemicals.\n\n### Observed material effects\n**Solvent was important to reaction selectivity and crystallization recovery.** Under broadly comparable C0 reaction conditions, S0 performed better than S1\u2013S3. Batch 1 (S0/C0) gave reaction yield 0.611 and crystallization recovery 0.471. Batches 2\u20134 using S1, S2, and S3 gave reaction yields 0.481, 0.539, and 0.450 and crystal recoveries 0.403, 0.463, and 0.380, respectively. Stirring and crystallization histories were not perfectly identical, so the solvent ranking is suggestive rather than a clean factorial estimate.\n\n**C1 was the most useful catalyst in the S0 region explored.** Batch 8 (S0/C1) retained reaction yield 0.608 and increased crystal recovery to 0.520. Across S0/C1 batches 8\u201314, reaction yields were generally about 0.60\u20130.71 and crystal recovery about 0.44\u20130.54. Catalyst comparisons in other solvents were less decisive: C1/S1 in batch 5 only slightly exceeded C0/S1 in batch 2, C2/S2 in batch 6 was worse than C0/S2 in batch 3, and C3/S3 in batch 7 was similar to C0/S3 in batch 4. These comparisons remain confounded by catalyst\u2013solvent interaction and assay noise.\n\n### Reaction mechanism and concentration dependence\nA useful empirical relationship was\n\n`reaction yield \u2248 conversion \u00d7 selectivity`.\n\nConversion was usually near unity, making selectivity\u2014not conversion\u2014the main reaction limitation. For example, batch 1 had conversion 1.000, selectivity 0.613, and yield 0.611. Batch 13 had conversion 0.997, selectivity 0.717, and yield 0.709.\n\nLower reagent concentration improved reaction selectivity in the S0/C1 region. With 0.02 mol reagent in 0.08 L, batch 13 reached yield 0.709, compared with approximately 0.608\u20130.615 for 0.04 mol batches 8\u201310; the intermediate 0.03 mol batch 14 gave yield 0.649. My interpretation is that dilution suppressed a bimolecular or concentration-sensitive byproduct pathway. An alternative explanation is a change in catalyst-to-substrate ratio, because catalyst charge was held at 0.005 mol. A catalyst-loading factorial was not performed, so those hypotheses remain unresolved.\n\nLong reaction exposure could reverse this benefit. Batch 24 used 0.02 mol reagent with S0/C1 but heated for 14,400 s at 330 K; its final reaction yield was only 0.545, selectivity 0.536, and degradation warning 0.265. In comparison, batch 13 used a much shorter 3,600 s treatment at 350 K and had yield 0.709 and degradation warning 0.108. This supports a process-history interpretation: once conversion is essentially complete, extra thermal residence promotes impurity/degradation formation rather than useful conversion. Temperature and time were changed together, so a separate temperature-versus-residence-time mechanism was not identified.\n\n### Reaction\u2013crystallization coupling\nThe crystallization recovery was defined as seed-excluded recovered target divided by target present before separation. It is therefore distinct from reaction yield. A useful approximate overall material relationship is\n\n`target recovered from feed \u2248 reaction yield \u00d7 crystal recovery`.\n\nThus batch 8 corresponds to roughly 0.608 \u00d7 0.520 \u2248 0.316 recovered target per unit limiting reagent, whereas batch 13 corresponds to roughly 0.709 \u00d7 0.509 \u2248 0.360. However, the stated optimization objective concerns the crystallization-stage recovery itself, so improved reaction yield does not automatically improve the primary recovery metric.\n\nDilution improved the reaction more clearly than it improved crystallization recovery: batches 13 and 14 had better reaction yields but crystal recoveries of 0.509 and 0.516, close to batch 8's 0.520. This indicates that the separation was governed mainly by solvent/temperature history and solid-state kinetics rather than simply by how much target was produced.\n\n### Crystallization history\nCooling depth affected recovery in the expected direction, but not fines control. Batch 12 used a relatively warm 300-to-290 K history and gave crystal recovery 0.435. Batch 10 used deep cooling to 250 K followed by reheating to 290 K and recooling to 260 K; recovery increased to 0.536. The likely interpretation is a lower equilibrium solubility at the colder endpoint.\n\nThermal cycling did not produce the hoped-for selective dissolution and regrowth of fines. Batch 9 used cooling to 270 K, reheating to 295 K, holding, and recooling; it gave recovery 0.511 but final fines fraction 1.000. Batch 11 used two reheating/recooling cycles and gave recovery 0.503 with fines 0.994. These results do not rule out a narrower optimized temperature cycle, but the tested cycles did not deliver effective Ostwald ripening.\n\nBatch 8 used a gradual 300\u2192285\u2192270 K sequence with long holds and no added seed. It produced recovery 0.520, purity 0.981, normalized crystal size 0.083, and fines 0.987. Because normalized size is `min(d50/250 \u00b5m, 1)`, the assay size corresponds to a d50 of about 21 \u00b5m. Batch 1, with 0.05 g seed and a faster single cooling step, had normalized size 0.046 (about 11 \u00b5m), recovery 0.471, and fines 0.997. This is consistent with slower staged cooling and avoiding excessive nuclei improving growth somewhat, but it is not proof of a seed effect because several variables changed together.\n\n### Quality/recovery tradeoff and recommendation\nPurity was not the binding constraint. In the documented batches it was generally about 0.965\u20131.000, comfortably above the required 0.80. The unresolved limitation was particle-number fines: final-assay fines fractions remained approximately 0.987\u20131.000, far above the required 0.50.\n\nBatch 10 had the largest observed crystal recovery among the closely documented S0/C1 histories, 0.536, but its fines fraction was 1.000. Batch 8 had slightly lower recovery, 0.520, but combined it with purity 0.981, the largest useful observed size in that comparison, and fines 0.987. For that reason, the sealed recommendation remains **batch 8** as the strongest observed compromise. It is not a constraint-feasible solution, and no completed batch met the fines specification.\n\n### Revisions and uncertainty\nThe campaign progressed from broad solvent/catalyst screening to S0/C1 concentration studies, staged cooling, long aging, seeding changes, low stirring, and thermal cycling. Early expectations that long holds or reheating would eliminate fines were revised after batches 9\u201312 and the later long-history experiments failed to do so. Batch 24, despite low stirring, staged cooling, seeding, and extensive aging, still gave fines 1.000 and recovery only 0.294.\n\nFinal-assay standard uncertainties were approximately 0.010 for crystal recovery, 0.010 for purity, 0.018 for fines, and 0.025 for normalized size. Consequently, differences such as fines 0.987 versus 1.000 are not statistically decisive. Prefilter particle imaging and final assays also differed: for batch 8 the particle measurement reported fines 0.999 and size 0.040, whereas the final assay reported 0.987 and 0.083. This reinforces that the modest apparent particle-size improvements should be treated cautiously.\n\nUntested alternatives include a designed catalyst-loading study at fixed substrate concentration, narrower seeding-temperature windows, much smaller controlled supersaturation increments, alternative isolation methods that selectively remove fines, and a true residence-time series at fixed temperature. These are mechanistically plausible next tests, not conclusions supported by the completed campaign."
  },
  "failure": null,
  "elapsed_s": 61.07799999997951,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 989312,
    "input_tokens": 1148634,
    "output_tokens": 11304,
    "reasoning_output_tokens": 5203
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
          "estimate": 0.36,
          "lower80": 0.18,
          "upper80": 0.58
        },
        "crystal_purity": {
          "estimate": 0.97,
          "lower80": 0.93,
          "upper80": 0.995
        },
        "crystal_size": {
          "estimate": 0.13,
          "lower80": 0.075,
          "upper80": 0.21
        },
        "crystal_yield": {
          "estimate": 0.38,
          "lower80": 0.28,
          "upper80": 0.49
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q01"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.43,
          "lower80": 0.22,
          "upper80": 0.66
        },
        "crystal_purity": {
          "estimate": 0.985,
          "lower80": 0.95,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.105,
          "lower80": 0.055,
          "upper80": 0.18
        },
        "crystal_yield": {
          "estimate": 0.33,
          "lower80": 0.23,
          "upper80": 0.44
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q02"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.46,
          "lower80": 0.22,
          "upper80": 0.71
        },
        "crystal_purity": {
          "estimate": 0.98,
          "lower80": 0.945,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.16,
          "lower80": 0.075,
          "upper80": 0.27
        },
        "crystal_yield": {
          "estimate": 0.47,
          "lower80": 0.36,
          "upper80": 0.58
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q03"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.28,
          "lower80": 0.12,
          "upper80": 0.5
        },
        "crystal_purity": {
          "estimate": 0.982,
          "lower80": 0.95,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.14,
          "lower80": 0.085,
          "upper80": 0.22
        },
        "crystal_yield": {
          "estimate": 0.49,
          "lower80": 0.39,
          "upper80": 0.59
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q04"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.24,
          "lower80": 0.1,
          "upper80": 0.44
        },
        "crystal_purity": {
          "estimate": 0.983,
          "lower80": 0.952,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.155,
          "lower80": 0.095,
          "upper80": 0.24
        },
        "crystal_yield": {
          "estimate": 0.49,
          "lower80": 0.39,
          "upper80": 0.59
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q05"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.82,
          "lower80": 0.61,
          "upper80": 0.97
        },
        "crystal_purity": {
          "estimate": 0.955,
          "lower80": 0.9,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.055,
          "lower80": 0.02,
          "upper80": 0.105
        },
        "crystal_yield": {
          "estimate": 0.5,
          "lower80": 0.39,
          "upper80": 0.61
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q06"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.22,
          "lower80": 0.09,
          "upper80": 0.41
        },
        "crystal_purity": {
          "estimate": 0.984,
          "lower80": 0.954,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.17,
          "lower80": 0.105,
          "upper80": 0.26
        },
        "crystal_yield": {
          "estimate": 0.5,
          "lower80": 0.4,
          "upper80": 0.6
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q07"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.67,
          "lower80": 0.4,
          "upper80": 0.9
        },
        "crystal_purity": {
          "estimate": 0.96,
          "lower80": 0.91,
          "upper80": 0.995
        },
        "crystal_size": {
          "estimate": 0.07,
          "lower80": 0.025,
          "upper80": 0.14
        },
        "crystal_yield": {
          "estimate": 0.35,
          "lower80": 0.22,
          "upper80": 0.49
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q08"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.93,
          "lower80": 0.78,
          "upper80": 1.0
        },
        "crystal_purity": {
          "estimate": 0.92,
          "lower80": 0.82,
          "upper80": 0.98
        },
        "crystal_size": {
          "estimate": 0.035,
          "lower80": 0.01,
          "upper80": 0.075
        },
        "crystal_yield": {
          "estimate": 0.02,
          "lower80": 0.002,
          "upper80": 0.06
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q09"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.73,
          "lower80": 0.48,
          "upper80": 0.93
        },
        "crystal_purity": {
          "estimate": 0.95,
          "lower80": 0.88,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.065,
          "lower80": 0.025,
          "upper80": 0.13
        },
        "crystal_yield": {
          "estimate": 0.14,
          "lower80": 0.06,
          "upper80": 0.25
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q10"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.26,
          "lower80": 0.11,
          "upper80": 0.47
        },
        "crystal_purity": {
          "estimate": 0.982,
          "lower80": 0.95,
          "upper80": 1.0
        },
        "crystal_size": {
          "estimate": 0.15,
          "lower80": 0.09,
          "upper80": 0.235
        },
        "crystal_yield": {
          "estimate": 0.49,
          "lower80": 0.39,
          "upper80": 0.59
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q11"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.58,
          "lower80": 0.34,
          "upper80": 0.8
        },
        "crystal_purity": {
          "estimate": 0.96,
          "lower80": 0.91,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.085,
          "lower80": 0.04,
          "upper80": 0.155
        },
        "crystal_yield": {
          "estimate": 0.58,
          "lower80": 0.47,
          "upper80": 0.69
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q12"
      }
    ],
    "rationale": "Q01\u2013Q02: prior solvent screening favored S1 over S3 for recovery, while S3 tended toward slightly higher purity; particle differences remain uncertain. Q03\u2013Q04: sparse seeding should permit more growth per primary seed but risks secondary nucleation, whereas heavier seeding better controls supersaturation and fines. Q05\u2013Q06: the gradual 300\u2192278 K ramp should strongly suppress nucleation relative to an immediate crash; their long low-temperature exposure makes equilibrium recovery similar, but particle quality should differ sharply. Q07\u2013Q08: the final 315 K excursion likely redissolves part of the crop, and the rapid recool should regenerate fines; campaign thermal cycles did not show reliable ripening. Q09\u2013Q10: particles are present because seeds were charged, but 60 seconds gives negligible seed-excluded recovery; a 2-hour hold permits some growth without approaching the long-ramp result. Q11\u2013Q12: doubling reagent concentration should increase recovery through greater supersaturation, but also increases secondary nucleation and impurity inclusion, creating a recovery/fines tradeoff. Intervals are deliberately broad because these recipes use much finer, longer cooling ramps and different scale/loadings than the campaign; particle predictions are substantially more uncertain than purity."
  },
  "failure": null,
  "elapsed_s": 81.51600000000326,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 989312,
    "input_tokens": 1237672,
    "output_tokens": 15575,
    "reasoning_output_tokens": 7791
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
    "report": "## 1. Status of the main claims\n\n### Supported by direct observations\n- **Conversion was usually saturated, leaving selectivity as the main reaction limitation.** Batch 1 had conversion 1.000, selectivity 0.613, and yield 0.611; batch 13 had 0.997, 0.717, and 0.709. Thus `reaction yield \u2248 conversion \u00d7 selectivity` was directly supported over the observed range.\n- **Purity was not the binding constraint; fines were.** Documented final purities were generally about 0.965\u20131.000, while fines were about 0.987\u20131.000. No completed batch met fines \u22640.50.\n- **S0 was the strongest observed solvent region.** With C0, batch 1 using S0 gave reaction yield 0.611 and crystal recovery 0.471, versus batches 2\u20134 using S1\u2013S3 with reaction yields 0.481, 0.539, and 0.450 and recoveries 0.403, 0.463, and 0.380. This is an observed association, not an isolated solvent effect, because stirring and crystallization histories differed.\n- **Lower reagent charge was associated with higher reaction selectivity in the S0/C1 region.** Batch 13 at 0.02 mol gave selectivity 0.717 and yield 0.709; batch 14 at 0.03 mol gave 0.655 and 0.649; batches 8\u201312 at 0.04 mol were generally near 0.60\u20130.62 yield. Catalyst-to-substrate ratio changed at the same time, so dilution is an interpretation rather than a demonstrated cause.\n- **Deeper cooling was associated with greater recovery.** Warm-ended batch 12 recovered 0.435, whereas deep-cool/reheat batch 10 recovered 0.536. The direction is consistent with lower solubility at lower temperature, although their full histories were not identical.\n- **The tested thermal cycles did not solve the fines problem.** Batches 9\u201311 retained fines of approximately 0.994\u20131.000 despite reheating and recooling. Batch 24 also retained fines 1.000 after extensive staged cooling and aging.\n\n### Supported, but only as interpretations\n- **C1 was the most useful catalyst in the explored S0 region.** Repeated S0/C1 batches 8\u201314 performed well, and batch 8 reached recovery 0.520. However, batch 1 versus batch 8 was not a clean C0/C1 comparison: seed, stirring, and cooling history also changed.\n- **A concentration-sensitive byproduct pathway may explain the batch 13\u201314 trend.** This is plausible, but an increased catalyst-to-substrate ratio or altered crystallization feed composition could explain the same observations.\n- **Excess thermal residence promotes degradation after conversion is complete.** Batch 24 had yield 0.545 and degradation warning 0.265, versus batch 13 at yield 0.709 and warning 0.108. This supports a history effect, but temperature, residence time, seeding, and downstream duration were all different.\n- **Batch 8\u2019s staged cooling and lack of seed may have improved growth.** Relative to batch 1, batch 8 increased normalized size from 0.046 to 0.083 and recovery from 0.471 to 0.520. The comparison does not identify whether cooling rate, seed mass, stirring, catalyst, or their interaction caused the change.\n\n### Contradicted or weakened\n- **The initial expectation that long holds or moderate reheating would ripen away fines was contradicted.** Batches 9\u201311 and 24 showed no practically meaningful fines reduction.\n- **A simple claim that dilution always improves the whole process was contradicted by batch 24.** Its low charge did not preserve the high selectivity seen in batch 13. Dilution therefore interacts with thermal history and catalyst ratio rather than acting independently.\n\n### Still untested\n- Whether dilution or catalyst-to-substrate ratio caused the batch 13 improvement.\n- A matched C0-versus-C1 comparison at identical S0 conditions.\n- Whether genuinely fine-grained, near-continuous cooling can cross the fines threshold; the campaign used much coarser temperature changes than the held-out recipes.\n- Whether seed mass suppresses secondary nucleation or merely increases the number-weighted seed population. Existing seed comparisons changed several other variables.\n- Selective fines removal during isolation and a systematic temperature\u2013time reaction study.\n\n## 2. One additional experiment\n\nI would run one **instrumented, finely stepped S0/C1 seeded cooling experiment** from the original state: 0.004 mol reagent, 0.020 L S0, 0.00025 mol C1, the specified 385 K reaction/quench sequence, 0.045 g seed at 300 K, followed by approximately 1 K cooling increments every four hours to 278.15 K. I would take non-destructive particle-size measurements near 295, 289, 283, and 278 K, then filter and perform the final assay.\n\nThis would distinguish three competing explanations:\n\n1. **Coarse supersaturation jumps caused the campaign\u2019s fines.** Expected result: size grows progressively, fines remain below 0.50, and final recovery is roughly in the 0.4\u20130.5 region.\n2. **Secondary nucleation is intrinsically strong even under slow cooling.** Expected result: fines rise toward 0.9\u20131.0 during the ramp, with only modest size growth despite adequate recovery.\n3. **The seed population or measurement context dominates the reported particle metrics.** Expected result: fines are already high at the first measurement, or in-process imaging appears acceptable but the final assay again reports much higher fines or a materially different size.\n\nThe intermediate measurements are essential: one endpoint alone could not distinguish immediate seed-related fines from late supersaturation-driven nucleation or an assay-context discrepancy.\n\n## 3. Least-used observation and least-reliable prediction\n\nThe observation used least effectively was the **disagreement between batch 8\u2019s in-process particle measurement and its final assay**. The particle measurement gave fines 0.999 and normalized size 0.040, whereas the final assay gave fines 0.987 and size 0.083. The account mentioned this as uncertainty but did not incorporate a phase-, timing-, or instrument-specific bias model. That omission matters because the held-out predictions assigned substantial probability to fines below 0.50 even though every campaign endpoint remained near 1.0.\n\nThe least reliable held-out prediction is **Q03**. It combined a very small seed charge, a much finer and longer cooling ramp than any clean campaign analogue, and a point estimate for fines of 0.46\u2014almost exactly at the feasibility boundary. The campaign did not isolate seed mass at this scale, and the mechanism has competing signs: sparse seeding could allow large crystals to grow, or it could fail to consume supersaturation and trigger a burst of secondary nuclei. Its stated 80% fines interval of 0.22\u20130.71 appropriately crossed the threshold, but even that interval rests on extrapolation rather than a directly calibrated seed\u2013cooling model."
  },
  "failure": null,
  "elapsed_s": 55.296999999991385,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 1066496,
    "input_tokens": 1330901,
    "output_tokens": 18281,
    "reasoning_output_tokens": 8926
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
    "selection_rationale": "No completed batch met the fines constraint (<=0.50). Batch 8 was the strongest observed compromise: crystal_yield 0.5198, crystal_purity 0.9807, and fines 0.9870; it retained high recovery and purity despite the unresolved fines failure."
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
        "catalyst": 1,
        "catalyst_amount_mol": 0.005,
        "operation": "add_catalyst"
      },
      {
        "duration_s": 3600,
        "operation": "heat",
        "stirring_speed_rpm": 400,
        "target_temperature_K": 350
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
    "excluded_rejected_attempts": [],
    "lifecycle_index": 8,
    "source_attempts": 13
  },
  "prediction_evaluation": {
    "contrasts": [
      {
        "absolute_delta_error": 0.022940623437742474,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_yield",
        "predicted_delta": -0.04999999999999999,
        "resolved": true,
        "true_delta": -0.07294062343774246
      },
      {
        "absolute_delta_error": 0.016253877452758303,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_purity",
        "predicted_delta": 0.015000000000000013,
        "resolved": false,
        "true_delta": -0.0012538774527582897
      },
      {
        "absolute_delta_error": 0.040653301928301994,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_size",
        "predicted_delta": -0.02500000000000001,
        "resolved": true,
        "true_delta": 0.015653301928301985
      },
      {
        "absolute_delta_error": 0.5132152850558221,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.07,
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
        "absolute_delta_error": 0.006132470445263327,
        "direction_correct": true,
        "factor": "seed",
        "metric": "crystal_purity",
        "predicted_delta": 0.0020000000000000018,
        "resolved": false,
        "true_delta": 0.008132470445263329
      },
      {
        "absolute_delta_error": 0.020422495607400712,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_size",
        "predicted_delta": -0.01999999999999999,
        "resolved": false,
        "true_delta": 0.0004224956074007219
      },
      {
        "absolute_delta_error": 0.15517376032701968,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.18,
        "resolved": false,
        "true_delta": -0.02482623967298031
      },
      {
        "absolute_delta_error": 0.009767182469520963,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_yield",
        "predicted_delta": 0.010000000000000009,
        "resolved": false,
        "true_delta": 0.00023281753047904585
      },
      {
        "absolute_delta_error": 0.023209363860740795,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.028000000000000025,
        "resolved": false,
        "true_delta": -0.00479063613925923
      },
      {
        "absolute_delta_error": 0.0607945906364231,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_size",
        "predicted_delta": -0.1,
        "resolved": true,
        "true_delta": -0.03920540936357691
      },
      {
        "absolute_delta_error": 0.09637716023803633,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.58,
        "resolved": true,
        "true_delta": 0.6763771602380363
      },
      {
        "absolute_delta_error": 0.19156172818020112,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_yield",
        "predicted_delta": -0.15000000000000002,
        "resolved": true,
        "true_delta": 0.041561728180201096
      },
      {
        "absolute_delta_error": 0.01473583293460301,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.02400000000000002,
        "resolved": false,
        "true_delta": -0.009264167065397011
      },
      {
        "absolute_delta_error": 0.06955626788314162,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_size",
        "predicted_delta": -0.1,
        "resolved": true,
        "true_delta": -0.030443732116858392
      },
      {
        "absolute_delta_error": 0.2461786076870266,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.45000000000000007,
        "resolved": true,
        "true_delta": 0.6961786076870267
      },
      {
        "absolute_delta_error": 0.03072767781178036,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_yield",
        "predicted_delta": 0.12000000000000001,
        "resolved": true,
        "true_delta": 0.15072767781178037
      },
      {
        "absolute_delta_error": 0.04407302371933752,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_purity",
        "predicted_delta": 0.029999999999999916,
        "resolved": true,
        "true_delta": -0.014073023719337607
      },
      {
        "absolute_delta_error": 0.015124201609462394,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_size",
        "predicted_delta": 0.03,
        "resolved": true,
        "true_delta": 0.014875798390537605
      },
      {
        "absolute_delta_error": 0.22026443684698094,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.20000000000000007,
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
        "absolute_delta_error": 0.01597633258618314,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_purity",
        "predicted_delta": -0.02200000000000002,
        "resolved": false,
        "true_delta": -0.00602366741381688
      },
      {
        "absolute_delta_error": 0.037436293373212796,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_size",
        "predicted_delta": -0.06499999999999999,
        "resolved": true,
        "true_delta": -0.027563706626787192
      },
      {
        "absolute_delta_error": 0.36857898286242896,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.31999999999999995,
        "resolved": true,
        "true_delta": 0.6885789828624289
      }
    ],
    "failures": [],
    "metrics": {
      "crystal_fines_fraction": {
        "coverage80": 0.5833333333333334,
        "interval_score80": 0.9260749695285764,
        "interval_width": 0.3933333333333333,
        "mae": 0.17760649413691723,
        "n": 12,
        "planned": 12
      },
      "crystal_purity": {
        "coverage80": 0.9166666666666666,
        "interval_score80": 0.09009395043719681,
        "interval_width": 0.07408333333333335,
        "mae": 0.017730203888803548,
        "n": 12,
        "planned": 12
      },
      "crystal_size": {
        "coverage80": 0.5833333333333334,
        "interval_score80": 0.1619160838297367,
        "interval_width": 0.12666666666666668,
        "mae": 0.04224457412759228,
        "n": 12,
        "planned": 12
      },
      "crystal_yield": {
        "coverage80": 0.3333333333333333,
        "interval_score80": 0.8233627383524086,
        "interval_width": 0.1998333333333333,
        "mae": 0.14363591451837884,
        "n": 12,
        "planned": 12
      }
    },
    "quality": {
      "balanced_accuracy": 0.9166666666666667,
      "false_negative": 0,
      "false_positive": 1,
      "true_negative": 5,
      "true_positive": 6
    },
    "resolved_direction_correct": 10,
    "resolved_direction_n": 14,
    "tie_correct": 2,
    "tie_n": 10,
    "valid": true
  },
  "public_baselines": {
    "available": true,
    "mae": {
      "public_mean": {
        "crystal_fines_fraction": 0.34531752610441036,
        "crystal_purity": 0.0048204030418712756,
        "crystal_size": 0.019172650467519807,
        "crystal_yield": 0.15718255372255543
      },
      "public_nearest_neighbor": {
        "crystal_fines_fraction": 0.34771492468022025,
        "crystal_purity": 0.012878135030100915,
        "crystal_size": 0.019951895565436223,
        "crystal_yield": 0.08053717850704849
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
        "cached_input": 989312,
        "input": 1071220,
        "output": 8216,
        "stage": "source",
        "uncached_input": 81908
      },
      {
        "cached_input": 0,
        "input": 77414,
        "output": 3088,
        "stage": "K1",
        "uncached_input": 77414
      },
      {
        "cached_input": 0,
        "input": 89038,
        "output": 4271,
        "stage": "Q",
        "uncached_input": 89038
      },
      {
        "cached_input": 77184,
        "input": 93229,
        "output": 2706,
        "stage": "K2",
        "uncached_input": 16045
      }
    ],
    "total": {
      "cached_input": 1066496,
      "input": 1330901,
      "input_plus_output": 1349182,
      "output": 18281,
      "uncached_input": 264405
    },
    "valid": true
  },
  "elapsed_s": 549.7030000000086
}
```
