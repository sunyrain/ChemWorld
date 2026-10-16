# repeat-03/EC-W03-B12-discovery-E-Opaque

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-03\EC-W03-B12-discovery-E-Opaque\participant\discovery-E-Opaque

## 同期笔记

### v1 · 公开事件 0

# Electrochemical hypothesis notebook

## Prior expectations (before physical experiment)
H1 [tentative]: Product formation requires nonzero applied potential and delivered charge; conversion should rise with electrolysis duration or current cap until a plateau, while excessive forcing may lower selectivity/efficiency through degradation.

H2 [tentative]: Potential sign is mechanistically decisive: one polarity should favor target formation and the opposite should give low yield or a different selectivity pattern.

H3 [tentative]: Anonymous solvent and electrolyte profiles may independently affect transport, ohmic efficiency, pH, and precipitation. A screening across all four labels followed by local comparisons should expose these effects.

Design decision: hold loading initially at 0.020 mol in 0.040 L (0.50 mol/L), use one intermediate UV-vis or pH observation per batch, and span polarity, potential magnitude, current cap, duration, solvent, and electrolyte. Repeat or localize promising conditions. Evidence differences will be interpreted cautiously relative to declared assay noise.

### v2 · 公开事件 56

# Electrochemical hypothesis notebook

## H1 [supported in tested scope]
At 0.50 mol/L loading, electrolysis time increases target conversion/yield between 300 and 3600 s at +1.0 V, 100 mA cap. Batch 2 (event runner-operation-0014) gave yield 0.0139 at 300 s, whereas the otherwise matching S0/E0 batch 8 (runner-operation-0056) gave 0.0361 at 3600 s. Because each is single-run and differences include assay noise, functional form and plateau remain unresolved. Test 1200 and 14400 s.

## H2 [supported, nonlinear potential-window form]
Polarity and magnitude are decisive. At S0/E0, 100 mA, 300 s, +1.0 V produced much higher efficiency/selectivity and nonzero estimated yield (runner-operation-0014) than -1.0 V (runner-operation-0007) or -2.0 V (runner-operation-0021). Yet +2.0 V collapsed performance (runner-operation-0028), opposing a monotonic “more positive is better” account. Working claim: a positive-potential window near +1 V favors target, while negative polarity and excessive positive potential favor nonproductive pathways. Exact optimum is unresolved.

## H3 [medium effects supported but identities confounded]
At +1.0 V, 100 mA, 3600 s, diagonal S1/E1 gave the highest observed yield, selectivity, and efficiencies (runner-operation-0035), followed by S2/E2, S0/E0, and S3/E3 (runner-operation-0042, -0056, -0049). Since solvent and electrolyte changed together and there is no repeat, their separate causal contributions remain unresolved. pH/precipitation vary strongly with medium and may mediate or merely correlate.

## Next tests
Within S1/E1 at fixed 0.50 mol/L and +1.0 V, map duration (1200, 14400 s) and current-cap dependence (10, 500 mA at 3600 s). Prediction: low current lowers conversion; high current may accelerate conversion but can reduce efficiency/selectivity, while long duration may approach a plateau or degradation regime. A result showing proportional yield across the entire range would favor simple charge control instead.

### v3 · 公开事件 84

# Electrochemical hypothesis notebook

## H1 [supported in tested S1/E1, +1.0 V scope]
Target formation grows strongly with both duration and current cap at fixed 0.50 mol/L. At 100 mA, yields were 0.0440, 0.0887, and 0.3186 for 1200, 3600, and 14400 s (runner-operation-0063, -0035, -0070). At 3600 s, yields were 0.00945, 0.0887, and 0.4538 for caps of 10, 100, and 500 mA (runner-operation-0077, -0035, -0084). These numerical separations exceed individual declared yield noise (0.01), though most conditions lack replication.

A descriptive charge-cap exposure variable D = current_cap × time organizes these five points: least-squares yield ≈ 0.00456 + 2.374e-7 D (D in mA·s), with predictions 0.0131, 0.0331, 0.0900, 0.3465, 0.4319 for observed yields 0.00945, 0.04398, 0.08873, 0.31863, 0.45383. This is an empirical local relation, not proof that delivered charge equals the cap-time product. Current and time are not interchangeable mechanistically: the 500 mA condition lowers energy and ohmic efficiencies relative to 100 mA long-duration conditions. Saturation beyond the tested exposure is unresolved.

## H2 [supported, nonlinear potential-window form]
At S0/E0, 100 mA, 300 s, +1.0 V produced much higher efficiency/selectivity and nonzero estimated yield (runner-operation-0014) than -1.0 V or -2.0 V (runner-operation-0007, -0021). +2.0 V collapsed performance (runner-operation-0028), rejecting monotonic magnitude response. Working mechanism: the target pathway is enabled in a moderate positive-potential window; negative polarity is poorly productive and excessive positive potential diverts current to nonproductive chemistry. A quantitative voltage curve between 0 and +2 V remains unmeasured.

## H3 [medium effects supported; components unresolved]
At +1.0 V, 100 mA, 3600 s, diagonal S1/E1 had the highest observed yield, selectivity, and efficiencies (runner-operation-0035), followed by S2/E2, S0/E0, and S3/E3 (runner-operation-0042, -0056, -0049). Solvent and electrolyte changed together, so separate effects and interactions cannot be identified. The strong pH/precipitation differences may mediate transport/speciation or may only correlate with medium identity.

## Integrated predictive account
Within the observed domain, polarity/potential first gates whether productive electrochemistry occurs; medium sets transport/faradaic/ohmic multipliers; accumulated electrochemical exposure then controls conversion and yield. Moderate +1.0 V with S1/E1 is the best tested window. Increasing cap raises yield rapidly but can trade off ohmic and energy efficiency; extending time at 100 mA raises yield while retaining high efficiencies. Selectivity stays about 0.94–0.97 in the S1/E1 +1 V exposure series.

## Limits and decisions
All batches used 0.020 mol reagent in 0.040 L nominal solvent (0.50 mol/L before sampling). No replicate was performed, current is a cap rather than measured delivery, and conversion/yield estimates sometimes differ in ways consistent with independent assay noise. Do not extrapolate the linear exposure relation outside tested cap 10–500 mA and duration 1200–14400 s, or across potential/medium changes. Recommend batch 12 for operating output because it has the highest tested yield and score, while batch 10 is preferable if energy/ohmic efficiency is weighted more heavily.

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
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "metrics": {
    "cost": 0.28271999955177307,
    "electrochemical_conversion": 0.010835841298103333,
    "electrochemical_selectivity": 0.5406470894813538,
    "energy_efficiency": 0.228801429271698,
    "faradaic_efficiency": 0.3875284194946289,
    "ohmic_efficiency": 0.9659870862960815,
    "pH_normalized": 0.23031213879585266,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.3588246703147888
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
    "cost": 0.28271999955177307,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.8391516804695129,
    "energy_efficiency": 0.7193763256072998,
    "faradaic_efficiency": 0.760771632194519,
    "ohmic_efficiency": 0.9748249650001526,
    "pH_normalized": 0.2276168018579483,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.33733057975769043,
    "selective_product_yield": 0.013884035870432854,
    "transport_efficiency": 0.787028431892395
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
      "duration_s": 300,
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
    "cost": 0.27584001421928406,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.4101746380329132,
    "energy_efficiency": 0.050675615668296814,
    "faradaic_efficiency": 0.2038010209798813,
    "ohmic_efficiency": 0.9740350842475891,
    "pH_normalized": 0.2283317893743515,
    "precipitation_signal": 0.9871104955673218,
    "safety_risk": 0.072194404900074,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.22035792469978333
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
      "potential_V": 2
    },
    {
      "duration_s": 300,
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
    "cost": 0.27584001421928406,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.02824951522052288,
    "ohmic_efficiency": 0.9861932396888733,
    "pH_normalized": 0.22764120995998383,
    "precipitation_signal": 0.9878587126731873,
    "safety_risk": 0.072194404900074,
    "score": 0.003258600365370512,
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
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 1,
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
    "cost": 0.30004000663757324,
    "electrochemical_conversion": 0.08812111616134644,
    "electrochemical_selectivity": 0.954411506652832,
    "energy_efficiency": 0.8855838179588318,
    "faradaic_efficiency": 0.9187591075897217,
    "ohmic_efficiency": 0.9616739749908447,
    "pH_normalized": 0.21465101838111877,
    "precipitation_signal": 0.6510295271873474,
    "safety_risk": 0.09559440612792969,
    "score": 0.5894411206245422,
    "selective_product_yield": 0.08873247355222702,
    "transport_efficiency": 0.9082496166229248
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
      "current_mA": 100,
      "electrolyte_profile": 2,
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
    "cost": 0.3256399929523468,
    "electrochemical_conversion": 0.07260945439338684,
    "electrochemical_selectivity": 0.7939794063568115,
    "energy_efficiency": 0.7353307008743286,
    "faradaic_efficiency": 0.7794104814529419,
    "ohmic_efficiency": 0.9377337098121643,
    "pH_normalized": 0.17481280863285065,
    "precipitation_signal": 0.0023995577357709408,
    "safety_risk": 0.1135944053530693,
    "score": 0.5004723072052002,
    "selective_product_yield": 0.06598067283630371,
    "transport_efficiency": 0.7547271251678467
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
      "current_mA": 100,
      "electrolyte_profile": 3,
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
    "cost": 0.30963999032974243,
    "electrochemical_conversion": 0.05938802286982536,
    "electrochemical_selectivity": 0.7194212079048157,
    "energy_efficiency": 0.6464661359786987,
    "faradaic_efficiency": 0.5278396010398865,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.28484079241752625,
    "precipitation_signal": 0.0,
    "safety_risk": 0.12619440257549286,
    "score": 0.4200892150402069,
    "selective_product_yield": 0.042675167322158813,
    "transport_efficiency": 0.5312399864196777
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
      "current_mA": 100,
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
    "cost": 0.28404000401496887,
    "electrochemical_conversion": 0.06370284408330917,
    "electrochemical_selectivity": 0.8236374855041504,
    "energy_efficiency": 0.7047011852264404,
    "faradaic_efficiency": 0.7447009086608887,
    "ohmic_efficiency": 0.991905152797699,
    "pH_normalized": 0.2266431748867035,
    "precipitation_signal": 0.9957303404808044,
    "safety_risk": 0.072194404900074,
    "score": 0.4890020787715912,
    "selective_product_yield": 0.03614644706249237,
    "transport_efficiency": 0.7382055521011353
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
      "potential_V": 1
    },
    {
      "duration_s": 1200,
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
    "cost": 0.29207998514175415,
    "electrochemical_conversion": 0.026322491466999054,
    "electrochemical_selectivity": 0.9388172626495361,
    "energy_efficiency": 0.9449468851089478,
    "faradaic_efficiency": 0.8990811705589294,
    "ohmic_efficiency": 0.9933291673660278,
    "pH_normalized": 0.2107059806585312,
    "precipitation_signal": 0.6674489378929138,
    "safety_risk": 0.09559440612792969,
    "score": 0.5777387022972107,
    "selective_product_yield": 0.04398169741034508,
    "transport_efficiency": 0.9199123978614807
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
      "current_mA": 100,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 1
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
    "cost": 0.3043600022792816,
    "electrochemical_conversion": 0.35405829548835754,
    "electrochemical_selectivity": 0.967009425163269,
    "energy_efficiency": 0.9281243681907654,
    "faradaic_efficiency": 0.9167628884315491,
    "ohmic_efficiency": 0.95278000831604,
    "pH_normalized": 0.20839183032512665,
    "precipitation_signal": 0.6566107869148254,
    "safety_risk": 0.09559440612792969,
    "score": 0.6933102011680603,
    "selective_product_yield": 0.3186304271221161,
    "transport_efficiency": 0.9181124567985535
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
      "current_mA": 10,
      "electrolyte_profile": 1,
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
    "cost": 0.29874399304389954,
    "electrochemical_conversion": 0.021795516833662987,
    "electrochemical_selectivity": 0.9324120283126831,
    "energy_efficiency": 0.9505550861358643,
    "faradaic_efficiency": 0.8966593146324158,
    "ohmic_efficiency": 0.9990093111991882,
    "pH_normalized": 0.20937687158584595,
    "precipitation_signal": 0.6644999384880066,
    "safety_risk": 0.09559440612792969,
    "score": 0.26705285906791687,
    "selective_product_yield": 0.009447136893868446,
    "transport_efficiency": 0.9038392901420593
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
      "electrolyte_profile": 1,
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
    "cost": 0.3057999908924103,
    "electrochemical_conversion": 0.43561163544654846,
    "electrochemical_selectivity": 0.9622111916542053,
    "energy_efficiency": 0.7927608489990234,
    "faradaic_efficiency": 0.9350715279579163,
    "ohmic_efficiency": 0.8340470194816589,
    "pH_normalized": 0.20989719033241272,
    "precipitation_signal": 0.6578359007835388,
    "safety_risk": 0.09559440612792969,
    "score": 0.7175165414810181,
    "selective_product_yield": 0.4538252651691437,
    "transport_efficiency": 0.956296443939209
  }
}
```

## K1 封存报告

## Mechanistic account

I interpret this system as a potential-gated electrochemical conversion whose rate is controlled mainly by electrochemical exposure, while the anonymous solvent/electrolyte pair controls transport, faradaic performance, acid–base state, and precipitation. The data support three linked ideas: (1) productive chemistry occurs only in a moderate positive-potential window; (2) within that window, product formation increases with current cap and time; and (3) the medium changes both the productive fraction of current and the physical state of the mixture.

### Experimental domain

Every batch used 0.020 mol of limiting reagent and 0.040 L of solvent, corresponding to a nominal initial loading of 0.50 mol/L. Thus concentration effects were not measured. Potentials ranged from −2.0 to +2.0 V, current caps from 10 to 500 mA, and electrolysis times from 300 to 14,400 s. All reported numerical outcomes below are final-assay estimates, not hidden true compositions. The declared standard deviations were approximately 0.01 for yield and conversion, 0.012 for electrochemical selectivity and faradaic efficiency, 0.014 for transport efficiency, and 0.016 for energy efficiency.

## 1. Potential polarity and a productive voltage window

Batches 1–4 isolated the clearest qualitative feature of the mechanism. They all used solvent S0, electrolyte E0, a 100 mA cap, and 300 s electrolysis:

- Batch 1, −1.0 V: yield 0, conversion 0.0108, selectivity 0.5406, faradaic efficiency 0.3875, transport efficiency 0.3588, energy efficiency 0.2288.
- Batch 2, +1.0 V: yield 0.0139, reported conversion 0, selectivity 0.8392, faradaic efficiency 0.7608, transport efficiency 0.7870, energy efficiency 0.7194.
- Batch 3, −2.0 V: yield 0, reported conversion 0, selectivity 0.4102, faradaic efficiency 0.2038, transport efficiency 0.2204, energy efficiency 0.0507.
- Batch 4, +2.0 V: yield 0.00079, reported conversion 0, selectivity 0, faradaic efficiency 0.0283, transport and energy-efficiency estimates both 0.

The contrast between batches 1 and 2 supports a polarity-dependent productive pathway: positive polarization near +1 V favors target formation, whereas negative polarization is largely nonproductive. Batch 4 changed the initial explanation from “more positive potential is better” to a window model. Doubling the positive potential to +2 V did not improve conversion; instead, nearly every productive-efficiency indicator collapsed. The most plausible process-level interpretation is that moderate positive potential activates the desired electron-transfer sequence, while excessive positive potential diverts current into solvent/electrolyte oxidation, reactant destruction, electrode passivation, or another unobserved side pathway. The data cannot distinguish those alternatives because byproducts and electrode state were not directly identified.

A convenient phenomenological voltage factor would therefore be peaked rather than monotonic, for example

W(V) = exp[−(V−V*)²/(2σV²)] × G(V),

where G(V) strongly suppresses negative polarity and V* lies somewhere near +1 V. This is a conjectural functional form, not a fitted equation: only −2, −1, +1, and +2 V were tested, so neither V* nor σV is identifiable.

## 2. Electrochemical exposure controls product formation

Once the medium and potential were fixed at S1/E1 and +1.0 V, product formation increased strongly with either time or current cap.

At a 100 mA cap:

- Batch 9, 1,200 s: yield 0.0440, conversion 0.0263, selectivity 0.9388.
- Batch 5, 3,600 s: yield 0.0887, conversion 0.0881, selectivity 0.9544.
- Batch 10, 14,400 s: yield 0.3186, conversion 0.3541, selectivity 0.9670.

At 3,600 s:

- Batch 11, 10 mA: yield 0.00945, conversion 0.0218.
- Batch 5, 100 mA: yield 0.0887, conversion 0.0881.
- Batch 12, 500 mA: yield 0.4538, conversion 0.4356.

These differences are much larger than the declared yield uncertainty and establish that both current cap and duration are important. Selectivity remained high, approximately 0.93–0.97, throughout this S1/E1, +1 V series. Thus, in the tested range, additional electrochemical exposure mostly increased the extent of the same selective pathway rather than switching to a different product regime.

Define the cap-time exposure D = Icap t in mA·s. For batches 11, 9, 5, 10, and 12, D was respectively 36,000; 120,000; 360,000; 1,440,000; and 1,800,000 mA·s. A descriptive least-squares relation is

Y ≈ 0.00456 + 2.374×10⁻⁷ D.

It predicts yields of 0.0131, 0.0331, 0.0900, 0.3465, and 0.4319, compared with observed values of 0.00945, 0.04398, 0.08873, 0.31863, and 0.45383. This simple relation organizes the data surprisingly well, but it should not be interpreted as Faraday’s law with known delivered charge. The instrument setting was a current cap; actual current and total charge were not measured. Current and time may also have distinct kinetic effects.

A more mechanistic but still phenomenological expression would be

Y = Ymax {1 − exp[−kM W(V) Qeff]} Sprod,

Qeff = ∫ Iactual(t) dt,

where kM is a medium-dependent rate factor, W(V) is the potential-window factor, and Sprod is the fraction of converted material directed to target. Over the measured low-to-moderate conversion range, the exponential reduces approximately to a linear exposure law. No saturation was reached decisively, so Ymax cannot be fitted. The linear model must not be extrapolated beyond 500 mA, 14,400 s, or the tested loading.

## 3. Current–efficiency coupling

Current cap increased yield, but it was not energetically free. In the 3,600 s S1/E1 series:

- Batch 11 at 10 mA had energy efficiency 0.9506 and ohmic efficiency 0.9990.
- Batch 5 at 100 mA had energy efficiency 0.8856 and ohmic efficiency 0.9617.
- Batch 12 at 500 mA had energy efficiency 0.7928 and ohmic efficiency 0.8340.

Meanwhile, faradaic efficiency stayed high—0.8967, 0.9188, and 0.9351—and transport efficiency was 0.9038, 0.9082, and 0.9563. Therefore, the high-current penalty appeared primarily in ohmic and aggregate energy efficiency, not in product selectivity or the reported faradaic/transport factors. A plausible coupling is increasing resistive loss or polarization with current:

ηohmic ≈ fM/[1 + aM Icap^n],

ηenergy ≈ ηfaradaic ηtransport ηohmic × h(V),

although the precise multiplicative structure is not identifiable. The observation is consistent with iR loss or another current-dependent energetic penalty, but resistance, cell voltage under load, temperature, and actual current were not measured.

This creates a real operating trade-off. Batch 12 maximized tested yield and public score, whereas batch 10 produced less material but retained higher energy and ohmic efficiencies: batch 10 had yield 0.3186, energy efficiency 0.9281, and ohmic efficiency 0.9528, compared with 0.4538, 0.7928, and 0.8340 in batch 12. The sealed recommendation of batch 12 therefore reflects maximum tested output under the balanced score, not universal dominance for every possible objective.

## 4. Medium-dependent transport, speciation, and precipitation

Batches 5–8 screened the four solvent/electrolyte labels at +1.0 V, 100 mA, and 3,600 s. Solvent and electrolyte were changed together, so the experiment identifies pair effects but cannot separate solvent effects, electrolyte effects, or their interaction:

- Batch 5, S1/E1: yield 0.0887, conversion 0.0881, selectivity 0.9544, faradaic efficiency 0.9188, transport efficiency 0.9082, energy efficiency 0.8856.
- Batch 6, S2/E2: yield 0.0660, conversion 0.0726, selectivity 0.7940, faradaic efficiency 0.7794, transport efficiency 0.7547, energy efficiency 0.7353.
- Batch 8, S0/E0: yield 0.0361, conversion 0.0637, selectivity 0.8236, faradaic efficiency 0.7447, transport efficiency 0.7382, energy efficiency 0.7047.
- Batch 7, S3/E3: yield 0.0427, conversion 0.0594, selectivity 0.7194, faradaic efficiency 0.5278, transport efficiency 0.5312, energy efficiency 0.6465.

S1/E1 was the strongest tested pair across yield, selectivity, and most efficiency measures. S2/E2 was intermediate. S3/E3 gave the weakest faradaic and transport performance, although its ohmic-efficiency estimate was 1.0. This shows that excellent apparent conductivity alone is insufficient: productive charge transfer and transport/speciation factors matter separately.

The medium also shifted pH and precipitation signals substantially:

- S0/E0, batch 8: normalized pH 0.2266 and precipitation signal 0.9957.
- S1/E1, batch 5: normalized pH 0.2147 and precipitation signal 0.6510.
- S2/E2, batch 6: normalized pH 0.1748 and precipitation signal 0.00240.
- S3/E3, batch 7: normalized pH 0.2848 and precipitation signal 0.

Precipitation is therefore not simply proportional to yield: S0/E0 precipitated strongly but was inferior to S1/E1, while S2/E2 had almost no precipitation yet still gave moderate yield. My preferred interpretation is that medium controls several coupled properties—ionic transport, reactant/product solvation, acid–base state, and phase behavior—and that an intermediate physical regime in S1/E1 happens to support the productive pathway. Precipitation could remove product from further reaction, block electrodes, or merely report medium identity. These alternatives are unidentifiable because no cross-combinations such as S1/E0 or S0/E1 were tested.

The observed safety-risk values also varied with the diagonal medium screen: approximately 0.0722 for S0/E0, 0.0956 for S1/E1, 0.1136 for S2/E2, and 0.1262 for S3/E3. All were below the 0.65 limit. Because solvent and electrolyte were paired, risk cannot be attributed to either component independently.

## 5. Integrated process model

A compact causal account is:

1. The applied potential selects which electron-transfer manifold is accessible. Around +1 V, the target-forming sequence is active; negative potentials and +2 V are largely nonproductive.
2. The solvent/electrolyte pair determines effective conductivity, mass transport, acid–base/speciation conditions, and phase behavior. These determine an effective rate constant kM and efficiency factors.
3. Current and time determine accumulated productive exposure. At fixed S1/E1 and +1 V, yield is approximately linear in current-cap × time over the tested domain.
4. Raising current increases production rate but introduces an ohmic/energy penalty. Within the measured range it did not reduce selectivity or faradaic efficiency.
5. Product accumulation may eventually saturate through reagent depletion, mass-transfer limitation, electrode passivation, or degradation, but the location and even the dominant cause of that plateau were not established.

In pseudocode:

productive_gate = peaked_function(potential, optimum_near=+1 V)
medium_rate = unknown_pair_effect(solvent, electrolyte, pH_state, phase_state)
effective_charge = integral(actual_current over time)
conversion = saturating_function(medium_rate * productive_gate * effective_charge)
selective_yield = conversion * target_selectivity
energy_efficiency = faradaic_factor * transport_factor * ohmic_factor
ohmic_factor decreases as current increases

This model explains why batch 4 failed despite positive potential, why batches 5–8 differed at the same electrical settings, and why batches 9–12 showed systematic exposure dependence within the best tested medium.

## 6. Evidence that formed or changed the account

The explanation developed in three stages. Batches 1–2 first suggested strong polarity dependence. Batches 3–4 then rejected a simple monotonic dependence on potential magnitude and produced the voltage-window hypothesis. Batches 5–8 showed that medium identity changes selectivity and multiple efficiency components, with S1/E1 emerging as the best tested pair. Finally, batches 9–12 established systematic current/time dependence and exposed the current-versus-energy-efficiency trade-off. Batch 10 showed that long operation at 100 mA can raise yield while retaining high efficiency; batch 12 showed that high current can raise yield further but lowers ohmic and energy efficiency.

## 7. Scope, uncertainty, and alternatives

The strongest claims apply only to the fixed 0.50 mol/L loading and the tested anonymous materials. There were no replicate batches, so small differences should not be overinterpreted. Nevertheless, the main polarity, medium, time, and current contrasts are generally much larger than declared assay noise.

Yield and conversion estimates were not always internally ordered. For example, batch 12 reported yield 0.4538 and conversion 0.4356, while batch 9 reported yield 0.0440 and conversion 0.0263. These differences are on the scale expected from independently noisy estimates and should not be treated as evidence for impossible mass balance or a new pathway.

Important unidentifiable factors include actual current, delivered charge, electrode surface state, temperature during electrolysis, individual solvent and electrolyte effects, side-product identities, and whether precipitation is causal. A charge-only model is a plausible alternative to the kinetic account because cap-time exposure organizes the S1/E1 data well. Conversely, current-specific heating, polarization, or mixing could explain why current and time are not exactly interchangeable. The experiments do not distinguish these possibilities.

Likewise, the potential-window result could arise from intrinsic reaction energetics, electrode passivation, electrolyte decomposition, or instrument-level current limitation. The data establish the empirical window but not its microscopic origin. Future confirmation would require voltage points between 0 and +2 V, crossed solvent/electrolyte combinations, replicated conditions, measured current-time traces, and concentration variation; none of those measurements were made here.

Overall, the most defensible predictive rule is: at this loading, use the S1/E1 pair and a potential near +1 V; expect target yield to rise approximately with electrochemical exposure over the observed range, while anticipating declining ohmic and energy efficiency as the current cap is raised. Treat the linear exposure equation as a local interpolation, not a universal law.

## K2 封存报告

1. Claims, laws, and evidence updates

No instance-specific prior, nominal material-property dossier, or supplied mechanistic law was provided. The solvent and electrolyte labels were explicitly anonymous. My only initial claims were self-developed hypotheses recorded before experimentation.

The claim that product formation depends on electrochemical exposure was supported. At S1/E1 and +1.0 V, increasing time at 100 mA raised yield from 0.0440 in batch 9 (1,200 s), to 0.0887 in batch 5 (3,600 s), to 0.3186 in batch 10 (14,400 s). At 3,600 s, increasing the current cap from 10 mA in batch 11 to 100 mA in batch 5 and 500 mA in batch 12 raised yield from 0.00945 to 0.0887 and 0.4538. This supported a local current-cap × time exposure law, but did not establish that actual delivered charge equaled the cap-time product.

The initial broad idea that potential magnitude might simply increase conversion was contradicted. Batch 2 at +1.0 V was productive relative to batch 1 at −1.0 V, but batch 4 at +2.0 V collapsed to yield 0.00079, zero estimated selectivity, and near-zero productive efficiencies. Batch 3 at −2.0 V was also unproductive. These observations changed my judgment to a polarity-sensitive, nonmonotonic potential-window account centered near +1 V.

The hypothesis that medium affects transport and efficiency was supported at the level of paired formulations. Under common electrical conditions, S1/E1 in batch 5 outperformed S2/E2, S0/E0, and S3/E3 in batches 6, 8, and 7. However, the separate solvent and electrolyte contributions were untested because only diagonal pairs were used. Any claim assigning the effect specifically to S1 or E1 remains unsupported.

A current-dependent efficiency penalty was supported. Ohmic efficiency declined from 0.9990 in batch 11 at 10 mA to 0.9617 in batch 5 at 100 mA and 0.8340 in batch 12 at 500 mA. Energy efficiency showed the same direction, while selectivity and faradaic efficiency remained high. This changed the account from a single exposure law to an exposure law coupled to current-dependent energetic loss.

Saturation, concentration dependence, the exact voltage optimum, actual-current behavior, and the microscopic identities of side reactions were untested. The proposed saturating kinetic equation and Gaussian-like voltage window were explanatory forms, not fitted or confirmed laws.

2. Most informative additional experiment

I would run one new batch at the established 0.50 mol/L loading with S1/E1, +1.0 V, a 400 mA cap, and 3,600 s electrolysis. Its cap-time exposure would be 1,440,000 mA·s, exactly matching batch 10 at 100 mA for 14,400 s.

This would directly compare equal nominal exposure delivered through different current/time combinations. If yield and conversion matched batch 10 within combined uncertainty, while ohmic and energy efficiencies were lower, it would support my leading hybrid explanation: accumulated exposure controls product formation, but current separately controls energetic loss. If yield, conversion, and efficiencies all matched batch 10, the simpler pure charge/exposure alternative would gain support. If yield differed substantially, current and time would not be interchangeable; a higher yield would suggest current-dependent kinetics or transport enhancement, whereas a lower yield would suggest high-current side reactions, polarization, heating, or passivation. A large selectivity loss would specifically weaken the claim that current changes only efficiency rather than pathway choice.

3. Unused evidence, weak predictions, and goal effects

The detailed raw final-assay spectra and most raw UV–visible traces were not used in the quantitative model; I relied primarily on processed estimates. Intermediate UV–visible observations, measurement cost, and full mass-balance metadata were also not modeled. Normalized pH, precipitation, and safety risk were used only qualitatively. No current-time trace, electrode-state observation, temperature trajectory, or identified byproduct evidence was available.

The least reliable blind predictions are the crossed-medium cases Q05–Q10 because the campaign confounded solvent and electrolyte identity. Predictions for long negative-potential operation, especially Q03, Q05, Q07, Q09, and high-current Q11, are also weak because negative potentials were observed only at 300 s and 100 mA. Q12 is uncertain because it doubles the largest tested cap-time exposure and changes potential and medium simultaneously relative to the closest high-current batch. Even Q01–Q04 require interpolation from ±1.0 V to ±0.8 V without a measured voltage curve.

The sealed recommendation of batch 12 is reliable only as the highest-yield, highest-score tested condition. It is less reliable as a universal recommendation because it had lower energy and ohmic efficiencies than batch 10, lacked replication, and was not compared across alternative media at 500 mA.

The assigned mechanism-discovery goal affected evidence collection: I prioritized polarity, potential magnitude, medium screening, time, and current breadth rather than replication or narrow score optimization. This produced evidence for the principal qualitative relationships but left variance, solvent/electrolyte decomposition, and precise response surfaces poorly identified. The secondary optimization score did not create a clear conflict during exploration, although it influenced the final choice of batch 12. These are retrospective assessments based on the completed evidence; they are not presented as contemporaneous thoughts beyond the hypotheses actually recorded before and during the campaign.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.42,
        "upper80": 0.68
      },
      "energy_efficiency": {
        "estimate": 0.24,
        "lower80": 0.14,
        "upper80": 0.34
      },
      "faradaic_efficiency": {
        "estimate": 0.4,
        "lower80": 0.3,
        "upper80": 0.5
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.043,
        "lower80": 0.0,
        "upper80": 0.28
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.37,
        "lower80": 0.27,
        "upper80": 0.47
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.86,
        "lower80": 0.76,
        "upper80": 0.94
      },
      "energy_efficiency": {
        "estimate": 0.74,
        "lower80": 0.62,
        "upper80": 0.84
      },
      "faradaic_efficiency": {
        "estimate": 0.78,
        "lower80": 0.68,
        "upper80": 0.87
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.499,
        "lower80": 0.13,
        "upper80": 0.58
      },
      "selective_product_yield": {
        "estimate": 0.02,
        "lower80": 0.005,
        "upper80": 0.045
      },
      "transport_efficiency": {
        "estimate": 0.79,
        "lower80": 0.68,
        "upper80": 0.88
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.56,
        "lower80": 0.4,
        "upper80": 0.7
      },
      "energy_efficiency": {
        "estimate": 0.23,
        "lower80": 0.12,
        "upper80": 0.35
      },
      "faradaic_efficiency": {
        "estimate": 0.4,
        "lower80": 0.28,
        "upper80": 0.52
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.3,
        "lower80": 0.18,
        "upper80": 0.4
      },
      "selective_product_yield": {
        "estimate": 0.035,
        "lower80": 0.005,
        "upper80": 0.09
      },
      "transport_efficiency": {
        "estimate": 0.37,
        "lower80": 0.25,
        "upper80": 0.49
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.85,
        "lower80": 0.76,
        "upper80": 0.93
      },
      "energy_efficiency": {
        "estimate": 0.72,
        "lower80": 0.62,
        "upper80": 0.82
      },
      "faradaic_efficiency": {
        "estimate": 0.76,
        "lower80": 0.67,
        "upper80": 0.85
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.517,
        "lower80": 0.45,
        "upper80": 0.59
      },
      "selective_product_yield": {
        "estimate": 0.085,
        "lower80": 0.04,
        "upper80": 0.16
      },
      "transport_efficiency": {
        "estimate": 0.76,
        "lower80": 0.66,
        "upper80": 0.85
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.63,
        "lower80": 0.42,
        "upper80": 0.8
      },
      "energy_efficiency": {
        "estimate": 0.3,
        "lower80": 0.16,
        "upper80": 0.46
      },
      "faradaic_efficiency": {
        "estimate": 0.5,
        "lower80": 0.32,
        "upper80": 0.68
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.347,
        "lower80": 0.23,
        "upper80": 0.46
      },
      "selective_product_yield": {
        "estimate": 0.045,
        "lower80": 0.01,
        "upper80": 0.11
      },
      "transport_efficiency": {
        "estimate": 0.48,
        "lower80": 0.3,
        "upper80": 0.66
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.9,
        "lower80": 0.75,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.82,
        "lower80": 0.64,
        "upper80": 0.94
      },
      "faradaic_efficiency": {
        "estimate": 0.86,
        "lower80": 0.7,
        "upper80": 0.97
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.581,
        "lower80": 0.5,
        "upper80": 0.67
      },
      "selective_product_yield": {
        "estimate": 0.14,
        "lower80": 0.06,
        "upper80": 0.27
      },
      "transport_efficiency": {
        "estimate": 0.85,
        "lower80": 0.68,
        "upper80": 0.96
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.48,
        "lower80": 0.28,
        "upper80": 0.68
      },
      "energy_efficiency": {
        "estimate": 0.18,
        "lower80": 0.06,
        "upper80": 0.32
      },
      "faradaic_efficiency": {
        "estimate": 0.3,
        "lower80": 0.14,
        "upper80": 0.48
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.256,
        "lower80": 0.0,
        "upper80": 0.38
      },
      "selective_product_yield": {
        "estimate": 0.025,
        "lower80": 0.0,
        "upper80": 0.075
      },
      "transport_efficiency": {
        "estimate": 0.28,
        "lower80": 0.12,
        "upper80": 0.46
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.77,
        "lower80": 0.6,
        "upper80": 0.9
      },
      "energy_efficiency": {
        "estimate": 0.66,
        "lower80": 0.48,
        "upper80": 0.8
      },
      "faradaic_efficiency": {
        "estimate": 0.64,
        "lower80": 0.46,
        "upper80": 0.8
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.461,
        "lower80": 0.37,
        "upper80": 0.54
      },
      "selective_product_yield": {
        "estimate": 0.06,
        "lower80": 0.02,
        "upper80": 0.14
      },
      "transport_efficiency": {
        "estimate": 0.63,
        "lower80": 0.45,
        "upper80": 0.79
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.54,
        "lower80": 0.36,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.24,
        "lower80": 0.12,
        "upper80": 0.38
      },
      "faradaic_efficiency": {
        "estimate": 0.39,
        "lower80": 0.25,
        "upper80": 0.55
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.295,
        "lower80": 0.19,
        "upper80": 0.4
      },
      "selective_product_yield": {
        "estimate": 0.035,
        "lower80": 0.008,
        "upper80": 0.095
      },
      "transport_efficiency": {
        "estimate": 0.36,
        "lower80": 0.23,
        "upper80": 0.51
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.82,
        "lower80": 0.66,
        "upper80": 0.94
      },
      "energy_efficiency": {
        "estimate": 0.72,
        "lower80": 0.54,
        "upper80": 0.86
      },
      "faradaic_efficiency": {
        "estimate": 0.77,
        "lower80": 0.6,
        "upper80": 0.91
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.518,
        "lower80": 0.43,
        "upper80": 0.6
      },
      "selective_product_yield": {
        "estimate": 0.1,
        "lower80": 0.035,
        "upper80": 0.2
      },
      "transport_efficiency": {
        "estimate": 0.76,
        "lower80": 0.59,
        "upper80": 0.9
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.35,
        "upper80": 0.75
      },
      "energy_efficiency": {
        "estimate": 0.18,
        "lower80": 0.08,
        "upper80": 0.32
      },
      "faradaic_efficiency": {
        "estimate": 0.42,
        "lower80": 0.25,
        "upper80": 0.6
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.319,
        "lower80": 0.22,
        "upper80": 0.43
      },
      "selective_product_yield": {
        "estimate": 0.1,
        "lower80": 0.02,
        "upper80": 0.25
      },
      "transport_efficiency": {
        "estimate": 0.4,
        "lower80": 0.23,
        "upper80": 0.58
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.86,
        "lower80": 0.72,
        "upper80": 0.96
      },
      "energy_efficiency": {
        "estimate": 0.62,
        "lower80": 0.45,
        "upper80": 0.78
      },
      "faradaic_efficiency": {
        "estimate": 0.8,
        "lower80": 0.68,
        "upper80": 0.93
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.602,
        "lower80": 0.5,
        "upper80": 0.7
      },
      "selective_product_yield": {
        "estimate": 0.32,
        "lower80": 0.16,
        "upper80": 0.58
      },
      "transport_efficiency": {
        "estimate": 0.82,
        "lower80": 0.7,
        "upper80": 0.95
      }
    }
  ],
  "rationale": "Predictions use the observed polarity window near +1 V, the approximately increasing yield with current-cap × time, and the current-dependent energy/ohmic penalty. The 0.48 mol/L query loading is close to the studied 0.50 mol/L loading. Intervals are widest for negative-potential, high-exposure, and crossed solvent/electrolyte cases because those require extrapolation or separation of medium effects that were confounded in the campaign. Score estimates apply the published weighted formula and its 0.02 yield gate."
}
```
