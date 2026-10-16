# repeat-01/EC-W04-B12-optimization-E-Opaque

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-01\EC-W04-B12-optimization-E-Opaque\participant\optimization-E-Opaque

## 同期笔记

### v1 · 公开事件 0

# Electrochemical campaign hypotheses

## H1 [tentative]
At fixed loading, balanced efficiency will have an intermediate optimum in potential magnitude and electrolysis time: insufficient drive limits conversion, while excessive drive/time reduces selectivity and energy efficiency. Current cap may bind only in some media.

## H2 [tentative]
Anonymous solvent and electrolyte profiles may materially alter transport, ohmic loss, and selectivity; therefore the first batches will screen material combinations and both potential signs before local refinement.

**Pre-experiment testable expectation:** at least one moderate potential/time condition will outperform both a low-drive and a high-drive condition at the same 0.02 mol reagent in 0.05 L solvent. A sign reversal may sharply change selective product yield. UV-vis will be used on selected batches as a noisy intermediate diagnostic, not as the final criterion.

### v2 · 公开事件 49

# Electrochemical campaign hypotheses

## H1 [supported qualitatively; optimum unresolved]
Negative potential is productive in tested conditions, whereas +1.0 V at high cap/time gave zero measured yield and score (final assay event runner-operation-0021). Increasing negative drive/time increased conversion relative to the initial low-charge trial, but efficiency/selectivity tradeoffs remain: S0/E0 at -2.5 V for 14400 s reached more conversion yet only score 0.209 (runner-operation-0028).

## H2 [supported for tested diagonal pairs]
Material choice strongly matters. At -1.5 V, 500 mA cap, 7200 s, 0.02 mol in 0.05 L, S2/E2 was best among diagonal S1/E1, S2/E2, S3/E3 with scores 0.278, 0.311, 0.177 respectively (runner-operation-0035, -0042, -0049). S2/E2 also showed negligible precipitation versus S1/E1. This is numerical evidence across confounded solvent/electrolyte pairs, not yet attribution to either component.

## H3 [tentative]
The S2/E2 advantage may arise from electrolyte E2, solvent S2, or interaction. Cross-pairs S2/E1 and S1/E2 will distinguish main effects; then potential/time refinement will test whether milder potential improves the balanced score despite lower conversion. Evidence that a cross-pair exceeds S2/E2 would redirect final optimization.

### v3 · 公开事件 84

# Electrochemical campaign hypotheses

## H1 [supported in tested scope]
Negative potential is required for productive conversion in this system. The tested positive high-cap condition produced zero yield/score (runner-operation-0021), whereas negative conditions produced measurable yield (e.g. runner-operation-0014 onward). Excessively negative potential was not beneficial: on S1/E2 at 7200 s, moving from -1.5 V to -1.0 V and -0.75 V raised score from 0.334 to 0.405 and 0.431 (runner-operation-0063, -0070, -0077).

## H2 [supported in tested scope]
Solvent S1 and electrolyte E2 form the best tested material pair. Cross-pair tests indicate both matter: S1/E2 scored 0.334, exceeding S2/E2 (0.311) and S2/E1 (0.285) at matched -1.5 V, 500 mA cap, 7200 s (runner-operation-0063, -0042, -0056). This supports material main effects or interaction but does not uniquely decompose them.

## H3 [supported locally; boundary unresolved]
At S1/E2 and -0.75 V, extending electrolysis from 7200 to 14400 s increased conversion from 0.426 to 0.809, selective yield from 0.277 to 0.562, and balanced score from 0.431 to 0.545 (runner-operation-0077, -0084), while selectivity remained about 0.65 and safety risk remained 0.083. This numerical difference is much larger than stated final-assay noise scales, though there is no replicate. The optimum beyond 14400 s is untested and outside the legal single-segment duration range.

## Operating decision
Recommend batch 12: 0.02 mol limiting reagent in 0.05 L S1; E2; -0.75 V with 500 mA magnitude cap; electrolyze 14400 s; terminate, then assay. It is the highest observed score and yield under the safety limit. Change this decision if replication shows instability or if a nearby milder potential/current setting demonstrates materially better ohmic/energy efficiency without sacrificing yield.

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
    "cost": 0.28512001037597656,
    "electrochemical_conversion": 0.012074419297277927,
    "electrochemical_selectivity": 1.0,
    "energy_efficiency": 0.54636549949646,
    "faradaic_efficiency": 0.546867847442627,
    "ohmic_efficiency": 0.9572166204452515,
    "pH_normalized": 0.23443032801151276,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.5181640982627869
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
    "electrochemical_conversion": 0.03960590437054634,
    "electrochemical_selectivity": 0.6096861362457275,
    "energy_efficiency": 0.029473481699824333,
    "faradaic_efficiency": 0.10201752930879593,
    "ohmic_efficiency": 0.8875528573989868,
    "pH_normalized": 0.2317349761724472,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.20717447996139526,
    "selective_product_yield": 0.03755393996834755,
    "transport_efficiency": 0.1282743513584137
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
    "cost": 0.2921999990940094,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.0,
    "ohmic_efficiency": 0.8182538747787476,
    "pH_normalized": 0.2324499785900116,
    "precipitation_signal": 0.9863388538360596,
    "safety_risk": 0.05933958664536476,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.0
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
      "current_mA": 500,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -2.5
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
    "cost": 0.3569999933242798,
    "electrochemical_conversion": 0.17362138628959656,
    "electrochemical_selectivity": 0.4501611590385437,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.12334384769201279,
    "ohmic_efficiency": 0.9313426613807678,
    "pH_normalized": 0.23175939917564392,
    "precipitation_signal": 0.9870871305465698,
    "safety_risk": 0.05933958664536476,
    "score": 0.20910215377807617,
    "selective_product_yield": 0.08573846518993378,
    "transport_efficiency": 0.09185630828142166
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
      "solvent": 1,
      "volume_L": 0.05
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -1.5
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
    "cost": 0.32659998536109924,
    "electrochemical_conversion": 0.2586152255535126,
    "electrochemical_selectivity": 0.47545284032821655,
    "energy_efficiency": 0.09531523287296295,
    "faradaic_efficiency": 0.28457748889923096,
    "ohmic_efficiency": 0.8257129192352295,
    "pH_normalized": 0.2099734991788864,
    "precipitation_signal": 0.709762692451477,
    "safety_risk": 0.08273958414793015,
    "score": 0.2775326669216156,
    "selective_product_yield": 0.12814265489578247,
    "transport_efficiency": 0.27406802773475647
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
      "volume_L": 0.05
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -1.5
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
    "cost": 0.358599990606308,
    "electrochemical_conversion": 0.27638351917266846,
    "electrochemical_selectivity": 0.5437362790107727,
    "energy_efficiency": 0.175028458237648,
    "faradaic_efficiency": 0.31804925203323364,
    "ohmic_efficiency": 0.7617440223693848,
    "pH_normalized": 0.17581218481063843,
    "precipitation_signal": 0.0023995577357709408,
    "safety_risk": 0.10073958337306976,
    "score": 0.31138020753860474,
    "selective_product_yield": 0.1582837849855423,
    "transport_efficiency": 0.2933659255504608
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
      "volume_L": 0.05
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": -1.5
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
    "cost": 0.3386000096797943,
    "electrochemical_conversion": 0.07005418092012405,
    "electrochemical_selectivity": 0.43888282775878906,
    "energy_efficiency": 0.03638724610209465,
    "faradaic_efficiency": 0.06616039574146271,
    "ohmic_efficiency": 0.9194492101669312,
    "pH_normalized": 0.2787778973579407,
    "precipitation_signal": 0.0,
    "safety_risk": 0.11333958804607391,
    "score": 0.17683419585227966,
    "selective_product_yield": 0.033623334020376205,
    "transport_efficiency": 0.06956075131893158
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
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -1.5
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
    "cost": 0.358599990606308,
    "electrochemical_conversion": 0.2621082365512848,
    "electrochemical_selectivity": 0.48520874977111816,
    "energy_efficiency": 0.1532960832118988,
    "faradaic_efficiency": 0.29441872239112854,
    "ohmic_efficiency": 0.8216068744659424,
    "pH_normalized": 0.2166876494884491,
    "precipitation_signal": 0.5652920007705688,
    "safety_risk": 0.10073958337306976,
    "score": 0.28491246700286865,
    "selective_product_yield": 0.11024928838014603,
    "transport_efficiency": 0.2879233658313751
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
      "volume_L": 0.05
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -1.5
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
    "cost": 0.32659998536109924,
    "electrochemical_conversion": 0.2927190959453583,
    "electrochemical_selectivity": 0.5548101663589478,
    "energy_efficiency": 0.2049250453710556,
    "faradaic_efficiency": 0.30719706416130066,
    "ohmic_efficiency": 0.8232319355010986,
    "pH_normalized": 0.16263499855995178,
    "precipitation_signal": 0.008188718929886818,
    "safety_risk": 0.08273958414793015,
    "score": 0.33377206325531006,
    "selective_product_yield": 0.18338274955749512,
    "transport_efficiency": 0.3280283510684967
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
      "volume_L": 0.05
    },
    {
      "current_mA": 500,
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
    "cost": 0.31940001249313354,
    "electrochemical_conversion": 0.3843301236629486,
    "electrochemical_selectivity": 0.6501553654670715,
    "energy_efficiency": 0.37927961349487305,
    "faradaic_efficiency": 0.4045751392841339,
    "ohmic_efficiency": 0.6794392466545105,
    "pH_normalized": 0.16032086312770844,
    "precipitation_signal": 0.0,
    "safety_risk": 0.08273958414793015,
    "score": 0.4054711163043976,
    "selective_product_yield": 0.23042082786560059,
    "transport_efficiency": 0.4059247076511383
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
      "volume_L": 0.05
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -0.75
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
    "cost": 0.3158000111579895,
    "electrochemical_conversion": 0.42634522914886475,
    "electrochemical_selectivity": 0.6590359210968018,
    "energy_efficiency": 0.40488535165786743,
    "faradaic_efficiency": 0.4448503255844116,
    "ohmic_efficiency": 0.5896739363670349,
    "pH_normalized": 0.16130590438842773,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.08273958414793015,
    "score": 0.4311595857143402,
    "selective_product_yield": 0.27725958824157715,
    "transport_efficiency": 0.4520302712917328
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
      "volume_L": 0.05
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -0.75
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
    "cost": 0.32659998536109924,
    "electrochemical_conversion": 0.8093780279159546,
    "electrochemical_selectivity": 0.6503139734268188,
    "energy_efficiency": 0.3833722472190857,
    "faradaic_efficiency": 0.40853351354599,
    "ohmic_efficiency": 0.6030224561691284,
    "pH_normalized": 0.1618262231349945,
    "precipitation_signal": 0.0,
    "safety_risk": 0.08273958414793015,
    "score": 0.5449472069740295,
    "selective_product_yield": 0.5623827576637268,
    "transport_efficiency": 0.4297584593296051
  }
}
```

## K1 封存报告

## Mechanistic account

I interpret this benchmark world as a potential-dependent electrochemical conversion of a limiting reactant into a target product, with parallel unproductive charge transfer, side-product formation, precipitation, and resistive/transport losses. The solvent and electrolyte labels are anonymous benchmark formulations, so the discussion below concerns their observed functional roles—not real chemical identities.

All 12 batches used 0.020 mol reagent and 0.050 L solvent. Consequently, the campaign principally identified effects of potential, electrolysis duration, current cap, solvent, and electrolyte at a fixed initial concentration of approximately 0.40 mol L⁻¹. No conclusion about concentration or scale dependence can be drawn.

### Proposed process structure

A useful qualitative representation is:

- Reactant + productive cathodic charge → target product
- Reactant + unproductive charge → soluble impurities or degraded material
- Dissolved species ⇌ precipitated/inactive material
- Applied electrical power → productive electrochemistry + activation loss + ohmic heating/loss + transport loss

For a simple working model, let `X` denote conversion, `S` electrochemical selectivity, and `Y` selective product yield. The observations are broadly consistent with

`Y ≈ X × S × R`,

where `R` represents recovery or retention of target product in the assayed phase and may be reduced by precipitation, degradation, or other mass-balance effects. This is only a structural hypothesis: the assay did not provide enough independently identified quantities to estimate `R` or a detailed species balance.

Conversion could be represented phenomenologically as

`dX/dt = k_prod(V, solvent, electrolyte, state) × I_effective/F × (1-X) - k_loss(V, state) × X`,

with selectivity determined by competition between productive and side-reaction rates. The configured current was a cap rather than a direct measurement of delivered current, so `I_effective` is not identifiable from the campaign. Likewise, a possible efficiency decomposition is

`energy efficiency ≈ faradaic efficiency × transport efficiency × voltage-utilization factor`,

with ohmic efficiency reporting a related but not necessarily independent loss channel. This explains why increasing nominal electrical severity does not necessarily increase useful conversion or score.

## Evidence that potential polarity and magnitude matter

Polarity was the clearest qualitative control. Batch 3 used S0/E0, +1.0 V, a 500 mA cap, and 3600 s; it returned zero conversion, zero target yield, zero faradaic and transport efficiency, and score 0. Batch 2 used the same material pair, cap, and duration but −1.5 V; it produced conversion 0.0396, selectivity 0.6097, yield 0.0376, and score 0.207. These batches strongly support a productive negative-potential direction under the tested conventions.

Batch 1, at +1.0 V but only 100 mA and 300 s, showed a small conversion estimate of 0.0121 and assay selectivity clipped at 1.0, yet target yield was zero and the score gate reduced the score to zero. Because conversion uncertainty was 0.01 and yield uncertainty was 0.01, this is not convincing evidence for useful positive-potential chemistry. It could reflect assay noise, trace nonproductive conversion, or a tiny process below the yield gate.

Potential magnitude was non-monotonic. With S1/E2 at 500 mA and 7200 s:

- Batch 9, −1.5 V: conversion 0.2927, selectivity 0.5548, yield 0.1834, energy efficiency 0.2049, score 0.3338.
- Batch 10, −1.0 V: conversion 0.3843, selectivity 0.6502, yield 0.2304, energy efficiency 0.3793, score 0.4055.
- Batch 11, −0.75 V: conversion 0.4263, selectivity 0.6590, yield 0.2773, energy efficiency 0.4049, score 0.4312.

Thus, making the potential less negative from −1.5 to −0.75 V improved conversion, selectivity, yield, and energy efficiency in this local comparison. This rules out a simple model in which conversion depends only on nominal voltage magnitude or nominal charge. Plausible explanations are that excessive overpotential activates side reactions, lowers faradaic selectivity, changes electrode passivation, or pushes the system into an unfavorable transport regime. Another possibility is that the current cap was not reached uniformly and that the effective current–voltage response varied sharply with medium.

Batch 4 further illustrates the cost of excessive drive. S0/E0 at −2.5 V, 500 mA, and 14400 s reached conversion 0.1736 but only selectivity 0.4502, yield 0.0857, zero reported energy efficiency, and score 0.2091. Although its duration was long, it performed much worse than the milder S1/E2 conditions. Potential, material choice, and time are therefore strongly coupled.

The data do not locate the true potential optimum. The best tested potential was −0.75 V, but no condition between 0 and −0.75 V was assayed. Extrapolating that still milder negative potentials would continue improving performance is conjectural: productive rate could collapse near an onset potential.

## Solvent and electrolyte effects

The matched diagonal screen at −1.5 V, 500 mA, and 7200 s showed substantial medium effects:

- Batch 5, S1/E1: conversion 0.2586, selectivity 0.4755, yield 0.1281, score 0.2775, precipitation signal 0.7098.
- Batch 6, S2/E2: conversion 0.2764, selectivity 0.5437, yield 0.1583, score 0.3114, precipitation signal 0.0024.
- Batch 7, S3/E3: conversion 0.0701, selectivity 0.4389, yield 0.0336, score 0.1768, precipitation signal 0.

Because each solvent changed together with its electrolyte, those three batches alone could not assign the effects to either component. Cross-pair experiments helped:

- Batch 8, S2/E1: conversion 0.2621, selectivity 0.4852, yield 0.1102, score 0.2849, precipitation 0.5653.
- Batch 9, S1/E2: conversion 0.2927, selectivity 0.5548, yield 0.1834, score 0.3338, precipitation 0.0082.

At matched electrical conditions, changing E1 to E2 while changing from batch 5 to batch 9 increased score by about 0.056 and nearly eliminated precipitation. Comparing batches 6 and 9 indicates that S1 was better than S2 when paired with E2: score rose by about 0.022, yield by 0.025, and conversion by 0.016. Comparing batches 5 and 8 indicates that S2/E1 modestly exceeded S1/E1 in conversion and score but had a lower measured yield. These comparisons suggest that E2 provides the larger favorable contribution, while S1 is the best tested partner for E2. Nevertheless, solvent–electrolyte interaction remains plausible; the design was not a full 4×4 factorial and provides no replicates.

Functionally, E2 appears to support higher productive current fraction, transport, and suppression of precipitation. At the matched −1.5 V condition, batch 9 had faradaic efficiency 0.3072 and transport efficiency 0.3280, compared with 0.2846 and 0.2741 in batch 5 and 0.2944 and 0.2879 in batch 8. S1/E2 may therefore stabilize soluble electroactive species or improve interfacial kinetics. These molecular explanations are conjectures because the labels are anonymous and no species-specific mapping was public.

## Time and accumulated charge

The cleanest duration comparison is between batches 11 and 12, both using S1/E2, −0.75 V, and a 500 mA cap:

- Batch 11, 7200 s: conversion 0.4263, selectivity 0.6590, yield 0.2773, score 0.4312.
- Batch 12, 14400 s: conversion 0.8094, selectivity 0.6503, yield 0.5624, score 0.5449.

Doubling duration nearly doubled conversion and approximately doubled selective yield, while selectivity changed little. This is consistent with substantial reactant remaining after 7200 s and approximately cumulative productive charge transfer over this interval. It also suggests that major degradation had not yet overtaken production by 14400 s in S1/E2. The faradaic, transport, energy, and ohmic efficiencies in batch 12 were 0.4085, 0.4298, 0.3834, and 0.6030, respectively, all still appreciable.

The relationship is not exactly linear: conversion increased by 0.383 rather than another 0.426, as expected from reactant depletion, changing composition, or efficiency drift. A saturating form such as `X(t)=X_max[1-exp(-k_eff t)]` is plausible locally, but two time points cannot distinguish it from charge-limited linear conversion with changing efficiency. Because 14400 s was the legal maximum for one electrolysis operation and no longer run was tested, any claim about a time optimum or late degradation is extrapolation.

## Precipitation, pH proxy, and coupling to performance

Precipitation was strongly medium-dependent. S0/E0 gave precipitation signals near 1 in batches 1–4. S1/E1 and S2/E1 also gave large signals of 0.710 and 0.565 in batches 5 and 8. In contrast, E2 conditions in batches 6 and 9–12 gave signals near zero. This association suggests that E2 suppresses an insoluble reactant, product, salt, or passivating phase. Suppressing precipitation could improve accessible reactant concentration, mass transport, electrode area, product recovery, or all four.

However, precipitation is not proven to be the direct cause of lower score. Batch 7 had zero precipitation but poor conversion and score, showing that absence of precipitation is not sufficient. It is more likely one coupled loss mechanism among several.

The normalized pH signal also depended on the material pair: approximately 0.16–0.18 for E2 batches 6 and 9–12, 0.21–0.22 for E1 batches 5 and 8, about 0.23 for S0/E0, and 0.279 for S3/E3. Within S1/E2 it stayed near 0.16 across potential and duration. This makes pH primarily a formulation-dependent state marker in the observed data. It may affect proton-coupled electron transfer or precipitation, but causal direction is not identifiable because pH was not independently manipulated.

## Efficiency tradeoffs and score behavior

The public balanced score rewards yield most heavily but also conversion, selectivity, faradaic efficiency, transport efficiency, ohmic efficiency, and energy efficiency, with a multiplicative gate when yield is extremely low. The campaign results are consistent with this structure. Batch 1 had apparently excellent selectivity and ohmic efficiency but zero yield, so its score was zero. Batch 12 had only moderate selectivity and efficiencies but much higher conversion and yield, producing the best score, 0.5449.

Ohmic efficiency did not move in the same direction as overall performance. For S1/E2 at 7200 s, it fell from 0.8232 at −1.5 V to 0.6794 at −1.0 V and 0.5897 at −0.75 V, even while yield and total score improved. This indicates a tradeoff: the milder-potential regime was chemically more productive and energy-efficient overall but appeared less favorable on the separately reported ohmic channel. The channels should therefore not be treated as independent multiplicative physical efficiencies without further calibration.

Safety risk was determined mainly by the initial formulation in these experiments and remained comfortably below the limit. The recommended S1 batches showed risk 0.0827, and batch 12 remained far below the 0.65 constraint. No observed evidence indicates that the longer electrolysis increased the reported risk, although the benchmark risk metric need not cover unobserved real-world hazards.

## Experiments that changed the explanation

1. Batches 2 and 3 established the negative-polarity requirement: −1.5 V produced measurable conversion and yield whereas +1.0 V did not.
2. Batch 4 showed that simply maximizing negative potential and duration was not a successful strategy; excessive drive produced low selectivity and no reported energy efficiency.
3. Batches 5–7 revealed large formulation effects and showed that low precipitation alone was not enough for high performance.
4. Batches 8 and 9 separated some solvent and electrolyte contributions and identified S1/E2 as the best tested pair.
5. Batches 9–11 overturned any assumption that more negative potential was better: performance improved monotonically over the tested sequence −1.5, −1.0, and −0.75 V.
6. Batch 12 demonstrated that duration remained strongly beneficial at −0.75 V, raising selective yield to 0.5624 and score to 0.5449.

## Scope and uncertainty

The conclusions apply only near 0.020 mol reagent in 0.050 L solvent, with the tested anonymous formulations, potential convention, and a 500 mA cap for most informative batches. There were no replicate batches, so process variability cannot be separated from condition effects. Final-assay noise was much smaller than many of the major observed differences—for example, selective-yield noise was stated as 0.01—but unmodeled batch variability is unknown.

The campaign cannot identify actual delivered current, electrode area, current density, cell resistance, electron stoichiometry, reactant/product concentrations over time, electrode passivation, temperature evolution, or molecular identities. Thus it cannot distinguish definitively among kinetic activation, mass transport, ohmic limitation, precipitation-mediated passivation, and electrolyte-specific stabilization. Several reported efficiencies may share latent causes and should not be assumed statistically independent.

Plausible alternative explanations include:

- The apparent potential optimum may reflect the simulator’s current–voltage response rather than suppression of a chemical side reaction.
- E2 may improve conductivity or current delivery rather than intrinsic selectivity.
- The precipitation signal may report a spectator salt rather than loss of target or reactant.
- Differences of modest size between S1/E2 and S2/E2 may include assay noise or uncontrolled simulated process variation.
- The high yield at 14400 s may not persist beyond that time; depletion, product destruction, or passivation could eventually dominate.

## Best-supported operating mechanism and recommendation

The best-supported account is that productive reduction occurs in a finite negative-potential window. E2 creates the most favorable tested electrochemical environment, probably by improving productive faradaic/transport behavior and suppressing precipitation. S1 further improves that environment. Excessively negative potential diverts current into inefficient pathways, whereas −0.75 V retains selectivity and permits productive conversion to accumulate over time. At the tested concentration, 14400 s had not yet reached complete conversion or an evident degradation-dominated regime.

Accordingly, the sealed recommended batch 12—0.020 mol reagent, 0.050 L S1, electrolyte E2, −0.75 V, 500 mA cap, and 14400 s—is an evidence-based optimum among completed experiments, not a claim of the global optimum. Its observed final values were conversion 0.8094, selectivity 0.6503, selective product yield 0.5624, faradaic efficiency 0.4085, transport efficiency 0.4298, ohmic efficiency 0.6030, energy efficiency 0.3834, precipitation signal 0, safety risk 0.0827, and balanced score 0.5449.

## K2 封存报告

1. **Claims and laws.** No instance-specific prior, nominal material-property dossier, or supplied mechanistic law was provided; the anonymous labels carried no chemical prior. My initial self-developed claim that useful performance would have an intermediate electrical-drive region was supported qualitatively. Positive drive was contradicted as a productive strategy by batch 3 (+1.0 V, 500 mA, 3600 s), which returned zero conversion, yield, and score, while batch 2 at −1.5 V produced measurable yield. Excessive negative drive was also unfavorable: batch 4 at −2.5 V and 14400 s scored only 0.209. Most importantly, matched S1/E2 batches 9–11 improved as potential moved from −1.5 to −1.0 to −0.75 V, with scores 0.334, 0.405, and 0.431. This evidence changed my view from a generic ‘more charge may improve conversion’ model to a finite productive-potential-window model.

The claim that solvent and electrolyte materially affect performance was supported. The diagonal comparison in batches 5–7 produced scores of 0.278 for S1/E1, 0.311 for S2/E2, and 0.177 for S3/E3. Cross-pairs then changed the attribution: batch 9 (S1/E2, score 0.334) exceeded both batch 6 (S2/E2) and batch 8 (S2/E1, score 0.285), making S1/E2 the best tested pair and suggesting a particularly favorable role for E2. A separable solvent-plus-electrolyte law remained untested because the campaign did not cover the full factorial and interactions could not be identified.

A local accumulated-charge/time relationship was supported by batches 11 and 12. At identical S1/E2, −0.75 V, and 500 mA settings, doubling time from 7200 to 14400 s raised conversion from 0.426 to 0.809 and yield from 0.277 to 0.562 while selectivity stayed near 0.65. A globally linear time law was not supported or tested; depletion already makes strict linearity implausible, and behavior beyond 14400 s was not observed.

The idea that suppressing precipitation is sufficient for success was contradicted: batch 7 had zero precipitation signal but poor conversion and score. The weaker claim that precipitation is one adverse coupled process remained supported by the association of E1/S0 conditions with high precipitation and E2 conditions with near-zero precipitation. The heuristic `yield ≈ conversion × selectivity × retention` was only a conceptual bookkeeping relation, not a validated quantitative law; assay values, especially batch 2, did not support treating the reported channels as an exact identity.

2. **One discriminating experiment.** I would run 0.020 mol reagent in 0.050 L S1 with E2 at −1.5 V, a 250 mA cap, and 14400 s, followed by the same final assay. This has the same nominal current–time product as batch 9 (500 mA for 7200 s) but halves the current cap. My leading explanation is that the poorer result at −1.5 V primarily reflects potential-activated side reactions; an alternative is that the observed loss is mainly current-density/transport or current-delivery limitation.

If the new batch retained roughly batch-9 selectivity and efficiencies despite lower current—approximately 0.55 selectivity, 0.31 faradaic efficiency, and score near 0.33—I would strengthen the potential-controlled side-reaction explanation. If selectivity, faradaic/transport efficiency, and yield rose substantially toward or beyond batches 10–12 at the same nominal charge, I would shift toward current-density or transport limitation as the main cause. If conversion fell nearly in proportion to effective current without appreciable efficiency changes, I would infer that the configured current cap or delivered-current response dominates kinetics. A poor result accompanied by increasing precipitation would instead increase support for time-dependent passivation or phase loss. The comparison would still be imperfect because longer residence time is a confound, but it is the most informative single experiment available within the original duration limit.

3. **Unused evidence, reliability, and goal effects.** The intermediate UV–visible measurements and their full spectral shapes were largely unused beyond confirming broad efficiency trends; decisions relied mainly on final assays. Raw multichannel peak patterns, detailed mass-balance packets, and spectral artifacts were not quantitatively modeled. pH-normalized and precipitation signals were used qualitatively but not in a fitted causal model. No replicate evidence was collected, so stochastic process variation remained unestimated.

The least reliable predictions are the short positive-potential prediction Q02 and, more generally, Q04/Q06/Q08/Q10/Q12. Batch 1 showed high reported efficiency channels at very low positive-potential exposure despite zero yield, whereas batch 3 showed all productive efficiency channels collapsing to zero after a stronger positive exposure; interpolation between those regimes is poorly constrained. Predictions involving untested S0/E1, S0/E3, S2/E0 combinations are also weak because solvent–electrolyte interactions were only sparsely sampled. All prediction batches used 0.012 mol in 0.025 L rather than the campaign’s 0.020 mol in 0.050 L, so concentration extrapolation adds uncertainty. Q11 is uncertain because current-cap effects were not independently mapped.

The recommendation for batch 12 is reliable only as the highest observed completed batch, not as a global optimum. It lies on the maximum tested duration boundary, lacks replication, and does not establish whether a milder potential or altered current would improve the score further.

The assigned goal did affect evidence collection: maximizing balanced score encouraged broad early screening followed by exploitation of S1/E2 and −0.75 V. That strategy found a strong operating point but displaced replication, a full solvent–electrolyte factorial, independent pH manipulation, and systematic current/time separation. I see no clear conflict between the goal and honest interpretation, but the optimization emphasis made causal identification and uncertainty estimation weaker than they would have been in a mechanism-first campaign.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.72,
        "lower80": 0.35,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.4,
        "lower80": 0.18,
        "upper80": 0.62
      },
      "faradaic_efficiency": {
        "estimate": 0.43,
        "lower80": 0.22,
        "upper80": 0.65
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.11,
        "lower80": 0.0,
        "upper80": 0.23
      },
      "selective_product_yield": {
        "estimate": 0.007,
        "lower80": 0.0,
        "upper80": 0.025
      },
      "transport_efficiency": {
        "estimate": 0.42,
        "lower80": 0.2,
        "upper80": 0.64
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.8,
        "lower80": 0.25,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.5,
        "lower80": 0.2,
        "upper80": 0.72
      },
      "faradaic_efficiency": {
        "estimate": 0.52,
        "lower80": 0.22,
        "upper80": 0.74
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.016,
        "lower80": 0.0,
        "upper80": 0.1
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0.0,
        "upper80": 0.014
      },
      "transport_efficiency": {
        "estimate": 0.5,
        "lower80": 0.2,
        "upper80": 0.72
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.68,
        "lower80": 0.45,
        "upper80": 0.88
      },
      "energy_efficiency": {
        "estimate": 0.31,
        "lower80": 0.15,
        "upper80": 0.5
      },
      "faradaic_efficiency": {
        "estimate": 0.34,
        "lower80": 0.18,
        "upper80": 0.53
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.334,
        "lower80": 0.22,
        "upper80": 0.45
      },
      "selective_product_yield": {
        "estimate": 0.06,
        "lower80": 0.02,
        "upper80": 0.12
      },
      "transport_efficiency": {
        "estimate": 0.36,
        "lower80": 0.18,
        "upper80": 0.55
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.05,
        "lower80": 0.0,
        "upper80": 0.25
      },
      "energy_efficiency": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.12
      },
      "faradaic_efficiency": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.12
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0.0,
        "upper80": 0.012
      },
      "transport_efficiency": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.13
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.64,
        "lower80": 0.39,
        "upper80": 0.84
      },
      "energy_efficiency": {
        "estimate": 0.28,
        "lower80": 0.12,
        "upper80": 0.47
      },
      "faradaic_efficiency": {
        "estimate": 0.31,
        "lower80": 0.15,
        "upper80": 0.5
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.31,
        "lower80": 0.19,
        "upper80": 0.43
      },
      "selective_product_yield": {
        "estimate": 0.06,
        "lower80": 0.018,
        "upper80": 0.125
      },
      "transport_efficiency": {
        "estimate": 0.33,
        "lower80": 0.16,
        "upper80": 0.52
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.05,
        "lower80": 0.0,
        "upper80": 0.27
      },
      "energy_efficiency": {
        "estimate": 0.025,
        "lower80": 0.0,
        "upper80": 0.14
      },
      "faradaic_efficiency": {
        "estimate": 0.025,
        "lower80": 0.0,
        "upper80": 0.14
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.016,
        "lower80": 0.0,
        "upper80": 0.09
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0.0,
        "upper80": 0.014
      },
      "transport_efficiency": {
        "estimate": 0.025,
        "lower80": 0.0,
        "upper80": 0.14
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.52,
        "lower80": 0.25,
        "upper80": 0.76
      },
      "energy_efficiency": {
        "estimate": 0.12,
        "lower80": 0.02,
        "upper80": 0.29
      },
      "faradaic_efficiency": {
        "estimate": 0.15,
        "lower80": 0.04,
        "upper80": 0.32
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.19,
        "lower80": 0.07,
        "upper80": 0.31
      },
      "selective_product_yield": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.058
      },
      "transport_efficiency": {
        "estimate": 0.16,
        "lower80": 0.04,
        "upper80": 0.34
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.04,
        "lower80": 0.0,
        "upper80": 0.23
      },
      "energy_efficiency": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.11
      },
      "faradaic_efficiency": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.11
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.075
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0.0,
        "upper80": 0.011
      },
      "transport_efficiency": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.12
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.7,
        "lower80": 0.45,
        "upper80": 0.9
      },
      "energy_efficiency": {
        "estimate": 0.34,
        "lower80": 0.16,
        "upper80": 0.54
      },
      "faradaic_efficiency": {
        "estimate": 0.36,
        "lower80": 0.18,
        "upper80": 0.56
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.35,
        "lower80": 0.22,
        "upper80": 0.48
      },
      "selective_product_yield": {
        "estimate": 0.075,
        "lower80": 0.025,
        "upper80": 0.145
      },
      "transport_efficiency": {
        "estimate": 0.38,
        "lower80": 0.19,
        "upper80": 0.58
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.05,
        "lower80": 0.0,
        "upper80": 0.27
      },
      "energy_efficiency": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.13
      },
      "faradaic_efficiency": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.13
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.085
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0.0,
        "upper80": 0.013
      },
      "transport_efficiency": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.13
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.66,
        "lower80": 0.43,
        "upper80": 0.84
      },
      "energy_efficiency": {
        "estimate": 0.18,
        "lower80": 0.06,
        "upper80": 0.36
      },
      "faradaic_efficiency": {
        "estimate": 0.25,
        "lower80": 0.11,
        "upper80": 0.43
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.332,
        "lower80": 0.21,
        "upper80": 0.46
      },
      "selective_product_yield": {
        "estimate": 0.2,
        "lower80": 0.1,
        "upper80": 0.32
      },
      "transport_efficiency": {
        "estimate": 0.26,
        "lower80": 0.11,
        "upper80": 0.44
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.14
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "faradaic_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "selective_product_yield": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.007
      },
      "transport_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.07
      }
    }
  ],
  "rationale": "Predictions extrapolate the campaign’s strong polarity effect: negative potentials were productive, while sustained positive-potential batches collapsed toward zero yield and score. Negative-potential estimates scale approximate charge per mole while allowing improved selectivity near −0.8 V; S2 is given a modest benefit, E1 a small penalty relative to the uncertain S0/E0 baseline, and E3 a larger penalty. The 500 mA negative batch receives higher yield but lower electrical efficiencies than the 100 mA analogue. Intervals are deliberately broad because the new concentration, several solvent–electrolyte combinations, and the current-by-duration interactions were not directly replicated; bounds also include final-assay noise and possible score-gate behavior at very low yield."
}
```
