# repeat-01/EC-W01-B12-discovery-E-Opaque

既有科学公开材料；非provider内部推理。

来源：D:\Projects\ChemWorld-local-research\20261016-unified-matrices\attempt-01\repeat-01\EC-W01-B12-discovery-E-Opaque\participant\discovery-E-Opaque

## 同期笔记

### v1 · 公开事件 0

# Electrochemical hypothesis notebook

## Pre-experiment expectations

**H1 [tentative].** Product formation should be polarity-dependent and increase with electrolysis time or current cap until conversion saturates; excessive magnitude/time may lower selectivity or energy efficiency through side reactions. This predicts a non-monotonic yield optimum across potential magnitude and duration.

**H2 [tentative].** Solvent and electrolyte identities may separately affect transport/ohmic efficiency and intrinsic selectivity. A screening design will first compare materials under a common loading (0.020 mol reagent in 0.040 L solvent), then probe voltage, current-cap, time, polarity, and segmentation around informative conditions.

Intermediate UV-vis snapshots will be used once per batch as supporting kinetic/efficiency evidence; final assays are authoritative. Material effects remain unresolved until direct comparisons are obtained.

### v2 · 公开事件 21

# Electrochemical hypothesis notebook

## Current hypotheses

**H1 [supported in sign, narrowed].** Under S0/E0 at 0.020 mol in 0.040 L, the productive/efficient polarity is positive near +1 V. Batch 1 (+1 V, 100 mA cap, 600 s; final event runner-operation-0007) retained high selectivity and efficiencies but only ~0.021 conversion. Batch 2 at -1 V (runner-operation-0014) showed substantially worse efficiencies and no resolved conversion; Batch 3 at +2 V (runner-operation-0021) collapsed faradaic and transport efficiencies. Thus response is strongly non-monotonic in signed potential, opposing a simple magnitude-only law.

**H2 [tentative].** Near +1 V, conversion is charge/time limited while selectivity remains high. Prediction before the next experiment: extending +1 V/100 mA from 600 to 6000 s should raise conversion materially, unless passivation or reagent-access limits dominate.

**H3 [unresolved].** The final precipitation signal is near saturation in all first three batches, so it does not yet distinguish productive chemistry from a medium/loading effect. Solvent/electrolyte comparisons remain necessary.

### v3 · 公开事件 42

# Electrochemical hypothesis notebook

## Current hypotheses

**H1 [supported in tested S0/E0 scope].** Response is strongly dependent on signed potential: +1 V is productive; -1 V and +2 V are poor (final events runner-operation-0007, -0014, -0021). A simple absolute-potential model is rejected. The likely useful window is intermediate positive potential.

**H2 [supported qualitatively; quantitative form unresolved].** At +1 V, longer time increases conversion: 6000 s/100 mA produced ~0.115 conversion and ~0.112 selective yield (runner-operation-0028), versus ~0.021 conversion and zero-resolved yield at 600 s (runner-operation-0007). Lowering the cap to 20 mA at 6000 s reduced conversion to ~0.032 but increased faradaic/transport efficiency to ~0.93/0.92 (runner-operation-0035). Raising it to 500 mA destroyed selectivity and most efficiency (runner-operation-0042). Thus current cap affects both productive charge and a steep high-current loss, not merely rate.

**Predictive working model.** In the +1 V window and before strong depletion, conversion should scale approximately with an effective charge term, while efficiencies decline with current stress. A long, moderate-current run (40 mA, 14400 s) should approach the conversion of 100 mA, 6000 s but retain better efficiencies. This prediction is prospective.

**H3 [unresolved].** Precipitation remains near saturation and appears weakly informative at this loading. Material effects are not yet tested.

### v4 · 公开事件 63

# Electrochemical hypothesis notebook

## Current hypotheses

**H1 [supported in tested range].** At fixed S0/E0 loading, signed potential has an intermediate positive optimum: +1 V outperformed -1 V, +2 V, and +0.7 V in the tested designs (runner-operation-0014, -0021, -0049, -0056). The comparison with +0.7 V is partly linked to yield and efficiency differences larger than individual final-assay noise scales, but only single batches were run.

**H2 [supported qualitatively].** Conversion depends on effective charge/time, while current stress penalizes selectivity and faradaic/transport efficiency. The prospective prediction was borne out: +1 V, 40 mA, 14400 s reached ~0.147 conversion, ~0.136 yield, and ~0.92 faradaic/transport efficiency (runner-operation-0049), improving the overall balance over 100 mA/6000 s (runner-operation-0028) and avoiding the collapse at 500 mA (runner-operation-0042). Exact functional form and depletion behavior remain unresolved.

**H3 [tentative material effect].** Replacing S0 by S1 at +1 V/40 mA/14400 s gave similar selective yield (~0.136) and high selectivity, with higher energy efficiency but somewhat lower faradaic/transport efficiency (runner-operation-0063 versus -0049). This is numerical evidence from unreplicated batches, not yet a secure solvent effect.

**H4 [unresolved].** Precipitation stays near saturation across conditions and is likely dominated by fixed loading/medium rather than conversion. Electrolyte comparisons and remaining material combinations will test transport/ohmic sensitivity.

### v5 · 公开事件 84

# Electrochemical hypothesis notebook

## Final source-stage synthesis

**H1 [supported within the sampled loading and materials].** The electrochemical response is polarity-specific and non-monotonic in potential. With S0/E0 at 0.020 mol reagent in 0.040 L, +1 V was productive, whereas -1 V and +2 V gave no resolved conversion and poor efficiencies (runner-operation-0007, -0014, -0021). +0.7 V remained productive but gave lower yield than +1 V in single long-run comparisons (runner-operation-0049 versus -0056). Consequently, a signed intermediate-positive potential window, rather than absolute voltage magnitude, is the primary potential law.

**H2 [supported qualitatively; parametric law unresolved].** At +1 V, productive conversion rises with duration/effective charge, but high current cap imposes a strong efficiency/selectivity penalty. Extending 100 mA from 600 to 6000 s raised conversion from ~0.021 to ~0.115 (runner-operation-0007 versus -0028). At 6000 s, 20 mA yielded only ~0.032 conversion but high efficiencies (runner-operation-0035), while 500 mA nearly eliminated selectivity and faradaic/transport performance (runner-operation-0042). The prospective moderate-current prediction succeeded: 40 mA for 14400 s reached ~0.147 conversion, ~0.136 yield, and ~0.92 faradaic/transport efficiency (runner-operation-0049). A useful predictive form should therefore combine a saturating effective-charge term with current-stress and signed-potential window factors; exact coefficients cannot be identified from this sparse grid.

**H3 [material dependence supported, attribution partly confounded].** Direct substitutions from S0/E0 showed S1/E0 preserved yield while shifting the efficiency balance (runner-operation-0063), and S0/E1 retained high conversion/selectivity with strong efficiencies and the best observed score (runner-operation-0070). The S2/E2 and S3/E3 combinations were worse (runner-operation-0077, -0084), but solvent and electrolyte contributions are confounded in those two comparisons and must not be assigned separately. Material identity also shifted pH-normalized and precipitation outputs substantially; precipitation fell from near 1 for E0 cases to ~0.85 for S0/E1 and near zero in the paired S2/E2 and S3/E3 cases.

**H4 [scope and uncertainty].** Conclusions apply to 0.020 mol/0.040 L initial loading. All designs are unreplicated and final-assay noise is declared; numerical differences should be treated as provisional where similar in magnitude to uncertainty. The intermediate UV-vis readings broadly corroborated large efficiency changes, but do not replace final assays. Segmentation, depletion saturation above ~0.15 conversion, and fully crossed solvent/electrolyte effects remain unresolved.

## Recommendation decision

Select Batch 10 (S0/E1, +1 V, 40 mA cap, 14400 s): it has the best observed balanced score and jointly strong conversion, selectivity, faradaic, transport, ohmic, and energy efficiencies. This is a tested operating point, not a claim of global optimality; a replicated local grid around potential +1 V and 20–60 mA would be the next study.

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
    "electrochemical_conversion": 0.02056857757270336,
    "electrochemical_selectivity": 0.9495708346366882,
    "energy_efficiency": 0.8010963797569275,
    "faradaic_efficiency": 0.8320691585540771,
    "ohmic_efficiency": 0.9695378541946411,
    "pH_normalized": 0.23218974471092224,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.8033654093742371
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
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.6255703568458557,
    "energy_efficiency": 0.24048729240894318,
    "faradaic_efficiency": 0.39272937178611755,
    "ohmic_efficiency": 0.9783756732940674,
    "pH_normalized": 0.2294943928718567,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.191747784614563,
    "selective_product_yield": 0.01273958571255207,
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
    "cost": 0.28308001160621643,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.0,
    "ohmic_efficiency": 0.9758104681968689,
    "pH_normalized": 0.23020939528942108,
    "precipitation_signal": 0.9868234395980835,
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
      "potential_V": 1
    },
    {
      "duration_s": 6000,
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
    "cost": 0.2849999964237213,
    "electrochemical_conversion": 0.11490065604448318,
    "electrochemical_selectivity": 0.9105417132377625,
    "energy_efficiency": 0.7129942774772644,
    "faradaic_efficiency": 0.7916689515113831,
    "ohmic_efficiency": 0.9773074388504028,
    "pH_normalized": 0.2295188158750534,
    "precipitation_signal": 0.987571656703949,
    "safety_risk": 0.072194404900074,
    "score": 0.5379016399383545,
    "selective_product_yield": 0.11226052790880203,
    "transport_efficiency": 0.7601814270019531
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
      "current_mA": 20,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 6000,
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
    "cost": 0.28308001160621643,
    "electrochemical_conversion": 0.03188921511173248,
    "electrochemical_selectivity": 0.9456571340560913,
    "energy_efficiency": 0.8735303282737732,
    "faradaic_efficiency": 0.925710916519165,
    "ohmic_efficiency": 0.9937994480133057,
    "pH_normalized": 0.2344796061515808,
    "precipitation_signal": 0.9868980646133423,
    "safety_risk": 0.072194404900074,
    "score": 0.5687295794487,
    "selective_product_yield": 0.03517703711986542,
    "transport_efficiency": 0.9152014851570129
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
      "current_mA": 500,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 6000,
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
    "cost": 0.2946000099182129,
    "electrochemical_conversion": 0.0021511756349354982,
    "electrochemical_selectivity": 0.0042426493018865585,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.02405594103038311,
    "ohmic_efficiency": 0.8933091163635254,
    "pH_normalized": 0.23120366036891937,
    "precipitation_signal": 0.9975283145904541,
    "safety_risk": 0.072194404900074,
    "score": 0.04047219082713127,
    "selective_product_yield": 0.010337181389331818,
    "transport_efficiency": 0.0
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
      "current_mA": 40,
      "electrolyte_profile": 0,
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
    "cost": 0.28490400314331055,
    "electrochemical_conversion": 0.1468660831451416,
    "electrochemical_selectivity": 0.9370536208152771,
    "energy_efficiency": 0.9014825820922852,
    "faradaic_efficiency": 0.9168441295623779,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.23021826148033142,
    "precipitation_signal": 0.982570469379425,
    "safety_risk": 0.072194404900074,
    "score": 0.6131651401519775,
    "selective_product_yield": 0.1355079710483551,
    "transport_efficiency": 0.9202445149421692
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
      "current_mA": 40,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 0.7
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
    "cost": 0.28421279788017273,
    "electrochemical_conversion": 0.12027331441640854,
    "electrochemical_selectivity": 0.8942734599113464,
    "energy_efficiency": 0.884231448173523,
    "faradaic_efficiency": 0.8475004434585571,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.22852078080177307,
    "precipitation_signal": 0.9954432845115662,
    "safety_risk": 0.072194404900074,
    "score": 0.5721737146377563,
    "selective_product_yield": 0.09190019220113754,
    "transport_efficiency": 0.8410050868988037
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
      "current_mA": 40,
      "electrolyte_profile": 0,
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
    "cost": 0.3009040057659149,
    "electrochemical_conversion": 0.12337445467710495,
    "electrochemical_selectivity": 0.9424866437911987,
    "energy_efficiency": 0.9724039435386658,
    "faradaic_efficiency": 0.830741822719574,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.2345096468925476,
    "precipitation_signal": 0.9987349510192871,
    "safety_risk": 0.09559440612792969,
    "score": 0.6053506135940552,
    "selective_product_yield": 0.13644425570964813,
    "transport_efficiency": 0.8515730500221252
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
      "current_mA": 40,
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
    "cost": 0.28490400314331055,
    "electrochemical_conversion": 0.15224593877792358,
    "electrochemical_selectivity": 0.9718971848487854,
    "energy_efficiency": 0.9581303000450134,
    "faradaic_efficiency": 0.9261475801467896,
    "ohmic_efficiency": 0.9793274402618408,
    "pH_normalized": 0.19775448739528656,
    "precipitation_signal": 0.8540157079696655,
    "safety_risk": 0.072194404900074,
    "score": 0.6253582239151001,
    "selective_product_yield": 0.12798626720905304,
    "transport_efficiency": 0.927497148513794
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
      "solvent": 2,
      "volume_L": 0.04
    },
    {
      "current_mA": 40,
      "electrolyte_profile": 2,
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
    "cost": 0.3265039920806885,
    "electrochemical_conversion": 0.11544418334960938,
    "electrochemical_selectivity": 0.7133615016937256,
    "energy_efficiency": 0.7191565632820129,
    "faradaic_efficiency": 0.6855887174606323,
    "ohmic_efficiency": 0.9808018803596497,
    "pH_normalized": 0.16693492233753204,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.1135944053530693,
    "score": 0.4790029525756836,
    "selective_product_yield": 0.07523058354854584,
    "transport_efficiency": 0.6927686333656311
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
      "solvent": 3,
      "volume_L": 0.04
    },
    {
      "current_mA": 40,
      "electrolyte_profile": 3,
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
    "cost": 0.3105039894580841,
    "electrochemical_conversion": 0.08805341273546219,
    "electrochemical_selectivity": 0.8498650789260864,
    "energy_efficiency": 0.8512985706329346,
    "faradaic_efficiency": 0.6658181548118591,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.28475531935691833,
    "precipitation_signal": 0.0,
    "safety_risk": 0.12619440257549286,
    "score": 0.5230754017829895,
    "selective_product_yield": 0.101643405854702,
    "transport_efficiency": 0.6870431303977966
  }
}
```

## K1 封存报告

Mechanistic report

1. Experimental scope and evidence base

All 12 batches used the same initial loading: 0.020 mol of limiting reagent in 0.040 L of solvent, corresponding to a nominal initial concentration of 0.50 mol L^-1 before analytical sampling. Consequently, the campaign identifies effects of potential, current cap, electrolysis time, solvent label, and electrolyte label only at this loading. It does not identify concentration or volume laws.

The most defensible account is a competing-process model: productive conversion requires an intermediate positive potential and accumulated effective charge, while excessive current or excessive potential activates a strong loss pathway. Solvent and electrolyte alter charge transport, selectivity, and phase/equilibrium behavior. Because the materials are anonymous benchmark labels, none of these effects should be assigned to real chemical identities.

2. Potential dependence: a signed electrochemical window

The potential response is strongly asymmetric and non-monotonic. Batch 1, using S0/E0 at +1.0 V, a 100 mA cap, and 600 s, gave electrochemical conversion 0.0206, selectivity 0.9496, faradaic efficiency 0.8321, transport efficiency 0.8034, and energy efficiency 0.8011. Changing only the sign in Batch 2 (-1.0 V, 100 mA, 600 s) produced no resolved conversion and much poorer faradaic, transport, and energy efficiencies: 0.3927, 0.4190, and 0.2405. Raising the potential to +2.0 V in Batch 3, again at 100 mA and 600 s, produced no resolved conversion, selectivity, faradaic efficiency, transport efficiency, or energy efficiency, although ohmic efficiency remained high at 0.9758.

Thus neither absolute voltage magnitude nor a monotonic increase with positive potential explains the data. I infer a productive potential window centered approximately near +1 V in the tested S0/E0 system. Negative polarity does not drive the same productive pathway, and +2 V strongly favors an unproductive process, passivation, or an explicit high-overpotential loss channel.

A direct long-run comparison further supports the window. Batch 7 at +1.0 V, 40 mA, and 14,400 s gave conversion 0.1469, selectivity 0.9371, and selective-product yield 0.1355. Batch 8 differed only in potential, using +0.7 V, and gave conversion 0.1203, selectivity 0.8943, and yield 0.0919. Its faradaic and transport efficiencies, 0.8475 and 0.8410, were also below Batch 7 values of 0.9168 and 0.9202. These differences are appreciably larger than the declared final-assay standard uncertainties for most corresponding channels, although they come from single batches.

A useful phenomenological term is therefore a signed window W(V), with W(+1 V) high, W(+0.7 V) moderately lower, and W(-1 V) and W(+2 V) near zero. The available points do not determine whether W is Gaussian, Butler-Volmer-like with a competing high-overpotential reaction, or a piecewise benchmark response.

3. Time, charge, and current stress

At a productive potential, conversion depends on accumulated electrolysis exposure. Batch 4 repeated the Batch 1 S0/E0, +1 V, 100 mA condition but increased time from 600 to 6,000 s. Conversion rose from 0.0206 to 0.1149 and selective-product yield rose from a clipped/noisy value of 0 to 0.1123. Selectivity remained high but decreased from 0.9496 to 0.9105. Faradaic and transport efficiencies also decreased from 0.8321 and 0.8034 to 0.7917 and 0.7602. This supports productive charge accumulation accompanied by a smaller time- or conversion-dependent penalty.

The current-cap experiments show that current is not merely a linear rate multiplier. At +1 V and 6,000 s:

• Batch 5, 20 mA: conversion 0.0319, yield 0.0352, selectivity 0.9457, faradaic efficiency 0.9257, transport efficiency 0.9152, and energy efficiency 0.8735.
• Batch 4, 100 mA: conversion 0.1149, yield 0.1123, selectivity 0.9105, faradaic efficiency 0.7917, transport efficiency 0.7602, and energy efficiency 0.7130.
• Batch 6, 500 mA: conversion 0.0022, selectivity 0.0042, yield 0.0103, faradaic efficiency 0.0241, transport efficiency 0, and energy efficiency 0.

From 20 to 100 mA, a higher cap increases conversion but reduces efficiencies. At 500 mA, the productive process collapses despite the much larger nominal current-time product. Ohmic efficiency changes less dramatically—0.9938, 0.9773, and 0.8933 in Batches 5, 4, and 6—so the high-current failure cannot be described as purely ohmic loss. It more plausibly represents a parallel reaction, passivation, transport exhaustion, degradation, or an empirical current-stress penalty.

The current-time products provide a compact comparison. Batches 1, 5, 4, and 7 have nominal cap-time products of 60,000, 120,000, 600,000, and 576,000 mA·s and conversions of 0.0206, 0.0319, 0.1149, and 0.1469. This is broadly consistent with conversion increasing with effective charge at non-destructive currents. Batch 6 has a nominal product of 3,000,000 mA·s but essentially no conversion, decisively demonstrating failure of a simple charge-only law.

Before Batch 7, I predicted that 40 mA for 14,400 s would approach the conversion obtained at 100 mA for 6,000 s while retaining the superior efficiencies associated with moderate current. The result supported that prediction: Batch 7 reached conversion 0.1469, yield 0.1355, faradaic efficiency 0.9168, transport efficiency 0.9202, energy efficiency 0.9015, and ohmic efficiency 1.000. It exceeded Batch 4 in conversion, yield, and every efficiency channel while using a similar nominal cap-time product. This suggests that distributing charge over longer time at moderate current avoids the high-current loss pathway.

4. A possible mathematical representation

One phenomenological model consistent with the observations is:

q_eff = t · I_eff(I_cap, V, material)

X = X_max · [1 - exp(-k_material · W(V) · q_eff)] · D(I_cap, V, t, material)

S = S0_material · W_S(V) · D_S(I_cap, V, t, material)

Y = X · S · R_material + measurement/process residual

Here X is conversion, S is electrochemical selectivity, and Y is selective-product yield. W(V) is the signed productive-potential window. D and D_S are loss factors close to one at moderate current but falling steeply above a material-dependent stress threshold. For example, one could use

D = exp[-a_material · t · max(0, I_cap - I_crit)^p]

or a smoother logistic penalty. I_eff need not equal the current cap; it could be the minimum of the cap and a potential-, resistance-, or transport-limited current. The efficiencies can be represented as related but nonidentical products:

eta_F = F_material(V) · C_F(I_cap, t)
eta_T = T_material · C_T(I_cap, t)
eta_ohm = O_material(I_cap)
eta_E ≈ eta_F · eta_T · eta_ohm · G(V, material),

with independent residuals because the measured energy efficiency is not exactly the product of the other channels.

This is a structural model, not a fitted law. The campaign does not contain enough independent points to estimate X_max, k, I_crit, the exponent p, or the shape and center of W. It does, however, identify their qualitative roles.

5. Solvent and electrolyte effects

Batch 7 provides the S0/E0 reference at +1 V, 40 mA, and 14,400 s. Batch 9 changed only the solvent to S1 while retaining E0. Batch 9 gave conversion 0.1234, selectivity 0.9425, yield 0.1364, energy efficiency 0.9724, faradaic efficiency 0.8307, transport efficiency 0.8516, and ohmic efficiency 1.000. Relative to Batch 7, the selective yields 0.1364 and 0.1355 are indistinguishable at the scale of the declared yield uncertainty of 0.01. S1 therefore preserved product yield but numerically shifted the efficiency balance: higher energy efficiency but lower faradaic and transport efficiencies. Since there is no replicate, the precise solvent effect remains provisional.

Batch 10 changed only the electrolyte from E0 to E1 while retaining S0 and the Batch 7 electrical program. It gave conversion 0.1522, selectivity 0.9719, yield 0.1280, energy efficiency 0.9581, faradaic efficiency 0.9261, transport efficiency 0.9275, and ohmic efficiency 0.9793. Compared with Batch 7, E1 preserved or improved most conversion/selectivity/efficiency measures, although the measured yield was slightly lower. Batch 10 had the highest observed balanced score, 0.6254, versus 0.6132 for Batch 7, and was therefore the sealed operating recommendation. The recommendation is a tested compromise, not evidence of a global optimum.

Batches 11 and 12 tested paired material changes rather than isolated factors. Batch 11 used S2/E2 and produced conversion 0.1154, selectivity 0.7134, yield 0.0752, faradaic efficiency 0.6856, transport efficiency 0.6928, and energy efficiency 0.7192. Batch 12 used S3/E3 and produced conversion 0.0881, selectivity 0.8499, yield 0.1016, faradaic efficiency 0.6658, transport efficiency 0.6870, and energy efficiency 0.8513. Both combinations were inferior to S0/E0 or S0/E1 under the same electrical program, but solvent and electrolyte contributions are inseparable in these two batches. It would be unjustified to claim independently that S2, E2, S3, or E3 caused a particular loss.

6. pH-normalized and precipitation channels

The final pH-normalized and precipitation signals appear much more sensitive to material identity than to the amount of productive conversion. Across the early E0 cases, precipitation remained close to saturation even when electrochemical behavior changed drastically. For example, Batches 1, 3, 4, 6, 7, 8, and 9 all had precipitation signals around 0.98–1.00 despite outcomes ranging from no resolved conversion to conversion 0.147 and from nearly zero to high faradaic efficiency. This makes precipitation an unlikely direct proxy for product formation at this loading.

Material changes shifted these observables substantially. The S0/E0 reference Batch 7 had pH-normalized 0.2302 and precipitation 0.9826. S0/E1 in Batch 10 gave 0.1978 and 0.8540. S2/E2 in Batch 11 gave 0.1669 and 0.0052, while S3/E3 in Batch 12 gave 0.2848 and 0. These results suggest a material-dependent acid/base or phase-equilibrium subsystem coupled to, but not uniquely determining, electrochemical productivity. An alternative is that precipitation is a direct categorical property of the anonymous medium combinations. The campaign cannot discriminate those interpretations.

7. Relationship among conversion, selectivity, and selective yield

Selective-product yield often roughly tracked conversion times selectivity in the productive long runs, but it was not an exact algebraic identity. For example, Batch 7 had conversion 0.1469, selectivity 0.9371, and yield 0.1355, which are mutually consistent. Batch 1, however, had conversion 0.0206 and selectivity 0.9496 but reported yield 0. This should not be interpreted as proof that converted reactant formed no target. The final-assay yield uncertainty is 0.01, values are clipped to the allowed interval, and low-level channel processing can produce such discrepancies. Likewise, Batch 2 reported no resolved conversion but yield 0.0127. Therefore, I treat the three observables as noisy correlated channels generated from a latent product balance rather than imposing an exact identity on their processed estimates.

8. How the explanation changed during the campaign

The initial working idea was that conversion would increase with potential magnitude and charge until selectivity declined. Batches 2 and 3 rejected the magnitude-only component: reversing polarity was harmful, and +2 V was substantially worse than +1 V. The model was revised to include a signed potential window.

Batch 4 established a strong duration effect at +1 V. Batches 5 and 6 then showed that current produces a rate-efficiency tradeoff and, at 500 mA, a near-total collapse. This changed the explanation from a simple effective-charge law to a charge law multiplied by a nonlinear current-stress term.

Batch 7 prospectively tested that revised account. Its combination of 40 mA and long duration delivered both higher conversion and better efficiencies than the similar-charge 100 mA case, strengthening the interpretation that moderate current avoids an adverse pathway. Batch 8 narrowed the favorable voltage region by showing +0.7 V to be productive but inferior to +1 V. Batches 9–12 then demonstrated material dependence, with the clean comparisons S1 versus S0 and E1 versus E0 being most informative and the paired S2/E2 and S3/E3 results remaining confounded.

9. Unidentified quantities and plausible alternative mechanisms

Several mechanistic quantities are not publicly observable: actual current versus the configured cap, electrode overpotential, charge passed, electron stoichiometry, electrode area, mass-transfer coefficients, identities or concentrations of intermediates and byproducts, and the real meaning of the anonymous material labels. Consequently, the data cannot distinguish among several plausible explanations:

• High-current collapse could arise from a parallel electrochemical reaction, electrode passivation, transport depletion, degradation, or a benchmark-level penalty.
• The potential window could reflect activation of the target reaction near +1 V followed by a competing reaction at +2 V, or it could arise from potential-dependent actual current and transport.
• The long-time advantage at 40 mA could represent reduced side reaction, reduced passivation, better transport matching, or simply a more favorable effective-current regime.
• Material effects could be kinetic, conductive, solvation-related, acid/base-related, or phase-related. Batches 11 and 12 cannot separate solvent-electrolyte interactions from main effects.
• The efficiency channels are correlated outputs and should not be treated as fully independent mechanistic measurements.

All batches were unreplicated. Declared final-assay standard uncertainties were approximately 0.010 for conversion and yield, 0.012 for selectivity and faradaic/ohmic efficiency, 0.014 for transport efficiency, 0.016 for energy efficiency, 0.002 for pH-normalized, and 0.006 for precipitation. Large contrasts—such as Batch 6 versus Batch 7 or Batch 3 versus Batch 1—are robust relative to these scales. Small differences, such as the Batch 7 versus Batch 9 yields, are not persuasive evidence of an effect.

10. Overall account and limits of extrapolation

Within the sampled 0.50 mol L^-1 loading, this world behaves as though target formation requires an intermediate positive potential and an adequate effective charge dose. Moderate current applied for longer time is preferable to forcing nominal charge through at high current. Excessive current and excessive positive potential activate a severe unproductive pathway that suppresses conversion, selectivity, and faradaic/transport/energy efficiency, while leaving ohmic efficiency comparatively less affected. Solvent and electrolyte tune transport, selectivity, energy efficiency, and a separate pH/precipitation subsystem.

The best tested compromise was Batch 10: S0/E1, +1 V, 40 mA, and 14,400 s. Extrapolation beyond the tested loading, beyond 14,400 s, or to unsampled solvent-electrolyte crosses is not justified. The most informative next study, if experimentation were available, would be replicated local sampling around +1 V and 20–60 mA, combined with a fully crossed solvent/electrolyte design and direct observation of actual charge. Those experiments would distinguish a saturating effective-charge model from passivation, degradation, and transport-limited alternatives.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific mechanistic prior was supplied. The task specified anonymous solvents and electrolytes, observable channels, and scoring rules, but supplied no claim about the reaction law or optimal conditions.

Supported self-developed claims:

• A signed, intermediate-positive potential window is supported. Under otherwise identical short-run S0/E0 conditions, Batch 1 at +1.0 V gave conversion 0.0206, selectivity 0.9496, and faradaic efficiency 0.8321. Batch 2 at −1.0 V gave no resolved conversion and faradaic efficiency 0.3927, while Batch 3 at +2.0 V gave no resolved conversion and essentially zero faradaic, transport, and energy efficiency. Batch 8 at +0.7 V remained productive but was inferior to Batch 7 at +1.0 V under the same 40 mA, 14,400 s program: yields were 0.0919 and 0.1355, respectively.

• Productive exposure accumulates with electrolysis time at moderate current. Extending +1 V, 100 mA electrolysis from 600 s in Batch 1 to 6,000 s in Batch 4 raised conversion from 0.0206 to 0.1149 and yield from a clipped/noisy zero to 0.1123.

• Current produces a rate–efficiency tradeoff and a severe high-current penalty. At +1 V for 6,000 s, Batch 5 at 20 mA had conversion 0.0319 but faradaic efficiency 0.9257; Batch 4 at 100 mA had conversion 0.1149 and faradaic efficiency 0.7917; Batch 6 at 500 mA collapsed to conversion 0.0022, selectivity 0.0042, and faradaic efficiency 0.0241. Thus nominal charge alone is insufficient.

• The prospective moderate-current prediction was supported. Before Batch 7, the stated prediction was that 40 mA for 14,400 s would approach or exceed the conversion of the 100 mA, 6,000 s case while retaining better efficiencies. Batch 7 gave conversion 0.1469, yield 0.1355, and faradaic/transport efficiencies of 0.9168/0.9202, all favorable relative to Batch 4.

• Material identity matters. Batch 9 directly changed S0 to S1 at fixed E0 and electrical conditions; it preserved yield but shifted the efficiency profile. Batch 10 directly changed E0 to E1 at fixed S0 and gave conversion 0.1522, selectivity 0.9719, and the highest observed score, 0.6254.

Contradicted or weakened claims:

• The initial idea that performance might rise with potential magnitude was contradicted by Batch 3: +2 V was much worse than +1 V. Batch 2 also contradicted any law based only on absolute potential magnitude because −1 V did not resemble +1 V.

• A simple linear charge law was contradicted by Batch 6. Its nominal current–time product was five times that of Batch 4, yet its productive response nearly vanished.

• Precipitation as a direct product proxy was contradicted. Batches 3 and 6 had precipitation near 0.99–1.00 despite negligible productive performance, while productive Batch 7 also had precipitation 0.9826. The channel appears predominantly material- or phase-dependent at this loading.

Untested or unresolved claims:

• No concentration, volume, or reagent-inventory law was tested because every campaign batch used 0.020 mol in 0.040 L.

• The actual-current law is unidentifiable because only current caps, not charge passed, were observed.

• Conversion saturation, electron stoichiometry, electrode passivation, degradation, and mass-transfer coefficients were not separately measured.

• Independent effects of S2, E2, S3, and E3 remain untested. Batches 11 and 12 changed solvent and electrolyte together, so their inferior performance cannot be assigned to either factor.

• Solvent–electrolyte interactions, segmented electrolysis, and repeatability were not tested. All final conditions were unreplicated.

The largest changes in judgment came from Batches 2–3, which forced replacement of a magnitude-based potential idea with a signed window; Batch 6, which forced addition of a nonlinear current-loss term; and Batch 7, which supported the resulting moderate-current/long-time account.

2. One additional discriminating experiment

I would run S0/E0 at the established loading, +1.0 V, 50 mA, and 12,000 s. Its nominal current–time product would be 600,000 mA·s, exactly matching Batch 4 at 100 mA for 6,000 s and close to Batch 7 at 40 mA for 14,400 s.

The leading explanation predicts conversion and yield near or above Batch 4 but with faradaic and transport efficiencies closer to Batch 7. Roughly, conversion around 0.13–0.15 together with efficiencies near 0.88–0.92 would support a productive effective-charge term multiplied by an instantaneous current-stress penalty.

Different outcomes would change the judgment as follows:

• If conversion matched Batch 4 and efficiencies also remained near Batch 4, a mostly cumulative-charge explanation would gain support and the inferred current-stress advantage of Batch 7 would weaken.

• If performance approached Batch 7, the current-stress account would be strengthened because comparable nominal charge delivered at lower current would again outperform 100 mA.

• If conversion were substantially higher merely because elapsed time was longer, a time-dependent chemical or transport process—not charge alone—would need greater weight.

• If conversion or efficiencies deteriorated despite moderate current, long-time passivation, depletion, or degradation would become more plausible.

One unreplicated experiment could not fully identify these mechanisms, but this matched-charge interpolation would target the main ambiguity more directly than another broad material screen.

3. Unused evidence, weak predictions, and influence of the goal

The raw characterization artifacts and full spectra were not inspected or quantitatively modeled. Only the supplied processed estimates and brief peak summaries were used. The intermediate UV–visible measurements were used as qualitative corroboration of major efficiency changes, but their spectra were not fitted and they were not incorporated into a kinetic model. Cost and safety data were also largely unused because safety risk stayed low and nearly constant for the chosen loading, while cost was not the primary research objective. The pH-normalized and precipitation channels were interpreted qualitatively but were not used to predict yield or choose the final condition.

The least reliable blind predictions are Q03, Q05, Q07, and Q09: they combine long negative-polarity electrolysis with material or duration extrapolation unsupported by direct campaign analogues. Q07 and Q08 are especially uncertain because E3 was never isolated from S3. Q09 and Q10 are similarly uncertain because S2 was never isolated from E2. The exact near-zero values and yield-gated scores predicted for Q11 and Q12 are also unreliable, although the qualitative expectation of a 500 mA collapse is comparatively well supported by Batch 6. All blind questions use a smaller absolute inventory than the campaign, so predictions involving fractional conversion depend on an untested inventory-scaling assumption.

The sealed recommendation, Batch 10, is reliable only as the best observed balanced condition. It is not a demonstrated global optimum. Its score of 0.6254 was only modestly above Batch 7 at 0.6132, both were unreplicated, and Batch 10 did not have the highest measured yield. Exact superiority is therefore less secure than the broader recommendation for an intermediate positive potential and moderate current.

The assigned explanatory goal materially affected evidence collection. It motivated deliberately poor but diagnostic conditions—negative polarity, +2 V, and 500 mA—and a broad material screen rather than repeatedly optimizing the public score. This produced stronger evidence about polarity and current stress but left little capacity for replication, a local response surface, or a fully crossed solvent–electrolyte design. There was no clear conflict with the operating recommendation: the explanatory campaign still found a strong condition. However, a score-first campaign would probably have spent more batches replicating and refining Batches 7 and 10, whereas the actual campaign prioritized mechanism discrimination.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.68,
        "lower80": 0.45,
        "upper80": 0.82
      },
      "energy_efficiency": {
        "estimate": 0.33,
        "lower80": 0.15,
        "upper80": 0.5
      },
      "faradaic_efficiency": {
        "estimate": 0.46,
        "lower80": 0.3,
        "upper80": 0.62
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.2,
        "lower80": 0.05,
        "upper80": 0.39
      },
      "selective_product_yield": {
        "estimate": 0.012,
        "lower80": 0,
        "upper80": 0.035
      },
      "transport_efficiency": {
        "estimate": 0.48,
        "lower80": 0.3,
        "upper80": 0.65
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.92,
        "lower80": 0.84,
        "upper80": 0.97
      },
      "energy_efficiency": {
        "estimate": 0.79,
        "lower80": 0.69,
        "upper80": 0.87
      },
      "faradaic_efficiency": {
        "estimate": 0.78,
        "lower80": 0.68,
        "upper80": 0.86
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.51,
        "lower80": 0.27,
        "upper80": 0.61
      },
      "selective_product_yield": {
        "estimate": 0.028,
        "lower80": 0.005,
        "upper80": 0.052
      },
      "transport_efficiency": {
        "estimate": 0.74,
        "lower80": 0.62,
        "upper80": 0.83
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.3,
        "upper80": 0.74
      },
      "energy_efficiency": {
        "estimate": 0.2,
        "lower80": 0.05,
        "upper80": 0.4
      },
      "faradaic_efficiency": {
        "estimate": 0.3,
        "lower80": 0.13,
        "upper80": 0.49
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.12,
        "lower80": 0.02,
        "upper80": 0.3
      },
      "selective_product_yield": {
        "estimate": 0.009,
        "lower80": 0,
        "upper80": 0.03
      },
      "transport_efficiency": {
        "estimate": 0.34,
        "lower80": 0.15,
        "upper80": 0.53
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.87,
        "lower80": 0.81,
        "upper80": 0.92
      },
      "energy_efficiency": {
        "estimate": 0.7,
        "lower80": 0.6,
        "upper80": 0.79
      },
      "faradaic_efficiency": {
        "estimate": 0.73,
        "lower80": 0.64,
        "upper80": 0.81
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.534,
        "lower80": 0.46,
        "upper80": 0.6
      },
      "selective_product_yield": {
        "estimate": 0.155,
        "lower80": 0.1,
        "upper80": 0.21
      },
      "transport_efficiency": {
        "estimate": 0.69,
        "lower80": 0.58,
        "upper80": 0.78
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.32,
        "upper80": 0.79
      },
      "energy_efficiency": {
        "estimate": 0.28,
        "lower80": 0.08,
        "upper80": 0.5
      },
      "faradaic_efficiency": {
        "estimate": 0.35,
        "lower80": 0.16,
        "upper80": 0.56
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.162,
        "lower80": 0.025,
        "upper80": 0.35
      },
      "selective_product_yield": {
        "estimate": 0.011,
        "lower80": 0,
        "upper80": 0.034
      },
      "transport_efficiency": {
        "estimate": 0.39,
        "lower80": 0.18,
        "upper80": 0.6
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.91,
        "lower80": 0.85,
        "upper80": 0.96
      },
      "energy_efficiency": {
        "estimate": 0.79,
        "lower80": 0.69,
        "upper80": 0.88
      },
      "faradaic_efficiency": {
        "estimate": 0.75,
        "lower80": 0.65,
        "upper80": 0.84
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.557,
        "lower80": 0.48,
        "upper80": 0.62
      },
      "selective_product_yield": {
        "estimate": 0.147,
        "lower80": 0.09,
        "upper80": 0.205
      },
      "transport_efficiency": {
        "estimate": 0.72,
        "lower80": 0.61,
        "upper80": 0.81
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.45,
        "lower80": 0.17,
        "upper80": 0.69
      },
      "energy_efficiency": {
        "estimate": 0.18,
        "lower80": 0.02,
        "upper80": 0.4
      },
      "faradaic_efficiency": {
        "estimate": 0.22,
        "lower80": 0.05,
        "upper80": 0.44
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.08,
        "lower80": 0.01,
        "upper80": 0.27
      },
      "selective_product_yield": {
        "estimate": 0.007,
        "lower80": 0,
        "upper80": 0.029
      },
      "transport_efficiency": {
        "estimate": 0.25,
        "lower80": 0.06,
        "upper80": 0.48
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.79,
        "lower80": 0.65,
        "upper80": 0.89
      },
      "energy_efficiency": {
        "estimate": 0.72,
        "lower80": 0.56,
        "upper80": 0.84
      },
      "faradaic_efficiency": {
        "estimate": 0.58,
        "lower80": 0.41,
        "upper80": 0.72
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.479,
        "lower80": 0.37,
        "upper80": 0.57
      },
      "selective_product_yield": {
        "estimate": 0.115,
        "lower80": 0.058,
        "upper80": 0.18
      },
      "transport_efficiency": {
        "estimate": 0.58,
        "lower80": 0.4,
        "upper80": 0.73
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.47,
        "lower80": 0.19,
        "upper80": 0.7
      },
      "energy_efficiency": {
        "estimate": 0.18,
        "lower80": 0.02,
        "upper80": 0.39
      },
      "faradaic_efficiency": {
        "estimate": 0.25,
        "lower80": 0.07,
        "upper80": 0.47
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.082,
        "lower80": 0.01,
        "upper80": 0.28
      },
      "selective_product_yield": {
        "estimate": 0.007,
        "lower80": 0,
        "upper80": 0.03
      },
      "transport_efficiency": {
        "estimate": 0.28,
        "lower80": 0.08,
        "upper80": 0.5
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.76,
        "lower80": 0.62,
        "upper80": 0.86
      },
      "energy_efficiency": {
        "estimate": 0.66,
        "lower80": 0.5,
        "upper80": 0.79
      },
      "faradaic_efficiency": {
        "estimate": 0.65,
        "lower80": 0.49,
        "upper80": 0.77
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.484,
        "lower80": 0.37,
        "upper80": 0.57
      },
      "selective_product_yield": {
        "estimate": 0.12,
        "lower80": 0.063,
        "upper80": 0.182
      },
      "transport_efficiency": {
        "estimate": 0.64,
        "lower80": 0.46,
        "upper80": 0.77
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.08,
        "lower80": 0,
        "upper80": 0.25
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0,
        "upper80": 0.08
      },
      "faradaic_efficiency": {
        "estimate": 0.015,
        "lower80": 0,
        "upper80": 0.1
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.017,
        "lower80": 0,
        "upper80": 0.07
      },
      "selective_product_yield": {
        "estimate": 0.004,
        "lower80": 0,
        "upper80": 0.018
      },
      "transport_efficiency": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.09
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.04,
        "lower80": 0,
        "upper80": 0.18
      },
      "energy_efficiency": {
        "estimate": 0.015,
        "lower80": 0,
        "upper80": 0.1
      },
      "faradaic_efficiency": {
        "estimate": 0.035,
        "lower80": 0,
        "upper80": 0.13
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.039,
        "lower80": 0.005,
        "upper80": 0.09
      },
      "selective_product_yield": {
        "estimate": 0.009,
        "lower80": 0,
        "upper80": 0.025
      },
      "transport_efficiency": {
        "estimate": 0.02,
        "lower80": 0,
        "upper80": 0.11
      }
    }
  ],
  "rationale": "Predictions use the observed signed potential window near +1 V, approximate charge/time scaling at moderate current, and the severe efficiency/selectivity collapse seen at 500 mA. The new 0.48 M loading is close to the studied 0.50 M loading, but its smaller reagent inventory may raise fractional conversion at fixed charge. E1 is projected to preserve the favorable positive-polarity response; E3 and S2 receive wider, generally adverse adjustments because their campaign evidence was partly confounded. Intervals combine declared assay noise with larger uncertainty for polarity, material, loading, and current extrapolations; near-zero yield also creates large score uncertainty through the score's yield gate."
}
```
