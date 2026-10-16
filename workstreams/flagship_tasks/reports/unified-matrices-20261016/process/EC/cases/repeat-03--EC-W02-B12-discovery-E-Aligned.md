# repeat-03/EC-W02-B12-discovery-E-Aligned

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-03\EC-W02-B12-discovery-E-Aligned\participant\discovery-E-Aligned

## 同期笔记

### v1 · 公开事件 0

# Pre-experiment hypotheses

**H1 [tentative]** Product formation is polarity-dependent and rises with electrolysis charge/time until conversion saturates; excessive potential or duration may lower selectivity through a competing degradation pathway. A sign reversal should sharply reduce target yield if the target is formed only in one electrode direction.

**H2 [tentative]** At fixed reagent loading, electrolyte/solvent conductivity and transport jointly determine delivered current and thus conversion, but selectivity also depends on interfacial potential shifts and proton activity. Therefore the most conductive pair need not maximize selective yield or energy efficiency.

**H3 [tentative]** A nonzero current cap can be transport-limited: raising the cap should matter only until the cell's delivered current is set by resistance/kinetics. At comparable conditions, time and cap effects will help distinguish charge control from pure elapsed-time chemistry.

Plan: use 0.020 mol reagent in 0.040 L solvent for all batches; span both potential signs, durations, current caps, and material identities, with matched comparisons and one intermediate measurement per batch. Predictions: positive-potential moderate conditions will outperform negative polarity under at least one material pair; very aggressive positive electrolysis may increase conversion but reduce selectivity/efficiency. These expectations will be revised if observations contradict them.

### v2 · 公开事件 42

# Working hypotheses after six batches

**H1 [supported in tested S0/E0 scope, revised polarity]** Target accumulation is favored at negative rather than positive potential. At 600 s, +1.0 V gave zero reported selective yield despite high efficiency estimates (event runner-operation-0007), whereas -1.0 V gave a small positive yield (runner-operation-0014). Negative-potential responses are not monotone in magnitude across -0.5, -1.0, -1.5 V (runner-operation-0021, -0014, -0028); -1.0 V is provisionally near the better region. Because yields are near assay noise at 600 s, the voltage-shape claim remains unresolved.

**H2 [supported for duration, S0/E0/-1 V]** Conversion and selective yield rise strongly with duration: 600, 7200, and 14400 s give approximately 0/0.012, 0.075/0.049, and 0.146/0.092 for conversion/yield (runner-operation-0014, -0035, -0042). Selectivity stays about 0.57 at the two long durations, consistent with approximately linear charge accumulation over this range rather than late degradation. Prediction: at 14400 s, material or current changes should primarily alter conversion through delivered charge/transport, while selectivity may shift separately.

**H3 [unresolved]** The +1 V batch had high reported Faradaic/transport/energy efficiencies but no target yield; this suggests efficiency channels may describe total electrochemistry rather than target formation, or that polarity directs charge to a different product. Final target yield, not UV-vis efficiency alone, will guide the material screen.

**Confound C1:** precipitation signal is essentially saturated for S0/E0 in every assay, so this pair cannot identify whether precipitation limits target recovery. Material variants with lower nominal precipitating salt / higher solubility will test that alternative.

### v3 · 公开事件 84

# Final source-stage hypotheses

**H1 [supported in tested domain] — polarity and potential window.** At 0.020 mol reagent / 0.040 L, target formation is cathodic in this benchmark: long -1.0 V electrolysis produces substantial selective yield (runner-operation-0042), whereas +1.0 V at 600 s produced no reported target despite high Faradaic/transport efficiency (runner-operation-0007). The 600 s comparison is near the assay floor, so the exact sign contrast at longer times was not directly replicated. Within negative potentials, the sparse 600 s data at -0.5, -1.0, -1.5 V do not resolve a smooth optimum because target signals are near zero (runner-operation-0021, -0014, -0028). Use -1.0 V as the empirically anchored setting, not as a proven global optimum.

**H2 [supported in S0/E0 at -1.0 V] — time/charge accumulation.** From 7200 to 14400 s, conversion rises 0.0754→0.1461 and selective yield 0.0492→0.0918 while selectivity remains about 0.57 (runner-operation-0035, -0042). This is consistent with approximately linear charge-controlled accumulation over that interval and no observed late selectivity collapse. The 600 s assay is noisy near zero. Extrapolation should be bounded: eventual reagent depletion or degradation was not observed/tested.

**H3 [supported] — current cap is active at low caps, with a higher-cap plateau unresolved.** At otherwise matched S0/E0, -1.0 V, 14400 s, lowering the cap from 100 to 10 to 1 mA reduces conversion/yield from 0.146/0.0918 to 0.0246/0.0153 to reported zero/zero (runner-operation-0042, -0049, -0056). Thus time alone is insufficient; delivered charge is constrained by the cap at least below 10 mA. The response is sub-proportional between 10 and 100 mA, consistent with resistance/kinetic limitation or assay floor. Caps above 100 mA were not tested, so the plateau threshold is unknown.

**H4 [supported qualitatively, effect attribution unresolved] — materials change precipitation, pH, transport, and yield separately.** At -1.0 V, 100 mA, 14400 s, diagonal S0/E0, S1/E1, S2/E2, S3/E3 give yields about 0.0918, 0.0880, 0.0537, 0.0584 and precipitation about 0.998, 0.715, 0, 0.005 (runner-operation-0042, -0063, -0070, -0077). Eliminating precipitation therefore does not by itself improve target yield. Mixed S0/E3 gives zero precipitation but yield 0.0774 (runner-operation-0084), suggesting S0 contributes favorably relative to S3 under E3, though a matched S3/E3 comparison changes both only by solvent and supports that direction with a numerical difference larger than final-assay yield noise. Electrolyte effects remain partly confounded because only E3 was crossed with two solvents.

**Mechanistic working account.** Negative polarization drives the target-forming electron-transfer branch. Product accumulation is governed by effective charge (duration × delivered current) multiplied by a material-dependent Faradaic/transport factor; selectivity is comparatively stable near 0.52–0.57 for the tested long negative runs. Nominal conductivity and potential shifts influence delivered current/efficiency, while proton activity and precipitation alter pH/solid signal, but precipitation is not the main yield determinant in this range. Positive polarization can sustain efficient non-target electrochemistry, so efficiency channels cannot be equated with target yield across signs.

**Operating decision.** Batch 6 (S0/E0, -1.0 V, 100 mA cap, 14400 s) is the recommendation because it has the highest observed score (0.3322) and target yield (0.0918) among completed batches, without a degradation/selectivity loss versus 7200 s. I would change this choice if a replicated low-precipitation material condition exceeded it beyond assay variability, or if longer/higher-current testing revealed a safer high-yield plateau.

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
    "electrochemical_conversion": 0.02276882901787758,
    "electrochemical_selectivity": 0.8974339962005615,
    "energy_efficiency": 0.869667649269104,
    "faradaic_efficiency": 0.9735972285270691,
    "ohmic_efficiency": 0.9653005003929138,
    "pH_normalized": 0.22897005081176758,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.0,
    "selective_product_yield": 0.0,
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
    "electrochemical_selectivity": 0.575653076171875,
    "energy_efficiency": 0.2517053484916687,
    "faradaic_efficiency": 0.3857153058052063,
    "ohmic_efficiency": 0.9741383194923401,
    "pH_normalized": 0.22627469897270203,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.1814069002866745,
    "selective_product_yield": 0.012373019941151142,
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
      "current_mA": 100,
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
      "operation": "terminate"
    },
    {
      "instrument": "final_assay",
      "operation": "measure"
    }
  ],
  "metrics": {
    "cost": 0.28271999955177307,
    "electrochemical_conversion": 0.0019589851144701242,
    "electrochemical_selectivity": 0.6197043061256409,
    "energy_efficiency": 0.5943892598152161,
    "faradaic_efficiency": 0.45556560158729553,
    "ohmic_efficiency": 0.9353523254394531,
    "pH_normalized": 0.22698970139026642,
    "precipitation_signal": 0.9871450662612915,
    "safety_risk": 0.072194404900074,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.4721224904060364
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
    "cost": 0.2829599976539612,
    "electrochemical_conversion": 0.0010065361857414246,
    "electrochemical_selectivity": 0.4767659604549408,
    "energy_efficiency": 0.08669000118970871,
    "faradaic_efficiency": 0.33636927604675293,
    "ohmic_efficiency": 0.9815899729728699,
    "pH_normalized": 0.22629910707473755,
    "precipitation_signal": 0.987893283367157,
    "safety_risk": 0.072194404900074,
    "score": 0.03772210702300072,
    "selective_product_yield": 0.0032109112944453955,
    "transport_efficiency": 0.3048817217350006
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
      "potential_V": -1
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
    "cost": 0.28547999262809753,
    "electrochemical_conversion": 0.0754348635673523,
    "electrochemical_selectivity": 0.5720658898353577,
    "energy_efficiency": 0.23707550764083862,
    "faradaic_efficiency": 0.3968895971775055,
    "ohmic_efficiency": 0.9725042581558228,
    "pH_normalized": 0.23125991225242615,
    "precipitation_signal": 0.9872196912765503,
    "safety_risk": 0.072194404900074,
    "score": 0.3077346384525299,
    "selective_product_yield": 0.04918275400996208,
    "transport_efficiency": 0.3863801062107086
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
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1
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
    "electrochemical_conversion": 0.14612282812595367,
    "electrochemical_selectivity": 0.5698725581169128,
    "energy_efficiency": 0.2596757113933563,
    "faradaic_efficiency": 0.4099213182926178,
    "ohmic_efficiency": 0.974361002445221,
    "pH_normalized": 0.2279839664697647,
    "precipitation_signal": 0.9978500008583069,
    "safety_risk": 0.072194404900074,
    "score": 0.3322393000125885,
    "selective_product_yield": 0.09177185595035553,
    "transport_efficiency": 0.3852379620075226
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
      "current_mA": 10,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1
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
    "cost": 0.2831760048866272,
    "electrochemical_conversion": 0.024602117016911507,
    "electrochemical_selectivity": 0.5605422854423523,
    "energy_efficiency": 0.260945200920105,
    "faradaic_efficiency": 0.38404905796051025,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.22699855268001556,
    "precipitation_signal": 0.9828920960426331,
    "safety_risk": 0.072194404900074,
    "score": 0.22590750455856323,
    "selective_product_yield": 0.015310198068618774,
    "transport_efficiency": 0.3874494135379791
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
      "current_mA": 1,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1
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
    "cost": 0.28265759348869324,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.5569276809692383,
    "energy_efficiency": 0.25591298937797546,
    "faradaic_efficiency": 0.3895479440689087,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.2253010869026184,
    "precipitation_signal": 0.9957649111747742,
    "safety_risk": 0.072194404900074,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.3830525875091553
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
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -1
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
    "cost": 0.3043600022792816,
    "electrochemical_conversion": 0.12123311311006546,
    "electrochemical_selectivity": 0.5655837655067444,
    "energy_efficiency": 0.3015159070491791,
    "faradaic_efficiency": 0.3213653862476349,
    "ohmic_efficiency": 0.9853024482727051,
    "pH_normalized": 0.20722901821136475,
    "precipitation_signal": 0.7148279547691345,
    "safety_risk": 0.09559440612792969,
    "score": 0.32019495964050293,
    "selective_product_yield": 0.08799666166305542,
    "transport_efficiency": 0.34219664335250854
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
      "solvent": 2,
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -1
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
    "cost": 0.3299599885940552,
    "electrochemical_conversion": 0.12002012133598328,
    "electrochemical_selectivity": 0.555263876914978,
    "energy_efficiency": 0.26884979009628296,
    "faradaic_efficiency": 0.28950586915016174,
    "ohmic_efficiency": 0.8998906016349792,
    "pH_normalized": 0.17240428924560547,
    "precipitation_signal": 0.0,
    "safety_risk": 0.1135944053530693,
    "score": 0.28754016757011414,
    "selective_product_yield": 0.0536787323653698,
    "transport_efficiency": 0.2908554673194885
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
      "solvent": 3,
      "volume_L": 0.04
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": -1
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
    "cost": 0.3139599859714508,
    "electrochemical_conversion": 0.12019973248243332,
    "electrochemical_selectivity": 0.523597776889801,
    "energy_efficiency": 0.307341068983078,
    "faradaic_efficiency": 0.28830376267433167,
    "ohmic_efficiency": 0.9778853058815002,
    "pH_normalized": 0.27916985750198364,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.12619440257549286,
    "score": 0.29655858874320984,
    "selective_product_yield": 0.05840711668133736,
    "transport_efficiency": 0.29548370838165283
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
      "potential_V": -1
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
    "electrochemical_conversion": 0.10200194269418716,
    "electrochemical_selectivity": 0.5431946516036987,
    "energy_efficiency": 0.2942160367965698,
    "faradaic_efficiency": 0.2832440435886383,
    "ohmic_efficiency": 0.9921419024467468,
    "pH_normalized": 0.2690844237804413,
    "precipitation_signal": 0.0,
    "safety_risk": 0.072194404900074,
    "score": 0.30284732580184937,
    "selective_product_yield": 0.07742659747600555,
    "transport_efficiency": 0.3044689893722534
  }
}
```

## K1 封存报告

## Mechanism report

### 1. Empirical scope

All twelve batches used the same initial loading: 0.020 mol of limiting reagent in 0.040 L of solvent, nominally 0.50 mol L⁻¹ before sampling. Consequently, the campaign identifies responses to potential, electrolysis duration, current cap, solvent, and electrolyte only at that loading and volume. Every condition was run once; apparent differences must therefore be interpreted in light of the stated final-assay noise and uncontrolled process variation.

The principal interpretation is that negative polarization accesses the target-forming branch, while accumulated product is governed by effective delivered charge and material-dependent charge utilization. Solvent and electrolyte separately affect transport, interfacial energetics, acid/base state, and precipitation. The measured efficiency channels describe total electrochemical performance and do not necessarily describe formation of the desired product.

### 2. Proposed process model

A useful phenomenological description is:

Q_eff = t × min(I_cap, I_cell(V,S,E,state))

X = 1 − exp[−k_X(V,S,E) Q_eff/n₀]

Y_target ≈ X × s_target(V,S,E) × r(S,E,pH,precipitation)

Here Q_eff is effective charge, I_cell is the current the cell could deliver given potential, solvent, electrolyte, shared fixture resistance, transport, and evolving state; X is electrochemical conversion; s_target is the fraction of converted material entering the desired branch; and r is a material-dependent recovery or persistence factor. In the low-conversion region sampled here, the conversion equation reduces approximately to X ≈ k_X Q_eff/n₀.

The measured energy efficiency can be understood qualitatively as a product of several imperfect factors, for example

η_energy ∝ η_F × η_transport × η_ohmic × g(V),

where g(V) accounts for voltage overhead and other losses. This is not an identified exact law: the assay channels are noisy synthetic observables, and the campaign did not measure actual current or charge. It nevertheless explains why a condition can show good Faradaic, transport, and ohmic efficiencies while making little or no target if its charge is directed to another electrochemical branch.

### 3. Potential polarity and target branching

Batch 1 used S0/E0, +1.0 V, a 100 mA cap, and 600 s. It reported high Faradaic efficiency (0.9736), transport efficiency (0.9449), ohmic efficiency (0.9653), energy efficiency (0.8697), conversion 0.02277, and selectivity 0.8974, but selective product yield was reported as zero. Thus positive polarization supported electrochemistry, but the efficiency channels did not translate into detected desired product.

The matched negative-potential Batch 2 used −1.0 V for 600 s. It had much lower Faradaic, transport, and energy efficiencies (0.3857, 0.4120, and 0.2517) yet gave a small positive selective yield of 0.01237. Its conversion was clipped or reported at zero, making conversion and yield internally inconsistent near the detection floor. I interpret that inconsistency as independent assay noise or clipping, not as literal product formation at exactly zero conversion.

Batches 3 and 4 tested −0.5 and −1.5 V at the same 100 mA cap and 600 s. Their conversion/yield pairs were 0.00196/0 and 0.00101/0.00321, respectively. These signals are too close to the assay floor to establish a reliable voltage-response curve. The data empirically anchor −1.0 V as a workable negative setting, but they do not prove that −1.0 V is a global potential optimum.

My mechanistic conjecture is that negative polarization drives the desired electron-transfer direction, whereas positive polarization favors a different electrochemical transformation or background process. A less specific alternative is that both signs can form target, but their onset potentials differ and the short 600 s trials were too insensitive to resolve it. Because no long-duration positive-potential batch was run, polarity specificity remains suggestive rather than conclusively established.

### 4. Duration dependence

The strongest identified relationship is the duration response at S0/E0, −1.0 V, and a 100 mA cap:

- Batch 2, 600 s: conversion 0, yield 0.01237, selectivity 0.5757.
- Batch 5, 7200 s: conversion 0.07543, yield 0.04918, selectivity 0.5721.
- Batch 6, 14400 s: conversion 0.14612, yield 0.09177, selectivity 0.5699.

Between 7200 and 14400 s, doubling time nearly doubled both conversion and yield. The incremental slopes over that interval are approximately 9.8×10⁻⁶ conversion units s⁻¹ and 5.9×10⁻⁶ yield units s⁻¹. Selectivity remained essentially constant near 0.57. This is consistent with approximately linear accumulation at low conversion, with no detectable late loss of selectivity or degradation through 14400 s.

This relationship should not be extrapolated indefinitely. A saturating charge model is more plausible once reagent depletion, mass-transfer limitation, product degradation, or electrode passivation becomes important. The campaign reached only about 15% conversion, so it did not identify that saturation region.

### 5. Current-cap dependence

Batches 6–8 isolate the effect of the current cap at S0/E0, −1.0 V, and 14400 s:

- 100 mA cap, Batch 6: conversion 0.14612; yield 0.09177.
- 10 mA cap, Batch 7: conversion 0.02460; yield 0.01531.
- 1 mA cap, Batch 8: conversion and yield both reported as zero.

Selectivity remained fairly stable—0.5699, 0.5605, and 0.5569—despite the large change in conversion. This supports a picture in which the current cap controls the reaction rate without greatly changing branch selectivity over this range. The response from 10 to 100 mA was sub-proportional: conversion rose by about sixfold rather than tenfold. Possible explanations include cell resistance or interfacial kinetics limiting the actual current below the 100 mA setting, nonlinear transport losses, and increased importance of the assay floor at the 10 mA condition.

The data establish that caps at or below 10 mA are consequential. They do not establish whether 100 mA is already above the natural cell-current plateau, because no cap above 100 mA was tested and actual current was not observed.

### 6. Material, pH, and precipitation couplings

At −1.0 V, 100 mA, and 14400 s, the four diagonal material pairs gave:

- Batch 6, S0/E0: conversion 0.14612, selectivity 0.5699, yield 0.09177, precipitation 0.99785, pH-normalized 0.2280, score 0.3322.
- Batch 9, S1/E1: conversion 0.12123, selectivity 0.5656, yield 0.08800, precipitation 0.71483, pH-normalized 0.2072, score 0.3202.
- Batch 10, S2/E2: conversion 0.12002, selectivity 0.5553, yield 0.05368, precipitation 0, pH-normalized 0.1724, score 0.2875.
- Batch 11, S3/E3: conversion 0.12020, selectivity 0.5236, yield 0.05841, precipitation 0.00524, pH-normalized 0.2792, score 0.2966.

The lower-precipitation pairs did not produce higher target yield. In particular, S0/E0 had nearly saturated precipitation yet the highest conversion and yield, whereas S2/E2 and S3/E3 essentially eliminated precipitation but gave lower yields. Therefore precipitation is not the dominant cause of lost target yield in this tested region. It may represent precipitation of a supporting salt or another nuisance phase rather than the desired product. It could still affect transport or recovery, but its effect is outweighed by other material factors.

The nominal material dossier supplies plausible couplings. Conductivity, diffusivity, diffusion-layer thickness, and solvent transport factors affect I_cell and η_transport. Standard-potential shifts change the effective overpotential at a fixed applied voltage. Proton activity, acid concentration, and pKa affect proton-coupled electron transfer and the measured pH. Salt concentration and solubility product determine precipitation. Double-layer capacitance can alter charging losses and the interfacial field. These influences are correlated, so a simple ranking by bulk conductivity alone is not expected to predict target yield.

Batch 12 provides the only direct solvent contrast at a fixed electrolyte: S0/E3 versus S3/E3 in Batch 11. Batch 12 gave conversion 0.10200, selectivity 0.5432, yield 0.07743, precipitation 0, and pH-normalized 0.2691. Relative to S3/E3, changing to S0 lowered conversion from 0.1202 to 0.1020 but increased selectivity from 0.5236 to 0.5432 and yield from 0.0584 to 0.0774. The yield difference, about 0.019, is larger than the nominal 0.01 final-assay yield noise, although it remains a single comparison. This suggests that S0 favors target branching, stability, or assay recovery under E3 even though it does not maximize total conversion in that pair.

No electrolyte was crossed with multiple solvents except E3, and only S0 was used with multiple electrolytes in Batches 6 and 12. Even that S0 comparison changes E0 to E3 and shows conversion/yield falling from 0.1461/0.0918 to 0.1020/0.0774 while precipitation falls to zero. It supports an E0 advantage under S0 but cannot identify whether conductivity, overpotential shift, proton chemistry, hidden residuals, or another electrolyte property causes it.

### 7. Relation between conversion, selectivity, and yield

A first approximation is Y_target ≈ X × selectivity, but the observations do not satisfy that identity exactly. For Batch 6, X × selectivity is about 0.083, compared with measured yield 0.0918. For Batch 9 it is about 0.0686 versus yield 0.0880; for Batch 10 it is about 0.0666 versus yield 0.0537. These discrepancies can arise from independent channel noise, distinct definitions or calibrations, a material-dependent recovery factor, or conversion and selectivity referring to electrochemical rather than isolated-product quantities.

I therefore treat conversion, electrochemical selectivity, and selective product yield as related but nonredundant observables. An improved predictive model would include a recovery/persistence factor rather than forcing yield to equal the product of the other two channels exactly.

### 8. What changed the explanation

The initial expectation was that moderate positive polarization might be productive and that overly aggressive operation might sacrifice selectivity. Batch 1 contradicted the first part: it had excellent efficiency metrics but no target yield. Batch 2 shifted the working account toward a cathodic target branch.

Batches 5 and 6 were decisive for the charge-accumulation model. Their near-proportional duration response and stable selectivity argued against rapid late degradation over the observed interval.

Batches 7 and 8 showed that elapsed time is not sufficient by itself and that low current caps strongly restrict conversion. This changed the explanation from a generic time-dependent process to an effective-charge model.

Batches 9–12 changed the interpretation of precipitation. Near-zero precipitation did not improve yield, so precipitation was demoted from a possible principal loss mechanism to a correlated or secondary material response. Batch 12 also showed that solvent can change target yield in a direction different from total conversion.

### 9. Unidentified quantities and alternatives

Several important factors are not identifiable from this campaign:

1. Actual current, integrated charge, electrode area, cell resistance, electrode gap, and kinetic exchange-current parameters were not observed. The shared fixture was constant across batches but unknown.
2. Chemical identities and species-level assignments are deliberately hidden. The desired and competing reactions cannot be written as molecular half-reactions.
3. The exact onset potential, Tafel slope, mass-transfer limiting current, electron stoichiometry, and charge required per mole are not identified.
4. Solvent and electrolyte properties are correlated. Most material trials changed both simultaneously, preventing clean attribution.
5. Product precipitation cannot be distinguished from precipitation of an electrolyte-derived phase using the reported scalar signal alone.
6. Each condition had a single final assay. Near-zero results, especially Batches 2–4 and 8, are strongly affected by clipping and measurement noise.
7. No long-duration positive control, no potential scan at long duration, no conditions above 100 mA, and no run beyond 14400 s were performed.
8. Temperature evolution, electrode passivation, and time-dependent solution composition were not independently measured.

Plausible alternative accounts include: positive and negative potentials both form target but with different thresholds; the apparent cathodic preference is a short-time detection artifact; material-dependent assay recovery rather than chemistry creates part of the yield ranking; or precipitation changes active surface area while a compensating transport effect masks its influence. The available evidence favors the effective-charge/cathodic-branch model but does not uniquely exclude these alternatives.

### 10. Overall conclusion and bounded prediction rule

Within the tested 0.020 mol/0.040 L regime, target yield is best explained as a cathodic, effective-charge-driven response. Duration and current cap control how much reaction occurs, while voltage sign and materials control which branch receives that charge and how efficiently product persists or is recovered. Selectivity was comparatively stable around 0.52–0.57 across the long negative-potential experiments, so most observed yield variation there came from conversion and a secondary material/recovery factor rather than large selectivity changes. High electrochemical efficiency at positive potential should not be interpreted as high target yield.

For interpolation near the tested domain, I would predict conversion approximately proportional to duration at fixed −1.0 V and sufficiently high current cap, then apply material-specific selectivity and recovery corrections. I would impose saturation outside the observed low-conversion range and would not extrapolate the linear law past 14400 s or to a different loading without additional evidence. Batch 6—S0/E0, −1.0 V, 100 mA, 14400 s—remains the strongest observed operating point, but it is an empirical local recommendation rather than proof of the global mechanistic optimum.

## K2 封存报告

1. **Claims and laws assessed**

No instance-specific prior mechanism or response law was supplied. The material dossier provided nominal properties and cautioned that hidden, fixed residuals could modify them; I treated those properties as qualitative priors rather than ground truth.

- **Supported:** My effective-charge law was supported within the tested negative-potential regime. At S0/E0, −1.0 V and 100 mA, increasing duration from 7200 s in Batch 5 to 14400 s in Batch 6 raised conversion from 0.0754 to 0.1461 and yield from 0.0492 to 0.0918, while selectivity stayed near 0.57. Batches 6–8 also showed that lowering the current cap from 100 to 10 to 1 mA reduced yield from 0.0918 to 0.0153 to zero. These observations changed the account from generic elapsed-time dependence to dependence on delivered charge constrained by current and cell transport.

- **Partly supported but not established:** A target-favoring negative-polarity branch was suggested by Batch 2, where −1.0 V produced a small yield of 0.0124, while Batch 1 at +1.0 V reported zero yield. However, Batch 1 simultaneously showed conversion 0.0228, selectivity 0.897, and high efficiencies. Because both trials lasted only 600 s and their yields were near the assay floor, this is not decisive evidence for strict polarity specificity. Batches 3 and 4 at −0.5 and −1.5 V also remained near zero, so they did not identify a voltage optimum.

- **Contradicted or revised:** The initial conjecture that moderate positive polarization would straightforwardly maximize desired product was contradicted by the zero reported yield in Batch 1, despite excellent efficiency channels. The initial concern that longer aggressive electrolysis would already reduce selectivity was not supported: Batches 5 and 6 retained nearly constant selectivity as duration doubled. The idea that precipitation was the principal yield-limiting loss was contradicted by the material screen. Batch 6 had precipitation 0.998 and the highest yield, whereas Batches 10 and 11 had precipitation near zero but yields only 0.0537 and 0.0584.

- **Material claims only partially identified:** Batch 12 versus Batch 11 isolated one solvent contrast under E3: S0 increased yield from 0.0584 to 0.0774 even though conversion fell from 0.1202 to 0.1020. This supports separate effects on conversion and target recovery or branching. Most other material comparisons, such as Batches 6, 9, 10, and 11, changed solvent and electrolyte together, so attribution to conductivity, proton activity, potential shift, or hidden residuals remains untested.

- **Untested:** Saturation at high conversion, degradation beyond 14400 s, the current plateau above 100 mA, actual delivered current, long-duration positive-potential behavior, electron stoichiometry, and molecular reaction identities were not tested.

2. **Best additional discriminating experiment**

I would run the exact Batch 6 formulation and duration—0.020 mol reagent, 0.040 L S0, E0, 100 mA cap, and 14400 s—but reverse the potential from −1.0 to +1.0 V. This is the missing long-duration polarity control.

Before seeing the result, I would interpret outcomes as follows:

- A positive-potential yield remaining below about 0.02 while conversion and efficiency channels are appreciable would strongly support the leading branch-specific explanation: positive polarization conducts charge into a non-target process, so efficiency cannot be equated with target yield.
- A yield comparable to or exceeding Batch 6—roughly 0.07–0.10 or more—would substantially weaken or reject strict cathodic specificity. It would instead favor the alternative that Batch 1 was dominated by short-time accumulation, clipping, or measurement noise and that positive polarization may actually be highly productive after sufficient charge.
- Low conversion and low yield would support a polarity-dependent kinetic or onset limitation, but would not distinguish target branching from a general lack of electrochemical turnover.
- High conversion and intermediate yield would favor a continuous polarity-dependent selectivity model rather than two fully distinct branches.

A replicate would ultimately be desirable, but this single matched experiment has greater discriminatory value than another material screen because the leading polarity conclusion currently rests on short, near-floor observations.

3. **Unused evidence, reliability, and effect of the goal**

The raw characterization artifacts and full spectra were not inspected, so peak shapes, calibration residuals, clipping details, and possible spectral evidence for competing products were unused. Intermediate UV–visible observations were collected in every batch but were used mainly as corroborating efficiency measurements rather than analyzed as a complete time-resolved dataset. Cost and safety were recorded but varied little enough in the chosen conditions that they did not drive the mechanism. The nominal capacitance, acid, diffusivity, diffusion-layer, and solubility-product properties were discussed qualitatively but were not quantitatively fitted because the material design was too confounded.

The least reliable predictions are the long positive-potential cases, especially Q04, Q06, Q08, Q10, and Q12. They extrapolate from only Batch 1, whose high conversion/selectivity and zero yield admit two opposing interpretations. Predictions at 500 mA, Q11 and Q12, are also weak because no cap above 100 mA was tested. Material predictions involving S2/E0 or positive potentials with E1/E3 rely on incomplete crosses. Short-duration scores in Q01 and Q02 are especially unstable because the published score gate changes rapidly when yield lies near 0.02. All predictions additionally transfer from 0.020 mol in 0.040 L to 0.012 mol in 0.025 L; the concentrations are similar, but invariance to absolute amount and volume was not directly tested.

The Batch 6 recommendation is more reliable as a local empirical choice than as a global optimum: it had the highest observed score and yield, but potential, current, duration, and materials were only sparsely searched and no condition was replicated.

The assigned explanatory goal materially shaped evidence collection. I spent batches on polarity, duration, current-cap, and material contrasts rather than concentrating solely on score optimization. That produced useful mechanistic contrasts, including Batches 5–8, but left fewer opportunities for replication, a full solvent-by-electrolyte factorial design, or optimization around Batch 6. I see no clear conflict between the research goal and honest use of the evidence; the trade-off was breadth and causal diagnosis versus precision and optimization.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.595,
        "lower80": 0.54,
        "upper80": 0.65
      },
      "energy_efficiency": {
        "estimate": 0.36,
        "lower80": 0.26,
        "upper80": 0.46
      },
      "faradaic_efficiency": {
        "estimate": 0.42,
        "lower80": 0.36,
        "upper80": 0.48
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.1271,
        "lower80": 0.0,
        "upper80": 0.27
      },
      "selective_product_yield": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.027
      },
      "transport_efficiency": {
        "estimate": 0.43,
        "lower80": 0.35,
        "upper80": 0.51
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.91,
        "lower80": 0.84,
        "upper80": 0.97
      },
      "energy_efficiency": {
        "estimate": 0.9,
        "lower80": 0.76,
        "upper80": 0.98
      },
      "faradaic_efficiency": {
        "estimate": 0.95,
        "lower80": 0.88,
        "upper80": 1.0
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.50805,
        "lower80": 0.05,
        "upper80": 0.64
      },
      "selective_product_yield": {
        "estimate": 0.018,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "transport_efficiency": {
        "estimate": 0.93,
        "lower80": 0.84,
        "upper80": 1.0
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.59,
        "lower80": 0.55,
        "upper80": 0.63
      },
      "energy_efficiency": {
        "estimate": 0.35,
        "lower80": 0.27,
        "upper80": 0.44
      },
      "faradaic_efficiency": {
        "estimate": 0.42,
        "lower80": 0.37,
        "upper80": 0.47
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.3375,
        "lower80": 0.27,
        "upper80": 0.4
      },
      "selective_product_yield": {
        "estimate": 0.055,
        "lower80": 0.025,
        "upper80": 0.09
      },
      "transport_efficiency": {
        "estimate": 0.43,
        "lower80": 0.37,
        "upper80": 0.49
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.91,
        "lower80": 0.84,
        "upper80": 0.97
      },
      "energy_efficiency": {
        "estimate": 0.88,
        "lower80": 0.74,
        "upper80": 0.98
      },
      "faradaic_efficiency": {
        "estimate": 0.95,
        "lower80": 0.87,
        "upper80": 1.0
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.6329,
        "lower80": 0.45,
        "upper80": 0.72
      },
      "selective_product_yield": {
        "estimate": 0.19,
        "lower80": 0.06,
        "upper80": 0.32
      },
      "transport_efficiency": {
        "estimate": 0.93,
        "lower80": 0.83,
        "upper80": 1.0
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.53,
        "upper80": 0.63
      },
      "energy_efficiency": {
        "estimate": 0.37,
        "lower80": 0.27,
        "upper80": 0.47
      },
      "faradaic_efficiency": {
        "estimate": 0.36,
        "lower80": 0.29,
        "upper80": 0.43
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.3292,
        "lower80": 0.25,
        "upper80": 0.4
      },
      "selective_product_yield": {
        "estimate": 0.057,
        "lower80": 0.025,
        "upper80": 0.095
      },
      "transport_efficiency": {
        "estimate": 0.38,
        "lower80": 0.3,
        "upper80": 0.46
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.87,
        "lower80": 0.77,
        "upper80": 0.95
      },
      "energy_efficiency": {
        "estimate": 0.75,
        "lower80": 0.57,
        "upper80": 0.9
      },
      "faradaic_efficiency": {
        "estimate": 0.85,
        "lower80": 0.7,
        "upper80": 0.96
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.5608,
        "lower80": 0.39,
        "upper80": 0.66
      },
      "selective_product_yield": {
        "estimate": 0.14,
        "lower80": 0.035,
        "upper80": 0.27
      },
      "transport_efficiency": {
        "estimate": 0.8,
        "lower80": 0.63,
        "upper80": 0.93
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.56,
        "lower80": 0.5,
        "upper80": 0.62
      },
      "energy_efficiency": {
        "estimate": 0.34,
        "lower80": 0.24,
        "upper80": 0.44
      },
      "faradaic_efficiency": {
        "estimate": 0.3,
        "lower80": 0.23,
        "upper80": 0.37
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.3047,
        "lower80": 0.23,
        "upper80": 0.38
      },
      "selective_product_yield": {
        "estimate": 0.05,
        "lower80": 0.018,
        "upper80": 0.085
      },
      "transport_efficiency": {
        "estimate": 0.32,
        "lower80": 0.24,
        "upper80": 0.4
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.83,
        "lower80": 0.7,
        "upper80": 0.93
      },
      "energy_efficiency": {
        "estimate": 0.7,
        "lower80": 0.48,
        "upper80": 0.87
      },
      "faradaic_efficiency": {
        "estimate": 0.75,
        "lower80": 0.57,
        "upper80": 0.9
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.5129,
        "lower80": 0.34,
        "upper80": 0.62
      },
      "selective_product_yield": {
        "estimate": 0.1,
        "lower80": 0.018,
        "upper80": 0.22
      },
      "transport_efficiency": {
        "estimate": 0.72,
        "lower80": 0.52,
        "upper80": 0.88
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.57,
        "lower80": 0.5,
        "upper80": 0.64
      },
      "energy_efficiency": {
        "estimate": 0.3,
        "lower80": 0.2,
        "upper80": 0.41
      },
      "faradaic_efficiency": {
        "estimate": 0.39,
        "lower80": 0.31,
        "upper80": 0.47
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.305,
        "lower80": 0.22,
        "upper80": 0.38
      },
      "selective_product_yield": {
        "estimate": 0.035,
        "lower80": 0.008,
        "upper80": 0.072
      },
      "transport_efficiency": {
        "estimate": 0.36,
        "lower80": 0.27,
        "upper80": 0.45
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.86,
        "lower80": 0.74,
        "upper80": 0.95
      },
      "energy_efficiency": {
        "estimate": 0.72,
        "lower80": 0.51,
        "upper80": 0.89
      },
      "faradaic_efficiency": {
        "estimate": 0.86,
        "lower80": 0.7,
        "upper80": 0.96
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.532,
        "lower80": 0.38,
        "upper80": 0.64
      },
      "selective_product_yield": {
        "estimate": 0.1,
        "lower80": 0.02,
        "upper80": 0.22
      },
      "transport_efficiency": {
        "estimate": 0.76,
        "lower80": 0.58,
        "upper80": 0.91
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.59,
        "lower80": 0.54,
        "upper80": 0.64
      },
      "energy_efficiency": {
        "estimate": 0.35,
        "lower80": 0.25,
        "upper80": 0.45
      },
      "faradaic_efficiency": {
        "estimate": 0.42,
        "lower80": 0.35,
        "upper80": 0.49
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.3389,
        "lower80": 0.25,
        "upper80": 0.43
      },
      "selective_product_yield": {
        "estimate": 0.058,
        "lower80": 0.022,
        "upper80": 0.105
      },
      "transport_efficiency": {
        "estimate": 0.43,
        "lower80": 0.35,
        "upper80": 0.51
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.91,
        "lower80": 0.82,
        "upper80": 0.97
      },
      "energy_efficiency": {
        "estimate": 0.88,
        "lower80": 0.71,
        "upper80": 0.98
      },
      "faradaic_efficiency": {
        "estimate": 0.95,
        "lower80": 0.84,
        "upper80": 1.0
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.6394,
        "lower80": 0.44,
        "upper80": 0.74
      },
      "selective_product_yield": {
        "estimate": 0.205,
        "lower80": 0.055,
        "upper80": 0.35
      },
      "transport_efficiency": {
        "estimate": 0.93,
        "lower80": 0.8,
        "upper80": 1.0
      }
    }
  ],
  "rationale": "Predictions interpolate the observed potential-dependent efficiency and selectivity channels, scale low-conversion accumulation approximately with duration and inverse reagent amount at nearly unchanged concentration, and apply material corrections from the E0/E1/E3 and S0/S2 comparisons. The 500 mA cases are predicted close to the 100 mA cases because campaign data indicated sub-proportional current-cap response and probable cell limitation above low caps. Positive-potential long-duration intervals are deliberately wide: only a short positive run was observed, its conversion and efficiencies were high but its yield was clipped at zero. Score estimates apply the published weighted formula and the selective-yield gate, making short-duration score intervals especially asymmetric."
}
```
