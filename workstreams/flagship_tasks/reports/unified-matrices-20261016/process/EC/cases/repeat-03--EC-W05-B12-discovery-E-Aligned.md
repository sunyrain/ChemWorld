# repeat-03/EC-W05-B12-discovery-E-Aligned

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-03\EC-W05-B12-discovery-E-Aligned\participant\discovery-E-Aligned

## 同期笔记

### v1 · 公开事件 0

# Electrochemical hypothesis notebook

## Prior expectations (before physical experiments)

**H1 [tentative].** Product formation should depend on signed overpotential relative to a material-dependent effective standard potential. Because nominal shifts vary across solvent/electrolyte choices, equal applied potential may produce different conversion. Both signs must be tested rather than assuming only one productive polarity.

**H2 [tentative].** Delivered charge should rise with duration and current cap until limited by ohmic/transport ceilings; conversion may saturate with charge, while excessive magnitude or duration may lower selectivity and energy efficiency through competing reactions. A short/long and low/high-cap design can distinguish kinetic, charge-limited, and transport-limited behavior.

**H3 [tentative].** Conductivity should favor ohmic efficiency, diffusivity/thinner diffusion layer should favor transport efficiency, and proton activity/precipitation may alter selectivity. These nominal-property predictions are defeasible because fixed hidden residuals and interactions are declared.

**Planned test.** Use constant reagent/volume loading where possible, span both potential signs, durations, caps, and several material pairs; include strategically matched comparisons and one repeat. One intermediate UV-vis or pH observation per batch will be used for temporal or acid/precipitation diagnostics. A claim will be narrowed if effects are confounded by simultaneous factor changes or are not repeatable.

### v2 · 公开事件 73

# Electrochemical hypothesis notebook

## Prior expectations and tested design
Both potential signs, multiple potential magnitudes, duration/current-cap combinations, and four matched solvent/electrolyte pairs were tested at a common 0.02 mol in 0.05 L loading. Intermediate efficiency probes were included.

## H1 — signed potential window [supported in tested S0/E0 scope]
Negative potential is the productive polarity, but response is non-monotone in magnitude. At 600 s and 100 mA, -1 V produced a small target yield and nonzero score while +1 V produced no detected yield (final assays: runner-operation-0014 versus runner-operation-0007). At the same short conditions, +2 V was entirely unproductive and -2 V only weakly productive (runner-operation-0021, -0028). Thus a polarity effect is evident, while a simple absolute-voltage law is rejected.

At 2400 s/200 mA, -0.5 V outperformed -1 and -1.5 V in score and retained higher selectivity/energy efficiency (runner-operation-0035, -0042, -0049); conversion estimates were similar within their stated assay scale. Working consequence: expect a broad optimum near modest negative bias, with overbias mainly penalizing selectivity/efficiency.

## H2 — charge/time dependence [unresolved but supported qualitatively]
Longer/higher-cap operation increased S0/E0 final selective yield from the noisy low short-run regime to about 0.04 (runner-operation-0014 versus -0042), but current and duration changed together, so their separate roles remain unresolved. Conversion near 0.05 across -0.5 to -1.5 V after the long treatment suggests a duration/loading ceiling rather than potential-limited conversion in that window. A later prediction should not equate the current cap with delivered current.

## H3 — material effects and precipitation [supported as pair-specific; causal components unresolved]
At -0.5 V, 200 mA cap, 2400 s, matched S2/E2 gave target yield comparable to or slightly above S0/E0 despite lower ohmic efficiency, and essentially no precipitation, whereas S0/E0 showed saturated precipitation (runner-operation-0065 versus -0035). Matched S1/E1 and S3/E3 had much lower yield (runner-operation-0057, -0073). Numerical differences exceed single-assay noise for the low-yield pairs, but solvent and electrolyte were changed together. Crossed S2/E0 and S0/E2 tests are planned to distinguish solvent from electrolyte contributions.

## H4 — efficiency structure [tentative]
Ohmic efficiency does not by itself predict productive yield: matched S3/E3 retained high ohmic efficiency but poor faradaic/transport efficiencies and yield (runner-operation-0073). Productive performance appears multiplicative or bottlenecked by faradaic/transport/selectivity terms. Intermediate-to-final comparisons in matched-pair batches show modest drift but do not alone identify kinetics because UV-vis uncertainty is larger than final-assay uncertainty.

### v3 · 公开事件 89

# Electrochemical hypothesis notebook — final source-stage synthesis

## Experimental scope
All comparisons used 0.02 mol reagent in 0.05 L initial solvent. The campaign spans both potential signs, ±0.5 to ±2 V, 100–200 mA caps, 600–2400 s, all four matched material pairs, and two diagnostic crosses. Current is treated only as a cap, not an assumed delivered value.

## H1 — polarity and potential window [supported in S0/E0]
Productive behavior is polarity-specific and non-monotone. Negative bias produced target whereas positive bias at +1 or +2 V did not produce assay-detectable yield in the tested short runs (runner-operation-0014 versus -0007 and -0021). At 2400 s/200 mA, -0.5 V gave better score/selectivity/energy efficiency than -1 and -1.5 V, while their conversions were similar on the assay scale (runner-operation-0035, -0042, -0049). A useful predictive form is therefore a signed activation window with an overbias penalty, not a function of |V| alone.

**Testable consequence:** at fixed S0/E0 loading and long duration, values modestly negative should outperform either positive potentials or very negative potentials; the precise optimum remains unresolved between zero and -1 V.

## H2 — charge/time saturation [partially supported, components unresolved]
A short -1 V/100 mA-cap run had only noisy low yield, whereas the longer -1 V/200 mA-cap run reached about 0.04 yield (runner-operation-0014, -0042). Because duration and cap changed together, separate current-cap and time exponents cannot be identified. Similar conversion after 2400 s across -0.5 to -1.5 V suggests an approach to a loading/time ceiling in that range rather than simple proportionality to potential. Any blind prediction should model duration/current monotonically only at low exposure, then saturate, and should avoid assuming the cap is the delivered current.

## H3 — electrolyte/solvent and precipitation [supported for electrolyte-sensitive behavior; yield ranking uncertain]
Matched S2/E2 combined useful yield with essentially absent precipitation, while S0/E0 precipitated strongly (runner-operation-0065 versus -0035). Crosses localize much of the precipitation change to E2: S0/E2 also had zero precipitation and the highest observed yield estimate, whereas S2/E0 retained near-saturated precipitation and lower yield (runner-operation-0089 versus -0081). Thus electrolyte profile strongly controls precipitation/pH and likely shifts the effective potential; solvent also changes conversion/efficiencies, but its isolated yield effect is not secure because assay yield uncertainty is 0.01 and the cross differences are modest.

S1/E1 and S3/E3 were clearly less productive under the shared -0.5 V/2400 s condition (runner-operation-0057, -0073). Nominal conductivity alone is not a sufficient material ranking.

## H4 — coupled efficiency bottleneck [supported qualitatively]
High ohmic efficiency can coexist with poor faradaic/transport efficiencies and low yield (S3/E3, runner-operation-0073). Productive performance is better regarded as jointly limited by faradaic transfer, transport, selectivity, and precipitation than by any single efficiency. Intermediate UV-vis values are directionally consistent with final efficiencies but too uncertain to infer a detailed time law from one within-batch point.

## Remaining uncertainties and prediction discipline
No independent replicate was completed, and some contrasts are confounded or near stated measurement noise. The exact zero-bias threshold, delivered-current law, long-time degradation onset, and all solvent-by-electrolyte interactions remain unresolved. Predictions outside the observed loading/material/potential/time range should therefore be conservative. Batch 12 (S0/E2, -0.5 V, 200 mA cap, 2400 s segmented) is the preferred operating example because it couples the highest observed yield estimate with no precipitation and a near-best balanced score; batch 5 has a numerically slightly higher score but saturated precipitation.

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
    "electrochemical_conversion": 0.02042853832244873,
    "electrochemical_selectivity": 0.998518168926239,
    "energy_efficiency": 0.9158964157104492,
    "faradaic_efficiency": 0.8230613470077515,
    "ohmic_efficiency": 0.9602119326591492,
    "pH_normalized": 0.23308512568473816,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.7943575978279114
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
    "electrochemical_selectivity": 0.643891453742981,
    "energy_efficiency": 0.28471639752388,
    "faradaic_efficiency": 0.4072032868862152,
    "ohmic_efficiency": 0.9690497517585754,
    "pH_normalized": 0.2303897738456726,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.20330846309661865,
    "selective_product_yield": 0.01299411989748478,
    "transport_efficiency": 0.4334600865840912
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
    "ohmic_efficiency": 0.9711474776268005,
    "pH_normalized": 0.231104776263237,
    "precipitation_signal": 0.9869203567504883,
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
    "electrochemical_conversion": 0.0002544042654335499,
    "electrochemical_selectivity": 0.4774746894836426,
    "energy_efficiency": 0.036502815783023834,
    "faradaic_efficiency": 0.28798946738243103,
    "ohmic_efficiency": 0.9833056330680847,
    "pH_normalized": 0.23041419684886932,
    "precipitation_signal": 0.9876685738563538,
    "safety_risk": 0.05933958664536476,
    "score": 0.03072280064225197,
    "selective_product_yield": 0.0028336115647107363,
    "transport_efficiency": 0.2565019130706787
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
      "potential_V": -0.5
    },
    {
      "duration_s": 2400,
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
    "cost": 0.28595998883247375,
    "electrochemical_conversion": 0.052189648151397705,
    "electrochemical_selectivity": 0.7206888198852539,
    "energy_efficiency": 0.5987956523895264,
    "faradaic_efficiency": 0.4029203951358795,
    "ohmic_efficiency": 0.8754711151123047,
    "pH_normalized": 0.23537498712539673,
    "precipitation_signal": 0.9869949817657471,
    "safety_risk": 0.05933958664536476,
    "score": 0.37375444173812866,
    "selective_product_yield": 0.043278537690639496,
    "transport_efficiency": 0.39241093397140503
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
      "current_mA": 200,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1
    },
    {
      "duration_s": 2400,
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
    "cost": 0.2869200110435486,
    "electrochemical_conversion": 0.05089178681373596,
    "electrochemical_selectivity": 0.6424971222877502,
    "energy_efficiency": 0.2833634316921234,
    "faradaic_efficiency": 0.4159521162509918,
    "ohmic_efficiency": 0.9386242628097534,
    "pH_normalized": 0.2320990413427353,
    "precipitation_signal": 0.9976252913475037,
    "safety_risk": 0.05933958664536476,
    "score": 0.3205331563949585,
    "selective_product_yield": 0.04144609346985817,
    "transport_efficiency": 0.391268789768219
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
      "current_mA": 200,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.5
    },
    {
      "duration_s": 2400,
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
    "cost": 0.287880003452301,
    "electrochemical_conversion": 0.0513702854514122,
    "electrochemical_selectivity": 0.5681748986244202,
    "energy_efficiency": 0.1447705179452896,
    "faradaic_efficiency": 0.33195286989212036,
    "ohmic_efficiency": 0.9906179308891296,
    "pH_normalized": 0.23111364245414734,
    "precipitation_signal": 0.9826673865318298,
    "safety_risk": 0.05933958664536476,
    "score": 0.2739037573337555,
    "selective_product_yield": 0.03068597801029682,
    "transport_efficiency": 0.33535322546958923
  }
}
```

### 批次 8 · 终点事件 57

```json
{
  "ordinal": 8,
  "lifecycle_index": 8,
  "end_step": 57,
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
      "current_mA": 200,
      "electrolyte_profile": 1,
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
    "cost": 0.32396000623703003,
    "electrochemical_conversion": 0.04600495845079422,
    "electrochemical_selectivity": 0.5513649582862854,
    "energy_efficiency": 0.413086861371994,
    "faradaic_efficiency": 0.4102906584739685,
    "ohmic_efficiency": 0.7678598165512085,
    "pH_normalized": 0.20273199677467346,
    "precipitation_signal": 0.7230653762817383,
    "safety_risk": 0.08273958414793015,
    "score": 0.1062340959906578,
    "selective_product_yield": 0.007025619503110647,
    "transport_efficiency": 0.4037953019142151
  }
}
```

### 批次 9 · 终点事件 65

```json
{
  "ordinal": 9,
  "lifecycle_index": 9,
  "end_step": 65,
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
      "current_mA": 200,
      "electrolyte_profile": 2,
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
    "cost": 0.35596001148223877,
    "electrochemical_conversion": 0.05185577645897865,
    "electrochemical_selectivity": 0.5668773055076599,
    "energy_efficiency": 0.426154762506485,
    "faradaic_efficiency": 0.4156349301338196,
    "ohmic_efficiency": 0.7158676981925964,
    "pH_normalized": 0.17194634675979614,
    "precipitation_signal": 0.008188718929886818,
    "safety_risk": 0.10073958337306976,
    "score": 0.3192174434661865,
    "selective_product_yield": 0.047616101801395416,
    "transport_efficiency": 0.4364662170410156
  }
}
```

### 批次 10 · 终点事件 73

```json
{
  "ordinal": 10,
  "lifecycle_index": 10,
  "end_step": 73,
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
      "current_mA": 200,
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
    "cost": 0.3359600007534027,
    "electrochemical_conversion": 0.03456278145313263,
    "electrochemical_selectivity": 0.5690513253211975,
    "energy_efficiency": 0.267119437456131,
    "faradaic_efficiency": 0.15534301102161407,
    "ohmic_efficiency": 0.8588048219680786,
    "pH_normalized": 0.28282278776168823,
    "precipitation_signal": 0.0,
    "safety_risk": 0.11333958804607391,
    "score": 0.08861536532640457,
    "selective_product_yield": 0.007568552624434233,
    "transport_efficiency": 0.15669260919094086
  }
}
```

### 批次 11 · 终点事件 81

```json
{
  "ordinal": 11,
  "lifecycle_index": 11,
  "end_step": 81,
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
      "current_mA": 200,
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
    "cost": 0.35596001148223877,
    "electrochemical_conversion": 0.0672011598944664,
    "electrochemical_selectivity": 0.5179727673530579,
    "energy_efficiency": 0.45247137546539307,
    "faradaic_efficiency": 0.42643263936042786,
    "ohmic_efficiency": 0.8376917839050293,
    "pH_normalized": 0.2482246607542038,
    "precipitation_signal": 0.9902478456497192,
    "safety_risk": 0.10073958337306976,
    "score": 0.32264694571495056,
    "selective_product_yield": 0.029372289776802063,
    "transport_efficiency": 0.43361255526542664
  }
}
```

### 批次 12 · 终点事件 89

```json
{
  "ordinal": 12,
  "lifecycle_index": 12,
  "end_step": 89,
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
      "electrolyte_profile": 2,
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
    "cost": 0.30395999550819397,
    "electrochemical_conversion": 0.04481462761759758,
    "electrochemical_selectivity": 0.6758767366409302,
    "energy_efficiency": 0.5574389696121216,
    "faradaic_efficiency": 0.450214684009552,
    "ohmic_efficiency": 0.8336706757545471,
    "pH_normalized": 0.15362673997879028,
    "precipitation_signal": 0.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.3731827735900879,
    "selective_product_yield": 0.052801910787820816,
    "transport_efficiency": 0.4714396297931671
  }
}
```

## K1 封存报告

# Mechanistic account of the electrochemical world

## 1. Empirical domain

The campaign used twelve batches, all at the same initial loading: 0.020 mol limiting reagent in 0.050 L solvent. Applied potential ranged from +2.0 to −2.0 V, the current cap from 100 to 200 mA, and total electrolysis time from 600 to 2400 s. Therefore, the evidence supports comparisons within this loading regime; it does not independently establish concentration, scale, or electrode-area laws.

The main response variables were selective-product yield, conversion, selectivity, faradaic, transport, ohmic and energy efficiencies, normalized pH, and precipitation. These observables should not be treated as interchangeable. In particular, measured selective-product yield was not always numerically equal to conversion × selectivity. I therefore regard yield as a separately calibrated endpoint affected by product accessibility or recovery and instrument/process noise, rather than imposing an exact algebraic identity unsupported by the observations.

## 2. Signed potential controls the reaction

The clearest result is that potential polarity matters. This is not a system governed simply by |V|.

With S0/E0, 100 mA and 600 s:

- Batch 1 at +1.0 V had yield 0, score 0, conversion 0.0204, and selectivity 0.9985, despite high faradaic and energy efficiencies of 0.823 and 0.916.
- Batch 2 at −1.0 V produced yield 0.0130 and score 0.203, with selectivity 0.644, faradaic efficiency 0.407, and energy efficiency 0.285.
- Batch 3 at +2.0 V had zero yield, conversion, selectivity, faradaic efficiency and energy efficiency within the processed estimates.
- Batch 4 at −2.0 V was only weakly productive: yield 0.00283, score 0.0307, selectivity 0.477 and energy efficiency 0.0365.

Thus, the high efficiency values in batch 1 did not imply production. They probably describe efficient passage or storage of charge in a nonproductive regime. Batch 1 caused me to reject an early “maximize measured efficiency” explanation. Batches 2–4 instead support a cathodic productive pathway activated at negative potential, together with loss of performance under excessive negative bias.

A useful conjectural variable is a material-dependent signed overpotential:

η = V_applied − E_eff(solvent, electrolyte),

where E_eff contains the declared solvent and electrolyte standard-potential shifts plus fixed hidden interfacial residuals. Product formation occurs over a bounded negative-η window. A schematic product rate is

r_P = k_P(material,pH)·C_R·f_act(−η)·f_transport,

where f_act rises after cathodic activation but saturates. A competing rate, r_side, rises more strongly at excessive |η|. Then selectivity may be represented qualitatively as

S ≈ r_P/(r_P + r_side).

This explains why stronger negative potential can preserve conversion while lowering selectivity and energy efficiency.

## 3. A broad optimum near modest negative bias

Batches 5–7 held S0/E0, loading, current cap (200 mA), and duration (2400 s) constant while changing negative potential:

- Batch 5, −0.5 V: conversion 0.0522, selectivity 0.721, yield 0.0433, faradaic efficiency 0.403, energy efficiency 0.599, score 0.374.
- Batch 6, −1.0 V: conversion 0.0509, selectivity 0.642, yield 0.0414, faradaic efficiency 0.416, energy efficiency 0.283, score 0.321.
- Batch 7, −1.5 V: conversion 0.0514, selectivity 0.568, yield 0.0307, faradaic efficiency 0.332, energy efficiency 0.145, score 0.274.

Conversion was nearly invariant across these three batches, whereas selectivity, yield and energy efficiency declined with increasingly negative potential. This is evidence for a conversion or exposure ceiling after 2400 s and an overbias penalty, not evidence that more negative potential accelerates useful conversion indefinitely. The best observed region was −0.5 V, but the experiment did not sample between 0 and −0.5 V; the exact optimum and onset potential remain unidentified.

Ohmic efficiency increased from 0.875 at −0.5 V to 0.939 at −1.0 V and 0.991 at −1.5 V. That pattern reinforces the distinction between electrical conduction and chemical usefulness: larger voltage can make resistive losses a smaller fraction of the electrical input while simultaneously worsening chemical selectivity and energy efficiency.

## 4. Exposure, current and transport

A plausible charge/exposure model is

I_delivered = min(I_cap, I_kinetic(η), I_lim(material)),
Q_eff = ∫ I_delivered dt,
X = X_max·[1 − exp(−k_Q Q_eff/n_0)],

with a separate degradation or side-reaction term at large overpotential or exposure. The limiting current could scale approximately as

I_lim ∝ A·D_eff·C_R/δ_eff,

while solution resistance could scale as

R_Ω ∝ gap/(A·κ_eff).

These equations are mechanistic scaffolds, not fitted laws. Electrode area, gap and base resistance were fixed but hidden, so their individual values cannot be inferred.

The comparison between batch 2 (−1 V, 100 mA, 600 s; yield 0.0130) and batch 6 (−1 V, 200 mA, 2400 s; yield 0.0414) supports increasing production with greater exposure. However, current cap and duration changed together. Consequently, the campaign cannot identify whether time, delivered current, or both caused the increase. It would be unjustified to calculate charge as I_cap·t and assume all of it was delivered productively.

The similar approximately 0.051 conversions in batches 5–7 suggest saturation at the tested long exposure. This may reflect reactant accessibility, interfacial coverage, mass transport, or an equilibrium-like ceiling. A simple linear-in-time extrapolation beyond 2400 s is therefore not supported.

## 5. Material, acidity and precipitation couplings

At −0.5 V, 200 mA and 2400 s, matched material pairs produced markedly different behavior:

- Batch 5, S0/E0: yield 0.0433, conversion 0.0522, score 0.374, pH_normalized 0.235, precipitation 0.987.
- Batch 8, S1/E1: yield 0.00703, conversion 0.0460, score 0.106, pH 0.203, precipitation 0.723.
- Batch 9, S2/E2: yield 0.0476, conversion 0.0519, score 0.319, pH 0.172, precipitation 0.00819.
- Batch 10, S3/E3: yield 0.00757, conversion 0.0346, score 0.0886, pH 0.283, precipitation 0.

These results show that eliminating precipitation is not sufficient for productivity: S3/E3 had no detected precipitation yet poor yield because faradaic and transport efficiencies were only 0.155 and 0.157. Conversely, S0/E0 produced useful yield despite nearly saturated precipitation. Productive operation requires several favorable factors simultaneously.

The pH ordering is broadly consistent with the nominal acid properties. E2, with the highest declared acid concentration and lowest pKa, gave the lowest normalized pH in batches 9 and 12. E3 gave the highest pH in batch 10. I interpret pH mainly as an electrolyte-controlled state variable that can shift proton-coupled kinetics, interfacial speciation, and precipitation.

Precipitation can be represented schematically by an ion product condition:

P_precip ≈ sigmoid[a·(log Q_ion − log K_sp,eff)],

with K_sp,eff modified by solvent. The nominal dossier predicts E0 to be much more precipitation-prone than E2 because E0 has more precipitating salt and a much smaller solubility product. The experiments support that direction.

## 6. Crossed experiments separate some electrolyte and solvent effects

Batches 11 and 12 crossed the S0/S2 solvents and E0/E2 electrolytes at −0.5 V, 200 mA and 2400 s:

- Batch 11, S2/E0: conversion 0.0672, selectivity 0.518, yield 0.0294, score 0.323, pH 0.248, precipitation 0.990.
- Batch 12, S0/E2: conversion 0.0448, selectivity 0.676, yield 0.0528, score 0.373, pH 0.154, precipitation 0.

Together with batch 5 (S0/E0) and batch 9 (S2/E2), these crosses indicate that electrolyte identity dominates the observed precipitation and pH changes: both E0 batches precipitated strongly, while both E2 batches did not. E2 also appears favorable for accessible selective yield under these conditions. However, the yield differences are not all decisive relative to the final-assay yield standard deviation of 0.01. For example, batch 12 exceeded batch 5 by only about 0.0095. I therefore regard “E2 suppresses precipitation” as strongly supported, but “E2 intrinsically raises yield by a fixed amount” as only tentative.

Solvent effects are more complicated. S2/E0 in batch 11 had the highest measured conversion, 0.0672, but lower selectivity and yield than S0/E2. S2 may aid reactant conversion or transport while changing product recovery or side reactions. Because only the S0/S2 × E0/E2 submatrix was crossed, general solvent–electrolyte interaction terms remain unidentifiable.

## 7. Efficiency bottlenecks

No single efficiency predicts yield. Batch 10 had high ohmic efficiency, 0.859, but low faradaic and transport efficiencies and very low yield. Batch 1 had high faradaic, ohmic and energy efficiencies but zero selective yield. The system is better viewed as a coupled sequence:

1. the signed potential must activate the target electron-transfer pathway;
2. ionic conduction must deliver current with limited ohmic loss;
3. reactant must reach the interface, imposing a transport ceiling;
4. transferred charge must be faradaically assigned to chemical reactions;
5. competition among target and side pathways sets selectivity;
6. precipitation, solvation and phase accessibility affect recovered selective yield.

A qualitative composite law might be

Y_obs ≈ X(Q_eff,η)·S(η,pH,material)·R_access(precipitation,solvent) + measurement/process error.

This is not an exact identity. The observed discrepancies between yield and conversion × selectivity imply that R_access, normalization differences, latent interactions, or assay noise matter. At very low conversion, selectivity estimates are also unstable: batch 1’s selectivity of 0.999 accompanied zero measured yield.

Energy efficiency can be interpreted schematically as the chemical value of target formation divided by electrical input. It therefore falls both when |V| is unnecessarily large and when faradaic charge is diverted to side pathways. The decline from 0.599 at −0.5 V to 0.145 at −1.5 V in batches 5–7 is consistent with this interpretation.

## 8. Intermediate evidence

The 600 s UV-visible observations in batches 8–11 already showed material-specific efficiency patterns that largely persisted to the final assay after another 1800 s. For example, batch 9 changed from intermediate faradaic/transport/ohmic efficiencies of about 0.390/0.394/0.688 to final values of 0.416/0.436/0.716. Batch 10 remained faradaically and transport limited: approximately 0.163/0.122 at the intermediate measurement and 0.155/0.157 finally. Batch 11 changed from approximately 0.372/0.419/0.863 to 0.426/0.434/0.838.

These comparisons suggest that material identity establishes persistent bottlenecks rather than merely changing the endpoint. Nevertheless, the intermediate UV-visible measurement has larger uncertainty than the final assay, and the two measurements used different calibration channels. I do not infer detailed kinetic rate constants from these pairs.

## 9. Scope, uncertainty and alternatives

Supported within the tested domain:

- productive chemistry requires negative rather than positive applied potential;
- excessive negative bias penalizes selectivity and energy efficiency;
- long exposure approaches a conversion ceiling near the tested loading;
- electrolyte profile strongly controls pH and precipitation;
- ohmic efficiency alone is not a proxy for chemical productivity;
- faradaic, transport, selectivity and product-accessibility effects jointly limit yield.

Unidentifiable from this campaign:

- delivered current versus current cap;
- separate current and duration exponents;
- electrode area, gap, resistance and absolute limiting current;
- the exact onset or optimum between 0 and −0.5 V;
- behavior at other reagent concentrations or volumes;
- independent effects for every solvent and electrolyte, because most were tested only as matched pairs;
- long-time degradation beyond 2400 s;
- repeatability, because no exact independent replicate was performed;
- whether yield/conversion inconsistencies arise chiefly from recovery, normalization, latent chemistry, or assay noise.

Plausible alternatives remain. The apparent potential optimum could reflect a material-shifted thermodynamic threshold plus parasitic reduction, or an interfacial adsorption window rather than ordinary Butler–Volmer competition. The conversion ceiling could be transport depletion, electrode passivation, precipitation-induced blocking, or finite accessible reactant. E2’s advantage could be caused primarily by suppressed precipitation, by its potential shift and acidity, or by an unobserved correlated residual. The present data favor a coupled cathodic-activation/transport/side-reaction model but do not uniquely select among these microscopic alternatives.

Overall, I think this world behaves as a signed-potential electrochemical network with a modest-cathodic productive window, saturating exposure response, material-dependent transport and resistance, proton/speciation coupling, and electrolyte-controlled precipitation. Batch 12 was a strong operating example because S0/E2 at −0.5 V and 2400 s combined the highest observed yield estimate (0.0528), zero precipitation, and a near-best score (0.373), while batch 5 had the numerically highest score (0.374) but nearly saturated precipitation.

## K2 封存报告

1. **Claims and laws tested.** No instance-specific mechanism prior or expected answer was supplied. The only supplied scientific prior was the nominal material-property dossier, explicitly described as incomplete and potentially affected by hidden residuals.

- The self-developed **signed-potential law** was supported: negative bias was productive whereas positive bias was not under matched short-run conditions. Batch 2 at −1 V gave yield 0.0130 and score 0.203, while batch 1 at +1 V gave zero yield and score; batches 3 and 4 similarly distinguished +2 V from weakly productive −2 V.
- A simple law that productivity increases monotonically with |potential| was contradicted. At fixed S0/E0, 200 mA and 2400 s, batches 5–7 had similar conversion near 0.051, but yield, selectivity and energy efficiency declined from −0.5 to −1.5 V. This evidence changed the interpretation to a bounded cathodic window with an overbias penalty.
- The idea that high electrical efficiency alone predicts product formation was contradicted by batch 1, whose faradaic and energy efficiencies were high despite zero yield. Batch 10 also showed that high ohmic efficiency can coexist with poor faradaic/transport performance and low yield.
- Increasing electrolysis exposure was qualitatively supported by batches 2 and 6, but current cap and duration changed together. Separate current and time laws, the delivered current, and the proposed saturating charge equation remained untested.
- Electrolyte-controlled precipitation and acidity were supported. E0 precipitated strongly in batches 5 and 11, whereas E2 showed essentially no precipitation in batches 9 and 12. The lower normalized pH with E2 was also consistent with its nominal acid properties. The S0/S2 crosses in batches 11–12 changed the judgment from a generic matched-material effect to a more specific electrolyte-dominated precipitation effect.
- The nominal conductivity ranking was not a sufficient performance law: batch 10 retained good ohmic efficiency but poor yield, while batch 9 performed well despite lower ohmic efficiency. Detailed transport equations and microscopic causes such as adsorption, passivation, or proton-coupled electron transfer remained untested.

2. **One additional discriminating experiment.** I would repeat the batch-5 recipe exactly—0.020 mol reagent, 0.050 L S0, E0, −0.5 V and 2400 s—but lower only the current cap from 200 to 100 mA, followed by the same final assay. This directly separates two explanations that were confounded in the campaign. My leading explanation is that delivered current is substantially kinetic- or transport-limited, so increasing the cap above that limit has only a modest effect; the alternative is a cap-controlled charge law in which conversion and yield scale approximately with available current.

If the 100 mA result remained close to batch 5—conversion about 0.052 and yield about 0.043 within assay and process uncertainty—I would strengthen the transport/kinetic-limitation and time-ceiling interpretation. If conversion and yield fell toward roughly half those values while selectivity remained similar, I would favor a current-proportional charge model over the proposed cap-insensitive saturation. If yield fell disproportionately while conversion remained similar, I would instead infer a current-dependent selectivity or product-accessibility mechanism. An exact replicate at 200 mA would still ultimately be needed to quantify process variability.

3. **Unused evidence, weak predictions, and goal effects.** The detailed raw spectra, peak shapes and most artifact contents were not used quantitatively; interpretation relied mainly on processed estimates. Cost, temperature changes, detailed risk accumulation, sample-volume changes, and most calibrated mass-balance fields were also not used mechanistically. Intermediate UV-visible measurements were used only qualitatively because they came from a noisier instrument than the final assay. The nominal material properties were not fitted quantitatively, and no exact replicate was available to estimate process repeatability.

The least reliable predictions are Q11–Q12 because 500 mA was outside the experimentally studied cap range, and Q03–Q12 because 7200 s was a threefold extrapolation beyond the longest campaign duration. Q05–Q08 are additionally weak because S0 paired with E1 or E3 was never directly observed; only matched S1/E1 and S3/E3 batches were available. Positive-polarity score predictions are fragile because selective yield lies near zero and the published 0.02 yield gate makes small yield errors cause large proportional score changes. All predictions also extrapolated from the campaign’s fixed 0.020 mol/0.050 L loading to 0.012 mol/0.025 L.

The recommendation of batch 12 is reliable for avoiding precipitation but less reliable as a claim of uniquely maximal score: its score of 0.373 was essentially tied with batch 5 at 0.374, and its yield advantage was comparable to the stated yield uncertainty.

The discovery-oriented goal did affect evidence collection. It encouraged testing both polarities, multiple magnitudes, all matched material pairs, and the S0/S2–E0/E2 crosses rather than repeatedly optimizing near batch 5. That produced broader mechanistic evidence but left no exact replicate and insufficient separation of current from duration. I see no fundamental conflict with the assigned goal, but the breadth–replication tradeoff reduced precision in the final extrapolations.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.67,
        "lower80": 0.5,
        "upper80": 0.82
      },
      "energy_efficiency": {
        "estimate": 0.4,
        "lower80": 0.25,
        "upper80": 0.55
      },
      "faradaic_efficiency": {
        "estimate": 0.41,
        "lower80": 0.29,
        "upper80": 0.54
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.34,
        "lower80": 0.16,
        "upper80": 0.46
      },
      "selective_product_yield": {
        "estimate": 0.024,
        "lower80": 0.006,
        "upper80": 0.052
      },
      "transport_efficiency": {
        "estimate": 0.4,
        "lower80": 0.27,
        "upper80": 0.54
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.95,
        "lower80": 0.65,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.9,
        "lower80": 0.72,
        "upper80": 0.99
      },
      "faradaic_efficiency": {
        "estimate": 0.82,
        "lower80": 0.65,
        "upper80": 0.95
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.24
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0.0,
        "upper80": 0.012
      },
      "transport_efficiency": {
        "estimate": 0.79,
        "lower80": 0.62,
        "upper80": 0.92
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.67,
        "lower80": 0.52,
        "upper80": 0.8
      },
      "energy_efficiency": {
        "estimate": 0.4,
        "lower80": 0.25,
        "upper80": 0.54
      },
      "faradaic_efficiency": {
        "estimate": 0.41,
        "lower80": 0.29,
        "upper80": 0.53
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.37,
        "lower80": 0.25,
        "upper80": 0.5
      },
      "selective_product_yield": {
        "estimate": 0.105,
        "lower80": 0.05,
        "upper80": 0.18
      },
      "transport_efficiency": {
        "estimate": 0.4,
        "lower80": 0.27,
        "upper80": 0.53
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.9,
        "lower80": 0.55,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.82,
        "lower80": 0.58,
        "upper80": 0.96
      },
      "faradaic_efficiency": {
        "estimate": 0.78,
        "lower80": 0.55,
        "upper80": 0.92
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.05,
        "lower80": 0.0,
        "upper80": 0.35
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.02
      },
      "transport_efficiency": {
        "estimate": 0.74,
        "lower80": 0.5,
        "upper80": 0.9
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.38,
        "upper80": 0.76
      },
      "energy_efficiency": {
        "estimate": 0.35,
        "lower80": 0.18,
        "upper80": 0.53
      },
      "faradaic_efficiency": {
        "estimate": 0.4,
        "lower80": 0.25,
        "upper80": 0.55
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.33,
        "lower80": 0.2,
        "upper80": 0.46
      },
      "selective_product_yield": {
        "estimate": 0.07,
        "lower80": 0.025,
        "upper80": 0.14
      },
      "transport_efficiency": {
        "estimate": 0.45,
        "lower80": 0.28,
        "upper80": 0.62
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.85,
        "lower80": 0.48,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.76,
        "lower80": 0.48,
        "upper80": 0.94
      },
      "faradaic_efficiency": {
        "estimate": 0.68,
        "lower80": 0.42,
        "upper80": 0.88
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.05,
        "lower80": 0.0,
        "upper80": 0.34
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.02
      },
      "transport_efficiency": {
        "estimate": 0.72,
        "lower80": 0.46,
        "upper80": 0.89
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.52,
        "lower80": 0.3,
        "upper80": 0.71
      },
      "energy_efficiency": {
        "estimate": 0.22,
        "lower80": 0.08,
        "upper80": 0.4
      },
      "faradaic_efficiency": {
        "estimate": 0.22,
        "lower80": 0.08,
        "upper80": 0.39
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.26,
        "lower80": 0.13,
        "upper80": 0.4
      },
      "selective_product_yield": {
        "estimate": 0.045,
        "lower80": 0.012,
        "upper80": 0.105
      },
      "transport_efficiency": {
        "estimate": 0.22,
        "lower80": 0.07,
        "upper80": 0.4
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.75,
        "lower80": 0.35,
        "upper80": 0.96
      },
      "energy_efficiency": {
        "estimate": 0.56,
        "lower80": 0.28,
        "upper80": 0.79
      },
      "faradaic_efficiency": {
        "estimate": 0.52,
        "lower80": 0.26,
        "upper80": 0.75
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.04,
        "lower80": 0.0,
        "upper80": 0.3
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.019
      },
      "transport_efficiency": {
        "estimate": 0.4,
        "lower80": 0.18,
        "upper80": 0.64
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.5,
        "lower80": 0.32,
        "upper80": 0.68
      },
      "energy_efficiency": {
        "estimate": 0.34,
        "lower80": 0.19,
        "upper80": 0.51
      },
      "faradaic_efficiency": {
        "estimate": 0.43,
        "lower80": 0.29,
        "upper80": 0.57
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.34,
        "lower80": 0.22,
        "upper80": 0.46
      },
      "selective_product_yield": {
        "estimate": 0.08,
        "lower80": 0.033,
        "upper80": 0.15
      },
      "transport_efficiency": {
        "estimate": 0.44,
        "lower80": 0.29,
        "upper80": 0.59
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.86,
        "lower80": 0.5,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.75,
        "lower80": 0.48,
        "upper80": 0.92
      },
      "faradaic_efficiency": {
        "estimate": 0.78,
        "lower80": 0.53,
        "upper80": 0.92
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.05,
        "lower80": 0.0,
        "upper80": 0.34
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.02
      },
      "transport_efficiency": {
        "estimate": 0.78,
        "lower80": 0.54,
        "upper80": 0.92
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.38,
        "upper80": 0.75
      },
      "energy_efficiency": {
        "estimate": 0.28,
        "lower80": 0.11,
        "upper80": 0.47
      },
      "faradaic_efficiency": {
        "estimate": 0.32,
        "lower80": 0.16,
        "upper80": 0.5
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.32,
        "lower80": 0.19,
        "upper80": 0.45
      },
      "selective_product_yield": {
        "estimate": 0.13,
        "lower80": 0.06,
        "upper80": 0.23
      },
      "transport_efficiency": {
        "estimate": 0.3,
        "lower80": 0.13,
        "upper80": 0.49
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.75,
        "lower80": 0.38,
        "upper80": 0.96
      },
      "energy_efficiency": {
        "estimate": 0.48,
        "lower80": 0.22,
        "upper80": 0.72
      },
      "faradaic_efficiency": {
        "estimate": 0.55,
        "lower80": 0.29,
        "upper80": 0.77
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.04,
        "lower80": 0.0,
        "upper80": 0.3
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.019
      },
      "transport_efficiency": {
        "estimate": 0.5,
        "lower80": 0.25,
        "upper80": 0.73
      }
    }
  ],
  "rationale": "Predictions use the observed cathodic productive window near −0.5 to −1 V, saturation with exposure, and the strong positive-polarity suppression of selective yield. Long cathodic runs were extrapolated upward from batches 2 and 5–7, with wider intervals because duration, current cap, loading, and concentration were not independently identified. Electrolyte and solvent adjustments follow the matched-pair and S0/S2–E0/E2 cross comparisons; E1 and especially E3 carry broader material uncertainty. At 500 mA I assumed transport-limited gains in yield but lower efficiencies rather than charge scaling linearly with the cap. Score estimates include inferred conversion and ohmic terms and the published yield gate, making positive-polarity score intervals especially asymmetric."
}
```
