# repeat-03/EC-W04-B12-discovery-E-Opaque

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-03\EC-W04-B12-discovery-E-Opaque\participant\discovery-E-Opaque

## 同期笔记

### v1 · 公开事件 0

# Electrochemical hypothesis notebook

## Prior expectations (before physical experiments)
H1 [tentative]: Product formation requires a nonzero applied potential and electrolysis time; its sign and magnitude may produce a peaked response rather than simple monotonicity because excessive drive can reduce selectivity/efficiency. Test by spanning both signs and durations at fixed loading/medium.

H2 [tentative]: Anonymous solvent and electrolyte identities can independently affect transport, ohmic efficiency, and selectivity. Test with controlled material swaps near a promising electrical condition.

H3 [tentative]: Delivered response may saturate with the nonnegative current cap; compare caps under otherwise fixed conditions. A cap effect is unresolved unless differences exceed assay noise or repeat.

Design principle: use 12 independent batches as a compact factorial/response-surface screen, keeping several controlled pairs and at least one repeat. Final assays are authoritative; intermediate UV-vis/pH snapshots will probe time evolution or medium effects.

### v2 · 公开事件 32

# Electrochemical hypothesis notebook

## Prior expectations
H1: product formation may show sign/magnitude and time dependence with overdrive penalties. H2: media affect transport/ohmic/selectivity. H3: current-cap saturation is possible.

## Evidence update after batches 1–4
H1 [supported for polarity-dependent efficiencies; product-yield response unresolved]: At fixed 0.02 mol/0.05 L, S0/E0, 100 mA cap and 300 s, intermediate UV-vis differs strongly with potential. At −1 V the mid-course faradaic/transport estimates were about 0.44/0.43 (event runner-operation-0021), while +2 V gave values near zero (runner-operation-0013); +1 V gave high mid-course efficiencies (runner-operation-0029). Final conversion and selective yield were at/near the lower boundary in all four assays (runner-operation-0008, -0016, -0024, -0032), so 300 s is likely too short to resolve kinetics at this loading. Differences in final tiny yields may be assay noise/edge clipping, not established product formation.

The positive +2 V condition appears electrically unproductive under this scope, opposing any simple monotonic drive model. −2 V also had poor mid-course energy efficiency. A moderate-potential window is therefore more plausible.

Next testable consequence: extending moderate +1 V and −1 V electrolysis should lift conversion/yield above the boundary if low response is chiefly kinetic; failure even at long time would instead favor a missing-medium/current requirement. I will prioritize 1200–3600 s and then controlled current/material swaps.

### v3 · 公开事件 80

# Electrochemical hypothesis notebook

## Current account after batches 1–10
H1 [supported in S0/E0 at 0.02 mol in 0.05 L]: Response depends strongly on potential sign/magnitude and elapsed electrolysis. The +2 V extreme is inefficient (events runner-operation-0013/-0016); moderate potentials are productive. Extending 300→1200→3600 s at +1 V raises final conversion/yield from boundary-level to roughly 0.012/0.016 and 0.027/0.034 (runner-operation-0032, -0040, -0048), consistent with slow accumulation, though assay noise makes exact short-time intercept uncertain. At 3600 s, −1 V trades higher conversion/faradaic transport for lower selectivity (runner-operation-0056), whereas +1 V is near-maximally selective (runner-operation-0048).

H4 [supported, moderate positive optimum]: +0.5 V at 100 mA cap and 3600 s combines high selectivity with substantially higher energy efficiency (~0.79), producing the best score so far (runner-operation-0064). This rejects a monotonic improvement with positive magnitude. Potential likely controls a selectivity/overpotential tradeoff.

H3 [supported for a pronounced cap effect, functional form unresolved]: At +1 V/3600 s, a 10 mA cap gives very high intermediate efficiencies but low final conversion (runner-operation-0069/-0072), consistent with charge limitation. A 500 mA cap collapses faradaic/transport/selectivity (runner-operation-0077/-0080), consistent with parasitic current/overdrive. Thus current_mA is a cap with an intermediate useful regime, not a guaranteed beneficial dose. Exact optimum is not identified and the comparisons are unreplicated.

H2 [unresolved]: media have not yet been varied. Final two controlled batches will separately swap solvent S0→S1 and electrolyte E0→E1 at +0.5 V, 100 mA, 3600 s. Material conclusions will remain provisional without repeats.

### v4 · 公开事件 96

# Electrochemical hypothesis notebook — final source-stage record

## Empirical account and scope
H1 [supported in the tested loading]: At 0.02 mol reagent in 0.05 L, conversion/product accumulation is slow over 300–3600 s and potential response is nonmonotonic. Moderate potentials outperform ±2 V in useful efficiency. Negative moderate bias favors conversion/faradaic throughput but sacrifices selectivity; moderate positive bias favors selectivity and energy efficiency (key assays runner-operation-0048, -0056, -0064). A predictive model should therefore include separate potential-dependent activation and parasitic/overdrive terms, not merely |V| or total time.

H3 [supported qualitatively, not quantitatively calibrated]: current cap creates a regime tradeoff. A 10 mA cap is charge/throughput limited despite favorable efficiencies, while 500 mA is dominated by low-selectivity parasitic behavior; 100 mA is substantially better in these conditions (runner-operation-0064, -0072, -0080). Because current_mA is only a cap, delivered charge cannot be inferred directly. Intermediate and final efficiency differences within a batch also warn against treating one snapshot as time invariant.

H2 [supported for material dependence, with single-comparison limitation]: Relative to S0/E0 at +0.5 V, 100 mA, 3600 s (runner-operation-0064), solvent S1 raises conversion, faradaic/transport efficiencies, and selective yield while reducing selectivity somewhat (runner-operation-0088). Electrolyte E1 also raises faradaic/transport response and selective yield, changes pH/precipitation markedly, and lowers selectivity (runner-operation-0096). These are numerical controlled-pair differences larger than typical declared assay noise for several channels, but neither swap was replicated; interactions and other S/E levels remain unresolved.

## Provisional predictive structure
For fixed loading/volume, treat yield as conversion × a sign/material-dependent selectivity factor, with conversion increasing and tending toward saturation in time. Let useful electrical efficiency have a broad optimum in moderate potential/current-cap space and fall at extreme potential or cap. Material factors separately modify transport/faradaic efficiency and selectivity. This structure predicts: (i) longer electrolysis raises conversion most clearly before saturation; (ii) sign reversal changes selectivity and efficiency even at equal |V|; (iii) S1 or E1 can improve throughput at moderate positive bias but may not maximize selectivity; (iv) extrapolation beyond tested 300–3600 s and untested material interactions is uncertain.

## Recommendation decision
Batch 11 is the balanced operating recommendation: S1/E0, +0.5 V, 100 mA cap, 3600 s at the fixed loading. It achieved the highest observed balanced score (~0.519) and strong yield/efficiency without approaching the safety limit (runner-operation-0088). Batch 12 has a numerically higher selective-yield estimate and lower risk but a slightly lower balanced score and lower selectivity; either difference is unreplicated. The recommendation would change if repeats establish batch 12’s yield advantage as robust or if the objective prioritizes yield/safety over the published balanced metric.

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
      "potential_V": -2
    },
    {
      "duration_s": 150,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "duration_s": 150,
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
    "electrochemical_conversion": 0.011259781196713448,
    "electrochemical_selectivity": 0.5458994507789612,
    "energy_efficiency": 0.07589691132307053,
    "faradaic_efficiency": 0.3135564923286438,
    "ohmic_efficiency": 0.9740383625030518,
    "pH_normalized": 0.2344122976064682,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.2848527431488037
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
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 2
    },
    {
      "duration_s": 150,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "duration_s": 150,
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
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.010023192502558231,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.0,
    "ohmic_efficiency": 0.982876181602478,
    "pH_normalized": 0.23171694576740265,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.03836137056350708,
    "selective_product_yield": 0.00897990819066763,
    "transport_efficiency": 0.02610676921904087
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
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1
    },
    {
      "duration_s": 150,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "duration_s": 150,
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
    "cost": 0.3031199872493744,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.6581524610519409,
    "energy_efficiency": 0.2705806493759155,
    "faradaic_efficiency": 0.42657074332237244,
    "ohmic_efficiency": 0.952828049659729,
    "pH_normalized": 0.23243194818496704,
    "precipitation_signal": 0.9863442182540894,
    "safety_risk": 0.05933958664536476,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.4431276321411133
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
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 150,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "duration_s": 150,
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
    "cost": 0.3031199872493744,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.9613004326820374,
    "energy_efficiency": 0.23188450932502747,
    "faradaic_efficiency": 0.29021430015563965,
    "ohmic_efficiency": 0.9649862051010132,
    "pH_normalized": 0.23174136877059937,
    "precipitation_signal": 0.9870924353599548,
    "safety_risk": 0.05933958664536476,
    "score": 0.04440912976861,
    "selective_product_yield": 0.0027955439873039722,
    "transport_efficiency": 0.2587267756462097
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
      "volume_L": 0.05
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
      "duration_s": 600,
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
    "cost": 0.30347999930381775,
    "electrochemical_conversion": 0.012480034492909908,
    "electrochemical_selectivity": 0.9963550567626953,
    "energy_efficiency": 0.24371002614498138,
    "faradaic_efficiency": 0.27375829219818115,
    "ohmic_efficiency": 0.9644203782081604,
    "pH_normalized": 0.23670215904712677,
    "precipitation_signal": 0.9864188432693481,
    "safety_risk": 0.05933958664536476,
    "score": 0.26963362097740173,
    "selective_product_yield": 0.01641545444726944,
    "transport_efficiency": 0.26324883103370667
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
      "duration_s": 1800,
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
    "cost": 0.3044399917125702,
    "electrochemical_conversion": 0.026667172089219093,
    "electrochemical_selectivity": 0.9939978122711182,
    "energy_efficiency": 0.2671627104282379,
    "faradaic_efficiency": 0.28876468539237976,
    "ohmic_efficiency": 0.9662771224975586,
    "pH_normalized": 0.23342621326446533,
    "precipitation_signal": 0.9970491528511047,
    "safety_risk": 0.05933958664536476,
    "score": 0.3402865529060364,
    "selective_product_yield": 0.03361225873231888,
    "transport_efficiency": 0.26408135890960693
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
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "duration_s": 1800,
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
    "cost": 0.3044399917125702,
    "electrochemical_conversion": 0.05402994900941849,
    "electrochemical_selectivity": 0.6720671653747559,
    "energy_efficiency": 0.27430349588394165,
    "faradaic_efficiency": 0.45989131927490234,
    "ohmic_efficiency": 0.9978386759757996,
    "pH_normalized": 0.2324407994747162,
    "precipitation_signal": 0.9820912480354309,
    "safety_risk": 0.05933958664536476,
    "score": 0.33952170610427856,
    "selective_product_yield": 0.03606633469462395,
    "transport_efficiency": 0.4632916748523712
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
      "solvent": 0,
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 0.5
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
      "duration_s": 1800,
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
    "cost": 0.30371999740600586,
    "electrochemical_conversion": 0.04361509531736374,
    "electrochemical_selectivity": 0.9378023743629456,
    "energy_efficiency": 0.7908305525779724,
    "faradaic_efficiency": 0.5188862681388855,
    "ohmic_efficiency": 0.9494911432266235,
    "pH_normalized": 0.23074333369731903,
    "precipitation_signal": 0.9949641227722168,
    "safety_risk": 0.05933958664536476,
    "score": 0.4603509306907654,
    "selective_product_yield": 0.024099180474877357,
    "transport_efficiency": 0.5123909115791321
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
      "volume_L": 0.05
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
      "duration_s": 1800,
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
    "cost": 0.30314400792121887,
    "electrochemical_conversion": 0.003600894706323743,
    "electrochemical_selectivity": 0.9805969595909119,
    "energy_efficiency": 0.5339303612709045,
    "faradaic_efficiency": 0.4981641173362732,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.232757106423378,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.4257231056690216,
    "selective_product_yield": 0.021682316437363625,
    "transport_efficiency": 0.5189954042434692
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
      "volume_L": 0.05
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
      "duration_s": 1800,
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
    "cost": 0.3102000057697296,
    "electrochemical_conversion": 0.016369987279176712,
    "electrochemical_selectivity": 0.019033947959542274,
    "energy_efficiency": 0.014645654708147049,
    "faradaic_efficiency": 0.009028017520904541,
    "ohmic_efficiency": 0.820952296257019,
    "pH_normalized": 0.23044297099113464,
    "precipitation_signal": 0.992000162601471,
    "safety_risk": 0.05933958664536476,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.010377603583037853
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
      "solvent": 1,
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 0.5
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
      "duration_s": 1800,
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
    "cost": 0.3237200081348419,
    "electrochemical_conversion": 0.084535613656044,
    "electrochemical_selectivity": 0.8678299188613892,
    "energy_efficiency": 0.8116961121559143,
    "faradaic_efficiency": 0.7538946270942688,
    "ohmic_efficiency": 0.9157654643058777,
    "pH_normalized": 0.23477515578269958,
    "precipitation_signal": 0.9953573942184448,
    "safety_risk": 0.08273958414793015,
    "score": 0.5191243290901184,
    "selective_product_yield": 0.06301939487457275,
    "transport_efficiency": 0.7610745429992676
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
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 0.5
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
      "duration_s": 1800,
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
    "cost": 0.30371999740600586,
    "electrochemical_conversion": 0.05832590162754059,
    "electrochemical_selectivity": 0.8296146988868713,
    "energy_efficiency": 0.773223876953125,
    "faradaic_efficiency": 0.7567282915115356,
    "ohmic_efficiency": 0.9411357641220093,
    "pH_normalized": 0.20192290842533112,
    "precipitation_signal": 0.8460460305213928,
    "safety_risk": 0.05933958664536476,
    "score": 0.5122030377388,
    "selective_product_yield": 0.07350365817546844,
    "transport_efficiency": 0.7779532670974731
  }
}
```

## K1 封存报告

Mechanism report

1. Experimental scope

All 12 batches used 0.020 mol of the anonymous limiting reagent in 0.050 L of solvent, corresponding to a nominal initial concentration of 0.40 mol L^-1. Each electrolysis was divided into two equal time segments around one intermediate measurement. Thus, comparisons primarily isolate potential, total duration, current cap, solvent identity, or electrolyte identity at one loading and volume. The reported current is a cap, not a measurement of delivered current.

The final assays are noisy, independently calibrated channel estimates. In particular, selective_product_yield is not numerically constrained to equal measured conversion multiplied by measured selectivity. Several responses were close to zero, where clipping and noise are consequential. I therefore treat broad, repeated trends as more credible than exact identities among low-valued channels.

2. Proposed process picture

I interpret the system as a competition among three coupled electrochemical processes:

(a) productive electron transfer that consumes reactant;
(b) potential-, current-, and medium-dependent selection between target and non-target pathways; and
(c) parasitic current or degradation that becomes important at excessive electrical drive.

A useful minimal model would contain an unobserved delivered current

I_del(t) = min[I_cap, I_polar(V, solvent, electrolyte, state(t))],

and productive charge

Q_prod(t) = integral FE(V, I_del, solvent, electrolyte, state) * I_del dt.

Conversion could then be approximated over the tested regime by a saturating law such as

X(t) = X_max * {1 - exp[-k_Q Q_prod(t)/n0]},

where n0 is initial reagent amount. Target formation would additionally depend on a selectivity function

S_target = f(V, I_del, solvent, electrolyte, conversion, time),

with latent target yield approximately X*S_target in the underlying process, although the separately noisy public assay channels need not obey that identity exactly. Transport efficiency modifies the current that reaches productive sites, ohmic efficiency accounts for resistive loss, and faradaic efficiency partitions delivered charge between chemical and parasitic reactions. A schematic energy-efficiency relation is

eta_E proportional to (useful chemical output)/(integral |V I_del| dt),

so raising potential or the current cap can increase rate while simultaneously lowering eta_E through resistive and parasitic losses.

The evidence favors broad optima in both potential and current cap rather than monotonic improvement with electrical drive. Potential sign also changes the balance of pathways, not merely their common rate.

3. Evidence that formed the account

Potential screen, batches 1–4:

At S0/E0, a 100 mA cap, and 300 s total electrolysis, both extreme potentials were poor. Batch 1 at -2.0 V ended with conversion 0.0113, selectivity 0.5459, zero reported selective yield, energy efficiency 0.0759, and faradaic efficiency 0.3136. Batch 2 at +2.0 V had conversion at the lower boundary, selectivity 0.0100, faradaic efficiency at the lower boundary, and only 0.0261 transport efficiency. Its halfway UV-vis estimate likewise placed faradaic efficiency at zero. This was the clearest evidence against a simple model in which increasing |V| always increases useful reaction.

Moderate potentials were electrically more favorable. At the halfway measurement, batch 3 at -1.0 V had faradaic and transport efficiencies of about 0.440 and 0.427. Batch 4 at +1.0 V had corresponding values of about 0.535 and 0.490 and energy efficiency about 0.511. Final product responses after only 300 s were nevertheless at or near the assay boundary: batch 3 reported zero conversion and yield, while batch 4 reported zero conversion and yield 0.00280. These observations shifted my explanation from “wrong potential alone” to “moderate potential plus slow accumulation.”

Time and polarity, batches 4–7:

At +1.0 V, S0/E0, and a 100 mA cap, increasing total duration produced a systematic rise in the final low-level product channels. Batch 4 at 300 s gave conversion at the lower boundary and yield 0.00280; batch 5 at 1200 s gave conversion 0.0125 and yield 0.0164; batch 6 at 3600 s gave conversion 0.0267 and yield 0.0336. Scores rose from 0.0444 to 0.2696 and 0.3403. The exact short-time values are uncertain, but the ordered change supports time-dependent accumulation in this range.

Batch 7 tested -1.0 V for 3600 s. Relative to batch 6 at +1.0 V, it showed higher conversion (0.0540 versus 0.0267), faradaic efficiency (0.4599 versus 0.2888), and transport efficiency (0.4633 versus 0.2641), but lower selectivity (0.6721 versus 0.9940). Its yield, 0.0361, and score, 0.3395, were close to those of batch 6. This controlled sign comparison suggests that negative moderate bias favors throughput, whereas positive moderate bias favors target selectivity. It is not adequately described by a function of |V| alone.

Moderate positive potential, batch 8:

Batch 8 used +0.5 V, S0/E0, 100 mA, and 3600 s. It achieved conversion 0.0436, selectivity 0.9378, energy efficiency 0.7908, faradaic efficiency 0.5189, transport efficiency 0.5124, and score 0.4604. Compared with batch 6 at +1.0 V and otherwise matching conditions, +0.5 V retained high selectivity while greatly improving energy, faradaic, and transport efficiencies. This established a moderate positive operating window and reinforced the proposed overpotential penalty at larger positive bias. It does not establish that exactly +0.5 V is the optimum because intermediate potentials were not sampled.

Current-cap tests, batches 6, 9, and 10:

At +1.0 V, S0/E0, and 3600 s, changing the cap caused a strongly nonmonotonic response. With a 10 mA cap, batch 9 had low conversion, 0.00360, despite selectivity 0.9806. Its final energy, faradaic, and transport efficiencies were approximately 0.534, 0.498, and 0.519. The halfway UV-vis estimates were near unity, consistent with a clean but throughput-limited regime.

At the opposite extreme, batch 10 used a 500 mA cap. Its faradaic efficiency fell to 0.00903, transport efficiency to 0.0104, selectivity to 0.0190, energy efficiency to 0.0146, and selective yield to the lower boundary. This is much more than a small rate change and is consistent with parasitic current, electrode-side competition, or another high-current loss process.

The 100 mA condition in batch 6 lay between these regimes and gave the useful product response noted above. The evidence therefore supports an intermediate current-cap window: too low limits charge throughput, while too high diverts current away from the selective process. Because delivered current was not measured, I cannot determine whether the 100 and 500 mA caps were continuously reached or identify a conventional current density.

Medium effects, batches 8, 11, and 12:

Batch 11 changed only solvent S0 to S1 relative to batch 8, retaining E0, +0.5 V, 100 mA, and 3600 s. Conversion rose from 0.0436 to 0.0845, selective yield from 0.0241 to 0.0630, faradaic efficiency from 0.5189 to 0.7539, and transport efficiency from 0.5124 to 0.7611. Energy efficiency remained high and increased numerically from 0.7908 to 0.8117. Selectivity decreased from 0.9378 to 0.8678, and ohmic efficiency decreased from 0.9495 to 0.9158. The changes in several channels are larger than their declared assay noise scales, so S1 plausibly improves charge transport or productive kinetics while slightly weakening target discrimination or increasing resistive loss. Batch 11 had the highest observed balanced score, 0.5191. Its safety risk, 0.0827, was higher than S0’s 0.0593 but far below the 0.65 limit.

Batch 12 instead retained S0 and changed electrolyte E0 to E1 at the batch-8 electrical condition. It gave conversion 0.0583, selectivity 0.8296, selective yield 0.0735, energy efficiency 0.7732, faradaic efficiency 0.7567, transport efficiency 0.7780, and score 0.5122. Thus E1 also appears to improve productive charge use and transport while reducing selectivity relative to E0. Unlike the solvent swap, E1 changed pH_normalized from 0.2307 in batch 8 to 0.2019 and precipitation_signal from 0.9950 to 0.8460. This suggests that electrolyte identity couples to the acid/base or phase/precipitation state, which could in turn influence charge transfer and selectivity. That causal direction is conjectural: the measurements establish association, not whether pH or precipitation is the mediator.

The reported selective yield of batch 12 exceeds its reported conversion. I interpret this as a consequence of independent noisy estimator channels at small absolute signal, rather than literal mass creation. It is a warning not to derive precise stoichiometry from these processed values.

4. Role of pH, precipitation, and ohmic efficiency

For S0/E0 batches, pH_normalized remained narrowly near 0.23 despite large electrical changes. Precipitation_signal was also normally near saturation, approximately 0.98–1.00. Consequently, those two channels cannot explain the potential and current effects within that medium: they show too little resolved variation and may be saturated. E1 in batch 12 produced the only marked joint decrease in both pH_normalized and precipitation_signal, so these variables may be useful signatures of electrolyte-controlled speciation or phase behavior.

Ohmic efficiency was generally high, often roughly 0.92–1.00, except under the 500 mA cap, where it fell to about 0.821. The much larger collapse in faradaic efficiency, transport efficiency, and selectivity at 500 mA implies that ordinary ohmic loss alone is insufficient to explain the high-cap failure. A parasitic electrochemical pathway or strong interfacial/transport limitation is more plausible.

5. What is observed versus extrapolated

Observed within the tested domain:

• Useful response is slow over 300–3600 s at this loading.
• Moderate potentials outperform ±2 V in the measured efficiency channels.
• Potential sign changes the conversion/selectivity balance at equal magnitude.
• A 500 mA cap is severely detrimental at +1.0 V, while 10 mA is throughput limited.
• S1 and E1 each improve several throughput-related channels relative to the S0/E0 reference at +0.5 V, but each reduces measured selectivity.
• Every tested batch remained below the safety limit.

Reasonable interpolation, but not directly established:

• Conversion probably continues as a saturating function of productive charge rather than increasing linearly forever.
• Potential and current cap likely have broad internal optima near the moderate tested region.
• S1 probably changes mobility, interfacial kinetics, or solvation; E1 probably changes conductivity/speciation and phase behavior.

Unsupported extrapolation:

• Performance beyond 3600 s, at other reagent concentrations or volumes, or under continuous rather than segmented operation is unknown.
• The exact optimum potential or cap cannot be inferred from the sparse grid.
• No conclusion can be made about solvents S2/S3, electrolytes E2/E3, or the S1/E1 combination.
• Real chemical identities, electrode reactions, electron stoichiometry, electrode area, temperature dependence, and actual delivered current are hidden or unmeasured.

6. Unidentifiable factors and alternatives

There were no independent repeats. Consequently, material effects are supported by controlled numerical contrasts but their repeatability and interactions remain unresolved. Instrument noise is especially important for conversion and yield near zero. Midpoint and final measurements also differ within some batches; these could reflect genuine state evolution, different instrument calibrations/noise, or both.

Several mechanistic alternatives remain compatible with the evidence:

• The high-current collapse could arise from a competing faradaic reaction, electrode passivation, local depletion, or concentration polarization. The available channels cannot distinguish them.
• The potential-sign effect could represent different electrode reactions, asymmetric activation barriers, or sign-dependent production of a mediator. Hidden species mapping prevents assignment.
• The S1 improvement could result from conductivity, reactant activity, mass transfer, or suppression of a parasitic reaction rather than a single transport mechanism.
• E1’s pH and precipitation changes might cause its efficiency differences, or all three effects might be parallel consequences of a hidden speciation change.
• The nearly saturated precipitation signal in most batches may represent a real phase constraint or merely a channel with little resolution in this region.

A more identifiable model would require delivered-current or charge data, time-series assays at several points, repeat batches, a denser potential/current grid, and crossed solvent–electrolyte combinations. Those measurements were not made, so they are proposed discriminating tests rather than evidence.

7. Overall account

Within the studied 0.40 mol L^-1 system, target production is governed by productive charge delivery multiplied by a separately voltage- and medium-dependent selectivity. Electrolysis duration increases accumulated conversion, but useful charge efficiency is maximized only in a moderate electrical window. Negative moderate potential promotes throughput at the expense of selectivity; moderate positive potential gives better target discrimination and energy efficiency. Very large positive potential or a very high current cap activates severe losses, whereas a very low cap limits total conversion. Solvent and electrolyte tune transport/faradaic efficiency and probably speciation, with S1 and E1 both improving throughput but reducing selectivity relative to S0/E0. This account explains the principal controlled comparisons, while leaving the chemical identities and precise elementary mechanism unidentifiable.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific prior, nominal property dossier, or supplied mechanistic law was provided. The solvent and electrolyte labels were explicitly anonymous, so my starting claims were self-developed hypotheses rather than adaptations of a supplied instance prior.

Supported within the tested scope:

• The law that useful response depends nonmonotonically on potential was supported. At fixed S0/E0, 100 mA, and 300 s, +2 V in batch 2 produced essentially zero faradaic efficiency and very low transport efficiency, whereas moderate ±1 V in batches 3 and 4 gave much stronger intermediate efficiencies. Batch 8 at +0.5 V and 3600 s had energy efficiency 0.791 and score 0.460, outperforming the corresponding +1 V batch 6 on those measures. These results changed my view from a generic “more drive may accelerate reaction” prior to a broad moderate-potential optimum with overdrive losses.

• Slow time-dependent accumulation was supported over 300–3600 s. At +1 V, the reported yield increased from 0.0028 in batch 4 at 300 s to 0.0164 in batch 5 at 1200 s and 0.0336 in batch 6 at 3600 s. This evidence changed my judgment after batches 1–4: the nearly absent early product was not adequately explained by potential choice alone. Saturation at longer times, however, was not tested.

• Potential sign controls pathway balance, rather than only rate, was supported. At 3600 s, batch 7 at -1 V had higher conversion and faradaic/transport efficiencies than batch 6 at +1 V, but substantially lower selectivity: 0.672 versus 0.994. This contradicted any law depending only on |V|.

• An intermediate current-cap regime was supported qualitatively. Batch 9 at 10 mA was efficient but had low conversion, consistent with throughput limitation. Batch 10 at 500 mA showed a collapse in selectivity, faradaic efficiency, transport efficiency, and yield. Batch 6 at 100 mA was much more productive. This changed H3 from an unresolved cap effect into a supported regime tradeoff.

• Medium dependence was supported, although only by unreplicated controlled contrasts. Relative to S0/E0 in batch 8, solvent S1 in batch 11 increased conversion, yield, faradaic efficiency, and transport efficiency while reducing selectivity. Electrolyte E1 in batch 12 produced a similar throughput/selectivity tradeoff and also changed pH_normalized and precipitation_signal. Thus the claim that solvent and electrolyte can separately modify the response was supported.

Contradicted or weakened:

• A monotonic “larger potential or current is better” law was contradicted by batches 2 and 10.

• A sign-symmetric law based on |V| was contradicted by batches 6 and 7.

• A simple exact observational identity selective_product_yield = conversion × selectivity was contradicted as a law for the processed assay outputs. Batch 12, for example, reported yield 0.0735 and conversion 0.0583. I interpret this as independent noisy estimator channels, not a physical violation of mass balance.

Untested or unresolved:

• The proposed exponential or saturating conversion law was not identified because no duration exceeded 3600 s and there were no time-series final assays.

• The elementary cause of high-current failure—parasitic faradaic chemistry, passivation, local depletion, or concentration polarization—remained unidentifiable.

• The suggestion that E1 acts through acid/base or precipitation-state changes was only an association from batch 12, not a tested causal law.

• Solvents S2/S3, electrolytes E2/E3, solvent–electrolyte interactions, concentration effects, delivered current, and electrode-scale parameters were untested.

2. One additional discriminating experiment

I would run one batch at the batch-8 conditions—0.020 mol reagent, 0.050 L S0, E0, +0.5 V, and 3600 s—but raise the current cap from 100 to 500 mA. I would include the same midpoint UV-vis measurement and final assay. This comparison would distinguish my leading cap-driven parasitic-loss explanation from the alternative that batch 10 failed mainly because +1 V and 500 mA interact as a combined overpotential condition.

If the +0.5 V/500 mA batch also showed near-zero faradaic and transport efficiency, low selectivity, and negligible yield, I would strengthen the claim that the high cap itself accesses a broadly parasitic or transport-limited regime. If it instead resembled batch 8 despite the higher cap, I would reject a general 500 mA penalty and favor a potential–current interaction or the possibility that the cap is only reached under sufficiently large polarization. An intermediate result—higher conversion but lower efficiency than batch 8—would support a continuous rate-versus-parasitic tradeoff rather than a sharp regime boundary. Because it would still be a single batch, a surprising result would revise but not conclusively settle the mechanism.

3. Unused evidence, weak predictions, and goal effects

I relied mainly on processed estimates and did not fit the raw UV-visible spectra. Cost was not mechanistically informative and was used only implicitly. Safety risk constrained acceptability but varied little except for S1, so it could not identify reaction pathways. The near-saturated precipitation readings and narrowly clustered pH readings in most S0/E0 batches were largely unused because they had little resolving power. Intermediate UV-visible observations were used qualitatively, but I did not combine them quantitatively with final assays because the instruments have different calibration and noise contracts. No replicate evidence existed to estimate batch-to-batch variability.

The least reliable blind predictions are Q07–Q08, which use entirely untested E3, and Q09–Q10, which use entirely untested S2. Q11–Q12 are also weak because they extrapolate the single observed 500 mA failure to different potentials, twice the longest studied duration, and a different reagent amount and volume. All 7200 s predictions extrapolate beyond the observed time domain. Q01–Q02 are less extreme in duration but their predicted yields lie near the score gate at 0.02, making their scores especially sensitive to small assay or model errors. The action order in the prediction batches also differed from my campaign, and no evidence established whether order is irrelevant.

The batch-11 recommendation is less secure than its rank suggests. It had the highest observed balanced score, but the S1 effect was measured only once. Batch 12 had a numerically higher selective-yield estimate and lower safety risk, so a yield- or safety-focused objective, or successful replication, could change the choice.

The assigned discovery goal affected evidence collection: I used the 12 batches to span potential sign and magnitude, duration, current cap, solvent, and electrolyte rather than concentrating on replication or local optimization. That broadened the explanatory evidence but weakened precision, interaction identification, and confidence in the final recommendation. There was no clear conflict with the balanced operating objective—the selected batch also had the highest observed score—but a purely optimization-focused campaign would likely have replicated batches 8, 11, and 12 and refined the +0.5 V/100 mA neighborhood instead of spending batches on extreme or mechanistically diagnostic conditions.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.72,
        "lower80": 0.58,
        "upper80": 0.84
      },
      "energy_efficiency": {
        "estimate": 0.4,
        "lower80": 0.25,
        "upper80": 0.56
      },
      "faradaic_efficiency": {
        "estimate": 0.46,
        "lower80": 0.34,
        "upper80": 0.58
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.15,
        "lower80": 0.02,
        "upper80": 0.34
      },
      "selective_product_yield": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.025
      },
      "transport_efficiency": {
        "estimate": 0.47,
        "lower80": 0.34,
        "upper80": 0.6
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.96,
        "lower80": 0.87,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.57,
        "lower80": 0.38,
        "upper80": 0.74
      },
      "faradaic_efficiency": {
        "estimate": 0.42,
        "lower80": 0.28,
        "upper80": 0.56
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.27,
        "lower80": 0.06,
        "upper80": 0.48
      },
      "selective_product_yield": {
        "estimate": 0.013,
        "lower80": 0.0,
        "upper80": 0.032
      },
      "transport_efficiency": {
        "estimate": 0.4,
        "lower80": 0.26,
        "upper80": 0.55
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.72,
        "lower80": 0.58,
        "upper80": 0.84
      },
      "energy_efficiency": {
        "estimate": 0.42,
        "lower80": 0.26,
        "upper80": 0.59
      },
      "faradaic_efficiency": {
        "estimate": 0.5,
        "lower80": 0.38,
        "upper80": 0.63
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.42,
        "lower80": 0.33,
        "upper80": 0.54
      },
      "selective_product_yield": {
        "estimate": 0.115,
        "lower80": 0.06,
        "upper80": 0.2
      },
      "transport_efficiency": {
        "estimate": 0.51,
        "lower80": 0.38,
        "upper80": 0.65
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.96,
        "lower80": 0.87,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.58,
        "lower80": 0.39,
        "upper80": 0.76
      },
      "faradaic_efficiency": {
        "estimate": 0.43,
        "lower80": 0.29,
        "upper80": 0.58
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.46,
        "lower80": 0.36,
        "upper80": 0.58
      },
      "selective_product_yield": {
        "estimate": 0.115,
        "lower80": 0.06,
        "upper80": 0.2
      },
      "transport_efficiency": {
        "estimate": 0.42,
        "lower80": 0.27,
        "upper80": 0.58
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.61,
        "lower80": 0.35,
        "upper80": 0.81
      },
      "energy_efficiency": {
        "estimate": 0.52,
        "lower80": 0.28,
        "upper80": 0.73
      },
      "faradaic_efficiency": {
        "estimate": 0.68,
        "lower80": 0.43,
        "upper80": 0.86
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.49,
        "lower80": 0.32,
        "upper80": 0.66
      },
      "selective_product_yield": {
        "estimate": 0.17,
        "lower80": 0.06,
        "upper80": 0.34
      },
      "transport_efficiency": {
        "estimate": 0.7,
        "lower80": 0.45,
        "upper80": 0.88
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.82,
        "lower80": 0.6,
        "upper80": 0.95
      },
      "energy_efficiency": {
        "estimate": 0.6,
        "lower80": 0.37,
        "upper80": 0.79
      },
      "faradaic_efficiency": {
        "estimate": 0.66,
        "lower80": 0.42,
        "upper80": 0.84
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.55,
        "lower80": 0.39,
        "upper80": 0.7
      },
      "selective_product_yield": {
        "estimate": 0.2,
        "lower80": 0.08,
        "upper80": 0.38
      },
      "transport_efficiency": {
        "estimate": 0.7,
        "lower80": 0.46,
        "upper80": 0.87
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.65,
        "lower80": 0.18,
        "upper80": 0.91
      },
      "energy_efficiency": {
        "estimate": 0.43,
        "lower80": 0.1,
        "upper80": 0.76
      },
      "faradaic_efficiency": {
        "estimate": 0.5,
        "lower80": 0.12,
        "upper80": 0.84
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.4,
        "lower80": 0.12,
        "upper80": 0.65
      },
      "selective_product_yield": {
        "estimate": 0.1,
        "lower80": 0.01,
        "upper80": 0.3
      },
      "transport_efficiency": {
        "estimate": 0.52,
        "lower80": 0.14,
        "upper80": 0.86
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.85,
        "lower80": 0.3,
        "upper80": 0.99
      },
      "energy_efficiency": {
        "estimate": 0.54,
        "lower80": 0.12,
        "upper80": 0.83
      },
      "faradaic_efficiency": {
        "estimate": 0.47,
        "lower80": 0.1,
        "upper80": 0.83
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.46,
        "lower80": 0.15,
        "upper80": 0.71
      },
      "selective_product_yield": {
        "estimate": 0.11,
        "lower80": 0.01,
        "upper80": 0.32
      },
      "transport_efficiency": {
        "estimate": 0.5,
        "lower80": 0.12,
        "upper80": 0.85
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.68,
        "lower80": 0.2,
        "upper80": 0.92
      },
      "energy_efficiency": {
        "estimate": 0.46,
        "lower80": 0.11,
        "upper80": 0.78
      },
      "faradaic_efficiency": {
        "estimate": 0.54,
        "lower80": 0.15,
        "upper80": 0.86
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.43,
        "lower80": 0.14,
        "upper80": 0.68
      },
      "selective_product_yield": {
        "estimate": 0.12,
        "lower80": 0.01,
        "upper80": 0.34
      },
      "transport_efficiency": {
        "estimate": 0.57,
        "lower80": 0.18,
        "upper80": 0.88
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.89,
        "lower80": 0.34,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.59,
        "lower80": 0.16,
        "upper80": 0.86
      },
      "faradaic_efficiency": {
        "estimate": 0.5,
        "lower80": 0.12,
        "upper80": 0.85
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.5,
        "lower80": 0.18,
        "upper80": 0.74
      },
      "selective_product_yield": {
        "estimate": 0.13,
        "lower80": 0.01,
        "upper80": 0.36
      },
      "transport_efficiency": {
        "estimate": 0.54,
        "lower80": 0.15,
        "upper80": 0.87
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.22,
        "lower80": 0.01,
        "upper80": 0.55
      },
      "energy_efficiency": {
        "estimate": 0.06,
        "lower80": 0.0,
        "upper80": 0.18
      },
      "faradaic_efficiency": {
        "estimate": 0.06,
        "lower80": 0.0,
        "upper80": 0.2
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.06,
        "lower80": 0.0,
        "upper80": 0.23
      },
      "selective_product_yield": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "transport_efficiency": {
        "estimate": 0.07,
        "lower80": 0.0,
        "upper80": 0.23
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.08,
        "lower80": 0.0,
        "upper80": 0.3
      },
      "energy_efficiency": {
        "estimate": 0.04,
        "lower80": 0.0,
        "upper80": 0.15
      },
      "faradaic_efficiency": {
        "estimate": 0.03,
        "lower80": 0.0,
        "upper80": 0.14
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.025,
        "lower80": 0.0,
        "upper80": 0.15
      },
      "selective_product_yield": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.035
      },
      "transport_efficiency": {
        "estimate": 0.04,
        "lower80": 0.0,
        "upper80": 0.16
      }
    }
  ],
  "rationale": "Predictions interpolate the observed polarity tradeoff near ±1 V, extrapolate time/charge exposure from 300–3600 s to 600 or 7200 s with saturation, and account for the smaller reagent amount. E1 is assigned the observed throughput gain and selectivity penalty; E3 and S2 receive much wider intervals because they were never tested. The 500 mA cases reflect the severe parasitic-efficiency collapse observed at high current cap. Score estimates include the published low-yield gate, so uncertainty is especially asymmetric near a selective yield of 0.02."
}
```
