# repeat-01/EC-W02-B12-optimization-E-MisIndexed

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-01\EC-W02-B12-optimization-E-MisIndexed\participant\optimization-E-MisIndexed

## 同期笔记

### v1 · 公开事件 0

# Electrochemical campaign hypotheses

## H1 [tentative]
At fixed loading, balanced score should peak at an intermediate overpotential and electrolysis duration: insufficient drive limits conversion, while excessive drive/time lowers selectivity and energy efficiency. Test by spanning potential sign/magnitude, current cap, and duration.

## H2 [tentative]
High-conductivity media should improve ohmic efficiency, but transport and precipitation may offset this. E3/S0 are prior candidates for conductivity; E0 has thin diffusion layer; E2 carries the strongest precipitation concern. Comparisons will treat final assays as authoritative.

## Planned decision rule
Use broad material and operating-condition screening first, then spend later batches near the best observed score. Change the recommendation if a later batch has a clearly higher public score rather than merely a small noisy component difference.

### v2 · 公开事件 85

# Electrochemical campaign hypotheses

## H1 [supported in tested scope]
Positive polarization is productive and negative polarization is not under matched S0/E0, 100 mA-cap, 1800 s conditions. Batch 1 (+1.0 V) scored 0.567 versus batch 2 (-1.0 V) 0.284 (final-assay events runner-operation-0007 and -0014). This is a numerical and practically large difference relative to the stated assay noise, though it does not establish behavior at every material or magnitude.

## H2 [supported with qualifications]
At +1.0 V in S0, electrolyte E1 was the best tested 7200 s profile: score 0.621 (runner-operation-0035), versus E0 0.593 (-0028), E2 0.564 (-0042), and E3 0.510 (-0021). E1 combined high selectivity/efficiency with moderate precipitation; precipitation signal alone did not rank score. Solvent S0 also exceeded S1–S3 in the tested E1 comparison (events -0035, -0049, -0056, -0063), but each condition has only one final assay.

## H3 [supported in a narrow operating region]
For E1/S0 at +1.0 V and 100 mA cap, longer electrolysis increased conversion and selective yield without a large efficiency collapse: 7200 s scored 0.621 (-0035), 14400 s scored 0.691 (-0070), and two 14400 s segments scored 0.840 (-0085). The 28800 s result had conversion 0.691, selective yield 0.693, selectivity 0.948, and strong efficiency components. A separate +1.5 V/14400 s batch collapsed to score 0.0067 (-0077), supporting a sharp high-potential side-reaction/transport failure alternative rather than monotonic voltage benefit.

## Recommendation decision
Select batch 12 (E1/S0, 0.02 mol in 0.05 L, +1.0 V, 100 mA cap, 2×14400 s). It has the highest observed score by a wide margin. This recommendation would change if repeat assays showed the gain was not reproducible, or if still-longer electrolysis revealed degradation/efficiency loss; neither was tested.

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
    "cost": 0.28571999073028564,
    "electrochemical_conversion": 0.05233539268374443,
    "electrochemical_selectivity": 0.8980063199996948,
    "energy_efficiency": 0.8702253699302673,
    "faradaic_efficiency": 0.9748222827911377,
    "ohmic_efficiency": 0.9653005003929138,
    "pH_normalized": 0.22897005081176758,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.5668513178825378,
    "selective_product_yield": 0.02522830292582512,
    "transport_efficiency": 0.9461185336112976
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
    "cost": 0.28571999073028564,
    "electrochemical_conversion": 0.009975438006222248,
    "electrochemical_selectivity": 0.5760180354118347,
    "energy_efficiency": 0.25159168243408203,
    "faradaic_efficiency": 0.38621339201927185,
    "ohmic_efficiency": 0.9741383194923401,
    "pH_normalized": 0.22627469897270203,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.28424787521362305,
    "selective_product_yield": 0.019178958609700203,
    "transport_efficiency": 0.4124701917171478
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
    "cost": 0.287880003452301,
    "electrochemical_conversion": 0.1132374256849289,
    "electrochemical_selectivity": 0.8663612008094788,
    "energy_efficiency": 0.8524199724197388,
    "faradaic_efficiency": 0.6090919971466064,
    "ohmic_efficiency": 0.9626166820526123,
    "pH_normalized": 0.2695680558681488,
    "precipitation_signal": 0.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.5099034309387207,
    "selective_product_yield": 0.0936574637889862,
    "transport_efficiency": 0.6256489157676697
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
    "electrochemical_conversion": 0.1641889214515686,
    "electrochemical_selectivity": 0.858977198600769,
    "energy_efficiency": 0.8256116509437561,
    "faradaic_efficiency": 0.9286320805549622,
    "ohmic_efficiency": 0.9730700850486755,
    "pH_normalized": 0.22629910707473755,
    "precipitation_signal": 0.987893283367157,
    "safety_risk": 0.05933958664536476,
    "score": 0.5930706262588501,
    "selective_product_yield": 0.1498916745185852,
    "transport_efficiency": 0.8971445560455322
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
    "cost": 0.287880003452301,
    "electrochemical_conversion": 0.1722317337989807,
    "electrochemical_selectivity": 0.9493215680122375,
    "energy_efficiency": 0.885606586933136,
    "faradaic_efficiency": 0.9157494306564331,
    "ohmic_efficiency": 0.9668999314308167,
    "pH_normalized": 0.20622022449970245,
    "precipitation_signal": 0.8436887264251709,
    "safety_risk": 0.05933958664536476,
    "score": 0.6205107569694519,
    "selective_product_yield": 0.16760818660259247,
    "transport_efficiency": 0.905239999294281
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
    "electrochemical_conversion": 0.1525459885597229,
    "electrochemical_selectivity": 0.8565728068351746,
    "energy_efficiency": 0.8139064908027649,
    "faradaic_efficiency": 0.8302167057991028,
    "ohmic_efficiency": 0.9610520005226135,
    "pH_normalized": 0.15415410697460175,
    "precipitation_signal": 0.0023995577357709408,
    "safety_risk": 0.05933958664536476,
    "score": 0.5644469857215881,
    "selective_product_yield": 0.13852322101593018,
    "transport_efficiency": 0.8055333495140076
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
    "electrochemical_conversion": 0.16197986900806427,
    "electrochemical_selectivity": 0.8997887969017029,
    "energy_efficiency": 0.8619518280029297,
    "faradaic_efficiency": 0.8149211406707764,
    "ohmic_efficiency": 0.9870655536651611,
    "pH_normalized": 0.20691271126270294,
    "precipitation_signal": 0.6940808892250061,
    "safety_risk": 0.08273958414793015,
    "score": 0.5822628736495972,
    "selective_product_yield": 0.14405281841754913,
    "transport_efficiency": 0.8183215260505676
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
      "solvent": 2,
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
    "cost": 0.33987998962402344,
    "electrochemical_conversion": 0.1426004022359848,
    "electrochemical_selectivity": 0.9112278819084167,
    "energy_efficiency": 0.8563686609268188,
    "faradaic_efficiency": 0.7992904782295227,
    "ohmic_efficiency": 0.9559306502342224,
    "pH_normalized": 0.22195850312709808,
    "precipitation_signal": 0.5080054402351379,
    "safety_risk": 0.10073958337306976,
    "score": 0.5654159188270569,
    "selective_product_yield": 0.11449197679758072,
    "transport_efficiency": 0.7927951216697693
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
      "solvent": 3,
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
    "cost": 0.31988000869750977,
    "electrochemical_conversion": 0.1503799557685852,
    "electrochemical_selectivity": 0.8897917866706848,
    "energy_efficiency": 0.8999853134155273,
    "faradaic_efficiency": 0.8076202273368835,
    "ohmic_efficiency": 0.9958652853965759,
    "pH_normalized": 0.21261118352413177,
    "precipitation_signal": 0.611060380935669,
    "safety_risk": 0.11333958804607391,
    "score": 0.5891692042350769,
    "selective_product_yield": 0.15411946177482605,
    "transport_efficiency": 0.8284514546394348
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
    "cost": 0.29076001048088074,
    "electrochemical_conversion": 0.3529353737831116,
    "electrochemical_selectivity": 0.9619195461273193,
    "energy_efficiency": 0.9281471371650696,
    "faradaic_efficiency": 0.9137532114982605,
    "ohmic_efficiency": 0.958005964756012,
    "pH_normalized": 0.19996103644371033,
    "precipitation_signal": 0.8492700457572937,
    "safety_risk": 0.05933958664536476,
    "score": 0.6913589835166931,
    "selective_product_yield": 0.3158477246761322,
    "transport_efficiency": 0.9151028394699097
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
      "potential_V": 1.5
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
    "cost": 0.29363998770713806,
    "electrochemical_conversion": 0.013452183455228806,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.012963879853487015,
    "faradaic_efficiency": 0.002204522956162691,
    "ohmic_efficiency": 0.9818722605705261,
    "pH_normalized": 0.20094606280326843,
    "precipitation_signal": 0.8571591973304749,
    "safety_risk": 0.05933958664536476,
    "score": 0.0066647096537053585,
    "selective_product_yield": 0.0015959294978529215,
    "transport_efficiency": 0.009384461678564548
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
      "duration_s": 14400,
      "operation": "electrolyze"
    },
    {
      "instrument": "uvvis",
      "operation": "measure"
    },
    {
      "duration_s": 14400,
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
    "cost": 0.314520001411438,
    "electrochemical_conversion": 0.6912023425102234,
    "electrochemical_selectivity": 0.9482660889625549,
    "energy_efficiency": 0.9259930849075317,
    "faradaic_efficiency": 0.9132503271102905,
    "ohmic_efficiency": 0.9848328232765198,
    "pH_normalized": 0.20144827663898468,
    "precipitation_signal": 0.8506432175636292,
    "safety_risk": 0.05933958664536476,
    "score": 0.8400890231132507,
    "selective_product_yield": 0.6933524012565613,
    "transport_efficiency": 0.934475302696228
  }
}
```

## K1 封存报告

Mechanism report

1. Empirical picture

The system behaves like a polarity-specific electrochemical conversion with a useful positive-potential window, charge/time-limited conversion inside that window, and a severe failure mode at excessive positive potential. Medium choice affects several partially independent factors: interfacial selectivity, Faradaic efficiency, mass transport, ohmic loss, acid state, and precipitation. The best observed condition was not simply the most conductive or least precipitating medium.

All batches used 0.020 mol reagent in 0.050 L solvent, a configured 100 mA current cap, and the stated potential. Thus concentration, current cap, and volume were not independently identified. Final-assay values below are observations, subject to the published channel-specific noise.

2. Potential polarity and electrochemical window

Batches 1 and 2 provide the clearest polarity comparison. Both used solvent S0, electrolyte E0, 100 mA, and 1800 s. At +1.0 V, batch 1 gave score 0.5669, conversion 0.0523, selectivity 0.8980, selective yield 0.0252, Faradaic efficiency 0.9748, transport efficiency 0.9461, and energy efficiency 0.8702. At -1.0 V, batch 2 fell to score 0.2842, conversion 0.0100, selectivity 0.5760, Faradaic efficiency 0.3862, transport efficiency 0.4125, and energy efficiency 0.2516. This supports a productive electrode process under positive polarization; reversing polarity directs charge into other processes or fails to activate the desired transformation.

Potential magnitude is strongly non-monotonic. With the otherwise favorable E1/S0 medium and 14400 s duration, batch 10 at +1.0 V scored 0.6914, whereas batch 11 at +1.5 V scored only 0.00666. Batch 11 had conversion 0.0135, selectivity reported as 0, selective yield 0.00160, Faradaic efficiency 0.00220, transport efficiency 0.00938, and energy efficiency 0.01296, while ohmic efficiency remained high at 0.9819. Therefore, the +1.5 V failure is unlikely to be primarily bulk resistance. A plausible interpretation is that +1.5 V crosses an interfacial electrochemical window: parasitic electron transfer, electrode blocking, depletion near the interface, or formation of an unobserved side product consumes the applied drive. This interpretation is mechanistic conjecture; the campaign did not directly identify the side reaction.

The precise boundary is unresolved because no potentials between +1.0 and +1.5 V were tested. It is therefore justified to call +1.0 V productive and +1.5 V destructive under E1/S0, but not to claim that +1.0 V is the exact optimum.

3. Time dependence and conversion

At fixed E1/S0, +1.0 V, and 100 mA cap, duration was the dominant controllable variable in the tested productive region:

- Batch 5, 7200 s: conversion 0.1722, selective yield 0.1676, selectivity 0.9493, score 0.6205.
- Batch 10, 14400 s: conversion 0.3529, selective yield 0.3158, selectivity 0.9619, score 0.6914.
- Batch 12, two consecutive 14400 s periods, 28800 s total: conversion 0.6912, selective yield 0.6934, selectivity 0.9483, score 0.8401.

Conversion increased approximately in proportion to elapsed electrolysis time over this range, with no observed approach to a low conversion plateau. Meanwhile, the efficiency components remained high: batch 12 had Faradaic efficiency 0.9133, transport efficiency 0.9345, ohmic efficiency 0.9848, and energy efficiency 0.9260. This suggests a charge- or time-limited productive process at +1.0 V, rather than rapid equilibrium followed by degradation.

A minimal phenomenological model would be

  dX/dt = k_eff(V,S,E,C,I_cap,state) * (1-X)^n,

  Y_sel approximately X * S_product,

where X is conversion and S_product is product selectivity. Over the observed range, a nearly linear approximation X approximately k_app*t is adequate, but a saturating law such as X = 1-exp(-k_app*t) remains plausible outside the measured range. Batch 12 does not prove that still longer operation would continue improving the score; substrate depletion, product oxidation, heating, or electrode fouling could eventually dominate.

Batch 12 included a UV-vis measurement after its first 14400 s segment before the second segment. Its sample consumption was small relative to 0.050 L, but this makes it not perfectly identical to a hypothetical uninterrupted 28800 s run.

4. Electrolyte effects

Batches 3-6 compared all electrolyte profiles in S0 at +1.0 V, 100 mA, and 7200 s:

- E0, batch 4: score 0.5931; conversion 0.1642; selectivity 0.8590; Faradaic/transport efficiencies 0.9286/0.8971; precipitation signal 0.9879.
- E1, batch 5: score 0.6205; conversion 0.1722; selectivity 0.9493; Faradaic/transport efficiencies 0.9157/0.9052; precipitation 0.8437.
- E2, batch 6: score 0.5644; conversion 0.1525; selectivity 0.8566; Faradaic/transport efficiencies 0.8302/0.8055; precipitation 0.0024.
- E3, batch 3: score 0.5099; conversion 0.1132; selectivity 0.8664; Faradaic/transport efficiencies 0.6091/0.6256; precipitation 0.

E1 was the best tested compromise. It did not maximize every isolated property, but it combined the highest conversion and selectivity with strong transport, Faradaic, energy, and ohmic performance. E0 retained excellent charge efficiency but had lower selectivity. E2 and E3 demonstrated that suppressing precipitation alone does not maximize the balanced objective.

The nominal dossier offers plausible causes: electrolyte conductivity, diffusivity, diffusion-layer thickness, acid concentration/pKa, supporting-electrolyte concentration, double-layer capacitance, precipitation tendency, and standard-potential shift can all alter the effective interfacial overpotential and mass-transfer rate. For example, the low precipitation observed for E2 and E3 is qualitatively consistent with their nominal salt/solubility properties. However, the dossier explicitly allows hidden, fixed world residuals and solvent coupling, so these nominal properties cannot uniquely explain the rankings.

5. Solvent effects

Batches 5 and 7-9 compared solvents with E1 at +1.0 V, 100 mA, and 7200 s:

- S0, batch 5: score 0.6205; conversion 0.1722; selectivity 0.9493; selective yield 0.1676.
- S1, batch 7: score 0.5823; conversion 0.1620; selectivity 0.8998; yield 0.1441.
- S2, batch 8: score 0.5654; conversion 0.1426; selectivity 0.9112; yield 0.1145.
- S3, batch 9: score 0.5892; conversion 0.1504; selectivity 0.8898; yield 0.1541.

S0 was best overall. S3 showed high energy and ohmic efficiency but did not match S0 in conversion, selectivity, or total score. S1 and S2 had lower Faradaic and transport efficiencies than S0. This is consistent with coupled roles for solvent conductivity, diffusivity, proton activity, double-layer capacitance, and potential shift. It also shows why a single descriptor is inadequate: nominally favorable diffusivity or solubility did not guarantee the best outcome.

Observed safety risk also depended on solvent: it was about 0.0593 for S0, 0.0827 for S1, 0.1007 for S2, and 0.1133 for S3 in these comparisons, all below the stated 0.65 limit. Thus S0 was favorable for both score and observed risk in this campaign.

6. Acid state and precipitation

Final normalized pH varied mainly with electrolyte and medium. Representative values were 0.2263 for E0/S0, 0.2062 for E1/S0, 0.1542 for E2/S0, and 0.2696 for E3/S0 at 7200 s. Within E1/S0, normalized pH was relatively stable across longer runs: 0.2062 at 7200 s, 0.2000 at 14400 s, and 0.2014 at 28800 s. This suggests that the large time-dependent conversion increase was not accompanied by a comparably large measured bulk acid-state shift.

Precipitation was not monotonic with performance. E1/S0 retained a high precipitation signal near 0.84-0.85 in batches 5, 10, and 12, yet produced the best scores. E2 and E3 nearly eliminated the signal but scored worse. Precipitation may still affect active area or transport, but in the tested domain it was not the limiting determinant of the balanced score. An alternative is that the precipitation channel detects a spectator solid with limited kinetic impact.

7. Score structure and why batch 12 won

For yields above the public 0.02 gate, the score is consistent with the published weighted sum:

  score = 0.30*selective_yield
        + 0.15*selectivity
        + 0.10*conversion
        + 0.15*energy_efficiency
        + 0.12*Faradaic_efficiency
        + 0.10*transport_efficiency
        + 0.08*ohmic_efficiency.

When selective yield is below 0.02, the multiplicative yield gate strongly suppresses the sum. This explains the extremely low score of batch 11 despite its high ohmic efficiency. Batch 12 won because its much larger conversion and selective yield were achieved without sacrificing selectivity or the efficiency terms; it did not win merely by maximizing one channel.

8. Integrated mechanistic hypothesis

A useful conceptual model is:

  effective overpotential = applied potential - medium-dependent formal potential - iR - interfacial polarization;

  productive current = total current * FE(V,S,E,state);

  reactant flux = min(diffusive supply, interfacial kinetic demand);

  product formation rate is proportional to productive current times product selectivity;

  parasitic rate rises sharply outside the productive potential window.

Electrolyte and solvent jointly determine conductivity, iR loss, reactant mobility, proton activity, double-layer structure, formal potential, precipitation, and interfacial selectivity. At E1/S0 and +1.0 V, these factors place the electrode in a broad productive regime: Faradaic and transport efficiencies remain near 0.9, and conversion accumulates with time. At negative potential, the desired electron-transfer direction is disfavored. At +1.5 V, a competing interfacial process appears to dominate, collapsing Faradaic and transport performance even though bulk ohmic efficiency remains high.

9. Scope and unidentifiable factors

This account is limited to one reagent loading, one initial volume, and one configured current cap. Actual current-time traces, passed charge, electrode potential after iR correction, electrode area, local temperature, stirring, concentration profiles, and identities of products or deposits were not observed. Therefore, kinetic constants, reaction order, electron stoichiometry, exchange current, diffusion coefficients in the realized world, and exact onset potential of the parasitic pathway are not identifiable.

There were no replicate final assays. Differences among singleton material conditions may contain process variation and assay noise. A few low-level estimates were not perfectly mass-action-consistent—for example, selective yield sometimes slightly exceeded the independently estimated conversion—so small discrepancies should not be interpreted mechanistically. Intermediate UV-vis estimates also had larger stated uncertainties than final-assay values and were used diagnostically rather than as the primary basis for ranking.

Material interactions were only partly crossed: electrolytes were compared in S0, and solvents were compared with E1. Consequently, strong solvent-electrolyte interactions could reverse rankings elsewhere. Duration dependence was established most clearly for E1/S0, not for every material pair. Only -1.0, +1.0, and one +1.5 V condition were informative, so the detailed voltage-response curve remains unknown.

Plausible alternatives to the proposed +1.5 V side-reaction explanation include rapid electrode passivation, local reactant depletion, a potential-dependent transport artifact, or a hidden medium-specific state transition. The available observations distinguish this failure from simple ohmic loss but do not distinguish among those interfacial alternatives.

Overall, the strongest evidence-supported statement is that this world rewards sustained electrolysis in a narrow positive-potential regime, with E1/S0 providing the best tested balance of interfacial selectivity, charge efficiency, transport, and risk. Batch 12 is the best observed realization, while behavior beyond 28800 s or between +1.0 and +1.5 V remains extrapolative.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific prior or previously observed outcome was supplied. The only starting information was the public scoring/instrument contract and the nominal material dossier, which explicitly warned that hidden world residuals and couplings could change material behavior.

My initial claim that useful performance would occur at an intermediate positive potential was supported, but only coarsely. Batch 1 at +1.0 V substantially outperformed the matched negative-polarity batch 2. More decisively, batch 10 at +1.0 V scored 0.6914, whereas batch 11 at +1.5 V scored 0.00666 with nearly zero Faradaic and transport efficiency. Batch 11 changed my judgment from expecting a smooth voltage optimum to expecting a sharp upper failure region. The exact optimum and threshold remain untested because no intermediate potentials between +1.0 and +1.5 V were run.

The expectation that high nominal conductivity would improve ohmic efficiency was only partly supported. Ohmic efficiency was generally high, but the nominally highly conductive E3 was not the best electrolyte: batch 3 scored 0.5099, versus 0.6205 for E1 in batch 5 under the same S0, +1.0 V, 7200 s conditions. Thus conductivity alone was contradicted as a sufficient ranking law. The broader claim that conductivity, transport, interfacial selectivity, and precipitation are coupled tradeoffs was supported by batches 3–6.

The possibility that precipitation would control performance was weakened. E2 and E3 nearly eliminated the precipitation signal in batches 6 and 3, yet both scored below E1 in batch 5, whose precipitation signal was about 0.844. This changed my view toward precipitation being secondary or possibly spectator-like in the tested domain. It was not proved harmless, because electrode deposits and active area were not directly observed.

The duration law was supported within E1/S0 at +1.0 V. Scores rose from 0.6205 at 7200 s in batch 5, to 0.6914 at 14400 s in batch 10, and 0.8401 at 28800 s in batch 12. Conversion and selective yield rose strongly while efficiency remained high. This supports a charge/time-limited productive regime over that interval. Saturation, degradation, or fouling beyond 28800 s remain untested.

The solvent ranking S0 > S3 ≈ S1 > S2 for balanced performance was supported only in the E1, +1.0 V, 7200 s slice represented by batches 5 and 7–9. It is not a universal solvent law because solvent-by-electrolyte interactions were not crossed.

The public weighted-score relationship was consistent with the final assays, including the severe selective-yield gate in batch 11. Current-cap effects, reaction order, concentration dependence, electron stoichiometry, the actual current-time response, and the detailed voltage-response curve were untested.

2. One discriminating experiment

I would run one recovery experiment in E1/S0 at the campaign loading and 100 mA cap: expose the cell briefly to +1.5 V, measure diagnostically, switch to +1.0 V for a substantial electrolysis period, measure again, then terminate and perform the final assay.

This would distinguish my leading explanation—a predominantly reversible, potential-dependent parasitic pathway above the useful electrochemical window—from the alternative of irreversible electrode passivation or persistent medium damage.

If performance recovered after switching to +1.0 V, with strong Faradaic/transport efficiency and renewed product formation, I would favor a reversible competition between desired and parasitic current at +1.5 V. If the cell remained inactive at +1.0 V after the +1.5 V exposure, I would shift toward irreversible passivation, stable inhibitor/degradation-product formation, or lasting precipitation at the interface. Partial recovery that depended on the +1.5 V exposure time would support a mixed model with both instantaneous current diversion and cumulative surface damage. A control at +1.0 V would be scientifically desirable, although batch 10 already provides a historical reference rather than a simultaneous replicate.

3. Unused evidence, reliability, and goal effects

The largest unused evidence source was the detailed raw characterization artifacts. I used processed final-assay estimates and the summarized intermediate UV-vis efficiencies, but did not analyze full spectra, baselines, peak shapes, or raw replicate signals. Intermediate UV-vis observations were used mainly as diagnostics and not fitted quantitatively. Cost, normalized pH, precipitation, and safety were inspected, but only partially incorporated because the assigned objective directly rewarded the electrochemical performance components. No dedicated pH-meter experiment was performed.

Several important variables were never observed: actual current, passed charge, local electrode potential after iR correction, temperature history, concentration gradients, deposit composition, electrode condition, and identities of side products. The nominal material properties were used qualitatively, not as a fitted quantitative model.

The least reliable predictions are the 600 s cases Q01–Q02 because selective yield lies near the 0.02 multiplicative gate and no campaign batch used such a short duration. The negative-potential predictions for untested electrolyte or solvent combinations—especially Q05, Q07, and Q09—are also weak. Q11–Q12 are uncertain because 500 mA was never tested; predicting little change assumes the fixed-potential cell remains below the current cap. All predictions additionally extrapolate from 0.020 mol in 0.050 L to 0.012 mol in 0.025 L and from ±1.0 V to ±0.8 V.

The batch-12 recommendation is reliable as the highest observed campaign score, but less reliable as a universally optimal procedure because there were no replicates, no finer potential scan, and no durations beyond 28800 s. Its reproducibility and proximity to the true optimum are unknown.

The assigned goal did affect evidence collection. Because the goal was to maximize score, I used early batches for broad screening and later batches to exploit E1/S0 and longer duration. This produced a strong recommendation but sacrificed replication, systematic current and concentration studies, a full factorial solvent-electrolyte design, and fine mapping of the +1.0 to +1.5 V transition. That is a real optimization-versus-identification tradeoff rather than evidence of a contradiction in the observed results.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.6,
        "lower80": 0.42,
        "upper80": 0.74
      },
      "energy_efficiency": {
        "estimate": 0.3,
        "lower80": 0.14,
        "upper80": 0.46
      },
      "faradaic_efficiency": {
        "estimate": 0.4,
        "lower80": 0.23,
        "upper80": 0.56
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.123,
        "lower80": 0.0,
        "upper80": 0.34
      },
      "selective_product_yield": {
        "estimate": 0.008,
        "lower80": 0.0,
        "upper80": 0.025
      },
      "transport_efficiency": {
        "estimate": 0.44,
        "lower80": 0.27,
        "upper80": 0.6
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.91,
        "lower80": 0.82,
        "upper80": 0.97
      },
      "energy_efficiency": {
        "estimate": 0.91,
        "lower80": 0.8,
        "upper80": 0.99
      },
      "faradaic_efficiency": {
        "estimate": 0.96,
        "lower80": 0.86,
        "upper80": 1.0
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.339,
        "lower80": 0.03,
        "upper80": 0.58
      },
      "selective_product_yield": {
        "estimate": 0.012,
        "lower80": 0.0,
        "upper80": 0.03
      },
      "transport_efficiency": {
        "estimate": 0.93,
        "lower80": 0.82,
        "upper80": 1.0
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.42,
        "upper80": 0.71
      },
      "energy_efficiency": {
        "estimate": 0.27,
        "lower80": 0.15,
        "upper80": 0.4
      },
      "faradaic_efficiency": {
        "estimate": 0.38,
        "lower80": 0.25,
        "upper80": 0.51
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.309,
        "lower80": 0.12,
        "upper80": 0.4
      },
      "selective_product_yield": {
        "estimate": 0.035,
        "lower80": 0.012,
        "upper80": 0.07
      },
      "transport_efficiency": {
        "estimate": 0.42,
        "lower80": 0.28,
        "upper80": 0.56
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.9,
        "lower80": 0.84,
        "upper80": 0.95
      },
      "energy_efficiency": {
        "estimate": 0.88,
        "lower80": 0.8,
        "upper80": 0.95
      },
      "faradaic_efficiency": {
        "estimate": 0.94,
        "lower80": 0.86,
        "upper80": 0.99
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.623,
        "lower80": 0.56,
        "upper80": 0.68
      },
      "selective_product_yield": {
        "estimate": 0.18,
        "lower80": 0.12,
        "upper80": 0.25
      },
      "transport_efficiency": {
        "estimate": 0.91,
        "lower80": 0.82,
        "upper80": 0.98
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.45,
        "upper80": 0.76
      },
      "energy_efficiency": {
        "estimate": 0.36,
        "lower80": 0.2,
        "upper80": 0.51
      },
      "faradaic_efficiency": {
        "estimate": 0.45,
        "lower80": 0.28,
        "upper80": 0.6
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.338,
        "lower80": 0.08,
        "upper80": 0.44
      },
      "selective_product_yield": {
        "estimate": 0.025,
        "lower80": 0.006,
        "upper80": 0.055
      },
      "transport_efficiency": {
        "estimate": 0.48,
        "lower80": 0.31,
        "upper80": 0.64
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.95,
        "lower80": 0.89,
        "upper80": 0.99
      },
      "energy_efficiency": {
        "estimate": 0.93,
        "lower80": 0.84,
        "upper80": 0.99
      },
      "faradaic_efficiency": {
        "estimate": 0.93,
        "lower80": 0.84,
        "upper80": 0.99
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.644,
        "lower80": 0.57,
        "upper80": 0.71
      },
      "selective_product_yield": {
        "estimate": 0.2,
        "lower80": 0.13,
        "upper80": 0.28
      },
      "transport_efficiency": {
        "estimate": 0.91,
        "lower80": 0.8,
        "upper80": 0.98
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.5,
        "lower80": 0.33,
        "upper80": 0.66
      },
      "energy_efficiency": {
        "estimate": 0.22,
        "lower80": 0.09,
        "upper80": 0.36
      },
      "faradaic_efficiency": {
        "estimate": 0.25,
        "lower80": 0.12,
        "upper80": 0.4
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.257,
        "lower80": 0.05,
        "upper80": 0.35
      },
      "selective_product_yield": {
        "estimate": 0.025,
        "lower80": 0.005,
        "upper80": 0.055
      },
      "transport_efficiency": {
        "estimate": 0.3,
        "lower80": 0.15,
        "upper80": 0.46
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.86,
        "lower80": 0.76,
        "upper80": 0.94
      },
      "energy_efficiency": {
        "estimate": 0.86,
        "lower80": 0.74,
        "upper80": 0.95
      },
      "faradaic_efficiency": {
        "estimate": 0.62,
        "lower80": 0.48,
        "upper80": 0.75
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.511,
        "lower80": 0.42,
        "upper80": 0.59
      },
      "selective_product_yield": {
        "estimate": 0.09,
        "lower80": 0.04,
        "upper80": 0.15
      },
      "transport_efficiency": {
        "estimate": 0.63,
        "lower80": 0.48,
        "upper80": 0.77
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.37,
        "upper80": 0.7
      },
      "energy_efficiency": {
        "estimate": 0.28,
        "lower80": 0.13,
        "upper80": 0.44
      },
      "faradaic_efficiency": {
        "estimate": 0.35,
        "lower80": 0.18,
        "upper80": 0.52
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.3,
        "lower80": 0.11,
        "upper80": 0.41
      },
      "selective_product_yield": {
        "estimate": 0.04,
        "lower80": 0.012,
        "upper80": 0.085
      },
      "transport_efficiency": {
        "estimate": 0.4,
        "lower80": 0.22,
        "upper80": 0.57
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.88,
        "lower80": 0.77,
        "upper80": 0.95
      },
      "energy_efficiency": {
        "estimate": 0.84,
        "lower80": 0.72,
        "upper80": 0.94
      },
      "faradaic_efficiency": {
        "estimate": 0.82,
        "lower80": 0.68,
        "upper80": 0.93
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.545,
        "lower80": 0.45,
        "upper80": 0.63
      },
      "selective_product_yield": {
        "estimate": 0.075,
        "lower80": 0.025,
        "upper80": 0.14
      },
      "transport_efficiency": {
        "estimate": 0.8,
        "lower80": 0.64,
        "upper80": 0.91
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.42,
        "upper80": 0.71
      },
      "energy_efficiency": {
        "estimate": 0.27,
        "lower80": 0.15,
        "upper80": 0.4
      },
      "faradaic_efficiency": {
        "estimate": 0.38,
        "lower80": 0.25,
        "upper80": 0.51
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.309,
        "lower80": 0.12,
        "upper80": 0.4
      },
      "selective_product_yield": {
        "estimate": 0.035,
        "lower80": 0.012,
        "upper80": 0.07
      },
      "transport_efficiency": {
        "estimate": 0.42,
        "lower80": 0.28,
        "upper80": 0.56
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.9,
        "lower80": 0.84,
        "upper80": 0.95
      },
      "energy_efficiency": {
        "estimate": 0.88,
        "lower80": 0.8,
        "upper80": 0.95
      },
      "faradaic_efficiency": {
        "estimate": 0.94,
        "lower80": 0.86,
        "upper80": 0.99
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.623,
        "lower80": 0.56,
        "upper80": 0.68
      },
      "selective_product_yield": {
        "estimate": 0.18,
        "lower80": 0.12,
        "upper80": 0.25
      },
      "transport_efficiency": {
        "estimate": 0.91,
        "lower80": 0.82,
        "upper80": 0.98
      }
    }
  ],
  "rationale": "Predictions extrapolate the campaign’s strong polarity effect, the productive but bounded positive-potential window, the electrolyte and solvent rankings, and approximately time/charge-limited conversion near +1 V. The smaller reagent inventory should raise fractional conversion at a given productive charge, while +0.8 V should be somewhat slower than the observed +1.0 V runs. Negative-potential estimates remain low and have wider intervals. The 500 mA cases are predicted close to their 100 mA counterparts because at fixed ±0.8 V the cell is likely voltage/kinetics-limited rather than current-cap-limited; uncertainty intervals allow model error. Score estimates apply the public weighted components and the selective-yield gate, making the short 600 s cases especially uncertain."
}
```
