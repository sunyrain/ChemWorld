# repeat-03/EC-W02-B12-discovery-E-MisIndexed

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-03\EC-W02-B12-discovery-E-MisIndexed\participant\discovery-E-MisIndexed

## 同期笔记

### v1 · 公开事件 0

# Electrochemical hypothesis notebook

## Prior expectations (before batch 1)
H1 [tentative]: Product formation requires an effective overpotential whose threshold shifts additively with solvent and electrolyte standard-potential shifts. Conversion should rise with |effective driving potential| and electrolysis time, then saturate; excessive drive/time may reduce selectivity through degradation.

H2 [tentative]: Delivered current is limited by the smaller of the set cap and potential/ohmic/transport limits. Thus raising the current cap should matter only below a plateau. Higher conductivity should improve ohmic efficiency, whereas high diffusivity and thin diffusion layers should improve transport efficiency.

H3 [tentative]: Potential sign may select opposite productive/unproductive pathways rather than being symmetric. I will compare signs, magnitudes, durations, caps, and material pairs at fixed loading (0.02 mol in 0.04 L initially), using matched contrasts where possible.

Prediction for batch 1: a moderate positive potential in S0/E0 will give measurable conversion; later sign and magnitude contrasts will determine direction and threshold. Evidence that both signs behave similarly would weaken H3.

### v2 · 公开事件 35

# Electrochemical hypothesis notebook

## Prior expectations
At campaign start I expected an additive material-dependent potential threshold, saturating time response, current-cap plateau, and possible sign asymmetry.

## H1 [supported, narrowed]: positive-potential activity has a narrow window in S0/E0
At fixed 0.02 mol/0.04 L, 100 mA cap, 1800 s, +1.0 V produced high selectivity (~0.897) and high efficiencies but only ~0.052 conversion (final assay event runner-operation-0007). Reversing to -1.0 V sharply lowered efficiencies and conversion (runner-operation-0014), supporting polarity dependence. A +0.3 V condition was intermediate (runner-operation-0021), while +1.5 and +2.5 V essentially collapsed faradaic/transport efficiency and productive response (runner-operation-0028, runner-operation-0035). Thus response is not monotone in positive potential: a peak near +1 V is more plausible than a simple threshold-plus-saturation law.

Alternative: the collapse may reflect a hard parasitic-current onset rather than chemical degradation; final assays do not yet separate these. Testable consequence: material standard-potential shifts should translate the optimum voltage, while changing cap should alter collapse if it is current-driven.

## H2 [unresolved]: time and current-cap law
Predicted before new tests: at +1.0 V, extending time should raise conversion until reagent depletion/degradation; lowering the 100 mA cap substantially should lower conversion, while raising it may have little effect if another limit is active.

## H3 [supported in S0/E0]: sign asymmetry
The matched ±1 V contrast is much larger than final-assay uncertainty for efficiency metrics, but conversion/yield are near low absolute levels and noisy. I will not assume symmetry for blind predictions.

### v3 · 公开事件 77

# Electrochemical hypothesis notebook

## H1 [supported, scope: tested material pairs]: narrow positive potential window
Matched S0/E0 data support a response maximum near +1 V: -1, +0.3, +1, +1.5, and +2.5 V show strongly nonmonotone faradaic and transport efficiencies (final assay events runner-operation-0014, -0021, -0007, -0028, -0035). A parasitic-current onset is favored over gradual chemical degradation because collapse is abrupt between +1 and +1.5 V.

Nominal solvent+electrolyte standard-potential shifts were used to translate the applied potential for S1/E1, S2/E2, and S3/E3. All three translated conditions retained high selectivity (~0.86-0.88), but their faradaic/transport efficiencies differed substantially (runner-operation-0063, -0070, -0077), consistent with material transport/interface factors beyond potential shift. Because pair identity and adjusted voltage changed together, separate solvent and electrolyte effects remain unresolved.

## H2 [supported, local]: charge/time and current cap are distinct controls
At S0/E0, +1 V, 100 mA cap, extending 1800 to 7200 s raised conversion from ~0.052 to ~0.179 and selective yield from ~0.025 to ~0.167 while selectivity/efficiencies stayed high (runner-operation-0007 vs -0042). This is compatible with approximately accumulated productive charge before depletion. Lowering the cap to 10 mA reduced conversion (~0.015, runner-operation-0049). Raising it to 500 mA did not raise conversion over 100 mA but collapsed faradaic/transport efficiency (runner-operation-0056), indicating a useful cap plateau plus parasitic/transport penalty rather than guaranteed delivered current.

Prediction before batch 12: at +1 V, S0/E0, 100 mA, 14400 s, conversion should exceed the 7200 s value but grow sublinearly; selectivity may remain high if no late degradation occurs. A fall in selective yield or selectivity would instead mark over-electrolysis. This final test determines whether the 7200 s local law extrapolates to the full duration range.

## H3 [supported in S0/E0]: polarity asymmetry
The ±1 V contrast shows positive bias is the productive direction in the tested formulation. Material shifts may move the window but do not justify sign symmetry.

### v4 · 公开事件 84

# Electrochemical hypothesis notebook — source-stage final

## H1 [supported in tested scope]: narrow, sign-specific productive window
For 0.02 mol in 0.04 L S0 with E0, 100 mA cap and 1800 s, positive bias is productive but nonmonotone. The final-assay sequence at -1, +0.3, +1, +1.5 and +2.5 V (runner-operation-0014, -0021, -0007, -0028, -0035) places the useful window near +1 V. Both faradaic and transport efficiencies collapse abruptly above +1 V, favoring onset of a parasitic/interface regime over a monotone activation law. Negative bias is substantially worse, so potential magnitude alone is not predictive.

A useful phenomenological representation is a signed material-shifted voltage window: productive rate = charge-limited rate × a peaked window function of applied potential minus a material-dependent shift. Exact width/center are unresolved because only one dense voltage series was run (S0/E0).

## H2 [supported locally]: cumulative productive charge with cap-dependent efficiency
At S0/E0 and +1 V, 100 mA, conversion rose from ~0.052 (1800 s) to ~0.179 (7200 s) to ~0.337 (14400 s), while selective yield rose from ~0.025 to ~0.167 to ~0.325 (runner-operation-0007, -0042, -0084). The 14400 s result confirms continued, mildly sublinear accumulation without a selectivity crash; long electrolysis is not over-electrolysis within the tested range. Selectivity stayed about 0.87-0.90 and efficiencies remained high.

At 1800 s, reducing the current cap from 100 to 10 mA lowered conversion to ~0.015 (runner-operation-0049). Raising the cap to 500 mA left conversion near ~0.051 but reduced faradaic and transport efficiencies to ~0.25 and ~0.24 (runner-operation-0056). Therefore current_mA is a cap with a productive plateau around the tested 100 mA scale, not a delivered-current setting; excessive cap accesses parasitic/transport losses.

## H3 [supported qualitatively, coefficients unresolved]: material shifts plus independent transport/interface factors
I applied nominal solvent+electrolyte potential-shift corrections to paired S1/E1, S2/E2 and S3/E3 conditions. Each retained high selectivity (~0.86-0.88), but faradaic/transport efficiency decreased across the tested pairs (approximately 0.77/0.80, 0.69/0.69, 0.59/0.60; runner-operation-0063, -0070, -0077). This supports independent material effects beyond voltage translation. Because solvent, electrolyte, and adjusted voltage covaried, their individual coefficients and interactions remain unresolved; nominal conductivity alone did not rank observed efficiency.

Precipitation varied strongly by material: near 1 for E0-containing S0 batches, ~0.71 for S1/E1, and near 0 for S2/E2 and S3/E3. This is descriptive rather than causal because paired materials changed together. pH_normalized was largely time/cap-invariant within S0/E0 (~0.225-0.229), but material-dependent in paired tests.

## Recommended operating point
Batch 12 (S0/E0, +1 V, 100 mA cap, 14400 s, 0.02 mol in 0.04 L) is the strongest tested operating recommendation: highest selective yield (~0.325) and score (~0.672) with high selectivity and efficiencies. This recommendation is empirical within the tested loading; material-pair extrapolation should use the shifted peaked-window model and retain uncertainty about solvent/electrolyte interactions.

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
    "cost": 0.28332000970840454,
    "electrochemical_conversion": 0.05227825790643692,
    "electrochemical_selectivity": 0.8974339962005615,
    "energy_efficiency": 0.869667649269104,
    "faradaic_efficiency": 0.9735972285270691,
    "ohmic_efficiency": 0.9653005003929138,
    "pH_normalized": 0.22897005081176758,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.5663837790489197,
    "selective_product_yield": 0.02515225298702717,
    "transport_efficiency": 0.944893479347229
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
    "cost": 0.28332000970840454,
    "electrochemical_conversion": 0.009952208958566189,
    "electrochemical_selectivity": 0.575653076171875,
    "energy_efficiency": 0.2517053484916687,
    "faradaic_efficiency": 0.3857153058052063,
    "ohmic_efficiency": 0.9741383194923401,
    "pH_normalized": 0.22627469897270203,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.2838066816329956,
    "selective_product_yield": 0.019159242510795593,
    "transport_efficiency": 0.41197213530540466
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
      "potential_V": 0.3
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
    "cost": 0.28281599283218384,
    "electrochemical_conversion": 0.026750005781650543,
    "electrochemical_selectivity": 0.7445391416549683,
    "energy_efficiency": 0.6870166063308716,
    "faradaic_efficiency": 0.6649624705314636,
    "ohmic_efficiency": 0.9012727737426758,
    "pH_normalized": 0.22698970139026642,
    "precipitation_signal": 0.9871450662612915,
    "safety_risk": 0.072194404900074,
    "score": 0.30123937129974365,
    "selective_product_yield": 0.01364460214972496,
    "transport_efficiency": 0.6815193891525269
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
      "potential_V": 1.5
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
    "cost": 0.2836799919605255,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.02824951522052288,
    "ohmic_efficiency": 0.9815899729728699,
    "pH_normalized": 0.22629910707473755,
    "precipitation_signal": 0.987893283367157,
    "safety_risk": 0.072194404900074,
    "score": 0.003244058694690466,
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
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 2.5
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
    "cost": 0.28439998626708984,
    "electrochemical_conversion": 0.0034490374382585287,
    "electrochemical_selectivity": 0.006436008028686047,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.01102422270923853,
    "ohmic_efficiency": 0.9878400564193726,
    "pH_normalized": 0.23125991225242615,
    "precipitation_signal": 0.9872196912765503,
    "safety_risk": 0.072194404900074,
    "score": 0.03566121682524681,
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
      "current_mA": 100,
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
    "cost": 0.28547999262809753,
    "electrochemical_conversion": 0.17920774221420288,
    "electrochemical_selectivity": 0.891326904296875,
    "energy_efficiency": 0.8591160178184509,
    "faradaic_efficiency": 0.9731315970420837,
    "ohmic_efficiency": 0.974361002445221,
    "pH_normalized": 0.2279839664697647,
    "precipitation_signal": 0.9978500008583069,
    "safety_risk": 0.072194404900074,
    "score": 0.6202771067619324,
    "selective_product_yield": 0.1674012690782547,
    "transport_efficiency": 0.9484482407569885
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
      "current_mA": 10,
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
    "cost": 0.2826719880104065,
    "electrochemical_conversion": 0.014734047465026379,
    "electrochemical_selectivity": 0.8803371787071228,
    "energy_efficiency": 0.8803064227104187,
    "faradaic_efficiency": 0.9414592385292053,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.22699855268001556,
    "precipitation_signal": 0.9828920960426331,
    "safety_risk": 0.072194404900074,
    "score": 0.31041204929351807,
    "selective_product_yield": 0.01115830522030592,
    "transport_efficiency": 0.9448596239089966
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
    "cost": 0.28619998693466187,
    "electrochemical_conversion": 0.05083495005965233,
    "electrochemical_selectivity": 0.8893049359321594,
    "energy_efficiency": 0.2555781900882721,
    "faradaic_efficiency": 0.24753062427043915,
    "ohmic_efficiency": 0.888979971408844,
    "pH_normalized": 0.2253010869026184,
    "precipitation_signal": 0.9957649111747742,
    "safety_risk": 0.072194404900074,
    "score": 0.310484915971756,
    "selective_product_yield": 0.029144546017050743,
    "transport_efficiency": 0.24103528261184692
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
      "potential_V": 0.92
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
    "cost": 0.2992624044418335,
    "electrochemical_conversion": 0.03461761772632599,
    "electrochemical_selectivity": 0.8761370182037354,
    "energy_efficiency": 0.8740222454071045,
    "faradaic_efficiency": 0.7743602395057678,
    "ohmic_efficiency": 0.9814401268959045,
    "pH_normalized": 0.20722901821136475,
    "precipitation_signal": 0.7148279547691345,
    "safety_risk": 0.09559440612792969,
    "score": 0.5318101048469543,
    "selective_product_yield": 0.049556247889995575,
    "transport_efficiency": 0.7951915264129639
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
      "potential_V": 0.98
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
    "cost": 0.3249056041240692,
    "electrochemical_conversion": 0.047256436198949814,
    "electrochemical_selectivity": 0.8562340140342712,
    "energy_efficiency": 0.775575578212738,
    "faradaic_efficiency": 0.6927112936973572,
    "ohmic_efficiency": 0.8980686068534851,
    "pH_normalized": 0.17240428924560547,
    "precipitation_signal": 0.0,
    "safety_risk": 0.1135944053530693,
    "score": 0.481151282787323,
    "selective_product_yield": 0.024257536977529526,
    "transport_efficiency": 0.6940609216690063
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
      "potential_V": 1.28
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
    "cost": 0.30912160873413086,
    "electrochemical_conversion": 0.04096817970275879,
    "electrochemical_selectivity": 0.8803294897079468,
    "energy_efficiency": 0.8051086068153381,
    "faradaic_efficiency": 0.592180073261261,
    "ohmic_efficiency": 0.9833022356033325,
    "pH_normalized": 0.27916985750198364,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.12619440257549286,
    "score": 0.47439104318618774,
    "selective_product_yield": 0.026055805385112762,
    "transport_efficiency": 0.5993599891662598
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
    "electrochemical_conversion": 0.3371933698654175,
    "electrochemical_selectivity": 0.8697588443756104,
    "energy_efficiency": 0.855861485004425,
    "faradaic_efficiency": 0.9135919213294983,
    "ohmic_efficiency": 0.9904371500015259,
    "pH_normalized": 0.2265060693025589,
    "precipitation_signal": 0.9940261244773865,
    "safety_risk": 0.072194404900074,
    "score": 0.6723289489746094,
    "selective_product_yield": 0.32472968101501465,
    "transport_efficiency": 0.934816837310791
  }
}
```

## K1 封存报告

## Mechanistic account

I interpret this world as a potential-windowed electrochemical conversion whose rate is governed by productive charge transfer, reactant availability, and material-dependent transport/interface factors. The applied current is a cap rather than a guaranteed current. Productive performance therefore requires three things simultaneously: the correct potential polarity and voltage window, enough electrolysis time, and a current cap that is neither charge-starved nor strongly parasitic.

All batches used 0.020 mol reagent in 0.040 L solvent, so the inferred relationships apply primarily at that loading and concentration.

### 1. Potential controls pathway selection

The clearest causal series was batches 1–5, all using S0/E0, a 100 mA cap, and 1800 s:

- Batch 2, −1.0 V: conversion 0.0100, selectivity 0.576, faradaic efficiency 0.386, transport efficiency 0.412, and energy efficiency 0.252.
- Batch 3, +0.3 V: conversion 0.0268, selectivity 0.745, faradaic efficiency 0.665, transport efficiency 0.682, and energy efficiency 0.687.
- Batch 1, +1.0 V: conversion 0.0523, selectivity 0.897, faradaic efficiency 0.974, transport efficiency 0.945, and energy efficiency 0.870.
- Batch 4, +1.5 V: conversion and selectivity were reported at zero after clipping, with faradaic efficiency 0.028 and transport and energy efficiencies at zero.
- Batch 5, +2.5 V: conversion 0.00345, selectivity 0.00644, faradaic efficiency 0.011, transport efficiency 0.0005, and energy efficiency zero.

Thus the response is neither symmetric in voltage nor monotonic with positive potential. Positive bias is the productive polarity for S0/E0, activation improves between +0.3 and +1.0 V, and a sharply unproductive regime appears between +1.0 and +1.5 V. Ohmic efficiency remained high even in batches 4 and 5, so simple solution resistance cannot explain the collapse. I instead infer the onset of a parasitic electrode or interface process that consumes the available current while producing almost no target. Possible physical interpretations include solvent/electrolyte discharge, a competing redox pathway, surface passivation, or a control-regime transition. The public observations cannot distinguish these possibilities.

A useful phenomenological voltage law is

`k_productive = k_material × A(V_eff) × [1 − P(V_eff)]`,

where `A` is an activation function that rises with positive effective potential, `P` is a steep parasitic-pathway function that turns on at higher potential, and

`V_eff = V_applied − ΔV_material`.

Equivalently, their product can be represented by an asymmetric peaked window rather than a monotonic Butler–Volmer-like response. For S0/E0 the observed optimum lies near +1.0 V, but the experiment spacing only bounds rather than precisely identifies its center and width.

### 2. Time dependence is consistent with pseudo-first-order conversion locally

Batches 1, 6, and 12 held S0/E0, +1.0 V, and 100 mA fixed while changing duration:

- 1800 s, batch 1: conversion 0.0523 and selective-product yield 0.0252.
- 7200 s, batch 6: conversion 0.1792 and selective-product yield 0.1674.
- 14400 s, batch 12: conversion 0.3372 and selective-product yield 0.3247.

Selectivity remained high—0.897, 0.891, and 0.870—and there was no late selectivity collapse. Faradaic and transport efficiencies also remained high. Consequently, the loss of performance above +1 V is not reproduced merely by passing charge for longer at +1 V; excessive voltage and excessive duration are distinct phenomena in the tested range.

The conversions fit a local pseudo-first-order depletion law surprisingly well:

`X(t) = 1 − exp(−k_eff t)`.

The individual effective rate constants calculated from the three batches are 2.98×10⁻⁵, 2.74×10⁻⁵, and 2.86×10⁻⁵ s⁻¹, with a mean of about 2.86×10⁻⁵ s⁻¹. Their agreement is approximately 9% across an eightfold time range. This supports a rate that declines with remaining reactant rather than strictly constant conversion per unit time.

However, constant productive current with gradual polarization is a plausible alternative: conversion only reached 0.337, and the stated assay uncertainty for conversion was 0.01. I therefore regard the exponential law as a compact local predictive model, not proof of an elementary first-order chemical step.

### 3. The current setting is a cap with an intermediate useful regime

Batches 7, 1, and 8 compared 10, 100, and 500 mA at S0/E0, +1.0 V, and 1800 s:

- 10 mA, batch 7: conversion 0.0147, faradaic efficiency 0.941, transport efficiency 0.945, and energy efficiency 0.880.
- 100 mA, batch 1: conversion 0.0523, faradaic efficiency 0.974, transport efficiency 0.945, and energy efficiency 0.870.
- 500 mA, batch 8: conversion 0.0508, faradaic efficiency 0.248, transport efficiency 0.241, and energy efficiency 0.256.

The 10 mA condition retained good efficiencies but was charge-starved. Raising the cap from 10 to 100 mA increased conversion substantially. Raising it further to 500 mA did not measurably increase conversion—the difference between batches 1 and 8 was much smaller than the 0.01 conversion uncertainty—but caused a large efficiency collapse. Selectivity itself remained near 0.88–0.90, suggesting that the small amount of product still formed through the same selective route while most additional electrical demand entered unproductive or transport-limited channels.

I would model this as

`I_productive = min(I_cap, I_kinetic(V_eff), I_transport(material,state)) × η_F(V_eff,I_cap,material)`

and

`dX/dt = K × I_productive × (1 − X)`.

At low cap, `I_cap` limits conversion. Near 100 mA another limit is approached while efficiency remains high. At 500 mA, increasing the configured cap primarily lowers faradaic and transport efficiency rather than increasing productive current. Because actual current and passed charge were not observed, the precise current law and electron stoichiometry are unidentifiable.

### 4. Materials shift the voltage window and independently alter transport/interface behavior

The nominal dossier suggested an additive first approximation to the potential shift. The solvent-plus-electrolyte nominal shifts are approximately +0.10 V for S0/E0, +0.02 V for S1/E1, +0.08 V for S2/E2, and +0.38 V for S3/E3. Batches 9–11 were therefore run at 0.92, 0.98, and 1.28 V respectively, intended to preserve roughly the effective potential represented by +1.0 V for S0/E0.

At 1800 s and 100 mA:

- Batch 9, S1/E1 at 0.92 V: conversion 0.0346, selectivity 0.876, faradaic efficiency 0.774, transport efficiency 0.795, ohmic efficiency 0.981, and energy efficiency 0.874.
- Batch 10, S2/E2 at 0.98 V: conversion 0.0473, selectivity 0.856, faradaic efficiency 0.693, transport efficiency 0.694, ohmic efficiency 0.898, and energy efficiency 0.776.
- Batch 11, S3/E3 at 1.28 V: conversion 0.0410, selectivity 0.880, faradaic efficiency 0.592, transport efficiency 0.599, ohmic efficiency 0.983, and energy efficiency 0.805.

All three retained high selectivity, which is consistent with—though does not prove—the idea that nominal potential shifts translate the productive voltage window. Their faradaic and transport efficiencies differed greatly, showing that voltage translation is insufficient as a complete material model.

Nominal bulk conductivity alone did not rank performance. The paired electrolytes nominally increase in conductivity from E0 toward E3, yet the adjusted paired experiments showed decreasing faradaic/transport efficiency. Other properties—diffusivity, diffusion-layer thickness, solvent diffusivity and conductivity factors, double-layer capacitance, proton activity, solvation, and fixed world-specific residuals—must therefore matter. In particular, the thicker nominal diffusion layers in later electrolyte profiles offer a plausible explanation for some of the transport trend, but this cannot be isolated from simultaneous solvent changes and hidden interface residuals.

A more complete material representation would be

`ΔV_material = ΔV_solvent + ΔV_electrolyte + ΔV_interaction`,

`k_material = f(diffusivity, diffusion-layer thickness, solvation, proton activity, interface kinetics, latent residuals)`,

and

`I_transport ∝ D_eff C / δ_eff`

as a mechanistic prior. The campaign does not identify the coefficients or even establish that the nominal entries are correctly indexed for this world.

### 5. pH and precipitation appear primarily material-controlled

Within S0/E0, normalized pH stayed near 0.225–0.229 across polarity, voltage, duration, and current-cap changes. This suggests that the electrolyte/solvent acid reservoir dominates bulk pH and that the extent of conversion was too small to shift it appreciably.

The paired-material results differed: normalized pH was 0.207 for S1/E1, 0.172 for S2/E2, and 0.279 for S3/E3. These values are compatible with material-dependent acid concentration, pKa, and solvent proton activity, but they are not monotonic in any one nominal property.

Precipitation signal was near 1 throughout S0/E0, about 0.715 for S1/E1, zero for S2/E2, and 0.005 for S3/E3. Because the solvent and electrolyte were always changed together in these comparisons, I cannot assign this to salt concentration, Ksp, solvent solubility, pH, or their interactions individually. Importantly, S0/E0 retained the best electrochemical efficiencies despite its maximal precipitation signal, so the observations do not support treating that signal as evidence of severe electrode fouling in this operating range. It may instead describe a separate bulk equilibrium or suspended phase.

### 6. Relationship among reported performance channels

Faradaic, transport, ohmic, and energy efficiencies are correlated in some regimes but are not related by a single observed algebraic identity. For example, batch 8 had faradaic and transport efficiencies near 0.25 but ohmic efficiency 0.889, while its energy efficiency was 0.256. Batch 11 had faradaic/transport efficiencies near 0.60 and energy efficiency 0.805. Thus energy efficiency is not simply the product of the three reported efficiencies across all materials.

Likewise, selective-product yield should not be forced to equal measured conversion times selectivity. These are independently noisy synthetic assay channels: batch 9, for example, reported yield 0.0496, conversion 0.0346, and selectivity 0.876. Such differences are comparable to low absolute signals and the stated channel uncertainties. Mechanistic fitting should use a latent mass-balanced state with a measurement model rather than require the noisy processed estimates to satisfy exact identities.

### 7. How the explanation changed

Batch 1 established a high-efficiency but low-conversion baseline. Batch 2 established strong polarity asymmetry. Batch 3 initially supported ordinary positive-potential activation, but batches 4 and 5 rejected a monotonic activation model and required a narrow productive window with a high-voltage parasitic regime. Batch 6 showed that time could raise conversion and yield without destroying selectivity. Batches 7 and 8 separated charge starvation from excessive-current inefficiency and established that the current input behaves as a cap. Batches 9–11 showed that nominal potential-shift correction preserves a selective regime only approximately and that material-dependent transport/interface terms remain important. Finally, batch 12 confirmed continued productive accumulation to 14400 s and made the pseudo-first-order time law substantially more credible.

### 8. Scope, unidentifiable factors, and alternatives

The strongest conclusions concern S0/E0 at 0.020 mol in 0.040 L. Concentration, volume, and reagent amount were never varied, so reaction order with respect to reagent and electrolyte, dilution effects, and scale dependence are unknown. There were no exact replicates, and several extreme responses were clipped at zero or one. Only paired solvent/electrolyte changes were tested, so solvent effects, electrolyte effects, and their interaction are inseparable. The material batches also used adjusted voltages, confounding material identity with potential.

No actual current trace, charge, electrode potential under load, temperature trajectory, individual species concentration, or product identity was observed. Electron stoichiometry, elementary rate constants, electrode area, and the identities of parasitic products are consequently unidentifiable. The fixture was constant across the campaign, so its effects are absorbed into fitted constants.

The preferred explanation for high-voltage collapse is a parasitic electrochemical pathway or interface transition. Alternatives include rapid passivation, a transport/control instability, or a benchmark response gate rather than chemical degradation. The preferred time law is pseudo-first-order conversion, but constant-current conversion with gradual polarization could fit the limited range. Material trends may reflect diffusion-layer thickness and solvation, but fixed latent material residuals or non-additive solvent–electrolyte coupling are equally plausible.

Overall, the most defensible predictive structure is a material-shifted, asymmetric voltage window coupled to a capped-current/transport model and approximately first-order reactant depletion. Within its demonstrated scope, the empirically strongest condition was batch 12: S0/E0, +1.0 V, 100 mA cap, and 14400 s, giving conversion 0.337, selectivity 0.870, selective-product yield 0.325, and score 0.672.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific prior or proposed ground-truth mechanism was supplied. The material dossier provided nominal properties and warned that fixed latent residuals and solvent–electrolyte coupling could occur, but it did not prescribe a response law. My initial laws were therefore self-developed.

Supported:
- Polarity dependence was strongly supported. At otherwise matched conditions, batch 1 at +1.0 V gave conversion 0.052, selectivity 0.897, and faradaic efficiency 0.974, whereas batch 2 at −1.0 V gave 0.010, 0.576, and 0.386. This changed polarity asymmetry from a tentative expectation to a supported local conclusion.
- A finite productive voltage window was supported. Batch 3 at +0.3 V was intermediate, but batches 4 and 5 at +1.5 and +2.5 V produced essentially zero useful conversion and extremely low faradaic/transport efficiency. These results supported a peaked or gated voltage response.
- Product accumulation with time was supported locally. Batches 1, 6, and 12 at +1.0 V and 100 mA increased conversion from 0.052 at 1800 s to 0.179 at 7200 s and 0.337 at 14400 s. The corresponding effective first-order constants were similar, so a local pseudo-first-order law became plausible.
- The current setting behaved like a cap. Batch 7 at 10 mA was charge-starved, while batch 8 at 500 mA did not improve conversion over batch 1 at 100 mA and sharply reduced faradaic, transport, and energy efficiencies.
- Material dependence beyond a simple voltage shift was supported: adjusted batches 9–11 retained fairly high selectivity but had substantially different faradaic and transport efficiencies.

Contradicted or narrowed:
- A simple monotonic activation/threshold law was contradicted by batches 4 and 5. Increasing positive voltage beyond +1.0 V made performance dramatically worse rather than merely saturating it.
- The possibility that long electrolysis at +1.0 V would cause an early selectivity collapse was not supported. Batch 12 still had selectivity 0.870 and selective yield 0.325 after 14400 s.
- A simple expectation that greater nominal bulk conductivity would rank overall efficiency was contradicted or at least shown to be insufficient by batches 9–11. Their efficiency ordering did not follow conductivity alone.
- A strict linear conversion-versus-time law was narrowed by the mildly sublinear series in batches 1, 6, and 12; pseudo-first-order depletion described those observations better, although the distinction is not decisive.

Untested or unresolved:
- Additivity of solvent and electrolyte potential shifts was not actually isolated. Batches 9–11 changed solvent, electrolyte, and voltage together.
- Separate solvent, electrolyte, double-layer, diffusion, proton-activity, and latent-residual effects remained unidentifiable.
- The proposed high-voltage parasitic pathway was not distinguished from passivation, irreversible solution degradation, or a controller/transport transition.
- Reaction order outside the single approximately 0.5 mol/L loading, electron stoichiometry, actual delivered current, and electrode-area dependence were untested.
- Whether precipitation causally affects the electrode remained unresolved. S0/E0 showed precipitation near one while retaining excellent performance.

The most important judgment-changing evidence was therefore the collapse in batches 4–5, the current-cap contrast among batches 7, 1, and 8, and the successful long-duration result in batch 12.

2. One additional discriminating experiment

I would use the established S0/E0 loading and 100 mA cap in a staged-potential experiment: electrolyze at +1.0 V long enough to establish productive behavior, switch to +1.5 V for a defined interval, then return to +1.0 V. I would take an intermediate UV–Vis measurement after each stage and finish with the final assay. Existing batches 1 and 6 provide approximate unstressed +1.0 V references.

My leading explanation is a largely reversible, voltage-gated parasitic current regime above the productive window. The main alternative is irreversible passivation or chemical degradation caused by the +1.5 V exposure.

- If efficiency and productive accumulation collapse during +1.5 V but resume at approximately the prior +1.0 V rate after returning to +1.0 V, I would favor the reversible competing-pathway or controller-regime explanation.
- If performance remains suppressed after returning to +1.0 V, I would shift toward irreversible passivation, electrode damage, or destruction of an essential solution component.
- If +1.5 V becomes productive after first operating at +1.0 V, I would infer strong state dependence, such as electrode conditioning or intermediate formation, and reject a static voltage-window model.
- If no collapse occurs in the staged experiment, I would question the reproducibility of batches 4–5 and prioritize replication/noise or hidden-state explanations.

This design is more diagnostic than another isolated endpoint because it tests reversibility within one vessel while controlling material identity and much of the batch-to-batch variation.

3. Unused evidence, reliability, and effect of the goal

The raw characterization artifacts and most spectral shapes were not incorporated into the model; I relied mainly on processed estimates. Intermediate UV–Vis measurements were used as qualitative confirmation but not fitted jointly with final assays. Cost, detailed safety accumulation, temperature changes during solvent addition, sample-volume loss, spectral peak coordinates, and most nominal capacitance, acid, Ksp, and solubility descriptors were also unused quantitatively. pH and precipitation were described but not used to predict productive kinetics. No exact replicate data were available, so process variability could not be separated from stated instrument noise.

The least reliable blind predictions are Q05–Q10 because they use solvent/electrolyte combinations never tested orthogonally. Q11 is also weak because it combines negative potential with a 500 mA cap, whereas the high-current penalty was observed only near +1.0 V. Q01 and Q02 have low predicted yields near the assay-noise scale, so their relative uncertainty is large. Predictions for Q03–Q04 are more defensible because they remain closest to the S0/E0 voltage and duration series, although +0.8 V was still interpolated rather than directly tested.

The batch 12 recommendation is reliable only within the tested S0/E0 recipe and loading. It should not be interpreted as globally optimal across all material combinations, concentrations, costs, or precipitation constraints. It also rests on one observation at 14400 s rather than replication.

The explanatory goal materially affected evidence collection. I spent batches on negative polarity, deliberately poor high voltages, current-cap extremes, duration contrasts, and material comparisons instead of repeatedly optimizing the public score. That produced strong qualitative mechanism contrasts but left insufficient replication and an underpowered material design. In retrospect, changing solvent and electrolyte together in batches 9–11 limited identifiability; an orthogonal design would have been scientifically stronger. There was no conflict with safety limits, but there was a clear tradeoff between broad mechanism discovery and precise local optimization.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.52,
        "upper80": 0.68
      },
      "energy_efficiency": {
        "estimate": 0.32,
        "lower80": 0.22,
        "upper80": 0.42
      },
      "faradaic_efficiency": {
        "estimate": 0.43,
        "lower80": 0.34,
        "upper80": 0.52
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.3127,
        "lower80": 0.25,
        "upper80": 0.38
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.018
      },
      "transport_efficiency": {
        "estimate": 0.45,
        "lower80": 0.35,
        "upper80": 0.55
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.88,
        "lower80": 0.83,
        "upper80": 0.93
      },
      "energy_efficiency": {
        "estimate": 0.87,
        "lower80": 0.77,
        "upper80": 0.96
      },
      "faradaic_efficiency": {
        "estimate": 0.96,
        "lower80": 0.88,
        "upper80": 1.0
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.5533,
        "lower80": 0.49,
        "upper80": 0.62
      },
      "selective_product_yield": {
        "estimate": 0.014,
        "lower80": 0.0,
        "upper80": 0.035
      },
      "transport_efficiency": {
        "estimate": 0.93,
        "lower80": 0.84,
        "upper80": 1.0
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.52,
        "upper80": 0.68
      },
      "energy_efficiency": {
        "estimate": 0.32,
        "lower80": 0.22,
        "upper80": 0.42
      },
      "faradaic_efficiency": {
        "estimate": 0.43,
        "lower80": 0.34,
        "upper80": 0.52
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.3244,
        "lower80": 0.26,
        "upper80": 0.39
      },
      "selective_product_yield": {
        "estimate": 0.028,
        "lower80": 0.012,
        "upper80": 0.047
      },
      "transport_efficiency": {
        "estimate": 0.45,
        "lower80": 0.35,
        "upper80": 0.55
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.88,
        "lower80": 0.83,
        "upper80": 0.93
      },
      "energy_efficiency": {
        "estimate": 0.87,
        "lower80": 0.77,
        "upper80": 0.96
      },
      "faradaic_efficiency": {
        "estimate": 0.96,
        "lower80": 0.88,
        "upper80": 1.0
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.612,
        "lower80": 0.55,
        "upper80": 0.68
      },
      "selective_product_yield": {
        "estimate": 0.156,
        "lower80": 0.125,
        "upper80": 0.19
      },
      "transport_efficiency": {
        "estimate": 0.93,
        "lower80": 0.84,
        "upper80": 1.0
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.61,
        "lower80": 0.48,
        "upper80": 0.73
      },
      "energy_efficiency": {
        "estimate": 0.38,
        "lower80": 0.23,
        "upper80": 0.55
      },
      "faradaic_efficiency": {
        "estimate": 0.38,
        "lower80": 0.23,
        "upper80": 0.54
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.3283,
        "lower80": 0.22,
        "upper80": 0.45
      },
      "selective_product_yield": {
        "estimate": 0.032,
        "lower80": 0.008,
        "upper80": 0.065
      },
      "transport_efficiency": {
        "estimate": 0.41,
        "lower80": 0.25,
        "upper80": 0.58
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.88,
        "lower80": 0.78,
        "upper80": 0.95
      },
      "energy_efficiency": {
        "estimate": 0.87,
        "lower80": 0.73,
        "upper80": 0.97
      },
      "faradaic_efficiency": {
        "estimate": 0.85,
        "lower80": 0.68,
        "upper80": 0.97
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.5892,
        "lower80": 0.48,
        "upper80": 0.69
      },
      "selective_product_yield": {
        "estimate": 0.141,
        "lower80": 0.095,
        "upper80": 0.19
      },
      "transport_efficiency": {
        "estimate": 0.88,
        "lower80": 0.7,
        "upper80": 1.0
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.42,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.26,
        "lower80": 0.12,
        "upper80": 0.44
      },
      "faradaic_efficiency": {
        "estimate": 0.27,
        "lower80": 0.12,
        "upper80": 0.44
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.2761,
        "lower80": 0.17,
        "upper80": 0.39
      },
      "selective_product_yield": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "transport_efficiency": {
        "estimate": 0.29,
        "lower80": 0.13,
        "upper80": 0.48
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.83,
        "lower80": 0.7,
        "upper80": 0.93
      },
      "energy_efficiency": {
        "estimate": 0.75,
        "lower80": 0.58,
        "upper80": 0.89
      },
      "faradaic_efficiency": {
        "estimate": 0.58,
        "lower80": 0.4,
        "upper80": 0.76
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.4874,
        "lower80": 0.37,
        "upper80": 0.6
      },
      "selective_product_yield": {
        "estimate": 0.096,
        "lower80": 0.05,
        "upper80": 0.15
      },
      "transport_efficiency": {
        "estimate": 0.62,
        "lower80": 0.42,
        "upper80": 0.8
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.38,
        "upper80": 0.7
      },
      "energy_efficiency": {
        "estimate": 0.28,
        "lower80": 0.13,
        "upper80": 0.46
      },
      "faradaic_efficiency": {
        "estimate": 0.3,
        "lower80": 0.14,
        "upper80": 0.48
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.2734,
        "lower80": 0.16,
        "upper80": 0.39
      },
      "selective_product_yield": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.045
      },
      "transport_efficiency": {
        "estimate": 0.32,
        "lower80": 0.15,
        "upper80": 0.51
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.78,
        "lower80": 0.64,
        "upper80": 0.9
      },
      "energy_efficiency": {
        "estimate": 0.7,
        "lower80": 0.53,
        "upper80": 0.85
      },
      "faradaic_efficiency": {
        "estimate": 0.64,
        "lower80": 0.45,
        "upper80": 0.8
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.473,
        "lower80": 0.36,
        "upper80": 0.59
      },
      "selective_product_yield": {
        "estimate": 0.083,
        "lower80": 0.04,
        "upper80": 0.14
      },
      "transport_efficiency": {
        "estimate": 0.65,
        "lower80": 0.45,
        "upper80": 0.82
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.45,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.1,
        "lower80": 0.01,
        "upper80": 0.24
      },
      "faradaic_efficiency": {
        "estimate": 0.11,
        "lower80": 0.02,
        "upper80": 0.25
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.214,
        "lower80": 0.13,
        "upper80": 0.32
      },
      "selective_product_yield": {
        "estimate": 0.027,
        "lower80": 0.0,
        "upper80": 0.065
      },
      "transport_efficiency": {
        "estimate": 0.12,
        "lower80": 0.02,
        "upper80": 0.27
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.88,
        "lower80": 0.79,
        "upper80": 0.95
      },
      "energy_efficiency": {
        "estimate": 0.256,
        "lower80": 0.13,
        "upper80": 0.41
      },
      "faradaic_efficiency": {
        "estimate": 0.245,
        "lower80": 0.12,
        "upper80": 0.4
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.3587,
        "lower80": 0.25,
        "upper80": 0.47
      },
      "selective_product_yield": {
        "estimate": 0.156,
        "lower80": 0.11,
        "upper80": 0.21
      },
      "transport_efficiency": {
        "estimate": 0.237,
        "lower80": 0.1,
        "upper80": 0.4
      }
    }
  ],
  "rationale": "Predictions use the observed asymmetric potential window, with +0.8 V near the productive regime and −0.8 V on its inefficient flank. Duration-dependent yield follows the locally supported pseudo-first-order conversion trend. Electrolyte and solvent changes shift the effective voltage and add uncertain transport/interface penalties; these untested cross-combinations receive wider intervals. The 500 mA cases retain roughly saturated conversion/yield but incur the strong faradaic, transport, and energy-efficiency penalty observed in the campaign. Intervals include final-assay noise, interpolation uncertainty, the slightly changed concentration, and substantial uncertainty for material interactions."
}
```
