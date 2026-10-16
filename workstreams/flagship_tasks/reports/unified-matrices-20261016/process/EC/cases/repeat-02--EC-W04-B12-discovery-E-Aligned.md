# repeat-02/EC-W04-B12-discovery-E-Aligned

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-02\EC-W04-B12-discovery-E-Aligned\participant\discovery-E-Aligned

## 同期笔记

### v1 · 公开事件 0

# Electrochemical campaign hypotheses

## Pre-experiment expectations
**H1 [tentative].** At fixed loading (0.040 mol reagent in 0.080 L solvent), conversion should rise with electrolysis duration and with sufficient absolute driving potential, but selectivity and energy efficiency may peak at an intermediate drive because excessive potential promotes side reactions.

**H2 [tentative].** Potential response should depend on the combined solvent/electrolyte standard-potential shifts; comparisons will therefore include both potential signs and multiple material pairs. Current is a cap, so observed cap dependence may reflect either current limitation or a plateau in delivered current.

**H3 [tentative].** Nominal conductivity/diffusivity predict transport/ohmic metrics, while proton activity and precipitation propensity may modify selectivity. Planned tests include duration, current cap, polarity, and material contrasts. A UV-vis snapshot will be used in each batch before termination to provide a consistent intermediate diagnostic.

A result pattern that is nonmonotonic in potential, insensitive to current above some cap, or strongly shifted across materials will narrow these claims.

### v2 · 公开事件 84

# Electrochemical campaign hypotheses — final source-stage synthesis

All conclusions are restricted to the tested fixed loading: 0.040 mol reagent in 0.080 L solvent (nominal 0.50 mol/L), single electrolysis segments, and the public synthetic benchmark.

## H1 [supported in a restricted regime]
At solvent-S0/electrolyte-E0, +1.0 V and a 100 mA cap, a very long electrolysis produces substantially more target than short runs. The 14,400 s batch gave selective-product yield 0.131 and conversion 0.113 (runner-operation-0063), whereas 60–1,800 s batches remained near the assay floor (runner-operation-0014, -0007, -0021). The small non-monotonic differences among the short runs are not evidence against a duration effect because they are comparable to stated assay noise and the signals are near zero.

Testable consequence: at this loading and moderate current cap, increasing duration from the short regime toward 14,400 s should raise conversion/yield, though saturation was not located.

## H2 [supported; threshold/overdrive interpretation unresolved]
The current cap is not simply “more is better.” At +1.0 V in S0/E0, raising the cap from 100 to 500 mA produced very low faradaic/transport efficiencies and near-zero yield at 3,600–14,400 s (runner-operation-0035, -0042), while 100 mA for 14,400 s retained faradaic efficiency 0.607, transport efficiency 0.628, selectivity 0.981, and yield 0.131 (runner-operation-0063). This is consistent with a high-current parasitic pathway or transport-limited regime; because delivered current was not directly observed, a cap-dependent control response remains an alternative.

Testable consequence: blind conditions at 500 mA, especially long duration, should show poorer faradaic/transport efficiency than otherwise similar 100 mA conditions.

## H3 [supported for polarity at one matched condition; magnitude unresolved]
For S0/E0, 100 mA and 600 s, +1.0 V showed markedly higher energy/faradaic/transport efficiencies than -1.0 V (runner-operation-0007 versus -0028). Target-yield signals were near zero, so polarity effects on yield at short time remain unresolved. At 500 mA and 3,600 s, both +2.0 and -2.0 V were inefficient (runner-operation-0049, -0056); this does not isolate a smooth potential law because the high-current regime dominates.

## H4 [material dependence supported, attribution unresolved]
At +1.0 V, 100 mA, 14,400 s, matched material pairs differed substantially (runner-operation-0063, -0070, -0077, -0084). S2/E2 gave the strongest observed balanced result: yield 0.133, conversion 0.162, selectivity 0.879, faradaic efficiency 0.797, transport efficiency 0.805, and energy efficiency 0.837 (runner-operation-0077). S1/E1 had similar conversion and strong efficiencies but lower yield/selectivity; S3/E3 was clearly weaker. S2/E2 also showed minimal precipitation signal, unlike S0/E0. These pairwise changes confound solvent and electrolyte, so they establish material-pair effects but cannot assign causality to either component or a single dossier property.

## Predictive working account
Useful target production requires the productive potential sign, enough charge/time, and avoidance of a high-cap transport/parasitic regime. Material pairs shift transport, proton/precipitation environment, and effective potential; the S2/E2 pair best balanced these factors in the tested long-duration moderate-cap regime. The account is qualitative rather than a fitted kinetic law because the design has no true replicates and sparse potential/current levels. A crossed solvent/electrolyte study and intermediate current caps would most efficiently distinguish material causality and locate the current threshold.

## Decision
Recommend batch 11 (runner-operation-0077) for the secondary operating readout because it achieved the highest public balanced score and the strongest combined conversion, yield, energy, faradaic, and transport metrics without approaching the safety limit. This would change if repeat measurements showed its apparent advantage over batch 9 or 10 was not reproducible.

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
    "cost": 0.3524399995803833,
    "electrochemical_conversion": 0.013086915947496891,
    "electrochemical_selectivity": 1.0,
    "energy_efficiency": 0.6831510066986084,
    "faradaic_efficiency": 0.6771227121353149,
    "ohmic_efficiency": 0.9572166204452515,
    "pH_normalized": 0.23443032801151276,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.6484189629554749
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
      "potential_V": 1
    },
    {
      "duration_s": 60,
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
    "cost": 0.3522239923477173,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 1.0,
    "energy_efficiency": 0.6661815047264099,
    "faradaic_efficiency": 0.6539456248283386,
    "ohmic_efficiency": 0.9660544395446777,
    "pH_normalized": 0.2317349761724472,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.22596263885498047,
    "selective_product_yield": 0.009483265690505505,
    "transport_efficiency": 0.6802024841308594
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
    "cost": 0.3529199957847595,
    "electrochemical_conversion": 0.00958786066621542,
    "electrochemical_selectivity": 0.9767236113548279,
    "energy_efficiency": 0.6682271361351013,
    "faradaic_efficiency": 0.6216338872909546,
    "ohmic_efficiency": 0.952828049659729,
    "pH_normalized": 0.2324499785900116,
    "precipitation_signal": 0.9863388538360596,
    "safety_risk": 0.072194404900074,
    "score": 0.09629775583744049,
    "selective_product_yield": 0.004154444206506014,
    "transport_efficiency": 0.638190746307373
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
    "cost": 0.3524399995803833,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.6219521760940552,
    "energy_efficiency": 0.2525532841682434,
    "faradaic_efficiency": 0.45584696531295776,
    "ohmic_efficiency": 0.9649862051010132,
    "pH_normalized": 0.23175939917564392,
    "precipitation_signal": 0.9870871305465698,
    "safety_risk": 0.072194404900074,
    "score": 0.04522924870252609,
    "selective_product_yield": 0.0029523202683776617,
    "transport_efficiency": 0.42435941100120544
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
      "current_mA": 500,
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
    "cost": 0.3594000041484833,
    "electrochemical_conversion": 0.0034490374382585287,
    "electrochemical_selectivity": 0.006436008028686047,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.01102422270923853,
    "ohmic_efficiency": 0.829846203327179,
    "pH_normalized": 0.23672018945217133,
    "precipitation_signal": 0.9864134788513184,
    "safety_risk": 0.072194404900074,
    "score": 0.030311280861496925,
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
    "cost": 0.38100001215934753,
    "electrochemical_conversion": 0.0021511756349354982,
    "electrochemical_selectivity": 0.0042426493018865585,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.02405594103038311,
    "ohmic_efficiency": 0.8317029476165771,
    "pH_normalized": 0.2334442436695099,
    "precipitation_signal": 0.997043788433075,
    "safety_risk": 0.072194404900074,
    "score": 0.03792485594749451,
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
      "potential_V": 2
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
    "cost": 0.36660000681877136,
    "electrochemical_conversion": 0.010353217832744122,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 5.735348167945631e-05,
    "faradaic_efficiency": 0.0021574273705482483,
    "ohmic_efficiency": 0.9473733305931091,
    "pH_normalized": 0.23245882987976074,
    "precipitation_signal": 0.9820858836174011,
    "safety_risk": 0.072194404900074,
    "score": 0.029109057039022446,
    "selective_product_yield": 0.007292202208191156,
    "transport_efficiency": 0.005557783879339695
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
      "current_mA": 500,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -2
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
    "cost": 0.36660000681877136,
    "electrochemical_conversion": 0.02504274994134903,
    "electrochemical_selectivity": 0.5300207138061523,
    "energy_efficiency": 0.031636714935302734,
    "faradaic_efficiency": 0.1369275599718094,
    "ohmic_efficiency": 0.9326693415641785,
    "pH_normalized": 0.2307613641023636,
    "precipitation_signal": 0.994958758354187,
    "safety_risk": 0.072194404900074,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.13043221831321716
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
    "cost": 0.3579599857330322,
    "electrochemical_conversion": 0.11300060898065567,
    "electrochemical_selectivity": 0.9808417558670044,
    "energy_efficiency": 0.6712485551834106,
    "faradaic_efficiency": 0.6072558164596558,
    "ohmic_efficiency": 0.9960755705833435,
    "pH_normalized": 0.23277513682842255,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.5137727856636047,
    "selective_product_yield": 0.13097913563251495,
    "transport_efficiency": 0.6280871033668518
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
      "solvent": 1,
      "volume_L": 0.08
    },
    {
      "current_mA": 100,
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
    "cost": 0.38995999097824097,
    "electrochemical_conversion": 0.1584090292453766,
    "electrochemical_selectivity": 0.8042500019073486,
    "energy_efficiency": 0.7592618465423584,
    "faradaic_efficiency": 0.7757596969604492,
    "ohmic_efficiency": 0.937464714050293,
    "pH_normalized": 0.2037143111228943,
    "precipitation_signal": 0.7153439521789551,
    "safety_risk": 0.09559440612792969,
    "score": 0.5291305780410767,
    "selective_product_yield": 0.10987874865531921,
    "transport_efficiency": 0.7771092653274536
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
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "current_mA": 100,
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
    "cost": 0.4411599934101105,
    "electrochemical_conversion": 0.16181080043315887,
    "electrochemical_selectivity": 0.8786922097206116,
    "energy_efficiency": 0.8368596434593201,
    "faradaic_efficiency": 0.7974506616592407,
    "ohmic_efficiency": 0.9311953186988831,
    "pH_normalized": 0.17381398379802704,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.1135944053530693,
    "score": 0.564136803150177,
    "selective_product_yield": 0.13323388993740082,
    "transport_efficiency": 0.8046305775642395
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
      "solvent": 3,
      "volume_L": 0.08
    },
    {
      "current_mA": 100,
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
    "cost": 0.40915998816490173,
    "electrochemical_conversion": 0.05765271186828613,
    "electrochemical_selectivity": 0.7331938147544861,
    "energy_efficiency": 0.5674875378608704,
    "faradaic_efficiency": 0.3628753125667572,
    "ohmic_efficiency": 0.9823869466781616,
    "pH_normalized": 0.278285413980484,
    "precipitation_signal": 0.0,
    "safety_risk": 0.12619440257549286,
    "score": 0.3814053237438202,
    "selective_product_yield": 0.06663944572210312,
    "transport_efficiency": 0.3841002583503723
  }
}
```

## K1 封存报告

# Mechanism report

## 1. Empirical picture

This world behaves like an electrochemical conversion with three coupled controls:

1. **Charge/time must be sufficient to produce appreciable conversion.**
2. **The productive current fraction collapses in an excessive-current regime.**
3. **The solvent/electrolyte pair changes mass transport, interfacial kinetics, acid/precipitation behavior, and the effective potential.**

All experiments used 0.040 mol reagent in 0.080 L solvent, corresponding to a nominal initial concentration of 0.50 mol/L. Thus, conclusions apply only to this loading and batch geometry.

## 2. Proposed process model

A useful conceptual model is

- effective overpotential:
  `eta = E_applied - E0_base - shift_solvent - shift_electrolyte - i*R`,
- transport-limited current:
  `i_lim ∝ D_eff*C/(diffusion-layer thickness)`,
- delivered current:
  `i = min(i_cap, i_kinetic(eta), i_lim)`,
- productive current:
  `i_product = i * FE(eta, i/i_lim, medium, proton activity, precipitation)`,
- conversion:
  `X(t) ≈ 1 - exp[-k_Q * integral(i_product dt)/n_reagent]`,
- target yield:
  `Y_target ≈ X * S_product`, subject to measurement noise and possible product loss.

Here `FE` is faradaic efficiency and `S_product` is chemical selectivity. I do not claim that the simulator literally implements these equations; they summarize the observed dependencies.

The configured current is a cap, not a measured current. Therefore, `i_cap*t` is only an upper bound on charge. For example, the upper-bound charges were 6, 60, 180, and 1440 C for the 100 mA experiments lasting 60, 600, 1800, and 14,400 s, respectively. The 500 mA experiments had upper bounds of 1800 C at 3600 s and 7200 C at 14,400 s. Actual delivered current, electrode area, and current density were not observed.

## 3. Time and charge dependence at moderate current

The clearest duration comparison used solvent-S0/electrolyte-E0, +1.0 V, and a 100 mA cap:

- **Batch 2, 60 s:** conversion 0, yield 0.00948, selectivity 1.000, faradaic efficiency 0.654, transport efficiency 0.680, energy efficiency 0.666.
- **Batch 1, 600 s:** conversion 0.0131, yield 0, selectivity 1.000, faradaic efficiency 0.677, transport efficiency 0.648, energy efficiency 0.683.
- **Batch 3, 1800 s:** conversion 0.00959, yield 0.00415, selectivity 0.977, faradaic efficiency 0.622, transport efficiency 0.638, energy efficiency 0.668.
- **Batch 9, 14,400 s:** conversion 0.113, yield 0.131, selectivity 0.981, faradaic efficiency 0.607, transport efficiency 0.628, energy efficiency 0.671.

The small, nonmonotonic differences among Batches 1–3 are near the assay floor and comparable to the declared channel noise. They do not establish fine short-time kinetics. Batch 9, however, gives a much larger target signal and supports the conclusion that sufficient duration or cumulative productive charge is required.

The near-constant efficiency metrics across these four durations suggest that the 100 mA regime maintains approximately the same operating mode while conversion accumulates. A plausible extrapolation is that conversion would continue increasing beyond the short-time regime before eventually saturating, but the campaign did not locate that saturation point.

The fact that Batch 9 yield (0.131) is slightly greater than its reported conversion (0.113) shows that the processed assay channels should not be treated as exact algebraic identities. Their difference is plausibly due to independent measurement noise or channel-specific process proxies. I therefore use `yield ≈ conversion × selectivity` only as a conceptual relationship.

## 4. High-current collapse

The most important mechanistic change was caused by raising the cap from 100 to 500 mA. With S0/E0 at +1.0 V:

- **Batch 5, 500 mA, 3600 s:** conversion 0.00345, yield 0.00847, selectivity 0.00644, faradaic efficiency 0.0110, transport efficiency 0.000515, energy efficiency 0, and ohmic efficiency 0.830.
- **Batch 6, 500 mA, 14,400 s:** conversion 0.00215, yield 0.0103, selectivity 0.00424, faradaic efficiency 0.0241, transport efficiency 0, energy efficiency 0, and ohmic efficiency 0.832.

Thus, despite much larger possible charge, these batches produced essentially no useful conversion. Longer operation did not rescue Batch 6. This rejects a simple model in which target production depends only on `current cap × time`.

My leading explanation is entry into a transport-limited or parasitic-current regime. When demanded current substantially exceeds the productive transport rate, most current goes to side reactions, double-layer charging, or other nonproductive pathways. Increased `iR` loss is visible in the reduction of ohmic efficiency from approximately 0.96–1.00 in moderate-current runs to about 0.83 in Batches 5 and 6, but ohmic loss alone is too small to explain faradaic efficiency near zero. The dominant failure is therefore probably chemical or transport selectivity rather than simple resistance.

An alternative is that the current controller delivers a qualitatively different waveform or operating state at a 500 mA cap. Since actual current was not measured, the campaign cannot distinguish controller behavior from intrinsic electrochemical side reactions.

## 5. Potential polarity and magnitude

A matched polarity comparison exists at S0/E0, 100 mA, and 600 s:

- **Batch 1, +1.0 V:** selectivity 1.000, faradaic efficiency 0.677, transport efficiency 0.648, and energy efficiency 0.683.
- **Batch 4, -1.0 V:** selectivity 0.622, faradaic efficiency 0.456, transport efficiency 0.424, and energy efficiency 0.253.

Both target-yield measurements were close to zero at this short duration, so this comparison does not prove a yield difference. It does show that positive polarity better supports the productive electrochemical state under these conditions.

Potential magnitude was probed at 500 mA and is consequently confounded with high-current failure:

- **Batch 7, +2.0 V, 3600 s:** conversion 0.0104, yield 0.00729, selectivity 0, faradaic efficiency 0.00216, transport efficiency 0.00556, and energy efficiency 0.000057.
- **Batch 8, -2.0 V, 3600 s:** conversion 0.0250, yield 0, selectivity 0.530, faradaic efficiency 0.137, transport efficiency 0.130, and energy efficiency 0.0316.

Both were poor. Batch 8 retained more non-target electrochemical activity, but its target yield was zero. These results are consistent with potential-dependent side pathways, although they do not identify an optimum potential or a quantitative Tafel relationship. A smooth potential law cannot be inferred because there were no moderate-current measurements spanning several potentials.

## 6. Material-pair effects

Batches 9–12 provide the most informative material comparison: all used +1.0 V, 100 mA, 14,400 s, and the same reagent concentration.

- **Batch 9, S0/E0:** conversion 0.113, yield 0.131, selectivity 0.981, faradaic efficiency 0.607, transport efficiency 0.628, energy efficiency 0.671, ohmic efficiency 0.996, normalized pH 0.233, precipitation signal 1.000.
- **Batch 10, S1/E1:** conversion 0.158, yield 0.110, selectivity 0.804, faradaic efficiency 0.776, transport efficiency 0.777, energy efficiency 0.759, ohmic efficiency 0.937, normalized pH 0.204, precipitation signal 0.715.
- **Batch 11, S2/E2:** conversion 0.162, yield 0.133, selectivity 0.879, faradaic efficiency 0.797, transport efficiency 0.805, energy efficiency 0.837, ohmic efficiency 0.931, normalized pH 0.174, precipitation signal 0.00524.
- **Batch 12, S3/E3:** conversion 0.0577, yield 0.0666, selectivity 0.733, faradaic efficiency 0.363, transport efficiency 0.384, energy efficiency 0.567, ohmic efficiency 0.982, normalized pH 0.278, precipitation signal 0.

These observations demonstrate a strong material-pair dependence. Batch 11 had the best combined conversion and efficiency metrics. Batch 10 was also transport-efficient but less selective. Batch 9 was highly selective but suffered strong precipitation and lower conversion. Batch 12 was weak despite no detected precipitation.

The dossier gives a plausible transport explanation. Electrolyte-E2 has a comparatively thin nominal diffusion layer of 0.48 mm, which could compensate for its modest bulk conductivity and support the high observed transport efficiency in Batch 11. Electrolyte-E3 has high nominal conductivity but a much thicker 2.8 mm diffusion layer; Batch 12 consequently had good ohmic efficiency but poor transport and faradaic efficiencies. This separates ohmic conduction from reagent/product mass transport: high conductivity alone does not guarantee productive conversion.

Precipitation is also coupled but is not the sole control. Moving from Batch 9 to Batch 11 reduced the precipitation signal from 1.000 to 0.005 while increasing conversion and transport efficiency. However, Batch 12 had zero precipitation and still performed poorly. Precipitation may sequester reagent or product, block an interface, or simply correlate with acid and material identity. The data support it as one loss mechanism, not the master variable.

Nominal standard-potential shifts cannot alone explain the material ranking. S2/E2 and S3/E3 have the same summed nominal shift of approximately +0.38 V, yet their results differ sharply. Therefore, diffusivity, diffusion-layer thickness, proton activity, capacitance, hidden material residuals, or pair-specific interfacial kinetics must matter in addition to potential alignment.

The normalized-pH ordering also correlates imperfectly with performance. Batch 11 had the lowest value and performed best, but only four paired materials were tested. Proton activity may affect reaction kinetics, selectivity, and precipitation, but the campaign cannot identify a causal pH law.

## 7. Interpretation of efficiency channels

The observations suggest distinct loss factors rather than one general efficiency:

- **Ohmic efficiency** remained high for the long 100 mA material comparison (0.931–0.996), so resistance was not normally the principal limitation.
- **Transport efficiency** tracked productive behavior more closely: 0.805 in Batch 11 versus 0.384 in Batch 12 and approximately zero in high-current Batches 5–7.
- **Faradaic efficiency** followed transport efficiency, consistent with insufficient reactant transport diverting current to parasitic chemistry.
- **Energy efficiency** combined these effects and was highest in Batch 11 at 0.837.
- **Chemical selectivity** could remain high even when conversion was low, as in short S0/E0 runs, showing that selectivity alone does not imply useful productivity.

A plausible multiplicative representation is

`useful energy performance ≈ ohmic efficiency × transport factor × faradaic/chemical factor`,

but the reported channels should not be assumed to multiply exactly because they are independently processed observables.

## 8. Safety and the public score

Observed safety risk was well below the 0.65 limit in every reported batch. It was about 0.072 for the S0 experiments and rose across the material comparison to 0.0956 in Batch 10, 0.1136 in Batch 11, and 0.126 in Batch 12. This appears to contain a material-dependent contribution, but no experiment isolated its origin.

The public balanced scores for the long moderate-current material runs were 0.514, 0.529, 0.564, and 0.381 for Batches 9–12. These scores agree qualitatively with the mechanistic interpretation, but they are composite secondary observations rather than direct mechanistic variables.

## 9. What formed or changed the explanation

The initial working expectation was that conversion would increase with charge and that excessive driving force might reduce selectivity. Batches 1–3 showed that short experiments were largely below the productive signal range. Batch 4 established a polarity effect on efficiency. Batches 5 and 6 changed the explanation most strongly: their failure despite large possible charge required a current-dependent transport or side-reaction term rather than simple charge integration. Batches 7 and 8 showed that larger absolute potential did not overcome this failed regime.

Batch 9 then showed that long duration is productive when the current cap remains moderate. Finally, Batches 10–12 demonstrated that material choice shifts conversion, efficiency, precipitation, and pH. Batch 11 supported a coupled transport/interfacial account, while the poor result of Batch 12 despite high conductivity, high ohmic efficiency, no precipitation, and the same nominal potential shift as Batch 11 ruled out explanations based on any one of those properties alone.

## 10. Scope, unidentifiable factors, and alternatives

The following remain unidentifiable from this campaign:

- actual current and time-dependent current response;
- electrode area, current density, gap, and contact resistance;
- electron stoichiometry of target formation;
- kinetic rate constants, exchange current, and a Tafel slope;
- the individual effects of solvent versus electrolyte, because Batches 9–12 changed them together;
- material-specific hidden residuals and solvent/electrolyte interactions;
- whether precipitation consumes reagent, traps product, passivates an electrode, or is merely correlated with another property;
- whether poor high-current results arise from transport limitation, product degradation, competing redox chemistry, or controller behavior;
- whether target yield eventually saturates or declines at very long moderate-current operation;
- reproducibility, because no exact batch was replicated.

Declared assay noise is material near zero: approximately 0.006 for yield, 0.010 for conversion, 0.012 for selectivity/faradaic efficiency, 0.014 for transport efficiency, and 0.016 for energy efficiency. Small differences among near-zero batches should not be overinterpreted. Conversely, the large efficiency collapses at 500 mA and the broad material differences exceed these nominal noise scales, although process variability was not independently estimated.

Plausible alternative mechanisms include direct product degradation at high cumulative charge, a sharp interfacial transition induced by high current, material-dependent changes in the true equilibrium potential, and precipitation-driven electrode passivation. The present evidence favors a transport-coupled parasitic-current account because transport and faradaic efficiencies collapse together, while ohmic efficiency remains substantially higher. It does not uniquely prove that account.

In summary, my best explanatory model is a charge-accumulating productive reaction that operates efficiently only within a moderate-current, correctly polarized window. Solvent and electrolyte jointly set effective overpotential, mass-transfer capacity, proton/precipitation conditions, and interfacial selectivity. Exceeding the transport-compatible current diverts charge away from target production, whereas insufficient duration leaves conversion near the detection/noise floor. This model explains the major observations but remains qualitative outside the tested 0.50 mol/L loading, material pairs, and discrete operating conditions.

## K2 封存报告

1. No instance-specific prior law or parameter set was supplied. The only prior information was the nominal material-property dossier, which I treated as mechanistic context rather than a response law.

Supported claims:
- The restricted duration/charge claim was supported: at S0/E0, +1.0 V and 100 mA, Batch 9 at 14,400 s gave yield 0.131 and conversion 0.113, whereas Batches 1–3 at 60–1,800 s remained near zero. This changed my view from an initially unresolved time effect to a supported long-versus-short effect, though not a fitted kinetic law.
- The proposed high-current penalty was strongly supported. Batches 5 and 6 at +1.0 V and 500 mA had near-zero faradaic, transport and energy efficiencies despite large possible charge. This contradicted a simple law based only on current × time and motivated the transport-limited/parasitic-current explanation.
- A polarity effect was supported at one matched condition: Batch 1 (+1.0 V) had substantially higher faradaic, transport and energy efficiencies than Batch 4 (-1.0 V), both at 100 mA and 600 s. Their yields were near the noise floor, so a polarity effect on yield itself remained unresolved.
- Material-pair dependence was supported by Batches 9–12. Batch 11 (S2/E2) had the strongest combined efficiencies and conversion, whereas Batch 12 (S3/E3) was much weaker under otherwise matched controls.

Contradicted or narrowed claims:
- “More current gives more product” was contradicted by Batches 5–6 versus Batch 9.
- Nominal conductivity alone was contradicted as an adequate predictor: Batch 12 retained high ohmic efficiency but poor transport and faradaic efficiencies.
- Absence of precipitation alone was contradicted as a sufficient condition for strong performance: Batch 12 had precipitation signal 0 but performed poorly. Conversely, Batch 9 performed reasonably despite precipitation signal 1.
- A single summed standard-potential shift was inadequate because the nominally similar combined shifts for S2/E2 and S3/E3 accompanied very different outcomes in Batches 11 and 12.

Untested claims include the exact exponential conversion equation, the location of a current threshold, a Tafel or smooth potential law, eventual saturation or product decay at long moderate-current duration, separable solvent and electrolyte effects, and reproducibility. The +2/-2 V observations in Batches 7–8 were confounded by the 500 mA regime and did not constitute a clean potential scan.

2. I would run one staged S0/E0 batch at the original 0.040 mol/0.080 L loading and +1.0 V: first 14,400 s at 100 mA, then switch to 500 mA for an additional 3,600 s, with UV-vis immediately before and after the switch and a final assay after termination. Existing Batch 9 supplies the matched endpoint before the added high-current stage.

If final target yield remained near Batch 9’s 0.131 while the post-switch transport/faradaic indicators collapsed, I would strengthen the leading interpretation that high current mainly diverts new charge into parasitic pathways without rapidly destroying accumulated target. If yield fell clearly below Batch 9 beyond measurement uncertainty, I would favor the alternative that high current degrades product or reverses productive chemistry. If yield rose substantially, I would weaken the claim that 500 mA is intrinsically unproductive and instead suspect state dependence, induction, or current-controller behavior in Batches 5–6. This experiment would not fully separate intrinsic electrochemistry from controller behavior because actual current is not directly measured, but it would distinguish diversion from target destruction more sharply than another endpoint-only high-current batch.

3. The largest unused evidence source was the raw characterization content. I used processed final-assay values and selected intermediate UV-vis estimates but did not inspect or model the complete raw spectra, peak assignments, mass-balance packets, replicate signals, baselines, or drift information. I also did not quantitatively exploit all nominal capacitance, acid/pKa, diffusivity, solubility-product, and conductivity values because the design did not independently vary them. Cost, temperature changes, and most safety variation were not central to the mechanism analysis.

The least reliable predictions are Q05–Q10 because they use solvent/electrolyte combinations not isolated in the campaign, and Q11–Q12 because they extrapolate the high-current collapse to ±0.8 V, a lower reagent amount, and a new duration. Q01–Q02 are also uncertain because short-run yields lie near the assay noise floor and the score’s yield gate amplifies small errors. Predictions for positive-polarity, 100 mA, long-duration conditions are comparatively better grounded.

The Batch 11 recommendation is reliable only as a selection among observed batches at the tested loading and operating condition. Its general superiority is less reliable: it had no replicate, solvent and electrolyte effects were confounded, and its yield of 0.133 was almost indistinguishable from Batch 9’s 0.131 even though its conversion and efficiency metrics were stronger.

The explanatory research goal encouraged broad contrasts in duration, polarity, current and materials rather than repeated optimization around one point. That improved mechanism discovery, especially the identification of the 500 mA failure regime, but left too few batches for replication, crossed material factors, or a dense potential/current response surface. The secondary score influenced the final recommendation and the decision to examine long, moderate-current material pairs, but I found no clear conflict in which optimization caused evidence to be suppressed or misreported.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.4,
        "upper80": 0.75
      },
      "energy_efficiency": {
        "estimate": 0.25,
        "lower80": 0.12,
        "upper80": 0.38
      },
      "faradaic_efficiency": {
        "estimate": 0.44,
        "lower80": 0.3,
        "upper80": 0.56
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.167,
        "lower80": 0.0,
        "upper80": 0.32
      },
      "selective_product_yield": {
        "estimate": 0.011,
        "lower80": 0.0,
        "upper80": 0.03
      },
      "transport_efficiency": {
        "estimate": 0.42,
        "lower80": 0.28,
        "upper80": 0.56
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.95,
        "lower80": 0.85,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.64,
        "lower80": 0.5,
        "upper80": 0.74
      },
      "faradaic_efficiency": {
        "estimate": 0.65,
        "lower80": 0.53,
        "upper80": 0.75
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.47,
        "lower80": 0.35,
        "upper80": 0.56
      },
      "selective_product_yield": {
        "estimate": 0.032,
        "lower80": 0.012,
        "upper80": 0.06
      },
      "transport_efficiency": {
        "estimate": 0.64,
        "lower80": 0.5,
        "upper80": 0.74
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.45,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.24,
        "lower80": 0.12,
        "upper80": 0.36
      },
      "faradaic_efficiency": {
        "estimate": 0.44,
        "lower80": 0.32,
        "upper80": 0.55
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.321,
        "lower80": 0.2,
        "upper80": 0.43
      },
      "selective_product_yield": {
        "estimate": 0.05,
        "lower80": 0.02,
        "upper80": 0.09
      },
      "transport_efficiency": {
        "estimate": 0.42,
        "lower80": 0.3,
        "upper80": 0.54
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.94,
        "lower80": 0.87,
        "upper80": 0.99
      },
      "energy_efficiency": {
        "estimate": 0.64,
        "lower80": 0.53,
        "upper80": 0.74
      },
      "faradaic_efficiency": {
        "estimate": 0.6,
        "lower80": 0.5,
        "upper80": 0.7
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.518,
        "lower80": 0.43,
        "upper80": 0.59
      },
      "selective_product_yield": {
        "estimate": 0.17,
        "lower80": 0.11,
        "upper80": 0.24
      },
      "transport_efficiency": {
        "estimate": 0.62,
        "lower80": 0.51,
        "upper80": 0.71
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.42,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.31,
        "lower80": 0.17,
        "upper80": 0.45
      },
      "faradaic_efficiency": {
        "estimate": 0.52,
        "lower80": 0.38,
        "upper80": 0.65
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.354,
        "lower80": 0.23,
        "upper80": 0.46
      },
      "selective_product_yield": {
        "estimate": 0.058,
        "lower80": 0.025,
        "upper80": 0.1
      },
      "transport_efficiency": {
        "estimate": 0.55,
        "lower80": 0.4,
        "upper80": 0.68
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.82,
        "lower80": 0.7,
        "upper80": 0.91
      },
      "energy_efficiency": {
        "estimate": 0.73,
        "lower80": 0.6,
        "upper80": 0.83
      },
      "faradaic_efficiency": {
        "estimate": 0.76,
        "lower80": 0.62,
        "upper80": 0.86
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.553,
        "lower80": 0.44,
        "upper80": 0.64
      },
      "selective_product_yield": {
        "estimate": 0.18,
        "lower80": 0.11,
        "upper80": 0.27
      },
      "transport_efficiency": {
        "estimate": 0.78,
        "lower80": 0.64,
        "upper80": 0.87
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.47,
        "lower80": 0.3,
        "upper80": 0.63
      },
      "energy_efficiency": {
        "estimate": 0.16,
        "lower80": 0.06,
        "upper80": 0.29
      },
      "faradaic_efficiency": {
        "estimate": 0.28,
        "lower80": 0.15,
        "upper80": 0.42
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.25,
        "lower80": 0.12,
        "upper80": 0.38
      },
      "selective_product_yield": {
        "estimate": 0.025,
        "lower80": 0.005,
        "upper80": 0.06
      },
      "transport_efficiency": {
        "estimate": 0.3,
        "lower80": 0.16,
        "upper80": 0.44
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.72,
        "lower80": 0.56,
        "upper80": 0.84
      },
      "energy_efficiency": {
        "estimate": 0.55,
        "lower80": 0.4,
        "upper80": 0.68
      },
      "faradaic_efficiency": {
        "estimate": 0.43,
        "lower80": 0.29,
        "upper80": 0.57
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.396,
        "lower80": 0.27,
        "upper80": 0.5
      },
      "selective_product_yield": {
        "estimate": 0.075,
        "lower80": 0.035,
        "upper80": 0.13
      },
      "transport_efficiency": {
        "estimate": 0.42,
        "lower80": 0.28,
        "upper80": 0.57
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.5,
        "lower80": 0.32,
        "upper80": 0.68
      },
      "energy_efficiency": {
        "estimate": 0.22,
        "lower80": 0.09,
        "upper80": 0.36
      },
      "faradaic_efficiency": {
        "estimate": 0.38,
        "lower80": 0.24,
        "upper80": 0.52
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.291,
        "lower80": 0.15,
        "upper80": 0.43
      },
      "selective_product_yield": {
        "estimate": 0.035,
        "lower80": 0.01,
        "upper80": 0.08
      },
      "transport_efficiency": {
        "estimate": 0.45,
        "lower80": 0.3,
        "upper80": 0.6
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.9,
        "lower80": 0.78,
        "upper80": 0.97
      },
      "energy_efficiency": {
        "estimate": 0.72,
        "lower80": 0.58,
        "upper80": 0.82
      },
      "faradaic_efficiency": {
        "estimate": 0.65,
        "lower80": 0.5,
        "upper80": 0.78
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.52,
        "lower80": 0.4,
        "upper80": 0.62
      },
      "selective_product_yield": {
        "estimate": 0.15,
        "lower80": 0.08,
        "upper80": 0.23
      },
      "transport_efficiency": {
        "estimate": 0.62,
        "lower80": 0.48,
        "upper80": 0.75
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.45,
        "lower80": 0.2,
        "upper80": 0.65
      },
      "energy_efficiency": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "faradaic_efficiency": {
        "estimate": 0.08,
        "lower80": 0.01,
        "upper80": 0.2
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.056,
        "lower80": 0.0,
        "upper80": 0.18
      },
      "selective_product_yield": {
        "estimate": 0.007,
        "lower80": 0.0,
        "upper80": 0.03
      },
      "transport_efficiency": {
        "estimate": 0.07,
        "lower80": 0.0,
        "upper80": 0.18
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.12
      },
      "energy_efficiency": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.03
      },
      "faradaic_efficiency": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.022,
        "lower80": 0.0,
        "upper80": 0.09
      },
      "selective_product_yield": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.025
      },
      "transport_efficiency": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.04
      }
    }
  ],
  "rationale": "The new concentration (0.48 mol/L) is close to the studied 0.50 mol/L regime. I scaled conversion and yield mainly by charge per mole, retained the observed advantage of positive polarity, and imposed the severe faradaic/transport collapse seen at a 500 mA cap. Electrolyte and crossed solvent effects were inferred from nominal transport, potential-shift, and precipitation properties; their intervals are wider because those combinations were not directly isolated. Score estimates apply the published weighted formula and selective-yield gate, while intervals include assay noise, sparse potential coverage, absent replicates, and uncertainty about delivered current."
}
```
