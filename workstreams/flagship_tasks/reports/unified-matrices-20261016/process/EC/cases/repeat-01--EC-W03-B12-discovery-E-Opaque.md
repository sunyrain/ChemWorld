# repeat-01/EC-W03-B12-discovery-E-Opaque

既有科学公开材料；非provider内部推理。

来源：D:\CW267\s01\repeat-01\EC-W03-B12-discovery-E-Opaque\participant\discovery-E-Opaque

## 同期笔记

### v1 · 公开事件 0

# Electrochemical hypothesis notebook

## Pre-experiment expectations

**H1 [tentative].** Product formation depends nonlinearly on signed potential and electrolysis duration: conversion should increase with charge/time until side reactions reduce selectivity and energy efficiency. Both potential signs must be tested because productive polarity is unknown.

**H2 [tentative].** Solvent and electrolyte identities affect transport/ohmic efficiency and may interact with potential rather than acting as simple additive offsets.

**H3 [tentative].** A current cap can become rate-limiting; at fixed potential and loading, increasing the cap should increase short-time conversion until a potential/transport ceiling, while possibly lowering selectivity at extreme drive.

Planned tests: twelve independent, fixed-loading batches spanning both potential signs, short/long durations, all four solvents/electrolytes, and several current caps. Use one intermediate UV-vis or pH observation per batch, then explicit termination and final assay. Interpret numerical differences cautiously against declared assay noise; use replicated/paired conditions where the budget permits.

### v2 · 公开事件 42

# Electrochemical hypothesis notebook

## Pre-experiment expectations
H1: nonlinear signed-potential/time response; H2: solvent/electrolyte interactions; H3: current-cap limitation.

## Interim interpretation (through event runner-operation-0042)

**H1 [supported qualitatively, quantitative form unresolved].** Polarity and drive strongly alter efficiencies. At +1.5 V for 300 s in S0/E0, UV-vis and final assay showed essentially no productive response (events 0005, 0007), whereas the otherwise matched -1.5 V batch showed finite faradaic/transport efficiency and a small selective yield (events 0012, 0014). This supports a signed response, though yield is near the assay noise scale and needs longer-time testing. Extreme +2.25 V at 900 s in S1/E1 was also nearly unproductive (event 0028). A mild +0.75 V, 60 s condition had high efficiency/selectivity but zero resolved yield (event 0021), consistent with insufficient charge rather than necessarily wrong polarity.

**H2 [unresolved].** Material combinations differ substantially in pH/precipitation (S1/E1: about 0.21/0.65; S2/E2: about 0.18/~0; events 0021, 0035), but potential, duration, and polarity are confounded across most comparisons. These medium observables may be stable fingerprints rather than causal performance predictors.

**H3 [unresolved].** No direct cap pair has yet been completed. High ohmic efficiency is common, while transport and faradaic efficiencies collapse at some high positive drives, suggesting kinetic/selectivity loss rather than simple bulk resistance.

**Next predictions recorded before testing.** Extending the productive negative-potential batches should raise conversion/yield initially; excessive duration may reveal degradation or diminishing returns. A paired 5 versus 500 mA cap at identical S3/E3, +1.5 V, 900 s should diagnose cap limitation. Longer mild +0.75 V electrolysis should distinguish slow productive conversion from a polarity-specific dead branch.

### v3 · 公开事件 84

# Electrochemical hypothesis notebook — final source-stage view

All claims apply to 0.020 mol reagent in 0.040 L solvent (nominal 0.50 mol L⁻¹ loading) within the tested anonymous materials.

**H1 [supported in tested scope]. Signed potential and duration jointly govern outcome.** A matched S0/E0 comparison at ±1.5 V, 100 mA, 300 s changed the response from essentially unproductive at positive polarity (event 0007) to finite efficiencies and small yield at negative polarity (event 0014). However polarity is not universally decisive: mild +0.75 V in S1/E1 gave high efficiencies and, after 3600 s, resolved conversion/yield (event 0077). Thus the operative window depends on material/potential, not merely sign.

For S0/E0 at -1.5 V and 100 mA, extending 300→3600→14400 s raised selective yield approximately 0.010→0.030→0.049 and conversion approximately 0→0.025→0.124 (events 0014, 0063, 0070). The first yield increase was about 3-fold and the next only 1.63-fold despite 4-fold more time, supporting diminishing yield returns while conversion continues to accumulate. Noise affects the smallest values, but the long-time trend greatly exceeds the declared final-assay noise.

**H2 [supported as interaction/fingerprint; causal separation incomplete].** S1/E1 maintains pH-normalized ~0.21 and precipitation ~0.65 (events 0021, 0077); S2/E2 maintains ~0.17–0.18 and ~0 (events 0035, 0042, 0084); S0/E0 maintains ~0.23 and precipitation near 1 (events 0007, 0014, 0063, 0070). These repeatable medium fingerprints accompany distinct efficiency regimes. Because solvent and electrolyte were paired rather than fully crossed, their separate contributions remain unidentified.

**H3 [supported for tested S3/E3 condition, direction revised].** At +1.5 V for 900 s, a 5 mA cap gave faradaic/transport efficiencies near 0.80 and selective yield ~0.008 (event 0049), whereas 500 mA gave efficiencies near 0.1 and unresolved yield (event 0056). Increasing the cap therefore did not simply accelerate conversion; it shifted operation into a low-efficiency regime. The current is a cap, so actual delivered charge remains unobserved and a mechanistic distinction between current-limited kinetics and potential-driven side reactions is unresolved.

**Predictive working model.** Treat conversion as increasing, saturating with effective charge/time, while selectivity and faradaic/transport efficiency are window functions of signed potential, cap, and material. Selective yield is approximately conversion × productive selectivity but assay channels need not multiply exactly because they are independently calibrated/noisy. Low/moderate drive can preserve efficiency; extreme potential or a permissive high-current cap can collapse it. pH/precipitation primarily identify medium state and may modify transport.

**Recommendation decision.** Batch 11 (event 0077: S1/E1, +0.75 V, 20 mA, 3600 s) is the best operating recommendation despite only moderate yield, because it has the highest observed public score and simultaneously high selectivity, faradaic, transport, ohmic, and energy efficiencies. Batch 10 offers higher conversion/yield but much poorer energy and faradaic efficiency. This decision would change if the objective prioritized throughput/yield over balanced efficiency.

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
      "duration_s": 300,
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
    "cost": 0.2827799916267395,
    "electrochemical_conversion": 0.008014115504920483,
    "electrochemical_selectivity": 0.01034972071647644,
    "energy_efficiency": 0.005256945732980967,
    "faradaic_efficiency": 0.02452157624065876,
    "ohmic_efficiency": 0.9742781519889832,
    "pH_normalized": 0.23031213879585266,
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
      "duration_s": 300,
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
    "cost": 0.2827799916267395,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.48389551043510437,
    "energy_efficiency": 0.09307534247636795,
    "faradaic_efficiency": 0.28971680998802185,
    "ohmic_efficiency": 0.9831159710884094,
    "pH_normalized": 0.2276168018579483,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.11784496903419495,
    "selective_product_yield": 0.01004763413220644,
    "transport_efficiency": 0.3159736394882202
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
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "current_mA": 20,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 0.75
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
    "cost": 0.29160359501838684,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.8769968748092651,
    "energy_efficiency": 0.8754001259803772,
    "faradaic_efficiency": 0.7729300260543823,
    "ohmic_efficiency": 0.9767675995826721,
    "pH_normalized": 0.21038080751895905,
    "precipitation_signal": 0.6509549021720886,
    "safety_risk": 0.09559440612792969,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.7894869446754456
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
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "current_mA": 300,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 2.25
    },
    {
      "duration_s": 900,
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
    "cost": 0.3010300099849701,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.02824951522052288,
    "ohmic_efficiency": 0.9501097798347473,
    "pH_normalized": 0.20969022810459137,
    "precipitation_signal": 0.6517031192779541,
    "safety_risk": 0.09559440612792969,
    "score": 0.003144612768664956,
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
      "solvent": 2,
      "volume_L": 0.04
    },
    {
      "current_mA": 20,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -0.75
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
    "cost": 0.3172036111354828,
    "electrochemical_conversion": 0.0035535290371626616,
    "electrochemical_selectivity": 0.5332017540931702,
    "energy_efficiency": 0.3828665614128113,
    "faradaic_efficiency": 0.34708765149116516,
    "ohmic_efficiency": 0.9814807176589966,
    "pH_normalized": 0.1780887395143509,
    "precipitation_signal": 0.0,
    "safety_risk": 0.1135944053530693,
    "score": 0.12531405687332153,
    "selective_product_yield": 0.008520460687577724,
    "transport_efficiency": 0.3365781605243683
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
      "solvent": 2,
      "volume_L": 0.04
    },
    {
      "current_mA": 300,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -2.25
    },
    {
      "duration_s": 900,
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
    "cost": 0.32662999629974365,
    "electrochemical_conversion": 0.015097436495125294,
    "electrochemical_selectivity": 0.39513564109802246,
    "energy_efficiency": 0.05065391957759857,
    "faradaic_efficiency": 0.20911139249801636,
    "ohmic_efficiency": 0.9170047044754028,
    "pH_normalized": 0.17481280863285065,
    "precipitation_signal": 0.0023995577357709408,
    "safety_risk": 0.1135944053530693,
    "score": 0.1461973786354065,
    "selective_product_yield": 0.015397783368825912,
    "transport_efficiency": 0.18442805111408234
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
      "solvent": 3,
      "volume_L": 0.04
    },
    {
      "current_mA": 5,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": 1.5
    },
    {
      "duration_s": 900,
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
    "cost": 0.30122700333595276,
    "electrochemical_conversion": 0.01128576323390007,
    "electrochemical_selectivity": 0.8011499643325806,
    "energy_efficiency": 0.729966938495636,
    "faradaic_efficiency": 0.8019527792930603,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.28484079241752625,
    "precipitation_signal": 0.0,
    "safety_risk": 0.12619440257549286,
    "score": 0.19700385630130768,
    "selective_product_yield": 0.008041332475841045,
    "transport_efficiency": 0.8053531050682068
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
      "solvent": 3,
      "volume_L": 0.04
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": 1.5
    },
    {
      "duration_s": 900,
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
    "cost": 0.3109000027179718,
    "electrochemical_conversion": 0.007480132393538952,
    "electrochemical_selectivity": 0.8074412941932678,
    "energy_efficiency": 0.09436627477407455,
    "faradaic_efficiency": 0.11517836898565292,
    "ohmic_efficiency": 0.9356027245521545,
    "pH_normalized": 0.2831433117389679,
    "precipitation_signal": 0.00031451715040020645,
    "safety_risk": 0.12619440257549286,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.1086830124258995
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
      "current_mA": 100,
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
    "cost": 0.2847599983215332,
    "electrochemical_conversion": 0.025136789306998253,
    "electrochemical_selectivity": 0.46471408009529114,
    "energy_efficiency": 0.13780859112739563,
    "faradaic_efficiency": 0.2812131643295288,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.22865696251392365,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.2458537220954895,
    "selective_product_yield": 0.030038727447390556,
    "transport_efficiency": 0.30204442143440247
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
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.5
    },
    {
      "duration_s": 14400,
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
    "cost": 0.2842400074005127,
    "electrochemical_conversion": 0.1235232874751091,
    "electrochemical_selectivity": 0.49290627241134644,
    "energy_efficiency": 0.12098605930805206,
    "faradaic_efficiency": 0.29889488220214844,
    "ohmic_efficiency": 0.9725879430770874,
    "pH_normalized": 0.2263428121805191,
    "precipitation_signal": 0.9927664399147034,
    "safety_risk": 0.072194404900074,
    "score": 0.26277896761894226,
    "selective_product_yield": 0.04881305247545242,
    "transport_efficiency": 0.30024445056915283
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
      "current_mA": 20,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 0.75
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
    "cost": 0.2988159954547882,
    "electrochemical_conversion": 0.028387783095240593,
    "electrochemical_selectivity": 0.8816697597503662,
    "energy_efficiency": 0.8945979475975037,
    "faradaic_efficiency": 0.8027969002723694,
    "ohmic_efficiency": 0.9929443001747131,
    "pH_normalized": 0.20937687158584595,
    "precipitation_signal": 0.6644999384880066,
    "safety_risk": 0.09559440612792969,
    "score": 0.3950403332710266,
    "selective_product_yield": 0.014892694540321827,
    "transport_efficiency": 0.8099768757820129
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
      "solvent": 2,
      "volume_L": 0.04
    },
    {
      "current_mA": 300,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -2.25
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
    "cost": 0.33664000034332275,
    "electrochemical_conversion": 0.08716204017400742,
    "electrochemical_selectivity": 0.3735675513744354,
    "energy_efficiency": 0.0473993755877018,
    "faradaic_efficiency": 0.15094317495822906,
    "ohmic_efficiency": 0.9330808520317078,
    "pH_normalized": 0.17333491146564484,
    "precipitation_signal": 0.0,
    "safety_risk": 0.1135944053530693,
    "score": 0.1972997784614563,
    "selective_product_yield": 0.05154024064540863,
    "transport_efficiency": 0.17216812074184418
  }
}
```

## K1 封存报告

Mechanistic account

1. Experimental scope

All 12 batches used 0.020 mol of the anonymous limiting reagent in 0.040 L of solvent, corresponding to a nominal initial loading of 0.50 mol L⁻¹. I varied the anonymous solvent/electrolyte pair, signed potential, current cap, and electrolysis duration. Each batch had one intermediate UV–visible or pH measurement and one final assay. The material labels are benchmark-only identifiers, so this report makes no claims about real chemical identities.

The evidence supports a charge-driven conversion process embedded in a narrower, material-dependent electrochemical efficiency window. Time or effective charge raises conversion, but potential and current cap determine what fraction of the electrical drive follows the productive pathway. Excessive drive can therefore produce worse faradaic, transport, and energy efficiency without proportionally improving selective product yield.

2. Proposed process model

A useful latent-variable model is:

I_eff = min(I_cap, I_kinetic(V,M), I_transport(V,M,X))

Q_eff = integral I_eff dt

X(t) = 1 − exp[−k(V,M) Q_eff/n0]

Y_product ≈ X × S(V,I_eff,M,X)

Here M represents the combined solvent/electrolyte environment, X is conversion, S is productive selectivity, and n0 is the initial reagent amount. Because actual current and delivered charge were not measured, Q_eff is latent rather than observed.

I interpret the reported faradaic efficiency as a proxy for the fraction of charge entering productive chemistry, transport efficiency as the fraction of the electrochemical demand that can be supplied without severe mass-transfer loss, ohmic efficiency as the absence of a large resistive penalty, and energy efficiency as their combined energetic consequence. One possible qualitative factorization is:

energy efficiency ≈ f(|V|) × faradaic efficiency × transport efficiency × ohmic efficiency,

where f includes voltage demand and other normalization. This is not an exact fitted identity; the channels were independently calibrated and noisy.

The productive rate constant and selectivity appear window-shaped rather than monotonic in potential and current. In pseudocode:

activation = signed_potential_response(V,M)
side_reaction_penalty = g(excess_overpotential, I_eff, M)
transport_penalty = h(I_eff, conversion, M)
productive_rate = activation × faradaic_efficiency × transport_efficiency

Increasing duration then raises conversion, while excessive potential or a permissive current cap can lower the productive fraction. Thus high instantaneous efficiency and high accumulated yield need not occur at the same setting.

3. Evidence that formed the account

Polarity was first implicated by the matched S0/E0 experiments. Batch 1 used +1.5 V, 100 mA, and 300 s. Its final conversion was 0.0080, selectivity 0.0103, faradaic efficiency 0.0245, transport efficiency 0, and selective yield 0. Batch 2 changed only the potential to −1.5 V. It produced selectivity 0.4839, faradaic efficiency 0.2897, transport efficiency 0.3160, and selective yield 0.0100. Its reported conversion was 0, which is inconsistent with taking every small channel estimate literally, but the coordinated changes in multiple efficiency channels support a genuine polarity effect. The smallest conversion and yield estimates are close to their declared noise scales.

Batches 3 and 4 showed that positive polarity is not intrinsically inactive. In S1/E1, batch 3 at +0.75 V, 20 mA, and 60 s had selectivity 0.8770, faradaic efficiency 0.7729, transport efficiency 0.7895, ohmic efficiency 0.9768, and energy efficiency 0.8754, but no resolved conversion or yield. This looks like an efficient operating state observed before enough charge had accumulated. In contrast, batch 4 at +2.25 V, 300 mA, and 900 s had selectivity 0, transport efficiency 0, energy efficiency 0, and yield only 0.00079. Potential, current cap, and time all changed together, so this pair alone cannot identify which variable caused the collapse; it does show that stronger nominal drive was not automatically better.

The analogous S2/E2 observations reinforce the distinction between accumulated conversion and instantaneous efficiency. Batch 5 at −0.75 V, 20 mA, and 60 s had faradaic efficiency 0.3471, transport efficiency 0.3366, energy efficiency 0.3829, conversion 0.00355, and yield 0.00852. Batch 6 at −2.25 V, 300 mA, and 900 s had conversion 0.0151 and yield 0.0154, but lower faradaic, transport, and energy efficiencies of 0.2091, 0.1844, and 0.0507. The higher-drive condition accumulated more product while operating less efficiently.

The decisive current-cap test was the matched S3/E3 pair. Batch 7 used +1.5 V, a 5 mA cap, and 900 s. Its faradaic, transport, and energy efficiencies were 0.8020, 0.8054, and 0.7300; selectivity was 0.8011 and yield 0.00804. Batch 8 differed only in using a 500 mA cap. Its corresponding efficiencies fell to 0.1152, 0.1087, and 0.0944, while yield was unresolved at zero. Ohmic efficiency remained high in both batches, 1.000 and 0.9356. This changed my initial simple hypothesis that a higher cap should merely accelerate a short run. Instead, the current cap couples strongly to faradaic and transport losses. The experiment does not reveal actual current, so the safest interpretation is that the high cap permitted entry into an inefficient regime rather than proving that 500 mA was continuously delivered.

The clearest duration series was S0/E0 at −1.5 V and 100 mA. From batches 2, 9, and 10, increasing duration from 300 to 3600 to 14400 s raised selective yield from 0.0100 to 0.0300 to 0.0488. Reported conversion changed from 0 to 0.0251 to 0.1235. The first yield increase was about threefold for a twelvefold duration increase; the next was only about 1.63-fold for a further fourfold duration increase. This supports continuing conversion with diminishing selective-yield returns. Across these batches, faradaic efficiency stayed near 0.28–0.30 and transport efficiency near 0.30, while selectivity remained approximately 0.46–0.49. The relative stability of those efficiencies makes duration or accumulated charge the most plausible cause of the conversion trend.

Batch 11 tested whether the efficient mild-positive S1/E1 state from batch 3 could eventually form product. At +0.75 V, 20 mA, and 3600 s it gave conversion 0.0284, selective yield 0.0149, selectivity 0.8817, faradaic efficiency 0.8028, transport efficiency 0.8100, ohmic efficiency 0.9929, and energy efficiency 0.8946. This supports the earlier interpretation that batch 3 was efficient but too short, rather than chemically inactive. It also demonstrates that productive polarity depends on the material environment and operating window.

Batch 12 extended the high-drive S2/E2 condition from batch 6 to 7200 s while retaining −2.25 V and 300 mA. Conversion rose to 0.0872 and yield to 0.0515, but selectivity was only 0.3736, faradaic efficiency 0.1509, transport efficiency 0.1722, and energy efficiency 0.0474. Thus long operation can accumulate substantial product even in an inefficient regime. This is compatible with the proposed separation between a time-integrated conversion variable and instantaneous pathway efficiencies.

4. Medium state and coupling

The pH-normalized and precipitation channels behaved mainly as reproducible fingerprints of the paired media. S0/E0 repeatedly had pH-normalized values near 0.23 and precipitation near 1. S1/E1 repeatedly had pH-normalized values near 0.21 and precipitation near 0.65. S2/E2 repeatedly had pH-normalized values near 0.17–0.18 and precipitation near zero. S3/E3 had pH-normalized values near 0.28 and precipitation near zero in the measured low-current batch. Their stability across different durations suggests that they are dominated by medium composition rather than accumulated conversion over the explored range.

These variables could affect ion availability, interfacial speciation, mass transport, or competing pathways, thereby shifting the potential window. However, the evidence does not establish that precipitation causes a particular efficiency response. For example, S0/E0 displayed precipitation near one while retaining high ohmic efficiency and moderate faradaic/transport efficiency at negative potential. Precipitation may instead be a correlated medium-state marker or a benign phase signal.

5. Measurement consistency and limitations

Intermediate UV–visible measurements generally supported the qualitative final-assay regimes. Batch 1 was near zero in faradaic, transport, and energy efficiency at both stages. Batch 9 gave intermediate faradaic/transport efficiencies of 0.294/0.298 and final values of 0.281/0.302. Batch 11 gave intermediate values of 0.761/0.808 and final values of 0.803/0.810. These agreements strengthen the high-versus-low efficiency distinctions. Exact discrepancies should not be overinterpreted because UV–visible measurements have larger declared noise than final assays.

Conversion, selective yield, and selectivity should be understood as independently noisy processed estimates, not exact algebraic components. Batch 2, for example, reported zero conversion but a small positive yield; batch 5 reported yield greater than conversion. Such low-level inconsistencies are plausibly explained by independent calibration, clipping at zero, and measurement noise. I therefore infer the latent process from coordinated movements across multiple channels and from duration series rather than enforcing an exact observed identity Y = X × S.

6. Scope and unidentifiable factors

The model is supported only at one initial concentration and volume. Reagent concentration, reagent amount, solvent volume, electrode area, mixing, temperature, and actual current were not independently varied or observed. Consequently, I cannot separate intrinsic kinetic constants from mass-transfer or geometric factors.

Solvent and electrolyte identities were paired as S0/E0, S1/E1, S2/E2, and S3/E3; they were not factorially crossed. Their individual effects and solvent–electrolyte interactions are therefore unidentifiable. Each final setting was measured once, so fine differences comparable to assay noise are unresolved. The longest time tested was 14400 s, and extrapolation beyond it is unsafe because depletion, fouling, or changing selectivity could become important.

Potential, current cap, and duration were not fully factorial across all media. The proposed smooth saturation and window functions are therefore mechanistic conjectures consistent with the data, not uniquely fitted laws. In particular, the data cannot distinguish whether the high-current collapse is caused primarily by side reactions, concentration polarization, interfacial changes, or another benchmark-specific rule.

7. Plausible alternatives

An alternative to the effective-charge model is a two-state electrode or medium transition: mild conditions occupy a selective state, whereas high potential or current cap switches the interface into an inefficient state. That model would also explain the sharp batch 7 versus batch 8 contrast.

Another alternative is that each medium has a different formal potential, so the apparent polarity and magnitude effects are simply distances from a material-specific optimum. This is plausible and is partly incorporated in the signed_potential_response term, but the experiments cannot recover those formal potentials uniquely.

The stable pH and precipitation signals could be causal modifiers of speciation and transport, or merely outputs that identify the medium. The paired-material design cannot discriminate those explanations. Similarly, diminishing yield with time could reflect ordinary substrate depletion, slow product loss, electrode fouling, or a decreasing productive current; no direct channel isolated these possibilities.

8. Overall conclusion

Within the tested benchmark, conversion is best understood as an accumulated, approximately saturating response to latent effective charge. Selectivity and electrical efficiencies are controlled by a narrower material-dependent window in signed potential and current cap. Mild drive can give excellent faradaic, transport, ohmic, and energy efficiencies but requires sufficient time to accumulate measurable product, as shown by batches 3 and 11. Strong or permissive drive can raise long-time conversion while wasting charge and energy, as shown by batches 6, 8, and 12. The S0/E0 time series demonstrates diminishing selective-yield returns, while the S3/E3 current-cap pair shows that nominally greater available current can be actively harmful. This account explains the major coordinated observations, but actual delivered current, separate solvent and electrolyte effects, and the microscopic origin of the inefficient state remain unidentifiable.

## K2 封存报告

1. Claims and laws

No instance-specific prior mechanism, nominal property dossier, or supplied law was provided. The solvent and electrolyte labels were explicitly anonymous, so the tested claims were self-developed from the campaign.

My initial signed-potential/time hypothesis was supported but required qualification. The matched S0/E0 comparison changed my judgment first: batch 1 at +1.5 V was essentially unproductive, whereas batch 2 at −1.5 V had appreciable selectivity and faradaic/transport efficiencies. This supported a polarity effect. However, batches 3 and 11 showed that positive polarity can be highly efficient and productive in S1/E1 at +0.75 V. I therefore rejected any universal “negative potential is productive” rule in favor of a material-dependent potential window.

The law that conversion accumulates with time while selective yield shows diminishing returns was supported locally. In the matched S0/E0 series, batches 2, 9, and 10 increased from 300 to 3600 to 14400 s; conversion rose from an unresolved value to 0.025 and 0.124, while yield rose from 0.010 to 0.030 and 0.049. Batch 11 also changed the interpretation of batch 3: the short batch had excellent efficiencies but no resolved yield, whereas the longer matched condition produced measurable conversion and yield. An exponential or other specific saturation equation remains untested; only the qualitative accumulating, sublinear response is supported.

My initial current-cap claim—that increasing the cap would accelerate conversion until a ceiling—was contradicted in its simple form. Batches 7 and 8 differed only by a 5 versus 500 mA cap at S3/E3, +1.5 V, and 900 s. Faradaic and transport efficiencies fell from about 0.80 to about 0.11, and yield went from 0.008 to unresolved. This was the clearest judgment-changing result and led to the revised claim that a high cap can admit a low-efficiency regime. Whether that regime reflects continuous transport loss or a discrete interfacial transition remains untested because actual current was not observed.

Stable medium fingerprints were supported: S0/E0 repeatedly showed pH-normalized near 0.23 and precipitation near one; S1/E1 showed approximately 0.21 and 0.65; S2/E2 showed approximately 0.17–0.18 and near-zero precipitation. The stronger claim that these variables causally control performance was not tested. Solvent and electrolyte were paired rather than crossed.

An exact observed law such as yield = conversion × selectivity was contradicted by small-channel inconsistencies, notably batches 2 and 5. I retained it only as a possible latent relation obscured by independent calibration, clipping, and noise. The proposed factorization of energy efficiency into voltage, faradaic, transport, and ohmic terms was explanatory rather than fitted and remains untested quantitatively.

2. One additional discriminating experiment

I would repeat the batch 7/8 S3/E3 condition at +1.5 V for 900 s but use an intermediate 100 mA cap. This directly targets the distinction between my leading continuous effective-current/transport-penalty account and the alternative of a threshold-like two-state electrode or medium transition.

A moderate result—for example, faradaic and transport efficiencies between the approximately 0.80 values of batch 7 and the approximately 0.11 values of batch 8—would support a continuous cap-dependent penalty. Efficiencies remaining close to batch 7 would suggest a threshold above 100 mA; values already close to batch 8 would suggest a threshold below 100 mA. A result outside both endpoint regimes would indicate stronger non-monotonic behavior or poor repeatability and would weaken both explanations. Selectivity stayed near 0.80 in both original endpoint batches, so a large selectivity collapse at 100 mA would also force revision of my claim that the cap primarily changes charge and transport efficiency rather than intrinsic product selection. Even this experiment would not identify the microscopic cause without an actual-current measurement.

3. Unused evidence, reliability, and effect of the goal

I did not quantitatively model the raw spectral traces, peak assignments, electrode-millivolt signals, or replicate-level instrument signals; I used their processed estimates. Cost and most safety-risk observations were also not mechanistically informative and were not included in the model. Ohmic efficiency was considered qualitatively but varied much less than the other efficiency channels, so it supplied little discrimination. Several isolated conditions, especially batch 4, were used only as qualitative evidence because potential, current cap, and duration changed together.

The least reliable blind predictions are Q05–Q10 because they contain solvent/electrolyte crossings never tested in the campaign. My inference that electrolyte profile largely determines the favorable potential sign is plausible but not identified separately from solvent. Q11 and Q12 are also weak because the only direct 5-versus-500 mA comparison was in S3/E3, not E0. Positive-potential S0 predictions are interpolations from a poor +1.5 V result rather than measurements at +0.8 V. Prediction intervals were widened for these cases, but structural uncertainty may still exceed them. No prediction truth was supplied, so none of these extrapolations has been retrospectively validated.

The recommendation of batch 11 is reliable as a selection among the 12 observed balanced scores, but not as a universal optimum. It was a single replicate, had only moderate yield, and was tested at one loading. A throughput- or yield-focused objective could instead favor a long-duration condition such as batch 10 or 12.

The explanatory research goal materially affected evidence collection. I prioritized polarity comparisons, a duration series, a current-cap contrast, all four paired media, and intermediate measurements rather than repeatedly optimizing the public score. That improved mechanistic discrimination but left too few batches for replication, a full solvent-by-electrolyte factorial design, or a dense response surface. There was no clear conflict with the stated goal because optimization was explicitly secondary; however, the resulting operating recommendation is less thoroughly optimized than it would have been in a score-only campaign.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.35,
        "upper80": 0.75
      },
      "energy_efficiency": {
        "estimate": 0.3,
        "lower80": 0.12,
        "upper80": 0.48
      },
      "faradaic_efficiency": {
        "estimate": 0.4,
        "lower80": 0.2,
        "upper80": 0.6
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.18,
        "lower80": 0.05,
        "upper80": 0.31
      },
      "selective_product_yield": {
        "estimate": 0.012,
        "lower80": 0,
        "upper80": 0.03
      },
      "transport_efficiency": {
        "estimate": 0.42,
        "lower80": 0.2,
        "upper80": 0.62
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.2,
        "lower80": 0.02,
        "upper80": 0.4
      },
      "energy_efficiency": {
        "estimate": 0.06,
        "lower80": 0,
        "upper80": 0.2
      },
      "faradaic_efficiency": {
        "estimate": 0.12,
        "lower80": 0,
        "upper80": 0.3
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.02,
        "lower80": 0,
        "upper80": 0.1
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.12,
        "lower80": 0,
        "upper80": 0.3
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.4,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.3,
        "lower80": 0.16,
        "upper80": 0.43
      },
      "faradaic_efficiency": {
        "estimate": 0.4,
        "lower80": 0.25,
        "upper80": 0.55
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.32,
        "lower80": 0.22,
        "upper80": 0.39
      },
      "selective_product_yield": {
        "estimate": 0.045,
        "lower80": 0.02,
        "upper80": 0.07
      },
      "transport_efficiency": {
        "estimate": 0.42,
        "lower80": 0.25,
        "upper80": 0.58
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.2,
        "lower80": 0.03,
        "upper80": 0.4
      },
      "energy_efficiency": {
        "estimate": 0.06,
        "lower80": 0,
        "upper80": 0.2
      },
      "faradaic_efficiency": {
        "estimate": 0.12,
        "lower80": 0,
        "upper80": 0.3
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.08,
        "lower80": 0,
        "upper80": 0.18
      },
      "selective_product_yield": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.03
      },
      "transport_efficiency": {
        "estimate": 0.12,
        "lower80": 0,
        "upper80": 0.3
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.15,
        "lower80": 0.03,
        "upper80": 0.4
      },
      "energy_efficiency": {
        "estimate": 0.08,
        "lower80": 0,
        "upper80": 0.3
      },
      "faradaic_efficiency": {
        "estimate": 0.12,
        "lower80": 0,
        "upper80": 0.35
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.06,
        "lower80": 0,
        "upper80": 0.18
      },
      "selective_product_yield": {
        "estimate": 0.008,
        "lower80": 0,
        "upper80": 0.03
      },
      "transport_efficiency": {
        "estimate": 0.15,
        "lower80": 0,
        "upper80": 0.4
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.82,
        "lower80": 0.6,
        "upper80": 0.93
      },
      "energy_efficiency": {
        "estimate": 0.55,
        "lower80": 0.28,
        "upper80": 0.78
      },
      "faradaic_efficiency": {
        "estimate": 0.55,
        "lower80": 0.3,
        "upper80": 0.75
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.42,
        "lower80": 0.28,
        "upper80": 0.54
      },
      "selective_product_yield": {
        "estimate": 0.035,
        "lower80": 0.015,
        "upper80": 0.065
      },
      "transport_efficiency": {
        "estimate": 0.58,
        "lower80": 0.32,
        "upper80": 0.78
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.15,
        "lower80": 0.02,
        "upper80": 0.4
      },
      "energy_efficiency": {
        "estimate": 0.06,
        "lower80": 0,
        "upper80": 0.25
      },
      "faradaic_efficiency": {
        "estimate": 0.1,
        "lower80": 0,
        "upper80": 0.32
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.04,
        "lower80": 0,
        "upper80": 0.16
      },
      "selective_product_yield": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.025
      },
      "transport_efficiency": {
        "estimate": 0.12,
        "lower80": 0,
        "upper80": 0.36
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.78,
        "lower80": 0.55,
        "upper80": 0.92
      },
      "energy_efficiency": {
        "estimate": 0.42,
        "lower80": 0.2,
        "upper80": 0.67
      },
      "faradaic_efficiency": {
        "estimate": 0.45,
        "lower80": 0.22,
        "upper80": 0.68
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.38,
        "lower80": 0.22,
        "upper80": 0.52
      },
      "selective_product_yield": {
        "estimate": 0.035,
        "lower80": 0.012,
        "upper80": 0.065
      },
      "transport_efficiency": {
        "estimate": 0.48,
        "lower80": 0.25,
        "upper80": 0.72
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.35,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.28,
        "lower80": 0.1,
        "upper80": 0.5
      },
      "faradaic_efficiency": {
        "estimate": 0.35,
        "lower80": 0.18,
        "upper80": 0.55
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.3,
        "lower80": 0.18,
        "upper80": 0.4
      },
      "selective_product_yield": {
        "estimate": 0.04,
        "lower80": 0.018,
        "upper80": 0.07
      },
      "transport_efficiency": {
        "estimate": 0.36,
        "lower80": 0.18,
        "upper80": 0.58
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.18,
        "lower80": 0.02,
        "upper80": 0.42
      },
      "energy_efficiency": {
        "estimate": 0.07,
        "lower80": 0,
        "upper80": 0.28
      },
      "faradaic_efficiency": {
        "estimate": 0.12,
        "lower80": 0,
        "upper80": 0.34
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.06,
        "lower80": 0,
        "upper80": 0.18
      },
      "selective_product_yield": {
        "estimate": 0.008,
        "lower80": 0,
        "upper80": 0.028
      },
      "transport_efficiency": {
        "estimate": 0.14,
        "lower80": 0,
        "upper80": 0.38
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.35,
        "upper80": 0.75
      },
      "energy_efficiency": {
        "estimate": 0.07,
        "lower80": 0,
        "upper80": 0.22
      },
      "faradaic_efficiency": {
        "estimate": 0.12,
        "lower80": 0.03,
        "upper80": 0.3
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.21,
        "lower80": 0.1,
        "upper80": 0.32
      },
      "selective_product_yield": {
        "estimate": 0.025,
        "lower80": 0.005,
        "upper80": 0.055
      },
      "transport_efficiency": {
        "estimate": 0.12,
        "lower80": 0.02,
        "upper80": 0.3
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.2,
        "lower80": 0.01,
        "upper80": 0.43
      },
      "energy_efficiency": {
        "estimate": 0.02,
        "lower80": 0,
        "upper80": 0.12
      },
      "faradaic_efficiency": {
        "estimate": 0.05,
        "lower80": 0,
        "upper80": 0.2
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.02,
        "lower80": 0,
        "upper80": 0.1
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0,
        "upper80": 0.02
      },
      "transport_efficiency": {
        "estimate": 0.05,
        "lower80": 0,
        "upper80": 0.2
      }
    }
  ],
  "rationale": "Predictions use the observed polarity-dependent efficiency windows, the S0/E0 duration series, and the sharp efficiency loss at high current cap. I treated E0 as favoring negative potential and inferred—more uncertainly—from the paired campaign data that E1 and E3 favor positive potential. Yield increases sublinearly with duration, while selectivity and electrical efficiencies are primarily operating-window properties. Intervals are widest for untested solvent/electrolyte crossings and high-current extrapolations; score estimates also include the published low-yield multiplicative gate."
}
```
