# repeat-02/EC-W01-B12-discovery-E-MisIndexed

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-02\EC-W01-B12-discovery-E-MisIndexed\participant\discovery-E-MisIndexed

## 同期笔记

### v1 · 公开事件 0

# Pre-experiment hypotheses

H1 [tentative] Product formation has a preferred potential sign and an intermediate magnitude: conversion should increase with delivered charge/time, while excessive magnitude or duration may reduce selectivity and energy efficiency.

H2 [tentative] Transport and ohmic efficiency should improve with nominal conductivity and diffusivity, but selectivity may instead track solvent proton activity and electrolyte potential shift; thus material rankings may interact with applied potential.

H3 [tentative] A current cap matters only when below potential-driven demand; raising an already nonbinding cap should have little effect. At binding caps, conversion should approximately track cap × time before substrate depletion.

Initial test plan: use a fixed loading (0.020 mol in 0.050 L) and span both potential signs, durations, current caps, solvents, and electrolytes. Use intermediate UV–vis or pH measurements to distinguish transport/charge effects and acidity/precipitation from final product outcomes. These expectations will be revised only after observations.

### v2 · 公开事件 35

# Working hypotheses after batches 1–5

H1 [supported in tested S0/E0 scope] Product formation prefers positive potential near +1 V and accumulates with electrolysis time. At +1 V, extending 600 to 3600 s increased final conversion from 0.018 to 0.062 and selective yield from a clipped/near-zero value to 0.064 (events runner-operation-0007, runner-operation-0035). The -1 V control gave essentially no conversion and only a small noisy yield estimate (runner-operation-0014).

H1b [supported qualitatively] Excess positive overpotential is harmful: +1.5 V for 3600 s collapsed conversion, selectivity, transport, and energy metrics relative to +1 V (runner-operation-0028 versus runner-operation-0035). This favors a potential window rather than monotonic voltage response.

H2 [unresolved] UV–vis efficiency estimates broadly anticipate final efficiency but differ enough that they should not substitute for the assay. Precipitation is near saturation in all S0/E0 tests, so material comparisons are needed to separate precipitation from electrochemical loss.

H3 [untested] Current-cap binding remains unknown. Next tests will map time/current near +1 V, then compare material combinations. A long +1 V run at low cap should show less conversion if the cap binds; similar conversion would imply a nonbinding cap.

### v3 · 公开事件 84

# Final working account after 12 batches

H1 [supported within studied loading] At 0.020 mol in 0.050 L, useful target formation requires positive polarization near +1 V. The -1 V control and short positive runs produced negligible conversion/yield, whereas +1 V for 3600–7200 s produced increasing conversion and yield (runner-operation-0014, runner-operation-0035, runner-operation-0042). +1.5 V for 3600 s and +1 V with a 500 mA cap for 7200 s collapsed faradaic/transport performance and product formation (runner-operation-0028, runner-operation-0056), consistent with a bounded operating window and parasitic-current/degradation branch.

H2 [supported, nonlinear current-cap effect] At +1 V/S0/E0/7200 s, lowering the cap from 100 to 10 mA reduced conversion about fourfold while raising faradaic and energy efficiencies; raising it to 500 mA destroyed useful conversion. Thus cap × time is informative only in a low-current regime; current density also changes selectivity/side-reaction partitioning (runner-operation-0042, runner-operation-0049, runner-operation-0056). The actual delivered-current law remains unobserved, so no strict charge-normalized kinetic coefficient is claimed.

H3 [supported material dependence; attribution partly unresolved] At +1 V, 100 mA, 7200 s, S1/E1 and S1/E0 gave the strongest combined yield and efficiency (runner-operation-0063, runner-operation-0084), outperforming S0/E0, S2/E2, and S3/E3 (runner-operation-0042, runner-operation-0070, runner-operation-0077). The S1/E0 cross nearly matches S1/E1, suggesting S1 drives much of the gain, while E1 may reduce precipitation (0.73 versus ~0.99) and shift acidity. Because only one cross was run and estimates have declared noise, electrolyte main effects and solvent–electrolyte interactions remain unresolved.

Predictive working form: target yield ≈ conversion × selectivity plus assay/process scatter; conversion rises roughly with time near +1 V before depletion, multiplied by a material/transport factor and a bell-shaped current/potential efficiency term. Efficiency is highest at modest current, while throughput is higher at an intermediate cap. Outside the window (negative sign, +1.5 V here, or 500 mA cap here), parasitic pathways dominate.

Decision: recommend batch 12 (S1/E0, +1 V, 100 mA cap, 7200 s) as the best observed balanced point. Its score advantage over batch 9 is numerically small and not evidence of superiority; I choose it for slightly higher observed yield/selectivity/energy efficiency. More replication and crossed materials would change this decision if batch 9 proves more reproducible or precipitation becomes operationally decisive.

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
    "cost": 0.28512001037597656,
    "electrochemical_conversion": 0.004502770025283098,
    "electrochemical_selectivity": 0.8499323129653931,
    "energy_efficiency": 0.8201635479927063,
    "faradaic_efficiency": 0.6191908717155457,
    "ohmic_efficiency": 0.9438269734382629,
    "pH_normalized": 0.23020939528942108,
    "precipitation_signal": 0.9868234395980835,
    "safety_risk": 0.05933958664536476,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.6357477903366089
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
      "potential_V": 1.5
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
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.02824951522052288,
    "ohmic_efficiency": 0.9844148755073547,
    "pH_normalized": 0.2295188158750534,
    "precipitation_signal": 0.987571656703949,
    "safety_risk": 0.05933958664536476,
    "score": 0.0032529826276004314,
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
    "electrochemical_conversion": 0.062289755791425705,
    "electrochemical_selectivity": 0.9456571340560913,
    "energy_efficiency": 0.5920684337615967,
    "faradaic_efficiency": 0.6418315768241882,
    "ohmic_efficiency": 0.97674161195755,
    "pH_normalized": 0.2344796061515808,
    "precipitation_signal": 0.9868980646133423,
    "safety_risk": 0.05933958664536476,
    "score": 0.4742980897426605,
    "selective_product_yield": 0.06372986733913422,
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
      "current_mA": 100,
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
    "cost": 0.287880003452301,
    "electrochemical_conversion": 0.11637037992477417,
    "electrochemical_selectivity": 0.9434638023376465,
    "energy_efficiency": 0.5964290499687195,
    "faradaic_efficiency": 0.6363047361373901,
    "ohmic_efficiency": 0.9785983562469482,
    "pH_normalized": 0.23120366036891937,
    "precipitation_signal": 0.9975283145904541,
    "safety_risk": 0.05933958664536476,
    "score": 0.49371182918548584,
    "selective_product_yield": 0.1176142767071724,
    "transport_efficiency": 0.6116213798522949
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
      "current_mA": 10,
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
    "cost": 0.285288006067276,
    "electrochemical_conversion": 0.027417324483394623,
    "electrochemical_selectivity": 0.9370536208152771,
    "energy_efficiency": 0.8990198969841003,
    "faradaic_efficiency": 0.9168441295623779,
    "ohmic_efficiency": 1.0,
    "pH_normalized": 0.23021826148033142,
    "precipitation_signal": 0.982570469379425,
    "safety_risk": 0.05933958664536476,
    "score": 0.5671942830085754,
    "selective_product_yield": 0.023319173604249954,
    "transport_efficiency": 0.9202445149421692
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
    "cost": 0.2994000017642975,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.008051441982388496,
    "ohmic_efficiency": 0.9101666212081909,
    "pH_normalized": 0.22852078080177307,
    "precipitation_signal": 0.9954432845115662,
    "safety_risk": 0.05933958664536476,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.0015560885658487678
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
      "electrolyte_profile": 1,
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
    "cost": 0.3078800141811371,
    "electrochemical_conversion": 0.1540023386478424,
    "electrochemical_selectivity": 0.9004208445549011,
    "energy_efficiency": 0.909344494342804,
    "faradaic_efficiency": 0.8270372748374939,
    "ohmic_efficiency": 0.994864821434021,
    "pH_normalized": 0.20395824313163757,
    "precipitation_signal": 0.7300134301185608,
    "safety_risk": 0.08273958414793015,
    "score": 0.5981954336166382,
    "selective_product_yield": 0.1590329110622406,
    "transport_efficiency": 0.8478685617446899
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
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 2,
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
    "cost": 0.33987998962402344,
    "electrochemical_conversion": 0.1449209302663803,
    "electrochemical_selectivity": 0.746811032295227,
    "energy_efficiency": 0.7026745080947876,
    "faradaic_efficiency": 0.7034595012664795,
    "ohmic_efficiency": 0.9345540404319763,
    "pH_normalized": 0.16594988107681274,
    "precipitation_signal": 0.0,
    "safety_risk": 0.10073958337306976,
    "score": 0.4891292154788971,
    "selective_product_yield": 0.09184640645980835,
    "transport_efficiency": 0.7048090696334839
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
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 3,
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
    "cost": 0.31988000869750977,
    "electrochemical_conversion": 0.08510129898786545,
    "electrochemical_selectivity": 0.8616297841072083,
    "energy_efficiency": 0.5959312319755554,
    "faradaic_efficiency": 0.38626500964164734,
    "ohmic_efficiency": 0.9814802408218384,
    "pH_normalized": 0.28423500061035156,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.11333958804607391,
    "score": 0.41054320335388184,
    "selective_product_yield": 0.06394737958908081,
    "transport_efficiency": 0.3934449553489685
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
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1
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
    "cost": 0.3008800148963928,
    "electrochemical_conversion": 0.1415846347808838,
    "electrochemical_selectivity": 0.938556969165802,
    "energy_efficiency": 0.9204410910606384,
    "faradaic_efficiency": 0.8127752542495728,
    "ohmic_efficiency": 0.9878636598587036,
    "pH_normalized": 0.23370085656642914,
    "precipitation_signal": 0.9891219139099121,
    "safety_risk": 0.08273958414793015,
    "score": 0.6015936732292175,
    "selective_product_yield": 0.16207782924175262,
    "transport_efficiency": 0.8340002298355103
  }
}
```

## K1 封存报告

Mechanistic report

1. Empirical scope

All 12 batches used 0.020 mol of limiting reagent in 0.050 L of solvent, corresponding to a nominal initial loading of 0.40 mol L⁻¹. Consequently, the campaign identifies effects of potential, current limit, electrolysis time, solvent and electrolyte only at this one loading and volume. It does not establish concentration or scale-up laws.

The strongest observed balanced conditions were batch 12: solvent S1, electrolyte E0, +1.0 V, 100 mA current limit and 7200 s. Its final assay gave selective-product yield 0.1621, conversion 0.1416, selectivity 0.9386, faradaic efficiency 0.8128, transport efficiency 0.8340, ohmic efficiency 0.9879, energy efficiency 0.9204 and score 0.6016. Batch 9, S1/E1 under the same electrical conditions, was nearly equivalent: yield 0.1590 and score 0.5982. That difference is too small to establish that batch 12 is intrinsically superior.

2. Proposed process structure

I interpret the system as a potential-driven conversion with three competing current destinations:

• desired electron transfer to the target product;
• nonproductive electrochemical reactions, which increase outside a favorable potential/current window;
• transport, interfacial or precipitation-related losses that limit how much configured current reaches productive chemistry.

A useful conceptual decomposition is

Iproductive = Idelivered × FE,
rate(target) ∝ Iproductive × selectivity,

where Idelivered is not observed and need not equal the configured current limit. A more explicit but still provisional model is

Idelivered = min(Icap, Ikinetic(η, materials), Itransport(materials, concentration)),

dX/dt = k0 · Fpotential(η) · Fcurrent(Icap, η) · Ftransport · (1 − X),

Ytarget ≈ X · S + process/assay error.

Here X is conversion, S is electrochemical selectivity, and η is an effective overpotential. A plausible expression is

η = Vapplied − Eeffective(solvent, electrolyte, pH) − IdeliveredRcell,

with additional interfacial terms. The material dossier supplies nominal solvent and electrolyte potential shifts, conductivity, diffusivity, double-layer capacitance, proton activity and precipitation properties, so those terms are mechanistically plausible. However, neither Eeffective nor the sign and magnitude with which each nominal shift enters the actual response was independently identified.

At low conversion and within the favorable window, the batch 1/5/6 S0/E0 data are approximately compatible with a linear-in-time regime. A least-squares line through conversion at 600, 3600 and 7200 s gives X ≈ 0.00896 + 1.49×10⁻⁵t, with t in seconds. This is only a local empirical summary of three unreplicated points, not a general kinetic constant. A saturating law such as X = 1 − exp(−kefft) is more plausible for longer times.

3. Potential dependence

Batches 1–4 established that productive response is not monotonic in applied voltage.

• Batch 1, S0/E0 at +1.0 V, 100 mA and 600 s, gave conversion 0.0181 and selectivity 0.9496, although selective yield was reported as zero.
• Batch 2 changed only the sign to −1.0 V. Conversion was clipped at zero, selectivity fell to 0.6260, faradaic efficiency to 0.3932 and energy efficiency to 0.2403. Its small yield estimate of 0.0127 despite zero reported conversion is most reasonably treated as assay/process noise or a difference between independently processed channels, not evidence for efficient negative-potential synthesis.
• Batch 3 at +0.5 V and 600 s produced only 0.0045 conversion and zero reported yield.
• Batch 4 at +1.5 V and 3600 s collapsed to zero reported conversion and selectivity, with faradaic efficiency 0.0282, transport efficiency zero and yield 0.00079.

Thus the data favor a bounded positive-potential window near +1 V. Below it, activation is weak; above it, nonproductive reactions, passivation, controller saturation or another interfacial failure dominates. Batch 4 changed my initial monotonic-voltage expectation into a peaked-window explanation.

The exact optimum is not known: only +0.5, +1.0 and +1.5 V were sampled, and duration was not identical at +1.5 V. The apparent failure at +1.5 V could alternatively arise from the combination of higher potential and longer exposure rather than voltage alone.

4. Time dependence near +1 V

For S0/E0 at +1.0 V and a 100 mA limit:

• batch 1, 600 s: conversion 0.0181, yield 0;
• batch 5, 3600 s: conversion 0.0623, yield 0.0637;
• batch 6, 7200 s: conversion 0.1164, yield 0.1176.

Conversion and yield therefore rose approximately with time over 3600–7200 s, while selectivity remained high at 0.9457 and 0.9435. Faradaic efficiency was also fairly stable, 0.6418 and 0.6363. This supports accumulation of target product in a locally near-linear, low-conversion regime rather than rapid equilibrium.

No experiment tested times beyond 7200 s at the useful 100 mA condition. Substrate depletion, product degradation, electrode passivation or precipitation could cause saturation or reversal later, so linear extrapolation to 14400 s or beyond is unjustified.

5. Current-limit coupling and the throughput–efficiency tradeoff

Batches 6–8 held S0/E0, +1.0 V and 7200 s constant while changing the configured current limit:

• 10 mA, batch 7: conversion 0.0274, yield 0.0233, FE 0.9168, transport efficiency 0.9202, energy efficiency 0.8990 and score 0.5672.
• 100 mA, batch 6: conversion 0.1164, yield 0.1176, FE 0.6363, transport efficiency 0.6116, energy efficiency 0.5964 and score 0.4937.
• 500 mA, batch 8: zero conversion, selectivity and yield, FE 0.0081, transport efficiency 0.0016 and energy efficiency zero.

This is not a simple rule in which more allowed charge always gives more product. Raising the limit from 10 to 100 mA increased throughput about fourfold but reduced faradaic, transport and energy efficiencies. Raising it to 500 mA destroyed productive behavior. Ohmic efficiency remained comparatively high—1.000, 0.9786 and 0.9102—so a purely bulk-resistance explanation is inadequate.

I infer that low current stays within a selective, transport-supported regime, whereas intermediate current increases productive flux at the price of more losses. Very high current enters a strongly parasitic or transport-starved regime. Possible physical causes include concentration polarization, interfacial depletion, gas evolution, electrode fouling, local pH excursions or product degradation. The observations do not distinguish these alternatives.

Because only current limits were configured, actual current and total charge are unmeasured. Products such as Icap×time are upper bounds rather than delivered charge, and no electron stoichiometry or true faradaic material balance can be reconstructed.

6. Solvent and electrolyte effects

Batches 6 and 9–12 compared materials at +1.0 V, 100 mA and 7200 s:

• S0/E0, batch 6: conversion 0.1164, selectivity 0.9435, yield 0.1176, FE 0.6363, transport 0.6116, energy 0.5964, precipitation signal 0.9975, score 0.4937.
• S1/E1, batch 9: conversion 0.1540, selectivity 0.9004, yield 0.1590, FE 0.8270, transport 0.8479, energy 0.9093, precipitation 0.7300, score 0.5982.
• S2/E2, batch 10: conversion 0.1449, selectivity 0.7468, yield 0.0918, FE 0.7035, transport 0.7048, energy 0.7027, precipitation zero, score 0.4891.
• S3/E3, batch 11: conversion 0.0851, selectivity 0.8616, yield 0.0639, FE 0.3863, transport 0.3934, energy 0.5959, precipitation 0.0052, score 0.4105.
• S1/E0, batch 12: conversion 0.1416, selectivity 0.9386, yield 0.1621, FE 0.8128, transport 0.8340, energy 0.9204, precipitation 0.9891, score 0.6016.

The S1/E0 cross is especially informative. Relative to S0/E0, changing only the solvent to S1 raised conversion, yield, faradaic efficiency, transport efficiency and energy efficiency while leaving selectivity broadly similar. This suggests that S1 supplies much of the advantage seen in S1/E1. Its greater nominal relative diffusivity is consistent with improved transport, although its lower nominal conductivity means the response cannot be reduced to conductivity alone. Solvation, double-layer structure, proton activity and fixed hidden residuals are plausible contributors.

Comparing S1/E0 with S1/E1 suggests that E1 may modestly increase conversion and reduce precipitation, while E0 may preserve higher selectivity. However, these are single noisy observations. There was no S0/E1 batch, so an electrolyte main effect cannot be separated cleanly from solvent–electrolyte interaction.

The paired S2/E2 and S3/E3 batches show that suppressing the precipitation signal is not sufficient for high target yield. Both had almost no reported precipitation, yet their yields and efficiencies were below those of the S1 formulations. Conversely, S1/E0 had precipitation near one and still produced the highest observed yield. Precipitation may therefore be a parallel equilibrium or passivation risk rather than a direct proxy for target formation.

7. Acidity and precipitation

Final normalized pH varied systematically across paired materials: approximately 0.166 for S2/E2, 0.204 for S1/E1, 0.231–0.234 for E0-containing batches and 0.284 for S3/E3. This broadly follows the nominal acid profiles and supports a genuine acid/base coupling.

The batch 12 intermediate pH-meter result, pH_normalized 0.2340 and precipitation 0.9625, agreed closely with its final-assay values of 0.2337 and 0.9891. This indicates that those state variables were already present before termination and were not created by the final assay.

A possible coupled process is

acid/base state → interfacial kinetics and effective potential,
acid/base state + salt/solvent → precipitation,
precipitation → available area or mass transport.

But precipitation did not map monotonically to performance. It may affect longevity or reproducibility more strongly than a single 7200 s endpoint, or the reported signal may describe a species that is not the principal passivating phase.

8. Instrument evidence

Intermediate UV–visible measurements generally identified the same operating regimes as the final assay. For example, batch 8 already showed near-zero faradaic and transport performance before termination, while batch 9 showed high efficiencies. Exact UV–visible and final-assay values differed, as expected from their declared noise models and independent calibration channels. I therefore use UV–visible data as corroborative state evidence, not as an interchangeable measure of final yield or conversion.

The occasional inconsistency between conversion and selective yield—notably batches 1 and 2, and yields slightly greater than conversion in several productive batches—shows that the processed channels are noisy or not constrained by an exact algebraic identity. The conceptual Y ≈ X·S relation should therefore include channel-specific calibration and process noise rather than be enforced exactly.

9. Safety and cost coupling

All observed safety risks were below the 0.65 limit. At the fixed loading, risk was mainly formulation-dependent: about 0.0593 for S0, 0.0827 for S1, 0.1007 for S2 and 0.1133 for S3. The visible risk did not rise appreciably with electrolysis time or potential in the tested batches. This could mean the benchmark risk model is dominated by charged material inventory, not that extreme electrical conditions are intrinsically harmless.

S1 improved electrochemical performance at a modestly higher risk and cost than S0. The balanced recommendation therefore reflects a tradeoff rather than a universal maximum-yield rule.

10. What changed the explanation

Batches 1–3 established polarity and activation: positive potential was necessary, while −1 V and +0.5 V were weak. Batch 4 rejected a monotonic voltage model by showing catastrophic performance at +1.5 V. Batches 5 and 6 established time accumulation near +1 V. Batches 7 and 8 rejected the idea that the current setting was merely a harmless upper bound: it controlled both rate and efficiency and exposed a catastrophic high-current regime. Batches 9–11 revealed substantial material effects, and batch 12 was the key partial cross showing that S1 itself accounts for much of the improved transport and faradaic behavior.

11. Unidentifiable quantities and limitations

The campaign cannot identify actual current, total delivered charge, electron stoichiometry, electrode area, electrode gap, cell resistance, mass-transfer coefficients, intrinsic rate constants, exchange current, standard potential, individual side products or degradation products. Electrode geometry and base resistance were fixed across the world but undisclosed. Hidden correlated material residuals may be as important as nominal dossier properties.

There were no true replicates. Most factor changes were one-at-a-time only in the electrical series, while material tests were largely paired combinations. Potential and duration were confounded in the +1.5 V comparison. Current–potential interactions, full solvent-by-electrolyte interactions, concentration effects and long-time saturation remain unidentified. Reported zeros may be clipping or below-detection outcomes rather than exact physical zeros.

12. Plausible alternative accounts

The high-current and high-potential failures could arise from chemical side reactions, electrode passivation, controller behavior, local heating or transport depletion; the available channels do not select uniquely among them. Material effects attributed to S1 diffusivity could instead result from hidden solvation/interface residuals. The precipitation signal could represent an innocuous parallel phase rather than the cause of transport loss. Finally, independent assay noise can explain some apparent violations of yield–conversion consistency.

Within these limitations, the most defensible predictive account is a positive-potential, low-conversion electrolysis with a narrow productive overpotential/current window, approximately time-proportional accumulation over 3600–7200 s, a strong throughput–efficiency tradeoff with current limit, and substantial solvent-controlled transport/interfacial coupling. S1 with E0 or E1 at +1 V and an intermediate current limit is the supported regime; behavior outside the tested loading, time range and material combinations is extrapolative.

## K2 封存报告

1. Claims and laws

No instance-specific prior or prescribed response law was supplied. The material dossier provided nominal properties and explicitly warned that hidden residuals and coupling could alter them; I treated those as qualitative priors, not ground truth.

• Supported: my pre-experiment claim that target formation would have a preferred potential sign and an intermediate magnitude. Batch 2 at −1.0 V had zero reported conversion and poor efficiency, while batches 5–6 at +1.0 V produced appreciable conversion and yield. Batch 4 at +1.5 V collapsed, contradicting any monotonic voltage-benefit law and changing my judgment to a bounded positive-potential window.

• Supported locally: conversion near +1.0 V rises with time before obvious depletion. For S0/E0 at 100 mA, batches 1, 5 and 6 increased from 0.018 to 0.062 to 0.116 conversion at 600, 3600 and 7200 s. This relationship remains untested beyond 7200 s and outside the single loading.

• Partly supported but substantially revised: I initially proposed that a current cap would matter mainly when binding and that conversion might then scale with cap × time. Batch 7 showed the expected lower throughput at 10 mA, but batch 8 at 500 mA gave essentially zero conversion, faradaic efficiency and transport efficiency. That evidence contradicted a simple charge-throughput law and led to the current-window/parasitic-pathway explanation.

• Partly supported: nominal transport properties matter, but no simple conductivity ranking works. Batch 12 showed that changing S0 to S1 with E0 improved conversion, yield, faradaic efficiency and transport efficiency relative to batch 6, consistent with a solvent-mediated transport or interface effect. However, S1 has lower nominal conductivity than S0, so conductivity alone was contradicted as the controlling descriptor.

• Supported only provisionally: solvent S1 appears to provide much of the improvement in the strong S1/E1 result. Batch 12, S1/E0, nearly matched batch 9, S1/E1, while outperforming batch 6, S0/E0. This inference rests on one cross and lacks replication.

• Contradicted as a simple causal law: less precipitation does not automatically imply better product formation. Batches 10 and 11 had near-zero precipitation signals but weaker yield than precipitation-rich batch 12.

• Untested: concentration dependence, delivered-current and charge laws, behavior beyond 7200 s at useful settings, full solvent-by-electrolyte interactions, electrode passivation itself, product degradation, and whether the observed time trend eventually saturates or reverses.

2. One discriminating experiment

I would run S0/E0 at the original 0.020 mol in 0.050 L, +1.0 V and a 500 mA cap for 1440 s, followed by UV–visible characterization and the final assay. Its configured cap×time equals that of batch 6 at 100 mA for 7200 s.

This would contrast my leading explanation—an instantaneous high-current regime causes transport failure, parasitic chemistry or passivation—with the alternative that batch 8 failed mainly because its long run delivered excessive cumulative charge or exposure.

• If the short 500 mA batch still had near-zero faradaic efficiency, transport efficiency and yield, it would strongly support a current-density-specific failure and reject nominal charge equivalence.

• If it approached batch 6 in conversion and yield, the cumulative-charge/exposure alternative would gain support, and I would weaken the claim that 500 mA is intrinsically pathological.

• If it gave high early conversion but poorer selectivity or efficiency than batch 6, I would adopt a mixed model: high current accelerates conversion while simultaneously increasing parasitic branching, with the complete collapse in batch 8 requiring prolonged exposure.

Because actual current is unmeasured, even this experiment would test configured-current behavior rather than prove equal delivered charge.

3. Unused evidence, reliability and goal effects

I did not inspect or model the raw UV–visible spectra, individual replicate signals, spectral assignments, final-assay raw packets or mass-balance fields. I relied on processed estimates. Most nominal dossier variables—double-layer capacitance, Ksp, diffusion-layer thickness and supporting-electrolyte concentration—were not quantitatively fitted. Cost was recorded but not used mechanistically, and pH received only one dedicated intermediate measurement, in batch 12. The campaign also lacked true replicate batches.

The least reliable blind predictions are those for the 500 mA cases, Q11–Q12, because only one high-current batch was observed and it was at +1.0 V. Predictions for the untested S0/E1, S0/E3 and S2/E0 combinations are also weak because solvent and electrolyte main effects are incompletely separated. All predictions extrapolate from 0.40 M and 0.050 L to 0.48 M and 0.025 L. The negative-potential long-duration predictions and short-run scores near the 0.02 yield gate are especially uncertain.

The recommendation distinguishing batch 12 from batch 9 is not robust: their scores, 0.6016 and 0.5982, differ by much less than the combined experimental uncertainty. Likewise, the claim that S1 is the dominant material factor is less reliable than the direct observation that the two S1 formulations performed well.

The assigned mechanism-discovery goal affected collection by favoring broad contrasts—polarity, potential, time, current and several materials—over replication or narrow score optimization. That improved qualitative discrimination but left effect sizes and interactions uncertain. I see no clear conflict with the goal: the broad design was useful for explanation, although a purely optimization-focused campaign would likely have replicated batches 9 and 12 and refined their neighborhood instead.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.68,
        "lower80": 0.48,
        "upper80": 0.82
      },
      "energy_efficiency": {
        "estimate": 0.31,
        "lower80": 0.17,
        "upper80": 0.45
      },
      "faradaic_efficiency": {
        "estimate": 0.44,
        "lower80": 0.31,
        "upper80": 0.56
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.098,
        "lower80": 0.0,
        "upper80": 0.25
      },
      "selective_product_yield": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.022
      },
      "transport_efficiency": {
        "estimate": 0.46,
        "lower80": 0.32,
        "upper80": 0.59
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.92,
        "lower80": 0.82,
        "upper80": 0.99
      },
      "energy_efficiency": {
        "estimate": 0.75,
        "lower80": 0.61,
        "upper80": 0.88
      },
      "faradaic_efficiency": {
        "estimate": 0.68,
        "lower80": 0.57,
        "upper80": 0.77
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.337,
        "lower80": 0.0,
        "upper80": 0.5
      },
      "selective_product_yield": {
        "estimate": 0.014,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "transport_efficiency": {
        "estimate": 0.66,
        "lower80": 0.54,
        "upper80": 0.76
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.35,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.24,
        "lower80": 0.08,
        "upper80": 0.39
      },
      "faradaic_efficiency": {
        "estimate": 0.38,
        "lower80": 0.22,
        "upper80": 0.53
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.118,
        "lower80": 0.0,
        "upper80": 0.3
      },
      "selective_product_yield": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.03
      },
      "transport_efficiency": {
        "estimate": 0.41,
        "lower80": 0.25,
        "upper80": 0.56
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.94,
        "lower80": 0.86,
        "upper80": 0.99
      },
      "energy_efficiency": {
        "estimate": 0.73,
        "lower80": 0.58,
        "upper80": 0.86
      },
      "faradaic_efficiency": {
        "estimate": 0.68,
        "lower80": 0.55,
        "upper80": 0.79
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.533,
        "lower80": 0.46,
        "upper80": 0.62
      },
      "selective_product_yield": {
        "estimate": 0.14,
        "lower80": 0.08,
        "upper80": 0.22
      },
      "transport_efficiency": {
        "estimate": 0.66,
        "lower80": 0.52,
        "upper80": 0.78
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.3,
        "upper80": 0.77
      },
      "energy_efficiency": {
        "estimate": 0.35,
        "lower80": 0.15,
        "upper80": 0.55
      },
      "faradaic_efficiency": {
        "estimate": 0.48,
        "lower80": 0.28,
        "upper80": 0.66
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.132,
        "lower80": 0.0,
        "upper80": 0.34
      },
      "selective_product_yield": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.032
      },
      "transport_efficiency": {
        "estimate": 0.53,
        "lower80": 0.32,
        "upper80": 0.7
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.9,
        "lower80": 0.76,
        "upper80": 0.98
      },
      "energy_efficiency": {
        "estimate": 0.78,
        "lower80": 0.58,
        "upper80": 0.92
      },
      "faradaic_efficiency": {
        "estimate": 0.72,
        "lower80": 0.52,
        "upper80": 0.86
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.544,
        "lower80": 0.4,
        "upper80": 0.66
      },
      "selective_product_yield": {
        "estimate": 0.135,
        "lower80": 0.06,
        "upper80": 0.23
      },
      "transport_efficiency": {
        "estimate": 0.72,
        "lower80": 0.51,
        "upper80": 0.87
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.48,
        "lower80": 0.2,
        "upper80": 0.7
      },
      "energy_efficiency": {
        "estimate": 0.18,
        "lower80": 0.03,
        "upper80": 0.38
      },
      "faradaic_efficiency": {
        "estimate": 0.28,
        "lower80": 0.12,
        "upper80": 0.48
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.061,
        "lower80": 0.0,
        "upper80": 0.24
      },
      "selective_product_yield": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.025
      },
      "transport_efficiency": {
        "estimate": 0.32,
        "lower80": 0.14,
        "upper80": 0.52
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.84,
        "lower80": 0.65,
        "upper80": 0.96
      },
      "energy_efficiency": {
        "estimate": 0.6,
        "lower80": 0.38,
        "upper80": 0.79
      },
      "faradaic_efficiency": {
        "estimate": 0.43,
        "lower80": 0.25,
        "upper80": 0.63
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.42,
        "lower80": 0.28,
        "upper80": 0.55
      },
      "selective_product_yield": {
        "estimate": 0.07,
        "lower80": 0.02,
        "upper80": 0.15
      },
      "transport_efficiency": {
        "estimate": 0.44,
        "lower80": 0.25,
        "upper80": 0.64
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.3,
        "upper80": 0.77
      },
      "energy_efficiency": {
        "estimate": 0.27,
        "lower80": 0.08,
        "upper80": 0.48
      },
      "faradaic_efficiency": {
        "estimate": 0.36,
        "lower80": 0.18,
        "upper80": 0.56
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.101,
        "lower80": 0.0,
        "upper80": 0.3
      },
      "selective_product_yield": {
        "estimate": 0.007,
        "lower80": 0.0,
        "upper80": 0.03
      },
      "transport_efficiency": {
        "estimate": 0.39,
        "lower80": 0.2,
        "upper80": 0.59
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.86,
        "lower80": 0.68,
        "upper80": 0.97
      },
      "energy_efficiency": {
        "estimate": 0.68,
        "lower80": 0.47,
        "upper80": 0.84
      },
      "faradaic_efficiency": {
        "estimate": 0.58,
        "lower80": 0.39,
        "upper80": 0.75
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.473,
        "lower80": 0.34,
        "upper80": 0.59
      },
      "selective_product_yield": {
        "estimate": 0.095,
        "lower80": 0.035,
        "upper80": 0.18
      },
      "transport_efficiency": {
        "estimate": 0.57,
        "lower80": 0.37,
        "upper80": 0.75
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.08,
        "lower80": 0.0,
        "upper80": 0.3
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.05
      },
      "faradaic_efficiency": {
        "estimate": 0.015,
        "lower80": 0.0,
        "upper80": 0.08
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.06
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0.0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.02,
        "lower80": 0.0,
        "upper80": 0.1
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.22,
        "lower80": 0.0,
        "upper80": 0.5
      },
      "energy_efficiency": {
        "estimate": 0.035,
        "lower80": 0.0,
        "upper80": 0.16
      },
      "faradaic_efficiency": {
        "estimate": 0.06,
        "lower80": 0.0,
        "upper80": 0.2
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.038,
        "lower80": 0.0,
        "upper80": 0.18
      },
      "selective_product_yield": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "transport_efficiency": {
        "estimate": 0.07,
        "lower80": 0.0,
        "upper80": 0.23
      }
    }
  ],
  "rationale": "Predictions interpolate the observed narrow productive window near positive 1 V, approximately time-dependent formation at 100 mA, and the severe loss regime observed at 500 mA. Negative-potential batches are assigned near-zero target yield, while positive 7200 s batches retain material-dependent performance. Intervals are widened for the untested 0.48 M loading, half-volume geometry, uncrossed solvent/electrolyte combinations, assay noise and the nonlinear score gate near 0.02 yield."
}
```
