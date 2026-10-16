# repeat-01/EC-W04-B12-discovery-E-Aligned

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-01\EC-W04-B12-discovery-E-Aligned\participant\discovery-E-Aligned

## 同期笔记

### v1 · 公开事件 0

# Pre-experiment hypotheses

H1 [tentative] Product formation should depend on signed overpotential relative to material-shifted onset: positive and negative potentials may be strongly asymmetric. Conversion should rise with time/charge before selectivity or efficiency deteriorates at excessive driving force.

H2 [tentative] Transport and ohmic efficiency should improve with effective conductivity and diffusivity, but electrolyte/solvent potential shifts may move the productive window. Thus E0/S0 or E3/S0 may conduct well, while E1/S1 may transport efficiently; observed assay data will override this nominal prior.

H3 [tentative] Current is a cap rather than delivered charge. At low cap, conversion should be cap/time limited; above the cell demand it may plateau. A signed-potential, time, cap, and material factorial screen at fixed loading (initially 0.020 mol in 0.050 L) will test these claims.

Predictions before experiment: a moderate potential and duration should outperform extremes in selective yield and energy efficiency; reversing potential sign may sharply suppress or redirect conversion. Results that show comparable sign responses, monotonic benefit at extremes, or material rankings contrary to nominal properties will revise these claims.

### v2 · 公开事件 84

# Final source-stage hypothesis notebook

## H1 [supported in tested positive-potential window; sign and high-field asymmetry]
Product formation is strongly potential-window dependent rather than monotonic in |potential|. At E2/S0, 14,400 s and 100 mA cap, conversion/selective yield increased from 0.263/0.239 at +0.4 V (runner-operation-0063), to 0.328/0.298 at +0.8 V (runner-operation-0049), to 0.362/0.331 at +1.0 V (runner-operation-0070). However +1.6 V for 7,200 s collapsed conversion, selectivity, faradaic and energy efficiencies to approximately zero (runner-operation-0056), whereas +0.8 V for 7,200 s gave conversion 0.161 and yield 0.156 (runner-operation-0042). This supports a productive positive window with a destructive/diverting high-potential regime. Negative-potential evidence is limited to E0/S0: -0.8 V gave conversion at the floor and low selectivity (runner-operation-0014), so sign generality across materials remains unresolved.

Testable consequence: interpolation near +1.0 V should remain productive, but a threshold between +1.0 and +1.6 V should cause an abrupt loss; threshold location should shift with nominal material potential shifts.

## H2 [supported for time dependence in one regime]
For E2/S0 at +0.8 V and 100 mA cap, conversion rose from 0.0094 at 600 s (runner-operation-0028) to 0.1607 at 7,200 s (runner-operation-0042) and 0.3275 at 14,400 s (runner-operation-0049), with selectivity and efficiency remaining high. This is consistent with an approximately linear early/mid-time charge-limited regime over the tested range, not yet substrate-depletion saturation. Between-batch uncertainty and the 600 s near-floor value limit precision.

Testable consequence: at this loading, intermediate durations should approximately interpolate until conversion becomes large enough for depletion or degradation; long times at +1.6 V should not be extrapolated from this law.

## H3 [supported: current cap is active at low cap]
At E2/S0, +1.0 V, 14,400 s, lowering the cap from 100 to 10 mA reduced conversion from 0.362 (runner-operation-0070) to 0.0476 (runner-operation-0077), while ohmic efficiency increased to about 0.998. The conversion ratio (~7.6) is qualitatively consistent with charge limitation but not claimed proportional without more cap levels. High-cap saturation remains untested.

Testable consequence: below the cell's demanded current, yield should scale strongly with cap×time; above it, increasing the cap should have little effect.

## H4 [supported for precipitation/material effects; residuals unresolved]
At S0, +0.8 V, 100 mA, 600 s, E0 and E1 showed severe precipitation signals (1.00 and 0.839; runner-operation-0007 and runner-operation-0021), while E2 and E3 were near zero (runner-operation-0028 and runner-operation-0035). E2 combined low precipitation with high faradaic/transport efficiency; E3 avoided precipitation but had substantially lower faradaic/transport efficiencies. Numerical conversion differences at 600 s are small relative to the assay noise scale and should not be treated as a reliable electrolyte effect.

Changing only solvent from S0 to S2 at E2, +1.0 V, 100 mA, 14,400 s reduced conversion/selective yield from 0.362/0.331 (runner-operation-0070) to 0.281/0.275 (runner-operation-0084), with lower selectivity and efficiencies. This one comparison supports a solvent effect but cannot distinguish conductivity, solvation, potential-shift, and hidden residual mechanisms.

## Working predictive account and decision
Use a signed effective-overpotential window modified by electrolyte and solvent standard-potential shifts. Within the productive window, extent is primarily accumulated delivered charge, constrained by the current cap and time; material transport/ohmic factors modulate delivered current and efficiency. Precipitation independently gates usable product, especially for E0/E1. Beyond an upper positive threshold, a competing/degradation pathway collapses faradaic selectivity and transport efficiency. This is an empirical scoped account, not a unique mechanism.

Recommended tested condition is batch 10 (E2/S0, +1.0 V, 100 mA cap, 14,400 s): highest observed score and selective yield, with high selectivity and efficiencies and no precipitation. I would change this choice if replicated evidence showed the apparent +1.0 V advantage was noise, or if an untested nearby voltage/cap improved yield without crossing the high-potential collapse.

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
      "potential_V": 0.8
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
    "cost": 0.28519201278686523,
    "electrochemical_conversion": 0.016118235886096954,
    "electrochemical_selectivity": 0.9864726662635803,
    "energy_efficiency": 0.6708076596260071,
    "faradaic_efficiency": 0.545807421207428,
    "ohmic_efficiency": 0.9488057494163513,
    "pH_normalized": 0.23443032801151276,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.5171036720275879
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
      "potential_V": -0.8
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
    "cost": 0.28519201278686523,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.6910410523414612,
    "energy_efficiency": 0.40402787923812866,
    "faradaic_efficiency": 0.46832001209259033,
    "ohmic_efficiency": 0.9576435685157776,
    "pH_normalized": 0.2317349761724472,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.24444086849689484,
    "selective_product_yield": 0.013939778320491314,
    "transport_efficiency": 0.4945768117904663
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
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 0.8
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
    "cost": 0.28519201278686523,
    "electrochemical_conversion": 0.007576971780508757,
    "electrochemical_selectivity": 0.860494077205658,
    "energy_efficiency": 0.8266544342041016,
    "faradaic_efficiency": 0.8169344663619995,
    "ohmic_efficiency": 0.9396834373474121,
    "pH_normalized": 0.20242463052272797,
    "precipitation_signal": 0.8390123248100281,
    "safety_risk": 0.05933958664536476,
    "score": 0.016275139525532722,
    "selective_product_yield": 0.000637519231531769,
    "transport_efficiency": 0.8334913849830627
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
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": 0.8
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
    "cost": 0.28519201278686523,
    "electrochemical_conversion": 0.009430931881070137,
    "electrochemical_selectivity": 0.8886573910713196,
    "energy_efficiency": 0.8296782374382019,
    "faradaic_efficiency": 0.8782563805580139,
    "ohmic_efficiency": 0.9459753632545471,
    "pH_normalized": 0.1583879441022873,
    "precipitation_signal": 0.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.34107717871665955,
    "selective_product_yield": 0.012911942787468433,
    "transport_efficiency": 0.8467687964439392
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
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": 0.8
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
    "cost": 0.28519201278686523,
    "electrochemical_conversion": 0.010964980348944664,
    "electrochemical_selectivity": 0.7675487399101257,
    "energy_efficiency": 0.7034745216369629,
    "faradaic_efficiency": 0.4944763481616974,
    "ohmic_efficiency": 0.9589851498603821,
    "pH_normalized": 0.2750227451324463,
    "precipitation_signal": 0.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.2911360561847687,
    "selective_product_yield": 0.014185898005962372,
    "transport_efficiency": 0.4839668869972229
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
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": 0.8
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
    "cost": 0.28730401396751404,
    "electrochemical_conversion": 0.16072577238082886,
    "electrochemical_selectivity": 0.9215794205665588,
    "energy_efficiency": 0.8637403249740601,
    "faradaic_efficiency": 0.8740627765655518,
    "ohmic_efficiency": 0.9472663402557373,
    "pH_normalized": 0.16007278859615326,
    "precipitation_signal": 0.0023995577357709408,
    "safety_risk": 0.05933958664536476,
    "score": 0.5962183475494385,
    "selective_product_yield": 0.15580350160598755,
    "transport_efficiency": 0.8493794798851013
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
      "current_mA": 100,
      "electrolyte_profile": 2,
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
    "cost": 0.2896080017089844,
    "electrochemical_conversion": 0.32750242948532104,
    "electrochemical_selectivity": 0.9151692390441895,
    "energy_efficiency": 0.8690923452377319,
    "faradaic_efficiency": 0.8521642684936523,
    "ohmic_efficiency": 0.9788278341293335,
    "pH_normalized": 0.1590873748064041,
    "precipitation_signal": 0.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.655979335308075,
    "selective_product_yield": 0.2982248365879059,
    "transport_efficiency": 0.8555646538734436
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
      "current_mA": 100,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": 1.6
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
    "cost": 0.2896080017089844,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.008051441982388496,
    "ohmic_efficiency": 0.9904510378837585,
    "pH_normalized": 0.15738990902900696,
    "precipitation_signal": 0.00031451715040020645,
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
      "solvent": 0,
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": 0.4
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
    "cost": 0.28730401396751404,
    "electrochemical_conversion": 0.26300373673439026,
    "electrochemical_selectivity": 0.8292244672775269,
    "energy_efficiency": 0.7815618515014648,
    "faradaic_efficiency": 0.7013316750526428,
    "ohmic_efficiency": 0.9244104027748108,
    "pH_normalized": 0.15940368175506592,
    "precipitation_signal": 0.008188718929886818,
    "safety_risk": 0.05933958664536476,
    "score": 0.5700426697731018,
    "selective_product_yield": 0.23931802809238434,
    "transport_efficiency": 0.7221629619598389
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
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 2,
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
    "cost": 0.29076001048088074,
    "electrochemical_conversion": 0.3623864948749542,
    "electrochemical_selectivity": 0.9785937666893005,
    "energy_efficiency": 0.9337854981422424,
    "faradaic_efficiency": 0.9390836358070374,
    "ohmic_efficiency": 0.9470465183258057,
    "pH_normalized": 0.15708954632282257,
    "precipitation_signal": 0.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.7047562003135681,
    "selective_product_yield": 0.3305453062057495,
    "transport_efficiency": 0.9404332637786865
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
      "current_mA": 10,
      "electrolyte_profile": 2,
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
    "cost": 0.2855759859085083,
    "electrochemical_conversion": 0.04756684601306915,
    "electrochemical_selectivity": 0.94280606508255,
    "energy_efficiency": 0.9603658318519592,
    "faradaic_efficiency": 0.9165279865264893,
    "ohmic_efficiency": 0.998435914516449,
    "pH_normalized": 0.15807457268238068,
    "precipitation_signal": 0.005239714402705431,
    "safety_risk": 0.05933958664536476,
    "score": 0.5826773643493652,
    "selective_product_yield": 0.03405294567346573,
    "transport_efficiency": 0.923707902431488
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
      "volume_L": 0.05
    },
    {
      "current_mA": 100,
      "electrolyte_profile": 2,
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
    "cost": 0.34275999665260315,
    "electrochemical_conversion": 0.2806921899318695,
    "electrochemical_selectivity": 0.8705427646636963,
    "energy_efficiency": 0.8158780932426453,
    "faradaic_efficiency": 0.7621603608131409,
    "ohmic_efficiency": 0.9445438385009766,
    "pH_normalized": 0.1743343025445938,
    "precipitation_signal": 0.0,
    "safety_risk": 0.10073958337306976,
    "score": 0.6088460087776184,
    "selective_product_yield": 0.2748412787914276,
    "transport_efficiency": 0.7833852767944336
  }
}
```

## K1 封存报告

## 1. Experimental scope

I studied 12 batches, all at the same initial loading: 0.020 mol limiting reagent in 0.050 L solvent (nominally 0.40 mol L⁻¹). Each batch received one continuous electrolysis period, one UV–vis measurement, termination, and a final assay. Variables explored were potential sign and magnitude, electrolysis time, current cap, electrolyte profile, and one solvent substitution. Because there were no technical replicates, conclusions rely on effect size, internal trends, and the declared instrument uncertainties rather than formal estimates of run-to-run variance.

The main empirical finding is that this world behaves like a charge-limited electrochemical conversion inside a finite positive-potential window. Time and current cap determine how much reaction occurs within that window; electrolyte and solvent influence precipitation, transport, ohmic loss, acidity, and the location or quality of the potential window. Excessively positive potential produces an abrupt collapse rather than a continuing increase in conversion.

## 2. Proposed process model

A useful phenomenological model is:

η = V_applied − [E₀ + ΔE_electrolyte + ΔE_solvent + δ_world] − iR_eff

I_delivered = min(I_cap, I_cell(η, materials))

Q = ∫ I_delivered dt

X_productive ≈ 1 − exp[−k(η, materials)Q/Q*]

Y_selective ≈ X_productive × S(η, materials) × G_precipitation

Here η is an unobserved effective overpotential, δ_world represents the fixed hidden material/interface residuals, and R_eff depends on fixture resistance and effective conductivity. At low conversion, the exponential reduces to an approximately linear charge law. S is a potential-dependent selectivity factor. G_precipitation represents loss or masking associated with salt precipitation. This is an explanatory approximation, not a uniquely identified kinetic law.

I infer three regimes:

1. **Under-driven or current-limited:** conversion is small because delivered charge is small.
2. **Productive window:** increasing positive potential, time, or an active current cap increases conversion while selectivity remains high.
3. **High-potential collapse:** a competing process, passivation, deactivation, or benchmark control transition suppresses productive faradaic behavior.

The identity of the high-potential process is not observable. Calling it “degradation” is a conjecture; plausible alternatives include electrode passivation, diversion to an unobserved side reaction, loss of active material, or a sharp transport/interface transition.

## 3. Evidence for time and charge dependence

The cleanest time series used S0/E2 at +0.8 V and a 100 mA cap:

- Batch 4, 600 s: conversion 0.00943, selective yield 0.01291.
- Batch 6, 7,200 s: conversion 0.16073, selective yield 0.15580.
- Batch 7, 14,400 s: conversion 0.32750, selective yield 0.29822.

The 7,200-to-14,400 s doubling produced approximately a doubling of conversion (ratio about 2.04). Conversion rates calculated simply as X/t are approximately 2.23×10⁻⁵ s⁻¹ and 2.27×10⁻⁵ s⁻¹ for those two batches. This strongly supports an approximately linear, delivered-charge-limited regime over this interval. Batch 4 is close to the final-assay conversion noise scale of 0.01, so its small departure from this line is not mechanistically significant.

There is no evidence that substrate-depletion saturation had been reached by 14,400 s: conversion was only about 0.33 and remained nearly proportional to time. Extrapolating the linear law much beyond the observed range would nevertheless be unsafe because depletion, product inhibition, heating, or secondary reactions could eventually intervene.

The current-cap comparison supports the same account. At S0/E2, +1.0 V, and 14,400 s:

- Batch 10, 100 mA cap: conversion 0.36239 and selective yield 0.33055.
- Batch 11, 10 mA cap: conversion 0.04757 and selective yield 0.03405.

A tenfold lower cap reduced conversion by a factor of about 7.6 and yield by about 9.7. Batch 11 also had very high ohmic efficiency, 0.99844, compared with 0.94705 in batch 10. Thus the low cap conserves voltage/ohmic efficiency but severely limits productive charge. The response is qualitatively compatible with cap×time scaling, although two cap levels cannot establish exact proportionality or reveal the cap above which the cell becomes potential- rather than cap-limited.

## 4. Potential response and competing high-potential process

At S0/E2, 100 mA, and 14,400 s, the productive response increased across the tested moderate positive potentials:

- Batch 9, +0.4 V: conversion 0.26300, selectivity 0.82922, yield 0.23932, faradaic efficiency 0.70133.
- Batch 7, +0.8 V: conversion 0.32750, selectivity 0.91517, yield 0.29822, faradaic efficiency 0.85216.
- Batch 10, +1.0 V: conversion 0.36239, selectivity 0.97859, yield 0.33055, faradaic efficiency 0.93908.

This is not merely a conversion effect: selectivity and faradaic efficiency also improved toward +1.0 V. In this tested range, additional positive driving force appears to favor the productive electron-transfer channel relative to parasitic current.

The trend cannot be extrapolated monotonically. Batch 8 used S0/E2 at +1.6 V, 100 mA, for 7,200 s and returned conversion 0, selectivity 0, energy efficiency 0, transport efficiency 0.00156, and faradaic efficiency 0.00805. At the same duration, batch 6 at +0.8 V had conversion 0.16073, selectivity 0.92158, yield 0.15580, and faradaic efficiency 0.87406. The effect is far larger than measurement uncertainty and indicates an abrupt regime change somewhere between +1.0 and +1.6 V under these material conditions.

The near-unity ohmic efficiency in batch 8 (0.99045) rules out simple ohmic loss as the sole explanation. Instead, current or potential is being rendered chemically unproductive, or the interface is effectively deactivated. The simultaneous collapse of faradaic and transport metrics is compatible with passivation or a benchmark-defined failure pathway, but the available channels cannot distinguish them.

Potential sign also matters, although the evidence is confounded by electrolyte choice. Batch 2, S0/E0 at −0.8 V for 600 s, had conversion at the zero floor, selectivity 0.691, and faradaic efficiency 0.468. Batch 1 at +0.8 V under otherwise matching conditions had conversion 0.0161 and selectivity 0.986. Both suffered complete precipitation signal, and the responses are small, so this supports—but does not conclusively prove—a productive positive polarity. I would not assume quantitative sign symmetry or transfer the E0 threshold directly to E2.

## 5. Electrolyte coupling, acidity, and precipitation

Batches 1, 3, 4, and 5 screened E0–E3 with S0 at +0.8 V, 100 mA, and 600 s. Their conversion values—0.0161, 0.00758, 0.00943, and 0.01096—are all close to the 0.01 assay-noise scale. Therefore, these batches do not reliably rank intrinsic reaction rates.

They do clearly separate precipitation and efficiency behavior:

- Batch 1, E0: precipitation signal 1.000; selective yield reported at the zero floor; faradaic efficiency 0.546 and transport efficiency 0.517.
- Batch 3, E1: precipitation 0.839; yield 0.00064; faradaic efficiency 0.817 and transport efficiency 0.833.
- Batch 4, E2: precipitation 0; yield 0.01291; faradaic efficiency 0.878 and transport efficiency 0.847.
- Batch 5, E3: precipitation 0; yield 0.01419; faradaic efficiency 0.494 and transport efficiency 0.484.

This ranking agrees qualitatively with the nominal precipitation priors. E0 has the largest precipitating-salt concentration and smallest Ksp; E1 is intermediate; E2 and E3 have progressively less favorable conditions for precipitation. A plausible submodel is an ion-product threshold:

P_precip = sigmoid[a(log₁₀Q_ion − log₁₀Ksp_eff)]

with Ksp_eff modified by solvent and hidden residuals. Precipitation can remove reactive or product species, obstruct transport, or simply reduce assay-visible product. The present data do not identify which role dominates.

E2 provided the best balance: little precipitation plus high faradaic and transport efficiencies. E3 avoided precipitation but performed poorly in those efficiency channels, despite its high nominal bulk conductivity. This shows that conductivity alone is insufficient; diffusion-layer thickness, diffusivity, interfacial capacitance, standard-potential shift, and fixed residual interactions all matter.

The normalized pH measurements were also materially structured: approximately 0.234 for E0, 0.202 for E1, 0.158 for E2, and 0.275 for E3 in the positive-potential screen. The lower E2 value is consistent with its greater nominal acid concentration and lower pKa. These observations support an acid-equilibrium contribution but do not show whether proton activity directly controls the productive electron-transfer step.

## 6. Solvent effect

Batch 12 changed S0 to S2 while retaining E2, +1.0 V, 100 mA, and 14,400 s. Relative to batch 10:

- Conversion decreased from 0.36239 to 0.28069.
- Selectivity decreased from 0.97859 to 0.87054.
- Yield decreased from 0.33055 to 0.27484.
- Faradaic efficiency decreased from 0.93908 to 0.76216.
- Transport efficiency decreased from 0.94043 to 0.78339.
- Energy efficiency decreased from 0.93379 to 0.81588.
- Normalized pH increased from 0.15709 to 0.17433.
- Precipitation remained at zero.

Thus S2 prevents neither the desired reaction nor precipitation control, but it weakens overall performance. This is consistent with its lower nominal conductivity and proton activity, but its +0.20 V standard-potential shift also changes effective overpotential. The experiment cannot distinguish these contributions. It is particularly important not to attribute the entire difference to conductivity, because selectivity and faradaic efficiency changed alongside transport efficiency.

## 7. Measurement interpretation

UV–vis and final-assay efficiencies usually agreed qualitatively but were not identical. For batch 10, UV–vis estimated energy/faradaic/transport efficiencies of 0.994/0.946/0.905, whereas the final assay gave 0.934/0.939/0.940. This level of disagreement is compatible with different declared measurement noise and sampling. Mechanistic conclusions are therefore based on large contrasts and replicated trends across conditions, not small channel differences.

Near-zero values require special caution because of clipping and noise. For example, batch 2 reported zero conversion but a small positive yield of 0.01394, and batch 4 had yield slightly greater than measured conversion. These should not be read as violations of mass balance; they are independent noisy processed estimates near their resolution limits.

## 8. What changed my explanation

The initial expectation was a smooth optimum in driving force with charge-limited conversion. Batches 4, 6, and 7 supported the charge/time part. Batch 11 then showed directly that the current cap is active and not just a configuration label. Batches 9 and 10 showed that moderate positive potential improves both conversion and selectivity. Batch 8 changed the explanation most strongly: the response at +1.6 V was not a mild selectivity penalty but a near-total collapse, requiring a separate high-potential state or pathway. The electrolyte screen changed the material explanation from a simple conductivity ranking to a coupled precipitation–transport–interface model. Batch 12 demonstrated that solvent shifts several efficiencies together and cannot be represented only as an inert resistance factor.

## 9. Scope, unidentified quantities, and alternatives

The account is supported only for 0.020 mol reagent in roughly 0.050 L solvent, the tested anonymous materials, potentials −0.8 to +1.6 V, caps of 10 and 100 mA, and times up to 14,400 s. Loading, concentration, volume, repeated electrolysis stages, and a 500 mA cap were not varied. E0, E1, and E3 were tested only at short time, and only S0 and S2 were compared directly.

Unidentified quantities include the formal reaction potential, actual current-time trace, electron stoichiometry, electrode area, cell resistance, mass-transfer coefficient, reaction order, species identities, precipitation composition, and hidden world residuals. Consequently, k, E₀, and the exact functional forms above cannot be fitted uniquely.

Plausible alternative models include: a thresholded empirical response surface with no literal mechanistic states; time-dependent electrode activation followed by passivation; precipitation altering optical visibility rather than chemical yield; or a high-potential protection/control rule rather than chemical degradation. The present observations favor the delivered-charge plus potential-window account because it jointly explains time, cap, potential, and efficiency trends, but they do not uniquely establish a molecular mechanism.

The most defensible predictive rule within the observed domain is: choose a non-precipitating electrolyte such as E2, account for solvent-dependent potential shifts, operate in the moderate positive window near the tested +1.0 V condition, and treat conversion as approximately proportional to delivered charge until depletion becomes important. Do not extrapolate through the abrupt high-potential boundary.

## K2 封存报告

1. **Claims and laws evaluated**

No world-specific instance prior, response law, or expected optimum was supplied. The material dossier supplied only nominal properties—conductivity, diffusivity, acidity, Ksp-related quantities, capacitance, and potential shifts—which I treated as mechanistic priors rather than known rankings.

- **Approximately charge-limited time law: supported within a restricted regime.** Before experimentation I proposed that conversion would increase with accumulated delivered charge. With S0/E2 at +0.8 V and 100 mA, conversion increased from 0.0094 at 600 s (batch 4) to 0.1607 at 7,200 s (batch 6) and 0.3275 at 14,400 s (batch 7). The near-doubling from batches 6 to 7 changed this from a tentative idea into the strongest empirical law, although saturation remains untested.
- **Low current cap limits conversion: supported.** At S0/E2, +1.0 V, and 14,400 s, reducing the cap from 100 mA in batch 10 to 10 mA in batch 11 reduced conversion from 0.3624 to 0.0476 and yield from 0.3305 to 0.0341. This showed that the cap can be active. Whether caps above 100 mA are nonbinding was not tested.
- **Moderate positive-potential window: supported.** At 14,400 s, batches 9, 7, and 10 showed increasing conversion, yield, selectivity, and faradaic efficiency from +0.4 to +0.8 to +1.0 V. Thus the initial expectation that moderate driving force would outperform weaker driving force was supported.
- **Smooth deterioration at excessive potential: contradicted by a sharper transition.** I initially anticipated a gradual selectivity or efficiency penalty. Batch 8 at +1.6 V instead showed an abrupt collapse: conversion, selectivity, and energy efficiency were at zero, and faradaic and transport efficiencies were near zero. The matched-duration batch 6 at +0.8 V was productive. This forced the addition of a distinct high-potential state or pathway rather than a smooth optimum alone.
- **Positive versus negative polarity: only partly supported.** For E0/S0 at 600 s, batch 1 at +0.8 V had much higher selectivity than batch 2 at −0.8 V, but both conversion/yield measurements were close to their noise floors and both had complete precipitation signal. Therefore polarity-dependent selectivity is supported for E0, while a general law that negative potential suppresses conversion remains untested.
- **Precipitation follows electrolyte properties: supported qualitatively.** In the 600 s electrolyte screen, E0 and E1 produced precipitation signals of 1.000 and 0.839 in batches 1 and 3, whereas E2 and E3 were near zero in batches 4 and 5. This agreed with the nominal salt concentration/Ksp ranking.
- **Simple conductivity ranking: contradicted.** E3 had high nominal bulk conductivity but batch 5 had faradaic and transport efficiencies near 0.49, much lower than E2 in batch 4. Conductivity alone therefore cannot explain performance; potential shift, diffusion-layer behavior, interfacial effects, and hidden residuals must be coupled.
- **Solvent is an inert resistance modifier: contradicted or at least inadequate.** Changing S0 to S2 between otherwise comparable batches 10 and 12 changed conversion, selectivity, faradaic efficiency, transport efficiency, energy efficiency, and normalized pH together. One comparison supports a solvent effect but does not identify whether conductivity, proton activity, solvation, or potential shift caused it.
- **E1/S1 as a favorable transport combination: untested.** E1 with S0 performed efficiently in batch 3, but S1 was never used. Likewise, depletion kinetics, reaction order, exact electron stoichiometry, and the molecular identity of the high-potential failure process remained untested.

2. **Most informative additional experiment**

I would run the standard 0.020 mol/0.050 L S0/E2 mixture at a 100 mA cap, first at +1.6 V for 3,600 s, measure by UV–vis, then switch the same batch to +1.0 V for 7,200 s, measure again, terminate, and obtain the final assay. Existing batches 8 and 10 provide the high-potential and productive-potential references.

This distinguishes a reversible potential-gated diversion—the leading minimal explanation—from irreversible passivation or degradation:

- If the +1.6 V stage produces negligible response but the subsequent +1.0 V stage resumes conversion near the rate inferred from batches 6, 7, and 10, I would favor a reversible competing-current or interface-state explanation.
- If the batch remains largely inactive after switching to +1.0 V, I would favor irreversible passivation, reagent destruction, or persistent electrode deactivation.
- If substantial conversion occurs during the +1.6 V stage or the final result follows total delivered charge without a persistent penalty, I would weaken the claimed high-potential cliff and treat batch 8 as an anomalous or context-dependent observation.
- Partial recovery would support a mixed model in which +1.6 V progressively converts active electrode or reagent into an inactive state.

A staged experiment is preferable to another independent endpoint because it tests reversibility while using the same vessel and material realization.

3. **Unused evidence, reliability, and goal effects**

The raw UV–vis spectral shapes and characterization artifacts were not analyzed; I used their processed efficiency estimates only as qualitative cross-checks. Cost and safety-risk observations contributed little because the tested batches showed no discriminating safety excursion. Nominal capacitance, diffusivity, diffusion-layer thickness, and individual conductivity values were not separately identifiable. I also did not exploit loading order because it was not varied systematically. The electrolyte screen occurred at only 600 s, leaving its conversion differences comparable to assay noise.

The least reliable blind predictions are the negative-polarity extrapolations for E1 and E3 (Q05 and Q07), the S2/E0 negative-polarity case (Q09), and the 500 mA cases (Q11–Q12). Those combine conditions never observed together or assume that 100 mA was already near a potential-limited regime. Predictions at the new 0.012 mol/0.025 L loading also assume that product amount scales mainly with charge and that concentration/geometry effects are secondary. Q01 and Q02 are especially score-uncertain because their predicted yields lie near the scoring gate and the assay floor.

The sealed recommendation of batch 10 is reliable as the best among tested batches, but not as a proven global optimum. There were no replicates and no exploration between +1.0 and +1.6 V, near the apparent regime boundary. A nearby potential might improve yield or unexpectedly cross the failure threshold.

The explanatory research goal materially affected evidence collection: I spent batches on polarity, electrolyte identity, time, current cap, and solvent contrasts rather than replicating the best condition or densely optimizing around +1.0 V. That breadth exposed the time law, precipitation ranking, cap dependence, and high-potential collapse, but it reduced precision and local optimization confidence. I see no clear conflict with the assigned goal because the public score was explicitly secondary; the trade-off was deliberate breadth versus replication, not suppression of inconvenient evidence.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.69,
        "lower80": 0.56,
        "upper80": 0.81
      },
      "energy_efficiency": {
        "estimate": 0.404,
        "lower80": 0.3,
        "upper80": 0.51
      },
      "faradaic_efficiency": {
        "estimate": 0.47,
        "lower80": 0.37,
        "upper80": 0.57
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.211,
        "lower80": 0.0,
        "upper80": 0.45
      },
      "selective_product_yield": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.042
      },
      "transport_efficiency": {
        "estimate": 0.495,
        "lower80": 0.39,
        "upper80": 0.6
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.986,
        "lower80": 0.93,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.671,
        "lower80": 0.57,
        "upper80": 0.77
      },
      "faradaic_efficiency": {
        "estimate": 0.546,
        "lower80": 0.45,
        "upper80": 0.64
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.452,
        "lower80": 0.18,
        "upper80": 0.56
      },
      "selective_product_yield": {
        "estimate": 0.025,
        "lower80": 0.002,
        "upper80": 0.059
      },
      "transport_efficiency": {
        "estimate": 0.517,
        "lower80": 0.41,
        "upper80": 0.62
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.69,
        "lower80": 0.55,
        "upper80": 0.82
      },
      "energy_efficiency": {
        "estimate": 0.404,
        "lower80": 0.3,
        "upper80": 0.51
      },
      "faradaic_efficiency": {
        "estimate": 0.47,
        "lower80": 0.37,
        "upper80": 0.57
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.391,
        "lower80": 0.3,
        "upper80": 0.49
      },
      "selective_product_yield": {
        "estimate": 0.1,
        "lower80": 0.041,
        "upper80": 0.181
      },
      "transport_efficiency": {
        "estimate": 0.495,
        "lower80": 0.39,
        "upper80": 0.6
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.986,
        "lower80": 0.93,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.671,
        "lower80": 0.57,
        "upper80": 0.77
      },
      "faradaic_efficiency": {
        "estimate": 0.546,
        "lower80": 0.45,
        "upper80": 0.64
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.507,
        "lower80": 0.42,
        "upper80": 0.59
      },
      "selective_product_yield": {
        "estimate": 0.16,
        "lower80": 0.09,
        "upper80": 0.25
      },
      "transport_efficiency": {
        "estimate": 0.517,
        "lower80": 0.41,
        "upper80": 0.62
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.39,
        "upper80": 0.79
      },
      "energy_efficiency": {
        "estimate": 0.5,
        "lower80": 0.33,
        "upper80": 0.67
      },
      "faradaic_efficiency": {
        "estimate": 0.7,
        "lower80": 0.53,
        "upper80": 0.85
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.466,
        "lower80": 0.31,
        "upper80": 0.61
      },
      "selective_product_yield": {
        "estimate": 0.13,
        "lower80": 0.043,
        "upper80": 0.25
      },
      "transport_efficiency": {
        "estimate": 0.8,
        "lower80": 0.63,
        "upper80": 0.93
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.86,
        "lower80": 0.77,
        "upper80": 0.94
      },
      "energy_efficiency": {
        "estimate": 0.827,
        "lower80": 0.72,
        "upper80": 0.92
      },
      "faradaic_efficiency": {
        "estimate": 0.817,
        "lower80": 0.7,
        "upper80": 0.91
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.599,
        "lower80": 0.5,
        "upper80": 0.69
      },
      "selective_product_yield": {
        "estimate": 0.215,
        "lower80": 0.12,
        "upper80": 0.33
      },
      "transport_efficiency": {
        "estimate": 0.833,
        "lower80": 0.71,
        "upper80": 0.93
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.54,
        "lower80": 0.31,
        "upper80": 0.74
      },
      "energy_efficiency": {
        "estimate": 0.42,
        "lower80": 0.24,
        "upper80": 0.6
      },
      "faradaic_efficiency": {
        "estimate": 0.42,
        "lower80": 0.26,
        "upper80": 0.59
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.351,
        "lower80": 0.19,
        "upper80": 0.51
      },
      "selective_product_yield": {
        "estimate": 0.07,
        "lower80": 0.012,
        "upper80": 0.16
      },
      "transport_efficiency": {
        "estimate": 0.46,
        "lower80": 0.29,
        "upper80": 0.63
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.768,
        "lower80": 0.65,
        "upper80": 0.87
      },
      "energy_efficiency": {
        "estimate": 0.703,
        "lower80": 0.59,
        "upper80": 0.81
      },
      "faradaic_efficiency": {
        "estimate": 0.494,
        "lower80": 0.38,
        "upper80": 0.61
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.455,
        "lower80": 0.35,
        "upper80": 0.56
      },
      "selective_product_yield": {
        "estimate": 0.115,
        "lower80": 0.049,
        "upper80": 0.205
      },
      "transport_efficiency": {
        "estimate": 0.484,
        "lower80": 0.36,
        "upper80": 0.61
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.614,
        "lower80": 0.39,
        "upper80": 0.8
      },
      "energy_efficiency": {
        "estimate": 0.353,
        "lower80": 0.19,
        "upper80": 0.52
      },
      "faradaic_efficiency": {
        "estimate": 0.38,
        "lower80": 0.23,
        "upper80": 0.54
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.341,
        "lower80": 0.19,
        "upper80": 0.49
      },
      "selective_product_yield": {
        "estimate": 0.07,
        "lower80": 0.009,
        "upper80": 0.16
      },
      "transport_efficiency": {
        "estimate": 0.41,
        "lower80": 0.25,
        "upper80": 0.58
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.877,
        "lower80": 0.75,
        "upper80": 0.96
      },
      "energy_efficiency": {
        "estimate": 0.586,
        "lower80": 0.45,
        "upper80": 0.71
      },
      "faradaic_efficiency": {
        "estimate": 0.443,
        "lower80": 0.32,
        "upper80": 0.57
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.438,
        "lower80": 0.33,
        "upper80": 0.55
      },
      "selective_product_yield": {
        "estimate": 0.113,
        "lower80": 0.047,
        "upper80": 0.204
      },
      "transport_efficiency": {
        "estimate": 0.431,
        "lower80": 0.3,
        "upper80": 0.57
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.69,
        "lower80": 0.54,
        "upper80": 0.82
      },
      "energy_efficiency": {
        "estimate": 0.404,
        "lower80": 0.28,
        "upper80": 0.53
      },
      "faradaic_efficiency": {
        "estimate": 0.47,
        "lower80": 0.35,
        "upper80": 0.59
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.393,
        "lower80": 0.28,
        "upper80": 0.51
      },
      "selective_product_yield": {
        "estimate": 0.105,
        "lower80": 0.036,
        "upper80": 0.2
      },
      "transport_efficiency": {
        "estimate": 0.495,
        "lower80": 0.37,
        "upper80": 0.62
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.986,
        "lower80": 0.91,
        "upper80": 1.0
      },
      "energy_efficiency": {
        "estimate": 0.671,
        "lower80": 0.54,
        "upper80": 0.79
      },
      "faradaic_efficiency": {
        "estimate": 0.546,
        "lower80": 0.42,
        "upper80": 0.67
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.508,
        "lower80": 0.4,
        "upper80": 0.61
      },
      "selective_product_yield": {
        "estimate": 0.165,
        "lower80": 0.078,
        "upper80": 0.28
      },
      "transport_efficiency": {
        "estimate": 0.517,
        "lower80": 0.38,
        "upper80": 0.65
      }
    }
  ],
  "rationale": "Predictions anchor the ±0.8 V E0 efficiencies and selectivities to batches 1–2, extrapolate the demonstrated near-linear charge–time behavior from batches 4, 6, and 7, and adjust conversion/yield for the smaller 0.012 mol charge basis. E1 and E3 positive-polarity estimates use their measured batch-3 and batch-5 efficiency profiles; their negative-polarity results are less identified and therefore receive wider intervals. The S2 adjustment follows the coupled solvent penalty observed between batches 10 and 12. I expect the 500 mA cap to be mostly nonbinding at fixed ±0.8 V, so Q11–Q12 remain close to their 100 mA counterparts but have wider intervals. Score estimates also account for the published selective-yield gate, which makes the short, near-zero-yield cases especially uncertain."
}
```
