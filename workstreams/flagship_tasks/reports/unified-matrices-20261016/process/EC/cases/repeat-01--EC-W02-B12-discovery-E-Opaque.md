# repeat-01/EC-W02-B12-discovery-E-Opaque

既有科学公开材料；非provider内部推理。

来源：D:\Projects\ChemWorld-local-research\20261016-unified-matrices\attempt-01\repeat-01\EC-W02-B12-discovery-E-Opaque\participant\discovery-E-Opaque

## 同期笔记

### v1 · 公开事件 0

# Electrochemical hypothesis notebook

## Pre-experiment expectations
H1 [tentative]: Product formation requires electrolysis above a sign-dependent potential threshold; conversion should rise with delivered charge then saturate, while excessive magnitude/time may reduce selectivity through degradation.

H2 [tentative]: Solvent and electrolyte identities will affect transport/ohmic efficiency and may shift the productive potential window. A balanced medium should maximize selective yield rather than conversion alone.

Plan: use fixed loading (0.020 mol reagent in 0.050 L solvent) for comparability, screen both potential signs, magnitude, time/current cap, and anonymous materials. Use one intermediate UV-vis per batch when useful. Results that show similar outcomes across sign or material controls would weaken the corresponding claims.

### v2 · 公开事件 28

# Electrochemical hypothesis notebook

## H1 [supported in tested S0/E0 scope]
Product formation is strongly polarity-selective and has a bounded potential window. At +1 V, 100 mA cap, 1800 s, final conversion/selective yield were about 0.052/0.025 with high selectivity and efficiency (runner-operation-0007). Reversing to -1 V sharply reduced conversion and efficiency (runner-operation-0014). Increasing magnitude to ±2 V did not improve conversion: +2 V produced no detected product metrics (runner-operation-0021), while -2 V remained weak (runner-operation-0028). Thus a monotone magnitude law is rejected; a peak near the modest positive region is plausible. The exact threshold/peak remains unresolved.

## H2 [unresolved]
Medium and electrolyte may control transport/ohmic response and yield. Only S0/E0 has been tested, so no material claim yet.

## H3 [tentative; prediction before next tests]
At +1 V, conversion should increase with cumulative electrolysis time before saturation. If the cap is binding, lowering the current cap should slow conversion; matching nominal charge with fourfold time may approximately restore it. Intermediate UV-vis is noisier and reports efficiency rather than conversion here, so final assays will anchor comparisons.

Next: two time/current-cap experiments followed by one-factor solvent and electrolyte screens at fixed 0.020 mol/0.050 L loading.

### v3 · 公开事件 44

# Electrochemical hypothesis notebook

## H1 [supported in tested S0/E0 scope]
Product formation is strongly polarity-selective and has a bounded potential window. +1 V outperformed -1 V and ±2 V in the initial single-segment screen (runner-operation-0007, -0014, -0021, -0028). A monotone potential-magnitude law is rejected; a modest positive window is favored.

## H2 [unresolved]
Medium/electrolyte effects remain untested; screen next with one-factor changes.

## H3 [revised: simple cumulative-charge model rejected]
Prediction was that longer cumulative time or charge matching would preserve/improve conversion. Instead, splitting 1800 s into 300+1500 s at 100 mA gave high early UV-vis efficiencies but much lower final efficiency/conversion than the single 1800 s batch (runner-operation-0033 vs -0036 and -0007). At 25 mA, 1800 s UV-vis was also high, but extending to 7200 s ended with low conversion/efficiency (runner-operation-0041 vs -0044). This is consistent with time-dependent product loss/passivation after an initially efficient regime, but segmentation itself and between-batch variability are confounded. The nominal-charge equivalence model is not supported.

Testable consequence: single uninterrupted runs near the productive +1 V condition should be preferred over long/segmented exposure. A repeat demonstrating stable high final outcome would make intrinsic segmentation/time damage more plausible; large replicate scatter would instead favor batch variability.

### v4 · 公开事件 86

# Electrochemical hypothesis notebook

## H1 [supported in tested loading and S0/E0 scope]
The response has a sign-selective, non-monotone potential window. At fixed 0.020 mol reagent in 0.050 L, +1 V/100 mA/1800 s produced the strongest initial S0/E0 outcome (runner-operation-0007); -1 V was much weaker (runner-operation-0014), +2 V gave zero reported conversion/yield (runner-operation-0021), and -2 V was weak (runner-operation-0028). This supports a productive modest-positive regime plus off-window loss/passivation, not a function of absolute voltage alone. Exact onset and peak are unresolved because intermediate potentials were not sampled.

## H2 [supported qualitatively; factor interactions unresolved]
Anonymous media change distinct response components at +1 V/100 mA/1800 s. Relative to S0/E0 (runner-operation-0007), S1 retained comparable conversion but lower efficiencies and higher risk (runner-operation-0051); S2 had poor selective yield (runner-operation-0058); S3 combined high selectivity/energy efficiency and selective yield with lower conversion and higher risk (runner-operation-0065). Changing electrolyte in S0 showed E1 as the best balanced case, with high conversion, selectivity and efficiencies (runner-operation-0072); E2 was moderately productive and nearly eliminated precipitation signal while shifting pH lower (runner-operation-0079); E3 had low conversion but nonzero selective yield and no precipitation signal (runner-operation-0086). Material effects therefore appear multidimensional rather than a single conductivity ranking. Each comparison is unreplicated, so numerical differences near assay/process uncertainty remain unresolved and solvent-electrolyte interactions were not tested.

## H3 [simple cumulative-charge account rejected; mechanistic alternative unresolved]
Segmented runs showed high early UV-vis efficiencies followed by much poorer final conversion/efficiency after further electrolysis (runner-operation-0033 to -0036; runner-operation-0041 to -0044). A matched nominal charge at lower cap/longer time did not restore the original single-segment outcome. Candidate explanations are time-dependent passivation/product loss, sensitivity to operation segmentation, or batch variability. Because the 100 mA segmented run had the same total duration as the original but disagreed, duration alone is insufficient; replicate single-segment and deliberately segmented pairs would discriminate alternatives.

## Predictive account and scope
For 0.020 mol in 0.050 L, expect best balanced performance near +1 V, with severe suppression on negative polarity and at +2 V. Current/time should not be modeled only by I×t: an initially efficient regime can decay during prolonged or repeated segments. E1 in S0 is the leading balanced formulation; S3/E0 may favor selective yield/energy efficiency at the cost of risk and conversion; E2/E3 suppress precipitation. Quantitative extrapolation beyond sampled potentials, loadings, and material combinations remains uncertain.

## Decision
Recommend batch 10 (S0/E1, +1 V, 100 mA cap, uninterrupted 1800 s) as the best balanced observed operating point (runner-operation-0072). This would change if replicated batches show its advantage is within process variability or if a solvent-electrolyte interaction yields a superior robust window.

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
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 1800,
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
    "cost": 0.28571999073028564,
    "electrochemical_conversion": 0.05233539268374443,
    "electrochemical_selectivity": 0.8980063199996948,
    "energy_efficiency": 0.8702253699302673,
    "faradaic_efficiency": 0.9748222827911377,
    "ohmic_efficiency": 0.9653005003929138,
    "pH_normalized": 0.22897005081176758,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.5668513178825378,
    "selective_product_yield": 0.02522830292582512,
    "transport_efficiency": 0.9461185336112976
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
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1
    },
    {
      "duration_s": 1800,
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
    "cost": 0.28571999073028564,
    "electrochemical_conversion": 0.009975438006222248,
    "electrochemical_selectivity": 0.5760180354118347,
    "energy_efficiency": 0.25159168243408203,
    "faradaic_efficiency": 0.38621339201927185,
    "ohmic_efficiency": 0.9741383194923401,
    "pH_normalized": 0.22627469897270203,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.28424787521362305,
    "selective_product_yield": 0.019178958609700203,
    "transport_efficiency": 0.4124701917171478
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
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 2
    },
    {
      "duration_s": 1800,
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
    "cost": 0.28644001483917236,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.0,
    "ohmic_efficiency": 0.9736917614936829,
    "pH_normalized": 0.22698970139026642,
    "precipitation_signal": 0.9871450662612915,
    "safety_risk": 0.05933958664536476,
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
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -2
    },
    {
      "duration_s": 1800,
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
    "cost": 0.28644001483917236,
    "electrochemical_conversion": 0.007706241216510534,
    "electrochemical_selectivity": 0.4232766330242157,
    "energy_efficiency": 0.028069986030459404,
    "faradaic_efficiency": 0.27460572123527527,
    "ohmic_efficiency": 0.985849916934967,
    "pH_normalized": 0.22629910707473755,
    "precipitation_signal": 0.987893283367157,
    "safety_risk": 0.05933958664536476,
    "score": 0.061741042882204056,
    "selective_product_yield": 0.005982661619782448,
    "transport_efficiency": 0.24311818182468414
  }
}
```

### 批次 5 · 终点事件 36

```json
{
  "ordinal": 5,
  "lifecycle_index": 5,
  "end_step": 36,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.05
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
      "duration_s": 1500,
      "operation": "electrolyze"
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
    "cost": 0.30371999740600586,
    "electrochemical_conversion": 0.011582084000110626,
    "electrochemical_selectivity": 0.8902111649513245,
    "energy_efficiency": 0.12119372934103012,
    "faradaic_efficiency": 0.17469176650047302,
    "ohmic_efficiency": 0.9725042581558228,
    "pH_normalized": 0.23124182224273682,
    "precipitation_signal": 0.987224280834198,
    "safety_risk": 0.05933958664536476,
    "score": 0.20121967792510986,
    "selective_product_yield": 0.014769427478313446,
    "transport_efficiency": 0.16418230533599854
  }
}
```

### 批次 6 · 终点事件 44

```json
{
  "ordinal": 6,
  "lifecycle_index": 6,
  "end_step": 44,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.05
    },
    {
      "current_mA": 25,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 1800,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "duration_s": 5400,
      "operation": "electrolyze"
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
    "cost": 0.30371999740600586,
    "electrochemical_conversion": 0.012874608859419823,
    "electrochemical_selectivity": 0.8731366395950317,
    "energy_efficiency": 0.2391219139099121,
    "faradaic_efficiency": 0.28640761971473694,
    "ohmic_efficiency": 0.9935307502746582,
    "pH_normalized": 0.22796587646007538,
    "precipitation_signal": 0.9978545308113098,
    "safety_risk": 0.05933958664536476,
    "score": 0.2947360873222351,
    "selective_product_yield": 0.018785813823342323,
    "transport_efficiency": 0.2617242932319641
  }
}
```

### 批次 7 · 终点事件 51

```json
{
  "ordinal": 7,
  "lifecycle_index": 7,
  "end_step": 51,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 1800,
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
    "cost": 0.3057200014591217,
    "electrochemical_conversion": 0.04888518154621124,
    "electrochemical_selectivity": 0.8456712365150452,
    "energy_efficiency": 0.8206965923309326,
    "faradaic_efficiency": 0.8283283710479736,
    "ohmic_efficiency": 0.9994011521339417,
    "pH_normalized": 0.2320316880941391,
    "precipitation_signal": 0.9784285426139832,
    "safety_risk": 0.08273958414793015,
    "score": 0.5293564200401306,
    "selective_product_yield": 0.03996109589934349,
    "transport_efficiency": 0.8317286968231201
  }
}
```

### 批次 8 · 终点事件 58

```json
{
  "ordinal": 8,
  "lifecycle_index": 8,
  "end_step": 58,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 1800,
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
    "cost": 0.33772000670433044,
    "electrochemical_conversion": 0.021697623655200005,
    "electrochemical_selectivity": 0.863889753818512,
    "energy_efficiency": 0.6837108135223389,
    "faradaic_efficiency": 0.5807086229324341,
    "ohmic_efficiency": 0.9766117930412292,
    "pH_normalized": 0.247245654463768,
    "precipitation_signal": 0.9851889610290527,
    "safety_risk": 0.10073958337306976,
    "score": 0.052694886922836304,
    "selective_product_yield": 0.0023937898222357035,
    "transport_efficiency": 0.5742132663726807
  }
}
```

### 批次 9 · 终点事件 65

```json
{
  "ordinal": 9,
  "lifecycle_index": 9,
  "end_step": 65,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 3,
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 1800,
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
    "cost": 0.3177199959754944,
    "electrochemical_conversion": 0.030035467818379402,
    "electrochemical_selectivity": 0.9234119653701782,
    "energy_efficiency": 0.9389678835868835,
    "faradaic_efficiency": 0.676113486289978,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.2377985417842865,
    "precipitation_signal": 0.9959874749183655,
    "safety_risk": 0.11333958804607391,
    "score": 0.527291476726532,
    "selective_product_yield": 0.047009509056806564,
    "transport_efficiency": 0.6969447135925293
  }
}
```

### 批次 10 · 终点事件 72

```json
{
  "ordinal": 10,
  "lifecycle_index": 10,
  "end_step": 72,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 1800,
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
    "cost": 0.28571999073028564,
    "electrochemical_conversion": 0.057565659284591675,
    "electrochemical_selectivity": 0.9619195461273193,
    "energy_efficiency": 0.9281471371650696,
    "faradaic_efficiency": 0.9137532114982605,
    "ohmic_efficiency": 0.958005964756012,
    "pH_normalized": 0.19996103644371033,
    "precipitation_signal": 0.8492700457572937,
    "safety_risk": 0.05933958664536476,
    "score": 0.5782721042633057,
    "selective_product_yield": 0.03734789043664932,
    "transport_efficiency": 0.9151028394699097
  }
}
```

### 批次 11 · 终点事件 79

```json
{
  "ordinal": 11,
  "lifecycle_index": 11,
  "end_step": 79,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 1800,
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
    "cost": 0.28571999073028564,
    "electrochemical_conversion": 0.05105088651180267,
    "electrochemical_selectivity": 0.843726634979248,
    "energy_efficiency": 0.8321650624275208,
    "faradaic_efficiency": 0.8083652853965759,
    "ohmic_efficiency": 0.9637795686721802,
    "pH_normalized": 0.15215590596199036,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.05933958664536476,
    "score": 0.5222423076629639,
    "selective_product_yield": 0.03364243730902672,
    "transport_efficiency": 0.8155452013015747
  }
}
```

### 批次 12 · 终点事件 86

```json
{
  "ordinal": 12,
  "lifecycle_index": 12,
  "end_step": 86,
  "actions": [
    {
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 1800,
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
    "cost": 0.28571999073028564,
    "electrochemical_conversion": 0.014712505042552948,
    "electrochemical_selectivity": 0.8623121976852417,
    "energy_efficiency": 0.8501046895980835,
    "faradaic_efficiency": 0.6331492066383362,
    "ohmic_efficiency": 0.9921419024467468,
    "pH_normalized": 0.2690844237804413,
    "precipitation_signal": 0.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.4906495213508606,
    "selective_product_yield": 0.03843022882938385,
    "transport_efficiency": 0.6543741822242737
  }
}
```

## K1 封存报告

## 1. Empirical scope

All completed batches used 0.020 mol of anonymous limiting reagent in 0.050 L of solvent (nominal initial concentration 0.40 mol L⁻¹). The principal reference treatment was solvent S0, electrolyte E0, +1.0 V, a 100 mA current cap, and 1800 s of electrolysis. Because the materials are anonymous benchmark formulations, this report describes functional roles rather than real chemical identities.

The measured outputs should be treated as distinct operational metrics. In particular, selective-product yield is not consistently equal to conversion × selectivity: batch 9 reported conversion 0.0300 but selective-product yield 0.0470, whereas batch 10 reported conversion 0.0576, selectivity 0.9619, and yield 0.0373. I therefore do not impose an ordinary material-balance identity on those three processed channels.

## 2. Proposed phenomenological mechanism

I infer a polarity-selective electrochemical pathway with a relatively narrow productive potential window near +1 V. A useful schematic is

reactant --(productive electron transfer)--> target

competing with

reactant/current --(wrong polarity or excessive driving force)--> unproductive states, electrode passivation, degradation, or bypass current.

Transport through the solvent/electrolyte and interfacial charge transfer determine how much imposed current reaches the productive pathway. Electrolyte identity additionally controls acid/base state and precipitation, which can change the fraction of material remaining electrochemically accessible.

A compact model would be

C = clip[A(S,E) · G(V;S,E) · H(I,t,n) + εC, 0, 1],

Y = clip[B(S,E) · GY(V;S,E) · HY(I,t,n) + εY, 0, 1],

where C is measured conversion, Y is the independently calibrated selective-product-yield channel, S and E are solvent and electrolyte, V is potential, I is the current cap, t is exposure time, and n represents the number or pattern of electrolysis segments. G is strongly asymmetric in voltage and peaks in a modest positive region. H cannot be reduced confidently to total nominal charge Q = It. The errors include both process variability and instrument noise.

A possible voltage kernel is a positive-polarity gate multiplied by a peaked function, for example

G(V) ≈ 1(V > V_on) exp[-(V − V*)²/w²],

with V* near +1 V under S0/E0. This equation is only a qualitative interpolation: the campaign did not sample enough intermediate potentials to estimate V_on, V*, or w.

Faradaic and transport efficiencies appear to be the main efficiency channels that track productive operation. Ohmic efficiency remained high in many unsuccessful batches, so low bulk resistance alone is insufficient. Energy efficiency then reflects a coupling among productive faradaic current, transport, potential, and material response rather than simply ohmic efficiency.

## 3. Evidence for the potential-window mechanism

Batch 1, at S0/E0, +1 V, 100 mA, and one uninterrupted 1800 s segment, produced conversion 0.0523, selectivity 0.8980, selective-product yield 0.0252, faradaic efficiency 0.9748, transport efficiency 0.9461, ohmic efficiency 0.9653, and energy efficiency 0.8702. Its score was 0.5669.

Changing only the potential sign to −1 V in batch 2 reduced conversion to 0.0100, selectivity to 0.5760, yield to 0.0192, faradaic efficiency to 0.3862, transport efficiency to 0.4125, and energy efficiency to 0.2516. This is strong evidence that the mechanism is polarity-sensitive rather than dependent only on |V|.

Increasing the positive potential to +2 V in batch 3 did not improve the reaction: reported conversion, selectivity, selective yield, faradaic efficiency, transport efficiency, and energy efficiency were all zero, while ohmic efficiency remained 0.9737. Thus the cell could remain ohmically conductive while essentially none of the response was assigned to productive chemistry. This observation changed my initial expectation of a simple threshold followed by monotonic acceleration and instead supports a bounded window or severe high-potential inhibition.

Batch 4 at −2 V was also weak: conversion 0.00771, selectivity 0.4233, yield 0.00598, faradaic efficiency 0.2746, transport efficiency 0.2431, and energy efficiency 0.0281. Together, batches 1–4 establish the ordering +1 V ≫ −1 V > −2 V and +2 V ≈ inactive for the measured productive response under S0/E0. They do not identify the exact optimum, since 0–0.9 V and 1.1–1.9 V were not tested.

Plausible physical interpretations include a required reduction/oxidation direction followed by an overpotential-driven side reaction, destruction of a reactive intermediate at +2 V, electrode-film formation, or diversion of current into an unobserved reaction. These alternatives cannot be separated with the available observables.

## 4. Time, current, charge, and segmentation

The campaign does not support a model in which outcome is determined solely by Q = It.

Batch 5 used the same S0/E0, +1 V, 100 mA, and total 1800 s as batch 1, but electrolysis was split into 300 s and 1500 s segments. Its UV-vis measurement after 300 s indicated high instantaneous processed efficiencies: faradaic 0.9722, transport 0.9487, ohmic 0.9502, and energy 0.9058. After the second segment, however, the final assay reported conversion 0.0116, yield 0.0148, faradaic efficiency 0.1747, transport efficiency 0.1642, and energy efficiency 0.1212. This differed greatly from batch 1 despite the same nominal final charge of 180 C.

Batch 6 used a 25 mA cap for 1800 s, followed by another 5400 s, for the same nominal total charge of 180 C over 7200 s. The intermediate UV-vis efficiencies after 1800 s were again high (faradaic 0.9530, transport 0.9280, energy 0.8537), but the final assay gave conversion 0.0129, yield 0.0188, faradaic efficiency 0.2864, transport efficiency 0.2617, and energy efficiency 0.2391.

These results are consistent with an initially efficient regime followed by passivation, product loss, depletion of an electroactive interfacial species, or activation of a competing pathway. A simple illustrative extension is

H(I,t,n) = formation(I,t) · exp[-k_loss t − k_seg max(n−1,0)],

but neither k_loss nor k_seg is identifiable. Batch 5 is especially important because total current cap and duration matched batch 1; therefore elapsed duration alone cannot explain their difference. Operation segmentation might matter, but ordinary between-batch process variability is an equally plausible explanation.

There is also an instrument confound: the early values came from UV-vis and the endpoints from the final assay, which have different noise and calibration profiles. Consequently, the apparent within-batch decline is suggestive rather than a direct, instrument-matched kinetic measurement. The defensible conclusion is that nominal charge equivalence failed, not that a particular decay law was proven.

## 5. Solvent coupling

Batches 7–9 changed solvent while retaining E0, +1 V, 100 mA, and one 1800 s segment.

Batch 7 (S1/E0) gave conversion 0.0489, selectivity 0.8457, yield 0.0400, faradaic efficiency 0.8283, transport efficiency 0.8317, ohmic efficiency 0.9994, and energy efficiency 0.8207. It preserved conversion reasonably well but reduced faradaic and transport performance relative to batch 1. Safety risk increased from 0.0593 for S0 to 0.0827.

Batch 8 (S2/E0) was substantially poorer: conversion 0.0217, yield 0.00239, faradaic efficiency 0.5807, transport efficiency 0.5742, and energy efficiency 0.6837. Its selectivity among the measured response remained 0.8639, showing that high selectivity alone did not ensure appreciable target yield. Risk was 0.1007.

Batch 9 (S3/E0) produced conversion 0.0300 but selectivity 0.9234, yield 0.0470, and energy efficiency 0.9390; faradaic and transport efficiencies were lower at 0.6761 and 0.6969. Risk was highest among the solvent screen at 0.1133, still well below the campaign safety limit of 0.65.

I infer that solvents alter at least two separable factors: availability/transport of electroactive material and the partitioning or detection of selective product. S1 favored conversion retention, S2 was generally unfavorable, and S3 favored selectivity, the selective-yield channel, and energy efficiency despite lower conversion. Because each solvent was tested once and only with E0, solvent rankings may change with electrolyte; no solvent–electrolyte interaction parameters are identifiable.

## 6. Electrolyte, pH, and precipitation coupling

Batches 10–12 changed electrolyte in S0 at +1 V, 100 mA, and 1800 s.

Batch 10 (E1) was the strongest balanced observation: conversion 0.0576, selectivity 0.9619, yield 0.0373, faradaic efficiency 0.9138, transport efficiency 0.9151, ohmic efficiency 0.9580, energy efficiency 0.9281, pH-normalized response 0.2000, precipitation signal 0.8493, and score 0.5783.

Batch 11 (E2) gave conversion 0.0511, selectivity 0.8437, yield 0.0336, faradaic efficiency 0.8084, transport efficiency 0.8155, energy efficiency 0.8322, pH-normalized response 0.1522, and precipitation signal only 0.00524.

Batch 12 (E3) had low conversion, 0.0147, but yield 0.0384 and selectivity 0.8623. Faradaic and transport efficiencies were 0.6331 and 0.6544, energy efficiency was 0.8501, pH-normalized response was 0.2691, and precipitation signal was zero.

The reference E0 endpoint in batch 1 had pH-normalized response 0.2290 and precipitation signal 1.0. Thus electrolyte identity strongly controls precipitation: E2 and E3 nearly abolished it, while E0 and E1 retained substantial signals. This is not explained by pH alone, because E2 had a lower pH-normalized value than E0 whereas E3 had a higher value, yet both suppressed precipitation. Electrolyte-specific ion pairing, solubility, interfacial adsorption, or complexation is therefore more plausible than a single scalar pH law.

Precipitation is not simply detrimental within these data. The best balanced batch, E1, still had a large precipitation signal, while E2 suppressed precipitation but did not surpass E1. The precipitate might contain an inert electrolyte component, target, impurity, or reactant; the hidden species mapping prevents identification. E1 may improve the productive potential window while tolerating some precipitation, whereas E2/E3 alter phase behavior more strongly.

## 7. Integrated interpretation

The most economical account is a coupled electrochemical-transport system:

1. A polarity-specific interfacial electron-transfer step is activated near a modest positive potential.
2. Excess positive driving force around +2 V diverts current or disables the productive pathway, even though the cell remains ohmically efficient.
3. Solvent and electrolyte independently affect transport, faradaic partitioning, product environment, and precipitation.
4. Ohmic efficiency is usually near unity and is not the principal bottleneck. Faradaic and transport efficiencies better distinguish productive from unproductive settings.
5. Extended or segmented operation can end in a low-efficiency state; total charge alone does not predict the endpoint.
6. Electrolyte controls pH/precipitation and likely shifts interfacial kinetics, but precipitation is not a sufficient predictor of performance.

For prediction only within the studied loading, I would use a hierarchical response surface with categorical solvent/electrolyte factors, an asymmetric peaked voltage term, and explicit time/current/segmentation terms rather than Q alone. I would allow separate equations for conversion, selective yield, and each efficiency channel, with correlated process noise. The leading observed balanced region is S0/E1 near +1 V with a 100 mA cap and a single 1800 s exposure. S3/E0 is a plausible alternative when selective-yield and energy-efficiency channels are emphasized over conversion and risk.

## 8. Limitations and plausible alternatives

All material comparisons were unreplicated. The large difference between batches 1 and 5 demonstrates that process variability or segmentation effects can be substantial, so modest numerical rankings should not be treated as exact material constants. Instrument noise was declared, but the magnitude of batch-to-batch process variability was not independently determined.

Only one reagent loading, one liquid volume, four coarse potentials, two current caps, and a few timing patterns were explored. Concentration effects, true current histories, electrode area, temperature evolution, mass-transfer coefficients, and chemical species identities were not observed. No no-electrolysis blank was assayed. Solvent–electrolyte combinations outside the one-factor screens were not tested.

The narrow-window interpretation could alternatively reflect a hard simulator threshold, electrode passivation, irreversible intermediate destruction, or material-specific spectral visibility rather than a single molecular transition-state mechanism. The apparent time decay could instead be segmentation sensitivity, assay differences, or stochastic batch heterogeneity. The precipitation signal could represent product isolation, reactant loss, or an unrelated salt phase. These explanations remain observationally equivalent in the completed campaign.

The strongest conclusions are therefore qualitative: productive behavior is highly polarity- and voltage-window-dependent; material identity changes different response components in different directions; E1/S0 was the best balanced observed formulation; E2/E3 strongly suppressed precipitation; and a charge-only kinetic model is inadequate.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific prior or nominal material-property dossier was supplied. The solvent and electrolyte labels were explicitly opaque, so all substantive laws below were self-developed from the campaign.

Supported:
- A polarity-sensitive productive pathway was supported. Under otherwise matched S0/E0 conditions, batch 1 at +1 V gave conversion 0.0523 and score 0.5669, whereas batch 2 at −1 V gave conversion 0.0100 and score 0.2842.
- A bounded positive-potential window was supported qualitatively. Batch 3 at +2 V reported zero productive metrics despite ohmic efficiency 0.9737, changing my initial view from a simple positive threshold with increasing response to a non-monotone window near +1 V.
- Solvent and electrolyte identities affect different response components rather than merely conductivity. Batches 7–9 separated solvent effects, while batches 10–12 showed electrolyte-dependent conversion, efficiency, pH, and precipitation. Batch 10 (E1) was the best balanced observation; batches 11 and 12 nearly eliminated precipitation without becoming the best overall conditions.
- Ohmic efficiency alone is not a sufficient predictor. Batch 3 retained high ohmic efficiency while productive response was absent; faradaic and transport efficiencies were more diagnostic.

Contradicted or weakened:
- A response law depending only on voltage magnitude was contradicted by batches 1–4: +1 V was productive, −1 V was much weaker, and ±2 V were poor.
- A monotonic “more positive potential gives more conversion” law was contradicted by batch 3 at +2 V.
- A simple cumulative-charge law based only on Q = It was contradicted or at least strongly weakened. Batch 1 and batch 5 both nominally used +1 V, 100 mA, and 1800 s, yet batch 5’s segmented treatment ended with conversion 0.0116 versus 0.0523 in batch 1. Batch 6 delivered the same nominal 180 C at 25 mA over 7200 s but ended with conversion 0.0129. Segmentation, process variability, and different intermediate/final instruments remain confounded, so a specific decay mechanism was not proven.
- A one-dimensional pH explanation for precipitation was weakened by batches 11 and 12: both suppressed precipitation, although their normalized pH values moved in different directions relative to E0.

Untested or unidentifiable:
- The exact onset, optimum, and width of the positive potential window were untested because no intermediate potential between +1 and +2 V was studied.
- Solvent–electrolyte interactions were untested; the material screens changed one factor at a time.
- Molecular identities, electron stoichiometry, precipitate composition, electrode-film formation, and whether the lost response represented reactant loss or product degradation were unidentifiable.
- The proposed peaked voltage equation and explicit passivation/segmentation terms were phenomenological conjectures, not fitted laws.

2. Most informative additional experiment

I would repeat batch 1 exactly: 0.020 mol reagent, 0.050 L S0, E0, +1 V, 100 mA, one uninterrupted 1800 s electrolysis, termination, and final assay. This single experiment most directly distinguishes my leading explanation—that the low batch-5 endpoint arose from segmentation-associated state change or passivation—from the alternative that the difference between batches 1 and 5 was mainly ordinary batch variability.

If the repeat were close to batch 1, with conversion near 0.05 and high faradaic/transport efficiencies, I would strengthen the claim that uninterrupted operation reproducibly maintains the productive regime and that segmentation contributed to batch 5’s collapse. If it instead resembled batch 5, with conversion around 0.01 and low final efficiencies, I would treat batch 1 as a possible favorable outlier and substantially weaken both the segmentation mechanism and the operating recommendation’s precision. An intermediate result or large disagreement among metrics would leave process variability dominant and motivate replicated uninterrupted-versus-segmented pairs; one extra batch cannot by itself separate passivation from every segmentation artifact.

3. Unused evidence, reliability, and goal effects

The account relied mainly on processed final-assay values and selected UV-vis estimates. Raw spectral shapes, peak assignments, and any detailed mass-balance fields were not analyzed, so they did not constrain the mechanism. Cost was largely unused, and safety risk was used only qualitatively when comparing solvents. Intermediate UV-vis observations were not fitted quantitatively because they lacked the full endpoint metric set and used a different calibration/noise profile from the final assay. The campaign also produced no true replication, so process variance was not estimated independently.

The least reliable predictions are Q11 and Q12 because 500 mA was far outside the tested 25–100 mA range. Q03–Q10 are also weak because uninterrupted 7200 s behavior was never directly observed; their material, polarity, duration, concentration, and potential effects must be extrapolated jointly. Scores for low-yield cases are especially uncertain because the 0.02 selective-yield gate amplifies small yield errors. Q01 and Q02 avoid the long-duration extrapolation but still use an untested 0.48 mol L⁻¹ loading, 0.8 V, and 600 s duration. The batch-10 recommendation is the best observed choice, but it is unreplicated and may not survive solvent–electrolyte interaction testing.

The mechanism-first assigned goal materially affected evidence collection: I favored broad polarity, solvent, electrolyte, and time/current coverage over repeated local optimization around the best score. That breadth enabled the qualitative account but left the leading condition and process variability poorly replicated. There was no clear conflict with safety—the observed risks remained below the stated limit—and the broad study still found batch 10, the highest-scoring observed batch, as the final recommendation.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.35,
        "upper80": 0.82
      },
      "energy_efficiency": {
        "estimate": 0.32,
        "lower80": 0.1,
        "upper80": 0.58
      },
      "faradaic_efficiency": {
        "estimate": 0.42,
        "lower80": 0.18,
        "upper80": 0.68
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.159,
        "lower80": 0.01,
        "upper80": 0.34
      },
      "selective_product_yield": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.025
      },
      "transport_efficiency": {
        "estimate": 0.44,
        "lower80": 0.2,
        "upper80": 0.7
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.9,
        "lower80": 0.72,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.9,
        "lower80": 0.7,
        "upper80": 0.99
      },
      "faradaic_efficiency": {
        "estimate": 0.95,
        "lower80": 0.78,
        "upper80": 1.0
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.567,
        "lower80": 0.22,
        "upper80": 0.65
      },
      "selective_product_yield": {
        "estimate": 0.03,
        "lower80": 0.012,
        "upper80": 0.055
      },
      "transport_efficiency": {
        "estimate": 0.93,
        "lower80": 0.75,
        "upper80": 1.0
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.25,
        "upper80": 0.82
      },
      "energy_efficiency": {
        "estimate": 0.18,
        "lower80": 0.0,
        "upper80": 0.45
      },
      "faradaic_efficiency": {
        "estimate": 0.3,
        "lower80": 0.05,
        "upper80": 0.6
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.159,
        "lower80": 0.0,
        "upper80": 0.32
      },
      "selective_product_yield": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.03
      },
      "transport_efficiency": {
        "estimate": 0.32,
        "lower80": 0.08,
        "upper80": 0.62
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.87,
        "lower80": 0.65,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.55,
        "lower80": 0.2,
        "upper80": 0.9
      },
      "faradaic_efficiency": {
        "estimate": 0.55,
        "lower80": 0.2,
        "upper80": 0.9
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.421,
        "lower80": 0.12,
        "upper80": 0.62
      },
      "selective_product_yield": {
        "estimate": 0.022,
        "lower80": 0.006,
        "upper80": 0.06
      },
      "transport_efficiency": {
        "estimate": 0.55,
        "lower80": 0.2,
        "upper80": 0.88
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.68,
        "lower80": 0.38,
        "upper80": 0.9
      },
      "energy_efficiency": {
        "estimate": 0.35,
        "lower80": 0.1,
        "upper80": 0.67
      },
      "faradaic_efficiency": {
        "estimate": 0.45,
        "lower80": 0.17,
        "upper80": 0.75
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.271,
        "lower80": 0.03,
        "upper80": 0.45
      },
      "selective_product_yield": {
        "estimate": 0.016,
        "lower80": 0.002,
        "upper80": 0.04
      },
      "transport_efficiency": {
        "estimate": 0.47,
        "lower80": 0.18,
        "upper80": 0.77
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.94,
        "lower80": 0.77,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.78,
        "lower80": 0.42,
        "upper80": 0.98
      },
      "faradaic_efficiency": {
        "estimate": 0.82,
        "lower80": 0.48,
        "upper80": 0.99
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.529,
        "lower80": 0.25,
        "upper80": 0.67
      },
      "selective_product_yield": {
        "estimate": 0.035,
        "lower80": 0.012,
        "upper80": 0.07
      },
      "transport_efficiency": {
        "estimate": 0.82,
        "lower80": 0.47,
        "upper80": 0.99
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.65,
        "lower80": 0.32,
        "upper80": 0.88
      },
      "energy_efficiency": {
        "estimate": 0.38,
        "lower80": 0.11,
        "upper80": 0.7
      },
      "faradaic_efficiency": {
        "estimate": 0.3,
        "lower80": 0.06,
        "upper80": 0.62
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.23,
        "lower80": 0.02,
        "upper80": 0.42
      },
      "selective_product_yield": {
        "estimate": 0.015,
        "lower80": 0.001,
        "upper80": 0.042
      },
      "transport_efficiency": {
        "estimate": 0.32,
        "lower80": 0.07,
        "upper80": 0.64
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.87,
        "lower80": 0.65,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.7,
        "lower80": 0.36,
        "upper80": 0.94
      },
      "faradaic_efficiency": {
        "estimate": 0.48,
        "lower80": 0.18,
        "upper80": 0.78
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.436,
        "lower80": 0.17,
        "upper80": 0.59
      },
      "selective_product_yield": {
        "estimate": 0.035,
        "lower80": 0.012,
        "upper80": 0.07
      },
      "transport_efficiency": {
        "estimate": 0.52,
        "lower80": 0.21,
        "upper80": 0.81
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.22,
        "upper80": 0.8
      },
      "energy_efficiency": {
        "estimate": 0.2,
        "lower80": 0.0,
        "upper80": 0.49
      },
      "faradaic_efficiency": {
        "estimate": 0.25,
        "lower80": 0.02,
        "upper80": 0.55
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.05,
        "lower80": 0.0,
        "upper80": 0.2
      },
      "selective_product_yield": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.018
      },
      "transport_efficiency": {
        "estimate": 0.27,
        "lower80": 0.03,
        "upper80": 0.57
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.85,
        "lower80": 0.61,
        "upper80": 0.97
      },
      "energy_efficiency": {
        "estimate": 0.55,
        "lower80": 0.22,
        "upper80": 0.84
      },
      "faradaic_efficiency": {
        "estimate": 0.45,
        "lower80": 0.14,
        "upper80": 0.75
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.118,
        "lower80": 0.0,
        "upper80": 0.4
      },
      "selective_product_yield": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.025
      },
      "transport_efficiency": {
        "estimate": 0.48,
        "lower80": 0.17,
        "upper80": 0.78
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.45,
        "lower80": 0.12,
        "upper80": 0.73
      },
      "energy_efficiency": {
        "estimate": 0.08,
        "lower80": 0.0,
        "upper80": 0.3
      },
      "faradaic_efficiency": {
        "estimate": 0.12,
        "lower80": 0.0,
        "upper80": 0.38
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.027,
        "lower80": 0.0,
        "upper80": 0.14
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.014
      },
      "transport_efficiency": {
        "estimate": 0.15,
        "lower80": 0.0,
        "upper80": 0.43
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.75,
        "lower80": 0.45,
        "upper80": 0.94
      },
      "energy_efficiency": {
        "estimate": 0.25,
        "lower80": 0.04,
        "upper80": 0.58
      },
      "faradaic_efficiency": {
        "estimate": 0.3,
        "lower80": 0.05,
        "upper80": 0.62
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.179,
        "lower80": 0.01,
        "upper80": 0.4
      },
      "selective_product_yield": {
        "estimate": 0.012,
        "lower80": 0.001,
        "upper80": 0.035
      },
      "transport_efficiency": {
        "estimate": 0.35,
        "lower80": 0.08,
        "upper80": 0.68
      }
    }
  ],
  "rationale": "Predictions use the observed polarity-selective window near +1 V, the failure of charge-only scaling, and the measured E1, E3, and S2 effects. Positive 0.8 V is treated as near the productive window; negative polarity, long exposure, and especially the 500 mA cap reduce expected productive efficiencies. E1 improves the positive-polarity balance, E3 preserves yield better than conversion, and S2 strongly suppresses yield. Intervals are deliberately broad because the new concentration, 0.8 V, uninterrupted 7200 s runs, high-current cases, and their interactions were not directly tested; the selective-yield score gate also makes low-yield score uncertainty asymmetric."
}
```
