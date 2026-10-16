# repeat-02/EC-W04-B12-optimization-E-Aligned

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-02\EC-W04-B12-optimization-E-Aligned\participant\optimization-E-Aligned

## 同期笔记

### v1 · 公开事件 0

# Electrochemical campaign hypotheses

## H1 [tentative]
At fixed 0.02 mol reagent in 0.04 L solvent, the better balanced score should occur at the potential sign that drives target conversion, with an intermediate potential magnitude and electrolysis time: insufficient charge limits conversion, while excessive polarization/time should lower selectivity and energy efficiency. E3/S0 may favor ohmic efficiency from nominal conductivity, whereas E1/S1 may favor transport; the best material pairing is unresolved because hidden interface residuals may dominate.

**Pre-experiment test:** screen both potential signs plus material and dose variation. A sign giving near-zero selective yield will be treated as directionally inactive. For an active sign, later batches will refine potential/time/current around the best observed score; a current cap that is not reached cannot be interpreted as a current effect.

## H2 [tentative]
Precipitation may gate productive yield for E0 more than E2/E3 based on nominal salt/Ksp properties. pH and precipitation readouts will be used as contextual correlates, not assumed causes.

### v2 · 公开事件 42

# Electrochemical campaign hypotheses

## H1 [supported in tested scope]
The negative potential sign is productive; +1.2 V was essentially inactive at 300 s (final assay event runner-operation-0007), while -1.2 V at the same cap/time gave measurable electrochemical efficiencies and score 0.160 (runner-operation-0014). The sign inference is strong, but the apparent conversion at very low charge was near assay resolution, so detailed short-time kinetics remain unresolved.

At -1.2 V, 500 mA cap and 6000 s in S0, electrolyte identity materially changes performance. E2 gave the best tested score 0.359 and selective yield 0.184 (runner-operation-0035), narrowly above E1 score 0.340/yield 0.165 (runner-operation-0028), while E0 and E3 were much worse (runner-operation-0021, runner-operation-0042). The E2–E1 numerical difference is modest relative to single-run noise and remains unresolved without replication; both outperform E0/E3 by larger margins.

**Decision:** hold E2 and screen solvents, then refine potential/time around the strongest combination. Reverse this choice if another solvent causes E1-like transport to dominate or if E2 selectivity collapses.

## H2 [narrowed]
Precipitation is not required for target formation: E2 had essentially zero precipitation signal while outperforming strongly precipitating E0/E1 in the tested S0 condition (runner-operation-0035 versus runner-operation-0021 and runner-operation-0028). This does not establish precipitation as causal inhibition because electrolyte changes are confounded with transport, acidity, and interface kinetics.

## H3 [tentative]
For an active negative bias, solvent diffusion and proton activity may trade transport against selectivity. Prediction before the solvent screen: S1 may raise transport, while S2/S3 may improve selectivity/precipitation behavior but lose ohmic efficiency.

### v3 · 公开事件 77

# Electrochemical campaign hypotheses

## H1 [supported in tested scope]
Negative bias is the productive sign (runner-operation-0007 versus runner-operation-0014). Within the active sign, performance is non-monotone with potential magnitude: for E2/S0 at 6000 s and a 500 mA cap, -0.8 V scored 0.441 (runner-operation-0070) and -0.5 V scored 0.455 (runner-operation-0077), both above -1.2 V at 0.359 (runner-operation-0035). The stronger -1.2 V condition lost energy/faradaic efficiency and selective yield. The optimum below -0.5 V remains untested.

## H2 [supported as ranking, mechanism unresolved]
E2/S0 is the best tested material pairing. At E2/-1.2 V/6000 s, S0 through S3 scores were respectively 0.359, 0.354, 0.324, and 0.337 (runner-operation-0035, runner-operation-0049, runner-operation-0056, runner-operation-0063). S0 versus S1 is too close for a confident solvent effect given single noisy assays, but S0 is the operational incumbent. The solvent screen did not support the simple prediction that nominal diffusivity alone determines transport or score.

## H3 [tentative duration tradeoff]
At -0.5 V, extending from 6000 to 9000 s may raise conversion and selective yield enough to improve the balanced score, but could lower average faradaic/energy efficiency or induce degradation. **Pre-final test prediction:** 9000 s should exceed 6000 s if productive conversion remains below saturation; a lower score would locate the practical optimum at or below 6000 s.

Precipitation is not required for target formation and remains a contextual correlate rather than a causal claim.

### v4 · 公开事件 84

# Electrochemical campaign hypotheses — final source-stage record

## H1 [supported in tested scope]
Negative bias is productive and the balanced response is non-monotone with potential magnitude. The positive-sign control was inactive (runner-operation-0007); at E2/S0 and 6000 s, reducing cathodic magnitude from -1.2 V to -0.8 and -0.5 V improved scores from 0.359 to 0.441 and 0.455 (runner-operation-0035, runner-operation-0070, runner-operation-0077). This supports avoiding excessive polarization, but does not locate the optimum below -0.5 V.

## H2 [supported operationally; fine ranking unresolved]
E2/S0 is the best tested material setting. E2 outperformed E0/E3 clearly in the common S0/-1.2 V/6000 s screen; E2 versus E1 was closer and is not treated as a precise mechanistic ranking. Across solvents at E2, S0 and S1 were nearly tied at -1.2 V, while S2/S3 were lower (runner-operation-0035, runner-operation-0049, runner-operation-0056, runner-operation-0063). Hidden interface residuals and coupled properties remain alternatives to nominal transport explanations.

## H3 [supported between tested durations]
At E2/S0, -0.5 V and 500 mA cap, extending electrolysis from 6000 to 9000 s raised score from 0.455 to 0.507 and selective yield from 0.283 to 0.434 (runner-operation-0077, runner-operation-0084), while final energy and faradaic efficiencies remained substantial. This is evidence for a beneficial duration effect over this interval, not proof that still longer operation improves performance.

## Recommendation
Select batch 12: 0.02 mol reagent, 0.04 L S0, E2, -0.5 V, 500 mA magnitude cap, 9000 s. It is the highest-scoring completed batch (0.507) and had safety risk 0.072, below the stated limit. The current setting is a cap, so no claim is made that 500 mA was continuously delivered.

## Unresolved tests
Bracket potential below -0.5 V and duration above 9000 s; replicate S0 versus S1 and E2 versus E1; independently vary current cap to distinguish transport limitation from voltage-dependent selectivity.

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
      "potential_V": 1.2
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
    "cost": 0.28274399042129517,
    "electrochemical_conversion": 0.008014115504920483,
    "electrochemical_selectivity": 0.01034972071647644,
    "energy_efficiency": 0.005256945732980967,
    "faradaic_efficiency": 0.02452157624065876,
    "ohmic_efficiency": 0.9628238677978516,
    "pH_normalized": 0.23443032801151276,
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
      "potential_V": -1.2
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
    "cost": 0.28274399042129517,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.6320253610610962,
    "energy_efficiency": 0.19927366077899933,
    "faradaic_efficiency": 0.3906446099281311,
    "ohmic_efficiency": 0.9716616868972778,
    "pH_normalized": 0.2317349761724472,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.15991906821727753,
    "selective_product_yield": 0.010869380086660385,
    "transport_efficiency": 0.4169014096260071
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
      "current_mA": 500,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.2
    },
    {
      "duration_s": 6000,
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
    "cost": 0.296999990940094,
    "electrochemical_conversion": 0.09115887433290482,
    "electrochemical_selectivity": 0.6278475522994995,
    "energy_efficiency": 0.0635124146938324,
    "faradaic_efficiency": 0.0967552661895752,
    "ohmic_efficiency": 0.8462901711463928,
    "pH_normalized": 0.2324499785900116,
    "precipitation_signal": 0.9863388538360596,
    "safety_risk": 0.072194404900074,
    "score": 0.21881568431854248,
    "selective_product_yield": 0.051169123500585556,
    "transport_efficiency": 0.11331217736005783
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
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -1.2
    },
    {
      "duration_s": 6000,
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
    "cost": 0.296999990940094,
    "electrochemical_conversion": 0.28137385845184326,
    "electrochemical_selectivity": 0.5471780896186829,
    "energy_efficiency": 0.1919003576040268,
    "faradaic_efficiency": 0.3950963616371155,
    "ohmic_efficiency": 0.8426691293716431,
    "pH_normalized": 0.2017340511083603,
    "precipitation_signal": 0.8397605419158936,
    "safety_risk": 0.072194404900074,
    "score": 0.3396850824356079,
    "selective_product_yield": 0.1649998128414154,
    "transport_efficiency": 0.36360880732536316
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
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -1.2
    },
    {
      "duration_s": 6000,
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
    "cost": 0.296999990940094,
    "electrochemical_conversion": 0.2928675711154938,
    "electrochemical_selectivity": 0.6135647296905518,
    "energy_efficiency": 0.22335955500602722,
    "faradaic_efficiency": 0.38335278630256653,
    "ohmic_efficiency": 0.8225494027137756,
    "pH_normalized": 0.1633487343788147,
    "precipitation_signal": 0.0,
    "safety_risk": 0.072194404900074,
    "score": 0.35916993021965027,
    "selective_product_yield": 0.18417972326278687,
    "transport_efficiency": 0.37284332513809204
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
      "current_mA": 500,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": -1.2
    },
    {
      "duration_s": 6000,
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
    "cost": 0.296999990940094,
    "electrochemical_conversion": 0.09214520454406738,
    "electrochemical_selectivity": 0.5030766129493713,
    "energy_efficiency": 0.07138857990503311,
    "faradaic_efficiency": 0.13983066380023956,
    "ohmic_efficiency": 0.8696581125259399,
    "pH_normalized": 0.27174678444862366,
    "precipitation_signal": 0.0023995577357709408,
    "safety_risk": 0.072194404900074,
    "score": 0.20982013642787933,
    "selective_product_yield": 0.05522925779223442,
    "transport_efficiency": 0.11514732241630554
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
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -1.2
    },
    {
      "duration_s": 6000,
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
    "cost": 0.31299999356269836,
    "electrochemical_conversion": 0.29099443554878235,
    "electrochemical_selectivity": 0.6007938981056213,
    "energy_efficiency": 0.26555290818214417,
    "faradaic_efficiency": 0.3631942570209503,
    "ohmic_efficiency": 0.7733732461929321,
    "pH_normalized": 0.16231870651245117,
    "precipitation_signal": 0.0,
    "safety_risk": 0.09559440612792969,
    "score": 0.3541164994239807,
    "selective_product_yield": 0.17650803923606873,
    "transport_efficiency": 0.3665946125984192
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
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -1.2
    },
    {
      "duration_s": 6000,
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
    "electrochemical_conversion": 0.25620967149734497,
    "electrochemical_selectivity": 0.5713034868240356,
    "energy_efficiency": 0.27135753631591797,
    "faradaic_efficiency": 0.3441038131713867,
    "ohmic_efficiency": 0.7190573811531067,
    "pH_normalized": 0.17312930524349213,
    "precipitation_signal": 0.00031451715040020645,
    "safety_risk": 0.1135944053530693,
    "score": 0.32355138659477234,
    "selective_product_yield": 0.1298445612192154,
    "transport_efficiency": 0.3376084864139557
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
      "potential_V": -1.2
    },
    {
      "duration_s": 6000,
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
    "cost": 0.32260000705718994,
    "electrochemical_conversion": 0.2502041757106781,
    "electrochemical_selectivity": 0.5574840307235718,
    "energy_efficiency": 0.2878100872039795,
    "faradaic_efficiency": 0.31567302346229553,
    "ohmic_efficiency": 0.8264484405517578,
    "pH_normalized": 0.16709403693675995,
    "precipitation_signal": 0.008188718929886818,
    "safety_risk": 0.12619440257549286,
    "score": 0.33748552203178406,
    "selective_product_yield": 0.16007976233959198,
    "transport_efficiency": 0.3365042805671692
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
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -0.8
    },
    {
      "duration_s": 6000,
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
    "electrochemical_conversion": 0.36186689138412476,
    "electrochemical_selectivity": 0.6833385825157166,
    "energy_efficiency": 0.5040575861930847,
    "faradaic_efficiency": 0.4547862410545349,
    "ohmic_efficiency": 0.7258982062339783,
    "pH_normalized": 0.15708954632282257,
    "precipitation_signal": 0.0,
    "safety_risk": 0.072194404900074,
    "score": 0.44087842106819153,
    "selective_product_yield": 0.22774168848991394,
    "transport_efficiency": 0.4561358392238617
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
      "volume_L": 0.04
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -0.5
    },
    {
      "duration_s": 6000,
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
    "cost": 0.28859999775886536,
    "electrochemical_conversion": 0.41003063321113586,
    "electrochemical_selectivity": 0.7020896673202515,
    "energy_efficiency": 0.4242883026599884,
    "faradaic_efficiency": 0.512391209602356,
    "ohmic_efficiency": 0.5814133882522583,
    "pH_normalized": 0.15807457268238068,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.072194404900074,
    "score": 0.45494934916496277,
    "selective_product_yield": 0.28344154357910156,
    "transport_efficiency": 0.5195711851119995
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
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -0.5
    },
    {
      "duration_s": 9000,
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
    "cost": 0.29159998893737793,
    "electrochemical_conversion": 0.578459620475769,
    "electrochemical_selectivity": 0.6933677792549133,
    "energy_efficiency": 0.40277519822120667,
    "faradaic_efficiency": 0.4760744273662567,
    "ohmic_efficiency": 0.5947619080543518,
    "pH_normalized": 0.15859489142894745,
    "precipitation_signal": 0.0,
    "safety_risk": 0.072194404900074,
    "score": 0.5068543553352356,
    "selective_product_yield": 0.433823823928833,
    "transport_efficiency": 0.4972993731498718
  }
}
```

## K1 封存报告

Mechanistic report

Scope and evidence base

This account applies only to the anonymous benchmark system studied in the twelve completed batches. Every batch contained 0.020 mol limiting reagent in 0.040 L solvent. The solvent, electrolyte profile, configured potential, current cap, and electrolysis duration were varied. The identities behind S0–S3 and E0–E3 are deliberately anonymous, so no real chemical identity is inferred. All numerical outcomes below are final-assay estimates from this synthetic world; differences from single batches should not be treated as replicated physical effects.

Proposed process model

I interpret the system as a cathodic electrochemical conversion governed by five coupled stages:

1. The applied potential establishes a cathodic driving force relative to a medium-dependent effective reduction potential.
2. Charge transfer at the interface converts reactant into a reactive/product-forming state, while competing electron-consuming reactions reduce faradaic efficiency.
3. Reactant and ionic transport through a diffusion layer limit sustainable current. The configured current is therefore best understood as a cap, not proof that this current flowed continuously.
4. The electrolyte and solvent jointly control conductivity, diffusion, proton activity, interfacial capacitance, precipitation, and selectivity.
5. Continued electrolysis increases conversion and product yield until depletion, transport limitation, or side reactions make additional charge progressively less useful.

A useful qualitative representation is

I_actual(t) = min[I_cap, I_kinetic(eta, medium), I_transport(concentration, diffusivity, diffusion-layer thickness)],

where eta is an effective overpotential that depends on the configured potential and the solvent/electrolyte potential shifts. Product formation may then be represented approximately by

dn_product/dt = FE(t) * S(t) * I_actual(t)/(zF),

dn_side/dt = [1 - FE(t)] * I_actual(t)/(z_side F),

with conversion X increasing with productive charge, while selectivity S and faradaic efficiency FE may decrease at excessive overpotential or late in electrolysis. The measured selective-product yield should broadly track conversion times selectivity, but it need not equal their simple product because the reported channels are separately noisy, bounded estimates and may use different internal normalizations.

Potential direction and magnitude

The strongest directional evidence is the comparison between batches 1 and 2. Batch 1 used S0/E0, +1.2 V, a 100 mA cap, and 300 s. It produced a score of 0.000, selective-product yield 0.000, conversion 0.008, and essentially zero transport and energy efficiency. Batch 2 used the same materials, cap, and duration but -1.2 V. It produced score 0.160, selective-product yield 0.0109, selectivity 0.632, faradaic efficiency 0.391, and transport efficiency 0.417. Its reported conversion was clipped at 0, so the very small short-time conversion is not quantitatively resolved, but the efficiency channels clearly identify negative bias as the productive direction.

Potential magnitude was not monotonic. With E2/S0, a 500 mA cap, and 6000 s, batch 5 at -1.2 V scored 0.359, whereas batch 10 at -0.8 V scored 0.441 and batch 11 at -0.5 V scored 0.455. From batch 5 to batch 10, conversion rose from 0.293 to 0.362, selectivity from 0.614 to 0.683, selective yield from 0.184 to 0.228, and energy efficiency from 0.223 to 0.504. Batch 11 at -0.5 V further raised conversion to 0.410, selectivity to 0.702, yield to 0.283, faradaic efficiency to 0.512, and transport efficiency to 0.520, although its ohmic efficiency was lower at 0.581.

Thus, in the tested interval, the more negative -1.2 V condition did not deliver a superior net rate or score. I infer that excessive cathodic polarization activates parasitic current, worsens energy use, and possibly intensifies local concentration or proton gradients. A less extreme potential can consequently generate more useful product even if its nominal electrical driving force is smaller. This inference is supported over -1.2 to -0.5 V, but the location of the optimum is not identified: no potential between -0.5 and 0 V was tested.

Charge and duration

At S0/E0 and -1.2 V, raising the current cap from 100 to 500 mA and extending time from 300 to 6000 s changed the score from 0.160 in batch 2 to 0.219 in batch 3. Batch 3 reached conversion 0.091 and yield 0.051, but its final faradaic, transport, and energy efficiencies were only 0.097, 0.113, and 0.064. This suggests that simply requesting much more charge cannot overcome an unfavorable transport/interface medium.

The cleaner duration comparison is between batches 11 and 12, both E2/S0, -0.5 V, and a 500 mA cap. Extending electrolysis from 6000 to 9000 s raised conversion from 0.410 to 0.578, selective yield from 0.283 to 0.434, and score from 0.455 to 0.507. Selectivity changed only slightly, from 0.702 to 0.693. Final faradaic efficiency fell from 0.512 to 0.476, energy efficiency from 0.424 to 0.403, and transport efficiency from 0.520 to 0.497, while ohmic efficiency was similar within assay uncertainty, 0.581 versus 0.595. I therefore infer diminishing marginal efficiency with time but continued net product formation through 9000 s. The additional yield carried enough score weight to compensate for modest efficiency losses.

This does not establish that still longer operation is beneficial. A plausible continuation is a peak followed by a plateau or decline as reactant is depleted and side reactions dominate. Batch 12 only establishes that the optimum duration, under its other settings, was not below 6000 s.

Electrolyte effects

Batches 3–6 screened E0–E3 at common S0, -1.2 V, 500 mA cap, and 6000 s:

- Batch 3, E0: score 0.219, conversion 0.091, selectivity 0.628, yield 0.051, faradaic efficiency 0.097, transport efficiency 0.113, precipitation signal 0.986.
- Batch 4, E1: score 0.340, conversion 0.281, selectivity 0.547, yield 0.165, faradaic efficiency 0.395, transport efficiency 0.364, precipitation signal 0.840.
- Batch 5, E2: score 0.359, conversion 0.293, selectivity 0.614, yield 0.184, faradaic efficiency 0.383, transport efficiency 0.373, precipitation signal 0.
- Batch 6, E3: score 0.210, conversion 0.092, selectivity 0.503, yield 0.055, faradaic efficiency 0.140, transport efficiency 0.115, precipitation signal 0.0024.

E1 and E2 were therefore the productive electrolyte class in this screen, whereas E0 and E3 were transport-poor. This agrees qualitatively with the nominal dossier: E1 has high diffusivity and a thin diffusion layer, while E2 also has a relatively thin layer. E0 and especially E3 have thicker nominal diffusion layers. Bulk conductivity alone cannot explain the ranking because E3 has the highest declared conductivity but performed poorly. I infer that mass transport and interface kinetics were more important than nominal bulk conductivity under these conditions.

E2 was the operational winner, but the score difference between E2 and E1 was only about 0.019 in single assays. It is not sufficient to identify E2 as intrinsically superior with high confidence. E2 also differs from E1 in acidity, potential shift, conductivity, diffusion properties, salt loading, and hidden residuals, so the causal electrolyte property is unidentifiable from this screen.

Precipitation and acidity

The electrolyte screen shows that precipitation is not required for productive conversion. E2 in batch 5 had a precipitation signal of 0 while outperforming strongly precipitating E0 and E1. E0 combined near-maximal precipitation with low transport and yield, which is consistent with precipitation blocking mass transfer or electrode area. However, E1 also had a large precipitation signal while performing almost as well as E2. Consequently, precipitation may be harmful in some media but is neither a sufficient explanation for failure nor a universal performance gate.

The normalized-pH estimates also changed with electrolyte: approximately 0.232 for E0, 0.202 for E1, 0.163 for E2, and 0.272 for E3 in batches 3–6. The productive E1/E2 conditions were more acidic by this normalized measure than E3, but acidity is confounded with transport and interfacial properties. Within E2/S0, normalized pH stayed near 0.157–0.163 as potential changed, while performance varied substantially. Thus bulk pH alone is not the main explanation for the potential response; unmeasured local interfacial pH could still matter.

Solvent effects

Batches 5 and 7–9 screened S0–S3 at common E2, -1.2 V, 500 mA cap, and 6000 s:

- Batch 5, S0: score 0.359, conversion 0.293, selectivity 0.614, yield 0.184, ohmic efficiency 0.823, safety risk 0.072.
- Batch 7, S1: score 0.354, conversion 0.291, selectivity 0.601, yield 0.177, ohmic efficiency 0.773, safety risk 0.096.
- Batch 8, S2: score 0.324, conversion 0.256, selectivity 0.571, yield 0.130, ohmic efficiency 0.719, safety risk 0.114.
- Batch 9, S3: score 0.337, conversion 0.250, selectivity 0.557, yield 0.160, ohmic efficiency 0.826, safety risk 0.126.

S0 and S1 were nearly tied, with S0 selected as the incumbent because it had the slightly higher observed score, yield, ohmic efficiency, and lower safety risk. The data did not support a simple rule based only on nominal solvent diffusivity: S1 has the highest declared relative diffusivity but did not beat S0. Likewise, reduced nominal proton activity in S2/S3 did not improve selectivity in this operating region. The solvent evidently changes several coupled quantities at once—conductivity, solvation, potential shift, proton activity, double-layer behavior, and hidden interface kinetics—so no single-property causal coefficient can be extracted.

Efficiency tradeoffs and the balanced score

The public score rewards selective yield most heavily but also rewards conversion, selectivity, energy, faradaic, transport, and ohmic efficiencies. This explains why maximizing any one channel would be inadequate. For example, batch 1 retained very high ohmic efficiency, about 0.963, but had no useful conversion and scored zero. Batch 5 had reasonable ohmic efficiency, 0.823, but its stronger polarization produced weaker energy and yield outcomes. Batch 12 did not maximize ohmic efficiency, but it combined the campaign's largest selective yield with moderate values across all remaining components and therefore achieved the highest score.

My qualitative objective model is

Score approximately equals a yield-gated weighted combination of conversion, selectivity, selective yield, faradaic efficiency, transport efficiency, ohmic efficiency, and energy efficiency.

Productive operation therefore requires three things simultaneously: a nonzero cathodic reaction rate, sufficient transport to sustain useful current, and restrained polarization so that a substantial fraction of charge and energy reaches the target pathway.

How the experiments changed the explanation

The initial expectation was that the productive sign would have to be discovered and that an intermediate potential/time would balance conversion against efficiency. Batch 1 rejected positive bias as useful in the tested direction, while batch 2 established negative bias as active.

The nominal properties initially made both high-conductivity E3/S0 and high-transport E1/S1 plausible. Batches 3–6 changed this view: E3's high bulk conductivity did not compensate for poor transport-scale behavior, and E2 became the better operational electrolyte. The result shifted the explanation away from bulk resistance alone and toward diffusion-layer and interface control.

The solvent screen in batches 5 and 7–9 rejected the simplest nominal-diffusivity prediction because S1 did not outperform S0. It also showed that lower proton activity in S2/S3 did not automatically improve selectivity.

Batches 10 and 11 produced the most important mechanistic revision. Less negative potentials improved conversion, selectivity, faradaic efficiency, transport efficiency, and score relative to -1.2 V. This made parasitic polarization and coupled transport loss central to the explanation rather than treating stronger bias as automatically faster.

Finally, batch 12 showed that additional time at the milder -0.5 V bias remained productive: conversion and yield rose substantially while efficiency losses were moderate. This distinguished excessive potential from useful additional duration; stronger driving force was harmful, but longer exposure at moderated driving force was beneficial over the tested interval.

Recommended operating point and observed outcome

The sealed recommendation is batch 12: 0.020 mol reagent, 0.040 L S0, E2, configured potential -0.5 V, current cap 500 mA, and electrolysis time 9000 s. Its final assay reported score 0.5069, selective-product yield 0.4338, conversion 0.5785, selectivity 0.6934, faradaic efficiency 0.4761, transport efficiency 0.4973, ohmic efficiency 0.5948, energy efficiency 0.4028, normalized pH 0.1586, precipitation signal 0, and safety risk 0.0722. This was the highest score among the twelve completed batches and remained well below the stated safety limit of 0.65.

Unidentifiable factors and plausible alternatives

Several important quantities cannot be identified from this campaign:

- Actual current-time traces were not measured, so charge passed and whether the 500 mA cap was reached are unknown.
- Electrode area, gap, and contact resistance were fixed but not independently varied. Ohmic and transport effects cannot be separated completely.
- Hidden world-specific solvent, electrolyte, solvation, and interface residuals were fixed across the campaign but not observable.
- Product electron stoichiometry z is unknown, preventing an absolute coulombic material balance from configured current and duration.
- No temperature, local interfacial pH, reactant concentration profile, or time-resolved product concentration was measured.
- Each main condition had one final assay. Small differences, especially E2 versus E1 and S0 versus S1, could reflect assay/process noise rather than true ranking.
- Potential and current cap were not varied independently in a factorial design. The apparent potential effect could include changes in actual current and transport state.
- Duration was compared directly only at -0.5 V between 6000 and 9000 s; duration behavior elsewhere is extrapolation.

A plausible alternative to the side-reaction explanation is that -1.2 V primarily creates a severe concentration gradient or interfacial state that suppresses productive current, rather than directly accelerating a chemical byproduct channel. Another possibility is a potential-dependent surface coverage or double-layer transition that changes target selectivity. The final assays alone cannot distinguish these mechanisms. Precipitation could physically block the interface in E0, but E0 also has poorer nominal diffusion, so blockage is not uniquely identified. The superior E2/S0 performance could arise from an especially favorable hidden interface residual rather than the published nominal properties.

Testable consequences for future work

Without claiming these tests were performed, the proposed model predicts that: (1) potentials between -0.5 and 0 V should reveal a peak where declining reaction rate eventually outweighs further efficiency gains; (2) durations beyond 9000 s should eventually show diminishing score gains or a decline; (3) lowering the current cap at fixed potential would have little effect if the process is already transport-limited, but would reduce rate if the cap is binding; (4) time-resolved current and product measurements should show stronger efficiency decay at -1.2 V than at -0.5 V; and (5) replicated E1/E2 and S0/S1 comparisons are necessary before interpreting their small score differences as genuine material effects.

Overall conclusion

This world behaves like a cathodic, transport-coupled electrochemical conversion with a strong penalty for excessive polarization. Electrolyte and solvent act through coupled mass-transfer, ohmic, proton, precipitation, and interface effects rather than through any single nominal property. In the tested region, E2/S0 supplied the best compromise, -0.5 V avoided the efficiency/selectivity losses seen at -1.2 V, and extending electrolysis to 9000 s increased useful conversion enough to outweigh moderate efficiency decline. The account is well supported for the tested comparisons but should not be extrapolated to untested potentials, longer times, other loadings, or real chemical identities without further evidence.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific prior response law or instance parameter set was supplied. The supplied material dossier provided nominal properties and explicitly warned that hidden residuals and solvent coupling could alter them; I treated it as a qualitative prior rather than a claimed performance ranking.

Supported claims and laws:
- Productive polarity: negative bias was supported as the productive direction. Batch 1 at +1.2 V gave zero selective yield and score, whereas batch 2 at -1.2 V, with the same E0/S0 materials, current cap, and duration, showed measurable electrochemical efficiencies and score 0.160. This was the clearest evidence that changed my judgment early in the campaign.
- Intermediate-potential law: stronger cathodic bias was not automatically better. For E2/S0 at 6000 s, score increased from 0.359 at -1.2 V in batch 5 to 0.441 at -0.8 V in batch 10 and 0.455 at -0.5 V in batch 11. Selectivity, yield, and faradaic efficiency also improved. This supported a non-monotone relationship in which excessive polarization incurs side-reaction, interfacial, or transport penalties.
- Duration tradeoff: at E2/S0 and -0.5 V, extending operation from 6000 s in batch 11 to 9000 s in batch 12 raised conversion from 0.410 to 0.578, yield from 0.283 to 0.434, and score from 0.455 to 0.507, while several efficiencies declined modestly. This supported continued product formation with diminishing efficiency over that tested interval.
- Transport-sensitive electrolyte behavior: at common S0/-1.2 V/6000 s conditions, E1 and E2 in batches 4 and 5 substantially outperformed E0 and E3 in batches 3 and 6. This supported the importance of diffusion-layer and interface behavior rather than bulk conductivity alone.
- Precipitation was not required for product formation. Batch 5 had essentially zero precipitation signal yet outperformed the strongly precipitating E0 and E1 cases in batches 3 and 4.

Contradicted or weakened claims:
- A simple bulk-conductivity ranking was contradicted. E3 had the highest nominal electrolyte conductivity but performed poorly in batch 6.
- The expectation that S1's higher nominal diffusivity would make it superior was not supported. S1 in batch 7 scored 0.354, essentially tied with but slightly below S0 in batch 5 at 0.359.
- The conjecture that lower-proton-activity S2 or S3 would improve selectivity was contradicted in the tested E2/-1.2 V setting: batches 8 and 9 had lower selectivity and score than batch 5.
- A strong causal claim that precipitation alone suppresses performance was weakened by batch 4, where E1 retained good performance despite a precipitation signal of 0.840.

Untested claims:
- The optimum potential below -0.5 V was not located.
- Whether operation longer than 9000 s improves or reduces score was not tested.
- Actual current delivery and whether the 500 mA cap bound the process were not measured.
- Potential-dependent parasitic chemistry, concentration polarization, and electrode-surface-state changes remain observationally confounded.
- E2 versus E1 and S0 versus S1 were not replicated, so their fine rankings remain unresolved.
- Electron stoichiometry, local interfacial pH, temperature effects, and time-resolved kinetics were not identified.

2. One discriminating experiment

I would run one new batch with the batch-5 composition and duration—0.020 mol reagent, 0.040 L S0, E2, -1.2 V, and 6000 s—but lower the current cap from 500 to 100 mA. It would be compared prospectively with batch 5 at the same potential and batch 11 at -0.5 V.

My leading explanation is that -1.2 V directly favors parasitic charge transfer or an unfavorable potential-dependent interfacial state. The principal alternative is that batch 5 was poor mainly because a high requested current created concentration gradients and transport limitation.

- If the lower-current experiment retained approximately batch-5-like selectivity and poor energy/faradaic performance, despite less current stress, I would strengthen the potential-specific side-reaction or surface-state explanation.
- If lowering the cap substantially restored selectivity, faradaic efficiency, transport efficiency, and energy efficiency toward batch-11 values, I would favor concentration polarization or current-driven interfacial gradients as the main cause.
- If efficiencies improved but yield became very small, the cap would appear binding and the result would show a rate-efficiency tradeoff rather than cleanly selecting either mechanism.
- If the result were indistinguishable within assay uncertainty, one batch would be insufficient, and direct current-time measurements or replicated tests would be needed.

3. Unused evidence, reliability, and goal effects

Evidence not fully used included the detailed raw spectral traces and individual proxy-peak shapes from the characterization artifacts. I relied mainly on calibrated processed estimates because the hidden species mapping prevented a secure mechanistic assignment of those peaks. Intermediate UV–visible measurements were useful for confirming broad efficiency patterns but were not modeled jointly with final assays. I also did not extract quantitative laws from cost, small temperature changes during solvent addition, capacitance values, individual acid constants, or all declared precipitation constants because the campaign did not independently vary the coupled properties needed to identify their effects.

The least reliable predictions are those requiring multiple simultaneous extrapolations from the campaign. Q01 is especially uncertain because its expected yield lies near the score's multiplicative gate. Q05 extrapolates E1 from -1.2 to -0.8 V at a different loading and cap; Q09 combines S2 with E0, a pairing never tested; and Q11 extrapolates E0 to a milder potential and longer duration under a likely transport-limited 500 mA cap. The positive-potential predictions are directionally more secure because batch 1 was inactive, but their exact near-zero intervals across other electrolytes and solvents remain extrapolations.

The batch-12 recommendation is reliable as the highest observed completed score, but less reliable as a global optimum. It lacks replication, the potential region between -0.5 and 0 V was not explored, durations beyond 9000 s were not tested, and actual current was unknown. The fine choices of E2 over E1 and S0 over S1 are also less reliable than the recommendation's broader preference for moderate negative bias and adequate duration.

The optimization goal did affect evidence collection. After identifying active polarity, I allocated batches adaptively toward higher score rather than constructing a balanced factorial design. This improved the achieved recommendation but left potential, cap, duration, and material interactions partly confounded. All material screens were initially performed at -1.2 V rather than repeated near the later -0.5 V optimum, and no capacity remained for replication. Thus there was a real, though not hidden, tradeoff between score optimization and mechanism identification.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.66,
        "lower80": 0.55,
        "upper80": 0.75
      },
      "energy_efficiency": {
        "estimate": 0.41,
        "lower80": 0.27,
        "upper80": 0.54
      },
      "faradaic_efficiency": {
        "estimate": 0.49,
        "lower80": 0.36,
        "upper80": 0.61
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.36,
        "lower80": 0.15,
        "upper80": 0.47
      },
      "selective_product_yield": {
        "estimate": 0.023,
        "lower80": 0.006,
        "upper80": 0.05
      },
      "transport_efficiency": {
        "estimate": 0.48,
        "lower80": 0.34,
        "upper80": 0.6
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.04
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0,
        "upper80": 0.025
      },
      "faradaic_efficiency": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.04
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.015
      },
      "selective_product_yield": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.012
      },
      "transport_efficiency": {
        "estimate": 0.005,
        "lower80": 0,
        "upper80": 0.03
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.66,
        "lower80": 0.54,
        "upper80": 0.75
      },
      "energy_efficiency": {
        "estimate": 0.3,
        "lower80": 0.17,
        "upper80": 0.43
      },
      "faradaic_efficiency": {
        "estimate": 0.32,
        "lower80": 0.2,
        "upper80": 0.45
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.36,
        "lower80": 0.25,
        "upper80": 0.46
      },
      "selective_product_yield": {
        "estimate": 0.13,
        "lower80": 0.07,
        "upper80": 0.22
      },
      "transport_efficiency": {
        "estimate": 0.32,
        "lower80": 0.2,
        "upper80": 0.45
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.045
      },
      "energy_efficiency": {
        "estimate": 0.004,
        "lower80": 0,
        "upper80": 0.025
      },
      "faradaic_efficiency": {
        "estimate": 0.009,
        "lower80": 0,
        "upper80": 0.04
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.02
      },
      "selective_product_yield": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.013
      },
      "transport_efficiency": {
        "estimate": 0.004,
        "lower80": 0,
        "upper80": 0.03
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.64,
        "lower80": 0.52,
        "upper80": 0.74
      },
      "energy_efficiency": {
        "estimate": 0.46,
        "lower80": 0.32,
        "upper80": 0.58
      },
      "faradaic_efficiency": {
        "estimate": 0.5,
        "lower80": 0.38,
        "upper80": 0.61
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.45,
        "lower80": 0.33,
        "upper80": 0.56
      },
      "selective_product_yield": {
        "estimate": 0.25,
        "lower80": 0.15,
        "upper80": 0.37
      },
      "transport_efficiency": {
        "estimate": 0.52,
        "lower80": 0.39,
        "upper80": 0.64
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.012,
        "lower80": 0,
        "upper80": 0.05
      },
      "energy_efficiency": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.03
      },
      "faradaic_efficiency": {
        "estimate": 0.012,
        "lower80": 0,
        "upper80": 0.045
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.02
      },
      "selective_product_yield": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.014
      },
      "transport_efficiency": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.035
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.52,
        "lower80": 0.4,
        "upper80": 0.64
      },
      "energy_efficiency": {
        "estimate": 0.16,
        "lower80": 0.07,
        "upper80": 0.28
      },
      "faradaic_efficiency": {
        "estimate": 0.18,
        "lower80": 0.1,
        "upper80": 0.3
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.27,
        "lower80": 0.17,
        "upper80": 0.38
      },
      "selective_product_yield": {
        "estimate": 0.075,
        "lower80": 0.035,
        "upper80": 0.14
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
        "lower80": 0,
        "upper80": 0.045
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0,
        "upper80": 0.03
      },
      "faradaic_efficiency": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.04
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.02
      },
      "selective_product_yield": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.013
      },
      "transport_efficiency": {
        "estimate": 0.005,
        "lower80": 0,
        "upper80": 0.035
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.61,
        "lower80": 0.48,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.29,
        "lower80": 0.16,
        "upper80": 0.43
      },
      "faradaic_efficiency": {
        "estimate": 0.28,
        "lower80": 0.16,
        "upper80": 0.42
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.33,
        "lower80": 0.21,
        "upper80": 0.44
      },
      "selective_product_yield": {
        "estimate": 0.12,
        "lower80": 0.055,
        "upper80": 0.22
      },
      "transport_efficiency": {
        "estimate": 0.27,
        "lower80": 0.15,
        "upper80": 0.41
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.045
      },
      "energy_efficiency": {
        "estimate": 0.004,
        "lower80": 0,
        "upper80": 0.025
      },
      "faradaic_efficiency": {
        "estimate": 0.009,
        "lower80": 0,
        "upper80": 0.04
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.02
      },
      "selective_product_yield": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.013
      },
      "transport_efficiency": {
        "estimate": 0.004,
        "lower80": 0,
        "upper80": 0.03
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.64,
        "lower80": 0.51,
        "upper80": 0.74
      },
      "energy_efficiency": {
        "estimate": 0.21,
        "lower80": 0.11,
        "upper80": 0.34
      },
      "faradaic_efficiency": {
        "estimate": 0.22,
        "lower80": 0.12,
        "upper80": 0.35
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.33,
        "lower80": 0.22,
        "upper80": 0.44
      },
      "selective_product_yield": {
        "estimate": 0.15,
        "lower80": 0.08,
        "upper80": 0.25
      },
      "transport_efficiency": {
        "estimate": 0.19,
        "lower80": 0.1,
        "upper80": 0.31
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.045
      },
      "energy_efficiency": {
        "estimate": 0.004,
        "lower80": 0,
        "upper80": 0.025
      },
      "faradaic_efficiency": {
        "estimate": 0.009,
        "lower80": 0,
        "upper80": 0.04
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.02
      },
      "selective_product_yield": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.013
      },
      "transport_efficiency": {
        "estimate": 0.004,
        "lower80": 0,
        "upper80": 0.03
      }
    }
  ],
  "rationale": "The campaign showed that negative bias is the productive direction, while positive bias gave essentially no target formation; therefore all positive-potential queries are predicted near the bounded assay floor. Negative-bias estimates interpolate the E0/E1/E3 screens and the observed improvement from -1.2 to -0.8 V, with charge-per-reagent scaling for the lower loading. E1 is predicted best because of its demonstrated transport advantage; E0 and E3 remain transport-limited, while S2 introduces uncertain coupled conductivity, precipitation, and solvation effects. The 500 mA E0 case is not scaled linearly from its current cap because campaign evidence indicated strong transport limitation. Intervals combine final-assay noise with wider uncertainty for changed loading, duration, current cap, and untested material-potential couplings; Q01 is especially uncertain because its yield lies near the score's multiplicative gate."
}
```
