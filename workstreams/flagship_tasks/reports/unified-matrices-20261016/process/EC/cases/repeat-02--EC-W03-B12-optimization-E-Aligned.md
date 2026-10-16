# repeat-02/EC-W03-B12-optimization-E-Aligned

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-02\EC-W03-B12-optimization-E-Aligned\participant\optimization-E-Aligned

## 同期笔记

### v1 · 公开事件 0

# Electrochemical campaign hypotheses

## H1 [tentative; pre-experiment]
At fixed loading (0.020 mol reagent in 0.040 L), balanced score should peak at an intermediate effective driving potential and duration: insufficient charge limits conversion, while excessive potential/time lowers selectivity and energy efficiency. A moderate current cap should avoid transport limitation. This predicts a unimodal response across potential/time rather than monotonic improvement.

## H2 [tentative; pre-experiment]
Materials will shift the optimum. High-conductivity media should improve ohmic efficiency, whereas high diffusivity/thin diffusion layers should improve transport; these gains may trade against proton activity, precipitation, and interfacial selectivity. I will first screen material combinations at common electrolysis conditions, then refine the best region and include repeats to assess whether numerical differences exceed assay variability.

Decision rule: prioritize final-assay score and its weighted components; change the material or driving-condition preference if a comparison shows that yield/selectivity losses outweigh transport/ohmic gains. Intermediate UV-vis will be used diagnostically, not as the final ranking.

### v2 · 公开事件 28

# Electrochemical campaign hypotheses

## H1 [supported in explored positive-potential scope]
At fixed 0.020 mol/0.040 L and +1.0 V, 500 mA cap, 4000 s, performance depends strongly on electrolyte. E1 gave score 0.730 with yield 0.466 (event runner-operation-0014), exceeding E2 (0.660, yield 0.392; runner-operation-0021) and E3 (0.280, yield 0.067; runner-operation-0028). The differences are far larger than the declared assay noise, although there is no repeat yet. E0 at only 100 mA/600 s is confounded by charge and cannot rank materials (runner-operation-0007).

## H2 [revised]
E1 is the working electrolyte for solvent and driving-condition optimization. Its high diffusivity/thin nominal diffusion layer is consistent with observed high transport efficiency, but hidden residuals or kinetics remain alternatives. E3's nominal conductivity did not compensate for very poor faradaic/transport response under this condition.

## H3 [tentative]
For E1 the +1.0 V, 500 mA, 4000 s point is charge-limited rather than overdriven because conversion is only ~0.47 while selectivity and faradaic efficiency remain high. Longer duration may raise yield and score until degradation/energy penalties dominate. I will screen solvents and duration/potential around E1, then repeat the best point.

### v3 · 公开事件 70

# Electrochemical campaign hypotheses

## H1 [supported in tested positive-potential scope]
E1/S1 is the best tested material pair at +1.0 V and 500 mA. At 4000 s it scored 0.744 (runner-operation-0035), versus E1/S0 0.730, E1/S2 0.630, and E1/S3 0.604 (events runner-operation-0014, -0042, -0049). The S1 advantage over S0 is modest relative to a single-run comparison, so repeatability remains important; the larger gaps to S2/S3 are more persuasive.

## H2 [supported; unimodal score with duration]
For E1/S1 at +1.0 V, 500 mA, increasing duration 4000→8000→12000 s raised score 0.744→0.807→0.831 and yield 0.500→0.755→0.911 (runner-operation-0035, -0056, -0063). At 14400 s yield rose slightly to 0.926 but score fell to 0.807 as faradaic and transport efficiencies declined (runner-operation-0070). Thus ~12000 s is the current operating optimum, while the exact maximum is unresolved between sampled durations.

## H3 [testable sign dependence]
The target pathway appears anodic/positive under tested conditions, but sign has not been challenged. Before final recommendation I will test the opposite sign at otherwise matched conditions. If negative potential retains high yield, the assumed polarity specificity is rejected; if yield collapses, polarity becomes a strong categorical control.

Decision: reserve the final batch for a repeat of E1/S1, +1.0 V, 500 mA, 12000 s to assess robustness, unless the sign test unexpectedly outperforms it.

### v4 · 公开事件 84

# Electrochemical campaign conclusions

## H1 [supported in tested scope]
At fixed 0.020 mol reagent in 0.040 L, the best tested procedure is solvent S1/electrolyte E1, +1.0 V, 500 mA cap, 12000 s. Batch 9 scored 0.8306 with yield 0.9109 (runner-operation-0063). An exact repeat scored 0.8134 with yield 0.9047 (runner-operation-0084), supporting robustness of high yield and score while showing run/assay variability in the precise score.

## H2 [supported; bounded duration optimum]
At the recommended materials and electrical setting, score increased from 4000 to 12000 s, then declined at 14400 s despite slightly higher yield (runner-operation-0035, -0056, -0063, -0070). The decline coincided with lower faradaic and transport efficiencies. The optimum is therefore bounded within the long-duration region, but durations between 8000 and 14400 s were not densely resolved.

## H3 [supported polarity advantage, not absolute specificity]
Reversing +1.0 V to -1.0 V at matched S1/E1, 500 mA and 12000 s lowered score from the positive-potential replicate range 0.813–0.831 to 0.477 and yield from ~0.905–0.911 to 0.384 (runner-operation-0077 versus -0063/-0084). Negative potential still produced appreciable conversion/yield, so sign changes pathway efficiency rather than acting as an on/off switch.

## Material interpretation and limits
E1 outperformed E2 and E3 at the common S0 condition; E1/S1 was the strongest tested pair. S1 versus S0 improvement was modest and not repeated independently. Precipitation signal remained substantial (~0.66) at the optimum, so it is not a simple failure indicator in this benchmark. Potential and current-cap response were not independently mapped beyond the sign comparison; the cap is not assumed to equal delivered current. Conclusions apply to the stated loading and sampled settings.

## Recommendation
Select lifecycle batch 9 (+1.0 V, 500 mA cap, 12000 s, S1/E1) because it has the highest observed public balanced-efficiency-v2 score. Batch 12 is confirmatory evidence for the same procedure.

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
    "cost": 0.2828400135040283,
    "electrochemical_conversion": 0.019808726385235786,
    "electrochemical_selectivity": 0.8394781947135925,
    "energy_efficiency": 0.7357316613197327,
    "faradaic_efficiency": 0.7831928730010986,
    "ohmic_efficiency": 0.9659870862960815,
    "pH_normalized": 0.23031213879585266,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.7544891238212585
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
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 4000,
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
    "cost": 0.2906000018119812,
    "electrochemical_conversion": 0.47148334980010986,
    "electrochemical_selectivity": 0.9632416367530823,
    "energy_efficiency": 0.8173479437828064,
    "faradaic_efficiency": 0.9251975417137146,
    "ohmic_efficiency": 0.8710753917694092,
    "pH_normalized": 0.2024710327386856,
    "precipitation_signal": 0.854923665523529,
    "safety_risk": 0.072194404900074,
    "score": 0.7299143075942993,
    "selective_product_yield": 0.46607446670532227,
    "transport_efficiency": 0.9514544010162354
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
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 4000,
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
    "cost": 0.2906000018119812,
    "electrochemical_conversion": 0.45212522149086,
    "electrochemical_selectivity": 0.8679179549217224,
    "energy_efficiency": 0.73640376329422,
    "faradaic_efficiency": 0.8555232882499695,
    "ohmic_efficiency": 0.82923424243927,
    "pH_normalized": 0.15281572937965393,
    "precipitation_signal": 0.0,
    "safety_risk": 0.072194404900074,
    "score": 0.6598108410835266,
    "selective_product_yield": 0.3924684226512909,
    "transport_efficiency": 0.8720801472663879
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
      "current_mA": 500,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 4000,
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
    "cost": 0.2906000018119812,
    "electrochemical_conversion": 0.07513303309679031,
    "electrochemical_selectivity": 0.8101509809494019,
    "energy_efficiency": 0.15661652386188507,
    "faradaic_efficiency": 0.18053549528121948,
    "ohmic_efficiency": 0.8876694440841675,
    "pH_normalized": 0.27337321639060974,
    "precipitation_signal": 0.0,
    "safety_risk": 0.072194404900074,
    "score": 0.2802072763442993,
    "selective_product_yield": 0.06698743253946304,
    "transport_efficiency": 0.14904795587062836
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
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 4000,
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
    "cost": 0.30660000443458557,
    "electrochemical_conversion": 0.5056931376457214,
    "electrochemical_selectivity": 0.9859725832939148,
    "energy_efficiency": 0.773415207862854,
    "faradaic_efficiency": 0.9802079796791077,
    "ohmic_efficiency": 0.8161141276359558,
    "pH_normalized": 0.21465101838111877,
    "precipitation_signal": 0.6510295271873474,
    "safety_risk": 0.09559440612792969,
    "score": 0.7444909811019897,
    "selective_product_yield": 0.5004318952560425,
    "transport_efficiency": 0.9696985483169556
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
      "solvent": 2,
      "volume_L": 0.04
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 4000,
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
    "cost": 0.33219999074935913,
    "electrochemical_conversion": 0.41011443734169006,
    "electrochemical_selectivity": 0.8944819569587708,
    "energy_efficiency": 0.6920269131660461,
    "faradaic_efficiency": 0.8113053441047668,
    "ohmic_efficiency": 0.7832175493240356,
    "pH_normalized": 0.2256777435541153,
    "precipitation_signal": 0.48494383692741394,
    "safety_risk": 0.1135944053530693,
    "score": 0.6297206282615662,
    "selective_product_yield": 0.3735221028327942,
    "transport_efficiency": 0.7866219878196716
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
      "solvent": 3,
      "volume_L": 0.04
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 4000,
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
    "cost": 0.31619998812675476,
    "electrochemical_conversion": 0.3915746510028839,
    "electrochemical_selectivity": 0.8377295732498169,
    "energy_efficiency": 0.71512770652771,
    "faradaic_efficiency": 0.7378029823303223,
    "ohmic_efficiency": 0.8828607797622681,
    "pH_normalized": 0.2136879414319992,
    "precipitation_signal": 0.5617441534996033,
    "safety_risk": 0.12619440257549286,
    "score": 0.6036152839660645,
    "selective_product_yield": 0.32747897505760193,
    "transport_efficiency": 0.7412033081054688
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
      "potential_V": 1
    },
    {
      "duration_s": 8000,
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
    "cost": 0.31459999084472656,
    "electrochemical_conversion": 0.7870999574661255,
    "electrochemical_selectivity": 0.9740456342697144,
    "energy_efficiency": 0.7967399954795837,
    "faradaic_efficiency": 0.7723219990730286,
    "ohmic_efficiency": 0.8348283767700195,
    "pH_normalized": 0.20869219303131104,
    "precipitation_signal": 0.6595747470855713,
    "safety_risk": 0.09559440612792969,
    "score": 0.8068980574607849,
    "selective_product_yield": 0.7550754547119141,
    "transport_efficiency": 0.7658266425132751
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
    "cost": 0.32260000705718994,
    "electrochemical_conversion": 0.9103952646255493,
    "electrochemical_selectivity": 0.9703783988952637,
    "energy_efficiency": 0.8242355585098267,
    "faradaic_efficiency": 0.5781680345535278,
    "ohmic_efficiency": 0.8477693200111389,
    "pH_normalized": 0.2107059806585312,
    "precipitation_signal": 0.6674489378929138,
    "safety_risk": 0.09559440612792969,
    "score": 0.8305894732475281,
    "selective_product_yield": 0.9108541011810303,
    "transport_efficiency": 0.5989992618560791
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
    "cost": 0.32739999890327454,
    "electrochemical_conversion": 0.9631152749061584,
    "electrochemical_selectivity": 0.9985705614089966,
    "energy_efficiency": 0.7009551525115967,
    "faradaic_efficiency": 0.5170475840568542,
    "ohmic_efficiency": 0.8072202205657959,
    "pH_normalized": 0.20839183032512665,
    "precipitation_signal": 0.6566107869148254,
    "safety_risk": 0.09559440612792969,
    "score": 0.8074774146080017,
    "selective_product_yield": 0.925913393497467,
    "transport_efficiency": 0.5183971524238586
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
      "potential_V": -1
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
    "cost": 0.32260000705718994,
    "electrochemical_conversion": 0.6260438561439514,
    "electrochemical_selectivity": 0.6159765720367432,
    "energy_efficiency": 0.3523922860622406,
    "faradaic_efficiency": 0.39624524116516113,
    "ohmic_efficiency": 0.8206984996795654,
    "pH_normalized": 0.20937687158584595,
    "precipitation_signal": 0.6644999384880066,
    "safety_risk": 0.09559440612792969,
    "score": 0.4766700863838196,
    "selective_product_yield": 0.3842085003852844,
    "transport_efficiency": 0.4034251868724823
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
    "cost": 0.32260000705718994,
    "electrochemical_conversion": 0.8958887457847595,
    "electrochemical_selectivity": 0.9622111916542053,
    "energy_efficiency": 0.7842181324958801,
    "faradaic_efficiency": 0.5527094602584839,
    "ohmic_efficiency": 0.8340470194816589,
    "pH_normalized": 0.20989719033241272,
    "precipitation_signal": 0.6578359007835388,
    "safety_risk": 0.09559440612792969,
    "score": 0.8134006857872009,
    "selective_product_yield": 0.904683530330658,
    "transport_efficiency": 0.5739343762397766
  }
}
```

## K1 封存报告

## Mechanistic account

I interpret this world as a coupled electrochemical conversion in which material choice and applied potential determine interfacial kinetics, while current, duration, mass transport, solution resistance, proton activity, and precipitation determine how much of the limiting reagent reaches the desired product and at what energetic cost.

### 1. Observed scoring law

The public results are consistent with the declared balanced-efficiency-v2 score being the weighted sum

S = 0.30Y + 0.15Sel + 0.10X + 0.15E + 0.12F + 0.10T + 0.08O,

where Y is selective-product yield, Sel electrochemical selectivity, X conversion, E energy efficiency, F faradaic efficiency, T transport efficiency, and O ohmic efficiency. A yield gate sets the score to zero when Y is at or below 0.02. For example, inserting batch 9's observations gives approximately 0.831, its reported score. Batch 1 had measured conversion 0.0198 and selectivity 0.839 but zero reported yield and score, consistent with this gate.

This objective creates an important trade-off: maximizing conversion or yield alone is not optimal if the additional charge substantially reduces faradaic, transport, or energy efficiency.

### 2. Proposed process model

A useful qualitative model is:

1. The applied potential is shifted by both electrolyte and solvent properties:

   eta_eff = V_applied - V_threshold - DeltaV_electrolyte - DeltaV_solvent - iR.

   The nominal standard-potential shifts therefore alter the effective overpotential. Hidden, fixed world-specific interfacial and solvation residuals probably modify this expression.

2. The electrochemical rate rises with effective overpotential but is limited by the current cap and mass transport:

   i_delivered = min(i_cap, i_kinetic(eta_eff), i_lim),

   with a limiting current schematically proportional to

   i_lim proportional to D_eff C A / delta_eff.

   Here D_eff and delta_eff depend on the electrolyte, solvent, and their coupling. The supplied nominal diffusivity and diffusion-layer thickness are therefore mechanistically relevant, but they do not fully predict performance.

3. Product formation depends on useful charge and selectivity:

   dP/dt proportional to F(t) Sel(t) i_delivered,

   while reagent depletion can be represented as

   dR/dt = -k_eff(eta_eff, materials, pH) R.

   A simple saturation approximation would be X(t) approximately 1-exp(-k_eff t), although the campaign did not provide enough duration points to establish this exact law.

4. As electrolysis proceeds, reagent depletion and interfacial changes increase the fraction of current going to side reactions. This lowers faradaic and transport efficiency at long duration even while conversion and yield continue increasing. Heating or other time-integrated losses may also reduce energy efficiency.

5. Ohmic efficiency is governed mainly by effective conductivity and cell resistance, for example O decreasing with iR/|V|. The electrode geometry and base resistance were fixed across this campaign, so differences among batches mainly reflect material-dependent conductivity and hidden solvent/electrolyte interactions.

6. Proton activity and precipitation are coupled to materials and conversion. They may change kinetics, product availability, or interface behavior. However, precipitation signal was not a simple failure indicator: the best batches retained a signal near 0.66.

### 3. Evidence that shaped the explanation

#### Initial low-charge batch

Batch 1 used S0/E0, +1.0 V, a 100 mA cap, and 600 s. It produced conversion 0.0198, selectivity 0.839, energy efficiency 0.736, faradaic efficiency 0.783, transport efficiency 0.754, ohmic efficiency 0.966, precipitation signal 1.0, and zero selective yield and score. This initially indicated that respectable efficiency factors are insufficient if too little useful charge is passed. Because both current and duration differed from later batches, batch 1 cannot isolate an E0 material effect.

#### Electrolyte screen

At S0, +1.0 V, 500 mA, and 4000 s:

- Batch 2, E1: score 0.7299, conversion 0.4715, yield 0.4661, selectivity 0.9632, faradaic efficiency 0.9252, transport efficiency 0.9515, and ohmic efficiency 0.8711.
- Batch 3, E2: score 0.6598, conversion 0.4521, yield 0.3925, selectivity 0.8679, faradaic efficiency 0.8555, transport efficiency 0.8721, and ohmic efficiency 0.8292.
- Batch 4, E3: score 0.2802, conversion 0.0751, yield 0.0670, selectivity 0.8102, faradaic efficiency 0.1805, transport efficiency 0.1490, and ohmic efficiency 0.8877.

These results changed my early expectation that nominal bulk conductivity might dominate. E3 had the highest nominal electrolyte conductivity but performed very poorly in faradaic and transport terms. E1, with high nominal diffusivity and a thin diffusion layer, was substantially better overall. The result suggests that mass transport, interfacial kinetics, and electrolyte-specific selectivity dominate over bulk conductivity alone. Hidden material residuals or solvent/electrolyte coupling remain plausible explanations for the unusually poor E3 behavior.

E2 produced zero precipitation signal but still underperformed E1. Thus eliminating the measured precipitation signal was not sufficient to maximize the objective.

#### Solvent screen

With E1, +1.0 V, 500 mA, and 4000 s:

- Batch 2, S0: score 0.7299 and yield 0.4661.
- Batch 5, S1: score 0.7445 and yield 0.5004.
- Batch 6, S2: score 0.6297 and yield 0.3735.
- Batch 7, S3: score 0.6036 and yield 0.3275.

S1 was the best tested solvent. In batch 5 it gave conversion 0.5057, selectivity 0.9860, faradaic efficiency 0.9802, transport efficiency 0.9697, energy efficiency 0.7734, and ohmic efficiency 0.8161. Its advantage over S0 was modest, whereas the deficits of S2 and S3 were much larger. This supports a solvent-dependent balance among diffusivity, potential shift, conductivity, proton activity, and interfacial selectivity rather than a ranking by any single nominal property. The S1-versus-S0 difference was not independently replicated at 4000 s, so its exact magnitude is uncertain.

#### Duration series and the efficiency trade-off

For S1/E1 at +1.0 V and 500 mA:

- Batch 5, 4000 s: score 0.7445, conversion 0.5057, yield 0.5004, F = 0.9802, T = 0.9697.
- Batch 8, 8000 s: score 0.8069, conversion 0.7871, yield 0.7551, F = 0.7723, T = 0.7658.
- Batch 9, 12000 s: score 0.8306, conversion 0.9104, yield 0.9109, F = 0.5782, T = 0.5990.
- Batch 10, 14400 s: score 0.8075, conversion 0.9631, yield 0.9259, F = 0.5170, T = 0.5184.

Conversion and yield rose toward saturation with time, but faradaic and transport efficiencies fell strongly. The score consequently had an interior optimum in the sampled range: the gain from 12000 to 14400 s in conversion and yield was too small to compensate for the efficiency losses. This is the clearest evidence for a depletion- or transport-coupled side-reaction process.

Energy efficiency did not vary monotonically in the individual noisy assays: it was 0.7734, 0.7967, 0.8242, and 0.7010 across those four batches. Nevertheless, the marked decline at 14400 s contributed to the lower score and is compatible with excessive time-integrated charge or side reactions.

Batch 9's selective yield was slightly greater than its measured conversion, and the same occurred in batch 12. I regard these small inconsistencies as assay noise, not evidence for physical yield above conversion.

#### Potential polarity

Batch 11 reversed the potential to -1.0 V while retaining S1/E1, 500 mA, and 12000 s. It gave score 0.4767, conversion 0.6260, yield 0.3842, selectivity 0.6160, energy efficiency 0.3524, faradaic efficiency 0.3962, transport efficiency 0.4034, and ohmic efficiency 0.8207.

Compared with positive-potential batches 9 and 12, the reversed sign caused large losses in desired-product selectivity and charge utilization. This supports a polarity-sensitive target pathway. It is not an absolute on/off polarity rule, because appreciable conversion and product were still observed at -1.0 V. A plausible alternative is that both polarities can drive conversion through different pathways, with the negative-potential pathway producing more side products.

#### Repeatability

Batch 12 exactly repeated the recommended S1/E1, +1.0 V, 500 mA, 12000 s procedure. It gave score 0.8134, conversion 0.8959, yield 0.9047, selectivity 0.9622, energy efficiency 0.7842, faradaic efficiency 0.5527, transport efficiency 0.5739, and ohmic efficiency 0.8340. Batch 9 gave 0.8306 under the same procedure. The repeat supports the robustness of high yield and a score above 0.81, while the 0.017 score difference cautions against treating the exact observed maximum as deterministic.

### 4. Important couplings

The evidence suggests several nonseparable couplings:

- **Potential × material:** nominal potential shifts and hidden interfacial properties change effective overpotential, so the optimum voltage may differ among solvent/electrolyte pairs.
- **Current × transport:** increasing the current cap can improve rate only until kinetic or mass-transfer limitation is reached. Beyond that point it should reduce faradaic and energy efficiency.
- **Duration × conversion × efficiency:** longer time increases conversion toward saturation but progressively lowers faradaic and transport efficiency, generating the observed score maximum.
- **Solvent × electrolyte:** conductivity, diffusivity, proton activity, double-layer capacitance, and solvation jointly determine performance. The rankings cannot be reconstructed from isolated nominal properties.
- **pH/proton activity × selectivity:** pH_normalized stayed near 0.20–0.23 for the strongest E1 experiments, but the available data do not isolate whether this range is causally optimal or merely correlated with E1.
- **Precipitation × interface:** precipitation might remove ions or alter electrode behavior, but a signal near 0.65 coexisted with the best score. It may be a secondary consequence or a partially tolerated process rather than the controlling limitation.

### 5. Scope and unresolved parameters

The conclusions apply directly only to 0.020 mol reagent in 0.040 L solvent, the fixed campaign cell, the tested anonymous materials, and the sampled electrical conditions. Potential magnitude was not mapped systematically: only +1.0 and -1.0 V were directly compared at the final condition. Current-cap response was also not independently measured; 100 mA was used only in the short, confounded first batch, while all later optimization used 500 mA. Therefore the actual delivered-current trajectory, kinetic exchange current, electron stoichiometry, limiting current, and true overpotential are unidentifiable.

Other unidentifiable factors include electrode area and gap, campaign-specific contact resistance, hidden material residuals, interfacial rate constants, side-product identities, whether efficiency decay is caused primarily by depletion, passivation, heating, pH drift, or competing electrochemistry, and whether precipitation is beneficial, harmful, or incidental. The assays provide endpoint metrics rather than species-resolved time courses, so several mechanisms can reproduce the same observations.

Plausible alternatives include electrode passivation rather than bulk depletion as the main cause of declining long-duration efficiency; a solvent-specific kinetic residual rather than nominal S1 diffusivity as the reason S1 performs best; and two parallel polarity-dependent reaction networks rather than a single reversible pathway. The campaign discriminates among operating procedures more strongly than among these microscopic explanations.

### 6. Final mechanistic conclusion

The best-supported picture is a positively favored, mass-transport-sensitive electrochemical conversion. E1/S1 provides the most favorable tested combination of interfacial selectivity and transport. At +1.0 V and a 500 mA cap, useful product accumulates with time, but the reagent becomes progressively harder to convert efficiently and an increasing share of charge is lost to transport limitation or side reactions. Around 12000 s, the high conversion and selective yield still outweigh these efficiency losses; by 14400 s, additional yield is too small to compensate. Batch 9 is the highest observed realization of that balance, and batch 12 confirms that the same procedure reproducibly occupies the high-performing region.

## K2 封存报告

1. **Supported, contradicted, and untested claims**

No instance-specific prior or hidden response law was supplied. The supplied material dossier provided nominal properties and explicitly warned that hidden, fixed material residuals and solvent coupling could change their predictive value. The public scoring weights and the 0.02 selective-yield gate were supplied rather than discovered; the observed scores, including the zero score in batch 1, were consistent with them.

Several self-developed claims were supported:

- **An intermediate electrolysis duration maximizes the balanced score.** For S1/E1 at +1.0 V and 500 mA, increasing duration from 4000 to 8000 to 12000 s raised score from 0.7445 to 0.8069 to 0.8306 in batches 5, 8, and 9. Extending to 14400 s in batch 10 lowered score to 0.8075 even though yield rose from 0.9109 to 0.9259. The simultaneous fall in faradaic and transport efficiencies changed the initial broad expectation of “longer gives more product” into a bounded optimum near 12000 s.
- **E1 is the strongest tested electrolyte under the common screened condition.** At S0, +1.0 V, 500 mA, and 4000 s, batches 2, 3, and 4 gave scores of 0.7299, 0.6598, and 0.2802 for E1, E2, and E3. These differences were much larger than the declared assay noise.
- **Positive polarity favors the target pathway.** Reversing +1.0 V to -1.0 V at matched S1/E1, 500 mA, and 12000 s lowered score from 0.8306 and 0.8134 in positive-potential batches 9 and 12 to 0.4767 in batch 11. Yield fell from about 0.91 to 0.384 and selectivity from about 0.96–0.97 to 0.616.
- **The recommended procedure is reproducibly high-performing.** Batch 12 repeated batch 9 and again produced high yield and a score above 0.81, although it did not reproduce the exact maximum.

Claims that were contradicted or weakened included:

- **Bulk conductivity alone should determine performance.** This was contradicted by batch 4: E3 had the highest nominal bulk conductivity but very poor conversion, faradaic efficiency, transport efficiency, and score. Interfacial kinetics, diffusion, and hidden material couplings must matter substantially.
- **Suppressing precipitation should necessarily improve the objective.** Batch 3 had a zero precipitation signal but underperformed batch 2, while batches 9 and 12 were best despite precipitation signals near 0.66. Precipitation may still have an effect, but it was not a sufficient ranking variable.
- **Polarity might act as an on/off switch.** Batch 11 contradicted that stronger version because negative potential still produced appreciable conversion and product. The evidence supports a quantitative polarity advantage rather than absolute specificity.

Important laws remained untested or only partly tested. The proposed charge-per-mole saturation relationship was consistent with the duration series but was not separated from depletion, passivation, or time-dependent effects. Potential magnitude was not mapped beyond ±1.0 V, and current dependence was not isolated: batch 1 used 100 mA but also differed in electrolyte exposure time, while later optimization used 500 mA. Solvent S1's modest advantage over S0 at 4000 s was not independently replicated. The effects of concentration, volume, electrode history, and electrolyte–solvent interactions were also not factorially identified.

2. **One additional discriminating experiment**

I would run one interrupted-electrolysis experiment at the recommended composition and total productive electrolysis time: S1/E1, 0.020 mol in 0.040 L, +1.0 V, 500 mA for 6000 s; record UV-vis; impose a substantial near-open-circuit rest using the lowest permissible current and approximately zero potential; then restore +1.0 V and 500 mA for another 6000 s, record UV-vis again, terminate, and perform the final assay. Batches 9 and 12 provide continuous-12000-s historical comparators.

The leading explanation is reversible depletion or diffusion-layer polarization, while the principal alternative is irreversible electrode passivation or a purely cumulative side-reaction burden.

- If the interruption restored second-segment faradaic/transport behavior and produced a higher final score than batches 9 and 12 at similar conversion, I would increase confidence in reversible concentration polarization or diffusion-layer relaxation.
- If the interrupted batch closely matched the continuous controls, I would infer that resting does not materially reset the limitation; cumulative reagent depletion or charge-dependent side reactions would remain more plausible.
- If it performed worse, I would suspect time-dependent chemical degradation, precipitation during the rest, or loss of a beneficial activated electrode state.
- If intermediate UV-vis indicated recovery but the final assay did not, I would separate short-timescale transport recovery from irreversible selectivity or product-stability losses.

This single experiment would not uniquely identify every microscopic process, but it would distinguish a recoverable transport limitation from an irreversible, cumulative limitation more directly than another endpoint duration point.

3. **Unused evidence, weak predictions, and goal effects**

The raw characterization artifacts and complete spectra were not inspected; decisions used processed estimates and summarized peaks. Consequently, possible spectral evidence for changing side products, passivation proxies, or concentration trends was unused. The intermediate UV-vis measurements were used mainly as diagnostics and were not formally fitted against final assays. Nominal acid concentration, pKa, capacitance, Ksp, potential shifts, and conductivity were interpreted qualitatively rather than estimated in a quantitative coupled model. Cost and safety data were also not discriminating because all tested risks remained well below the safety limit.

Other unused experimental opportunities included concentration and volume variation, independent current sweeps, a positive-potential magnitude sweep, repeated material-screen points, time-resolved pH, and interrupted or staged electrolysis. Batch 1 was too confounded to provide a clean 100-versus-500 mA comparison.

The least reliable blind predictions are those near the 0.02 yield gate—especially Q01, Q02, Q07, and Q08—because a small yield error can change the score discontinuously from zero to a substantial weighted value. Predictions for E3 at -0.8 V, S2/E0 combinations, and high-current E0 batches are also weak because those exact material, polarity, potential, and current combinations were not studied. All ±0.8 V predictions extrapolate from ±1.0 V rather than from a measured voltage-response curve. Prediction intervals attempted to reflect this, but they remain model-dependent.

The recommendation of the S1/E1, +1.0 V, 500 mA, 12000 s procedure is relatively reliable as a local empirical choice because batches 9 and 12 agree. The claims that 12000 s is the exact optimum, that +1.0 V is the best magnitude, or that 500 mA is the best current are much less reliable. Batch 9's status as the single highest realization may partly reflect measurement or process variation; batch 12 is evidence for the operating region rather than the exact score.

The assigned goal did affect evidence collection. Maximizing the public score encouraged rapid movement from material screening to exploitation of E1/S1 and long-duration refinement. With only 12 final assays, this produced a strong local recommendation but left voltage, current, concentration, repeatability of inferior materials, and microscopic mechanism sparsely studied. There was no clear conflict with safety—the observed risks remained below the limit—but the optimization objective favored endpoint score information over a balanced mechanistic design.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.42,
        "upper80": 0.75
      },
      "energy_efficiency": {
        "estimate": 0.42,
        "lower80": 0.25,
        "upper80": 0.58
      },
      "faradaic_efficiency": {
        "estimate": 0.45,
        "lower80": 0.3,
        "upper80": 0.6
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.38
      },
      "selective_product_yield": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.02
      },
      "transport_efficiency": {
        "estimate": 0.5,
        "lower80": 0.34,
        "upper80": 0.65
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.82,
        "lower80": 0.72,
        "upper80": 0.9
      },
      "energy_efficiency": {
        "estimate": 0.68,
        "lower80": 0.55,
        "upper80": 0.78
      },
      "faradaic_efficiency": {
        "estimate": 0.78,
        "lower80": 0.68,
        "upper80": 0.86
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.52
      },
      "selective_product_yield": {
        "estimate": 0.011,
        "lower80": 0.002,
        "upper80": 0.03
      },
      "transport_efficiency": {
        "estimate": 0.74,
        "lower80": 0.62,
        "upper80": 0.83
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.48,
        "upper80": 0.71
      },
      "energy_efficiency": {
        "estimate": 0.38,
        "lower80": 0.24,
        "upper80": 0.51
      },
      "faradaic_efficiency": {
        "estimate": 0.4,
        "lower80": 0.27,
        "upper80": 0.54
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.368,
        "lower80": 0.29,
        "upper80": 0.45
      },
      "selective_product_yield": {
        "estimate": 0.108,
        "lower80": 0.05,
        "upper80": 0.18
      },
      "transport_efficiency": {
        "estimate": 0.45,
        "lower80": 0.31,
        "upper80": 0.59
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.83,
        "lower80": 0.75,
        "upper80": 0.9
      },
      "energy_efficiency": {
        "estimate": 0.64,
        "lower80": 0.51,
        "upper80": 0.74
      },
      "faradaic_efficiency": {
        "estimate": 0.72,
        "lower80": 0.59,
        "upper80": 0.82
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.559,
        "lower80": 0.47,
        "upper80": 0.65
      },
      "selective_product_yield": {
        "estimate": 0.249,
        "lower80": 0.15,
        "upper80": 0.36
      },
      "transport_efficiency": {
        "estimate": 0.7,
        "lower80": 0.56,
        "upper80": 0.8
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.66,
        "lower80": 0.54,
        "upper80": 0.77
      },
      "energy_efficiency": {
        "estimate": 0.45,
        "lower80": 0.31,
        "upper80": 0.58
      },
      "faradaic_efficiency": {
        "estimate": 0.5,
        "lower80": 0.36,
        "upper80": 0.64
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.409,
        "lower80": 0.32,
        "upper80": 0.5
      },
      "selective_product_yield": {
        "estimate": 0.118,
        "lower80": 0.06,
        "upper80": 0.2
      },
      "transport_efficiency": {
        "estimate": 0.57,
        "lower80": 0.42,
        "upper80": 0.7
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.95,
        "lower80": 0.88,
        "upper80": 0.99
      },
      "energy_efficiency": {
        "estimate": 0.78,
        "lower80": 0.66,
        "upper80": 0.88
      },
      "faradaic_efficiency": {
        "estimate": 0.91,
        "lower80": 0.82,
        "upper80": 0.98
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.633,
        "lower80": 0.54,
        "upper80": 0.72
      },
      "selective_product_yield": {
        "estimate": 0.246,
        "lower80": 0.15,
        "upper80": 0.36
      },
      "transport_efficiency": {
        "estimate": 0.93,
        "lower80": 0.84,
        "upper80": 0.99
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.38,
        "upper80": 0.69
      },
      "energy_efficiency": {
        "estimate": 0.12,
        "lower80": 0.04,
        "upper80": 0.23
      },
      "faradaic_efficiency": {
        "estimate": 0.14,
        "lower80": 0.05,
        "upper80": 0.25
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.27
      },
      "selective_product_yield": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.025
      },
      "transport_efficiency": {
        "estimate": 0.14,
        "lower80": 0.05,
        "upper80": 0.26
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.78,
        "lower80": 0.65,
        "upper80": 0.88
      },
      "energy_efficiency": {
        "estimate": 0.18,
        "lower80": 0.08,
        "upper80": 0.29
      },
      "faradaic_efficiency": {
        "estimate": 0.2,
        "lower80": 0.1,
        "upper80": 0.32
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.27,
        "lower80": 0.0,
        "upper80": 0.36
      },
      "selective_product_yield": {
        "estimate": 0.027,
        "lower80": 0.01,
        "upper80": 0.055
      },
      "transport_efficiency": {
        "estimate": 0.18,
        "lower80": 0.08,
        "upper80": 0.3
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.4,
        "upper80": 0.68
      },
      "energy_efficiency": {
        "estimate": 0.28,
        "lower80": 0.15,
        "upper80": 0.41
      },
      "faradaic_efficiency": {
        "estimate": 0.32,
        "lower80": 0.18,
        "upper80": 0.47
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.295,
        "lower80": 0.21,
        "upper80": 0.39
      },
      "selective_product_yield": {
        "estimate": 0.066,
        "lower80": 0.025,
        "upper80": 0.13
      },
      "transport_efficiency": {
        "estimate": 0.36,
        "lower80": 0.21,
        "upper80": 0.51
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.78,
        "lower80": 0.66,
        "upper80": 0.87
      },
      "energy_efficiency": {
        "estimate": 0.52,
        "lower80": 0.38,
        "upper80": 0.65
      },
      "faradaic_efficiency": {
        "estimate": 0.62,
        "lower80": 0.47,
        "upper80": 0.75
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.47,
        "lower80": 0.38,
        "upper80": 0.56
      },
      "selective_product_yield": {
        "estimate": 0.179,
        "lower80": 0.09,
        "upper80": 0.29
      },
      "transport_efficiency": {
        "estimate": 0.6,
        "lower80": 0.44,
        "upper80": 0.73
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.43,
        "upper80": 0.67
      },
      "energy_efficiency": {
        "estimate": 0.28,
        "lower80": 0.15,
        "upper80": 0.42
      },
      "faradaic_efficiency": {
        "estimate": 0.28,
        "lower80": 0.16,
        "upper80": 0.42
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.404,
        "lower80": 0.31,
        "upper80": 0.5
      },
      "selective_product_yield": {
        "estimate": 0.29,
        "lower80": 0.17,
        "upper80": 0.43
      },
      "transport_efficiency": {
        "estimate": 0.32,
        "lower80": 0.19,
        "upper80": 0.46
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.8,
        "lower80": 0.7,
        "upper80": 0.88
      },
      "energy_efficiency": {
        "estimate": 0.58,
        "lower80": 0.45,
        "upper80": 0.7
      },
      "faradaic_efficiency": {
        "estimate": 0.45,
        "lower80": 0.31,
        "upper80": 0.59
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.644,
        "lower80": 0.55,
        "upper80": 0.73
      },
      "selective_product_yield": {
        "estimate": 0.622,
        "lower80": 0.49,
        "upper80": 0.75
      },
      "transport_efficiency": {
        "estimate": 0.45,
        "lower80": 0.31,
        "upper80": 0.6
      }
    }
  ],
  "rationale": "Predictions use campaign-observed charge-per-mole saturation, the strong positive-polarity advantage, electrolyte ranking (E1 best and E3 poorest), solvent penalties, and declining faradaic/transport efficiency at high conversion. The 0.48 M query loading is close to the studied 0.50 M loading. Intervals combine assay noise with wider extrapolation uncertainty for untested ±0.8 V and material combinations; score intervals also reflect the discontinuous 0.02 selective-yield gate."
}
```
