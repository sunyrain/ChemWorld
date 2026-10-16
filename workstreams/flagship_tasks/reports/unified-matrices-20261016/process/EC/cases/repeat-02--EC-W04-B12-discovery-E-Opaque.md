# repeat-02/EC-W04-B12-discovery-E-Opaque

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-02\EC-W04-B12-discovery-E-Opaque\participant\discovery-E-Opaque

## 同期笔记

### v1 · 公开事件 0

# Electrochemical hypothesis notebook

## Pre-experiment expectations

**H1 [tentative].** At fixed loading (0.020 mol reagent in 0.050 L solvent), conversion should rise with electrolysis time and delivered charge until substrate limitation or degradation; current caps may matter only when they bind delivered current.

**H2 [tentative].** Product formation is polarity-specific: one potential sign should outperform the opposite sign, while excessive absolute potential may reduce selectivity or energy efficiency.

**H3 [tentative].** Anonymous solvent and electrolyte identities may affect transport, ohmic efficiency, pH/precipitation, and hence yield. A factorial-like screen followed by local contrasts should separate these effects.

Plan: hold loading fixed across 12 independent batches; first map polarity, magnitude, time, current cap and materials, then use later batches for targeted repeats/segmented tests. One UV-vis or pH observation per batch will be used where informative. A result would weaken H1 if longer time lowers conversion without increased degradation; H2 if signs are symmetric within uncertainty; H3 if material contrasts are small and not repeatable.

### v2 · 公开事件 42

# Electrochemical hypothesis notebook

## Findings after six batches (fixed 0.020 mol / 0.050 L)

**H1 [supported in tested S0/E0 scope].** At −0.5 V and 100 mA cap, extending electrolysis from 600 to 1800 to 3600 s increased final conversion (about 0.012, 0.020, 0.050) and selective yield (about 0.014, 0.018, 0.045), while selectivity and efficiency metrics were broadly stable (final assays: runner-operation-0035, -0028, -0042). This supports a time/charge-controlled regime over 600–3600 s, though single runs and assay noise limit precision. Prediction: still longer operation should further increase conversion until saturation/degradation.

**H2 [supported qualitatively, nonmonotone magnitude].** Potential sign and magnitude matter strongly. +1 V gave higher measured conversion but extremely low selective yield (runner-operation-0007) relative to −1 V (runner-operation-0014); at negative polarity, −2 V collapsed efficiency/yield (runner-operation-0021), whereas −0.5 V was substantially better (runner-operation-0028). Thus the productive window appears mildly negative rather than maximal |V|. Exact sign effect remains partly confounded by assay noise and the unusual yield/conversion relationship.

**H3 [unresolved].** Solvent/electrolyte effects remain untested. Next: screen all anonymous material pairs at −0.5 V and longer duration, plus current-cap and repeat/segmentation contrasts.

**Confound.** Precipitation signal is near 1 throughout S0/E0, so selective-product yield may incorporate a phase/precipitation behavior not captured simply by conversion × selectivity. The reported conversion and selective yield should be modeled as related but not assumed algebraically identical.

### v3 · 公开事件 84

# Electrochemical hypothesis notebook

## Final source-stage account (fixed 0.020 mol reagent / 0.050 L solvent)

**H1 [supported in S0/E0, −0.5 V, 100 mA scope].** From 600→1800→3600 s, final conversion rose roughly 0.012→0.020→0.050 and selective yield 0.014→0.018→0.045, with broadly stable selectivity/efficiency (runner-operation-0035, -0028, -0042). This is consistent with accumulated charge/time controlling extent before saturation. A 20 mA cap at 3600 s produced lower selective yield (~0.018) and a conversion estimate clipped at zero (runner-operation-0084), supporting a binding-current effect qualitatively, but the conversion/yield inconsistency makes its magnitude uncertain.

**H2 [supported qualitatively; quantitative form unresolved].** Productive behavior is polarity- and magnitude-specific. +1 V had higher conversion but nearly zero selective yield (runner-operation-0007); −1 V improved yield (runner-operation-0014); −2 V collapsed efficiencies and yielded no detected selective product (runner-operation-0021). The best tested window was mildly negative, −0.5 V (runner-operation-0028 and -0042). This suggests a desired reduction pathway competing with nonproductive oxidation at positive bias and inefficient/side-reaction-dominated behavior at excessive negative bias. Only single runs were available, so exact thresholds remain unresolved.

**H3 [supported for material dependence, identities opaque].** At −0.5 V, 100 mA, 3600 s, changing solvent from S0 altered conversion, yield, transport and risk: S1 and S2 were worse in selective yield than S0; S3 had comparable yield but lower conversion/faradaic/transport efficiency (runner-operation-0049, -0056, -0063 versus -0042). With S0, E1 and E2 increased conversion but reduced selective yield relative to E0, and progressively suppressed precipitation (runner-operation-0070, -0077 versus -0042). Thus electrolyte influences speciation/phase behavior separately from charge-transfer extent. E2's near-zero precipitation and lower pH-normalized value are strong qualitative contrasts, but causal interpretation is not identifiable from anonymous labels.

**Working predictive model.** Within a fixed material/potential regime, conversion initially increases with effective charge, approximately with time when the current cap is nonbinding; a lower cap reduces extent. Selective yield depends additionally on a window function of signed potential and material-dependent selectivity/phase factors. Efficiency peaks near mild negative bias and worsens at |V| that is too large. Extrapolation beyond tested ranges should saturate rather than remain linear.

**Limitations and suspended claims.** No technical repeats were run; final assay noise, clipping, and occasional yield/conversion inconsistency prevent exact kinetic constants or algebraic yield = conversion×selectivity claims. E3 was not tested. The near-unit precipitation signal in most conditions is associated with, but not demonstrably causal for, yield. Batch 6 is the operating recommendation because it gave the best observed score and highest selective yield among a coherent S0/E0 time series, not because optimization was the primary objective.

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
    "cost": 0.28571999073028564,
    "electrochemical_conversion": 0.032129980623722076,
    "electrochemical_selectivity": 1.0,
    "energy_efficiency": 0.5409024953842163,
    "faradaic_efficiency": 0.5415942668914795,
    "ohmic_efficiency": 0.9572166204452515,
    "pH_normalized": 0.23443032801151276,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.20992566645145416,
    "selective_product_yield": 0.009760934859514236,
    "transport_efficiency": 0.5128905177116394
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
    "electrochemical_conversion": 0.011924302205443382,
    "electrochemical_selectivity": 0.6610745787620544,
    "energy_efficiency": 0.278411328792572,
    "faradaic_efficiency": 0.427999347448349,
    "ohmic_efficiency": 0.9660544395446777,
    "pH_normalized": 0.2317349761724472,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.3227793574333191,
    "selective_product_yield": 0.021980460733175278,
    "transport_efficiency": 0.454256147146225
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
    "cost": 0.28644001483917236,
    "electrochemical_conversion": 0.007179038133472204,
    "electrochemical_selectivity": 0.506598711013794,
    "energy_efficiency": 0.06802051514387131,
    "faradaic_efficiency": 0.24533773958683014,
    "ohmic_efficiency": 0.9696498513221741,
    "pH_normalized": 0.2324499785900116,
    "precipitation_signal": 0.9863388538360596,
    "safety_risk": 0.05933958664536476,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.2618946433067322
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
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -0.5
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
    "cost": 0.2853600084781647,
    "electrochemical_conversion": 0.020332247018814087,
    "electrochemical_selectivity": 0.69989413022995,
    "energy_efficiency": 0.6401931643486023,
    "faradaic_efficiency": 0.5453222393989563,
    "ohmic_efficiency": 0.9313426613807678,
    "pH_normalized": 0.23175939917564392,
    "precipitation_signal": 0.9870871305465698,
    "safety_risk": 0.05933958664536476,
    "score": 0.36709198355674744,
    "selective_product_yield": 0.01835993118584156,
    "transport_efficiency": 0.5138346552848816
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
    "cost": 0.28512001037597656,
    "electrochemical_conversion": 0.011553158052265644,
    "electrochemical_selectivity": 0.7350095510482788,
    "energy_efficiency": 0.6516550779342651,
    "faradaic_efficiency": 0.5323100686073303,
    "ohmic_efficiency": 0.930776834487915,
    "pH_normalized": 0.23672018945217133,
    "precipitation_signal": 0.9864134788513184,
    "safety_risk": 0.05933958664536476,
    "score": 0.29026079177856445,
    "selective_product_yield": 0.014369865879416466,
    "transport_efficiency": 0.5218006372451782
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
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -0.5
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
    "cost": 0.28571999073028564,
    "electrochemical_conversion": 0.049801331013441086,
    "electrochemical_selectivity": 0.7328161597251892,
    "energy_efficiency": 0.6742552518844604,
    "faradaic_efficiency": 0.534893810749054,
    "ohmic_efficiency": 0.9326335787773132,
    "pH_normalized": 0.2334442436695099,
    "precipitation_signal": 0.997043788433075,
    "safety_risk": 0.05933958664536476,
    "score": 0.4193759858608246,
    "selective_product_yield": 0.04505382105708122,
    "transport_efficiency": 0.5102105140686035
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
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -0.5
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
    "cost": 0.29872000217437744,
    "electrochemical_conversion": 0.052484799176454544,
    "electrochemical_selectivity": 0.6729387640953064,
    "energy_efficiency": 0.6165085434913635,
    "faradaic_efficiency": 0.4538329541683197,
    "ohmic_efficiency": 0.944599449634552,
    "pH_normalized": 0.2358059585094452,
    "precipitation_signal": 0.9775494933128357,
    "safety_risk": 0.08273958414793015,
    "score": 0.3851374685764313,
    "selective_product_yield": 0.03573549911379814,
    "transport_efficiency": 0.4572333097457886
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
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -0.5
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
    "cost": 0.3307200074195862,
    "electrochemical_conversion": 0.03752542659640312,
    "electrochemical_selectivity": 0.6664106845855713,
    "energy_efficiency": 0.6026403903961182,
    "faradaic_efficiency": 0.464063435792923,
    "ohmic_efficiency": 0.9204974174499512,
    "pH_normalized": 0.24695418775081635,
    "precipitation_signal": 0.9850548505783081,
    "safety_risk": 0.10073958337306976,
    "score": 0.14404213428497314,
    "selective_product_yield": 0.007754191756248474,
    "transport_efficiency": 0.45756807923316956
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
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -0.5
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
    "cost": 0.3177199959754944,
    "electrochemical_conversion": 0.030750634148716927,
    "electrochemical_selectivity": 0.6662580966949463,
    "energy_efficiency": 0.6569899916648865,
    "faradaic_efficiency": 0.34139689803123474,
    "ohmic_efficiency": 0.9558468461036682,
    "pH_normalized": 0.24071985483169556,
    "precipitation_signal": 0.9949686527252197,
    "safety_risk": 0.11333958804607391,
    "score": 0.3670044243335724,
    "selective_product_yield": 0.03927982226014137,
    "transport_efficiency": 0.3622281849384308
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
      "current_mA": 100,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -0.5
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
    "cost": 0.28571999073028564,
    "electrochemical_conversion": 0.05926027148962021,
    "electrochemical_selectivity": 0.6712120771408081,
    "energy_efficiency": 0.6180010437965393,
    "faradaic_efficiency": 0.4795578718185425,
    "ohmic_efficiency": 0.9143089056015015,
    "pH_normalized": 0.20043565332889557,
    "precipitation_signal": 0.8446682095527649,
    "safety_risk": 0.05933958664536476,
    "score": 0.3859463334083557,
    "selective_product_yield": 0.02618648111820221,
    "transport_efficiency": 0.4809074401855469
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
      "solvent": 0,
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -0.5
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
    "cost": 0.2787199914455414,
    "electrochemical_conversion": 0.05762360244989395,
    "electrochemical_selectivity": 0.676092267036438,
    "energy_efficiency": 0.6399761438369751,
    "faradaic_efficiency": 0.47574833035469055,
    "ohmic_efficiency": 0.918401300907135,
    "pH_normalized": 0.15807457268238068,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.05933958664536476,
    "score": 0.3915793299674988,
    "selective_product_yield": 0.03183991461992264,
    "transport_efficiency": 0.48292824625968933
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
      "current_mA": 20,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -0.5
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
    "cost": 0.28514400124549866,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.7068493366241455,
    "energy_efficiency": 0.7058799862861633,
    "faradaic_efficiency": 0.49561405181884766,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.23196634650230408,
    "precipitation_signal": 0.9932199120521545,
    "safety_risk": 0.05933958664536476,
    "score": 0.37200817465782166,
    "selective_product_yield": 0.018212011083960533,
    "transport_efficiency": 0.5168389678001404
  }
}
```

## K1 封存报告

Mechanistic account

I treat this as a signed-potential electrochemical network in which charge delivery controls reaction extent, while potential, solvent, and electrolyte determine how much of that extent reaches or retains the assayed target. The public channels should not be interpreted as direct species inventories: in several batches selective-product yield exceeded the reported conversion, and batch 12 reported zero conversion while retaining nonzero yield. I therefore regard conversion, selectivity, and yield as independently noisy or differently normalized observables, not quantities constrained exactly by yield = conversion × selectivity.

Experimental basis

All batches used 0.020 mol reagent in 0.050 L solvent. Unless noted otherwise, the current cap was 100 mA.

• Batch 1: S0/E0, +1.0 V, 1800 s. Conversion 0.0321, electrochemical selectivity 1.000, selective yield 0.00976, faradaic efficiency 0.5416, transport efficiency 0.5129, energy efficiency 0.5409, score 0.2099.
• Batch 2: S0/E0, −1.0 V, 1800 s. Conversion 0.0119, selectivity 0.6611, yield 0.0220, faradaic efficiency 0.4280, transport efficiency 0.4543, energy efficiency 0.2784, score 0.3228.
• Batch 3: S0/E0, −2.0 V, 1800 s. Conversion 0.00718, selectivity 0.5066, yield clipped to zero, faradaic efficiency 0.2453, transport efficiency 0.2619, energy efficiency 0.0680, score zero.
• Batch 4: S0/E0, −0.5 V, 1800 s. Conversion 0.0203, selectivity 0.6999, yield 0.0184, faradaic efficiency 0.5453, transport efficiency 0.5138, energy efficiency 0.6402, score 0.3671.
• Batch 5: S0/E0, −0.5 V, 600 s. Conversion 0.0116, selectivity 0.7350, yield 0.0144, score 0.2903.
• Batch 6: S0/E0, −0.5 V, 3600 s. Conversion 0.0498, selectivity 0.7328, yield 0.0451, faradaic efficiency 0.5349, transport efficiency 0.5102, energy efficiency 0.6743, score 0.4194. This was the sealed recommendation.
• Batches 7–9 changed only the solvent from the batch-6 recipe. S1 gave conversion 0.0525 and yield 0.0357; S2 gave 0.0375 and 0.00775; S3 gave 0.0308 and 0.0393. Their scores were 0.3851, 0.1440, and 0.3670, respectively.
• Batches 10–11 changed only the electrolyte from the batch-6 recipe. E1 gave conversion 0.0593, yield 0.0262, pH-normalized 0.2004, and precipitation signal 0.8447. E2 gave conversion 0.0576, yield 0.0318, pH-normalized 0.1581, and precipitation signal 0.00524. Their scores were 0.3859 and 0.3916. For comparison, batch 6 with E0 had pH-normalized 0.2334 and precipitation signal 0.9970.
• Batch 12 repeated the batch-6 materials, potential, and duration but lowered the current cap to 20 mA. It gave conversion clipped to zero, yield 0.0182, selectivity 0.7068, energy efficiency 0.7059, and score 0.3720.

1. Charge/time controls the extent within a fixed regime

The cleanest internal series is batches 5, 4, and 6: S0/E0 at −0.5 V and 100 mA for 600, 1800, and 3600 s. Conversion increased from 0.0116 to 0.0203 to 0.0498, while selective yield increased from 0.0144 to 0.0184 to 0.0451. Selectivity remained approximately 0.70–0.74, and faradaic, transport, ohmic, and energy efficiencies did not deteriorate with duration. This suggests that these durations remain largely in an extent-limited regime rather than a severe product-degradation regime.

A useful conceptual equation is

Q_eff = I_eff(V, solvent, electrolyte, state) × t,

X(t) ≈ X_max[1 − exp(−k_Q Q_eff)],

where X is latent reacted fraction and I_eff is the actual productive current, bounded by the configured current cap. At low extent this reduces approximately to X ∝ I_eff t. I do not claim fitted values for k_Q or X_max because only three durations were tested and there were no repeats.

Batch 12 supports current limitation qualitatively. Reducing the cap from 100 to 20 mA at 3600 s lowered selective yield from 0.0451 to 0.0182. Its conversion channel was clipped at zero, which is inconsistent with its nonzero product signal and should not be read literally as absence of reaction. The defensible conclusion is that the lower cap reduced productive extent; its exact factor is unidentifiable.

2. There is a signed-potential window, not a monotonic |V| benefit

The potential series changed the initial explanation substantially. A simple assumption that larger |V| accelerates the desired reaction is contradicted by batch 3: at −2.0 V, energy efficiency fell to 0.068, faradaic efficiency to 0.245, transport efficiency to 0.262, and target yield to zero. Mildly negative −0.5 V was much better across the balanced metrics.

Positive and negative potentials also appear to access different reaction networks. Batch 1 at +1.0 V showed conversion 0.0321 and reported selectivity 1.0, yet only 0.00976 selective yield. Batch 2 at −1.0 V showed lower conversion but higher yield. Thus the positive-potential conversion channel may include nonproductive oxidation, a target-losing follow-up process, or a normalization/phase effect that the selectivity channel does not capture. The data do not identify which alternative is correct.

My mechanistic interpretation is a competition among at least three pathways:

R + e− → P or a target-forming precursor at mildly negative potential;
R → oxidized/nonproductive material at positive potential;
R/P + excessive cathodic drive → side products, solvent/electrolyte reduction, or transport-limited loss at strongly negative potential.

A compact phenomenological form would be

r_target = k_red(V)·a_R·η_transport·η_F,

r_side = k_ox(V)·a_R + k_over(V)·a_R + k_deg(V)·a_P,

where k_red is largest in a mildly negative window, k_ox grows on the positive side, and k_over grows when the potential is too negative. The efficiency collapse in batch 3 is evidence for k_over or an equivalent parasitic-current term. These are functional relationships, not identified elementary steps.

3. Solvent couples transport, selectivity, safety, and product recovery

The solvent screen shows that solvent effects cannot be represented only as a change in bulk reaction rate. Relative to S0 in batch 6:

• S1 preserved or slightly increased measured conversion (0.0525) but lowered yield to 0.0357, selectivity to 0.6729, faradaic efficiency to 0.4538, and transport efficiency to 0.4572.
• S2 lowered both conversion and selectivity and nearly eliminated selective yield (0.00775). It also had the highest pH-normalized value, 0.2470, among these comparisons.
• S3 produced lower conversion and much lower faradaic/transport efficiencies (0.3414/0.3622) but retained a relatively high yield, 0.0393.

Safety risk also rose from 0.0593 for S0 to 0.0827, 0.1007, and 0.1133 for S1, S2, and S3. This is an observed solvent-associated coupling, although the anonymous labels prevent chemical interpretation.

These results imply separate solvent factors for charge transfer, mass transport, side reactions, and target retention or assay recovery. A reasonable model is

Y_obs ≈ X_latent × S_electrochemical × f_recovery(solvent, electrolyte, pH, phase) + measurement error,

with f_recovery not assumed to equal one. S3 is especially informative: its relatively high yield despite weaker conversion and charge-efficiency channels indicates either unusually favorable recovery/retention or correlated measurement differences. S2 likely has an unfavorable combination of selectivity and recovery, not merely a slower rate.

4. Electrolyte strongly controls pH/phase behavior independently of conversion

The electrolyte comparison is the clearest evidence for a coupled speciation or phase process. At the batch-6 conditions, E1 and E2 increased measured conversion from 0.0498 to 0.0593 and 0.0576, but reduced selective yield from 0.0451 to 0.0262 and 0.0318. Meanwhile pH-normalized fell from 0.2334 with E0 to 0.2004 with E1 and 0.1581 with E2. The precipitation signal fell from 0.9970 to 0.8447 and then essentially zero, 0.00524.

I therefore infer that electrolyte affects at least two coupled subsystems:

(1) electrochemical charge transfer and substrate disappearance, which were not harmed and may have improved with E1/E2;
(2) proton balance, ion pairing, solubility, precipitation, or phase partitioning, which changed dramatically and altered recovered target yield.

One possible process is

P_solution ⇌ P_assayed/precipitated,

with an equilibrium fraction f_phase = g(electrolyte, pH, solvent). E0 strongly favors the high-precipitation state, whereas E2 strongly favors the low-precipitation state. The association between high precipitation and high batch-6 yield is suggestive but not sufficient to prove that precipitation causes higher yield. Precipitation could protect product from further reaction, improve assay recovery, or merely co-vary with another electrolyte property. Conversely, E2 may retain product in a form less strongly represented by the selective-yield channel.

5. Efficiency structure

Ohmic efficiency remained high in all reported batches, approximately 0.91–1.00, so bulk ohmic loss was generally not the principal limitation. The larger changes occurred in faradaic and transport efficiencies. In particular, the −2.0 V condition simultaneously depressed faradaic, transport, and energy efficiency, consistent with parasitic current plus transport limitation. Solvent S3 also depressed faradaic and transport efficiency despite high ohmic efficiency, demonstrating that a conductive cell can still use charge unproductively or deliver reactant poorly to the active interface.

A useful decomposition is

I_productive = I_applied × η_ohmic × η_transport × η_F × w(V),

where w(V) is a signed-potential target-window factor. Energy efficiency then carries an additional voltage penalty, so increasing |V| can lower energy efficiency even if total current rises. This describes the observed pattern but should not be taken as a uniquely identified factorization; the public efficiency channels may share latent causes.

6. Scope and predictive implications

Within S0/E0 and the tested loading, I expect increasing time at −0.5 V and a nonbinding current cap initially to raise conversion and selective yield, eventually approaching saturation. Extrapolating the roughly increasing 600–3600 s series indefinitely would be unjustified: substrate depletion, product degradation, or transport changes should ultimately bend the curve. A current cap well below 100 mA is expected to reduce extent at fixed time. Potentials much more negative than −0.5 V are expected to sacrifice energy and faradaic efficiency; positive potential is expected to alter the product network and give poor recovered target even when a conversion-like signal rises.

S0/E0 is the best-supported operating combination, not necessarily the universal optimum. S3 may have favorable recovery but worse transport and higher risk. E1/E2 may improve disappearance of starting material while changing pH and suppressing the phase state associated with high recovered yield. E3 was never tested, so nothing specific can be inferred about it.

7. Unidentifiable factors and plausible alternatives

No technical replicate was performed. Consequently, small differences—especially among selectivities near 0.67–0.73 or efficiencies differing by only a few hundredths—cannot confidently be separated from assay noise and process variability. Large contrasts such as batch 3 versus batch 4, or the E0 versus E2 precipitation signal, are more persuasive.

The actual current trajectory was not observed, so the 100 mA setting could be a cap rather than the delivered current. Electrode area, temperature trajectory, electrode kinetics, mass-transfer coefficients, chemical identities, speciation, and concentrations after sampling were not measured or disclosed. Elementary rate constants and reaction orders are therefore not identifiable.

The yield/conversion inconsistencies admit several alternatives: different normalization bases; independent channel noise and clipping; target already present in a distinct assay pool; phase-dependent sampling; or conversion and yield representing different latent windows. I favor independent noisy observables coupled through reaction and recovery because that explanation accommodates all batches without forcing impossible mass-balance identities.

Likewise, the electrolyte–precipitation relationship could reflect direct solubility control, pH-mediated speciation, ionic-strength effects, or an assay visibility change. The campaign establishes a strong coupling but does not distinguish these mechanisms.

Overall conclusion

The simplest account consistent with the campaign is a charge-limited target-forming reduction operating in a mildly negative potential window, embedded in competing oxidation/over-reduction pathways and coupled to material-dependent transport, proton/speciation balance, and phase recovery. Time and available current set latent extent; signed potential sets pathway competition and energetic cost; solvent controls transport, selectivity, recovery, and risk; electrolyte strongly controls pH/precipitation and thus the relationship between conversion and recovered target. Batch 6 was recommended because it combined the strongest observed selective yield (0.0451) and highest score (0.4194) in a coherent S0/E0 duration series, while remaining inside the favorable −0.5 V regime.

## K2 封存报告

1. Claims and laws assessed

No instance-specific prior mechanism or nominal material-property dossier was supplied. The solvent and electrolyte labels were explicitly opaque. My initial claims were therefore self-developed rather than updates to a supplied instance prior.

• Time/charge law: supported within a limited scope. Before observing the results, I proposed that reaction extent would rise with electrolysis time or productive charge until saturation or degradation. At S0/E0, −0.5 V, and a 100 mA cap, batches 5, 4, and 6 increased from 600 to 1800 to 3600 s. Conversion rose from 0.0116 to 0.0203 to 0.0498, and selective yield from 0.0144 to 0.0184 to 0.0451, without a corresponding efficiency collapse. This changed my judgment from tentative to supported for that operating region. Batch 12, using a 20 mA rather than 100 mA cap for 3600 s, produced only 0.0182 yield versus 0.0451 in batch 6, qualitatively supporting a current-limited component. Its zero-clipped conversion prevents a reliable quantitative current law. Saturation and long-time degradation remained untested.

• Monotonic absolute-potential law: contradicted. A naive law in which greater |V| simply accelerates useful conversion was rejected by batch 3. At −2.0 V it gave zero detected selective yield, energy efficiency 0.0680, faradaic efficiency 0.2453, and transport efficiency 0.2619, all far below the −0.5 V result in batch 4. This evidence led to the signed-potential-window account.

• Polarity-specific pathways: qualitatively supported. Batch 1 at +1.0 V showed conversion 0.0321 and reported selectivity 1.0 but only 0.00976 selective yield. Batch 2 at −1.0 V had lower conversion, 0.0119, but higher yield, 0.0220. Together with batches 3–4, this favored different productive and nonproductive pathways on the two potential signs rather than a single rate controlled by |V|. The elementary identities of those pathways remained untested.

• Material independence: contradicted. Solvent changes in batches 7–9 altered yield, transport, faradaic efficiency, and safety risk relative to batch 6. S2 was particularly unfavorable: batch 8 yielded 0.00775 compared with 0.0451 for S0 in batch 6. Electrolyte changes were also consequential. Batches 10 and 11 had somewhat higher conversion than batch 6 but lower yield, while precipitation fell from 0.997 with E0 to 0.845 with E1 and 0.00524 with E2. This evidence changed my view from a generic material-effect hypothesis to a more specific coupling among electrolyte, pH/speciation, phase behavior, and recovered product.

• Exact identity yield = conversion × selectivity: contradicted as an observation law. Several batches violated it numerically; batch 12 even combined zero-clipped conversion with nonzero yield. I therefore treated these as independently noisy or differently normalized channels. That does not disprove a latent mass balance, but it rules out imposing the public point estimates as an exact algebraic identity.

• Precipitation protects or improves recovery of target: suggestive but untested causally. The E0/E1/E2 comparison is consistent with this explanation, but electrolyte changes many properties simultaneously. Direct causation was never isolated.

2. One additional discriminating experiment

I would run S0 with E2 at −0.5 V, a 100 mA cap, and 7200 s, using the same 0.020 mol/0.050 L loading as the campaign, followed by the final assay. This extends batch 11 while preserving its low-precipitation electrolyte and can distinguish my leading phase/recovery explanation from the alternative that batch 11 merely had insufficient electrolysis time.

If conversion increased substantially but precipitation remained near zero and selective yield remained well below an equivalently extended E0 expectation, I would strengthen the claim that electrolyte-dependent speciation or recovery decouples substrate disappearance from recovered target. If yield rose approximately in proportion to time and approached the E0 trajectory despite continued low precipitation, I would weaken the proposed protective/recovery role of precipitation and favor a primarily kinetic explanation. If both conversion and yield plateaued, I would infer an electrolyte-specific electrochemical or equilibrium ceiling. If precipitation rose during the longer treatment along with yield, the experiment would not separate time from phase causation; it would instead show that phase state itself evolves with charge. Because the original campaign had no repeats, any isolated result would remain provisional.

3. Unused evidence, unreliable outputs, and goal effects

The raw spectral traces and characterization artifacts were not analyzed; interpretation relied on processed estimates. Intermediate UV–visible and pH measurements were used mainly as diagnostics rather than fitted jointly with final assays. Cost was not mechanistically informative, and safety risk was only partly incorporated through the solvent comparison. No electrode-area, actual-current trajectory, temperature, concentration profile, or species-resolved evidence was available. E3 was never tested, and no technical replicate was performed. The design also did not independently vary reagent concentration, total volume, or order of addition.

The least reliable sealed predictions are Q07–Q08 because E3 had no campaign evidence; Q11–Q12 because 500 mA and 7200 s required large extrapolations; and the long positive-potential cases because the campaign only tested +1.0 V for 1800 s. Predictions at the new 0.012 mol/0.025 L loading also extrapolate beyond the sole campaign loading. The score predictions inherit additional uncertainty from the selective-yield gate, especially when predicted yield is near 0.02.

Batch 6 is the most defensible recommendation among observed batches because it had the highest measured score and yield and belonged to a coherent duration series. It is nevertheless less reliable as a universal optimum because it was not replicated, potentials around −0.5 V were not finely mapped, E3 was absent, and times beyond 3600 s were not tested.

The assigned goal emphasized explanatory and predictive research, with public optimization score secondary. That encouraged polarity, duration, solvent, electrolyte, and current-cap contrasts rather than repeatedly optimizing the best recipe. The benefit was broader mechanistic coverage; the cost was the absence of replication, incomplete factorial separation, and sparse local optimization. There was no clear conflict requiring unsafe or scientifically uninformative work, but allocating at least one batch to a repeat would have improved uncertainty assessment.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.7,
        "lower80": 0.55,
        "upper80": 0.82
      },
      "energy_efficiency": {
        "estimate": 0.48,
        "lower80": 0.3,
        "upper80": 0.63
      },
      "faradaic_efficiency": {
        "estimate": 0.49,
        "lower80": 0.38,
        "upper80": 0.6
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.3125,
        "lower80": 0.15,
        "upper80": 0.42
      },
      "selective_product_yield": {
        "estimate": 0.017,
        "lower80": 0.003,
        "upper80": 0.035
      },
      "transport_efficiency": {
        "estimate": 0.49,
        "lower80": 0.38,
        "upper80": 0.6
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.93,
        "lower80": 0.72,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.58,
        "lower80": 0.4,
        "upper80": 0.72
      },
      "faradaic_efficiency": {
        "estimate": 0.54,
        "lower80": 0.4,
        "upper80": 0.67
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.1378,
        "lower80": 0.0,
        "upper80": 0.3
      },
      "selective_product_yield": {
        "estimate": 0.0065,
        "lower80": 0.0,
        "upper80": 0.022
      },
      "transport_efficiency": {
        "estimate": 0.52,
        "lower80": 0.4,
        "upper80": 0.64
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.68,
        "lower80": 0.52,
        "upper80": 0.81
      },
      "energy_efficiency": {
        "estimate": 0.46,
        "lower80": 0.26,
        "upper80": 0.62
      },
      "faradaic_efficiency": {
        "estimate": 0.48,
        "lower80": 0.35,
        "upper80": 0.6
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.3846,
        "lower80": 0.28,
        "upper80": 0.5
      },
      "selective_product_yield": {
        "estimate": 0.075,
        "lower80": 0.035,
        "upper80": 0.14
      },
      "transport_efficiency": {
        "estimate": 0.48,
        "lower80": 0.35,
        "upper80": 0.6
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.9,
        "lower80": 0.62,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.56,
        "lower80": 0.33,
        "upper80": 0.72
      },
      "faradaic_efficiency": {
        "estimate": 0.54,
        "lower80": 0.36,
        "upper80": 0.69
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.3002,
        "lower80": 0.08,
        "upper80": 0.46
      },
      "selective_product_yield": {
        "estimate": 0.014,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "transport_efficiency": {
        "estimate": 0.52,
        "lower80": 0.34,
        "upper80": 0.67
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.64,
        "lower80": 0.45,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.42,
        "lower80": 0.22,
        "upper80": 0.58
      },
      "faradaic_efficiency": {
        "estimate": 0.43,
        "lower80": 0.3,
        "upper80": 0.56
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.3537,
        "lower80": 0.22,
        "upper80": 0.47
      },
      "selective_product_yield": {
        "estimate": 0.045,
        "lower80": 0.015,
        "upper80": 0.1
      },
      "transport_efficiency": {
        "estimate": 0.45,
        "lower80": 0.31,
        "upper80": 0.57
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.88,
        "lower80": 0.57,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.48,
        "lower80": 0.25,
        "upper80": 0.67
      },
      "faradaic_efficiency": {
        "estimate": 0.48,
        "lower80": 0.3,
        "upper80": 0.64
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.2196,
        "lower80": 0.03,
        "upper80": 0.4
      },
      "selective_product_yield": {
        "estimate": 0.011,
        "lower80": 0.0,
        "upper80": 0.043
      },
      "transport_efficiency": {
        "estimate": 0.46,
        "lower80": 0.28,
        "upper80": 0.62
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.66,
        "lower80": 0.34,
        "upper80": 0.87
      },
      "energy_efficiency": {
        "estimate": 0.45,
        "lower80": 0.17,
        "upper80": 0.68
      },
      "faradaic_efficiency": {
        "estimate": 0.46,
        "lower80": 0.24,
        "upper80": 0.66
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.3686,
        "lower80": 0.15,
        "upper80": 0.55
      },
      "selective_product_yield": {
        "estimate": 0.055,
        "lower80": 0.008,
        "upper80": 0.15
      },
      "transport_efficiency": {
        "estimate": 0.47,
        "lower80": 0.24,
        "upper80": 0.68
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.88,
        "lower80": 0.48,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.5,
        "lower80": 0.19,
        "upper80": 0.75
      },
      "faradaic_efficiency": {
        "estimate": 0.5,
        "lower80": 0.23,
        "upper80": 0.72
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.2441,
        "lower80": 0.02,
        "upper80": 0.48
      },
      "selective_product_yield": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "transport_efficiency": {
        "estimate": 0.48,
        "lower80": 0.21,
        "upper80": 0.72
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.4,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.42,
        "lower80": 0.2,
        "upper80": 0.6
      },
      "faradaic_efficiency": {
        "estimate": 0.42,
        "lower80": 0.27,
        "upper80": 0.57
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.2177,
        "lower80": 0.02,
        "upper80": 0.38
      },
      "selective_product_yield": {
        "estimate": 0.013,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "transport_efficiency": {
        "estimate": 0.43,
        "lower80": 0.27,
        "upper80": 0.58
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.82,
        "lower80": 0.48,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.49,
        "lower80": 0.23,
        "upper80": 0.7
      },
      "faradaic_efficiency": {
        "estimate": 0.45,
        "lower80": 0.24,
        "upper80": 0.63
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.0762,
        "lower80": 0.0,
        "upper80": 0.28
      },
      "selective_product_yield": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.028
      },
      "transport_efficiency": {
        "estimate": 0.44,
        "lower80": 0.23,
        "upper80": 0.62
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.38,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.34,
        "lower80": 0.12,
        "upper80": 0.55
      },
      "faradaic_efficiency": {
        "estimate": 0.42,
        "lower80": 0.24,
        "upper80": 0.58
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.3968,
        "lower80": 0.24,
        "upper80": 0.55
      },
      "selective_product_yield": {
        "estimate": 0.22,
        "lower80": 0.08,
        "upper80": 0.42
      },
      "transport_efficiency": {
        "estimate": 0.4,
        "lower80": 0.2,
        "upper80": 0.57
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.75,
        "lower80": 0.4,
        "upper80": 0.96
      },
      "energy_efficiency": {
        "estimate": 0.36,
        "lower80": 0.12,
        "upper80": 0.59
      },
      "faradaic_efficiency": {
        "estimate": 0.44,
        "lower80": 0.22,
        "upper80": 0.63
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.3742,
        "lower80": 0.12,
        "upper80": 0.55
      },
      "selective_product_yield": {
        "estimate": 0.035,
        "lower80": 0.002,
        "upper80": 0.12
      },
      "transport_efficiency": {
        "estimate": 0.4,
        "lower80": 0.18,
        "upper80": 0.6
      }
    }
  ],
  "rationale": "Predictions extrapolate the fixed-loading campaign's time, signed-potential, material, and current-cap contrasts. Mild negative bias is treated as the productive window; positive bias retains favorable efficiency channels but gives substantially less recovered target. Longer duration raises extent, E1 reduces recovered yield relative to E0, S2 is strongly unfavorable, and untested E3 receives especially wide intervals. The 500 mA cases allow greater extent but lower transport and energy efficiency. Score estimates use the published weighted components and the selective-yield gate. Intervals are deliberately broad because loading changed, 7200 s and 500 mA require extrapolation, E3 was never observed, and the campaign had no technical replicates."
}
```
