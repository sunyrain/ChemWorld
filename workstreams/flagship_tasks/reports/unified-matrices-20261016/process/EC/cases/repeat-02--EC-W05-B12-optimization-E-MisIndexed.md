# repeat-02/EC-W05-B12-optimization-E-MisIndexed

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-02\EC-W05-B12-optimization-E-MisIndexed\participant\optimization-E-MisIndexed

## 同期笔记

### v1 · 公开事件 0

# Electrochemical campaign hypotheses

## H1 [tentative; pre-experiment]
At fixed 0.04 mol reagent in 0.08 L solvent, productive conversion should show a potential window: insufficient magnitude gives low conversion, while excessive magnitude or duration sacrifices selectivity/energy efficiency. I will test both signs and span magnitudes/durations.

## H2 [tentative; pre-experiment]
Transport and ohmic efficiency should improve with higher nominal conductivity, but selectivity may depend on interfacial/solvation factors; therefore S0/E0 or S0/E3 are prior candidates, not assumed winners. Material evidence will override this prior.

## H3 [tentative; pre-experiment]
Current cap may be inactive when above cell-delivered current. Paired cap/duration comparisons near the best condition will distinguish charge limitation from a true plateau.

Decision plan: use early batches for broad sign/material/potential screening, then concentrate later batches around the best public score and check local repeatability. A score difference comparable to stated assay noise will be treated as unresolved rather than decisive.

### v2 · 公开事件 85

# Electrochemical campaign hypotheses — final source-stage revision

## H1 [supported in tested scope]
The productive polarity is negative under S0/E0 at 0.04 mol in 0.08 L. At +1.2 V the assay was effectively unproductive (runner-operation-0007), whereas -1.2 V gave measurable yield and score (runner-operation-0014). This is strong within-condition polarity evidence, though the exact onset can shift with materials.

## H2 [supported locally; non-monotone potential response]
For S0/E0, 100 mA cap and 14,400 s, balanced performance improved as potential moved from -1.2 toward -0.3 V: scores were about 0.307, 0.337, 0.386, 0.429, and 0.445 at -1.2, -0.9, -0.7, -0.5, and -0.3 V (runner-operation-0014, -0028, -0035, -0042, -0049). At -0.1 V score fell to about 0.419 (runner-operation-0056), supporting a local optimum near -0.3 V rather than monotonic improvement. Assay noise makes fine localization unresolved; a narrower potential grid would be needed.

## H3 [supported in tested comparison]
At -1.2 V, raising the cap from 100 to 500 mA increased conversion/yield but reduced faradaic, transport, ohmic, and energy efficiencies enough to lower the balanced score (runner-operation-0014 versus -0021). Thus the current cap can be active, and maximum current is not optimal for the balanced objective.

## H4 [supported for the tested material comparison]
At -0.3 V, 100 mA, 14,400 s with S0, E0 outscored E1, E2, and E3 (runner-operation-0049 versus -0063, -0070, -0077). This ranking is conditional on common applied potential; electrolyte-dependent potential shifts mean it is not proof that each alternative was individually optimized.

## H5 [supported; recommendation basis]
Repeating the -0.3 V electrolysis for a total of 28,800 s under S0/E0 increased conversion and selective yield while retaining good efficiencies, producing the campaign-best score about 0.491 (runner-operation-0085). The comparison to the single 14,400 s run is not a replicate and is consistent with a duration effect; its quantitative size remains subject to assay noise and possible run variability.

Recommended tested procedure: 0.04 mol reagent, 0.08 L S0, E0, -0.3 V, 100 mA cap, two 14,400 s electrolysis segments (28,800 s total), then terminate and assay. I would change this decision if replication showed the score advantage over the 14,400 s condition was not reproducible, or if a local potential/material optimization exceeded it.

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
    "cost": 0.3591119945049286,
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
    "cost": 0.3591119945049286,
    "electrochemical_conversion": 0.06132001057267189,
    "electrochemical_selectivity": 0.6156089305877686,
    "energy_efficiency": 0.20381268858909607,
    "faradaic_efficiency": 0.3716629445552826,
    "ohmic_efficiency": 0.9741578102111816,
    "pH_normalized": 0.2303897738456726,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.30666518211364746,
    "selective_product_yield": 0.0509859174489975,
    "transport_efficiency": 0.39791974425315857
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
    "cost": 0.38675999641418457,
    "electrochemical_conversion": 0.16531947255134583,
    "electrochemical_selectivity": 0.6092459559440613,
    "energy_efficiency": 0.1037076935172081,
    "faradaic_efficiency": 0.15552355349063873,
    "ohmic_efficiency": 0.8587707281112671,
    "pH_normalized": 0.231104776263237,
    "precipitation_signal": 0.9869203567504883,
    "safety_risk": 0.072194404900074,
    "score": 0.256708562374115,
    "selective_product_yield": 0.09553676098585129,
    "transport_efficiency": 0.17208045721054077
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
      "current_mA": 100,
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
    "cost": 0.35738399624824524,
    "electrochemical_conversion": 0.0756063312292099,
    "electrochemical_selectivity": 0.6191945672035217,
    "energy_efficiency": 0.3150472939014435,
    "faradaic_efficiency": 0.453803151845932,
    "ohmic_efficiency": 0.9645761847496033,
    "pH_normalized": 0.23041419684886932,
    "precipitation_signal": 0.9876685738563538,
    "safety_risk": 0.072194404900074,
    "score": 0.3372182846069336,
    "selective_product_yield": 0.052224431186914444,
    "transport_efficiency": 0.4223155975341797
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
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -0.7
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
    "cost": 0.3562319874763489,
    "electrochemical_conversion": 0.09031547605991364,
    "electrochemical_selectivity": 0.6841302514076233,
    "energy_efficiency": 0.4936274588108063,
    "faradaic_efficiency": 0.476654052734375,
    "ohmic_efficiency": 0.9542807936668396,
    "pH_normalized": 0.23537498712539673,
    "precipitation_signal": 0.9869949817657471,
    "safety_risk": 0.072194404900074,
    "score": 0.38605090975761414,
    "selective_product_yield": 0.06733430176973343,
    "transport_efficiency": 0.4661445915699005
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
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -0.5
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
    "cost": 0.3550800085067749,
    "electrochemical_conversion": 0.09719819575548172,
    "electrochemical_selectivity": 0.7131296992301941,
    "energy_efficiency": 0.6601400971412659,
    "faradaic_efficiency": 0.5335361361503601,
    "ohmic_efficiency": 0.9386242628097534,
    "pH_normalized": 0.2320990413427353,
    "precipitation_signal": 0.9976252913475037,
    "safety_risk": 0.072194404900074,
    "score": 0.42902427911758423,
    "selective_product_yield": 0.07771478593349457,
    "transport_efficiency": 0.5088527798652649
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
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -0.3
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
    "cost": 0.35392799973487854,
    "electrochemical_conversion": 0.11435122787952423,
    "electrochemical_selectivity": 0.7393480539321899,
    "energy_efficiency": 0.6658192276954651,
    "faradaic_efficiency": 0.5596175789833069,
    "ohmic_efficiency": 0.9293215274810791,
    "pH_normalized": 0.23111364245414734,
    "precipitation_signal": 0.9826673865318298,
    "safety_risk": 0.072194404900074,
    "score": 0.4453343451023102,
    "selective_product_yield": 0.08440835028886795,
    "transport_efficiency": 0.5630179047584534
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
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -0.1
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
    "cost": 0.3527759909629822,
    "electrochemical_conversion": 0.10878129303455353,
    "electrochemical_selectivity": 0.7701550126075745,
    "energy_efficiency": 0.5333543419837952,
    "faradaic_efficiency": 0.6180099844932556,
    "ohmic_efficiency": 0.7102961540222168,
    "pH_normalized": 0.229416161775589,
    "precipitation_signal": 0.995540201663971,
    "safety_risk": 0.072194404900074,
    "score": 0.41877180337905884,
    "selective_product_yield": 0.06743638962507248,
    "transport_efficiency": 0.6115146279335022
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
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -0.3
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
    "cost": 0.35392799973487854,
    "electrochemical_conversion": 0.08921360969543457,
    "electrochemical_selectivity": 0.6807018518447876,
    "energy_efficiency": 0.6195405125617981,
    "faradaic_efficiency": 0.47975045442581177,
    "ohmic_efficiency": 0.8821706771850586,
    "pH_normalized": 0.20306052267551422,
    "precipitation_signal": 0.8586449027061462,
    "safety_risk": 0.072194404900074,
    "score": 0.4061844050884247,
    "selective_product_yield": 0.0800827145576477,
    "transport_efficiency": 0.5005817413330078
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
      "current_mA": 100,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -0.3
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
    "cost": 0.35392799973487854,
    "electrochemical_conversion": 0.10316310077905655,
    "electrochemical_selectivity": 0.7015961408615112,
    "energy_efficiency": 0.5935003757476807,
    "faradaic_efficiency": 0.4796251058578491,
    "ohmic_efficiency": 0.8372315168380737,
    "pH_normalized": 0.15213987231254578,
    "precipitation_signal": 0.0,
    "safety_risk": 0.072194404900074,
    "score": 0.39445772767066956,
    "selective_product_yield": 0.057486455887556076,
    "transport_efficiency": 0.4809747040271759
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
      "current_mA": 100,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": -0.3
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
    "cost": 0.35392799973487854,
    "electrochemical_conversion": 0.09424985200166702,
    "electrochemical_selectivity": 0.6462005972862244,
    "energy_efficiency": 0.6024711728096008,
    "faradaic_efficiency": 0.4353039562702179,
    "ohmic_efficiency": 0.9029287099838257,
    "pH_normalized": 0.2696843147277832,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.072194404900074,
    "score": 0.3817956745624542,
    "selective_product_yield": 0.05450257286429405,
    "transport_efficiency": 0.4424838721752167
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
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -0.3
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
      "duration_s": 14400,
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
    "cost": 0.3736560046672821,
    "electrochemical_conversion": 0.20796114206314087,
    "electrochemical_selectivity": 0.7533100843429565,
    "energy_efficiency": 0.6816251873970032,
    "faradaic_efficiency": 0.5657294988632202,
    "ohmic_efficiency": 0.9138361215591431,
    "pH_normalized": 0.23060987889766693,
    "precipitation_signal": 0.993804395198822,
    "safety_risk": 0.072194404900074,
    "score": 0.49077045917510986,
    "selective_product_yield": 0.1834806352853775,
    "transport_efficiency": 0.5869544744491577
  }
}
```

## K1 封存报告

Mechanistic report

1. Empirical scope and experimental design

All completed batches used the same initial loading: 0.040 mol of limiting reagent in 0.080 L of solvent-S0, corresponding to a nominal initial concentration of 0.50 mol L^-1. Thus, the campaign identifies behavior only at this loading and in S0; it does not experimentally determine solvent effects or concentration scaling. The variables actually varied were potential polarity and magnitude, current cap, electrolyte profile, and total electrolysis duration.

Batches 1–8 used electrolyte-E0 and mapped the electrical controls. Batch 1 used +1.2 V, a 100 mA cap, and 14,400 s. Batch 2 reversed the potential to -1.2 V at otherwise identical settings. Batch 3 retained -1.2 V but raised the cap to 500 mA. Batches 4–8 used 100 mA and 14,400 s at -0.9, -0.7, -0.5, -0.3, and -0.1 V, respectively. Batches 9–11 compared E1, E2, and E3 with E0 under the common setting -0.3 V, 100 mA, and 14,400 s. Batch 12 repeated the best E0 electrical setting but applied two 14,400 s electrolysis segments, for 28,800 s total.

2. Proposed process picture

I infer that the target is generated by a cathodic electrochemical pathway competing with unproductive charge transfer and possibly chemical or electrode-surface side reactions. A useful qualitative representation is:

R + n e^- -> P_target
R + m e^- -> byproducts
solvent/electrolyte or interfacial species + e^- -> parasitic products

The productive rate probably depends on an effective overpotential rather than applied potential alone. One possible description is

eta_eff = E_applied - E0_eff(electrolyte, solvent, pH, interfacial state) - I R_cell,

with polarity conventions absorbed into E0_eff. The delivered current may then be approximated by

I_delivered = min(I_cap, I_kinetic(eta_eff), I_transport),

and conversion should depend on integrated charge and faradaic allocation:

dX/dt approximately proportional to I_delivered × FE_product / (n F N_R),

subject to depletion, transport, and surface-state effects. Target accumulation also depends on selectivity, but the independently noisy public assay estimates mean that measured selective-product yield should not be forced to equal the numerical product of measured conversion and selectivity.

The balanced score favors neither charge throughput nor conversion alone. Its public components weight selective-product yield most strongly, while also rewarding selectivity, energy efficiency, faradaic efficiency, transport efficiency, ohmic efficiency, and conversion. Consequently, a condition with more current can score worse if its extra conversion is obtained through inefficient or nonselective pathways.

3. Evidence for cathodic polarity

The clearest mechanistic contrast is between batches 1 and 2. At +1.2 V, E0, 100 mA, and 14,400 s, batch 1 was essentially unproductive: final electrochemical conversion was 0.0080, selectivity 0.0103, selective-product yield 0, faradaic efficiency 0.0245, transport efficiency 0, and score 0. The ohmic estimate remained high, about 0.965, showing that good electrical conduction alone was insufficient to create the target.

Reversing only the potential to -1.2 V in batch 2 produced conversion 0.0613, selectivity 0.6156, selective-product yield 0.0510, faradaic efficiency 0.3717, transport efficiency 0.3979, energy efficiency 0.2038, ohmic efficiency 0.9742, and score 0.3067. This strongly supports a cathodic target-forming channel rather than a merely thermal or time-dependent transformation. It also indicates that polarity controls faradaic chemistry much more strongly than it controls bulk ohmic behavior.

I cannot infer an absolute redox potential or electron stoichiometry from these data. The material dossier supplies nominal standard-potential shifts, but the hidden world-specific residuals, reference convention, electrode geometry, and product electron count remain unknown.

4. Potential window and competing reactions

Within S0/E0 at a 100 mA cap and 14,400 s, performance was non-monotonic in applied potential. Moving from -1.2 V toward -0.3 V improved the balanced score:

• Batch 2, -1.2 V: score 0.3067; conversion 0.0613; selectivity 0.6156; yield 0.0510; FE 0.3717; transport 0.3979; energy efficiency 0.2038.
• Batch 4, -0.9 V: score 0.3372; conversion 0.0756; selectivity 0.6192; yield 0.0522; FE 0.4538; transport 0.4223; energy efficiency 0.3150.
• Batch 5, -0.7 V: score 0.3861; conversion 0.0903; selectivity 0.6841; yield 0.0673; FE 0.4767; transport 0.4661; energy efficiency 0.4936.
• Batch 6, -0.5 V: score 0.4290; conversion 0.0972; selectivity 0.7131; yield 0.0777; FE 0.5335; transport 0.5089; energy efficiency 0.6601.
• Batch 7, -0.3 V: score 0.4453; conversion 0.1144; selectivity 0.7393; yield 0.0844; FE 0.5596; transport 0.5630; energy efficiency 0.6658.

A still milder setting was worse:

• Batch 8, -0.1 V: score 0.4188; conversion 0.1088; selectivity 0.7702; yield 0.0674; FE 0.6180; transport 0.6115; energy efficiency 0.5334; ohmic efficiency 0.7103.

These observations suggest a productive window near -0.3 V under the tested conditions. The unusual fact that conversion increased as the potential became less negative from -1.2 to -0.3 V argues against a simple monotonic Butler–Volmer picture for target formation. My leading explanation is that strong cathodic polarization activates parasitic current, concentration polarization, or an inhibiting interfacial state. These processes consume charge and lower FE, transport efficiency, and energy efficiency, and may suppress net target accumulation. Near -0.3 V, the target reaction remains active while the competing channels are less important. At -0.1 V, the higher selectivity and FE suggest cleaner charge allocation, but the lower yield, energy efficiency, and especially lower ohmic estimate show that the cell is becoming insufficiently driven or entering a different current-limited regime.

The precise optimum is not identifiable. Only 0.2 V spacing was used around the best region, and each point was assayed once. Given final-assay standard uncertainties such as 0.010 for conversion, 0.012 for selectivity and FE, 0.016 for energy efficiency, and 0.010 for yield, the data support a broad local window more strongly than an exact optimum of -0.300 V.

5. Current-cap coupling

Batches 2 and 3 isolate the current-cap effect at -1.2 V. Raising the cap from 100 to 500 mA increased conversion from 0.0613 to 0.1653 and selective-product yield from 0.0510 to 0.0955. However, FE fell from 0.3717 to 0.1555, transport efficiency from 0.3979 to 0.1721, energy efficiency from 0.2038 to 0.1037, and ohmic efficiency from 0.9742 to 0.8588. Selectivity stayed similar within the scale of the observations, 0.6156 versus 0.6092. The balanced score therefore fell from 0.3067 to 0.2567.

This shows that the cap was not wholly irrelevant: additional current or charge throughput caused more reaction. But much of that added charge was inefficient. Plausible causes include reagent depletion at the electrode, enlarged concentration gradients, ohmic heating or voltage loss, double-layer charging, hydrogen-like parasitic reduction, or another hidden side reaction. Because temperature, actual current traces, gas evolution, and individual byproducts were not observed, those alternatives cannot be distinguished. The evidence establishes a throughput–efficiency tradeoff, not its microscopic identity.

The cap effect was tested only at -1.2 V. It is an extrapolation, not an observation, to assume that 100 mA is also the optimal cap at -0.3 V. A moderate cap between 100 and 500 mA at -0.3 V might improve the score, but the campaign did not test it.

6. Electrolyte effects and coupling to nominal properties

At the common condition -0.3 V, 100 mA, 14,400 s in S0, E0 was best among the four profiles:

• Batch 7, E0: score 0.4453; conversion 0.1144; selectivity 0.7393; yield 0.0844; FE 0.5596; transport 0.5630; ohmic 0.9293; precipitation signal 0.9827.
• Batch 9, E1: score 0.4062; conversion 0.0892; selectivity 0.6807; yield 0.0801; FE 0.4798; transport 0.5006; ohmic 0.8822; precipitation 0.8586.
• Batch 10, E2: score 0.3945; conversion 0.1032; selectivity 0.7016; yield 0.0575; FE 0.4796; transport 0.4810; ohmic 0.8372; precipitation 0.
• Batch 11, E3: score 0.3818; conversion 0.0943; selectivity 0.6462; yield 0.0545; FE 0.4353; transport 0.4425; ohmic 0.9029; precipitation 0.0052.

The nominal dossier alone does not predict this ordering. E0 has high nominal conductivity but also a thick diffusion layer, low diffusivity, a -0.12 V standard-potential shift, and the strongest nominal precipitation tendency. E3 has the highest nominal conductivity and little predicted precipitation, yet it did not achieve the highest FE, transport efficiency, or score at the shared applied potential. E2 has the largest nominal diffusivity and no observed precipitation signal, but also underperformed E0.

This supports coupled behavior rather than a single-property ranking. Electrolytes may alter effective redox onset, proton activity, supporting-ion concentration, double-layer structure, precipitation, and mass transfer simultaneously. Because the profiles have different nominal standard-potential shifts, a common applied potential does not imply a common effective overpotential. Therefore, the observed ranking means only that E0 was best at the tested common operating point. E1–E3 may have different individually optimized potentials.

Precipitation is especially instructive. E0 showed precipitation signals near one in most relevant assays, yet delivered the best score. E2 and E3 showed essentially none but scored worse. Thus precipitation was not a simple fatal constraint in this world. It may be a spectator equilibrium, a proxy that saturates easily, or a process whose negative transport consequences are outweighed by E0's other interfacial advantages. No solid was isolated or identified, so assigning it a catalytic or passivating role would be conjectural.

The pH-normalized estimates also changed with electrolyte: about 0.231 for E0 in batch 7, 0.203 for E1, 0.152 for E2, and 0.270 for E3. These differences are much larger than the stated pH-normalized assay noise and are consistent with electrolyte-specific acid equilibria. However, pH and electrolyte identity changed together; the campaign cannot determine whether pH directly controls selectivity or is merely correlated with the underlying formulation.

7. Duration and cumulative electrolysis

Batch 12 used the batch-7 condition but doubled total electrolysis time from 14,400 to 28,800 s through two segments. It was the campaign best: score 0.4908, conversion 0.2080, selectivity 0.7533, selective-product yield 0.1835, FE 0.5657, transport efficiency 0.5870, ohmic efficiency 0.9138, and energy efficiency 0.6816. Observed safety risk remained 0.0722.

Relative to batch 7, conversion rose from 0.1144 to 0.2080 and selective yield from 0.0844 to 0.1835, while the efficiency measures remained broadly similar or improved slightly. This is consistent with continued productive charge transfer without severe deactivation over 28,800 s. The conversion increase was somewhat less than exactly twofold, which could reflect depletion, gradual transport limitation, or normal assay/process variation. The yield estimate increased by more than twofold, but because conversion, selectivity, and yield are separately noisy processed estimates, I do not interpret that superlinearity as proof of activation.

The evidence does not establish the eventual optimum duration. Conversion was still only about 0.208 after 28,800 s, so longer operation might continue increasing yield. Conversely, depletion, passivation, side reactions, cost, or energy use could eventually dominate. Batch 12 shows that 28,800 s was better than 14,400 s at this setting; it does not show that 28,800 s is the global temporal optimum.

8. Safety and physical-cost interpretation

All tested batches at the standard 0.040 mol/0.080 L preparation showed observed safety risk near 0.0722, far below the public limit of 0.65. Within this campaign, changing electrical conditions did not visibly raise the reported peak risk. This should not be generalized beyond the tested loading, volume, duration, and bounded synthetic world. The cost differences from electrolysis were comparatively small, while assay and preparation costs contributed materially. The public balanced score itself did not directly reward low cost or low precipitation, although these factors can correlate with scored efficiencies.

9. Unidentifiable factors and plausible alternative models

Several mechanistic quantities remain unidentifiable:

• Electron stoichiometry n and the actual delivered current as a function of time.
• Electrode area, gap, contact resistance, true reference-electrode convention, and local electrode potential.
• Concentration profiles, temperature evolution, gas generation, electrode fouling, and identities of side products.
• The hidden fixed residuals coupling solvent, electrolyte, kinetics, transport, and interface structure.
• Whether the near-optimal potential reflects intrinsic target kinetics, suppression of a side reaction, a surface transition, or a measurement-level composite of all three.
• Solvent dependence, because only S0 was experimentally used.
• Concentration dependence, because all batches used the same initial loading and volume.
• Individual optimum potentials for E1–E3 and the optimum current at -0.3 V.

A plausible alternative to the competing-reaction explanation is that very negative potential changes the electrode surface or precipitate coverage, reducing effective active area. Another is that the cell becomes transport-limited and the extra applied voltage is lost ohmically or in nonproductive double-layer processes. A third is that E0 creates a beneficial interphase despite its high precipitation signal. The available aggregate efficiencies cannot discriminate these possibilities.

10. Consolidated working model and recommendation

My working model is a cathodic target reaction with a finite operating window. At insufficient cathodic drive, target throughput falls. At excessive negative drive or excessive current, parasitic electrochemistry and transport/ohmic losses consume a larger share of charge. Electrolyte identity shifts both the effective redox window and the interfacial/transport response, so nominal conductivity or diffusivity alone is not predictive. Product formation can continue over at least 28,800 s at the best tested setting without a large efficiency collapse.

The sealed recommended batch is batch 12: 0.040 mol reagent in 0.080 L solvent-S0, electrolyte-E0, -0.3 V, 100 mA current cap, and 28,800 s total electrolysis, followed by termination and final assay. This is an empirical recommendation within the tested domain, supported by the campaign-best score of 0.4908. It should not be interpreted as proof of a global optimum. The most valuable unresolved tests, if experiments were available, would be replication of batches 7 and 12, a finer potential grid around -0.3 V, moderate current caps at that potential, longer-duration mapping, electrolyte-specific potential optimization, and solvent/concentration variation.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific prior response law or known optimum was supplied. The only supplied prior was the nominal material dossier, which described properties such as conductivity, diffusivity, acidity, precipitation tendency, capacitance, and potential shifts while explicitly warning that hidden world-specific couplings remained. I therefore treated it as a mechanistic prior rather than ground truth.

My pre-experiment claim that the process would have a finite productive potential window was supported. Batch 1 at +1.2 V was essentially unproductive, whereas batch 2 at -1.2 V produced measurable target. More importantly, batches 2, 4, 5, 6, and 7 showed progressively higher scores as the potential moved from -1.2 to -0.3 V, while batch 8 declined at -0.1 V. The batch-8 reversal changed my judgment from a possible monotonic preference for milder negative potentials to a local-window explanation centered roughly near -0.3 V.

The claim that excessive current could improve throughput while harming balanced efficiency was supported by batches 2 and 3. Raising the cap from 100 to 500 mA at -1.2 V increased conversion and selective yield, but sharply reduced faradaic, transport, energy, and ohmic efficiencies, lowering the score from 0.3067 to 0.2567. This was the clearest evidence that maximum current was not optimal for the stated objective.

The tentative material claim that high nominal conductivity would identify the best electrolyte was contradicted or, more precisely, shown to be incomplete. At the shared -0.3 V condition, E0 in batch 7 outscored E1, E2, and E3 in batches 9–11. E3 had the highest nominal conductivity and little precipitation but did not give the best efficiency or score. The evidence changed my view toward a coupled effective-potential/interfacial model rather than a single-property ranking.

The concern that E0's strong precipitation tendency would necessarily make it inferior was contradicted within the tested scope. Batch 7 had a precipitation signal near one and nevertheless beat the nearly precipitation-free E2 and E3 batches 10 and 11. Whether precipitation was beneficial, passive, or merely correlated remained untested.

The claim that productive electrolysis could continue beyond 14,400 s without a major efficiency collapse was supported by batch 12. Doubling total duration at the batch-7 setting raised conversion from 0.1144 to 0.2080 and selective yield from 0.0844 to 0.1835 while retaining good efficiencies, increasing the score from 0.4453 to 0.4908.

Several important laws remained untested: solvent dependence, concentration scaling, the current-cap response near -0.3 V, durations beyond 28,800 s, electrolyte-specific optimal potentials, repeatability, and whether the observed potential penalty arose from instantaneous side reactions, mass transport, or persistent electrode-surface modification.

2. One additional discriminating experiment

I would run one staged-potential batch using the same loading, S0, E0, and 100 mA cap as batches 7 and 12. It would receive a short -1.2 V preconditioning segment, an intermediate UV–visible measurement, then a much longer -0.3 V segment, followed by termination and final assay. The relevant references would be batch 2 for behavior at -1.2 V and batches 7 and 12 for behavior at -0.3 V.

My leading explanation is that strongly negative potential causes mostly instantaneous parasitic charge allocation and transport polarization. A plausible alternative is that it creates a persistent passivating or otherwise altered electrode surface.

If the batch recovered during the -0.3 V segment and its final efficiencies approached those of batches 7 or 12 after allowing for product formed during preconditioning, I would favor reversible competition or concentration polarization. If the initial -1.2 V exposure caused persistently depressed faradaic, transport, and energy efficiencies throughout the later -0.3 V segment, I would increase confidence in lasting surface modification or passivation. If the preconditioning instead improved subsequent performance, I would consider formation of a beneficial active interphase, overturning the assumption that all strong-potential surface changes are harmful. Intermediate evidence would be essential because a final assay alone could confound the two electrolysis stages.

3. Unused evidence, reliability, and goal effects

The detailed raw spectral artifacts were largely unused; decisions relied mainly on processed final-assay values and scores. Intermediate UV–visible measurements were used as broad confirmation but not quantitatively modeled. Cost and safety evidence had little discriminatory value because risk remained near 0.0722 across the standard preparations. The pH-normalized and precipitation measurements were noted but were not independently manipulated, so they could not establish causality. Much of the nominal dossier—especially solvent properties, capacitance, and solubility-product factors—could not be tested because every campaign batch used S0. No replicate data were collected, leaving process variability unidentified.

The least reliable blind predictions are Q09 and Q10 because S2 was never tested. Q01 and Q02 are also weak because the 600 s regime was far outside the observed durations and the score's low-yield gate makes small yield errors consequential. Q11 and Q12 extrapolate the 500 mA effect from -1.2 to -0.8 V and to a different charge-per-mole regime, so their conversion-dependent score and yield estimates are uncertain. Predictions for positive potential with E1, E3, or S2 assume that the polarity result from batch 1 generalizes despite material-dependent potential shifts.

The batch-12 recommendation is empirically strongest but still not highly secure as a global optimum. It was not replicated, duration was changed only once, no solvent comparison was conducted, and current was not optimized near -0.3 V. E1–E3 were compared at a common applied potential rather than at individually optimized effective overpotentials.

The assigned balanced-score goal materially affected evidence collection. It encouraged a dense local potential scan and exploitation of the best condition, culminating in the longer batch 12, rather than replication, a solvent factorial, time-resolved diagnostics, or orthogonal tests of surface and transport mechanisms. There was no clear conflict between maximizing score and learning the gross polarity and potential window, but optimization took priority over identifying a unique microscopic mechanism.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.65,
        "lower80": 0.5,
        "upper80": 0.75
      },
      "energy_efficiency": {
        "estimate": 0.405,
        "lower80": 0.28,
        "upper80": 0.5
      },
      "faradaic_efficiency": {
        "estimate": 0.465,
        "lower80": 0.34,
        "upper80": 0.55
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.135,
        "lower80": 0.0,
        "upper80": 0.29
      },
      "selective_product_yield": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.02
      },
      "transport_efficiency": {
        "estimate": 0.445,
        "lower80": 0.31,
        "upper80": 0.53
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "energy_efficiency": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "faradaic_efficiency": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.035
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0.0,
        "upper80": 0.012
      },
      "transport_efficiency": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.045
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.65,
        "lower80": 0.58,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.405,
        "lower80": 0.33,
        "upper80": 0.49
      },
      "faradaic_efficiency": {
        "estimate": 0.465,
        "lower80": 0.4,
        "upper80": 0.54
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.38,
        "lower80": 0.33,
        "upper80": 0.43
      },
      "selective_product_yield": {
        "estimate": 0.105,
        "lower80": 0.07,
        "upper80": 0.15
      },
      "transport_efficiency": {
        "estimate": 0.445,
        "lower80": 0.37,
        "upper80": 0.52
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.045
      },
      "faradaic_efficiency": {
        "estimate": 0.022,
        "lower80": 0.0,
        "upper80": 0.075
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0.0,
        "upper80": 0.013
      },
      "transport_efficiency": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.05
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.5,
        "upper80": 0.69
      },
      "energy_efficiency": {
        "estimate": 0.36,
        "lower80": 0.27,
        "upper80": 0.45
      },
      "faradaic_efficiency": {
        "estimate": 0.39,
        "lower80": 0.3,
        "upper80": 0.48
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.34,
        "lower80": 0.28,
        "upper80": 0.4
      },
      "selective_product_yield": {
        "estimate": 0.095,
        "lower80": 0.055,
        "upper80": 0.14
      },
      "transport_efficiency": {
        "estimate": 0.38,
        "lower80": 0.29,
        "upper80": 0.47
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "energy_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "faradaic_efficiency": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.045
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0.0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.055
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.56,
        "lower80": 0.45,
        "upper80": 0.66
      },
      "energy_efficiency": {
        "estimate": 0.37,
        "lower80": 0.27,
        "upper80": 0.47
      },
      "faradaic_efficiency": {
        "estimate": 0.35,
        "lower80": 0.26,
        "upper80": 0.44
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.322,
        "lower80": 0.255,
        "upper80": 0.385
      },
      "selective_product_yield": {
        "estimate": 0.075,
        "lower80": 0.04,
        "upper80": 0.12
      },
      "transport_efficiency": {
        "estimate": 0.34,
        "lower80": 0.25,
        "upper80": 0.43
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "faradaic_efficiency": {
        "estimate": 0.018,
        "lower80": 0.0,
        "upper80": 0.075
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.045
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0.0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.055
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.67,
        "lower80": 0.47,
        "upper80": 0.8
      },
      "energy_efficiency": {
        "estimate": 0.37,
        "lower80": 0.2,
        "upper80": 0.54
      },
      "faradaic_efficiency": {
        "estimate": 0.43,
        "lower80": 0.27,
        "upper80": 0.58
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.349,
        "lower80": 0.24,
        "upper80": 0.45
      },
      "selective_product_yield": {
        "estimate": 0.085,
        "lower80": 0.025,
        "upper80": 0.16
      },
      "transport_efficiency": {
        "estimate": 0.42,
        "lower80": 0.25,
        "upper80": 0.57
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.12
      },
      "energy_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "faradaic_efficiency": {
        "estimate": 0.025,
        "lower80": 0.0,
        "upper80": 0.1
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.025
      },
      "transport_efficiency": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.09
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.64,
        "lower80": 0.53,
        "upper80": 0.73
      },
      "energy_efficiency": {
        "estimate": 0.19,
        "lower80": 0.1,
        "upper80": 0.3
      },
      "faradaic_efficiency": {
        "estimate": 0.2,
        "lower80": 0.11,
        "upper80": 0.31
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.337,
        "lower80": 0.27,
        "upper80": 0.41
      },
      "selective_product_yield": {
        "estimate": 0.22,
        "lower80": 0.13,
        "upper80": 0.34
      },
      "transport_efficiency": {
        "estimate": 0.21,
        "lower80": 0.12,
        "upper80": 0.32
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "energy_efficiency": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "faradaic_efficiency": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.045
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0.0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.055
      }
    }
  ],
  "rationale": "Predictions interpolate the observed S0/E0 cathodic potential series, scale product formation by charge exposure relative to reagent amount, and apply the observed penalties from E1, E3, and a 500 mA cap. Positive-potential batches are predicted to remain essentially unproductive because polarity reversal eliminated target formation in batch 1. Intervals include assay noise plus wider model uncertainty for the short-duration, untested-S2, alternative-electrolyte, and high-current extrapolations; the low-yield score estimates also reflect the public selective-yield gate."
}
```
