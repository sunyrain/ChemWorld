# repeat-03/EC-W03-B12-discovery-E-Aligned

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-03\EC-W03-B12-discovery-E-Aligned\participant\discovery-E-Aligned

## 同期笔记

### v1 · 公开事件 0

# Pre-experimental hypotheses

H1 [tentative] At fixed loading, conversion should rise with delivered charge and absolute overpotential before saturating, while selectivity/energy efficiency may peak at intermediate magnitude because high driving force promotes side reactions. Opposite potential signs may be strongly asymmetric.

H2 [tentative] Transport and ohmic efficiency should improve with conductivity and diffusivity, but the best electrolyte/solvent pairing may trade those gains against pH, precipitation, and potential shifts. Nominally E3 is most conductive but has a thick diffusion layer; E1 has the strongest nominal mass transport; E2 is acidic and resistive.

H3 [tentative] The current setting is only a cap: at low overpotential the realized response may be potential-limited, whereas at stronger drive a low current cap should constrain conversion and possibly improve selectivity.

Planned tests use a common 0.020 mol in 0.040 L loading, compare both signs, durations, current caps, and several solvent/electrolyte combinations. Intermediate UV-vis snapshots will test time/charge trends without advancing chemistry. Final assays remain authoritative. Material rankings will be revised if experiment contradicts the dossier.

### v2 · 公开事件 28

# Updated hypotheses after potential/sign screen

H1 [supported in tested short-time scope] The productive polarity is positive, but the window is bounded. At S0/E1, 100 mA cap, 300 s, +1.0 V produced measurable conversion (~0.015) with high selectivity/efficiencies (event runner-operation-0007). +0.5 V was near zero conversion (runner-operation-0021), while +1.5 V collapsed faradaic efficiency, transport estimate, and selectivity (runner-operation-0028). Thus a threshold followed by a high-drive side-reaction regime is more plausible than monotonic voltage response.

H2 [supported qualitatively] Reversing to -1.0 V greatly reduced efficiency relative to +1.0 V (runner-operation-0014 versus -0007). Conversion/yield channels near zero are at the scale of assay noise, so no quantitative reverse productivity is claimed.

H3 [unresolved] At +1.0 V the observed ~0.015 conversion after 300 s is consistent with a charge-limited ceiling of order 100 mA × 300 s relative to 0.020 mol, but delivered current and electron stoichiometry are unobserved. Longer duration and cap variation should distinguish charge limitation from potential/transport limitation.

Next tests will emphasize +1.0 V, vary current cap and duration, then compare electrolyte profiles and one shifted/less-conductive solvent. A result that remains invariant across duration/cap would reject the simple charge-limited interpretation.

### v3 · 公开事件 84

# Final source-stage hypotheses

H1 [supported in tested domain] Productive response has a positive-potential window rather than monotonic dependence. With S0/E1 and 100 mA for 300 s, +0.5 V was essentially below conversion quantitation, +1.0 V gave ~0.015 conversion with high selectivity, and +1.5 V collapsed faradaic/transport performance and selectivity (events runner-operation-0021, -0007, -0028). Negative polarity was also inefficient (runner-operation-0014). A parsimonious account is an activation threshold near the positive direction followed by competing parasitic electrochemistry at excessive potential.

H2 [supported over tested caps/times] Near +1.0 V, extent is jointly charge/time limited. At 3600 s, raising the current cap 20 → 100 → 400 mA increased conversion about 0.020 → 0.079 → 0.351 while selectivity stayed high (~0.93–0.95; runner-operation-0035, -0056, -0042). This is much larger than the assay conversion uncertainty and approximately proportional over this sparse range. At 100 mA, 60 and 300 s results differ by only ~0.003 and are unresolved against ~0.01 assay uncertainty, but 3600 s is clearly higher (runner-operation-0049, -0007, -0056). The cap is not assumed to equal delivered current; the observations only establish cap-dependent response.

H3 [supported; nominal conductivity alone rejected as ranking rule] Material identity strongly changes the efficiency regime. At +1.0 V, 400 mA, 3600 s in S0, E1 and E2 gave high conversion (~0.351 and ~0.340) and high faradaic/transport efficiencies, whereas E0 and E3 gave only ~0.067–0.085 conversion with faradaic and transport efficiencies around 0.18–0.20 (runner-operation-0042, -0070, -0063, -0077). E3's high nominal conductivity did not confer good transport efficiency, implying that potential shift/interface kinetics or diffusion-layer effects dominate its response under these conditions.

H4 [unresolved mechanistic modifier] Precipitation signal is electrolyte-dependent but is not a simple universal blocker: E0 saturated near 1 with poor performance, E3 and E2 were near zero with respectively poor and good performance, while the best E1 condition retained a high signal near 0.85. It may mark distinct salt equilibria rather than a causal activity loss. S2/E1 lowered ohmic efficiency and selectivity versus S0/E1 while retaining substantial conversion (runner-operation-0084 versus -0042), consistent with solvent control of resistance and interfacial selectivity; one comparison is insufficient to separate its coupled property changes.

Predictive scope: fixed 0.020 mol/0.040 L loading, tested potentials -1.0 to +1.5 V, caps 20–400 mA, durations 60–3600 s, with material comparisons at +1.0 V/400 mA/3600 s. Extrapolation to longer times should allow saturation/depletion and cannot remain linear indefinitely. The most defensible operating recommendation among completed batches is batch 6 (S0/E1, +1.0 V, 400 mA cap, 3600 s): it combines the highest measured selective yield with high selectivity and electrochemical efficiencies, without the high-potential collapse.

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
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 300,
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
    "electrochemical_conversion": 0.015033862553536892,
    "electrochemical_selectivity": 0.9417526721954346,
    "energy_efficiency": 0.9126999974250793,
    "faradaic_efficiency": 0.9275918006896973,
    "ohmic_efficiency": 0.9651356339454651,
    "pH_normalized": 0.20516636967658997,
    "precipitation_signal": 0.851891279220581,
    "safety_risk": 0.072194404900074,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.8988880515098572
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
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -1
    },
    {
      "duration_s": 300,
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
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.6039119362831116,
    "energy_efficiency": 0.2876383662223816,
    "faradaic_efficiency": 0.3670108914375305,
    "ohmic_efficiency": 0.9739734530448914,
    "pH_normalized": 0.2024710327386856,
    "precipitation_signal": 0.854923665523529,
    "safety_risk": 0.072194404900074,
    "score": 0.15917359292507172,
    "selective_product_yield": 0.010674876160919666,
    "transport_efficiency": 0.3932677209377289
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
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 0.5
    },
    {
      "duration_s": 300,
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
    "cost": 0.28266000747680664,
    "electrochemical_conversion": 5.19099849043414e-05,
    "electrochemical_selectivity": 0.8190228343009949,
    "energy_efficiency": 0.7832443118095398,
    "faradaic_efficiency": 0.693453848361969,
    "ohmic_efficiency": 0.9350225925445557,
    "pH_normalized": 0.2031860202550888,
    "precipitation_signal": 0.8373757600784302,
    "safety_risk": 0.072194404900074,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.7100107669830322
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
      "potential_V": 1.5
    },
    {
      "duration_s": 300,
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
    "cost": 0.2827799916267395,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.02824951522052288,
    "ohmic_efficiency": 0.981480062007904,
    "pH_normalized": 0.20249544084072113,
    "precipitation_signal": 0.8381239771842957,
    "safety_risk": 0.072194404900074,
    "score": 0.003243711544200778,
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
    "cost": 0.2828879952430725,
    "electrochemical_conversion": 0.020141130313277245,
    "electrochemical_selectivity": 0.933536171913147,
    "energy_efficiency": 0.8944354057312012,
    "faradaic_efficiency": 0.9057698845863342,
    "ohmic_efficiency": 0.9929190278053284,
    "pH_normalized": 0.20745623111724854,
    "precipitation_signal": 0.837450385093689,
    "safety_risk": 0.072194404900074,
    "score": 0.5610439777374268,
    "selective_product_yield": 0.023940660059452057,
    "transport_efficiency": 0.8952603936195374
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
      "current_mA": 400,
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
    "cost": 0.28835999965667725,
    "electrochemical_conversion": 0.3510061800479889,
    "electrochemical_selectivity": 0.9519597887992859,
    "energy_efficiency": 0.8449041843414307,
    "faradaic_efficiency": 0.9590389728546143,
    "ohmic_efficiency": 0.8970226049423218,
    "pH_normalized": 0.2041803002357483,
    "precipitation_signal": 0.8480806946754456,
    "safety_risk": 0.072194404900074,
    "score": 0.6871981620788574,
    "selective_product_yield": 0.3409530222415924,
    "transport_efficiency": 0.9343556761741638
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
      "electrolyte_profile": 1,
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
    "electrochemical_conversion": 0.011757167056202888,
    "electrochemical_selectivity": 0.9292353987693787,
    "energy_efficiency": 0.9075004458427429,
    "faradaic_efficiency": 0.9052276611328125,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.20319488644599915,
    "precipitation_signal": 0.8331227898597717,
    "safety_risk": 0.072194404900074,
    "score": 0.24026080965995789,
    "selective_product_yield": 0.008599844761192799,
    "transport_efficiency": 0.908627986907959
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
    "cost": 0.28404000401496887,
    "electrochemical_conversion": 0.07922631502151489,
    "electrochemical_selectivity": 0.9259119629859924,
    "energy_efficiency": 0.9028729796409607,
    "faradaic_efficiency": 0.911121666431427,
    "ohmic_efficiency": 0.9910537004470825,
    "pH_normalized": 0.2014974057674408,
    "precipitation_signal": 0.8459956645965576,
    "safety_risk": 0.072194404900074,
    "score": 0.5786117315292358,
    "selective_product_yield": 0.0576326884329319,
    "transport_efficiency": 0.9046263098716736
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
      "current_mA": 400,
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
    "cost": 0.28835999965667725,
    "electrochemical_conversion": 0.06681196391582489,
    "electrochemical_selectivity": 0.8199702501296997,
    "energy_efficiency": 0.2087860107421875,
    "faradaic_efficiency": 0.17550866305828094,
    "ohmic_efficiency": 0.9302269816398621,
    "pH_normalized": 0.22865696251392365,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.29836732149124146,
    "selective_product_yield": 0.07419833540916443,
    "transport_efficiency": 0.1963399350643158
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
      "current_mA": 400,
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
    "cost": 0.28835999965667725,
    "electrochemical_conversion": 0.34026822447776794,
    "electrochemical_selectivity": 0.8940153121948242,
    "energy_efficiency": 0.7795631885528564,
    "faradaic_efficiency": 0.8798033595085144,
    "ohmic_efficiency": 0.8633801341056824,
    "pH_normalized": 0.15082675218582153,
    "precipitation_signal": 0.0,
    "safety_risk": 0.072194404900074,
    "score": 0.632378339767456,
    "selective_product_yield": 0.28184208273887634,
    "transport_efficiency": 0.8811529874801636
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
      "current_mA": 400,
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
    "cost": 0.28835999965667725,
    "electrochemical_conversion": 0.08476588129997253,
    "electrochemical_selectivity": 0.8260488510131836,
    "energy_efficiency": 0.25770121812820435,
    "faradaic_efficiency": 0.19333580136299133,
    "ohmic_efficiency": 0.9138800501823425,
    "pH_normalized": 0.2730598449707031,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.072194404900074,
    "score": 0.305736780166626,
    "selective_product_yield": 0.061118077486753464,
    "transport_efficiency": 0.2005157321691513
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
      "solvent": 2,
      "volume_L": 0.04
    },
    {
      "current_mA": 400,
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
    "cost": 0.3299599885940552,
    "electrochemical_conversion": 0.3155498802661896,
    "electrochemical_selectivity": 0.8642747402191162,
    "energy_efficiency": 0.7202144861221313,
    "faradaic_efficiency": 0.8555840849876404,
    "ohmic_efficiency": 0.8426343202590942,
    "pH_normalized": 0.22419984638690948,
    "precipitation_signal": 0.48111996054649353,
    "safety_risk": 0.1135944053530693,
    "score": 0.6181029677391052,
    "selective_product_yield": 0.30370959639549255,
    "transport_efficiency": 0.8768090605735779
  }
}
```

## K1 封存报告

Mechanistic report

1. Experimental basis and scope

All 12 batches used the same initial loading: 0.020 mol of limiting reagent in 0.040 L total added solvent, corresponding to a nominal initial concentration of 0.50 mol L⁻¹. Each batch received one electrolysis period followed by a final assay. Thus, the strongest conclusions concern this loading, the tested anonymous materials, potentials from −1.0 to +1.5 V, current caps from 20 to 400 mA, and durations from 60 to 3600 s. The electrode geometry and base contact resistance were fixed across the campaign but were not measured.

The final-assay uncertainties were approximately 0.010 for conversion and selective-product yield, 0.012 for selectivity and faradaic/ohmic efficiency, 0.014 for transport efficiency, and 0.016 for energy efficiency. Consequently, near-zero results and differences of only a few hundredths require caution.

2. Proposed process model

I interpret the system as having a productive anodic-like branch at positive potential, competing parasitic electrochemistry at excessive positive drive, and a weak or unproductive branch at negative polarity. A useful conceptual decomposition is:

η = V_applied − V0(E,S) − iRΩ(E,S)

i = min[I_cap, i_kin(η,E,S), i_transport(E,S,X)]

dn_product/dt ≈ FE(η,E,S) × Sel(η,E,S) × i/(νF)

dn_reactant/dt ≈ −i_product/(νF) − r_parasitic

Here E and S denote electrolyte and solvent, V0 is an effective formal-potential term, RΩ is an effective cell resistance, ν is an unknown electron stoichiometry, and i_transport summarizes diffusion-layer, diffusivity, solvation, and interfacial limitations. None of i, V0, RΩ, or ν was directly observed, so these equations describe identifiable relationships rather than fitted physical constants.

The voltage dependence appears windowed rather than monotonic. One possible empirical form is:

productive_factor(η) = sigmoid[a(η−η_on)] × sigmoid[b(η_fail−η)]

The first factor represents activation of productive electron transfer and the second represents loss to side reactions at excessive drive. Faradaic efficiency and selectivity would then decline once parasitic current becomes important. Conversion may be approximated at low extent by a charge-dependent relation, X ≈ α(E,S,V)∫i dt, while a depletion-aware extension would be X = 1−exp[−k_eff(E,S,V,I)t]. The existing data do not distinguish these forms over the full trajectory, and indefinite linear extrapolation would be physically implausible.

3. Potential and polarity dependence

Batches 1–4 formed the central voltage-window explanation. They all used S0/E1, a 100 mA cap, and 300 s:

• Batch 1, +1.0 V: conversion 0.0150, selectivity 0.9418, faradaic efficiency 0.9276, transport efficiency 0.8989, ohmic efficiency 0.9651, and energy efficiency 0.9127.
• Batch 2, −1.0 V: reported conversion 0, selectivity 0.6039, faradaic efficiency 0.3670, transport efficiency 0.3933, and energy efficiency 0.2876.
• Batch 3, +0.5 V: conversion 0.000052, selectivity 0.8190, faradaic efficiency 0.6935, transport efficiency 0.7100, and energy efficiency 0.7832.
• Batch 4, +1.5 V: conversion 0, selectivity 0, faradaic efficiency 0.0282, transport efficiency 0, and energy efficiency 0.

The conversion values in batches 2–4 are at or below measurement uncertainty, so their precise magnitudes are not meaningful. Their efficiency patterns are nevertheless strongly separated. Batch 3 suggests that +0.5 V is below or close to productive onset. Batch 1 establishes productive operation near +1.0 V. Batch 4 shows a severe high-potential failure rather than improved conversion. Batch 2 demonstrates polarity asymmetry. These results changed the initial generic hypothesis of increasing response with absolute overpotential into a directional, bounded productive window.

The high-potential collapse could arise from solvent/electrolyte oxidation, an alternative substrate pathway, electrode passivation, or another parasitic current. The observations cannot identify which microscopic process dominates. Because batch 4 had only a terminal snapshot, transient early production followed by destruction is also a plausible alternative to immediate suppression.

4. Current-cap and duration dependence

Batches 5, 6, and 8 used S0/E1 at +1.0 V for 3600 s while varying the current cap:

• Batch 5, 20 mA: conversion 0.0201, selectivity 0.9335, selective yield 0.0239, faradaic efficiency 0.9058, transport efficiency 0.8953, ohmic efficiency 0.9929, energy efficiency 0.8944.
• Batch 8, 100 mA: conversion 0.0792, selectivity 0.9259, selective yield 0.0576, faradaic efficiency 0.9111, transport efficiency 0.9046, ohmic efficiency 0.9911, energy efficiency 0.9029.
• Batch 6, 400 mA: conversion 0.3510, selectivity 0.9520, selective yield 0.3410, faradaic efficiency 0.9590, transport efficiency 0.9344, ohmic efficiency 0.8970, energy efficiency 0.8449.

The conversion increase from approximately 0.020 to 0.079 to 0.351 is much larger than assay uncertainty and is approximately cap-proportional over this sparse range. Meanwhile, selectivity, faradaic efficiency, and transport efficiency remained high. This supports a charge- or rate-limited regime near +1.0 V rather than a purely potential-limited plateau. The reduction in ohmic and energy efficiency at 400 mA is consistent with increased iR loss or another current-dependent energetic penalty. Importantly, I do not equate the configured cap with the unmeasured delivered current.

Duration was tested at S0/E1, +1.0 V, and 100 mA:

• Batch 7, 60 s: conversion 0.0118 and selective yield 0.0086.
• Batch 1, 300 s: conversion 0.0150 and reported selective yield 0.
• Batch 8, 3600 s: conversion 0.0792 and selective yield 0.0576.

The 60- and 300-s conversion difference is smaller than the conversion uncertainty, so it is not convincing evidence of early-time kinetics. The 3600-s result is clearly higher. This supports cumulative electrolysis, but the data cannot resolve induction time, initial capacitive charging, a linear kinetic segment, or gradual current decay. A time series within one vessel or replicate batches would be needed to distinguish those possibilities.

5. Electrolyte coupling

Batches 6 and 9–11 compared electrolyte profiles under S0, +1.0 V, 400 mA, and 3600 s:

• E1, batch 6: conversion 0.3510, selectivity 0.9520, yield 0.3410, FE 0.9590, transport efficiency 0.9344, energy efficiency 0.8449.
• E2, batch 10: conversion 0.3403, selectivity 0.8940, yield 0.2818, FE 0.8798, transport efficiency 0.8812, energy efficiency 0.7796.
• E0, batch 9: conversion 0.0668, selectivity 0.8200, yield 0.0742, FE 0.1755, transport efficiency 0.1963, energy efficiency 0.2088.
• E3, batch 11: conversion 0.0848, selectivity 0.8260, yield 0.0611, FE 0.1933, transport efficiency 0.2005, energy efficiency 0.2577.

E1 and E2 occupy a high-performance regime, whereas E0 and E3 occupy a low-faradaic, low-transport regime. This rejects nominal bulk conductivity as a sufficient ranking variable: E3 had the highest declared conductivity but performed poorly. The electrolyte’s formal-potential shift, diffusion-layer thickness, diffusivity, acid environment, interfacial residuals, and their solvent coupling are therefore likely more important than conductivity alone.

A plausible explanation is that +1.0 V lies inside the productive effective-overpotential window for E1 and E2 but outside or near an inefficient boundary for E0 and E3. An alternative is that E0/E3 cause strong interfacial or mass-transfer suppression independent of potential alignment. Because each electrolyte was tested at only one potential in this high-current comparison, potential shift and intrinsic electrolyte effects are not separately identifiable.

6. Solvent coupling

Batch 12 changed the solvent from S0 to S2 while retaining E1, +1.0 V, 400 mA, and 3600 s. It produced conversion 0.3155, selectivity 0.8643, selective yield 0.3037, FE 0.8556, transport efficiency 0.8768, ohmic efficiency 0.8426, and energy efficiency 0.7202. Relative to batch 6, conversion remained substantial, but selectivity and all major efficiency measures decreased. This is consistent with S2’s lower nominal conductivity and its shifted electrochemical environment, although relative diffusivity, proton activity, solvation, and hidden interface residuals changed simultaneously. One solvent comparison cannot assign causality to a single property.

Batch 12 also had a higher observed safety-risk metric, 0.1136 versus approximately 0.0722 for the S0 batches. This is an observed operational distinction, not evidence identifying a particular chemical hazard.

7. pH and precipitation

The normalized pH channel varied primarily with electrolyte: approximately 0.151 for E2, 0.205 for E1/S0, 0.229 for E0, and 0.273 for E3. These directions broadly agree with the declared differences in acid concentration and pKa, but the normalized scale cannot be converted into an actual proton concentration without additional calibration.

Precipitation was strongly material-dependent: batch 9 E0 was clipped at 1.0, batch 6 E1/S0 was about 0.848, batch 10 E2 was 0, batch 11 E3 was about 0.005, and batch 12 S2/E1 was about 0.481. However, precipitation is not a simple universal performance blocker. E1/S0 performed best despite a high precipitation signal; E3 performed poorly with almost no signal; and E2 performed well with none. I therefore treat precipitation as a coupled salt-equilibrium marker rather than a demonstrated causal loss mechanism. It could still harm performance within a single material family, but the cross-material evidence is confounded.

8. Measurement consistency and limitations

Selective-product yield should be related conceptually to conversion and selectivity, but the three reported channels should not be forced into an exact algebraic identity. They have independent noise and process proxies. For example, batch 12 reported yield 0.3037 while conversion × selectivity is lower, and batch 1 reported zero yield despite small positive conversion and high selectivity. Near-zero clipping and approximately 0.010 yield uncertainty explain some discrepancies; larger deviations indicate that the synthetic assay channels are not exact deterministic transforms of one another. Conclusions therefore rely on large, repeated directional contrasts rather than exact mass-balance identities.

No experimental condition was replicated. The campaign cannot estimate batch-to-batch process variance, delivered current, electron stoichiometry, electrode kinetics, true formal potentials, current-time profiles, concentration gradients, product degradation rates, or the chemical identity of precipitates and byproducts. Fixed world-specific electrode and material residuals are inseparable from the anonymous material effects. Intermediate UV-visible estimates broadly supported the existence of efficiency changes, but they were noisier than the final assay and did not provide independent species identities.

9. Overall explanatory account

Within the tested domain, the system behaves like a positive-polarity electrochemical conversion with three coupled controls:

(1) A narrow effective-potential window controls whether productive transfer is activated and whether parasitic chemistry dominates. +0.5 V is too weak under S0/E1, +1.0 V is productive, and +1.5 V is destructive or strongly parasitic.

(2) Within the productive window, accumulated current and duration control extent. Raising the current cap greatly increases conversion over 3600 s, with a measurable ohmic/energy penalty at 400 mA but no observed selectivity collapse.

(3) Electrolyte and solvent shift the effective window and determine kinetic, transport, acid-base, precipitation, and resistance terms. E1/S0 provides the best observed combination; E2/S0 is a credible but less selective alternative; E0 and E3 are inefficient at the tested potential despite their nominal property advantages in some dimensions.

The sealed recommendation of batch 6 is therefore mechanistically coherent: S0/E1 at +1.0 V lies in the productive voltage window, and the 400 mA cap with 3600 s supplies much greater extent while retaining high faradaic efficiency and selectivity. This conclusion is an interpolation among completed experiments. It should not be extrapolated to still higher potentials, current caps, concentrations, or durations without allowing for heating, depletion, passivation, and product degradation.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific prior mechanism or quantitative response law was supplied. The supplied material dossier provided nominal properties and explicitly warned that they were incomplete priors subject to hidden, fixed material and interface residuals. My initial laws were therefore self-developed rather than tests of a supplied ground-truth model.

Supported:
• A directional, bounded potential window was supported. For S0/E1 at 100 mA and 300 s, batch 1 at +1.0 V had conversion 0.0150, selectivity 0.9418, and faradaic efficiency 0.9276. Batch 3 at +0.5 V was essentially below conversion resolution, while batch 4 at +1.5 V had near-zero conversion and collapsed selectivity and faradaic efficiency. Batch 2 at −1.0 V was also much less efficient. These observations changed my judgment from a generic response to absolute overpotential into a positive-polarity activation window followed by a high-drive parasitic regime.
• Current-cap dependence within that window was supported. At +1.0 V for 3600 s in S0/E1, conversion rose from 0.0201 in batch 5 at 20 mA to 0.0792 in batch 8 at 100 mA and 0.3510 in batch 6 at 400 mA. Selectivity remained about 0.93–0.95. This supported a charge/rate-limited component rather than a potential-only plateau.
• A duration effect was supported only over the wide interval. At 100 mA and +1.0 V, batch 8 at 3600 s clearly exceeded batches 7 and 1 at 60 and 300 s. The difference between 60 and 300 s was smaller than the conversion uncertainty and was not treated as resolved.
• Strong electrolyte coupling was supported. At +1.0 V, 400 mA, and 3600 s, E1 and E2 in batches 6 and 10 produced conversion near 0.35 with high efficiencies, whereas E0 and E3 in batches 9 and 11 produced only 0.067–0.085 conversion with faradaic and transport efficiencies near 0.18–0.20.
• A current-dependent energetic penalty was supported qualitatively: batch 6 achieved much greater conversion at 400 mA, but its ohmic and energy efficiencies were lower than those in batch 8 at 100 mA.

Contradicted or narrowed:
• A monotonic benefit from increasing potential was contradicted by batch 4. +1.5 V was substantially worse than +1.0 V.
• A response controlled mainly by nominal bulk conductivity was contradicted. E3 had the highest declared conductivity but performed poorly in batch 11. Its large diffusion-layer thickness and low diffusivity-to-thickness ratio were more consistent with the observed weak transport.
• A simple claim that precipitation universally blocks conversion was contradicted by the cross-material pattern. Batch 6 performed best despite a precipitation signal near 0.85; batch 11 performed poorly with a signal near zero; batch 10 performed well with no detected precipitation.
• The idea that configured current could be treated as known delivered current was not supported. Only current caps were controlled, so I narrowed the law to cap-dependent response without asserting an actual current-time trace.

Untested or unresolved:
• The exact kinetic law—linear charge response, exponential depletion, induction, or current decay—remained unidentified.
• Product formation followed by destruction at +1.5 V was not distinguished from immediate suppression by a parasitic current.
• Electron stoichiometry, formal potentials, delivered current, electrode kinetics, and individual ohmic versus interfacial losses were unmeasured.
• Solvent effects were only weakly tested. Batch 12 showed that S2/E1 reduced selectivity and efficiencies relative to S0/E1 in batch 6, but conductivity, potential shift, solvation, proton activity, and hidden residuals all changed together.
• No condition was replicated, so fixed material contrasts were much clearer than batch-to-batch process variability.

2. Most informative additional experiment

I would run one E0/S0 batch at the original 0.020 mol/0.040 L loading, +0.8 V, a 400 mA cap, and 3600 s, followed by the same final assay. This directly contrasts with E0 batch 9 at +1.0 V while keeping its loading, material, cap, and duration fixed.

The leading composite explanation is that E0 has two disadvantages: +1.0 V places it too far into an inefficient effective-potential region because of its material potential shift, and its low diffusivity-to-layer-thickness ratio imposes a persistent transport limitation. The principal alternative is that batch 9 was poor almost entirely because of voltage misalignment, with its low reported transport efficiency being secondary to that operating point rather than intrinsic mass transfer.

Possible outcomes and updates:
• If +0.8 V markedly increased faradaic efficiency and selectivity but transport efficiency remained near batch 9’s approximately 0.20 and conversion improved only moderately, I would strengthen the composite explanation: voltage alignment controls the reaction branch, while E0 remains intrinsically transport-limited.
• If conversion, faradaic efficiency, and transport efficiency all rose close to batch 6’s E1 values, I would favor the voltage-misalignment alternative and retract the claim that E0’s low transport efficiency is largely persistent across potential.
• If +0.8 V produced little or no improvement, I would weaken the inferred E0 potential-window shift and attribute its poor performance mainly to transport, interface kinetics, precipitation, or a hidden material residual.
• If selectivity improved while conversion fell, I would infer that +0.8 V reduces parasitic chemistry but lies below the rate-optimal potential, implying separate optima for selectivity and throughput.

Replicating batch 9 would better estimate variance, but the proposed changed-potential experiment offers more discrimination between the two leading causal explanations.

3. Unused evidence, reliability, and goal effects

The full raw final-assay spectra and characterization artifacts were not analyzed. I relied on calibrated processed metrics and selected public peaks rather than fitting chromatographic or spectroscopic traces. Intermediate UV-visible measurements were collected in all batches and confirmed broad efficiency regimes, but I did not exploit their raw wavelength-dependent structure. Cost was not mechanistically analyzed, and safety-risk evidence was used only to note that batch 12 was higher than the S0 batches. The pH and precipitation channels were used qualitatively, but the campaign did not isolate their causal effects. Nominal capacitance, acid equilibrium, Ksp, and supporting-electrolyte concentration were not independently perturbed, so many supplied descriptors remained confounded.

The least reliable blind predictions are those combining conditions outside the observed design: 7200 s, 500 mA, E0 at +0.8 V, and negative-polarity long-duration operation. The E0 predictions depend particularly strongly on whether its batch-9 failure was caused by potential misalignment, persistent mass transport, or both. Predictions with selective-product yield near the 0.02 multiplicative score gate are also unreliable because small assay fluctuations can produce a discontinuous score change. Negative-polarity yields are near the assay floor, making relative errors large. Predictions for E1 at positive potential are comparatively better anchored by batches 1, 5, 6, 7, and 8.

Batch 6 is reliable as the best completed condition, not as a proven global optimum. It was substantially better than the other assayed batches across yield and most efficiency metrics, but it was not replicated, and the campaign did not finely scan potential around +1.0 V, duration beyond 3600 s, or current between 100 and 400 mA. A neighboring untested condition could therefore be superior.

The assigned goal emphasized explanatory and predictive research, with public score explicitly secondary. That influenced evidence collection: I spent batches on polarity, potential, current, duration, electrolyte, and solvent contrasts instead of repeatedly optimizing or replicating the highest-scoring recipe. This improved mechanistic breadth but reduced precision about process variance and the exact optimum. I found no clear conflict between the scientific goal and safety constraints; all observed risks remained below the stated limit. The main tradeoff was breadth versus replication and local optimization, not a conflict that forced evidence to be ignored.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.38,
        "upper80": 0.7
      },
      "energy_efficiency": {
        "estimate": 0.15,
        "lower80": 0.03,
        "upper80": 0.3
      },
      "faradaic_efficiency": {
        "estimate": 0.22,
        "lower80": 0.09,
        "upper80": 0.37
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.25
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0,
        "upper80": 0.018
      },
      "transport_efficiency": {
        "estimate": 0.2,
        "lower80": 0.08,
        "upper80": 0.34
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.92,
        "lower80": 0.83,
        "upper80": 0.97
      },
      "energy_efficiency": {
        "estimate": 0.42,
        "lower80": 0.27,
        "upper80": 0.57
      },
      "faradaic_efficiency": {
        "estimate": 0.82,
        "lower80": 0.69,
        "upper80": 0.91
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.416,
        "lower80": 0,
        "upper80": 0.5
      },
      "selective_product_yield": {
        "estimate": 0.04,
        "lower80": 0.015,
        "upper80": 0.074
      },
      "transport_efficiency": {
        "estimate": 0.22,
        "lower80": 0.11,
        "upper80": 0.36
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.56,
        "lower80": 0.37,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.16,
        "lower80": 0.03,
        "upper80": 0.32
      },
      "faradaic_efficiency": {
        "estimate": 0.23,
        "lower80": 0.08,
        "upper80": 0.39
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.32
      },
      "selective_product_yield": {
        "estimate": 0.018,
        "lower80": 0,
        "upper80": 0.05
      },
      "transport_efficiency": {
        "estimate": 0.2,
        "lower80": 0.07,
        "upper80": 0.36
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.92,
        "lower80": 0.84,
        "upper80": 0.97
      },
      "energy_efficiency": {
        "estimate": 0.42,
        "lower80": 0.27,
        "upper80": 0.57
      },
      "faradaic_efficiency": {
        "estimate": 0.82,
        "lower80": 0.7,
        "upper80": 0.91
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.498,
        "lower80": 0.38,
        "upper80": 0.6
      },
      "selective_product_yield": {
        "estimate": 0.24,
        "lower80": 0.15,
        "upper80": 0.34
      },
      "transport_efficiency": {
        "estimate": 0.22,
        "lower80": 0.11,
        "upper80": 0.36
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.65,
        "lower80": 0.49,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.38,
        "lower80": 0.22,
        "upper80": 0.54
      },
      "faradaic_efficiency": {
        "estimate": 0.42,
        "lower80": 0.27,
        "upper80": 0.57
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.35,
        "lower80": 0,
        "upper80": 0.46
      },
      "selective_product_yield": {
        "estimate": 0.045,
        "lower80": 0.013,
        "upper80": 0.087
      },
      "transport_efficiency": {
        "estimate": 0.45,
        "lower80": 0.29,
        "upper80": 0.6
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.91,
        "lower80": 0.83,
        "upper80": 0.96
      },
      "energy_efficiency": {
        "estimate": 0.86,
        "lower80": 0.75,
        "upper80": 0.93
      },
      "faradaic_efficiency": {
        "estimate": 0.84,
        "lower80": 0.73,
        "upper80": 0.92
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.598,
        "lower80": 0.5,
        "upper80": 0.69
      },
      "selective_product_yield": {
        "estimate": 0.17,
        "lower80": 0.105,
        "upper80": 0.245
      },
      "transport_efficiency": {
        "estimate": 0.83,
        "lower80": 0.71,
        "upper80": 0.91
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.35,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.13,
        "lower80": 0,
        "upper80": 0.29
      },
      "faradaic_efficiency": {
        "estimate": 0.14,
        "lower80": 0.03,
        "upper80": 0.28
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.28
      },
      "selective_product_yield": {
        "estimate": 0.008,
        "lower80": 0,
        "upper80": 0.029
      },
      "transport_efficiency": {
        "estimate": 0.16,
        "lower80": 0.04,
        "upper80": 0.31
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.8,
        "lower80": 0.67,
        "upper80": 0.89
      },
      "energy_efficiency": {
        "estimate": 0.23,
        "lower80": 0.08,
        "upper80": 0.39
      },
      "faradaic_efficiency": {
        "estimate": 0.18,
        "lower80": 0.06,
        "upper80": 0.32
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.284,
        "lower80": 0,
        "upper80": 0.39
      },
      "selective_product_yield": {
        "estimate": 0.027,
        "lower80": 0.004,
        "upper80": 0.063
      },
      "transport_efficiency": {
        "estimate": 0.19,
        "lower80": 0.06,
        "upper80": 0.34
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.53,
        "lower80": 0.34,
        "upper80": 0.7
      },
      "energy_efficiency": {
        "estimate": 0.13,
        "lower80": 0,
        "upper80": 0.29
      },
      "faradaic_efficiency": {
        "estimate": 0.18,
        "lower80": 0.05,
        "upper80": 0.33
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0,
        "lower80": 0,
        "upper80": 0.29
      },
      "selective_product_yield": {
        "estimate": 0.012,
        "lower80": 0,
        "upper80": 0.041
      },
      "transport_efficiency": {
        "estimate": 0.21,
        "lower80": 0.07,
        "upper80": 0.37
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.84,
        "lower80": 0.73,
        "upper80": 0.92
      },
      "energy_efficiency": {
        "estimate": 0.31,
        "lower80": 0.17,
        "upper80": 0.46
      },
      "faradaic_efficiency": {
        "estimate": 0.6,
        "lower80": 0.44,
        "upper80": 0.73
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.382,
        "lower80": 0.27,
        "upper80": 0.49
      },
      "selective_product_yield": {
        "estimate": 0.11,
        "lower80": 0.061,
        "upper80": 0.169
      },
      "transport_efficiency": {
        "estimate": 0.22,
        "lower80": 0.09,
        "upper80": 0.37
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.5,
        "lower80": 0.31,
        "upper80": 0.67
      },
      "energy_efficiency": {
        "estimate": 0.11,
        "lower80": 0,
        "upper80": 0.28
      },
      "faradaic_efficiency": {
        "estimate": 0.2,
        "lower80": 0.06,
        "upper80": 0.36
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.23,
        "lower80": 0.1,
        "upper80": 0.35
      },
      "selective_product_yield": {
        "estimate": 0.06,
        "lower80": 0.021,
        "upper80": 0.112
      },
      "transport_efficiency": {
        "estimate": 0.18,
        "lower80": 0.04,
        "upper80": 0.34
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.9,
        "lower80": 0.8,
        "upper80": 0.96
      },
      "energy_efficiency": {
        "estimate": 0.36,
        "lower80": 0.2,
        "upper80": 0.52
      },
      "faradaic_efficiency": {
        "estimate": 0.8,
        "lower80": 0.66,
        "upper80": 0.9
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.604,
        "lower80": 0.44,
        "upper80": 0.72
      },
      "selective_product_yield": {
        "estimate": 0.58,
        "lower80": 0.39,
        "upper80": 0.77
      },
      "transport_efficiency": {
        "estimate": 0.18,
        "lower80": 0.06,
        "upper80": 0.33
      }
    }
  ],
  "rationale": "Predictions use the observed positive-polarity operating window, duration/current dependence, and material couplings from the completed campaign. E0 is assigned persistently weak transport because its nominal diffusivity-to-layer-thickness ratio and batch-9 transport result were both low; lowering the potential from 1.0 to 0.8 V is nevertheless expected to improve its faradaic branch by avoiding excessive effective drive. E1 remains the strongest transport medium, while E3 remains transport-limited. Negative-polarity yields are predicted near the assay floor. Intervals include assay noise, lack of replication, extrapolation to 7200 s and 500 mA, uncertainty in delivered current and saturation, and the score's selective-yield gate."
}
```
