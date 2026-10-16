# repeat-01/EC-W02-B12-discovery-E-Aligned

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-01\EC-W02-B12-discovery-E-Aligned\participant\discovery-E-Aligned

## 同期笔记

### v1 · 公开事件 0

# Pre-experiment hypotheses

**H1 [tentative].** Product formation is polarity- and overpotential-dependent: one potential sign should be strongly more productive, with conversion increasing with magnitude and time before selectivity/efficiency losses at excessive drive. A sign-reversed matched pair will identify productive polarity.

**H2 [tentative].** Current-cap effects separate charge/kinetic limitation from voltage control. If the cap binds, raising it should accelerate early conversion; if it does not, matched outcomes should be similar. Early UV–vis followed by final assay will provide within-batch time information.

**H3 [tentative].** Solvent and electrolyte affect distinct terms: conductivity/contact should chiefly influence ohmic efficiency, diffusivity/layer thickness transport efficiency, and acid/precipitating properties pH and precipitation. Nominal shifts should translate the potential-response curve, but hidden fixed residuals may reverse rankings.

**Design commitment.** Use a constant reagent loading and volume, first establish polarity and useful drive, then compare solvent and electrolyte one-factor changes plus current and duration/drive contrasts. Numerical differences will remain provisional unless larger than declared noise or repeated/structured contrasts support them.

### v2 · 公开事件 40

# Working hypotheses after polarity/drive tests

**H1 [supported in tested S0/E0 scope].** Negative potential is the productive polarity. At +1.2 V, 600 s gave essentially zero yield/efficiencies (final event runner-operation-0008), whereas −1.2 V produced nonzero selectivity, Faradaic/transport efficiency, and yield (runner-operation-0016). This is a polarity effect, not yet a full signed response curve.

**H2 [supported for time; current-cap effect unresolved/non-monotone].** At −2.0 V and 500 mA cap, extending 600 to 3600 s increased conversion from ~0.016 to ~0.113 and yield from ~0.010 to ~0.061 (runner-operation-0032 vs runner-operation-0040), approximately consistent with charge accumulation in the low-conversion regime. At −1.2 V, increasing the cap 100→500 mA did not improve yield or efficiencies (runner-operation-0016 vs runner-operation-0024); possible explanations are that the cap does not bind at 100 mA, higher cap worsens transport/interface efficiency, or final yield noise is important at ~0.01. A direct mechanistic law for cap remains unresolved.

**H3 [supported partly].** S0/E0 has high ohmic efficiency (~0.93–0.98) but modest transport efficiency (~0.23–0.41), consistent with conductivity being good while diffusion-layer transport limits. E0 conditions also show saturated precipitation signal near 1 and pH_normalized near 0.23 (final events through runner-operation-0040).

**H4 [tentative].** For the productive polarity, potential magnitude trades energy efficiency/selectivity against reaction rate: −1.2 V shows higher energy efficiency and selectivity than −2.0 V, while longer time at −2.0 increases conversion. Material one-factor tests should reveal whether nominal conductivity/diffusion/shift factors predict these components.

**Decision.** Continue with one-factor solvent and electrolyte substitutions at −2.0 V, 500 mA, 1200 s (early read at 240 s), then reserve the last batch for a higher-information extreme or replication. Results contradicting nominal-property ordering will narrow H3/H4 rather than be dismissed as noise.

### v3 · 公开事件 88

# Working hypotheses before final batch

**H1 [supported].** Negative potential is productive in S0/E0; +1.2 V is effectively inactive under the tested loading/time (runner-operation-0008 vs runner-operation-0016).

**H2 [supported for low-conversion time scaling; cap law unresolved].** Conversion/yield rise with duration at −2.0 V (runner-operation-0032 vs runner-operation-0040). The −1.2 V cap comparison does not show a beneficial 500 mA effect (runner-operation-0016 vs runner-operation-0024), so current_mA must be treated as a cap with possible efficiency penalties rather than delivered charge.

**H3 [material response supported, simple nominal ranking rejected].** At matched −2.0 V, 500 mA, 1200 s, solvent S1 outperformed S2 and S3 in selective yield (runner-operation-0048, -0056, -0064); S3's nominal conductivity did not rescue its lower Faradaic/transport performance. For electrolytes, E1 gave the strongest balanced result and yield (~0.039; runner-operation-0072), E2 increased conversion but had low yield and eliminated precipitation (~0 at runner-operation-0080), and E3 suppressed precipitation but also Faradaic/transport efficiency (runner-operation-0088). Thus precipitation tracks nominal salt/Ksp and pH tracks acidity, but low precipitation alone does not imply productive selectivity.

**H4 [supported locally].** E1 is a useful compromise: relative to E0/S0 material comparisons it improves transport/energy and lowers precipitation without the efficiency losses seen for E2/E3. Potential magnitude still appears to trade energy efficiency/selectivity against rate.

**Prospective final test.** Run S0/E1 at −1.2 V, 100 mA cap for 3600 s with an intermediate 600 s UV–vis. Prediction made before the experiment: yield should exceed the 600 s S0/E0/−1.2/100 result and E1 should retain better precipitation/transport behavior, while conversion may remain modest because the low cap binds. Failure to exceed the earlier yield would argue for strong E1×potential interaction or time-dependent deactivation.

### v4 · 公开事件 96

# Final source-stage synthesis

**H1 [supported in explored domain].** Productive chemistry is cathodic: +1.2 V is inactive, whereas −1.2 to −2.0 V gives appreciable Faradaic/transport efficiencies and target yield (runner-operation-0008, -0016, -0032). The sign effect is much larger than assay noise.

**H2 [supported with limits].** At −2.0 V/S0/E0, conversion and yield increase strongly from 600 to 3600 s (runner-operation-0032 vs -0040), consistent with approximately cumulative charge at low conversion. Duration did not proportionally increase conversion at −1.2 V/100 mA: the final E1 test after 3600 s remained low-conversion (~0.020) but yielded ~0.032 (runner-operation-0096). This indicates current-cap/kinetic limitation and/or a noisy conversion channel; extrapolation to high conversion should not be linear.

**H3 [supported].** Increasing cathodic magnitude from −1.2 toward −2.0 sacrifices energy efficiency and selectivity while increasing rate under sufficiently long electrolysis. A practical response model therefore needs separate terms for extent (time/current/potential) and quality (potential-dependent Faradaic/selectivity/energy factors), not conversion alone.

**H4 [supported for one-factor material tests].** Material changes alter largely separable observables. E1 is the best tested balanced electrolyte: at matched −2.0 V/500 mA/1200 s it improved yield, transport and energy while lowering precipitation relative to E0 (runner-operation-0072 versus the S0/E0 time-series neighborhood). E2 eliminated precipitation but did not maximize target yield (runner-operation-0080); E3 also suppressed precipitation while losing Faradaic/transport performance (runner-operation-0088). Solvent S1 was best of S1–S3 at the matched condition (runner-operation-0048, -0056, -0064). Nominal conductivity/diffusivity alone is therefore insufficient; fixed residual/interface terms are consequential.

**H5 [final prospective test supported, scope narrow].** S0/E1 at −1.2 V, 100 mA, 3600 s exceeded the earlier S0/E0/−1.2 V/100 mA/600 s yield and combined the campaign's highest score with high selectivity, Faradaic, transport, ohmic, and energy efficiencies (runner-operation-0096 versus -0016). The test simultaneously changed electrolyte and duration, so it supports the operating combination but does not isolate the cause of improvement.

**Predictive account retained.** Use a signed-potential gate (anodic near-zero, cathodic active); represent extent as a saturating function of time and delivered-current limitation, with current_mA only an upper bound; multiply extent by material- and overpotential-dependent Faradaic/selectivity/transport factors. More-negative potential accelerates extent but penalizes energy/selectivity. E1 shifts the best balance toward mild cathodic drive; S1 is the strongest tested nonbaseline solvent at −2.0 V. pH and precipitation follow electrolyte acid/salt properties but precipitation suppression is not itself a proxy for product yield.

**Unresolved alternatives.** Absolute conversion near zero is assay-noise-sensitive in short runs; no exact delivered-current trace was observed; S1×E1 interaction was not tested; only one repeat-equivalent baseline neighborhood exists. These limit quantitative interpolation and any claim of a unique mechanistic equation.

## 实际批次及公开测量

### 批次 1 · 终点事件 8

```json
{
  "ordinal": 1,
  "lifecycle_index": 1,
  "end_step": 8,
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
      "potential_V": 1.2
    },
    {
      "duration_s": 120,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "duration_s": 480,
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
    "cost": 0.3008747398853302,
    "electrochemical_conversion": 0.009264115244150162,
    "electrochemical_selectivity": 0.01034972071647644,
    "energy_efficiency": 0.005256945732980967,
    "faradaic_efficiency": 0.02452157624065876,
    "ohmic_efficiency": 0.9705405235290527,
    "pH_normalized": 0.2289474457502365,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.0
  }
}
```

### 批次 2 · 终点事件 16

```json
{
  "ordinal": 2,
  "lifecycle_index": 2,
  "end_step": 16,
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
      "potential_V": -1.2
    },
    {
      "duration_s": 120,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "duration_s": 480,
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
    "cost": 0.3008880019187927,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.5764105916023254,
    "energy_efficiency": 0.17037318646907806,
    "faradaic_efficiency": 0.38618457317352295,
    "ohmic_efficiency": 0.9783982634544373,
    "pH_normalized": 0.22625209391117096,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.1743171513080597,
    "selective_product_yield": 0.01238091941922903,
    "transport_efficiency": 0.4124414026737213
  }
}
```

### 批次 3 · 终点事件 24

```json
{
  "ordinal": 3,
  "lifecycle_index": 3,
  "end_step": 24,
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
      "potential_V": -1.2
    },
    {
      "duration_s": 120,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "duration_s": 480,
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
    "cost": 0.3020400106906891,
    "electrochemical_conversion": 0.014664499089121819,
    "electrochemical_selectivity": 0.567408561706543,
    "energy_efficiency": 0.11167619377374649,
    "faradaic_efficiency": 0.21641658246517181,
    "ohmic_efficiency": 0.8799730539321899,
    "pH_normalized": 0.22696709632873535,
    "precipitation_signal": 0.9871507287025452,
    "safety_risk": 0.072194404900074,
    "score": 0.001995611470192671,
    "selective_product_yield": 0.00017894005577545613,
    "transport_efficiency": 0.23297350108623505
  }
}
```

### 批次 4 · 终点事件 32

```json
{
  "ordinal": 4,
  "lifecycle_index": 4,
  "end_step": 32,
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
      "potential_V": -2
    },
    {
      "duration_s": 120,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "duration_s": 480,
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
    "cost": 0.30300000309944153,
    "electrochemical_conversion": 0.016434352844953537,
    "electrochemical_selectivity": 0.4561455249786377,
    "energy_efficiency": 0.019822297617793083,
    "faradaic_efficiency": 0.2723284661769867,
    "ohmic_efficiency": 0.934730589389801,
    "pH_normalized": 0.22627650201320648,
    "precipitation_signal": 0.9878990054130554,
    "safety_risk": 0.072194404900074,
    "score": 0.10364178568124771,
    "selective_product_yield": 0.009985895827412605,
    "transport_efficiency": 0.24084092676639557
  }
}
```

### 批次 5 · 终点事件 40

```json
{
  "ordinal": 5,
  "lifecycle_index": 5,
  "end_step": 40,
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
      "duration_s": 3000,
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
    "cost": 0.3149999976158142,
    "electrochemical_conversion": 0.11324251443147659,
    "electrochemical_selectivity": 0.4939168095588684,
    "energy_efficiency": 0.02747369185090065,
    "faradaic_efficiency": 0.2438051551580429,
    "ohmic_efficiency": 0.934164822101593,
    "pH_normalized": 0.2312372922897339,
    "precipitation_signal": 0.9872254133224487,
    "safety_risk": 0.072194404900074,
    "score": 0.23526568710803986,
    "selective_product_yield": 0.06137827783823013,
    "transport_efficiency": 0.23329567909240723
  }
}
```

### 批次 6 · 终点事件 48

```json
{
  "ordinal": 6,
  "lifecycle_index": 6,
  "end_step": 48,
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
      "current_mA": 500,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -2
    },
    {
      "duration_s": 240,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "duration_s": 960,
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
    "cost": 0.321399986743927,
    "electrochemical_conversion": 0.04229365661740303,
    "electrochemical_selectivity": 0.471242755651474,
    "energy_efficiency": 0.05479026585817337,
    "faradaic_efficiency": 0.27428287267684937,
    "ohmic_efficiency": 0.9197180271148682,
    "pH_normalized": 0.23299455642700195,
    "precipitation_signal": 0.9933977127075195,
    "safety_risk": 0.09559440612792969,
    "score": 0.22313565015792847,
    "selective_product_yield": 0.028499973937869072,
    "transport_efficiency": 0.24959953129291534
  }
}
```

### 批次 7 · 终点事件 56

```json
{
  "ordinal": 7,
  "lifecycle_index": 7,
  "end_step": 56,
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
      "current_mA": 500,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -2
    },
    {
      "duration_s": 240,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "duration_s": 960,
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
    "cost": 0.34700000286102295,
    "electrochemical_conversion": 0.03390434756875038,
    "electrochemical_selectivity": 0.47912681102752686,
    "energy_efficiency": 0.04045460373163223,
    "faradaic_efficiency": 0.14564242959022522,
    "ohmic_efficiency": 0.9310662150382996,
    "pH_normalized": 0.248920738697052,
    "precipitation_signal": 0.9723350405693054,
    "safety_risk": 0.1135944053530693,
    "score": 0.17448970675468445,
    "selective_product_yield": 0.018025610595941544,
    "transport_efficiency": 0.1490427851676941
  }
}
```

### 批次 8 · 终点事件 64

```json
{
  "ordinal": 8,
  "lifecycle_index": 8,
  "end_step": 64,
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
      "current_mA": 500,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -2
    },
    {
      "duration_s": 240,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "duration_s": 960,
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
    "cost": 0.3310000002384186,
    "electrochemical_conversion": 0.022918207570910454,
    "electrochemical_selectivity": 0.5049253702163696,
    "energy_efficiency": 0.04920337721705437,
    "faradaic_efficiency": 0.1797027587890625,
    "ohmic_efficiency": 0.9495700597763062,
    "pH_normalized": 0.23576228320598602,
    "precipitation_signal": 0.9881285429000854,
    "safety_risk": 0.12619440257549286,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.17320740222930908
  }
}
```

### 批次 9 · 终点事件 72

```json
{
  "ordinal": 9,
  "lifecycle_index": 9,
  "end_step": 72,
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
      "potential_V": -2
    },
    {
      "duration_s": 240,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "duration_s": 960,
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
    "cost": 0.305400013923645,
    "electrochemical_conversion": 0.04190802201628685,
    "electrochemical_selectivity": 0.5100141763687134,
    "energy_efficiency": 0.11369603127241135,
    "faradaic_efficiency": 0.26516643166542053,
    "ohmic_efficiency": 0.9518091082572937,
    "pH_normalized": 0.20225253701210022,
    "precipitation_signal": 0.8602932691574097,
    "safety_risk": 0.072194404900074,
    "score": 0.24610833823680878,
    "selective_product_yield": 0.03932176157832146,
    "transport_efficiency": 0.2859977185726166
  }
}
```

### 批次 10 · 终点事件 80

```json
{
  "ordinal": 10,
  "lifecycle_index": 10,
  "end_step": 80,
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
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -2
    },
    {
      "duration_s": 240,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "duration_s": 960,
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
    "cost": 0.305400013923645,
    "electrochemical_conversion": 0.05503680557012558,
    "electrochemical_selectivity": 0.49138349294662476,
    "energy_efficiency": 0.09015718847513199,
    "faradaic_efficiency": 0.2561946213245392,
    "ohmic_efficiency": 0.891998291015625,
    "pH_normalized": 0.15114770829677582,
    "precipitation_signal": 0.0,
    "safety_risk": 0.072194404900074,
    "score": 0.1769586205482483,
    "selective_product_yield": 0.01570836640894413,
    "transport_efficiency": 0.25754421949386597
  }
}
```

### 批次 11 · 终点事件 88

```json
{
  "ordinal": 11,
  "lifecycle_index": 11,
  "end_step": 88,
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
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": -2
    },
    {
      "duration_s": 240,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "duration_s": 960,
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
    "cost": 0.305400013923645,
    "electrochemical_conversion": 0.04069721698760986,
    "electrochemical_selectivity": 0.47143474221229553,
    "energy_efficiency": 0.07258089631795883,
    "faradaic_efficiency": 0.16945607960224152,
    "ohmic_efficiency": 0.9430109858512878,
    "pH_normalized": 0.26854175329208374,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.072194404900074,
    "score": 0.1430913805961609,
    "selective_product_yield": 0.014074541628360748,
    "transport_efficiency": 0.17663602530956268
  }
}
```

### 批次 12 · 终点事件 96

```json
{
  "ordinal": 12,
  "lifecycle_index": 12,
  "end_step": 96,
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
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -1.2
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
      "duration_s": 3000,
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
    "cost": 0.3023279905319214,
    "electrochemical_conversion": 0.01954413764178753,
    "electrochemical_selectivity": 0.5878042578697205,
    "energy_efficiency": 0.2075084000825882,
    "faradaic_efficiency": 0.337985634803772,
    "ohmic_efficiency": 0.9900268316268921,
    "pH_normalized": 0.20144374668598175,
    "precipitation_signal": 0.8506802320480347,
    "safety_risk": 0.072194404900074,
    "score": 0.2865492105484009,
    "selective_product_yield": 0.03205474466085434,
    "transport_efficiency": 0.3592105805873871
  }
}
```

## K1 封存报告

Mechanistic report

Experimental scope

All batches used 0.020 mol of limiting reagent in 0.040 L of one solvent, corresponding to an initial nominal loading of 0.50 mol L⁻¹ before sampling. Potential, current cap, electrolyte, solvent, and electrolysis time were varied. The reported current was a configured upper bound; delivered current was not measured. Final-assay standard uncertainties were approximately 0.010 for conversion and selective yield, 0.012 for selectivity and Faradaic/ohmic efficiency, 0.014 for transport efficiency, and 0.016 for energy efficiency. Consequently, values near 0.01—especially short-run yields and conversions—should not be overinterpreted.

Proposed process model

I infer a cathodic electrochemical pathway with four coupled stages:

1. A polarity/overpotential gate activates electron transfer. Positive potential is effectively unproductive in the explored domain, whereas negative potential enables target and competing reductions.
2. The cell and electrolyte determine delivered current through ohmic and interfacial limitations. A useful abstraction is

   I_del(t) = min[I_cap, G(S,E)|η|, I_transport(S,E,state)],

   where S is solvent, E is electrolyte, G is an effective conductance, and η is an effective overpotential after solvent/electrolyte potential shifts and unknown interface offsets.
3. Conversion accumulates with productive charge but eventually should saturate:

   X(t) ≈ 1 − exp[−k(S,E,η) ∫ I_del(t) dt /(nF N₀)].

   This is a qualitative equation rather than an identified kinetic law: electron stoichiometry n, electrode area, actual current, and rate constant were not observed.
4. Product formation is conversion multiplied by charge utilization and branching factors. Conceptually,

   Y_target ≈ X × FE(η,S,E,state) × Sel(η,S,E,state),

   with transport and precipitation able to alter both FE and selectivity. The separately calibrated assay channels are noisy, so I would not force this identity exactly on individual observations; for example, batch 2 reported conversion clipped to 0 but selective yield 0.0124.

The data suggest that increasing cathodic drive raises the attainable rate but lowers energy efficiency and, to a lesser extent, selectivity. Thus the fastest condition is not necessarily the best balanced condition. I would model FE, selectivity, and energy efficiency as plateaued or peaked functions of effective overpotential rather than constants.

Evidence for the polarity gate

Batch 1 used S0/E0, +1.2 V, a 100 mA cap, and 600 s. Its final assay was essentially inactive: conversion 0.0093, selectivity 0.0103, selective yield 0, FE 0.0245, transport efficiency 0, and energy efficiency 0.0053. Its 120 s UV–vis estimate likewise gave zero FE, transport, and energy efficiency.

Batch 2 changed only the sign to −1.2 V. At 120 s it already showed FE 0.325, transport efficiency 0.368, and energy efficiency 0.228. At 600 s its final selectivity was 0.576, FE 0.386, transport efficiency 0.412, energy efficiency 0.170, and yield 0.0124. These polarity-dependent differences are much larger than the stated measurement uncertainties. I therefore regard cathodic activation as the strongest identified relationship in the campaign.

Potential, time, and current-cap coupling

Batches 2 and 3 compared 100 and 500 mA caps at −1.2 V for 600 s in S0/E0. Contrary to a simple “more cap gives more product” rule, batch 3 had lower FE (0.216), transport efficiency (0.233), energy efficiency (0.112), and observed yield (0.00018) than batch 2. The yield difference is near the assay noise scale, but the efficiency differences are substantial. Possible explanations are that 100 mA was already sufficient for the potential-controlled current, that a higher cap allowed a less efficient interfacial regime, or that fixed transport limitation dominated. This experiment changed my interpretation of current_mA from a charge-delivery variable to a cap whose effect depends on whether it binds.

Batch 4 used −2.0 V, 500 mA, and 600 s in S0/E0. It gave conversion 0.0164, selectivity 0.456, yield 0.0100, FE 0.272, transport efficiency 0.241, and energy efficiency 0.0198. Relative to batch 2, the stronger cathodic drive did not clearly improve the short-run yield but sharply reduced energy efficiency and reduced selectivity.

The clearest extent result came from batch 5, which retained the batch-4 condition but increased total time from 600 to 3600 s. Conversion increased to 0.113 and yield to 0.0614, while selectivity was 0.494, FE 0.244, transport efficiency 0.233, and energy efficiency 0.0275. The roughly sixfold increase in time produced about a sixfold increase in observed yield relative to batch 4, consistent with low-conversion charge accumulation. This supports time dependence but does not prove first-order kinetics or exact linearity.

Batch 12 probed a milder regime: S0/E1, −1.2 V, 100 mA, 3600 s. Its final conversion was only 0.0195, but it retained selectivity 0.588, FE 0.338, transport efficiency 0.359, ohmic efficiency 0.990, energy efficiency 0.208, and yield 0.0321. Its 600 s UV–vis readout already showed FE 0.378, transport 0.381, and energy efficiency 0.189. Compared with the high-drive batch 5, batch 12 sacrificed extent but greatly improved every measured efficiency. This is why I interpret potential and cap as controlling a rate–quality tradeoff, not merely conversion.

Solvent effects

Batches 6–8 compared S1, S2, and S3 while holding E0, −2.0 V, 500 mA, and 1200 s fixed:

• Batch 6, S1: conversion 0.0423, selectivity 0.471, yield 0.0285, FE 0.274, transport 0.250, ohmic 0.920, energy 0.0548.
• Batch 7, S2: conversion 0.0339, selectivity 0.479, yield 0.0180, FE 0.146, transport 0.149, ohmic 0.931, energy 0.0405.
• Batch 8, S3: conversion 0.0229, selectivity 0.505, yield reported as 0, FE 0.180, transport 0.173, ohmic 0.950, energy 0.0492.

S1 was the strongest tested nonbaseline solvent under this matched condition, especially in FE, transport, and yield. S2 and S3 had reasonable ohmic efficiencies but poorer FE and transport, showing that bulk conductivity alone does not control productivity. The nominal dossier helps rationalize some trends—S1 has high relative diffusivity, while S2 and S3 have less favorable conductivity or diffusivity combinations—but it cannot explain the whole ordering. Hidden, fixed solvent–interface and solvent–electrolyte residuals are evidently important.

Solvent effects on pH and precipitation were smaller within E0 than electrolyte effects. Final pH_normalized values were 0.233 for S1, 0.249 for S2, and 0.236 for S3; precipitation remained high at 0.993, 0.972, and 0.988. Thus changing solvent alone did not remove the strong E0 precipitation tendency.

Electrolyte effects

Batches 9–11 varied electrolyte E1–E3 in S0 at −2.0 V, 500 mA, and 1200 s:

• Batch 9, E1: conversion 0.0419, selectivity 0.510, yield 0.0393, FE 0.265, transport 0.286, ohmic 0.952, energy 0.114, pH_normalized 0.202, precipitation 0.860.
• Batch 10, E2: conversion 0.0550, selectivity 0.491, yield 0.0157, FE 0.256, transport 0.258, ohmic 0.892, energy 0.0902, pH_normalized 0.151, precipitation 0.
• Batch 11, E3: conversion 0.0407, selectivity 0.471, yield 0.0141, FE 0.169, transport 0.177, ohmic 0.943, energy 0.0726, pH_normalized 0.269, precipitation 0.0052.

These results separate acid/salt behavior from productive electrochemistry. The pH ordering is qualitatively consistent with the nominal acid properties: the more acidic E2 had the lowest normalized pH, and weakly acidic E3 had the highest. The precipitation observations also broadly follow the declared salt/Ksp differences: E0 produced signals near 1, E1 reduced but did not eliminate precipitation, and E2/E3 nearly eliminated it.

However, precipitation suppression did not maximize target yield. E2 had the highest conversion of the matched electrolyte series but much lower yield than E1, while E3 lost FE and transport performance. This suggests either competing conversion, altered interfacial kinetics, or target-branch suppression. E1 was the best balanced electrolyte tested, combining the highest yield, transport efficiency, and energy efficiency of this matched series with reduced precipitation.

Ohmic and transport interpretation

Ohmic efficiencies were generally high, approximately 0.88–0.99, even when conversion or yield was poor. Therefore cell resistance was not the sole bottleneck. Transport efficiencies varied more strongly, approximately 0–0.41 across the campaign, and tracked productive cathodic operation and material identity more closely.

A plausible decomposition is

   η_ohm = f[κ(S,E), fixed contact resistance, I_del],
   η_transport = f[D(S,E)/δ(E), concentration, reaction rate],

where κ is effective conductivity, D effective diffusivity, and δ an effective diffusion-layer thickness. These variables are informed by the nominal dossier but include unknown world-specific residuals. The consistently high E0/S0 ohmic efficiency alongside only moderate transport efficiency supports a diffusion/mass-transfer limitation rather than a purely resistive limitation.

Acid/base and precipitation coupling

I infer a parallel equilibrium subsystem rather than a simple causal chain from precipitation to product. Electrolyte acid concentration and pKa control pH; precipitating-salt concentration, Ksp, solvent solubility factors, and reaction-generated ionic species control precipitation. Precipitation may remove charge carriers or foul the interface, but the campaign does not identify whether it directly causes efficiency loss. E2 and E3 are important counterexamples: both suppressed precipitation without giving the best target yield. Thus precipitation is a state descriptor and possible modifier, not a reliable surrogate objective.

How the explanation changed

The initial working hypothesis was that polarity and overpotential would govern conversion, current cap would primarily regulate charge delivery, and nominal conductivity/diffusivity would predict material performance. Batch 1 versus batch 2 strongly confirmed the polarity hypothesis. Batches 2–3 weakened the simple current-cap hypothesis because raising the cap did not improve the outcome. Batches 4–5 established duration as a major extent variable and exposed the energy/selectivity cost of stronger cathodic drive. Batches 6–11 showed that nominal properties explain only broad tendencies: S1 and E1 were favorable, but conductivity, low precipitation, or high conversion alone did not rank target yield. Batch 12 confirmed prospectively that a mild cathodic E1 condition could retain substantially better efficiencies over a long run, although its low conversion showed that it is not a high-throughput condition.

Scope and extrapolation

The polarity conclusion is robust for the tested loading, materials, and +1.2/−1.2 V comparison. Time scaling is supported locally for S0/E0 at −2.0 V between 600 and 3600 s, but should not be extrapolated linearly toward complete conversion. Material rankings are one-factor conclusions at −2.0 V, 500 mA, and 1200 s; they need not persist at other potentials, concentrations, or times. Batch 12 suggests E1 remains favorable at −1.2 V, but because it also changed duration relative to batch 2, it does not independently identify an E1 effect at mild potential.

The explored potential response is sparse: +1.2, −1.2, and −2.0 V were tested, but no threshold scan or potentials near zero were measured. Likewise, only one direct current-cap contrast was made, and actual current, charge, temperature trajectory, electrode area, gap, and interfacial resistance were unavailable. No solvent–electrolyte interaction matrix was run: notably, the potentially attractive S1/E1 pair was not tested. There were no true replicate batches, so hidden run-to-run variability cannot be separated from assay noise.

Unidentifiable factors and alternatives

The observations cannot uniquely distinguish Butler–Volmer electron-transfer kinetics from a simpler thresholded empirical potential response. They also cannot distinguish diffusion-layer limitation from electrode fouling, precipitation-induced blocking, reagent adsorption, or a cap-dependent change in the simulated interface. A competing cathodic reaction is plausible because stronger drive can preserve conversion while lowering target efficiency, but no byproduct identity was observed. The mismatch among independently noisy conversion, yield, and selectivity channels—especially in batches 2 and 3—prevents strict mass-balance reconstruction at low signal.

A credible alternative model is that effective potential shifts, rather than intrinsic selectivity changes, explain much of the electrolyte ordering. Another is that E1 primarily improves mass transfer or interface stability while its acid and precipitation properties are secondary. These alternatives remain observationally equivalent with the available design.

Overall account

This world behaves like a cathodically activated, charge-accumulating conversion in which potential magnitude controls both rate and efficiency, current is capped rather than guaranteed, and solvent/electrolyte properties independently influence ohmic transport, mass transfer, acid/base state, precipitation, and interfacial selectivity. Mild cathodic drive favors selectivity and energy efficiency; stronger cathodic drive plus long time increases extent. E1 provided the best tested electrolyte compromise, S1 was the best tested nonbaseline solvent under the matched material screen, and suppression of precipitation alone was not sufficient for high target yield. The most defensible predictive form is therefore a signed-potential activation model with saturating charge accumulation and separate material-dependent efficiency factors, rather than a single linear regression on voltage, nominal conductivity, or elapsed time.

## K2 封存报告

1. Supported, contradicted, and untested claims

No explicit instance-specific mechanism or quantitative response-law prior was supplied. The material dossier supplied nominal solvent and electrolyte properties, but it explicitly described them as incomplete priors subject to hidden fixed residuals; it did not supply the world’s selectivity, Faradaic-efficiency, or kinetic law.

Supported claims:

• A polarity gate was strongly supported. Batch 1 at +1.2 V was essentially inactive, whereas otherwise matched batch 2 at −1.2 V showed selectivity 0.576, Faradaic efficiency 0.386, transport efficiency 0.412, and nonzero target yield. This was the clearest evidence changing the initial tentative polarity hypothesis into a supported claim.

• Electrolysis time controls reaction extent in the active cathodic regime. At S0/E0, −2.0 V, and 500 mA, extending electrolysis from 600 s in batch 4 to 3600 s in batch 5 increased conversion from 0.016 to 0.113 and yield from 0.010 to 0.061. This supported cumulative-charge or time-integrated kinetics locally, though not a globally linear law.

• Stronger cathodic drive entails a rate–quality tradeoff. Batches 4–5 achieved more extent at −2.0 V, but their energy efficiencies were only about 0.020–0.027, compared with 0.170 in batch 2 and 0.208 in batch 12 at −1.2 V. Selectivity was also lower near −2.0 V. This supported separating extent from Faradaic, selectivity, and energy-efficiency factors.

• Electrolyte acid and salt properties were qualitatively informative for pH and precipitation. In the matched electrolyte screen, batch 10/E2 had the lowest normalized pH, 0.151, and no detected precipitation; batch 11/E3 had high normalized pH, 0.269, and precipitation near zero; batch 9/E1 was intermediate. This broadly agreed with the nominal acid and precipitation dossier.

• E1 was the best tested balanced electrolyte. Under the matched −2.0 V screen, batch 9/E1 produced yield 0.039, transport efficiency 0.286, and energy efficiency 0.114, outperforming batches 10/E2 and 11/E3 on the balanced outcome. Batch 12 further showed that E1 could retain high efficiency under milder cathodic drive.

Contradicted or weakened claims:

• The simple claim that a higher current cap should increase productive output was contradicted or at least seriously weakened. At −1.2 V and 600 s, raising the cap from 100 mA in batch 2 to 500 mA in batch 3 reduced the observed Faradaic, transport, and energy efficiencies. The very small yields were noise-sensitive, but the efficiency changes were too large to justify treating configured current as delivered charge.

• A simple nominal-conductivity ranking was contradicted. Batches 6–8 all retained high ohmic efficiency, yet S2 and S3 had substantially poorer Faradaic and transport performance than S1. Bulk conductivity alone therefore did not predict target production.

• The claim that suppressing precipitation should improve target yield was contradicted. Batches 10 and 11 nearly eliminated precipitation but did not outperform batch 9/E1 in yield. Precipitation may modify the interface, but it was not a sufficient productivity proxy.

• An exact identity between measured conversion, selectivity, and selective yield was not supported at low signal. For example, batch 2 reported conversion clipped to zero but yield 0.012. Independent assay noise and clipping make a strict batch-level mass-balance equation inappropriate near the detection floor.

Untested claims:

• No solvent-by-electrolyte interaction matrix was tested; notably S1/E1 was never run.

• The activation threshold and detailed potential-response shape were untested between +1.2 and −1.2 V and beyond the sparse −2.0 V point.

• Saturation at high conversion, deactivation, electrode fouling, and the electron stoichiometry were untested.

• Delivered current was not measured, so current-cap binding could not be identified directly.

• There were no true replicates, preventing separation of process variability from assay noise.

2. Most informative additional experiment

I would run one S1/E1 batch at the established loading, −2.0 V, 500 mA, and 1200 s, with an intermediate UV–vis measurement at 240 s and the final assay. This would complete the most important missing interaction cell relative to batch 6, which isolated S1 with E0, and batch 9, which isolated E1 with S0.

The leading explanation treats solvent and electrolyte as approximately separable modifiers of transport, ohmic loss, acid/precipitation state, and interfacial efficiency. It therefore predicts that S1/E1 should preserve or combine the favorable transport and productivity seen in batches 6 and 9, subject to saturation.

A plausible alternative is that hidden solvent–electrolyte interfacial coupling dominates the apparent one-factor rankings. If S1/E1 produced substantially poorer Faradaic efficiency, transport efficiency, or yield than both batches 6 and 9, I would reject approximate separability and give interaction-specific interface chemistry a central role. If it markedly exceeded both one-factor results, I would likewise infer a strong positive interaction rather than simple additivity. If it fell near a bounded combination of batches 6 and 9, with E1-like precipitation and S1/E1-like transport improvements, that would strengthen the separable-factor account. An early UV–vis result followed by a concordant final result would also help distinguish an initial-rate effect from late deactivation, although one batch would still not establish repeatability.

3. Unused evidence, weak predictions, and influence of the goal

The full raw spectral artifacts were not analyzed; the account used processed estimates and supplied peak summaries. Consequently, possible peak-shape, baseline, or minor-band evidence was unused. Detailed nominal quantities such as double-layer capacitance, supporting-electrolyte concentration, and diffusion-layer thickness were considered qualitatively but were not fitted quantitatively. Cost, small sampling-volume changes, and most thermal-state information were not used in the mechanism because they did not vary in a sufficiently controlled way. The intermediate UV–vis measurements were used mainly as qualitative early-time checks rather than as a formally fitted time series.

The least reliable blind predictions are the 7200 s predictions at ±0.8 V, because neither potential was tested and 7200 s exceeds the campaign’s longest 3600 s run. Predictions for positive-potential E1, E3, and S2 cases are especially uncertain: the only positive control was batch 1 with S0/E0 at +1.2 V. Q11 and Q12 are also weak because they combine the untested ±0.8 V values, long duration, and a 500 mA cap, while the only direct cap comparison was the short −1.2 V comparison between batches 2 and 3. The E3 and S2 cathodic predictions additionally assume that material rankings extrapolate across potential and duration, which was not demonstrated.

The sealed recommendation of batch 12 is reliable only as an empirical choice among the twelve observed batches: it had the highest measured balanced score and favorable efficiencies. Its causal interpretation is less reliable because it changed both electrolyte and duration relative to batch 2, and it was not replicated. It should not be read as proof that E1 alone caused the improvement or that the condition is universally optimal.

The assigned goal did affect evidence collection. Because the primary goal emphasized an explanatory and predictive account rather than score maximization, the campaign allocated batches to polarity, duration, current-cap, solvent, and electrolyte contrasts. That breadth enabled the mechanism report but left no true replicates, no dense potential curve, and no full interaction design. A purely optimization-focused campaign would probably have concentrated more trials around E1 and mild cathodic conditions after batch 9, whereas this campaign retained broad material comparisons. There was no clear conflict with safety: the tested recipes stayed far below the published safety limit.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.63,
        "lower80": 0.54,
        "upper80": 0.71
      },
      "energy_efficiency": {
        "estimate": 0.23,
        "lower80": 0.14,
        "upper80": 0.32
      },
      "faradaic_efficiency": {
        "estimate": 0.4,
        "lower80": 0.3,
        "upper80": 0.48
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.09,
        "lower80": 0,
        "upper80": 0.23
      },
      "selective_product_yield": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.02
      },
      "transport_efficiency": {
        "estimate": 0.4,
        "lower80": 0.29,
        "upper80": 0.49
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.025
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0,
        "upper80": 0.03
      },
      "faradaic_efficiency": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.025
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.012,
        "lower80": 0,
        "upper80": 0.055
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0,
        "upper80": 0.013
      },
      "transport_efficiency": {
        "estimate": 0.004,
        "lower80": 0,
        "upper80": 0.025
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.64,
        "lower80": 0.56,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.24,
        "lower80": 0.16,
        "upper80": 0.33
      },
      "faradaic_efficiency": {
        "estimate": 0.4,
        "lower80": 0.3,
        "upper80": 0.48
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.319,
        "lower80": 0.22,
        "upper80": 0.4
      },
      "selective_product_yield": {
        "estimate": 0.046,
        "lower80": 0.022,
        "upper80": 0.085
      },
      "transport_efficiency": {
        "estimate": 0.4,
        "lower80": 0.29,
        "upper80": 0.49
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.025
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0,
        "upper80": 0.03
      },
      "faradaic_efficiency": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.025
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.012,
        "lower80": 0,
        "upper80": 0.055
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0,
        "upper80": 0.013
      },
      "transport_efficiency": {
        "estimate": 0.004,
        "lower80": 0,
        "upper80": 0.025
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.65,
        "lower80": 0.57,
        "upper80": 0.73
      },
      "energy_efficiency": {
        "estimate": 0.26,
        "lower80": 0.17,
        "upper80": 0.35
      },
      "faradaic_efficiency": {
        "estimate": 0.4,
        "lower80": 0.31,
        "upper80": 0.48
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.327,
        "lower80": 0.24,
        "upper80": 0.41
      },
      "selective_product_yield": {
        "estimate": 0.056,
        "lower80": 0.027,
        "upper80": 0.1
      },
      "transport_efficiency": {
        "estimate": 0.39,
        "lower80": 0.29,
        "upper80": 0.48
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.025
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0,
        "upper80": 0.03
      },
      "faradaic_efficiency": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.025
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.012,
        "lower80": 0,
        "upper80": 0.055
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0,
        "upper80": 0.013
      },
      "transport_efficiency": {
        "estimate": 0.004,
        "lower80": 0,
        "upper80": 0.025
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.61,
        "lower80": 0.51,
        "upper80": 0.7
      },
      "energy_efficiency": {
        "estimate": 0.18,
        "lower80": 0.1,
        "upper80": 0.27
      },
      "faradaic_efficiency": {
        "estimate": 0.25,
        "lower80": 0.16,
        "upper80": 0.34
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.264,
        "lower80": 0.17,
        "upper80": 0.35
      },
      "selective_product_yield": {
        "estimate": 0.031,
        "lower80": 0.01,
        "upper80": 0.06
      },
      "transport_efficiency": {
        "estimate": 0.23,
        "lower80": 0.14,
        "upper80": 0.33
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.025
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0,
        "upper80": 0.03
      },
      "faradaic_efficiency": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.025
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.012,
        "lower80": 0,
        "upper80": 0.055
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0,
        "upper80": 0.013
      },
      "transport_efficiency": {
        "estimate": 0.004,
        "lower80": 0,
        "upper80": 0.025
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.52,
        "upper80": 0.71
      },
      "energy_efficiency": {
        "estimate": 0.17,
        "lower80": 0.09,
        "upper80": 0.26
      },
      "faradaic_efficiency": {
        "estimate": 0.25,
        "lower80": 0.16,
        "upper80": 0.34
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.259,
        "lower80": 0.16,
        "upper80": 0.35
      },
      "selective_product_yield": {
        "estimate": 0.03,
        "lower80": 0.009,
        "upper80": 0.06
      },
      "transport_efficiency": {
        "estimate": 0.22,
        "lower80": 0.13,
        "upper80": 0.32
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.025
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0,
        "upper80": 0.03
      },
      "faradaic_efficiency": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.025
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.011,
        "lower80": 0,
        "upper80": 0.052
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0,
        "upper80": 0.013
      },
      "transport_efficiency": {
        "estimate": 0.004,
        "lower80": 0,
        "upper80": 0.025
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.51,
        "upper80": 0.7
      },
      "energy_efficiency": {
        "estimate": 0.16,
        "lower80": 0.08,
        "upper80": 0.25
      },
      "faradaic_efficiency": {
        "estimate": 0.25,
        "lower80": 0.15,
        "upper80": 0.35
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.265,
        "lower80": 0.16,
        "upper80": 0.36
      },
      "selective_product_yield": {
        "estimate": 0.045,
        "lower80": 0.015,
        "upper80": 0.085
      },
      "transport_efficiency": {
        "estimate": 0.25,
        "lower80": 0.15,
        "upper80": 0.35
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.025
      },
      "energy_efficiency": {
        "estimate": 0.004,
        "lower80": 0,
        "upper80": 0.028
      },
      "faradaic_efficiency": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.025
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.011,
        "lower80": 0,
        "upper80": 0.052
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0,
        "upper80": 0.013
      },
      "transport_efficiency": {
        "estimate": 0.004,
        "lower80": 0,
        "upper80": 0.025
      }
    }
  ],
  "rationale": "The campaign showed a strong polarity gate: cathodic operation was productive, while +1.2 V was essentially inactive, so all +0.8 V predictions remain near the assay floor. For −0.8 V, I extrapolated the higher selectivity and efficiency expected at milder cathodic drive, with yield increasing over 7200 s but remaining uncertain because this potential was not tested. E1 receives the best material adjustment; E3 and S2 receive lower Faradaic and transport efficiencies. A 500 mA cap is allowed more extent but penalized efficiency based on the −1.2 V cap comparison. Intervals include assay noise, sparse potential coverage, uncertain current-cap binding, and untested long-time/material interactions."
}
```
