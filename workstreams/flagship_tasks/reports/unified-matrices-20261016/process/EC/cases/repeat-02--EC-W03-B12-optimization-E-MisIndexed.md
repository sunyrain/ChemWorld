# repeat-02/EC-W03-B12-optimization-E-MisIndexed

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-02\EC-W03-B12-optimization-E-MisIndexed\participant\optimization-E-MisIndexed

## 同期笔记

### v1 · 公开事件 0

# Electrochemical campaign hypotheses

## H1 [tentative]
At fixed loading, balanced efficiency should peak at moderate overpotential and duration: insufficient drive limits conversion, while excessive magnitude/time lowers selectivity and energy efficiency. Test across both potential signs and short/long electrolysis.

## H2 [tentative]
Electrolytes/solvents with higher conductivity and transport should improve ohmic/transport efficiency, but potential shifts and hidden interfacial residuals may dominate selectivity. E1/S0 are prior candidates for conductivity; E3/S1 may offer a transport compromise. Direct final assays are authoritative.

## Design commitment
Use 0.020 mol reagent in 0.050 L solvent for comparability unless observations demand refinement. First map polarity, magnitude, duration, and materials broadly; then locally refine and repeat the strongest region. UV-vis snapshots will be diagnostic, not used as substitutes for final assays.

### v2 · 公开事件 49

# Electrochemical campaign hypotheses

## H1 [supported in tested S0/E1 scope]
Positive polarity is required for strong balanced performance: at ±1.0 V, 500 mA cap, 7200 s, the positive case scored 0.738 while the negative case scored 0.383 (events runner-operation-0014 and -0021). The effect is large relative to assay noise, though only one matched pair was tested.

The response has a narrow potential window. Raising +1.0 to +1.5 V at the same material/current/time collapsed conversion and score to near zero (runner-operation-0028), opposing any monotonic-overpotential claim. At +1.0 V, extending 7200→10800→14400 s raised yield, but efficiency losses caused scores 0.738→0.754→0.749 (runner-operation-0014, -0042, -0049). Thus the provisional duration optimum is around 10–13 ks for this recipe.

## H2 [unresolved]
S0/E1 gives high selectivity and ohmic efficiency but precipitation is consistently high; alternative electrolytes or solvents may improve transport/precipitation enough to increase score. Material shifts imply that matching effective potential may require lower applied voltage for E0/E3 and slightly lower for E2.

## Next decision
Compare material profiles near shift-adjusted positive potentials at 10.8 ks. Retain +1.0 V S0/E1 as benchmark. Revise the recommendation if another material exceeds 0.754 by more than ordinary assay-scale variation or shows a clearly better efficiency/yield balance.

### v3 · 公开事件 84

# Electrochemical campaign hypotheses — final source-stage synthesis

## H1 [supported in tested scope]
For 0.020 mol reagent in 0.050 L, productive operation requires positive polarity and a bounded potential/time window. The ±1.0 V matched comparison strongly favored positive polarity (scores 0.738 vs 0.383; runner-operation-0014 and -0021). +1.5 V was destructive/nonproductive (score 0.003; runner-operation-0028). With S0/E1 at +1.0 V and 500 mA cap, scores for 7.2, 10.8, and 14.4 ks were 0.738, 0.754, and 0.749 (runner-operation-0014, -0042, -0049), supporting an intermediate-time optimum rather than monotonic improvement.

## H2 [supported for tested material combinations]
Material choice substantially changes the efficiency balance. At comparable long electrolysis, S0/E0 and shift-adjusted S0/E3 were poor (scores 0.307 and 0.290; runner-operation-0063 and -0056); S0/E2 was viable but below S0/E1 (0.724 vs 0.754; runner-operation-0070 and -0042). Replacing S0 with S1 while using E1, +1.1 V, 500 mA cap, and 10.8 ks produced the campaign-best score 0.795 with yield 0.831, selectivity 0.981, conversion 0.851, and improved transport 0.608 (runner-operation-0077). Extending to 12.0 ks increased yield to 0.871 but reduced efficiency components and score to 0.780 (runner-operation-0084).

## Scope and unresolved alternatives
These are single-batch comparisons without direct repeats, so assay noise and run-to-run process variation remain unresolved. Potential and solvent were co-adjusted between the S0 and S1 benchmarks, so their separate causal effects are not identified. The best observed operating point is batch 11; a denser local design around +1.05–1.15 V and 9–11 ks would be the next test.

## Decision
Recommend completed batch 11: 0.020 mol reagent, 0.050 L S1, E1, +1.1 V, 500 mA cap, 10,800 s. This decision would change if a replicated local competitor exceeded its balanced score with comparable safety.

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
    "cost": 0.28644001483917236,
    "electrochemical_conversion": 0.09235981851816177,
    "electrochemical_selectivity": 0.9423536062240601,
    "energy_efficiency": 0.913285493850708,
    "faradaic_efficiency": 0.9287574887275696,
    "ohmic_efficiency": 0.9651356339454651,
    "pH_normalized": 0.20516636967658997,
    "precipitation_signal": 0.851891279220581,
    "safety_risk": 0.05933958664536476,
    "score": 0.5855979919433594,
    "selective_product_yield": 0.06449674814939499,
    "transport_efficiency": 0.9000536799430847
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
      "current_mA": 500,
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
    "cost": 0.2994000017642975,
    "electrochemical_conversion": 0.6289246678352356,
    "electrochemical_selectivity": 0.9638566374778748,
    "energy_efficiency": 0.8178838491439819,
    "faradaic_efficiency": 0.6827183961868286,
    "ohmic_efficiency": 0.8710753917694092,
    "pH_normalized": 0.2024710327386856,
    "precipitation_signal": 0.854923665523529,
    "safety_risk": 0.05933958664536476,
    "score": 0.7376259565353394,
    "selective_product_yield": 0.6165421605110168,
    "transport_efficiency": 0.7089751958847046
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
      "current_mA": 500,
      "electrolyte_profile": 1,
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
    "cost": 0.2994000017642975,
    "electrochemical_conversion": 0.3536227345466614,
    "electrochemical_selectivity": 0.5949146747589111,
    "energy_efficiency": 0.31626540422439575,
    "faradaic_efficiency": 0.35739579796791077,
    "ohmic_efficiency": 0.8578490614891052,
    "pH_normalized": 0.2031860202550888,
    "precipitation_signal": 0.8373757600784302,
    "safety_risk": 0.05933958664536476,
    "score": 0.3832336366176605,
    "selective_product_yield": 0.20761226117610931,
    "transport_efficiency": 0.3739526867866516
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
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 1.5
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
    "cost": 0.30660000443458557,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.02824951522052288,
    "ohmic_efficiency": 0.9128813743591309,
    "pH_normalized": 0.20249544084072113,
    "precipitation_signal": 0.8381239771842957,
    "safety_risk": 0.05933958664536476,
    "score": 0.0030270081479102373,
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
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 0.7
    },
    {
      "duration_s": 10800,
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
    "cost": 0.3001199960708618,
    "electrochemical_conversion": 0.7851367592811584,
    "electrochemical_selectivity": 0.8980105519294739,
    "energy_efficiency": 0.6998559236526489,
    "faradaic_efficiency": 0.5697012543678284,
    "ohmic_efficiency": 0.8143174052238464,
    "pH_normalized": 0.20745623111724854,
    "precipitation_signal": 0.837450385093689,
    "safety_risk": 0.05933958664536476,
    "score": 0.7192418575286865,
    "selective_product_yield": 0.7053982615470886,
    "transport_efficiency": 0.5591917634010315
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
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 10800,
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
    "cost": 0.30660000443458557,
    "electrochemical_conversion": 0.7838388681411743,
    "electrochemical_selectivity": 0.9580760598182678,
    "energy_efficiency": 0.7285358905792236,
    "faradaic_efficiency": 0.5827329754829407,
    "ohmic_efficiency": 0.8712981343269348,
    "pH_normalized": 0.2041803002357483,
    "precipitation_signal": 0.8480806946754456,
    "safety_risk": 0.05933958664536476,
    "score": 0.7535935640335083,
    "selective_product_yield": 0.7559370398521423,
    "transport_efficiency": 0.5580496191978455
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
      "current_mA": 500,
      "electrolyte_profile": 1,
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
    "cost": 0.31380000710487366,
    "electrochemical_conversion": 0.8790689706802368,
    "electrochemical_selectivity": 0.9516658782958984,
    "energy_efficiency": 0.6117053031921387,
    "faradaic_efficiency": 0.4678148031234741,
    "ohmic_efficiency": 0.902859628200531,
    "pH_normalized": 0.20319488644599915,
    "precipitation_signal": 0.8331227898597717,
    "safety_risk": 0.05933958664536476,
    "score": 0.7486713528633118,
    "selective_product_yield": 0.8359023332595825,
    "transport_efficiency": 0.471215158700943
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
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": 0.72
    },
    {
      "duration_s": 10800,
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
    "cost": 0.30055201053619385,
    "electrochemical_conversion": 0.1576804667711258,
    "electrochemical_selectivity": 0.782631516456604,
    "energy_efficiency": 0.1903260201215744,
    "faradaic_efficiency": 0.12432779371738434,
    "ohmic_efficiency": 0.862666666507721,
    "pH_normalized": 0.2723751962184906,
    "precipitation_signal": 0.00031451715040020645,
    "safety_risk": 0.05933958664536476,
    "score": 0.2896459996700287,
    "selective_product_yield": 0.10739466547966003,
    "transport_efficiency": 0.11783243715763092
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
      "current_mA": 500,
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 10800,
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
    "cost": 0.30426764488220215,
    "electrochemical_conversion": 0.1551521122455597,
    "electrochemical_selectivity": 0.8199702501296997,
    "energy_efficiency": 0.1523270457983017,
    "faradaic_efficiency": 0.11718098074197769,
    "ohmic_efficiency": 0.9187827706336975,
    "pH_normalized": 0.22865696251392365,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.30695846676826477,
    "selective_product_yield": 0.14744366705417633,
    "transport_efficiency": 0.13801224529743195
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
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": 1
    },
    {
      "duration_s": 10800,
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
    "cost": 0.30660000443458557,
    "electrochemical_conversion": 0.7937712073326111,
    "electrochemical_selectivity": 0.9007968902587891,
    "energy_efficiency": 0.7577624917030334,
    "faradaic_efficiency": 0.5653561949729919,
    "ohmic_efficiency": 0.8319326639175415,
    "pH_normalized": 0.15082675218582153,
    "precipitation_signal": 0.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.7244071960449219,
    "selective_product_yield": 0.6839275360107422,
    "transport_efficiency": 0.5667057633399963
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
      "solvent": 1,
      "volume_L": 0.05
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 1.1
    },
    {
      "duration_s": 10800,
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
    "cost": 0.3287599980831146,
    "electrochemical_conversion": 0.8512284755706787,
    "electrochemical_selectivity": 0.981396496295929,
    "energy_efficiency": 0.7546384930610657,
    "faradaic_efficiency": 0.6009684205055237,
    "ohmic_efficiency": 0.8372393846511841,
    "pH_normalized": 0.20937687158584595,
    "precipitation_signal": 0.6644999384880066,
    "safety_risk": 0.08273958414793015,
    "score": 0.7947366237640381,
    "selective_product_yield": 0.8309944272041321,
    "transport_efficiency": 0.6081483364105225
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
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": 1.1
    },
    {
      "duration_s": 12000,
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
    "cost": 0.3314000070095062,
    "electrochemical_conversion": 0.8517181873321533,
    "electrochemical_selectivity": 0.972674548625946,
    "energy_efficiency": 0.6831395626068115,
    "faradaic_efficiency": 0.5242974162101746,
    "ohmic_efficiency": 0.8505879044532776,
    "pH_normalized": 0.20989719033241272,
    "precipitation_signal": 0.6578359007835388,
    "safety_risk": 0.08273958414793015,
    "score": 0.7802090048789978,
    "selective_product_yield": 0.8705004453659058,
    "transport_efficiency": 0.5455223321914673
  }
}
```

## K1 封存报告

Mechanistic report

Scope and evidence base

All 12 batches used the same nominal loading: 0.020 mol limiting reagent in 0.050 L solvent (0.40 mol L^-1 before sampling). Consequently, the campaign identifies effects of polarity, potential, current cap, duration, solvent, and electrolyte only within that loading regime. Every batch had one UV–vis measurement followed by a destructive final assay. The final assays are the principal evidence because their uncertainties were smaller and they directly reported conversion, selective-product yield, selectivity, and efficiency components.

Proposed process structure

I interpret the system as a potential-driven electrochemical conversion with at least three coupled limitations:

1. Interfacial activation: productive electron transfer requires positive polarization beyond a material-dependent onset.
2. Charge/transport supply: conversion accumulates with delivered charge, but the configured current is a cap rather than proof that the full current flows. Conductivity, diffusion, diffusion-layer thickness, solvent mobility, and precipitation can limit the realized reaction rate.
3. Competing loss channels: excessive potential or extended electrolysis diverts current to side reactions and/or deactivates the productive pathway. These losses reduce faradaic, transport, and energy efficiency even when conversion or product yield continues to rise.

A useful qualitative model is

I_eff(t) = min(I_cap, I_kinetic(V - E_onset), I_transport),

dX/dt = k_product(V, materials) I_eff(t) (1-X) / (nF N0) - k_loss(V, materials) X,

dB/dt = k_side(V, materials) I_eff(t) + k_overprocess(V, materials) X,

with selective yield approximately Y = X S, where S is the fraction of converted material reaching or retaining the target. The measured yield is not always numerically identical to measured conversion times selectivity, so this relation should be treated as a structural approximation rather than an exact observation law. Faradaic efficiency reports the fraction of charge serving useful chemistry; transport efficiency reflects delivery of reactant/ions to the interface; ohmic efficiency reflects resistive loss; and energy efficiency is a coupled outcome of these efficiencies and applied potential. In simple terms,

eta_energy ≈ f(eta_F, eta_transport, eta_ohmic, useful thermodynamic voltage / applied voltage),

where f need not be a literal product in this synthetic world.

Evidence for polarity and an activation window

Batch 2 and batch 3 provide the cleanest polarity comparison. Both used S0/E1, a 500 mA cap, and 7,200 s, but batch 2 used +1.0 V and batch 3 used -1.0 V. Batch 2 gave conversion 0.629, selectivity 0.964, yield 0.617, faradaic efficiency 0.683, transport efficiency 0.709, energy efficiency 0.818, and score 0.738. Batch 3 gave conversion 0.354, selectivity 0.595, yield 0.208, faradaic efficiency 0.357, transport efficiency 0.374, energy efficiency 0.316, and score 0.383. This large matched difference supports a positive-polarity productive reaction rather than a polarity-symmetric Joule-heating process.

The response is not monotonic in positive potential. Batch 4 used the same S0/E1, 500 mA, and 7,200 s as batch 2 but increased the potential from +1.0 to +1.5 V. Its conversion, selectivity, energy efficiency, and transport efficiency were reported as zero, yield was only 0.00079, faradaic efficiency was 0.028, and score was 0.003, although ohmic efficiency remained high at 0.913. Thus bulk resistance was not the cause of failure. A plausible explanation is a narrow productive interfacial window: +1.5 V promotes a dominant parasitic reaction, passivating film, destructive over-oxidation, or an unfavorable interfacial state. The campaign cannot distinguish those alternatives because no direct electrode-surface or byproduct measurement was made.

Charge and time dependence

Batch 1 used S0/E1 at +1.0 V but only a 100 mA cap for 3,600 s. It retained excellent efficiencies—faradaic 0.929, transport 0.900, ohmic 0.965, and energy 0.913—but reached conversion 0.092 and yield 0.0645, giving score 0.586. This is consistent with charge-limited operation: gentle conditions are efficient per unit charge but do not process enough substrate.

At +1.0 V, 500 mA, S0/E1, increasing time from 7,200 s (batch 2) to 10,800 s (batch 6) and 14,400 s (batch 7) raised conversion from 0.629 to 0.784 to 0.879 and yield from 0.617 to 0.756 to 0.836. Selectivity remained high at 0.964, 0.958, and 0.952. In contrast, faradaic efficiency declined from 0.683 to 0.583 to 0.468, transport efficiency from 0.709 to 0.558 to 0.471, and energy efficiency from 0.818 to 0.729 to 0.612. Scores therefore rose from 0.738 to 0.754 and then fell slightly to 0.749. This supports progressive substrate depletion, concentration polarization, growing transport resistance, or increasing parasitic charge consumption late in the run. It also explains why maximizing conversion alone does not maximize the balanced score.

Potential and time are coupled rather than independently monotonic. Batch 5 used S0/E1 at +0.7 V for 10,800 s. It reached conversion 0.785 and yield 0.705, close to the conversion of batch 6 at +1.0 V, but selectivity was lower at 0.898 versus 0.958. Its score was 0.719 rather than 0.754. The lower potential therefore did not simply preserve selectivity; in this material combination, +1.0 V appears closer to the selective interfacial window.

Material effects and couplings

The nominal material dossier suggested that conductivity, diffusivity, diffusion-layer thickness, proton activity, solubility product, capacitance, and potential shifts could all matter. The experiments show that no single nominal descriptor ranks performance.

E1 with S0 was the strongest of the S0 combinations tested. At +1.0 V, 500 mA, and 10,800 s, batch 6 scored 0.754. E2 under the same settings in batch 10 scored 0.724, with conversion 0.794, selectivity 0.901, yield 0.684, faradaic efficiency 0.565, transport efficiency 0.567, ohmic efficiency 0.832, and energy efficiency 0.758. E2 eliminated the measured precipitation signal, whereas E1/S0 showed a precipitation signal near 0.85. Nevertheless, removal of precipitation did not compensate for E2's lower target selectivity and yield. Precipitation is therefore not itself the score-controlling variable in this tested range; it may be a correlated consequence or a secondary transport influence.

Batch 9 tested S0/E0 at +1.0 V, 500 mA, and 10,800 s. Despite E0's high nominal conductivity, it produced conversion 0.155, yield 0.147, faradaic efficiency 0.117, transport efficiency 0.138, and score 0.307. Its ohmic efficiency remained 0.919 and precipitation signal saturated at 1.0. This separates bulk ohmic conduction from productive interfacial and mass-transport chemistry: a conductive medium can still have poor faradaic use and poor substrate transport.

Batch 8 used S0/E3 at +0.72 V, 500 mA, and 10,800 s. This voltage was chosen as a shift-adjusted extrapolation from E1, but it yielded conversion 0.158, yield 0.107, faradaic efficiency 0.124, transport efficiency 0.118, and score 0.290. The failure shows that nominal standard-potential shifts are insufficient to transfer an optimum between electrolyte profiles. It does not establish that E3 is intrinsically poor, because E3 was not tested at +1.0 V or across a local potential series. Hidden electrolyte-specific kinetics, solvent coupling, or an incorrect shift-adjustment assumption remain plausible.

The best material combination was S1/E1. Batch 11 used +1.1 V, 500 mA, and 10,800 s and gave the campaign-best score, 0.795. Its final assay reported conversion 0.851, selectivity 0.981, yield 0.831, faradaic efficiency 0.601, transport efficiency 0.608, ohmic efficiency 0.837, and energy efficiency 0.755. The precipitation signal fell to 0.664 from approximately 0.848 for S0/E1 in batch 6. Relative to batch 6, S1/E1 improved conversion, yield, selectivity, and transport, while modestly lowering ohmic efficiency. This is qualitatively consistent with S1's higher nominal diffusivity and greater relative solubility product but lower conductivity. However, solvent and potential changed together (+1.0 to +1.1 V), so the campaign does not identify how much of the improvement came from S1 itself versus the 0.1 V adjustment or their interaction.

Batch 12 repeated the S1/E1, +1.1 V, 500 mA condition but extended electrolysis from 10,800 to 12,000 s. Conversion stayed almost unchanged (0.8512 to 0.8517), while yield increased from 0.831 to 0.871. Selectivity remained high but declined from 0.981 to 0.973. Faradaic efficiency fell from 0.601 to 0.524, transport efficiency from 0.608 to 0.546, and energy efficiency from 0.755 to 0.683; score fell to 0.780. This suggests that the reaction was already near its accessible conversion plateau by 10,800 s and that later charge primarily improved product accumulation or assay-level yield at an unfavorable efficiency cost. Because these are unreplicated batches, the small conversion difference should not be interpreted literally, but the coordinated declines across several efficiency channels support a real late-time penalty.

Acid/base and precipitation behavior

Final pH-normalized values depended strongly on electrolyte but varied little with duration within a material pair. S0/E1 batches were around 0.20; S0/E2 was 0.151; S0/E0 was 0.229; and S0/E3 was 0.272. This is consistent with electrolyte-controlled acid speciation rather than electrolysis time being the dominant pH determinant under the tested conditions. Precipitation also tracked the material pairing: high for S0/E1 and S0/E0, absent for S0/E2, near zero for S0/E3, and intermediate for S1/E1. These observations support coupling among proton activity, salt solubility, and transport, but the data do not show that either pH or precipitation directly causes selectivity changes.

Interpretation of the balanced optimum

The public score rewards yield most strongly while also rewarding conversion, selectivity, and the four efficiency components. The observed optimum is consequently a compromise, not the maximum of any single response. Batch 7 had higher yield than batch 6 but a slightly lower score because its efficiency losses outweighed the yield gain. Batch 12 likewise had higher yield than batch 11 but a lower score. Batch 1 had the best efficiency components but inadequate conversion and yield. This pattern is exactly what the proposed activation/charge/loss model predicts: early operation is efficient but incomplete; an intermediate charge reaches high product formation while preserving useful-current fractions; excessive duration or potential increases loss channels.

Recommended mechanistic operating region

The best directly observed recipe was batch 11: 0.020 mol reagent, 0.050 L S1, electrolyte E1, +1.1 V, 500 mA cap, and 10,800 s. The evidence supports a local optimum around positive 1.0–1.1 V and approximately 10–11 ks for E1, with the exact voltage depending on solvent. This region is an observation-based interpolation only. A narrower optimum near +1.05 to +1.15 V and 9–11 ks is plausible, but was not experimentally mapped and is therefore conjectural.

Unidentifiable factors and plausible alternatives

The campaign contains no direct measurement of actual current versus time, total charge passed, electrode potential after iR drop, temperature trajectory, electrode surface state, product/byproduct identity, or concentration profiles. Thus kinetic limitation, current-cap limitation, mass-transfer limitation, passivation, and substrate depletion cannot be quantitatively separated. The high-potential collapse might represent solvent/electrolyte decomposition, product destruction, electrode passivation, or a benchmark-specific selectivity switch. The late-time efficiency decline might arise from depletion, rising resistance, product re-electrolysis, precipitation, or accumulated side products.

Material comparisons are partly confounded by potential selection. In particular, E3 was evaluated at +0.72 V rather than in a full voltage sweep, and S1 was evaluated at +1.1 V while the closest S0 benchmark used +1.0 V. Nominal property shifts did not reliably predict the optimum, implying important hidden, fixed world-specific transport, solvation, or interfacial residuals. These factors cannot be inferred uniquely from 12 experiments.

No conditions were replicated exactly. Final-assay noise is small relative to several large contrasts, such as polarity and the +1.5 V collapse, but small differences such as scores 0.754 versus 0.749 are not strong evidence for a precisely located optimum. The report therefore supports the qualitative mechanism and batch-11 recommendation while leaving detailed rate constants, transfer coefficients, reaction order, electron stoichiometry, and causal material contributions unidentified.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific prior or quantitative response law was supplied. The only prior information was the nominal material dossier and the public scoring/instrument contracts; the dossier explicitly warned that hidden, fixed residuals and solvent–electrolyte couplings could override nominal rankings.

My self-developed claim that performance should peak at an intermediate potential and electrolysis duration was supported. Batch 1 was efficient but charge-limited at +1.0 V, 100 mA, and 3,600 s, whereas batches 2, 6, and 7 showed that longer operation increased yield but progressively reduced faradaic, transport, and energy efficiency. Their scores rose from 0.738 at 7,200 s to 0.754 at 10,800 s, then declined to 0.749 at 14,400 s. Batch 4 changed my judgment most strongly about potential: increasing from +1.0 V in batch 2 to +1.5 V under otherwise matched conditions collapsed the score from 0.738 to 0.003. This contradicted any monotonic “more positive potential gives more conversion” law and established a narrow productive window.

The claim that positive polarity is favored was supported by the matched comparison of batches 2 and 3. At ±1.0 V with S0/E1, 500 mA, and 7,200 s, the positive batch scored 0.738 versus 0.383 for the negative batch and was superior in yield, selectivity, and all reported non-ohmic efficiencies.

A simple charge-limited model was supported qualitatively by batch 1: its conversion and yield were low while its faradaic, transport, ohmic, and energy efficiencies were high. The coordinated efficiency losses at longer times in batches 6 and 7 support an additional depletion, polarization, or overprocessing term. The experiments did not identify which of those processes dominates.

The nominal-property claim that high bulk conductivity alone should produce the best electrolyte was contradicted. E0 has high nominal conductivity, yet batch 9 produced only a 0.307 score, faradaic efficiency 0.117, and transport efficiency 0.138 despite ohmic efficiency 0.919. Thus productive interfacial kinetics and mass transport were separable from bulk ohmic performance.

My attempt to transfer the E1 optimum to E3 using nominal standard-potential shifts was contradicted or at least unsupported. Shift-adjusted batch 8 at +0.72 V scored only 0.290. Because E3 was not tested across a voltage series, this result rejects the simple shift-only transfer rule, not E3 under all conditions.

The idea that precipitation must be the dominant performance penalty was not supported. Batch 10 had essentially no precipitation signal but scored below batch 6, whose precipitation signal was about 0.85. Conversely, changing from S0/E1 in batch 6 to S1/E1 in batch 11 reduced precipitation and improved several outcomes, but solvent and potential changed together. A direct causal role for precipitation therefore remained untested.

The supplied nominal suggestions concerning diffusivity, conductivity, proton activity, capacitance, and solubility were only partially tested. Batch 11 was qualitatively consistent with S1 improving transport at some cost to ohmic efficiency, but the design could not isolate solvent properties from the +0.1 V potential change. Exact kinetic laws, electron stoichiometry, reaction order, actual current, electrode passivation, and product re-electrolysis remained untested.

2. Most informative additional experiment

I would run one new batch at the batch-11 composition and potential—0.020 mol reagent, 0.050 L S1, E1, and +1.1 V—but use a 375 mA current cap for 14,400 s. This has the same nominal current–time product as 500 mA for 10,800 s, allowing comparison with batch 11 while changing current density and elapsed time.

My leading explanation is that the late efficiency decline is substantially caused by high-current concentration polarization and transport limitation. The main alternative is that performance is controlled chiefly by cumulative charge or by time-dependent depletion, product destruction, or passivation.

If the proposed lower-current batch retained approximately the conversion and yield of batch 11 while increasing transport, faradaic, and energy efficiency, I would strengthen the concentration-polarization explanation and infer that the 500 mA cap is too aggressive. If it reproduced batch 11 across both product and efficiency metrics, I would favor a primarily charge-controlled description. If it gave lower conversion despite the same nominal charge, I would infer that the configured cap is not equivalent to delivered charge or that the productive rate has a nonlinear current dependence. If yield or efficiency deteriorated mainly because of the longer elapsed time, I would strengthen the alternatives involving passivation, product re-electrolysis, or time-dependent degradation. A single final assay would still not uniquely separate those latter alternatives, but it would distinguish current-density sensitivity from a simple charge-only law.

3. Unused evidence, reliability, and goal effects

I did not inspect or model the raw UV–vis spectra or final-assay signal artifacts; I used their processed estimates. The intermediate UV–vis readings were used mainly as diagnostics and were not fitted quantitatively. No pH-meter measurements were taken, so acid/base behavior was inferred only from final-assay pH-normalized values and the nominal dossier. Cost and safety observations were recorded but supplied little mechanistic discrimination because safety remained well below the limit across the tested campaign.

Large portions of the design space were unused: S3 was never tested, S2 was not tested experimentally, most solvent–electrolyte combinations were absent, E3 received only one shift-adjusted voltage, reagent concentration and volume were held fixed, and no condition was exactly replicated. Actual current, total delivered charge, temperature history, electrode state, and product/byproduct identity were unavailable.

The least reliable blind predictions are those for S2 (Q09–Q10), because that solvent was never used, and those for E0 at +0.8 V (especially Q12), because batch 9 showed that the potential response can be sharply nonlinear and E0 had no local voltage series. E3 predictions (Q07–Q08) are also weak because batch 8 confounded electrolyte identity with an unvalidated voltage adjustment. The 600 s predictions (Q01–Q02) are sensitive to the selective-yield score gate, so a small yield error can cause a disproportionately large score error. High-current extrapolations at the new concentration are likewise uncertain.

The batch-11 recommendation is reliable as the best observed batch, but less reliable as a precisely optimized universal procedure. It was not replicated, the nearby potential range was not mapped, and its advantage over batch 12 partly reflects the balanced score’s efficiency weights. Attribution of its improvement specifically to S1 is weaker than the empirical recommendation because batch 11 also used a different potential from the closest S0 benchmark.

The assigned goal did affect evidence collection. Maximizing the balanced score encouraged exploitation around the promising E1 region and the use of all final assays on complete batches. That improved confidence in the operating recommendation but reduced factorial coverage, replication, and causal identification of individual material properties. I found no clear conflict between the score objective and safety evidence because observed risks remained low; the main conflict was optimization versus mechanistic identifiability.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.45,
        "lower80": 0.2,
        "upper80": 0.7
      },
      "energy_efficiency": {
        "estimate": 0.3,
        "lower80": 0.1,
        "upper80": 0.55
      },
      "faradaic_efficiency": {
        "estimate": 0.3,
        "lower80": 0.12,
        "upper80": 0.55
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.05,
        "lower80": 0.005,
        "upper80": 0.18
      },
      "selective_product_yield": {
        "estimate": 0.003,
        "lower80": 0.0002,
        "upper80": 0.012
      },
      "transport_efficiency": {
        "estimate": 0.55,
        "lower80": 0.3,
        "upper80": 0.78
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.85,
        "lower80": 0.68,
        "upper80": 0.96
      },
      "energy_efficiency": {
        "estimate": 0.75,
        "lower80": 0.5,
        "upper80": 0.9
      },
      "faradaic_efficiency": {
        "estimate": 0.78,
        "lower80": 0.55,
        "upper80": 0.93
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.5,
        "lower80": 0.25,
        "upper80": 0.68
      },
      "selective_product_yield": {
        "estimate": 0.018,
        "lower80": 0.008,
        "upper80": 0.03
      },
      "transport_efficiency": {
        "estimate": 0.75,
        "lower80": 0.52,
        "upper80": 0.9
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.35,
        "upper80": 0.75
      },
      "energy_efficiency": {
        "estimate": 0.28,
        "lower80": 0.13,
        "upper80": 0.46
      },
      "faradaic_efficiency": {
        "estimate": 0.28,
        "lower80": 0.14,
        "upper80": 0.47
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.31,
        "lower80": 0.18,
        "upper80": 0.45
      },
      "selective_product_yield": {
        "estimate": 0.045,
        "lower80": 0.02,
        "upper80": 0.09
      },
      "transport_efficiency": {
        "estimate": 0.45,
        "lower80": 0.27,
        "upper80": 0.64
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.86,
        "lower80": 0.73,
        "upper80": 0.95
      },
      "energy_efficiency": {
        "estimate": 0.72,
        "lower80": 0.54,
        "upper80": 0.86
      },
      "faradaic_efficiency": {
        "estimate": 0.7,
        "lower80": 0.5,
        "upper80": 0.86
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.56,
        "lower80": 0.43,
        "upper80": 0.68
      },
      "selective_product_yield": {
        "estimate": 0.18,
        "lower80": 0.1,
        "upper80": 0.27
      },
      "transport_efficiency": {
        "estimate": 0.68,
        "lower80": 0.48,
        "upper80": 0.84
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.65,
        "lower80": 0.47,
        "upper80": 0.8
      },
      "energy_efficiency": {
        "estimate": 0.45,
        "lower80": 0.29,
        "upper80": 0.62
      },
      "faradaic_efficiency": {
        "estimate": 0.5,
        "lower80": 0.33,
        "upper80": 0.68
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.42,
        "lower80": 0.3,
        "upper80": 0.54
      },
      "selective_product_yield": {
        "estimate": 0.105,
        "lower80": 0.055,
        "upper80": 0.17
      },
      "transport_efficiency": {
        "estimate": 0.55,
        "lower80": 0.37,
        "upper80": 0.71
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.93,
        "lower80": 0.83,
        "upper80": 0.985
      },
      "energy_efficiency": {
        "estimate": 0.84,
        "lower80": 0.7,
        "upper80": 0.93
      },
      "faradaic_efficiency": {
        "estimate": 0.86,
        "lower80": 0.72,
        "upper80": 0.95
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.63,
        "lower80": 0.52,
        "upper80": 0.72
      },
      "selective_product_yield": {
        "estimate": 0.245,
        "lower80": 0.16,
        "upper80": 0.32
      },
      "transport_efficiency": {
        "estimate": 0.83,
        "lower80": 0.67,
        "upper80": 0.92
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.38,
        "upper80": 0.76
      },
      "energy_efficiency": {
        "estimate": 0.32,
        "lower80": 0.16,
        "upper80": 0.5
      },
      "faradaic_efficiency": {
        "estimate": 0.36,
        "lower80": 0.2,
        "upper80": 0.55
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.34,
        "lower80": 0.21,
        "upper80": 0.47
      },
      "selective_product_yield": {
        "estimate": 0.065,
        "lower80": 0.028,
        "upper80": 0.12
      },
      "transport_efficiency": {
        "estimate": 0.43,
        "lower80": 0.25,
        "upper80": 0.62
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.82,
        "lower80": 0.66,
        "upper80": 0.93
      },
      "energy_efficiency": {
        "estimate": 0.58,
        "lower80": 0.39,
        "upper80": 0.75
      },
      "faradaic_efficiency": {
        "estimate": 0.55,
        "lower80": 0.36,
        "upper80": 0.73
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.48,
        "lower80": 0.34,
        "upper80": 0.61
      },
      "selective_product_yield": {
        "estimate": 0.14,
        "lower80": 0.07,
        "upper80": 0.22
      },
      "transport_efficiency": {
        "estimate": 0.58,
        "lower80": 0.39,
        "upper80": 0.75
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.52,
        "lower80": 0.3,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.24,
        "lower80": 0.1,
        "upper80": 0.43
      },
      "faradaic_efficiency": {
        "estimate": 0.25,
        "lower80": 0.1,
        "upper80": 0.45
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.27,
        "lower80": 0.13,
        "upper80": 0.41
      },
      "selective_product_yield": {
        "estimate": 0.035,
        "lower80": 0.012,
        "upper80": 0.08
      },
      "transport_efficiency": {
        "estimate": 0.38,
        "lower80": 0.19,
        "upper80": 0.58
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.84,
        "lower80": 0.67,
        "upper80": 0.95
      },
      "energy_efficiency": {
        "estimate": 0.56,
        "lower80": 0.36,
        "upper80": 0.74
      },
      "faradaic_efficiency": {
        "estimate": 0.5,
        "lower80": 0.3,
        "upper80": 0.7
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.46,
        "lower80": 0.3,
        "upper80": 0.6
      },
      "selective_product_yield": {
        "estimate": 0.12,
        "lower80": 0.05,
        "upper80": 0.21
      },
      "transport_efficiency": {
        "estimate": 0.52,
        "lower80": 0.32,
        "upper80": 0.71
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.5,
        "lower80": 0.28,
        "upper80": 0.7
      },
      "energy_efficiency": {
        "estimate": 0.18,
        "lower80": 0.06,
        "upper80": 0.36
      },
      "faradaic_efficiency": {
        "estimate": 0.2,
        "lower80": 0.07,
        "upper80": 0.4
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.3,
        "lower80": 0.16,
        "upper80": 0.44
      },
      "selective_product_yield": {
        "estimate": 0.11,
        "lower80": 0.04,
        "upper80": 0.21
      },
      "transport_efficiency": {
        "estimate": 0.25,
        "lower80": 0.09,
        "upper80": 0.46
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.86,
        "lower80": 0.7,
        "upper80": 0.95
      },
      "energy_efficiency": {
        "estimate": 0.5,
        "lower80": 0.3,
        "upper80": 0.69
      },
      "faradaic_efficiency": {
        "estimate": 0.38,
        "lower80": 0.2,
        "upper80": 0.59
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.56,
        "lower80": 0.39,
        "upper80": 0.7
      },
      "selective_product_yield": {
        "estimate": 0.47,
        "lower80": 0.27,
        "upper80": 0.66
      },
      "transport_efficiency": {
        "estimate": 0.4,
        "lower80": 0.21,
        "upper80": 0.61
      }
    }
  ],
  "rationale": "Predictions extrapolate the campaign’s positive-polarity advantage, narrow productive potential window, approximate two-electron charge limitation at short duration, and efficiency losses at high current or prolonged electrolysis. E1 is assigned the strongest positive-polarity performance; E0 at +0.8 V is treated as better than the tested overdriven +1.0 V case but remains uncertain, while E3 and untested S2 receive wider intervals. The very short batches may fall near the score’s yield gate. Intervals include assay noise plus substantial model uncertainty from the new concentration, unreplicated material effects, and absent local voltage sweeps."
}
```
