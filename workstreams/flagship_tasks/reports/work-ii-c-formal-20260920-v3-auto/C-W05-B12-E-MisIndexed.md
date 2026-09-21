# C-W05-B12-E-MisIndexed

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
      "target_temperature_K": 350
    },
    {
      "instrument": "hplc",
      "operation": "measure"
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
      "duration_s": 7200,
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
  "end_step": 11,
  "lifecycle_index": 1,
  "metrics": {
    "byproduct_signal": 0.3816840350627899,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7226314544677734,
    "crystal_fines_fraction": 0.360476553440094,
    "crystal_purity": 0.9856451749801636,
    "crystal_size": 0.07863935083150864,
    "crystal_yield": 0.3317459225654602,
    "degradation_warning": 0.15398813784122467,
    "safety_risk": 0.1693452000617981,
    "score": 0.4557507634162903,
    "selectivity": 0.4410509765148163,
    "virtual_spectrum_summary": 0.2792208790779114,
    "yield": 0.4388884902000427
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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
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
  "end_step": 21,
  "lifecycle_index": 2,
  "metrics": {
    "byproduct_signal": 0.2886554002761841,
    "conversion": 0.9863571524620056,
    "cost": 1.0,
    "crystal_csd_quality": 0.6054673194885254,
    "crystal_fines_fraction": 0.6811865568161011,
    "crystal_purity": 0.9810664057731628,
    "crystal_size": 0.10267704725265503,
    "crystal_yield": 0.41796383261680603,
    "degradation_warning": 0.04237132892012596,
    "safety_risk": 0.17478981614112854,
    "score": 0.4343448877334595,
    "selectivity": 0.5149983763694763,
    "virtual_spectrum_summary": 0.17782756686210632,
    "yield": 0.49580931663513184
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
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
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
      "duration_s": 3600,
      "operation": "heat",
      "stirring_speed_rpm": 200,
      "target_temperature_K": 285
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 260
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
  "end_step": 33,
  "lifecycle_index": 3,
  "metrics": {
    "byproduct_signal": 0.3141336143016815,
    "conversion": 0.9976611733436584,
    "cost": 1.0,
    "crystal_csd_quality": 0.6733870506286621,
    "crystal_fines_fraction": 0.48594966530799866,
    "crystal_purity": 0.9896738529205322,
    "crystal_size": 0.06584396213293076,
    "crystal_yield": 0.37214431166648865,
    "degradation_warning": 0.0694359540939331,
    "safety_risk": 0.17069323360919952,
    "score": 0.4473940134048462,
    "selectivity": 0.4647045433521271,
    "virtual_spectrum_summary": 0.2040196806192398,
    "yield": 0.46351268887519836
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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
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
      "duration_s": 7200,
      "operation": "heat",
      "stirring_speed_rpm": 150,
      "target_temperature_K": 290
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 255
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
  "end_step": 45,
  "lifecycle_index": 4,
  "metrics": {
    "byproduct_signal": 0.30871814489364624,
    "conversion": 0.988798201084137,
    "cost": 1.0,
    "crystal_csd_quality": 0.5922257304191589,
    "crystal_fines_fraction": 0.6939682364463806,
    "crystal_purity": 1.0,
    "crystal_size": 0.07319236546754837,
    "crystal_yield": 0.41537782549858093,
    "degradation_warning": 0.04858642444014549,
    "safety_risk": 0.1738160252571106,
    "score": 0.42694053053855896,
    "selectivity": 0.4911350905895233,
    "virtual_spectrum_summary": 0.1916588693857193,
    "yield": 0.4774089455604553
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
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
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
      "duration_s": 1800,
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
  "end_step": 56,
  "lifecycle_index": 5,
  "metrics": {
    "byproduct_signal": 0.29941388964653015,
    "conversion": 0.985413670539856,
    "cost": 1.0,
    "crystal_csd_quality": 0.5954880118370056,
    "crystal_fines_fraction": 0.6875555515289307,
    "crystal_purity": 0.9757065176963806,
    "crystal_size": 0.053508367389440536,
    "crystal_yield": 0.4284514784812927,
    "degradation_warning": 0.04627608880400658,
    "safety_risk": 0.17614783346652985,
    "score": 0.4302918612957001,
    "selectivity": 0.5209618806838989,
    "virtual_spectrum_summary": 0.18550188839435577,
    "yield": 0.509268581867218
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
      "catalyst": 0,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
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
  "end_step": 66,
  "lifecycle_index": 6,
  "metrics": {
    "byproduct_signal": 0.2938608229160309,
    "conversion": 0.9771837592124939,
    "cost": 1.0,
    "crystal_csd_quality": 0.5838469862937927,
    "crystal_fines_fraction": 0.6895415782928467,
    "crystal_purity": 0.9987188577651978,
    "crystal_size": 0.04763433337211609,
    "crystal_yield": 0.41420528292655945,
    "degradation_warning": 0.049987390637397766,
    "safety_risk": 0.17374329268932343,
    "score": 0.4252656102180481,
    "selectivity": 0.5016187429428101,
    "virtual_spectrum_summary": 0.18411776423454285,
    "yield": 0.49576032161712646
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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
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
  "end_step": 76,
  "lifecycle_index": 7,
  "metrics": {
    "byproduct_signal": 0.301922082901001,
    "conversion": 0.9977701306343079,
    "cost": 1.0,
    "crystal_csd_quality": 0.675851583480835,
    "crystal_fines_fraction": 0.4716412425041199,
    "crystal_purity": 0.9795233011245728,
    "crystal_size": 0.0906694233417511,
    "crystal_yield": 0.40635088086128235,
    "degradation_warning": 0.04528772830963135,
    "safety_risk": 0.17117132246494293,
    "score": 0.458331435918808,
    "selectivity": 0.44844627380371094,
    "virtual_spectrum_summary": 0.18643660843372345,
    "yield": 0.471935898065567
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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 255
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
  "lifecycle_index": 8,
  "metrics": {
    "byproduct_signal": 0.29423201084136963,
    "conversion": 1.0,
    "cost": 1.0,
    "crystal_csd_quality": 0.7064964175224304,
    "crystal_fines_fraction": 0.474070280790329,
    "crystal_purity": 0.9800379872322083,
    "crystal_size": 0.1075720563530922,
    "crystal_yield": 0.4176007807254791,
    "degradation_warning": 0.05185560882091522,
    "safety_risk": 0.1713741421699524,
    "score": 0.4703439772129059,
    "selectivity": 0.47962912917137146,
    "virtual_spectrum_summary": 0.18516263365745544,
    "yield": 0.4681662917137146
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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
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
    "byproduct_signal": 0.30468156933784485,
    "conversion": 0.99418705701828,
    "cost": 1.0,
    "crystal_csd_quality": 0.6788195371627808,
    "crystal_fines_fraction": 0.4909827411174774,
    "crystal_purity": 0.9824036955833435,
    "crystal_size": 0.058225370943546295,
    "crystal_yield": 0.41379666328430176,
    "degradation_warning": 0.04445921257138252,
    "safety_risk": 0.1715007871389389,
    "score": 0.45621782541275024,
    "selectivity": 0.4578617513179779,
    "virtual_spectrum_summary": 0.18758150935173035,
    "yield": 0.4683801233768463
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
      "volume_L": 0.06
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 265
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
  "end_step": 106,
  "lifecycle_index": 10,
  "metrics": {
    "byproduct_signal": 0.301545649766922,
    "conversion": 0.9847586154937744,
    "cost": 1.0,
    "crystal_csd_quality": 0.6681224703788757,
    "crystal_fines_fraction": 0.47161367535591125,
    "crystal_purity": 0.9810901284217834,
    "crystal_size": 0.07043053209781647,
    "crystal_yield": 0.40639206767082214,
    "degradation_warning": 0.05852209031581879,
    "safety_risk": 0.17648907005786896,
    "score": 0.4556856155395508,
    "selectivity": 0.4651823043823242,
    "virtual_spectrum_summary": 0.19218504428863525,
    "yield": 0.47360876202583313
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
      "volume_L": 0.04
    },
    {
      "catalyst": 1,
      "catalyst_amount_mol": 0.005,
      "operation": "add_catalyst"
    },
    {
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 255
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
  "lifecycle_index": 11,
  "metrics": {
    "byproduct_signal": 0.3122501075267792,
    "conversion": 0.9989932179450989,
    "cost": 1.0,
    "crystal_csd_quality": 0.48746126890182495,
    "crystal_fines_fraction": 0.9934489727020264,
    "crystal_purity": 0.9994803071022034,
    "crystal_size": 0.06344708800315857,
    "crystal_yield": 0.41292551159858704,
    "degradation_warning": 0.03823317959904671,
    "safety_risk": 0.19162309169769287,
    "score": 0.3706287741661072,
    "selectivity": 0.4797264337539673,
    "virtual_spectrum_summary": 0.18894249200820923,
    "yield": 0.460223913192749
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
      "duration_s": 1800,
      "operation": "heat",
      "stirring_speed_rpm": 500,
      "target_temperature_K": 330
    },
    {
      "operation": "seed_crystals",
      "seed_mass_g": 0.05
    },
    {
      "duration_s": 14400,
      "operation": "cool_crystallize",
      "target_temperature_K": 255
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
  "end_step": 126,
  "lifecycle_index": 12,
  "metrics": {
    "byproduct_signal": 0.29007482528686523,
    "conversion": 0.9963182806968689,
    "cost": 1.0,
    "crystal_csd_quality": 0.6787276864051819,
    "crystal_fines_fraction": 0.48905038833618164,
    "crystal_purity": 0.9943683743476868,
    "crystal_size": 0.09888295084238052,
    "crystal_yield": 0.4035373628139496,
    "degradation_warning": 0.05464399605989456,
    "safety_risk": 0.1713741421699524,
    "score": 0.4606953263282776,
    "selectivity": 0.46547141671180725,
    "virtual_spectrum_summary": 0.1841309517621994,
    "yield": 0.4673558473587036
  },
  "ordinal": 12
}
```

## K1

```json
{
  "payload": {
    "report": "Mechanistic account\n\nRecommended process and outcome\nBatch 8 remains the recommendation: 0.040 mol reagent, 0.080 L solvent-S2, 0.005 mol catalyst-C1, reaction at 330 K for 1,800 s with 500 rpm stirring, addition of 0.050 g seed, cooling to 255 K over 14,400 s, immediate filtration, termination, and final assay. Its observed seed-excluded crystal recovery was 0.4176, with crystal purity 0.9800 and fines number fraction 0.4741. Thus it gave the highest observed recovery among batches satisfying purity >=0.80 and fines <=0.50.\n\nMaterial effects and reaction\u2013crystallization coupling\nSolvent-S2 was selected from the supplied prior because it had the lowest nominal relative solubility (0.70), highest relative crystal growth (1.30), lowest nucleation tendency (0.65), and lowest impurity occlusion (0.65). Consistent with that prior, every assayed S2 process produced very pure crystals (approximately 0.976\u20131.000). However, no other solvent was experimentally tested, so superiority over S0, S1, or S3 remains an interpretation rather than a demonstrated ranking.\n\nCatalyst identity strongly affected downstream particle quality even when the nominal crystallization procedure was similar. With C0, batches 2, 4, 5, and 6 gave recoveries of 0.414\u20130.428 but fines fractions of 0.681\u20130.694. With C1 at full solvent volume, batches 7\u20139 and 12 gave fines of 0.472, 0.474, 0.491, and 0.489 while retaining recoveries of 0.404\u20130.418. This is the clearest observed reaction\u2013crystallization coupling.\n\nThe coupling is not explained simply by bulk crystal purity: both catalyst families produced approximately 0.98\u20131.00 purity. C0 often showed somewhat better liquid-phase reaction selectivity (roughly 0.49\u20130.52 in batches 2 and 4\u20136) than C1 (roughly 0.45\u20130.48 in batches 7\u20139 and 12), yet its particle distribution was much worse. A plausible interpretation is that catalyst-dependent residual species, byproduct identity, or solution speciation changed heterogeneous nucleation or crystal-growth kinetics without being captured by the scalar purity measurement. Catalyst carryover acting as nucleation sites is another possibility. These alternatives were not independently assayed and therefore remain unresolved.\n\nReaction severity mattered. Batch 1 used C1 but was heated at 350 K for 3,600 s; it showed byproduct signal 0.382 and degradation warning 0.154, versus degradation warnings near 0.04\u20130.06 for the 330 K, 1,800 s C1 processes. Its reaction selectivity was only 0.441. The revised 330 K/1,800 s condition therefore reduced apparent degradation while maintaining essentially complete conversion. For example, batch 8 gave conversion 1.000, reaction selectivity 0.480, and liquid-product yield 0.468. The evidence supports avoiding the hotter, longer reaction, although reaction temperature and residence time were not mapped independently.\n\nCrystallization mechanism and concentration effects\nA useful qualitative description is supersaturation-controlled competition between nucleation and growth:\n\nS = (C - C*)/C*,\nB = k_b S^b,\nG = k_g S^g,\n\nwhere S is supersaturation, B is nucleation rate, and G is crystal-growth rate. Conditions that make B large relative to G create many small particles and raise the number fraction below 20 micrometres. Recovery can be approximated by\n\nR_cryst = n_target,recovered excluding seed / n_target,before separation,\n\nand, at equilibrium, tends to increase as the residual dissolved amount C*(T_f)V decreases. This recovery is explicitly a crystallization-stage recovery, not overall yield from charged reagent. If reaction and crystallization definitions are treated as approximately compatible, batch 8\u2019s overall recovered-target fraction would be on the order of reaction yield times crystallization recovery, about 0.47 \u00d7 0.42, rather than 0.42 of the initial reagent.\n\nThe solvent-volume study supports a nonlinear supersaturation effect. At 0.080 L, C1 batches 7\u20139 and 12 all met the fines constraint. Reducing S2 to 0.060 L in batch 10 still worked (recovery 0.4064, fines 0.4716, purity 0.9811). Reducing it further to 0.040 L in batch 11 caused a sharp fines increase to 0.9934, despite recovery of 0.4129 and purity of 0.9995. The most likely interpretation is that the concentrated charge crossed a nucleation threshold, creating an overwhelming number of fine particles. This sharp response argues against pursuing recovery by concentration alone.\n\nTemperature revealed a narrower tradeoff under the preferred C1/full-volume conditions. Direct cooling gave:\n- Batch 7, 260 K: recovery 0.4064, fines 0.4716.\n- Batch 8, 255 K: recovery 0.4176, fines 0.4741.\n- Batch 9, 250 K: recovery 0.4138, fines 0.4910.\n- Batch 12, 255 K replicate: recovery 0.4035, fines 0.4891.\n\nThe expected thermodynamic tendency is increased recovery at lower temperature, but the observed recovery differences are small relative to process and assay variability. Fines generally approached the constraint at the coldest settings. Consequently, 255 K represents an empirical compromise rather than proof of a sharply defined optimum.\n\nProcess-history dependence\nBatch 1 cooled to 280 K and was then held for 7,200 s; during the hold the vessel warmed toward ambient before filtration. It produced particularly low fines (0.3605) but only 0.3317 recovery. This is consistent with partial dissolution or Ostwald-type ripening removing the smallest crystals at the cost of recovered mass. Because batch 1 also used the harsher reaction, the thermal-history contribution cannot be isolated.\n\nBatch 3 deliberately used a cycle of cooling to 250 K, reheating to 285 K, and recooling to 260 K. It met the constraints (recovery 0.3721, purity 0.9897, fines 0.4859), but recovery was lower than in the simpler direct-cooling C1 batches 7\u20139. The cycle may have dissolved fines and allowed regrowth, but it offered no recovery advantage. With C0, a more extensive 250\u2192290\u2192255 K cycle in batch 4 failed to correct the fines problem (0.6940), showing that thermal annealing could not overcome the catalyst-associated CSD effect under the tested conditions. Similarly, warming after cold crystallization in C0 batch 5 still left fines at 0.6876. These observations motivated the revision toward simple, direct cooling with C1.\n\nRevisions during the campaign\nThe work progressed from a hotter reaction and warm crystallization in batch 1, through deeper cooling with C0 in batch 2, thermal cycling in batches 3\u20135, and direct-temperature tests in batches 6\u20139. The large catalyst-dependent fines contrast shifted emphasis from maximizing nominal reaction selectivity to controlling downstream nucleation. Batches 10\u201311 then tested concentration, revealing the severe fines penalty at 0.040 L. Batch 12 repeated the chosen batch-8 recipe and confirmed feasibility, though with modestly lower recovery.\n\nUncertainty and unresolved tradeoff\nBatch 8 and its batch-12 replicate gave recoveries of 0.4176 and 0.4035, purities of 0.9800 and 0.9944, and fines of 0.4741 and 0.4891. Their mean recovery is about 0.411 and their mean fines fraction about 0.482. This reproducibility supports the process region, but both fines results lie close to the 0.50 constraint. The final-assay fines noise specification was approximately 0.018, and independent in-process particle measurements also placed several batches near the boundary (batch 8: 0.4862; batch 9: 0.5006; batch 12: 0.4911). Therefore the recommendation qualifies on observed final assays but has limited fines margin.\n\nThe unresolved optimization problem is a recovery\u2013robustness tradeoff. Deeper cooling or greater concentration might increase thermodynamic recovery, but the tested evidence shows increasing or catastrophic fines risk. Warmer holds or thermal cycling can lower fines in some histories, but they sacrifice recovery and were not consistently effective. A future study could test slightly warmer final temperatures, controlled cooling-rate profiles, seed-size distributions, or a modestly larger solvent volume to create more fines margin; none of those alternatives was tested here. Catalyst carryover and solution speciation should also be measured directly to determine why C1 controls fines much better than C0."
  },
  "failure": null,
  "elapsed_s": 71.93799999999464,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 530560,
    "input_tokens": 633413,
    "output_tokens": 9633,
    "reasoning_output_tokens": 3059
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
          "estimate": 0.24,
          "lower80": 0.1,
          "upper80": 0.4
        },
        "crystal_purity": {
          "estimate": 0.89,
          "lower80": 0.81,
          "upper80": 0.95
        },
        "crystal_size": {
          "estimate": 0.31,
          "lower80": 0.18,
          "upper80": 0.46
        },
        "crystal_yield": {
          "estimate": 0.205,
          "lower80": 0.12,
          "upper80": 0.3
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q01"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.16,
          "lower80": 0.05,
          "upper80": 0.3
        },
        "crystal_purity": {
          "estimate": 0.94,
          "lower80": 0.88,
          "upper80": 0.98
        },
        "crystal_size": {
          "estimate": 0.38,
          "lower80": 0.24,
          "upper80": 0.54
        },
        "crystal_yield": {
          "estimate": 0.285,
          "lower80": 0.19,
          "upper80": 0.39
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q02"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.46,
          "lower80": 0.25,
          "upper80": 0.67
        },
        "crystal_purity": {
          "estimate": 0.84,
          "lower80": 0.74,
          "upper80": 0.92
        },
        "crystal_size": {
          "estimate": 0.24,
          "lower80": 0.1,
          "upper80": 0.4
        },
        "crystal_yield": {
          "estimate": 0.125,
          "lower80": 0.05,
          "upper80": 0.23
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q03"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.31,
          "lower80": 0.14,
          "upper80": 0.5
        },
        "crystal_purity": {
          "estimate": 0.86,
          "lower80": 0.77,
          "upper80": 0.94
        },
        "crystal_size": {
          "estimate": 0.28,
          "lower80": 0.15,
          "upper80": 0.43
        },
        "crystal_yield": {
          "estimate": 0.155,
          "lower80": 0.07,
          "upper80": 0.25
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q04"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.28,
          "lower80": 0.12,
          "upper80": 0.47
        },
        "crystal_purity": {
          "estimate": 0.86,
          "lower80": 0.77,
          "upper80": 0.94
        },
        "crystal_size": {
          "estimate": 0.33,
          "lower80": 0.19,
          "upper80": 0.49
        },
        "crystal_yield": {
          "estimate": 0.15,
          "lower80": 0.07,
          "upper80": 0.25
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q05"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.54,
          "lower80": 0.34,
          "upper80": 0.73
        },
        "crystal_purity": {
          "estimate": 0.85,
          "lower80": 0.75,
          "upper80": 0.93
        },
        "crystal_size": {
          "estimate": 0.2,
          "lower80": 0.09,
          "upper80": 0.35
        },
        "crystal_yield": {
          "estimate": 0.155,
          "lower80": 0.07,
          "upper80": 0.26
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q06"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.26,
          "lower80": 0.11,
          "upper80": 0.44
        },
        "crystal_purity": {
          "estimate": 0.86,
          "lower80": 0.77,
          "upper80": 0.94
        },
        "crystal_size": {
          "estimate": 0.35,
          "lower80": 0.21,
          "upper80": 0.51
        },
        "crystal_yield": {
          "estimate": 0.155,
          "lower80": 0.07,
          "upper80": 0.26
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q07"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.52,
          "lower80": 0.31,
          "upper80": 0.72
        },
        "crystal_purity": {
          "estimate": 0.88,
          "lower80": 0.78,
          "upper80": 0.95
        },
        "crystal_size": {
          "estimate": 0.24,
          "lower80": 0.11,
          "upper80": 0.4
        },
        "crystal_yield": {
          "estimate": 0.105,
          "lower80": 0.03,
          "upper80": 0.2
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q08"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.86,
          "lower80": 0.65,
          "upper80": 0.98
        },
        "crystal_purity": {
          "estimate": 0.87,
          "lower80": 0.7,
          "upper80": 0.96
        },
        "crystal_size": {
          "estimate": 0.075,
          "lower80": 0.03,
          "upper80": 0.14
        },
        "crystal_yield": {
          "estimate": 0.008,
          "lower80": 0,
          "upper80": 0.03
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q09"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.64,
          "lower80": 0.42,
          "upper80": 0.82
        },
        "crystal_purity": {
          "estimate": 0.86,
          "lower80": 0.73,
          "upper80": 0.94
        },
        "crystal_size": {
          "estimate": 0.14,
          "lower80": 0.06,
          "upper80": 0.25
        },
        "crystal_yield": {
          "estimate": 0.06,
          "lower80": 0.015,
          "upper80": 0.14
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q10"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.27,
          "lower80": 0.11,
          "upper80": 0.46
        },
        "crystal_purity": {
          "estimate": 0.87,
          "lower80": 0.78,
          "upper80": 0.94
        },
        "crystal_size": {
          "estimate": 0.34,
          "lower80": 0.2,
          "upper80": 0.5
        },
        "crystal_yield": {
          "estimate": 0.16,
          "lower80": 0.07,
          "upper80": 0.27
        },
        "particles_present": true,
        "quality_feasible": true,
        "query_id": "Q11"
      },
      {
        "crystal_fines_fraction": {
          "estimate": 0.63,
          "lower80": 0.42,
          "upper80": 0.81
        },
        "crystal_purity": {
          "estimate": 0.84,
          "lower80": 0.73,
          "upper80": 0.92
        },
        "crystal_size": {
          "estimate": 0.18,
          "lower80": 0.08,
          "upper80": 0.31
        },
        "crystal_yield": {
          "estimate": 0.29,
          "lower80": 0.17,
          "upper80": 0.42
        },
        "particles_present": true,
        "quality_feasible": false,
        "query_id": "Q12"
      }
    ],
    "rationale": "Q01\u2013Q02: S3 is predicted to outperform S1 because its lower nominal solubility and impurity occlusion, lower nucleation tendency, and higher growth tendency should raise recovery, purity, and size while reducing fines. Q03\u2013Q04: greater seeding should suppress uncontrolled primary nucleation and modestly improve recovery and CSD, although seed-excluded yield does not count the seed itself. Q05\u2013Q06: the gradual ramp and cold shock have similar final temperature and total time, so equilibrium recovery is similar, but the shock is expected to generate substantially more fines. Q07\u2013Q08: the 315 K excursion should redissolve product; only one hour of recooling is unlikely to restore recovery and may cause renewed nucleation, despite some purification. Q09\u2013Q10: seed particles remain present in both, but 60 seconds gives almost no seed-excluded deposition; the two-hour hold increases recovery and growth but probably remains fines-limited. Q11\u2013Q12: doubling reagent concentration should increase recovered fraction but cross toward a high-nucleation regime, reducing size and worsening fines and occlusion. Intervals are deliberately broad because the recipes extrapolate far beyond the campaign in solvent identity, concentration, cooling duration, and thermal history; feasibility is assigned from the point estimates, not guaranteed by the intervals."
  },
  "failure": null,
  "elapsed_s": 95.81200000000536,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 530560,
    "input_tokens": 679851,
    "output_tokens": 13959,
    "reasoning_output_tokens": 5688
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
    "report": "1. Status of the main claims\n\nSupported by direct observations:\n- Catalyst choice was strongly associated with downstream fines. C0 batches 2, 4, 5, and 6 had final fines fractions of about 0.681\u20130.694, whereas full-volume C1 batches 7, 8, 9, and 12 gave 0.472\u20130.491. This association is robust within the campaign.\n- Batch 8\u2019s operating region was reproducible but close to the fines boundary. Batch 8 gave recovery 0.4176, purity 0.9800, and fines 0.4741; its recipe replicate, batch 12, gave 0.4035, 0.9944, and 0.4891.\n- Purity was not the binding constraint. All completed batches had very high assayed crystal purity, approximately 0.976\u20131.000, including the high-fines C0 batches.\n- A severe concentration effect was observed. Reducing S2 from 0.080 L to 0.060 L in batch 10 retained acceptable fines (0.4716), but 0.040 L in batch 11 produced fines of 0.9934. Calling this a nucleation threshold is an interpretation, but the abrupt empirical deterioration is direct evidence.\n- The hotter, longer reaction in batch 1 showed more degradation and byproduct signal: degradation warning 0.154 and byproduct signal 0.382, versus warnings around 0.04\u20130.06 for the later 330 K/1,800 s C1 batches. Avoiding that harsher reaction is therefore supported, although temperature and duration were changed together.\n\nSupported only as interpretations:\n- Catalyst carryover acting as heterogeneous nucleation sites is plausible, but catalyst identity was never separated from catalyst-dependent reaction composition or solution speciation. The observation supports coupling, not that particular mechanism.\n- The account attributed batch 11\u2019s fines excursion to high supersaturation and nucleation. That is consistent with the volume series, but volume, concentration, and solvent-to-solute ratio were not independently varied.\n- The low fines and low recovery in batch 1 are consistent with dissolution/ripening during its warm post-cooling history, but its harsher reaction is a confounder.\n\nContradicted or weakened:\n- Recovery did not increase monotonically with deeper final cooling. For otherwise similar C1 batches, recovery was 0.4064 at 260 K (batch 7), 0.4176 at 255 K (batch 8), and 0.4138 at 250 K (batch 9). Any thermodynamic trend was smaller than process variation over this range.\n- Thermal annealing was not a generally effective fines remedy. Batch 3\u2019s cycle qualified but recovered only 0.3721, while direct-cooling batches 7\u20139 recovered about 0.406\u20130.418. C0 batch 4 remained at 0.694 fines after cycling, and warming after cooling did not rescue batch 5.\n- Greater concentration did not demonstrably improve recovery: batches 10 and 11 recovered 0.4064 and 0.4129, neither exceeding batch 8, while batch 11 suffered a major CSD penalty.\n- A simple \u201cmore bulk impurity causes more fines\u201d explanation is weakened because C0 often had better scalar reaction selectivity than C1 yet much worse fines, while final crystal purity remained high.\n\nStill untested:\n- The claimed superiority of S2 over S0, S1, and S3. Every campaign batch used S2; its favorable nominal dossier was prior evidence, not an experimental solvent comparison.\n- Whether C0 itself, a C0-derived product/byproduct, or another unmeasured solution property causes the fines increase.\n- Effects of seed size distribution, cooling rate independent of final temperature, catalyst removal, washing, and solvent mixtures.\n- Robust operation with a comfortable fines margin below 0.50; the recommended region was feasible but marginal.\n\n2. One additional experiment\n\nI would run a catalyst-loading discrimination experiment using 0.040 mol reagent, 0.080 L S2, and only 0.0005 mol C0. I would react at 330 K, using a longer residence time if needed to approach the conversion of batch 8, take an HPLC measurement before crystallization, then add 0.050 g seed, cool directly to 255 K over 14,400 s, measure particle size, filter, terminate, and assay.\n\nThis single batch would be compared with the high-C0-loading batches 2/4\u20136 and the C1 reference batches 8/12. It would distinguish three explanations:\n- If C0 acts mainly through catalyst-particle or catalyst-concentration-dependent heterogeneous nucleation, a tenfold reduction should move fines from about 0.69 toward the C1 range near 0.47\u20130.49 while retaining reasonable recovery.\n- If catalyst identity creates a potent dissolved nucleation promoter even at low loading, fines should remain high despite the reduced C0 amount.\n- If the effect is mediated mainly by reaction composition, fines should track the measured HPLC byproduct/selectivity profile rather than catalyst loading itself. A C1-like chromatographic profile with C0-like fines would argue against the scalar reaction-composition explanation; simultaneous improvement of both would support it.\n\nThe cleanest favorable result would be purity above 0.95, recovery around 0.40, and fines below 0.50. Persisting fines near 0.65\u20130.70 would strongly support an identity-specific C0 effect. An intermediate result would indicate a dose-dependent coupling and motivate a proper catalyst-loading series.\n\n3. Least effectively used observation and least reliable prediction\n\nThe account used crystal_size least effectively. It focused on recovery, purity, and the thresholded fines fraction, but the observed median-size metric was not redundant with fines. For example, batch 2 had crystal_size 0.1027 despite fines 0.681, while batch 1 had size 0.0786 and much lower fines of 0.360. Batch 8 had size 0.1076 and fines 0.474, whereas batch 12 had size 0.0989 and fines 0.489. These combinations suggest broad or possibly bimodal distributions: a respectable d50 can coexist with a large sub-20 \u00b5m population. Treating \u201clarger size\u201d and \u201cfewer fines\u201d as one mechanism therefore lost information.\n\nQ02 is the least reliable held-out prediction. Its optimistic S3 estimates rely almost entirely on nominal solvent properties\u2014lower solubility and occlusion and better growth/nucleation balance\u2014because the campaign supplied no experimental evidence for S3 or any solvent other than S2. It also extrapolates to a much smaller charge, a hotter quenched reaction, and an exceptionally long multistage cooling history. Hidden solvent-specific residuals could reverse the nominal ranking. Q01 has the same general limitation for S1, but Q02 made the stronger favorable extrapolation and is therefore the most vulnerable sealed prediction."
  },
  "failure": null,
  "elapsed_s": 74.14100000000326,
  "usage": {
    "cache_write_input_tokens": 0,
    "cached_input_tokens": 565248,
    "input_tokens": 730535,
    "output_tokens": 16892,
    "reasoning_output_tokens": 7098
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
    "selection_rationale": "Highest observed seed-excluded crystal recovery among completed batches meeting both quality constraints: crystal_yield 0.4176, crystal_purity 0.9800, and fines fraction 0.4741. The full-solvent, C1-catalyzed, seeded slow-cooling process also showed reproducible feasibility in nearby batches."
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
        "duration_s": 1800,
        "operation": "heat",
        "stirring_speed_rpm": 500,
        "target_temperature_K": 330
      },
      {
        "operation": "seed_crystals",
        "seed_mass_g": 0.05
      },
      {
        "duration_s": 14400,
        "operation": "cool_crystallize",
        "target_temperature_K": 255
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
    "source_attempts": 10
  },
  "prediction_evaluation": {
    "contrasts": [
      {
        "absolute_delta_error": 0.2892231216822536,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_yield",
        "predicted_delta": 0.07999999999999999,
        "resolved": true,
        "true_delta": -0.2092231216822536
      },
      {
        "absolute_delta_error": 0.05014777149572891,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_purity",
        "predicted_delta": 0.04999999999999993,
        "resolved": false,
        "true_delta": -0.00014777149572897663
      },
      {
        "absolute_delta_error": 0.06288280081646157,
        "direction_correct": true,
        "factor": "solvent",
        "metric": "crystal_size",
        "predicted_delta": 0.07,
        "resolved": true,
        "true_delta": 0.007117199183538439
      },
      {
        "absolute_delta_error": 0.19661623193981456,
        "direction_correct": false,
        "factor": "solvent",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.07999999999999999,
        "resolved": true,
        "true_delta": -0.27661623193981455
      },
      {
        "absolute_delta_error": 0.030132329809087866,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_yield",
        "predicted_delta": 0.03,
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
        "absolute_delta_error": 0.04497943907987052,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_size",
        "predicted_delta": 0.040000000000000036,
        "resolved": false,
        "true_delta": -0.004979439079870487
      },
      {
        "absolute_delta_error": 0.2834195253798536,
        "direction_correct": false,
        "factor": "seed",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.15000000000000002,
        "resolved": true,
        "true_delta": 0.13341952537985358
      },
      {
        "absolute_delta_error": 0.0045664791321695375,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_yield",
        "predicted_delta": 0.0050000000000000044,
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
        "absolute_delta_error": 0.08616113116301133,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_size",
        "predicted_delta": -0.13,
        "resolved": true,
        "true_delta": -0.04383886883698868
      },
      {
        "absolute_delta_error": 0.35381528795023254,
        "direction_correct": true,
        "factor": "cooling_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.26,
        "resolved": true,
        "true_delta": 0.6138152879502325
      },
      {
        "absolute_delta_error": 0.09304184008830015,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_yield",
        "predicted_delta": -0.05,
        "resolved": true,
        "true_delta": 0.04304184008830014
      },
      {
        "absolute_delta_error": 0.03037751463115035,
        "direction_correct": false,
        "factor": "thermal_history",
        "metric": "crystal_purity",
        "predicted_delta": 0.020000000000000018,
        "resolved": true,
        "true_delta": -0.01037751463115033
      },
      {
        "absolute_delta_error": 0.07014464698269009,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_size",
        "predicted_delta": -0.10999999999999999,
        "resolved": true,
        "true_delta": -0.0398553530173099
      },
      {
        "absolute_delta_error": 0.38994217799874087,
        "direction_correct": true,
        "factor": "thermal_history",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.26,
        "resolved": true,
        "true_delta": 0.6499421779987409
      },
      {
        "absolute_delta_error": 0.05414975880452933,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_yield",
        "predicted_delta": 0.052,
        "resolved": true,
        "true_delta": 0.10614975880452933
      },
      {
        "absolute_delta_error": 0.0022800208771958097,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_purity",
        "predicted_delta": -0.010000000000000009,
        "resolved": true,
        "true_delta": -0.012280020877195819
      },
      {
        "absolute_delta_error": 0.05227418830942542,
        "direction_correct": true,
        "factor": "continue_growth",
        "metric": "crystal_size",
        "predicted_delta": 0.06500000000000002,
        "resolved": true,
        "true_delta": 0.012725811690574594
      },
      {
        "absolute_delta_error": 0.26253026625748244,
        "direction_correct": false,
        "factor": "continue_growth",
        "metric": "crystal_fines_fraction",
        "predicted_delta": -0.21999999999999997,
        "resolved": false,
        "true_delta": 0.04253026625748246
      },
      {
        "absolute_delta_error": 0.11506595761778371,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_yield",
        "predicted_delta": 0.12999999999999998,
        "resolved": false,
        "true_delta": 0.014934042382216267
      },
      {
        "absolute_delta_error": 0.024890313202054815,
        "direction_correct": false,
        "factor": "upstream_loading",
        "metric": "crystal_purity",
        "predicted_delta": -0.030000000000000027,
        "resolved": false,
        "true_delta": -0.005109686797945212
      },
      {
        "absolute_delta_error": 0.1316616016103552,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_size",
        "predicted_delta": -0.16000000000000003,
        "resolved": true,
        "true_delta": -0.028338398389644838
      },
      {
        "absolute_delta_error": 0.242412437007269,
        "direction_correct": true,
        "factor": "upstream_loading",
        "metric": "crystal_fines_fraction",
        "predicted_delta": 0.36,
        "resolved": true,
        "true_delta": 0.602412437007269
      }
    ],
    "failures": [],
    "metrics": {
      "crystal_fines_fraction": {
        "coverage80": 0.5,
        "interval_score80": 1.9693593529187343,
        "interval_width": 0.3566666666666667,
        "mae": 0.3072068345342453,
        "n": 12,
        "planned": 12
      },
      "crystal_purity": {
        "coverage80": 0.0,
        "interval_score80": 0.6066378216653467,
        "interval_width": 0.17499999999999996,
        "mae": 0.11733044883320133,
        "n": 12,
        "planned": 12
      },
      "crystal_size": {
        "coverage80": 0.08333333333333333,
        "interval_score80": 0.964753144586277,
        "interval_width": 0.26166666666666666,
        "mae": 0.18887454433832104,
        "n": 12,
        "planned": 12
      },
      "crystal_yield": {
        "coverage80": 0.6666666666666666,
        "interval_score80": 0.33972522387798937,
        "interval_width": 0.1729166666666667,
        "mae": 0.09333212096072756,
        "n": 12,
        "planned": 12
      }
    },
    "quality": {
      "balanced_accuracy": 0.8571428571428572,
      "false_negative": 0,
      "false_positive": 2,
      "true_negative": 5,
      "true_positive": 5
    },
    "resolved_direction_correct": 10,
    "resolved_direction_n": 15,
    "tie_correct": 1,
    "tie_n": 9,
    "valid": true
  },
  "public_baselines": {
    "available": true,
    "mae": {
      "public_mean": {
        "crystal_fines_fraction": 0.3051880688917262,
        "crystal_purity": 0.004412286692505883,
        "crystal_size": 0.019036061626971638,
        "crystal_yield": 0.18659649597592676
      },
      "public_nearest_neighbor": {
        "crystal_fines_fraction": 0.2429360310884219,
        "crystal_purity": 0.0056682323177831935,
        "crystal_size": 0.017613703074160356,
        "crystal_yield": 0.1621633475719643
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
        "cached_input": 530560,
        "input": 598511,
        "output": 6633,
        "stage": "source",
        "uncached_input": 67951
      },
      {
        "cached_input": 0,
        "input": 34902,
        "output": 3000,
        "stage": "K1",
        "uncached_input": 34902
      },
      {
        "cached_input": 0,
        "input": 46438,
        "output": 4326,
        "stage": "Q",
        "uncached_input": 46438
      },
      {
        "cached_input": 34688,
        "input": 50684,
        "output": 2933,
        "stage": "K2",
        "uncached_input": 15996
      }
    ],
    "total": {
      "cached_input": 565248,
      "input": 730535,
      "input_plus_output": 747427,
      "output": 16892,
      "uncached_input": 165287
    },
    "valid": true
  },
  "elapsed_s": 466.76600000000326
}
```
