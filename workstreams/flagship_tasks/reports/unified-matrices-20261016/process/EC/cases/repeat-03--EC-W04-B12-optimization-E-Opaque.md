# repeat-03/EC-W04-B12-optimization-E-Opaque

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-03\EC-W04-B12-optimization-E-Opaque\participant\optimization-E-Opaque

## 同期笔记

### v1 · 公开事件 0

# Electrochemical campaign hypotheses

## H1 [tentative]
Balanced score should show an interior optimum in potential magnitude and electrolysis time: insufficient driving force/time limits conversion, while excessive values reduce selectivity and energy efficiency and may raise safety risk. Test by broad screening, then local refinement.

## H2 [tentative]
Anonymous solvent and electrolyte profiles may substantially alter transport, ohmic efficiency, and selectivity. Screen profile combinations at a common loading before refining operating variables.

## Decision plan
Use 0.020 mol reagent in 0.040 L as a common initial loading, one UV-vis measurement per batch after electrolysis, and final assay after explicit termination. Early batches will map material profiles and signed potentials; later batches will refine the best region. A large score or component difference must be interpreted cautiously until replicated because assay uncertainty and coupled parameter changes remain possible.

### v2 · 公开事件 84

# Electrochemical campaign hypotheses

## H1 [supported in tested scope, optimum not yet bounded]
For the negative-potential branch, longer electrolysis and less extreme negative potential improved the balanced score across the later E2/S1 sequence. At fixed 0.020 mol in 0.040 L, 500 mA cap, 14,400 s, S1/E2, scores rose from 0.336 at -2.0 V (runner-operation-0042) to 0.363 at -1.8 V (runner-operation-0070), 0.389 at -1.6 V (runner-operation-0077), and 0.413 at -1.4 V (runner-operation-0084). The simultaneous rise in selective-product yield (about 0.247 to 0.366) and energy efficiency (about 0.088 to 0.190) supports the trend, but the optimum may lie at still lower magnitude and was not bounded.

## H2 [supported for electrolyte E2; solvent effect unresolved]
E2 produced the strongest tested region. At -2.0 V/500 mA/14,400 s, S0/E2 and S1/E2 scores were close (0.334, runner-operation-0056; 0.336, runner-operation-0042), so the apparent S1 advantage is not persuasive relative to measurement uncertainty and coupled run variation. S3/E2 was lower at 0.317 (runner-operation-0063), but this single comparison is insufficient for a general solvent ranking.

## H3 [supported sign asymmetry in one tested comparison]
The positive-potential S1/E1 run gave near-zero electrochemical conversion and score 0.037 (runner-operation-0014), whereas several negative-potential runs produced material yield and higher score. Because electrolyte and potential magnitude were confounded, this establishes a practical tested preference, not a universal polarity law.

## Confounds and limits
Early runs changed solvent, electrolyte, potential, current cap, and duration together, so they map outcomes rather than isolate causal effects. Final-assay standard deviations are nonzero; close numerical differences should not be overinterpreted. The current setting is only a cap, so delivered-current behavior remains unresolved. Loading was held at 0.020 mol reagent and 0.040 L solvent throughout.

## Recommendation decision
Select batch 12: S1, E2, -1.4 V, 500 mA cap, 14,400 s at the common loading. It had the highest observed public score (0.413) and selective-product yield (0.366), with safety risk 0.096 below the stated 0.65 limit (runner-operation-0084). This choice would change if replication showed the apparent -1.4 V advantage was noise or if a lower-magnitude potential gave a superior score.

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
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "metrics": {
    "cost": 0.2828879952430725,
    "electrochemical_conversion": 0.014089567586779594,
    "electrochemical_selectivity": 0.6323518753051758,
    "energy_efficiency": 0.21779567003250122,
    "faradaic_efficiency": 0.41531622409820557,
    "ohmic_efficiency": 0.9628238677978516,
    "pH_normalized": 0.23443032801151276,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.3866124749183655
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
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "current_mA": 200,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 1.8
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
    "cost": 0.3011919856071472,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.010023192502558231,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.0,
    "ohmic_efficiency": 0.9422476291656494,
    "pH_normalized": 0.2049882858991623,
    "precipitation_signal": 0.7272359132766724,
    "safety_risk": 0.09559440612792969,
    "score": 0.03690200671553612,
    "selective_product_yield": 0.00897990819066763,
    "transport_efficiency": 0.02610676921904087
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
      "solvent": 2,
      "volume_L": 0.04
    },
    {
      "current_mA": 200,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -1.8
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
    "cost": 0.3293839991092682,
    "electrochemical_conversion": 0.037904150784015656,
    "electrochemical_selectivity": 0.46694883704185486,
    "energy_efficiency": 0.09992965310811996,
    "faradaic_efficiency": 0.20528335869312286,
    "ohmic_efficiency": 0.9070793986320496,
    "pH_normalized": 0.17481791973114014,
    "precipitation_signal": 0.0,
    "safety_risk": 0.1135944053530693,
    "score": 0.10596715658903122,
    "selective_product_yield": 0.010033971630036831,
    "transport_efficiency": 0.2218402773141861
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
      "solvent": 3,
      "volume_L": 0.04
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": -2.2
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
    "cost": 0.33987998962402344,
    "electrochemical_conversion": 0.070277139544487,
    "electrochemical_selectivity": 0.3478567600250244,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.10764703154563904,
    "ohmic_efficiency": 0.922243595123291,
    "pH_normalized": 0.27807846665382385,
    "precipitation_signal": 0.0,
    "safety_risk": 0.12619440257549286,
    "score": 0.1621222048997879,
    "selective_product_yield": 0.02867630496621132,
    "transport_efficiency": 0.07615949213504791
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
      "electrolyte_profile": 1,
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
    "cost": 0.3546000123023987,
    "electrochemical_conversion": 0.38471999764442444,
    "electrochemical_selectivity": 0.43625330924987793,
    "energy_efficiency": 0.018262676894664764,
    "faradaic_efficiency": 0.21539674699306488,
    "ohmic_efficiency": 0.9232028722763062,
    "pH_normalized": 0.2066948413848877,
    "precipitation_signal": 0.8390869498252869,
    "safety_risk": 0.072194404900074,
    "score": 0.2785446345806122,
    "selective_product_yield": 0.17234227061271667,
    "transport_efficiency": 0.2048872858285904
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
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 2,
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
    "cost": 0.3562000095844269,
    "electrochemical_conversion": 0.4720633327960968,
    "electrochemical_selectivity": 0.5078783631324768,
    "energy_efficiency": 0.0875355452299118,
    "faradaic_efficiency": 0.27594277262687683,
    "ohmic_efficiency": 0.8450552821159363,
    "pH_normalized": 0.16330410540103912,
    "precipitation_signal": 0.0023995577357709408,
    "safety_risk": 0.09559440612792969,
    "score": 0.33646243810653687,
    "selective_product_yield": 0.2470017373561859,
    "transport_efficiency": 0.251259446144104
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
      "solvent": 2,
      "volume_L": 0.04
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": -1.6
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
    "cost": 0.370279997587204,
    "electrochemical_conversion": 0.2163330465555191,
    "electrochemical_selectivity": 0.40816283226013184,
    "energy_efficiency": 0.05577544495463371,
    "faradaic_efficiency": 0.11256872117519379,
    "ohmic_efficiency": 0.9014947414398193,
    "pH_normalized": 0.28708145022392273,
    "precipitation_signal": 0.0,
    "safety_risk": 0.1135944053530693,
    "score": 0.21599237620830536,
    "selective_product_yield": 0.09181198477745056,
    "transport_efficiency": 0.11596907675266266
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
      "electrolyte_profile": 2,
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
    "cost": 0.3402000069618225,
    "electrochemical_conversion": 0.47959843277931213,
    "electrochemical_selectivity": 0.5016255378723145,
    "energy_efficiency": 0.0832807645201683,
    "faradaic_efficiency": 0.2678162753582001,
    "ohmic_efficiency": 0.9114694595336914,
    "pH_normalized": 0.15738990902900696,
    "precipitation_signal": 0.00031451715040020645,
    "safety_risk": 0.072194404900074,
    "score": 0.33436161279678345,
    "selective_product_yield": 0.2249274104833603,
    "transport_efficiency": 0.26132091879844666
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
      "current_mA": 500,
      "electrolyte_profile": 2,
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
    "cost": 0.36579999327659607,
    "electrochemical_conversion": 0.42023012042045593,
    "electrochemical_selectivity": 0.46414119005203247,
    "energy_efficiency": 0.1210978627204895,
    "faradaic_efficiency": 0.21762137115001678,
    "ohmic_efficiency": 0.9077567458152771,
    "pH_normalized": 0.16709403693675995,
    "precipitation_signal": 0.008188718929886818,
    "safety_risk": 0.12619440257549286,
    "score": 0.3174954354763031,
    "selective_product_yield": 0.2170206755399704,
    "transport_efficiency": 0.23845264315605164
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
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -1.8
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
    "cost": 0.35043999552726746,
    "electrochemical_conversion": 0.5295357704162598,
    "electrochemical_selectivity": 0.5458509922027588,
    "energy_efficiency": 0.13269858062267303,
    "faradaic_efficiency": 0.28463611006736755,
    "ohmic_efficiency": 0.8170973658561707,
    "pH_normalized": 0.16032086312770844,
    "precipitation_signal": 0.0,
    "safety_risk": 0.09559440612792969,
    "score": 0.3633887469768524,
    "selective_product_yield": 0.26843348145484924,
    "transport_efficiency": 0.28598570823669434
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
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -1.6
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
    "cost": 0.3446800112724304,
    "electrochemical_conversion": 0.57603919506073,
    "electrochemical_selectivity": 0.5424617528915405,
    "energy_efficiency": 0.1649692803621292,
    "faradaic_efficiency": 0.3037678301334381,
    "ohmic_efficiency": 0.8090665340423584,
    "pH_normalized": 0.16130590438842773,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.09559440612792969,
    "score": 0.3894762396812439,
    "selective_product_yield": 0.3116180896759033,
    "transport_efficiency": 0.3109477758407593
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
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -1.4
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
    "cost": 0.338919997215271,
    "electrochemical_conversion": 0.5991601943969727,
    "electrochemical_selectivity": 0.5591042041778564,
    "energy_efficiency": 0.19028021395206451,
    "faradaic_efficiency": 0.295850545167923,
    "ohmic_efficiency": 0.7947605848312378,
    "pH_normalized": 0.1618262231349945,
    "precipitation_signal": 0.0,
    "safety_risk": 0.09559440612792969,
    "score": 0.4128803014755249,
    "selective_product_yield": 0.36588719487190247,
    "transport_efficiency": 0.3170754611492157
  }
}
```

## K1 封存报告

## Mechanistic account

I interpret this benchmark world as a coupled electrolysis-and-product-recovery system. The controllable variables are reagent loading, liquid volume and solvent identity, electrolyte profile, applied potential, current limit, and electrolysis duration. These jointly determine conversion, electrochemical selectivity, faradaic and transport efficiencies, solution resistance, energy efficiency, pH-related state, and precipitation. The reported selective-product yield then appears to be approximately conversion multiplied by selectivity, modified by phase/recovery effects and measurement noise. The balanced score is dominated by selective-product yield but also rewards conversion, selectivity, faradaic efficiency, transport efficiency, ohmic efficiency, and energy efficiency.

All twelve batches used 0.020 mol reagent and initially 0.040 L solvent, corresponding nominally to 0.50 mol/L. Loading effects therefore cannot be identified from this campaign.

### Proposed process structure

A useful conceptual model is:

1. The selected solvent and electrolyte establish conductivity, transport, pH-related state, and the tendency of material to precipitate.
2. Potential determines both productive electron transfer and competing pathways. Potential magnitude need not monotonically improve performance: excessive magnitude can consume energy, promote side reactions, or reduce effective selectivity.
3. Current limit and time set a nominal charge ceiling, `Q_max = I_limit × t`, but actual delivered current was not measured. Consequently, neither the true charge nor electron stoichiometry is identifiable.
4. Product formation may be represented schematically as

   `reactant --productive electron transfer--> target`

   competing with

   `reactant/intermediate --side electron transfer--> impurity or degradation products`.

5. A first-order empirical decomposition is

   `target formed ≈ initial reagent × conversion × electrochemical selectivity`,

   followed by a medium-dependent recovery or precipitation factor. Thus,

   `selective yield ≈ conversion × selectivity × recovery_factor + measurement error`.

This approximation is supported in the best region. Batch 11 had conversion 0.5760 and selectivity 0.5425, whose product is about 0.3125, nearly identical to its measured selective-product yield of 0.3116. In batch 12, conversion 0.5992 times selectivity 0.5591 is about 0.335, compared with measured yield 0.3659. The differences are compatible with process corrections and assay noise; the relationship should not be treated as an exact law.

A schematic efficiency model is:

`faradaic efficiency = productive charge / delivered charge`,

`transport efficiency = reactant reaching the productive electrochemical region / available reactant`,

`ohmic efficiency = useful electrical potential / total imposed potential`,

and

`energy efficiency ≈ a coupled function of faradaic, transport, ohmic, conversion, and potential magnitude`.

The measured components are correlated rather than independent. For example, changes in electrolyte can simultaneously affect conductivity, mass transfer, pH, precipitation, and selectivity.

## Evidence that shaped the explanation

### Polarity and sufficient electrolysis severity

Batch 1 used S0/E0, −1.2 V, 100 mA, and 600 s. It produced only 0.0141 conversion and zero measured selective-product yield, despite selectivity 0.6324. Its precipitation signal was saturated at 1.0. This result first indicated that nominal selectivity alone was insufficient: little substrate reacted, and precipitation or recovery behavior could suppress useful yield.

Batch 2 used S1/E1 at +1.8 V, 200 mA, and 1,800 s. It showed zero measured conversion, selectivity 0.0100, zero faradaic and energy efficiency, and only 0.0090 selective yield, giving score 0.0369. This strongly discouraged the tested positive-potential branch. However, solvent, electrolyte, magnitude, and duration all differed from batch 1, so the campaign does not identify a universal polarity law. The justified operational statement is only that negative potentials were markedly more successful among the combinations tested.

Increasing current and duration generally moved the negative-potential runs into a productive regime. Batch 3, S2/E2 at −1.8 V, 200 mA for 3,600 s, reached conversion 0.0379, yield 0.0100, and score 0.1060. Batch 4, S3/E3 at −2.2 V, 500 mA for 7,200 s, reached conversion 0.0703, yield 0.0287, and score 0.1621. Batch 5, S0/E1 at −2.5 V, 500 mA for 14,400 s, reached conversion 0.3847, yield 0.1723, and score 0.2785. These runs suggest that adequate charge exposure was necessary, although the changing media prevent a quantitative time or current law from being fitted.

### Electrolyte E2 as the best tested operating region

The strongest results occurred with electrolyte E2. At −2.0 V, 500 mA, and 14,400 s:

- Batch 6, S1/E2: score 0.3365, conversion 0.4721, selectivity 0.5079, yield 0.2470, faradaic efficiency 0.2759, transport efficiency 0.2513, and precipitation signal 0.0024.
- Batch 8, S0/E2: score 0.3344, conversion 0.4796, selectivity 0.5016, yield 0.2249, faradaic efficiency 0.2678, transport efficiency 0.2613, and precipitation signal 0.0003.
- Batch 9, S3/E2: score 0.3175, conversion 0.4202, selectivity 0.4641, yield 0.2170, faradaic efficiency 0.2176, transport efficiency 0.2385, and precipitation signal 0.0082.

These comparisons isolate solvent identity reasonably well because the other programmed variables were held constant. S1 and S0 had essentially equal scores relative to assay uncertainty; therefore, a decisive S1-over-S0 solvent effect is not established. S1 gave higher measured yield, while S0 gave somewhat higher conversion, transport efficiency, and ohmic efficiency. S3 was lower overall in this single comparison.

E2 also maintained pH-normalized values near 0.16 and negligible precipitation in batches 6 and 8–12. By contrast, E1-containing batches 2 and 5 had precipitation signals of 0.727 and 0.839, respectively. Because other variables differed, I treat this as evidence that the medium controls solubility or phase behavior, not proof that E1 intrinsically causes precipitation in every condition.

### Potential dependence within the best-defined series

The clearest relationship came from batches 6, 10, 11, and 12, all using S1/E2, 0.020 mol reagent, 0.040 L solvent, a 500 mA current limit, and 14,400 s:

- Batch 6, −2.0 V: score 0.3365; conversion 0.4721; selectivity 0.5079; yield 0.2470; energy efficiency 0.0875.
- Batch 10, −1.8 V: score 0.3634; conversion 0.5295; selectivity 0.5459; yield 0.2684; energy efficiency 0.1327.
- Batch 11, −1.6 V: score 0.3895; conversion 0.5760; selectivity 0.5425; yield 0.3116; energy efficiency 0.1650.
- Batch 12, −1.4 V: score 0.4129; conversion 0.5992; selectivity 0.5591; yield 0.3659; energy efficiency 0.1903.

Within this interval, making the potential less negative improved conversion, selective yield, energy efficiency, and the total score. This is inconsistent with a simple model in which greater overpotential always accelerates the desired reaction. A more plausible account is an interior potential response: beyond the productive window, increasingly negative potential promotes unproductive current or side reactions and reduces energy utilization. Alternatively, the benchmark may encode a preferred formal potential near this region, with efficiency declining as the set point moves away from it.

Ohmic efficiency decreased from 0.8451 at −2.0 V to 0.7948 at −1.4 V even as the overall score improved. Thus, the optimum is a balance, not simultaneous maximization of every component. Improvements in yield, conversion, selectivity, and energy efficiency outweighed the modest ohmic-efficiency loss.

Faradaic efficiency was not perfectly monotonic: 0.2759, 0.2846, 0.3038, and 0.2959 across −2.0, −1.8, −1.6, and −1.4 V. Given the final-assay standard deviation of 0.012, the final decrease is not decisive. Transport efficiency rose more consistently from 0.2513 to 0.3171. The data therefore suggest that the potential trend may involve both productive charge allocation and mass-transfer coupling.

The optimum was not bounded. Batch 12 was the least negative member of the controlled series and remained the best result. Potentials less negative than −1.4 V might improve the score further, reach an optimum, or eventually fail to drive the reaction. Any claim that −1.4 V is the true mechanistic optimum would be extrapolation beyond the evidence.

## Precipitation and pH coupling

Precipitation appears to be a medium-dependent loss or warning channel. Batch 1 combined precipitation signal 1.0 with zero selective yield. Batch 5 had precipitation 0.839 but still obtained yield 0.1723, showing that precipitation is not an absolute on/off barrier. The best E2/S1 series had precipitation between zero and 0.0052 and pH-normalized values between about 0.160 and 0.163.

A plausible process is that electrolyte and solvent determine an acid/base or ionic equilibrium, which controls product or reagent solubility. Precipitation could remove product from the measured liquid phase, impede mass transport, or merely report a solid-forming condition. The available observations cannot distinguish these possibilities. It is also possible that precipitation is correlated with a hidden impurity rather than directly causing low yield.

## Score behavior

The public score is consistent with a weighted balance of the reported electrochemical quantities, with selective-product yield carrying the largest weight and a low-yield multiplicative gate. This explains why batch 1 scored zero despite respectable measured selectivity and ohmic efficiency: its selective yield was zero. Batch 2 had a small positive score because its noisy measured yield was about 0.009, but it remained below the stated 0.02 gate threshold. Once yield became substantial, as in batches 6–12, the score closely tracked a combination of yield, conversion, selectivity, and efficiencies rather than any single metric.

Accordingly, maximizing conversion alone would be inadequate. A useful operating point must generate product selectively, transport material effectively, avoid wasting charge, and avoid excessive electrical energy use.

## Safety and cost

Safety risk was largely associated with material addition and solvent identity rather than the final potential trend. The best S1/E2 series had reported safety risk 0.0956, well below the 0.65 limit. S3 runs were higher at 0.1262, S2 runs around 0.1136, S1 around 0.0956, and S0 around 0.0722. This repeated ordering suggests a solvent-dependent safety contribution in the benchmark.

Costs among the mature runs were similar, approximately 0.34–0.37. Batch 12 cost 0.3389 and therefore did not obtain its superior score by accepting an unusually high reported cost.

## Scope and identifiability limits

The conclusions apply only to the anonymous benchmark labels and the tested loading. The solvent and electrolyte identifiers do not imply real chemical identities.

The following factors remain unidentifiable:

- The electron stoichiometry of the productive reaction.
- Actual current as a function of time; only a current limit was set.
- Whether the reaction is kinetic, transport-limited, or charge-limited at each operating point.
- The separate effects of current and duration, because they were not independently varied in the refined region.
- Loading and dilution dependence, since reagent amount and initial solvent volume were constant.
- The optimum below |1.4| V, because the controlled potential series ended at −1.4 V.
- Whether E2 acts primarily through conductivity, buffering, interfacial kinetics, solubility, or several mechanisms simultaneously.
- Whether precipitation directly removes target product, removes reagent, blocks the electrode, or is simply correlated with another state variable.
- Long-term degradation or repeated-batch reproducibility; no exact replicate of batch 12 was performed.

The final-assay uncertainties also matter. Reported standard deviations included approximately 0.010 for conversion and selective yield, 0.012 for selectivity and faradaic/ohmic efficiency, 0.014 for transport efficiency, and 0.016 for energy efficiency. The large sequential gains from batch 6 to batch 12 are supported across several components, but close comparisons such as the scores of batches 6 and 8 should not be interpreted as definitive material rankings.

## Plausible alternative explanations

One alternative is that the potential trend is not a direct selectivity effect but reflects current delivery: at very negative set points, resistance, polarization, or a benchmark current-control rule may reduce productive charge. Without delivered-current traces, this cannot be separated from chemical side reactions.

A second alternative is that S1/E2 mainly improves product solubility or assay recovery rather than intrinsic electrosynthesis. The approximate conversion-times-selectivity relationship argues for genuine formation, but recovery effects could still explain part of the yield advantage.

A third alternative is that the low yields in early batches arose chiefly from inadequate electrolysis duration rather than poor materials. The campaign intentionally moved several variables together early on, so E0, E1, and E3 were not tested under every favorable setting.

A fourth possibility is that the small nonzero yield in batch 2 and the discrepancies between conversion-times-selectivity and reported yield are measurement noise near zero rather than real chemistry.

## Overall interpretation

The world most plausibly contains a negatively driven target electroreaction with a finite favorable potential window. Productive performance depends strongly on the electrolyte/solvent environment because that environment couples charge transfer, transport, resistance, pH-related equilibria, and precipitation. Long electrolysis at the 500 mA limit was necessary to reach the useful regime at the fixed 0.50 mol/L nominal loading. Within the best-characterized S1/E2 region, reducing the magnitude of the negative potential from −2.0 to −1.4 V progressively improved the balance between target formation and electrical efficiency. Batch 12 therefore represents the best observed point, not a proven global optimum.

## K2 封存报告

1. **Claims and laws assessed.** No instance-specific mechanistic prior was supplied; only the operating objective, score definition, instrument contracts, and anonymous material labels were provided. My initial law that useful performance would have an interior dependence on potential was only partly supported. In the controlled S1/E2 series, making the potential less negative improved score from 0.3365 at −2.0 V (batch 6) through 0.3634 and 0.3895 at −1.8 and −1.6 V (batches 10–11) to 0.4129 at −1.4 V (batch 12). Yield and energy efficiency rose concurrently. This contradicted any simple law that greater negative magnitude always improves conversion, but the proposed interior optimum remained untested because performance was still improving at the least-negative tested point. The claim that solvent/electrolyte identity matters was supported: E2 conditions gave the strongest region and negligible precipitation in batches 6 and 8–12, whereas E1 batches 2 and 5 had precipitation signals of 0.727 and 0.839. A precise solvent ranking was not supported: at otherwise matched conditions, S1/E2 and S0/E2 scored 0.3365 and 0.3344 (batches 6 and 8), too close for a strong conclusion. The practical negative-polarity preference was supported by the near-inactive +1.8 V batch 2 versus productive negative-potential batches, but a universal polarity law remained untested because batch 2 also differed in electrolyte and exposure. The approximate law `selective yield ≈ conversion × selectivity` was supported especially by batch 11: 0.5760 × 0.5425 ≈ 0.3125 versus measured yield 0.3116. Batch 12 deviated more, 0.5992 × 0.5591 ≈ 0.335 versus yield 0.3659, so this is an approximate process relation, not an identity. Evidence that most changed my judgment was the monotonic four-batch potential sequence (6, 10, 11, 12), which shifted the explanation away from “more overpotential is better,” and the matched solvent comparison in batches 6, 8, and 9, which weakened confidence that S1 itself was uniquely optimal.

2. **One additional discriminating experiment.** I would run the batch-12 formulation and exposure—0.020 mol reagent, 0.040 L S1, E2, 500 mA limit, and 14,400 s—but at −1.0 V, followed by the final assay. This would distinguish my leading finite favorable-potential-window explanation from the alternative that performance simply continues improving as the potential becomes less negative over this range. A materially lower score, yield, conversion, and faradaic efficiency than batch 12 would support an optimum between approximately −1.4 and −1.0 V. A further improvement continuing the batch 6→10→11→12 trend would weaken my claimed nearby interior optimum and move the preferred region toward −1.0 V or still lower magnitude. Similar score with higher energy efficiency but lower conversion would indicate a plateau with a trade-off rather than a sharp optimum. Because actual delivered current is unavailable, even this result would not fully distinguish chemical selectivity effects from potential-dependent current delivery.

3. **Unused evidence, reliability, and goal effects.** I did not quantitatively exploit the raw spectral traces or inspect the full characterization artifacts. Most intermediate UV–visible spectra, peak shapes, baseline information, and replicate-level signals were unused; the decisions relied mainly on processed final-assay estimates. Temperature evolution, detailed cost increments, sample-volume changes, and spectral evidence for reactant depletion were also not modeled. There were no exact replicates, and loading was never varied. Consequently, the least reliable blind predictions are the +0.8 V cases, because the only positive-potential evidence was batch 2 at +1.8 V with E1, and the E0/E3 positive branches were never observed. Predictions at −0.8 V are also extrapolations beyond the controlled series ending at −1.4 V. The current-effect prediction, especially the difference between the 100 and 500 mA cases, is weak because current and duration were not independently varied under matched conditions and delivered current was not measured. The batch-12 recommendation is reliable as the highest observed score, but less reliable as a global optimum because it was neither replicated nor bracketed on the less-negative side. The assigned score-maximization goal clearly affected evidence collection: early batches used broad, confounded changes to locate a productive region, and later batches exploited S1/E2 rather than completing a factorial study. This improved the best observed score but left polarity, loading, current, duration, and material mechanisms less identifiable. I see no improper conflict with the goal, but there was a real exploration-versus-identification trade-off.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.48,
        "upper80": 0.74
      },
      "energy_efficiency": {
        "estimate": 0.25,
        "lower80": 0.14,
        "upper80": 0.35
      },
      "faradaic_efficiency": {
        "estimate": 0.41,
        "lower80": 0.3,
        "upper80": 0.51
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.16,
        "lower80": 0.0,
        "upper80": 0.32
      },
      "selective_product_yield": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "transport_efficiency": {
        "estimate": 0.38,
        "lower80": 0.26,
        "upper80": 0.49
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.055
      },
      "energy_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.055
      },
      "faradaic_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.075
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.017
      },
      "transport_efficiency": {
        "estimate": 0.03,
        "lower80": 0.0,
        "upper80": 0.09
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.64,
        "lower80": 0.52,
        "upper80": 0.74
      },
      "energy_efficiency": {
        "estimate": 0.28,
        "lower80": 0.18,
        "upper80": 0.37
      },
      "faradaic_efficiency": {
        "estimate": 0.42,
        "lower80": 0.32,
        "upper80": 0.51
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.36,
        "lower80": 0.26,
        "upper80": 0.46
      },
      "selective_product_yield": {
        "estimate": 0.12,
        "lower80": 0.045,
        "upper80": 0.22
      },
      "transport_efficiency": {
        "estimate": 0.4,
        "lower80": 0.29,
        "upper80": 0.49
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.075
      },
      "energy_efficiency": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "faradaic_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.025,
        "lower80": 0.0,
        "upper80": 0.1
      },
      "selective_product_yield": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.024
      },
      "transport_efficiency": {
        "estimate": 0.03,
        "lower80": 0.0,
        "upper80": 0.1
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.5,
        "lower80": 0.36,
        "upper80": 0.63
      },
      "energy_efficiency": {
        "estimate": 0.14,
        "lower80": 0.055,
        "upper80": 0.24
      },
      "faradaic_efficiency": {
        "estimate": 0.24,
        "lower80": 0.14,
        "upper80": 0.35
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.255,
        "lower80": 0.16,
        "upper80": 0.36
      },
      "selective_product_yield": {
        "estimate": 0.06,
        "lower80": 0.015,
        "upper80": 0.14
      },
      "transport_efficiency": {
        "estimate": 0.22,
        "lower80": 0.12,
        "upper80": 0.33
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.065
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.055
      },
      "faradaic_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.025,
        "lower80": 0.0,
        "upper80": 0.095
      },
      "selective_product_yield": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.023
      },
      "transport_efficiency": {
        "estimate": 0.025,
        "lower80": 0.0,
        "upper80": 0.085
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.43,
        "lower80": 0.29,
        "upper80": 0.57
      },
      "energy_efficiency": {
        "estimate": 0.11,
        "lower80": 0.025,
        "upper80": 0.21
      },
      "faradaic_efficiency": {
        "estimate": 0.13,
        "lower80": 0.055,
        "upper80": 0.23
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.2,
        "lower80": 0.1,
        "upper80": 0.3
      },
      "selective_product_yield": {
        "estimate": 0.03,
        "lower80": 0.004,
        "upper80": 0.09
      },
      "transport_efficiency": {
        "estimate": 0.14,
        "lower80": 0.06,
        "upper80": 0.25
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.055
      },
      "faradaic_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.09
      },
      "selective_product_yield": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.022
      },
      "transport_efficiency": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.08
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.57,
        "lower80": 0.42,
        "upper80": 0.7
      },
      "energy_efficiency": {
        "estimate": 0.24,
        "lower80": 0.13,
        "upper80": 0.35
      },
      "faradaic_efficiency": {
        "estimate": 0.36,
        "lower80": 0.24,
        "upper80": 0.47
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.32,
        "lower80": 0.21,
        "upper80": 0.43
      },
      "selective_product_yield": {
        "estimate": 0.095,
        "lower80": 0.03,
        "upper80": 0.19
      },
      "transport_efficiency": {
        "estimate": 0.33,
        "lower80": 0.21,
        "upper80": 0.44
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "energy_efficiency": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.065
      },
      "faradaic_efficiency": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.025,
        "lower80": 0.0,
        "upper80": 0.105
      },
      "selective_product_yield": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.025
      },
      "transport_efficiency": {
        "estimate": 0.025,
        "lower80": 0.0,
        "upper80": 0.095
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.66,
        "lower80": 0.55,
        "upper80": 0.76
      },
      "energy_efficiency": {
        "estimate": 0.3,
        "lower80": 0.2,
        "upper80": 0.39
      },
      "faradaic_efficiency": {
        "estimate": 0.43,
        "lower80": 0.33,
        "upper80": 0.52
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.48,
        "lower80": 0.39,
        "upper80": 0.58
      },
      "selective_product_yield": {
        "estimate": 0.4,
        "lower80": 0.27,
        "upper80": 0.55
      },
      "transport_efficiency": {
        "estimate": 0.41,
        "lower80": 0.31,
        "upper80": 0.5
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "energy_efficiency": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "faradaic_efficiency": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.055
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.018,
        "lower80": 0.0,
        "upper80": 0.085
      },
      "selective_product_yield": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.02
      },
      "transport_efficiency": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.08
      }
    }
  ],
  "rationale": "The campaign showed a strong practical polarity asymmetry: tested negative potentials produced target chemistry, whereas the positive-potential batch was near zero. I extrapolated the improving negative-potential trend toward −0.8 V, scaled product formation mainly by nominal charge per mole, and allowed electrolyte and solvent effects inferred from the sparse material comparisons. Q11 receives the largest yield because its charge exposure approaches that of the productive campaign runs; the 100 mA batches are charge-limited, and 600 s is especially insufficient. Intervals combine assay noise with much larger model uncertainty from extrapolating beyond −1.4 V, changing loading slightly, and lacking isolated E0/E1/E3 response curves. Positive-potential intervals remain near zero but allow small clipped assay signals and weak unobserved activity."
}
```
