# repeat-01/EC-W03-B12-discovery-E-MisIndexed

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-01\EC-W03-B12-discovery-E-MisIndexed\participant\discovery-E-MisIndexed

## 同期笔记

### v1 · 公开事件 0

# Electrochemical hypothesis notebook

## Prior expectations (before physical experiments)

**H1 [tentative]** At fixed loading, conversion should increase with electrolysis duration and with delivered charge until reactant depletion, while faradaic/energy efficiency may fall at excessive potential or long duration because parasitic current grows.

**H2 [tentative]** Potential sign and magnitude should strongly control target selectivity. Because the redox direction is unknown, I will bracket both signs at matched magnitude before narrowing the favorable polarity.

**H3 [tentative]** Transport and ohmic efficiency should improve with nominal conductivity and diffusivity but may trade off against precipitation and proton activity. E0/S0 is a conductivity-rich baseline; E3 and S1 provide higher diffusivity contrasts; E2 provides acidity/thin diffusion layer but poor conductivity.

Testable consequences: matched-sign comparisons will identify polarity; a potential series will show threshold/overdrive; duration and current-cap contrasts will separate kinetic/charge limitation from selectivity loss; material changes at fixed loading and waveform will reveal transport/interface shifts. These expectations will be revised only from public observations.

### v2 · 公开事件 28

# Electrochemical hypothesis notebook

## H1 [tentative]
At fixed loading, conversion should increase with duration and delivered charge until depletion; excessive duration/current may reduce faradaic or energy efficiency. A duration/current series remains needed.

## H2 [supported only locally; nonmonotonic]
The response is strongly polarity- and magnitude-dependent, not a simple function of |V|. At S0/E0, 100 mA cap, 300 s, +1 V gave high selectivity and efficiencies with small positive conversion, whereas +2 V collapsed conversion/selectivity/faradaic/transport signals (events runner-operation-0007, -0021). Negative settings produced essentially zero conversion and poorer efficiency; apparent tiny yields at -1/-2 V are comparable to final-assay yield uncertainty and conflict with zero target-proxy signal/conversion, so are not evidence of productive chemistry (events -0014, -0028). The useful positive window appears bounded below +2 V. Test next: lengthen electrolysis at +1 V, and later probe an intermediate positive potential if capacity permits.

## H3 [tentative]
Transport/ohmic effects should depend on nominal conductivity/diffusivity, but precipitation may confound productivity. S0/E0 shows precipitation signal near 1 in all four polarity tests, so its otherwise strong ohmic efficiency may not translate into isolated yield. Material contrasts should test whether lower precipitation propensity outweighs conductivity loss.

## Interpretive caution
Final-assay standard deviations make near-zero conversion/yield estimates ambiguous; mechanistic claims will emphasize contrasts much larger than the declared noise and coherent shifts across conversion, selectivity, and efficiency channels.

### v3 · 公开事件 77

# Electrochemical hypothesis notebook

## H1 [supported in tested range; saturating/charge-limited]
At S0/E0 and +1 V, extending 300 to 3000 s raised conversion from about 0.014 to 0.061 and selective yield from ~0 (below resolution) to 0.056 while selectivity stayed near 0.84 (events runner-operation-0007, -0035). The less-than-tenfold conversion gain suggests current/transport decay or nonlinear saturation. At -1 V, long duration also produced coherent target formation but at roughly half the conversion and much poorer faradaic/transport efficiency (event -0042), so both signs are productive over long times but with different kinetic/selectivity branches.

## H2 [supported locally; bounded potential window]
At fixed S0/E0, +1 V is substantially more productive and efficient than -1 V; ±2 V are outside the useful window under these conditions (events -0007, -0014, -0021, -0028, -0035, -0042). This is consistent with a potential-window model rather than monotonic overpotential response.

## H3 [supported: current-cap tradeoff]
At +1 V, 3000 s, lowering the cap from 100 to 10 mA reduced conversion/yield while increasing faradaic, transport, ohmic and energy efficiencies; raising it to 500 mA retained similar conversion but sharply degraded those efficiencies and yield (events -0035, -0049, -0056). Thus the cap is active at 10 mA, 100 mA is a favorable compromise, and 500 mA drives parasitic/transport losses. Since cap is not guaranteed current, prediction should use a saturating delivered-current dependence, not assume charge = cap×time.

## H4 [supported for matched +1 V/100 mA/3000 s]
Material choice changes more than conductivity. S1/E1 was best: conversion ~0.069, selectivity ~0.939, yield ~0.084 and efficiencies ~0.90–0.99 with reduced (not absent) precipitation (event -0063). S2/E2 suppressed precipitation completely and gave slightly higher conversion but lower selectivity/yield/efficiency (event -0070). S3/E3 also suppressed precipitation but had weaker selectivity/faradaic transport performance (event -0077). S0/E0 had near-complete precipitation and lower yield (event -0035). Therefore precipitation alone does not determine productivity; interfacial selectivity and charge efficiency dominate, with S1/E1 the observed optimum.

## Final prospective test
Use S1/E1 at +1 V, 100 mA cap for 12000 s. Prediction: conversion and yield should exceed the 3000 s result, but sublinearly; selectivity should remain high unless depletion/overelectrolysis becomes important. A large selectivity or efficiency collapse would reject extrapolation of the favorable window to long duration.

### v4 · 公开事件 84

# Electrochemical hypothesis notebook — final source-stage interpretation

## H1 [supported in sampled duration range]
Product formation is time/charge dependent but sublinear. At +1 V and 100 mA cap, S0/E0 rose from conversion 0.014 at 300 s to 0.061 at 3000 s (events runner-operation-0007, -0035). For S1/E1, increasing 3000 to 12000 s raised conversion from 0.069 to 0.266 and yield from 0.084 to 0.279 while retaining selectivity ~0.93 and high efficiencies (events -0063, -0084). The S1/E1 long-time change is near proportional within assay uncertainty, whereas S0/E0's earlier comparison was sublinear; duration law is therefore material-dependent or confounded by low-end measurement noise.

## H2 [supported locally; polarity and potential-window mechanism]
At S0/E0, +1 V outperformed -1 V at both 300 and 3000 s; negative polarity remained productive only after longer electrolysis and had markedly poorer faradaic/transport/energy efficiency. Both +2 and -2 V at 300 s were essentially unproductive, with +2 V especially collapsing faradaic and transport signals (events -0007, -0014, -0021, -0028, -0035, -0042). Prediction should use polarity-specific bounded activation windows rather than |V| monotonicity.

## H3 [supported; current cap produces rate–efficiency tradeoff]
At S0/E0, +1 V, 3000 s: 10 mA cap yielded low conversion but best efficiencies; 100 mA increased conversion/yield with still-good efficiencies; 500 mA did not improve conversion beyond uncertainty and strongly lowered faradaic, transport and energy efficiency (events -0049, -0035, -0056). Model delivered current as capped and saturating, with parasitic loss increasing at high cap.

## H4 [supported for matched conditions]
At +1 V, 100 mA, 3000 s, material ranking reflects coupled kinetics/transport/precipitation rather than a single nominal property. S1/E1 gave the best coherent outcome (high selectivity and efficiencies, moderate precipitation); S2/E2 and S3/E3 nearly eliminated precipitation but sacrificed selectivity or charge/transport efficiency; S0/E0 precipitated strongly (events -0035, -0063, -0070, -0077). The result argues against precipitation as the sole limiter. Nominal potential shifts alone also do not explain the ranking.

## Working predictive account
Conversion follows accumulated productive charge with a material- and sign-dependent activation factor, saturation/depletion at high extent, and a current-cap/transport ceiling. Selective yield is approximately conversion × intrinsic material/polarity selectivity plus assay noise, while faradaic and energy efficiencies fall when cap or potential drives parasitic current. Precipitation is a parallel material-dependent state indicator that can reduce accessible product but is not sufficient to predict yield.

## Recommendation decision
Batch 12 (S1/E1, +1 V, 100 mA cap, 12000 s at 0.02 mol in 0.04 L) is the strongest tested operating point: highest selective yield and score, high selectivity and efficiencies, and safety risk below the stated limit (event -0084). This is an observed optimum, not proof of global optimality; the main unresolved gaps are replication, intermediate positive potentials, crossed solvent/electrolyte combinations, and longer-time depletion/overelectrolysis.

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
      "duration_s": 300,
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
    "cost": 0.28271999955177307,
    "electrochemical_conversion": 0.01392891351133585,
    "electrochemical_selectivity": 0.8394781947135925,
    "energy_efficiency": 0.7378983497619629,
    "faradaic_efficiency": 0.7854432463645935,
    "ohmic_efficiency": 0.9659870862960815,
    "pH_normalized": 0.23031213879585266,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.7567394971847534
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
      "duration_s": 300,
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
    "cost": 0.28271999955177307,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.5403205752372742,
    "energy_efficiency": 0.2102794200181961,
    "faradaic_efficiency": 0.36285680532455444,
    "ohmic_efficiency": 0.9748249650001526,
    "pH_normalized": 0.2276168018579483,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.14466306567192078,
    "selective_product_yield": 0.01047626230865717,
    "transport_efficiency": 0.3891136050224304
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
      "solvent": 0,
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 2
    },
    {
      "duration_s": 300,
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
    "cost": 0.2828400135040283,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.0,
    "ohmic_efficiency": 0.9740350842475891,
    "pH_normalized": 0.2283317893743515,
    "precipitation_signal": 0.9871104955673218,
    "safety_risk": 0.072194404900074,
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
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -2
    },
    {
      "duration_s": 300,
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
    "cost": 0.2828400135040283,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.39477163553237915,
    "energy_efficiency": 0.01755278743803501,
    "faradaic_efficiency": 0.25971290469169617,
    "ohmic_efficiency": 0.9861932396888733,
    "pH_normalized": 0.22764120995998383,
    "precipitation_signal": 0.9878587126731873,
    "safety_risk": 0.072194404900074,
    "score": 0.015143711119890213,
    "selective_product_yield": 0.0015516281127929688,
    "transport_efficiency": 0.22822536528110504
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
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 3000,
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
    "cost": 0.28380000591278076,
    "electrochemical_conversion": 0.061047278344631195,
    "electrochemical_selectivity": 0.8355644941329956,
    "energy_efficiency": 0.6855505108833313,
    "faradaic_efficiency": 0.7520089149475098,
    "ohmic_efficiency": 0.9731909036636353,
    "pH_normalized": 0.23260200023651123,
    "precipitation_signal": 0.9871851205825806,
    "safety_risk": 0.072194404900074,
    "score": 0.49338477849960327,
    "selective_product_yield": 0.05622175708413124,
    "transport_efficiency": 0.7414994835853577
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
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1
    },
    {
      "duration_s": 3000,
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
    "cost": 0.28380000591278076,
    "electrochemical_conversion": 0.03036843240261078,
    "electrochemical_selectivity": 0.5345399975776672,
    "energy_efficiency": 0.21824978291988373,
    "faradaic_efficiency": 0.38706278800964355,
    "ohmic_efficiency": 0.9750476479530334,
    "pH_normalized": 0.229326069355011,
    "precipitation_signal": 0.9978154301643372,
    "safety_risk": 0.072194404900074,
    "score": 0.28423482179641724,
    "selective_product_yield": 0.02530071884393692,
    "transport_efficiency": 0.3623794615268707
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
      "solvent": 0,
      "volume_L": 0.04
    },
    {
      "current_mA": 10,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 3000,
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
    "cost": 0.28271999955177307,
    "electrochemical_conversion": 0.017223980277776718,
    "electrochemical_selectivity": 0.8253258466720581,
    "energy_efficiency": 0.8254925012588501,
    "faradaic_efficiency": 0.8860611319541931,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.22834065556526184,
    "precipitation_signal": 0.9828575253486633,
    "safety_risk": 0.072194404900074,
    "score": 0.34294381737709045,
    "selective_product_yield": 0.012977712787687778,
    "transport_efficiency": 0.8894615173339844
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
      "solvent": 0,
      "volume_L": 0.04
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 3000,
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
    "cost": 0.28859999775886536,
    "electrochemical_conversion": 0.05258758366107941,
    "electrochemical_selectivity": 0.8236374855041504,
    "energy_efficiency": 0.13811898231506348,
    "faradaic_efficiency": 0.15624837577342987,
    "ohmic_efficiency": 0.8924130201339722,
    "pH_normalized": 0.2266431748867035,
    "precipitation_signal": 0.9957303404808044,
    "safety_risk": 0.072194404900074,
    "score": 0.2627195119857788,
    "selective_product_yield": 0.026930466294288635,
    "transport_efficiency": 0.14975303411483765
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
      "duration_s": 3000,
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
    "cost": 0.29980000853538513,
    "electrochemical_conversion": 0.06865853071212769,
    "electrochemical_selectivity": 0.9388172626495361,
    "energy_efficiency": 0.9449468851089478,
    "faradaic_efficiency": 0.8990811705589294,
    "ohmic_efficiency": 0.9933291673660278,
    "pH_normalized": 0.2107059806585312,
    "precipitation_signal": 0.6674489378929138,
    "safety_risk": 0.09559440612792969,
    "score": 0.5940123796463013,
    "selective_product_yield": 0.08411522954702377,
    "transport_efficiency": 0.9199123978614807
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
      "solvent": 2,
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 3000,
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
    "cost": 0.3253999948501587,
    "electrochemical_conversion": 0.07408522069454193,
    "electrochemical_selectivity": 0.8087707161903381,
    "energy_efficiency": 0.7552710771560669,
    "faradaic_efficiency": 0.764382541179657,
    "ohmic_efficiency": 0.9269829988479614,
    "pH_normalized": 0.17182955145835876,
    "precipitation_signal": 0.0,
    "safety_risk": 0.1135944053530693,
    "score": 0.4976520836353302,
    "selective_product_yield": 0.04393177479505539,
    "transport_efficiency": 0.7657321095466614
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
      "solvent": 3,
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 3000,
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
    "cost": 0.3093999922275543,
    "electrochemical_conversion": 0.054484765976667404,
    "electrochemical_selectivity": 0.7129852771759033,
    "energy_efficiency": 0.6620658040046692,
    "faradaic_efficiency": 0.5300768613815308,
    "ohmic_efficiency": 0.978295624256134,
    "pH_normalized": 0.2838279902935028,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.12619440257549286,
    "score": 0.41666606068611145,
    "selective_product_yield": 0.031204581260681152,
    "transport_efficiency": 0.5372567772865295
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
      "duration_s": 12000,
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
    "cost": 0.3034000098705292,
    "electrochemical_conversion": 0.26583221554756165,
    "electrochemical_selectivity": 0.9306500554084778,
    "energy_efficiency": 0.9049294590950012,
    "faradaic_efficiency": 0.8736225962638855,
    "ohmic_efficiency": 0.9796068668365479,
    "pH_normalized": 0.20989719033241272,
    "precipitation_signal": 0.6578359007835388,
    "safety_risk": 0.09559440612792969,
    "score": 0.6581918597221375,
    "selective_product_yield": 0.27861228585243225,
    "transport_efficiency": 0.8948475122451782
  }
}
```

## K1 封存报告

# Mechanism report

## 1. Experimental scope

All batches used 0.020 mol of anonymous limiting reagent in 0.040 L solvent, corresponding nominally to 0.50 mol L⁻¹ before sampling. I varied applied potential, current cap, electrolysis duration, and paired solvent/electrolyte formulation. Final-assay uncertainties were approximately 0.010 for conversion and selective yield, 0.012 for selectivity and faradaic efficiency, 0.014 for transport efficiency, and 0.016 for energy efficiency. Consequently, isolated values near zero should not be overinterpreted.

The strongest observed condition was batch 12: solvent-S1/electrolyte-E1, +1 V, 100 mA current cap, and 12000 s. It produced conversion 0.2658, selectivity 0.9307, selective-product yield 0.2786, faradaic efficiency 0.8736, transport efficiency 0.8948, ohmic efficiency 0.9796, energy efficiency 0.9049, precipitation signal 0.6578, and score 0.6582. Its safety risk was 0.0956, well below the stated 0.65 limit.

## 2. Proposed working mechanism

I interpret the system as a potential-gated electrochemical conversion whose productive rate is controlled jointly by interfacial activation, delivered charge, mass transport, and competing parasitic current. Material identity changes all of those factors and also controls a parallel precipitation process.

A useful qualitative model is:

- Delivered current: I_del(t) = min[I_cap, I_kin(V,m), I_transport(X,m,t)].
- Productive current: I_prod = FE(V,I_cap,m,X) × I_del.
- Conversion rate: dX/dt = k_m × A_m(V,sign) × I_prod × g_transport(m,I_cap,X) × g_depletion(X).
- Target formation rate: dY_target/dt ≈ S_m(V,sign,I_cap,X) × dX/dt, with additional effects from precipitation or product accessibility.
- Parasitic current increases when the potential magnitude or current cap exceeds the useful interfacial/transport window.

Here m denotes the coupled solvent/electrolyte/electrode environment, A_m is a polarity-specific activation-window function, FE is faradaic efficiency, S_m is intrinsic target selectivity, and g_depletion declines as accessible reactant is consumed. The current setting is only a cap; it is not evidence that the cell passed exactly I_cap × t charge.

A plausible activation form would be a bounded window rather than a monotonic function of absolute potential, for example:

A_m(V) = sigmoid[(V − V_on,m)/w_on] × sigmoid[(V_off,m − V)/w_off]

for the favorable positive branch, with a separate weaker function for negative polarity. This captures activation near +1 V and collapse outside the useful window without claiming a uniquely identified equation.

## 3. Evidence for a polarity-specific potential window

Batches 1–4 bracketed potential at S0/E0, 100 mA, and 300 s:

- Batch 1, +1 V: conversion 0.0139, selectivity 0.8395, faradaic efficiency 0.7854, transport efficiency 0.7567, and energy efficiency 0.7379.
- Batch 2, −1 V: reported conversion 0, selectivity 0.5403, faradaic efficiency 0.3629, transport efficiency 0.3891, and energy efficiency 0.2103.
- Batch 3, +2 V: conversion, selectivity, faradaic efficiency, transport efficiency, and energy efficiency all reported as 0.
- Batch 4, −2 V: conversion 0, selectivity 0.3948, faradaic efficiency 0.2597, transport efficiency 0.2282, and energy efficiency 0.0176.

The tiny yields in batches 2 and 4, 0.0105 and 0.0016, occurred with zero reported conversion and absent target-proxy signal. They are comparable to the 0.010 yield uncertainty and should be treated as low-end assay variation, not clear target formation.

These observations changed my initial expectation that response might increase with absolute overpotential. Instead, +1 V occupied a useful window, −1 V accessed a less efficient branch, and ±2 V were outside the useful short-time window. The result is polarity-specific: it cannot be described adequately by |V| alone.

The longer experiments confirmed that negative polarity was not completely inactive. Batch 5 (+1 V, 3000 s) gave conversion 0.0610, selectivity 0.8356, and yield 0.0562, whereas batch 6 (−1 V, 3000 s) gave conversion 0.0304, selectivity 0.5345, and yield 0.0253. Batch 6 also retained much poorer faradaic, transport, and energy efficiencies: 0.3871, 0.3624, and 0.2182 versus 0.7520, 0.7415, and 0.6856 in batch 5. Thus both polarities can accumulate product over time, but they appear to represent different kinetic or interfacial branches.

One plausible chemical interpretation is that positive and negative polarization drive different charge-transfer pathways, only one of which efficiently forms the target. Another possibility is that both eventually form the target through a reversible or indirect intermediate, with substantially different parasitic-current fractions. Species identities and electron stoichiometry were not observable, so these alternatives cannot be distinguished.

The ±2 V experiments lasted only 300 s. I therefore infer short-time collapse at those settings, not permanent inactivity at every duration.

## 4. Duration and accumulated productive charge

At S0/E0, +1 V, and 100 mA, increasing time from 300 s in batch 1 to 3000 s in batch 5 raised conversion from 0.0139 to 0.0610. The average apparent conversion rate changed from about 4.6×10⁻⁵ s⁻¹ to 2.0×10⁻⁵ s⁻¹. That less-than-tenfold conversion gain for a tenfold time increase could indicate declining current, transport limitation, surface blockage, precipitation, or simply distortion of the 300 s comparison by low-end assay uncertainty.

The cleaner S1/E1 comparison was closer to proportional. Batch 9 at 3000 s gave conversion 0.0687 and yield 0.0841. Batch 12 at 12000 s gave conversion 0.2658 and yield 0.2786. A fourfold duration produced approximately 3.9-fold conversion and 3.3-fold yield while selectivity remained high, changing only from 0.9388 to 0.9307. Faradaic efficiency declined modestly from 0.8991 to 0.8736, transport efficiency from 0.9199 to 0.8948, and energy efficiency from 0.9449 to 0.9049.

Thus, within 3000–12000 s for S1/E1, accumulated productive charge is the leading predictor of conversion, with only moderate efficiency loss. Depletion or severe overelectrolysis had not yet dominated by 12000 s, although extrapolation much further is unsupported.

The reported batch-12 yield slightly exceeded its conversion, and batch 9 showed a similar discrepancy. Therefore the processed yield and conversion channels should not be forced into an exact identity Y = X×S. They are independently calibrated noisy observables, or their benchmark definitions use different normalizations. Their differences are small enough to be compatible with combined measurement uncertainty. Mechanistically, I retain only the approximate expectation that yield should rise with both conversion and selectivity.

## 5. Current-cap coupling and parasitic current

Batches 5, 7, and 8 isolated the current-cap effect at S0/E0, +1 V, and 3000 s:

- Batch 7, 10 mA: conversion 0.0172, yield 0.0130, faradaic efficiency 0.8861, transport efficiency 0.8895, ohmic efficiency 1.000, and energy efficiency 0.8255.
- Batch 5, 100 mA: conversion 0.0610, yield 0.0562, faradaic efficiency 0.7520, transport efficiency 0.7415, ohmic efficiency 0.9732, and energy efficiency 0.6856.
- Batch 8, 500 mA: conversion 0.0526, yield 0.0269, faradaic efficiency 0.1562, transport efficiency 0.1498, ohmic efficiency 0.8924, and energy efficiency 0.1381.

At 10 mA, the cap constrained the rate but preserved efficient use of charge. Raising it to 100 mA increased productive conversion substantially at an acceptable efficiency cost. Raising it further to 500 mA did not improve conversion beyond uncertainty and sharply reduced every current-sensitive efficiency channel. This is strong evidence for a transport or interfacial ceiling: above it, added available current is largely diverted into parasitic processes or incurs polarization/ohmic loss.

A compact empirical form could be:

I_productive ≈ I_cap/[1 + I_cap/I_sat,m] × FE₀,m × exp[−(I_cap/I_side,m)^p]

where the first factor saturates productive flux and the exponential represents increasing parasitic loss. The data identify the qualitative ordering 10 mA < useful throughput near 100 mA << inefficient overdrive at 500 mA, but they do not uniquely identify I_sat, I_side, or p.

The term “parasitic process” is intentionally broad. It could mean side-product formation, solvent/electrolyte charging, capacitive current, local concentration polarization, or another benchmark loss channel. No direct side-product measurement was exposed.

## 6. Material, transport, acid, and precipitation coupling

Batches 5 and 9–11 compared matched pairs at +1 V, 100 mA, and 3000 s:

- Batch 5, S0/E0: conversion 0.0610, selectivity 0.8356, yield 0.0562, FE 0.7520, transport 0.7415, ohmic 0.9732, energy 0.6856, pH-normalized 0.2326, precipitation 0.9872.
- Batch 9, S1/E1: conversion 0.0687, selectivity 0.9388, yield 0.0841, FE 0.8991, transport 0.9199, ohmic 0.9933, energy 0.9449, pH-normalized 0.2107, precipitation 0.6674.
- Batch 10, S2/E2: conversion 0.0741, selectivity 0.8088, yield 0.0439, FE 0.7644, transport 0.7657, ohmic 0.9270, energy 0.7553, pH-normalized 0.1718, precipitation 0.
- Batch 11, S3/E3: conversion 0.0545, selectivity 0.7130, yield 0.0312, FE 0.5301, transport 0.5373, ohmic 0.9783, energy 0.6621, pH-normalized 0.2838, precipitation 0.0052.

S1/E1 was best because it combined high selectivity with high faradaic, transport, ohmic, and energy efficiencies. S2/E2 achieved slightly higher conversion and eliminated precipitation, but its lower selectivity and efficiency produced less target yield. S3/E3 also suppressed precipitation but had weaker selectivity and charge utilization. S0/E0 had severe precipitation despite good ohmic efficiency.

This changed my initial property-based explanation. Nominal bulk conductivity alone does not rank performance: S0/E0 had the most favorable simple conductivity product but was not best. Nominal diffusivity alone also fails: S1/E1 and S3/E3 have similarly favorable rough diffusivity products, yet their transport efficiencies were 0.9199 and 0.5373. The declared hidden solvent/electrolyte residuals and interfacial couplings must therefore be important.

The precipitation observations broadly agree with the nominal formulation dossier: E0 contains the highest precipitating-salt concentration and a low solubility product, while the other paired formulations have more favorable effective solubility. However, precipitation is not the sole performance controller. Eliminating its signal in S2/E2 and S3/E3 did not make either outperform S1/E1. I interpret precipitation as a parallel material-dependent process that may block area, alter transport, or sequester accessible product, but whose effect competes with intrinsic interfacial selectivity and faradaic efficiency.

The pH-normalized signal was mainly material-specific and changed little with duration: S1/E1 measured 0.2107 in batch 9 and 0.2099 in batch 12. This suggests that, over the observed interval, the acid/electrolyte state acts mostly as a stable boundary condition rather than a strongly drifting reaction coordinate. Because this is a normalized channel rather than a reported physical pH, I do not assign a hydrogen-ion concentration or proton stoichiometry.

The nominal standard-potential shifts also do not provide a complete effective-overpotential correction. The paired nominal shifts are approximately −0.20 V for S0/E0, +0.30 V for S1/E1, +0.38 V for S2/E2, and +0.10 V for S3/E3. Their observed ranking at the same applied +1 V is not explained by that sequence alone. Kinetic, solvation, and interfacial residuals must accompany any potential-shift model.

## 7. Efficiency relationships

I regard faradaic, transport, ohmic, and energy efficiency as related diagnostics rather than independent causes:

- Faradaic efficiency estimates the fraction of electrochemical throughput associated with productive chemistry.
- Transport efficiency represents access of reactant or charge carriers to the productive interface.
- Ohmic efficiency reflects resistive loss and was generally high except under the 500 mA overdrive and the low-conductivity S2/E2 condition.
- Energy efficiency combines potential utilization and charge losses but is not numerically equal to the simple product of the other reported channels.

A mechanistic accounting might use

η_energy = F(η_F, η_transport, η_ohmic, overpotential utilization, material residuals),

but the observations do not support imposing η_energy = η_Fη_transportη_ohmic exactly. For example, batch 9 had energy efficiency 0.9449, exceeding that simple product. These are separately calibrated benchmark channels.

The coherent simultaneous collapse of faradaic, transport, and energy efficiencies at +2 V and 500 mA is nevertheless informative: it indicates a shared unfavorable state, such as excessive polarization or current demand beyond mass-transfer capacity.

## 8. Safety and cost

All observed risks were far below the 0.65 safety limit. Risk depended more on material choice than on duration in the tested set: approximately 0.0722 for S0/E0, 0.0956 for S1/E1, 0.1136 for S2/E2, and 0.1262 for S3/E3. Batch 12 retained the same 0.0956 risk as batch 9 despite fourfold longer electrolysis, so the reported risk was not accumulating directly with electrolysis time under those conditions.

Physical costs were similar and small compared with the scientific performance differences: batch 12 cost about 0.3034 versus 0.2998 for batch 9. I therefore selected batch 12 on observed performance, not because of a materially lower cost.

## 9. What is identified, and what is not

Reasonably supported within the tested domain:

1. The productive response has a polarity-specific potential window, with +1 V favorable for the sampled pairs and S0/E0.
2. Product formation accumulates with time; S1/E1 remains productive through 12000 s.
3. Current cap creates a throughput–efficiency tradeoff, with 100 mA superior to both 10 and 500 mA for balanced performance under the tested baseline.
4. Material choice strongly affects selectivity, transport, faradaic loss, precipitation, pH-normalized state, and risk.
5. Precipitation is neither necessary nor sufficient to explain poor performance.

Unidentifiable or weakly identified factors:

- Solvent and electrolyte effects are confounded because only matched pairs S0/E0, S1/E1, S2/E2, and S3/E3 were compared. No crossed combinations were tested.
- Actual current-time traces, passed charge, electrode area, gap, and base resistance were unavailable. The 100 mA value is a cap, not a measured constant current.
- There were no replicate batches, so fixed condition effects cannot be cleanly separated from assay noise at the low end.
- Only one reagent concentration and nominal liquid volume were used; concentration order, dilution effects, and volume scaling are unknown.
- Chemical identities, electron stoichiometry, intermediates, side products, and whether precipitation contains target material are hidden.
- Potential was sparsely sampled. The optimum within the positive window could lie below, near, or somewhat above +1 V; +2 V only establishes an unfavorable endpoint at 300 s.
- The long-duration behavior was tested only for S1/E1. Eventual depletion, passivation, degradation, or overelectrolysis beyond 12000 s remains unknown.
- UV–visible measurements supplied efficiency proxies but not a fully identified concentration-time trace.

## 10. Plausible alternative explanations

Several alternatives remain consistent with the observations:

- The apparent material trends could be dominated by fixed hidden interfacial residuals rather than the nominal conductivity, diffusivity, acidity, or solubility properties.
- Precipitation signal may be a correlated spectator rather than a causal limiter. Its association with S0/E0 does not prove that suppressing it would improve yield.
- The 500 mA efficiency collapse could arise from a simulated current-control mismatch, capacitive charging, or ohmic polarization rather than formation of a chemical side product.
- The negative-potential branch could represent a different route to the same target, reversible conversion through an intermediate, or partially overlapping assay response.
- The apparently sublinear S0/E0 time dependence may be caused mainly by noise in batch 1, whereas the S1/E1 data are consistent with nearly linear conversion versus time between 3000 and 12000 s.
- Because yield, conversion, and selectivity are independently processed channels, their small algebraic inconsistencies need not imply unusual chemistry.

## 11. Predictive conclusions

Within the observed domain, I would predict that S1/E1 near +1 V and a moderate current cap will outperform the other tested paired formulations for target yield and balanced efficiency. Increasing duration from 3000 s should continue to increase conversion substantially up to at least 12000 s while preserving selectivity near 0.93, as observed, but extrapolation beyond that interval should include depletion or passivation uncertainty.

At the same material and duration, lowering the cap substantially below 100 mA should preserve efficiency but reduce conversion, while raising it toward 500 mA should yield little additional conversion and much poorer faradaic, transport, and energy efficiency. Moving the potential toward ±2 V should be treated as high risk for loss of productive electrochemical performance, even though physical safety risk remained low in the short tests.

This account is a phenomenological mechanism, not a molecular identification. Its central claim is that target formation is governed by accumulated productive charge inside a material-dependent, polarity-specific potential window, with current/transport saturation and parasitic loss at overdrive, plus a coupled but non-determinative precipitation process.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific prior mechanism or expected optimum was supplied. The supplied information consisted of nominal material properties and general instrument/scoring contracts, including the warning that hidden, fixed material residuals and solvent coupling could matter.

Supported self-developed claims:
- A polarity-specific, bounded potential window was supported. At S0/E0 and 300 s, +1 V in batch 1 retained selectivity 0.839 and substantial faradaic/transport efficiencies, whereas +2 V in batch 3 collapsed conversion, selectivity, faradaic efficiency, and transport efficiency to zero. The −1 V branch was weaker than +1 V at both 300 s (batches 2 versus 1) and 3000 s (batches 6 versus 5). This changed my judgment from a possible monotonic dependence on absolute overpotential to a sign-dependent window.
- Product formation depended on duration or accumulated productive charge. Extending S0/E0 at +1 V from 300 to 3000 s raised conversion from 0.014 to 0.061 (batches 1 and 5). More decisively, extending S1/E1 from 3000 to 12000 s raised conversion from 0.069 to 0.266 and yield from 0.084 to 0.279 while maintaining selectivity near 0.93 (batches 9 and 12).
- A current-cap throughput–efficiency tradeoff was supported. At +1 V for 3000 s, 10 mA gave low conversion but high efficiencies (batch 7); 100 mA increased yield while retaining useful efficiencies (batch 5); 500 mA failed to improve conversion and sharply reduced faradaic, transport, ohmic, and energy efficiencies (batch 8).
- Material behavior required coupled interfacial and transport factors. Under matched conditions, S1/E1 in batch 9 outperformed S0/E0, S2/E2, and S3/E3 in batches 5, 10, and 11 through its combination of selectivity and efficiency.

Contradicted or narrowed claims:
- A simple “larger |V| gives more conversion” law was contradicted by batches 1–4, especially the collapse at +2 V in batch 3.
- A simple conductivity ranking was contradicted. Nominally conductive S0/E0 was not best; S1/E1 performed better in batch 9 than S0/E0 in batch 5.
- A precipitation-only explanation was contradicted as a sufficient account. Batches 10 and 11 nearly eliminated precipitation but did not outperform the moderately precipitating S1/E1 condition in batch 9.
- A universal strongly saturating duration law was narrowed. The S0/E0 comparison in batches 1 and 5 appeared sublinear, but S1/E1 conversion was nearly proportional to duration between batches 9 and 12. Low-end assay uncertainty may partly explain the apparent S0/E0 curvature.
- Exact identities such as yield = conversion × selectivity were contradicted as descriptions of the processed assay channels: batches 9 and 12 reported yield slightly above conversion. The channels should be treated as independently noisy or differently normalized.

Untested claims include molecular identities, electron stoichiometry, the nature of parasitic current, whether precipitate contains target, behavior beyond 12000 s, concentration scaling, crossed solvent/electrolyte laws, and the precise location of the positive-potential optimum. Because ±2 V was tested only for 300 s, permanent inactivity at those potentials was not established.

2. One additional discriminating experiment

I would run S0/E0 at +1 V with a 10 mA cap for 30000 s, using the same 0.020 mol reagent and 0.040 L solvent as batches 5 and 7. This gives the same nominal cap×time as the 100 mA, 3000 s condition in batch 5 and ten times the duration of the 10 mA condition in batch 7.

My leading explanation is that moderate current increases throughput, whereas high current encounters transport saturation and parasitic loss; sufficiently long low-current operation should therefore accumulate substantial product while preserving relatively high efficiency. The main alternative is that productive chemistry requires a current-density-dependent interfacial state or suffers time-dependent passivation, so nominal charge equivalence would not produce comparable conversion.

Interpretation of outcomes:
- If the long 10 mA run approached or exceeded batch 5 yield while retaining efficiencies near batch 7, I would strengthen the accumulated-productive-charge model and conclude that 100 mA mainly accelerates the process.
- If yield remained near batch 7 despite tenfold longer duration, I would favor a current-threshold, passivation, or actual-current-decay explanation over simple charge accumulation.
- If yield increased but efficiencies or selectivity collapsed late in the run, I would add time-dependent degradation or product overelectrolysis to the mechanism.
- If conversion matched batch 5 but yield did not, I would infer that current density affects selectivity independently of total conversion.

This experiment would still be imperfect because the cap is not a measured current trace. Direct coulometry would be preferable if available.

3. Unused evidence, reliability, and goal effects

Evidence not fully used included the raw spectral arrays and complete characterization artifacts; I relied mainly on processed estimates and supplied peak assignments. Intermediate UV–visible measurements were collected but not modeled systematically against final assays. I also did not quantitatively exploit double-layer capacitance, acid concentration/pKa, individual peak areas, cost, or the essentially zero mass-balance summaries. No dedicated pH-meter measurements, replicates, crossed material controls, or current-time traces were obtained.

The least reliable sealed predictions are Q05–Q10 because they use solvent/electrolyte combinations never tested during the campaign; hidden coupling prevents cleanly transferring paired-material effects. Q11 is also weak because it combines negative polarity, high current, long duration, and a potential not directly tested together. Q01 and Q02 have especially uncertain scores because predicted yields lie near the 0.02 multiplicative score gate, so small assay fluctuations can cause large score changes. Predictions for Q03 and Q04 are comparatively better anchored by batches 1, 2, 5, and 6, although 7200 s remains an extrapolation.

Batch 12 is a reliable recommendation among the conditions actually tested because it had the highest observed yield and score with high efficiencies and low safety risk. It is not a reliable claim of global optimality: it was unreplicated, sat at the longest tested duration, and the campaign did not refine potential around +1 V or test crossed materials.

The assigned explanatory and predictive goal materially shaped evidence collection. I deliberately spent batches on both polarities, ±2 V failures, current-cap extremes, duration contrasts, and multiple materials rather than repeatedly optimizing the public score. This broadened mechanistic coverage but left fewer batches for replication and local optimization around S1/E1. The secondary recommendation requirement created an exploration–exploitation tradeoff, but there was no clear conflict with safety: all tested batches remained well below the stated risk limit.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.56,
        "lower80": 0.48,
        "upper80": 0.64
      },
      "energy_efficiency": {
        "estimate": 0.29,
        "lower80": 0.18,
        "upper80": 0.4
      },
      "faradaic_efficiency": {
        "estimate": 0.43,
        "lower80": 0.34,
        "upper80": 0.52
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.1365,
        "lower80": 0.0,
        "upper80": 0.3
      },
      "selective_product_yield": {
        "estimate": 0.009,
        "lower80": 0.0,
        "upper80": 0.025
      },
      "transport_efficiency": {
        "estimate": 0.42,
        "lower80": 0.31,
        "upper80": 0.53
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.84,
        "lower80": 0.78,
        "upper80": 0.9
      },
      "energy_efficiency": {
        "estimate": 0.75,
        "lower80": 0.62,
        "upper80": 0.85
      },
      "faradaic_efficiency": {
        "estimate": 0.79,
        "lower80": 0.68,
        "upper80": 0.88
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.4235,
        "lower80": 0.1,
        "upper80": 0.55
      },
      "selective_product_yield": {
        "estimate": 0.017,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "transport_efficiency": {
        "estimate": 0.79,
        "lower80": 0.67,
        "upper80": 0.89
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.56,
        "lower80": 0.49,
        "upper80": 0.63
      },
      "energy_efficiency": {
        "estimate": 0.27,
        "lower80": 0.16,
        "upper80": 0.37
      },
      "faradaic_efficiency": {
        "estimate": 0.41,
        "lower80": 0.32,
        "upper80": 0.5
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.3134,
        "lower80": 0.23,
        "upper80": 0.4
      },
      "selective_product_yield": {
        "estimate": 0.052,
        "lower80": 0.025,
        "upper80": 0.095
      },
      "transport_efficiency": {
        "estimate": 0.4,
        "lower80": 0.29,
        "upper80": 0.5
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.85,
        "lower80": 0.8,
        "upper80": 0.89
      },
      "energy_efficiency": {
        "estimate": 0.72,
        "lower80": 0.59,
        "upper80": 0.8
      },
      "faradaic_efficiency": {
        "estimate": 0.76,
        "lower80": 0.65,
        "upper80": 0.83
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.5263,
        "lower80": 0.46,
        "upper80": 0.6
      },
      "selective_product_yield": {
        "estimate": 0.11,
        "lower80": 0.07,
        "upper80": 0.16
      },
      "transport_efficiency": {
        "estimate": 0.76,
        "lower80": 0.63,
        "upper80": 0.84
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.66,
        "lower80": 0.52,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.38,
        "lower80": 0.2,
        "upper80": 0.58
      },
      "faradaic_efficiency": {
        "estimate": 0.48,
        "lower80": 0.3,
        "upper80": 0.66
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.368,
        "lower80": 0.24,
        "upper80": 0.49
      },
      "selective_product_yield": {
        "estimate": 0.06,
        "lower80": 0.02,
        "upper80": 0.12
      },
      "transport_efficiency": {
        "estimate": 0.5,
        "lower80": 0.3,
        "upper80": 0.7
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.92,
        "lower80": 0.82,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.87,
        "lower80": 0.68,
        "upper80": 0.99
      },
      "faradaic_efficiency": {
        "estimate": 0.88,
        "lower80": 0.7,
        "upper80": 0.97
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.6049,
        "lower80": 0.49,
        "upper80": 0.7
      },
      "selective_product_yield": {
        "estimate": 0.16,
        "lower80": 0.08,
        "upper80": 0.27
      },
      "transport_efficiency": {
        "estimate": 0.86,
        "lower80": 0.65,
        "upper80": 0.98
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.48,
        "lower80": 0.35,
        "upper80": 0.65
      },
      "energy_efficiency": {
        "estimate": 0.18,
        "lower80": 0.05,
        "upper80": 0.36
      },
      "faradaic_efficiency": {
        "estimate": 0.3,
        "lower80": 0.15,
        "upper80": 0.48
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.2626,
        "lower80": 0.14,
        "upper80": 0.39
      },
      "selective_product_yield": {
        "estimate": 0.04,
        "lower80": 0.01,
        "upper80": 0.09
      },
      "transport_efficiency": {
        "estimate": 0.32,
        "lower80": 0.16,
        "upper80": 0.5
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.78,
        "lower80": 0.63,
        "upper80": 0.89
      },
      "energy_efficiency": {
        "estimate": 0.7,
        "lower80": 0.48,
        "upper80": 0.87
      },
      "faradaic_efficiency": {
        "estimate": 0.66,
        "lower80": 0.45,
        "upper80": 0.82
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.4856,
        "lower80": 0.37,
        "upper80": 0.6
      },
      "selective_product_yield": {
        "estimate": 0.09,
        "lower80": 0.035,
        "upper80": 0.17
      },
      "transport_efficiency": {
        "estimate": 0.67,
        "lower80": 0.43,
        "upper80": 0.84
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.52,
        "lower80": 0.38,
        "upper80": 0.66
      },
      "energy_efficiency": {
        "estimate": 0.2,
        "lower80": 0.05,
        "upper80": 0.38
      },
      "faradaic_efficiency": {
        "estimate": 0.32,
        "lower80": 0.16,
        "upper80": 0.49
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.2726,
        "lower80": 0.14,
        "upper80": 0.4
      },
      "selective_product_yield": {
        "estimate": 0.04,
        "lower80": 0.008,
        "upper80": 0.09
      },
      "transport_efficiency": {
        "estimate": 0.33,
        "lower80": 0.15,
        "upper80": 0.52
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.82,
        "lower80": 0.68,
        "upper80": 0.9
      },
      "energy_efficiency": {
        "estimate": 0.66,
        "lower80": 0.44,
        "upper80": 0.84
      },
      "faradaic_efficiency": {
        "estimate": 0.68,
        "lower80": 0.48,
        "upper80": 0.83
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.4878,
        "lower80": 0.38,
        "upper80": 0.59
      },
      "selective_product_yield": {
        "estimate": 0.1,
        "lower80": 0.04,
        "upper80": 0.18
      },
      "transport_efficiency": {
        "estimate": 0.66,
        "lower80": 0.43,
        "upper80": 0.82
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.52,
        "lower80": 0.42,
        "upper80": 0.62
      },
      "energy_efficiency": {
        "estimate": 0.04,
        "lower80": 0.0,
        "upper80": 0.14
      },
      "faradaic_efficiency": {
        "estimate": 0.09,
        "lower80": 0.02,
        "upper80": 0.2
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.1904,
        "lower80": 0.06,
        "upper80": 0.29
      },
      "selective_product_yield": {
        "estimate": 0.032,
        "lower80": 0.005,
        "upper80": 0.07
      },
      "transport_efficiency": {
        "estimate": 0.08,
        "lower80": 0.01,
        "upper80": 0.2
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.82,
        "lower80": 0.76,
        "upper80": 0.88
      },
      "energy_efficiency": {
        "estimate": 0.12,
        "lower80": 0.04,
        "upper80": 0.22
      },
      "faradaic_efficiency": {
        "estimate": 0.14,
        "lower80": 0.07,
        "upper80": 0.25
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.2727,
        "lower80": 0.2,
        "upper80": 0.36
      },
      "selective_product_yield": {
        "estimate": 0.065,
        "lower80": 0.025,
        "upper80": 0.12
      },
      "transport_efficiency": {
        "estimate": 0.13,
        "lower80": 0.05,
        "upper80": 0.24
      }
    }
  ],
  "rationale": "Predictions interpolate the S0/E0 polarity, duration, and current-cap contrasts from batches 1–8 and extrapolate the approximately charge-dependent long-time behavior seen in batches 9 and 12. Crossed solvent/electrolyte combinations were not tested, so Q05–Q10 receive wider intervals based on nominal conductivity, diffusivity, potential-shift, and precipitation trends. The 500 mA cases reflect the strong parasitic-current and transport-efficiency collapse observed in batch 8. Scores apply the published weighted metric formula and selective-yield gate; intervals include assay noise, duration extrapolation, and substantial material-coupling uncertainty."
}
```
