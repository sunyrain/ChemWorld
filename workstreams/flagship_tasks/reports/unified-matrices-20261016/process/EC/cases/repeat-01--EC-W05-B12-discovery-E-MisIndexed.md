# repeat-01/EC-W05-B12-discovery-E-MisIndexed

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-01\EC-W05-B12-discovery-E-MisIndexed\participant\discovery-E-MisIndexed

## 同期笔记

### v1 · 公开事件 0

# Electrochemical hypothesis notebook

## H1 [tentative]
At fixed 0.50 mol/L loading, signed potential should control productive conversion asymmetrically: one sign will outperform the other, conversion will rise with duration and magnitude before selectivity/energy penalties appear. A current cap may become binding at sufficiently large overpotential.

## H2 [tentative]
Material effects should separate transport and ohmic behavior: higher nominal conductivity should improve ohmic efficiency, whereas diffusion-layer thickness and diffusivity should affect transport efficiency. These priors may be overridden by fixed world residuals.

## H3 [tentative]
Precipitation and acidity may confound apparent performance. Electrolyte E0 is predicted to show more precipitation propensity than E3 from nominal salt/Ksp information; pH and UV-vis snapshots will be used as diagnostics.

Planned tests: sign and potential magnitude comparisons, duration and current-cap contrasts, four solvent/electrolyte combinations, and at least one replicate or segmented-potential test. Differences will remain unresolved unless larger than stated noise and coherent across related observables.

### v2 · 公开事件 56

# Electrochemical hypothesis notebook

## H1 [supported in tested S0/E0 scope]
Potential response is sign-asymmetric. At +1 V the final assay showed high selectivity/efficiency but only 0.0011 selective yield (event runner-operation-0007); at -1 V yield was 0.0130 despite lower efficiencies (runner-operation-0014). Within negative potentials, -1 V exceeded -0.5 and -1.5 V in selective yield (events runner-operation-0021, -0028), consistent with a finite kinetic window rather than monotonic magnitude response. Differences near the low-yield boundary are noisy, so the precise optimum remains unresolved.

## H2 [supported in tested S0/E0 scope]
At -1 V and 100 mA cap, longer electrolysis increased final conversion/yield: 60 s gave 0.0041/0.0089, 600 s 0/0.0130, and 1800 s 0.0211/0.0224 (events runner-operation-0035, -0014, -0042). The 600 s conversion estimate is clipped/noisy, but the yield ordering supports time accumulation. Testable consequence: still longer operation should raise yield until substrate depletion or degradation.

## H3 [revised]
Current cap is not simply beneficial when raised. At -1 V, 500 mA cap depressed faradaic/transport/ohmic metrics and selective yield to the assay floor versus 20 or 100 mA (events runner-operation-0056, -0049, -0014), suggesting high delivered current induces transport/ohmic loss. Whether 20 and 100 mA differ is unresolved at current noise.

## H4 [supported for E0]
Precipitation is essentially saturated (~0.98–1.00) across the S0/E0 series, making E0 a strong precipitation confound. Material comparisons will test whether lower nominal precipitation propensity improves yield and efficiencies.

Next decision: compare matched S1/E1, S2/E2, and S3/E3 at -1 V, 100 mA, 1800 s, then use the last batch to replicate or probe the most informative material result.

### v3 · 公开事件 84

# Electrochemical hypothesis notebook

## H1 [supported in S0/E0 scope; quantitative optimum unresolved]
Potential response is sign-asymmetric and non-monotone. At 600 s, +1 V gave high selectivity/efficiency but only 0.0011 selective yield (runner-operation-0007), whereas -1 V gave 0.0130 (runner-operation-0014). Negative-potential comparisons (-0.5, -1.0, -1.5 V; runner-operation-0021, -0014, -0028) favor a window near -1 V, but assay noise is large relative to these small yields. A mechanistic account should separate charge-transfer direction from efficiency: positive bias appears efficient yet unproductive for the target.

## H2 [supported in tested S0/E0 range]
At -1 V and 100 mA cap, product accumulation increases with time. Final selective yields at 60, 600, 1800, and 7200 s were 0.0089, 0.0130, 0.0224, and 0.0591 (runner-operation-0035, -0014, -0042, -0084); 7200 s also raised conversion to 0.0595. This is approximately an intercept plus near-linear growth over the tested range, though the short-time intercept is likely measurement/background noise. No depletion plateau was observed.

## H3 [supported qualitatively]
At -1 V and 600 s, a 500 mA cap depressed faradaic, transport, and ohmic efficiencies and drove selective yield to the assay floor compared with 20 or 100 mA (runner-operation-0056 versus -0049 and -0014). Thus the cap is only an upper bound: high caps permit a transport/ohmic-loss regime, while evidence distinguishing 20 from 100 mA is weak.

## H4 [material dependence supported; causal decomposition unresolved]
Matched solvent/electrolyte pairs at -1 V, 100 mA, 1800 s differed strongly in precipitation and pH. S0/E0 remained precipitation-saturated (~1; runner-operation-0042), S1/E1 was intermediate (0.731; -0063), and S2/E2 and S3/E3 were near zero (-0070, -0077), agreeing directionally with the nominal precipitation prior. However lower precipitation did not guarantee higher selective yield: yields were 0.0224, 0.0234, 0.0042, and 0.0071, respectively. Solvent and electrolyte were changed together, so their individual effects and hidden residuals remain unresolved. S0/E0 and S1/E1 appear best among tested pairs for target yield; S0/E0 has higher selectivity/efficiency, while S1/E1 reduces precipitation.

## Predictive working model and limits
Within the studied 0.50 mol/L loading, use a signed-potential window centered roughly at -1 V; scale conversion/yield upward with elapsed charge/time until an unobserved saturation point; penalize very high current caps through falling transport and faradaic efficiencies. Treat material-pair corrections as empirical rather than derivable solely from nominal conductivity. Positive bias should remain low-yield even if efficiency channels are high. Extrapolation beyond 7200 s, unpaired solvent/electrolyte combinations, and exact current delivery are unresolved.

## Recommendation decision
Batch 12 is the operating recommendation because it has the largest selective yield and conversion observed, the highest observed score (narrowly), moderate faradaic/transport efficiency, low safety risk, and directly demonstrates the long-duration trend. This recommendation would change if throughput or precipitation avoidance were prioritized over per-batch target yield.

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
      "potential_V": -0.5
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
    "cost": 0.2757200002670288,
    "electrochemical_conversion": 0.0023671130184084177,
    "electrochemical_selectivity": 0.6956106424331665,
    "energy_efficiency": 0.6592008471488953,
    "faradaic_efficiency": 0.4818178415298462,
    "ohmic_efficiency": 0.9251751899719238,
    "pH_normalized": 0.231104776263237,
    "precipitation_signal": 0.9869203567504883,
    "safety_risk": 0.072194404900074,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.49837473034858704
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
    "electrochemical_conversion": 0.00126677006483078,
    "electrochemical_selectivity": 0.5373783707618713,
    "energy_efficiency": 0.10247080773115158,
    "faradaic_efficiency": 0.3531084358692169,
    "ohmic_efficiency": 0.9781976342201233,
    "pH_normalized": 0.23041419684886932,
    "precipitation_signal": 0.9876685738563538,
    "safety_risk": 0.072194404900074,
    "score": 0.04560511186718941,
    "selective_product_yield": 0.0036485616583377123,
    "transport_efficiency": 0.3216208815574646
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
      "duration_s": 60,
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
    "cost": 0.27562400698661804,
    "electrochemical_conversion": 0.004081509076058865,
    "electrochemical_selectivity": 0.6398956179618835,
    "energy_efficiency": 0.27024927735328674,
    "faradaic_efficiency": 0.4178524315357208,
    "ohmic_efficiency": 0.9674157500267029,
    "pH_normalized": 0.23537498712539673,
    "precipitation_signal": 0.9869949817657471,
    "safety_risk": 0.072194404900074,
    "score": 0.1364751160144806,
    "selective_product_yield": 0.008866063319146633,
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
    "electrochemical_conversion": 0.021125322207808495,
    "electrochemical_selectivity": 0.637702226638794,
    "energy_efficiency": 0.29284948110580444,
    "faradaic_efficiency": 0.43088415265083313,
    "ohmic_efficiency": 0.9692724943161011,
    "pH_normalized": 0.2320990413427353,
    "precipitation_signal": 0.9976252913475037,
    "safety_risk": 0.072194404900074,
    "score": 0.3182702362537384,
    "selective_product_yield": 0.022356536239385605,
    "transport_efficiency": 0.4062007963657379
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
    "cost": 0.2826479971408844,
    "electrochemical_conversion": 0.011604281142354012,
    "electrochemical_selectivity": 0.627807080745697,
    "energy_efficiency": 0.2933078408241272,
    "faradaic_efficiency": 0.4045216143131256,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.23111364245414734,
    "precipitation_signal": 0.9826673865318298,
    "safety_risk": 0.072194404900074,
    "score": 0.12568426132202148,
    "selective_product_yield": 0.00808033999055624,
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
    "cost": 0.2768000066280365,
    "electrochemical_conversion": 0.010483215562999249,
    "electrochemical_selectivity": 0.6456847786903381,
    "energy_efficiency": 0.14559002220630646,
    "faradaic_efficiency": 0.207375630736351,
    "ohmic_efficiency": 0.8635371923446655,
    "pH_normalized": 0.229416161775589,
    "precipitation_signal": 0.995540201663971,
    "safety_risk": 0.072194404900074,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.2008802741765976
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
    "cost": 0.2993200123310089,
    "electrochemical_conversion": 0.011325862258672714,
    "electrochemical_selectivity": 0.4579375088214874,
    "energy_efficiency": 0.22556422650814056,
    "faradaic_efficiency": 0.2749573588371277,
    "ohmic_efficiency": 0.9674895405769348,
    "pH_normalized": 0.20476384460926056,
    "precipitation_signal": 0.7306620478630066,
    "safety_risk": 0.09559440612792969,
    "score": 0.25065210461616516,
    "selective_product_yield": 0.023404473438858986,
    "transport_efficiency": 0.29578864574432373
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
      "potential_V": -1
    },
    {
      "duration_s": 1800,
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
    "cost": 0.3179199993610382,
    "electrochemical_conversion": 0.02921551838517189,
    "electrochemical_selectivity": 0.5003582835197449,
    "energy_efficiency": 0.26203757524490356,
    "faradaic_efficiency": 0.30589261651039124,
    "ohmic_efficiency": 0.9107071161270142,
    "pH_normalized": 0.16965022683143616,
    "precipitation_signal": 0.0,
    "safety_risk": 0.1135944053530693,
    "score": 0.05469724163413048,
    "selective_product_yield": 0.00422638887539506,
    "transport_efficiency": 0.30724218487739563
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
    "cost": 0.3089199960231781,
    "electrochemical_conversion": 0.025363700464367867,
    "electrochemical_selectivity": 0.45748573541641235,
    "energy_efficiency": 0.22406016290187836,
    "faradaic_efficiency": 0.2576015889644623,
    "ohmic_efficiency": 0.9700570106506348,
    "pH_normalized": 0.2838256359100342,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.12619440257549286,
    "score": 0.0864548310637474,
    "selective_product_yield": 0.007147760130465031,
    "transport_efficiency": 0.26478150486946106
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
    "cost": 0.28547999262809753,
    "electrochemical_conversion": 0.05948854237794876,
    "electrochemical_selectivity": 0.6161341667175293,
    "energy_efficiency": 0.2895949184894562,
    "faradaic_efficiency": 0.37271592020988464,
    "ohmic_efficiency": 0.985348641872406,
    "pH_normalized": 0.23062115907669067,
    "precipitation_signal": 0.9938013553619385,
    "safety_risk": 0.072194404900074,
    "score": 0.3224959671497345,
    "selective_product_yield": 0.05913284420967102,
    "transport_efficiency": 0.39394086599349976
  }
}
```

## K1 封存报告

Mechanistic account

1. Experimental domain and main observations

All twelve batches used 0.020 mol reagent in 0.040 L solvent, so the tested initial loading was 0.50 mol/L. The manipulated variables were potential, current cap, electrolysis time, solvent, and electrolyte profile. Final-assay values are noisy channel-specific estimates rather than exact stoichiometric identities: for example, batch 1 reported conversion 0.0234, selectivity 0.9985, but selective-product yield only 0.00110; batch 2 reported conversion clipped to 0 while yield was 0.01299. I therefore do not impose yield = conversion × selectivity on individual reported values, especially near zero.

The central empirical pattern is that target formation favors negative potential, particularly a window near -1 V, and accumulates with electrolysis time. A positive potential can give high electrical-efficiency readouts without producing much target. Very high permitted current degrades transport and faradaic behavior. Solvent/electrolyte choice strongly changes precipitation, pH, and the partition between conversion and desired-product yield.

2. Proposed process model

I interpret the system as an electrode-driven conversion with at least three competing charge pathways:

• productive electron transfer from reactant to target;
• nonproductive or side-product electron transfer;
• capacitive, ohmic, or otherwise unproductive current.

A useful conceptual model is

eta = V_applied - E_effective(materials, pH, hidden residuals) - iR,

i = min(I_cap, i_kinetic(eta), i_transport),

r_target = i × FE(eta, materials, i) × S_target(eta, materials, time) / (nF),

where eta is effective overpotential, I_cap is the configured current ceiling, FE is faradaic efficiency, and S_target is the fraction of faradaic conversion reaching the target. The actual delivered current, electron number n, electrode area, and resistance were not observed, so this is a structural explanation rather than an identified electrochemical law.

At low conversion, accumulated target should be approximately proportional to productive charge:

Y_target(t) ≈ Y_background + k_productive t.

A simple descriptive least-squares fit to the S0/E0, -1 V, 100 mA-cap series at 60, 600, 1800, and 7200 s gives

Y_target ≈ 0.00893 + 7.00×10^-6 t,

with t in seconds. The nonzero intercept is best regarded as assay/background scatter, not instantaneous chemical production. A corresponding descriptive fit to reported conversion is approximately

X ≈ 0.00147 + 8.16×10^-6 t.

These equations summarize only the measured interval; they should eventually bend toward a saturation or degradation limit. No plateau was observed by 7200 s.

3. Potential dependence

Batch 1 (+1 V, 100 mA, 600 s, S0/E0) had very high selectivity and efficiency readouts—selectivity 0.9985, faradaic efficiency 1.000, transport efficiency 0.9858, ohmic efficiency 0.9602, and energy efficiency 0.9631—but selective-product yield was only 0.00110. Batch 2, with the potential reversed to -1 V and otherwise matched, gave yield 0.01299 despite lower faradaic, transport, and energy efficiencies of 0.4067, 0.4329, and 0.2849. Thus positive bias appears electrically well behaved but points charge into a pathway that does not accumulate the assayed target, whereas negative bias accesses the productive direction.

The negative-potential series suggests a finite window rather than monotonic improvement with magnitude. At 600 s and 100 mA cap:

• batch 3, -0.5 V: yield 0, conversion 0.00237, selectivity 0.6956;
• batch 2, -1.0 V: yield 0.01299, conversion reported as 0, selectivity 0.6435;
• batch 4, -1.5 V: yield 0.00365, conversion 0.00127, selectivity 0.5374.

The -1 V condition produced the largest measured yield. Moving from -1 to -1.5 V also lowered faradaic efficiency from 0.4067 to 0.3531, transport efficiency from 0.4329 to 0.3216, and energy efficiency from 0.2849 to 0.1025. My explanation is that modest cathodic overpotential activates target formation, while excessive magnitude increasingly drives side reactions or transport-limited current. Because yields were close to the assay floor and no exact replicates were run, the optimum cannot be localized more precisely than a broad region around -1 V.

An alternative is that the apparent optimum is partly produced by independent noise in the conversion and yield channels. Nevertheless, the simultaneous deterioration of several efficiency channels at -1.5 V makes a genuine overpotential penalty plausible.

4. Time dependence

At -1 V, 100 mA cap, and S0/E0, selective-product yield increased with time:

• batch 5, 60 s: 0.00887 yield and 0.00408 conversion;
• batch 2, 600 s: 0.01299 yield and conversion clipped to 0;
• batch 6, 1800 s: 0.02236 yield and 0.02113 conversion;
• batch 12, 7200 s: 0.05913 yield and 0.05949 conversion.

The 600 s conversion value is evidently dominated by near-zero noise, but the yield sequence and the strong 7200 s result support cumulative target formation. Batch 12 had selectivity 0.6161, faradaic efficiency 0.3727, transport efficiency 0.3939, ohmic efficiency 0.9853, and energy efficiency 0.2896. The efficiencies did not improve with duration; rather, longer time integrated a modest productive current into more product. This distinction explains why batch 12 can outperform short, apparently efficient runs in final yield.

No evidence establishes what happens beyond 7200 s. Substrate depletion, product degradation, electrode fouling, or precipitation could eventually make the curve sublinear or turn it downward. Linear extrapolation beyond the observed range is therefore conjectural.

5. Current-cap coupling

At -1 V and 600 s in S0/E0, changing the cap from 20 to 500 mA produced a clear high-current penalty:

• batch 7, 20 mA: yield 0.00808, faradaic efficiency 0.4045, transport efficiency 0.4079, ohmic efficiency 1.000, energy efficiency 0.2933;
• batch 2, 100 mA: yield 0.01299, faradaic efficiency 0.4067, transport efficiency 0.4329, ohmic efficiency 0.9690, energy efficiency 0.2849;
• batch 8, 500 mA: yield clipped to 0, faradaic efficiency 0.2074, transport efficiency 0.2009, ohmic efficiency 0.8635, energy efficiency 0.1456.

The 20 and 100 mA cases are too close, relative to noise and the lack of replication, to establish a useful difference. The 500 mA case, however, simultaneously depressed all major efficiency channels. In the proposed model, the larger cap permits current density to approach or exceed mass-transport capacity; concentration polarization, increased iR loss, and side reactions then consume charge. The current cap is not necessarily the delivered current, so its exact causal effect cannot be converted into a current-response equation.

Plausible alternatives are electrode heating, interfacial degradation, or a potential-control artifact at high allowed current. Those mechanisms cannot be distinguished because actual current, charge, temperature, and electrode state were not measured.

6. Solvent/electrolyte coupling, pH, and precipitation

Batches 6 and 9–11 compared matched solvent/electrolyte pairs at -1 V, 100 mA, and 1800 s:

• batch 6, S0/E0: yield 0.02236, conversion 0.02113, selectivity 0.6377, pH-normalized 0.2321, precipitation 0.9976;
• batch 9, S1/E1: yield 0.02340, conversion 0.01133, selectivity 0.4579, pH-normalized 0.2048, precipitation 0.7307;
• batch 10, S2/E2: yield 0.00423, conversion 0.02922, selectivity 0.5004, pH-normalized 0.1697, precipitation 0;
• batch 11, S3/E3: yield 0.00715, conversion 0.02536, selectivity 0.4575, pH-normalized 0.2838, precipitation 0.00524.

The precipitation ordering agrees qualitatively with the nominal material dossier: E0 had the strongest precipitation propensity, E1 was intermediate, and E2/E3 were much less prone. This supports the interpretation that the precipitation signal reflects a real material-controlled equilibrium rather than merely electrolysis extent.

Precipitation was not the sole determinant of target formation. S0/E0 and S1/E1 gave the highest yields despite substantial precipitation, while the nearly precipitation-free S2/E2 and S3/E3 pairs gave appreciably lower yields. S2/E2 and S3/E3 also showed conversion estimates larger than their target yields, suggesting that these media support reactant consumption but partition more material into undesired products. In contrast, S0/E0 achieved higher reported selectivity, while S1/E1 traded some selectivity and efficiency for lower precipitation and a similar observed yield.

A plausible coupling is

E_effective = E_base + DeltaE_solvent + DeltaE_electrolyte + DeltaE_pH + hidden interaction,

k_transport proportional to D_effective/delta_effective,

R_solution roughly inversely proportional to conductivity_effective,

with precipitation removing some dissolved species or modifying the electrode surface. However, the data do not identify the sign or magnitude of each term. Each solvent was tested only with the same-index electrolyte, so solvent main effects, electrolyte main effects, and their interactions are perfectly confounded. The nominal properties also include fixed but hidden world residuals, and the observed ohmic efficiencies do not form a simple ranking by nominal conductivity alone.

Safety risk also varied with the material pair: approximately 0.0722 for S0/E0, 0.0956 for S1/E1, 0.1136 for S2/E2, and 0.1262 for S3/E3. These are observations, but the experiments do not identify which solvent or electrolyte property caused that ordering.

7. Interpretation of efficiency channels

The data indicate that the efficiency observables describe different bottlenecks and cannot substitute for target yield:

• Faradaic efficiency describes how much current appears chemically productive in a broad sense, but may include non-target chemistry.
• Electrochemical selectivity describes pathway partitioning, although at very low signal it can be inconsistent with the independent yield channel.
• Transport efficiency falls when mass delivery to the interface is inadequate, most clearly at the 500 mA cap.
• Ohmic efficiency is generally high but falls at high permitted current.
• Energy efficiency combines electrical losses and productive chemistry and was highest under +1 V even though target yield was poor.

Thus optimization of energy efficiency alone would select the wrong potential for the target. A mechanistic predictor needs both a direction-dependent target-formation term and separate transport/ohmic penalties.

8. Experiments that changed the explanation

Batch 1 initially suggested a highly efficient system, but its very low yield forced a distinction between electrical efficiency and target productivity. Batch 2 established the potential-sign asymmetry. Batches 3 and 4 changed a simple 'more negative is better' hypothesis into a finite-window hypothesis centered near -1 V. Batches 5, 6, and especially 12 established sustained time accumulation without an observed plateau. Batches 7 and 8 showed that merely increasing the current ceiling is not beneficial and identified a high-current loss regime. Batches 9–11 demonstrated that precipitation follows material choice but does not by itself control target yield; they also exposed strong conversion-to-product partitioning differences among material pairs.

9. Scope and non-identifiability

This account is supported only for 0.50 mol/L initial loading, the tested 0.040 L volume, potentials from -1.5 to +1 V, current caps from 20 to 500 mA, times from 60 to 7200 s, and the four matched material pairs. There were no exact condition replicates. Most yields were small compared with the final-assay noise scale, so fine rankings among low-yield batches are uncertain.

Unidentified quantities include actual current and charge, electrode area and kinetics, electron stoichiometry, uncompensated resistance, mass-transfer coefficient, temperature, individual chemical species, side products, product degradation, and whether precipitation occurs in bulk solution or on the electrode. The separate effects of solvent and electrolyte cannot be recovered from matched-pair tests. Spectral assignments were not used to identify intermediates, and pH was represented only by a normalized channel.

Other explanations remain plausible: precipitation or optical matrix effects could bias assay channels; independent channel noise could generate some yield/conversion inconsistencies; positive potential could destroy target rather than simply fail to form it; and the 500 mA penalty could arise from electrode damage instead of mass transport. The evidence favors, but does not uniquely prove, the productive-cathodic-window plus transport-loss model.

10. Overall working prediction

For conditions near those tested, I would predict target formation by first locating the effective potential relative to a material-dependent cathodic window, then calculating a delivered-current term limited by kinetics, the current cap, mass transport, and ohmic resistance. Productive charge should be multiplied by faradaic and target-selectivity factors, integrated over time, and eventually passed through a saturation/degradation function. Around S0/E0 at -1 V and 100 mA cap, early target yield rises roughly 7×10^-6 per second over 60–7200 s, but that coefficient must not be transferred unchanged to other materials or extrapolated indefinitely. Very positive potential should remain low-yield despite high apparent efficiencies; excessively high current caps should lower faradaic, transport, and energy performance; and low precipitation alone should not be assumed to imply high target yield.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific prior law or expected answer was supplied. The material dossier supplied nominal properties and qualitative mechanistic priors, while explicitly warning that hidden residuals and solvent–electrolyte coupling could override simple rankings.

Supported:
- A finite productive potential window was supported within S0/E0. At 600 s, -1.0 V in batch 2 gave greater measured selective-product yield (0.01299) than -0.5 V in batch 3 (0) or -1.5 V in batch 4 (0.00365). This changed my initial possibility that increasing cathodic magnitude would monotonically improve production.
- Time accumulation at -1 V was supported. Selective yields increased from 0.00887 at 60 s in batch 5, to 0.01299 at 600 s in batch 2, 0.02236 at 1800 s in batch 6, and 0.05913 at 7200 s in batch 12. Batch 12 was the strongest evidence that useful product continued accumulating without an observed plateau.
- A high-current penalty was supported qualitatively. At 500 mA in batch 8, faradaic, transport, ohmic, and energy efficiencies were 0.207, 0.201, 0.864, and 0.146, all worse than the corresponding 20 mA results in batch 7 and 100 mA results in batch 2. This changed my judgment from treating the current setting mainly as a way to accelerate conversion to treating it as a possible transport/side-reaction control.
- The dossier’s qualitative precipitation ordering was supported. Precipitation was about 0.998 for S0/E0 in batch 6, 0.731 for S1/E1 in batch 9, and essentially absent for S2/E2 and S3/E3 in batches 10 and 11.

Contradicted or weakened:
- A simple “more negative potential is better” law was contradicted by batch 4: -1.5 V performed worse than -1 V and had lower faradaic, transport, and energy efficiencies.
- A simple “less precipitation gives more target product” claim was contradicted. Nearly precipitation-free batches 10 and 11 yielded only 0.00423 and 0.00715, whereas precipitation-rich batch 6 yielded 0.02236.
- A simple ranking from nominal conductivity to observed ohmic or target performance was not sustained. Material pairs changed several properties simultaneously, and the observed responses did not follow conductivity alone.
- Treating the reported channels as exact algebraic identities was contradicted by the measurements. Batch 1 reported conversion 0.0234 and selectivity 0.9985 but yield 0.00110; batch 2 reported conversion clipped to zero but yield 0.01299. I consequently treated these as noisy, separately calibrated estimates rather than enforcing yield = conversion × selectivity for each assay.

Partially supported but uncertain:
- The claim that positive bias is electrically efficient but poorly targeted rested mainly on batch 1. Its +1 V condition produced very high efficiency and selectivity readouts but very low measured target yield. Because this was a single low-signal result with no long-duration positive-potential counterpart, it remained much less secure than the time trend at negative potential.
- Differences between 20 and 100 mA were unresolved. Batches 7 and 2 differed numerically, but the values were close relative to assay noise and were not replicated.

Untested:
- Saturation, depletion, fouling, and product degradation beyond 7200 s were untested.
- Solvent main effects, electrolyte main effects, and their interactions were unidentifiable because batches 6 and 9–11 changed solvent and electrolyte together.
- Actual delivered current, charge, electrode temperature, resistance, electrode condition, electron stoichiometry, and side-product identities were unmeasured.
- Whether precipitation occurred in solution or on the electrode, and whether it caused kinetic inhibition or analytical interference, was untested.

2. Best additional discriminating experiment

I would run one long-duration positive-potential experiment matched to batch 12: 0.020 mol reagent in 0.040 L S0, E0 electrolyte, +1.0 V, 100 mA cap, and 7200 s, followed by the final assay.

This would distinguish my leading “cathodic target window” explanation from the important alternative that batch 1’s low yield was an assay fluctuation and positive bias is actually highly productive, as its excellent efficiency and selectivity channels might suggest. Long duration would amplify the difference beyond the final-assay yield noise.

- If the yield remained near the floor or below roughly 0.02 while faradaic, transport, and energy efficiencies stayed high, I would strengthen the conclusion that positive current is efficiently directed toward a non-target process.
- If yield approached or exceeded batch 12’s 0.05913, especially with substantial conversion and high selectivity, I would reject the strong sign-direction claim and reinterpret batch 1’s yield as an anomalously low measurement. The leading model would become a charge-accumulation model in which positive bias may be superior.
- An intermediate yield, or simultaneous collapse of all efficiency channels, would leave the sign mechanism unresolved and suggest duration-dependent depletion, degradation, or electrode-state effects instead.

This single experiment would not resolve solvent/electrolyte effects, but it addresses the largest mechanistic uncertainty created by the campaign.

3. Unused evidence, reliability, and effect of the assigned goal

The raw UV–visible and final-assay artifacts were not inspected peak by peak, so spectral shapes, baselines, assignments, and possible matrix interference were unused. Intermediate UV–visible and pH measurements were used mainly through their processed summaries rather than their full signals. Cost and safety observations were considered for the recommendation but not incorporated into the kinetic explanation except for noting the material-pair safety ordering. The nominal double-layer capacitance, diffusivity, diffusion-layer thickness, acid properties, and potential shifts informed qualitative interpretation but could not be fitted separately with the chosen paired-material design.

The least reliable predictions are the untested solvent/electrolyte crosses in Q05–Q10, the long positive-potential predictions in Q04, Q06, Q08, Q10, and Q12, and both 500 mA long-duration predictions Q11–Q12. Those cases extrapolate across interactions, duration, or current regimes not jointly observed. Score predictions near the 0.02 yield gate are particularly fragile because a small yield error produces a large nonlinear score error. Q01 and Q03 are comparatively better anchored by the S0/E0 negative-potential and duration series, although -0.8 V was still interpolated rather than directly tested.

Batch 12 is a defensible recommendation as the best observed batch: it had the campaign’s largest measured yield and conversion and the highest observed score. It is less reliable as proof of a global optimum because there were no exact replicates, the selected value may benefit from measurement noise, and long positive-potential or crossed-material alternatives were not tested.

The assigned goal emphasized explanatory discovery over public-score optimization. That encouraged potential-sign, magnitude, time, current, and material contrasts rather than repeatedly refining the highest-scoring recipe. This breadth produced useful mechanistic evidence, especially batches 2–8 and 12, but reduced replication and left the material comparison confounded. Using one intermediate measurement in every batch increased coverage of pH and efficiency behavior, although the full spectral information was not exploited. I see no clear conflict between the research goal and the final recommendation, but a score-maximization goal alone would likely have allocated more batches to replication and local optimization around batch 12.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.67,
        "lower80": 0.6,
        "upper80": 0.74
      },
      "energy_efficiency": {
        "estimate": 0.43,
        "lower80": 0.32,
        "upper80": 0.54
      },
      "faradaic_efficiency": {
        "estimate": 0.45,
        "lower80": 0.37,
        "upper80": 0.53
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.156,
        "lower80": 0.0,
        "upper80": 0.39
      },
      "selective_product_yield": {
        "estimate": 0.009,
        "lower80": 0.0,
        "upper80": 0.025
      },
      "transport_efficiency": {
        "estimate": 0.47,
        "lower80": 0.38,
        "upper80": 0.56
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.97,
        "lower80": 0.91,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.9,
        "lower80": 0.8,
        "upper80": 0.98
      },
      "faradaic_efficiency": {
        "estimate": 0.96,
        "lower80": 0.88,
        "upper80": 1.0
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.086,
        "lower80": 0.0,
        "upper80": 0.39
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.018
      },
      "transport_efficiency": {
        "estimate": 0.95,
        "lower80": 0.87,
        "upper80": 1.0
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.64,
        "lower80": 0.56,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.3,
        "lower80": 0.2,
        "upper80": 0.4
      },
      "faradaic_efficiency": {
        "estimate": 0.4,
        "lower80": 0.32,
        "upper80": 0.48
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.34,
        "lower80": 0.18,
        "upper80": 0.49
      },
      "selective_product_yield": {
        "estimate": 0.07,
        "lower80": 0.03,
        "upper80": 0.12
      },
      "transport_efficiency": {
        "estimate": 0.41,
        "lower80": 0.32,
        "upper80": 0.5
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.95,
        "lower80": 0.86,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.82,
        "lower80": 0.68,
        "upper80": 0.94
      },
      "faradaic_efficiency": {
        "estimate": 0.9,
        "lower80": 0.78,
        "upper80": 0.99
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.276,
        "lower80": 0.02,
        "upper80": 0.61
      },
      "selective_product_yield": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.045
      },
      "transport_efficiency": {
        "estimate": 0.88,
        "lower80": 0.75,
        "upper80": 0.98
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.5,
        "lower80": 0.37,
        "upper80": 0.63
      },
      "energy_efficiency": {
        "estimate": 0.22,
        "lower80": 0.1,
        "upper80": 0.36
      },
      "faradaic_efficiency": {
        "estimate": 0.3,
        "lower80": 0.18,
        "upper80": 0.43
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.266,
        "lower80": 0.07,
        "upper80": 0.43
      },
      "selective_product_yield": {
        "estimate": 0.03,
        "lower80": 0.005,
        "upper80": 0.075
      },
      "transport_efficiency": {
        "estimate": 0.32,
        "lower80": 0.18,
        "upper80": 0.46
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.88,
        "lower80": 0.73,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.6,
        "lower80": 0.42,
        "upper80": 0.77
      },
      "faradaic_efficiency": {
        "estimate": 0.7,
        "lower80": 0.52,
        "upper80": 0.85
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.184,
        "lower80": 0.01,
        "upper80": 0.47
      },
      "selective_product_yield": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "transport_efficiency": {
        "estimate": 0.68,
        "lower80": 0.49,
        "upper80": 0.84
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.48,
        "lower80": 0.33,
        "upper80": 0.63
      },
      "energy_efficiency": {
        "estimate": 0.2,
        "lower80": 0.08,
        "upper80": 0.35
      },
      "faradaic_efficiency": {
        "estimate": 0.28,
        "lower80": 0.15,
        "upper80": 0.43
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.254,
        "lower80": 0.06,
        "upper80": 0.43
      },
      "selective_product_yield": {
        "estimate": 0.027,
        "lower80": 0.003,
        "upper80": 0.07
      },
      "transport_efficiency": {
        "estimate": 0.27,
        "lower80": 0.13,
        "upper80": 0.43
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.82,
        "lower80": 0.64,
        "upper80": 0.95
      },
      "energy_efficiency": {
        "estimate": 0.5,
        "lower80": 0.31,
        "upper80": 0.69
      },
      "faradaic_efficiency": {
        "estimate": 0.6,
        "lower80": 0.4,
        "upper80": 0.78
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.123,
        "lower80": 0.0,
        "upper80": 0.41
      },
      "selective_product_yield": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.035
      },
      "transport_efficiency": {
        "estimate": 0.55,
        "lower80": 0.35,
        "upper80": 0.73
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.39,
        "upper80": 0.7
      },
      "energy_efficiency": {
        "estimate": 0.25,
        "lower80": 0.11,
        "upper80": 0.41
      },
      "faradaic_efficiency": {
        "estimate": 0.34,
        "lower80": 0.2,
        "upper80": 0.49
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.287,
        "lower80": 0.08,
        "upper80": 0.46
      },
      "selective_product_yield": {
        "estimate": 0.04,
        "lower80": 0.006,
        "upper80": 0.09
      },
      "transport_efficiency": {
        "estimate": 0.35,
        "lower80": 0.19,
        "upper80": 0.51
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.86,
        "lower80": 0.69,
        "upper80": 0.97
      },
      "energy_efficiency": {
        "estimate": 0.56,
        "lower80": 0.37,
        "upper80": 0.74
      },
      "faradaic_efficiency": {
        "estimate": 0.68,
        "lower80": 0.49,
        "upper80": 0.84
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.177,
        "lower80": 0.01,
        "upper80": 0.46
      },
      "selective_product_yield": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.04
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
        "lower80": 0.48,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.16,
        "lower80": 0.06,
        "upper80": 0.29
      },
      "faradaic_efficiency": {
        "estimate": 0.24,
        "lower80": 0.12,
        "upper80": 0.38
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.252,
        "lower80": 0.03,
        "upper80": 0.42
      },
      "selective_product_yield": {
        "estimate": 0.035,
        "lower80": 0.0,
        "upper80": 0.1
      },
      "transport_efficiency": {
        "estimate": 0.23,
        "lower80": 0.1,
        "upper80": 0.38
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.85,
        "lower80": 0.69,
        "upper80": 0.96
      },
      "energy_efficiency": {
        "estimate": 0.42,
        "lower80": 0.24,
        "upper80": 0.61
      },
      "faradaic_efficiency": {
        "estimate": 0.55,
        "lower80": 0.37,
        "upper80": 0.73
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.097,
        "lower80": 0.0,
        "upper80": 0.37
      },
      "selective_product_yield": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.035
      },
      "transport_efficiency": {
        "estimate": 0.5,
        "lower80": 0.31,
        "upper80": 0.69
      }
    }
  ],
  "rationale": "Predictions use the observed cathodic window near -1 V, approximate time accumulation through 7200 s, and the strong efficiency penalty seen at a 500 mA cap. Positive bias is assigned high electrical efficiencies but low target yield, following batch 1; long-time positive-bias and untested solvent/electrolyte cross-combinations receive wide intervals. Material adjustments reflect the matched-pair results and nominal transport, conductivity, and potential-shift information. Score uncertainty is especially asymmetric when predicted yield is near the 0.02 multiplicative gate."
}
```
