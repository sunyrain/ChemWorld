# repeat-03/EC-W05-B12-discovery-E-MisIndexed

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-03\EC-W05-B12-discovery-E-MisIndexed\participant\discovery-E-MisIndexed

## 同期笔记

### v1 · 公开事件 0

# Electrochemical hypothesis notebook

## Prior expectations (before physical experiments)

**H1 [tentative] — signed overpotential response.** At fixed loading and materials, productive conversion should rise with the magnitude of potential in one productive sign after an onset, then selectivity/efficiency may fall at more extreme magnitude from side reactions. The opposite sign may be weak or differently selective. Test by paired signs and at least two magnitudes.

**H2 [tentative] — charge/time saturation.** At fixed potential and material, longer electrolysis or a larger current cap should increase conversion only until reagent, transport, or kinetic saturation; current_mA is only a cap, so delivered charge may cease to scale with it. Test short/long duration and low/high caps.

**H3 [tentative] — material roles.** Nominal conductivity should favor ohmic efficiency, while diffusivity/layer thickness should affect transport; potential shifts should move apparent onset, and proton activity/precipitation may trade against selectivity. Because hidden fixed residuals and possible dossier misindexing exist, comparative assays are authoritative.

Design: use a common 0.020 mol reagent in 0.040 L solvent where legal, broad material/potential/time screening, and reserve repeats/targeted contrasts to separate curvature from noise. Intermediate UV-vis will be used once per batch for corroborating efficiency signals; final assay remains primary.

### v2 · 公开事件 28

# Electrochemical hypothesis notebook

## Prior expectations

H1 anticipated a signed, peaked potential response; H2 anticipated charge/time saturation; H3 anticipated material-dependent transport, ohmic and interfacial behavior. Common baseline is 0.020 mol in 0.040 L.

## H1 [supported in direction and non-monotonic efficiency; productive yield still unresolved]

At S0/E0, 100 mA cap, 600 s, the UV-vis efficiencies are strongly potential dependent: +1.0 V gives high faradaic/transport/ohmic efficiencies (event runner-operation-0005), while −1.0 V sharply lowers faradaic and transport but not ohmic efficiency (runner-operation-0012), and +2.0 V collapses faradaic/transport and final selectivity (runner-operation-0026 and runner-operation-0028). +0.5 V is intermediate (runner-operation-0019). This supports a productive positive-potential window with an optimum near +1 V rather than dependence on |V| alone.

Final selective-product yield is near the assay floor in all four and is noisy/non-monotone (runner-operation-0007, -0014, -0021, -0028), so it does not yet establish a yield optimum. The zero reported conversion with nonzero yield at −1 and +2 V cautions against literal ratio calculations at the detection boundary.

Testable consequence: under longer time or larger delivered charge near +1 V, conversion/yield should rise while the efficiency ordering across potentials persists. A failure of yield to rise would favor a hidden kinetic/loading limitation or an assay-floor explanation.

### v3 · 公开事件 56

# Electrochemical hypothesis notebook

## H1 [supported in efficiency response; yield near detection floor]
At S0/E0, 600 s, potential response is asymmetric and peaked: +1 V has high efficiencies (runner-operation-0005), −1 V loses faradaic/transport efficiency (runner-operation-0012), +0.5 V is intermediate (runner-operation-0019), and +2 V collapses faradaic/transport and selectivity (runner-operation-0026, -0028). This favors a positive-potential window rather than |V| scaling. Product-yield comparisons remain noisy near zero.

## H2 [partly supported, quantitative form unresolved]
At +1 V S0/E0, the 1800 s final assay has conversion 0.0407 and yield 0.0244 (runner-operation-0056), above the corresponding 600 s baseline values 0.0234 and 0.00110 (runner-operation-0007), while 60 s gave 0.0119 and 0.00881 (runner-operation-0049). The broadly increasing conversion with time supports charge accumulation, but yield is not monotone at the short/baseline pair and assay noise is material at these low signals. Treat time scaling as saturating/approximately increasing, not established linearity.

Changing only the current cap at 600 s from 20 to 500 mA leaves efficiencies near unity; final yields differ (0.0115 vs 0.0162; runner-operation-0035 and -0042) but the magnitude is comparable to run-to-run scatter seen across time conditions. This is consistent with potential control delivering less than the cap, but a cap effect is unresolved without replication.

## H3 [awaiting tests]
Nominal material-property effects remain to be tested. Strong precipitation signal near 1 across S0/E0 conditions may obscure proton/precipitation coupling.

Next consequence: material changes should alter transport/ohmic efficiency reproducibly more than the current-cap contrast if the dossier descriptors are mechanistically useful.

### v4 · 公开事件 84

# Electrochemical hypothesis notebook

## H1 [supported in the tested S0/E0 scope]
At 0.020 mol/0.040 L and 600 s, response is signed and non-monotonic in potential. +1 V gives high faradaic and transport efficiencies (runner-operation-0005); −1 V lowers both while retaining high ohmic efficiency (runner-operation-0012); +0.5 V is intermediate (runner-operation-0019); +2 V collapses faradaic/transport efficiency and final selectivity (runner-operation-0026, -0028). Thus a positive-potential window near +1 V is favored, not a function of |V| alone. An empirical predictive account should use signed potential relative to a material-dependent onset plus a high-overpotential penalty.

## H2 [supported for time; cap effect unresolved]
At +1 V S0/E0, conversion increases broadly from 60 s (0.0119, runner-operation-0049) through 600 s (0.0234, runner-operation-0007) to 1800 s (0.0407, runner-operation-0056), consistent with charge accumulation and eventual saturation. Yield is noisy at the assay floor, but the 1800 s condition also gives the largest tested value in this time series (0.0244). A saturating time response is more defensible than linear extrapolation.

At 600 s, 20 and 500 mA caps both retain near-unity final faradaic/transport/ohmic efficiencies (runner-operation-0035, -0042). Their yield difference is comparable to scatter among nearby low-signal runs. Interpret current_mA as a ceiling: predictions should weakly depend on the cap once it exceeds delivered current, but may decline at very low caps; the location of that regime was not resolved.

## H3 [supported qualitatively; solvent/electrolyte interactions unresolved]
Material changes cause large, structured effects. Relative to S0/E0 (runner-operation-0007), changing only solvent to S1 lowers faradaic/transport efficiencies and selectivity while maintaining high ohmic efficiency (runner-operation-0063). Changing only electrolyte to E1 moderately lowers transport/faradaic efficiency and substantially lowers precipitation and pH-normalized signal (runner-operation-0070). The matched S2/E2 system has still lower efficiencies and essentially no precipitation (runner-operation-0077); S3/E3 has the weakest faradaic/transport efficiencies, no precipitation, higher pH-normalized signal, and near-zero reported conversion (runner-operation-0084). Ohmic efficiency remains high throughout, so nominal bulk conductivity alone does not control performance; interface/transport and potential-shift terms are needed.

Because S2/E2 and S3/E3 change solvent and electrolyte together, their separate contributions and interactions cannot be identified. Fixed hidden material residuals and single-run assay noise also limit precision. Nevertheless, the efficiency ordering is much larger than UV-vis noise and broadly corroborated by final assays.

## Working predictive model and decision
Use a bounded product of: (i) a signed-potential activation centered at a material-shifted onset, (ii) a high-positive-potential deactivation/selectivity penalty, (iii) saturating time/charge uptake, (iv) a current-cap limiter only when binding, and (v) material-specific faradaic and transport factors. Treat ohmic efficiency as comparatively insensitive under tested conditions. Avoid literal yield/selectivity ratios when conversion is reported at zero.

For an operating recommendation among completed batches, prefer batch 8 (S0/E0, +1 V, 100 mA cap, 1800 s): it combines the highest observed campaign score with the clearest conversion/yield improvement while retaining high selectivity and efficiencies. This is an empirical choice, not proof of a global optimum.

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
    "cost": 0.2828400135040283,
    "electrochemical_conversion": 0.023405056446790695,
    "electrochemical_selectivity": 0.998518168926239,
    "energy_efficiency": 0.9631397724151611,
    "faradaic_efficiency": 1.0,
    "ohmic_efficiency": 0.9602119326591492,
    "pH_normalized": 0.23308512568473816,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.032431427389383316,
    "selective_product_yield": 0.001095070969313383,
    "transport_efficiency": 0.9858177900314331
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
    "cost": 0.2828400135040283,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.6434827446937561,
    "energy_efficiency": 0.2848791182041168,
    "faradaic_efficiency": 0.40667814016342163,
    "ohmic_efficiency": 0.9690497517585754,
    "pH_normalized": 0.2303897738456726,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.20308656990528107,
    "selective_product_yield": 0.012986360117793083,
    "transport_efficiency": 0.43293496966362
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
      "potential_V": 0.5
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
    "electrochemical_conversion": 0.006868478376418352,
    "electrochemical_selectivity": 0.8744789361953735,
    "energy_efficiency": 0.8271051645278931,
    "faradaic_efficiency": 0.7713616490364075,
    "ohmic_efficiency": 0.9251751899719238,
    "pH_normalized": 0.231104776263237,
    "precipitation_signal": 0.9869203567504883,
    "safety_risk": 0.072194404900074,
    "score": 0.004817426670342684,
    "selective_product_yield": 0.0001921776420203969,
    "transport_efficiency": 0.7879185676574707
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
    "cost": 0.28308001160621643,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.02824951522052288,
    "ohmic_efficiency": 0.9833056330680847,
    "pH_normalized": 0.23041419684886932,
    "precipitation_signal": 0.9876685738563538,
    "safety_risk": 0.072194404900074,
    "score": 0.0032494785264134407,
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
      "solvent": 0,
      "volume_L": 0.04
    },
    {
      "current_mA": 20,
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
    "cost": 0.2826479971408844,
    "electrochemical_conversion": 0.006526156794279814,
    "electrochemical_selectivity": 0.9944328665733337,
    "energy_efficiency": 0.9540458917617798,
    "faradaic_efficiency": 1.0,
    "ohmic_efficiency": 0.9919342994689941,
    "pH_normalized": 0.23537498712539673,
    "precipitation_signal": 0.9869949817657471,
    "safety_risk": 0.072194404900074,
    "score": 0.3421466648578644,
    "selective_product_yield": 0.011505601927638054,
    "transport_efficiency": 0.990170955657959
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
    "cost": 0.2826921045780182,
    "electrochemical_conversion": 0.008057958446443081,
    "electrochemical_selectivity": 0.9924110770225525,
    "energy_efficiency": 0.9712506532669067,
    "faradaic_efficiency": 1.0,
    "ohmic_efficiency": 0.9881584048271179,
    "pH_normalized": 0.2320990413427353,
    "precipitation_signal": 0.9976252913475037,
    "safety_risk": 0.072194404900074,
    "score": 0.4837644100189209,
    "selective_product_yield": 0.0161740779876709,
    "transport_efficiency": 0.9893726110458374
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
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 60,
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
    "cost": 0.2826240062713623,
    "electrochemical_conversion": 0.01189231127500534,
    "electrochemical_selectivity": 0.9860008955001831,
    "energy_efficiency": 0.9579402208328247,
    "faradaic_efficiency": 0.9921573996543884,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.23111364245414734,
    "precipitation_signal": 0.9826673865318298,
    "safety_risk": 0.072194404900074,
    "score": 0.26176583766937256,
    "selective_product_yield": 0.008813085965812206,
    "transport_efficiency": 0.9955577850341797
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
    "cost": 0.28332000970840454,
    "electrochemical_conversion": 0.040745195001363754,
    "electrochemical_selectivity": 0.9826774597167969,
    "energy_efficiency": 0.9533127546310425,
    "faradaic_efficiency": 0.9891111254692078,
    "ohmic_efficiency": 0.9861299991607666,
    "pH_normalized": 0.229416161775589,
    "precipitation_signal": 0.995540201663971,
    "safety_risk": 0.072194404900074,
    "score": 0.5976349711418152,
    "selective_product_yield": 0.024388615041971207,
    "transport_efficiency": 0.9826157689094543
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
    "cost": 0.2988399863243103,
    "electrochemical_conversion": 0.011196622624993324,
    "electrochemical_selectivity": 0.7761551737785339,
    "energy_efficiency": 0.787880003452301,
    "faradaic_efficiency": 0.8338663578033447,
    "ohmic_efficiency": 0.9929165244102478,
    "pH_normalized": 0.2331753969192505,
    "precipitation_signal": 0.9993284940719604,
    "safety_risk": 0.09559440612792969,
    "score": 0.508945643901825,
    "selective_product_yield": 0.027512172237038612,
    "transport_efficiency": 0.8546976447105408
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
      "electrolyte_profile": 1,
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
    "cost": 0.2828400135040283,
    "electrochemical_conversion": 0.028999224305152893,
    "electrochemical_selectivity": 0.9432896971702576,
    "energy_efficiency": 0.8979896306991577,
    "faradaic_efficiency": 0.8857091069221497,
    "ohmic_efficiency": 0.9449054598808289,
    "pH_normalized": 0.20074638724327087,
    "precipitation_signal": 0.8478067517280579,
    "safety_risk": 0.072194404900074,
    "score": 0.2807583808898926,
    "selective_product_yield": 0.010159099474549294,
    "transport_efficiency": 0.887058675289154
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
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 2,
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
    "cost": 0.32444000244140625,
    "electrochemical_conversion": 0.024803686887025833,
    "electrochemical_selectivity": 0.746263325214386,
    "energy_efficiency": 0.708601713180542,
    "faradaic_efficiency": 0.7323735952377319,
    "ohmic_efficiency": 0.9241854548454285,
    "pH_normalized": 0.17063526809215546,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.1135944053530693,
    "score": 0.2335539311170578,
    "selective_product_yield": 0.010164802893996239,
    "transport_efficiency": 0.7395535111427307
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
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 3,
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
    "cost": 0.3084399998188019,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.7136480212211609,
    "energy_efficiency": 0.46861129999160767,
    "faradaic_efficiency": 0.3339889645576477,
    "ohmic_efficiency": 0.9834055304527283,
    "pH_normalized": 0.28434595465660095,
    "precipitation_signal": 0.0,
    "safety_risk": 0.12619440257549286,
    "score": 0.2561466693878174,
    "selective_product_yield": 0.015238527208566666,
    "transport_efficiency": 0.3552139103412628
  }
}
```

## K1 封存报告

## Mechanistic account

### Experimental domain

All 12 batches used 0.020 mol of limiting reagent in 0.040 L of solvent, corresponding to a nominal initial loading of 0.50 mol L⁻¹. Unless stated otherwise, electrolysis was performed at +1.0 V with a 100 mA current ceiling for 600 s. Each batch received one UV–visible measurement after electrolysis and a final assay after termination. Consequently, the conclusions below apply primarily to this loading, volume, apparatus, and tested ranges; they should not be treated as a universal electrochemical law.

### Core explanation

I infer a potential-controlled, direction-specific electron-transfer process coupled to mass transport and material-dependent interfacial chemistry. Productive operation occurs in a positive-potential window near +1 V for solvent S0/electrolyte E0. A potential below that window supplies insufficient productive driving force, whereas a substantially more positive potential activates parasitic or deactivating processes that destroy faradaic efficiency, transport performance, and selectivity. Time controls accumulated conversion through delivered charge, but `current_mA` appears principally to be a ceiling: changing that ceiling over the tested range had much less effect than changing potential, time, or materials.

A useful qualitative model is

η = V − E_onset(materials),

I_delivered = min[I_cap, I_kinetic(η, materials, concentration)],

X(t) ≈ X_max {1 − exp[−k_eff(η, materials, I_delivered)t]},

and

Y_sel ≈ X · S(η, materials) · F_FE(η, materials) · F_transport(materials, state).

Here, activation increases with positive η near onset, but `S` and `F_FE` include a high-overpotential penalty. One possible bounded potential factor is the product of a positive-direction sigmoid and a peaked penalty:

f_V(η) = sigmoid[(η−η₀)/w] · exp{−a[max(η−η_opt,0)]²}.

This is a mechanistic sketch rather than a fitted equation. The dataset identifies the existence and approximate location of a window, but not unique values for η₀, η_opt, w, or a.

### Evidence for a signed, non-monotonic potential response

Batch 1 established the S0/E0 baseline at +1.0 V, 100 mA and 600 s. Its UV–visible estimates were faradaic efficiency 0.979, transport efficiency 0.960, ohmic efficiency 0.982, and energy efficiency 0.914. The final assay reported conversion 0.0234, selectivity 0.9985, selective-product yield 0.00110, and score 0.0324.

Batch 2 reversed the sign to −1.0 V while holding the other variables fixed. UV–visible faradaic and transport efficiencies fell to 0.379 and 0.422, while ohmic efficiency remained 0.995. The final assay reported conversion clipped at 0, selectivity 0.643, yield 0.0130, and score 0.203. Thus the response is not governed simply by |V|: polarity strongly affects the faradaic and transport channels, whereas the resistive/ohmic channel changes little.

Batch 3 tested +0.5 V. Its UV–visible faradaic and transport efficiencies, 0.811 and 0.798, lay between the −1 and +1 V results; final conversion was 0.00687 and selectivity 0.874. This supports progressive activation on moving toward the +1 V window.

Batch 4 tested +2.0 V. UV–visible energy and transport efficiencies were clipped at 0, and faradaic efficiency was only 0.0125. The final assay likewise gave conversion and selectivity of 0, transport and energy efficiencies of 0, and faradaic efficiency 0.0282. Ohmic efficiency nevertheless remained 0.983. This observation changed the explanation from a simple positive-overpotential activation law to a peaked response containing a severe high-potential penalty. Plausible processes include parasitic charge transfer, product or reagent degradation, surface blocking, or entry into a nonproductive interfacial state. The observations establish the penalty but do not distinguish these microscopic alternatives.

The strongest potential-dependent changes occurred in faradaic, transport, energy, and selectivity channels, not in ohmic efficiency. Therefore bulk resistance alone cannot explain the potential optimum.

### Time and delivered charge

Batches 7, 1, and 8 form the controlled time series at S0/E0, +1.0 V and a 100 mA ceiling:

- Batch 7, 60 s: final conversion 0.0119, yield 0.00881, selectivity 0.986, and score 0.262.
- Batch 1, 600 s: final conversion 0.0234, yield 0.00110, selectivity 0.9985, and score 0.0324.
- Batch 8, 1800 s: final conversion 0.0407, yield 0.0244, selectivity 0.9827, and score 0.598.

Conversion broadly increased with duration, supporting accumulation of productive charge. The increase is much less than proportional to time, so a saturating kinetic or transport-limited law is more plausible than indefinite linear growth. Batch 8 retained high final faradaic, transport, and ohmic efficiencies of 0.989, 0.983, and 0.986, respectively; there was no observed efficiency collapse by 1800 s.

Selective-product yield was not monotonic between 60 and 600 s, despite the conversion trend. These yields are close to the assay’s absolute noise scale, so I interpret the time evidence mainly through conversion and the clearly stronger 1800 s result rather than fitting a precise yield-time law. Extrapolation beyond 1800 s is especially uncertain: the proposed saturation is mechanistically reasonable but was not directly located.

### Current ceiling

Batches 5 and 6 tested 20 and 500 mA ceilings, respectively, at +1.0 V for 600 s in S0/E0. Batch 5 gave final faradaic, transport, and ohmic efficiencies of 1.000, 0.990, and 0.992, with conversion 0.00653 and yield 0.0115. Batch 6 gave corresponding efficiencies of 1.000, 0.989, and 0.988, with conversion 0.00806 and yield 0.0162. Their UV–visible efficiency results were also very similar and close to unity.

The tenfold-lower and fivefold-higher ceilings therefore did not produce anything resembling a proportional response. My leading explanation is that the potentiostatic kinetics or cell resistance determined the actual current and that both ceilings were mostly nonbinding, although the experiment did not directly report delivered current or charge. An alternative is that current matters but its effect is obscured by final-assay noise at low conversion. Because there were no replicates and no delivered-current trace, the location of any genuinely current-limited regime is unidentifiable.

### Solvent and electrolyte couplings

Material effects were large and structured.

Batch 9 changed only solvent, from S0 to S1, while retaining E0 and the baseline electrical program. Relative to Batch 1, UV–visible faradaic efficiency fell from 0.979 to 0.847 and transport efficiency from 0.960 to 0.851; final selectivity fell from 0.9985 to 0.776. Ohmic efficiency remained high at 0.993. Final conversion and yield were 0.0112 and 0.0275. This indicates that solvent affects interfacial charge utilization and transport/selectivity more than bulk ohmic loss. The nominal dossier is consistent with this direction because S1 has lower relative conductivity but greater relative diffusivity and a positive potential shift; however, hidden solvent residuals prevent attributing the result to one descriptor.

Batch 10 changed only electrolyte, from E0 to E1, in S0. It produced final faradaic efficiency 0.886, transport efficiency 0.887, ohmic efficiency 0.945, conversion 0.0290, selectivity 0.943, yield 0.0102, pH-normalized signal 0.2007, and precipitation signal 0.848. The S0/E0 baseline had pH-normalized signal about 0.233 and precipitation essentially 1. Thus electrolyte identity changes both electrochemical efficiency and coupled acid/precipitation equilibria. E1’s nominal +0.18 V standard-potential shift relative to E0’s −0.12 V also implies that a fixed applied voltage does not correspond to a fixed effective overpotential.

Batch 11 used S2/E2 together. Its final faradaic, transport, and ohmic efficiencies were 0.732, 0.740, and 0.924; conversion was 0.0248, selectivity 0.746, pH-normalized signal 0.171, and precipitation signal only 0.00524. Batch 12 used S3/E3 and showed still weaker faradaic and transport efficiencies, 0.334 and 0.355, while ohmic efficiency remained 0.983. It had conversion clipped at 0, selectivity 0.714, pH-normalized signal 0.284, and precipitation signal 0.

Across these systems, ohmic efficiency stayed comparatively high even where faradaic and transport efficiencies deteriorated severely. Nominal conductivity is therefore not the sole or dominant performance variable in the tested apparatus. The data require material-dependent interfacial and mass-transport factors, potentially involving diffusivity, diffusion-layer thickness, double-layer capacitance, proton activity, solvation, and potential shifts.

Precipitation is strongly coupled to materials: it was approximately 0.98–1.00 throughout S0/E0, 0.848 in S0/E1, 0.005 in S2/E2, and 0 in S3/E3. It could influence transport or surface activity, but the present data do not establish causality. It may instead be a parallel equilibrium indicator controlled by electrolyte Ksp, salt concentration, proton state, and solvent solubility. In particular, high S0/E0 efficiency despite maximal precipitation argues against a universal claim that precipitation simply poisons the process.

### Measurement consistency and low-signal caution

The final assay channels cannot safely be treated as exact algebraic identities in this low-conversion region. For example, Batch 1 reported conversion 0.0234 and selectivity 0.9985 but yield 0.00110, while Batch 2 reported conversion clipped at 0 yet yield 0.0130. These discrepancies are consistent with independently noisy, bounded estimates near zero and with clipping of negative noisy conversion estimates. They could also reflect differing definitions of the synthetic channels, whose hidden species mapping was not public. I therefore did not calculate selectivity as yield/conversion or force a mass-balance identity.

UV–visible and final-assay efficiencies usually agreed qualitatively but differed numerically, as expected for independent measurements. Effects much larger than their stated noise—especially the collapse at +2 V and the material-associated transport differences—are credible. Small differences among low yields are not strong evidence without replication.

### Variables judged most important

1. **Signed applied potential relative to a material-dependent onset.** This controls activation and the severe high-potential penalty.
2. **Electrolysis duration and accumulated delivered charge.** Conversion rises with time but appears sublinear.
3. **Solvent/electrolyte combination.** It shifts onset and affects faradaic utilization, transport, selectivity, proton state, and precipitation.
4. **Interfacial and transport properties.** These explain large changes that persist while ohmic efficiency remains high.
5. **Current ceiling.** It is secondary when nonbinding, but could matter below an unmeasured threshold.
6. **Initial concentration/loading.** It is mechanistically important but was held fixed, so its response is completely unidentified here.

### Scope and non-identifiability

The response surface is only locally characterized. Potential was varied only in S0/E0 at one main duration and loading. Consequently, the optimal potential may shift substantially with electrolyte or solvent, and +1 V should not be assumed optimal for all four material families. Likewise, time was varied only near +1 V in S0/E0.

S2/E2 and S3/E3 changed solvent and electrolyte simultaneously, so their separate main effects and interactions cannot be recovered. Only S1 versus S0 at E0 and E1 versus E0 in S0 are clean single-factor contrasts. Electrode geometry, contact resistance, kinetic prefactors, actual delivered current, hidden world residuals, molecular identities, and microscopic side products were not observed. With no batch replication, process variability cannot be separated cleanly from instrument noise.

No experiment varied reagent loading or solvent volume. Concentration dependence, reagent-order kinetics, depletion limits, and scale effects are therefore conjectural. There was also no temporal sampling within a single vessel, so the proposed exponential saturation is not uniquely distinguished from diffusion-limited square-root-time behavior, electrode deactivation, or a sequence of induction and steady-state regimes.

### Plausible alternative accounts

A purely empirical categorical response surface could explain the results without assigning nominal material properties any causal role; fixed hidden material residuals may dominate the dossier values. The +2 V collapse could arise from electrode passivation rather than homogeneous side reactions. The apparent time saturation could reflect declining electrode activity instead of reagent depletion or transport limitation. Material-dependent precipitation could cause some of the transport response, but it could equally be a noncausal reporter of acid–salt equilibrium. Finally, the weak current-ceiling effect could mean that the ceiling never bound, or it could be a genuine plateau in charge-transfer kinetics.

### Overall conclusion

The most defensible account is a bounded, material-shifted electrochemical window: positive potential activates productive conversion, excessive positive potential drives a nonproductive state, time accumulates conversion with diminishing returns, and solvent/electrolyte properties modulate onset, faradaic efficiency, transport, selectivity, proton state, and precipitation. Ohmic loss is comparatively minor across the tested cells. Batch 8—S0/E0, +1.0 V, 100 mA ceiling, 1800 s—provided the strongest observed combined outcome, with conversion 0.0407, selective-product yield 0.0244, selectivity 0.9827, and score 0.5976, but it is evidence for a good tested operating point rather than proof of a global optimum.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific response prior or true mechanism was supplied. The material dossier supplied nominal properties and warned that hidden residuals or misindexing could occur, but it did not supply a law mapping conditions to selectivity or faradaic efficiency.

My signed-potential-window hypothesis was supported within S0/E0. Batch 1 at +1.0 V had high faradaic and transport efficiencies, whereas Batch 2 at −1.0 V had much lower values. Batch 3 at +0.5 V was intermediate. Batch 4 at +2.0 V contradicted a simple monotonic positive-overpotential law: faradaic and transport performance collapsed while ohmic efficiency remained high. That result was the clearest reason to replace simple activation with a peaked response containing a high-potential penalty. The microscopic cause of that penalty—reversible parasitic current, solution degradation, passivation, or another interfacial transition—remained untested.

The time/charge hypothesis was partly supported. Conversion broadly increased across Batch 7 (60 s), Batch 1 (600 s), and Batch 8 (1800 s), but the selective-yield estimates were not monotonic at low signal. The data supported increasing conversion with time but did not uniquely establish exponential saturation rather than diffusion-limited growth or progressive deactivation. Saturation itself was not reached.

The proposal that current was principally a nonbinding ceiling was weakly supported by Batches 5 and 6: changing the ceiling from 20 to 500 mA produced very similar efficiency estimates. It was not proved because delivered current and charge were unavailable, there were no replicates, and lower ceilings were not tested.

Material-dependent coupling was supported qualitatively. Batch 9 isolated an S0-to-S1 solvent change and reduced faradaic efficiency, transport efficiency, and selectivity. Batch 10 isolated E0-to-E1 and changed efficiency, pH-normalized signal, and precipitation. Batches 11 and 12 showed still larger material-associated differences, but their solvent and electrolyte changes were confounded. The stronger claim that nominal conductivity should dominate performance was not supported: ohmic efficiency stayed high even when faradaic and transport efficiencies were poor. The supplied nominal properties themselves, their indexing, and the fixed-fixture statement were not directly testable with this campaign.

The exact identity `selective yield = conversion × selectivity` was contradicted as an equation for the reported low-signal estimates: Batch 1 and especially Batch 2 did not satisfy it. I treated this as independent assay noise, clipping, or different channel definitions rather than evidence against mass conservation in the latent chemistry.

2. One additional discriminating experiment

I would run one S0/E0 batch at the original loading as a potential-step rescue experiment. After a short +2.0 V exposure, I would take an intermediate UV–visible measurement, switch to +1.0 V, electrolyze for the same 600 s used in Batch 1, take a second intermediate measurement if permitted, then terminate and perform the final assay. Existing Batches 1 and 4 would provide the reference endpoints.

If the efficiencies recovered toward Batch 1 after stepping down to +1.0 V, I would favor a largely reversible, instantaneous potential-dependent diversion of current. If they remained close to the failed Batch 4 state, I would favor persistent passivation, reagent/product destruction, or another irreversible state change. Recovery of faradaic efficiency without recovery of yield would instead suggest that the electrode response is reversible but the earlier +2.0 V exposure irreversibly altered the solution inventory. Partial recovery would support a mixture of reversible parasitic current and persistent damage. This single experiment would not uniquely separate electrode passivation from homogeneous degradation, but it would distinguish the leading reversible window model from the broad alternative of persistent high-potential damage.

3. Unused evidence, reliability, and goal effects

I did not inspect or model the raw spectral artifacts; the account used processed estimates. Cost and safety records were not incorporated into the kinetic model, although all tested risks remained below the stated safety limit. The nominal diffusivity, capacitance, conductivity, acid, Ksp, and potential-shift values were used qualitatively rather than fitted quantitatively. Final pH and precipitation signals informed the material interpretation but not the yield model. Temperature changes, spectral peak shapes, and actual current or delivered charge were unavailable or unused. I also chose UV–visible measurements for all intermediate slots, so no intermediate pH trajectories were collected.

The least reliable predictions are the 7200 s extrapolations because the longest campaign run was only 1800 s. Predictions for S0/E3 and S2/E0 are especially uncertain because those exact combinations were never tested; Batches 11 and 12 confounded solvent and electrolyte effects. Long-duration negative-potential predictions are also weak because negative potential was tested only once, for 600 s. Scores near the 0.02 selective-yield gate are highly uncertain because small yield errors can produce large score changes. The Batch 8 recommendation is reliable only as the best observed batch, not as a global optimum: it lacked replication and local refinement.

The explanatory research goal materially affected evidence collection. I spent batches on polarity, potential magnitude, current ceiling, duration, and material contrasts rather than replicating the best condition or densely optimizing around Batch 8. That broadened mechanistic coverage but weakened estimates of process variance and local optima. There was no clear conflict with safety, but treating public score as secondary meant the campaign favored discriminating contrasts over maximum-score exploitation. These are retrospective conclusions based on the recorded campaign, not claims about unrecorded contemporaneous thoughts.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.7,
        "lower80": 0.52,
        "upper80": 0.82
      },
      "energy_efficiency": {
        "estimate": 0.4,
        "lower80": 0.23,
        "upper80": 0.57
      },
      "faradaic_efficiency": {
        "estimate": 0.5,
        "lower80": 0.35,
        "upper80": 0.65
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.0714,
        "lower80": 0.0,
        "upper80": 0.3
      },
      "selective_product_yield": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.018
      },
      "transport_efficiency": {
        "estimate": 0.52,
        "lower80": 0.35,
        "upper80": 0.68
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.96,
        "lower80": 0.88,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.92,
        "lower80": 0.8,
        "upper80": 1.0
      },
      "faradaic_efficiency": {
        "estimate": 0.94,
        "lower80": 0.84,
        "upper80": 1.0
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.5769,
        "lower80": 0.18,
        "upper80": 0.66
      },
      "selective_product_yield": {
        "estimate": 0.024,
        "lower80": 0.006,
        "upper80": 0.045
      },
      "transport_efficiency": {
        "estimate": 0.94,
        "lower80": 0.84,
        "upper80": 1.0
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.7,
        "lower80": 0.5,
        "upper80": 0.83
      },
      "energy_efficiency": {
        "estimate": 0.4,
        "lower80": 0.2,
        "upper80": 0.6
      },
      "faradaic_efficiency": {
        "estimate": 0.5,
        "lower80": 0.3,
        "upper80": 0.67
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.3678,
        "lower80": 0.12,
        "upper80": 0.46
      },
      "selective_product_yield": {
        "estimate": 0.028,
        "lower80": 0.006,
        "upper80": 0.07
      },
      "transport_efficiency": {
        "estimate": 0.52,
        "lower80": 0.3,
        "upper80": 0.7
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.96,
        "lower80": 0.87,
        "upper80": 0.99
      },
      "energy_efficiency": {
        "estimate": 0.92,
        "lower80": 0.78,
        "upper80": 0.98
      },
      "faradaic_efficiency": {
        "estimate": 0.94,
        "lower80": 0.84,
        "upper80": 0.99
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.6214,
        "lower80": 0.53,
        "upper80": 0.67
      },
      "selective_product_yield": {
        "estimate": 0.134,
        "lower80": 0.06,
        "upper80": 0.24
      },
      "transport_efficiency": {
        "estimate": 0.94,
        "lower80": 0.82,
        "upper80": 0.99
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.38,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.27,
        "lower80": 0.1,
        "upper80": 0.46
      },
      "faradaic_efficiency": {
        "estimate": 0.35,
        "lower80": 0.15,
        "upper80": 0.55
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.2315,
        "lower80": 0.0,
        "upper80": 0.4
      },
      "selective_product_yield": {
        "estimate": 0.0155,
        "lower80": 0.0,
        "upper80": 0.045
      },
      "transport_efficiency": {
        "estimate": 0.4,
        "lower80": 0.2,
        "upper80": 0.62
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.88,
        "lower80": 0.72,
        "upper80": 0.96
      },
      "energy_efficiency": {
        "estimate": 0.78,
        "lower80": 0.6,
        "upper80": 0.91
      },
      "faradaic_efficiency": {
        "estimate": 0.78,
        "lower80": 0.6,
        "upper80": 0.91
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.535,
        "lower80": 0.4,
        "upper80": 0.61
      },
      "selective_product_yield": {
        "estimate": 0.088,
        "lower80": 0.03,
        "upper80": 0.18
      },
      "transport_efficiency": {
        "estimate": 0.8,
        "lower80": 0.62,
        "upper80": 0.92
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.52,
        "lower80": 0.25,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.16,
        "lower80": 0.0,
        "upper80": 0.38
      },
      "faradaic_efficiency": {
        "estimate": 0.22,
        "lower80": 0.05,
        "upper80": 0.45
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.0707,
        "lower80": 0.0,
        "upper80": 0.28
      },
      "selective_product_yield": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.03
      },
      "transport_efficiency": {
        "estimate": 0.25,
        "lower80": 0.05,
        "upper80": 0.5
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.75,
        "lower80": 0.55,
        "upper80": 0.9
      },
      "energy_efficiency": {
        "estimate": 0.5,
        "lower80": 0.28,
        "upper80": 0.72
      },
      "faradaic_efficiency": {
        "estimate": 0.5,
        "lower80": 0.3,
        "upper80": 0.72
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.3962,
        "lower80": 0.2,
        "upper80": 0.52
      },
      "selective_product_yield": {
        "estimate": 0.045,
        "lower80": 0.008,
        "upper80": 0.12
      },
      "transport_efficiency": {
        "estimate": 0.5,
        "lower80": 0.28,
        "upper80": 0.72
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.56,
        "lower80": 0.32,
        "upper80": 0.76
      },
      "energy_efficiency": {
        "estimate": 0.22,
        "lower80": 0.04,
        "upper80": 0.45
      },
      "faradaic_efficiency": {
        "estimate": 0.28,
        "lower80": 0.08,
        "upper80": 0.5
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.1321,
        "lower80": 0.0,
        "upper80": 0.34
      },
      "selective_product_yield": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "transport_efficiency": {
        "estimate": 0.32,
        "lower80": 0.1,
        "upper80": 0.56
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.8,
        "lower80": 0.62,
        "upper80": 0.92
      },
      "energy_efficiency": {
        "estimate": 0.7,
        "lower80": 0.5,
        "upper80": 0.86
      },
      "faradaic_efficiency": {
        "estimate": 0.75,
        "lower80": 0.55,
        "upper80": 0.9
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.4957,
        "lower80": 0.33,
        "upper80": 0.59
      },
      "selective_product_yield": {
        "estimate": 0.068,
        "lower80": 0.018,
        "upper80": 0.15
      },
      "transport_efficiency": {
        "estimate": 0.75,
        "lower80": 0.55,
        "upper80": 0.9
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.7,
        "lower80": 0.49,
        "upper80": 0.84
      },
      "energy_efficiency": {
        "estimate": 0.4,
        "lower80": 0.19,
        "upper80": 0.61
      },
      "faradaic_efficiency": {
        "estimate": 0.5,
        "lower80": 0.3,
        "upper80": 0.68
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.3692,
        "lower80": 0.12,
        "upper80": 0.47
      },
      "selective_product_yield": {
        "estimate": 0.031,
        "lower80": 0.006,
        "upper80": 0.078
      },
      "transport_efficiency": {
        "estimate": 0.52,
        "lower80": 0.29,
        "upper80": 0.71
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.96,
        "lower80": 0.87,
        "upper80": 0.99
      },
      "energy_efficiency": {
        "estimate": 0.92,
        "lower80": 0.78,
        "upper80": 0.99
      },
      "faradaic_efficiency": {
        "estimate": 0.94,
        "lower80": 0.83,
        "upper80": 1.0
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.6254,
        "lower80": 0.53,
        "upper80": 0.68
      },
      "selective_product_yield": {
        "estimate": 0.144,
        "lower80": 0.065,
        "upper80": 0.26
      },
      "transport_efficiency": {
        "estimate": 0.94,
        "lower80": 0.81,
        "upper80": 1.0
      }
    }
  ],
  "rationale": "Predictions use the observed signed potential window: S0/E0 performed strongly near positive 1 V but poorly at negative potential, while excessive positive potential caused collapse. The 7200 s cases extrapolate the observed sublinear increase with time, with wide yield intervals because the campaign only reached 1800 s and low-yield assay noise was substantial. Electrolytes E1 and E3 and solvent S2 were assigned material-dependent onset and transport penalties inferred from the partially confounded material contrasts. Current ceilings of 100 and 500 mA are predicted to behave similarly because the campaign showed little cap sensitivity. Score estimates apply the published weighted components and selective-yield gate; uncertainty intervals include instrument noise, unreplicated process variation, long-time extrapolation, and unidentified solvent–electrolyte interactions."
}
```
