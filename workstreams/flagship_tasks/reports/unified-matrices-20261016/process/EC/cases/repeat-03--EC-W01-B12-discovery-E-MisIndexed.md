# repeat-03/EC-W01-B12-discovery-E-MisIndexed

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-03\EC-W01-B12-discovery-E-MisIndexed\participant\discovery-E-MisIndexed

## 同期笔记

### v1 · 公开事件 0

# Electrochemical hypothesis notebook

## Prior expectations (before physical experiments)

**H1 [tentative]** Product formation is polarity-selective and has an activation/overpotential threshold shifted by solvent and electrolyte standard-potential terms. At fixed loading, the productive sign should show rising conversion with |potential| and time until selectivity or efficiency declines; the opposite sign should give little target yield. A potential-sign pair will test this.

**H2 [tentative]** Delivered reaction rate is limited by the lesser of the current cap and transport/ohmic delivery. Thus low caps should reduce time-rate approximately proportionally, while sufficiently high caps plateau; E0/S0 should favor ohmic efficiency, whereas the thinner diffusion layer and higher diffusivity of E1 may favor transport.

**H3 [tentative]** E3 is precipitation-prone because its declared salt concentration and low Ksp are extreme, while S2/S3 may mitigate precipitation via higher relative solubility product. pH and precipitation measurements will diagnose this material interaction.

Design: hold loading near 0.02 mol in 0.05 L and span potential sign, magnitude, time, current cap, solvent, and electrolyte. Use matched comparisons and at least one repeat. Numerical differences smaller than the declared instrument noise will not be treated alone as effects.

### v2 · 公开事件 35

# Electrochemical hypothesis notebook

## Prior expectations
At fixed loading (0.02 mol/0.05 L), I expected polarity-selective formation with a threshold, delivered rate limited by current/transport, and E3-prone precipitation.

## H1 [supported in tested S0/E0 scope]
Negative potential is the productive polarity: -1.5 V produced substantial selectivity and nonzero selective yield (event runner-operation-0014), whereas +1.5 V was essentially null (runner-operation-0007). At -2.0 V, selectivity and faradaic/energy efficiency were numerically worse and yield was not detected (runner-operation-0021), suggesting a productive window rather than monotone benefit from magnitude. This comparison is stronger for polarity than for the precise optimum because final-assay noise and single replicates remain.

Testable consequence: another -1.5 V repeat should resemble the productive efficiency regime; later blind predictions should assign near-zero target yield to positive polarity at comparable conditions.

## H2 [partially supported / rate law unresolved]
At -1.5 V, lowering the cap from 200 to 50 mA reduced observed selective yield (runner-operation-0028 versus 0014), and extending 600 to 1800 s raised conversion/yield numerically (0035 versus 0014). Differences in yield are comparable to assay uncertainty, so exact cap/time scaling is unresolved. Efficiencies change less than yield, consistent with accumulated charge controlling extent while material/overpotential controls efficiency.

## H3 [challenged as initially framed]
Precipitation signal was near its upper bound even for E0/S0 (0007, 0014, 0021, 0028, 0035), so E3-specific precipitation cannot be inferred from nominal Ksp alone. Possibilities: the channel orientation reflects precipitation propensity/presence broadly, substrate loading dominates, or the dossier-to-observation link is incomplete. Retain material-interaction tests but suspend any claim that E3 uniquely causes the signal.

### v3 · 公开事件 84

# Electrochemical hypothesis notebook

## H1 — polarity and potential window [supported in S0/E0]
At fixed 0.02 mol/0.05 L, -1.5 V is the productive polarity: two 600 s replicates gave selectivity about 0.56 and selective yield about 0.014–0.016 (runner-operation-0014, runner-operation-0042). +1.5 V gave essentially zero efficiency/yield (0007). Increasing magnitude to -2.0 V reduced faradaic/transport/energy efficiencies and had undetected yield (0021). The evidence supports a polarity-specific productive window centered nearer -1.5 than -2.0 V, not a monotone |V| response. The exact threshold and optimum remain unmapped.

Predictive consequence: positive-potential blind cases at comparable loading should have near-zero target yield; moderately negative cases should retain roughly 0.5–0.57 selectivity, while excessively negative potential should lose efficiency.

## H2 — charge, cap, and time [supported qualitatively; functional form unresolved]
At -1.5 V S0/E0, 50 mA for 600 s gave lower yield than 200 mA (0028 versus 0014/0042). Extending 200 mA electrolysis to 1800 s increased conversion/yield numerically to about 0.033/0.025 (0035). At 500 mA and 3600 s conversion/yield rose further to about 0.042/0.044 but faradaic, transport, and energy efficiencies fell strongly (0084). Thus extent accumulates with time/charge but sublinearly, while high cap/long operation incurs transport or side-reaction losses. Because current_mA is only a cap and delivered current was not directly observed, charge-based equations remain phenomenological rather than Coulombic.

A useful qualitative model is: target yield = productive-polarity gate × saturation in effective delivered charge × material selectivity, with efficiency penalties at excessive overpotential/cap/time. Replicate scatter/noise precludes precise fitted coefficients.

## H3 — material controls [supported for pH/precipitation; target-yield ranking unresolved]
Material changes caused large, repeatable-scale shifts in pH and precipitation channels relative to their stated noise: S0/E0 had pH_norm about 0.23 and precipitation near 1 (0014/0042); S1/E1 shifted to 0.204/0.709 (0049); S2/E2 to 0.166/near 0 (0056); S3/E3 to 0.286/near 0 (0063). Crossed S0/E1 retained high precipitation (0.854; 0070), while S2/E3 stayed near zero (0077), indicating solvent strongly modulates precipitation/solubility and electrolyte strongly influences pH; simple E3-only precipitation was rejected.

Efficiency patterns also depend on materials. S0/E0 and S0/E1 gave faradaic/transport efficiencies around 0.31–0.34 under the common -1.5 V/200 mA/600 s condition (0014, 0042, 0070), versus about 0.19–0.24 and 0.21–0.23 for E2/E3 combinations (0056, 0063, 0077). Ohmic efficiency stayed high across all tested media, so transport/faradaic losses discriminate materials more than gross ohmic loss. Selective yields are noisy and do not establish a firm material ranking.

## Scope and unresolved alternatives
All batches used one loading and volume, so concentration dependence is untested. Potential shifts may mean that a single absolute -1.5 V is not equally overdriven for every solvent/electrolyte. The precipitation channel may report equilibrium state rather than harmful fouling because high precipitation coexisted with competitive efficiencies. Conversion and selective-yield estimates sometimes differ in ways that discourage imposing a simple identity between them. Future tests should map potential relative to each material's shift, obtain time series at several caps, and replicate crossed material pairs.

## Recommendation decision
Batch 5 (S0/E0, -1.5 V, 200 mA cap, 1800 s) is preferred as the best balance: the highest observed campaign score, increased extent over 600 s, and substantially better efficiency than the 500 mA/3600 s extreme. This recommendation would change if replicate assays showed its yield advantage over the 600 s condition is noise, or if a material-specific potential adjustment improves another medium.

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
      "current_mA": 200,
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
    "cost": 0.28571999073028564,
    "electrochemical_conversion": 0.008014115504920483,
    "electrochemical_selectivity": 0.01034972071647644,
    "energy_efficiency": 0.005256945732980967,
    "faradaic_efficiency": 0.02452157624065876,
    "ohmic_efficiency": 0.9624304175376892,
    "pH_normalized": 0.23218974471092224,
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
      "current_mA": 200,
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
    "cost": 0.28571999073028564,
    "electrochemical_conversion": 0.0018169634277001023,
    "electrochemical_selectivity": 0.5630763173103333,
    "energy_efficiency": 0.10909713804721832,
    "faradaic_efficiency": 0.3170040547847748,
    "ohmic_efficiency": 0.9712682366371155,
    "pH_normalized": 0.2294943928718567,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.18432234227657318,
    "selective_product_yield": 0.014433681964874268,
    "transport_efficiency": 0.34326085448265076
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
      "volume_L": 0.05
    },
    {
      "current_mA": 200,
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
    "cost": 0.28595998883247375,
    "electrochemical_conversion": 0.0023208654019981623,
    "electrochemical_selectivity": 0.4809303879737854,
    "energy_efficiency": 0.05924990028142929,
    "faradaic_efficiency": 0.225590318441391,
    "ohmic_efficiency": 0.9651492834091187,
    "pH_normalized": 0.23020939528942108,
    "precipitation_signal": 0.9868234395980835,
    "safety_risk": 0.05933958664536476,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.24214722216129303
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
      "volume_L": 0.05
    },
    {
      "current_mA": 50,
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
    "cost": 0.285180002450943,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.520408034324646,
    "energy_efficiency": 0.08039208501577377,
    "faradaic_efficiency": 0.3408716320991516,
    "ohmic_efficiency": 0.9915223121643066,
    "pH_normalized": 0.2295188158750534,
    "precipitation_signal": 0.987571656703949,
    "safety_risk": 0.05933958664536476,
    "score": 0.0256930124014616,
    "selective_product_yield": 0.0021240736823529005,
    "transport_efficiency": 0.3093841075897217
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
      "volume_L": 0.05
    },
    {
      "current_mA": 200,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.5
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
    "cost": 0.2871600091457367,
    "electrochemical_conversion": 0.033032674342393875,
    "electrochemical_selectivity": 0.5594891309738159,
    "energy_efficiency": 0.09446730464696884,
    "faradaic_efficiency": 0.3281783163547516,
    "ohmic_efficiency": 0.9696341753005981,
    "pH_normalized": 0.2344796061515808,
    "precipitation_signal": 0.9868980646133423,
    "safety_risk": 0.05933958664536476,
    "score": 0.2575637698173523,
    "selective_product_yield": 0.024826738983392715,
    "transport_efficiency": 0.3176688551902771
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
      "current_mA": 200,
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
    "cost": 0.28571999073028564,
    "electrochemical_conversion": 0.012012387625873089,
    "electrochemical_selectivity": 0.5572957396507263,
    "energy_efficiency": 0.11706750094890594,
    "faradaic_efficiency": 0.3412100374698639,
    "ohmic_efficiency": 0.9714909195899963,
    "pH_normalized": 0.23120366036891937,
    "precipitation_signal": 0.9975283145904541,
    "safety_risk": 0.05933958664536476,
    "score": 0.2032376080751419,
    "selective_product_yield": 0.01579095423221588,
    "transport_efficiency": 0.31652671098709106
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
      "solvent": 1,
      "volume_L": 0.05
    },
    {
      "current_mA": 200,
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
    "cost": 0.3057200014591217,
    "electrochemical_conversion": 0.018922334536910057,
    "electrochemical_selectivity": 0.5201752781867981,
    "energy_efficiency": 0.149906724691391,
    "faradaic_efficiency": 0.2777554392814636,
    "ohmic_efficiency": 0.9850097894668579,
    "pH_normalized": 0.20364195108413696,
    "precipitation_signal": 0.7092664241790771,
    "safety_risk": 0.08273958414793015,
    "score": 0.14485618472099304,
    "selective_product_yield": 0.01176821906119585,
    "transport_efficiency": 0.2811557948589325
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
      "solvent": 2,
      "volume_L": 0.05
    },
    {
      "current_mA": 200,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -1.5
    },
    {
      "duration_s": 600,
      "operation": "electrolyze"
    },
    {
      "instrument": "ph_meter",
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
    "cost": 0.3307200074195862,
    "electrochemical_conversion": 0.002173599787056446,
    "electrochemical_selectivity": 0.41431111097335815,
    "energy_efficiency": 0.11932569742202759,
    "faradaic_efficiency": 0.23910987377166748,
    "ohmic_efficiency": 0.9439569115638733,
    "pH_normalized": 0.16625024378299713,
    "precipitation_signal": 0.00031451715040020645,
    "safety_risk": 0.10073958337306976,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.23261453211307526
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
      "solvent": 3,
      "volume_L": 0.05
    },
    {
      "current_mA": 200,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": -1.5
    },
    {
      "duration_s": 600,
      "operation": "electrolyze"
    },
    {
      "instrument": "ph_meter",
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
    "cost": 0.3107199966907501,
    "electrochemical_conversion": 0.004274771548807621,
    "electrochemical_selectivity": 0.48905301094055176,
    "energy_efficiency": 0.14654825627803802,
    "faradaic_efficiency": 0.18998730182647705,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.2855640947818756,
    "precipitation_signal": 0.008188718929886818,
    "safety_risk": 0.11333958804607391,
    "score": 0.22573894262313843,
    "selective_product_yield": 0.020303118973970413,
    "transport_efficiency": 0.2108185738325119
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
      "current_mA": 200,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -1.5
    },
    {
      "duration_s": 600,
      "operation": "electrolyze"
    },
    {
      "instrument": "ph_meter",
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
    "cost": 0.2787199914455414,
    "electrochemical_conversion": 0.024805359542369843,
    "electrochemical_selectivity": 0.5671432018280029,
    "energy_efficiency": 0.16178002953529358,
    "faradaic_efficiency": 0.3124863803386688,
    "ohmic_efficiency": 0.9563614726066589,
    "pH_normalized": 0.19775448739528656,
    "precipitation_signal": 0.8540157079696655,
    "safety_risk": 0.05933958664536476,
    "score": 0.03527029976248741,
    "selective_product_yield": 0.002733813365921378,
    "transport_efficiency": 0.3138359785079956
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
      "volume_L": 0.05
    },
    {
      "current_mA": 200,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": -1.5
    },
    {
      "duration_s": 600,
      "operation": "electrolyze"
    },
    {
      "instrument": "ph_meter",
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
    "cost": 0.3307200074195862,
    "electrochemical_conversion": 0.019958052784204483,
    "electrochemical_selectivity": 0.4371214807033539,
    "energy_efficiency": 0.13043564558029175,
    "faradaic_efficiency": 0.21144485473632812,
    "ohmic_efficiency": 0.9671778082847595,
    "pH_normalized": 0.2894478738307953,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.10073958337306976,
    "score": 0.047899648547172546,
    "selective_product_yield": 0.004495758097618818,
    "transport_efficiency": 0.2186247855424881
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
      "current_mA": 500,
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
    "cost": 0.29580000042915344,
    "electrochemical_conversion": 0.042432673275470734,
    "electrochemical_selectivity": 0.5437451004981995,
    "energy_efficiency": 0.04083112254738808,
    "faradaic_efficiency": 0.09204919636249542,
    "ohmic_efficiency": 0.9449224472045898,
    "pH_normalized": 0.22972576320171356,
    "precipitation_signal": 0.9937044382095337,
    "safety_risk": 0.05933958664536476,
    "score": 0.20311757922172546,
    "selective_product_yield": 0.04406921565532684,
    "transport_efficiency": 0.11327414214611053
  }
}
```

## K1 封存报告

Mechanistic report

1. Experimental scope

I completed 12 batches. Every batch used 0.020 mol of limiting reagent in 0.050 L of a single solvent, so the nominal starting concentration was 0.40 mol L⁻¹. Consequently, this campaign identifies effects of polarity, applied potential, current cap, duration, solvent, and electrolyte only within that loading regime; it does not identify concentration or dilution effects.

Batches 1–6 and 12 used solvent S0/electrolyte E0. Batches 1 and 2 formed a polarity pair at +1.5 and −1.5 V, 200 mA, 600 s. Batch 3 used −2.0 V. Batch 4 used a 50 mA cap. Batch 5 extended the duration to 1800 s. Batch 6 repeated batch 2. Batch 12 used 500 mA for 3600 s. The material survey used S1/E1 in batch 7, S2/E2 in batch 8, S3/E3 in batch 9, and crossed pairs S0/E1 and S2/E3 in batches 10 and 11, all at −1.5 V, 200 mA, 600 s.

2. Productive electrochemical direction and potential window

The clearest causal result is polarity selection. With S0/E0, +1.5 V in batch 1 produced essentially no target response: selective product yield was 0, selectivity 0.010, faradaic efficiency 0.0245, transport efficiency 0, and energy efficiency 0.0053. Reversing only the potential to −1.5 V in batch 2 produced yield 0.0144, selectivity 0.563, faradaic efficiency 0.317, transport efficiency 0.343, and energy efficiency 0.109. The exact repeat in batch 6 gave yield 0.0158, selectivity 0.557, faradaic efficiency 0.341, transport efficiency 0.317, and energy efficiency 0.117. The repeat therefore reproduced the main productive regime, especially selectivity, despite assay noise.

I infer that the target-forming electrode reaction requires negative polarization under the benchmark sign convention. A minimal representation is a polarity gate G(V), close to zero at positive potential and appreciable at sufficiently negative potential.

More negative was not uniformly better. At −2.0 V, batch 3 gave selectivity 0.481, faradaic efficiency 0.226, transport efficiency 0.242, energy efficiency 0.059, and no detected selective yield. These are all worse than the two −1.5 V runs. Thus the likely response is window-shaped rather than monotonic in |V|: insufficient negative overpotential gives slow target formation, moderate negative overpotential favors it, and excessive negative overpotential increases competing electrochemistry, polarization, or transport losses.

One possible phenomenological form is

  η = −[Vapplied − ΔE(solvent,electrolyte)]
  W(η) = activation(η) × penalty_at_large_η,

where activation rises beyond a threshold and the second factor falls once overpotential promotes side reactions. A bell-shaped or difference-of-sigmoids function could represent W. The data locate a favorable S0/E0 region nearer −1.5 than −2.0 V, but they do not locate its precise optimum or threshold.

The nominal dossier makes ΔE material-dependent: both solvents and electrolytes have declared standard-potential shifts. Therefore, −1.5 V is not necessarily the same effective overpotential for every material pair. Material results obtained at one absolute voltage cannot cleanly separate intrinsic material quality from a shifted potential window.

3. Current, duration, effective charge, and efficiency loss

At −1.5 V and 600 s, reducing the current cap from 200 mA to 50 mA in batch 4 lowered selective yield to 0.0021, compared with 0.0144 and 0.0158 in batches 2 and 6. Selectivity remained moderately high at 0.520, and faradaic efficiency was 0.341, so the low yield is more consistent with insufficient delivered charge or rate than with complete loss of the selective pathway.

Increasing duration from 600 to 1800 s at 200 mA in batch 5 increased observed conversion to 0.0330 and yield to 0.0248, while maintaining selectivity 0.559, faradaic efficiency 0.328, transport efficiency 0.318, and ohmic efficiency 0.970. This suggests accumulation of product with time without a major change in pathway over that interval. However, the yield increase over the 600 s replicates is only about 0.009–0.010, comparable to the declared selective-yield assay noise of 0.01. It is mechanistically suggestive rather than a precise kinetic estimate.

The extreme condition in batch 12, 500 mA for 3600 s, gave the largest observed conversion and yield, 0.0424 and 0.0441, but efficiency deteriorated: faradaic efficiency was 0.0920, transport efficiency 0.113, energy efficiency 0.0408, and ohmic efficiency 0.945. Despite far more nominal current-time exposure than batch 5, yield rose only modestly. This strongly supports diminishing returns and increasing loss at high cap and long duration.

A useful qualitative rate model is

  Ieffective = min(Icap, Ikinetic(η), Itransport(material,state))
  Qeffective = ∫ Ieffective(t)·FE(t)·TE(t)·OE(t) dt
  Y = Ymax·G(V)·Smaterial·[1 − exp(−kQeffective)] − Yloss,

where FE, TE, and OE denote faradaic, transport, and ohmic efficiencies. Yloss can increase with excessive overpotential, current density, accumulated charge, or time. This equation is a conceptual decomposition, not a fitted law. Actual current, electrode area, and time-resolved efficiencies were not measured, and the specified current was a cap rather than necessarily the delivered current.

The batch-12 result implies that simply maximizing Icap·time is inefficient. A moderate cap and duration allow the productive pathway to operate before transport limitations or side reactions dominate. This is why batch 5 was the sealed recommendation: it had the highest observed campaign score (0.258) and more extent than the 600 s experiments while retaining substantially better efficiencies than batch 12.

4. Transport and ohmic behavior

Ohmic efficiency was high in every final assay, approximately 0.944–1.000, and was 0.970–0.971 in the productive S0/E0 repeats. It changed much less than faradaic and transport efficiencies. I therefore do not think bulk resistance was the principal limitation in the moderate operating regime. It became somewhat worse at the 500 mA extreme, consistent with an increasing ohmic drop, but faradaic and transport efficiencies collapsed much more strongly.

The important bottlenecks appear to be interfacial selectivity and mass transport. At the common −1.5 V, 200 mA, 600 s condition, S0/E0 gave transport efficiencies of 0.343 and 0.317; S1/E1 gave 0.281; S2/E2 gave 0.233; and the E3-containing batches gave about 0.211–0.219. Faradaic efficiency followed a broadly similar ordering. These changes are compatible with coupling among diffusivity, diffusion-layer thickness, solvent diffusivity, double-layer properties, and hidden fixed world residuals.

The comparison of E1 in two solvents is informative. Batch 7, S1/E1, gave faradaic/transport efficiencies of 0.278/0.281, whereas batch 10, S0/E1, gave 0.312/0.314. This suggests that S0 improves charge utilization or transport relative to S1 under these conditions, consistent with S0's higher nominal relative conductivity, although the experiments were not replicated. Energy efficiency was 0.150 in batch 7 and 0.162 in batch 10.

5. Acid-base state and precipitation coupling

The pH-normalized observation depended strongly on electrolyte identity. E0/S0 was stable near 0.229–0.234 across batches 1–6 and 12. E1 gave 0.204 with S1 in batch 7 and 0.198 with S0 in batch 10. E2/S2 gave the lowest value, 0.166, in batch 8. E3 gave 0.286 with S3 in batch 9 and 0.289 with S2 in batch 11. Because changing solvent within E1 or E3 caused only a small pH shift, electrolyte acid concentration and pKa appear to dominate pH, with solvent proton activity providing a secondary correction. This ordering is qualitatively consistent with the nominal acid properties, especially the high acid concentration and low pKa of E2.

My initial conjecture that E3 alone would cause the most precipitation was rejected. The precipitation signal was near saturation for S0/E0: 1.000 in batches 1 and 2 and 0.987–0.998 in batches 3–6 and 12. It was 0.709 for S1/E1 and 0.854 for S0/E1. In contrast, it was essentially zero for S2/E2 (0.00031), S3/E3 (0.0082), and S2/E3 (0.0052).

The crossed comparisons indicate strong solvent control. E3 has the most unfavorable nominal salt concentration/Ksp combination, yet pairing it with either S2 or S3 kept the signal near zero. Both solvents have substantially increased nominal relative solubility products. Conversely, S0, whose relative solubility-product factor is only 1, retained a high signal with both E0 and E1. A plausible equilibrium description is

  Pprecip ≈ sigmoid[a·(log10 ionic activity product − log10 Ksp,effective)],
  Ksp,effective = Ksp,electrolyte × fsolvent × fcoupling,

with saturation of the observable near zero or one. The data support solvent-dependent solubility coupling, but they cannot identify the coefficients or confirm that the signal measures solid amount rather than propensity/equilibrium state.

High precipitation signal did not automatically imply poor electrochemical performance. S0/E0 combined a near-maximal precipitation signal with the best moderate-condition faradaic and transport efficiencies. Thus precipitation may be an equilibrium spectator, may occur away from the active interface, or may be represented by a channel whose magnitude is not proportional to electrode fouling. Treating it as a direct deactivation term would contradict this campaign.

6. Material effects on selectivity and yield

At the common material-screen condition, selectivity was 0.557–0.563 for S0/E0, 0.520 for S1/E1, 0.414 for S2/E2, 0.489 for S3/E3, 0.567 for S0/E1, and 0.437 for S2/E3. This suggests that E0 or E1 with S0 supports the most selective observed regime, whereas the tested S2 combinations were less selective. Nevertheless, a single absolute potential may place the materials at different effective overpotentials, so this is an operating-condition ranking, not necessarily an intrinsic ranking.

Selective yields were noisier and did not define a secure material ordering: batch 7 yielded 0.0118, batch 8 had no detected yield, batch 9 yielded 0.0203, batch 10 yielded 0.0027, and batch 11 yielded 0.0045. Batch 9's relatively high yield despite low faradaic/transport efficiencies may reflect assay variation, a different material-specific kinetic factor, or a mismatch between instantaneous efficiency observables and accumulated product. Replication would be required before claiming that S3/E3 genuinely outperforms the other material pairs in product amount.

7. Measurement relationships and apparent inconsistencies

I would not impose the identity selective yield = conversion × selectivity on the reported channels. For example, batch 2 reported conversion 0.0018, selectivity 0.563, and yield 0.0144; batch 6 reported conversion 0.0120, selectivity 0.557, and yield 0.0158. The conversion assay has declared noise of 0.01, making values near zero particularly unstable. The channels may also be independently calibrated normalized descriptors rather than exact stoichiometric fractions on one basis.

The batch-2/batch-6 repeat is useful for interpreting uncertainty. Selectivity agreed within 0.006 and yield within 0.0014, while conversion differed by about 0.0102 and transport efficiency by about 0.027. I therefore place greater confidence in the existence of the selective negative-potential regime than in any individual low conversion estimate or fine ranking of efficiencies.

8. Integrated account

My best account is a coupled sequence:

(a) Electrolyte and solvent establish acid-base state, effective redox-potential shift, conductivity, interfacial capacitance, solubility, and transport properties.

(b) Negative applied potential activates the target-forming electron-transfer pathway. Positive potential does not. Target selectivity peaks in a finite effective-overpotential window.

(c) Delivered current is jointly limited by the imposed cap, charge-transfer kinetics, ohmic drop, and diffusion. Under moderate S0/E0 conditions, ohmic loss is small and mass transport/interfacial faradaic competition dominate.

(d) Product accumulates with effective charge but approaches diminishing returns. High current or prolonged operation increasingly diverts charge to side reactions or produces transport polarization, reducing faradaic, transport, and energy efficiencies.

(e) Acid-base and precipitation equilibria are coupled to the material pair. Electrolyte primarily controls the observed pH ordering; solvent solubility strongly controls the precipitation channel. Precipitation is not demonstrably the main cause of electrochemical loss in the tested regime.

9. Limits, unidentifiable factors, and alternatives

The campaign cannot identify reaction order, exchange current, transfer coefficient, diffusion coefficient in the actual mixture, electron stoichiometry, true delivered current, electrode area, electrode gap, contact resistance, or product/side-product identities. Fixture properties and hidden world-specific residuals were fixed but unobserved. No concentration series, mixed-solvent series, temperature series, open-circuit measurement, current transient, or time-resolved composition was obtained.

Potential, current, and duration were only sparsely sampled. Current and duration were not varied in a complete factorial design, so the high-current penalty cannot be cleanly separated from the long-duration penalty in batch 12. Only the batch-2 condition was exactly replicated. Most material pairs were measured once, and potential shifts confound material comparisons.

Plausible alternatives remain. The −2.0 V decline could arise from a competing electrode reaction, reagent degradation, product destruction, gas evolution, or simply a material-specific potential window. The high-current efficiency loss could reflect diffusion limitation, interfacial blocking, uncompensated resistance, or time-dependent depletion. The precipitation signal could represent thermodynamic propensity rather than actual deposited solid. Differences attributed to solvent transport could instead come from hidden solvent–electrolyte interface residuals.

Accordingly, the report supports a robust qualitative architecture—negative-polarity activation, a finite potential window, charge-dependent accumulation with diminishing efficiency, and strong material coupling—but not a unique microscopic mechanism or precisely parameterized predictive equation.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific prior mechanism, response law, or correct answer was supplied. The supplied information consisted of nominal material properties, instrument/scoring contracts, and the warning that fixed hidden material residuals could exist.

Supported:
- A strong polarity gate was supported by the matched S0/E0 comparison. Batch 1 at +1.5 V had zero selective yield and nearly zero selectivity and faradaic efficiency, whereas batch 2 at −1.5 V gave yield 0.0144, selectivity 0.563, and faradaic efficiency 0.317. Batch 6 repeated the negative condition and reproduced yield 0.0158 and selectivity 0.557. This was the clearest evidence changing the explanation toward a polarity-specific target pathway.
- A finite productive potential window was supported, although not precisely located. Batch 3 at −2.0 V was worse than batches 2 and 6 at −1.5 V: selectivity fell to 0.481, faradaic efficiency to 0.226, and yield was undetected. This contradicted a simple law in which greater negative magnitude always improves performance.
- Product accumulation with diminishing returns was qualitatively supported. The 50 mA condition in batch 4 gave only 0.0021 yield; extending the 200 mA run to 1800 s in batch 5 increased yield to 0.0248. However, batch 12 at 500 mA for 3600 s reached only 0.0441 yield while faradaic, transport, and energy efficiencies fell to 0.092, 0.113, and 0.041. This shifted the account away from a linear current-time law toward effective-charge accumulation with high-current or late-stage losses.
- Electrolyte-dominated acid-base behavior was supported. E1 produced similar pH-normalized values in two solvents—0.204 in batch 7 and 0.198 in batch 10—while E3 similarly gave 0.286 in batch 9 and 0.289 in batch 11. E2 gave the lowest value, 0.166 in batch 8, broadly consistent with its nominal acid properties.
- Strong solvent control of precipitation/solubility was supported. S0 gave precipitation signals near 1 with E0 and 0.854 with E1, while S2 or S3 gave near-zero signals in batches 8, 9, and 11. The crossed pairs were important evidence that solvent could override the electrolyte-only expectation.
- Ohmic loss appeared secondary in the tested range. Ohmic efficiency remained about 0.944–1.000, while faradaic and transport efficiencies varied much more.

Contradicted or revised:
- My initial expectation that E3 would be uniquely precipitation-prone was contradicted. E3 gave signals of only 0.0082 with S3 in batch 9 and 0.0052 with S2 in batch 11, whereas S0/E0 remained near saturation. The revised explanation assigns major control to solvent-dependent effective solubility rather than electrolyte identity alone.
- A monotonic benefit from voltage magnitude was contradicted by batch 3.
- A simple proportional relationship between nominal current-time exposure and yield was contradicted by the poor efficiency and modest incremental yield in batch 12.
- A direct identity among measured conversion, selectivity, and selective yield was not supported. For example, batch 2 reported conversion 0.0018, selectivity 0.563, and yield 0.0144. Independent assay noise or differing calibration bases must be allowed.

Untested or unresolved:
- Concentration dependence, reaction order, the exact activation threshold, and the location of the optimum potential were untested.
- The proposed effective-charge and window equations were conceptual rather than fitted laws.
- Actual delivered current, electron stoichiometry, electrode area, kinetic constants, product degradation, and time-resolved depletion were unmeasured.
- Material-specific potential shifts were not mapped; therefore the material ranking at one absolute potential remains confounded.
- Whether precipitation represents actual fouling, bulk solid, or merely equilibrium propensity remains unresolved.

2. One additional discriminating experiment

I would run S0/E0 at −1.5 V and the original 0.020 mol/0.050 L loading, using 250 mA for 7200 s, followed by the same final assay. This has the same nominal charge exposure as batch 12—250×7200 equals 500×3600 mA·s—but delivers it at half the current over twice the time.

My leading explanation attributes much of batch 12's loss to high-current transport polarization or current-dependent side reactions. It predicts that the proposed run should recover appreciably higher faradaic, transport, and energy efficiencies than batch 12 and should give at least comparable, possibly greater, selective yield.

An alternative is that performance depends mainly on cumulative charge or accumulated conversion, regardless of current profile. Under that account, the proposed run should resemble batch 12 in yield and efficiency. A third alternative is time-dependent fouling, product destruction, or reagent instability. That would be favored if the longer, lower-current run failed to recover efficiency and produced less yield than batch 12. A mixed result—for example, recovered transport efficiency but lower yield—would suggest that high-current polarization and slow time-dependent loss both operate. One experiment could not uniquely separate every alternative, but this charge-matched comparison would directly challenge the most important current-versus-time ambiguity.

3. Unused evidence, weak predictions, and effect of the goal

The analysis relied mainly on processed final-assay values. Raw spectra, peak assignments, calibration traces, and replicate-level signal structure were not inspected or modeled. Intermediate UV–visible and pH measurements were used only selectively; their full raw signals and discrepancies from final assays were not incorporated. Cost and safety observations were also not modeled quantitatively. Safety remained well below the 0.65 limit, although solvent-dependent risk differences were visible. Several nominal properties—double-layer capacitance, supporting-electrolyte concentration, and individual diffusivity terms—could not be isolated from one another and therefore remained unused as quantitative predictors.

The blind predictions are least reliable for the 7200 s conditions because the campaign reached only 3600 s, and for ±0.8 V because the campaign directly tested only ±1.5 V and −2.0 V. Q11 and Q12 are especially uncertain because they combine the untested 7200 s duration with a 500 mA cap. Q07–Q10 also require untested material pairings or extrapolation of material-specific potential shifts. The positive-potential predictions are more reliable qualitatively—target formation should be very small—but their exact nonzero estimates and score intervals depend strongly on clipped assay noise. All predictions also use a concentration of 0.48 mol L⁻¹ rather than the campaign's 0.40 mol L⁻¹.

The sealed recommendation of batch 5 is reasonably supported as a balance of observed score and efficiency, but its yield advantage over the 600 s repeats was only about the size of the stated yield noise and was not replicated. It is therefore less secure than the polarity conclusion.

The assigned goal explicitly prioritized explanation over public-score optimization. That led me to collect a polarity pair, a potential comparison, current and duration perturbations, an exact repeat, a broad material screen, and two crossed material pairs. This improved mechanistic coverage but left fewer batches for replication, dense potential mapping, and local optimization around batch 5. I found no clear conflict between the explanatory goal and safety, but there was a tradeoff between breadth and precision: the campaign identified several qualitative couplings while leaving many response coefficients poorly determined.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.38,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.18,
        "lower80": 0.05,
        "upper80": 0.34
      },
      "faradaic_efficiency": {
        "estimate": 0.3,
        "lower80": 0.14,
        "upper80": 0.48
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.13,
        "lower80": 0.0,
        "upper80": 0.3
      },
      "selective_product_yield": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.032
      },
      "transport_efficiency": {
        "estimate": 0.3,
        "lower80": 0.15,
        "upper80": 0.44
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "energy_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "faradaic_efficiency": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.065
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.014
      },
      "transport_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.055
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.38,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.19,
        "lower80": 0.06,
        "upper80": 0.35
      },
      "faradaic_efficiency": {
        "estimate": 0.3,
        "lower80": 0.14,
        "upper80": 0.47
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.3,
        "lower80": 0.18,
        "upper80": 0.42
      },
      "selective_product_yield": {
        "estimate": 0.105,
        "lower80": 0.035,
        "upper80": 0.2
      },
      "transport_efficiency": {
        "estimate": 0.28,
        "lower80": 0.12,
        "upper80": 0.43
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "energy_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.045
      },
      "faradaic_efficiency": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.06
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.56,
        "lower80": 0.35,
        "upper80": 0.71
      },
      "energy_efficiency": {
        "estimate": 0.2,
        "lower80": 0.07,
        "upper80": 0.36
      },
      "faradaic_efficiency": {
        "estimate": 0.26,
        "lower80": 0.11,
        "upper80": 0.43
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.29,
        "lower80": 0.16,
        "upper80": 0.42
      },
      "selective_product_yield": {
        "estimate": 0.09,
        "lower80": 0.025,
        "upper80": 0.185
      },
      "transport_efficiency": {
        "estimate": 0.27,
        "lower80": 0.11,
        "upper80": 0.42
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "energy_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "faradaic_efficiency": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.075
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.065
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.46,
        "lower80": 0.24,
        "upper80": 0.65
      },
      "energy_efficiency": {
        "estimate": 0.13,
        "lower80": 0.03,
        "upper80": 0.29
      },
      "faradaic_efficiency": {
        "estimate": 0.17,
        "lower80": 0.05,
        "upper80": 0.34
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.23,
        "lower80": 0.08,
        "upper80": 0.36
      },
      "selective_product_yield": {
        "estimate": 0.05,
        "lower80": 0.005,
        "upper80": 0.135
      },
      "transport_efficiency": {
        "estimate": 0.21,
        "lower80": 0.07,
        "upper80": 0.37
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.065
      },
      "energy_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "faradaic_efficiency": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.075
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.065
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.46,
        "lower80": 0.25,
        "upper80": 0.65
      },
      "energy_efficiency": {
        "estimate": 0.16,
        "lower80": 0.04,
        "upper80": 0.32
      },
      "faradaic_efficiency": {
        "estimate": 0.245,
        "lower80": 0.09,
        "upper80": 0.41
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.25,
        "lower80": 0.1,
        "upper80": 0.38
      },
      "selective_product_yield": {
        "estimate": 0.07,
        "lower80": 0.012,
        "upper80": 0.16
      },
      "transport_efficiency": {
        "estimate": 0.2,
        "lower80": 0.06,
        "upper80": 0.36
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.065
      },
      "energy_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "faradaic_efficiency": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.075
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.065
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.5,
        "lower80": 0.28,
        "upper80": 0.68
      },
      "energy_efficiency": {
        "estimate": 0.04,
        "lower80": 0.0,
        "upper80": 0.15
      },
      "faradaic_efficiency": {
        "estimate": 0.07,
        "lower80": 0.015,
        "upper80": 0.19
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.22,
        "lower80": 0.09,
        "upper80": 0.34
      },
      "selective_product_yield": {
        "estimate": 0.11,
        "lower80": 0.035,
        "upper80": 0.28
      },
      "transport_efficiency": {
        "estimate": 0.08,
        "lower80": 0.01,
        "upper80": 0.2
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "energy_efficiency": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.045
      },
      "faradaic_efficiency": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.016
      },
      "transport_efficiency": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.055
      }
    }
  ],
  "rationale": "The campaign showed a strong polarity gate: negative potential produced the target, whereas positive potential was essentially inactive. Because ±0.8 V lies outside the tested potential range and may be near the activation threshold, intervals are deliberately broad. Negative-potential yield was projected from effective charge with diminishing returns, material-dependent selectivity and efficiency, and severe transport/faradaic penalties at high current. E1 was treated as broadly similar to E0 but slightly less efficient, E3 and S2 as less favorable and more uncertain. Positive-potential estimates mainly represent clipped assay noise. Score estimates also account for the selective-yield gate and uncertainty in unrequested conversion and ohmic-efficiency components."
}
```
