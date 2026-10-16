# repeat-02/EC-W04-B12-discovery-E-MisIndexed

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-02\EC-W04-B12-discovery-E-MisIndexed\participant\discovery-E-MisIndexed

## 同期笔记

### v1 · 公开事件 0

# Electrochemical hypothesis notebook

## Prior expectations (before batch 1)
H1 [tentative] At fixed 0.04 mol reagent in 0.08 L solvent, conversion should rise with absolute driving potential and electrolysis duration until depletion, while selectivity may peak at an intermediate overpotential because excessive drive promotes side reactions.

H2 [tentative] Current caps can bind delivered current, so time alone will not determine charge; electrolyte/solvent conductivity should influence ohmic and energy efficiency. Nominally conductive combinations (especially E2 and S0) may improve ohmic efficiency, but E2's positive potential shift should displace the potential-response curve.

H3 [tentative] Potential-sign response may be asymmetric rather than a function of magnitude alone. I will use paired signs and at least one time/current series to distinguish polarity, charge limitation, and material effects.

A result showing similar outcomes at opposite signs would weaken H3; monotone selectivity through the tested potential range would weaken the proposed intermediate optimum in H1.

### v2 · 公开事件 85

# Electrochemical hypothesis notebook

## Final source-stage account

### H1 — bounded productive potential window [supported in S2/E2]
At 0.04 mol reagent in 0.08 L, S2/E2 at +1.5 V and a 100 mA cap sustains high selectivity and charge/transport efficiency, whereas +1.0 V gives little detectable conversion and +2.0 V collapses selectivity and faradaic/transport efficiency. Evidence: final assays at +1.0 V (runner-operation-0020), +1.5 V (runner-operation-0048), and +2.0 V (runner-operation-0034). The +1.5 V assay gave selectivity 0.988, FE 0.992, transport 0.996, and conversion 0.033; +2.0 V gave all three selectivity/FE/transport near zero. This supports an intermediate-overpotential window rather than monotonic benefit from voltage.

Potential sign is strongly asymmetric in the tested scope: S2/E2 at -1.0 V (runner-operation-0027) had much lower selectivity and efficiencies than +1.0 V (runner-operation-0020), and E0/S0 showed the same qualitative sign disadvantage (runner-operation-0007 versus -1.0 V runner-operation-0013), although low conversion and precipitation complicate the E0/S0 pair.

Testable consequence: for S2/E2, response should peak near +1.5 V and shift with declared material potential shifts; negative potentials should remain poorly productive at comparable magnitude.

### H2 — current cap controls regime, not guaranteed charge [supported qualitatively]
At +1.5 V in S2/E2 for 600 s, a 10 mA cap retained high FE/transport but no detectable yield (runner-operation-0055), while a 500 mA cap collapsed selectivity, FE, energy, and transport (runner-operation-0062). Together with the productive 100 mA runs, this suggests a low-cap charge-limited regime, an intermediate productive regime, and a high-cap transport/side-reaction regime. Absolute delivered current was not observed, so a quantitative current law remains unresolved.

### H3 — time response is nonmonotone because efficiency deteriorates on long electrolysis [supported, mechanism unresolved]
At +1.5 V, 100 mA, S2/E2, increasing from 60 s (runner-operation-0041) to 1800 s (runner-operation-0048) raised final conversion/yield while preserving near-unity FE and transport. In the 7200 s batch, UV-vis at 1800 s still showed FE=1 and transport=1 (runner-operation-0081), but by 7200 s these fell to about 0.33 and 0.35 (runner-operation-0083); the final assay yield was 0.0265 (runner-operation-0085), not higher than the 1800 s result within the assay's stated yield noise. This favors time-dependent concentration polarization, reagent depletion, interfacial change, or byproduct accumulation over a time-invariant Faraday law. These alternatives were not separated.

### H4 — material choice affects precipitation and operating window [supported only for paired formulations]
E0/S0 precipitated strongly in both sign tests (runner-operation-0007, runner-operation-0013). S2/E2 suppressed final precipitation and was productive near +1.5 V (runner-operation-0048). S1/E1 at the same nominal potential/current/time precipitated substantially and lost selectivity/FE (runner-operation-0069); S3/E3 avoided precipitation but had intermediate performance (runner-operation-0076). Because solvent and electrolyte were changed together, their individual contributions and possible interactions remain unresolved; the nominal dossier is consistent with, but does not prove, the precipitation interpretation.

### Scope and uncertainty
Final-assay conversion and selective-yield values were often comparable to their stated 0.01 noise scales, so small numerical differences are not strong evidence. The large efficiency/selectivity collapses and the within-batch 1800-to-7200 UV-vis deterioration are more persuasive than marginal yield rankings. No replicate batch was run, so repeatability remains an open requirement.

### Operating decision
Batch 7 is the most defensible recommendation: S2/E2, +1.5 V, 100 mA cap, 1800 s. I prefer it over the longer batch 12 because the latter showed late efficiency decay, and over batch 6 because 60 s produced less conversion/yield. I would change this decision if replication showed batch-7 yield was noise-dominated or if a nearby potential/current produced equal selectivity with higher reproducible conversion.

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
    "electrochemical_conversion": 0.013086915947496891,
    "electrochemical_selectivity": 1.0,
    "energy_efficiency": 0.6831510066986084,
    "faradaic_efficiency": 0.6771227121353149,
    "ohmic_efficiency": 0.9572166204452515,
    "pH_normalized": 0.23443032801151276,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.6484189629554749
  }
}
```

### 批次 2 · 终点事件 13

```json
{
  "ordinal": 2,
  "lifecycle_index": 2,
  "end_step": 13,
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
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "metrics": {
    "cost": 0.3274399936199188,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.6606547832489014,
    "energy_efficiency": 0.27864500880241394,
    "faradaic_efficiency": 0.4274474084377289,
    "ohmic_efficiency": 0.9660544395446777,
    "pH_normalized": 0.2317349761724472,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.1772691309452057,
    "selective_product_yield": 0.011142478324472904,
    "transport_efficiency": 0.45370420813560486
  }
}
```

### 批次 3 · 终点事件 20

```json
{
  "ordinal": 3,
  "lifecycle_index": 3,
  "end_step": 20,
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
      "current_mA": 100,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "instrument": "ph_meter",
      "operation": "measure"
    },
    {
      "duration_s": 600,
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
    "cost": 0.4286400079727173,
    "electrochemical_conversion": 0.0006304567214101553,
    "electrochemical_selectivity": 0.8740193843841553,
    "energy_efficiency": 0.8176618814468384,
    "faradaic_efficiency": 0.7675839066505432,
    "ohmic_efficiency": 0.915018618106842,
    "pH_normalized": 0.17481118440628052,
    "precipitation_signal": 0.0,
    "safety_risk": 0.1135944053530693,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.7841407656669617
  }
}
```

### 批次 4 · 终点事件 27

```json
{
  "ordinal": 4,
  "lifecycle_index": 4,
  "end_step": 27,
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
      "current_mA": 100,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -1
    },
    {
      "instrument": "ph_meter",
      "operation": "measure"
    },
    {
      "duration_s": 600,
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
    "cost": 0.4286400079727173,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.5370853543281555,
    "energy_efficiency": 0.2731221914291382,
    "faradaic_efficiency": 0.35157251358032227,
    "ohmic_efficiency": 0.9271767735481262,
    "pH_normalized": 0.17412059009075165,
    "precipitation_signal": 0.0,
    "safety_risk": 0.1135944053530693,
    "score": 0.029927246272563934,
    "selective_product_yield": 0.0022121944930404425,
    "transport_efficiency": 0.32008495926856995
  }
}
```

### 批次 5 · 终点事件 34

```json
{
  "ordinal": 5,
  "lifecycle_index": 5,
  "end_step": 34,
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
      "current_mA": 100,
      "electrolyte_profile": 2,
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
    "cost": 0.43588000535964966,
    "electrochemical_conversion": 0.0034490374382585287,
    "electrochemical_selectivity": 0.006436008028686047,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.01102422270923853,
    "ohmic_efficiency": 0.9623374342918396,
    "pH_normalized": 0.17908813059329987,
    "precipitation_signal": 0.0,
    "safety_risk": 0.1135944053530693,
    "score": 0.034797653555870056,
    "selective_product_yield": 0.0084654176607728,
    "transport_efficiency": 0.0005147586925886571
  }
}
```

### 批次 6 · 终点事件 41

```json
{
  "ordinal": 6,
  "lifecycle_index": 6,
  "end_step": 41,
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
      "current_mA": 100,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": 1.5
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
    "cost": 0.4354360103607178,
    "electrochemical_conversion": 0.002920722821727395,
    "electrochemical_selectivity": 0.9942426681518555,
    "energy_efficiency": 0.9375463128089905,
    "faradaic_efficiency": 1.0,
    "ohmic_efficiency": 0.9522853493690491,
    "pH_normalized": 0.17581218481063843,
    "precipitation_signal": 0.0023995577357709408,
    "safety_risk": 0.1135944053530693,
    "score": 0.3265947103500366,
    "selective_product_yield": 0.011099033057689667,
    "transport_efficiency": 0.9893726110458374
  }
}
```

### 批次 7 · 终点事件 48

```json
{
  "ordinal": 7,
  "lifecycle_index": 7,
  "end_step": 48,
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
      "current_mA": 100,
      "electrolyte_profile": 2,
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
    "cost": 0.43647998571395874,
    "electrochemical_conversion": 0.03343962877988815,
    "electrochemical_selectivity": 0.9878324270248413,
    "energy_efficiency": 0.9428983926773071,
    "faradaic_efficiency": 0.9921573996543884,
    "ohmic_efficiency": 0.98384690284729,
    "pH_normalized": 0.17482678592205048,
    "precipitation_signal": 0.0,
    "safety_risk": 0.1135944053530693,
    "score": 0.5993203520774841,
    "selective_product_yield": 0.030147748067975044,
    "transport_efficiency": 0.9955577850341797
  }
}
```

### 批次 8 · 终点事件 55

```json
{
  "ordinal": 8,
  "lifecycle_index": 8,
  "end_step": 55,
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
      "current_mA": 10,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": 1.5
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
    "cost": 0.4354360103607178,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.9731932878494263,
    "energy_efficiency": 0.9694521427154541,
    "faradaic_efficiency": 0.9755492806434631,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.17312930524349213,
    "precipitation_signal": 0.00031451715040020645,
    "safety_risk": 0.1135944053530693,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.9690539240837097
  }
}
```

### 批次 9 · 终点事件 62

```json
{
  "ordinal": 9,
  "lifecycle_index": 9,
  "end_step": 62,
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
      "potential_V": 1.5
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
    "cost": 0.43720000982284546,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.031468190252780914,
    "faradaic_efficiency": 0.0,
    "ohmic_efficiency": 0.7915424704551697,
    "pH_normalized": 0.1751430779695511,
    "precipitation_signal": 0.008188718929886818,
    "safety_risk": 0.1135944053530693,
    "score": 0.06410591304302216,
    "selective_product_yield": 0.01722601428627968,
    "transport_efficiency": 0.012177566066384315
  }
}
```

### 批次 10 · 终点事件 69

```json
{
  "ordinal": 10,
  "lifecycle_index": 10,
  "end_step": 69,
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
      "current_mA": 100,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 1.5
    },
    {
      "instrument": "ph_meter",
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
    "cost": 0.37828001379966736,
    "electrochemical_conversion": 0.015369986183941364,
    "electrochemical_selectivity": 0.019033947959542274,
    "energy_efficiency": 0.014645654708147049,
    "faradaic_efficiency": 0.009028017520904541,
    "ohmic_efficiency": 0.9546998143196106,
    "pH_normalized": 0.20370754599571228,
    "precipitation_signal": 0.7154496908187866,
    "safety_risk": 0.09559440612792969,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.010377603583037853
  }
}
```

### 批次 11 · 终点事件 76

```json
{
  "ordinal": 11,
  "lifecycle_index": 11,
  "end_step": 76,
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
      "current_mA": 100,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": 1.5
    },
    {
      "instrument": "ph_meter",
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
    "cost": 0.3974800109863281,
    "electrochemical_conversion": 0.02302798070013523,
    "electrochemical_selectivity": 0.8312817811965942,
    "energy_efficiency": 0.45731979608535767,
    "faradaic_efficiency": 0.4126834273338318,
    "ohmic_efficiency": 0.9802416563034058,
    "pH_normalized": 0.2777584195137024,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.12619440257549286,
    "score": 0.17754711210727692,
    "selective_product_yield": 0.009638501331210136,
    "transport_efficiency": 0.41986337304115295
  }
}
```

### 批次 12 · 终点事件 85

```json
{
  "ordinal": 12,
  "lifecycle_index": 12,
  "end_step": 85,
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
      "current_mA": 100,
      "electrolyte_profile": 2,
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
      "duration_s": 5400,
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
    "cost": 0.4827199876308441,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.9679781198501587,
    "energy_efficiency": 0.30148380994796753,
    "faradaic_efficiency": 0.2924306392669678,
    "ohmic_efficiency": 0.968361496925354,
    "pH_normalized": 0.17432305216789246,
    "precipitation_signal": 0.0,
    "safety_risk": 0.1135944053530693,
    "score": 0.3423025608062744,
    "selective_product_yield": 0.026523685082793236,
    "transport_efficiency": 0.3136555850505829
  }
}
```

## K1 封存报告

Mechanism report

1. Experimental scope

All 12 batches used 0.040 mol of anonymous limiting reagent in 0.080 L of one solvent. The controlled electrochemical variables were solvent identity, electrolyte profile, applied potential, current cap, and electrolysis time. The cell fixture was fixed across the campaign, so its electrode area, gap, and base contact resistance were campaign-wide nuisance constants rather than varied factors.

The final-assay uncertainties are important when interpreting the results: standard deviations were 0.010 for conversion and selective-product yield, 0.012 for selectivity and faradaic efficiency, 0.014 for transport efficiency, 0.016 for energy efficiency, 0.012 for ohmic efficiency, 0.002 for normalized pH, and 0.006 for precipitation signal. Several measured conversions and yields were therefore near the assay noise floor. Large changes in efficiency or precipitation are much more convincing than small yield differences.

2. Principal observations

The most informative potential series used S2/E2 at a 100 mA cap. At +1.0 V for 600 s, batch 3 gave conversion 0.00063, selectivity 0.874, faradaic efficiency 0.768, transport efficiency 0.784, and no final precipitation. At -1.0 V for 600 s, batch 4 gave conversion reported as zero, selectivity 0.537, faradaic efficiency 0.352, transport efficiency 0.320, and yield 0.0022. At +2.0 V for 600 s, batch 5 gave conversion 0.00345 but selectivity 0.0064, faradaic efficiency 0.011, transport efficiency 0.0005, and energy efficiency clipped at zero. Thus, increasing positive potential was not monotonically beneficial: +1.0 V was relatively efficient but weakly converting, while +2.0 V entered an almost completely unproductive regime.

The productive window was found near +1.5 V. In S2/E2 with a 100 mA cap, batch 6 at 60 s gave selectivity 0.994, faradaic efficiency 1.000, transport efficiency 0.989, energy efficiency 0.938, conversion 0.0029, and yield 0.0111. Batch 7 at 1800 s retained selectivity 0.988, faradaic efficiency 0.992, transport efficiency 0.996, energy efficiency 0.943, and ohmic efficiency 0.984, while conversion rose to 0.0334 and yield to 0.0301. Although the yield change is modest relative to its noise, the combined conversion increase and sustained near-unity efficiencies support a productive intermediate-potential regime.

Current cap changed the regime strongly. At +1.5 V for 600 s in S2/E2, batch 8 with a 10 mA cap retained high selectivity (0.973), faradaic efficiency (0.976), transport efficiency (0.969), energy efficiency (0.969), and ohmic efficiency (1.000), but conversion and yield were reported as zero. Batch 9 with a 500 mA cap instead gave selectivity and faradaic efficiency reported as zero, transport efficiency 0.012, energy efficiency 0.031, and ohmic efficiency 0.792. Its reported yield of 0.0172 despite zero conversion illustrates why near-floor conversion and yield channels should not be forced into an exact mass balance. The robust observation is the efficiency collapse at the high cap.

Time also changed the operating regime. Batch 12 used the same S2/E2, +1.5 V, 100 mA conditions for 7200 s. Its UV-vis measurement at 1800 s showed faradaic efficiency 1.000, transport efficiency 1.000, energy efficiency 0.910, and ohmic efficiency 0.946. At 7200 s, before termination, these had fallen to approximately 0.328, 0.348, 0.415, and 0.892, respectively. The final assay gave yield 0.0265, selectivity 0.968, faradaic efficiency 0.292, transport efficiency 0.314, and energy efficiency 0.301. Thus, long electrolysis caused a within-batch loss of charge and transport efficiency; it did not simply continue the favorable 60-to-1800 s trend.

Material pairs mattered. E0/S0 produced complete precipitation signals in both batch 1 (+1.0 V) and batch 2 (-1.0 V). Batch 1 nevertheless had conversion 0.0131, selectivity 1.000, and faradaic efficiency 0.677, but selective yield was reported as zero, consistent with precipitation or recovery loss masking an otherwise selective electrochemical step. Batch 2 had lower selectivity (0.661), faradaic efficiency (0.427), and transport efficiency (0.454).

At +1.5 V, 100 mA, and 1800 s, batch 10 using S1/E1 gave precipitation 0.715, selectivity 0.019, faradaic efficiency 0.009, and transport efficiency 0.010. Batch 11 using S3/E3 avoided precipitation (0.0052) but was intermediate: conversion 0.0230, selectivity 0.831, faradaic efficiency 0.413, transport efficiency 0.420, and yield 0.0096. Batch 7 using S2/E2 was clearly superior in electrochemical efficiency under the same nominal controls. Because solvent and electrolyte were changed together in these comparisons, their individual effects are not identifiable.

Normalized pH was mainly material-dependent over the tested conditions. S2/E2 final values clustered around 0.173–0.179, E0/S0 around 0.232–0.234, S1/E1 was 0.204, and S3/E3 was 0.278. These are normalized instrument outputs, not ordinary pH units. The association between pH and precipitation is not monotonic across all materials, so pH alone is not a sufficient precipitation law.

3. Proposed process model

I interpret the system as competing productive and parasitic electrode reactions, coupled to ohmic loss, mass transport, acid/base state, and precipitation. A useful latent driving variable is an effective interfacial overpotential:

η = E_applied - ΔE_electrolyte - ΔE_solvent - E_reaction - I_actual R_ohmic.

The absolute sign convention and E_reaction are unknown. The declared material shifts nevertheless organize the data. S2 and E2 contribute nominal positive shifts of +0.20 and +0.28 V. Consequently, +1.0 V may underdrive this pair, +1.5 V may place it near the productive window, and +2.0 V may overdrive it. S1/E1 has only about +0.02 V combined nominal shift, so +1.5 V could impose substantially more effective overpotential and favor parasitic reactions, consistent with batch 10. S3/E3 has about +0.28 V combined shift and gave intermediate behavior in batch 11. This alignment is suggestive rather than a fitted or uniquely established law because each pair also differs in conductivity, diffusivity, proton activity, double-layer capacitance, and precipitation chemistry.

The actual current can be represented schematically as

I_actual = min(I_cap, I_kinetic(η), I_transport),

with productive and side-reaction partial currents satisfying

FE = I_product / (I_product + I_side + I_nonfaradaic).

At low current cap, batch 8 suggests I_actual is cap-limited: efficiency remains high, but insufficient charge passes to make product detectable in 600 s. At an intermediate cap, batch 7 suggests the productive partial current dominates. At 500 mA, batch 9 indicates that side reactions and transport limitation dominate. The current cap is therefore not simply a rate setting; it selects among electrochemical regimes.

A corresponding material-balance model is

dN_reactant/dt = -I_actual FE/(nF),

dN_target/dt = S(η,state) I_actual FE/(nF) - k_loss(state)N_target,

where n, the electron stoichiometry, is unknown. A measured selective-product yield would approximately track recovered N_target/N_initial, but assay noise, precipitation, and unobserved recovery processes prevent an exact equality with measured conversion times selectivity.

The productive selectivity function S appears peaked rather than monotonic in η. At low drive, productive reaction is slow; near the optimum, target formation dominates; at excessive drive, competing reduction/oxidation, solvent or electrolyte decomposition, and possibly electrode-surface changes consume current. Batch 5 and batch 9 show that excessive potential and excessive permitted current can each reach the unproductive regime by different control paths.

Transport can be represented by a limiting current such as

I_lim(t) ∝ nFAD_eff C_reactant(t)/δ_eff(t),

and a qualitative efficiency relation such as

T_eff ≈ 1/[1 + (I_actual/I_lim)^m],

for some positive exponent m. The nominal diffusivity, diffusion-layer thickness, solvent diffusivity factor, and concentration all contribute to I_lim. During long electrolysis, C_reactant may decrease and δ_eff may grow because of concentration polarization, bubbles, deposits, precipitate, or interfacial films. This makes I_lim fall with time. The within-batch deterioration between 1800 and 7200 s in batch 12 is the strongest evidence for a time-dependent state variable rather than a constant-efficiency Faraday law.

Ohmic efficiency depends on conductivity and current approximately through power loss I_actual²R. It remained high in most moderate-current batches but fell to 0.792 in the 500 mA batch, consistent with stronger resistive loss at large current. Conductivity alone cannot explain selectivity: S2/E2 contains a nominally conductive electrolyte but a relatively low-conductivity solvent, and its success occurred only in the appropriate potential/current window.

Precipitation is plausibly governed by an ionic-product threshold,

precipitation when Q_ions(state,pH,conversion) > Ksp_effective(solvent,electrolyte),

followed by removal or masking of soluble target and possible electrode fouling. E0 has the highest declared precipitating-salt concentration and the least favorable nominal solubility conditions among the tested paired formulations, consistent with the saturated precipitation signal in batches 1 and 2. S2 has a tenfold favorable solvent solubility-product factor and E2 has very low precipitating-salt concentration, consistent with near-zero final precipitation. This explanation is mechanistically plausible and dossier-consistent, but precipitation was not independently manipulated, so it remains partly correlational.

4. How the explanation developed

Batches 1 and 2 first established that potential sign matters and exposed precipitation as a separate bottleneck: good electrochemical selectivity did not guarantee recovered yield when precipitation was saturated. Batches 3 and 4 showed that changing to S2/E2 suppressed precipitation and preserved a polarity asymmetry, shifting attention from simple solubility toward interfacial potential and efficiency.

Batch 5 rejected a monotonic voltage model because +2.0 V nearly eliminated selectivity and faradaic/transport efficiencies. Batch 6 identified +1.5 V as a high-efficiency region, while batch 7 showed that this regime could persist long enough to increase conversion. Batches 8 and 9 then rejected the idea that potential alone determines performance: the current cap independently created charge-limited and severely overdriven regimes.

Batches 10 and 11 demonstrated that the +1.5 V setting is not universally optimal across materials. Their behavior led to the effective-potential-shift hypothesis and reinforced the importance of precipitation and transport. Finally, batch 12 changed the time model: extrapolating the favorable 60-to-1800 s trend would have predicted continued improvement, but direct within-batch UV-vis evidence showed large efficiency decay by 7200 s.

5. Scope, unidentified quantities, and alternatives

This account is supported only for the tested anonymous materials, 0.50 mol/L initial reagent loading, 0.080 L nominal volume, fixed campaign cell, potentials from -1 to +2 V in the informative series, current caps from 10 to 500 mA, and times from 60 to 7200 s. It should not be treated as a real-material mechanism.

No actual current trace, passed charge, electrode potential at the interface, electrode area, temperature trajectory, product concentration, gas evolution, impedance, or species identity was observed. Therefore n, exchange-current densities, Tafel slopes, resistance, limiting current, kinetic orders, and deactivation constants cannot be identified. The potential-shift equation organizes the observations but is not uniquely fitted.

Solvent and electrolyte effects are confounded because only matched pairs were compared at the long common condition. Factorial solvent-by-electrolyte experiments would be required to separate conductivity, solvation, proton activity, double-layer capacitance, and precipitation contributions. There were also no independent replicate batches, so batch-to-batch variability cannot be estimated beyond the supplied instrument noise.

The long-time efficiency loss could reflect reagent depletion, concentration polarization, electrode fouling, electrolyte depletion, product inhibition, bubbles, or a growing side-product pool. The available measurements do not distinguish these alternatives. Likewise, the poor +2.0 V and 500 mA results could arise from electrochemical side reactions, transport starvation, or both. The data support a regime transition but not its microscopic identity.

The most defensible operational mechanism is therefore: material-dependent potential shifts determine where the electrode sits relative to a narrow productive overpotential window; the current cap determines whether the system is charge-limited, productively controlled, or transport/side-reaction dominated; material transport and precipitation properties determine whether electrochemically generated target remains accessible; and prolonged operation evolves the transport/interface state until efficiency declines. Batch 7—S2/E2, +1.5 V, 100 mA cap, 1800 s—best occupied the productive window in this campaign, but that recommendation is an empirical point within the stated scope, not evidence of a universal optimum.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific prior, example outcome, or true mechanism was supplied. The only prior information was the nominal anonymous-material dossier and the instrument/scoring contracts.

Supported:
- The self-developed claim of a bounded productive potential window was supported. For S2/E2 at 100 mA, batch 3 (+1.0 V, 600 s) was efficient but barely converting, batch 7 (+1.5 V, 1800 s) gave selectivity 0.988, faradaic efficiency 0.992, transport efficiency 0.996, and conversion 0.033, while batch 5 (+2.0 V, 600 s) collapsed to selectivity 0.006 and faradaic efficiency 0.011. Batch 5 was the clearest evidence against a monotonic voltage-benefit law.
- Polarity asymmetry was supported by batches 1–2 and 3–4: positive potentials consistently retained higher selectivity and efficiencies than comparable negative potentials, although low conversion and precipitation limited quantitative interpretation.
- A current-regime law was supported qualitatively. At +1.5 V in S2/E2, batch 8 with a 10 mA cap retained high efficiencies but produced no detectable yield, whereas batch 9 with a 500 mA cap had near-zero selectivity and faradaic efficiency. This supports low-cap charge limitation, an intermediate productive regime, and high-cap side-reaction/transport limitation.
- The nominal precipitation prior was qualitatively supported. E0/S0 produced precipitation signals of 1.0 in batches 1 and 2, while S2/E2 produced essentially none in batches 3–9 and 12. Batch 10, using S1/E1, also showed substantial precipitation (0.715). This supports a material-dependent solubility constraint, though not the exact nominal constants.

Contradicted or narrowed:
- A simple time-invariant Faraday law was contradicted. Batch 7 improved from the short batch-6 regime while retaining near-unity efficiencies, but in batch 12 the UV-vis faradaic and transport efficiencies fell from 1.00 at 1800 s to about 0.33 and 0.35 at 7200 s. Thus, extrapolating constant efficiency with time was not defensible.
- The initial expectation that conversion would simply rise toward depletion was narrowed: early conversion may rise, but long operation changes the interface or transport state and need not improve recovered yield. Batch 12 yielded 0.0265, not clearly above batch 7’s 0.0301.
- A universal +1.5 V optimum was contradicted by material comparisons. At the same nominal controls, batch 10 (S1/E1) was almost completely inefficient and batch 11 (S3/E3) was only intermediate.

Still untested or only suggestive:
- The additive effective-potential relation using solvent and electrolyte potential shifts was not directly tested because the campaign changed solvents and electrolytes together. It organizes batches 7, 10, and 11 but is not identified.
- Conductivity, diffusivity, proton activity, and double-layer capacitance were never varied independently, so their causal coefficients remain unknown.
- Precipitation plausibly reduced recovery in batches 1, 2, and 10, but no intervention isolated precipitation from correlated material and electrochemical effects.
- Electron stoichiometry, actual current, limiting current, Tafel behavior, electrode fouling, gas evolution, and product degradation were unmeasured.

Retrospectively, the largest judgment changes came from batch 5, which rejected monotonic voltage improvement; batches 8–9, which established a separate current-cap regime; and the within-batch measurements in batch 12, which revealed long-time efficiency decay.

2. One additional discriminating experiment

I would run one cross-paired batch with S2 solvent and E1 electrolyte, using 0.040 mol reagent in 0.080 L, a 100 mA cap, approximately +1.2 V, and 1800 s, with UV-vis before termination and a final assay. This approximately compensates for the declared S2/E1 potential shifts under the additive effective-overpotential explanation and can be compared with the existing productive S2/E2 batch 7 and poor S1/E1 batch 10.

If the cross-pair gave near-batch-7 selectivity and faradaic/transport efficiencies, it would strengthen the explanation that nominal potential shifts and solvent-controlled solubility/transport largely determine the operating window. If it instead resembled batch 10 despite the adjusted potential and S2 solvent, I would reduce confidence in the additive-shift law and favor electrolyte-specific reaction chemistry, nonadditive solvent–electrolyte coupling, or an interfacial effect not represented by the dossier. An intermediate result would imply that potential alignment matters but is insufficient without favorable transport or electrolyte chemistry.

3. Unused evidence, reliability, and effect of the goal

Most raw characterization artifacts were not analyzed beyond their public processed estimates and summarized peaks. Consequently, baseline shapes, replicate-level signals, spectral residuals, and possible peak evolution were unused. Nominal acid concentration, pKa, double-layer capacitance, and several diffusivity/conductivity values informed qualitative reasoning but were not quantitatively fitted. Cost and safety observations were also largely unused mechanistically because all selected batches remained within the safety limit. Intermediate pH measurements were sparse and could not establish a pH-rate law.

The least reliable predictions are those for untested solvent–electrolyte combinations, especially Q05–Q10, because the campaign used only matched pairs. Q11–Q12 are also weak because they combine 500 mA, 7200 s, lower reagent inventory, and ±0.8 V—an extrapolation beyond the single high-current observation in batch 9. All long-time predictions are uncertain because batch 12 provided only one trajectory showing state-dependent deterioration. Predictions of selective yield and score are especially fragile near zero because yield noise is 0.01 and the score has a multiplicative low-yield gate.

Batch 7 remains the best-supported recommendation, but it has no independent replicate, and its conversion and yield were only 0.033 and 0.030. Its efficiency advantage is much more reliable than its precise yield. The recommendation would be weakened by a replicate showing that those small product metrics were noise-dominated.

The explanatory research goal did affect evidence collection. I prioritized polarity, potential, time, current-cap, material, and within-batch time-course contrasts rather than repeatedly optimizing or replicating the highest-scoring condition. This produced stronger regime-level evidence but poorer repeatability estimates and left solvent and electrolyte effects confounded. There was no clear conflict with safety, but there was a tradeoff between broad mechanism discovery and precise optimization.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.72,
        "lower80": 0.48,
        "upper80": 0.9
      },
      "energy_efficiency": {
        "estimate": 0.32,
        "lower80": 0.15,
        "upper80": 0.5
      },
      "faradaic_efficiency": {
        "estimate": 0.46,
        "lower80": 0.28,
        "upper80": 0.64
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.102,
        "lower80": 0.0,
        "upper80": 0.24
      },
      "selective_product_yield": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.02
      },
      "transport_efficiency": {
        "estimate": 0.48,
        "lower80": 0.28,
        "upper80": 0.68
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.97,
        "lower80": 0.84,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.78,
        "lower80": 0.56,
        "upper80": 0.95
      },
      "faradaic_efficiency": {
        "estimate": 0.78,
        "lower80": 0.58,
        "upper80": 0.94
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.103,
        "lower80": 0.0,
        "upper80": 0.25
      },
      "selective_product_yield": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.018
      },
      "transport_efficiency": {
        "estimate": 0.76,
        "lower80": 0.55,
        "upper80": 0.93
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.25,
        "upper80": 0.82
      },
      "energy_efficiency": {
        "estimate": 0.15,
        "lower80": 0.03,
        "upper80": 0.35
      },
      "faradaic_efficiency": {
        "estimate": 0.22,
        "lower80": 0.05,
        "upper80": 0.46
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.049,
        "lower80": 0.0,
        "upper80": 0.18
      },
      "selective_product_yield": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.02
      },
      "transport_efficiency": {
        "estimate": 0.25,
        "lower80": 0.06,
        "upper80": 0.49
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.9,
        "lower80": 0.65,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.35,
        "lower80": 0.14,
        "upper80": 0.61
      },
      "faradaic_efficiency": {
        "estimate": 0.35,
        "lower80": 0.13,
        "upper80": 0.63
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.11,
        "lower80": 0.0,
        "upper80": 0.3
      },
      "selective_product_yield": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.025
      },
      "transport_efficiency": {
        "estimate": 0.38,
        "lower80": 0.14,
        "upper80": 0.66
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.5,
        "lower80": 0.19,
        "upper80": 0.79
      },
      "energy_efficiency": {
        "estimate": 0.2,
        "lower80": 0.04,
        "upper80": 0.45
      },
      "faradaic_efficiency": {
        "estimate": 0.25,
        "lower80": 0.06,
        "upper80": 0.52
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.265,
        "lower80": 0.05,
        "upper80": 0.46
      },
      "selective_product_yield": {
        "estimate": 0.02,
        "lower80": 0.002,
        "upper80": 0.065
      },
      "transport_efficiency": {
        "estimate": 0.35,
        "lower80": 0.11,
        "upper80": 0.63
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.9,
        "lower80": 0.68,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.55,
        "lower80": 0.27,
        "upper80": 0.81
      },
      "faradaic_efficiency": {
        "estimate": 0.55,
        "lower80": 0.27,
        "upper80": 0.82
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.497,
        "lower80": 0.26,
        "upper80": 0.71
      },
      "selective_product_yield": {
        "estimate": 0.12,
        "lower80": 0.035,
        "upper80": 0.28
      },
      "transport_efficiency": {
        "estimate": 0.65,
        "lower80": 0.36,
        "upper80": 0.88
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.45,
        "lower80": 0.15,
        "upper80": 0.75
      },
      "energy_efficiency": {
        "estimate": 0.16,
        "lower80": 0.02,
        "upper80": 0.39
      },
      "faradaic_efficiency": {
        "estimate": 0.2,
        "lower80": 0.03,
        "upper80": 0.46
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.176,
        "lower80": 0.02,
        "upper80": 0.39
      },
      "selective_product_yield": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.055
      },
      "transport_efficiency": {
        "estimate": 0.3,
        "lower80": 0.07,
        "upper80": 0.59
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.95,
        "lower80": 0.75,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.62,
        "lower80": 0.33,
        "upper80": 0.87
      },
      "faradaic_efficiency": {
        "estimate": 0.65,
        "lower80": 0.36,
        "upper80": 0.89
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.526,
        "lower80": 0.28,
        "upper80": 0.75
      },
      "selective_product_yield": {
        "estimate": 0.1,
        "lower80": 0.025,
        "upper80": 0.25
      },
      "transport_efficiency": {
        "estimate": 0.75,
        "lower80": 0.47,
        "upper80": 0.94
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.23,
        "upper80": 0.83
      },
      "energy_efficiency": {
        "estimate": 0.16,
        "lower80": 0.02,
        "upper80": 0.4
      },
      "faradaic_efficiency": {
        "estimate": 0.22,
        "lower80": 0.04,
        "upper80": 0.49
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.228,
        "lower80": 0.03,
        "upper80": 0.45
      },
      "selective_product_yield": {
        "estimate": 0.018,
        "lower80": 0.0,
        "upper80": 0.07
      },
      "transport_efficiency": {
        "estimate": 0.28,
        "lower80": 0.06,
        "upper80": 0.57
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.92,
        "lower80": 0.69,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.58,
        "lower80": 0.29,
        "upper80": 0.84
      },
      "faradaic_efficiency": {
        "estimate": 0.6,
        "lower80": 0.31,
        "upper80": 0.86
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.514,
        "lower80": 0.26,
        "upper80": 0.74
      },
      "selective_product_yield": {
        "estimate": 0.13,
        "lower80": 0.035,
        "upper80": 0.3
      },
      "transport_efficiency": {
        "estimate": 0.68,
        "lower80": 0.39,
        "upper80": 0.91
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.25,
        "lower80": 0.02,
        "upper80": 0.58
      },
      "energy_efficiency": {
        "estimate": 0.05,
        "lower80": 0.0,
        "upper80": 0.2
      },
      "faradaic_efficiency": {
        "estimate": 0.08,
        "lower80": 0.0,
        "upper80": 0.28
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.06,
        "lower80": 0.0,
        "upper80": 0.23
      },
      "selective_product_yield": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.035
      },
      "transport_efficiency": {
        "estimate": 0.08,
        "lower80": 0.0,
        "upper80": 0.29
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.35,
        "lower80": 0.04,
        "upper80": 0.7
      },
      "energy_efficiency": {
        "estimate": 0.04,
        "lower80": 0.0,
        "upper80": 0.18
      },
      "faradaic_efficiency": {
        "estimate": 0.06,
        "lower80": 0.0,
        "upper80": 0.24
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.133,
        "lower80": 0.0,
        "upper80": 0.32
      },
      "selective_product_yield": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.055
      },
      "transport_efficiency": {
        "estimate": 0.05,
        "lower80": 0.0,
        "upper80": 0.22
      }
    }
  ],
  "rationale": "Predictions combine the observed polarity asymmetry, material-dependent potential shifts, precipitation losses for S0/E0, long-time efficiency decay, and the collapse seen at a 500 mA cap. The new concentration is close to that studied, but the smaller reagent inventory and untested solvent–electrolyte pairings make long-time yields and efficiencies uncertain; intervals are therefore wider for 7200 s, crossed material pairs, and high-current cases. Score estimates also account for the strong low-yield multiplicative gate."
}
```
