# repeat-02/EC-W02-B12-discovery-E-Opaque

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-02\EC-W02-B12-discovery-E-Opaque\participant\discovery-E-Opaque

## 同期笔记

### v1 · 公开事件 0

# Electrochemical campaign hypotheses

## Pre-experiment expectations

**H1 [tentative].** At fixed loading (0.020 mol reagent in 0.050 L solvent), conversion should rise with electrolysis time and current cap before saturating, while efficiency/selectivity may fall at excessive potential or duration because of side reactions.

**H2 [tentative].** Potential sign and magnitude, solvent identity, and electrolyte identity may independently control charge delivery, transport, and selectivity. I will use broad contrasts first, then targeted time/current tests and replication.

Testable consequences: opposite potential signs should produce clearly distinct final-assay patterns if polarity is mechanistically directional; time series at a productive setting should separate conversion-limited from selectivity-limited behavior. Claims will remain unresolved where single comparisons confound factors or differences are comparable to declared instrument noise.

### v2 · 公开事件 56

# Electrochemical campaign hypotheses

## Pre-experiment expectations

**H1 [revised: supported for time, rejected for cap-driven conversion in tested range].** At S0/E0 and +1 V, extending 600 to 3600 to 14400 s increased final conversion approximately 0.023 → 0.091 → 0.303 (events runner-operation-0007, -0035, -0056). However increasing the current cap from 100 to 500 mA at 3600 s left conversion essentially unchanged (~0.091 vs ~0.090) while sharply lowering faradaic, transport, and energy efficiencies (events -0035, -0042). Thus delivered reaction rate appears potential/transport-limited rather than cap-limited by 100 mA, and the reported efficiencies penalize excessive configured cap. Prediction: below a lower cap conversion should eventually become cap-limited; above that knee conversion should plateau while efficiency falls.

**H2 [supported in S0/E0 scope].** Polarity affects selectivity more than conversion at 3600 s: +1 and -1 V at 500 mA gave similar conversion (~0.090 vs ~0.098) but selectivity ~0.899 vs ~0.577 and yield ~0.089 vs ~0.058 (events -0042, -0049). At 600 s, ±1 V showed the same selectivity ordering, although low conversion and assay noise make yield comparisons weak (events -0007, -0014). ±2 V was poor in the short trials (events -0021, -0028), consistent with a moderate-magnitude window.

**H3 [tentative].** For +1 V/S0/E0, selective yield is primarily conversion × selectivity; duration raises yield but causes diminishing conversion gain, whereas a high current cap reduces efficiency without improving throughput. Material effects remain untested. Next: vary solvent and electrolyte at fixed +1 V, 100 mA, 3600 s, then replicate or test a lower cap if remaining design permits.

### v3 · 公开事件 84

# Electrochemical campaign hypotheses

## Final source-stage account

**H1 [supported in tested S0/E0 scope].** At +1 V and 100 mA cap, extending electrolysis from 600 to 3600 to 14400 s increased conversion approximately 0.023 → 0.091 → 0.303 (events runner-operation-0007, -0035, -0056), with diminishing conversion per unit time. Selectivity stayed near 0.89. A saturating or progressively transport-limited time response is more plausible than a constant-rate model over the full interval.

**H2 [supported in tested S0/E0 scope].** Potential polarity primarily changes selectivity: at 3600 s/500 mA, +1 and -1 V gave similar conversion (~0.090 vs ~0.098) but selectivity ~0.899 vs ~0.577 (events -0042, -0049). Short ±1 V data agree directionally (events -0007, -0014). Short ±2 V trials were poor (events -0021, -0028), supporting a moderate-magnitude operating window, though magnitude and low-conversion noise are entangled.

**H3 [supported for cap comparison at +1 V/S0/E0].** Raising the current cap 100→500 mA at 3600 s did not raise conversion (~0.091 vs ~0.090) but sharply lowered faradaic, transport, and energy efficiencies (events -0035, -0042). The cap is therefore not guaranteed delivered current; reaction rate is already potential/transport limited by a cap of 100 mA, while excess cap is inefficient. A lower-cap knee remains unresolved.

**H4 [material effects partly resolved].** Relative to S0/E0 at +1 V, 100 mA, 3600 s (event -0035), S1/E0 reduced conversion and selectivity modestly and lowered faradaic/transport efficiencies (event -0063), suggesting S0 is preferable among the isolated solvent comparison. S0/E1 increased observed conversion, selectivity, and most efficiencies, giving the best balanced score, though selective yield was noisily lower than the S0/E0 replicate (event -0070). S2/E2 and S3/E3 were progressively worse in conversion and charge/transport efficiency (events -0077, -0084), but solvent and electrolyte contributions are confounded for those pairs. Precipitation signal varied strongly with material pair and should be treated as a material-linked indicator, not a demonstrated cause of yield.

**Working predictive model.** At the fixed loading used here (0.020 mol in 0.050 L), conversion depends on time through a sublinear/saturating function whose scale depends on potential magnitude and material transport; potential sign multiplies selectivity; and efficiency declines when the configured current cap greatly exceeds the delivered-current regime. Selective yield is broadly coupled to conversion × selectivity, but independent assay noise is conspicuous at low conversion. Extrapolation to untested solvent/electrolyte combinations or caps below 100 mA remains uncertain.

**Recommendation decision.** Choose batch 10 (S0/E1, +1 V, 100 mA, 3600 s): it had the highest balanced public score and strong selectivity/efficiency. This is a balanced operating choice, not proof that it maximizes true yield; batch 5 (S0/E0 under the same electrical conditions) is a close mechanistic comparator and had slightly higher observed selective yield.

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
    "electrochemical_conversion": 0.022787874564528465,
    "electrochemical_selectivity": 0.8980063199996948,
    "energy_efficiency": 0.8702253699302673,
    "faradaic_efficiency": 0.9748222827911377,
    "ohmic_efficiency": 0.9653005003929138,
    "pH_normalized": 0.22897005081176758,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.9461185336112976
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
    "electrochemical_selectivity": 0.5760180354118347,
    "energy_efficiency": 0.25159168243408203,
    "faradaic_efficiency": 0.38621339201927185,
    "ohmic_efficiency": 0.9741383194923401,
    "pH_normalized": 0.22627469897270203,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.18159562349319458,
    "selective_product_yield": 0.012379591353237629,
    "transport_efficiency": 0.4124701917171478
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
      "potential_V": 2
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
    "cost": 0.28547999262809753,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.0,
    "ohmic_efficiency": 0.9736917614936829,
    "pH_normalized": 0.22698970139026642,
    "precipitation_signal": 0.9871450662612915,
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
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -2
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
    "cost": 0.28547999262809753,
    "electrochemical_conversion": 4.6335102524608374e-05,
    "electrochemical_selectivity": 0.4232766330242157,
    "energy_efficiency": 0.028069986030459404,
    "faradaic_efficiency": 0.27460572123527527,
    "ohmic_efficiency": 0.985849916934967,
    "pH_normalized": 0.22629910707473755,
    "precipitation_signal": 0.987893283367157,
    "safety_risk": 0.05933958664536476,
    "score": 0.02578638307750225,
    "selective_product_yield": 0.002520720474421978,
    "transport_efficiency": 0.24311818182468414
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
    "cost": 0.28644001483917236,
    "electrochemical_conversion": 0.09129364043474197,
    "electrochemical_selectivity": 0.8940926194190979,
    "energy_efficiency": 0.8370735049247742,
    "faradaic_efficiency": 0.9527704119682312,
    "ohmic_efficiency": 0.9725042581558228,
    "pH_normalized": 0.23125991225242615,
    "precipitation_signal": 0.9872196912765503,
    "safety_risk": 0.05933958664536476,
    "score": 0.5810955762863159,
    "selective_product_yield": 0.08644126355648041,
    "transport_efficiency": 0.9422609806060791
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
    "electrochemical_conversion": 0.08999577909708023,
    "electrochemical_selectivity": 0.899038553237915,
    "energy_efficiency": 0.1988275796175003,
    "faradaic_efficiency": 0.21240518987178802,
    "ohmic_efficiency": 0.8721224069595337,
    "pH_normalized": 0.2279839664697647,
    "precipitation_signal": 0.9978500008583069,
    "safety_risk": 0.05933958664536476,
    "score": 0.3143921494483948,
    "selective_product_yield": 0.08894017338752747,
    "transport_efficiency": 0.187721848487854
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
      "volume_L": 0.05
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1
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
    "electrochemical_conversion": 0.0981978252530098,
    "electrochemical_selectivity": 0.5769981741905212,
    "energy_efficiency": 0.13217756152153015,
    "faradaic_efficiency": 0.19050666689872742,
    "ohmic_efficiency": 0.9036839604377747,
    "pH_normalized": 0.22699855268001556,
    "precipitation_signal": 0.9828920960426331,
    "safety_risk": 0.05933958664536476,
    "score": 0.24819299578666687,
    "selective_product_yield": 0.05816878378391266,
    "transport_efficiency": 0.1939070224761963
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
      "volume_L": 0.05
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 0,
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
    "cost": 0.31380000710487366,
    "electrochemical_conversion": 0.3027196526527405,
    "electrochemical_selectivity": 0.8893049359321594,
    "energy_efficiency": 0.17419618368148804,
    "faradaic_efficiency": 0.17300400137901306,
    "ohmic_efficiency": 0.888979971408844,
    "pH_normalized": 0.2253010869026184,
    "precipitation_signal": 0.9957649111747742,
    "safety_risk": 0.05933958664536476,
    "score": 0.3746858537197113,
    "selective_product_yield": 0.2545299530029297,
    "transport_efficiency": 0.16650864481925964
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
    "cost": 0.30643999576568604,
    "electrochemical_conversion": 0.0751623883843422,
    "electrochemical_selectivity": 0.8386805653572083,
    "energy_efficiency": 0.8521074056625366,
    "faradaic_efficiency": 0.8175172209739685,
    "ohmic_efficiency": 0.9976380467414856,
    "pH_normalized": 0.2323479950428009,
    "precipitation_signal": 0.9991756081581116,
    "safety_risk": 0.08273958414793015,
    "score": 0.5476515293121338,
    "selective_product_yield": 0.08256380259990692,
    "transport_efficiency": 0.8383485078811646
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
    "cost": 0.28644001483917236,
    "electrochemical_conversion": 0.09976132959127426,
    "electrochemical_selectivity": 0.9619195461273193,
    "energy_efficiency": 0.9281471371650696,
    "faradaic_efficiency": 0.9137532114982605,
    "ohmic_efficiency": 0.958005964756012,
    "pH_normalized": 0.19996103644371033,
    "precipitation_signal": 0.8492700457572937,
    "safety_risk": 0.05933958664536476,
    "score": 0.5944273471832275,
    "selective_product_yield": 0.07713358104228973,
    "transport_efficiency": 0.9151028394699097
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
      "solvent": 2,
      "volume_L": 0.05
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
    "cost": 0.3384400010108948,
    "electrochemical_conversion": 0.07788469642400742,
    "electrochemical_selectivity": 0.8329150080680847,
    "energy_efficiency": 0.7793521285057068,
    "faradaic_efficiency": 0.692959189414978,
    "ohmic_efficiency": 0.9133688807487488,
    "pH_normalized": 0.17338931560516357,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.10073958337306976,
    "score": 0.49261218309402466,
    "selective_product_yield": 0.05581707879900932,
    "transport_efficiency": 0.7001391649246216
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
      "solvent": 3,
      "volume_L": 0.05
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
    "cost": 0.3184399902820587,
    "electrochemical_conversion": 0.02725277654826641,
    "electrochemical_selectivity": 0.8178709149360657,
    "energy_efficiency": 0.7461369037628174,
    "faradaic_efficiency": 0.43395760655403137,
    "ohmic_efficiency": 0.9912338852882385,
    "pH_normalized": 0.2796901762485504,
    "precipitation_signal": 0.0,
    "safety_risk": 0.11333958804607391,
    "score": 0.4284745752811432,
    "selective_product_yield": 0.04752078279852867,
    "transport_efficiency": 0.4551825523376465
  }
}
```

## K1 封存报告

Mechanistic report

1. Experimental domain and variables

All 12 batches used 0.020 mol of anonymous limiting reagent in 0.050 L total solvent. The manipulated variables were solvent identity S0–S3, electrolyte identity E0–E3, potential (-2 to +2 V in the tested set), current limit (100 or 500 mA), and electrolysis time (600, 3600, or 14,400 s). Because the materials are anonymous benchmark formulations, the report concerns functional roles rather than molecular identities.

I interpret the system as having at least four coupled stages:

(1) charge delivery through the solvent/electrolyte medium;
(2) potential-dependent conversion of reactant into both target and non-target products;
(3) polarity-dependent partitioning between those product channels;
(4) material-dependent recovery or observability of the target in the final assay.

The current setting appears to behave as a ceiling rather than a guarantee of delivered productive current. Transport, solution resistance, interfacial kinetics, and parasitic charge consumption can therefore decouple configured current from chemical conversion.

2. Empirical electrical response

Potential polarity affected selectivity much more strongly than conversion. At S0/E0, 3600 s, and a 500 mA limit, batch 6 at +1 V gave conversion 0.0900 and selectivity 0.8990, whereas batch 7 at -1 V gave conversion 0.0982 but selectivity only 0.5770. Their selective-product yields were 0.0889 and 0.0582, respectively. Thus either polarity could consume substrate under those conditions, but positive polarity favored the target-producing branch.

The 600 s tests support the same directional asymmetry, although their very small conversions make quantitative interpretation weak. Batch 1 (+1 V, 100 mA) had conversion 0.0228 and selectivity 0.8980. Batch 2 (-1 V, 100 mA) reported conversion clipped at zero, selectivity 0.5760, and yield 0.0124. The apparent nonzero yield with zero processed conversion demonstrates that independently processed low-level channels should not be forced into exact mass-action identities near their detection/noise floor.

Increasing potential magnitude from 1 to 2 V did not improve the short experiment. Batch 3 at +2 V gave processed conversion, selectivity, yield, faradaic efficiency, and transport efficiency at or near zero. Batch 4 at -2 V gave conversion 0.000046, selectivity 0.4233, yield 0.00252, faradaic efficiency 0.2746, and transport efficiency 0.2431. These observations suggest a moderate-potential productive window around +1 V. A plausible process is that excessive magnitude drives solvent/electrolyte reactions, passivation, or another unproductive interfacial state. That explanation is conjectural: the experiment observed performance loss but did not identify a chemical side product or electrode state.

A minimal polarity model would be

C = F(|V|, t, medium, I_limit),
S = G(sign(V), |V|, medium),

where C is conversion and S is target selectivity. In the tested S0/E0 region, changing sign at |V| = 1 V had little effect on C at 3600 s but changed S by about 0.32. This argues against a model in which negative polarity merely slows the same target reaction. It instead suggests parallel polarity-sensitive product channels.

3. Time dependence

At +1 V in S0/E0, conversion rose with duration:

• batch 1: 600 s, 100 mA limit, C = 0.0228;
• batch 5: 3600 s, 100 mA limit, C = 0.0913;
• batch 8: 14,400 s, 500 mA limit, C = 0.3027.

Selectivity remained comparatively stable: 0.8980, 0.8941, and 0.8893. Time therefore mainly accumulated conversion rather than changing the product branching ratio over this interval. Batch 8 reached the largest observed yield, 0.2545, but had poor electrical efficiencies: faradaic 0.1730, transport 0.1665, energy 0.1742, and ohmic 0.8890.

A useful descriptive interpolation for conversion in this narrow region is approximately

C(t) ≈ 0.091 (t/3600 s)^0.8–0.9,

for 600–14,400 s, with eventual clipping or saturation required outside that range. Equivalently, a mechanistic model might use C = C∞[1-exp(-k_eff t)], with k_eff controlled by potential and medium. The campaign does not distinguish a true first-order saturation law from a sublinear charge-transport law. Moreover, the longest run used a different current limit, so its inclusion assumes the conclusion below that limits above 100 mA do not materially accelerate conversion at +1 V.

4. Current-limit and efficiency coupling

Batches 5 and 6 provide the clean current-limit comparison at S0/E0, +1 V, and 3600 s. Raising the limit from 100 to 500 mA left conversion essentially unchanged (0.0913 versus 0.0900) and selectivity unchanged within assay variation (0.8941 versus 0.8990). It nevertheless reduced final faradaic efficiency from 0.9528 to 0.2124, transport efficiency from 0.9423 to 0.1877, energy efficiency from 0.8371 to 0.1988, and ohmic efficiency from 0.9725 to 0.8721. The corresponding scores fell from 0.5811 to 0.3144.

My explanation is that productive delivery is already limited by the electrode/medium system at or below 100 mA. Increasing the configured ceiling contributes mostly nonproductive current, polarization loss, or an efficiency-denominator penalty rather than additional substrate conversion. One possible representation is

I_productive = min(I_limit, I_kinetic(V), I_transport(medium)),
I_total = I_productive + I_parasitic(V, I_limit, medium),
FE ≈ I_productive/I_total.

This accounts for constant conversion together with falling faradaic and transport efficiencies. It predicts a lower-current knee below which conversion will become current-limited, but no experiment below 100 mA was performed, so the knee is unidentifiable.

The UV-vis measurements support the large efficiency contrasts rather than relying only on final assays. For example, batch 5 UV-vis estimated faradaic/transport efficiencies of 0.9637/0.9401, whereas batch 6 gave 0.1992/0.1742. Exact UV-vis and final-assay values differed, as expected from their distinct calibrations and noise.

5. Material effects

Batch 5, S0/E0 at +1 V, 100 mA, 3600 s, is the main reference: conversion 0.0913, selectivity 0.8941, yield 0.0864, faradaic efficiency 0.9528, transport efficiency 0.9423, and score 0.5811.

Changing only solvent from S0 to S1 in batch 9 reduced conversion to 0.0752, selectivity to 0.8387, faradaic efficiency to 0.8175, and transport efficiency to 0.8383. Energy efficiency remained high at 0.8521, and yield was 0.0826. This isolated comparison supports S0 over S1 for both target branching and charge transport, although the yield difference itself was small.

Changing only electrolyte from E0 to E1 while retaining S0 in batch 10 increased conversion to 0.0998 and selectivity to 0.9619. Its energy, faradaic, transport, and ohmic efficiencies were 0.9281, 0.9138, 0.9151, and 0.9580. It achieved the highest balanced score, 0.5944, and was therefore the sealed recommendation. Its measured yield, 0.0771, was lower than simple conversion × selectivity would suggest and lower than batch 5's 0.0864. Consequently E1 is supported as the best balanced electrolyte observed, not conclusively as the maximum-yield electrolyte.

Batches 11 and 12 tested paired changes, so solvent and electrolyte effects cannot be separated. Batch 11 (S2/E2) gave conversion 0.0779, selectivity 0.8329, yield 0.0558, faradaic efficiency 0.6930, transport efficiency 0.7001, and score 0.4926. Batch 12 (S3/E3) gave conversion 0.0273, selectivity 0.8179, yield 0.0475, faradaic efficiency 0.4340, transport efficiency 0.4552, and score 0.4285. These pairs were progressively poorer in charge utilization and conversion, but the data cannot say whether S2/S3, E2/E3, or their interactions caused the losses.

Material identity also strongly affected pH-normalized and precipitation channels. At the common +1 V/100 mA/3600 s setting, batch 5 S0/E0 had pH-normalized 0.2313 and precipitation signal 0.9872; batch 10 S0/E1 had 0.2000 and 0.8493; batch 11 S2/E2 had 0.1734 and 0.00524; and batch 12 S3/E3 had 0.2797 and zero precipitation signal. Precipitation cannot be assigned a beneficial or harmful causal role: high-performing batches 5 and 10 both had high precipitation signals, but the design did not independently manipulate precipitation. It may instead report solubility, ionic strength, or product partitioning associated with each medium.

6. Yield formation and recovery

Selective-product yield was broadly related to conversion and selectivity, but it was not exactly their product. A more defensible equation is

Y_observed = C × S × R(medium, time, phase state) + assay error,

where R represents product survival, recovery, phase accessibility, or another unobserved mapping between formed target and measured target. At moderate conversion, C × S is close to yield in several S0/E0 batches: batch 5 gives about 0.0816 versus observed 0.0864; batch 6 about 0.0809 versus 0.0889; batch 7 about 0.0567 versus 0.0582; and batch 8 about 0.269 versus 0.255. Material-screen batches show larger deviations: batch 10 gives C × S near 0.096 versus yield 0.0771, while batch 9 gives about 0.063 versus yield 0.0826. These discrepancies are too structured to assume exact Y = C × S, but there are too few replicates to distinguish medium-dependent recovery from random assay/process variation. At very low conversion, independent channel noise and clipping dominate, as illustrated by batches 1–4 and 12.

7. Overall proposed mechanism

The limiting reagent reaches an electrode where a moderate positive potential opens a target-favored electron-transfer pathway. A competing pathway remains available at negative polarity and consumes a similar fraction of reagent but produces substantially less target. Very large positive or negative potentials favor unproductive charge transfer, passivation, or degradation. The solvent/electrolyte combination sets conductivity, interfacial kinetics, transport capacity, acid/base state, and phase behavior. These medium properties determine the maximum productive current and also influence selectivity and recovery. Reaction progress accumulates sublinearly with time, while high configured current above the medium's productive capacity is diverted into losses rather than accelerating conversion.

In pseudocode:

transport_cap = T(solvent, electrolyte, phase_state)
kinetic_cap = K(abs(potential), solvent, electrolyte)
productive_current = min(current_limit, transport_cap, kinetic_cap)
side_current = H(abs(potential), current_limit, medium)
conversion = progress(productive_current, time)
selectivity = branch_fraction(sign(potential), abs(potential), medium)
formed_target = conversion * selectivity
observed_yield = formed_target * recovery(medium, phase_state, time) + measurement_error

The E1/S0 medium appears to improve target branching and balanced electrical performance relative to E0/S0, while S0/E0 provides a slightly higher observed yield in the matched 3600 s assays. Longer operation raises total target production but sacrifices throughput-normalized electrical efficiency, especially with the unnecessary 500 mA ceiling.

8. Scope, unresolved parameters, and alternatives

This account is supported only at one reagent concentration, one liquid volume, four anonymous solvents/electrolytes, and a sparse electrical design. Electrode area, true current trace, resistance, temperature trajectory, product identities, electron stoichiometry, and actual species concentrations were not measured publicly. Therefore no absolute kinetic constant, Faraday-law electron number, or molecular mechanism can be identified.

Solvent and electrolyte effects are independently identifiable only for S1 versus S0 at E0 and E1 versus E0 in S0. Results for S2/E2 and S3/E3 are confounded and may include strong interactions. There were no exact batch replicates, so process variation cannot be cleanly separated from factor effects. Final pH and precipitation were observed but not manipulated, making causal claims inappropriate.

Plausible alternatives include: (a) the current-limit dependence may partly arise from how benchmark efficiency metrics are normalized rather than actual parasitic chemistry; (b) the apparent time sublinearity may reflect charge delivery, progressive depletion, passivation, or simply a nonlinear instrument mapping; (c) polarity could change product observability rather than intrinsic branching, although the consistent selectivity contrast makes a genuine branch change more plausible; and (d) discrepancies between conversion × selectivity and yield could be independent assay noise rather than recovery chemistry.

Within these limits, the most robust conclusions are that +1 V is preferable to -1 V for selectivity, ±2 V is poor in the tested short trials, increasing the current ceiling from 100 to 500 mA does not accelerate conversion at +1 V but severely reduces reported efficiencies, time increases conversion while leaving selectivity near 0.89 in S0/E0, and medium identity changes transport, charge efficiency, selectivity, pH, and phase-related signals. Batch 10 is the best observed balanced operating point, whereas batch 8 demonstrates how longer time can maximize observed product amount at substantially poorer electrical efficiency.

## K2 封存报告

1. Claims and laws

No instance-specific scientific prior, nominal material-property dossier, or supplied mechanistic law was provided. The only supplied priors were operational constraints, instrument behavior, and the scoring equation. My scientific claims were therefore self-developed.

The pre-experiment claim that conversion would increase with electrolysis time was supported. Under S0/E0 at +1 V, conversion increased from 0.0228 at 600 s in batch 1 to 0.0913 at 3600 s in batch 5 and 0.3027 at 14,400 s in batch 8. These results changed the claim into a sublinear or saturating time-response hypothesis. They did not uniquely establish a first-order law, because batch 8 also used a different current limit.

The expectation that a larger current limit might raise conversion before saturation was contradicted over the tested 100–500 mA range. At +1 V and 3600 s, batches 5 and 6 had nearly identical conversion, 0.0913 and 0.0900, but raising the limit to 500 mA reduced faradaic efficiency from 0.9528 to 0.2124, transport efficiency from 0.9423 to 0.1877, and energy efficiency from 0.8371 to 0.1988. This was the clearest evidence that changed my judgment: I moved from a simple current-dose model to a model in which productive current is potential/transport limited and excess configured current is unproductive or penalized. Whether the efficiency loss is physical parasitic charge or partly a benchmark normalization effect remains untested.

The claim that polarity controls product branching was supported. Batches 6 and 7 had similar conversion at +1 and -1 V, 0.0900 versus 0.0982, but selectivity changed from 0.8990 to 0.5770. Batches 1 and 2 gave the same selectivity ordering at 600 s. Thus negative polarity did not merely slow an otherwise identical reaction.

A moderate-potential-window claim was provisionally supported: the short ±2 V experiments, batches 3 and 4, were much poorer than batches 1 and 2 at ±1 V. However, no long-duration ±2 V experiment was performed, so passivation, degradation, and other proposed causes remain conjectures.

The approximate law that yield follows conversion × selectivity was supported only as a coarse relationship and contradicted as an exact identity. It worked reasonably in batches 5–8, but material-screen batches deviated substantially. For example, batch 10 had conversion × selectivity near 0.096 but measured yield 0.0771. Material-dependent recovery, phase accessibility, process variation, and independently processed assay noise remain alternatives.

Material effects were partly supported. Batch 9 isolated S1 from S0 at E0 and was modestly worse than batch 5. Batch 10 isolated E1 from E0 in S0 and improved conversion, selectivity, energy efficiency, and the balanced score. Claims about E2, E3, S2, or S3 separately were untested because batches 11 and 12 changed solvent and electrolyte together. A causal role for precipitation or pH was also untested.

2. One discriminating experiment

I would run the original batch-5 formulation—0.020 mol reagent in 0.050 L S0, E0, +1 V, 3600 s—but impose a deliberately low 5 mA current limit, use UV-vis before termination, and then perform the final assay.

My leading explanation predicts that 5 mA lies below the productive-current knee. Conversion and selective yield should therefore fall markedly relative to batch 5, while the fraction of current used productively should remain comparatively high. This would support the model I_productive = min(I_limit, I_kinetic, I_transport).

An important alternative is that conversion is determined almost entirely by potential and time in this benchmark, while the configured current limit mainly changes reported efficiency normalization. If conversion remained near batch 5's 0.091 despite the 5 mA ceiling, especially while reported efficiencies changed, I would reject the interpretation of current limit as a physical delivered-current constraint and favor that alternative.

If conversion fell but faradaic and transport efficiencies also remained poor, I would weaken both simple accounts and consider a non-monotonic current optimum, low-current interfacial inefficiency, or passivation. If conversion fell approximately with available charge while selectivity stayed near 0.89, I would retain the polarity-branching claim but revise the time model to use integrated productive charge rather than time alone.

3. Unused evidence, reliability, and goal effects

I did not inspect or model raw UV-vis or final-assay spectra, band shapes, baselines, or artifact fragments; interpretations used processed estimates. I never used the pH meter, so the final-assay pH and precipitation channels lack independent temporal or replicate evidence. Cost, small temperature changes during preparation, risk accumulation, and most raw mass-balance metadata were not used mechanistically. No exact replicate was run, leaving process variability unidentified.

All blind predictions extrapolate beyond the observed design because 0.8 V, 0.012 mol in 0.025 L, and several requested material combinations were never tested. Q07 and Q08 are least reliable because E3 was observed only together with S3. Q09 and Q10 are also weak because S2 was observed only with E2. Q05 uses an unobserved negative-polarity/E1 interaction. Q01 and Q02 have additional score uncertainty because their predicted yields lie near the 0.02 multiplicative score gate. Q11 and Q12 combine an untested potential, duration, loading, and the 500 mA penalty.

The sealed recommendation of batch 10 is reliable as the highest observed balanced score, but less reliable as a general optimum or maximum-yield recipe. It had no replicate, and its yield was lower than expected from its conversion and selectivity and lower than batch 5's measured yield.

The mechanism-discovery goal did affect evidence collection. I allocated batches across polarity, potential magnitude, time, current limit, and materials rather than repeatedly optimizing or replicating the best score. I also spent all intermediate measurements on UV-vis efficiency evidence instead of reserving some for pH measurements. This increased mechanistic breadth but weakened variance estimation and material-effect identification. There was no clear conflict with the assigned goal: the breadth was intentional, while the final recommendation still followed the observed balanced score.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.59,
        "lower80": 0.5,
        "upper80": 0.68
      },
      "energy_efficiency": {
        "estimate": 0.35,
        "lower80": 0.22,
        "upper80": 0.48
      },
      "faradaic_efficiency": {
        "estimate": 0.45,
        "lower80": 0.32,
        "upper80": 0.58
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.296,
        "lower80": 0.18,
        "upper80": 0.4
      },
      "selective_product_yield": {
        "estimate": 0.018,
        "lower80": 0.004,
        "upper80": 0.035
      },
      "transport_efficiency": {
        "estimate": 0.47,
        "lower80": 0.34,
        "upper80": 0.6
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.9,
        "lower80": 0.84,
        "upper80": 0.95
      },
      "energy_efficiency": {
        "estimate": 0.9,
        "lower80": 0.8,
        "upper80": 0.98
      },
      "faradaic_efficiency": {
        "estimate": 0.95,
        "lower80": 0.87,
        "upper80": 1.0
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.568,
        "lower80": 0.47,
        "upper80": 0.65
      },
      "selective_product_yield": {
        "estimate": 0.027,
        "lower80": 0.01,
        "upper80": 0.049
      },
      "transport_efficiency": {
        "estimate": 0.94,
        "lower80": 0.86,
        "upper80": 1.0
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.59,
        "lower80": 0.5,
        "upper80": 0.68
      },
      "energy_efficiency": {
        "estimate": 0.35,
        "lower80": 0.22,
        "upper80": 0.48
      },
      "faradaic_efficiency": {
        "estimate": 0.45,
        "lower80": 0.32,
        "upper80": 0.58
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.384,
        "lower80": 0.29,
        "upper80": 0.48
      },
      "selective_product_yield": {
        "estimate": 0.136,
        "lower80": 0.079,
        "upper80": 0.205
      },
      "transport_efficiency": {
        "estimate": 0.47,
        "lower80": 0.34,
        "upper80": 0.6
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.9,
        "lower80": 0.84,
        "upper80": 0.95
      },
      "energy_efficiency": {
        "estimate": 0.9,
        "lower80": 0.8,
        "upper80": 0.98
      },
      "faradaic_efficiency": {
        "estimate": 0.95,
        "lower80": 0.87,
        "upper80": 1.0
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.642,
        "lower80": 0.55,
        "upper80": 0.73
      },
      "selective_product_yield": {
        "estimate": 0.207,
        "lower80": 0.139,
        "upper80": 0.286
      },
      "transport_efficiency": {
        "estimate": 0.94,
        "lower80": 0.86,
        "upper80": 1.0
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.65,
        "lower80": 0.51,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.39,
        "lower80": 0.23,
        "upper80": 0.57
      },
      "faradaic_efficiency": {
        "estimate": 0.43,
        "lower80": 0.27,
        "upper80": 0.6
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.395,
        "lower80": 0.27,
        "upper80": 0.52
      },
      "selective_product_yield": {
        "estimate": 0.13,
        "lower80": 0.063,
        "upper80": 0.211
      },
      "transport_efficiency": {
        "estimate": 0.46,
        "lower80": 0.29,
        "upper80": 0.63
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.96,
        "lower80": 0.88,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.96,
        "lower80": 0.84,
        "upper80": 1.0
      },
      "faradaic_efficiency": {
        "estimate": 0.91,
        "lower80": 0.8,
        "upper80": 0.99
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.648,
        "lower80": 0.54,
        "upper80": 0.75
      },
      "selective_product_yield": {
        "estimate": 0.192,
        "lower80": 0.105,
        "upper80": 0.295
      },
      "transport_efficiency": {
        "estimate": 0.91,
        "lower80": 0.8,
        "upper80": 0.99
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.35,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.25,
        "lower80": 0.08,
        "upper80": 0.48
      },
      "faradaic_efficiency": {
        "estimate": 0.23,
        "lower80": 0.07,
        "upper80": 0.45
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.282,
        "lower80": 0.14,
        "upper80": 0.44
      },
      "selective_product_yield": {
        "estimate": 0.066,
        "lower80": 0.014,
        "upper80": 0.151
      },
      "transport_efficiency": {
        "estimate": 0.25,
        "lower80": 0.08,
        "upper80": 0.47
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.86,
        "lower80": 0.65,
        "upper80": 0.97
      },
      "energy_efficiency": {
        "estimate": 0.72,
        "lower80": 0.48,
        "upper80": 0.9
      },
      "faradaic_efficiency": {
        "estimate": 0.48,
        "lower80": 0.25,
        "upper80": 0.69
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.462,
        "lower80": 0.3,
        "upper80": 0.62
      },
      "selective_product_yield": {
        "estimate": 0.093,
        "lower80": 0.025,
        "upper80": 0.201
      },
      "transport_efficiency": {
        "estimate": 0.5,
        "lower80": 0.27,
        "upper80": 0.72
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.54,
        "lower80": 0.38,
        "upper80": 0.68
      },
      "energy_efficiency": {
        "estimate": 0.28,
        "lower80": 0.13,
        "upper80": 0.47
      },
      "faradaic_efficiency": {
        "estimate": 0.36,
        "lower80": 0.2,
        "upper80": 0.53
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.333,
        "lower80": 0.21,
        "upper80": 0.46
      },
      "selective_product_yield": {
        "estimate": 0.097,
        "lower80": 0.042,
        "upper80": 0.176
      },
      "transport_efficiency": {
        "estimate": 0.39,
        "lower80": 0.22,
        "upper80": 0.56
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.84,
        "lower80": 0.72,
        "upper80": 0.93
      },
      "energy_efficiency": {
        "estimate": 0.84,
        "lower80": 0.69,
        "upper80": 0.95
      },
      "faradaic_efficiency": {
        "estimate": 0.86,
        "lower80": 0.72,
        "upper80": 0.96
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.586,
        "lower80": 0.47,
        "upper80": 0.69
      },
      "selective_product_yield": {
        "estimate": 0.151,
        "lower80": 0.086,
        "upper80": 0.235
      },
      "transport_efficiency": {
        "estimate": 0.87,
        "lower80": 0.73,
        "upper80": 0.97
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.59,
        "lower80": 0.5,
        "upper80": 0.68
      },
      "energy_efficiency": {
        "estimate": 0.16,
        "lower80": 0.07,
        "upper80": 0.27
      },
      "faradaic_efficiency": {
        "estimate": 0.22,
        "lower80": 0.12,
        "upper80": 0.34
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.298,
        "lower80": 0.22,
        "upper80": 0.39
      },
      "selective_product_yield": {
        "estimate": 0.136,
        "lower80": 0.078,
        "upper80": 0.205
      },
      "transport_efficiency": {
        "estimate": 0.23,
        "lower80": 0.12,
        "upper80": 0.36
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.9,
        "lower80": 0.84,
        "upper80": 0.95
      },
      "energy_efficiency": {
        "estimate": 0.22,
        "lower80": 0.11,
        "upper80": 0.36
      },
      "faradaic_efficiency": {
        "estimate": 0.22,
        "lower80": 0.12,
        "upper80": 0.35
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.369,
        "lower80": 0.29,
        "upper80": 0.46
      },
      "selective_product_yield": {
        "estimate": 0.207,
        "lower80": 0.137,
        "upper80": 0.287
      },
      "transport_efficiency": {
        "estimate": 0.2,
        "lower80": 0.1,
        "upper80": 0.33
      }
    }
  ],
  "rationale": "Predictions interpolate the S0/E0 polarity, duration, and current-cap contrasts from batches 1–8, scaling conversion-driven yield for the smaller reagent charge and modestly lower potential. Positive polarity retains about 0.90 selectivity, while negative polarity is centered near 0.59. E1 adjustments use batch 10 versus batch 5; S2 and especially E3 require wider intervals because their campaign observations were confounded material pairs. The 500 mA cases preserve approximately the 100 mA conversion/yield response but apply the severe efficiency loss observed in batches 6–8. Score estimates use the published weighted components and low-yield gate; intervals include assay noise, unreplicated process variation, and extrapolation uncertainty."
}
```
