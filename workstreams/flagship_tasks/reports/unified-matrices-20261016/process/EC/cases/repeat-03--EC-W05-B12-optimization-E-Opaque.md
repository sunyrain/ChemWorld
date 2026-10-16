# repeat-03/EC-W05-B12-optimization-E-Opaque

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-03\EC-W05-B12-optimization-E-Opaque\participant\optimization-E-Opaque

## 同期笔记

### v1 · 公开事件 0

# Electrochemical campaign hypotheses

## H1 [tentative]
At fixed loading, the balanced score should show an interior optimum in potential, duration, and current cap: insufficient charge limits conversion, while excessive potential/time raises degradation and lowers selectivity and energy efficiency. Electrolyte and solvent identities may strongly shift transport/ohmic terms.

**Planned test:** begin with a broad screen across potential sign, solvent, electrolyte, duration, and current cap, then refine around the highest public final-assay score. A materially better result at the search boundary will trigger expansion toward that boundary; a strong material interaction will take priority over a single global optimum.

## H2 [tentative]
A moderate reagent concentration is expected to balance productive conversion against transport loss. Initial batches will hold loading constant where possible so electrochemical factors are interpretable; concentration will be varied only after a promising material/field region appears.

### v2 · 公开事件 42

# Electrochemical campaign hypotheses

## H1 [supported in a limited scope]
Productive behavior occurs under the tested negative-potential regime at 0.25 M nominal loading, whereas the initial 0.50 M, +1.2 V condition gave zero yield and complete precipitation (final assay event runner-operation-0007). The sign effect is not isolated because loading also changed, so polarity itself remains unresolved.

At solvent-S0, electrolyte-E0, -1.5 V, 100 mA cap, 3600 s, the 0.25 M batch gave the current best score 0.2686 with yield 0.0262 and selectivity 0.577 (runner-operation-0014). This supports refining charge delivery and loading around that recipe rather than broad material switching.

## H2 [material effects likely but incompletely mapped]
At matched electrolysis settings/loading, changing paired solvent/electrolyte identities changed score substantially: S1/E1 was gated to zero (runner-operation-0021), S2/E2 scored 0.1078 (runner-operation-0028), and S3/E3 scored 0.1554 (runner-operation-0035). These comparisons confound solvent and electrolyte. Holding S0 while changing E0 to E1 slightly lowered the score from 0.2686 to 0.2524 (runner-operation-0042), so E0 remains preferred but the numerical difference is not yet a repeated effect.

## Next tests
Keep S0/E0 and 0.25 M fixed while varying potential, current cap, and duration. If improved conversion is accompanied by a yield above the 0.02 gate without a large efficiency collapse, refine there. A lower-loading test will check whether precipitation reduction offsets lower throughput.

### v3 · 公开事件 84

# Electrochemical campaign hypotheses

## H1 [supported for the tested S0/E0, 0.25 M scope]
The balanced score has a tradeoff between productive charge and efficiency. At -1.3 V and a 100 mA cap, extending electrolysis from 7200 to 10800 to 14400 s raised the observed score from 0.3026 to 0.3085 to 0.3146 (events runner-operation-0063, -0070, -0077). The corresponding conversion rose, and the 14400 s batch gave the highest observed selective-product yield within this series (0.0806). These are independent batches but unreplicated conditions, so the monotonic duration effect is supported only in this local tested range.

Moving from -1.3 to -1.4 V at 14400 s increased observed yield to 0.0849 but reduced efficiency terms and score to 0.2932 (runner-operation-0084). Thus the best balanced setting among completed batches is the -1.3 V condition rather than the highest-yield condition.

## H2 [material/loading dependence; partially resolved]
The initial 0.50 M S0/E0 batch at +1.2 V was fully precipitation-limited and gated to zero score (runner-operation-0007), while 0.25 M S0/E0 at -1.5 V produced a score of 0.2686 (runner-operation-0014). Loading and polarity are confounded, so no isolated sign law is claimed. Broad paired material changes were generally inferior (runner-operation-0021, -0028, -0035), and switching only E0 to E1 under the matched S0 recipe gave 0.2524 (runner-operation-0042), numerically below E0.

## Operating decision
Recommend completed batch 11: 0.020 mol limiting reagent in 0.080 L solvent-S0, electrolyte-E0, potential -1.3 V, current cap 100 mA, electrolysis 14400 s. It had the highest public balanced-efficiency-v2 score (0.3146) among the 12 final assays. Batch 12 is an alternative when maximizing yield rather than the balanced score. A future study would replicate batches 10-12 and refine potential between -1.25 and -1.35 V and duration near/above 14400 s; evidence of a downturn or excessive degradation would bound the optimum.

## 实际批次及公开测量

### 批次 1 · 终点事件 7

```json
{
  "ordinal": 1,
  "lifecycle_index": 1,
  "end_step": 7,
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
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1.2
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
    "cost": 0.35392799973487854,
    "electrochemical_conversion": 0.008014115504920483,
    "electrochemical_selectivity": 0.01034972071647644,
    "energy_efficiency": 0.005256945732980967,
    "faradaic_efficiency": 0.02452157624065876,
    "ohmic_efficiency": 0.9653199911117554,
    "pH_normalized": 0.23308512568473816,
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
      "volume_L": 0.08
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.5
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
    "cost": 0.2943600118160248,
    "electrochemical_conversion": 0.022379744797945023,
    "electrochemical_selectivity": 0.5772162079811096,
    "energy_efficiency": 0.12831933796405792,
    "faradaic_efficiency": 0.3260131776332855,
    "ohmic_efficiency": 0.9792658090591431,
    "pH_normalized": 0.2303897738456726,
    "precipitation_signal": 1.0,
    "safety_risk": 0.0464978851377964,
    "score": 0.2686290144920349,
    "selective_product_yield": 0.02623618394136429,
    "transport_efficiency": 0.3522700071334839
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
      "volume_L": 0.08
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -1.5
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
    "cost": 0.32635998725891113,
    "electrochemical_conversion": 0.01565592549741268,
    "electrochemical_selectivity": 0.404956191778183,
    "energy_efficiency": 0.08608990907669067,
    "faradaic_efficiency": 0.19971494376659393,
    "ohmic_efficiency": 0.9449852108955383,
    "pH_normalized": 0.20443867146968842,
    "precipitation_signal": 0.7141679525375366,
    "safety_risk": 0.06989788264036179,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.21627184748649597
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
      "volume_L": 0.08
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -1.5
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
    "cost": 0.37755998969078064,
    "electrochemical_conversion": 0.01841692253947258,
    "electrochemical_selectivity": 0.40229332447052,
    "energy_efficiency": 0.0784284695982933,
    "faradaic_efficiency": 0.26625245809555054,
    "ohmic_efficiency": 0.9463211894035339,
    "pH_normalized": 0.17094862461090088,
    "precipitation_signal": 0.0,
    "safety_risk": 0.0878978818655014,
    "score": 0.10781706124544144,
    "selective_product_yield": 0.010357578285038471,
    "transport_efficiency": 0.2347649186849594
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
      "volume_L": 0.08
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": -1.5
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
    "cost": 0.3455600142478943,
    "electrochemical_conversion": 0.02051893062889576,
    "electrochemical_selectivity": 0.42376741766929626,
    "energy_efficiency": 0.06194078549742699,
    "faradaic_efficiency": 0.19402359426021576,
    "ohmic_efficiency": 0.9763364195823669,
    "pH_normalized": 0.2890998125076294,
    "precipitation_signal": 0.0,
    "safety_risk": 0.10049788653850555,
    "score": 0.15536688268184662,
    "selective_product_yield": 0.015589220449328423,
    "transport_efficiency": 0.18351413309574127
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
      "volume_L": 0.08
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -1.5
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
    "cost": 0.2943600118160248,
    "electrochemical_conversion": 0.02880636416375637,
    "electrochemical_selectivity": 0.5319238305091858,
    "energy_efficiency": 0.1274031102657318,
    "faradaic_efficiency": 0.30981534719467163,
    "ohmic_efficiency": 0.9704110026359558,
    "pH_normalized": 0.20372962951660156,
    "precipitation_signal": 0.8528557419776917,
    "safety_risk": 0.0464978851377964,
    "score": 0.2524243891239166,
    "selective_product_yield": 0.024402622133493423,
    "transport_efficiency": 0.2851320207118988
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
      "volume_L": 0.08
    },
    {
      "current_mA": 200,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.5
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
    "cost": 0.2965199947357178,
    "electrochemical_conversion": 0.056118372827768326,
    "electrochemical_selectivity": 0.5689502358436584,
    "energy_efficiency": 0.10728307068347931,
    "faradaic_efficiency": 0.24747221171855927,
    "ohmic_efficiency": 0.9906179308891296,
    "pH_normalized": 0.23111364245414734,
    "precipitation_signal": 0.9826673865318298,
    "safety_risk": 0.0464978851377964,
    "score": 0.2511090338230133,
    "selective_product_yield": 0.03342949599027634,
    "transport_efficiency": 0.25087258219718933
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
      "volume_L": 0.08
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
    "cost": 0.29363998770713806,
    "electrochemical_conversion": 0.033090002834796906,
    "electrochemical_selectivity": 0.629239022731781,
    "energy_efficiency": 0.29306289553642273,
    "faradaic_efficiency": 0.416513055562973,
    "ohmic_efficiency": 0.9861299991607666,
    "pH_normalized": 0.229416161775589,
    "precipitation_signal": 0.995540201663971,
    "safety_risk": 0.0464978851377964,
    "score": 0.0524708591401577,
    "selective_product_yield": 0.0033577552530914545,
    "transport_efficiency": 0.4100176990032196
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
      "volume_L": 0.08
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.3
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
    "cost": 0.2959440052509308,
    "electrochemical_conversion": 0.06467676907777786,
    "electrochemical_selectivity": 0.5841414928436279,
    "energy_efficiency": 0.21844728291034698,
    "faradaic_efficiency": 0.3482257127761841,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.23142993450164795,
    "precipitation_signal": 1.0,
    "safety_risk": 0.0464978851377964,
    "score": 0.30256685614585876,
    "selective_product_yield": 0.05672689899802208,
    "transport_efficiency": 0.36905696988105774
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
      "volume_L": 0.08
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.3
    },
    {
      "duration_s": 10800,
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
    "cost": 0.2978160083293915,
    "electrochemical_conversion": 0.11523743718862534,
    "electrochemical_selectivity": 0.6123336553573608,
    "energy_efficiency": 0.20162475109100342,
    "faradaic_efficiency": 0.3659074306488037,
    "ohmic_efficiency": 0.965594470500946,
    "pH_normalized": 0.2291157990694046,
    "precipitation_signal": 0.9925763010978699,
    "safety_risk": 0.0464978851377964,
    "score": 0.30854371190071106,
    "selective_product_yield": 0.05681352689862251,
    "transport_efficiency": 0.3672570288181305
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
      "volume_L": 0.08
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.3
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
    "cost": 0.2996880114078522,
    "electrochemical_conversion": 0.14660878479480743,
    "electrochemical_selectivity": 0.5846961736679077,
    "energy_efficiency": 0.19994297623634338,
    "faradaic_efficiency": 0.35908395051956177,
    "ohmic_efficiency": 0.9790727496147156,
    "pH_normalized": 0.2301008403301239,
    "precipitation_signal": 1.0,
    "safety_risk": 0.0464978851377964,
    "score": 0.3145783543586731,
    "selective_product_yield": 0.08059769868850708,
    "transport_efficiency": 0.36626386642456055
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
      "volume_L": 0.08
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.4
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
    "cost": 0.30026400089263916,
    "electrochemical_conversion": 0.11088933050632477,
    "electrochemical_selectivity": 0.562774121761322,
    "energy_efficiency": 0.15374140441417694,
    "faradaic_efficiency": 0.3070635497570038,
    "ohmic_efficiency": 0.9941052198410034,
    "pH_normalized": 0.23062115907669067,
    "precipitation_signal": 0.9938013553619385,
    "safety_risk": 0.0464978851377964,
    "score": 0.29324132204055786,
    "selective_product_yield": 0.08490056544542313,
    "transport_efficiency": 0.3282884955406189
  }
}
```

## K1 封存报告

## Scope and evidential basis

This report describes the bounded synthetic electrochemical world explored in 12 completed batches. Solvent-S0…S3 and electrolyte-E0…E3 are anonymous benchmark labels, so any proposed molecular interpretation is unidentifiable. All comparisons are between single batches without replication; observed differences therefore combine process effects and declared assay noise. Final-assay standard deviations were approximately 0.010 for conversion and selective-product yield, 0.012 for selectivity and faradaic/ohmic efficiency, 0.014 for transport efficiency, and 0.016 for energy efficiency.

## Observed operating map

The most informative batches were:

- **Batch 1:** 0.040 mol reagent, 0.080 L S0, E0, +1.2 V, 100 mA, 3600 s. Score 0; yield 0; conversion 0.0080; selectivity 0.0103; precipitation signal 1.0.
- **Batch 2:** 0.020 mol, 0.080 L S0, E0, −1.5 V, 100 mA, 3600 s. Score 0.2686; yield 0.0262; conversion 0.0224; selectivity 0.5772; faradaic/transport/ohmic/energy efficiencies 0.3260/0.3523/0.9793/0.1283.
- **Batches 3–5:** the same loading and electrolysis settings as batch 2 but paired S1/E1, S2/E2, and S3/E3. Scores were respectively 0, 0.1078, and 0.1554. Their yields were 0, 0.0104, and 0.0156, showing a strong medium/formulation dependence, although solvent and electrolyte were changed together and cannot be separated in these batches.
- **Batch 6:** S0/E1 under the batch-2 electrical recipe. Score 0.2524, yield 0.0244, conversion 0.0288, selectivity 0.5319. This isolated one electrolyte change and was numerically inferior to S0/E0, especially in transport efficiency (0.2851 versus 0.3523), although the difference was not replicated.
- **Batch 7:** S0/E0, −1.5 V, 200 mA, 3600 s. Conversion and yield increased to 0.0561 and 0.0334, but faradaic, transport, and energy efficiencies fell to 0.2475, 0.2509, and 0.1073. The resulting score, 0.2511, was slightly below batch 2.
- **Batch 8:** S0/E0, −1.0 V, 100 mA, 3600 s. Efficiency indicators were excellent—faradaic 0.4165, transport 0.4100, ohmic 0.9861, energy 0.2931—and selectivity was 0.6292. Nevertheless, selective-product yield was only 0.00336, so the score was only 0.0525.
- **Batches 9–11:** S0/E0, −1.3 V, 100 mA, with durations 7200, 10800, and 14400 s. Scores increased from 0.3026 to 0.3085 to 0.3146. Conversion increased from 0.0647 to 0.1152 to 0.1466; yields were 0.0567, 0.0568, and 0.0806. Energy efficiency declined modestly from 0.2184 to 0.2016 to 0.1999, while faradaic and transport efficiencies remained near 0.35–0.37. Batch 11 was the highest-scoring experiment.
- **Batch 12:** S0/E0, −1.4 V, 100 mA, 14400 s. Yield rose to 0.0849, the campaign maximum, but conversion was 0.1109, selectivity 0.5628, faradaic efficiency 0.3071, transport efficiency 0.3283, and energy efficiency 0.1537. Score fell to 0.2932.

## Proposed process model

I interpret the world as having at least four coupled stages:

1. **Electrical activation and pathway selection.** Applied potential controls whether charge reaches a productive reduction/oxidation channel rather than merely determining total conversion. Batch 8 is crucial: at −1.0 V it had high apparent electrochemical efficiencies and selectivity but almost no isolated productive yield. This suggests a potential-dependent activation or pathway threshold between approximately −1.0 and −1.3 V. Once the productive channel is accessible, increasing potential magnitude further raises energetic losses or competing chemistry.

2. **Charge delivery and conversion.** A useful first approximation is an effective charge variable

   `Q_eff = I_eff(V, medium, concentration) × t`,

   followed by a saturating conversion law such as

   `X = X_max × [1 − exp(−k(V, medium, concentration) Q_eff)]`.

   Here the configured current is a cap, not necessarily the actual current. The batch-9–11 duration series supports increasing conversion with time at fixed settings. Doubling the current cap in batch 7 also increased conversion relative to batch 2, but did not preserve efficiency, indicating that `I_eff` and efficiency are coupled rather than independent.

3. **Product branching and loss.** Productive yield appears to depend on conversion, potential-dependent branching, and a survival/recovery factor:

   `Y_product ≈ f(X, selectivity, medium) × survival(V, Q_eff, concentration)`.

   I would not impose `Y = X × selectivity` exactly: the reported quantities do not consistently obey that identity, so they may be separately calibrated observables or include different process factors. The lower selectivity and efficiency at −1.4 V relative to −1.3 V are consistent with increased side reactions, overpotential loss, or product degradation. This interpretation is plausible rather than directly identified because degradation species were not observed in the reported final-assay fields.

4. **Transport, resistance, and medium effects.** Solvent/electrolyte identity changes charge transport, current utilization, and possibly product stabilization. Ohmic efficiency remained high in nearly every productive batch (roughly 0.94–1.00), so ohmic loss was not the dominant limitation in the explored region. Transport and faradaic efficiencies varied much more and tracked changes in balanced performance. The S0/E0 combination was the strongest tested formulation; E1 in S0 was close but somewhat worse, while the paired S1/E1, S2/E2, and S3/E3 experiments were substantially poorer.

## Concentration, precipitation, pH, and safety

The initial 0.50 M nominal batch was inactive, while the later 0.25 M nominal S0/E0 batches were productive. This is compatible with concentration-dependent precipitation, aggregation, or transport inhibition. However, polarity and concentration changed together between batches 1 and 2, so concentration cannot be isolated from potential sign using those batches.

The precipitation signal was not a simple veto. It was 1.0 in batch 2 and approximately 0.99–1.0 in many successful S0/E0 batches, whereas batches 4 and 5 had zero precipitation signal but lower scores. Thus it may report a phase-equilibrium feature of S0 rather than directly measuring loss of all active reagent. It could still reduce the soluble active fraction, but that effect is unidentifiable from these data.

For productive S0/E0 batches, normalized pH stayed near 0.23 and did not systematically follow score. No deliberate pH intervention was performed, so acid/base causality cannot be inferred. Safety risk was stable at about 0.0465 for the 0.020 mol S0 batches and did not change with potential, current, or duration in the tested range. Higher risks appeared for other paired media—approximately 0.0699 for S1/E1, 0.0879 for S2/E2, and 0.1005 for S3/E3—but all remained well below the 0.65 limit.

## Relationship between chemistry and the published score

The score is not simply yield. Before gating, the published balanced-efficiency objective is the weighted sum

`W = 0.30Y + 0.15S + 0.10X + 0.15EE + 0.12FE + 0.10TE + 0.08OE`,

where `Y` is selective-product yield, `S` selectivity, `X` conversion, and EE/FE/TE/OE are energy, faradaic, transport, and ohmic efficiencies. The observations are consistent with an additional yield gate approximately

`score ≈ W × min(1, Y/0.02)`.

This explains why batch 8, despite excellent efficiency terms, scored poorly, and why batches 4 and 5 were strongly penalized. Above a yield of about 0.02, efficiency and selectivity tradeoffs dominate. Consequently, the score optimum need not coincide with maximum yield: batch 12 had the highest yield but batch 11 had the best balance.

## How the explanation changed

The zero result from batch 1 initially suggested severe precipitation or an incorrect electrochemical regime. Batch 2 established that the system could be productive after changing to lower loading and negative potential. Batches 3–6 then showed that anonymous medium and electrolyte identities materially affect performance, with S0/E0 preferred.

Batches 7 and 8 changed the explanation from “more electrical drive is better” to a tradeoff model. Higher current increased conversion but reduced utilization efficiencies; weaker potential preserved efficiency but failed to generate enough target product. Batches 9–11 demonstrated that, near −1.3 V, longer processing can increase conversion and balanced score without the large efficiency collapse seen from more aggressive current or potential. Batch 12 then supplied evidence for the high-potential side of an optimum: a slightly more negative potential improved yield but harmed several efficiency/selectivity terms enough to reduce the score.

## Scope, unresolved parameters, and alternatives

The supported scope is narrow: S0/E0, approximately 0.25 M nominal reagent loading, negative potentials from −1.0 to −1.5 V, current caps of 100–200 mA, and durations of 3600–14400 s. The data do not identify molecular species, electrode kinetics, electrode area, actual current trajectories, charge passed, conductivity, temperature dependence, mass-transfer coefficients, product degradation rates, or whether precipitation removes reactant, product, electrolyte, or an unrelated proxy.

Plausible alternatives include: (a) the apparent potential optimum could reflect instrument-calibrated synthetic pathway switching rather than physical overpotential chemistry; (b) the duration trend could partly reflect batch noise because no condition was replicated; (c) the S0 advantage could be a solvent effect, an interaction with E0, or both; and (d) batch 1 could have failed mainly because positive polarity selected the wrong reaction, not because concentration was high.

Within the observed campaign, the most defensible operating interpretation is therefore an interior balanced optimum near **S0/E0, 0.020 mol in 0.080 L, −1.3 V, 100 mA cap, and 14400 s**. Extrapolation beyond 14400 s is uncertain: the observed duration trend had not yet turned downward, but conversion saturation and cumulative side reactions make indefinite improvement unlikely. Likewise, potentials between roughly −1.25 and −1.35 V may improve the balance, but that is a conjecture requiring new evidence rather than an observed result.

## K2 封存报告

1. **Claims and laws assessed.** No instance-specific scientific prior or material-property dossier was supplied; only anonymous material labels, instrument contracts, and the published scoring rule were available.

The supplied balanced-score law was supported by the final-assay results: the weighted component sum, together with the 0.02 selective-yield gate, explains why batch 8 scored only 0.0525 despite strong efficiency terms, and why batch 11 outscored the higher-yield batch 12. The supplied measurement-noise levels were used to limit confidence, but the campaign had no replicates with which to validate those noise models empirically.

My initial claim that potential, charge delivery, and duration would have an interior balanced optimum was partly supported. At fixed S0/E0 loading, increasing duration at −1.3 V from 7200 to 10800 to 14400 s increased score from 0.3026 to 0.3085 to 0.3146 in batches 9–11. Increasing the potential magnitude to −1.4 V in batch 12 raised yield but reduced the score to 0.2932, supporting a potential-dependent efficiency tradeoff. A duration optimum was not located, however, because batch 11 was at the maximum tested duration and the score was still rising.

The claim that more electrical drive is not always better was supported. Doubling the current cap from 100 mA in batch 2 to 200 mA in batch 7 raised conversion and yield but reduced faradaic, transport, and energy efficiencies, with score falling from 0.2686 to 0.2511. Batch 8 materially changed my judgment: at −1.0 V it showed high selectivity and efficiency but very low yield, indicating that efficient charge handling alone did not ensure target formation.

Strong material dependence was supported by batches 2–6, although most comparisons were confounded. At matched loading and electrical settings, paired S1/E1, S2/E2, and S3/E3 in batches 3–5 were inferior to S0/E0 in batch 2. Batch 6 isolated E1 within S0 and was numerically worse than E0, especially in transport efficiency, but there was no replicate to establish a precise electrolyte effect.

My proposed moderate-concentration advantage was only partially supported and remains confounded. Batch 1 at nominal 0.50 M and +1.2 V was inactive, whereas batch 2 at 0.25 M and −1.5 V was productive; concentration and polarity changed simultaneously. Likewise, the claim that negative polarity is intrinsically required was not directly tested at matched concentration, potential magnitude, and duration. The conjectures of product degradation, precipitation-controlled soluble fraction, and saturating conversion kinetics were not directly measured. Precipitation as a simple performance veto was contradicted: successful batches 2 and 9–12 had precipitation signals near one, while lower-scoring batches 4 and 5 had signals near zero.

2. **Most informative additional experiment.** I would run 0.020 mol reagent in 0.080 L S0 with E0, +1.3 V, a 100 mA cap, and 14400 s—identical to batch 11 except for potential sign. This directly distinguishes my leading polarity/pathway-selection explanation from the alternative that batch 1 failed mainly because of high concentration and that potential magnitude, rather than sign, governs the process.

If the positive-polarity batch were near batch 11 in yield, selectivity, and score, I would reject a polarity-specific productive pathway and attribute much more of batch 1's failure to concentration or another setup interaction. If it remained near zero despite the lower loading and long duration, I would strongly favor polarity-specific pathway selection. An intermediate result—some yield but markedly lower selectivity or efficiency—would suggest both signs can react but access different product branches. Because this would still be a single batch, a difference comparable to assay noise would leave the issue unresolved rather than proving equivalence.

3. **Unused evidence, reliability, and goal effects.** I did not inspect or model the complete raw spectral artifacts, peak shapes, or intermediate UV–visible traces beyond their processed efficiency estimates. I also made little use of cost, mass-balance detail, sample loss, and exact pH variation because they showed no clear relationship to the objective within the observed batches. The campaign did not map solvent and electrolyte independently, did not test lower concentrations systematically, did not replicate any condition, and did not isolate polarity. Consequently, possible material interactions, precipitation mechanisms, and stochastic batch variation remain poorly identified.

The blind predictions are least reliable for Q11 and Q12 because 500 mA is far outside the tested 100–200 mA range; Q12 additionally combines high current with an unvalidated positive-polarity regime. All positive-polarity predictions are weak because only batch 1 used positive potential and it was concentration-confounded. Q07–Q10 are also weak because E3 and S2 were not independently paired with the requested counterparts. All predictions extrapolate to 0.48 M and ±0.8 V, a region not directly tested. The point predictions therefore depend heavily on the unverified polarity and concentration explanations.

Batch 11 is the strongest recommendation for the observed balanced-score objective, but its absolute reliability is limited: it was unreplicated, the duration optimum was not bounded, and nearby potential was sampled only sparsely. Batch 12 would be more defensible only if yield, rather than the specified balanced score, were the goal.

The assigned goal did affect evidence collection. Maximizing score encouraged broad early screening followed by exploitation around S0/E0 and −1.3 V. That strategy found a better operating point, but it displaced mechanistically cleaner experiments such as matched polarity controls, independent solvent/electrolyte factorials, concentration series, and replicates. The single intermediate-measurement allowance was used for UV–visible measurements, but the final decisions relied mainly on final assays. There was no clear conflict with safety—the observed risks stayed far below the limit—but optimization pressure did create a conflict between locating a high score and identifying causal laws.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.32,
        "lower80": 0.05,
        "upper80": 0.62
      },
      "energy_efficiency": {
        "estimate": 0.25,
        "lower80": 0.1,
        "upper80": 0.42
      },
      "faradaic_efficiency": {
        "estimate": 0.35,
        "lower80": 0.17,
        "upper80": 0.52
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.008,
        "lower80": 0,
        "upper80": 0.045
      },
      "selective_product_yield": {
        "estimate": 0.0006,
        "lower80": 0,
        "upper80": 0.009
      },
      "transport_efficiency": {
        "estimate": 0.31,
        "lower80": 0.13,
        "upper80": 0.49
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.02,
        "lower80": 0,
        "upper80": 0.12
      },
      "energy_efficiency": {
        "estimate": 0.008,
        "lower80": 0,
        "upper80": 0.045
      },
      "faradaic_efficiency": {
        "estimate": 0.025,
        "lower80": 0,
        "upper80": 0.09
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.008
      },
      "selective_product_yield": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.006
      },
      "transport_efficiency": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.06
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.5,
        "lower80": 0.25,
        "upper80": 0.7
      },
      "energy_efficiency": {
        "estimate": 0.23,
        "lower80": 0.1,
        "upper80": 0.38
      },
      "faradaic_efficiency": {
        "estimate": 0.34,
        "lower80": 0.18,
        "upper80": 0.5
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.055,
        "lower80": 0.005,
        "upper80": 0.16
      },
      "selective_product_yield": {
        "estimate": 0.004,
        "lower80": 0,
        "upper80": 0.016
      },
      "transport_efficiency": {
        "estimate": 0.33,
        "lower80": 0.16,
        "upper80": 0.49
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.025,
        "lower80": 0,
        "upper80": 0.14
      },
      "energy_efficiency": {
        "estimate": 0.007,
        "lower80": 0,
        "upper80": 0.05
      },
      "faradaic_efficiency": {
        "estimate": 0.025,
        "lower80": 0,
        "upper80": 0.1
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.001,
        "lower80": 0,
        "upper80": 0.015
      },
      "selective_product_yield": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.007
      },
      "transport_efficiency": {
        "estimate": 0.008,
        "lower80": 0,
        "upper80": 0.07
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.46,
        "lower80": 0.2,
        "upper80": 0.68
      },
      "energy_efficiency": {
        "estimate": 0.2,
        "lower80": 0.07,
        "upper80": 0.35
      },
      "faradaic_efficiency": {
        "estimate": 0.29,
        "lower80": 0.13,
        "upper80": 0.46
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.041,
        "lower80": 0.002,
        "upper80": 0.14
      },
      "selective_product_yield": {
        "estimate": 0.0035,
        "lower80": 0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.25,
        "lower80": 0.09,
        "upper80": 0.43
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.02,
        "lower80": 0,
        "upper80": 0.13
      },
      "energy_efficiency": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.045
      },
      "faradaic_efficiency": {
        "estimate": 0.02,
        "lower80": 0,
        "upper80": 0.09
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.001,
        "lower80": 0,
        "upper80": 0.014
      },
      "selective_product_yield": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.007
      },
      "transport_efficiency": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.065
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.43,
        "lower80": 0.17,
        "upper80": 0.66
      },
      "energy_efficiency": {
        "estimate": 0.17,
        "lower80": 0.05,
        "upper80": 0.32
      },
      "faradaic_efficiency": {
        "estimate": 0.25,
        "lower80": 0.09,
        "upper80": 0.43
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.032,
        "lower80": 0.001,
        "upper80": 0.125
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0,
        "upper80": 0.014
      },
      "transport_efficiency": {
        "estimate": 0.22,
        "lower80": 0.06,
        "upper80": 0.4
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.018,
        "lower80": 0,
        "upper80": 0.13
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0,
        "upper80": 0.045
      },
      "faradaic_efficiency": {
        "estimate": 0.02,
        "lower80": 0,
        "upper80": 0.09
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.001,
        "lower80": 0,
        "upper80": 0.014
      },
      "selective_product_yield": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.007
      },
      "transport_efficiency": {
        "estimate": 0.005,
        "lower80": 0,
        "upper80": 0.065
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.4,
        "lower80": 0.14,
        "upper80": 0.64
      },
      "energy_efficiency": {
        "estimate": 0.15,
        "lower80": 0.035,
        "upper80": 0.3
      },
      "faradaic_efficiency": {
        "estimate": 0.24,
        "lower80": 0.08,
        "upper80": 0.42
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.024,
        "lower80": 0,
        "upper80": 0.11
      },
      "selective_product_yield": {
        "estimate": 0.0025,
        "lower80": 0,
        "upper80": 0.014
      },
      "transport_efficiency": {
        "estimate": 0.2,
        "lower80": 0.045,
        "upper80": 0.39
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.018,
        "lower80": 0,
        "upper80": 0.13
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0,
        "upper80": 0.045
      },
      "faradaic_efficiency": {
        "estimate": 0.02,
        "lower80": 0,
        "upper80": 0.09
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.001,
        "lower80": 0,
        "upper80": 0.014
      },
      "selective_product_yield": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.007
      },
      "transport_efficiency": {
        "estimate": 0.005,
        "lower80": 0,
        "upper80": 0.065
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.5,
        "lower80": 0.25,
        "upper80": 0.7
      },
      "energy_efficiency": {
        "estimate": 0.09,
        "lower80": 0.025,
        "upper80": 0.2
      },
      "faradaic_efficiency": {
        "estimate": 0.18,
        "lower80": 0.07,
        "upper80": 0.34
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.22,
        "lower80": 0.07,
        "upper80": 0.35
      },
      "selective_product_yield": {
        "estimate": 0.022,
        "lower80": 0.007,
        "upper80": 0.05
      },
      "transport_efficiency": {
        "estimate": 0.16,
        "lower80": 0.045,
        "upper80": 0.32
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.05,
        "lower80": 0,
        "upper80": 0.2
      },
      "energy_efficiency": {
        "estimate": 0.015,
        "lower80": 0,
        "upper80": 0.07
      },
      "faradaic_efficiency": {
        "estimate": 0.04,
        "lower80": 0,
        "upper80": 0.14
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.002,
        "lower80": 0,
        "upper80": 0.03
      },
      "selective_product_yield": {
        "estimate": 0.0004,
        "lower80": 0,
        "upper80": 0.009
      },
      "transport_efficiency": {
        "estimate": 0.02,
        "lower80": 0,
        "upper80": 0.1
      }
    }
  ],
  "rationale": "All queries use a high nominal loading (0.48 M), close to the campaign's inactive 0.50 M batch and well above the productive 0.25 M region, while ±0.8 V lies outside the well-supported productive potential range near −1.3 V. I therefore predict mostly sub-gate yields. Negative polarity is favored based on the campaign's productive negative-potential batches; positive-polarity estimates remain near the assay floor. Longer duration should help negative-polarity conversion, whereas E1, E3, and S2 are discounted from the observed material screen. The 500 mA negative case may overcome some kinetic limitation but sacrifices energy, faradaic, and transport efficiency. Intervals are deliberately broad because concentration, polarity, electrolyte, solvent, and current are being extrapolated without replicated controls."
}
```
