# repeat-01/EC-W01-B12-optimization-E-MisIndexed

既有科学公开材料；非provider内部推理。

来源：D:\Projects\ChemWorld-local-research\20261016-unified-matrices\attempt-01\repeat-01\EC-W01-B12-optimization-E-MisIndexed\participant\optimization-E-MisIndexed

## 同期笔记

### v1 · 公开事件 0

# Pre-experimental hypotheses

H1 [tentative] At fixed loading (0.020 mol reagent in 0.040 L solvent), higher nominal conductivity should improve transport and ohmic efficiency; therefore S0/E0 is an initial efficiency-oriented candidate, but selectivity may instead favor a lower-proton-activity solvent. Test consequence: matched electrolysis conditions should distinguish material effects.

H2 [tentative] Product formation is polarity-specific and likely peaks at an intermediate effective potential and charge. Both signs and a broad potential/current/time range should be screened before local refinement. Excess duration or driving force may raise conversion while lowering selectivity/energy efficiency.

Decision: use the first batches as a broad material/polarity/condition screen, then spend later batches refining the best observed score. Numerical differences will remain provisional where assay uncertainty or confounding prevents attribution.

### v2 · 公开事件 21

# Working hypotheses

H1 [supported in tested scope] Productive electrolysis is polarity-specific: at S0/E0, +1.0 V and 200 mA cap gave score 0.599 (event runner-operation-0007), whereas -1.0 V gave 0.333 with sharply poorer efficiency components (runner-operation-0014). Yield estimates were similar within assay uncertainty, so the score difference mainly supports an efficiency/polarity effect, not a yield effect.

H2 [supported qualitatively] Excess drive can destroy performance. At +2.0 V, 500 mA cap, 14,400 s, S0/E0, all product/conversion efficiency readouts collapsed to zero despite high ohmic efficiency (runner-operation-0021). This is consistent with degradation or severe side reaction, though potential, current cap, and duration were confounded.

H3 [tentative] The useful region lies at intermediate positive potential/charge. Next: separate potential/current/time with +1.0 to +1.5 V tests and compare materials. A nonzero high score at +1.5 V would narrow the cliff; otherwise refine near +1.0 V.

### v3 · 公开事件 49

# Working hypotheses

H1 [supported in tested scope] Productive performance at S0/E0 is strongly polarity- and potential-dependent. +1.0 V is far superior to -1.0 V (events runner-operation-0007 and -0014). +1.2 V already collapses most electrochemical metrics (runner-operation-0035), with +1.5 and +2.0 V essentially inactive (runner-operation-0028, -0021). This sharp cliff argues against simply maximizing voltage.

H2 [supported in tested scope] At +1.0 V, extending electrolysis from 7,200 to 14,400 s increased selective product yield from 0.090 to 0.216 and score from 0.599 to 0.646 while retaining high efficiencies (runner-operation-0007 vs -0049). This numerical gain exceeds the individual stated assay standard deviations, though it is not replicated.

H3 [unresolved] Lower potential (+0.8 V) for 14,400 s gave more yield (0.253) but much poorer faradaic/transport/energy efficiency and lower score 0.461 (runner-operation-0042). The balanced optimum is therefore near +1.0 V, but material shifts may move it.

Next decision: screen solvent/electrolyte identity under the +1.0 V, 200 mA, 14,400 s reference, then use remaining batches for local potential/duration refinement or replication. Revise if another material clearly exceeds score 0.646.

### v4 · 公开事件 84

# Final source-stage synthesis

H1 [supported in campaign scope] The response is polarity-specific with a narrow productive positive-potential window. For S0/E0, +1.0 V strongly outperformed -1.0 V, while +1.2 V and above collapsed balanced performance (runner-operation-0007, -0014, -0035, -0028, -0021). The exact cliff location is unresolved and may shift with material.

H2 [supported in campaign scope] Electrolyte E1 substantially improved the +1.0 V, 200 mA-cap, 14,400 s reference relative to E0: selective yield 0.687 vs 0.216 and score 0.844 vs 0.646 (runner-operation-0063 vs -0049), while all principal efficiency components remained high. This is evidence of a material effect under the matched tested condition, although only one batch per electrolyte was assayed.

H3 [supported qualitatively] Current cap trades conversion/yield against transport and faradaic efficiency. With S0/E1 at +1.0 V for 14,400 s, 500 mA raised yield to 0.819 but lowered score to 0.741 (runner-operation-0070); 300 mA yielded 0.790 and score 0.836 (runner-operation-0077). The 200 mA condition achieved the highest observed score, 0.844 (runner-operation-0063). The 250 mA score 0.841 (runner-operation-0084) is numerically close and not distinguishable from 200 mA given stated assay uncertainties and lack of repeats.

H4 [unresolved] Solvent S1 increased yield versus S0 under E0 but reduced balanced score and raised safety risk (runner-operation-0056 vs -0049). This single comparison does not establish a general solvent ranking or interaction with E1.

Recommendation decision: select batch 9 (S0, E1, 0.020 mol in 0.040 L, +1.0 V, 200 mA cap, 14,400 s) because it has the highest observed public score and a favorable efficiency balance. Batch 12 at 250 mA is statistically plausible as equivalent; replication around 200–250 mA would be the first follow-up that could change the selection.

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
      "current_mA": 200,
      "electrolyte_profile": 0,
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
    "cost": 0.2844737768173218,
    "electrochemical_conversion": 0.11903645098209381,
    "electrochemical_selectivity": 0.9495708346366882,
    "energy_efficiency": 0.9066821336746216,
    "faradaic_efficiency": 0.9392082691192627,
    "ohmic_efficiency": 0.9769874215126038,
    "pH_normalized": 0.23218974471092224,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.5993042588233948,
    "selective_product_yield": 0.09016075730323792,
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
      "amount_mol": 0.02,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.04
    },
    {
      "current_mA": 200,
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
    "cost": 0.28835999965667725,
    "electrochemical_conversion": 0.13263000547885895,
    "electrochemical_selectivity": 0.6285305023193359,
    "energy_efficiency": 0.23142015933990479,
    "faradaic_efficiency": 0.3768777847290039,
    "ohmic_efficiency": 0.9570533633232117,
    "pH_normalized": 0.2294943928718567,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.3331550657749176,
    "selective_product_yield": 0.095987968146801,
    "transport_efficiency": 0.40313461422920227
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
      "potential_V": 2
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
    "cost": 0.3402000069618225,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.0,
    "ohmic_efficiency": 0.9331657886505127,
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
      "current_mA": 200,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1.5
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
    "cost": 0.29124000668525696,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.02824951522052288,
    "ohmic_efficiency": 0.9702000021934509,
    "pH_normalized": 0.2295188158750534,
    "precipitation_signal": 0.987571656703949,
    "safety_risk": 0.072194404900074,
    "score": 0.003208077745512128,
    "selective_product_yield": 0.0007897500181570649,
    "transport_efficiency": 0.0
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
      "current_mA": 200,
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
    "cost": 0.2895120084285736,
    "electrochemical_conversion": 0.0034490374382585287,
    "electrochemical_selectivity": 0.006436008028686047,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.01102422270923853,
    "ohmic_efficiency": 0.9625267386436462,
    "pH_normalized": 0.2344796061515808,
    "precipitation_signal": 0.9868980646133423,
    "safety_risk": 0.072194404900074,
    "score": 0.03480406478047371,
    "selective_product_yield": 0.0084654176607728,
    "transport_efficiency": 0.0005147586925886571
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
      "current_mA": 200,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 0.8
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
    "cost": 0.29181599617004395,
    "electrochemical_conversion": 0.2637104392051697,
    "electrochemical_selectivity": 0.9315722584724426,
    "energy_efficiency": 0.4210221469402313,
    "faradaic_efficiency": 0.3745647370815277,
    "ohmic_efficiency": 0.9466148614883423,
    "pH_normalized": 0.23120366036891937,
    "precipitation_signal": 0.9975283145904541,
    "safety_risk": 0.072194404900074,
    "score": 0.4607919454574585,
    "selective_product_yield": 0.25288882851600647,
    "transport_efficiency": 0.3498813807964325
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
      "current_mA": 200,
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
    "cost": 0.28634756803512573,
    "electrochemical_conversion": 0.2323978990316391,
    "electrochemical_selectivity": 0.9370536208152771,
    "energy_efficiency": 0.9014825820922852,
    "faradaic_efficiency": 0.9168441295623779,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.23021826148033142,
    "precipitation_signal": 0.982570469379425,
    "safety_risk": 0.072194404900074,
    "score": 0.6458183526992798,
    "selective_product_yield": 0.21584126353263855,
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
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "current_mA": 200,
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
    "cost": 0.31011998653411865,
    "electrochemical_conversion": 0.40107688307762146,
    "electrochemical_selectivity": 0.955841064453125,
    "energy_efficiency": 0.6670317053794861,
    "faradaic_efficiency": 0.5522388219833374,
    "ohmic_efficiency": 0.9605118632316589,
    "pH_normalized": 0.23249587416648865,
    "precipitation_signal": 0.9908607602119446,
    "safety_risk": 0.09559440612792969,
    "score": 0.5920903086662292,
    "selective_product_yield": 0.36955907940864563,
    "transport_efficiency": 0.545743465423584
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
      "volume_L": 0.04
    },
    {
      "current_mA": 200,
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
    "cost": 0.29412001371383667,
    "electrochemical_conversion": 0.6947111487388611,
    "electrochemical_selectivity": 0.9521832466125488,
    "energy_efficiency": 0.9454994201660156,
    "faradaic_efficiency": 0.9248588681221008,
    "ohmic_efficiency": 0.9805063605308533,
    "pH_normalized": 0.2000686377286911,
    "precipitation_signal": 0.8648538589477539,
    "safety_risk": 0.072194404900074,
    "score": 0.8441886901855469,
    "selective_product_yield": 0.6869087219238281,
    "transport_efficiency": 0.9456901550292969
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
    "electrochemical_conversion": 0.8559954166412354,
    "electrochemical_selectivity": 0.9964759945869446,
    "energy_efficiency": 0.6003233194351196,
    "faradaic_efficiency": 0.4596281349658966,
    "ohmic_efficiency": 0.8661380410194397,
    "pH_normalized": 0.19775448739528656,
    "precipitation_signal": 0.8540157079696655,
    "safety_risk": 0.072194404900074,
    "score": 0.7414310574531555,
    "selective_product_yield": 0.8192248344421387,
    "transport_efficiency": 0.4609777331352234
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
    "electrochemical_conversion": 0.8291028141975403,
    "electrochemical_selectivity": 0.9580751657485962,
    "energy_efficiency": 0.9082831144332886,
    "faradaic_efficiency": 0.7308927178382874,
    "ohmic_efficiency": 0.9288291335105896,
    "pH_normalized": 0.19873952865600586,
    "precipitation_signal": 0.8619048595428467,
    "safety_risk": 0.072194404900074,
    "score": 0.8357051610946655,
    "selective_product_yield": 0.7900680303573608,
    "transport_efficiency": 0.7380726337432861
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
      "current_mA": 250,
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
    "cost": 0.296999990940094,
    "electrochemical_conversion": 0.7703025341033936,
    "electrochemical_selectivity": 0.9466809630393982,
    "energy_efficiency": 0.8961553573608398,
    "faradaic_efficiency": 0.8092880249023438,
    "ohmic_efficiency": 0.9544808268547058,
    "pH_normalized": 0.19925984740257263,
    "precipitation_signal": 0.8552408218383789,
    "safety_risk": 0.072194404900074,
    "score": 0.8408148288726807,
    "selective_product_yield": 0.7694494128227234,
    "transport_efficiency": 0.8305130004882812
  }
}
```

## K1 封存报告

## Mechanistic account

I interpret this world as a charge-driven electrochemical conversion with three competing processes: desired electron transfer, parasitic electron transfer, and a high-driving-force loss process such as product degradation, electrode passivation, or diversion to unobserved products. Mass transport, ohmic loss, proton activity, precipitation, and the imposed current ceiling modulate those processes. This is an empirical explanation of the synthetic benchmark, not a claim about a named real chemical system.

### 1. Public objective and measured state variables

The reported balanced-efficiency score is consistent with the public weighted sum

S = 0.30Y + 0.15Sel + 0.10X + 0.15EE + 0.12FE + 0.10TE + 0.08OE,

where Y is selective-product yield, Sel electrochemical selectivity, X conversion, EE energy efficiency, FE faradaic efficiency, TE transport efficiency, and OE ohmic efficiency. A low-yield gate applies near Y = 0.02. Thus, maximizing conversion or yield alone is not sufficient: current and potential that accelerate conversion can reduce several efficiency terms enough to lower the total score.

The controlled variables explored were applied potential, current cap, electrolysis duration, solvent, and electrolyte. Reagent loading and initial volume were held at 0.020 mol and 0.040 L throughout, so the observations principally describe that 0.5 mol/L starting composition. Temperature, electrode geometry, gap, contact resistance, true current history, interfacial concentrations, and identities of side products were not measured.

### 2. Potential and polarity: a narrow productive window

Batch 1 established a productive reference using S0/E0, +1.0 V, a 200 mA cap, and 7,200 s. It produced conversion 0.119, yield 0.090, selectivity 0.950, FE 0.939, TE 0.911, OE 0.977, EE 0.907, and score 0.599.

Batch 2 reversed the polarity while retaining the other conditions. At -1.0 V it gave similar measured conversion (0.133) and yield (0.096), but selectivity fell to 0.629, FE to 0.377, TE to 0.403, and EE to 0.231; the score fell to 0.333. The yield difference from batch 1 is not compelling relative to assay uncertainty, but the large efficiency differences support a polarity-specific interfacial pathway. Negative polarization can apparently consume reactant or charge, but much less of the charge follows the efficient target pathway.

Batches 3–5 revealed a sharp loss of performance above the productive positive-potential window. Batch 5 at +1.2 V, 200 mA, and 7,200 s gave only 0.0085 yield and score 0.0348. Batch 4 at +1.5 V under the same cap and duration gave 0.00079 yield and score 0.0032. Batch 3 combined +2.0 V, 500 mA, and 14,400 s and returned zero for conversion, yield, selectivity, FE, TE, and EE, with score zero. Batch 3 confounds voltage, cap, and duration, but batches 4 and 5 show that elevated voltage itself is associated with the collapse.

I therefore do not model target rate as monotonically increasing with applied potential. A plausible qualitative scheme is

reactant --k_target(η)--> target
reactant --k_side(η)--> side products
target --k_loss(η,Q,t)--> degradation or electrochemically invisible material,

where η is an effective overpotential and Q is delivered charge. Around the useful window, k_target is large and k_side and k_loss remain modest. Above a threshold, k_loss, k_side, or passivation grows much faster than k_target. The zero-like endpoint at high voltage could arise from destructive chemistry, strong passivation, or an assay-visible species being removed from the calibrated channels. Those alternatives cannot be distinguished here.

An empirical response law could use windowed rates, for example

k_target = k0 f(materials) exp(aη) exp[-b max(0,η-η_cliff)^2],
k_side = ks f_s(materials) exp(c|η|),

with an additional passivation or degradation state that accumulates at high |η|. This is a proposed structure, not a fitted equation.

### 3. Duration and charge exposure

Batches 1 and 7 isolate duration reasonably well for S0/E0 at +1.0 V and a 200 mA cap. Increasing duration from 7,200 to 14,400 s increased conversion from 0.119 to 0.232 and yield from 0.090 to 0.216. The principal efficiencies remained high: batch 7 reported selectivity 0.937, FE 0.917, TE 0.920, OE 1.000, and EE 0.901. Its score rose to 0.646.

Thus, within this tested condition, additional exposure accumulated target rather than immediately destroying it. Conversion was approximately doubled, consistent with progress that was still well short of complete. Yield increased by about 2.4-fold, although exact proportionality should not be overinterpreted because each condition had only one destructive assay.

Batch 6 showed why duration cannot be interpreted without potential. At +0.8 V, 200 mA, and 14,400 s, conversion and yield were actually slightly higher than in batch 7 (0.264 and 0.253), but FE was only 0.375, TE 0.350, and EE 0.421, giving score 0.461. In this world, +0.8 V can accumulate product, but apparently does so with substantially poorer charge utilization and transport behavior. The balanced optimum near +1.0 V is therefore not simply the maximum-conversion potential.

A useful progress model would be based on delivered rather than commanded charge:

dX/dt = (I_actual/(nF N0)) FE(η,I,materials,state) (1-X) - k_loss X,

dY/dt = Sel(η,I,materials,state) dX_formed/dt - k_product_loss Y.

I_actual was not exposed, so neither electron stoichiometry n nor kinetic constants are identifiable. The commanded current is only a cap and should not automatically be treated as the actual current.

### 4. Electrolyte-dependent mass transport and interfacial potential

The largest improvement came from changing electrolyte. Batch 9 used S0/E1 at +1.0 V, 200 mA, and 14,400 s. It gave conversion 0.695, yield 0.687, selectivity 0.952, FE 0.925, TE 0.946, OE 0.981, EE 0.945, and the campaign-best score 0.844. Under matched operational settings, batch 7 with E0 gave conversion 0.232, yield 0.216, and score 0.646.

The nominal material dossier provides a plausible transport explanation. E1 has lower bulk conductivity than E0 (5.8 versus 15.0 S/m), but its diffusion layer is much thinner (0.95 versus 2.8 mm) and its diffusivity is higher (1.25e-9 versus 6.5e-10 m²/s). A simple mass-transfer coefficient k_m proportional to D/delta is therefore roughly 5.7 times larger for E1 than E0 before hidden residuals and solvent coupling. That direction agrees with the much higher conversion and the high measured TE in batch 9. Conductivity alone is consequently not the governing material descriptor; interfacial mass transfer and potential alignment can dominate.

Nominal standard-potential shifts also differ: E0 is listed at +0.28 V, E1 at 0.0 V, while S0 contributes -0.08 V. If these shifts enter an effective overpotential such as

η = V_applied - [E_base + ΔE_electrolyte + ΔE_solvent + hidden residual] - I_actual R,

then changing E0 to E1 moves the system substantially relative to the narrow productive window. The sign convention and E_base are not observable, so this equation is only a mechanistic bookkeeping hypothesis. The E1 improvement may result from mass transport, better overpotential alignment, different proton activity or double-layer behavior, or a combination.

The pH-related and precipitation observables changed consistently with an electrolyte effect. E0/S0 batches near the reference had pH_normalized around 0.23 and precipitation_signal near 0.98–1.00. E1/S0 batches were around pH_normalized 0.20 and precipitation_signal 0.85–0.86. These signals were not part of the weighted score, and the meaning of a high precipitation signal cannot be converted into a physical solid amount from the available evidence. Still, they show that E1 changed acid/precipitation equilibria along with electrochemical performance. Reduced passivation by precipitate is one plausible contributor, but it is not established.

E2 and E3 were never tested. Consequently, the campaign supports E1 over E0 only under the tested S0/reference conditions; it does not establish that E1 is globally best among all four electrolytes.

### 5. Current cap: conversion-efficiency tradeoff

Batches 9–12 map the current-cap response for S0/E1 at +1.0 V and 14,400 s:

- Batch 9, 200 mA: conversion 0.695, yield 0.687, FE 0.925, TE 0.946, OE 0.981, EE 0.945, score 0.844.
- Batch 12, 250 mA: conversion 0.770, yield 0.769, FE 0.809, TE 0.831, OE 0.954, EE 0.896, score 0.841.
- Batch 11, 300 mA: conversion 0.829, yield 0.790, FE 0.731, TE 0.738, OE 0.929, EE 0.908, score 0.836.
- Batch 10, 500 mA: conversion 0.856, yield 0.819, FE 0.460, TE 0.461, OE 0.866, EE 0.600, score 0.741.

Conversion and yield generally rose with the cap, but with diminishing returns. FE, TE, and OE generally declined, especially at 500 mA. This is consistent with concentration polarization: greater current depletes reactant near the electrode faster than diffusion replenishes it, increasing parasitic charge and ohmic heating/loss. A schematic coupling is

I_actual = min(I_cap, I_kinetic(η), I_transport),
I_transport approximately proportional to n F A (D/delta) C_surface,
TE approximately decreases as I_actual/I_transport approaches or exceeds the favorable regime.

An ohmic term V_ohmic = I_actual R_solution would additionally lower OE and EE as current increases. E1's thin diffusion layer permits much greater productive throughput than E0, but even E1 becomes transport-limited at high cap.

The 200 and 250 mA scores differ by only 0.0034, much smaller than what can safely be resolved from single noisy assays. Batch 9 is the highest observation and was therefore selected, but batches 9 and 12 are scientifically plausible near-equivalents. The evidence is stronger for rejecting 500 mA as a balanced optimum than for locating the optimum precisely between 200 and 250 mA.

### 6. Solvent effects

Batch 8 changed S0 to S1 while retaining E0, +1.0 V, 200 mA, and 14,400 s. Relative to batch 7, S1 raised conversion from 0.232 to 0.401 and yield from 0.216 to 0.370, but reduced FE from 0.917 to 0.552, TE from 0.920 to 0.546, and EE from 0.901 to 0.667. Score fell from 0.646 to 0.592. Safety risk also rose from 0.0722 to 0.0956, still well below the 0.65 limit.

The dossier lists S1 as more diffusive but less conductive than S0, with lower proton activity and a +0.02 V rather than -0.08 V nominal potential shift. The observed combination—more product but poorer charge and transport efficiency—could reflect a changed effective potential, altered solvation/selectivity, or a mismatch between reaction rate and bulk conduction. Because only E0 was used in this solvent comparison, solvent and electrolyte may interact. S1 with E1 was not tested, and S2/S3 were not tested, so no global solvent ordering is justified.

### 7. How the explanation changed during the campaign

Batch 1 initially suggested that the high nominal conductivity of S0/E0 would be a strong efficiency-oriented choice. Batch 2 established that polarity substantially changes efficiency even when measured conversion and yield are similar. Batches 3–5 overturned any simple 'more voltage gives more reaction' account by revealing a sharp high-voltage collapse. Batches 6 and 7 separated conversion from balanced efficiency and showed that duration could raise yield safely near +1.0 V.

Batch 8 showed that a solvent can raise yield while lowering the balanced score. Batch 9 was the major mechanistic revision: despite E1's lower nominal bulk conductivity, it greatly increased conversion and yield without sacrificing efficiency. This shifted the explanation from conductivity-dominated behavior toward coupled mass transfer, interfacial potential, and electrolyte equilibrium effects. Batches 10–12 then demonstrated the current-dependent conversion/efficiency tradeoff and narrowed the useful cap to roughly 200–250 mA for the tested recipe.

### 8. Scope, uncertainty, and alternative explanations

This explanation is valid only for the sampled benchmark world and principally for 0.020 mol reagent in 0.040 L solvent. Concentration, volume, reagent loading, sequential electrolysis, and longer total durations were not varied. There were no replicate final assays, so close numerical rankings—especially batches 9 versus 12—cannot be treated as statistically resolved.

Several factors are structurally unidentifiable:

1. Actual current and charge were not reported, preventing kinetic or electron-stoichiometry estimation.
2. Electrode area, gap, base resistance, and world-specific material residuals were fixed but hidden.
3. The assay reports calibrated public proxies rather than molecular identities, so side products and degradation pathways cannot be assigned.
4. Potential shifts, transport properties, proton activity, precipitation, and double-layer capacitance change together when a material is changed.
5. High-voltage failure could be chemical degradation, passivation, reactant depletion, target destruction, or movement outside an assay-visible state.
6. The precipitation signal may mark equilibrium tendency, suspended material, or another calibrated proxy; its causal relation to transport is not established.
7. Noise can produce internally imperfect relations, such as small discrepancies between measured conversion, selectivity, and yield, so exact algebraic identities should not be imposed on individual assays.

A plausible alternative to the proposed degradation cliff is a highly nonmonotonic faradaic-efficiency window with little actual current at some voltages. Another is rapid electrode passivation rather than bulk degradation. Likewise, E1's advantage could be dominated by its potential shift rather than its D/delta ratio. The present experiments demonstrate the operational response but do not uniquely partition those mechanisms.

Overall, the simplest account consistent with the campaign is a narrow positive-potential target pathway whose useful rate is jointly controlled by material-dependent effective overpotential and mass transfer. Moderate charge exposure accumulates target; excessive voltage invokes a catastrophic competing process, while excessive current cap creates transport and faradaic losses. Under the tested composition, S0/E1 at +1.0 V and approximately a 200–250 mA cap lies near the best balance, with batch 9 providing the highest observed score.

## K2 封存报告

1. No instance-specific prior or proposed response law was supplied. The public material dossier provided only nominal mechanistic priors, not a ranking. My initial conductivity-oriented conjecture was contradicted: E1 had lower nominal conductivity than E0, yet batch 9 greatly outperformed matched batch 7, supporting a stronger role for mass transfer, potential alignment, or electrolyte coupling. The polarity law was supported by batches 1 and 2: reversing +1.0 V to -1.0 V sharply reduced selectivity and efficiency. The intermediate-potential-window hypothesis was supported by the collapse at +1.2, +1.5, and +2.0 V in batches 5, 4, and 3. The duration law was supported locally by batches 1 and 7, where doubling time increased yield while retaining high efficiencies. The current-cap tradeoff was supported by batches 9–12: yield rose from 200 to 500 mA, but transport and faradaic efficiency deteriorated, lowering the score at 500 mA. Batch 9 most changed my judgment because E1 delivered both much greater yield and high efficiencies. General claims about E2, E3, S2, S3, electrolyte–solvent interactions, concentration effects, and behavior beyond 14,400 s remained untested.

2. I would run one sequential challenge experiment at the original S0/E0 loading: +1.0 V, 200 mA for 7,200 s, followed by +1.2 V, 200 mA for 7,200 s, then terminate and assay. Batch 1 indicates that the first segment should create about 0.09 yield, while batch 5 shows almost no endpoint product when +1.2 V is used alone. If the sequential yield collapsed well below roughly 0.05, I would favor voltage-induced destruction of existing target. If approximately the batch-1 yield remained but did not grow, I would favor inhibited formation or electrode passivation that leaves existing target intact. If yield approached the longer +1.0 V result from batch 7, I would weaken the proposed voltage cliff and consider transient conditioning, stochastic assay variation, or a history-dependent interface instead.

3. Much evidence was underused: raw spectral artifacts were not inspected; UV–visible intermediate measurements were used mainly as qualitative checks; pH_normalized and precipitation_signal were not systematically modeled; and nominal acidity, double-layer capacitance, Ksp, cost, and safety data were not separated experimentally. No pH-meter measurements or replicate final assays were obtained. The blind predictions involving untested E3 or S2 (especially Q07–Q10) are least reliable, followed by the 500 mA extrapolations Q11–Q12 and the 600 s predictions Q01–Q02, whose scores are highly sensitive to the 0.02 yield gate. Negative-polarity E1 in Q05 is also weakly identified. The batch-9 recommendation is operationally defensible but not statistically secure because batch 12 was only 0.0034 score lower and neither condition was replicated. The score-maximization goal did affect evidence collection: after batch 9, experiments concentrated on current-cap refinement near the apparent optimum rather than broad material coverage, replication, or mechanistic diagnostics. I see no clear conflict with the assigned goal, but that adaptive emphasis reduced the reliability of predictions outside the optimized region.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.38,
        "upper80": 0.8
      },
      "energy_efficiency": {
        "estimate": 0.32,
        "lower80": 0.15,
        "upper80": 0.5
      },
      "faradaic_efficiency": {
        "estimate": 0.38,
        "lower80": 0.2,
        "upper80": 0.57
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.13,
        "lower80": 0.0,
        "upper80": 0.34
      },
      "selective_product_yield": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.025
      },
      "transport_efficiency": {
        "estimate": 0.55,
        "lower80": 0.32,
        "upper80": 0.73
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.9,
        "lower80": 0.7,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.72,
        "lower80": 0.5,
        "upper80": 0.88
      },
      "faradaic_efficiency": {
        "estimate": 0.75,
        "lower80": 0.54,
        "upper80": 0.91
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.3,
        "lower80": 0.04,
        "upper80": 0.55
      },
      "selective_product_yield": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "transport_efficiency": {
        "estimate": 0.78,
        "lower80": 0.58,
        "upper80": 0.93
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.63,
        "lower80": 0.48,
        "upper80": 0.76
      },
      "energy_efficiency": {
        "estimate": 0.32,
        "lower80": 0.2,
        "upper80": 0.45
      },
      "faradaic_efficiency": {
        "estimate": 0.38,
        "lower80": 0.25,
        "upper80": 0.52
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.351,
        "lower80": 0.24,
        "upper80": 0.46
      },
      "selective_product_yield": {
        "estimate": 0.075,
        "lower80": 0.035,
        "upper80": 0.14
      },
      "transport_efficiency": {
        "estimate": 0.52,
        "lower80": 0.36,
        "upper80": 0.67
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.93,
        "lower80": 0.84,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.68,
        "lower80": 0.5,
        "upper80": 0.83
      },
      "faradaic_efficiency": {
        "estimate": 0.7,
        "lower80": 0.52,
        "upper80": 0.85
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.523,
        "lower80": 0.39,
        "upper80": 0.66
      },
      "selective_product_yield": {
        "estimate": 0.11,
        "lower80": 0.05,
        "upper80": 0.22
      },
      "transport_efficiency": {
        "estimate": 0.74,
        "lower80": 0.56,
        "upper80": 0.88
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.34,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.28,
        "lower80": 0.12,
        "upper80": 0.48
      },
      "faradaic_efficiency": {
        "estimate": 0.32,
        "lower80": 0.14,
        "upper80": 0.53
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.36,
        "lower80": 0.22,
        "upper80": 0.51
      },
      "selective_product_yield": {
        "estimate": 0.15,
        "lower80": 0.05,
        "upper80": 0.3
      },
      "transport_efficiency": {
        "estimate": 0.48,
        "lower80": 0.25,
        "upper80": 0.7
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.94,
        "lower80": 0.84,
        "upper80": 0.99
      },
      "energy_efficiency": {
        "estimate": 0.72,
        "lower80": 0.5,
        "upper80": 0.88
      },
      "faradaic_efficiency": {
        "estimate": 0.7,
        "lower80": 0.48,
        "upper80": 0.87
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.626,
        "lower80": 0.48,
        "upper80": 0.76
      },
      "selective_product_yield": {
        "estimate": 0.34,
        "lower80": 0.18,
        "upper80": 0.55
      },
      "transport_efficiency": {
        "estimate": 0.76,
        "lower80": 0.53,
        "upper80": 0.91
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.28,
        "upper80": 0.77
      },
      "energy_efficiency": {
        "estimate": 0.24,
        "lower80": 0.08,
        "upper80": 0.47
      },
      "faradaic_efficiency": {
        "estimate": 0.28,
        "lower80": 0.1,
        "upper80": 0.52
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.305,
        "lower80": 0.14,
        "upper80": 0.49
      },
      "selective_product_yield": {
        "estimate": 0.07,
        "lower80": 0.015,
        "upper80": 0.18
      },
      "transport_efficiency": {
        "estimate": 0.42,
        "lower80": 0.18,
        "upper80": 0.68
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.93,
        "lower80": 0.78,
        "upper80": 0.99
      },
      "energy_efficiency": {
        "estimate": 0.78,
        "lower80": 0.52,
        "upper80": 0.94
      },
      "faradaic_efficiency": {
        "estimate": 0.8,
        "lower80": 0.54,
        "upper80": 0.95
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.577,
        "lower80": 0.4,
        "upper80": 0.74
      },
      "selective_product_yield": {
        "estimate": 0.18,
        "lower80": 0.07,
        "upper80": 0.38
      },
      "transport_efficiency": {
        "estimate": 0.72,
        "lower80": 0.43,
        "upper80": 0.9
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.5,
        "lower80": 0.22,
        "upper80": 0.74
      },
      "energy_efficiency": {
        "estimate": 0.2,
        "lower80": 0.05,
        "upper80": 0.43
      },
      "faradaic_efficiency": {
        "estimate": 0.25,
        "lower80": 0.07,
        "upper80": 0.5
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.265,
        "lower80": 0.1,
        "upper80": 0.46
      },
      "selective_product_yield": {
        "estimate": 0.04,
        "lower80": 0.005,
        "upper80": 0.12
      },
      "transport_efficiency": {
        "estimate": 0.35,
        "lower80": 0.12,
        "upper80": 0.62
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.9,
        "lower80": 0.7,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.52,
        "lower80": 0.26,
        "upper80": 0.75
      },
      "faradaic_efficiency": {
        "estimate": 0.55,
        "lower80": 0.29,
        "upper80": 0.78
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.445,
        "lower80": 0.27,
        "upper80": 0.62
      },
      "selective_product_yield": {
        "estimate": 0.075,
        "lower80": 0.02,
        "upper80": 0.2
      },
      "transport_efficiency": {
        "estimate": 0.58,
        "lower80": 0.3,
        "upper80": 0.8
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.5,
        "lower80": 0.27,
        "upper80": 0.7
      },
      "energy_efficiency": {
        "estimate": 0.12,
        "lower80": 0.02,
        "upper80": 0.3
      },
      "faradaic_efficiency": {
        "estimate": 0.15,
        "lower80": 0.03,
        "upper80": 0.34
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.245,
        "lower80": 0.12,
        "upper80": 0.39
      },
      "selective_product_yield": {
        "estimate": 0.1,
        "lower80": 0.03,
        "upper80": 0.25
      },
      "transport_efficiency": {
        "estimate": 0.18,
        "lower80": 0.03,
        "upper80": 0.4
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.88,
        "lower80": 0.69,
        "upper80": 0.97
      },
      "energy_efficiency": {
        "estimate": 0.24,
        "lower80": 0.07,
        "upper80": 0.48
      },
      "faradaic_efficiency": {
        "estimate": 0.2,
        "lower80": 0.04,
        "upper80": 0.45
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.417,
        "lower80": 0.27,
        "upper80": 0.57
      },
      "selective_product_yield": {
        "estimate": 0.33,
        "lower80": 0.15,
        "upper80": 0.55
      },
      "transport_efficiency": {
        "estimate": 0.22,
        "lower80": 0.04,
        "upper80": 0.48
      }
    }
  ],
  "rationale": "Predictions extrapolate from the campaign’s polarity-specific, narrow positive-potential window and its observed current/transport tradeoff. The new concentration (0.48 M) is close to the studied 0.50 M, but 100 mA and shorter charge exposures generally imply lower yield; 600 s cases may fall below the score’s 0.02 yield gate. E1 is expected to outperform E0 through its higher nominal D/delta, while E3 and especially S2 carry wide intervals because they were not experimentally tested. At 500 mA I expect greater conversion/yield but severe faradaic, transport, and energy losses. Intervals include assay noise plus substantial extrapolation uncertainty, particularly for unseen material combinations and negative polarity."
}
```
