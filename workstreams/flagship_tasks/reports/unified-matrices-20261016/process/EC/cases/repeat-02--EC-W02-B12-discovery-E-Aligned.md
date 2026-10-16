# repeat-02/EC-W02-B12-discovery-E-Aligned

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-02\EC-W02-B12-discovery-E-Aligned\participant\discovery-E-Aligned

## 同期笔记

### v1 · 公开事件 0

# Pre-experiment hypotheses

**H1 [tentative].** At fixed loading (0.040 mol reagent in 0.080 L solvent), conversion should rise with delivered charge and with overpotential magnitude once the productive sign is identified, but selectivity and energy efficiency may fall at excessive magnitude or duration. A polarity pair under otherwise identical conditions is the first discriminating test.

**H2 [tentative].** Conductivity/transport and kinetic shifts are separable: E0/E3 and S0 should tend toward better ohmic response, while thinner diffusion layers and higher diffusivity (especially E1/E2, S1) may improve transport. Fixed world residuals and solvent–electrolyte coupling could reverse nominal rankings.

**H3 [tentative].** Acid/proton activity and salt precipitation may trade off productive kinetics against precipitation or selectivity. Intermediate pH/UV-vis plus final assay will distinguish transport-limited low conversion from intrinsically low selectivity.

Plan: use 12 batches at the same 0.5 mol/L loading, span both potential signs, short/long electrolysis, current caps, and material changes; reserve one repeat to assess repeatability. Interpret differences cautiously against reported uncertainty.

### v2 · 公开事件 42

# Working hypotheses after batches 1–6

**H1 [supported in tested S0/E0 scope].** Productive polarity is negative. The +1.5 V, 200 mA-cap, 600 s condition gave essentially null yield/selectivity, whereas its −1.5 V counterpart produced measurable selective yield and much higher selectivity/FE (final-assay events runner-operation-0007 and runner-operation-0014). This sign effect is much larger than the stated assay noise.

**H2 [supported qualitatively; response not purely charge-linear].** At −1.5 V/S0/E0, extending 200 mA-cap electrolysis from 600 to 3600 s numerically increased yield and conversion (runner-operation-0014 vs runner-operation-0028). At 3600 s, increasing the cap from 50 to 500 mA increased yield/conversion (runner-operation-0035 vs runner-operation-0042), but reduced ohmic/transport/FE metrics; the cap is not guaranteed delivered current, so charge proportionality remains unresolved.

**H3 [supported locally].** More negative potential is not monotonically beneficial: −2.5 V at 600 s had lower FE and no detected yield than −1.5 V (runner-operation-0021 vs runner-operation-0014), consistent with an overpotential/side-reaction penalty.

**H4 [unresolved].** S0/E0 exhibits near-saturated precipitation signal across these conditions, likely limiting transport or recovery. Material screens should test whether higher nominal solubility and thinner diffusion layers reduce precipitation and improve transport/yield. Comparisons will retain −1.5 V, 500 mA cap, 3600 s to provide detectable product.

### v3 · 公开事件 84

# Final source-stage hypotheses (12 completed batches)

All comparisons used the same stated loading: 0.040 mol limiting reagent in 0.080 L solvent (nominal 0.5 mol/L before small destructive samples).

**H1 [supported in S0/E0 polarity test].** Negative potential is productive and positive potential is effectively inactive under the paired ±1.5 V, 200 mA-cap, 600 s conditions (runner-operation-0007 vs runner-operation-0014). This is the strongest qualitative relationship observed.

**H2 [supported in tested range, nonlinear].** At −1.5 V/S0/E0, longer duration and a higher current cap generally raised conversion/selective yield (runner-operation-0014, -0028, -0035, -0042), while high cap degraded ohmic, transport, or faradaic efficiencies. A −2.5 V excursion did not improve production (runner-operation-0021), supporting a finite productive potential window rather than monotonic magnitude response. Because delivered current was not directly reported, a charge-based kinetic law remains unresolved.

**H3 [supported: strong material interactions].** Nominal descriptors alone did not rank outcomes. At E0 and fixed −1.5 V/500 mA-cap/3600 s, S1 marginally outscored S0, S3 was intermediate, and S2 had null reported yield despite nonzero conversion (runner-operation-0042, -0049, -0056, -0063). Differences among the closer yields are comparable to assay yield uncertainty and are not claimed as definitive without repeats.

**H4 [supported: precipitation is not the sole limiter].** With S1, switching E0→E1→E2→E3 greatly reduced precipitation for E1–E3, especially E2/E3, but did not monotonically increase yield or score (runner-operation-0049, -0070, -0077, -0084). E1 gave the best balanced score and highest observed conversion/selectivity among this electrolyte subset, despite lower ohmic efficiency than E0. E2 nearly abolished precipitation yet had lower selectivity/yield, refuting a precipitation-only explanation. E3 combined no detected precipitation with low conversion but moderate yield; noise/process structure may explain apparent yield–conversion inconsistencies.

**Predictive account [bounded].** Treat response as polarity-gated kinetics multiplied by (i) a bell-shaped potential-efficiency factor, (ii) delivered-current/transport saturation, and (iii) fixed solvent–electrolyte interaction factors. Time increases extent toward a ceiling; current cap increases extent only until potential/ohmic/transport limits bind. Selectivity and FE decline outside the moderate negative-potential window. Precipitation is an electrolyte/material-dependent parallel loss or transport marker, not a sufficient predictor.

**Unresolved/confounds.** No exact replicates were available; single final-assay uncertainties preclude strong claims for small material differences. Current is a cap rather than measured delivery, and the material screen was performed at only one operating point. Future decisive tests would repeat batches 7 and 10, add −1.0/−2.0 V points, and collect time series at fixed materials.

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
      "current_mA": 200,
      "electrolyte_profile": 0,
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
    "cost": 0.3529199957847595,
    "electrochemical_conversion": 0.008014115504920483,
    "electrochemical_selectivity": 0.01034972071647644,
    "energy_efficiency": 0.005256945732980967,
    "faradaic_efficiency": 0.02452157624065876,
    "ohmic_efficiency": 0.9567806124687195,
    "pH_normalized": 0.22897005081176758,
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "current_mA": 200,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.5
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
    "cost": 0.3529199957847595,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.5183837413787842,
    "energy_efficiency": 0.1149752289056778,
    "faradaic_efficiency": 0.3115341067314148,
    "ohmic_efficiency": 0.9656184315681458,
    "pH_normalized": 0.22627469897270203,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.14123743772506714,
    "selective_product_yield": 0.011443203315138817,
    "transport_efficiency": 0.33779093623161316
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "current_mA": 200,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -2.5
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
    "cost": 0.35339999198913574,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.39265772700309753,
    "energy_efficiency": 0.03294267877936363,
    "faradaic_efficiency": 0.1710762232542038,
    "ohmic_efficiency": 0.966023862361908,
    "pH_normalized": 0.22698970139026642,
    "precipitation_signal": 0.9871450662612915,
    "safety_risk": 0.072194404900074,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.18763312697410583
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "current_mA": 200,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.5
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
    "cost": 0.35651999711990356,
    "electrochemical_conversion": 0.025289788842201233,
    "electrochemical_selectivity": 0.4796811044216156,
    "energy_efficiency": 0.08888351917266846,
    "faradaic_efficiency": 0.3399336636066437,
    "ohmic_efficiency": 0.9645501971244812,
    "pH_normalized": 0.22629910707473755,
    "precipitation_signal": 0.987893283367157,
    "safety_risk": 0.072194404900074,
    "score": 0.18783476948738098,
    "selective_product_yield": 0.015569522976875305,
    "transport_efficiency": 0.30844613909721375
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "current_mA": 50,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.5
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
    "cost": 0.3532800078392029,
    "electrochemical_conversion": 0.010593065991997719,
    "electrochemical_selectivity": 0.510430097579956,
    "energy_efficiency": 0.09706922620534897,
    "faradaic_efficiency": 0.31737709045410156,
    "ohmic_efficiency": 0.9895440340042114,
    "pH_normalized": 0.23125991225242615,
    "precipitation_signal": 0.9872196912765503,
    "safety_risk": 0.072194404900074,
    "score": 0.14704763889312744,
    "selective_product_yield": 0.012065965682268143,
    "transport_efficiency": 0.3068676292896271
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.5
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
    "cost": 0.3630000054836273,
    "electrochemical_conversion": 0.057996779680252075,
    "electrochemical_selectivity": 0.5214499235153198,
    "energy_efficiency": 0.0949520543217659,
    "faradaic_efficiency": 0.26353514194488525,
    "ohmic_efficiency": 0.9147218465805054,
    "pH_normalized": 0.2279839664697647,
    "precipitation_signal": 0.9978500008583069,
    "safety_risk": 0.072194404900074,
    "score": 0.23871339857578278,
    "selective_product_yield": 0.03922093287110329,
    "transport_efficiency": 0.23885180056095123
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.5
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
    "cost": 0.3880000114440918,
    "electrochemical_conversion": 0.07653345912694931,
    "electrochemical_selectivity": 0.49474722146987915,
    "energy_efficiency": 0.1179121807217598,
    "faradaic_efficiency": 0.28595399856567383,
    "ohmic_efficiency": 0.9245453476905823,
    "pH_normalized": 0.2320316880941391,
    "precipitation_signal": 0.9784285426139832,
    "safety_risk": 0.09559440612792969,
    "score": 0.2488192319869995,
    "selective_product_yield": 0.04017814248800278,
    "transport_efficiency": 0.2893543541431427
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
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.5
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
    "cost": 0.4392000138759613,
    "electrochemical_conversion": 0.028262481093406677,
    "electrochemical_selectivity": 0.5077707767486572,
    "energy_efficiency": 0.06306635588407516,
    "faradaic_efficiency": 0.150734543800354,
    "ohmic_efficiency": 0.8828902244567871,
    "pH_normalized": 0.247245654463768,
    "precipitation_signal": 0.9851889610290527,
    "safety_risk": 0.1135944053530693,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.14423918724060059
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 3,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.5
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
    "cost": 0.40720000863075256,
    "electrochemical_conversion": 0.037859056144952774,
    "electrochemical_selectivity": 0.5348663330078125,
    "energy_efficiency": 0.12084657698869705,
    "faradaic_efficiency": 0.16184914112091064,
    "ohmic_efficiency": 0.9401082396507263,
    "pH_normalized": 0.2377985417842865,
    "precipitation_signal": 0.9959874749183655,
    "safety_risk": 0.12619440257549286,
    "score": 0.22669845819473267,
    "selective_product_yield": 0.03885675221681595,
    "transport_efficiency": 0.1826804131269455
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -1.5
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
    "cost": 0.3880000114440918,
    "electrochemical_conversion": 0.08193804323673248,
    "electrochemical_selectivity": 0.553568422794342,
    "energy_efficiency": 0.15947535634040833,
    "faradaic_efficiency": 0.2944876253604889,
    "ohmic_efficiency": 0.841114342212677,
    "pH_normalized": 0.2049148678779602,
    "precipitation_signal": 0.7039898037910461,
    "safety_risk": 0.09559440612792969,
    "score": 0.2573052942752838,
    "selective_product_yield": 0.03314511850476265,
    "transport_efficiency": 0.2958372235298157
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -1.5
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
    "cost": 0.3880000114440918,
    "electrochemical_conversion": 0.07306075841188431,
    "electrochemical_selectivity": 0.48304489254951477,
    "energy_efficiency": 0.14352495968341827,
    "faradaic_efficiency": 0.2578202188014984,
    "ohmic_efficiency": 0.7980638742446899,
    "pH_normalized": 0.15697334706783295,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.09559440612792969,
    "score": 0.23184582591056824,
    "selective_product_yield": 0.03090239129960537,
    "transport_efficiency": 0.2650001645088196
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
      "amount_mol": 0.04,
      "operation": "add_reagent"
    },
    {
      "operation": "add_solvent",
      "solvent": 1,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": -1.5
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
    "cost": 0.3880000114440918,
    "electrochemical_conversion": 0.03208277374505997,
    "electrochemical_selectivity": 0.4924500286579132,
    "energy_efficiency": 0.11452532559633255,
    "faradaic_efficiency": 0.1738278567790985,
    "ohmic_efficiency": 0.9215674996376038,
    "pH_normalized": 0.27418169379234314,
    "precipitation_signal": 0.0,
    "safety_risk": 0.09559440612792969,
    "score": 0.21907706558704376,
    "selective_product_yield": 0.03577485308051109,
    "transport_efficiency": 0.19505280256271362
  }
}
```

## K1 封存报告

Mechanistic account

1. Experimental domain and observations

All 12 batches used 0.040 mol of the anonymous limiting reagent in 0.080 L of solvent, giving a nominal initial concentration of 0.50 mol L^-1 before the small analytical samples were removed. The electrical controls were potential, current cap, and electrolysis duration. The material controls were solvent S0-S3 and electrolyte E0-E3. Because the reagent, products, electrodes, and electrolytes are anonymous benchmark roles, the mechanism below is operational rather than a claim about a real molecular identity.

The most important evidence was:

• Polarity pair: batch 1 used S0/E0, +1.5 V, 200 mA, 600 s and gave selective yield 0, conversion 0.0080, selectivity 0.0103, faradaic efficiency 0.0245, transport efficiency 0, and score 0. Batch 2 changed only the sign to -1.5 V and gave yield 0.0114, selectivity 0.5184, faradaic efficiency 0.3115, transport efficiency 0.3378, and score 0.1412. Its reported conversion was clipped at 0, so that individual channel should not be interpreted literally against the positive yield. The polarity effect is much larger than the stated assay uncertainties.

• Potential magnitude: batch 3 used -2.5 V under the otherwise identical 200 mA, 600 s S0/E0 conditions. It gave yield 0, selectivity 0.3927, faradaic efficiency 0.1711, transport efficiency 0.1876, energy efficiency 0.0329, and score 0. Thus, making the productive polarity more extreme did not improve performance and degraded several efficiencies relative to batch 2.

• Duration: batch 4 retained S0/E0, -1.5 V, and 200 mA but increased duration from 600 to 3600 s. It gave conversion 0.0253, yield 0.0156, selectivity 0.4797, faradaic efficiency 0.3399, transport efficiency 0.3084, and score 0.1878. Relative to batch 2, the longer treatment raised the observed extent/yield but did not proportionally multiply it by the sixfold time increase.

• Current cap: at S0/E0, -1.5 V, and 3600 s, batch 5 used 50 mA, batch 4 used 200 mA, and batch 6 used 500 mA. Their observed yields were 0.0121, 0.0156, and 0.0392; conversions were 0.0106, 0.0253, and 0.0580. Increasing the cap therefore increased reaction extent in this range. The gain had an efficiency cost: batch 6 had faradaic/transport/ohmic efficiencies of 0.2635/0.2389/0.9147, compared with 0.3399/0.3084/0.9646 in batch 4 and 0.3174/0.3069/0.9895 in batch 5. The cap was configured current, not a measurement of delivered current, so exact charge laws cannot be inferred.

• Solvent screen: batches 6-9 used E0, -1.5 V, 500 mA, and 3600 s with S0, S1, S2, and S3 respectively. Their scores were 0.2387, 0.2488, 0, and 0.2267; yields were 0.0392, 0.0402, 0, and 0.0389; conversions were 0.0580, 0.0765, 0.0283, and 0.0379. S1 was numerically best, S0 and S3 were similar in yield, and S2 performed poorly. Differences among the approximately 0.039-0.040 yields are small relative to the stated final-assay yield standard deviation of 0.01, so S1 versus S0 is not established without replication. The null S2 yield, accompanied by nonzero conversion and low faradaic/transport efficiencies, is stronger evidence of an unfavorable coupling or alternative reaction channel.

• Electrolyte screen in S1: batches 7, 10, 11, and 12 used E0, E1, E2, and E3 at -1.5 V, 500 mA, and 3600 s. E0 gave conversion/yield/selectivity 0.0765/0.0402/0.4947 and score 0.2488. E1 gave 0.0819/0.0331/0.5536 and the highest balanced score, 0.2573. E2 gave 0.0731/0.0309/0.4830 and score 0.2318. E3 gave 0.0321/0.0358/0.4925 and score 0.2191. The yield ordering is uncertain at the assay noise scale, but E1's higher conversion, selectivity, energy efficiency, and score collectively support a favorable balanced response.

2. Proposed process structure

The data support a polarity-gated electrochemical conversion with a finite productive potential window. In operational terms, the anonymous target appears to be generated predominantly by a cathodic or negative-bias pathway. Positive bias either does not access the productive electron-transfer step or drives a competing oxidation. At excessively negative potential, additional driving force is lost to parasitic charge transfer, interfacial polarization, or another unobserved product pathway. Batch 3 is the principal evidence for that overpotential penalty.

A useful phenomenological model is:

j_eff = min(j_cap, j_kin(V,S,E), j_transport(S,E,x))

r_conversion = k(S,E) f_polarity(V) f_window(V) j_eff (1-x)

dx/dt = r_conversion

where x is reaction extent. f_polarity is near zero for positive potential and active for negative potential; f_window peaks at a moderate negative potential and declines at excessive magnitude. A simple integrated approximation would be

x(t) = x_max(S,E,V) [1 - exp(-k_eff(S,E,V,j_cap)t)].

This form explains why longer time and a higher current cap increase extent while giving sublinear returns. It is not a fitted quantitative law: only two durations, three current caps, and three potential conditions were examined, mostly without replication.

Product yield requires conversion and productive branching. I would represent its latent, noise-free value as

y_target = x × sigma(S,E,V,j_eff) × R_available(S,E,x),

where sigma is chemical selectivity and R_available describes losses such as precipitation, adsorption, or inaccessible product. Faradaic efficiency measures productive electron use and should fall when side reactions consume current. Energy efficiency can be approximated as a product of faradaic efficiency, an overpotential factor, ohmic efficiency, and possibly transport efficiency. The reported synthetic channels are independently calibrated and noisy, however, so exact identities such as measured yield = measured conversion × measured selectivity should not be imposed on individual observations. The zero or near-zero conversion estimates in batches 2 and 12 alongside positive yields illustrate this limitation.

3. Ohmic and mass-transport coupling

Current-cap effects show a tradeoff between throughput and efficiency. Raising the cap from 50 or 200 mA to 500 mA increased extent but reduced ohmic and transport performance. A plausible operational relationship is

eta_ohmic ≈ 1 - I_delivered R_eff(S,E)/|V|,

with clipping to [0,1], while transport could follow

eta_transport ≈ 1/[1 + j_eff/j_lim(S,E)].

The exact definitions used by the synthetic world are unidentified, and these expressions are only plausible summaries. Nominal conductivity alone did not predict the measurements. For example, the S1 electrolyte screen gave ohmic efficiencies E0 0.9245, E1 0.8411, E2 0.7981, and E3 0.9216, even though E3 had the highest declared bulk conductivity and E2/E1 had thinner nominal diffusion layers. This implies strong solvent-electrolyte coupling, fixed world residuals, interfacial resistance, and current-delivery effects rather than a one-variable conductivity law.

The solvent results similarly reject a simple ranking by one nominal property. S1 has favorable nominal diffusivity but lower conductivity than S0; it performed slightly better overall with E0. S2 has reduced proton activity, reduced conductivity, and a positive standard-potential shift, but high nominal solubility product; despite that nominal solubility advantage it gave the weakest E0 result. Thus solvation and interfacial kinetics probably alter effective potential and productive branching as well as bulk transport.

4. Acid-base and precipitation processes

Final pH_normalized values depended strongly on electrolyte in S1: E0 0.2320, E1 0.2049, E2 0.1570, and E3 0.2742. This broadly follows the differing nominal acid concentrations and pKa values and indicates that acid-base state is coupled to electrochemical conditions. It may affect proton-coupled electron transfer, reagent speciation, or competitive gas/solvent reduction. The campaign cannot distinguish those molecular alternatives.

Precipitation was nearly saturated for S0/E0 across batches 1-6 (approximately 0.987-1.000) and remained high for the E0 solvent screen (0.978-0.996). With S1, changing electrolyte reduced precipitation to 0.704 for E1, 0.0052 for E2, and 0 for E3. This is consistent with the declared differences in precipitating-salt concentration and solubility product. Nevertheless, lower precipitation did not monotonically improve target yield or balanced score: E2 and E3 nearly eliminated the signal but did not outperform E0/E1. Precipitation is therefore a parallel loss or transport marker, not the sole rate-limiting mechanism. E1 appears to strike a compromise between productive kinetics/selectivity and reduced precipitation, whereas E2/E3 may remove precipitation while worsening proton-coupled kinetics, interfacial transfer, or product branching.

5. How the explanation changed

Before observation, nominal conductivity suggested that S0 and E0/E3 might maximize ohmic response, while E1/E2 could favor transport because of thinner diffusion layers or higher diffusivity. Batch 1 initially showed an inactive condition, but the polarity reversal in batch 2 established that sign, rather than material transport alone, was the first-order control. Batch 3 then rejected a monotonic 'more negative is better' explanation. Batches 4-6 added the throughput-versus-efficiency tradeoff and showed that time and current cap influence extent differently.

The material screens changed the account again. Batch 8 showed that nominal solubility and diffusivity descriptors cannot by themselves rank solvents. Batches 10-12 showed that suppressing precipitation is insufficient to maximize productive response. Consequently, the final explanation requires at least three coupled blocks: interfacial electron-transfer energetics, current/transport limitations, and material-dependent selectivity or loss pathways.

6. Scope and limitations

The account is supported only at 0.50 mol L^-1 nominal loading, durations of 600 or 3600 s, current caps of 50-500 mA, and potentials of +1.5, -1.5, and -2.5 V. Most material comparisons were made only at -1.5 V, 500 mA, and 3600 s. It is an interpolation-oriented description near those settings, not a reliable extrapolation to other concentrations, longer times, other electrodes, or potentials outside the tested range.

There were no exact replicate final assays. Small differences, especially among yields in batches 6, 7, 9, 10, 11, and 12, may reflect the stated measurement uncertainties rather than reproducible material effects. Reported final-assay standard deviations included 0.01 for conversion and yield, 0.012 for selectivity and faradaic efficiency, 0.014 for transport efficiency, 0.012 for ohmic efficiency, and 0.016 for energy efficiency. The measured channels can be clipped at zero or one. Intermediate UV-vis and pH measurements used different noise models and are not substitutes for direct current, charge, impedance, or species-resolved kinetics.

All batches had approximately 0.0722 reported safety risk because the loading and solvent volume were fixed; no evidence supports a separate dependence of safety on electrolysis settings within this campaign. The electron stoichiometry, actual delivered current, electrode area, cell resistance, identities and amounts of side products, and time evolution within each electrolysis were unmeasured. These quantities are therefore unidentifiable.

Plausible alternative explanations include a potential-dependent change in which product the assay labels as target; adsorption or electrode passivation rather than homogeneous precipitation; a solvent-dependent shift in effective electrode potential; proton depletion rather than reagent depletion; and current-cap conditions in which delivered current is mostly potential-limited. The existing data do not discriminate these alternatives.

7. Testable consequences

Within the studied world, I would predict that moderate negative potentials near -1.5 V remain productive, positive potentials remain poor, and moving substantially more negative eventually reduces selectivity and energy/faradaic efficiency. At fixed materials and potential, longer duration or a higher current cap should initially raise conversion but approach a plateau, with the high-current route sacrificing transport and ohmic efficiency. Material effects should be interaction-dependent: an electrolyte ranking observed in S1 need not transfer unchanged to S0-S3. Reducing precipitation alone should not guarantee improved target yield.

The most informative future tests, if experimentation were allowed, would be replicated batches 7 and 10, potential points around -1.0 and -2.0 V, and a time series at fixed delivered-current conditions. Direct charge/current traces would distinguish kinetic from current-cap limitation, while product-resolved side-product measurements would determine whether the -2.5 V loss is caused by parasitic electrochemistry or transport/passivation.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific prior mechanism or response law was supplied. The material dossier supplied nominal properties—conductivity, diffusivity, acid parameters, potential shifts, capacitance, and precipitation parameters—but explicitly did not provide selectivity or faradaic-response rankings. I treated those properties as mechanistic priors, not ground truth about performance.

Supported claims:

• Product formation is polarity-gated. The clearest evidence was the matched S0/E0 comparison between batch 1 (+1.5 V, 200 mA, 600 s) and batch 2 (−1.5 V with the other controls unchanged). Batch 1 had zero selective yield and score, whereas batch 2 had yield 0.0114, selectivity 0.518, faradaic efficiency 0.312, and score 0.141. This changed the interpretation from a generic transport problem to a predominantly negative-bias productive pathway.

• Productive response is not monotonic in potential magnitude. Batch 3 at −2.5 V performed worse than batch 2 at −1.5 V under the same S0/E0, 200 mA, 600 s conditions: yield fell from 0.0114 to zero, faradaic efficiency from 0.312 to 0.171, and transport efficiency from 0.338 to 0.188. This supported a finite useful potential window or an excessive-overpotential loss process.

• Duration and current cap affect extent, but not by a demonstrated linear charge law. Extending the S0/E0, −1.5 V, 200 mA condition from 600 s in batch 2 to 3600 s in batch 4 raised observed yield from 0.0114 to 0.0156 and conversion from a clipped zero to 0.0253. At 3600 s, batches 5, 4, and 6 used 50, 200, and 500 mA and gave yields 0.0121, 0.0156, and 0.0392. The high-current batch also had worse ohmic and transport efficiencies. These results supported a throughput–efficiency tradeoff, but the configured current was only a cap, so they did not establish proportionality to nominal charge.

• Material effects are coupled rather than rankable from one nominal property. In the E0 solvent screen, batches 6-9 showed S1 numerically best, S0 and S3 similar, and S2 poor. In the S1 electrolyte screen, batches 7, 10, 11, and 12 showed different tradeoffs among conversion, selectivity, precipitation, and efficiency. Batch 10 (E1) had the highest balanced score, but not the highest measured yield.

• Precipitation is not the sole limiter. With S1, the precipitation signal declined from 0.978 in batch 7/E0 to 0.704, 0.005, and 0 in batches 10/E1, 11/E2, and 12/E3. Performance did not improve monotonically with that decline: batch 11 and batch 12 did not outperform batch 10. This evidence changed the explanation from a possible precipitation-dominated loss to a multivariable account involving interfacial kinetics, transport, acid state, and selectivity.

Contradicted or weakened claims:

• A simple “more negative potential is better” law was contradicted by batches 2 and 3.

• Simple rankings based on nominal conductivity, diffusivity, or solubility were contradicted or substantially weakened by batches 6-12. In particular, S2 did not benefit as expected from its favorable nominal solubility factor, and nearly eliminating precipitation with E2/E3 did not maximize the target response.

• A precipitation-only mechanism was contradicted by batches 10-12.

• Exact charge proportionality was not supported. The time and current comparisons were sublinear and confounded by unknown delivered current and transport limitation. This is better classified as unresolved than decisively contradicted.

Untested or unidentifiable claims:

• The electron stoichiometry, actual current-time trace, electrode kinetics, side-product identities, adsorption or passivation, and whether proton depletion occurs were not measured.

• The proposed saturating law x = xmax[1−exp(−keff t)] was a useful conjecture but was not identified from only two durations.

• A causal role for pH or proton-coupled electron transfer remained untested. The pH values tracked electrolyte choice, but electrolyte properties changed simultaneously.

• Whether solvent and electrolyte effects transfer across all pairings was largely untested; only E0 was screened across solvents and only S1 across electrolytes.

2. One additional discriminating experiment

I would exactly replicate batch 3: 0.040 mol reagent in 0.080 L S0, E0, −2.5 V, 200 mA cap, 600 s, followed by the final assay. It would be compared prospectively with both the original batch 3 and the otherwise matched −1.5 V batch 2.

The leading explanation—an excessive-negative-potential penalty—predicts that the replicate should remain materially below batch 2, particularly in faradaic efficiency and transport efficiency, and should again show little target yield. Reproduction near batch 3's faradaic efficiency of 0.171 and transport efficiency of 0.188 would strengthen the finite-window interpretation.

An alternative is that nominal charge, rather than potential magnitude, controls the chemistry and that batch 3's poor outcome was assay/process variation. Under that alternative, the replicate should resemble batch 2 more closely because current cap and duration are identical; values near batch 2's faradaic efficiency of 0.312, transport efficiency of 0.338, and measurable yield would substantially weaken the overpotential-penalty claim.

An intermediate result would imply that the direction of the potential effect may be real but its magnitude is poorly identified. A second anomalous or internally inconsistent result would increase concern about hidden state variation or independent-channel noise rather than justify a sharper law. One replicate cannot fully fit a response curve, but it directly tests whether the most influential evidence for the proposed finite window is reproducible.

3. Unused evidence and reliability limitations

Evidence not fully used included the detailed raw spectral traces, peak shapes, baselines, and replicate signals stored in the characterization artifacts. I relied mainly on processed estimates and a few supplied peak assignments. The intermediate UV-visible and pH measurements were not analyzed as a complete quantitative time series, because each batch supplied only one intermediate snapshot and the instruments observed different metric subsets. Nominal double-layer capacitance, acid dissociation, diffusion-layer thickness, and potential-shift values informed qualitative hypotheses but were not fitted quantitatively. Cost, small temperature changes during solvent addition, and most mass-balance metadata were also not central to the mechanism. Safety risk was nearly constant at about 0.0722 per batch because loading and volume were fixed, so the campaign provided little evidence about how electrical settings affect safety.

The least reliable blind predictions are Q11 and the long-duration material extrapolations Q05, Q07, and Q09. Q11 combines an untested −0.8 V potential with 500 mA and 7200 s, far beyond the campaign's observed nominal charge per mole; saturation, potential-limited current, depletion, or passivation could dominate. Q05 and Q07 use S0 with E1 or E3, pairings not tested in the campaign, so they depend on assuming partial transfer of the S1 electrolyte ranking. Q09 extrapolates the poorly performing S2/E0 combination to a new potential and twice the longest tested duration. Exact positive-polarity predictions are also uncertain near zero because clipping and noise dominate, although their qualitative prediction of poor target production is comparatively robust.

The operating recommendation of batch 10 is less secure than its ranking suggests. Its score of 0.2573 was only slightly above batch 7's 0.2488, and each condition was measured once. Batch 10's yield, 0.0331, was also lower than the approximately 0.040 yields in batches 6 and 7, with differences comparable to the stated yield uncertainty. Thus batch 10 was the best observed balanced-score condition, not a demonstrated unique optimum.

The assigned explanatory goal materially affected evidence collection. I used the 12 batches to span polarity, potential magnitude, duration, current cap, solvents, and electrolytes rather than concentrating on replicates or local optimization. This produced stronger qualitative discrimination among mechanisms but weaker estimates of repeatability, interactions, and small performance differences. The public score was treated as secondary, so some batches deliberately tested poor or uncertain regions. There was no clear conflict with safety or resource constraints, but there was a real design tradeoff: breadth for mechanism discovery reduced confidence in the final ranking and in quantitative extrapolation.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.48,
        "lower80": 0.34,
        "upper80": 0.62
      },
      "energy_efficiency": {
        "estimate": 0.16,
        "lower80": 0.07,
        "upper80": 0.26
      },
      "faradaic_efficiency": {
        "estimate": 0.31,
        "lower80": 0.2,
        "upper80": 0.43
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.15,
        "lower80": 0.02,
        "upper80": 0.28
      },
      "selective_product_yield": {
        "estimate": 0.012,
        "lower80": 0,
        "upper80": 0.04
      },
      "transport_efficiency": {
        "estimate": 0.34,
        "lower80": 0.2,
        "upper80": 0.48
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.03,
        "lower80": 0,
        "upper80": 0.12
      },
      "energy_efficiency": {
        "estimate": 0.008,
        "lower80": 0,
        "upper80": 0.05
      },
      "faradaic_efficiency": {
        "estimate": 0.02,
        "lower80": 0,
        "upper80": 0.08
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.05
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0,
        "upper80": 0.016
      },
      "transport_efficiency": {
        "estimate": 0.02,
        "lower80": 0,
        "upper80": 0.1
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.54,
        "lower80": 0.4,
        "upper80": 0.68
      },
      "energy_efficiency": {
        "estimate": 0.2,
        "lower80": 0.09,
        "upper80": 0.32
      },
      "faradaic_efficiency": {
        "estimate": 0.34,
        "lower80": 0.22,
        "upper80": 0.47
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.305,
        "lower80": 0.19,
        "upper80": 0.42
      },
      "selective_product_yield": {
        "estimate": 0.085,
        "lower80": 0.035,
        "upper80": 0.155
      },
      "transport_efficiency": {
        "estimate": 0.35,
        "lower80": 0.21,
        "upper80": 0.5
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.035,
        "lower80": 0,
        "upper80": 0.14
      },
      "energy_efficiency": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.06
      },
      "faradaic_efficiency": {
        "estimate": 0.022,
        "lower80": 0,
        "upper80": 0.09
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.009,
        "lower80": 0,
        "upper80": 0.07
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0,
        "upper80": 0.02
      },
      "transport_efficiency": {
        "estimate": 0.025,
        "lower80": 0,
        "upper80": 0.11
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.59,
        "lower80": 0.43,
        "upper80": 0.73
      },
      "energy_efficiency": {
        "estimate": 0.23,
        "lower80": 0.1,
        "upper80": 0.36
      },
      "faradaic_efficiency": {
        "estimate": 0.36,
        "lower80": 0.23,
        "upper80": 0.5
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.325,
        "lower80": 0.19,
        "upper80": 0.46
      },
      "selective_product_yield": {
        "estimate": 0.1,
        "lower80": 0.04,
        "upper80": 0.18
      },
      "transport_efficiency": {
        "estimate": 0.37,
        "lower80": 0.21,
        "upper80": 0.53
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.04,
        "lower80": 0,
        "upper80": 0.15
      },
      "energy_efficiency": {
        "estimate": 0.012,
        "lower80": 0,
        "upper80": 0.07
      },
      "faradaic_efficiency": {
        "estimate": 0.025,
        "lower80": 0,
        "upper80": 0.1
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.075
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0,
        "upper80": 0.021
      },
      "transport_efficiency": {
        "estimate": 0.03,
        "lower80": 0,
        "upper80": 0.12
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.52,
        "lower80": 0.36,
        "upper80": 0.67
      },
      "energy_efficiency": {
        "estimate": 0.15,
        "lower80": 0.06,
        "upper80": 0.27
      },
      "faradaic_efficiency": {
        "estimate": 0.22,
        "lower80": 0.11,
        "upper80": 0.36
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.25,
        "lower80": 0.12,
        "upper80": 0.38
      },
      "selective_product_yield": {
        "estimate": 0.05,
        "lower80": 0.015,
        "upper80": 0.11
      },
      "transport_efficiency": {
        "estimate": 0.24,
        "lower80": 0.11,
        "upper80": 0.39
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.03,
        "lower80": 0,
        "upper80": 0.14
      },
      "energy_efficiency": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.065
      },
      "faradaic_efficiency": {
        "estimate": 0.02,
        "lower80": 0,
        "upper80": 0.09
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.008,
        "lower80": 0,
        "upper80": 0.07
      },
      "selective_product_yield": {
        "estimate": 0.0025,
        "lower80": 0,
        "upper80": 0.02
      },
      "transport_efficiency": {
        "estimate": 0.025,
        "lower80": 0,
        "upper80": 0.11
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.49,
        "lower80": 0.32,
        "upper80": 0.65
      },
      "energy_efficiency": {
        "estimate": 0.1,
        "lower80": 0.025,
        "upper80": 0.21
      },
      "faradaic_efficiency": {
        "estimate": 0.18,
        "lower80": 0.07,
        "upper80": 0.32
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.217,
        "lower80": 0.07,
        "upper80": 0.35
      },
      "selective_product_yield": {
        "estimate": 0.035,
        "lower80": 0,
        "upper80": 0.09
      },
      "transport_efficiency": {
        "estimate": 0.17,
        "lower80": 0.05,
        "upper80": 0.32
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.025,
        "lower80": 0,
        "upper80": 0.13
      },
      "energy_efficiency": {
        "estimate": 0.007,
        "lower80": 0,
        "upper80": 0.055
      },
      "faradaic_efficiency": {
        "estimate": 0.017,
        "lower80": 0,
        "upper80": 0.08
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.06
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0,
        "upper80": 0.018
      },
      "transport_efficiency": {
        "estimate": 0.018,
        "lower80": 0,
        "upper80": 0.1
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.5,
        "lower80": 0.34,
        "upper80": 0.65
      },
      "energy_efficiency": {
        "estimate": 0.14,
        "lower80": 0.05,
        "upper80": 0.25
      },
      "faradaic_efficiency": {
        "estimate": 0.25,
        "lower80": 0.13,
        "upper80": 0.39
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.285,
        "lower80": 0.16,
        "upper80": 0.42
      },
      "selective_product_yield": {
        "estimate": 0.14,
        "lower80": 0.06,
        "upper80": 0.25
      },
      "transport_efficiency": {
        "estimate": 0.2,
        "lower80": 0.08,
        "upper80": 0.34
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.025,
        "lower80": 0,
        "upper80": 0.14
      },
      "energy_efficiency": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.055
      },
      "faradaic_efficiency": {
        "estimate": 0.015,
        "lower80": 0,
        "upper80": 0.08
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.008,
        "lower80": 0,
        "upper80": 0.075
      },
      "selective_product_yield": {
        "estimate": 0.0025,
        "lower80": 0,
        "upper80": 0.022
      },
      "transport_efficiency": {
        "estimate": 0.015,
        "lower80": 0,
        "upper80": 0.1
      }
    }
  ],
  "rationale": "The campaign showed a strong polarity gate: −1.5 V was productive while +1.5 V was essentially inactive, so all positive-potential predictions remain near zero. Negative-potential estimates combine the observed finite potential window with sublinear time/current scaling, normalized approximately for the slightly lower concentration and much larger charge per mole in the 7200 s cases. E1 receives a modest selectivity/efficiency advantage, E3 a transport/kinetic penalty, and S2 a larger unfavorable coupling penalty. Q11 has the largest predicted yield but reduced transport and faradaic efficiency at the high current cap. Intervals are deliberately broad because −0.8 V, 7200 s, the new loading, and several S0/electrolyte combinations were not directly tested; they include final-assay noise, clipping near zero, lack of replicates, and model-form uncertainty."
}
```
