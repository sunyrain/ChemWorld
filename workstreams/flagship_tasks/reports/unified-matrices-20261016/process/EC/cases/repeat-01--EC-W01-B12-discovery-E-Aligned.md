# repeat-01/EC-W01-B12-discovery-E-Aligned

既有科学公开材料；非provider内部推理。

来源：D:\Projects\ChemWorld-local-research\20261016-unified-matrices\attempt-01\repeat-01\EC-W01-B12-discovery-E-Aligned\participant\discovery-E-Aligned

## 同期笔记

### v1 · 公开事件 0

# Electrochemical campaign hypotheses

## Prior expectations (before physical experiments)

**H1 [tentative].** At fixed loading, conversion should grow with delivered charge and then saturate; however the current cap may not be reached when ohmic or transport limits dominate. Thus duration and current-cap effects should interact.

**H2 [tentative].** Product formation is polarity-specific: one potential sign should be productive, while the opposite sign may show little target yield or increased byproduct. Increasing absolute potential should initially improve conversion but eventually reduce selectivity/energy efficiency.

**H3 [tentative].** Conductivity and mass transport jointly govern performance. Nominally conductive media may improve ohmic efficiency, whereas thinner diffusion layers/higher diffusivity may improve transport; neither alone guarantees selectivity. Electrolyte potential shifts should translate the apparent potential-response curve.

Plan: use 12 independent batches at a fixed 0.020 mol in 0.050 L loading, spanning both potential signs, duration, current cap, solvents and electrolytes. Comparisons will be treated as provisional unless replicated or well separated relative to stated measurement uncertainty.

### v2 · 公开事件 49

# Electrochemical campaign hypotheses

## Current interpretation after batches 1–7

**H1 [supported in tested S0/E0 scope].** Delivered-charge response is strongly sublinear. At +0.5 V and 3600 s, raising the current cap from 25 to 100 to 300 mA increased measured conversion only about 0.020→0.062→0.069, while faradaic efficiency fell about 0.79→0.64→0.21 and transport efficiency fell about 0.77→0.63→0.22 (final-assay events runner-operation-0042, -0035, -0049). This is consistent with an increasingly transport-limited current and parasitic charge at high cap, not proportional current delivery. A cap is therefore not interchangeable with actual charge.

**H2 [supported but polarity mechanism unresolved].** S0/E0 at −1.0 V, 100 mA, 600 s was much less efficient than +1.0 V under the matched recipe (runner-operation-0014 versus -0007), supporting polarity-specific target chemistry. Because low conversion is near assay noise, the exact negative-polarity baseline remains uncertain.

**H3 [supported: peaked potential response].** At S0/E0, 100 mA, 3600 s, +0.5 V gave conversion/selectivity/energy efficiency ≈0.062/0.870/0.799; +1.0 V gave ≈0.053/0.926/0.614; +2.0 V collapsed faradaic/transport performance and target yield (events runner-operation-0035, -0021, -0028). Potential improves neither rate nor efficiency monotonically; a parasitic high-potential pathway is likely. The optimum depends on the weighted objective: +0.5 favors yield/energy, +1.0 favors selectivity.

**H4 [unresolved confound].** Precipitation signal is near unity in every S0/E0 assay, so its meaning cannot yet be separated from electrolyte identity. Upcoming solvent/electrolyte changes test whether nominal solubility properties shift this channel and whether that co-varies with product recovery.

Next: hold loading, +0.5 V, 100 mA, 3600 s while varying solvent/electrolyte. Evidence contradicting H1 would be a material where 300 mA remains high in transport/faradaic efficiency; evidence against H3 would be a shifted electrolyte where +2 V is productive, consistent with a translated potential window rather than a universal threshold.

### v3 · 公开事件 84

# Electrochemical campaign hypotheses

## Final source-stage interpretation (12 batches)

All claims concern the fixed tested loading (0.020 mol reagent in 0.050 L solvent). Final-assay uncertainties are approximately 0.01 for conversion/yield, 0.012 for selectivity/faradaic/ohmic efficiency, 0.014 for transport efficiency, and 0.016 for energy efficiency; isolated differences near these scales are not treated as effects.

**H1 [supported in S0/E0 scope].** Response to current cap is strongly sublinear and efficiency deteriorates at high cap. At +0.5 V for 3600 s, 25→100→300 mA changed conversion about 0.020→0.062→0.069 but faradaic efficiency about 0.79→0.64→0.21 and transport efficiency about 0.77→0.63→0.22 (runner-operation-0042, -0035, -0049). A predictive model should use an effective current limited by transport/interface kinetics, not equate the cap with delivered current. Short-to-long duration at +1 V (600→3600 s) raised conversion from about 0.018 to 0.053 (runner-operation-0007, -0021), compatible with accumulation followed by saturation, but only two durations were tested.

**H2 [supported qualitatively].** Polarity is asymmetric: matched S0/E0 ±1 V, 100 mA, 600 s produced much poorer efficiency at negative polarity (runner-operation-0014 versus -0007). Exact target-yield differences at this low-conversion regime are noisy, so the mechanistic assignment remains qualitative.

**H3 [supported in S0/E0; translated-window alternative retained].** The potential response is peaked rather than monotonic. At 100 mA for 3600 s, +0.5 V gave conversion/selectivity/energy efficiency ≈0.062/0.870/0.799, +1.0 V ≈0.053/0.926/0.614, and +2.0 V collapsed conversion and faradaic/transport efficiency (runner-operation-0035, -0021, -0028). This supports productive activation at moderate positive potential plus a high-potential parasitic pathway. Electrolyte/solvent standard-potential shifts may translate the window; the campaign does not fully map those interactions.

**H4 [supported material dependence, mechanism unresolved].** At +0.5 V, 100 mA, 3600 s, solvents changed selectivity and efficiencies without a clearly resolved conversion shift: S0/S1/S2/S3 final events are runner-operation-0035/-0056/-0063/-0070. S1 increased transport relative to S0 but target yield was lower; S2 lowered selectivity; S3 lowered faradaic/transport efficiency. These deviations show hidden solvation/interface factors beyond nominal conductivity.

Changing electrolyte from E0 to E1 under the same S0 operating point increased conversion to ≈0.082, transport efficiency to ≈0.748, and reduced precipitation signal to ≈0.862 (runner-operation-0077). E3 eliminated the precipitation signal but had lower conversion and transport/faradaic efficiency (runner-operation-0084). Thus precipitation propensity is electrolyte-sensitive but absence of precipitation does not itself maximize electrochemical performance. E2 was not tested, and material-by-potential/current interactions remain unresolved.

**Working predictive account.** Productive positive-polarity kinetics rise into a moderate-potential window; effective rate is bounded by transport and available current. Conversion grows sublinearly with time/effective charge. Faradaic and transport efficiencies decrease when the cap substantially exceeds the medium-dependent limiting current, while excessive positive potential activates a severe parasitic pathway. Material shifts modify conductivity, limiting transport, pH/precipitation, and the location of the potential window. Negative polarity uses a substantially less productive pathway in the tested region.

**Recommendation decision.** Batch 11 (S0/E1, +0.5 V, 100 mA, 3600 s) is the most balanced operating recommendation: it had the highest observed score (0.5170), highest conversion among tested batches, useful yield, and strong transport/energy efficiency. Its score is essentially tied with batch 6 (0.5169) within measurement uncertainty, so this is not evidence that it is uniquely optimal; batch 6 is the lower-current efficiency-oriented alternative.

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
    "electrochemical_conversion": 0.01807035692036152,
    "electrochemical_selectivity": 0.9495708346366882,
    "energy_efficiency": 0.6409902572631836,
    "faradaic_efficiency": 0.6713747978210449,
    "ohmic_efficiency": 0.9695378541946411,
    "pH_normalized": 0.23218974471092224,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.6426710486412048
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
    "electrochemical_selectivity": 0.6259675025939941,
    "energy_efficiency": 0.24028417468070984,
    "faradaic_efficiency": 0.39323651790618896,
    "ohmic_efficiency": 0.9783756732940674,
    "pH_normalized": 0.2294943928718567,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.19194842875003815,
    "selective_product_yield": 0.012746867723762989,
    "transport_efficiency": 0.41949331760406494
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
    "electrochemical_conversion": 0.05328724533319473,
    "electrochemical_selectivity": 0.9259447455406189,
    "energy_efficiency": 0.6137293577194214,
    "faradaic_efficiency": 0.6031450033187866,
    "ohmic_efficiency": 0.9651492834091187,
    "pH_normalized": 0.23020939528942108,
    "precipitation_signal": 0.9868234395980835,
    "safety_risk": 0.05933958664536476,
    "score": 0.4611680805683136,
    "selective_product_yield": 0.04442897066473961,
    "transport_efficiency": 0.6197019219398499
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
      "potential_V": 2
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
    "cost": 0.287880003452301,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.02824951522052288,
    "ohmic_efficiency": 0.9879685640335083,
    "pH_normalized": 0.2295188158750534,
    "precipitation_signal": 0.987571656703949,
    "safety_risk": 0.05933958664536476,
    "score": 0.0032642087899148464,
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
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 0.5
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
    "cost": 0.28571999073028564,
    "electrochemical_conversion": 0.062289755791425705,
    "electrochemical_selectivity": 0.8696447014808655,
    "energy_efficiency": 0.7985026240348816,
    "faradaic_efficiency": 0.6418315768241882,
    "ohmic_efficiency": 0.9554193019866943,
    "pH_normalized": 0.2344796061515808,
    "precipitation_signal": 0.9868980646133423,
    "safety_risk": 0.05933958664536476,
    "score": 0.4908137917518616,
    "selective_product_yield": 0.05925723910331726,
    "transport_efficiency": 0.6313221454620361
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
      "current_mA": 25,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 0.5
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
    "cost": 0.285180002450943,
    "electrochemical_conversion": 0.020039275288581848,
    "electrochemical_selectivity": 0.8643509745597839,
    "energy_efficiency": 0.8456438779830933,
    "faradaic_efficiency": 0.7911400198936462,
    "ohmic_efficiency": 0.9892595410346985,
    "pH_normalized": 0.23120366036891937,
    "precipitation_signal": 0.9975283145904541,
    "safety_risk": 0.05933958664536476,
    "score": 0.5169432759284973,
    "selective_product_yield": 0.025722885504364967,
    "transport_efficiency": 0.7664567232131958
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
      "current_mA": 300,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 0.5
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
    "cost": 0.2871600091457367,
    "electrochemical_conversion": 0.06919393688440323,
    "electrochemical_selectivity": 0.86936354637146,
    "energy_efficiency": 0.383578896522522,
    "faradaic_efficiency": 0.2124265432357788,
    "ohmic_efficiency": 0.9035483002662659,
    "pH_normalized": 0.23021826148033142,
    "precipitation_signal": 0.982570469379425,
    "safety_risk": 0.05933958664536476,
    "score": 0.33179062604904175,
    "selective_product_yield": 0.05857371911406517,
    "transport_efficiency": 0.21582689881324768
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
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 0.5
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
    "cost": 0.3057200014591217,
    "electrochemical_conversion": 0.058069199323654175,
    "electrochemical_selectivity": 0.8486829400062561,
    "energy_efficiency": 0.8015425801277161,
    "faradaic_efficiency": 0.6843048930168152,
    "ohmic_efficiency": 0.9605118632316589,
    "pH_normalized": 0.23249587416648865,
    "precipitation_signal": 0.9908607602119446,
    "safety_risk": 0.08273958414793015,
    "score": 0.4899958372116089,
    "selective_product_yield": 0.033055298030376434,
    "transport_efficiency": 0.6778095364570618
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
      "solvent": 2,
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 0.5
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
    "cost": 0.33772000670433044,
    "electrochemical_conversion": 0.052169568836688995,
    "electrochemical_selectivity": 0.6612101793289185,
    "energy_efficiency": 0.6582878828048706,
    "faradaic_efficiency": 0.5710205435752869,
    "ohmic_efficiency": 0.9647567868232727,
    "pH_normalized": 0.24697262048721313,
    "precipitation_signal": 0.9939592480659485,
    "safety_risk": 0.10073958337306976,
    "score": 0.42407193779945374,
    "selective_product_yield": 0.0534735731780529,
    "transport_efficiency": 0.5918518304824829
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
      "solvent": 3,
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 0.5
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
    "cost": 0.3177199959754944,
    "electrochemical_conversion": 0.05650801211595535,
    "electrochemical_selectivity": 0.7696759700775146,
    "energy_efficiency": 0.7287520170211792,
    "faradaic_efficiency": 0.45005205273628235,
    "ohmic_efficiency": 0.9404974579811096,
    "pH_normalized": 0.23948635160923004,
    "precipitation_signal": 0.9837813377380371,
    "safety_risk": 0.11333958804607391,
    "score": 0.41333383321762085,
    "selective_product_yield": 0.028442129492759705,
    "transport_efficiency": 0.45140162110328674
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
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 0.5
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
    "cost": 0.28571999073028564,
    "electrochemical_conversion": 0.08230733871459961,
    "electrochemical_selectivity": 0.8462569117546082,
    "energy_efficiency": 0.8257542848587036,
    "faradaic_efficiency": 0.7403725981712341,
    "ohmic_efficiency": 0.953435480594635,
    "pH_normalized": 0.19873952865600586,
    "precipitation_signal": 0.8619048595428467,
    "safety_risk": 0.05933958664536476,
    "score": 0.5170444846153259,
    "selective_product_yield": 0.06045747920870781,
    "transport_efficiency": 0.7475525140762329
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
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": 0.5
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
    "cost": 0.28571999073028564,
    "electrochemical_conversion": 0.03584006056189537,
    "electrochemical_selectivity": 0.8076375126838684,
    "energy_efficiency": 0.7848061323165894,
    "faradaic_efficiency": 0.5260183811187744,
    "ohmic_efficiency": 0.977682888507843,
    "pH_normalized": 0.2733696401119232,
    "precipitation_signal": 0.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.4547591805458069,
    "selective_product_yield": 0.05415817350149155,
    "transport_efficiency": 0.5472433567047119
  }
}
```

## K1 封存报告

## Mechanistic account

### 1. Scope of the evidence

Twelve independent batches were studied. Every batch used 0.020 mol of limiting reagent in 0.050 L of one solvent, corresponding to the same nominal initial loading of 0.40 mol L⁻¹. The controlled variables were solvent S0–S3, electrolyte E0–E3, applied potential, current cap, and electrolysis duration. E2 was not tested. No loading, volume, or mixed-solvent series was performed.

Final-assay standard uncertainties were approximately 0.010 for conversion and selective-product yield, 0.012 for selectivity, faradaic efficiency and ohmic efficiency, 0.014 for transport efficiency, and 0.016 for energy efficiency. There were no true replicates. I therefore regard differences comparable to those uncertainties as unresolved, especially near zero conversion.

### 2. Proposed process structure

I interpret the system as a positive-polarity electrochemical conversion with five coupled elements:

1. **Potential-dependent activation.** A productive electrode pathway becomes accessible in a moderate positive-potential window.
2. **A competing high-potential pathway.** Excess positive driving force diverts current into parasitic electrochemistry or interface degradation, sharply reducing faradaic and transport performance.
3. **Transport-limited current.** The configured current is a cap, not necessarily the current actually sustained productively. At high caps, reactant supply to the interface becomes limiting and an increasing fraction of charge is unproductive.
4. **Time-dependent accumulation and depletion.** Conversion grows with electrolysis time, but much less than proportionally once transport, depletion, or side reactions become important.
5. **Material-dependent shifts.** Solvent and electrolyte affect the effective potential window, mass transport, conductivity, proton activity, precipitation, selectivity, and possibly product recovery through both their declared nominal properties and fixed hidden residual factors.

A useful conceptual model is

η = sV − [E* + ΔE_solvent + ΔE_electrolyte + ξ_interface] − I_actual R_cell,

where η is the effective productive overpotential, s identifies the productive polarity, and ξ_interface represents the fixed but unobserved world-specific interfacial contribution.

The actual productive current could be represented as

I_actual ≈ min(I_cap, I_lim),

or more smoothly as

I_actual = I_cap I_lim/(I_cap + I_lim),

with a limiting current of the approximate form

I_lim ∝ A nF D_eff C/δ_eff.

The fixture area, gap, and base resistance were constant within this campaign but were not observed. Solvent and electrolyte modify D_eff, δ_eff, conductivity, and interfacial kinetics.

A simple conversion law consistent with the data is

X(t) = X_max[1 − exp(−k_eff t)],

where k_eff depends on productive current and potential. One possible decomposition is

k_eff ∝ I_actual × FE(η,I_cap/I_lim) × g_transport/(n₀F).

The faradaic efficiency could decrease both below the productive potential window and above a parasitic threshold. A schematic response is

FE = FE_max × f_activation(η) × f_parasitic(η) × f_transport(I_cap/I_lim),

where f_activation rises with positive η, f_parasitic falls at excessive η, and f_transport falls as the current cap exceeds the medium-dependent limiting current.

Observed selective-product yield is not perfectly equal to conversion times selectivity. I would model it approximately as

Y_obs ≈ X × S_product × R_material,precipitation + assay error,

where R is an effective recovery or survival factor. The assay channels may also be independently noisy synthetic estimators, so exact algebraic closure should not be imposed.

### 3. Evidence for polarity dependence

Batches 1 and 2 were a matched polarity comparison in S0/E0 at 100 mA for 600 s.

- **Batch 1, +1.0 V:** conversion 0.0181, selectivity 0.9496, faradaic efficiency 0.6714, transport efficiency 0.6427, energy efficiency 0.6410, and ohmic efficiency 0.9695.
- **Batch 2, −1.0 V:** reported conversion 0, selectivity 0.6260, faradaic efficiency 0.3932, transport efficiency 0.4195, energy efficiency 0.2403, and ohmic efficiency 0.9784.

The positive-potential batch was clearly superior in faradaic, transport, selectivity, and energy channels. Conversion was close to the assay uncertainty in both cases, and batch 2 reported a small yield of 0.0127 despite zero clipped conversion. I therefore infer polarity asymmetry confidently but do not treat the low-conversion yield values as a precise mass balance. A plausible alternative is that both polarities permit some reaction but negative polarity predominantly drives a different, inefficient route.

### 4. Time response

Batches 1 and 3 differed principally in duration at +1.0 V, 100 mA, S0/E0:

- **Batch 1, 600 s:** conversion 0.0181 and yield 0.
- **Batch 3, 3600 s:** conversion 0.0533 and yield 0.0444.

A sixfold increase in time produced only about a threefold increase in measured conversion. Faradaic efficiency changed from 0.6714 to 0.6031 and transport efficiency from 0.6427 to 0.6197. This is consistent with sublinear accumulation caused by depletion, increasing concentration polarization, product loss, or time-dependent side reactions. With only two durations and no replicate, a saturating exponential cannot be distinguished from other concave laws such as X proportional to the square root of time.

### 5. Potential window and parasitic high-potential chemistry

Batches 3–5 compared potential in S0/E0 at 100 mA for 3600 s:

- **Batch 5, +0.5 V:** conversion 0.0623, selectivity 0.8696, yield 0.0593, faradaic efficiency 0.6418, transport efficiency 0.6313, energy efficiency 0.7985.
- **Batch 3, +1.0 V:** conversion 0.0533, selectivity 0.9259, yield 0.0444, faradaic efficiency 0.6031, transport efficiency 0.6197, energy efficiency 0.6137.
- **Batch 4, +2.0 V:** conversion 0, selectivity 0, yield 0.0008, faradaic efficiency 0.0282, transport efficiency 0, energy efficiency 0.

The response is strongly nonmonotonic. Moving from +0.5 to +1.0 V did not measurably improve conversion and reduced energy efficiency, although selectivity was higher at +1.0 V. At +2.0 V the productive system collapsed. Ohmic efficiency remained high in batch 4 (0.9880), so ordinary bulk resistance alone cannot explain the collapse. The most plausible account is activation of a parasitic electron-transfer or interface pathway at excessive positive overpotential. Electrode passivation is another plausible explanation, although it was not directly measured.

The location of this window is not necessarily universal. Declared solvent and electrolyte standard-potential shifts should translate effective overpotential, but each alternative material was tested at only one potential. Thus +2.0 V is demonstrated to be destructive only for the S0/E0 combination under these conditions.

### 6. Current cap and transport limitation

Batches 5–7 varied current cap at +0.5 V for 3600 s in S0/E0:

- **Batch 6, 25 mA:** conversion 0.0200, yield 0.0257, faradaic efficiency 0.7911, transport efficiency 0.7665, ohmic efficiency 0.9893, energy efficiency 0.8456.
- **Batch 5, 100 mA:** conversion 0.0623, yield 0.0593, faradaic efficiency 0.6418, transport efficiency 0.6313, ohmic efficiency 0.9554, energy efficiency 0.7985.
- **Batch 7, 300 mA:** conversion 0.0692, yield 0.0586, faradaic efficiency 0.2124, transport efficiency 0.2158, ohmic efficiency 0.9035, energy efficiency 0.3836.

Increasing the cap from 25 to 100 mA increased conversion substantially, but increasing it another threefold to 300 mA added almost no conversion or yield. Meanwhile faradaic and transport efficiencies collapsed at 300 mA. This is the clearest evidence for a medium-dependent limiting current. It also shows why charge computed as I_cap × time would be misleading: the cap is not a direct measure of useful delivered charge.

The gradual decline in ohmic efficiency with current is consistent with increasing I·R loss, but it is smaller than the faradaic and transport losses. The primary high-current limitation therefore appears to be mass transport or interfacial supply rather than only bulk resistance.

### 7. Solvent effects

Batches 5, 8, 9, and 10 compared S0–S3 with E0 at +0.5 V, 100 mA, and 3600 s.

- **S0, batch 5:** conversion 0.0623, selectivity 0.8696, yield 0.0593, FE 0.6418, transport 0.6313, energy 0.7985.
- **S1, batch 8:** conversion 0.0581, selectivity 0.8487, yield 0.0331, FE 0.6843, transport 0.6778, energy 0.8015.
- **S2, batch 9:** conversion 0.0522, selectivity 0.6612, yield 0.0535, FE 0.5710, transport 0.5919, energy 0.6583.
- **S3, batch 10:** conversion 0.0565, selectivity 0.7697, yield 0.0284, FE 0.4501, transport 0.4514, energy 0.7288.

Most conversion differences are within roughly one conversion standard uncertainty, so there is no strong evidence for a solvent conversion ranking at this single operating point. The selectivity loss in S2 and the faradaic/transport losses in S3 are much larger than measurement uncertainty. S1 showed somewhat better transport and faradaic efficiencies than S0, consistent with its higher nominal relative diffusivity, but its observed product yield was substantially lower. This suggests an additional solvent-dependent recovery, product-stability, or interfacial-selectivity factor.

The nominal properties alone therefore do not provide a complete ranking. In particular, conductivity, diffusivity, proton activity, capacitance, solubility, and potential shift are coupled rather than independently varied, and the dossier explicitly permits fixed hidden residuals.

### 8. Electrolyte, acidity, and precipitation

Batches 5, 11, and 12 compared E0, E1, and E3 in S0 at +0.5 V, 100 mA, and 3600 s:

- **E0, batch 5:** conversion 0.0623, yield 0.0593, transport 0.6313, FE 0.6418, pH-normalized 0.2345, precipitation signal 0.9869.
- **E1, batch 11:** conversion 0.0823, yield 0.0605, transport 0.7476, FE 0.7404, pH-normalized 0.1987, precipitation signal 0.8619.
- **E3, batch 12:** conversion 0.0358, yield 0.0542, transport 0.5472, FE 0.5260, pH-normalized 0.2734, precipitation signal 0.

E1 gave the strongest observed conversion and transport performance. Its nominal thin diffusion layer and high diffusivity provide a plausible transport explanation despite its lower nominal bulk conductivity than E0. E3 had high nominal conductivity but a much thicker diffusion layer and gave poorer transport performance. This supports a mass-transfer term resembling D/δ rather than conductivity alone.

The pH-normalized ordering also follows the nominal acid formulations qualitatively: E1 appeared most acidic, E0 intermediate, and E3 least acidic. Precipitation was strongly electrolyte-dependent. E0 was near unity, E1 remained high but lower, and E3 was zero. Nevertheless, eliminating the precipitation signal did not maximize conversion or efficiency. Precipitation is therefore not the sole performance-limiting mechanism.

I cannot determine whether the precipitation channel measures actual deposited material, equilibrium propensity, or a correlated assay proxy. It may reduce recovery, alter the interface, or merely report a parallel equilibrium. The E3 result shows that a low precipitation signal is insufficient for high electrochemical performance. E2 was never tested, so its behavior is an extrapolation only.

### 9. Interpretation of yield and selectivity

Conversion, selectivity, and selective-product yield are correlated but not exactly algebraically linked. For example, batch 11 had conversion 0.0823 and selectivity 0.8463, whose product is near 0.070, while reported yield was 0.0605. Batch 12 had conversion 0.0358 and selectivity 0.8076 but yield 0.0542. Near-zero batches also showed clipping inconsistencies.

Possible explanations include independent channel noise, recovery effects, precipitation or phase partitioning, temporal differences embedded in the synthetic calibration, or a definition of selective-product yield that is not simply conversion times electrochemical selectivity. I would not fit a strict mass-balance identity without additional calibration evidence.

### 10. Safety and cost

All tested recipes remained far below the stated safety limit; the common S0/E0 batches showed safety risk around 0.0593. No experiment supplied evidence that safety was the active determinant of the electrochemical trends. This only establishes safety within the tested loading and operating window. It does not justify extrapolation to greater concentration, volume, duration, or more extreme potential.

### 11. What changed the explanation

The matched polarity experiment in batches 1–2 established that the productive pathway favors positive potential. The longer batch 3 showed that reaction accumulates with time but sublinearly. Batch 4 was decisive in rejecting a monotonic “more positive potential gives more conversion” model: +2.0 V destroyed productive performance while ohmic efficiency remained high. Batch 5 located a more favorable moderate-potential point. Batches 6–7 then rejected a proportional charge model by showing diminishing conversion and severe efficiency loss at 300 mA. Solvent batches 8–10 demonstrated that material effects cannot be reduced to bulk conductivity. Finally, batches 11–12 separated transport performance from precipitation: E1 improved transport and conversion while E3 eliminated precipitation without becoming the best electrochemical medium.

### 12. Unidentifiable factors and alternatives

The following remain unidentifiable from this campaign:

- Actual current and total charge, as distinct from the current cap.
- Electrode area, gap, base resistance, and the absolute limiting current.
- Electron stoichiometry and the identities of target, impurity, or degradation products.
- Whether the +2.0 V failure is solution-phase side reaction, electrode passivation, solvent/electrolyte decomposition, or another interface process.
- The separate causal effects of conductivity, diffusivity, diffusion-layer thickness, capacitance, acidity, solubility, and potential shift because these properties changed together.
- Material-by-potential and material-by-current interactions.
- The kinetic law at long time, since only 600 and 3600 s were compared and not at every condition.
- E2 behavior and responses at other loadings or volumes.
- Whether precipitation directly removes product/reactant, passivates the electrode, or is only a correlated equilibrium signal.

Plausible alternative models include a passivation model in which surface coverage grows with potential and time; a two-pathway kinetic model with productive and destructive currents; or a purely empirical response surface with a material-specific potential optimum and current saturation. The current evidence favors the two-pathway, transport-limited account because it explains polarity asymmetry, the +2.0 V collapse, the 300 mA efficiency loss, and the electrolyte dependence with one coherent structure, but it is not uniquely proven.

### 13. Overall conclusion

Within the tested 0.40 mol L⁻¹ batches, the world behaves like a transport-limited positive-polarity electrochemical conversion with a finite productive potential window. Moderate positive potential activates target formation; excessive potential activates a severe competing process. Raising current cap initially increases conversion, but beyond a medium-dependent limiting current it mainly lowers faradaic, transport, ohmic, and energy efficiencies. Solvent and electrolyte jointly shift mass transport, interfacial kinetics, selectivity, acidity, precipitation, and the effective potential window. E1 in S0 at +0.5 V and 100 mA for 3600 s, batch 11, was the strongest balanced observed condition, but its score was effectively tied with the efficient low-current batch 6 and should not be interpreted as a uniquely identified global optimum.

## K2 封存报告

### 1. Status of supplied and self-developed claims

No instance-specific prior response law, known optimum, or example outcome was supplied. The supplied material dossier provided nominal mechanistic properties—conductivity, diffusivity, diffusion-layer thickness, acidity, solubility, capacitance, and potential shifts—but explicitly did not provide selectivity or faradaic-efficiency rankings. My initial polarity, saturation, and transport claims were self-developed and recorded before the experiments.

- **Current-cap/transport law: supported within S0/E0.** Batches 6, 5, and 7 used 25, 100, and 300 mA at +0.5 V for 3600 s. Conversion rose only 0.0200→0.0623→0.0692, while faradaic efficiency fell 0.7911→0.6418→0.2124 and transport efficiency fell 0.7665→0.6313→0.2158. This changed my view from a generic charge-response hypothesis to a specific conclusion that the configured current is a cap and cannot be treated as useful current. The exact min-current or harmonic-current equation remains untested.

- **Sublinear time response: provisionally supported.** At +1.0 V and 100 mA, extending electrolysis from 600 s in batch 1 to 3600 s in batch 3 raised conversion from 0.0181 to 0.0533, much less than sixfold. This supports a concave response, but two durations cannot distinguish depletion, exponential saturation, diffusion-controlled square-root behavior, or progressive passivation.

- **Productive polarity asymmetry: supported qualitatively.** Matched batches 1 and 2 showed much better selectivity, faradaic efficiency, transport efficiency, and energy efficiency at +1.0 V than at −1.0 V. Conversion was near the assay noise floor, so the size of the polarity effect on conversion or yield was not precisely identified.

- **Monotonic potential benefit: contradicted.** Batch 4 at +2.0 V gave essentially zero conversion and selectivity, faradaic efficiency 0.0282, and zero reported transport and energy efficiencies. Batches 5 and 3 at +0.5 and +1.0 V were productive. Batch 4 was the main evidence that changed my explanation toward a finite productive window plus a high-potential parasitic or passivating process.

- **A universal potential window: untested.** The peaked response was mapped only for S0/E0. The supplied solvent and electrolyte potential shifts suggest that the window could move, but E1, E3, S1, S2, and S3 were each examined at only one potential.

- **Conductivity as the dominant material descriptor: contradicted as a sufficient explanation.** E1 in batch 11 had stronger transport efficiency and conversion than E0 in batch 5 despite lower nominal bulk conductivity. E3 in batch 12 had high nominal conductivity but weaker transport performance. The E1/E3 ordering is more consistent with diffusivity and diffusion-layer thickness also mattering, although correlated material changes prevent identification of individual coefficients.

- **Nominal precipitation differences: qualitatively supported.** The precipitation signal was about 0.987 for E0 in batch 5, 0.862 for E1 in batch 11, and zero for E3 in batch 12. However, the stronger causal claim that suppressing precipitation improves electrochemical performance was contradicted: E3 eliminated the signal but did not maximize conversion, yield, or efficiency.

- **Solvent-specific hidden effects: supported, but not mechanistically resolved.** Batches 5 and 8–10 had similar conversion within roughly assay uncertainty, yet S2 in batch 9 had distinctly poorer selectivity and S3 in batch 10 had distinctly poorer faradaic and transport efficiencies. Nominal properties alone did not explain all of these differences.

- **Strict yield = conversion × selectivity: not supported.** Several batches deviated from that identity, especially near the detection floor and in batch 12. Independent assay noise, recovery, partitioning, or a different channel definition are plausible, but the proposed recovery factor was not independently measured.

### 2. One discriminating additional experiment

I would run one S0/E0 batch at the original 0.020 mol/0.050 L loading, +0.5 V, 300 mA, for 1200 s, followed by the final assay. It would have the same nominal capped charge as batch 5 at 100 mA for 3600 s, while separating high current from long exposure.

- If the new batch produced substantially less conversion and yield than batch 5 and retained the low faradaic and transport efficiencies seen in batch 7, that would strengthen the leading explanation that 300 mA exceeds a transport/interfacial limiting current and diverts charge into parasitic processes.
- If it produced conversion and yield comparable to batch 5 despite the shorter duration, a nominal-charge model would become more plausible, although the efficiency channels would still determine how much parasitic current was present.
- If it outperformed batch 5 and did not show the efficiency collapse of batch 7, I would reduce confidence in a current-cap-controlled limitation and favor a time-dependent alternative: progressive passivation, depletion, or product degradation during the 3600 s exposure may have caused much of batch 7’s poor result.
- If both conversion and efficiencies were already poor after 1200 s, that would distinguish an immediate high-current penalty from a slowly accumulated passivation mechanism, though it would not by itself separate mass transport from rapid interfacial damage.

This experiment would not identify electrode area or actual current, but it would be more diagnostic than another unmatched optimization point.

### 3. Unused evidence, weak predictions, and goal effects

The raw spectral artifacts and detailed peak shapes were not used in my quantitative account; I relied on calibrated processed estimates. Intermediate UV–visible measurements were used mainly as consistency checks rather than fitted jointly with final assays. I also did not quantitatively exploit cost, small temperature changes, raw mass-balance fields, capacitance, proton activity, or Ksp values. Those variables were either invariant, weakly sampled, or too confounded with other material properties to support separate coefficients.

The least reliable sealed predictions are Q11 and Q12 because 500 mA exceeds the largest tested cap of 300 mA and combines that extrapolation with 7200 s, a duration twice the longest observed. Long-duration yields in Q03–Q10 are also uncertain because the campaign contained only one matched duration comparison and never used 7200 s. Predictions involving negative polarity with E1, E3, or S2—Q05, Q07, and Q09—are especially weak because material-by-polarity interactions were never measured. All prediction queries also changed the loading from 0.40 to 0.48 mol L⁻¹ and halved the volume, neither of which was experimentally varied. Yield predictions are less secure than efficiency predictions because yield did not obey a strict observed algebraic relationship with conversion and selectivity.

The batch 11 recommendation is also not uniquely reliable. Its score of 0.5170 was effectively tied with batch 6 at 0.5169, and neither condition was replicated. Batch 11 favors throughput and balanced performance; batch 6 is a credible lower-current, efficiency-oriented alternative. Furthermore, E2 was not tested, and the material-specific potential optima were not mapped.

The assigned goal emphasized explanatory and predictive understanding, with public optimization score secondary. That affected evidence collection: I spent batches on polarity, potential, time, current, solvents, and electrolytes rather than repeatedly optimizing the best score. This breadth was useful for mechanism development but left few degrees of freedom for replication, loading effects, interaction mapping, or precise uncertainty estimation. I found no direct conflict between the research goal and making an operating recommendation, but the mechanistic breadth made the recommendation less statistically secure than a dedicated optimization campaign would have made it.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.65,
        "lower80": 0.48,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.3,
        "lower80": 0.16,
        "upper80": 0.42
      },
      "faradaic_efficiency": {
        "estimate": 0.42,
        "lower80": 0.3,
        "upper80": 0.52
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.13,
        "lower80": 0.03,
        "upper80": 0.27
      },
      "selective_product_yield": {
        "estimate": 0.008,
        "lower80": 0,
        "upper80": 0.025
      },
      "transport_efficiency": {
        "estimate": 0.45,
        "lower80": 0.31,
        "upper80": 0.56
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.91,
        "lower80": 0.82,
        "upper80": 0.96
      },
      "energy_efficiency": {
        "estimate": 0.7,
        "lower80": 0.58,
        "upper80": 0.81
      },
      "faradaic_efficiency": {
        "estimate": 0.64,
        "lower80": 0.55,
        "upper80": 0.72
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.47,
        "lower80": 0.32,
        "upper80": 0.57
      },
      "selective_product_yield": {
        "estimate": 0.022,
        "lower80": 0.008,
        "upper80": 0.045
      },
      "transport_efficiency": {
        "estimate": 0.63,
        "lower80": 0.54,
        "upper80": 0.71
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.48,
        "upper80": 0.75
      },
      "energy_efficiency": {
        "estimate": 0.27,
        "lower80": 0.14,
        "upper80": 0.4
      },
      "faradaic_efficiency": {
        "estimate": 0.4,
        "lower80": 0.28,
        "upper80": 0.51
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.33,
        "lower80": 0.24,
        "upper80": 0.43
      },
      "selective_product_yield": {
        "estimate": 0.06,
        "lower80": 0.025,
        "upper80": 0.11
      },
      "transport_efficiency": {
        "estimate": 0.43,
        "lower80": 0.3,
        "upper80": 0.55
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.9,
        "lower80": 0.82,
        "upper80": 0.96
      },
      "energy_efficiency": {
        "estimate": 0.68,
        "lower80": 0.55,
        "upper80": 0.79
      },
      "faradaic_efficiency": {
        "estimate": 0.61,
        "lower80": 0.51,
        "upper80": 0.7
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.53,
        "lower80": 0.43,
        "upper80": 0.63
      },
      "selective_product_yield": {
        "estimate": 0.19,
        "lower80": 0.11,
        "upper80": 0.3
      },
      "transport_efficiency": {
        "estimate": 0.61,
        "lower80": 0.5,
        "upper80": 0.7
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.45,
        "upper80": 0.73
      },
      "energy_efficiency": {
        "estimate": 0.36,
        "lower80": 0.2,
        "upper80": 0.51
      },
      "faradaic_efficiency": {
        "estimate": 0.5,
        "lower80": 0.37,
        "upper80": 0.62
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.37,
        "lower80": 0.25,
        "upper80": 0.48
      },
      "selective_product_yield": {
        "estimate": 0.07,
        "lower80": 0.025,
        "upper80": 0.14
      },
      "transport_efficiency": {
        "estimate": 0.55,
        "lower80": 0.42,
        "upper80": 0.68
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.86,
        "lower80": 0.77,
        "upper80": 0.94
      },
      "energy_efficiency": {
        "estimate": 0.75,
        "lower80": 0.62,
        "upper80": 0.86
      },
      "faradaic_efficiency": {
        "estimate": 0.72,
        "lower80": 0.61,
        "upper80": 0.82
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.58,
        "lower80": 0.48,
        "upper80": 0.68
      },
      "selective_product_yield": {
        "estimate": 0.24,
        "lower80": 0.14,
        "upper80": 0.37
      },
      "transport_efficiency": {
        "estimate": 0.74,
        "lower80": 0.63,
        "upper80": 0.84
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.52,
        "lower80": 0.35,
        "upper80": 0.68
      },
      "energy_efficiency": {
        "estimate": 0.16,
        "lower80": 0.05,
        "upper80": 0.31
      },
      "faradaic_efficiency": {
        "estimate": 0.3,
        "lower80": 0.18,
        "upper80": 0.43
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.27,
        "lower80": 0.15,
        "upper80": 0.38
      },
      "selective_product_yield": {
        "estimate": 0.035,
        "lower80": 0.005,
        "upper80": 0.09
      },
      "transport_efficiency": {
        "estimate": 0.34,
        "lower80": 0.21,
        "upper80": 0.48
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.79,
        "lower80": 0.66,
        "upper80": 0.9
      },
      "energy_efficiency": {
        "estimate": 0.74,
        "lower80": 0.59,
        "upper80": 0.85
      },
      "faradaic_efficiency": {
        "estimate": 0.55,
        "lower80": 0.42,
        "upper80": 0.68
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.49,
        "lower80": 0.36,
        "upper80": 0.59
      },
      "selective_product_yield": {
        "estimate": 0.14,
        "lower80": 0.07,
        "upper80": 0.25
      },
      "transport_efficiency": {
        "estimate": 0.55,
        "lower80": 0.42,
        "upper80": 0.68
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.45,
        "lower80": 0.29,
        "upper80": 0.62
      },
      "energy_efficiency": {
        "estimate": 0.16,
        "lower80": 0.04,
        "upper80": 0.32
      },
      "faradaic_efficiency": {
        "estimate": 0.3,
        "lower80": 0.17,
        "upper80": 0.43
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.26,
        "lower80": 0.14,
        "upper80": 0.37
      },
      "selective_product_yield": {
        "estimate": 0.035,
        "lower80": 0.004,
        "upper80": 0.09
      },
      "transport_efficiency": {
        "estimate": 0.35,
        "lower80": 0.22,
        "upper80": 0.49
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.7,
        "lower80": 0.56,
        "upper80": 0.82
      },
      "energy_efficiency": {
        "estimate": 0.75,
        "lower80": 0.6,
        "upper80": 0.85
      },
      "faradaic_efficiency": {
        "estimate": 0.62,
        "lower80": 0.48,
        "upper80": 0.73
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.49,
        "lower80": 0.36,
        "upper80": 0.6
      },
      "selective_product_yield": {
        "estimate": 0.14,
        "lower80": 0.07,
        "upper80": 0.25
      },
      "transport_efficiency": {
        "estimate": 0.6,
        "lower80": 0.47,
        "upper80": 0.71
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.42,
        "upper80": 0.75
      },
      "energy_efficiency": {
        "estimate": 0.1,
        "lower80": 0.02,
        "upper80": 0.22
      },
      "faradaic_efficiency": {
        "estimate": 0.08,
        "lower80": 0.03,
        "upper80": 0.2
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.21,
        "lower80": 0.1,
        "upper80": 0.33
      },
      "selective_product_yield": {
        "estimate": 0.045,
        "lower80": 0.01,
        "upper80": 0.12
      },
      "transport_efficiency": {
        "estimate": 0.1,
        "lower80": 0.03,
        "upper80": 0.24
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.88,
        "lower80": 0.76,
        "upper80": 0.96
      },
      "energy_efficiency": {
        "estimate": 0.2,
        "lower80": 0.05,
        "upper80": 0.34
      },
      "faradaic_efficiency": {
        "estimate": 0.12,
        "lower80": 0.03,
        "upper80": 0.23
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.32,
        "lower80": 0.2,
        "upper80": 0.43
      },
      "selective_product_yield": {
        "estimate": 0.16,
        "lower80": 0.07,
        "upper80": 0.29
      },
      "transport_efficiency": {
        "estimate": 0.12,
        "lower80": 0.03,
        "upper80": 0.25
      }
    }
  ],
  "rationale": "Predictions anchor the ±0.8 V cases to the campaign’s matched-polarity and +0.5/+1.0 V results, extrapolate useful product accumulation to 7200 s at the new 0.48 M loading, and apply the observed E1, E3, and S2 shifts. Positive polarity is expected to retain high selectivity, whereas negative polarity is less efficient. The 500 mA cases receive severe faradaic and transport penalties based on the observed 100-to-300 mA saturation. Intervals include assay noise plus substantial extrapolation uncertainty for longer duration, altered loading, material–potential interactions, and high current. Scores also account for the published yield gate and unreported conversion/ohmic contributions."
}
```
