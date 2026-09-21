# C-W03-B12-E-MisIndexed

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
      "target_temperature_K": 278
    },
    {
      "duration_s": 14400,
      "operation": "wait",
      "stirring_speed_rpm": 250
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
    "byproduct_signal": 0.3711370527744293,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7748509645462036,
    "crystal_fines_fraction": 0.2663921117782593,
    "crystal_purity": 0.9873898029327393,
    "crystal_size": 0.08396164327859879,
    "crystal_yield": 0.42769062519073486,
    "degradation_warning": 0.19209504127502441,
    "safety_risk": 0.1812707930803299,
    "score": 0.5131430625915527,
    "selectivity": 0.5126135349273682,
    "virtual_spectrum_summary": 0.29056814312934875,
    "yield": 0.510451078414917
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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 340
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
      "target_temperature_K": 260
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
  "end_step": 22,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.2476285845041275,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7466758489608765,
    "crystal_fines_fraction": 0.3829295337200165,
    "crystal_purity": 0.9830790162086487,
    "crystal_size": 0.10480833053588867,
    "crystal_yield": 0.5090250968933105,
    "degradation_warning": 0.05616452917456627,
    "safety_risk": 0.1883922964334488,
    "score": 0.5325652360916138,
    "selectivity": 0.6026226282119751,
    "virtual_spectrum_summary": 0.16146975755691528,
    "yield": 0.5902459621429443
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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 340
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
      "target_temperature_K": 260
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
  "end_step": 32,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.29337960481643677,
    "conversion": 0.98990797996521,
    "cost": 1.0,
    "crystal_csd_quality": 0.7133803367614746,
    "crystal_fines_fraction": 0.4020978510379791,
    "crystal_purity": 0.9904663562774658,
    "crystal_size": 0.06876683235168457,
    "crystal_yield": 0.3932737410068512,
    "degradation_warning": 0.055931493639945984,
    "safety_risk": 0.17273564636707306,
    "score": 0.4714964032173157,
    "selectivity": 0.4794876277446747,
    "virtual_spectrum_summary": 0.18652796745300293,
    "yield": 0.4745762348175049
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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 340
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
      "target_temperature_K": 260
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
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.24566993117332458,
    "conversion": 0.9869914054870605,
    "cost": 1.0,
    "crystal_csd_quality": 0.6185208559036255,
    "crystal_fines_fraction": 0.6606403589248657,
    "crystal_purity": 1.0,
    "crystal_size": 0.0752529576420784,
    "crystal_yield": 0.5347687602043152,
    "degradation_warning": 0.07229717075824738,
    "safety_risk": 0.19009268283843994,
    "score": 0.48702535033226013,
    "selectivity": 0.611891508102417,
    "virtual_spectrum_summary": 0.1676521897315979,
    "yield": 0.597044050693512
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
      "solvent": 3,
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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 340
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
      "target_temperature_K": 260
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
  "end_step": 52,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.3104579448699951,
    "conversion": 0.9952210783958435,
    "cost": 1.0,
    "crystal_csd_quality": 0.6049439311027527,
    "crystal_fines_fraction": 0.6421070694923401,
    "crystal_purity": 0.9679437875747681,
    "crystal_size": 0.04959581047296524,
    "crystal_yield": 0.3964444696903229,
    "degradation_warning": 0.060491014271974564,
    "safety_risk": 0.1856231540441513,
    "score": 0.42346227169036865,
    "selectivity": 0.5017753839492798,
    "virtual_spectrum_summary": 0.19797283411026,
    "yield": 0.4950774610042572
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
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 340
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
      "target_temperature_K": 260
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
  "end_step": 62,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.260836660861969,
    "conversion": 0.9874805212020874,
    "cost": 1.0,
    "crystal_csd_quality": 0.6276792287826538,
    "crystal_fines_fraction": 0.6024136543273926,
    "crystal_purity": 0.9980607628822327,
    "crystal_size": 0.04662299156188965,
    "crystal_yield": 0.49828648567199707,
    "degradation_warning": 0.05391741544008255,
    "safety_risk": 0.1658046990633011,
    "score": 0.47549551725387573,
    "selectivity": 0.558103621006012,
    "virtual_spectrum_summary": 0.16772300004959106,
    "yield": 0.5571942329406738
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
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 340
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
      "operation": "cool_crystallize",
      "target_temperature_K": 250
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
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.24345438182353973,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7209064960479736,
    "crystal_fines_fraction": 0.36628419160842896,
    "crystal_purity": 0.9800393581390381,
    "crystal_size": 0.08967601507902145,
    "crystal_yield": 0.5503736138343811,
    "degradation_warning": 0.05689406767487526,
    "safety_risk": 0.18933558464050293,
    "score": 0.5386089086532593,
    "selectivity": 0.5845825672149658,
    "virtual_spectrum_summary": 0.15950223803520203,
    "yield": 0.6102738380432129
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
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 340
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
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
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.23576432466506958,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7601982355117798,
    "crystal_fines_fraction": 0.3706429898738861,
    "crystal_purity": 0.9800196290016174,
    "crystal_size": 0.10656559467315674,
    "crystal_yield": 0.5555052161216736,
    "degradation_warning": 0.06346194446086884,
    "safety_risk": 0.18876409530639648,
    "score": 0.5473887920379639,
    "selectivity": 0.5990870594978333,
    "virtual_spectrum_summary": 0.15822824835777283,
    "yield": 0.589851975440979
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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 340
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 310
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
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
  "end_step": 96,
  "lifecycle_index": 9,
  "metrics": {
    "byproduct_signal": 0.2462138831615448,
    "conversion": 0.9992900490760803,
    "cost": 1.0,
    "crystal_csd_quality": 0.744836151599884,
    "crystal_fines_fraction": 0.3786921203136444,
    "crystal_purity": 0.9824365377426147,
    "crystal_size": 0.05880967155098915,
    "crystal_yield": 0.5464122891426086,
    "degradation_warning": 0.056065551936626434,
    "safety_risk": 0.18876011669635773,
    "score": 0.5355948209762573,
    "selectivity": 0.5773196816444397,
    "virtual_spectrum_summary": 0.16064713895320892,
    "yield": 0.5900657773017883
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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 340
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
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
    "byproduct_signal": 0.23909100890159607,
    "conversion": 0.9842556118965149,
    "cost": 1.0,
    "crystal_csd_quality": 0.7008022665977478,
    "crystal_fines_fraction": 0.3950147330760956,
    "crystal_purity": 0.978108823299408,
    "crystal_size": 0.07097608596086502,
    "crystal_yield": 0.5475293397903442,
    "degradation_warning": 0.06747189909219742,
    "safety_risk": 0.18876409530639648,
    "score": 0.5268940329551697,
    "selectivity": 0.5884006023406982,
    "virtual_spectrum_summary": 0.16186240315437317,
    "yield": 0.5963975787162781
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
      "volume_L": 0.06
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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 340
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
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
  "end_step": 119,
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.24932228028774261,
    "conversion": 0.9988722801208496,
    "cost": 1.0,
    "crystal_csd_quality": 0.7335378527641296,
    "crystal_fines_fraction": 0.366940438747406,
    "crystal_purity": 0.9918763637542725,
    "crystal_size": 0.07748822867870331,
    "crystal_yield": 0.5435906648635864,
    "degradation_warning": 0.04782664775848389,
    "safety_risk": 0.197214737534523,
    "score": 0.5378499031066895,
    "selectivity": 0.6032847166061401,
    "virtual_spectrum_summary": 0.1586492508649826,
    "yield": 0.5837073922157288
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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 340
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.01
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 250
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
  "end_step": 129,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.23160713911056519,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7324294447898865,
    "crystal_fines_fraction": 0.38562309741973877,
    "crystal_purity": 0.994350016117096,
    "crystal_size": 0.09787648916244507,
    "crystal_yield": 0.5414417386054993,
    "degradation_warning": 0.06625033915042877,
    "safety_risk": 0.18876409530639648,
    "score": 0.5378322005271912,
    "selectivity": 0.5849292874336243,
    "virtual_spectrum_summary": 0.15719658136367798,
    "yield": 0.589041531085968
  },
  "ordinal": 12
}
```

## K1

```json
{
  "payload": {
    "report": "Mechanistic account\n\nThe recommended process remains batch 8: 0.040 mol reagent and 0.005 mol catalyst-C0 in 0.080 L solvent-S2; heat toward 340 K for 1,800 s at 500 rpm; add 0.010 g seed; cool directly to 250 K for 14,400 s and then maintain the 250 K crystallization trajectory for another 14,400 s; filter, terminate, and assay. Batch 8 produced an observed seed-excluded crystal recovery of 0.556, purity 0.980, and fines fraction 0.371. Its replicate, batch 12, gave 0.541 recovery, 0.994 purity, and 0.386 fines, confirming feasibility while showing batch-to-batch/instrument uncertainty.\n\nMaterial effects\n\nObservation: With catalyst-C0 and broadly comparable reaction/crystallization conditions, solvent-S2 in batch 2 gave 0.509 recovery, 0.983 purity, and 0.383 fines. Solvent-S3 in batch 5 gave only 0.396 recovery and 0.642 fines; solvent-S1 in batch 6 gave 0.498 recovery but 0.602 fines. Thus S1 and S3 failed the fines constraint despite high purity. S0 was not tested.\n\nInterpretation: S2\u2019s nominal low relative solubility (0.70), high growth tendency (1.30), low nucleation tendency (0.65), and low impurity-occlusion tendency (0.65) form a coherent explanation: cooling creates substantial supersaturation, but growth on existing crystals competes effectively with secondary nucleation, while impurities are rejected from the lattice. The observed high purity and acceptable fines support this interpretation, although hidden solvent residuals and changed reaction behavior prevent assigning the result solely to those nominal properties.\n\nObservation: In the S2 catalyst comparison, C0/batch 2 gave 0.509 recovery and acceptable fines; C2/batch 3 gave 0.393 recovery; C3/batch 4 gave 0.535 recovery but 0.661 fines, violating the constraint. Batch 1 used C1 but also harsher reaction and different post-cooling history, so its 0.428 recovery cannot be treated as a controlled catalyst comparison.\n\nInterpretation: Catalyst choice altered not only conversion but the product/impurity mixture delivered to crystallization. C3 generated enough crystallizable target for high recovery, but apparently also promoted a liquor composition or supersaturation response favoring excessive nucleation. C0 provided the better constrained compromise. This is a coupling effect rather than proof that C0 is intrinsically the most active catalyst.\n\nReaction\u2013crystallization coupling\n\nA useful reaction approximation is\n\n  Y_target \u2248 X \u00d7 S_target,\n\nwhere X is conversion and S_target is selectivity. The amount of isolated target then scales as\n\n  n_isolated,target \u2248 n_feed \u00d7 Y_target \u00d7 R_cryst,\n\nwhere R_cryst is the reported seed-excluded crystallization recovery. Importantly, R_cryst is normalized to target already present before separation, so it is not the overall yield from charged reagent.\n\nThe reaction screens frequently approached complete conversion, but selectivity remained only moderate. For example, batch 2\u2019s HPLC showed conversion 0.983, selectivity 0.590, and reaction yield 0.560; its final assay showed selectivity 0.603. Batch 3 had similar conversion (0.990) but lower selectivity (0.447) and subsequently lower crystal recovery. This indicates that driving conversion alone is not sufficient: byproducts can reduce target inventory, alter solubility, promote nucleation, or become occluded. Nevertheless, final crystal purities were generally about 0.97\u20131.00, showing that crystallization efficiently rejected much of the reaction impurity burden.\n\nCrystallization can be described through supersaturation, for example\n\n  \u03c3 = C/C*(T,composition) \u2212 1,\n\nwith nucleation increasing steeply with \u03c3 while crystal growth consumes \u03c3. Cooling S2 to 250 K lowers C*, increasing recovery. Seeding supplies growth surface so that target deposition need not begin through uncontrolled primary nucleation. The observed combination of high purity and moderate fines is consistent with growth-dominated removal, but no direct concentration-versus-time data were collected, so the precise nucleation and growth laws remain unverified.\n\nProcess-history dependence and revisions\n\nBatch 2 used 0.020 g seed and one 14,400 s cooling stage to 260 K, yielding 0.509 recovery. After revising to a deeper and longer cold history, batch 7 used 0.050 g seed and two 14,400 s stages at 250 K and reached 0.550 recovery with 0.366 fines. Reducing seed to 0.010 g in batch 8 slightly improved observed recovery to 0.556 while retaining acceptable fines (0.371) and high purity. This motivated the final recommendation.\n\nThe data do not show that ever-longer cold aging is beneficial. Batch 10 added a third 14,400 s stage at 250 K but gave 0.548 recovery, 0.395 fines, and lower CSD quality than batch 8. A staged path through 310 K before 250 K in batch 9 produced 0.546 recovery and 0.379 fines, offering no clear advantage. These results suggest diminishing returns after two cold stages and possible secondary nucleation or attrition during extended processing.\n\nBatch 1 illustrates history sensitivity but is confounded: after crystallizing at 278 K, a subsequent ordinary wait allowed the vessel to warm toward ambient before filtration. It returned only 0.428 recovery. Redissolution during warming is a plausible explanation, but its C1 catalyst, 360 K/3,600 s reaction, and different degradation burden also changed, so warming cannot be isolated as the sole cause.\n\nConcentration was also tested. Batch 11 reduced S2 volume from 0.080 to 0.060 L but gave 0.544 recovery rather than improving upon batch 8. It had higher observed safety risk (about 0.197 versus 0.189) and therefore offered no demonstrated benefit. All studied batches remained well below the 0.65 safety limit.\n\nUncertainty and unresolved tradeoffs\n\nThe batch-8/12 replicate spread\u20140.556 versus 0.541 recovery, fines 0.371 versus 0.386, and CSD quality 0.760 versus 0.732\u2014shows that differences of roughly one to two percentage points in recovery should not be overinterpreted. Final-assay noise, process variation, and hidden fixed material residuals all contribute. The small apparent benefit of 0.010 g over 0.050 g seed is consequently suggestive, not conclusive.\n\nThe main unresolved tradeoff is recovery versus particle quality. C3/batch 4 achieved 0.535 recovery but excessive fines (0.661); S1/batch 6 approached 0.50 recovery but also failed on fines (0.602). Deeper/longer cooling with C0/S2 increased recovery, yet an additional cold stage did not improve it and slightly worsened fines. A slower optimized cooling ramp, alternative seed-size distribution, staged catalyst/reagent addition, or controlled low-temperature residence might improve this frontier, but these alternatives were not tested. Likewise, S0, intermediate solvent mixtures, lower catalyst loadings, and a factorial separation of reaction temperature from residence time remain untested.\n\nOverall, the evidence supports a mechanism in which C0 supplies a reasonably selective reaction mixture, S2 combines low target solubility with favorable growth and impurity rejection, and a modest seed charge plus two-stage low-temperature residence converts supersaturation primarily into crystal growth. The recommendation is robustly within the purity and fines constraints, but its approximately 0.54\u20130.56 recovery should be treated as an experimentally supported range rather than an exact optimum."
  },
  "failure": null,
  "elapsed_s": 56.375,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 461440,
    "input_tokens": 524803,
    "output_tokens": 7441,
    "reasoning_output_tokens": 1717
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
          "estimate": 0.53,
          "lower80": 0.41,
          "upper80": 0.65
        },
        "crystal_purity": {
          "estimate": 0.93,
          "lower80": 0.87,
          "upper80": 0.98
        },
        "crystal_size": {
          "estimate": 0.085,
          "lower80": 0.05,
          "upper80": 0.13
        },
        "crystal_yield": {
          "estimate": 0.25,
          "lower80": 0.14,
          "upper80": 0.37
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q01"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.41,
          "lower80": 0.3,
          "upper80": 0.53
        },
        "crystal_purity": {
          "estimate": 0.96,
          "lower80": 0.91,
          "upper80": 0.99
        },
        "crystal_size": {
          "estimate": 0.11,
          "lower80": 0.07,
          "upper80": 0.16
        },
        "crystal_yield": {
          "estimate": 0.36,
          "lower80": 0.23,
          "upper80": 0.49
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q02"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.66,
          "lower80": 0.52,
          "upper80": 0.78
        },
        "crystal_purity": {
          "estimate": 0.86,
          "lower80": 0.77,
          "upper80": 0.94
        },
        "crystal_size": {
          "estimate": 0.052,
          "lower80": 0.025,
          "upper80": 0.09
        },
        "crystal_yield": {
          "estimate": 0.18,
          "lower80": 0.08,
          "upper80": 0.3
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q03"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.47,
          "lower80": 0.35,
          "upper80": 0.6
        },
        "crystal_purity": {
          "estimate": 0.9,
          "lower80": 0.82,
          "upper80": 0.96
        },
        "crystal_size": {
          "estimate": 0.078,
          "lower80": 0.043,
          "upper80": 0.12
        },
        "crystal_yield": {
          "estimate": 0.22,
          "lower80": 0.11,
          "upper80": 0.34
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q04"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.43,
          "lower80": 0.32,
          "upper80": 0.55
        },
        "crystal_purity": {
          "estimate": 0.91,
          "lower80": 0.83,
          "upper80": 0.97
        },
        "crystal_size": {
          "estimate": 0.105,
          "lower80": 0.065,
          "upper80": 0.155
        },
        "crystal_yield": {
          "estimate": 0.24,
          "lower80": 0.13,
          "upper80": 0.36
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q05"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.61,
          "lower80": 0.48,
          "upper80": 0.73
        },
        "crystal_purity": {
          "estimate": 0.88,
          "lower80": 0.79,
          "upper80": 0.95
        },
        "crystal_size": {
          "estimate": 0.067,
          "lower80": 0.035,
          "upper80": 0.11
        },
        "crystal_yield": {
          "estimate": 0.25,
          "lower80": 0.14,
          "upper80": 0.37
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q06"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.44,
          "lower80": 0.33,
          "upper80": 0.56
        },
        "crystal_purity": {
          "estimate": 0.91,
          "lower80": 0.83,
          "upper80": 0.97
        },
        "crystal_size": {
          "estimate": 0.108,
          "lower80": 0.066,
          "upper80": 0.158
        },
        "crystal_yield": {
          "estimate": 0.25,
          "lower80": 0.14,
          "upper80": 0.37
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q07"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.34,
          "lower80": 0.24,
          "upper80": 0.46
        },
        "crystal_purity": {
          "estimate": 0.94,
          "lower80": 0.87,
          "upper80": 0.98
        },
        "crystal_size": {
          "estimate": 0.135,
          "lower80": 0.085,
          "upper80": 0.195
        },
        "crystal_yield": {
          "estimate": 0.2,
          "lower80": 0.09,
          "upper80": 0.32
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q08"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.58,
          "lower80": 0.43,
          "upper80": 0.72
        },
        "crystal_purity": {
          "estimate": 0.84,
          "lower80": 0.73,
          "upper80": 0.93
        },
        "crystal_size": {
          "estimate": 0.045,
          "lower80": 0.018,
          "upper80": 0.085
        },
        "crystal_yield": {
          "estimate": 0.012,
          "lower80": 0,
          "upper80": 0.055
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q09"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.49,
          "lower80": 0.36,
          "upper80": 0.63
        },
        "crystal_purity": {
          "estimate": 0.88,
          "lower80": 0.79,
          "upper80": 0.95
        },
        "crystal_size": {
          "estimate": 0.065,
          "lower80": 0.03,
          "upper80": 0.11
        },
        "crystal_yield": {
          "estimate": 0.08,
          "lower80": 0.025,
          "upper80": 0.17
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q10"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.45,
          "lower80": 0.33,
          "upper80": 0.57
        },
        "crystal_purity": {
          "estimate": 0.91,
          "lower80": 0.83,
          "upper80": 0.97
        },
        "crystal_size": {
          "estimate": 0.102,
          "lower80": 0.062,
          "upper80": 0.152
        },
        "crystal_yield": {
          "estimate": 0.24,
          "lower80": 0.13,
          "upper80": 0.36
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q11"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.58,
          "lower80": 0.45,
          "upper80": 0.7
        },
        "crystal_purity": {
          "estimate": 0.86,
          "lower80": 0.77,
          "upper80": 0.94
        },
        "crystal_size": {
          "estimate": 0.072,
          "lower80": 0.038,
          "upper80": 0.116
        },
        "crystal_yield": {
          "estimate": 0.42,
          "lower80": 0.28,
          "upper80": 0.56
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q12"
      }
    ],
    "rationale": "All recipes contain seed, so particles are expected even where seed-excluded product recovery is very small. Q01\u2013Q02: S3 is predicted to outperform S1 through lower nominal solubility and nucleation/occlusion tendencies, improving recovery, purity, size, and fines. Q03\u2013Q04: increasing seed mass should suppress uncontrolled S0 nucleation and improve feasibility, with only a modest recovery effect. Q05\u2013Q06: the gradual ramp should produce larger, less fine particles than an immediate quench followed by an equal long residence; final recovery is similar because endpoint temperature and total time are comparable. Q07\u2013Q08: the 315 K anneal is expected to dissolve fines and improve purity/size, but incomplete recovery during the short recooling step reduces yield. Q09\u2013Q10: two hours at 292 K allows appreciably more growth than 60 seconds, though recovery remains low because the endpoint is shallow. Q11\u2013Q12: doubling reagent concentration increases supersaturation and recovery but is expected to increase nucleation, fines, and impurity occlusion enough to lose feasibility. Uncertainty is broad because these recipes use C1/S0, much lower scale and concentration, and much longer cooling histories than the campaign; S0 was not experimentally tested, and several feasibility calls lie close to the fines threshold."
  },
  "failure": null,
  "elapsed_s": 67.21900000001187,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 461440,
    "input_tokens": 565224,
    "output_tokens": 10566,
    "reasoning_output_tokens": 3145
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
    "report": "1. Claim audit\n\nSupported by direct observation:\n- S2 was the best tested solvent under the campaign conditions. With C0, batch 2 (S2) gave 0.509 crystal recovery, 0.983 purity and 0.383 fines, versus batch 5 (S3: 0.396, 0.968, 0.642) and batch 6 (S1: 0.498, 0.998, 0.602). The interpretation that S2\u2019s nominal low solubility/high-growth properties caused this result remains inferential.\n- C0 was the best demonstrated constrained catalyst compromise. In the matched S2 screen, batch 2 met both quality limits; C2/batch 3 had lower recovery (0.393), while C3/batch 4 had higher recovery (0.535) but excessive fines (0.661). The observation is direct; attributing C3\u2019s fines specifically to its reaction-mixture composition is interpretation.\n- Conversion alone was insufficient. Batches 2 and 3 both approached complete conversion, but batch 3 had lower selectivity/reaction yield and lower crystal recovery.\n- Crystallization strongly purified the product. Final crystal purities were generally 0.97\u20131.00 despite moderate reaction selectivity and substantial byproduct signals.\n- A deeper, longer cold history was associated with better recovery: batch 2 reached 0.509 at 260 K with one cold stage, whereas batches 7 and 8 reached 0.550 and 0.556 with two stages at 250 K. This is not a clean causal isolation because seed mass and temperature also changed.\n- Additional cold residence showed diminishing returns. A third 250 K stage in batch 10 gave 0.548 recovery and 0.395 fines, not an improvement over batch 8. The staged 310-to-250 K route in batch 9 likewise did not outperform batch 8.\n- Reducing solvent volume did not help: batch 11 at 0.060 L gave 0.544 recovery and higher risk, versus 0.556 in batch 8 at 0.080 L.\n\nContradicted or weakened:\n- A simple ranking based only on nominal solvent nucleation/occlusion properties is inadequate. S3 nominally looked better than S1 for fines, yet batch 5 had slightly more fines than batch 6. Reaction\u2013solvent interactions or hidden residuals matter.\n- Any strong claim that more seed improves recovery is contradicted by the observed direction: batch 7 used 0.050 g seed and recovered 0.550, while batch 8 used 0.010 g and recovered 0.556. Conversely, the difference is too small relative to batch variability to establish that less seed is intrinsically better.\n- A monotonic claim that longer cold aging always raises recovery is contradicted by batch 10.\n\nStill untested:\n- Direct nucleation and growth kinetics, supersaturation trajectories, and whether the process is truly growth-dominated were not measured.\n- S0, solvent mixtures, seed-size distribution, and catalyst-load effects were not tested.\n- Batch 1\u2019s low recovery after warming may reflect redissolution, but C1, harsher reaction conditions and degradation were simultaneous confounders.\n- Batch 4 does not establish whether C3 intrinsically creates fines or whether a revised crystallization history could rescue its attractive recovery.\n\n2. One additional experiment\n\nI would repeat the batch-8 recipe exactly but replace C0 with C3, adding HPLC after reaction and particle-size measurement immediately before filtration. This directly addresses the unresolved recovery\u2013fines frontier using batch 8 as the historical control and batch 4 as the C3 reference.\n\nIt would distinguish two explanations:\n- Catalyst-composition mechanism: C3 generates a liquor composition that persistently promotes nucleation. Expected outcome: recovery remains approximately 0.53\u20130.57, but fines remain above 0.50, with lower CSD quality; HPLC may show a different selectivity/byproduct pattern from C0.\n- Crystallization-history/noise mechanism: batch 4\u2019s excessive fines arose mainly from its shorter, warmer crystallization history or random variation. Expected outcome: the batch-8 low-seed, two-stage 250 K treatment reduces C3 fines below 0.50 while retaining its high recovery and purity. That result could reveal a better process, though it would not alter the sealed recommendation.\n\nAn intermediate particle measurement would be especially useful because it separates actual pre-filtration particle behavior from final-assay noise.\n\n3. Least effectively used evidence and least reliable prediction\n\nThe least effectively used campaign observation was batch 1. I invoked its post-cooling warm-up as evidence for redissolution, but the batch simultaneously used C1, a 360 K/3,600 s reaction, substantial degradation, cooling only to 278 K, and an ambient-warming wait. Its low 0.428 recovery therefore cannot identify a warming effect. It was useful only as a warning about history dependence, not as causal evidence.\n\nThe least reliable held-out prediction is Q03. It combines S0\u2014which was never tested\u2014with the smallest seed charge, a much lower reaction scale/concentration, C1, and an extremely long gradual cooling schedule far outside the campaign design. Its predicted fines and feasibility depend on extrapolating nominal S0 nucleation/occlusion properties and an uncertain seed-mass effect. Q12 is also uncertain because doubling reagent may cause nonlinear supersaturation, but Q03 compounds more unsupported factors, making its recovery, fines and feasibility estimates the weakest."
  },
  "failure": null,
  "elapsed_s": 54.280999999988126,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 491008,
    "input_tokens": 608690,
    "output_tokens": 12629,
    "reasoning_output_tokens": 4006
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
    "selection_rationale": "Highest observed seed-excluded crystal recovery (0.556) among completed batches while meeting crystal purity (0.980 >= 0.80) and fines (0.371 <= 0.50) constraints; its low seed dose and extended 250 K crystallization also gave the best observed overall score."
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
        "catalyst": 0,
        "catalyst_amount_mol": 0.005,
        "operation": "add_catalyst"
      },
      {
        "duration_s": 1800,
        "operation": "heat",
        "stirring_speed_rpm": 500,
        "target_temperature_K": 340
      },
      {
        "operation": "seed_crystals",
        "seed_mass_g": 0.01
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 250
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
    "source_attempts": 11
  },
  "prediction_evaluation": {
    "contrasts": [
      {
        "absolute_delta_error": 0.2598915100154434,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_yield",
        "predicted_delta": 0.10999999999999999,
        "resolved": true,
        "true_delta": -0.14989151001544343
      },
      {
        "absolute_delta_error": 0.029354120884849233,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_purity",
        "predicted_delta": 0.029999999999999916,
        "resolved": false,
        "true_delta": 0.0006458791151506826
      },
      {
        "absolute_delta_error": 0.005619598499364983,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_size",
        "predicted_delta": 0.024999999999999994,
        "resolved": true,
        "true_delta": 0.01938040150063501
      },
      {
        "absolute_delta_error": 0.4083138299289017,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.12000000000000005,
        "resolved": true,
        "true_delta": -0.5283138299289017
      },
      {
        "absolute_delta_error": 0.04015921777357051,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_yield",
        "predicted_delta": 0.04000000000000001,
        "resolved": false,
        "true_delta": -0.00015921777357050249
      },
      {
        "absolute_delta_error": 0.03025394536462178,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_purity",
        "predicted_delta": 0.040000000000000036,
        "resolved": false,
        "true_delta": 0.009746054635378254
      },
      {
        "absolute_delta_error": 0.03318557110203587,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_size",
        "predicted_delta": 0.026000000000000002,
        "resolved": true,
        "true_delta": -0.007185571102035868
      },
      {
        "absolute_delta_error": 0.3542669082202977,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.19000000000000006,
        "resolved": true,
        "true_delta": 0.16426690822029769
      },
      {
        "absolute_delta_error": 0.009547857564826095,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_yield",
        "predicted_delta": 0.010000000000000009,
        "resolved": false,
        "true_delta": 0.0004521424351739134
      },
      {
        "absolute_delta_error": 0.026445289569308805,
        "direction_correct": false,
        "factor": "cooling_history",
        "metric": "crystal_purity",
        "predicted_delta": -0.030000000000000027,
        "resolved": false,
        "true_delta": -0.0035547104306912214
      },
      {
        "absolute_delta_error": 0.005313452665703031,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_size",
        "predicted_delta": -0.03799999999999999,
        "resolved": true,
        "true_delta": -0.04331345266570302
      },
      {
        "absolute_delta_error": 0.4429539628584593,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.18,
        "resolved": true,
        "true_delta": 0.6229539628584593
      },
      {
        "absolute_delta_error": 0.09437670725156425,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_yield",
        "predicted_delta": -0.04999999999999999,
        "resolved": true,
        "true_delta": 0.04437670725156426
      },
      {
        "absolute_delta_error": 0.04105618279419909,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_purity",
        "predicted_delta": 0.029999999999999916,
        "resolved": true,
        "true_delta": -0.011056182794199176
      },
      {
        "absolute_delta_error": 0.06670558127064301,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_size",
        "predicted_delta": 0.02700000000000001,
        "resolved": true,
        "true_delta": -0.039705581270643
      },
      {
        "absolute_delta_error": 0.7603702872401259,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.09999999999999998,
        "resolved": true,
        "true_delta": 0.6603702872401259
      },
      {
        "absolute_delta_error": 0.02651718430200213,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_yield",
        "predicted_delta": 0.068,
        "resolved": true,
        "true_delta": 0.09451718430200214
      },
      {
        "absolute_delta_error": 0.051943686041185266,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_purity",
        "predicted_delta": 0.040000000000000036,
        "resolved": true,
        "true_delta": -0.01194368604118523
      },
      {
        "absolute_delta_error": 0.006101832298345225,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_size",
        "predicted_delta": 0.020000000000000004,
        "resolved": true,
        "true_delta": 0.013898167701654779
      },
      {
        "absolute_delta_error": 0.1553927297818387,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.08999999999999997,
        "resolved": false,
        "true_delta": 0.06539272978183874
      },
      {
        "absolute_delta_error": 0.16504321303990108,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_yield",
        "predicted_delta": 0.18,
        "resolved": false,
        "true_delta": 0.014956786960098917
      },
      {
        "absolute_delta_error": 0.04482839724908727,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_purity",
        "predicted_delta": -0.050000000000000044,
        "resolved": false,
        "true_delta": -0.005171602750912774
      },
      {
        "absolute_delta_error": 0.004356873957321053,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_size",
        "predicted_delta": -0.03,
        "resolved": true,
        "true_delta": -0.025643126042678946
      },
      {
        "absolute_delta_error": 0.4759895667604082,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.12999999999999995,
        "resolved": true,
        "true_delta": 0.6059895667604082
      }
    ],
    "failures": [],
    "metrics": {
      "crystal_fines_fraction": {
        "coverage80": 0.4166666666666667,
        "interval_score80": 2.169057433484428,
        "interval_width": 0.24666666666666667,
        "mae": 0.2945378487858927,
        "n": 12,
        "planned": 12
      },
      "crystal_purity": {
        "coverage80": 0.16666666666666666,
        "interval_score80": 0.39498284012624735,
        "interval_width": 0.1433333333333333,
        "mae": 0.08709582857158808,
        "n": 12,
        "planned": 12
      },
      "crystal_size": {
        "coverage80": 0.8333333333333334,
        "interval_score80": 0.11296895180548765,
        "interval_width": 0.08283333333333333,
        "mae": 0.024528176707569533,
        "n": 12,
        "planned": 12
      },
      "crystal_yield": {
        "coverage80": 0.8333333333333334,
        "interval_score80": 0.2789019350688117,
        "interval_width": 0.21416666666666664,
        "mae": 0.0547456547352344,
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
    "resolved_direction_correct": 8,
    "resolved_direction_n": 16,
    "tie_correct": 2,
    "tie_n": 8,
    "valid": true
  },
  "public_baselines": {
    "available": true,
    "mae": {
      "public_mean": {
        "crystal_fines_fraction": 0.3128742633647808,
        "crystal_purity": 0.004263537114872956,
        "crystal_size": 0.018999905288188203,
        "crystal_yield": 0.2939114269636789
      },
      "public_nearest_neighbor": {
        "crystal_fines_fraction": 0.41699797917851167,
        "crystal_purity": 0.004465715873000181,
        "crystal_size": 0.019341322368955867,
        "crystal_yield": 0.21790688206977837
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
        "cached_input": 461440,
        "input": 495073,
        "output": 5286,
        "stage": "source",
        "uncached_input": 33633
      },
      {
        "cached_input": 0,
        "input": 29730,
        "output": 2155,
        "stage": "K1",
        "uncached_input": 29730
      },
      {
        "cached_input": 0,
        "input": 40421,
        "output": 3125,
        "stage": "Q",
        "uncached_input": 40421
      },
      {
        "cached_input": 29568,
        "input": 43466,
        "output": 2063,
        "stage": "K2",
        "uncached_input": 13898
      }
    ],
    "total": {
      "cached_input": 491008,
      "input": 608690,
      "input_plus_output": 621319,
      "output": 12629,
      "uncached_input": 117682
    },
    "valid": true
  },
  "elapsed_s": 459.2030000000086
}
```
