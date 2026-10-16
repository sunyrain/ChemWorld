# repeat-01/EC-W04-B12-discovery-E-Opaque

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-01\EC-W04-B12-discovery-E-Opaque\participant\discovery-E-Opaque

## 同期笔记

### v1 · 公开事件 0

# Electrochemical hypothesis notebook

## Pre-experiment expectations

**H1 [tentative] — charge/potential response.** At fixed loading (0.020 mol in 0.050 L), conversion should rise with electrolysis duration and delivered charge until reagent depletion, while selectivity may peak at an intermediate signed potential/current because stronger forcing can promote degradation. The current setting is only a cap, so observed behavior may instead be potential- or transport-limited.

**H2 [tentative] — medium and electrolyte effects.** Solvent and electrolyte identities may independently alter transport/ohmic efficiency and the productive potential window. A crossed screen across anonymous labels and both potential signs should reveal whether effects are broad main effects or interactions.

**H3 [tentative] — time course.** If electrochemical conversion is approximately first-order in remaining reagent under stable current, conversion will show diminishing returns with duration; if charge-limited at stable delivered current it may instead be near-linear initially. Intermediate UV–vis followed by final assay will be used within batches to distinguish time response from endpoint-only differences.

**Decision plan.** Use a common loading and volume for comparability, span both potential signs, multiple durations/current caps, and all material labels. Replicate a promising condition late. Numerical differences smaller than declared measurement noise or unsupported by replication will remain unresolved.

### v2 · 公开事件 50

# Electrochemical hypothesis notebook

## Current interpretation

**H1 [supported for tested E0/S0 scope] — polarity and forcing.** Negative potential is the productive polarity. At the common 0.020 mol/0.050 L loading, −1 V for 600 s gave selective-product yield 0.0133 and score 0.212 (event runner-operation-0015), whereas +1 V for 600 s gave reported yield 0 and score 0 (runner-operation-0008). Stronger/longer forcing was not proportionally beneficial: −1.5 V, 300 mA, 3600 s only reached yield 0.0173 with much lower energy/transport efficiencies (runner-operation-0022); +2 V was essentially unproductive (runner-operation-0029). This supports a cathodic target pathway plus increasing parasitic loss at strong forcing, but current and time remain confounded in the −1.5 V comparison.

**H2 [unresolved] — materials.** Diagonal S1/E1, S2/E2, and S3/E3 screens at −1 V, 100 mA, 600 s differed numerically (runner-operation-0036, -0043, -0050), but each changes solvent and electrolyte together. S2/E2 suppressed precipitation almost completely and retained a relatively high score, while S0/E0 scored highest. Crossed S2/E0 and S0/E2 tests are needed to allocate these effects.

**H3 [partly opposed] — simple charge control.** The weak gain from substantially more nominal charge in runner-operation-0022 versus -0015, alongside lower efficiency, argues against a single linear charge law over this range. Alternatives include potential-dependent selectivity, current not reaching the cap, and rapid passivation/transport limitation. A matched time or current series in the best material pair is still needed.

**Measurement caveat.** Some final-assay conversion estimates were near zero while selective-product yield was positive; at this low-response regime the estimates and noise/missingness should not be forced into exact mass-balance identities.

### v3 · 公开事件 86

# Electrochemical hypothesis notebook

## Final source-stage interpretation

**H1 [supported in tested range] — polarity-dependent target formation.** At the fixed 0.020 mol in 0.050 L loading, negative potential produced measurable selective-product yield, whereas matched +1 V and stronger +2 V conditions were essentially unproductive (runner-operation-0015 versus -0008; runner-operation-0029). The safest predictive rule is therefore a cathodic productive branch and an anodic/nonproductive branch. Exact threshold and symmetry are unmeasured.

**H2 [supported qualitatively, quantitative law unresolved] — excessive forcing lowers efficiencies.** Relative to −1 V/100 mA/600 s (runner-operation-0015), −1.5 V/300 mA/3600 s produced only a small yield increase while faradaic, transport, and energy efficiencies fell sharply (runner-operation-0022). Because potential, cap, and time changed together, this establishes poor performance of that combined high-forcing regime, not separate causal coefficients. +2 V/300 mA/3600 s was also strongly inefficient and nonproductive (runner-operation-0029).

**H3 [supported] — electrolyte E2 changes solution/phase behavior.** In solvent S0 at −1 V/100 mA/600 s, E2 gave precipitation signal near zero and pH-normalized near 0.159 (runner-operation-0064), versus precipitation near one and pH near 0.232 for E0 (runner-operation-0015). The same low-precipitation/low-pH pattern recurred in the segmented replicate and long E2 batches (runner-operation-0079, -0086). Thus this material effect is repeatable even though yield is variable.

**H4 [tentative] — solvent S0 favors productive yield.** With E0 under the common electrical condition, S1 and S2 gave yields 0.00094 and 0 (runner-operation-0071, -0057), lower than S0's 0.0133 (runner-operation-0015). However these are single realizations and final-yield noise is 0.01, so the magnitude and even a small effect remain uncertain. S3/E0 was not tested.

**H5 [unresolved time response] — longer cathodic operation may raise yield with diminishing efficiency.** For S0/E2 at −1 V/100 mA, two 600 s endpoints yielded 0.0208 and 0.00554 (runner-operation-0064, -0079; mean about 0.0132), demonstrating substantial endpoint variability. The 3600 s endpoint yielded 0.0326 (runner-operation-0086), a numerical increase of about 0.0195 over that mean, but only one long run and assay noise/process variability prevent a firm kinetic law. Conversion estimates did not consistently track product yield near the low-response floor, so they should not be used alone to infer rate.

**Predictive scope and gaps.** The strongest transferable predictors are potential sign and E2-associated suppression of precipitation. Current-cap effects were not isolated, and the cap is not delivered current. Material interactions are incompletely crossed. For blind conditions, interpolate cautiously around −1 V; expect positive sign to give near-zero target yield, and treat long-duration gains as uncertain/saturating rather than linear in nominal charge.

**Operating decision.** Batch 9 is the recommendation candidate because it had the highest observed public score (0.310) under moderate cathodic forcing and E2's repeatable low-precipitation regime. Batch 12 had slightly lower score (0.301) and higher yield but required sixfold longer electrolysis. This choice would change if priority were maximal single-run yield regardless of time, in which case batch 12 would be preferred.

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
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1
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
      "duration_s": 300,
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
    "cost": 0.30324000120162964,
    "electrochemical_conversion": 0.01305403746664524,
    "electrochemical_selectivity": 1.0,
    "energy_efficiency": 0.27662381529808044,
    "faradaic_efficiency": 0.2867445647716522,
    "ohmic_efficiency": 0.9572166204452515,
    "pH_normalized": 0.2344122976064682,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.25804081559181213
  }
}
```

### 批次 2 · 终点事件 15

```json
{
  "ordinal": 2,
  "lifecycle_index": 2,
  "end_step": 15,
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
    "cost": 0.2852399945259094,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.6610745787620544,
    "energy_efficiency": 0.278411328792572,
    "faradaic_efficiency": 0.427999347448349,
    "ohmic_efficiency": 0.9660544395446777,
    "pH_normalized": 0.2317349761724472,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.2123403549194336,
    "selective_product_yield": 0.013313425704836845,
    "transport_efficiency": 0.454256147146225
  }
}
```

### 批次 3 · 终点事件 22

```json
{
  "ordinal": 3,
  "lifecycle_index": 3,
  "end_step": 22,
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
      "current_mA": 300,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.5
    },
    {
      "duration_s": 3600,
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
    "cost": 0.2844800055027008,
    "electrochemical_conversion": 0.04209668189287186,
    "electrochemical_selectivity": 0.5773762464523315,
    "energy_efficiency": 0.06392668187618256,
    "faradaic_efficiency": 0.14261692762374878,
    "ohmic_efficiency": 0.9191845059394836,
    "pH_normalized": 0.2324499785900116,
    "precipitation_signal": 0.9863388538360596,
    "safety_risk": 0.05933958664536476,
    "score": 0.1836196631193161,
    "selective_product_yield": 0.017309214919805527,
    "transport_efficiency": 0.15917383134365082
  }
}
```

### 批次 4 · 终点事件 29

```json
{
  "ordinal": 4,
  "lifecycle_index": 4,
  "end_step": 29,
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
      "current_mA": 300,
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
    "cost": 0.29363998770713806,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.02824951522052288,
    "ohmic_efficiency": 0.9481644034385681,
    "pH_normalized": 0.23175939917564392,
    "precipitation_signal": 0.9870871305465698,
    "safety_risk": 0.05933958664536476,
    "score": 0.003138467436656356,
    "selective_product_yield": 0.0007897500181570649,
    "transport_efficiency": 0.0
  }
}
```

### 批次 5 · 终点事件 36

```json
{
  "ordinal": 5,
  "lifecycle_index": 5,
  "end_step": 36,
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
      "current_mA": 100,
      "electrolyte_profile": 1,
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
    "cost": 0.3052400052547455,
    "electrochemical_conversion": 0.008301571011543274,
    "electrochemical_selectivity": 0.5074349045753479,
    "energy_efficiency": 0.19736437499523163,
    "faradaic_efficiency": 0.3231564164161682,
    "ohmic_efficiency": 0.9463586211204529,
    "pH_normalized": 0.2099734991788864,
    "precipitation_signal": 0.709762692451477,
    "safety_risk": 0.08273958414793015,
    "score": 0.13924196362495422,
    "selective_product_yield": 0.010896531865000725,
    "transport_efficiency": 0.3126469552516937
  }
}
```

### 批次 6 · 终点事件 43

```json
{
  "ordinal": 6,
  "lifecycle_index": 6,
  "end_step": 43,
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
      "current_mA": 100,
      "electrolyte_profile": 2,
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
    "cost": 0.3372400104999542,
    "electrochemical_conversion": 0.007184173446148634,
    "electrochemical_selectivity": 0.5703724026679993,
    "energy_efficiency": 0.3072640895843506,
    "faradaic_efficiency": 0.347796231508255,
    "ohmic_efficiency": 0.9284676909446716,
    "pH_normalized": 0.17581218481063843,
    "precipitation_signal": 0.0023995577357709408,
    "safety_risk": 0.10073958337306976,
    "score": 0.18767312169075012,
    "selective_product_yield": 0.013186510652303696,
    "transport_efficiency": 0.3231129050254822
  }
}
```

### 批次 7 · 终点事件 50

```json
{
  "ordinal": 7,
  "lifecycle_index": 7,
  "end_step": 50,
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
      "current_mA": 100,
      "electrolyte_profile": 3,
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
    "cost": 0.31723999977111816,
    "electrochemical_conversion": 0.014631609432399273,
    "electrochemical_selectivity": 0.47669339179992676,
    "energy_efficiency": 0.25446319580078125,
    "faradaic_efficiency": 0.2773588299751282,
    "ohmic_efficiency": 0.9978722929954529,
    "pH_normalized": 0.2787778973579407,
    "precipitation_signal": 0.0,
    "safety_risk": 0.11333958804607391,
    "score": 0.1191568374633789,
    "selective_product_yield": 0.009340956807136536,
    "transport_efficiency": 0.28075918555259705
  }
}
```

### 批次 8 · 终点事件 57

```json
{
  "ordinal": 8,
  "lifecycle_index": 8,
  "end_step": 57,
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
    "cost": 0.3372400104999542,
    "electrochemical_conversion": 0.0006503025069832802,
    "electrochemical_selectivity": 0.5949186086654663,
    "energy_efficiency": 0.3060525357723236,
    "faradaic_efficiency": 0.3721844255924225,
    "ohmic_efficiency": 0.9686378240585327,
    "pH_normalized": 0.24695418775081635,
    "precipitation_signal": 0.9850548505783081,
    "safety_risk": 0.10073958337306976,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.36568906903266907
  }
}
```

### 批次 9 · 终点事件 64

```json
{
  "ordinal": 9,
  "lifecycle_index": 9,
  "end_step": 64,
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
      "current_mA": 100,
      "electrolyte_profile": 2,
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
    "cost": 0.2852399945259094,
    "electrochemical_conversion": 0.0039770640432834625,
    "electrochemical_selectivity": 0.6026841402053833,
    "energy_efficiency": 0.3393875062465668,
    "faradaic_efficiency": 0.369478702545166,
    "ohmic_efficiency": 0.9875956177711487,
    "pH_normalized": 0.15940368175506592,
    "precipitation_signal": 0.008188718929886818,
    "safety_risk": 0.05933958664536476,
    "score": 0.3103313744068146,
    "selective_product_yield": 0.020822789520025253,
    "transport_efficiency": 0.3903099596500397
  }
}
```

### 批次 10 · 终点事件 71

```json
{
  "ordinal": 10,
  "lifecycle_index": 10,
  "end_step": 71,
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
    "cost": 0.3052400052547455,
    "electrochemical_conversion": 0.020977111533284187,
    "electrochemical_selectivity": 0.6223071813583374,
    "energy_efficiency": 0.2705433964729309,
    "faradaic_efficiency": 0.3696982264518738,
    "ohmic_efficiency": 0.945728600025177,
    "pH_normalized": 0.23380811512470245,
    "precipitation_signal": 0.987458348274231,
    "safety_risk": 0.08273958414793015,
    "score": 0.013862285763025284,
    "selective_product_yield": 0.0009448264609090984,
    "transport_efficiency": 0.37104782462120056
  }
}
```

### 批次 11 · 终点事件 79

```json
{
  "ordinal": 11,
  "lifecycle_index": 11,
  "end_step": 79,
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
      "current_mA": 100,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -1
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
      "duration_s": 300,
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
    "cost": 0.30324000120162964,
    "electrochemical_conversion": 0.020695678889751434,
    "electrochemical_selectivity": 0.6229200959205627,
    "energy_efficiency": 0.31449514627456665,
    "faradaic_efficiency": 0.40399739146232605,
    "ohmic_efficiency": 0.9605247974395752,
    "pH_normalized": 0.15805624425411224,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.05933958664536476,
    "score": 0.08606890588998795,
    "selective_product_yield": 0.005538844037801027,
    "transport_efficiency": 0.4111773371696472
  }
}
```

### 批次 12 · 终点事件 86

```json
{
  "ordinal": 12,
  "lifecycle_index": 12,
  "end_step": 86,
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
      "current_mA": 100,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -1
    },
    {
      "duration_s": 3600,
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
    "cost": 0.2794399857521057,
    "electrochemical_conversion": 0.018863549456000328,
    "electrochemical_selectivity": 0.594516932964325,
    "energy_efficiency": 0.29937005043029785,
    "faradaic_efficiency": 0.34402012825012207,
    "ohmic_efficiency": 0.9738733172416687,
    "pH_normalized": 0.15859489142894745,
    "precipitation_signal": 0.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.30147701501846313,
    "selective_product_yield": 0.03263607993721962,
    "transport_efficiency": 0.3652450740337372
  }
}
```

## K1 封存报告

Mechanistic account

I infer that the target is formed predominantly by a cathodic pathway. Potential polarity is the clearest electrical control: at the common loading of 0.020 mol reagent in 0.050 L solvent, batch 2 (S0/E0, −1.0 V, 100 mA cap, 600 s) produced selective-product yield 0.0133, whereas the approximately matched positive-polarity batch 1 (S0/E0, +1.0 V, 100 mA, 600 s) reported zero yield. Strongly positive batch 4 (+2.0 V, 300 mA, 3600 s) was also essentially unproductive, with yield 0.00079, zero estimated conversion and selectivity, and energy efficiency zero. Thus I expect the productive activation term to be large only at negative potential. Batch 1’s selectivity estimate of 1.0 should not be interpreted as genuine perfect selectivity because its product yield was at the measurement floor.

A useful qualitative kinetic model is

  dP/dt = k_prod(S,E) A_cathode(V) (1−X) η_transport − k_loss(S,E,V,I,t)P,

where A_cathode(V) rises as potential becomes sufficiently negative, while parasitic reaction, degradation, polarization or passivation losses increase with excessive overpotential, current and elapsed time. One possible parameterization is A_cathode(V)=sigmoid[−a(V−V0)] and k_loss=k_base+k_V|V|^m+k_I I_eff^n, but the data do not identify these coefficients or even the delivered current I_eff. The specified current was only a cap.

Evidence against a simple linear nominal-charge law comes from batch 3. Moving from batch 2’s −1.0 V, 100 mA and 600 s to −1.5 V, 300 mA and 3600 s increased yield only from 0.0133 to 0.0173. Meanwhile faradaic efficiency fell from 0.428 to 0.143, transport efficiency from 0.454 to 0.159, energy efficiency from 0.278 to 0.0639, and ohmic efficiency from 0.966 to 0.919. The combined high-forcing regime is therefore inefficient and plausibly dominated by side reactions, transport limitation or surface passivation. Potential, current cap and time all changed together, so their separate causal contributions are unidentifiable.

Duration may still increase cathodic product formation under moderate forcing. With S0/E2 at −1.0 V and 100 mA, the two 600 s endpoints, batches 9 and 11, yielded 0.0208 and 0.00554, respectively, while the 3600 s batch 12 yielded 0.0326. The 600 s mean was about 0.0132, so batch 12 was numerically about 0.0195 higher. However, the large difference between replicate-like batches 9 and 11, together with the stated yield noise of 0.01, makes the shape of the time response uncertain. I would use a saturating relationship such as Y(t)=Y_inf[1−exp(−kt)] multiplied by a loss term, rather than linear extrapolation with time or charge.

Medium effects

Electrolyte E2 has a strong and repeatable effect on pH and precipitation. In S0 at the common −1.0 V/100 mA/600 s condition, E0 in batch 2 gave normalized pH 0.2317 and precipitation signal 1.000, whereas E2 in batch 9 gave pH 0.1594 and precipitation 0.0082. The E2 pattern repeated in batches 11 and 12: normalized pH was 0.1581 and 0.1586, while precipitation was 0.0052 and 0.000. A second crossed comparison supports an approximately additive pH shift: S2/E0 in batch 8 had pH 0.2470, while S2/E2 in batch 6 had pH 0.1758. In both S0 and S2, substituting E2 for E0 lowered normalized pH by roughly 0.072–0.073.

A compact empirical pH model over this limited domain is

  pH_normalized ≈ baseline + solvent_offset[S] + electrolyte_offset[E],

with electrolyte_offset[E2] approximately −0.073 relative to E0. This is an interpolation, not a chemical pKa assignment, because the materials are anonymous.

Precipitation is not controlled by pH alone. E0 produced precipitation signals near one in S0, S1 and S2 (batches 2, 10 and 8). E2 suppressed precipitation in both tested solvents. Yet S3/E3 in batch 7 also had zero precipitation despite a much higher normalized pH of 0.2788. I therefore infer electrolyte-specific solubility, complexation or interfacial effects in addition to any pH coupling. A plausible empirical form is a threshold model,

  precipitation = sigmoid[a_E + b_S + c·pH_normalized + d_(S,E)],

with large electrolyte terms and possible interactions.

E2 did not demonstrably increase mean yield. In S0, the mean of E2 batches 9 and 11 at 600 s was about 0.0132, essentially the 0.0133 observed with E0 in batch 2, although individual scores differed greatly. In S2, E2 batch 6 yielded 0.0132 while E0 batch 8 reported zero, suggesting a possible favorable interaction, but each condition was observed once. The defensible conclusion is that E2 robustly changes pH and suppresses precipitation; a direct E2 yield advantage remains unresolved.

Solvent S0 may favor productive yield. With E0 at −1.0 V, 100 mA and 600 s, S0 in batch 2 yielded 0.0133, while S1 in batch 10 yielded 0.000945 and S2 in batch 8 yielded zero. These single-run differences suggest solvent-dependent productive kinetics, mass transport or product stability, but they are comparable to the assay noise and process variability. S3/E0 was never tested, so a complete solvent ranking is not identifiable.

Safety risk behaved primarily as a solvent lookup at the common loading: approximately 0.0593 for S0, 0.0827 for S1, 0.1007 for S2 and 0.1133 for S3. Repeated S0 batches retained the same risk despite changes in electrolyte, potential and duration. Within the tested conditions, I would therefore model risk as R≈R_solvent(S,loading), while avoiding extrapolation beyond the fixed concentration and volume.

Efficiency and measurement interpretation

Faradaic and transport efficiencies tended to move together, consistent with a shared limitation in productive charge utilization and delivery to the electrode. Ohmic efficiency remained comparatively high, about 0.919–0.998 across endpoints, so bulk resistance was probably not the dominant source of lost performance. Energy efficiency was much more sensitive to forcing and fell markedly in batch 3 and batch 4. I would represent these as coupled but distinct latent factors rather than impose an exact identity:

  useful_product_rate ∝ A_cathode(V) × η_F × η_T,
  energy_efficiency = f(η_F,η_T,η_O,V,I_eff),

where η_F, η_T and η_O are faradaic, transport and ohmic efficiencies.

Intermediate UV–visible measurements do not establish a clean time trend. In batch 1, the 300 s UV–visible estimates were higher than the 600 s final-assay efficiencies, which could indicate deterioration. In batch 11, the 300 s UV–visible estimates did not show the same direction relative to the 600 s final assay. Because these are different instruments with different uncertainty profiles, I do not treat cross-instrument changes as direct kinetic trajectories. By contrast, the pH-meter and final-assay pH values in batch 12 agreed closely (0.15885 versus 0.15859), supporting the stability of the E2 pH observation.

Conversion, selectivity and yield estimates near zero should not be forced into exact mass-balance equations. Several batches reported small or zero conversion alongside positive selective-product yield. For example, batch 2 reported zero conversion but yield 0.0133. These channels have independent noise and clipping near their lower boundary. I interpret them as noisy indicators of a low-response regime, not exact algebraic quantities satisfying Y=X×S in every run.

How the explanation changed

Batches 1 and 2 established polarity as the first major mechanism variable. Batch 3 rejected a naive assumption that more nominal charge would proportionally improve performance, while batch 4 reinforced the nonproductive nature of positive forcing. The diagonal material screen in batches 5–7 initially confounded solvent and electrolyte effects. Crossed batches 8–10 separated them and showed that E2’s strongest reproducible role was pH/precipitation control, while S0 appeared favorable for yield and safety. Batch 11 revealed substantial endpoint variability at nominally repeated S0/E2 conditions. Batch 12 supplied tentative evidence for a positive but non-linear duration effect under moderate cathodic forcing.

Scope, uncertainties and alternatives

This account applies mainly near 0.020 mol reagent in 0.050 L solvent, potentials around −1 V, a 100 mA cap, and durations from 600 to 3600 s. Reagent concentration, volume, current cap and delivered current were not independently varied. The cathodic threshold, detailed potential optimum, solvent–electrolyte interactions, product degradation rate and electrode passivation are unidentifiable. E1 and E3 were only observed in diagonal combinations, and S3 was never crossed with E0 or E2.

Plausible alternatives include: (1) the apparent high-forcing penalty is caused mainly by duration-dependent passivation rather than overpotential; (2) the current cap was rarely reached, making potential and medium conductivity the true controls; (3) precipitation changes assay accessibility rather than underlying reaction yield; and (4) E2 changes spectral or phase partitioning without changing intrinsic product formation. The present observations distinguish these alternatives only partially.

Overall, my best predictive account is a cathodically activated target pathway operating in competition with forcing-dependent loss processes. Solvent controls safety and probably productive kinetics; electrolyte E2 reproducibly lowers normalized pH and prevents precipitation; moderate negative forcing preserves charge and transport efficiency better than the tested high-forcing regimes. Yield increases with time are plausible but noisy and should be modeled as saturating, with wide uncertainty rather than proportional to nominal charge.

## K2 封存报告

1. Claim assessment

No instance-specific prior law or parameter set was supplied; only anonymous material labels and instrument/scoring contracts were provided.

Supported claims:
- A cathodic productive branch was supported. At otherwise similar S0/E0 conditions, batch 2 (−1.0 V, 100 mA, 600 s) gave selective-product yield 0.0133, whereas batch 1 (+1.0 V, 100 mA, 600 s) reported zero yield. Batch 4 at +2.0 V was also essentially unproductive (yield 0.00079). These observations changed polarity from a generic factor into the strongest qualitative predictor.
- E2 reproducibly changed solution/phase behavior. Replacing E0 with E2 lowered normalized pH by about 0.072–0.073 in both S0 (batches 2 and 9) and S2 (batches 8 and 6). Precipitation changed from approximately one with E0 to approximately zero with E2. Batches 11 and 12 repeated the low-pH, low-precipitation E2 pattern.
- Excess combined forcing was inefficient. Compared with batch 2, batch 3 (−1.5 V, 300 mA, 3600 s) gained little yield but lost substantial faradaic, transport and energy efficiency.

Contradicted or weakened claims:
- A simple linear relationship between nominal charge and product yield was contradicted by batch 3: much greater nominal charge produced only a small yield increase over batch 2. Batch 12 suggested that longer operation can help under moderate forcing, but not enough to restore a linear law.
- A deterministic yield advantage for E2 was weakened by batches 9 and 11. They used nearly the same S0/E2 electrical condition but yielded 0.0208 and 0.00554. Their mean was close to the S0/E0 yield in batch 2. E2’s phase effect is much better supported than a yield effect.
- A clean monotonic time course was not established. Batch 12 at 3600 s yielded more than the two 600 s S0/E2 runs, but there was only one long run and substantial replicate-like variability.

Untested or unresolved claims:
- Potential magnitude, current cap and duration were not independently separated in the high-forcing comparison.
- Delivered current was unobserved, so the current cap cannot be treated as actual current.
- A complete solvent ranking, E1/E3 main effects, most solvent–electrolyte interactions, the cathodic threshold, and concentration/volume scaling remained untested.
- The suggested saturating kinetic and precipitation-threshold equations were useful organizing models, not identified laws.

2. One additional discriminating experiment

I would run one S0/E0 batch at the original 0.020 mol/0.050 L loading, −1.5 V, 100 mA cap and 600 s, followed by the final assay. This differs from batch 2 only in potential and separates potential magnitude from the longer duration and higher current cap used together in batch 3.

If faradaic, transport and energy efficiencies collapsed toward batch 3 while yield improved little, I would strengthen the explanation that overpotential itself activates parasitic chemistry or polarization. If the result remained close to batch 2, I would instead attribute most of batch 3’s efficiency loss to long-duration passivation, the higher current cap, or their interaction. An intermediate result would support contributions from both potential and accumulated electrolysis. A surprisingly large yield increase without an efficiency penalty would contradict the proposed moderate-potential optimum and motivate a narrower potential-response study.

3. Unused evidence and reliability

The full raw spectral artifacts were not analyzed; interpretation mainly used processed estimates and the supplied peak summary. Cost, temperature changes, sample-volume changes and most raw signal shapes were not used mechanistically. Intermediate UV–visible observations were used cautiously because they could not be compared cleanly with final-assay values. Conversion estimates near zero were also down-weighted because they were inconsistent with small positive yield estimates at the measurement floor.

The least reliable predictions are those for E1 and E3, the 500 mA cap, 7200 s duration, the changed 0.012 mol/0.025 L loading, and positive-polarity selectivity. These required extrapolation from confounded or sparse evidence. Score predictions are especially fragile because the published yield gate makes them highly sensitive to noisy yields around 0.02.

The batch 9 recommendation is also uncertain: it had the highest observed score, 0.310, but batch 11 at nearly the same condition scored only 0.086, while batch 12 scored 0.301 after much longer electrolysis. Thus batch 9 may partly represent a favorable realization rather than a stable optimum.

The assigned goal emphasized explanation over score optimization. That encouraged broad polarity, material and duration contrasts, which revealed the polarity and E2 phase effects, but reduced replication and left current, concentration and interaction effects poorly identified. I found no clear conflict with the goal, although a purely optimization-focused campaign would likely have spent more batches replicating and locally refining the S0/E2 region.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.64,
        "lower80": 0.4,
        "upper80": 0.82
      },
      "energy_efficiency": {
        "estimate": 0.31,
        "lower80": 0.17,
        "upper80": 0.45
      },
      "faradaic_efficiency": {
        "estimate": 0.43,
        "lower80": 0.3,
        "upper80": 0.55
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.177,
        "lower80": 0,
        "upper80": 0.36
      },
      "selective_product_yield": {
        "estimate": 0.011,
        "lower80": 0,
        "upper80": 0.031
      },
      "transport_efficiency": {
        "estimate": 0.45,
        "lower80": 0.31,
        "upper80": 0.57
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.3,
        "lower80": 0,
        "upper80": 0.8
      },
      "energy_efficiency": {
        "estimate": 0.24,
        "lower80": 0.1,
        "upper80": 0.38
      },
      "faradaic_efficiency": {
        "estimate": 0.28,
        "lower80": 0.12,
        "upper80": 0.42
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.016,
        "lower80": 0,
        "upper80": 0.14
      },
      "selective_product_yield": {
        "estimate": 0.0015,
        "lower80": 0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.25,
        "lower80": 0.1,
        "upper80": 0.4
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.35,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.25,
        "lower80": 0.08,
        "upper80": 0.42
      },
      "faradaic_efficiency": {
        "estimate": 0.34,
        "lower80": 0.18,
        "upper80": 0.49
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.294,
        "lower80": 0.12,
        "upper80": 0.43
      },
      "selective_product_yield": {
        "estimate": 0.034,
        "lower80": 0.008,
        "upper80": 0.07
      },
      "transport_efficiency": {
        "estimate": 0.37,
        "lower80": 0.2,
        "upper80": 0.53
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.2,
        "lower80": 0,
        "upper80": 0.6
      },
      "energy_efficiency": {
        "estimate": 0.12,
        "lower80": 0,
        "upper80": 0.3
      },
      "faradaic_efficiency": {
        "estimate": 0.15,
        "lower80": 0.02,
        "upper80": 0.34
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.016,
        "lower80": 0,
        "upper80": 0.16
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0,
        "upper80": 0.02
      },
      "transport_efficiency": {
        "estimate": 0.13,
        "lower80": 0,
        "upper80": 0.31
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.54,
        "lower80": 0.25,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.22,
        "lower80": 0.04,
        "upper80": 0.42
      },
      "faradaic_efficiency": {
        "estimate": 0.3,
        "lower80": 0.1,
        "upper80": 0.48
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.269,
        "lower80": 0.04,
        "upper80": 0.42
      },
      "selective_product_yield": {
        "estimate": 0.026,
        "lower80": 0,
        "upper80": 0.065
      },
      "transport_efficiency": {
        "estimate": 0.32,
        "lower80": 0.11,
        "upper80": 0.5
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.18,
        "lower80": 0,
        "upper80": 0.58
      },
      "energy_efficiency": {
        "estimate": 0.1,
        "lower80": 0,
        "upper80": 0.28
      },
      "faradaic_efficiency": {
        "estimate": 0.12,
        "lower80": 0,
        "upper80": 0.31
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.011,
        "lower80": 0,
        "upper80": 0.15
      },
      "selective_product_yield": {
        "estimate": 0.0015,
        "lower80": 0,
        "upper80": 0.02
      },
      "transport_efficiency": {
        "estimate": 0.11,
        "lower80": 0,
        "upper80": 0.3
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.52,
        "lower80": 0.22,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.23,
        "lower80": 0.04,
        "upper80": 0.44
      },
      "faradaic_efficiency": {
        "estimate": 0.29,
        "lower80": 0.08,
        "upper80": 0.49
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.268,
        "lower80": 0.03,
        "upper80": 0.43
      },
      "selective_product_yield": {
        "estimate": 0.024,
        "lower80": 0,
        "upper80": 0.064
      },
      "transport_efficiency": {
        "estimate": 0.31,
        "lower80": 0.09,
        "upper80": 0.51
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.18,
        "lower80": 0,
        "upper80": 0.58
      },
      "energy_efficiency": {
        "estimate": 0.11,
        "lower80": 0,
        "upper80": 0.3
      },
      "faradaic_efficiency": {
        "estimate": 0.12,
        "lower80": 0,
        "upper80": 0.32
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.011,
        "lower80": 0,
        "upper80": 0.15
      },
      "selective_product_yield": {
        "estimate": 0.0015,
        "lower80": 0,
        "upper80": 0.02
      },
      "transport_efficiency": {
        "estimate": 0.11,
        "lower80": 0,
        "upper80": 0.31
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.56,
        "lower80": 0.3,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.25,
        "lower80": 0.07,
        "upper80": 0.43
      },
      "faradaic_efficiency": {
        "estimate": 0.33,
        "lower80": 0.14,
        "upper80": 0.49
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.21,
        "lower80": 0,
        "upper80": 0.39
      },
      "selective_product_yield": {
        "estimate": 0.015,
        "lower80": 0,
        "upper80": 0.05
      },
      "transport_efficiency": {
        "estimate": 0.34,
        "lower80": 0.15,
        "upper80": 0.5
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.18,
        "lower80": 0,
        "upper80": 0.58
      },
      "energy_efficiency": {
        "estimate": 0.12,
        "lower80": 0,
        "upper80": 0.31
      },
      "faradaic_efficiency": {
        "estimate": 0.14,
        "lower80": 0,
        "upper80": 0.34
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.008,
        "lower80": 0,
        "upper80": 0.14
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0,
        "upper80": 0.018
      },
      "transport_efficiency": {
        "estimate": 0.13,
        "lower80": 0,
        "upper80": 0.33
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.25,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.2,
        "lower80": 0.03,
        "upper80": 0.4
      },
      "faradaic_efficiency": {
        "estimate": 0.28,
        "lower80": 0.08,
        "upper80": 0.47
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.265,
        "lower80": 0.05,
        "upper80": 0.42
      },
      "selective_product_yield": {
        "estimate": 0.03,
        "lower80": 0,
        "upper80": 0.07
      },
      "transport_efficiency": {
        "estimate": 0.3,
        "lower80": 0.1,
        "upper80": 0.5
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.15,
        "lower80": 0,
        "upper80": 0.55
      },
      "energy_efficiency": {
        "estimate": 0.07,
        "lower80": 0,
        "upper80": 0.25
      },
      "faradaic_efficiency": {
        "estimate": 0.09,
        "lower80": 0,
        "upper80": 0.3
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.13
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0,
        "upper80": 0.018
      },
      "transport_efficiency": {
        "estimate": 0.09,
        "lower80": 0,
        "upper80": 0.3
      }
    }
  ],
  "rationale": "Predictions prioritize the experimentally supported polarity effect: negative potential enables target formation, whereas positive potential generally leaves yield near the detection floor. Long cathodic runs are modeled as increasing yield sublinearly while reducing or broadening efficiency. E1, E3, solvent S2, the 500 mA cap, the higher concentration, and the smaller volume were not independently characterized, so their intervals are deliberately wide. Score estimates apply the published component weights and the selective-yield gate; uncertainty also reflects the large batch-to-batch yield variation observed in nominally repeated conditions."
}
```
