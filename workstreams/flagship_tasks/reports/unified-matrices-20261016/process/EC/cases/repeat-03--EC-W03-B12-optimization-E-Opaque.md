# repeat-03/EC-W03-B12-optimization-E-Opaque

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-03\EC-W03-B12-optimization-E-Opaque\participant\optimization-E-Opaque

## 同期笔记

### v1 · 公开事件 0

# Electrochemical campaign hypotheses

## Pre-experiment expectations

**H1 [tentative].** At fixed loading (0.020 mol reagent in 0.050 L), balanced efficiency will have an interior optimum in potential magnitude and electrolysis time: weak/short conditions should limit conversion, while strong/long conditions should reduce selectivity and energy efficiency. The preferred potential sign, solvent, and electrolyte are unknown.

**H2 [tentative].** Current-cap increases should help only until charge/transport ceases to be limiting; beyond that, selectivity or efficiency may decline. A polarity screen followed by material and local condition refinement should identify the best procedure.

Predicted test: initial batches spanning both signs, materials, durations, and caps should show enough separation in final-assay score to focus later batches. These expectations will be revised if the public observations contradict them.

### v2 · 公开事件 35

# Electrochemical campaign hypotheses

## Pre-experiment expectations
**H1 [tentative].** At fixed loading (0.020 mol in 0.050 L), balanced efficiency may have an interior optimum in potential magnitude and time.

## Evidence update after batches 1–5
**H2 [supported: polarity, tested scope].** Negative potential is required for the productive direction. At +1.5 V/S0/E0/100 mA/600 s the assay score was 0 with essentially null conversion/yield (event runner-operation-0007), whereas the matched -1.5 V batch scored 0.131 and showed appreciable selectivity and efficiency (runner-operation-0014). I will shelve positive-polarity optimization.

**H3 [unresolved].** Low product yield/conversion, rather than ohmic efficiency, is now the principal bottleneck. Across negative-potential batches 2–5, ohmic efficiency remained high while selective yield stayed near the assay noise scale and scores were only 0–0.140 (events runner-operation-0014, -0021, -0028, -0035). The apparent numerical lead of batch 5 is too small and confounded by changed solvent, electrolyte, potential, cap, and time. Testable consequence: substantially longer electrolysis at a promising negative condition should increase conversion/yield; if it does not, material identity or potential rather than charge exposure dominates.

Decision: use the remaining batches for time/current/potential and then material refinement at fixed 0.020 mol/0.050 L. I will prefer final-assay score over noisy intermediate UV-vis for selection.

### v3 · 公开事件 63

# Electrochemical campaign hypotheses

## Pre-experiment expectations
**H1 [supported in explored scope].** At fixed loading (0.020 mol in 0.050 L), balanced efficiency has competing charge-exposure and current-cap effects.

## Evidence through batch 9
**H2 [supported: polarity].** Negative potential is required for the productive direction: matched +1.5 V and -1.5 V S0/E0, 100 mA, 600 s batches scored 0 and 0.131, respectively (runner-operation-0007, -0014). Positive-polarity optimization is shelved.

**H3 [supported: duration at S0/E0, -1.5 V, 100 mA].** Increasing duration from 600 to 7200 to 14400 s increased observed selective yield from about 0.011 to 0.036 to 0.059 and scores from 0.131 to 0.249 to 0.261 (runner-operation-0014, -0042, -0049). The gain from 7200 to 14400 s is modest in score because efficiency remains limiting.

**H4 [supported nonmonotonic cap effect in tested range].** At 14400 s, raising the cap from 100 to 200 mA improved score to 0.284 and yield to 0.114 (runner-operation-0063), while 500 mA reduced score to 0.220 despite more conversion than 100 mA, because faradaic/transport/energy efficiencies fell (runner-operation-0056). Prediction made now: an intermediate 250–300 mA cap may improve yield without the severe 500 mA efficiency penalty.

Material effects remain unresolved because early material comparisons were confounded. Next: local current/potential refinement, then one or two fixed-condition material comparisons.

### v4 · 公开事件 84

# Electrochemical campaign hypotheses

## Final source-stage interpretation

**H1 [supported in tested scope].** Productive conversion requires negative potential. The matched polarity comparison at S0/E0, 100 mA, 600 s gave score 0 at +1.5 V and 0.131 at -1.5 V (runner-operation-0007 versus runner-operation-0014). This claim is limited to the tested loading/material pair.

**H2 [supported in tested scope].** At S0/E0 and -1.5 V, longer electrolysis improved conversion/yield: 600, 7200, and 14400 s produced progressively higher observed selective yield and score (runner-operation-0014, -0042, -0049). The small late score increment indicates that conversion alone is not the objective; energy/faradaic/transport efficiencies constrain balanced performance.

**H3 [supported: nonmonotonic current-cap tradeoff].** At -1.5 V and 14400 s, 200 mA was better balanced than 100, 300, or 500 mA. The 500 mA batch increased conversion but lost faradaic, transport, and energy efficiency (runner-operation-0056); 200 mA produced the best score among those caps (runner-operation-0063). This supports an interior cap optimum, but it is not proof of a precise optimum because there are no replicates.

**H4 [supported locally].** At 200 mA and 14400 s in S0/E0, reducing magnitude from -1.5 to -1.2 and then -0.9 V numerically improved balanced score from 0.284 to 0.289 to 0.294 (runner-operation-0063, -0077, -0084). Batch 12 (-0.9 V) is the campaign leader with observed yield 0.122, selectivity 0.528, conversion 0.187, energy efficiency 0.183, faradaic efficiency 0.239, transport efficiency 0.260, and ohmic efficiency 0.961. Score differences between batches 11 and 12 are small relative to unquantified process repeatability, so the exact potential optimum remains unresolved.

**Unresolved alternatives.** Early solvent/electrolyte comparisons were confounded with potential, cap, and duration; therefore S0/E0 is the best-tested rather than definitively best material pair. Near-unity precipitation signal in S0 may indicate an unscored operational concern. No replicate precision study was possible within the 12-batch campaign.

**Decision.** Recommend batch 12 because it has the highest public balanced-efficiency-v2 score. This decision would change if replicated local comparisons showed that the 0.005 score advantage over batch 11 is not reproducible, or if a fixed-condition material screen outperformed S0/E0.

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
      "potential_V": 1.5
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
    "cost": 0.2853600084781647,
    "electrochemical_conversion": 0.008014115504920483,
    "electrochemical_selectivity": 0.01034972071647644,
    "energy_efficiency": 0.005256945732980967,
    "faradaic_efficiency": 0.02452157624065876,
    "ohmic_efficiency": 0.9742781519889832,
    "pH_normalized": 0.23031213879585266,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
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
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.5
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
    "cost": 0.2853600084781647,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.48420125246047974,
    "energy_efficiency": 0.0930182933807373,
    "faradaic_efficiency": 0.29009097814559937,
    "ohmic_efficiency": 0.9831159710884094,
    "pH_normalized": 0.2276168018579483,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.1306617259979248,
    "selective_product_yield": 0.011119496077299118,
    "transport_efficiency": 0.31634777784347534
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
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -1.5
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
    "cost": 0.30535998940467834,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.5272122621536255,
    "energy_efficiency": 0.14010117948055267,
    "faradaic_efficiency": 0.267416387796402,
    "ohmic_efficiency": 0.9622116088867188,
    "pH_normalized": 0.21038080751895905,
    "precipitation_signal": 0.6509549021720886,
    "safety_risk": 0.08273958414793015,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.2839733064174652
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
      "solvent": 2,
      "volume_L": 0.05
    },
    {
      "current_mA": 300,
      "electrolyte_profile": 2,
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
    "cost": 0.3413200080394745,
    "electrochemical_conversion": 0.025229385122656822,
    "electrochemical_selectivity": 0.38509824872016907,
    "energy_efficiency": 0.035177066922187805,
    "faradaic_efficiency": 0.23560723662376404,
    "ohmic_efficiency": 0.9053492546081543,
    "pH_normalized": 0.1731279492378235,
    "precipitation_signal": 0.0,
    "safety_risk": 0.10073958337306976,
    "score": 0.1218792200088501,
    "selective_product_yield": 0.012794682756066322,
    "transport_efficiency": 0.2041196972131729
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
      "solvent": 3,
      "volume_L": 0.05
    },
    {
      "current_mA": 300,
      "electrolyte_profile": 3,
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
    "cost": 0.3213199973106384,
    "electrochemical_conversion": 0.023359283804893494,
    "electrochemical_selectivity": 0.3781256079673767,
    "energy_efficiency": 0.017095277085900307,
    "faradaic_efficiency": 0.15332399308681488,
    "ohmic_efficiency": 0.9615349769592285,
    "pH_normalized": 0.28910213708877563,
    "precipitation_signal": 0.0,
    "safety_risk": 0.11333958804607391,
    "score": 0.13960514962673187,
    "selective_product_yield": 0.01586584933102131,
    "transport_efficiency": 0.1428145170211792
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
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.5
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
    "cost": 0.2893199920654297,
    "electrochemical_conversion": 0.056297626346349716,
    "electrochemical_selectivity": 0.4784207046031952,
    "energy_efficiency": 0.10098865628242493,
    "faradaic_efficiency": 0.3142969608306885,
    "ohmic_efficiency": 0.9833386540412903,
    "pH_normalized": 0.229326069355011,
    "precipitation_signal": 0.9978154301643372,
    "safety_risk": 0.05933958664536476,
    "score": 0.24868892133235931,
    "selective_product_yield": 0.03601223975419998,
    "transport_efficiency": 0.28961360454559326
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
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.5
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
    "cost": 0.29363998770713806,
    "electrochemical_conversion": 0.11864611506462097,
    "electrochemical_selectivity": 0.4720104932785034,
    "energy_efficiency": 0.10634071379899979,
    "faradaic_efficiency": 0.29239845275878906,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.22834065556526184,
    "precipitation_signal": 0.9828575253486633,
    "safety_risk": 0.05933958664536476,
    "score": 0.26087766885757446,
    "selective_product_yield": 0.058642320334911346,
    "transport_efficiency": 0.29579880833625793
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
      "volume_L": 0.05
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.5
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
    "cost": 0.32820001244544983,
    "electrochemical_conversion": 0.1987079232931137,
    "electrochemical_selectivity": 0.47942158579826355,
    "energy_efficiency": 0.036322806030511856,
    "faradaic_efficiency": 0.11725063621997833,
    "ohmic_efficiency": 0.9338681101799011,
    "pH_normalized": 0.2266431748867035,
    "precipitation_signal": 0.9957303404808044,
    "safety_risk": 0.05933958664536476,
    "score": 0.2204754501581192,
    "selective_product_yield": 0.0779598280787468,
    "transport_efficiency": 0.11075527966022491
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
      "solvent": 0,
      "volume_L": 0.05
    },
    {
      "current_mA": 200,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.5
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
    "cost": 0.3022800087928772,
    "electrochemical_conversion": 0.20181705057621002,
    "electrochemical_selectivity": 0.467680960893631,
    "energy_efficiency": 0.13199836015701294,
    "faradaic_efficiency": 0.2643442749977112,
    "ohmic_efficiency": 0.9965550899505615,
    "pH_normalized": 0.22865696251392365,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.28440698981285095,
    "selective_product_yield": 0.11436701565980911,
    "transport_efficiency": 0.2851755619049072
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
      "volume_L": 0.05
    },
    {
      "current_mA": 300,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.5
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
    "cost": 0.31092000007629395,
    "electrochemical_conversion": 0.2190885692834854,
    "electrochemical_selectivity": 0.498549222946167,
    "energy_efficiency": 0.082041896879673,
    "faradaic_efficiency": 0.19102667272090912,
    "ohmic_efficiency": 0.9394239187240601,
    "pH_normalized": 0.2263428121805191,
    "precipitation_signal": 0.9927664399147034,
    "safety_risk": 0.05933958664536476,
    "score": 0.25488677620887756,
    "selective_product_yield": 0.09524837136268616,
    "transport_efficiency": 0.1923762559890747
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
      "volume_L": 0.05
    },
    {
      "current_mA": 200,
      "electrolyte_profile": 0,
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
    "cost": 0.2988240122795105,
    "electrochemical_conversion": 0.21717076003551483,
    "electrochemical_selectivity": 0.5015334486961365,
    "energy_efficiency": 0.14740166068077087,
    "faradaic_efficiency": 0.27520251274108887,
    "ohmic_efficiency": 0.9611932039260864,
    "pH_normalized": 0.2273278534412384,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.2888714373111725,
    "selective_product_yield": 0.10552031546831131,
    "transport_efficiency": 0.28238245844841003
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
      "volume_L": 0.05
    },
    {
      "current_mA": 200,
      "electrolyte_profile": 0,
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
    "cost": 0.2953679859638214,
    "electrochemical_conversion": 0.18731053173542023,
    "electrochemical_selectivity": 0.5284345746040344,
    "energy_efficiency": 0.18321822583675385,
    "faradaic_efficiency": 0.23888571560382843,
    "ohmic_efficiency": 0.9607234001159668,
    "pH_normalized": 0.22784817218780518,
    "precipitation_signal": 0.993991494178772,
    "safety_risk": 0.05933958664536476,
    "score": 0.29368525743484497,
    "selective_product_yield": 0.12223687767982483,
    "transport_efficiency": 0.26011064648628235
  }
}
```

## K1 封存报告

## Mechanistic account

I interpret this synthetic electrochemical world as a charge-driven conversion with strong polarity dependence and coupled kinetic, transport, ohmic, and selectivity losses. The useful cathodic direction is represented by negative applied potential. Product formation depends on accumulated effective charge, but the public balanced-efficiency-v2 objective is not maximized simply by maximizing conversion: high current can accelerate conversion while reducing faradaic, transport, and energy efficiencies.

All batches used the same nominal loading—0.020 mol limiting reagent in 0.050 L solvent—so the campaign identifies relationships only at approximately 0.40 mol L⁻¹ initial concentration. Solvent loss from sampling was negligible for interpreting the comparisons.

## Proposed process model

A compact representation is:

1. The applied potential and material identities establish an available electrochemical current,
   I_available = f(V, solvent, electrolyte, composition, time).
2. The actual current is limited by the configured cap:
   I(t) = min(I_cap, I_available).
3. Effective productive charge is
   Q_productive = integral[FE(t) × transport_efficiency(t) × I(t)] dt.
4. Conversion grows with productive charge, approximately as a saturating process such as
   X = 1 − exp(−k_Q Q_productive/n₀),
   where n₀ is initial reagent amount and k_Q includes the unknown electron stoichiometry and calibration.
5. Selective yield is approximately conversion times electrochemical selectivity, with assay noise and possible additional recovery or precipitation effects:
   Y_selective ≈ X × S_electrochemical.
6. Energy efficiency falls when the cell uses excessive voltage or current relative to productive charge. Ohmic efficiency can remain high even when faradaic and transport efficiencies are poor, so ohmic loss is not the only inefficiency.

This is a qualitative model rather than an identified law. The available observations do not provide delivered current, charge, cell resistance, electrode area, concentrations during electrolysis, or electron stoichiometry, so its constants cannot be estimated uniquely.

## Evidence for polarity control

The clearest mechanistic comparison is between batches 1 and 2. Both used solvent-S0, electrolyte-E0, 100 mA, and 600 s, differing principally in potential polarity.

- Batch 1 at +1.5 V scored 0. Its final assay gave conversion 0.0080, selectivity 0.0103, selective yield 0, energy efficiency 0.0053, faradaic efficiency 0.0245, transport efficiency 0, and ohmic efficiency 0.9743.
- Batch 2 at −1.5 V scored 0.1307. Its final assay gave selectivity 0.4842, selective yield 0.0111, energy efficiency 0.0930, faradaic efficiency 0.2901, transport efficiency 0.3163, and ohmic efficiency 0.9831. Reported conversion was clipped or noise-limited at 0 despite nonzero selective yield, illustrating that small assay estimates should not be forced into exact mass-balance identities.

Thus the productive electrode reaction requires negative polarity in the tested S0/E0 system. Positive potential apparently drives the wrong direction or leaves the target pathway electrochemically inaccessible. This finding caused me to abandon positive-potential optimization after batch 1.

## Charge-exposure and duration relationship

Batches 2, 6, and 7 isolate electrolysis duration reasonably well at S0/E0, −1.5 V, and a 100 mA cap:

- Batch 2, 600 s: score 0.1307; selective yield 0.0111.
- Batch 6, 7,200 s: score 0.2487; conversion 0.0563; selective yield 0.0360; selectivity 0.4784; faradaic efficiency 0.3143; transport efficiency 0.2896.
- Batch 7, 14,400 s: score 0.2609; conversion 0.1186; selective yield 0.0586; selectivity 0.4720; faradaic efficiency 0.2924; transport efficiency 0.2958.

Longer electrolysis increased conversion and selective yield while selectivity stayed near 0.47–0.48. This supports accumulated productive charge as a principal state variable. The score gain from 7,200 to 14,400 s was modest relative to the doubling in time because the scoring objective also rewards efficiency, and because conversion may be approaching a slower regime. The data do not distinguish reactant depletion, electrode passivation, mass-transfer limitation, or an intrinsically saturating kinetic law.

## Current-cap coupling and the interior optimum

Batches 7–10 held S0/E0, −1.5 V, and 14,400 s fixed while varying the current cap:

- Batch 7, 100 mA: conversion 0.1186, yield 0.0586, FE 0.2924, transport 0.2958, energy efficiency 0.1063, score 0.2609.
- Batch 9, 200 mA: conversion 0.2018, yield 0.1144, FE 0.2643, transport 0.2852, energy efficiency 0.1320, score 0.2844.
- Batch 10, 300 mA: conversion 0.2191, yield 0.0952, FE 0.1910, transport 0.1924, energy efficiency 0.0820, score 0.2549.
- Batch 8, 500 mA: conversion 0.1987, yield 0.0780, FE 0.1173, transport 0.1108, energy efficiency 0.0363, score 0.2205.

The response is nonmonotonic. Raising the cap from 100 to 200 mA increased conversion and yield enough to improve the balanced score. Above 200 mA, faradaic, transport, and energy efficiencies deteriorated substantially; conversion did not continue to improve reliably, and the score fell. A plausible mechanism is that moderate current reduces charge-transfer limitation, whereas higher current produces concentration polarization and competitive side reactions. The especially low FE and transport efficiency at 500 mA support this interpretation. Another plausible explanation is synthetic current-dependent efficiency penalties rather than a literal physical boundary layer; the public data cannot distinguish those implementations.

Ohmic efficiency stayed comparatively high throughout—0.9966 at 200 mA, 0.9394 at 300 mA, and 0.9339 at 500 mA—so the dominant high-current penalties were not purely ohmic. They were more consistent with nonproductive electron transfer and transport limitation.

## Potential-magnitude effects near the best region

Batches 9, 11, and 12 used S0/E0, 200 mA, and 14,400 s:

- Batch 9 at −1.5 V: conversion 0.2018, selectivity 0.4677, yield 0.1144, energy efficiency 0.1320, FE 0.2643, transport 0.2852, ohmic efficiency 0.9966, score 0.2844.
- Batch 11 at −1.2 V: conversion 0.2172, selectivity 0.5015, yield 0.1055, energy efficiency 0.1474, FE 0.2752, transport 0.2824, ohmic efficiency 0.9612, score 0.2889.
- Batch 12 at −0.9 V: conversion 0.1873, selectivity 0.5284, yield 0.1222, energy efficiency 0.1832, FE 0.2389, transport 0.2601, ohmic efficiency 0.9607, score 0.2937.

Within this local series, reducing the potential magnitude improved selectivity and energy efficiency and produced progressively higher balanced scores, even though conversion did not increase monotonically. Batch 12 had lower conversion than batches 9 and 11 but the highest observed selective yield and selectivity, and the best score. This indicates that excessive overpotential favors competing pathways or wastes energy. The optimum for the balanced objective is therefore shifted toward milder negative potential rather than toward maximum conversion.

I cannot claim that −0.9 V is the true potential optimum. It was the mildest negative potential tested at the best current/time setting, so the optimum could lie at a still less negative value, or batch 12 could exceed batch 11 partly because of assay/process variation. The score difference between batches 11 and 12 was only about 0.0048.

## Solvent, electrolyte, pH, and precipitation

Material effects are poorly identifiable. Early batches changed solvent, electrolyte, potential, current, and time simultaneously:

- Batch 3 used S1/E1, −1.5 V, 100 mA, 600 s and scored 0. Its selectivity was 0.5272, but selective yield was reported as 0; precipitation signal was 0.651.
- Batch 4 used S2/E2, −2.0 V, 300 mA, 1,800 s and scored 0.1219, with conversion 0.0252, selectivity 0.3851, yield 0.0128, and precipitation signal 0.
- Batch 5 used S3/E3 under the same nominal electrical conditions as batch 4 and scored 0.1396, with conversion 0.0234, selectivity 0.3781, yield 0.0159, and precipitation signal 0.

The batch 4 versus 5 comparison weakly suggests that S3/E3 may differ from S2/E2, but the score difference is small and there were no replicates. Because solvent and electrolyte identities were always paired in these screens, their separate effects cannot be inferred. S0/E0 became the best-tested pair, not a demonstrated global material optimum.

S0/E0 batches had normalized pH near 0.227–0.230 and precipitation signals close to 1.0. The best batch 12 had pH_normalized 0.22785 and precipitation_signal 0.99399. In contrast, batches 4 and 5 showed precipitation signal 0. These observations establish a material-dependent association, but not its meaning. Precipitation could represent target isolation, an impurity, electrode fouling, or merely a synthetic diagnostic channel. It was not part of the published score formula, and no direct solid-phase assay was performed. Therefore I do not treat high precipitation as either beneficial or harmful without qualification.

## Relationship to the public score

The public score weights selective product yield most heavily, followed by selectivity and energy efficiency, with additional contributions from conversion, faradaic efficiency, transport efficiency, and ohmic efficiency. This explains why aggressive conditions did not win. Batch 8 had more conversion than batch 7 but a worse score because its efficiency components collapsed. Batch 12 won by balancing moderate conversion with the best observed yield/selectivity combination and improved energy efficiency.

The public contract also specifies a selective-yield gate near 0.02. Very small yields were consequently fragile: batch 3 had a reported yield of zero and score zero, while batch 2 had yield 0.0111 and a nonzero but limited score. I regard the precise low-yield gating behavior as part of the scoring implementation rather than a mechanistic discontinuity in chemistry.

## Role of intermediate measurements

Each batch included one UV–visible measurement, but the final assay was more informative and more precise for selection. Intermediate UV–visible values sometimes tracked the direction of efficiency changes—for example, batch 8 already showed poor FE and transport efficiency at high current—but individual UV–visible energy-efficiency estimates differed appreciably from final-assay estimates. I therefore used them as qualitative diagnostics rather than as exact kinetic observations. Sampling was instantaneous in the synthetic contract and did not advance the reaction.

## Scope and uncertainty

The conclusions apply only to the anonymous benchmark materials, the fixed 0.020 mol/0.050 L loading, the tested batch geometry, electrolysis times up to 14,400 s, and the particular synthetic instrumentation. They make no claim about real chemical identities or transferable electrode chemistry.

Important unidentifiable factors include delivered current versus current cap, electrode area, cell resistance, temperature during electrolysis, electron stoichiometry, kinetic orders, diffusion coefficients, reactant depletion profiles, product degradation rates, and the chemical identity of the precipitate. Solvent and electrolyte effects are confounded. There were no replicated batches, so process repeatability cannot be separated from the declared final-assay noise. Several near-zero estimates were clipped, making low-conversion mass-balance comparisons unreliable.

Plausible alternative models include: a purely empirical response surface with penalties for voltage and current; electrode passivation rather than reactant depletion causing duration saturation; product degradation at high current rather than side-reaction competition; or a material-dependent conductivity rule that indirectly generates the observed FE and transport responses. The campaign supports the qualitative polarity, exposure, and current-tradeoff relationships, but it cannot uniquely select among these microscopic explanations.

Overall, the most defensible explanation is a negative-polarity, charge-accumulating target reaction whose useful rate initially benefits from current and time, coupled to increasingly severe faradaic and mass-transport losses at high current and to selectivity/energy losses at excessive negative potential. Batch 12 best balanced those effects among the tested procedures, but the exact local optimum and the best material pair remain uncertain.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific prior or nominal material-property dossier was supplied. The only initial expectations were self-developed from the public task structure and then tested experimentally.

Supported:
- Productive polarity is negative in the tested S0/E0 system. Batches 1 and 2 were matched at 100 mA and 600 s except for +1.5 versus −1.5 V. Batch 1 scored 0 with essentially null target formation, whereas batch 2 scored 0.131 and showed substantial selectivity and electrochemical efficiencies. This was the clearest evidence that changed my strategy: I stopped exploring positive potentials.
- Product formation depends on accumulated exposure. At S0/E0, −1.5 V, and 100 mA, extending electrolysis from 600 s in batch 2 to 7,200 s in batch 6 and 14,400 s in batch 7 increased selective yield from 0.011 to 0.036 and 0.059, and score from 0.131 to 0.249 and 0.261.
- Current has an interior balanced-performance optimum rather than a monotonic benefit. At −1.5 V for 14,400 s, batch 9 at 200 mA scored 0.284, exceeding batch 7 at 100 mA, batch 10 at 300 mA, and batch 8 at 500 mA. The 500 mA condition retained appreciable conversion but had markedly lower faradaic, transport, and energy efficiencies. This changed my initial broad expectation that more charge delivery would mainly improve the conversion bottleneck.
- Milder negative potential improved the local balance. At 200 mA and 14,400 s, scores increased from 0.284 in batch 9 at −1.5 V to 0.289 in batch 11 at −1.2 V and 0.294 in batch 12 at −0.9 V. Batch 12 combined lower conversion with better selectivity, yield, and energy efficiency, supporting a conversion–selectivity/efficiency tradeoff.

Contradicted or narrowed:
- My initial expectation of a clearly identifiable interior optimum in both potential and time was only partly supported. An interior current-cap optimum was observed, but the best potential was at the mildest boundary tested, −0.9 V, and the best duration remained the longest tested, 14,400 s. Their optima were therefore not bracketed.
- The initial material screen did not identify a defensible best solvent or electrolyte. Batches 3–5 changed materials together with electrical conditions, so their differences could not support the intended material ranking.

Untested or unresolved:
- Whether solvent-S0 or electrolyte-E0 is intrinsically optimal remains untested by a controlled material comparison.
- The proposed microscopic causes of high-current losses—concentration polarization and competing electron-transfer pathways—were not directly measured. Electrode passivation, product degradation, or an empirical simulator penalty remain alternatives.
- The meaning of the near-unity precipitation signal in S0 batches was not identified.
- Loading, concentration, electrode-area, temperature, delivered-current, and repeatability effects were not independently studied.

2. One discriminating experiment

I would run 0.010 mol reagent in 0.025 L S0, preserving the campaign concentration of 0.40 mol L⁻¹, with E0 at −0.9 V, a 200 mA cap, and 14,400 s, followed by the final assay. This would be compared with batch 12, which used twice the reagent and solvent at the same concentration and electrical program.

My leading charge-exposure explanation predicts that approximately the same available charge applied to half as many reagent moles should produce a substantially larger fractional conversion, unless depletion or another loss intervenes. Selectivity and efficiency might remain broadly similar if they are primarily controlled by potential, current density, and material identity.

A large increase in fractional conversion would strengthen the productive-charge-per-mole model and suggest that batch 12 remained charge-limited. Little or no increase, especially with similar efficiency metrics, would favor a time-dependent ceiling such as passivation or deactivation. Lower conversion together with worse faradaic or transport efficiency would instead suggest that vessel geometry, electrode-to-volume scaling, or concentration-independent current density dominates, showing that simple charge-per-mole scaling is inadequate. A large selectivity change would imply that scale or absolute inventory is coupled to the pathway and would weaken the proposed separation between conversion control and potential-controlled selectivity.

3. Unused evidence, reliability, and goal effects

The detailed raw spectra in the characterization artifacts were not inspected; I used processed estimates and supplied peak summaries. Intermediate UV–visible measurements were used only qualitatively because they were noisier and sometimes differed from final-assay estimates. Cost and safety data were nearly constant and nonlimiting in the explored region, so they did not guide optimization. pH and precipitation signals were recorded but not mechanistically resolved. The early material observations in batches 3–5 were largely unusable for causal attribution because solvent, electrolyte, potential, current, and sometimes duration changed together.

The least reliable blind predictions are those involving E1, E3, or solvent-S2—especially Q05–Q10—because the campaign did not isolate those material effects. All predictions also extrapolate from 0.40 mol L⁻¹ and 0.020 mol/0.050 L to 0.48 mol L⁻¹ and 0.012 mol/0.025 L. Predictions at +0.8 V are directionally confident as near-zero production but numerically uncertain near assay clipping and the selective-yield score gate. Q11 at −0.8 V and 500 mA is also uncertain because the campaign never established whether that cap would bind at such a mild potential.

The batch-12 recommendation is the strongest available empirical choice but not highly secure as a universal optimum. Its score exceeded batch 11 by only about 0.0048, with no replication, and neither still milder potentials nor controlled material alternatives were tested.

The assigned goal did affect evidence collection. Maximizing score encouraged sequential exploitation after the polarity and duration findings, leaving few batches for replication, controlled material comparisons, or explicitly mechanistic interventions. The mandatory one-intermediate-measurement-per-batch budget provided useful diagnostics but did not replace time courses or replicates. Thus there was an exploration–optimization tradeoff: the campaign found a better operating point, but causal identification and uncertainty calibration remained weaker. There was no clear conflict in the sense of knowingly discarding a superior observed procedure; rather, the scoring goal shaped which uncertainties remained unresolved.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.54,
        "lower80": 0.43,
        "upper80": 0.64
      },
      "energy_efficiency": {
        "estimate": 0.2,
        "lower80": 0.12,
        "upper80": 0.28
      },
      "faradaic_efficiency": {
        "estimate": 0.29,
        "lower80": 0.21,
        "upper80": 0.37
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.064,
        "lower80": 0.0,
        "upper80": 0.15
      },
      "selective_product_yield": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.019
      },
      "transport_efficiency": {
        "estimate": 0.3,
        "lower80": 0.21,
        "upper80": 0.39
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.055
      },
      "energy_efficiency": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.024
      },
      "faradaic_efficiency": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.025
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0.0,
        "upper80": 0.012
      },
      "transport_efficiency": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.03
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.54,
        "lower80": 0.45,
        "upper80": 0.63
      },
      "energy_efficiency": {
        "estimate": 0.2,
        "lower80": 0.13,
        "upper80": 0.27
      },
      "faradaic_efficiency": {
        "estimate": 0.29,
        "lower80": 0.22,
        "upper80": 0.36
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.278,
        "lower80": 0.21,
        "upper80": 0.34
      },
      "selective_product_yield": {
        "estimate": 0.05,
        "lower80": 0.026,
        "upper80": 0.078
      },
      "transport_efficiency": {
        "estimate": 0.3,
        "lower80": 0.22,
        "upper80": 0.38
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.065
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.027
      },
      "faradaic_efficiency": {
        "estimate": 0.016,
        "lower80": 0.0,
        "upper80": 0.052
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.009,
        "lower80": 0.0,
        "upper80": 0.038
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.014
      },
      "transport_efficiency": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.033
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.43,
        "upper80": 0.66
      },
      "energy_efficiency": {
        "estimate": 0.19,
        "lower80": 0.1,
        "upper80": 0.28
      },
      "faradaic_efficiency": {
        "estimate": 0.27,
        "lower80": 0.17,
        "upper80": 0.37
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.272,
        "lower80": 0.19,
        "upper80": 0.35
      },
      "selective_product_yield": {
        "estimate": 0.048,
        "lower80": 0.02,
        "upper80": 0.08
      },
      "transport_efficiency": {
        "estimate": 0.28,
        "lower80": 0.17,
        "upper80": 0.39
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.03
      },
      "faradaic_efficiency": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.055
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.009,
        "lower80": 0.0,
        "upper80": 0.045
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.035
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.5,
        "lower80": 0.37,
        "upper80": 0.62
      },
      "energy_efficiency": {
        "estimate": 0.14,
        "lower80": 0.06,
        "upper80": 0.23
      },
      "faradaic_efficiency": {
        "estimate": 0.18,
        "lower80": 0.09,
        "upper80": 0.28
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.228,
        "lower80": 0.14,
        "upper80": 0.31
      },
      "selective_product_yield": {
        "estimate": 0.035,
        "lower80": 0.011,
        "upper80": 0.066
      },
      "transport_efficiency": {
        "estimate": 0.17,
        "lower80": 0.07,
        "upper80": 0.28
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.018,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "energy_efficiency": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.03
      },
      "faradaic_efficiency": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.052
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.044
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.035
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.44,
        "lower80": 0.31,
        "upper80": 0.57
      },
      "energy_efficiency": {
        "estimate": 0.16,
        "lower80": 0.07,
        "upper80": 0.25
      },
      "faradaic_efficiency": {
        "estimate": 0.27,
        "lower80": 0.16,
        "upper80": 0.38
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.244,
        "lower80": 0.15,
        "upper80": 0.33
      },
      "selective_product_yield": {
        "estimate": 0.04,
        "lower80": 0.014,
        "upper80": 0.073
      },
      "transport_efficiency": {
        "estimate": 0.25,
        "lower80": 0.13,
        "upper80": 0.37
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "energy_efficiency": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.03
      },
      "faradaic_efficiency": {
        "estimate": 0.014,
        "lower80": 0.0,
        "upper80": 0.055
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.047
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.016
      },
      "transport_efficiency": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.038
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.52,
        "lower80": 0.42,
        "upper80": 0.62
      },
      "energy_efficiency": {
        "estimate": 0.075,
        "lower80": 0.02,
        "upper80": 0.15
      },
      "faradaic_efficiency": {
        "estimate": 0.13,
        "lower80": 0.06,
        "upper80": 0.22
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.233,
        "lower80": 0.17,
        "upper80": 0.3
      },
      "selective_product_yield": {
        "estimate": 0.08,
        "lower80": 0.047,
        "upper80": 0.12
      },
      "transport_efficiency": {
        "estimate": 0.13,
        "lower80": 0.05,
        "upper80": 0.23
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.065
      },
      "energy_efficiency": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.026
      },
      "faradaic_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.045
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.035
      }
    }
  ],
  "rationale": "Negative polarity was strongly productive in the campaign, whereas positive polarity gave essentially zero yield; duration increased charge exposure, and a 500 mA cap traded higher conversion for sharply poorer faradaic, transport, and energy efficiencies. Predictions interpolate the S0/E0 negative-potential results while scaling exposure for the smaller reagent charge, and widen intervals for the unisolated electrolyte/solvent effects and the new concentration. Near-zero positive-polarity yields produce near-zero gated scores."
}
```
