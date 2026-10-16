# repeat-03/EC-W05-B12-discovery-E-Opaque

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-03\EC-W05-B12-discovery-E-Opaque\participant\discovery-E-Opaque

## 同期笔记

### v1 · 公开事件 0

# Electrochemical-system hypotheses

## H1 [tentative]
At fixed loading (0.020 mol in 0.040 L), conversion should rise with delivered charge and potential magnitude once the productive polarity is selected, but selective yield and energy efficiency should peak at intermediate severity because longer/higher-potential operation promotes byproduct or degradation pathways. The opposite polarity may suppress target formation or favor a distinct path.

## H2 [tentative]
Solvent and electrolyte labels can independently affect transport/ohmic efficiency and therefore delivered current, so a nominal current cap is not equivalent to charge passed. Comparisons should use the same loading, potential, cap, and time.

## H3 [tentative]
A current-cap series at fixed potential/time should distinguish charge limitation from potential-driven selectivity: if conversion rises while selectivity stays similar, cap mainly controls rate; changing selectivity would implicate competing current-dependent pathways.

### Planned tests
Use twelve independent batches at the fixed loading, spanning both potential signs, time, potential magnitude, current cap, all four solvents and electrolytes, with one intermediate UV-vis measurement per batch where possible. Numerical differences will be treated cautiously relative to the declared assay noise and checked with targeted repeats/comparisons.

### v2 · 公开事件 56

# Electrochemical-system hypotheses

## H1 [supported in tested S0/E0 scope; nonlinear]
The productive response is strongly nonlinear in potential, time, and polarity. At 600 s, both ±1 V gave low selective yield and their numerical difference is comparable to the assay yield-noise scale (events runner-operation-0007 and -0014), so a polarity advantage is unresolved there. At 3600 s, +1 V gave much higher selective yield, conversion, selectivity, and efficiency than −1 V (events -0042 vs -0035). Both ±2 V were poor at 600 s (events -0021, -0028), supporting a finite potential window rather than monotonic benefit from magnitude. Prediction: at S0/E0 and 3600 s, +1 V should remain superior to −1 V; very long +1 V may eventually plateau or lose selectivity.

## H2 [supported qualitatively; material scope unresolved]
The current cap is not delivered current. In the −1 V/3600 s series, raising the cap from 20 to 100 to 500 mA numerically increased conversion/yield, while 500 mA sharply reduced faradaic, transport, ohmic, and energy efficiencies (events -0049, -0035, -0056). This is consistent with charge limitation at low cap and parasitic/ohmic losses at high cap. Lack of repeats leaves exact cap effects uncertain.

## H3 [tentative kinetic account]
A short induction/charge-accumulation regime may explain the low +1 V yield at 600 s followed by strong yield at 3600 s, whereas negative polarity has lower intrinsic target selectivity. Alternative: apparent crossover is stochastic/process variability; a long-duration test and material comparisons will probe scope.

### Decisions
Use +1 V, 100 mA, 3600 s as the reference condition for S1/E1, S2/E2, and S3/E3 comparisons. Reserve the final S0/E0 batch for +1 V at 14400 s to test plateau/degradation. Material effects will remain confounded between paired solvent/electrolyte changes, so conclusions should be framed as formulation-pair effects rather than assigning causality to one component.

### v3 · 公开事件 84

# Electrochemical-system hypotheses — final source-stage synthesis

## H1 [supported in tested S0/E0 scope]
At +1 V and 100 mA cap, target formation is time-dependent over 600–14400 s: selective yield rose from 0.0011 to 0.0987 to 0.3199, with conversion 0.0234, 0.0916, and 0.2961 (events runner-operation-0007, -0042, -0084). The long run retained high selectivity (0.971) and high energy/ohmic efficiency, so the predicted degradation downturn was not reached. A simple useful local account is increasing charge exposure with a slow/induction-like early regime, not instantaneous equilibration. Extrapolation beyond 14400 s is unresolved.

## H2 [supported: polarity and potential window]
Polarity changes the pathway, not merely the rate. At 3600 s in S0/E0, +1 V strongly outperformed −1 V in yield, conversion, selectivity, faradaic efficiency, transport efficiency, and energy efficiency (events -0042 vs -0035). At 600 s both signs were near the yield-noise floor (events -0007, -0014), so the short-time polarity difference is unresolved. At 600 s, ±2 V were both poor relative to the moderate-potential behavior (events -0021, -0028), indicating a finite productive potential window and parasitic loss at excessive magnitude.

## H3 [supported qualitatively at −1 V]
The nominal cap controls accessible rate only until parasitic/ohmic penalties dominate. At −1 V and 3600 s, 20→100→500 mA caps numerically increased yield/conversion, but the 500 mA condition sharply lowered faradaic, transport, ohmic, and energy efficiencies (events -0049, -0035, -0056). Thus delivered charge should be modeled as potential-, medium-, and cap-dependent; cap is not assumed delivered current. Exact functional form and repeatability remain unresolved.

## H4 [supported for paired formulations; component attribution unresolved]
At +1 V, 100 mA, 3600 s, paired S0/E0 gave the strongest overall response (event -0042). S1/E1 and S2/E2 were intermediate, while S3/E3 had especially weak faradaic/transport efficiencies (events -0063, -0070, -0077). Precipitation signal also separated formulations: near 1 for S0/E0, about 0.73 for S1/E1, and near 0 for S2/E2 and S3/E3. Because solvent and electrolyte were changed together, these are formulation-pair effects; no independent solvent-versus-electrolyte causal claim is justified.

## Working predictive account
Within the tested loading of 0.020 mol in 0.040 L, conversion grows with productive charge exposure, multiplied by formulation-specific transport/faradaic factors. Target yield is approximately conversion times a polarity/potential-dependent pathway factor, with an early-time threshold or induction term. Moderate +1 V accesses a highly selective path in S0/E0; −1 V accesses a lower-selectivity/lower-efficiency path; |V|=2 V incurs strong parasitic suppression. High current caps can raise conversion yet lower efficiency through transport/ohmic/parasitic losses.

## Recommendation decision
Batch 12 (+1 V, 100 mA cap, 14400 s, S0/E0) is the operating recommendation: it achieved the highest observed score and selective yield while retaining high selectivity and efficiencies (event -0084). This is an observed optimum among tested points, not proof of a global optimum. It would be reconsidered if longer operation reveals degradation, if independent S/E swaps outperform S0/E0, or if repeat runs show substantial process variability.

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
    "electrochemical_conversion": 0.023405056446790695,
    "electrochemical_selectivity": 0.998518168926239,
    "energy_efficiency": 0.9631397724151611,
    "faradaic_efficiency": 1.0,
    "ohmic_efficiency": 0.9602119326591492,
    "pH_normalized": 0.23308512568473816,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.032431427389383316,
    "selective_product_yield": 0.001095070969313383,
    "transport_efficiency": 0.9858177900314331
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
    "electrochemical_selectivity": 0.6434827446937561,
    "energy_efficiency": 0.2848791182041168,
    "faradaic_efficiency": 0.40667814016342163,
    "ohmic_efficiency": 0.9690497517585754,
    "pH_normalized": 0.2303897738456726,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.20308656990528107,
    "selective_product_yield": 0.012986360117793083,
    "transport_efficiency": 0.43293496966362
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
    "ohmic_efficiency": 0.9711474776268005,
    "pH_normalized": 0.231104776263237,
    "precipitation_signal": 0.9869203567504883,
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
      "potential_V": -2
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
    "electrochemical_conversion": 0.00024919878342188895,
    "electrochemical_selectivity": 0.4771483242511749,
    "energy_efficiency": 0.03654424101114273,
    "faradaic_efficiency": 0.2876546382904053,
    "ohmic_efficiency": 0.9833056330680847,
    "pH_normalized": 0.23041419684886932,
    "precipitation_signal": 0.9876685738563538,
    "safety_risk": 0.072194404900074,
    "score": 0.030663253739476204,
    "selective_product_yield": 0.0028296606615185738,
    "transport_efficiency": 0.25616708397865295
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
    "cost": 0.28404000401496887,
    "electrochemical_conversion": 0.0413973331451416,
    "electrochemical_selectivity": 0.6398956179618835,
    "energy_efficiency": 0.27024927735328674,
    "faradaic_efficiency": 0.4178524315357208,
    "ohmic_efficiency": 0.9674157500267029,
    "pH_normalized": 0.23537498712539673,
    "precipitation_signal": 0.9869949817657471,
    "safety_risk": 0.072194404900074,
    "score": 0.31868255138397217,
    "selective_product_yield": 0.0325041301548481,
    "transport_efficiency": 0.40734297037124634
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
      "current_mA": 100,
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
    "cost": 0.28404000401496887,
    "electrochemical_conversion": 0.0915781557559967,
    "electrochemical_selectivity": 0.9924110770225525,
    "energy_efficiency": 0.9525881409645081,
    "faradaic_efficiency": 0.9827661514282227,
    "ohmic_efficiency": 0.9692724943161011,
    "pH_normalized": 0.2320990413427353,
    "precipitation_signal": 0.9976252913475037,
    "safety_risk": 0.072194404900074,
    "score": 0.6218015551567078,
    "selective_product_yield": 0.09870610386133194,
    "transport_efficiency": 0.9580828547477722
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
      "current_mA": 20,
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
    "cost": 0.2828879952430725,
    "electrochemical_conversion": 0.017859596759080887,
    "electrochemical_selectivity": 0.627807080745697,
    "energy_efficiency": 0.2933078408241272,
    "faradaic_efficiency": 0.4045216143131256,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.23111364245414734,
    "precipitation_signal": 0.9826673865318298,
    "safety_risk": 0.072194404900074,
    "score": 0.18806560337543488,
    "selective_product_yield": 0.01202103029936552,
    "transport_efficiency": 0.4079219698905945
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
      "current_mA": 500,
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
    "cost": 0.2897999882698059,
    "electrochemical_conversion": 0.08442520350217819,
    "electrochemical_selectivity": 0.6456847786903381,
    "energy_efficiency": 0.13989238440990448,
    "faradaic_efficiency": 0.19981251657009125,
    "ohmic_efficiency": 0.8635371923446655,
    "pH_normalized": 0.229416161775589,
    "precipitation_signal": 0.995540201663971,
    "safety_risk": 0.072194404900074,
    "score": 0.24989506602287292,
    "selective_product_yield": 0.03741259127855301,
    "transport_efficiency": 0.19331717491149902
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
      "current_mA": 100,
      "electrolyte_profile": 1,
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
    "cost": 0.30004000663757324,
    "electrochemical_conversion": 0.06316675990819931,
    "electrochemical_selectivity": 0.7233936786651611,
    "energy_efficiency": 0.718433678150177,
    "faradaic_efficiency": 0.6889169812202454,
    "ohmic_efficiency": 0.9674895405769348,
    "pH_normalized": 0.20476384460926056,
    "precipitation_signal": 0.7306620478630066,
    "safety_risk": 0.09559440612792969,
    "score": 0.4731023907661438,
    "selective_product_yield": 0.06489191949367523,
    "transport_efficiency": 0.7097482681274414
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
      "solvent": 2,
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 2,
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
    "cost": 0.3256399929523468,
    "electrochemical_conversion": 0.08347900956869125,
    "electrochemical_selectivity": 0.7739008069038391,
    "energy_efficiency": 0.7102834582328796,
    "faradaic_efficiency": 0.7391970753669739,
    "ohmic_efficiency": 0.9107071161270142,
    "pH_normalized": 0.16965022683143616,
    "precipitation_signal": 0.0,
    "safety_risk": 0.1135944053530693,
    "score": 0.4812830686569214,
    "selective_product_yield": 0.048975441604852676,
    "transport_efficiency": 0.7405466437339783
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
      "solvent": 3,
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 3,
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
    "cost": 0.30963999032974243,
    "electrochemical_conversion": 0.047300588339567184,
    "electrochemical_selectivity": 0.7223699688911438,
    "energy_efficiency": 0.4833497107028961,
    "faradaic_efficiency": 0.36507949233055115,
    "ohmic_efficiency": 0.9700570106506348,
    "pH_normalized": 0.2838256359100342,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.12619440257549286,
    "score": 0.3521295189857483,
    "selective_product_yield": 0.02633821591734886,
    "transport_efficiency": 0.3722594380378723
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
      "current_mA": 100,
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
    "cost": 0.28835999965667725,
    "electrochemical_conversion": 0.2961335778236389,
    "electrochemical_selectivity": 0.9708430171012878,
    "energy_efficiency": 0.949072539806366,
    "faradaic_efficiency": 0.8035455942153931,
    "ohmic_efficiency": 0.985348641872406,
    "pH_normalized": 0.23062115907669067,
    "precipitation_signal": 0.9938013553619385,
    "safety_risk": 0.072194404900074,
    "score": 0.6713008880615234,
    "selective_product_yield": 0.31989920139312744,
    "transport_efficiency": 0.8247705101966858
  }
}
```

## K1 封存报告

Mechanism report

Scope and experimental basis

All 12 batches used 0.020 mol limiting reagent in 0.040 L solvent (nominal initial concentration 0.50 mol L^-1). Each batch was independently configured, electrolyzed once, observed by UV-vis, terminated, and measured by final assay. Solvent S0–S3 and electrolyte E0–E3 are anonymous benchmark labels, so no molecular identity or real-material mechanism can be assigned to them. Most comparisons are single runs; numerical differences near the declared assay noise should not be treated as established effects.

Proposed working mechanism

I infer that target formation requires passage of productive charge through a polarity- and potential-dependent electrochemical pathway. A compact phenomenological representation is

Q_eff = integral I_delivered(t) dt × eta_transport(S,E,V,Icap) × eta_F(S,E,V,Icap),

X = F(Q_eff; V,S,E),

Y_target = X × phi_target(V,S,E,t),

where Q_eff is effective productive charge, X is conversion, phi_target is the fraction of converted material reaching the target, and Y_target is selective product yield. The current cap is only an upper bound: delivered current and productive charge depend on potential, medium, transport, and parasitic reactions. The measured faradaic, transport, ohmic, and energy efficiencies are therefore coupled rather than independent outputs.

The evidence favors a finite productive potential window. Moderate +1 V accesses a highly selective, efficient pathway in S0/E0 after sufficient electrolysis time. Negative polarity accesses a less efficient and less selective pathway. Increasing |V| to 2 V does not simply accelerate conversion; it appears to favor parasitic electrochemistry or otherwise suppress productive transport/faradaic utilization. High current caps can increase conversion while decreasing efficiency, consistent with polarization, transport limitation, ohmic heating/loss, or competing electrode reactions. These specific microscopic alternatives cannot be distinguished by the available observables.

Time dependence and possible induction behavior

At +1 V, 100 mA cap, S0/E0, increasing time from 600 to 3,600 to 14,400 s increased final selective product yield from 0.00110 (batch 1) to 0.0987 (batch 6) to 0.3199 (batch 12). Final electrochemical conversion increased from 0.0234 to 0.0916 to 0.2961. Selectivity remained very high: 0.9985, 0.9924, and 0.9708, respectively. Thus, over the tested range, longer operation mainly accumulated productive conversion rather than causing a major loss of pathway selectivity.

This series is compatible with an early induction or charge-threshold regime followed by continuing conversion. It is also compatible with ordinary nonlinear kinetics plus measurement noise at low product concentration; the data do not uniquely establish a physical induction step. A useful local model would be X approximately increasing with max(0,Q_eff−Q0), possibly approaching saturation at larger charge. A simple constant-rate law is inadequate across the whole interval because the 600 s yield is extremely small relative to the later points. No degradation downturn was observed by 14,400 s, so any claim that yield peaks at longer times is an extrapolation, not an observation.

Polarity and potential dependence

At 3,600 s in S0/E0, +1 V (batch 6) clearly outperformed −1 V (batch 5). Batch 6 gave conversion 0.0916, selectivity 0.9924, yield 0.0987, faradaic efficiency 0.9828, transport efficiency 0.9581, and energy efficiency 0.9526. Batch 5 gave conversion 0.0414, selectivity 0.6399, yield 0.0325, faradaic efficiency 0.4179, transport efficiency 0.4073, and energy efficiency 0.2702. This coordinated change across several channels supports a genuine polarity-dependent pathway rather than merely a noisy yield difference.

At 600 s, however, +1 V (batch 1) produced yield 0.00110 and −1 V (batch 2) produced 0.0130. Both are near the low-yield/noise regime, and batch 2's reported conversion was clipped at zero despite nonzero yield. That internal inconsistency is consistent with independent channel noise and means the apparent short-time advantage of −1 V is unresolved. I therefore do not infer a real polarity crossover from batches 1 and 2.

Excessive potential magnitude was unfavorable at 600 s. Batch 3 at +2 V had zero reported yield, conversion, faradaic efficiency, transport efficiency, and energy efficiency. Batch 4 at −2 V had yield 0.00283, conversion 0.000249, selectivity 0.477, faradaic efficiency 0.288, transport efficiency 0.256, and energy efficiency 0.0365. Compared with the corresponding ±1 V conditions, these observations support a potential-window model with strong parasitic suppression at |V|=2 V. Because only one duration was tested at ±2 V, I cannot separate immediate potential damage from an altered time dependence.

Current-cap coupling

The current-cap series was performed at −1 V, S0/E0, and 3,600 s. At caps of 20, 100, and 500 mA (batches 7, 5, and 8), yields were 0.0120, 0.0325, and 0.0374, while conversions were 0.0179, 0.0414, and 0.0844. Thus greater current availability numerically increased reaction progress, but yield showed diminishing returns.

The 500 mA condition incurred a pronounced efficiency penalty: batch 8 had faradaic efficiency 0.1998, transport efficiency 0.1933, ohmic efficiency 0.8635, and energy efficiency 0.1399. At 100 mA these values were 0.4179, 0.4073, 0.9674, and 0.2702; at 20 mA they were 0.4045, 0.4079, 1.000, and 0.2933. This suggests that the productive pathway becomes limited by transport or interfacial supply, while additional available current is increasingly consumed by parasitic processes and resistive losses. The exact functional dependence is unidentifiable because delivered current and charge were not measured directly, the series was performed only at −1 V, and there were no replicates.

Medium/formulation effects

At +1 V, 100 mA, and 3,600 s, paired S/E formulations were compared. S0/E0 (batch 6) was strongest overall: yield 0.0987, selectivity 0.9924, faradaic efficiency 0.9828, transport efficiency 0.9581, and energy efficiency 0.9526. S1/E1 (batch 9) gave yield 0.0649, selectivity 0.7234, faradaic efficiency 0.6889, transport efficiency 0.7097, and energy efficiency 0.7184. S2/E2 (batch 10) gave yield 0.0490, selectivity 0.7739, faradaic efficiency 0.7392, transport efficiency 0.7405, and energy efficiency 0.7103. S3/E3 (batch 11) was weakest in charge utilization, with yield 0.0263, selectivity 0.7224, faradaic efficiency 0.3651, transport efficiency 0.3723, and energy efficiency 0.4833.

These results imply that the medium affects both charge delivery and chemical branching. In the model, formulation therefore modifies eta_transport, eta_F, and phi_target, not just one scalar rate constant. Ohmic efficiencies remained relatively high in these four batches (approximately 0.91–0.97), whereas transport and faradaic efficiencies varied much more, suggesting that simple resistance alone cannot explain the formulation ranking.

Precipitation signal also tracked formulation: approximately 0.998 for S0/E0, 0.731 for S1/E1, and near zero for S2/E2 and S3/E3. This could indicate a phase or solubility coupling associated with the productive S0/E0 state, perhaps by removing product from solution or changing interfacial transport. That interpretation is conjectural: the signal does not identify the precipitating species, and it might instead be a correlated medium property or inactive solid. The normalized pH values also differed among paired formulations—about 0.232 for S0/E0, 0.205 for S1/E1, 0.170 for S2/E2, and 0.284 for S3/E3—but solvent and electrolyte were changed simultaneously, so pH cannot be isolated as a causal variable.

How the explanation changed

The initial hypothesis was that conversion would increase with charge and that excessive severity could reduce selectivity. Batches 1–4 established that potential magnitude is not monotonic: ±2 V were poor, and the short ±1 V results were too close to the low-signal regime to establish a polarity ranking. Batches 5 and 6 changed the account substantially: at 3,600 s, +1 V produced a coordinated improvement in every important electrochemical output over −1 V, revealing a polarity-specific productive pathway. Batches 7 and 8 then showed that more current availability can increase conversion while degrading charge and energy utilization, motivating the distinction between nominal current cap and effective productive charge. Batches 9–11 showed that medium effects act on both transport/faradaic utilization and selectivity. Finally, batch 12 disproved the tentative expectation of degradation within the tested time window: at 14,400 s it retained selectivity 0.9708 and energy efficiency 0.9491 while reaching the highest yield, 0.3199.

Unidentifiable factors and limitations

1. Solvent and electrolyte effects are confounded. Batches 9–11 changed S and E together, so the individual contribution of either component and any S×E interaction cannot be estimated.
2. Delivered current, electrode area, charge, electrode state, temperature trajectory, concentrations during reaction, and identities of products or precipitates were not observed. Therefore no microscopic rate constant, electron stoichiometry, or electrode mechanism can be identified.
3. Every condition was run once. Process variability cannot be separated from treatment effects, although large coordinated differences—especially batches 5 versus 6—are more persuasive than isolated small differences.
4. Final-assay channels have independent noise and clipping. Low conversion/yield results, such as batch 2's zero conversion with nonzero yield, should not be forced into exact mass-balance identities.
5. The proposed equations are phenomenological and local to 0.50 mol L^-1 initial loading and the tested ranges. They should not be extrapolated to other concentrations, volumes, potentials beyond ±2 V, current caps beyond 20–500 mA, or times beyond 14,400 s without evidence.
6. Precipitation and normalized pH are correlates, not demonstrated mediators.

Plausible alternative explanations

A single homogeneous kinetic network with polarity-dependent rate constants could reproduce much of the data without a literal induction step. Electrode conditioning or nucleation could instead create the apparent slow early regime. The loss at ±2 V might arise from substrate destruction, product destruction, electrode passivation, gas evolution, or an instrument-visible state change; these alternatives are observationally equivalent here. Formulation differences might reflect conductivity, viscosity/diffusion, proton activity, substrate solvation, product solubility, or electrode-film formation. The campaign cannot select among these microscopic explanations.

Overall conclusion

The most defensible predictive account is a nonlinear effective-charge model coupled to pathway selection. Moderate positive potential (+1 V) in S0/E0 creates the most productive and selective pathway observed. Reaction progress grows strongly with time through 14,400 s. Negative polarity lowers pathway selectivity and productive charge utilization. Excessive potential magnitude suppresses the desired process, while excessive current availability produces diminishing yield gains and substantial faradaic, transport, ohmic, and energy penalties. Medium composition controls both transport/faradaic performance and chemical branching, but its solvent and electrolyte contributions remain inseparable. Batch 12 is the best observed operating point, not a demonstrated global optimum.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific prior, nominal material-property dossier, or prescribed mechanistic law was supplied. The solvent and electrolyte labels were explicitly anonymous. My starting claims were therefore self-developed hypotheses rather than applications of a supplied prior.

• Supported: reaction progress increases with productive charge exposure. At +1 V, 100 mA, S0/E0, selective yield rose from 0.00110 at 600 s (batch 1) to 0.0987 at 3,600 s (batch 6) and 0.3199 at 14,400 s (batch 12); conversion likewise rose from 0.0234 to 0.0916 to 0.2961.

• Supported: there is a finite productive potential window rather than a monotonic benefit from larger |V|. At 600 s, +2 V was essentially inactive (batch 3), and −2 V gave only 0.00283 yield with very low energy efficiency (batch 4). These results were worse than the moderate-potential behavior.

• Supported in the tested S0/E0 scope: polarity changes pathway efficiency and selectivity. The decisive evidence was the coordinated difference between +1 V in batch 6 and −1 V in batch 5 at 3,600 s. Batch 6 had yield 0.0987, selectivity 0.992, and energy efficiency 0.953, versus 0.0325, 0.640, and 0.270 in batch 5. The short-time comparison, batches 1 and 2, had not established this because both yields were near the low-signal regime and batch 2 reported zero conversion alongside nonzero yield.

• Supported qualitatively: raising the current cap can increase progress but produce diminishing returns and parasitic losses. In the −1 V, 3,600 s series, conversion rose across 20, 100, and 500 mA caps (batches 7, 5, and 8), while the 500 mA batch had much poorer faradaic, transport, ohmic, and energy efficiencies. Selectivity stayed numerically similar across that series, consistent with the cap affecting rate more than branching under those conditions.

• Supported only for paired formulations: medium choice affects transport/faradaic utilization and pathway selectivity. At otherwise matched +1 V conditions, S0/E0 was strongest (batch 6), S1/E1 and S2/E2 were intermediate (batches 9 and 10), and S3/E3 had particularly weak transport and faradaic efficiencies (batch 11).

• Contradicted within the tested range: my initial expectation that sufficiently long or severe operation might cause a yield/selectivity downturn was not observed for longer time at +1 V. Batch 12 at 14,400 s retained selectivity 0.971 and energy efficiency 0.949 while producing the highest yield. This does not rule out degradation beyond 14,400 s, but it changed the claim from an expected interior time optimum to an untested longer-time possibility.

• Untested: whether the early-time behavior is a true induction or threshold process rather than smooth nonlinear kinetics; whether product precipitation causes, protects, or merely correlates with high yield; the individual effects of solvent and electrolyte; interactions between unmatched S/E pairs; delivered current and electron stoichiometry; behavior beyond 14,400 s; and reproducibility at the recommended condition. Because every condition was run once, process variance also remains unidentified.

2. One proposed discriminating experiment

I would run one independent crossed-formulation batch using S2/E0 at the established reference setting: 0.020 mol reagent in 0.040 L, +1 V, 100 mA cap, and 3,600 s, followed by the same final assay. This is not an executed experiment.

The leading explanation treats productive conversion as effective charge multiplied by medium-dependent transport/faradaic factors, with precipitation mainly a correlated state marker. A plausible alternative is that the near-complete precipitation signal characteristic of S0/E0 is mechanistically important—for example, product removal may protect the target or shift branching.

The known anchors are S0/E0 in batch 6, which combined high yield and efficiencies with precipitation near one, and S2/E2 in batch 10, which had lower yield and precipitation near zero. The crossed S2/E0 experiment would partially separate solvent from electrolyte:

• If S2/E0 retained high yield, selectivity, and charge efficiencies despite a low precipitation signal, I would reject precipitation as a necessary mediator and attribute more of the batch-10 deficit to E2 or an S2×E2 interaction.

• If S2/E0 showed low precipitation together with a substantial loss of yield but retained relatively good electrical efficiencies, I would increase belief that an S0-dependent phase/solubility process affects chemical branching or product preservation.

• If both precipitation and all charge efficiencies fell, the result would support a broader solvent-controlled transport/interfacial explanation but would still not prove precipitation is causal.

• If S2/E0 resembled neither parent pairing, strong solvent–electrolyte interaction would become the leading account, and additive formulation extrapolations would be abandoned.

One crossed batch cannot fully identify causality; the complementary S0/E2 crossing and replication would ultimately be required.

3. Unused evidence, weak predictions, and effect of the goal

The detailed raw UV-vis spectra, band shapes, and characterization artifacts were not analyzed. Intermediate UV-vis estimates were collected but used mainly as qualitative consistency checks; the final account relied primarily on final-assay outputs. Cost, small temperature changes during solvent addition, and the full temporal risk accumulation were not used mechanistically. Normalized pH and precipitation were not central to experimental adaptation and were interpreted only after the formulation comparison. No independent solvent/electrolyte swaps or exact replicates were available.

The least reliable blind predictions are those for unmatched solvent/electrolyte combinations (especially Q05–Q10), because the campaign changed S and E together. Q12 is also weak because positive polarity at 500 mA was never tested; it requires extrapolating the high-current penalty observed only at negative polarity. Q01 and Q02 are uncertain because predicted yields lie near zero and the score has a multiplicative yield gate, so small yield errors can cause large score errors. The 7,200 s predictions extrapolate between sparsely sampled times, and the proposed induction form was never identified. Predictions for the measured efficiencies under S0/E0, + polarity, and 100 mA are comparatively better constrained.

The batch-12 recommendation is empirically supported as the best observed batch, but it is not a secure global optimum: it was a single run, used the longest tested duration, and had no neighboring longer-time point or replicate. Its absolute performance and robustness are therefore less reliable than its ranking within the observed campaign.

The assigned goal did affect evidence collection. Because explanation and prediction were primary and public score was secondary, I spent batches on polarity, potential magnitude, time, current cap, and formulation contrasts rather than repeatedly optimizing around the first high-scoring condition. This breadth exposed the potential window and current-efficiency tradeoff, but it left fewer resources for replication, fine mapping near +1 V, and independent S/E crossings. I see no direct conflict between the goal and safety: observed risks remained below the stated limit. The main tradeoff was explanatory breadth versus statistical precision and optimization confidence.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.65,
        "lower80": 0.48,
        "upper80": 0.79
      },
      "energy_efficiency": {
        "estimate": 0.34,
        "lower80": 0.18,
        "upper80": 0.5
      },
      "faradaic_efficiency": {
        "estimate": 0.45,
        "lower80": 0.28,
        "upper80": 0.61
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.132,
        "lower80": 0.02,
        "upper80": 0.31
      },
      "selective_product_yield": {
        "estimate": 0.008,
        "lower80": 0,
        "upper80": 0.025
      },
      "transport_efficiency": {
        "estimate": 0.46,
        "lower80": 0.29,
        "upper80": 0.63
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.98,
        "lower80": 0.91,
        "upper80": 1
      },
      "energy_efficiency": {
        "estimate": 0.95,
        "lower80": 0.86,
        "upper80": 1
      },
      "faradaic_efficiency": {
        "estimate": 0.98,
        "lower80": 0.9,
        "upper80": 1
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.234,
        "lower80": 0.04,
        "upper80": 0.59
      },
      "selective_product_yield": {
        "estimate": 0.008,
        "lower80": 0,
        "upper80": 0.027
      },
      "transport_efficiency": {
        "estimate": 0.96,
        "lower80": 0.87,
        "upper80": 1
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.66,
        "lower80": 0.54,
        "upper80": 0.76
      },
      "energy_efficiency": {
        "estimate": 0.34,
        "lower80": 0.2,
        "upper80": 0.49
      },
      "faradaic_efficiency": {
        "estimate": 0.45,
        "lower80": 0.32,
        "upper80": 0.59
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.35,
        "lower80": 0.27,
        "upper80": 0.44
      },
      "selective_product_yield": {
        "estimate": 0.05,
        "lower80": 0.024,
        "upper80": 0.086
      },
      "transport_efficiency": {
        "estimate": 0.46,
        "lower80": 0.32,
        "upper80": 0.61
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.98,
        "lower80": 0.93,
        "upper80": 1
      },
      "energy_efficiency": {
        "estimate": 0.95,
        "lower80": 0.87,
        "upper80": 1
      },
      "faradaic_efficiency": {
        "estimate": 0.98,
        "lower80": 0.89,
        "upper80": 1
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.644,
        "lower80": 0.56,
        "upper80": 0.72
      },
      "selective_product_yield": {
        "estimate": 0.16,
        "lower80": 0.1,
        "upper80": 0.23
      },
      "transport_efficiency": {
        "estimate": 0.96,
        "lower80": 0.87,
        "upper80": 1
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.41,
        "upper80": 0.76
      },
      "energy_efficiency": {
        "estimate": 0.25,
        "lower80": 0.09,
        "upper80": 0.46
      },
      "faradaic_efficiency": {
        "estimate": 0.36,
        "lower80": 0.18,
        "upper80": 0.57
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.303,
        "lower80": 0.17,
        "upper80": 0.43
      },
      "selective_product_yield": {
        "estimate": 0.04,
        "lower80": 0.012,
        "upper80": 0.078
      },
      "transport_efficiency": {
        "estimate": 0.38,
        "lower80": 0.19,
        "upper80": 0.59
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.85,
        "lower80": 0.64,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.72,
        "lower80": 0.49,
        "upper80": 0.91
      },
      "faradaic_efficiency": {
        "estimate": 0.76,
        "lower80": 0.53,
        "upper80": 0.94
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.523,
        "lower80": 0.39,
        "upper80": 0.64
      },
      "selective_product_yield": {
        "estimate": 0.11,
        "lower80": 0.055,
        "upper80": 0.18
      },
      "transport_efficiency": {
        "estimate": 0.75,
        "lower80": 0.52,
        "upper80": 0.94
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.34,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.18,
        "lower80": 0.04,
        "upper80": 0.39
      },
      "faradaic_efficiency": {
        "estimate": 0.25,
        "lower80": 0.08,
        "upper80": 0.46
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.255,
        "lower80": 0.11,
        "upper80": 0.38
      },
      "selective_product_yield": {
        "estimate": 0.025,
        "lower80": 0.003,
        "upper80": 0.058
      },
      "transport_efficiency": {
        "estimate": 0.27,
        "lower80": 0.08,
        "upper80": 0.49
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.8,
        "lower80": 0.58,
        "upper80": 0.95
      },
      "energy_efficiency": {
        "estimate": 0.58,
        "lower80": 0.34,
        "upper80": 0.81
      },
      "faradaic_efficiency": {
        "estimate": 0.5,
        "lower80": 0.26,
        "upper80": 0.75
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.428,
        "lower80": 0.27,
        "upper80": 0.57
      },
      "selective_product_yield": {
        "estimate": 0.08,
        "lower80": 0.031,
        "upper80": 0.15
      },
      "transport_efficiency": {
        "estimate": 0.5,
        "lower80": 0.26,
        "upper80": 0.75
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.4,
        "upper80": 0.73
      },
      "energy_efficiency": {
        "estimate": 0.3,
        "lower80": 0.14,
        "upper80": 0.49
      },
      "faradaic_efficiency": {
        "estimate": 0.4,
        "lower80": 0.22,
        "upper80": 0.59
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.315,
        "lower80": 0.19,
        "upper80": 0.44
      },
      "selective_product_yield": {
        "estimate": 0.04,
        "lower80": 0.013,
        "upper80": 0.078
      },
      "transport_efficiency": {
        "estimate": 0.4,
        "lower80": 0.21,
        "upper80": 0.6
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.88,
        "lower80": 0.72,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.88,
        "lower80": 0.7,
        "upper80": 0.98
      },
      "faradaic_efficiency": {
        "estimate": 0.9,
        "lower80": 0.73,
        "upper80": 1
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.588,
        "lower80": 0.45,
        "upper80": 0.69
      },
      "selective_product_yield": {
        "estimate": 0.13,
        "lower80": 0.073,
        "upper80": 0.2
      },
      "transport_efficiency": {
        "estimate": 0.88,
        "lower80": 0.7,
        "upper80": 0.99
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.65,
        "lower80": 0.51,
        "upper80": 0.76
      },
      "energy_efficiency": {
        "estimate": 0.12,
        "lower80": 0.02,
        "upper80": 0.27
      },
      "faradaic_efficiency": {
        "estimate": 0.18,
        "lower80": 0.06,
        "upper80": 0.34
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.257,
        "lower80": 0.18,
        "upper80": 0.35
      },
      "selective_product_yield": {
        "estimate": 0.065,
        "lower80": 0.027,
        "upper80": 0.115
      },
      "transport_efficiency": {
        "estimate": 0.18,
        "lower80": 0.05,
        "upper80": 0.35
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.93,
        "lower80": 0.8,
        "upper80": 1
      },
      "energy_efficiency": {
        "estimate": 0.48,
        "lower80": 0.27,
        "upper80": 0.69
      },
      "faradaic_efficiency": {
        "estimate": 0.55,
        "lower80": 0.32,
        "upper80": 0.77
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.504,
        "lower80": 0.37,
        "upper80": 0.64
      },
      "selective_product_yield": {
        "estimate": 0.25,
        "lower80": 0.11,
        "upper80": 0.42
      },
      "transport_efficiency": {
        "estimate": 0.55,
        "lower80": 0.32,
        "upper80": 0.77
      }
    }
  ],
  "rationale": "The 0.48 mol/L query loading is close to the studied 0.50 mol/L loading. Predictions interpolate the observed ±1 V behavior to ±0.8 V and extend the measured time trends to 7200 s. Positive polarity is assigned the high-selectivity pathway; negative polarity retains lower faradaic, transport, and energy efficiency. Effects of E1, E3, and S2 are conservatively apportioned from confounded paired-formulation results, while 500 mA includes the observed high-cap efficiency penalty. Intervals combine assay noise with wider uncertainty for time extrapolation, unseen solvent/electrolyte combinations, and the untested positive-polarity high-current interaction."
}
```
