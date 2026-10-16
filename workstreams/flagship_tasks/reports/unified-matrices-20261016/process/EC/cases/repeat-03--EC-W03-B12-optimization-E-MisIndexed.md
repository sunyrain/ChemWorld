# repeat-03/EC-W03-B12-optimization-E-MisIndexed

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-03\EC-W03-B12-optimization-E-MisIndexed\participant\optimization-E-MisIndexed

## 同期笔记

### v1 · 公开事件 0

# Electrochemical campaign hypotheses

## H1 [tentative]
At fixed 0.04 mol reagent in 0.08 L solvent, the balanced score should have an interior optimum in effective overpotential and electrolysis time: too little charge limits conversion, while excessive magnitude/time lowers selectivity and energy efficiency. Prediction before batch 1: moderate potential magnitude and current cap will outperform extremes; sign remains unresolved and must be tested.

## H2 [tentative]
Nominal conductivity favors E1 and S0, whereas diffusion/low proton activity may favor E3 and S1/S2. Balanced performance may therefore require a tradeoff rather than simply the highest-conductivity pair. A material screen followed by local potential/time refinement will distinguish this.

## Design decision
Use full loading (0.04 mol, 0.08 L) consistently, screen both potential signs and several electrolyte/solvent combinations, then spend later batches around the best observed region. One UV-vis snapshot per batch will provide a less precise but independent efficiency diagnostic before the required terminal assay; final assays remain authoritative.

### v2 · 公开事件 84

# Electrochemical campaign hypotheses — final source-stage revision

## H1 [supported in tested scope]
The productive polarity is negative. At S0/E0, +1.2 V for 1200 s gave score 0 and essentially no product (runner-operation-0007), whereas −1.2 V under otherwise matched conditions gave score 0.149 (runner-operation-0014). This is a polarity conclusion only for the tested loading and settings; it does not establish symmetry or a universal sign law.

## H2 [supported, with material/time confounding noted]
At 0.04 mol reagent in 0.08 L solvent and a 500 mA cap, extending operation and avoiding excessive negative bias improved balanced performance. E2/S0 at −1.2 V for 14400 s scored 0.331 (runner-operation-0056), while E2/S0 at −2.0 V for 7200 s scored 0.235 (runner-operation-0049). The comparison mixes voltage and duration, so it supports an operating-region decision rather than an isolated causal coefficient. A direct testable consequence is that, at fixed 14400 s on E1/S0, potentials near −0.9 to −1.1 V should outperform substantially more negative settings.

## H3 [supported in local screen]
E1/S0 was the strongest tested material pair. At 14400 s and 500 mA cap, stepping E1/S0 from −1.3 V to −1.1 V and −0.9 V increased final score from 0.357 to 0.381 to 0.409 (runner-operation-0063, runner-operation-0077, runner-operation-0084). The last condition also had the highest observed selective product yield (0.244) and energy efficiency (0.375). Since the optimum boundary was not crossed, a still less-negative potential remains an unresolved alternative.

## Material interpretation and limitation
E1/S0's conductivity advantages appear to outweigh its large precipitation signal (~0.84–0.85 in the best local trials); precipitation was not itself a score component but may signal robustness risk. S1 reduced precipitation somewhat and increased selectivity, but its E1 trial scored 0.346 with higher safety risk (runner-operation-0070), below the nearby E1/S0 trials. Final-assay noise and single replicates mean small numerical differences are not automatically material effects; the large monotonic local score changes are used only to select the best observed completed batch.

## Final decision
Recommend batch 12: 0.04 mol reagent, 0.08 L S0, E1, −0.9 V, 500 mA cap, 14400 s, then terminate. Change this decision if replication shows the gain over batch 11 is not reproducible, or if a less-negative potential improves the same score without sacrificing yield.

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
      "potential_V": 1.2
    },
    {
      "duration_s": 1200,
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
    "cost": 0.3527759909629822,
    "electrochemical_conversion": 0.008014115504920483,
    "electrochemical_selectivity": 0.01034972071647644,
    "energy_efficiency": 0.005256945732980967,
    "faradaic_efficiency": 0.02452157624065876,
    "ohmic_efficiency": 0.97013258934021,
    "pH_normalized": 0.23031213879585266,
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
      "current_mA": 100,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.2
    },
    {
      "duration_s": 1200,
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
    "cost": 0.3527759909629822,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.5169861316680908,
    "energy_efficiency": 0.1494969129562378,
    "faradaic_efficiency": 0.3316132426261902,
    "ohmic_efficiency": 0.978970468044281,
    "pH_normalized": 0.2276168018579483,
    "precipitation_signal": 1.0,
    "safety_risk": 0.072194404900074,
    "score": 0.14919407665729523,
    "selective_product_yield": 0.011594683863222599,
    "transport_efficiency": 0.35787004232406616
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
      "current_mA": 500,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.2
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
    "cost": 0.3694800138473511,
    "electrochemical_conversion": 0.06316003203392029,
    "electrochemical_selectivity": 0.5051632523536682,
    "energy_efficiency": 0.06768190115690231,
    "faradaic_efficiency": 0.11966752260923386,
    "ohmic_efficiency": 0.8828339576721191,
    "pH_normalized": 0.2283317893743515,
    "precipitation_signal": 0.9871104955673218,
    "safety_risk": 0.072194404900074,
    "score": 0.19828854501247406,
    "selective_product_yield": 0.024788329377770424,
    "transport_efficiency": 0.1362244337797165
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
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -1.6
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
    "cost": 0.3752399981021881,
    "electrochemical_conversion": 0.13313351571559906,
    "electrochemical_selectivity": 0.5023641586303711,
    "energy_efficiency": 0.09509989619255066,
    "faradaic_efficiency": 0.321816086769104,
    "ohmic_efficiency": 0.9182406663894653,
    "pH_normalized": 0.20249544084072113,
    "precipitation_signal": 0.8381239771842957,
    "safety_risk": 0.072194404900074,
    "score": 0.26609259843826294,
    "selective_product_yield": 0.07349871844053268,
    "transport_efficiency": 0.2903285324573517
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
    "cost": 0.4058000147342682,
    "electrochemical_conversion": 0.08988229930400848,
    "electrochemical_selectivity": 0.5340074896812439,
    "energy_efficiency": 0.07205038517713547,
    "faradaic_efficiency": 0.19634737074375153,
    "ohmic_efficiency": 0.9048863053321838,
    "pH_normalized": 0.2857264280319214,
    "precipitation_signal": 0.0,
    "safety_risk": 0.09559440612792969,
    "score": 0.2306528389453888,
    "selective_product_yield": 0.05406513810157776,
    "transport_efficiency": 0.18583790957927704
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
    "cost": 0.37380000948905945,
    "electrochemical_conversion": 0.1358790397644043,
    "electrochemical_selectivity": 0.5063320994377136,
    "energy_efficiency": 0.14451804757118225,
    "faradaic_efficiency": 0.31078433990478516,
    "ohmic_efficiency": 0.8950957655906677,
    "pH_normalized": 0.15380999445915222,
    "precipitation_signal": 0.0023995577357709408,
    "safety_risk": 0.072194404900074,
    "score": 0.2719714641571045,
    "selective_product_yield": 0.07748053222894669,
    "transport_efficiency": 0.28610101342201233
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
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -2
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
    "cost": 0.38100001215934753,
    "electrochemical_conversion": 0.11713708937168121,
    "electrochemical_selectivity": 0.44649821519851685,
    "energy_efficiency": 0.08023174107074738,
    "faradaic_efficiency": 0.2311147004365921,
    "ohmic_efficiency": 0.9528635144233704,
    "pH_normalized": 0.15282459557056427,
    "precipitation_signal": 0.0,
    "safety_risk": 0.072194404900074,
    "score": 0.23469829559326172,
    "selective_product_yield": 0.05520246922969818,
    "transport_efficiency": 0.23451505601406097
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
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -1.2
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
    "cost": 0.38675999641418457,
    "electrochemical_conversion": 0.30110228061676025,
    "electrochemical_selectivity": 0.5316594839096069,
    "energy_efficiency": 0.22472958266735077,
    "faradaic_efficiency": 0.33622264862060547,
    "ohmic_efficiency": 0.8857470750808716,
    "pH_normalized": 0.15112711489200592,
    "precipitation_signal": 0.00031451715040020645,
    "safety_risk": 0.072194404900074,
    "score": 0.33082863688468933,
    "selective_product_yield": 0.14360281825065613,
    "transport_efficiency": 0.32972729206085205
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
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -1.3
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
    "cost": 0.3896400034427643,
    "electrochemical_conversion": 0.3115118741989136,
    "electrochemical_selectivity": 0.5589682459831238,
    "energy_efficiency": 0.23409812152385712,
    "faradaic_efficiency": 0.32734403014183044,
    "ohmic_efficiency": 0.9307786822319031,
    "pH_normalized": 0.20351119339466095,
    "precipitation_signal": 0.8538698554039001,
    "safety_risk": 0.072194404900074,
    "score": 0.357257604598999,
    "selective_product_yield": 0.19528447091579437,
    "transport_efficiency": 0.3481753170490265
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
      "potential_V": -1.4
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
    "cost": 0.42451998591423035,
    "electrochemical_conversion": 0.3223777115345001,
    "electrochemical_selectivity": 0.5898571610450745,
    "energy_efficiency": 0.1997261345386505,
    "faradaic_efficiency": 0.3381584882736206,
    "ohmic_efficiency": 0.8592058420181274,
    "pH_normalized": 0.20839183032512665,
    "precipitation_signal": 0.6566107869148254,
    "safety_risk": 0.09559440612792969,
    "score": 0.34578436613082886,
    "selective_product_yield": 0.17280934751033783,
    "transport_efficiency": 0.3395080864429474
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
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -1.1
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
    "cost": 0.38387998938560486,
    "electrochemical_conversion": 0.35638105869293213,
    "electrochemical_selectivity": 0.5856726169586182,
    "energy_efficiency": 0.2870481014251709,
    "faradaic_efficiency": 0.36984461545944214,
    "ohmic_efficiency": 0.8857187032699585,
    "pH_normalized": 0.2021820843219757,
    "precipitation_signal": 0.8509208559989929,
    "safety_risk": 0.072194404900074,
    "score": 0.38110461831092834,
    "selective_product_yield": 0.20539037883281708,
    "transport_efficiency": 0.3770245313644409
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
      "solvent": 0,
      "volume_L": 0.08
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -0.9
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
    "cost": 0.3781200051307678,
    "electrochemical_conversion": 0.35881590843200684,
    "electrochemical_selectivity": 0.6043039560317993,
    "energy_efficiency": 0.3748612105846405,
    "faradaic_efficiency": 0.3681500554084778,
    "ohmic_efficiency": 0.8730828762054443,
    "pH_normalized": 0.20270240306854248,
    "precipitation_signal": 0.8442568182945251,
    "safety_risk": 0.072194404900074,
    "score": 0.4090102016925812,
    "selective_product_yield": 0.24430567026138306,
    "transport_efficiency": 0.3893750011920929
  }
}
```

## K1 封存报告

Mechanistic report

1. Empirical scope and operating variables

All completed batches used 0.040 mol of limiting reagent in 0.080 L of one solvent, so the nominal initial reagent concentration was 0.50 mol L⁻¹. The variables actually explored were electrode-potential sign and magnitude, current cap, electrolysis duration, solvent identity, and electrolyte profile. The cell geometry and contact resistance were fixed but unknown. Consequently, this report describes the tested 0.50 mol L⁻¹ regime and should not be assumed to hold at other concentrations, volumes, or fixtures.

The public score was approximately the declared weighted sum

S = 0.30Y + 0.15Sel + 0.15η_energy + 0.12η_F + 0.10X + 0.10η_transport + 0.08η_ohmic,

where Y is selective product yield, Sel is electrochemical selectivity, X is electrochemical conversion, and the η terms are efficiencies. Thus yield and selectivity were especially important, while increasing conversion at the expense of Faradaic or energy efficiency could reduce overall performance.

2. Proposed process model

I think the benchmark represents a cathodic conversion competing with nonproductive charge transfer and mass-transport limitations. A useful qualitative model is:

E_eff = E_applied − ΔE_electrolyte − ΔE_solvent − E_eq,

i(t) = min[I_cap, i_kinetic(E_eff, composition), i_transport(composition, conversion)],

dn_target/dt = i(t)η_F(t)Sel(t)/(nF),

dn_reactant/dt = −i(t)η_F(t)/(nF) plus any nonproductive chemical loss.

The shift terms are not identifiable from the campaign, but the material dossier makes such coupling plausible: electrolyte and solvent each have nominal standard-potential shifts, conductivities, diffusivities, capacitances, proton activities, and precipitation properties. In this world, negative applied potential was required for productive conversion. Increasing cathodic driving force should initially increase productive current, but excessive overpotential can accelerate side reactions, lower product selectivity and Faradaic efficiency, and waste energy. High current can also increase concentration polarization, decreasing transport efficiency. Ohmic efficiency is expected to depend on conductivity and current, while energy efficiency additionally penalizes excessive cell voltage and nonproductive current.

The current setting should therefore be interpreted as a cap, not necessarily the realized current. Because no current trace or passed charge was observed, the actual charge cannot be reconstructed as I_cap × time. This is important when comparing materials: a conductive material may draw more useful current at the same potential, while a resistive one may never reach the cap.

Selective product yield is expected to scale roughly with conversion times selectivity, but the public quantities are distinct noisy estimators rather than an exact identity. For example, batch 12 had conversion 0.359 and selectivity 0.604, whose simple product is near, but not identical to, the measured yield of 0.244. Instrument noise, channel-specific calibration, and differing definitions can explain such deviations.

3. Evidence establishing polarity

Batch 1 used S0/E0 at +1.2 V, a 100 mA cap, and 1200 s. Its final score was 0, selective product yield was 0, and the UV–visible snapshot showed zero Faradaic, transport, and energy efficiency within the processed estimates. The final assay reported only about 0.008 conversion and 0.010 selectivity, both comparable to their stated assay uncertainty. This was evidence that the positive polarity was essentially inactive under those conditions.

Batch 2 reversed only the potential sign while retaining S0/E0, 100 mA, and 1200 s. Its score rose to 0.149, with yield 0.0116, selectivity 0.517, Faradaic efficiency 0.332, transport efficiency 0.358, and energy efficiency 0.149. The reported conversion was clipped to zero, so that particular conversion estimate should not be interpreted literally; the nonzero yield and efficiencies nevertheless demonstrate productive chemistry. This matched pair was the clearest mechanistic result of the campaign: productive conversion is cathodic in the tested convention.

Only one positive-potential condition was tested, so I infer a polarity requirement rather than a complete potential-response symmetry law.

4. Charge, time, and overdrive

Batch 3 retained S0/E0 and −1.2 V but increased the current cap from 100 to 500 mA and duration from 1200 to 7200 s. Conversion and yield increased to 0.063 and 0.0248, but Faradaic efficiency fell to 0.120, transport efficiency to 0.136, energy efficiency to 0.0677, and ohmic efficiency to 0.883. The score increased only modestly, from 0.149 to 0.198. Since both time and current cap changed, their effects are inseparable. Still, the result is consistent with greater cumulative conversion accompanied by current-driven transport loss and nonproductive charge.

The E2/S0 series provided evidence that extreme cathodic bias was detrimental. Batch 6 used −1.5 V, 500 mA, and 7200 s and scored 0.272, with conversion 0.136, selectivity 0.506, yield 0.0775, Faradaic efficiency 0.311, and energy efficiency 0.145. Batch 7 used the same material pair, cap, and duration at −2.0 V and fell to score 0.235: conversion was 0.117, selectivity 0.446, yield 0.0552, Faradaic efficiency 0.231, and energy efficiency 0.0802. Although assay noise prevents treating every small difference as causal, the coordinated decline across yield, selectivity, Faradaic efficiency, and energy efficiency strongly supports an overdrive penalty.

Batch 8 used E2/S0 at the less negative potential of −1.2 V for the maximum tested duration, 14400 s. It achieved score 0.331, conversion 0.301, yield 0.144, selectivity 0.532, Faradaic efficiency 0.336, transport efficiency 0.330, and energy efficiency 0.225. This was a major improvement over batches 6 and 7. However, duration also doubled relative to them, so it does not independently quantify a voltage coefficient. My interpretation is an operating-region conclusion: moderate cathodic bias sustained for longer was superior to forcing the system at very negative bias.

5. Electrolyte and solvent effects

The nominal material properties suggest several coupled effects rather than a single material ranking. E1 had the highest nominal conductivity, E3 the highest nominal diffusivity, E2 a thin diffusion layer but low conductivity and high acidity, and E0 a high nominal precipitating-salt level. S0 had the highest nominal relative conductivity and low cost but ordinary proton activity and solubility product. S1 offered higher nominal diffusivity and salt solubility but lower conductivity and higher cost.

At 500 mA and 7200 s, batch 4 used E1/S0 at −1.6 V and scored 0.266. It produced conversion 0.133, yield 0.0735, Faradaic efficiency 0.322, transport efficiency 0.290, and ohmic efficiency 0.918. Batch 6, E2/S0 at −1.5 V, scored a similar 0.272 with conversion 0.136 and yield 0.0775. E2 had much less observed precipitation (0.0024 versus 0.838 for E1) and higher energy efficiency (0.145 versus 0.095), while E1 had slightly better ohmic and transport efficiencies. These trials used different potentials, so they indicate tradeoffs rather than a controlled electrolyte ranking.

Batch 5 tested E3/S1 at −1.5 V for 7200 s. Its precipitation signal was zero, but it scored only 0.231, with conversion 0.0899, yield 0.0541, Faradaic efficiency 0.196, and transport efficiency 0.186. The result shows that nominal diffusivity and suppression of precipitation were not sufficient for high balanced performance. It could reflect poorer realized current, hidden material residuals, or a mismatched effective potential.

The best local material comparison involved E1. Batch 9 used E1/S0 at −1.3 V for 14400 s and scored 0.357, with yield 0.195, selectivity 0.559, and energy efficiency 0.234. Batch 10 used E1/S1 at −1.4 V for 14400 s and scored 0.346. S1 increased selectivity to 0.590 and reduced the precipitation signal from about 0.854 to 0.657, but yield fell to 0.173, energy efficiency to 0.200, and ohmic efficiency to 0.859. Its safety risk was also higher, 0.0956 versus 0.0722 for S0 trials. Because the potentials differed by 0.1 V to account qualitatively for nominal material shifts, this is not a strict one-factor comparison. Nonetheless, S0 appeared to exploit E1’s high conductivity more effectively, and the score did not reward precipitation suppression enough to offset its electrical disadvantages.

The pH and precipitation observations were strongly material-dependent. Representative normalized pH values were about 0.15 for E2/S0, 0.20 for E1 formulations, 0.23 for E0/S0, and 0.286 for E3/S1. E0/S0 precipitated almost completely by the public signal (~0.99–1.00); E1/S0 was also high (~0.84–0.85); E1/S1 was intermediate (~0.66); and the tested E2/S0 and E3/S1 conditions were near zero. This pattern is qualitatively consistent with electrolyte/solvent acid and solubility properties. However, precipitation was not a score component and did not prevent E1/S0 from being best. It may be a parallel equilibrium reporter, a mild transport modifier, or a robustness warning rather than the main rate-limiting process.

6. Local optimum development

The final E1/S0 potential sequence most strongly shaped the recommendation. All three batches used 0.040 mol reagent, 0.080 L S0, E1, a 500 mA cap, and 14400 s:

• Batch 9, −1.3 V: score 0.357; conversion 0.312; selectivity 0.559; yield 0.195; energy efficiency 0.234; Faradaic efficiency 0.327; transport efficiency 0.348; ohmic efficiency 0.931.

• Batch 11, −1.1 V: score 0.381; conversion 0.356; selectivity 0.586; yield 0.205; energy efficiency 0.287; Faradaic efficiency 0.370; transport efficiency 0.377; ohmic efficiency 0.886.

• Batch 12, −0.9 V: score 0.409; conversion 0.359; selectivity 0.604; yield 0.244; energy efficiency 0.375; Faradaic efficiency 0.368; transport efficiency 0.389; ohmic efficiency 0.873.

Moving from −1.3 toward −0.9 V increased score monotonically over this local sequence. The main gains were in selective yield, selectivity, energy efficiency, and transport efficiency; conversion changed little between −1.1 and −0.9 V. Ohmic efficiency declined, but its score weight was smaller and the decline was outweighed by other improvements. This behavior is consistent with less negative operation suppressing parasitic current while retaining adequate productive kinetics over the long electrolysis time.

Batch 12 was therefore the best observed procedure, not a proven mathematical optimum. Because −0.9 V was the least negative potential tested in the final E1/S0 sequence, the optimum was not bracketed. A somewhat less negative potential might improve energy efficiency further, or it might eventually become charge-limited and reduce conversion and yield. That is an extrapolation left unresolved by the sealed campaign.

7. Mechanistic interpretation of efficiencies

I interpret Faradaic efficiency as the fraction of passed charge associated with productive reactant conversion, transport efficiency as a penalty for concentration polarization or diffusion-layer depletion, and ohmic efficiency as a penalty for resistive voltage loss. Energy efficiency likely combines productive charge utilization with voltage expenditure. Selectivity then partitions converted material between target and electrochemical byproducts.

Under this interpretation, the best E1/S0 condition works because high conductivity permits useful cathodic current at only moderate overpotential. Long duration supplies enough cumulative charge to reach approximately 0.36 conversion, while the relatively mild −0.9 V setting avoids much of the side-reaction and energy penalty seen at more negative settings. Its large precipitation signal could reduce accessible area or mass transport, but the observed transport efficiency of 0.389 was still the highest measured in the final local sequence. Either precipitation was not severe enough to dominate, or E1’s conductivity compensated for it.

8. Unidentifiable factors and limitations

Several mechanistic quantities cannot be identified from these experiments:

• The realized current, charge passed, electron stoichiometry, exchange current, transfer coefficient, and equilibrium potential were not observed.

• Solvent and electrolyte potential shifts were supplied only as nominal priors; hidden, fixed world residuals and solvent–electrolyte coupling may change their effective values.

• Electrode area, gap, and contact resistance were constant but unknown, preventing extraction of current density or conductivity from performance.

• There were no replicate batches. The final assay had stated noise, so small differences should not be treated as established effects.

• Current cap and duration were changed together between early batches 2 and 3, and several material comparisons used different potentials. Their individual causal effects are therefore confounded.

• Only a sparse subset of the 16 solvent/electrolyte combinations was tested. E1/S2, E1/S3, and many other pairs remain unknown.

• Concentration and volume were fixed, so reaction order, dilution effects, and concentration-dependent precipitation cannot be inferred.

• Product degradation with time was not independently measured. Long duration could improve conversion while also causing degradation, but the present data cannot separate those pathways.

• Normalized pH and precipitation were measured reporters, not direct proof that proton activity or solid formation caused a score change.

9. Plausible alternative explanations

An alternative to the overpotential/side-reaction explanation is that the potential mainly controls whether the cell hits its current cap; the efficiency changes might then arise from different realized currents and ohmic heating rather than intrinsic selectivity kinetics. Without a current trace, both explanations remain plausible and may operate together.

Another possibility is that hidden world-specific residuals make E1 unusually favorable independently of its nominal conductivity. The material dossier explicitly allows bounded latent transport, solvation, and interface-kinetics effects. Thus the campaign supports E1/S0 empirically in this world, not a universal material-property rule.

The precipitation signal may represent an equilibrium spectator process correlated with electrolyte identity rather than electrode fouling. E1/S0 remained the best despite high precipitation, which argues against treating precipitation alone as the controlling cause. Conversely, precipitation might still limit long-term reproducibility outside the instantaneous synthetic assay.

Finally, the rise in score from batch 11 to 12 could partly contain assay noise. However, the simultaneous improvements in yield, selectivity, energy efficiency, and transport efficiency, together with the preceding improvement from batch 9 to 11, make a genuine local trend more plausible than a single-channel fluctuation.

10. Overall account

Within the tested world, the reaction is a cathodic, charge-driven conversion whose balanced outcome reflects a competition among productive electron transfer, side reactions, transport limitation, ohmic loss, and material-dependent acid/precipitation equilibria. Conductive E1 in S0 gave the best compromise. A long electrolysis supplied sufficient cumulative conversion, while progressively reducing the magnitude of the cathodic potential from −1.3 to −0.9 V improved selectivity and energy use rather than starving the desired pathway. The sealed recommendation—batch 12, 0.040 mol reagent in 0.080 L S0, E1, −0.9 V, 500 mA cap, 14400 s—should therefore be understood as the best observed point on an incompletely bracketed response surface, not as a universal or fully identified kinetic optimum.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific response law, calibrated kinetic model, or prior ranking of the materials was supplied. The supplied dossier contained only nominal material properties and explicitly allowed hidden world-specific residuals. The scoring and instrument contracts were supplied, but they were not mechanistic priors.

The self-developed cathodic-polarity claim was strongly supported. Batch 1 at +1.2 V produced zero yield and score, whereas batch 2 changed only the sign to −1.2 V and produced yield 0.0116 and score 0.149. This matched comparison changed polarity from unresolved to supported.

The claim that excessive cathodic bias harms balanced performance was supported locally. With E2/S0, batch 7 at −2.0 V scored 0.235, below batch 6 at −1.5 V, 0.272; yield, selectivity, Faradaic efficiency, and energy efficiency all declined. Later, E1/S0 improved from batch 9 at −1.3 V (0.357) to batch 11 at −1.1 V (0.381) and batch 12 at −0.9 V (0.409). However, an interior optimum was not established because performance was still improving at the least-negative tested point.

The tentative expectation that high nominal diffusivity or low precipitation might identify the best material was contradicted as a simple ranking. Batch 5, E3/S1, had no detected precipitation but scored only 0.231. Conversely, E1/S0 in batches 9, 11, and 12 retained a precipitation signal near 0.85 yet gave the best scores. Precipitation may still affect robustness, but it was not the dominant observed score determinant.

The hypothesis that conductivity is useful was supported empirically but not isolated causally. E1/S0 became the best tested pair, especially in batches 9, 11, and 12, consistent with E1 and S0 having favorable nominal conductivity. Hidden material residuals, different effective potentials, and the lack of a complete factorial screen prevent attributing that advantage solely to conductivity.

The proposed benefit of long, moderately biased electrolysis was supported as an operating-region claim. Batch 8 at −1.2 V for 14400 s scored 0.331, well above shorter, more negative E2/S0 batches 6 and 7. Duration and potential were confounded, so a separate time law remained untested. Likewise, the suggestion that a larger current cap causes transport and Faradaic losses was only weakly supported: batches 2 and 3 changed both current cap and duration.

The solvent claim that S1 suppresses precipitation was provisionally supported: E1/S1 batch 10 had precipitation 0.657 versus approximately 0.85 for nearby E1/S0 batches. Nevertheless, batch 10 scored below batches 9, 11, and 12. Because potential also differed, the solvent effect was not cleanly identified.

Untested claims include reaction order, exact electron stoichiometry, the realized-current law, the location of the potential optimum above −0.9 V, concentration effects, electrode fouling by precipitate, product degradation during long electrolysis, and most solvent–electrolyte interactions.

2. Most informative additional experiment

I would repeat the batch-12 composition and duration—0.040 mol reagent, 0.080 L S0, E1, 500 mA cap, and 14400 s—but use −0.7 V. I would retain the same termination and final-assay procedure.

The leading explanation is that moving toward less-negative potential suppresses parasitic charge and improves selectivity and energy efficiency while still providing adequate productive current. A plausible alternative is that the apparent batch-9-to-12 trend was dominated by assay variation or a narrow current-threshold effect, rather than a broad overpotential penalty.

If −0.7 V increased score, selectivity, and energy efficiency while maintaining yield near batch 12, I would conclude that the explored optimum was not bracketed and move the preferred region toward less-negative potential. If selectivity and energy efficiency improved but conversion and yield fell enough to reduce score, that would reveal the expected kinetic-versus-efficiency crossover and place an interior optimum between −0.9 and −0.7 V. If all productive metrics collapsed, I would infer a sharp activation or current threshold near −0.9 V and weaken the broad parasitic-overdrive explanation. If the result was statistically indistinguishable from batch 12, I would regard the surface as locally flat and prioritize replication over further voltage refinement. A highly discordant result would increase concern that the previous monotonic sequence was substantially affected by run-to-run or assay noise.

3. Unused evidence, reliability, and goal effects

Most raw spectral information was unused. I relied on processed final-assay estimates and did not model chromatographic peak shapes, UV–visible absorbance arrays, mass-balance details, or raw calibration channels. The intermediate UV–visible measurements were used mainly to recognize batch 1 as inactive; their quantitative values were not incorporated into a fitted response model. Cost, minor temperature changes, sample consumption, raw pH electrode information, and most spectral assignments were also unused. Normalized pH and precipitation informed qualitative interpretation but were not used quantitatively to predict score.

The least reliable blind predictions are Q09 and Q10 because S2 was never tested, and Q07 and Q08 because E3 was observed only once in a different solvent and at a different potential. Q11 and Q12 are also uncertain because the effect of the 500 mA cap at the new smaller loading was not isolated. Q01 is especially sensitive to the selective-yield gate near 0.02, so a small yield error can cause a large score error. All predictions extrapolate from 0.040 mol/0.080 L to 0.012 mol/0.025 L and assume that the nearly matched concentration is more important than absolute scale. Positive-potential predictions are directionally confident but their tiny nonzero assay-floor values are not precise.

The batch-12 recommendation is the most reliable among tested batches but less reliable as a true optimum: it had the highest observed score, yet there were no replicates and the optimum was not bracketed on the less-negative side.

The assigned maximization goal materially affected evidence collection. With only 12 completed batches, the campaign shifted from polarity and material exploration toward exploiting E1/S0 and improving score. That choice produced a strong operating recommendation but sacrificed replication, full factorial material comparisons, independent current-versus-time tests, concentration studies, and direct mechanistic identification. This is a genuine exploration–exploitation tradeoff rather than evidence of a conflict with the data.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.54,
        "lower80": 0.43,
        "upper80": 0.65
      },
      "energy_efficiency": {
        "estimate": 0.24,
        "lower80": 0.12,
        "upper80": 0.36
      },
      "faradaic_efficiency": {
        "estimate": 0.36,
        "lower80": 0.24,
        "upper80": 0.48
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.17,
        "lower80": 0.04,
        "upper80": 0.31
      },
      "selective_product_yield": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.033
      },
      "transport_efficiency": {
        "estimate": 0.38,
        "lower80": 0.25,
        "upper80": 0.51
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.032
      },
      "energy_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.028
      },
      "faradaic_efficiency": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.036
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.001,
        "lower80": 0.0,
        "upper80": 0.032
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0.0,
        "upper80": 0.014
      },
      "transport_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.027
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.48,
        "upper80": 0.68
      },
      "energy_efficiency": {
        "estimate": 0.3,
        "lower80": 0.19,
        "upper80": 0.41
      },
      "faradaic_efficiency": {
        "estimate": 0.36,
        "lower80": 0.25,
        "upper80": 0.47
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.317,
        "lower80": 0.21,
        "upper80": 0.42
      },
      "selective_product_yield": {
        "estimate": 0.06,
        "lower80": 0.025,
        "upper80": 0.105
      },
      "transport_efficiency": {
        "estimate": 0.38,
        "lower80": 0.26,
        "upper80": 0.5
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.036
      },
      "energy_efficiency": {
        "estimate": 0.007,
        "lower80": 0.0,
        "upper80": 0.03
      },
      "faradaic_efficiency": {
        "estimate": 0.014,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.038
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0.0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.03
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.63,
        "lower80": 0.53,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.4,
        "lower80": 0.28,
        "upper80": 0.52
      },
      "faradaic_efficiency": {
        "estimate": 0.43,
        "lower80": 0.31,
        "upper80": 0.55
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.381,
        "lower80": 0.28,
        "upper80": 0.48
      },
      "selective_product_yield": {
        "estimate": 0.12,
        "lower80": 0.07,
        "upper80": 0.18
      },
      "transport_efficiency": {
        "estimate": 0.44,
        "lower80": 0.31,
        "upper80": 0.57
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.038
      },
      "energy_efficiency": {
        "estimate": 0.007,
        "lower80": 0.0,
        "upper80": 0.032
      },
      "faradaic_efficiency": {
        "estimate": 0.014,
        "lower80": 0.0,
        "upper80": 0.042
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0.0,
        "upper80": 0.016
      },
      "transport_efficiency": {
        "estimate": 0.007,
        "lower80": 0.0,
        "upper80": 0.032
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.45,
        "upper80": 0.7
      },
      "energy_efficiency": {
        "estimate": 0.27,
        "lower80": 0.14,
        "upper80": 0.4
      },
      "faradaic_efficiency": {
        "estimate": 0.31,
        "lower80": 0.18,
        "upper80": 0.44
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.306,
        "lower80": 0.18,
        "upper80": 0.43
      },
      "selective_product_yield": {
        "estimate": 0.075,
        "lower80": 0.027,
        "upper80": 0.135
      },
      "transport_efficiency": {
        "estimate": 0.34,
        "lower80": 0.19,
        "upper80": 0.49
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.011,
        "lower80": 0.0,
        "upper80": 0.037
      },
      "energy_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.031
      },
      "faradaic_efficiency": {
        "estimate": 0.013,
        "lower80": 0.0,
        "upper80": 0.041
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0.0,
        "upper80": 0.016
      },
      "transport_efficiency": {
        "estimate": 0.006,
        "lower80": 0.0,
        "upper80": 0.031
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.47,
        "upper80": 0.75
      },
      "energy_efficiency": {
        "estimate": 0.26,
        "lower80": 0.12,
        "upper80": 0.41
      },
      "faradaic_efficiency": {
        "estimate": 0.33,
        "lower80": 0.18,
        "upper80": 0.48
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.294,
        "lower80": 0.16,
        "upper80": 0.43
      },
      "selective_product_yield": {
        "estimate": 0.065,
        "lower80": 0.018,
        "upper80": 0.13
      },
      "transport_efficiency": {
        "estimate": 0.29,
        "lower80": 0.13,
        "upper80": 0.46
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "energy_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.03
      },
      "faradaic_efficiency": {
        "estimate": 0.013,
        "lower80": 0.0,
        "upper80": 0.043
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.042
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0.0,
        "upper80": 0.017
      },
      "transport_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.032
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.54,
        "lower80": 0.42,
        "upper80": 0.65
      },
      "energy_efficiency": {
        "estimate": 0.18,
        "lower80": 0.08,
        "upper80": 0.3
      },
      "faradaic_efficiency": {
        "estimate": 0.23,
        "lower80": 0.12,
        "upper80": 0.35
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.264,
        "lower80": 0.16,
        "upper80": 0.37
      },
      "selective_product_yield": {
        "estimate": 0.07,
        "lower80": 0.027,
        "upper80": 0.125
      },
      "transport_efficiency": {
        "estimate": 0.24,
        "lower80": 0.12,
        "upper80": 0.37
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.01,
        "lower80": 0.0,
        "upper80": 0.036
      },
      "energy_efficiency": {
        "estimate": 0.004,
        "lower80": 0.0,
        "upper80": 0.027
      },
      "faradaic_efficiency": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.002,
        "lower80": 0.0,
        "upper80": 0.04
      },
      "selective_product_yield": {
        "estimate": 0.001,
        "lower80": 0.0,
        "upper80": 0.016
      },
      "transport_efficiency": {
        "estimate": 0.005,
        "lower80": 0.0,
        "upper80": 0.03
      }
    }
  ],
  "rationale": "The campaign’s matched polarity test showed productive chemistry only at negative potential, so all positive-potential batches are predicted near the assay floor. Negative-potential estimates combine charge-per-mole scaling with the observed benefits of moderate cathodic bias and low current, while allowing broad intervals for the new smaller scale. E1 is favored by its observed conductivity/performance, E3 is intermediate, and untested S2 receives wider uncertainty. Score intervals also reflect the strong selective-yield gate near 0.02 and the absence of replicates or measured current traces."
}
```
