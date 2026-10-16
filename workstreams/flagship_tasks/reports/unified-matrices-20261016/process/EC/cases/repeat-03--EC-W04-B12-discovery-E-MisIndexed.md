# repeat-03/EC-W04-B12-discovery-E-MisIndexed

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-03\EC-W04-B12-discovery-E-MisIndexed\participant\discovery-E-MisIndexed

## 同期笔记

### v1 · 公开事件 0

# Electrochemical mechanism notebook

## Pre-experiment expectations

**H1 [tentative].** Product formation should depend on signed overpotential rather than absolute voltage. Because nominal standard-potential shifts vary by solvent and electrolyte, the favorable potential magnitude/sign may move with material pairing. A polarity screen at matched loading, volume, duration, and current cap should sharply distinguish productive from unproductive sign.

**H2 [tentative].** Conversion should rise with delivered charge/time and then saturate, while selectivity and energy efficiency may fall at excessive magnitude or duration through side reactions. Thus a short/long duration pair and a voltage series can identify a productive window rather than merely maximize conversion.

**H3 [tentative].** Transport/ohmic behavior should track the nominal conductivity–diffusivity tradeoff, but hidden fixed residuals may reverse the nominal ranking. E0/S0 is the initial reference because its nominal conductivity is favorable; E1 may improve mass transport; E2 may improve ohmic efficiency but shifts the electrochemical threshold.

**Plan.** Use a fixed loading of 0.020 mol in 0.040 L for comparability. First screen signed potential on E0/S0 at matched current cap and time; then map duration, current cap, and voltage magnitude near the productive sign; finally compare materials under a shared promising condition and replicate a promising batch. UV–vis intermediate measurements will be used after electrolysis in each batch to obtain efficiency diagnostics; final assay remains authoritative. Predictions will be revised if matched comparisons contradict these trends.

### v2 · 公开事件 14

# Electrochemical mechanism notebook

## Current hypotheses

**H1 [supported for E0/S0 near |1.2 V|].** Productive polarity is negative. At matched 0.020 mol / 0.040 L, E0/S0, 100 mA cap, and 600 s, +1.2 V gave essentially zero yield/efficiency (final assay event runner-operation-0007), whereas −1.2 V gave selective-product yield 0.0128, selectivity 0.632, faradaic efficiency 0.391 and transport efficiency 0.417 (runner-operation-0014). This is a large numerical polarity contrast, though each condition is unreplicated. The sign effect is consistent with a cathodic target pathway, not an absolute-voltage response.

**H2 [tentative].** The low yield at −1.2 V is charge/transport limited at 600 s rather than intrinsically unreactive: the current cap and short duration supply little charge, while selectivity is already moderate. Prediction: extending duration at the same setting should increase yield/conversion, initially roughly with charge, then plateau or lose selectivity.

**H3 [unresolved].** E0/S0 has high ohmic efficiency but poor transport and maximal precipitation signal in both polarity tests. E0 nominal salt precipitation may be limiting accessible reactant. Material comparisons must separate transport and precipitation from voltage-threshold shifts.

## Next decisions

Map time at −1.2 V (longer duration) and current-cap dependence. Then vary negative potential magnitude to locate the selectivity/energy optimum. Compare electrolyte/solvent identities using the same fixed loading and a shared negative-potential condition. Replicate the most informative/promising condition; revise H2 if longer time does not raise yield.

### v3 · 公开事件 84

# Electrochemical mechanism notebook

## Final source-stage synthesis

**H1 [supported in tested scope].** The target pathway is cathodic. Under matched E0/S0, 0.020 mol in 0.040 L, 100 mA cap, 600 s, +1.2 V was effectively inactive (runner-operation-0007), while −1.2 V produced measurable target yield and moderate selectivity/faradaic efficiency (runner-operation-0014). The large sign contrast supports signed overpotential control. The exact threshold is material dependent because nominal solvent/electrolyte standard-potential shifts differ.

**H2 [supported qualitatively, quantitative form unresolved].** There is a negative-potential window rather than monotonic benefit from magnitude. On E0/S0 at 600 s and 100 mA, −0.8 V showed higher selectivity, faradaic and energy efficiencies than −1.2 V, while −1.8 V was substantially worse (runner-operation-0035 versus -0014 and -0028). On E3/S0, −0.5 V had high energy efficiency but substantially lower target yield than −0.8 V (runner-operation-0077 versus -0063), suggesting onset between these settings followed by increasing parasitic loss at large overpotential.

**H3 [supported, with a nonmonotonic product-time consequence].** Longer electrolysis increases the conversion-like assay channel but does not proportionally increase isolated/selective target yield. At E0/S0, extending −1.2 V from 600 to 3600 s changed assay conversion upward but did not improve target yield (runner-operation-0014 versus -0021). At E3/S0, −0.8 V extension from 600 to 3600 s raised conversion to 0.0463 while target yield fell from 0.0200 to 0.0140 in the observed pair (runner-operation-0063 versus -0070). This is consistent with target formation followed by secondary loss or a competing pathway, but assay noise and lack of time-series replicates leave the kinetic form unresolved. Testable consequence: a duration sweep should show an interior maximum in target yield even as conversion continues rising.

**H4 [supported for current-cap contrast on E0/S0].** Increasing the cap from 100 to 500 mA at −0.8 V, 600 s only modestly increased observed target yield while sharply lowering faradaic, transport, ohmic and energy efficiencies (runner-operation-0035 versus -0042). The cap is a ceiling rather than delivered current; nevertheless, the efficiency change indicates the high-cap regime permits substantially more parasitic/ohmic burden. Prediction: below the binding cap, outcomes should be cap-insensitive; once binding, higher cap gives diminishing yield and poorer efficiency.

**H5 [material effects supported; mechanism partition unresolved].** E3/S0 at −0.8 V, 100 mA, 600 s gave the campaign's highest observed score and yield with near-zero precipitation (runner-operation-0063). Its repeat retained near-zero precipitation and similar order of yield but lower score/efficiencies (runner-operation-0084), demonstrating process/instrument variation and preventing a precise point-law claim. E2/S0 also eliminated precipitation but did not improve target yield over E0/S0 (runner-operation-0049 versus -0035), so removing precipitation alone is insufficient. E3's stronger nominal acidity and thinner diffusion layer are plausible contributors, while its lower conductivity opposes a simple conductivity-only explanation. E0/S1 reduced target yield to zero in one assay (runner-operation-0056), showing solvent identity matters independently of nominal diffusivity.

## Predictive account and scope

At fixed loading, target yield can be treated as a cathodic onset/window response multiplied by material-specific faradaic selectivity and a time-dependent survival term. Conversion rises with cumulative delivered charge, but target survival/selectivity decay at long time or excessive negative magnitude/current. Transport and ohmic factors modulate delivered charge; precipitation can suppress accessible reactant but is not the sole yield determinant. This account is qualitative because only sparse paired conditions and one repeat were available; exact coefficients, onset shifts, and long-time decay constants remain unresolved.

## Recommendation decision

Recommend completed batch 9 (E3/S0, −0.8 V, 100 mA cap, 600 s, fixed 0.020 mol/0.040 L) because it had the highest observed score and selective-product yield, near-zero precipitation, and strong ohmic/energy behavior. The lower repeat in batch 12 argues for cautious expectations rather than changing the selected observed batch. I would change this decision if replicated neighboring potentials/times showed a reliably higher mean yield or if a safety constraint emerged; all tested safety-risk observations remained below the stated limit.

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
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.6320253610610962,
    "energy_efficiency": 0.19927366077899933,
    "faradaic_efficiency": 0.3906446099281311,
    "ohmic_efficiency": 0.9716616868972778,
    "pH_normalized": 0.2317349761724472,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.18808011710643768,
    "selective_product_yield": 0.012758851982653141,
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
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.2
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
    "cost": 0.28432801365852356,
    "electrochemical_conversion": 0.03089923784136772,
    "electrochemical_selectivity": 0.6087257862091064,
    "energy_efficiency": 0.20630478858947754,
    "faradaic_efficiency": 0.3631322681903839,
    "ohmic_efficiency": 0.9584352970123291,
    "pH_normalized": 0.2324499785900116,
    "precipitation_signal": 0.9863388538360596,
    "safety_risk": 0.072194404900074,
    "score": 0.16994643211364746,
    "selective_product_yield": 0.011838189326226711,
    "transport_efficiency": 0.37968918681144714
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
      "potential_V": -1.8
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
    "cost": 0.28303200006484985,
    "electrochemical_conversion": 0.0008542571449652314,
    "electrochemical_selectivity": 0.5147737860679626,
    "energy_efficiency": 0.055148832499980927,
    "faradaic_efficiency": 0.3265741467475891,
    "ohmic_efficiency": 0.9799388647079468,
    "pH_normalized": 0.23175939917564392,
    "precipitation_signal": 0.9870871305465698,
    "safety_risk": 0.072194404900074,
    "score": 0.03867320343852043,
    "selective_product_yield": 0.0033102179877460003,
    "transport_efficiency": 0.2950865924358368
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
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -0.8
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
    "cost": 0.28279200196266174,
    "electrochemical_conversion": 0.010722673498094082,
    "electrochemical_selectivity": 0.6870147585868835,
    "energy_efficiency": 0.38973236083984375,
    "faradaic_efficiency": 0.4788903594017029,
    "ohmic_efficiency": 0.9560095071792603,
    "pH_normalized": 0.23672018945217133,
    "precipitation_signal": 0.9864134788513184,
    "safety_risk": 0.072194404900074,
    "score": 0.23302718997001648,
    "selective_product_yield": 0.013415700756013393,
    "transport_efficiency": 0.4683808982372284
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
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -0.8
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
    "cost": 0.28356000781059265,
    "electrochemical_conversion": 0.012271043844521046,
    "electrochemical_selectivity": 0.7057439684867859,
    "energy_efficiency": 0.11448747664690018,
    "faradaic_efficiency": 0.15424512326717377,
    "ohmic_efficiency": 0.7896485328674316,
    "pH_normalized": 0.2334442436695099,
    "precipitation_signal": 0.997043788433075,
    "safety_risk": 0.072194404900074,
    "score": 0.19539985060691833,
    "selective_product_yield": 0.017436282709240913,
    "transport_efficiency": 0.12956178188323975
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
      "solvent": 0,
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -0.8
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
    "cost": 0.28279200196266174,
    "electrochemical_conversion": 0.01677713729441166,
    "electrochemical_selectivity": 0.6374239325523376,
    "energy_efficiency": 0.4406839907169342,
    "faradaic_efficiency": 0.4153667986392975,
    "ohmic_efficiency": 0.9788278341293335,
    "pH_normalized": 0.1590873748064041,
    "precipitation_signal": 0.0,
    "safety_risk": 0.072194404900074,
    "score": 0.19201438128948212,
    "selective_product_yield": 0.011400886811316013,
    "transport_efficiency": 0.41876718401908875
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
      "solvent": 1,
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -0.8
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
    "cost": 0.2987920045852661,
    "electrochemical_conversion": 0.001116607105359435,
    "electrochemical_selectivity": 0.6251427531242371,
    "energy_efficiency": 0.3617182970046997,
    "faradaic_efficiency": 0.4021787941455841,
    "ohmic_efficiency": 0.9624764323234558,
    "pH_normalized": 0.23410847783088684,
    "precipitation_signal": 0.9904223084449768,
    "safety_risk": 0.09559440612792969,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.3956834375858307
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
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": -0.8
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
    "cost": 0.28279200196266174,
    "electrochemical_conversion": 0.003251433838158846,
    "electrochemical_selectivity": 0.5215097665786743,
    "energy_efficiency": 0.38179445266723633,
    "faradaic_efficiency": 0.3228035867214203,
    "ohmic_efficiency": 0.9906403422355652,
    "pH_normalized": 0.2710776925086975,
    "precipitation_signal": 0.008188718929886818,
    "safety_risk": 0.072194404900074,
    "score": 0.2935795485973358,
    "selective_product_yield": 0.01996052823960781,
    "transport_efficiency": 0.34363484382629395
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
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": -0.8
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
    "cost": 0.2837519943714142,
    "electrochemical_conversion": 0.04628780111670494,
    "electrochemical_selectivity": 0.5497019290924072,
    "energy_efficiency": 0.36497190594673157,
    "faradaic_efficiency": 0.3404853045940399,
    "ohmic_efficiency": 0.9500912427902222,
    "pH_normalized": 0.26876354217529297,
    "precipitation_signal": 0.0,
    "safety_risk": 0.072194404900074,
    "score": 0.2074926495552063,
    "selective_product_yield": 0.013969291932880878,
    "transport_efficiency": 0.3418349027633667
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
      "current_mA": 100,
      "electrolyte_profile": 3,
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
    "cost": 0.28271999955177307,
    "electrochemical_conversion": 0.019349945709109306,
    "electrochemical_selectivity": 0.5591211318969727,
    "energy_efficiency": 0.5451909303665161,
    "faradaic_efficiency": 0.38156959414482117,
    "ohmic_efficiency": 0.9401222467422485,
    "pH_normalized": 0.26974859833717346,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.072194404900074,
    "score": 0.08131737262010574,
    "selective_product_yield": 0.004944234620779753,
    "transport_efficiency": 0.38874951004981995
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
      "current_mA": 100,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": -0.8
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
    "cost": 0.28279200196266174,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.513342559337616,
    "energy_efficiency": 0.3417770266532898,
    "faradaic_efficiency": 0.29734501242637634,
    "ohmic_efficiency": 0.9769180417060852,
    "pH_normalized": 0.27026891708374023,
    "precipitation_signal": 0.0,
    "safety_risk": 0.072194404900074,
    "score": 0.19174684584140778,
    "selective_product_yield": 0.013789936900138855,
    "transport_efficiency": 0.31856995820999146
  }
}
```

## K1 封存报告

## Mechanistic account

I infer that the desired product is formed by a cathodic pathway controlled by effective overpotential, charge delivery, interfacial selectivity, mass transport, and product survival. A compact qualitative model is:

η = −[Vapplied − Eeffective(materials)]

rate_target(t) ≈ ktarget(η, electrolyte, solvent, pH) × transport × available_reactant

rate_side(t) ≈ kside(η, current, materials) × available_reactant

observed target yield ≈ ∫ rate_target(t) × survival(t) dt.

Here Eeffective includes the declared solvent/electrolyte potential shifts plus unknown fixed world-specific interfacial residuals. “Current” in the experiments was a current cap, not a measured delivered current, so charge cannot be calculated from cap × time without an additional current trace. Transport, ohmic loss, precipitation, and secondary destruction affect different parts of the response and cannot be reduced to one material ranking.

### 1. Polarity and potential window

The strongest mechanistic evidence is the matched polarity comparison on E0/S0 at 0.020 mol reagent, 0.040 L solvent, a 100 mA cap, and 600 s. Batch 1 at +1.2 V was essentially inactive: selective-product yield was 0, conversion 0.0080, selectivity 0.0103, faradaic efficiency 0.0245, and energy efficiency 0.0053. Batch 2 at −1.2 V instead gave yield 0.01276, selectivity 0.632, faradaic efficiency 0.391, transport efficiency 0.417, and energy efficiency 0.199. Although neither polarity was replicated, this contrast is much larger than the declared assay noise and supports a cathodic, signed-overpotential mechanism rather than one responding only to |V|.

The response was not monotonic with increasingly negative voltage. On E0/S0 at 100 mA and 600 s, batch 5 at −0.8 V gave yield 0.01342, selectivity 0.687, faradaic efficiency 0.479, transport efficiency 0.468, and energy efficiency 0.390. Batch 2 at −1.2 V had similar yield but poorer efficiencies, while batch 4 at −1.8 V fell to yield 0.00331, selectivity 0.515, faradaic efficiency 0.327, transport efficiency 0.295, and energy efficiency 0.0551. I therefore infer an operating window: insufficient cathodic drive lies below onset, moderate drive favors the target, and excessive drive increasingly favors parasitic electrochemistry and energy loss.

Batch 11 provides evidence for the low-voltage side of this window in E3/S0. At −0.5 V, 100 mA, and 600 s, energy efficiency was high (0.545), but target yield was only 0.00494. Batch 9 at −0.8 V under otherwise matched conditions gave yield 0.01996 and energy efficiency 0.382. This suggests that −0.5 V is near or below productive onset for this material pair, while −0.8 V supplies enough cathodic drive. The exact onset is not identified.

### 2. Time, conversion, and secondary loss

Longer electrolysis did not proportionally improve the target-yield channel. For E0/S0 at −1.2 V and 100 mA, extending time from 600 s in batch 2 to 3600 s in batch 3 increased measured conversion from a noise-clipped 0 to 0.0309, but yield changed from 0.01276 to 0.01184; selectivity and the efficiency channels also did not improve. For E3/S0 at −0.8 V and 100 mA, batch 9 at 600 s gave yield 0.01996, whereas batch 10 at 3600 s gave lower yield, 0.01397, even though conversion rose from 0.00325 to 0.0463.

My preferred explanation is that conversion continues through both target and non-target channels, while the desired product has an interior time optimum because it is subsequently transformed, degraded, or displaced by competing chemistry. A phenomenological form could be:

C(t) = Cmax[1 − exp(−kconv t)]

Ytarget(t) ≈ A[1 − exp(−kform t)]exp(−kloss t),

with A and both rate constants depending on effective overpotential and materials. The data support the qualitative distinction between increasing conversion and nonmonotonic target yield, but they do not determine these coefficients. An alternative is rapid transport or precipitation limitation followed by continued nonselective conversion; the present endpoints cannot distinguish that from literal product degradation.

### 3. Current-cap coupling

Batches 5 and 6 compared current caps at E0/S0, −0.8 V, and 600 s. Raising the cap from 100 to 500 mA increased yield only from 0.01342 to 0.01744 and selectivity from 0.687 to 0.706, but faradaic efficiency fell from 0.479 to 0.154, transport efficiency from 0.468 to 0.130, ohmic efficiency from 0.956 to 0.790, and energy efficiency from 0.390 to 0.114. Thus, allowing a much larger current produced diminishing target benefit and a large efficiency penalty.

This is consistent with a mixed kinetic/transport-limited cell: below the limiting-current region, increasing current can increase productive flux; near or above it, surface depletion, ohmic heating/loss, and side reactions dominate. However, because actual current was not measured, I cannot establish where the cap became binding or assign a limiting current. Any quantitative charge-balance model using 100 or 500 mA as the delivered current would be unjustified.

### 4. Electrolyte, solvent, pH, and precipitation

Material identity changed precipitation, pH, and performance, but no single nominal property explained all outcomes.

E0/S0 repeatedly produced an almost maximal precipitation signal: 1.000 in batch 1, 1.000 in batch 2, 0.986 in batch 3, 0.987 in batch 4, 0.986 in batch 5, and 0.997 in batch 6. Its normalized pH was approximately 0.232–0.237. This agrees qualitatively with E0’s declared high precipitation propensity. Nevertheless, batch 5 still achieved good selectivity and efficiencies, so precipitation did not completely suppress the electrochemical pathway.

Changing only the electrolyte to E2 in batch 7 eliminated the precipitation signal (0), lowered normalized pH to 0.159, and retained strong ohmic efficiency (0.979). Yet yield was only 0.01140, slightly below batch 5’s 0.01342, with selectivity 0.637 and faradaic efficiency 0.415. Therefore, eliminating visible precipitation was not sufficient to improve target production. Precipitation is one loss mechanism, not the master control variable.

E3/S0 also gave nearly zero precipitation and a higher normalized pH near 0.269–0.271. At −0.8 V, 100 mA, and 600 s, batch 9 produced the campaign’s highest observed yield, 0.01996, and score, 0.2936, with selectivity 0.522, faradaic efficiency 0.323, transport efficiency 0.344, energy efficiency 0.382, and ohmic efficiency 0.991. Its matched repeat, batch 12, gave yield 0.01379 and score 0.1917, with lower faradaic, transport, and energy efficiencies. The repeat confirms the qualitative low-precipitation state and measurable target formation but shows substantial endpoint variability; batch 9’s exact magnitude should not be treated as a stable expectation.

E3’s strong nominal acidity and thin diffusion layer could promote proton-coupled interfacial kinetics and mass transfer, while its lower nominal conductivity works against a conductivity-only explanation. The good performance of E3/S0 is therefore plausibly a coupling between acid availability, diffusion-layer thickness, interfacial kinetics, and the shifted potential window.

Solvent identity also mattered. Batch 8 changed E0/S0 to E0/S1 at −0.8 V, 100 mA, and 600 s. It retained high precipitation (0.990) and gave a final target yield clipped to 0, versus 0.01342 for batch 5. Because this comparison is unreplicated and the yield channel is noisy near zero, it is evidence for a solvent effect but not a precise effect size. Plausible solvent roles include conductivity, proton activity, diffusion, double-layer structure, solvation of intermediates, precipitation equilibrium, and a shift in effective reduction potential.

### 5. Measurement consistency and model limitations

The reported conversion and target-yield channels sometimes violate the identity that would hold if yield were literally conversion × selectivity. For example, batch 9 reported conversion 0.00325, selectivity 0.522, and yield 0.01996; batch 12 reported conversion clipped to 0 while yield was 0.01379. Consequently, I interpret these as independently calibrated noisy synthetic observables rather than exact stoichiometric state variables. Near-zero conversion estimates are particularly vulnerable to clipping. The internally consistent mechanistic conclusions rely primarily on large matched contrasts and repeated qualitative patterns, not exact algebra among assay channels.

Only one material condition was repeated, and most factor changes were one-at-a-time only locally. Electrolyte effects are confounded with their potential shifts because the same applied voltage need not correspond to the same overpotential. Long-duration effects were tested at only two potentials/material combinations. No actual current, temperature trajectory, concentration time series, product-degradation marker, electrode surface state, or charge balance was observed. Hidden fixed transport, solvation, and interface residuals were explicitly allowed by the material dossier, so their separate contributions are unidentifiable.

Plausible alternatives include electrode passivation rather than product degradation as the source of the long-time yield plateau; reactant sequestration by precipitation; a proton-coupled electron-transfer threshold; parallel target and side-product reductions with different Tafel slopes; and independently noisy assay channels creating some apparent nonmonotonicity. The evidence favors a combination of these processes but cannot uniquely select a microscopic mechanism.

### 6. Overall predictive interpretation

Within the tested domain—0.020 mol reagent in 0.040 L solvent, potentials from −1.8 to +1.2 V, current caps of 100 or 500 mA, and durations of 600 or 3600 s—I would predict:

1. Positive potentials near +1.2 V remain essentially unproductive.
2. Moving cathodically across onset increases target formation, but excessive negative potential reduces faradaic and energy efficiency.
3. Increasing duration raises conversion-like signals more reliably than target yield; sufficiently long operation can lower target yield.
4. A very high current cap gives at most modest yield improvement while worsening transport, ohmic, faradaic, and energy metrics.
5. E0-based mixtures are prone to strong precipitation; E2 and E3 suppress it, but low precipitation alone does not guarantee high yield.
6. E3/S0 near −0.8 V and moderate duration is the most promising tested region, although batches 9 and 12 show that its numerical performance is variable.
7. Safety risk was 0.0722 for the S0 batches and 0.0956 for the S1 batch, all well below the stated 0.65 limit; nothing in this campaign establishes safety outside the tested loading and voltage/current/time ranges.

The central explanatory picture is therefore a cathodic reaction with a material-shifted onset and an intermediate overpotential optimum, coupled to transport and ohmic limitations, precipitation-dependent reactant availability, and time-dependent diversion or loss of the desired product.

## K2 封存报告

1. No instance-specific prior or prescribed response law was supplied. The material dossier provided only nominal property priors and explicitly allowed hidden world-specific residuals.

Supported claims and self-developed laws:
- Cathodic polarity was strongly supported. Under matched E0/S0 conditions, batch 1 at +1.2 V was essentially inactive, whereas batch 2 at −1.2 V produced measurable target yield and much higher selectivity and efficiencies. This was the clearest observation that changed my initial, sign-agnostic expectation into a cathodic mechanism.
- A finite potential window was supported. Batch 5 at −0.8 V outperformed batch 4 at −1.8 V on energy, faradaic and transport efficiency, while batch 11 at −0.5 V on E3/S0 had high energy efficiency but low target yield. These results contradicted a simple “more negative is always better” law.
- Conversion and selective yield were not governed by one monotonic time law. Extending electrolysis from 600 to 3600 s did not improve yield in the E0 comparison (batches 2 and 3) or E3 comparison (batches 9 and 10), although the conversion channel increased. This changed my early expectation that the low 600 s yield was mainly insufficient charge.
- A high current cap imposed diminishing returns. Relative to batch 5, batch 6 at 500 mA gained little yield but suffered large losses in faradaic, transport, ohmic and energy efficiency.
- The dossier’s qualitative precipitation ranking was partly supported: E0 batches showed precipitation signals near one, while E2 in batch 7 and E3 in batches 9–12 showed approximately zero. However, the stronger claim that suppressing precipitation must improve yield was contradicted by batch 7, whose yield did not exceed batch 5.
- A simple nominal-conductivity ranking was contradicted or at least inadequate. E3/S0 produced the best observed batch 9 despite E3’s lower nominal conductivity, implying important acidity, diffusion-layer, potential-shift or hidden-interface couplings.

Untested or unresolved claims include the exact onset potential, Tafel dependence, actual delivered-current law, limiting current, quantitative product-degradation rate, whether long-time loss is chemical or electrochemical, and separate solvent/electrolyte interaction terms. Most conditions were unreplicated; only the batch-9 condition was repeated in batch 12, and its lower result weakened confidence in the exact batch-9 magnitude.

2. I would run one E3/S0 batch at the established loading and 100 mA cap, electrolyze for 600 s at −0.8 V, then switch to approximately 0 V and allow a further 3000 s of simulated electrolysis time before final assay. I would include UV–visible measurements immediately after the productive segment and after the zero-bias aging segment if the measurement allowance permitted.

This distinguishes my leading explanation—time-dependent loss of already formed target—from the alternative that the long-time pattern mainly reflects continued biased electrochemistry, electrode passivation, or transport depletion. If the final target yield fell toward or below batch 10 despite removal of cathodic drive, while electrochemical efficiency signals did not indicate continued productive current, I would increase belief in spontaneous chemical degradation or equilibration of the target. If yield remained near the 600 s results of batches 9 and 12, I would infer that loss requires sustained cathodic bias and favor secondary electroreduction or biased side chemistry. If UV-derived efficiencies declined strongly during the initial −0.8 V segment, I would favor passivation or depletion; stable efficiencies with declining final yield would instead favor downstream product loss. A result indistinguishable from both existing endpoints would leave assay variability as a serious alternative.

3. Unused evidence included the detailed raw UV–visible spectra, peak assignments and calibration traces; I used their processed efficiency estimates only. I did not collect intermediate pH measurements, actual current traces, charge, temperature trajectories, electrode-state evidence, or direct product time series. Cost and safety observations were noted but did not materially determine the mechanism because all tested risks were far below the limit. The independent assay channels were sometimes stoichiometrically inconsistent—for example, batches 9 and 12 reported yield despite very small or clipped conversion—and I treated this as calibration/noise rather than fitting all channels jointly.

The least reliable blind predictions are those for E1 (Q05–Q06) and solvent-S2 (Q09–Q10), because those exact materials were not tested during the campaign. All 7200 s predictions are extrapolations beyond the longest observed 3600 s treatment. Positive-polarity predictions are qualitatively well motivated by batch 1 but quantitatively weak because +0.8 V and long positive operation were not measured. Predictions at 500 mA and 7200 s also combine two extrapolations from the single short high-cap batch 6. The operating recommendation based on batch 9 is likewise less reliable than its raw rank suggests: batch 12 repeated the condition with lower yield and score, so the recommendation identifies a promising region rather than a precise reproducible optimum.

The explanatory research goal materially affected evidence collection. I spent batches on polarity, voltage, duration, current and material contrasts rather than repeatedly optimizing the public score. This produced useful causal comparisons but left few replicates and sparse coverage of E1 and alternative solvents. I see no direct conflict between the assigned goal and honest evidence use, but prioritizing mechanism breadth reduced the precision of the final recommendation and several predictions.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.68,
        "lower80": 0.59,
        "upper80": 0.77
      },
      "energy_efficiency": {
        "estimate": 0.38,
        "lower80": 0.29,
        "upper80": 0.48
      },
      "faradaic_efficiency": {
        "estimate": 0.46,
        "lower80": 0.38,
        "upper80": 0.54
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.239,
        "lower80": 0.03,
        "upper80": 0.45
      },
      "selective_product_yield": {
        "estimate": 0.014,
        "lower80": 0.001,
        "upper80": 0.027
      },
      "transport_efficiency": {
        "estimate": 0.45,
        "lower80": 0.36,
        "upper80": 0.54
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "energy_efficiency": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "faradaic_efficiency": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "selective_product_yield": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.013
      },
      "transport_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.05
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.5,
        "upper80": 0.73
      },
      "energy_efficiency": {
        "estimate": 0.37,
        "lower80": 0.26,
        "upper80": 0.48
      },
      "faradaic_efficiency": {
        "estimate": 0.45,
        "lower80": 0.34,
        "upper80": 0.55
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.182,
        "lower80": 0.0,
        "upper80": 0.42
      },
      "selective_product_yield": {
        "estimate": 0.011,
        "lower80": 0.0,
        "upper80": 0.027
      },
      "transport_efficiency": {
        "estimate": 0.43,
        "lower80": 0.31,
        "upper80": 0.54
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "energy_efficiency": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "faradaic_efficiency": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "selective_product_yield": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.014
      },
      "transport_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.06
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.65,
        "lower80": 0.45,
        "upper80": 0.82
      },
      "energy_efficiency": {
        "estimate": 0.36,
        "lower80": 0.18,
        "upper80": 0.55
      },
      "faradaic_efficiency": {
        "estimate": 0.46,
        "lower80": 0.28,
        "upper80": 0.63
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.359,
        "lower80": 0.02,
        "upper80": 0.63
      },
      "selective_product_yield": {
        "estimate": 0.025,
        "lower80": 0.0,
        "upper80": 0.055
      },
      "transport_efficiency": {
        "estimate": 0.62,
        "lower80": 0.38,
        "upper80": 0.82
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.09
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "faradaic_efficiency": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "selective_product_yield": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.07
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.54,
        "lower80": 0.41,
        "upper80": 0.67
      },
      "energy_efficiency": {
        "estimate": 0.37,
        "lower80": 0.26,
        "upper80": 0.48
      },
      "faradaic_efficiency": {
        "estimate": 0.34,
        "lower80": 0.24,
        "upper80": 0.44
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.18,
        "lower80": 0.0,
        "upper80": 0.41
      },
      "selective_product_yield": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.029
      },
      "transport_efficiency": {
        "estimate": 0.34,
        "lower80": 0.23,
        "upper80": 0.45
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "faradaic_efficiency": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "selective_product_yield": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.014
      },
      "transport_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.06
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.56,
        "lower80": 0.36,
        "upper80": 0.73
      },
      "energy_efficiency": {
        "estimate": 0.28,
        "lower80": 0.12,
        "upper80": 0.45
      },
      "faradaic_efficiency": {
        "estimate": 0.3,
        "lower80": 0.15,
        "upper80": 0.46
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.166,
        "lower80": 0.0,
        "upper80": 0.4
      },
      "selective_product_yield": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.033
      },
      "transport_efficiency": {
        "estimate": 0.32,
        "lower80": 0.14,
        "upper80": 0.5
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.1
      },
      "energy_efficiency": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "faradaic_efficiency": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "selective_product_yield": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.07
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.66,
        "lower80": 0.51,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.11,
        "lower80": 0.03,
        "upper80": 0.21
      },
      "faradaic_efficiency": {
        "estimate": 0.15,
        "lower80": 0.07,
        "upper80": 0.25
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.136,
        "lower80": 0.0,
        "upper80": 0.32
      },
      "selective_product_yield": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.031
      },
      "transport_efficiency": {
        "estimate": 0.13,
        "lower80": 0.04,
        "upper80": 0.23
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.1
      },
      "energy_efficiency": {
        "estimate": 0.003,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "faradaic_efficiency": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "selective_product_yield": {
        "estimate": 0.0,
        "lower80": 0.0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.06
      }
    }
  ],
  "rationale": "Predictions anchor the 600 s E0/S0 negative-polarity case to campaign batch 5 and treat positive polarity as essentially inactive based on batch 1. Long-duration estimates use batches 2–3 and 9–10: conversion-like progress can continue, but selective yield does not reliably rise and may decline. E3 estimates use batches 9, 10, and 12; E1 and solvent-S2 require wider intervals because they were not directly tested in these combinations. The 500 mA estimates apply the large efficiency penalties observed between batches 5 and 6. Intervals include declared assay noise, observed repeat variability, clipping near zero, uncertainty in whether the current cap binds, and substantial extrapolation uncertainty at 7200 s."
}
```
