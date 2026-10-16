# repeat-02/EC-W05-B12-optimization-E-Opaque

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-02\EC-W05-B12-optimization-E-Opaque\participant\optimization-E-Opaque

## 同期笔记

### v1 · 公开事件 0

# Electrochemical campaign hypotheses

## H1 [tentative; pre-experiment]
At fixed loading (0.020 mol reagent in 0.050 L), score will be governed by a tradeoff: increasing absolute potential, current cap, or duration should initially raise conversion/yield but eventually reduce selectivity and energy efficiency and may raise safety risk. Both potential signs must be tested because the productive polarity is unknown.

## H2 [tentative; pre-experiment]
Solvent and electrolyte identities may strongly affect transport/ohmic efficiency and selectivity. Initial screening will compare diverse solvent/electrolyte combinations under matched electrolysis, then refine the most promising region. A useful test consequence is a reproducible score ordering under matched conditions; a single numerical difference will remain provisional given assay noise.

## Decision plan
Keep loading and volume fixed initially, test both signs and material pairs across broad but safe conditions, then allocate later batches to local refinement and at least one repeat. Change course if safety approaches the 0.65 limit or if yield remains near the multiplicative gate.

### v2 · 公开事件 84

# Electrochemical campaign hypotheses and conclusions

## H1 [supported only in tested scope]
At 0.020 mol reagent in 0.050 L solvent-S0 with electrolyte-E0, negative polarity is productive and positive polarity is not. Matched ±1.5 V, 100 mA-cap, 1800 s batches gave score 0 at positive polarity (final assay event runner-operation-0007) versus 0.232 at negative polarity (runner-operation-0014). The sign effect is much larger than the stated assay noise and is treated as robust for this formulation.

Longer electrolysis at −1.5 V increased observed conversion/yield over 1800–14400 s: the 7200 s batch scored 0.260 (runner-operation-0021), and the 14400 s batch scored 0.282 (runner-operation-0028). This is not a general monotonic claim beyond the tested interval. At −2.0 V, 200 mA cap, 7200 s, score fell to 0.249 with poorer energy and transport metrics (runner-operation-0035), supporting an efficiency/selectivity penalty at excessive magnitude.

## H2 [partially supported; material effects confounded in diagonal screen]
Solvent/electrolyte identity materially affects the efficiency balance. Diagonal S1/E1, S2/E2, and S3/E3 screens at −1.5 V for 14400 s scored 0.228, 0.237, and 0.116 (runner-operation-0042, -0049, -0056), all below S0/E0. Because both identities changed together, those comparisons do not isolate which component caused the loss.

With solvent-S0 held fixed, E1, E2, and E3 scored 0.278, 0.272, and 0.258 (runner-operation-0063, -0070, -0077). Numerical differences among E0/E1/E2 are modest relative to single-assay noise, so their fine ordering remains unresolved; E3 appears less promising. Precipitation signal varied sharply with material but was not itself in the score.

## H3 [supported by repeat within tested procedure]
The leading procedure is reproducible at the campaign's resolution: S0/E0, −1.5 V, 100 mA cap, 14400 s scored 0.282 at runner-operation-0028 and 0.283 at runner-operation-0084. The repeat also retained high ohmic efficiency (~1) and similar selectivity/energy/transport measures. This supports selection of the repeated batch rather than interpreting its slightly higher score as a meaningful superiority.

## Operating decision
Recommend 0.020 mol reagent + 0.050 L solvent-S0; set −1.5 V with 100 mA nonnegative current cap and electrolyte-E0; electrolyze 14400 s; then terminate. Scope is this fixed loading and tested range. A future result showing a materially higher repeated score for E1/E2 or a potential near −1.5 V would change the material/potential choice.

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
      "potential_V": 1.5
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
    "cost": 0.286080002784729,
    "electrochemical_conversion": 0.008014115504920483,
    "electrochemical_selectivity": 0.01034972071647644,
    "energy_efficiency": 0.005256945732980967,
    "faradaic_efficiency": 0.02452157624065876,
    "ohmic_efficiency": 0.9704279899597168,
    "pH_normalized": 0.23308512568473816,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
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
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.5
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
    "cost": 0.286080002784729,
    "electrochemical_conversion": 0.007126472890377045,
    "electrochemical_selectivity": 0.5764462351799011,
    "energy_efficiency": 0.12848509848117828,
    "faradaic_efficiency": 0.3251281976699829,
    "ohmic_efficiency": 0.9792658090591431,
    "pH_normalized": 0.2303897738456726,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.23215575516223907,
    "selective_product_yield": 0.017572954297065735,
    "transport_efficiency": 0.3513849973678589
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
    "cost": 0.2893199920654297,
    "electrochemical_conversion": 0.055129412561655045,
    "electrochemical_selectivity": 0.5531466007232666,
    "energy_efficiency": 0.1355162262916565,
    "faradaic_efficiency": 0.2976158857345581,
    "ohmic_efficiency": 0.9660394787788391,
    "pH_normalized": 0.231104776263237,
    "precipitation_signal": 0.9869203567504883,
    "safety_risk": 0.05933958664536476,
    "score": 0.26028773188591003,
    "selective_product_yield": 0.02353670820593834,
    "transport_efficiency": 0.31417277455329895
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
    "cost": 0.29363998770713806,
    "electrochemical_conversion": 0.11758214980363846,
    "electrochemical_selectivity": 0.5377435684204102,
    "energy_efficiency": 0.10239339619874954,
    "faradaic_efficiency": 0.3535277545452118,
    "ohmic_efficiency": 0.9781976342201233,
    "pH_normalized": 0.23041419684886932,
    "precipitation_signal": 0.9876685738563538,
    "safety_risk": 0.05933958664536476,
    "score": 0.28152215480804443,
    "selective_product_yield": 0.06953411549329758,
    "transport_efficiency": 0.3220402002334595
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
      "current_mA": 200,
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
    "cost": 0.2965199947357178,
    "electrochemical_conversion": 0.10170742124319077,
    "electrochemical_selectivity": 0.5160925388336182,
    "energy_efficiency": 0.049550384283065796,
    "faradaic_efficiency": 0.2743712365627289,
    "ohmic_efficiency": 0.9674157500267029,
    "pH_normalized": 0.23537498712539673,
    "precipitation_signal": 0.9869949817657471,
    "safety_risk": 0.05933958664536476,
    "score": 0.24928419291973114,
    "selective_product_yield": 0.05854344367980957,
    "transport_efficiency": 0.2638617753982544
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
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 1,
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
    "cost": 0.3136399984359741,
    "electrochemical_conversion": 0.0867585763335228,
    "electrochemical_selectivity": 0.4219074547290802,
    "energy_efficiency": 0.08703487366437912,
    "faradaic_efficiency": 0.25081631541252136,
    "ohmic_efficiency": 0.9584342837333679,
    "pH_normalized": 0.2054329365491867,
    "precipitation_signal": 0.724872887134552,
    "safety_risk": 0.08273958414793015,
    "score": 0.22810561954975128,
    "selective_product_yield": 0.04567471519112587,
    "transport_efficiency": 0.22613297402858734
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
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 2,
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
    "cost": 0.34564000368118286,
    "electrochemical_conversion": 0.09891442954540253,
    "electrochemical_selectivity": 0.42822012305259705,
    "energy_efficiency": 0.11777473241090775,
    "faradaic_efficiency": 0.23951460421085358,
    "ohmic_efficiency": 0.9791736602783203,
    "pH_normalized": 0.1716480702161789,
    "precipitation_signal": 0.0,
    "safety_risk": 0.10073958337306976,
    "score": 0.23678016662597656,
    "selective_product_yield": 0.04540785774588585,
    "transport_efficiency": 0.24291495978832245
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
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
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
    "cost": 0.3256399929523468,
    "electrochemical_conversion": 0.07117988169193268,
    "electrochemical_selectivity": 0.41127386689186096,
    "energy_efficiency": 0.09588053822517395,
    "faradaic_efficiency": 0.2122533768415451,
    "ohmic_efficiency": 0.9950506687164307,
    "pH_normalized": 0.28314098715782166,
    "precipitation_signal": 0.00031451715040020645,
    "safety_risk": 0.11333958804607391,
    "score": 0.11589864641427994,
    "selective_product_yield": 0.010927664116024971,
    "transport_efficiency": 0.2057580202817917
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
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 1,
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
    "cost": 0.29363998770713806,
    "electrochemical_conversion": 0.10442992299795151,
    "electrochemical_selectivity": 0.5178065896034241,
    "energy_efficiency": 0.16423077881336212,
    "faradaic_efficiency": 0.2763303518295288,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.20306052267551422,
    "precipitation_signal": 0.8586449027061462,
    "safety_risk": 0.05933958664536476,
    "score": 0.27760207653045654,
    "selective_product_yield": 0.07325895130634308,
    "transport_efficiency": 0.29716160893440247
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
      "electrolyte_profile": 2,
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
    "cost": 0.29363998770713806,
    "electrochemical_conversion": 0.11782462894916534,
    "electrochemical_selectivity": 0.540424108505249,
    "energy_efficiency": 0.16214816272258759,
    "faradaic_efficiency": 0.2836216390132904,
    "ohmic_efficiency": 0.9587823152542114,
    "pH_normalized": 0.15213987231254578,
    "precipitation_signal": 0.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.27169692516326904,
    "selective_product_yield": 0.05098104104399681,
    "transport_efficiency": 0.2849712371826172
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
    "cost": 0.29363998770713806,
    "electrochemical_conversion": 0.10774312913417816,
    "electrochemical_selectivity": 0.4915830194950104,
    "energy_efficiency": 0.15742208063602448,
    "faradaic_efficiency": 0.25491824746131897,
    "ohmic_efficiency": 0.9827043414115906,
    "pH_normalized": 0.2696843147277832,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.05933958664536476,
    "score": 0.25816911458969116,
    "selective_product_yield": 0.04875899478793144,
    "transport_efficiency": 0.26209816336631775
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
    "electrochemical_conversion": 0.10495772212743759,
    "electrochemical_selectivity": 0.5490975975990295,
    "energy_efficiency": 0.13320092856884003,
    "faradaic_efficiency": 0.2911659777164459,
    "ohmic_efficiency": 0.9955646991729736,
    "pH_normalized": 0.23062115907669067,
    "precipitation_signal": 0.9938013553619385,
    "safety_risk": 0.05933958664536476,
    "score": 0.2826046645641327,
    "selective_product_yield": 0.07979978621006012,
    "transport_efficiency": 0.31239092350006104
  }
}
```

## K1 封存报告

## Mechanistic interpretation

I interpret this benchmark as a polarity-selective electrochemical conversion with three coupled layers: (1) electrode kinetics determine whether the intended reaction is accessible; (2) accumulated electrolysis exposure controls conversion; and (3) solvent/electrolyte-dependent transport, resistance, speciation, and phase behavior determine how much converted material becomes the selective product and how efficiently electrical input is used.

### 1. Productive polarity is the dominant qualitative variable

The strongest evidence is the matched-polarity comparison. Batches 1 and 2 both used 0.020 mol reagent, 0.050 L solvent-S0, electrolyte-E0, a 100 mA current cap, |V| = 1.5 V, and 1800 s. Batch 1 at +1.5 V gave score 0, electrochemical conversion 0.0080, selectivity 0.0103, selective-product yield 0, faradaic efficiency 0.0245, and transport efficiency 0. Batch 2 at −1.5 V gave score 0.2322, selectivity 0.5764, selective-product yield 0.0176, faradaic efficiency 0.3251, and transport efficiency 0.3514. Their safety risks were identical at 0.05934.

Thus, negative polarization opens the productive pathway, whereas positive polarization mainly fails to produce target product under these conditions. Because the difference is much larger than the stated assay noise, I regard the polarity conclusion as robust within this formulation. A plausible process is electron transfer to a reactant or reactive intermediate at negative potential, followed by a selective chemical step. At positive potential, the corresponding oxidation may be inaccessible or may feed an unobserved side pathway. The public data cannot distinguish direct reactant reduction from reduction of a catalyst, mediator, or solvent-derived intermediate.

A minimal kinetic representation is

r_target = k_target(V, medium, pH) × C_reactant,
r_side = k_side(V, medium, pH) × C_reactant,
selectivity ≈ r_target/(r_target + r_side),

where k_target is effectively activated at negative potential. The observations establish the sign dependence but not the microscopic elementary steps.

### 2. Duration controls accumulated conversion, with an efficiency tradeoff

At −1.5 V, 100 mA cap, S0/E0, increasing electrolysis duration raised conversion and product yield:

- Batch 2, 1800 s: conversion 0.0071, yield 0.0176, score 0.2322.
- Batch 3, 7200 s: conversion 0.0551, yield 0.0235, score 0.2603.
- Batch 4, 14400 s: conversion 0.1176, yield 0.0695, score 0.2815.
- Batch 12, a repeat at 14400 s: conversion 0.1050, yield 0.0798, score 0.2826.

This supports an accumulated-exposure model. If I_eff is the actual cell current, a natural hidden state is charge Q = integral I_eff dt. A possible empirical form is

X(t) = 1 − exp[−k_eff(V, medium) t]

or, more physically, X as a saturating function of Q/(nF N0). Only low conversion was reached—about 0.10–0.12 at 14400 s—so these experiments do not locate a true conversion plateau.

The efficiencies did not improve with time in the same way. From batch 2 to batch 4, final faradaic efficiency was broadly similar (0.325 versus 0.354), transport efficiency was similar (0.351 versus 0.322), and selectivity remained near 0.54–0.58, but energy efficiency decreased from 0.1285 to 0.1024. This suggests that longer operation accumulates more product while also accumulating electrical losses, concentration polarization, or nonproductive charge. Consequently, the balanced score increased only modestly despite the substantial conversion increase.

Selective-product yield is approximately, but not exactly, conversion multiplied by selectivity. For example, batch 4 has 0.1176 × 0.5377 ≈ 0.063, near its measured yield of 0.0695. Departures in other batches are compatible with assay noise, hidden process factors, or the benchmark using related but nonidentical definitions for conversion, selectivity, and isolated selective yield. I would therefore not impose exact algebraic equality.

### 3. Potential magnitude has a productive window rather than a simple “more is better” effect

Batch 5 used −2.0 V, a 200 mA cap, and 7200 s in S0/E0. Relative to batch 3 at −1.5 V, 100 mA, and the same duration, conversion rose from 0.0551 to 0.1017 and yield from 0.0235 to 0.0585. However, selectivity fell from 0.5531 to 0.5161, energy efficiency from 0.1355 to 0.0496, faradaic efficiency from 0.2976 to 0.2744, transport efficiency from 0.3142 to 0.2639, and score from 0.2603 to 0.2493.

This changed the initial “greater driving force should improve performance” hypothesis into a window hypothesis: additional overpotential accelerates charge transfer and conversion but also drives side reactions and dissipative losses. A schematic relation is

k_target ∝ exp(a_target |η|),
k_side ∝ exp(a_side |η|),

with the side pathway or energy penalty becoming relatively more important at large |η|. The selected −1.5 V condition is therefore a balance, not necessarily the kinetic maximum.

This comparison is confounded because both potential and current cap changed. The actual current was never reported, so it is unknown whether the 100 or 200 mA cap was binding. Accordingly, I can attribute the result only to the combined electrical setting, not uniquely to potential.

### 4. Medium identity couples transport, selectivity, pH, and phase behavior

The diagonal material screen at −1.5 V, 100 mA, and 14400 s produced:

- Batch 4, S0/E0: score 0.2815, conversion 0.1176, selectivity 0.5377, yield 0.0695.
- Batch 6, S1/E1: score 0.2281, conversion 0.0868, selectivity 0.4219, yield 0.0457.
- Batch 7, S2/E2: score 0.2368, conversion 0.0989, selectivity 0.4282, yield 0.0454.
- Batch 8, S3/E3: score 0.1159, conversion 0.0712, selectivity 0.4113, yield 0.0109.

This establishes that medium formulation matters, but it does not separate solvent effects from electrolyte effects because both changed together.

Batches 9–11 held solvent-S0 fixed and varied electrolyte. E1, E2, and E3 respectively scored 0.2776, 0.2717, and 0.2582, versus 0.2815 and 0.2826 for the two E0 observations. E0, E1, and E2 are close enough that their precise ordering is not secure from one assay each; E3 appears less favorable. The electrolyte can plausibly affect solution conductivity, interfacial field, ion pairing, reactant speciation, proton availability, and migration of charged intermediates.

The phase-related observables show especially strong coupling. In solvent-S0, precipitation signal was about 0.99–1.00 with E0, 0.859 with E1, 0 with E2, and 0.005 with E3. Normalized pH also shifted: approximately 0.23 for E0, 0.203 for E1, 0.152 for E2, and 0.270 for E3. These changes indicate that electrolyte identity changes acid/base or solubility behavior, not merely bulk resistance. Nevertheless, precipitation was not directly penalized in the published score, and high-scoring E0 batches had almost complete precipitation signal. It could represent benign product precipitation, an unrelated salt, or a benchmark phase marker; its chemical identity is unidentifiable.

Ohmic efficiency remained high in almost every final assay, generally 0.96–1.00, while transport and faradaic efficiencies were only about 0.21–0.35. Thus, simple resistive loss was probably not the primary bottleneck in the tested region. Charge utilization and mass transport were more limiting. One possible factorization is

energy efficiency ≈ f_voltage(V) × faradaic efficiency × transport efficiency × ohmic efficiency,

but the observed values do not satisfy a single exact product rule. I regard this only as a conceptual decomposition; independent noise and hidden normalization likely affect each reported channel.

### 5. Safety and cost behavior

At fixed reagent loading, the visible safety risk depended strongly on solvent choice but did not increase during the tested electrolysis intervals. S0 batches had risk 0.05934, whereas the S1, S2, and S3 diagonal batches had risks 0.08274, 0.10074, and 0.11334. All are well below the 0.65 limit. This pattern suggests that the reported risk is dominated by material inventory or solvent hazard terms rather than electrical exposure at these settings. Because solvent and electrolyte were changed together in those batches, a smaller electrolyte contribution cannot be excluded.

No experiment approached the safety boundary, so the campaign does not identify nonlinear high-risk regimes. Extrapolation to larger reagent quantities, higher concentration, longer times, or more extreme potentials is unsupported.

### 6. How the explanation evolved

Batch 1 initially showed that the chosen positive polarity was essentially inactive. Batch 2 reversed the polarity and immediately established a productive negative-potential mechanism. Batches 3 and 4 then showed that accumulated electrolysis time raises conversion and yield. Batch 5 demonstrated that a more extreme electrical setting sacrifices balanced efficiency despite increasing conversion, motivating the finite-window interpretation. Batches 6–8 revealed strong formulation dependence, while batches 9–11 narrowed part of that effect to electrolyte-dependent speciation and transport within S0. Batch 12 repeated batch 4 and reproduced its score very closely: 0.2826 versus 0.2815. That repeat is the main evidence that the selected procedure is stable at the resolution of this campaign rather than a single favorable assay fluctuation.

### 7. Scope, unknowns, and alternatives

The conclusions apply to 0.020 mol reagent in 0.050 L solvent, a nominal initial concentration of 0.4 mol/L, and only the tested anonymous materials. Reagent loading, concentration, solvent volume, electrode geometry, temperature, stirring, cell resistance, and actual current were not varied or observed. The current setting is a cap rather than a measured current, so charge throughput and current density cannot be reconstructed. Solvent effects are poorly isolated because only S0 received an electrolyte series; no full solvent-by-electrolyte factorial design was performed. Potential was sampled sparsely (+1.5, −1.5, and one confounded −2.0 condition), so −1.5 V is the best tested value, not a proven mathematical optimum.

Several mechanisms remain plausible: direct electroreduction of the limiting reagent; reduction of a mediator followed by homogeneous conversion; electrode generation of an acid/base species that changes substrate speciation; or a coupled electron-transfer/precipitation process that removes product from solution. The public observations cannot identify molecular species or determine whether precipitation is cause, consequence, or spectator. Similarly, poor positive-polarity performance could reflect thermodynamic mismatch, electrode passivation, or formation of undetected byproducts.

Within these limits, the most economical explanatory model is: negative potential activates the target pathway; duration accumulates conversion; excessive driving force increases conversion but disproportionately harms energy, faradaic, transport, and selectivity terms; and solvent/electrolyte-dependent speciation and mobility tune those competing pathways. This model explains why the sealed S0/E0, −1.5 V, 100 mA-cap, 14400 s procedure gave the best and repeatable balanced score without claiming that it is globally optimal outside the tested domain.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific prior, nominal material-property dossier, or supplied mechanistic law was provided. The only material information was anonymous solvent and electrolyte labels, so all substantive hypotheses were self-developed.

Supported:
- Productive conversion depends strongly on polarity. Matched batches 1 and 2 showed essentially no target production at +1.5 V but a score of 0.232 at −1.5 V. Before those experiments, the productive sign was explicitly unknown; batch 2 was the evidence that changed the explanation toward a negative-potential pathway.
- Accumulated electrolysis exposure raises conversion and yield in the tested S0/E0 region. At −1.5 V and 100 mA, batches 2, 3, and 4 increased duration from 1800 to 7200 to 14400 s; conversion rose from 0.0071 to 0.0551 to 0.1176. Batch 12 repeated the 14400 s procedure and gave conversion 0.1050 and nearly the same score as batch 4, supporting repeatability.
- Greater electrical forcing can trade balanced efficiency for conversion. Compared with batch 3, batch 5 used −2.0 V and 200 mA at the same 7200 s duration. Conversion increased from 0.0551 to 0.1017, but energy efficiency, transport efficiency, selectivity, and overall score declined. This changed the initial broad monotonic expectation into a finite productive-window hypothesis.
- Medium identity matters. Batches 6–8 produced substantially different scores and phase behavior from S0/E0, while batches 9–11 showed electrolyte-dependent changes within solvent-S0. The exact ranking of E0, E1, and E2 was not securely resolved, but E3 appeared less favorable.
- A charge-based relationship was supported retrospectively by the numerical results: batches 3 and 5 were approximately consistent with conversion scaling as I·t·FE/(2Fn). This is an empirical interpretation, not proof of a two-electron molecular mechanism.

Contradicted or narrowed:
- A simple “more potential/current is better” law was contradicted by batch 5: higher conversion did not imply a higher balanced score.
- Any simple claim that high precipitation signal is necessarily harmful was contradicted in the scoring sense: the best S0/E0 batches 4 and 12 had precipitation signals near one. Its chemical meaning remains unknown.
- A precise material ranking was not supported. Differences among E0, E1, and E2 were modest relative to assay noise and were usually based on one batch each.

Untested:
- Exact reaction order, molecular intermediates, electron stoichiometry, actual current versus current-cap behavior, and whether precipitation is product, salt, or spectator remained untested.
- Loading, concentration, volume, temperature, mixing, electrode geometry, and potentials near −1.5 V were not systematically varied.
- The campaign did not test a full solvent-by-electrolyte factorial design or establish behavior beyond 14400 s.

2. Most informative additional experiment

I would repeat the batch-4/12 formulation and potential—0.020 mol reagent, 0.050 L S0, E0, and −1.5 V—but use 500 mA for 2880 s. This supplies the same nominal charge as 100 mA for 14400 s while changing current and residence time by a factor of five.

The leading charge-controlled explanation predicts broadly similar conversion after correcting for faradaic efficiency. If yield and score also remained near batches 4 and 12, that would support charge throughput as the main conversion variable and weaken alternatives requiring long homogeneous reaction time.

If conversion were similar but selectivity, transport efficiency, or energy efficiency were substantially worse, I would retain charge control for conversion but infer a current-density-dependent mass-transfer or side-reaction penalty. If conversion were much lower despite equal nominal charge, I would conclude that the configured current is only a cap, that −1.5 V cannot deliver 500 mA, or that time-dependent homogeneous chemistry is important. If the short high-current batch performed much better, I would infer that prolonged exposure causes product loss or other time-dependent degradation.

3. Unused evidence, reliability, and goal effects

The intermediate UV–visible measurements were used only qualitatively; their full spectra, raw signals, calibration details, and differences from the final assays were not modeled. Cost observations were not mechanistically analyzed. pH and precipitation measurements were noted, but without species identities they could not be assigned causal roles. The campaign also did not exploit repeated assays to estimate batch-to-batch variance except for the exact-condition repeat in batches 4 and 12.

The least reliable blind predictions are Q11 and Q12 because 500 mA is far outside the independently tested current setting and actual current delivery was unobserved. All predictions at ±0.8 V are extrapolations beyond the measured potentials. Q09 and Q10 are additionally uncertain because the S2/E0 combination was never tested; solvent-S2 was observed only with E2. The 600 s predictions Q01 and Q02 are sensitive to assay-floor clipping and the selective-yield score gate. Positive-polarity scores are likely low, but their exact near-zero values are poorly identifiable.

The sealed recommendation is comparatively reliable only for reproducing the exact batch-4/12 operating point. Its claim to global optimality is weak because potential was sparsely sampled, current and potential were confounded in batch 5, and no loading optimization was performed.

The assigned goal did affect evidence collection. Maximizing the public balanced score encouraged exploitation of S0/E0 and use of every final assay, rather than a full factorial mechanistic study. After the poor diagonal material screens, remaining batches were directed toward electrolyte comparisons in S0 and a repeat of the best recipe. That improved confidence in the recommendation but left solvent effects, current dependence, charge-versus-time dependence, and molecular mechanism underidentified. There was no clear conflict between the optimization goal and safety evidence because every tested batch remained far below the safety limit.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.61,
        "lower80": 0.47,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.21,
        "lower80": 0.08,
        "upper80": 0.33
      },
      "faradaic_efficiency": {
        "estimate": 0.34,
        "lower80": 0.23,
        "upper80": 0.45
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.076,
        "lower80": 0.0,
        "upper80": 0.22
      },
      "selective_product_yield": {
        "estimate": 0.0054,
        "lower80": 0.0,
        "upper80": 0.025
      },
      "transport_efficiency": {
        "estimate": 0.39,
        "lower80": 0.27,
        "upper80": 0.51
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.075
      },
      "energy_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "faradaic_efficiency": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.085
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.055
      },
      "selective_product_yield": {
        "estimate": 0.0005,
        "lower80": 0.0,
        "upper80": 0.012
      },
      "transport_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.06
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.48,
        "upper80": 0.7
      },
      "energy_efficiency": {
        "estimate": 0.2,
        "lower80": 0.1,
        "upper80": 0.3
      },
      "faradaic_efficiency": {
        "estimate": 0.34,
        "lower80": 0.25,
        "upper80": 0.43
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.307,
        "lower80": 0.245,
        "upper80": 0.365
      },
      "selective_product_yield": {
        "estimate": 0.0634,
        "lower80": 0.025,
        "upper80": 0.11
      },
      "transport_efficiency": {
        "estimate": 0.38,
        "lower80": 0.28,
        "upper80": 0.49
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "energy_efficiency": {
        "estimate": 0.007,
        "lower80": 0.0,
        "upper80": 0.065
      },
      "faradaic_efficiency": {
        "estimate": 0.021,
        "lower80": 0.0,
        "upper80": 0.09
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.065
      },
      "selective_product_yield": {
        "estimate": 0.0007,
        "lower80": 0.0,
        "upper80": 0.014
      },
      "transport_efficiency": {
        "estimate": 0.007,
        "lower80": 0.0,
        "upper80": 0.065
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.45,
        "upper80": 0.69
      },
      "energy_efficiency": {
        "estimate": 0.24,
        "lower80": 0.12,
        "upper80": 0.35
      },
      "faradaic_efficiency": {
        "estimate": 0.3,
        "lower80": 0.21,
        "upper80": 0.39
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.299,
        "lower80": 0.21,
        "upper80": 0.36
      },
      "selective_product_yield": {
        "estimate": 0.0541,
        "lower80": 0.018,
        "upper80": 0.1
      },
      "transport_efficiency": {
        "estimate": 0.36,
        "lower80": 0.25,
        "upper80": 0.47
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.014,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "energy_efficiency": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "faradaic_efficiency": {
        "estimate": 0.019,
        "lower80": 0.0,
        "upper80": 0.085
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.065
      },
      "selective_product_yield": {
        "estimate": 0.0006,
        "lower80": 0.0,
        "upper80": 0.014
      },
      "transport_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.065
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.54,
        "lower80": 0.4,
        "upper80": 0.66
      },
      "energy_efficiency": {
        "estimate": 0.2,
        "lower80": 0.09,
        "upper80": 0.31
      },
      "faradaic_efficiency": {
        "estimate": 0.27,
        "lower80": 0.17,
        "upper80": 0.37
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.276,
        "lower80": 0.16,
        "upper80": 0.35
      },
      "selective_product_yield": {
        "estimate": 0.0453,
        "lower80": 0.012,
        "upper80": 0.09
      },
      "transport_efficiency": {
        "estimate": 0.32,
        "lower80": 0.2,
        "upper80": 0.43
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.075
      },
      "energy_efficiency": {
        "estimate": 0.007,
        "lower80": 0.0,
        "upper80": 0.065
      },
      "faradaic_efficiency": {
        "estimate": 0.017,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "selective_product_yield": {
        "estimate": 0.0005,
        "lower80": 0.0,
        "upper80": 0.013
      },
      "transport_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.06
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.49,
        "lower80": 0.35,
        "upper80": 0.62
      },
      "energy_efficiency": {
        "estimate": 0.16,
        "lower80": 0.06,
        "upper80": 0.28
      },
      "faradaic_efficiency": {
        "estimate": 0.3,
        "lower80": 0.2,
        "upper80": 0.4
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.268,
        "lower80": 0.15,
        "upper80": 0.35
      },
      "selective_product_yield": {
        "estimate": 0.0457,
        "lower80": 0.012,
        "upper80": 0.095
      },
      "transport_efficiency": {
        "estimate": 0.34,
        "lower80": 0.22,
        "upper80": 0.45
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.011,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "energy_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "faradaic_efficiency": {
        "estimate": 0.018,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "selective_product_yield": {
        "estimate": 0.0005,
        "lower80": 0.0,
        "upper80": 0.013
      },
      "transport_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.06
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.42,
        "upper80": 0.69
      },
      "energy_efficiency": {
        "estimate": 0.13,
        "lower80": 0.04,
        "upper80": 0.25
      },
      "faradaic_efficiency": {
        "estimate": 0.26,
        "lower80": 0.15,
        "upper80": 0.38
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.342,
        "lower80": 0.25,
        "upper80": 0.43
      },
      "selective_product_yield": {
        "estimate": 0.234,
        "lower80": 0.1,
        "upper80": 0.42
      },
      "transport_efficiency": {
        "estimate": 0.22,
        "lower80": 0.1,
        "upper80": 0.36
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "faradaic_efficiency": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.095
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.075
      },
      "selective_product_yield": {
        "estimate": 0.0006,
        "lower80": 0.0,
        "upper80": 0.017
      },
      "transport_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.07
      }
    }
  ],
  "rationale": "Negative polarity was strongly productive in the campaign, whereas positive polarity produced essentially no target signal, so all +0.8 V predictions remain near the assay floor. For negative batches I extrapolated the observed potential dependence of selectivity and efficiencies from −1.5 and −2.0 V. Charge balance in campaign batches 3 and 5 was consistent with approximately two-electron conversion, X≈I·t·FE/(2Fn), which informed the effects of duration, reagent amount, and especially the 500 mA condition. E1 was modeled as similar to E0 with somewhat lower faradaic/transport performance but higher energy efficiency; E3 and solvent-S2 received penalties supported by batches 7 and 11. Score estimates apply the published component weights and selective-yield gate. Intervals are wider for the untested −0.8 V, altered concentration, high-current extrapolation, and near-zero gated scores."
}
```
