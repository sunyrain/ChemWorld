# repeat-03/EC-W02-B12-optimization-E-MisIndexed

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-03\EC-W02-B12-optimization-E-MisIndexed\participant\optimization-E-MisIndexed

## 同期笔记

### v1 · 公开事件 0

# Electrochemical campaign hypotheses

## H1 [tentative]
At fixed loading, balanced score should be maximized at moderate overpotential and duration: too little charge limits conversion, while excessive magnitude/time should reduce selectivity and energy efficiency. Current caps may bind through transport and resistance.

## H2 [tentative]
Nominally conductive media (especially E2/E3 and S0) should improve ohmic efficiency, but thick diffusion layers or precipitation can oppose total score. E0 may have favorable transport despite lower conductivity; material ranking is unresolved because latent residuals and selectivity are unknown.

## Planned test
Use equal reagent/volume across batches, first screen electrolyte/solvent and potential sign/magnitude, then use later batches to refine and replicate the strongest region. UV-vis before termination will be used selectively to diagnose efficiency, while final assay is authoritative. A result showing highest score at a boundary will shift refinement toward that boundary rather than preserving the moderate-condition prior.

### v2 · 公开事件 77

# Electrochemical campaign hypotheses

## H1 [supported in tested positive-potential scope]
At 0.020 mol reagent in 0.040 L solvent, long electrolysis (14,400 s) at a 100 mA cap strongly outperformed the short 3,600 s run because conversion and selective yield increased without loss of the high efficiency suite (final assays at runner-operation-0007 and runner-operation-0028). Raising the cap to 150 or 500 mA produced only modest conversion gains while substantially lowering faradaic/transport efficiency (runner-operation-0021, runner-operation-0063), supporting a transport/current-density penalty.

## H2 [supported for tested materials, with confounding]
S0/E0 is the strongest tested pair by balanced score. S1/E1, S2/E2, and S0/E3 were lower (runner-operation-0042, -0049, -0056). These comparisons used potential adjustments based on nominal shifts, so residual material effects are not cleanly separated from potential mismatch. E2/S2 and E3/S0 greatly suppressed precipitation relative to E0/S0, but precipitation is not in the stated score and their efficiency/yield deficits dominated.

## H3 [tentative]
For S0/E0 at 100 mA and 14,400 s, the local applied-potential optimum lies near +1.1 V: +0.8 V was below +1.0 V, and +1.1 V gave the campaign-best score so far (runner-operation-0070, -0028, -0077). The final batch will test +1.2 V under otherwise identical conditions. A lower score would bracket a local optimum near +1.1 V; a higher score would leave the optimum above the tested range.

## Polarity
The -1.0 V comparison was decisively inferior to +1.0 V at the short-duration baseline (runner-operation-0014 versus -0007), so the productive direction in this world is positive. This does not establish symmetry or behavior at all negative magnitudes.

### v3 · 公开事件 84

# Electrochemical campaign hypotheses

## H1 [supported in tested positive-potential scope]
At 0.020 mol reagent in 0.040 L solvent, long electrolysis (14,400 s) at a 100 mA cap improved balanced performance relative to 3,600 s, while 150–500 mA caps sharply penalized faradaic and transport efficiency (runner-operation-0007, -0028, -0021, -0063). The data support a current/transport penalty rather than a simple charge-only law.

## H2 [supported for tested material procedures, causality unresolved]
S0/E0 gave the highest balanced scores among tested pairs. S1/E1, S2/E2, and S0/E3 were lower (runner-operation-0042, -0049, -0056). Potential was adjusted using nominal shifts, so pair identity and potential mismatch remain partly confounded. E2/S2 and E3/S0 suppressed precipitation, but that benefit did not compensate their lower yield/efficiency under the tested procedures.

## H3 [supported locally; sharp boundary]
For S0/E0, 0.020 mol/0.040 L, 100 mA, and 14,400 s, +1.1 V was best (runner-operation-0077; score about 0.686). +0.8 and +1.0 V were lower (runner-operation-0070, -0028). Contrary to a smooth extrapolation, +1.2 V collapsed conversion, selectivity, and most efficiencies (runner-operation-0084). Thus the viable high-score window has a sharp upper boundary between +1.1 and +1.2 V, plausibly a regime switch or severe degradation; the exact threshold is unresolved. Operationally prefer +1.1 V, and avoid extrapolation upward.

## H4 [supported for tested baseline]
At 3,600 s, -1.0 V was decisively inferior to +1.0 V (runner-operation-0014 versus -0007), identifying positive polarity as productive in this world. Behavior at other negative magnitudes and long duration remains underdetermined.

## Recommendation decision
Select batch 11: S0/E0, 0.020 mol reagent, 0.040 L solvent, +1.1 V, 100 mA cap, 14,400 s. It achieved the highest observed public score and sits below the demonstrated +1.2 V failure boundary. A future replicate or a dense scan around +1.05–1.15 V could change confidence, but no tested batch exceeds it.

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
    "cost": 0.28404000401496887,
    "electrochemical_conversion": 0.09654239565134048,
    "electrochemical_selectivity": 0.8974339962005615,
    "energy_efficiency": 0.869667649269104,
    "faradaic_efficiency": 0.9735972285270691,
    "ohmic_efficiency": 0.9653005003929138,
    "pH_normalized": 0.22897005081176758,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.5825900435447693,
    "selective_product_yield": 0.06441827863454819,
    "transport_efficiency": 0.944893479347229
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
    "cost": 0.28404000401496887,
    "electrochemical_conversion": 0.027948666363954544,
    "electrochemical_selectivity": 0.575653076171875,
    "energy_efficiency": 0.2517053484916687,
    "faradaic_efficiency": 0.3857153058052063,
    "ohmic_efficiency": 0.9741383194923401,
    "pH_normalized": 0.22627469897270203,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.3011143207550049,
    "selective_product_yield": 0.029338575899600983,
    "transport_efficiency": 0.41197213530540466
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
      "potential_V": 1
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
    "cost": 0.296999990940094,
    "electrochemical_conversion": 0.19980350136756897,
    "electrochemical_selectivity": 0.8815194964408875,
    "energy_efficiency": 0.23292215168476105,
    "faradaic_efficiency": 0.19249247014522552,
    "ohmic_efficiency": 0.8586733341217041,
    "pH_normalized": 0.22698970139026642,
    "precipitation_signal": 0.9871450662612915,
    "safety_risk": 0.072194404900074,
    "score": 0.3517196476459503,
    "selective_product_yield": 0.17291711270809174,
    "transport_efficiency": 0.20904937386512756
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
    "cost": 0.28835999965667725,
    "electrochemical_conversion": 0.34981781244277954,
    "electrochemical_selectivity": 0.8584048748016357,
    "energy_efficiency": 0.8250539302825928,
    "faradaic_efficiency": 0.9759536981582642,
    "ohmic_efficiency": 0.9730700850486755,
    "pH_normalized": 0.22629910707473755,
    "precipitation_signal": 0.987893283367157,
    "safety_risk": 0.072194404900074,
    "score": 0.6712464690208435,
    "selective_product_yield": 0.3144640028476715,
    "transport_efficiency": 0.9444661736488342
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
      "amount_mol": 0.005,
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
    "cost": 0.2433599978685379,
    "electrochemical_conversion": 0.37199148535728455,
    "electrochemical_selectivity": 0.8970819115638733,
    "energy_efficiency": 0.2351941168308258,
    "faradaic_efficiency": 0.25796130299568176,
    "ohmic_efficiency": 0.9725042581558228,
    "pH_normalized": 0.23125991225242615,
    "precipitation_signal": 0.9872196912765503,
    "safety_risk": 0.04014495760202408,
    "score": 0.4415533244609833,
    "selective_product_yield": 0.3367062509059906,
    "transport_efficiency": 0.24745185673236847
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
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 0.92
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
    "cost": 0.30389919877052307,
    "electrochemical_conversion": 0.29430440068244934,
    "electrochemical_selectivity": 0.8895378708839417,
    "energy_efficiency": 0.8372593522071838,
    "faradaic_efficiency": 0.8070698976516724,
    "ohmic_efficiency": 0.9516416788101196,
    "pH_normalized": 0.2078981101512909,
    "precipitation_signal": 0.7090387940406799,
    "safety_risk": 0.09559440612792969,
    "score": 0.6203621029853821,
    "selective_product_yield": 0.2689790427684784,
    "transport_efficiency": 0.7823865413665771
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
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": 0.98
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
    "cost": 0.32984480261802673,
    "electrochemical_conversion": 0.265444815158844,
    "electrochemical_selectivity": 0.8350324630737305,
    "energy_efficiency": 0.7609872817993164,
    "faradaic_efficiency": 0.6858407258987427,
    "ohmic_efficiency": 0.9403808116912842,
    "pH_normalized": 0.174402117729187,
    "precipitation_signal": 0.0,
    "safety_risk": 0.1135944053530693,
    "score": 0.5586593747138977,
    "selective_product_yield": 0.22085490822792053,
    "transport_efficiency": 0.6892411112785339
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
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": 1.1
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
    "cost": 0.28893598914146423,
    "electrochemical_conversion": 0.2660398483276367,
    "electrochemical_selectivity": 0.8935827612876892,
    "energy_efficiency": 0.8750060796737671,
    "faradaic_efficiency": 0.7345069646835327,
    "ohmic_efficiency": 0.9950919151306152,
    "pH_normalized": 0.2678794264793396,
    "precipitation_signal": 0.00031451715040020645,
    "safety_risk": 0.072194404900074,
    "score": 0.5993022322654724,
    "selective_product_yield": 0.22286851704120636,
    "transport_efficiency": 0.7280116081237793
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
      "current_mA": 150,
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
    "cost": 0.29124000668525696,
    "electrochemical_conversion": 0.36664092540740967,
    "electrochemical_selectivity": 0.8804804682731628,
    "energy_efficiency": 0.7426783442497253,
    "faradaic_efficiency": 0.6498452425003052,
    "ohmic_efficiency": 0.9913796186447144,
    "pH_normalized": 0.22731485962867737,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.6080260276794434,
    "selective_product_yield": 0.3450956642627716,
    "transport_efficiency": 0.6706764698028564
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
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 0.8
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
    "cost": 0.2872079908847809,
    "electrochemical_conversion": 0.3390050232410431,
    "electrochemical_selectivity": 0.867084264755249,
    "energy_efficiency": 0.8356011509895325,
    "faradaic_efficiency": 0.876417875289917,
    "ohmic_efficiency": 0.9572204351425171,
    "pH_normalized": 0.22500072419643402,
    "precipitation_signal": 0.9928010106086731,
    "safety_risk": 0.072194404900074,
    "score": 0.6404341459274292,
    "selective_product_yield": 0.27202099561691284,
    "transport_efficiency": 0.8777674436569214
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
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1.1
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
    "cost": 0.28893598914146423,
    "electrochemical_conversion": 0.3670535981655121,
    "electrochemical_selectivity": 0.8861923813819885,
    "energy_efficiency": 0.8869682550430298,
    "faradaic_efficiency": 0.9499086737632751,
    "ohmic_efficiency": 0.9794122576713562,
    "pH_normalized": 0.22598575055599213,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.6861294507980347,
    "selective_product_yield": 0.3179970383644104,
    "transport_efficiency": 0.9570886492729187
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
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1.2
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
    "cost": 0.28919339179992676,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.0,
    "ohmic_efficiency": 0.9956789016723633,
    "pH_normalized": 0.2265060693025589,
    "precipitation_signal": 0.9940261244773865,
    "safety_risk": 0.072194404900074,
    "score": 0.045863937586545944,
    "selective_product_yield": 0.011055422015488148,
    "transport_efficiency": 0.0
  }
}
```

## K1 封存报告

Mechanistic report

1. Scope and evidential basis

This account describes the bounded synthetic electrochemical world explored in 12 completed batches. It is not a claim about any real solvent, electrolyte, or chemical identity. Solvent labels S0–S3 and electrolyte labels E0–E3 are anonymous benchmark materials. The electrode geometry and contact resistance were fixed within the campaign but hidden, so all inferred relationships are conditional on that single fixture and world.

All quantitative outcome values below are final-assay estimates, hence noisy. There were no true replicate batches. Comparisons that changed several variables simultaneously identify useful procedures, not isolated causal effects.

2. Proposed operating picture

I think performance is governed by coupled charge delivery, mass transport, interfacial selectivity, and parasitic-current processes. A useful conceptual model is:

I_eff = min(I_cap, I_kinetic(eta, medium), I_transport)

eta = V_applied - E_effective

E_effective = E_base + electrolyte_shift + solvent_shift + hidden interfacial residual

I_transport is expected to scale qualitatively with concentration, diffusivity, and diffusion-layer thickness, for example I_transport proportional to D*C/delta. Conductivity and hidden cell resistance determine an ohmic factor, while double-layer properties may determine how much current is initially non-faradaic.

A minimal conversion model would be something like:

conversion approximately 1 - exp[-k_charge*FE*integral(I_eff dt)/N0]

but this is incomplete because FE, transport efficiency, and selectivity themselves change with current, loading, potential, medium, and time. The data reject a simple model in which only total nominal charge matters.

The target pathway appears to require positive polarization. Within the productive positive-potential region, increasing duration raises conversion. Excessive current relative to transport capacity diverts charge into parasitic processes, decreasing faradaic and transport efficiencies. Selectivity has a relatively broad favorable region near +1.0 to +1.1 V for S0/E0, followed by a very sharp failure between +1.1 and +1.2 V.

Selective-product yield generally follows conversion and selectivity, but it should not be assumed to equal their exact product. The assay channels are independently calibrated and noisy, and some low-signal results are not algebraically consistent with that identity. I therefore treat conversion, selectivity, and selective-product yield as related but distinct public observables.

3. Evidence for polarity and charge-time behavior

Batch 1 established a productive baseline: 0.020 mol reagent, 0.040 L S0, E0, +1.0 V, 100 mA cap, and 3,600 s. It gave conversion 0.0965, selectivity 0.8974, selective-product yield 0.0644, faradaic efficiency 0.9736, transport efficiency 0.9449, ohmic efficiency 0.9653, energy efficiency 0.8697, and score 0.5826.

Batch 2 changed only the potential sign to -1.0 V at the same short-duration baseline. Its score fell to 0.3011; conversion was 0.0279, selectivity 0.5757, yield 0.0293, faradaic efficiency 0.3857, transport efficiency 0.4120, and energy efficiency 0.2517. Ohmic efficiency remained high at 0.9741. This is strong evidence that the productive target reaction uses the positive polarity, while negative polarization mainly drives an inefficient alternative process. It does not establish the response at every negative voltage.

Batch 4 retained S0/E0, +1.0 V, and 100 mA but extended electrolysis to 14,400 s. Conversion rose to 0.3498 and selective-product yield to 0.3145, while faradaic and transport efficiencies remained very high at 0.9760 and 0.9445. Its score rose to 0.6712. Comparing batches 1 and 4 supports continued productive charge accumulation over this time interval, with only a modest measured selectivity decrease from 0.8974 to 0.8584. Because these were not replicates, the small selectivity difference should not be overinterpreted.

Thus, under the studied loading and current cap, the system was charge-limited at 3,600 s and benefited from the maximum tested duration of 14,400 s.

4. Current and transport coupling

Batch 3 used +1.0 V, a 500 mA cap, and 7,200 s with the same 0.020 mol/0.040 L S0/E0 composition. Conversion increased to 0.1998 and yield to 0.1729, but faradaic efficiency collapsed to 0.1925, transport efficiency to 0.2090, energy efficiency to 0.2329, and ohmic efficiency to 0.8587. The score was only 0.3517.

Batch 9 tested a less extreme increase: +1.0 V, 150 mA, and 14,400 s. It reached conversion 0.3666 and yield 0.3451, slightly above batch 4, but faradaic efficiency fell to 0.6498 and transport efficiency to 0.6707. Its score, 0.6080, was below batch 4 despite the higher yield.

These results imply that nominal current above roughly 100 mA exceeds a favorable transport or interfacial-current regime in this fixture. The extra current can increase reaction progress, but an increasing fraction is lost to side reactions, charging, or transport-limited chemistry. The close co-movement of faradaic and transport efficiencies supports transport-limited parasitic current, although it does not prove which microscopic process consumes that current.

Ohmic efficiency did not move in parallel at 150 mA: batch 9 had ohmic efficiency 0.9914. Therefore the principal penalty at 150 mA was not simply bulk resistance. At 500 mA, ohmic efficiency also declined, suggesting that resistance becomes important only at the more extreme cap.

5. Loading dependence

Batch 5 reduced the reagent from 0.020 to 0.005 mol while retaining 0.040 L S0, E0, +1.0 V, 100 mA, and 14,400 s. A charge-only model would predict much higher fractional conversion at one-quarter of the substrate amount. Instead, conversion was only 0.3720, close to batch 4's 0.3498. Selectivity was 0.8971 and yield 0.3367, but faradaic efficiency fell to 0.2580, transport efficiency to 0.2475, and energy efficiency to 0.2352. The score was 0.4416.

This was a major change to the explanation. The current cap is favorable only relative to sufficient substrate concentration or transport flux. At lower loading, substrate supply becomes insufficient to sustain productive current, and parasitic pathways take over. In conceptual terms, decreasing C lowers I_transport, so the same 100 mA cap produces a much larger I/I_transport ratio. Consequently, scaling substrate down without scaling current down is not a safe route to high fractional conversion.

The lower-loading batch also had lower safety risk, 0.0401 versus approximately 0.0722 for the standard S0 loading, but safety was already well below the 0.65 limit and the efficiency loss dominated the balanced score.

6. Solvent and electrolyte effects

The nominal material dossier suggests several competing properties: conductivity, diffusivity, diffusion-layer thickness, potential shifts, acid behavior, double-layer capacitance, and precipitation tendency. The experimental results are consistent with these properties being coupled rather than with any single nominal ranking.

Batch 6 used S1/E1, +0.92 V, 100 mA, and 14,400 s at the standard loading. It produced conversion 0.2943, selectivity 0.8895, yield 0.2690, faradaic efficiency 0.8071, transport efficiency 0.7824, ohmic efficiency 0.9516, energy efficiency 0.8373, precipitation signal 0.7090, and score 0.6204.

Batch 7 used S2/E2 at +0.98 V. It gave conversion 0.2654, selectivity 0.8350, yield 0.2209, faradaic efficiency 0.6858, transport efficiency 0.6892, ohmic efficiency 0.9404, energy efficiency 0.7610, no detected precipitation signal, and score 0.5587.

Batch 8 used S0/E3 at +1.10 V. It gave conversion 0.2660, selectivity 0.8936, yield 0.2229, faradaic efficiency 0.7345, transport efficiency 0.7280, ohmic efficiency 0.9951, energy efficiency 0.8750, precipitation signal approximately 0.0003, and score 0.5993.

S0/E0 therefore gave the best observed balanced performance under the tested procedures. This does not mean S0 or E0 independently caused the advantage: S1/E1 and S2/E2 were changed as pairs, and E3 was tested only with S0. The applied potentials were also adjusted using nominal potential shifts, so material identity and residual potential mismatch are confounded.

The E3 result illustrates the trade-off particularly well. Its high nominal conductivity was consistent with excellent measured ohmic efficiency, and precipitation was nearly absent, but its faradaic and transport efficiencies and yield remained below S0/E0. Its thick nominal diffusion layer is one plausible contributor. E2/S2 also suppressed precipitation, plausibly because S2's high relative solubility product offset E2's strong nominal precipitation tendency, but this interpretation is mechanistic conjecture rather than a separately controlled result.

S0/E0 consistently showed precipitation signals near one. Nevertheless, precipitation was not a direct component of the published score, and its procedure retained the strongest efficiencies and yield. The precipitate might be benign, might be downstream of productive operation, or might impose a limitation that would emerge outside the tested duration. Its identity and causal role are unidentifiable here.

7. Potential window and sharp upper failure

At standard loading, S0/E0, 100 mA, and 14,400 s, batch 10 used +0.8 V. It gave score 0.6404, conversion 0.3390, selectivity 0.8671, yield 0.2720, faradaic efficiency 0.8764, transport efficiency 0.8778, ohmic efficiency 0.9572, and energy efficiency 0.8356.

Batch 4 at +1.0 V scored 0.6712, while batch 11 at +1.1 V was the campaign best. Batch 11 gave conversion 0.3671, selectivity 0.8862, yield 0.3180, faradaic efficiency 0.9499, transport efficiency 0.9571, ohmic efficiency 0.9794, energy efficiency 0.8870, and score 0.6861. These results locate a favorable operating region near +1.0 to +1.1 V rather than at the lowest productive voltage.

Batch 12 then changed only the applied potential from +1.1 to +1.2 V. Its measured conversion, selectivity, faradaic efficiency, transport efficiency, and energy efficiency were all zero, while selective-product yield was only 0.0111, ohmic efficiency remained 0.9957, and the score collapsed to 0.0459. The yield fell below the published 0.02 multiplicative-gate threshold, which helps explain the especially low score.

This result rules out smooth upward extrapolation from +0.8, +1.0, and +1.1 V. The simplest operational model is a sharp regime boundary between +1.1 and +1.2 V. Above it, target conversion and useful current vanish or become undetectable while electrical conduction remains efficient.

Possible mechanisms include a hidden competing redox channel, rapid target or intermediate degradation, electrode passivation, an interfacial-state transition, or a benchmark response-law switch. High ohmic efficiency argues against complete loss of electrical contact. The observations do not distinguish chemical destruction from assay-channel disappearance, and the exact threshold was not resolved. Consequently, +1.1 V is supported, but values even slightly above it should not be assumed safe.

8. Acidity, precipitation, and safety

Measured normalized pH varied with medium but was fairly stable within S0/E0: approximately 0.225–0.231 in most standard-pair batches. S1/E1 gave about 0.208, S2/E2 about 0.174, and S0/E3 about 0.268. These differences are qualitatively compatible with different nominal acid concentrations and pKa values, but the campaign did not independently vary acid properties, so pH cannot be assigned a causal coefficient.

Precipitation and pH may couple to transport, passivation, or target stability. However, the best S0/E0 batches had maximal precipitation signals, while low-precipitation material pairs performed worse. Thus precipitation signal alone is not a valid optimization surrogate in the explored domain.

Safety risk was approximately 0.0722 for standard S0/E0 batches, 0.0956 for S1/E1, and 0.1136 for S2/E2, all well below the 0.65 limit. No studied electrolysis condition produced a safety-limited optimum. These public risk values appear driven substantially by additions and material choice rather than by the electrolysis variables, but the experiment set was not designed to decompose the risk model.

9. Overall mechanistic interpretation

The world appears to contain a productive positive-potential pathway whose rate increases with useful charge and whose intrinsic selectivity is high near the optimum. The most important coupling is between current and available substrate transport. At standard concentration, a 100 mA cap maintains high faradaic and transport efficiency; 150–500 mA increasingly overwhelms the productive flux. At one-quarter loading, even 100 mA is excessive relative to substrate supply. Long duration is beneficial when the current is kept within the efficient regime.

Potential controls more than rate. From +0.8 to +1.1 V it changes activation, conversion, and energy efficiency moderately, with a local maximum near +1.1 V. By +1.2 V, a distinct nonproductive regime dominates. Medium selection changes effective potential, conductivity, transport, acidity, precipitation, and hidden interfacial residuals simultaneously. S0/E0 happens to balance those factors best in this world, despite strong precipitation.

A compact pseudocode representation would be:

eta = V - E_effective(solvent, electrolyte, hidden_interface)
transport_capacity = f(D, concentration, diffusion_layer, fixture)
productive_current = min(I_cap, kinetic_current(eta), transport_capacity)
parasitic_fraction = g(I_cap/transport_capacity, eta, loading, medium)
if eta crosses upper_regime_boundary:
    target_pathway becomes negligible and/or target degrades
FE = 1 - parasitic_fraction
conversion accumulates from productive_current over time
selectivity = favorable_window(eta, medium) modified by degradation
score = published weighted combination, with a gate when yield is below 0.02

This is a qualitative model, not an identified kinetic law.

10. Unidentifiable factors and alternatives

The campaign cannot identify the electron stoichiometry, exchange-current law, actual delivered current, equilibrium potential, transfer coefficient, diffusion coefficient after hidden residuals, electrode area, cell resistance, or identities of target and byproducts. It also cannot distinguish interfacial kinetics from mass transport quantitatively because current and concentration were sparsely sampled.

Material effects are only partly identifiable because the solvent/electrolyte design was not a full factorial. E1 and E2 were never tested with S0, while S1–S3 were not systematically crossed with every electrolyte. Applied-potential adjustments add another confound.

There were no replicate batches, so small differences comparable with instrument uncertainties may be noise. The large contrasts—polarity, high-current efficiency loss, low-loading efficiency loss, and the +1.2 V collapse—are much more persuasive than small changes in selectivity among neighboring positive-potential batches.

The sharp +1.2 V failure could represent real degradation, passivation, a hidden discontinuous benchmark law, or an observation/detection effect. The retained high ohmic efficiency narrows but does not settle these alternatives. Additional measurements would have been needed to identify the failure mechanism, but none are claimed here.

Finally, the favorable duration may not extrapolate beyond 14,400 s. Continued operation could eventually exhaust substrate, accumulate byproducts, intensify precipitation, or lower selectivity. Likewise, the local optimum between +1.1 and +1.2 V was not densely mapped.

11. Best supported procedural conclusion

The strongest observed procedure was batch 11: 0.020 mol reagent, 0.040 L S0, electrolyte E0, +1.1 V, 100 mA current cap, and 14,400 s electrolysis. Its final score was approximately 0.6861. It combines high conversion and selective-product yield with high faradaic, transport, ohmic, and energy efficiencies, and it remains below the demonstrated +1.2 V failure boundary. This is an empirical recommendation within the tested world, not proof of a universal optimum.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific prior or hidden-world ranking was supplied. The supplied material dossier contained nominal properties and explicitly warned that hidden residuals and solvent–electrolyte coupling could alter them. I therefore treated it as mechanistic background, not as a prediction of the winning material.

Supported self-developed claims:
- Positive polarity is productive under the tested baseline. Batch 1 at +1.0 V scored 0.5826, whereas otherwise matched batch 2 at -1.0 V scored 0.3011, with much lower selectivity, faradaic efficiency, transport efficiency, and energy efficiency.
- Duration helps when current remains in the efficient regime. Extending the S0/E0, +1.0 V, 100 mA procedure from 3,600 s in batch 1 to 14,400 s in batch 4 raised conversion from 0.0965 to 0.3498 and score from 0.5826 to 0.6712 while retaining high faradaic and transport efficiencies.
- Excess current causes a transport/faradaic penalty. Batch 3 at 500 mA and batch 9 at 150 mA had greater reaction progress than shorter or lower-current counterparts, but markedly worse faradaic and transport efficiencies and lower balanced scores than batch 4. The evidence supports a current-to-transport-capacity coupling rather than a charge-only law.
- Loading and current are coupled. Batch 5 used one-quarter of the standard reagent amount but the same 100 mA cap. It did not approach complete fractional conversion; instead, faradaic and transport efficiencies fell to about 0.258 and 0.247. This supports the explanation that productive current capacity decreases with available substrate concentration or flux.
- S0/E0 was the strongest tested procedure-level material combination. Batches 6–8, using S1/E1, S2/E2, and S0/E3, scored 0.6204, 0.5587, and 0.5993, below the best S0/E0 batches. This does not identify independent solvent or electrolyte effects.
- A favorable S0/E0 potential region exists near +1.0 to +1.1 V. Batch 10 at +0.8 V scored 0.6404, batch 4 at +1.0 V scored 0.6712, and batch 11 at +1.1 V scored 0.6861.

Claims contradicted or substantially revised:
- A simple total-charge model was contradicted by batches 3, 5, and 9. Nominal charge alone could not explain conversion or score because current efficiency changed strongly with current cap and loading.
- The initial broad expectation of a smooth moderate-overpotential trade-off was inadequate. Batch 12, differing from batch 11 only by increasing potential from +1.1 to +1.2 V, collapsed to score 0.0459, with reported conversion, selectivity, faradaic efficiency, transport efficiency, and energy efficiency all zero. This changed the final account from a smooth local optimum to a favorable window with a possible sharp upper regime boundary.
- High nominal conductivity was not sufficient for the best score. Batch 8 with E3/S0 had ohmic efficiency 0.9951 but lower faradaic efficiency, transport efficiency, yield, and score than batch 11. The nominal-property dossier was therefore useful mechanistically but not as a single-variable ranking.
- Lower precipitation was not synonymous with better performance. Batches 7 and 8 had negligible precipitation signals but scored below the strongly precipitating S0/E0 procedures.

Untested or unresolved claims:
- The proposed proportionality of transport capacity to D*C/delta was not quantitatively identified.
- Electron stoichiometry, actual delivered current, equilibrium potential, exchange-current behavior, electrode area, and hidden fixture resistance were not observed.
- The cause of the batch 12 collapse—degradation, passivation, a competing redox pathway, an interfacial transition, or an observation artifact—remains unresolved.
- Independent solvent and electrolyte effects were not identified because most material comparisons changed both together.
- No claim about operation beyond 14,400 s was tested.
- Negative-potential behavior was sampled only at -1.0 V in the campaign, so a general negative-potential response law was not established.

The clearest judgment-changing evidence was batch 3 for the high-current penalty, batch 4 for the benefit of long low-current operation, batch 5 for concentration/current coupling, and batch 12 for the sharp upper-potential failure.

2. Most informative additional experiment

I would repeat the standard S0/E0 procedure at +1.2 V, 100 mA, and 14,400 s with the same 0.020 mol reagent and 0.040 L solvent, but include a UV–visible measurement immediately before termination and then perform the final assay. This is one batch and directly tests whether batch 12 represents a reproducible physical regime rather than a singular final-assay or process anomaly.

Interpretation of possible outcomes:
- If the repeat again gives near-zero final conversion, selectivity, faradaic efficiency, and transport efficiency, and the pre-termination UV–visible efficiency estimates are also strongly depressed, I would substantially strengthen the sharp electrochemical/interfacial regime-switch explanation.
- If the repeat again loses final target signal but the pre-termination UV–visible measurement reports high faradaic and transport efficiencies, I would shift toward rapid late target destruction, termination-dependent chemistry, or a mismatch between proxy and final-assay channels rather than general failure of charge transfer.
- If both UV–visible and final-assay results resemble batch 11 rather than batch 12, I would treat batch 12 as an anomalous realization or measurement/process failure and withdraw the strong boundary claim.
- If the result is intermediate, I would infer a stochastic or steep but continuous transition and would broaden uncertainty around the +1.1 V recommendation. A later dense scan would then be desirable, but it is not part of this proposed single experiment.

A +1.15 V experiment would locate the boundary more precisely, but an exact +1.2 V repeat is more decisive for distinguishing the leading reproducible-regime explanation from the anomaly alternative.

3. Unused evidence, weak predictions, and goal effects

Important evidence that was available but underused includes the raw spectral artifacts, detailed peak shapes, calibration metadata, and mass-balance packets. I relied mainly on processed estimates. The intermediate UV–visible measurements were collected but were not used in a formal time-dependent fit. Detailed nominal capacitance, conductivity, diffusivity, acid, pKa, and precipitation properties were discussed qualitatively but could not be separately estimated from the sparse, confounded design. pH and precipitation signals were also not systematically manipulated, and cost and risk were not modeled beyond confirming that safety remained below the limit.

The least reliable sealed predictions are those requiring the most extrapolation: E1 with S0, E0 with S2, all -0.8 V cases, the 600 s cases, and the 500 mA cases at a new loading and potential. Their uncertainty is larger because the campaign contained only one negative-polarity batch, one 500 mA batch, no 600 s batch, and no direct observations of those cross-paired materials. Predictions with yields near the 0.02 score gate are especially fragile because a small yield error can cause a disproportionate score error.

The batch 11 recommendation is reliable as the best observed batch, but less reliable as a global optimum. It had no replicate, lies only 0.1 V below the batch 12 collapse, and the interval between +1.1 and +1.2 V was not mapped. Unexplored solvent–electrolyte combinations or a potential slightly below +1.1 V could perform better.

The assigned goal did affect evidence collection. Because the objective was to maximize the public balanced-efficiency score, later batches concentrated on promising positive-potential S0/E0 conditions rather than full factorial material identification, replication, raw-spectrum diagnostics, or mechanistic isolation of pH and precipitation. Using nearly every batch as a final-assayed optimization trial produced a useful recommendation but left causal parameters and repeatability weakly identified. There was no clear conflict with the stated goal, but there was a real optimization-versus-mechanistic-identification trade-off.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.52,
        "lower80": 0.35,
        "upper80": 0.68
      },
      "energy_efficiency": {
        "estimate": 0.2,
        "lower80": 0.08,
        "upper80": 0.35
      },
      "faradaic_efficiency": {
        "estimate": 0.3,
        "lower80": 0.15,
        "upper80": 0.45
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.129,
        "lower80": 0.05,
        "upper80": 0.24
      },
      "selective_product_yield": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.025
      },
      "transport_efficiency": {
        "estimate": 0.32,
        "lower80": 0.17,
        "upper80": 0.48
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.89,
        "lower80": 0.82,
        "upper80": 0.94
      },
      "energy_efficiency": {
        "estimate": 0.84,
        "lower80": 0.75,
        "upper80": 0.92
      },
      "faradaic_efficiency": {
        "estimate": 0.94,
        "lower80": 0.86,
        "upper80": 1
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.495,
        "lower80": 0.28,
        "upper80": 0.57
      },
      "selective_product_yield": {
        "estimate": 0.018,
        "lower80": 0.005,
        "upper80": 0.035
      },
      "transport_efficiency": {
        "estimate": 0.92,
        "lower80": 0.82,
        "upper80": 0.98
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.42,
        "upper80": 0.67
      },
      "energy_efficiency": {
        "estimate": 0.22,
        "lower80": 0.1,
        "upper80": 0.36
      },
      "faradaic_efficiency": {
        "estimate": 0.34,
        "lower80": 0.2,
        "upper80": 0.49
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.289,
        "lower80": 0.21,
        "upper80": 0.37
      },
      "selective_product_yield": {
        "estimate": 0.045,
        "lower80": 0.02,
        "upper80": 0.075
      },
      "transport_efficiency": {
        "estimate": 0.36,
        "lower80": 0.21,
        "upper80": 0.52
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.87,
        "lower80": 0.82,
        "upper80": 0.92
      },
      "energy_efficiency": {
        "estimate": 0.84,
        "lower80": 0.76,
        "upper80": 0.91
      },
      "faradaic_efficiency": {
        "estimate": 0.9,
        "lower80": 0.82,
        "upper80": 0.97
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.635,
        "lower80": 0.58,
        "upper80": 0.69
      },
      "selective_product_yield": {
        "estimate": 0.245,
        "lower80": 0.19,
        "upper80": 0.3
      },
      "transport_efficiency": {
        "estimate": 0.9,
        "lower80": 0.81,
        "upper80": 0.97
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.53,
        "lower80": 0.38,
        "upper80": 0.67
      },
      "energy_efficiency": {
        "estimate": 0.18,
        "lower80": 0.06,
        "upper80": 0.33
      },
      "faradaic_efficiency": {
        "estimate": 0.28,
        "lower80": 0.12,
        "upper80": 0.45
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.265,
        "lower80": 0.17,
        "upper80": 0.36
      },
      "selective_product_yield": {
        "estimate": 0.04,
        "lower80": 0.012,
        "upper80": 0.075
      },
      "transport_efficiency": {
        "estimate": 0.3,
        "lower80": 0.14,
        "upper80": 0.48
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.88,
        "lower80": 0.81,
        "upper80": 0.93
      },
      "energy_efficiency": {
        "estimate": 0.78,
        "lower80": 0.66,
        "upper80": 0.88
      },
      "faradaic_efficiency": {
        "estimate": 0.78,
        "lower80": 0.65,
        "upper80": 0.89
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.588,
        "lower80": 0.51,
        "upper80": 0.65
      },
      "selective_product_yield": {
        "estimate": 0.22,
        "lower80": 0.16,
        "upper80": 0.28
      },
      "transport_efficiency": {
        "estimate": 0.76,
        "lower80": 0.63,
        "upper80": 0.88
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.52,
        "lower80": 0.36,
        "upper80": 0.67
      },
      "energy_efficiency": {
        "estimate": 0.18,
        "lower80": 0.05,
        "upper80": 0.34
      },
      "faradaic_efficiency": {
        "estimate": 0.25,
        "lower80": 0.1,
        "upper80": 0.43
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.258,
        "lower80": 0.16,
        "upper80": 0.36
      },
      "selective_product_yield": {
        "estimate": 0.035,
        "lower80": 0.009,
        "upper80": 0.07
      },
      "transport_efficiency": {
        "estimate": 0.28,
        "lower80": 0.12,
        "upper80": 0.47
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.85,
        "lower80": 0.76,
        "upper80": 0.92
      },
      "energy_efficiency": {
        "estimate": 0.7,
        "lower80": 0.55,
        "upper80": 0.83
      },
      "faradaic_efficiency": {
        "estimate": 0.65,
        "lower80": 0.49,
        "upper80": 0.79
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.525,
        "lower80": 0.43,
        "upper80": 0.61
      },
      "selective_product_yield": {
        "estimate": 0.16,
        "lower80": 0.1,
        "upper80": 0.23
      },
      "transport_efficiency": {
        "estimate": 0.67,
        "lower80": 0.5,
        "upper80": 0.82
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.5,
        "lower80": 0.32,
        "upper80": 0.66
      },
      "energy_efficiency": {
        "estimate": 0.12,
        "lower80": 0.02,
        "upper80": 0.28
      },
      "faradaic_efficiency": {
        "estimate": 0.2,
        "lower80": 0.05,
        "upper80": 0.38
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.226,
        "lower80": 0.12,
        "upper80": 0.34
      },
      "selective_product_yield": {
        "estimate": 0.03,
        "lower80": 0.005,
        "upper80": 0.065
      },
      "transport_efficiency": {
        "estimate": 0.23,
        "lower80": 0.07,
        "upper80": 0.43
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.8,
        "lower80": 0.68,
        "upper80": 0.89
      },
      "energy_efficiency": {
        "estimate": 0.52,
        "lower80": 0.34,
        "upper80": 0.69
      },
      "faradaic_efficiency": {
        "estimate": 0.5,
        "lower80": 0.32,
        "upper80": 0.67
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.429,
        "lower80": 0.32,
        "upper80": 0.53
      },
      "selective_product_yield": {
        "estimate": 0.105,
        "lower80": 0.055,
        "upper80": 0.17
      },
      "transport_efficiency": {
        "estimate": 0.53,
        "lower80": 0.34,
        "upper80": 0.7
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.45,
        "lower80": 0.27,
        "upper80": 0.62
      },
      "energy_efficiency": {
        "estimate": 0.1,
        "lower80": 0.01,
        "upper80": 0.24
      },
      "faradaic_efficiency": {
        "estimate": 0.12,
        "lower80": 0.01,
        "upper80": 0.29
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.194,
        "lower80": 0.09,
        "upper80": 0.31
      },
      "selective_product_yield": {
        "estimate": 0.025,
        "lower80": 0.002,
        "upper80": 0.06
      },
      "transport_efficiency": {
        "estimate": 0.15,
        "lower80": 0.02,
        "upper80": 0.34
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.86,
        "lower80": 0.77,
        "upper80": 0.92
      },
      "energy_efficiency": {
        "estimate": 0.28,
        "lower80": 0.16,
        "upper80": 0.43
      },
      "faradaic_efficiency": {
        "estimate": 0.25,
        "lower80": 0.13,
        "upper80": 0.4
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.393,
        "lower80": 0.31,
        "upper80": 0.48
      },
      "selective_product_yield": {
        "estimate": 0.23,
        "lower80": 0.16,
        "upper80": 0.3
      },
      "transport_efficiency": {
        "estimate": 0.27,
        "lower80": 0.14,
        "upper80": 0.43
      }
    }
  ],
  "rationale": "Predictions interpolate the campaign’s S0/E0 polarity, duration, loading, material-shift, and current-cap contrasts. Positive 100 mA conditions retain high selectivity and efficiency; negative polarity is mostly parasitic, while 500 mA incurs severe faradaic/transport penalties. E1 and E3 estimates incorporate their observed material penalties and nominal potential shifts; S2/E0 is more uncertain because that pair was not tested. Intervals combine assay noise with wider model uncertainty for new material pairings, short duration, negative polarity, and the 500 mA regime; score estimates also account for the yield gate near 0.02."
}
```
