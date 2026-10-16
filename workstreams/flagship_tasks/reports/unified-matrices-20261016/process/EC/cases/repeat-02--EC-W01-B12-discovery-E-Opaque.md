# repeat-02/EC-W01-B12-discovery-E-Opaque

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-02\EC-W01-B12-discovery-E-Opaque\participant\discovery-E-Opaque

## 同期笔记

### v1 · 公开事件 0

# Electrochemical hypothesis notebook

## H1 [tentative; pre-experiment]
At fixed 0.04 mol reagent in 0.08 L, response should depend nonlinearly on potential sign/magnitude and duration: conversion should rise with delivered charge/time, while selectivity may peak at an intermediate driving force if over-electrolysis creates byproduct. Current cap may limit rate, so duration and cap may interact.

## H2 [tentative; pre-experiment]
Anonymous solvent and electrolyte profiles may independently alter transport/ohmic efficiency and product selectivity. I will use broad contrasts across all four IDs and both potential signs, then repeat informative conditions to separate reproducibility from numerical differences.

## Planned tests
Use one consistent loading (0.5 mol/L nominal), span potential sign/magnitude, short/long electrolysis, current caps, solvents, and electrolytes. One intermediate UV-vis or pH measurement per batch will probe mechanism without consuming final-assay capacity. Conclusions will remain conditional where factors are confounded.

### v2 · 公开事件 70

# Electrochemical hypothesis notebook

## H1 [supported for studied conditions; revised]
Potential sign is not globally predictive by itself. In matched S1/E1 and S2/E2 high-charge pairs, negative potential produced appreciable conversion/yield while positive potential was near-null (events runner-operation-0035 vs -0042; -0049 vs -0056). However S3/E3 at +1.5 V produced high selectivity and higher yield than its -1.5 V counterpart (-0070 vs -0063). Thus a medium/electrolyte-by-polarity interaction is required; a universal one-polarity mechanism is rejected.

## H2 [supported, identity unresolved]
Material profile strongly modifies precipitation, pH, transport, and productive polarity. S0/E0 has precipitation near unity and weak conversion even at substantial charge (-0021), S2/E2 suppresses precipitation but does not maximize yield (-0049), and S3/E3 suppresses precipitation while enabling selective positive-potential product (-0070). Because solvent and electrolyte were changed together, their individual roles remain confounded.

## H3 [tentative]
Conversion/yield depend on charge and driving force, but excessive magnitude reduces efficiency through parasitic current. Negative -2 V/long electrolysis increased conversion over short -1 V exposure, while faradaic/energy efficiencies were low. Testable consequence: material crossovers at fixed +1.5 V/current/time can identify whether S3 or E3 carries the positive-polarity benefit.

## Decision
Use the final two batches as S3/E0 and S0/E3 crossovers at the successful +1.5 V, 250 mA, 14400 s condition. A strong response in only one crossover will assign the dominant material contribution; both or neither would imply additive interaction.

### v3 · 公开事件 84

# Electrochemical hypothesis notebook

## H1 [supported in tested design space]
Productive polarity is conditional on the coupled solvent/electrolyte environment, not an intrinsic global sign rule. Matched S1/E1 and S2/E2 pairs favored negative potentials (runner-operation-0035 vs -0042; -0049 vs -0056), whereas S3/E3 at +1.5 V gave near-unity selectivity and 0.0845 selective yield, exceeding its negative counterpart (runner-operation-0070 vs -0063).

## H2 [supported interaction; main mechanistic account]
Solvent and electrolyte jointly gate productive electrolysis through separable phase/transport and selectivity effects. E3 appears sufficient to suppress precipitation (S0/E3, runner-operation-0084), while E0 permits precipitation even with S3 (S3/E0, -0077); neither crossover reproduced the productive S3/E3 response. Therefore the high-selectivity positive branch requires an S3×E3 interaction rather than either material alone. Alternative explanations include an unmeasured nonlinear pH/speciation crossover; the final pH values do not by themselves establish causality.

## H3 [supported qualitatively; quantitative law unresolved]
More charge/time increased conversion and target yield on productive negative branches, but high driving force coincided with low faradaic/energy efficiency, consistent with parasitic current. The available design confounds magnitude, current cap, duration, and material in several comparisons, so no universal kinetic coefficient is claimed. `current_mA` is interpreted only as a cap.

## Predictive scope
At 0.04 mol in 0.08 L: (i) S1/E1 or S2/E2 should favor negative over equally strong positive potential; (ii) S3/E3 should uniquely enable a selective positive-potential branch around +1.5 V; (iii) swapping either member away from S3/E3 should sharply reduce that branch; (iv) longer electrolysis should generally raise conversion until parasitic loss/over-electrolysis dominates. Exact interpolation outside observed potentials, durations, and caps remains uncertain.

## Operating decision
Batch 10 is the most mechanistically credible recommendation: S3/E3, +1.5 V, 250 mA cap, 14400 s achieved the best combination of substantial selective yield and near-unity selectivity without precipitation (runner-operation-0070). Batch 2 had a higher balanced score but near-zero measured conversion and a yield close to assay-scale uncertainty, so it is less robust as an operating choice.

## 实际批次及公开测量

### 批次 1 · 终点事件 7

```json
{
  "ordinal": 1,
  "lifecycle_index": 1,
  "end_step": 7,
  "actions": [
    {
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
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
    "cost": 0.3524399995803833,
    "electrochemical_conversion": 0.011068047024309635,
    "electrochemical_selectivity": 0.6258968710899353,
    "energy_efficiency": 0.25900930166244507,
    "faradaic_efficiency": 0.4174010157585144,
    "ohmic_efficiency": 0.9695378541946411,
    "pH_normalized": 0.23218974471092224,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.38869723677635193
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
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
    "cost": 0.3524399995803833,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.9492443203926086,
    "energy_efficiency": 0.7850880026817322,
    "faradaic_efficiency": 0.8099481463432312,
    "ohmic_efficiency": 0.9783756732940674,
    "pH_normalized": 0.2294943928718567,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.3900074362754822,
    "selective_product_yield": 0.014894237741827965,
    "transport_efficiency": 0.8362049460411072
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -2
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
    "cost": 0.38100001215934753,
    "electrochemical_conversion": 0.06744828075170517,
    "electrochemical_selectivity": 0.4877714514732361,
    "energy_efficiency": 0.03491140902042389,
    "faradaic_efficiency": 0.12886205315589905,
    "ohmic_efficiency": 0.9331657886505127,
    "pH_normalized": 0.23020939528942108,
    "precipitation_signal": 0.9868234395980835,
    "safety_risk": 0.072194404900074,
    "score": 0.1975284367799759,
    "selective_product_yield": 0.025741897523403168,
    "transport_efficiency": 0.1454189568758011
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 2
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
    "cost": 0.38100001215934753,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.02824951522052288,
    "ohmic_efficiency": 0.9453239440917969,
    "pH_normalized": 0.2295188158750534,
    "precipitation_signal": 0.987571656703949,
    "safety_risk": 0.072194404900074,
    "score": 0.0031294943764805794,
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -2
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
    "cost": 0.44179999828338623,
    "electrochemical_conversion": 0.21833884716033936,
    "electrochemical_selectivity": 0.4840036630630493,
    "energy_efficiency": 0.05815504491329193,
    "faradaic_efficiency": 0.24139882624149323,
    "ohmic_efficiency": 0.9109281301498413,
    "pH_normalized": 0.20790329575538635,
    "precipitation_signal": 0.7135940194129944,
    "safety_risk": 0.09559440612792969,
    "score": 0.2614156901836395,
    "selective_product_yield": 0.11108984053134918,
    "transport_efficiency": 0.23088936507701874
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 2
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
    "cost": 0.44179999828338623,
    "electrochemical_conversion": 0.0021511756349354982,
    "electrochemical_selectivity": 0.0042426493018865585,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.02405594103038311,
    "ohmic_efficiency": 0.9127849340438843,
    "pH_normalized": 0.20462734997272491,
    "precipitation_signal": 0.7242242693901062,
    "safety_risk": 0.09559440612792969,
    "score": 0.04127749055624008,
    "selective_product_yield": 0.010337181389331818,
    "transport_efficiency": 0.0
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 2,
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
    "cost": 0.5073999762535095,
    "electrochemical_conversion": 0.15810458362102509,
    "electrochemical_selectivity": 0.3454156816005707,
    "energy_efficiency": 0.04231446608901024,
    "faradaic_efficiency": 0.1605556458234787,
    "ohmic_efficiency": 0.9222502708435059,
    "pH_normalized": 0.16794772446155548,
    "precipitation_signal": 0.0,
    "safety_risk": 0.1135944053530693,
    "score": 0.2010067105293274,
    "selective_product_yield": 0.05864810198545456,
    "transport_efficiency": 0.16395600140094757
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 2,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": 2.5
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
    "cost": 0.5073999762535095,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.008051441982388496,
    "ohmic_efficiency": 0.9075462818145752,
    "pH_normalized": 0.16625024378299713,
    "precipitation_signal": 0.00031451715040020645,
    "safety_risk": 0.1135944053530693,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.0015560885658487678
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 3,
      "volume_L": 0.08
    },
    {
      "current_mA": 250,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": -1.5
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
    "cost": 0.42500001192092896,
    "electrochemical_conversion": 0.08684289455413818,
    "electrochemical_selectivity": 0.48991888761520386,
    "energy_efficiency": 0.14207665622234344,
    "faradaic_efficiency": 0.1816248744726181,
    "ohmic_efficiency": 0.9944390058517456,
    "pH_normalized": 0.2855640947818756,
    "precipitation_signal": 0.008188718929886818,
    "safety_risk": 0.12619440257549286,
    "score": 0.24353423714637756,
    "selective_product_yield": 0.061516325920820236,
    "transport_efficiency": 0.20245614647865295
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 3,
      "volume_L": 0.08
    },
    {
      "current_mA": 250,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": 1.5
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
    "cost": 0.42500001192092896,
    "electrochemical_conversion": 0.10411442071199417,
    "electrochemical_selectivity": 0.9992378354072571,
    "energy_efficiency": 0.23188431560993195,
    "faradaic_efficiency": 0.19930659234523773,
    "ohmic_efficiency": 0.9538899064064026,
    "pH_normalized": 0.28324997425079346,
    "precipitation_signal": 0.0,
    "safety_risk": 0.12619440257549286,
    "score": 0.34073832631111145,
    "selective_product_yield": 0.08454983681440353,
    "transport_efficiency": 0.20065619051456451
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 3,
      "volume_L": 0.08
    },
    {
      "current_mA": 250,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1.5
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
    "cost": 0.42500001192092896,
    "electrochemical_conversion": 0.013452183455228806,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.012963879853487015,
    "faradaic_efficiency": 0.002204522956162691,
    "ohmic_efficiency": 0.962087869644165,
    "pH_normalized": 0.24047139286994934,
    "precipitation_signal": 0.9916704893112183,
    "safety_risk": 0.12619440257549286,
    "score": 0.006538411136716604,
    "selective_product_yield": 0.0015959294978529215,
    "transport_efficiency": 0.009384461678564548
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "current_mA": 250,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": 1.5
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
    "cost": 0.37380000948905945,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.0,
    "ohmic_efficiency": 0.9840685129165649,
    "pH_normalized": 0.2733696401119232,
    "precipitation_signal": 0.0,
    "safety_risk": 0.072194404900074,
    "score": 0.04535050690174103,
    "selective_product_yield": 0.011055422015488148,
    "transport_efficiency": 0.0
  }
}
```

## K1 封存报告

Mechanistic account

All 12 batches used 0.040 mol of limiting reagent in 0.080 L of solvent (nominal initial concentration 0.50 mol L^-1). I varied solvent identity S0–S3, electrolyte identity E0–E3, potential, current cap, and electrolysis duration. Because the substances are anonymous benchmark materials, terms such as oxidation, reduction, protonation, adsorption, or ion pairing can only be proposed as latent processes; the experiments do not identify a real chemical structure.

1. Core explanation

I infer that the system has at least three coupled layers:

(a) A medium/electrolyte-controlled state. Solvent and electrolyte establish pH-like speciation, precipitation or phase availability, ionic transport, and resistance.

(b) A polarity- and potential-dependent electron-transfer branch. The productive direction is not universal: it depends strongly on the solvent–electrolyte combination and potential magnitude.

(c) Competition between target formation and parasitic current. Increasing time, current cap, or driving force can increase conversion, but high-charge conditions often have poor faradaic and energy efficiencies. Thus conversion and efficiency need not improve together.

A useful conceptual model is

q_eff = integral I_actual(t) dt,

X = 1 - exp[-k_eff(S,E,V,pH,phase) q_eff],

logit(Sel) = a(S,E) + b(S,E) sign(V) + c(S,E)|V| - d(S,E)|V|^2 - h(q_eff),

Y_target approximately equals X × Sel × R_phase,

where X is conversion, Sel is target selectivity, and R_phase is an availability/recovery factor affected by precipitation and medium. The measured selective-product yield does not equal measured conversion times measured selectivity exactly, so this is a latent-process relation rather than an exact identity between separately noisy assay channels. Actual current was not measured; `current_mA` was only a cap, so q_eff cannot be calculated from cap × time without an additional electrochemical model.

I would model precipitation separately, for example

P(precipitation) = logistic[p0 + pS(S) + pE(E) + pSE(S,E) + ppH(pH)],

and allow precipitation to influence both transport and R_phase. Ohmic efficiency remained generally high while faradaic and transport efficiencies varied greatly, suggesting that resistance alone is not the main limitation. Productive electron transfer and mass/phase transport are more important bottlenecks.

2. Evidence for polarity-dependent reaction pathways

Batch 1 used S0/E0, -1.0 V, a 100 mA cap, and 600 s. Its final conversion was 0.0111, selectivity 0.6259, and selective yield 0.0000, with faradaic efficiency 0.4174, transport efficiency 0.3887, energy efficiency 0.2590, and precipitation signal 1.000. This initially suggested that a short, mild negative treatment was insufficient.

Batch 2 reversed only the potential to +1.0 V at the same S0/E0, cap, and duration. It produced a nominal conversion of 0.0000, selectivity 0.9492, and yield 0.0149. Its faradaic, transport, and energy efficiencies were much higher—0.8099, 0.8362, and 0.7851—and its score was 0.3900. However, conversion was clipped at zero and yield was only about 1.5 times the stated final-assay yield standard deviation of 0.01. I therefore treat this as evidence for an efficient low-extent positive-potential response, not as robust evidence of substantial production.

At stronger conditions, S0/E0 behaved differently. Batch 3 (-2.0 V, 500 mA cap, 7200 s) gave conversion 0.0674, selectivity 0.4878, yield 0.0257, faradaic efficiency 0.1289, transport efficiency 0.1454, and energy efficiency 0.0349. Batch 4, its +2.0 V counterpart, was essentially inactive: conversion 0.0000, selectivity 0.0000, yield 0.00079, and energy and transport efficiencies 0.0000. This comparison changed my initial simple polarity hypothesis. In S0/E0, mild positive polarization may be efficient at very low extent, but strong positive polarization appears overdriven or routed into a parasitic pathway; strong negative polarization gives measurable conversion at poor efficiency.

The polarity contrast was repeated in other media. With S1/E1 at 500 mA and 14400 s, batch 5 at -2.0 V gave conversion 0.2183, selectivity 0.4840, and yield 0.1111, whereas batch 6 at +2.0 V gave conversion 0.00215, selectivity 0.00424, and yield 0.0103. With S2/E2 at the same cap and duration, batch 7 at -2.5 V gave conversion 0.1581, selectivity 0.3454, and yield 0.0586; batch 8 at +2.5 V gave zeros for conversion, selectivity, yield, and energy efficiency. These paired results strongly support a negative-potential productive branch for S1/E1 and S2/E2 and a parasitic or blocked strong-positive branch.

S3/E3 revealed a different regime. Batch 9 at -1.5 V, 250 mA, and 14400 s gave conversion 0.0868, selectivity 0.4899, and yield 0.0615. Batch 10 at +1.5 V under the same conditions gave conversion 0.1041, selectivity 0.9992, and yield 0.0845. Thus S3/E3 uniquely enabled a highly selective positive-potential route. This overturned any global rule that negative potential is always productive. The sign effect must be conditional on medium/electrolyte state, plausibly through a change in accessible substrate state, interfacial adsorption, or competing redox threshold.

3. Solvent–electrolyte coupling and precipitation

The paired-material survey initially confounded solvent and electrolyte because S0/E0, S1/E1, S2/E2, and S3/E3 were varied together. Nevertheless, it showed systematic environmental differences. Final pH_normalized values were approximately 0.23 for S0/E0, 0.205–0.208 for S1/E1, 0.166–0.168 for S2/E2, and 0.283–0.286 for S3/E3. Within each polarity pair the pH values were close, implying that material identity controlled this state more strongly than potential sign.

Precipitation showed an even stronger material pattern. It was approximately 0.99–1.00 for S0/E0, about 0.71–0.72 for S1/E1, and approximately zero for S2/E2 and S3/E3. Batches 11 and 12 were designed as crossovers to separate S3 and E3 at the successful batch-10 electrolysis settings.

Batch 11 used S3/E0 at +1.5 V, 250 mA, and 14400 s. It had precipitation 0.9917, conversion 0.0135, selectivity 0.0000, yield 0.00160, faradaic efficiency 0.00220, and transport efficiency 0.00938. Therefore S3 alone did not reproduce either the low-precipitation state or productive positive branch.

Batch 12 used S0/E3 at the same electrical conditions. It had precipitation 0.0000 and pH_normalized 0.2734, showing that E3 was sufficient to suppress precipitation even with S0. Nevertheless, conversion, selectivity, faradaic efficiency, transport efficiency, and energy efficiency were all reported as 0.0000; yield was only 0.0111, close to the assay noise scale. E3 therefore controls or strongly contributes to the soluble/low-precipitation state, but it is not sufficient for productive positive-potential conversion.

The combined crossover evidence supports a genuine S3×E3 interaction. E3 supplies a phase/speciation environment with little precipitation, while S3 supplies an additional interfacial or chemical compatibility required for the selective positive route. Neither component alone reproduces batch 10. An alternative interpretation is that E3 determines pH and precipitation while S3 shifts the positive-potential redox threshold. The data cannot distinguish that from direct solvent–electrolyte ion-pairing or an electrode-interface interaction.

4. Charge, conversion, and efficiency

Within S0/E0, moving from the short -1.0 V batch 1 to the stronger and longer -2.0 V batch 3 increased conversion from 0.0111 to 0.0674 and yield from 0.0000 to 0.0257, while energy efficiency fell from 0.2590 to 0.0349 and faradaic efficiency fell from 0.4174 to 0.1289. Although potential, cap, and duration all changed, this is consistent with additional charge increasing extent while an increasing fraction of current enters side reactions.

The long negative batches also illustrate medium dependence at nominally high charge. Batch 5 reached conversion 0.2183 and yield 0.1111; batch 7 reached 0.1581 and 0.0586; batch 9, with a lower cap and smaller magnitude, reached 0.0868 and 0.0615. These are not sufficient to estimate a universal kinetic constant because solvent, electrolyte, potential, and current cap changed simultaneously. They do support saturation- or loss-prone kinetics rather than a linear law in cap × time.

Ohmic efficiency was high in every reported final assay, approximately 0.91–0.99, including inactive batches. For example, batch 8 had ohmic efficiency 0.9075 despite no product, and batch 12 had 0.9841 despite no measured conversion or faradaic efficiency. Consequently, electrical conduction can remain adequate while charge goes to non-target pathways. Faradaic and transport efficiencies are more diagnostic of productive operation.

5. Scope and identifiability limits

The account applies only to the tested loading of 0.040 mol in 0.080 L and to the explored ranges of -2.5 to +2.5 V, 100–500 mA caps, and 600–14400 s. Concentration dependence, reagent-order kinetics, solvent-volume effects, electrode area, true current-time traces, and temperature effects were not identified. No zero-electrolysis control was performed, so very small yields cannot be cleanly separated from background or assay noise.

Many final estimates have bounded noise: stated standard deviations include 0.01 for conversion, 0.012 for selectivity, 0.01 for selective yield, 0.012 for faradaic efficiency, 0.014 for transport efficiency, and 0.016 for energy efficiency. Reported zeros are clipped values, not proof that the underlying quantity is exactly zero. This is particularly important for batches 2, 4, 6, 11, and 12. Large matched contrasts, such as batch 5 versus 6 or batch 7 versus 8, are much more persuasive than isolated near-zero differences.

Solvent and electrolyte main effects are incompletely identified. The crossover experiments isolate E3 and E0 behavior at one positive-potential setting, but there are no S1/E0, S2/E0, S3/E1, or analogous negative-potential crossovers. Potential magnitude, current cap, and duration are also confounded except within the matched polarity pairs. The campaign therefore identifies qualitative interactions but not a unique parametric rate law.

The measurements do not establish whether precipitation causes low conversion, merely accompanies a material state, or removes product after formation. Batch 12 shows that suppressing precipitation is not sufficient for productive conversion, which argues against precipitation being the sole bottleneck. Likewise, pH_normalized correlates with material profile but does not prove proton-coupled electron transfer.

6. Plausible alternatives

One alternative is a two-redox-window model rather than a continuous polarity interaction: each material pair may shift two competing onset potentials, one for target formation and one for solvent/electrolyte decomposition. S3/E3 could place the target onset below the parasitic onset at +1.5 V, whereas S0/E0 at +2.0 V lies beyond the parasitic threshold.

A second alternative is phase-limited accessibility. The electrolyte may control precipitation or aggregation, and solvent may control how the soluble species approaches the electrode. This explains why E3 suppresses precipitation but requires S3 for productive positive electrolysis.

A third alternative is product degradation or over-electrolysis. Strong positive potentials may initially form target but rapidly destroy it, producing the near-null final assays in batches 4, 6, and 8. Since no time-series final assays were available within a batch, failure to form product cannot be distinguished from transient formation followed by consumption.

A fourth alternative is current limitation. Because only current caps were commanded, different media may have drawn very different actual currents. Apparent material chemistry could partly reflect unequal delivered charge. The high ohmic-efficiency channel does not provide a full current trace, so this remains unresolved.

7. Overall predictive account

Within this benchmark, I predict that S1/E1 and S2/E2 will continue to favor negative over equally strong positive potentials, while S3/E3 has a distinct selective positive branch near +1.5 V. Replacing either S3 or E3 should sharply reduce that positive branch. E3 should continue to suppress precipitation across at least some solvents, but low precipitation alone will not guarantee reaction. Increasing effective charge on a productive branch should initially increase conversion, followed by diminishing returns and lower faradaic or energy efficiency as parasitic pathways grow. These are interpolative expectations grounded in the 12 batches; predictions outside the tested loading, potential, cap, and duration ranges are conjectural.

## K2 封存报告

1. Supported, contradicted, and untested claims

No substantive instance-specific prior mechanism or material-property dossier was supplied. The solvent and electrolyte identities were opaque, so all mechanistic laws below were self-developed from the campaign.

Supported:
- Material identity strongly controls the reaction state. The matched S1/E1 pair favored negative polarization: batch 5 at -2.0 V gave conversion 0.2183 and yield 0.1111, whereas batch 6 at +2.0 V gave conversion 0.0022 and yield 0.0103. The analogous S2/E2 contrast was also strong: batch 7 gave yield 0.0586 at -2.5 V, while batch 8 gave 0 at +2.5 V.
- A solvent–electrolyte interaction is needed to explain the selective positive-potential branch. Batch 10, S3/E3 at +1.5 V, gave selectivity 0.9992 and yield 0.0845. Neither crossover reproduced it: S3/E0 in batch 11 gave yield 0.0016 and S0/E3 in batch 12 gave only 0.0111 with zero reported selectivity.
- E3 is associated with suppression of precipitation but is not sufficient for productive electrolysis. Batch 12 had precipitation 0 with S0/E3 but almost no productive signal, while batch 11 with S3/E0 had precipitation 0.9917.
- Greater electrical exposure can increase reaction extent while lowering efficiency. Relative to batch 1, batch 3 produced more conversion and yield under a stronger, longer negative treatment, but had much lower faradaic and energy efficiencies. This supports competition between target production and parasitic current, although potential, cap, and duration were confounded.

Contradicted or substantially revised:
- My initial tentative idea that one potential sign would generally be productive was contradicted. Negative potential was favored in batches 5/6 and 7/8, but S3/E3 favored +1.5 V in batch 10 over -1.5 V in batch 9. Polarity therefore has to interact with material identity and magnitude.
- A simple monotonic rule that stronger positive potential improves conversion was contradicted. S0/E0 at +1.0 V in batch 2 showed high apparent efficiencies but little product, while +2.0 V in batch 4 was essentially inactive. Strong positive conditions were also inactive in batches 6 and 8.
- A precipitation-only explanation was contradicted by batch 12: precipitation was absent, yet productive conversion and efficiencies remained near zero.
- The early expectation that solvent and electrolyte might have independently additive effects was weakened by batches 10–12. Their behavior is more consistent with a non-additive S3×E3 coupling.

Untested or unresolved:
- No unique kinetic law, reaction order, activation threshold, or saturation constant was identified.
- Actual current and delivered charge were not measured, so current-cap effects cannot be separated from medium-dependent current draw.
- Product formation followed by degradation cannot be distinguished from failure to form product because final product assays were not collected as a time series.
- The causal role of pH remains untested. pH_normalized tracked material combinations, but the campaign did not independently manipulate pH.
- Concentration and solvent-volume laws remain untested because completed campaign batches used the same loading.
- Most solvent/electrolyte cross-combinations were not tested, and there were no genuine replicate batches.

The evidence that most changed my judgment was the reversal between batch pairs 5/6 and 9/10, followed by the crossover failures in batches 11 and 12. Those observations forced replacement of a global polarity rule with a material-dependent interaction model.

2. One additional discriminating experiment

I would run S0/E3 at +0.8 V, a 250 mA current cap, and the standard campaign loading, terminating after 14400 s for a final assay. This would distinguish my leading S3×E3-interaction explanation from the alternative that E3 alone enables positive electrolysis but shifts its optimal potential below the +1.5 V used in batch 12.

- If this experiment remained near-null, especially with suppressed precipitation, I would strengthen the conclusion that E3 creates a soluble state but S3 supplies a separate requirement for productive positive electron transfer.
- If it produced substantial conversion, faradaic efficiency, and selective yield, I would weaken the claim that S3 is required. I would instead favor an electrolyte-controlled redox-window model in which batch 12 was overdriven at +1.5 V.
- If conversion appeared but selectivity or recovered yield remained poor, I would adopt a mixed explanation: E3 may enable charge transfer, while S3 directs selectivity or prevents subsequent loss.

A single result would still not prove a unique molecular mechanism, but it directly tests the most important unresolved interpretation of the batch-12 crossover.

3. Unused evidence, reliability, and goal effects

The detailed raw spectral artifacts and most peak shapes from the intermediate UV–vis and final multichannel assays were not incorporated into the quantitative account. I mainly used processed estimates. The intermediate UV–vis measurements were also not exploited as a systematic time series because there was only one intermediate measurement per batch and their full values were not retained in my comparative model. Cost, small sample-consumption differences, and safety-risk values were largely unused because they did not discriminate the leading mechanism under the tested conditions. Final-assay peak assignments were synthetic proxies and did not identify chemical structures.

The operating recommendation of batch 10 is not highly replicated: it rests on one S3/E3 positive batch, one negative counterpart, and two crossovers. Its qualitative superiority over batches 11 and 12 is clear, but its exact yield and selectivity may not reproduce precisely. Batch 2's high score is especially unreliable as mechanistic evidence because its conversion was clipped at zero and its yield, 0.0149, was close to the assay uncertainty and below the score gate threshold.

Among the sealed predictions, the least reliable are those involving untested material cross-combinations—especially Q05–Q10—and the long-duration, low-potential extrapolations. Q11 and Q12 are also uncertain because the campaign did not isolate current-cap effects at fixed potential and duration. Q01 and Q02 are relatively better anchored by batches 1 and 2, although the change from ±1.0 to ±0.8 V and the near-zero product scale still introduce uncertainty.

The assigned goal emphasized discovering an explanatory, predictive account rather than maximizing the public score. That led me to spend batches on broad polarity contrasts, all four paired material environments, and the two diagnostic crossovers instead of repeatedly optimizing or replicating the best-scoring region. This improved qualitative mechanism discrimination but reduced precision, repeatability assessment, and local optimization. There was no clear conflict with safety or resource constraints, but there was a real design tradeoff: stronger evidence for interaction structure came at the expense of replicate-based uncertainty estimates and a denser response surface around batch 10.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.66,
        "lower80": 0.35,
        "upper80": 0.85
      },
      "energy_efficiency": {
        "estimate": 0.31,
        "lower80": 0.12,
        "upper80": 0.5
      },
      "faradaic_efficiency": {
        "estimate": 0.46,
        "lower80": 0.25,
        "upper80": 0.65
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.098,
        "lower80": 0.0,
        "upper80": 0.28
      },
      "selective_product_yield": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.025
      },
      "transport_efficiency": {
        "estimate": 0.43,
        "lower80": 0.22,
        "upper80": 0.64
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.93,
        "lower80": 0.65,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.76,
        "lower80": 0.48,
        "upper80": 0.94
      },
      "faradaic_efficiency": {
        "estimate": 0.8,
        "lower80": 0.55,
        "upper80": 0.96
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.335,
        "lower80": 0.08,
        "upper80": 0.56
      },
      "selective_product_yield": {
        "estimate": 0.013,
        "lower80": 0.0,
        "upper80": 0.035
      },
      "transport_efficiency": {
        "estimate": 0.82,
        "lower80": 0.58,
        "upper80": 0.98
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
        "upper80": 0.45
      },
      "faradaic_efficiency": {
        "estimate": 0.4,
        "lower80": 0.2,
        "upper80": 0.6
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.315,
        "lower80": 0.18,
        "upper80": 0.43
      },
      "selective_product_yield": {
        "estimate": 0.045,
        "lower80": 0.01,
        "upper80": 0.1
      },
      "transport_efficiency": {
        "estimate": 0.42,
        "lower80": 0.22,
        "upper80": 0.62
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.88,
        "lower80": 0.6,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.65,
        "lower80": 0.32,
        "upper80": 0.9
      },
      "faradaic_efficiency": {
        "estimate": 0.72,
        "lower80": 0.4,
        "upper80": 0.92
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.503,
        "lower80": 0.32,
        "upper80": 0.68
      },
      "selective_product_yield": {
        "estimate": 0.08,
        "lower80": 0.025,
        "upper80": 0.17
      },
      "transport_efficiency": {
        "estimate": 0.74,
        "lower80": 0.45,
        "upper80": 0.94
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.53,
        "lower80": 0.25,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.2,
        "lower80": 0.04,
        "upper80": 0.43
      },
      "faradaic_efficiency": {
        "estimate": 0.36,
        "lower80": 0.13,
        "upper80": 0.62
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.298,
        "lower80": 0.16,
        "upper80": 0.46
      },
      "selective_product_yield": {
        "estimate": 0.065,
        "lower80": 0.015,
        "upper80": 0.14
      },
      "transport_efficiency": {
        "estimate": 0.38,
        "lower80": 0.15,
        "upper80": 0.65
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.12,
        "lower80": 0.0,
        "upper80": 0.4
      },
      "energy_efficiency": {
        "estimate": 0.03,
        "lower80": 0.0,
        "upper80": 0.15
      },
      "faradaic_efficiency": {
        "estimate": 0.07,
        "lower80": 0.0,
        "upper80": 0.25
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.053,
        "lower80": 0.0,
        "upper80": 0.2
      },
      "selective_product_yield": {
        "estimate": 0.009,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "transport_efficiency": {
        "estimate": 0.08,
        "lower80": 0.0,
        "upper80": 0.3
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.48,
        "lower80": 0.18,
        "upper80": 0.75
      },
      "energy_efficiency": {
        "estimate": 0.19,
        "lower80": 0.03,
        "upper80": 0.42
      },
      "faradaic_efficiency": {
        "estimate": 0.32,
        "lower80": 0.08,
        "upper80": 0.58
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.281,
        "lower80": 0.12,
        "upper80": 0.46
      },
      "selective_product_yield": {
        "estimate": 0.05,
        "lower80": 0.008,
        "upper80": 0.13
      },
      "transport_efficiency": {
        "estimate": 0.38,
        "lower80": 0.12,
        "upper80": 0.68
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.18,
        "lower80": 0.0,
        "upper80": 0.5
      },
      "energy_efficiency": {
        "estimate": 0.05,
        "lower80": 0.0,
        "upper80": 0.22
      },
      "faradaic_efficiency": {
        "estimate": 0.1,
        "lower80": 0.0,
        "upper80": 0.32
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.071,
        "lower80": 0.0,
        "upper80": 0.24
      },
      "selective_product_yield": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "transport_efficiency": {
        "estimate": 0.12,
        "lower80": 0.0,
        "upper80": 0.38
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.48,
        "lower80": 0.18,
        "upper80": 0.75
      },
      "energy_efficiency": {
        "estimate": 0.17,
        "lower80": 0.02,
        "upper80": 0.38
      },
      "faradaic_efficiency": {
        "estimate": 0.3,
        "lower80": 0.07,
        "upper80": 0.57
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.267,
        "lower80": 0.1,
        "upper80": 0.45
      },
      "selective_product_yield": {
        "estimate": 0.045,
        "lower80": 0.005,
        "upper80": 0.12
      },
      "transport_efficiency": {
        "estimate": 0.34,
        "lower80": 0.1,
        "upper80": 0.62
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.68,
        "lower80": 0.3,
        "upper80": 0.92
      },
      "energy_efficiency": {
        "estimate": 0.35,
        "lower80": 0.08,
        "upper80": 0.65
      },
      "faradaic_efficiency": {
        "estimate": 0.48,
        "lower80": 0.15,
        "upper80": 0.78
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.352,
        "lower80": 0.12,
        "upper80": 0.55
      },
      "selective_product_yield": {
        "estimate": 0.03,
        "lower80": 0.0,
        "upper80": 0.1
      },
      "transport_efficiency": {
        "estimate": 0.5,
        "lower80": 0.18,
        "upper80": 0.82
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.5,
        "lower80": 0.25,
        "upper80": 0.75
      },
      "energy_efficiency": {
        "estimate": 0.13,
        "lower80": 0.02,
        "upper80": 0.32
      },
      "faradaic_efficiency": {
        "estimate": 0.26,
        "lower80": 0.08,
        "upper80": 0.52
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.274,
        "lower80": 0.16,
        "upper80": 0.43
      },
      "selective_product_yield": {
        "estimate": 0.085,
        "lower80": 0.02,
        "upper80": 0.18
      },
      "transport_efficiency": {
        "estimate": 0.3,
        "lower80": 0.1,
        "upper80": 0.57
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.85,
        "lower80": 0.55,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.52,
        "lower80": 0.22,
        "upper80": 0.8
      },
      "faradaic_efficiency": {
        "estimate": 0.58,
        "lower80": 0.3,
        "upper80": 0.82
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.466,
        "lower80": 0.3,
        "upper80": 0.64
      },
      "selective_product_yield": {
        "estimate": 0.12,
        "lower80": 0.035,
        "upper80": 0.23
      },
      "transport_efficiency": {
        "estimate": 0.62,
        "lower80": 0.34,
        "upper80": 0.88
      }
    }
  ],
  "rationale": "Predictions interpolate from the campaign at nearly the same concentration (0.48 versus 0.50 mol/L). The S0/E0 ±1 V, 100 mA, 600 s pair anchors Q01–Q02; longer times are expected to raise extent, while strong charge delivery can reduce faradaic and energy efficiency through parasitic pathways. Electrolyte and solvent crossovers are much less identified, so Q05–Q10 have wider intervals. E1 is provisionally assigned the negative-polarity preference seen in S1/E1, while E3 is expected to suppress precipitation but not by itself reproduce the productive S3/E3 positive branch. High-current predictions balance increased yield against reduced efficiency. Score estimates apply the published weighted components and selective-yield gate, with additional uncertainty for unrequested conversion and ohmic-efficiency channels; intervals also account for assay noise, clipped near-zero results, and substantial extrapolation of material interactions."
}
```
