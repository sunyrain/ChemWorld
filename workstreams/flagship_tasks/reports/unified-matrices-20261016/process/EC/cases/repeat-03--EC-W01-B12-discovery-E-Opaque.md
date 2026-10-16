# repeat-03/EC-W01-B12-discovery-E-Opaque

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-03\EC-W01-B12-discovery-E-Opaque\participant\discovery-E-Opaque

## 同期笔记

### v1 · 公开事件 0

# Pre-experiment hypotheses

**H1 [tentative].** At fixed loading, electrochemical conversion should increase with delivered charge until depletion or degradation, while selectivity and efficiency may peak at an intermediate potential/current/time rather than increasing monotonically. Because current is only a cap, potential and electrolyte/solvent can also change delivered charge through transport/ohmic effects.

**H2 [tentative].** Potential sign may gate productive versus nonproductive chemistry; material identities may shift transport, pH, and precipitation. I will hold reagent concentration constant where possible, span both signs and short/long electrolysis, and use replicated/contrasting conditions to separate sign, duration, cap, solvent, and electrolyte effects.

**Precommitted tests.** Early broad runs will locate the productive sign and approximate response scale. Later runs will test duration and current-cap response within that sign, material swaps, and at least one repeat. A result inconsistent with monotone charge response will shift the account toward saturation/degradation or potential-limited delivery. Intermediate UV-vis or pH readings will be reserved for paired time-course or mechanistic contrasts; final assays are authoritative for outcome comparisons.

### v2 · 公开事件 42

# Working explanatory account after six batches

**H1 [supported within S0/E0, unresolved generally].** Productive chemistry is associated with negative potential. At +1.5 V for 600 s, efficiencies and yield were essentially zero (events runner-operation-0005, -0007); at -1.5 V for the same cap/time, efficiency channels were clearly nonzero and final selectivity was about 0.56 (events -0012, -0014). This sign contrast is much larger than stated assay noise, although conversion/yield remain near the low-signal region.

**H2 [supported qualitatively].** Potential magnitude has a selectivity/efficiency optimum rather than monotone benefit: -1.0 V, 100 mA, 1800 s outperformed -2.0 V at matched cap/time on efficiency and selectivity (events -0021, -0028). A plausible account is competing nonproductive current at excessive overpotential; a narrower voltage scan would test it.

**H3 [supported within tested range].** Extent rises with longer electrolysis/delivered-charge opportunity, while high current caps penalize transport/ohmic/faradaic efficiency. At -1.0 V, raising cap and duration from 100 mA/1800 s to 500 mA/3600 s raised conversion/yield but lowered efficiency (events -0028, -0035). Using 250 mA/7200 s increased conversion/yield again and recovered efficiency (event -0042). Because duration and cap were jointly changed, this is not yet a separately identified kinetic law.

**H4 [unresolved].** The consistently high precipitation signal (~0.99-1) may be a medium/loading feature or coupled to reaction state; current evidence cannot distinguish. Next I will compare anonymous solvent/electrolyte combinations at a common negative-potential protocol, then repeat/refine the most informative condition. Material comparisons, not labels, will determine scope.

### v3 · 公开事件 84

# Final source-stage hypothesis notebook

**H1 [supported in tested scope].** Product formation is cathodic/sign-gated: +1.5 V gave no detectable selective yield, whereas -1.5 V at matched loading, cap, and time gave nonzero faradaic/transport response and a small positive yield (events runner-operation-0007 and -0014). Prediction: positive-potential blind cases remain near zero yield, while moderate negative cases are productive.

**H2 [supported qualitatively; quantitative form unresolved].** There is an intermediate negative-potential efficiency optimum. At common S0/E0 and 100 mA/1800 s, -1.0 V had higher selectivity, faradaic efficiency, and energy efficiency than -2.0 V (events -0021 and -0028). This supports increasing activation followed by an overpotential penalty, but the sparse voltage grid cannot identify curvature or an exact optimum.

**H3 [supported in S0/E0 but cap and time partly confounded].** Product extent increases with electrolysis opportunity, while larger current caps trade throughput for transport/ohmic/faradaic efficiency. The sequence 100 mA/1800 s, 500 mA/3600 s, and 250 mA/7200 s at -1.0 V showed increasing conversion/yield overall, with the intermediate cap/long duration giving the best balance (events -0028, -0035, -0042). A predictive model should therefore use a saturating charge/time term multiplied by potential-, cap-, solvent-, and electrolyte-efficiency factors, not treat the cap as guaranteed current. Long extrapolations remain uncertain because depletion/degradation was not reached.

**H4 [supported material dependence].** At -1.0 V, 250 mA, 7200 s, E0, solvent S1 numerically outperformed S0/S2/S3 in conversion, yield, and overall score (events -0042, -0049, -0056, -0063). Differences from S2/S3 exceed several stated channel noise scales; S1 versus S0 is smaller and unreplicated. S2/S3 also carried higher observed risk. Scope is fixed loading (0.02 mol in 0.04 L nominal before sampling).

**H5 [supported for electrolyte control of side-state; productivity ranking uncertain].** With S1 and the common electrolysis protocol, changing E0→E1→E2→E3 strongly shifted pH and precipitation: E2/E3 suppressed precipitation from near unity to near zero, while E1 was intermediate (events -0049, -0070, -0077, -0084). Productivity scores among E0 and E1 were nearly equal relative to assay noise, so no unique best electrolyte is established. This decoupling suggests electrolyte governs acid/base/solubility state more strongly than the primary cathodic formation step.

**Unresolved alternatives and limitations.** No exact repeats were completed, so numerical differences smaller than combined stated measurement noise are not evidence of effects. Duration and cap were not fully factorial, delivered current was not directly observed, and high precipitation may mask rather than cause poor transport. The strongest operating observation is batch 7 (S1/E0, -1.0 V, 250 mA cap, 7200 s), but batch 10 (S1/E1) is essentially tied on score and has substantially lower precipitation. A future discriminating study should repeat these two conditions and add multiple durations at fixed cap to fit a saturating charge-response law.

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
    "cost": 0.2829599976539612,
    "electrochemical_conversion": 0.008014115504920483,
    "electrochemical_selectivity": 0.01034972071647644,
    "energy_efficiency": 0.005256945732980967,
    "faradaic_efficiency": 0.02452157624065876,
    "ohmic_efficiency": 0.976645290851593,
    "pH_normalized": 0.23218974471092224,
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
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
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
    "cost": 0.2829599976539612,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.560074508190155,
    "energy_efficiency": 0.10744526237249374,
    "faradaic_efficiency": 0.3135705590248108,
    "ohmic_efficiency": 0.9854831099510193,
    "pH_normalized": 0.2294943928718567,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.14816011488437653,
    "selective_product_yield": 0.011662633158266544,
    "transport_efficiency": 0.33982735872268677
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
      "potential_V": -2
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
    "cost": 0.28404000401496887,
    "electrochemical_conversion": 0.006130163092166185,
    "electrochemical_selectivity": 0.4782479703426361,
    "energy_efficiency": 0.05836587771773338,
    "faradaic_efficiency": 0.22284860908985138,
    "ohmic_efficiency": 0.9758104681968689,
    "pH_normalized": 0.23020939528942108,
    "precipitation_signal": 0.9868234395980835,
    "safety_risk": 0.072194404900074,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.2394055277109146
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
    "electrochemical_conversion": 0.014539969153702259,
    "electrochemical_selectivity": 0.5868677496910095,
    "energy_efficiency": 0.21439558267593384,
    "faradaic_efficiency": 0.42112892866134644,
    "ohmic_efficiency": 0.9773074388504028,
    "pH_normalized": 0.2295188158750534,
    "precipitation_signal": 0.987571656703949,
    "safety_risk": 0.072194404900074,
    "score": 0.1767764836549759,
    "selective_product_yield": 0.01206878200173378,
    "transport_efficiency": 0.3896414041519165
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
    "electrochemical_conversion": 0.07645079493522644,
    "electrochemical_selectivity": 0.6339096426963806,
    "energy_efficiency": 0.07515961676836014,
    "faradaic_efficiency": 0.16754864156246185,
    "ohmic_efficiency": 0.8914523720741272,
    "pH_normalized": 0.2344796061515808,
    "precipitation_signal": 0.9868980646133423,
    "safety_risk": 0.072194404900074,
    "score": 0.23741303384304047,
    "selective_product_yield": 0.05427209287881851,
    "transport_efficiency": 0.15703916549682617
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
      "current_mA": 250,
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
    "cost": 0.2897999882698059,
    "electrochemical_conversion": 0.1428254246711731,
    "electrochemical_selectivity": 0.6242353916168213,
    "energy_efficiency": 0.19092358648777008,
    "faradaic_efficiency": 0.3256781995296478,
    "ohmic_efficiency": 0.9466148614883423,
    "pH_normalized": 0.23120366036891937,
    "precipitation_signal": 0.9975283145904541,
    "safety_risk": 0.072194404900074,
    "score": 0.31073272228240967,
    "selective_product_yield": 0.09755419939756393,
    "transport_efficiency": 0.300994873046875
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
      "volume_L": 0.04
    },
    {
      "current_mA": 250,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1
    },
    {
      "duration_s": 7200,
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
    "cost": 0.298799991607666,
    "electrochemical_conversion": 0.1738084852695465,
    "electrochemical_selectivity": 0.6127479076385498,
    "energy_efficiency": 0.27672162652015686,
    "faradaic_efficiency": 0.35262489318847656,
    "ohmic_efficiency": 0.961149275302887,
    "pH_normalized": 0.2341933399438858,
    "precipitation_signal": 0.9779878854751587,
    "safety_risk": 0.09559440612792969,
    "score": 0.33795174956321716,
    "selective_product_yield": 0.10780337452888489,
    "transport_efficiency": 0.35602524876594543
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
      "volume_L": 0.04
    },
    {
      "current_mA": 250,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1
    },
    {
      "duration_s": 7200,
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
    "cost": 0.32440000772476196,
    "electrochemical_conversion": 0.1355125457048416,
    "electrochemical_selectivity": 0.4778125286102295,
    "energy_efficiency": 0.20788030326366425,
    "faradaic_efficiency": 0.3093498647212982,
    "ohmic_efficiency": 0.9355753064155579,
    "pH_normalized": 0.24495884776115417,
    "precipitation_signal": 0.986085057258606,
    "safety_risk": 0.1135944053530693,
    "score": 0.272785484790802,
    "selective_product_yield": 0.047089483588933945,
    "transport_efficiency": 0.3028545081615448
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
      "volume_L": 0.04
    },
    {
      "current_mA": 250,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1
    },
    {
      "duration_s": 7200,
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
    "cost": 0.3084000051021576,
    "electrochemical_conversion": 0.09779226779937744,
    "electrochemical_selectivity": 0.5305331349372864,
    "energy_efficiency": 0.18303661048412323,
    "faradaic_efficiency": 0.2051016241312027,
    "ohmic_efficiency": 0.968878448009491,
    "pH_normalized": 0.24180050194263458,
    "precipitation_signal": 0.9946194887161255,
    "safety_risk": 0.12619440257549286,
    "score": 0.2628394067287445,
    "selective_product_yield": 0.071029894053936,
    "transport_efficiency": 0.22593289613723755
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
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "current_mA": 250,
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
    "cost": 0.3057999908924103,
    "electrochemical_conversion": 0.17739765346050262,
    "electrochemical_selectivity": 0.6054915189743042,
    "energy_efficiency": 0.33334824442863464,
    "faradaic_efficiency": 0.35643452405929565,
    "ohmic_efficiency": 0.9020342230796814,
    "pH_normalized": 0.20164410769939423,
    "precipitation_signal": 0.7191752791404724,
    "safety_risk": 0.09559440612792969,
    "score": 0.33705437183380127,
    "selective_product_yield": 0.09258454293012619,
    "transport_efficiency": 0.35778412222862244
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
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "current_mA": 250,
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
    "cost": 0.3057999908924103,
    "electrochemical_conversion": 0.1646042764186859,
    "electrochemical_selectivity": 0.5578301548957825,
    "energy_efficiency": 0.33304116129875183,
    "faradaic_efficiency": 0.3262925148010254,
    "ohmic_efficiency": 0.8905975222587585,
    "pH_normalized": 0.15492473542690277,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.09559440612792969,
    "score": 0.3200053572654724,
    "selective_product_yield": 0.08721356838941574,
    "transport_efficiency": 0.33347246050834656
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
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "current_mA": 250,
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
    "cost": 0.3057999908924103,
    "electrochemical_conversion": 0.1266491562128067,
    "electrochemical_selectivity": 0.5457717180252075,
    "energy_efficiency": 0.2880180776119232,
    "faradaic_efficiency": 0.2726193070411682,
    "ohmic_efficiency": 0.9567427635192871,
    "pH_normalized": 0.2773926258087158,
    "precipitation_signal": 0.0,
    "safety_risk": 0.09559440612792969,
    "score": 0.30385470390319824,
    "selective_product_yield": 0.09161052852869034,
    "transport_efficiency": 0.2938442528247833
  }
}
```

## K1 封存报告

## Mechanistic account

I interpret this world as a cathodic conversion of a limiting reactant into a target product, accompanied by competing charge-consuming pathways. Productive conversion requires the correct potential sign, while potential magnitude, current cap, duration, solvent, and electrolyte jointly determine reaction extent and the faradaic, transport, ohmic, and energy losses. Electrolyte also controls an acid/base–solubility state that is visible through normalized pH and precipitation.

All batches used 0.020 mol reagent in 0.040 L nominal solvent, so the investigated starting concentration was approximately 0.50 mol L⁻¹. Material labels are anonymous; no real chemical identity is inferred.

## Observational basis

The principal final-assay results were:

| Batch | Solvent/electrolyte | Potential, cap, time | Conversion | Selectivity | Selective yield | FE | Transport | Ohmic | Energy | pH norm. | Precip. | Score |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | S0/E0 | +1.5 V, 100 mA, 600 s | 0.0080 | 0.0103 | 0.0000 | 0.0245 | 0.0000 | 0.9766 | 0.0053 | 0.2322 | 1.0000 | 0.0000 |
| 2 | S0/E0 | −1.5 V, 100 mA, 600 s | 0.0000* | 0.5601 | 0.0117 | 0.3136 | 0.3398 | 0.9855 | 0.1074 | 0.2295 | 1.0000 | 0.1482 |
| 3 | S0/E0 | −2.0 V, 100 mA, 1800 s | 0.0061 | 0.4782 | 0.0000 | 0.2228 | 0.2394 | 0.9758 | 0.0584 | 0.2302 | 0.9868 | 0.0000 |
| 4 | S0/E0 | −1.0 V, 100 mA, 1800 s | 0.0145 | 0.5869 | 0.0121 | 0.4211 | 0.3896 | 0.9773 | 0.2144 | 0.2295 | 0.9876 | 0.1768 |
| 5 | S0/E0 | −1.0 V, 500 mA, 3600 s | 0.0765 | 0.6339 | 0.0543 | 0.1675 | 0.1570 | 0.8915 | 0.0752 | 0.2345 | 0.9869 | 0.2374 |
| 6 | S0/E0 | −1.0 V, 250 mA, 7200 s | 0.1428 | 0.6242 | 0.0976 | 0.3257 | 0.3010 | 0.9466 | 0.1909 | 0.2312 | 0.9975 | 0.3107 |
| 7 | S1/E0 | −1.0 V, 250 mA, 7200 s | 0.1738 | 0.6127 | 0.1078 | 0.3526 | 0.3560 | 0.9611 | 0.2767 | 0.2342 | 0.9780 | 0.3380 |
| 8 | S2/E0 | −1.0 V, 250 mA, 7200 s | 0.1355 | 0.4778 | 0.0471 | 0.3093 | 0.3029 | 0.9356 | 0.2079 | 0.2450 | 0.9861 | 0.2728 |
| 9 | S3/E0 | −1.0 V, 250 mA, 7200 s | 0.0978 | 0.5305 | 0.0710 | 0.2051 | 0.2259 | 0.9689 | 0.1830 | 0.2418 | 0.9946 | 0.2628 |
| 10 | S1/E1 | −1.0 V, 250 mA, 7200 s | 0.1774 | 0.6055 | 0.0926 | 0.3564 | 0.3578 | 0.9020 | 0.3333 | 0.2016 | 0.7192 | 0.3371 |
| 11 | S1/E2 | −1.0 V, 250 mA, 7200 s | 0.1646 | 0.5578 | 0.0872 | 0.3263 | 0.3335 | 0.8906 | 0.3330 | 0.1549 | 0.0052 | 0.3200 |
| 12 | S1/E3 | −1.0 V, 250 mA, 7200 s | 0.1266 | 0.5458 | 0.0916 | 0.2726 | 0.2938 | 0.9567 | 0.2880 | 0.2774 | 0.0000 | 0.3039 |

*The batch-2 conversion estimate was clipped at zero despite a small positive yield and strong efficiency signals; I treat it as a near-detection-limit inconsistency rather than literal negative mechanistic evidence.

## 1. Potential sign gates the productive pathway

The clearest causal contrast is batches 1 and 2. They differed only in potential sign: +1.5 versus −1.5 V. At positive potential, selective yield, transport efficiency, and useful energy efficiency were essentially zero. Reversing the sign produced selectivity 0.560, FE 0.314, transport efficiency 0.340, and yield 0.0117. These changes are much larger than the published final-assay noise scales.

I therefore infer a cathodic productive step, schematically

R + n e⁻ → P,

with positive potential either failing to activate R or directing charge into a different, unobserved process. High ohmic efficiency in both batches shows that good electrical conduction alone is insufficient: batch 1 had ohmic efficiency 0.977 but made no measurable product. Thus the important gate is electrochemical direction and reaction kinetics, not merely cell resistance.

A useful model factor is a cathodic activation term g(V) that is close to zero for positive V and positive for negative V. This inference is strong within the tested range, but the exact threshold potential was not measured.

## 2. Excess negative potential creates a nonproductive overpotential penalty

Batches 3 and 4 compared −2.0 and −1.0 V at identical S0/E0 composition, 100 mA cap, and 1800 s duration. The less extreme potential was better on every reaction-efficiency measure: selectivity rose from 0.478 to 0.587, FE from 0.223 to 0.421, transport efficiency from 0.239 to 0.390, and energy efficiency from 0.058 to 0.214. The yield changed from a clipped zero to 0.0121.

This rejects a simple rule that increasingly negative potential always improves the process. My preferred explanation is that negative potential initially activates the productive electron-transfer pathway, but excessive overpotential increases parasitic current, degradation, or another charge-consuming reaction. In generic form,

g(V) = activation(V) × penalty(V),

where activation grows after crossing a cathodic threshold and penalty decreases again at excessive magnitude. A bell-shaped response or the product of two logistic functions would be reasonable. The observations locate −1.0 V on a better part of this window than −2.0 V, but they do not prove that −1.0 V is the exact optimum; values between or around those points were not mapped at matched time.

The −1.5 V result cannot cleanly refine the curve because batch 2 used only 600 s and was close to the assay detection boundary.

## 3. Extent depends on electrolysis opportunity, while high current caps reduce efficiency

At −1.0 V in S0/E0, batches 4–6 show that longer and/or larger charge opportunity increases conversion and yield:

- Batch 4, 100 mA cap for 1800 s: conversion 0.0145, yield 0.0121.
- Batch 5, 500 mA cap for 3600 s: conversion 0.0765, yield 0.0543.
- Batch 6, 250 mA cap for 7200 s: conversion 0.1428, yield 0.0976.

However, the 500 mA condition had much poorer FE, transport, ohmic, and energy efficiencies than the 250 mA long-duration condition. In particular, transport efficiency was 0.157 in batch 5 versus 0.301 in batch 6, and ohmic efficiency was 0.891 versus 0.947. This suggests concentration polarization and resistance become more important as the requested current rises.

The set current is a cap, not a measurement of delivered current. I therefore would not predict conversion from nominal I×t alone. A mechanistic approximation is

I_eff = I_cap × h_transport(I_cap,V,S,E,X) × h_ohmic(I_cap,V,S,E),

Q_productive(t) = ∫ FE(V,I,S,E,X) I_eff dt,

X(t) ≈ 1 − exp[−k(S,E,V) Q_productive/(nF N0)],

where N0 is initial reactant amount and F is Faraday's constant. At the low conversions studied, the exponential may look approximately linear in productive charge. As conversion rises, depletion, mass transfer, or degradation should produce saturation, but the campaign did not reach a high enough conversion to identify that regime.

A simpler empirical predictor consistent with the evidence would be

logit(X) = a + fV(V) + fI(I_cap) + ft(log t) + solvent effect + electrolyte effect + interactions,

with fV nonmonotone, ft increasing and saturating, and fI containing both a throughput benefit and an efficiency penalty.

Crucially, cap and duration were changed together across batches 4–6. The experiments establish a throughput–efficiency tradeoff but do not separately identify a time rate constant or a current exponent.

## 4. Yield is primarily conversion multiplied by selectivity

A natural material-balance relationship is

Y_P ≈ X × S_P,

where X is electrochemical conversion and S_P is selectivity to target product. Several assays are broadly consistent with this after allowing for independent noise. For example, batch 7 gives 0.1738×0.6127 ≈ 0.1065, close to measured yield 0.1078. Batch 6 gives approximately 0.0892 versus measured 0.0976. Deviations are expected because conversion, selectivity, and yield are independently noisy synthetic channels; discrepancies near the detection limit are especially prominent in batches 2–4.

The solvent and electrolyte can therefore improve yield by changing either conversion, selectivity, or both. They need not act directly on the product channel.

## 5. Solvent affects transport, faradaic behavior, selectivity, and safety

Batches 6–9 held E0, −1.0 V, 250 mA, and 7200 s fixed while changing solvent. S1 was the best observed medium: relative to S0 it raised conversion from 0.1428 to 0.1738, yield from 0.0976 to 0.1078, FE from 0.3257 to 0.3526, transport efficiency from 0.3010 to 0.3560, energy efficiency from 0.1909 to 0.2767, and score from 0.3107 to 0.3380.

S2 and S3 were less effective. S2 notably lowered selectivity to 0.4778 and yield to 0.0471. S3 had FE 0.2051 and transport efficiency 0.2259. Their observed safety risks were also higher: approximately 0.114 for S2 and 0.126 for S3, compared with approximately 0.096 for S1 and 0.072 for S0 under the preparation conditions.

I interpret the solvent effects as changes in reactant availability, ion transport, interfacial kinetics, and possibly stabilization of productive versus side-reaction intermediates. The evidence supports a real disadvantage of S2/S3 relative to S1 in this protocol. The smaller S1–S0 difference is less certain because there were no repeats and several channel differences are comparable to one or two stated noise scales.

Because every solvent comparison used E0, solvent–electrolyte interactions are unidentifiable. It is plausible, for example, that E2 behaves differently in S0 than in S1.

## 6. Electrolyte controls a coupled pH/precipitation state

Batches 7 and 10–12 changed electrolyte at fixed S1, −1.0 V, 250 mA, and 7200 s. The largest electrolyte effect was not on conversion but on normalized pH and precipitation:

- E0: pH 0.234, precipitation 0.978.
- E1: pH 0.202, precipitation 0.719.
- E2: pH 0.155, precipitation 0.005.
- E3: pH 0.277, precipitation 0.000.

Thus E2 and E3 almost completely suppressed the precipitation signature, while E0 produced nearly maximal precipitation. E1 was intermediate. This difference is vastly larger than assay noise and is the strongest material-dependent secondary-state effect.

Precipitation is not a simple monotone function of normalized pH: both the lowest-pH electrolyte E2 and the highest-pH electrolyte E3 suppressed it. A more plausible process is electrolyte-specific solubility, complexation, or ion-pairing, with pH as one coupled variable rather than the sole cause. Schematically,

precipitation = H(activity of precipitating species − Ksp_eff(S,E,pH)),

where both species activity and effective solubility depend on electrolyte identity.

The primary reaction was less sensitive. E0 and E1 had nearly tied scores, 0.3380 and 0.3371, and similar conversion, selectivity, FE, and transport efficiency. E2 and E3 were somewhat lower overall but still productive. Consequently, precipitation is not required for product formation: batches 11 and 12 had essentially zero precipitation yet yields of 0.0872 and 0.0916. Conversely, the data do not show whether precipitation harms transport, is merely a spectator state, or removes a side product. This could only be resolved by controlled electrolyte comparisons with time courses or direct phase characterization.

E1/E2 increased measured energy efficiency to about 0.333, but their ohmic efficiencies were lower than E0. This reinforces that energy efficiency is a composite outcome, not synonymous with ohmic efficiency.

## 7. A compact process model

My preferred causal structure is:

1. Solvent and electrolyte establish conductivity, solvation, interfacial environment, normalized pH, and solubility state.
2. Negative potential activates electron transfer to reactant; positive potential does not produce the target.
3. Excessive negative overpotential partitions more current into parasitic pathways, lowering FE and selectivity.
4. The current cap and medium determine actual interfacial current. At high cap, transport polarization and ohmic loss reduce useful current.
5. Productive charge converts reactant. Conversion grows with time/charge and should eventually saturate.
6. A branching step divides converted material between target and unobserved side products; this determines selectivity.
7. Electrolyte-dependent acid/base or solubility equilibria control precipitation, partially independently of the productive branch.

One possible pseudocode representation is:

medium = properties(solvent, electrolyte)
pH_state = acid_base_equilibrium(medium, reaction_progress)
precip = solubility_switch(medium, pH_state, reaction_progress)
activation = cathodic_window(potential)
I_actual = min(I_cap, kinetic_current(activation, medium), mass_transfer_limit(medium, conversion))
FE = productive_fraction(potential, I_actual, medium)
dX_dt = FE * I_actual/(n*F*N0) * remaining_reactant_factor(X)
selectivity = branch_fraction(potential, medium, I_actual, pH_state)
yield = conversion * selectivity
energy_efficiency = function(FE, transport_efficiency, ohmic_efficiency, potential)

This is an explanatory scaffold rather than an identified equation. The campaign establishes the signs and qualitative shapes of several terms but not their unique functional forms.

## Scope and uncertainty

The account is limited to the tested 0.50 mol L⁻¹ nominal starting composition, potentials from +1.5 to −2.0 V, current caps of 100–500 mA, and electrolysis durations of 600–7200 s. It should not be assumed valid at different reagent loading, solvent volume, temperature, or much longer duration.

No batch was exactly repeated. Therefore, small differences—especially the score difference between batches 7 and 10—cannot establish a reproducible ranking. Final-assay standard deviations were approximately 0.010 for conversion and yield, 0.012 for selectivity and FE, 0.014 for transport, 0.012 for ohmic efficiency, 0.016 for energy efficiency, 0.002 for normalized pH, and 0.006 for precipitation. Independent channel noise also explains some internal mass-balance inconsistencies.

The following factors remain unidentifiable:

- actual current and delivered charge versus the configured current cap;
- electron stoichiometry n;
- kinetic rate constants and reaction order;
- exact cathodic onset and optimal potential;
- whether high-cap losses are primarily transport, electrode kinetics, or resistance;
- identities and amounts of side products;
- whether precipitation contains product, reactant, electrolyte, or an impurity;
- causal direction between pH, precipitation, and efficiency;
- solvent–electrolyte interactions outside S1/E0 slices;
- depletion or degradation behavior at high conversion;
- reproducibility and process variability.

## Plausible alternatives

The decline at −2.0 V could reflect a potential-specific side reaction, a change in electrode surface state, or measurement masking rather than a smooth overpotential penalty. The high-current result could arise from a cap-dependent hidden control rule instead of physical concentration polarization. Precipitation might be a benign electrolyte salt rather than a reaction intermediate or product. Solvent effects might operate mainly through conductivity or mainly through chemical selectivity; the available efficiency channels do not uniquely distinguish these explanations.

## Overall conclusion

The most defensible account is a cathodic, charge-driven conversion with a finite productive potential window and a throughput–efficiency tradeoff. Moderate negative potential around −1.0 V was superior to either positive potential or −2.0 V. Longer operation increased conversion, while an excessive current cap reduced transport, faradaic, ohmic, and energy efficiency. S1 supported the best observed balance, and electrolyte mainly controlled a strongly coupled pH/precipitation state while exerting more modest effects on productivity. Batch 7 supplied the strongest observed product outcome, but batch 10 was essentially tied in aggregate score and demonstrated that much lower precipitation can coexist with comparable electrochemical performance.

## K2 封存报告

1. **Supported, contradicted, and untested claims**

No instance-specific prior, nominal material dossier, or supplied mechanistic law was provided. The only material information was a set of anonymous solvent and electrolyte labels. The claims below were therefore self-developed from the campaign.

- **Supported: productive conversion is cathodic/sign-gated.** Batch 1 at +1.5 V, 100 mA, 600 s had zero selective yield and essentially zero useful transport/energy response. Batch 2, differing primarily by using −1.5 V, showed selective yield 0.0117, selectivity 0.560, FE 0.314, and transport efficiency 0.340. This was the first major change in judgment: after batch 1, a generally unreactive system remained plausible; batch 2 instead indicated that potential direction was decisive.
- **Contradicted: more negative potential is always better.** At matched 100 mA and 1800 s, batch 4 at −1.0 V outperformed batch 3 at −2.0 V in selectivity, FE, transport efficiency, energy efficiency, yield, and score. This changed the account from a simple cathodic-threshold law to a finite productive potential window with an excessive-overpotential penalty.
- **Supported qualitatively but not fully identified: extent increases with electrolysis opportunity, while high current caps impose efficiency losses.** Across batches 4–6, conversion and yield increased as duration/current opportunity increased. However, batch 5 at 500 mA had much lower FE, transport, ohmic, and energy efficiencies than batch 6 at 250 mA. These observations motivated a productive-charge model in which actual current is limited by transport and resistance. Because current and duration were changed together, the separate current and time laws remain untested.
- **Supported approximately: selective yield behaves like conversion multiplied by selectivity.** Batch 7 gave conversion × selectivity ≈ 0.1065 versus measured yield 0.1078. Other batches were broadly consistent within independent channel noise, although low-signal batches 2–4 showed larger apparent inconsistencies.
- **Supported: solvent changes both productivity and electrochemical efficiency.** In the matched solvent comparison of batches 6–9, S1/E0 in batch 7 gave the highest observed yield and score, while S2 in batch 8 strongly reduced selectivity and S3 in batch 9 reduced FE and transport efficiency. The S1 advantage over S2/S3 was persuasive; its smaller advantage over S0 was not replicated and is less certain.
- **Supported: electrolyte strongly controls a pH/precipitation state.** At common S1 operating conditions, precipitation changed from 0.978 with E0 in batch 7 to 0.719 with E1 in batch 10, 0.005 with E2 in batch 11, and zero with E3 in batch 12. Because both low-pH E2 and high-pH E3 suppressed precipitation, a simple monotone pH-only precipitation law was contradicted. Electrolyte-specific solubility, complexation, or ion pairing became the preferred explanation.
- **Contradicted: precipitation is required for target formation.** Batches 11 and 12 retained yields of 0.0872 and 0.0916 with essentially no precipitation.
- **Untested:** the electron stoichiometry, exact cathodic onset, precise optimum potential, reaction order, actual delivered current, identities of side products and precipitate, behavior near depletion, long-time degradation, and most solvent–electrolyte interactions. No exact repeat was performed, so reproducibility and small rankings—especially batch 7 versus batch 10—remain untested.

2. **One additional discriminating experiment**

I would run S0/E0 with the original 0.020 mol reagent and 0.040 L solvent at −1.0 V, a 100 mA cap, and 7200 s, followed by the final assay. This fills the most important missing cell relative to batches 4–6.

The leading explanation is that useful extent depends on productive delivered charge, so lowering the cap from batch 6's 250 mA to 100 mA should reduce conversion/yield, while improving or preserving FE, transport, ohmic, and energy efficiencies. A plausible alternative is that the current cap was largely nonbinding and potential plus duration controlled the rate; the similar conversion-per-time seen in batches 5 and 6 leaves that possibility open.

- **Lower yield than batch 6, accompanied by higher FE/transport efficiency:** would strengthen the productive-charge and current-dependent transport-loss account.
- **Yield close to batch 6 despite the 2.5-fold lower cap, with similarly high efficiencies:** would favor the alternative that the cell is potential-limited and the configured cap does not determine actual current over this range.
- **Low yield and unexpectedly low efficiencies even at 100 mA:** would weaken both simple accounts and raise time-dependent deactivation, precipitation-mediated transport, or batch variability as leading explanations.
- **Yield greater than batch 6:** would suggest a genuine intermediate-current optimum or severe parasitic chemistry at 250 mA, rather than merely a monotone throughput–efficiency tradeoff.

A single final assay would still not reveal actual current, but this missing factorial comparison would materially separate the competing interpretations.

3. **Unused evidence, weak predictions, and effect of the goal**

The mechanism used the processed final-assay channels and selected intermediate UV–vis/pH results. It did not quantitatively fit the full raw spectra, peak shapes, peak areas, baselines, or cross-instrument calibration packets. Temperature changes, detailed cost records, and most process-risk accumulation were also not incorporated into the kinetic account. Safety differences among solvents were noted, but safety was not modeled mechanistically. Intermediate UV–vis readings were used mainly as qualitative confirmation because they were noisier than final assays and were not collected as a consistent within-batch time series.

The least reliable blind predictions are those requiring multiple extrapolations: the 500 mA/7200 s negative-potential case, because cap and duration were confounded in the campaign; the S0/E1 and S0/E3 combinations, because those electrolytes were only tested with S1; and every −0.8 V prediction, because −0.8 V was not directly tested. Long positive-potential predictions are also less secure than the point estimates imply: the sign contrast was strong, but only one positive-potential batch was run, at +1.5 V for 600 s. The recommendation of batch 7 over batch 10 is weak as a strict ranking because their scores were nearly tied and neither condition was repeated.

The assigned explanatory goal materially affected evidence collection. It encouraged broad contrasts across sign, potential magnitude, current/time, all solvents, and all electrolytes, and it motivated intermediate measurements rather than repeatedly optimizing the public score. The cost was limited replication and an incomplete factorial design, which reduced precision and left interactions unresolved. There was no clear conflict with the operating objective—batch 7 was also the highest observed score—but a score-first campaign would likely have repeated and locally refined batches 7 and 10 instead of spending later batches on broader electrolyte contrasts.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.42,
        "upper80": 0.75
      },
      "energy_efficiency": {
        "estimate": 0.25,
        "lower80": 0.14,
        "upper80": 0.36
      },
      "faradaic_efficiency": {
        "estimate": 0.45,
        "lower80": 0.31,
        "upper80": 0.58
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.11,
        "lower80": 0.0,
        "upper80": 0.24
      },
      "selective_product_yield": {
        "estimate": 0.007,
        "lower80": 0.0,
        "upper80": 0.025
      },
      "transport_efficiency": {
        "estimate": 0.41,
        "lower80": 0.28,
        "upper80": 0.53
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "energy_efficiency": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.035
      },
      "faradaic_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.055
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.035
      },
      "selective_product_yield": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.012
      },
      "transport_efficiency": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.05
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.51,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.28,
        "lower80": 0.18,
        "upper80": 0.39
      },
      "faradaic_efficiency": {
        "estimate": 0.44,
        "lower80": 0.33,
        "upper80": 0.56
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.34,
        "lower80": 0.26,
        "upper80": 0.43
      },
      "selective_product_yield": {
        "estimate": 0.078,
        "lower80": 0.037,
        "upper80": 0.13
      },
      "transport_efficiency": {
        "estimate": 0.4,
        "lower80": 0.29,
        "upper80": 0.51
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
        "upper80": 0.04
      },
      "faradaic_efficiency": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.045
      },
      "selective_product_yield": {
        "estimate": 0.0,
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
        "estimate": 0.61,
        "lower80": 0.48,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.34,
        "lower80": 0.22,
        "upper80": 0.47
      },
      "faradaic_efficiency": {
        "estimate": 0.44,
        "lower80": 0.31,
        "upper80": 0.57
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.34,
        "lower80": 0.25,
        "upper80": 0.43
      },
      "selective_product_yield": {
        "estimate": 0.068,
        "lower80": 0.025,
        "upper80": 0.13
      },
      "transport_efficiency": {
        "estimate": 0.4,
        "lower80": 0.27,
        "upper80": 0.53
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "energy_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.045
      },
      "faradaic_efficiency": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.045
      },
      "selective_product_yield": {
        "estimate": 0.0,
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
        "estimate": 0.55,
        "lower80": 0.41,
        "upper80": 0.68
      },
      "energy_efficiency": {
        "estimate": 0.29,
        "lower80": 0.17,
        "upper80": 0.42
      },
      "faradaic_efficiency": {
        "estimate": 0.35,
        "lower80": 0.22,
        "upper80": 0.49
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.3,
        "lower80": 0.21,
        "upper80": 0.39
      },
      "selective_product_yield": {
        "estimate": 0.052,
        "lower80": 0.016,
        "upper80": 0.11
      },
      "transport_efficiency": {
        "estimate": 0.34,
        "lower80": 0.21,
        "upper80": 0.48
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "energy_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.045
      },
      "faradaic_efficiency": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.045
      },
      "selective_product_yield": {
        "estimate": 0.0,
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
        "estimate": 0.48,
        "lower80": 0.34,
        "upper80": 0.62
      },
      "energy_efficiency": {
        "estimate": 0.3,
        "lower80": 0.18,
        "upper80": 0.43
      },
      "faradaic_efficiency": {
        "estimate": 0.42,
        "lower80": 0.29,
        "upper80": 0.55
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.3,
        "lower80": 0.2,
        "upper80": 0.39
      },
      "selective_product_yield": {
        "estimate": 0.045,
        "lower80": 0.012,
        "upper80": 0.092
      },
      "transport_efficiency": {
        "estimate": 0.39,
        "lower80": 0.26,
        "upper80": 0.52
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "energy_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.045
      },
      "faradaic_efficiency": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.045
      },
      "selective_product_yield": {
        "estimate": 0.0,
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
        "estimate": 0.63,
        "lower80": 0.51,
        "upper80": 0.73
      },
      "energy_efficiency": {
        "estimate": 0.09,
        "lower80": 0.025,
        "upper80": 0.18
      },
      "faradaic_efficiency": {
        "estimate": 0.18,
        "lower80": 0.09,
        "upper80": 0.29
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.28,
        "lower80": 0.19,
        "upper80": 0.38
      },
      "selective_product_yield": {
        "estimate": 0.145,
        "lower80": 0.07,
        "upper80": 0.24
      },
      "transport_efficiency": {
        "estimate": 0.17,
        "lower80": 0.08,
        "upper80": 0.28
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
        "upper80": 0.035
      },
      "faradaic_efficiency": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "selective_product_yield": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.012
      },
      "transport_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.05
      }
    }
  ],
  "rationale": "The campaign showed a strong potential-sign gate: positive potential produced essentially no target or useful electrochemical efficiencies, whereas moderate negative potential was productive. For negative-potential cases I interpolated from the −1.0 V results, scaled reaction extent for the slightly lower concentration and electrolysis opportunity, and applied observed electrolyte, solvent, and current-cap effects. E1 was treated as raising energy efficiency with little change in transport or FE; E3 as moderately reducing productivity; S2 as primarily reducing selectivity; and a 500 mA cap as increasing extent while sharply penalizing FE, transport, and energy efficiency. Intervals include assay noise plus substantial model uncertainty from the untested −0.8 V point, absence of exact repeats, confounded current-duration effects, and unmeasured delivered current."
}
```
