# repeat-03/EC-W01-B12-optimization-E-MisIndexed

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-03\EC-W01-B12-optimization-E-MisIndexed\participant\optimization-E-MisIndexed

## 同期笔记

### v1 · 公开事件 0

# Source-stage hypothesis notebook

## H1 [tentative]
At fixed loading, balanced score should have an interior potential/current-duration region: increasing absolute driving force or time first raises conversion/yield, then loses selectivity and energy efficiency. This predicts a moderate setting will outperform both mild/short and extreme/long settings within a material pair.

## H2 [tentative]
Nominally conductive media (especially S0 and E0/E3) should improve ohmic efficiency, but the best balanced score may instead require a compromise with transport and selectivity. E3 has elevated precipitation risk from its salt/Ksp dossier; S1/S2 may mitigate precipitation but incur conductivity penalties.

## H3 [unresolved sign]
The productive potential sign is unknown. Early paired-sign experiments at otherwise matched fixed loading will identify it; subsequent batches will refine magnitude, duration/current cap, and promising material combinations. A result would change this plan if both signs give near-zero selective yield, in which case material screening takes priority.

All comparisons will use 0.020 mol reagent in 0.040 L solvent unless an operational constraint forces otherwise. Intermediate UV-vis will be used mainly to diagnose efficiency before termination; final assays are authoritative.

### v2 · 公开事件 84

# Source-stage hypothesis notebook

## H1 [supported in tested scope; refined]
At fixed 0.020 mol / 0.040 L loading, positive potential is productive and negative potential is inferior: matched S0/E0, 1.0 V, 100 mA cap, 3600 s gave scores 0.536 versus 0.310 at -1.0 V (final assays runner-operation-0007 and -0014). The response is not monotone in all factors: S1/E0 at 1.2 V, 300 mA, 7200 s produced no detected conversion/yield (runner-operation-0021), so material coupling and/or excessive drive can null performance. The sign conclusion is strong for the matched pair; the exact cause of the zero remains unresolved.

## H2 [supported in tested scope]
S0/E1 is the best tested material pair. At 1.0 V, 100 mA, 7200 s it scored 0.624 with selective yield 0.165 (runner-operation-0028), exceeding E2 and E3 in S0 (scores 0.598 and 0.554; runner-operation-0035 and -0042) and E1 in S1/S2/S3 (0.593/0.517/0.590; runner-operation-0049/-0056/-0063). These are mostly single runs, so small material differences are not repeatability evidence; the larger ranking gaps motivate the selection. E3 precipitation concern was not borne out under the tested S0 condition, while precipitation_signal was paradoxically high for S0/E0 and S0/E1; therefore precipitation_signal is not treated as a simple material failure indicator here.

## H3 [supported: current-duration tradeoff]
For S0/E1 at 1.0 V, extending 100 mA-cap operation from 7200 to 14400 s increased score from 0.624 to 0.705 and selective yield from 0.165 to 0.327 (runner-operation-0028 vs -0070). At 14400 s, raising the cap to 500 mA raised yield to 0.823 but lowered faradaic/transport/energy efficiencies and scored 0.738 (runner-operation-0077). An intermediate 300 mA cap achieved the best balance: score 0.826, selective yield 0.800, conversion 0.799, selectivity 0.949, energy efficiency 0.887, with safety risk 0.072 (runner-operation-0084). Thus a cap near 300 mA appears preferable to both 100 and 500 mA for this tested duration and pair. The exact optimum is unresolved between sparse cap levels, and final-assay noise plus single replicates limits fine distinctions.

## Decision
Recommend batch 12: 0.020 mol reagent, 0.040 L S0, E1, +1.0 V, 300 mA cap, 14400 s. I would change this decision if a replicate or nearby cap/potential condition materially reduced its observed advantage, or if safety/precipitation constraints were tightened below the observed values.

## 实际批次及公开测量

### 批次 1 · 终点事件 7

```json
{
  "ordinal": 1,
  "lifecycle_index": 1,
  "end_step": 7,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 3600,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "metrics": {
    "cost": 0.28404000401496887,
    "electrochemical_conversion": 0.08101586997509003,
    "electrochemical_selectivity": 0.9495708346366882,
    "energy_efficiency": 0.7765322327613831,
    "faradaic_efficiency": 0.8071436285972595,
    "ohmic_efficiency": 0.9695378541946411,
    "pH_normalized": 0.23218974471092224,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.5356166362762451,
    "selective_product_yield": 0.054451022297143936,
    "transport_efficiency": 0.7784398794174194
  }
}
```

### 批次 2 · 终点事件 14

```json
{
  "ordinal": 2,
  "lifecycle_index": 2,
  "end_step": 14,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1
    },
    {
      "duration_s": 3600,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "metrics": {
    "cost": 0.28404000401496887,
    "electrochemical_conversion": 0.028602926060557365,
    "electrochemical_selectivity": 0.6255703568458557,
    "energy_efficiency": 0.24048729240894318,
    "faradaic_efficiency": 0.39272937178611755,
    "ohmic_efficiency": 0.9783756732940674,
    "pH_normalized": 0.2294943928718567,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.3095265328884125,
    "selective_product_yield": 0.0315379723906517,
    "transport_efficiency": 0.4189862012863159
  }
}
```

### 批次 3 · 终点事件 21

```json
{
  "ordinal": 3,
  "lifecycle_index": 3,
  "end_step": 21,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "current_mA": 300,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1.2
    },
    {
      "duration_s": 7200,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "metrics": {
    "cost": 0.29880842566490173,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.0,
    "ohmic_efficiency": 0.9850577116012573,
    "pH_normalized": 0.23418448865413666,
    "precipitation_signal": 0.9822408556938171,
    "safety_risk": 0.09559440612792969,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.0
  }
}
```

### 批次 4 · 终点事件 28

```json
{
  "ordinal": 4,
  "lifecycle_index": 4,
  "end_step": 28,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 7200,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "metrics": {
    "cost": 0.28547999262809753,
    "electrochemical_conversion": 0.16845181584358215,
    "electrochemical_selectivity": 0.9273543953895569,
    "energy_efficiency": 0.8931524753570557,
    "faradaic_efficiency": 0.9514824748039246,
    "ohmic_efficiency": 0.9740233421325684,
    "pH_normalized": 0.19905288517475128,
    "precipitation_signal": 0.8491079807281494,
    "safety_risk": 0.072194404900074,
    "score": 0.6236562728881836,
    "selective_product_yield": 0.16545264422893524,
    "transport_efficiency": 0.9199949502944946
  }
}
```

### 批次 5 · 终点事件 35

```json
{
  "ordinal": 5,
  "lifecycle_index": 5,
  "end_step": 35,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 7200,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "metrics": {
    "cost": 0.28547999262809753,
    "electrochemical_conversion": 0.16268257796764374,
    "electrochemical_selectivity": 0.9256767630577087,
    "energy_efficiency": 0.8642503619194031,
    "faradaic_efficiency": 0.8645631670951843,
    "ohmic_efficiency": 0.9685879349708557,
    "pH_normalized": 0.15641580522060394,
    "precipitation_signal": 0.0,
    "safety_risk": 0.072194404900074,
    "score": 0.5978491306304932,
    "selective_product_yield": 0.1548393815755844,
    "transport_efficiency": 0.8540537357330322
  }
}
```

### 批次 6 · 终点事件 42

```json
{
  "ordinal": 6,
  "lifecycle_index": 6,
  "end_step": 42,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 7200,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "metrics": {
    "cost": 0.28547999262809753,
    "electrochemical_conversion": 0.12769781053066254,
    "electrochemical_selectivity": 0.9268405437469482,
    "energy_efficiency": 0.8996289968490601,
    "faradaic_efficiency": 0.6970230937004089,
    "ohmic_efficiency": 0.9807637333869934,
    "pH_normalized": 0.27484753727912903,
    "precipitation_signal": 0.0023995577357709408,
    "safety_risk": 0.072194404900074,
    "score": 0.5539279580116272,
    "selective_product_yield": 0.1261662393808365,
    "transport_efficiency": 0.6723397970199585
  }
}
```

### 批次 7 · 终点事件 49

```json
{
  "ordinal": 7,
  "lifecycle_index": 7,
  "end_step": 49,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 7200,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "metrics": {
    "cost": 0.3014799952507019,
    "electrochemical_conversion": 0.16605611145496368,
    "electrochemical_selectivity": 0.906825065612793,
    "energy_efficiency": 0.8773676156997681,
    "faradaic_efficiency": 0.8367710709571838,
    "ohmic_efficiency": 0.996627926826477,
    "pH_normalized": 0.20364195108413696,
    "precipitation_signal": 0.7092664241790771,
    "safety_risk": 0.09559440612792969,
    "score": 0.5930418968200684,
    "selective_product_yield": 0.14882498979568481,
    "transport_efficiency": 0.8401714563369751
  }
}
```

### 批次 8 · 终点事件 56

```json
{
  "ordinal": 8,
  "lifecycle_index": 8,
  "end_step": 56,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 7200,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "metrics": {
    "cost": 0.32708001136779785,
    "electrochemical_conversion": 0.1336877942085266,
    "electrochemical_selectivity": 0.7947602272033691,
    "energy_efficiency": 0.7625535130500793,
    "faradaic_efficiency": 0.7515162229537964,
    "ohmic_efficiency": 0.9753817319869995,
    "pH_normalized": 0.21422593295574188,
    "precipitation_signal": 0.5816152095794678,
    "safety_risk": 0.1135944053530693,
    "score": 0.5167307257652283,
    "selective_product_yield": 0.09016772359609604,
    "transport_efficiency": 0.745020866394043
  }
}
```

### 批次 9 · 终点事件 63

```json
{
  "ordinal": 9,
  "lifecycle_index": 9,
  "end_step": 63,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 3,
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 7200,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "metrics": {
    "cost": 0.3110800087451935,
    "electrochemical_conversion": 0.1511397808790207,
    "electrochemical_selectivity": 0.8860914707183838,
    "energy_efficiency": 0.9006291627883911,
    "faradaic_efficiency": 0.8116931319236755,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.2111297845840454,
    "precipitation_signal": 0.6089179515838623,
    "safety_risk": 0.12619440257549286,
    "score": 0.5900485515594482,
    "selective_product_yield": 0.15423621237277985,
    "transport_efficiency": 0.8325244188308716
  }
}
```

### 批次 10 · 终点事件 70

```json
{
  "ordinal": 10,
  "lifecycle_index": 10,
  "end_step": 70,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 14400,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "metrics": {
    "cost": 0.28835999965667725,
    "electrochemical_conversion": 0.35984084010124207,
    "electrochemical_selectivity": 0.9750677347183228,
    "energy_efficiency": 0.9471549391746521,
    "faradaic_efficiency": 0.9322609901428223,
    "ohmic_efficiency": 0.9645636081695557,
    "pH_normalized": 0.19775448739528656,
    "precipitation_signal": 0.8540157079696655,
    "safety_risk": 0.072194404900074,
    "score": 0.7047813534736633,
    "selective_product_yield": 0.32688799500465393,
    "transport_efficiency": 0.9336105585098267
  }
}
```

### 批次 11 · 终点事件 77

```json
{
  "ordinal": 11,
  "lifecycle_index": 11,
  "end_step": 77,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.04
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 14400,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "metrics": {
    "cost": 0.31139999628067017,
    "electrochemical_conversion": 0.8540775775909424,
    "electrochemical_selectivity": 0.9688385128974915,
    "energy_efficiency": 0.598641574382782,
    "faradaic_efficiency": 0.45280465483665466,
    "ohmic_efficiency": 0.8796163201332092,
    "pH_normalized": 0.19873952865600586,
    "precipitation_signal": 0.8619048595428467,
    "safety_risk": 0.072194404900074,
    "score": 0.7382116317749023,
    "selective_product_yield": 0.8232585787773132,
    "transport_efficiency": 0.45998457074165344
  }
}
```

### 批次 12 · 终点事件 84

```json
{
  "ordinal": 12,
  "lifecycle_index": 12,
  "end_step": 84,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.04
    },
    {
      "current_mA": 300,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 14400,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "metrics": {
    "cost": 0.2998799979686737,
    "electrochemical_conversion": 0.7992426156997681,
    "electrochemical_selectivity": 0.9493532180786133,
    "energy_efficiency": 0.8867700099945068,
    "faradaic_efficiency": 0.6945759057998657,
    "ohmic_efficiency": 0.9421776533126831,
    "pH_normalized": 0.19925984740257263,
    "precipitation_signal": 0.8552408218383789,
    "safety_risk": 0.072194404900074,
    "score": 0.8255044221878052,
    "selective_product_yield": 0.7995275259017944,
    "transport_efficiency": 0.7158008217811584
  }
}
```

## K1 封存报告

Mechanistic account

I interpret this synthetic electrochemical world as a coupled charge-transfer, mass-transport, solution-resistance, acid/base, and precipitation system. The measured balanced-efficiency score is not controlled by conversion alone. It rewards selective product yield most strongly, while also rewarding selectivity, energy efficiency, faradaic efficiency, transport efficiency, ohmic efficiency, and conversion. Consequently, the best operating point is a compromise between delivering enough charge and avoiding inefficient high-current operation.

1. Core process model

A useful conceptual model is:

η_eff = V_applied − E_ref − ΔE_electrolyte − ΔE_solvent − iR

I_actual = min(I_cap, I_kinetic(η_eff), I_transport)

Q = ∫ I_actual dt

X ≈ 1 − exp(−k_productive Q/n_reagent)

Y_selective ≈ X × S × FE, with measurement and process deviations.

Here η_eff is an effective overpotential, I_cap is the configured current ceiling, iR represents ohmic loss, and I_transport is a mass-transfer ceiling. This is not an identified quantitative law; it is a compact explanation of the observed patterns. Electrolyte and solvent affect several terms simultaneously, including the potential shift, conductivity, diffusivity, diffusion-layer thickness, double-layer response, proton activity, and precipitation tendency. Hidden fixed world-specific residuals and solvent–electrolyte interactions further modify those nominal properties.

The productive polarity is positive under the directly compared S0/E0 conditions. Batch 1 used S0/E0, +1.0 V, a 100 mA cap, and 3600 s. It produced conversion 0.0810, selectivity 0.9496, selective product yield 0.0545, and score 0.5356. Batch 2 differed only in using −1.0 V; it produced conversion 0.0286, selectivity 0.6256, yield 0.0315, and score 0.3095. This matched comparison is the strongest evidence about potential sign. It suggests that positive polarization accesses the target pathway, whereas negative polarization mainly gives weak or inefficient conversion.

2. Current, time, and efficiency tradeoff

The S0/E1 series provides the clearest response surface. At +1.0 V and a 100 mA cap, increasing electrolysis time from 7200 s in batch 4 to 14400 s in batch 10 increased conversion from 0.1685 to 0.3598 and selective yield from 0.1655 to 0.3269. The score rose from 0.6237 to 0.7048. Selectivity remained high, increasing within assay variation from 0.9274 to 0.9751. Batch 10 also had energy efficiency 0.9472, faradaic efficiency 0.9323, transport efficiency 0.9336, and ohmic efficiency 0.9646. Thus, at the low current cap, additional time mostly delivered useful charge rather than causing a pronounced deterioration.

At 14400 s, current cap had a non-monotone effect on the balanced objective. Batch 11 raised the cap to 500 mA. Conversion reached 0.8541 and selective yield reached 0.8233, but energy efficiency fell to 0.5986, faradaic efficiency to 0.4528, transport efficiency to 0.4600, and ohmic efficiency to 0.8796. Its score was only 0.7382 despite the high yield. This is consistent with polarization, mass-transfer limitation, and parasitic charge consumption at high current.

Batch 12 used the intermediate 300 mA cap at the same +1.0 V and 14400 s. It gave the highest observed score, 0.8255, with conversion 0.7992, selective yield 0.7995, selectivity 0.9494, energy efficiency 0.8868, faradaic efficiency 0.6946, transport efficiency 0.7158, and ohmic efficiency 0.9422. The slight numerical excess of measured yield over measured conversion should not be interpreted literally; the two assay channels have independent stated noise. Mechanistically, batch 12 lies near the favorable knee of the current response: it supplies substantially more productive charge than 100 mA while avoiding much of the efficiency collapse seen at 500 mA.

A plausible current-dependent representation is:

FE(I) ≈ FE_0/[1 + (I/I_FE)^m]

T(I) ≈ 1/[1 + (I/I_lim)^n]

Y(I,t) ≈ [1 − exp(−a I t T(I))] × S(I) × FE(I).

This form naturally produces an intermediate current optimum for the weighted score. The three current-cap levels are too sparse to estimate a, I_FE, I_lim, m, or n uniquely. Moreover, configured cap is not necessarily identical to actual current at every moment.

3. Electrolyte effects

Batches 4–6 compared electrolytes E1, E2, and E3 in S0 at +1.0 V, 100 mA, and 7200 s. E1 was best: batch 4 scored 0.6237 with yield 0.1655, faradaic efficiency 0.9515, transport efficiency 0.9200, and energy efficiency 0.8932. E2 in batch 5 scored 0.5978 with yield 0.1548, faradaic efficiency 0.8646, transport efficiency 0.8541, and energy efficiency 0.8643. E3 in batch 6 scored 0.5539 with yield 0.1262, faradaic efficiency 0.6970, transport efficiency 0.6723, and energy efficiency 0.8996. All retained high measured selectivity near 0.926.

This ordering is consistent with E1 offering a favorable transport–kinetics compromise. Its nominal diffusion layer is thinner and its diffusivity higher than E0, while its standard-potential shift is neutral. E0 has high nominal bulk conductivity but a much thicker diffusion layer and lower diffusivity. E2 has a thinner layer but lower conductivity, a positive potential shift, and stronger acidity. E3 has good conductivity but low diffusivity and a negative potential shift. The experiments show that conductivity alone does not rank performance: transport, interfacial kinetics, effective potential, and hidden interaction terms matter.

The comparison with E0 is not perfectly matched in time. Batch 1 used E0 for only 3600 s and obtained a low conversion of 0.0810; batch 4 used E1 for 7200 s and obtained 0.1685. Therefore, the campaign does not isolate E0 versus E1 at equal duration. The E1 conclusion rests on its superior results among the matched E1/E2/E3 comparison and its strong behavior during later current/time optimization, not on an exact E0/E1 causal contrast.

4. Solvent effects and couplings

Batches 4 and 7–9 compared solvents with E1 at +1.0 V, 100 mA, and 7200 s. S0/E1 in batch 4 scored 0.6237. S1/E1 in batch 7 scored 0.5930, with conversion 0.1661, yield 0.1488, and selectivity 0.9068. S2/E1 in batch 8 scored 0.5167, with conversion 0.1337, yield 0.0902, and selectivity 0.7948. S3/E1 in batch 9 scored 0.5900, with conversion 0.1511, yield 0.1542, and selectivity 0.8861. S0 therefore gave the best tested balance, though batches 7 and 9 were reasonably competitive.

S0 has the highest nominal relative conductivity but only moderate relative diffusivity. Its strong performance suggests that low solution resistance and a favorable potential/interfacial coupling outweigh its diffusion disadvantage in this fixture. S1 has higher nominal diffusivity but lower conductivity; S2 has both low conductivity and low proton activity; S3 is intermediate in conductivity but low in diffusivity. The observed solvent ranking again shows that no single dossier property determines the outcome.

Safety risk also depended on solvent under these otherwise similar conditions. It was approximately 0.0722 for S0, 0.0956 for S1, 0.1136 for S2, and 0.1262 for S3. These values are observations from the tested recipes, not universal solvent constants, but they further favor S0 for this operating region.

The clearest evidence for strong material coupling is batch 3. S1/E0 at +1.2 V, 300 mA, and 7200 s produced measured conversion, selective yield, faradaic efficiency, transport efficiency, and energy efficiency all at zero, while ohmic efficiency remained 0.9851. This result cannot be attributed uniquely to potential, current, solvent, electrolyte, or their interaction because all differed from the best baseline. Plausible explanations include an unfavorable effective-potential window, interfacial passivation, a solvent–electrolyte kinetic incompatibility, or complete diversion into an unobserved/nonproductive pathway. It cautions against extrapolating the successful S0/E1 current response to other material pairs.

5. Selectivity and potential window

Within the successful +1.0 V experiments, electrochemical selectivity was usually high: 0.927–0.975 for S0/E1 across batches 4, 10, 11, and 12. Raising current from 100 to 500 mA at fixed potential and duration reduced efficiencies much more than it reduced selectivity. This suggests that the high-current penalty is primarily wasted charge, transport polarization, and ohmic loss rather than wholesale loss of chemical pathway discrimination.

Nevertheless, the batch-3 failure at +1.2 V is consistent with a finite productive potential window. I conjecture that target formation is favored once positive overpotential exceeds an onset, but performance may collapse outside a material-dependent window because of passivation or competing reactions. Only one +1.2 V experiment was performed, and it used a different material pair, so the campaign cannot distinguish an excessive-potential effect from a material interaction. No general quadratic potential optimum is identified.

6. Acid/base and precipitation behavior

The pH-normalized measurement was material dependent but comparatively stable within S0/E1: 0.1991 in batch 4, 0.1978 in batch 10, 0.1987 in batch 11, and 0.1993 in batch 12. This stability while current and conversion changed substantially suggests that the E1/S0 acid–base environment is buffered or dominated by the electrolyte formulation rather than by conversion alone.

Precipitation_signal did not behave as a simple predictor of failure. It was 1.000 in batch 1, 0.849 in batch 4, 0 in batch 5, 0.0024 in batch 6, and about 0.709, 0.582, and 0.609 in batches 7–9. In the optimized S0/E1 series it remained about 0.854–0.862 in batches 10–12, even while batch 12 achieved the best score. Thus, high precipitation_signal may indicate a state feature or incipient solid formation without necessarily preventing productive electrolysis in this benchmark. Alternatively, its direction or calibration may not support the naive interpretation that larger always means worse. Because the campaign did not independently manipulate precipitation or inspect solids, its mechanistic role is unidentifiable.

7. Relationship to the balanced score

The public objective assigns its largest weight to selective product yield, followed by electrochemical selectivity and energy efficiency, then faradaic efficiency, conversion, transport efficiency, and ohmic efficiency. This explains why batch 11, despite serious efficiency losses, still outscored batch 10: its yield gain was large. Batch 12 improved the compromise by retaining almost the same high-yield regime while recovering much of the energy, faradaic, transport, and ohmic performance.

The yield gate also matters. Batches with selective yield below approximately 0.02 would be multiplicatively suppressed. No successful recommended candidate was near that boundary, while batch 3 had zero yield and therefore necessarily scored zero.

8. Scope and confidence

The strongest findings are local to 0.020 mol reagent in 0.040 L solvent, the common loading used throughout the campaign. The data support positive rather than negative polarity for S0/E0; S0/E1 as the best tested pair; longer operation up to 14400 s at +1.0 V; and an intermediate 300 mA current cap as superior to 100 and 500 mA for the balanced objective. Batch 12 is the best direct observation, not an extrapolated optimum.

Fine optimization remains uncertain. There were no replicate batches, and final-assay uncertainties include roughly 0.01 for selective yield and conversion, 0.012 for selectivity/faradaic/ohmic efficiency, 0.014 for transport efficiency, and 0.016 for energy efficiency. These uncertainties are small relative to the major gaps between batches 10–12 but prevent overinterpreting small differences among materials. The true current optimum could lie between the tested caps, and potential values near +1.0 V were not finely scanned.

Unidentifiable factors include actual current trajectories, electrode area and gap, world-specific contact resistance, electrode surface state, kinetic constants, electron stoichiometry, mass-transfer coefficients, identities and amounts of side products, and the hidden correlated residuals in each solvent–electrolyte pair. The campaign also cannot separate time from total charge without recorded current, nor determine whether batch 3 reflects passivation, inactivity, degradation, or an unfavorable effective potential.

Plausible alternative models include: a purely empirical material-specific response surface without transferable electrochemical structure; stochastic passivation causing the isolated batch-3 zero; a hard threshold in effective potential rather than a smooth Butler–Volmer-like response; or current-dependent heating/interfacial changes not exposed in the public measurements. The consistent current-efficiency pattern in batches 10–12 favors the charge-transfer/transport interpretation, but it does not uniquely prove it.

Overall, my best explanation is that S0/E1 places the cell in a favorable positive-potential window with good conductivity, adequate transport, and stable selectivity. At low current, conversion is charge-limited. At very high current, conversion rises but faradaic, transport, energy, and ohmic efficiencies deteriorate. A 300 mA cap over 14400 s reaches a favorable intermediate regime, producing the best observed balance without approaching the safety limit.

## K2 封存报告

1. Claims and laws

No instance-specific prior law or prior outcome table was supplied. The supplied information consisted of nominal material properties, instrument/scoring contracts, and hidden-residual warnings. My initial laws were therefore self-developed hypotheses rather than supplied ground truth.

Supported:
- Positive polarity was favored over negative polarity in the only matched comparison. Batch 1 (+1.0 V, S0/E0) scored 0.536 versus 0.310 for batch 2 at −1.0 V, with higher conversion, selectivity, yield, and efficiencies. This changed the potential sign from unresolved to supported-positive within that scope.
- A current–efficiency tradeoff was supported by batches 10–12. At S0/E1, +1.0 V, and 14400 s, increasing the cap from 100 to 300 mA greatly increased yield while retaining useful efficiency; 500 mA raised yield further but sharply reduced faradaic, transport, energy, and ohmic efficiencies. The resulting intermediate optimum in score supported the proposed coupled charge/transport model.
- Longer electrolysis was beneficial in the tested low-current regime: batch 10 outperformed batch 4 when duration increased from 7200 to 14400 s at otherwise matched S0/E1 conditions.
- Material effects were coupled rather than governed by conductivity alone. E1 was best among the matched S0/E1, S0/E2, and S0/E3 tests in batches 4–6, while S0 was best among the matched E1 solvent tests in batches 4 and 7–9.

Contradicted or weakened:
- A simple claim that the most nominally conductive electrolyte should be best was weakened: E0 had higher nominal conductivity, yet E1 produced the strongest optimized behavior. Conductivity was evidently only one component.
- My initial concern that E3 would necessarily fail through precipitation was not supported. Batch 6 had little measured precipitation signal and remained productive, though its transport and faradaic efficiencies were inferior to E1.
- Precipitation_signal was contradicted as a simple monotonic failure indicator. It remained about 0.85–0.86 in the successful optimized batches 10–12.

Untested or unresolved:
- A transferable quantitative Butler–Volmer, mass-transfer, or exponential conversion law was not identified.
- Whether batch 3’s zero conversion arose from excessive potential, S1/E0 coupling, passivation, or stochastic failure remains unresolved because several factors changed together.
- The exact optimum near 300 mA and +1.0 V was untested between sparse levels, and none of the leading conditions was replicated.

2. One additional discriminating experiment

I would repeat the batch-12 material/loading/potential recipe—S0/E1, 0.020 mol reagent, 0.040 L solvent, +1.0 V—but use a 500 mA cap for 8640 s. Its nominal cap×time charge equals that of batch 12 at 300 mA for 14400 s.

The leading explanation predicts a current-density penalty: relative to batch 12, the proposed batch should show lower faradaic, transport, energy, and ohmic efficiencies, and probably lower selective yield per nominal charge. A competing total-charge model predicts similar conversion and yield because nominal charge is matched, with only modest metric differences.

If yield and conversion closely matched batch 12 while efficiencies also remained similar, I would weaken the current-dependent polarization explanation and favor total delivered charge/time as the dominant variable. If yield were similar but efficiencies were lower, I would retain a current-dependent loss mechanism while concluding that enough excess charge compensates for it. If both yield and efficiencies were substantially lower, that would strongly support transport limitation or interfacial polarization at high current. A complete or erratic failure would increase the plausibility of passivation or stochastic state changes and would reduce confidence in a smooth response law.

3. Unused evidence, reliability, and goal effects

Most raw spectral traces and artifact-level peak shapes were unused; I relied primarily on processed final-assay estimates. Intermediate UV–vis measurements were inspected operationally but not fitted quantitatively. I also did not exploit the full nominal acid, capacitance, solubility-product, temperature, cost, or spectral metadata because the campaign contained too few independently varied experiments to identify their effects. There were no replicates, so between-batch process variability could not be separated from treatment effects.

The least reliable blind predictions are Q10 (untested S2/E0 coupling), Q11–Q12 (high-current E0 behavior at an untested potential), and Q05/Q07 (negative polarity with electrolytes not tested at negative potential). Q01 and Q02 are also uncertain because their short duration places predicted yield near the 0.02 multiplicative gate, making score sensitive to small yield errors.

Batch 12 is the strongest observed recommendation but is only a local, unreplicated optimum. Its exact transfer to nearby potentials, concentrations, fixtures, or material pairs is less reliable than its superiority within the tested campaign.

The assigned maximization goal clearly affected evidence collection. Early batches established polarity and screened materials, but later batches concentrated on improving score around S0/E1 rather than completing a balanced mechanistic factorial design or obtaining replicates. This improved the operating recommendation but left potential–material confounding, uncertainty about batch 3, and the exact current optimum unresolved. I see no direct conflict between the goal and honest interpretation, but the adaptive optimization reduced the breadth of causal evidence.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.38,
        "upper80": 0.76
      },
      "energy_efficiency": {
        "estimate": 0.23,
        "lower80": 0.08,
        "upper80": 0.4
      },
      "faradaic_efficiency": {
        "estimate": 0.38,
        "lower80": 0.22,
        "upper80": 0.55
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.18,
        "lower80": 0.03,
        "upper80": 0.34
      },
      "selective_product_yield": {
        "estimate": 0.012,
        "lower80": 0,
        "upper80": 0.035
      },
      "transport_efficiency": {
        "estimate": 0.4,
        "lower80": 0.22,
        "upper80": 0.58
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.9,
        "lower80": 0.78,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.72,
        "lower80": 0.55,
        "upper80": 0.86
      },
      "faradaic_efficiency": {
        "estimate": 0.78,
        "lower80": 0.64,
        "upper80": 0.9
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.5,
        "lower80": 0.38,
        "upper80": 0.58
      },
      "selective_product_yield": {
        "estimate": 0.022,
        "lower80": 0.005,
        "upper80": 0.055
      },
      "transport_efficiency": {
        "estimate": 0.75,
        "lower80": 0.6,
        "upper80": 0.88
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.48,
        "upper80": 0.75
      },
      "energy_efficiency": {
        "estimate": 0.24,
        "lower80": 0.12,
        "upper80": 0.38
      },
      "faradaic_efficiency": {
        "estimate": 0.38,
        "lower80": 0.25,
        "upper80": 0.52
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.313,
        "lower80": 0.24,
        "upper80": 0.39
      },
      "selective_product_yield": {
        "estimate": 0.045,
        "lower80": 0.02,
        "upper80": 0.08
      },
      "transport_efficiency": {
        "estimate": 0.41,
        "lower80": 0.28,
        "upper80": 0.55
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.94,
        "lower80": 0.86,
        "upper80": 0.99
      },
      "energy_efficiency": {
        "estimate": 0.81,
        "lower80": 0.68,
        "upper80": 0.92
      },
      "faradaic_efficiency": {
        "estimate": 0.84,
        "lower80": 0.72,
        "upper80": 0.94
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.568,
        "lower80": 0.5,
        "upper80": 0.64
      },
      "selective_product_yield": {
        "estimate": 0.11,
        "lower80": 0.07,
        "upper80": 0.16
      },
      "transport_efficiency": {
        "estimate": 0.81,
        "lower80": 0.68,
        "upper80": 0.92
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.38,
        "upper80": 0.74
      },
      "energy_efficiency": {
        "estimate": 0.22,
        "lower80": 0.08,
        "upper80": 0.39
      },
      "faradaic_efficiency": {
        "estimate": 0.34,
        "lower80": 0.17,
        "upper80": 0.51
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.293,
        "lower80": 0.18,
        "upper80": 0.37
      },
      "selective_product_yield": {
        "estimate": 0.035,
        "lower80": 0.01,
        "upper80": 0.07
      },
      "transport_efficiency": {
        "estimate": 0.39,
        "lower80": 0.22,
        "upper80": 0.56
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.93,
        "lower80": 0.84,
        "upper80": 0.99
      },
      "energy_efficiency": {
        "estimate": 0.86,
        "lower80": 0.74,
        "upper80": 0.95
      },
      "faradaic_efficiency": {
        "estimate": 0.91,
        "lower80": 0.8,
        "upper80": 0.98
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.593,
        "lower80": 0.52,
        "upper80": 0.66
      },
      "selective_product_yield": {
        "estimate": 0.12,
        "lower80": 0.075,
        "upper80": 0.18
      },
      "transport_efficiency": {
        "estimate": 0.88,
        "lower80": 0.76,
        "upper80": 0.96
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.4,
        "upper80": 0.76
      },
      "energy_efficiency": {
        "estimate": 0.25,
        "lower80": 0.09,
        "upper80": 0.43
      },
      "faradaic_efficiency": {
        "estimate": 0.32,
        "lower80": 0.15,
        "upper80": 0.5
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.297,
        "lower80": 0.18,
        "upper80": 0.38
      },
      "selective_product_yield": {
        "estimate": 0.04,
        "lower80": 0.01,
        "upper80": 0.08
      },
      "transport_efficiency": {
        "estimate": 0.35,
        "lower80": 0.17,
        "upper80": 0.53
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.92,
        "lower80": 0.82,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.82,
        "lower80": 0.68,
        "upper80": 0.93
      },
      "faradaic_efficiency": {
        "estimate": 0.62,
        "lower80": 0.46,
        "upper80": 0.77
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.515,
        "lower80": 0.43,
        "upper80": 0.59
      },
      "selective_product_yield": {
        "estimate": 0.1,
        "lower80": 0.055,
        "upper80": 0.155
      },
      "transport_efficiency": {
        "estimate": 0.6,
        "lower80": 0.44,
        "upper80": 0.75
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.5,
        "lower80": 0.28,
        "upper80": 0.7
      },
      "energy_efficiency": {
        "estimate": 0.15,
        "lower80": 0.02,
        "upper80": 0.34
      },
      "faradaic_efficiency": {
        "estimate": 0.25,
        "lower80": 0.08,
        "upper80": 0.44
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.243,
        "lower80": 0.08,
        "upper80": 0.36
      },
      "selective_product_yield": {
        "estimate": 0.02,
        "lower80": 0,
        "upper80": 0.055
      },
      "transport_efficiency": {
        "estimate": 0.3,
        "lower80": 0.11,
        "upper80": 0.5
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.85,
        "lower80": 0.58,
        "upper80": 0.97
      },
      "energy_efficiency": {
        "estimate": 0.45,
        "lower80": 0.16,
        "upper80": 0.7
      },
      "faradaic_efficiency": {
        "estimate": 0.55,
        "lower80": 0.26,
        "upper80": 0.78
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.404,
        "lower80": 0.12,
        "upper80": 0.5
      },
      "selective_product_yield": {
        "estimate": 0.04,
        "lower80": 0,
        "upper80": 0.1
      },
      "transport_efficiency": {
        "estimate": 0.5,
        "lower80": 0.22,
        "upper80": 0.73
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.5,
        "lower80": 0.3,
        "upper80": 0.69
      },
      "energy_efficiency": {
        "estimate": 0.12,
        "lower80": 0.02,
        "upper80": 0.28
      },
      "faradaic_efficiency": {
        "estimate": 0.18,
        "lower80": 0.05,
        "upper80": 0.36
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.243,
        "lower80": 0.12,
        "upper80": 0.38
      },
      "selective_product_yield": {
        "estimate": 0.08,
        "lower80": 0.02,
        "upper80": 0.2
      },
      "transport_efficiency": {
        "estimate": 0.22,
        "lower80": 0.06,
        "upper80": 0.41
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.91,
        "lower80": 0.78,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.58,
        "lower80": 0.4,
        "upper80": 0.74
      },
      "faradaic_efficiency": {
        "estimate": 0.45,
        "lower80": 0.29,
        "upper80": 0.62
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.565,
        "lower80": 0.46,
        "upper80": 0.69
      },
      "selective_product_yield": {
        "estimate": 0.41,
        "lower80": 0.22,
        "upper80": 0.65
      },
      "transport_efficiency": {
        "estimate": 0.46,
        "lower80": 0.29,
        "upper80": 0.63
      }
    }
  ],
  "rationale": "Predictions are anchored to the matched S0/E0 polarity results, the S0/E1 electrolyte and duration series, and the observed 100–300–500 mA efficiency tradeoff. I treated 0.8 V as a milder version of the tested 1.0 V regime, scaled short-time yield downward, and allowed high current to increase conversion/yield while reducing faradaic, transport, and energy efficiencies. Intervals are wider for untested negative-polarity, S2/E0, and high-current combinations because material–potential coupling caused a complete failure in one campaign batch. Score estimates apply the published component weighting and account for the selective-yield gate, which especially enlarges uncertainty near 0.02 yield."
}
```
