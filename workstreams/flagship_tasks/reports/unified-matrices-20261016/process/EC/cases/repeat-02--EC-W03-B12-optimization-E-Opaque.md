# repeat-02/EC-W03-B12-optimization-E-Opaque

既有科学公开材料；非provider内部推理。

来源：D:\CW267\a2\repeat-02\EC-W03-B12-optimization-E-Opaque\participant\optimization-E-Opaque

## 同期笔记

### v1 · 公开事件 0

# Electrochemical campaign hypotheses

## H1 [tentative]
At fixed loading (0.020 mol reagent in 0.050 L solvent), balanced efficiency will show a bounded optimum in potential magnitude and electrolysis duration: too little charge gives low conversion, while excessive forcing lowers selectivity/energy efficiency and raises degradation or risk.

## H2 [tentative]
Solvent and electrolyte identities may strongly affect transport and ohmic efficiency, so an initial broad material/polarity screen should precede local optimization.

**Pre-experiment testable expectation.** Across broad combinations of solvent, electrolyte, potential sign, current cap, and duration, at least one moderate condition should outperform both weak/short and strong/long extremes. I will hold loading constant where possible, use final assays as authoritative, and reserve later batches for confirmation/local refinement of the best region. A UV-vis snapshot may diagnose efficiency trends but will not replace final assay.

### v2 · 公开事件 63

# Electrochemical campaign hypotheses

## H1 [supported in tested scope]
At 0.020 mol reagent in 0.050 L, performance has a bounded dependence on forcing. Positive 1.5 V gave essentially no useful product at both 800 s and 4000 s (final assays runner-operation-0021 and -0014), whereas negative potentials gave nonzero scores and improving yield when magnitude was reduced and duration increased: −1.5 V/800 s < −1.0 V/4000 s < −0.5 V/8000 s for S0/E0 (runner-operation-0028, -0035, -0042). This sequence confounds potential with duration, so it supports a useful low-magnitude/long-duration region rather than a separable causal law.

## H2 [supported, identities still confounded]
At −0.5 V, 500 mA cap, 8000 s, paired S1/E1 substantially outperformed paired S0/E0, S2/E2, and S3/E3 (scores about 0.496, 0.240, 0.367, 0.213; runner-operation-0049, -0042, -0056, -0063). Because solvent and electrolyte were changed together, their individual contributions remain unresolved. S1/E1 is the current optimization region.

## H3 [tentative]
For S1/E1, extending −0.5 V electrolysis may raise conversion/yield, but excessive exposure could reduce selectivity or efficiency. A modest potential increase might trade some energy/selectivity for conversion. Remaining batches will test these local alternatives and, if neither improves, confirm the best observed condition.

### v3 · 公开事件 84

# Electrochemical campaign hypotheses

## H1 [supported in tested scope]
At 0.020 mol reagent in 0.050 L, useful conversion favored negative, relatively low-magnitude potential and long exposure. Positive 1.5 V was unproductive in tested runs (runner-operation-0014, -0021); negative conditions gave useful product, with the best region near −0.5 V. Potential and duration were not fully crossed, so this is an operating-region conclusion, not a separable kinetic law.

## H2 [supported for paired formulations; components unresolved]
At −0.5 V, 500 mA cap, 8000 s, S1/E1 outperformed paired S0/E0, S2/E2, and S3/E3 (runner-operation-0049 versus -0042, -0056, -0063). Solvent and electrolyte effects remain confounded because identities were paired rather than factorially separated.

## H3 [supported locally]
Within S1/E1 at −0.5 V, increasing duration from 8000 to 12000 to 14400 s increased conversion and selective product yield and raised score from about 0.496 to 0.576 to 0.607 (runner-operation-0049, -0070, -0084). At 12000 s, increasing magnitude to −0.7 V lowered score to about 0.548 despite somewhat higher energy/ohmic efficiency, chiefly alongside lower yield/selectivity (runner-operation-0077 versus -0070). Differences exceed the reported final-assay noise for the major yield/conversion changes, though no exact replicate was performed.

## Recommendation decision
Select batch 12: 0.020 mol reagent, 0.050 L S1, E1, −0.5 V, 500 mA cap, 14400 s. It achieved the highest observed balanced-efficiency score (about 0.607) with conversion about 0.896 and selective product yield about 0.650 at safety risk about 0.083 (runner-operation-0084). The optimum may lie beyond the tested duration boundary or at a slightly different potential; this remains unresolved.

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
    "electrochemical_conversion": 0.017460986971855164,
    "electrochemical_selectivity": 0.8394781947135925,
    "energy_efficiency": 0.5888849496841431,
    "faradaic_efficiency": 0.6321778893470764,
    "ohmic_efficiency": 0.9659870862960815,
    "pH_normalized": 0.23031213879585266,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.6034741401672363
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
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1.5
    },
    {
      "duration_s": 4000,
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
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.010023192502558231,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.0,
    "ohmic_efficiency": 0.91678786277771,
    "pH_normalized": 0.2276168018579483,
    "precipitation_signal": 1.0,
    "safety_risk": 0.05933958664536476,
    "score": 0.035987500101327896,
    "selective_product_yield": 0.00897990819066763,
    "transport_efficiency": 0.02610676921904087
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
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": 1.5
    },
    {
      "duration_s": 800,
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
    "cost": 0.2874000072479248,
    "electrochemical_conversion": 0.0,
    "electrochemical_selectivity": 0.0,
    "energy_efficiency": 0.0,
    "faradaic_efficiency": 0.0,
    "ohmic_efficiency": 0.9035614728927612,
    "pH_normalized": 0.2283317893743515,
    "precipitation_signal": 0.9871104955673218,
    "safety_risk": 0.05933958664536476,
    "score": 0.0,
    "selective_product_yield": 0.0,
    "transport_efficiency": 0.0
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
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1.5
    },
    {
      "duration_s": 800,
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
    "cost": 0.2874000072479248,
    "electrochemical_conversion": 0.008792336098849773,
    "electrochemical_selectivity": 0.4562331438064575,
    "energy_efficiency": 0.0060824379324913025,
    "faradaic_efficiency": 0.14958903193473816,
    "ohmic_efficiency": 0.9157196283340454,
    "pH_normalized": 0.22764120995998383,
    "precipitation_signal": 0.9878587126731873,
    "safety_risk": 0.05933958664536476,
    "score": 0.06037713587284088,
    "selective_product_yield": 0.0068879881873726845,
    "transport_efficiency": 0.11810148507356644
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
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -1
    },
    {
      "duration_s": 4000,
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
    "cost": 0.2930000126361847,
    "electrochemical_conversion": 0.064767025411129,
    "electrochemical_selectivity": 0.5490882396697998,
    "energy_efficiency": 0.046485260128974915,
    "faradaic_efficiency": 0.1293499618768692,
    "ohmic_efficiency": 0.8736987709999084,
    "pH_normalized": 0.23260200023651123,
    "precipitation_signal": 0.9871851205825806,
    "safety_risk": 0.05933958664536476,
    "score": 0.20563659071922302,
    "selective_product_yield": 0.04173976182937622,
    "transport_efficiency": 0.11884049326181412
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
      "electrolyte_profile": 0,
      "operation": "set_potential",
      "potential_V": -0.5
    },
    {
      "duration_s": 8000,
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
    "cost": 0.2930000126361847,
    "electrochemical_conversion": 0.12102726101875305,
    "electrochemical_selectivity": 0.6115096807479858,
    "energy_efficiency": 0.15607492625713348,
    "faradaic_efficiency": 0.13875392079353333,
    "ohmic_efficiency": 0.7511903047561646,
    "pH_normalized": 0.229326069355011,
    "precipitation_signal": 0.9978154301643372,
    "safety_risk": 0.05933958664536476,
    "score": 0.24015118181705475,
    "selective_product_yield": 0.08252670615911484,
    "transport_efficiency": 0.1140705868601799
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
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -0.5
    },
    {
      "duration_s": 8000,
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
    "cost": 0.31299999356269836,
    "electrochemical_conversion": 0.5224549770355225,
    "electrochemical_selectivity": 0.6972336769104004,
    "energy_efficiency": 0.4449467360973358,
    "faradaic_efficiency": 0.49626052379608154,
    "ohmic_efficiency": 0.667582631111145,
    "pH_normalized": 0.21038967370986938,
    "precipitation_signal": 0.6467019319534302,
    "safety_risk": 0.08273958414793015,
    "score": 0.49613356590270996,
    "selective_product_yield": 0.36545681953430176,
    "transport_efficiency": 0.4996608793735504
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
      "current_mA": 500,
      "electrolyte_profile": 2,
      "operation": "set_potential",
      "potential_V": -0.5
    },
    {
      "duration_s": 8000,
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
    "cost": 0.3449999988079071,
    "electrochemical_conversion": 0.4413793087005615,
    "electrochemical_selectivity": 0.5908501744270325,
    "energy_efficiency": 0.22092442214488983,
    "faradaic_efficiency": 0.43875229358673096,
    "ohmic_efficiency": 0.39490824937820435,
    "pH_normalized": 0.17212991416454315,
    "precipitation_signal": 0.00031451715040020645,
    "safety_risk": 0.10073958337306976,
    "score": 0.3669852018356323,
    "selective_product_yield": 0.24537484347820282,
    "transport_efficiency": 0.43225693702697754
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
      "current_mA": 500,
      "electrolyte_profile": 3,
      "operation": "set_potential",
      "potential_V": -0.5
    },
    {
      "duration_s": 8000,
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
    "cost": 0.32499998807907104,
    "electrochemical_conversion": 0.08360301703214645,
    "electrochemical_selectivity": 0.5174821019172668,
    "energy_efficiency": 0.17929650843143463,
    "faradaic_efficiency": 0.07384564727544785,
    "ohmic_efficiency": 0.7861926555633545,
    "pH_normalized": 0.28515711426734924,
    "precipitation_signal": 0.008188718929886818,
    "safety_risk": 0.11333958804607391,
    "score": 0.21277852356433868,
    "selective_product_yield": 0.06225615739822388,
    "transport_efficiency": 0.0946769118309021
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
      "solvent": 1,
      "volume_L": 0.05
    },
    {
      "current_mA": 500,
      "electrolyte_profile": 1,
      "operation": "set_potential",
      "potential_V": -0.5
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
    "cost": 0.31700000166893005,
    "electrochemical_conversion": 0.7835226655006409,
    "electrochemical_selectivity": 0.7184351682662964,
    "energy_efficiency": 0.45953506231307983,
    "faradaic_efficiency": 0.5031311511993408,
    "ohmic_efficiency": 0.6252703666687012,
    "pH_normalized": 0.20839183032512665,
    "precipitation_signal": 0.6566107869148254,
    "safety_risk": 0.08273958414793015,
    "score": 0.5763359665870667,
    "selective_product_yield": 0.5348091125488281,
    "transport_efficiency": 0.5044807195663452
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
      "potential_V": -0.7
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
    "cost": 0.32179999351501465,
    "electrochemical_conversion": 0.7154908776283264,
    "electrochemical_selectivity": 0.6600223183631897,
    "energy_efficiency": 0.5077949166297913,
    "faradaic_efficiency": 0.45378077030181885,
    "ohmic_efficiency": 0.7427200078964233,
    "pH_normalized": 0.20937687158584595,
    "precipitation_signal": 0.6644999384880066,
    "safety_risk": 0.08273958414793015,
    "score": 0.5479881763458252,
    "selective_product_yield": 0.4709971249103546,
    "transport_efficiency": 0.4609606862068176
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
      "potential_V": -0.5
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
    "cost": 0.31940001249313354,
    "electrochemical_conversion": 0.896446168422699,
    "electrochemical_selectivity": 0.6820757985115051,
    "energy_efficiency": 0.4363401532173157,
    "faradaic_efficiency": 0.45520463585853577,
    "ohmic_efficiency": 0.652097225189209,
    "pH_normalized": 0.20989719033241272,
    "precipitation_signal": 0.6578359007835388,
    "safety_risk": 0.08273958414793015,
    "score": 0.6066943407058716,
    "selective_product_yield": 0.6495068073272705,
    "transport_efficiency": 0.4764295816421509
  }
}
```

## K1 封存报告

## Mechanism report

### 1. Empirical operating picture

The system behaves like a polarity-sensitive electrochemical conversion whose outcome depends jointly on potential, exposure time, solvent/electrolyte formulation, and transport losses. The best observed region used 0.020 mol reagent in 0.050 L solvent-S1, electrolyte-E1, a configured potential of −0.5 V, a 500 mA current cap, and long electrolysis. Batch 12, run for 14,400 s, gave the highest measured balanced-efficiency-v2 score, 0.6067. Its final assay reported conversion 0.8964, selectivity 0.6821, selective-product yield 0.6495, faradaic efficiency 0.4552, transport efficiency 0.4764, ohmic efficiency 0.6521, and energy efficiency 0.4363. Observed safety risk was 0.0827, well below the public limit of 0.65.

The score is consistent with the public weighted relation

S_base = 0.30Y + 0.10X + 0.15S_el + 0.15η_energy + 0.12η_F + 0.10η_transport + 0.08η_ohmic,

where Y is selective-product yield and X is electrochemical conversion. The public yield gate appears to multiply this base score by approximately min(1,Y/0.02). This explains why very low-yield batches received greatly suppressed scores. Thus the campaign objective was not simply maximum conversion: it rewarded conversion and yield while retaining selectivity and several electrical-efficiency terms.

### 2. Potential polarity and magnitude

The clearest mechanistic feature is polarity asymmetry. At otherwise matched S0/E0 conditions, batches 3 and 4 both used a 500 mA cap and 800 s, but batch 3 used +1.5 V and batch 4 used −1.5 V. Batch 3 produced measured conversion, selectivity, selective yield, faradaic efficiency, and transport efficiency all at or clipped to zero, with score 0. Batch 4 produced conversion 0.00879, selectivity 0.456, yield 0.00689, faradaic efficiency 0.150, transport efficiency 0.118, and score 0.0604. This direct sign comparison supports a target-forming cathodic or otherwise negative-potential pathway.

Positive-potential results were consistently poor. Batch 2 used S0/E0, +1.5 V, 500 mA, and 4,000 s; it had conversion reported as zero, selectivity 0.0100, yield 0.00898, and score 0.0360. The small mismatch between zero processed conversion and nonzero yield is most plausibly endpoint noise or clipping near zero rather than evidence for appreciable productive chemistry. Batch 1 at +1.0 V, 100 mA, and 600 s gave conversion 0.0175 and apparently high selectivity 0.839, but selective yield was zero and the score was zero. At such low product level, the high selectivity estimate does not establish a productive positive-potential mechanism.

Among negative conditions in S0/E0, lower-magnitude potential combined with longer exposure improved outcomes:

- Batch 4: −1.5 V, 800 s — conversion 0.00879, yield 0.00689, score 0.0604.
- Batch 5: −1.0 V, 4,000 s — conversion 0.0648, yield 0.0417, score 0.2056.
- Batch 6: −0.5 V, 8,000 s — conversion 0.1210, yield 0.0825, score 0.2402.

Because potential and time changed together, these three batches do not separately identify their effects. They nevertheless locate a useful region at moderate negative potential and long duration rather than strongly negative, short electrolysis.

A cleaner local potential comparison was obtained in S1/E1 at 12,000 s. Batch 10 at −0.5 V scored 0.5763, whereas batch 11 at −0.7 V scored 0.5480. Batch 11 had somewhat higher energy and ohmic efficiencies (0.508 and 0.743 versus 0.460 and 0.625), but lower conversion (0.715 versus 0.784), selectivity (0.660 versus 0.718), yield (0.471 versus 0.535), faradaic efficiency (0.454 versus 0.503), and transport efficiency (0.461 versus 0.504). Thus, in this local region, extra potential magnitude did not improve productive throughput. It likely increased nonproductive charge transfer or shifted the reaction network away from the desired product.

### 3. Time dependence and possible kinetic sequence

The strongest controlled trend was duration at fixed composition and electrical settings. Batches 7, 10, and 12 all used 0.020 mol reagent, 0.050 L S1, E1, −0.5 V, and a 500 mA cap:

- Batch 7, 8,000 s: conversion 0.5225, selectivity 0.6972, yield 0.3655, score 0.4961.
- Batch 10, 12,000 s: conversion 0.7835, selectivity 0.7184, yield 0.5348, score 0.5763.
- Batch 12, 14,400 s: conversion 0.8964, selectivity 0.6821, yield 0.6495, score 0.6067.

Conversion and yield increased monotonically across the measured interval. Selectivity improved slightly from 8,000 to 12,000 s and then fell by 14,400 s. Faradaic, transport, and energy efficiencies were also slightly lower in batch 12 than batch 10. This suggests that the desired conversion continued late in the run, while depletion, product degradation, or competing reactions became increasingly important. Because yield carried the largest score weight, its continued increase outweighed those efficiency losses.

A plausible phenomenological model is

-dR/dt = [k_target(E,M) + k_side(E,M)]R,

dP/dt = k_target(E,M)R − k_degradation(E,M)P,

where R is reactant, P is desired product, E is potential, and M represents the coupled solvent/electrolyte medium. Negative potential makes k_target appreciable, while excessive magnitude may increase k_side or k_degradation. This form can produce increasing conversion with time, an intermediate selectivity maximum, and eventual efficiency decline. It is a conjectural model: no species-resolved time series was measured, so the individual rate constants cannot be estimated.

The configured charge ceilings, I_cap·t, ranged from 400 C in batches 3 and 4 to 7,200 C in batch 12, but these are not measured delivered charges. The stated current was a cap, and no current transient or integrated charge was observed. Consequently, conversion cannot legitimately be interpreted as a direct Faraday-law calibration from the configured cap alone.

### 4. Solvent/electrolyte coupling

Medium selection exerted a large effect. Batches 6–9 used identical −0.5 V, 500 mA, 8,000 s settings but tested paired formulations:

- Batch 6, S0/E0: conversion 0.1210, yield 0.0825, score 0.2402.
- Batch 7, S1/E1: conversion 0.5225, yield 0.3655, score 0.4961.
- Batch 8, S2/E2: conversion 0.4414, yield 0.2454, score 0.3670.
- Batch 9, S3/E3: conversion 0.0836, yield 0.0623, score 0.2128.

S1/E1 offered the best overall balance. S2/E2 supported fairly high conversion and faradaic efficiency (0.4388) but had low ohmic efficiency (0.3949), low energy efficiency (0.2209), and lower selectivity (0.5909). S3/E3 retained good ohmic efficiency (0.7862) yet had very poor faradaic and transport efficiencies (0.0738 and 0.0947), consistent with current passing through non-target processes despite relatively low resistive loss. S0/E0 had high ohmic efficiency in several runs but weak productive conversion, showing that conductivity alone did not determine performance.

A useful conceptual decomposition is

j_effective = min[j_cap, G(M)f(E)],

productive rate ∝ j_effective·η_F(E,M)·η_transport(E,M),

with additional selectivity and degradation factors determining final product yield. In this view, ohmic efficiency describes only one loss channel. A medium can conduct well but still deliver charge to side reactions or suffer poor mass transport.

Solvent and electrolyte were always changed as matched pairs in the material screen. Therefore, their individual effects and any solvent×electrolyte interaction are unidentifiable. It is possible that S1 is beneficial regardless of electrolyte, that E1 is the dominant factor, or that only the S1/E1 combination is favorable. All three explanations remain compatible with the data.

### 5. Yield, selectivity, and secondary observables

Selective-product yield broadly tracked conversion multiplied by selectivity, suggesting a relation such as

Y ≈ X·S_el·η_recovery + measurement/process error.

For example, batch 7 had X·S_el ≈ 0.364, very close to its measured yield of 0.365. Agreement was not exact in every batch, especially near zero signal, so η_recovery should not be assumed equal to one or constant. Final-assay noise, clipping, and unobserved product loss can all contribute.

Normalized pH was nearly constant within a formulation: S1/E1 batches were around 0.208–0.210. Across media it ranged approximately from 0.172 in batch 8 to 0.285 in batch 9. Because pH covaried with formulation and was never independently manipulated, it cannot be assigned a causal role.

Precipitation signal also depended strongly on formulation: approximately 0.99 for S0/E0, 0.65 for S1/E1, and near zero for S2/E2 and S3/E3. Performance did not vary monotonically with that signal. It may report medium-specific phase behavior, solubility, or an unrelated endpoint feature rather than a necessary step in target formation.

Observed safety risk was stable within each tested formulation and increased from about 0.059 for S0/E0 to 0.083 for S1/E1, 0.101 for S2/E2, and 0.113 for S3/E3. This pattern suggests that the solvent formulation contributed more to the reported risk than duration or potential over the tested region. All runs remained far below the limit, so safety gating did not drive the optimum.

### 6. How the explanation changed

The initial hypothesis was a generic bounded optimum in potential and duration, with possible material effects. Batches 1–4 changed this into a polarity-specific explanation: positive potential was essentially unproductive, while matched −1.5 V produced detectable target formation. Batches 5 and 6 shifted attention toward milder negative potential with longer electrolysis. Batches 6–9 established that electrical settings alone were insufficient and that the medium strongly controlled conversion and efficiency; S1/E1 became the leading region. Batches 7, 10, and 12 then demonstrated a clear duration response in that region. Batch 11 showed that increasing potential magnitude from −0.5 to −0.7 V did not substitute beneficially for time.

### 7. Scope and unresolved alternatives

This account applies only to the tested anonymous benchmark materials, a fixed nominal loading of 0.020 mol in 0.050 L, and the tested electrical/time ranges. Important limitations are:

1. Reagent concentration, volume, and loading were not varied, so concentration and electrode-area-normalized rate laws are unidentifiable.
2. Current-cap effects were not independently mapped; all optimized batches used 500 mA, and actual current/charge was not observed.
3. Solvent and electrolyte effects are confounded by paired changes.
4. There were no exact replicates. Large differences such as the S1/E1 versus S0/E0 yield difference are much larger than the stated assay noise, but run-to-run process variability was not directly estimated.
5. No hidden species identities or mechanism-to-species mapping were public. Claims about reduction, degradation, conductivity, or mass transfer are phenomenological interpretations, not chemical identifications.
6. The best duration was the allowed upper boundary, 14,400 s. Performance might continue improving beyond that boundary, plateau, or decline; extrapolation is unsupported.
7. Plausible alternatives include potential-dependent electrode activation/passivation, formulation-dependent current delivery, product adsorption, or simple benchmark response surfaces rather than a literal sequence of chemical elementary steps.

Overall, the most defensible explanation is a cathodically favored conversion with a moderate-potential window. Productive performance is controlled by the coupled medium through faradaic and transport efficiencies, not merely ohmic conduction. At the best observed S1/E1 condition, longer exposure continued to raise conversion and yield, while declining selectivity and electrical efficiencies signaled the onset of competing late-stage processes.

## K2 封存报告

1. Supported, contradicted, and untested claims

No instance-specific prior, nominal material dossier, or claimed mechanism was supplied. The solvent and electrolyte labels were explicitly anonymous, so all world-specific claims were developed from the campaign.

The proposed polarity asymmetry was supported. The cleanest evidence was the matched 800 s comparison: batch 3 at +1.5 V gave zero measured productive response and score 0, while batch 4 at −1.5 V gave detectable yield (0.0069) and score 0.0604. This changed my judgment from a generic potential-window hypothesis to a cathodically favored operating picture.

The claim that formulation strongly affects performance was supported. Under the same −0.5 V, 500 mA, 8,000 s settings, paired S1/E1 in batch 7 scored 0.496, versus 0.240 for S0/E0 in batch 6, 0.367 for S2/E2 in batch 8, and 0.213 for S3/E3 in batch 9. However, separate solvent and electrolyte effects were untested because these factors were changed together.

A useful moderate-potential region was supported locally. At 12,000 s in S1/E1, batch 10 at −0.5 V scored 0.576, exceeding batch 11 at −0.7 V, which scored 0.548. The stronger potential improved some electrical components but reduced conversion, selectivity, yield, faradaic efficiency, and transport efficiency.

The initial expectation of an interior time optimum was not supported for the total score within the tested range. At otherwise identical S1/E1 conditions, score rose from 0.496 at 8,000 s in batch 7 to 0.576 at 12,000 s in batch 10 and 0.607 at 14,400 s in batch 12. Thus the score optimum remained at the duration boundary. A weaker version—late exposure begins to impair some components—was supported because selectivity and several efficiency terms declined from batch 10 to batch 12 even while conversion and yield continued to rise.

The approximation that selective yield broadly follows conversion times selectivity was supported qualitatively, especially in batch 7, but contradicted as an exact identity by discrepancies in batches 10 and 12 and by noisy near-zero results. It should remain a phenomenological approximation with recovery and measurement terms.

The claim that ohmic efficiency alone cannot explain productivity was supported: batch 9 retained high ohmic efficiency (0.786) but had faradaic efficiency 0.074, transport efficiency 0.095, and low yield. Conversely, batch 8 had poor ohmic efficiency but appreciably greater conversion.

Elementary kinetic claims—reactant depletion, product degradation, passivation, or named side reactions—were untested. No species-resolved time course, delivered-current trace, or mechanistic identity mapping was available. Likewise, causal roles for normalized pH and precipitation were untested; their values covaried with formulation.

2. One additional discriminating experiment

I would run S0/E1 at the established comparison condition: 0.020 mol reagent, 0.050 L solvent, −0.5 V, 500 mA cap, and 8,000 s, followed by final assay. This crosses the best electrolyte label into the S0 solvent and can be compared directly with batch 6 (S0/E0) and batch 7 (S1/E1).

If S0/E1 approached batch 7 in yield, faradaic/transport efficiency, and score, I would infer that E1 is the principal source of the S1/E1 advantage and weaken the explanation that a special paired-medium interaction is required. If it remained near batch 6, I would reject an E1-alone explanation and favor either a dominant S1 solvent effect or an S1×E1 interaction. An intermediate result would support approximately additive contributions. One experiment could not distinguish an S1-only effect from genuine synergy; that would subsequently require S1/E0.

3. Unused evidence, reliability, and goal effects

The final interpretation relied mainly on processed final-assay endpoints. Raw multichannel spectra and peak shapes were not inspected in detail, and the UV–visible intermediate measurements were not systematically fitted into a time-dependent model. Cost carried little mechanistic information and was not used. Normalized pH and precipitation were noted but not exploited quantitatively because they were confounded with formulation. No exact replicate data existed, so process repeatability remained unused because it was never measured.

The least reliable blind predictions are the cross-formulation cases Q05–Q10. S0/E1, S0/E3, and S2/E0 were never tested, so those predictions depend on an unverified decomposition of paired material effects. Long positive-potential predictions—especially Q04, Q06, Q08, Q10, and Q12—are also weak because the campaign tested +1.0 V only briefly and +1.5 V under different durations, not +0.8 V for 7,200 s. All prediction batches also changed loading, volume, and sometimes addition order relative to the main campaign, while concentration and order effects were not mapped. Q11 is relatively better anchored because it is closest to the tested negative-potential S0/E0 region.

The recommendation of batch 12 is reliable as the best observed batch, but less reliable as a global optimum: it had no exact replicate, used the maximum allowed duration, and did not separate solvent from electrolyte effects. Performance beyond 14,400 s or at nearby potentials remains unknown.

The assigned score-maximization goal did affect evidence collection. After batch 7 identified S1/E1 as promising, the remaining experiments emphasized duration and local potential optimization, producing higher scores but leaving fewer opportunities for cross-formulation tests, current-cap mapping, positive-potential characterization, or replication. This created a real optimization-versus-identification tradeoff, although there was no clear conflict with safety because every observed risk remained far below the stated limit.

## Q 封存预测

```json
{
  "predictions": [
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.38,
        "upper80": 0.78
      },
      "energy_efficiency": {
        "estimate": 0.38,
        "lower80": 0.18,
        "upper80": 0.57
      },
      "faradaic_efficiency": {
        "estimate": 0.22,
        "lower80": 0.08,
        "upper80": 0.4
      },
      "query_id": "Q01",
      "score": {
        "estimate": 0.055,
        "lower80": 0,
        "upper80": 0.16
      },
      "selective_product_yield": {
        "estimate": 0.004,
        "lower80": 0,
        "upper80": 0.015
      },
      "transport_efficiency": {
        "estimate": 0.2,
        "lower80": 0.06,
        "upper80": 0.38
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.82,
        "lower80": 0.6,
        "upper80": 0.94
      },
      "energy_efficiency": {
        "estimate": 0.62,
        "lower80": 0.45,
        "upper80": 0.77
      },
      "faradaic_efficiency": {
        "estimate": 0.65,
        "lower80": 0.46,
        "upper80": 0.8
      },
      "query_id": "Q02",
      "score": {
        "estimate": 0.044,
        "lower80": 0,
        "upper80": 0.13
      },
      "selective_product_yield": {
        "estimate": 0.002,
        "lower80": 0,
        "upper80": 0.012
      },
      "transport_efficiency": {
        "estimate": 0.62,
        "lower80": 0.43,
        "upper80": 0.78
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.58,
        "lower80": 0.4,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.16,
        "lower80": 0.05,
        "upper80": 0.34
      },
      "faradaic_efficiency": {
        "estimate": 0.16,
        "lower80": 0.04,
        "upper80": 0.34
      },
      "query_id": "Q03",
      "score": {
        "estimate": 0.226,
        "lower80": 0.07,
        "upper80": 0.32
      },
      "selective_product_yield": {
        "estimate": 0.03,
        "lower80": 0.008,
        "upper80": 0.075
      },
      "transport_efficiency": {
        "estimate": 0.14,
        "lower80": 0.03,
        "upper80": 0.31
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.25,
        "upper80": 0.82
      },
      "energy_efficiency": {
        "estimate": 0.32,
        "lower80": 0.12,
        "upper80": 0.58
      },
      "faradaic_efficiency": {
        "estimate": 0.25,
        "lower80": 0.06,
        "upper80": 0.53
      },
      "query_id": "Q04",
      "score": {
        "estimate": 0.104,
        "lower80": 0,
        "upper80": 0.28
      },
      "selective_product_yield": {
        "estimate": 0.008,
        "lower80": 0,
        "upper80": 0.035
      },
      "transport_efficiency": {
        "estimate": 0.22,
        "lower80": 0.05,
        "upper80": 0.49
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.67,
        "lower80": 0.45,
        "upper80": 0.82
      },
      "energy_efficiency": {
        "estimate": 0.36,
        "lower80": 0.17,
        "upper80": 0.57
      },
      "faradaic_efficiency": {
        "estimate": 0.42,
        "lower80": 0.2,
        "upper80": 0.64
      },
      "query_id": "Q05",
      "score": {
        "estimate": 0.388,
        "lower80": 0.22,
        "upper80": 0.55
      },
      "selective_product_yield": {
        "estimate": 0.18,
        "lower80": 0.05,
        "upper80": 0.38
      },
      "transport_efficiency": {
        "estimate": 0.4,
        "lower80": 0.18,
        "upper80": 0.62
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.62,
        "lower80": 0.32,
        "upper80": 0.84
      },
      "energy_efficiency": {
        "estimate": 0.42,
        "lower80": 0.19,
        "upper80": 0.65
      },
      "faradaic_efficiency": {
        "estimate": 0.38,
        "lower80": 0.14,
        "upper80": 0.62
      },
      "query_id": "Q06",
      "score": {
        "estimate": 0.285,
        "lower80": 0.02,
        "upper80": 0.4
      },
      "selective_product_yield": {
        "estimate": 0.018,
        "lower80": 0,
        "upper80": 0.09
      },
      "transport_efficiency": {
        "estimate": 0.36,
        "lower80": 0.13,
        "upper80": 0.61
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.5,
        "lower80": 0.27,
        "upper80": 0.7
      },
      "energy_efficiency": {
        "estimate": 0.16,
        "lower80": 0.04,
        "upper80": 0.35
      },
      "faradaic_efficiency": {
        "estimate": 0.09,
        "lower80": 0,
        "upper80": 0.25
      },
      "query_id": "Q07",
      "score": {
        "estimate": 0.147,
        "lower80": 0.01,
        "upper80": 0.27
      },
      "selective_product_yield": {
        "estimate": 0.015,
        "lower80": 0,
        "upper80": 0.055
      },
      "transport_efficiency": {
        "estimate": 0.1,
        "lower80": 0,
        "upper80": 0.27
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.45,
        "lower80": 0.18,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.22,
        "lower80": 0.06,
        "upper80": 0.46
      },
      "faradaic_efficiency": {
        "estimate": 0.1,
        "lower80": 0,
        "upper80": 0.29
      },
      "query_id": "Q08",
      "score": {
        "estimate": 0.04,
        "lower80": 0,
        "upper80": 0.19
      },
      "selective_product_yield": {
        "estimate": 0.004,
        "lower80": 0,
        "upper80": 0.025
      },
      "transport_efficiency": {
        "estimate": 0.11,
        "lower80": 0,
        "upper80": 0.31
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.55,
        "lower80": 0.34,
        "upper80": 0.72
      },
      "energy_efficiency": {
        "estimate": 0.12,
        "lower80": 0.03,
        "upper80": 0.3
      },
      "faradaic_efficiency": {
        "estimate": 0.22,
        "lower80": 0.07,
        "upper80": 0.42
      },
      "query_id": "Q09",
      "score": {
        "estimate": 0.216,
        "lower80": 0.1,
        "upper80": 0.34
      },
      "selective_product_yield": {
        "estimate": 0.07,
        "lower80": 0.018,
        "upper80": 0.18
      },
      "transport_efficiency": {
        "estimate": 0.21,
        "lower80": 0.06,
        "upper80": 0.41
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.45,
        "lower80": 0.18,
        "upper80": 0.7
      },
      "energy_efficiency": {
        "estimate": 0.15,
        "lower80": 0.03,
        "upper80": 0.37
      },
      "faradaic_efficiency": {
        "estimate": 0.12,
        "lower80": 0,
        "upper80": 0.32
      },
      "query_id": "Q10",
      "score": {
        "estimate": 0.049,
        "lower80": 0,
        "upper80": 0.2
      },
      "selective_product_yield": {
        "estimate": 0.006,
        "lower80": 0,
        "upper80": 0.03
      },
      "transport_efficiency": {
        "estimate": 0.13,
        "lower80": 0.01,
        "upper80": 0.34
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.59,
        "lower80": 0.44,
        "upper80": 0.71
      },
      "energy_efficiency": {
        "estimate": 0.15,
        "lower80": 0.06,
        "upper80": 0.29
      },
      "faradaic_efficiency": {
        "estimate": 0.14,
        "lower80": 0.05,
        "upper80": 0.28
      },
      "query_id": "Q11",
      "score": {
        "estimate": 0.241,
        "lower80": 0.15,
        "upper80": 0.33
      },
      "selective_product_yield": {
        "estimate": 0.075,
        "lower80": 0.035,
        "upper80": 0.14
      },
      "transport_efficiency": {
        "estimate": 0.13,
        "lower80": 0.04,
        "upper80": 0.27
      }
    },
    {
      "electrochemical_selectivity": {
        "estimate": 0.4,
        "lower80": 0.14,
        "upper80": 0.68
      },
      "energy_efficiency": {
        "estimate": 0.2,
        "lower80": 0.05,
        "upper80": 0.44
      },
      "faradaic_efficiency": {
        "estimate": 0.12,
        "lower80": 0,
        "upper80": 0.33
      },
      "query_id": "Q12",
      "score": {
        "estimate": 0.096,
        "lower80": 0,
        "upper80": 0.25
      },
      "selective_product_yield": {
        "estimate": 0.01,
        "lower80": 0,
        "upper80": 0.045
      },
      "transport_efficiency": {
        "estimate": 0.13,
        "lower80": 0.01,
        "upper80": 0.35
      }
    }
  ],
  "rationale": "Predictions extrapolate the observed cathodic advantage, the S0/E0 time–potential trend, and the strong but solvent-confounded E1 and weak E3 paired-formulation behavior. Positive-potential and cross-formulation intervals are deliberately wide because those conditions were not directly mapped. Score estimates apply the published weighted components and the selective-yield gate; intervals include assay noise, lack of replicates, changed loading, unknown delivered current, and unresolved solvent–electrolyte interactions."
}
```
