# repeat-02/EC-W01-B12-optimization-E-Aligned

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-02\EC-W01-B12-optimization-E-Aligned\participant\optimization-E-Aligned

## 同期笔记

### v1 · 公开事件 0

# Electrochemical campaign hypotheses

## H1 [tentative]
At fixed loading, balanced score should peak at an intermediate overpotential and electrolysis duration: insufficient drive limits conversion, while excessive drive/time reduces selectivity and energy efficiency. Testable consequence: a coarse potential–time sweep will show a non-monotone score.

## H2 [tentative]
Higher conductivity is expected to improve ohmic efficiency, but transport and selectivity may favor a different solvent/electrolyte pair; nominal properties are priors only. I will first compare materials under common loading and then refine the best region. Evidence can overturn the nominal ranking.

## Design decision
Use 0.04 mol reagent in 0.08 L (0.5 mol/L) for every batch to make comparisons and later predictions interpretable. Spend one UV–vis intermediate measurement per batch after electrolysis, then explicitly terminate and run final assay. Initial coarse screen will vary solvent, electrolyte, potential, current cap, and duration; later batches will refine or replicate promising conditions.

### v2 · 公开事件 35

# Electrochemical campaign hypotheses

## H1 [supported in sampled scope]
The productive polarity is negative. At +1.0 V for 1200 s with S0/E0, conversion was only ~0.017 and selective yield was reported as zero (runner-operation-0007). At -1.0 V, negative-potential batches produced nonzero selective yield (runner-operation-0014 and later). This is not yet a symmetric sign comparison because duration/current differed; nevertheless positive +1 V is deprioritized.

## H2 [supported for the tested matched pairs]
At -1.0 V, 500 mA cap, 7200 s, S1/E1 gave the highest score among matched-index pairs: ~0.321 versus S0/E0 ~0.240, S2/E2 ~0.272, S3/E3 ~0.205 (runner-operation-0014, -0021, -0028, -0035). S1/E1 combines the best observed conversion and transport without the very low efficiencies of S0/E0/S3/E3. The comparison does not separate solvent from electrolyte effects; cross-pairs remain unresolved.

## H3 [tentative]
For S1/E1 the optimum should be at a less negative potential and/or shorter duration than the initial -1.0 V, 7200 s condition because its selectivity (~0.585), faradaic efficiency (~0.334), and transport efficiency (~0.350) leave substantial room despite useful conversion (~0.163). Next test: potential and duration refinement around this pair. A markedly higher score at stronger drive would overturn the direction of refinement.

### v3 · 公开事件 84

# Electrochemical campaign hypotheses

## H1 [supported in tested scope]
Negative potential is the productive polarity. The sole positive-potential test (+1.0 V, S0/E0, 1200 s) had conversion ~0.017 and zero reported selective yield (runner-operation-0007), whereas all negative-potential screens gave nonzero yield. The sign comparison is confounded by time/current and therefore does not establish a universal polarity law.

## H2 [supported, with interaction]
Material effects are interactive. Among matched-index pairs at -1.0 V, 500 mA cap, 7200 s, S1/E1 led the score (~0.321; runner-operation-0021). Subsequent cross-pair S0/E1 at -0.45 V and 14400 s reached the campaign-best ~0.505 (runner-operation-0070), exceeding S1/E1 at the same potential/time (~0.456; runner-operation-0063). Thus E1 is favored by current evidence, while S0 improves the balance relative to S1 under the refined condition. S0/E0 was much worse even at -0.45 V (runner-operation-0077), opposing a solvent-only explanation.

## H3 [supported locally; optimum unresolved]
For S1/E1, moving from -1.0 V/7200 s (score ~0.321, runner-operation-0021) to -0.6 V/7200 s (~0.385, runner-operation-0042), then lengthening to 14400 s (~0.433, runner-operation-0056), and using -0.45 V/14400 s (~0.456, runner-operation-0063) improved the observed balance. At -0.3 V/7200 s the score fell to ~0.369 (runner-operation-0049), consistent with an intermediate potential optimum rather than monotonic improvement. However duration and potential were not crossed completely, and final-assay noise means fine distinctions are unresolved.

## Final operating decision
Recommend completed batch 10: 0.04 mol reagent, 0.08 L S0, E1, -0.45 V, 500 mA cap, 14400 s. It had the highest observed score (~0.505; runner-operation-0070), with conversion ~0.484, selectivity ~0.724, selective yield ~0.328, and stronger efficiency balance than nearby alternatives. Batch 12 at -0.55 V was lower (~0.483; runner-operation-0084), supporting but not precisely locating a local optimum near -0.45 V. Precipitation remained high (~0.854), an unresolved limitation and possible optimization target.

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
      "current_mA": 200,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 1200,
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
    "cost": 0.35251230001449585,
    "electrochemical_conversion": 0.01726597733795643,
    "electrochemical_selectivity": 0.9495708346366882,
    "energy_efficiency": 0.9066821336746216,
    "faradaic_efficiency": 0.9392082691192627,
    "ohmic_efficiency": 0.9769874215126038,
    "pH_normalized": 0.23218974471092224,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.9105045199394226
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1
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
    "cost": 0.36660000681877136,
    "electrochemical_conversion": 0.06495750695466995,
    "electrochemical_selectivity": 0.637496829032898,
    "energy_efficiency": 0.08978945016860962,
    "faradaic_efficiency": 0.15637436509132385,
    "ohmic_efficiency": 0.8930863738059998,
    "pH_normalized": 0.2294943928718567,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.2404996156692505,
    "selective_product_yield": 0.05478658154606819,
    "transport_efficiency": 0.18263117969036102
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -1
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
    "cost": 0.3986000120639801,
    "electrochemical_conversion": 0.1629536747932434,
    "electrochemical_selectivity": 0.58479243516922,
    "energy_efficiency": 0.3317759037017822,
    "faradaic_efficiency": 0.33363693952560425,
    "ohmic_efficiency": 0.8122000694274902,
    "pH_normalized": 0.20363308489322662,
    "precipitation_signal": 0.7135193943977356,
    "safety_risk": 0.09559440612792969,
    "score": 0.3207954466342926,
    "selective_product_yield": 0.08994339406490326,
    "transport_efficiency": 0.3501938283443451
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -1
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
    "cost": 0.4498000144958496,
    "electrochemical_conversion": 0.1413106620311737,
    "electrochemical_selectivity": 0.4584375023841858,
    "energy_efficiency": 0.2514221966266632,
    "faradaic_efficiency": 0.33934885263442993,
    "ohmic_efficiency": 0.7255498766899109,
    "pH_normalized": 0.16724827885627747,
    "precipitation_signal": 0.0,
    "safety_risk": 0.1135944053530693,
    "score": 0.2716023027896881,
    "selective_product_yield": 0.07146763056516647,
    "transport_efficiency": 0.3078612983226776
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 3,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": -1
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
    "cost": 0.41780000925064087,
    "electrochemical_conversion": 0.048851966857910156,
    "electrochemical_selectivity": 0.5716292262077332,
    "energy_efficiency": 0.06823349744081497,
    "faradaic_efficiency": 0.1083734855055809,
    "ohmic_efficiency": 0.892223596572876,
    "pH_normalized": 0.2895091474056244,
    "precipitation_signal": 0.0,
    "safety_risk": 0.12619440257549286,
    "score": 0.20527176558971405,
    "selective_product_yield": 0.03412684425711632,
    "transport_efficiency": 0.09786401689052582
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -0.6
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
    "cost": 0.3928399980068207,
    "electrochemical_conversion": 0.203890860080719,
    "electrochemical_selectivity": 0.6586341857910156,
    "energy_efficiency": 0.45902711153030396,
    "faradaic_efficiency": 0.45660972595214844,
    "ohmic_efficiency": 0.7094680666923523,
    "pH_normalized": 0.20462734997272491,
    "precipitation_signal": 0.7242242693901062,
    "safety_risk": 0.09559440612792969,
    "score": 0.38548770546913147,
    "selective_product_yield": 0.14235392212867737,
    "transport_efficiency": 0.4319263994693756
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -0.3
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
    "cost": 0.3885200023651123,
    "electrochemical_conversion": 0.24125170707702637,
    "electrochemical_selectivity": 0.6979203224182129,
    "energy_efficiency": 0.29346054792404175,
    "faradaic_efficiency": 0.4972311556339264,
    "ohmic_efficiency": 0.450577050447464,
    "pH_normalized": 0.20364195108413696,
    "precipitation_signal": 0.7092664241790771,
    "safety_risk": 0.09559440612792969,
    "score": 0.3692917823791504,
    "selective_product_yield": 0.1689414381980896,
    "transport_efficiency": 0.5006315112113953
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.08
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
    "cost": 0.4014799892902374,
    "electrochemical_conversion": 0.3984687328338623,
    "electrochemical_selectivity": 0.6489005088806152,
    "energy_efficiency": 0.4597517251968384,
    "faradaic_efficiency": 0.4406052231788635,
    "ohmic_efficiency": 0.7263256311416626,
    "pH_normalized": 0.2019444704055786,
    "precipitation_signal": 0.7221392393112183,
    "safety_risk": 0.09559440612792969,
    "score": 0.4334966540336609,
    "selective_product_yield": 0.24320760369300842,
    "transport_efficiency": 0.4341098964214325
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -0.45
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
    "cost": 0.39715999364852905,
    "electrochemical_conversion": 0.429752916097641,
    "electrochemical_selectivity": 0.667695939540863,
    "energy_efficiency": 0.446196973323822,
    "faradaic_efficiency": 0.4541054368019104,
    "ohmic_efficiency": 0.6424490213394165,
    "pH_normalized": 0.20395824313163757,
    "precipitation_signal": 0.7300134301185608,
    "safety_risk": 0.09559440612792969,
    "score": 0.4562593996524811,
    "selective_product_yield": 0.30939310789108276,
    "transport_efficiency": 0.47493669390678406
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -0.45
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
    "cost": 0.3651599884033203,
    "electrochemical_conversion": 0.4841303825378418,
    "electrochemical_selectivity": 0.7243803143501282,
    "energy_efficiency": 0.5271472930908203,
    "faradaic_efficiency": 0.5115669369697571,
    "ohmic_efficiency": 0.715765655040741,
    "pH_normalized": 0.19775448739528656,
    "precipitation_signal": 0.8540157079696655,
    "safety_risk": 0.072194404900074,
    "score": 0.5045433044433594,
    "selective_product_yield": 0.32820063829421997,
    "transport_efficiency": 0.5129165053367615
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -0.45
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
    "cost": 0.3651599884033203,
    "electrochemical_conversion": 0.15412643551826477,
    "electrochemical_selectivity": 0.7015290260314941,
    "energy_efficiency": 0.26268184185028076,
    "faradaic_efficiency": 0.15301565825939178,
    "ohmic_efficiency": 0.7657336592674255,
    "pH_normalized": 0.22920545935630798,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.2861323952674866,
    "selective_product_yield": 0.10149329155683517,
    "transport_efficiency": 0.16019560396671295
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -0.55
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
    "cost": 0.3680399954319,
    "electrochemical_conversion": 0.43172571063041687,
    "electrochemical_selectivity": 0.6723278760910034,
    "energy_efficiency": 0.5268324613571167,
    "faradaic_efficiency": 0.44631364941596985,
    "ohmic_efficiency": 0.7923023700714111,
    "pH_normalized": 0.19925984740257263,
    "precipitation_signal": 0.8552408218383789,
    "safety_risk": 0.072194404900074,
    "score": 0.482776015996933,
    "selective_product_yield": 0.32011234760284424,
    "transport_efficiency": 0.46753859519958496
  }
}
```

## K1 封存报告

Mechanistic account

The system appears to be a potential-window-limited electrochemical conversion of a 0.04 mol limiting reagent in 0.08 L solvent (nominal initial concentration 0.50 mol/L). All 12 batches used that loading, so the campaign identifies responses only at this concentration and volume. A selected solvent and electrolyte determine the effective redox window, ionic resistance, interfacial kinetics, mass transport, acidity, and precipitation tendency. Applied potential, current limit, and electrolysis time then determine charge delivery and product formation. The final score is the stated weighted sum of conversion, selectivity, selective yield, faradaic efficiency, transport efficiency, ohmic efficiency, and energy efficiency, subject to the selective-yield gate. For example, inserting batch 10's final-assay components into the published weights reproduces its score of about 0.5045. Batch 1 had reported selective yield 0 and therefore scored 0 despite high values for several efficiency channels.

A useful conceptual model is

E_eff = E_applied - E_eq(solvent,electrolyte) - iR(solvent,electrolyte,state),

i(t) = min(i_limit, i_kinetic(E_eff), i_transport(state)),

dn_target/dt ≈ FE(E_eff,materials,state) × i(t)/(zF) × S(E_eff,materials,state),

with competing reaction, degradation, or passivation rates increasing outside a favorable potential window. Conversion should depend on the time integral of productive current, while selective yield is approximately conversion times selectivity, modified by product loss, precipitation, degradation, and assay noise. The observed yield is broadly, but not exactly, consistent with such a product: batch 10 had conversion 0.4841 and selectivity 0.7244, whose product is roughly 0.351, versus measured selective yield 0.3282. The discrepancy is plausibly due to downstream loss/process penalties and measurement variation; it does not uniquely identify a missing chemical step.

Polarity and potential window

The productive operating region was at negative applied potential. Batch 1, S0/E0 at +1.0 V, 200 mA, and 1200 s, gave conversion 0.0173, selectivity 0.9496, but selective yield 0 and score 0. In contrast, batch 2 with S0/E0 at -1.0 V, 500 mA, and 7200 s gave nonzero yield 0.0548 and score 0.2405. This suggests the desired transformation is reductive in the simulator's sign convention. It is not a clean polarity experiment, however, because current and duration also changed; therefore the claim is limited to the tested procedures rather than a universal proof about sign.

More negative potential was not monotonically better. For S1/E1 at 500 mA and 7200 s, batch 3 at -1.0 V gave conversion 0.1630, selectivity 0.5848, yield 0.0899, faradaic efficiency 0.3336, transport efficiency 0.3502, energy efficiency 0.3318, and score 0.3208. Batch 6 at -0.6 V improved conversion to 0.2039, selectivity to 0.6586, yield to 0.1424, faradaic efficiency to 0.4566, transport efficiency to 0.4319, energy efficiency to 0.4590, and score to 0.3855. Batch 7 at -0.3 V increased conversion further to 0.2413 and selectivity to 0.6979, but energy efficiency fell to 0.2935 and ohmic efficiency to 0.4506; its score fell to 0.3693. These results support a bounded productive window: strong negative drive incurs parasitic-current or transport penalties, whereas drive too close to zero incurs polarization/ohmic or energy penalties. The precise microscopic explanation is not identifiable from the public channels; a bell-shaped electron-transfer selectivity, competing electrolysis, or a potential-dependent interfacial state could all produce this pattern.

Time dependence

At S1/E1 and -0.6 V, doubling time from 7200 s in batch 6 to 14400 s in batch 8 raised conversion from 0.2039 to 0.3985 and yield from 0.1424 to 0.2432. Conversion therefore remained far from saturation and was approximately proportional to time over this interval. Selectivity changed only modestly, from 0.6586 to 0.6489, while the final score rose from 0.3855 to 0.4335. The less-than-proportional yield increase and slight selectivity loss are consistent with accumulated side reaction, product loss, or changing transport, but there was no direct species-resolved measurement that distinguishes these mechanisms. The campaign only tested the maximum 14400 s at refined conditions, so it cannot locate a time optimum beyond that boundary; recommending 14400 s is a within-domain boundary result, not evidence that still longer electrolysis would remain beneficial.

Material roles and coupling

The matched-pair screen at -1.0 V, 500 mA, and 7200 s showed strong material dependence. S1/E1 in batch 3 scored 0.3208, compared with S0/E0 in batch 2 at 0.2405, S2/E2 in batch 4 at 0.2716, and S3/E3 in batch 5 at 0.2053. Their respective conversion values were 0.1630, 0.0650, 0.1413, and 0.0489. Because solvent and electrolyte changed together, this screen alone could not assign the effect to either component.

Cross-pair experiments showed that the response is not a simple ranking of solvents or conductivity alone. At -0.45 V, 500 mA, and 14400 s, S1/E1 in batch 9 scored 0.4563, while replacing only S1 with S0 to form S0/E1 in batch 10 raised the score to 0.5045. Batch 10 gave conversion 0.4841, selectivity 0.7244, selective yield 0.3282, faradaic efficiency 0.5116, transport efficiency 0.5129, ohmic efficiency 0.7158, and energy efficiency 0.5271. In contrast, replacing E1 with E0 while retaining S0 in batch 11 reduced the score to 0.2861, with conversion 0.1541, yield 0.1015, faradaic efficiency 0.1530, and transport efficiency 0.1602. Thus E1 seems essential to the best observed interfacial/transport regime, while S0 improves its balance relative to S1.

This is qualitatively compatible with the nominal material dossier. S0 has higher relative conductivity than S1 (1.2 versus 0.7) and lower stated cost, which could improve iR and energy performance. S1 has higher nominal relative diffusivity (1.25 versus 0.78), yet S0/E1 still performed better, showing that bulk diffusivity alone does not control the response. E0 has higher nominal bulk conductivity than E1 (10.5 versus 5.8 S/m) but lower diffusivity, a thicker diffusion layer, more precipitating salt, and a different standard-potential shift. Its poor performance in batch 11 shows that maximizing nominal conductivity is insufficient. A plausible coupling is that E1 supplies favorable reaction selectivity and interfacial kinetics, while S0 improves conductivity and shifts the operating potential into a favorable window. Hidden fixed world residuals and solvent-electrolyte interactions could also be responsible; the campaign cannot separate those from the nominal-property explanation.

Potential shifts may explain why the optimum depends on materials. The dossier assigns S0 and S1 nominal standard-potential shifts of -0.08 and +0.02 V, respectively, and electrolyte-specific shifts as well. Accordingly, the same applied potential does not necessarily mean the same overpotential across pairs. A generic relationship would be E_eq = E_base + ΔE_solvent + ΔE_electrolyte + ΔE_hidden_interaction. The data support using an effective rather than raw potential, but they are insufficient to estimate all of these terms independently.

Local refinement around the best pair

Batch 10, S0/E1 at -0.45 V and 14400 s, was the campaign maximum at score 0.5045. Batch 12 tested the same materials, current limit, and time at -0.55 V. It gave conversion 0.4317, selectivity 0.6723, yield 0.3201, faradaic efficiency 0.4463, transport efficiency 0.4675, ohmic efficiency 0.7923, energy efficiency 0.5268, and score 0.4828. Moving from -0.45 to -0.55 V improved measured ohmic efficiency but reduced conversion, selectivity, faradaic efficiency, and transport efficiency enough to lower the total score. Together with the S1/E1 potential series, this supports a local balanced optimum near -0.45 V, although only two potentials were tested for S0/E1 and the exact optimum could lie between or slightly outside them.

Acidity and precipitation

The pH-normalized channel was comparatively stable within an electrolyte family and varied across electrolytes: approximately 0.20 for E1 batches, 0.229 for E0, 0.167 for E2, and 0.290 for E3 in the representative final assays. This is consistent with electrolyte-controlled acid speciation, in qualitative agreement with the different nominal acid concentrations and pKa values. Since pH was not independently varied, its causal effect on conversion or selectivity is unidentifiable; it may be a correlated material descriptor rather than the driver.

Precipitation was also strongly material dependent. E0 batches showed precipitation signal 1.0. The E2 and E3 matched-pair batches showed 0, while E1 conditions were intermediate to high: about 0.71-0.73 for S1/E1 and about 0.85 for S0/E1. High precipitation did not prevent S0/E1 from being the best pair, so precipitation is not a simple dominant negative predictor within these data. It could represent a spectator salt, product capture, electrode fouling, or a correlated equilibrium channel. Because no isolated solid assay or time-resolved precipitation experiment was performed, those alternatives remain unresolved. It may nevertheless be an important future optimization target because batch 10 combined the best score with a high precipitation signal of 0.854.

Measurement interpretation

Each batch received one UV-visible intermediate measurement after electrolysis and one destructive final assay after termination. The UV-visible measurements were useful directional indicators of faradaic, transport, ohmic, and energy efficiencies, but they were noisier and not identical to final-assay estimates. For batch 10, UV-visible estimates were approximately 0.519 faradaic, 0.477 transport, 0.726 ohmic, and 0.587 energy efficiency, whereas the final assay reported 0.512, 0.513, 0.716, and 0.527. This is consistent with the stated instrument uncertainties and different channel calibrations. Final conclusions therefore use the final assays. Most conditions were single batches without exact replication, so small score differences should not be treated as precise effects; the large qualitative differences are more credible than fine ranking near the optimum.

Scope and unidentifiable quantities

The report applies only to the tested 0.50 mol/L loading, 0.08 L volume, available anonymous materials, potentials from +1.0 to -1.0 V in the actual campaign, current limits of 200 or 500 mA, and times of 1200, 7200, or 14400 s. Loading, dilution, sequential potential programs, current limits below 500 mA in the productive region, mixed solvents, electrode geometry, and temperatures were not varied. Electrode area, gap, base resistance, and hidden world residuals were fixed but unknown, so kinetic constants, electron stoichiometry z, true current-time traces, exchange currents, transfer coefficients, diffusion coefficients in the actual mixtures, and an absolute equilibrium potential cannot be identified. Likewise, conversion loss cannot be partitioned uniquely into unreacted substrate, side product, degradation, or precipitated material.

Plausible alternative models include: a primarily kinetic model with a narrow potential-dependent selectivity window; a transport/passivation model in which precipitation or surface coverage lowers productive current; and a hidden material-interaction model in which S0/E1 happens to have favorable latent solvation and interface factors not predictable from the nominal dossier. The observations favor a hybrid model because potential, time, and material changes independently affected different efficiency channels, but they do not establish a unique molecular mechanism.

Overall conclusion

The most economical explanation is a reductive conversion operating in a finite effective-overpotential window. Productive charge initially accumulates roughly with time, but side reactions, polarization, transport, and material-dependent interfacial effects determine how much charge becomes selective product. Electrolyte E1 provides the best observed reaction/transport compromise, and solvent S0 improves conductivity and the effective potential environment when coupled to E1. Excessively negative potential sacrifices faradaic and transport performance; insufficiently negative potential sacrifices energy/ohmic balance. The sealed recommendation—batch 10: 0.04 mol reagent, 0.08 L S0, E1, -0.45 V, 500 mA limit, 14400 s—is therefore supported as the best observed balance, not as a proven global optimum.

## K2 封存报告

1. Claims and laws

No empirical, instance-specific prior or known response law was supplied. The public material dossier supplied nominal physical-property priors, but explicitly warned that hidden fixed residuals and solvent–electrolyte couplings could override a simple ranking.

My initial law that balanced performance should peak at an intermediate potential was supported locally. For S1/E1 at 7200 s, the score rose from 0.321 at -1.0 V in batch 3 to 0.385 at -0.6 V in batch 6, then fell to 0.369 at -0.3 V in batch 7. At 14400 s, -0.45 V in batch 9 scored 0.456 versus 0.433 at -0.6 V in batch 8. Batch 12 at -0.55 V also scored less than otherwise matched batch 10 at -0.45 V, 0.483 versus 0.505. These results changed my view from a generic “more drive gives more conversion” model to a finite effective-overpotential window balancing productive conversion against faradaic, transport, ohmic, and energy losses.

The associated claim of an intermediate time optimum was untested rather than supported. At -0.6 V, extending S1/E1 from 7200 s in batch 6 to 14400 s in batch 8 increased score from 0.385 to 0.433 and conversion from 0.204 to 0.398. Since 14400 s was the tested upper boundary, no downturn in performance with still longer time was observed.

The hypothesis that nominal conductivity alone would predict the best materials was contradicted. E0 has higher nominal bulk conductivity than E1, yet S0/E0 in batch 11 scored only 0.286, compared with 0.505 for S0/E1 in batch 10 under the same potential, current, time, loading, and solvent. Conversely, replacing S1 by the more conductive S0 while retaining E1 raised the score from 0.456 in batch 9 to 0.505 in batch 10. This evidence changed my explanation toward a solvent–electrolyte interaction: E1 supplied a favorable reaction/interface regime while S0 improved the overall balance. The matched-pair screen in batches 2–5 had suggested S1/E1 was best, but batches 9–11 showed that this was not a separable solvent ranking.

A negative-polarity preference received suggestive but not decisive support. Batch 1 at +1.0 V produced conversion 0.017 and reported selective yield 0, whereas subsequent negative-potential batches produced nonzero yield. That observation caused me to deprioritize positive potentials. However, batch 1 also used only 200 mA for 1200 s, while the main negative tests used 500 mA for 7200 or 14400 s. Thus polarity was never tested under charge-matched conditions. The strong efficiency channels in batch 1—approximately 0.939 faradaic, 0.911 transport, and 0.907 energy efficiency—are plausible opposing evidence. A universal “negative potential is productive, positive potential is not” law therefore remained untested, not established.

The claim that precipitation would necessarily suppress performance was contradicted as a simple law. Batch 10 was the best batch despite a precipitation signal near 0.854, while E2 and E3 conditions with precipitation signal 0 in batches 4 and 5 scored only 0.272 and 0.205. Precipitation could still affect yield or electrodes, but the campaign did not identify its role.

2. One additional discriminating experiment

I would repeat the complete batch-10 recipe but reverse only the potential from -0.45 to +0.45 V: 0.04 mol reagent, 0.08 L S0, E1, 500 mA, 14400 s, followed by the final assay. This directly distinguishes my leading sign-specific, finite-overpotential explanation from the alternative that batch 1's zero yield resulted mainly from insufficient charge and that positive potential can be equally or more productive.

If the positive-potential batch gave near-zero selective yield while retaining reasonable efficiency channels, I would strengthen the sign-specific interpretation: positive current would then appear to drive a non-target process or the wrong interfacial state. If it approached batch 10's yield of 0.328 and score of 0.505, I would reject the claimed reductive preference and reinterpret batch 1 as a low-charge, gate-limited observation. If it showed substantial conversion but low selective yield or selectivity, I would infer that both polarities consume reactant but only negative potential favors the target. If both conversion and efficiency collapsed, I would favor an effective-potential/kinetic explanation over a purely product-selectivity explanation. Because this would still be a single assay, a small difference from batch 10 would remain inconclusive relative to process and measurement uncertainty.

3. Unused evidence, reliability, and goal effects

I did not inspect the complete raw final-assay or UV–visible artifacts. I used their processed estimates but not full peak shapes, baselines, replicate signals, or mass-balance details. I also did not use pH-meter measurements, time-resolved sampling, current–time traces, isolated precipitate evidence, or exact replicate batches. Many nominal dossier variables—capacitance, pKa, solubility product, diffusion-layer thickness, and potential shifts—were used only qualitatively because the design did not vary them independently. Most cross-pairs were never tested, and electrode geometry and hidden fixed residuals remained unidentifiable.

The least reliable predictions are the long-duration positive-potential cases Q04, Q06, Q08, Q10, and especially high-current Q12. They extrapolate from the single short positive-potential batch 1. Q01, Q02, Q07, and Q09 are also fragile because their predicted selective yields lie near the 0.02 multiplicative score gate, so modest assay or model error can cause a discontinuous score change. All prediction queries also used 0.012 mol in 0.025 L rather than the campaign's 0.04 mol in 0.08 L; the concentration is similar, but fixed electrode geometry means volume scaling need not follow charge-per-mole scaling exactly.

The recommendation of batch 10 is reliable as the highest observed batch, but less reliable as a global optimum. It was not exactly replicated, the potential grid around -0.45 V was sparse, 14400 s was a boundary, and other solvent–electrolyte cross-pairs were not exhaustively screened.

The assigned maximization goal materially affected evidence collection. After S1/E1 and then S0/E1 performed well, I concentrated the remaining batches on improving score rather than balancing the design, reproducing conditions, testing positive polarity at equal charge, or identifying individual solvent and electrolyte effects. This exploitation produced a stronger operating recommendation but weaker causal identification and wider prediction uncertainty. There was no unavoidable conflict in the task itself, but under the 12-batch limit I favored optimization over mechanistic completeness.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.7,
        "lower80": 0.52,
        "upper80": 0.84
      },
      "energy_efficiency": {
        "estimate": 0.16,
        "lower80": 0.07,
        "upper80": 0.29
      },
      "faradaic_efficiency": {
        "estimate": 0.19,
        "lower80": 0.1,
        "upper80": 0.32
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.12
      },
      "selective_product_yield": {
        "estimate": 0.004,
        "lower80": 0,
        "upper80": 0.018
      },
      "transport_efficiency": {
        "estimate": 0.38,
        "lower80": 0.22,
        "upper80": 0.56
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.95,
        "lower80": 0.86,
        "upper80": 1
      },
      "energy_efficiency": {
        "estimate": 0.93,
        "lower80": 0.82,
        "upper80": 1
      },
      "faradaic_efficiency": {
        "estimate": 0.96,
        "lower80": 0.89,
        "upper80": 1
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.68
      },
      "selective_product_yield": {
        "estimate": 0.012,
        "lower80": 0,
        "upper80": 0.035
      },
      "transport_efficiency": {
        "estimate": 0.95,
        "lower80": 0.86,
        "upper80": 1
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.67,
        "lower80": 0.56,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.15,
        "lower80": 0.08,
        "upper80": 0.25
      },
      "faradaic_efficiency": {
        "estimate": 0.18,
        "lower80": 0.11,
        "upper80": 0.27
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.28,
        "lower80": 0.2,
        "upper80": 0.36
      },
      "selective_product_yield": {
        "estimate": 0.035,
        "lower80": 0.015,
        "upper80": 0.065
      },
      "transport_efficiency": {
        "estimate": 0.38,
        "lower80": 0.25,
        "upper80": 0.53
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.93,
        "lower80": 0.84,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.88,
        "lower80": 0.74,
        "upper80": 0.97
      },
      "faradaic_efficiency": {
        "estimate": 0.94,
        "lower80": 0.85,
        "upper80": 0.99
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.618,
        "lower80": 0.54,
        "upper80": 0.7
      },
      "selective_product_yield": {
        "estimate": 0.155,
        "lower80": 0.09,
        "upper80": 0.24
      },
      "transport_efficiency": {
        "estimate": 0.91,
        "lower80": 0.79,
        "upper80": 0.98
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.68,
        "lower80": 0.57,
        "upper80": 0.79
      },
      "energy_efficiency": {
        "estimate": 0.36,
        "lower80": 0.23,
        "upper80": 0.49
      },
      "faradaic_efficiency": {
        "estimate": 0.37,
        "lower80": 0.25,
        "upper80": 0.5
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.359,
        "lower80": 0.29,
        "upper80": 0.44
      },
      "selective_product_yield": {
        "estimate": 0.075,
        "lower80": 0.04,
        "upper80": 0.13
      },
      "transport_efficiency": {
        "estimate": 0.48,
        "lower80": 0.34,
        "upper80": 0.62
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.9,
        "lower80": 0.78,
        "upper80": 0.97
      },
      "energy_efficiency": {
        "estimate": 0.82,
        "lower80": 0.65,
        "upper80": 0.93
      },
      "faradaic_efficiency": {
        "estimate": 0.88,
        "lower80": 0.75,
        "upper80": 0.96
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.583,
        "lower80": 0.49,
        "upper80": 0.67
      },
      "selective_product_yield": {
        "estimate": 0.13,
        "lower80": 0.07,
        "upper80": 0.22
      },
      "transport_efficiency": {
        "estimate": 0.87,
        "lower80": 0.73,
        "upper80": 0.96
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.45,
        "upper80": 0.74
      },
      "energy_efficiency": {
        "estimate": 0.15,
        "lower80": 0.05,
        "upper80": 0.29
      },
      "faradaic_efficiency": {
        "estimate": 0.18,
        "lower80": 0.08,
        "upper80": 0.31
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.254,
        "lower80": 0,
        "upper80": 0.34
      },
      "selective_product_yield": {
        "estimate": 0.035,
        "lower80": 0.012,
        "upper80": 0.075
      },
      "transport_efficiency": {
        "estimate": 0.25,
        "lower80": 0.12,
        "upper80": 0.42
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.83,
        "lower80": 0.67,
        "upper80": 0.93
      },
      "energy_efficiency": {
        "estimate": 0.68,
        "lower80": 0.48,
        "upper80": 0.83
      },
      "faradaic_efficiency": {
        "estimate": 0.72,
        "lower80": 0.54,
        "upper80": 0.87
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.491,
        "lower80": 0.38,
        "upper80": 0.6
      },
      "selective_product_yield": {
        "estimate": 0.075,
        "lower80": 0.03,
        "upper80": 0.15
      },
      "transport_efficiency": {
        "estimate": 0.66,
        "lower80": 0.46,
        "upper80": 0.82
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.47,
        "upper80": 0.76
      },
      "energy_efficiency": {
        "estimate": 0.11,
        "lower80": 0.03,
        "upper80": 0.23
      },
      "faradaic_efficiency": {
        "estimate": 0.13,
        "lower80": 0.05,
        "upper80": 0.24
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.235,
        "lower80": 0,
        "upper80": 0.32
      },
      "selective_product_yield": {
        "estimate": 0.025,
        "lower80": 0.005,
        "upper80": 0.06
      },
      "transport_efficiency": {
        "estimate": 0.23,
        "lower80": 0.1,
        "upper80": 0.39
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.88,
        "lower80": 0.75,
        "upper80": 0.96
      },
      "energy_efficiency": {
        "estimate": 0.68,
        "lower80": 0.49,
        "upper80": 0.82
      },
      "faradaic_efficiency": {
        "estimate": 0.82,
        "lower80": 0.66,
        "upper80": 0.93
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.515,
        "lower80": 0.41,
        "upper80": 0.61
      },
      "selective_product_yield": {
        "estimate": 0.08,
        "lower80": 0.035,
        "upper80": 0.16
      },
      "transport_efficiency": {
        "estimate": 0.72,
        "lower80": 0.54,
        "upper80": 0.86
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.66,
        "lower80": 0.54,
        "upper80": 0.77
      },
      "energy_efficiency": {
        "estimate": 0.15,
        "lower80": 0.07,
        "upper80": 0.26
      },
      "faradaic_efficiency": {
        "estimate": 0.17,
        "lower80": 0.1,
        "upper80": 0.26
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.305,
        "lower80": 0.24,
        "upper80": 0.39
      },
      "selective_product_yield": {
        "estimate": 0.16,
        "lower80": 0.09,
        "upper80": 0.25
      },
      "transport_efficiency": {
        "estimate": 0.2,
        "lower80": 0.11,
        "upper80": 0.32
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.88,
        "lower80": 0.73,
        "upper80": 0.96
      },
      "energy_efficiency": {
        "estimate": 0.8,
        "lower80": 0.61,
        "upper80": 0.92
      },
      "faradaic_efficiency": {
        "estimate": 0.86,
        "lower80": 0.69,
        "upper80": 0.96
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.736,
        "lower80": 0.61,
        "upper80": 0.83
      },
      "selective_product_yield": {
        "estimate": 0.55,
        "lower80": 0.35,
        "upper80": 0.74
      },
      "transport_efficiency": {
        "estimate": 0.78,
        "lower80": 0.59,
        "upper80": 0.91
      }
    }
  ],
  "rationale": "Predictions extrapolate the campaign's fixed-concentration potential, charge-per-mole, time, and material trends. Negative-potential estimates are anchored by the -1.0 to -0.45 V assays; positive-potential efficiency estimates are anchored by batch 1, with yield scaled by charge per mole and bounded for depletion. Material adjustments follow the observed E1 advantage and the nominal conductivity, transport, and potential-shift differences. Intervals include final-assay noise, single-batch material comparisons, uncertainty from the smaller volume/current regime, and the score discontinuity near the 0.02 selective-yield gate."
}
```
