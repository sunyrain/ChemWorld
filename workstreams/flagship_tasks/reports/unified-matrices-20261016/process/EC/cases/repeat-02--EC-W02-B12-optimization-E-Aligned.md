# repeat-02/EC-W02-B12-optimization-E-Aligned

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-02\EC-W02-B12-optimization-E-Aligned\participant\optimization-E-Aligned

## 同期笔记

### v1 · 公开事件 0

# Electrochemical campaign hypotheses

## H1 [tentative]
At fixed loading, balanced score should show an interior optimum in potential magnitude and electrolysis duration: insufficient charge limits conversion, while excessive driving force/time lowers selectivity and energy efficiency. This will be tested with broad contrasts and then local refinement.

## H2 [tentative]
High conductivity alone will not ensure the best balanced score. Electrolyte/solvent combinations should trade transport and ohmic efficiency against pH, precipitation, and interfacial selectivity. Nominally E0/S0 favors conductivity, E2 favors thinner diffusion layers but lower conductivity, and S2/S3 may suppress proton activity and precipitation. Material rankings remain unresolved because hidden fixed residuals are declared.

## Design decision
Use comparable reagent loading and volume initially; allocate one intermediate UV-vis measurement per batch when feasible, then final assays. Early batches screen potential sign, material profiles, current cap, and charge; later batches refine and replicate the best region. A numerical score difference will guide optimization but will not alone establish a repeatable effect without confirmation.

### v2 · 公开事件 84

# Electrochemical campaign hypotheses

## H1 [supported in tested negative-potential scope; optimum unresolved]
Positive potential was ineffective at +1.2 V (assay event runner-operation-0007), whereas reversing to -1.2 V produced a nonzero score (runner-operation-0014); polarity is therefore consequential under S0/E0 and the tested loading. With S1/E1, 500 mA cap, and 14,400 s, making potential less negative improved the public score across -1.6, -1.2, -0.9, and -0.6 V (runner-operation-0063, -0056, -0070, -0077). The -0.4 V batch gave the largest observed score, 0.54748, at event runner-operation-0084, but it differs from -0.6 V by only about 0.0024, far smaller than several channel uncertainties; the location of a true optimum and repeatability remain unresolved. A future test should bracket -0.4 V with replication and less-negative potentials.

## H2 [partly supported, limited by paired-factor confounding]
At -1.2 V, 500 mA cap, and 3,600 s, paired S1/E1 outscored paired S0/E0, S2/E2, and S3/E3 (assays runner-operation-0028, -0021, -0035, -0042). This supports using S1/E1 in the observed scope, but solvent and electrolyte effects were changed together and therefore cannot be attributed separately. S2/E2 suppressed precipitation relative to S1/E1 yet did not improve balanced score, consistent with the predicted transport/ohmic/selectivity tradeoff rather than conductivity or precipitation alone controlling performance.

## H3 [supported in tested duration range]
For S1/E1 at -1.2 V and 500 mA cap, extending electrolysis from 3,600 to 7,200 to 14,400 s raised score and selective-product yield (runner-operation-0028, -0049, -0056). No downturn was observed by the legal maximum duration, so the hypothesized long-time degradation optimum was not reached in this range.

## Recommendation decision
Select batch 12: 0.020 mol reagent in 0.040 L S1; E1; -0.4 V; 500 mA magnitude cap; 14,400 s. It has the highest observed score and yield (runner-operation-0084). This is an operating recommendation, not evidence that it is statistically superior to batch 11; confirmation would require replicates.

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
      "potential_V": 1.2
    },
    {
      "duration_s": 600,
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
    "cost": 0.28287473320961,
    "electrochemical_conversion": 0.008014115504920483,
    "electrochemical_selectivity": 0.01034972071647644,
    "energy_efficiency": 0.005256945732980967,
    "faradaic_efficiency": 0.02452157624065876,
    "ohmic_efficiency": 0.9705422520637512,
    "pH_normalized": 0.22897005081176758,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.0
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
      "potential_V": -1.2
    },
    {
      "duration_s": 600,
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
    "cost": 0.2828879952430725,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.5507639646530151,
    "energy_efficiency": 0.17965897917747498,
    "faradaic_efficiency": 0.35250434279441833,
    "ohmic_efficiency": 0.9783982634544373,
    "pH_normalized": 0.22627469897270203,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.1622038185596466,
    "selective_product_yield": 0.011944524012506008,
    "transport_efficiency": 0.3787611722946167
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
      "current_mA": 500,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.2
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
    "cost": 0.29124000668525696,
    "electrochemical_conversion": 0.10301900655031204,
    "electrochemical_selectivity": 0.5400475859642029,
    "energy_efficiency": 0.12408152967691422,
    "faradaic_efficiency": 0.20512989163398743,
    "ohmic_efficiency": 0.8799730539321899,
    "pH_normalized": 0.22698970139026642,
    "precipitation_signal": 0.9871450662612915,
    "safety_risk": 0.072194404900074,
    "score": 0.24187545478343964,
    "selective_product_yield": 0.04924027994275093,
    "transport_efficiency": 0.22168679535388947
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
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -1.2
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
    "cost": 0.30724000930786133,
    "electrochemical_conversion": 0.14859555661678314,
    "electrochemical_selectivity": 0.5431817173957825,
    "energy_efficiency": 0.18231596052646637,
    "faradaic_efficiency": 0.3549685478210449,
    "ohmic_efficiency": 0.8135601878166199,
    "pH_normalized": 0.20621326565742493,
    "precipitation_signal": 0.69908207654953,
    "safety_risk": 0.09559440612792969,
    "score": 0.29009220004081726,
    "selective_product_yield": 0.08792947977781296,
    "transport_efficiency": 0.3234809935092926
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
      "solvent": 2,
      "volume_L": 0.04
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -1.2
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
    "cost": 0.3328399956226349,
    "electrochemical_conversion": 0.143845334649086,
    "electrochemical_selectivity": 0.5619614720344543,
    "energy_efficiency": 0.20764265954494476,
    "faradaic_efficiency": 0.3120505213737488,
    "ohmic_efficiency": 0.6260665655136108,
    "pH_normalized": 0.1786634773015976,
    "precipitation_signal": 0.0,
    "safety_risk": 0.1135944053530693,
    "score": 0.2734483778476715,
    "selective_product_yield": 0.08645913749933243,
    "transport_efficiency": 0.3015410602092743
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
      "solvent": 3,
      "volume_L": 0.04
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": -1.2
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
    "cost": 0.3168399930000305,
    "electrochemical_conversion": 0.0564260371029377,
    "electrochemical_selectivity": 0.5244921445846558,
    "energy_efficiency": 0.09224679321050644,
    "faradaic_efficiency": 0.14042767882347107,
    "ohmic_efficiency": 0.8967416882514954,
    "pH_normalized": 0.2811680734157562,
    "precipitation_signal": 0.0023995577357709408,
    "safety_risk": 0.12619440257549286,
    "score": 0.20989063382148743,
    "selective_product_yield": 0.038573648780584335,
    "transport_efficiency": 0.11574433743953705
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
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -1.2
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
    "cost": 0.3158800005912781,
    "electrochemical_conversion": 0.31511157751083374,
    "electrochemical_selectivity": 0.5696935653686523,
    "energy_efficiency": 0.2217300832271576,
    "faradaic_efficiency": 0.32887643575668335,
    "ohmic_efficiency": 0.8464126586914062,
    "pH_normalized": 0.20691271126270294,
    "precipitation_signal": 0.6940808892250061,
    "safety_risk": 0.09559440612792969,
    "score": 0.34510207176208496,
    "selective_product_yield": 0.18157166242599487,
    "transport_efficiency": 0.3322767913341522
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
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -1.2
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
    "cost": 0.33316001296043396,
    "electrochemical_conversion": 0.6045060753822327,
    "electrochemical_selectivity": 0.5663701295852661,
    "energy_efficiency": 0.21710264682769775,
    "faradaic_efficiency": 0.33477047085762024,
    "ohmic_efficiency": 0.8317086696624756,
    "pH_normalized": 0.2052152305841446,
    "precipitation_signal": 0.706953763961792,
    "safety_risk": 0.09559440612792969,
    "score": 0.4158281087875366,
    "selective_product_yield": 0.32773303985595703,
    "transport_efficiency": 0.3282751142978668
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
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -1.6
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
    "cost": 0.3446800112724304,
    "electrochemical_conversion": 0.5072095990180969,
    "electrochemical_selectivity": 0.5134835243225098,
    "energy_efficiency": 0.15838350355625153,
    "faradaic_efficiency": 0.2642449736595154,
    "ohmic_efficiency": 0.8909170031547546,
    "pH_normalized": 0.20722901821136475,
    "precipitation_signal": 0.7148279547691345,
    "safety_risk": 0.09559440612792969,
    "score": 0.36798402667045593,
    "selective_product_yield": 0.283308744430542,
    "transport_efficiency": 0.28507623076438904
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
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -0.9
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
    "cost": 0.3245199918746948,
    "electrochemical_conversion": 0.7129843235015869,
    "electrochemical_selectivity": 0.630828320980072,
    "energy_efficiency": 0.3765515387058258,
    "faradaic_efficiency": 0.3829699456691742,
    "ohmic_efficiency": 0.7424106001853943,
    "pH_normalized": 0.2049148678779602,
    "precipitation_signal": 0.7039898037910461,
    "safety_risk": 0.09559440612792969,
    "score": 0.4934942126274109,
    "selective_product_yield": 0.42435869574546814,
    "transport_efficiency": 0.384319543838501
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
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -0.6
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
    "cost": 0.3158800005912781,
    "electrochemical_conversion": 0.8118973970413208,
    "electrochemical_selectivity": 0.6459125876426697,
    "energy_efficiency": 0.42521801590919495,
    "faradaic_efficiency": 0.43019482493400574,
    "ohmic_efficiency": 0.6325092315673828,
    "pH_normalized": 0.2058999091386795,
    "precipitation_signal": 0.7118789553642273,
    "safety_risk": 0.09559440612792969,
    "score": 0.5450782775878906,
    "selective_product_yield": 0.5241912007331848,
    "transport_efficiency": 0.4373747706413269
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
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -0.4
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
    "cost": 0.31011998653411865,
    "electrochemical_conversion": 0.8572301864624023,
    "electrochemical_selectivity": 0.6673166751861572,
    "energy_efficiency": 0.29597365856170654,
    "faradaic_efficiency": 0.4341837167739868,
    "ohmic_efficiency": 0.46078822016716003,
    "pH_normalized": 0.20642022788524628,
    "precipitation_signal": 0.7052149176597595,
    "safety_risk": 0.09559440612792969,
    "score": 0.5474780201911926,
    "selective_product_yield": 0.6091849207878113,
    "transport_efficiency": 0.45540866255760193
  }
}
```

## K1 封存报告

Mechanistic report

1. Scope and empirical basis

I interpret this as a cathodic electrochemical conversion in which the desired product competes with unproductive electron transfer, electrolyte/solvent-dependent transport losses, proton-related chemistry, and precipitation. This is a model of the synthetic benchmark world, not a claim about any particular real chemical identity. All batches used 0.020 mol limiting reagent and 0.040 L solvent, so the campaign identifies behavior only at that loading and volume. Electrode geometry, gap, and base contact resistance were fixed across the campaign but unknown.

The principal batch results were:
• Batch 1: S0/E0, +1.2 V, 100 mA cap, 600 s. Score 0; conversion 0.0080, selectivity 0.0103, selective-product yield 0, and precipitation signal 1.0.
• Batch 2: S0/E0, −1.2 V, 100 mA cap, 600 s. Score 0.1622; selectivity 0.5508, yield 0.0119, faradaic efficiency 0.3525, transport efficiency 0.3788, and ohmic efficiency 0.9784. The reported conversion was clipped/noisy at 0 despite the small nonzero yield.
• Batch 3: S0/E0, −1.2 V, 500 mA cap, 3,600 s. Score 0.2419; conversion 0.1030, selectivity 0.5400, yield 0.0492, and precipitation 0.9871.
• Batch 4: S1/E1, −1.2 V, 500 mA, 3,600 s. Score 0.2901; conversion 0.1486, selectivity 0.5432, yield 0.0879, energy efficiency 0.1823, faradaic efficiency 0.3550, transport efficiency 0.3235, ohmic efficiency 0.8136, and precipitation 0.6991.
• Batch 5: S2/E2 under the same electrical conditions as batch 4. Score 0.2734; conversion 0.1438, selectivity 0.5620, yield 0.0865, and precipitation 0.
• Batch 6: S3/E3 under the same electrical conditions. Score 0.2099; conversion 0.0564, selectivity 0.5245, yield 0.0386, and precipitation 0.0024.
• Batch 7: S1/E1, −1.2 V, 500 mA, 7,200 s. Score 0.3451; conversion 0.3151, selectivity 0.5697, and yield 0.1816.
• Batch 8: S1/E1, −1.2 V, 500 mA, 14,400 s. Score 0.4158; conversion 0.6045, selectivity 0.5664, yield 0.3277, energy efficiency 0.2171, faradaic efficiency 0.3348, transport efficiency 0.3283, and ohmic efficiency 0.8317.
• Batch 9: S1/E1, −1.6 V, 500 mA, 14,400 s. Score 0.3680; conversion 0.5072, selectivity 0.5135, yield 0.2833, energy efficiency 0.1584, and faradaic efficiency 0.2642.
• Batch 10: S1/E1, −0.9 V, 500 mA, 14,400 s. Score 0.4935; conversion 0.7130, selectivity 0.6308, yield 0.4244, energy efficiency 0.3766, and faradaic efficiency 0.3830.
• Batch 11: S1/E1, −0.6 V, 500 mA, 14,400 s. Score 0.5451; conversion 0.8119, selectivity 0.6459, yield 0.5242, energy efficiency 0.4252, faradaic efficiency 0.4302, transport efficiency 0.4374, and ohmic efficiency 0.6325.
• Batch 12: S1/E1, −0.4 V, 500 mA, 14,400 s. Score 0.5475; conversion 0.8572, selectivity 0.6673, yield 0.6092, energy efficiency 0.2960, faradaic efficiency 0.4342, transport efficiency 0.4554, and ohmic efficiency 0.4608.

2. Polarity and potential window

The clearest mechanistic conclusion is that productive conversion requires negative polarization in the explored convention. Reversing S0/E0 from +1.2 V in batch 1 to −1.2 V in batch 2 changed the assay from essentially inactive and nonselective to approximately 0.55 selectivity with measurable product. Because those batches otherwise used the same nominal current cap, duration, loading, and medium, polarity is the best-supported causal factor in the campaign.

Within S1/E1 at 500 mA and 14,400 s, progressively less negative potentials from −1.6 to −0.4 V improved conversion, selectivity, yield, faradaic efficiency, transport efficiency, and the total score. Thus, more cathodic driving force was not beneficial over that interval. I conjecture that excessively negative polarization diverts current into side reactions and/or drives an interfacial state unfavorable to target formation. This explains why batch 9 at −1.6 V was worse than batch 8 at −1.2 V, and why −0.9 and −0.6 V were substantially better.

The potential trends are not uniform across every efficiency component. Ohmic efficiency fell from 0.8909 at −1.6 V to 0.4608 at −0.4 V, while faradaic and transport efficiencies rose. Energy efficiency peaked at −0.6 V rather than −0.4 V. I therefore view the public score as a genuine compromise: −0.4 V generated more target product and higher conversion, but −0.6 V used electrical energy and the resistive part of the cell more favorably. The score difference between batches 11 and 12 was only about 0.0024, much smaller than the noise scale of several assay channels. Batch 12 is the highest observation, but the evidence does not establish that −0.4 V is reproducibly superior to −0.6 V or that the true optimum lies exactly there. A still less negative optimum is plausible because no potential between −0.4 and 0 V was tested.

3. Charge, current, and time

At −1.2 V in S1/E1, increasing duration from 3,600 to 7,200 to 14,400 s raised conversion from 0.1486 to 0.3151 to 0.6045 and yield from 0.0879 to 0.1816 to 0.3277. These values are approximately proportional to time over the observed range, with no clear saturation. Selectivity stayed near 0.54–0.57, suggesting that duration mainly accumulated conversion rather than radically changing the product branching ratio. No strong late-time degradation was visible by 14,400 s.

Batch 2 versus batch 3 also shows that a much larger nominal charge opportunity improves conversion and yield, but current and duration were changed together: 100 mA for 600 s versus 500 mA for 3,600 s. Consequently, this comparison cannot identify separate current and time effects. Furthermore, the configured current was a cap; actual current was not directly reported. It is possible that electrode kinetics or cell resistance prevented the system from reaching 500 mA, especially near −0.4 V.

A compact kinetic picture consistent with the observations is:

I_actual = min(I_cap, G_medium × |E_applied − E_effective|),
dr_R/dt = −r_target − r_side,
dr_P/dt = r_target − r_degradation,
r_target ≈ k_ET(E_effective, medium, pH) × C_R × f_transport,
r_side ≈ k_side(E_effective, proton activity, interfacial state) × C_R.

Here R and P denote reactant and target product, G_medium is an effective conductance, and f_transport depends on diffusion, diffusion-layer thickness, and evolving concentration. Conversion is approximately 1 − R/R0, instantaneous selectivity is r_target/(r_target+r_side), and isolated selective yield is related to P/R0. The reported conversion multiplied by selectivity is close to, but not exactly equal to, measured yield; this is expected from independent channel noise, possible time integration of changing selectivity, and the benchmark’s separate calibrated estimators.

4. Solvent/electrolyte coupling

The nominal dossier suggests several coupled roles:
• Conductivity controls resistive voltage loss and attainable current.
• Diffusivity and diffusion-layer thickness control reactant delivery and product removal.
• Double-layer capacitance affects interfacial charging and the fraction of current initially or locally unavailable for faradaic chemistry.
• Acid concentration, pKa, and solvent proton activity influence proton-coupled electron transfer and hydrogen-like side reactions.
• Precipitating-salt concentration and solubility product determine obstruction or sequestration by a solid phase.
• Solvent and electrolyte standard-potential shifts change the effective overpotential at a fixed applied voltage.

At −1.2 V, 500 mA, and 3,600 s, the paired S1/E1 system in batch 4 had the best score among the four matched-index pairs. S2/E2 in batch 5 nearly matched its conversion, selectivity, and yield while eliminating the precipitation signal, but its lower ohmic efficiency reduced the balanced score. S3/E3 in batch 6 had little precipitation and high nominal bulk conductivity, yet produced much lower conversion and yield. S0/E0 in batch 3 had near-complete precipitation and lower yield than S1/E1. These results demonstrate that neither conductivity nor suppression of precipitation alone determines performance.

I suspect S1/E1 provides a favorable compromise among transport, potential alignment, proton activity, and interfacial selectivity. E1 has the largest listed diffusivity and a relatively thin diffusion layer, while S1 increases relative diffusivity. Those features are consistent with useful mass transport. Its conductivity is not the highest, which agrees with the observation that S1/E1 does not maximize ohmic efficiency. Its precipitation burden is intermediate rather than minimal.

However, the material experiment was not factorial: solvent and electrolyte were changed together. S1 versus S2 cannot be separated from E1 versus E2. The pairs also differ in combined nominal standard-potential shift, so part of the apparent material ranking may simply reflect different effective overpotential at the shared −1.2 V. Hidden, fixed world-specific transport, solvation, and interface residuals were declared and may also change the ranking. Claims about an independently optimal solvent or independently optimal electrolyte would therefore be unjustified.

5. Precipitation and pH

Precipitation was strongly medium-dependent: approximately 1.0 for S0/E0, 0.70 for S1/E1, and approximately zero for S2/E2 and S3/E3. Yet batch 4 outscored batches 5 and 6. I infer that precipitation can be detrimental but is not the sole bottleneck at this scale. It may reduce active area or transport, but S1/E1 apparently compensates through more favorable electron-transfer or diffusion properties. An alternative is that the precipitation signal reports a spectator equilibrium with limited direct effect on the target reaction.

The normalized pH was also medium-dependent: about 0.23 for S0/E0, 0.206 for S1/E1, 0.179 for S2/E2, and 0.281 for S3/E3 in the representative assays. Within repeated S1/E1 batches it remained near 0.205–0.207, despite large changes in potential and duration. This stability suggests that pH was buffered mainly by the electrolyte formulation rather than being substantially consumed by electrolysis. Proton activity may still affect selectivity and side reactions, but the campaign does not isolate it from other material properties.

A possible precipitation submodel is that a dissolved ion product Q is compared with an effective Ksp modified by solvent. When Q/Ksp exceeds unity, a precipitation fraction grows and may reduce the active transport factor or accessible area. This is conjectural; no direct solid amount or electrode fouling measurement was available.

6. Efficiency relationships and score behavior

The public balanced score weights selective-product yield most heavily, followed by selectivity and energy efficiency, with smaller contributions from conversion, faradaic, transport, and ohmic efficiency. It also gates extremely low yield. That explains why batch 1 scored zero and why the high-yield batches dominated despite imperfect ohmic efficiency.

Faradaic efficiency can be interpreted as the fraction of transferred electronic charge assigned to productive chemistry. Transport efficiency represents the degree to which diffusion and interfacial supply allow that productive current to be sustained. Ohmic efficiency penalizes voltage lost in bulk/contact resistance. Energy efficiency couples product formation to total electrical work and therefore need not move in the same direction as conversion. In batches 9–12, less negative potential apparently reduced parasitic faradaic loss and improved target branching, but the corresponding cell-current/resistance regime lowered the reported ohmic component. At −0.4 V, the yield gain was just sufficient to offset the energy and ohmic penalties, giving the largest observed total score.

A conceptual bookkeeping model is:

productive electron rate ≈ FE × I_actual/(nF),
transport-limited rate ≈ productive electron rate × T_eff,
P(t) ≈ integral[min(kinetic rate, transport-limited rate)] dt,
energy efficiency ≈ useful chemical output/(integral |E × I_actual| dt),
ohmic efficiency ≈ 1 − resistive loss/applied electrical input.

These equations describe plausible couplings rather than fitted laws. The electron stoichiometry n, actual current trajectory, resistance, concentrations during electrolysis, and useful product energy were not observed.

7. Safety and cost

All observed safety risks were well below the 0.65 limit. Risk depended visibly on the solvent pair—about 0.0722 for S0, 0.0956 for S1, 0.1136 for S2, and 0.1262 for S3—but did not visibly increase with potential or electrolysis duration in this campaign. This may mean the benchmark’s reported risk is dominated by material handling at this loading rather than electrical operation. It should not be extrapolated to other volumes, concentrations, currents, or real materials.

S1/E1 batches cost somewhat more than S0/E0 but did not approach a resource constraint. The recommended batch 12 cost about 0.3101 in the public units. Cost was not part of the stated balanced-efficiency score, so the recommendation was driven primarily by product and efficiency metrics.

8. How the explanation changed

Batch 1 established that the initially chosen positive polarity was essentially inactive. Batch 2 reversed the mechanistic picture by showing that cathodic polarization produced selective chemistry. Batch 3 showed that much greater charge opportunity increased conversion, although it did not separate current from time. Batches 4–6 changed the explanation from a simple conductivity-based view to a coupled-medium view: the most conductive or least-precipitating pair was not necessarily best. Batches 7 and 8 showed an approximately cumulative time response without an observed degradation turnover. Batch 9 showed that stronger cathodic drive could be counterproductive. Batches 10–12 then located a broad high-performance region between approximately −0.9 and −0.4 V, with −0.6 and −0.4 V nearly tied in score but differing in their efficiency tradeoffs.

9. Unidentifiable factors and alternatives

The following remain unidentifiable from the campaign:
• Separate solvent and electrolyte main effects and their interaction.
• Actual current versus the configured current cap, total charge passed, and current transients.
• Electron stoichiometry and whether target formation is one elementary step or a sequence.
• Whether selectivity loss at strongly negative voltage is caused by solvent/electrolyte reduction, proton reduction, reactant over-reduction, product degradation, adsorption, or another synthetic side channel.
• Whether precipitation blocks electrodes, sequesters reactant, or is largely spectator behavior.
• Loading, concentration, and volume effects, because all completed batches used the same nominal recipe.
• Repeatability and process variance, because no exact batch was replicated.
• The true local potential optimum; −0.4 V was an edge of the tested high-performing sequence.

A plausible alternative to the side-reaction explanation is that the effective potential shifts supplied by the media make −1.6 and −1.2 V poorly matched to the target redox couple, while −0.6 to −0.4 V aligns it optimally. Another is that large cathodic polarization changes adsorption or depletes reactant at the interface, so the apparent potential effect is fundamentally transport-coupled rather than a direct selectivity effect. A third is that hidden fixed material residuals, rather than the nominal dossier properties, dominate the S1/E1 advantage.

10. Overall interpretation

The world behaves like a cathodic, transport-coupled conversion with a broad voltage window rather than a process improved monotonically by stronger polarization. Product accumulation increases with electrolysis time over the tested range. Medium selection changes effective redox alignment, proton environment, precipitation, transport, and resistive loss simultaneously. S1/E1 gave the best tested compromise, and moderate cathodic polarization around −0.6 to −0.4 V suppressed the losses seen at more negative voltage. Batch 12 is the best observed operating point, but the nearly tied batch 11 and the absence of replicates mean the scientifically defensible conclusion is a high-performing region, not a precisely identified universal optimum.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific prior law or expected optimum was supplied. The material dossier supplied nominal conductivity, diffusivity, diffusion-layer, capacitance, acidity, precipitation, and potential-shift properties, but explicitly presented them as incomplete mechanistic priors rather than a response law.

Supported claims:
• Productive conversion was cathodic in the tested sign convention. Batch 1 at +1.2 V had zero yield and score, whereas batch 2 at −1.2 V produced measurable yield and a score of 0.162 under otherwise comparable conditions. This polarity contrast was the strongest causal evidence.
• Stronger cathodic polarization was not monotonically beneficial. At fixed S1/E1, 500 mA cap, and 14,400 s, performance improved from −1.6 V in batch 9 to −1.2 V in batch 8, −0.9 V in batch 10, and −0.6 V in batch 11. This supported a bounded productive potential window rather than “more voltage is better.”
• Time accumulated conversion over the tested range. At fixed S1/E1, −1.2 V, and 500 mA, batches 4, 7, and 8 increased from 3,600 to 7,200 to 14,400 s; conversion rose from 0.149 to 0.315 to 0.605 and yield from 0.088 to 0.182 to 0.328.
• Conductivity or precipitation alone did not rank the media. Batch 4, S1/E1, outscored the more strongly precipitation-suppressing S2/E2 and S3/E3 batches 5 and 6. S3/E3 also performed poorly despite high nominal electrolyte conductivity.

Contradicted or weakened claims:
• The initial possibility that stronger cathodic drive would increase conversion was contradicted by batches 8–12. Less-negative potentials improved conversion, selectivity, and faradaic efficiency down to −0.4 V.
• The tentative expectation of an observable long-time degradation turnover was not supported: batches 4, 7, and 8 showed continued gains through 14,400 s. This does not prove degradation is absent beyond the tested range.
• A simple “avoid precipitation to maximize score” explanation was contradicted by batch 4 outperforming batches 5 and 6 despite its precipitation signal near 0.70.

Untested or unresolved claims:
• A true interior potential optimum was not located. Batch 12 at −0.4 V had the highest observed score, but it was the least-negative tested point in the refinement sequence and exceeded batch 11 by only about 0.0024.
• Separate solvent and electrolyte effects were untested because batches 3–6 changed both together.
• Current-cap effects were not isolated: batches 2 and 3 changed both current cap and duration.
• Electrode fouling, product degradation, actual current, charge passed, and the identity of competing reactions were not measured.

The evidence that most changed the retrospective explanation was the batch 1/2 polarity reversal, the unexpected S1/E1 advantage in batch 4 despite nonminimal precipitation, and the monotonic improvement from batches 9 through 12 as the potential became less negative.

2. One additional discriminating experiment

I would repeat the batch 8 recipe exactly—0.020 mol reagent, 0.040 L S1, E1, −1.2 V, and 14,400 s—but reduce the current cap from 500 to 100 mA. This directly distinguishes a primarily voltage-controlled side-reaction explanation from a current-density/transport explanation while using batch 8 as the existing comparator.

If selectivity, faradaic efficiency, and energy efficiency remained near batch 8 while conversion and yield fell roughly with available charge, I would favor voltage-dependent branching: the applied potential would determine target versus side-reaction chemistry, while current mainly controls throughput.

If the lower-current experiment substantially increased selectivity and faradaic or transport efficiency, I would shift toward the alternative that high current density causes interfacial depletion, polarization, or transport-induced side chemistry. A large efficiency gain with only a modest yield loss would imply that current optimization is at least as important as potential optimization.

If the result were nearly identical to batch 8 in all metrics, I would infer that the 500 mA cap was not binding and that actual current was limited by the cell. If both yield and efficiencies collapsed at 100 mA, that would support a minimum-current or interfacial activation requirement. An exact replicate would still be desirable afterward because the campaign contains no direct estimate of batch-to-batch process variance.

3. Unused evidence, reliability, and goal effects

Most raw spectral arrays and peak shapes were unused; interpretation relied mainly on calibrated processed estimates. Intermediate UV–vis measurements were used for early directional decisions but not quantitatively modeled because they were noisier than final assays and omitted yield and selectivity. The detailed nominal capacitance, pKa, salt concentration, Ksp, and potential-shift values were not independently identifiable from the paired material screen. Cost, temperature changes, raw mass-balance details, and assay peak-area relationships were also not incorporated into a fitted mechanism. No dedicated pH-meter measurements or exact replicates were collected.

The least reliable recommendation is the distinction between batches 11 and 12. Batch 12 was correctly selected as the highest observation, but its score advantage over batch 11 is too small to establish superiority given channel noise and absent replication. The broader recommendation of S1/E1 near −0.6 to −0.4 V is more reliable than the exact −0.4 V setting.

Among the blind predictions, Q05–Q10 are least reliable because they contain solvent/electrolyte combinations never tested independently. Q11 is also uncertain because the response to a 500 mA cap at the new volume and loading was not isolated. The positive-polarity predictions are directionally more secure—batch 1 strongly indicated negligible target production—but their tiny nonzero assay values remain difficult to predict. Q01 is especially uncertain in score because its predicted yield lies near the 0.02 multiplicative-gate threshold, making small yield errors produce disproportionate score errors.

The assigned goal did affect evidence collection. Maximizing the balanced score encouraged sequential exploitation after S1/E1 and the moderate-potential region looked promising. As a result, later batches refined duration and potential rather than completing a solvent-by-electrolyte factorial design, isolating current from time, or allocating exact replicates. The intermediate-measurement allowance was used broadly, but the design favored locating a strong operating procedure over maximizing mechanistic identifiability. There was no clear conflict with safety—the observed risks remained far below the limit—but the optimization objective reduced the evidence available for causal separation and uncertainty estimation.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.48,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.28,
        "lower80": 0.16,
        "upper80": 0.41
      },
      "faradaic_efficiency": {
        "estimate": 0.39,
        "lower80": 0.27,
        "upper80": 0.52
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.303,
        "lower80": 0.08,
        "upper80": 0.42
      },
      "selective_product_yield": {
        "estimate": 0.023,
        "lower80": 0.006,
        "upper80": 0.047
      },
      "transport_efficiency": {
        "estimate": 0.41,
        "lower80": 0.28,
        "upper80": 0.54
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.012,
        "lower80": 0,
        "upper80": 0.05
      },
      "energy_efficiency": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.03
      },
      "faradaic_efficiency": {
        "estimate": 0.018,
        "lower80": 0,
        "upper80": 0.055
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.012
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0,
        "upper80": 0.012
      },
      "transport_efficiency": {
        "estimate": 0.005,
        "lower80": 0,
        "upper80": 0.035
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.52,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.3,
        "lower80": 0.2,
        "upper80": 0.41
      },
      "faradaic_efficiency": {
        "estimate": 0.4,
        "lower80": 0.3,
        "upper80": 0.52
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.419,
        "lower80": 0.33,
        "upper80": 0.51
      },
      "selective_product_yield": {
        "estimate": 0.25,
        "lower80": 0.16,
        "upper80": 0.36
      },
      "transport_efficiency": {
        "estimate": 0.42,
        "lower80": 0.31,
        "upper80": 0.54
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.015,
        "lower80": 0,
        "upper80": 0.06
      },
      "energy_efficiency": {
        "estimate": 0.008,
        "lower80": 0,
        "upper80": 0.035
      },
      "faradaic_efficiency": {
        "estimate": 0.02,
        "lower80": 0,
        "upper80": 0.06
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.001,
        "lower80": 0,
        "upper80": 0.018
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.008,
        "lower80": 0,
        "upper80": 0.04
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.63,
        "lower80": 0.52,
        "upper80": 0.74
      },
      "energy_efficiency": {
        "estimate": 0.34,
        "lower80": 0.21,
        "upper80": 0.46
      },
      "faradaic_efficiency": {
        "estimate": 0.44,
        "lower80": 0.31,
        "upper80": 0.56
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.443,
        "lower80": 0.34,
        "upper80": 0.55
      },
      "selective_product_yield": {
        "estimate": 0.28,
        "lower80": 0.17,
        "upper80": 0.4
      },
      "transport_efficiency": {
        "estimate": 0.48,
        "lower80": 0.34,
        "upper80": 0.61
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.015,
        "lower80": 0,
        "upper80": 0.065
      },
      "energy_efficiency": {
        "estimate": 0.008,
        "lower80": 0,
        "upper80": 0.04
      },
      "faradaic_efficiency": {
        "estimate": 0.02,
        "lower80": 0,
        "upper80": 0.065
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.001,
        "lower80": 0,
        "upper80": 0.02
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0,
        "upper80": 0.016
      },
      "transport_efficiency": {
        "estimate": 0.008,
        "lower80": 0,
        "upper80": 0.045
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.42,
        "upper80": 0.67
      },
      "energy_efficiency": {
        "estimate": 0.15,
        "lower80": 0.07,
        "upper80": 0.26
      },
      "faradaic_efficiency": {
        "estimate": 0.23,
        "lower80": 0.12,
        "upper80": 0.36
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.295,
        "lower80": 0.21,
        "upper80": 0.39
      },
      "selective_product_yield": {
        "estimate": 0.14,
        "lower80": 0.06,
        "upper80": 0.24
      },
      "transport_efficiency": {
        "estimate": 0.18,
        "lower80": 0.08,
        "upper80": 0.31
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.014,
        "lower80": 0,
        "upper80": 0.06
      },
      "energy_efficiency": {
        "estimate": 0.007,
        "lower80": 0,
        "upper80": 0.035
      },
      "faradaic_efficiency": {
        "estimate": 0.018,
        "lower80": 0,
        "upper80": 0.06
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.001,
        "lower80": 0,
        "upper80": 0.018
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.007,
        "lower80": 0,
        "upper80": 0.04
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.61,
        "lower80": 0.49,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.25,
        "lower80": 0.14,
        "upper80": 0.38
      },
      "faradaic_efficiency": {
        "estimate": 0.31,
        "lower80": 0.19,
        "upper80": 0.44
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.337,
        "lower80": 0.24,
        "upper80": 0.45
      },
      "selective_product_yield": {
        "estimate": 0.19,
        "lower80": 0.1,
        "upper80": 0.31
      },
      "transport_efficiency": {
        "estimate": 0.3,
        "lower80": 0.18,
        "upper80": 0.44
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.014,
        "lower80": 0,
        "upper80": 0.06
      },
      "energy_efficiency": {
        "estimate": 0.007,
        "lower80": 0,
        "upper80": 0.035
      },
      "faradaic_efficiency": {
        "estimate": 0.018,
        "lower80": 0,
        "upper80": 0.06
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.001,
        "lower80": 0,
        "upper80": 0.018
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.007,
        "lower80": 0,
        "upper80": 0.04
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.64,
        "lower80": 0.53,
        "upper80": 0.74
      },
      "energy_efficiency": {
        "estimate": 0.33,
        "lower80": 0.21,
        "upper80": 0.45
      },
      "faradaic_efficiency": {
        "estimate": 0.41,
        "lower80": 0.29,
        "upper80": 0.53
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.452,
        "lower80": 0.35,
        "upper80": 0.56
      },
      "selective_product_yield": {
        "estimate": 0.34,
        "lower80": 0.22,
        "upper80": 0.5
      },
      "transport_efficiency": {
        "estimate": 0.4,
        "lower80": 0.28,
        "upper80": 0.53
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.012,
        "lower80": 0,
        "upper80": 0.055
      },
      "energy_efficiency": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.035
      },
      "faradaic_efficiency": {
        "estimate": 0.016,
        "lower80": 0,
        "upper80": 0.055
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.015
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0,
        "upper80": 0.013
      },
      "transport_efficiency": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.04
      }
    }
  ],
  "rationale": "Predictions are anchored to the campaign’s sharp polarity contrast: negative potentials produced target chemistry, whereas positive potentials gave essentially zero yield and a yield-gated score. The new concentration (0.48 mol/L) is close to the studied 0.50 mol/L, so negative-potential yields were scaled mainly by reagent inventory, duration, current cap, and the observed improvement near −0.8 V relative to −1.2 V. E1 is expected to improve transport and productive charge use, E3 to be transport-limited, and S2 to trade lower precipitation against poorer conductivity. Intervals include assay noise plus substantial extrapolation uncertainty from the untested solvent/electrolyte combinations, absence of exact replicates, and unknown actual current below the configured cap."
}
```
