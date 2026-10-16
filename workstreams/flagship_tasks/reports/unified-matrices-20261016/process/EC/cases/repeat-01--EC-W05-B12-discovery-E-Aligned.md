# repeat-01/EC-W05-B12-discovery-E-Aligned

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-01\EC-W05-B12-discovery-E-Aligned\participant\discovery-E-Aligned

## 同期笔记

### v1 · 公开事件 0

# Electrochemical hypothesis notebook

## Prior expectations (before physical experiments)
**H1 [tentative].** Product formation is polarity-specific and rises with absolute overpotential and electrolysis time until conversion saturates; excessive driving force or charge may lower selectivity through degradation. A sign reversal at otherwise matched conditions should strongly reduce selective yield if this is correct.

**H2 [tentative].** Delivered performance separates into kinetic/charge, transport, and ohmic terms. Higher conductivity should improve ohmic and energy efficiency, while diffusivity and diffusion-layer thickness should govern transport/current-cap sensitivity. Nominal properties suggest E0/S0 may be conductive, E1 transport-favorable, and E3 highly conductive but diffusion-layer-limited.

**H3 [tentative].** Current is a cap rather than guaranteed delivery. At low caps, yield should scale approximately with current × time; at high caps, potential, ohmic resistance, and mass transport may limit delivered charge, causing a plateau.

**H4 [tentative].** pH and precipitation may independently gate efficiency/selectivity. E2 is more acidic; E0 has the strongest nominal precipitation tendency. pH/UV-vis snapshots will be used to distinguish material-state effects from charge effects.

Planned tests use a fixed loading (0.020 mol in 0.040 L) and cover both potential signs, short/long duration, all solvent/electrolyte labels, and current caps. Matched contrasts and at least one replicate will distinguish gross response trends from instrument noise.

### v2 · 公开事件 63

# Electrochemical hypothesis notebook

## Prior expectations
Fixed loading is 0.020 mol in 0.040 L. The planned scope covers both signs, time, materials, and current caps.

## H1 [supported in tested scope]
Product formation is cathodic (negative applied potential). At +1.2 V, E0/S0, 100 mA, 1800 s, UV-vis efficiencies were effectively zero and final selective yield was 0 (events runner-operation-0005, -0007). The matched -1.2 V experiment produced nonzero faradaic/transport response and selective yield about 0.019 (events -0012, -0014). This sign contrast is much larger than the stated assay uncertainty, though exact near-zero conversion remains noise-limited.

## H2 [narrowed]
Efficiency is not predicted by conductivity alone. E0/S0 has near-unity ohmic efficiency but complete precipitation signal and only modest productive response (events -0014, -0021). E2 and E3 largely suppress precipitation (events -0035, -0042), while E2/S0 and E3/S0 show broadly similar low-charge outcomes. Thus precipitation is a separable material penalty; ohmic efficiency alone is insufficient.

## H3 [partly supported; alternatives unresolved]
Increasing drive/time from -1.2 V, 100 mA, 1800 s to longer/higher-charge conditions raises conversion and selective yield, but faradaic efficiency and selectivity can decline. The -1.5 V, 300 mA, 7200 s E2 runs gave conversion about 0.14–0.16 and yields roughly 0.04–0.085 depending on solvent (events -0049, -0056, -0063), compared with ~0.017 at the short E2/S0 condition (-0035). Potential, duration, current cap, and solvent are confounded across this comparison; dedicated current-cap tests follow.

## H4 [supported qualitatively]
Electrolyte controls pH and precipitation: E2 is more acidic and essentially nonprecipitating in tested solvents, while E0 precipitates strongly. Solvent S1 and S3 produced numerically higher yield than S2 in the long E2 screen, but single-run differences are not yet firm given assay noise and hidden solvent residuals.

## Next tests
At E2/S1 and -1.5 V, compare 50 versus 500 mA caps at 7200 s, then a 300 mA 14400 s run. If the low-cap run is distinctly lower while 300 and 500 mA are similar, infer a transition from charge-cap limitation to potential/transport limitation. If 14400 s materially exceeds 7200 s, time saturation has not yet been reached.

### v3 · 公开事件 84

# Electrochemical hypothesis notebook

## Scope
All conclusions refer to the fixed loading 0.020 mol limiting reagent in 0.040 L solvent. The campaign spans both polarity signs, 1800–14400 s, 50–500 mA caps, four electrolytes, and four solvents (with incomplete factorial coverage).

## H1 [supported in tested scope]: cathodic, charge-driven conversion
The productive direction is negative potential. The matched ±1.2 V, E0/S0, 100 mA, 1800 s contrast changed UV-vis faradaic/transport response from effectively zero at positive polarity (runner-operation-0005) to clearly nonzero at negative polarity (-0012); final selective yield changed from 0 to about 0.019 (-0007, -0014). This supports a polarity-specific cathodic reaction rather than a sign-symmetric heating or time effect.

At E2/S1 and -1.5 V, conversion increased strongly with the current cap at 7200 s: about 0.038, 0.159, and 0.276 for 50, 300, and 500 mA (-0070, -0049, -0077). Doubling duration at 500 mA to 14400 s increased conversion to about 0.510 (-0084). These results are approximately consistent with delivered charge controlling conversion over this range; there is no demonstrated saturation yet. The 300 mA datum used a different run order only, not a replicate, so exact linearity remains unresolved.

## H2 [supported]: selectivity is roughly separable from conversion in the useful regime
For E2/S1 at -1.5 V, final electrochemical selectivity stayed near 0.50 across current/time contrasts while conversion varied more than tenfold (-0049, -0070, -0077, -0084). Selective yield therefore tracks conversion approximately as conversion × selectivity, with assay noise/process residuals. A predictive working model is:
- positive potential: productive terms near zero;
- negative potential: conversion rises with delivered charge (current cap × time until potential/transport limitation);
- selective yield ≈ conversion × a material/potential-dependent selectivity near 0.5 for E2/S1 at -1.5 V.
This model should not be extrapolated past conversion saturation or to untested potential extremes without allowing selectivity degradation.

## H3 [supported qualitatively]: current is a cap, with efficiency tradeoffs
Higher caps increased conversion but reduced ohmic efficiency: at E2/S1, 50 mA gave ohmic efficiency about 0.968, versus about 0.787 at 500 mA (-0070, -0077). Faradaic and transport efficiencies remained only around 0.25–0.29 and did not rise with charge. Thus more current mainly increases throughput while imposing ohmic loss; a high cap is not equivalent to proportionally improved efficiency.

## H4 [supported]: materials act through distinct pH, precipitation, transport, and ohmic factors
E0/S0 showed essentially complete precipitation and near-unity ohmic efficiency (-0014, -0021), demonstrating that conductivity cannot predict productive performance alone. E2 was acidic (normalized pH near 0.16) and essentially nonprecipitating across solvents (-0035, -0049, -0056, -0063). Solvent S1 and S3 gave numerically higher long-run yields than S2 at E2/-1.5 V/300 mA/7200 s (-0049, -0056, -0063), but those single-run differences are not cleanly resolved relative to assay uncertainty and hidden solvent residuals.

## Mechanistic account and unresolved alternatives
A minimal account is cathodic electron transfer followed by a roughly 50%-selective product-forming branch, competing with nonproductive faradaic pathways. Delivered rate is jointly bounded by current cap, potential, transport, and ohmic resistance. Precipitation can remove mobile/reactive material independently of ohmic conductivity. The data do not distinguish a single electron-transfer step from a multistep cathodic sequence, do not establish electron stoichiometry, and do not separate kinetic overpotential from potential-dependent selectivity because only sparse potentials were tested.

## Decision
Batch 12 is the best predictive/operating reference among completed batches: E2/S1, -1.5 V, 500 mA cap, 14400 s. It has the highest conversion, selective yield, and score while remaining below the safety limit and showing no precipitation. This is not necessarily the energy-optimal condition. I would change this choice if a longer/higher-cap run showed selectivity collapse or if a moderate-cap replicate gave comparable yield with materially better ohmic/energy efficiency.

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
    "cost": 0.2834640145301819,
    "electrochemical_conversion": 0.008014115504920483,
    "electrochemical_selectivity": 0.01034972071647644,
    "energy_efficiency": 0.005256945732980967,
    "faradaic_efficiency": 0.02452157624065876,
    "ohmic_efficiency": 0.9653199911117554,
    "pH_normalized": 0.23308512568473816,
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
    "cost": 0.2834640145301819,
    "electrochemical_conversion": 0.009296816773712635,
    "electrochemical_selectivity": 0.6156089305877686,
    "energy_efficiency": 0.20381268858909607,
    "faradaic_efficiency": 0.3716629445552826,
    "ohmic_efficiency": 0.9741578102111816,
    "pH_normalized": 0.2303897738456726,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.2844398021697998,
    "selective_product_yield": 0.019481411203742027,
    "transport_efficiency": 0.39791974425315857
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
      "current_mA": 300,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -2
    },
    {
      "duration_s": 3600,
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
    "cost": 0.2842400074005127,
    "electrochemical_conversion": 0.06906739622354507,
    "electrochemical_selectivity": 0.4995759129524231,
    "energy_efficiency": 0.07287335395812988,
    "faradaic_efficiency": 0.23899760842323303,
    "ohmic_efficiency": 0.9404993057250977,
    "pH_normalized": 0.231104776263237,
    "precipitation_signal": 0.9869203567504883,
    "safety_risk": 0.072194404900074,
    "score": 0.230479434132576,
    "selective_product_yield": 0.027434010058641434,
    "transport_efficiency": 0.25555452704429626
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
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -1.2
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
    "cost": 0.2834640145301819,
    "electrochemical_conversion": 0.011409304104745388,
    "electrochemical_selectivity": 0.5347200036048889,
    "energy_efficiency": 0.1638919562101364,
    "faradaic_efficiency": 0.35400375723838806,
    "ohmic_efficiency": 0.961742639541626,
    "pH_normalized": 0.2020447701215744,
    "precipitation_signal": 0.8428990840911865,
    "safety_risk": 0.072194404900074,
    "score": 0.12173384428024292,
    "selective_product_yield": 0.009349432773888111,
    "transport_efficiency": 0.32251623272895813
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
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -1.2
    },
    {
      "duration_s": 1800,
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
    "cost": 0.27646398544311523,
    "electrochemical_conversion": 0.018088029697537422,
    "electrochemical_selectivity": 0.5638753175735474,
    "energy_efficiency": 0.1978503167629242,
    "faradaic_efficiency": 0.3249015808105469,
    "ohmic_efficiency": 0.9600793123245239,
    "pH_normalized": 0.1583990603685379,
    "precipitation_signal": 0.0,
    "safety_risk": 0.072194404900074,
    "score": 0.2230256348848343,
    "selective_product_yield": 0.016625767573714256,
    "transport_efficiency": 0.3143921196460724
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
      "current_mA": 100,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": -1.2
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
    "cost": 0.2834640145301819,
    "electrochemical_conversion": 0.015623717568814754,
    "electrochemical_selectivity": 0.5390123128890991,
    "energy_efficiency": 0.2157510221004486,
    "faradaic_efficiency": 0.31292322278022766,
    "ohmic_efficiency": 0.9749907851219177,
    "pH_normalized": 0.2716825306415558,
    "precipitation_signal": 0.0023995577357709408,
    "safety_risk": 0.072194404900074,
    "score": 0.23191557824611664,
    "selective_product_yield": 0.01754188910126686,
    "transport_efficiency": 0.28823986649513245
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
      "current_mA": 300,
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
    "cost": 0.3115600049495697,
    "electrochemical_conversion": 0.15922604501247406,
    "electrochemical_selectivity": 0.49603506922721863,
    "energy_efficiency": 0.14888037741184235,
    "faradaic_efficiency": 0.2681582272052765,
    "ohmic_efficiency": 0.9021043181419373,
    "pH_normalized": 0.1558038890361786,
    "precipitation_signal": 0.0,
    "safety_risk": 0.09559440612792969,
    "score": 0.2686014175415039,
    "selective_product_yield": 0.08146102726459503,
    "transport_efficiency": 0.27155858278274536
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
      "current_mA": 300,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -1.5
    },
    {
      "duration_s": 7200,
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
    "cost": 0.330159991979599,
    "electrochemical_conversion": 0.137367382645607,
    "electrochemical_selectivity": 0.44007691740989685,
    "energy_efficiency": 0.12626446783542633,
    "faradaic_efficiency": 0.2624475955963135,
    "ohmic_efficiency": 0.8598524928092957,
    "pH_normalized": 0.16995058953762054,
    "precipitation_signal": 0.00031451715040020645,
    "safety_risk": 0.1135944053530693,
    "score": 0.2373490333557129,
    "selective_product_yield": 0.042613208293914795,
    "transport_efficiency": 0.25595223903656006
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
      "current_mA": 300,
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
    "cost": 0.3211599886417389,
    "electrochemical_conversion": 0.14084051549434662,
    "electrochemical_selectivity": 0.46661174297332764,
    "energy_efficiency": 0.1612696349620819,
    "faradaic_efficiency": 0.2463928461074829,
    "ohmic_efficiency": 0.9200315475463867,
    "pH_normalized": 0.16795013844966888,
    "precipitation_signal": 0.008188718929886818,
    "safety_risk": 0.12619440257549286,
    "score": 0.26369985938072205,
    "selective_product_yield": 0.08513839542865753,
    "transport_efficiency": 0.26722413301467896
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
      "current_mA": 50,
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
    "cost": 0.3007600009441376,
    "electrochemical_conversion": 0.038440559059381485,
    "electrochemical_selectivity": 0.49943405389785767,
    "energy_efficiency": 0.1480780839920044,
    "faradaic_efficiency": 0.25635820627212524,
    "ohmic_efficiency": 0.9676070213317871,
    "pH_normalized": 0.15380604565143585,
    "precipitation_signal": 0.0,
    "safety_risk": 0.09559440612792969,
    "score": 0.10266590863466263,
    "selective_product_yield": 0.00864530261605978,
    "transport_efficiency": 0.257707804441452
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
    "cost": 0.32019999623298645,
    "electrochemical_conversion": 0.27644798159599304,
    "electrochemical_selectivity": 0.5043148994445801,
    "energy_efficiency": 0.1753680258989334,
    "faradaic_efficiency": 0.2841516137123108,
    "ohmic_efficiency": 0.7870184183120728,
    "pH_normalized": 0.15479108691215515,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.09559440612792969,
    "score": 0.2967374622821808,
    "selective_product_yield": 0.1364913284778595,
    "transport_efficiency": 0.29133155941963196
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
      "potential_V": -1.5
    },
    {
      "duration_s": 14400,
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
    "cost": 0.33480000495910645,
    "electrochemical_conversion": 0.5095835328102112,
    "electrochemical_selectivity": 0.49559301137924194,
    "energy_efficiency": 0.15385489165782928,
    "faradaic_efficiency": 0.24783480167388916,
    "ohmic_efficiency": 0.800366997718811,
    "pH_normalized": 0.15531140565872192,
    "precipitation_signal": 0.0,
    "safety_risk": 0.09559440612792969,
    "score": 0.353304922580719,
    "selective_product_yield": 0.2808462083339691,
    "transport_efficiency": 0.2690597474575043
  }
}
```

## K1 封存报告

## Mechanistic interpretation

### 1. Empirical operating domain

All batches used 0.020 mol of limiting reagent in 0.040 L of solvent. The campaign explored potentials from −2.0 to +1.2 V, current caps from 50 to 500 mA, electrolysis times from 1,800 to 14,400 s, all four electrolytes, and all four solvents, although not as a complete factorial design. Safety risk remained below the specified 0.65 limit in every batch; observed values ranged from about 0.072 for S0 to 0.126 for S3.

My central explanation is that this is a cathodic, charge-driven conversion with three coupled layers:

1. Applied potential determines whether the productive electron-transfer channel is accessible.
2. Current cap and time determine delivered charge and therefore conversion, until kinetic, ohmic, transport, or substrate-depletion limits intervene.
3. Electrolyte and solvent modify pH, precipitation, transport, interfacial kinetics, and resistance. These factors affect both how much current can be used productively and how the converted material partitions between target and competing products.

### 2. Polarity and activation of the productive pathway

The strongest mechanistic observation is the matched polarity contrast between batches 1 and 2. Both used S0/E0, 100 mA, and 1,800 s at the same loading. Batch 1 used +1.2 V; its intermediate UV–visible estimates gave essentially zero faradaic, transport, and energy efficiency, and its final assay gave selective product yield 0, electrochemical conversion 0.0080, and selectivity 0.0103. Batch 2 used −1.2 V; its intermediate estimates were faradaic efficiency 0.344, transport efficiency 0.387, and energy efficiency 0.252. Its final assay gave selective product yield 0.0195 and selectivity 0.616.

The conversion estimates in both low-signal final assays were close to the approximately 0.01 conversion uncertainty, and the batch-2 yield was not numerically consistent with conversion multiplied by selectivity. I therefore do not interpret their exact low-level values literally. The combined spectral and processed-channel contrast nevertheless supports a polarity-specific cathodic pathway rather than a sign-symmetric thermal or mixing effect.

A minimal reaction scheme is:

R + e− ⇌ R*−

R*− → P_target

R*− → P_side or other nonproductive sinks

Positive potential does not appreciably populate the productive reduced intermediate in the tested range. This scheme is conceptual: neither the number of electrons nor the existence of a freely diffusing radical intermediate was measured.

### 3. Charge–conversion relationship

For a fixed material combination and potential, a useful first approximation is

Q_cap = I_cap t,

X ≈ min[X_max, k_Q η_delivered Q_cap],

where X is conversion, η_delivered represents the combined kinetic, transport, and ohmic limitations, and k_Q includes reagent loading and an unknown electron stoichiometry.

Batches 7, 10, 11, and 12 provide the cleanest test because all used E2/S1 at −1.5 V:

- Batch 10: 50 mA, 7,200 s; conversion 0.0384, selectivity 0.499, yield 0.00865.
- Batch 7: 300 mA, 7,200 s; conversion 0.159, selectivity 0.496, yield 0.0815.
- Batch 11: 500 mA, 7,200 s; conversion 0.276, selectivity 0.504, yield 0.136.
- Batch 12: 500 mA, 14,400 s; conversion 0.510, selectivity 0.496, yield 0.281.

Conversion rose approximately with current cap at fixed time and nearly doubled when time doubled at 500 mA. Thus the system had not reached a strong conversion plateau by batch 12. The trend is consistent with delivered charge controlling conversion over this domain. It does not prove exact linearity: current was reported as a configured cap rather than a directly measured time-resolved current, and only one observation was obtained at each condition.

In pseudocode, my working conversion model would be:

if potential is not sufficiently cathodic:
    productive_rate ≈ 0
else:
    kinetic_drive = f(overpotential)
    current_used = min(current_cap, kinetic_limit, transport_limit)
    conversion_rate ∝ current_used × faradaic_efficiency
    conversion = saturating_integral(conversion_rate, time, remaining_reagent)

The effective overpotential should depend on applied potential plus the declared solvent and electrolyte standard-potential shifts and unknown fixed world residuals. Because only a few potentials were used and potential was often confounded with current and time, I cannot identify the functional form of f(overpotential) or a formal onset potential.

### 4. Selectivity and productive yield

In the E2/S1, −1.5 V series, electrochemical selectivity remained remarkably stable near 0.50 while conversion varied from 0.038 to 0.510. This suggests that, within that domain, the target-forming and side-product branches have similar dependence on current and time. A useful model is therefore

Y_target ≈ X × S,

S ≈ 0.50 for E2/S1 near −1.5 V,

with channel-specific measurement noise and possible process residuals.

This relationship worked closely for batches 7 and 11. It was less exact at the low-yield batch 10 and at batch 12: batch 12 had X × S ≈ 0.253 versus measured yield 0.281. The assay channels have independent stated uncertainties, so yield should not be forced algebraically to equal the product of separately calibrated conversion and selectivity estimates. The discrepancies could also reflect latent mass-balance or species-mapping effects, but those were not identifiable from public observations.

Batch 3, using E0/S0 at −2.0 V, 300 mA for 3,600 s, gave conversion 0.0691, selectivity 0.500, and yield 0.0274. Compared with the shorter, less strongly driven E0 experiments, this shows that stronger overall drive can raise conversion. However, because potential, current, and time all changed together, batch 3 cannot isolate a pure potential effect or establish that −2.0 V is intrinsically better than −1.5 V. Excessively negative potentials might eventually increase side reactions or degradation, but this remains a plausible extrapolation rather than an observed result.

### 5. Ohmic, transport, and faradaic coupling

The current-cap series reveals a throughput–efficiency tradeoff. In E2/S1 at −1.5 V and 7,200 s, final ohmic efficiency fell from 0.968 at 50 mA in batch 10 to 0.902 at 300 mA in batch 7 and 0.787 at 500 mA in batch 11. Conversion nevertheless increased strongly. This is consistent with increasing resistive polarization at high current: a larger absolute reaction rate is obtained even though a smaller fraction of the applied electrical effort is retained as useful cell potential.

Faradaic and transport efficiencies were much less responsive than conversion. Across the long E2/S1 runs they were generally around 0.25–0.29. A separable representation is

η_energy ≈ η_ohmic × η_transport × η_faradaic × C,

where C may include normalization and kinetic terms used by the benchmark. I would not assert an exact product because the observed energy-efficiency values do not establish that identity. Mechanistically, however, the three efficiencies describe distinct losses:

- η_ohmic decreases with cell current and effective resistance.
- η_transport depends on diffusivity, diffusion-layer thickness, concentration, and current demand.
- η_faradaic represents competition between target-related electron transfer and nonproductive charge consumption.

The fixed fixture means electrode area, gap, and base resistance were common to all batches in this campaign. They are therefore unidentifiable constants here and should not be mistaken for material properties.

### 6. Electrolyte effects, pH, and precipitation

The electrolyte screen at S0, −1.2 V, 100 mA, and 1,800 s was conducted in batches 2, 4, 5, and 6:

- E0, batch 2: precipitation signal 1.000; pH-normalized 0.230; yield 0.0195.
- E1, batch 4: precipitation 0.843; pH-normalized 0.202; yield 0.00935.
- E2, batch 5: precipitation 0; pH-normalized 0.158; yield 0.0166.
- E3, batch 6: precipitation 0.0024; pH-normalized 0.272; yield 0.0175.

These results broadly follow the nominal dossier: E2 is the most acidic and has weak precipitation tendency, while E0 has a strong precipitation tendency. Batch 3 also retained a precipitation signal of 0.987 under stronger E0 electrolysis. Thus precipitation is a persistent electrolyte-dependent state variable, not merely low-current measurement noise.

E0 also produced very high ohmic efficiency, approximately 0.94–0.97 in its final assays, despite nearly complete precipitation. Consequently, bulk conductivity alone cannot rank overall performance. A conductive medium can still lose reactive or supporting species through precipitation or suffer poor mass transport. A schematic coupling is

mobile concentration = total concentration × (1 − precipitated fraction),

transport limit ∝ mobile concentration × diffusivity / diffusion-layer thickness.

The exact precipitating species and whether precipitation removes reagent, product, or only supporting salt are hidden. Therefore this equation describes a plausible mechanism, not an identified mass balance.

E2 was selected for the later charge-response series because it consistently suppressed precipitation. Its low normalized pH may also shift the reduction potential, protonate an intermediate, or change product branching. The campaign did not independently vary acid concentration within an electrolyte, so direct proton involvement is not identifiable.

### 7. Solvent effects

Batches 7–9 compared solvents at E2, −1.5 V, 300 mA, and 7,200 s:

- S1, batch 7: conversion 0.159, selectivity 0.496, yield 0.0815, ohmic efficiency 0.902, transport efficiency 0.272.
- S2, batch 8: conversion 0.137, selectivity 0.440, yield 0.0426, ohmic efficiency 0.860, transport efficiency 0.256.
- S3, batch 9: conversion 0.141, selectivity 0.467, yield 0.0851, ohmic efficiency 0.920, transport efficiency 0.267.

S1 and S3 gave numerically higher selective yield than S2, whereas their conversion values were relatively close. This suggests that solvent can affect product branching or the yield-channel response in addition to conductivity. However, each condition was measured once, yield uncertainty was about 0.01, and the batch-9 yield exceeds conversion multiplied by the separately reported selectivity. I therefore regard the precise S1-versus-S3 ordering as unresolved. S0 was not included in this matched long-duration solvent comparison, so a complete solvent ranking is unjustified.

Possible solvent mechanisms include shifts in effective standard potential, altered proton activity, solvation of the reduced intermediate, differences in diffusivity and double-layer capacitance, and suppression or enhancement of precipitation. These contributions are correlated in the supplied solvent profiles and cannot be separated with the available design.

### 8. Experiments that changed the explanation

Batches 1 and 2 established cathodic polarity as the primary qualitative rule. Batch 3 showed that stronger combined drive could produce appreciably more conversion but also demonstrated that high conductivity did not eliminate the E0 precipitation problem. Batches 4–6 separated electrolyte-controlled pH and precipitation from simple ohmic behavior and motivated the use of E2.

Batches 7–9 showed that solvent changes could alter selective yield even when conversion and efficiency measures were broadly similar. Most importantly, batches 10–12 transformed the account from a qualitative material ranking into a quantitative charge-driven model: increasing current cap and duration produced systematic conversion increases while selectivity stayed close to 0.50. Batch 12, with E2/S1 at −1.5 V, 500 mA, and 14,400 s, supplied the highest observed conversion (0.510), yield (0.281), and public score (0.353), with zero measured precipitation and safety risk 0.0956.

### 9. Scope, limitations, and alternatives

The proposed model is supported only over the tested concentration, volume, fixture, and material labels. It should not be extrapolated linearly beyond 14,400 s or 500 mA because substrate depletion, transport limitation, heating, electrode changes, or selectivity loss may eventually cause saturation or decline. No temperature series, loading series, volume series, or true replicate series was performed.

Several factors remain unidentifiable:

- electron stoichiometry and the identity or lifetime of intermediates;
- actual current as a function of time versus the configured cap;
- kinetic onset potential and exchange-current behavior;
- the composition of precipitate and side products;
- whether pH acts mechanistically or merely covaries with electrolyte identity;
- hidden world-specific solvent, transport, and interfacial residuals;
- electrode area, gap, resistance, and other fixed fixture constants;
- whether final-assay channel discrepancies are entirely measurement noise or include latent mass-balance behavior.

A plausible alternative is that the apparent charge law is actually a potential-controlled rate with the current cap constraining it over the tested range. Another is that precipitation changes only supporting-electrolyte conductivity rather than directly removing reactive material. The data favor a cathodic, approximately charge-controlled model with separable branching, but they do not uniquely identify a molecular mechanism.

Overall, the most defensible predictive account is: require negative potential; calculate conversion primarily from usable charge with corrections for potential, transport, and ohmic loss; treat selectivity as an approximately material- and potential-specific branching fraction near 0.50 for E2/S1 at −1.5 V; and include electrolyte-dependent pH and precipitation as separate state variables rather than inferring performance from conductivity alone.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific prior, hidden response law, or claimed ground-truth mechanism was supplied. The only prior information was the public nominal material dossier and general instrument/task contracts. I treated the dossier as qualitative prior evidence because it explicitly allowed fixed world residuals and possible misindexing.

Supported claims:
- Cathodic polarity is required in the tested domain. The matched S0/E0 experiments were decisive: batch 1 at +1.2 V had essentially zero productive UV–visible response and zero final selective yield, whereas batch 2 at −1.2 V showed nonzero faradaic and transport efficiencies and final yield about 0.019. This changed the initial polarity hypothesis into the strongest qualitative conclusion of the campaign.
- Conversion is approximately charge-controlled over the E2/S1, −1.5 V domain. At 7,200 s, conversion rose from 0.038 in batch 10 at 50 mA to 0.159 in batch 7 at 300 mA and 0.276 in batch 11 at 500 mA. Doubling time at 500 mA raised conversion to 0.510 in batch 12. These observations changed my account from a generic potential-driven reaction to a working delivered-charge model.
- Selectivity was approximately separable from conversion for E2/S1 at −1.5 V. Batches 7, 10, 11, and 12 retained selectivity near 0.50 while conversion varied more than tenfold.
- Electrolyte-dependent precipitation and pH are distinct from ohmic performance. E0 gave precipitation near 1 in batches 2 and 3 despite high ohmic efficiency. E2 and E3 largely suppressed precipitation in batches 5 and 6. This contradicted any simple overall ranking based only on conductivity.
- Higher current involved an ohmic tradeoff. In the E2/S1 series, final ohmic efficiency declined from about 0.968 in batch 10 at 50 mA to 0.787 in batch 11 at 500 mA even though conversion increased.

Contradicted or narrowed claims:
- The preliminary expectation that nominal conductivity might predict energy efficiency or overall performance was too simple. E0 was highly ohmically efficient but strongly precipitating, while energy efficiency did not follow a monotonic conductivity ranking.
- A high-current plateau was not observed. Batches 10–12 continued to show substantial conversion gains with current and time. Thus the prior expectation of eventual saturation remains physically plausible but was not reached in the campaign.
- A clean solvent ranking was not established. Batches 7–9 gave numerically different yields for S1, S2, and S3, but conversion was fairly similar, each condition was observed once, and independently calibrated yield, conversion, and selectivity channels were not always algebraically consistent.

Untested or unresolved claims:
- The molecular identity, lifetime, and electron stoichiometry of a reduced intermediate were not measured.
- A potential threshold or kinetic overpotential law was not identified because potential was sparsely sampled and often confounded with current and duration.
- The conjecture that excessively negative potential or excessive charge eventually lowers selectivity was not tested cleanly. Batch 3 used stronger potential, current, and duration simultaneously.
- It remains unknown whether precipitation removes reactant, product, or only supporting electrolyte.
- Because actual current versus time was not observed, the statement that the configured current was fully delivered remains untested.

2. One additional discriminating experiment

I would run E2/S1 at −1.5 V with the original 0.020 mol in 0.040 L loading, a 250 mA current cap, and 14,400 s duration, followed by the same final assay. This supplies the same nominal charge, 3,600 C, as batch 11 at 500 mA for 7,200 s, while changing instantaneous current and duration by factors of two.

My leading charge-controlled explanation predicts conversion and selectivity broadly similar to batch 11: conversion near 0.276 and selectivity near 0.50, but with better ohmic efficiency at the lower current. Agreement within process and assay uncertainty would strengthen the claim that integrated usable charge is the main conversion coordinate.

If conversion were substantially lower than batch 11, I would infer that high instantaneous current, current-dependent interfacial kinetics, or another rate effect matters beyond integrated charge. If conversion were substantially higher, I would infer that lower-current operation avoids ohmic or transport losses sufficiently to deliver charge more productively, or that residence time contributes independently. A major selectivity change at matched nominal charge would reject the simple separable branching model and indicate current- or time-dependent pathway competition. Interpretation would still be limited unless actual delivered current were measured.

3. Unused evidence, reliability, and effect of the goal

The detailed raw spectral artifacts were not analyzed beyond their public peak summaries and processed estimates. Raw replicate traces, baselines, peak shapes, and channel-specific mass-balance information therefore did not contribute to the model. The intermediate pH and UV–visible measurements were used qualitatively, but I did not fit their full spectra or quantitatively reconcile them with final-assay channels. Cost, small temperature changes during solvent addition, sample-consumption details, and cumulative process cost were also not mechanistically modeled. Nominal diffusivity, capacitance, conductivity, acid, and solubility properties were used as qualitative context rather than fitted covariates because the experimental design was too sparse and correlated to identify their separate coefficients.

The least reliable predictions are the cathodic −0.8 V predictions, because −0.8 V was never tested and the response near onset may be highly nonlinear. Q07 and Q09 additionally rely on extrapolating electrolyte or solvent potential shifts from unmatched conditions. Q11 combines high current with strongly precipitating E0, a combination not directly tested. Exact near-zero values for all positive-potential predictions are also uncertain because clipped assay noise can generate small positive processed estimates, although their qualitative prediction of negligible productive chemistry is more reliable. All predictions use a new 0.012 mol/0.025 L scale, so the assumed transfer from the campaign’s 0.020 mol/0.040 L loading is another uncertainty.

The batch-12 recommendation is reliable only as the best observed operating point, not as a proven optimum. It had the highest measured conversion, yield, and score, but it was unreplicated; longer operation, other high-charge solvents, and energy-optimal conditions were not tested. The precise superiority of S1 over S3 is especially uncertain.

The assigned mechanism-discovery goal materially affected evidence collection. I prioritized a matched polarity contrast, an electrolyte screen, a solvent screen, and current/time contrasts rather than repeatedly optimizing the public score. This broadened mechanistic coverage but left few replicates and sparse potential sampling. I found no direct conflict between the research goal and safety or resource constraints, but the breadth-versus-replication tradeoff reduced confidence in fine material rankings and quantitative prediction intervals.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.56,
        "lower80": 0.35,
        "upper80": 0.7
      },
      "energy_efficiency": {
        "estimate": 0.22,
        "lower80": 0.1,
        "upper80": 0.34
      },
      "faradaic_efficiency": {
        "estimate": 0.34,
        "lower80": 0.23,
        "upper80": 0.45
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.03,
        "lower80": 0,
        "upper80": 0.15
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.36,
        "lower80": 0.25,
        "upper80": 0.47
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.022
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0,
        "upper80": 0.025
      },
      "faradaic_efficiency": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.025
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.04
      },
      "selective_product_yield": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.012
      },
      "transport_efficiency": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.025
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.56,
        "lower80": 0.43,
        "upper80": 0.67
      },
      "energy_efficiency": {
        "estimate": 0.21,
        "lower80": 0.11,
        "upper80": 0.31
      },
      "faradaic_efficiency": {
        "estimate": 0.33,
        "lower80": 0.24,
        "upper80": 0.42
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.28,
        "lower80": 0.08,
        "upper80": 0.36
      },
      "selective_product_yield": {
        "estimate": 0.023,
        "lower80": 0.005,
        "upper80": 0.055
      },
      "transport_efficiency": {
        "estimate": 0.35,
        "lower80": 0.26,
        "upper80": 0.44
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.022
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0,
        "upper80": 0.025
      },
      "faradaic_efficiency": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.025
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.04
      },
      "selective_product_yield": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.012
      },
      "transport_efficiency": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.025
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.54,
        "lower80": 0.41,
        "upper80": 0.65
      },
      "energy_efficiency": {
        "estimate": 0.19,
        "lower80": 0.1,
        "upper80": 0.29
      },
      "faradaic_efficiency": {
        "estimate": 0.33,
        "lower80": 0.24,
        "upper80": 0.42
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.27,
        "lower80": 0.1,
        "upper80": 0.35
      },
      "selective_product_yield": {
        "estimate": 0.027,
        "lower80": 0.008,
        "upper80": 0.065
      },
      "transport_efficiency": {
        "estimate": 0.31,
        "lower80": 0.22,
        "upper80": 0.4
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.022
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0,
        "upper80": 0.025
      },
      "faradaic_efficiency": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.025
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.04
      },
      "selective_product_yield": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.012
      },
      "transport_efficiency": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.025
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.54,
        "lower80": 0.42,
        "upper80": 0.65
      },
      "energy_efficiency": {
        "estimate": 0.23,
        "lower80": 0.13,
        "upper80": 0.33
      },
      "faradaic_efficiency": {
        "estimate": 0.31,
        "lower80": 0.22,
        "upper80": 0.4
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.28,
        "lower80": 0.14,
        "upper80": 0.36
      },
      "selective_product_yield": {
        "estimate": 0.038,
        "lower80": 0.012,
        "upper80": 0.085
      },
      "transport_efficiency": {
        "estimate": 0.29,
        "lower80": 0.2,
        "upper80": 0.38
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.022
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0,
        "upper80": 0.025
      },
      "faradaic_efficiency": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.025
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.04
      },
      "selective_product_yield": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.012
      },
      "transport_efficiency": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.025
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.52,
        "lower80": 0.38,
        "upper80": 0.64
      },
      "energy_efficiency": {
        "estimate": 0.14,
        "lower80": 0.06,
        "upper80": 0.24
      },
      "faradaic_efficiency": {
        "estimate": 0.33,
        "lower80": 0.23,
        "upper80": 0.43
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.26,
        "lower80": 0.08,
        "upper80": 0.34
      },
      "selective_product_yield": {
        "estimate": 0.027,
        "lower80": 0.006,
        "upper80": 0.075
      },
      "transport_efficiency": {
        "estimate": 0.33,
        "lower80": 0.23,
        "upper80": 0.43
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.022
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0,
        "upper80": 0.025
      },
      "faradaic_efficiency": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.025
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.04
      },
      "selective_product_yield": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.012
      },
      "transport_efficiency": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.025
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.5,
        "lower80": 0.38,
        "upper80": 0.6
      },
      "energy_efficiency": {
        "estimate": 0.09,
        "lower80": 0.035,
        "upper80": 0.17
      },
      "faradaic_efficiency": {
        "estimate": 0.25,
        "lower80": 0.17,
        "upper80": 0.34
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.26,
        "lower80": 0.19,
        "upper80": 0.35
      },
      "selective_product_yield": {
        "estimate": 0.095,
        "lower80": 0.035,
        "upper80": 0.18
      },
      "transport_efficiency": {
        "estimate": 0.24,
        "lower80": 0.16,
        "upper80": 0.33
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.022
      },
      "energy_efficiency": {
        "estimate": 0.004,
        "lower80": 0,
        "upper80": 0.022
      },
      "faradaic_efficiency": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.025
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.04
      },
      "selective_product_yield": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.012
      },
      "transport_efficiency": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.025
      }
    }
  ],
  "rationale": "The matched campaign polarity test made negative potential productive and positive potential effectively inactive, so all +0.8 V predictions remain near the assay floor. For cathodic batches I scaled conversion and yield approximately with charge per mole, allowed E1, E3, and S2 potential shifts to make reduction easier than E0/S0 at −0.8 V, and retained the observed roughly 0.5–0.56 selectivity. The 500 mA case receives higher yield but lower faradaic, transport, and energy efficiency from current-dependent losses. Intervals include assay noise, sparse potential coverage, precipitation/material residuals, and uncertainty from changing the loading and volume."
}
```
