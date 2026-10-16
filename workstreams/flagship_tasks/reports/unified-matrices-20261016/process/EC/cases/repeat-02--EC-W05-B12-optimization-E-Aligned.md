# repeat-02/EC-W05-B12-optimization-E-Aligned

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-02\EC-W05-B12-optimization-E-Aligned\participant\optimization-E-Aligned

## 同期笔记

### v1 · 公开事件 0

# Electrochemical campaign hypotheses

## H1 [tentative]
At fixed loading (0.040 mol in 0.080 L), balanced score should peak at a moderate driving potential and electrolysis time: insufficient charge limits conversion, while excessive magnitude/time lowers selectivity and energy efficiency. Test across both signs, caps, and durations.

## H2 [tentative]
Higher-conductivity solvent/electrolyte combinations should improve ohmic efficiency, but transport, precipitation, and interfacial selectivity may favor a different combination. Nominally S0/E0 or S0/E3 are conductivity candidates; experimental assays are authoritative.

## Plan
Use early batches as a material/polarity screen, then refine potential, current cap, and duration around the best observed region. One UV-vis measurement per batch will be used when informative. A numerical difference will not be treated as a reliable material effect without corroboration.

### v2 · 公开事件 70

# Electrochemical campaign hypotheses

## H1 [supported in tested positive-potential scope]
Positive potential is productive; the matched negative-potential test gave zero selective yield (event runner-operation-0007), whereas +1.0 V gave nonzero yield and score (runner-operation-0014). At S0/E0, increasing duration from 600 to 14,400 s increased observed selective yield and score while keeping high selectivity (events 0014, 0035, 0042, 0049, 0056). Thus the optimum in that tested range is at or beyond the longest single segment, though degradation beyond it remains unresolved.

## H2 [material effect supported for S1 versus tested alternatives at +1.0 V, 200 mA cap, 14,400 s]
S1/E0 substantially outperformed S0/E0 and S2/E0 in the matched long run: score 0.576 and yield 0.241 (event 0063), versus 0.465/0.148 (0056) and 0.425/0.129 (0070). S1 improved faradaic and transport efficiencies but reduced selectivity relative to S0. This single comparison is larger than typical assay noise, but repeatability remains untested.

## H3 [supported warning]
High cap/overdrive is harmful in tested cases: +1.5 V, 500 mA, 7200 s with S0/E1 collapsed the measured efficiencies and yield (event 0021), and +1.0 V, 500 mA with S0/E3 was also poor (0028). Material confounding prevents attributing this solely to current or potential.

## Next decisions
Use the remaining batches to test whether S1/E0 benefits from longer segmented electrolysis and to refine potential/current around +1.0 V. Reverse the long-duration claim if added duration lowers balanced score.

### v3 · 公开事件 85

# Electrochemical campaign hypotheses — final source-stage record

## H1 [supported in tested scope]
Productive polarity is positive. The matched negative run gave zero yield (runner-operation-0007), while positive runs produced target (0014 onward). At S0/E0, longer operation through 14,400 s raised yield and balanced score (0014, 0035, 0042, 0049, 0056).

## H2 [supported in matched material comparison; repeatability unresolved]
At +1.0 V, 200 mA cap, 14,400 s, S1/E0 was the best tested material combination (runner-operation-0063: score about 0.576, yield about 0.241), exceeding S0/E0 (0056) and S2/E0 (0070). Its advantage came chiefly from higher faradaic, transport, and energy efficiencies, despite lower selectivity than S0.

## H3 [supported non-monotonic time/cap response]
Simply doubling the S1/E0 electrolysis from 14,400 to 28,800 s reduced yield and efficiency (runner-operation-0078), consistent with time-dependent degradation/passivation or loss of productive current. Raising the cap from 200 to 300 mA at 14,400 s also reduced balanced score (0085 versus 0063), mainly through lower efficiency rather than a large yield gain. Thus cap is an active constraint and not equivalent to delivered charge.

## H4 [supported warning, attribution unresolved]
The combined high-potential/high-cap/material changes tested at +1.5 V, 500 mA collapsed performance (0021). Because potential, cap, and electrolyte changed together, the causal contribution of each remains unresolved.

## Decision
Recommend batch 9 (S1, E0, +1.0 V, 200 mA cap, 14,400 s, fixed 0.040 mol/0.080 L loading). Change this choice if replicate evidence shows its apparent efficiency advantage is assay/process noise, or if finer potential/cap refinement finds a reproducibly higher score.

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
    "cost": 0.3526799976825714,
    "electrochemical_conversion": 0.01442666444927454,
    "electrochemical_selectivity": 0.6481926441192627,
    "energy_efficiency": 0.3096332252025604,
    "faradaic_efficiency": 0.43699949979782104,
    "ohmic_efficiency": 0.9295637607574463,
    "pH_normalized": 0.23308512568473816,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.40829575061798096
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
      "current_mA": 200,
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
    "cost": 0.3526799976825714,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.9981916546821594,
    "energy_efficiency": 0.5586340427398682,
    "faradaic_efficiency": 0.5001056790351868,
    "ohmic_efficiency": 0.9384015798568726,
    "pH_normalized": 0.2303897738456726,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.3551696836948395,
    "selective_product_yield": 0.01666507124900818,
    "transport_efficiency": 0.5263625383377075
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
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 1,
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
    "cost": 0.37380000948905945,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.0,
    "ohmic_efficiency": 0.8389231562614441,
    "pH_normalized": 0.20273536443710327,
    "precipitation_signal": 0.8421508073806763,
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
    "cost": 0.35580000281333923,
    "electrochemical_conversion": 0.009741307236254215,
    "electrochemical_selectivity": 0.8725504875183105,
    "energy_efficiency": 0.14014863967895508,
    "faradaic_efficiency": 0.1442456841468811,
    "ohmic_efficiency": 0.8490503430366516,
    "pH_normalized": 0.2699976861476898,
    "precipitation_signal": 0.0,
    "safety_risk": 0.072194404900074,
    "score": 0.1643650233745575,
    "selective_product_yield": 0.012978817336261272,
    "transport_efficiency": 0.11275814473628998
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
    "cost": 0.35363999009132385,
    "electrochemical_conversion": 0.026599589735269547,
    "electrochemical_selectivity": 0.9946044683456421,
    "energy_efficiency": 0.5395680069923401,
    "faradaic_efficiency": 0.5073994994163513,
    "ohmic_efficiency": 0.9367675185203552,
    "pH_normalized": 0.23537498712539673,
    "precipitation_signal": 0.9869949817657471,
    "safety_risk": 0.072194404900074,
    "score": 0.427706778049469,
    "selective_product_yield": 0.03134206309914589,
    "transport_efficiency": 0.49689000844955444
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
    "cost": 0.3550800085067749,
    "electrochemical_conversion": 0.04791633039712906,
    "electrochemical_selectivity": 0.9924110770225525,
    "energy_efficiency": 0.5555996298789978,
    "faradaic_efficiency": 0.5146855115890503,
    "ohmic_efficiency": 0.9386242628097534,
    "pH_normalized": 0.2320990413427353,
    "precipitation_signal": 0.9976252913475037,
    "safety_risk": 0.072194404900074,
    "score": 0.4395139217376709,
    "selective_product_yield": 0.05556086450815201,
    "transport_efficiency": 0.49000218510627747
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
    "cost": 0.3579599857330322,
    "electrochemical_conversion": 0.0997890755534172,
    "electrochemical_selectivity": 0.9860008955001831,
    "energy_efficiency": 0.5481169819831848,
    "faradaic_efficiency": 0.4815601408481598,
    "ohmic_efficiency": 0.9701858162879944,
    "pH_normalized": 0.23111364245414734,
    "precipitation_signal": 0.9826673865318298,
    "safety_risk": 0.072194404900074,
    "score": 0.45269569754600525,
    "selective_product_yield": 0.09566989541053772,
    "transport_efficiency": 0.48496049642562866
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
    "cost": 0.36371999979019165,
    "electrochemical_conversion": 0.1658622920513153,
    "electrochemical_selectivity": 0.9826774597167969,
    "energy_efficiency": 0.5189814567565918,
    "faradaic_efficiency": 0.4660162627696991,
    "ohmic_efficiency": 0.955481767654419,
    "pH_normalized": 0.229416161775589,
    "precipitation_signal": 0.995540201663971,
    "safety_risk": 0.072194404900074,
    "score": 0.4645552635192871,
    "selective_product_yield": 0.14802537858486176,
    "transport_efficiency": 0.4595209062099457
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
    "cost": 0.3957200050354004,
    "electrochemical_conversion": 0.2807636857032776,
    "electrochemical_selectivity": 0.7826850414276123,
    "energy_efficiency": 0.765027642250061,
    "faradaic_efficiency": 0.7489309310913086,
    "ohmic_efficiency": 0.956113874912262,
    "pH_normalized": 0.2331753969192505,
    "precipitation_signal": 0.9993284940719604,
    "safety_risk": 0.09559440612792969,
    "score": 0.575886070728302,
    "selective_product_yield": 0.2410525530576706,
    "transport_efficiency": 0.7697622179985046
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
      "solvent": 2,
      "volume_L": 0.08
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
    "cost": 0.4469200074672699,
    "electrochemical_conversion": 0.20204512774944305,
    "electrochemical_selectivity": 0.7220774292945862,
    "energy_efficiency": 0.485964834690094,
    "faradaic_efficiency": 0.5093450546264648,
    "ohmic_efficiency": 0.9066917300224304,
    "pH_normalized": 0.2472575455904007,
    "precipitation_signal": 0.9823437333106995,
    "safety_risk": 0.1135944053530693,
    "score": 0.42477795481681824,
    "selective_product_yield": 0.12880294024944305,
    "transport_efficiency": 0.5106946229934692
  }
}
```

### 批次 11 · 终点事件 78

```json
{
  "ordinal": 11,
  "lifecycle_index": 11,
  "end_step": 78,
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
    "cost": 0.42524001002311707,
    "electrochemical_conversion": 0.23284941911697388,
    "electrochemical_selectivity": 0.7232131958007812,
    "energy_efficiency": 0.4613102078437805,
    "faradaic_efficiency": 0.4657806158065796,
    "ohmic_efficiency": 0.9290430545806885,
    "pH_normalized": 0.23184628784656525,
    "precipitation_signal": 0.9963794946670532,
    "safety_risk": 0.09559440612792969,
    "score": 0.42712298035621643,
    "selective_product_yield": 0.16215449571609497,
    "transport_efficiency": 0.47296056151390076
  }
}
```

### 批次 12 · 终点事件 85

```json
{
  "ordinal": 12,
  "lifecycle_index": 12,
  "end_step": 85,
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
      "current_mA": 300,
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
    "cost": 0.4014799892902374,
    "electrochemical_conversion": 0.2662571668624878,
    "electrochemical_selectivity": 0.7811020016670227,
    "energy_efficiency": 0.512912392616272,
    "faradaic_efficiency": 0.4709441363811493,
    "ohmic_efficiency": 0.9055889844894409,
    "pH_normalized": 0.23236660659313202,
    "precipitation_signal": 0.9897154569625854,
    "safety_risk": 0.09559440612792969,
    "score": 0.469928115606308,
    "selective_product_yield": 0.23674307763576508,
    "transport_efficiency": 0.4921690821647644
  }
}
```

## K1 封存报告

## Mechanistic account

I interpret this benchmark as a charge-driven electrochemical conversion with three coupled limitations: electrode kinetics/selectivity, mass transport, and electrical/energetic loss. The measured target yield is governed not simply by nominal charge, but by how much productive current reaches the reactant before transport limitation, passivation, depletion, or degradation becomes important.

A useful conceptual model is

- effective overpotential: `eta = V_applied - E0_effective(solvent,electrolyte,pH) - i*R_effective`;
- productive rate: `r_target ≈ I_effective*FE*selectivity/(nF)`;
- transport ceiling: `I_effective <= I_lim`, with `I_lim` increasing with diffusivity and decreasing with diffusion-layer thickness;
- accumulated conversion: `dX/dt = productive conversion - loss/passivation terms`;
- target yield: approximately conversion times product selectivity, with assay noise and possibly different internal definitions preventing exact equality;
- energy efficiency: reduced by excessive overpotential, resistance, nonfaradaic current, and unproductive reactions.

The public score is the declared weighted sum of conversion, selectivity, yield, faradaic, transport, ohmic, and energy efficiencies. The observations are consistent with the public 0.02 yield gate acting as a proportional penalty below 0.02: for example, batch 2 had yield 0.01667 and a score lower than its ungated weighted sum by approximately `0.01667/0.02`. Once yield exceeded 0.02, the reported scores closely followed the weighted sum.

## Polarity and potential

Polarity was the first decisive variable. Batch 1 used S0/E0, -1.0 V, a 200 mA cap, and 600 s. Its final assay found conversion 0.01443, selectivity 0.6482, faradaic efficiency 0.4370, transport efficiency 0.4083, energy efficiency 0.3096, but zero selective-product yield and therefore zero score. Batch 2 used the otherwise matched +1.0 V condition. It produced yield 0.01667, selectivity 0.9982, faradaic efficiency 0.5001, transport efficiency 0.5264, energy efficiency 0.5586, and score 0.3552. The assay conversion estimate in batch 2 was clipped to zero despite nonzero yield, so I regard that particular conversion value as a noisy boundary estimate rather than evidence of literally zero reaction.

Thus the productive electrode reaction requires positive rather than negative polarization in the tested convention. The sign reversal also changed selectivity and energetic performance, not merely total conversion. I infer that positive overpotential activates the target electron-transfer direction, whereas negative polarization either drives the reverse/competing chemistry or fails to access the target pathway.

The data do not locate a continuous potential optimum. Only +1.0 V was well explored under comparable conditions. Batch 3 at +1.5 V also changed electrolyte, current cap, and duration, so it cannot isolate the potential effect. Its collapse nevertheless establishes that the combined high-drive regime was unsuitable: S0/E1, +1.5 V, 500 mA, and 7200 s gave zero measured yield, conversion, selectivity, faradaic efficiency, transport efficiency, and energy efficiency, with only ohmic efficiency remaining high at 0.8389. Excess overpotential is therefore a plausible contributor through side reactions or degradation, but this attribution remains conjectural because of the confounding changes.

## Time and charge accumulation

The clearest response series used S0/E0 at +1.0 V with a 200 mA cap:

- Batch 2, 600 s: yield 0.01667; score 0.3552.
- Batch 5, 1800 s: yield 0.03134; conversion 0.02660; score 0.4277.
- Batch 6, 3600 s: yield 0.05556; conversion 0.04792; score 0.4395.
- Batch 7, 7200 s: yield 0.09567; conversion 0.09979; score 0.4527.
- Batch 8, 14,400 s: yield 0.14803; conversion 0.16586; score 0.4646.

Over this interval, accumulated productive conversion increased with time, while selectivity stayed very high: 0.9946, 0.9924, 0.9860, and 0.9827 in batches 5–8. Faradaic efficiency declined moderately at long time, from about 0.515 in batch 6 to 0.466 in batch 8; transport efficiency declined from about 0.490 to 0.460. This is consistent with gradual substrate depletion, concentration polarization, electrode fouling, or increasing competition from secondary reactions. Nevertheless, through 14,400 s the gain in yield outweighed the efficiency losses in the balanced score.

Time was not globally monotonic. Batch 9 used the superior S1/E0 medium at +1.0 V, 200 mA, for 14,400 s and reached yield 0.24105 and score 0.57589. Batch 11 used the same nominal recipe and settings but two consecutive 14,400 s electrolysis segments, totaling 28,800 s. Its yield fell to 0.16215, conversion to 0.23285, faradaic efficiency to 0.4658, transport efficiency to 0.4730, energy efficiency to 0.4613, and score to 0.4271. This large deterioration is much greater than the stated final-assay noise scales. It suggests that the second segment entered an unproductive regime involving passivation, reactant depletion, target destruction, or accumulated side products. Because there was no final assay at the segment boundary in batch 11, I cannot distinguish destruction of previously formed target from loss of continued production.

A minimal phenomenological model would therefore include a declining active-state variable `a(t)` and possibly product loss:

`dX_target/dt = a(t)*k_prod(eta)*C_reactant*f_transport - k_loss(eta,C_byproduct)*X_target`

`da/dt = -k_pass(eta,i,C_byproduct)*a`

At early and intermediate times the first term dominates; at sufficiently long time, loss/passivation dominates.

## Current cap and transport coupling

The current entry appears to act as a cap rather than proof that the stated current was continuously delivered. Actual current was not observed, so charge cannot be calculated reliably as `cap*time`.

The best comparison of cap used S1/E0, +1.0 V, and 14,400 s. Batch 9 at 200 mA produced conversion 0.28076, yield 0.24105, faradaic efficiency 0.7489, transport efficiency 0.7698, energy efficiency 0.7650, ohmic efficiency 0.9561, and score 0.57589. Batch 12 at 300 mA produced similar conversion and yield—0.26626 and 0.23674—but faradaic, transport, and energy efficiencies fell to 0.4709, 0.4922, and 0.5129; ohmic efficiency fell to 0.9056, and score fell to 0.46993. Selectivity was nearly unchanged, 0.7827 versus 0.7811.

This pattern suggests that the additional allowed current was largely unproductive. A plausible relationship is

`FE(i) ≈ FE0 / (1 + (i/i_side)^m)`

and

`transport_efficiency ≈ min(1, I_lim/I_demand)`,

with a corresponding energy penalty once current demand approaches or exceeds the transport-supported current. At 300 mA, target production did not rise enough to compensate for the larger fraction of side, charging, or transport-limited current. The unchanged selectivity suggests the cap primarily altered current utilization rather than the relative identity of products once productive conversion occurred.

Batch 4, S0/E3 at +1.0 V, 500 mA, 1800 s, also occupied a poor high-cap regime: yield 0.01298, conversion 0.00974, faradaic efficiency 0.1442, transport efficiency 0.1128, energy efficiency 0.1401, and score 0.1644. However, its different electrolyte prevents a clean current-only conclusion.

## Solvent effects

The most important material result was the matched long-duration solvent comparison at E0, +1.0 V, 200 mA, and 14,400 s:

- Batch 8, S0: conversion 0.16586, yield 0.14803, selectivity 0.98268, FE 0.4660, transport efficiency 0.4595, energy efficiency 0.5190, ohmic efficiency 0.9555, score 0.46456.
- Batch 9, S1: conversion 0.28076, yield 0.24105, selectivity 0.78269, FE 0.7489, transport efficiency 0.7698, energy efficiency 0.7650, ohmic efficiency 0.9561, score 0.57589.
- Batch 10, S2: conversion 0.20205, yield 0.12880, selectivity 0.72208, FE 0.5093, transport efficiency 0.5107, energy efficiency 0.4860, ohmic efficiency 0.9067, score 0.42478.

S1 did not win by maximizing selectivity; S0 was substantially more selective. S1 instead produced a large coupled improvement in conversion, faradaic efficiency, transport efficiency, and energy efficiency while maintaining essentially the same high ohmic efficiency as S0. The nominal dossier gives S1 higher relative diffusivity (1.25 versus 0.78 for S0), lower relative conductivity (0.7 versus 1.2), lower proton activity, and a +0.02 V potential shift rather than -0.08 V. The observations therefore suggest that mass transport, solvation, proton activity, or a hidden interfacial residual mattered more than bulk conductivity alone. The nearly identical ohmic efficiencies of batches 8 and 9 argue against resistance as the principal source of S1's advantage.

S2, with still lower nominal proton activity and a +0.20 V shift, did not reproduce S1's advantage. It had poorer selectivity and efficiencies. Hence neither lower proton activity nor a positive potential shift alone explains S1. I favor a solvent-specific coupling among diffusivity, solvation of reactant/intermediate, and the electrode interface. The public dossier explicitly allows fixed hidden transport, solvation, and interface residuals, so an S1-specific residual is a plausible alternative to a simple nominal-property law.

## Electrolyte, pH, and precipitation

The campaign did not provide an unconfounded electrolyte comparison. E0 was used in nearly every informative batch. E1 appeared only in the simultaneously high-potential/high-cap batch 3, and E3 appeared only in high-cap batch 4. Consequently, electrolyte-specific rate, selectivity, conductivity, and potential-shift effects are not identifiable from these experiments.

The normalized pH values in most E0 final assays were tightly clustered near 0.23: for example, 0.2294 in batch 8, 0.2332 in batch 9, 0.2318 in batch 11, and 0.2324 in batch 12. Batch 3/E1 was lower at 0.2027, while batch 4/E3 was higher at 0.2700. These differences are compatible with the nominal acid properties, but electrolyte was confounded with operating condition. No causal pH optimum can be claimed.

E0 batches generally showed precipitation signals near one, including 0.9955 in batch 8, 0.9993 in batch 9, 0.9823 in batch 10, 0.9964 in batch 11, and 0.9897 in batch 12. Batch 4/E3 showed zero precipitation signal. Despite severe precipitation signal, batch 9 was the best run. Precipitation therefore was not an immediate disqualifier and is not directly weighted in the declared score. It could nevertheless participate in passivation or long-time loss, particularly the decline in batch 11. That proposed coupling is plausible but unproven because precipitation remained high in both the successful 14,400 s and unsuccessful 28,800 s S1/E0 runs.

## Ohmic behavior and safety

Ohmic efficiency was generally high, about 0.91–0.97 in the useful runs. It varied less than faradaic and transport efficiencies and therefore was not the dominant discriminator. For example, batches 8 and 9 had almost identical ohmic efficiencies but very different scores. The high-cap batch 12 reduced ohmic efficiency modestly, consistent with a larger `iR` loss, but its largest penalties were faradaic, transport, and energy efficiency.

The visible safety risk after charging the standard recipe was approximately 0.0722 in the reported batches, well below the 0.65 limit, and electrolysis did not visibly increase it. This only supports safety within the simulator's observed metric and tested recipe; it does not identify which physical hazards are represented.

## How the explanation changed

1. Batches 1 and 2 established productive polarity and rejected an initially symmetric view of positive and negative operation.
2. Batches 5–8 established a time-dependent accumulation regime at S0/E0 and initially suggested that the longest available duration was best.
3. Batch 9 changed the material explanation: nominal conductivity was not sufficient, because S1 greatly improved transport, faradaic, and energy efficiencies despite lower nominal conductivity and lower product selectivity.
4. Batch 10 showed that reducing proton activity or shifting potential further positive was not by itself beneficial.
5. Batch 11 overturned any global monotonic-time hypothesis by showing severe deterioration at 28,800 s.
6. Batch 12 showed that more current capacity was also not monotonically beneficial; the 200 mA cap was better balanced than 300 mA in S1/E0.

## Scope and unresolved alternatives

The strongest claims apply only near the tested standard loading of 0.040 mol reagent in 0.080 L solvent and to the fixed world-specific electrode geometry and contact resistance. Concentration and volume were not varied, so kinetic order, diffusion scaling with concentration, and electrode-area-normalized current density are unknown.

All principal conditions were assayed once. Differences much larger than the declared instrument noise—especially the batch 9 versus batch 8 efficiency changes and the batch 11 decline—are persuasive within this world, but process repeatability was not measured. The observed estimates also include clipping, as illustrated by batch 2's zero conversion estimate alongside nonzero yield.

Actual current, cell voltage under load, charge passed, temperature trajectories, electrode area, and hidden species concentrations were not observed. Therefore kinetic constants, electron stoichiometry, limiting current, resistance, and passivation constants cannot be separately estimated. Several mechanisms remain observationally equivalent:

- reactant depletion versus electrode passivation for the long-time decline;
- target destruction versus cessation of target formation in batch 11;
- solvent-enhanced diffusion versus favorable solvation/interfacial kinetics for S1;
- parasitic faradaic chemistry versus double-layer charging under high current;
- precipitation-induced fouling versus unrelated time-dependent degradation.

The assay precipitation and pH channels provide suggestive context but not identification. E1 and E3 effects are especially confounded with potential and current.

## Overall working mechanism

My best account is that positive polarization near +1.0 V activates a highly selective target pathway. At moderate current demand, target accumulates approximately with productive charge. The current that can be used productively is capped by solvent- and electrolyte-dependent transport plus interface kinetics. S1/E0 has a favorable world-specific coupling that supports high faradaic and transport efficiencies at 200 mA, even though its intrinsic product selectivity is lower than S0/E0. Raising the current cap pushes the cell toward transport limitation and parasitic current, while extending electrolysis far beyond 14,400 s moves it into a passivated, depleted, or product-loss regime. The balanced optimum consequently lies at an intermediate potential/current/time rather than at maximum electrical drive or maximum duration. Among tested experiments, batch 9 best occupied that regime.

## K2 封存报告

1. **Supported, contradicted, and untested claims**

No instance-specific prior or proposed answer was supplied. The material dossier supplied nominal properties and qualitative cautions, but explicitly did not provide an objective ranking or a complete response law.

**Supported:**
- My proposed polarity law—positive polarization accesses the target pathway, while negative polarization does not—was supported by batches 1 and 2. At otherwise matched S0/E0, 200 mA, 600 s conditions, batch 1 at −1.0 V had zero selective-product yield and zero score, whereas batch 2 at +1.0 V had yield 0.01667 and score 0.3552.
- The initial finite-time accumulation law was supported locally by batches 2, 5, 6, 7, and 8. At S0/E0, +1.0 V, and 200 mA, increasing duration from 600 to 14,400 s raised yield from 0.01667 to 0.14803 and score from 0.3552 to 0.4646, while selectivity remained above 0.98 in the longer runs.
- The claim that transport and faradaic utilization, rather than bulk ohmic efficiency alone, control performance was supported by batch 9. Compared with matched batch 8, changing S0 to S1 raised faradaic efficiency from 0.4660 to 0.7489 and transport efficiency from 0.4595 to 0.7698, while ohmic efficiency was essentially unchanged, 0.9555 versus 0.9561. The score increased from 0.4646 to 0.5759.
- The law that increasing the current cap can reduce balanced performance was supported by batches 9 and 12. Raising the cap from 200 to 300 mA under otherwise matched S1/E0 conditions barely changed yield, 0.24105 to 0.23674, but lowered faradaic, transport, and energy efficiencies and reduced score to 0.4699.
- The public low-yield score gate was consistent with batches 2 and 4: their scores were approximately their weighted component sums multiplied by yield divided by 0.02.

**Contradicted or narrowed:**
- A globally monotonic duration law was contradicted by batch 11. Doubling the batch-9 electrolysis time from 14,400 to 28,800 s reduced yield from 0.24105 to 0.16215 and score from 0.5759 to 0.4271. This changed my judgment from “longer is better over the explored range” to a peaked response involving depletion, passivation, target loss, or another time-dependent penalty.
- A simple nominal-conductivity ranking was contradicted by batches 8 and 9. S1 had lower declared relative conductivity than S0 but substantially better transport, faradaic, and energy efficiencies. Conductivity alone therefore could not explain the solvent ranking.
- A simple “lower proton activity is better” interpretation was not supported. Batch 10 using S2 did not reproduce the S1 advantage and scored only 0.4248.

**Untested or unidentifiable:**
- The continuous potential optimum was not established. +1.0 V was explored repeatedly, but the +1.5 V batch also changed electrolyte and cap, and no clean potential series was run.
- Electrolyte effects were not independently identified. Batch 3/E1 and batch 4/E3 differed simultaneously in several operating variables from the E0 experiments.
- The campaign could not separate reactant depletion, reversible concentration polarization, electrode passivation, and target destruction as causes of batch 11’s decline.
- Kinetic order, electron stoichiometry, actual delivered current, electrode-area-normalized current density, and resistance were untested or unobservable.
- Whether the near-unity precipitation signal caused long-time fouling remained untested. It accompanied both successful batch 9 and deteriorated batch 11.

The largest changes in judgment came from batch 2 establishing productive polarity, batch 9 overturning the nominal-conductivity expectation, batch 11 contradicting monotonic time benefit, and batch 12 showing that additional current capacity was mostly unproductive.

2. **One additional discriminating experiment**

I would exactly replicate batch 9—0.040 mol reagent, 0.080 L S1, E0, +1.0 V, 200 mA cap, and 14,400 s—with a predeclared comparison against the batch-9 assay values. This would distinguish my leading explanation, a reproducible S1-dependent transport/interfacial advantage, from the important alternative that batch 9 was an unusually favorable single process realization or assay fluctuation.

- If the replicate again produced faradaic and transport efficiencies near 0.75, yield near 0.24, and a score clearly above the matched S0 result from batch 8, I would strengthen the claim that S1 has a real fixed coupling advantage in this world.
- If it instead resembled batch 8—efficiencies near 0.46–0.52 and score near 0.46—I would substantially weaken both the S1 mechanism and the recommendation, treating batch 9 as non-reproducible.
- If yield repeated but efficiencies did not, I would suspect covariance or inconsistency among processed assay channels rather than a simple transport mechanism.
- If efficiencies repeated but yield did not, I would infer that product formation or stability has an additional variable not captured by the efficiency channels.

This replicate would not by itself distinguish diffusion from interfacial solvation. After establishing reproducibility, that distinction would require a designed current/concentration series across both S0 and S1.

3. **Unused evidence, reliability, and goal effects**

I did not analyze the raw UV–visible spectra or final-assay spectral packets; decisions used their processed estimates. I also did not use a pH meter, so pH evidence came only from final assays. Cost and safety observations were monitored but contributed little to mechanism inference because safety stayed far below its limit and varied little after preparation. Precipitation and normalized-pH channels were noted but not systematically varied. Several nominal dossier properties—capacitance, salt concentration, solubility product, and diffusion-layer thickness—could not be separated experimentally. Actual current and charge passed were unavailable, so the current settings were treated as caps rather than measured currents.

The least reliable predictions are those for E1 and E3 (Q05–Q08), because those electrolytes were observed only under heavily confounded conditions; the 500 mA cases (Q11–Q12), because high-cap behavior was sparse and nonlinear; and the long negative-polarity cases, because only one short negative run was performed. All blind predictions also extrapolate from +1.0/−1.0 V to ±0.8 V and from 0.040 mol in 0.080 L to 0.012 mol in 0.025 L. The batch-9 recommendation itself is less secure than its numerical lead suggests because it rests on one realization rather than a replicate.

The assigned optimization goal did affect evidence collection. After identifying a promising S1/E0 condition, I used the remaining batches to test longer time and higher current rather than performing replicates or a balanced factorial study. This was reasonable for maximizing the public score, but it left electrolyte, potential, and mechanistic interactions confounded. There was no direct conflict between the optimization goal and using mechanistic evidence, but optimization took priority over precise causal identification.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.68,
        "lower80": 0.48,
        "upper80": 0.82
      },
      "energy_efficiency": {
        "estimate": 0.38,
        "lower80": 0.22,
        "upper80": 0.52
      },
      "faradaic_efficiency": {
        "estimate": 0.46,
        "lower80": 0.32,
        "upper80": 0.58
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.12
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0.0,
        "upper80": 0.01
      },
      "transport_efficiency": {
        "estimate": 0.52,
        "lower80": 0.35,
        "upper80": 0.68
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.995,
        "lower80": 0.94,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.67,
        "lower80": 0.55,
        "upper80": 0.77
      },
      "faradaic_efficiency": {
        "estimate": 0.58,
        "lower80": 0.46,
        "upper80": 0.68
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.473,
        "lower80": 0.39,
        "upper80": 0.55
      },
      "selective_product_yield": {
        "estimate": 0.026,
        "lower80": 0.014,
        "upper80": 0.045
      },
      "transport_efficiency": {
        "estimate": 0.66,
        "lower80": 0.54,
        "upper80": 0.76
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.3,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.28,
        "lower80": 0.12,
        "upper80": 0.42
      },
      "faradaic_efficiency": {
        "estimate": 0.38,
        "lower80": 0.2,
        "upper80": 0.52
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.05,
        "lower80": 0.0,
        "upper80": 0.15
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.02
      },
      "transport_efficiency": {
        "estimate": 0.45,
        "lower80": 0.25,
        "upper80": 0.62
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.97,
        "lower80": 0.91,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.63,
        "lower80": 0.51,
        "upper80": 0.74
      },
      "faradaic_efficiency": {
        "estimate": 0.54,
        "lower80": 0.42,
        "upper80": 0.66
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.51,
        "lower80": 0.42,
        "upper80": 0.59
      },
      "selective_product_yield": {
        "estimate": 0.16,
        "lower80": 0.11,
        "upper80": 0.22
      },
      "transport_efficiency": {
        "estimate": 0.62,
        "lower80": 0.49,
        "upper80": 0.73
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.45,
        "lower80": 0.2,
        "upper80": 0.7
      },
      "energy_efficiency": {
        "estimate": 0.22,
        "lower80": 0.08,
        "upper80": 0.4
      },
      "faradaic_efficiency": {
        "estimate": 0.3,
        "lower80": 0.12,
        "upper80": 0.48
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.027,
        "lower80": 0.0,
        "upper80": 0.13
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.55,
        "lower80": 0.3,
        "upper80": 0.75
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.86,
        "lower80": 0.68,
        "upper80": 0.97
      },
      "energy_efficiency": {
        "estimate": 0.72,
        "lower80": 0.5,
        "upper80": 0.85
      },
      "faradaic_efficiency": {
        "estimate": 0.65,
        "lower80": 0.42,
        "upper80": 0.78
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.527,
        "lower80": 0.39,
        "upper80": 0.62
      },
      "selective_product_yield": {
        "estimate": 0.14,
        "lower80": 0.08,
        "upper80": 0.21
      },
      "transport_efficiency": {
        "estimate": 0.78,
        "lower80": 0.55,
        "upper80": 0.9
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.35,
        "lower80": 0.12,
        "upper80": 0.6
      },
      "energy_efficiency": {
        "estimate": 0.18,
        "lower80": 0.04,
        "upper80": 0.38
      },
      "faradaic_efficiency": {
        "estimate": 0.28,
        "lower80": 0.08,
        "upper80": 0.47
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0.0,
        "upper80": 0.01
      },
      "transport_efficiency": {
        "estimate": 0.3,
        "lower80": 0.1,
        "upper80": 0.54
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.9,
        "lower80": 0.72,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.5,
        "lower80": 0.3,
        "upper80": 0.7
      },
      "faradaic_efficiency": {
        "estimate": 0.48,
        "lower80": 0.25,
        "upper80": 0.66
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.417,
        "lower80": 0.28,
        "upper80": 0.51
      },
      "selective_product_yield": {
        "estimate": 0.07,
        "lower80": 0.03,
        "upper80": 0.13
      },
      "transport_efficiency": {
        "estimate": 0.42,
        "lower80": 0.22,
        "upper80": 0.65
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.45,
        "lower80": 0.2,
        "upper80": 0.68
      },
      "energy_efficiency": {
        "estimate": 0.3,
        "lower80": 0.12,
        "upper80": 0.49
      },
      "faradaic_efficiency": {
        "estimate": 0.38,
        "lower80": 0.18,
        "upper80": 0.56
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.022,
        "lower80": 0.0,
        "upper80": 0.11
      },
      "selective_product_yield": {
        "estimate": 0.0015,
        "lower80": 0.0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.48,
        "lower80": 0.27,
        "upper80": 0.66
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.74,
        "lower80": 0.55,
        "upper80": 0.9
      },
      "energy_efficiency": {
        "estimate": 0.55,
        "lower80": 0.36,
        "upper80": 0.71
      },
      "faradaic_efficiency": {
        "estimate": 0.55,
        "lower80": 0.38,
        "upper80": 0.69
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.447,
        "lower80": 0.32,
        "upper80": 0.53
      },
      "selective_product_yield": {
        "estimate": 0.13,
        "lower80": 0.07,
        "upper80": 0.2
      },
      "transport_efficiency": {
        "estimate": 0.57,
        "lower80": 0.39,
        "upper80": 0.72
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.25,
        "lower80": 0.05,
        "upper80": 0.5
      },
      "energy_efficiency": {
        "estimate": 0.05,
        "lower80": 0.0,
        "upper80": 0.18
      },
      "faradaic_efficiency": {
        "estimate": 0.08,
        "lower80": 0.0,
        "upper80": 0.22
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "selective_product_yield": {
        "estimate": 0.0005,
        "lower80": 0.0,
        "upper80": 0.006
      },
      "transport_efficiency": {
        "estimate": 0.05,
        "lower80": 0.0,
        "upper80": 0.2
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.92,
        "lower80": 0.68,
        "upper80": 0.99
      },
      "energy_efficiency": {
        "estimate": 0.28,
        "lower80": 0.08,
        "upper80": 0.52
      },
      "faradaic_efficiency": {
        "estimate": 0.25,
        "lower80": 0.08,
        "upper80": 0.48
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.34,
        "lower80": 0.18,
        "upper80": 0.46
      },
      "selective_product_yield": {
        "estimate": 0.09,
        "lower80": 0.03,
        "upper80": 0.16
      },
      "transport_efficiency": {
        "estimate": 0.2,
        "lower80": 0.05,
        "upper80": 0.42
      }
    }
  ],
  "rationale": "Predictions interpolate the campaign's S0/E0 polarity and duration series while adjusting for the nearly matched 0.48 M loading. Positive polarization is expected to remain productive and highly selective; negative polarization is assigned near-zero target yield and a strong yield-gate penalty. Lower current should improve transport and energy utilization, whereas the 500 mA cases are widened and down-weighted for transport-limited or parasitic current. Electrolyte and S2 estimates have broader intervals because those effects were confounded or sparsely sampled in the campaign."
}
```
